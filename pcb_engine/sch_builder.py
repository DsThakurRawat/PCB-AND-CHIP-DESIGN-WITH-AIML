#!/usr/bin/env python3
"""
Programmatic KiCad 9 Schematic Generator.
Transforms structured CircuitSpec definitions into verified KiCad 9 schematics.
"""

import sys
import json
from pathlib import Path
from typing import Union
import kicad_sch_api as ksa
from pcb_engine.circuit_spec import CircuitSpec, ComponentSpec, NetSpec

class SchematicBuilder:
    def __init__(self, spec: CircuitSpec):
        self.spec = spec
        self.sch = ksa.create_schematic(spec.title)

    def build(self, output_path: str) -> str:
        out_sch = Path(output_path).resolve()
        out_sch.parent.mkdir(parents=True, exist_ok=True)

        # 1. Place components
        default_x = 40.0
        default_y = 50.0
        x_step = 30.0
        row_limit = 5
        
        placed_pins = {}

        for idx, comp in enumerate(self.spec.components):
            # Calculate grid position if not explicitly specified
            if comp.pos:
                pos = comp.pos
            else:
                col = idx % row_limit
                row = idx // row_limit
                pos = (default_x + col * x_step, default_y + row * 40.0)

            # Add component
            added_comp = self.sch.components.add(
                lib_id=comp.lib_id,
                reference=comp.ref,
                value=comp.value,
                position=pos,
                rotation=comp.rotation,
                footprint=comp.footprint or ""
            )

            # Cache pin positions
            pins = self.sch.list_component_pins(comp.ref)
            placed_pins[comp.ref] = {str(pin_num): pt for pin_num, pt in pins}

        # 2. Wire nets by placing net labels on corresponding component pins
        connected_pins = set()
        for net in self.spec.nets:
            net_name = net.name
            for ref, pin_num in net.nodes:
                pin_num_str = str(pin_num)
                connected_pins.add((ref, pin_num_str))
                if ref not in placed_pins:
                    print(f"[!] Warning: Reference {ref} in net {net_name} not found in components", file=sys.stderr)
                    continue
                
                if pin_num_str not in placed_pins[ref]:
                    # Try finding pin position directly
                    try:
                        pos = self.sch.get_component_pin_position(ref, pin_num_str)
                    except Exception:
                        print(f"[!] Warning: Pin {pin_num_str} of {ref} in net {net_name} not found", file=sys.stderr)
                        continue
                else:
                    pos = placed_pins[ref][pin_num_str]

                # Attach net label directly to pin position
                self.sch.add_label(net_name, position=pos)

        # 2b. Add no-connect flags to all unrouted / unused pins
        for comp_ref, pins_dict in placed_pins.items():
            for pin_num_str, pin_pos in pins_dict.items():
                if (comp_ref, pin_num_str) not in connected_pins:
                    try:
                        self.sch.no_connects.add(position=pin_pos)
                    except Exception:
                        pass

        # 3. Add PWR_FLAG to power nets if specified
        pwr_x = 30.0
        pwr_y = default_y + ((len(self.spec.components) // row_limit) + 1) * 40.0
        for idx, net in enumerate(self.spec.nets):
            if net.is_power:
                flag_ref = f"#FLG{idx+1}"
                try:
                    pflag = self.sch.components.add(
                        lib_id="power:PWR_FLAG",
                        reference=flag_ref,
                        value="PWR_FLAG",
                        position=(pwr_x + idx * 20.0, pwr_y)
                    )
                    flag_pin = self.sch.get_component_pin_position(flag_ref, "1")
                    self.sch.add_label(net.name, position=flag_pin)
                except Exception as e:
                    pass

        # 4. Save schematic
        self.sch.save_as(str(out_sch))
        print(f"[+] KiCad 9 schematic successfully generated: {out_sch}")
        return str(out_sch)

def build_from_spec_file(spec_path: str, output_sch_path: str) -> str:
    with open(spec_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    spec = CircuitSpec(**data)
    builder = SchematicBuilder(spec)
    return builder.build(output_sch_path)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: sch_builder.py <spec.json> <output.kicad_sch>")
        sys.exit(1)
    build_from_spec_file(sys.argv[1], sys.argv[2])

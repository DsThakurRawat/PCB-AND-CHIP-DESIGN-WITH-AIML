#!/usr/bin/env python3
"""
Programmatic KiCad 9 PCB Layout Generator.
Takes a structured CircuitSpec and places footprints, assigns netlists,
creates Edge.Cuts board outline, and adds silkscreen annotations.
"""

import sys
import json
from pathlib import Path
import pcbnew
from pcb_engine.circuit_spec import CircuitSpec

FOOTPRINT_DIR = Path("/usr/share/kicad/footprints")

def load_fp(lib_name: str, mod_name: str) -> pcbnew.FOOTPRINT:
    lib_path = FOOTPRINT_DIR / f"{lib_name}.pretty"
    if not lib_path.exists():
        raise FileNotFoundError(f"Footprint library not found: {lib_path}")
    fp = pcbnew.FootprintLoad(str(lib_path), mod_name)
    if not fp:
        raise ValueError(f"Could not load footprint '{mod_name}' from '{lib_name}'")
    return fp

class PCBBuilder:
    def __init__(self, spec: CircuitSpec, board_width: float = 60.0, board_height: float = 40.0):
        self.spec = spec
        self.board = pcbnew.BOARD()
        self.width = board_width
        self.height = board_height
        self.net_map = {}

    def setup_nets(self):
        # Net 0 is empty default net
        for idx, net in enumerate(self.spec.nets, start=1):
            net_info = pcbnew.NETINFO_ITEM(self.board, net.name)
            self.board.Add(net_info)
            self.net_map[net.name] = net_info

    def add_outline(self, x0: float = 100.0, y0: float = 100.0, margin: float = 5.0):
        # Draw Edge.Cuts rectangle
        pts = [
            (x0, y0),
            (x0 + self.width, y0),
            (x0 + self.width, y0 + self.height),
            (x0, y0 + self.height)
        ]
        edge_layer = pcbnew.Edge_Cuts
        for i in range(4):
            x1, y1 = pts[i]
            x2, y2 = pts[(i + 1) % 4]
            seg = pcbnew.PCB_SHAPE(self.board, pcbnew.SHAPE_T_SEGMENT)
            seg.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1), pcbnew.FromMM(y1)))
            seg.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2), pcbnew.FromMM(y2)))
            seg.SetWidth(pcbnew.FromMM(0.1))
            seg.SetLayer(edge_layer)
            self.board.Add(seg)

    def add_silkscreen_text(self, text: str, x: float, y: float, size: float = 1.2):
        txt = pcbnew.PCB_TEXT(self.board)
        txt.SetText(text)
        txt.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
        txt.SetLayer(pcbnew.F_SilkS)
        txt.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(size), pcbnew.FromMM(size)))
        self.board.Add(txt)

    def build(self, output_pcb_path: str, x0: float = 100.0, y0: float = 100.0) -> str:
        out_pcb = Path(output_pcb_path).resolve()
        out_pcb.parent.mkdir(parents=True, exist_ok=True)

        self.setup_nets()
        self.add_outline(x0, y0)
        self.add_silkscreen_text(self.spec.title, x0 + 5.0, y0 + 4.0, size=1.5)

        # Build pin to net lookup: {ref: {pin_num: net_info}}
        node_to_net = {}
        for net in self.spec.nets:
            net_info = self.net_map[net.name]
            for ref, pin_num in net.nodes:
                node_to_net.setdefault(ref, {})[str(pin_num)] = net_info

        # Auto-place components inside board
        margin_x = 10.0
        cur_x = x0 + margin_x
        cur_y = y0 + 16.0
        spacing = 9.0

        for comp in self.spec.components:
            if not comp.footprint or ":" not in comp.footprint:
                continue
            lib_name, mod_name = comp.footprint.split(":", 1)
            try:
                fp = load_fp(lib_name, mod_name)
            except Exception as e:
                print(f"[!] Warning: Could not load footprint {comp.footprint}: {e}", file=sys.stderr)
                continue

            fp.SetReference(comp.ref)
            fp.SetValue(comp.value)
            fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(cur_x), pcbnew.FromMM(cur_y)))
            
            # Connect pads to nets
            comp_net_assignments = node_to_net.get(comp.ref, {})
            for pad in fp.Pads():
                pad_num = pad.GetNumber()
                if pad_num in comp_net_assignments:
                    pad.SetNet(comp_net_assignments[pad_num])

            self.board.Add(fp)
            cur_x += spacing
            if (cur_x - x0) > (self.width - margin_x):
                cur_x = x0 + margin_x
                cur_y += 12.0

        pcbnew.SaveBoard(str(out_pcb), self.board)
        print(f"[+] PCB board saved successfully: {out_pcb}")
        return str(out_pcb)

def build_pcb_from_spec_file(spec_path: str, output_pcb_path: str, width: float = 65.0, height: float = 40.0) -> str:
    with open(spec_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    spec = CircuitSpec(**data)
    builder = PCBBuilder(spec, board_width=width, board_height=height)
    return builder.build(output_pcb_path)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: pcb_builder.py <spec.json> <output.kicad_pcb>")
        sys.exit(1)
    build_pcb_from_spec_file(sys.argv[1], sys.argv[2])

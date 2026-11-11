#!/usr/bin/env python3
"""
Step 2: Generate Dual-Channel 555 Tone Demonstrator Schematic
Author: Divyansh Rawat (Roll No: 124EC0030)
Verification: kicad-cli sch erc -> 0 errors, 0 warnings
"""

import sys
import json
import subprocess
from pathlib import Path

ROOT_DIR = Path("/home/divyansh-rawat/AIPCBDESIGN").resolve()
sys.path.insert(0, str(ROOT_DIR))

import kicad_sch_api as ksa
from pcb_engine.circuit_spec import ComponentSpec, NetSpec

EDIR = ROOT_DIR / "end_exam"
SCH_FILE = EDIR / "dual_555_tone_demonstrator.kicad_sch"
PRO_FILE = EDIR / "dual_555_tone_demonstrator.kicad_pro"

def build_schematic():
    print(" [*] Synthesizing Dual-Channel 555 Schematic...")
    sch = ksa.create_schematic("Dual inductance-sensitive tone demonstrator - A")
    sch.set_paper_size("A3")

    # Title Block
    sch.set_title_block(
        title="Dual Inductance-Sensitive Tone Demonstrator - A",
        date="2026-11-11",
        rev="v1.0",
        company="Electronic Prototyping and Manufacturing (EPM) - Laboratory",
        comments={
            1: "Author: Divyansh Rawat (Roll No: 124EC0030)",
            2: "Dual 555 Inductance-Sensitive Oscillator Demonstrator",
            3: "Layout Variant A (90 x 70 mm Double-Layer PCB)",
            4: "Department of ECE, IIIT Kurnool"
        }
    )

    # Visual Section Boxes
    # 1. Power Supply Subsystem (Left)
    sch.add_rectangle(start=(15, 15), end=(110, 185), stroke_width=0.3)
    sch.add_text("POWER SUPPLY (9V DC)", position=(20, 22), size=2.4, bold=True)

    # 2. Channel A Oscillator (Top-Right)
    sch.add_rectangle(start=(120, 15), end=(405, 135), stroke_width=0.3)
    sch.add_text("CHANNEL A: 555 OSCILLATOR", position=(125, 22), size=2.4, bold=True)

    # 3. Channel B Oscillator (Bottom-Right)
    sch.add_rectangle(start=(120, 145), end=(405, 265), stroke_width=0.3)
    sch.add_text("CHANNEL B: 555 OSCILLATOR", position=(125, 152), size=2.4, bold=True)

    # 4. Mechanical Mounting (Bottom-Left)
    sch.add_rectangle(start=(15, 195), end=(110, 265), stroke_width=0.3)
    sch.add_text("MECHANICAL (4x M3 HOLES)", position=(20, 202), size=2.4, bold=True)

    # Components list with verified through-hole footprints
    comps = [
        # --- POWER SUBSYSTEM ---
        ComponentSpec(ref="J1", lib_id="Connector_Generic:Conn_01x02", value="9V_INPUT_J_PWR", footprint="TerminalBlock_Phoenix:TerminalBlock_Phoenix_MPT-0,5-2-2.54_1x02_P2.54mm_Horizontal", pos=(35, 55)),
        ComponentSpec(ref="C1", lib_id="Device:C_Polarized", value="100uF_16V", footprint="Capacitor_THT:CP_Radial_D6.3mm_P2.50mm", pos=(60, 55)),
        ComponentSpec(ref="C2", lib_id="Device:C", value="100nF", footprint="Capacitor_THT:C_Disc_D4.3mm_W1.9mm_P5.00mm", pos=(80, 55)),
        ComponentSpec(ref="D1", lib_id="Device:LED", value="PWR_LED_GREEN", footprint="LED_THT:LED_D3.0mm", pos=(60, 95)),
        ComponentSpec(ref="R1", lib_id="Device:R", value="1k", footprint="Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal", pos=(80, 95)),
        ComponentSpec(ref="TP1", lib_id="Connector:TestPoint", value="TP_9V", footprint="TestPoint:TestPoint_THTPad_D1.5mm_Drill0.7mm", pos=(60, 135)),
        ComponentSpec(ref="TP2", lib_id="Connector:TestPoint", value="TP_GND", footprint="TestPoint:TestPoint_THTPad_D1.5mm_Drill0.7mm", pos=(80, 135)),

        # --- CHANNEL A ---
        ComponentSpec(ref="U1", lib_id="Timer:NE555P", value="NE555P", footprint="Package_DIP:DIP-8_W7.62mm", pos=(220, 75)),
        ComponentSpec(ref="J2", lib_id="Connector_Generic:Conn_01x02", value="L_A_10mH", footprint="Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical", pos=(150, 45)),
        ComponentSpec(ref="C3", lib_id="Device:C_Polarized", value="2.2uF", footprint="Capacitor_THT:CP_Radial_D5.0mm_P2.00mm", pos=(175, 45)),
        ComponentSpec(ref="R2", lib_id="Device:R", value="47k", footprint="Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal", pos=(175, 80)),
        ComponentSpec(ref="C4", lib_id="Device:C_Polarized", value="2.2uF", footprint="Capacitor_THT:CP_Radial_D5.0mm_P2.00mm", pos=(175, 115)),
        ComponentSpec(ref="C5", lib_id="Device:C_Polarized", value="10uF", footprint="Capacitor_THT:CP_Radial_D5.0mm_P2.00mm", pos=(280, 75)),
        ComponentSpec(ref="J3", lib_id="Connector_Generic:Conn_01x02", value="SPK_A_8R", footprint="Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical", pos=(320, 75)),
        ComponentSpec(ref="C6", lib_id="Device:C", value="100nF", footprint="Capacitor_THT:C_Disc_D4.3mm_W1.9mm_P5.00mm", pos=(245, 45)),
        ComponentSpec(ref="C7", lib_id="Device:C_Polarized", value="10uF", footprint="Capacitor_THT:CP_Radial_D5.0mm_P2.00mm", pos=(265, 45)),
        ComponentSpec(ref="TP3", lib_id="Connector:TestPoint", value="TP_OUT_A", footprint="TestPoint:TestPoint_THTPad_D1.5mm_Drill0.7mm", pos=(280, 110)),
        ComponentSpec(ref="TP4", lib_id="Connector:TestPoint", value="TP_TIM_A", footprint="TestPoint:TestPoint_THTPad_D1.5mm_Drill0.7mm", pos=(150, 80)),

        # --- CHANNEL B ---
        ComponentSpec(ref="U2", lib_id="Timer:NE555P", value="NE555P", footprint="Package_DIP:DIP-8_W7.62mm", pos=(220, 205)),
        ComponentSpec(ref="J4", lib_id="Connector_Generic:Conn_01x02", value="L_B_10mH", footprint="Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical", pos=(150, 175)),
        ComponentSpec(ref="C8", lib_id="Device:C_Polarized", value="2.2uF", footprint="Capacitor_THT:CP_Radial_D5.0mm_P2.00mm", pos=(175, 175)),
        ComponentSpec(ref="R3", lib_id="Device:R", value="47k", footprint="Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal", pos=(175, 210)),
        ComponentSpec(ref="C9", lib_id="Device:C_Polarized", value="2.2uF", footprint="Capacitor_THT:CP_Radial_D5.0mm_P2.00mm", pos=(175, 245)),
        ComponentSpec(ref="C10", lib_id="Device:C_Polarized", value="10uF", footprint="Capacitor_THT:CP_Radial_D5.0mm_P2.00mm", pos=(280, 205)),
        ComponentSpec(ref="J5", lib_id="Connector_Generic:Conn_01x02", value="SPK_B_8R", footprint="Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical", pos=(320, 205)),
        ComponentSpec(ref="C11", lib_id="Device:C", value="100nF", footprint="Capacitor_THT:C_Disc_D4.3mm_W1.9mm_P5.00mm", pos=(245, 175)),
        ComponentSpec(ref="C12", lib_id="Device:C_Polarized", value="10uF", footprint="Capacitor_THT:CP_Radial_D5.0mm_P2.00mm", pos=(265, 175)),
        ComponentSpec(ref="TP5", lib_id="Connector:TestPoint", value="TP_OUT_B", footprint="TestPoint:TestPoint_THTPad_D1.5mm_Drill0.7mm", pos=(280, 240)),
        ComponentSpec(ref="TP6", lib_id="Connector:TestPoint", value="TP_TIM_B", footprint="TestPoint:TestPoint_THTPad_D1.5mm_Drill0.7mm", pos=(150, 210)),

        # --- MECHANICAL MOUNTING HOLES ---
        ComponentSpec(ref="H1", lib_id="Mechanical:MountingHole", value="MountingHole_M3", footprint="MountingHole:MountingHole_3.2mm_M3", pos=(35, 225)),
        ComponentSpec(ref="H2", lib_id="Mechanical:MountingHole", value="MountingHole_M3", footprint="MountingHole:MountingHole_3.2mm_M3", pos=(55, 225)),
        ComponentSpec(ref="H3", lib_id="Mechanical:MountingHole", value="MountingHole_M3", footprint="MountingHole:MountingHole_3.2mm_M3", pos=(75, 225)),
        ComponentSpec(ref="H4", lib_id="Mechanical:MountingHole", value="MountingHole_M3", footprint="MountingHole:MountingHole_3.2mm_M3", pos=(95, 225)),
    ]

    placed_pins = {}
    for comp in comps:
        c = sch.components.add(
            lib_id=comp.lib_id,
            reference=comp.ref,
            value=comp.value,
            position=comp.pos
        )
        try:
            c.footprint = comp.footprint
        except Exception as e:
            print(f'Error setting footprint on {comp.ref}: {e}')

        pins = {}
        for pnum in ["1", "2", "3", "4", "5", "6", "7", "8", "A", "K"]:
            try:
                pt = sch.get_component_pin_position(comp.ref, pnum)
                pins[pnum] = pt
            except Exception:
                pass
        placed_pins[comp.ref] = pins

    # Netlist definition
    nets = [
        # Power & Ground
        NetSpec(name="GND", nodes=[
            ("J1", "2"),
            ("C1", "2"),
            ("C2", "2"),
            ("D1", "1"),  # cathode
            ("TP2", "1"),
            ("U1", "1"),
            ("C4", "2"),
            ("J3", "2"),
            ("C6", "2"),
            ("C7", "2"),
            ("U2", "1"),
            ("C9", "2"),
            ("J5", "2"),
            ("C11", "2"),
            ("C12", "2"),
        ]),
        NetSpec(name="+9V", nodes=[
            ("J1", "1"),
            ("C1", "1"),
            ("C2", "1"),
            ("R1", "1"),
            ("TP1", "1"),
            ("U1", "4"),
            ("U1", "8"),
            ("J2", "1"),
            ("C6", "1"),
            ("C7", "1"),
            ("U2", "4"),
            ("U2", "8"),
            ("J4", "1"),
            ("C11", "1"),
            ("C12", "1"),
        ]),
        NetSpec(name="NetLED_PWR", nodes=[
            ("R1", "2"),
            ("D1", "2"),  # anode
        ]),

        # Channel A
        NetSpec(name="TIMING_A", nodes=[
            ("U1", "7"),
            ("J2", "2"),
            ("C3", "1"),
            ("R2", "1"),
            ("TP4", "1"),
        ]),
        NetSpec(name="SENSE_A", nodes=[
            ("U1", "2"),
            ("U1", "6"),
            ("C3", "2"),
            ("R2", "2"),
            ("C4", "1"),
        ]),
        NetSpec(name="OUT_A", nodes=[
            ("U1", "3"),
            ("C5", "1"),
            ("TP3", "1"),
        ]),
        NetSpec(name="SPK_A_POS", nodes=[
            ("C5", "2"),
            ("J3", "1"),
        ]),

        # Channel B
        NetSpec(name="TIMING_B", nodes=[
            ("U2", "7"),
            ("J4", "2"),
            ("C8", "1"),
            ("R3", "1"),
            ("TP6", "1"),
        ]),
        NetSpec(name="SENSE_B", nodes=[
            ("U2", "2"),
            ("U2", "6"),
            ("C8", "2"),
            ("R3", "2"),
            ("C9", "1"),
        ]),
        NetSpec(name="OUT_B", nodes=[
            ("U2", "3"),
            ("C10", "1"),
            ("TP5", "1"),
        ]),
        NetSpec(name="SPK_B_POS", nodes=[
            ("C10", "2"),
            ("J5", "1"),
        ]),
    ]

    # Deterministic Outward Wiring with Clean Stubs & Net Labels
    connected_pins = set()
    used_wire_endpoints = set()

    for net in nets:
        net_name = net.name
        for ref, pin_num in net.nodes:
            pin_num_str = str(pin_num)
            connected_pins.add((ref, pin_num_str))
            if ref not in placed_pins or pin_num_str not in placed_pins[ref]:
                continue
            pt = placed_pins[ref][pin_num_str]
            comp_pos = next(c.pos for c in comps if c.ref == ref)

            stub_len = 6.35
            dx, dy = 0.0, 0.0

            if ref in ("U1", "U2"):
                # 555 IC:
                if pin_num_str in ("4", "7", "6", "2"):
                    dx = -stub_len
                elif pin_num_str == "3":
                    dx = stub_len
                elif pin_num_str in ("8", "5"):
                    dy = -stub_len
                elif pin_num_str == "1":
                    dy = stub_len
            elif ref.startswith("J"):
                # Connectors: route stubs outward
                if pin_num_str == "1":
                    dy = -stub_len
                else:
                    dy = stub_len
            elif ref.startswith("TP"):
                dy = -stub_len
            else:
                # 2-pin passives
                other_pins = [p for num, p in placed_pins[ref].items() if num != pin_num_str]
                if other_pins and abs(other_pins[0].x - pt.x) < 0.5:
                    dy = -stub_len if pt.y < other_pins[0].y else stub_len
                elif other_pins and abs(other_pins[0].y - pt.y) < 0.5:
                    dx = -stub_len if pt.x < other_pins[0].x else stub_len
                else:
                    if abs(pt.x - comp_pos[0]) > abs(pt.y - comp_pos[1]):
                        dx = stub_len if pt.x >= comp_pos[0] else -stub_len
                    else:
                        dy = stub_len if pt.y >= comp_pos[1] else -stub_len

            end_x = round(pt.x + dx, 2)
            end_y = round(pt.y + dy, 2)

            wire_key = ((round(pt.x, 2), round(pt.y, 2)), (end_x, end_y))
            if wire_key not in used_wire_endpoints:
                used_wire_endpoints.add(wire_key)
                sch.add_wire((pt.x, pt.y), (end_x, end_y))
                sch.add_label(net_name, position=(end_x, end_y))

    # Add no-connect flags to unused Pin 5 on U1 and U2
    for uref in ["U1", "U2"]:
        if "5" in placed_pins[uref]:
            p5 = placed_pins[uref]["5"]
            try:
                sch.no_connects.add(position=(p5.x, p5.y))
            except Exception:
                pass

    # Add PWR_FLAG for +9V and GND
    sch.components.add(lib_id="power:PWR_FLAG", reference="#FLG1", value="PWR_FLAG", position=(25, 45))
    p1 = sch.get_component_pin_position("#FLG1", "1")
    sch.add_wire((p1.x, p1.y), (p1.x, p1.y - 6.35))
    sch.add_label("+9V", position=(p1.x, p1.y - 6.35))

    sch.components.add(lib_id="power:PWR_FLAG", reference="#FLG2", value="PWR_FLAG", position=(25, 65))
    p2 = sch.get_component_pin_position("#FLG2", "1")
    sch.add_wire((p2.x, p2.y), (p2.x, p2.y + 6.35))
    sch.add_label("GND", position=(p2.x, p2.y + 6.35))

    sch.save_as(str(SCH_FILE))
    print(f" [✓] Schematic generated successfully at {SCH_FILE}")

def run_erc_validation():
    print(" [*] Running Automated ERC Check...")
    rpt_file = EDIR / "dual_555_erc.rpt"
    json_file = EDIR / "dual_555_erc.json"

    # Run kicad-cli sch erc
    cmd = [
        "kicad-cli", "sch", "erc",
        "--output", str(rpt_file),
        "--format", "json",
        str(SCH_FILE)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if rpt_file.exists():
        rpt_file.rename(json_file)

    cmd_rpt = [
        "kicad-cli", "sch", "erc",
        "--output", str(rpt_file),
        "--format", "report",
        str(SCH_FILE)
    ]
    subprocess.run(cmd_rpt, capture_output=True, text=True)

    with open(json_file) as f:
        erc_data = json.load(f)

    sheets = erc_data.get("sheets", [])
    total_violations = 0
    for s in sheets:
        violations = s.get("violations", [])
        total_violations += len(violations)

    print(f" [✓] ERC Completed: {total_violations} violations found.")
    if total_violations > 0:
        with open(rpt_file) as f:
            print(f.read())
        return False
    return True

if __name__ == "__main__":
    build_schematic()
    success = run_erc_validation()
    if not success:
        sys.exit(1)
    print("==================================================================")
    print(" [✓] STEP 2 SUCCESS: 0 ERC VIOLATIONS ACHIEVED!")
    print("==================================================================")

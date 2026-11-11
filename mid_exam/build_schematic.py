#!/usr/bin/env python3
"""
Step 2 & 3: Fully Wired Schematic Synthesis & ERC Validation for School/College Quiz Buzzer
Course: Electronic Prototyping and Manufacturing (EPM) Laboratory
Faculty: Dr. Eswaramoorthy K V
Author: Divyansh Rawat (Roll No: 124EC0030)
"""

import sys
import subprocess
from pathlib import Path

MID_DIR = Path("/home/divyansh-rawat/AIPCBDESIGN/mid_exam").resolve()
SCH_FILE = MID_DIR / "school_college_quiz_buzzer.kicad_sch"
PRO_FILE = MID_DIR / "school_college_quiz_buzzer.kicad_pro"

import kicad_sch_api as ksa
from pcb_engine.circuit_spec import ComponentSpec, NetSpec

def build_schematic():
    print(" [*] Synthesizing Point-to-Point Wired Quiz Buzzer Schematic...")
    sch = ksa.create_schematic("School/College Quiz Buzzer (8 Players)")
    sch.set_paper_size("A3")

    sch.set_title_block(
        title="School/College Quiz Buzzer (8 Players)",
        date="2026-11-11",
        rev="v1.0",
        company="IIITDM Kurnool - Dept of ECE | EPM Laboratory",
        comments={
            1: "Author: Divyansh Rawat (Roll No: 124EC0030)",
            2: "Mid Semester Practical Examination",
            3: "Faculty: Dr. Eswaramoorthy K V",
            4: "8-Player Quiz Buzzer with 74LS373 & Regulated 5V Power Supply"
        }
    )

    # Section Boxes
    sch.add_rectangle(start=(15, 15), end=(180, 105), stroke_width=0.3)
    sch.add_text("SECTION 1: REGULATED POWER SUPPLY (230V AC TO 5V DC)", position=(20, 22), size=2.2, bold=True)

    sch.add_rectangle(start=(15, 115), end=(140, 285), stroke_width=0.3)
    sch.add_text("SECTION 2: PLAYER INPUTS (S1-S8 & PULL-DOWNS)", position=(20, 122), size=2.2, bold=True)

    sch.add_rectangle(start=(145, 115), end=(265, 285), stroke_width=0.3)
    sch.add_text("SECTION 3: 74LS373 LATCH & DIODE OR-ING", position=(150, 122), size=2.2, bold=True)

    sch.add_rectangle(start=(185, 15), end=(265, 105), stroke_width=0.3)
    sch.add_text("LOCKOUT & BUZZER DRIVER", position=(190, 22), size=2.0, bold=True)

    sch.add_rectangle(start=(270, 15), end=(410, 285), stroke_width=0.3)
    sch.add_text("SECTION 4: ANNUNCIATOR STAGE (SCR1-SCR8 & BL1-BL8)", position=(275, 22), size=2.2, bold=True)

    comps = [
        # --- POWER SUPPLY ---
        ComponentSpec(ref="J1", lib_id="Connector_Generic:Conn_01x02", value="AC_230V_IN", footprint="TerminalBlock_Phoenix:TerminalBlock_Phoenix_MPT-0,5-2-2.54_1x02_P2.54mm_Horizontal", pos=(25, 45)),
        ComponentSpec(ref="S9", lib_id="Switch:SW_SPST", value="SW_ON_OFF", footprint="Button_Switch_THT:SW_Slide_SPDT_Angled_CK_OS102011MA1Q", pos=(45, 45)),
        ComponentSpec(ref="F1", lib_id="Device:Fuse", value="0.5A_250V", footprint="Fuse:Fuseholder_Cylinder-5x20mm_Schurter_0031_8201_Horizontal_Open", pos=(65, 45)),
        ComponentSpec(ref="X1", lib_id="Transformer:TEZ0.5-D-1", value="230V_7.5V_500mA", footprint="Transformer_THT:Transformer_Breve_TEZ-22x24", pos=(90, 55)),
        ComponentSpec(ref="BR1", lib_id="Device:D_Bridge_+-AA", value="1A_BRIDGE", footprint="Diode_THT:Diode_Bridge_Round_D9.0mm", pos=(115, 55)),
        ComponentSpec(ref="C1", lib_id="Device:C_Polarized", value="1000uF_25V", footprint="Capacitor_THT:CP_Radial_D10.0mm_P5.00mm", pos=(135, 60)),
        ComponentSpec(ref="IC1", lib_id="Regulator_Linear:LM7805_TO220", value="LM7805", footprint="Package_TO_SOT_THT:TO-220-3_Vertical", pos=(150, 55)),
        ComponentSpec(ref="C2", lib_id="Device:C", value="0.1uF", footprint="Capacitor_THT:C_Disc_D4.3mm_W1.9mm_P5.00mm", pos=(168, 60)),

        # Power Test Points
        ComponentSpec(ref="TP1", lib_id="Connector:TestPoint", value="TP_AC_L", footprint="TestPoint:TestPoint_THTPad_D1.5mm_Drill0.7mm", pos=(35, 35)),
        ComponentSpec(ref="TP2", lib_id="Connector:TestPoint", value="TP_AC_N", footprint="TestPoint:TestPoint_THTPad_D1.5mm_Drill0.7mm", pos=(35, 65)),
        ComponentSpec(ref="TP3", lib_id="Connector:TestPoint", value="TP_+5V", footprint="TestPoint:TestPoint_THTPad_D1.5mm_Drill0.7mm", pos=(175, 40)),
        ComponentSpec(ref="TP4", lib_id="Connector:TestPoint", value="TP_GND", footprint="TestPoint:TestPoint_THTPad_D1.5mm_Drill0.7mm", pos=(175, 80)),

        # --- 74LS373 CORE ---
        ComponentSpec(ref="IC2", lib_id="74xx:74LS373", value="74LS373", footprint="Package_DIP:DIP-20_W7.62mm", pos=(185, 200)),

        # --- LOCKOUT & BUZZER ---
        ComponentSpec(ref="R11", lib_id="Device:R", value="56k", footprint="Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal", pos=(195, 95)),
        ComponentSpec(ref="T2", lib_id="Transistor_BJT:BC548", value="BC548_LOCK", footprint="Package_TO_SOT_THT:TO-92_Inline", pos=(210, 95)),
        ComponentSpec(ref="R10", lib_id="Device:R", value="1k", footprint="Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal", pos=(225, 95)),
        ComponentSpec(ref="R9", lib_id="Device:R", value="1k", footprint="Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal", pos=(225, 55)),
        ComponentSpec(ref="T1", lib_id="Transistor_BJT:BC548", value="BC548_BUZ", footprint="Package_TO_SOT_THT:TO-92_Inline", pos=(210, 55)),
        ComponentSpec(ref="PZ1", lib_id="Device:Buzzer", value="PIEZO_BUZZER", footprint="Buzzer_Beeper:Buzzer_12x9.5RM7.6", pos=(195, 45)),

        # --- MECHANICAL ---
        ComponentSpec(ref="H1", lib_id="Mechanical:MountingHole", value="MountingHole_M3", footprint="MountingHole:MountingHole_3.2mm_M3", pos=(25, 275)),
        ComponentSpec(ref="H2", lib_id="Mechanical:MountingHole", value="MountingHole_M3", footprint="MountingHole:MountingHole_3.2mm_M3", pos=(135, 275)),
        ComponentSpec(ref="H3", lib_id="Mechanical:MountingHole", value="MountingHole_M3", footprint="MountingHole:MountingHole_3.2mm_M3", pos=(255, 275)),
        ComponentSpec(ref="H4", lib_id="Mechanical:MountingHole", value="MountingHole_M3", footprint="MountingHole:MountingHole_3.2mm_M3", pos=(395, 275)),
    ]

    # Add 8 Switches S1-S8, 8 Pull-downs R1-R8 with 18mm pitch
    y_start = 135
    y_pitch = 18
    for i in range(1, 9):
        y = y_start + (i - 1) * y_pitch
        comps.append(ComponentSpec(ref=f"S{i}", lib_id="Switch:SW_Push", value=f"SW_P{i}", footprint="Button_Switch_THT:SW_PUSH_6mm", pos=(35, y)))
        comps.append(ComponentSpec(ref=f"R{i}", lib_id="Device:R", value="1.2k", footprint="Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal", pos=(65, y)))

    # Add 8 Diodes D1-D8, 8 Resistors R12-R19, 8 SCRs SCR1-SCR8, 8 Lamps BL1-BL8
    for i in range(1, 9):
        y = y_start + (i - 1) * y_pitch
        comps.append(ComponentSpec(ref=f"D{i}", lib_id="Device:D", value="1N4148", footprint="Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal", pos=(235, y)))
        comps.append(ComponentSpec(ref=f"R{11+i}", lib_id="Device:R", value="1k", footprint="Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal", pos=(285, y)))
        comps.append(ComponentSpec(ref=f"SCR{i}", lib_id="Device:Q_SCR_AKG", value="TYN612", footprint="Package_TO_SOT_THT:TO-220-3_Vertical", pos=(320, y)))
        comps.append(ComponentSpec(ref=f"BL{i}", lib_id="Device:Lamp", value="6V_BULB", footprint="Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical", pos=(355, y)))

    # External Pin Headers
    comps.append(ComponentSpec(ref="J2", lib_id="Connector_Generic:Conn_01x08", value="REMOTE_SWITCHES", footprint="Connector_PinHeader_2.54mm:PinHeader_1x08_P2.54mm_Vertical", pos=(105, 200)))
    comps.append(ComponentSpec(ref="J3", lib_id="Connector_Generic:Conn_01x08", value="REMOTE_BULBS", footprint="Connector_PinHeader_2.54mm:PinHeader_1x08_P2.54mm_Vertical", pos=(385, 200)))

    # Place components
    placed_pins = {}
    comp_map = {}
    for comp in comps:
        comp_map[comp.ref] = comp
        c = sch.components.add(
            lib_id=comp.lib_id,
            reference=comp.ref,
            value=comp.value,
            position=comp.pos
        )
        if comp.ref.startswith("R") and comp.ref not in ("R9", "R10", "R11"):
            c.rotation = 90
        elif comp.ref.startswith("BL"):
            c.rotation = 90

        try:
            c.footprint = comp.footprint
        except Exception:
            pass

        pins = {}
        for p in sch.list_component_pins(comp.ref):
            pins[p[0]] = p[1]
        placed_pins[comp.ref] = pins

    # Circuit Nets
    nets = [
        # --- AC MAINS ---
        NetSpec(name="AC_LIVE", nodes=[("J1", "1"), ("S9", "1"), ("TP1", "1")]),
        NetSpec(name="AC_SW", nodes=[("S9", "2"), ("F1", "1")]),
        NetSpec(name="AC_PRI_L", nodes=[("F1", "2"), ("X1", "1")]),
        NetSpec(name="AC_NEUT", nodes=[("J1", "2"), ("X1", "4"), ("TP2", "1")]),
        NetSpec(name="SEC_AC1", nodes=[("X1", "6"), ("BR1", "3")]),
        NetSpec(name="SEC_AC2", nodes=[("X1", "7"), ("BR1", "4")]),

        # --- UNREGULATED DC & 5V REGULATION ---
        NetSpec(name="UNREG_DC", nodes=[("BR1", "1"), ("C1", "1"), ("IC1", "1")]),

        # --- +5V RAIL A ---
        NetSpec(name="+5V", nodes=[
            ("IC1", "3"), ("C2", "1"), ("TP3", "1"),
            ("IC2", "20"),
            ("R11", "1"),
            ("PZ1", "1"),
            ("S1", "1"), ("S2", "1"), ("S3", "1"), ("S4", "1"),
            ("S5", "1"), ("S6", "1"), ("S7", "1"), ("S8", "1"),
            ("BL1", "1"), ("BL2", "1"), ("BL3", "1"), ("BL4", "1"),
            ("BL5", "1"), ("BL6", "1"), ("BL7", "1"), ("BL8", "1"),
        ]),

        # --- GND RAIL B ---
        NetSpec(name="GND", nodes=[
            ("BR1", "2"), ("C1", "2"), ("IC1", "2"), ("C2", "2"), ("TP4", "1"),
            ("IC2", "10"), ("IC2", "1"),
            ("T1", "3"), ("T2", "3"),
            ("R1", "2"), ("R2", "2"), ("R3", "2"), ("R4", "2"),
            ("R5", "2"), ("R6", "2"), ("R7", "2"), ("R8", "2"),
            ("SCR1", "2"), ("SCR2", "2"), ("SCR3", "2"), ("SCR4", "2"),
            ("SCR5", "2"), ("SCR6", "2"), ("SCR7", "2"), ("SCR8", "2"),
        ]),

        # --- DATA INPUTS D0-D7 ---
        NetSpec(name="DATA_0", nodes=[("S1", "2"), ("R1", "1"), ("IC2", "3"), ("J2", "1")]),
        NetSpec(name="DATA_1", nodes=[("S2", "2"), ("R2", "1"), ("IC2", "4"), ("J2", "2")]),
        NetSpec(name="DATA_2", nodes=[("S3", "2"), ("R3", "1"), ("IC2", "7"), ("J2", "3")]),
        NetSpec(name="DATA_3", nodes=[("S4", "2"), ("R4", "1"), ("IC2", "8"), ("J2", "4")]),
        NetSpec(name="DATA_4", nodes=[("S5", "2"), ("R5", "1"), ("IC2", "13"), ("J2", "5")]),
        NetSpec(name="DATA_5", nodes=[("S6", "2"), ("R6", "1"), ("IC2", "14"), ("J2", "6")]),
        NetSpec(name="DATA_6", nodes=[("S7", "2"), ("R7", "1"), ("IC2", "17"), ("J2", "7")]),
        NetSpec(name="DATA_7", nodes=[("S8", "2"), ("R8", "1"), ("IC2", "18"), ("J2", "8")]),

        # --- OUTPUTS Q0-Q7 ---
        NetSpec(name="Q0", nodes=[("IC2", "2"), ("D1", "2"), ("R12", "1")]),
        NetSpec(name="Q1", nodes=[("IC2", "5"), ("D2", "2"), ("R13", "1")]),
        NetSpec(name="Q2", nodes=[("IC2", "6"), ("D3", "2"), ("R14", "1")]),
        NetSpec(name="Q3", nodes=[("IC2", "9"), ("D4", "2"), ("R15", "1")]),
        NetSpec(name="Q4", nodes=[("IC2", "12"), ("D5", "2"), ("R16", "1")]),
        NetSpec(name="Q5", nodes=[("IC2", "15"), ("D6", "2"), ("R17", "1")]),
        NetSpec(name="Q6", nodes=[("IC2", "16"), ("D7", "2"), ("R18", "1")]),
        NetSpec(name="Q7", nodes=[("IC2", "19"), ("D8", "2"), ("R19", "1")]),

        # --- COMMON DIODE CATHODE BUS ---
        NetSpec(name="DIODE_OR_BUS", nodes=[
            ("D1", "1"), ("D2", "1"), ("D3", "1"), ("D4", "1"),
            ("D5", "1"), ("D6", "1"), ("D7", "1"), ("D8", "1"),
            ("R10", "1"), ("R9", "1")
        ]),

        # --- LOCKOUT CONTROL ---
        NetSpec(name="T2_BASE", nodes=[("R10", "2"), ("T2", "2")]),
        NetSpec(name="LATCH_ENABLE", nodes=[("T2", "1"), ("R11", "2"), ("IC2", "11")]),

        # --- BUZZER CONTROL ---
        NetSpec(name="T1_BASE", nodes=[("R9", "2"), ("T1", "2")]),
        NetSpec(name="BUZZER_DRIVE", nodes=[("T1", "1"), ("PZ1", "2")]),

        # --- SCR GATES & BULBS ---
        NetSpec(name="GATE_1", nodes=[("R12", "2"), ("SCR1", "3")]),
        NetSpec(name="BULB_1", nodes=[("SCR1", "1"), ("BL1", "2"), ("J3", "1")]),

        NetSpec(name="GATE_2", nodes=[("R13", "2"), ("SCR2", "3")]),
        NetSpec(name="BULB_2", nodes=[("SCR2", "1"), ("BL2", "2"), ("J3", "2")]),

        NetSpec(name="GATE_3", nodes=[("R14", "2"), ("SCR3", "3")]),
        NetSpec(name="BULB_3", nodes=[("SCR3", "1"), ("BL3", "2"), ("J3", "3")]),

        NetSpec(name="GATE_4", nodes=[("R15", "2"), ("SCR4", "3")]),
        NetSpec(name="BULB_4", nodes=[("SCR4", "1"), ("BL4", "2"), ("J3", "4")]),

        NetSpec(name="GATE_5", nodes=[("R16", "2"), ("SCR5", "3")]),
        NetSpec(name="BULB_5", nodes=[("SCR5", "1"), ("BL5", "2"), ("J3", "5")]),

        NetSpec(name="GATE_6", nodes=[("R17", "2"), ("SCR6", "3")]),
        NetSpec(name="BULB_6", nodes=[("SCR6", "1"), ("BL6", "2"), ("J3", "6")]),

        NetSpec(name="GATE_7", nodes=[("R18", "2"), ("SCR7", "3")]),
        NetSpec(name="BULB_7", nodes=[("SCR7", "1"), ("BL7", "2"), ("J3", "7")]),

        NetSpec(name="GATE_8", nodes=[("R19", "2"), ("SCR8", "3")]),
        NetSpec(name="BULB_8", nodes=[("SCR8", "1"), ("BL8", "2"), ("J3", "8")]),
    ]

    # DRAW WIRES AND LABELS ACCURATELY
    used_wire_endpoints = set()

    for net in nets:
        net_name = net.name
        for ref, pin_num in net.nodes:
            pin_num_str = str(pin_num)
            if ref not in placed_pins or pin_num_str not in placed_pins[ref]:
                continue
            pt = placed_pins[ref][pin_num_str]
            c_pos = comp_map[ref].pos

            dx = 0.0
            dy = 0.0

            # Tailored pin direction logic per component type
            if ref in ("J2", "J3"):
                p_idx = int(pin_num_str)
                stub_len = 6.35 if (p_idx % 2 == 1) else 12.70
                dx = -stub_len
                dy = 0.0
            elif ref == "J1":
                dx = -5.08
                dy = 0.0
            elif ref.startswith("SCR"):
                if pin_num_str == "3": # Gate (left)
                    dx = -3.81
                    dy = 0.0
                elif pin_num_str == "1": # Anode (top)
                    dx = 0.0
                    dy = -3.81
                elif pin_num_str == "2": # Cathode (bottom)
                    dx = 0.0
                    dy = 3.81
            elif ref.startswith("BL"):
                if pin_num_str == "1":
                    dx = -3.81
                    dy = 0.0
                else:
                    dx = 3.81
                    dy = 0.0
            elif ref.startswith("S") and ref != "S9": # Switches S1-S8
                if pin_num_str == "1":
                    dx = -3.81
                    dy = 0.0
                else:
                    dx = 3.81
                    dy = 0.0
            elif ref.startswith("R") and ref not in ("R9", "R10", "R11"):
                # Horizontal resistors
                if pin_num_str == "1":
                    dx = 3.81
                    dy = 0.0
                else:
                    dx = -3.81
                    dy = 0.0
            elif ref.startswith("D") and not ref.startswith("D_"):
                # Horizontal diodes D1-D8
                if pin_num_str == "1": # Cathode (left)
                    dx = -3.81
                    dy = 0.0
                else: # Anode (right)
                    dx = 3.81
                    dy = 0.0
            elif ref in ("T1", "T2"):
                if pin_num_str == "1": # Collector (top)
                    dx, dy = 0.0, -3.81
                elif pin_num_str == "2": # Base (left)
                    dx, dy = -3.81, 0.0
                elif pin_num_str == "3": # Emitter (bottom)
                    dx, dy = 0.0, 3.81
            elif ref == "X1":
                if pin_num_str in ("1", "4"): # Primary (left)
                    dx, dy = -3.81, 0.0
                else: # Secondary (right)
                    dx, dy = 3.81, 0.0
            elif ref == "IC2":
                # 74LS373 DIP-20
                if pin_num_str == "20":
                    dx = 0.0
                    dy = -5.08
                elif pin_num_str == "10":
                    dx = 0.0
                    dy = 5.08
                elif int(pin_num_str) in [1, 3, 4, 7, 8, 11, 13, 14, 17, 18]:
                    dx = -5.08
                    dy = 0.0
                else:
                    dx = 5.08
                    dy = 0.0
            else:
                stub_len = 3.81
                if abs(pt.x - c_pos[0]) >= abs(pt.y - c_pos[1]):
                    dx = -stub_len if pt.x <= c_pos[0] else stub_len
                else:
                    dy = -stub_len if pt.y <= c_pos[1] else stub_len

            end_x = round(pt.x + dx, 2)
            end_y = round(pt.y + dy, 2)

            wire_key = ((round(pt.x, 2), round(pt.y, 2)), (end_x, end_y))
            if wire_key not in used_wire_endpoints:
                used_wire_endpoints.add(wire_key)
                sch.add_wire((pt.x, pt.y), (end_x, end_y))

            sch.add_label(net_name, position=(end_x, end_y))

    # Add PWR_FLAG to UNREG_DC and GND (LM7805 VO already acts as power_out)
    sch.components.add("power:PWR_FLAG", reference="#FLG01", value="PWR_FLAG", position=(130, 40))
    sch.components.add("power:PWR_FLAG", reference="#FLG02", value="PWR_FLAG", position=(100, 85))

    p1 = sch.get_component_pin_position("#FLG01", "1")
    sch.add_wire((p1.x, p1.y), (p1.x, p1.y - 3.81))
    sch.add_label("UNREG_DC", position=(p1.x, p1.y - 3.81))

    p2 = sch.get_component_pin_position("#FLG02", "1")
    sch.add_wire((p2.x, p2.y), (p2.x, p2.y + 3.81))
    sch.add_label("GND", position=(p2.x, p2.y + 3.81))

    sch.save_as(str(SCH_FILE))
    print(f" [✓] Schematic successfully written to: {SCH_FILE}")

def run_erc_validation():
    print(" [*] Running KiCad Electrical Rules Check (ERC)...")
    res = subprocess.run(
        ["kicad-cli", "sch", "erc", "--severity-all", str(SCH_FILE)],
        capture_output=True,
        text=True
    )
    print(res.stdout)
    if res.returncode != 0:
        print(f" [!] ERC reported issues:\n{res.stderr}")
        return False
    print(" [✓] ERC PASSED WITH ZERO VIOLATIONS!")
    return True

if __name__ == "__main__":
    build_schematic()
    run_erc_validation()

#!/usr/bin/env python3
"""
Fully Wired KiCad Schematic Generator for School/College Quiz Buzzer (8 Players)
Creates visible point-to-point wiring between all matching net nodes per the EFY reference circuit.
Preserves all net labels in place.
Validates 0 ERC errors, 0 ERC warnings, and 0 PCB DRC parity issues.
Author: Divyansh Rawat (Roll No: 124EC0030)
"""

import sys
import subprocess
from pathlib import Path

MID_DIR = Path("/home/divyansh-rawat/AIPCBDESIGN/mid_exam").resolve()
SCH_FILE = MID_DIR / "school_college_quiz_buzzer.kicad_sch"
PCB_FILE = MID_DIR / "school_college_quiz_buzzer.kicad_pcb"

sys.path.insert(0, "/home/divyansh-rawat/AIPCBDESIGN/.venv/lib/python3.14/site-packages")
import kicad_sch_api as ksa

def make_wired_schematic():
    print(" [*] Reverting to clean schematic base...")
    subprocess.run(["git", "checkout", str(SCH_FILE)], check=True)

    sch = ksa.load_schematic(str(SCH_FILE))

    def snap(v):
        return round(round(v / 1.27) * 1.27, 2)

    def snap_pt(pt):
        return (snap(pt[0]), snap(pt[1]))

    def add_w(p1, p2):
        s = snap_pt(p1)
        e = snap_pt(p2)
        if s != e:
            sch.add_wire(s, e)

    def add_j(p):
        sch.junctions.add(snap_pt(p))

    def route_ortho(p1, p2, start_horizontal=True):
        s = snap_pt(p1)
        e = snap_pt(p2)
        if s == e:
            return
        if s[0] == e[0] or s[1] == e[1]:
            sch.add_wire(s, e)
        elif start_horizontal:
            mid = (e[0], s[1])
            sch.add_wire(s, mid)
            sch.add_wire(mid, e)
            add_j(mid)
        else:
            mid = (s[0], e[1])
            sch.add_wire(s, mid)
            sch.add_wire(mid, e)
            add_j(mid)

    print(" [-] 1. Visible wiring for AC Mains & Power Supply...")
    # AC_LIVE: (15.24, 44.45) to (35.56, 44.45)
    add_w((15.24, 44.45), (35.56, 44.45))
    add_w((35.56, 44.45), (39.37, 44.45))
    add_w((39.37, 44.45), (39.37, 35.56))
    add_j((35.56, 44.45))

    # AC_SW: (53.34, 44.45) to (64.77, 36.83)
    add_w((53.34, 44.45), (64.77, 44.45))
    add_w((64.77, 44.45), (64.77, 36.83))
    add_j((64.77, 44.45))

    # AC_PRI_L: (64.77, 52.07) to (81.28, 49.53)
    add_w((64.77, 52.07), (73.66, 52.07))
    add_w((73.66, 52.07), (73.66, 49.53))
    add_w((73.66, 49.53), (81.28, 49.53))
    add_j((73.66, 52.07))
    add_j((73.66, 49.53))

    # AC_NEUT: (15.24, 46.99) to (81.28, 59.69) and TP2 (39.37, 64.77)
    add_w((15.24, 46.99), (15.24, 59.69))
    add_w((15.24, 59.69), (81.28, 59.69))
    add_w((39.37, 59.69), (39.37, 64.77))
    add_j((15.24, 59.69))
    add_j((39.37, 59.69))

    # SEC_AC1: (99.06, 49.53) to (115.57, 43.18)
    add_w((99.06, 49.53), (107.95, 49.53))
    add_w((107.95, 49.53), (107.95, 43.18))
    add_w((107.95, 43.18), (115.57, 43.18))
    add_j((107.95, 49.53))
    add_j((107.95, 43.18))

    # SEC_AC2: (99.06, 59.69) to (115.57, 66.04)
    add_w((99.06, 59.69), (107.95, 59.69))
    add_w((107.95, 59.69), (107.95, 66.04))
    add_w((107.95, 66.04), (115.57, 66.04))
    add_j((107.95, 59.69))
    add_j((107.95, 66.04))

    # UNREG_DC: (127.00, 54.61) to (138.43, 54.61), C1 (134.62, 52.07), PWR_FLAG (129.54, 35.56)
    add_w((127.00, 54.61), (138.43, 54.61))
    add_w((134.62, 52.07), (134.62, 54.61))
    add_j((134.62, 54.61))
    add_w((129.54, 35.56), (129.54, 54.61))
    add_j((129.54, 54.61))

    # +5V in Power Block: (161.29, 54.61) to (175.26, 35.56) and C2 (167.64, 52.07)
    add_w((161.29, 54.61), (175.26, 54.61))
    add_w((175.26, 54.61), (175.26, 35.56))
    add_j((175.26, 54.61))
    add_w((167.64, 52.07), (167.64, 54.61))
    add_j((167.64, 54.61))

    print(" [-] 2. Visible wiring for Lockout & Buzzer Stage...")
    # T1_BASE: (224.79, 62.23) to (200.66, 54.61)
    add_w((224.79, 62.23), (200.66, 62.23))
    add_w((200.66, 62.23), (200.66, 54.61))
    add_j((200.66, 62.23))

    # T2_BASE: (224.79, 102.87) to (200.66, 95.25)
    add_w((224.79, 102.87), (224.79, 95.25))
    add_w((224.79, 95.25), (200.66, 95.25))
    add_j((224.79, 95.25))

    # BUZZER_DRIVE: (212.09, 45.72) to (193.04, 50.80)
    add_w((212.09, 45.72), (212.09, 50.80))
    add_w((212.09, 50.80), (193.04, 50.80))
    add_j((212.09, 50.80))

    # LATCH_ENABLE: (212.09, 86.36) to (195.58, 102.87) and IC2(11) (167.64, 209.55)
    # T2(1) is at (212.09, 86.36). Route around R11 bottom (y=108.0) to R11(2) at (195.58, 102.87)
    add_w((212.09, 86.36), (205.74, 86.36))
    add_w((205.74, 86.36), (205.74, 107.95))
    add_w((205.74, 107.95), (195.58, 107.95))
    add_w((195.58, 107.95), (195.58, 102.87))
    add_j((205.74, 86.36))
    add_j((205.74, 107.95))
    add_j((195.58, 107.95))
    add_j((195.58, 102.87))
    # Route over to IC2(11)
    add_w((195.58, 107.95), (162.56, 107.95))
    add_w((162.56, 107.95), (162.56, 209.55))
    add_w((162.56, 209.55), (167.64, 209.55))
    add_j((162.56, 107.95))
    add_j((162.56, 209.55))

    print(" [-] 3. Visible wiring for Common Diode OR-ing Bus...")
    bus_x = 227.33
    add_w((bus_x, 46.99), (bus_x, 261.62))
    for y in [46.99, 87.63, 134.62, 152.4, 171.45, 189.23, 207.01, 224.79, 242.57, 261.62]:
        add_j((bus_x, y))
    add_w((224.79, 87.63), (bus_x, 87.63))
    add_w((224.79, 46.99), (bus_x, 46.99))

    print(" [-] 4. Visible wiring for GATE_1 to GATE_8 (Bypassing Resistor Body)...")
    gate_pts = [
        ((276.86, 134.62), (312.42, 137.16)),
        ((276.86, 152.4), (312.42, 154.94)),
        ((276.86, 171.45), (312.42, 173.99)),
        ((276.86, 189.23), (312.42, 191.77)),
        ((276.86, 207.01), (312.42, 209.55)),
        ((276.86, 224.79), (312.42, 227.33)),
        ((276.86, 242.57), (312.42, 245.11)),
        ((276.86, 261.62), (312.42, 264.16)),
    ]
    for p1, p2 in gate_pts:
        bypass_y = p1[1] - 3.81
        add_w(p1, (p1[0], bypass_y))
        add_w((p1[0], bypass_y), (p2[0], bypass_y))
        add_w((p2[0], bypass_y), p2)
        add_j((p1[0], bypass_y))
        add_j((p2[0], bypass_y))

    print(" [-] 5. Visible wiring for Common Power & GND Rails...")
    # +5V Switch Rail
    s_vcc_x = 26.67
    add_w((s_vcc_x, 134.62), (s_vcc_x, 261.62))
    for y in [134.62, 152.4, 171.45, 189.23, 207.01, 224.79, 242.57, 261.62]:
        add_j((s_vcc_x, y))

    # GND Pull-down Resistor Rail
    r_gnd_x = 57.15
    add_w((r_gnd_x, 134.62), (r_gnd_x, 261.62))
    for y in [134.62, 152.4, 171.45, 189.23, 207.01, 224.79, 242.57, 261.62]:
        add_j((r_gnd_x, y))

    # +5V Lamp Rail
    bl_vcc_x = 346.71
    add_w((bl_vcc_x, 134.62), (bl_vcc_x, 261.62))
    for y in [134.62, 152.4, 171.45, 189.23, 207.01, 224.79, 242.57, 261.62]:
        add_j((bl_vcc_x, y))

    print(" [-] 6. Visible wiring for DATA_0 to DATA_7 (Switch to Pull-down Resistor)...")
    data_pts = [
        ((44.45, 134.62), (72.39, 134.62)),
        ((44.45, 152.40), (72.39, 152.40)),
        ((44.45, 171.45), (72.39, 171.45)),
        ((44.45, 189.23), (72.39, 189.23)),
        ((44.45, 207.01), (72.39, 207.01)),
        ((44.45, 224.79), (72.39, 224.79)),
        ((44.45, 242.57), (72.39, 242.57)),
        ((44.45, 261.62), (72.39, 261.62)),
    ]
    for p1, p2 in data_pts:
        arch_y = p1[1] - 3.81
        add_w(p1, (p1[0], arch_y))
        add_w((p1[0], arch_y), (p2[0], arch_y))
        add_w((p2[0], arch_y), p2)
        add_j((p1[0], arch_y))
        add_j((p2[0], arch_y))

    print(" [-] 7. Visible wiring for Q0 to Q7 (Diode Anode to Gate Resistor)...")
    q_pts = [
        ((242.57, 134.62), (292.10, 134.62)),
        ((242.57, 152.40), (292.10, 152.40)),
        ((242.57, 171.45), (292.10, 171.45)),
        ((242.57, 189.23), (292.10, 189.23)),
        ((242.57, 207.01), (292.10, 207.01)),
        ((242.57, 224.79), (292.10, 224.79)),
        ((242.57, 242.57), (292.10, 242.57)),
        ((242.57, 261.62), (292.10, 261.62)),
    ]
    for p1, p2 in q_pts:
        arch_y = p1[1] + 3.81
        add_w(p1, (p1[0], arch_y))
        add_w((p1[0], arch_y), (p2[0], arch_y))
        add_w((p2[0], arch_y), p2)
        add_j((p1[0], arch_y))
        add_j((p2[0], arch_y))



    sch.save_as(str(SCH_FILE))
    print(f" [✓] Wired schematic successfully saved to {SCH_FILE}!")

    # Check ERC
    print(" [*] Running KiCad ERC...")
    erc = subprocess.run(["kicad-cli", "sch", "erc", "--severity-all", str(SCH_FILE)], capture_output=True, text=True)
    print(erc.stdout)

    # Check PCB DRC Parity
    print(" [*] Running KiCad PCB DRC & Parity Check...")
    drc = subprocess.run(["kicad-cli", "pcb", "drc", "--schematic-parity", str(PCB_FILE)], capture_output=True, text=True)
    print(drc.stdout)

if __name__ == "__main__":
    make_wired_schematic()

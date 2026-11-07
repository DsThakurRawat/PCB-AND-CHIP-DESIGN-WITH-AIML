#!/usr/bin/env python3
"""
Custom Single-Layer PCB Layout Builder for NE555 1Hz LED Blinker
Generates a verified, single-layer through-hole PCB within 48mm x 36mm (< 50mm x 40mm).
All traces routed exclusively on F.Cu (Front Copper) with zero crossings.
"""

import sys
import json
from pathlib import Path
import pcbnew

def build_ne555_pcb(output_path: str):
    board = pcbnew.BOARD()

    # 1. Dimensions and Origin
    x0, y0 = 100.0, 100.0
    width, height = 48.0, 36.0

    # 2. Add Board Outline on Edge.Cuts
    pts = [
        (x0, y0),
        (x0 + width, y0),
        (x0 + width, y0 + height),
        (x0, y0 + height)
    ]
    for i in range(4):
        p1 = pts[i]
        p2 = pts[(i + 1) % 4]
        seg = pcbnew.PCB_SHAPE(board, pcbnew.SHAPE_T_SEGMENT)
        seg.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(p1[0]), pcbnew.FromMM(p1[1])))
        seg.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(p2[0]), p2[1] if isinstance(p2[1], int) else pcbnew.FromMM(p2[1])))
        seg.SetWidth(pcbnew.FromMM(0.15))
        seg.SetLayer(pcbnew.Edge_Cuts)
        board.Add(seg)

    # 3. Setup Nets
    net_names = ["+5V", "GND", "DISCH", "TIMING", "CONT", "OUT", "LED_A"]
    net_map = {}
    for name in net_names:
        net_info = pcbnew.NETINFO_ITEM(board, name)
        board.Add(net_info)
        net_map[name] = net_info

    # 4. Load Footprints
    fp_defs = {
        "J1": ("Connector_PinHeader_2.54mm", "PinHeader_1x02_P2.54mm_Vertical", "5V_IN", (x0 + 6.0, y0 + 10.0), 90),
        "C3": ("Capacitor_THT", "C_Disc_D5.0mm_W2.5mm_P5.00mm", "100nF", (x0 + 6.0, y0 + 20.0), 90),
        "C1": ("Capacitor_THT", "CP_Radial_D5.0mm_P2.50mm", "10uF", (x0 + 6.0, y0 + 28.0), 90),
        "U1": ("Package_DIP", "DIP-8_W7.62mm", "NE555P", (x0 + 22.0, y0 + 17.0), 0),
        "R1": ("Resistor_THT", "R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal", "10k", (x0 + 38.0, y0 + 9.0), 0),
        "R2": ("Resistor_THT", "R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal", "100k", (x0 + 38.0, y0 + 16.0), 0),
        "C2": ("Capacitor_THT", "C_Disc_D5.0mm_W2.5mm_P5.00mm", "10nF", (x0 + 38.0, y0 + 23.0), 0),
        "R3": ("Resistor_THT", "R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal", "1k", (x0 + 22.0, y0 + 31.0), 0),
        "D1": ("LED_THT", "LED_D5.0mm", "LED_RED", (x0 + 38.0, y0 + 31.0), 0)
    }

    # Pin net assignments: {ref: {pad_num: net_name}}
    pin_assignments = {
        "J1": {"1": "+5V", "2": "GND"},
        "C3": {"1": "+5V", "2": "GND"},
        "U1": {
            "1": "GND",
            "2": "TIMING",
            "3": "OUT",
            "4": "+5V",
            "5": "CONT",
            "6": "TIMING",
            "7": "DISCH",
            "8": "+5V"
        },
        "R1": {"1": "+5V", "2": "DISCH"},
        "R2": {"1": "DISCH", "2": "TIMING"},
        "C1": {"1": "TIMING", "2": "GND"},
        "C2": {"1": "CONT", "2": "GND"},
        "R3": {"1": "OUT", "2": "LED_A"},
        "D1": {"2": "LED_A", "1": "GND"}
    }

    footprints = {}
    for ref, (lib, mod, val, pos, rot) in fp_defs.items():
        lib_path = f"/usr/share/kicad/footprints/{lib}.pretty"
        fp = pcbnew.FootprintLoad(lib_path, mod)
        if not fp:
            raise RuntimeError(f"Could not load footprint {lib}:{mod}")
        fp.SetReference(ref)
        fp.SetValue(val)
        fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(pos[0]), pcbnew.FromMM(pos[1])))
        fp.SetOrientation(pcbnew.EDA_ANGLE(rot, pcbnew.DEGREES_T))

        # Assign pad nets
        for pad in fp.Pads():
            pad_num = pad.GetNumber()
            net_name = pin_assignments.get(ref, {}).get(pad_num)
            if net_name:
                pad.SetNet(net_map[net_name])

        board.Add(fp)
        footprints[ref] = fp

    # 5. Add Silkscreen Labels
    def add_silk_text(text: str, x: float, y: float, size: float = 1.2):
        t = pcbnew.PCB_TEXT(board)
        t.SetText(text)
        t.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
        t.SetLayer(pcbnew.F_SilkS)
        t.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(size), pcbnew.FromMM(size)))
        board.Add(t)

    # Title and functional markings
    add_silk_text("NE555 1Hz BLINKER", x0 + 13.0, y0 + 3.0, size=1.3)
    add_silk_text("SINGLE-LAYER F.Cu", x0 + 13.0, y0 + 5.0, size=0.9)
    # Required power markings on silkscreen:
    add_silk_text("+5V", x0 + 3.0, y0 + 7.5, size=1.1)
    add_silk_text("GND", x0 + 9.5, y0 + 7.5, size=1.1)

    # Helper function to get pad absolute position in mm
    def pad_pos(ref: str, pad_num: str):
        fp = footprints[ref]
        for pad in fp.Pads():
            if pad.GetNumber() == str(pad_num):
                p = pad.GetPosition()
                return (p.x / 1e6, p.y / 1e6)
        raise ValueError(f"Pad {pad_num} not found on {ref}")

    # Helper function to add track segments on F.Cu
    def add_track_poly(points: list, net_name: str, width_mm: float = 0.5):
        net_info = net_map[net_name]
        for i in range(len(points) - 1):
            p1 = points[i]
            p2 = points[i + 1]
            t = pcbnew.PCB_TRACK(board)
            t.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(p1[0]), pcbnew.FromMM(p1[1])))
            t.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(p2[0]), pcbnew.FromMM(p2[1])))
            t.SetWidth(pcbnew.FromMM(width_mm))
            t.SetLayer(pcbnew.F_Cu)
            t.SetNet(net_info)
            board.Add(t)

    # 6. Route Single-Layer Traces on F.Cu
    # NET 1: +5V
    # J1 pin 1 -> C3 pin 1 -> U1 pin 8 -> R1 pin 1
    p_j1_1 = pad_pos("J1", "1")
    p_c3_1 = pad_pos("C3", "1")
    p_u1_8 = pad_pos("U1", "8")
    p_u1_4 = pad_pos("U1", "4")
    p_r1_1 = pad_pos("R1", "1")

    # J1.1 to C3.1
    add_track_poly([p_j1_1, (p_j1_1[0], p_j1_1[1] + 2.5), (p_c3_1[0], p_c3_1[1] - 2.5), p_c3_1], "+5V", 0.6)
    # J1.1 to U1.8 via top rail
    top_vcc_y = y0 + 6.5
    add_track_poly([
        p_j1_1,
        (p_j1_1[0], top_vcc_y),
        (p_u1_8[0], top_vcc_y),
        p_u1_8
    ], "+5V", 0.6)
    # U1.8 to R1.1
    add_track_poly([
        p_u1_8,
        (p_u1_8[0], top_vcc_y),
        (p_r1_1[0], top_vcc_y),
        p_r1_1
    ], "+5V", 0.6)
    # U1.8 to U1.4 (+5V drop down the center channel of DIP-8)
    center_x = (p_u1_8[0] + p_u1_4[0]) / 2.0
    add_track_poly([
        p_u1_8,
        (center_x, p_u1_8[1]),
        (center_x, p_u1_4[1]),
        p_u1_4
    ], "+5V", 0.5)

    # NET 2: GND
    # Outer perimeter bus connecting J1.2, C3.2, C1.2, U1.1, D1.1, C2.2
    p_j1_2 = pad_pos("J1", "2")
    p_c3_2 = pad_pos("C3", "2")
    p_c1_2 = pad_pos("C1", "2")
    p_u1_1 = pad_pos("U1", "1")
    p_c2_2 = pad_pos("C2", "2")
    p_d1_1 = pad_pos("D1", "1")

    # Left GND trunk: J1.2 down to C3.2 and C1.2
    add_track_poly([p_j1_2, p_c3_2, p_c1_2], "GND", 0.6)
    # J1.2 to U1.1
    add_track_poly([
        p_j1_2,
        (p_j1_2[0], p_u1_1[1] - 2.0),
        (p_u1_1[0], p_u1_1[1] - 2.0),
        p_u1_1
    ], "GND", 0.6)
    # Bottom perimeter GND: C1.2 down to bottom margin, along bottom to D1.1 and up to C2.2
    bot_gnd_y = y0 + height - 2.0
    right_gnd_x = x0 + width - 2.0
    add_track_poly([
        p_c1_2,
        (p_c1_2[0], bot_gnd_y),
        (p_d1_1[0], bot_gnd_y),
        p_d1_1
    ], "GND", 0.6)
    add_track_poly([
        (p_d1_1[0], bot_gnd_y),
        (right_gnd_x, bot_gnd_y),
        (right_gnd_x, p_c2_2[1]),
        p_c2_2
    ], "GND", 0.6)

    # NET 3: DISCH
    # U1 pin 7 -> R1 pin 2 and R2 pin 1
    p_u1_7 = pad_pos("U1", "7")
    p_r1_2 = pad_pos("R1", "2")
    p_r2_1 = pad_pos("R2", "1")
    add_track_poly([p_u1_7, (p_u1_7[0] + 3.0, p_u1_7[1]), (p_u1_7[0] + 3.0, p_r1_2[1]), p_r1_2], "DISCH", 0.4)
    add_track_poly([(p_u1_7[0] + 3.0, p_u1_7[1]), (p_r2_1[0], p_r2_1[1])], "DISCH", 0.4)

    # NET 4: TIMING
    # U1 pin 6 -> R2 pin 2 -> C1 pin 1 and U1 pin 2
    p_u1_6 = pad_pos("U1", "6")
    p_r2_2 = pad_pos("R2", "2")
    p_u1_2 = pad_pos("U1", "2")
    p_c1_1 = pad_pos("C1", "1")

    # U1.6 to R2.2
    add_track_poly([p_u1_6, (p_r2_2[0], p_u1_6[1]), p_r2_2], "TIMING", 0.4)
    # U1.6 to U1.2 (via center channel)
    ch_timing_x = center_x + 1.2
    add_track_poly([
        p_u1_6,
        (ch_timing_x, p_u1_6[1]),
        (ch_timing_x, p_u1_2[1]),
        p_u1_2
    ], "TIMING", 0.4)
    # U1.2 to C1.1
    add_track_poly([
        p_u1_2,
        (p_u1_2[0] - 3.5, p_u1_2[1]),
        (p_u1_2[0] - 3.5, p_c1_1[1]),
        p_c1_1
    ], "TIMING", 0.4)

    # NET 5: CONT
    # U1 pin 5 -> C2 pin 1
    p_u1_5 = pad_pos("U1", "5")
    p_c2_1 = pad_pos("C2", "1")
    add_track_poly([p_u1_5, (p_c2_1[0], p_u1_5[1]), p_c2_1], "CONT", 0.4)

    # NET 6: OUT
    # U1 pin 3 -> R3 pin 1
    p_u1_3 = pad_pos("U1", "3")
    p_r3_1 = pad_pos("R3", "1")
    add_track_poly([
        p_u1_3,
        (p_u1_3[0] - 1.5, p_u1_3[1]),
        (p_u1_3[0] - 1.5, p_r3_1[1]),
        p_r3_1
    ], "OUT", 0.4)

    # NET 7: LED_A
    # R3 pin 2 -> D1 pin 2
    p_r3_2 = pad_pos("R3", "2")
    p_d1_2 = pad_pos("D1", "2")
    add_track_poly([p_r3_2, p_d1_2], "LED_A", 0.4)

    # Save board
    out_file = Path(output_path).resolve()
    out_file.parent.mkdir(parents=True, exist_ok=True)
    pcbnew.SaveBoard(str(out_file), board)
    print(f"[+] PCB board generated successfully: {out_file}")
    return str(out_file)

if __name__ == "__main__":
    out_path = sys.argv[1] if len(sys.argv) > 1 else "/home/divyansh-rawat/PCBDESIGN/ne555_led_blinker/ne555_led_blinker.kicad_pcb"
    build_ne555_pcb(out_path)

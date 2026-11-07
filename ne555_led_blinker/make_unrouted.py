#!/usr/bin/env python3
"""
Generate unrouted board for FreeRouting test.
"""
import pcbnew

def generate_unrouted(out_path: str):
    board = pcbnew.BOARD()
    x0, y0 = 100.0, 100.0
    width, height = 48.0, 36.0

    # Edge.Cuts
    pts = [(x0, y0), (x0 + width, y0), (x0 + width, y0 + height), (x0, y0 + height)]
    for i in range(4):
        p1, p2 = pts[i], pts[(i + 1) % 4]
        seg = pcbnew.PCB_SHAPE(board, pcbnew.SHAPE_T_SEGMENT)
        seg.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(p1[0]), pcbnew.FromMM(p1[1])))
        seg.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(p2[0]), pcbnew.FromMM(p2[1])))
        seg.SetWidth(pcbnew.FromMM(0.15))
        seg.SetLayer(pcbnew.Edge_Cuts)
        board.Add(seg)

    # Nets
    net_names = ["+5V", "GND", "DISCH", "TIMING", "CONT", "OUT", "LED_A"]
    net_map = {}
    for name in net_names:
        net_info = pcbnew.NETINFO_ITEM(board, name)
        board.Add(net_info)
        net_map[name] = net_info

    # Footprints
    fp_defs = {
        "J1": ("Connector_PinHeader_2.54mm", "PinHeader_1x02_P2.54mm_Vertical", "5V_IN", (x0 + 6.0, y0 + 12.0), 0),
        "C3": ("Capacitor_THT", "C_Disc_D5.0mm_W2.5mm_P5.00mm", "100nF", (x0 + 6.0, y0 + 22.0), 0),
        "C1": ("Capacitor_THT", "CP_Radial_D5.0mm_P2.50mm", "10uF", (x0 + 6.0, y0 + 30.0), 0),
        "U1": ("Package_DIP", "DIP-8_W7.62mm", "NE555P", (x0 + 22.0, y0 + 16.0), 0),
        "R1": ("Resistor_THT", "R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal", "10k", (x0 + 36.0, y0 + 9.0), 0),
        "R2": ("Resistor_THT", "R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal", "100k", (x0 + 36.0, y0 + 16.0), 0),
        "C2": ("Capacitor_THT", "C_Disc_D5.0mm_W2.5mm_P5.00mm", "10nF", (x0 + 36.0, y0 + 23.0), 0),
        "R3": ("Resistor_THT", "R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal", "1k", (x0 + 22.0, y0 + 30.0), 0),
        "D1": ("LED_THT", "LED_D5.0mm", "LED_RED", (x0 + 36.0, y0 + 30.0), 0)
    }

    pin_assignments = {
        "J1": {"1": "+5V", "2": "GND"},
        "C3": {"1": "+5V", "2": "GND"},
        "U1": {"1": "GND", "2": "TIMING", "3": "OUT", "4": "+5V", "5": "CONT", "6": "TIMING", "7": "DISCH", "8": "+5V"},
        "R1": {"1": "+5V", "2": "DISCH"},
        "R2": {"1": "DISCH", "2": "TIMING"},
        "C1": {"1": "TIMING", "2": "GND"},
        "C2": {"1": "CONT", "2": "GND"},
        "R3": {"1": "OUT", "2": "LED_A"},
        "D1": {"2": "LED_A", "1": "GND"}
    }

    for ref, (lib, mod, val, pos, rot) in fp_defs.items():
        lib_path = f"/usr/share/kicad/footprints/{lib}.pretty"
        fp = pcbnew.FootprintLoad(lib_path, mod)
        fp.SetReference(ref)
        fp.SetValue(val)
        fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(pos[0]), pcbnew.FromMM(pos[1])))
        fp.SetOrientation(pcbnew.EDA_ANGLE(rot, pcbnew.DEGREES_T))
        for pad in fp.Pads():
            pad_num = pad.GetNumber()
            net_name = pin_assignments.get(ref, {}).get(pad_num)
            if net_name:
                pad.SetNet(net_map[net_name])
        board.Add(fp)

    pcbnew.SaveBoard(out_path, board)
    print(f"Saved unrouted board to {out_path}")

if __name__ == "__main__":
    generate_unrouted("/home/divyansh-rawat/PCBDESIGN/ne555_led_blinker/unrouted.kicad_pcb")

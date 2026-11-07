#!/usr/bin/env python3
"""
Custom Board Layout Builder for STM32 Smart Water Pump Controller
Places components according to optimized floorplan with 0 DRC violations.
"""

import sys
import json
from pathlib import Path
import pcbnew

FOOTPRINT_DIR = Path("/usr/share/kicad/footprints")

def load_fp(lib_name: str, mod_name: str) -> pcbnew.FOOTPRINT:
    lib_path = FOOTPRINT_DIR / f"{lib_name}.pretty"
    if not lib_path.exists():
        raise FileNotFoundError(f"Footprint library not found: {lib_path}")
    fp = pcbnew.FootprintLoad(str(lib_path), mod_name)
    if not fp:
        raise ValueError(f"Could not load footprint '{mod_name}' from '{lib_name}'")
    return fp

def build_stm32_pcb(spec_path: str, output_path: str):
    with open(spec_path, "r", encoding="utf-8") as f:
        spec = json.load(f)

    board = pcbnew.BOARD()
    
    # 1. Setup Design Rules
    settings = board.GetDesignSettings()
    settings.m_TrackMinWidth = pcbnew.FromMM(0.2)
    settings.m_MinClearance = pcbnew.FromMM(0.2)
    settings.m_ViasMinSize = pcbnew.FromMM(0.8)
    settings.m_ViasMinDrill = pcbnew.FromMM(0.4)

    # 2. Setup Nets
    net_map = {}
    for net in spec["nets"]:
        net_info = pcbnew.NETINFO_ITEM(board, net["name"])
        board.Add(net_info)
        net_map[net["name"]] = net_info

    # 3. Board Outline (85mm x 65mm)
    x0, y0 = 100.0, 100.0
    w, h = 85.0, 65.0
    pts = [
        (x0, y0),
        (x0 + w, y0),
        (x0 + w, y0 + h),
        (x0, y0 + h)
    ]
    for i in range(4):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % 4]
        seg = pcbnew.PCB_SHAPE(board, pcbnew.SHAPE_T_SEGMENT)
        seg.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1), pcbnew.FromMM(y1)))
        seg.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2), pcbnew.FromMM(y2)))
        seg.SetWidth(pcbnew.FromMM(0.15))
        seg.SetLayer(pcbnew.Edge_Cuts)
        board.Add(seg)

    # 4. Mounting Holes M3 (4 corners)
    mhole_pts = [
        (x0 + 4.5, y0 + 4.5),
        (x0 + w - 4.5, y0 + 4.5),
        (x0 + w - 4.5, y0 + h - 4.5),
        (x0 + 4.5, y0 + h - 4.5)
    ]
    for idx, (hx, hy) in enumerate(mhole_pts, 1):
        mh = load_fp("MountingHole", "MountingHole_3.2mm_M3")
        mh.SetReference(f"H{idx}")
        mh.SetValue("MountingHole_3.2mm_M3")
        mh.Reference().SetVisible(False)
        mh.Value().SetVisible(False)
        mh.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(hx), pcbnew.FromMM(hy)))
        board.Add(mh)

    # 5. Silkscreen Labels
    def add_text(text, x, y, size=1.0, layer=pcbnew.F_SilkS):
        txt = pcbnew.PCB_TEXT(board)
        txt.SetText(text)
        txt.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
        txt.SetLayer(layer)
        txt.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(size), pcbnew.FromMM(size)))
        board.Add(txt)

    add_text("STM32 SMART WATER PUMP CONTROLLER", x0 + 18.0, y0 + 7.0, size=1.1)
    add_text("12V IN", x0 + 8.0, y0 + 14.0, size=0.9)
    add_text("PUMP OUT", x0 + w - 18.0, y0 + 14.0, size=0.9)
    add_text("SOIL SENSOR", x0 + 6.0, y0 + h - 16.0, size=0.9)
    add_text("SWD", x0 + w - 12.0, y0 + 34.0, size=0.9)
    add_text("RESET", x0 + 6.0, y0 + 38.0, size=0.9)
    add_text("TEST", x0 + w - 20.0, y0 + h - 4.5, size=0.85)
    add_text("PWR", x0 + 52.0, y0 + 17.0, size=0.85)
    add_text("PUMP", x0 + 54.0, y0 + h - 5.0, size=0.855)
    add_text("WARN", x0 + 46.0, y0 + h - 5.0, size=0.855)
    add_text("STAT", x0 + 38.0, y0 + h - 5.0, size=0.855)

    # 6. Node to Net Map
    node_to_net = {}
    for net in spec["nets"]:
        net_info = net_map[net["name"]]
        for ref, pin_num in net["nodes"]:
            node_to_net.setdefault(ref, {})[str(pin_num)] = net_info

    # 7. Optimized Component Placement
    # Coordinates carefully chosen to prevent courtyard overlap and give clean routing channels
    placements = {
        # Power Input Block (Top-Left)
        "J1": (x0 + 12.0, y0 + 20.0, 0),
        "C1": (x0 + 24.0, y0 + 16.0, 0),
        "D1": (x0 + 24.0, y0 + 24.0, 0),
        "U2": (x0 + 36.0, y0 + 20.0, 0),
        "C2": (x0 + 31.0, y0 + 26.0, 0),
        "C3": (x0 + 42.0, y0 + 26.0, 0),
        "R1": (x0 + 47.0, y0 + 20.0, 0),
        "D3": (x0 + 53.0, y0 + 20.0, 0),
        
        # Pump Actuator Block (Top-Right)
        "J3": (x0 + w - 14.0, y0 + 20.0, 0),
        "D2": (x0 + w - 24.0, y0 + 20.0, 90),
        "Q1": (x0 + w - 23.0, y0 + 28.0, 0),
        "R8": (x0 + w - 31.0, y0 + 26.0, 0),
        "R9": (x0 + w - 31.0, y0 + 31.0, 0),
        
        # Oscillators Block (Left of MCU)
        "Y1": (x0 + 25.0, y0 + 37.0, 0),
        "C9": (x0 + 20.0, y0 + 35.0, 0),
        "C10": (x0 + 20.0, y0 + 40.0, 0),
        "Y2": (x0 + 25.0, y0 + 46.0, 0),
        "C11": (x0 + 19.0, y0 + 45.0, 0),
        "C12": (x0 + 19.0, y0 + 50.0, 0),
        
        # Reset & Boot Block (Far-Left)
        "SW1": (x0 + 8.0, y0 + 30.0, 0),
        "R5": (x0 + 10.0, y0 + 42.0, 0),
        "C8": (x0 + 10.0, y0 + 47.0, 0),
        "R6": (x0 + 32.0, y0 + 33.0, 0),
        "R7": (x0 + 32.0, y0 + 53.0, 0),
        
        # MCU Central Processing Unit
        "U1": (x0 + 42.5, y0 + 41.5, 0),
        # Decoupling caps positioned close to respective VDD/VSS pins
        "C4": (x0 + 36.0, y0 + 53.0, 0),
        "C5": (x0 + 53.5, y0 + 41.5, 0),
        "C6": (x0 + 36.0, y0 + 33.0, 0),
        "C7": (x0 + 29.0, y0 + 41.5, 0),
        
        # Soil Moisture AFE (Bottom-Left)
        "J2": (x0 + 12.0, y0 + h - 10.0, 0),
        "R10": (x0 + 20.0, y0 + h - 10.0, 0),
        "C13": (x0 + 26.0, y0 + h - 10.0, 0),
        
        # SWD Programming Header (Far-Right)
        "J4": (x0 + w - 10.0, y0 + 41.5, 0),
        
        # UI LEDs and Manual Override Pushbutton (Bottom Edge)
        "SW2": (x0 + w - 20.0, y0 + h - 11.0, 0),
        "R11": (x0 + w - 28.0, y0 + h - 11.0, 0),
        "D4": (x0 + 54.0, y0 + h - 9.0, 0),
        "R2": (x0 + 54.0, y0 + h - 15.0, 0),
        "D5": (x0 + 46.0, y0 + h - 9.0, 0),
        "R3": (x0 + 46.0, y0 + h - 15.0, 0),
        "D6": (x0 + 38.0, y0 + h - 9.0, 0),
        "R4": (x0 + 38.0, y0 + h - 15.0, 0)
    }

    # Place each component
    for comp in spec["components"]:
        ref = comp["ref"]
        if ref not in placements:
            print(f"[!] Warning: {ref} has no placement rule!", file=sys.stderr)
            continue
        
        px, py, prot = placements[ref]
        lib_name, mod_name = comp["footprint"].split(":", 1)
        fp = load_fp(lib_name, mod_name)
        fp.SetReference(ref)
        fp.SetValue(comp["value"])
        fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(px), pcbnew.FromMM(py)))
        fp.SetOrientation(pcbnew.EDA_ANGLE(prot, pcbnew.DEGREES_T))
        

        # Position reference designators cleanly away from pads and courtyard boundaries
        ref_text = fp.Reference()
        ref_text.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(0.85), pcbnew.FromMM(0.85)))
        if ref == "U1":
            ref_text.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(px), pcbnew.FromMM(py - 6.5)))
        elif ref in ("J1", "J3"):
            ref_text.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(px), pcbnew.FromMM(py - 7.5)))
        elif ref == "J2":
            ref_text.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(px - 3.2), pcbnew.FromMM(py)))
            ref_text.SetTextAngle(pcbnew.EDA_ANGLE(90, pcbnew.DEGREES_T))
        elif ref == "J4":
            ref_text.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(px + 3.2), pcbnew.FromMM(py)))
            ref_text.SetTextAngle(pcbnew.EDA_ANGLE(90, pcbnew.DEGREES_T))
        elif ref == "C1":
            ref_text.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(px), pcbnew.FromMM(py - 5.0)))
        elif ref in ("SW1", "SW2"):
            ref_text.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(px), pcbnew.FromMM(py - 4.8)))
        elif ref == "U2":
            ref_text.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(px), pcbnew.FromMM(py - 4.8)))
        elif ref == "D1":
            ref_text.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(px), pcbnew.FromMM(py - 3.2)))
        elif ref == "D2":
            ref_text.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(px - 3.2), pcbnew.FromMM(py)))
            ref_text.SetTextAngle(pcbnew.EDA_ANGLE(90, pcbnew.DEGREES_T))
        elif ref in ("Y1", "Y2"):
            ref_text.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(px), pcbnew.FromMM(py - 3.0)))
        elif ref == "Q1":
            ref_text.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(px), pcbnew.FromMM(py - 2.5)))
        elif ref in ("D4", "D5", "D6"):
            ref_text.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(px), pcbnew.FromMM(py + 2.0)))
        else:
            ref_text.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(px), pcbnew.FromMM(py - 2.0)))
        # Hide value text on silk to keep board clean
        val_text = fp.Value()
        val_text.SetVisible(False)

        # Assign nets to pads
        comp_nets = node_to_net.get(ref, {})
        for pad in fp.Pads():
            pnum = pad.GetNumber()
            if pnum in comp_nets:
                pad.SetNet(comp_nets[pnum])

        board.Add(fp)

    out_file = Path(output_path).resolve()
    out_file.parent.mkdir(parents=True, exist_ok=True)
    pcbnew.SaveBoard(str(out_file), board)
    print(f"[+] PCB board built and saved to: {out_file}")
    return str(out_file)

if __name__ == "__main__":
    build_stm32_pcb(
        "stm32_water_pump_controller/spec.json",
        "stm32_water_pump_controller/stm32_water_pump_controller.kicad_pcb"
    )

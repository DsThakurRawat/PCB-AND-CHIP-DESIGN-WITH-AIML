#!/usr/bin/env python3
"""
Direct Scripted Approach: Add and Fill Copper Zone using pcbnew.
Demonstrates deterministic, non-failing copper zone addition.
"""

import sys
from pathlib import Path
import pcbnew

def add_copper_zone(
    pcb_path: str,
    net_name: str = "GND",
    layer: str = "B.Cu",
    x1: float = 50.0,
    y1: float = 50.0,
    x2: float = 150.0,
    y2: float = 130.0
) -> str:
    pcb = Path(pcb_path).resolve()
    board = pcbnew.LoadBoard(str(pcb))
    if not board:
        raise ValueError(f"Could not load board: {pcb}")

    # 1. Ensure net exists or create it
    net = board.FindNet(net_name)
    if not net:
        net = pcbnew.NETINFO_ITEM(board, net_name)
        board.Add(net)

    # 2. Create zone container
    zone = pcbnew.ZONE(board)
    layer_id = board.GetLayerID(layer) if layer != "B.Cu" else pcbnew.B_Cu
    zone.SetLayer(layer_id)
    zone.SetNet(net)

    # 3. Add polygon corners
    poly = pcbnew.SHAPE_LINE_CHAIN()
    poly.Append(pcbnew.FromMM(x1), pcbnew.FromMM(y1))
    poly.Append(pcbnew.FromMM(x2), pcbnew.FromMM(y1))
    poly.Append(pcbnew.FromMM(x2), pcbnew.FromMM(y2))
    poly.Append(pcbnew.FromMM(x1), pcbnew.FromMM(y2))
    poly.SetClosed(True)
    
    zone.AddPolygon(poly)
    board.Add(zone)

    # 4. Fill zones
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())

    pcbnew.SaveBoard(str(pcb), board)
    print(f"[+] Copper zone for net '{net_name}' added on {layer} and filled successfully in {pcb.name}")
    return str(pcb)

if __name__ == "__main__":
    pcb_arg = sys.argv[1] if len(sys.argv) > 1 else "demo_board/demo_board.kicad_pcb"
    add_copper_zone(pcb_arg)

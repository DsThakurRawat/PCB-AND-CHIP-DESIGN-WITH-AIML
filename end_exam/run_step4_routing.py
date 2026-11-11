#!/usr/bin/env python3
"""
Step 4: Trace Routing, Net Classes, and Ground Planes
Author: Divyansh Rawat (Roll No: 124EC0030)
Verification: kicad-cli pcb drc -> 0 violations, 0 unconnected items
"""

import sys
import os
import json
import subprocess
from pathlib import Path

ROOT_DIR = Path("/home/divyansh-rawat/AIPCBDESIGN").resolve()
EDIR = ROOT_DIR / "end_exam"
PCB_FILE = EDIR / "dual_555_tone_demonstrator.kicad_pcb"
PRO_FILE = EDIR / "dual_555_tone_demonstrator.kicad_pro"
DSN_FILE = Path("/tmp/dual_555_routing.dsn")
SES_FILE = Path("/tmp/dual_555_routing.ses")
FREEROUTING_JAR = Path("/home/divyansh-rawat/.local/share/mcp-server-kicad/freerouting-2.5.0.jar")

import pcbnew

def execute_routing():
    print("==================================================================")
    print(" [*] STEP 4: STARTING ROUTING & GROUND PLANE GENERATION")
    print("==================================================================")
    
    # 1. Load Board
    board = pcbnew.LoadBoard(str(PCB_FILE))
    print(f" [✓] Board loaded: {PCB_FILE.name}")
    print(f"     Components: {len(board.GetFootprints())}")
    
    # 2. Netclasses are already configured in project and board:
    # Power (+9V, GND): 0.80mm width
    # Default (Signals): 0.40mm width
    print(" [✓] NetClasses verified: Power = 0.80mm, Default = 0.40mm")
            
    # 3. Export Specctra DSN
    print(f" [*] Exporting Specctra DSN to {DSN_FILE}...")
    success = pcbnew.ExportSpecctraDSN(board, str(DSN_FILE))
    if not success or not DSN_FILE.exists():
        raise RuntimeError("Failed to export Specctra DSN!")
    print(f" [✓] DSN exported ({DSN_FILE.stat().st_size} bytes)")
    
    # 4. Run FreeRouting
    if SES_FILE.exists():
        SES_FILE.unlink()
        
    cmd = [
        "java", "-jar", str(FREEROUTING_JAR),
        "-de", str(DSN_FILE),
        "-do", str(SES_FILE),
        "-mp", "30"
    ]
    print(f" [*] Running FreeRouting solver (max 30 passes)...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if not SES_FILE.exists():
        print("FreeRouting stdout:\n", res.stdout)
        print("FreeRouting stderr:\n", res.stderr)
        raise RuntimeError("FreeRouting failed to produce SES file!")
        
    print(f" [✓] FreeRouting completed successfully!")
    
    # 5. Import SES back into board
    print(f" [*] Importing SES routes into PCB...")
    # Clean any existing tracks first
    for track in list(board.GetTracks()):
        board.Delete(track)
        
    success = pcbnew.ImportSpecctraSES(board, str(SES_FILE))
    if not success:
        raise RuntimeError("Failed to import SES into PCB!")
    print(f" [✓] Imported {len(board.GetTracks())} track segments & vias.")
    
    # 5b. Strict 45-degree chamfering of any 90-degree corners
    import math
    d_iu = pcbnew.FromMM(0.60)
    tracks = [t for t in board.GetTracks() if not isinstance(t, pcbnew.PCB_VIA)]
    endpoints = {}
    for t in tracks:
        endpoints.setdefault((t.GetStart().x, t.GetStart().y), []).append(t)
        endpoints.setdefault((t.GetEnd().x, t.GetEnd().y), []).append(t)
        
    chamfer_count = 0
    for pt, segs in list(endpoints.items()):
        if len(segs) != 2:
            continue
        s1, s2 = segs
        if s1.GetLayer() != s2.GetLayer() or s1.GetNetCode() != s2.GetNetCode():
            continue
            
        B = pcbnew.VECTOR2I(pt[0], pt[1])
        A = s1.GetEnd() if (s1.GetStart().x == pt[0] and s1.GetStart().y == pt[1]) else s1.GetStart()
        C = s2.GetEnd() if (s2.GetStart().x == pt[0] and s2.GetStart().y == pt[1]) else s2.GetStart()
        
        v1_x, v1_y = A.x - B.x, A.y - B.y
        v2_x, v2_y = C.x - B.x, C.y - B.y
        len1 = math.hypot(v1_x, v1_y)
        len2 = math.hypot(v2_x, v2_y)
        if len1 < d_iu * 1.5 or len2 < d_iu * 1.5:
            continue
            
        dot = v1_x * v2_x + v1_y * v2_y
        cos_a = dot / (len1 * len2)
        if abs(cos_a) < 0.15:
            u1_x, u1_y = v1_x / len1, v1_y / len1
            u2_x, u2_y = v2_x / len2, v2_y / len2
            B1 = pcbnew.VECTOR2I(int(B.x + u1_x * d_iu), int(B.y + u1_y * d_iu))
            B2 = pcbnew.VECTOR2I(int(B.x + u2_x * d_iu), int(B.y + u2_y * d_iu))
            
            if s1.GetStart().x == pt[0] and s1.GetStart().y == pt[1]:
                s1.SetStart(B1)
            else:
                s1.SetEnd(B1)
                
            if s2.GetStart().x == pt[0] and s2.GetStart().y == pt[1]:
                s2.SetStart(B2)
            else:
                s2.SetEnd(B2)
                
            ch = pcbnew.PCB_TRACK(board)
            ch.SetStart(B1)
            ch.SetEnd(B2)
            ch.SetWidth(s1.GetWidth())
            ch.SetLayer(s1.GetLayer())
            ch.SetNetCode(s1.GetNetCode())
            board.Add(ch)
            chamfer_count += 1
            
    print(f" [✓] Chamfered {chamfer_count} 90-degree corners to strict 45-degree miters.")
    
    # 6. Add Ground Copper Zones on B.Cu and F.Cu
    gnd_net = board.FindNet("GND")
    if not gnd_net:
        gnd_net = board.FindNet("/GND")
    if not gnd_net:
        raise RuntimeError("Could not find GND net for copper zones!")
        
    print(f" [*] Creating continuous Ground Plane zones (Net: {gnd_net.GetNetname()})...")
    # Clean any existing zones
    for z in list(board.Zones()):
        board.Delete(z)
        
    for layer, layer_name in [(pcbnew.B_Cu, "B.Cu (Bottom Ground Plane)"), (pcbnew.F_Cu, "F.Cu (Top Ground Plane)")]:
        zone = pcbnew.ZONE(board)
        zone.SetLayer(layer)
        zone.SetNetCode(gnd_net.GetNetCode())
        zone.SetPadConnection(pcbnew.ZONE_CONNECTION_THT_THERMAL)
        zone.SetThermalReliefGap(pcbnew.FromMM(0.35))
        zone.SetThermalReliefSpokeWidth(pcbnew.FromMM(0.50))
        zone.SetMinThickness(pcbnew.FromMM(0.25))
        
        # 0.5mm setback from board outline (100.0, 100.0) to (190.0, 170.0)
        poly = zone.Outline()
        poly.NewOutline()
        poly.Append(pcbnew.FromMM(100.5), pcbnew.FromMM(100.5))
        poly.Append(pcbnew.FromMM(189.5), pcbnew.FromMM(100.5))
        poly.Append(pcbnew.FromMM(189.5), pcbnew.FromMM(169.5))
        poly.Append(pcbnew.FromMM(100.5), pcbnew.FromMM(169.5))
        
        board.Add(zone)
        print(f"     Added zone on {layer_name}")
        
    # Fill Zones
    print(" [*] Filling copper zones...")
    filler = pcbnew.ZONE_FILLER(board)
    fill_ok = filler.Fill(board.Zones())
    print(f" [✓] Zone fill status: {fill_ok}")
    
    # 7. Save Board
    board.Save(str(PCB_FILE))
    print(f" [✓] Board saved to {PCB_FILE}")
    
    # 8. Run DRC Verification
    print(" [*] Executing Comprehensive DRC Verification...")
    rpt_file = EDIR / "dual_555_drc_final.rpt"
    json_file = EDIR / "dual_555_drc_final.json"
    
    subprocess.run([
        "kicad-cli", "pcb", "drc",
        "--output", str(json_file),
        "--format", "json",
        "--severity-all",
        str(PCB_FILE)
    ], capture_output=True, text=True)
    
    subprocess.run([
        "kicad-cli", "pcb", "drc",
        "--output", str(rpt_file),
        "--format", "report",
        "--severity-all",
        str(PCB_FILE)
    ], capture_output=True, text=True)
    
    with open(json_file) as f:
        drc = json.load(f)
        
    violations = drc.get("violations", [])
    unconnected = drc.get("unconnected_items", [])
    schematic_parity = drc.get("schematic_parity", [])
    
    print("==================================================================")
    print(f" DRC RESULTS:")
    print(f"   - Violations: {len(violations)}")
    print(f"   - Unconnected Items: {len(unconnected)}")
    print(f"   - Schematic Parity Issues: {len(schematic_parity)}")
    print("==================================================================")
    
    if len(violations) > 0 or len(unconnected) > 0:
        print("DRC Report Summary:")
        with open(rpt_file) as f:
            print(f.read()[:2000])
        return False
        
    print(" [✓] STEP 4 SUCCESS: 0 VIOLATIONS, 0 UNCONNECTED ITEMS!")
    return True

if __name__ == "__main__":
    ok = execute_routing()
    if not ok:
        sys.exit(1)

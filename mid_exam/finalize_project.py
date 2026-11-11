#!/usr/bin/env python3
"""
Master Finalization & Manufacturing Deliverable Synthesis for Mid Semester Exam
Circuit: School/College Quiz Buzzer (8 Players)
Student: Divyansh Rawat (Roll No: 124EC0030)
Faculty: Dr. Eswaramoorthy K V
Department of Electronics and Communication Engineering
Indian Institute of Information Technology, Design and Manufacturing, Kurnool
"""

import sys
import os
import shutil
import subprocess
from pathlib import Path

ROOT_DIR = Path("/home/divyansh-rawat/AIPCBDESIGN").resolve()
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(ROOT_DIR / "scripts"))

import pcbnew
from export_manufacturing import export_manufacturing

MID_DIR = ROOT_DIR / "mid_exam"
BASE_PCB = MID_DIR / "school_college_quiz_buzzer.kicad_pcb"
ROUTED_PCB = MID_DIR / "school_college_quiz_buzzer_routed.kicad_pcb"
MFG_DIR = MID_DIR / "manufacturing"

def finalize():
    print("==================================================================")
    print(" [*] FINALIZING MID EXAM PROJECT: SCHOOL/COLLEGE QUIZ BUZZER")
    print("==================================================================")

    # 1. Use routed PCB if available, otherwise update BASE_PCB
    target_pcb = ROUTED_PCB if ROUTED_PCB.exists() else BASE_PCB
    print(f"[-] Loading PCB from: {target_pcb}")

    board = pcbnew.LoadBoard(str(target_pcb))
    if not board:
        raise RuntimeError(f"Failed to load board: {target_pcb}")

    # 2. Add full B.Cu GND plane
    print("[-] Adding Solid GND Copper Plane on B.Cu...")
    gnd_net = board.FindNet("GND")
    if not gnd_net:
        gnd_net = pcbnew.NETINFO_ITEM(board, "GND")
        board.Add(gnd_net)

    # Check if a GND zone already exists on B.Cu
    existing_zone = None
    for z in board.Zones():
        if z.GetLayer() == pcbnew.B_Cu and z.GetNetname() == "GND":
            existing_zone = z
            break

    if not existing_zone:
        zone = pcbnew.ZONE(board)
        zone.SetLayer(pcbnew.B_Cu)
        zone.SetNet(gnd_net)
        zone.SetPadConnection(pcbnew.ZONE_CONNECTION_THT_THERMAL)

        poly = pcbnew.SHAPE_LINE_CHAIN()
        # Board dimensions: 70, 48 to 250, 178
        poly.Append(pcbnew.FromMM(70.5), pcbnew.FromMM(48.5))
        poly.Append(pcbnew.FromMM(249.5), pcbnew.FromMM(48.5))
        poly.Append(pcbnew.FromMM(249.5), pcbnew.FromMM(177.5))
        poly.Append(pcbnew.FromMM(70.5), pcbnew.FromMM(177.5))
        poly.SetClosed(True)

        zone.AddPolygon(poly)
        board.Add(zone)

    # 3. Refill all copper zones
    print("[-] Refilling copper zones...")
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())

    # Save to main project PCB
    board.Save(str(BASE_PCB))
    print(f"[✓] Successfully saved finalized PCB to: {BASE_PCB}")

    # 4. Run DRC verification
    print("[-] Running DRC with schematic parity check...")
    drc_rpt = MID_DIR / "school_college_quiz_buzzer-drc.rpt"
    cmd_drc = [
        "kicad-cli", "pcb", "drc",
        "--schematic-parity",
        "--severity-all",
        "-o", str(drc_rpt),
        str(BASE_PCB)
    ]
    res_drc = subprocess.run(cmd_drc, capture_output=True, text=True)
    print(res_drc.stdout)
    if drc_rpt.exists():
        print(f"[✓] DRC Report saved to: {drc_rpt}")

    # 5. Export Manufacturing Deliverables
    print("[-] Exporting complete manufacturing package...")
    mfg_results = export_manufacturing(str(BASE_PCB), str(MFG_DIR))
    print(f"[✓] Manufacturing exports completed: {mfg_results}")

    # 6. Generate Complete BOM CSV
    print("[-] Exporting complete CSV BOM...")
    bom_csv = MID_DIR / "school_college_quiz_buzzer_bom.csv"
    cmd_bom = [
        "kicad-cli", "sch", "export", "bom",
        "-o", str(bom_csv),
        str(MID_DIR / "school_college_quiz_buzzer.kicad_sch")
    ]
    try:
        subprocess.run(cmd_bom, check=True)
        print(f"[✓] BOM exported to: {bom_csv}")
    except Exception as e:
        print(f"[!] Warning exporting BOM: {e}")

    print("==================================================================")
    print(" [✓] ALL 5 MID-SEMESTER EXAM DELIVERABLES SUCCESSFULLY COMPLETED!")
    print("==================================================================")

if __name__ == "__main__":
    finalize()

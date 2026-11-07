#!/usr/bin/env python3
"""
Master Build & Verification Pipeline for 02_sallen_key_filter.
Orchestrates:
1. Schematic generation from spec.json (.kicad_sch)
2. ERC validation (0 errors, 0 warnings)
3. PCB layout synthesis with collision-free component floorplanning
4. Automated 2-layer FreeRouting
5. DRC validation (0 violations, 0 unconnected items)
6. Complete manufacturing export (Gerbers, Drill, pos CSV, PDF, iBOM, 3D render)
"""

import sys
import os
import re
import json
import subprocess
import shutil
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.resolve()
WORKSPACE_DIR = PROJECT_DIR.parent.parent
sys.path.insert(0, str(WORKSPACE_DIR))

import pcbnew
import mcp_server_kicad.pcb as ar
from pcb_engine.sch_builder import build_from_spec_file
from scripts.generate_ibom import generate_ibom
from scripts.render_3d import render_3d_pcb

SPEC_PATH = PROJECT_DIR / "spec.json"
SCH_PATH = PROJECT_DIR / "sallen_key_filter.kicad_sch"
PCB_PATH = PROJECT_DIR / "sallen_key_filter_routed.kicad_pcb"
MAIN_PCB_PATH = PROJECT_DIR / "sallen_key_filter.kicad_pcb"
PRO_PATH = PROJECT_DIR / "sallen_key_filter.kicad_pro"
MFG_DIR = PROJECT_DIR / "manufacturing"

def step1_schematic():
    print("\n" + "="*60)
    print("[1/6] Building KiCad 9 Schematic from spec.json...")
    print("="*60)
    build_from_spec_file(str(SPEC_PATH), str(SCH_PATH))

    # Ensure project file exists
    ref_pro = WORKSPACE_DIR / "demo_board" / "demo_board.kicad_pro"
    if ref_pro.exists() and not PRO_PATH.exists():
        shutil.copy(ref_pro, PRO_PATH)
    print(f"[+] Schematic generated: {SCH_PATH}")

def step2_erc():
    print("\n" + "="*60)
    print("[2/6] Running Electrical Rules Checker (ERC)...")
    print("="*60)
    json_rpt = PROJECT_DIR / "sallen_key_filter_erc.json"
    text_rpt = PROJECT_DIR / "sallen_key_filter_erc.rpt"

    cmd_json = [
        "kicad-cli", "sch", "erc",
        "--format", "json",
        "--severity-all",
        "--exit-code-violations",
        "--output", str(json_rpt),
        str(SCH_PATH)
    ]
    proc = subprocess.run(cmd_json, capture_output=True, text=True)

    cmd_text = [
        "kicad-cli", "sch", "erc",
        "--severity-all",
        "--output", str(text_rpt),
        str(SCH_PATH)
    ]
    subprocess.run(cmd_text, capture_output=True, text=True)

    print(f"[-] ERC exit code: {proc.returncode}")
    if json_rpt.exists():
        with open(json_rpt, "r", encoding="utf-8") as f:
            erc_data = json.load(f)
        violations = list(erc_data.get("violations", []))
        for sheet in erc_data.get("sheets", []):
            violations.extend(sheet.get("violations", []))
        print(f"[-] Total ERC Violations: {len(violations)}")
        for v in violations:
            print(f"    ! [{v.get('severity')}] {v.get('description')}")
        if violations or proc.returncode != 0:
            raise RuntimeError(f"ERC failed with {len(violations)} violations")
    print(f"[+] ERC PASSED (0 errors, 0 warnings).")

def step3_layout():
    print("\n" + "="*60)
    print("[3/6] Generating Clean Unrouted PCB Layout...")
    print("="*60)
    board = pcbnew.BOARD()
    x0, y0 = 100.0, 100.0
    width, height = 85.0, 48.0

    # Board Outline on Edge.Cuts
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
    net_names = ["VIN", "N_R1_R2", "V_PLUS", "VOUT", "GND", "+12V", "-12V"]
    net_map = {}
    for name in net_names:
        net_info = pcbnew.NETINFO_ITEM(board, name)
        board.Add(net_info)
        net_map[name] = net_info

    # Collision-free footprint floorplanning
    fp_defs = {
        "J1": ("TerminalBlock_Phoenix", "TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal", "SIG_IN", (x0 + 9.0, y0 + 24.0), 0),
        "R1": ("Resistor_SMD", "R_0805_2012Metric", "15.9k", (x0 + 22.0, y0 + 20.0), 0),
        "R2": ("Resistor_SMD", "R_0805_2012Metric", "15.9k", (x0 + 32.0, y0 + 20.0), 0),
        "C1": ("Capacitor_SMD", "C_0805_2012Metric", "10nF", (x0 + 27.0, y0 + 13.0), 90),
        "C2": ("Capacitor_SMD", "C_0805_2012Metric", "10nF", (x0 + 32.0, y0 + 29.0), 90),
        "U1": ("Package_SO", "SOIC-8_3.9x4.9mm_P1.27mm", "TL071", (x0 + 46.0, y0 + 24.0), 0),
        "J2": ("TerminalBlock_Phoenix", "TerminalBlock_Phoenix_MKDS-1,5-3-5.08_1x03_P5.08mm_Horizontal", "POWER", (x0 + 46.0, y0 + 40.0), 0),
        "C3": ("Capacitor_SMD", "C_0805_2012Metric", "100nF", (x0 + 58.0, y0 + 16.0), 90),
        "C4": ("Capacitor_SMD", "C_0805_2012Metric", "100nF", (x0 + 58.0, y0 + 32.0), 90),
        "J3": ("TerminalBlock_Phoenix", "TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal", "SIG_OUT", (x0 + 76.0, y0 + 24.0), 180)
    }

    pin_assignments = {
        "J1": {"1": "VIN", "2": "GND"},
        "R1": {"1": "VIN", "2": "N_R1_R2"},
        "R2": {"1": "N_R1_R2", "2": "V_PLUS"},
        "C1": {"1": "N_R1_R2", "2": "VOUT"},
        "C2": {"1": "V_PLUS", "2": "GND"},
        "U1": {"3": "V_PLUS", "2": "VOUT", "6": "VOUT", "7": "+12V", "4": "-12V"},
        "J2": {"1": "+12V", "2": "GND", "3": "-12V"},
        "C3": {"1": "+12V", "2": "GND"},
        "C4": {"1": "GND", "2": "-12V"},
        "J3": {"1": "VOUT", "2": "GND"}
    }

    for ref, (lib, mod, val, pos, rot) in fp_defs.items():
        lib_path = f"/usr/share/kicad/footprints/{lib}.pretty"
        fp = pcbnew.FootprintLoad(lib_path, mod)
        if not fp:
            raise RuntimeError(f"Could not load footprint {lib}:{mod}")
        fp.SetReference(ref)
        fp.SetValue(val)
        fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(pos[0]), pcbnew.FromMM(pos[1])))
        fp.SetOrientation(pcbnew.EDA_ANGLE(rot, pcbnew.DEGREES_T))

        ref_text = fp.Reference()
        ref_text.SetVisible(True)
        ref_text.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(pos[0]), pcbnew.FromMM(pos[1] - 4.5)))
        val_text = fp.Value()
        val_text.SetVisible(False)

        for pad in fp.Pads():
            pad_num = pad.GetNumber()
            net_name = pin_assignments.get(ref, {}).get(pad_num)
            if net_name and net_name in net_map:
                pad.SetNet(net_map[net_name])

        board.Add(fp)

    # Silkscreen text
    def add_silk(text: str, x: float, y: float, size: float = 1.0):
        t = pcbnew.PCB_TEXT(board)
        t.SetText(text)
        t.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
        t.SetLayer(pcbnew.F_SilkS)
        t.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(size), pcbnew.FromMM(size)))
        board.Add(t)

    add_silk("SALLEN-KEY ACTIVE LPF (1kHz)", x0 + 20.0, y0 + 5.0, size=1.3)
    add_silk("IN", x0 + 6.0, y0 + 34.0, size=1.0)
    add_silk("+12V GND -12V", x0 + 34.0, y0 + 44.5, size=0.9)
    add_silk("OUT", x0 + 72.0, y0 + 34.0, size=1.0)

    unrouted_path = PROJECT_DIR / "sallen_key_filter.kicad_pcb"
    pcbnew.SaveBoard(str(unrouted_path), board)
    print(f"[+] Unrouted board saved: {unrouted_path}")
    return unrouted_path

def step4_autoroute(unrouted_pcb: Path):
    print("\n" + "="*60)
    print("[4/6] Autorouting Traces with FreeRouting...")
    print("="*60)
    dsn_path = PROJECT_DIR / "sallen_key_filter.dsn"
    ses_path = PROJECT_DIR / "sallen_key_filter.ses"

    # Export DSN
    ar._export_dsn(str(unrouted_pcb), str(dsn_path))

    # Set trace width to 0.35mm (350um) and clearance to 0.25mm (250um)
    content = dsn_path.read_text(encoding="utf-8")
    content = content.replace('(rule\n      (width 200)\n      (clearance 200)', '(rule\n      (width 350)\n      (clearance 250)')
    dsn_path.write_text(content, encoding="utf-8")

    # Run FreeRouting
    jar, _ = ar._ensure_jar()
    java = ar._find_on_path("java")
    print(f"[-] Running FreeRouting engine (jar: {Path(jar).name}, java: {java})...")
    err = ar._run_freerouting(jar, str(dsn_path), str(ses_path), max_passes=25, num_threads=1, timeout=120, java=java)
    if err:
        raise RuntimeError(f"FreeRouting error: {err}")

    # Import SES into final PCB
    print(f"[-] Importing routed session into {PCB_PATH}...")
    ar._import_ses(str(unrouted_pcb), str(ses_path), str(PCB_PATH))
    ar._fix_displaced_fp_text(str(PCB_PATH))

    # Clean up reference text placement
    board = pcbnew.LoadBoard(str(PCB_PATH))
    for fp in board.GetFootprints():
        ref = fp.GetReference()
        pos = fp.GetPosition()
        ref_text = fp.Reference()
        ref_text.SetVisible(True)
        val_text = fp.Value()
        val_text.SetVisible(False)
        if ref in ["J1", "J3"]:
            ref_text.SetPosition(pcbnew.VECTOR2I(pos.x, pos.y - pcbnew.FromMM(8.0)))
        elif ref == "J2":
            ref_text.SetPosition(pcbnew.VECTOR2I(pos.x, pos.y - pcbnew.FromMM(8.0)))
        elif ref == "U1":
            ref_text.SetPosition(pcbnew.VECTOR2I(pos.x, pos.y - pcbnew.FromMM(5.0)))
        else:
            ref_text.SetPosition(pcbnew.VECTOR2I(pos.x, pos.y - pcbnew.FromMM(3.0)))
    pcbnew.SaveBoard(str(PCB_PATH), board)

    shutil.copy(PCB_PATH, MAIN_PCB_PATH)
    print(f"[+] Routed PCB successfully saved: {PCB_PATH}")

def step5_drc():
    print("\n" + "="*60)
    print("[5/6] Running Design Rules Checker (DRC)...")
    print("="*60)
    json_rpt = PROJECT_DIR / "sallen_key_filter_routed_drc.json"
    text_rpt = PROJECT_DIR / "sallen_key_filter_routed_drc.rpt"

    cmd_json = [
        "kicad-cli", "pcb", "drc",
        "--format", "json",
        "--severity-all",
        "--exit-code-violations",
        "--output", str(json_rpt),
        str(PCB_PATH)
    ]
    proc = subprocess.run(cmd_json, capture_output=True, text=True)

    cmd_text = [
        "kicad-cli", "pcb", "drc",
        "--severity-all",
        "--output", str(text_rpt),
        str(PCB_PATH)
    ]
    subprocess.run(cmd_text, capture_output=True, text=True)

    print(f"[-] DRC exit code: {proc.returncode}")
    if json_rpt.exists():
        with open(json_rpt, "r", encoding="utf-8") as f:
            drc_data = json.load(f)
        violations = drc_data.get("violations", [])
        unconnected = drc_data.get("unconnected_items", [])
        print(f"[-] Total DRC Violations: {len(violations)}")
        print(f"[-] Total Unconnected Items: {len(unconnected)}")
        for v in violations:
            print(f"    ! [{v.get('severity')}] {v.get('type')}: {v.get('description')}")
        for u in unconnected:
            print(f"    ! [UNCONNECTED] {u.get('description')}")
        if violations or unconnected:
            raise RuntimeError(f"DRC failed with {len(violations)} violations, {len(unconnected)} unconnected")
    print(f"[+] DRC PASSED (0 violations, 0 unconnected). Reports: {json_rpt.name}, {text_rpt.name}")

def step6_manufacturing():
    print("\n" + "="*60)
    print("[6/6] Exporting Complete Manufacturing Package...")
    print("="*60)
    MFG_DIR.mkdir(parents=True, exist_ok=True)
    gerber_dir = MFG_DIR / "gerbers"
    gerber_dir.mkdir(parents=True, exist_ok=True)

    # 1. Gerbers
    print("[-] Exporting RS-274X Gerber layers...")
    cmd_gerber = [
        "kicad-cli", "pcb", "export", "gerbers",
        "--output", str(gerber_dir) + "/",
        str(PCB_PATH)
    ]
    subprocess.run(cmd_gerber, check=True)

    # 2. Drill files
    print("[-] Exporting Excellon drill files...")
    cmd_drill = [
        "kicad-cli", "pcb", "export", "drill",
        "--output", str(gerber_dir) + "/",
        "--format", "excellon",
        str(PCB_PATH)
    ]
    subprocess.run(cmd_drill, check=True)

    # 3. Create ZIP archive
    zip_base = MFG_DIR / "sallen_key_filter_gerbers"
    shutil.make_archive(str(zip_base), "zip", gerber_dir)
    print(f"[+] Gerber ZIP archive created: {zip_base}.zip")

    # 4. Pick-and-Place Position CSV
    pos_file = MFG_DIR / "sallen_key_filter_pos.csv"
    cmd_pos = [
        "kicad-cli", "pcb", "export", "pos",
        "--format", "csv",
        "--units", "mm",
        "--output", str(pos_file),
        str(PCB_PATH)
    ]
    subprocess.run(cmd_pos, check=True)
    print(f"[+] Pick-and-place CSV: {pos_file.name}")

    # 5. PDF Layout
    pdf_file = MFG_DIR / "sallen_key_filter.pdf"
    cmd_pdf = [
        "kicad-cli", "pcb", "export", "pdf",
        "--layers", "F.Cu,B.Cu,F.SilkS,Edge.Cuts",
        "--output", str(pdf_file),
        str(PCB_PATH)
    ]
    subprocess.run(cmd_pdf, check=True)
    print(f"[+] PCB Layout PDF: {pdf_file.name}")

    # 6. Interactive HTML BOM
    print("[-] Generating Interactive HTML BOM...")
    ibom_path = generate_ibom(str(PCB_PATH), str(MFG_DIR))
    print(f"[+] Interactive HTML BOM: {Path(ibom_path).name}")

    # 7. 3D Raytrace Render
    print("[-] Generating Photorealistic 3D Raytrace Render...")
    render_file = MFG_DIR / "sallen_key_filter_3d.png"
    render_3d_pcb(str(PCB_PATH), str(render_file), width=1920, height=1080, rotate="-45,0,45", zoom=1.4)
    print(f"[+] 3D render generated: {render_file}")

def main():
    print("==================================================================")
    print("   AUTONOMOUS SALLEN-KEY ACTIVE FILTER PCB END-TO-END PIPELINE    ")
    print("==================================================================")
    step1_schematic()
    step2_erc()
    unrouted = step3_layout()
    step4_autoroute(unrouted)
    step5_drc()
    step6_manufacturing()
    print("\n" + "="*60)
    print("  [SUCCESS] 02_SALLEN_KEY_FILTER COMPLETED WITH 0 ERRORS!         ")
    print("==================================================================")

if __name__ == "__main__":
    main()

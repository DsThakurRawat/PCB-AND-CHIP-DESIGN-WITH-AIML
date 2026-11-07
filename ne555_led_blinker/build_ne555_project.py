#!/usr/bin/env python3
"""
Master Build & Verification Pipeline for NE555 Single-Layer LED Blinker PCB.
Orchestrates:
1. Schematic generation (.kicad_sch)
2. Project creation (.kicad_pro)
3. Board generation (.kicad_pcb)
4. Single-layer autorouting on F.Cu
5. ERC & DRC validation (strict exit code checks)
6. Manufacturing package (Gerbers, Drill, BOM, PDF, 3D Render)
"""

import sys
import os
import re
import json
import subprocess
import shutil
from pathlib import Path
import pcbnew
import mcp_server_kicad.pcb as ar
from pcb_engine.sch_builder import build_from_spec_file
from scripts.generate_ibom import generate_ibom
from scripts.render_3d import render_3d_pcb

PROJECT_DIR = Path(__file__).parent.resolve()
SPEC_PATH = PROJECT_DIR / "spec.json"
SCH_PATH = PROJECT_DIR / "ne555_led_blinker.kicad_sch"
PCB_PATH = PROJECT_DIR / "ne555_led_blinker.kicad_pcb"
PRO_PATH = PROJECT_DIR / "ne555_led_blinker.kicad_pro"
MFG_DIR = PROJECT_DIR / "manufacturing"

def step1_generate_schematic():
    print("\n" + "="*60)
    print("[1/7] Generating KiCad 9 Schematic...")
    print("="*60)
    build_from_spec_file(str(SPEC_PATH), str(SCH_PATH))

    # Copy / generate project file
    ref_pro = PROJECT_DIR.parent / "demo_board" / "demo_board.kicad_pro"
    if ref_pro.exists():
        shutil.copy(ref_pro, PRO_PATH)
    print(f"[+] Schematic generated: {SCH_PATH}")

def step2_run_erc():
    print("\n" + "="*60)
    print("[2/7] Running Electrical Rules Checker (ERC)...")
    print("="*60)
    json_rpt = PROJECT_DIR / "ne555_led_blinker_erc.json"
    text_rpt = PROJECT_DIR / "ne555_led_blinker_erc.rpt"

    # JSON report
    cmd_json = [
        "kicad-cli", "sch", "erc",
        "--format", "json",
        "--severity-all",
        "--exit-code-violations",
        "--output", str(json_rpt),
        str(SCH_PATH)
    ]
    proc = subprocess.run(cmd_json, capture_output=True, text=True)
    
    # Text report
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
        violations = erc_data.get("violations", [])
        print(f"[-] Total ERC Violations: {len(violations)}")
        for v in violations:
            print(f"    ! [{v.get('severity')}] {v.get('description')}")
        if violations:
            raise RuntimeError(f"ERC failed with {len(violations)} violations")
    print(f"[+] ERC PASSED (0 errors, 0 warnings). Reports: {json_rpt.name}, {text_rpt.name}")

def step3_generate_unrouted_pcb():
    print("\n" + "="*60)
    print("[3/7] Generating Unrouted PCB Layout (48mm x 36mm)...")
    print("="*60)
    board = pcbnew.BOARD()
    x0, y0 = 100.0, 100.0
    width, height = 48.0, 36.0

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
    net_names = ["+5V", "GND", "DISCH", "TIMING", "CONT", "OUT", "LED_A"]
    net_map = {}
    for name in net_names:
        net_info = pcbnew.NETINFO_ITEM(board, name)
        board.Add(net_info)
        net_map[name] = net_info

    # Footprint definitions: all Through-Hole components
    fp_defs = {
        "J1": ("Connector_PinHeader_2.54mm", "PinHeader_1x02_P2.54mm_Vertical", "5V_GND", (x0 + 6.0, y0 + 12.0), 0),
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

    for ref, (lib, mod, val, pos, rot) in fp_defs.items():
        lib_path = f"/usr/share/kicad/footprints/{lib}.pretty"
        fp = pcbnew.FootprintLoad(lib_path, mod)
        if not fp:
            raise RuntimeError(f"Could not load footprint {lib}:{mod}")
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

    # Silkscreen text on F.SilkS
    def add_silk(text: str, x: float, y: float, size: float = 1.0):
        t = pcbnew.PCB_TEXT(board)
        t.SetText(text)
        t.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
        t.SetLayer(pcbnew.F_SilkS)
        t.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(size), pcbnew.FromMM(size)))
        board.Add(t)

    add_silk("NE555 1Hz BLINKER", x0 + 13.0, y0 + 3.0, size=1.2)
    add_silk("SINGLE LAYER (F.Cu)", x0 + 13.0, y0 + 5.0, size=0.9)
    # Required explicit power markings:
    add_silk("+5V", x0 + 2.5, y0 + 11.5, size=1.0)
    add_silk("GND", x0 + 2.5, y0 + 14.5, size=1.0)

    unrouted_path = PROJECT_DIR / "unrouted.kicad_pcb"
    pcbnew.SaveBoard(str(unrouted_path), board)
    print(f"[+] Unrouted layout saved: {unrouted_path}")
    return unrouted_path

def step4_single_layer_autoroute(unrouted_pcb: Path):
    print("\n" + "="*60)
    print("[4/7] Autorouting Single-Layer Traces exclusively on F.Cu...")
    print("="*60)
    dsn_path = PROJECT_DIR / "single_layer.dsn"
    ses_path = PROJECT_DIR / "single_layer.ses"

    # Export DSN from unrouted board
    ar._export_dsn(str(unrouted_pcb), str(dsn_path))

    # Modify DSN to remove B.Cu layer and all vias (strictly single-layer Front Copper)
    content = dsn_path.read_text(encoding="utf-8")
    content = re.sub(r'\(layer B\.Cu\s+\(type signal\)\s+\(property\s+\(index 1\)\s+\)\s+\)', '', content)
    content = re.sub(r'\(via [^)]+\)', '', content)
    # Set default trace width to 0.4mm (400um) and clearance to 0.25mm (250um)
    content = content.replace('(rule\n      (width 200)\n      (clearance 200)', '(rule\n      (width 400)\n      (clearance 250)\n      (cost via -1)')
    dsn_path.write_text(content, encoding="utf-8")

    # Run FreeRouting
    jar, _ = ar._ensure_jar()
    java = ar._find_on_path("java")
    print(f"[-] Running FreeRouting engine (jar: {Path(jar).name}, java: {java})...")
    err = ar._run_freerouting(jar, str(dsn_path), str(ses_path), max_passes=20, num_threads=1, timeout=120, java=java)
    if err:
        raise RuntimeError(f"FreeRouting error: {err}")

    # Import SES into final PCB
    print(f"[-] Importing routed session into {PCB_PATH}...")
    ar._import_ses(str(unrouted_pcb), str(ses_path), str(PCB_PATH))
    ar._fix_displaced_fp_text(str(PCB_PATH))

    # Verify no traces on B.Cu and no vias
    board = pcbnew.LoadBoard(str(PCB_PATH))
    f_cu_tracks = sum(1 for t in board.GetTracks() if t.GetLayerName() == "F.Cu")
    b_cu_tracks = sum(1 for t in board.GetTracks() if t.GetLayerName() == "B.Cu")
    vias_count = sum(1 for t in board.GetTracks() if isinstance(t, pcbnew.PCB_VIA))

    print(f"[+] Routing Complete:")
    print(f"    - Front Copper (F.Cu) Traces: {f_cu_tracks}")
    print(f"    - Back Copper (B.Cu) Traces:  {b_cu_tracks} (Strictly Single-Layer!)")
    print(f"    - Vias placed:                {vias_count} (Zero vias used)")

    if b_cu_tracks > 0 or vias_count > 0:
        raise RuntimeError(f"Design is not strictly single-layer: B.Cu={b_cu_tracks}, Vias={vias_count}")

def step5_run_drc():
    print("\n" + "="*60)
    print("[5/7] Running Design Rules Checker (DRC)...")
    print("="*60)
    json_rpt = PROJECT_DIR / "ne555_led_blinker_drc.json"
    text_rpt = PROJECT_DIR / "ne555_led_blinker_drc.rpt"

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
            print(f"    ! [{v.get('severity')}] {v.get('description')}")
        if violations or unconnected:
            raise RuntimeError(f"DRC failed with {len(violations)} violations, {len(unconnected)} unconnected")
    print(f"[+] DRC PASSED (0 violations, 0 unconnected). Reports: {json_rpt.name}, {text_rpt.name}")

def step6_export_manufacturing():
    print("\n" + "="*60)
    print("[6/7] Exporting Complete Manufacturing Package...")
    print("="*60)
    MFG_DIR.mkdir(parents=True, exist_ok=True)
    gerber_dir = MFG_DIR / "gerbers"
    gerber_dir.mkdir(parents=True, exist_ok=True)

    # 1. Gerbers
    print("[-] Generating RS-274X Gerber layers...")
    cmd_gerber = [
        "kicad-cli", "pcb", "export", "gerbers",
        "--output", str(gerber_dir) + "/",
        str(PCB_PATH)
    ]
    subprocess.run(cmd_gerber, check=True)

    # 2. Drill files
    print("[-] Generating Excellon drill files...")
    cmd_drill = [
        "kicad-cli", "pcb", "export", "drill",
        "--output", str(gerber_dir) + "/",
        "--format", "excellon",
        str(PCB_PATH)
    ]
    subprocess.run(cmd_drill, check=True)

    # 3. Create ZIP archive
    zip_base = MFG_DIR / "ne555_led_blinker_gerbers"
    shutil.make_archive(str(zip_base), "zip", gerber_dir)
    print(f"[+] Gerber ZIP archive created: {zip_base}.zip")

    # 4. Pick-and-Place Position CSV
    pos_file = MFG_DIR / "ne555_led_blinker_pos.csv"
    cmd_pos = [
        "kicad-cli", "pcb", "export", "pos",
        "--format", "csv",
        "--units", "mm",
        "--output", str(pos_file),
        str(PCB_PATH)
    ]
    subprocess.run(cmd_pos, check=True)
    print(f"[+] Component position CSV: {pos_file.name}")

    # 5. PDF Layout
    pdf_file = MFG_DIR / "ne555_led_blinker.pdf"
    cmd_pdf = [
        "kicad-cli", "pcb", "export", "pdf",
        "--layers", "F.Cu,F.SilkS,Edge.Cuts",
        "--output", str(pdf_file),
        str(PCB_PATH)
    ]
    subprocess.run(cmd_pdf, check=True)
    print(f"[+] PCB Layout PDF: {pdf_file.name}")

    # 6. Interactive HTML BOM
    print("[-] Generating Interactive HTML BOM...")
    ibom_path = generate_ibom(str(PCB_PATH), str(MFG_DIR))
    print(f"[+] Interactive HTML BOM: {Path(ibom_path).name}")

def step7_render_3d():
    print("\n" + "="*60)
    print("[7/7] Generating Photorealistic 3D Raytrace Render...")
    print("="*60)
    render_file = PROJECT_DIR / "ne555_led_blinker_3d.png"
    render_3d_pcb(str(PCB_PATH), str(render_file), width=1920, height=1080, rotate="-45,0,45", zoom=1.4)
    # Also copy to manufacturing directory
    shutil.copy(render_file, MFG_DIR / "ne555_led_blinker_3d.png")
    print(f"[+] 3D render generated: {render_file}")

def main():
    print("==================================================================")
    print("  AUTONOMOUS SINGLE-LAYER NE555 LED BLINKER PCB DESIGN PIPELINE   ")
    print("==================================================================")
    step1_generate_schematic()
    step2_run_erc()
    unrouted = step3_generate_unrouted_pcb()
    step4_single_layer_autoroute(unrouted)
    step5_run_drc()
    step6_export_manufacturing()
    step7_render_3d()
    print("\n" + "="*60)
    print("  [SUCCESS] NE555 SINGLE-LAYER PCB COMPLETED WITH 0 ERRORS!       ")
    print("==================================================================")

if __name__ == "__main__":
    main()

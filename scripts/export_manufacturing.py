#!/usr/bin/env python3
"""
Complete Manufacturing Export Pipeline for KiCad 9.
Generates:
- Gerber files (RS-274X)
- NC Drill files (Excellon)
- Component position file (pick-and-place CSV)
- PDF documentation
- Interactive HTML BOM
- Altium-style 3D Raytraced Image
"""

import sys
import subprocess
import shutil
from pathlib import Path
from generate_ibom import generate_ibom
from render_3d import render_3d_pcb

def export_manufacturing(pcb_path: str, output_dir: str = None) -> dict:
    pcb = Path(pcb_path).resolve()
    if not pcb.exists():
        raise FileNotFoundError(f"PCB file not found: {pcb}")

    out = Path(output_dir).resolve() if output_dir else pcb.parent / "manufacturing"
    out.mkdir(parents=True, exist_ok=True)
    gerber_dir = out / "gerbers"
    gerber_dir.mkdir(parents=True, exist_ok=True)

    print(f"[*] Exporting manufacturing package to: {out}")

    # 1. Export Gerbers
    print("[-] Exporting Gerber layers...")
    cmd_gerber = [
        "kicad-cli", "pcb", "export", "gerbers",
        "--output", str(gerber_dir),
        str(pcb)
    ]
    subprocess.run(cmd_gerber, check=True)

    # 2. Export Drill files
    print("[-] Exporting Excellon drill files...")
    cmd_drill = [
        "kicad-cli", "pcb", "export", "drill",
        "--output", str(gerber_dir) + "/",
        "--format", "excellon",
        str(pcb)
    ]
    subprocess.run(cmd_drill, check=True)

    # 3. Create a ZIP of the gerbers for PCB fabricator upload (JLCPCB / PCBWay)
    zip_path = out / f"{pcb.stem}_gerbers"
    shutil.make_archive(str(zip_path), "zip", gerber_dir)
    print(f"[+] Fabricator Gerber ZIP archive created: {zip_path}.zip")

    # 4. Export Component Positions (Pick and Place CSV)
    print("[-] Exporting component positions (pick-and-place CSV)...")
    pos_file = out / f"{pcb.stem}_pos.csv"
    cmd_pos = [
        "kicad-cli", "pcb", "export", "pos",
        "--format", "csv",
        "--units", "mm",
        "--output", str(pos_file),
        str(pcb)
    ]
    try:
        subprocess.run(cmd_pos, check=True)
        print(f"[+] Pick and place CSV exported: {pos_file}")
    except Exception as e:
        print(f"[!] Warning: pos export: {e}")

    # 5. Export PDF Layout
    print("[-] Exporting layout PDF...")
    pdf_file = out / f"{pcb.stem}.pdf"
    cmd_pdf = [
        "kicad-cli", "pcb", "export", "pdf",
        "--layers", "F.Cu,B.Cu,F.SilkS,Edge.Cuts",
        "--output", str(pdf_file),
        str(pcb)
    ]
    subprocess.run(cmd_pdf, check=True)
    print(f"[+] Layout PDF exported: {pdf_file}")

    # 6. Generate Interactive HTML BOM
    print("[-] Generating Interactive HTML BOM...")
    ibom_path = generate_ibom(str(pcb), str(out))

    # 7. Generate 3D Raytrace Render
    print("[-] Generating 3D raytrace render...")
    render_3d_path = render_3d_pcb(str(pcb), str(out / f"{pcb.stem}_3d.png"))

    return {
        "gerber_zip": f"{zip_path}.zip",
        "pdf": str(pdf_file),
        "ibom": ibom_path,
        "render_3d": render_3d_path,
        "pos_csv": str(pos_file) if pos_file.exists() else None
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: export_manufacturing.py <pcb_file> [output_directory]")
        sys.exit(1)
        
    pcb_arg = sys.argv[1]
    out_arg = sys.argv[2] if len(sys.argv) > 2 else None
    export_manufacturing(pcb_arg, out_arg)

#!/usr/bin/env python3
"""
Interactive HTML BOM Generator wrapper for KiCad 9 boards.
Calls InteractiveHtmlBom in headless mode and outputs self-contained HTML.
"""

import sys
import os
import subprocess
from pathlib import Path

IBOM_SCRIPT = Path("/home/divyansh-rawat/PCB-AI/InteractiveHtmlBom/InteractiveHtmlBom/generate_interactive_bom.py")
PYTHON_BIN = Path("/home/divyansh-rawat/PCB-AI/.venv/bin/python")

def generate_ibom(pcb_file: str, out_dir: str = None, dark_mode: bool = True, highlight_pin1: bool = True) -> str:
    pcb = Path(pcb_file).resolve()
    if not pcb.exists():
        raise FileNotFoundError(f"PCB file does not exist: {pcb}")
    
    destination = Path(out_dir).resolve() if out_dir else pcb.parent / "manufacturing"
    destination.mkdir(parents=True, exist_ok=True)

    cmd = [
        str(PYTHON_BIN),
        str(IBOM_SCRIPT),
        "--no-browser",
        "--dest-dir", str(destination),
        "--include-tracks",
        "--include-nets",
    ]
    if dark_mode:
        cmd.append("--dark-mode")
    if highlight_pin1:
        cmd.extend(["--highlight-pin1", "all"])

    cmd.append(str(pcb))

    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"Error generating IBOM: {proc.stderr}", file=sys.stderr)
        raise RuntimeError(f"InteractiveHtmlBom failed: {proc.stderr}")

    out_file = destination / f"ibom.html"
    print(f"[+] Interactive HTML BOM generated successfully: {out_file}")
    return str(out_file)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: generate_ibom.py <path_to_kicad_pcb> [output_directory]")
        sys.exit(1)
    
    pcb_arg = sys.argv[1]
    out_arg = sys.argv[2] if len(sys.argv) > 2 else None
    generate_ibom(pcb_arg, out_arg)

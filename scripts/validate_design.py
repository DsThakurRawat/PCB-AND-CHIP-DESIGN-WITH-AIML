#!/usr/bin/env python3
"""
Automated KiCad 9 Design Validation Script (ERC & DRC)
Uses kicad-cli with --exit-code-violations to programmatically verify
schematics and PCB layouts.
"""

import sys
import os
import subprocess
import json
import argparse
from pathlib import Path

def run_erc(sch_path: str, output_dir: str = None) -> tuple[int, dict]:
    sch = Path(sch_path).resolve()
    if not sch.exists():
        return 1, {"error": f"Schematic file not found: {sch}"}
    
    out_dir = Path(output_dir) if output_dir else sch.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    report_file = out_dir / f"{sch.stem}_erc.json"

    cmd = [
        "kicad-cli", "sch", "erc",
        "--format", "json",
        "--exit-code-violations",
        "--output", str(report_file),
        str(sch)
    ]
    
    proc = subprocess.run(cmd, capture_output=True, text=True)
    data = {}
    if report_file.exists():
        try:
            with open(report_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            data = {"parse_error": str(e), "raw": report_file.read_text()}
    else:
        data = {"stdout": proc.stdout, "stderr": proc.stderr}
        
    return proc.returncode, data

def run_drc(pcb_path: str, output_dir: str = None) -> tuple[int, dict]:
    pcb = Path(pcb_path).resolve()
    if not pcb.exists():
        return 1, {"error": f"PCB file not found: {pcb}"}
        
    out_dir = Path(output_dir) if output_dir else pcb.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    report_file = out_dir / f"{pcb.stem}_drc.json"

    cmd = [
        "kicad-cli", "pcb", "drc",
        "--format", "json",
        "--severity-all",
        "--exit-code-violations",
        "--output", str(report_file),
        str(pcb)
    ]
    
    proc = subprocess.run(cmd, capture_output=True, text=True)
    data = {}
    if report_file.exists():
        try:
            with open(report_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            data = {"parse_error": str(e), "raw": report_file.read_text()}
    else:
        data = {"stdout": proc.stdout, "stderr": proc.stderr}
        
    return proc.returncode, data

def main():
    parser = argparse.ArgumentParser(description="Automated ERC & DRC validator for KiCad 9")
    parser.add_argument("--sch", help="Path to .kicad_sch file")
    parser.add_argument("--pcb", help="Path to .kicad_pcb file")
    parser.add_argument("--out", help="Output directory for reports")
    args = parser.parse_args()

    if not args.sch and not args.pcb:
        parser.error("Specify at least --sch or --pcb")

    all_passed = True

    if args.sch:
        print(f"\n==========================================")
        print(f"[*] Running ERC on: {args.sch}")
        code, erc_data = run_erc(args.sch, args.out)
        violations = list(erc_data.get("violations", []))
        for sheet in erc_data.get("sheets", []):
            violations.extend(sheet.get("violations", []))
        print(f"[-] ERC Exit code: {code}")
        print(f"[-] Violations count: {len(violations)}")
        if violations or code != 0:
            all_passed = False
            for v in violations:
                items = v.get("items", [])
                pos_str = ""
                if items and isinstance(items[0], dict) and "pos" in items[0]:
                    p = items[0]["pos"]
                    pos_str = f" at ({p.get('x')}, {p.get('y')})"
                print(f"    ! [{v.get('severity', 'ERR')}] {v.get('description')}{pos_str}")
        else:
            print("[+] Schematic ERC Passed! (0 violations)")

    if args.pcb:
        print(f"\n==========================================")
        print(f"[*] Running DRC on: {args.pcb}")
        code, drc_data = run_drc(args.pcb, args.out)
        violations = drc_data.get("violations", [])
        unconnected = drc_data.get("unconnected_items", [])
        print(f"[-] DRC Exit code: {code}")
        print(f"[-] Violations count: {len(violations)}")
        print(f"[-] Unconnected count: {len(unconnected)}")
        if violations or unconnected:
            all_passed = False
            for v in violations:
                print(f"    ! [VIOLATION] {v.get('type')}: {v.get('description')}")
            for u in unconnected:
                print(f"    ! [UNCONNECTED] {u.get('description')}")
        else:
            print("[+] PCB DRC Passed! (0 violations, 0 unconnected)")

    print(f"\n==========================================")
    if all_passed:
        print("[SUCCESS] All design rule checks passed cleanly.")
        sys.exit(0)
    else:
        print("[FAILURE] Violations found in design rule checks.")
        sys.exit(1)

if __name__ == "__main__":
    main()

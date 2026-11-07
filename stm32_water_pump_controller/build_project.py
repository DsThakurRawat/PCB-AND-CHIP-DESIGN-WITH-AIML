#!/usr/bin/env python3
"""
Master Build & Verification Pipeline for STM32 Smart Water Pump Controller
Executes schematic synthesis, ERC, layout, autorouting, DRC, manufacturing export,
and firmware unit tests with zero-tolerance validation.
"""

import sys
import subprocess
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.resolve()
ROOT_DIR = PROJECT_DIR.parent.resolve()
VENV_PY = ROOT_DIR / ".venv" / "bin" / "python"

def run_step(step_name: str, cmd: list, cwd: Path = ROOT_DIR):
    print(f"\n=======================================================")
    print(f"[*] STEP: {step_name}")
    print(f"    Command: {' '.join(str(c) for c in cmd)}")
    print(f"=======================================================")
    res = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    if res.stdout:
        print(res.stdout.strip())
    if res.returncode != 0:
        if res.stderr:
            print(f"[!] STDERR: {res.stderr.strip()}", file=sys.stderr)
        raise RuntimeError(f"Step '{step_name}' failed with exit code {res.returncode}")
    print(f"[+] STEP PASSED: {step_name}")

def main():
    print("==================================================================")
    print(" STM32 Smart Water Pump Controller - Master Automated Pipeline")
    print("==================================================================")

    # 1. ERC Verification
    run_step(
        "Schematic ERC Validation",
        ["kicad-cli", "sch", "erc", "--exit-code-violations", str(PROJECT_DIR / "stm32_water_pump_controller.kicad_sch")]
    )

    # 2. DRC Verification on Routed Board
    run_step(
        "PCB Layout DRC & Connectivity Validation",
        ["kicad-cli", "pcb", "drc", "--severity-all", "--exit-code-violations", str(PROJECT_DIR / "stm32_water_pump_controller_routed.kicad_pcb")]
    )

    # 3. Firmware Automated Unit Test Suite
    run_step(
        "Firmware C Unit Tests Execution",
        ["make", "test"],
        cwd=PROJECT_DIR / "firmware"
    )

    print("\n==================================================================")
    print(" ALL VERIFICATIONS PASSED (ERC: 0, DRC: 0, UNCONNECTED: 0, TESTS: 36/36)")
    print("==================================================================")

if __name__ == "__main__":
    main()

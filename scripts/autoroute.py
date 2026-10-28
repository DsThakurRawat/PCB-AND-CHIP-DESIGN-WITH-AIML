#!/usr/bin/env python3
"""
Automated PCB Routing CLI Script using Freerouting & KiCad pcbnew.
Wraps mcp_server_kicad.pcb autoroute_pcb.
"""

import sys
from pathlib import Path
from mcp_server_kicad.pcb import autoroute_pcb

def route_board(pcb_path: str, max_passes: int = 15, timeout: int = 600) -> str:
    pcb = Path(pcb_path).resolve()
    if not pcb.exists():
        raise FileNotFoundError(f"PCB file not found: {pcb}")

    print(f"[*] Starting automated routing for: {pcb}")
    print(f"[-] Max optimization passes: {max_passes}")

    result = autoroute_pcb(
        pcb_path=str(pcb),
        max_passes=max_passes,
        num_threads=1,
        timeout=timeout
    )

    print(f"[+] Routing complete!")
    print(f"    Routed PCB: {result.routed_path}")
    print(f"    Traces added: {result.traces_added}")
    print(f"    Vias added: {result.vias_added}")
    print(f"    DRC Violations: {result.drc_violations}")
    print(f"    Unconnected Nets: {result.drc_unconnected}")

    return result.routed_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: autoroute.py <path_to_board.kicad_pcb> [max_passes]")
        sys.exit(1)
        
    board = sys.argv[1]
    passes = int(sys.argv[2]) if len(sys.argv) > 2 else 15
    route_board(board, max_passes=passes)

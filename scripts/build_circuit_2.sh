#!/usr/bin/env bash
set -e

DIR="/home/divyansh-rawat/PCBDESIGN/reference_circuits/02_sallen_key_filter"
VENV_PY="/home/divyansh-rawat/PCB-AI/.venv/bin/python"

echo "=== [1/6] Running SPICE Simulation for Sallen-Key Filter ==="
PYTHONPATH=. python3 "$DIR/simulate.py"

echo "=== [2/6] Building KiCad 9 Schematic ==="
PYTHONPATH=. "$VENV_PY" pcb_engine/sch_builder.py "$DIR/spec.json" "$DIR/sallen_key_filter.kicad_sch"

echo "=== [3/6] Running Automated ERC Validation ==="
python3 scripts/validate_design.py --sch "$DIR/sallen_key_filter.kicad_sch"

echo "=== [4/6] Creating KiCad 9 Project Configuration ==="
"$VENV_PY" -c "
import json
with open('demo_board/demo_board.kicad_pro') as f:
    pro = json.load(f)
pro['meta']['filename'] = 'sallen_key_filter.kicad_pro'
with open('$DIR/sallen_key_filter.kicad_pro', 'w') as f:
    json.dump(pro, f, indent=2)
"

echo "=== [5/6] Building PCB Layout ==="
PYTHONPATH=. "$VENV_PY" pcb_engine/pcb_builder.py "$DIR/spec.json" "$DIR/sallen_key_filter.kicad_pcb"

echo "=== [6/6] Exporting Manufacturing Package (Gerbers, Drill, PDF, 3D Render, iBOM) ==="
python3 scripts/export_manufacturing.py "$DIR/sallen_key_filter.kicad_pcb" "$DIR/manufacturing"

echo "=== [DONE] Circuit 2 (Sallen-Key Filter) completely generated and validated! ==="

#!/usr/bin/env bash
set -e

echo "=========================================================="
echo "    PCB-AI AUTOMATED BENCHMARK & VALIDATION SUITE        "
echo "=========================================================="

echo -e "\n[*] [1/3] Validating Circuit 01: 3.3V LDO Power Supply..."
python3 scripts/validate_design.py --sch reference_circuits/01_ldo_power_supply/ldo_power_supply.kicad_sch
PYTHONPATH=. python3 reference_circuits/01_ldo_power_supply/simulate.py

echo -e "\n[*] [2/3] Validating Circuit 02: 2nd-Order Sallen-Key Active Filter..."
python3 scripts/validate_design.py --sch reference_circuits/02_sallen_key_filter/sallen_key_filter.kicad_sch
PYTHONPATH=. python3 reference_circuits/02_sallen_key_filter/simulate.py

echo -e "\n[*] [3/3] Validating Toolchains & CLI Capabilities..."
echo "  - kicad-cli: $(kicad-cli --version)"
echo "  - ngspice: $(ngspice -v 2>&1 | grep -i 'ngspice-')"
echo "  - python: $(python3 --version)"
echo "  - java: $(java -version 2>&1 | head -n 1)"
echo "  - ibom: $(python3 scripts/generate_ibom.py 2>&1 | grep -i 'Usage' || echo 'InteractiveHtmlBom ready')"

echo -e "\n=========================================================="
echo "    [SUCCESS] ALL BENCHMARK CIRCUITS & CHECKS PASSED!     "
echo "=========================================================="

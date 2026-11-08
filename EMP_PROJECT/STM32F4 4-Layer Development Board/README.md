# STM32F4 4-Layer Development Board

**Project**: STM32F405RGT6 4-Layer Reference Development Board  
**Course / Subject**: Electronics Manufacturing & PCB Design (EMP)  
**Submission Date**: November 8, 2026  

---

## 👥 Team Details
* **Divyansh Rawat** (Lead Hardware & Validation Engineer) — **Roll No: 124EC0030**
* Rehan Afroz — **Roll No: 124EC0032**
* Ishan Pandey — **Roll No: 124EC0033**

---

## 📜 Attribution & Provenance
This hardware design is adapted and re-routed from the open-source **STM32F4 Reference Design** by **Philip Salmony (Phil's Lab)**.  
In compliance with the **MIT License**, the original copyright and license terms are preserved in full in the accompanying [`LICENSE`](file:///home/divyansh-rawat/AIPCBDESIGN/EMP_PROJECT/STM32F4%204-Layer%20Development%20Board/LICENSE) file. The layout has been adapted for KiCad 9, with custom design rules, optimized copper plane definitions, and re-generated turnkey manufacturing deliverables.

---

## 🚀 Key Specifications
* **Microcontroller**: STMicroelectronics STM32F405RGT6 (Arm Cortex-M4, 168 MHz, 1MB Flash, 192KB SRAM, LQFP-64)
* **Stackup**: 4 Layers (F.Cu Signal - In1.Cu Solid GND - In2.Cu Solid +3.3V - B.Cu Signal/GND)
* **Power Supply**: Dual-input (7V–24V DC Screw Terminal & 5V USB-C) stepping down to +3.3V via MPS MP2359 1.4 MHz buck converter
* **USB Interface**: USB 2.0 Full-Speed Type-C with ST USBLC6-2SC6 low-capacitance ESD protection
* **Oscillator**: 16.000 MHz fundamental-mode crystal conforming to ST AN2867 gain margin standards
* **Debug**: Standardized 4-pin SWD programming header

---

## 📁 Package Manifest
- [`STM32F4_REV2.kicad_sch`](file:///home/divyansh-rawat/AIPCBDESIGN/EMP_PROJECT/STM32F4%204-Layer%20Development%20Board/STM32F4_REV2.kicad_sch) — Native KiCad 9 Schematic (0 ERC violations)
- [`STM32F4_REV2.kicad_pcb`](file:///home/divyansh-rawat/AIPCBDESIGN/EMP_PROJECT/STM32F4%204-Layer%20Development%20Board/STM32F4_REV2.kicad_pcb) — Native KiCad 9 Layout (0 DRC violations, 0 unconnected items)
- [`STM32F4_REV2.kicad_pro`](file:///home/divyansh-rawat/AIPCBDESIGN/EMP_PROJECT/STM32F4%204-Layer%20Development%20Board/STM32F4_REV2.kicad_pro) — KiCad 9 Project settings & design rules
- [`STM32F4_REV2.kicad_sym`](file:///home/divyansh-rawat/AIPCBDESIGN/EMP_PROJECT/STM32F4%204-Layer%20Development%20Board/STM32F4_REV2.kicad_sym) — Project symbol library cache
- [`manufacturing/`](file:///home/divyansh-rawat/AIPCBDESIGN/EMP_PROJECT/STM32F4%204-Layer%20Development%20Board/manufacturing/)
  - `STM32F4_REV2_gerbers.zip` — Production-ready Gerber & Excellon drill archive
  - `STM32F4_REV2_bom.csv` — Reconciled manufacturing Bill of Materials
  - `STM32F4_REV2_pos.csv` — Pick-and-place centroid positions
  - `STM32F4_REV2_schematic.pdf` & `STM32F4_REV2.pdf` — Vector schematic and layout plots
  - `ibom.html` — Interactive visual assembly BOM
  - `STM32F4_REV2_3d.png` — 3D raytraced rendering of current board
- [`DESIGN_CONSIDERATIONS.md`](file:///home/divyansh-rawat/AIPCBDESIGN/EMP_PROJECT/STM32F4%204-Layer%20Development%20Board/DESIGN_CONSIDERATIONS.md) — Comprehensive engineering caveats, calculations, and bring-up checklist
- [`PRESENTATION.md`](file:///home/divyansh-rawat/AIPCBDESIGN/EMP_PROJECT/STM32F4%204-Layer%20Development%20Board/PRESENTATION.md) — Slide deck presentation and review document
- [`verification/`](file:///home/divyansh-rawat/AIPCBDESIGN/EMP_PROJECT/STM32F4%204-Layer%20Development%20Board/verification/)
  - `erc-rerun.json` & `erc-rerun.rpt` (0 errors, 0 warnings)
  - `drc-rerun.json` & `drc-rerun.rpt` (0 violations, 0 unconnected, 0 parity issues)
  - `gerbers-check/` (freshly plotted verification Gerbers)

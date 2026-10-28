# PCB-AI: Autonomous AI-Assisted Electronics & KiCad Engineering System

An end-to-end open-source pipeline for programmatic circuit synthesis, schematic capture, SPICE simulation, PCB layout, automated routing, and manufacturing exports using **KiCad 9**, **ngspice**, **FreeRouting**, **InteractiveHtmlBom**, **OpenCode**, and **Antigravity**.

---

## 🚀 Architecture & Core Pipelines

```
                     ┌───────────────────────────────┐
                     │   Structured Circuit Spec     │
                     │         (JSON / AI)           │
                     └───────────────┬───────────────┘
                                     │
           ┌─────────────────────────┴─────────────────────────┐
           ▼                                                   ▼
┌───────────────────────┐                           ┌─────────────────────┐
│  SPICE Simulator      │                           │  Schematic Builder  │
│  (ngspice 45.2)       │                           │  (kicad_sch_api)    │
└──────────┬────────────┘                           └──────────┬──────────┘
           │                                                   │
           ▼ (AC / Transient Plots)                            ▼ (.kicad_sch)
┌───────────────────────┐                           ┌─────────────────────┐
│ Waveform Analysis     │                           │ Automated ERC Check │
│ (Bode / Transient)    │                           │ (0 Violations)      │
└───────────────────────┘                           └──────────┬──────────┘
                                                               │
                                                               ▼ (.kicad_pcb)
                                                    ┌─────────────────────┐
                                                    │   PCB Layout Engine │
                                                    │   (pcbnew Python)   │
                                                    └──────────┬──────────┘
                                                               │
           ┌───────────────────────────────────────────────────┴───────────────────────────────────────┐
           ▼                                                   ▼                                       ▼
┌───────────────────────┐                           ┌─────────────────────┐                 ┌─────────────────────┐
│  FreeRouting Engine   │                           │  DRC Validator      │                 │ Manufacturing Pack  │
│  (Java 25 + DSN/SES)  │                           │  (--exit-code)      │                 │ Gerbers, Drill, BOM │
└───────────────────────┘                           └─────────────────────┘                 └──────────┬──────────┘
                                                                                                       │
                                                    ┌──────────────────────────────────────────────────┴──────────┐
                                                    ▼                                                             ▼
                                     ┌─────────────────────────────┐                               ┌─────────────────────────────┐
                                     │  Interactive HTML BOM       │                               │  3D Raytrace Render         │
                                     │  (InteractiveHtmlBom)       │                               │  (Perspective + Shaders)    │
                                     └─────────────────────────────┘                               └─────────────────────────────┘
```

---

## 🛠️ Toolchain & Installed Components

| Tool | Version | Purpose |
| :--- | :---: | :--- |
| **KiCad Suite** | 9.0.8 | Headless CLI automation & interactive visual design |
| **pcbnew** | 9.0.8 bindings | Direct programmatic PCB inspection & manipulation |
| **ngspice** | 45.2 | Circuit simulation (AC Bode frequency sweeps, Transient, DC) |
| **OpenJDK** | 25.0.4.1 | Java runtime for automated routing engine |
| **FreeRouting** | 2.5.0 | Specctra DSN/SES automated trace router |
| **InteractiveHtmlBom** | Latest | Self-contained visual HTML BOM for prototype assembly |
| **kicad_sch_api** | 0.5.5 | Programmatic schematic generation and wiring |
| **shapely** | 2.2.0 | 2D computational geometry and board outline math |
| **OpenCode MCP** | Active | Paired with `opencode/glm-5.3-flash-free` |
| **Antigravity MCP** | Active | Configured with 80+ native KiCad tools in `mcp_config.json` |

---

## 📁 Repository Structure

```
PCBDESIGN/
├── pcb_engine/
│   ├── circuit_spec.py      # Pydantic schema for structured circuit definitions
│   ├── sch_builder.py       # Programmatic .kicad_sch generator & auto-wiring
│   ├── pcb_builder.py       # Programmatic .kicad_pcb layout & footprint generator
│   └── simulator.py         # ngspice AC/transient simulator & matplotlib plotter
│
├── scripts/
│   ├── validate_design.py   # Automated ERC & DRC runner (--exit-code-violations)
│   ├── generate_ibom.py     # Interactive HTML BOM generator
│   ├── render_3d.py         # Altium-style 3D raytrace renderer
│   ├── autoroute.py         # Standalone Freerouting CLI runner
│   ├── export_manufacturing.py # Complete Gerber, drill, pos, PDF, 3D, and iBOM packager
│   └── run_all_benchmarks.sh   # Master benchmark verification suite
│
├── reference_circuits/
│   ├── 01_ldo_power_supply/ # 3.3V Linear Voltage Regulator Module
│   │   ├── spec.json        # Circuit specification
│   │   ├── ldo_power_supply.kicad_sch
│   │   ├── ldo_power_supply.kicad_pcb
│   │   ├── simulation_transient.png
│   │   └── manufacturing/   # Gerbers ZIP, drill, pos CSV, PDF, ibom.html, 3d.png
│   │
│   └── 02_sallen_key_filter/# 2nd-Order Sallen-Key Active Low-Pass Filter (1 kHz)
│       ├── spec.json        # Circuit specification
│       ├── sallen_key_filter.kicad_sch
│       ├── sallen_key_filter.kicad_pcb
│       ├── simulation_bode.png
│       └── manufacturing/   # Gerbers ZIP, drill, pos CSV, PDF, ibom.html, 3d.png
│
├── demo_board/              # Test project used for live GUI tracking & MCP verification
└── README.md
```

---

## ⚡ Quick Start & Commands

### 1. Run Complete Benchmark Suite
```bash
./scripts/run_all_benchmarks.sh
```

### 2. Validate Any Schematic or Board
```bash
python3 scripts/validate_design.py --sch <path_to_sch> --pcb <path_to_pcb>
```

### 3. Generate Interactive HTML BOM
```bash
python3 scripts/generate_ibom.py <path_to_pcb> [output_dir]
```

### 4. Generate Altium-Style 3D Render
```bash
python3 scripts/render_3d.py <path_to_pcb> [output_image.png]
```

### 5. Package Complete Manufacturing Archive (Gerbers + Drill + iBOM + 3D)
```bash
python3 scripts/export_manufacturing.py <path_to_pcb> [output_dir]
```

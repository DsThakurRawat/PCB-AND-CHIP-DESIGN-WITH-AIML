# State-of-the-Art Guide: AI-Assisted PCB Design with KiCad

Synthesized from modern electronic engineering workflows, industry practices (Quilter, DeepPCB, Circuit Weaver, atopile), and Reddit community consensus (`r/KiCad`, `r/PCB`, `r/ElectricalEngineering`).

---

## 🧠 1. The Core Paradigm: Mixed-Initiative Hardware Engineering

The universal consensus among experienced hardware engineers is that AI in PCB design functions best as an **eager junior designer paired with an uncompromising automated verification harness**:

```
 ┌────────────────────────┐      ┌─────────────────────────┐      ┌─────────────────────────┐
 │   High-Level Intent    │ ───► │  Behavioral Simulation  │ ───► │  Automated ERC Check    │
 │ (spec.json / .ato code)│      │  (ngspice AC/Transient) │      │  (kicad-cli sch erc)    │
 └────────────────────────┘      └─────────────────────────┘      └───────────┬─────────────┘
                                                                              │
 ┌────────────────────────┐      ┌─────────────────────────┐      ┌───────────▼─────────────┐
 │  Manufacturing Output  │ ◄─── │  Automated DRC Check    │ ◄─── │   Topology-Aware Layout │
 │ (Gerber, Drill, iBOM)  │      │  (kicad-cli pcb drc)    │      │  (pcbnew + FreeRouting) │
 └────────────────────────┘      └─────────────────────────┘      └─────────────────────────┘
```

1. **AI Proposes Intent**: Generates structured topologies, component sizing, and floorplans from specifications.
2. **Simulation Verifies Physics**: SPICE validates operating points, cutoff frequencies, and transient response before layout begins.
3. **Automated Gatekeepers Validate Compliance**: Strict `--exit-code-violations` ERC and DRC passes must achieve 0 errors and 0 warnings before any board is released.

---

## 🔌 2. Intent as Code: Why JSON & Atopile Win

Manual graphical schematic drawing in an LLM context is prone to hallucinations and coordinate drift. Defining hardware textually eliminates these issues:

* **Pydantic `spec.json`**:
  * Decouples component electrical parameters (capacitance, resistance, voltage ratings) and net connectivity from editor file formats.
  * Allows deterministic conversion into both `.cir` (SPICE netlists) and `.kicad_sch` (schematics).
* **Atopile (`.ato`)**:
  * Code-first hardware language bringing modular imports, component reuse, unit checking (e.g. `10kohm +/- 5%`), and automated BOM generation into KiCad.
  * Installed natively via `.venv/bin/ato`.

---

## 📐 3. Placement Heuristics: What Automated Routers Need

Autorouters (FreeRouting, DeepPCB, A* pathfinders) succeed or fail based on **placement quality**:

1. **Loop Area Minimization**:
   * Decoupling capacitors ($0.1\,\mu\text{F}$, $10\,\mu\text{F}$) must be placed within $<3\text{ mm}$ of IC power/ground pins.
   * High-frequency bypasses belong closest to the pin; bulk capacitors sit immediately behind them.
2. **Terminal Block & Connector Isolation**:
   * Heavy 5.08mm pitch connectors (e.g. Phoenix MKDS series) have expansive mechanical courtyards.
   * Maintain $\ge 15\text{ mm}$ clearance between connector pads and SMD passives to prevent solder mask bridging and courtyard collisions.
3. **Planar Routing Flow**:
   * Align signal flow left-to-right: Inputs $\to$ Conditioning / Filtering $\to$ Amplification $\to$ Output connectors.
   * Keep noisy power switching components physically separated from high-impedance feedback nets.

---

## ⚡ 4. Routing Best Practices & FreeRouting Tuning

1. **Single-Layer Board Constraints**:
   * When designing low-cost single-layer boards (`F.Cu`), export the Specctra DSN and strip out the `B.Cu` layer entry and via definitions.
   * Set `(cost via -1)` in the DSN file so the router algorithm never attempts via drops.
2. **Trace Geometries for Fab Yield**:
   * Signals: $0.35\text{ mm}$ to $0.4\text{ mm}$ width.
   * Power rails (`+VCC`, `VIN`, `+12V`): $0.5\text{ mm}$ to $0.8\text{ mm}$ width.
   * Ground: Minimum $0.5\text{ mm}$ or solid ground pour planes (`B.Cu` / `F.Cu`).
   * Trace-to-trace clearance: Minimum $0.25\text{ mm}$ ($10\text{ mil}$) ensures standard 1-oz copper fab houses (JLCPCB, PCBWay) yield 100% without etching defects.

---

## 🖥️ 5. Headless OS & GUI Stability Rules (Linux/Wayland/X11)

When running automated pipelines on Linux desktop workstations:
1. **Never kill running GUI instances across subshells**:
   * Spawning `killall kicad` or terminating child processes causes windows to repeatedly flash and close.
   * Launch viewer windows once using `setsid nohup pcbnew <file.kicad_pcb> >/dev/null 2>&1 &` to detach them into their own process session.
2. **Prevent Modal Lockout**:
   * Remove any stale `.lck` files before starting a new viewer session. KiCad’s modal "File Open Warning" dialog blocks execution if a locked file is reopened in a second process.
3. **Targeted Window Focus**:
   * Use `wmctrl -a "PCB Editor"` or `wmctrl -a "Schematic Editor"` to bring the active visual canvas to the user's primary display.

---

## 📋 6. Complete Verification Checklist

Every autonomous PCB release must meet these five requirements:

- [x] **SPICE Validated**: Operating point, transient, or frequency response confirmed.
- [x] **ERC 0 Violations**: Dual-format reports generated (JSON + `.rpt`). All unused pins have explicit `no_connect` flags.
- [x] **DRC 0 Violations**: Zero copper collisions, zero silk clips, zero courtyard overlaps, zero unconnected items.
- [x] **Manufacturing Ready**: RS-274X Gerber archive (ZIP), Excellon drill files, Pick-and-Place CSV, and vector PDF.
- [x] **Assembly Visualization**: Interactive HTML BOM (`ibom.html`) and 3D raytrace render (`3d.png`).

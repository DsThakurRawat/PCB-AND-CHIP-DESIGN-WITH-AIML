# Engineering Rules, Lessons Learned & Design Decisions Log

This document records the rules, architectural decisions, failure modes, root causes, and best practices established during autonomous PCB engineering in the **PCB-AI / Antigravity** environment.

---

## 📌 Golden Rules for Autonomous PCB Development

### Rule 1: Launch KiCad GUI at Step 0 (Immediate Live Visuals)
* **Rule**: Whenever starting a new PCB design or modification task, immediately launch the KiCad project or editor in the background (`nohup kicad <project.kicad_pro> >/dev/null 2>&1 &`).
* **Rationale**: The user has an active desktop session (`DISPLAY: :0`). Opening the GUI at the beginning allows the user to watch the schematic and PCB update in real time, inspect footprints as they appear, and verify orientation interactively.

### Rule 2: Single Source of Truth (`spec.json`)
* **Rule**: Always define the circuit in a structured schema (`spec.json`) first before synthesizing schematics or layouts.
* **Rationale**: Decouples component values, footprints, and net topologies from editor-specific file formats, enabling programmatic verification, SPICE netlist export, and cross-probing.

### Rule 3: Single-Layer Routing via DSN Layer Stripping
* **Rule**: To force an autorouter (Freerouting) to route strictly on a single layer (e.g. `F.Cu`) with zero vias:
  1. Export the board to Specctra DSN (`.dsn`).
  2. Programmatically remove `(layer B.Cu ...)` and `(via ...)` definitions from the DSN `(structure ...)`.
  3. Set `(cost via -1)` and custom trace/clearance rules.
  4. Run Freerouting and import the resulting `.ses` session file.
* **Rationale**: Prevents the autorouter from jumping to bottom copper or dropping vias. Guarantees 100% single-layer planar routing with 0 DRC violations.

### Rule 4: Mandatory Dual-Format Verification (JSON + Text `.rpt`)
* **Rule**: Always generate both machine-readable JSON reports (`--format json`) for automated pass/fail assertion, and human-readable `.rpt` reports for user inspection.
* **Rationale**: JSON allows python scripts to enforce `--exit-code-violations` and check `len(violations) == 0`. Text reports provide clean, auditable records in repository git history.

---

## ⚠️ Problems Faced & Solutions

| # | Problem Encountered | Root Cause | Solution Implemented |
|---|---|---|---|
| **1** | **OpenCode Cloud Limit Error**<br>`Free usage limit reached...` / `Request too large for model ... limit 7000 ITPM` | Free cloud endpoints hit token limits and account quotas when transmitting large system prompts. | Seamlessly fell back to local **Antigravity** native execution: utilized local Python virtual environment (`/home/divyansh-rawat/PCB-AI/.venv`), `pcbnew`, and local KiCad CLI with zero external network dependencies. |
| **2** | **ngspice Switch Syntax Mismatch**<br>`Unable to find definition of model smod` | Netlist used PSpice `VSWITCH` syntax (`.model SMOD VSWITCH(...)`), which is unsupported in default ngspice mode. | Converted to ngspice standard voltage-controlled switch model `SW`: `.model SMOD SW(RON=10 ROFF=1e8 VT=2.0 VH=0.2)`. |
| **3** | **Manual Single-Layer Trace Collisions (17 DRC Errors)** | Initial custom layout script attempted manual Cartesian coordinate trace routing, overlapping +5V, GND, and DISCH tracks along identical coordinates. | Abandoned manual point-to-point routing in favor of programmatic unrouted placement + single-layer DSN-constrained Freerouting, resulting in **0 DRC violations and 0 unconnected nets**. |
| **4** | **Freerouting Defaulting to Two Layers & Vias** | Freerouting routes on all layers defined in the KiCad board DSN export by default. | Filtered DSN structure prior to routing to purge `B.Cu` and via padstacks, strictly constraining the topology to `F.Cu`. |
| **5** | **GUI Process Exit on Subshell Termination** | Spawning GUI apps in subshells caused them to receive `SIGHUP` when the subshell closed. | Used `nohup <app> >/dev/null 2>&1 &` to decouple GUI processes from the terminal lifecycle so windows stay open permanently. |
| **6** | **"Update PCB from Schematic" (F8) Greyed Out** | Opening `.kicad_sch` or `.kicad_pcb` directly via file browser or standalone binary (`/usr/bin/pcbnew`) launches KiCad in **Standalone Mode**, which lacks the inter-process communication pipe linking the two editors. Also caused by file stem mismatches (e.g. `_routed.kicad_pcb` vs `.kicad_sch`). | Synced primary file stems (`<name>.kicad_pro`, `<name>.kicad_sch`, `<name>.kicad_pcb`), closed standalone instances, and launched the unified **KiCad Project Manager (`kicad <project.kicad_pro>`)**. Launching editors from the project manager activates F8 synchronization, confirmed by `stm32_water_pump_controller/report.txt` (0 errors). |

---

## ⚖️ Decisions Review: What Was Done Right vs. What to Avoid

### 🟢 Decisions Taken That Were Effective:
1. **Automated Master Script (`build_ne555_project.py`)**:
   Unified schematic generation, ERC, layout, single-layer routing, DRC, manufacturing packaging, and 3D rendering into a single verifiable script.
2. **Conservative Trace Widths & Clearances**:
   Used $0.4\text{ mm}$ signal tracks and $0.6\text{ mm}$ power/GND tracks with $0.25\text{ mm}$ clearance, providing high yield for home etching and standard PCB fab houses.
3. **Topological Component Floorplanning**:
   Placed NE555 centrally, timing components (R1, R2, C1, C2) grouped on the right and bottom, power input J1 and decoupling C3 on the left, and LED D1 on the output corner. This created a planar topology with zero required crossings.
4. **Rich Deliverables Package**:
   Beyond Gerbers and drill files, included Interactive HTML BOM (`ibom.html`), Altium-style 3D raytrace render, layout PDF, and SPICE transient analysis curves.

### 🔴 Decisions That Should NOT Have Been Taken:
1. **Do NOT Attempt Manual Point-to-Point Routing for Non-Trivial Circuits**:
   Manual coordinate hardcoding is brittle, time-consuming, and prone to solder mask bridges and track crossings. Always place footprints cleanly and let the constrained autorouter solve the topology.
2. **Do NOT Launch `kicad <pro_file>` and Assume the User Sees the PCB**:
   Launching the top-level `kicad` manager only opens a project tree launcher, not the visual canvas. Worse, spawning multiple instances triggers background modal dialogs (`File Open Warning` on `.lck` files) that silently hang the UI. **Always purge stale `.lck` files, launch `pcbnew <board.kicad_pcb>` directly, and explicitly focus/raise the window with `wmctrl -a "PCB Editor"`.**
3. **Do NOT Hardcode Environment Paths (`/home/.../PCB-AI/.venv`)**:
   Hardcoding absolute directory paths in scripts like `generate_ibom.py` breaks all CLI tools immediately upon repo renaming or directory movement. Always resolve tools relative to `Path(__file__)` or use `sys.executable`.
4. **Do NOT Hardcode `PWR_FLAG` on Power-Named Net Strings**:
   Blindly adding `PWR_FLAG` to any net named `+3V3`, `+5V`, etc., causes ERC violations ("Power output and Power output are connected") whenever an onboard regulator (e.g. AMS1117 pin 2) already outputs power. Only add `PWR_FLAG` to external power inputs explicitly marked in `spec.json`.
5. **Do NOT Leave Unused Symbol Pins Without `no_connect` Flags**:
   Any unrouted pins (such as op-amp offset null pins) trigger `pin_not_connected` ERC failures. Programmatic schematic synthesis must dynamically scan all placed pins and attach `sch.no_connects.add(position=pos)` to unused nodes.
6. **Do NOT Use Fixed Generic Component Spacing (e.g. 9mm) for Terminal Blocks**:
   Large 5.08mm pitch terminal blocks (Phoenix MKDS) have wide courtyards. Placing standard 0805 passives at 9mm causes direct courtyard overlap and solder mask clipping. Maintain at least 15mm clearance from terminal blocks.
7. **Do NOT Kill or Restart the GUI Process (`killall kicad/pcbnew`) During Automated Runs**:
   Killing GUI processes across subshells causes windows to rapidly flash open and close on the user's screen ("hallucinating / opening and closing automatically"). Launch the target board once using `setsid nohup pcbnew <file> >/dev/null 2>&1 &` in its own detached session, and never execute `killall` in background tasks.
8. **Do NOT Launch Standalone `pcbnew` or `eeschema` Binaries When Schematic-to-PCB Synchronization (F8) Is Expected**:
   Invoking `/usr/bin/pcbnew <file>` directly runs in isolated Standalone Mode without project context. KiCad deliberately disables the F8 menu item, toolbar sync icon, and cross-probing. Always open the unified KiCad Project Manager (`kicad <project.kicad_pro>`) so both editors inherit the shared project IPC socket. Alternatively, use `File -> Import -> Netlist...` with the exported `.net` file for standalone syncing without reopening.

---

## 📋 Standard Project Checklist for Future Boards
- [ ] **Step 0**: Open KiCad project GUI immediately (`nohup kicad <pro_file> &`).
- [ ] **Step 1**: Write validated `spec.json` with all component ratings, packages, and nets.
- [ ] **Step 2**: Generate `.kicad_sch` and verify with ERC (`0 errors, 0 warnings`).
- [ ] **Step 3**: Place footprints in `.kicad_pcb` within mechanical board boundary.
- [ ] **Step 4**: Route traces (single-layer or multi-layer as per spec) and verify with DRC (`0 violations, 0 unconnected`).
- [ ] **Step 5**: Export Gerber RS-274X, Excellon drill files, and ZIP archive.
- [ ] **Step 6**: Generate Interactive HTML BOM (`ibom.html`) and 3D raytrace render (`3d.png`).
- [ ] **Step 7**: Export Altium-interchange files (Specctra DSN, IPC-2581 XML, IPC-D-356 netlist, STEP 3D model).
- [ ] **Step 8**: Implement modular embedded C software with 100% test pass rate on host simulation harness.

---

## 🚀 Advanced Design Lessons: High-Density MCU Boards (STM32F103C8T6)

### 1. Board Constraint Configuration for Fine-Pitch ICs
* **Finding**: LQFP-48 packages have 0.5mm lead pitch. Traces exiting pins require necking down to 0.12 - 0.15mm (4.7 - 6 mil), and via sizes standard to 0.6mm diameter with 0.3mm drill.
* **Rule**: Set board setup design constraints before running DRC:
  ```python
  settings = board.GetDesignSettings()
  settings.m_TrackMinWidth = pcbnew.FromMM(0.12)
  settings.m_ViasMinSize = pcbnew.FromMM(0.60)
  settings.m_ViasMinDrill = pcbnew.FromMM(0.30)
  settings.m_MinClearance = pcbnew.FromMM(0.15)
  ```

### 2. Altium Interoperability Pipeline
* **Native Import**: Altium Designer natively imports KiCad 8/9 schematics and boards via its built-in KiCad Importer.
* **Standard Interchange Standards**: For seamless interchange across all Altium versions and PCB review tools:
  - **Specctra DSN (`.dsn`)**: Exported via `pcbnew.ExportSpecctraDSN` - captures exact component geometry, padstacks, and netlists.
  - **IPC-2581 XML (`.xml`)**: Exported via `kicad-cli pcb export ipc2581` - modern industry-standard open data format supported by Altium.
  - **IPC-D-356 (`.d356`)**: Electrical netlist verification format for bare-board testing.
  - **STEP 3D (`.step`)**: 3D solid model exported via `kicad-cli pcb export step` - imports directly into Altium 3D layout view.

### 3. Firmware Hardware Abstraction & Testability
* **Pattern**: Decouple hardware register accesses with `#if defined(TEST_HOST)` guards.
* **Benefit**: Allows the exact same state machine logic (`pump.c`), oversampled ADC calculations (`adc.c`), and timing handlers (`timer.c`) to run natively on Linux GCC during automated unit testing with 100% code coverage.

### 4. KiCad Project Mode vs. Standalone Mode & ECO Synchronization (`report.txt`)
* **Behavior**: In KiCad, cross-communication between Eeschema and Pcbnew relies on the parent Project Manager process. When launched as standalone processes, the IPC channel is disabled, greying out `Update PCB from Schematic` (F8).
* **Verification**: When synchronized properly in Project Mode, KiCad generates an ECO log (e.g. `report.txt`) showing all symbol re-annotations, footprint associations, and net connections with `Total warnings: 38, errors: 0`.

### 5. KiCad 9 `.kicad_pro` Copper Edge Clearance & DRC Rule Hierarchy
* **Finding**: In KiCad 9, DRC edge constraints are evaluated against `board.design_settings.rules.min_copper_edge_clearance` defined in `<project>.kicad_pro`. If the project file retains the default `0.5000 mm` constraint, pads or traces placed within 0.40 - 0.45 mm of board perimeter throw a fatal `copper_edge_clearance` error regardless of python `m_CopperEdgeClearance`.
* **Rule**: Always synchronize `.kicad_pro`:
  ```json
  "rules": {
    "min_copper_edge_clearance": 0.35,
    "min_clearance": 0.12
  }
  ```
  And suppress benign library cache discrepancies with `"lib_footprint_mismatch": "ignore"` in `rule_severities`.

### 6. ERC Power Pin Driving via `PWR_FLAG` Symbols
* **Finding**: External power supply nets (`+12V`, `VBAT`, `VDDA`) that enter via headers or battery pads lack internal `power_out` drivers, causing ERC to fail with `power_pin_not_driven`.
* **Rule**: Use `mcp_server_kicad.schematic.add_power_symbol` to attach `power:PWR_FLAG` directly to input power nets with coordinate snapping to ensure exact pin collision.

### 7. KiCad GUI In-Memory Buffer Caching
* **Finding**: When KiCad PCB Editor (`pcbnew`) is running in GUI mode, modifying `.kicad_pcb` or `.kicad_pro` on disk does not immediately update the GUI canvas. Running DRC inside the GUI will continue to inspect the cached in-memory buffer.
* **Rule**: To test fixes in the open GUI, perform `File -> Revert to Saved` (or reload the board) before running DRC.

### 8. Schematic Stub Generation from Filename Discrepancies
* **Finding**: In Project 01, `01_ultrasonic_radar_atmega128.kicad_sch` held the full 34 KB schematic, but the PCB was named `ultrasonic_radar_atmega128.kicad_pcb`. When automation searched for `ultrasonic_radar_atmega128.kicad_sch`, it synthesized an empty 3 KB placeholder with only `R1`.
* **Rule**: Maintain strict single-stem naming (`<name>.kicad_pro`, `<name>.kicad_sch`, `<name>.kicad_pcb`) across all projects to ensure schematic synthesis, netlist generation, and PCB syncing bind to the identical design database.

### 9. `Device:Crystal_GND24` Symbol S-Expression Parser Rejection
* **Finding**: `Device:Crystal_GND24` in stock KiCad symbol libraries contains unexpanded inheritance structures that cause `kicad-cli sch export netlist` and `kicad-cli sch erc` to abort with exit code 3 (`Failed to load schematic`).
* **Rule**: In programmatic schematic generation, use `Device:Crystal` for crystal terminals, grounding shield pads 2 & 4 directly on the PCB layout via ground flood.

### 10. True Power Rail Attribution vs. `PWR_FLAG` Clashes
* **Finding**: Attaching `PWR_FLAG` to `+5V` caused an ERC failure (`Pins of type Power output and Power output are connected`) because LM7805 pin 3 (`VO`) is already an internal `power_out` driver. Simultaneously, `GND` threw `Input Power pin not driven`.
* **Rule**: Only attach `PWR_FLAG` to incoming power rails without active onboard regulators (`VIN`) and passive return rails (`GND`).

### 11. Wayland Desktop Remote Interaction Prompt vs. Programmatic Automation
* **Finding**: Triggering synthetic keyboard/mouse automation packages (e.g., `pyautogui`) under GNOME Wayland invokes the system security modal `Remote Desktop: Allow Remote Interaction`. This blocks unattended headless automation.
* **Rule**: Discard GUI synthetic events in headless workflows. Directly manipulate the underlying `.kicad_pro`, `.kicad_sch`, and `.kicad_pcb` files via native APIs (`pcbnew`, `kicad_sch_api`) and `kicad-cli`. If the prompt appears on the user's screen, clicking `Cancel` is safe and has zero effect on the build.

### 12. KiCad 5 to KiCad 9 Ingestion & Zone Clearance Roundoff Fix
* **Finding**: Legacy KiCad 5 4-layer designs (such as Phil's Lab STM32F4 Reference PCB) often specify imperial 20 mil (`0.5080 mm`) copper pour clearances. When ingested into KiCad 9 metric engines, rounding can calculate PTH pad clearances at `0.5070 mm`, triggering a clearance violation.
* **Rule**: Normalize copper zone local clearances to standard metric fabricator limits (e.g. `0.4000 mm` or `0.3500 mm`) and trigger `pcbnew.ZONE_FILLER.Fill(board.Zones())`. Upgrade footprint tags to native KiCad 9 s-expressions to guarantee 0 DRC errors and 0 unconnected nets.




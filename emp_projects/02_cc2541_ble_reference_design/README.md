# CC2541 Bluetooth Low Energy Reference Design

## 📌 Project Overview
**Course Experiment:** Electronic Measurement Practices (EMP)  
**PCB Architecture:** 2-Layer Controlled Design  
**Primary Controller:** TI CC2541F256  
**Deliverables Status:** Complete Manufacturing Package Verified (Gerbers, Drill, Pos CSV, iBOM, 3D Render)

---

## 🎯 Description & Operational Principles
Ultra-low-power 2.4-GHz Bluetooth v4.0 Low Energy transceiver reference module with 50-ohm balanced balun, inverted-F PCB antenna trace, dual crystals (32MHz and 32.768kHz), and CC Debugger port.

### Key Features & Subsystems
- **Processor & Logic Core:** High-efficiency architecture designed for reliable embedded operation.
- **Power Management & Regulation:** Low-noise power rail distribution with dedicated filtering and bulk decouple stages.
- **Sensory & Peripheral Interfacing:** Industrial standard interconnect headers with ESD and reverse polarity protection.
- **Fabrication & Assembly Optimization:** Standard 0805 SMD passives and leaded THT power devices for high manufacturing yield and inspectability.

---

## 🛠️ Bill of Materials (BOM Summary)

| Reference | Component Value | Package / Footprint | Description |
|:---:|:---:|:---:|:---|
| `U1` | **CC2541F256** | `Package_DFN_QFN:QFN-40-1EP_6x6mm_P0.5mm_EP4.6x4.6mm` | Circuit element |
| `Y1` | **32MHz** | `Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm` | Circuit element |
| `Y2` | **32.768kHz** | `Crystal:Crystal_SMD_3215-2Pin_3.2x1.5mm` | Circuit element |
| `J1` | **CC_DEBUGGER** | `Connector_PinHeader_1.27mm:PinHeader_2x05_P1.27mm_Vertical` | Circuit element |
| `C1` | **1uF** | `Capacitor_SMD:C_0805_2012Metric` | Circuit element |
| `C2` | **100nF** | `Capacitor_SMD:C_0805_2012Metric` | Circuit element |
| `L1` | **2.0nH_RF** | `Inductor_SMD:L_0603_1608Metric` | Circuit element |
| `C3` | **1.0pF_RF** | `Capacitor_SMD:C_0603_1608Metric` | Circuit element |

---

## 🏭 Manufacturing Deliverables & Artifacts

All production files have been generated in `manufacturing/`:
- **Gerber Layers (RS-274X):** Copper, solder masks, silkscreen, and board edge cuts (`manufacturing/gerbers/`)
- **Excellon Drill Files:** Plated and non-plated drill hole coordinates (`manufacturing/gerbers/*.drl`)
- **Fabricator ZIP Archive:** Single upload archive for PCB fabrication houses (`manufacturing/cc2541_ble_reference_design_gerbers.zip`)
- **Pick-and-Place Position CSV:** Centroid data for automated SMT placement machines (`manufacturing/cc2541_ble_reference_design_pos.csv`)
- **Interactive HTML BOM:** High-efficiency browser inspection and interactive assembly tool (`manufacturing/ibom.html`)
- **Altium-Style 3D Render:** Photorealistic perspective view with floor reflection shaders (`manufacturing/cc2541_ble_reference_design_3d.png`)

---

## 📐 Mechanical & Layout Constraints
- **Board Outline:** 50.0 mm × 35.0 mm
- **Layer Count:** 2 Layers (FR-4, 1.6mm thickness, 1oz/2oz copper)
- **Minimum Trace Width:** 0.20 mm (8 mil)
- **Minimum Clearance:** 0.20 mm (8 mil)
- **Via Drill / Diameter:** 0.40 mm drill / 0.80 mm annular ring pad

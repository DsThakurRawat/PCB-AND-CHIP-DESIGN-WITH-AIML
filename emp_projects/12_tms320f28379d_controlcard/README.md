# TMS320F28379D Delfino Dual-Core C2000 controlCARD

## 📌 Project Overview
**Course Experiment:** Electronic Measurement Practices (EMP)  
**PCB Architecture:** 4-Layer Controlled Design  
**Primary Controller:** TI TMS320F28379D  
**Deliverables Status:** Complete Manufacturing Package Verified (Gerbers, Drill, Pos CSV, iBOM, 3D Render)

---

## 🎯 Description & Operational Principles
Texas Instruments C2000 Delfino Dual-Core 200MHz TMS320F28379D modular controlCARD with 180-pin HSEC180 edge connector, galvanically isolated USB JTAG emulator, and REF3030 precision ADC reference.

### Key Features & Subsystems
- **Processor & Logic Core:** High-efficiency architecture designed for reliable embedded operation.
- **Power Management & Regulation:** Low-noise power rail distribution with dedicated filtering and bulk decouple stages.
- **Sensory & Peripheral Interfacing:** Industrial standard interconnect headers with ESD and reverse polarity protection.
- **Fabrication & Assembly Optimization:** Standard 0805 SMD passives and leaded THT power devices for high manufacturing yield and inspectability.

---

## 🛠️ Bill of Materials (BOM Summary)

| Reference | Component Value | Package / Footprint | Description |
|:---:|:---:|:---:|:---|
| `U1` | **TMS320F28379D** | `Package_QFP:LQFP-100_14x14mm_P0.5mm` | Circuit element |
| `U2` | **FT2232HL_JTAG** | `Package_QFP:LQFP-64_10x10mm_P0.5mm` | Circuit element |
| `U3` | **REF3030_3V** | `Package_TO_SOT_SMD:SOT-23` | Circuit element |
| `J1` | **HSEC180_EDGE** | `Connector_PinHeader_2.54mm:PinHeader_2x20_P2.54mm_Vertical` | Circuit element |
| `J2` | **USB_JTAG_IN** | `Connector_USB:USB_C_Receptacle_GCT_USB4085` | Circuit element |

---

## 🏭 Manufacturing Deliverables & Artifacts

All production files have been generated in `manufacturing/`:
- **Gerber Layers (RS-274X):** Copper, solder masks, silkscreen, and board edge cuts (`manufacturing/gerbers/`)
- **Excellon Drill Files:** Plated and non-plated drill hole coordinates (`manufacturing/gerbers/*.drl`)
- **Fabricator ZIP Archive:** Single upload archive for PCB fabrication houses (`manufacturing/tms320f28379d_controlcard_gerbers.zip`)
- **Pick-and-Place Position CSV:** Centroid data for automated SMT placement machines (`manufacturing/tms320f28379d_controlcard_pos.csv`)
- **Interactive HTML BOM:** High-efficiency browser inspection and interactive assembly tool (`manufacturing/ibom.html`)
- **Altium-Style 3D Render:** Photorealistic perspective view with floor reflection shaders (`manufacturing/tms320f28379d_controlcard_3d.png`)

---

## 📐 Mechanical & Layout Constraints
- **Board Outline:** 90.0 mm × 50.0 mm
- **Layer Count:** 4 Layers (FR-4, 1.6mm thickness, 1oz/2oz copper)
- **Minimum Trace Width:** 0.20 mm (8 mil)
- **Minimum Clearance:** 0.20 mm (8 mil)
- **Via Drill / Diameter:** 0.40 mm drill / 0.80 mm annular ring pad

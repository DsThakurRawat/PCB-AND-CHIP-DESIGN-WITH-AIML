# STM32-Based 3-Phase BLDC Motor Controller

## 📌 Project Overview
**Course Experiment:** Electronic Measurement Practices (EMP)  
**PCB Architecture:** 2-Layer Controlled Design  
**Primary Controller:** STM32F401 / TI DRV8301  
**Deliverables Status:** Complete Manufacturing Package Verified (Gerbers, Drill, Pos CSV, iBOM, 3D Render)

---

## 🎯 Description & Operational Principles
Rugged 3-phase BLDC brushless motor controller integrating TI DRV8301 3-phase gate driver, 6x 60V 50A power MOSFET inverter bridge, triple low-side current shunts, bus filter caps, and Hall inputs.

### Key Features & Subsystems
- **Processor & Logic Core:** High-efficiency architecture designed for reliable embedded operation.
- **Power Management & Regulation:** Low-noise power rail distribution with dedicated filtering and bulk decouple stages.
- **Sensory & Peripheral Interfacing:** Industrial standard interconnect headers with ESD and reverse polarity protection.
- **Fabrication & Assembly Optimization:** Standard 0805 SMD passives and leaded THT power devices for high manufacturing yield and inspectability.

---

## 🛠️ Bill of Materials (BOM Summary)

| Reference | Component Value | Package / Footprint | Description |
|:---:|:---:|:---:|:---|
| `U1` | **STM32F401CCU6** | `Package_QFP:LQFP-48_7x7mm_P0.5mm` | Circuit element |
| `U2` | **DRV8301** | `Package_SO:HTSSOP-56-1EP_6.1x14mm_P0.5mm_EP3.61x6.35mm` | Circuit element |
| `Q1` | **MOSFET_U_HI** | `Package_TO_SOT_SMD:TO-252-2` | Circuit element |
| `Q2` | **MOSFET_U_LO** | `Package_TO_SOT_SMD:TO-252-2` | Circuit element |
| `Q3` | **MOSFET_V_HI** | `Package_TO_SOT_SMD:TO-252-2` | Circuit element |
| `Q4` | **MOSFET_V_LO** | `Package_TO_SOT_SMD:TO-252-2` | Circuit element |
| `Q5` | **MOSFET_W_HI** | `Package_TO_SOT_SMD:TO-252-2` | Circuit element |
| `Q6` | **MOSFET_W_LO** | `Package_TO_SOT_SMD:TO-252-2` | Circuit element |
| `J1` | **PHASE_OUT_UVW** | `TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-3-5.08_1x03_P5.08mm_Horizontal` | Circuit element |
| `J2` | **DC_BUS_IN_48V** | `TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal` | Circuit element |
| `C1` | **470uF_63V** | `Capacitor_THT:CP_Radial_D10.0mm_P5.00mm` | Circuit element |

---

## 🏭 Manufacturing Deliverables & Artifacts

All production files have been generated in `manufacturing/`:
- **Gerber Layers (RS-274X):** Copper, solder masks, silkscreen, and board edge cuts (`manufacturing/gerbers/`)
- **Excellon Drill Files:** Plated and non-plated drill hole coordinates (`manufacturing/gerbers/*.drl`)
- **Fabricator ZIP Archive:** Single upload archive for PCB fabrication houses (`manufacturing/stm32_bldc_motor_controller_gerbers.zip`)
- **Pick-and-Place Position CSV:** Centroid data for automated SMT placement machines (`manufacturing/stm32_bldc_motor_controller_pos.csv`)
- **Interactive HTML BOM:** High-efficiency browser inspection and interactive assembly tool (`manufacturing/ibom.html`)
- **Altium-Style 3D Render:** Photorealistic perspective view with floor reflection shaders (`manufacturing/stm32_bldc_motor_controller_3d.png`)

---

## 📐 Mechanical & Layout Constraints
- **Board Outline:** 95.0 mm × 68.0 mm
- **Layer Count:** 2 Layers (FR-4, 1.6mm thickness, 1oz/2oz copper)
- **Minimum Trace Width:** 0.20 mm (8 mil)
- **Minimum Clearance:** 0.20 mm (8 mil)
- **Via Drill / Diameter:** 0.40 mm drill / 0.80 mm annular ring pad

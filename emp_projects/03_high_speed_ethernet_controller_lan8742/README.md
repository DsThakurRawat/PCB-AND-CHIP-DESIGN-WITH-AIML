# High-Speed Ethernet Controller Board (LAN8742)

## 📌 Project Overview
**Course Experiment:** Electronic Measurement Practices (EMP)  
**PCB Architecture:** 2-Layer Controlled Design  
**Primary Controller:** Microchip LAN8742A  
**Deliverables Status:** Complete Manufacturing Package Verified (Gerbers, Drill, Pos CSV, iBOM, 3D Render)

---

## 🎯 Description & Operational Principles
High-performance 10/100 Ethernet Physical Layer transceiver board with RMII host bus, integrated RJ45 MagJack, MCO/25MHz clock selection, and low-jitter power decoupling for STM32H753.

### Key Features & Subsystems
- **Processor & Logic Core:** High-efficiency architecture designed for reliable embedded operation.
- **Power Management & Regulation:** Low-noise power rail distribution with dedicated filtering and bulk decouple stages.
- **Sensory & Peripheral Interfacing:** Industrial standard interconnect headers with ESD and reverse polarity protection.
- **Fabrication & Assembly Optimization:** Standard 0805 SMD passives and leaded THT power devices for high manufacturing yield and inspectability.

---

## 🛠️ Bill of Materials (BOM Summary)

| Reference | Component Value | Package / Footprint | Description |
|:---:|:---:|:---:|:---|
| `U1` | **LAN8742A** | `Package_DFN_QFN:QFN-24-1EP_4x4mm_P0.5mm_EP2.7x2.7mm` | Circuit element |
| `J1` | **RJ45_MAGJACK** | `Connector_RJ:RJ45_Amphenol_RJHSE5380` | Circuit element |
| `J2` | **RMII_STM32_BUS** | `Connector_PinHeader_2.54mm:PinHeader_2x10_P2.54mm_Vertical` | Circuit element |
| `Y1` | **25.000MHz** | `Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm` | Circuit element |
| `FB1` | **FERRITE_BEAD** | `Inductor_SMD:L_0805_2012Metric` | Circuit element |
| `C1` | **10uF** | `Capacitor_SMD:C_0805_2012Metric` | Circuit element |
| `C2` | **100nF** | `Capacitor_SMD:C_0805_2012Metric` | Circuit element |

---

## 🏭 Manufacturing Deliverables & Artifacts

All production files have been generated in `manufacturing/`:
- **Gerber Layers (RS-274X):** Copper, solder masks, silkscreen, and board edge cuts (`manufacturing/gerbers/`)
- **Excellon Drill Files:** Plated and non-plated drill hole coordinates (`manufacturing/gerbers/*.drl`)
- **Fabricator ZIP Archive:** Single upload archive for PCB fabrication houses (`manufacturing/high_speed_ethernet_lan8742_gerbers.zip`)
- **Pick-and-Place Position CSV:** Centroid data for automated SMT placement machines (`manufacturing/high_speed_ethernet_lan8742_pos.csv`)
- **Interactive HTML BOM:** High-efficiency browser inspection and interactive assembly tool (`manufacturing/ibom.html`)
- **Altium-Style 3D Render:** Photorealistic perspective view with floor reflection shaders (`manufacturing/high_speed_ethernet_lan8742_3d.png`)

---

## 📐 Mechanical & Layout Constraints
- **Board Outline:** 60.0 mm × 48.0 mm
- **Layer Count:** 2 Layers (FR-4, 1.6mm thickness, 1oz/2oz copper)
- **Minimum Trace Width:** 0.20 mm (8 mil)
- **Minimum Clearance:** 0.20 mm (8 mil)
- **Via Drill / Diameter:** 0.40 mm drill / 0.80 mm annular ring pad

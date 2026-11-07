# CH32V307 RISC-V Ethernet + PoE Development Board

## 📌 Project Overview
**Course Experiment:** Electronic Measurement Practices (EMP)  
**PCB Architecture:** 2-Layer Controlled Design  
**Primary Controller:** WCH CH32V307VCT6  
**Deliverables Status:** Complete Manufacturing Package Verified (Gerbers, Drill, Pos CSV, iBOM, 3D Render)

---

## 🎯 Description & Operational Principles
QingKe RISC-V4F development board with IEEE 802.3af Power-over-Ethernet (PoE) 48V to 5V rectification and step-down, integrated 10/100M Ethernet PHY, USB Type-C, and WCH-Link SWD.

### Key Features & Subsystems
- **Processor & Logic Core:** High-efficiency architecture designed for reliable embedded operation.
- **Power Management & Regulation:** Low-noise power rail distribution with dedicated filtering and bulk decouple stages.
- **Sensory & Peripheral Interfacing:** Industrial standard interconnect headers with ESD and reverse polarity protection.
- **Fabrication & Assembly Optimization:** Standard 0805 SMD passives and leaded THT power devices for high manufacturing yield and inspectability.

---

## 🛠️ Bill of Materials (BOM Summary)

| Reference | Component Value | Package / Footprint | Description |
|:---:|:---:|:---:|:---|
| `U1` | **CH32V307VCT6** | `Package_QFP:LQFP-100_14x14mm_P0.5mm` | Circuit element |
| `J1` | **RJ45_POE** | `Connector_RJ:RJ45_Amphenol_RJHSE5380` | Circuit element |
| `D1` | **MB10S_BRIDGE** | `Package_SO:SOIC-4_3.9x4.9mm_P1.27mm` | Circuit element |
| `U2` | **AMS1117-3.3** | `Package_TO_SOT_SMD:SOT-223-3_TabPin2` | Circuit element |
| `J2` | **USB_C** | `Connector_USB:USB_C_Receptacle_GCT_USB4085` | Circuit element |
| `J3` | **WCH_LINK_HDR** | `Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical` | Circuit element |
| `Y1` | **8.000MHz** | `Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm` | Circuit element |

---

## 🏭 Manufacturing Deliverables & Artifacts

All production files have been generated in `manufacturing/`:
- **Gerber Layers (RS-274X):** Copper, solder masks, silkscreen, and board edge cuts (`manufacturing/gerbers/`)
- **Excellon Drill Files:** Plated and non-plated drill hole coordinates (`manufacturing/gerbers/*.drl`)
- **Fabricator ZIP Archive:** Single upload archive for PCB fabrication houses (`manufacturing/ch32v307_ethernet_poe_gerbers.zip`)
- **Pick-and-Place Position CSV:** Centroid data for automated SMT placement machines (`manufacturing/ch32v307_ethernet_poe_pos.csv`)
- **Interactive HTML BOM:** High-efficiency browser inspection and interactive assembly tool (`manufacturing/ibom.html`)
- **Altium-Style 3D Render:** Photorealistic perspective view with floor reflection shaders (`manufacturing/ch32v307_ethernet_poe_3d.png`)

---

## 📐 Mechanical & Layout Constraints
- **Board Outline:** 90.0 mm × 60.0 mm
- **Layer Count:** 2 Layers (FR-4, 1.6mm thickness, 1oz/2oz copper)
- **Minimum Trace Width:** 0.20 mm (8 mil)
- **Minimum Clearance:** 0.20 mm (8 mil)
- **Via Drill / Diameter:** 0.40 mm drill / 0.80 mm annular ring pad

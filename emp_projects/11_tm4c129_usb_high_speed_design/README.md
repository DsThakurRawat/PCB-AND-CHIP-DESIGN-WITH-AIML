# TM4C129 USB High-Speed Reference Design

## 📌 Project Overview
**Course Experiment:** Electronic Measurement Practices (EMP)  
**PCB Architecture:** 2-Layer Controlled Design  
**Primary Controller:** TI TM4C1294NCPDT  
**Deliverables Status:** Complete Manufacturing Package Verified (Gerbers, Drill, Pos CSV, iBOM, 3D Render)

---

## 🎯 Description & Operational Principles
Texas Instruments TM4C129x 120MHz ARM Cortex-M4F platform with Microchip USB3300 ULPI High-Speed USB 2.0 PHY, USB-C interface, 90-ohm controlled differential impedance, and dual LDO power rails.

### Key Features & Subsystems
- **Processor & Logic Core:** High-efficiency architecture designed for reliable embedded operation.
- **Power Management & Regulation:** Low-noise power rail distribution with dedicated filtering and bulk decouple stages.
- **Sensory & Peripheral Interfacing:** Industrial standard interconnect headers with ESD and reverse polarity protection.
- **Fabrication & Assembly Optimization:** Standard 0805 SMD passives and leaded THT power devices for high manufacturing yield and inspectability.

---

## 🛠️ Bill of Materials (BOM Summary)

| Reference | Component Value | Package / Footprint | Description |
|:---:|:---:|:---:|:---|
| `U1` | **TM4C1294NCPDT** | `Package_QFP:TQFP-128_14x14mm_P0.4mm` | Circuit element |
| `U2` | **USB3300_ULPI** | `Package_DFN_QFN:QFN-32-1EP_5x5mm_P0.5mm_EP3.3x3.3mm` | Circuit element |
| `J1` | **USB_C_HS** | `Connector_USB:USB_C_Receptacle_GCT_USB4085` | Circuit element |
| `Y1` | **24.000MHz** | `Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm` | Circuit element |
| `Y2` | **25.000MHz** | `Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm` | Circuit element |
| `J2` | **ARM_JTAG_10PIN** | `Connector_PinHeader_1.27mm:PinHeader_2x05_P1.27mm_Vertical` | Circuit element |

---

## 🏭 Manufacturing Deliverables & Artifacts

All production files have been generated in `manufacturing/`:
- **Gerber Layers (RS-274X):** Copper, solder masks, silkscreen, and board edge cuts (`manufacturing/gerbers/`)
- **Excellon Drill Files:** Plated and non-plated drill hole coordinates (`manufacturing/gerbers/*.drl`)
- **Fabricator ZIP Archive:** Single upload archive for PCB fabrication houses (`manufacturing/tm4c129_usb_high_speed_gerbers.zip`)
- **Pick-and-Place Position CSV:** Centroid data for automated SMT placement machines (`manufacturing/tm4c129_usb_high_speed_pos.csv`)
- **Interactive HTML BOM:** High-efficiency browser inspection and interactive assembly tool (`manufacturing/ibom.html`)
- **Altium-Style 3D Render:** Photorealistic perspective view with floor reflection shaders (`manufacturing/tm4c129_usb_high_speed_3d.png`)

---

## 📐 Mechanical & Layout Constraints
- **Board Outline:** 85.0 mm × 60.0 mm
- **Layer Count:** 2 Layers (FR-4, 1.6mm thickness, 1oz/2oz copper)
- **Minimum Trace Width:** 0.20 mm (8 mil)
- **Minimum Clearance:** 0.20 mm (8 mil)
- **Via Drill / Diameter:** 0.40 mm drill / 0.80 mm annular ring pad

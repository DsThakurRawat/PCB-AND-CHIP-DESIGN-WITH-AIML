# Custom ESP32-S3 Development Board with USB-C

## 📌 Project Overview
**Course Experiment:** Electronic Measurement Practices (EMP)  
**PCB Architecture:** 2-Layer Controlled Design  
**Primary Controller:** ESP32-S3-WROOM-1  
**Deliverables Status:** Complete Manufacturing Package Verified (Gerbers, Drill, Pos CSV, iBOM, 3D Render)

---

## 🎯 Description & Operational Principles
High-performance IoT dev board powered by Espressif ESP32-S3-WROOM-1 with native USB Type-C, ESD suppressor, CH340K / dual-transistor auto-reset circuitry, WS2812B RGB LED, and 800mA 3.3V LDO.

### Key Features & Subsystems
- **Processor & Logic Core:** High-efficiency architecture designed for reliable embedded operation.
- **Power Management & Regulation:** Low-noise power rail distribution with dedicated filtering and bulk decouple stages.
- **Sensory & Peripheral Interfacing:** Industrial standard interconnect headers with ESD and reverse polarity protection.
- **Fabrication & Assembly Optimization:** Standard 0805 SMD passives and leaded THT power devices for high manufacturing yield and inspectability.

---

## 🛠️ Bill of Materials (BOM Summary)

| Reference | Component Value | Package / Footprint | Description |
|:---:|:---:|:---:|:---|
| `U1` | **ESP32-S3-WROOM-1** | `RF_Module:ESP32-S3-WROOM-1` | Circuit element |
| `J1` | **USB_C** | `Connector_USB:USB_C_Receptacle_GCT_USB4085` | Circuit element |
| `U2` | **AMS1117-3.3** | `Package_TO_SOT_SMD:SOT-223-3_TabPin2` | Circuit element |
| `D1` | **WS2812B_RGB** | `LED_SMD:LED_WS2812B_PLCC4_5.0x5.0mm_P3.2mm` | Circuit element |
| `SW1` | **RESET** | `Button_Switch_SMD:SW_Push_SPST_NO_Alps_SKRK` | Circuit element |
| `SW2` | **BOOT** | `Button_Switch_SMD:SW_Push_SPST_NO_Alps_SKRK` | Circuit element |

---

## 🏭 Manufacturing Deliverables & Artifacts

All production files have been generated in `manufacturing/`:
- **Gerber Layers (RS-274X):** Copper, solder masks, silkscreen, and board edge cuts (`manufacturing/gerbers/`)
- **Excellon Drill Files:** Plated and non-plated drill hole coordinates (`manufacturing/gerbers/*.drl`)
- **Fabricator ZIP Archive:** Single upload archive for PCB fabrication houses (`manufacturing/esp32_s3_usbc_devboard_gerbers.zip`)
- **Pick-and-Place Position CSV:** Centroid data for automated SMT placement machines (`manufacturing/esp32_s3_usbc_devboard_pos.csv`)
- **Interactive HTML BOM:** High-efficiency browser inspection and interactive assembly tool (`manufacturing/ibom.html`)
- **Altium-Style 3D Render:** Photorealistic perspective view with floor reflection shaders (`manufacturing/esp32_s3_usbc_devboard_3d.png`)

---

## 📐 Mechanical & Layout Constraints
- **Board Outline:** 58.0 mm × 28.0 mm
- **Layer Count:** 2 Layers (FR-4, 1.6mm thickness, 1oz/2oz copper)
- **Minimum Trace Width:** 0.20 mm (8 mil)
- **Minimum Clearance:** 0.20 mm (8 mil)
- **Via Drill / Diameter:** 0.40 mm drill / 0.80 mm annular ring pad

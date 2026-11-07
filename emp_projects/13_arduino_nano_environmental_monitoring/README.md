# Arduino Nano-Based Environmental Monitoring System

## 📌 Project Overview
**Course Experiment:** Electronic Measurement Practices (EMP)  
**PCB Architecture:** 2-Layer Controlled Design  
**Primary Controller:** Arduino Nano Core  
**Deliverables Status:** Complete Manufacturing Package Verified (Gerbers, Drill, Pos CSV, iBOM, 3D Render)

---

## 🎯 Description & Operational Principles
Compact environmental sensing instrument incorporating Bosch BME280 (temperature, humidity, barometric pressure), MQ-135 air quality gas analyzer, 0.96-inch I2C OLED display, and acoustic alarm.

### Key Features & Subsystems
- **Processor & Logic Core:** High-efficiency architecture designed for reliable embedded operation.
- **Power Management & Regulation:** Low-noise power rail distribution with dedicated filtering and bulk decouple stages.
- **Sensory & Peripheral Interfacing:** Industrial standard interconnect headers with ESD and reverse polarity protection.
- **Fabrication & Assembly Optimization:** Standard 0805 SMD passives and leaded THT power devices for high manufacturing yield and inspectability.

---

## 🛠️ Bill of Materials (BOM Summary)

| Reference | Component Value | Package / Footprint | Description |
|:---:|:---:|:---:|:---|
| `J1` | **NANO_HDR_L** | `Connector_PinHeader_2.54mm:PinHeader_1x15_P2.54mm_Vertical` | Circuit element |
| `J2` | **NANO_HDR_R** | `Connector_PinHeader_2.54mm:PinHeader_1x15_P2.54mm_Vertical` | Circuit element |
| `U1` | **BME280_SENSOR** | `Package_LGA:LGA-8_2.5x2.5mm_P0.65mm` | Circuit element |
| `J3` | **MQ135_GAS_SOCKET** | `Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical` | Circuit element |
| `J4` | **OLED_SSD1306_4P** | `Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical` | Circuit element |
| `BZ1` | **BUZZER** | `Buzzer_Beeper:Buzzer_12x9.5RM7.6` | Circuit element |
| `J5` | **PWR_IN_5V** | `TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal` | Circuit element |

---

## 🏭 Manufacturing Deliverables & Artifacts

All production files have been generated in `manufacturing/`:
- **Gerber Layers (RS-274X):** Copper, solder masks, silkscreen, and board edge cuts (`manufacturing/gerbers/`)
- **Excellon Drill Files:** Plated and non-plated drill hole coordinates (`manufacturing/gerbers/*.drl`)
- **Fabricator ZIP Archive:** Single upload archive for PCB fabrication houses (`manufacturing/arduino_nano_environmental_monitoring_gerbers.zip`)
- **Pick-and-Place Position CSV:** Centroid data for automated SMT placement machines (`manufacturing/arduino_nano_environmental_monitoring_pos.csv`)
- **Interactive HTML BOM:** High-efficiency browser inspection and interactive assembly tool (`manufacturing/ibom.html`)
- **Altium-Style 3D Render:** Photorealistic perspective view with floor reflection shaders (`manufacturing/arduino_nano_environmental_monitoring_3d.png`)

---

## 📐 Mechanical & Layout Constraints
- **Board Outline:** 80.0 mm × 60.0 mm
- **Layer Count:** 2 Layers (FR-4, 1.6mm thickness, 1oz/2oz copper)
- **Minimum Trace Width:** 0.20 mm (8 mil)
- **Minimum Clearance:** 0.20 mm (8 mil)
- **Via Drill / Diameter:** 0.40 mm drill / 0.80 mm annular ring pad

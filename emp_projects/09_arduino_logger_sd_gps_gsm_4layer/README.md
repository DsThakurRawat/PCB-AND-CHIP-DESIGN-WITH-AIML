# Arduino Telemetry Logger with SD Card, GPS and GSM (4-Layer PCB)

## 📌 Project Overview
**Course Experiment:** Electronic Measurement Practices (EMP)  
**PCB Architecture:** 4-Layer Controlled Design  
**Primary Controller:** ATmega328P-AU  
**Deliverables Status:** Complete Manufacturing Package Verified (Gerbers, Drill, Pos CSV, iBOM, 3D Render)

---

## 🎯 Description & Operational Principles
Rugged 4-layer remote telemetry logging platform incorporating ATmega328P MCU, SIM800L cellular GSM modem with high-burst capacitors, NEO-6M GPS satellite receiver, and SPI MicroSD socket.

### Key Features & Subsystems
- **Processor & Logic Core:** High-efficiency architecture designed for reliable embedded operation.
- **Power Management & Regulation:** Low-noise power rail distribution with dedicated filtering and bulk decouple stages.
- **Sensory & Peripheral Interfacing:** Industrial standard interconnect headers with ESD and reverse polarity protection.
- **Fabrication & Assembly Optimization:** Standard 0805 SMD passives and leaded THT power devices for high manufacturing yield and inspectability.

---

## 🛠️ Bill of Materials (BOM Summary)

| Reference | Component Value | Package / Footprint | Description |
|:---:|:---:|:---:|:---|
| `U1` | **ATmega328P-AU** | `Package_QFP:TQFP-32_7x7mm_P0.8mm` | Circuit element |
| `U2` | **SIM800L_MOD** | `RF_Module:SIM800L` | Circuit element |
| `U3` | **NEO-6M_GPS** | `RF_GPS:UBX-NEO-6M` | Circuit element |
| `J1` | **MICROSD_SLOT** | `Connector_Card:microSD_HC_Hirose_DM3D-SF` | Circuit element |
| `C1` | **1000uF_6.3V** | `Capacitor_Tantalum_SMD:CP_EIA-7343-31_Kemet-D` | Circuit element |
| `U4` | **TPS63020_REG** | `Package_DFN_QFN:QFN-14-1EP_3x4mm_P0.5mm_EP1.65x2.65mm` | Circuit element |

---

## 🏭 Manufacturing Deliverables & Artifacts

All production files have been generated in `manufacturing/`:
- **Gerber Layers (RS-274X):** Copper, solder masks, silkscreen, and board edge cuts (`manufacturing/gerbers/`)
- **Excellon Drill Files:** Plated and non-plated drill hole coordinates (`manufacturing/gerbers/*.drl`)
- **Fabricator ZIP Archive:** Single upload archive for PCB fabrication houses (`manufacturing/arduino_logger_sd_gps_gsm_gerbers.zip`)
- **Pick-and-Place Position CSV:** Centroid data for automated SMT placement machines (`manufacturing/arduino_logger_sd_gps_gsm_pos.csv`)
- **Interactive HTML BOM:** High-efficiency browser inspection and interactive assembly tool (`manufacturing/ibom.html`)
- **Altium-Style 3D Render:** Photorealistic perspective view with floor reflection shaders (`manufacturing/arduino_logger_sd_gps_gsm_3d.png`)

---

## 📐 Mechanical & Layout Constraints
- **Board Outline:** 80.0 mm × 60.0 mm
- **Layer Count:** 4 Layers (FR-4, 1.6mm thickness, 1oz/2oz copper)
- **Minimum Trace Width:** 0.20 mm (8 mil)
- **Minimum Clearance:** 0.20 mm (8 mil)
- **Via Drill / Diameter:** 0.40 mm drill / 0.80 mm annular ring pad

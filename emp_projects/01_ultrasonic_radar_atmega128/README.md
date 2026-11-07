# Ultrasonic Radar Model Using ATmega128

## 📌 Project Overview
**Course Experiment:** Electronic Measurement Practices (EMP)  
**PCB Architecture:** 2-Layer Controlled Design  
**Primary Controller:** ATmega128A  
**Deliverables Status:** Complete Manufacturing Package Verified (Gerbers, Drill, Pos CSV, iBOM, 3D Render)

---

## 🎯 Description & Operational Principles
Panoramic ultrasonic radar mapping station with ATmega128 MCU, SG90 servo sweep platform, HC-SR04 sonar module, 16x2 HD44780 LCD readout, and RS232 host telemetry.

### Key Features & Subsystems
- **Processor & Logic Core:** High-efficiency architecture designed for reliable embedded operation.
- **Power Management & Regulation:** Low-noise power rail distribution with dedicated filtering and bulk decouple stages.
- **Sensory & Peripheral Interfacing:** Industrial standard interconnect headers with ESD and reverse polarity protection.
- **Fabrication & Assembly Optimization:** Standard 0805 SMD passives and leaded THT power devices for high manufacturing yield and inspectability.

---

## 🛠️ Bill of Materials (BOM Summary)

| Reference | Component Value | Package / Footprint | Description |
|:---:|:---:|:---:|:---|
| `U1` | **ATmega128A** | `Package_QFP:TQFP-64_14x14mm_P0.8mm` | Circuit element |
| `U2` | **MAX232** | `Package_SO:SOIC-16_3.9x9.9mm_P1.27mm` | Circuit element |
| `U3` | **LM7805** | `Package_TO_SOT_SMD:TO-252-2` | Circuit element |
| `J1` | **HC_SR04_HDR** | `Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical` | Circuit element |
| `J2` | **SERVO_SG90** | `Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical` | Circuit element |
| `J3` | **LCD_16x2_HDR** | `Connector_PinHeader_2.54mm:PinHeader_1x16_P2.54mm_Vertical` | Circuit element |
| `J4` | **AVR_ISP_6PIN** | `Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Vertical` | Circuit element |
| `J5` | **PWR_JACK** | `Connector_BarrelJack:BarrelJack_Horizontal` | Circuit element |
| `Y1` | **16MHz_XTAL** | `Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm` | Circuit element |
| `C1` | **100uF_16V** | `Capacitor_THT:CP_Radial_D6.3mm_P2.50mm` | Circuit element |
| `C2` | **100nF** | `Capacitor_SMD:C_0805_2012Metric` | Circuit element |
| `R1` | **10k_RST** | `Resistor_SMD:R_0805_2012Metric` | Circuit element |
| `SW1` | **RESET** | `Button_Switch_SMD:SW_Push_SPST_NO_Alps_SKRK` | Circuit element |
| `D1` | **PWR_LED** | `LED_SMD:LED_0805_2012Metric` | Circuit element |

---

## 🏭 Manufacturing Deliverables & Artifacts

All production files have been generated in `manufacturing/`:
- **Gerber Layers (RS-274X):** Copper, solder masks, silkscreen, and board edge cuts (`manufacturing/gerbers/`)
- **Excellon Drill Files:** Plated and non-plated drill hole coordinates (`manufacturing/gerbers/*.drl`)
- **Fabricator ZIP Archive:** Single upload archive for PCB fabrication houses (`manufacturing/ultrasonic_radar_atmega128_gerbers.zip`)
- **Pick-and-Place Position CSV:** Centroid data for automated SMT placement machines (`manufacturing/ultrasonic_radar_atmega128_pos.csv`)
- **Interactive HTML BOM:** High-efficiency browser inspection and interactive assembly tool (`manufacturing/ibom.html`)
- **Altium-Style 3D Render:** Photorealistic perspective view with floor reflection shaders (`manufacturing/ultrasonic_radar_atmega128_3d.png`)

---

## 📐 Mechanical & Layout Constraints
- **Board Outline:** 100.0 mm × 75.0 mm
- **Layer Count:** 2 Layers (FR-4, 1.6mm thickness, 1oz/2oz copper)
- **Minimum Trace Width:** 0.20 mm (8 mil)
- **Minimum Clearance:** 0.20 mm (8 mil)
- **Via Drill / Diameter:** 0.40 mm drill / 0.80 mm annular ring pad

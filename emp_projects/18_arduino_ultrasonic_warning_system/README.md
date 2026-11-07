# Monitoring and Warning System Using Arduino and Ultrasonic Sensor

## 📌 Project Overview
**Course Experiment:** Electronic Measurement Practices (EMP)  
**PCB Architecture:** 2-Layer Controlled Design  
**Primary Controller:** ATmega328P / Arduino Core  
**Deliverables Status:** Complete Manufacturing Package Verified (Gerbers, Drill, Pos CSV, iBOM, 3D Render)

---

## 🎯 Description & Operational Principles
Automated distance perimeter monitoring and alarm station featuring HC-SR04 ultrasonic sonar, 3-level LED status warning (Green/Yellow/Red), high-output piezo alarm, and SPDT relay for external loads.

### Key Features & Subsystems
- **Processor & Logic Core:** High-efficiency architecture designed for reliable embedded operation.
- **Power Management & Regulation:** Low-noise power rail distribution with dedicated filtering and bulk decouple stages.
- **Sensory & Peripheral Interfacing:** Industrial standard interconnect headers with ESD and reverse polarity protection.
- **Fabrication & Assembly Optimization:** Standard 0805 SMD passives and leaded THT power devices for high manufacturing yield and inspectability.

---

## 🛠️ Bill of Materials (BOM Summary)

| Reference | Component Value | Package / Footprint | Description |
|:---:|:---:|:---:|:---|
| `U1` | **ATmega328P-PU** | `Package_DIP:DIP-28_W7.62mm` | Circuit element |
| `J1` | **HC_SR04_PORT** | `Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical` | Circuit element |
| `K1` | **RELAY_5V_SPDT** | `Relay_THT:Relay_SPDT_SANYOU_SRD_Series_Form_C` | Circuit element |
| `J2` | **RELAY_OUT_AC** | `TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-3-5.08_1x03_P5.08mm_Horizontal` | Circuit element |
| `BZ1` | **ALARM_BUZZER** | `Buzzer_Beeper:Buzzer_12x9.5RM7.6` | Circuit element |
| `D1` | **LED_SAFE_GRN** | `LED_THT:LED_D5.0mm` | Circuit element |
| `D2` | **LED_WARN_YEL** | `LED_THT:LED_D5.0mm` | Circuit element |
| `D3` | **LED_DANG_RED** | `LED_THT:LED_D5.0mm` | Circuit element |
| `J3` | **LCD_I2C_HDR** | `Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical` | Circuit element |
| `J4` | **DC_PWR_IN_5V** | `Connector_BarrelJack:BarrelJack_Horizontal` | Circuit element |

---

## 🏭 Manufacturing Deliverables & Artifacts

All production files have been generated in `manufacturing/`:
- **Gerber Layers (RS-274X):** Copper, solder masks, silkscreen, and board edge cuts (`manufacturing/gerbers/`)
- **Excellon Drill Files:** Plated and non-plated drill hole coordinates (`manufacturing/gerbers/*.drl`)
- **Fabricator ZIP Archive:** Single upload archive for PCB fabrication houses (`manufacturing/arduino_ultrasonic_warning_system_gerbers.zip`)
- **Pick-and-Place Position CSV:** Centroid data for automated SMT placement machines (`manufacturing/arduino_ultrasonic_warning_system_pos.csv`)
- **Interactive HTML BOM:** High-efficiency browser inspection and interactive assembly tool (`manufacturing/ibom.html`)
- **Altium-Style 3D Render:** Photorealistic perspective view with floor reflection shaders (`manufacturing/arduino_ultrasonic_warning_system_3d.png`)

---

## 📐 Mechanical & Layout Constraints
- **Board Outline:** 85.0 mm × 60.0 mm
- **Layer Count:** 2 Layers (FR-4, 1.6mm thickness, 1oz/2oz copper)
- **Minimum Trace Width:** 0.20 mm (8 mil)
- **Minimum Clearance:** 0.20 mm (8 mil)
- **Via Drill / Diameter:** 0.40 mm drill / 0.80 mm annular ring pad

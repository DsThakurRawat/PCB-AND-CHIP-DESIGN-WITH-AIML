# Arduino Multi-Sensor Training Robot PCB with L298 Motor Driver

## 📌 Project Overview
**Course Experiment:** Electronic Measurement Practices (EMP)  
**PCB Architecture:** 2-Layer Controlled Design  
**Primary Controller:** ATmega328P / Arduino Shield  
**Deliverables Status:** Complete Manufacturing Package Verified (Gerbers, Drill, Pos CSV, iBOM, 3D Render)

---

## 🎯 Description & Operational Principles
Robotics educational development board featuring an ST L298 dual H-bridge motor driver, 8x flyback Schottky diodes, 4x IR line tracker headers, HC-SR04 sonar port, dual LDR inputs, and TO-220 5V regulator.

### Key Features & Subsystems
- **Processor & Logic Core:** High-efficiency architecture designed for reliable embedded operation.
- **Power Management & Regulation:** Low-noise power rail distribution with dedicated filtering and bulk decouple stages.
- **Sensory & Peripheral Interfacing:** Industrial standard interconnect headers with ESD and reverse polarity protection.
- **Fabrication & Assembly Optimization:** Standard 0805 SMD passives and leaded THT power devices for high manufacturing yield and inspectability.

---

## 🛠️ Bill of Materials (BOM Summary)

| Reference | Component Value | Package / Footprint | Description |
|:---:|:---:|:---:|:---|
| `U1` | **L298_DRIVER** | `Package_TO_SOT_THT:TO-220-15_P2.54x5.08mm_StaggerEven_Lead4.58mm_Vertical` | Circuit element |
| `U2` | **LM7805** | `Package_TO_SOT_THT:TO-220-3_Vertical` | Circuit element |
| `J1` | **MOTOR_LEFT** | `TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal` | Circuit element |
| `J2` | **MOTOR_RIGHT** | `TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal` | Circuit element |
| `J3` | **BATTERY_IN_12V** | `TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal` | Circuit element |
| `J4` | **IR_SENSORS_4X** | `Connector_PinHeader_2.54mm:PinHeader_1x12_P2.54mm_Vertical` | Circuit element |
| `J5` | **HC_SR04_PORT** | `Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical` | Circuit element |
| `BZ1` | **BUZZER** | `Buzzer_Beeper:Buzzer_12x9.5RM7.6` | Circuit element |
| `C1` | **470uF_25V** | `Capacitor_THT:CP_Radial_D10.0mm_P5.00mm` | Circuit element |

---

## 🏭 Manufacturing Deliverables & Artifacts

All production files have been generated in `manufacturing/`:
- **Gerber Layers (RS-274X):** Copper, solder masks, silkscreen, and board edge cuts (`manufacturing/gerbers/`)
- **Excellon Drill Files:** Plated and non-plated drill hole coordinates (`manufacturing/gerbers/*.drl`)
- **Fabricator ZIP Archive:** Single upload archive for PCB fabrication houses (`manufacturing/arduino_multisensor_robot_l298d_gerbers.zip`)
- **Pick-and-Place Position CSV:** Centroid data for automated SMT placement machines (`manufacturing/arduino_multisensor_robot_l298d_pos.csv`)
- **Interactive HTML BOM:** High-efficiency browser inspection and interactive assembly tool (`manufacturing/ibom.html`)
- **Altium-Style 3D Render:** Photorealistic perspective view with floor reflection shaders (`manufacturing/arduino_multisensor_robot_l298d_3d.png`)

---

## 📐 Mechanical & Layout Constraints
- **Board Outline:** 105.0 mm × 85.0 mm
- **Layer Count:** 2 Layers (FR-4, 1.6mm thickness, 1oz/2oz copper)
- **Minimum Trace Width:** 0.20 mm (8 mil)
- **Minimum Clearance:** 0.20 mm (8 mil)
- **Via Drill / Diameter:** 0.40 mm drill / 0.80 mm annular ring pad

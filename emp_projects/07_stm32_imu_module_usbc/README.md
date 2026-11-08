# STM32-Based 6/9-DoF IMU Module with USB-C

## 📌 Project Overview
**Course Experiment:** Electronic Measurement Practices (EMP) — Project 07  
**PCB Architecture:** 4-Layer Controlled Impedance Design (SIG-GND-GND-SIG)  
**Primary Controller:** STM32F411CEU6 (ARM Cortex-M4 32-bit MCU with FPU, UFQFPN-48)  
**Motion Sensor:** TDK InvenSense MPU-6050 (6-Axis Gyroscope + Accelerometer, QFN-24)  
**Interface:** USB Type-C (Molex 217179-0001 Receptacle) with Dedicated ESD Protection  
**Deliverables Status:** Complete Turnkey Manufacturing Suite Verified (0 ERC Violations, 0 DRC Errors, 0 Unconnected Items, 0 Schematic Parity Mismatches)

---

## 🎯 Description & Operational Principles
Compact high-precision motion tracking inertial measurement unit featuring an STM32 MCU, 6-axis IMU, USB Type-C interface, ESD protection, and precision 3.3V low-dropout power conditioning.

### Key Features & Subsystems
- **Processor & Logic Core:** STM32F411CEU6 operating up to 100 MHz with 512 KB Flash, 128 KB SRAM, and 24 MHz external crystal oscillator.
- **Inertial Measurement Core:** MPU-6050 6-axis motion tracking sensor connected via dedicated I²C interface (`IMU_SCL` / `IMU_SDA` on PB8/PB9) with external hardware interrupt (`IMU_INT` on PB12).
- **USB Type-C Interfacing:** Molex 217179-0001 reversible connector with 5.1 kΩ CC pull-downs for automatic host detection, bidirectional USB 2.0 full-speed differential pair (`USB_D_P` / `USB_D_N`), and AQ3045-01ETG ESD protection diodes.
- **Power Architecture:** AMS1117-3.3V LDO regulator converting 5V USB VBUS to low-noise 3.3V system rail with bulk decoupling and filtered regulation networks.
- **Debug & Expansion:** No-legs Tag-Connect TC2030-NL SWD debugging interface and JST-GH SM06B-GHS-TB 6-pin auxiliary sensor expansion header.

---

## 🛠️ Bill of Materials (BOM Summary)

| Reference | Component Value | Package / Footprint | Description | Qty |
|:---:|:---:|:---:|:---|:---:|
| **U1** | AMS1117-3.3 | SOT-223 | 1A Low-Dropout Linear Voltage Regulator (5V to 3.3V) | 1 |
| **U2** | STM32F411CEU6 | UFQFPN-48 (7×7mm) | ARM Cortex-M4 32-Bit MCU + FPU, 512KB Flash, 128KB RAM | 1 |
| **U3** | MPU-6050 | QFN-24 (4×4mm) | 6-Axis Motion Tracking Sensor (3-Axis Gyro + 3-Axis Accel) | 1 |
| **J1** | 217179-0001 | USB Type-C SMD | Molex 16-Pin USB 2.0 Type-C Receptacle | 1 |
| **J2** | TC2030-NL | Tag-Connect 6-Pin | No-Legs SWD Programming and Debug Connector | 1 |
| **J3** | SM06B-GHS-TB | JST GH 1.25mm 6P | 6-Position Horizontal Auxiliary Expansion Header | 1 |
| **X1** | 24MHz | SMD 3225 | High-Precision System Crystal Resonator (10ppm, 7pF) | 1 |
| **D1** | GREEN | 0402 SMD | Power Status Indicator LED (3.3V Rail) | 1 |
| **D2** | RED | 0402 SMD | Microcontroller Status Indicator LED (PB13) | 1 |
| **D3, D4, D5** | AQ3045-01ETG | SOD-882 | 30kV Automotive Bi-directional TVS ESD Protection Diodes | 3 |
| **C1** | 100nF, 50V | 0402 SMD | Ceramic Input Decoupling Capacitor | 1 |
| **C3, C4** | 22µF | 0805 SMD | Bulk Filtering Capacitors (+5V VBUS & +3.3V LDO Rail) | 2 |
| **C5, C12** | 2.2µF | 0603 SMD | MCU VCAP1 Internal Regulator Filter & IMU Decoupling | 2 |
| **C6, C9, C10, C13, C14, C15, C16, C17, C** | 100nF | 0402 SMD | Power Rail & Reset Decoupling High-Frequency Filter Caps | 9 |
| **C7, C8** | 10pF | 0402 SMD | 24MHz Crystal Oscillator Load Capacitors | 2 |
| **C11** | 2.2nF | 0402 SMD | IMU Charge Pump Output Capacitor (`IMU_CPOUT`) | 1 |
| **R1, R4** | 1kΩ | 0402 SMD | Current-Limiting Resistors for Power and Status LEDs | 2 |
| **R2, R3** | 2.2kΩ | 0402 SMD | I²C Bus Pull-Up Resistors (`IMU_SCL` / `IMU_SDA`) | 2 |
| **R5** | 10kΩ | 0402 SMD | Microcontroller Hardware Reset Pull-Up Resistor (`NRST`) | 1 |
| **R6** | 0Ω | 0402 SMD | Crystal Oscillator Drive Damping / Bypass Resistor | 1 |
| **R7** | 10kΩ | 0402 SMD | Bootloader Configuration Pull-Down Resistor (`BOOT0`) | 1 |
| **R8, R9** | 5.1kΩ | 0402 SMD | USB Type-C Configuration Channel Pull-Downs (CC1 / CC2) | 2 |
| **MH1–MH4** | M3 | 3.2mm NPTH | Mechanical Chassis Mounting Holes (30mm × 30mm Pattern) | 4 |
| **TH1, TH2** | 1.15mm | NPTH | Optical Fabrication and Assembly Tooling Alignment Holes | 2 |

---

## 🏭 Manufacturing Deliverables & Artifacts

All production files are generated in [`manufacturing/`](file:///home/divyansh-rawat/AIPCBDESIGN/emp_projects/07_stm32_imu_module_usbc/manufacturing):
- **Gerber Layers (RS-274X):** Copper, solder masks, silkscreen, paste, edge cuts ([`manufacturing/gerbers/`](file:///home/divyansh-rawat/AIPCBDESIGN/emp_projects/07_stm32_imu_module_usbc/manufacturing/gerbers))
- **Excellon Drill Files:** Plated and non-plated drill hole coordinates ([`manufacturing/gerbers/stm32_imu_module_usbc.drl`](file:///home/divyansh-rawat/AIPCBDESIGN/emp_projects/07_stm32_imu_module_usbc/manufacturing/gerbers/stm32_imu_module_usbc.drl))
- **Fabricator ZIP Archive:** Production archive for PCB fab houses ([`manufacturing/stm32_imu_module_usbc_gerbers.zip`](file:///home/divyansh-rawat/AIPCBDESIGN/emp_projects/07_stm32_imu_module_usbc/manufacturing/stm32_imu_module_usbc_gerbers.zip))
- **Pick-and-Place Position CSV:** Centroid coordinates for automated SMT assembly ([`manufacturing/stm32_imu_module_usbc_pos.csv`](file:///home/divyansh-rawat/AIPCBDESIGN/emp_projects/07_stm32_imu_module_usbc/manufacturing/stm32_imu_module_usbc_pos.csv))
- **Interactive HTML BOM:** Interactive visual assembly inspection tool ([`manufacturing/ibom.html`](file:///home/divyansh-rawat/AIPCBDESIGN/emp_projects/07_stm32_imu_module_usbc/manufacturing/ibom.html))
- **Assembly Documentation PDF:** Production schematic and board drawings ([`manufacturing/stm32_imu_module_usbc.pdf`](file:///home/divyansh-rawat/AIPCBDESIGN/emp_projects/07_stm32_imu_module_usbc/manufacturing/stm32_imu_module_usbc.pdf))
- **Altium-Style 3D Render:** High-resolution perspective render ([`manufacturing/stm32_imu_module_usbc_3d.png`](file:///home/divyansh-rawat/AIPCBDESIGN/emp_projects/07_stm32_imu_module_usbc/manufacturing/stm32_imu_module_usbc_3d.png))

---

## 📐 Mechanical & Layout Constraints
- **Board Outline:** 36.00 mm × 36.00 mm with 3.0 mm radiused corners
- **Layer Count:** 4 Layers (L1: Signal, L2: GND Plane, L3: GND Plane, L4: Signal)
- **Minimum Trace Width:** 0.127 mm (5 mil)
- **Minimum Clearance:** 0.127 mm (5 mil)
- **Via Drill / Diameter:** 0.20 mm drill / 0.40 mm diameter micro-vias
- **Controlled Impedance:** 90 Ω USB differential impedance pair (`USB_D_P` / `USB_D_N`)

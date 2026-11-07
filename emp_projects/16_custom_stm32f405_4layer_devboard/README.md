# Custom STM32F405 4-Layer Development Board

## 📌 Project Overview
**Course Experiment:** Electronic Measurement Practices (EMP)  
**PCB Architecture:** 4-Layer Controlled Design  
**Primary Controller:** Embedded Controller  
**Deliverables Status:** Complete Manufacturing Package Verified (Gerbers, Drill, Pos CSV, iBOM, 3D Render)

---

## 🎯 Description & Operational Principles
High-density 4-layer development module with STM32F405RGT6 (168MHz ARM Cortex-M4), solid internal ground/power planes, USB-C interface, SWD programming header, and peripheral breakout headers.

### Key Features & Subsystems
- **Processor & Logic Core:** High-efficiency architecture designed for reliable embedded operation.
- **Power Management & Regulation:** Low-noise power rail distribution with dedicated filtering and bulk decouple stages.
- **Sensory & Peripheral Interfacing:** Industrial standard interconnect headers with ESD and reverse polarity protection.
- **Fabrication & Assembly Optimization:** Standard 0805 SMD passives and leaded THT power devices for high manufacturing yield and inspectability.

---

## 🛠️ Bill of Materials (BOM Summary)

| Reference | Component Value | Package / Footprint | Description |
|:---:|:---:|:---:|:---|

---

## 🏭 Manufacturing Deliverables & Artifacts

All production files have been generated in `manufacturing/`:
- **Gerber Layers (RS-274X):** Copper, solder masks, silkscreen, and board edge cuts (`manufacturing/gerbers/`)
- **Excellon Drill Files:** Plated and non-plated drill hole coordinates (`manufacturing/gerbers/*.drl`)
- **Fabricator ZIP Archive:** Single upload archive for PCB fabrication houses (`manufacturing/custom_stm32f405_4layer_gerbers.zip`)
- **Pick-and-Place Position CSV:** Centroid data for automated SMT placement machines (`manufacturing/custom_stm32f405_4layer_pos.csv`)
- **Interactive HTML BOM:** High-efficiency browser inspection and interactive assembly tool (`manufacturing/ibom.html`)
- **Altium-Style 3D Render:** Photorealistic perspective view with floor reflection shaders (`manufacturing/custom_stm32f405_4layer_3d.png`)

---

## 📐 Mechanical & Layout Constraints
- **Board Outline:** 80 mm × 60 mm
- **Layer Count:** 4 Layers (FR-4, 1.6mm thickness, 1oz/2oz copper)
- **Minimum Trace Width:** 0.20 mm (8 mil)
- **Minimum Clearance:** 0.20 mm (8 mil)
- **Via Drill / Diameter:** 0.40 mm drill / 0.80 mm annular ring pad

# Electronic Prototyping and Manufacturing (EPM) Laboratory — Viva Voce
## Student: Divyansh Rawat (Roll No: 124EC0030)
## Faculty: Dr. Eswaramoorthy K V | IIIT Kurnool

---

### Question:
> **A block diagram of Circuit is given.**
> **Answer: List all the design considerations for each functional block when designing a PCB.**

---

### Block 1: Power Supply & Filtering Subsystem (9V DC Input, Protection, Bulk Reservoir)
1. **Reverse Polarity Protection:** A series protection diode (e.g., 1N4007 or Schottky 1N5819) installed at the 9V power input connector prevents instantaneous destruction of polarized electrolytic capacitors and 555 ICs if a battery is connected in reverse.
2. **Decoupling Hierarchy (Multi-Tier Filtering):**
   - **Bulk Reservoir Capacitor (100 µF, 16V):** Absorbs low-frequency voltage sag and current surges caused by totem-pole switching.
   - **High-Frequency Local Bypass Capacitors (100 nF Ceramic Disc):** Positioned within 3 mm of Pin 8 (VCC) and Pin 1 (GND) of each 555 timer to supply fast edge transient current ($dI/dt$) and eliminate high-frequency switching hash.
3. **Trace Current Sizing:** Power distribution rails (+9V and GND) are routed with wide traces (0.80 mm width) to minimize parasitic trace resistance ($IR$ drop) and parasitic loop inductance.
4. **Visual Power Diagnostics:** A green LED in series with a 1 kΩ ballast resistor provides visual confirmation of power integrity on the board.
5. **Dedicated Diagnostic Test Points:** Labeled through-hole test points `TP1` (+9V) and `TP2` (GND) for multimeter and oscilloscope grounding.

---

### Block 2: Inductance-Sensitive Timing Core (External Choke Connectors J2/J4, LC Tank, 555 Astable Core)
1. **Loop Area Minimization:** The oscillatory loop consisting of the external inductor (10 mH choke), timing capacitor $C_3$ (2.2 µF), and Pin 7 (internal discharge NPN transistor) carries high $dI/dt$ and can radiate EMI. Traces must be kept as short and direct as possible over a continuous ground plane to prevent slot antenna radiation.
2. **High-Impedance Sense Node Isolation:** Pins 2 (Trigger) and 6 (Threshold) exhibit high input impedance (> $10^{12}\,\Omega$). These traces must be kept away from high-current switching nodes (Pin 3 output and power traces) to avoid capacitive crosstalk and false frequency triggering.
3. **Reset Pin (Pin 4) Tie-Off:** Reset must be tied directly to +9V with a low-inductance connection to prevent inductive voltage spikes from triggering false resets.
4. **Control Voltage Pin (Pin 5) Treatment:** Unused Pin 5 must have a deliberate constraint (either a 10 nF decoupling capacitor to ground or an explicit no-connect rule) to prevent floating noise pickup into the internal 2/3 $V_{CC}$ comparator threshold.
5. **Channel-to-Channel Isolation:** Dual channels (Channel A and Channel B) are physically separated by > 20 mm with an intervening ground copper pour to suppress mutual inductive coupling and injection locking.

---

### Block 3: Audio Output & Acoustic Transducer Driver (Pin 3 Totem-Pole, DC Blocking C5/C10, Speakers J3/J5)
1. **DC Bias Blocking:** A 10 µF electrolytic coupling capacitor blocks the 4.5 V average DC quiescent bias of the 555 totem-pole output square wave, preventing continuous DC current from heating and damaging the 8 Ω speaker voice coil.
2. **Dynamic Return Currents:** Driving an 8 Ω speaker from a 9 V rail can generate peak instantaneous current pulses of $\approx \frac{9\text{ V}}{8\,\Omega} \approx 1\text{ A}$. The return pins of connectors J3 and J5 are tied directly to the low-impedance ground plane with thermal relief pads.
3. **Speaker Current Protection Consideration:** While the raw 555 is rated up to 200 mA output current (sufficient for low-volume audio demonstration), an industrial or consumer product requires a series current-limiting resistor (47–100 Ω) or an external BJT transistor buffer (e.g. 2N2222 / 2N3904) to avoid thermal overload of the 555 totem-pole driver.
4. **Connector Location & Polarity Silkscreen:** Placed along the upper edge of the board with explicit silkscreen polarity markings (`+`, `-`) and channel labels (`SPK_A`, `SPK_B`).

---

### Block 4: Ground Plane Architecture & EMI/EMC Mitigation
1. **Continuous Double-Sided Ground Planes:** Both Front Copper (`F.Cu`) and Back Copper (`B.Cu`) have solid flooded copper pours assigned to the GND net. This provides ultra-low impedance return paths for all signal tracks and drastically reduces radiated loop areas.
2. **Thermal Relief Spokes:** All through-hole ground pads connect to the planes using 4-spoke thermal reliefs (0.50 mm spoke width, 0.35 mm thermal gap) to facilitate proper heat concentration during soldering without sinking excessive heat into the plane.
3. **No 90° Bends / Acid Trap Prevention:** All trace turns strictly follow 45° chamfered miters. No 90° right angles or acute corners (< 90°) are permitted, preventing acid traps during PCB etching and microstrip impedance discontinuities.

---

### Block 5: Mechanical Constraints & Manufacturability (DFM)
1. **Precise Board Dimensions & Edge Setback:** Exact $90 \times 70\text{ mm}$ rectangular outline on `Edge.Cuts` with a minimum $0.50\text{ mm}$ copper-to-edge clearance along the perimeter to prevent copper delamination during panel V-scoring or routing.
2. **Symmetrical M3 Mounting Holes:** 4x 3.2 mm diameter mounting holes (`H1`..`H4`) located at $(105, 105)$, $(185, 105)$, $(105, 165)$, $(185, 165)$ with $6.0\text{ mm}$ copper and silkscreen keepouts to safely accommodate standard M3 screw heads and washers.
3. **Silkscreen Legibility & Clearances:** Silkscreen font height $\ge 0.85\text{ mm}$, line thickness $0.12\text{ mm}$, placed strictly outside exposed copper pads and component courtyards to prevent solderability defects.

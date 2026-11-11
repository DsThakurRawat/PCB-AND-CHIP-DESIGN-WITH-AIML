# PCB Design Errors: What Humans and AI Tools Get Wrong

*A catalogue of mistakes made by people, by AI tools, and by both working together, with the quickest way to catch each one. Companion to the PCB Design Rules file.*

## How to use this document

Every error has an ID, a severity, and a short *Catch it* note.

- **H-xx**: errors people typically make.
- **A-xx**: errors AI tools typically make.
- **S-xx**: shared errors that come from how people and AI tools work together.

**Severity.** Critical means a dead board, a safety hazard, or a wasted fabrication order. Major means the board works badly, is unreliable, or needs a respin. Minor means cost, convenience, or polish.

**Scope.** “AI tools” covers chat assistants (LLMs), AI schematic and layout generators, autorouters and auto-placers, footprint and library generators, and AI review or simulation helpers. This is a catalogue of failure modes, not a measurement of how often each one happens. Tools differ and keep changing, so test any tool on a small, known design before trusting it.

## Part 1: Errors humans make

### Requirements and planning

- **H-01 Vague requirements (Major).** Layout starts without voltage, current, speed, size, environment, and standards defined. *Catch it:* a one-page requirements list, reviewed before schematic capture.
- **H-02 Fab limits ignored (Major).** Trace, space, drill, or annular-ring values the fab cannot build, or the fab chosen after layout. *Catch it:* load the fab’s rules into DRC on day one.
- **H-03 Wrong layer count or stackup (Major).** Two layers for a fast or noisy design, or impedance calculated without the fab’s real stackup. *Catch it:* agree the stackup with the fab before placement.
- **H-04 Late mechanical decisions (Minor).** Connectors, holes, and outline fixed after layout is done. *Catch it:* import the enclosure drawing before placing parts.
- **H-05 Part availability ignored (Major).** Out-of-stock, end-of-life, or single-source parts. *Catch it:* check stock and lifecycle during schematic design.

### Schematic

- **H-06 Wrong pinout or pin function (Critical).** Pin number confused with function, swapped TX and RX, wrong enable polarity. *Catch it:* a second person checks every IC pin against the datasheet.
- **H-07 Floating or unconnected pins (Critical).** Missing power pins, floating inputs, forgotten reset, boot, or enable lines. *Catch it:* ERC plus a pin-by-pin walkthrough.
- **H-08 Missing pull-ups or pull-downs (Major).** I2C, open-drain, reset, and boot-mode lines. *Catch it:* search each datasheet for pull-up and pull-down requirements.
- **H-09 Logic level mismatch (Critical).** A 5 V output into a 3.3 V input, or thresholds that do not line up. *Catch it:* compare output levels against input thresholds and absolute maximums for every connection.
- **H-10 Ratings not derated (Major).** Capacitor voltage, ceramic capacitance loss under DC bias, resistor power, connector current, inductor saturation. *Catch it:* review every passive against worst-case conditions.
- **H-11 Missing protection (Critical).** No reverse-polarity, ESD, overcurrent, or inrush protection on exposed inputs. *Catch it:* list every external connector and ask what happens when it is misused.
- **H-12 Regulator support parts wrong (Major).** Wrong feedback divider, inductor, or output capacitor, including ESR limits on some LDOs. *Catch it:* recompute with the datasheet equations and compare with the reference design.
- **H-13 Power sequencing ignored (Major).** Rails that must start in order, or brown-out and reset behavior unchecked. *Catch it:* read the datasheet’s sequencing section.
- **H-14 Warnings waived, nets unclear (Minor).** ERC warnings dismissed without a reason, auto-named nets, no test points. *Catch it:* every waiver gets a written reason; name nets by function.

### Footprints and parts

- **H-15 Wrong footprint (Critical).** Generic or unverified land pattern, wrong pad size or pitch. *Catch it:* compare with the datasheet land pattern and print the layout 1:1.
- **H-16 Pin 1 or polarity wrong (Critical).** Mirrored connectors, connectors viewed from the wrong side, reversed diodes or electrolytic capacitors. *Catch it:* check pin 1 and polarity on every polarized part.
- **H-17 Thermal pad or paste mask wrong (Major).** Poor solder joints or shorted pads. *Catch it:* follow the datasheet’s paste and via recommendations.
- **H-18 Hole size wrong (Major).** Through-hole drill too small for the pin or too loose to solder well. *Catch it:* pin diagonal plus clearance and fab tolerance, checked against the datasheet.
- **H-19 3D model trusted as proof (Minor).** A good-looking model sits on a wrong footprint. *Catch it:* the 3D view checks fit, not pad correctness.
- **H-20 Package does not suit assembly (Minor).** 0201 parts for hand soldering, or BGAs with no inspection option. *Catch it:* confirm packages with the assembler.

### Placement

- **H-21 Decoupling far from pins (Major).** *Catch it:* check the loop from pin to capacitor to ground via.
- **H-22 Noisy and sensitive circuits together (Major).** Switchers, drivers, or relays beside ADCs, sensors, or RF. *Catch it:* mark noisy zones on the floorplan.
- **H-23 Crystal placed badly (Major).** Far from the IC, or with signals routed beneath it. *Catch it:* follow the crystal vendor’s layout guide.
- **H-24 Heat ignored (Major).** Hot parts beside heat-sensitive parts or electrolytic capacitors. *Catch it:* estimate power loss per part before placing.
- **H-25 No room for rework (Minor).** Parts too close to each other or to the edge; probes and irons cannot reach. *Catch it:* 3D view plus the assembler’s spacing rules.
- **H-26 Connector or mounting hole misplaced (Critical).** Wrong side, wrong orientation, or misaligned with the enclosure. *Catch it:* overlay the mechanical drawing.

### Power, ground, and safety

- **H-27 Traces too thin, too few vias (Major).** Overheating or voltage drop on power paths. *Catch it:* IPC-2221 or IPC-2152 calculator; several vias at power layer changes.
- **H-28 Broken ground plane (Major).** Slots and splits under signals, long or thin ground connections, return currents forced into large loops. *Catch it:* view the plane layer for gaps under fast nets; use short, direct ground vias.
- **H-29 Switching regulator layout wrong (Major).** Large hot loop, feedback near the switch node, noisy ground. *Catch it:* copy the vendor’s evaluation board layout.
- **H-30 Thermal path missing (Major).** No copper or thermal vias for hot parts; open vias in pads wick solder away. *Catch it:* thermal estimate; cap, fill, or move vias in pads.
- **H-31 Creepage and clearance too small (Critical).** Mains or high-voltage areas laid out by guess. *Catch it:* take distances from the applicable standard and get a qualified review.

### Routing and signal integrity

- **H-32 Impedance not controlled or not specified (Major).** *Catch it:* put target impedances and the stackup in the fab notes.
- **H-33 Pairs and buses unmatched (Major).** Skew in differential pairs, DDR, and parallel buses. *Catch it:* run length reports against the interface limits.
- **H-34 Crosstalk, stubs, and sharp corners (Major).** Long parallel runs, stubs, poor topology, acute angles. *Catch it:* apply spacing and topology rules; review high-speed nets by eye.
- **H-35 Return path broken (Major).** Fast signals cross plane gaps or change layers with no nearby return via. *Catch it:* trace the reference plane along each fast net.
- **H-36 Analog next to digital (Major).** *Catch it:* clearance rules for analog net classes.
- **H-37 Termination missing (Major).** *Catch it:* follow the interface spec or part datasheet.
- **H-38 RF keep-outs ignored (Major).** Metal or traces inside an antenna or module keep-out. *Catch it:* mark vendor keep-outs as rule areas.

### EMC and ESD

- **H-39 ESD protection misplaced (Major).** Far from the connector, or missing. *Catch it:* place it at the connector with a short path to ground.
- **H-40 Large loops and unfiltered cables (Major).** Fast edges where they are not needed. *Catch it:* review loop areas; slow edges with series resistors.
- **H-41 No room to fix EMI later (Minor).** *Catch it:* reserve footprints for filter parts.

### Manufacturing, assembly, and test

- **H-42 DRC skipped or errors waived (Critical).** *Catch it:* DRC with the fab’s rules and zero unexplained errors.
- **H-43 Output files not reviewed (Critical).** Missing layer, wrong drill units, wrong outline, wrong finish or thickness. *Catch it:* open Gerbers and drill files in an independent viewer.
- **H-44 BOM errors (Major).** Wrong part number or package, missing lines, wrong quantity. *Catch it:* cross-check the BOM against schematic and footprints.
- **H-45 Rotation and offset wrong (Major).** Parts assembled turned 90 or 180 degrees. *Catch it:* preview the placement file with the assembler.
- **H-46 Silkscreen and assembly aids (Minor).** Text on pads, unreadable labels, missing polarity marks, no fiducials or panel features. *Catch it:* review silkscreen layers; ask the assembler for requirements.
- **H-47 No test access (Major).** No test points or debug header. *Catch it:* write the bring-up plan before layout ends.
- **H-48 Unbalanced copper or pads (Major).** Board warps; small passives tombstone. *Catch it:* symmetric stackup, balanced pours, and symmetric pad connections.

### Process and human factors

- **H-49 No independent review (Major).** Self-review misses what the author already believes. *Catch it:* a second person reviews against a checklist.
- **H-50 Reference design copied without understanding (Major).** Values and layout do not fit your conditions. *Catch it:* list every difference between your design and the reference.
- **H-51 Schedule pressure (Major).** Checks skipped to save time. *Catch it:* a release checklist that cannot be skipped.
- **H-52 Wrong revision sent to the fab (Critical).** *Catch it:* version control and tagged releases.
- **H-53 Confirmation bias (Major).** Believing your own work because you made it. *Catch it:* check against sources, not impressions.

## Part 2: Errors AI tools make

### Chat assistants (LLMs)

- **A-01 Invented facts (Critical).** Fabricated pinouts, part numbers, ratings, or footprints, stated confidently. *Catch it:* verify every value against the datasheet and require a source.
- **A-02 Wrong part variant or datasheet revision (Critical).** Mixes up suffix variants that have different pinouts or voltage limits. *Catch it:* confirm the exact part number and datasheet revision.
- **A-03 Unit and arithmetic errors (Major).** mil versus mm, mA versus A, ounces of copper versus microns, wrong formula for trace width, dividers, or impedance. *Catch it:* recompute with a calculator or script.
- **A-04 Fake citations (Major).** Standards clauses or datasheet pages that do not exist. *Catch it:* open every cited source.
- **A-05 Generic advice on a specific part (Major).** “One 100 nF per pin” where the datasheet specifies a particular network. *Catch it:* the datasheet overrides general rules.
- **A-06 Guessing missing inputs (Major).** Assumes voltage, frequency, or environment instead of asking. *Catch it:* give requirements up front and ask the tool to list its assumptions.
- **A-07 Overconfidence (Major).** No uncertainty flagged on safety, EMC, or thermal questions. *Catch it:* treat output as a draft and ask what could be wrong.
- **A-08 Incomplete lists (Major).** Leaves out items such as ESD, sequencing, or thermal because the prompt never mentioned them. *Catch it:* compare against a checklist.
- **A-09 Drift in long sessions (Major).** Changes net names, pin assignments, or values, and forgets earlier constraints. *Catch it:* keep constraints in a file and compare each output against it.
- **A-10 Plausible but wrong scripts (Major).** Netlist or CAD scripts that run but connect the wrong pins. *Catch it:* run ERC on generated output and review the diffs.
- **A-11 Agreeing with a wrong plan (Major).** Goes along with the user’s confident but flawed choice. *Catch it:* ask for failure modes and the strongest argument against the design.
- **A-12 Misreading images (Major).** Small text and dense routing in screenshots get misread. *Catch it:* provide machine-readable files (netlist, DRC report), not only images.

### Autorouters and auto-placers

- **A-13 Routes by connectivity, not electrical intent (Major).** Stubs, unequal lengths, bad return paths, acute angles. *Catch it:* route critical nets by hand and check them against signal-integrity rules.
- **A-14 Net classes missing (Major).** Power routed with signal-width traces. *Catch it:* define net classes before routing.
- **A-15 Planes cut up (Major).** Excess vias and tracks perforate ground planes, and slots appear under fast signals. *Catch it:* inspect the plane layers.
- **A-16 Too many layer changes (Major).** Extra vias, with no return vias beside signal vias. *Catch it:* review via count and return paths on critical nets.
- **A-17 Placement optimizes wire length, not function (Major).** Decoupling far from pins, noisy parts beside sensitive ones, heat sources clustered. *Catch it:* lock critical parts and set placement constraints.
- **A-18 DRC-clean but no margin (Major).** Routes at absolute minimum spacing, lowering yield. *Catch it:* set preferred rules above the fab’s minimums.
- **A-19 Unrouted nets hidden (Major).** Leaves nets incomplete or ignores ratsnest lines. *Catch it:* run a connectivity check on the final file.
- **A-20 Keep-outs not respected (Major).** Antenna, mechanical, and thermal zones are ignored unless encoded. *Catch it:* define keep-outs as rule areas.
- **A-21 Hard to debug and rework (Minor).** No test access or probing room. *Catch it:* reserve test points before auto-placement.

### Generative schematic and layout tools

- **A-22 Plausible but wrong topology (Critical).** A generated design is missing a feedback network, bootstrap capacitor, compensation, or pull-ups. *Catch it:* compare against the vendor reference design.
- **A-23 Reference values not adapted (Major).** Copies an example without adjusting to your input voltage, current, or frequency. *Catch it:* recalculate every value for your conditions.
- **A-24 Learns bad habits (Major).** Reproduces common hobby-board practices, such as split ground planes. *Catch it:* review against the PCB Design Rules file.
- **A-25 Unaware of your fab or stackup (Major).** Assumes generic settings. *Catch it:* supply fab rules and stackup as inputs.
- **A-26 Non-reproducible results (Major).** Same prompt, different board. *Catch it:* log prompts and settings, and keep every version in version control.
- **A-27 Neat but wrong (Major).** Visual polish hides electrical errors. *Catch it:* judge by checks and calculations, not appearance.

### Library, footprint, and BOM tools

- **A-28 Wrong generated footprint (Critical).** Pad dimensions, pitch, or pin numbering wrong, often from datasheet table or unit misreads. *Catch it:* compare with the land pattern drawing and print 1:1.
- **A-29 Symbol, footprint, and part mismatched (Major).** A footprint for a different package variant. *Catch it:* check the part-number-to-footprint mapping.
- **A-30 Unsafe “equivalent” parts (Major).** Substitutes differ in voltage rating, tolerance, dielectric, height, or pinout. *Catch it:* compare key parameters line by line.
- **A-31 Datasheet extraction mistakes (Major).** Typical confused with maximum, footnotes missed, table rows misaligned. *Catch it:* read the original table and its notes.
- **A-32 Stale stock and price data (Minor).** *Catch it:* recheck with the distributor before ordering.

### Simulation and review helpers

- **A-33 Wrong model inputs (Major).** Wrong stackup, dielectric constant, or idealised parts produce authoritative-looking results. *Catch it:* validate inputs and cross-check with the fab’s impedance calculator or a field solver.
- **A-34 “DRC clean” treated as “correct” (Major).** Checkers know rules, not intent. *Catch it:* human review of intent, plus functional tests.
- **A-35 False alarms and misses in AI review (Major).** Flags non-issues, misses real ones, and lacks context. *Catch it:* use it to supplement human review, never to replace it.

## Part 3: Errors shared by people and AI tools

- **S-01 Trusting without verifying (Critical).** People trust AI output, AI trusts the user’s inputs, and both trust the tool report. *Catch it:* every claim traces to a datasheet, a calculation, or a check.
- **S-02 Wrong inputs, polished output (Critical).** Wrong requirements or the wrong datasheet revision produce a neat but wrong design. *Catch it:* review the inputs before reviewing the outputs.
- **S-03 Constraints not written down (Major).** Net classes, stackup, keep-outs, and rules live in someone’s head or a chat, so both guess. *Catch it:* keep a machine-readable constraints file.
- **S-04 Changes after checks (Major).** A late change or an AI regeneration goes in after review. *Catch it:* rerun ERC, DRC, and review after every change.
- **S-05 Unit and convention mix-ups (Major).** mil versus mm, connector view direction, pin numbering, and rotation conventions between CAD and assembler. *Catch it:* state conventions in the project notes and verify them with one test part.
- **S-06 Shared blind spots (Major).** Power sequencing, tolerance stack-up, thermal, ESD, and manufacturing quirks that nobody checks. *Catch it:* use a checklist built from standards and past failures.
- **S-07 Incomplete handoff (Major).** Missing fab notes for impedance, stackup, and finish, or output files that disagree. *Catch it:* a release package checklist.
- **S-08 No traceability (Major).** No record of who or what made a change, or why. *Catch it:* version control, a change log, and a prompt log.
- **S-09 Safety treated like any other rule (Critical).** Mains, medical, automotive, and battery designs without qualified review. *Catch it:* named expert sign-off and accredited testing where required.
- **S-10 No prototype or bring-up plan (Major).** Errors are found in volume production. *Catch it:* a small first batch and written bring-up steps.

## Part 4: How human and AI errors differ

- **People** tend to make slips (a swapped pin, a typo in a value) and have knowledge gaps. Fatigue, haste, and habit play a large role. People usually know when they are unsure and can ask.
- **AI tools** tend to make plausible-looking errors: confident inventions, inconsistency over long work, and generic answers where specifics matter. They know nothing about the physical board unless given its data, and they rarely signal doubt.
- **Both** are weakest on rare parts, unusual constraints, and anything missing from a checklist.

What this means for review:

- Aim human review at facts: pins, footprints, ratings, polarity, and calculations.
- Aim automated checks at consistency: BOM versus schematic versus footprints, ERC, DRC, and unrouted nets.
- Use AI to catch human slips such as missed checklist items, inconsistent names, and missing pull-ups, but verify what it reports.

## Part 5: A workflow that catches both

1. Write the requirements and a machine-readable constraints file (stackup, net classes, keep-outs, fab rules).
2. Treat datasheets and verified libraries as the only source of truth.
3. Let AI draft in small steps, one block or net class at a time, and review each step.
4. Run automated checks: ERC, DRC with the fab’s rules, BOM-to-schematic-to-footprint consistency scripts, and an unrouted-net check.
5. Have an independent person review the high-risk items: pins, footprints, power, protection, and polarity.
6. Verify numbers with a separate tool: trace-width and impedance calculators, thermal estimates, and simulation.
7. Review the release files: Gerbers and drill files in an independent viewer, BOM, placement file, 3D view, and a 1:1 paper print.
8. Order a small prototype run, follow the bring-up plan, and record what went wrong so the checklist improves.

## Part 6: Top checks before ordering

- Every footprint matches its datasheet land pattern.
- Pin 1 and polarity are verified on every polarized part.
- Every IC pin function is checked against the datasheet.
- No floating inputs, and all power pins are connected.
- Voltage levels are compatible and ratings are derated.
- Protection is in place at every external connector.
- Power trace widths and vias are checked for current.
- The ground plane is unbroken under fast signals.
- DRC is run with the fab’s rules and has zero unexplained errors.
- Gerbers and drill files are viewed in an independent tool.
- BOM, part numbers, and placement rotations are checked.
- Anything AI-generated is traced to a source and signed off by a person.

*This list is general guidance. It does not replace datasheets, fab capability documents, safety and EMC standards, or review by a qualified engineer.*

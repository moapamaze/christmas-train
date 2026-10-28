C5 has a concrete custom coach-truck development layout and reproducible mechanical screens. The current mass allowance is **2,000 kg complete / 1,400 kg unsprung per truck**. The earlier 1,800/1,200 comparison is explicitly superseded. Final CAD audit and mass reconciliation are recorded separately; no completed suspension, axle fatigue, brake fit or operating envelope is claimed.

| Coil item | Regular coach | Accessible coach |
|---|---:|---:|
| Upper coach mass | 13,200 kg | 11,000 kg |
| Sprung mass per truck | 5,200 kg | 4,100 kg |
| Coil load at upper mass | 6.37432 kN | 5.02591 kN |
| Free height for 250 mm installed | 293.04324 mm | 283.93794 mm |
| Wahl stress: static / 35 mm bump | 354.96 / 643.59 MPa | 279.87 / 568.50 MPa |
| Normal rebound proposal | 40 mm | 30 mm |
| Coil compression remaining at normal rebound | 3.043 mm | 3.938 mm |
| Seat separation at captured 60 mm droop | 16.957 mm | 26.062 mm |
| Ideal v=1 buckling compression / working maximum | 127.79 / 78.04 mm | 137.21 / 68.94 mm |

Each truck uses eight proposed coils: 18 mm wire, 100 mm mean diameter, seven active/nine total turns, and 148.0911 N/mm calculated rate with G=79 GPa. Nominal solid height is 162 mm; a 5% allowance makes 170.1 mm, leaving 44.9 mm at the 215 mm bump height. Scherdel's ideal v=1 buckling screen assumes lateral end restraint; the v=2 unrestrained cases fail before upper static load. Actual material, rate/height tolerances, guidance, corrosion, preset process and fatigue remain unselected. Spring engagement alone does not establish valid center-bearing contact during rebound.

At 35 mm bump, spring loads reach 1.813/2.031 times upper static load. Regular springs therefore cannot carry a 2× force at that travel without stop reaction; accessible springs reach that ideal force just before the stop. Neither result validates stop energy or dynamic loads. Captured droop is a retention configuration, not a spring-engaged boarding state.

The represented nonbody truck is 1662.01 kg. Adding the explicit 200 kg omitted-OEM-brake allowance gives 1862.01 kg, leaving 137.99 kg within the 2,000 kg development allowance. Moving components plus half the link mass and the same brake allowance total 1291.71 kg; coil participation and other incomplete items remain to reconcile. Body-attached hardware is 62.41 kg per truck and must be counted once in the separate body budget. Its inclusion in the old tare budget remains unresolved. Using 100 kg per OEM brake instead of 50 kg would exceed the complete-truck allowance by 62.01 kg.

Subtract complete truck mass for body-support force and only unsprung mass for primary-coil force. The old coach tare allocations remain unreconciled. Parallel updated tare adds 1,000 kg for two truck allowances increasing from 1,500 to 2,000 kg; accessible adds another 50 kg only if its old 130 kg folding pair becomes C31's 180 kg pair. Both folding assemblies remain aboard in every mode.

| Coach | Mass case | Gross kg | Equal body center kN/truck | Floor above rail mm |
|---|---|---:|---:|---:|
| regular | legacy tare unreconciled | 7,040 | 14.906 | 838.295 |
| regular | parallel tare sensitivity | 8,040 | 19.809 | 834.156 |
| regular | upper design load | 13,200 | 45.111 | 812.800 |
| accessible | legacy tare unreconciled | 7,535 | 17.333 | 827.141 |
| accessible | parallel tare sensitivity | 8,585 | 22.482 | 822.795 |
| accessible | upper design load | 11,000 | 34.323 | 812.800 |

The proposed normal equal-heave floor ranges are 777.8–852.8 mm regular and 777.8–842.8 mm accessible. They are not allowed boarding-height ranges. At the C4 threshold point X30,Y−52.25 in about pitch reference X153, ±1° roll adds 0.912 in and ±1° pitch adds 2.147 in. The combined probe already exceeds C4's 2.5 in height condition before heave. Station height and a permitted immobilized boarding condition remain open.

The current sidebearer envelope is 100×50×50 mm with a 1,000 N/mm target, zero running gap and ±0.5 mm shim/preload sensitivity. It needs an effective compression modulus of 10 MPa to meet that rate; no supplier material curve is selected. At ±2° about spherical center Z830.7, contact plane Z470.7 and Y500, geometric closure is 17.67 mm. The CAD procurement target is 20 mm stroke. A volume-conservation probe at 20 mm compression expands the block to 129.10×64.55 mm under equal biaxial strain; actual constrained bulging, pressure, fatigue and friction remain to validate.

The coupled model solves a shared rigid-body roll angle, two truck-frame angles, unilateral pads, gravity moment and all eight wheel reactions. CG height 0.5/1/1.5 m above the actual roll center, CG offset 0/100 mm, lateral acceleration 0/0.4 m/s² and rail crosslevels are sensitivity inputs, not accepted conditions.

| Coupled case at 1,000 N/mm | Numerical result | Interpretation |
|---|---|---|
| Legacy regular tare 7,040 kg, centered CG 1 m high, opposed ±40 mm mean truck crosslevels | Body roll 0°; relative roll ±1.541°; pad 13.450 mm; each center 1.456 kN | Center remains compressive in this specific diagnostic. |
| Same coach, both trucks +40 mm | Body roll 2.630°; relative roll 0.157°; center 13.538 kN | Absolute body roll differs from relative joint roll. |
| Updated accessible tare 8,585 kg, opposed ±40 mm | Center 9.032 kN; pad 13.450 mm | Tare changes center retention. |
| Worst combined empty contact probe | Center -4.445 kN; relative 2.160°; pad 19.351 mm | Negative center invalidates the maintained-contact solution. No catcher capacity is inferred. |
| Worst wheel probe including differential twist | Eight wheel reactions kN: [16.14, 1.12, 11.198, 6.061, 8.967, 8.293, 4.025, 13.235] | Positive wheel force is not an unloading acceptance criterion; contact may already be invalid. |
| Largest combined compression probe | Relative 4.495°; pad 38.723 mm | Exceeds the proposed joint/stroke range. |

The flat legacy-regular local restoring slope is 293.0 kN·m/rad. Separate ideal lower/upper stiffness inequalities are recorded in the JSON, but they do not define a common accepted operating window: combined CG, acceleration, twist and tolerance cases still fail. Negative forces are not clamped. Maximum axle-to-box bearing angle in the combined sensitivity sweep is 3.030°, above the catalog’s conditional 2° guideline; those combined cases are outside the proposed geometry/support range. Actual nonlinear pads, friction, body torsion, damping and stop/catcher redistribution are omitted.

At twice the 45.111 kN equal body-center load, the 200×160×12 fabricated crossbeam gives 54.08 MPa over 1,076 mm clear span, or 62.32 MPa over the conservative 1,240 mm spring-center span. Two 12 mm sideframe webs with 200 mm credited gross depth give 84.58 MPa. These are uniform simply supported gross-section probes; local openings, drop shape, pad-base recesses, load introduction, plate buckling, welds and fatigue are excluded. A ±500 mm body CG shifts the upper regular center maximum to 53.333 kN; the corresponding 2×/3× attachment probes are 106.666/159.999 kN. Lift-retention probe is 39.227 kN per truck, not an operational uplift limit.

Outboard brake relocation avoids a known local girder conflict but lengthens the axle load path. For a 200 mm torque arm, 500 mm link-force overhang and 100 kg brake mass at 560 mm, an 80 mm shaft's nominal combined stress is 22.0/53.8/105.8/316.0 MPa at torque probes 0.364/1/2/6 kNm; a 90 mm stem gives 15.5/37.8/74.3/221.9 MPa. This omits wheel-load bending, bearing-seat transitions, threads, fits, shocks and rotating fatigue. Actual maximum D1 torque and the hub torque joint remain open. The 500 mm link closure calculation is planar; spherical eyes still need a full axle-tilt check.

SKF 22218 E is 90×160×40 mm with shaft abutment at least 101 mm, housing opening at most 149 mm and fillet at most 2 mm. Proposed outboard 22216 E is 80×140×33 with corresponding 91/129/2 mm limits. A removable 96 mm thrust spacer permits the main bearing to install over the 90 mm maximum stem. Fits, bearing clearance, seals, load distribution and life remain open. The SKF catalog ratings are not permitted vehicle loads. General minimum equivalent load for each 22216 E is 2.7 kN; the low-speed oil-lubricated formula gives 0.81 kN. Coasting carrier loads may be lower, so minimum-load/skidding and lubricant suitability remain application holds.

At ±7° yaw and 5,486.4 mm pivot spacing, ideal centerline geometry needs radius at least 22.51 m/73.85 ft. The earlier 50 ft curve needs about 10.37° and redesign. Actual route, wheel profile, back-to-back, contact spacing, wear and flange behavior remain unselected. The 480 mm wheel-contact halfspan used in force calculations is a proxy, not half the 914.4 mm gauge.

Primary sources: [SKF printed pages 24–27](https://www.skf.com/binaries/pub12/Images/0901d196808a4ad1-Spherical-roller-bearings_18406-EN_tcm_12-480491.pdf), [Scherdel page 7](https://federfibel.scherdel.com/English/90_Druckversion/compression_springs.pdf), and [Lee Spring design considerations](https://www.leespring.com/sites/default/files/pdf/Lee%20Spring%20-%20WhitePaper%20-%20Spring%20Design%20General%20Consideration_US.pdf). Retained D1 Dexter parts establish a brake family, not actual mating dimensions, whole-package clearance or maximum torque. Precise external interfaces do not prevent continued custom development, but no fabrication or operation release is asserted.

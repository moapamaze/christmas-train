# Reviewer Cover Memo — PF-CT rev L4.2

To: Reviewing Professional Engineer (Nevada) · From: Pulsipher Farms owner team · Date: 28 Oct 2026

[[STAMP]]

## Purpose
We request review and, if acceptable, stamping of the design calculations and drawings for the Pulsipher Farms Christmas Train (36 in gauge, 6 mph governed maximum - an owner-selected limit we ask you to confirm - track designed LEVEL (Layout F 0.0 %), vehicles checked at a conservative 2 % grade, 100 m min. radius). The package was prepared in-house; every supplier value we do not hold is marked AWAIT and every engineering choice not dictated by a code is marked ASSUMED so you can see what to verify.

## Package contents
| Doc | File |
|---|---|
| Calculation package (numbered index, 12 subsystems, fix log) | calcs/PE/PF-CT_PE_calc_package.pdf |
| Drawing set (sheet index on G-001, rev L4.2) | drawings/PF-CT_R2_drawing_set.pdf |
| Design basis | calcs/PE/PF-CT_design_basis.pdf |
| Assumptions & open items | calcs/PE/PF-CT_assumptions_open_items.pdf |
| L4 drive calc (source + JSON) | calcs/L4/drive_L4.py / .json; interfaces calcs/L4/loco_interfaces_L4.py / .json |
| L3 drive calc - fallback | calcs/L3/drive_L3.py / .json |
| L2 drive calc - rejected alternative | calcs/L2/gear_drive_L2.py / .json |
| Earlier calc notes C1-C16 | calcs/PF-CT_R2_calc_notes.pdf |
| CAD (STEP/GLB per assembly) | cad/ |

## Key results
- Drive L4: Poclain MS05 468/234 + RS120-2 chain 3:1 per axle, frame-mounted; 2% start 37.67 kN at 350 bar (η 0.90) vs 32.61 kN needed (~303 bar), equal-torque capped 37.11 kN dry (L4.1: no flow divider - electronic traction control); dry/sanded margin 1.10 with 2 × 75.4 kg front plates, wet unsanded 0.66 → sand MANDATORY; 2% hold 2.69 mph; chain utilization 0.68 of the maker allowable (SF 7.9 ultimate at HPRV).
- Speed: 6 mph GOVERNED (owner-selected - please confirm): H1P053 stroke stop sealed at 42 cc + hard 2,600 rpm limit + PLUS+1 + independent 2-channel 7 mph overspeed relay to emergency brake. Hardware capable of ~7.6 mph (margin only).
- Axle: Ø150 pressed sprocket seat, no keyway, no hardening credit, heaviest axle: Goodman n 1.57; press-fit slip SF 3.11.
- A roller chain in passenger rail traction is not a catalog rail application: Poclain AE and Tsubaki data are pending (Assumptions B1-B3).
- Brakes: emergency 0.632 m/s² net on 2% down; stop 9.7 m from the governed 6 mph, 12.4 m from the 7 mph trip (information: 22.5 m from 10 mph); service stop 13.4 m from 6 mph.
- Power: hot-humid demand 39.7 → 31.1 kW with RenewAire HE05IN ERVs (ε 0.55 ASSUMED) at plan OA, 27.7 kW at 62.1 OA, vs 35 kW continuous.
- Highest remaining utilizations: K2-fp 1.00; D4-mb 1.00; L42-k2 1.00; K2-m2 1.00; K2-a 1.00; D1-f 0.99.
- Unresolved failures: 0 (none live: K2-rD closed by gauge-face lubrication, K2-xf closed by the 50 mm cradle drop). Outside-basis sensitivity: D1-a2/D1-a2s/D1-s (2% on an uncompensated R100, margin 0.98). All other as-found failures have a logged fix - calc package App. C.

- Rev L4.2: loco 19934 kg, tender 8,706.5 kg (TB-3.13d), train 81513 kg; K2-a 25.89 kN of record; forward 2 % start margin 1.112; reverse full-train start limit 1.20 %; run-in worst 25.3 kN ≤ 33.2; strength cases at 430 bar (chain MBL spec ≥ 326 kN, 15T in 4140).
## What we ask you to decide
See Assumptions & Open Items Part A - chiefly the governed 6 mph limit, the roller-chain final drive in rail service, the load-case basis (F2291 vs IBC), brake criteria, axle fatigue method, parked wind and anchors, ADA and fire performance.

## Limits of this package
- Supplier-dependent items (Part B) must be closed with certified data before fabrication; drawings show envelopes for those items.
- No FEA was run; checks are hand calcs on conservative load paths. The PE may require FEA of the powered-truck sideframe/horn, the MS05 motor bracket/transom and the pressed-hub seat.
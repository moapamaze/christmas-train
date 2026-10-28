# PF-CT Calculation Package for PE Review — rev L4.2 (28 Oct 2026)

Pulsipher Farms Christmas Train · 36 in gauge diesel-hydraulic locomotive (8 × Ø1,450 drivers), tender T2, 4 coaches R2 · Logandale, Nevada

Status: PRELIMINARY - prepared by the owner team for review by a Nevada-registered PE. Not for construction until stamped. Supplier values not in hand are marked AWAIT; engineering choices not fixed by a code are marked ASSUMED for the PE to confirm or change.

[[STAMP]]

## Numbered index

| No. | Section | Calcs | Max util (excl. spec-requirement rows) |
|---|---|---|---|
| 0 | Design basis, masses, criteria | - | - |
| 1 | Locomotive frame and body | 21 | 0.95 |
| 2 | Trucks and suspension (powered, leading, tender/coach) | 9 | 0.53 |
| 3 | Axles and bearings | 10 | 0.97 |
| 4 | Drive (rev L4.1 Poclain MS05 2-speed + ANSI 120-2 chain 3:1, governed 6 mph) and hydraulics | 87 | 1.00 |
| 5 | Brakes - service, emergency, parking | 17 | 0.90 |
| 6 | Couplers, drawbars and end restraint | 25 | 0.96 |
| 7 | Tender T2 - structure, engine/pump/genset mounts, fuel, cooling | 8 | 0.94 |
| 8 | Generator sizing and selection recommendation | 5 | 0.90 |
| 9 | Coaches R2 - frame, body, roof, floor, doors, stairs, seating, restraint, egress | 27 | 0.71 |
| 10 | Electrical (train supply) and coach HVAC | 4 | 0.92 |
| 11 | Wind - 40 mph no-run, overturning, tie-downs | 11 | 0.86 |
| 12 | Track / rail interface - wheel profile, gauge, curve clearances | 33 | 1.00 |
| A | Fastener torque schedule | - | - |
| B | Weld schedule | - | - |
| C | Fix log (failures found and how they were fixed) | - | - |
| D | Revision history | - | - |

Total calculation rows: 257. Utilization = demand / capacity (for FS rows: required / available). Rows that failed as-found are kept, shaded, and marked with their fix. Rows with util = 1.00 and demand = capacity are specification-requirement rows (the minimum rating a supplier part must meet), not a check at its limit.
\pagebreak
## 0 Design basis (summary - full text in PF-CT Design Basis)

- Train mass (loaded, T2 tender, L4 drive): 81,513 kg; W = 799.4 kN. Loco 19,934 kg (L4.2: safety-chain parts 32.2 kg (2 × PL44.5 A572-50 lugs faced to 42.5 in the jaw zone + PL16 diaphragms, 1-1/8 in G-2130 shackles, Crosby S-1325A couplers; X11150; replaces the PL40 10.2 kg), Ø120 traction pins + GE120ES-class housings +2 × 22 kg (X4075/7275), sanders on both trucks (rear boxes 46 kg body-mounted X6400 + 8 kg nozzles X7275, front upgrade 6 kg), float bypass block 14 kg, T04 orifices / 2-channel vent switch / 96-tooth pony wheel 7 kg, brake-release piping 38.5 kg GROSS (Loco Bot E7, replaces the 5.0 kg net), MR feed JL-A→BP-1 11 kg (X8190), 20 L release reservoir 14 kg; L4.1: + T04 release circuit rev (6.0 L + 1.0 L accumulators, hand pump, shuttles; steering 7) 20 kg X5675, + low traction pins 2 × 55 kg (X4075/7275, ASSUMED), Loco Bot close-out 21.3 kg (saddle gussets 12.7, SD-1 caps 3.2, SD-2 clamps 5.4), + HL-1 headlamp 25 kg (upper bound) X175, TC/valve package 28 kg X5675, ballast clamp bars 21.1 kg X4075, hub 31.4 kg/axle (Ø350 flange), Loco Bot ledger 01:57 (barrel 2,076.2, saddles 195.7, bell 14.3, whistle 4.9, slats 21.9, L-107 -1.0); no flow divider. Loco = RT1-corrected base 16,657 (INCLUDES the L3 3 mm hood 898 kg) + L4 drive delta + Loco Bot shell ledger rev 2 (Steering 17): L-108 barrel 2,280.6 incl. saddles (S4N) - 898 hood, L-109 smokebox 227.9 IN FULL (the L3 smokebox front left with the ~1,000 kg L3 cab/front - no double count), L-110 fittings 51, L-107 P1-L net +28.2 + SS± HSS3x3x1/8 +9.1, cab L-111 C1 813.9 @X9283 replacing the ~1,000 kg L3 cab/front, fit-out 6, FT-1 15.6, BT-1 battery 68.2 in the Y- front pocket (base also INCLUDES the L3 PL6 deck 1,248) + front ballast plates trimmed 1,056 -> 150.8 (2 x 75.4); pilot slats 21.9 and JL plates 9.7 (ledger rev 2) + pony own ballast 1,250; jumpers 40 kg in train mass only; L4 drive delta +571 kg, part ASSUMED); tender 8,706.5; coaches 3 × 13,200 + 11,000 loaded.
- Driver adhesion weight 171.7 kN (lead truck 23.8 kN). μ dry 0.25 / wet 0.15 / sanded 0.25 (ASSUMED rail practice).
- Speed: GOVERNED 6 mph maximum operating speed - OWNER-SELECTED LIMIT (28 Oct 2026), PE TO CONFIRM; hard limit = H1P053 PUMP stroke stop sealed at 42 cc + HARD tamper-sealed 2,600 rpm engine limit (L4.2: 5.96 mph loaded, 6.47 mph no-load high-idle check < 7 mph trip) + PLUS+1; overspeed trip 7 mph by a 2-channel speed relay INDEPENDENT of PLUS+1 → emergency brake + pump neutral. Hardware is capable of ~7.6 mph with the stop removed - margin only, not permitted. Brakes, curve and passenger checks use 6 mph (trip case 7 mph).
- design grade 2% GOVERNING (max 2.0% on tangents, compensated on curves - route redline 28 Oct 2026); min. radius 100 m (design basis; R50 under study, see §12); gauge 914.4.
- Steel ASD: 0.6Fy bending/tension, 0.4Fy shear at ×1.3 service; Fy at ×2.0 exceptional. Welds E70, 0.3·Fu throat.
- Wind: 40 mph gust no-run; parked 100 mph 3-s gust (ASCE 7-22, ASSUMED - PE to take site value).

\pagebreak
## 1 Locomotive frame and body

### Governing codes and standards
- AISC 360-22 (ASD) for members and connections; AWS D1.1/D1.1M:2020 welding
- ASTM F2291-23 §6 (design loads, patron areas), F1193 (quality/manufacture), F770 (operations)
- IBC 2021 §1607 for walking-surface, guard and grab loads (reference only - PE to confirm applicability)

### Load cases and basis
- DL+equipment ×1.3 service vs 0.6Fy; ×2.0 overload (track irregularity / jacking) vs Fy
- Drawbar 70 kN service, 200 kN ultimate (pin/box/rail) - ASSUMED basis, see §6
- Ballast 3 g long. / 2 g vert. / 1 g lat. (ASSUMED, F2291 equipment restraint)
- Jacking: 2 × loco weight on 4 pads
- Cab roof 20 psf live + 300 lb point; treads 300 lb; grabs 200 lb

### Hand calculations

| ID | Check | Inputs | Formula | Demand | Capacity | Unit | Util | Status | Note |
|---|---|---|---|---|---|---|---|---|---|
| C4 | Loco main rail HSS12x6x3/8, vertical ×2.0 (uniform equivalent) | Sprung body 8439 kg (LT42 reactions) spread uniformly; overhang 3775 mm | see PF-CT_R2_calc_notes (calcs.py) | 90.1 | 345.0 | MPa | 0.26 | OK | Ballast sits directly over the front bolster, adds no frame moment. |
| C4b | Loco main rail at rear sill, drawbar 70 kN service + vertical ×1.3 | Eccentric drawbar: rail centroid Z1302 − coupler Z550 = 752 mm; moment shared by both rails via end sill + knee gussets | see PF-CT_R2_calc_notes (calcs.py) | 105.7 | 207.0 | MPa | 0.51 | OK |  |
| C4b | Loco main rail at rear sill, drawbar 200 kN ultimate + vertical ×1.3 | Eccentric drawbar: rail centroid Z1302 − coupler Z550 = 752 mm; moment shared by both rails via end sill + knee gussets | see PF-CT_R2_calc_notes (calcs.py) | 193.3 | 345.0 | MPa | 0.56 | OK |  |
| C8 | Loco body bolster box (PL12 flanges 350, PL10 webs, 305 deep), rear, ×2.0 | Rear body reaction 5873 kg (LT42) at centre plate, span 480 mm (rails Y±240, rev L1) | see PF-CT_R2_calc_notes (calcs.py) | 9.7 | 250.0 | MPa | 0.04 | OK |  |
| C8f | Loco front bolster with full 1.5 t ballast, ×2.0 | Ballast load lands on rails directly; conservative to put on bolster | see PF-CT_R2_calc_notes (calcs.py) | 6.7 | 250.0 | MPa | 0.03 | OK |  |
| C9a | Ballast pocket end wall PL20, 3 g longitudinal | 750 kg per side, resultant at mid-height of 255 mm stack; wall acts as cantilever 480 wide | see PF-CT_R2_calc_notes (calcs.py) | 87.6 | 150.0 | MPa | 0.58 | OK | 3 g longitudinal / 2 g vertical / 1 g lateral ASSUMED (engineer to set per ASTM F2291). |
| C9b | (Original idea) PL12 end wall, 3 g longitudinal | Shows why the end walls are PL20 | see PF-CT_R2_calc_notes (calcs.py) | 243.3 | 150.0 | MPa | 1.62 | FIXED - PL20 end walls (C9a) |  |
| C9c | Ballast hold-down 4× M20 cl. 8.8 rods, 1 g up + preload | Each rod tensile stress area 245 mm², proof 600 MPa; ASD limit | see PF-CT_R2_calc_notes (calcs.py) | 1,838.7 | 70,419.2 | N | 0.03 | OK |  |
| C10a | Cab step tread PL8 × 240, 500 span, 300 lb point | IBC 1607 stair tread 300 lb concentrated (ASSUMED code basis) | see PF-CT_R2_calc_notes (calcs.py) | 65.1 | 150.0 | MPa | 0.43 | OK |  |
| C10b | Cab step tread deflection | Limit L/240 | see PF-CT_R2_calc_notes (calcs.py) | 1.7 | 2.1 | mm | 0.81 | OK |  |
| C10c | Grab iron Ø32 solid A36, 1,200 span, 200 lb any direction | OSHA 1910.29 / IBC 1607.9 200 lb (ASSUMED code basis) | see PF-CT_R2_calc_notes (calcs.py) | 83.0 | 150.0 | MPa | 0.55 | OK |  |
| C10e | Cab roof purlin HSS2x2x1/8 @600, 20 psf live + dead | Span 2,700 mm simply supported | see PF-CT_R2_calc_notes (calcs.py) | 77.6 | 207.0 | MPa | 0.38 | OK |  |
| C10f | Cab roof purlin HSS2x2x1/8 deflection | Limit L/180 | see PF-CT_R2_calc_notes (calcs.py) | 11.6 | 15.0 | mm | 0.77 | OK |  |
| C10g | Cab roof purlin HSS3x2x1/8 @600 deflection (adopted) | Limit L/180 | see PF-CT_R2_calc_notes (calcs.py) | 4.4 | 15.0 | mm | 0.29 | OK |  |
| C10h | Cab roof purlin HSS3x2x1/8 @600 bending (adopted) |  | see PF-CT_R2_calc_notes (calcs.py) | 43.9 | 207.0 | MPa | 0.21 | OK |  |
| C16a | Cab clear headroom (deck to purlin underside) vs 6 ft 3 in crew + shoes | Roof top 3700 - 3 skin - 76.2 HSS3x2 purlin = 3621; cab floor PL6 top 1605; 6 mm floor mat | see PF-CT_R2_calc_notes (calcs.py) | 1,905 | 2,009.8 | mm | 0.95 | OK | 1,905 mm standing target ASSUMED (owner/crew to confirm) |
| C16b | Route overhead clearance adopted vs train height + 300 sway/bounce/track-lift + 300 decorations | Adopted R2: nothing lower than 4,300 mm above top of rail within 2,000 mm of track CL (lights, wires, signs, branches, arches) | see PF-CT_R2_calc_notes (calcs.py) | 4,300.0 | 4,300 | mm ARL | 1.00 | OK |  |
| L1-J | Jacking pad - bolster web local yielding (AISC J10.2), 2 webs PL10, lb 150 | P = 2·19,934 kg·g/4 pads | Rn/Ω = 2·Fy·tw·(5k+lb)/1.5, k=12 | 97.743 | 700.0 | kN | 0.14 | OK |  |
| L1-H1 | L-107 blind-bolt holes Ø26 in main-rail OUTER webs (24 holes, 6 stations) - fatigue stress range at the hole vs AISC App. 3 Cat D threshold | hole Z1360 (57.6 mm off the NA), Ix loss 0.93 % | Δσ = 2·0.3·σ_service(y_hole) | 10.3 | 48.0 | MPa | 0.21 | OK | APPROVED with conditions (edge/weld-toe rules, see Loco Bot review). C4 util with holes 0.262 |
| L1-H2 | L-107 RB-1 bracket: Hollo-Bolt HB16 per-bolt shear + tension, worst L7-B3 (Loco Bot bracket_load_table.csv, 3 g long.) | V 15.4 kN, T 8.9 kN per bolt (L7-B3 / L7-B2) | linear V/30 + T/21 ≤ 1 (Lindapter SWL, conservative) | 0.51 | 1.0 | interaction | 0.51 | OK | Web bearing 15.4 vs 72.6 kN (util 0.21); 28 of 30 holes approved, 2 end-sill holes rejected |
| L1-H3 | L-107 SD-1 bolster hold-down HB16 in PL12 bolster top (4 holes) - uplift | 5.99 kN per bolt | T/21 kN SWL | 5.99 | 21.0 | kN | 0.28 | OK | APPROVED if the holes move to Y±90 (≥ 50 mm from the rail-web weld toe). Optional 2 holes in the rear end sill (drawgear zone): REJECTED |

### Materials
- Main rails HSS12x6x3/8 ASTM A500 Gr C (Fy 345); sills, crossmembers HSS A500C
- Bolster boxes, gussets, plates ASTM A36; drop box PL16 ASTM A572 Gr 50
- Cab/hood: 10 ga (3.4) A1011 CS skin on HSS2x2x1/8 posts; roof purlins HSS3x2x1/8 @600 (C10g/h)

### Welds (AWS D1.1, E70XX, prequalified WPS unless noted)
- Crossmembers to rails: 6 mm fillet all round (E70, D1.1 prequalified)
- Drop box to rails/sill: 10 mm fillet all round, 100% VT + MT (C5w)
- Bolster box seams: 6 mm fillet both sides; centre-plate ring 8 mm fillet all round

### Bolts and torques
- Ballast hold-down 4× M20 cl. 8.8 rods, 441 N·m (dry K 0.20) - C9c
- Cab-to-frame: M16 cl. 8.8, 219 N·m (dry K 0.20), Nord-Lock washers

### Fixes logged
- F13: ballast end wall PL12 → PL20 (C9b NG → C9a 0.58)
- F04/C16: cab roof 3,700, purlins HSS3x2x1/8 (deflection)
\pagebreak
## 2 Trucks and suspension (powered, leading, tender/coach)

### Governing codes and standards
- AISC 360-22 (ASD); AWS D1.1
- EN 13749:2021 load cases used as a method reference for truck frames (ASSUMED - PE to confirm)
- SMI Handbook of Spring Design / EN 13906-1 for coil springs

### Load cases and basis
- Vertical: sprung load ×1.3 service, ×2.0 exceptional (EN 13749 style)
- Lateral 0.35 × axle load at flange
- MS05 motor bracket on the transom: chain pull at the 430 bar strength basis (HPRV 380 + spike) + motor reaction torque (§4)

### Hand calculations

| ID | Check | Inputs | Formula | Demand | Capacity | Unit | Util | Status | Note |
|---|---|---|---|---|---|---|---|---|---|
| C3a | Coach truck transom 2×HSS10x4x1/4 upright, ×2.0 | P=46.5 kN at centre plate, span 1449 mm between sideframes | see PF-CT_R2_calc_notes (calcs.py) | 65.9 | 345.0 | MPa | 0.19 | OK |  |
| C3b | Coach truck sideframe PL25×170 A36, ×1.3 | Simply supported on axlebox springs 1,200 mm apart, transom load at centre | see PF-CT_R2_calc_notes (calcs.py) | 80.0 | 150.0 | MPa | 0.53 | OK |  |
| C3b | Coach truck sideframe PL25×170 A36, ×2.0 | Simply supported on axlebox springs 1,200 mm apart, transom load at centre | see PF-CT_R2_calc_notes (calcs.py) | 123.1 | 250.0 | MPa | 0.49 | OK |  |
| T1-a | Powered-truck inside sideframe (PL30 chords as truss-girder) bending, ×2.0 | centre load 35.1 kN ×2.0, span 1,550 between springs; chords PL30×110 / PL30×80 at 520 c/c | σ = M·c/I, M = P L/4 | 19.572 | 250 | MPa | 0.08 | OK |  |
| T1-b | Powered-truck horn cheek PL30×(220 wide) shear from lateral 0.35×axle load | Y = 0.35·42.9 kN | τ = 1.5 Y / (2 cheeks·30·220) | 1.707 | 100.0 | MPa | 0.02 | OK |  |
| T1-c | Transom PL16 box 300×200 + MS05 motor bracket (L4): weld 2×400×10 both sides, chain pull at 430 bar strength basis (HPRV 380 + spike) ×1.5 + reaction torque | F 54.7 kN, M 10.93 kN·m, T_react 3203 N·m | f = √(σ_b² + τ²) (weld, line method) | 30.579 | 145.0 | MPa | 0.21 | OK | Transom horizontal bending 7.5 MPa (negligible). E70, 0.3×483 = 145 MPa |
| T1-d | Primary spring envelope: coil spring solid height + travel vs 170 mm LT18 window | static 17.5 kN/box, rate 701 N/mm for 25 mm static; coil d26 D112 n5.1 (5160 hot-wound) | H_loaded ≥ (n+2)·d + 25 bump + 10 clash | 219.6 | 170 | mm | 1.29 | FIXED - rubber-metal chevron springs specified | FAILS for a coil: FIX - specify rubber-metal (chevron) primary springs, 1 per box, rate ~580 N/mm vert., ≥ 26 kN max, fits 170 mm (AWAIT supplier, e.g. LT35 quotes) |
| T1-e | Primary spring spec load: max (×1.8 dynamic) vs supplier rating to be met | 17.5 kN × 1.8 | F_max = 1.8 F_static | 31.554 | 31.554 | kN | 1.00 | OK | Specification row (util 1.0 by definition) - supplier must certify |
| T1-f | Traction-pin spherical plain bearing GE120ES-class (L4.2: the pin carries LONGITUDINAL load only → RADIAL rating) - required static rating at the 3 g truck case | F = 144.2 kN (3 g × A-101 truck 4,900 kg at the pin) | C0_req = 2.0 · F (s0 2) | 288.4 | 288.4 | kN | 1.00 | OK | AWAIT SKF GE120ES radial C0 ≥ value (do not use until confirmed); L4.1 GE100ES vertical-load row superseded - the centre pad carries the vertical load |

### Materials
- Sideframes PL30 A572 Gr 50 (raised from A36 for toughness/fatigue), transom PL16 A572-50
- Primary springs: rubber-metal chevron, NR compound, steel interleaves (supplier)
- Coach/tender trucks: sideframe PL25 A36, transom 2×HSS10x4x1/4 A500C (C3)

### Welds (AWS D1.1, E70XX, prequalified WPS unless noted)
- Horn cheeks to chords: CJP groove (D1.1 prequal. TC-U4b) + 6 fillet cap, UT 100% (cyclic)
- Transom box: 8 mm fillet both sides; L4 motor bracket PL25: 2×400×10 fillet both sides + 2 PL16 gussets (T1-c), MT
- Grind toe of all cheek and transom welds (fatigue detail cat. C → B')

### Bolts and torques
- Axlebox keeper bolts M20 cl.10.9, 610 N·m (dry K 0.20), Nord-Lock
- Pivot cap M24 cl.10.9, 1,055 N·m (dry K 0.20)
- MS05 slide plate 4× M20 cl.10.9 in 50 mm slots, 610 N·m (dry K 0.20), Nord-Lock, after setting sag with the 2× M20 jack screws

### Fixes logged
- Primary coil springs do not fit the 170 mm window (T1-d) → rubber-metal chevron springs specified
- Sideframe material A36 → A572-50 for cyclic margin
\pagebreak
## 3 Axles and bearings

### Governing codes and standards
- EN 13103-1:2017 (powered axle) method used as screen; AAR M-101 for steel grade reference
- ISO 281:2007 bearing life; ISO 76 static rating
- Goodman fatigue screen (Shigley) for the Ø150 pressed sprocket seat - NO hardening credit, fretting Kf 2.0 (Stress Bot)
- Lamé thick-cylinder press fit, μ 0.12

### Load cases and basis
- Vertical 1.25 Q, lateral 0.35 × axle load at flange radius (EN 13103 simplified)
- Torque at 430 bar strength basis (HPRV 380 + spike) through the 3:1 chain (no efficiency credit) - structural peak; heaviest axle (L3-as-is REAR-2 + L4) for the seat
- Hub force at the sprocket seat: chain pull + 3 g on the sprocket/hub mass
- Bearing life: 20,000 h at 7.5 mph, P = 1.3 × (Fr + 2.5 Fa) with the chain-pull reaction on the HEAVIEST axle (Stress Bot #13)

### Hand calculations

| ID | Check | Inputs | Formula | Demand | Capacity | Unit | Util | Status | Note |
|---|---|---|---|---|---|---|---|---|---|
| C7 | Loco (front driver, full ballast) axle wheel seat Ø140 bending (fatigue screen) | Q=23.4 kN/wheel, ×1.25 vertical, Y=0.35×axle load on flange at r=725; bearing arm 176 mm | see PF-CT_R2_calc_notes (calcs.py) | 63.2 | 120.0 | MPa | 0.53 | OK | Allowable 120 MPa = EN 13103 wheel-seat permissible for A1N-class steel used as a screen; axle steel 4140 Q&T or EA1N; engineer to run full EN 13103/AAR check. |
| C7 | Coach axle wheel seat Ø110 bending (fatigue screen) | Q=16.2 kN/wheel, ×1.25 vertical, Y=0.35×axle load on flange at r=300; bearing arm 169 mm | see PF-CT_R2_calc_notes (calcs.py) | 52.2 | 120.0 | MPa | 0.44 | OK | Allowable 120 MPa = EN 13103 wheel-seat permissible for A1N-class steel used as a screen; axle steel 4140 Q&T or EA1N; engineer to run full EN 13103/AAR check. |
| X1-a | L4 driven axle Ø150 pressed sprocket seat - EN 13103 screen (bending + hub moment + torsion at 430 bar strength basis (HPRV 380 + spike), nominal von Mises) | heaviest axle 49.12 kN; M_EN 17.28 + hub 3.03 kN·m | σ = 32M/πd³, τ = 16T/πd³ | 66.3 | 110 | MPa | 0.60 | OK | 110 MPa = EN 13103 permissible for press-fitted seats, EA4T class (ASSUMED for 34CrNiMo6 - PE to confirm) |
| X1-c | Ø150 pressed seat fatigue WITHOUT hardening credit, fretting Kf 2.0, heaviest axle (Stress Bot) - Goodman n required 1.5 vs available | M_seat 20.32 kN·m, T 5.91 kN·m | 1/n = σa/Se + σm/Su; Se = 0.5Su·ka·kb·0.814/Kf | 1.5 | 1.57 | n req/avail | 0.95 | OK | Ø140 gives n 1.37 (NG) → Ø150 raised seat on a Ø130 body. No keyway |
| X1-d | Seat-to-body shoulder Ø150/Ø130, r13 fillet (Kf 1.36) - Goodman n required 1.5 vs available | σa 128.1 MPa, Se 207 MPa | 1/n = σa/Se + σm/Su | 1.5 | 1.54 | n req/avail | 0.97 | OK |  |
| X1-e | Press fit Ø150 × 110, 0.12 mm min interference, μ 0.12 - slip torque vs 430 bar strength basis (HPRV 380 + spike) axle torque | p_min 64.0 MPa | T = μ·p·π·d²·L/2 | 9.609 | 29.9 | kN·m | 0.32 | OK | SF 3.11; shrink fit ≤ 200 °C; oil-injection removal |
| X1-f | Pressed hub 4140 Ø240 hoop stress at max interference 0.17 mm vs 0.6·Sy | p_max 85.3 MPa | σθ = p(1+c²)/(1-c²) | 194.7 | 393.0 | MPa | 0.49 | OK |  |
| X1-g | 45T split ring to the Ø350 hub flange (L4.1): 12 × M16 cl.8.8 FITTED DIN 609/7968, PCD 300 - shear per bolt at 430 bar strength basis (HPRV 380 + spike) × 1.5 | T_HPRV/(0.15 m·12) × 1.5 | Fv = 0.6·fub·A(Ø17)/γM2 | 8.01 | 87.2 | kN | 0.09 | OK | Bearing util 0.021; friction capacity 22.1 kN·m at 0.75 proof preload (HPRV util 0.43); tighten 219 N·m dry (153 lubricated), Nord-Lock, re-torque at 10 h |
| X1-h | Ø350 hub flange: bolt-hole edge distance (Ø17 reamed at PCD 300) vs 1.25·d0 | e = 175 - 150 = 25 mm | e ≥ 1.25 d0 | 21.25 | 25 | mm | 0.85 | OK |  |
| X1-b | Loco inside axlebox bearing - required dynamic rating C, HEAVIEST axle + chain-pull reaction | P = 58.5 kN; L 53.0 Mrev | C_req = P · L^(3/10) | 192.4 | 192.4 | kN | 1.00 | OK | Spec row: select bearing with C ≥ 190 kN (L4.1 basis; computed 192.4, earlier ≥ 169 superseded) - supplier confirmation HELD |

### Materials
- Driven axles (L4): 34CrNiMo6 (EN 10083-3) Q&T Rm ≥ 1,000 MPa or EA4T, UT per ASTM A388, MT after machining; Ø150 raised sprocket seat fine-turned/ground Ra 0.8, r13 relief + undercut at the hub edge, NO keyway, no hardening credit taken
- Coach/tender/lead axles Ø110 4140 Q&T
- Bearings: sealed, grease Li-complex EP2; temperature sensor on driven axleboxes (ASSUMED)
- Pressed hub AISI 4140 Q&T Ø240×110 with integral Ø350×20 flange (L4.1, 31.4 kg); 45T 120-2 split rim ring with bolting web (Source Bot rev 3) on 12 × M16 8.8 fitted DIN 609/7968, 219 N·m

### Bolts and torques
- Axle end caps M16 cl.10.9, 3 per end, 313 N·m (dry K 0.20) + tab washer

### Fixes logged
- Outboard Ø80 axle stub + DT5 key (C7k old NG, F03) eliminated (L2/L3); axle half-length 724 → 560
- L3 Ø120 keyed reducer seat REMOVED with the Dodge reducer (L4)
- L4: Ø150 pressed seat passes WITHOUT hardening credit on the heaviest axle (Stress Bot) - Ø140 would fail (n 1.37)
\pagebreak
## 4 Drive (rev L4.1 Poclain MS05 2-speed + ANSI 120-2 chain 3:1, governed 6 mph) and hydraulics

### Governing codes and standards
- Poclain MS05 catalog + Application Engineering review (radial load/offset, shaft code 5 DIN 5480 W55x3x17, shift on the move, rail traction duty)
- ANSI/ASME B29.1 roller chain; maker (Tsubaki) allowable-load and lubrication practice; ISO 4413 hydraulic fluid power; SAE J517 / ISO 18752 hoses
- ASTM F2291 §6.6 (power/drive, speed control), F1193

### Load cases and basis
- Start at 350 bar (H1P053 L35 pressure limiter) in 1st (468 cc); HPRV 380 bar (L4.2); the ~430 bar spike = STRENGTH basis (no efficiency credit)
- Motor start η_hm 0.90 base, 0.80 pessimistic (AWAIT Poclain starting efficiency); chain 0.97
- Adhesion: μ 0.25 dry / 0.15 wet / 0.25 sanded. Equal-torque cap 4·μ·lightest axle (parallel loop) GOVERNS - L4.1: no flow divider (Jahns HTO-4-35-FI rejected, D1-c)
- Curve resistance Röckl 400/(R-20) N/kN; start need W·(0.0208 + grade + curve)
- GOVERNED 6 mph by the pump stroke stop; independent 7 mph trip; hardware max 7.6 mph
- Engine V3307 45.6 kW net continuous (40.5 kW at 43 °C); pump allowance 35 kW (34.5 kW with the compressor clutched)

### Hand calculations

| ID | Check | Inputs | Formula | Demand | Capacity | Unit | Util | Status | Note |
|---|---|---|---|---|---|---|---|---|---|
| D1-a | Start 2% tangent - DRY, equal torque (L4.1 electronic traction control, no divider): need vs min(TE 350 bar, 4·μ·Q_min) | need 32.61 kN; TE 37.7 kN; lightest axle F2 37.11 kN | F = min(TE, 4·0.25·Q_min) | 32.61 | 37.1 | kN | 0.88 | OK | Margin 1.14 (rule ≥ 1.10 on 2% by front-ballast sizing, 2 × 75.4 kg plates) |
| D1-as | Start 2% tangent - WET, SANDED (μ 0.25), equal torque | sand MANDATORY on wet grades / curves < R100 (auto-sand on slip) | F = min(TE, 4·0.25·Q_min) | 32.61 | 37.1 | kN | 0.88 | OK | Unsanded wet margin 0.68 (NG on 2% - operating rule: sand) |
| D1-a2 | Start 2% + R100 uncompensated - DRY, equal torque (L4.1 electronic traction control, no divider): need vs min(TE 350 bar, 4·μ·Q_min) | need 36.61 kN; TE 37.7 kN; lightest axle F2 37.11 kN | F = min(TE, 4·0.25·Q_min) | 36.61 | 37.1 | kN | 0.99 | OK | Margin 1.01 (rule ≥ 1.10 on 2% by front-ballast sizing, 2 × 75.4 kg plates) |
| D1-a2s | Start 2% + R100 uncompensated - WET, SANDED (μ 0.25), equal torque | sand MANDATORY on wet grades / curves < R100 (auto-sand on slip) | F = min(TE, 4·0.25·Q_min) | 36.61 | 37.1 | kN | 0.99 | OK | Unsanded wet margin 0.61 (NG on 2% - operating rule: sand) |
| D1-a3 | Start 0% + R50 - DRY, equal torque (L4.1 electronic traction control, no divider): need vs min(TE 350 bar, 4·μ·Q_min) | need 27.29 kN; TE 37.7 kN; lightest axle F2 37.11 kN | F = min(TE, 4·0.25·Q_min) | 27.29 | 37.1 | kN | 0.74 | OK | Margin 1.36 (rule ≥ 1.10 on 2% by front-ballast sizing, 2 × 75.4 kg plates) |
| D1-a3s | Start 0% + R50 - WET, SANDED (μ 0.25), equal torque | sand MANDATORY on wet grades / curves < R100 (auto-sand on slip) | F = min(TE, 4·0.25·Q_min) | 27.29 | 37.1 | kN | 0.74 | OK | Unsanded wet margin 0.82 (NG on 2% - operating rule: sand) |
| D1-b | 2% start - pessimistic η_hm 0.80 (pending Poclain starting efficiency) | same | F = 4·p·V/(2π)·0.80·0.97·i/r | 32.61 | 33.5 | kN | 0.97 | OK | 341 bar needed at η 0.80 vs 350 limiter |
| D1-c | REJECTED OPTION (L4.1): Jahns HTO-4-35-FI gear flow divider - TE with motor Δp capped by the 320 bar section rating vs 2% need | motor Δp ≤ 290.0 bar; 17.4 L/min/section at 2 mph vs min 12-16 | F = 4·Δp·V/(2π)·η·i/r | 32.61 | 31.2 | kN | 1.04 | REJECTED OPTION - gear flow divider not fitted; electronic traction control (D1-m/m2) | Also below its minimum flow at every start, +160 kg, +heat → NOT FITTED; electronic traction control adopted (D1-m) |
| D1-c2 | Divider at a start: flow per section at 0.5 mph in 1st vs catalog minimum 12 L/min (accuracy not defined below) | 4 × 468 cc × n / ηv / 4 | Q = V·n/ηv | 12.0 | 4.4 | L/min (min req/avail) | 2.73 | REJECTED OPTION - divider below its minimum flow at starts | Rejected-option row: the divider is not proven to lock the axles at start |
| D1-d | Single-wheelset spin at the HARD 2,600 rpm engine limit and the 42 cc stop (L4.2 high-idle check): standstill start in 1st (MS05 fail-to-1st; 2nd only through the PNOZ s30 ≥ 1.5 mph contact) vs MS05 HighFlow 1st max | one axle takes the full pump flow, no-load η_v 0.99 | n = Q·ηv/Vg | 229 | 370 | rpm | 0.62 | OK | Rolling in 2nd (other axles turning): 378 rpm vs 430 (util 0.879). HighFlow valving REQUIRED (Classic 275 NG); traction control destrokes |
| D1-m | Electronic traction control (L4.1, replaces the divider): slip threshold vs ground-speed reference (3rd pickup on the unbraked pony) | MS05 sensor per motor + pony reference | spec | 1.1 | 1.1 | ratio | 1.00 | OK | Spec row: axle > v_ref × 1.10 or + 0.5 mph or > 0.5 m/s² → auto-sand, destroke to v_ref × 1.05 in ≤ 0.3 s (AWAIT Danfoss), ramp back; hill-start hold; rollback alarm. PLUS+1 software HELD vendor ask |
| D1-m2 | 2% start with traction control - DRY/SANDED equal-torque margin vs front-ballast rule 1.10 | lightest axle 37.11 kN, 2 × 75.4 kg plates | 4·0.25·Q_min / need | 1.1 | 1.14 | margin (rule/avail) | 0.96 | OK | Wet unsanded 0.68 → sand mandatory (unchanged rule) |
| D1-u | H1P053 input shaft G1 (14T 12/24) max torque vs V3307 engine peak 265 N·m (L4.1) | continuous 164.1 N·m (35 kW at 2,200 + charge) | T_peak / T_max | 265.0 | 592.0 | N·m | 0.45 | OK | AIE 'SAE B 13T' drive mates only G4 → engine coupling hub must be 14T 12/24 (AIE confirmation HELD); alternate G5 15T (370 N·m) |
| D1-u2 | REJECTED OPTION: shaft G4 (13T 16/32, mates the AIE drive as quoted) vs engine peak 265 N·m | Danfoss rated 180 / max 222 N·m | T_peak / T_max | 265.0 | 222.0 | N·m | 1.19 | REJECTED OPTION - G4 shaft; G1 kept (D1-u) | G4 fails (1.19) → not used |
| D1-e | Pump H1P053 UNLIMITED input torque at the 430 bar STRENGTH basis (HPRV 380 + spike, L4.2) vs G1 input shaft rating 534 N·m | 430 bar × 53.8 cc/(2π·0.93) | T = Δp·Vg/(2π·η_hm) | 395.9 | 534 | N·m | 0.74 | OK | 35 kW cap (128.5 N·m) = anti-stall SOFTWARE; 34.5 kW while the compressor clutch is engaged |
| D1-f | 6 mph GOVERNOR (L4.2): loaded speed in 2nd at the 42 cc stroke stop and the hard tamper-sealed 2,600 rpm engine limit | 4 × 234 cc, 15:45, Ø1,450 | v = Q·η/(Vg·i) | 5.96 | 6.0 | mph | 0.99 | OK | No-load at η_v 0.99: 6.47 mph (< 7 mph independent trip). Stop sealed at 42 cc; engine limit sealed by AIE (data HELD) |
| D1-d2 | INFORMATION (double failure, not a design case): standstill spin in 2nd at 2,600 rpm / 42 cc, no-load, only if PLUS+1 AND the PNOZ s30 ≥ 1.5 mph contact both fail | one axle, η_v 0.99 | n = Q·ηv/Vg | 457 | 430 | rpm | 1.06 | INFORMATION - double failure (PLUS+1 AND PNOZ s30); not a design case | INFO ONLY (util 1.064) - any single failure leaves the MS05 in 1st (fail-to-1st valves) |
| D1-n | Overspeed protection: independent 2-channel speed relay (SIL 2 / PL d class) vs governed 6 mph + 1 mph | 2 dedicated sensors on different trucks | spec | 7.0 | 7.0 | mph | 1.00 | OK | Hard-wired to the BP exhaust valve + pump neutral (CCO), NOT through PLUS+1 (Stress Bot); tested daily (F770) |
| D1-o | MS05 pressure: HPRV 380 bar (L4.2 pressure revision, PL 350 unchanged, 30 bar spacing) vs motor max 450 bar |  |  | 380.0 | 450 | bar | 0.84 | OK |  |
| D1-g | Main loop hose -16 (25.4 bore) velocity at the stop flow | Q 103.7 L/min | v = Q/A | 3.411 | 4.6 | m/s | 0.74 | OK | L4.2: -16 loop hose, code 62 / 24° S25 ends, whip restraints ≥ 420 bar WORKING (maker 420), ISO 18752 / SAE J517 impulse rating (ISO 18752 / ISO 6605, 133 % of WP) covering the ~430 bar transient; strength cases checked at 430 bar; Danfoss overshoot = information only |
| D1-h | Branch hose -10 (15.9 bore) per motor | Q 25.9 L/min | v = Q/A | 2.176 | 4.6 | m/s | 0.47 | OK |  |
| D1-i | Hydraulic oil cooler duty vs SPEC ≥ 14 kW at 43 °C OUTSIDE air (tender left wall, own louvre) | 35 kW, η_pump × η_motor × chain | Q = (1-η)·P | 9.0 | 14.0 | kW | 0.64 | OK | AWAIT cooler supplier curve at 43 °C; electric fan from the genset charger |
| D1-t | Hot-day engine power: traction allowance + fan/aux with the compressor clutched vs V3307 net at 43 °C | compressor off 37.3 kW | demand / P_43C | 40.5 | 40.5 | kW | 1.00 | OK | compressor electric clutch engages only at low traction demand or MR < 7.0 bar; anti-stall map drops to 34.5 kW while clutched; hydraulic cooler fan electric 24 V from the genset charger (not on the engine/alternator) |
| D1-j | 2% hold speed (power-limited, best displacement, dp ≤ 350; 2nd only ≤ 300 bar) vs 2 mph target (ASSUMED) | 35 kW × 0.855 × 0.92 × 0.95 × chain 0.97 | v = P_rim/R | 2.0 | 2.69 | mph | 0.74 | OK | Hot day 2.65 mph |
| D1-qA | Route Alt A: worst START anywhere on the loop incl. curve resistance (Röckl 400/(R-20) N/kN, train-length averaged) vs adhesion-limited TE (L4.1 equal-torque dry cap 4·0.25·Q_min) | equivalent grade 2.0% (AREMA 0.8 lb/ton/° cross-check 2.199% → 33.06 kN) | F = W·(0.0208 + i + w_c) (× W_L4.1/W_RT1) | 32.61 | 37.11 | kN | 0.88 | OK | Wet: sand μ_req 0.208 (≤ 0.25 sanded). Hold incl. curves 2.72 mph (AREMA 2.52) vs 2 mph - curve compensation in the redline keeps grade + curve ≤ 2.0% |
| D1-qB | Route Alt B: worst START anywhere on the loop incl. curve resistance (Röckl 400/(R-20) N/kN, train-length averaged) vs adhesion-limited TE (L4.1 equal-torque dry cap 4·0.25·Q_min) | equivalent grade 2.0% (AREMA 0.8 lb/ton/° cross-check 2.199% → 33.06 kN) | F = W·(0.0208 + i + w_c) (× W_L4.1/W_RT1) | 32.61 | 37.11 | kN | 0.88 | OK | Wet: sand μ_req 0.208 (≤ 0.25 sanded). Hold incl. curves 2.72 mph (AREMA 2.52) vs 2 mph - curve compensation in the redline keeps grade + curve ≤ 2.0% |
| D1-qC | Route Alt C: worst START anywhere on the loop incl. curve resistance (Röckl 400/(R-20) N/kN, train-length averaged) vs adhesion-limited TE (L4.1 equal-torque dry cap 4·0.25·Q_min) | equivalent grade 2.0% (AREMA 0.8 lb/ton/° cross-check 2.185% → 32.96 kN) | F = W·(0.0208 + i + w_c) (× W_L4.1/W_RT1) | 32.61 | 37.11 | kN | 0.88 | OK | Wet: sand μ_req 0.208 (≤ 0.25 sanded). Hold incl. curves 2.72 mph (AREMA 2.53) vs 2 mph - curve compensation in the redline keeps grade + curve ≤ 2.0% |
| D1-qD | Route Alt D: worst START anywhere on the loop incl. curve resistance (Röckl 400/(R-20) N/kN, train-length averaged) vs adhesion-limited TE (L4.1 equal-torque dry cap 4·0.25·Q_min) | equivalent grade 2.0% (AREMA 0.8 lb/ton/° cross-check 2.199% → 33.06 kN) | F = W·(0.0208 + i + w_c) (× W_L4.1/W_RT1) | 32.61 | 37.11 | kN | 0.88 | OK | Wet: sand μ_req 0.208 (≤ 0.25 sanded). Hold incl. curves 2.72 mph (AREMA 2.52) vs 2 mph - curve compensation in the redline keeps grade + curve ≤ 2.0% |
| D1-r | R50 (Alt C intent) start on 2% WITH curve compensation 1.33% (grade on curve 0.67%) vs adhesion-limited TE | w_c(R50) Röckl 13.33‰, AREMA 13.97‰ | F = W·(0.0208 + i + w_c) (× W_L4.1/W_RT1) | 32.61 | 37.11 | kN | 0.88 | OK | UNCOMPENSATED R50 at 2.0% needs 43.3 kN > 37.1 kN adhesion (NG) - Alt C must compensate R50 curves by ≥ 1.33% (grade ≤ 0.67% on the curve) |
| D1-s | R100 start on 2% WITHOUT compensation (sensitivity, if the track crew does not compensate) vs adhesion-limited TE | w_c(R100) Röckl 5.0‰ (AREMA 6.99‰ → 36.93 kN) | F = W·(0.0208 + i + w_c), L4.1 W (drive_L4 case 2% + R100 uncompensated) | 36.61 | 37.11 | kN | 0.99 | OK | SENSITIVITY only (basis: curves compensated). Hold 2.27 mph. Recommend compensation 0.04%/° rule ≈ 0.5% on R100, 1.33% on R50, 1.6% on R45 |
| D2-a | Chain Tsubaki RS120-2: pull at 430 bar strength basis (HPRV 380 + spike) vs maker allowable load | T_axle 9,609 N·m on PD 546.2 mm | F = 2T/PD | 35.2 | 51.7 | kN | 0.68 | OK | SF on ultimate 7.3 (HPRV), 7.9 (heaviest-axle slip) |
| D2-b | Chain: continuous 2% running pull vs allowable |  |  | 13.3 | 51.7 | kN | 0.26 | OK |  |
| D2-c | Motor shaft code 5 (W55x3x17) radial load at 400 bar vs catalog dynamic radial (sprocket at offset ≤ 0) | chart p.20 |  | 35.2 | 60.0 | kN | 0.59 | OK | AWAIT Poclain AE for offset and shift-on-the-move |
| D2-d | Motor bearing life at continuous 2% running vs 20,000 h at 6 mph | L ∝ F^-10/3 from 10 Mrev at 30 kN |  | 127.2 | 152.0 | Mrev | 0.84 | OK |  |
| D2-e | Chain wear take-up: centre growth at 3% elongation vs slotted-mount slide | C 417.6 → 451.4 mm |  | 33.8 | 37.0 | mm | 0.91 | OK | Replace the chain at 2% (3% absolute) |
| D2-f | L4.1 corrected chain slack (dL = 2·span/C·dC, Stress Bot r2): axle bump to tight chain at sag 17 mm, chain line horizontal, vs the ±22 mm hard bump stop - NO IDLER | span 376.1 mm, dL/dC 1.801; 3 mm primary shim: 28.0 mm | z_tight from √((√(C²+z0²)+S/(dL/dC))² − C²) − z0 | 22.0 | 30.8 | mm | 0.71 | OK | Re-shim procedure: wheel-wear height at the centre plate/side bearers only; primary re-shim ≤ 3 mm then motor-slide reset at ride height (chain line horizontal ±3). L4 row used dL = dC (wrong). |
| D2-g | Oil-bath case radial clearance at 3% wear + ±25 travel vs 15 mm minimum | case inner r 332.7 mm vs OD/2 284.5 + ride-out 8.2 + 25 |  | 15.0 | 15.0 | mm | 1.00 | OK | X -336..C_new+158 from the axle, Z axle +/-336 (was -310..C+125, +/-305 - FAILED at 3 %: the 15T would have hit the end wall) |
| D2-g2 | Oil-bath case MOTOR end clearance at 3% wear with the Martin 15T OD 202 (L4.1; case sized on ~206) vs 15 mm | OD 202.0 (L4 206.1) |  | 15.0 | 17.1 | mm | 0.88 | OK | case unchanged; 15T to sideframe chord 85 mm (lateral) |
| D4-ri | L4.2 trip run-in (Stress Bot r3): worst loco-tender buff over CCO overspeed / 24 V loss (≥ 3 s swash ramp, MS05 fail-to-1st), FLOAT entry with the bypass failed closed, accidental T04 and a T04 line burst downstream of the choke (Ø1.2 port orifices, 2-channel vent switch) vs the R80 loco-LT allowance | Stress Bot s4 lumped-mass model, k 20/100 kN/mm, 1.0 mm play; tender TB-3.13d 8,706.5 kg, CG [2422.7, 11.3, 1110.4], brake 5.845 kN (0.671 m/s²); hydraulic trip force at 400 bar kept (above the HPRV 380 setting; the ~430 bar spike is a ms-scale transient); L4 as-was 67.0 kN | max buff over all design cases | 25.3 | 33.2 | kN | 0.76 | OK | Double failures (information only): 24 V loss + bypass failed closed 29.7 kN; T04 burst + both vent channels failed 34.3 kN. Direction change only at zero speed + ≥ 1 s ramp. |
| D4-wt | L4.2 forward 2 % start, sand on BOTH trucks (every driven axle, direction of travel), Ø120 traction pin (h 0.65 m) + laminated elastomer centre pad / PTFE yaw slide (pad share 0.083, μ ≤ 0.08) - margin rule ≥ 1.10 | worn Ø1430 margin 1.112; degraded (trailing nozzles failed, carry-over μ 0.20) 1.101 new / 1.083 worn; rigid steel plate at μ 0.08 would give 1.079 | 4·μ·min(axle with transfer) / need | 0.899 | 0.909 | need/cap | 0.99 | OK | margin 1.112 (worn, governing) vs 1.10 |
| D4-wr | L4.2 reverse full-train start, sand on both trucks: OPERATING RULE grade ≤ 1.2 % (from the calc: 1.10 margin at 1.39 % new / 1.35 % worn; reverse pull cap of record 28.9 kN with 1.10: 1.21 % - GOVERNS) | reverse 2 % margin 0.899 (< 1.10: the lightest axle F2 is already sanded) - covered by the rule; PLUS+1 reverse pull cap 28.9 kN (supersedes 29.4) | g_rule ≤ min(g(1.10, worn), g(1.10, 28.9 kN cap)) | 1.2 | 1.21 | % | 0.99 | OK | Track is LEVEL (Layout F, 0.0 %, Rail Bot §5b FINAL); 2 % checked as the conservative vehicle case |
| D4-hf | L4.1 hub shrink fit 0.15-0.20 (oil pressing deleted): slip torque, hub 30 K hot, 9.6 µm smoothing, removal groove deducted vs 1.5 × HPRV axle torque | δ_eff 0.0887 mm, μ 0.12 | T = π d² L μ p / 2 | 14.397 | 16.7 | kN·m | 0.86 | OK | SF at HPRV 1.74 (≥ 1.5); hoop 195 MPa < 393 |
| D4-sp | L4.2 HIGH-IDLE CHECK: top speed at the HARD tamper-sealed 2,600 rpm engine limit with the 42 cc stop, no-load η_v 0.99 vs the 7 mph independent trip | 2nd 234 cc, 15:45, Ø1,450; loaded 5.96 mph | v = Q·η/(Vg·i) | 6.47 | 7.0 | mph | 0.92 | OK | The L4.1 2,850 rpm high-idle case no longer exists (engine cannot exceed 2,600); AIE to set and seal (HELD) |
| D4-ch | L4.2 chain reversal with the zero-speed interlock + ≥ 1 s ramp (impact ~1.3) at the 430 bar STRENGTH basis vs ANSI 120-2 allowable | Stress Bot r2 #3; pull at 430 bar 35.2 kN | F = 1.3·F_430 | 45.8 | 51.7 | kN | 0.89 | OK | breaking-strength certificate: see D4-mb |
| D4-mb | L4.2 chain minimum breaking load at the 430 bar STRENGTH basis: same factor as the old ≥ 302.5 kN at HPRV 400 → required MBL vs the SPECIFIED certified MBL (ANSI 120-2, mill certificate per lot) | ANSI B29.1 duplex 302.5 kN at HPRV 400 (pull 32.7 kN) -> factor 9.24; pull at 430 bar 35.2 kN | MBL_req = factor · pull_430 | 325.2 | 326 | kN | 1.00 | OK | SPEC ≥ 326 kN certified. Standard Tsubaki RS120-2 (296 kN) does NOT meet it at 430 (util 1.099, see D4-mb2; it passes at HPRV 380: 287.4 kN, util 0.971) - higher-strength 120-2 = VENDOR BATCH, or PE acceptance of SF 8.41 on ultimate at the spike |
| D4-mb2 | INFORMATION: standard Tsubaki RS120-2 published 296 kN vs the same-factor MBL at the 430 bar strength basis |  |  | 325.2 | 296.0 | kN | 1.10 | INFORMATION - standard 296 kN chain not accepted; SPEC certified MBL (D4-mb) | NOT ACCEPTED as standard - see D4-mb (passes at HPRV 380, 287.4 kN) |
| L41-sw | Loco Bot (c): L-108 saddle web PL10 out-of-plane at 3 g longitudinal WITH the 100×70 rivnut windows - FIX: 8 × PL10 45×150 gussets per saddle at Y±535/±685 | as detailed 1101 MPa (NG, util 5.9) | σ = F·h / S | 52 | 187 | MPa | 0.28 | OK | +12.7 kg (6 saddles) in the ledger |
| L41-s1 | Loco Bot (e): SD-1 bolster cap re-cut inboard to Y±50, HB16 at Y±90 (edge 40 ≥ 1.5 d0), cap bending under 8.05 kN uplift (LRFD) | PL10 × 200, lever 73.8 | 1.6 M / φ Fy Z | 0.95 | 1.125 | kN·m | 0.84 | OK |  |
| L41-s2 | Loco Bot (d): SD-2 end-sill hold-down by 4 clamp plates PL16 80×120 under the sill flange (no sill holes) - clamp plate bending | uplift 8.05 kN, 2 clamps/side | σ = M/S | 17.7 | 150 | MPa | 0.12 | OK | M16 8.8 4.03 kN vs 62.8 kN |
| L41-cb | Loco Bot (f): ballast clamp bars FB100×12×560 for 1 plate (75.4 kg) per side pocket - 2 g uplift + 3 kN rattle preload; plate located by the pocket walls | 4 bars, 2 per plate | M = F/4·(L − b/2) | 110 | 187 | MPa | 0.59 | OK | rod nuts 30 N·m + Nord-Lock (not 441) |
| L41-w1 | Ø1430 driver condemning limit - governed speed (42 cc stop, sealed 2,600 rpm) vs 6 mph | v ∝ D: 5.96 × 1430/1450 | v ≤ 6.0 | 5.88 | 6.0 | mph | 0.98 | OK | trip set in axle rpm for Ø1450 → 6.90 mph at Ø1430 (safe side) |
| L41-w2 | Steering 7 (b): 2 % start at Ø1430 - forward equal-torque cap with transfer (worn tread −341 kg) vs need | margin 1.128 | need / cap | 0.887 | 0.909 | - | 0.97 | OK | margin ≥ 1.10 basis; TE at 350 bar 38.2 kN |
| L41-w3 | Reverse full-train start at Ø1430 (L4.2, sand both trucks, centre pad) - rule grade vs worn-wheel 1.10 grade | worn grade for 1.10: 1.35 % | g_rule ≤ g_cap | 1.2 | 1.35 | % | 0.89 | OK | operating rule 1.2 % (governed by the 28.9 kN reverse pull cap; L4.1 1.55 superseded) |
| L41-w4 | L4.2 FINAL flange-height limit (Loco Bot E7 / Rail Bot §5b): WITHDRAW at 28 mm train-wide, re-profile ≤ 27; joint rail-head vertical wear ≤ 2 mm (rail height condemn ≤ 86.9 mm at bolt positions) - worn flange vs ASCE 40 joint-bolt head top | head top 32.5 mm below TOR new − 2 mm wear = 30.5; 30 mm limit WITHDRAWN; 6 mm joint limit WITHDRAWN (applies only > 1 m from rail ends) | h_f ≤ head top − joint wear | 28.0 | 30.5 | mm | 0.92 | OK | clear 2.5 mm at both limits; bolt protrusion ≤ 10 mm measured at install (worst 9.1 with flat bars ≤ 12.0 + 3/4 in B18.10 oval-neck H ≤ 12.7); pony 22 mm to the flangeway; frog flangeway ≥ 36 mm |
| L41-w5 | Steering 7 (b): lower outline at Ø1430 (all truck items −10 mm) | min 255 → 245 ATOR | 150 ≤ clear | 150 | 245 | mm | 0.61 | OK |  |
| L41-t1 | L4.2 T04 apply delay (choke Ø2.4 + 1.0 L damping accumulator; Ø1.2 orifice in each T04 port) - required ≥ 1.0 s for the run-in result | V 0.18 L at Δp 17.5 bar | t = V / Q_orifice | 1.0 | 1.01 | s | 0.99 | OK | rise 4.21 s ≥ 2.0; release 6.20 s vs the separate T04 target 8 s; verify by timed commissioning test |
| L41-t2 | Steering 7 (a): manual-release accumulator - required V0 for 2 releases (2 × 0.58 L, 22 → 15 bar, pre-charge 13.5, adiabatic) vs 6.0 L | T04 volume 4 × 0.10 L ASSUMED | V0 = ΔV / [(p0/p1)^(1/n) − (p0/p2)^(1/n)] | 5.45 | 6.0 | L | 0.91 | OK |  |
| L41-b1 | Steering 8/9: LOCO brake release time WORST CASE (8 × 1.0 L calipers, 0 → 5.1 bar g, supply drooped to 5.6 bar, isothermal, + 1.0 s signal/relay ASSUMED) at the specified min total conductance C 3.0 | Loco Bot 3.7 s at C 2.0 (1.8-7.3); this model 3.68 s fill at C 2.0 | ISO 6358 fill | 3.46 | 4.0 | s | 0.86 | OK | C required ≥ 2.50; design budget C 5.26 → 2.40 s; commissioning timed test |
| L41-b2 | Steering 8/9: release-path total sonic conductance - spec minimum vs parts budget (regulator 10 + relay 8 + 3/4 in trunk 8 in series, 4 × 1/2 in branches C 2.0 in parallel) | C_tot = (ΣC_i^-3)^(-1/3) | C_spec ≤ C_budget | 3.0 | 5.26 | dm³/(s·bar) | 0.57 | OK | Loco Bot line lengths / fittings to confirm trunk and branch C |
| L41-b3 | Steering 8/9: MR after one loco release from cut-in (7.5 − 0.98 bar) vs regulator set 6.0 + 0.4 bar regulating head | 48 L free air per release; recharge 17.8 s at 14 cfm | p_MR ≥ p_set + 0.4 | 6.4 | 6.52 | bar | 0.98 | OK |  |
| L41-b4 | Steering 8/9: train steady brake-air demand (14.0 L calipers; 84 L free air per release) vs IR 2340 compressor 14 cfm | 3.55 cfm steady | demand / FAD | 3.55 | 14.0 | cfm | 0.25 | OK | duty 25 %% |
| L41-b5 | TB-3.13d tender brake (8,706.5 kg; calipers unchanged, 5.845 kN, mixed Coremo D 2N sets, pad wear limit 5.5 mm) vs loco 0.690 - decel mismatch vs 0.03 m/s² run-in allowance | tender 5.845/8.7001 = 0.672 / loco 0.690 | abs(Δa) | 0.018 | 0.03 | m/s² | 0.60 | OK | tender softer: buff run-in covered by D4-ri |
| L41-e1 | ERV roof pod: static allocation 3,450 ARL + kinematic allowance (bounce/roll/lateral, ASSUMED 150 mm) vs K-401 overhead 4,300 | static 3,450 | z_kin ≤ 4,300 | 3,600 | 4,300 | mm | 0.84 | OK | 3,450 is a STATIC allocation; kinematic envelope checked against K-401 |
| L42-dn | Descent 2 % (FLOAT mode: loop bypass + ≥ 3 s swash ramp) - FRICTION brakes sized for the full descent with the loaded train: descent force vs SERVICE friction force | train 81513 kg; shares loco 0.245 / tender 0.104 / coaches 0.651 | F = m·g·(i - r) | 15.99 | 39.35 | kN | 0.41 | OK | Disc heat: continuous descent limit 2398 m (coaches govern, ΔT 250 K adiabatic) vs Layout F dead level; cooler in float 3.3 of 14 kW (util 0.24) - not overloaded |
| L42-dc | Float-mode cooler load vs cooler rating |  |  | 3.3 | 14.0 | kW | 0.24 | OK | bypass circulation only |
| L42-t1 | T04 release time (normal, charge feed through the CDK 20 bar reducer, Ø2.4 choke + 1.0 L damping accumulator + Ø1.2 port orifices) vs the SEPARATE T04 release target | delay 1.01 s + rise 4.21 s | orifice/accumulator model, Cd 0.62 | 6.2 | 8.0 | s | 0.78 | OK | MET. Air (friction) release ≤ 4 s is a separate target - L42-ar |
| L42-t2 | T04 line burst DOWNSTREAM of the choke (hard lines / 4SH; Ø1.2 port orifice per motor): loco-tender run-in vs the R80 allowance | rise to 90 % in 3.32 s | Stress Bot s4 | 25.3 | 33.2 | kN | 0.76 | OK | 2-channel vent switch; accidental T04 (BP first) 23.8 kN |
| L42-t3 | T04 charge-feed pressure at LOW IDLE (charge 21 bar min ASSUMED, CDK 20 bar) vs T04 full release 15 bar (ASSUMED) |  |  | 15.0 | 20.0 | bar | 0.75 | OK | margin 1.33; loop shuttle DELETED - no loop-pressure part in the T04 circuit |
| L42-t4 | Tow / engine-off T04 release: 6.0 L bladder accumulator (pre-charge 13.5 bar) + hand pump - accumulator volume for 2 releases |  | Boyle | 5.45 | 6.0 | L | 0.91 | OK | 97 hand-pump strokes for a full recharge |
| L42-p1 | Traction pin Ø120 4140 Q&T - service: 1.3 × TE at the 430 bar strength basis (0.6 Fy) | lever 0.46 m ASSUMED | σ = M/Z | 82 | 393 | MPa | 0.21 | OK | GE120ES-class spherical plain bearing; +22 kg per pin vs Ø100/GE100ES (ledger) |
| L42-p2 | Traction pin Ø120 - 3 g truck (A-101 4,900 kg, exceptional, Fy) |  | σ = M/Z | 391 | 655 | MPa | 0.60 | OK | pin in build/model.py (Z1110 → Z650 at X4075 / X7275) |
| L42-cp | Centre-plate friction in the start margin: laminated elastomer pad + PTFE yaw slide (pad share 0.083 ASSUMED, μ ≤ 0.08) - forward 2 % margin | k_pin 32.9 / k_pad 3.0 MN/m | 4·μ·min axle / need | 0.899 | 0.909 | need/cap | 0.99 | OK | fwd margin 1.112 vs 1.10; pad stiffness and PTFE μ = VENDOR BATCH (ASSUMED) |
| L42-k2 | K2-a OF RECORD (L4.2): max driver wheel at the PLUS+1 forward TE command limit 33.0 kN (1.01 × the 2 % need) incl. +42.8 kg final drive, Ø120 pins, P-106 pockets, gross brake piping/chains and the 59.8 kg NB-1 nose ballast at X450 | reverse pull cap 28.9 kN → wheel 25.74 kN | truck-pitch + body transfer | 25.89 | 26.0 | kN | 1.00 | OK | loco 19934 kg; without NB-1 the start TE would load a wheel to 26.1 kN (Loco Bot drift) - FIXED by NB-1 |
| L42-sf | Sanders on BOTH trucks (level switch, flow proof, hill-hold) - forward 2 % start margin, worn Ø1430 |  |  | 0.899 | 0.909 | need/cap | 0.99 | OK | margin 1.112 |
| L42-pz | Pony reference: ~96-tooth target wheel - pulse rate at 0.5 mph (worn) vs the 10 Hz minimum for the 100 ms filter | 2 Hall sensors in quadrature; agreement check vs axles; PNOZ s30 kept independent | f = v·z/(π·D) | 10.0 | 10.5 | Hz | 0.95 | OK | 92 teeth minimum |
| L42-wd | Wind on curves: R80 dry at 25 mph wind (interim rule: 25 mph limit on R ≤ 80, no full-pull starts with a lubricator out) - L/V margin | 40 mph dry 0.939 (covered by the rule); lubricated 40 mph 1.287 |  | 1.0 | 1.018 | 1/margin | 0.98 | OK | Layout F has no R70 |
| L42-lg | Safety-chain lug PL44.5 A572-50 faced to 42.5 mm + 1-1/8 in G-2130 shackle - 1.5 × TE at the 430 bar strength basis vs shackle WLL 93.2 kN | 69.4 kN |  | 69.4 | 93.2 | kN | 0.74 | OK | lug util 0.17; each chain = 2 × G-2130 + 2 × S-1325A + 1-2 links 5/8 G100; coupler WLL ≥ chain WLL PASS (Loco Bot E8) |
| L42-ar | Brake AIR release time (QEV option B kept, MR ≥ 5.6 bar) vs the ≤ 4 s air release target | C_spec_min 3.2 per branch; relay/regulator C ≥ 8-10; valve purchase spec C ≥ 0.31 | ISO 6358 fill | 2.36 | 4.0 | s | 0.59 | OK | Loco Bot E7/E8; coach release indication dual-channel per Electro E3.6h (PL d Cat 3) |
| L42-mr | MR after one release from the 6.0 bar governor minimum (coupled MR ~190 L) vs the 5.6 bar used in the release time | release volume 10.26 L | Boyle | 5.6 | 5.68 | bar (min) | 0.99 | OK | 20 L local reservoir DELETED |
| L42-qa | QEV option A (QEVs deleted): spring-apply exhaust time through the relay, worst branch, cold -10 °C, 6.0 → 0.5 bar g (ASSUMED full-apply pressure) | relay exhaust C 8 ASSUMED; to 0.3 bar g 2.38 s | ISO 6358 discharge | 2.13 | 2.0 | s | 1.06 | INFORMATION - QEV option A rejected; option B kept (L42-qb) | INFORMATION: option A FAILS (shortfall 0.13 s) although its 7 mph / 2 % stop passes (21.7 m vs 30) → option B KEPT |
| L42-qb | QEV option B (maker-certified ≥ 15 bar 1/2 in QEV, vendor batch): spring-apply time, worst branch, cold |  | ISO 6358 discharge | 0.94 | 2.0 | s | 0.47 | OK | 7 mph trip stop on 2 % down with the apply delay: 20.1 m vs 30 m; piping 43.7 kg gross |
| L42-tv | Tow valve across loop A-B: HYDAC KHB3K DN06 class (500 bar) at the 430 bar strength basis (DN25 310 bar NOT allowed on the loop) | tow ≤ 2 mph in 1st: 67.1 L/min | p/rating | 430.0 | 500.0 | bar | 0.86 | OK | util 0.86 |
| L42-tq | Tow valve DN06 sizing: Δp at the 2 mph tow flow (4 MS05 in 1st, worn Ø1430) vs 30 bar limit | bore 6 mm, K 1.5 ASSUMED | Δp = K·ρ·v²/2 | 10.2 | 30.0 | bar | 0.34 | OK | tow drag 1.27 kN, heat 1.14 kW; confirm with the HYDAC DN06 curve (vendor batch) |
| L42-hs | Loop hose Manuli DIAMONDSPIR H10018025 (ISO 18752-C, 560 bar WP) vs the 430 bar spike / strength basis | HPRV 380 → 0.679 | p/WP | 430.0 | 560.0 | bar | 0.77 | OK | OD 41.2, 2.91 kg/m; impulse rating per ISO 18752-C |
| L42-hb | Loop hose minimum bend radius 350 mm vs the tender's tightest bend at R70 (394.3 mm, Tender Bot) |  |  | 350.0 | 394.3 | mm | 0.89 | OK | util 0.888 |
| L42-gb | GRADE BASIS: track Layout F dead level (0.0 %, Rail Bot §5b FINAL); vehicles checked at 2 % as the conservative case - reverse full-train start limit (all files) |  |  | 1.2 | 1.21 | % | 0.99 | OK | governed by the 28.9 kN reverse pull cap with 1.10 |
| D2-h | 15T bore spline N55x3x17 on MS05 shaft code 5 (W55x3x17): flank pressure at the 430 bar STRENGTH basis × KA 1.5 - 15T made to order in 4140 Q&T 28-32 HRC (L4.2) | T 3,203 × 1.5 N·m; L 60 engaged | p = 2T/(d·z·h·L·φ) | 102.6 | 150.0 | MPa | 0.68 | OK | C1045 catalogue hub would be 1.03 (NG) - Martin D120B15 stock NOT accepted; REQUIRE ≥ 58 mm engaged, hub face to shoulder ≤ 2 mm, end plate. Hub torsion util 0.09 |

### Materials
- Motor: Poclain MS05 468/234 2C HighFlow, T04 brake, shaft code 5, DIN 5480 W55x3x17 (male), speed sensor (model code AWAIT Poclain)
- Chain: ANSI 120-2 (Tsubaki RS120-2 or equal), 54 links, oil bath ISO VG 220 EP
- Sprockets: 15T Martin D120B15 (OD 202) hub broached DIN 5480 N55x3x17 (female), ≥ 58 mm engaged; 45T SPLIT rim ring with bolting web, 12× M16 8.8 fitted DIN 609/7968 (219 N·m) to the Ø350 flange of a 4140 pressed hub (31.4 kg) - replaceable in place, no pressing
- Oil-bath case 3 mm steel on the motor bracket, floating seal plate at the axle
- Hydraulic fluid ISO VG 46 HV; EXTERNAL charge filtration HYDAC DF 60 pressure filter with clogging indicator (grade ASSUMED β10 ≥ 200)
- Pump: Danfoss H1P053 with CCO (control cut-off, wired to the Pilz s30 7 mph trip), G1 shaft (14T 12/24; engine coupling hub 14T 12/24 on the SAE B pad), L35 (PL 350 / HPRV 380), stroke stop 42 cc sealed + hard 2,600 rpm engine limit, PLUS+1 (anti-stall 35 kW, shift, traction control)
- L4.1 NO flow divider. Traction control: 3rd speed pickup on the pony tone ring, loop A/B transducers, auto-sanders
- L4.1 loco valves (steering 7): T04 release from the loco loop = [L4.2: loop shuttle DELETED - T04 fed from the H1 charge circuit] + 10 µm filter + 3-way reducing/relieving valve 20 bar + 3/2 solenoid NORMALLY VENTED (HydraForce SV08/SV10-30 class) + choke Ø2.4 + 1.0 L damping accumulator + brake-line shuttle; manual release = check + 6.0 L bladder accumulator + 12 cm³ hand pump + guarded 3/2 valve; loss of loop/charge APPLIES the T04; no 4th dry-break; tow = lockable 2-way ball valve ≥ 420 bar (L4.2) -16 across A/B (HYDAC KHB class) with limit switch

### Welds (AWS D1.1, E70XX, prequalified WPS unless noted)
- Motor bracket PL25 A572-50 to transom: 2 × 400 × 10 fillet both sides + 2 PL16 gussets (T1-c), MT

### Bolts and torques
- MS05 mounting flange cl.10.9 per Poclain (AWAIT)
- Slide plate 4× M20 cl.10.9, 610 N·m; jack screws M20
- 45T ring web to the Ø350 hub flange 12× M16 cl.8.8 fitted DIN 609/7968 at PCD 300, 219 N·m dry, Nord-Lock, re-torque at 10 h (7.45 kN/bolt at HPRV × 1.5)
- Brake calipers M20 cl.10.9, 610 N·m (dry K 0.20)

### Fixes logged
- L4: Dodge TA7315H15MS + H1B110 + Gates belt REMOVED (owner: no belt) → MS05 + RS120-2 chain 3:1, nothing outside the wheels
- Equal-torque start limited by the lightest axle → L4.1: gear flow divider REJECTED (below min flow at starts, 320 bar section rating < need, +160 kg) → electronic traction control + front ballast for ≥ 1.10 dry; sand mandatory on wet grades
- Pump shaft: AIE SAE B 13T drive would force G4 (fails 1.19 on engine peak) → keep G1 + 14T 12/24 coupling hub (D1-u)
- Spline engagement 70 → 60 mm (full code-5 spline): 95 MPa, util 0.95 (D2-h)
- HighFlow valving required for single-axle spin (D1-d)
- Overspeed trip made independent of PLUS+1 (D1-n)
- Cooler raised to ≥ 14 kW at 43 °C outside air (D1-i); compressor clutch gating + 34.5 kW anti-stall (D1-t)
- Chain case enlarged to ≥ 15 mm radial at 3% + travel (D2-g)
- Charge pump: Danfoss 10 % rule gives ~193 cc for LSHT motors (meaningless) → OPEN item; charge filter added
\pagebreak
## 5 Brakes - service, emergency, parking

### Governing codes and standards
- ASTM F2291-23 §6 (fail-safe brakes, controls) and F1193; ASTM F770 (operations)
- Air components to SAE J1410/J1402 & FMVSS 121 component practice (reference); NFPA 70 for controls
- 49 CFR 232 used as practice reference only (not applicable)

### Load cases and basis
- Brake force set at μ_use 0.12 of TARE (empty) axle load on every braked axle → no wheel slide on wet rail empty or loaded (μ wet 0.15)
- Braked: 4 loco driven axles (axle disc, 2 calipers), 4 tender axles, 16 coach axles; lead truck unbraked
- Emergency = spring-applied on BP exhaust (fail-safe); service = 70% of emergency; parking = same spring units
- Cases on 2% DESCENDING, reaction/propagation 1.5 s, from the GOVERNED 6 mph (owner-selected, PE to confirm) and the 7 mph overspeed trip; loaded train. 10 mph shown for information only (hardware capability, not permitted)

### Hand calculations

| ID | Check | Inputs | Formula | Demand | Capacity | Unit | Util | Status | Note |
|---|---|---|---|---|---|---|---|---|---|
| B1-a | Emergency braking force vs wet adhesion of braked tare (no slide) | F = 0.12·ΣW_tare (562 kN) | F/ (0.15·ΣW_tare) | 67.472 | 84.34 | kN | 0.80 | OK |  |
| B1-b | Emergency stop from governed 6 mph on 2% down, loaded - distance vs 20 m criterion (ASSUMED) | a = F/m - g·0.02 = 0.632 m/s² | d = v·t + v²/2a | 9.719 | 20 | m | 0.49 | OK |  |
| B1-c | Emergency stop from the 7 mph overspeed trip on 2% down | a 0.632 m/s² | d = v·t + v²/2a | 12.446 | 30 | m | 0.41 | OK | 30 m criterion ASSUMED. Information only: from 10 mph (hardware capability, not permitted) 22.5 m |
| B1-d | Service stop from governed 6 mph on 2% down (70% force) vs 30 m | a = 0.383 m/s² | d = v·t + v²/2a | 13.409 | 30 | m | 0.45 | OK |  |
| B1-e | Parking: all spring brakes hold loaded train on 2%, FS 1.5 | required 1.5·0.02·W | F_avail = ΣF_spring | 23.981 | 67.472 | kN | 0.35 | OK |  |
| B1-f | Parking on loco spring brakes ALONE (train) - not permitted | loco 4 discs |  | 23.981 | 20.604 | kN | 1.16 | FIXED by rule - train parks with all spring brakes + chocks | NG → procedure: train parks with BP exhausted (all cars spring-applied) + chocks; loco alone may hold only itself |
| B1-g | Loco AXLE disc (L3, Y+ side away from the reducer) - clamp needed PER CALIPER with 2 calipers per disc (Ø340, r_eff 135, μ_pad 0.35) vs spec 22 kN | T_axle 3.73 kN·m (1:1 - no gear multiplication) | N = T/(2 calipers · 2 μ r) | 19.759 | 22.0 | kN | 0.90 | OK | Reference: Coremo Ocmea D 3.5N spring-applied air-released, 24.2 kN clamp (supplier §5) - AWAIT brake supplier. Burnish pads at commissioning (initial torque 30-50 % low until bedded) |
| B1-l | Caliper release air: regulated supply vs Coremo D 3.5N max release pressure | MR 8.5 bar → regulator | spec | 6.0 | 6.0 | bar | 1.00 | OK | Dedicated regulated release-air supply off MR (6 bar max for Coremo; 5.1 bar min) - supplier F9 |
| B1-h | Coach axle disc caliper clamp needed (Ø300 disc, r_eff 125) vs spec 10 kN | T_axle 0.71 kN·m | N = T/(2 μ r) | 8.11 | 10.0 | kN | 0.81 | OK | Spring-applied caliper ≥ 10 kN clamp (AWAIT supplier) |
| B1-i | Loco disc temperature rise, one emergency stop on 2% | E 449 kJ, share 0.076 | ΔT = E·share/(m_disc c) | 4.178 | 150 | K | 0.03 | OK |  |
| B1-j | Drag braking 100 m of 2% at governed 6 mph - loco disc ΔT | (0.02-0.005)·W·100 m | ΔT = E·share/(m c) | 11.168 | 150 | K | 0.07 | OK | Unit case; real route descents in B1-j2 (2% is the GOVERNING design grade - the track is NOT level) |
| B1-j2 | Drag braking the longest continuous route descent (redline Alt A-D: 7.68 m fall over 505 m, avg 1.52%) at governed 6 mph - loco disc ΔT, NO cooling credit | E = W·(Δz - 0.005·L) | ΔT = E·share/(m c) | 38.382 | 150 | K | 0.26 | OK | Adiabatic upper bound (≈ 3.2 min at 6 mph, disc cooling ignored). Hydrostatic/engine braking credit would reduce it - AWAIT. Ops rule: ≤ 6 mph on descents |
| B1-k | Emergency in-train buff at loco-tender drawbar vs 70 kN service | trailing mass × a - trailing brake force |  | 4.104 | 70 | kN | 0.06 | OK |  |
| B1-m | MS05 T04 parking brakes (4 motors through 3:1) hold the LOCO ALONE on 2%, FS 1.5 | 1.5·0.02·W_loco | F = ΣT04·3/r | 5.865 | 52.4 | kN | 0.11 | OK | Loco alone only - a train parks on all spring brakes (B1-e/f) |
| B1-n | MS05 T04 dynamic (emergency) energy per motor, loco-only stop from 6 mph vs catalog limit | max 10 dynamic applications (Poclain) | E = ½mv²/4 | 17.9 | 85.9 | kJ | 0.21 | OK | Release by charge pressure via a PLUS+1 solenoid + accumulator: applied only on park or < 0.5 mph (engine stall does NOT dump them) |
| B1-o | Loco brake ratio matched to the coaches (draft-gear run-in, K1-a3): loco emergency decel vs coach decel | loco 0.690 / tender TB-3.13d 5.845 kN = 0.671 / coaches 0.69 m/s² | spec | 0.69 | 0.69 | m/s² | 1.00 | OK | REQUIRED (Stress Bot R3): loco SERVICE and emergency brake rate ≤ 0.69 m/s² (= loaded coaches) - caliper clamp / relay valve set at commissioning; brake test records the loco-alone decel |
| B1-p | Fail-safe brake logic (BP 5.0 bar UIC / Knorr KE + WABCO IR-2 971 899 152 0 inverting relay + ASCO 8210G035 24 VDC de-energize-to-vent): loss of BP, MR or 24 V → spring apply | 4 failure paths on B-601 | spec | 1 | 1 | logic | 1.00 | OK | PE to verify PL of the s30 → ASCO / CCO path; AWAIT WABCO IR-2 curve vs Coremo release 5.1-6 bar |

### Materials
- Discs: loco Ø340×25 on the axle (Y+, free side), 2 calipers each, coach/tender Ø300×20, cast iron GG25/ductile, or 4140 (ASSUMED)
- Pads sintered, μ 0.35-0.40 (ASSUMED; AWAIT supplier)
- Loco caliper reference Coremo Ocmea D 3.5N (25.4 mm disc thickness check AWAIT); release air via 6 bar regulator off MR; MS05 T04 multidisc brakes = loco-only parking + motor emergency (B1-m/n)
- Air: 3 × Midland Haldex 19820 main reservoirs (47 L, 150 psi) on the tender X3600-4440 (TB-3); BP 5.0 bar, MR cut-out 8.5 bar, safety valve 10 bar; Ingersoll Rand 2340 compressor with electric clutch (tender)
- Towing: wind-off calipers + T04 release screws + H1P053 tow bypass, max 2 mph (tag-out)

### Bolts and torques
- Caliper mounts M20 cl.10.9, 610 N·m (dry K 0.20), Loctite 243 + witness mark

### Fixes logged
- Tare-based brake ratio 12% adopted (loaded-only sizing slid empty coaches on wet rail)
- L3: loco brake back on an axle disc on the free side (Y+); axle torque is 1:1 so 2 spring calipers per disc (B1-g)
- Parking rule: never rely on loco brakes alone for a train (B1-f)
- r_eff 145 → 135 mm per real calipers: clamp 17.5 → 18.8 kN, 22 kN spec still holds (supplier F8)
- Commissioning: pad burnish/bedding step before brake tests; regulated release-air supply (supplier F8/F9)
- L4: MS05 T04 parking/emergency brakes (B1-m/n), independent overspeed relay to BP exhaust, tow release procedure, loco brake ratio matched to coaches (B1-o)
\pagebreak
## 6 Couplers, drawbars and end restraint

### Governing codes and standards
- AISC 360-22 (ASD) pins, plates, net section; AWS D1.1
- ASTM F2291 §6 (secondary restraint of coupled vehicles); NACM chain WLL

### Load cases and basis
- Service 70 kN (≥ 1.9 × max adhesion-limited start 36.96 kN)
- Ultimate 200 kN (≈ 2.6 × train weight × 0.1 g impact - ASSUMED)
- Curving R100 lateral components

### Hand calculations

| ID | Check | Inputs | Formula | Demand | Capacity | Unit | Util | Status | Note |
|---|---|---|---|---|---|---|---|---|---|
| C5 | Loco rear drop box PL16 A572-50 root bending, 70 kN | Lever 600 mm, box 552×400 mm | see PF-CT_R2_calc_notes (calcs.py) | 8.9 | 207.0 | MPa | 0.04 | OK |  |
| C5 | Loco rear drop box PL16 A572-50 root bending, 200 kN | Lever 600 mm, box 552×400 mm | see PF-CT_R2_calc_notes (calcs.py) | 25.6 | 345.0 | MPa | 0.07 | OK |  |
| C5w | Loco rear box root weld, 10 mm fillet all round, 200 kN | E70 weld metal: 0.6×FEXX = 289 MPa nominal (ultimate case) | see PF-CT_R2_calc_notes (calcs.py) | 67.5 | 289.2 | MPa | 0.23 | OK |  |
| C5 | Tender drop box PL16 A572-50 root bending, 70 kN | Lever 286 mm, box 702×400 mm | see PF-CT_R2_calc_notes (calcs.py) | 3.0 | 207.0 | MPa | 0.01 | OK |  |
| C5 | Tender drop box PL16 A572-50 root bending, 200 kN | Lever 286 mm, box 702×400 mm | see PF-CT_R2_calc_notes (calcs.py) | 8.7 | 345.0 | MPa | 0.03 | OK |  |
| C5w | Tender box root weld, 10 mm fillet all round, 200 kN | E70 weld metal: 0.6×FEXX = 289 MPa nominal (ultimate case) | see PF-CT_R2_calc_notes (calcs.py) | 31.0 | 289.2 | MPa | 0.11 | OK |  |
| C6a | Drawbar PL32×150 A572-50 net tension at Ø61 hole, 200 kN | Net section (150−61)×32 | see PF-CT_R2_calc_notes (calcs.py) | 70.2 | 345.0 | MPa | 0.20 | OK |  |
| C6b | Drawbar bearing on Ø60 pin, 200 kN | Bearing limit 1.5 Fy (ultimate case) | see PF-CT_R2_calc_notes (calcs.py) | 104.2 | 517.5 | MPa | 0.20 | OK |  |
| C6c | Drawbar 1473 mm buckling (weak axis, pinned) at 70 kN buff | Euler Pcr=373 kN; require ≥2.0× service | see PF-CT_R2_calc_notes (calcs.py) | 140,000.0 | 372,635.5 | N | 0.38 | OK | Pins allow rotation in plan; vertical rotation restrained by pocket plates - pinned assumed (conservative). |
| C6c | Drawbar 800 mm buckling (weak axis, pinned) at 70 kN buff | Euler Pcr=1263 kN; require ≥2.0× service | see PF-CT_R2_calc_notes (calcs.py) | 140,000.0 | 1,263,309.4 | N | 0.11 | OK | Pins allow rotation in plan; vertical rotation restrained by pocket plates - pinned assumed (conservative). |
| C6d | Pin Ø60 4140 Q&T bending, 200 kN, spacer bushings (4 mm gap) | Double shear pin; M=F/2×(gap+t_plate/2+t_bar/4) | see PF-CT_R2_calc_notes (calcs.py) | 103.7 | 655.0 | MPa | 0.16 | OK |  |
| C6e | Pin Ø60 double shear, 200 kN |  | see PF-CT_R2_calc_notes (calcs.py) | 35.4 | 393.0 | MPa | 0.09 | OK |  |
| C6f | Pocket plates PL20 bearing on pin, 200 kN |  | see PF-CT_R2_calc_notes (calcs.py) | 83.3 | 517.5 | MPa | 0.16 | OK |  |
| C6g | Safety chains 2× Grade 100 1/2 in, WLL vs 70 kN service | NACM WLL 15,000 lbf each (verify with chain supplier certificate) | see PF-CT_R2_calc_notes (calcs.py) | 70,000 | 133,400 | N | 0.52 | OK |  |
| C6h | Safety chains 2× Grade 100 1/2 in, MBS vs 200 kN | Min. break = 4×WLL per NACM grade 100 | see PF-CT_R2_calc_notes (calcs.py) | 200,000 | 533,600 | N | 0.37 | OK |  |
| K1-a | Coach drawbar angle on R100 WITH ≥10 m spirals (steady) - empty coach leading-wheel L/V = curving Y/Q (Heumann) + drawbar lateral at max adhesion TE 37.9 kN | angle (5180+736.5)/R = 3.39° (old K1-a 1.82° was 1.86× low); Q empty 9.86 kN; Y/Q curving 0.861 | L/V = Y/Q + F·sinθ·(1+o/s)/(2Q) | 1.025 | 1.342 | L/V | 0.76 | OK | Nadal 70°, μ 0.3 (1.34) - quasi-static; gauge-face lubrication recommended |
| K1-a2 | Same, Alt A as drawn (tangent-arc, NO spirals): transient drawbar angle from the 3-D sweep | angle 7.30° (1.9-2.1× steady) | L/V = Y/Q + F·sinθ·(1+o/s)/(2Q) | 1.214 | 1.342 | L/V | 0.91 | OK | Passes at the 37.9 kN adhesion limit; 70 kN service buff would give 1.51 (NG) - see K1-a3/K1-d: 10 m spirals recommended on every curve |
| K1-a3 | In-train buff/draft that keeps the empty-coach wheel at Nadal on Alt A as drawn (R100, no spirals) vs max force with PRELOADED draft gear (k 20 kN/mm, 1.0 mm TOTAL play at the renew limit) | allowable 51.7 kN (tender 38.5); 2 mm slack @ 50 kN/mm gives 67.4/65.6 kN | 6-mass lumped model (calcs/track/drawgear.py) | 35.3 | 38.5 | kN | 0.92 | OK | REQUIRED (Stress Bot R3): preloaded draft gear, renew at 1.0 mm TOTAL play (F770 inspection), k ≥ 20 kN/mm (≤ 100 on the R80 route, K1-h); loco brake rate ≤ 0.69 m/s² (B1-o) |
| K1-b | Pin retention: head + Ø10 cross-bolt + R-clip vs 1 g up-lift of drawbar (end restraint) | drawbar 1473 PL32×150 = 55 kg | τ cross-bolt | 20.602 | 256.0 | MPa | 0.08 | OK | 3 g vertical |
| K1-c | Max service drawbar force (adhesion-limited start) vs 70 kN design | μ 0.25 dry on drivers |  | 37.11 | 70 | kN | 0.53 | OK |  |
| K1-d | Drawgear slack: start snatch / emergency run-in with 2 mm slack per joint (k 50 kN/mm, steel pins) vs 70 kN service | 6-mass model; loco 1.03 vs cars 0.69 m/s²; brake 0.3 s + 0.25 s/car |  | 67.4 | 70 | kN | 0.96 | OK | 1 mm at 200 kN/mm already gives 79-88 kN; 10 mm @ 50 gives 158 kN (Stress Bot 206-235 with 48 kN HPRV TE). Matching the loco brake ratio only trims run-in 10-15 %: slack control governs |
| K1-e | DB-800 loco-tender (kept as drawn): exact-geometry swing at R60 - tender pocket (300 mouth) | loco side 19.32° vs 32.4° | 2-D pin geometry (drawbar_L4.py) | 10.98 | 19.2 | deg | 0.57 | OK | PASS; transient on spirals: route L4 (K2-r) |
| K1-f | Drawbar pin Ø60 length under head vs grip 108 + washer + cross-bolt hole + end distance (L-104 drawn 250 corrected) | grip 108 + 2 + 15 + 15 |  | 140 | 150 | mm | 0.93 | OK | Specify 150 under head (170 o/a); 12 pins (10 + 2 spares) |
| K1-h | Draft-gear basis (Stress Bot R3): 1.0 mm TOTAL play at the renew limit, k swept 20-200 kN/mm, loco brake ≤ 0.69 m/s² - peak start-snatch / run-in force at k 100 vs route F (R80) coach buff allowance | k 20: 35.3 kN; k 100: 41.3 kN; k 150: 50.1 kN (NG) | 6-mass model (calcs/track/drawgear_S3.py) | 41.3 | 45.8 | kN | 0.90 | OK | Specify k 20-100 kN/mm for R80 (route E R70 allowance 38.8 kN limits k to ≤ 25). Stiffer is NOT safer: k 150-200 gives 50-55 kN |
| K1-g | Safety chain 5/8 in G100 WLL vs 70 kN single-chain service; shackle Crosby G-2130 1 in WLL 83.4 kN | 2 per joint |  | 70 | 83.4 | kN | 0.84 | OK | Chain WLL 100.5 kN; shackle governs |

### Materials
- Drawbars PL32×150 A572-50; pins Ø60 4140 Q&T, H8/f7; bushes 4140
- Safety chains 2 × 5/8 in Grade 100 per joint (WLL 100.5 kN each) with Crosby G-2130 1 in bolt shackles (WLL 8.5 t)
- 5 joints: DB-800 loco-tender, DB-1473 elsewhere; 12 pins Ø60 × 150 under head (10 + 2 spares)

### Welds (AWS D1.1, E70XX, prequalified WPS unless noted)
- Pocket plates PL20 to box: 10 mm fillet all round, MT

### Bolts and torques
- Cross-bolt M10 cl.8.8 + nyloc, 50 N·m (dry K 0.20)

### Fixes logged
- F11: safety chains added
- Spacer bushings limit pin gap to 4 mm (C6d) - SUPERSEDED 28 Oct: 4 mm pin gap gives > 70 kN snatch/run-in (K1-d); basis now (Stress Bot R3) 1.0 mm TOTAL play renew limit, preloaded draft gear k ≥ 20 kN/mm (≤ 100 for R80, K1-h)
- K1-a corrected 28 Oct 2026: drawbar angle (5180+736.5)/R (was (2437+736.5)/R, 1.86× low) + curve-entry transient from the 3-D sweep; L/V now includes the curving guidance force (Heumann) and uses Nadal 1.34 (μ 0.3), not 0.8
\pagebreak
## 7 Tender T2 - structure, engine/pump/genset mounts, fuel, cooling

### Governing codes and standards
- AISC 360-22; AWS D1.1 / D1.3 (sheet)
- NFPA 30A / 49 CFR 393.65-.67 (fuel tank practice, reference); NFPA 37 (stationary engines, reference)
- EPA Tier 4 engine (AIE V3307) installation per AIE/Kubota manual (AWAIT)

### Load cases and basis
- Equipment restraint 3 g long. / 2 g vert. / 1 g lat. (ASSUMED, same as ballast)
- Ambient 43 °C (110 °F) cooling design

### Hand calculations

| ID | Check | Inputs | Formula | Demand | Capacity | Unit | Util | Status | Note |
|---|---|---|---|---|---|---|---|---|---|
| E-AIE  | AIE V3307 package + radiator + H1P053 mount bolts 2×M16 cl.8.8 per isolator: combined T+V (AISC J3.7) | 610 kg, CG 500 above mounts, mount spacing 900 long.; Fx 3 g = 17.9 kN | (ft/Ft)²+(fv/Fv)² ≤ 1; Ft 0.75Fu/2, Fv 0.45Fu/2 (threads incl.) | 0.008 | 1.0 | interaction | 0.01 | OK | Isolator rated ≥ 3.5 kN uplift / 4.5 kN shear - AWAIT isolator supplier |
| E-Gens | Genset PTI-38 (TB-3 layout approved; X1060-2768) mount bolts 2×M16 cl.8.8 per isolator: combined T+V (AISC J3.7) | 699 kg, CG 550 above mounts, mount spacing 1300 long.; Fx 3 g = 20.6 kN | (ft/Ft)²+(fv/Fv)² ≤ 1; Ft 0.75Fu/2, Fv 0.45Fu/2 (threads incl.) | 0.009 | 1.0 | interaction | 0.01 | OK | Isolator rated ≥ 2.6 kN uplift / 5.1 kN shear - AWAIT isolator supplier |
| E-rail | Tender main rail HSS10x4x1/4 between pivots (2,600), all equipment ×2.0 | w = 10.40 N/mm per rail | M = wL²/8 ×2.0 | 68.803 | 345 | MPa | 0.20 | OK |  |
| E-fuel | Fuel tank 150 L strapped: 2 straps 50×6 A36 at 3 g | tank 40 kg + 126 kg diesel | σ = 3mg/(2·A) | 8.14 | 150 | MPa | 0.05 | OK |  |
| E-air | Tender cooling air: engine (45.6) + genset engine (~42 kW) jacket heat at ΔT_air 15 K, louvre free area at 3 m/s vs provided 2×0.9 m² | V̇ = Q/(ρ cp ΔT) = 5.05 m³/s | A = V̇ / 3 m/s | 1.683 | 1.8 | m² | 0.94 | OK | Louvres 0.9 m² free area per side (intake one side, discharge other) - specified |
| E-run | Fuel endurance: 150 L vs 5 h evening (Tender Bot duty 14.6 L/h) | full-power screen 19.1 L/h | t = V/q | 73.0 | 135.0 | L | 0.54 | OK | 90% usable |
| E-cg | Tender TB-3.13d (8,706.5 kg, CG [2422.7, 11.3, 1110.4], Tender Bot) - max wheel load vs the 26 kN rail basis | front truck share 53.0 % | lever about the pivots X1200 / 3800; ΔQ = Q·y/980 | 11.442 | 26.0 | kN | 0.44 | OK | L4.2: TB-3.13d (+59.9 kg vs TB-3.11) supersedes TB-3.11 8,646.6 / TB-3.9 8,616.3 / TB-3.8 8,568.8 |
| E-xh | Under-deck transformer cradle hangers (TB-3.4): 4 × L3x3x1/4, each 2 × M16 8.8 × ~140 through both HSS10x4 walls at mid-web Z963 with DOM 25.4 × 3.05 crush tubes (no welds on the rails; nearest bolt 81 mm from the X2449 crossmember weld ≥ 3d 48); whole 168.7 kg assembly at 3 g vertical + 1 g | V = 168.7·9.81·4 / 8 bolts | bolt shear, threads in the plane | 0.827 | 30.144 | kN | 0.03 | OK | Tender Bot: ~330 N/bolt on the 89.6 kg isolated mass at 3 g; torque M16 8.8 with crush tubes per the frame standard (153 N·m lubricated) |

### Materials
- Rails HSS10x4x1/4 A500C; bolsters fish-belly PL10/12 A36; deck 6 mm tread plate A786
- Skin 10 ga A1011; posts HSS2x2x1/8; fuel tank 3 mm 5052 Al or 12 ga steel with baffles, vent, rollover check valve

### Welds (AWS D1.1, E70XX, prequalified WPS unless noted)
- Engine/genset mount pedestals PL16 to rails: 8 mm fillet all round
- Deck tread plate stitch 6 mm 50 @ 300 to bearers (sealed seam with sealant)

### Bolts and torques
- Isolator bolts M16 cl.8.8, 219 N·m (dry K 0.20), Nord-Lock
- Fuel tank straps M12 cl.8.8, 88 N·m (dry K 0.20)

### Fixes logged
- Pump H1P045 → H1P053 (§4) - same SAE B pad (AWAIT Danfoss/AIE fit)
- Cooling louvres sized (E-air)
- L4 (Tender Bot): hydraulic cooler ≥ 14 kW on the LEFT wall X3455-4145; rev TB-3 layout APPROVED 28 Oct: genset X1060-2768, R-wall NEMA 3R cabinet X2820-3780 (listed UL 1008 ATS with integral main; separate QOM22225NRB main, handle ≤ Z1639), 150 L custom tank X3900-4500 behind X3800 firewall, ODX-AGM34, 3 × Haldex MR X3600-4440; tender 8,706.5 kg (TB-3.13d, CG [2422.7, 11.3, 1110.4]; was TB-3.11 8,646.6, TB-3.8 8,568.8, TB-3.4 8,465.3) incl. the 168.7 kg under-deck shore transformer assembly (Acme T2535173S 15 kVA NEMA 3R on isolators, L3x3x1/4 cradle hung from the HSS rails by 2 × M16 8.8 through-bolts per hanger at mid-web Z963 with crush tubes - no welds on the rails, 3 mm shield 450 × 1,120 at Z300, inrush limiter on the cradle X2360-2665; nothing under the deck aft of X2900); tender CG + axle loads rerun on the real T2 CG (E-cg)
- Genset PTI-38 (699 kg) in the approved TB-3 reservation (≤ 1,775 long). Rated 40 °C, NOT the 43 °C design day; NO UL 2200 listing shown - derate letter + listing OPEN
\pagebreak
## 8 Generator sizing and selection recommendation

### Governing codes and standards
- NFPA 70 (NEC) 2023 Art. 445 (generators), 250.35 (separately derived), 522/525 (amusement attractions)
- ISO 8528-1 rating definitions (COP/PRP)

### Load cases and basis
- Plan basis (tender-lt45 / systems-p1): electrical demand 26.8 kW hot dry evening, 31.7 kW hot dry day, 39.7 kW hot humid (110 °F / 75 °F, Δw 0.006, +15 %, COP 2.5, incl. 4.288 kW aux)
- Outside air per ASHRAE 62.1-2022 Table 6-1 'transportation waiting' analog (Rp 3.8 L/s·person, Ra 0.3 L/s·m², cabin 20.5 m², Ez 1.0 low-level supply): regular coach 33 occ. → 131.5 L/s (279 cfm), accessible 14 occ. → 59.3 L/s (126 cfm); train 454 L/s vs plan 847.5 L/s (7.5 L/s·person)
- OA load at basis conditions 41.48 W thermal per L/s = 19.08 W electric per L/s (×1.15 / COP 2.5); 62.1 OA sensible 10.7 + latent 8.2 kW thermal
- ERV: RenewAire HE05IN (120 V, 120-375 cfm, AHRI 1060 core L62-G5) one per coach; total effectiveness 0.55 cooling ASSUMED - AWAIT RenewAire selection printout; fans ≤ 343 W vs 250 W plan allowance (+0.27 kW train)
- Superseded: rev. A §8 used COP 3.0 and ΔT 11.1 K with 60 % effectiveness - inconsistent with the 39.7 kW plan basis; corrected here to the plan basis

### Hand calculations

| ID | Check | Inputs | Formula | Demand | Capacity | Unit | Util | Status | Note |
|---|---|---|---|---|---|---|---|---|---|
| G1-a | Hot-humid demand WITHOUT fix (plan OA 847.5 L/s) vs 35 kW continuous | plan 39.7 kW |  | 39.7 | 35.0 | kW | 1.13 | FIXED - ERV + staging (G1-b) | NG - the 4.7 kW shortfall |
| G1-e | ERV total effectiveness REQUIRED to reach 34.4 kW (plan OA 847.5 L/s, incl. +0.27 kW fan delta) vs selected 0.55 ASSUMED | OA electric share 16.17 kW | ε = (D0 + ΔPfan - 34.4)/P_OA | 0.344 | 0.55 | - | 0.62 | OK | COP 3 sensitivity ε ≥ 0.393; at 62.1 OA ε ≥ 0 (OA cut alone reaches 32.19 kW) |
| G1-b | Hot-humid demand WITH HE05IN ERVs (ε 0.55), plan OA 847.5 L/s - governing | ERV saves 8.89 kW electric; fans +0.27 kW | D = 39.7 - ε·Q·19.08 W/(L/s) + ΔPfan | 31.08 | 34.4 | kW | 0.90 | OK |  |
| G1-f | Hot-humid demand WITH ERVs at 62.1 OA (454 L/s) - design flow | no-ERV 32.19 kW; ERV saves 4.76 kW | same | 27.7 | 34.4 | kW | 0.81 | OK |  |
| G1-c | Largest step load (staged starts: inverter heat pumps soft-start, 1 coach at a time) vs 35 kW | running 31.08 + one inverter ramp 1.5 kW (ASSUMED) |  | 32.58 | 38.5 | kW | 0.85 | OK | Gen-set transient capability 110% (ISO 8528 PRP) - AWAIT genset data |

### Design statements
- Recommendation: keep the 35 kW CONTINUOUS (ISO 8528 COP, not standby) single-phase 120/240 V 60 Hz Kubota-powered enclosed set that fits the rev TB-3 tender reservation (X1060–2768, i.e. 1,708 long, allow up to 1,775 × 800 × 1,000, ≤ 900 kg; layout basis PowerTech PTI-38 1,708 × 667 × 864, 699 kg), derated for 43 °C at the site, AND close the hot-humid gap with one RenewAire HE05IN ERV per coach + a demand/staging controller (shed 1 coach compressor stage if total > 33 kW).
- ERV location: a low clerestory-style roof pod on each coach (unit 880 × 956 × 307 mm, 43 kg), top ≤ 3,450 mm above rail (coach roof peak 3,089; locomotive roof 3,700; K-401 overhead 4,300). The R2 coach has no ceiling plenum (finished ceiling ≈ roof) and the end-hood pocket (1,217 W × 544 D × 431 H mm above the door header) is too shallow for any 300-cfm unit found. OA louvre and EA louvre on opposite sides/ends of the pod (62.1 Table 5-1 separation - PE to confirm).
- Alternates (data verified this turn, see calcs/erv/erv_selection.md): Mitsubishi Lossnay LGH-F300RVX2-E (208/230 V, 300 cfm, 331 mm tall, 34 kg - rejected: intake limited to 40 °C / 80 % RH, below the 43 °C design day); Fantech ATMO 300E-EC (120 V, 301 cfm, 546 mm tall - too tall for a low pod); Panasonic FV-10VEC2 (120 V, 100 cfm, 225 mm tall - 3 needed per regular coach). No 12/24 V ERV of this airflow was found.
- Alternative if ERVs are rejected: 45 kW continuous set (needs bay re-check - the LT45.1 gaps 124/94/25 mm will not take a larger enclosure without re-layout).
- Tender layout rev TB-3 (Tender Bot design_basis §11, APPROVED 28 Oct 2026): genset X1060–2768 Y417–1084; right-wall outward-facing NEMA 3R electrical cabinet X2820–3780 (panel QO142M225PRB, factory-enclosed listed 200 A NEMA 3R UL 1008 ATS with integral main, charger SENS S2); main breaker in a SEPARATE QOM22225NRB enclosure with its handle at Z ≤ 1,639 above top of rail (NEC 404.8 met without a step); custom 150 L 5052 Al fuel tank X3900–4500 behind a steel firewall at X3800; genset start battery ODX-AGM34 X2850–3200; 3 × Haldex 19820 main reservoirs X3600–4440. Tender ≈ 8,465.3 kg (Tender Bot TB-3.4, Steering 16): under-deck shore transformer ASSEMBLY 168.7 kg at CG [2502, 24, 608] between the frame rails - Acme T2535173S 15 kVA UL 506 NEMA 3R upright (Z420–851) on 4 elastomer isolators, L3x3x1/4 cradle (cross angles X2280–2356 / X2644–2720) hung from the HSS rails by 2 × M16 8.8 through-bolts per hanger at mid-web Z963 with DOM crush tubes (no welds on the rails, ≥ 3d from any weld), bolted 3 mm ballast/spray shield 450 × 1,120 at Z300, inrush limiter on the cradle box rails X2360–2665 (nothing under the deck aft of X2900); placed equipment 2,051.9 kg at CG ≈ [2221, +41, 1480]. Tender CG on the real T2 structure CG: [2433, +10, 1109] (E-cg). Transformer top vs X2500 crossmember: CLASH 15 mm (K2-xf).
- Genset purchase is NOT released (spec approval first) - procurement spec above; AWAIT supplier quotes.

### Fixes logged
- 4.7 kW shortfall closed by HE05IN ERV + staging (G1-b 31.1 kW at plan OA; 27.7 kW at 62.1 OA) - owner/PE decision on ERV vs 45 kW set
- §8 rev. A COP 3.0 / ΔT 11.1 K inconsistency corrected to plan basis (COP 2.5, ΔT 19.4 K)
\pagebreak
## 9 Coaches R2 - frame, body, roof, floor, doors, stairs, seating, restraint, egress

### Governing codes and standards
- AISC 360-22; AWS D1.1/D1.3
- ASTM F2291-23 §6 (patron containment, restraint analysis), F770 (operations, evacuation), F1193
- IBC 2021 §1607 (100 psf assembly floor, 50 plf / 200 lb guards), §1011 stairs; NFPA 101 §7 egress (reference)
- 2010 ADA Standards §234/1002 amusement rides - accessible coach (PE/owner)

### Load cases and basis
- Floor 100 psf (4.79 kPa) crowd + 300 lb point; dead 0.5 kPa
- Seats: 3 g longitudinal on seat + occupants (ASSUMED; F2291 accel. envelope ≤ 0.2 g at the governed 6 mph)
- Roof 20 psf maint. + 300 lb point; wind 100 mph parked on walls (ASCE 7-22 basic, ASSUMED)
- Guards 50 plf / 200 lb at 42 in

### Hand calculations

| ID | Check | Inputs | Formula | Demand | Capacity | Unit | Util | Status | Note |
|---|---|---|---|---|---|---|---|---|---|
| C1 | Coach main rail HSS12x4x1/4 bending, vertical ×1.3 | Sprung loaded coach 9476 kg uniform on 2 rails over 10160 mm, bolsters at 2337/7823 mm; M=12.5 kN·m/rail at ×1.0 | see PF-CT_R2_calc_notes (calcs.py) | 48.0 | 207.0 | MPa | 0.23 | OK | ×1.3 service vs 0.6Fy; ×2.0 overload vs Fy. Side sills and floor ignored (conservative). |
| C1 | Coach main rail HSS12x4x1/4 bending, vertical ×2.0 | Sprung loaded coach 9476 kg uniform on 2 rails over 10160 mm, bolsters at 2337/7823 mm; M=12.5 kN·m/rail at ×1.0 | see PF-CT_R2_calc_notes (calcs.py) | 73.8 | 345.0 | MPa | 0.21 | OK | ×1.3 service vs 0.6Fy; ×2.0 overload vs Fy. Side sills and floor ignored (conservative). |
| C1d | Coach end-overhang deflection (×1.0) | Cantilever 2337 mm; limit L/360 | see PF-CT_R2_calc_notes (calcs.py) | 1.7 | 6.5 | mm | 0.25 | OK |  |
| C1b | Coach main rail, vertical ×1.3 + 70 kN buff (eccentric) | Coupler 550 mm vs rail centroid 635 mm: e=85 mm | see PF-CT_R2_calc_notes (calcs.py) | 64.2 | 207.0 | MPa | 0.31 | OK |  |
| C2 | Coach bolster HSS12x4x1/4 + 2×PL10×100 doublers, centre load ×1.3 | P=46.5 kN at centre plate, span 1728 mm (rail c/c), simply supported | see PF-CT_R2_calc_notes (calcs.py) | 76.7 | 207.0 | MPa | 0.37 | OK | Doublers PL10×100 top+bottom over centre 600 mm; internal PL10 diaphragm each side of centre plate. |
| C2 | Coach bolster HSS12x4x1/4 + 2×PL10×100 doublers, centre load ×2.0 | P=46.5 kN at centre plate, span 1728 mm (rail c/c), simply supported | see PF-CT_R2_calc_notes (calcs.py) | 118.0 | 345.0 | MPa | 0.34 | OK | Doublers PL10×100 top+bottom over centre 600 mm; internal PL10 diaphragm each side of centre plate. |
| C10d | Coach platform guard post 1-1/2 in sch 40 A53B, 200 lb at 42 in | Cantilever post from floor/side sill | see PF-CT_R2_calc_notes (calcs.py) | 177.8 | 144.6 | MPa | 1.23 | FIXED - 2 in sch 40 posts |  |
| C10d | Coach platform guard post 2 in sch 40 A53B, 200 lb at 42 in | Cantilever post from floor/side sill | see PF-CT_R2_calc_notes (calcs.py) | 103.3 | 144.6 | MPa | 0.71 | OK |  |
| C15a | Stair tread formed channel 3/16 in (4.8) x 280 go x 40 flanges, 914 span, 300 lb point | Simply supported between stringers; IBC 1607 300 lb concentrated on 4 in² (ASSUMED code basis) | see PF-CT_R2_calc_notes (calcs.py) | 70.4 | 150.0 | MPa | 0.47 | OK |  |
| C15b | Stair tread deflection, 300 lb point | Limit L/240 | see PF-CT_R2_calc_notes (calcs.py) | 0.7 | 3.8 | mm | 0.19 | OK |  |
| C15c | Stair stringer PL8x150 A36, 100 psf crowd + dead (per stringer) | Horizontal span 1550 mm hinge-to-foot; plan area 1.28 m²; 100 psf = 4.79 kPa (IBC 1607 stairs, ASSUMED) | see PF-CT_R2_calc_notes (calcs.py) | 23.6 | 150.0 | MPa | 0.16 | OK |  |
| C15d | Stair stringer deflection (along slope) | Limit L/360 | see PF-CT_R2_calc_notes (calcs.py) | 0.7 | 5.2 | mm | 0.13 | OK |  |
| C15e | Chain stay 3/8 in Grade 70 (x2), foot unsupported, full crowd | Moment of full load about the floor hinge / 548 mm chain lever arm; WLL 6,600 lbf for 3/8 G70 ASSUMED - verify on chain tag / supplier (AWAIT) | see PF-CT_R2_calc_notes (calcs.py) | 5.2 | 29.4 | kN | 0.18 | OK |  |
| C15f | Floor hinge pin Ø25 4140 Q&T (2 per stair), single shear | Hinge reaction with chains loaded; brackets/bolts to side sill by PE | see PF-CT_R2_calc_notes (calcs.py) | 9.4 | 262.0 | MPa | 0.04 | OK |  |
| C15g | Stair handrail 1-1/2 in sch 40 A53B, 200 lb at mid-span (662 along slope) | Posts at treads 1, 3, 5; IBC 1607.9 200 lb any direction (ASSUMED) | see PF-CT_R2_calc_notes (calcs.py) | 27.6 | 144.6 | MPa | 0.19 | OK |  |
| C15h | Stair handrail post 2 in sch 40 A53B, 200 lb at 895 above tread | Fold-flat post locked upright by strut + Ø16 pin | see PF-CT_R2_calc_notes (calcs.py) | 86.6 | 144.6 | MPa | 0.60 | OK |  |
| C15i | Stair handrail post lock pin Ø16 4140, double shear | Couple over 100 mm hinge-to-pin | see PF-CT_R2_calc_notes (calcs.py) | 19.8 | 262.0 | MPa | 0.08 | OK |  |
| R1-a | Floor crossmember HSS6x2x3/16 between rails (1,728) at 900 c/c, 100 psf + DL | w 4.76 N/mm | σ = wL²/8S | 29.138 | 207.0 | MPa | 0.14 | OK |  |
| R1-b | Floor crossmember deflection, live only | L/360 | δ = 5wL⁴/384EI | 0.538 | 4.8 | mm | 0.11 | OK |  |
| R1-c | Outrigger HSS6x2x3/16 cantilever 533 to side sill, floor + wall/roof line 2.0 N/mm |  | M = w a²/2 + P a | 26.82 | 207.0 | MPa | 0.13 | OK |  |
| R1-d | Floor panel (1 in composite) required stiffness per mm width for L/360 at 100 psf, span 900 | spec value to supplier | EI ≥ 5qL⁴·360/(384 L) | 16.368 | 16.368 | N·m²/mm·1e-3 | 1.00 | OK | Spec row - panel supplier to certify EI and 300 lb point (AWAIT) |
| R1-e | Roof bow HSS2x2x1/8 @880 (at each window post), span 2,794, deflection L/180 | 20 psf + 0.25 kPa dead | δ = 5wL⁴/384EI | 19.518 | 15.522 | mm | 1.26 | FIXED - HSS3x2x1/8 bows (R1-f) | NG → FIX: HSS3x2x1/8 roof bows |
| R1-f | Roof bow HSS3x2x1/8 @880 (at each window post), span 2,794, deflection L/180 | 20 psf + 0.25 kPa dead | δ = 5wL⁴/384EI | 7.366 | 15.522 | mm | 0.47 | OK | ADOPTED |
| R1-g | Window post HSS2x2x1/8 @880, 100 mph parked wind (Cp 0.8) + 50 plf lean, span 1,100 | q 980 Pa | M = wL²/8 + P_lean·L/4 | 36.035 | 207.0 | MPa | 0.17 | OK |  |
| R1-h | Bench anchor (4-seat bench, 2 rear anchors) M12 cl.8.8 tension at 3 g | Fx 10.24 kN, CG 600, base 450 | T = Fx·h/(b·2) - DL/4; Ft = 0.75Fu/2·As | 5.972 | 25.29 | kN | 0.24 | OK | Through-bolt to crossmember or 100×100×6 backing plate - no inserts in composite floor |
| R1-i | Egress width: NFPA 101 0.2 in/person (level) for 32 pax vs 2 × 813 end doors |  | W_req = 0.2 in × n | 162.56 | 1,626 | mm | 0.10 | OK |  |
| R1-j | Evacuation time to ground: stair deploy 60 s + 32 pax at 0.5 p/s per stair × 2 stairs vs 180 s (ASSUMED target) |  | t = t_deploy + n/(2·0.5) | 92.0 | 180 | s | 0.51 | OK | Train crew procedure per ASTM F770; drill to verify |

### Design statements
- Occupant restraint (ASTM F2291 restraint analysis): accelerations at the governed 6 mph (owner-selected limit, PE to confirm) with 1.0 m/s² emergency are ≤ 0.11 g longitudinal, ≤ 0.04 g lateral on R100 (quasi-static lateral scales with v²: 0.06 × (6/7.5)²) → seated patrons need seat backs + handholds; no individual restraint; gates latched and interlocked to traction (no movement with a gate open).
- Doors/gates: end doors 32 in (813) clear; platform side gates 42 in high, latched + proximity-switch interlock to the traction-enable loop (fail-safe).
- Emergency-exit stairs both sides at every door (C15, C-304); stowed latches with proximity switches in the same interlock loop.

### Materials
- Underframe: HSS12x4x1/4 rails, HSS6x2x3/16 crossmembers/outriggers/side sills A500C
- Body: HSS2x2x1/8 posts, 16 ga skin, roof bows HSS3x2x1/8 @880 (fix), polycarbonate glazing 6 mm (FMVSS 205 AS-? AWAIT)
- Floor: 1 in composite panel, fire/smoke per NFPA 130 Table A practice (reference)

### Welds (AWS D1.1, E70XX, prequalified WPS unless noted)
- Crossmembers/outriggers to rails: 5 mm fillet all round
- Window posts to side sill and eave: 3 mm fillet all round (D1.3 for 16 ga skin plug welds)

### Bolts and torques
- Bench anchors M12 cl.8.8, 88 N·m (dry K 0.20), nyloc, backing plate
- Stair hinge pins Ø25 4140 + R-clip; handrail posts lock pin Ø16

### Fixes logged
- Roof bows HSS2x2x1/8 @880 deflect 1.12×limit → HSS3x2x1/8 (R1-e/f)
- Guard post 1-1/2 → 2 in sch 40 (C10d)
- Seat anchors through-bolted (R1-h)
\pagebreak
## 10 Electrical (train supply) and coach HVAC

### Governing codes and standards
- NFPA 70 (NEC) 2023 Art. 400 (flexible cords), 445, 250, 522/525; NFPA 101 §7.9 emergency lighting (90 min)
- UL 1995 / AHRI 210/240 HVAC equipment; ASHRAE 62.1 ventilation (reference)

### Hand calculations

| ID | Check | Inputs | Formula | Demand | Capacity | Unit | Util | Status | Note |
|---|---|---|---|---|---|---|---|---|---|
| H1-a | Genset output current 35 kW / 240 V vs main breaker 175 A (125%) |  | I = P/V; OCPD ≥ 1.15·I (445.12) | 145.833 | 175 | A | 0.83 | OK |  |
| H1-b | First train-line jumper (all 4 coaches) type W 2/0 3C+G (ampacity 195 A, NEC 400.5 col. B, ASSUMED) | 34.4 kW target (≥ G1-b 31.1 kW) incl. ERV case | I = P/V | 179.167 | 195 | A | 0.92 | OK | Continuous load ×1.25 |
| H1-c | Coach branch #4 SOOW (70 A) for 10 kW coach peak |  | I = P/V ×1.25 | 52.083 | 70 | A | 0.74 | OK |  |
| H1-d | Voltage drop 65 m train line 2/0 Cu at 143 A, 1-phase | R 0.33 Ω/km (2/0 Cu) | ΔV = 2·I·R·L | 2.556 | 3.0 | % | 0.85 | OK |  |

### Design statements
- HVAC: one inverter heat-pump (mini-split class) per coach + one RenewAire HE05IN ERV per coach (enthalpy core, ε 0.55 ASSUMED - AWAIT printout) in a roof clerestory pod supplying the ASHRAE 62.1 outside-air rate (279 cfm regular / 126 cfm accessible) through low-level side supply; MERV 13 filters; condensate to track drain.
- Staging/demand controller in the tender AC panel: limits total to 33 kW, sheds compressor stages coach-by-coach, keeps ventilation and emergency lights.
- Grounding: genset neutral bonded at the genset (separately derived); equipment grounding conductor through every jumper; GFCI on 120 V receptacles; bonding jumpers across trucks.
- Emergency lighting: battery-backed 90 min per coach; exit/orientation 10 W per coach (plan EL1).

### Fixes logged
- 4.7 kW hot-humid shortfall closed (ERV + staging) - see §8
\pagebreak
## 11 Wind - 40 mph no-run, overturning, tie-downs

### Governing codes and standards
- ASCE 7-22 Ch. 26-29 (parked, basic wind speed - site value AWAIT from ASCE hazard tool; 100 mph ASSUMED)
- ASTM F2291 §6 environmental loads; operating limit per F770

### Hand calculations

| ID | Check | Inputs | Formula | Demand | Capacity | Unit | Util | Status | Note |
|---|---|---|---|---|---|---|---|---|---|
| C11 | Coach empty wind overturning FS at 67 mph gust | Side area 23.2 m², Cd 1.2, centroid Z1750 mm, restoring m·g·gauge/2 | see PF-CT_R2_calc_notes (calcs.py) | 1.5 | 1.4 | FS req/avail | 1.09 | FIXED by rule - 40 mph no-run + tie-downs (C11w, W1) | Requirement FS ≥ 1.5 ASSUMED; engineer to set per ASTM F2291 environmental loads. |
| C11 | Coach loaded wind overturning FS at 67 mph gust | Side area 23.2 m², Cd 1.2, centroid Z1750 mm, restoring m·g·gauge/2 | see PF-CT_R2_calc_notes (calcs.py) | 1.5 | 2.3 | FS req/avail | 0.67 | OK | Requirement FS ≥ 1.5 ASSUMED; engineer to set per ASTM F2291 environmental loads. |
| C11 | Locomotive wind overturning FS at 67 mph gust | Side area 35.0 m², Cd 1.2, centroid Z1900 mm, restoring m·g·gauge/2 | see PF-CT_R2_calc_notes (calcs.py) | 1.5 | 1.8 | FS req/avail | 0.86 | OK | Requirement FS ≥ 1.5 ASSUMED; engineer to set per ASTM F2291 environmental loads. |
| C11 | Tender wind overturning FS at 67 mph gust | Side area 9.5 m², Cd 1.2, centroid Z1430 mm, restoring m·g·gauge/2 | see PF-CT_R2_calc_notes (calcs.py) | 1.5 | 4.2 | FS req/avail | 0.36 | OK | Requirement FS ≥ 1.5 ASSUMED; engineer to set per ASTM F2291 environmental loads. |
| C11w | Coach empty overturning FS at 40 mph gust (adopted no-run limit) | Owner decision R2: no running above 40 mph gusts; parked train tied down (wind tie-downs) | see PF-CT_R2_calc_notes (calcs.py) | 1.5 | 3.9 | FS req/avail | 0.39 | OK |  |
| C11w | Coach loaded overturning FS at 40 mph gust (adopted no-run limit) | Owner decision R2: no running above 40 mph gusts; parked train tied down (wind tie-downs) | see PF-CT_R2_calc_notes (calcs.py) | 1.5 | 6.3 | FS req/avail | 0.24 | OK |  |
| C11w | Locomotive overturning FS at 40 mph gust (adopted no-run limit) | Owner decision R2: no running above 40 mph gusts; parked train tied down (wind tie-downs) | see PF-CT_R2_calc_notes (calcs.py) | 1.5 | 4.9 | FS req/avail | 0.30 | OK |  |
| C11w | Tender overturning FS at 40 mph gust (adopted no-run limit) | Owner decision R2: no running above 40 mph gusts; parked train tied down (wind tie-downs) | see PF-CT_R2_calc_notes (calcs.py) | 1.5 | 11.7 | FS req/avail | 0.13 | OK |  |
| W1-Coac | Coach empty parked 100 mph: tie-down force per windward tie (2 ties) vs G70 3/8 chain WLL 29.4 kN | F 34.1 kN at Z1750; 0.6D restoring | T = (M_o - 0.6 M_r)/(gauge·2) | 20.803 | 29.4 | kN | 0.71 | OK |  |
| W1-Loco | Locomotive parked 100 mph: tie-down force per windward tie (2 ties) vs G70 3/8 chain WLL 29.4 kN | F 51.4 kN at Z1900; 0.6D restoring | T = (M_o - 0.6 M_r)/(gauge·2) | 24.123 | 29.4 | kN | 0.82 | OK |  |
| W1-Tend | Tender parked 100 mph: tie-down force per windward tie (2 ties) vs G70 3/8 chain WLL 29.4 kN | F 14.0 kN at Z1430; 0.6D restoring | T = (M_o - 0.6 M_r)/(gauge·2) | 0.0 | 29.4 | kN | 0.00 | OK |  |

### Design statements
- No-run above 40 mph gust (anemometer at the station, ops rule per F770); all vehicles FS ≥ 3.8 at 40 mph (C11w).
- Parked: 2 ties per vehicle each side (4 per vehicle) to helical anchors / deadman - anchor capacity ≥ 30 kN each AWAIT geotech.
\pagebreak
## 12 Track / rail interface - wheel profile, gauge, curve clearances

### Governing codes and standards
- ASTM F2291 §6 (clearance envelope); AREMA Ch. 4/5 practice (reference); ASCE 40 lb rail section properties

### Hand calculations

| ID | Check | Inputs | Formula | Demand | Capacity | Unit | Util | Status | Note |
|---|---|---|---|---|---|---|---|---|---|
| K2-a | Max static driver wheel load (L4.1: Loco Bot ledger 01:57 - barrel 2,076.2 + saddles 195.7, smokebox 227.9 incl. SBX-7, fittings 40.3, deck +36.3, cab C1 813.9, BT-1 + 2 × 75.4 kg plates + clamp bars in the front pocket, slats 21.9, HL-1 headlamp 25, TC/valve package 28, hub 31.4/axle, no divider, sprung pony) vs revised rail basis 26 kN |  |  | 25.89 | 26.0 | kN | 1.00 | OK | Rail basis raised 24 → 26 kN (ASCE 40 base stress ≈ 101×26/22.85 = 115 MPa vs 172 allow.) |
| FT-1a | Loco front tow lug FT-1 (L-111): 8 × Lindapter HB16-2 in the front end sill, 70 kN at 20°/15°, worst bolt T 14.0 / V 3.7 kN | axial 63.5 kN; shear/bolt 3.67 kN | T/21 + V/30 (HB16 SWL basis) | 0.79 | 1.0 | - | 0.79 | OK | Loco Bot value verified; HB16-2 clamp range to confirm with Lindapter; holes drilled, ≥ 50 mm from weld toes |
| FT-1b | FT-1 end-sill wall yield line (HSS12x6x3/8, t 8.86, panel 278 × 328 clamped, patch 126 × 236) - Loco Bot Pu 220 kN / 1.67 | independent pyramid Pu 280.6 kN (0.9× = 252.5) | 70 / (220/1.67) | 0.53 | 1.0 | - | 0.53 | OK | governing lower bound kept; independent 0.46 |
| FT-1h | FT-1 Crosby G-209 shackle (Loco Bot) |  |  | 0.84 | 1.0 | - | 0.84 | OK | governing FT-1 item |
| K2-a2 | Loco Bot S17: equal-torque dry 2 % start margin after the front-ballast trim (1,056 -> 150.8 kg plates + BT-1 68.2 kg in the pocket) - rule >= 1.10 | lightest axle F2 37.11 kN | rule / margin | 1.1 | 1.14 | - | 0.96 | OK | smokebox 227.9 kg counted in full (no double count: the L3 smokebox front left the base with the ~1,000 kg L3 cab/front) |
| K2-hb | Loco Bot S17: S4N saddle holes at bearer B4 (HSS5x3x3/16, front bolster) Y±250 - net section with the REQUIRED fix (M12 hex rivnuts on the bearer CL, pairs ±25 in Y) | M 7.47 kN·m (LC4P 2 g) | f / (0.6·Fu·Afn/Afg), AISC F13.1 | 136.1 | 194.08 | MPa | 0.70 | OK | as proposed (2 rivnuts at X±25 in one section): 1.03 NG, and the hex-16 hole runs 5.6 mm into the 9.5 corner radius (rivnut cannot seat) - applies to every F-07 saddle rivnut S1-S6; B1/S1 0.15, B4 Y±480 0.41 |
| K2-hs | Loco Bot S17: S1 smokebox saddle rivnut tension (227.9 kg, 1 g roll + 1 g up) and pilot slat holes (20 × M10 in the L3 PL12 face, 6 % row loss) |  | T / SWL 4 kN (ASSUMED) | 0.991 | 4.0 | kN | 0.25 | OK | pilot slats OK with conditions: >= 30 mm from box edges/welds, clear of the coupler pocket Y±560 and the FT-1 load path, full 12 mm thread or through-bolted |
| K2-ss | Deck side stringers SS± C3x4.1 -> HSS3x3x1/8 (P-A1, ADOPTED S17), grillage with S17 loads |  | M/S vs 0.6 Fy | 81.31 | 207.0 | MPa | 0.39 | OK | was 0.57 on C3x4.1; bearer max 0.67 |
| K2-r70 | L-109 R70 swept half-width (Loco Bot sweep, K-401 method): cab eave governs | R100 1,581.6 reproduced | envelope vs 1,696 | 1,629.4 | 1,696.0 | mm | 0.96 | OK | 66.6 mm margin CONFIRMED; front-end items 198 / 547 / 559 |
| K2-b | ASCE 40 rail base stress at 26 kN (scaled from 22.85 kN screening) vs 172 MPa |  | σ ∝ Q | 114.923 | 172 | MPa | 0.67 | OK |  |
| K2-c | Rigid wheelbase 1,550 on R100 - versine vs flangeway play 12.4 |  | f = wb²/8R | 3.003 | 12.4 | mm | 0.24 | OK |  |
| K2-d | Loco swept half-envelope on R100 - 3-D kinematic sweep of the R2 model (governing point: CAB ROOF eave, incl. 2° sway + 6.2 play) vs K-401 half 1,696 | old single-point cab-step check 1487 (understated - wrong governing point; K-401 L2 and the sweep agree within 4 mm at R45: 1,719 / 1,715) | route_check.py sweep | 1,581.603 | 1,696 | mm | 0.93 | OK | R50 1,691.7 (+widening 1,701 NG → cab-roof eave trim ≥ 10 mm if R50 is adopted); R45 1,715 NG |
| K2-d2 | Coach swept half-envelope on R100 incl. Trim Bot garland/lights 60 mm per side vs K-401 1,696 | coach 1586.5 + 60 | sweep + 60 | 1,646.529 | 1,696 | mm | 0.97 | OK | R50 1,688 (+widening 917.5 → 1,693 OK; 920.7 → 1,697 NG: keep R50 widening at 917.5 or garland ≤ 50 mm) |
| K2-e | Driver top to running-board edge angle (underside Z1,530): vertical clearance - 25 bump vs 50 min |  |  | 50 | 55 | mm | 0.91 | OK |  |
| K2-f | Driver tyre sweep under running board at R100 (truck yaw) - lateral movement at wheel end vs board overhang beyond tyre 703 | yaw 0.92° | Δy = 1,500·sin(yaw) | 24.0 | 703 | mm | 0.03 | OK |  |
| K2-g | L4 chain case (lowest part, inside the frame) vs rail top - case bottom Z389 | case bottom Z389, rail top Z0 | vertical clearance - 25 bump - 50 wheel wear | 75 | 314 | mm | 0.24 | OK |  |
| K2-h | Decorative cylinders Ø380 on T1 at Y±790 (L4, moved from Y±750) vs lead-truck wheel rim - min gap after 6.2 play on Alt A as drawn (R100, no spirals) vs 10 mm | at Y±750 it was 0.1 (NG) | sweep | 10 | 37.013 | mm | 0.27 | OK | FIXED rev L4: cylinders at Y±790 (25 mm at R50) |
| K2-i | Loco-tender DB-800: tender-side pocket swing (300 mouth, limit 19.2°) - max angle on Alt A as drawn | loco side 13.3° vs 32.4° | sweep | 10.016 | 19.218 | deg | 0.52 | OK | R50 needs 19.5-19.7° → tender pocket mouth 150 (limit 32.4°) if R50 is adopted |
| K2-c2 | Rigid 1,550 driver truck on R45 - versine incl. flange lead vs flangeway play at gauge -3 (9.4) | 2-axle truck cannot jam; versine criterion with flange lead | f = (wb+2·lead)²/8R | 7.62 | 9.4 | mm | 0.81 | OK | Stress Bot's 13.2 mm (= wb²/4R) is a 3-axle criterion - not applicable to 2-axle trucks |
| K2-j | Max gauge accepted by the wheelsets: widened 920.7 + 6 build + 6 wear (932.8) - tread overlap on the rail head (worn flange 17, min B2B 857, tread 120, chamfer 5) | overlap 56.2 vs ASCE 40 head 47.6 |  | 932.8 | 941.4 | mm | 0.99 | OK | Absolute max 941.4; maintenance limit 932 proposed |
| K2-k | Restraining rail flangeway, min case (widened 917.5, check gauge 886 +2/-0) vs 25 mm (22 flange + 3) | flangeway = G - C |  | 25.0 | 26.6 | mm | 0.94 | OK | No widening (914.4) → 23.4 NG: restraining rail only with widened gauge |
| K2-b2 | ASCE 40 rail base stress, track_structure spec (ties 6×8×6 ft @ 22.5 in, 2×26 kN) vs 172 MPa | track engineer calc reproduced |  | 153 | 172 | MPa | 0.89 | OK | Lateral basis 0.35×2×26 = 18.2 kN (engineer used 17.1). Their 'L/V 0.11 at R100' is centrifugal only - flange guidance gives Y/Q ≈ 0.8-0.9 on R≤100: design curves < R100 for 0.5×axle |
| K2-l | Lead (pony) truck, ACTUAL wheel load 2.9 kN (LT42: body reaction 0; PE 5.4 was wrong) - free swing arm, leading wheel Y/Q on R45 vs Nadal 1.34 | Q 2.89 kN (2.15 in twist); Heumann 1,050 wb | Y/Q chord mode | 0.942 | 1.342 | L/V | 0.70 | OK | Passes ONLY with no lateral centering force: allowable arm/centering friction 0.4 kN at Q_min (μ 0.3, 1.2 margin). REQUIRED: load the pony (K2-m) + swing stops ±120 mm (Stress Bot R3; R80 working route swing 89.5 mm, E 102, A 72, D 119) |
| K2-m | Pony load 15 kN (upper end of 10-15) taken as a BODY SPRING (reacted at X1,525, outside the pivots) - max driver wheel vs 26 kN | spring lifts 1.80×F off the front truck: F2 axle 11.67 kN, rear wheel 26.5 | statics | 26.5 | 26.0 | kN | 1.02 | REJECTED OPTION - sprung pony with own ballast adopted (K2-m2) | Body-spring loading over-loads the rear truck and strips the front drivers (equal-torque cap 25.2 → 13.9 kN). RECOMMENDED: sprung pony carrying its OWN 1.25 t ballast (12.3 kN, Q 5.96 kN/wheel, no effect on the drivers) |
| K2-m2 | ADOPTED L4: sprung pony carrying its OWN 1.25 t ballast (no load transfer to the drivers) - max driver wheel vs 26 kN | K2-m body-spring option REJECTED | statics | 25.89 | 26.0 | kN | 1.00 | OK | Pony Q ≈ 5.96 kN/wheel → K2-l lead-wheel Y/Q improves; swing stops ±120 mm |
| K2-n | Barrel saddles S3 (X2450) / S5 (X5675), bearers and RB-1 brackets vs the L4 chain drive (Loco Bot) - min plan gap | drive top Z1061 vs RB bracket bottom Z1175.0 | CAD envelope | 50 | 389 | mm | 0.13 | OK | CLEAR; keep-out zones on L-103 |
| K2-lo | K-401 LOWER OUTLINE (Steering 14b): all non-wheel parts >= 150 mm ATOR between the rails / >= 100 mm outside; level track + vertical curves R >= 500 m (crest/sag loss included), new wheels, static | governing: transom HSS10x4x1/4 (upright, pair) tender clear 196.0 mm (between); loco/tender/coach checked from the CAD model | limit / clearance | 150.0 | 196.0 | mm | 0.77 | OK | PASS all vehicles. Not included: wheel wear + spring deflection (tender/coach transom margin 46 mm; PE to set wheel-wear limit) and coach stairs (deployed only at rest). Tender transformer shield bottom Z300 (TB-3.4, 150 margin); inrush box bottom Z380. |
| K2-fp | Fouling point / clearance mark, #8 turnouts (Rail Bot, Steering 14c): track centres at the mark vs 2 x 1,696 dynamic half-width + 200 | mark at 3.6 m centres; #8 frog 7.153 deg, lead R 84.9 m → 33.99 m from the points (Rail Bot 34.0 m) | 2·1,696 + 200 | 3,592.0 | 3,600 | mm | 1.00 | OK | Clearance marks 34.0 m from the points of each #8 - VERIFIED (33.99 m). Working layout F (R80, level), owner pending. If either track is on R80 at the mark, add ~37 mm per side (loco end throw 185 vs 148 at R100) - within the 200 mm allowance (74 < 200); level layout F, owner pending. |
| K2-xf | Tender shore transformer (TB-3.13d) top vs the X2500 HSS10x4 frame crossmember underside Z836 - cradle DROPPED 50 mm (kept since TB-3.8) | unit top Z851 → Z801 static; Z811 at the isolator stop | Z_top vs Z_underside | 811 | 836 | mm | 0.97 | OK | CLOSED: 25 mm at the isolator stop, 100 mm to the K-401 outline |
| K2-rF | Route L4 Alt F R80 - WORKING ROUTE (owner pending) (final spiralled, L4 masses): max L/V (loco/tender/empty coach at full TE 37.7 kN) vs Nadal 1.34 | env loco 1609.6 / coach+garland 1657.1 vs 1,696; ΔQ/Q 0.29 vs 0.6 | Heumann Y/Q + F·sinθ·fac/2Q | 1.27 | 1.342 | L/V | 0.95 | OK | PASS |
| K2-rE | Route L4 Alt E R70 (final spiralled, L4 masses): max L/V (loco/tender/empty coach at full TE 37.7 kN) vs Nadal 1.34 | env loco 1635.5 / coach+garland 1670.7 vs 1,696; ΔQ/Q 0.33 vs 0.6 | Heumann Y/Q + F·sinθ·fac/2Q | 1.32 | 1.342 | L/V | 0.98 | OK | PASS |
| K2-rA | Route L4 Alt A R100 (final spiralled, L4 masses): max L/V (loco/tender/empty coach at full TE 37.7 kN) vs Nadal 1.34 | env loco 1581.7 / coach+garland 1646.5 vs 1,696; ΔQ/Q 0.23 vs 0.6 | Heumann Y/Q + F·sinθ·fac/2Q | 1.18 | 1.342 | L/V | 0.88 | OK | PASS |
| K2-rD | Route Alt D R60 with truck-pitch transfer at the traction pin, HIGH-RAIL GAUGE-FACE LUBRICATED (Nadal 1.84 at flange μ 0.15) - lubricators on ALL R ≤ 80 | dry L/V 1.381 vs 1.342 (NG dry); F 1.258, E 1.309 | Heumann Y/Q + F·sinθ·fac/2Q | 1.381 | 1.84 | L/V | 0.75 | OK | CLOSED (L4.1): top of rail kept dry for 2 % starts; lubricator maintenance in the operating manual |

### Design statements
- Wheel profile (all vehicles): 1:20 tread taper, flange height 25 mm, flange thickness 22 mm at gauge point (10 mm below tread), flange angle 70°, root radius 12, tread width 120.
- Back-to-back 858 ±1.0 mm (G 914.4 - 2×22 - 2×6.2 play). WHEELSET flange-face gauge 902 nom / 891 min worn (857 + 2×17); wheel check dimension (B2B + one flange) 881 max new / 874 min worn. (The former 'check gauge 892 min' was the worn wheelset gauge, a WHEEL dimension - it is NOT a track check gauge: as one it leaves a 22 mm flangeway, NG.)
- Track gauge 914.4 +6/-3 (tangent, R ≥ 75); widened 917.5 (36-1/8 in) on R50-75 and 920.7 (36-1/4 in) on R45-50 - accepted by all wheelsets (K2-j). Absolute max gauge 941.4 (full head under worn tread); MAINTENANCE LIMIT 932 (renew/regauge).
- Restraining (guard) rail on curves < R60: TRACK CHECK GAUGE (high-rail gauge face to restraining face) 886 +2/-0, renew below 883 (must stay > 881 wheel check dimension); FLANGEWAY = G - 886 = 31.6 at 917.5 / 34.8 at 920.7 (min 26.6 / 29.8 ≥ 25). Restraining rail REQUIRES the widened gauge (at 914.4 the flangeway is 28.4, min 23.4 < 25 NG). The track engineer's 886 is correct; the PE '892' is the wheel dimension above.
- Design grade 2% GOVERNING (route redline 28 Oct 2026; curves compensated so grade + curve resistance ≤ 2.0%). The track is NOT designed level; 'laser-levelled 0%' reports do not change the basis until the owner confirms.
- Minimum radius: design basis 100 m (unchanged). R60/R50 study results and the changes each needs: calcs/track/route_check.md.
- Rail ASCE 40 lb/yd new (track_structure spec), ties 6×8 in × 6 ft at 22.5 in (572), tie plates, 9/16 in cut spikes - consistent with the 26 kN wheel basis (K2-b2). Curves < R100: lateral design 0.5×axle, rail braces or 4 spikes/plate on the high rail, gauge-face lubrication. Ballast ≥ 10 in under ties (Stress Bot subgrade 26-34 psi at 6 in vs 20).
\pagebreak
## A Fastener torque schedule (ISO 898-1; preload 75% proof; mark after torque)

| Size | Class | As mm² | Preload kN | Torque dry/zinc K0.20 N·m | Torque lubricated K0.14 N·m |
|---|---|---|---|---|---|
| M10 | 8.8 | 58.0 | 25.2 | 50 | 35 |
| M10 | 10.9 | 58.0 | 36.1 | 72 | 51 |
| M12 | 8.8 | 84.3 | 36.7 | 88 | 62 |
| M12 | 10.9 | 84.3 | 52.5 | 126 | 88 |
| M16 | 8.8 | 157.0 | 68.3 | 219 | 153 |
| M16 | 10.9 | 157.0 | 97.7 | 313 | 219 |
| M20 | 8.8 | 245.0 | 110.2 | 441 | 309 |
| M20 | 10.9 | 245.0 | 152.5 | 610 | 427 |
| M24 | 8.8 | 353.0 | 158.8 | 762 | 534 |
| M24 | 10.9 | 353.0 | 219.7 | 1055 | 738 |

Running-gear and drive fasteners: Nord-Lock wedge washers or prevailing-torque nuts + witness mark; re-torque after 10 h running. Structural slip-critical joints (if any added): ASTM F3125 A325 per RCSC 2020 turn-of-nut.

## B Weld schedule

| Joint | Weld | Size | Inspection |
|---|---|---|---|
| Drop drawbar box to rails / sill | Fillet all round | 10 | 100% VT + MT |
| Pocket plates PL20 to box | Fillet all round | 10 | 100% VT + MT |
| Loco crossmembers to main rails | Fillet all round | 6 | VT |
| Bolster box seams | Fillet both sides | 6 | VT |
| Centre plate to bolster | Fillet all round | 8 | VT + MT |
| Powered truck horn cheeks to chords | CJP groove + 6 fillet cap, toes ground | full pen. | VT + UT 100% |
| Transom box seams | Fillet both sides | 8 | VT + MT 10% |
| MS05 motor bracket PL25 to transom (L4) | 2 × 400 fillet both sides + 2 PL16 gussets | 10 | VT + MT |
| Chain oil-bath case seams (3 mm) | Continuous fillet, leak test | 3 | VT + leak |
| Engine/genset pedestals to tender rails | Fillet all round | 8 | VT |
| Coach crossmembers/outriggers to rails | Fillet all round | 5 | VT |
| Window posts / roof bows | Fillet all round | 3 | VT |
| Stair stringers / treads (C-304) | Fillet both sides | 5 | VT |

All welding by AWS D1.1-qualified welders to a written WPS; CWI inspection of primary members (drawgear, trucks, drive brackets). Pre-heat per D1.1 Table 5.8 for A572-50 > 20 mm.

## C Fix log

| # | Subsystem | As-found problem | Fix | Ref |
|---|---|---|---|---|
| 1 | Drive | Owner plan direct drive / L1 1:1 on Ø1,450: 21.9 kN vs 31.2 kN 2% start | Rev L2 custom spur gear (1.81:1), rev L3 Dodge TA7315H15MS + H1B110 + belt, then rev L4 (owner: no belt) Poclain MS05 468/234 + ANSI 120-2 chain 3:1 - 37.7 kN at 350 bar | F25, F26, D1-a |
| 2 | Drive (L4.1) | Flow divider (L4 per-motor slip control) not buildable: Jahns HTO-4-35-FI runs below its 12-16 L/min minimum at every start, 320 bar section rating caps TE at 31.2 kN < 32.3 needed, +160 kg | Divider DELETED; electronic traction control (per-motor sensors + pony ground-speed reference, pump destroke, auto-sand, start in 1st, hill-start hold); TE cap = equal torque; dry/sanded 2% margin 1.10 kept with 2 × 75.4 kg plates | D1-c, D1-m, D1-m2 |
| 3 | Truck (L4.1) | Truck-pitch weight transfer missing (Stress Bot r2): pivot h 1.08 m → equal-torque 2 % start fwd 0.94 / rev 0.69 | LOW TRACTION PIN per truck at h 0.65 m (Ø100 4140 pin, GE100ES under the transom, centre plate flat-lined): fwd 1.13; reverse PLUS+1 pull cap 28.9 kN + reverse full-train starts only ≤ 1.20 % (L4.2) grade (covers Ø1430 worn drivers); K2-a 25.7 kN with transfer | D4-wt/wr |
| 4 | Drive (L4.1) | Trip run-in: CCO/24 V trip in 1st at 400 bar gave 67 kN, accidental T04 52 kN vs 33.2 kN R80 limit | Pump ramp to neutral ≥ 3 s, motors de-energize to 2nd, T04 pressure switch vents BP first + choked T04 (≥ 1.0 s + 2.0 s): worst 23.7 kN | D4-ri |
| 5 | Drive (L4.1) | Chain slack check used dL = dC (L = C) | dL = (2·span/C)·dC; ±22 mm bump stops, ±1 mm side float, re-shim at the centre plate (primary ≤ 3 mm + motor-slide reset); 2 % elongation hard limit; B29.1 certificate ≥ 302.5 kN; zero-speed reversal | D2-f/D4-ch |
| 6 | Axle (L4.1) | Hub fit 0.12-0.17 with an oil-press option (SF 0.87 pressed) | SHRINK ONLY 0.15-0.20; hot hub 30 K + smoothing SF 1.87 at HPRV; removal groove kept | D4-hf |
| 7 | Drive (L4.1) | Kubota high idle could exceed 6 mph at the 42 cc stop | Stroke stop 38 cc sealed: 5.91 mph at 2,850 rpm high idle | D4-sp |
| 8 | Route (L4.1) | Route D R60 L/V 1.39 > 1.34 (K2-rD); with transfer E/F marginal | High-rail gauge-face lubricators on ALL R ≤ 80 (Nadal 1.84): D 1.32 margin - CLOSED | K2-rD |
| 9 | Tender (L4.1) | Transformer top Z851 vs X2500 crossmember Z836 (K2-xf) | Tender Bot TB-3.8: cradle dropped 50 mm (25 mm at the isolator stop, 100 mm to K-401) - CLOSED; tender TB-3.9 8,616.3 kg, brake 5.825 kN = 0.676 m/s² vs loco 0.690 (within 0.03) | K2-xf/E-cg |
| 10 | Loco body (L4.1) | Loco Bot: saddle web windows cut the 3 g longitudinal path (util 5.9); B1 hole X460 in the sill weld zone; SD-1 hole outside the cap; SD-2 hold-down open; clamp bars for 1 plate/side | 8 gussets per saddle (0.28); B1 holes X480/600; SD-1 cap re-cut to Y±50 (0.84); SD-2 clamp plates under the sill flange (no holes); clamp bars 0.59 at 30 N·m | L41-sw/s1/s2/cb |
| 11 | T04 release (L4.1 s7) | T04 release held by a 0.75 L accumulator on the brake line: an engine stall left the motor brakes released ~30 s (loss of charge did NOT apply them); a 4th dry-break was proposed | Release supply from the loco loop (LP shuttle + 20 bar reducing/relieving valve + normally-vented solenoid); choke Ø2.4 + 1.0 L damping accumulator (delay 1.01 s, rise 2.97 s); manual release from a 6.0 L accumulator + hand pump via a guarded valve; loss of loop/charge or 24 V applies the T04 after the BP vents; no 4th dry-break | L41-t1/t2 |
| 12 | Wheels (L4.1 s7) | No driver condemning limit; pony Ø630 worn gives a 35.0 mm flange vs ~32.5 mm to the ASCE 40 joint-bolt heads | Driver condemning DIAMETER Ø1430 adopted (6 mph governor / 7 mph trip, adhesion 1.116, clearances pass); FLANGE-HEIGHT limit 28 mm / ≤ 27 (L4.2 FINAL) on all loco wheels (re-profile); reverse-start rule ≤ 1.20 % (L4.2); diameters entered in PLUS+1 at gauging | L41-w1..w5 |
| 13 | Brake air (L4.1 s8/9) | Loco release time not specified; Loco Bot estimate 3.7 s at an assumed C 2.0 (range 1.8-7.3 s); release regulator/relay not sized for flow | Target ≤ 4 s WORST CASE; release path total C ≥ 3.0 (required 2.5) → 3.46 s incl. 1.0 s signal; parts budget C 5.26 → 2.4 s: relieving regulator C ≥ 10, 1/2 in relay valve C ≥ 8 piloted by the IR-2, 3/4 in trunk C ≥ 8, 4 × 1/2 in branches C ≥ 2.0, quick-exhausts, release-proof switch; timed commissioning test | L41-b1..b4 |
| 14 | Drive (L4.1) | AIE SAE B 13T pump drive mates only H1P053 shaft G4 (222 N·m max < 265 engine peak) | Keep G1; engine coupling hub 14T 12/24 (AIE confirmation held) | D1-u |
| 15 | Drive (L4.1) | 15T spline engagement 70 mm ASSUMED, code-5 spline only ~60 mm | Full-length engagement ≥ 58 mm, 95 MPa (0.95); 4140 15T if shorter | D2-h |
| 16 | Axle (L4.1) | Ring bolts 10.9 fitted (non-catalog) and Ø340 flange edge 20 mm = 1.18 d0 | Catalog 8.8 fitted DIN 609/7968, 219 N·m; Ø350 flange edge 25 mm = 1.47 d0; hub 31.4 kg | X1-g, X1-h |
| 17 | Drive (L4) | Equal torque limited by the lightest axle (L4 early pass F2 29.6 kN): 2% start margin 0.92 | (L4: flow divider) → sand mandatory wet; front ballast trimmed to 150.8 kg (2 × 75.4 plates) + BT-1 68.2 kg in the pocket (Steering 17, C9 rule) → lightest axle 35.63 kN, dry equal-torque margin 1.10 | D1-a/c/m |
| 18 | Drive (L4) | Chain case at 3% stretch + ±25 travel had < 15 mm radial clearance | Case enlarged (axle-end inner r 332.7) | D2-g |
| 19 | Drive (L4) | Source Bot 56 links would put the motor 38 mm into the transom | 54 links (C 417.6 mm new); slotted mount + 2 M20 jack screws, no idler | D2-e/f |
| 20 | Axle (L4) | Ø140 pressed seat n 1.37 without hardening credit | Ø150 raised seat, no key: n 1.64 on the heaviest axle | X1-c |
| 21 | Drive (L4) | Overspeed trip ran through PLUS+1 | Independent 2-channel speed relay to BP exhaust + pump neutral | D1-n |
| 22 | Drive (L3) | H1B110 in line on the TA II input does not fit (rear Y491 vs sideframe 330 / wheel 427; hits horn cheek) | 1:1 synchronous-belt drop: motor through the open sideframe window, 6 mm inside the wheel line | F27, D1-p |
| 23 | Axle (L3) | Ø120 keyed seat, 4140 profile keyseat: fatigue n 0.96 < 1.5 | 34CrNiMo6 Q&T + sled-runner keyseat + induction-hardened seat: n 1.82 | X1-c/d, C7s |
| 24 | Drive (L3) | One spinning wheelset could drive the TA II input to 2,106 rpm (> 1,790) | Per-motor speed sensors + PLUS+1 anti-slip destroke | D1-l/m |
| 25 | Brakes (L3) | Axle disc is now 1:1 - one caliper would need ~35 kN | 2 spring calipers per disc, 17.5 kN each vs 22 kN spec | B1-g |
| 26 | Drive | DT5 hub key 243 MPa at relief; KTR FA25 at 1.10× | Eliminated (L2/L3: outboard stub/coupling removed) | F03 |
| 27 | Drive | Pump H1P045 flow limited top speed | H1P053 kept; L4: 6 mph governed by the sealed 38 cc stop (5.91 mph at 2,850 high idle; 5.4 at rated); 7.6 mph hardware max, independent 7 mph trip | D1-f |
| 28 | Drive | Pump input 350 N·m at 380 bar > G4 shaft 222 N·m | G1 input shaft 534 N·m (368 N·m at 400 bar) + anti-stall software 35 kW (supplier F2) | D1-e |
| 29 | Drive | Relief 380 bar not a Danfoss setting | Option L35: pressure limiter 350 / HPRV 400 bar; torques re-run (supplier F3) | X1-a, D1-g |
| 30 | Brakes | Caliper r_eff 145 optimistic | r_eff 135 → 18.8 kN clamp, 22 kN spec holds; Coremo D 3.5N reference; burnish + regulated release air | B1-g, B1-l |
| 31 | Drive | Wet-rail 2% start short 9.2 kN | Sanders on leading axle each direction (μ ≥ 0.21) | D1-c |
| 32 | Drive | F25-A memo: nose reaction taken as 0.75 × torque (wrong) | Full axle torque to nose link (C7n) | C7n |
| 33 | Brakes | L2: axle disc space lost to the gear case | L3: disc back on the axle, free side (Y+), 2 calipers | B1-g |
| 34 | Brakes | Loaded-weight brake sizing slides empty coaches on wet rail | Tare-based 12% braking ratio | B1-a |
| 35 | Brakes | Loco spring brakes alone cannot hold the train on 2% | Park with BP exhausted (all spring brakes) + chocks | B1-e/f |
| 36 | Trucks | Coil primary springs do not fit the 170 mm LT18 window | Rubber-metal chevron springs (spec) | T1-d |
| 37 | Coaches | Roof bows HSS2x2x1/8 @880 deflect 1.26 × L/180 | HSS3x2x1/8 bows | R1-e/f |
| 38 | Coaches | Guard post 1-1/2 in sch 40 overstressed | 2 in sch 40 | C10d |
| 39 | Loco | Ballast end wall PL12 overstressed | PL20 + 4 × M20 hold-downs | C9 |
| 40 | Wind | Empty coach FS 1.37 at 67 mph | 40 mph no-run + parked tie-downs | C11w, W1 |
| 41 | Drive (L4.2) | Stress Bot r3: descents on hydrostatic retarding; T04 burst/accidental apply; 2,850 rpm high idle; 30 mm flange limit with 6 mm joint wear | FLOAT mode (loop bypass, ≥ 3 s swash ramp), friction brakes sized for the full 2 % descent; Ø1.2 T04 port orifices + hard lines/4SH + 2-channel vent switch, T04 fed from the H1 CHARGE circuit (loop shuttle deleted); hard tamper-sealed 2,600 rpm + 42 cc; flange 28 mm / re-profile ≤ 27, 2 mm joint wear: run-in worst 25.3 kN ≤ 33.2 | L42-dn, L42-t1..t4, D4-ri, D4-sp |
| 42 | Pressure (L4.2) | No -16 assembly ≥ 450 bar; strength at HPRV 400 only | PL 350 / HPRV 380; loop parts ≥ 420 bar WP with ISO 18752 / ISO 6605 impulse rating covering the ~430 bar spike; every STRENGTH case at 430 bar: 15T sprocket made to order in 4140 Q&T (C1045 stock hub 1.03 NG); chain MBL SPEC ≥ 326 kN certified (standard 296 kN not accepted) | D2-h, D4-mb, D1-g |
| 43 | Mass (L4.2) | K2-a drifted to 26.1 kN (final drive 336.7 kg/axle, gross brake piping/chains, Ø120 pins, P-106 pockets) | NB-1 nose ballast 59.8 kg at X450 (ahead of the front pivot unloads the rear truck) + PLUS+1 forward TE command limit 33.0 kN: K2-a 25.89 kN of record; reverse pull cap 28.9 kN | L42-k2 |
| 44 | Power | Hot-humid coach HVAC 4.7 kW over 35 kW | RenewAire HE05IN ERV per coach (roof pod) + staging controller (31.1 kW at plan OA) | G1-b/e/f |
| 45 | Track | Rail basis 22.85 kN exceeded (24.5 kN with L3) | Rail basis 26 kN, ASCE 40 min. | K2-a/b |

## D Revision history

| Rev | Date | Description |
|---|---|---|
| R1/R2 | 2026-10-27 | Design review, calc notes C1-C16, 13-sheet set |
| L1/L1b | 2026-10-27 | Loco to owner plan Ø1,450 drivers; 4 motors |
| L2 | 2026-10-27 | Inboard spur-gear drive; full PE-review calc package |
| L3 | 2026-10-28 | Owner: choose the best fit → catalog Dodge TA7315H15MS 14.9:1 + Danfoss H1B110 via 1:1 belt (L2 custom case rejected); Ø120 seat fix; axle discs 2 calipers; governed 6 mph owner-selected (PE to confirm) |
| L4 | 2026-10-28 | Owner: no belt → Poclain MS05 468/234 2-speed + T04 frame-mounted, ANSI 120-2 15T:45T 3:1 chain in oil bath, Ø150 pressed hub; H1P053 stroke-stop governor; independent overspeed; tender T2 update; Loco Bot interfaces; sprung pony; cylinders Y±790 |
| L4.1 | 2026-10-28 | Flow divider deleted → electronic traction control; Loco Bot ledger 01:57 + HL-1 headlamp 25 kg + TC/valve package 28 kg + clamp bars; hub Ø350 flange 31.4 kg; 8.8 fitted ring bolts 219 N·m; shaft code 5 W55x3x17 / hub N55x3x17, ≥ 58 mm engagement; pump G1 + 14T 12/24 coupling; T04 release + accumulator + tow valve specified; 15T OD 202; axlebox C ≥ 190 kN; 2 × 75.4 kg plates + clamp bars; DBK-1/jumper zones recorded (this document) |
| L4.2 | 2026-10-28 | Stress Bot r3 rulings: float-mode descents, T04 orifices + charge feed, 2,600 rpm sealed limit, flange 28 / ≤ 27, Ø120 pins + centre pad, sanders both trucks, reverse limit from the calc, pony 96T; PL 350 / HPRV 380, loop ≥ 420 bar, strength at 430; TB-3.13d; E7/E8 brake air (QEV B); NB-1 nose ballast, K2-a of record |
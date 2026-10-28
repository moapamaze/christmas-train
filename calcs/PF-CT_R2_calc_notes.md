# PF-CT R2 — Design review and hand calculations

Pulsipher Farms Christmas Train — preliminary, not for construction until PE stamped.

Basis: ASD, allowable 0.6 Fy for service (×1.3 dynamic) and Fy for check (×2.0 or 200 kN ultimate). A500C Fy 345 MPa, A36 250, A572-50 345, 4140 Q&T 655 (min. cert).
Supplier values not invented: items marked AWAIT need AIE, Dodge (ABB), Danfoss, Gates, ZF/WABCO data. Rev L3: governed 6 mph (owner-selected, PE to confirm). Load cases (3 g / 2 g / 1 g ballast, 200 lb guard, 300 lb tread, FS 1.5 wind) are ASSUMED for the PE to confirm.

## Findings and fixes

| ID | Area | Finding | Fix | Severity |
|---|---|---|---|---|
| F01 | Organization | 131 sheets, revisions LT1-LT45 / C1-C57 / DT1-DT5 with many superseded; nothing released. Fabricators can't tell what is current. | One parametric model (model.py) drives CAD + 12 sheet set PF-CT R2; superseded studies kept as reference only. | High |
| F02 | Couplers | Coupler height inherited 800 mm but modeled 550; loco rear pin hangs 752 mm below rail attachment (bending into frame), tender hitch 400 mm offset. | Standard 550 mm ARL on every vehicle; one PF-DB closed drop box (PL16 A572-50) + knee gussets; one drawbar design PL32x150, Ø60 4140 pins. Checked at 200 kN. | High |
| F03 | Drive | 750 cc motor change not carried into DT5 hub: 22x14x70 key on Ø80 sees 243 MPa at 420 bar (fails); GEARex FA25 at 1.10× capacity with 1.5 SF. | RESOLVED rev L2: DT5 outboard stub, hub key and KTR coupling eliminated. Motor splines into an inboard pinion shaft; gear seat keyless/shrink fit (key alt. 68 MPa, C7k). | High |
| F04 | Heights | Frame/cab heights still set by old Ø1,450 driver studies; roof 3,800-4,000. | DECIDED R2: roof 3,700 mm ARL adopted. Cab clear headroom verified from the model ≈1,960 mm (3,700 − 3 skin − 76 HSS3x2 purlin = 3,621 underside; cab deck 1,656; 1,959 with 6 mm mat) - good for a 6 ft 3 in crew member with shoes. Route overhead clearance adopted: nothing lower than 4,300 mm ARL within 2,000 mm of CL (train 3,700 + 600).; REV L1: running board 1,605 / rails 1,455 now follow the plan Ø1,450 drivers (LT18); cab floor 1,605 (plan 1,500, rear-driver clearance per LT19), headroom ≈2,010 with mat. | Med |
| F05 | Stability | No wind / overturning case anywhere. | Calc C11: empty coach FS 1.37 at 67 mph gust, 3.85 at 40 mph. DECIDED R2: no running above 40 mph gusts (FS ≥ 3.85 all vehicles); tie-downs when parked. Crew checks gusts before each run. | High |
| F06 | Running gear | Pony truck axles carry ~590 kg (5.8 kN/wheel) - light wheel, derailment risk on 100 m curve and turnouts. | OWNER DECISION (open). Recommend DELETE: gentle 100 m loop, two powered trucks carry and guide the loco; removes a light, derailment-prone axle. Alternative: spring preload ≥1,000 kg/axle. Model still shows it as an option.; REV L1: owner asked for the loco like the plans - leading truck Ø650 (LT11/LT18) kept in the model; delete still possible as a later owner decision. | High |
| F07 | Mass / rail | Ballast 1.5 t raises front driver wheel to 23.4 kN, above the 22.85 kN rail screening basis; mass figures differ between pages. | Single mass ledger: 74,760 best / 77,500 design / 80,000 check. Rail basis raised to 24 kN (ASCE 40 ≈103 MPa, OK). | Med |
| F08 | Coaches | Floor height conflict (28 in placeholder vs 32 in), failed boarding bridge plate, and no way to get passengers off between stations (old 2-tread side steps had 265/275 non-uniform risers and stopped 275 above rail). | DECIDED R2: floor 32 in (813) ARL; fold-down steel emergency/boarding stairs at every coach door, both sides (18): 6 equal 177 mm risers to ground (−250 ARL), 5 × 280 treads (~32°), 914 clear, handrails both sides, abrasive nosings, latched + traction/brake interlocked, stowed inside the 1,397 body half-width (dynamic outline 1,696 unchanged). Level 32 in platforms now optional. Keep a walkable egress strip to 3,300 mm from CL on at least one side. | High |
| F09 | Coaches | Platform guard posts 1-1/2 sch 40 overstress at 200 lb (178 MPa vs 145). | 2 in sch 40 posts (103 MPa). | Med |
| F10 | Brakes | 64 moving hose assemblies - leak/maintenance burden. | Relay valves on body, 1 caliper per axle, 2 moving hoses per truck → ~30 total. AWAIT ZF/WABCO. | Med |
| F11 | Couplers | No secondary connection between cars. | 2× Grade 100 1/2 in safety chains per joint (MBS 534 kN vs 200 kN). | High |
| F12 | Cab | Stowed/moving ladder at cab door. | Fixed 4-tread steps + Ø32 grab irons both sides; checked at 300 lb / 200 lb. | Med |
| F13 | Ballast | Ballast pocket end walls PL12 would see 243 MPa at 3 g. | PL20 end walls (88 MPa) + 4× M20 hold-down rods; pocket moved outboard to clear hood. | Med |
| F14 | Cab roof | HSS2x2x1/8 purlins deflect L/233 under 20 psf (11.6 mm); flexible for a walkable roof. | HSS3x2x1/8 @600 (4.4 mm). | Low |
| F15 | Fabrication | No general notes: welds, bolts, tolerances, materials, mill certs. | G-001 general notes added (AWS D1.1, A325/Gr8, tolerances, 4140 Q&T certs). | High |
| F16 | Fabrication | Custom machined bearing housings and odd sections. | Catalog SKF 22218 E / 32018 X cartridges, standard HSS + plate only; coach truck transom = 2 upright HSS10x4. | Med |
| F17 | Track | Rail shown differently across CAD sets; rail not approved. | ASCE 40 used as preliminary in all sheets; DO NOT ORDER until PE approves. | Med |
| F18 | Tender | R2 modeling error, now fixed. The 676 mm came from the superseded LT44 Hydra-Tech HT150DQV stock skid. Owner plan LT45.1 (AIE V3307 1,028 tall + genset envelope 1,000 on 80 mounts) fits the 1,204 clear bay. | R2 tender rebuilt to LT45.1 geometry (Rev T1). Open: genset model, mounts, cooling - AWAIT AIE / supplier. | Low |
| F19 | Clearance | No clearance outline for 100 m curve. | Dynamic half-width 1,696 mm; keep fixed objects ≥2,000 mm from CL; stations on tangent. | Med |
| F21 | Egress | Deployed stairs reach 2,947 mm from track CL (foot pad), beyond the 2,000 mm fixed-object line. | Keep ground 2,000-3,300 mm from CL clear and walkable (±75 mm) on at least the outside of the loop; where an object is inside 3,300 mm, sign that side 'do not deploy' and crew directs to the other side. Wheelchair users: crew-assisted evacuation procedure / portable ramp at platforms - PE + County to review. | High |
| F20 | Traction | SUPERSEDED by F25 (rev L1): margin 31.75 vs 31.03 kN was on Ø1,000 wheels. | See F25. | Med |
| F25 | Traction / running gear | Rev L1 returned the loco to the owner plan (8 × Ø1,450 drivers). 4 × MSE05 750 cc at 1:1 gave 21.9 kN at 350 bar vs 31.2 kN needed for a 2% start (T2 tender). Owner plan direct drive (DT4/DT5, sized on Ø1,000) cannot start 2% on Ø1,450; chains ruled out by owner 27 Oct. | SUPERSEDED BY L3 (28 Oct, see F26) - was RESOLVED rev L2 (owner chose option (c), 27 Oct): inboard axle-hung spur-gear case m10 21:38 = 1.81:1 per axle, MSE05 750/375 cc shaft motor toward truck centre, nose link to transom; nothing outside the wheels. 2% start 38.8 kN at 350 bar (adhesion-capped 35.8 dry; 32.7 at pessimistic η 0.80). Wet 2% start needs sand (μ ≥ 0.22). 2% hold 2.85 mph on V3307 45.6 kW. PE pass with the +464 kg L2 mass (ASSUMED): cap 36.96 kN dry / 22.2 wet, need 31.37, hold 2.84 mph (PF-CT_PE_calc_package §4). Calc calcs/L2/gear_drive_L2.json; C7g-C7n, C13, C13g, C13s. | High |
| F26 | Drive (rev L3) | Owner [pt77u] 28 Oct: not keen on the custom L2 gear case - weigh all options and choose the best fit. Compared L2 custom 1.81:1 + MSE05 750, Dodge 5:1 + Poclain MS05 280 cc, Dodge 14.9:1 + Danfoss H1B110, gearless LSHT (none fit a through axle). | ADOPTED rev L3: catalog Dodge Torque-Arm II TA7315H15MS (14.9:1, Ø120 straight bore, catalog TA rod) on each powered axle, Danfoss H1B110 variable bent-axis motor (same H1 family as the H1P053 pump). 2% start adhesion-capped 37.9 kN (42.2 kN at 350 bar; 31.5 kN needs ~262 bar); 2% hold 2.73 mph; reducer 0.50 of the 200 % start allowance at slip × SF 1.6. L2 kept as the rejected alternative; fallback TA7315H05MS 5.2:1 + MS05 ~280 cc. Calc calcs/L3/drive_L3.json; C7g-C7n, C13, PE D1/X1/B1. | High |
| F27 | Drive envelope (rev L3) | Envelope check (model.py): H1B110 in line on the TA II input shaft does NOT fit - reducer hub Y−267…+3 plus coupling and the 316 mm motor puts the motor rear at Y≈491 vs sideframe Y330 / wheel inner face Y427, and the motor body (X 109–349 from the axle) hits the horn cheek (X 110–140). The Ø120 keyed seat in plain 4140 also fails fatigue (n 0.96 vs 1.5). | FIX APPLIED: (1) 1:1 synchronous-belt input drop (catalog Gates Poly Chain class sprockets/belt, guarded) moves the motor to X 300–540 / Z 620–900, through the open sideframe window, rear at Y421 (6 mm inside the wheel line); motor bracket bolted to the reducer so belt centres do not move with the suspension. (2) Axle 34CrNiMo6 Q&T, sled-runner keyseat, induction-hardened + ground seat zone: n 1.82 (hardening factor ASSUMED - PE/metallurgist). (3) Axle disc on Y+ (free side) with 2 spring calipers per disc (axle torque now 1:1). AWAIT Dodge CAD for input-shaft position and Gates belt rating. | High |
| F28 | Industrial reducer in rail traction | Dodge TA II catalog ratings are for electric-motor industrial drives; Dodge asks for Application Engineering review for other prime movers and heavy shock. Rail traction (reversing, wheel-slip, track shock, axle-hung mass ~321 kg) is not a catalog application. | OPEN - flagged for the PE: RFQ to Dodge Application Engineering (rail-axle use, shock/overhung mass, straight-bore fit k6 + retention, rating at 16-35 rpm, reversing duty). Design checks use SF 1.6 (heavy shock) and the 200 % starting allowance; margins 0.41-0.62. | High |
| F29 | Operating speed | Owner decision 28 Oct: governed maximum operating speed 6 mph. | ADOPTED as the operating basis (brakes, stopping distances, curve/passenger checks): H1B minimum-displacement stop set to 60 cc and sealed (hard hydraulic limit at full pump flow), PLUS+1 pump speed control, independent overspeed trip at 7 mph (ASSUMED) → emergency brake; per-motor speed sensors also provide anti-slip. Hardware capable of ~10 mph (22 cc) - margin only. OWNER-SELECTED LIMIT - PE to confirm. | High |

## Calculation results

| ID | Item | Demand | Capacity | Unit | Ratio | OK | Basis / assumptions |
|---|---|---|---|---|---|---|---|
| C1 | Coach main rail HSS12x4x1/4 bending, vertical ×1.3 | 48.0 | 207.0 | MPa | 0.23 | OK | Sprung loaded coach 9476 kg uniform on 2 rails over 10160 mm, bolsters at 2337/7823 mm; M=12.5 kN·m/rail at ×1.0 ×1.3 service vs 0.6Fy; ×2.0 overload vs Fy. Side sills and floor ignored (conservative). |
| C1 | Coach main rail HSS12x4x1/4 bending, vertical ×2.0 | 73.8 | 345.0 | MPa | 0.21 | OK | Sprung loaded coach 9476 kg uniform on 2 rails over 10160 mm, bolsters at 2337/7823 mm; M=12.5 kN·m/rail at ×1.0 ×1.3 service vs 0.6Fy; ×2.0 overload vs Fy. Side sills and floor ignored (conservative). |
| C1d | Coach end-overhang deflection (×1.0) | 1.7 | 6.5 | mm | 0.25 | OK | Cantilever 2337 mm; limit L/360  |
| C1b | Coach main rail, vertical ×1.3 + 70 kN buff (eccentric) | 64.2 | 207.0 | MPa | 0.31 | OK | Coupler 550 mm vs rail centroid 635 mm: e=85 mm  |
| C2 | Coach bolster HSS12x4x1/4 + 2×PL10×100 doublers, centre load ×1.3 | 76.7 | 207.0 | MPa | 0.37 | OK | P=46.5 kN at centre plate, span 1728 mm (rail c/c), simply supported Doublers PL10×100 top+bottom over centre 600 mm; internal PL10 diaphragm each side of centre plate. |
| C2 | Coach bolster HSS12x4x1/4 + 2×PL10×100 doublers, centre load ×2.0 | 118.0 | 345.0 | MPa | 0.34 | OK | P=46.5 kN at centre plate, span 1728 mm (rail c/c), simply supported Doublers PL10×100 top+bottom over centre 600 mm; internal PL10 diaphragm each side of centre plate. |
| C3a | Coach truck transom 2×HSS10x4x1/4 upright, ×2.0 | 65.9 | 345.0 | MPa | 0.19 | OK | P=46.5 kN at centre plate, span 1449 mm between sideframes  |
| C3b | Coach truck sideframe PL25×170 A36, ×1.3 | 80.0 | 150.0 | MPa | 0.53 | OK | Simply supported on axlebox springs 1,200 mm apart, transom load at centre  |
| C3b | Coach truck sideframe PL25×170 A36, ×2.0 | 123.1 | 250.0 | MPa | 0.49 | OK | Simply supported on axlebox springs 1,200 mm apart, transom load at centre  |
| C4 | Loco main rail HSS12x6x3/8, vertical ×2.0 (uniform equivalent) | 90.1 | 345.0 | MPa | 0.26 | OK | Sprung body 8439 kg (LT42 reactions) spread uniformly; overhang 3775 mm Ballast sits directly over the front bolster, adds no frame moment. |
| C4b | Loco main rail at rear sill, drawbar 70 kN service + vertical ×1.3 | 105.7 | 207.0 | MPa | 0.51 | OK | Eccentric drawbar: rail centroid Z1302 − coupler Z550 = 752 mm; moment shared by both rails via end sill + knee gussets  |
| C4b | Loco main rail at rear sill, drawbar 200 kN ultimate + vertical ×1.3 | 193.3 | 345.0 | MPa | 0.56 | OK | Eccentric drawbar: rail centroid Z1302 − coupler Z550 = 752 mm; moment shared by both rails via end sill + knee gussets  |
| C5 | Loco rear drop box PL16 A572-50 root bending, 70 kN | 8.9 | 207.0 | MPa | 0.04 | OK | Lever 600 mm, box 552×400 mm  |
| C5 | Loco rear drop box PL16 A572-50 root bending, 200 kN | 25.6 | 345.0 | MPa | 0.07 | OK | Lever 600 mm, box 552×400 mm  |
| C5w | Loco rear box root weld, 10 mm fillet all round, 200 kN | 67.5 | 289.2 | MPa | 0.23 | OK | E70 weld metal: 0.6×FEXX = 289 MPa nominal (ultimate case)  |
| C5 | Tender drop box PL16 A572-50 root bending, 70 kN | 3.0 | 207.0 | MPa | 0.01 | OK | Lever 286 mm, box 702×400 mm  |
| C5 | Tender drop box PL16 A572-50 root bending, 200 kN | 8.7 | 345.0 | MPa | 0.03 | OK | Lever 286 mm, box 702×400 mm  |
| C5w | Tender box root weld, 10 mm fillet all round, 200 kN | 31.0 | 289.2 | MPa | 0.11 | OK | E70 weld metal: 0.6×FEXX = 289 MPa nominal (ultimate case)  |
| C6a | Drawbar PL32×150 A572-50 net tension at Ø61 hole, 200 kN | 70.2 | 345.0 | MPa | 0.2 | OK | Net section (150−61)×32  |
| C6b | Drawbar bearing on Ø60 pin, 200 kN | 104.2 | 517.5 | MPa | 0.2 | OK | Bearing limit 1.5 Fy (ultimate case)  |
| C6c | Drawbar 1473 mm buckling (weak axis, pinned) at 70 kN buff | 140,000.0 | 372,635.5 | N | 0.38 | OK | Euler Pcr=373 kN; require ≥2.0× service Pins allow rotation in plan; vertical rotation restrained by pocket plates - pinned assumed (conservative). |
| C6c | Drawbar 800 mm buckling (weak axis, pinned) at 70 kN buff | 140,000.0 | 1,263,309.4 | N | 0.11 | OK | Euler Pcr=1263 kN; require ≥2.0× service Pins allow rotation in plan; vertical rotation restrained by pocket plates - pinned assumed (conservative). |
| C6d | Pin Ø60 4140 Q&T bending, 200 kN, spacer bushings (4 mm gap) | 103.7 | 655.0 | MPa | 0.16 | OK | Double shear pin; M=F/2×(gap+t_plate/2+t_bar/4)  |
| C6e | Pin Ø60 double shear, 200 kN | 35.4 | 393.0 | MPa | 0.09 | OK |   |
| C6f | Pocket plates PL20 bearing on pin, 200 kN | 83.3 | 517.5 | MPa | 0.16 | OK |   |
| C6g | Safety chains 2× Grade 100 1/2 in, WLL vs 70 kN service | 70,000 | 133,400 | N | 0.52 | OK | NACM WLL 15,000 lbf each (verify with chain supplier certificate)  |
| C6h | Safety chains 2× Grade 100 1/2 in, MBS vs 200 kN | 200,000 | 533,600 | N | 0.37 | OK | Min. break = 4×WLL per NACM grade 100  |
| C7 | Loco (front driver, full ballast) axle wheel seat Ø140 bending (fatigue screen) | 63.2 | 120.0 | MPa | 0.53 | OK | Q=23.4 kN/wheel, ×1.25 vertical, Y=0.35×axle load on flange at r=725; bearing arm 176 mm Allowable 120 MPa = EN 13103 wheel-seat permissible for A1N-class steel used as a screen; axle steel 4140 Q&T or EA1N; engineer to run full EN 13103/AAR check. |
| C7 | Coach axle wheel seat Ø110 bending (fatigue screen) | 52.2 | 120.0 | MPa | 0.44 | OK | Q=16.2 kN/wheel, ×1.25 vertical, Y=0.35×axle load on flange at r=300; bearing arm 169 mm Allowable 120 MPa = EN 13103 wheel-seat permissible for A1N-class steel used as a screen; axle steel 4140 Q&T or EA1N; engineer to run full EN 13103/AAR check. |
| C7t | L3 axle Ø120 keyed seat torsion at 400 bar HPRV (TA7315H15MS 14.9:1) | 30.7 | 262.0 | MPa | 0.12 | OK | T_axle=10430 N·m (1.75 N·m/bar × 400 × 14.9, no η credit); axle 34CrNiMo6 Q&T (L3 fix)  |
| C7k | L3 reducer hub key 32×18 in 32×11×269 keyseat on Ø120 - hub-side bearing at 400 bar HPRV | 92.3 | 150 | MPa | 0.62 | OK | Dodge 120 mm straight bore keyseat 32×11×269 (catalog); sled-runner keyseat ends (L3 fix) Slip fit - shaft k6 + retaining collar AWAIT Dodge |
| C7g | L3 TA7315H15MS start: slip-limit torque × SF 1.6 vs 200 % starting allowance (2 × 11,030 N·m) | 10,998 | 22,060 | N·m | 0.5 | OK | Dodge metric TA II catalog: 11,030 N·m at 10 rpm SF 1.0, '200 % overload starting capacity'; SF 1.6 heavy shock ASSUMED Industrial rating - Dodge Application Engineering to confirm rail traction use (AWAIT) |
| C7h | L3 TA7315H15MS running: 2 % hold torque × SF 1.6 vs catalog rating at 16 rpm | 5,603 | 10,718 | N·m | 0.52 | OK | Rating interpolated 10/20 rpm, 15:1 column  |
| C7s | L3 Ø120 keyed seat fatigue (Goodman): required n 1.5 vs available (34CrNiMo6, sled-runner key, induction-hardened seat) | 1.5 | 1.8 | n req/avail | 0.82 | OK | As-found 4140 profile keyseat n = 0.96 (NG) - fix applied; induction-hardening factor 1.5 ASSUMED  |
| C7n | L3 TA rod anchor bracket weld 2×200×10 fillet to transom, 1.5×HPRV + 3 g | 36.2 | 145.0 | MPa | 0.25 | OK | Rod force 22.2 kN at 400 bar HPRV, arm 470 mm; bracket cantilever 155; E70 0.3×483  |
| C8 | Loco body bolster box (PL12 flanges 350, PL10 webs, 305 deep), rear, ×2.0 | 9.7 | 250.0 | MPa | 0.04 | OK | Rear body reaction 5873 kg (LT42) at centre plate, span 480 mm (rails Y±240, rev L1)  |
| C8f | Loco front bolster with full 1.5 t ballast, ×2.0 | 6.7 | 250.0 | MPa | 0.03 | OK | Ballast load lands on rails directly; conservative to put on bolster  |
| C9a | Ballast pocket end wall PL20, 3 g longitudinal | 87.6 | 150.0 | MPa | 0.58 | OK | 750 kg per side, resultant at mid-height of 255 mm stack; wall acts as cantilever 480 wide 3 g longitudinal / 2 g vertical / 1 g lateral ASSUMED (engineer to set per ASTM F2291). |
| C9b | (Original idea) PL12 end wall, 3 g longitudinal | 243.3 | 150.0 | MPa | 1.62 | NG | Shows why the end walls are PL20  |
| C9c | Ballast hold-down 4× M20 cl. 8.8 rods, 1 g up + preload | 1,838.7 | 70,419.2 | N | 0.03 | OK | Each rod tensile stress area 245 mm², proof 600 MPa; ASD limit  |
| C10a | Cab step tread PL8 × 240, 500 span, 300 lb point | 65.1 | 150.0 | MPa | 0.43 | OK | IBC 1607 stair tread 300 lb concentrated (ASSUMED code basis)  |
| C10b | Cab step tread deflection | 1.7 | 2.1 | mm | 0.81 | OK | Limit L/240  |
| C10c | Grab iron Ø32 solid A36, 1,200 span, 200 lb any direction | 83.0 | 150.0 | MPa | 0.55 | OK | OSHA 1910.29 / IBC 1607.9 200 lb (ASSUMED code basis)  |
| C10d | Coach platform guard post 1-1/2 in sch 40 A53B, 200 lb at 42 in | 177.8 | 144.6 | MPa | 1.23 | NG | Cantilever post from floor/side sill  |
| C10d | Coach platform guard post 2 in sch 40 A53B, 200 lb at 42 in | 103.3 | 144.6 | MPa | 0.71 | OK | Cantilever post from floor/side sill  |
| C10e | Cab roof purlin HSS2x2x1/8 @600, 20 psf live + dead | 77.6 | 207.0 | MPa | 0.38 | OK | Span 2,700 mm simply supported  |
| C10f | Cab roof purlin HSS2x2x1/8 deflection | 11.6 | 15.0 | mm | 0.77 | OK | Limit L/180  |
| C10g | Cab roof purlin HSS3x2x1/8 @600 deflection (adopted) | 4.4 | 15.0 | mm | 0.29 | OK | Limit L/180  |
| C10h | Cab roof purlin HSS3x2x1/8 @600 bending (adopted) | 43.9 | 207.0 | MPa | 0.21 | OK |   |
| C11 | Coach empty wind overturning FS at 67 mph gust | 1.5 | 1.4 | FS req/avail | 1.09 | NG | Side area 23.2 m², Cd 1.2, centroid Z1750 mm, restoring m·g·gauge/2 Requirement FS ≥ 1.5 ASSUMED; engineer to set per ASTM F2291 environmental loads. |
| C11 | Coach loaded wind overturning FS at 67 mph gust | 1.5 | 2.3 | FS req/avail | 0.67 | OK | Side area 23.2 m², Cd 1.2, centroid Z1750 mm, restoring m·g·gauge/2 Requirement FS ≥ 1.5 ASSUMED; engineer to set per ASTM F2291 environmental loads. |
| C11 | Locomotive wind overturning FS at 67 mph gust | 1.5 | 1.8 | FS req/avail | 0.86 | OK | Side area 35.0 m², Cd 1.2, centroid Z1900 mm, restoring m·g·gauge/2 Requirement FS ≥ 1.5 ASSUMED; engineer to set per ASTM F2291 environmental loads. |
| C11 | Tender wind overturning FS at 67 mph gust | 1.5 | 4.2 | FS req/avail | 0.36 | OK | Side area 9.5 m², Cd 1.2, centroid Z1430 mm, restoring m·g·gauge/2 Requirement FS ≥ 1.5 ASSUMED; engineer to set per ASTM F2291 environmental loads. |
| C13 | Start on 2% (L3 train mass), 350 bar, H1B110 + TA7315H15MS (η start 0.90; adhesion-capped) | 31.5 | 37.9 | kN | 0.83 | OK | 4 × 1.75 N·m/bar × 350 × 0.90 × belt 0.97 × 14.9 × 0.96 / 0.725 = 42.2 kN, capped at dry adhesion 37.93 kN; 262 bar needed η start 0.90 ASSUMED (AWAIT Danfoss starting torque); L2 custom case rejected |
| C13g | L3 2% start at pessimistic η start 0.80 (pending Danfoss) | 31.5 | 37.5 | kN | 0.84 | OK | 294 bar needed at η 0.80 vs 350 limiter  |
| C13s | Wet 2% start needs sand: required μ vs sanded μ 0.25 | 0.2 | 0.2 | μ | 0.83 | OK | Wet adhesion 0.15 gives 22.76 kN; sander on leading axle each direction REQUIRED Sanded μ 0.25 ASSUMED (rail practice 0.25-0.30) |
| C13b | Level wet start vs wet adhesion (per-axle anti-slip) | 14.9 | 22.8 | kN | 0.66 | OK | μ wet 0.15 on L3 driver weight  |
| C13t | Start on 2% at 350 bar, tender 9,315 kg (rev T1 built up, before savings) | 31.6 | 37.9 | kN | 0.83 | OK | Train 77.8 t with stairs, tender swapped from the 8,160 kg ledger; 0.40 kN per t (L3 drive capacity)  |
| C13u | Start on 2% at 350 bar, tender 8,304 kg (rev T2, owner-approved TW-1 subset, in model) | 31.2 | 37.9 | kN | 0.82 | OK | Train 77.8 t with stairs, tender swapped from the 8,160 kg ledger; 0.40 kN per t (L3 drive capacity)  |
| C14 | Max static wheel load with full ballast vs rail screening basis | 23.4 | 22.9 | kN | 1.02 | NG | Rail screening used 22.85 kN; new basis 24 kN (ASCE 40 base stress ≈ 101×23.4/22.85 = 103 MPa) Not a failure - update the rail basis to 24 kN. |
| C11w | Coach empty overturning FS at 40 mph gust (adopted no-run limit) | 1.5 | 3.9 | FS req/avail | 0.39 | OK | Owner decision R2: no running above 40 mph gusts; parked train tied down (wind tie-downs)  |
| C11w | Coach loaded overturning FS at 40 mph gust (adopted no-run limit) | 1.5 | 6.3 | FS req/avail | 0.24 | OK | Owner decision R2: no running above 40 mph gusts; parked train tied down (wind tie-downs)  |
| C11w | Locomotive overturning FS at 40 mph gust (adopted no-run limit) | 1.5 | 4.9 | FS req/avail | 0.3 | OK | Owner decision R2: no running above 40 mph gusts; parked train tied down (wind tie-downs)  |
| C11w | Tender overturning FS at 40 mph gust (adopted no-run limit) | 1.5 | 11.7 | FS req/avail | 0.13 | OK | Owner decision R2: no running above 40 mph gusts; parked train tied down (wind tie-downs)  |
| C15a | Stair tread formed channel 3/16 in (4.8) x 280 go x 40 flanges, 914 span, 300 lb point | 70.4 | 150.0 | MPa | 0.47 | OK | Simply supported between stringers; IBC 1607 300 lb concentrated on 4 in² (ASSUMED code basis)  |
| C15b | Stair tread deflection, 300 lb point | 0.7 | 3.8 | mm | 0.19 | OK | Limit L/240  |
| C15c | Stair stringer PL8x150 A36, 100 psf crowd + dead (per stringer) | 23.6 | 150.0 | MPa | 0.16 | OK | Horizontal span 1550 mm hinge-to-foot; plan area 1.28 m²; 100 psf = 4.79 kPa (IBC 1607 stairs, ASSUMED)  |
| C15d | Stair stringer deflection (along slope) | 0.7 | 5.2 | mm | 0.13 | OK | Limit L/360  |
| C15e | Chain stay 3/8 in Grade 70 (x2), foot unsupported, full crowd | 5.2 | 29.4 | kN | 0.18 | OK | Moment of full load about the floor hinge / 548 mm chain lever arm; WLL 6,600 lbf for 3/8 G70 ASSUMED - verify on chain tag / supplier (AWAIT)  |
| C15f | Floor hinge pin Ø25 4140 Q&T (2 per stair), single shear | 9.4 | 262.0 | MPa | 0.04 | OK | Hinge reaction with chains loaded; brackets/bolts to side sill by PE  |
| C15g | Stair handrail 1-1/2 in sch 40 A53B, 200 lb at mid-span (662 along slope) | 27.6 | 144.6 | MPa | 0.19 | OK | Posts at treads 1, 3, 5; IBC 1607.9 200 lb any direction (ASSUMED)  |
| C15h | Stair handrail post 2 in sch 40 A53B, 200 lb at 895 above tread | 86.6 | 144.6 | MPa | 0.6 | OK | Fold-flat post locked upright by strut + Ø16 pin  |
| C15i | Stair handrail post lock pin Ø16 4140, double shear | 19.8 | 262.0 | MPa | 0.08 | OK | Couple over 100 mm hinge-to-pin  |
| C16a | Cab clear headroom (deck to purlin underside) vs 6 ft 3 in crew + shoes | 1,905 | 2,009.8 | mm | 0.95 | OK | Roof top 3700 - 3 skin - 76.2 HSS3x2 purlin = 3621; cab floor PL6 top 1605; 6 mm floor mat 1,905 mm standing target ASSUMED (owner/crew to confirm) |
| C16b | Route overhead clearance adopted vs train height + 300 sway/bounce/track-lift + 300 decorations | 4,300.0 | 4,300 | mm ARL | 1.0 | OK | Adopted R2: nothing lower than 4,300 mm above top of rail within 2,000 mm of track CL (lights, wires, signs, branches, arches)  |

Note: rows marked NG are the as-found conditions that drove a fix (PL12 wall, 1-1/2 in post, empty-coach 67 mph wind; DT5 key/FA25 coupling eliminated in L2; L3 as-found 4140 keyseat fixed by C7s) or a basis update (rail 24 kN). C11 ratio = required FS / available FS.

## Wind stability

| Vehicle | Mass kg | Side area m² | FS 40 mph | FS 67 mph |
|---|---|---|---|---|
| Coach empty | 8,040 | 23.2 | 3.85 | 1.37 |
| Coach loaded | 13,200 | 23.2 | 6.33 | 2.25 |
| Locomotive | 16,810 | 35.0 | 4.92 | 1.75 |
| Tender | 8,160 | 9.5 | 11.71 | 4.17 |

## Clearance (R = 100 m)

- coach_end_out: 91 mm
- coach_mid_in: 38 mm
- loco_end_out: 148 mm
- loco_mid_in: 13 mm
- static_half: 1457.0 mm
- sway: 90 mm
- dynamic_half: 1696 mm
- recommended: 2000 mm

## Traction (rev L3: 4 × H1B110 → 1:1 belt → Dodge TA7315H15MS 14.9:1, Ø1,450, η start 0.90 / reducer 0.96 / belt 0.97 assumed)

Forces in kN unless the key names another unit (bar, cc, rpm, L/min); L2_F350_rejected = the rejected L2 custom case.

- F350: 42.2
- F400: 48.23
- need_2pct_77t5: 31.03
- need_level_wet: 14.91
- wet_adh: 22.76
- L2_F350_rejected: 37.61
- wheel: 1450.0
- ratio: 14.9
- need_2pct_T2: 31.53
- p_needed_bar: 262

## Notes

- Rev L3 drive: 4 × Danfoss H1B110 (110/22 cc, min-displacement stop 60 cc = 6 mph governed) → 1:1 synchronous belt → Dodge TA7315H15MS 14.9:1 on a Ø120 keyed axle seat; axle torque at the 350 bar limiter 8498 N·m, structural peak at the 400 bar HPRV 10430 N·m (no efficiency credit). L2 spur case rejected (custom).
- C15 stair: 6 equal risers of 177 mm (floor 813 to ground -250 ARL), 5 treads x 280 going, ~32.3 deg, 914 clear between stringers, est. mass 120 kg/stair. Foot pad adjusts +/-75 mm; where ground varies more, last riser ranges ~100-250 mm - crew checks. Latches: primary gravity latch + safety pin, rated >= 3 g x stair weight (~3.5 kN) - hardware rating AWAIT supplier. Gas-spring / damper force AWAIT supplier.

## Emergency / boarding stairs (R2)

- risers: 6
- rise: 177.2
- treads: 5
- go: 280.0
- pitch_deg: 32.3
- clear_width: 914.0
- total_rise: 1063
- run_h: 1550.0
- reach_from_CL: 2947.0
- mass_kg_est: 120
- count: 18
- rail_height: 865.0
- foot_adj: 75.0

## Cab headroom and route overhead clearance (R2)

- roof_top: 3700.0 mm
- purlin_underside: 3620.8 mm
- cab_floor: 1605.0 mm
- clear_to_deck: 2016 mm
- clear_with_mat: 2010 mm
- target: 1905 mm
- overhead_min: 4300 mm
- train_height: 3700.0 mm

## Revision history

| Rev | Date | Description |
|---|---|---|
| R1 | 2026-10-27 | Initial design review, model, 12-sheet set, calcs. |
| R2 | 2026-10-27 | Owner decisions: emergency stairs at every coach door (F08, F21, C15, C-304); 40 mph wind no-run limit + tie-downs decided (F05, C11w); cab roof 3,700 adopted, headroom ≈1,960 verified, route overhead clearance 4,300 (F04, C16); pony truck still open - recommend delete (F06). |
| L1/L1b | 2026-10-27 | Loco back to owner plan Ø1,450 drivers, inside frames (F25 opened); 4 staggered MSE05 motors. |
| L2 | 2026-10-27 | Owner chose F25 (c): inboard axle-hung spur-gear case 21:38 (1.81:1) per axle, MSE05 shaft motors inboard, nose link to transom, pinion-shaft disc brakes, sanders; outboard DT5 cartridges/couplings/motors removed; F03 and F25 resolved. |
| L3 | 2026-10-28 | Owner: choose the best fit (F26). Catalog Dodge TA7315H15MS 14.9:1 + Danfoss H1B110 via 1:1 synchronous-belt drop (F27 envelope fix), Ø120 keyed seat in 34CrNiMo6 induction-hardened, axle disc + 2 calipers on the free side, Dodge TA rod to the transom. Governed 6 mph owner-selected (F29). L2 custom case rejected; fallback 5:1 + MS05. TA II not rail-rated - Dodge AE open (F28). |

## Codes path

Clark County Code Ch. 22.16 (Ord. 5378) → Nevada PE stamps design + calcs → third-party inspection by one of the 4 County-approved QA agencies → County permit / operating inspection. Standards to cite: ASTM F2291, F1193, F770, F3598; AISC 360; AWS D1.1. Stairs: PE to confirm basis (IBC 1011 / 1607, ASTM F770 egress, OSHA 1910.25 as reference).
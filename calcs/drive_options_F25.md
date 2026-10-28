# F25 — Loco drive options on Ø1,450 drivers (comparison, rev L1) — DECIDED: option (c) inboard spur-gear, rev L2

DECIDED 27 Oct 2026: owner chose option (c) - inboard axle-hung spur-gear case per axle, built as rev L2 at 21:38 (1.81:1), Poclain MSE05 750/375 cc, 350 bar working / 380 bar relief, pump H1P053. Chains ruled out by owner. 2% start 38.8 kN at 350 bar (adhesion-capped 37.0 kN dry). Design: calcs/L2/gear_drive_L2.json, drawings L-103 / L-106, PF-CT_PE_calc_package §4. The option analysis below is kept for the record (rev L1 basis).

Pulsipher Farms Christmas Train — preliminary, not for construction until PE stamped. Memo date 27 Oct 2026. Comparison only: the adopted drive in model.py (4 × MSE05 750 cc at 1:1 on the axle ends) is not changed. Calc script: calcs/drive_options_F25.py (results in calcs/F25/drive_options_F25.json). Sketches: calcs/F25/F25_A/B/C_sketch.png.

## 1. The problem and the basis

- Owner decision (27 Oct): the Ø1,450 drivers stay ("thats how the drive should have been designed is with the bigger wheels"). On Ø1,450 the adopted 1:1 drive gives 21.9 kN at 350 bar against 31.2 kN for a 2% start with the T2 tender (−9.3 kN). That is F25.
- Train 77.94 t (T2), W = 764.4 kN. Resistances (render check, renders_work/traction.py): 2% start 31.20 kN, level start 14.99 kN, 2% running 19.11 kN, level running 3.82 kN.
- Adhesion on the drivers (143.3 kN, C13b): dry μ 0.25 = 35.8 kN, wet μ 0.15 = 21.5 kN. More than about 36 kN cannot be used on dry rail.
- Start force = motors × 350 bar × displacement / 2π × starting efficiency × ratio × drive efficiency / wheel radius 0.725 m. Starting efficiency 0.95 is the calc-notes basis (C13); 0.80 is the plan LT25 conservative value. Both are shown because Poclain has not confirmed it (AWAIT).
- Running power uses the LT25 method: 35 kW pump allowance on the V3307 (45.6 kW reference net continuous − 3 charge − 7 aux), pump 0.855, motor 0.855, 10 bar circuit loss, chain 0.97 per stage.
- Pump flow at 2,600 rpm, 0.95 volumetric: H1P045 111 L/min, H1P053 133 L/min, H1P060 149 L/min (Danfoss technical data: 045 max working 420 bar; 053 max working 380 bar, same SAE B flange; 060 max working 420 bar, SAE C flange).
- Poclain data (selection guide 2026, MS08 catalog 801478189C): MSE05 503–750 cc, 400 bar max, 250 rpm (2nd displacement 375 cc, 300 rpm), 29 kW, shaft motor Ø300 × 370, 55 kg. MSE08 1,043–1,248 cc, 400 bar, 125 rpm (2nd 522–624 cc, 110 rpm), 41 kW, shaft motor Ø335 × 418, 85 kg. MS11 730–1,259 cc, 450 bar, 200 rpm, Ø375 × 458.5, 114 kg. MS05 260–560 cc, 450 bar, 350 rpm. No Poclain motor is made at exactly 1,070 cc in a 400–450 bar frame except MS08 (467–934 cc, too small) or MSE08 1,043 cc; 1,146 and 1,248 are the practical B sizes.

## 2. Key numbers

| Item | A 1.5:1 | A 1.6:1 | A 1.75:1 (recommended) | A 2:1 | B MSE08 1,146 cc | B MSE08 1,248 / MS11 1,259 | C plan 2 × 560 cc 4:1 | Adopted now (1:1) |
|---|---|---|---|---|---|---|---|---|
| Start force at 350 bar, η 0.95 (kN) | 31.9 | 34.0 | 37.2 (capped at 35.8 by adhesion) | 42.5 (capped 35.8) | 33.5 | 36.4 / 36.8 (capped 35.8) | 30.8 | 21.9 |
| Same at η 0.80 (kN) | 26.8 | 28.6 | 31.3 | 35.8 | 28.2 | 30.7 / 31.0 | 25.9 | 18.4 |
| 2% dry start margin vs 31.2 kN, η 0.95 / 0.80 | +0.7 / −4.4 | +2.8 / −2.6 | +4.6 / +0.1 | +4.6 / +4.6 | +2.3 / −3.0 | +4.6 / −0.5 | −0.4 / −5.3 | −9.3 / −12.8 |
| Level wet start (needs 15.0, wet adhesion 21.5) | OK | OK | OK | OK | OK | OK | OK | OK |
| 2% wet start (needs 31.2, wet adhesion 21.5) | adhesion-limited, sand needed | same | same | same | same | same | same | fails on torque too |
| Motor rpm at 7.5 mph (limit) | 66 (250/300) | 71 | 77 | 88 | 44 (125/110) | 44 (125/110 or 200) | 177 (350) | 44 |
| Flow at 7.5 mph, small displacement (L/min) | 105 | 112 | 122 | 139 | 107 | 116 / 117 | 208 (single-speed 560) | 70 |
| Level top speed H1P045 / 053 / 060 (mph) | 8.0 / 9.5 / 10.7 | 7.5 / 8.9 / 10.0 | 6.8 / 8.2 / 9.2 | 6.0 / 7.1 / 8.0 | 7.8 / 9.4 / 10.5 | 7.2 / 8.6 / 9.6 | 4.0 / 4.8 / 5.4 (8.0 / 9.6 / 10.7 if 2-speed MS05) | 12 / 14 / 16 (not limiting) |
| 2% balancing speed, V3307, 35 kW pump | 2.8 mph | 2.8 | 2.8 | 2.7 | 2.9 | 2.9 | 2.7 | 2.9 |
| Engine needed for 7.5 mph on 2% (net continuous) | about 104 kW | 105 | 105 | 106 | 102 | 102 | 107 | 100 |
| Hardware | RS140-2 16T:24T | RS140-2 15T:24T | RS140-2 16T:28T, axle-hung oil-bath case | RS140-2 14T:28T | MSE08 shaft motor + ≥12 kN·m coupling | MSE08/MS11 + coupling | 2 jackshafts, 21/49 RS120 + 1.71 first stage | DT5 cartridge + KTR FA25 |
| Chain pull at motor max pressure (kN) / allowable | 40.0 / 68.4 | 42.6 / 68.4 | 40.0 / 68.4 (RS140-2) | 45.7 / 68.4 | — | — | 18.8 at 350, 22.5 at 420 / 30.4 (RS120) | — |
| Outermost drive part (Y, mm; body 1,300) | none outboard | none | none | none | ≈1,390 | ≈1,390–1,430 | none | 1,151 |
| Mass change vs adopted (ASSUMED) | ≈ +100 kg | ≈ +100 | ≈ +100 | ≈ +100 | ≈ +300 | ≈ +420 | ≈ +70 | 0 |
| Shop hours, net (ASSUMED ±30%) | 70–120 | 70–120 | 70–120 | 70–120 | 100–150 | 100–150 | 150–220 | — |
| Engineering hours (ASSUMED) | 70–110 | 70–110 | 70–110 | 70–110 | 60–100 | 60–100 | 130–190 | — |
| Relative cost (A = 1.0) | 1.0 | 1.0 | 1.0 | 1.0 | about 1.3 | about 1.4 | about 1.35 | — |

Margins use min(force, dry adhesion) − 31.2 kN. Level top speeds are flow-limited in the small displacement; on the level the power is ample (12.8 kW at the rim for 7.5 mph against about 23.5 kW available), so speed is set by pump flow and a 7.5 mph governor, not the engine.

## 3. Option A — per-axle reduction, 4 × MSE05 750/375 cc (recommended at 1.75:1)

- Layout: one oil-bath chain case per axle, hung on the axle on two bearings, with the motor bolted to it and a rubber-bushed nose link to the truck transom (the classic nose-suspended traction-motor arrangement). Case tilted about 15° down toward the truck centre: motor centre about 386 mm from the axle and Z621.
- Clearances (sketch A): motor top Z771 vs transom underside Z850 = 79 mm; motor housing to axle surface 171 mm; axle sprocket Ø397 PD keeps the case bottom about 485 mm above rail. Across the truck the case is 150 wide and the motor body spans Y −220…+150, leaving 50 mm to the opposite inside axlebox (Y270). The Ø325 brake rotor fits on the axle beside the case (the motor is offset 386 mm, so it clears the rotor by about 75 mm). Fits inside the inside-frame trucks; nothing outside the wheels. Primary-spring travel does not change chain centres because the case rides on the axle.
- Ratio choice: 1.5:1 meets the start only with η 0.95 (+0.7 kN, 2%). 1.6:1 gives +2.8 kN at η 0.95 but −2.6 kN at η 0.80. 1.75:1 is adhesion-limited at η 0.95 and still meets the start at η 0.80; with H1P053 it still reaches 8.2 mph on the level. 2:1 gives no more usable start (adhesion cap) and costs top speed. So 1.75:1 (16T:28T) is the sweet spot; 1.6:1 (15T:24T) is acceptable if Poclain confirms ≥ 0.90 starting efficiency.
- Chain: Tsubaki RS140-2 duplex, maximum allowable load 15,370 lbf = 68.4 kN (catalog). Pull 34 kN at a 350 bar start, 40 kN at the MSE05 400 bar maximum → factor 1.71. RS120-2 (51.4 kN) is too tight (1.29). Small sprocket at most 88 rpm, so lubrication is a slow-speed oil bath. Final selection AWAIT Tsubaki.
- Torque reaction: axle torque 7.94 kN·m at 400 bar stays inside the case; only the case reaction (motor torque × 0.75 = 3.4 kN·m) goes to the transom, about 7.6 kN on the nose link at a 450 mm arm. The inside axleboxes see weight plus the small nose reaction, not the chain pull.
- Axle and keys: axle Ø130 torsion 18.4 MPa at 400 bar. Axle sprocket on a keyless locking assembly (size AWAIT) or key 32 × 18 × 150 at 90 MPa bearing stress (< 150 MPa allowable). C7c (KTR coupling) and C7k (DT5 hub key 243 MPa) disappear because the outboard coupling and hub are deleted.
- Motor: MSE05 shaft-motor version (Ø300 × 312–370, 55 kg). Shaft radial load from a 40 kN chain pull is AWAIT Poclain (catalog curves only). If too high, add an outboard support bearing on the motor sprocket in the case wall.
- Pump: H1P053 (same SAE B flange as 045, 133 L/min, 380 bar max working) gives 8.2 mph on the level with 9% flow margin at 7.5 mph. H1P045 tops out at 6.8 mph at 1.75:1 (7.5 mph at 1.6:1, no margin). H1P060 adds speed but needs an SAE C engine adapter (AIE).
- Look: the outside of every driver shows only the wheel face, crank pin and side rod, like the plans. The DT5 outboard motors that now stick out to Y1,151 go away.
- Side rods: the axles are in a parallel hydraulic circuit, so moving rods do not fight the motors (hydraulic motors are speed-compliant). If the rods are made to move, they also share torque when one axle slips (a real-loco benefit) and must be sized for about half an axle's slip torque (about 11 kN rod force at r300, ASSUMED). Otherwise keep them decorative with a slotted big end.

## 4. Option B — bigger direct-drive motors at 1:1 (4 × MSE08 1,146–1,248 cc or MS11 1,259 cc)

- Real models: Poclain MSE08 1,146 cc (2nd 573) or 1,248 cc (2nd 624), 400 bar, 7,945 N·m, 125 rpm; or MS11 1,259 cc (2nd 630), 450 bar, 9,000 N·m, 200 rpm. MSE08 1,043 cc is too small (30.4 kN at η 0.95).
- Performance: 1,146 cc meets the start at η 0.95 (+2.3 kN) but not at η 0.80 (−3.0 kN). 1,248 cc and MS11 are adhesion-limited at η 0.95 and about 0.5 kN short at η 0.80. Small-displacement flow at 7.5 mph is 107–117 L/min, fine on H1P053. 2% speed is the same as A.
- Packaging: a 1:1 motor must be coaxial with the axle, and the axle runs straight through between the wheels, so the motor can only sit on the axle end, outside the wheel and rods (like DT5, but bigger). Ø335 × 418, 85 kg per end; with a cartridge and coupling it reaches Y≈1,390, past the 1,300 body line and the 1,250 running board.
- Torque reaction: the arm cannot reach the inside frame because the rotating wheel and side rods are in the way. It needs an outside torque bar on each side, carried by a cross-member passing under the rods between the two wheels (Z≈160–220). That is effectively a visible outside frame.
- Coupling and key: torque rises to 7,945 N·m, so the coupling needs ≥ 11.9 kN·m with service factor 1.5 (KTR size AWAIT). The axle-stub key gets worse than today's C7k, so it must go to a spline or locking assembly. C7c and C7k remain open problems.
- Look: large motor cans outside every driver plus a torque bar. This is the "goofy" outcome; it hides the wheel faces and crowds the rods (5 mm between rod and cartridge today).
- Upside: simplest hydraulics, no chains, quietest, motor parking brake acts directly on the axle.

## 5. Option C — the plans' own drive (LT23–LT25): 2 × MS05 560 cc, 4:1, jackshaft + chains

- Layout per LT18: one motor per powered truck drives a jackshaft under the transom (Z≈560, first stage about 1.71:1), and two RS120 chains 21T/49T (2.333:1) run to the axles (Ø595 PD axle sprockets). Everything is inboard, so the look is as clean as A.
- Performance: start 30.8 kN at η 0.95 and 25.9 kN at η 0.80 (two chain stages), both short of 31.2. Raising relief to 420 bar (MS05 is rated 450; pump H1P045/060 420) gives about 36.9 / 31.1 kN, marginal at η 0.80. With single-speed 560 cc the flow at 7.5 mph is 208 L/min, so top speed is 4.0 mph on H1P045 and 5.4 mph on H1P060, as LT23–LT25 found. A 2-speed MS05 (280 cc 2nd) would restore about 8 mph (AWAIT Poclain; LT25 assumed single-speed).
- Hardware: per truck one jackshaft on two pillow blocks, three sprockets, three chains with tensioners and guards, motor mount. Axle chain pull 18.8 kN at 350 bar (22.5 at 420) against 30.4 kN for single RS120. Three chain planes plus a Ø300 motor must fit in 540 mm between the inside axleboxes, which is very tight. LT18 itself lists chain load, bearings, lubrication, guards and suspension compensation as unresolved.
- Reliability: two motors instead of four, so one chain or motor failure loses half the loco's drive and hydrostatic retard. Most wearing parts and adjustments. Cheapest in motors (two fewer), but the most engineering and shop time.

## 6. Grade speed, bigger pump or engine

- With the V3307 (45.6 kW reference net continuous, 35 kW to the pump) every option balances at about 2.7–2.9 mph on 2%. The drive choice does not change this; only engine power does.
- 7.5 mph on 2% needs 19.1 kN × 3.35 m/s = 64 kW at the rim, about 92–97 kW at the pump shaft and about 100–107 kW net continuous from the engine. That is the same order as the render check's 88 kW (75.6 t train, 0.75 overall, +5 kW).
- A bigger pump alone does not help on grades (engine-limited); it only raises level top speed where flow is the limit.
- Engine steps (Kubota published gross intermittent; net continuous ASSUMED at the V3307 ratio 0.82, AIE to confirm): V3800-CR-TIEF4 86.4 kW at 2,600 → about 71 kW net → about 4.8 mph on 2%. V3800-CR-TIEF4H 96.4 kW at 2,400 → about 79 kW → about 5.5 mph. V5009-TIE5B 157.3 kW at 2,200, 625 kg dry → 7.5 mph is reachable, but it also needs a pump of about H1P100–115 class, about double the cooling and a tender re-layout. Not recommended for a farm ride; the realistic grade speed with the V3307 is about 2.8 mph, or about 5 mph with a V3800 swap.

## 7. Braking, maintenance, noise, PE

- Braking: hydrostatic retard gets no safety credit in any option (Danfoss/LT25). Air brakes on axle rotors or treads stay the independent stopping and holding system. In A and C a motor multidisc brake would act through the chain, so it is not independent. In B it acts on the axle through the coupling. A loses retard on one axle if a chain fails; C loses a whole truck.
- Maintenance: A has 4 sealed oil-bath cases (oil level and chain stretch through an inspection port, ASSUMED 250 h checks) and nothing to grease outboard. B has 4 large outboard couplings and cartridges, easy to reach but exposed. C has 6 chains, tensioners and 2 jackshafts, the most adjustments.
- Noise: B quietest; A low (enclosed duplex chain, ≤ 88 rpm small sprocket); C highest (two open or guarded stages, long chains).
- Approvability: A uses catalog parts with a short, clear load path (Tsubaki chain selection, Poclain shaft motor, locking assembly, nose link), the easiest PE package. B needs a width exception, an unusual outside torque bar and a 12 kN·m coupling. C is the plan's design, but its start force is below need at 350 bar and LT18 leaves its chain, bearing and guard design open.

## 8. Recommendation

Adopt Option A at 1.75:1 (RS140-2 16T:28T) in an axle-hung oil-bath case on each axle, keeping the four MSE05 750/375 cc motors (shaft version) and moving the pump to H1P053. It is the only option that:
- meets the 2% dry start even at the plan's conservative 0.80 starting efficiency, and is adhesion-limited at 0.95;
- keeps about 8 mph on the level;
- puts nothing outboard of the Ø1,450 drivers, so the side rods and wheel faces look like the plans;
- deletes the C7c/C7k coupling and key failures and the unresolved outboard torque-reaction path;
- costs the least.

Keep the V3307 and accept about 2.8 mph on 2% (same for every option), or treat a V3800 swap (about 5 mph) as a separate engine decision. Fit driver sanders for wet 2% starts (adhesion-limited for every option).

## 9. Needs vendor confirmation

- Poclain:
  - MSE05 750/375 shaft-motor version: availability, dimensions, permissible radial load for a 40 kN chain pull at about 150 mm overhang, starting (breakaway) torque efficiency.
  - 2-speed shift under load.
  - Multidisc brake option.
  - Quote for B sizes (MSE08 1,146/1,248, MS11 1,259) only if B is kept.
  - MS05 560 2-speed if C is kept.
- Danfoss / AIE:
  - H1P053 order code with SAE B 13T or 15T shaft (G4 180/222 N·m vs 15T), pressure and power-limiting control to hold pump input ≤ 150 N·m.
  - AIE adapter for SAE B (053) or SAE C (060).
  - V3307 package continuous rating and derating.
  - Net continuous for V3800 variants if a swap is considered.
- Tsubaki: RS140-2 slow-speed selection with service factor, sprocket hardening, oil-bath lubrication.
- KTR / Ringfeder (or equal): locking assembly for Ø130 axle at 8 kN·m; KTR only if B.
- PE: axle-hung case, nose link and axle-sprocket fit; rods decorative or functional.

## Sketches
![A](/workspace/train/calcs/F25/F25_A_sketch.png)
![B](/workspace/train/calcs/F25/F25_B_sketch.png)
![C](/workspace/train/calcs/F25/F25_C_sketch.png)

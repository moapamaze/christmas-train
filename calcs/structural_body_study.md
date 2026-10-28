# PF-CT R2 Locomotive — Load-bearing body study (stressed skin vs hybrid vs conventional vs heavy plate)
Pulsipher Farms Christmas Train — preliminary, not for construction until PE stamped. Study note SB-1 rev A, 27 Oct 2026 (rev A: CWF in-house rolling; tender per owner plan LT45.1). Basis: R2 parametric model (build/model.py), R2 calcs (C4, C4b, C5, C8, C11, C14), CAD mass report. Coaches stay at R2 full size (2,794 W × 7,925 L, floor 813, roof 3,089); loco body kept at R2 size. No prices in this document.
## 1. Answer in plain words
- Keep the R2-size loco body, but do NOT make it load-bearing. The cheapest and simplest all-in is option 2: keep the R2 HSS12×6 frame (already designed and checked) and replace the 3 mm welded cosmetic hood with a 4.8 mm (3/16 in) rolled shell bolted to flat CNC-cut rings. It looks better than the R2 body and costs fewer shop hours.
- Update 27 Oct (owner): CWF has in-house boiler-shop plate rolling. Outside rolling cost and lead time are removed from every option, and option 4 is re-estimated with in-house rolling and boiler-shop seam welding. The ranking and the recommendation do NOT change. The hybrid with a 10 mm structural shell still takes about 1.9× the all-in hours of option 2, and thicker shells are over the mass budget (section 9a).
- Option 3 (heavy plate frame: 2 × PL20×500 A572-50 plates plus the same bolted shell) is effectively tied (≈ 6% more hours, within the accuracy of the estimate). It is the best choice if CWF would rather burn and weld thick plate than cope HSS, and it looks most like a real locomotive frame.
- A full thin stressed skin (option 5) takes about 3.3× the all-in hours of option 2 (FEA, buckling, fatigue, County QA, distortion control) and looks worst. The hybrid with a thick structural rolled shell (option 4) takes about 1.9× even with CWF rolling it in-house. It also makes the loco ≈ 0.5 t heavier than R2 with all ballast removed.
- Why load-bearing does not pay here: the drawbar (Z 550) and both bolsters still need a sill or drag box. The rear 2.7 m is the cab, where there is no boiler tube. The frame it would replace is only ≈ 3.8 t of a 16.8 t loco (wheels and trucks are ≈ 11 t). Weight is not a goal, so any saving goes back in as ballast.
## 2. Basis and load cases (R2)
- Sprung body 8,439 kg on bolsters x 4,075 / 7,275; frame x 300–10,900; overhang 3,775. Overhang moment 55.6 kN·m static, ×2.0 vertical = 111.3 kN·m (R2 C4 basis).
- Drawgear 70 kN service / 200 kN ultimate at coupler Z 550 (R2 C4b/C5). Jacking: 16.8 t on 4 points; twist case = 3-point jacking (one jack slack), T ≈ 91 kN·m (accidental).
- Fatigue range ±0.3 g (0.6 × static, ASSUMED). AWS D1.1 cyclically-loaded provisions / AISC 360 App. 3 thresholds: C 69, D 48, E 31, E′ 18 MPa. ~10^7 cycles over the life (rail joints), so stay below threshold.
- Allowables ASD 0.6 Fy bending (A572-50 / A500C: 207 MPa), Fy at ultimate. R2 boiler/hood shell is Ø1,640 (r 820, Z 2,560, x 600–8,000), NOT 1.0–1.2 m. Ø1,100 is also shown in the formability table in case the loco-size render study shrinks it.
## 3. Options and hand checks
| Option | What carries load | Vertical bending ×2.0 (MPa / 207) | Drawgear 70 / 200 kN (MPa) | Twist 3-pt jack (MPa) | Buckling | Fatigue range (MPa) & category |
|---|---|---|---|---|---|---|
| 2 R2 frame + better shell | Same R2 frame; shell non-structural, bolted (removable) | 90 | 117 / 225 (Fy 345) | 69 | n/a (cosmetic 4.8 mm, bolted, R/t 171: no oil-canning) | 27 — E (crossmember/gusset fillet attachments >100 mm on HSS wall), CAFT 31 MPa |
| 3 Heavy plate frame + better shell | 2 PL20×500 plate frames + 6 plate stretchers, bolster boxes, drag box; body cosmetic | 67 | 83 / 155 (Fy 345) | 51 | web h/t = 25 (compact, no stiffeners needed) | 20 — C (stretcher end fillets, short attachments) - CAFT 69 MPa; few details |
| 1 R2 as drawn | 2 HSS12×6×3/8 rails + crossmembers, bolster boxes, PL16 drop box; body cosmetic | 90 | 117 / 225 (Fy 345) | 69 | n/a (cosmetic 3 mm skin; oil-canning only) | 27 — E (crossmember/gusset fillet attachments >100 mm on HSS wall), CAFT 31 MPa |
| 4 Hybrid thick structural shell | Centre sill box 250×305 PL10/12 + 10 mm shell via saddles; structural cab | 4 | 60 / 171 (Fy 345) | 2 | 10 mm shell R/t 82: no stiffeners; sill alone carries drawbar aft of cab front (no shell there) | 1 — C/D at shell-to-sill saddles and ring welds; load sharing needs FEA |
| 5 Full stressed skin | 5 mm shell, 4 mm skirts, PL6 deck, structural cab, bulkheads; local bolster/drag boxes | 7 | 8 / 21 (Fy 345) | 4 | shell local sigma_cr 221 MPa (kd 0.30) vs bending 7; skirt shear tau_cr 83 vs 19 MPa (FS 4.4); cab door openings + hatches NOT checkable by hand -> FEA | 2 — E/E' (stitch-welded rings/stringers, hatch doublers, Kt~3 at cut-outs) - CAFT 18-31 MPa local; needs FEA hot-spot |
Notes: options 1–2 carry the R2 values (C4 90 MPa, C4b 117/225 MPa). The global stresses in a closed Ø1,640 tube are tiny, so global strength is not the issue. The issues are getting 200 kN at Z 550 up about 1.6 m to the shell neutral axis (Z ≈ 2,140 for option 5), the cab zone with door openings and no tube, bolster point loads, engine and hydraulic access hatches, and jack points. All of these need local framing, and only FEA can check them. In option 4 the sill alone takes the drawbar aft of the cab front (171 MPa ultimate).
## 4. Mass, steel and adhesion (weight-neutral rule)
| Option | Frame steel (kg) | Body/shell steel (kg) | Loose ballast kept (kg) | Total steel incl. ballast (kg) | Loco mass (kg) | Δ vs R2 |
|---|---|---|---|---|---|---|
| 2 R2 frame + better shell | 3,815 | 2,922 | 478 | 7,215 | 16,810 | +0 |
| 3 Heavy plate frame + better shell | 4,312 | 2,922 | 0 | 7,234 | 16,829 | +19 |
| 1 R2 as drawn | 3,815 | 1,900 | 1,500 | 7,215 | 16,810 | +0 |
| 4 Hybrid thick structural shell | 3,429 | 4,313 | 0 | 7,742 | 17,337 | +527 |
| 5 Full stressed skin | 3,178 | 3,362 | 675 | 7,215 | 16,810 | +0 |
- Rule applied: any structure lighter than R2 gets ballast plates back, so the loco stays at 16.8 t. Heavier structure displaces ballast. Options 2, 3 and 5 stay weight-neutral. Option 4 overshoots by ≈ 0.5 t even with zero ballast, which pushes against the 24 kN rail wheel-load basis (R2 C14: 23.4 kN front wheel with full ballast).
- Adhesion with 4 full-size loaded coaches + stairs + tender (trailing 60,960 kg): the loco needs ≥ 11,889 kg on the drivers for a dry 2% start (μ 0.25) and ≥ 9,163 kg for a wet level start (μ 0.15). Every option is ≈ 16.8 t, all on drivers (pony deleted), so adhesion is fine.
- Caveat: the limit is the motors, not adhesion. With the 2.2 t of stairs the train is ≈ 77.8 t; a 2% start needs 31.13 kN against 31.75 kN at 350 bar (≈ 2% margin). Keep F20: start on level, or get Poclain to approve 400 bar (36.3 kN). Do not add body mass beyond R2 to 'help traction', because it uses up the rail wheel-load margin.
- Balance: in options 2 and 3 the ballast that used to sit over the front truck is partly replaced by evenly spread shell or plate mass. Re-check the front/rear truck split and the peak wheel load (≤ 24 kN) at weigh-in. The pockets stay for trim ballast.
## 5. Fabrication labor (shop hours, ASSUMED unit rates)
| Option | Cutting | Forming/rolling | Fit-up | Welding | Distortion control/straightening | Finish prep (body) | Inspection (VT/MT/UT, dims) | Machining | Total shop h |
|---|---|---|---|---|---|---|---|---|---|
| 2 R2 frame + better shell | 40 | 18 | 108 | 34 | 25 | 21 | 29 | 16 | 291 |
| 3 Heavy plate frame + better shell | 47 | 18 | 110 | 36 | 21 | 21 | 28 | 20 | 301 |
| 1 R2 as drawn | 42 | 25 | 112 | 57 | 54 | 36 | 32 | 16 | 374 |
| 4 Hybrid thick structural shell | 56 | 40 | 118 | 53 | 34 | 27 | 59 | 24 | 411 |
| 5 Full stressed skin | 76 | 56 | 159 | 136 | 109 | 58 | 95 | 28 | 717 |
Unit rates (ASSUMED, for the PE/CWF to correct): CNC plate part 0.4 h (heavy 0.6), HSS saw/cope 0.4 h; roll thin can 3 h + pre-bend 1 h; fit light 0.5 h / heavy 0.9 h / skin panel 2 h; fillet welds at 1.4 kg/h effective deposition (min 0.12 h/m); thin stitch welds 0.35 h/m; thin CJP seams 0.8 h/m; VT 0.05 h/m, MT/UT 0.5 h/m on critical joints; straightening 1.5 h/m² on structural thin skin vs 0.2–0.8 h/m² cosmetic. Benchmark: 290–720 h for 6.5–8.5 t of fabricated steel is ≈ 40–110 h/t, above structural-steel norms (15–45 h/t) as expected for vehicle work with a show finish. Option 4 is re-estimated with in-house rolling (5 h per can + pre-bend) and boiler-shop CJP seams at 0.9 h/m. CWF's own takeoff (sent 27 Oct) should replace these numbers.
## 6. Engineering, PE, FEA and County QA effort (hours, range)
| Option | Design & drawings | FEA | PE review & stamp (K2, Jared Krupa) | County / QA-agency audit & records | Testing | Total (mid) | Approvability |
|---|---|---|---|---|---|---|---|
| 2 R2 frame + better shell | 38–60 | 0–8 | 32–54 | 30–45 | 0–0 | 100–167 (134) | Easy: R2 calcs + ring/fastener check |
| 3 Heavy plate frame + better shell | 50–80 | 8–16 | 30–50 | 25–40 | 0–0 | 113–186 (150) | Easy: plain beam + plate, hand calcs; small drag-box FEA optional |
| 1 R2 as drawn | 30–50 | 0–8 | 30–50 | 30–45 | 0–0 | 90–153 (122) | Easy: hand calcs done (R2 C4/C5/C8) |
| 4 Hybrid thick structural shell | 120–180 | 70–110 | 60–100 | 50–80 | 10–20 | 310–490 (400) | Medium: shared load path sill/shell needs FEA and shear-connector design |
| 5 Full stressed skin | 200–300 | 150–220 | 100–160 | 80–120 | 30–50 | 560–850 (705) | Hard: FEA incl. buckling, hatch/cut-out and fatigue hot-spot; likely proof-load test |
Stamp scope: options 1–3 are a conventional welded frame, so ordinary structural practice applies (beam + plate, D1.1 prequalified WPS, MT/UT on drag box and bolsters). Option 5 is a semi-monocoque rail-vehicle body: the PE would need shell buckling, cut-out and fatigue hot-spot work, possibly a rail-vehicle specialist, and likely a strain-gauged proof load. That is also more County QA records (Ch. 22.16.150 materials/construction, 22.16.160 QA program, 22.16.170 installation inspections). The 3 mm sheet sits at the D1.1 lower limit (1/8 in); anything thinner falls under AWS D1.3.
## 7. Appearance (owner criterion)
| Option | Look score (1–5) | Why |
|---|---|---|
| 2 R2 frame + better shell | 4.5 | 4.8 mm skin, no welds on the visible face (bolted/riv-nut to CNC rings); true round, lap bands can read as boiler bands |
| 3 Heavy plate frame + better shell | 5 | Same clean shell as 2, plus real-looking plate frames under the running boards |
| 1 R2 as drawn | 2 | 3 mm skin welded to HSS hoops: oil-canning and weld show-through (dimples) likely; flat 3 mm cab panels drum |
| 4 Hybrid thick structural shell | 4 | 10 mm shell very true, no oil-canning; seams need grinding; structural cab gets welded doublers that show |
| 5 Full stressed skin | 2 | 5 mm skin stitch-welded to 13 rings + 8 stringers: 'hungry-horse' ripple, hatch doublers, straightening marks |
- Cab: use 4.8 mm flat panels, or 3 mm with formed beads and bonded (not welded) stiffeners, to avoid drumming and show-through. Smokebox: a separate 4.8 mm rolled can with a CNC-cut flat front plate and a bolted door ring.
## 8. Shell formability, plate availability and material (owner criterion; R2 shell Ø1,640)
| Plate | R/t at Ø1,640 | Outer-fibre strain Ø1,640 / Ø1,100 | Shell mass 7.4 m (kg) | Residual flat spot after pre-bend (≈) | Who can roll it (TYPICAL — confirm CWF) | Use |
|---|---|---|---|---|---|---|
| 3.0 mm (10 ga / 3 mm sheet) | 273 | 0.18% / 0.27% | 898 | 6 mm | CWF in-house; 1.2–1.5 m wide sheets → 2 long seams per can or coil-cut blanks | R2 as drawn: oil-cans, show-through |
| 4.8 mm (3/16 in) | 171 | 0.29% / 0.43% | 1,437 | 10 mm | CWF in-house (boiler shop, owner 27 Oct); routine; pre-bend ends | RECOMMENDED cosmetic shell (options 2, 3) |
| 6.0 mm (1/4 in) | 137 | 0.36% / 0.54% | 1,796 | 12 mm | CWF in-house; routine | Alternative cosmetic shell (+360 kg) |
| 10.0 mm (3/8 in) | 82 | 0.61% / 0.90% | 2,993 | 15 mm | CWF in-house (boiler-shell work); pre-bend essential; crane handling ~1 t cans | Option 4 structural shell |
| 12.0 mm (1/2 in) | 68 | 0.73% / 1.08% | 3,592 | 18 mm | CWF in-house (boiler-shell range); ~1.2 t cans | Over mass budget |
| 20.0 mm (3/4 in) | 41 | 1.2% / 1.79% | 5,986 | 30 mm | CWF boiler shop probably; confirm max thickness × width at Ø1,640 (AWAIT CWF) | Far over mass budget (≈ 6 t shell) |
| 25.0 mm (1 in) | 33 | 1.5% / 2.22% | 7,482 | 38 mm | Confirm with CWF (max roll capacity AWAIT) | Far over mass budget (≈ 7.5 t shell) |
- Minimum bend radius is not the constraint. Cold-rolling strain is ≤ 1.5% for every thickness at Ø1,640 and ≤ 2.2% at Ø1,100, well under the ~5% level where reference practice (e.g. ASME UCS-79) starts to ask for heat treatment. What limits it is roll-machine capacity (thickness × width at that diameter), pre-bending the ends (without it, a flat of roughly half the roll centre distance stays at the seam) and crane handling. With CWF's in-house boiler-shop rolls, 10–12 mm shells are no longer a sourcing problem. A thick shell is now limited by mass (it eats the ballast and the 24 kN wheel-load margin) and by engineering effort, not by rolling. CWF's boiler work also brings strength in rolled-seam fit-up and pressure-quality CJP welding with routine UT/RT. That benefits the 4.8 mm cosmetic shell too: true roundness, invisible ground seams.
- Mill and stock sizes (TYPICAL service-centre stock; confirm with PDM Steel, AWAIT): plate 3/16 in and up in 72/96/120 in widths × 240/288/480 in lengths, A36 and A572-50; 10 ga sheet 48/60 in × 96/120/144 in. The Ø1,640 circumference is 5,152 mm (203 in), so 96 × 240 in plate gives one 2.44 m can with one longitudinal seam. Three cans plus a smokebox can cover the 7.4 m hood. Lap the joints between cans under a boiler band so the visible face has no circumferential weld.
- Material: total steel incl. ballast is the same for options 1, 2, 3 and 5 (≈ 7.2 t) because of the weight-neutral rule; option 4 ≈ 7.7 t. What changes is the form: cheap flat ballast plate becomes useful shell or frame plate in options 2 and 3. No outside rolling package in any option (CWF rolls in-house). Dollar figures are on the owner's private Costs Page only.
## 9. All-in ranking (labor + engineering; no dollars)
| Rank | Option | Shop h | Eng/PE/QA h (mid) | All-in h | Relative | Look | Simplicity (1–5) | Approvability |
|---|---|---|---|---|---|---|---|---|
| 1 | 2 R2 HSS frame + 4.8 mm bolted cosmetic shell | 291 | 134 | 425 | 1.00× | 4.5 | 5 | Easy |
| 2 | 3 Heavy plate frame + 4.8 mm bolted cosmetic shell | 301 | 150 | 451 | 1.06× | 5 | 5 | Easy |
| 3 | 1 R2 as drawn (HSS frame + 3 mm welded cosmetic body) | 374 | 122 | 496 | 1.17× | 2 | 4 | Easy |
| 4 | 4 Hybrid: light sill + 10 mm structural rolled shell | 411 | 400 | 811 | 1.91× | 4 | 3 | Medium |
| 5 | 5 Full thin stressed skin (5 mm) | 717 | 705 | 1422 | 3.35× | 2 | 1 | Hard |
Accuracy: ±25% on hours. Options 2 and 3 are a tie within that band. Options 4 and 5 are clearly worse.
## 9a. Does a thick rolled structural shell now win? (CWF rolls in-house)
- No. Option 4 best case: shop hours −25% and engineering at the low end gives ≈ 618 h. Option 2 worst case: shop +25% and engineering at the high end gives ≈ 531 h. The ranges do not overlap. Most of option 4's penalty is engineering (FEA of the shared sill/shell load path, shear connection, stamp scope, QA), which in-house rolling does not change. A sill or frame is still needed for the drawbar, bolsters and cab zone.
- 12 mm or thicker structural shells are over the 16.8 t mass budget before ballast is even considered (shell alone 3.6 t at 12 mm, 6–7.5 t at 20–25 mm). They would need a heavier rail basis.
- What CWF's rolling does open up: a thicker COSMETIC shell (6 mm instead of 4.8 mm, +360 kg, offset by ballast) for an even crisper look, at about the same shop hours. This is an option for the owner, not a structural change.
## 10. Fabrication, approval and life-cycle notes
- CWF: options 2 and 3 are ordinary flat-position plate and HSS work under D1.1 prequalified WPSs. The shell is rolled, its seams are butt-welded in the flat on a bench, then it is bolted on. No thin-skin distortion sequence. The shell comes off in sections for engine, hydraulic and tank access, and for repair. No structural cut-outs need reinforcing.
- Inspection: 100% VT; MT on bolster, drag-box and drawbar-pocket welds; UT on any CJP in ≥ 12 mm; dimensional survey of centre-plate spacing and drawbar height (550 ± 10).
- Corrosion and repair: options 2 and 3 have open frames and a removable shell, so everything can be painted and inspected. Options 4 and 5 have closed shells and skirts with interior welds that can't be seen, need drain holes and interior coating, and a crack in a stressed skin is a structural repair needing PE sign-off.
- Owner's 'bigger body': the R2-size body is kept in every option. Only the frame/body split changes.
## 11. Tender — per the owner's plan LT45.1 (engine goes in the tender)
- The tender is already developed in the owner's plans: LT43.1 (insulated coal-style tender), LT44 (frame and six service connections) and LT45.1 of 25 Oct 2026 (two-engine layout). Sources: tender-lt45.html, tender-lt45-engineering.html, assets/tender-lt45/basis.json. R2 now uses that plan as its tender (model rev T1), not a fresh design.
- LT45.1 geometry: pins 0 / 5,000 at Z 550, trucks at 1,200 / 3,800, body X 400–4,600 × Y ±1,300, deck Z 1,100, flat roof Z 2,360 plus a coal-effect cover, 6 mm skin + 50 mm lining, giving a 1,204 mm clear bay. The AIE Kubota V3307 with radiator and H1P045 pump (1,250 × 687 × 1,028; 809 handedness width) sits on the left. A separate Kubota-powered 35 kW generator space (1,700 × 800 × 1,000 on 80 mm mounts) sits on the right, with the engine-driven brake compressor provision ahead of it. The 150 L shared fuel tank and AC panel sit aft of the X 2,800 partition; the hydraulic reservoir and side-mounted oil cooler are aft on the left. A 600 mm access strip runs between.
- F18 (power unit 676 mm too tall) was an R2 error. It came from LT44's check of a stock Hydra-Tech HT150DQV skid (1,880 mm tall), which LT45.1 dropped. Under LT45.1 the engine and generator envelope both fit the 1,204 mm bay.
- Still open (from LT45.1): the 35 kW generator model, mass and fit (gaps 124 / 94 / 25 mm); the hot-humid coach HVAC case (−4.7 kW at 35 kW); 7.6 kW left on the traction engine for auxiliaries, including the compressor; AIE Rev B vs Rev C GA and mounts; cooling, exhaust and removal paths; complete tender mass.
- Traction effect of tender mass: the R2 tender was 8.16 t. Every +1 t of train adds ≈ 0.40 kN to the 2% start demand. The 350 bar margin is only 0.62 kN, so a tender heavier than ≈ 9.7 t uses it up and 400 bar (Poclain approval) becomes necessary for 2% starts. Adhesion stays fine: the minimum loco rises only ≈ 0.2 t per +1 t of tender.
- The loco body recommendation (option 2) is independent of the tender.
## 12. Recommendation
- Adopt option 2: R2 HSS frame unchanged (C4/C5/C8 stand), with a 4.8 mm A36 rolled hood/smokebox shell and 4.8 mm cab panels bolted to PL10 flat CNC rings and frames. Ballast plates drop from 1.5 t to ≈ 0.5 t to hold 16.8 t. Keep option 3 (PL20×500 plate frames) as the CWF-preference alternate. Do not pursue a load-bearing (stressed-skin or structural-shell) body.
- Next steps: CWF (rolls in-house) to say which of options 2 or 3 it prefers and confirm max roll thickness × width (AWAIT CWF); PDM Steel for stock sizes (AWAIT); PE (K2) to accept the hand-calc scope; re-weigh/balance check at assembly. Nothing to be ordered until the PE approves.
## Files
- calcs/structural_body_study.py (checks, mass, hours) → structural_body_study.json; structural_body_report.py → structural_body_section.png; this memo .md/.pdf.

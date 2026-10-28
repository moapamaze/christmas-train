# PF-CT R2 Tender — Weight-reduction study TW-1
Pulsipher Farms Christmas Train — preliminary, not for construction until PE stamped. Study note TW-1, 27 Oct 2026. Basis: rev T1 tender (owner plan LT45.1), CAD mass report, owner tender ledger (Project Plan Page), tender-lt45/basis.json. Masses are screening estimates; ASSUMED items are marked. No supplier data is invented.
## 1. Answer in plain words
- Yes. Built up honestly, the tender as drawn is about 9,315 kg, not 8,160 kg: the trucks are lighter than the ledger allowed, but the 6 mm skin, PL10 deck, deck outriggers and the 3 mm coal cover are heavier. At that mass the 2% start margin at 350 bar is only 0.15 kN.
- A package of seven low-labor changes saves about 1,490 kg and gets the tender to about 7,825 kg (8,075 kg if the lighter generator does not happen). That is at or below the 8,160 kg ledger and 1.6–1.9 t under the ≈9.7 t limit where 400 bar would be needed.
- New 2% start margin at 350 bar: 0.75 kN (package) / 0.65 kN (without the genset saving), against 0.61 kN at the 8,160 kg ledger and 0.15 kN as drawn.
- Top moves: (1) 10 ga steel skin on posts instead of 6 mm plate; (2) 6 mm tread-plate deck on cross-bearers instead of PL10 + outriggers; (3) an open-skid 35 kW genset, because the insulated tender already is the sound enclosure; (4) lighter coal cover, fish-belly bolsters and lighter lining. The look stays: black with gold trim, the coal-effect cover stays, and the bolted skin reads as riveted tender plate.
- Moving equipment to the locomotive does not help the 2% start: the train weighs the same and the motors, not adhesion, are the limit. Each 1 t of loco ballast left out adds 0.40 kN; loco 15.8 t is well above the 11.9 t dry-2% adhesion minimum.
## 2. Mass breakdown (rev T1 tender, as drawn, built up)
- Wheel modeling fix: the CAD models each Ø600 wheel as a solid disc (332 kg). A plate-web wheel (rim 50 deep, web 25, hub Ø200, ASSUMED section) is ≈ 144 kg. Eight wheels: 2,652 → 1,152 kg. The same overstatement exists on the coach and loco CAD wheels (CAD mass only; the ledgers are not affected).
| Group | Item | kg | Basis |
|---|---|---|---|
| Trucks (2) | Wheels 8 × Ø600 plate-web (true section) | 1,152 | Rim 50 deep, web 25, hub Ø200 (ASSUMED section); CAD solid disc was 331 kg each, true ≈ 144 kg |
| Trucks (2) | Axles 4 × Ø110 × 1,400 | 418 | CAD |
| Trucks (2) | Truck frames, axleboxes, centre plates | 773 | CAD (C-303 coach truck) |
| Trucks (2) | Springs, brake discs, calipers, spring-brake chambers | 300 | ASSUMED 150 kg per truck (not modeled) |
| Frame + deck | Main rails, crossmembers, bolster boxes | 868 | CAD rev T1 |
| Frame + deck | PF-DB drop boxes and pockets, both ends | 339 | CAD rev T1 |
| Frame + deck | Deck PL10, 4.4 × 2.6 m | 898 | CAD rev T1 |
| Frame + deck | Outriggers to carry the deck edge and walls (5 × C6x8.2 full width) | 159 | ASSUMED - not in the model (deck overhangs the rails by 600 mm) |
| Body | Skin 6 mm steel, 28.1 m² (sides, ends, roof) | 1,321 | LT45.1 6 mm skin |
| Body | Skin posts, roof bows, door frames | 150 | ASSUMED |
| Body | Lining 50 mm mineral wool 100 kg/m³ + perforated steel liner 0.8 mm + facing | 275 | ASSUMED densities |
| Body | Coal-effect cover 3 mm steel, 10.8 m² + supports | 293 | ASSUMED 3 mm formed steel |
| Body | Doors, hinges, latches, handles, paint | 100 | ASSUMED |
| Equipment (dry) | AIE V3307 package + radiator + H1P045 | 610 | LT45.1 relocated 959.1 less tanks/cooler |
| Equipment (dry) | Fuel tank + hydraulic reservoir (empty) | 90 | basis.json 40 + 50 |
| Equipment (dry) | Hydraulic oil cooler | 55 | basis.json |
| Equipment (dry) | 35 kW generator set | 900 | Owner ledger ASSUMED (model not chosen) |
| Equipment (dry) | Compressor, coach AC panel, batteries | 160 | Owner ledger ASSUMED |
| Equipment (dry) | Mounts, exhaust + shields, ducts, hoses, cabling | 250 | ASSUMED - not in owner ledger |
| Fuel + fluids | Diesel 150 L | 126 | basis.json (0.84 kg/L) |
| Fuel + fluids | Hydraulic oil in reservoir | 78 | basis.json |

| Group | kg |
|---|---|
| Trucks (2) | 2,643 |
| Frame + deck | 2,263 |
| Body | 2,140 |
| Equipment (dry) | 2,065 |
| Fuel + fluids | 204 |
| Total | 9,315 |
- Against the owner's ledger (8,160 kg): trucks 2,643 vs 4,000 allowed (lighter); frame + body 4,403 vs 2,141 allowed (much heavier); equipment and fluids about 2,270 vs 2,019 (mounts/exhaust allowance added).
## 3. Candidate savings
| ID | Move | kg saved | Shop h | Eng h | Approvability | Look | Recommended |
|---|---|---|---|---|---|---|---|
| S1 | Skin 6 mm → 10 ga (3.4 mm) steel, bolted/plug-welded to posts at 500 mm (riveted-plate look) | 508 | +12 | +4 | Easy - non-structural skin; panel check for wind and oil-canning | 4/5 - posts at 500 + round-head bolts read as riveted tender plate; continuous welding would oil-can (2/5) | YES |
| S2 | Skin 6 mm → 8 ga (4.2 mm) steel (alternative to S1) | 371 | +6 | +3 | Easy | 4.5/5 | no |
| S3 | Skin → 4 mm aluminium 5052 (alternative to S1) | 1,018 | +40 | +12 | Harder - poor fire barrier around two diesels and exhaust; galvanic isolation; not CWF's usual material | 4/5 | no |
| D1 | Deck PL10 → 6 mm tread plate on 7 full-width C6 cross-bearers (replaces PL10 + outriggers) | 296 | +10 | +3 | Easy - equipment mounts land on rails and cross-bearers; spill floor stays steel and sealed | n/a (inside) | YES |
| G1 | Open-skid 35 kW genset (no sound enclosure or base tank) - the insulated tender is the enclosure; target ≤ 650 kg | 250 | +6 | +8 | AWAIT supplier data (mass, cooling air, open-frame rating); fuel from the shared tank | n/a | YES |
| G2 | Smaller generator (≈25 kW) by cutting coach heat/cool load | 200 | +0 | +6 | Not recommended - hot-humid case is already 4.7 kW short at 35 kW | n/a | no |
| K1 | Coal-effect cover 3 mm → 1.5 mm (16 ga) formed steel, textured coating | 127 | +6 | +1 | Easy - steel stays fire-safe near the exhaust | 5/5 - same shape, black with gold edge trim | YES |
| K2 | Coal-effect cover in fire-retardant FRP (alternative to K1) | 167 | +4 | +3 | OK if FR resin and kept clear of the exhaust outlet | 5/5 | no |
| K3 | Delete the coal-effect cover | 293 | -20 | +0 | Easy | Loses the owner's look - not recommended | no |
| B1 | Bolster boxes → fish-belly PL10 webs (deep only at the centre plate), lightening holes in webs | 140 | +4 | +4 | Easy - centre-plate load ≈44 kN ×2 dynamic gives ~12 MPa in the present box; coupler path untouched | n/a (under frame) | YES |
| L1 | Lining: 64 kg/m³ mineral wool + 0.8 mm perforated aluminium inner liner (steel liner kept by the exhaust) | 121 | +0 | +1 | Easy - wool stays non-combustible | n/a (inside) | YES |
| F1 | Run-day fuel: carry 100 L (tank 120 L) instead of 150 L | 48 | +0 | +1 | Easy - est. use ≈ 8.6 L/h both engines (ASSUMED), so 100 L ≈ 11 h | n/a | YES |
| W1 | Lightening holes in the wheel webs | 80 | +8 | +6 | Harder - wheel fatigue; changes the coach wheel too | n/a | no |
| W2 | Tender-only Ø460 trucks | 400 | +40 | +30 | Harder - new truck design and approval; loses one-spare-fits-all | 3/5 | no |
| R1 | Lighter main rails / lightening holes in rails or drop boxes | 60 | +0 | +10 | Not worth it - rails carry the 200 kN buff with the 286 mm offset moment + fatigue; holes in HSS add fatigue and corrosion details | n/a | no |
| M1 | Move tender equipment to the locomotive | 0 | +0 | +0 | No gain at 2%: train mass is unchanged and the motors, not adhesion, are the limit. Only helps if it replaces dead ballast kg-for-kg | n/a | no |
## 4. Recommended package
- S1: Skin 6 mm → 10 ga (3.4 mm) steel, bolted/plug-welded to posts at 500 mm (riveted-plate look) — 508 kg
- D1: Deck PL10 → 6 mm tread plate on 7 full-width C6 cross-bearers (replaces PL10 + outriggers) — 296 kg
- G1: Open-skid 35 kW genset (no sound enclosure or base tank) - the insulated tender is the enclosure; target ≤ 650 kg — 250 kg
- K1: Coal-effect cover 3 mm → 1.5 mm (16 ga) formed steel, textured coating — 127 kg
- B1: Bolster boxes → fish-belly PL10 webs (deep only at the centre plate), lightening holes in webs — 140 kg
- L1: Lining: 64 kg/m³ mineral wool + 0.8 mm perforated aluminium inner liner (steel liner kept by the exhaust) — 121 kg
- F1: Run-day fuel: carry 100 L (tank 120 L) instead of 150 L — 48 kg
- Total 1,490 kg → tender ≈ 7,825 kg (8,075 kg without G1). Labor: about +38 shop h and +22 engineering h in total; all steel work CWF already does (plate, forming, CNC cutting).
- Not touched: main rails HSS10x4x1/4, crossmembers at the ends, PF-DB drop boxes and pockets. So the 200 kN buff check (C5, C5w) and the fatigue details at the coupler are unchanged.
- Not recommended: aluminium skin (fire barrier around two diesels, galvanic isolation, not CWF's material); deleting the cover (loses the look); tender-only small-wheel trucks (new design and approval, loses the common spare); lighter rails or holes in rails (coupler load path and fatigue); a smaller generator (hot-humid case is already short).
## 5. Checks to do when detailing
- Skin: 10 ga panels between posts at 500 for wind (C11 pressure) and oil-canning; bolt or plug-weld, no continuous seam welds on the sides.
- Deck: 6 mm tread plate between cross-bearers at ≤ 650 for foot traffic and spill containment; all equipment mounts land on rails or cross-bearers.
- Bolsters: fish-belly web check at the centre plate (≈ 44 kN with ×2 dynamic) and side bearers.
- Genset G1: AWAIT supplier mass, open-frame continuous rating, cooling air and service sides. Fuel 100 L: confirm both engines' real consumption on a run day.
- Truck capacity: at ≈ 7.8–8.1 t the tender puts ≈ 4 t on each truck, below the loaded coach (≈ 6.6 t per truck), so approving the coach truck covers the tender.
## 6. Files
- calcs/tender_weight_study.py → tender_weight_study.json; this memo tender_weight_study.md / .pdf; calc rows C13t/C13u/C13v in calcs.json and PF-CT_R2_calc_notes.
## 7. Rev T2 — owner-approved subset, now in the model (27 Oct 2026)
- Owner approved S1 (10 ga skin on posts at ≤500, bolted / plug-welded), D1 (6 mm tread-plate deck on 7 C6 cross-bearers), K1 (1.5 mm coal-effect cover) and B1 (fish-belly bolsters). Not adopted: G1 open-skid genset (enclosed genset assumption kept), F1 (150 L fuel kept), L1 (standard 50 mm lining kept).
- Built into build/model.py as tender rev T2 and rebuilt in CAD. The coach / tender Ø600 wheels are now modeled to the true section (≈144 kg each). Deck top is Z1,096 (tread plate on the rail tops; LT45.1 nominal 1,100). Posts come out at 460 pitch on the sides and 498 on the ends (≤500).
- Modeled build-up: tender 8,304 kg (study estimate for this subset 8,244 kg; modeled posts and roof bows are heavier than the post allowance, the deck and bolsters are lighter). Saving 1,011 kg from 9,315 kg.
- 2% start margin at 350 bar: 0.56 kN (was 0.15 kN as drawn at rev T1; 0.61 kN at the 8,160 kg ledger). 1.39 t below the ≈9.7 t limit. Calc row C13u.
| Group | kg |
|---|---|
| Trucks (2) | 2,643 |
| Frame + deck | 1,773 |
| Body | 1,618 |
| Equipment (dry) | 2,065 |
| Fuel + fluids | 204 |
| Total | 8,304 |

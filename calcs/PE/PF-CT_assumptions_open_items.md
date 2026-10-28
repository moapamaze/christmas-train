# PF-CT Assumptions and Open Items — rev L4.2

Separates (A) what the PE must decide or verify, (B) what waits on supplier data, (C) owner decisions, and (D) what is finished in this package.

## A PE must decide or verify
| # | Item | Our assumption | Where |
|---|---|---|---|
| A1 | Applicability of ASTM F2291 load cases vs IBC/other for patron areas | F2291 + IBC 1607 reference values | §1, §9 |
| A2 | Equipment restraint factors 3 g / 2 g / 1 g and seat anchorage 3 g | ASSUMED | §1, §7, §9 |
| A3 | Drawgear 70 kN service / 200 kN ultimate basis | ASSUMED | §6 |
| A4 | Brake criteria: tare 12% ratio, ≤ 20 m emergency stop on 2% down, 1.5 s reaction | ASSUMED | §5 |
| A5 | Adhesion μ 0.25 dry / 0.15 wet / 0.25 sanded | rail practice | §4, §5 |
| A6 | Governed 6 mph maximum operating speed (OWNER-SELECTED) and the 7 mph overspeed trip setting | 6 mph hard limit via the sealed 42 cc pump stroke stop + tamper-sealed 2,600 rpm engine limit (L4.2); independent 2-channel relay trip 7 mph | §0, §4, §5 |
| A7 | Roller chain final drive in passenger rail traction (ANSI 120-2 in oil bath) - acceptance, inspection interval, guarding | SF 7.9 on ultimate at HPRV; util 0.63 of maker allowable; sag 17-20 mm, replace at 2% stretch | §4 D2 |
| A8 | Axle fatigue: full EN 13103 / AAR check of the Ø150 pressed sprocket seat (no hardening credit) | 34CrNiMo6/EA4T, n 1.64 heaviest axle; 110 MPa press-fit screen | §3 |
| A9 | Parked wind speed and tie-down anchors (site ASCE 7 value, geotech) | 100 mph | §11 |
| A10 | Restraint classification per F2291 (no individual restraints) | ≤ 0.11 g | §9 |
| A11 | Accessible coach: ADA §234 / wheelchair securement | not designed here | §9 |
| A12 | Fire/smoke performance of floor, lining, seats (NFPA 130 practice?) | reference only | §9 |
| A13 | Electrical design review and inspection (NEC 522/525) | per §10 | §10 |
| A14 | Rail basis 26 kN wheel load and owner track drawings (rail, ties, ballast) | ASCE 40 new, ties 6×8×6 ft @ 22.5 in, ≥ 10 in ballast | §12 |
| A15 | Curving derailment criterion: Nadal 70°/μ 0.3 = 1.34 quasi-static incl. curving guidance + drawbar lateral (route check RT1) | gauge-face lubrication on R < 100 | §6 K1-a, §12 |
| A16 | Drawgear (Stress Bot R3): renew at 1.0 mm TOTAL play; k ≥ 20 kN/mm and ≤ 100 kN/mm for R80 (≤ 25 if route E); loco service brake ≤ 0.69 m/s²; pony swing stops ±120 mm | draft-gear supplier k curve AWAIT | §6 K1-a3/K1-h, §5 B1-o, §12 K2-l |
| A17 | Pony truck loading (actual 2.9 kN/wheel): sprung pony with own 1.25 t ballast vs body spring (body spring 10-15 kN over-loads rear truck, K2-m) | own-ballast sprung pony; swing stops ±120 mm (Stress Bot R3; R80 swing 89.5 mm) | §12 K2-l/m |
| A18 | Decorative cylinders Ø380 vs the lead-truck wheel (K2-h) | moved to Y±790 in rev L4 (37 mm Alt A, 25 mm R50) | §12 |
| A19 | Traction control without a flow divider (L4.1): electronic slip control + pony ground-speed reference; TE capped at equal torque; dry/sanded 2% margin 1.10; wet unsanded needs sand (also at the worst start points of route Alts D/E/F) | PE to review the control logic and the functional track test; PLUS+1 software by Danfoss/integrator | §4 D1-c/m/m2 |
| A20 | Uncompensated 2% + R100 start (D1-a2/s): margin 0.98 without the divider credit | outside basis - route curves compensated; 4 plates would restore 1.00 | §4 |
| A21 | Mass re-baseline: LT43 relocation (~1.0 t) double-counted in the 17.667 t loco; corrected ~16.66 t, lead 2.9 kN/wheel, weakest driver axle ~25 kN → equal-torque start on 2% NG unless axle loads are levelled / per-motor torque control (route check RT1 loco_check) | L4 basis: corrected 16.66 t base + L4 drive + barrel + bell + L-107 P1-L + cab C1 + FT-1 + 1,056 kg front ballast + pony ballast = 19.82 t | §0, §4 |
| A22 | L-107 running boards (Loco Bot): P1-L aluminium deck +36.5 kg net vs the 1,248 kg L3 deck already in the base - INCLUDED; cab L-111 C1 813.9 kg replaces the 1,000 kg allowance | RESOLVED in the L4 mass basis | §0, §12 |
| A23 | Barrel 2,135 kg (93 % on the front truck) and bell 8 in at X2800 (40 kg) | included | §0 |
| A24 | L-107 blind-bolt holes (Loco Bot, L4.1): rail outer webs RELEASED - B1 holes X480/600 (28 mm from the X452 sill weld toe), 28 HB16 total; SD-1 bolster HB16 at Y±90 with the cap re-cut to Y±50; rear end-sill: NO holes - SD-2 held down by 4 PL16 clamp plates under the sill flange | CLOSED (L41-s1/s2) | §1 |
| A25 | Charge pump sizing for 4 × MS05 HighFlow + T04 release + shift (L4.1: no flow divider) (the Danfoss 10 % rule gives ~193 cc - not meaningful for LSHT motors); charge filter added | OPEN - Danfoss/Poclain | §4 |
| A26 | Chain-case floating seal plate at the axle (OI-L4-5): ±25 vertical (bump stops ±22) / ±1 lateral, ride-out checked. OI-L4-6 (45T replacement) RESOLVED: split rim ring with bolting web on the Ø350 hub flange (8.8 fitted bolts, 219 N·m), replaced in place | CLOSED (L4.1) | §4, L-106 |
| A27 | K-401 lower outline (Steering 14b): >= 150 mm above top of rail between the rails, >= 100 mm outside; basis level track and vertical curves R >= 500 m, new wheels, static | all vehicles PASS (governing 196 mm, tender/coach truck transoms); wheel-wear + spring-deflection allowance for PE | §12 K2-lo, K-401 |
| A28 | Fouling point / clearance marks (Rail Bot): 3.6 m track centres (2 x 1,696 + 200), 34.0 m from the points of each #8; working layout F (R80, level) - OWNER PENDING | verified 33.99 m; R80 adds ~37 mm/side, inside the 200 mm allowance | §12 K2-fp, K-401 |
| A29 | Shore transformer assembly under the tender deck vs X2500 HSS10x4 crossmember (K2-xf) | CLOSED (Tender Bot TB-3.8/3.9): cradle dropped 50 mm - 25 mm at the isolator stop, 100 mm to K-401 | §7 E-cg, §12 K2-xf, T-201 |
| A30 | Low traction pin per powered truck (L4.1, h 0.65 m): pin/housing detail and 55 kg mass ASSUMED - PE to verify pin bending (~131 MPa est. vs 393) and the transom housing; reverse pull cap + ≤ 1.20 % (L4.2) reverse-start rule | PE verify | §6, D4-wt/wr |
| A31 | Loco brake release air (L4.1 s8/9): line lengths and fittings (Loco Bot) to confirm the 3/4 in trunk C ≥ 8 and 1/2 in branches C ≥ 2.0; relay/regulator C values from WABCO/Norgren data; release-time test ≤ 4.0 s at MR cut-in and -10 °C | Loco Bot data / commissioning | §6, L41-b1/b2 |
| A32 | Worn-flange clearance (L4.1 s7): flange-height limit 28 mm / re-profile ≤ 27 (L4.2 FINAL; L4.1 30.0 withdrawn) vs ASCE 40 joint-bolt heads ~32.5 mm below TOR (3/4 in track bolts ASSUMED) and frog/guard flangeway depth ≥ 36 mm - confirm on the owner track drawings | PE / track verify | §6, L41-w4 |
| A33 | T04 release circuit (L4.1 s7): T04 release volume (0.10 L/motor), full-release 15 bar and max 30 bar ASSUMED - re-size the Ø2.4 choke and the 6.0 L / 1.0 L accumulators on Poclain data; timed commissioning test | Poclain data (HELD) / commissioning | §6, L41-t1/t2 |
| A34 | T04 choke and pump neutral ramp (L4.1): run-in 23.7 kN needs T04 delay ≥ 1.0 s + rise ≥ 2.0 s and pump ramp ≥ 3 s - verify by a timed commissioning test | PE verify / commissioning | §6, D4-ri |
| A35 | L4.2 coach brake-release indication dual-channel per Electro E3.6h (J-CC 22/23 + 34/35, Pilz B0 test pulses, PL d Cat 3, daily force-guided relay test): PE to confirm the fault exclusion for the single pressure element per switch and the test-pulse loop length over the trainline | PE confirm | §6a, L42-ar |
| A36 | L4.2 strength basis 430 bar (HPRV 380 + spike): PE to accept the basis and KA 1.5 on top; 15T made to order in 4140 Q&T | PE decide | §6a, D2-h |
| A37 | L4.2 chain breaking strength: SPEC ≥ 326 kN certified at the 430 bar strength basis; standard Tsubaki RS120-2 296 kN fails by 10 % (passes at HPRV 380) - PE may accept SF 8.41 on ultimate or require a higher-strength 120-2 | PE decide / vendor batch | D4-mb, D4-mb2 |
| A38 | L4.2 reverse full-train start limit 1.20 % (28.9 kN reverse pull cap with 1.10) - operating rule on every file; track is level | PE verify | D4-wr, L42-gb |
| A39 | L4.2 K2-a 25.89 kN of record relies on NB-1 nose ballast 59.8 kg at X450 and the PLUS+1 forward TE command limit 33.0 kN - verify by weighing the loco (wheel scales) before service | commissioning HOLD POINT | L42-k2 |
| A40 | L4.2 centre-plate pad stiffness (3.0 MN/m) and PTFE μ ≤ 0.08 ASSUMED; spring full-apply pressure 0.5 bar g ASSUMED (QEV option A check) | PE verify / supplier | L42-cp, L42-qa |
| A41 | L4.2 T04: charge low-idle 21 bar and T04 full release 15 bar ASSUMED - timed commissioning test of release (≤ 8 s) and burst behaviour | commissioning | L42-t1..t4 |
| A42 | P-103-1 motor hanger L-weld (140 + 150, 10 fillet both sides + 2 PL16 gussets) APPROVED - fatigue check pending at Loco Bot | Loco Bot / PE verify | L-103 |

## B Supplier data awaited (no values invented)
| # | Supplier | Data | Used as |
|---|---|---|---|
| B1 | Poclain Hydraulics Application Engineering | MS05 468/234 2C HighFlow + T04 + shaft code 5 (W55x3x17) + speed sensor model code; shaft shock rating at 2,979 N·m × 1.5; radial load at sprocket offset; starting efficiency; shift on the move; T04 release/charge flow; rail traction duty; CAD | η start 0.90 (0.80 checked); D2-c radial 32.7 vs 60 kN chart |
| B2 | Chain / sprocket maker (Tsubaki or equal) | ANSI 120-2 allowable at 15T/≤ 140 rpm, 54-link assembly + connecting link; 45T SPLIT rim ring with bolting web to the Ø350 hub flange (ring ~50 kg ASSUMED + hub 31.4 kg), hardened teeth | D2-a/b, unsprung 124 kg/axle |
| B3 | Martin Sprocket | D120B15 Type B, hardened teeth, OD 202, hub broached N55x3x17 (female) to MS05 shaft code 5 (W55x3x17 male); ≥ 58 mm engagement (Poclain spline length AWAIT) | 13.6 kg; D2-h |
| B4 | Danfoss / PLUS+1 integrator (L4.1) | Traction-control application on PLUS+1 (slip detection, destroke, auto-sand, hill-start hold) + EDC response time; 3rd speed pickup on the pony | D1-m |
| B5 | Valve suppliers (L4.1) | Tow ball valve HYDAC KHB3K DN06 class 500 bar, lockable + limit switch (L4.2; KHB3K DN25 310 bar NOT allowed on the loop); 3/2 normally-vented solenoid cartridge (HydraForce SV08/SV10-30 class); [LP-select shuttle DELETED L4.2]; 3-way reducing/relieving cartridge 20 bar (inlet ≥ 450); 6.0 L bladder + 1.0 L diaphragm accumulators; hand pump 12 cm³; guarded 3/2 manual valve; charge pressure switch 17 bar; T04 release volume per motor (Poclain) | loco_valves |
| B6 | Chain case fabricator / seal supplier | 3 mm oil-bath case, floating seal plate with lip seal at the axle hub land (±25 travel) | D2-g, OI-L4-5 |
| B7 | Oil-cooler supplier | ≥ 14 kW at 43 °C outside air, electric fan | D1-i |
| B8 | Ingersoll Rand | 2340 compressor with electric clutch, drive from V3307, 43 °C | B-601 |
| B9 | SKF/Timken / Strasburg-Uhrich | Axlebox bearing C ≥ 190 kN (L4.1: computed 186.7 governs; ≥ 169 superseded), fits, L10m review; GE100ES pivot | axlebox C_req spec row X1-b |
| B10 | Danfoss | H1P053 G1 shaft (14T 12/24) / L35 model code, AC-2 or EDC+PLUS+1 anti-stall | 35 kW anti-stall, 534 N·m G1 |
| B11 | AIE / Kubota | V3307 package GA, mounts, cooling at 43 °C, PTO for compressor; L4.1: pump-drive coupling hub 14T 12/24 on the SAE B pad (quote shows 13T) | 610 kg, 45.6 kW |
| B12 | Brake supplier (ZF/WABCO or industrial) | Spring calipers ≥ 22 kN, 2 per loco axle disc (ref. Coremo D 3.5N 24.2 kN) / ≥ 10 kN (coach), pads μ, valves, disc thickness; WABCO IR-2 971 899 152 0 data sheet (inversion curve vs Coremo release 5.1-6 bar); Knorr KE at BP 5.0 bar; ASCO 8210G035 24 VDC | clamp spec rows B1-g/h, release air B1-l |
| B13 | Spring supplier | Rubber-metal chevron primary springs 580 N/mm, 26 kN max, 170 mm | T1-d/e |
| B14 | Genset supplier | PTI-38 / DCA36: rating at 43 °C (both data sheets show 40 °C, NOT 43 °C) and UL 2200 listing (NOT shown); transient | §8; TB-3 layout approved (C7) - derate letter + listing OPEN |
| B15 | HVAC supplier | Mobile-rated heat pumps; RenewAire HE05IN selection printout (ε at 300 cfm, 43 °C), roof-pod mounting/vibration; condensate | §8 (ε 0.55 ASSUMED), §10 |
| B16 | Isolators | Engine/genset mount ratings (uplift/shear) | §7 |
| B17 | Composite floor | EI and point-load certification | R1-d |
| B18 | Hose / fitting suppliers (L4.2) | Loop hose SPEC Manuli DIAMONDSPIR H10018025 (ISO 18752-C, 560 bar WP) with code 62 / 24° S25 ends and whip restraints ≥ 420 bar WP; HYDAC KHB3K DN06-class 500 bar lockable tow ball valve (DN06 Δp curve to confirm the 2 mph tow sizing); bypass and float valves ≥ 420 bar | D1-g, §6a |
| B19 | Danfoss (L4.2) | HPRV overshoot figure - INFORMATION ONLY, not gating | §6a |
| B20 | Chain maker (L4.2) | ANSI 120-2 with a certified breaking strength ≥ 326 kN per lot | D4-mb |
| B21 | SKF / bearing supplier (L4.2) | GE120ES radial rating for the traction-pin housing | L42-p1/p2 |
| B22 | Air valve suppliers (L4.2) | 1/2 in QEV maker-certified ≥ 15 bar WP (option B); valve C ≥ 0.31 dm³/(s·bar); Crosby S-1325A / A-1342N WLL ≥ 5/8 G100 chain WLL certificate | L42-qb, L42-ar, L42-lg |
| B23 | Pad supplier (L4.2) | Laminated elastomer centre pad stiffness and PTFE slide μ | L42-cp |

## C Owner decisions open
| # | Decision | Recommendation |
|---|---|---|
| C1 | ERV + staging (keep 35 kW) vs a 45 kW genset | ERV (RenewAire HE05IN roof pod) + staging |
| C2 | Pony/leading truck retention (F06) | KEEP (owner, 28 Oct): sprung pony carrying its own ~1.25 t ballast, no lateral centering > 0.5 kN, swing stops per route radius (§12 K2-l/m) |
| C6 | Minimum radius (basis R100; Rail Bot R60; Stress Bot R100) | R100 with ≥ 10 m spirals recommended; R60/R50 only with the changes listed in calcs/track/route_check.md |
| C3 | Accept 2% hold of 2.7 mph (V3307); level runs at the 6 mph governor | accept - the route has 2% grades (descents up to ~0.5 km, see B1-j2), so the 2.7 mph hold applies on every climb |
| C5 | Governed 6 mph maximum (owner-selected 28 Oct) | DECIDED by owner - PE to confirm |
| C7 | Genset PTI-38 (699 kg) - tender layout rev TB-3 APPROVED 28 Oct (reservation X1060-2768, ≤ 1,775); rated 40 °C not 43 °C, no UL 2200 shown | PTI-38 layout approved; 43 °C derate letter and listing still OPEN before purchase |
| C8 | Accept roller-chain upkeep: check sag 17-20 mm monthly, oil level, replace the chain at 2 % stretch; 45T is a split rim ring (Source Bot rev 3), replaceable without a wheelset drop | accept (no belt per owner) |
| C9 | Front pocket ballast: smallest 75.4 kg plate multiple giving an equal-torque dry 2% start margin ≥ 1.10 | DECIDED - Steering 17 trim: 150.8 kg (2 plates, 1 per side) + BT-1 battery 68.2 kg in the Y- pocket, on the Loco Bot shell ledger rev 2 (was 1,056 kg); margin 1.10; trim at weigh-in |
| C4 | Accept sanders (visible sand boxes under running board) | accept, boxes hidden in hood |

## D Finished in this package (ready for review)
- L4 drive: no-belt option study, chain/sprocket rating, motor radial/bearing, 6 mph pump-stop governor, anti-slip/overspeed, Ø150 pressed seat (static + fatigue + press fit), motor bracket weld, case clearance, take-up without idler, unsprung mass, envelope check in the model, CAD/STEP. L3 (calcs/L3) kept as fallback, L2 as rejected.
- Traction/adhesion/power-speed tables; pump sizing vs V3307; hoses; cooler duty.
- Brakes: forces, stopping distances, parking, caliper clamp specs, thermal, buff.
- Structures: loco frame/body, trucks, coach underframe/body/roof/floor, stairs, tender structure, mounts, drawgear; wind; clearance.
- Electrical one-line sizing, HVAC shortfall closure, fastener torques, weld schedule, BOMs, drawings.
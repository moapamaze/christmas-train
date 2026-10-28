# PF-CT route vehicle/track check — RT1, 28 Oct 2026

Inputs: route_redline Alts A–D (read-only), track_structure (read-only), loco audit (read-only), Rail Bot screening, Stress Bot round 1. Vehicles: the R2/L3 model (model.py), with a 3-D kinematic sweep of every part (route_check.py / run_all.py / run_extra.py). The train is loco + tender + 3 coaches + accessible coach. Envelope K-401 half-width is 1,696 mm and fixed objects are at 2,000 mm. The design basis is unchanged: **R_min 100 m; 2 % is the GOVERNING design grade** (the track is not designed level).
Note: the redline sweeps are tangent–arc (no spirals). "With spirals" values are the steady-state curve angles, valid for spirals ≥ about 1 vehicle length (12 m). Re-sweep the final alignment with its spirals.

## 1 Pass/fail by alternative
| | A (R100, 1,677 m) | B (R45 hairpin) | C (R50) | D (R60) |
|---|---|---|---|---|
| Loco envelope (vs 1,696) | 1,583.6 ✔ | 1,715.4 ✘ | 1,695.3 (1,700+ with widening) ✘ marginal | 1,657.3 ✔ |
| Coach + 60 mm garland | 1,651.7 ✔ | 1,704.4 ✘ | 1,690.8 (1,696 at 917.5) marginal | 1,678.3 ✔ |
| Cylinders vs lead wheel (≥ 10 after play) | −0.4 ✘ (37 at Y±790) | −15.0 ✘ (22) | −13.5 ✘ (24) | −10.9 ✘ (26) |
| Loco–tender angle loco/tender (limit 32.4 / 19.2) | 13.3/10.0 ✔ | 29.4/21.3 ✘ | 26.4/19.7 ✘ tender | 22.1/16.4 ✔ |
| Coach drawbar angle | 7.3° | 15.8° | 14.3° | 12.0° |
| Lead-truck swing | 73 | 159 | 144 | 120 |
| L/V at a realistic 33 kN buff (empty coach), as drawn | 1.17 ✔ | 1.54 ✘ | 1.48 ✘ | 1.39 ✘ |
| Allowable buff at Nadal (coach / tender), as drawn | 52 / 39 kN | 23 / 18 | 25 / 19 | 30 / 22 |
| Start on 2 % incl. curves (L3 basis, adhesion 37.9) | 31.5 ✔ 1.20 | 31.5 ✔ | 31.5 ✔ (needs R50 compensation 1.33 %) | 31.5 ✔ |
| **Verdict** | **PASS with cylinder move + 10 m spirals + preloaded drawgear** | **FAIL** (R45 envelope) | **FAIL as drawn**; pass only with the R50 list below | **FAIL as drawn**; pass with the R60 list below |

## 2 Limiting numbers by radius (constant curve, sweep)
R: loco env / coach env (+garland) / loco–tender angle loco,tender / coach angle / lead swing / L/V no-spiral (coach, tender, loco) / L/V with spirals
- R100: 1,581.6 / 1,586.5 (1,646.5) / 13.0, 9.6 / 7.07 / 72 / 1.08, 1.21, 1.20 / 0.97, 1.10, 1.16
- R60: 1,655.4 / 1,614.5 (1,674.5) / 21.8, 16.2 / 11.8 / 119 / 1.25, 1.48, 1.43 / 1.07, 1.29, 1.36
- R50: 1,691.7 / 1,628.0 (1,688.0) / 26.2, 19.5 / 14.1 / 143 / 1.32, 1.59, 1.53 / 1.10, 1.37, 1.45
- R45: 1,715.5 ✘ / 1,641.7 (1,701.7 ✘) / 29.2, 21.8 / 15.7 / 159 / 1.36, 1.67, 1.61 / 1.12, 1.41, 1.51
L/V = Heumann chord-mode curving Y/Q + drawbar lateral (F_LT 29.4, F_C1 24.1 kN); limit Nadal 70°/μ 0.3 = 1.34; with gauge-face lubrication (μ_flange 0.15) Nadal = 1.84.
Smallest radius the current R2 clears, apart from the cylinders (which fail everywhere, even R125): **R80 as drawn (no spirals), R70 with ≥10 m spirals** (dry rail, no lubrication).
Reverse curves: a tangent ≥ 10 m (1 coach) between reverse curves gives no penalty over the single curve. T = 0 raises the coach angle 1.5× (R50: 21.6°, L/V 1.54 at 24 kN).

## 3 Rail Bot claims (verified)
- K1-a angle about half: **confirmed**. True steady angle is (5,180 + 736.5)/R = 3.39° at R100 vs 1.82° (×1.86). The transient at curve entry with no spiral is 7.07° (×2.1; Stress Bot ×1.89). K1-a is fixed in the PE package.
- Alt C coach drawbar 14.3°: ours 14.26° ✔. L/V 0.875 reproduces only as 70 kN·sinα/(2Q). It omits the curving guidance (≈0.89) and the overhang lever. With the full method at 24 kN it is 1.32; at 70 kN it is 2.15.
- Alt D L/V 0.73 (same method ✔); loco–tender 22.2° ✔ (22.1); lead swing 130 vs our 120.5 (theirs includes margin).
- Envelope/play convergence at R48: our loco envelope crosses 1,696 at ≈R49 ✔. Reverse curves → R55: not confirmed when tangents ≥ 10 m.
- Compensation mandatory below R68 for a 2 % start: **confirmed exactly** (Röckl, L3 basis, 68.3 m).

## 4 Stress Bot round 1 (verified)
1. Coupler L/V on reverse curves at 70 kN: **confirmed**, and worse with the curving force included (R50 T0 2.78, R45 2.27, R100 no-spiral 1.49). 70 kN of in-train buff is not acceptable on any curve without spirals. The allowable buff at Nadal is 52 kN for R100 as drawn and 111 kN for R100 with spirals.
2. Drawgear slack: **confirmed** with an independent 6-mass model (drawgear.py). At k 50 kN/mm: 2 mm/joint gives 67 kN start / 66 kN run-in; 10 mm gives 158 kN. At k 200: 1 mm gives 79–88 kN. Preloaded gear (k 20, ≤ 0.5 mm) gives 35 / 33 kN. Matching the loco brake ratio trims run-in by only 10–15 %.
   **Required (Stress Bot R3, rev L4):** preloaded rubber draft gear, renew at **1.0 mm TOTAL play** (F770 daily/annual check, measured at F2137 commissioning); stiffness **k ≥ 20 kN/mm and ≤ 100 kN/mm** for R80 (≤ 25 if route E; drawgear_S3.py: 35.3 kN at k 20, 41.3 kN at k 100 vs F 45.8 kN allowance). Loco service and emergency brake rate **≤ 0.69 m/s²**, matched to the coaches.
3. Pony truck 2.9 kN/wheel: **confirmed** (LT42 body reaction 0). A free-swinging arm gives Y/Q 0.94 vs 1.34 (passes), but only 0.4 kN of centering/friction is allowed.
   A 10–15 kN BODY spring is reacted at X1,525, outside the pivots. It lifts 1.80×F off the front drivers (F2 axle 25.2 → 11.7 kN at 15 kN) and adds 0.80×F to the rear truck (wheel 26.5 > 26 kN ✘).
   **Recommended design:** sprung pony carrying its OWN 1.25 t ballast (12.3 kN; Q 5.96 kN/wheel, 5.2 in twist).
   - Coil springs 2×75 N/mm per side, ±25 mm travel = ±15 %.
   - PTFE/bronze side bearers; body reaction ≈ 0.
   - No lateral centering > 0.5 kN.
   - Swing stops **±120 mm** (Stress Bot R3; swing R80 89.5, E 102, A 72, D 119). Supersedes ±95/145/175.
   - Allowable centering then 0.94 kN dry (3.1 kN lubricated).
   - Loco +1.25 t; no effect on the drivers.
8. Loco end throw: the PE K2-d checked the cab STEP (1,487 at R100). The governing point is the CAB ROOF eave with sway: the sweep gives 1,581.6 at R100 and 1,715.5 at R45, which agrees with K-401 (1,719 at R45). K2-d now uses the sweep.
   - Stress Bot's coach 1.73 m at R50 applies the widest static half at the end throw (conservative). The part-by-part sweep gives 1,628 (+60 garland).
   - Stress Bot's 13.2 mm binding is a 3-axle criterion. A 2-axle 1,550 truck needs 7.6 mm (with flange lead) vs 9.4 ✔.

## 5 Wheel/rail and track structure
- Widening 917.5 (R50–75) / 920.7 (R45–50) is accepted. Worst case 932.8 (built +6, wear +6) leaves 56.2 mm tread on a 47.6 head. Absolute max gauge is 941.4; **maintenance limit 932**. Widening adds up to 9.3 mm of envelope at R50 (included above).
- Restraining rail < R60: **track check gauge 886 +2/−0** (renew < 883; must stay > 881 = wheel check dimension). **Flangeway = G − 886** = 31.6 (min 26.6) at 917.5 and 34.8 (29.8) at 920.7. At 914.4 it would be 23.4 < 25 ✘, so restraining rail requires widened gauge.
- The PE "892" is the worn wheelset flange-face gauge (a wheel dimension); as a track check gauge it would leave 22 mm (✘). The PE text is corrected.
- Track spec: ASCE 40 new at 2×26 kN gives 153 MPa vs 172 ✔. Ties, plates and 9/16 cut spikes are consistent.
  - Lateral basis 0.35×axle = 18.2 kN (the engineer used 17.1). Their "L/V 0.11 at R100" is centrifugal only; flange guidance gives Y/Q 0.8–0.9.
  - On curves < R100: design 0.5×axle lateral, rail braces or 4 spikes/plate on the high rail, gauge-face lubricators.
  - Ballast ≥ 10 in (Stress Bot: subgrade 26–34 psi at 6 in vs 20).
  - Laying-temperature gap chart and rail anchors (Stress Bot #11).

## 6 Loco audit (Loco Bot) — mass, traction, lead truck
- **Mass double-count confirmed.** LT43 moved 1,010 kg (959 machinery/tanks/fluids + 51 retired compressor/VFD) to the tender, but the L3 loco (17,667 kg) still carries it. Corrected loco ≈ **16,657 kg** (16,810 − 1,010 + 857 L3); train ≈ 77.8 t (762.9 kN).
  - Corrected axle loads: lead 5.79 kN/axle (**2.9 kN/wheel**, not 5.4); F1 33.0, **F2 25.2**, R1 46.6, R2 47.0 kN; max wheel 23.5 < 26.
  - Ballast 1.5 → 0.5 t (SB-1 option 2) is weight-neutral; awaits weigh-in. The package is NOT re-baselined here.
- **Equal-torque start** (parallel H1B loop; the lightest axle slips first; cap = 4·μ·Q_min; curve adhesion ×0.95 R100 / ×0.9 R ≤ 60 ASSUMED):

| case | need kN | equal-torque dry | wet (no sand) | per-axle ideal dry |
|---|---|---|---|---|
| 0 % tangent | 15.9 | 25.2 ✔ (pitch transfer 22.9) | 15.1 ✘ 1.05 | 37.9 |
| 0 % R100 | 19.7 | 23.9 ✔ | 14.3 ✘ | 36.1 |
| 0 % R60 | 23.5 | 22.6 ✘ 1.04 | 13.6 ✘ | 34.2 ✔ |
| 0 % R50 | 26.0 | 22.6 ✘ 1.15 | 13.6 ✘ | 34.2 ✔ |
| 0 % R45 | 28.1 | 22.6 ✘ 1.24 | 13.6 ✘ | 34.2 ✔ |
| 2 % (basis, compensated) | 31.1 | 25.2 ✘ 1.24 | 15.1 ✘ | 37.9 ✔ 0.82 |

  Sanding does not lift the equal-torque cap (it is set by the lightest axle).
  - **Required (drive/controls; reported only, drive not edited):** level the driver axle loads (front-truck ballast; 1.0 t over the front pivot gives F2 30.1, cap 30.1) and/or per-motor displacement/slip control so torque follows axle load.
  - Sand is mandatory on wet starts. 2 % stays the brake/holding case.
  - "Laser-levelled 0 %" conflicts with the redline 2 % profiles; the basis is unchanged pending the owner.
- Drag-brake descents (B1-j2): longest A 7.68 m over 505 m, giving disc ΔT 34 K vs 150 ✔.

## 7 Proposed values (to Rail Bot)
- **Lead swing stops:** ±120 mm (Stress Bot R3; R50 not on the working route). Arm-end yaw pivot free (±5°).
- **DB-800 loco–tender pocket:**
  - Loco pocket (150 mouth) limit 32.4° vs need 13.3 (A) / 22.1 (D) / 26.4 (C).
  - Tender pocket (300 mouth) limit 19.2° vs need 10.0 / 16.4 / 19.7. For R50, cut the tender mouth to 150 (32.4°).
  - Rail Bot's 23°/11.6° are the steady loco-side angles; the transients are 26.2°/13.0°.
- **Tender end geometry:** the existing 350 mm static gap loses 24 (A) / 52 (D) / 68 (C) / 82 (B) / 92 (R50 S, T 0). Keep 350; no corner chamfer needed.
- **Safety chains** (at Y±450 ASSUMED): opening on the outside of the curve = 450·sin(body angle) = 53 (R100) / 88 (R60) / 105 (R50) / 117 (R45) mm. Set slack over the straight length to 60 / 100 / 120 mm. Use certified G100 chains.
- **Hoses** (near the centreline, Y ±150): opening 18 / 30 / 35 mm. Glad-hand hoses ≥ 600 long with ≥ 75 mm slack.
- **Garland:** 60 mm per side is fine to R60. At R50 keep widening at 917.5 or limit the garland to 50 mm.

## 8 Minimum-radius recommendation
**Keep R100 (design basis), with 10–12 m spirals on every curve.** Alan Keef's clearance drawing also recommends R100; Stress Bot R100; Rail Bot R60.

**R100 requires:**
- cylinders moved to Y±790 (needed on every alternative)
- ≥ 10 m spirals (Alt A as drawn passes L/V 1.21 at the 37.9 kN adhesion limit, but 70 kN buff would fail)
- preloaded drawgear, renew at 1.0 mm total play, k 20–100 kN/mm (R80)
- matched brake ratio
- sprung own-ballast pony
- curve compensation 0.5 % recommended
- gauge-face lubrication recommended

**R60 (Alt D) additionally requires:**
- 12 m (40 ft) spirals on every R ≤ 70 curve
- **≥ 10 m tangent between reverse curves** (D has 19.8/25.1 ✔)
- **slackless/preloaded draft gear**, which keeps buff ≤ 35 kN; the allowable with spirals + lube is 47 kN (tender), but only 17 kN dry with no lube
- **gauge-face lubrication mandatory** (L/V with spirals: loco 1.36 > 1.34 dry)
- 1.0 % curve compensation
- widened gauge 917.5
- lead stops ±145
- 0.5×axle lateral track design
- traction axle-load levelling / per-motor control (0 % R60 equal-torque 1.04)

**R50 (Alt C) additionally requires** (all of the R60 list, plus):
- restraining rail with widened gauge (917.5 max on R50 for envelope)
- cab-roof eave trim ≥ 10 mm
- garland ≤ 50 mm
- tender pocket mouth 150
- lead stops ±175
- 1.33 % compensation (grade ≤ 0.67 % on the curve)
- chains slack 120
- no emergency-stop or loco-only braking in curves: L/V margin at R50 is thin (1.17 at 33 kN, lubricated limit 1.53)

**R45 (Alt B): not feasible** with the current loco (envelope 1,715 / coach 1,702).

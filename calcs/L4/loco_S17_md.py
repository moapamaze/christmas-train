"""Writes loco_S17_answers.md from loco_S17.json (Steering 17). No prices."""
import json
J = json.load(open('/workspace/train/calcs/L4/loco_S17.json')); a = J['a']; L = []; p = L.append
n = a['plates']
p("# Steering 17 - answers to Loco Bot (shell package, /workspace/loco proposals). Grokky, 28 Oct 2026"); p("")
p("Calc: `calcs/L4/loco_S17.py` → `loco_S17.json`; grillage copy `calcs/L4/l107_grillage_S17.py` (Loco Bot's L-107L engine, read-only import of its geometry) → `l107_hole_moments_S17.json`; mass items in `drive_L4.py` (LB list). Ledger read: /workspace/loco/mass_ledger.csv rev 2 as of 01:32. No prices."); p("")
p("## (a) K2-a on the current ledger")
p("- Changes vs the 16,657 kg base: barrel 2,088.3 @X4231 + saddles 192.3 @X5675 (= 2,280.6 incl. S4N), hood −898, smokebox 227.9 @X450, fittings 51 (dome, stack, bell, whistle at their X), pilot slats 21.9 @X150 (L4.1: corrected from 54.9 per Loco Bot ledger_out; the JSON/ledger already carried 21.9), deck P1-L rev L.1 +28.2 + SS± HSS3x3x1/8 +9.1, cab C1 813.9 for −1,000 L3 cab/front, fit-out 6, JL plates 9.7, FT-1 15.6, BT-1 68.2 @X4075 (Y− pocket).")
p(f"- Front truck +{a['front_truck_extra_kg']:,} kg vs base, rear {a['rear_truck_extra_kg']} kg (your +399/+510 is against the PE row and counts only +77.9 kg of smokebox).")
p(f"- **Front ballast trimmed: plates 1,056 → {a['front_ballast_plates_kg']} kg ({n} × 75.4, {n // 2} per side) + BT-1 68.2 = pocket {a['pocket_total_kg']} kg.** Needed for margin 1.10: {a['ballast_needed_for_margin_110_kg']} kg. Equal-torque dry 2 % start margin **{a['start_margin_dry_equal_2pct']:.2f}** (kept ≥ 1.10). Plates stay symmetric; BT-1 is a 68.2 kg Y− offset.")
p(f"- **K2-a = {a['K2a_kN']} kN vs 26 ({a['K2a_kN']/26:.2f})**, governing wheel F1 on the L3-as-is basis. Without the trim it would be {a['K2a_if_ballast_not_trimmed_kN']} kN (your estimate 25.02, now 25.29 in ledger_out.json).")
p(f"- Loco {a['loco_kg']:,} kg; train {a['train_kg']:,} kg; W {a['W_kN']} kN; 2 % need {a['need_2pct_kN']} kN.")
p(f"- **Smokebox:** {a['smokebox_answer']}"); p(f"- {a['stack_note']}"); p("")
p("## (b) Provisional holes and stringers"); p("| Check | Demand | Capacity | Util | Result |"); p("|---|---:|---:|---:|---|")
for c in J['checks']:
    if c['id'].startswith(('H-', 'SS-', 'L7-')): p(f"| {c['id']} {c['desc']} | {c['demand']} | {c['capacity']} {c['unit']} | {c['util']} | {c['result']} |")
p("")
p("- **S4N at B4 as drawn is NOT accepted.** Two M12 hex-16 rivnuts at X±25 in one bearer section put the hole edge 34.2 mm off the bearer CL. The HSS5x3x3/16 top wall is flat only to 28.6 mm (corner radius 9.5), so the rivnut cannot seat. At Y±250 (over the bolster saddle, LC4P 2 g hogging 7.47 kN·m) the AISC F13.1 net tension wall gives 1.03.")
p("- **Fix (required, and the same for S1–S6 and every F-07 saddle rivnut):** turn the pattern 90°. Put the rivnuts on the bearer CL, in pairs at ±25 in Y about each bolt line (S4N: Y ±225/275 and ±455/505; S1 and S2–S6: ±275/325 and ±575/625). Put the saddle base PL10×100 holes on its CL to match. B4 Y±250 is then 0.70 and B1 0.15.")
p("- S1 at B1: OK with the CL pattern (bearer moment 1.6 kN·m; rivnut tension 0.99 kN vs 4 kN SWL ASSUMED, 0.25).")
p("- Pilot slats: OK with conditions. 20 × M10 tapped through the full 12 mm (or through-bolted with nuts), ≥ 30 mm from box edges and the end-plate welds, ≥ 40 mm clear of the coupler pocket opening (Y±560), and none in the FT-1 load path (FT-1 at Z1355 is above the pilot top Z1250). Row loss 6 %. Slat mass 54.9 kg carried in K2-a.")
p("- Deck side stringers SS± → HSS3x3x1/8 ADOPTED (+9.1 kg in the mass): 0.39 (was 0.57 on C3x4.1). Bearer max with the S17 loads is 0.67 gross (your rev L 0.73 used a 2,345 kg shell + 150 kg smokebox at Y±665).")
p("")
p("## (c) Design basis line 41 - FIXED"); p(f"- Now reads: {J['c']['line41']} Changed in PF-CT_design_basis.md (line 41), B-601 and L-101 notes. Flagged for PE sign-off."); p("")
p("## (d) L-109 R70"); p(f"- {J['d']['answer']}"); p("")
p("## Still owed - answers")
for k, v in J['owed'].items(): p(f"- {v}")
open('/workspace/train/calcs/L4/loco_S17_answers.md', 'w').write("\n".join(L) + "\n")

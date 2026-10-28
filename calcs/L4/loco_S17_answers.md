# Steering 17 - answers to Loco Bot (shell package, /workspace/loco proposals). Grokky, 28 Oct 2026

Calc: `calcs/L4/loco_S17.py` → `loco_S17.json`; grillage copy `calcs/L4/l107_grillage_S17.py` (Loco Bot's L-107L engine, read-only import of its geometry) → `l107_hole_moments_S17.json`; mass items in `drive_L4.py` (LB list). Ledger read: /workspace/loco/mass_ledger.csv rev 2 as of 01:32. No prices.

## (a) K2-a on the current ledger
- Changes vs the 16,657 kg base: barrel 2,088.3 @X4231 + saddles 192.3 @X5675 (= 2,280.6 incl. S4N), hood −898, smokebox 227.9 @X450, fittings 51 (dome, stack, bell, whistle at their X), pilot slats 21.9 @X150 (L4.1: corrected from 54.9 per Loco Bot ledger_out; the JSON/ledger already carried 21.9), deck P1-L rev L.1 +28.2 + SS± HSS3x3x1/8 +9.1, cab C1 813.9 for −1,000 L3 cab/front, fit-out 6, JL plates 9.7, FT-1 15.6, BT-1 68.2 @X4075 (Y− pocket).
- Front truck +2,431 kg vs base, rear -270 kg (your +399/+510 is against the PE row and counts only +77.9 kg of smokebox).
- **Front ballast trimmed: plates 1,056 → 150.8 kg (2 × 75.4, 1 per side) + BT-1 68.2 = pocket 219.0 kg.** Needed for margin 1.10: 0 kg. Equal-torque dry 2 % start margin **1.14** (kept ≥ 1.10). Plates stay symmetric; BT-1 is a 68.2 kg Y− offset.
- **K2-a = 25.89 kN vs 26 (1.00)**, governing wheel F1 on the L3-as-is basis. Without the trim it would be 28.11 kN (your estimate 25.02, now 25.29 in ledger_out.json).
- Loco 19,934 kg; train 81,513 kg; W 799.4 kN; 2 % need 32.61 kN.
- **Smokebox:** NO double count. The 16,657 kg base has no separate smokebox item: SB-1 body/shell 1,900 = L3 3 mm hood 898 + ~1,002 cab/front, and that ~1,000 kg is already removed in full with the L3 cab (CAB-L3-REMOVE). The L3 smokebox front left the ledger with it, and there is no 150 kg placeholder inside the PE figure. So the 227.9 kg counts IN FULL (Loco Bot netted only +77.9 over a placeholder: 150 kg x 2.13 front share = +320 kg more on the front truck than Loco Bot carried). Residual: the removed ~1,000 kg was located at the cab CG X9350; if part of it really sat at the smokebox, the front truck is slightly lighter than computed (conservative for K2-a, unconservative for adhesion by < 1 %). Weigh-in governs.
- L-110 stack 9.0 kg kept (no separate L3 trim stack in the ledger); conservative for the front truck.

## (b) Provisional holes and stringers
| Check | Demand | Capacity | Util | Result |
|---|---:|---:|---:|---|
| H-B4Y250-LB B4 (front bolster) S4N holes at Y±250 as proposed (2 x M12 hex-16 rivnuts at X±25 in one section), AISC F13.1 net tension wall | 136.1 | 131.97 MPa | 1.03 | NG |
| H-B4Y250-CL B4 (front bolster) S4N holes at Y±250 FIX: rivnuts on the bearer CL (pairs at ±25 in Y), 1 hole per section | 136.1 | 194.08 MPa | 0.7 | OK |
| H-B4Y480-LB B4 S4N holes at Y±480 as proposed (2 x M12 hex-16 rivnuts at X±25 in one section), AISC F13.1 net tension wall | 78.79 | 131.97 MPa | 0.6 | OK |
| H-B4Y480-CL B4 S4N holes at Y±480 FIX: rivnuts on the bearer CL (pairs at ±25 in Y), 1 hole per section | 78.79 | 194.08 MPa | 0.41 | OK |
| H-B1Y300-LB B1 S1 holes at Y±300 as proposed (2 x M12 hex-16 rivnuts at X±25 in one section), AISC F13.1 net tension wall | 29.61 | 131.97 MPa | 0.22 | OK |
| H-B1Y300-CL B1 S1 holes at Y±300 FIX: rivnuts on the bearer CL (pairs at ±25 in Y), 1 hole per section | 29.61 | 194.08 MPa | 0.15 | OK |
| H-B1Y600-LB B1 S1 holes at Y±600 as proposed (2 x M12 hex-16 rivnuts at X±25 in one section), AISC F13.1 net tension wall | 13.85 | 131.97 MPa | 0.1 | OK |
| H-B1Y600-CL B1 S1 holes at Y±600 FIX: rivnuts on the bearer CL (pairs at ±25 in Y), 1 hole per section | 13.85 | 194.08 MPa | 0.07 | OK |
| H-edge M12 hex rivnut hole at X±25 vs flat width of the HSS5x3 top wall (corner radius 9.5) | 34.24 | 28.6 mm | 1.2 | NG |
| H-edgeCL FIX: rivnut on the bearer CL, hole edge from CL | 9.24 | 28.6 mm | 0.32 | OK |
| H-S1-T S1 smokebox saddle rivnut tension, 1 g roll + 1 g up (worst bolt) | 990.82 | 4000.0 N | 0.25 | OK |
| H-PS Pilot slats: section loss of the PL12 pilot face along one hole row (10 x Ø11 over 1,800) | 0.06 | 0.15 - | 0.41 | OK |
| SS-HSS Deck side stringers SS± HSS3x3x1/8 (P-A1) max bending, grillage S17 | 81.31 | 207.0 MPa | 0.39 | OK |
| L7-M-S17 Bearer HSS5x3x3/16 max bending with S17 loads (gross) | 139.01 | 207.0 MPa | 0.67 | OK |

- **S4N at B4 as drawn is NOT accepted.** Two M12 hex-16 rivnuts at X±25 in one bearer section put the hole edge 34.2 mm off the bearer CL. The HSS5x3x3/16 top wall is flat only to 28.6 mm (corner radius 9.5), so the rivnut cannot seat. At Y±250 (over the bolster saddle, LC4P 2 g hogging 7.47 kN·m) the AISC F13.1 net tension wall gives 1.03.
- **Fix (required, and the same for S1–S6 and every F-07 saddle rivnut):** turn the pattern 90°. Put the rivnuts on the bearer CL, in pairs at ±25 in Y about each bolt line (S4N: Y ±225/275 and ±455/505; S1 and S2–S6: ±275/325 and ±575/625). Put the saddle base PL10×100 holes on its CL to match. B4 Y±250 is then 0.70 and B1 0.15.
- S1 at B1: OK with the CL pattern (bearer moment 1.6 kN·m; rivnut tension 0.99 kN vs 4 kN SWL ASSUMED, 0.25).
- Pilot slats: OK with conditions. 20 × M10 tapped through the full 12 mm (or through-bolted with nuts), ≥ 30 mm from box edges and the end-plate welds, ≥ 40 mm clear of the coupler pocket opening (Y±560), and none in the FT-1 load path (FT-1 at Z1355 is above the pilot top Z1250). Row loss 6 %. Slat mass 54.9 kg carried in K2-a.
- Deck side stringers SS± → HSS3x3x1/8 ADOPTED (+9.1 kg in the mass): 0.39 (was 0.57 on C3x4.1). Bearer max with the S17 loads is 0.67 gross (your rev L 0.73 used a 2,345 kg shell + 150 kg smokebox at Y±665).

## (c) Design basis line 41 - FIXED
- Now reads: Brakes: every driven axle (F1, F2, R1, R2) and every tender/coach axle is braked; the pony (lead) axle is UNBRAKED. Pony wheels Ø650 new, worn-wheel limit Ø630 (condemning). Loco brake rate <= 0.69 m/s² (Steering 13): brake force from the braked axles only, decelerating the whole loco mass incl. the pony. Changed in PF-CT_design_basis.md (line 41), B-601 and L-101 notes. Flagged for PE sign-off.

## (d) L-109 R70
- CONFIRMED: Loco Bot's R70 sweep reproduces our R100 governing figure exactly (cab eave 1,581.6), and at R70 the cab eave (±1,350, Z top of the 3 mm roof on HSS3x2x1/8 purlins) governs at 1,629.4 vs the K-401 half-width 1,696 = 66.6 mm margin. Front-end items all clear (deck-end corner 198, smokebox 547, pilot 559). End throw 207.6 mm at R70. R70 is not on the owner's working routes (F is R80, the minimum adopted radius is R80) - R70 is a margin check only.

## Still owed - answers
- FT-1: 0.79 (pin/lug) / 0.53 (bolts) / G-209 0.84 - unchanged (holes PROVISIONAL, L-111)
- The 16,657 kg base INCLUDES the L3 PL6 deck 1,248, outriggers 78, steel edge angles 154.5, the 3 mm hood 898 and ~1,000 cab/front (incl. the L3 smokebox front)
- cab C1 813.9 @X9283 replaces the ~1,000 kg L3 cab/front @X9350: net -186.1 kg
- L-104 pin: 150 mm under the head

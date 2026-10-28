"""Steering 17 (28 Oct 2026): Loco Bot shell package (/workspace/loco, proposals) - Grokky checks.
(a) K2-a rerun on the Loco Bot ledger rev 2 (drive_L4.json, LB list) + front-ballast trim; smokebox double-count answer.
(b) provisional holes: S1 saddle at B1, pilot slats, S4N at B4 (moved holes); deck side stringers SS± C3x4.1 -> HSS3x3x1/8.
    Bearer moments from a copy of Loco Bot's L-107L grillage (l107_grillage_S17.py, read-only import of /workspace/loco/l107L/geom.py)
    with the S17 loads: shell 2,331.6 (barrel 2,280.6 incl. saddles + fittings 51), S4N feet Y±250/480 at B4, smokebox 227.9 on S1 at B1 (Y±300/600).
(c) design basis line 41 brakes / pony wheel limit.  (d) L-109 R70 cab eave.  No prices."""
import json, math
g = 9.80665
DL = json.load(open("/workspace/train/calcs/L4/drive_L4.json"))["basis"]; ST = json.load(open("/workspace/train/calcs/L4/drive_L4.json"))["start"]
HM = json.load(open("/workspace/train/calcs/L4/l107_hole_moments_S17.json"))
GR = {c["id"]: c for c in json.load(open("/workspace/train/calcs/L4/l107_grillage_S17_out.json"))["checks"]}
LBO = json.load(open("/workspace/loco/ledger_out.json"))
J = dict(checks=[])
def chk(i, d, dem, cap, u, note=""):
    J["checks"].append(dict(id=i, desc=d, demand=round(dem, 2), capacity=round(cap, 2), unit=u, util=round(dem/cap, 2), result="OK" if dem <= cap else "NG", note=note))
# ---------------- (a)
ax = DL["axle_loads_kN_L3asis_plus_L4"]; Qmax = DL["max_driver_wheel_kN"]
B_old = 1055.6; front_share_B = 1.0      # pocket over the front pivot X4075
Q_if_untrimmed = Qmax + (B_old - DL["ballast_front_kg"]) * g / 4000
margin = [c for c in ST["cases"] if c["case"] == "2% tangent"][0]["dry_equal_margin"]
J["a"] = dict(loco_kg=DL["loco_kg"], items_sum_kg=DL["loco_items_sum_kg"], front_truck_extra_kg=DL["front_truck_extra_kg"], rear_truck_extra_kg=DL["rear_truck_extra_kg"],
              front_ballast_plates_kg=round(DL["ballast_front_kg"], 1), plates=round(DL["ballast_front_kg"] / 75.4), battery_in_pocket_kg=68.2, pocket_total_kg=round(DL["ballast_front_kg"] + 68.2, 1),
              ballast_needed_for_margin_110_kg=ST["ballast_front_kg_for_equal_torque_margin_110"], start_margin_dry_equal_2pct=margin,
              K2a_kN=Qmax, K2a_if_ballast_not_trimmed_kN=round(Q_if_untrimmed, 2), K2a_LocoBot_estimate_kN=LBO.get("K2a_est", LBO.get("K2a_of_record_kN")), LocoBot_front_truck_delta_kg=LBO.get("dR_front_kg", LBO.get("delta_note", {}).get("d_front_truck_kg")),
              axles_L3asis_kN=ax, axles_RT1corr_kN=DL["axle_loads_kN_RT1corr_plus_L4"], train_kg=DL["train_kg"], W_kN=DL["W_kN"], need_2pct_kN=DL["need_2pct_start_kN"],
              smokebox_answer="NO double count. The 16,657 kg base has no separate smokebox item: SB-1 body/shell 1,900 = L3 3 mm hood 898 + ~1,002 cab/front, and that ~1,000 kg is already removed in full with the L3 cab (CAB-L3-REMOVE). The L3 smokebox front left the ledger with it, and there is no 150 kg placeholder inside the PE figure. So the 227.9 kg counts IN FULL (Loco Bot netted only +77.9 over a placeholder: 150 kg x 2.13 front share = +320 kg more on the front truck than Loco Bot carried). Residual: the removed ~1,000 kg was located at the cab CG X9350; if part of it really sat at the smokebox, the front truck is slightly lighter than computed (conservative for K2-a, unconservative for adhesion by < 1 %). Weigh-in governs.",
              stack_note="L-110 stack 9.0 kg kept (no separate L3 trim stack in the ledger); conservative for the front truck.",
              note="Loco Bot's 25.02 kN (25.29 in ledger_out.json after the 01:32 update) added its +399 kg front-truck delta to the PE 24.04 kN and counted only +77.9 kg of smokebox. Recomputed directly on the S17 ledger (smokebox in full, battery in the front pocket): the governing wheel is F1 (front, L3-as-is basis) and the rear truck changes %+d kg. With all S17 items (incl. pilot slats 54.9 and JL plates 9.7 added in ledger rev 2 at 01:32) the front truck gains %d kg vs base (was 1,342), so the pocket plates come down 1,056 -> %.1f kg (%d x 75.4 plates + BT-1 68.2 kg in the Y- pocket) and the equal-torque dry 2%% start margin stays %.2f (rule >= 1.10)." % (DL["rear_truck_extra_kg"], DL["front_truck_extra_kg"], DL["ballast_front_kg"], round(DL["ballast_front_kg"] / 75.4), margin))
chk("K2-a", "Max static driver wheel load, S17 ledger, front plates trimmed to %.1f kg" % DL["ballast_front_kg"], Qmax, 26.0, "kN", "untrimmed 1,056 kg would be %.2f kN" % Q_if_untrimmed)
chk("K2-a/st", "Equal-torque dry 2 %% start margin after the trim (rule >= 1.10)", 1.10, margin, "-", "inverse util: rule / margin")
# ---------------- (b) holes. HSS5x3x3/16 bearer: b 76.2, d 127, t 4.43 (design); outside corner radius 2 x t_nom 4.76 = 9.5 -> flat top wall half-width 28.6
b, d, t, Fy, Fu = 76.2, 127.0, 4.43, 345.0, 427.0; S = 54900.0; flat_half = 38.1 - 9.5
Afg = b * t
def net_allow(n_holes_in_section, dh):
    Afn = (b - n_holes_in_section * dh) * t
    red = min(1.0, Fu * Afn / (Fy * Afg))     # AISC F13.1 (Yt = 1.0), applied to the HSS tension wall
    return 0.6 * Fy * red, Afn
hex_ac = 16.0 / math.cos(math.radians(30))       # 18.5 across corners (worst orientation)
J["b"] = {}
for key, lab in (("B4 Y±250", "B4 (front bolster) S4N holes at Y±250"), ("B4 Y±480", "B4 S4N holes at Y±480"), ("B1 Y±300", "B1 S1 holes at Y±300"), ("B1 Y±600", "B1 S1 holes at Y±600")):
    M = HM[key]["M_Nmm"]; f = M / S
    a1, _ = net_allow(2, hex_ac); a2, _ = net_allow(1, hex_ac)
    J["b"][key] = dict(M_kNm=round(M / 1e6, 2), case=HM[key]["case"], f_gross_MPa=round(f, 1), allow_LocoBot_pattern_MPa=round(a1, 1), allow_CL_row_MPa=round(a2, 1))
    chk("H-" + key.replace(" ", "").replace("±", "") + "-LB", lab + " as proposed (2 x M12 hex-16 rivnuts at X±25 in one section), AISC F13.1 net tension wall", f, a1, "MPa", HM[key]["case"])
    chk("H-" + key.replace(" ", "").replace("±", "") + "-CL", lab + " FIX: rivnuts on the bearer CL (pairs at ±25 in Y), 1 hole per section", f, a2, "MPa", HM[key]["case"])
edge = 25.0 + hex_ac / 2
chk("H-edge", "M12 hex rivnut hole at X±25 vs flat width of the HSS5x3 top wall (corner radius 9.5)", edge, flat_half, "mm", "hole runs %.1f mm into the corner radius: rivnut cannot seat - applies to every F-07 saddle rivnut (S1-S6, 40 off)" % (edge - flat_half))
chk("H-edgeCL", "FIX: rivnut on the bearer CL, hole edge from CL", hex_ac / 2, flat_half, "mm", "fully on the flat")
# S1 rivnut tension (same method as Loco Bot SD-3): 227.9 kg, roll arm 955, 1 g roll + 1 g up, 8 bolts Y±300/600
W1 = 227.9 * g; Iy = 2 * (2 * 300**2 + 2 * 600**2); T = W1 / 8 + W1 * 955 * 600 / Iy
chk("H-S1-T", "S1 smokebox saddle rivnut tension, 1 g roll + 1 g up (worst bolt)", T, 4000.0, "N", "rivnut SWL 4 kN ASSUMED (Loco Bot) - confirm supplier")
# pilot slats: 20 x M10 tapped into the L3 PL12 pilot face (10 slats, 2 rows of 10 across Y±900)
loss = 10 * 11.0 / 1800.0
chk("H-PS", "Pilot slats: section loss of the PL12 pilot face along one hole row (10 x Ø11 over 1,800)", loss, 0.15, "-", "limit 15 % ASSUMED for a non-structural fascia row; conditions: holes >= 30 mm (2.5d+) from box edges and the end-plate welds, >= 40 mm (4d) clear of the coupler pocket opening Y±560, tapped full 12 mm (1.2d engagement) or through-bolted with nuts, no holes in the drawbar/FT-1 load path (FT-1 is at Z1355 above the pilot top Z1250)")
chk("SS-HSS", "Deck side stringers SS± HSS3x3x1/8 (P-A1) max bending, grillage S17", GR["L7-M SS+"]["demand"], GR["L7-M SS+"]["capacity"], "MPa", "C3x4.1 was 85.2/150 = 0.57; +9.1 kg in the ledger")
chk("L7-M-S17", "Bearer HSS5x3x3/16 max bending with S17 loads (gross)", GR["L7-M bearer HSS5x3x3/16"]["demand"], GR["L7-M bearer HSS5x3x3/16"]["capacity"], "MPa", "Loco Bot rev L 152.1 (0.73) used shell 2,345.1 + 150 smokebox at Y±665")
# ---------------- (c) design basis line 41
J["c"] = dict(line41="Brakes: every driven axle (F1, F2, R1, R2) and every tender/coach axle is braked; the pony (lead) axle is UNBRAKED. Pony wheels Ø650 new, worn-wheel limit Ø630 (condemning). Loco brake rate <= 0.69 m/s² (Steering 13): brake force from the braked axles only, decelerating the whole loco mass incl. the pony.",
              old="brakes on every axle (incl. the pony)", for_PE="sign-off item")
# ---------------- (d) L-109 R70
J["d"] = dict(cab_eave_R70=1629.4, limit=1696.0, margin=66.6, R100=1581.6, answer="CONFIRMED: Loco Bot's R70 sweep reproduces our R100 governing figure exactly (cab eave 1,581.6), and at R70 the cab eave (±1,350, Z top of the 3 mm roof on HSS3x2x1/8 purlins) governs at 1,629.4 vs the K-401 half-width 1,696 = 66.6 mm margin. Front-end items all clear (deck-end corner 198, smokebox 547, pilot 559). End throw 207.6 mm at R70. R70 is not on the owner's working routes (F is R80, the minimum adopted radius is R80) - R70 is a margin check only.")
chk("L-109", "R70 swept half-width, cab eave governs", 1629.4, 1696.0, "mm", "margin 66.6")
J["owed"] = dict(FT1="FT-1: 0.79 (pin/lug) / 0.53 (bolts) / G-209 0.84 - unchanged (holes PROVISIONAL, L-111)",
                 deck_hood_base="The 16,657 kg base INCLUDES the L3 PL6 deck 1,248, outriggers 78, steel edge angles 154.5, the 3 mm hood 898 and ~1,000 cab/front (incl. the L3 smokebox front)",
                 cab_basis="cab C1 813.9 @X9283 replaces the ~1,000 kg L3 cab/front @X9350: net -186.1 kg", L104_pin="L-104 pin: 150 mm under the head")
json.dump(J, open("/workspace/train/calcs/L4/loco_S17.json", "w"), indent=1)
for c in J["checks"]: print(c["id"], c["demand"], c["capacity"], c["util"], c["result"])
print(J["a"]["note"])

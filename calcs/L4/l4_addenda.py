"""Rev L4 addenda (28 Oct 2026, steerings 6-8 + follow-ups): Loco Bot a-e, Electro E3, Source Bot rev 3 a-e.
Reads drive_L4.json (L-107 P1-L +36.5 kg, cab C1, FT-1, tender TB-3 8,295 kg). No prices."""
import json, math, csv
g = 9.80665
D9 = json.load(open("/workspace/train/calcs/L4/drive_L4.json"))
LC = json.load(open("/workspace/train/calcs/track/loco_check.json"))["mass"]
J = {"rev": "L4 addenda 28 Oct 2026"}
# ---- (a) L-107 cases, ballast rebalance, every wheel load vs 26 kN
lead_wheel = LC["lead_wheel_kN"]; pony_wheel = lead_wheel + 1250 * g / 1000 / 4
def case(D):
    b = D["basis"]; adh = b["axle_loads_kN_RT1corr_plus_L4"]; asis = b["axle_loads_kN_L3asis_plus_L4"]
    wheels = {k: round(max(adh[k], asis[k]) / 2, 2) for k in adh}
    st = D["start"]["cases"]; c2 = [c for c in st if c["case"] == "2% tangent"][0]
    return dict(L107_kg=b["L107_kg"], loco_kg=b["loco_kg"], train_kg=b["train_kg"], front_ballast_kg=round(b["ballast_front_kg"]), ballast_plates_per_side=round(b["ballast_front_kg"] / 150.8 * 1), ballast_plates=round(b["ballast_front_kg"] / 75.4),
                axle_kN_adhesion_basis=adh, axle_kN_L3asis_basis=asis, wheel_kN_max_of_bases=wheels,
                lead_pony_wheel_kN=round(pony_wheel, 2), K2a_max_wheel_kN=b["max_driver_wheel_kN"], K2a_util=round(b["max_driver_wheel_kN"] / 26.0, 3),
                all_wheels_pass_26kN=all(v <= 26.0 for v in wheels.values()) and pony_wheel <= 26.0,
                equal_torque_2pct_dry_margin=c2["dry_equal_margin"], wet_unsanded_2pct_margin_equal=c2["wet_equal_margin"], unsprung_drive_per_axle_kg=D["unsprung_per_axle"]["total_drive_unsprung_kg"])
J["L107_P1L"] = case(D9)
J["L107_P1L"]["note"] = ("Steering 11: L-107 is P1-L (aluminium deck) net +36.5 kg (moment CG X6024) - Steering 17: rev L.1 +28.2 + SS± HSS3x3x1/8 +9.1 = +37.3 kg; the 939/470 kg cases are DROPPED. Front ballast = smallest pair of 75.4 kg plates giving the "
                         f"equal-torque dry 2% start margin ≥ 1.10 (L4.1: no flow divider - equal torque governs) → {round(D9['basis']['ballast_front_kg'])} kg ({round(D9['basis']['ballast_front_kg'] / 75.4)} plates of 75.4 kg; Steering 17 trim with BT-1 68.2 kg in the Y- pocket). Lead/pony wheel = 2.89 kN + own 1.25 t ballast / 4. Owner decision C9.")
# ---- base contents and deductions for Loco Bot (steering 11 b)
J["base_contents"] = dict(
    deck=dict(answer="YES - the 16,657 kg base INCLUDES the L3 PL6 deck 1,248 kg", evidence=["train/cad/mass_report.json PF-L110_loco_frame_only 3,815.3 kg = frame 2,229.4 + deck 1,248.1 + coupler 209.9 + ballast 127.9",
        "structural_body_study.md §4 option 1 'R2 as drawn': frame steel 3,815 inside loco 16,810 (LT42) → 16,657 after the LT43 double-count removal (loco_check.py)"]),
    hood=dict(answer="YES - includes the L3 3 mm hood 898 kg", evidence=["structural_body_study.md §4: body/shell steel 1,900 = hood 898 + ~1,002 cab/front"]),
    cab=dict(answer="The base carries the L3 cab inside the 1,900 kg body/shell (1,900 - 898 hood = ~1,002 kg cab/front). Treated as a 1,000 kg placeholder at X9350 (cab X8000-10700 mid).",
             replaced_by="Cab L-111 C1 813.9 kg @X9283 Z2722 (net -186.1 kg) + FT-1 15.6 kg @X200"),
    deductions_for_LocoBot=["P1-L net +36.5 kg as ledgered (deck -529.9 = Al 718 - PL6 1,248; outriggers -78; edge angles -103.1) - do NOT also add P1, and do not add 1,248 back",
                            "L3-HOOD-REMOVE -898 @X4300 - correct, keep", "Add a CAB-L3-REMOVE -1,000 @X9350 row against CAB-L111-C1 +813.9 @X9283 (net -186.1); FT-1 +15.6 @X200",
                            "Barrel L-108 enters as its full 2,135 kg (net +1,237 after the hood removal) - unchanged"])
fr = lambda x: (7275 - x) / 3200
_dF = 813.9 * fr(9283) - 1000 * fr(9350); _dR = -186.1 - _dF
J["cab_effect"] = dict(front_truck_kg=round(_dF, 1), rear_truck_kg=round(_dR, 1), front_wheel_kN=round(_dF * g / 4 / 1000, 2), rear_wheel_kN=round(_dR * g / 4 / 1000, 2),
                       ft1_front_wheel_kN=round(15.6 * fr(200) * g / 4 / 1000, 3),
                       note="Cab swap alone moves ~138 kg onto the front truck (lever, behind the rear pivot) and takes ~324 kg off the rear. Final K2-a with all steering-11 changes and rebalanced ballast in L107_P1L.")
# ---- FT-1 front tow lug (L-111) verification
P, av, ah = 70.0, math.radians(20), math.radians(15)
Tax = P * math.cos(av) * math.cos(ah); Vres = math.hypot(P * math.sin(av), P * math.cos(av) * math.sin(ah))
mp = 345 * 8.86 ** 2 / 4                                   # N·mm/mm, HSS12x6x3/8 A500C Fy 345, design wall 8.86
a, b, c, d = 278.0, 328.0, 126.0, 236.0                    # clamped panel (flat x length) and bolt-patch
Pu_pyr = 4 * mp * (a / ((b - d) / 2) + b / ((a - c) / 2)) / 1000   # pyramid yield-line, fixed edges (m = m')
Pu_pyr_alt = 4 * mp * (a / ((b - c) / 2) + b / ((a - d) / 2)) / 1000
J["FT1"] = dict(load=f"{P} kN at up to 20° vertical / 15° lateral (L-111)", axial_kN=round(Tax, 1), shear_resultant_kN=round(Vres, 1), shear_per_bolt_kN=round(Vres / 8, 2),
    FT1a=dict(LocoBot="T 14.0 / V 3.7 kN per bolt, T/21 + V/30 = 0.79", check=round(14.0 / 21 + 3.7 / 30, 2), uniform_tension_per_bolt_kN=round(Tax / 8, 2),
              verdict="VERIFIED: 14.0/21 + 3.7/30 = 0.79; V matches 70 kN components/8 = %.2f; T 14.0 vs uniform %.2f implies the lug-eccentricity moment on the far row (plausible). HB16-2 clamp range covers PL + 9.5 wall (ASSUMED from Lindapter range table - confirm)." % (Vres / 8, Tax / 8)),
    FT1b=dict(LocoBot="Pu 220 kN / 1.67 = 131.55 vs 70 → 0.53", mp_Nmm_per_mm=round(mp), Pu_pyramid_kN=round(Pu_pyr, 1), Pu_pyramid_other_orientation_kN=round(Pu_pyr_alt, 1),
              Pu_with_10pct_corner_lever_reduction_kN=round(0.9 * min(Pu_pyr, Pu_pyr_alt), 1), util_independent=round(P / (0.9 * min(Pu_pyr, Pu_pyr_alt) / 1.67), 2),
              verdict="VERIFIED (conservative): independent pyramid yield-line with clamped edges gives Pu ≈ %.0f kN (≈ %.0f kN with a 10%% corner-lever allowance) ≥ Loco Bot's 220 kN, so 0.53 stands as the governing (lower-bound) figure; independent util %.2f. Full 70 kN applied to the wall (the axial component is %.1f kN)." % (min(Pu_pyr, Pu_pyr_alt), 0.9 * min(Pu_pyr, Pu_pyr_alt), P / (0.9 * min(Pu_pyr, Pu_pyr_alt) / 1.67), Tax)),
    other_checks="FT-1c lug 0.16, d 0.23, e 0.32, f 0.42, g weld 0.42, h Crosby G-209 shackle 0.84, i end-sill W2 welds 0.05 (Loco Bot) - accepted",
    holes=("8 HB16-2 in the FRONT end sill are ACCEPTED (provisional) - the earlier 'end-sill holes REJECTED' applies to the L-107 running-board brackets in the drawgear/end-sill zones, not to FT-1. "
           "Conditions: drilled not burned; ≥ 50 mm from weld toes and ≥ 3t from the HSS corner radius; no other holes inside the 126 × 236 patch; Lindapter install torque; line of pull through the bolt-group centroid ±25 mm."),
    verdict="FT-1 PASS - governing util 0.84 (G-209 shackle); bolts 0.79; wall 0.53")
# ---- (c) hood
J["hood_in_base"] = dict(answer="YES - the 16,657 kg base includes the L3 3 mm hood (898 kg)", evidence=["structural_body_study.md §4: R2 as drawn body/shell steel 1,900 kg INCLUDING the 3 mm hood 898 kg + 1,500 ballast, inside the LT42 16,810 kg",
    "loco_check.py: 16,657 = LT42 16,810 - 1,010 relocated + 857 L3 (hood not removed)"],
    consequence="barrel delta = 2,135 - 898 = +1,237 kg (not +385 vs the 1,750 L-107 provisional shell load). Loco Bot ledger line L3-HOOD-REMOVE -898 is CORRECT and must stay.")
# ---- (b) HB16 holes - reconciled with l107/bracket_load_table.csv (Loco Bot L7-B1..B3 per-bolt values)
rows = list(csv.DictReader(open("/workspace/loco/l107/bracket_load_table.csv")))
rb = [r for r in rows if r["type"] == "RB"]
Fz = max(float(r["Fz_down_max"]) for r in rb); Fx = max(float(r["Fx_3gP"]) for r in rb); Fy = max(float(r["Fy_1gP"]) for r in rb)
up = max(float(r["Fz_up_max"]) for r in rows if r["type"] == "BS")
t_w, Fu, d_b, d_h = 8.86, 427.0, 16.0, 26.0           # HSS12x6x3/8 A500C design wall 0.93 x 9.53; Fu 62 ksi
V_lb, T_lb = 15.4, 8.9                                 # Loco Bot L7-B3 (3 g long.) / L7-B2 (1 g lat.) per bolt, incl. PROV
Rbear = 2.4 * d_b * t_w * Fu / 2.0 / 1000; Rtear = 1.2 * (140 - d_h) * t_w * Fu / 2.0 / 1000
J["HB16_holes"] = dict(
    table_max=dict(RB_Fz_down_kN=Fz, RB_Fx_3g_kN=Fx, RB_Fy_1g_kN=Fy, BS_uplift_kN=up),
    rail_web_24=dict(where="HSS12x6x3/8 outer webs, Z1360, X station ±70, B1/B2/B3/B5/B7/B8",
                     HB16_linear_worst=round(max(V_lb / 30, T_lb / 21), 2), HB16_combined_LC_note="Loco Bot L7-B1..B3 linear T/21+V/30 max 0.51 (3 g long.)",
                     bearing_kN=dict(demand=V_lb, allow=round(min(Rbear, Rtear), 1), util=round(V_lb / min(Rbear, Rtear), 2)),
                     net_section="hole 57.6 mm off the rail NA; Ix loss 0.93 % → rail bending util 0.262 (C4 net); fatigue Δσ 10.3 vs Cat D 48 MPa (0.21)",
                     verdict="APPROVED with the loco_interfaces_L4 conditions (B1 group moved to X530; ≥ 50 mm from weld toes; drilled)"),
    bolster_4=dict(uplift_kN=up, util=round(up / 21, 2), verdict="APPROVED if moved to Y±90 (52 mm from the rail-web weld toe)"),
    end_sill_2=dict(verdict="REJECTED (drawgear zone X ≥ 10,148) - SD-2 bears on the sill without holes; hold-down by a clamp plate under the sill flange"),
    summary="28 of 30 holes approved (24 rail web + 4 bolster); 2 end-sill holes rejected. Worst HB16 0.51, web bearing 0.21, rail net section 0.26.")
# ---- (d) L-104 pin length
J["L104_pin"] = dict(grip_mm=108, head_mm=20, washer_mm=2, crossbolt_hole_centre_below_mm=15, end_distance_mm=15, L_under_head_required_mm=108 + 2 + 15 + 15,
                     L_specified_mm=150, overall_mm=170, drawn_mm=250,
                     verdict="model.py grip 108 is right; L-104 '250' was wrong (142 mm hanging below the pocket). Specify Ø60 × 150 under head (170 o/a). L-104 schedule corrected.",
                     count="5 joints × 2 = 10 + 2 spares = 12 pins, 12 bushes, 12 Ø10 cross-bolts, 12 R-clips")
# ---- (e) chain cases vs L-107 bearers / saddles
cases_x = [(2964.0, 3875.6), (4274.4, 5186.0), (6164.0, 7075.6), (7474.4, 8386.0)]; case_z_top, case_y_out = 1061.0, 257.0
rb_z_bot, rb_y_in = 1175.0, 316.0                       # RB-1 web plate bottom Z1175, on the rail OUTER web (Y ≥ 316)
cl = {}
for nm, x in (("B3/S3/F5", 2450.0), ("B5/S5/F11", 5675.0), ("B7", 8900.0)):
    dx = min(min(abs(x - a), abs(x - b)) for a, b in cases_x)
    cl[nm] = dict(X=x, plan_gap_mm=round(dx - 100), vertical_gap_mm=round(rb_z_bot - case_z_top), vertical_gap_at_25_bump_mm=round(rb_z_bot - case_z_top - 25), lateral_gap_mm=round(rb_y_in - case_y_out))
J["chain_case_clearance"] = dict(stations=cl, truck_yaw_R50_lateral_mm=35, verdict="CLEAR - bracket half-width 100 deducted; the case is 114 mm below and 59 mm inboard of every RB-1 and ≥ 389 mm away in plan; saddles S3/S5 sit on top of the bearers at Z ≥ 1,400 (frames F5/F11 above the rails)")
# ---- Electro E3
J["electrical_E3"] = dict(battery="BT-1: 2 × Lifeline GPL-27T 24 V + box, 68.2 kg, MOVED to the Y- front ballast pocket X4075 (Electro E3.3, Steering 17) - replaces plates kg-for-kg; was 56 kg under the cab X≈10,200",
                          jumpers="2/0 jumpers ~40 kg (tender/coach), train mass only", hot_kW="30.94 / 32.44 vs 33 shed point", winter_kW="31.20 / 32.70")
# ---- Source Bot rev 3
T = float(D9['motor_bearing']['spline_T_HPRV_Nm']); KA = 1.5; Td = T * KA   # L4.2: motor torque at the HPRV (380 bar -> 2,830 N.m; was 2,979 at 400)
m, z, dB = 3.0, 17, 55.0; d = m * z; h_w = 2.4; Lsp = 60.0; phi = 0.75   # L4.1: ~60 mm = full code-5 spline (Source Bot rev 3.5), was 70 ASSUMED
p = 2 * Td * 1e3 / (d * z * h_w * Lsp * phi)
D_hub, d_f2 = 133.0, 57.6
tau_hub = 16 * Td * 1e3 * D_hub / (math.pi * (D_hub**4 - d_f2**4))
p70 = 2 * Td * 1e3 / (d * z * h_w * 70.0 * phi); L_min = 2 * Td * 1e3 / (d * z * h_w * 100.0 * phi)
p_lim = 2 * (T * 350 / 380) * KA * 1e3 / (d * z * h_w * Lsp * phi)
J["spline_W55x3x17"] = dict(motor_shaft="Poclain MS05 shaft code 5, DIN 5480 W55x3x17 (male; 30°, flank-centred, 7H slide fit); 15T Martin D120B15 hub broached DIN 5480 N55x3x17 (female)",
    L_engaged_mm=Lsp, L_L4_assumed_mm=70.0, flank_pressure_L70_MPa=round(p70, 1), L_min_for_100MPa_mm=round(L_min, 1), flank_at_limiter_350_x1p5_MPa=round(p_lim, 1),
    L41_decision="Engage the FULL code-5 spline (~60 mm, AWAIT Poclain shaft drawing): REQUIRE ≥ 58 mm engaged, 15T hub face to shaft shoulder ≤ 2 mm, end plate + M16 retaining bolt; util %.2f at HPRV × 1.5 (≤ 1.0 OK). If the drawing shows < 58 mm: 15T made to order from 4140 Q&T 28-32 HRC (allow ~150 MPa → util ~%.2f)" % (p / 100, p / 150),
    T_HPRV_Nm=T, shock_KA=KA, T_design_Nm=Td, flank_pressure_MPa=round(p, 1), flank_allow_C1045_MPa=100.0, flank_util_C1045=round(p / 100, 2), flank_allow_MPa=150.0, flank_util=round(p / 150, 2), L42_strength_basis="430 bar strength basis x KA 1.5: catalogue C1045 15T hub %.1f MPa vs 100 = %.2f NG -> L4.2 RULING: 15T sprocket MADE TO ORDER from 4140 Q&T 28-32 HRC, DIN 5480 N55x3x17 broached, >= 58 mm engaged (allow 150 MPa, util %.2f); Martin D120B15 stock hub NOT accepted" % (p, p / 100, p / 150),
    basis="p = 2·T·KA/(d·z·h_w·L·φ), d 51, h_w 2.4 (ASSUMED effective), L 60 engaged (L4.1 = full code-5 spline per Source Bot rev 3.5; L4 assumed 70), φ 0.75; allow 100 MPa = C1045 hub, fixed spline, reversing (ASSUMED)",
    hub_torsion_MPa=round(tau_hub, 1), hub_torsion_allow_MPa=round(0.4 * 310, 0), hub_torsion_util=round(tau_hub / 124, 2),
    shaft_note="Shaft code 5 itself is Poclain-rated to the motor's 450 bar torque (3,352 N·m) > %s at HPRV 380; shock above that" % format(round(T), ',') + " - AWAIT Poclain AE written confirmation",
    ring_bolts="L4.1: 45T ring web to the Ø350 hub flange: 12 × M16 cl.8.8 FITTED DIN 609 / DIN 7968 (catalog), reamed Ø17, PCD 300, edge 25 mm = 1.47 d0; %.2f kN/bolt at HPRV (× 1.5 = %.2f) vs 87 kN shear (util 0.09); tighten 219 N·m dry (153 lubricated), Nord-Lock NL16 - see drive_L4.json axle.ring_bolts" % (T * 3 / 0.15 / 12 / 1000, T * 3 / 0.15 / 12 / 1000 * 1.5))
J["pump_H1P053"] = dict(input_shaft="L4.1: KEEP shaft G1 (ISO 3019-1 32-4, 14T 12/24, 534/592 N·m) on the SAE B 2-bolt flange; the AIE 'SAE B 13T pump drive' mates only G4 (180/222 N·m) which FAILS on the 265 N·m engine peak (1.19) → engine pump-drive coupling hub 14T 12/24 (≥ 48 mm engagement); alternate G5 15T 16/32 (370 N·m max). AIE confirmation HELD. Calc: drive_L4.json pump_shaft",
                        CCO="order EDC WITH CCO (control cut-off; Danfoss option E7/E8 12/24 V, Deutsch 2-pin): de-energized = pump to neutral. Wired in series with the Pilz PNOZ s30 7 mph safe output (independent of PLUS+1)",
                        charge_filter="external charge filtration, HYDAC DF 60 pressure filter (420 bar) with clogging indicator, β ≥ 200 at 10 µm (ASSUMED grade)")
J["brake_failsafe"] = dict(BP_bar=5.0, BP_psi=72.5, distributor="Knorr KE (UIC), apply-on-pressure output C",
    inverting_relay="WABCO IR-2 inverting relay 971 899 152 0 between the KE output C and the loco spring-brake (release) chambers, supply from MR via a ≤ 6 bar regulator",
    BP_vent="ASCO 8210G035 24 VDC, de-energize-to-vent, on the BP",
    logic=["BP drop → KE output C rises → IR-2 exhausts the release chambers → springs apply (proportional in service, full in emergency)",
           "24 V loss or s30 overspeed trip → ASCO de-energizes → BP vents → emergency on all vehicles; same s30 output drops H1P053 CCO → pump neutral",
           "MR / IR-2 supply loss → release chambers exhaust → springs apply",
           "Release only when BP ≥ 4.8 bar, MR healthy and 24 V healthy"],
    verify="IR-2 part number and its inversion curve vs the Coremo release range (5.1-6 bar) - AWAIT WABCO data sheet; PE to confirm the PL for the s30 → ASCO/CCO path")
J["drawbar"] = json.load(open("/workspace/train/calcs/L4/drawbar_L4.json"))["decision"]
json.dump(J, open("/workspace/train/calcs/L4/l4_addenda.json", "w"), indent=1, ensure_ascii=False)
if __name__ == "__main__":
    for k in ("L107_P1L", "base_contents", "cab_effect", "FT1", "HB16_holes", "L104_pin", "chain_case_clearance", "spline_W55x3x17"):
        print("==", k, json.dumps(J[k], ensure_ascii=False)[:1500])

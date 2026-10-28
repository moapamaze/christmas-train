"""No-belt drive study (28 Oct 2026). Study only: does not touch drawings, site or zip.
Envelope: build/model.py nobelt_envelope_check(); performance basis: drive_L3.py numbers."""
import sys, json, math
sys.path.insert(0, "/workspace/train/build")
import model
F_need, F_adh = 31.53, 37.93        # kN (2% start; dry adhesion)
r_w = 0.725; v6 = 35.3              # wheel radius m; wheel rpm at 6 mph
Qp = 133.0                          # L/min H1P053 delivered
T_run = 3502.0                      # N.m per axle running at 2%
SF = 1.6
def TE(Vg_cc, i, dp=350, eta_m=0.92, eta_g=0.97, n=4):
    T = Vg_cc * dp / (20 * math.pi) * eta_m      # N.m per motor
    return n * T * i * eta_g / r_w / 1000
R = {}
# ---- (a)/(b)/(c) in-line on the TA II input (clocking sweep)
motors = {"H1B110 SAE L*": (316.4, 125, 70), "H1B080 SAE L*": (289.9, 115, 57), "H1B080 SAE T*": (261.4, 115, 57),
          "H1B080 DIN L*": (265.9, 115, 50), "H1B080 DIN T*": (237.4, 115, 50), "H1B080 cartridge": (187.5, 110, 50),
          "fixed bent-axis 80cc (A2FM80 class, AWAIT)": (210, 95, 50), "MS05 2-speed no brake": (312, 150, 80),
          "MS05 2-speed + brake": (370, 150, 80)}
inline = {}
for lab, m in motors.items():
    for se in (100.0, 40.0):    # catalog shaft end Y+100 / Dodge-shortened input shaft Y+40
        best = None
        for th in range(-90, 91, 5):
            res = model.nobelt_envelope_check("inline", theta_deg=th, motor=(lab,) + m, shaft_end=se)
            mot = [r for r in res if "flange" in r["part"]][0]
            worst = min(r["min_gap_mm"] for r in res if "output lobe" not in r["part"])
            if best is None or worst > best[0]:
                best = (worst, th, mot["against"], mot["part"])
        inline[f"{lab} | shaft end Y{se:.0f}"] = dict(best_min_gap_mm=best[0], best_clock_deg=best[1], limited_by=best[2], motor=best[3],
                                                     fits=best[0] >= 10)
R["inline_sweep"] = inline
R["rangle"] = model.nobelt_envelope_check("rangle")
R["chain"] = model.nobelt_envelope_check("chain")
# ---- performance
perf = {}
perf["L3 belt (baseline) H1B110 x14.9"] = dict(start_kN=round(min(TE(110, 14.9), F_adh), 1), theory_kN=round(TE(110, 14.9), 1))
perf["(b) H1B080 x14.9"] = dict(start_kN_350=round(TE(80, 14.9, eta_m=0.9), 1), start_kN_400=round(TE(80, 14.9, 400, 0.9), 1))
te_c = TE(560, 5.0)
perf["(c) TA 5:1 + MS05 560/280"] = dict(start_kN=round(min(te_c, F_adh), 1), theory_kN=round(te_c, 1))
te_ch = TE(468, 3.0)
flow_6 = 4 * 0.234 * v6 * 3 / 0.95
perf["chain MS05 468/234 x3.0 (15/45)"] = dict(start_kN=round(min(te_ch, F_adh), 1), theory_kN=round(te_ch, 1),
    start_300bar_kN=round(TE(468, 3.0, 300), 1), margin=round(min(te_ch, F_adh) / F_need, 2),
    motor_rpm_6mph=round(v6 * 3, 1), flow_6mph_Lmin=round(flow_6, 1), pump_stop_cc=round(flow_6 / Qp * 53, 1),
    top_mph_full_disp=round(Qp * 0.95 / (4 * 0.468) / 3 / v6 * 6, 2), top_mph_half_disp_capability=round(Qp * 0.95 / (4 * 0.234) / 3 / v6 * 6, 2),
    TE_2nd_disp_350_kN=round(TE(234, 3.0), 1), run_2pct_kN=round(4 * T_run / r_w / 1000, 1))
# chain loads (per axle)
r_s = 0.546 / 2
T_adh_ax = F_adh * 1000 * r_w / 4
T_hprv_ax = 468 * 400 / (20 * math.pi) * 3.0
P_ult_120_2 = 2 * 151.2 * 0.85    # kN, ANSI 120 min tensile 34,000 lbf x2 strands x0.85 multi-strand factor
perf["chain loads"] = dict(axle_T_adh_Nm=round(T_adh_ax), pull_adh_kN=round(T_adh_ax / r_s / 1000, 1),
    axle_T_HPRV_Nm=round(T_hprv_ax), pull_HPRV_kN=round(T_hprv_ax / r_s / 1000, 1), ANSI120_2_ult_kN=round(P_ult_120_2),
    SF_ult_adh=round(P_ult_120_2 / (T_adh_ax / r_s / 1000), 1), SF_ult_HPRV=round(P_ult_120_2 / (T_hprv_ax / r_s / 1000), 1),
    chain_speed_mps_6mph=round(v6 * 3 * 15 * 0.0381 / 60, 2), wrap_small_deg=round(180 - 2 * math.degrees(math.asin((546 - 183) / 2 / 450)), 0),
    centre_pitches=round(450 / 38.1, 1),
    MS05_brake_park_kN=round(4 * 3165 * 3 / r_w / 1000, 1), MS05_brake_emerg_kN=round(4 * 2740 * 3 / r_w / 1000, 1))
# right angle torque use
for lab, Tr, d, kg in (("NORD SK 9072.1 / SEW KA127 class", 8500, 95, 360), ("NORD SK 9082.1", 13000, 110, 650), ("SEW KA157", 18000, 120, 600)):
    perf["(d) " + lab] = dict(rated_Nm=Tr, axle_seat_mm=d, approx_kg=kg, use_start_SF16=round(5715 * SF / Tr, 2),
        use_adh_SF16=round(6875 * SF / Tr, 2), use_run_SF16=round(T_run * SF / Tr, 2), start_kN=round(min(TE(110, 14.9), F_adh), 1))
R["perf"] = perf
json.dump(R, open("/workspace/train/calcs/L3/nobelt_study.json", "w"), indent=1, ensure_ascii=False)
for k, v in inline.items(): print(k, v)
print("RANGLE"); [print(" ", r) for r in R["rangle"]]
print("CHAIN"); [print(" ", r) for r in R["chain"]]
for k, v in perf.items(): print(k, v)

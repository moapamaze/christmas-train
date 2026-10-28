"""Rev L2 drive: inboard axle-hung spur-gear case per axle (owner choice F25 (c), 27 Oct 2026), 4 x Poclain MSE05 750/375 cc.
Basic AGMA 2101-D04 (metric) screens; supplier data marked AWAIT; assumptions marked ASSUMED. No prices here."""
import math, json
g = 9.81
J = {}
# ---------- basis
m_train = 77.8 - 8.16 + json.load(open("/workspace/train/calcs/tender_mass_T2.json"))["total_kg"] / 1000
W = m_train * g                      # kN
need2 = W * 0.0408                   # 2% start (calc basis)
need_lv = W * 0.019611324849561015
run = {g_: W * (0.005 + g_ / 100) for g_ in (0, 0.5, 1.0, 1.5, 2.0)}   # running resistance kN
adh_dry, adh_wet = 35.8, 21.5
D = 1450.0; r = D / 2000
n_mot = 4; cc = 750.0; cc2 = 375.0
z1, z2, mod = 21, 38, 10.0           # pinion / gear teeth, module mm
ratio = z2 / z1
eta_g = 0.98                         # single spur mesh incl. bearings ASSUMED
p_work, p_relief = 350.0, 400.0      # bar; H1P053 option L35 (supplier_data_L2 F3): pressure limiter 350 (non-dissipative, gear rating basis), HPRV 400 (transient peak = structural case); pump max 400, MSE05 max 400
p_lim = p_work
def F(p, eta, rt=ratio, c=cc): return n_mot * p / 10 * c / (2 * math.pi) * eta * rt * eta_g / r / 1000
J["basis"] = dict(train_t=round(m_train, 3), W_kN=round(W, 1), need_2pct_start_kN=round(need2, 2), need_level_start_kN=round(need_lv, 2),
                  running_kN={str(k): round(v, 2) for k, v in run.items()}, adh_dry_kN=adh_dry, adh_wet_kN=adh_wet)
# ---------- ratio scan
scan = {}
for a, b in ((20, 35), (21, 37), (21, 38), (20, 36), (19, 35)):
    rt = b / a
    nmax = 133.0 * 0.95 / (4 * cc2 / 1000)            # motor rpm at H1P053 full flow, small displacement
    vmax = nmax / rt * math.pi * D / 1000 / 60 / 0.44704
    scan[f"{a}:{b}"] = dict(ratio=round(rt, 4), F350_eta095=round(F(350, .95, rt), 2), F350_eta080=round(F(350, .80, rt), 2),
                           F380_eta080=round(F(380, .80, rt), 2), vmax_H1P053_mph=round(vmax, 2),
                           motor_rpm_10mph=round(10 * 0.44704 / (math.pi * D / 1000) * 60 * rt, 1))
J["ratio_scan"] = scan
# ---------- chosen
Fd = dict(F350_eta092=F(350, .92), F350_eta078=F(350, .78), F350_eta095=F(350, .95))   # F6: 0.92 base (Poclain 625 cc chart), 0.78 marginal (if the reading is the 750 cc cam) - AWAIT Poclain start torque
J["start"] = {k: round(v, 2) for k, v in Fd.items()}
J["start"].update(dry_available_kN=round(min(Fd["F350_eta092"], adh_dry), 2), dry_available_conservative_kN=round(min(Fd["F350_eta078"], adh_dry), 2),
                  dry_margin_conservative_kN=round(min(Fd["F350_eta078"], adh_dry) - need2, 2), eta_base=0.92, eta_marginal=0.78, eta_note="0.78 MARGINAL - pending Poclain starting torque (F6)", wet_available_kN=adh_wet,
                  wet_shortfall_kN=round(need2 - adh_wet, 2), sand_mu_needed=round(need2 / (adh_dry / 0.25), 3),
                  p_at_adhesion_eta092_bar=round(350 * adh_dry / Fd["F350_eta092"], 0), p_needed_eta078_bar=round(350 * need2 / Fd["F350_eta078"], 0),
                  level_wet_start_ok=need_lv < adh_wet)
w10 = 10 * 0.44704 / (math.pi * D / 1000) * 60
J["speed"] = dict(wheel_rpm_10mph=round(w10, 1), motor_rpm_10mph=round(w10 * ratio, 1), MSE05_limit_rpm="160 (1st) / 190 (2nd disp.) - 750 cc Classic, Poclain catalog (F1); HighFlow 220/240", MSE05_limit_2nd_rpm=190, motor_speed_util_10mph=round(w10 * ratio / 190, 2),
                  wheel_rpm_7p5mph=round(w10 * .75, 1), motor_rpm_7p5mph=round(w10 * .75 * ratio, 1),
                  flow_7p5mph_375cc_Lmin=round(4 * cc2 / 1000 * w10 * .75 * ratio / 0.95, 1), flow_10mph_375cc_Lmin=round(4 * cc2 / 1000 * w10 * ratio / 0.95, 1),
                  H1P053_Lmin=132.9, H1P060_Lmin=149.2,
                  vmax_flow_H1P053_mph=scan["21:38"]["vmax_H1P053_mph"],
                  vmax_flow_H1P060_mph=round(149.2 * 0.95 / (4 * cc2 / 1000) / ratio * math.pi * D / 1000 / 60 / 0.44704, 2))
# ---------- engine power / speed (V3307 45.6 kW net continuous; 3 charge + 7 aux -> 35 kW pump allowance; LT25 method)
def speed_on(Fk, P_pump=35.0):
    # iterate pressure-dependent line loss: rim = P_pump*0.855*0.855*dp/(dp+10)*eta_g
    v = 1.0
    for _ in range(50):
        T_m = Fk * 1000 * r / (n_mot * ratio * eta_g) / 0.95          # motor torque, N.m (use 2nd disp when it fits)
        disp = cc2 if (T_m * 2 * math.pi / (cc2 / 1e6) / 1e5) <= 350 else cc
        dp = T_m * 2 * math.pi / (disp / 1e6) / 1e5
        P_rim = P_pump * 0.855 * 0.855 * dp / (dp + 10) * eta_g
        v = P_rim / Fk
    vflow = 132.9 * 0.95 / (4 * disp / 1000) / ratio * math.pi * D / 1000 / 60
    return min(v, vflow, 7.5 * 0.44704) / 0.44704, round(dp), disp, round(P_rim, 1), vflow / 0.44704
tab = []
for gr, Fk in run.items():
    v, dp, disp, Pr, vf = speed_on(Fk)
    tab.append(dict(grade_pct=gr, resistance_kN=round(Fk, 2), speed_mph=round(v, 2), motor_dp_bar=dp, displacement_cc=disp, rim_kW=Pr,
                    limit=("7.5 mph governor" if v >= 7.49 else ("pump flow" if abs(v - vf) < 0.01 else "engine power"))))
J["power_speed_V3307"] = dict(engine_net_continuous_kW=45.6, charge_kW=3, aux_kW=7, pump_allowance_kW=35, eff="pump 0.855, motor 0.855, 10 bar loss, gear 0.98", table=tab,
                             hold_2pct_mph=[t for t in tab if t["grade_pct"] == 2.0][0]["speed_mph"],
                             full_start_force_speed_mph=round(35 * 0.855 * 0.855 * 0.97 * eta_g / need2 / 0.44704, 2),
                             kW_net_for_7p5mph_on_2pct=round((run[2.0] * 7.5 * 0.44704 / (0.855 * 0.855 * 0.97 * eta_g)) + 10, 0))
# ---------- gears (AGMA 2101 metric, basic)
d1, d2 = mod * z1, mod * z2; a = (d1 + d2) / 2; b = 100.0
T1_relief = p_relief / 10 * cc / (2 * math.pi)            # ideal motor torque at HPRV 400 bar (no eff credit) N.m - structural peak
T1_lim = p_lim / 10 * cc / (2 * math.pi)                  # at pressure limiter 350 bar - gear rating basis
T1_start = need2 * 1000 * r / (n_mot * ratio * eta_g)    # pinion torque at the 2% start
T1_adh = adh_dry * 1000 * r / (n_mot * ratio * eta_g)    # dry-slip limit
v_pitch = math.pi * d1 / 1000 * (w10 * ratio) / 60
Ko, Ks, KH, KB = 1.25, 1.0, 1.3, 1.0                       # moderate shock, size, load distribution (b/d~0.5, enclosed), rim
Kv = ((200 * 0 + 1)) if False else (( (59.77 + math.sqrt(200 * v_pitch)) / 59.77) ** 0.8255)  # AGMA Qv 8-ish: A=59.77,B=0.8255 (Qv 8)
YJ1, YJ2 = 0.34, 0.39                                     # AGMA 908 geometry factors, 20 deg full depth, 21/38 (chart, ASSUMED)
ZE = 191.0                                                # sqrt(MPa) steel/steel
ZI = math.cos(math.radians(20)) * math.sin(math.radians(20)) / 2 * ratio / (ratio + 1)
def bend(T, YJ, ko=Ko): Ft = 2 * T / (d1 / 1000); return Ft * ko * Kv * Ks * KH * KB / (b * mod * YJ)
def cont(T, ko=Ko): Ft = 2 * T / (d1 / 1000); return ZE * math.sqrt(Ft * ko * Kv * Ks * KH / (d1 * b * ZI))
St, Sc = 450.0, 1550.0                                   # AGMA 2001 grade 2 carburized & hardened (58-64 HRC case), MPa
gears = dict(module=mod, z_pinion=z1, z_gear=z2, ratio=round(ratio, 4), pressure_angle_deg=20, face_mm=b, d_pinion=d1, d_gear=d2,
             centre_mm=a, od_pinion=d1 + 2 * mod, od_gear=d2 + 2 * mod, material="18CrNiMo7-6 / AISI 8620 carburized, ground, AGMA Q10 (ASSUMED)",
             pitch_v_10mph_ms=round(v_pitch, 2), Kv=round(Kv, 3), factors=dict(Ko=Ko, Ks=Ks, KH=KH, KB=KB, YJ_pinion=YJ1, YJ_gear=YJ2, ZI=round(ZI, 4)))
for lab, T, ko in (("limiter_350bar", T1_lim, Ko), ("hprv_400bar_transient", T1_relief, 1.0), ("dry_slip_35p8kN", T1_adh, Ko), ("start_2pct_31p2kN", T1_start, Ko)):
    sb1, sb2, sc = bend(T, YJ1, ko), bend(T, YJ2, ko), cont(T, ko)
    gears[lab] = dict(Ko=ko, T_pinion_Nm=round(T), T_axle_Nm=round(T * ratio * eta_g), Ft_kN=round(2 * T / d1, 1), sigma_b_pinion=round(sb1), sigma_b_gear=round(sb2),
                      sigma_c=round(sc), SF_bend=round(St / sb1, 2), SH_contact=round(Sc / sc, 2))
J["gears"] = gears
# ---------- shafts, axle, keys
T_ax_relief = T1_relief * ratio
J["axle"] = dict(d_mm=130, T_relief_Nm=round(T_ax_relief), tau_MPa=round(16 * T_ax_relief * 1e3 / (math.pi * 130**3), 1),
                 gear_seat="Ø150 seat on a stepped axle ASSUMED; keyless locking assembly or shrink fit (supplier sizes); key alt. 36x20x160 on Ø150",
                 key_alt_bearing_MPa=round(2 * T_ax_relief * 1e3 / (150 * 10 * 160), 1), allow_key_MPa=150.0)
Tp = T1_relief
J["pinion_shaft"] = dict(d_mm=70, tau_MPa=round(16 * Tp * 1e3 / (math.pi * 70**3), 1), note="pinion integral with shaft, two bearings in the case; motor shaft drives it by spline, no gear load on the motor (Poclain shaft version)")
# ---------- bearings (loads; catalog ratings AWAIT)
Ft = 2 * T1_relief / d1 * 1000; Fr = Ft * math.tan(math.radians(20)); Fm = math.hypot(Ft, Fr)
Fs = 2 * T1_start / d1 * 1000; Fms = math.hypot(Fs, Fs * math.tan(math.radians(20)))
m_case, m_motor = 260.0, 55.0                     # ASSUMED gear case + gear/pinion 260 kg; MSE05 shaft motor 55 kg (Poclain)
J["bearings"] = dict(mesh_force_relief_kN=round(Fm / 1000, 1), mesh_force_start_kN=round(Fms / 1000, 1),
                     pinion_brg_each_peak_kN=round(Fm / 2000 * 1.1, 1), axle_suspension_brg_each_peak_kN=round((Fm / 2 + (m_case + m_motor) * g * 0.6 * 2.0) / 1000, 1),
                     static_C0_min_pinion_kN=round(Fm / 2000 * 1.1 * 2.0, 1), static_C0_min_axle_kN=round((Fm / 2 + (m_case + m_motor) * g * 0.6 * 2.0) / 1000 * 2.0, 1),
                     selection="pinion: 2 x SKF 22214 E (C0 228 kN; alt. 32214 J2/Q C0 208); case on axle: 2 x SKF 23030 CC/W33 (C0 750 kN; alt. 32030 X C0 655) - SKF catalog (supplier_data_L2 §3); s0>=2 required",
                     s0_pinion_22214E=round(228 / (Fm / 2000 * 1.1), 1), s0_axle_23030CC=round(750 / ((Fm / 2 + (m_case + m_motor) * g * 0.6 * 2.0) / 1000), 1),
                     fatigue_note="Running loads are small (35 kW pump allowance: ~2 kN rim per axle at 7.5 mph); bearings are governed by start/peak static loads and the 3 g vertical shock on the axle-hung mass")
# ---------- torque reaction (nose suspension to the transom)
arm = 0.640                                       # axle CL to nose link, m (link under transom X 135 from truck centre)
J["torque_reaction"] = dict(type="axle-hung case on 2 suspension bearings + rubber-bushed vertical nose link to the transom underside (classic nose-suspended)",
                            arm_m=arm, link_force_relief_kN=round(T_ax_relief / arm / 1000, 1), link_force_start_kN=round(T1_start * ratio * eta_g / arm / 1000, 1),
                            link_static_weight_kN=round((m_case + m_motor) * g * 0.45 / 1000, 2),
                            link="M24 rod-end / rubber-bushed link 2 x Ø60 bushes (AWAIT supplier); bracket PL20 welded to transom bottom PL16",
                            transom_bracket_weld="2 x 150 mm 8 fillet: throat 1,697 mm2 -> " + str(round((T_ax_relief / arm * 1.5 + (m_case + m_motor) * g * 3) / 1697, 1)) + " MPa at 1.5 x relief + 3 g (allow 145)",
                            path="nose link -> transom (Z850-1050) -> inside sideframes Y+/-330-360 -> axleboxes; nothing outside the wheels")
# ---------- packaging (nominal mm, truck coords, axle at x=0,z=725, motor toward truck centre)
J["packaging"] = dict(case_Y=[-255, -95], gear_lobe_dia=450, pinion_centre_x=a, motor="Poclain MSE05 shaft version Ø300 x 360 (incl. flange) ASSUMED from guide Ø300 x 312-370",
                      motor_Y=[-95, 265], motor_X=[a - 150, a + 150], motor_Z=[725 - 150, 725 + 150], case_bottom_Z=725 - 225,
                      clear_to_axlebox_X_mm=a - 150 - 110, clear_to_transom_face_mm=625 - (a + 150), clear_to_sideframe_Y_mm=330 - 265,
                      inside_frame_window_Y="+/-330 (inside sideframes); package spans Y-255..+265; main rails Y+/-240 are 300 mm higher (Z1150) - not a constraint at axle level",
                      stagger="case on -Y for axles X3300/6500, mirrored (+Y) for X4850/8050",
                      brake="axle disc space is taken by the gear case and motor; Ø340x25 disc + spring-applied air-released caliper (>= 22 kN clamp) on the pinion-shaft extension (PE calc B1-g)")

# ---------- supplier fold-in (calcs/suppliers/supplier_data_L2.md F1-F11, 27 Oct 2026) - no prices
J["supplier_foldin"] = dict(
    motor_speed=dict(limit_rpm_1st=160, limit_rpm_2nd=190, variant="Classic", n_10mph=round(w10 * ratio, 1), util=round(w10 * ratio / 190, 2), ref="F1"),
    pump=dict(model="Danfoss H1P053", input_shaft="G1 14T 12/24 DP, 534 N·m rated / 592 max (F2)", T_unlimited_400bar_Nm=round(400 * 53.8 / (2 * math.pi * 10) / 0.93, 0),
              T_unlimited_350bar_Nm=round(350 * 53.8 / (2 * math.pi * 10) / 0.93, 0),
              limiter="NO hydromechanical limiter on H1P - 35 kW cap by anti-stall software: AC-1/AC-2 automotive control, or EDC + PLUS+1 anti-stall (destroke on engine droop / p×Vg limit) (F2)",
              pressure="L35: pressure limiter 350 bar + HPRV 400 bar (F3); relief-case torques re-run at 350 (gear rating) and 400 (structural)",
              charge="charge relief ≤ 30 bar (24-28 bar), Poclain boost window 15-30 bar (F4)",
              case_drain="dedicated unrestricted motor case-drain line to tank, at/above shaft height; motor case ≤ 1 bar (F5)"),
    motor_shaft=dict(spline="DIN 5480 N55x3x17 (female in 42CrMo4)", keyed_limit_Nm=800, T_motor_400bar_Nm=round(T1_relief), T_motor_350bar_Nm=round(T1_lim), ref="F7 - keyed Ø50 shaft NOT permitted"),
    start_eta=dict(base=0.92, marginal=0.78, F_base_kN=round(Fd["F350_eta092"], 2), F_marginal_kN=round(Fd["F350_eta078"], 2), need_kN=round(need2, 2),
                   margin_marginal=round(Fd["F350_eta078"] / need2, 3), ref="F6 - 0.78 marginal, pending Poclain start torque"),
    brake=dict(r_eff_m=0.135, caliper_ref="Coremo Ocmea D 3.5N spring-applied air-released (24.2 kN clamp, 19.8 kg) - ref only, AWAIT supplier", release_air="regulated release-air supply off MR: 6 bar max regulator for Coremo (5.1-6 bar) (F9)",
               commissioning="pad burnish / bedding step before brake tests - initial torque may be 30-50 % below nominal (F8)", parking_option="T04 integral brake parking/hold only, not service (F10)"),
    bearings=dict(pinion="SKF 22214 E (alt. 32214 J2/Q pair) 70x125x31, C 213 / C0 228 kN", axle="SKF 23030 CC/W33 (alt. 32030 X pair) 150x225x56, C 531 / C0 750 kN",
                  L10h=dict(b22214E=8.2e7, b32214=2.9e7, b23030CC=6.7e8, b32030X=2.0e8), target_h=7500, ref="F11 / l10_L2.py - life governed by seats + static/shock, not L10"))

json.dump(J, open("/workspace/train/calcs/L2/gear_drive_L2.json", "w"), indent=1)
print(json.dumps(J, indent=1))

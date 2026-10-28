"""Rev L3 drive (28 Oct 2026, owner [pt77u] 'choose the best fit'): per powered axle a catalog Dodge Torque-Arm II
TA7315H15MS (14.9:1, Ø120 straight bore, catalog TA rod) on the axle, driven by a Danfoss H1B110 variable bent-axis motor
through a 1:1 synchronous-belt input drop (envelope fix E-L3-1, see packaging), pump H1P053 kept.
Owner-selected governed maximum 6 mph (H1B minimum-displacement stop + PLUS+1 pump control + overspeed trip) - PE to confirm.
Rejected alternative: L2 custom 1.81:1 spur case + MSE05 750 (calcs/L2). Fallback: TA7315H05MS 5.2:1 + Poclain MS05 ~280 cc.
Sources: ABB/Dodge Metric TA II catalog (src/dd/taii_metric.txt), Dodge MN1601, Danfoss H1B TI BC152886483576en-001303 (src/dd/h1b_ti.txt).
Supplier values not in hand = AWAIT; engineering choices = ASSUMED. No prices."""
import math, json
g = 9.80665
J = {}
# ---------------------------------------------------------------- basis (same as PE package, L3 masses)
m_add_axle = dict(reducer_TA7315H15MS=226.8, TA_rod_907109=19.6, H1B110_SAE=48.8, belt_drop_bracket_guard_sprockets=45.0,
                  disc_2_calipers=58.0, rod_anchor_bracket=10.0)          # kg; bracket/guard/sprockets 45 and 2nd caliper ASSUMED
m_axle_add = sum(m_add_axle.values())
m_L3_delta = 4 * m_axle_add - 4 * 160 - 136     # DT5 cartridge/coupling/carrier removed, stubs shortened (as L2); plan motor mass left in the base (conservative)
m_train = 77944 + m_L3_delta
W = m_train * g / 1000
drv = 143.3 + m_L3_delta * g / 1000
need2 = 0.0408 * W
adh_dry, adh_wet, mu_sand = 0.25 * drv, 0.15 * drv, 0.25
r = 0.725; D = 1.45
J["basis"] = dict(added_per_axle_kg=m_add_axle, added_per_axle_total_kg=round(m_axle_add, 1), m_L3_delta_kg=round(m_L3_delta), train_kg=round(m_train), W_kN=round(W, 1),
                  driver_weight_kN=round(drv, 1), need_2pct_start_kN=round(need2, 2), adh_dry_kN=round(adh_dry, 2), adh_wet_kN=round(adh_wet, 2),
                  v_governed_mph=6.0, v_overspeed_trip_mph=7.0, v_hardware_capability_mph=10.0,
                  governed_note="6 mph = OWNER-SELECTED governed maximum (28 Oct 2026); hard hydraulic limit = H1B minimum-displacement stop at 60 cc (tamper-sealed) + PLUS+1 pump speed control + independent overspeed trip 7 mph (ASSUMED) -> emergency brake. PE to confirm.")
# ---------------------------------------------------------------- components
i_red = 14.9                     # TA7315H15MS actual ratio (catalog Ref/Actual 14.9)
i_belt = 1.0
eta_red, eta_belt, eta_s_start, eta_hm_run, eta_v = 0.96, 0.97, 0.90, 0.92, 0.95   # ASSUMED: 2-stage helical 0.96; synchronous belt 0.97; bent-axis start 0.90 (AWAIT Danfoss); running hm 0.92; vol 0.95
Vg_max, Vg_min_hw, Vg_stop = 110.0, 22.0, 60.0        # cc; H1B110 min setting range 22-74 cc (TI p40); 60 cc stop for the 6 mph governor
tq_bar = 1.75                    # N.m/bar theoretical at max displacement (TI p11)
n_rated = dict(max_disp=2900, min_disp=4800); n_max = dict(max_disp=3700, min_disp=5950)
p_work, p_hprv, p_motor_max = 350.0, 400.0, 450.0
Q_pump = 133.0                   # L/min H1P053 at 2,600 rpm x 0.95 (L2 basis 132.9)
def F_start(p, eta=eta_s_start): return 4 * tq_bar * p * eta * i_belt * eta_belt * i_red * eta_red / r / 1000
J["components"] = dict(reducer="Dodge Torque-Arm II TA7315H15MS x 120 mm straight bore, part 907012, ratio 14.9, 226.8 kg (catalog)", rod="TA7315/8407RA TA rod assembly 907109, 19.6 kg",
                       motor="Danfoss H1B110 SAE-D (152-4) flange, 110/22 cc (min setting 22-74 cc), electric proportional control L* or two-position with PCOR (T*/P*), speed sensor (VS housing), 48.8 kg; 1.75 N.m/bar; rated 2,900 rpm @max / 4,800 @min disp; max working 450 bar",
                       belt="1:1 synchronous belt drop (Gates Poly Chain GT Carbon 14MGT class, ~Ø160 sprockets, c-c ~195) - catalog parts, rating AWAIT Gates",
                       pump="Danfoss H1P053 kept (G1 shaft, L35 PL 350 / HPRV 400, AC-2 or EDC + PLUS+1 anti-stall)",
                       eff=dict(reducer=eta_red, belt=eta_belt, motor_start_hm=eta_s_start, motor_run_hm=eta_hm_run, motor_vol=eta_v))
# ---------------------------------------------------------------- start / adhesion / pressure
F350 = F_start(350); F400 = F_start(400)
p_31 = 350 * need2 / F350
J["start"] = dict(F350_theory_capped_kN=round(min(F350, adh_dry), 2), F350_kN=round(F350, 2), F400_kN=round(F400, 2), adh_dry_kN=round(adh_dry, 2),
                  need_kN=round(need2, 2), margin_vs_need=round(min(F350, adh_dry) / need2, 3), p_for_need_bar=round(p_31), p_at_adhesion_bar=round(350 * adh_dry / F350),
                  F350_eta080_kN=round(F_start(350, 0.80), 2), p_for_need_eta080_bar=round(350 * need2 / F_start(350, 0.80)),
                  wet_unsanded_kN=round(adh_wet, 2), mu_sand_req=round(need2 / drv, 3), note="Adhesion-limited: pressure need only reach ~%d bar for the 2%% start; still holds at a pessimistic start eta 0.80 (%d bar)" % (round(p_31), round(350 * need2 / F_start(350, 0.80))))
# ---------------------------------------------------------------- speeds
def wheel_rpm(mph): return mph * 0.44704 / (math.pi * D) * 60
def motor_rpm(mph): return wheel_rpm(mph) * i_red * i_belt
def flow(mph, Vg): return 4 * Vg / 1000 * motor_rpm(mph) / eta_v
def v_flow(Vg, Q=Q_pump): return Q * eta_v / (4 * Vg / 1000) / (i_red * i_belt) / 60 * math.pi * D / 0.44704
Vg_for_6 = Q_pump * eta_v / (4 * motor_rpm(6.0)) * 1000
J["speed"] = dict(wheel_rpm_6mph=round(wheel_rpm(6), 1), motor_rpm_6mph=round(motor_rpm(6)), wheel_rpm_10mph=round(wheel_rpm(10), 1), motor_rpm_10mph=round(motor_rpm(10)),
                  reducer_input_rpm_6mph=round(motor_rpm(6)), reducer_input_limit_rpm=1790, reducer_output_limit_rpm=120,
                  flow_10mph_full_Lmin=round(flow(10, Vg_max)), flow_10mph_min22_Lmin=round(flow(10, Vg_min_hw), 1), vmax_hw_22cc_mph=round(v_flow(Vg_min_hw), 2),
                  Vg_stop_for_6mph_cc=round(Vg_for_6, 1), Vg_stop_set_cc=Vg_stop, vmax_at_60cc_mph=round(v_flow(Vg_stop), 2),
                  motor_rated_rpm_at_min=n_rated["min_disp"], motor_util_10mph_hw=round(motor_rpm(10) / n_rated["min_disp"], 3),
                  spin_one_axle_60cc_rpm=round(Q_pump * eta_v / Vg_stop * 1000), spin_one_axle_22cc_rpm=round(Q_pump * eta_v / Vg_min_hw * 1000),
                  spin_note="If one wheelset spins while the others stick, it can take all pump flow: 60 cc stop -> %d rpm (< 2,900 motor rated) but > 1,790 TA II input max -> per-motor speed sensors + PLUS+1 anti-slip destroke REQUIRED (spec); with 22 cc it would be %d rpm (> 4,800 rated)" % (round(Q_pump * eta_v / Vg_stop * 1000), round(Q_pump * eta_v / Vg_min_hw * 1000)))
# ---------------------------------------------------------------- power-limited speeds (V3307 35 kW pump allowance, L2 method)
def run_res(gr): return W * (0.005 + gr / 100)
def speed_on(Fk, P=35.0, vcap=6.0, Vfloor=None):
    Vfloor = Vg_stop if Vfloor is None else Vfloor
    v = 1.0; dp = 100.0
    for _ in range(60):
        T_ax = Fk * 1000 * r / 4
        T_m = T_ax / (i_red * eta_red * i_belt * eta_belt)
        # motor goes to the smallest displacement that holds dp <= 350 (H1B PCOR/proportional), not below the 60 cc stop
        Vg = max(Vfloor, min(Vg_max, T_m * 2 * math.pi / (350e5 * eta_hm_run) * 1e6))
        dp = T_m * 2 * math.pi / (Vg / 1e6) / 1e5 / eta_hm_run
        P_rim = P * 0.855 * eta_hm_run * eta_v / 0.855 * 0.855 * dp / (dp + 10) * eta_red * eta_belt   # pump 0.855 overall; motor 0.92x0.95; 10 bar line loss
        v = P_rim / Fk
    vf = v_flow(Vg) * 0.44704
    vv = min(v, vf, vcap * 0.44704)
    return vv / 0.44704, round(dp), round(Vg, 1), round(P_rim, 1), ("governor" if vv >= vcap * 0.44704 - 1e-6 else ("flow" if vv >= vf - 1e-6 else "power"))
tab = []
for gr in (0, 0.5, 1.0, 1.5, 2.0):
    v6 = speed_on(run_res(gr)); v10 = speed_on(run_res(gr), vcap=10.0, Vfloor=Vg_min_hw)
    tab.append(dict(grade_pct=gr, resistance_kN=round(run_res(gr), 2), speed_6mph_gov=round(v6[0], 2), limit=v6[4], dp_bar=v6[1], Vg_cc=v6[2], rim_kW=v6[3], speed_hw_uncapped=round(v10[0], 2)))
hold2 = [t for t in tab if t["grade_pct"] == 2.0][0]["speed_6mph_gov"]
J["power_speed"] = dict(table=tab, hold_2pct_mph=hold2, target_mph=2.0, method="35 kW pump allowance x pump 0.855 x motor 0.92 hm x 0.95 vol x dp/(dp+10) x reducer 0.96 x belt 0.97; motor at the displacement that holds dp<=350, not below the 60 cc stop")
# ---------------------------------------------------------------- reducer rating (TA II SF 1.0 catalog, 15:1 TA7315H)
rate = {10: 11030, 20: 10517, 30: 10196, 40: 9960, 50: 9770, 60: 9609, 70: 9471, 80: 9349, 90: 9206, 100: 8935, 110: 8726, 120: 8504}
def rating(n):
    ks = sorted(rate); n = max(10, min(120, n))
    for a, b in zip(ks, ks[1:]):
        if a <= n <= b: return rate[a] + (rate[b] - rate[a]) * (n - a) / (b - a)
    return rate[10]
SF_shock = 1.6                                    # Dodge 'heavy shock' service factor applied to traction (ASSUMED until Dodge AE confirms)
T_adh = adh_dry * 1000 * r / 4                     # wheel-slip limit per axle
T_need = need2 * 1000 * r / 4
T_hprv = tq_bar * p_hprv * i_red                  # theoretical, no efficiency credit (structural peak)
T_350 = tq_bar * 350 * i_red * eta_red * eta_belt
T_run2 = run_res(2.0) * 1000 * r / 4
n_run2 = wheel_rpm(hold2)
red = dict(rating_10rpm_SF1=11030, start_allow_200pct=22060,
           start_need_SF16=dict(T=round(T_need * SF_shock), cap=22060, util=round(T_need * SF_shock / 22060, 3)),
           adhesion_slip_SF16=dict(T=round(T_adh * SF_shock), cap=22060, util=round(T_adh * SF_shock / 22060, 3)),
           hprv_400bar_peak=dict(T=round(T_hprv), cap=22060, util=round(T_hprv / 22060, 3)),
           running_2pct_SF16=dict(T=round(T_run2 * SF_shock), n_rpm=round(n_run2, 1), cap=round(rating(n_run2)), util=round(T_run2 * SF_shock / rating(n_run2), 3)),
           adhesion_as_running_SF1=dict(T=round(T_adh), cap=11030, util=round(T_adh / 11030, 3), note="even a sustained slip-limit pull is inside the SF 1.0 running rating"),
           limiter_350bar=dict(T=round(T_350)), SF_used=SF_shock,
           note="Catalog is for electric-motor industrial drives; Dodge requires Application Engineering review for a non-electric prime mover / heavy shock -> AWAIT Dodge AE (rail traction not a catalog application)")
J["reducer"] = red
# ---------------------------------------------------------------- motor checks
J["motor"] = dict(T_350_Nm=round(tq_bar * 350), T_400_Nm=round(tq_bar * 400), p_max_working_bar=450, p_hprv_bar=400, util_pressure=round(400 / 450, 3),
                  n_6mph=round(motor_rpm(6)), n_10mph_hw=round(motor_rpm(10)), rated_min=4800, rated_max=2900,
                  control="H1B electric proportional (L*) driven by PLUS+1: starts at max displacement (max start torque), destrokes toward the 60 cc stop with speed; PCOR (pressure compensator override, option T*/P* family) returns motor toward max displacement when loop pressure rises (hill/start) = hydraulic anti-stall/auto-downshift; BPD (brake pressure defeat) keeps PCOR from fighting dynamic braking. Pump anti-stall (engine droop) unchanged on H1P053.",
                  min_stop="minimum-displacement limiter screw set to 60 cc and lock-wired/sealed (6 mph). Hardware can be reset to 22 cc for ~10 mph capability (not permitted in service).",
                  brake="H1B has NO brake -> axle disc + 2 spring-applied calipers per powered axle (B1)", speed_sensor="VS/DS housing with speed sensor port - order with sensor (overspeed + anti-slip)")
# ---------------------------------------------------------------- axle at the Ø120 keyed reducer seat
ax_load = drv / 4; Q = ax_load / 2
Mb_EN = 1.25 * Q * 0.157 + 0.35 * ax_load * 0.725            # kN.m (EN 13103 simplified, same as X1-a)
m_hung = m_add_axle["reducer_TA7315H15MS"] + m_add_axle["H1B110_SAE"] + m_add_axle["belt_drop_bracket_guard_sprockets"]
arm = 0.470                                                   # rod pin on the housing input end, 470 from the axle (ASSUMED layout)
F_rod_adh = T_adh / arm / 1000; F_rod_hprv = T_hprv / arm / 1000
P_hub = m_hung * g * 3.0 / 1000 + F_rod_adh                  # 3 g vertical on hung mass + rod reaction (kN) at the hub
a_hub, L_box = 0.330 - 0.1325, 0.660                         # hub centre Y-132.5, boxes at Y+/-330
M_hub = P_hub * a_hub * (L_box - a_hub) / L_box
M_seat = Mb_EN + M_hub
def sig(M, d): return 32 * M * 1e6 / (math.pi * d**3)
def tau(T, d): return 16 * T * 1e3 / (math.pi * d**3)
d = 120.0
sa_nom = sig(M_seat, d); tm_nom = tau(T_need, d); t_pk = tau(T_hprv, d)
def goodman(Su, Kf, Kfs, d=120.0, k_surf_treat=1.0, Sy=None):
    Se1 = 0.5 * min(Su, 1400); ka = 4.51 * Su**-0.265; kb = 1.51 * d**-0.157; ke = 0.814
    Se = Se1 * ka * kb * ke * k_surf_treat
    sa = Kf * sig(M_seat, d); sm = math.sqrt(3) * Kfs * tau(T_need, d)
    n = 1 / (sa / Se + sm / Su)
    return dict(Su=Su, Se=round(Se), sigma_a=round(sa, 1), sigma_m_vm=round(sm, 1), n=round(n, 2), util_vs_req15=round(1.5 / n, 3))
cases = {
    "A_4140QT_profile_key": goodman(965, 2.0, 2.6),
    "B_34CrNiMo6_QT_sled_runner_key": goodman(1000, 1.55, 2.2),
    "C_34CrNiMo6_QT_sled_runner_key_induction_hardened_seat": goodman(1000, 1.55, 2.2, k_surf_treat=1.5),
    "D_TA9415H_125_34CrNiMo6_sled_runner": goodman(1000, 1.55, 2.2, d=125.0),
}
vm_static = math.sqrt((2.0 * sig(M_seat, d))**2 + 3 * (2.6 * t_pk)**2)  # peak with Kt, vs yield
key_F = 2 * T_hprv / 0.120 / 1000
J["axle"] = dict(seat_d_mm=120, body_d_mm=130, M_EN_kNm=round(Mb_EN, 2), M_hub_kNm=round(M_hub, 2), M_seat_kNm=round(M_seat, 2), P_hub_kN=round(P_hub, 1), hung_mass_kg=round(m_hung, 1),
                 sigma_nom_MPa=round(sa_nom, 1), tau_start_MPa=round(tm_nom, 1), tau_hprv_MPa=round(t_pk, 1), vm_nom_MPa=round(math.sqrt(sa_nom**2 + 3 * t_pk**2), 1),
                 EN13103_screen=dict(perm_A1N=120, perm_A4T_class=145, util_A4T=round(math.sqrt(sa_nom**2 + 3 * t_pk**2) / 145, 3), note="EN 13103 has no keyed-seat permissible -> Shigley/Goodman fatigue with key Kf, required n >= 1.5 (ASSUMED)"),
                 fatigue=cases, required_n=1.5,
                 result="FAILS as a plain 4140 Ø120 profile keyseat (n %.2f). FIX APPLIED: 34CrNiMo6 (EN 10083-3) Q&T Rm>=1000, sled-runner keyseat 32x11 (catalog 32x11x269), induction-hardened + ground seat zone (k 1.5 ASSUMED, PE/metallurgist to confirm) -> n %.2f. TA9415H Ø125 alone gives n %.2f (rejected: +117 kg/axle, larger housing, still needs the material change)." % (cases["A_4140QT_profile_key"]["n"], cases["C_34CrNiMo6_QT_sled_runner_key_induction_hardened_seat"]["n"], cases["D_TA9415H_125_34CrNiMo6_sled_runner"]["n"]),
                 static_peak_vm_with_Kt_MPa=round(vm_static), Sy_34CrNiMo6=700, static_util=round(vm_static / 700, 3),
                 key=dict(size="32x11 keyseat x 269 (Dodge 120 mm bore), ISO key 32x18 C45", F_hprv_kN=round(key_F, 1), bearing_hub_MPa=round(key_F * 1000 / (7 * 269), 1), bearing_shaft_MPa=round(key_F * 1000 / (11 * 269), 1), allow=150),
                 fit="Dodge straight bore is a slip fit: specify shaft k6 (AWAIT Dodge), anti-fretting compound, Dodge setscrews + axial retaining collar; check key/seat for reversing traction torque at each 500 h inspection")
# ---------------------------------------------------------------- torque arm (Dodge TA rod) and anchor
J["torque_arm"] = dict(arm_m=arm, F_adhesion_kN=round(F_rod_adh, 1), F_hprv_kN=round(F_rod_hprv, 1), F_start_need_kN=round(T_need / arm / 1000, 1),
                       layout="Dodge TA rod vertical (within the +/-30 deg Dodge rule) from the housing input-end fulcrum, up to a rubber-bushed anchor bracket PL20 cantilevered 155 mm from the transom's axle-side face (Z~1,000) - classic nose suspension, rides the primary-spring motion",
                       bracket_M_kNm=round(F_rod_hprv * 1.5 * 0.155, 2),
                       weld="bracket PL20 to transom PL16: 2 x 200 x 10 fillet both sides (throat 2,828 mm2), S_weld = 2*200^2/6*7.07*... see PE C7n",
                       weld_shear_MPa=round((F_rod_hprv * 1.5 + 10 * g * 3 / 1000) * 1000 / 2828, 1),
                       weld_bending_MPa=round(F_rod_hprv * 1.5 * 0.155 * 1e6 / (2 * 7.07 * 200**2 / 6 + 2 * 7.07 * 200 * 20), 1),
                       note="Dodge TA rod itself rated by Dodge for the reducer torque (AWAIT AE for rail shock); bush the anchor end (rubber) for vertical/lateral compliance")
wv = math.hypot(J["torque_arm"]["weld_shear_MPa"], J["torque_arm"]["weld_bending_MPa"])
J["torque_arm"]["weld_resultant_MPa"] = round(wv, 1); J["torque_arm"]["weld_allow_MPa"] = 145.0
# ---------------------------------------------------------------- belt drop
T_in_adh = T_adh / (i_red * eta_red); T_in_hprv = tq_bar * p_hprv
J["belt"] = dict(T_input_adhesion_Nm=round(T_in_adh), T_input_hprv_Nm=round(T_in_hprv), sprocket_pd_mm=160, c_c_mm=195, F_eff_hprv_kN=round(2 * T_in_hprv / 0.160 / 1000, 1),
                 spec="Gates Poly Chain GT Carbon 14MGT 37-68 mm wide (catalog), rating >= %d N.m at 50-900 rpm incl. SF 1.4 -> AWAIT Gates selection" % round(T_in_hprv * 1.4),
                 why="H1B110 in line with the TA II input shaft does not fit (see packaging): the belt drop moves the motor 195 mm further from the axle so it clears the horn cheeks and passes through the open sideframe window inside the wheel line")
# ---------------------------------------------------------------- packaging (truck axle coords: axle X0 Z725; +X toward truck centre; Y lateral)
pk = dict(reducer_hub_Y=[-267.5, 2.5], reducer_radial_mm=299, reducer_input_end_X=487, input_shaft_X=229, input_shaft_end_Y_ASSUMED=100,
          inline_motor=dict(flange_Y=175, rear_Y=175 + 316.4, limit_sideframe_Y=330, limit_wheel_inner_Y=427, result="NO FIT: H1B110 SAE AA 316.4 + coupling puts the motor rear at Y491 vs sideframe 330 (X109-349 hits horn cheek X110-140) / wheel inner face 427"),
          belt_motor=dict(X=[300, 540], Z=[620, 900], Y=[105, 421], centre=[420, 760], clear_cheek_mm=300 - 140, clear_bottom_chord_mm=620 - 575, clear_top_chord_mm=1000 - 900,
                          clear_wheel_inner_face_mm=427 - 421, clear_transom_mm=625 - 540),
          disc=dict(d=340, Y=[190, 215], X_max=170, clear_to_motor_mm=300 - 170, clear_axlebox_mm=270 - 215),
          transom_clear_input_end_mm=625 - 487, reducer_top_Z=725 + 299, reducer_bottom_Z=725 - 299,
          mirror="input ends point to the truck centre on both axles of each truck (mirrored in X); reducers on Y-, discs/motors/belts on Y+ (all 4 axles)")
J["packaging"] = pk
# ---------------------------------------------------------------- brakes (governed 6 mph basis)
J["brake"] = dict(disc="Ø340x25 on the axle, Y+190..215 (side away from the reducer)", calipers="2 x spring-applied air-released per disc (ref Coremo Ocmea D 3.5N 24.2 kN) - axle torque is now 1:1 (no gear multiplication)",
                  r_eff=0.135, note="see PE B1-g: clamp per caliper with 2 calipers")
# ---------------------------------------------------------------- options compared (pros/cons; weights in kg, no prices)
J["options"] = [
    dict(id="L3 (chosen)", what="TA7315H15MS + H1B110 + 1:1 sync belt", pros="all catalog parts; adhesion-limited start at ~%d bar; 10 mph hardware capability on the existing H1P053; governed 6 mph by a hard min-displacement stop; same H1 family as the pump (one supplier/controls); no custom gears" % round(p_31),
         cons="TA II is industrial (not rail-traction rated) - Dodge AE must accept; Ø120 keyed axle seat needs 34CrNiMo6 + induction hardening; belt drop + guard to maintain; H1B has no brake (axle disc + 2 calipers); heavier (+%d kg/axle hung)" % round(m_axle_add)),
    dict(id="Fallback", what="TA7315H05MS 5.2:1 + Poclain MS05 ~280 cc (brake version)", pros="LSHT motor with built-in multi-disc brake; catalog parts", cons="Dodge must rate 5:1 below 90 rpm; ~7.4 mph flow cap on H1P053 (fine for 6 mph); MS05 length also needs the drop/space check; two suppliers"),
    dict(id="L2 (rejected)", what="custom 1.81:1 spur case + MSE05 750", pros="designed to fit; rail-style nose suspension; Ø150 seat", cons="one-off gear case (design, cutting, heat treat, inspection) - owner not keen; start η 0.78 marginal pending Poclain; 7.4 mph flow cap"),
]
json.dump(J, open("/workspace/train/calcs/L3/drive_L3.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(J, indent=1, ensure_ascii=False))

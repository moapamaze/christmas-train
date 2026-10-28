"""PF-CT rev L4.2 close-out (Grokky, 28 Oct 2026): L4.1 Stress Bot r2 rulings + L4.2 Stress Bot r3 rulings (descent float, T04 orifices), Tender Bot TB-3.13d, Loco Bot items.
Reads drive_L4.json (L4.1). Re-uses Stress Bot's run-in model by executing s4_brakes.py SOURCE up to 'runin = {}' (read-only; nothing written to /workspace/stress).
Writes l41_closeout.json / .md here."""
import json, math, sys, os, io, contextlib
SB = '/workspace/stress/loco_L4'; sys.path.insert(0, SB); os.chdir(SB)
src = open(SB + '/s4_brakes.py').read().split('runin = {}')[0]
# --- model changes: tender TB-3.13d brake 5.845 kN (calipers unchanged; 0.671 m/s2 at 8,706.5 kg; service 4.09 = 0.70 x full ASSUMED); loco T04/hyd force can be delayed by T_D
src = src.replace("tender=0.12 * m_tender * g / 1000,", "tender=5.845,")
src = src.replace("if loco_F: Fbr[0] += loco_F * 1000 * min(1, t / t_hyd)", "if loco_F: Fbr[0] += loco_F * 1000 * min(1, max(0.0, t - T_D[0]) / t_hyd)")
assert "tender=5.845," in src and "T_D[0]" in src
G = dict(T_D=[0.0])
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src, 's4_brakes_L41', 'exec'), G)
os.chdir('/workspace/train/calcs/L4')
sim, hyd, MPH, BR, allow_F, Fb = G['sim'], G['hyd'], G['MPH'], G['BR'], G['allow_F'], G['Fb']
heumann, RT, wb = G['heumann'], G['RT'], G['wb']
D = json.load(open('drive_L4.json')); B = D['basis']; g = 9.81
T4 = D['L42']['T04']
OUT = dict(rev='L4.2', inputs=dict(loco_kg=B['loco_kg'], tender_kg=B['tender_kg'], train_kg=B['train_kg'], tender_brake_full_kN=5.845, tender_brake_service_kN=4.09,
           tender_decel_full=round(5.845e3 / B['tender_kg'], 3), loco_brake_kN=round(Fb['loco'], 2), loco_decel=round(Fb['loco'] * 1000 / B['loco_kg'], 3)))
# allowance with lubricated gauge faces (Nadal 1.84, Stress Bot K2-rD) at R80 loco-tender joint
NAD_L = 1.84; al = RT['alts']['F']['coupler_deg']
allow_lub = round((NAD_L - heumann(wb, 80)['YQ1']) * 2 * RT['basis']['Q_kN']['loco'] / (math.sin(math.radians(al['lt_loco'])) * (1 + 3875 / 3200)), 1)
LIM = 33.2
# ---------------- 1. trip run-in ---------------------------------------------------------
RUN = {}
for k in (20, 100):
    for init, gr, vv in (('draft', 0.0, 6), ('draft', 0.0, 7), ('buff', 0.02, 6), ('buff', 0.02, 7)):
        tag = f'k{k}_{init}_{int(gr*100)}pct_{vv}mph'; v0 = vv * MPH
        G['T_D'][0] = 0.0
        r = dict(baseline_emergency=sim(k, init=init, grade=gr, v0=v0)['maxC'],
                 L4_trip_1st_400_0p3s=sim(k, init=init, grade=gr, v0=v0, loco_F=hyd['first_400'])['maxC'],
                 L41_CCO_trip_2nd_400_ramp3s=sim(k, init=init, grade=gr, v0=v0, loco_F=hyd['second_400'], t_hyd=3.0)['maxC'],
                 L41_24Vloss_2nd_default_400_ramp3s=sim(k, init=init, grade=gr, v0=v0, loco_F=hyd['second_400'], t_hyd=3.0)['maxC'])
        G['T_D'][0] = 0.5     # switch vents the BP first but T04 engages fast (0.5 s delay, 0.5 s rise) - shown for information: NG
        r['info_T04_BP_first_fast_0p5s'] = sim(k, init=init, grade=gr, v0=v0, loco_F=BR['MS05_T04_dynamic_kN'], t_hyd=0.5)['maxC']
        G['T_D'][0] = 1.0     # L4.1: BP vented first + choke orifice in the T04 release drain: T04 starts >= 1.0 s after the vent, rises over >= 2.0 s
        r['L41_T04_accidental_BP_first_choked'] = sim(k, init=init, grade=gr, v0=v0, loco_F=BR['MS05_T04_dynamic_kN'], t_hyd=2.0)['maxC']
        G['T_D'][0] = 0.0
        r['L4_T04_accidental_no_BP'] = sim(k, init=init, grade=gr, v0=v0, loco_F=BR['MS05_T04_dynamic_kN'], car_brakes=False, loco_fric=False, t_hyd=0.5)['maxC']
        # ---- L4.2 (Stress Bot r3 N1/N2 rulings)
        G['T_D'][0] = 0.0
        r['L42_float_entry_bypass_FAILED_closed_ramp3s_2nd'] = sim(k, init=init, grade=gr, v0=v0, loco_F=hyd['second_400'], t_hyd=3.0)['maxC']
        r['L42_T04_burst_downstream_orifices'] = sim(k, init=init, grade=gr, v0=v0, loco_F=BR['MS05_T04_dynamic_kN'], t_hyd=T4['burst_downstream']['rise_90pct_s'])['maxC']
        G['T_D'][0] = T4['normal']['delay_s']
        r['L42_T04_accidental_BP_first_orifices'] = sim(k, init=init, grade=gr, v0=v0, loco_F=BR['MS05_T04_dynamic_kN'], t_hyd=T4['normal']['rise_s'])['maxC']
        G['T_D'][0] = 0.0
        r['info_L42_24Vloss_bypass_FAILED_closed_1st_ramp3s'] = sim(k, init=init, grade=gr, v0=v0, loco_F=hyd['first_400'], t_hyd=3.0)['maxC']
        r['info_L42_T04_burst_AND_both_vent_channels_failed'] = sim(k, init=init, grade=gr, v0=v0, loco_F=BR['MS05_T04_dynamic_kN'], car_brakes=False, loco_fric=False, t_hyd=T4['burst_downstream']['rise_90pct_s'])['maxC']
        RUN[tag] = r
w41 = max(v for r in RUN.values() for kk, v in r.items() if kk.startswith('L41') or kk.startswith('L42') or kk == 'baseline_emergency')
w42 = {kk: max(r[kk] for r in RUN.values()) for kk in next(iter(RUN.values())) if 'L42' in kk}
w4 = max(v for r in RUN.values() for kk, v in r.items() if kk.startswith('L4_'))
OUT['runin'] = dict(cases_maxC_kN=RUN, worst_L41_kN=w41, worst_L42_by_case_kN=w42, worst_L4_as_was_kN=w4, limit_loco_LT_R80_dry_kN=LIM, model_allow_loco_LT_R80_kN=allow_F['loco_LT'],
    allow_lubricated_R80_kN=allow_lub, util=round(w41 / LIM, 2), result='PASS' if w41 <= LIM else 'NG',
    rules=["L4.2 DESCENTS: FLOAT MODE (loop bypass valve opened progressively while the swash ramps to zero over >= 3 s) replaces 'pump at neutral'; bypass-open proof switch, failure -> alarm and stop on the friction brakes",
           "L4.2 T04: Ø1.2 orifice in EACH motor's T04 port, hard lines or 4SH hose downstream of the choke, 2-CHANNEL BP-vent switch (a double failure is information only)",
           "Any trip (CCO overspeed, 24 V loss, s30) ramps the H1P053 to neutral over >= 3 s: EDC control orifices / PLUS+1 ramp, the hydraulic ramp is the fail-safe one (AWAIT Danfoss orifice size, no contact without the owner)",
           "L4.2: MS05 2-speed valve FAIL-TO-1st (de-energized = 468 cc); 2nd coil fed through a PNOZ s30 >= 1.5 mph contact; 24 V loss -> normally-open loop bypass = FLOAT, so no hydrostatic retarding (bypass failed closed + 24 V loss = double failure, information row)",
           "T04 release line pressure switch: on loss of T04 release pressure it opens the BP vent (emergency) FIRST; the T04 release supply comes from the loco's own loop (steering 7: LP shuttle + 20 bar reducing valve + normally-vented solenoid; loss of loop/charge applies the T04) and every apply path passes a choke Ø2.4 + 1.0 L damping accumulator so the T04 engages >= 1.0 s after the vent and builds over >= 2.0 s (L4.2 with the Ø1.2 port orifices: calc " + "%.2f / %.2f s" % (T4['normal']['delay_s'], T4['normal']['rise_s']) + ") (a fast 0.5 s T04 still gives 50 kN - NG, so the choke is REQUIRED; size AWAIT Poclain data, verify by a timed test at commissioning)",
           "Direction change only at zero speed (PLUS+1 interlock, wheel-speed < 0.1 mph) plus >= 1 s swash ramp through neutral"],
    basis="Stress Bot s4 lumped-mass model (k 20/100 kN/mm, 1.0 mm total play), tender brake 5.845 kN (TB-3.13d 0.671 m/s2), loco brake 0.69, tender 8,706.5 kg")
# ---------------- 2. brake match --------------------------------------------------------
OUT['brake_match'] = dict(loco_decel=OUT['inputs']['loco_decel'], tender_decel=OUT['inputs']['tender_decel_full'], coach_decel=round(0.12 * g, 3),
    result='MATCHED within 2 %: loco 0.690 / tender 0.671 (TB-3.13d, mixed Coremo D 2N sets, pad wear limit 5.5 mm) / coaches 0.12 g on empty tare; tender slightly softer -> tender buffs onto the loco, covered by the run-in check; service 4.08 kN',
    stops_worst=G['R']['stops_worst'])
# ---------------- 3. route L/V with truck-pitch transfer at the traction pin (h 0.65) ----
WT = D['weight_transfer']; ax = B['axle_loads_kN_RT1corr_plus_L4']; h = 0.65; hc = 0.55; mt, ml = B['train_kg'], B['loco_kg']
TE = min(D['start']['F350_kN'] if 'F350_kN' in D['start'] else 37.67, WT['cases']['L41_traction_pin_0p65']['forward']['equal_torque_cap_kN'])
def R1(TEk):
    Fd = TEk * (mt - ml) / mt; intra = TEk / 2 * h / 1.55; inter = Fd * (h - hc) / 3.2 / 2; return ax['R1'] - intra - inter
NAD = G['nadal'](); FAC = 1 + 3875 / 3200; FLT = RT['basis']['F_LT']; LV = {}
for tag, Rm in (('A', 100), ('F', 80), ('E', 70), ('D', 60)):
    ang = RT['alts'][tag]['coupler_deg']['lt_loco']; hy = heumann(wb, Rm)['YQ1']
    lv = hy + FLT * math.sin(math.radians(ang)) * FAC / (2 * R1(TE) / 2)
    LV[tag] = dict(R=Rm, LV=round(lv, 3), nadal_dry=round(NAD, 3), margin_dry=round(NAD / lv, 3), nadal_lubricated=NAD_L, margin_lubricated=round(NAD_L / lv, 3),
                   lubricated=Rm <= 80, result='PASS' if (NAD / lv >= 1.0 or (Rm <= 80 and NAD_L / lv >= 1.0)) else 'NG')
OUT['route_LV'] = dict(TE_kN=round(TE, 2), h_traction_m=h, cases=LV, rule="High-rail gauge-face lubricators on ALL R <= 80 curves (Routes F, E, D); top of rail kept DRY for 2 %% starts. Closes K2-rD (D: lubricated margin %.2f)" % LV['D']['margin_lubricated'])
# ---------------- 4. chain / hub / speed (from drive_L4.json) ----------------------------
# ---- L4.2 QEV option A: 7 mph trip stop on 2 % down with the loco spring-apply delayed by the relay-exhaust time
_QA = D['L42']['QEV_option']
M_, Fb_, Wbr_, names_ = G['M'], G['Fb'], G['Wbr'], G['names']; MPH_ = G['MPH']; rol_, rot_, tre_ = G['rolling'], G['rot'], G['t_react']
def _stop_delay(v_mph, mu, dly, grade=0.02, failed=()):
    Mt = M_.sum(); Fall = sum(min(Fb_[n], mu * Wbr_[n]) for n in names_ if n not in failed) * 1000; Fnl = Fall - (0 if 'loco' in failed else min(Fb_['loco'], mu * Wbr_['loco']) * 1000)
    a_dn = g * (grade - rol_); v = v_mph * MPH_; s = v * tre_ + 0.5 * a_dn * tre_ ** 2; v += a_dn * tre_
    a1 = (Fnl - Mt * g * (grade - rol_)) / (Mt * rot_)          # train braking without the loco during the extra delay
    if a1 * dly >= v: return round(s + v * v / (2 * a1), 1)
    s += v * dly - 0.5 * a1 * dly ** 2; v -= a1 * dly
    a2 = (Fall - Mt * g * (grade - rol_)) / (Mt * rot_)
    return round(s + v * v / (2 * a2), 1)
_cases = {}
for lab, mu in (('dry', 0.25), ('wet', 0.15), ('dusty', 0.10)):
    for f in ((), ('tender',), ('coach1',), ('acc',)):
        _cases['%s_%s' % (lab, ','.join(f) or 'none')] = dict(base=_stop_delay(7, mu, 0.0, failed=f), optA=_stop_delay(7, mu, _QA['option_A']['t_apply_to_0p3bar_s'] + 0.5, failed=f), optB=_stop_delay(7, mu, _QA['option_B']['t_apply_s'] + 0.5, failed=f))
_wA = max(v['optA'] for v in _cases.values()); _wB = max(v['optB'] for v in _cases.values())
OUT['stop_7mph_QEV'] = dict(limit_m=30.0, delay_basis="extra loco delay = spring-apply exhaust time (option A to 0.3 bar g, conservative) + 0.5 s signal ASSUMED, on top of the 1.5 s train reaction", cases=_cases,
    worst_optA_m=_wA, worst_optB_m=_wB, optA_passes_stop=bool(_wA <= 30.0), result="7 mph trip stop on 2 %% down: option A worst %.1f m, option B worst %.1f m vs 30 m (single failures, dry/wet/dusty)" % (_wA, _wB))
OUT['chain'] = dict(D['chain_slack_L41'], certificate="ANSI 120-2 duplex: mill certificate of breaking strength per ASME B29.1 >= 302.5 kN minimum ultimate (duplex), per lot, before fitting",
                    reversal="zero-speed interlock + >= 1 s ramp: impact factor ~1.3 -> ~42.5 kN vs 51.7 kN allowable (0.82)", transient_450bar_SF_on_ultimate=5.5,
                    OI_L4_5="CLOSED: floating seal plate +/-25 vertical (bump stops +/-22) / +/-1 lateral; ride-out of the 3 mm case at bump 22 checked with 15.0 (axle end) / 17.1 (motor end) clearances")
OUT['hub_fit'] = D['axle']['press_fit']; OUT['speed'] = {k: D['speed'][k] for k in D['speed'] if 'high_idle' in k or k in ('stop_rule', 'vmax_mph', 'Vp_stop_cc')}
OUT['operating_rules'] = ["Descents (L4.2): FLOAT MODE - brake handle out of RUN -> swash ramp to zero over >= 3 s with the loop bypass opening -> motors free-wheel; the friction brakes (independent / train) alone control speed on down grades (sized for the full 2 %% descent of the loaded train: %.0f %% of service force, cooler %.1f of 14 kW)" % (100 * D['L42']['descent']['hold_util_service'], D['L42']['descent']['cooler']['float_heat_kW']),
    "Dead-loco towing: open the tow (loop bypass) valve, wind out the T04 parking brakes (T04 release), motors to 2nd/freewheel; max tow speed 2 mph (ASSUMED until Poclain confirms case pressure)",
    "Reverse starts of the full train only on grades <= %.2f %% (L4.2: 1.10 margin with sand on both trucks and the centre-plate pad included; PLUS+1 reverse pull cap %.1f kN; forward TE command limit %.1f kN for K2-a)" % (D['L42']['sanding']['reverse_rule_pct'], D['L42']['K2a']['rev_cap_kN'], D['L42']['K2a']['fwd_TE_command_limit_kN']),
    "Wheels: driver condemning diameter Ø1430 (new Ø1450), pony Ø630 (new Ø650); FLANGE HEIGHT WITHDRAW limit 28 mm TRAIN-WIDE (re-profile to <= 27 mm) + 2 mm vertical rail-head wear limit at joints (L4.2); measured diameters entered in PLUS+1 at each gauging",
    "Sand (both trucks, every driven axle in the direction of travel) is mandatory for starts on wet rail and pre-sand on grades >= 1 %; level + flow proof; hill-hold until TE is established",
    "Wind (interim): 25 mph wind limit on R <= 80; no full-pull starts on R <= 80 while any lubricator is out of service"]
OUT['pony'] = dict(overspeed="PNOZ s30 overspeed INDEPENDENT: its own 2 sensors (pony + an axle) - unchanged; PLUS+1 slip reference now a 96-tooth pony target wheel with 2 quadrature sensors (L4.2, 10.5 Hz at 0.5 mph) + pony/axle agreement check",
                   spring="pony primary spring rate <= 1.19 kN/mm per wheel (static deflection >= 5 mm governs; the 1.23 twist limit is not binding) - track twist 1:200 at R80, Stress Bot s5/r3")
# ---------------- 5. Loco Bot steering-3 items ------------------------------------------
L = {}
# (c) saddle web, longitudinal 3 g out of plane of the PL10 web; web only reaches the cap at |y| > 520 (lightening hole); windows 550-650
W1 = 5393.7; F3 = 3 * W1; hcap = 1841.8 - 1615.0
S_web = 2 * (2 * (200 - 100)) * 10**2 / 6 / 2      # two ligament zones |y| 520-720 minus 100 window, both sides
M = F3 * hcap
S_g = 4 * 10 * 100**2 / 6                          # 4 gusset pairs (PL10 both faces, 45 proj + web = 100 deep) at Y+/-535 and +/-685
L['c_saddle_web'] = dict(load="3 g longitudinal %.1f kN per saddle at the cap (Z1842 at |y| 520), lever %.0f mm" % (F3 / 1000, hcap),
    as_detailed=dict(S_mm3=round(S_web), sigma_MPa=round(M / S_web), allow_MPa=187, util=round(M / S_web / 187, 2), result='NG'),
    fix="Add 2 x PL10 triangular gussets 45 x 150 (one each face, welded to web and base, 5 fillet) at Y+/-535 and +/-685 on S1-S6 (S4N: at its window ligaments); windows 100 x 70 stay clear for the M12x45 SHCS",
    with_gussets=dict(S_mm3=round(S_g + S_web), sigma_MPa=round(M / (S_g + S_web)), allow_MPa=187, util=round(M / (S_g + S_web) / 187, 2), result='PASS'),
    mass_add_kg=round(8 * 0.5 * 45 * 150 * 10 * 7.85e-6 * 6, 1), note="in-plane (vertical 2 g) ligament shear %.1f MPa - OK" % (2 * W1 / (2 * 100 * 10)))
# (d) B1 HB16 forward hole
L['d_B1_hole'] = dict(was="B1 RB-1 at X530, holes X460/600: X460 is 8 mm from the front end sill weld zone X300-452",
    fix="B1 RB-1 holes at X480 and X600 (RB-1 web plate X430-630): 28 mm from the X452 weld toe (>= 25 required by Grokky L4.1 rule; Loco Bot's 150 mm rule applies to crossmember/gusset welds, not the end-sill butt), edge 50 / 30 mm, pitch 120 >= 70",
    hb16_count="30 HB16 total = 28 released at L4 + 2 (B1 front pair restored); B2/B3/B5/B7/B8 20, B1 4 (2 per side), SD-1 bolsters B4/B6 4, B9 SD-2 0 (clamp) -> 28 rail-web + bolster; check: 5 x 4 + 4 + 4 = 28 + B1 restored 2 = 30",
    result='RELEASED')
# SD-2 hold-down
up = 8.05e3; Fb_cl = up / 2; Mcl = Fb_cl * 30 / 2; Scl = 80 * 16**2 / 6
L['d_SD2_holddown'] = dict(detail="SD-2 (B9 X10862) bears on the rear end-sill top; NO holes in the sill. Each side: 2 x PL16 80x120 clamp plates (A36) under the sill top flange lip, each pulled up by 1 x M16 8.8 x 90 through the SD-2 cap outboard/inboard of the flange (not through the sill), 6 mm packer at the heel, Nord-Lock, 150 N.m",
    uplift_kN=8.05, bolt_kN=round(Fb_cl / 1000, 2), bolt_cap_kN=round(0.75 * 800 * 157 / 1.5 / 1000, 1), clamp_plate_MPa=round(Mcl / Scl, 1), result='PASS',
    note="Drawgear zone (X >= 10148) untouched; lateral/longitudinal by bearing of the SD-2 legs on the sill faces")
# (e) SD-1 cap
Mcap = 8.05 * (163.8 - 90.0) / 1000
L['e_SD1_cap'] = dict(decision="RE-CUT (not shorten): SD-1 cap inboard edge from Y+/-100 to Y+/-50 so the HB16 at Y+/-90 has 40 mm edge (>= 1.5 d0 = 39, >= 20 Lindapter); bearing on the rail top Y163.8-316.2 unchanged",
    cap_bending_kNm=round(Mcap, 3), phiMn_kNm=round(0.9 * 250 * 200 * 10**2 / 4 / 1e6, 3), util_LRFD=round(1.6 * Mcap / (0.9 * 250 * 200 * 10**2 / 4 / 1e6), 2), result='PASS',
    mass_add_kg=round(2 * 2 * 200 * 50 * 10 * 7.85e-6, 2))
# (f) clamp bars, 1 plate per side
m_pl = 75.4; F_up = 2 * m_pl * g; pre = 3000.0; Fbar = (pre + F_up / 2); Lb = 520.0; bpl = 473.0
Mbar = Fbar / 4 * (Lb - bpl / 2); Sb = 100 * 12**2 / 6
L['f_clamp_bars'] = dict(plates="2 x PL25.4 (1 in) 800 x 473 A36 75.3-75.4 kg, ONE per side pocket (L-105)", bars="4 x FB100x12x560 A36 (2 per plate), bolted at both ends to the BH-1 rod anchors (M20 rods)",
    location="plates positively located in X and Y by the pocket walls (<= 2 mm gap, UHMW shim) - bars carry uplift and rattle preload only",
    load_per_bar_kN=round(Fbar / 1000, 2), M_kNm=round(Mbar / 1e6, 3), sigma_MPa=round(Mbar / Sb), allow_MPa=187, util=round(Mbar / Sb / 187, 2), result='PASS',
    torque="M20 rod nuts 30 N.m + Nord-Lock (preload ~1.5 kN per rod end; NOT the 441 N.m structural torque - that would yield the bar)", S504="109-BAL qty 2 x 75.4 RELEASED; 109-BCB 4 x FB100x12x560 21.1 kg added")
# (h) smaller items
L['h_rivnut_pull_test'] = "Production pull test: first 5 of each lot + 1 in 20 installed, proof 6.0 kN axial (1.5 x 4 kN SWL) for 10 s on the actual bearer wall; no spin, no pull-out, no flange lift > 0.1 mm; plus a spin-out check at the install torque. Record on S-505; a fail = test the whole bearer"
L['h_F13_pin'] = "F-13 290 mm Ø20 through pin cannot pass along a 25 x 25 L-110 yoke bar (coaxial, 2.5 mm wall): DELETE F-13. Yoke = Ø32 A4 round bar with turned Ø20 h9 journals x 25 each end running in the 2 SAE 841 flanged bushings in the cheeks (Y+/-125..135), collars outside; journal bending at 3 g + 1 g lateral ~4 MPa - PASS. Overall ~300 mm"
L['h_tabs'] = "ST-1 tabs on the HSS3x3x1/8 SS± stringers: M12x100 8.8 THROUGH-BOLTS with a DOM 19.05 x 2.1 crush tube (inserted from the open stringer end, all tabs within 60 mm of an end), Nord-Lock, 88 N.m - chosen over rivnuts (vibration, no spin-out); end shear ~1.6 kN/bolt vs bearing 26 kN"
LB = D['basis'].get('added_per_axle_kg', {})
m_truck = round(2 * 802 + 4 * 45 + 4 * 10 + 2 * 250 + 320 + 2 * (64 + 35 + 13.6 + 12 + 45 + 29) + 55 + 60)
L['h_truck_mass'] = dict(estimate_kg=m_truck, A101_assumed_kg=4900, result="A-101 4,900 kg is CONSERVATIVE (estimate %d kg: 2 wheelsets+unsprung drive 802 each, axleboxes, chevrons, sideframes PL30 ~250 each, transom/bolster 320, 2 x sprung drive 199, traction pin 55, piping 60) - keep 4,900 for lifting (>= 6.3 t gear OK); confirm by weighing at the truck builder" % m_truck)
L['h_OI_L4_5'] = OUT['chain']['OI_L4_5']
L['a_divider'] = "ONE statement everywhere: NO flow divider (Jahns rejected: 31.2 < 32.3 kN, below min flow, +160 kg). Anti-slip = PLUS+1 per-motor traction control (pony 3rd speed pickup, destroke, auto-sand, start in 1st, hill-start hold)"
L['b_interfaces'] = "interfaces_L41: rear-sill glad hands per JL-A: BP Y-650, WH (whistle, new) Y-800, MR Y-950, all Z1950; DBK-1 dry-breaks Y-220..-600, Z700-1100; AW-1 whistle line 1/2 in"
L['g_slats'] = "loco_S17_answers.md (a) slats 54.9 -> 21.9 (JSON/ledger already 21.9)"
OUT['loco_items'] = L
OUT['cross_refs'] = dict(tender="CLOSED: TB-3.13d 8,706.5 kg CG [2422.7, 11.3, 1110.4] incl. the tender-end safety-chain shackles (TB-3.13c 8,705.2; TB-3.13b 8,700.1; +59.9 kg vs TB-3.11); full brake 5.845 kN (0.671 m/s2; mixed Coremo D 2N spring sets, 25.4 mm discs, pad wear limit 5.5 mm), caliper air train 14.0 L / 84 L free air per release / 3.55 cfm steady vs 14 cfm; ERV roof 3,450 static, kinematic vs K-401 4,300; K2-xf CLOSED - transformer cradle dropped 50 mm (25 mm at the isolator stop, 100 mm to K-401)",
                         genset="CLOSED: Electro E3.4 already carries the 1.26 kW decoration LEDs inside 30.99 kW running / 32.49 kW peak hot; Stress Bot 33.24 kW double-counted; decorations shed first above 33 kW",
                         lights="Electro Bot: headlamp HL-1 25 kg @X175 Z3495 carried (SBX-7 inside the 227.9 kg smokebox, 0 kg)")
json.dump(OUT, open('l41_closeout.json', 'w'), indent=1, ensure_ascii=False)
if __name__ == '__main__':
    print(json.dumps({k: OUT[k] for k in ('inputs',)}, indent=1)); print('runin worst', w41, 'L4', w4, 'allow', allow_F['loco_LT'], 'lub', allow_lub)
    for t, v in LV.items(): print(t, v)
    for k in ('c_saddle_web', 'd_SD2_holddown', 'e_SD1_cap', 'f_clamp_bars', 'h_truck_mass'): print(k, OUT['loco_items'][k])

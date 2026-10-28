"""Builds route_check.json + route_check.md from route_sweep.json (kinematic sweep) + Heumann curving + coupler L/V.
Rev RT1 28 Oct 2026 - PF-CT R2 vehicle set (model.py), K-401 half-envelope 1,696 / fixed objects 2,000."""
import json, math
from heumann import heumann, nadal
D = json.load(open("/workspace/train/calcs/track/route_sweep.json"))
import os
if os.path.exists("/workspace/train/calcs/track/route_sweep_extra.json"):
    E = json.load(open("/workspace/train/calcs/track/route_sweep_extra.json"))
    D["cases"].update(E.get("cases", {})); D["alts"].update(E.get("alts", {}))
LC = json.load(open("/workspace/train/calcs/track/loco_check.json"))
GARLAND = 60.0                       # Trim Bot: garland / light strings per coach side (28 Oct)
def widen(R):                        # track_structure gauge widening (36-1/4 in R45-50, 36-1/8 in R50-75) + 3 mm build tol -> extra one-sided shift
    return (920.7 - 914.4 + 3) if R <= 50 else ((917.5 - 914.4 + 3) if R <= 75 else 0.0)
# STEADY drawbar angle vs each body (corrected - K1-a used (o + DB/2)/R, which omits the half pivot spacing and the pin-offset term):
#   theta_A = (xA + DB/2)/R + (yA - yB)/DB,  xA = pivot-centre-to-pin, yA = (xA^2 - sA^2)/2R (pin offset outward of track centre)
def steady(xA, sA, xB, sB, DB, R):
    R = R * 1000.0; yA = (xA**2 - sA**2) / (2 * R); yB = (xB**2 - sB**2) / (2 * R)
    tA = (xA + DB / 2) / R + (yA - yB) / DB; tB = (xB + DB / 2) / R + (yB - yA) / DB
    return math.degrees(abs(tA)), math.degrees(abs(tB))
SC = json.load(open("/workspace/train/calcs/track/start_curve.json"))
NAD = nadal(70, 0.3); ENV = 1696.0; PLAY = 6.2
Q = dict(loco=18.96, tender=10.18, coach_e=9.86, coach_l=16.19)
FAC = dict(loco=1 + 3875 / 3200, tender=1 + 1200 / 2600, coach=1 + 2437 / 5486)
F_LT = 29.4; F_C1 = 24.1; F_TE = 37.9; F_BUFF = 10.0
POCK = D["pocket"]
def lv_inc(F, a_deg, fac, q): return F * math.sin(math.radians(a_deg)) * fac / (2 * q)
def rowR(name, R):
    c = D["cases"][name]; r = c["res"]; cp = c["cpl"]
    hl = heumann(1.55, R); hc = heumann(1.2, R); hlt = heumann(1.05, R)
    coach_a = max(x["a_front"] for x in cp[1:]) ; coach_a = max(coach_a, max(x["a_rear"] for x in cp[1:]))
    lt_l = cp[0]["a_front"]; lt_t = cp[0]["a_rear"]
    # steady (body-centred) coupler angle ~ half the overhang chord angle - used for the "with 10 m spirals" estimate
    st_coach = steady(5180, 2743, 5180, 2743, 1473, R)[0]
    st_lt_l, st_lt_t = steady(5475, 1600, 2500, 1300, 800, R)
    k1a_old = math.degrees((2437 + 1473 / 2) / (R * 1000))
    yaw = c["yaw"]; ccoach = max(v for k, v in yaw.items() if k.startswith("Coach"))
    vers = 1550**2 / (8 * R * 1000); lead_l = 650 / 2 * math.tan(math.radians(70)) * (1550 / 2 / (R * 1000)) * 0 + 47.8 * 50 / R
    feff = (1550 + 2 * lead_l)**2 / (8 * R * 1000)
    out = dict(R=R,
        env_loco_out=r["Locomotive"]["out"], env_loco_out_nm=r["Locomotive"]["out_nm"], env_loco_low_out=r["Locomotive"]["low_out"], env_loco_in=r["Locomotive"]["inn"],
        env_tender_out=r["Tender"]["out"], env_coach_out=max(r[k]["out"] for k in r if k.startswith("Coach")), env_coach_in=max(r[k]["inn"] for k in r if k.startswith("Coach")),
        env_coach_low_out=max(r[k]["low_out"] for k in r if k.startswith("Coach")),
        yaw_loco=yaw["Locomotive T1"], yaw_tender=yaw["Tender T1"], yaw_coach=ccoach, driver_sweep=1500 * math.sin(math.radians(yaw["Locomotive T1"])),
        lead_swing=c["lead"]["swing"], lead_arm_deg=c["lead"]["arm_angle"],
        cyl_gap=c["cyl_gap"] - PLAY, cyl_gap_790=c["cyl_gap_790"] - PLAY,
        cpl_lt_loco=lt_l, cpl_lt_tender=lt_t, cpl_coach=coach_a, pocket_tender_util=lt_t / POCK["tender"], pocket_loco_util=lt_l / POCK["loco_rear"], pocket_coach_util=coach_a / POCK["coach"],
        versine=vers, versine_eff=feff, play=12.4, play_tol=9.4,
        YQ_loco=hl["YQ1"], YQ_coach=hc["YQ1"], YQ_lead=hlt["YQ1"],
        LV_coach_empty=hc["YQ1"] + lv_inc(F_C1, coach_a, FAC["coach"], Q["coach_e"]),
        LV_coach_empty_buff=hc["YQ1"] + lv_inc(F_BUFF, coach_a, FAC["coach"], Q["coach_e"]),
        LV_coach_empty_TE=hc["YQ1"] + lv_inc(F_TE, coach_a, FAC["coach"], Q["coach_e"]),
        LV_tender=hc["YQ1"] + lv_inc(F_LT, lt_t, FAC["tender"], Q["tender"]),
        LV_loco=hl["YQ1"] + lv_inc(F_LT, lt_l, FAC["loco"], Q["loco"]),
        LV_coach_empty_spiral=hc["YQ1"] + lv_inc(F_C1, st_coach, FAC["coach"], Q["coach_e"]),
        LV_tender_spiral=hc["YQ1"] + lv_inc(F_LT, st_lt_t, FAC["tender"], Q["tender"]),
        LV_loco_spiral=hl["YQ1"] + lv_inc(F_LT, st_lt_l, FAC["loco"], Q["loco"]),
        st_coach=st_coach, st_lt_loco=st_lt_l, st_lt_tender=st_lt_t, k1a_formula_deg=k1a_old,
        env_coach_out_garland=max(r[k]["out"] for k in r if k.startswith("Coach")) + GARLAND, widen_extra=widen(R),
        env_loco_out_widened=r["Locomotive"]["out"] + widen(R), env_coach_garland_widened=max(r[k]["out"] for k in r if k.startswith("Coach")) + GARLAND + widen(R),
        body_rel_deg=max(x["body"] for x in cp), chain_open_450=450 * math.sin(math.radians(max(x["body"] for x in cp))),
        lead_LV_free=hlt["YQ1"], lead_Q=LC["mass"]["lead_wheel_kN"],
        lead_Fc_allow=(NAD / 1.2 - hlt["YQ1"]) * LC["mass"]["lead_wheel_kN"],
        nadal=NAD, interf=c["inter_vehicle"][:3], all_interf=c["interf"][:4])
    return out
RAD = {}
for R in (125, 100, 90, 80, 70, 60, 50, 45, 40, 35):
    if f"const_R{R}" not in D["cases"]: continue
    RAD[R] = rowR(f"const_R{R}", R)
SC_ = {}
for k, c in D["cases"].items():
    if k.startswith("S_") or k.startswith("B_"):
        cp = c["cpl"]
        SC_[k] = dict(cpl_coach=max(max(x["a_front"], x["a_rear"]) for x in cp[1:]), cpl_lt_loco=cp[0]["a_front"], cpl_lt_tender=cp[0]["a_rear"],
                      env_loco_out=c["res"]["Locomotive"]["out"], env_coach_out=max(c["res"][q]["out"] for q in c["res"] if q.startswith("Coach")),
                      inter_vehicle=c["inter_vehicle"][:2], cyl_gap=c["cyl_gap"] - PLAY, lead_swing=c["lead"]["swing"],
                      body_rel_deg=max(x["body"] for x in cp))
        Rm = min(float(t[1:]) for t in k.split("_") if t.startswith("R"))
        hc = heumann(1.2, Rm); hl = heumann(1.55, Rm); x = SC_[k]; x["Rmin"] = Rm
        x["LV_coach_empty"] = hc["YQ1"] + lv_inc(F_C1, x["cpl_coach"], FAC["coach"], Q["coach_e"])
        x["LV_tender"] = hc["YQ1"] + lv_inc(F_LT, x["cpl_lt_tender"], FAC["tender"], Q["tender"])
        x["LV_loco"] = hl["YQ1"] + lv_inc(F_LT, x["cpl_lt_loco"], FAC["loco"], Q["loco"])
ALT = {}
for t, c in D["alts"].items():
    cp = c["cpl"]; r = c["res"]
    ALT[t] = dict(L_m=c["L_m"], env_loco_out=r["Locomotive"]["out"], env_coach_out=max(r[q]["out"] for q in r if q.startswith("Coach")),
                  env_coach_in=max(r[q]["inn"] for q in r if q.startswith("Coach")), cpl_lt_loco=cp[0]["a_front"], cpl_lt_tender=cp[0]["a_rear"],
                  cpl_coach=max(max(x["a_front"], x["a_rear"]) for x in cp[1:]), lead_swing=c["lead"]["swing"], lead_arm_deg=c["lead"]["arm_angle"],
                  cyl_gap=c["cyl_gap"] - PLAY, cyl_gap_790=c["cyl_gap_790"] - PLAY, inter_vehicle=c["inter_vehicle"][:3],
                  start=SC["alts"].get(t), body_rel_deg=max(x["body"] for x in cp), yaw=c["yaw"],
                  env_coach_out_garland=max(r[q]["out"] for q in r if q.startswith("Coach")) + GARLAND)
# smallest radius cleared (pass = everything incl. L/V without spirals at realistic forces; and with the listed fixes + spirals)
def passes(x, fixed=False):
    env = (x["env_loco_out_widened"] if not fixed else x["env_loco_out"] + min(x["widen_extra"], 6.0)) <= ENV and x["env_coach_garland_widened"] <= ENV
    cyl = (x["cyl_gap_790"] if fixed else x["cyl_gap"]) >= 10
    pock = x["pocket_tender_util"] * (POCK["tender"] / POCK["tender_fix150"] if fixed else 1) <= 1 and x["pocket_loco_util"] <= 1 and x["pocket_coach_util"] <= 1
    lv = (max(x["LV_coach_empty_spiral"], x["LV_tender_spiral"], x["LV_loco_spiral"]) if fixed else max(x["LV_coach_empty"], x["LV_tender"], x["LV_loco"])) <= NAD
    vs = x["versine_eff"] <= x["play_tol"]
    return dict(env=env, cyl=cyl, pocket=pock, lv=lv, versine=vs, all=env and cyl and pock and lv and vs)
for R, x in RAD.items():
    x["pass_asis"] = passes(x); x["pass_fixed"] = passes(x, True)
OUT = dict(rev="RT1 28 Oct 2026", basis=dict(envelope_half=ENV, fixed_obj=2000, nadal=NAD, play=PLAY, Q=Q, FAC=FAC, F_LT=F_LT, F_C1=F_C1, F_TE=F_TE, F_BUFF=F_BUFF, pocket=POCK),
           radii=RAD, s_curves=SC_, alts=ALT,
           min_R_asis=min([R for R, x in RAD.items() if all(RAD[r]["pass_asis"]["all"] for r in RAD if r >= R)], default=None),
           min_R_fixed=min([R for R, x in RAD.items() if all(RAD[r]["pass_fixed"]["all"] for r in RAD if r >= R)], default=None))
json.dump(OUT, open("/workspace/train/calcs/track/route_check.json", "w"), indent=1, default=float)
for R, x in RAD.items():
    print(R, {k: (round(v, 2) if isinstance(v, float) else v) for k, v in x.items() if k not in ("interf", "all_interf", "env_loco_out_nm")})
print("S", json.dumps(SC_, default=float)[:3000]); print("ALT", json.dumps(ALT, default=float)[:3000]); print(OUT["min_R_asis"], OUT["min_R_fixed"])

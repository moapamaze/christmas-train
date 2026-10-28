"""F25 drive option comparison (rev L1 running gear, Ø1,450 drivers). Comparison only - model.py drive unchanged.
Sources: Poclain selection guide 2026 / MS08 catalog 801478189C (tables in /workspace/train/vendor), Danfoss H1P 045/053
and 060/068 technical data, Tsubaki roller chain catalog (max allowable load), Kubota engine pages, plan LT18/LT23-LT25,
render check renders_work/traction.py (resistance constants). ASSUMED / AWAIT marked."""
import json, math
D = 1450.0; R = D / 2000                      # m
W = 77.944 * 9.80665                          # kN, T2 train
F_S2, F_L0, F_R2, F_RL = 0.0408142 * W, 0.0196113 * W, 0.025 * W, 0.005 * W
W_DRV = 143.3; MU_DRY, MU_WET = 0.25, 0.15
ADH_DRY, ADH_WET = W_DRV * MU_DRY, W_DRV * MU_WET
P_START = 350.0                               # bar, working start pressure basis (C13)
MPH = 0.44704
V_TOP = 7.5 * MPH
def wrpm(v): return v / (math.pi * D / 1000) * 60
N_TOP = wrpm(V_TOP)
ENG_RPM = 2600; ETA_V = 0.95
PUMPS = {"H1P045": (45.0, 420, 450), "H1P053": (53.8, 380, 400), "H1P060": (60.4, 420, 450)}   # cc, max working, peak (Danfoss)
def qpump(cc): return cc * ENG_RPM * ETA_V / 1000
# Poclain (selection guide 2026, Classic): max p, disp, 2nd disp, max rpm 1st/2nd, max kW, shaft-motor Ø, L2 max, mass max
MOT = {"MSE05 750": dict(pmax=400, cc=750, cc2=375, n1=250, n2=300, kw=29, dia=300, L2=370, kg=55),
       "MS05 560": dict(pmax=450, cc=560, cc2=280, n1=350, n2=360, kw=29, dia=300, L2=370, kg=55),
       "MSE08 1146": dict(pmax=400, cc=1146, cc2=573, n1=125, n2=110, kw=41, dia=335, L2=418, kg=85),
       "MSE08 1248": dict(pmax=400, cc=1248, cc2=624, n1=125, n2=110, kw=41, dia=335, L2=418, kg=85),
       "MS11 1259": dict(pmax=450, cc=1259, cc2=630, n1=200, n2=200, kw=50, dia=375, L2=458.5, kg=114)}
def start_force(n, cc, ratio, eta_m, eta_d=1.0, p=P_START):
    return n * p * cc / (20 * math.pi) * eta_m * ratio * eta_d / R / 1000
def rim_power(p_shaft, flow, eta_d):           # LT25 method: pump 0.855, motor 0.855 (0.90 x 0.95), 10 bar circuit
    return (p_shaft * 0.855 - 10 * flow / 600) * 0.855 * eta_d
def flow_at(v, n, cc, ratio): return n * cc / 1000 * wrpm(v) * ratio / ETA_V
def bal_speed(p_shaft, n, cc, ratio, eta_d, F):
    v = 1.0
    for _ in range(50):
        v = rim_power(p_shaft, flow_at(v, n, cc, ratio), eta_d) / F
    return v
def shaft_for(v, F, n, cc, ratio, eta_d):
    rim = F * v; q = flow_at(v, n, cc, ratio)
    return (rim / (0.855 * eta_d) + 10 * q / 600) / 0.855, q
OPTS = {
 "A1.5": dict(name="A 1.5:1 chain, 4 x MSE05", n=4, mot="MSE05 750", ratio=1.5, eta_d=0.97, spr=(16, 24)),
 "A1.6": dict(name="A 1.6:1 chain, 4 x MSE05", n=4, mot="MSE05 750", ratio=1.6, eta_d=0.97, spr=(15, 24)),
 "A1.75": dict(name="A 1.75:1 chain, 4 x MSE05 (recommended)", n=4, mot="MSE05 750", ratio=1.75, eta_d=0.97, spr=(16, 28)),
 "A2.0": dict(name="A 2:1 chain, 4 x MSE05", n=4, mot="MSE05 750", ratio=2.0, eta_d=0.97, spr=(14, 28)),
 "B1146": dict(name="B MSE08 1,146 cc 1:1 outboard", n=4, mot="MSE08 1146", ratio=1.0, eta_d=1.0),
 "B1248": dict(name="B MSE08 1,248 cc 1:1 outboard", n=4, mot="MSE08 1248", ratio=1.0, eta_d=1.0),
 "B_MS11": dict(name="B MS11 1,259 cc 1:1 outboard", n=4, mot="MS11 1259", ratio=1.0, eta_d=1.0),
 "C": dict(name="C plan LT25: 2 x MS05 560, 4:1 jackshaft + chains", n=2, mot="MS05 560", ratio=4.0, eta_d=0.97 * 0.97),
 "L1": dict(name="Adopted now (option C of 26 Oct): 4 x MSE05 1:1", n=4, mot="MSE05 750", ratio=1.0, eta_d=1.0),
}
P_PUMP = 35.0
def pd(p_in, z): return p_in / math.sin(math.pi / z)
res = {"inputs": dict(W_kN=W, F_start2=F_S2, F_start_level=F_L0, F_run2=F_R2, F_run_level=F_RL, adh_dry=ADH_DRY,
                       adh_wet=ADH_WET, wheel_rpm_7p5=N_TOP, p_start=P_START, pump_flow={k: qpump(v[0]) for k, v in PUMPS.items()}),
       "options": {}}
for k, o in OPTS.items():
    m = MOT[o["mot"]]; n, cc, i, ed = o["n"], m["cc"], o["ratio"], o["eta_d"]
    r = {"name": o["name"]}
    for eta in ("0.95", "0.90", "0.80"):
        r[f"F_start_{eta}"] = start_force(n, cc, i, float(eta), ed)
    r["F_start_pmax_0.80"] = start_force(n, cc, i, 0.80, ed, p=min(m["pmax"], 420))
    r["margin_dry_0.95"] = min(r["F_start_0.95"], ADH_DRY) - F_S2
    r["margin_dry_0.80"] = min(r["F_start_0.80"], ADH_DRY) - F_S2
    r["adh_limited"] = r["F_start_0.95"] > ADH_DRY
    r["wet_level_ok"] = min(r["F_start_0.80"], ADH_WET) >= F_L0
    r["wet_2pct"] = min(r["F_start_0.95"], ADH_WET) - F_S2
    r["motor_rpm_7p5"] = N_TOP * i
    r["rpm_ok"] = N_TOP * i <= m["n2"]
    r["flow_7p5_full"] = flow_at(V_TOP, n, cc, i)
    r["flow_7p5_half"] = flow_at(V_TOP, n, m["cc2"], i)
    tops = {}
    for pk, pv in PUMPS.items():
        q = qpump(pv[0])
        n_m = min(q * ETA_V / (n * m["cc2"] / 1000), m["n2"])
        tops[pk] = (n_m / i) * math.pi * D / 1000 / 60 / MPH
        n_m1 = min(q * ETA_V / (n * cc / 1000), m["n1"])
        tops[pk + "_full_disp"] = (n_m1 / i) * math.pi * D / 1000 / 60 / MPH
    r["level_top_mph"] = tops
    r["level_power_top_mph"] = bal_speed(P_PUMP, n, m["cc2"], i, ed, F_RL) / MPH
    r["F_half_disp_350"] = start_force(n, m["cc2"], i, 0.95, ed)
    r["bal_2pct_mph_35kW"] = bal_speed(P_PUMP, n, cc, i, ed, F_R2) / MPH
    ps, q = shaft_for(V_TOP, F_R2, n, cc, i, ed)
    r["shaft_kW_for_7p5_on_2pct"] = ps; r["flow_for_7p5_on_2pct"] = q; r["engine_net_cont_kW_needed"] = ps + 10
    r["motor_kW_each_7p5_2pct"] = F_R2 * V_TOP / n / ed
    r["motor"] = m
    if o.get("spr"):
        z1, z2 = o["spr"]; P140 = 44.45
        d1, d2 = pd(P140, z1), pd(P140, z2)
        T_relief = m["pmax"] * cc / (20 * math.pi) * 0.95 * i     # axle torque at motor max pressure (400 bar)
        T_adh = ADH_DRY / n * R * 1000 * 1.2                       # slip torque at mu 0.30 (sanded/dry high)
        r.update(spr_d=(d1, d2), T_axle_relief=T_relief, T_axle_slip=T_adh,
                 chain_pull_relief=T_relief / (d2 / 2000) / 1000, chain_pull_start=r["F_start_0.95"] / n * R * 1000 / (d2 / 2000) / 1000,
                 case_reaction_Nm=T_relief / i * (i - 1), axle_tau=16 * T_relief / (math.pi * 0.130 ** 3) / 1e6,
                 key_bearing=2 * T_relief / (0.130 * 0.009 * 0.150) / 1e6)
    res["options"][k] = r
# chain allowables (Tsubaki max allowable load, lbf -> kN)
CH = {"RS120-1": 6830, "RS120-2": 11560, "RS140-1": 9040, "RS140-2": 15370, "RS160-2": 20230}
res["chain_allow_kN"] = {k: v * 4.44822 / 1000 for k, v in CH.items()}
# option C chain loads (per LT18: 21/49 RS120 jackshaft->axle, first stage 4/2.333 = 1.714)
c = res["options"]["C"]
T_ax = c["F_start_0.95"] / 4 * R * 1000
d49 = pd(38.1, 49); d21 = pd(38.1, 21)
res["C_chain"] = dict(T_axle=T_ax, pull_axle_chain=T_ax / (d49 / 2000) / 1000, d49=d49, d21=d21,
                      T_jack=2 * T_ax / (49 / 21) / 0.97, pull_420=T_ax * 420 / 350 / (d49 / 2000) / 1000)
# engines (Kubota pages, gross intermittent) -> net continuous ASSUMED at V3307 ratio 45.6/55.4
ratio = 45.6 / 55.4
res["engines"] = {k: dict(gross=g, rpm=rp, kg=kg, net_cont_ASSUMED=(45.6 if k.startswith("V3307") else g * ratio))
                  for k, (g, rp, kg) in {"V3307-TIE4 (current)": (55.4, 2600, None), "V3800-CR-TIEF4": (86.4, 2600, 400),
                                          "V3800-CR-TIEF4H": (96.4, 2400, 400), "V5009-TIE5B": (157.3, 2200, 625)}.items()}
a = res["options"]["A1.75"]
for k, e in res["engines"].items():
    pp = max(0.0, e["net_cont_ASSUMED"] - 10)
    e["pump_kW"] = pp
    e["bal_2pct_mph_A1.75"] = bal_speed(pp, 4, 750, 1.75, 0.97, F_R2) / MPH
# hours & relative cost (ASSUMED, +/-30%)
res["hours"] = {
 "A": dict(eng=(70, 110), shop=(110, 160), credit_shop=-40, note="4 axle-hung oil-bath chain cases, nose links, sprocket locking, motor mounts; DT5 outboard carriers/couplings deleted"),
 "B": dict(eng=(60, 100), shop=(100, 150), credit_shop=0, note="4 bigger outboard carriers + over-wheel torque arches, larger couplings/stubs, width exception"),
 "C": dict(eng=(130, 190), shop=(190, 260), credit_shop=-40, note="2 jackshaft assemblies, 6 chains + tensioners + guards, 2 motor mounts, 2-stage ratio; DT5 outboard set deleted"),
}
json.dump(res, open("/workspace/train/calcs/F25/drive_options_F25.json", "w"), indent=1, default=float)
if __name__ == "__main__":
    print(json.dumps(res["inputs"], indent=1))
    for k, r in res["options"].items():
        print(k, {kk: (round(v, 2) if isinstance(v, float) else v) for kk, v in r.items() if kk not in ("motor", "name")})
    print(res["chain_allow_kN"]); print(res["C_chain"]); print(json.dumps(res["engines"], indent=1))

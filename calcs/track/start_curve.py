"""Starting / holding with curve resistance on the real profiles (Alt A, B, C if present).
Curve resistance basis: Rockl metre-gauge formula w_c = 400/(R-20) N/kN (applied to 914.4 mm gauge - between
Rockl's 750 mm (350/(R-10)) and 1,000 mm forms, so the metre-gauge form is the conservative choice); cross-check
AREMA 0.8 lb/ton per degree of curve.  Start resistance 0.0208 (PE basis), rolling 0.005.  Rev RT1 28 Oct 2026."""
import csv, json, os, math, sys
sys.path.insert(0, "/workspace/train/build")
import model as M
RR = "/workspace/route_redline"; g = 9.81
ROCKL = lambda R: 400.0 / (R - 20.0) / 1000.0
AREMA = lambda R: 0.8 * (5729.58 / (R / 0.3048)) / 2000.0
ADH_DRY, ADH_WET, TE = 37.93, 22.76, 37.9
START_R, ROLL = 0.0208, 0.005
RIM_KW_2PCT = 23.5   # L3 power_speed table, rim kW at 2 % (power-limited)
# vehicle centres from the front of the loco (m) and masses (kg, loaded)
c = M.consist()
cent = [(5.675, 17667), ((c[1][2] + 2500) / 1000, 8304)]
for i in range(4):
    cent.append(((c[2 + i][2] + 5080) / 1000, 11000 if i == 3 else 13200))
_k = 772.8 / (sum(m for _, m in cent) * g / 1000)   # scale vehicle masses to the PE basis W 772.8 kN (incl. crew/fuel allowances)
cent = [(o, m * _k) for o, m in cent]
Wt = sum(m for _, m in cent) * g / 1000

def prof(tag):
    rows = list(csv.DictReader(open(f"{RR}/{tag}_profile_5m.csv")))
    ch = [float(r["chainage_m"]) for r in rows]; gr = [float(r["grade_pct_to_next"]) / 100 for r in rows]
    rad = [float(r["radius_m"]) if r["radius_m"] not in ("", "nan") else None for r in rows]
    return ch, gr, rad

def at(ch, arr, x, L):
    x %= L
    lo, hi = 0, len(ch) - 1
    while hi - lo > 1:
        m = (lo + hi) // 2
        if ch[m] <= x: lo = m
        else: hi = m
    return arr[lo]

def analyse(tag, curve=ROCKL):
    ch, gr, rad = prof(tag); L = ch[-1] + (ch[-1] - ch[-2])
    worst = dict(start=0); worst_run = dict(R=0)
    vehicle_worst = dict(i_eq=0)
    for d in (1, -1):
        for k in range(len(ch)):
            s0 = ch[k]
            F = 0; Fr = 0; detail = []
            for (off, m) in cent:
                x = s0 - d * off
                i = d * at(ch, gr, x, L); r = at(ch, rad, x, L)
                cr = curve(r) if r else 0.0
                F += m * g / 1000 * (START_R + i + cr); Fr += m * g / 1000 * (ROLL + i + cr)
                if i + cr > vehicle_worst["i_eq"]: vehicle_worst = dict(i_eq=i + cr, ch=round(x % L, 1), grade=i, R=r, dir=d)
                detail.append((round(x % L, 1), round(i * 100, 2), r))
            if F > worst["start"]: worst = dict(start=F, ch=s0, dir=d, detail=detail)
            if Fr > worst_run["R"]: worst_run = dict(R=Fr, ch=s0, dir=d)
    ieq_train = worst["start"] / Wt - START_R
    v_hold = RIM_KW_2PCT / worst_run["R"] / 0.44704
    return dict(tag=tag, W_kN=round(Wt, 1), start_need_kN=round(worst["start"], 2), at_ch=worst["ch"], dir=worst["dir"],
                equiv_grade_pct=round(ieq_train * 100, 3), margin_dry=round(ADH_DRY / worst["start"], 3),
                sand_mu_req=round(worst["start"] / 151.7, 3), run_res_kN=round(worst_run["R"], 2), hold_mph=round(v_hold, 2),
                worst_vehicle_point=vehicle_worst, detail=worst["detail"])

def point_cases():
    out = []
    for lab, R, i in (("R100 at 1.5% (Alt A/B cap)", 100, 0.015), ("R125 at 1.62% (Alt B cap)", 125, 0.0162), ("R45 at 0.4% (Alt B hairpin cap)", 45, 0.004),
                      ("R50 at 2.0 - comp (Alt C basis)", 50, 0.02 - ROCKL(50)), ("R50 uncompensated at 2.0%", 50, 0.02),
                      ("R100 uncompensated at 2.0%", 100, 0.02), ("2.0% tangent", None, 0.02)):
        cr = ROCKL(R) if R else 0; ca = AREMA(R) if R else 0
        need = W_kN_total * (START_R + i + cr); needA = W_kN_total * (START_R + i + ca)
        out.append(dict(case=lab, R=R, grade_pct=round(i * 100, 3), rockl_permil=round(cr * 1000, 2), arema_permil=round(ca * 1000, 2),
                        comp_pct=round(cr * 100, 2), need_kN=round(need, 2), need_arema_kN=round(needA, 2), margin=round(TE / need, 3), margin_arema=round(TE / needA, 3),
                        hold_mph=round(RIM_KW_2PCT / (W_kN_total * (ROLL + i + cr)) / 0.44704, 2)))
    return out
W_kN_total = 772.8
if __name__ == "__main__":
    res = dict(basis=__doc__.strip(), points=point_cases(), alts={})
    for tag in ("A", "B", "C", "D"):
        if os.path.exists(f"{RR}/{tag}_profile_5m.csv"):
            res["alts"][tag] = dict(rockl=analyse(tag), arema=analyse(tag, AREMA))
    json.dump(res, open("/workspace/train/calcs/track/start_curve.json", "w"), indent=1)
    for p in res["points"]: print(p)
    for t, v in res["alts"].items():
        for k in ("rockl", "arema"):
            x = dict(v[k]); x.pop("detail"); print(t, k, x)

"""Allowable in-train buff/draft force per curve case so the empty-coach (and tender) wheel stays below Nadal (RT1 28 Oct 2026).
L/V = YQ_heumann + F·sin(α)·fac/(2Q).  α = sweep max (transient, no spirals) or steady (with ≥10 m spirals)."""
import json, math
from heumann import heumann, nadal
RC = json.load(open("route_check.json"))
N03 = nadal(70, 0.3); N15 = nadal(70, 0.15)
Qc, Qt = 9.86, 10.18; fc, ft = 1 + 2437 / 5486, 1 + 1200 / 2600
def fa(yq, a, fac, Q, lim): return max(lim - yq, 0) * 2 * Q / (math.sin(math.radians(a)) * fac) if a > 0 else 999
rows = []
def add(lab, R, a_c, a_t):
    yc = heumann(1.2, R)["YQ1"]
    r = dict(case=lab, R=R, a_coach=round(a_c, 2), a_tender=round(a_t, 2))
    for k, lim in (("dry_nadal", N03), ("dry_m12", N03 / 1.2), ("lube_m12", N15 / 1.2)):
        r["Fc_" + k] = round(fa(yc, a_c, fc, Qc, lim), 1); r["Ft_" + k] = round(fa(yc, a_t, ft, Qt, lim), 1)
    r["LV_coach_70"] = round(yc + 70 * math.sin(math.radians(a_c)) * fc / (2 * Qc), 2)
    r["LV_coach_33"] = round(yc + 33 * math.sin(math.radians(a_c)) * fc / (2 * Qc), 2)
    rows.append(r)
for R in (100, 60, 50, 45):
    x = RC["radii"][str(R)]
    add(f"R{R} no spiral (entry)", R, x["cpl_coach"], x["cpl_lt_tender"])
    add(f"R{R} with ≥10 m spirals (steady)", R, x["st_coach"], x["st_lt_tender"])
for k, x in RC["s_curves"].items():
    add(k, x["Rmin"], x["cpl_coach"], x["cpl_lt_tender"])
for t, x in RC["alts"].items():
    R = {"A": 100, "B": 45, "C": 50, "D": 60}[t]
    add(f"Alt {t} as drawn", R, x["cpl_coach"], x["cpl_lt_tender"])
json.dump(dict(nadal_dry=N03, nadal_lube015=N15, rows=rows), open("buff_allow.json", "w"), indent=1)
for r in rows: print(r)

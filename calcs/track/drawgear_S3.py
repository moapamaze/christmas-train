"""Stress Bot round 3 (28 Oct 2026) draft-gear basis check: 1.0 mm TOTAL play at the renew limit (= 0.5 mm each side in
drawgear.sim), stiffness k >= 20 kN/mm, loco service/emergency brake rate matched to the coaches (<= 0.69 m/s2).
Sweeps k to find the upper stiffness that keeps start snatch / run-in within the route buff allowances (route_L4: E R70 38.8 kN,
F R80 45.8 kN). Reuses sim() from drawgear.py unchanged (masses there: loco 17,667 / tender 8,304 - L4 masses are within 1 %)."""
import json, importlib.util, sys, io, contextlib
spec = importlib.util.spec_from_file_location("dg", __file__.replace("drawgear_S3.py", "drawgear.py"))
src = open(spec.origin).read().split("out = []")[0]
ns = {}; exec(src, ns); sim = ns["sim"]
ALLOW = {"E_R70": 38.8, "F_R80": 45.8}
rows = []
for k in (20, 25, 30, 40, 50, 75, 100, 150, 200):
    st = [float(v) for v in sim(k, 0.5, "start")]; rm = [float(v) for v in sim(k, 0.5, "run", decel=(0.69, 0.69))]
    peak = max(st[0], rm[1])
    rows.append(dict(k_kNmm=k, total_play_mm=1.0, start_T_kN=st[0], runin_C_matched_kN=rm[1], peak_kN=peak,
                     util_E=round(peak / ALLOW["E_R70"], 2), util_F=round(peak / ALLOW["F_R80"], 2)))
    print(rows[-1], flush=True)
def kmax(key):
    best = None
    for r in rows:                       # largest k with every stiffer-or-equal sweep point below it passing (non-monotonic response)
        if r[key] > 1.0: break
        best = r["k_kNmm"]
    return best
kmaxF = kmax("util_F"); kmaxE = kmax("util_E")
out = dict(basis="1.0 mm total play renew limit, k >= 20 kN/mm, loco brake rate <= 0.69 m/s2 (Stress Bot R3)", allow=ALLOW, rows=rows,
           k_max_F_kNmm=kmaxF, k_max_E_kNmm=kmaxE, at_k20=rows[0])
json.dump(out, open("drawgear_S3.json", "w"), indent=1)
print("kmax F", kmaxF, "kmax E", kmaxE)

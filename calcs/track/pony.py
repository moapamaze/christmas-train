"""Spring-loaded pony (lead) truck - owner keeps the leading truck (Stress Bot #3, Loco Bot C2/F06). RT1 28 Oct 2026.
Lead truck centre X1,525 (swing-arm anchor X2,600, arm 1,075); front pivot X4,075, rear X7,275 (model.py).  A spring preload F
reacted on the loco body at X1,525 lifts 1.797F off the front truck and adds 0.797F to the rear truck (lever outside the pivots)."""
import json
from heumann import heumann, nadal
g = 9.80665
LC = json.load(open("loco_check.json")); A = LC["mass"]["axles_corr_kN"]
lf = (7275 - 1525) / 3200; lr = lf - 1
N03, N15 = nadal(70, 0.3), nadal(70, 0.15)
TWIST = 0.75     # kN wheel unloading in twist on the unsprung pony (Stress Bot min wheel 2.17 vs 2.89); sprung pony k 150 N/mm total ASSUMED gives ~0.75 kN for 10 mm twist
rows = []
for F in (0.0, 10.0, 12.5, 15.0):
    for comp in (0.0, 1.0):          # comp = front-truck ballast (t) placed over the front pivot to restore the drivers
        Q = A["LEAD1"] / 2 + F / 4; Qmin = Q - TWIST
        fr = lf * F - comp * 1000 * g / 1000
        F1, F2 = A["F1"] - fr / 2, A["F2"] - fr / 2; R1, R2 = A["R1"] + lr * F / 2, A["R2"] + lr * F / 2
        yq = {R: heumann(1.05, R)["YQ1"] for R in (100, 60, 50, 45)}
        rows.append(dict(F_kN=F, front_ballast_t=comp, Q_wheel=round(Q, 2), Q_min_twist=round(Qmin, 2),
                         YQ_curving={R: round(v, 3) for R, v in yq.items()},
                         Fc_allow_kN_R50_dry_m12=round((N03 / 1.2 - yq[50]) * Qmin, 2), Fc_allow_kN_R50_lube_m12=round((N15 / 1.2 - yq[50]) * Qmin, 2),
                         F1=round(F1, 2), F2=round(F2, 2), R1=round(R1, 2), R2=round(R2, 2), max_wheel=round(max(F1, F2, R1, R2) / 2, 2),
                         equal_torque_cap_dry=round(4 * 0.25 * min(F1, F2, R1, R2), 2), ideal_cap_dry=round(0.25 * (F1 + F2 + R1 + R2), 2),
                         loco_kg=round(LC["mass"]["loco_corr_kg"] + comp * 1000)))
SPEC = dict(preload_kN=12.5, springs="2 coil springs (one per side bearer) at the pony bolster, 6.25 kN each installed; rate 75 N/mm each (150 N/mm per truck); "
            "installed deflection ≈ 83 mm; ±25 mm bounce/twist travel → ±1.9 kN (±15 %); solid height ≥ 40 mm below installed with a rubber bump stop at -30 mm",
            side_bearers="flat PTFE/bronze side-bearer plates at Y±300 on the pony bolster so the spring load does not add yaw torque > 0.25 kN·m (μ 0.1 × 12.5 kN × 0.2 m)",
            swing_stops="±175 mm (R50) / ±145 mm (R60) / ±95 mm (R100) at the swing-arm end, rubber-faced; NO lateral centering spring > 0.5 kN at full swing",
            front_ballast="+1.0 t over the front driver truck pivot (X4,075) to restore the front drivers (the spring lifts 1.80×F off the front truck)",
            check="free-swinging arm: leading-wheel Y/Q = Heumann 0.94 at R45-R50 (independent of Q) vs Nadal 1.34 dry → 0.70; preload makes the WHEEL LOAD robust to twist "
                  "(Q_min 5.3 kN vs 2.2 kN unsprung) and lets the truck accept ≤ 1.4 kN of arm/centering friction (vs 0.4 kN unsprung)")
json.dump(dict(rows=rows, spec=SPEC, lever_front=lf, lever_rear=lr), open("pony.json", "w"), indent=1)
for r in rows: print(r)

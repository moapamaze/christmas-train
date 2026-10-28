"""Loco mass re-check (LT43 double count), per-axle equal-torque start with curve resistance, lead-truck flange climb.
Rev RT1 28 Oct 2026.  Sources: assets/locomotive-lt42/mass-summary.json.gz (LT42 statics, 16,810 kg), tender-lt43.html
('locomotive changes from 16.81 t to 15.80 t ... front-truck body support 2,563 → 1,712 kg'), calcs/tender_mass_T2.json
(T2 ledger carries the V3307 package 610 + tanks 90 + cooler 55 ...), calcs/L3/drive_L3.json (L3 delta +857 kg on the
4 driven axles), structural_body_study.md (option 2 weight-neutral: ballast 1.5 → ~0.5 t, loco mass unchanged)."""
import json, gzip, math
from heumann import heumann, nadal
g = 9.80665
LT42 = json.load(gzip.open("/workspace/train/assets/locomotive-lt42/mass-summary.json.gz"))["revised"]
ax = {a["axle"]: a["rail_load_kN"] for a in LT42["axles"]}
m42 = LT42["total_kg"]; dL3 = 857.0
reloc = 16810 - 15800                     # LT43: machinery/tanks/fluids 959 + retired compressor/VFD 50.6
front_drop = 2563 - 1712                  # LT43 front-truck body support change
rear_drop = reloc - front_drop
corr = dict(LEAD1=ax["LEAD-1"], LEAD2=ax["LEAD-2"],
            F1=ax["FRONT-1"] - front_drop * g / 2000 + dL3 / 4 * g / 1000, F2=ax["FRONT-2"] - front_drop * g / 2000 + dL3 / 4 * g / 1000,
            R1=ax["REAR-1"] - rear_drop * g / 2000 + dL3 / 4 * g / 1000, R2=ax["REAR-2"] - rear_drop * g / 2000 + dL3 / 4 * g / 1000)
m_loco_corr = m42 - reloc + dL3
L3asis = dict(F1=ax["FRONT-1"] + dL3 / 4 * g / 1000, F2=ax["FRONT-2"] + dL3 / 4 * g / 1000, R1=ax["REAR-1"] + dL3 / 4 * g / 1000, R2=ax["REAR-2"] + dL3 / 4 * g / 1000)
W_L3 = 772.8; W_corr = W_L3 - reloc * g / 1000
drv = ["F1", "F2", "R1", "R2"]
mass = dict(loco_L3_kg=17667, loco_corr_kg=round(m_loco_corr), train_L3_kN=W_L3, train_corr_kN=round(W_corr, 1),
            axles_corr_kN={k: round(v, 2) for k, v in corr.items()}, axles_L3asis_kN={k: round(v, 2) for k, v in L3asis.items()},
            lead_wheel_kN=round(ax["LEAD-1"] / 2, 2), lead_wheel_L3_basis_kN=round((17667 * g / 1000 - 151.7) / 4, 2),
            max_wheel_corr_kN=round(max(corr[k] for k in drv) / 2, 2), drivers_corr_kN=round(sum(corr[k] for k in drv), 1),
            note="L3 W_drv 151.7 kN was obtained as loco minus lead; the LT42 statics give lead 11.6 kN (2.9 kN/wheel), not 21.6 kN. "
                 "Ballast 1.5 → ~0.5 t (SB-1 option 2) is weight-neutral (4.8 mm shell replaces it): total unchanged, front-truck share falls further "
                 "(ballast sat over the front truck) - AWAIT weigh-in / re-baseline.")
# ---------------- traction: start resistance + Röckl curve resistance; equal torque per motor (4 parallel H1B110 on one loop)
def need(W, i, R):
    wc = 0 if R is None else 0.4 / (R - 20)          # Röckl metre-gauge 400/(R-20) N/kN
    return W * (0.0208 + i + wc)
MU = dict(dry=0.25, wet=0.15, sanded=0.25)
CURV_ADH = {None: 1.0, 100: 0.95, 60: 0.9, 50: 0.9, 45: 0.9}   # ASSUMED reduction of usable adhesion on curves (lateral creep)
def caps(Q, R):
    k = CURV_ADH.get(R, 0.9)
    q = [Q[a] for a in drv]
    return dict(equal_dry=4 * MU["dry"] * min(q) * k, equal_wet=4 * MU["wet"] * min(q) * k, equal_sanded=4 * MU["sanded"] * min(q) * k,
                ideal_dry=MU["dry"] * sum(q) * k, ideal_wet=MU["wet"] * sum(q) * k)
def pitch(Q, F, hp=1100.0, hdb=550.0):
    """sensitivity: axle-load transfer under tractive effort F (loco leading). Truck pitch: each truck reacts F/2 at the pivot
    height hp (ASSUMED Z1,100) → leading axle of each truck unloads (F/2)·hp/wb; body pitch: drawbar at Z550 vs pivots →
    F·(hp-hdb)/3,200 moves from the front truck to the rear truck.  TA-rod torque reactions NOT included (depend on arm direction)."""
    t = F / 2 * hp / 1550; b = F * (hp - hdb) / 3200
    return dict(F1=Q["F1"] - t - b / 2, F2=Q["F2"] + t - b / 2, R1=Q["R1"] - t + b / 2, R2=Q["R2"] + t + b / 2)
def cap_with_pitch(Q, R, mu):
    F = 20.0
    for _ in range(60):
        q = pitch(Q, F); F = 4 * mu * min(q[a] for a in drv) * CURV_ADH.get(R, 0.9)
    return F
start = []
for lab, i, R in (("0% tangent", 0.0, None), ("0% R100", 0.0, 100), ("0% R60", 0.0, 60), ("0% R50", 0.0, 50), ("0% R45", 0.0, 45),
                  ("2% tangent / compensated curves", 0.02, None), ("2% R50 uncompensated", 0.02, 50)):
    for basis, Q, W in (("corrected", corr, W_corr), ("L3 as-is", L3asis, W_L3)):
        n = need(W, i, R); c = caps(Q, R)
        row = dict(case=lab, basis=basis, need_kN=round(n, 2), **{k: round(v, 2) for k, v in c.items()},
                   util_equal_dry=round(n / c["equal_dry"], 3), util_equal_wet=round(n / c["equal_wet"], 3), util_equal_sanded=round(n / c["equal_sanded"], 3),
                   util_ideal_dry=round(n / c["ideal_dry"], 3))
        if basis == "corrected":
            row["equal_dry_with_pitch"] = round(cap_with_pitch(Q, R, 0.25), 2); row["util_equal_dry_pitch"] = round(n / row["equal_dry_with_pitch"], 3)
        start.append(row)
# ---------------- lead truck: flange climb with actual load (Heumann free 2-axle truck, wb 1,050) + centering force
NAD = nadal(70, 0.3)
lead = []
SW = {100: 71.6, 60: 120.0, 50: 142.9, 45: 158.6}      # kinematic swing from the sweep (R60 interpolated - replaced by sweep in summarize)
for R in (100, 60, 50, 45):
    yq = heumann(1.05, R)["YQ1"]
    for lab, Q in (("as-is 2.9 kN/wheel", corr["LEAD1"] / 2), ("+0.5 t transfer", corr["LEAD1"] / 2 + 500 * g / 4000), ("+1.0 t transfer", corr["LEAD1"] / 2 + 1000 * g / 4000)):
        Fc = (NAD / 1.0 - yq) * Q        # centering force the leading outer wheel can take before Nadal (no margin)
        Fc_m = (NAD / 1.2 - yq) * Q      # with 1.2 margin on Nadal
        lead.append(dict(R=R, case=lab, Q=round(Q, 2), YQ_curving=round(yq, 3), Fc_allow_kN=round(Fc, 2), Fc_allow_margin12_kN=round(Fc_m, 2),
                         k_allow_Nmm=round(Fc_m * 1000 / SW[R], 1)))
OUT = dict(rev="RT1 28 Oct 2026", mass=mass, start=start, lead=lead, nadal=NAD, curve_adhesion_factor="ASSUMED 0.95 R100 / 0.90 R≤60")
json.dump(OUT, open("/workspace/train/calcs/track/loco_check.json", "w"), indent=1)
print(json.dumps(mass, indent=1))
for r in start: print(r)
for r in lead: print(r)

"""Route vehicle check rev L4 (28 Oct 2026) - Rail Bot FINAL spiralled alignments (altA/D/E/F.json + X_curve_table.csv, spirals integrated
by sweep_L4.py) with the L4 vehicle masses (drive_L4.json: L-107 P1-L +36.5 kg, cab C1, tender TB-3.3 8,451 kg; tender CG + wheel loads from calcs/tender/tender_cg_TB33.json). Pass/fail per alternative.
Checks: envelope (+widening, +60 mm garland) vs K-401 1,696; cylinders vs lead wheel (Y±790 as built, ≥10 after play); coupler swing vs pocket;
L/V (Heumann Y/Q + drawbar lateral) vs Nadal 1.34; wheel unloading ΔQ/Q ≤ 0.6 (ASSUMED limit); inter-vehicle gaps; lead-truck swing; start margins."""
import json, math, csv, sys
sys.path.insert(0, "/workspace/train/calcs/track")
from heumann import heumann, nadal
T = "/workspace/train/calcs/track"; g = 9.80665
D4 = json.load(open("/workspace/train/calcs/L4/drive_L4.json")); B = D4["basis"]; ST = D4["start"]
DB = json.load(open("/workspace/train/calcs/L4/drawbar_L4.json"))["decision"]
POCK = json.load(open(f"{T}/route_sweep.json"))["pocket"]
NAD = nadal(70, 0.3); ENV = 1696.0; PLAY = 6.2; GARLAND = 60.0; DQ_LIM = 0.6
def widen(R): return (920.7 - 914.4 + 3) if R <= 50 else ((917.5 - 914.4 + 3) if R <= 75 else 0.0)
# ---- L4 masses / wheel loads (lightest wheels govern L/V and unloading)
m_loco, m_tender, m_train = B["loco_kg"], B["tender_kg"], B["train_kg"]
TCG = json.load(open("/workspace/train/calcs/tender/tender_cg_TB33.json"))   # Steering 15: real T2 CG (was uniform W/8 and h 0.95 ASSUMED)
Q = dict(loco=round(min(B["axle_loads_kN_RT1corr_plus_L4"].values()) / 2, 2), tender=round(min(v["axle"] for v in TCG["axle_wheel_kN"].values()) / 2, 2), coach_e=9.86)
F_TE = min(ST["F350_kN"], ST["adh_avg_dry_kN"])                       # 37.67 kN hydraulic at 350 bar (< dry adhesion 44.5)
F_LT = F_TE * (m_train - m_loco) / m_train                           # drawbar behind the loco at full TE (start, uniform acceleration share)
F_C1 = F_TE * (m_train - m_loco - m_tender) / m_train                # tender-coach 1
FAC = dict(loco=1 + 3875 / 3200, tender=1 + 1200 / 2600, coach=1 + 2437 / 5486)   # pin overhang / pivot spacing lever on the nearer truck
H_CPL = 0.55; S_CONT = 0.985                                          # coupler height ARL; wheel contact spacing (gauge + 70)
HCG = dict(loco=1.10, tender=round(TCG["cg_mm"][2] / 1000, 3), coach=1.30)   # loco / coach ASSUMED; tender = real T2 CG TB-3.3 (was 0.95 ASSUMED)
V = 7.0 * 0.44704                                                    # overspeed trip speed
def lv_inc(F, a, fac, q): return F * math.sin(math.radians(a)) * fac / (2 * q)
def dQ(F, a, fac, q, m_truck_kg, hcg, R):
    lat = F * math.sin(math.radians(a)) * fac                         # kN on the nearer truck
    cen = m_truck_kg * V**2 / R / 1000                                # kN, unbalanced (no cant)
    return (lat * H_CPL + cen * hcg) / S_CONT / (2 * q)               # per wheel / static wheel, 2 wheels per side per truck
def start_need(tag):
    """worst start need over a 65 m train window on the profile (grade + 400/R kN curve resistance, L4 W)."""
    try: f = open(f"/workspace/route_redline/{tag}_profile_5m.csv")
    except FileNotFoundError: return None
    lines = f.read().splitlines()
    if lines[0].startswith("status"): lines = lines[1:]
    rows = list(csv.DictReader(lines))
    kc, kg, kr = ("chainage_m", "grade_pct_to_next", "radius_m") if "chainage_m" in rows[0] else ("ch_m", "grade_pct_ahead", "curve_R_m")
    ch = [float(r[kc]) for r in rows]; gr = [float(r[kg] or 0) for r in rows]
    Rr = [float(r[kr]) if r.get(kr) not in (None, "", "0", "0.0") else None for r in rows]
    best = (0, None)
    for i in range(len(rows)):
        j = i; s = 0.0; n = 0
        while j < len(rows) and ch[j] - ch[i] <= 65.0:
            s += gr[j] * B["W_kN"] / 100 + (400.0 / Rr[j] if Rr[j] else 0); n += 1; j += 1
        for sign in (1, -1):
            v = 16.65 + (s if sign > 0 else (-s + 2 * sum(400.0 / Rr[k] for k in range(i, j) if Rr[k]))) / n
            if v > best[0]: best = (v, ch[i])
    need = best[0]; lt = ST["lightest_axle_kN"]; sm = B["sum_axles_kN"]
    return dict(need_kN=round(need, 2), at_ch_m=best[1], TE_350=ST["F350_kN"], margin_TE=round(ST["F350_kN"] / need, 2),
                dry_equal=round(4 * 0.25 * lt / need, 2), wet_divider=round(0.15 * sm / need, 2), sand_required=0.15 * sm / need < 1.0)
OUT = dict(rev="L4 route check 28 Oct 2026", basis=dict(Q_kN=Q, F_TE=round(F_TE, 2), F_LT=round(F_LT, 2), F_C1=round(F_C1, 2), nadal=round(NAD, 3), envelope=ENV, garland=GARLAND,
           dQ_limit_ASSUMED=DQ_LIM, hcg_ASSUMED=HCG, v_mps=round(V, 2), pocket_deg={k: round(v, 1) for k, v in POCK.items()}, drawbars=dict(loco_tender=DB["loco_tender_mm"], others=DB["coach_coach_mm"]),
           notes=["Sweep integrates the 12 m clothoids, so coupler angles are actual (transient) - no spiral credit taken.",
                  "Pony ballast vs pony arm / lead wheel hits in the raw sweep are a CAD-grouping artefact (ballast tagged to the body, but specified ON the sprung pony frame) - excluded; fix the model group.",
                  "Cylinder gap uses the as-built Y±790 cylinders (cyl_gap_790) less 6.2 mm play."]), alts={})
for tag in "ADEF":
    S = json.load(open(f"{T}/L4/sweep_L4_{tag}.json")); R = S["Rmin_m"]; r = S["res"]; cp = S["cpl"]
    hl, hc, ht = heumann(1.55, R), heumann(1.2, R), heumann(1.05, R)
    a_lt_l, a_lt_t = cp[0]["a_front"], cp[0]["a_rear"]; a_c = max(max(x["a_front"], x["a_rear"]) for x in cp[1:])
    env_l = r["Locomotive"]["out"] + widen(R); env_c = max(r[k]["out"] for k in r if k.startswith("Coach")) + GARLAND + widen(R); env_t = r["Tender"]["out"] + widen(R)
    lv = dict(loco=hl["YQ1"] + lv_inc(F_LT, a_lt_l, FAC["loco"], Q["loco"]), tender=hc["YQ1"] + lv_inc(F_LT, a_lt_t, FAC["tender"], Q["tender"]),
              coach_empty=hc["YQ1"] + lv_inc(F_C1, a_c, FAC["coach"], Q["coach_e"]), lead_free=ht["YQ1"])
    dq = dict(loco=dQ(F_LT, a_lt_l, FAC["loco"], Q["loco"], m_loco / 2, HCG["loco"], R), tender=dQ(F_LT, a_lt_t, FAC["tender"], Q["tender"], m_tender / 2, HCG["tender"], R),
              coach_empty=dQ(F_C1, a_c, FAC["coach"], Q["coach_e"], Q["coach_e"] * 4 / g * 1000, HCG["coach"], R))
    pock = dict(loco=a_lt_l / POCK["loco_rear"], tender=a_lt_t / POCK["tender"], coach=a_c / POCK["coach"])
    cyl = S["cyl_gap_790"] - PLAY
    iv = min(x["min_gap"] for x in S["inter_vehicle"])
    real_interf = [x for x in S["interf"] if "pony ballast" not in (x["a"] + x["b"])]
    ri = min(x["min_gap"] for x in real_interf)
    chk = dict(envelope=max(env_l, env_c, env_t) <= ENV, cylinders=cyl >= 10, pocket=max(pock.values()) <= 1, LV=max(lv.values()) <= NAD,
               unloading=max(dq.values()) <= DQ_LIM, inter_vehicle=iv > 0, parts=ri > 0)
    OUT["alts"][tag] = dict(Rmin_m=R, L_m=round(S["L_m"], 1), env_loco=round(env_l, 1), env_coach_garland=round(env_c, 1), env_tender=round(env_t, 1), widen_mm=widen(R),
        cyl_gap_mm=round(cyl, 1), coupler_deg=dict(lt_loco=round(a_lt_l, 1), lt_tender=round(a_lt_t, 1), coach=round(a_c, 1)), pocket_util={k: round(v, 2) for k, v in pock.items()},
        LV={k: round(v, 2) for k, v in lv.items()}, LV_margin=round(NAD / max(lv.values()), 2), dQ_Q={k: round(v, 3) for k, v in dq.items()},
        lead_swing_mm=round(S["lead"]["swing"]), inter_vehicle_min_mm=round(iv, 1), parts_min_gap_mm=round(ri, 1), yaw_max_deg=round(max(S["yaw"].values()), 2),
        allow_buff_coach_kN=round((NAD - hc["YQ1"]) * 2 * Q["coach_e"] / (math.sin(math.radians(a_c)) * FAC["coach"]), 1),
        checks=chk, PASS=all(chk.values()))
for tag in ("A", "D", "E", "E1", "E15", "F", "F1", "F15"):
    OUT.setdefault("start", {})[tag] = start_need(tag)
json.dump(OUT, open(f"{T}/L4/route_L4.json", "w"), indent=1, default=float)
if __name__ == "__main__":
    print(json.dumps(OUT["basis"], default=float))
    for k, v in OUT["alts"].items(): print(k, json.dumps(v, default=float))
    for k, v in OUT["start"].items(): print("start", k, v)

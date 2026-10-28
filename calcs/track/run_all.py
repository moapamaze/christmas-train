"""Runs the route check: real alignments (A, B, C if present) + generic radius / reverse-curve cases.
Writes route_check.json and route_check.md.  Rev RT1 28 Oct 2026."""
import os, json, math, csv, time
import numpy as np
import route_check as R
from heumann import heumann, nadal
g = 9.81
V = R.build_vehicles()
S = R.straight_alignment(); trS = R.place_train(S, V, 100000.)
PAIRS = R.candidate_pairs(V, trS)
NADAL = nadal(70, 0.3)
ADH = 37.93; W_kN = 772.8
MASS = dict(loco=17667, tender=8304, reg=13200, acc=11000, reg_e=8040, acc_e=7000)
Q = dict(loco_drv=151.7 / 8, tender=MASS["tender"] * g / 8 / 1000, coach_e=MASS["reg_e"] * g / 8 / 1000, coach_l=MASS["reg"] * g / 8 / 1000)

def theta_max(Lm, half_clear=200 - 16, half_bar=75):
    f = lambda t: Lm * math.tan(t) + half_bar / math.cos(t) - half_clear
    return math.degrees(R.brentq(f, 0, 1.2))
POCKET = dict(loco_rear=theta_max(150), tender=theta_max(300), coach=theta_max(150), tender_fix150=theta_max(150))

def case(name, A, rng=None, step=1000., both=True, interf=True):
    t = time.time()
    outs = []
    for rev in ((False, True) if both else (False,)):
        r = R.sweep(A, V, step=step, reverse=rev, s_range=rng)
        cg = min(R.cyl_wheel_gap(V, tr) for s, tr in r["states"])
        cg790 = min(R.cyl_wheel_gap(V, tr, cy=790) for s, tr in r["states"])
        rows = R.interference(V, PAIRS, r["states"]) if interf else []
        outs.append((r, cg, cg790, rows))
    res = {}
    for k in outs[0][0]["res"]:
        a = [o[0]["res"][k] for o in outs]
        res[k] = dict(out=max(x["out"] for x in a), inn=max(x["inn"] for x in a), low_out=max(x["low_out"] for x in a),
                      low_inn=max(x["low_inn"] for x in a), out_nm=max(a, key=lambda x: x["out"])["out_nm"],
                      inn_nm=max(a, key=lambda x: x["inn"])["inn_nm"])
    cpl = []
    for j in range(len(V) - 1):
        a = [o[0]["cpl"][j] for o in outs]
        cpl.append(dict(a_front=max(x["a1max"] for x in a), a_rear=max(x["a2max"] for x in a), body=max(x["bodymax"] for x in a)))
    # NB a1 is angle vs vehicle ahead, a2 vs vehicle behind, at the max-angle position; also keep the overall max per side
    for j in range(len(V) - 1):
        for o in outs:
            c = o[0]["cpl"][j]
    lead = dict(swing=max(o[0]["lead"]["swing"] for o in outs), arm_angle=max(o[0]["lead"]["aoa"] for o in outs))
    yaw = {}
    for o in outs:
        for k, v in o[0]["yaw"].items(): yaw[k] = max(yaw.get(k, 0), v)
    rows = {}
    for o in outs:
        for x in o[3]:
            key = (x["a"], x["b"])
            if key not in rows or x["min_gap"] < rows[key]["min_gap"]: rows[key] = x
    rows = sorted(rows.values(), key=lambda x: x["min_gap"])
    inter_veh = [x for x in rows if x["a"].split(":")[0] != x["b"].split(":")[0]]
    out = dict(name=name, res=res, cpl=cpl, lead=lead, yaw=yaw, cyl_gap=min(o[1] for o in outs), cyl_gap_790=min(o[2] for o in outs),
               interf=[dict((k, float(v) if isinstance(v, (np.floating,)) else v) for k, v in x.items()) for x in rows[:8]],
               inter_vehicle=[dict((k, float(v) if isinstance(v, (np.floating,)) else v) for k, v in x.items()) for x in inter_veh[:4]],
               secs=round(time.time() - t, 1))
    print(name, out["secs"], "s", flush=True)
    return out

def synth(spec): return R.load_alignment("syn", R.synth_els(spec))
def rng_for(spec):
    Ltot = sum(x[1] if x[0] == "T" else x[1] * math.radians(x[2]) for x in spec) * 1000
    return (spec[0][1] * 1000 - 20000 + 60000, Ltot - 10000) if spec[0][1] >= 80 else (60000, Ltot - 10000)

CASES = {}
def run_syn(name, spec, step=1000.):
    CASES[name] = case(name, synth(spec), rng=(40000 + 20000, sum(x[1] if x[0] == "T" else x[1] * math.radians(x[2]) for x in spec) * 1000 - 5000), step=step)
    CASES[name]["spec"] = spec

if __name__ == "__main__":
    for Rr in (125, 100, 90, 80, 70, 60, 50, 45, 40, 35):
        run_syn(f"const_R{Rr}", [("T", 100), ("C", Rr, 120, "L"), ("T", 60)], step=1000.)
    for Rr, Tt in ((100, 25.66), (100, 0.0), (50, 0.0), (50, 5.0), (50, 10.0), (50, 15.0), (50, 20.0), (50, 25.66), (45, 15.93)):
        run_syn(f"S_R{Rr}_T{Tt}", [("T", 100), ("C", Rr, 90, "L"), ("T", Tt), ("C", Rr, 90, "R"), ("T", 60)], step=1000.)
    run_syn("B_R125_T15.93_R45", [("T", 100), ("C", 125, 74.4, "R"), ("T", 15.93), ("C", 45, 150, "L"), ("T", 60)], step=1000.)
    ALTS = {}
    for tag in ("A", "B", "C"):
        if os.path.exists(f"{R.RR}/{tag}_curve_table.csv"):
            A = R.load_alignment(tag)
            ALTS[tag] = case(f"Alt {tag}", A, step=2000.)
            ALTS[tag]["L_m"] = A["L"] / 1000
    json.dump(dict(cases=CASES, alts=ALTS, pocket=POCKET, nadal=NADAL), open(f"{R.OUT}/route_sweep.json", "w"), indent=1, default=float)
    print("done")

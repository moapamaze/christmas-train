"""Rev L4 route re-check on Rail Bot's FINAL spiralled alignments (route_redline/{A,D,E,F}_curve_table.csv, read-only).
Same kinematic sweep as RT1 (route_check.py / run_all.case), but the loader integrates the clothoid spirals of
'spiral-arc-spiral' elements (curvature 0 -> 1/R over Ls, arc, 1/R -> 0). Usage: python sweep_L4.py E  -> sweep_L4_E.json"""
import sys, os, csv, json, math
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, "/workspace/train/calcs/track"); os.chdir("/workspace/train/calcs/track")
import route_check as R
import run_all as RA

def load_spiral(tag, ds=50.0):
    els = list(csv.DictReader(open(f"{R.RR}/{tag}_curve_table.csv")))
    E0, N0 = float(els[0]["start_E"]), float(els[0]["start_N"])
    pts, curv, err = [], [], []
    for e in els:
        L = float(e["length_m"]) * 1000; n = max(2, int(round(L / ds))); h = L / n
        x, y = (float(e["start_E"]) - E0) * 1000, (float(e["start_N"]) - N0) * 1000
        th = math.radians(90 - float(e["bearing_deg"]))           # bearing (from N, cw) -> math angle
        if e["type"] == "tangent": kf = lambda s: 0.0
        else:
            Rr = float(e["radius_m"]) * 1000; Ls = float(e["spiral_Ls_m"] or 0) * 1000; sg = 1 if "CCW" in e["direction"] else -1
            def kf(s, Rr=Rr, Ls=Ls, L=L, sg=sg):
                k = 1 / Rr
                if Ls > 0 and s < Ls: k *= s / Ls
                elif Ls > 0 and s > L - Ls: k *= (L - s) / Ls
                return sg * k
        P, K = [], []
        for i in range(n):
            s = i * h; P.append((x, y)); K.append(kf(s))
            km = kf(s + h / 2); thm = th + km * h / 2
            x += h * math.cos(thm); y += h * math.sin(thm); th += (kf(s) + 4 * km + kf(s + h)) / 6 * h
        err.append(math.hypot(x - (float(e["end_E"]) - E0) * 1000, y - (float(e["end_N"]) - N0) * 1000))
        pts.append(np.array(P)); curv.append(np.array(K))
    P = np.vstack(pts); K = np.concatenate(curv)
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(np.vstack([P, P[:1]]), axis=0).T))]
    return dict(tag=tag, els=els, P=P, K=K, S=d[:-1], L=d[-1], tree=cKDTree(P), close_gap=float(np.hypot(*(P[-1] - P[0]))), el_end_err_mm=max(err))

if __name__ == "__main__":
    tag = sys.argv[1]
    A = load_spiral(tag)
    print(tag, "L", round(A["L"] / 1000, 1), "m, max element end error", round(A["el_end_err_mm"], 1), "mm, closure", round(A["close_gap"], 1), "mm", flush=True)
    out = RA.case(f"Alt {tag} (spiralled, L4)", A, step=float(os.environ.get("STEP", "2000")))
    out["L_m"] = A["L"] / 1000; out["el_end_err_mm"] = A["el_end_err_mm"]; out["closure_mm"] = A["close_gap"]
    out["Rmin_m"] = min(float(e["radius_m"]) for e in A["els"] if e["radius_m"])
    out["curves"] = [(e["element"], float(e["radius_m"]), float(e["spiral_Ls_m"] or 0)) for e in A["els"] if e["radius_m"]]
    json.dump(out, open(f"/workspace/train/calcs/track/L4/sweep_L4_{tag}.json", "w"), indent=1, default=float)
    print("done", tag, flush=True)

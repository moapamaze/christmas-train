"""PF-CT route vehicle/track check (Alt A / Alt B from /workspace/route_redline, read-only input).
Places the real R2/L3 model geometry (build/model.py) on the surveyed centrelines and sweeps the
whole train round each loop in both directions.  Units: mm, N unless noted.
Rev RT1, 28 Oct 2026.  Drive NOT changed (chain/belt decision pending) - uses the adhesion-capped 37.9 kN."""
import sys, csv, json, math
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, "/workspace/train/build")
import model as M

RR = "/workspace/route_redline"
OUT = "/workspace/train/calcs/track"
G = M.GAUGE; HG = G / 2
PLAY = 2 * 6.2            # nominal flangeway play (858 b-t-b, 22 flange)
PLAY_MIN = PLAY - 3.0     # gauge at -3 tolerance
SWAY_DEG = 2.0; ROLL_Z = 500.0
ENV_K401 = 1696.0; FIXED = 2000.0
ROCKL = lambda R_m: 400.0 / (R_m - 20.0) / 1000.0   # N/N (metre-gauge Rockl)
AREMA = lambda R_m: 0.8 * (5729.58 / (R_m / 0.3048)) / 2000.0  # 0.8 lb/ton/deg -> N/N

# ------------------------------------------------------------------ alignment
def synth_els(spec):
    """spec: list of ('T', L_m) or ('C', R_m, defl_deg, 'L'|'R'); returns curve-table-like dicts"""
    E, N, b = 0.0, 0.0, 0.0; els = []
    for it in spec:
        if it[0] == "T":
            els.append(dict(type="tangent", length_m=it[1], start_E=E, start_N=N, bearing_deg=b))
            E += it[1] * math.sin(math.radians(b)); N += it[1] * math.cos(math.radians(b))
        else:
            R, dd, side = it[1], it[2], it[3]; sg = 1 if side == "L" else -1
            br = math.radians(b); nx, ny = (-math.cos(br), math.sin(br)) if sg > 0 else (math.cos(br), -math.sin(br))
            cx, cy = E + R * nx, N + R * ny
            els.append(dict(type="circular curve", length_m=R * math.radians(dd), radius_m=R, start_E=E, start_N=N,
                            centre_E=cx, centre_N=cy, direction="L (CCW)" if sg > 0 else "R (CW)", bearing_deg=b))
            ph0 = math.atan2(N - cy, E - cx) + sg * math.radians(dd)
            E, N = cx + R * math.cos(ph0), cy + R * math.sin(ph0); b = (b - sg * dd) % 360
    return els

def load_alignment(tag, els=None):
    if els is None:
        els = list(csv.DictReader(open(f"{RR}/{tag}_curve_table.csv")))
    E0, N0 = float(els[0]["start_E"]), float(els[0]["start_N"])
    pts, curv, s_acc = [], [], 0.0
    ds = 50.0
    for e in els:
        L = float(e["length_m"]) * 1000
        n = max(2, int(round(L / ds)))
        t = np.linspace(0, L, n, endpoint=False)
        sx, sy = (float(e["start_E"]) - E0) * 1000, (float(e["start_N"]) - N0) * 1000
        if e["type"] == "tangent":
            b = math.radians(float(e["bearing_deg"]))
            x = sx + t * math.sin(b); y = sy + t * math.cos(b); k = np.zeros(n)
        else:
            R = float(e["radius_m"]) * 1000
            cx, cy = (float(e["centre_E"]) - E0) * 1000, (float(e["centre_N"]) - N0) * 1000
            ph0 = math.atan2(sy - cy, sx - cx); sg = 1 if "CCW" in e["direction"] else -1
            ph = ph0 + sg * t / R
            x = cx + R * np.cos(ph); y = cy + R * np.sin(ph); k = np.full(n, sg / R)
        pts.append(np.c_[x, y]); curv.append(k)
    P = np.vstack(pts); K = np.concatenate(curv)
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(np.vstack([P, P[:1]]), axis=0).T))]
    Ltot = d[-1]; S = d[:-1]
    clos = float(np.hypot(*(P[-1] - P[0])))
    return dict(tag=tag, els=els, P=P, K=K, S=S, L=Ltot, tree=cKDTree(P), close_gap=clos)

def Pof(A, s):
    s = np.mod(s, A["L"]); S = np.r_[A["S"], A["L"]]; P = np.vstack([A["P"], A["P"][:1]])
    return np.c_[np.interp(s, S, P[:, 0]), np.interp(s, S, P[:, 1])]

def offset(A, W):
    """signed lateral offset of world points W (n,2) from centreline: + = left of travel(+s); also curvature there"""
    d, i = A["tree"].query(W)
    j = (i + 1) % len(A["P"]); t = A["P"][j] - A["P"][i]; t /= np.linalg.norm(t, axis=1)[:, None]
    v = W - A["P"][i]; sgn = np.sign(t[:, 0] * v[:, 1] - t[:, 1] * v[:, 0])
    return d * sgn, A["K"][i]

# ------------------------------------------------------------------ vehicles from model.py
def bbox(p):
    if p["t"] == "B": return p["x0"], p["x1"], p["y0"], p["y1"], p["z0"], p["z1"]
    r = p["r"]
    if p["axis"] == "x": return p["a0"], p["a1"], p["c1"] - r, p["c1"] + r, p["c2"] - r, p["c2"] + r
    if p["axis"] == "y": return p["c1"] - r, p["c1"] + r, p["a0"], p["a1"], p["c2"] - r, p["c2"] + r
    return p["c1"] - r, p["c1"] + r, p["c2"] - r, p["c2"] + r, p["a0"], p["a1"]

TRUCK_GRP = {"axle", "wheel", "truck", "drive", "motor", "rods"}
def build_vehicles():
    L, T, C = M.LOCO, M.TENDER, M.COACH
    V = []
    def mk(name, prims, piv, a, pins, mass, mass_e, trucks, lead=None):
        parts = []
        for p in prims:
            bb = bbox(p)
            xc = (bb[0] + bb[1]) / 2
            if p["grp"] in TRUCK_GRP:
                if lead and ("lead" in p["name"] or "leading" in p["name"]): part = "LT"
                else: part = min(trucks, key=lambda t: abs(t[0] - xc))[1]
            else: part = "B"
            parts.append(dict(bb=bb, part=part, name=p["name"], grp=p["grp"]))
        return dict(name=name, parts=parts, piv=piv, a=a, pins=pins, mass=mass, mass_e=mass_e,
                    trucks={t[1]: t[0] for t in trucks}, lead=lead)
    V.append(mk("Locomotive", M.locomotive(), L["piv"], L["wb"] / 2, (None, L["len_pin"]), 17667, 17667,
                [(L["piv"][0], "T1"), (L["piv"][1], "T2")],
                lead=dict(axles=L["lead_axles"], anchor=L["lead_anchor"], arm=L["lead_anchor"] - sum(L["lead_axles"]) / 2)))
    V.append(mk("Tender", M.tender(), T["piv"], 600.0, (T["front_pin"], T["rear_pin"]), 8304, 8304,
                [(T["piv"][0], "T1"), (T["piv"][1], "T2")]))
    for i in range(4):
        acc = i == 3
        V.append(mk(f"Coach {i+1}" + (" (acc)" if acc else ""), M.coach(acc), C["bolsters"], 600.0, C["pin"],
                    11000 if acc else 13200, 7000 if acc else 8040,
                    [(C["bolsters"][0], "T1"), (C["bolsters"][1], "T2")]))
    return V

def tc(A, s, a):
    p1, p2 = Pof(A, np.array([s + a, s - a]))
    c = (p1 + p2) / 2; h = p1 - p2; h /= np.linalg.norm(h)
    return c, h

from scipy.optimize import brentq
def solve(f, lo, hi, it=60):
    try:
        return brentq(f, lo, hi, xtol=1e-3)
    except ValueError:
        pass
    flo = f(lo)
    for _ in range(it):
        mid = (lo + hi) / 2; fm = f(mid)
        if (fm > 0) == (flo > 0): lo, flo = mid, fm
        else: hi = mid
    return (lo + hi) / 2

def rot_r(h): return np.array([h[1], -h[0]])   # right-hand normal (model +Y = right)

def place_vehicle(A, v, s1):
    """front pivot at arc s1 -> frames for body and trucks"""
    xf, xr = v["piv"]; Lp = xr - xf
    c1, h1 = tc(A, s1, v["a"])
    s2 = solve(lambda s: np.linalg.norm(tc(A, s, v["a"])[0] - c1) - Lp, s1 - Lp * 1.2, s1 - Lp * 0.8)
    c2, h2 = tc(A, s2, v["a"])
    e = (c1 - c2) / np.linalg.norm(c1 - c2)
    fr = {"B": (c1, e, xf), "T1": (c1, h1, xf), "T2": (c2, h2, xr)}
    out = dict(s1=s1, s2=s2, fr=fr, e=e)
    if v["lead"]:
        ld = v["lead"]; xlc = sum(ld["axles"]) / 2; al = (ld["axles"][1] - ld["axles"][0]) / 2
        anc = c1 + (xf - ld["anchor"]) * e
        sl = solve(lambda s: np.linalg.norm(tc(A, s, al)[0] - anc) - ld["arm"], s1 + (ld["anchor"] and (xf - ld["anchor"])) + 50, s1 + 4000)
        cl, hl = tc(A, sl, al)
        arm = (cl - anc) / np.linalg.norm(cl - anc)
        out["lead"] = dict(sl=sl, c=cl, h=hl, arm=arm, swing=float(np.dot(cl - anc, rot_r(e))),
                           aoa=math.degrees(math.asin(max(-1, min(1, arm[0] * hl[1] - arm[1] * hl[0])))))
        fr["LT"] = (cl, hl, xlc)
    return out

def to_world(fr, X, Y):
    c, h, xo = fr
    n = rot_r(h)
    return c[None, :] + (xo - X)[:, None] * h[None, :] + Y[:, None] * n[None, :]

def pin_world(pl, v, which):
    X = v["pins"][which]
    return to_world(pl["fr"]["B"], np.array([X]), np.array([0.0]))[0]

def place_train(A, V, s_front):
    out = []
    pl = place_vehicle(A, V[0], s_front); out.append(pl)
    dbs = [M.DB_LT] + [M.DB_STD] * 4
    for k in range(1, len(V)):
        prev = out[-1]; pv = V[k - 1]; v = V[k]
        wp = pin_world(prev, pv, 1)
        dist_pin_piv = v["piv"][0] - v["pins"][0]
        guess = prev["s2"] - (pv["pins"][1] - pv["piv"][1]) - dbs[k - 1] - dist_pin_piv
        f = lambda s: np.linalg.norm(pin_world(place_vehicle(A, v, s), v, 0) - wp) - dbs[k - 1]
        s = solve(lambda s: -f(s), guess - 1500, guess + 1500, it=40)
        out.append(place_vehicle(A, v, s))
    return out

# ------------------------------------------------------------------ envelope points
def env_points(v):
    """outer plan corners of prims reaching |y| > 600 or near ends, with z top for sway"""
    X, Y, Z, NM, PT = [], [], [], [], []
    xs = [p["bb"][0] for p in v["parts"]] + [p["bb"][1] for p in v["parts"]]
    xmin, xmax = min(xs), max(xs)
    for p in v["parts"]:
        x0, x1, y0, y1, z0, z1 = p["bb"]
        if max(abs(y0), abs(y1)) < 600 and x0 > xmin + 400 and x1 < xmax - 400: continue
        for xx in (x0, x1):
            for yy in (y0, y1):
                X.append(xx); Y.append(yy); Z.append(z1); NM.append(p["name"]); PT.append(p["part"])
    return np.array(X), np.array(Y), np.array(Z), NM, PT

def sweep(A, V, step=1000.0, reverse=False, s_range=None):
    if reverse:
        A = dict(A); A["P"] = A["P"][::-1].copy(); A["K"] = -A["K"][::-1].copy()
        d = np.r_[0, np.cumsum(np.hypot(*np.diff(np.vstack([A["P"], A["P"][:1]]), axis=0).T))]
        A["S"] = d[:-1]; A["L"] = d[-1]; A["tree"] = cKDTree(A["P"])
    EP = [env_points(v) for v in V]
    res = {v["name"]: dict(out=-1e9, inn=-1e9, out_s=None, inn_s=None, out_nm="", inn_nm="",
                           out_geo=-1e9, inn_geo=-1e9, low_inn=-1e9, low_out=-1e9) for v in V}
    cpl = [dict(maxang=0, s=None, a1=0, a2=0, a1max=0, a2max=0, bodymax=0) for _ in range(len(V) - 1)]
    lead = dict(swing=0, aoa=0); yawrel = {}
    endgap = [1e9] * (len(V) - 1)
    states = []
    rng = np.arange(0, A["L"], step) if s_range is None else np.arange(s_range[0], s_range[1], step)
    for s in rng:
        tr = place_train(A, V, s)
        states.append((s, tr))
        for k, (v, pl) in enumerate(zip(V, tr)):
            X, Y, Z, NM, PT = EP[k]
            W = np.zeros((len(X), 2))
            for part in set(PT):
                m = np.array([q == part for q in PT])
                W[m] = to_world(pl["fr"][part], X[m], Y[m])
            off, kk = offset(A, W)
            # outside/inside relative to local curvature sign at the vehicle centre
            cv = offset(A, ((pl["fr"]["B"][0] + to_world(pl["fr"]["T2"], np.array([v["piv"][1]]), np.array([0.]))[0]) / 2)[None, :])[1][0]
            if abs(cv) < 1e-9:
                cv = 1e-12
            sg = -np.sign(cv)       # + = outside of curve (away from centre)
            sway = np.maximum(Z - ROLL_Z, 0) * math.sin(math.radians(SWAY_DEG))
            outv = off * sg; r = res[v["name"]]
            # outside: points with outv>0 ; inside: -outv
            o = outv + sway + PLAY / 2; i_ = -outv + sway + PLAY / 2
            io, ii = int(np.argmax(o)), int(np.argmax(i_))
            if o[io] > r["out"]: r.update(out=float(o[io]), out_s=float(s), out_nm=NM[io], out_geo=float(outv[io] - abs(Y[io])), out_R=1e-3 / max(abs(cv), 1e-12))
            if i_[ii] > r["inn"]: r.update(inn=float(i_[ii]), inn_s=float(s), inn_nm=NM[ii], inn_geo=float(-outv[ii] - abs(Y[ii])), inn_R=1e-3 / max(abs(cv), 1e-12))
            low = Z < 1400
            if low.any():
                r["low_out"] = max(r["low_out"], float(o[low].max())); r["low_inn"] = max(r["low_inn"], float(i_[low].max()))
            if v["lead"]:
                lead["swing"] = max(lead["swing"], abs(pl["lead"]["swing"])); lead["aoa"] = max(lead["aoa"], abs(pl["lead"]["aoa"]))
            for tn in ("T1", "T2"):
                h = pl["fr"][tn][1]; e = pl["e"]
                ang = abs(math.degrees(math.asin(max(-1, min(1, e[0] * h[1] - e[1] * h[0])))))
                key = (v["name"], tn); yawrel[key] = max(yawrel.get(key, 0), ang)
        for k in range(len(V) - 1):
            a, b = tr[k], tr[k + 1]
            pa = pin_world(a, V[k], 1); pb = pin_world(b, V[k + 1], 0)
            d = (pa - pb) / np.linalg.norm(pa - pb)
            a1 = math.degrees(math.asin(a["e"][0] * d[1] - a["e"][1] * d[0]))
            a2 = math.degrees(math.asin(b["e"][0] * d[1] - b["e"][1] * d[0]))
            m = max(abs(a1), abs(a2))
            cpl[k]['a1max'] = max(cpl[k]['a1max'], abs(a1)); cpl[k]['a2max'] = max(cpl[k]['a2max'], abs(a2))
            cpl[k]['bodymax'] = max(cpl[k]['bodymax'], abs(math.degrees(math.asin(a['e'][0] * b['e'][1] - a['e'][1] * b['e'][0]))))
            if m > cpl[k]["maxang"]: cpl[k].update(maxang=m, s=float(s), a1=a1, a2=a2, body=math.degrees(math.asin(a["e"][0] * b["e"][1] - a["e"][1] * b["e"][0])))
    return dict(res=res, cpl=cpl, lead=lead, yaw={f"{k[0]} {k[1]}": v for k, v in yawrel.items()}, states=states, A=A)

# ------------------------------------------------------------------ plan interference (rotating parts, vehicle ends)
def rect(fr, bb):
    X = np.array([bb[0], bb[1], bb[1], bb[0]]); Y = np.array([bb[2], bb[2], bb[3], bb[3]])
    return to_world(fr, X, Y)

def poly_gap(P, Q):
    """min distance between convex quads, negative = overlap depth (SAT)"""
    pen = 1e9; sep = False
    for poly in (P, Q):
        for i in range(4):
            ed = poly[(i + 1) % 4] - poly[i]; n = np.array([-ed[1], ed[0]]); nn = np.linalg.norm(n)
            if nn == 0: continue
            n /= nn
            a = P @ n; b = Q @ n
            ov = min(a.max(), b.max()) - max(a.min(), b.min())
            if ov < 0: sep = True
            pen = min(pen, ov)
    if not sep: return -pen
    def ps(p, a, b):
        ab = b - a; t = np.clip(np.dot(p - a, ab) / max(np.dot(ab, ab), 1e-9), 0, 1); return np.linalg.norm(p - (a + t * ab))
    return min(min(ps(p, Q[i], Q[(i + 1) % 4]) for p in P for i in range(4)),
               min(ps(q, P[i], P[(i + 1) % 4]) for q in Q for i in range(4)))

def straight_alignment():
    L = 200000.0; n = 4001
    P = np.c_[np.zeros(n), np.linspace(0, L, n)]
    return dict(tag="straight", P=P, K=np.zeros(n), S=np.linspace(0, L, n), L=L * 1.5, tree=cKDTree(P))

def candidate_pairs(V, trS):
    pairs = []
    for k, (v, pl) in enumerate(zip(V, trS)):
        parts = v["parts"]
        for i, p in enumerate(parts):
            for j in range(i + 1, len(parts)):
                q = parts[j]
                if p["part"] == q["part"]: continue
                if min(p["bb"][5], q["bb"][5]) - max(p["bb"][4], q["bb"][4]) <= 5: continue
                g = poly_gap(rect(pl["fr"][p["part"]], p["bb"]), rect(pl["fr"][q["part"]], q["bb"]))
                if 1.0 < g < 150: pairs.append((k, i, k, j, g))
        if k + 1 < len(V):
            w = V[k + 1]; pw = trS[k + 1]
            for i, p in enumerate(parts):
                if p["bb"][1] < max(pp["bb"][1] for pp in parts) - 1500: continue
                for j, q in enumerate(w["parts"]):
                    if q["bb"][0] > min(qq["bb"][0] for qq in w["parts"]) + 1500: continue
                    if min(p["bb"][5], q["bb"][5]) - max(p["bb"][4], q["bb"][4]) <= 5: continue
                    g = poly_gap(rect(pl["fr"][p["part"]], p["bb"]), rect(pw["fr"][q["part"]], q["bb"]))
                    if 1.0 < g < 1600: pairs.append((k, i, k + 1, j, g))
    return pairs

def interference(V, pairs, states):
    worst = {}
    for s, tr in states:
        for (k, i, k2, j, g0) in pairs:
            p = V[k]["parts"][i]; q = V[k2]["parts"][j]
            g = poly_gap(rect(tr[k]["fr"][p["part"]], p["bb"]), rect(tr[k2]["fr"][q["part"]], q["bb"]))
            key = (k, i, k2, j)
            if key not in worst or g < worst[key][0]: worst[key] = (g, s, g0)
    rows = []
    for (k, i, k2, j), (g, s, g0) in worst.items():
        p = V[k]["parts"][i]; q = V[k2]["parts"][j]
        rows.append(dict(a=f'{V[k]["name"]}:{p["part"]} {p["name"]}', b=f'{V[k2]["name"]}:{q["part"]} {q["name"]}',
                         static=round(g0, 1), min_gap=round(g, 1), at_ch_m=round(s / 1000, 1), loss=round(g0 - g, 1)))
    rows.sort(key=lambda r: r["min_gap"])
    return rows

# ------------------------------------------------------------------ refined round-geometry check: lead wheel rim vs T1 decorative cylinders
def cyl_wheel_gap(V, tr, cy=750.0, cz=725.0):
    """samples the outer rim face (y = +/-(HG+90)) of both lead wheels (Ø650) and measures the radial gap to the
    Ø380 decorative cylinders (axis y=+/-cy, z=cz, X1950-2450, on truck T1). Returns min gap (mm) BEFORE axle play."""
    L = M.LOCO; pl = tr[0]
    rl = L["lead_wheel"] / 2; yf = HG + 90
    best = 1e9
    hs = np.linspace(-rl, rl, 41); vs = np.linspace(0, rl, 21)
    H, Vv = np.meshgrid(hs, vs); m = H**2 + Vv**2 <= rl**2
    H = H[m]; Vv = Vv[m]
    for ax in L["lead_axles"]:
        for s_ in (1, -1):
            X = ax + H; Y = np.full_like(X, s_ * yf); Z = rl + Vv
            Wp = to_world(pl["fr"]["LT"], X, Y)
            c, h, xo = pl["fr"]["T1"]; n = rot_r(h)
            d = Wp - c[None, :]
            Xt = xo - d @ h; Yt = d @ n
            inx = (Xt >= 1950) & (Xt <= 2450)
            if not inx.any(): continue
            for sc in (1, -1):
                g = np.hypot(Yt[inx] - sc * cy, Z[inx] - cz) - 190
                best = min(best, float(g.min()))
    return best

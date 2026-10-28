"""L-107 calc note engine: grillage (w, dw/dX, dw/dY) for vertical cases, diaphragm share for horizontal,
bracket load table, member/plate/bolt checks, mass take-off.  Loco Bot P1 - PRELIMINARY, for Grokky / NV PE review."""
import math, json, csv, sys
import numpy as np
sys.path.insert(0, '/workspace/loco/l107L')
import geom as G
G.LINES["SS+"] = (G.LINES["SS+"][0], "HSS3x3x1/8"); G.LINES["SS-"] = (G.LINES["SS-"][0], "HSS3x3x1/8")  # S17 P-A1 adopted
g = 9.80665
PSF100 = 4.788e-3          # N/mm2 (100 psf)
P300 = 1334.5              # N (300 lb)
# ---------------------------------------------------------------- nodes
SX = [s[1] for s in G.STATIONS]
xs_extra = set()
for i in range(len(SX)-1):           # subdivide spans into 8 for accurate moments
    for k in range(1, 8): xs_extra.add(round(SX[i] + (SX[i+1]-SX[i])*k/8, 1))
for x in G.BALLAST_HDR_X: xs_extra.add(x)
for x in (6000.0, 7600.0, 8000.0, 10700.0): xs_extra.add(x)
XL = sorted(set(SX) | xs_extra)
LY = {k: v[0] for k, v in G.LINES.items()}
nodes = {}; 
def nid(x, y):
    key = (round(x, 1), round(y, 1))
    if key not in nodes: nodes[key] = len(nodes)
    return nodes[key]
elems = []   # (n1, n2, dir 'X'|'Y', sec, L, tag)
for name, (y, sec) in G.LINES.items():
    for i in range(len(XL)-1):
        elems.append((nid(XL[i], y), nid(XL[i+1], y), 'X', sec, XL[i+1]-XL[i], name))
BY = sorted(set([-G.BEARER_Y, -665.0, -G.RAIL_Y, 0.0, G.RAIL_Y, 665.0, G.BEARER_Y] +
                [v for y in (-1, 1) for v in np.linspace(0, 1, 5)[1:-1] * 0]))
def subdiv(a, b, n):
    return [a + (b-a)*k/n for k in range(n+1)]
BYS = sorted(set(round(v, 1) for v in (subdiv(-1170, -665, 4) + subdiv(-665, -240, 3) + subdiv(-240, 0, 2) +
                                         subdiv(0, 240, 2) + subdiv(240, 665, 3) + subdiv(665, 1170, 4)) + [250.0, -250.0, 480.0, -480.0, 300.0, -300.0, 600.0, -600.0]))
for (mk, x, sec, typ, note) in G.STATIONS:
    for i in range(len(BYS)-1):
        elems.append((nid(x, BYS[i]), nid(x, BYS[i+1]), 'Y', sec, BYS[i+1]-BYS[i], mk))
HYS = subdiv(665, 1170, 4); HYS = sorted(set(HYS + [700.0, 1020.0]))
for x in G.BALLAST_HDR_X:
    for s in (-1, 1):
        ys = sorted(s*v for v in HYS)
        for i in range(len(ys)-1):
            elems.append((nid(x, ys[i]), nid(x, ys[i+1]), 'Y', "C4x5.4", ys[i+1]-ys[i], "BH"))
N = len(nodes); ndof = 3*N
coords = {v: k for k, v in nodes.items()}
def kel(L, EI, GJ):
    k = EI/L**3*np.array([[12, 6*L, -12, 6*L], [6*L, 4*L*L, -6*L, 2*L*L], [-12, -6*L, 12, -6*L], [6*L, 2*L*L, -6*L, 4*L*L]])
    return k, GJ/L*np.array([[1, -1], [-1, 1]])
def kel_h(L, EI, hinge):
    """beam with moment release at end 'a', 'b' or 'ab' (DOF order w1 th1 w2 th2)"""
    if hinge == 'ab': return np.zeros((4, 4))
    c = 3*EI/L**3
    if hinge == 'b': v = np.array([1, L, -1, 0.0])
    else:            v = np.array([1, 0.0, -1, L])
    k = c*np.outer(v, v) / 1.0
    # correct form: for release at b, k = 3EI/L^3 * [[1,L,-1],[L,L^2,-L],[-1,-L,1]] on (w1,th1,w2)
    return k
STN_X = set(round(st[1], 1) for st in G.STATIONS)
PINNED = ("SC", "SS+", "SS-", "BH")   # framed between bearers / stringers with bolted shear tabs
def hinge_of(a, b, d, tag):
    if tag not in PINNED: return None
    if d == 'X':
        ha = round(coords[a][0], 1) in STN_X; hb = round(coords[b][0], 1) in STN_X
    else:   # ballast header ends at SS (|Y|665) and edge (|Y|1170)
        ha = abs(coords[a][1]) in (665.0, 1170.0); hb = abs(coords[b][1]) in (665.0, 1170.0)
    return ('ab' if ha and hb else 'a' if ha else 'b' if hb else None)
K = np.zeros((ndof, ndof))
for (a, b, d, sec, L, tag) in elems:
    S = G.SEC[sec]; kb, kt = kel(L, S.get("E", G.E_STEEL)*S["I"], S.get("G", G.G_STEEL)*S["J"])
    h = hinge_of(a, b, d, tag)
    if h: kb = kel_h(L, S.get("E", G.E_STEEL)*S["I"], h)
    if tag in PINNED: kt = kt*1e-4          # shear-tab ends: no torsional continuity (small stabilising value)
    if d == 'X': bd = [3*a, 3*a+1, 3*b, 3*b+1]; td = [3*a+2, 3*b+2]
    else:        bd = [3*a, 3*a+2, 3*b, 3*b+2]; td = [3*a+1, 3*b+1]
    K[np.ix_(bd, bd)] += kb; K[np.ix_(td, td)] += kt
sup = {}   # node -> (station mark, side)
for (mk, x, sec, typ, note) in G.STATIONS:
    for s in (-1, 1): sup[nid(x, s*G.RAIL_Y)] = (mk, s, typ)
fixed = [3*n for n in sup] + [3*n+1 for n in sup]   # w and bearer roll (dw/dX) held by bracket clip
free = [i for i in range(ndof) if i not in fixed]
Kff = K[np.ix_(free, free)]
def solve(F):
    u = np.zeros(ndof); u[free] = np.linalg.solve(Kff, F[free])
    R = K @ u - F
    return u, R
def nearest_x(x): return min(XL, key=lambda v: abs(v-x))
# ---------------------------------------------------------------- load builders (F = +down)
TRIB = {"SC": 665.0, "SS+": 625.0, "SS-": 625.0, "EA+": 292.5 + 80.0, "EA-": 292.5 + 80.0}  # deck strip to Y1250
def line_load(F, q_of_line, xr=(G.X0_DECK, G.X1_DECK)):
    for (a, b, d, sec, L, tag) in elems:
        if d != 'X' or tag not in q_of_line: continue
        xa, xb = coords[a][0], coords[b][0]
        lo, hi = max(xa, xr[0]), min(xb, xr[1])
        if hi <= lo: continue
        w = q_of_line[tag]*(hi-lo)
        F[3*a] += w/2; F[3*b] += w/2
    # deck overhang X300->B1 and B9->10900 assigned to end nodes (small)
def self_weight(F, fac=1.0):
    for (a, b, d, sec, L, tag) in elems:
        w = G.SEC[sec]["m"]*L/1000*g*fac
        F[3*a] += w/2; F[3*b] += w/2
    q = {k: v*G.DECK["kgm2"]*1e-6*g*fac for k, v in TRIB.items()}  # floor plate 11.26 psf
    line_load(F, q)
def point(F, x, y, P):
    # distribute to the two adjacent longitudinal lines at x (lever rule), node at nearest grid x
    ys = sorted(v for v in LY.values())
    x = nearest_x(x)
    if (round(x, 1), round(y, 1)) in nodes: F[3*nodes[(round(x, 1), round(y, 1))]] += P; return
    lo = max(v for v in ys if v <= y); hi = min(v for v in ys if v >= y)
    t = (y-lo)/(hi-lo); F[3*nid(x, lo)] += P*(1-t); F[3*nid(x, hi)] += P*t
def node_load(F, x, y, P): F[3*nid(x, y)] += P
# ---------------------------------------------------------------- equipment (m kg, list of (x,y) feet, zcg)
EQUIP = {
 "ballast": dict(m=1500.0, feet=[(x, s*y) for x in G.BALLAST_HDR_X for s in (-1, 1) for y in G.BALLAST_ROD_Y], z=1732.0,
                 src="L-105 / C9: 750 kg per side max (4x M20 rods per side, re-sited to L-107 ballast headers)"),
 "air_reservoirs": dict(m=150.0, feet=[(x, s*900.0) for x in (6000.0, 7600.0) for s in (-1, 1)], z=1765.0,
                 src="ASSUMED 2 x 75 kg MR/BP reservoirs incl. saddles (styling loco_L1 Y+/-900 X5900-7700); B-601 to confirm"),
}
PROV = {
 "shell_M2_L108": dict(m=2331.6, feet=[(x, s*y) for x in (1525.0, 2450.0, 5675.0, 7275.0) for s in (-1, 1) for y in (300.0, 600.0)] + [(4075.0, s*y) for s in (-1, 1) for y in (250.0, 480.0)], z=2560.0,
                 src="S17: L-108 barrel 2,280.6 incl. saddles (S4N) + L-110 fittings 51.0; S4N at B4 bolts Y+/-250/480"),
 "smokebox_L109": dict(m=227.9, feet=[(480.0, s*y) for s in (-1, 1) for y in (300.0, 600.0)], z=2560.0, src="S17: L-109 rev A 227.9 on S1 at B1, L-108 style Y+/-300/600"),
 "cab_M7_L111": dict(m=813.9, feet=[(x, s*1170.0) for x in (8000.0, 8900.0, 9900.0, 10700.0) for s in (-1, 1)], z=2722.0,
                 src="cab C1 APPROVED (Grokky 28 Oct), l111/parts_out.json; sill on edge lines"),
}
def eq_vert(F, eqs, gfac):
    for e in eqs.values():
        P = e["m"]*g*gfac/len(e["feet"])
        for (x, y) in e["feet"]: point(F, x, y, P)
def eq_pitch(F, eqs, ax_g):
    """vertical couple from longitudinal accel ax_g at CG height above support plane, applied over the item's feet"""
    for e in eqs.values():
        xs = sorted(set(f[0] for f in e["feet"]));
        if len(xs) < 2: continue
        Fx = e["m"]*g*ax_g; h = e["z"] - G.ZS; M = Fx*h
        x0, x1 = xs[0], xs[-1]; dP = M/(x1-x0)
        n0 = [f for f in e["feet"] if f[0] == x0]; n1 = [f for f in e["feet"] if f[0] == x1]
        for (x, y) in n1: point(F, x, y, +dP/len(n1))     # decel/accel sign: front-heavy -> rear feet + (envelope by symmetry)
        for (x, y) in n0: point(F, x, y, -dP/len(n0))
def eq_roll(F, eqs, ay_g):
    for e in eqs.values():
        Fy = e["m"]*g*ay_g; h = e["z"] - G.ZS
        for side in (-1, 1):
            fs = [f for f in e["feet"] if f[1]*side > 0]
            if not fs: continue
            ys = sorted(abs(f[1]) for f in fs); w = 2*min(ys) if len(set(ys)) == 1 else (max(ys)-min(ys))
        # couple resisted between left and right feet groups
        L = [f for f in e["feet"] if f[1] < 0]; R = [f for f in e["feet"] if f[1] > 0]
        arm = (np.mean([f[1] for f in R]) - np.mean([f[1] for f in L]))
        dP = Fy*h/arm
        for f in R: point(F, f[0], f[1], +dP/len(R))
        for f in L: point(F, f[0], f[1], -dP/len(L))
# ---------------------------------------------------------------- load cases
def F0(): return np.zeros(ndof)
cases = {}
F = F0(); self_weight(F); cases["LC0 DL (structure + deck)"] = F
F = F0(); self_weight(F); line_load(F, {k: PSF100*v for k, v in TRIB.items()}); cases["LC1 DL + 100 psf full deck"] = F
F = F0(); self_weight(F); line_load(F, {k: PSF100*v for k, v in TRIB.items() if k in ("SC", "SS+", "EA+")}); cases["LC2 DL + 100 psf one side (Y+)"] = F
pt_locs = [(x, 1170.0) for x in SX] + [((SX[i]+SX[i+1])/2, y) for i in range(len(SX)-1) for y in (0.0, 665.0, 1170.0)]
F = F0(); self_weight(F); eq_vert(F, EQUIP, 2.0); cases["LC4 DL + equipment 2 g vertical"] = F
F = F0(); self_weight(F); eq_vert(F, {**EQUIP, **PROV}, 2.0); cases["LC4P DL + equipment + PROV shell/cab 2 g vertical"] = F
F = F0(); self_weight(F); eq_vert(F, EQUIP, 1.0); eq_pitch(F, EQUIP, 3.0); cases["LC5 DL + equip 1 g + 3 g longitudinal (pitch couple)"] = F
F = F0(); self_weight(F); eq_vert(F, {**EQUIP, **PROV}, 1.0); eq_pitch(F, {**EQUIP, **PROV}, 3.0); cases["LC5P same incl. PROV shell/cab"] = F
F = F0(); self_weight(F); eq_vert(F, EQUIP, 1.0); eq_roll(F, EQUIP, 1.0); cases["LC6 DL + equip 1 g + 1 g lateral (roll couple)"] = F
F = F0(); self_weight(F); eq_vert(F, {**EQUIP, **PROV}, 1.0); eq_roll(F, {**EQUIP, **PROV}, 1.0); cases["LC6P same incl. PROV shell/cab"] = F
F = F0(); self_weight(F, 0.9); eq_vert(F, EQUIP, -1.0); cases["LC7 0.9 DL + equipment 1 g net UP"] = F
F = F0(); self_weight(F, 0.9); eq_vert(F, {**EQUIP, **PROV}, -1.0); cases["LC7P same incl. PROV shell/cab"] = F
results = {}
for name, Fc in cases.items():
    u, R = solve(Fc); results[name] = (u, R)
# point-load envelope (LC3)
lc3 = []
for (x, y) in pt_locs:
    F = F0(); self_weight(F); point(F, x, y, P300); u, R = solve(F); lc3.append(((x, y), u, R))
# ---------------------------------------------------------------- horizontal shares (to RB brackets only)
def mass_struct():
    return sum(G.SEC[sec]["m"]*L/1000 for (a, b, d, sec, L, tag) in elems) + 26.5*G.DECK["kgm2"]
M_STRUCT = mass_struct()
nRB = 2*len(G.stations_rb())
def horiz(eqs):
    m = M_STRUCT + sum(e["m"] for e in eqs.values())
    return dict(Fx_per_RB=3*g*m/nRB, Fy_per_RB_tension=1*g*m/len(G.stations_rb()), m=m)
H = horiz(EQUIP); HP = horiz({**EQUIP, **PROV})
# ---------------------------------------------------------------- bracket table
rows = []
def reac(R, mk, s):
    x = [st[1] for st in G.STATIONS if st[0] == mk][0]
    return -R[3*nid(x, s*G.RAIL_Y)]   # +down on rail (reaction sign flipped)
for (mk, x, sec, typ, note) in G.STATIONS:
    for s in (-1, 1):
        r = dict(station=mk, X=x, side="R (Y+)" if s > 0 else "L (Y-)", type=typ)
        for name, (u, R) in results.items():
            r[name.split(" ")[0]] = round(-reac(R, mk, s)/1000, 2)   # kN, + = DOWN onto rail
        pts = [-reac(R, mk, s) for (_, u, R) in lc3]
        r["LC3max"] = round(max(pts)/1000, 2); r["LC3min"] = round(min(pts)/1000, 2)
        r["Fx_3g"] = round(H["Fx_per_RB"]/1000, 2) if typ == "RB" else 0.0
        r["Fx_3gP"] = round(HP["Fx_per_RB"]/1000, 2) if typ == "RB" else 0.0
        r["Fy_1g"] = round(H["Fy_per_RB_tension"]/1000, 2) if typ == "RB" else 0.0
        r["Fy_1gP"] = round(HP["Fy_per_RB_tension"]/1000, 2) if typ == "RB" else 0.0
        rows.append(r)
# fix sign: reactions R = K u - F ; at support R is the support force on structure (+up in our +down convention => negative)
for r in rows:
    for k in list(r):
        if k.startswith("LC") and k not in ("LC3max", "LC3min"): r[k] = -r[k]
    r["LC3max"], r["LC3min"] = -r["LC3min"], -r["LC3max"]
vcols = [k for k in rows[0] if k.startswith("LC")]
for r in rows:
    vals = [r[k] for k in vcols]
    r["Fz_down_max"] = round(max(vals), 2); r["Fz_up_max"] = round(max(0.0, -min(vals)), 2)
# ---------------------------------------------------------------- member stresses (max over cases)
def member_forces(u):
    out = {}
    for (a, b, d, sec, L, tag) in elems:
        S = G.SEC[sec]; kb, kt = kel(L, S.get("E", G.E_STEEL)*S["I"], S.get("G", G.G_STEEL)*S["J"])
        h = hinge_of(a, b, d, tag)
        if h: kb = kel_h(L, S.get("E", G.E_STEEL)*S["I"], h)
        bd = [3*a, 3*a+1, 3*b, 3*b+1] if d == 'X' else [3*a, 3*a+2, 3*b, 3*b+2]
        f = kb @ u[bd]
        M = max(abs(f[1]), abs(f[3]))
        key = tag if tag in ("SC", "SS+", "SS-", "EA+", "EA-", "BH") else ("bearer " + sec)
        out[key] = max(out.get(key, 0), M)
    return out
mem = {}
allres = list(results.items()) + [(f"LC3 P300 at {p}", (u, R)) for (p, u, R) in lc3]
for name, (u, R) in allres:
    for k, M in member_forces(u).items():
        if M > mem.get(k, (0, ""))[0]: mem[k] = (M, name)
sec_of = {"SC": G.LINES["SC"][1], "SS+": G.LINES["SS+"][1], "SS-": G.LINES["SS-"][1], "EA+": G.LINES["EA+"][1], "EA-": G.LINES["EA-"][1], "BH": "C4x5.4",
          "bearer HSS5x3x3/16": "HSS5x3x3/16"}
checks = []
def chk(id_, desc, demand, cap, unit, basis):
    checks.append(dict(id=id_, desc=desc, demand=round(demand, 2), capacity=round(cap, 2), unit=unit, util=round(demand/cap, 2),
                       result="OK" if demand <= cap else "NG", basis=basis))
for k in ("bearer HSS5x3x3/16", "SC", "SS+", "EA+", "BH"):
    M, case = mem[k]; S = G.SEC[sec_of[k]]
    chk(f"L7-M {k}", f"{k} ({sec_of[k]}) max bending, governing: {case}", M/S["S"], 0.6*S["Fy"], "MPa", "ASD 0.6 Fy (C9a convention for g-cases)")
# deflections (LL only): LC1 minus LC0
u1 = results["LC1 DL + 100 psf full deck"][0] - results["LC0 DL (structure + deck)"][0]
wmax = max(u1[3*n] for n in range(N)); chk("L7-D1", "Grillage max live defl. 100 psf (governs at bearer tip, cantilever 930)", wmax, 2*930/360, "mm", "2Lc/360 (cantilever)")
wmid = max(u1[3*nid(x, y)] - 0.5*(u1[3*nid(SX[i], y)] + u1[3*nid(SX[i+1], y)]) for i in range(len(SX)-1) for y in (0.0, 665.0, 1170.0) for x in [nearest_x((SX[i]+SX[i+1])/2)])
chk("L7-D1b", "Stringer/edge mid-bay live defl. relative to bearers, 100 psf (max bay 1,625)", wmid, 1625/360, "mm", "L/360")
u3 = max((u[3*n] - results["LC0 DL (structure + deck)"][0][3*n] for (_, u, R) in lc3 for n in range(N)))
chk("L7-D2", "Grillage max deflection under 300 lb point (members)", u3, 1625/240, "mm", "L/240")
# deck (P1-L: aluminium tread plate, continuous over SC/SS/EA lines)
DK = G.DECK; t = DK["t"]; Ed = DK["E"]; D = Ed*t**3/(12*(1-0.33**2))
for span, lbl in ((665-38.1, "SC->SS clear span 627"), (1243.65-665-17.9, "SS->edge clear span 561")):
    wd = 0.01695*P300*span**2/D
    r0 = 28.2; Mp = P300/(4*math.pi)*((1+0.33)*math.log(2*span/(math.pi*r0)) + 1)
    chk(f"L7-P1 {lbl}", f"Deck {DK['name'][:28]}, 300 lb on 50x50 patch, bending", 6*Mp/t**2, DK["Fall"], "MPa", "0.6 Fty (ADM)")
    chk(f"L7-P2 {lbl}", "Deck deflection 300 lb point (w = 0.01695 P L^2 / D)", wd, span/240, "mm", "L/240 (as C10b)")
    q = PSF100; Mu = q*span**2/8; du = q*span**4/(185*Ed*t**3/12)
    chk(f"L7-P3 {lbl}", "Deck 100 psf, continuous over stringers, bending", 6*Mu/t**2, DK["Fall"], "MPa", "0.6 Fty")
    chk(f"L7-P4 {lbl}", "Deck 100 psf deflection (2-span, wL^4/185EI)", du, span/360, "mm", "L/360")
# ---------------------------------------------------------------- bracket (RB-1) checks; criteria cases taken separately (Grokky)
rb = [r for r in rows if r["type"] == "RB"]; sd = [r for r in rows if r["type"] != "RB"]
Fz_dn = max(r["Fz_down_max"] for r in rows)*1e3
Fz_up = max(r["Fz_up_max"] for r in rb)*1e3
Fx = HP["Fx_per_RB"]; FyP = HP["Fy_per_RB_tension"]
RBd = G.RB; e_y = G.RAIL_OUT - G.RAIL_Y            # 76 mm: reaction at rail CL vs web face
z_load = G.CAP_TOP - 6                                # load introduced at mid cap 1465.65
zb, zf, s_b = RBd["bolt_z"], RBd["wp_z0"], 2*RBd["bolt_dx"]
# (i) uplift (LC2/LC7): pry about cap/web contact at cap underside
T_up = Fz_up*e_y/(G.CAP_BOT - zb)/2;  V_up = Fz_up/2
# (ii) 1 g lateral: half by bearing of the opposite-side WP on its web, half by pull on this side, fulcrum WP toe
T_y = FyP*(z_load - zf)/(zb - zf)/2
# (iii) 3 g longitudinal: direct shear + in-plane couple on the bolt pair
V_x = math.hypot(Fx/2, Fx*(z_load - zb)/s_b)
for cid, T, V, txt in (("L7-B1", T_up, V_up, "LC2/LC7 uplift"), ("L7-B2", T_y, 0.0, "1 g lateral incl. PROV"), ("L7-B3", 0.0, V_x, "3 g longitudinal incl. PROV")):
    chk(cid, f"HB16 per bolt, {txt}: T={T/1e3:.1f} kN, V={V/1e3:.1f} kN, interaction T/21+V/30", T/G.HB16["swl_T"] + V/G.HB16["swl_V"], 1.0, "-", "Lindapter SWL 5:1, linear")
A_sp = RBd["w"]*(G.RAIL_OUT - G.RAIL_IN - 2*20)
chk("L7-B4", "Cap bearing on rail top (200 x 112 flat) at max down reaction", Fz_dn/A_sp, 0.9*250, "MPa", "0.9Fy")
Rn = 2*345*8.86*(5*13.3 + RBd["w"])/1.5
chk("L7-B5", "HSS12x6x3/8 web local yielding under cap (AISC J10.2, 2 webs)", Fz_dn, Rn, "N", "as L1-J")
Lw = 2*RBd["w"]; te = 0.707*6
f = math.hypot((Fz_dn + 0)/(Lw*te), Fx/(Lw*te))
chk("L7-B6", "RB-1 WP-to-CP fillet 6 mm both sides x200 (shop), max down + 3 g long", f, 145, "MPa", "E70 0.3x483 (as D2-f)")
Vcl = max(Fz_dn, Fz_up, Fx)/2
chk("L7-B7", "Clip CL to bearer, 2x M16 8.8 through HSS5x3 (snug, bearing type), per bolt", Vcl, 0.45*800*157/2.0, "N", "AISC J3 Fnv 0.45Fu /2.0")
chk("L7-B8", "HSS5x3x3/16 wall bearing at M16 (2 walls)", Vcl, 2*2.4*16*4.43*427/2.0, "N", "AISC J3.10 2.4dtFu /2.0")
Mwp = FyP/2*(z_load - zb); Swp = RBd["w"]*RBd["wp_t"]**2/6
chk("L7-B9", "RB-1 web plate PL12 bending at bolt line, 1 g lateral pull", Mwp/Swp, 0.6*250, "MPa", "0.6Fy")
sd_up = max(r["Fz_up_max"] for r in sd)*1e3
chk("L7-S1", "SD-1/SD-2 saddle hold-down, 1x HB16 per side, max uplift (tension)", sd_up, G.HB16["swl_T"], "N", "Lindapter SWL 5:1")
chk("L7-S2", "SD saddle 1 g lateral: lateral by 6-RB system; saddle leg is locator only", 0, 1, "-", "info")
# saddle stations: uplift check (compression-only)
summary = dict(M_STRUCT=round(M_STRUCT, 1), horiz=H, horizP=HP, Fz_down_max_kN=round(Fz_dn/1e3, 2), Fz_up_RB_kN=round(Fz_up/1e3, 2),
               saddle_uplift_max_kN=sd_up/1e3, T_up=T_up, T_y=T_y, V_x=V_x, V_up=V_up)
json.dump(dict(summary=summary, rows=rows, checks=checks), open('/workspace/train/calcs/L4/l107_grillage_S17_out.json', 'w'), indent=1, default=float)
if __name__ == "__main__":
    print(json.dumps(summary, indent=1, default=float))
    for c in checks: print(f'{c["id"]:38s} {c["demand"]:>10} / {c["capacity"]:>9} {c["unit"]:4s} {c["util"]:5} {c["result"]}  {c["desc"][:70]}')
    hdr = ["station", "side", "type"] + vcols + ["Fz_down_max", "Fz_up_max", "Fx_3gP", "Fy_1gP"]
    print(" ".join(f"{h[:6]:>6}" for h in hdr))
    for r in rows: print(" ".join(f"{str(r[h])[:6]:>6}" for h in hdr))
# ---- Grokky S17: bearer moments at the saddle-hole lines (B1, B4) and net section
import json as _j
S = G.SEC["HSS5x3x3/16"]; t = S["tw"]; b = 76.2; d = 127.0
def bearer_M(u, x, y0, y1):
    a, bb = nid(x, y0), nid(x, y1); L = y1 - y0
    kb, kt = kel(L, G.E_STEEL*S["I"], G.G_STEEL*S["J"]); f = kb @ u[[3*a, 3*a+2, 3*bb, 3*bb+2]]
    return f[1], -f[3]
res = {}
for mk, x, ys in (("B1", 480.0, (300.0, 600.0)), ("B4", 4075.0, (250.0, 480.0))):
    for y in ys:
        best = (0, "")
        for name, (u, R) in list(results.items()):
            i = BYS.index(round(y, 1)); lo, hi = BYS[i-1], BYS[i+1]
            for yy in (y, -y):
                j = BYS.index(round(yy, 1))
                Mr = bearer_M(u, x, BYS[j-1], BYS[j])[1]; Ml = bearer_M(u, x, BYS[j], BYS[j+1])[0]
                M = max(abs(Mr), abs(Ml))
                if M > best[0]: best = (M, name)
        res[f"{mk} Y±{y:.0f}"] = dict(M_Nmm=round(best[0]), case=best[1])
_j.dump(res, open('/workspace/train/calcs/L4/l107_hole_moments_S17.json', 'w'), indent=1); print(res)

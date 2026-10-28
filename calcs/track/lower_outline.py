"""K-401 lower outline check (Steering 14b): min 150 mm above top of rail (ATOR) between the rails,
100 mm ATOR outside the rails. Basis: level track and vertical curves R >= 500 m (crest + sag), new wheels,
static (tare/laden spring travel and wheel wear listed separately - PE item)."""
import sys, json
sys.path.insert(0, "/workspace/train/build")
import model
HG = 457.2; RH = 32.0            # half gauge; ~rail head half width (ASCE 40) -> outside zone starts at 489
RV = 500000.0                     # vertical curve radius mm
LIM_IN, LIM_OUT = 150.0, 100.0
VEH = {"locomotive": dict(piv=(4075.0, 7275.0)), "tender": dict(piv=(1200.0, 3800.0)), "coach": dict(piv=(2337.0, 7823.0))}
SKIP = ("wheel",)                 # wheels/flanges run on the rail

def bbox(p):
    if p["t"] == "B":
        return p["x0"], p["x1"], p["y0"], p["y1"], p["z0"], p["z1"]
    r, a0, a1, c1, c2 = p["r"], p["a0"], p["a1"], p["c1"], p["c2"]
    if p["axis"] == "y": return c1 - r, c1 + r, a0, a1, c2 - r, c2 + r
    if p["axis"] == "z": return c1 - r, c1 + r, c2 - r, c2 + r, a0, a1
    return a0, a1, c1 - r, c1 + r, c2 - r, c2 + r

def vc(x0, x1, piv):
    """worst loss of clearance (mm) on a 500 m crest or sag for a body-mounted point at x0..x1"""
    a, b = piv; L = b - a; worst = 0.0
    for x in (x0, x1, min(max((a + b) / 2, x0), x1)):
        if a <= x <= b:  worst = max(worst, (x - a) * (b - x) / (2 * RV))      # crest, between pivots
        else:
            d = a - x if x < a else x - b; worst = max(worst, d * (L + d) / (2 * RV))  # sag, overhang
    return worst

out = {"basis": "K-401 lower outline: >= 150 mm ATOR between the rails (|Y| < 489), >= 100 mm ATOR outside (|Y| >= 489); level track and vertical curves R >= 500 m; new wheels; static. Wheels/flanges excluded. Truck-mounted parts use the truck as the vehicle (VC effect < 0.2 mm).", "vehicles": {}}
for fn, V in VEH.items():
    P = getattr(model, fn)()
    if fn == "tender":
        pass
    rows = []
    for p in P:
        if p["grp"] in SKIP: continue
        x0, x1, y0, y1, z0, z1 = bbox(p)
        if z0 > 400: continue
        inside = y0 < HG + RH and y1 > -(HG + RH)
        lim = LIM_IN if inside else LIM_OUT
        body = p["grp"] not in ("truck", "drive", "axle", "motor", "rods")
        d = vc(x0, x1, V["piv"]) if body else 0.0
        cl = z0 - d
        rows.append(dict(name=p["name"][:90], grp=p["grp"], x=[round(x0), round(x1)], y=[round(y0), round(y1)], z0=round(z0, 1),
                         vc_loss=round(d, 1), clear=round(cl, 1), zone="between" if inside else "outside", limit=lim, util=round(lim / cl, 2) if cl > 0 else 99))
    rows.sort(key=lambda r: -r["util"])
    out["vehicles"][fn] = dict(n_checked=len(rows), worst=rows[:8], ok=all(r["util"] <= 1.0 for r in rows))
json.dump(out, open("/workspace/train/calcs/track/lower_outline.json", "w"), indent=1, ensure_ascii=False)
for fn, v in out["vehicles"].items():
    print(fn, "OK" if v["ok"] else "NG", v["n_checked"])
    for r in v["worst"][:6]: print("   ", r["util"], r["clear"], r["zone"], r["grp"], r["x"], r["y"], r["name"][:60])

"""Rev L4 drawbar swing check (Source Bot rev 3 A-001 query; DB-800 loco-tender KEPT as drawn): loco-tender vs train drawbars at R100/R60/R50.
Exact 2-D geometry: truck centres on the track circle, pins on the vehicle axis, drawbar = chord between pins.
Outputs drawbar angle to each vehicle axis, lateral drawbar component at 70 kN, and inside/outside end-corner clearances."""
import math, json, sys
sys.path.insert(0, "/workspace/train/build")
from model import LOCO, TENDER, COACH
# vehicle: truck centres (x along body from front pin datum), front/rear pin x, body end x (front, rear), half width at the ends
VEH = {
 "loco":   dict(piv=LOCO["piv"], pin_f=None, pin_r=LOCO["len_pin"], end_f=0.0, end_r=11300.0, hw_r=LOCO["half_w"]),
 "tender": dict(piv=TENDER["piv"], pin_f=TENDER["front_pin"], pin_r=TENDER["rear_pin"], end_f=TENDER["body_x"][0], end_r=TENDER["body_x"][1], hw_f=TENDER["half_w"], hw_r=TENDER["half_w"]),
 "coach":  dict(piv=COACH["bolsters"], pin_f=COACH["pin"][0], pin_r=COACH["pin"][1], end_f=0.0, end_r=COACH["uf_len"], hw_f=COACH["half_w"], hw_r=COACH["half_w"]),
}
def place(v, R, s0):
    """vehicle with front truck at arc length s0 (running forward = -s); returns world mapping fn(x,y)."""
    a, b = v["piv"]; s1 = s0 + (b - a)
    p0 = (R * math.sin(s0 / R), R - R * math.cos(s0 / R)); p1 = (R * math.sin(s1 / R), R - R * math.cos(s1 / R))
    ux, uy = (p1[0] - p0[0]) / (b - a), (p1[1] - p0[1]) / (b - a)
    nx, ny = -uy, ux                      # +y towards curve centre
    return lambda x, y=0.0: (p0[0] + (x - a) * ux + y * nx, p0[1] + (x - a) * uy + y * ny), (ux, uy)
def joint(va, vb, L, R):
    fa, ua = place(va, R, 0.0)
    pa = fa(va["pin_r"])
    s_pa = va["pin_r"] - va["piv"][0]; lo = s_pa + (vb["piv"][0] - vb["pin_f"]); hi = lo + 2 * L   # bisection (monotonic window) so |pin_b - pin_a| = L
    for _ in range(200):
        m = (lo + hi) / 2; fb, ub = place(vb, R, m); pb = fb(vb["pin_f"])
        d = math.dist(pa, pb)
        if d < L: lo = m
        else: hi = m
    fb, ub = place(vb, R, m); pb = fb(vb["pin_f"])
    dx, dy = (pb[0] - pa[0]) / L, (pb[1] - pa[1]) / L
    ang = lambda u: math.degrees(math.asin(max(-1, min(1, u[0] * dy - u[1] * dx))))
    th_a, th_b = ang(ua), ang(ub)
    # end corners: inside (+y, towards centre) and outside (-y)
    out = {}
    for side, sg in (("inside", 1), ("outside", -1)):
        ca = fa(va["end_r"], sg * va["hw_r"]); cb = fb(vb["end_f"], sg * vb["hw_f"])
        out[side] = round(math.dist(ca, cb))
    straight = round(L + (va["end_r"] - va["pin_r"]) * -1 + (vb["end_f"] - vb["pin_f"]))
    return dict(angle_a_deg=round(th_a, 2), angle_b_deg=round(th_b, 2), lateral_70kN_kN=round(70 * math.sin(math.radians(max(abs(th_a), abs(th_b)))), 1),
                corner_inside_mm=out["inside"], corner_outside_mm=out["outside"], gap_straight_mm=straight)
res = {}
for lab, a, b in (("loco-tender", "loco", "tender"), ("tender-coach", "tender", "coach"), ("coach-coach", "coach", "coach")):
    for L in (800.0, 1473.0):
        for R in (100.0e3, 60.0e3, 50.0e3):
            res[f"{lab} L{L:.0f} R{R/1e3:.0f}"] = joint(VEH[a], VEH[b], L, R)
for k, v in res.items(): print(k, v)
# service pull at the loco-tender joint = trailing share of the adhesion cap (~0.25 x 160 kN x 61.1/78.8 ~ 31 kN)
P_LT = 31.0
lt8, lt14 = res["loco-tender L800 R50"], res["loco-tender L1473 R50"]
POCKET = dict(loco_rear_deg=32.4, tender_deg=19.2, coach_deg=32.4)   # run_all.POCKET: 150 / 300 / 150 mm mouths
lt60 = res["loco-tender L800 R60"]; lt50 = res["loco-tender L800 R50"]
dec = dict(
  loco_tender_mm=800, tender_coach_mm=1473, coach_coach_mm=1473, status="AS DRAWN - KEPT (Loco Bot confirmed A-001/L-104, parent steering 28 Oct)",
  swing_R60_DB800={"loco_deg": lt60["angle_a_deg"], "loco_limit_deg": POCKET["loco_rear_deg"], "loco_util": round(abs(lt60["angle_a_deg"]) / POCKET["loco_rear_deg"], 2),
                   "tender_deg": lt60["angle_b_deg"], "tender_limit_deg": POCKET["tender_deg"], "tender_util": round(abs(lt60["angle_b_deg"]) / POCKET["tender_deg"], 2),
                   "end_corner_inside_mm": lt60["corner_inside_mm"]},
  swing_R50_DB800={"loco_deg": lt50["angle_a_deg"], "tender_deg": lt50["angle_b_deg"], "tender_util": round(abs(lt50["angle_b_deg"]) / POCKET["tender_deg"], 2)},
  tender_lateral_R60_kN_at_31kN_pull={"DB-800": round(P_LT * math.sin(math.radians(abs(lt60["angle_b_deg"]))), 1), "DB-1473_info": round(P_LT * math.sin(math.radians(abs(res["loco-tender L1473 R60"]["angle_b_deg"]))), 1)},
  note=("Steady exact-geometry swing at R60 with DB-800: 19.3 deg at the loco pocket (limit 32.4, 150 mouth) and 11.0 deg at the tender pocket "
        "(limit 19.2, 300 mouth). Both PASS. Information only: a 1,473 bar at loco-tender would cut the tender-side angle to 4.3 deg. It is not "
        "adopted because the as-drawn 800 passes and Loco Bot confirmed it. Transient (spiral) angles come from the route sweep calcs/track/L4."),
  joints=5, pins="2 per joint x 5 = 10 + 2 spares = 12 (Ø60 4140 Q&T, L 150 under head: grip 108 + cross-bolt; drawn 250 corrected)",
  safety_chain="2 x 5/8 in Grade 100 (WLL 100.5 kN, ASTM A973) per joint, with Crosby G-2130 1 in bolt-type shackles (WLL 8.5 t = 83.4 kN); replaces 1/2 in (66.7 kN < 70 kN service)")
json.dump(dict(rev="L4 28 Oct 2026", cases=res, decision=dec), open("/workspace/train/calcs/L4/drawbar_L4.json", "w"), indent=1)

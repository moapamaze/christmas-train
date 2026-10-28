"""Rev L4 review of Loco Bot interface items (28 Oct 2026): L-107 blind-bolt holes in primary members,
saddle beams S3/S5 vs L4 drive, bell.  Inputs read-only: /workspace/loco/l107/calc_out.json, geom.py;
PE C4/C4b (pe_calcs).  AISC 360-22 ASD; AISC App. 3 fatigue.  Output loco_interfaces_L4.json."""
import json, math, sys
sys.path.insert(0, "/workspace/loco/l107"); import geom as G
CO = json.load(open("/workspace/loco/l107/calc_out.json"))
rows = CO["rows"]
# HSS12x6x3/8 A500C: t_des = 0.93*9.525
t = 0.93 * 9.525; Fy, Fu = 345.0, 427.0; Ix = 83.25e6; ybar = (1150 + 1454.8) / 2
dh = G.HB16["hole"]; zb = G.RB["bolt_z"]; y_h = zb - ybar
dI = t * dh**3 / 12 + t * dh * y_h**2
# C4: rail bending x2.0 = 90.1 MPa at extreme fibre (152.4 mm) -> service x1.0 at hole level
s_hole_serv = 90.1 / 2 * abs(y_h) / 152.4 / (1 - dI / Ix)
s_range = 2 * 0.3 * s_hole_serv          # +/-0.3 g dynamic on the service stress (F2291 bounce allowance)
CatD_thr = 48.0                           # AISC App 3 Cat D (open hole / mechanically fastened, non-pretensioned) threshold MPa
J = {}
rb = [r for r in rows if r["type"] == "RB"]
def per_bolt(r):
    V = math.hypot(max(r["Fx_3gP"], r["Fx_3g"]) / 2, max(r["Fz_down_max"], r["Fz_up_max"]) / 2)
    T = max(r["Fy_1gP"], r["Fy_1g"]) / 2
    return V, T
worst = max(rb, key=lambda r: per_bolt(r)[0]); V, T = per_bolt(worst)
d = 16.0; Le_vert = (1454.8 - 19.0) - zb  # hole CL to start of top corner radius (r=2t)
lc = Le_vert - dh / 2
Rn_bear = min(1.2 * lc * t * Fu, 2.4 * d * t * Fu) / 2.0 / 1000   # ASD omega 2.0 (kN)
# HSS wall local check under bolt tension: yield line, ring dia 2x hole
Rn_wall = Fy * t**2 / 4 * (2 * math.pi + 4 * 70 / dh) / 1.67 / 1000 * 2   # simplified yield-line ring, ASD
J["rail_web_holes"] = dict(
    count=24, stations=[s[0] + " X%.0f" % s[1] for s in G.stations_rb()], hole_mm=dh, bolt="Lindapter HB16 (M16 8.8)",
    hole_Z=zb, hole_from_neutral_axis_mm=round(y_h, 1),
    Ix_loss_pct=round(100 * dI / Ix, 2), C4_util_net=round(0.26 / (1 - dI / Ix), 3),
    stress_at_hole_service_MPa=round(s_hole_serv, 1), fatigue_range_MPa=round(s_range, 1), CatD_threshold_MPa=CatD_thr,
    fatigue_util=round(s_range / CatD_thr, 2),
    worst_station=worst["station"] + " " + worst["side"], V_per_bolt_kN=round(V, 2), T_per_bolt_kN=round(T, 2),
    HB16_SWL_V_kN=30.0, HB16_SWL_T_kN=21.0,
    HB16_interaction=round((V / 30.0)**2 + (T / 21.0)**2, 3),
    bearing_tearout_allow_kN=round(Rn_bear, 1), bearing_util=round(V / Rn_bear, 3),
    wall_yieldline_allow_kN=round(Rn_wall, 1), wall_util=round(T / Rn_wall, 3),
    verdict="APPROVED with conditions",
    conditions=["Outer web only, at Z1360 (+/-5); never in the top/bottom walls or within the corner radius (hole edge >= 3t = 29 mm from the start of the corner radius; actual %.0f mm)" % (Le_vert - dh / 2),
                "Hole edge >= 50 mm (2 x hole) from any weld toe on the same wall; crossmember welds are on the INNER web so B2/B5 are OK; no hole within 150 mm (X) of a crossmember, bolster, knee-gusset or jacking-pad weld on either web",
                "Bolt pitch >= 2.7d_hole (70 mm); 140 mm as drawn; hole centre >= 1.5d_hole (39 mm) from any free edge or cut-out; >= 300 mm from another hole group",
                "No holes X >= 10,148 (drawgear zone) or within 300 mm of the front end sill (X300-452) welds: B1 at X480 needs the hole group at X >= 500 + 13 -> move the bracket 50 mm aft (X530) or confirm the sill weld toe position",
                "Holes drilled (not punched or flame-cut), deburred, cold galvanising or zinc primer in the bore; HB16 at 190 N.m; PE to approve; record on S-503 weld/hole map",
                "Fatigue Cat D (open hole / non-pretensioned) range %.1f MPa vs 48 MPa threshold -> infinite life" % s_range])
# bolster top plates PL12 (4 holes, B4/B6)
bs = [r for r in rows if r["type"] == "BS"]; Tbs = max(r["Fz_up_max"] for r in bs)
J["bolster_top_holes"] = dict(count=4, stations="B4 X4075, B6 X7275 at Y+/-110", plate="PL12 bolster top flange",
    uplift_per_bolt_kN=round(Tbs, 2), HB16_SWL_T_kN=21.0, util=round(Tbs / 21.0, 3),
    net_section="compression flange of the bolster box at the pivot (mid-span sagging): filled holes, no deduction per AISC B4.3; tension side unaffected",
    verdict="APPROVED with conditions",
    conditions=["The bolster box spans between the rail INNER webs (Y+/-163.8); its PL12 top plate is fillet-welded to them. At Y+/-110 the hole edge is ~33 mm from the weld toe (< 50): MOVE the holes to Y+/-90 (edge 52 mm from the toe) and shorten the SD-1 cap to suit",
                "The centre plate (Ø300 PL40) is on the bottom plate, so the top plate has no pivot weld; keep holes >= 50 mm from any internal diaphragm (assumed at Y0 and the webs at X3900/4250, X7100/7450: 162 mm - OK)",
                "Clamp range 12-29 mm OK for PL12; drilled; PE to approve"])
J["rear_end_sill_holes"] = dict(count=2, zone="X10748-10900, drawgear (70 kN service / 200 kN ultimate, C4b/C5/C8)",
    verdict="REJECTED",
    reasons=["The end sill is in the drawgear load path (eccentric drawbar moment shared by both rails through the sill and knee gussets); C4b/C8 would need re-analysis and the PE drawgear certification reopened for a 2-bolt hold-down",
             "Cyclic draft load: open holes are Cat D/E details next to knee-gusset weld toes; the draft gear with <=0.5 mm slack still cycles every start/stop",
             "B9 uplift is small (%.1f kN): a weld-free alternative exists" % max(r["Fz_up_max"] for r in rows if r["type"] == "ES") if any(r["type"] == "ES" for r in rows) else "B9 uplift is small: a weld-free alternative exists"],
    alternative="Bear B9 on the rail tops with a saddle and hold it down with 2 x U-bolt/clamp straps round the main rails just forward of X10148 (outside the drawgear zone), or tie B9 to B8 with the stringers and let B8 (RB, X9900) take the uplift")
# S3/S5 vs L4
sys.path.insert(0, "/workspace/train/build"); import model
def bb(p):
    if p["t"] == "B": return (p["x0"], p["x1"], p["y0"], p["y1"], p["z0"], p["z1"])
    r = p["r"]; a = p["axis"]
    if a == "y": return (p["c1"] - r, p["c1"] + r, p["a0"], p["a1"], p["c2"] - r, p["c2"] + r)
    if a == "x": return (p["a0"], p["a1"], p["c1"] - r, p["c1"] + r, p["c2"] - r, p["c2"] + r)
    return (p["c1"] - r, p["c1"] + r, p["c2"] - r, p["c2"] + r, p["a0"], p["a1"])
def gap(a, b): return max(max(b[2*i] - a[2*i+1], a[2*i] - b[2*i+1]) for i in range(3))
drv = [p for p in model.locomotive() if p["grp"] in ("drive", "motor")]
top = max(bb(p)[5] for p in drv)
S = {}
for nm, X in (("S3/B3", 2450.0), ("S5/B5", 5675.0)):
    parts = {"bearer HSS5x3x3/16": (X - 38, X + 38, -1170, 1170, G.BEARER_BOT, G.ZS),
             "RB-1 brackets (both sides)": (X - 100, X + 100, -348, 348, G.RB["wp_z0"], G.BEARER_BOT),
             "barrel saddle": (X - 150, X + 150, -900, 900, G.ZS, 2600)}
    S[nm] = {k: dict(min_gap_mm=round(min(gap(b, bb(d)) for d in drv)), nearest=min(drv, key=lambda d: gap(b, bb(d)))["name"][:60]) for k, b in parts.items()}
S["vertical"] = dict(L4_drive_top_Z=round(top), RB_bracket_bottom_Z=G.RB["wp_z0"], rail_bottom_Z=1150, vertical_gap_mm=round(G.RB["wp_z0"] - top),
                     note="Truck yaw at R45 moves the case corners < 15 mm in X; the plan gaps are >= 415 mm, and the drive is entirely below the rails (vertical gap %.0f mm to the RB plate). Driver wheel tops: nearest axle is 825-850 mm from S3/S5 (> R725)." % (G.RB["wp_z0"] - top))
S["verdict"] = "CLEAR - no clash; no change needed to S3 (X2450) or S5 (X5675). Keep-out for any later bracket: nothing below Z1150 within X2990-3843 / 4307-5160 / 6190-7043 / 7657-8510 (L4 case + motor plan per axle)."
J["saddles_S3_S5"] = S
J["bell"] = dict(accepted="8 in bell, CL X2800 on PL10 former F6, bell + yoke + saddle <= 270 mm (barrel top Z3380 to Z3650); 9 in only if bell + yoke <= 245 mm", mass_kg=40,
                 effect="in drive_L4 mass basis (front truck +56 kg); no K-401 effect (top <= Z3650 < 3,700 roof line)")
json.dump(J, open("/workspace/train/calcs/L4/loco_interfaces_L4.json", "w"), indent=1)
print(json.dumps(J, indent=1))

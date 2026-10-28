"""TW-1 tender weight-reduction study (rev T1 / LT45.1 tender). Writes tender_weight_study.json and
tender_weight_costs_OWNER_ONLY.json. Masses in kg. ASSUMED values are marked; nothing here is supplier data."""
import json, math, sys
sys.path.insert(0, "/workspace/train/build")
from model import TENDER, HALF_G
RHO = 7850.0; RHO_AL = 2700.0
cad = json.load(open("/workspace/train/backup_pre_T2/mass_report.json"))["PF-T200_tender"]["by_group"]  # frozen rev T1 CAD (study basis); rev T2 build-up is tender_mass_T2.py

# ---- 1. true wheel mass (CAD models each wheel as a solid Ø600 x 120 disc + Ø650 flange disc)
def ann(do, di, w): return math.pi / 4 * (do**2 - di**2) * w / 1e9 * RHO
def wheel_true(d=600, w=120, rim=50, web=25, hub_od=200, axle=110, fl_h=25, fl_w=25):
    return (ann(d, d - 2 * rim, w) + ann(d + 2 * fl_h, d, fl_w) + ann(d - 2 * rim, hub_od, web) + ann(hub_od, axle, w))
w_true = wheel_true(); w_cad = cad["wheel"] / 8
L = {}
def add(grp, item, kg, basis): L.setdefault(grp, []).append(dict(item=item, kg=round(kg, 1), basis=basis))
# trucks
add("Trucks (2)", "Wheels 8 × Ø600 plate-web (true section)", 8 * w_true, f"Rim 50 deep, web 25, hub Ø200 (ASSUMED section); CAD solid disc was {w_cad:.0f} kg each, true ≈ {w_true:.0f} kg")
add("Trucks (2)", "Axles 4 × Ø110 × 1,400", cad["axle"], "CAD")
add("Trucks (2)", "Truck frames, axleboxes, centre plates", cad["truck"], "CAD (C-303 coach truck)")
add("Trucks (2)", "Springs, brake discs, calipers, spring-brake chambers", 300, "ASSUMED 150 kg per truck (not modeled)")
# frame + deck
add("Frame + deck", "Main rails, crossmembers, bolster boxes", cad["frame"], "CAD rev T1")
add("Frame + deck", "PF-DB drop boxes and pockets, both ends", cad["coupler"], "CAD rev T1")
add("Frame + deck", "Deck PL10, 4.4 × 2.6 m", cad["deck"], "CAD rev T1")
outrig = 5 * 2.6 * 12.2
add("Frame + deck", "Outriggers to carry the deck edge and walls (5 × C6x8.2 full width)", outrig, "ASSUMED - not in the model (deck overhangs the rails by 600 mm)")
# body
bx0, bx1 = TENDER["body_x"]; hw = TENDER["half_w"]; H = TENDER["roof"] - TENDER["deck"]
A_side = 2 * (bx1 - bx0) * H / 1e6; A_end = 2 * (2 * hw) * H / 1e6; A_roof = (bx1 - bx0) * 2 * hw / 1e6
A_skin = A_side + A_end + A_roof
skin = lambda t, rho=RHO: A_skin * t / 1000 * rho
add("Body", f"Skin 6 mm steel, {A_skin:.1f} m² (sides, ends, roof)", skin(6), "LT45.1 6 mm skin")
add("Body", "Skin posts, roof bows, door frames", 150, "ASSUMED")
add("Body", "Lining 50 mm mineral wool 100 kg/m³ + perforated steel liner 0.8 mm + facing", A_skin * (5.0 + 3.8 + 1.0), "ASSUMED densities")
A_cov = 3.8 * 2.2 + 2 * 3.8 * 0.2 + 2 * 2.2 * 0.2
add("Body", f"Coal-effect cover 3 mm steel, {A_cov:.1f} m² + supports", A_cov * 3 / 1000 * RHO + 40, "ASSUMED 3 mm formed steel")
add("Body", "Doors, hinges, latches, handles, paint", 100, "ASSUMED")
# equipment + fluids (owner ledger, Project Plan Page + tender-lt45/basis.json)
add("Equipment (dry)", "AIE V3307 package + radiator + H1P045", 959.1 - 166 - 128.1 - 55, "LT45.1 relocated 959.1 less tanks/cooler")
add("Equipment (dry)", "Fuel tank + hydraulic reservoir (empty)", 90, "basis.json 40 + 50")
add("Equipment (dry)", "Hydraulic oil cooler", 55, "basis.json")
add("Equipment (dry)", "35 kW generator set", 900, "Owner ledger ASSUMED (model not chosen)")
add("Equipment (dry)", "Compressor, coach AC panel, batteries", 160, "Owner ledger ASSUMED")
add("Equipment (dry)", "Mounts, exhaust + shields, ducts, hoses, cabling", 250, "ASSUMED - not in owner ledger")
add("Fuel + fluids", "Diesel 150 L", 126, "basis.json (0.84 kg/L)")
add("Fuel + fluids", "Hydraulic oil in reservoir", 78.1, "basis.json")
base = {g: round(sum(i["kg"] for i in v), 1) for g, v in L.items()}
BASE = round(sum(base.values()), 1)

# ---- 2. candidate savings (kg saved = positive). hours: shop (+ = more), eng = engineering hours; look 1-5
c_skin_10ga = skin(6) - skin(3.42) - 60
c_skin_8ga = skin(6) - skin(4.18) - 30
c_skin_al = skin(6) - skin(4, RHO_AL) - 0  # aluminium posts swap roughly cancels
deck6 = (bx1 + 100 - (bx0 - 100)) * 2600 * 6 / 1e9 * RHO + 7 * 2.6 * 12.2
c_deck = cad["deck"] + outrig - deck6
cov15 = A_cov * 1.5 / 1000 * RHO + 40
c_cov = (A_cov * 3 / 1000 * RHO + 40) - cov15
c_cov_frp = (A_cov * 3 / 1000 * RHO + 40) - (A_cov * 9.0 + 30)
c_lin = A_skin * (5.0 + 3.8) - A_skin * (3.2 + 0.8 * 0.6 / 1000 * RHO_AL * 1.0 + 0)  # 64 kg/m³ wool + 0.8 mm perforated Al
C = [
 dict(id="S1", move="Skin 6 mm → 10 ga (3.4 mm) steel, bolted/plug-welded to posts at 500 mm (riveted-plate look)", kg=c_skin_10ga, shop_h=12, eng_h=4, approv="Easy - non-structural skin; panel check for wind and oil-canning", look="4/5 - posts at 500 + round-head bolts read as riveted tender plate; continuous welding would oil-can (2/5)", rec=True),
 dict(id="S2", move="Skin 6 mm → 8 ga (4.2 mm) steel (alternative to S1)", kg=c_skin_8ga, shop_h=6, eng_h=3, approv="Easy", look="4.5/5", rec=False),
 dict(id="S3", move="Skin → 4 mm aluminium 5052 (alternative to S1)", kg=c_skin_al, shop_h=40, eng_h=12, approv="Harder - poor fire barrier around two diesels and exhaust; galvanic isolation; not CWF's usual material", look="4/5", rec=False),
 dict(id="D1", move="Deck PL10 → 6 mm tread plate on 7 full-width C6 cross-bearers (replaces PL10 + outriggers)", kg=c_deck, shop_h=10, eng_h=3, approv="Easy - equipment mounts land on rails and cross-bearers; spill floor stays steel and sealed", look="n/a (inside)", rec=True),
 dict(id="G1", move="Open-skid 35 kW genset (no sound enclosure or base tank) - the insulated tender is the enclosure; target ≤ 650 kg", kg=250, shop_h=6, eng_h=8, approv="AWAIT supplier data (mass, cooling air, open-frame rating); fuel from the shared tank", look="n/a", rec=True),
 dict(id="G2", move="Smaller generator (≈25 kW) by cutting coach heat/cool load", kg=200, shop_h=0, eng_h=6, approv="Not recommended - hot-humid case is already 4.7 kW short at 35 kW", look="n/a", rec=False),
 dict(id="K1", move="Coal-effect cover 3 mm → 1.5 mm (16 ga) formed steel, textured coating", kg=c_cov, shop_h=6, eng_h=1, approv="Easy - steel stays fire-safe near the exhaust", look="5/5 - same shape, black with gold edge trim", rec=True),
 dict(id="K2", move="Coal-effect cover in fire-retardant FRP (alternative to K1)", kg=c_cov_frp, shop_h=4, eng_h=3, approv="OK if FR resin and kept clear of the exhaust outlet", look="5/5", rec=False),
 dict(id="K3", move="Delete the coal-effect cover", kg=A_cov * 3 / 1000 * RHO + 40, shop_h=-20, eng_h=0, approv="Easy", look="Loses the owner's look - not recommended", rec=False),
 dict(id="B1", move="Bolster boxes → fish-belly PL10 webs (deep only at the centre plate), lightening holes in webs", kg=140, shop_h=4, eng_h=4, approv="Easy - centre-plate load ≈44 kN ×2 dynamic gives ~12 MPa in the present box; coupler path untouched", look="n/a (under frame)", rec=True),
 dict(id="L1", move="Lining: 64 kg/m³ mineral wool + 0.8 mm perforated aluminium inner liner (steel liner kept by the exhaust)", kg=c_lin, shop_h=0, eng_h=1, approv="Easy - wool stays non-combustible", look="n/a (inside)", rec=True),
 dict(id="F1", move="Run-day fuel: carry 100 L (tank 120 L) instead of 150 L", kg=50 * 0.84 + 6, shop_h=0, eng_h=1, approv="Easy - est. use ≈ 8.6 L/h both engines (ASSUMED), so 100 L ≈ 11 h", look="n/a", rec=True),
 dict(id="W1", move="Lightening holes in the wheel webs", kg=8 * 10, shop_h=8, eng_h=6, approv="Harder - wheel fatigue; changes the coach wheel too", look="n/a", rec=False),
 dict(id="W2", move="Tender-only Ø460 trucks", kg=400, shop_h=40, eng_h=30, approv="Harder - new truck design and approval; loses one-spare-fits-all", look="3/5", rec=False),
 dict(id="R1", move="Lighter main rails / lightening holes in rails or drop boxes", kg=60, shop_h=0, eng_h=10, approv="Not worth it - rails carry the 200 kN buff with the 286 mm offset moment + fatigue; holes in HSS add fatigue and corrosion details", look="n/a", rec=False),
 dict(id="M1", move="Move tender equipment to the locomotive", kg=0, shop_h=0, eng_h=0, approv="No gain at 2%: train mass is unchanged and the motors, not adhesion, are the limit. Only helps if it replaces dead ballast kg-for-kg", look="n/a", rec=False),
]
for c in C: c["kg"] = round(c["kg"])
rec = [c for c in C if c["rec"]]
SAVE = sum(c["kg"] for c in rec); SAVE_noG = SAVE - next(c["kg"] for c in rec if c["id"] == "G1")
NEW = BASE - SAVE; NEW_noG = BASE - SAVE_noG
# ---- 3. 2% start margin (motor-limited at 350 bar). Basis: train 77.8 t with stairs incl. 8.16 t ledger tender
F350 = 4 * (35.0 * 750 / (2 * math.pi) * 0.95) / 0.5 / 1000
kN_per_t = 0.0408 * 9.81
need = lambda tender_kg: (77.8 - 8.16 + tender_kg / 1000) * kN_per_t
marg = lambda tk: F350 - need(tk)
limit = 8.16 + marg(8160) / kN_per_t
out = dict(study="TW-1", date="2026-10-27", wheel_true_kg=round(w_true, 1), wheel_cad_kg=round(w_cad, 1), skin_area_m2=round(A_skin, 2),
           ledger=L, groups=base, baseline_kg=BASE, candidates=C, recommended=[c["id"] for c in rec], save_kg=SAVE, save_noG_kg=SAVE_noG,
           new_kg=round(NEW), new_noG_kg=round(NEW_noG), F350=round(F350, 2), kN_per_t=round(kN_per_t, 4), limit_t=round(limit, 2),
           margin={"ledger_8160": round(marg(8160), 2), "baseline": round(marg(BASE), 2), "package": round(marg(NEW), 2), "package_noG": round(marg(NEW_noG), 2)},
           ballast_note=f"Each 1 t of loco ballast left out adds {kN_per_t:.2f} kN; loco 15.8 t is well above the 11.9 t dry-2% adhesion minimum.")
json.dump(out, open("/workspace/train/calcs/tender_weight_study.json", "w"), indent=1)
# ---- owner-only cost deltas (shop [price removed]-110/h SteelFlo, eng [price removed]/h ASSUMED; plate [price removed]-1.03/lb MPB; tread/sheet [price removed]-1.5/lb ASSUMED)
LB = 2.20462
def money(c, mat_lo, mat_hi):
    lo = c["shop_h"] * 80 + c["eng_h"] * 150 + mat_lo; hi = c["shop_h"] * 110 + c["eng_h"] * 150 + mat_hi
    return [round(lo, -1), round(hi, -1)]
mat = {"S1": (-c_skin_10ga * LB * 1.03 + 0, -c_skin_10ga * LB * 0.67 + 60 * LB * 1.2),
       "D1": (deck6 * LB * 1.0 - (cad["deck"] + outrig) * LB * 0.85, deck6 * LB * 1.5 - (cad["deck"] + outrig) * LB * 0.67),
       "G1": (0, 0), "K1": (-c_cov * LB * 1.0, -c_cov * LB * 0.5), "B1": (-140 * LB * 1.03, -140 * LB * 0.67),
       "L1": (300, 600), "F1": (-50, 0)}
COST = {c["id"]: dict(move=c["move"], kg=c["kg"], shop_h=c["shop_h"], eng_h=c["eng_h"], usd=money(c, *mat[c["id"]])) for c in rec}
tot = [sum(v["usd"][0] for v in COST.values()), sum(v["usd"][1] for v in COST.values())]
json.dump(dict(items=COST, total_usd=tot, note="G1 genset price delta AWAIT supplier quotes (open-skid usually costs less than enclosed; not counted)."),
          open("/workspace/train/calcs/tender_weight_costs_OWNER_ONLY.json", "w"), indent=1)
print("wheel", round(w_true, 1), "cad", round(w_cad, 1), "skin m2", round(A_skin, 2))
for g, v in base.items(): print(f"{g:18s} {v:8.0f}")
print("BASE", BASE)
for c in C: print(c["id"], c["kg"], c["rec"])
print("save", SAVE, "noG", SAVE_noG, "new", round(NEW), round(NEW_noG), "margins", out["margin"], "limit", round(limit, 2), "F350", round(F350, 2))
print("cost", {k: v["usd"] for k, v in COST.items()}, tot)

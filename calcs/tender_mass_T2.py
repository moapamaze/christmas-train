"""Tender rev T2 mass build-up (owner-approved TW-1 subset S1 + D1 + K1 + B1, 27 Oct 2026).
Pulsipher Farms Christmas Train — preliminary, not for construction until PE stamped.
Steel from the rev T2 CAD (cad/mass_report.json, true wheel section) + modeled body / roof / cover volumes from build/model.py
+ allowances for what is not modeled (marked ASSUMED). Writes tender_mass_T2.json. No prices here."""
import json, math, sys
sys.path.insert(0, "/workspace/train/build")
from model import tender, TENDER
RHO = 7850.0
cad = json.load(open("/workspace/train/cad/mass_report.json"))["PF-T200_tender"]["by_group"]
study = json.load(open("/workspace/train/calcs/tender_weight_study.json"))
def vol(p):
    if p["t"] == "B":
        dx, dy, dz = p["x1"] - p["x0"], p["y1"] - p["y0"], p["z1"] - p["z0"]; v = dx * dy * dz
        if p.get("hss"):
            ax, t = p["hss"]; ix, iy, iz = dx - 2 * t, dy - 2 * t, dz - 2 * t
            if ax == "x": ix = dx
            if ax == "y": iy = dy
            if ax == "z": iz = dz
            v -= max(ix, 0) * max(iy, 0) * max(iz, 0)
        return v
    return math.pi * (p["r"] ** 2 - p.get("rin", 0) ** 2) * (p["a1"] - p["a0"])
kg = lambda ps: sum(vol(p) for p in ps) * RHO / 1e9
T = tender()
pick = lambda key: [p for p in T if key in p["name"]]
skin = kg(pick("skin")) + kg(pick("flat roof"))
posts = kg(pick(" post HSS2x2")) + kg(pick("roof bow"))
cover = kg([p for p in T if p["grp"] == "trim"])
A_skin = study["skin_area_m2"]
L = {}
def add(g, item, m, basis): L.setdefault(g, []).append(dict(item=item, kg=round(m, 1), basis=basis))
add("Trucks (2)", "Wheels 8 × Ø600 plate-web", cad["wheel"], "CAD rev T2 true section (rim 50, web 25, hub Ø200 - section ASSUMED)")
add("Trucks (2)", "Axles 4 × Ø110", cad["axle"], "CAD")
add("Trucks (2)", "Truck frames, axleboxes, centre plates", cad["truck"], "CAD (C-303)")
add("Trucks (2)", "Springs, brake discs, calipers, spring-brake chambers", 300, "ASSUMED 150 kg per truck (not modeled)")
add("Frame + deck", "Main rails, crossmembers, fish-belly bolsters (B1)", cad["frame"], "CAD rev T2 (bolster lightening holes not modeled - conservative)")
add("Frame + deck", "PF-DB drop boxes and pockets", cad["coupler"], "CAD")
add("Frame + deck", "Deck 6 mm tread plate + 7 C6x8.2 cross-bearers (D1)", cad["deck"], "CAD rev T2")
add("Frame + deck", "Tread-plate pattern, bearer clips, welds", 0.03 * cad["deck"] + 15, "ASSUMED")
add("Body", "Skin 10 ga (3.42 mm) sides, ends, roof (S1)", skin, "Model rev T2")
add("Body", "Posts + roof bows HSS2x2x1/8 at ≤500", posts, "Model rev T2")
add("Body", "Door frames, bolts / plug welds, post clips", 40, "ASSUMED")
add("Body", "Lining 50 mm mineral wool 100 kg/m³ + 0.8 mm perforated steel liner + facing (standard, kept)", A_skin * (5.0 + 3.8 + 1.0), "ASSUMED densities (as TW-1 baseline)")
add("Body", "Coal-effect cover 1.5 mm formed steel (K1)", cover, "Model rev T2 (height ASSUMED)")
add("Body", "Cover supports, coal texture coating, gold trim", 40, "ASSUMED")
add("Body", "Doors, hinges, latches, handles, paint", 100, "ASSUMED")
# REV L4 (Tender Bot, 28 Oct 2026): H1P053 pump; genset PTI-38 699 kg (OWNER DECISION vs DCA36 1,137 kg + 346 mm roof raise; both rated 40 °C not 43 °C, no UL 2200 shown);
# IR 2340 compressor + clutch, coach AC panel, batteries 190 kg (was 160); hydraulic oil +26 kg (4 × MS05 loop, cooler 14 kW, flow divider)
L4_EQ = {"AIE V3307 package + radiator + H1P045": ("AIE V3307 package + radiator + H1P053", None, "rev L4: H1P053 (same SAE B pad)"),
         "35 kW generator set": ("35 kW generator set - PTI-38 (OWNER DECISION; DCA36 1,137 kg alt.)", 699, "rev L4 Tender Bot: PTI-38 data sheet 699 kg"),
         "Compressor, coach AC panel, batteries": ("Compressor IR 2340 + electric clutch, coach AC panel, batteries", 190, "rev L4 Tender Bot")}
for i in study["ledger"]["Equipment (dry)"]:
    nm, kg, note = L4_EQ.get(i["item"], (i["item"], None, None))
    add("Equipment (dry)", nm, i["kg"] if kg is None else kg, note or (i["basis"] + " (unchanged)"))
for i in study["ledger"]["Fuel + fluids"]: add("Fuel + fluids", i["item"], i["kg"], i["basis"] + " (150 L kept)")
add("Fuel + fluids", "Hydraulic oil - L4 additional (4 × MS05 loops, 14 kW cooler, flow divider)", 26, "rev L4 Tender Bot")
groups = {g: round(sum(i["kg"] for i in v), 1) for g, v in L.items()}
TOT = round(sum(groups.values()))
F350, kpt = study["F350"], study["kN_per_t"]
marg = lambda t: F350 - (77.8 - 8.16 + t / 1000) * kpt
out = dict(rev="T2 (L4 update 2026-10-28)", date="2026-10-28", approved=["S1", "D1", "K1", "B1"], not_adopted=["G1", "F1", "L1"], ledger=L, groups=groups,
           total_kg=TOT, T1_baseline_kg=study["baseline_kg"], saving_kg=round(study["baseline_kg"] - TOT),
           study_estimate_kg=round(study["baseline_kg"] - sum(c["kg"] for c in study["candidates"] if c["id"] in ("S1", "D1", "K1", "B1"))),
           margin_kN=round(marg(TOT), 2), margin_T1_kN=round(marg(study["baseline_kg"]), 2), margin_ledger_kN=round(marg(8160), 2), limit_t=study["limit_t"],
           headroom_t=round(study["limit_t"] - TOT / 1000, 2), F350=F350, kN_per_t=kpt)
# REV L4.2 (Tender Bot TB-3.13d, 28 Oct 2026): the CURRENT tender is carried here; the T2 build-up above is the study basis.
TB = dict(rev="TB-3.13d", kg=8706.5, cg_mm=[2422.7, 11.3, 1110.4], delta_vs_TB311_kg=59.9, includes="tender-end safety-chain shackles",
          MR_pipe="3/4 in x ~5.3 m to the MR glad hand at Y-950/Z1950 (~1.50 L, in the loco MR volume)",
          history="T2 build-up %d -> TB-3.4 8,465.3 -> TB-3.8 8,568.8 -> TB-3.9 8,616.3 -> TB-3.11 8,646.6 -> TB-3.13b 8,700.1 -> TB-3.13c 8,705.2 -> TB-3.13d 8,706.5 (+7.9 kg if the A-1342N fallback coupler is used) (Tender Bot layout items: genset/ATS/cabinet, 150 L tank, 3 MR, shore transformer cradle, etc.)" % TOT)
out.update(current=TB, current_kg=TB["kg"], reconciliation_to_current_kg=round(TB["kg"] - TOT, 1), margin_current_kN=round(marg(TB["kg"]), 2), headroom_current_t=round(study["limit_t"] - TB["kg"] / 1000, 2))
json.dump(out, open("/workspace/train/calcs/tender_mass_T2.json", "w"), indent=1)
for g, v in groups.items(): print(f"{g:18s}{v:8.0f}")
print("TOTAL", TOT, "saving", out["saving_kg"], "study est", out["study_estimate_kg"], "margin", out["margin_kN"], "headroom t", out["headroom_t"])
print("skin", round(skin), "posts", round(posts), "cover", round(cover))

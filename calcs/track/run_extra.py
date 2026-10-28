"""Extra sweep cases added 28 Oct (steering): Alt D (R60) and R60 / R70-R60 reverse curves."""
import json, sys
import run_all as RA
import route_check as R
out = {}
for nm, spec in (("S_R60_T0.0", [("T", 100), ("C", 60, 90, "L"), ("T", 0.01), ("C", 60, 90, "R"), ("T", 60)]),
                 ("S_R70_T19.78_R60", [("T", 100), ("C", 70, 49.6, "R"), ("T", 19.78), ("C", 60, 120, "L"), ("T", 60)]),
                 ("S_R60_T36.26_R50", [("T", 100), ("C", 60, 15.2, "R"), ("T", 36.26), ("C", 50, 120, "L"), ("T", 60)]),
                 ("S_R105_T35.22_R50", [("T", 100), ("C", 105, 71.8, "R"), ("T", 35.22), ("C", 50, 120, "L"), ("T", 60)])):
    RA.run_syn(nm, spec); out[nm] = RA.CASES[nm]
A = R.load_alignment("D"); d = RA.case("Alt D", A, step=2000.); d["L_m"] = A["L"] / 1000
json.dump(dict(cases=out, alts={"D": d}), open("route_sweep_extra.json", "w"), indent=1, default=float)
print("done", flush=True)

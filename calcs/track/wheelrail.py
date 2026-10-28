"""Wheel/rail interface for the track engineer's structure (28 Oct 2026): gauge widening, wheel drop, restraining-rail
check gauge / flangeway, and the track-structure load basis.  Rev RT1 28 Oct 2026.
Wheel profile (PE §12, all vehicles incl. Ø1,450 drivers, Ø650 lead, Ø600 tender/coach): B2B 858 ±1, flange 22 at the
gauge point (10 below tread), flange height 25, 70°, root R12, tread (rim) width 120 measured from the back face.
ASSUMED (PE to confirm): flange-thickness condemning limit 17 (5 mm wear); rim chamfer 5; rail side-wear allowance 3;
dynamic gauge spread under lateral load 3 (cut-spiked, plated).  ASCE 40 head width 1-7/8 in = 47.6 mm."""
import json, math
IN = 25.4; G0 = 914.4
B2B = (857.0, 858.0, 859.0); T_NEW, T_WORN = 22.0, 17.0; TREAD = 120.0; CHAMF = 5.0; HEAD = 1.875 * IN
WEAR_RAIL = 3.0; SPREAD = 3.0
wheelset_gauge = dict(nom=B2B[1] + 2 * T_NEW, min_worn=B2B[0] + 2 * T_WORN, max_new=B2B[2] + 2 * T_NEW)
check_dim = dict(max_new=B2B[2] + T_NEW, min_worn=B2B[0] + T_WORN)     # back of one flange to the gauge point of the other
def tread_on_head(G):
    """worst case: worn, narrowest wheelset pressed against one rail; overlap of the far wheel's effective tread
    (gauge point → rim chamfer) with the railhead measured from the railhead gauge face"""
    play = G - wheelset_gauge["min_worn"]
    return TREAD - T_WORN - CHAMF - play, play
G_abs = wheelset_gauge["min_worn"] + (TREAD - T_WORN - CHAMF - HEAD)   # full head width still under the effective tread
cases = []
for lab, Gn, tol in (("tangent / R ≥ 75 (914.4)", G0, 6.0), ("R50-75 (36-1/8 in = 917.5)", 36.125 * IN, 6.0), ("R45-50 (36-1/4 in = 920.7)", 36.25 * IN, 6.0)):
    Gw = Gn + tol + WEAR_RAIL + SPREAD
    ov, play = tread_on_head(Gw)
    cases.append(dict(case=lab, G_nom=round(Gn, 1), G_built_max=round(Gn + tol, 1), G_worst=round(Gw, 1), play_worst=round(play, 1),
                      tread_overlap=round(ov, 1), head=round(HEAD, 1), full_head_bearing=ov >= HEAD, margin_to_abs=round(G_abs - Gw, 1),
                      play_new_nom=round(Gn - wheelset_gauge["nom"], 1)))
# restraining (guard) rail on curves < R60 - check gauge C measured from the HIGH-rail gauge face to the restraining-rail face
C_lower = check_dim["max_new"]                 # must exceed: restraining contact before the outer flange touches the high rail
C_nom, C_tol, C_wear = 886.0, 2.0, 3.0
flange_clear = 3.0                             # flangeway must pass a new 22 flange + root + 3
def fw(G, C): return G - C
rr = []
for lab, Gn in (("R50-60 widened 917.5", 36.125 * IN), ("R45-50 widened 920.7", 36.25 * IN), ("no widening 914.4", G0)):
    Fmin = fw(Gn - 3.0, C_nom + C_tol); Fmax = fw(Gn + 6.0, C_nom - C_wear)
    rr.append(dict(case=lab, G=round(Gn, 1), C_nom=C_nom, flangeway_nom=round(fw(Gn, C_nom), 1), flangeway_min=round(Fmin, 1), flangeway_max=round(Fmax, 1),
                   flange_need=T_NEW + flange_clear, ok_min=Fmin >= T_NEW + flange_clear,
                   outer_flange_gap_at_contact=dict(largest_wheelset=round(C_nom - C_wear - C_lower, 1), smallest_worn=round(C_nom + C_tol - check_dim["min_worn"], 1))))
pe892 = dict(as_written="check gauge 892 min", flangeway_if_track_check_gauge=round(G0 - 892, 1),
             reading="892 = min worn wheelset (flange-face) gauge 857 + 2×17.5 - a WHEEL dimension, not a track check gauge. As a track/restraining check gauge it would leave a 22.4 mm flangeway against a 22 mm flange (19.4 at gauge -3) - NG.")
# track structure (track engineer, 28 Oct): ASCE 40 new, ties 6x8x6 ft @ 22.5 in, plates, 9/16 cut spikes
TS = json.load(open("/workspace/track_structure/track_calc.json"))
boef = [b for b in TS["boef"] if b["rail"] == "ASCE 40"]
Qb = 26.0; Qdrv = 24.46
track = dict(Q_basis=Qb, Q_max_static=Qdrv, base_stress_MPa=max(b["base_MPa"] for b in boef), base_allow=172,
             ballast_psi=TS["tie"]["ballast_psi"], plate_psi=TS["tie"]["plate_psi"], tie_bending_psi=TS["tie"]["tie_sig_seat"],
             lateral_TE_kN=TS["loads"]["lateral_design_kN"], lateral_basis_kN=0.35 * 2 * Qb, rollover_limit=TS["lateral"]["rollover_LV_rail40"],
             LV_actual_R100_claimed=TS["lateral"]["LV_actual_R100"])
OUT = dict(rev="RT1 28 Oct 2026", wheel=dict(B2B=B2B, t_new=T_NEW, t_worn=T_WORN, tread=TREAD, chamfer=CHAMF, head=round(HEAD, 1)),
           wheelset_gauge=wheelset_gauge, check_dim=check_dim, G_abs_max=round(G_abs, 1), G_maint_limit=932.0, widening=cases,
           restraining=dict(C_lower_bound=C_lower, C_nom=C_nom, C_tol=f"+{C_tol}/-0", C_renew_below=C_nom - C_wear, rows=rr, pe892=pe892), track=track)
json.dump(OUT, open("/workspace/train/calcs/track/wheelrail.json", "w"), indent=1)
print(json.dumps(OUT, indent=1))

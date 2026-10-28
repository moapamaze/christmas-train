"""Rev L4.1 drive (28 Oct 2026; L4 + Source Bot rev 3.5/3.5.1 flags + Loco Bot HL-1/DBK-1). Rev L4 drive. Owner: "a chain and sprockets would be way less complex" -> no gearbox, no belt.
Per powered axle (4): Poclain MS05 468/234 cc two-speed HighFlow shaft motor with T04 multidisc spring brake, frame-mounted
(slotted bracket on the truck transom), 15T:45T ANSI 120-2 duplex chain (3.00:1) in an oil-bath case, 45T split ring
sprocket bolted to a hub PRESSED/SHRUNK on a raised Ø150 axle seat (NO keyway). Pump H1P053 kept (35 kW anti-stall),
6 mph governed by a sealed H1P max-displacement (stroke) stop at 42 cc + a HARD tamper-sealed 2,600 rpm engine limit (L4.2), independent 7 mph overspeed trip, per-motor speed
sensors, anti-slip = L4.1 ELECTRONIC TRACTION CONTROL (no flow divider - see J["traction_control"]). Nothing outside the wheels; eight Ø1,450 drivers kept.
Folds in: Stress Bot (results_summary.md 28 Oct) axle/adhesion/cooler/derate/overspeed findings; Tender Bot TB-2 tender items.
Sources: Poclain MS05-MSE05 catalog 27/07/2023 (/workspace/ms05.pdf): disp 468/234, HighFlow 2C max 370/430 rpm,
Classic 2C 260/275 rpm, max power HighFlow 2C 50/30 kW, MS 450 bar, T04 brake 4,220/3,165 (residual)/2,740 (dynamic,
max 10 uses) N.m, release 12-30 bar, 85.9 kJ max energy, weight 2-disp HighFlow 55 kg / 64 kg with brake,
shaft CODE 5 = DIN 5480 W55x3x17 male (2A40 keyed Ø50 limited to 800 N.m -> rejected), 2A50 dynamic radial ~60 kN near offset 0
(chart p.20, read off graph - AWAIT Poclain AE), bearing L10 = 10 Mrev at ~30 kN (150 bar avg).
Supplier values not in hand = AWAIT; engineering choices = ASSUMED. No prices."""
import math, json, os
g = 9.80665
J = {}
L3 = json.load(open("/workspace/train/calcs/L3/drive_L3.json"))
# ------------------------------------------------------------------ masses per powered axle (replaces the L3 408.2 kg)
# L4.1 hub: Ø240 x 110 body, bore Ø150, integral Ø350 x 20 flange (was Ø340 / 28 kg ASSUMED), 12 x Ø17 reamed holes on PCD 300 - CALC
_rho = 7850.0
HUB = dict(body_kg=math.pi / 4 * (0.240**2 - 0.150**2) * 0.110 * _rho, flange_kg=math.pi / 4 * (0.350**2 - 0.240**2) * 0.020 * _rho,
           holes_kg=-12 * math.pi / 4 * 0.017**2 * 0.020 * _rho)
HUB_KG = round(sum(HUB.values()), 1)
m_add_axle = dict(MS05_HighFlow_2speed_T04_brake_2A50=64.0, motor_slide_bracket_PL25_jackscrews=35.0, sprocket_15T_Martin_D120B15_splined=13.6,
                  sprocket_45T_rim_ring_bolted=50.0, pressed_hub_4140_flange=HUB_KG, chain_120_2_54_links=24.0,
                  oil_bath_case_seal_plate_oil=50.0, disc_2_calipers=58.0)   # motor = catalog; rest ASSUMED
# L4.2: carry Loco Bot's L-103 LB detail 336.7 kg/axle (bracket_LB 46.7, 15T 14.2, ring bolts 2.04, case_LB 46.4; +10.7/axle, +42.8 loco) - calculated, verify by weighing
m_add_axle["L42_LocoBot_L103_LB_detail_delta"] = round(336.7 - sum(m_add_axle.values()), 2)
m_axle_add = sum(m_add_axle.values())
m_L4_delta = 4 * m_axle_add - 4 * 160 - 136          # same bookkeeping as L3 (DT5 parts removed, stubs shortened)
dm_vs_L3 = m_L4_delta - L3["basis"]["m_L3_delta_kg"]
V_TMR = round(2.19 / 7.73 * 5.3, 2)   # tender MR pipe 3/4 in x ~5.3 m (same bore as the Loco Bot MR feed 2.19 L / 7.73 m)
TENDER_L4 = 8706.5   # L4.2: Tender Bot TB-3.13d 8,706.5 kg, CG [2422.7, 11.3, 1110.4] incl. the tender-end safety-chain shackles (TB-3.13c 8,705.2; TB-3.13b 8,700.1; TB-3.11 8,646.6); brake force unchanged 5.845 kN -> full brake 0.671 m/s2; was TB-3.9 8,616.3 (mixed Coremo D 2N spring sets, 25.4 discs, pad wear limit 5.5, cradle -50); was TB-3.8 8,568.8; was TB-3.4 8,465.3 - Steering 16 TB-3.4: under-deck transformer assembly 168.7 kg (TB-3.3 8,451; TB-3.2 8,395)
dm_tender = TENDER_L4 - 8304.0
# MASS BASIS: route-check RT1 corrected loco (calcs/track/loco_check.json: LT43 double count removed, loco 16,657 kg L3, pony 2.9 kN/wheel)
RT1 = json.load(open("/workspace/train/calcs/track/loco_check.json"))["mass"]
dW = (m_L4_delta - L3["basis"]["m_L3_delta_kg"] + dm_tender) * g / 1000
B_front, B_pony = 650.0, 1250.0       # (B_front is only the starting value - recomputed below from the 1.10 rule) front-pocket ballast (incl. battery box) over the front pivot X4075 + sprung pony with its own 1.25 t ballast (RT1)
# REV L4 steering 6-8 (28 Oct): the 16,657 base INCLUDES the L3 3 mm hood (898 kg; structural_body_study §4 body/shell 1,900 incl. hood)
# -> barrel 2,135 replaces the 898 kg hood: +1,237 kg (the old "1,750" was L-107's provisional shell load, not a base allowance). 93 % front.
# REV L4 Steering 17 (28 Oct): Loco Bot shell package ledger rev 2 (/workspace/loco/mass_ledger.csv) replaces the L4 barrel/bell/L-107/battery lumps.
# Items are CHANGES vs the 16,657 kg corrected base (base includes the L3 3 mm hood 898, L3 PL6 deck 1,248, ~1,000 L3 cab/front = SB-1 body/shell 1,900 - hood 898).
# Smokebox 227.9 is counted IN FULL: the base has no separate smokebox item - the L3 smokebox front sits inside the ~1,002 kg "cab/front" that is already
# removed with the L3 cab (CAB-L3-REMOVE), so there is no double count and no 150 kg placeholder to net off (Loco Bot counted only +77.9).
LB = [("L-108 barrel cans/formers/strips/straps/bands/neoprene (closed-cell)/rivnuts/clips - Loco Bot ledger_out 01:57", 2076.2, 4231.0), ("L-108 frame saddles S2,S3,S5,S6 + S4N narrow (B4) - ledger 01:57", 195.7, 5675.0),
      ("remove L3 3 mm hood shell (in base)", -898.0, 4300.0), ("L-109 smokebox X300-600 + door + S1 saddle + headlight bracket", 227.9, 450.0),
      ("L-110 dome", 10.7, 4400.0), ("L-110 stack (kept - conservative for the front truck)", 9.0, 1100.0), ("L-110 bell (catalogue 8 in) + yoke + ringer - ledger 01:57", 14.3, 2800.0),
      ("L-110 whistle Kahlenberg 118 ACP + valve foot - ledger 01:57", 4.9, 6064.0), ("L-110 fasteners/gaskets", 1.5, 4000.0),
      ("L-107 P1-L rev L.1 net (Al deck, UHMW; 2 HB16 deleted -1.0) - ledger 01:57", 27.2, 6149.0), ("deck stringers SS± C3x4.1 -> HSS3x3x1/8 (P-A1 ADOPTED)", 9.1, 5600.0),
      ("cab L-111 C1", 813.9, 9283.0), ("remove L3 cab/front (in base)", -1000.0, 9350.0), ("cab fit-out C1.1", 6.0, 9900.0),
      ("FT-1 front tow point", 15.6, 200.0), ("L-109 pilot slats PS-1 10 x FB6x50x932 (ledger 01:57; was 54.9)", 21.9, 150.0), ("L-114 JL item (ledger rev 2, 01:32)", 9.7, 10740.0), ("BT-1 battery 2 x GPL-27T + box, Y- front pocket (replaces plates)", 68.2, 4075.0),
      # ---- REV L4.1 additions (28 Oct 2026)
      ("HL-1 headlamp housing (Teknoware PAR56 TL-TVN95112 in Trim box, UPPER BOUND, L-114 HL-1/HL-1M) Z3495", 25.0, 175.0),
      ("109-SBX-7 rev B headlight shelf bracket A36 PL6 (S-504 8.0 kg) - INSIDE the L-109 smokebox 227.9 per Loco Bot mass_ledger (no double count)", 0.0, 175.0),
      ("L4.1 traction-control + loco valve package: tow valve, LP selector/T04 release block + accumulator, PLUS+1 I/O, pony 3rd pickup, harness, mounting PL (ASSUMED)", 28.0, 5675.0),
      ("L4.2 safety-chain parts (Loco Bot E7: 2 x PL44.5 A572-50 lugs faced to 42.5 + PL16 diaphragms, each safety chain = 2 x 1-1/8 in G-2130 shackles + 2 x Crosby S-1325A couplers + 1-2 links of 5/8 G100, chain share) - 32.2 total, +12.7 vs E6", 32.2, 11150.0),
      ("L4.2 traction pins Ø100 -> Ø120 4140 Q&T (+16.3 kg each, 0.6 m) + GE120ES-class bearing and heavier housing (+5.7 kg each, ASSUMED) - front", 22.0, 4075.0),
      ("L4.2 traction pin Ø120 + GE120ES-class housing - rear", 22.0, 7275.0),
      ("L4.2 rear-truck sanders (both directions): 2 boxes 8 kg + 2 x 15 kg sand BODY-MOUNTED between the trucks at X6400 (hoses to the truck nozzles), level switches, flow proof (ASSUMED)", 46.0, 6400.0), ("L4.2 rear-truck sand nozzles/valves/hoses (8) on the truck (ASSUMED)", 8.0, 7275.0),
      ("L4.2 front-truck sander upgrade: 2nd-direction nozzles/valves, level switch, flow proof (ASSUMED)", 6.0, 4075.0),
      ("L4.2 float (loop bypass) valve block: pilot-operated 2/2 cross-port valve >= 420 bar, 200 L/min normally-open (fail-to-float), 2 check/make-up valves, manifold (ASSUMED)", 14.0, 5675.0),
      ("L4.2 T04 per-port Ø1.2 orifices + hard lines / 4SH hose, 2-channel vent switch, 96-tooth pony target wheel + 2 quadrature sensors (ASSUMED)", 7.0, 5675.0),
      ("L4.2 (Loco Bot E8) brake-release piping GROSS excl. the MR feed: BP-1 regulator/relay panel, 2 x 3/4 in 25x2.5 trunks, 4 x 1/2 J1402 hoses, 4 x 1/2 QEVs (option B, maker-certified 15 bar), caliper hoses, switch (43.7 total - 15.2 MR feed)", 28.5, 5675.0),
      ("L4.2 (Loco Bot E8) MR feed JL-A -> BP-1, 3/4 in 316 25 x 2.5, 8.75 m (2.75 L), in the 43.7 kg gross", 15.2, 8190.0),
      # L4.2 E8: the 20 L local release reservoir is DELETED - the coupled MR is ~190 L (Loco Bot E8), one release 6.0 -> 5.68 bar
      ("L4.1 (steering 7) T04 release rev: 6.0 L manual-release accumulator + 1.0 L damping accumulator, brake-line shuttle, hand pump, guarded release valve, charge pressure switch (net of the 0.75 L unit, ASSUMED)", 20.0, 5675.0),
      ("L4.2 K2-a FIX: nose ballast NB-1 PL25.4 600 x 500 A36 (59.8 kg) bolted to the smokebox floor on the S1 saddle at X450 - ahead of the front pivot it unloads the rear truck (R2 static -0.33 kN) so the max driver wheel stays <= 25.9 kN at the start TE; Loco Bot to detail on L-109 (calculated, verify by weighing)", 59.8, 450.0),
      ("L4.2 ballast clamp bars P-106-1 APPROVED: 4 x 106-CB1 FB100x16 x 475 A36 inside the pocket on M16 set screws (L4.1 bars 21.1 superseded)", 23.9, 4075.0),
      ("L4.2 front ballast pockets P-106-2 APPROVED (60 mm walls): 2 x 24.6 kg (end walls PL20, side walls PL12, hold-down tabs, set-screw lugs, liner) + 8 M20 rods/spacers 6.2 + set screws 0.8 + BT-1 straps 3.0 - not previously ledgered", 59.2, 4075.0),
      ("L4.1 low traction pin T1: Ø100 4140 pin from the body centre plate to a GE100ES spherical housing under the transom (traction at Z650) + housing PL16 + body boss (ASSUMED)", 55.0, 4075.0),
      ("L4.1 low traction pin T2 (as T1, ASSUMED)", 55.0, 7275.0),
      ("L4.1 saddle web gussets PL10 45x150, 8 per saddle S1-S6 (L-108, Loco Bot item c)", 12.7, 5675.0),
      ("L4.1 SD-1 caps re-cut inboard to Y+/-50 (+2 x 2 x 0.79)", 1.6, 4075.0), ("L4.1 SD-1 caps re-cut (rear bolster)", 1.6, 7275.0),
      ("L4.1 SD-2 hold-down: 4 x PL16 80x120 clamp plates + 4 x M16 8.8 (rear end sill, no holes)", 5.4, 10862.0)]
FLOW_DIVIDER_KG = 0.0    # L4.1: gear divider DELETED (Jahns HTO-4-35-FI ~160 kg would have been +160 kg on the loco); electronic TC instead
m_items = sum(k for _, k, _x in LB)
d_barrel, f_barrel_front = 2076.2 + 195.7 - 898.0, None
m_bell, x_bell = 40.3, None          # L-110 fittings total (bell, dome, stack, whistle)
m_L107, x_L107 = 27.2 + 9.1, 6015.0
m_cab_new, x_cab_new, m_cab_old, x_cab_old = 813.9, 9283.0, 1000.0, 9350.0
m_ft1, x_ft1 = 15.6, 200.0
m_batt, x_batt = 68.2, 4075.0        # BT-1 moved to the Y- front pocket (Electro E3.3), replaces ballast kg-for-kg
m_jump = 40.0                       # Electro E3: 2/0 inter-vehicle jumpers (tender/coaches) - train W only
fr = lambda x: (7275.0 - x) / 3200.0  # front-truck share of a mass at X (pivots X4075/X7275)
front_extra_kg = sum(k * fr(x) for _, k, x in LB)
rear_extra_kg = m_items - front_extra_kg
# front ballast REBALANCED: smallest plate-pair multiple (2 x 75.4 kg) giving equal-torque dry 2 % start margin 1.10 (owner decision C9), cap 1,500
_W0 = RT1["train_corr_kN"] + dW + (B_pony + m_items + m_jump) * g / 1000
_a0 = min(RT1["axles_corr_kN"][k] + dm_vs_L3 / 4 * g / 1000 + (front_extra_kg if k[0] == "F" else rear_extra_kg) * g / 2000 for k in ("F1", "F2", "R1", "R2"))
_B = max(0.0, (1.10 * 0.0408 * _W0 - 4 * 0.25 * _a0) / (4 * 0.25 * g / 2000 - 1.10 * 0.0408 * g / 1000))
B_plate = 75.4   # L4.1: 1 in (25.4) A36 cut 800 x 473 = 75.45 kg at 7,850 (Source Bot rev 3.5.1)
B_front = min(1500.0, max(2, math.ceil(_B / B_plate)) * B_plate)   # L4.1: 2 plates minimum (1 per pocket, lateral balance vs BT-1)   # Steering 17: trimmed to single 75.4 kg plates (battery BT-1 68.2 kg already in the Y- pocket); plates 1 per side, BT-1 left as a 68.2 kg Y- offset
W = RT1["train_corr_kN"] + dW + (B_front + B_pony + m_items + m_jump) * g / 1000
m_train = W * 1000 / g
loco_kg = RT1["loco_corr_kg"] + dm_vs_L3 + B_front + B_pony + m_items
r = 0.725; D = 1.45
ax = {k: round(RT1["axles_corr_kN"][k] + dm_vs_L3 / 4 * g / 1000 + ((B_front + front_extra_kg) * g / 2000 if k[0] == "F" else rear_extra_kg * g / 2000), 2) for k in ("F1", "F2", "R1", "R2")}  # adhesion basis (corrected + 1 t front ballast)
ax_noballast = {k: round(RT1["axles_corr_kN"][k] + dm_vs_L3 / 4 * g / 1000 + (front_extra_kg * g / 2000 if k[0] == "F" else rear_extra_kg * g / 2000), 2) for k in ("F1", "F2", "R1", "R2")}
ax_asis = {k: round(RT1["axles_L3asis_kN"][k] + dm_vs_L3 / 4 * g / 1000 + ((B_front + front_extra_kg) * g / 2000 if k[0] == "F" else rear_extra_kg * g / 2000), 2) for k in ("F1", "F2", "R1", "R2")}  # Stress Bot L3-as-is basis
drv = sum(ax.values())
need = lambda R=None, grade=0.0: W * (0.0208 + grade / 100 + (0.4 / (R - 20) if R else 0.0))   # Röckl 400/(R-20) N/kN
need2 = 0.0408 * W
# ------------------------------------------------------------------ L4.1 (Stress Bot loco round 2 #2): truck-pitch weight transfer under traction
# The traction force enters each truck at height h above rail -> per-axle transfer TE_truck*h/wb inside the truck (lead axle of each truck unloads)
# + inter-truck body pitch from the drawbar (h - h_coupler). As modelled (build/model.py) the force passes through the centre plate / pivot seat
# Z1050-1110 (GE100ES spherical pivot ~Z1080) -> h_p = 1.08 m: forward 2 % margin 0.94, reverse 0.69 = NG. FIX (L4.1): LOW TRACTION PIN per truck -
# Ø100 4140 pin hanging from the body centre plate through the transom to the GE100ES spherical bearing in a housing under the transom at Z650;
# the centre plate becomes a flat bronze/PTFE-lined vertical bearing (no longitudinal spigot load). h_t = 0.65 m.
H_PIVOT_MODEL, H_T, H_CPL, WB_T, PIV_T = 1.08, 0.65, 0.55, 1.55, 3.2
def ax_tr(TE, d=1, h=H_T):
    Fd = TE * (m_train_ - loco_kg_) / m_train_
    intra = TE / 2 * h / WB_T; inter = Fd * (h - H_CPL) / PIV_T / 2
    if d > 0:
        return dict(F1=ax["F1"] - intra + inter, F2=ax["F2"] + intra + inter, R1=ax["R1"] - intra - inter, R2=ax["R2"] + intra - inter)
    return dict(F1=ax["F1"] + intra - inter, F2=ax["F2"] - intra - inter, R1=ax["R1"] + intra + inter, R2=ax["R2"] - intra + inter)
m_train_, loco_kg_ = m_train, loco_kg
def te_cap(d, h=H_T, mu_=0.25):     # self-consistent equal-torque adhesion cap: TE = 4 mu min(axle(TE))
    TE = 30.0
    for _ in range(80): TE = 4 * mu_ * min(ax_tr(TE, d, h).values())
    return TE
def h_for(mreq, d=1):
    lo, hi = 0.0, 1.5
    for _ in range(60):
        mid = (lo + hi) / 2
        ok = min(ax_tr(need2, d, mid).values()) / need2 >= mreq
        lo, hi = (mid, hi) if ok else (lo, mid)
    return round(lo, 3)
WTR = {}
F350_pre = 4 * 468.0 * 350 / (20 * math.pi) * 0.90 * 3 * 0.97 / 0.725 / 1000   # = F350 below
for lab, h in (("as_modelled_pivot_1p08", H_PIVOT_MODEL), ("L41_traction_pin_0p65", H_T)):
    rr = {}
    for dn, d in (("forward", 1), ("reverse", -1)):
        a = ax_tr(need2, d, h); cap_ = te_cap(d, h); ac = ax_tr(min(cap_, F350_pre), d, h)
        rr[dn] = dict(axles_at_need={k: round(v, 2) for k, v in a.items()}, min_axle_kN=round(min(a.values()), 2), margin_2pct_dry_sanded=round(min(a.values()) / need2, 3),
                      margin_2pct_wet_unsanded=round(0.6 * min(a.values()) / need2, 3), equal_torque_cap_kN=round(cap_, 2),
                      max_grade_start_pct=round((cap_ / W - 0.0208) * 100, 2), max_wheel_at_cap_kN=round(max(ac.values()) / 2, 2))
    WTR[lab] = dict(h_m=h, **rr)
K2A_WHEEL = max(WTR["L41_traction_pin_0p65"][d]["max_wheel_at_cap_kN"] for d in ("forward", "reverse"))
J["basis"] = dict(loco_items_S17=[dict(item=n, kg=k, X=x) for n, k, x in LB], loco_items_sum_kg=round(m_items, 1), loco_kg=round(loco_kg), barrel_delta_kg=d_barrel, barrel_front_share=f_barrel_front, bell_kg=m_bell, front_truck_extra_kg=round(front_extra_kg), rear_truck_extra_kg=round(rear_extra_kg),
                  L107_kg=m_L107, L107_X=x_L107, cab_C1_kg=m_cab_new, cab_C1_X=x_cab_new, cab_L3_removed_kg=m_cab_old, FT1_kg=m_ft1, deck_L3_in_base_kg=1248.1, battery_kg=m_batt, battery_X=x_batt, jumpers_kg=m_jump, hood_in_base_kg=898.0,
                  mass_open="Steering 17: Loco Bot ledger rev 2 items (LB list) - L-108 barrel 2,088.3 + saddles 192.3 (S4N), L-109 smokebox 227.9 counted IN FULL (L3 smokebox front is inside the ~1,000 kg L3 cab/front already removed - no double count), L-110 fittings 51, L-107 P1-L rev L.1 net +28.2 + C3 stringers to HSS3x3x1/8 +9.1, cab C1 813.9 for the ~1,000 L3 cab/front, fit-out 6, FT-1 15.6, BT-1 battery 68.2 in the Y- front pocket; front plates trimmed 1,056 -> %.1f kg (equal-torque dry 2%% start margin kept >= 1.10); REV L4.1 (Loco Bot ledger_out 01:57 folded in: barrel 2,076.2, saddles 195.7, bell 14.3, whistle 4.9, slats 54.9 -> 21.9, L-107 -1.0): + HL-1 headlamp housing 25 (upper bound) at X175 (109-SBX-7 rev B 8.0 is inside the smokebox 227.9 - not added twice), + TC/valve package 28 @X5675, + ballast clamp bars 21.1 @X4075, hub 28 -> 31.4 kg/axle; NO flow divider (160 kg avoided); 2 x 75.4 kg plates kept (1 per pocket, 2 minimum)" % B_front, ballast_front_kg=B_front, pony_own_ballast_kg=B_pony, axle_loads_kN_no_front_ballast=ax_noballast, max_driver_wheel_kN=round(K2A_WHEEL, 2), max_driver_wheel_L3asis_static_kN=round(max(ax_asis.values()) / 2, 2), wheel_limit_kN=26.0, axle_loads_kN_L3asis_plus_L4=ax_asis, added_per_axle_kg=m_add_axle, added_per_axle_total_kg=m_axle_add, m_L4_delta_kg=round(m_L4_delta), change_vs_L3_kg=round(dm_vs_L3),
                  change_vs_L3_per_axle_kg=round(m_axle_add - L3["basis"]["added_per_axle_total_kg"], 1), tender_kg=TENDER_L4, tender_change_kg=dm_tender,
                  train_kg=round(m_train), W_kN=round(W, 1), driver_weight_kN=round(drv, 1), sum_axles_kN=round(sum(ax.values()), 1),
                  need_2pct_start_kN=round(need2, 2), v_governed_mph=6.0, v_overspeed_trip_mph=7.0,
                  axle_loads_kN_RT1corr_plus_L4=ax, mass_note="Study said ~-150 kg/axle; itemised L4 (incl. oil-bath case, seal plate, split ring sprocket, kept disc/calipers) gives %+.0f kg/axle. Adhesion uses the RT1-corrected axle loads (loco %d kg, lightest F2 %.2f kN); the axle seat and axleboxes use the heaviest L3-as-is axle (%.2f kN) - conservative until the weigh-in." % (m_axle_add - 408.2, loco_kg, ax["F2"], max(ax_asis.values())))
# ------------------------------------------------------------------ components / efficiencies
Vg1, Vg2, i_ch = 468.0, 234.0, 45 / 15
eta_s, eta_s_pess, eta_hm, eta_v, eta_ch = 0.90, 0.80, 0.92, 0.95, 0.97     # ASSUMED (start eff AWAIT Poclain); roller chain 0.97 in oil bath
Q_full, Vp, n_e = 133.0, 53.8, 2600.0
def T_m(Vg, p, eta=1.0): return Vg * p / (20 * math.pi) * eta                 # N.m per motor
def F_te(Vg, p, eta): return 4 * T_m(Vg, p, eta) * i_ch * eta_ch / r / 1000
J["components"] = dict(motor="Poclain MS05 HighFlow 2-displacement (2C) 468/234 cc, shaft code 5, DIN 5480 W55x3x17 (male), T04 parking/emergency multidisc brake, speed sensor TR/T4 (56 ppr), 450 bar max (MS), 64 kg - model code AWAIT Poclain",
                       chain="ANSI 120-2 (ISO 24B-2 equivalent NOT interchangeable - ANSI 120-2 specified) duplex roller chain, pitch 38.1, 54 links, riveted/connecting link per maker, heavy-series sidebars optional",
                       sprockets="15T: Martin D120B15 (Type B hub, hardened teeth, 13.6 kg, OD 202 published) hub broached DIN 5480 N55x3x17 (female) to suit MS05 shaft code 5, DIN 5480 W55x3x17 (male); engaged length = FULL shaft spline (~60 mm, AWAIT Poclain drawing; min 58 mm) + end plate, no setscrew (2A40 keyed and 2AC0 pinion shafts rejected). 45T (Source Bot rev 3): 120-2 SPLIT rim ring with a bolting web on the Ø350 flange (L4.1) of the pressed 4140 hub (ring ~50 kg ASSUMED, hub %.1f kg CALC)" % HUB_KG + "; the earlier Tsubaki D120A45 solid plate is superseded. Martin D120C45 cast hub (85 kg) REJECTED for unsprung mass. Teeth flame/induction-hardened option requested. Chain: Tsubaki RS120-2 (allowable 51.7 kN, 11.7 kg/m)",
                       hub="4140 Q&T (28-32 HRC) flanged hub Ø240 x 110, integral flange Ø350 x 20 (L4.1, was Ø340), bore Ø150 on a raised axle seat, diametral interference 0.15-0.20 mm, SHRINK FIT ONLY (hub heated to 200-230 °C; oil-pressing deleted - Stress Bot r2: SF 0.87); oil-injection groove in the hub bore + plugged port for REMOVAL ONLY (fit passes with the groove land deducted, see press_fit); hub-edge relief, witness marks for creep (no keyway)",
                       case="oil-bath chain case 3 mm steel, mounted to the motor bracket (sprung truck frame); axle passes through a floating seal plate (lip seal on the hub land, PTFE-faced plate sliding in a frame guide for +/-25 mm vertical primary travel; hard bump stops at +/-22 mm) - ASSUMED design, CWF/PE to confirm; ISO VG 220 EP gear oil ~4 L, lower strand immersed 6-12 mm, sight glass, magnetic drain, breather",
                       pump="Danfoss H1P053 kept (input shaft G1 = ISO 3019-1 Ø32-4, 14T 12/24, SAE B 2-bolt flange - see J['pump_shaft']: the AIE SAE B 13T drive needs a 14T 12/24 coupling hub; L35 PL 350 / HPRV 380 (L4.2 pressure revision; was 400), EDC + PLUS+1, 35 kW anti-stall); max-displacement (stroke) limiter set to 42 cc and sealed (6 mph)",
                       antislip="L4.1: NO flow divider. Electronic traction control in PLUS+1: per-motor MS05 sensors + a 3rd pickup on the unbraked pony tone ring (ground-speed reference), pump destroke on slip, auto-sand, start always in 1st, hill-start hold - J['traction_control']",
                       valves="L4.1: T04 release via low-pressure selector + 3-way solenoid (normally vented = brakes applied) + 0.75 L accumulator; tow = lockable >= 420 bar ball valve across A/B (L4.2) + Poclain freewheel - J['loco_valves']",
                       eff=dict(motor_start_hm=eta_s, motor_start_pessimistic=eta_s_pess, motor_run_hm=eta_hm, motor_vol=eta_v, chain=eta_ch))
# ------------------------------------------------------------------ start / adhesion (0 % + curve and 2 %), dry / wet / sanded
P_HPRV = 380.0   # L4.2 pressure revision: PL 350 / HPRV 380 bar (Oct 27 basis, 30 bar PL-HPRV spacing; no -16 assembly >= 450 bar exists)
P_STR = 430.0    # L4.2 STRENGTH basis: transient spike above the HPRV ~430 bar - every strength case is checked at 430 (parent basis 10:22)
F350 = F_te(Vg1, 350, eta_s); F400 = F_te(Vg1, P_STR, eta_s);   # name kept: F400 = TE at the strength pressure (now 430)
F350p = F_te(Vg1, 350, eta_s_pess)
mu = dict(dry=0.25, wet=0.15, sanded=0.25)
amin = min(ax.values()); asum = sum(ax.values()); amin0 = min(ax_noballast.values())
def cap(m, mode):     # adhesion cap (kN): equal torque -> lightest axle governs; flow divider (speed-locked) -> sum of axles
    return 4 * mu[m] * amin if mode == "equal" else mu[m] * asum
cases = []
for lab, R, gr in (("0% tangent", None, 0.0), ("0% + R100", 100, 0.0), ("0% + R60", 60, 0.0), ("0% + R50", 50, 0.0), ("2% tangent", None, 2.0), ("2% + R100 uncompensated", 100, 2.0)):
    n_ = need(R, gr)
    row = dict(case=lab, need_kN=round(n_, 2), TE_350_kN=round(F350, 1), TE_350_eta080_kN=round(F350p, 1))
    for m in mu:
        for mode in ("equal", "divider"):
            c_ = min(cap(m, mode), F350)
            row[f"{m}_{mode}_cap_kN"] = round(c_, 1); row[f"{m}_{mode}_margin"] = round(c_ / n_, 2)
    for m in mu: row[f"gov_{m}_margin"] = row[f"{m}_equal_margin"]   # L4.1 governing = equal torque (no divider)
    cases.append(row)
# front ballast needed so the EQUAL-torque (divider failed/bypassed) dry 2 % start has margin 1.10
W0 = W - B_front * g / 1000
B = 0.0
for _ in range(50):
    Wb = W0 + B * g / 1000
    B = max(0.0, (1.10 * 0.0408 * Wb / (4 * 0.25) - amin0) * 2 * 1000 / g)
B_plates = math.ceil(B / 2 / 75.4)
B100 = max(0.0, (0.0408 * W0 - 4 * 0.25 * amin0) / (4 * 0.25 * g / 2000 - 0.0408 * g / 1000))
J["start"] = dict(F350_kN=round(F350, 2), F400_kN=round(F400, 2), F_strength_kN=round(F400, 2), F_HPRV380_kN=round(F_te(Vg1, P_HPRV, eta_s), 2), p_HPRV_bar=P_HPRV, p_strength_bar=P_STR, F350_eta080_kN=round(F350p, 2), need_2pct_kN=round(need2, 2),
                  p_for_need_bar=round(350 * need2 / F350), p_for_need_eta080_bar=round(350 * need2 / F350p), adh_avg_dry_kN=round(0.25 * drv, 2),
                  lightest_axle=min(ax, key=ax.get), lightest_axle_kN=amin, heaviest_axle_kN=max(ax_asis.values()), cases=cases,
                  ballast_front_kg_for_equal_torque_margin_110=round(B), ballast_plates_per_side=B_plates, ballast_front_kg_for_equal_torque_margin_100=round(B100), ballast_capacity_kg=1500,
                  rules=["Sand is MANDATORY for any start on a wet rail on grade or on curves < R100 (sanders lead axle each direction; mu_sand 0.25)",
                         "L4.1: NO flow divider - every start is an equal-torque (parallel-loop) start: cap = 4 x mu x lightest axle; electronic traction control (pump destroke on slip, auto-sand) keeps adhesion; start in 1st",
                         ("Front: Loco Bot shell package (S17 ledger) +%.0f kg on the front truck + %.0f kg pocket ballast plates + 68.2 kg BT-1 battery (F2 +%.1f kN) - " % (front_extra_kg, B_front, (B_front + front_extra_kg) * g / 2000)) + "equal-torque 2%% start needs %.0f kg pocket ballast for margin 1.0, %.0f kg for 1.10 (1.5 t pockets) - plates set by the 1.10 rule (2 minimum)" % (B100, B)],
                  note="L4.1 GOVERNING cap = equal-torque (parallel loop) 4*mu*lightest axle (Stress Bot t1). The *_divider_* columns are kept for information only (L4 gear divider deleted). TE at 350 bar exceeds the dry cap -> adhesion-limited.")
# ------------------------------------------------------------------ speeds, governor, spin
def wheel_rpm(mph): return mph * 0.44704 / (math.pi * D) * 60
def motor_rpm(mph): return wheel_rpm(mph) * i_ch
Q_stop = lambda Vp_cc: n_e * Vp_cc / 1000 * 0.95
Vp_6 = 4 * Vg2 * motor_rpm(6.0) / eta_v / (n_e * 0.95)
Vp_stop = 42.0          # L4.2 (Stress Bot r3 N3 ruling): sealed stop back to 42 cc; the engine has a HARD, tamper-sealed 2,600 rpm limit (no high idle above 2,600) so 6 mph is kept
n_hi = 2600.0           # L4.2: hard engine speed limit = rated (was 2,850 high idle ASSUMED)
def v_of(Q, Vg): return Q * eta_v / (4 * Vg / 1000) / i_ch / 60 * math.pi * D / 0.44704
spin2 = Q_stop(Vp_stop) * eta_v / (Vg2 / 1000); spin1 = Q_stop(Vp_stop) * eta_v / (Vg1 / 1000)
J["speed"] = dict(wheel_rpm_6mph=round(wheel_rpm(6), 1), motor_rpm_6mph=round(motor_rpm(6), 1), chain_mps_6mph=round(motor_rpm(6) * 15 * 0.0381 / 60, 2),
                  pump_cc_for_6mph=round(Vp_6, 1), pump_stop_set_cc=Vp_stop, Q_at_stop_Lmin=round(Q_stop(Vp_stop), 1),
                  vmax_2nd_at_stop_mph=round(v_of(Q_stop(Vp_stop), Vg2), 2), vmax_1st_at_stop_mph=round(v_of(Q_stop(Vp_stop), Vg1), 2),
                  vmax_2nd_stop_removed_mph=round(v_of(Q_stop(Vp), Vg2), 2), vmax_1st_stop_removed_mph=round(v_of(Q_stop(Vp), Vg1), 2),
                  motor_max_rpm=dict(HighFlow_2C_1st=370, HighFlow_2C_2nd=430, Classic_2C_1st=260, Classic_2C_2nd=275),
                  spin_one_axle_2nd_rpm=round(spin2), spin_one_axle_1st_rpm=round(spin1), n_engine_rated=n_e, n_engine_high_idle_ASSUMED=n_hi,
                  vmax_2nd_high_idle_mph=round(v_of(Q_stop(Vp_stop) * n_hi / n_e, Vg2), 2), spin_one_axle_2nd_high_idle_rpm=round(spin2 * n_hi / n_e),
                  stop_rule="L4.1: stroke stop 38 cc sealed: 6 mph is reached only at high idle (%.2f mph at 2,850 rpm); at rated 2,600 under load %.2f mph. Spin at high idle %d rpm vs HighFlow 430 (util %.2f). PLUS+1 also commands 2,600 rpm when the Kubota ECU allows (AIE data held)." % (v_of(Q_stop(Vp_stop) * n_hi / n_e, Vg2), v_of(Q_stop(Vp_stop), Vg2), spin2 * n_hi / n_e, spin2 * n_hi / n_e / 430),
                  spin_note="One wheelset spinning alone at the 38 cc stop (rated 2,600): %d rpm in 2nd (HighFlow limit 430 -> util %.2f; Classic 275 -> NG) -> HighFlow valving REQUIRED; 1st %d rpm (limit 370) - hardware-safe with NO software; electronic TC destrokes on slip" % (spin2, spin2 / 430, spin1),
                  hardware_note="With the stroke stop removed the hardware tops out at %.1f mph (2nd) - far below L3's 10 mph capability" % v_of(Q_stop(Vp), Vg2),
                  shift="PLUS+1 shifts all 4 motors together: 1st (468 cc) below 2.5 mph or loop dp > 300 bar; 2nd (234 cc) above 3.0 mph with dp < 180 bar (hysteresis). Shift-on-the-move rating AWAIT Poclain.")
# ------------------------------------------------------------------ power-limited speeds (35 kW; hot-day 34.5 kW with compressor clutched)
def run_res(gr, R=None): return W * (0.005 + gr / 100 + (0.4 / (R - 20) if R else 0.0))
def hold(Fk, P, Qmax=Q_stop(Vp_stop)):
    best = None
    for Vg in (Vg2, Vg1):
        Tm = Fk * 1000 * r / 4 / (i_ch * eta_ch)
        dp = Tm * 2 * math.pi / (Vg / 1e6) / 1e5 / eta_hm
        if dp > (300 if Vg == Vg2 else 350): continue
        P_rim = P * 0.855 * eta_hm * eta_v * dp / (dp + 10) * eta_ch
        v = min(P_rim / Fk / 0.44704, v_of(Qmax, Vg), 6.0)
        lim = "governor" if v >= 6.0 - 1e-6 else ("flow" if abs(v - v_of(Qmax, Vg)) < 1e-6 else "power")
        if best is None or v > best[0]: best = (v, Vg, round(dp), lim, round(P_rim, 1))
    return best
tab = []
for gr, R in ((0, None), (0, 100), (0, 50), (0.5, None), (1.0, None), (1.5, None), (2.0, None)):
    a = hold(run_res(gr, R), 35.0); b = hold(run_res(gr, R), 34.5); c = hold(run_res(gr, R), 32.0)
    tab.append(dict(grade_pct=gr, R=R, resistance_kN=round(run_res(gr, R), 2), mph_35kW=round(a[0], 2), disp_cc=a[1], dp_bar=a[2], limit=a[3], rim_kW=a[4],
                    mph_hotday_34p5kW=round(b[0], 2), mph_32kW=round(c[0], 2)))
J["power_speed"] = dict(table=tab, hold_2pct_mph=[t for t in tab if t["grade_pct"] == 2.0][0]["mph_35kW"], hold_2pct_hot_mph=[t for t in tab if t["grade_pct"] == 2.0][0]["mph_hotday_34p5kW"],
                        target_mph=2.0, method="pump allowance x pump 0.855 x motor 0.92 hm x 0.95 vol x dp/(dp+10) x chain 0.97; best of 1st/2nd displacement with dp <= 350; flow cap at the 42 cc stop; 6 mph governor")
# ------------------------------------------------------------------ hot-day engine / cooler (Stress Bot #6/#7, Tender Bot §3/§6)
P_eng43 = 40.5; P_alt = 2.3; P_comp = 3.7
qloss = (1 - 0.855 * 0.87) * 35.0                          # loop loss (pump 0.855, MS05 overall ~0.87 ASSUMED); L4.1: divider loss term removed (no divider)
J["hotday"] = dict(engine_net_43C_kW=P_eng43, demand_compressor_off_kW=round(35 + P_alt, 1), util_off=round((35 + P_alt) / P_eng43, 3),
                   demand_compressor_on_kW=round(34.5 + P_alt + P_comp, 1), util_on=round((34.5 + P_alt + P_comp) / P_eng43, 3),
                   rule="compressor electric clutch engages only at low traction demand or MR < 7.0 bar; anti-stall map drops to 34.5 kW while clutched; hydraulic cooler fan electric 24 V from the genset charger (not on the engine/alternator)",
                   cooler_heat_kW=round(qloss, 1), cooler_spec_kW=14.0, cooler_util=round(qloss / 14.0, 2),
                   cooler_spec="Air-oil cooler >= 14 kW at 43 °C OUTSIDE air, oil in 70 °C (ETD 27 K), on the low-pressure return / flushing line, own ducted louvre on the tender LEFT wall X3455-4145 (Tender Bot TB-2), case-pressure bypass check upstream; AWAIT supplier curve")
# ------------------------------------------------------------------ chain
p_c = 38.1; N1, N2 = 15, 45
PD1 = p_c / math.sin(math.pi / N1); PD2 = p_c / math.sin(math.pi / N2)
def C_of(links):
    a = 2.0; b = (N1 + N2) / 2 - links; c = ((N2 - N1) / (2 * math.pi))**2
    x = (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a); return x * p_c
links = 54; C_new = C_of(links); C_2 = C_of(links * 1.02); C_3 = C_of(links * 1.03)
wrap = 180 - 2 * math.degrees(math.asin((PD2 - PD1) / 2 / C_new))
T_hprv_ax = T_m(Vg1, P_STR) * i_ch                      # no efficiency credit
T_slip_heavy = max(ax_asis.values()) * 0.25 * r            # divider can load the heaviest axle to its slip
T_run2 = run_res(2.0) * r / 4                         # kN.m per axle running 2 %
pull = lambda T_kNm: T_kNm * 1000 / (PD2 / 2 / 1000) / 1000
P_ult = 2 * 151.2 * 0.85      # ANSI 120 min tensile 34,000 lbf x 2 strands x 0.85 multi-strand factor (kN)
P_allow = 51.7                # Tsubaki RS120-2 max allowable load 51.7 kN (Source Bot rev 2, catalog)
J["chain"] = dict(PD_driver_mm=round(PD1, 1), PD_driven_mm=round(PD2, 1), OD_driven_mm_approx=round(PD2 + 0.6 * p_c), ratio=i_ch, links=links,
                  C_new_mm=round(C_new, 1), C_at_2pct_mm=round(C_2, 1), C_at_3pct_mm=round(C_3, 1), slide_range_mm=round(C_3 - C_new + 3, 0),
                  centre_pitches=round(C_new / p_c, 1), wrap_driver_deg=round(wrap, 1),
                  pull_HPRV_kN=round(pull(T_hprv_ax / 1000), 1), pull_slip_heaviest_kN=round(pull(T_slip_heavy), 1), pull_run_2pct_kN=round(pull(T_run2), 1), pull_run_level_kN=round(pull(run_res(0) * r / 4), 1),
                  ultimate_kN=round(P_ult), SF_ult_HPRV=round(P_ult / pull(T_hprv_ax / 1000), 1), SF_ult_slip=round(P_ult / pull(T_slip_heavy), 1),
                  allow_kN_ASSUMED=P_allow, util_allow_HPRV=round(pull(T_hprv_ax / 1000) / P_allow, 2), util_allow_run2=round(pull(T_run2) / P_allow, 2),
                  axle_T_HPRV_Nm=round(T_hprv_ax), axle_T_slip_heaviest_Nm=round(T_slip_heavy * 1000),
                  vertical_travel_note="motor on the sprung truck frame, chain line horizontal: 25 mm primary travel changes centres by %.1f mm" % (25**2 / (2 * C_new)),
                  reversing="bidirectional + motor brake through the chain: both strands become tight in turn -> fixed centres (slotted motor bracket + jack screws), NO spring idler",
                  maintenance=["Oil bath ISO VG 220 EP: check level weekly (sight glass), change every 500 h or each season (magnetic drain plug)",
                               "Tension: check sag monthly / 100 h at static ride height: 17-20 mm at mid-span (keeps >= 14 mm at full suspension travel) with the motor brake released; adjust with the motor-bracket jack screws and re-torque the slide bolts",
                               "Elongation: measure over 10 pitches every 250 h; REPLACE the chain at 2 % (short 11-pitch centres wear sprockets fast); 3 % is the absolute limit (slide range is sized for it)",
                               "Sprockets: replace the 15T at every chain change. The 45T is a rim-only SPLIT ring (2 halves, Source Bot rev 3) bolted to the pressed-hub flange: unbolt and replace in place, NO pressing and NO wheelset drop",
                               "Seal plate / breather: inspect for leaks weekly; oil on the wheel or rail = stop the train (adhesion)"])
# --- case clearance (parent steering 28 Oct: >= 15 mm radial at 3 % wear + suspension travel) and take-up without an idler
travel = 25.0                                   # primary vertical travel each way (axle vs sprung truck frame, LT18 window)
ride_out = lambda N, e: e * p_c / (2 * math.sin(math.pi / N))   # chain rides out on the teeth at elongation e
OD2 = PD2 + 0.6 * p_c; OD1 = 202.0; OD1_L4 = PD1 + 0.6 * p_c; wall = 3.0   # L4.1: Martin D120B15 published OD 202 (L4 used ~206)
r_case_axle = OD2 / 2 + ride_out(N2, 0.03) + travel + 15.0       # case is on the truck frame; the 45T moves with the axle
x_case_motor = C_3 + OD1_L4 / 2 + ride_out(N1, 0.03) + 15.0        # motor end: case built to the L4 size (OD 206 basis); L4.1 clearance recomputed with OD 202 below
dC_travel = math.hypot(C_new, travel) - C_new
deltaL0 = lambda f: 8 * f * f / (3 * C_new)                        # slack length for mid-span sag f
f_install = math.sqrt(3 * C_new * (deltaL0(0.02 * C_new) + 2 * dC_travel) / 8)
J["case_clearance"] = dict(rule=">= 15 mm radial from every sprocket/chain envelope at 3 %% elongation + full primary travel (+/-%.0f mm)" % travel,
    axle_end_inner_radius_mm=round(r_case_axle, 1), axle_end_outer_mm=round(r_case_axle + wall, 1), OD_45T=round(OD2, 1), ride_out_45T_3pct=round(ride_out(N2, 0.03), 1),
    motor_end_inner_from_axle_mm=round(x_case_motor, 1), motor_end_outer_from_axle_mm=round(x_case_motor + wall, 1), ride_out_15T_3pct=round(ride_out(N1, 0.03), 1),
    model_case="X -%.0f..C_new+%.0f from the axle, Z axle +/-%.0f (was -310..C+125, +/-305 - FAILED at 3 %%: the 15T would have hit the end wall)" % (r_case_axle + wall, x_case_motor + wall - C_new, r_case_axle + wall),
    motor_end_clearance_OD202_mm=round(x_case_motor - C_3 - OD1 / 2 - ride_out(N1, 0.03), 1), OD_15T_Martin=OD1, OD_15T_L4_approx=round(OD1_L4, 1),
    axle_end_clearance_mm=round(r_case_axle - OD2 / 2 - ride_out(N2, 0.03) - travel, 1),
    L41_note="15T OD 202 (Martin) < 206 used to size the case: motor-end clearance at 3 %% + travel rises 15.0 -> %.1f mm (>= 15 OK); case size unchanged; 15T to sideframe chord 85 mm (lateral, unchanged)" % (x_case_motor - C_3 - OD1 / 2 - ride_out(N1, 0.03)),
    seal_plate="floating seal plate at the axle must allow +/-%.0f mm vertical (bump stops +/-22) and +/-1 mm lateral axle motion (L4.1 axlebox side float <= +/-1) (lip seal on a sliding plate in a guided frame, labyrinth + V-ring) - OPEN item OI-L4-5" % travel)
J["take_up"] = dict(dC_full_travel_mm=round(dC_travel, 2), sense="any vertical axle movement from the horizontal static chain line LENGTHENS the centres (C' = sqrt(C^2 + dz^2))",
    install_sag_mm=round(f_install, 1), sag_at_full_travel_mm=round(math.sqrt(max(0, 3 * C_new * (deltaL0(f_install) - dC_travel) / 8)), 1),
    verdict="OK WITHOUT AN IDLER: set the sag at static ride height to %.0f-%.0f mm (motor brake released, axle at ride height); at full bump/rebound it falls to ~%.0f mm (>= 2%% of span), never tight. Slotted motor mount (4 x M20 10.9 in 50 mm slots) + 2 x M20 jack screws, slide %.0f mm covers 3 %% wear." % (f_install, f_install + 3, math.sqrt(max(0, 3 * C_new * (deltaL0(f_install) - dC_travel) / 8)), C_3 - C_new + 3))
# L4.1 (Stress Bot r2 #3): CORRECT slack geometry - slack length S = 8 f^2/(3 span), and a centre change dC uses dL = (2 span / C) dC of it (L4 used dL = dC, L = C)
span_ch = math.sqrt(C_new**2 - ((PD2 - PD1) / 2)**2); dLdC = 2 * span_ch / C_new; BUMP = 22.0
S_of = lambda f: 8 * f * f / (3 * span_ch); f_of = lambda S: math.sqrt(max(S, 0) * 3 * span_ch / 8)
def z_tight(f0, z0):   # axle rise from static (chain line offset z0 from horizontal) at which the slack is used up
    return math.sqrt((math.sqrt(C_new**2 + z0**2) + S_of(f0) / dLdC)**2 - C_new**2) - z0
SL = {}
for f0 in (17.0, 20.0):
    for z0 in (0.0, 3.0, 10.0):
        dC = math.sqrt(C_new**2 + (z0 + BUMP)**2) - math.sqrt(C_new**2 + z0**2)
        SL[f"sag{f0:.0f}_offset{z0:.0f}"] = dict(bump_to_tight_mm=round(z_tight(f0, z0), 1), margin_vs_stop22=round(z_tight(f0, z0) / BUMP, 2), sag_at_stop_mm=round(f_of(S_of(f0) - dLdC * dC), 1))
J["chain_slack_L41"] = dict(span_mm=round(span_ch, 1), dL_dC=round(dLdC, 3), bump_stops_mm=BUMP, axle_side_float_mm=1.0, cases=SL,
    pitch_under_traction_mm=round(need2 / 2 * H_T / WB_T / (2 * 0.58), 1),
    L4_error="L4 D2-f used dL = dC and L = C (slack 0.75 of 1.93 mm) - corrected here (Stress Bot r2)",
    rules=["Hard vertical bump stops +/-22 mm axle vs truck frame (primary travel 25 kept as the case/seal-plate envelope)",
           "Axlebox lateral (side) float <= +/-1 mm (thrust faces shimmed); chain-line coplanarity at install <= 0.4 mm with the axle centred",
           "RE-SHIM PROCEDURE: restore body/coupler height for wheel wear with shims at the CENTRE PLATE / side bearers (body-truck), NEVER under the primary springs. A primary re-shim (spring set) is limited to 3 mm total and is ALWAYS followed by a motor-slide reset: loosen the 4 x M20, re-set the sag to 17-20 mm at ride height with the chain line horizontal +/-3 mm, re-torque 610 N.m, record",
           "Sag 17-20 mm at static ride height, checked monthly / 100 h; chain replaced at 2 % elongation (HARD limit; 3 % no longer allowed)",
           "Oil level: lower strand immersed 20-25 mm static (was 6-12) so the lead axle stays immersed when it lifts on a climb; or a slinger (CWF option)"],
    verdict="PASS: with the corrected geometry the slack lasts to %.1f mm of bump at sag 17 (chain line horizontal) vs the 22 mm stop (margin %.2f); %.1f mm with a 3 mm primary shim. A 10 mm primary re-shim without a motor reset would give %.1f mm - NOT permitted by the procedure." % (z_tight(17, 0), z_tight(17, 0) / BUMP, z_tight(17, 3), z_tight(17, 10)))
J["weight_transfer"] = dict(basis="TE_truck*h/wb per axle (truck pitch) + drawbar body pitch (h - 0.55)/3.2; Stress Bot loco r2 #2; pivot height from build/model.py (centre plate Z1110, pivot seat Z1050-1110, GE100ES ~Z1080 -> 1.08 m)",
    fix="LOW TRACTION PIN per truck: traction height 0.65 m (Ø100 4140 pin from the body centre plate down through the transom to a GE100ES spherical bearing in a PL16 housing at Z650; centre plate flat-lined, vertical load only); margin 1.10 holds for h <= %.2f m" % h_for(1.10),
    cases=WTR, h_for_margin_110_fwd_m=h_for(1.10), h_for_margin_100_fwd_m=h_for(1.00), h_for_margin_110_rev_m=h_for(1.10, -1),
    PLUS1_pull_cap="Reverse: PLUS+1 caps reverse TE at the equal-torque adhesion cap %.1f kN (= max %.2f %% grade start with the full train); forward cap %.1f kN (> %.2f kN need)" % (WTR["L41_traction_pin_0p65"]["reverse"]["equal_torque_cap_kN"], WTR["L41_traction_pin_0p65"]["reverse"]["max_grade_start_pct"], WTR["L41_traction_pin_0p65"]["forward"]["equal_torque_cap_kN"], need2),
    rule="OPERATING RULE: no reverse start of the full train on a grade steeper than %.1f %% (propel moves on the level/yard only; the route runs forward)" % WTR["L41_traction_pin_0p65"]["reverse"]["max_grade_start_pct"],
    K2a="Max driver wheel at the equal-torque cap with transfer, RT1 axle set (sums to the loco mass with the pony): %.2f kN vs 26 (the L3-as-is static set is info only: %.2f)" % (K2A_WHEEL, max(ax_asis.values()) / 2))
# ---- L4.1 steering 7 (b): Ø1430 driver condemning limit (new Ø1450); pony Ø650 new / Ø630 worn, flange 35.0 mm worn (parent data)
_D_w = 1.430; _tread = 120.0; _dr = (D - _D_w) / 2 * 1000
_m_tread = math.pi * (D * 1000 - _dr) * _dr * _tread * 7.85e-6          # kg per driver wheel removed by wear
_dm_drv = 8 * _m_tread
_fac_drv = 1 - _dm_drv / (drv / 9.81 * 1000); _fac_need = 1 - _dm_drv / m_train
_fwd = WTR["L41_traction_pin_0p65"]["forward"]; _rev = WTR["L41_traction_pin_0p65"]["reverse"]
_W_w = (m_train - _dm_drv) * 9.81 / 1000; _rr = 0.0408 - 0.02
_rev_cap_w = _rev["equal_torque_cap_kN"] * _fac_drv; _g_rev_w = (_rev_cap_w / _W_w - _rr) * 100
_rpm_trip = 7.0 * 0.44704 / (math.pi * D) * 60
_bolt_top = 88.9 - 39.7 - 16.7                                             # ASCE 40: E = 1-9/16 in above base; 3/4 in track-bolt button head r ~16.7 (ASSUMED)
WEAR = dict(
    D_new_m=D, D_condemn_m=_D_w, radial_wear_mm=_dr, tread_mass_lost_per_wheel_kg=round(_m_tread, 1), loco_mass_worn_kg=round(loco_kg - _dm_drv, 0),
    speed=dict(vmax_high_idle_mph=round(J["speed"]["vmax_2nd_high_idle_mph"] * _D_w / D, 2), vmax_rated_mph=round(J["speed"]["vmax_2nd_at_stop_mph"] * _D_w / D, 2),
               hardware_mph=round(J["speed"]["vmax_2nd_stop_removed_mph"] * _D_w / D, 2),
               governor="42 cc stroke stop + sealed 2,600 rpm engine limit (L4.2): worn wheels only slow the loco (6 mph is a maximum)",
               trip="Overspeed relay set in AXLE RPM for the NEW Ø1450 wheel: %.1f rpm = 7.0 mph new, %.2f mph at Ø1430 (trips early = safe side); gap to the governed max %.2f mph" % (_rpm_trip, 7.0 * _D_w / D, 7.0 * _D_w / D - J["speed"]["vmax_2nd_high_idle_mph"] * _D_w / D),
               plus1="Enter the measured driver and pony diameters in PLUS+1 at each wheel gauging (monthly) - worst mismatch Ø630/650 pony vs Ø1450 drivers = 3.1 % apparent slip; slip threshold set >= 5 % above the calibrated ratio"),
    traction=dict(TE_350_kN=round(J["start"]["F350_kN"] * D / _D_w, 2), note="motor torque and chain pull unchanged (same motor torque, same 3:1); rail TE +1.4 % but adhesion-limited by PLUS+1",
                  fwd_margin_2pct_dry=round(_fwd["margin_2pct_dry_sanded"] * _fac_drv / _fac_need, 3), fwd_margin_2pct_wet=round(_fwd["margin_2pct_wet_unsanded"] * _fac_drv / _fac_need, 3),
                  rev_cap_kN=round(_rev_cap_w, 2), rev_max_grade_pct=round(_g_rev_w, 2), K2a_max_wheel_kN="<= %.2f (lighter wheels)" % K2A_WHEEL),
    brake=dict(loco_decel_ms2=round(0.69 * D / _D_w, 3), runin_effect_kN=round((0.69 * D / _D_w - 0.69) * loco_kg / 1000, 2), note="disc force fixed, rail force +1.4 %: loco 0.70 vs tender 0.671 m/s2 (TB-3.13d); run-in +0.2 kN (23.7 -> 23.9 vs 33.2) PASS"),
    clearance=dict(lower_outline="all truck/axle items drop %.0f mm: min 255 -> %.0f mm ATOR vs 150 (util %.2f) PASS" % (_dr, 255 - _dr, 150 / (255 - _dr)),
                   running_board="wheel top drops %.0f, body %.0f: gap 155 -> %.0f mm PASS" % (2 * _dr, _dr, 155 + _dr),
                   drawbar="loco drawbar pin drops <= %.0f mm vs tender: %.2f deg on the 800 c/c pinned bar PASS" % (_dr, math.degrees(math.atan(_dr / 800))),
                   chain="axle and motor bracket ride on the same truck: chain centre distance and case/seal envelope unchanged PASS",
                   flange_depth="Flange height grows 1:1 with tread wear: 25 new -> 35.0 at Ø1430 / pony Ø630 (parent data). ASCE 40 joint-bolt head top ~%.1f mm below TOR (ASSUMED 3/4 in track bolts): 35.0 mm NG (-%.1f mm). FLANGE-HEIGHT LIMIT 28 mm withdraw, re-profile <= 27 (L4.2 FINAL; L4.1 30.0 withdrawn) -> %.1f mm clear; frog/guard flangeway depth >= 36 mm required (owner track drawings)" % (_bolt_top, 35.0 - _bolt_top, _bolt_top - 30.0)),
    verdict="Ø1430 ADOPTED as the driver CONDEMNING DIAMETER (after re-profiling), with a separate FLANGE-HEIGHT limit 28 mm train-wide, re-profile <= 27 (L4.2 FINAL; L4.1 30.0 withdrawn; 35.0 mm worn flange is NOT permitted in service). Reverse full-train start rule tightened to <= %.2f %% to cover worn wheels." % (math.floor(_g_rev_w * 20) / 20),
    rev_rule_pct=math.floor(_g_rev_w * 20) / 20)
J["wheel_wear_L41"] = WEAR
J["weight_transfer"]["rule"] = "OPERATING RULE: no reverse start of the full train on a grade steeper than %.2f %% (covers worn Ø1430 drivers: %.2f %%; new wheels %.2f %%); propel moves on the level/yard only; the route runs forward" % (WEAR["rev_rule_pct"], _g_rev_w, _rev["max_grade_start_pct"])
# ---- L4.1 steering 7 (a): T04 release supply - no 4th dry-break
_V_rel = 4 * 0.10; _V_dmp_use = 0.18
def _acc_V0(dV, p0, p1, p2, n=1.4):   # gauge bar in, adiabatic
    a0, a1, a2 = p0 + 1.013, p1 + 1.013, p2 + 1.013
    return dV / ((a0 / a1) ** (1 / n) - (a0 / a2) ** (1 / n))
_V0_man = _acc_V0(2 * (_V_rel + _V_dmp_use), 13.5, 15.0, 22.0)
_A_or = lambda d: math.pi / 4 * (d / 1000) ** 2
_Q = lambda d, dp: 0.62 * _A_or(d) * math.sqrt(2 * dp * 1e5 / 870) * 1000          # L/s
_d_ch = 2.4; _t_delay = _V_dmp_use / _Q(_d_ch, 17.5); _t_rise = _V_rel / _Q(_d_ch, 10.0); _t_release = (_V_rel + _V_dmp_use) / _Q(_d_ch, 8.0)
J["T04_release_L41"] = dict(
    principle="NO 4th dry-break, all on the loco: release pressure is taken from the loco's own hydrostatic loop. Loss of loop or charge pressure APPLIES the T04 (purely hydraulic, no electronics needed); the accumulator serves ONLY the guarded manual release.",
    superseded_by="L42.T04_charge_feed (L4.2: loop shuttle DELETED, T04 fed from the H1 charge circuit M3 port)", circuit=["1 [L4.1, SUPERSEDED] LP-select shuttle across loop A/B (hot-oil shuttle type, spring-centred, body >= 450 bar, 10-size cartridge or equal) -> picks the low side = charge pressure (22-28 bar running)",
             "2 Pressure filter 10 um with bypass indicator (loop oil into the brake circuit)",
             "3 3-way pressure-REDUCING/RELIEVING cartridge, set 20 bar (range 7-35, inlet >= 450 bar rated); with the inlet below setting it is fully open, so the brake line FOLLOWS a falling charge pressure -> brakes apply on loss of loop/charge",
             "4 3/2 solenoid poppet, 24 V DC, NORMALLY VENTED (de-energized = brake port to case drain = APPLY); PLUS+1 energizes to release",
             "5 Fixed choke Ø%.1f mm (ASSUMED until Poclain gives the T04 release volume) in the common brake line + 1.0 L diaphragm DAMPING accumulator (pre-charge 13.5 bar) on the brake side: every apply path (solenoid vent or supply loss) passes the choke -> delay %.1f s, rise %.1f s (required >= 1.0 / >= 2.0 s for the run-in result); release in ~%.1f s" % (_d_ch, _t_delay, _t_rise, _t_release),
             "6 Brake-line ball shuttle (high select) feeding the 4 T04 ports from EITHER the service line (5) OR the manual-release line (7); the unused inlet is vented",
             "7 MANUAL RELEASE branch: check valve from the reducing-valve inlet -> %.1f L bladder accumulator (210 bar class, pre-charge 13.5 bar, safety block with isolation, bleed and gauge) + hand pump 12 cm3/stroke with check (dead-loco recharge) -> guarded 3/2 manual valve (normally vented, padlock, limit switch to PLUS+1 = traction inhibit + BP stays vented) -> shuttle 6" % min(v for v in (1.0, 2.5, 4.0, 6.0, 10.0) if v >= _V0_man),
             "8 Charge pressure switch, 17 bar falling, hard-wired with the T04-line switch: vents the BP FIRST (train air brakes lead), then the choked T04 follows",
             "9 Last resort: T04 mechanical release screws (M12, per Poclain) for rescue towing"],
    sizing=dict(T04_release_volume_L_ASSUMED=_V_rel, T04_full_release_bar_ASSUMED=15.0, T04_max_bar=30.0, PRV_set_bar=20.0, charge_bar="22-28",
                manual_acc_V0_L_required=round(_V0_man, 2), manual_acc_V0_L_spec=min(v for v in (1.0, 2.5, 4.0, 6.0, 10.0) if v >= _V0_man), manual_releases=2,
                damping_acc_L=1.0, choke_mm=_d_ch, delay_s=round(_t_delay, 2), rise_s=round(_t_rise, 2), release_s=round(_t_release, 2)),
    failure_modes=["Engine stall / loop loss at speed: charge decays -> switch vents BP -> T04 applies through the choke (dynamic use logged; inspect per Poclain after each; 10 dynamic uses max)",
                   "24 V loss: solenoid vents -> choked apply; BP vents (ASCO de-energize-to-vent)", "Hose burst on the brake line: brake applies (spring)",
                   "Manual valve left open: limit switch inhibits traction and holds the BP vented; accumulator volume only lasts 2 releases"],
    supersedes="L4.1 loco_valves 0.75 L accumulator ON the brake line (it held release ~30 s after a stall) - REMOVED to meet 'loss of loop/charge applies the brake'",
    held="Poclain: T04 release volume, full-release pressure, choke size (vendor ask HELD - no contact)")
# ======================= REV L4.2 (Grokky, 28 Oct 2026): Stress Bot loco round 3 rulings (parent, no owner decisions) =======================
L42 = {}
# --- 5. traction pin Ø120 + centre-plate friction in the start margin
_Fy41 = 655.0; _lev = 0.46; _d_pin = 0.120; _Zp = math.pi * _d_pin ** 3 / 32; _Ap = math.pi * _d_pin ** 2 / 4
_m_truck_A101, _m_truck_est = 4900.0, 3156.0
_N_cp = (loco_kg - 2 * _m_truck_est) * g / 2 / 1000          # body vertical per centre plate (heavier body = more friction, conservative)
_H_CP = 1.11
_E = 210e9; _I_pin = math.pi * _d_pin ** 4 / 64
_k_pin = 0.5 * 3 * _E * _I_pin / _lev ** 3 / 1e6        # MN/m: cantilever pin, halved for bearing/housing/transom compliance (conservative = more plate share)
_k_pad = 3.0                                                # MN/m: laminated elastomer centre pad longitudinal shear stiffness (SPEC <= 3.0; e.g. 2 x 15 mm layers, G 0.9 MPa, Ø300) - ASSUMED, PE/supplier verify
SHARE_PAD = _k_pad / (_k_pad + _k_pin)
def _h_eff(TE, mu_cp, share=None):
    share = SHARE_PAD if share is None else share
    Ft = TE / 2; Fc = min(mu_cp * _N_cp, share * Ft)
    return (Fc * _H_CP + (Ft - Fc) * H_T) / Ft
def _cap_f(d, mu_cp, mu_=0.25, fac=1.0):
    TE = 30.0
    for _ in range(80): TE = 4 * mu_ * fac * min(ax_tr(TE, d, _h_eff(TE, mu_cp)).values())
    return TE
def _marg(d, mu_cp, gr=2.0, fac=1.0, fneed=1.0):
    n_ = (0.0208 + gr / 100) * W * fneed; a = ax_tr(n_, d, _h_eff(n_, mu_cp)); return min(a.values()) * fac / n_, min(a, key=a.get), a
_pin = {}
for lab, F in (("service_HPRV_x1.3 (0.6Fy)", 1.3 * F400 / 2), ("3g_truck_A101_4900 (exceptional, Fy)", 3 * g * _m_truck_A101 / 1000), ("3g_truck_est_3156 (Fy)", 3 * g * _m_truck_est / 1000),
               ("drawgear_ult_200kN_share (Fy)", 200 / (loco_kg / 1000) * _m_truck_A101 / 1000)):
    sg = F * _lev / _Zp / 1000; lim = 0.6 * _Fy41 if "0.6Fy" in lab else _Fy41
    _pin[lab] = dict(F_kN=round(F, 1), sigma_MPa=round(sg), limit_MPa=round(lim), util=round(sg / lim, 2), shear_MPa=round(F / _Ap / 1000 * 4 / 3, 1))
_CP = {}
def _marg_r(d, mu_cp, share):
    n_ = (0.0208 + 0.02) * W; a = ax_tr(n_, d, _h_eff(n_, mu_cp, share)); return min(a.values()) / n_
for mu_cp in (0.0, 0.05, 0.08, 0.10, 0.15):
    mf, axf, _ = _marg(1, mu_cp); mr, axr, _ = _marg(-1, mu_cp)
    _CP["mu_%.2f" % mu_cp] = dict(rigid_steel_plate_fwd_margin=round(_marg_r(1, mu_cp, 1.0), 3), rigid_steel_plate_rev_margin=round(_marg_r(-1, mu_cp, 1.0), 3), h_eff_rigid_plate=round(_h_eff(need2, mu_cp, 1.0), 3),
                                  h_eff_fwd_at_need=round(_h_eff(need2, mu_cp), 3), fwd_margin_2pct=round(mf, 3), fwd_lightest=axf, rev_margin_2pct=round(mr, 3), rev_lightest=axr,
                                  fwd_cap_kN=round(_cap_f(1, mu_cp), 2), rev_cap_kN=round(_cap_f(-1, mu_cp), 2))
MU_CP = 0.08     # SPEC: PTFE-faced yaw slide on the elastomer pad, mu <= 0.08 dry (ASSUMED until the supplier confirms)
L42["traction_pin"] = dict(d_mm=120, material="4140 Q&T (Fy 655)", lever_m_ASSUMED=_lev, cases=_pin, bearing="GE120ES-class spherical plain bearing, RADIAL load (re-selected from the GE100ES: the L4.1 pin carries longitudinal load only; T1-f 'vertical 273 kN' superseded); static radial rating >= 2 x 144 kN (AWAIT SKF data)",
    housing="PL20 housing ring welded to the transom web, 2 x 10 fillets all round (PE verify); pin engagement >= 60 mm over the full centre-plate shim range (0-12 mm)",
    clearance="pin Ø120 vs motor brackets 25-55 mm -> 15-45 mm after the +10 mm radius; vs MS05 60-80 mm (+22 at 2 % chain stretch) -> 50-70 / 28-48 mm: PASS (model.py now has the pin)",
    centre_plate=dict(design="LAMINATED ELASTOMER centre pad (longitudinal shear stiffness <= 3.0 MN/m) with a PTFE-faced yaw slide (mu <= 0.08) on the flat-lined plate: the pad shears instead of sticking, so the stiff Ø120 pin carries the traction at 0.65 m; a rigid steel plate would put mu N at 1.11 m (sweep: rigid-plate margins)",
        k_pin_MN_m=round(_k_pin, 1), k_pad_MN_m=_k_pad, pad_share=round(SHARE_PAD, 3), N_kN_per_plate=round(_N_cp, 1), h_plate_m=_H_CP, h_pin_m=H_T, liner_mu_spec=MU_CP, sweep=_CP))
# --- 6/8. sanders on BOTH trucks ahead of the lead axle each direction (forward F1 + R1, reverse F2 + R2); carry-over mu 0.20 on the trailing axles (ASSUMED)
_mu_s, _mu_co, _mu_wet = 0.25, 0.20, 0.15
def _marg_sand(d, gr, mu_cp=MU_CP, fac=1.0, wet=True):
    sand = ("F1", "R1") if d > 0 else ("F2", "R2")
    n_ = (0.0208 + gr / 100) * W * (1.0 if fac == 1.0 else _fac_need); a = ax_tr(n_, d, _h_eff(n_, mu_cp))
    return 4 * min((_mu_s if k in sand else (_mu_co if wet else _mu_s)) * v * fac for k, v in a.items()) / n_
def _g_for(d, m=1.10, fac=1.0, wet=True):
    lo, hi = -1.0, 4.0
    for _ in range(50):
        mid = (lo + hi) / 2; lo, hi = (mid, hi) if _marg_sand(d, mid, fac=fac, wet=wet) >= m else (lo, mid)
    return lo
_SND = {}
for dn, d in (("forward", 1), ("reverse", -1)):
    for cond, wet in (("dry_or_sanded_all", False), ("DEGRADED_wet_trailing_nozzles_failed_carryover", True)):
        _SND[f"{dn}_{cond}"] = dict(margin_2pct_new=round(_marg_sand(d, 2.0, wet=wet), 3), margin_2pct_worn=round(_marg_sand(d, 2.0, fac=_fac_drv, wet=wet), 3),
                                    grade_m110_new=round(_g_for(d, wet=wet), 2), grade_m110_worn=round(_g_for(d, fac=_fac_drv, wet=wet), 2), grade_m100_new=round(_g_for(d, 1.0, wet=wet), 2))
_g_rev = min(_SND["reverse_dry_or_sanded_all"]["grade_m110_new"], _SND["reverse_dry_or_sanded_all"]["grade_m110_worn"])
_rr_pct = need2 / W * 100 - 2.0
_g_rev_cap = (28.9 / 1.10) / W * 100 - _rr_pct    # L4.2: reverse pull cap 28.9 kN of record with the same 1.10 margin
_g_rev_adh = _g_rev; _g_rev = min(_g_rev, _g_rev_cap)
REV_RULE = math.floor(_g_rev * 20) / 20
_fwd_ok = min(_SND["forward_dry_or_sanded_all"]["margin_2pct_new"], _SND["forward_dry_or_sanded_all"]["margin_2pct_worn"])
L42["sanding"] = dict(layout="Sanders on BOTH powered trucks: nozzles ahead of the LEAD axle of EACH truck in EACH direction (forward F1 + R1, reverse F2 + R2) so the lightest axle (R1 forward, F2 reverse) is always sanded directly, PLUS a nozzle ahead of each trailing axle (so no axle relies on carry-over); 8 nozzles per truck, 2 boxes per truck",
    proof="Sand-box level switch per box + flow proof (air-pressure switch downstream of each sand valve, or a sand-flow sensor): a failed proof inhibits starts on grades >= 1 % and alarms",
    rule="Pre-sand on every start with the grade >= 1 % or a wet rail; sand is MANDATORY on wet rail",
    mu=dict(sanded=_mu_s, carry_over_ASSUMED=_mu_co, wet_unsanded=_mu_wet, centre_plate_liner=MU_CP), cases=_SND, fwd_min_margin_2pct=round(_fwd_ok, 3),
    reverse_2pct_margin=_SND["reverse_dry_or_sanded_all"]["margin_2pct_new"], reverse_rule_pct=REV_RULE, reverse_grade_adhesion_110_pct=round(_g_rev_adh, 2), reverse_grade_TE_cap_28p9_110_pct=round(_g_rev_cap, 2), reverse_TE_cap_kN=28.9,
    reverse_verdict="Reverse 2 %% full-train start with sand on both trucks: margin %.3f (< 1.10, NOT met - the lightest axle F2 is already sanded, so sand cannot add adhesion beyond mu 0.25). Grade for 1.10: %.2f %% new / %.2f %% worn (dry or sanded), %.2f / %.2f degraded carry-over -> REVERSE FULL-TRAIN START LIMIT %.2f %% (all files)" % (
        _SND["reverse_dry_or_sanded_all"]["margin_2pct_new"], _SND["reverse_dry_or_sanded_all"]["grade_m110_new"], _SND["reverse_dry_or_sanded_all"]["grade_m110_worn"], _SND["reverse_DEGRADED_wet_trailing_nozzles_failed_carryover"]["grade_m110_new"], _SND["reverse_DEGRADED_wet_trailing_nozzles_failed_carryover"]["grade_m110_worn"], REV_RULE))
def _wmax(TE, d): return max(ax_tr(TE, d, _h_eff(TE, MU_CP)).values()) / 2
def _te_lim(d, wl=26.0):
    lo, hi = 20.0, 45.0
    for _ in range(50):
        mid = (lo + hi) / 2; lo, hi = (mid, hi) if _wmax(mid, d) <= wl else (lo, mid)
    return lo
_capf = _cap_f(1, MU_CP); _capr = _cap_f(-1, MU_CP)
TE_LIM_F = math.floor(min(_te_lim(1, 25.9), _capf) * 10) / 10   # L4.2: limit set for <= 25.9 kN (0.1 kN reserve below the 26 kN K2-a)
TE_LIM_R = min(28.9, math.floor(min(_te_lim(-1), _capr) * 10) / 10)   # L4.2: reverse pull cap 28.9 kN of record (supersedes 29.4 everywhere)
L42["K2a"] = dict(fwd_cap_kN=round(_capf, 2), rev_cap_kN=round(_capr, 2), wheel_at_fwd_cap_kN=round(_wmax(_capf, 1), 2), wheel_at_rev_cap_kN=round(_wmax(TE_LIM_R, -1), 2), fwd_TE_command_limit_kN=TE_LIM_F, rev_TE_command_limit_kN=TE_LIM_R, wheel_at_rev_limit_kN=round(_wmax(TE_LIM_R, -1), 2),
    wheel_at_limit_kN=round(_wmax(TE_LIM_F, 1), 2), limit_over_need=round(TE_LIM_F / need2, 3),
    rule="PLUS+1 caps the forward TE command at %.1f kN (%.2f x the 2 %% need) so no driver wheel exceeds 26 kN (K2-a); reverse pull is capped at %.1f kN of record (adhesion cap %.1f; wheel %.2f kN)" % (TE_LIM_F, TE_LIM_F / need2, TE_LIM_R, _capr, _wmax(TE_LIM_R, -1)))
J["weight_transfer"]["K2a"] = "L4.2: max driver wheel %.2f kN at the forward TE command limit %.1f kN (PLUS+1; %.2f x need) and %.2f kN at the reverse cap %.1f kN, vs 26 kN (centre-plate pad included; uncapped forward adhesion cap %.1f kN would give %.2f)" % (_wmax(TE_LIM_F, 1), TE_LIM_F, TE_LIM_F / need2, _wmax(TE_LIM_R, -1), _capr, _capf, _wmax(_capf, 1))
J["weight_transfer"]["rule"] = "OPERATING RULE (L4.2): no reverse start of the full train on a grade steeper than %.2f %% (1.10 margin with centre-plate friction mu %.2f, sand on both trucks, new and worn Ø1430 drivers; measured wheel diameters entered in PLUS+1 = maintenance HOLD POINT); propel moves on the level/yard only; the route runs forward" % (REV_RULE, MU_CP)
L42["sanding"]["reverse_verdict"] = L42["sanding"]["reverse_verdict"].replace("-> REVERSE FULL-TRAIN START LIMIT", "; the reverse pull cap of record 28.9 kN with the same 1.10 gives %.2f %% (GOVERNS) -> REVERSE FULL-TRAIN START LIMIT" % _g_rev_cap)
WEAR["rev_rule_pct"] = REV_RULE
# --- hill-hold (destroke-and-recover cannot roll back)
_p_hold = lambda gr: (gr / 100) * W / F350 * 350
L42["hill_hold"] = dict(rule="Friction brakes (loco air calipers + train air) stay APPLIED on a start until loop dp >= p_hold(grade) + 20 bar and TE is established; then released. During any slip destroke PLUS+1 never reduces dp below p_hold for the measured grade (inclinometer); any reverse motion (pony quadrature direction) -> brakes apply + alarm",
    p_hold_2pct_bar=round(_p_hold(2.0)), p_hold_1pct_bar=round(_p_hold(1.0)), hold_force_2pct_kN=round(0.02 * W, 2),
    slip_sequence="slip detected -> sand -> destroke to v_ref x 1.05 but dp >= p_hold -> recover at 0.5 kN/s; if slip persists at p_hold for 3 s -> brakes apply, traction off (no roll-back)")
# --- 7. pony target wheel + speed agreement
_hz = lambda mph, Dm, n: mph * 0.44704 / (math.pi * Dm) * n
_teeth = 96
L42["pony_reference"] = dict(target_wheel_teeth=_teeth, sensors="2 Hall sensors in quadrature (direction + 4 edges per tooth)", Hz_0p5mph_new=round(_hz(0.5, 0.650, _teeth), 1), Hz_0p5mph_worn=round(_hz(0.5, 0.630, _teeth), 1),
    pulses_per_100ms_at_0p5mph=round(_hz(0.5, 0.650, _teeth) * 0.1, 2), edges_per_100ms_quadrature=round(_hz(0.5, 0.650, _teeth) * 0.4, 1), teeth_min_for_10Hz=math.ceil(10 / _hz(0.5, 0.650, 1)),
    old="15-tooth ring: 1.64 Hz at 0.5 mph (0.61 s between pulses) vs a 100 ms filter - REPLACED",
    slip_logic="slip = (axle - v_ref) > max(0.5 mph, 10 %) AND axle accel > 0.5 m/s2; v_ref = max(pony, slowest axle, 0) within the pony plausibility window; period (edge-time) measurement, 100 ms filter",
    agreement="Pony / axle speed agreement: |pony - median(axles)| > 10 % (diameters calibrated) for > 2 s above 1 mph -> PONY FAULT: reference = slowest axle, 1st gear, 3 mph limit, alarm; pony at 0 with axles > 1 mph = fault (not slip)",
    overspeed="PNOZ s30 overspeed stays INDEPENDENT (its own 2 sensors on its own pony ring + an axle channel, 7 mph trip); PLUS+1 compares the s30 speed with its own and alarms a discrepancy > 10 %")
# --- 3. hard 2,600 rpm engine limit, 42 cc stop, recheck at no-load eta_v 0.99
_ev0 = 0.99
_Qnl = n_hi * Vp_stop / 1000 * _ev0
_spin2_nl = _Qnl * _ev0 / (Vg2 / 1000); _spin1_nl = _Qnl * _ev0 / (Vg1 / 1000)
_v2nd_min = 1.5     # s30 hard-wired speed-threshold contact feeds the 2nd-gear coil only >= 1.5 mph ground speed
_spin2_rolling = _spin2_nl - 3 * motor_rpm(_v2nd_min)
L42["high_idle"] = dict(engine_limit_rpm=n_hi, limit="HARD, tamper-sealed 2,600 rpm engine speed limit (Kubota ECU max-speed setting + sealed governor stop; AIE to set and seal - data HELD)", stop_cc=Vp_stop,
    vmax_loaded_mph=round(v_of(Q_stop(Vp_stop), Vg2), 2), vmax_noload_mph=round(_Qnl * _ev0 / (4 * Vg2 / 1000) / i_ch / 60 * math.pi * D / 0.44704, 2),
    spin_2nd_standstill_noload_rpm=round(_spin2_nl), util_2nd_standstill=round(_spin2_nl / 430, 3), spin_1st_noload_rpm=round(_spin1_nl), util_1st=round(_spin1_nl / 370, 3),
    spin_2nd_rolling_rpm=round(_spin2_rolling), util_2nd_rolling=round(_spin2_rolling / 430, 3),
    interlock="L4.2: MS05 2-speed valves re-wired FAIL-TO-1st (de-energized = 468 cc); the 2nd-gear coil is fed THROUGH a hard-wired PNOZ s30 speed-threshold contact (closed only >= 1.5 mph ground speed) in series with PLUS+1 (2nd commanded >= 3.0 mph with pony/axle agreement). A single axle can spin in 2nd only while the other 3 roll at >= 1.5 mph -> %d rpm vs 430 (util %.2f); at standstill or on any coil/wire/24 V failure the motors are in 1st -> %d rpm vs 370 (util %.2f). The no-interlock standstill-in-2nd figure (%d rpm, util %.2f) needs PLUS+1 AND the s30 contact to fail together. Per-motor electronic overspeed destroke at 420 rpm (PLUS+1) is a further layer." % (_spin2_rolling, _spin2_rolling / 430, _spin1_nl, _spin1_nl / 370, _spin2_nl, _spin2_nl / 430),
    verdict="6 mph kept (%.2f mph loaded at 2,600 / 42 cc; %.2f mph no-load light engine, below the 7 mph trip)" % (v_of(Q_stop(Vp_stop), Vg2), _Qnl * _ev0 / (4 * Vg2 / 1000) / i_ch / 60 * math.pi * D / 0.44704))
J["speed"]["stop_rule"] = "L4.2: stroke stop 42 cc sealed + HARD tamper-sealed 2,600 rpm engine limit (no high idle above rated): %.2f mph loaded in 2nd; no-load %.2f mph (eta_v 0.99); 7 mph trip independent" % (L42["high_idle"]["vmax_loaded_mph"], L42["high_idle"]["vmax_noload_mph"])
J["speed"]["spin_note"] = L42["high_idle"]["interlock"]
# --- 4. flange limit 28 mm withdraw (re-profile <= 27) + 2 mm vertical rail-head wear limit at joints
_bt = 88.9 - 39.7 - 16.7
L42["flange"] = dict(withdraw_mm=28.0, reprofile_to_mm=27.0, rail_head_vertical_wear_limit_at_joints_mm=2.0, bolt_head_top_below_TOR_new_mm=round(_bt, 1),
    clear_at_limits_mm=round(_bt - 2.0 - 28.0, 1), clear_new_rail_mm=round(_bt - 28.0, 1), applies="TRAIN-WIDE: loco drivers, pony, tender and coach wheels (Rail Bot track basis)",
    replaces="L4.1 30.0 mm flange-height limit (0.5 mm clear at 2 mm joint wear, -3.5 at 6 mm) - withdrawn", frog_flangeway_min_mm=36.0)
WEAR["clearance"]["flange_depth"] = "L4.2: flange height WITHDRAW limit 28 mm train-wide (re-profile to <= 27 mm) + 2 mm vertical rail-head wear limit at joints: ASCE 40 joint-bolt head top ~%.1f mm below TOR new -> %.1f mm clear at both limits; frog/guard flangeway depth >= 36 mm (owner track drawings)" % (_bt, _bt - 30.0)
WEAR["verdict"] = "Ø1430 ADOPTED as the driver CONDEMNING DIAMETER (after re-profiling); FLANGE: withdraw at 28 mm, re-profile to <= 27 mm (train-wide, L4.2; replaces the L4.1 30 mm limit); reverse full-train start limit %.2f %%." % REV_RULE
# --- 1. descents: float mode + friction brakes sized for the full 2 % descent with the loaded train
_coach_brk = 3 * 0.12 * 8040 * g / 1000 + 0.12 * 7000 * g / 1000
_F_loco_br = 0.69 * loco_kg / 1000; _F_ten_br = 5.845   # tender full brake force (calipers unchanged since TB-3.11; 0.671 m/s2 at TB-3.13d)
_F_full = _F_loco_br + _F_ten_br + _coach_brk
_F_desc = m_train * g * 0.02 / 1000; _F_desc_net = m_train * g * (0.02 - 0.005) / 1000
_v6 = 6 * 0.44704; _P_desc = _F_desc_net * _v6
_shares = dict(loco=_F_loco_br / _F_full, tender=_F_ten_br / _F_full, coaches=_coach_brk / _F_full)
_m_disc = dict(loco=4 * math.pi / 4 * 0.340 ** 2 * 0.025 * 7200, tender=4 * math.pi / 4 * 0.300 ** 2 * 0.020 * 7200, coaches=16 * math.pi / 4 * 0.300 ** 2 * 0.020 * 7200)
_cp = 460.0; _dT_lim = 250.0
_Lmax = {k: _m_disc[k] * _cp * _dT_lim / (_P_desc * 1000 * _shares[k]) * _v6 for k in _m_disc}
_q_bypass_Lmin = 4 * Vg2 * motor_rpm(6.0) / 1000; _dp_byp = 5.0
_P_float = _q_bypass_Lmin / 60000 * _dp_byp * 1e5 / 1000 + 2.5
L42["descent"] = dict(mode="FLOAT MODE replaces 'pump at neutral': brake handle out of RUN -> PLUS+1 ramps the swash to zero over >= 3 s and the pilot-operated 2/2 LOOP BYPASS (cross-port) valve opens as the ramp starts (<= 0.5 s), motors in 2nd; if the bypass fails closed the >= 3 s ramp bounds the retarding force (run-in case 'bypass failed'): the motors free-wheel and circulate oil through the bypass, NO hydrostatic retarding; charge pump keeps make-up + T04 released; float is left only with the train stopped or by a ramped re-engage (swash matched to speed, then the bypass closes)",
    bypass_valve="pilot-operated 2/2 cartridge, >= 420 bar working (L4.2 pressure revision), >= 200 L/min at dp <= 5 bar (1st-gear float after a 24 V loss = 2 x 99 L/min), NORMALLY OPEN = FAIL-TO-FLOAT (24 V loss, PLUS+1 fault or coil failure -> float; the BP vents and the friction brakes stop/hold the train), held closed by a 24 V solenoid in RUN; spool-position proof switch (traction enable needs 'closed'); 2 anti-cavitation make-up checks",
    descent_force_2pct_kN=round(_F_desc, 2), descent_force_net_rolling_kN=round(_F_desc_net, 2), friction_full_kN=round(_F_full, 2), friction_service_kN=round(0.7 * _F_full, 2),
    hold_util_service=round(_F_desc / (0.7 * _F_full), 2), shares={k: round(v, 3) for k, v in _shares.items()}, P_descent_6mph_kW=round(_P_desc, 1),
    disc_mass_kg={k: round(v, 1) for k, v in _m_disc.items()}, max_continuous_descent_m_at_dT250_adiabatic={k: round(v) for k, v in _Lmax.items()},
    governing_descent_m=round(min(_Lmax.values())), cooler=dict(float_heat_kW=round(_P_float, 1), cooler_kW=14.0, util=round(_P_float / 14.0, 2), note="bypass flow %.0f L/min x %.0f bar + 2.5 kW charge/idle (ASSUMED); the 32 kW HPRV lock case no longer exists" % (_q_bypass_Lmin, _dp_byp)),
    verdict="Friction brakes hold the full 2 %% descent of the loaded train at %.0f %% of service force; adiabatic disc limit dT 250 K allows %.0f m of continuous 2 %% descent at 6 mph (governing: %s). Track is designed LEVEL (Layout F) - if the owner adopts any grade, its length must be <= this or a cool-down stop rule applies." % (100 * _F_desc / (0.7 * _F_full), min(_Lmax.values()), min(_Lmax, key=_Lmax.get)))
# --- 2/9. T04: per-port Ø1.2 orifices, hard lines / 4SH, 2-channel vent switch; separate T04 release target
_d_po = 1.2
_A_eq = lambda: 1 / math.sqrt(1 / _A_or(_d_ch) ** 2 + 1 / (4 * _A_or(_d_po)) ** 2)
_Qeq = lambda dp: 0.62 * _A_eq() * math.sqrt(2 * dp * 1e5 / 870) * 1000
def _t_drain(V0=0.10, p0=15.0, d=_d_po, frac=0.9, dt=1e-3):   # spring-brake piston: p ~ V (linear), single motor port orifice to atmosphere
    V = V0; t = 0.0
    while V > V0 * (1 - frac):
        p = p0 * V / V0; V -= _Q(d, max(p, 0.05)) * dt; t += dt
    return t
_t_burst = _t_drain()
_t_delay42 = _V_dmp_use / _Q(_d_ch, 17.5); _t_rise42 = _V_rel / _Qeq(10.0); _t_rel42 = _V_dmp_use / _Q(_d_ch, 8.0) + _V_rel / _Qeq(8.0)
T04_REL_TARGET = 8.0
L42["T04"] = dict(port_orifice_mm=_d_po, lines="hard tube (P-clipped) or EN 856 4SH hose DOWNSTREAM of the choke to every T04 port", vent_switch="BP-vent charge/T04 pressure switch 2-CHANNEL (2 switches, either vents the BP; discrepancy alarm)",
    normal=dict(delay_s=round(_t_delay42, 2), rise_s=round(_t_rise42, 2), release_s=round(_t_rel42, 2)), burst_downstream=dict(delay_s=0.0, rise_90pct_s=round(_t_burst, 2), note="line burst between the choke and a motor: each motor drains through its own Ø1.2 port orifice (spring piston p ~ V, 15 bar full release ASSUMED)"),
    release_target_s=T04_REL_TARGET, release_met=_t_rel42 <= T04_REL_TARGET,
    release_target_basis="SEPARATE T04 release target <= %.0f s: the T04 is choked on purpose (slow APPLY protects the 33.2 kN run-in limit), and the same choke/orifices slow the release; traction enable waits for T04-line release proof (>= 15 bar) so a slow release only delays the start, it never drags. The AIR brake release stays <= 4 s." % T04_REL_TARGET)
# --- L4.2 pressure revision (b): T04 release fed from the H1 CHARGE circuit (M3 charge gauge port); LP-select loop shuttle DELETED
_p_ch_nom, _p_ch_min = 24.0, 21.0   # H1P053 charge pressure running (22-28 band, nominal 24) / low-idle minimum ASSUMED (AWAIT Danfoss charge relief setting)
def _t_rel_sup(p_sup):   # same choke/orifice model as L42 T04 'normal' (release dp 8 bar at a 20 bar supply), dp scales with the supply above the 12 bar mean back-pressure
    dp = max(min(p_sup, 20.0) - 12.0, 0.1)
    return _V_dmp_use / _Q(_d_ch, dp) + _V_rel / _Qeq(dp)
_V0_man42 = _acc_V0(2 * (_V_rel + _V_dmp_use), 13.5, 15.0, 22.0)
L42["T04_charge_feed"] = dict(
    circuit=["1 Tap from the H1P053 CHARGE gauge port M3 (charge pressure after the charge filter) - no loop-pressure part in the T04 release circuit",
             "2 Check valve + 10 um pressure filter", "3 CDK 3-way reducing/relieving cartridge set 20 bar (inlet = charge, <= 35 bar)",
             "4 3/2 solenoid poppet 24 V normally VENTED (de-energized = APPLY)", "5 Choke Ø2.4 + 1.0 L damping accumulator, then hard lines / 4SH to each T04 port with the Ø1.2 orifice (unchanged)",
             "6 Manual release: check from the charge tap -> 6.0 L bladder accumulator (pre-charge 13.5 bar) + hand pump 12 cm3/stroke -> guarded valve -> brake-line high-select shuttle (low pressure, <= 35 bar - not a loop part)",
             "DELETED: the LP-select shuttle across loop A/B (Source Bot: none rated above 350 bar)"],
    charge_bar=dict(nominal=_p_ch_nom, min_low_idle_ASSUMED=_p_ch_min, band="22-28 running"),
    T04_full_release_bar_ASSUMED=15.0, supply_bar_nom=min(_p_ch_nom, 20.0), pressure_margin=round(min(_p_ch_min, 20.0) / 15.0, 2),
    release_s_nominal=round(_t_rel_sup(_p_ch_nom), 2), release_s_low_idle=round(_t_rel_sup(_p_ch_min), 2), release_target_s=T04_REL_TARGET, release_margin=round(T04_REL_TARGET / _t_rel_sup(_p_ch_min), 2),
    note_4s="The T04 release is choked on purpose (slow apply = run-in limit); the separate T04 target is <= 8 s (ruling 9). The AIR brake release is the <= 4 s item (2.36 s worst). If a <= 4 s T04 release were required, a check valve in parallel with the Ø2.4 choke (free flow toward the T04, choked toward the vent) gives about %.1f s with the apply timing unchanged - NOT adopted" % (_V_rel / (4 * _Q(_d_po, 8.0)) + 0.1),
    tow=dict(manual_acc_V0_required_L=round(_V0_man42, 2), manual_acc_V0_spec_L=6.0, releases=2, charged_from="charge pressure via the check (holds the last running charge, >= 22 bar); dead loco: hand pump to 22-28 bar",
             hand_pump_strokes_full_recharge=round(2 * (_V_rel + _V_dmp_use) * 1000 / 12), result="PASS - 2 manual releases from the 6.0 L accumulator after an engine stop; unlimited with the hand pump (%d strokes per 2 releases)" % round(2 * (_V_rel + _V_dmp_use) * 1000 / 12)),
    engine_off="Engine off = no charge pressure = T04 APPLIED through the choke (fail-safe unchanged); the BP vents first via the 2-channel switch")
L42["loop_ball_valve_KHB3K"] = "HYDAC KHB3K DN25 is rated 310 bar: NOT allowed on the loop. The tow valve across A-B is a HYDAC KHB3K DN06 class ball valve (500 bar) - sized below for the 2 mph tow flow; lockable, limit switch to PLUS+1. No other ball valve is on a loop-pressure line (the brake-air trunk ball valve is air, <= 10 bar)."
import math as _m
_v_tow = 2 * 0.44704; _n_motor = _v_tow / (_m.pi * 1.430) * 60 * 3.0          # rpm at 2 mph, worn Ø1430, 3:1 chain
_Q1 = 4 * _n_motor * 468 / 1000; _Q2 = 4 * _n_motor * 234 / 1000             # L/min through the A-B tow valve, 1st / 2nd
_d06 = 6.0e-3; _A06 = _m.pi * _d06 ** 2 / 4; _K06 = 1.5                        # DN06 bore 6 mm, K 1.5 incl. ports (ASSUMED until the HYDAC curve is read)
_dp = lambda Q: _K06 * 870 * (Q / 60000 / _A06) ** 2 / 2 / 1e5               # bar
_drag = lambda Q, V: 4 * (_dp(Q) * 1e5 * V * 1e-6 / (2 * _m.pi)) * 3.0 / 0.715 / 1000   # kN at the rail
L42["tow_valve_DN06"] = dict(valve="HYDAC KHB3K DN06 class, 500 bar (DN25 310 bar NOT allowed on the loop)", rating_bar=500, strength_basis_bar=430, util_430=round(430 / 500, 3),
    tow_rule="tow <= 2 mph, MS05 in 1st (fail-to-1st, de-energized)", motor_rpm_2mph=round(_n_motor, 1), Q_1st_Lmin=round(_Q1, 1), Q_2nd_Lmin=round(_Q2, 1),
    dp_1st_bar=round(_dp(_Q1), 1), dp_2nd_bar=round(_dp(_Q2), 1), drag_1st_kN=round(_drag(_Q1, 468), 2), heat_1st_kW=round(_dp(_Q1) * _Q1 / 600, 2),
    dp_limit_bar=30.0, note="Δp kept <= 30 bar so the loop stays far below charge-relief / HPRV and the motors do not cavitate; bore 6 mm and K 1.5 ASSUMED - confirm from the HYDAC DN06 Δp curve (vendor batch, no contact). If the MS05 is declutched/freewheeled per Poclain the flow is ~0.")
L42["loop_hose"] = dict(hose="Manuli DIAMONDSPIR H10018025", WP_bar=560, standard="ISO 18752-C", OD_mm=41.2, min_bend_mm=350, kg_per_m=2.91,
    util_WP_vs_HPRV380=round(380 / 560, 3), util_WP_vs_spike430=round(430 / 560, 3), tightest_bend_R70_mm=394.3, util_bend=round(350 / 394.3, 3),
    note="loop hose >= 420 bar WP rule met with margin; tender tightest bend at R70 394.3 mm >= 350 min bend (Tender Bot)")
L42["brake_air_valve_C"] = "Source Bot: brake-air fill valves need C >= 0.31 dm3/(s bar) (per the Source data basis) - carried as the valve purchase spec; our path spec (C_spec_min 3.2 per branch / C >= 8-10 for the regulator and relay) is the governing value; vendor batch to confirm the as-bought C"
# --- L4.2 Loco Bot E8: QEV option A check (delete the QEVs; spring APPLY exhausts back through the relay valve)
def _t_exh(V, C, p0g, p1g, T=263.0, b=0.3, dt=1e-4):   # ISO 6358 discharge to atmosphere, isothermal at T (cold -10 C), V in L, C in dm3/(s bar)
    pa = 1.013; p = p0g + pa; t = 0.0
    while p > p1g + pa:
        r = pa / p; Qn = C * p * math.sqrt(293.0 / T) * (1.0 if r <= b else math.sqrt(1 - ((r - b) / (1 - b)) ** 2))
        p -= Qn * dt * pa / V * (T / 293.0); t += dt
    return t
_Cs = lambda *c: sum(x ** -3 for x in c) ** (-1 / 3)
_C_rel_exh, _C_trunks, _C_brA = 8.0, 48.9, 8.69          # relay exhaust C = relay spec (ASSUMED same as supply), 2 trunks, worst branch without QEV (Loco Bot E8)
_Vb, _Vtot = 2.0 + 0.86, 10.38                          # worst branch T2R: 2 calipers + 0.86 L pipe; total 8 calipers + 2.38 L pipe
_C_wA = _Cs(_C_brA, _Cs(_C_rel_exh, _C_trunks) / 4 * (_Vb / (_Vtot / 4)))   # worst branch's share of the common exhaust (volume-weighted)
_P_FULL_APPLY = 0.5    # bar g below which the Coremo D spring set gives (near) full clamp - ASSUMED (AWAIT Coremo curve); 0.3 bar g also reported
_tA = _t_exh(_Vb, _C_wA, 6.0, _P_FULL_APPLY); _tA3 = _t_exh(_Vb, _C_wA, 6.0, 0.3)
_C_qev_exh = 5.0       # QEV A->exhaust C per branch (option B purchase spec, ASSUMED = the P->A spec)
_tB = _t_exh(_Vb, _Cs(_C_qev_exh, 30.0), 6.0, _P_FULL_APPLY)
QEV_OPTION_A_OK = _tA <= 2.0
L42["QEV_option"] = dict(source="Loco Bot E8 (/workspace/loco/air/brake_path_L4.md, brake_ratings_E8.json): no catalogue 1/2 in QEV rated >= 15 bar working",
    option_A=dict(release_worst_s=2.39, worst_branch_C_exhaust=round(_C_wA, 2), relay_exhaust_C_ASSUMED=_C_rel_exh, from_bar_g=6.0, full_apply_bar_g_ASSUMED=_P_FULL_APPLY, cold_K=263,
                  t_apply_s=round(_tA, 2), t_apply_to_0p3bar_s=round(_tA3, 2), criterion_s=2.0, passes=QEV_OPTION_A_OK, shortfall_s=round(max(_tA - 2.0, 0.0), 2),
                  note="Exhaust time only (relay exhaust, worst branch, cold -10 C, isothermal); the IR-2 / relay pilot signal time comes on top"),
    option_B=dict(t_apply_s=round(_tB, 2), QEV="1/2 in QEV with a MAKER-CERTIFIED >= 15 bar (218 psi) working rating and a 4:1 burst test certificate - purchase spec, VENDOR BATCH (HOLD; no contact without the owner)"),
    decision=("ADOPT option A (QEVs deleted, -5.2 kg)" if QEV_OPTION_A_OK else "Option A FAILS the 2.0 s spring-apply criterion (%.2f s to %.1f bar g; %.2f s to 0.3 bar g) -> KEEP option B: maker-certified 15 bar QEVs (vendor batch); apply %.2f s; piping 43.7 kg gross" % (_tA, _P_FULL_APPLY, _tA3, _tB)),
    E8_carry=dict(trunk="3/4 in 316 seamless 25 x 2.5 (ID 20) trunk and MR feed, double-ferrule fittings", piping_gross_kg=43.7, piping_gross_option_A_kg=38.5, MR_feed_m=8.75, MR_feed_L=2.75,
                  hoses="SAE J1402 Type AII marked >= 225 psi WP, >= 900 psi burst (145 psi WP grades FAIL)", MR_one_release="6.0 -> 5.68 bar (coupled MR ~190 L incl. the tender MR pipe; >= the 5.6 bar worst case used for the release time)",
                  coupler="Crosby S-1325A WLL >= 5/8 G100 chain WLL: PASS (Loco Bot E8)"))
L42["release_interlock"] = dict(traction_enable=["T04 line >= 15 bar (2-channel)", "loco farthest-caliper release switch >= 5.1 bar", "Coach brake-release indication DUAL-CHANNEL per Electro E3.6h: trainline J-CC 22/23 + 34/35, Pilz B0 test pulses, PL d Cat 3, daily force-guided relay test (EOT BP switch >= 4.6 bar rising on the rear coach)", "2 s delay after the last proof"],
    coaches="Coach brake-release indication: dual-channel per Electro E3.6h (J-CC 22/23 + 34/35, Pilz B0 test pulses, PL d Cat 3, daily force-guided relay test). PE to confirm the fault exclusion for the single pressure element per switch and the test-pulse loop length (trainline run).")
# --- 10/11. wind on curves + 10 mph stop info
L42["wind_curve"] = dict(R80_dry_40mph_margin=0.939, R80_lub_40mph_margin=1.287, R80_dry_25mph_margin=1.018, R70_dry_25mph_margin=0.975,
    verdict="Dry R80 in 40 mph wind (0.939) is COVERED by the interim operating rule: 25 mph wind limit on R <= 80 and no full-pull starts on R <= 80 while any lubricator is out of service (lubricated R80 at 40 mph 1.287 PASS); Layout F has no R70.",
    rule="Wind > 25 mph: no operation on R <= 80 unless the walk-check confirms every gauge-face lubricator working; no full-pull starts on R <= 80 with any lubricator out of service")
L42["stop_10mph_info"] = "10 mph stop on 2 % down with the loco brake failed: 36.7 m vs 30 m (1.22) - INFORMATION ONLY: speed governed to 6 mph (42 cc + 2,600 rpm), independent 7 mph trip"
# --- safety-chain lugs PL44.5 + 1-1/8 in G-2130
_t_lug, _d_pin_sh, _a_edge = 42.5, 31.8, 32.5
_Rn_shear = 0.6 * 450 * 2 * _t_lug * (_a_edge + 35.0 / 2) / 1000 / 2.0; _Rn_bear = 1.8 * 345 * _t_lug * _d_pin_sh / 1000 / 2.0
L42["safety_chain_lugs"] = dict(plate="PL44.5 (1-3/4 in) A572-50, faced to 42.5 mm in the jaw zone of a 1-1/8 in Crosby G-2130 bolt shackle (WLL 9.5 t = 93.2 kN, pin 1-1/4 in)", weld="CJP to the rear headstock + PL16 internal diaphragm behind each lug; UT 100 %",
    hole_mm=35.0, edge_ASSUMED_mm=_a_edge + 17.5, shackle_util_70kN=round(70 / 93.2, 2), lug_shear_out_ASD_kN=round(_Rn_shear), lug_bearing_ASD_kN=round(_Rn_bear), util_200kN_ult=round(200 / min(_Rn_shear, _Rn_bear) / 2.0, 2), mass_kg_each=3.6,
    TE430_x1p5_kN=round(1.5 * F400, 1), shackle_util_HPRV_TE_x1p5=round(1.5 * F400 / 93.2, 2), lug_util_HPRV_TE_x1p5=round(1.5 * F400 / min(_Rn_shear, _Rn_bear), 2), chain_note="each safety chain = 2 x G-2130 + 2 x S-1325A + 1-2 links of 5/8 G100")
L42["loco_bot_E7"] = dict(
    safety_chain="EACH safety chain = 2 x 1-1/8 in G-2130 bolt shackles + 2 x Crosby S-1325A chain couplers (fallback A-1342N) + 1-2 links of 5/8 in Grade 100 chain; 5/8 in Grade 100 chain WLL 22,600 lb (100.5 kN); VENDOR-BATCH CHECK: coupler WLL >= the 5/8 G100 chain WLL (S-1325A / A-1342N size to be confirmed on the batch certificate), shackles 1-1/8 in G-2130 WLL 9.5 t",
    flange_final="FINAL: 28 mm withdraw train-wide, re-profile <= 27; joint rail-head vertical wear limit 2 mm; joint hardware protrusion past the gauge face measured <= 10 mm at install (Loco Bot: 2.09 mm min clearance at 2v+3s nominal hardware; 28 needed for high-tolerance hardware); pony 22 mm to the 50 mm flangeway; the 6 mm joint wear limit is WITHDRAWN",
    bp_trunk="L-114 note 3 AMENDED: the 3/4 in brake-release (BP-1) trunk at Z1180-1250 between the rails is an allowed exception, with >= 25 mm to the chain cases at the +/-22 mm bump stops and >= 75 mm from hot hydraulic lines",
    loop_hoses="SUPERSEDED by the L4.2 pressure revision: PL 350 / HPRV 380; loop hoses, fittings and whip restraints >= 420 bar WORKING (standard -16 hose, code 62 and 24 deg S25 ends at the maker's 420, Parker -16 restraint 420) with ISO 18752 / SAE J517 impulse rating covering the transient above HPRV; the >= 450 bar requirement and its HOLD are withdrawn; the Danfoss overshoot confirmation stays in the vendor batch (does not gate)",
    masses="brake piping 38.5 kg gross (replaces 5.0 net), MR feed 11.0 kg, safety-chain parts 32.2 kg (+12.7 vs E6) - in the loco ledger; adhesion and start margins rerun on the new loco mass")
L42["flange"]["rail_bot_5b_FINAL"] = "Rail Bot track_basis §5b (FINAL): joint rail-head vertical wear limit 2 mm = rail height condemn <= 86.9 mm at bolt positions; the 6 mm head-wear limit applies only > 1 m from rail ends; joint-bolt protrusion past the gauge face <= 10.0 mm (worst case 9.1 mm with FLAT joint bars <= 12.0 mm thick + 3/4 in ASME B18.10 oval-neck bolts, head H <= 12.7 mm); heavy 15.9 mm bars REJECTED"
L42["flange"]["joint_bar_max_mm"] = 12.0; L42["flange"]["rail_height_condemn_at_bolts_mm"] = 86.9
L42["flange"]["install_protrusion_max_mm"] = 10.0; L42["flange"]["pony_to_flangeway_mm"] = 22.0; L42["flange"]["joint_6mm_limit"] = "WITHDRAWN"
L42["grade_basis"] = "The TRACK is designed LEVEL: Layout F is CONFIRMED DEAD LEVEL, 0.0 % (Rail Bot §5b, final); the VEHICLES are designed and checked for a 2 % grade as a CONSERVATIVE case (kept; covers any future owner grade decision)."
# --- L4.2: chain minimum breaking load with the SAME factor as the old >= 302.5 kN at HPRV 400, applied at the 430 bar strength basis (and at HPRV 380 for information)
_pull400 = pull(T_m(Vg1, 400.0) * i_ch / 1000); _pull_h = pull(T_hprv_ax / 1000); _pull380 = pull(T_m(Vg1, P_HPRV) * i_ch / 1000); _fac_mbl = 302.5 / _pull400
_req430 = _fac_mbl * _pull_h; _req380 = _fac_mbl * _pull380
J["chain"]["MBL_L42"] = dict(old_req_kN=302.5, old_basis="ANSI B29.1 duplex 302.5 kN at HPRV 400 (pull %.1f kN) -> factor %.2f" % (_pull400, _fac_mbl), factor=round(_fac_mbl, 2),
    pull_430_kN=round(_pull_h, 1), required_430_kN=round(_req430, 1), pull_380_kN=round(_pull380, 1), required_380_kN=round(_req380, 1), tsubaki_RS120_2_published_kN=296.0,
    util_296_at_430=round(_req430 / 296.0, 3), util_296_at_380=round(_req380 / 296.0, 3), SF_ult_296_at_430=round(296.0 / _pull_h, 2),
    verdict="Same factor at HPRV 380: %.1f kN -> 296 PASSES (%.3f). Same factor at the 430 bar STRENGTH basis (governing): %.1f kN -> 296 does NOT pass (%.3f; SF on ultimate %.2f vs the old %.2f)." % (_req380, _req380 / 296.0, _req430, _req430 / 296.0, 296.0 / _pull_h, _fac_mbl),
    rule="SPEC: ANSI 120-2 chain with a mill certificate of breaking strength >= %.0f kN per lot (same factor at 430 bar). Standard Tsubaki RS120-2 (296 kN published) is NOT accepted unless the PE accepts SF %.2f on ultimate at the 430 bar spike; a higher-strength 120-2 (e.g. heavy/super series) certified >= %.0f kN is a VENDOR-BATCH item (no contact without the owner)" % (math.ceil(_req430), 296.0 / _pull_h, math.ceil(_req430)))
J["pressure_L42"] = dict(PL_bar=350, HPRV_bar=P_HPRV, spacing_bar=30, basis="L4.2 pressure revision (Source Bot: no -16 assembly rated >= 450 bar): PL 350 unchanged (working pull and gradeability unchanged), HPRV 380 (was 400) = the original Oct 27 basis, 30 bar PL-HPRV spacing",
    loop_parts="Loop components rated >= 420 bar WP >= HPRV 380 (standard -16 hose, code 62 and 24 deg S25 ends at the maker's 420, Parker -16 whip restraint 420); the transient spike (~430 bar) is covered by the ISO 18752 / ISO 6605 impulse rating (133 % of WP); strength cases are checked at 430 bar", strength_bar=P_STR,
    danfoss="The Danfoss HPRV overshoot figure is INFORMATION ONLY (vendor batch), not gating",
    rerun="All strength checks that used HPRV 400 re-run at the 430 bar STRENGTH basis (transient spike; HPRV 380 is the setting): spline, 45T ring bolts, hub fit, motor bearing radial, chain pull/MBL, motor bracket, axle seat, traction pin service case, safety-chain lugs. Run-in trip cases keep the Stress Bot 400 bar hydraulic force (conservative).")
J["L42"] = L42
J["basis"]["max_driver_wheel_kN"] = round(max(_wmax(TE_LIM_F, 1), _wmax(TE_LIM_R, -1)), 2)   # L4.2: at the PLUS+1 TE command limits (K2-a)
J["basis"]["max_driver_wheel_uncapped_kN"] = round(K2A_WHEEL, 2)
J["wheel_wear_L41"]["traction"]["K2a_max_wheel_kN"] = "<= %.2f at the PLUS+1 TE command limits (L4.2)" % J["basis"]["max_driver_wheel_kN"]
# ---- L4.1 steering 8/9: brake air (loco release time <= 4 s, train air with TB-3.9)
import math as _m
def _t_fill(C, V=8.0e-3, p1g=6.0, ptg=5.1, b=0.3, n=1.2, T=293.0):
    """ISO 6358 fill of the caliper volume V from 0 bar g to ptg through total sonic conductance C [dm3/(s bar)], supply p1g."""
    Cs = C * 1e-8; p1 = (p1g + 1.013) * 1e5; p = 1.013e5; pt = (ptg + 1.013) * 1e5; t = 0.0; dt = 1e-3
    while p < pt:
        r = p / p1; phi = 1.0 if r <= b else _m.sqrt(max(0.0, 1 - ((r - b) / (1 - b)) ** 2))
        p += n * 287 * T / V * Cs * p1 * 1.185 * phi * dt; t += dt
        if t > 60: return 99.0
    return round(t, 2)
_SIG = 1.0      # BP / driver command -> relay-valve opening allowance, s (ASSUMED; measure at commissioning)
_Creq = next(c / 100 for c in range(100, 1000, 5) if _t_fill(c / 100, p1g=5.6, n=1.0) + _SIG <= 4.0)
_BUD = dict(release_regulator_relieving_half_in=10.0, relay_valve_half_in=8.0, trunk_3q_in_ID19_le12m_eq=8.0)
_BR = 2.0   # per-axle branch (1/2 in hose ID 12.7 <= 2 m + full-bore fittings to 2 calipers), 4 in parallel
_Ctot = (sum(c ** -3 for c in _BUD.values()) + (4 * _BR) ** -3) ** (-1 / 3)
_t_spec = _t_fill(3.0, p1g=5.6, n=1.0) + _SIG
J["brake_air_L41"] = dict(
    basis="Steering 8/9: loco caliper air 8 x 1.0 L = 8.0 L, 48 L free air per release, MR drop 0.98 bar per release, recharge 17.8 s at 14 cfm (Loco Bot / Tender Bot). Target: loco brake release <= 4 s WORST CASE from BP rise / release command to every caliper >= 5.1 bar (Coremo full-release min). ISO 6358 fill model, b 0.3.",
    model_check=dict(loco_bot_estimate_s=3.7, loco_bot_C=2.0, loco_bot_range_s="1.8-7.3", this_model_C2_nominal_s=_t_fill(2.0), this_model_C2_worst_fill_s=_t_fill(2.0, p1g=5.6, n=1.0)),
    worst_case="regulated supply drooped to 5.6 bar g, isothermal fill (n 1.0), target 5.1 bar g, plus %.1f s signal/relay response (ASSUMED)" % _SIG,
    C_required_min=_Creq, C_spec_min=3.2, t_at_C_spec_s=round(_t_spec, 2),
    loco_bot_E7=dict(path_C_total=6.85, worst_branch="T2R, C 4.72 (series 4.70), 0.86 L", volume_L=10.26, calipers_L=8.0, pipe_L=2.26, mr_feed_L=2.19,
        release_nominal_s=2.22, release_worst_s=2.36, limit_s=4.0, result="PASS (L4.2: C_spec_min raised 3.0 -> 3.2 per branch/valve set because 3.0 gives 4.10 s at the real 10.26 L; 3.2 -> 3.91 s)",
        QEV="1/2 in QEV P->A C >= 5 purchase spec (C 3 still gives branch 2.9 >= 2.0)", source="/workspace/loco/air/brake_path_L4.md (Loco Bot E7)"),
    budget=dict(series_parts=_BUD, branch_per_axle_C=_BR, branches=4, C_total_budget=round(_Ctot, 2), t_at_budget_s=round(_t_fill(_Ctot, p1g=5.6, n=1.0) + _SIG, 2),
                rule="series: C_tot = (sum C_i^-3)^(-1/3); the 4 axle branches act in parallel (C adds). Part C values are the purchase spec minimums; Loco Bot line lengths/fittings to confirm the trunk and branch values"),
    parts=["Release-air regulator, relieving, 1/2 in ports, set 6.0 bar, C >= 10 dm3/(s bar) (>= 2,000 NL/min at 8 bar in; Norgren R74G / SMC AR40 class) - replaces the small B1-l regulator",
           "Brake relay valve 1/2 in ports, C >= 8, piloted by the existing WABCO 971 899 152 0 inverting relay (keeps the fail-safe logic; pilot only, no power flow through the IR-2)",
           "Release trunk 3/4 in (ID >= 19 mm; SS 25x2 or Cu-Ni 22x1.5 ID 19) <= 12 m equivalent length incl. fittings, C >= 8; full-bore ball valve only (no 1/4 in pilots or check valves in the power path)",
           "Per axle branch: 1/2 in SAE J1402 hose ID 12.7 <= 2 m + full-bore JIC/ORFS fittings to a tee at the two calipers, C >= 2.0 each (4 branches)",
           "Quick-exhaust valve 1/2 in at each axle tee (apply speed, does not slow release)",
           "Release-proof pressure switch on the farthest caliper line, 5.1 bar rising -> traction enable (no traction until every caliper is released)",
           "Commissioning test: time from release command to 5.1 bar at the farthest caliper <= 4.0 s at MR cut-in (7.5 bar) and -10 C; record in the brake test sheet"],
    mr_L42=dict(coupled_MR_L=190.0, release_volume_L=10.26, drop_per_release_bar=0.32, MR_min_bar=6.0, MR_after_one_release_from_min_bar=5.68, MR_after_from_cut_out_bar=8.18, worst_supply_in_release_time_bar=5.6,
        MR_feed_L=2.75, tender_MR_pipe_L=V_TMR, local_reservoir_L=0.0,
        note="L4.2 (Loco Bot E8): the coupled MR is ~190 L (3 x 47 L tender reservoirs + pipes incl. the MR feed 2.75 L and the tender MR pipe 3/4 in x ~5.3 m %.2f L); one release takes the MR 6.0 -> 5.68 bar (>= the 5.6 bar worst case in the release time). The 20 L local reservoir proposed on the earlier 51.8 L MR estimate is DELETED (-14 kg)" % V_TMR),
    mr=dict(drop_per_release_bar=0.98, mr_after_one_release_from_cut_in_bar=round(7.5 - 0.98, 2), regulator_set_bar=6.0, ok_after_one=7.5 - 0.98 >= 6.0 + 0.4,
            releases_before_regulator_droop_from_cut_out=int((8.5 - 6.4) // 0.98), recharge_s_at_14cfm=17.8,
            rule="Supply holds for 2 releases from cut-out (8.5 bar) and 1 from cut-in (7.5 bar); a 3rd quick release waits for recharge (17.8 s) - covered by the 4 s check at cut-in"),
    train=dict(caliper_volume_total_L=14.0, release_free_air_L=84.0, steady_demand_cfm=3.55, compressor_cfm=14.0, duty=round(3.55 / 14.0, 2), loco_share_L=8.0),
    tender_TB313c=dict(mass_kg=8706.5, cg=[2422.7, 11.3, 1110.4], includes="tender-end safety-chain shackles", full_brake_decel_ms2=round(5.845 / 8.7065, 3), full_brake_kN=5.845, MR_pipe="3/4 in x ~5.3 m to the MR glad hand at Y-950/Z1950, %.2f L (in the MR volume)" % V_TMR, supersedes="TB-3.13b 8,700.1 / TB-3.11 8,646.6 kg CG [2412.3, 10.6, 1109.1] 0.676 m/s2",
                     calipers="mixed Coremo D 2N spring sets, 25.4 mm discs, pad wear limit 5.5 mm", cradle_mm=-50),
    erv=dict(roof_allocation_static_mm=3450, kinematic_envelope_check_mm=4300, note="ERV pod 3,450 ARL is the STATIC allocation; the kinematic envelope (bounce/roll/lateral) is checked against the K-401 overhead 4,300"),
)
J["unsprung_per_axle"] = dict(hub_calc=dict((k, round(v, 2)) for k, v in HUB.items()), ring_45T_kg_ASSUMED=m_add_axle["sprocket_45T_rim_ring_bolted"], pressed_hub_kg=m_add_axle["pressed_hub_4140_flange"],
    chain_half_kg=round(0.5 * links * p_c / 1000 * 11.7, 1), seal_plate_moving_part_kg=5.0, disc_kg=29.0,
    total_drive_unsprung_kg=round(m_add_axle["sprocket_45T_rim_ring_bolted"] + m_add_axle["pressed_hub_4140_flange"] + 0.5 * links * p_c / 1000 * 11.7 + 5 + 29, 1),
    note="L4.1: hub Ø240x110 with Ø350 x 20 integral flange %.1f kg CALC (L4: Ø340, 28 kg ASSUMED). Source Bot REV3: 45T = rim-only 120-2 ring WITH a bolting web (~50 kg, ASSUMED) bolted to the hub flange (keyless hub pressed on the axle);" % HUB_KG + " the ring is SPLIT (2 halves) so it is replaced in place WITHOUT pressing or a wheelset drop. Tsubaki D120A45 plate (~53 kg) and Martin D120C45 (85 kg) dropped. MS05 motor, bracket and 15T are sprung (truck frame).")
J["chain"]["links_note"] = "54 links (C 417.6 new) are set by the motor-to-transom clearance; Source Bot listed 56 links at ~450 mm centres - ORDER 54 (or cut the 56 to 54; even count, no offset link). 56 links would put the motor 38 mm into the transom."
# ------------------------------------------------------------------ motor bearing (radial) and spline
Fr_dyn_allow = 60.0
L_req = 20000 * 60 * motor_rpm(6.0) / 1e6
L_at = lambda F: 10 * (30.0 / F)**(10 / 3)
J["motor_bearing"] = dict(radial_HPRV_kN=round(pull(T_hprv_ax / 1000), 1), allow_dyn_kN_chart=Fr_dyn_allow, util=round(pull(T_hprv_ax / 1000) / Fr_dyn_allow, 2),
                          L_req_Mrev_20000h_6mph=round(L_req, 1), L_at_run2pct_Mrev=round(L_at(pull(T_run2)), 0), L_at_level_Mrev=round(L_at(pull(run_res(0) * r / 4)), 0),
                          spline_T_HPRV_Nm=round(T_m(Vg1, P_STR)), spline="shaft code 5, DIN 5480 W55x3x17 (male; 15T hub N55x3x17 female) - no torque limitation published (2A40 keyed Ø50 limited to 800 N.m - REJECTED); AWAIT Poclain confirmation for %s N.m peak at the %.0f bar strength basis + chain overhung load" % (format(round(T_m(Vg1, P_STR)), ','), P_STR),
                          note="2A50 permissible dynamic radial ~60 kN at the reference offset read from the catalog chart (p.20); sprocket centre must sit at offset <= 0 (close to the flange) - AWAIT Poclain AE. Bearing life scaled L ∝ F^-10/3 from the catalog 10 Mrev at ~30 kN curve; running 2 % treated as continuous (conservative).",
                          rejected="2AC0 integral ANSI 100 12T pinion: PD 123 needs a 36T driven sprocket and a single-strand 100 chain at SF < 3 on ultimate - rejected")
# ------------------------------------------------------------------ axle: pressed hub, no keyway, heaviest axle, NO hardening credit
Rh = max(max(ax.values()), max(ax_asis.values())); Q = Rh / 2
Mb_EN = 1.25 * Q * 0.157 + 0.35 * Rh * 0.725
P_hub = pull(0.25 * drv / 4 * r) + 3 * (m_add_axle["sprocket_45T_rim_ring_bolted"] + m_add_axle["pressed_hub_4140_flange"]) * g / 1000
a_s, L_b = 0.330 - 0.210, 0.660                       # sprocket centre Y-210, boxes at Y+/-330
M_hub = P_hub * a_s * (L_b - a_s) / L_b
M_seat = Mb_EN + M_hub                                # arithmetic sum (chain pull is horizontal - conservative)
T_need_ax = need2 / 4 * r
def sig(M, d): return 32 * M * 1e6 / (math.pi * d**3)
def tau(T, d): return 16 * T * 1e6 / (math.pi * d**3)
def goodman(d, Kf, Kfs=2.0, Su=1000.0, k_tr=1.0, M=None):
    M = M_seat if M is None else M
    Se = 0.5 * min(Su, 1400) * 4.51 * Su**-0.265 * 1.51 * d**-0.157 * 0.814 * k_tr
    sa = Kf * sig(M, d); sm = math.sqrt(3) * Kfs * tau(T_need_ax, d)
    return dict(d=d, Kf=Kf, Se=round(Se), sigma_a=round(sa, 1), sigma_m_vm=round(sm, 1), n=round(1 / (sa / Se + sm / Su), 2))
seat = {f"d{d}_pressfit_Kf2.0_no_hardening": goodman(d, 2.0) for d in (130, 140, 145, 150)}
seat["d150_pressfit_Kf2.0_induction_hardened_k1.5_INFO"] = goodman(150, 2.0, k_tr=1.5)
fil = goodman(130, 1.36, Kfs=1.25)                    # body Ø130 at the seat shoulder: D/d 1.15, r 13 (r/d 0.10): Kt 1.40, q 0.9
vm_EN = math.sqrt(sig(M_seat, 150)**2 + 3 * tau(T_hprv_ax / 1000, 150)**2)
d_s, Dh, Lh, mu_f, E = 150.0, 240.0, 110.0, 0.12, 210000.0
c2 = (d_s / Dh)**2
p_of = lambda dl: dl * E * (1 - c2) / (2 * d_s)
T_cap = lambda p: math.pi * d_s**2 * Lh * mu_f * p / 2 / 1e6      # kN.m
# L4.1 (Stress Bot r2 #4): hot hub (oil bath, hub 30 K over the seat), roughness smoothing 9.6 um, groove land 6 mm deducted, shrink-only mu 0.12
_dh = 0.15 - 0.0096 - 11.5e-6 * 30 * d_s; _Th = math.pi * d_s**2 * (Lh - 6) * mu_f * p_of(_dh) / 2 / 1e6
FIT_HOT = dict(delta_eff_mm=round(_dh, 4), T_slip_kNm=round(_Th, 1), SF_HPRV=round(_Th / (T_hprv_ax / 1000), 2), SF_HPRV_x1p5=round(_Th / (1.5 * T_hprv_ax / 1000), 2),
               SF_reversal_ramped_x1p3=round(_Th / (1.3 * T_hprv_ax / 1000), 2), criteria="SF >= 1.5 at HPRV; >= 1.0 at HPRV x 1.5 and at a ramp-limited reversal (impact 1.3, PLUS+1 >= 1 s through zero)",
               allow_gradient_K=round((0.15 - 0.0096 - (1.5 * T_hprv_ax / 1000) / (math.pi * d_s**2 * (Lh - 6) * mu_f / 2 / 1e6) * 2 * d_s / (E * (1 - c2))) / (11.5e-6 * d_s), 0),
               verdict="PASS: shrink-only 0.15-0.20 keeps SF >= 1 at HPRV x 1.5 with a 30 K hot hub and the removal groove; the groove is KEPT (removal only). Oil-pressed assembly DELETED.")
# L4.1 ring bolts: catalog cl.8.8 FITTED bolts DIN 609 (hex, fitted shank Ø17 = d+1) / DIN 7968 (structural fitted), on PCD 300, 12 per hub, Ø350 flange
_F = T_hprv_ax / 1000 / 0.150 / 12; _Fd = 1.5 * _F
_As_sh = math.pi / 4 * 17**2; _Fv = 0.6 * 800 * _As_sh / 1.25 / 1000          # EN 1993-1-8 Tab 3.4 shear, plane through the fitted shank, gamma_M2 1.25
_Fb = 2.5 * 1.0 * 565 * 17 * 20 / 1.25 / 1000                                   # bearing on the 20 mm flange/web (C45/4140 fu >= 565 ASSUMED, alpha_b 1.0)
_FpC = 0.75 * 580 * 157 / 1000                                                  # project preload 0.75 x proof (ISO 898-1 8.8 M16 Sp 580 MPa, As 157) = S-503 rule
_slip = 12 * 0.9 * _FpC * 0.20 * 0.150                                             # friction capacity kN.m (mu 0.20 machined/clean, 0.9 relaxation)
RB = dict(spec="12 x M16 cl.8.8 FITTED bolts DIN 609 (or DIN 7968) zinc-flake, reamed Ø17 H11/k6 holes, PCD 300 on the Ø350 flange; Nord-Lock NL16; tighten 219 N.m DRY (S-503 rule T = K F d, K 0.20, F = 0.75 x proof 68.3 kN; 153 N.m if lubricated K 0.14) - re-torque at 10 h",
          F_per_bolt_HPRV_kN=round(_F, 2), F_design_HPRV_x1p5_kN=round(_Fd, 2), shear_cap_kN=round(_Fv, 1), util_shear=round(_Fd / _Fv, 3),
          bearing_cap_kN=round(_Fb, 1), util_bearing=round(_Fd / _Fb, 3), preload_kN=round(_FpC, 1), friction_capacity_kNm=round(_slip, 1), util_friction_vs_HPRV=round(T_hprv_ax / 1000 / _slip, 2),
          edge_distance_mm=175 - 150, edge_ratio_d0=round(25 / 17, 2), edge_rule="e >= 1.25 d0 = 21.3 mm (L4 Ø340: 20 mm = 1.18 d0 NG) -> Ø350: 25 mm = 1.47 d0 OK",
          note="Joint is friction-type at 8.8 preload (12 x 68.3 kN): the HPRV torque is carried by friction (%.2f of capacity); the fitted shanks are the positive back-up. 10.9 not needed (util %.3f in shear at HPRV x 1.5).")
RB["note"] = RB["note"] % (RB["util_friction_vs_HPRV"], RB["util_shear"])
J["axle"] = dict(heaviest_axle_kN=Rh, M_EN_kNm=round(Mb_EN, 2), P_hub_kN=round(P_hub, 1), M_hub_kNm=round(M_hub, 2), M_seat_kNm=round(M_seat, 2), T_need_kNm=round(T_need_ax, 2),
                 seat_fatigue=seat, chosen="Ø150 raised sprocket seat (body Ø130, journals per bearing), 34CrNiMo6 Q&T Rm>=1000 (or EA4T), NO keyway, fine-turned/ground Ra 0.8, relief radius r13 + undercut at the hub edge",
                 n_chosen=seat["d150_pressfit_Kf2.0_no_hardening"]["n"], required_n=1.5, shoulder_fillet_body130=fil,
                 EN13103_screen=dict(sigma_vm_MPa=round(vm_EN, 1), permissible_pressfit_seat_EA4T_MPa_ASSUMED=110, util=round(vm_EN / 110, 3)),
                 press_fit=dict(d=d_s, hub_OD=Dh, hub_len=Lh, mu=mu_f, interference_mm=[0.15, 0.20], p_min_MPa=round(p_of(0.15), 1), p_max_MPa=round(p_of(0.20), 1), L4_interference_mm=[0.12, 0.17],
                                T_slip_min_kNm=round(T_cap(p_of(0.15)), 1), SF_vs_HPRV=round(T_cap(p_of(0.15)) / (T_hprv_ax / 1000), 2), hot_case=FIT_HOT,
                                hub_hoop_max_MPa=round(p_of(0.20) * (1 + c2) / (1 - c2), 1), hub_Sy_4140_MPa=655,
                                assembly="SHRINK ONLY: heat hub to 200-230 °C (expansion %.2f mm at ΔT 190 K > 0.20 + 0.10 assembly clearance); NO oil pressing. Oil-injection groove (6 wide, in the hub bore, mid-length) + plugged M8 port for removal only" % (d_s * 11.5e-6 * 190)),
                 ring_bolts=RB,
                 note="Stress Bot asked for a seat that passes WITHOUT hardening credit on the heaviest axle: Ø150 with press-fit fretting Kf 2.0 gives n %.2f (Ø140 n %.2f fails). Hardening optional (info n %.2f)." % (seat["d150_pressfit_Kf2.0_no_hardening"]["n"], seat["d140_pressfit_Kf2.0_no_hardening"]["n"], seat["d150_pressfit_Kf2.0_induction_hardened_k1.5_INFO"]["n"]))
# ------------------------------------------------------------------ axlebox bearing (heaviest axle + chain pull) - Stress Bot #13
unsprung = 2 * 300 + 75 + 0.5 * (m_add_axle["sprocket_45T_rim_ring_bolted"] + m_add_axle["pressed_hub_4140_flange"]) + 58 * 0.5 + 15
P_box = (Rh - unsprung * g / 1000) / 2
F_ch_box = pull(T_run2) * (0.330 + 0.210) / 0.660 / 1.0     # chain pull reaction at the near (Y-) box, running 2 % continuous (conservative)
Fr = math.hypot(P_box, F_ch_box)
L10 = 20000 * 60 * wheel_rpm(7.5) / 1e6
Peq = 1.3 * (Fr + 2.5 * 0.35 * Rh / 2)
J["axlebox"] = dict(P_box_kN=round(P_box, 1), chain_reaction_kN=round(F_ch_box, 1), Fr_kN=round(Fr, 1), Peq_kN=round(Peq, 1), L_Mrev=round(L10, 1), C_req_kN=round(Peq * L10**0.3, 1),
                    C_req_design_basis_kN=190.0, C_req_L4_kN=186.7, C_req_L41_kN=round(Peq * L10**0.3, 1), C_earlier_basis_kN=169.0,
                    note="L4.1: GOVERNING bearing basis C >= 190 kN (rounded up from the computed C_req) per driven axlebox bearing (computed C_req L4.1 = %.1f kN; L4 186.7), heaviest axle + chain-pull reaction (Stress Bot #13). The earlier >= 169 kN basis is superseded. Strasburg/Uhrich bearing confirmation = HELD vendor ask (no contact)." % (Peq * L10**0.3))
# ------------------------------------------------------------------ motor bracket + transom
F_br = 1.5 * pull(T_hprv_ax / 1000) + 3 * 64 * g / 1000
M_br = F_br * 0.200
S_w = 2 * 0.707 * 10 * 400**2 / 6
J["bracket"] = dict(F_design_kN=round(F_br, 1), M_kNm=round(M_br, 2), weld="PL25 A572-50 hanger, 2 x 400 x 10 fillet both sides to the transom underside + 2 PL16 gussets; slotted motor plate (4 x M20 cl.10.9 in 50 mm slots) with 2 jack screws M20",
                    weld_bending_MPa=round(M_br * 1e6 / S_w, 1), weld_shear_MPa=round(F_br * 1000 / (2 * 400 * 7.07), 1), allow_MPa=145.0,
                    reaction_torque_Nm=round(T_m(Vg1, P_STR)), transom_horizontal_sigma_MPa=round(F_br * 0.660 / 4 * 1e6 / (((200 * 300**3 - 168 * 268**3) / 12) / 150), 1))
# ------------------------------------------------------------------ brakes (axle discs unchanged) + MS05 parking brake
T_park_ax = 3165 * i_ch; T_emer_ax = 2740 * i_ch
J["brake"] = dict(service_emergency="UNCHANGED from L3: Ø340x25 axle disc on the free side (Y+), 2 spring-applied air-released calipers per disc; tare 12 % ratio; train BP spring brakes",
                  MS05_T04_park_loco_kN=round(4 * T_park_ax / r / 1000, 1), MS05_T04_dynamic_kN=round(4 * T_emer_ax / r / 1000, 1),
                  MS05_energy_per_motor_6mph_loco_only_kJ=round(0.5 * loco_kg * (6 * 0.44704)**2 / 4 / 1000, 1), MS05_energy_limit_kJ=85.9,
                  MS05_release="L4.1 parts in J[loco_valves]: loop low-pressure (charge 12-30 bar) via LP selector + 3-way solenoid valve + 0.75 L accumulator: motor brakes apply ONLY on park command or below 0.5 mph; an engine stall at speed does NOT dump them (catalog: dynamic use max 10 times)",
                  towing=["Manual release for rescue towing: loco + coach spring calipers with mechanical wind-off release (supplier option) and the MS05 T04 emergency release screws (M12, 60 N.m, per Poclain) - tag-out card",
                          "Hydrostatic loop: open the L4.1 loco TOW VALVE (lockable ball valve across A/B, J[loco_valves]) and freewheel the MS05s per Poclain before towing; max tow speed 2 mph. H1P053 HPRV bypass (3 turns) = short moves only (Danfoss: <= 20 % max speed, <= 3 min)", "Re-apply and function-test every brake before service (Poclain: check the parking brake after any emergency use)"],
                  overspeed="Overspeed trip INDEPENDENT of PLUS+1: certified 2-channel speed relay (SIL 2 / PL d class) reading 2 dedicated sensors on different trucks, hard-wired to the BP exhaust (emergency) valve and pump neutral; trip 7 mph, tested daily (F770)")
# ------------------------------------------------------------------ REV L4.1 additions
J["rev"] = "L4.2"
# (1) flow-divider blocker: Jahns HTO-4-35-FI (IC Fluid catalog pp. 24-27, sourcing/refs/README.md) vs electronic traction control
_sec_cc = 34.3; _qmin = (12.0, 16.0); _qmax = 82.0; _p_cont = 320.0; _p_peak = 380.0; _acc = (0.03, 0.04); _m_div = 160.0; _bp = (3.0, 5.0)
_q_sec_2mph_1st = 4 * Vg1 * motor_rpm(2.0) / eta_v / 1000 / 4       # L/min per section at 2 mph in 1st
_q_sec_start = [round(4 * Vg1 * motor_rpm(v) / eta_v / 1000 / 4, 1) for v in (0.25, 0.5, 1.0, 2.0)]
_dp_motor_max = _p_cont - 25.0 - _bp[1]                              # loop high side limited by the section rating, less charge (low side) and tank back-pressure
_TE_div = F_te(Vg1, _dp_motor_max, eta_s)
_ax_div = dict(ax); _a_min_div = amin + 160.0 * fr(5675.0) * g / 2000     # (info) a 160 kg divider mid-loco
J["flow_divider_study"] = dict(
    candidate="Jahns HTO-4-35-FI 4-section gear divider (34.3 cc/rev/section; min 12-16 L/min, max 82 L/min per section; 320 bar cont / 380 peak; +/-3-4 %; ~160 kg; 770x250x256; per-section relief + suction; tank back-pressure 3-5 bar)",
    flow_per_section_Lmin_at_mph_0p25_0p5_1_2_in_1st=_q_sec_start, flow_per_section_2mph_1st_Lmin=round(_q_sec_2mph_1st, 1), min_flow_per_section_Lmin=_qmin,
    finding_min_flow="Every start (0-2 mph) runs the sections BELOW their 12-16 L/min minimum - the catalog accuracy (+/-3-4 %) does not apply there; the divider does not lock the axles when it is needed (start) - NOT DEMONSTRATED by any data",
    motor_dp_max_bar=_dp_motor_max, TE_at_section_rating_kN=round(_TE_div, 1), need_2pct_kN=round(need2, 2), margin_TE_at_section_rating=round(_TE_div / need2, 2),
    finding_pressure="Section rating 320 bar cont minus charge (low side ~25 bar) and tank back-pressure caps motor dp at ~%.0f bar -> TE %.1f kN < %.1f kN needed on 2%% (margin %.2f): the divider would itself fail the 2%% start (and intensification n/(n-k) on a slipping section is limited only by the section reliefs)" % (_dp_motor_max, _TE_div, need2, _TE_div / need2),
    mass_kg=_m_div, heat="adds ~5 % of 35 kW while engaged (removed from the cooler duty)",
    decision="(b) NO gear flow divider. Per-motor ELECTRONIC traction control (J['traction_control']). Divider mass in the ledger = 0 kg (not fitted); 160 kg avoided",
    rejected=["(a) Jahns HTO-4-35-FI gear divider: below min flow at every start, 320 bar section rating caps TE below the 2 % need, +160 kg, +heat", "(c) 4 x separate pumps/loops: no PTO space on the V3307, cost/complexity - not pursued"])
# (2) electronic traction control (replaces the divider)
_v_spin_1st = 4 * Vg1 * motor_rpm(0.5) / Vg1                       # one motor taking all the flow at 0.5 mph
J["traction_control"] = dict(
    hardware=["Existing MS05 speed sensor per motor (4) into PLUS+1 (axle speed)", "NEW 3rd pickup on the UNBRAKED, UNDRIVEN pony truck tone ring = true ground-speed reference (separate from the 2 overspeed-relay sensors)", "Existing H1P053 EDC displacement control (destroke), auto-sanders lead axle each direction (solenoid per side)", "Pressure transducers loop A and B (2) for hill-start hold and rollback logic"],
    logic=["Slip detect: any axle > v_ref x 1.10 or > v_ref + 0.5 mph, or axle acceleration > 0.5 m/s2 (100 ms filter)",
           "Response 1: auto-sand the lead axle (wet or dry); response 2: pump destroke to the flow for v_ref x 1.05 within 0.3 s (EDC response ASSUMED, AWAIT Danfoss); response 3: rate-limited ramp back (<= 0.5 kN/s) after re-adhesion (slip < 3 % for 1 s)",
           "Start always in 1st (468 cc): 2nd inhibited below 2.5 mph", "Hill-start hold: loco brakes released only when loop dp >= hold pressure for the grade (~%.0f bar on 2%%); rollback > 0.3 m with traction commanded -> alarm + pump hold + brake apply" % (350 * (0.02 * W) / F350),
           "Sensor fault (any axle or v_ref) -> alarm, 1st only, TE limited to the equal-torque dry value, sand on; fault of the pony reference -> fall back to the slowest axle as reference"],
    physics="The pump is a FLOW source: with the 4 motors in parallel, one spinning axle can only take the flow the pump delivers for the train speed - at 0.5 mph in 1st that axle reaches at most ~%.1f mph surface speed (x4), so spin is self-limited at starts; in 1st the hardware maximum spin is %d motor rpm vs 370 limit even with no software" % (4 * 0.5, spin1),
    cap="TE cap = equal torque 4 x mu x lightest axle (no credit for divider locking)",
    dry_2pct_margin=[c_["dry_equal_margin"] for c_ in cases if c_["case"] == "2% tangent"][0], sanded_2pct_margin=[c_["sanded_equal_margin"] for c_ in cases if c_["case"] == "2% tangent"][0], wet_unsanded_2pct_margin=[c_["wet_equal_margin"] for c_ in cases if c_["case"] == "2% tangent"][0],
    rule="Front-ballast rule unchanged: plates sized so the DRY/SANDED equal-torque 2 % start margin >= 1.10; wet unsanded fails as before -> SAND MANDATORY on wet grades/curves < R100 (operating rule, auto-sand)",
    software="PLUS+1 application + parameters by Danfoss/integrator = HELD vendor ask (no contact); PE to review the logic; functional test on track before service",
    mass_kg=28.0, mass_note="in LB 'L4.1 traction-control + loco valve package' 28 kg @X5675 (ASSUMED)")
_RL = json.load(open("/workspace/train/calcs/track/L4/route_L4.json"))["start"]
_Wl4 = 791.6
J["traction_control"]["route_starts_equal_torque"] = {k: dict(need_kN=round(v["need_kN"] * W / _Wl4, 2), dry_or_sanded=round(min(F350, 4 * 0.25 * amin) / (v["need_kN"] * W / _Wl4), 2),
    wet_unsanded=round(4 * 0.15 * amin / (v["need_kN"] * W / _Wl4), 2), wet_with_divider_L4=v["wet_divider"], sand_required=4 * 0.15 * amin < v["need_kN"] * W / _Wl4) for k, v in _RL.items()}
J["traction_control"]["route_note"] = "Worst route start points (route_L4.json, need scaled to the L4.1 W): dry/sanded all pass; WITHOUT the divider, wet unsanded starts at the worst points of Alts D, E, E1, F, F1 now need sand (0.86-0.99; E15/F15 already did; Alt A 1.04 still passes) (L4 divider credit lost) - covered by the existing rule: sand mandatory on wet grades/curves, auto-sand on slip"
# (3) pump input shaft
_T_cont = 35000 / (2 * math.pi * 2200 / 60) + 26 * 25 / (20 * math.pi) / 0.85     # 35 kW at 2,200 rpm (anti-stall low end) + charge pump 26 cc at 25 bar ASSUMED
_T_eng = 265.0
_T_hyd = 42 * P_STR / (20 * math.pi) / 0.95
SH = {"G1 ISO 3019-1 32-4 14T 12/24 (SAE C spline)": (534, 592), "G4 22-4 13T 16/32 (SAE B)": (180, 222), "G5 25-4 15T 16/32 (SAE B-B)": (277, 370)}
J["pump_shaft"] = dict(source="Danfoss H1P 045/053 Technical Information BC152886483105en (shaft options, rated/max torque); AIE V3307-CR-TIE4 package quote 74419: 'SAE B 13T pump drive', engine 265 N.m peak (tender/design_basis.md)",
    T_continuous_Nm=round(_T_cont, 1), T_engine_peak_Nm=_T_eng, T_hydraulic_42cc_400bar_Nm=round(_T_hyd, 1), T_hydraulic_42cc_HPRV_Nm=round(_T_hyd, 1), T_unlimited_HPRV_53cc_Nm=round(P_STR * 53.8 / (20 * math.pi) / 0.93, 1),
    options={k: dict(rated_Nm=v[0], max_Nm=v[1], util_cont=round(_T_cont / v[0], 2), util_peak=round(_T_eng / v[1], 2), ok=_T_cont <= v[0] and _T_eng <= v[1]) for k, v in SH.items()},
    finding="The AIE SAE B 13T drive mates ONLY shaft G4 (13T 16/32), and G4 FAILS: engine peak 265 > 222 N.m max (1.19). G1 (the L4 pick) does NOT fit a 13T female drive as quoted.",
    decision="KEEP H1P053 shaft G1 (14T 12/24, SAE B 2-bolt flange unchanged); the ENGINE-SIDE pump-drive coupling hub must be bored/broached 14T 12/24 (SAE C spline) for the SAE B pad - spline engagement >= 48 mm. Alternate if AIE cannot: shaft G5 (15T 16/32 SAE B-B, max 370, util 0.72) with a 15T coupling hub.",
    held="AIE confirmation of the 14T 12/24 coupling hub on the SAE B pad = HELD vendor ask (no contact; quote extension NOT re-raised)")
# (4) loco valves (T04 release + tow)
J["loco_valves"] = dict(
    T04_release=dict(parts=["Low-pressure selector (shuttle) on the loop A/B -> takes the LOW side (= charge 12-30 bar)", "Check valve -> diaphragm accumulator 0.75 L, 210 bar class, N2 pre-charge ~8 bar (HYDAC SBO-class or equal)",
                             "Pressure-reducing/relief valve set 28 bar (protects the T04 seal; release 12-30 bar)", "3-way 2-position solenoid valve, cartridge (HydraForce SV08/SV10-30 class or equal), DE-ENERGIZED = brake port vented to case/tank = BRAKES APPLIED (fail-safe)",
                             "Pressure switch on the brake line (release confirmed -> PLUS+1 traction enable)", "All on the loco valve block (Y+ side, away from DBK-1); one pilot line per truck to 2 MS05 brake ports"],
                      function="PLUS+1 energizes the solenoid to release; park command or < 0.5 mph -> de-energize -> apply. Engine stall at speed: the accumulator holds release ~30 s so the T04 is not used dynamically (catalog: max 10 dynamic uses); train air brakes stop the train",
                      volume="T04 release volume per motor = AWAIT Poclain; 0.75 L sized on 4 x ~0.1 L + leakage allowance (ASSUMED)", hose_across_DBK1="none - all on the loco"),
    tow=dict(parts=["Lockable manual tow valve: 2-way high-pressure ball valve >= 420 bar WORKING (L4.2: it sits on LOOP pressure - the HYDAC KHB3K DN25 at 310 bar is NOT acceptable; use a HYDAC KHB3K DN06-class 500 bar ball valve, sized for the 2 mph tow flow, L42 tow_valve_DN06), across loop A-B on the loco manifold, normally CLOSED, padlock + limit switch to PLUS+1 (traction inhibit when open)",
                    "MS05 freewheel: per Poclain (case-pressure freewheel / declutch) - AWAIT Poclain for the procedure; T04 manual release screws (M12)"],
             rule="Tow max 2 mph; H1P053 HPRV bypass (back out both HPRV plugs 3 turns, 22 mm hex, re-seat 70 N.m) is for short moves only (Danfoss: HPRVs are not tow valves, <= 20 % max speed, <= 3 min)"),
    mass_kg="in LB 28 kg package")
# (5) spline engagement (detail in l4_addenda.json spline_W55x3x17)
J["spline_engagement"] = dict(L4_assumed_mm=70, L41_basis_mm=60, required_min_mm=58, rule="engage the FULL code-5 spline length; hub face to shaft shoulder <= 2 mm; end plate", ref="l4_addenda.json spline_W55x3x17")
# (6) interfaces recorded (Loco Bot L-114 rev E3)
J["interfaces_L41"] = dict(DBK1="DBK-1 hydraulic dry-break + air zone on the loco LEFT: X10900-11300, Y-220 to -600, Z700-1100 (PROPOSAL, L-114 rev E3); no hydraulics at Y > -200 or above Z1100",
                           jumpers="Electric jumpers on the loco RIGHT: JL-E Y+500 to +1100, Z1700-2200 (L-114 rev E3)",
                           glad_hands_JL_A="Air glad hands on the REAR SILL per JL-A (L-114 rev E3): BP Y-650, WH (whistle - NEW glad hand) Y-800, MR Y-950, all at Z1950",
                           dry_breaks="DBK-1 hydraulic dry-breaks Y-220 to -600, Z700-1100 (loco left, X10900-11300)", AW1="AW-1 whistle air line 1/2 in",
                           HL1="HL-1 headlamp X175 Y0 Z3495 on 109-SBX-7 rev B (A36 PL6, 8.0 kg per S-504) - both in the K2-a ledger")
# ------------------------------------------------------------------ envelope (model)
try:
    import sys; sys.path.insert(0, "/workspace/train/build"); import model
    J["envelope"] = model.l4_envelope_check()
except Exception as e:
    J["envelope"] = dict(error=str(e))
J["options_note"] = "Ranking (no-belt study): chain (this rev) > L3 gearbox + belt (fallback, calcs/L3) > short H1B080 special > custom L2 > right-angle gearbox."
J["loco_valves"]["T04_release"] = dict(superseded_by="T04_release_L41", summary="LP shuttle (loop A/B) -> 10 um filter -> 3-way reducing/relieving valve 20 bar -> normally-vented 3/2 solenoid -> choke Ø2.4 + 1.0 L damping accumulator -> brake-line shuttle -> 4 T04; manual-release branch 6.0 L accumulator + hand pump + guarded valve; loss of loop/charge APPLIES the T04; no 4th dry-break")
J["brake"]["MS05_release"] = "L4.2: T04 release fed from the H1 CHARGE circuit (M3) - see J[L42][T04_charge_feed]; [L4.1 was: release from the loco's own loop (LP shuttle + 20 bar reducing valve + normally-vented solenoid); loss of loop/charge or 24 V applies the T04 through the choke after the BP vents; manual release from a 6.0 L accumulator + hand pump via a guarded valve"
json.dump(J, open(os.environ.get("DRIVE_OUT", "/workspace/train/calcs/L4/drive_L4.json"), "w"), indent=1, ensure_ascii=False)
if __name__ == "__main__":
    for k in ("basis", "start", "speed", "power_speed", "hotday", "chain", "motor_bearing", "axle", "axlebox", "bracket", "brake", "envelope"):
        print("==", k); print(json.dumps(J[k], ensure_ascii=False)[:2500])

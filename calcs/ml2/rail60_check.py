"""ML-2 rail section check on ASCE 60 lb (section 6040), replacing ASCE 40 in the old PE package (track_structure/track_calc.py
BOEF method, unchanged): P_design = DF 2.0 x Q_basis 26 kN, E 29e6 psi, ties @ 22.5 in, u = 1000/1500/3000 psi, adjacent-axle
superposition at the 1550 mm driver-truck wheelbase. Section properties (cited): Kimes Steel drawing RAIL-ASCE-60LB sec. 6040
(A 5.93 in2, I 14.56 in4, Zhead 6.62, Zbase 7.10 in3) https://www.kimessteel.com/shop/new-rail-60-lb-asce-piece-1018/document/38 ;
cross-check Tedrail ASTM A1 table (ASCE40 I 6.54 / Zb 3.89 / Zh 3.59; ASCE60 I 14.56 / Zb 7.10 / Zh 6.62)
https://www.tedrail.com/products/classify/ASTM%20A1%20STANDARDARD%20STEEL%20RAIL . Worn case: 6 mm vertical head wear (condemn limit,
used_60lb_rail_QA.md) with I/Zb/Zh ratios from track_structure/used_rail_qa/wear_check.json. Head width 2-3/8 in moves the tie
seat lever (gc). NOT PE-reviewed; calculated only, nothing tested."""
import math, json
kN2lb = 224.809; IN = 25.4; E = 29e6; s = 22.5; DF = 2.0; Qb = 26.0
WC = json.load(open('/workspace/track_structure/used_rail_qa/wear_check.json'))['cases']
w6 = [c for c in WC.values() if c['vertical_wear_mm'] == 6.0 and c['side_wear_mm'] == 0][0]['ratios']
L = json.load(open('/workspace/gh_site/data/mass_ledger.json'))
K2A = json.load(open('/workspace/loco/ml2/ml2_starts.json'))
Q = dict(loco_driver_static_max=round(max(K2A['static_axles_kN'].values()) / 2, 2), loco_driver_dynamic_target=26.5,
         coach_max=round(16.6 - L['coaches']['regular']['wheel_max_margin_to_16p6kN_N'] / 1000, 2),
         tender_nominal=round(L['tender']['mass_kg'] * 9.81 / 8 / 1000, 2), basis=Qb)
SEC = {'ASCE 40 (old PE basis)': dict(I=6.54, Zb=3.89, Zh=3.59, head=1.875),
       'ASCE 60 new': dict(I=14.56, Zb=7.10, Zh=6.62, head=2.375),
       'ASCE 60 worn 6 mm (condemn)': dict(I=14.56 * w6['I'], Zb=7.10 * w6['Zb'], Zh=6.62 * w6['Zh'], head=2.375)}
Pd = DF * Qb * kN2lb; rows = []
for u in (1000, 1500, 3000):
    for nm, p in SEC.items():
        beta = (u / (4 * E * p['I'])) ** 0.25; x = 1550 / IN
        muM = math.exp(-beta * x) * (math.cos(beta * x) - math.sin(beta * x)); muY = math.exp(-beta * x) * (math.cos(beta * x) + math.sin(beta * x))
        M = Pd / (4 * beta) * (1 + max(muM, 0)); y = Pd * beta / (2 * u) * (1 + muY); q = Pd * beta * s / 2 * (1 + muY)
        rows.append(dict(u_psi=u, rail=nm, M_lbin=round(M), base_MPa=round(M / p['Zb'] * 0.006895, 1), head_MPa=round(M / p['Zh'] * 0.006895, 1),
                         defl_in=round(y, 3), seat_lb=round(q)))
ALLOW = 172.0
gov = {nm: max(r['base_MPa'] for r in rows if r['rail'] == nm) for nm in SEC}
# tie / ballast at the governing seat load (track_calc method, 6x8x72 tie, A_eff = 2/3 tie area per rail)
tie = {}
for nm, p in SEC.items():
    q = max(r['seat_lb'] for r in rows if r['rail'] == nm); A_eff = 72 * 8 * 2 / 3; gc = 36 + p['head']; a = (72 - gc) / 2; w = 2 * q / 72
    tie[nm] = dict(seat_lb=q, ballast_psi=round(2 * q / A_eff, 1), plate_psi_6x9=round(q / 54), tie_seat_bending_psi=round(w * a * a / 2 / (8 * 36 / 6)))
OUT = dict(rev='ML-2 2026-11-02', method=__doc__.split('\n')[0], wheel_loads_kN=Q, P_design_kN=DF * Qb, allow_base_MPa=ALLOW, rows=rows,
           governing_base_MPa=gov, margin_MPa={k: round(ALLOW - v, 1) for k, v in gov.items()}, PASS={k: v <= ALLOW for k, v in gov.items()}, tie=tie,
           basis_check=dict(Q_basis_covers_max_dynamic_driver=Qb >= Q['loco_driver_dynamic_target'], margin_kN=round(Qb - Q['loco_driver_dynamic_target'], 2)),
           at_27kN_static_limit={k: dict(base_MPa=round(v*27/26,1), margin_MPa=round(ALLOW-v*27/26,1)) for k, v in gov.items()},
           sources=['https://www.kimessteel.com/shop/new-rail-60-lb-asce-piece-1018/document/38', 'https://www.tedrail.com/products/classify/ASTM%20A1%20STANDARDARD%20STEEL%20RAIL'])
json.dump(OUT, open('rail60_check.json', 'w'), indent=1); print(json.dumps(dict(gov=gov, margin=OUT['margin_MPa'], Q=Q, tie=tie), indent=1))

"""ML-2 NO-SAND start re-run (Loco/Stress method of record, NOT PE-reviewed). Runs a COPY of loco/k2a/k2a_L42R.py with the
sand-delete rows (sand_delete/sd_k2a.py whatif) + ML-2 rows (PX-1 +2.1 kg, KES-3 +0.06 kg) and tender 8,993.3 kg TB-3.15e,
into loco/ml2/run only. Then: no-sand wet/dry start caps (self-consistent equal-torque cap incl. weight transfer + centre-plate h_eff,
Grokky drive_L4 _cap_f) vs need = (0.0208 + grade) x W, W = ML-2 ledger train (loaded) + 1 x 90 kg crew."""
import json, re, sys, io, contextlib
HERE = '/workspace/loco/ml2/run'; g = 9.81
src = open('/workspace/loco/k2a/k2a_L42R.py').read().replace("HERE = '/workspace/loco/k2a'", f"HERE = '{HERE}'")
src = src.replace("TENDER_KG, TENDER_CG = 8951.7, [2440.5, 10.0, 1103.1]", "TENDER_KG, TENDER_CG = 8993.3, [2437.8, 10.0, 1099.8]  # ML-2: TB-3.15e (owner ruling)")
assert "8993.3" in src and f"HERE = '{HERE}'" in src
sd = open('/workspace/loco/sand_delete/sd_k2a.py').read()
SAND = eval(sd[sd.index('SAND = [') + 7: sd.index(']\nif mode') + 1])
ML2 = [("ML2-PX1 PX-1 package +2.1 kg (owner ruling) @X5675 (PX-1/BSC-1 location, LOCO_BASIS frozen run)", 2.1, 5675.0, 'body'),
       ("ML2-KES3 KES-3 Finder 7S relay + F-KES3 fuse @X10550", 0.06, 10550.0, 'body')]
src = src.replace("EX += R26_ROWS\n", "EX += R26_ROWS\nEX += SAND_DEL\nEX += ML2_ROWS\n", 1); assert "EX += ML2_ROWS" in src
G = {'__name__': '__main__', 'SAND_DEL': SAND, 'ML2_ROWS': ML2}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src, 'k2a_ml2', 'exec'), G)
DV, axF, dloco = G['DV'], G['axF'], G['dloco']
L = json.load(open('/workspace/gh_site/data/mass_ledger.json'))
M_train = L['train_totals']['train_loaded_kg']; LOCO = L['loco']['mass_kg']; CREW = 90.0
Wt = (M_train + CREW) * g / 1000
MU = dict(DRY=0.25, S0_wet=0.15, S3=0.10, S4_S2=0.085, S5=0.05)   # Stress no_sand mu cases (ns_run.py)
GR = dict(level=0.0, R80_eff_0p88=0.0088)
out = dict(loco_kg_k2a=round(G['F']['loco_kg'], 2), loco_kg_ledger=LOCO, train_kg=M_train, crew_kg=CREW, W_kN=round(Wt, 2),
           static_axles_kN={k: round(v, 3) for k, v in axF.items()}, cases={})
with G['ctx'](axF, dloco):
    DV['m_train_'] = M_train + CREW; DV['loco_kg_'] = LOCO + CREW
    for d, dn in ((1, 'fwd'), (-1, 'rev')):
        for mk, mu in MU.items():
            cap = DV['_cap_f'](d, G['MU'], mu)
            row = dict(mu=mu, cap_kN=round(cap, 2), max_start_grade_pct=round((cap / Wt - 0.0208) * 100, 2))
            for gk, gr in GR.items():
                need = (0.0208 + gr) * Wt
                row[gk] = dict(need_kN=round(need, 2), margin_kN=round(cap - need, 2), ratio=round(cap / need, 3), PASS=cap >= need)
            out['cases'][f'{dn}_{mk}'] = row
        # mu required to start (bisection)
        for gk, gr in GR.items():
            lo, hi = 0.01, 0.4; need = (0.0208 + gr) * Wt
            for _ in range(40):
                m = (lo + hi) / 2; lo, hi = (m, hi) if DV['_cap_f'](d, G['MU'], m) < need else (lo, m)
            out.setdefault('mu_required', {})[f'{dn}_{gk}'] = round(hi, 4)
    fw = DV['_fac_drv']; out['worn_drivers_factor'] = fw
    for d, dn in ((1, 'fwd'), (-1, 'rev')):
        for mk, mu in MU.items():
            out['cases'][f'{dn}_{mk}']['cap_worn_kN'] = round(DV['_cap_f'](d, G['MU'], mu, fac=fw), 2)
# Stress no_sand method of record (ns_run.py): equal-torque cap = 4 mu min(static axle), no transfer
mn = min(axF.values()); out['stress_static_method'] = {}
for mk, mu in MU.items():
    cap = 4 * mu * mn; out['stress_static_method'][mk] = dict(cap_kN=round(cap, 2), **{gk: dict(need_kN=round((0.0208+gr)*Wt, 2), margin_kN=round(cap-(0.0208+gr)*Wt, 2), ratio=round(cap/((0.0208+gr)*Wt), 3)) for gk, gr in GR.items()})
out['released_pull_limits_kN'] = dict(fwd=G['F']['TE_lim_fwd_kN'], rev=G['F']['TE_lim_rev_kN'])
out['released_pull_limits_E12_COST2_kN'] = dict(fwd=32.8, rev=30.1)
# reverse full-train start limit with the k2a 1.10 margin: TE_avail = min(cap, released rev pull limit 30.1)
out['reverse_start_limit_pct'] = {mk: dict(new=round((min(out['cases']['rev_'+mk]['cap_kN'],30.1)/1.10/Wt-0.0208)*100, 2), worn=round((min(out['cases']['rev_'+mk]['cap_worn_kN'],30.1)/1.10/Wt-0.0208)*100, 2)) for mk in MU}
json.dump(out, open('/workspace/loco/ml2/ml2_starts.json', 'w'), indent=1); print(json.dumps(out, indent=1))

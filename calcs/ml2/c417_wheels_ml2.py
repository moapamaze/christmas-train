"""F7 r5 (C4.12 FINAL as booked): wheel loads with COPIES (r5/build_copy/), band-edge sensitivities. Write guard: nothing outside r5/. NOT PE-reviewed."""
import os, sys, io, json, builtins, contextlib, copy
HERE = os.path.dirname(os.path.abspath(__file__)); sys.dont_write_bytecode = True
_open = builtins.open
def _guard(f, mode='r', *a, **k):
    if any(c in mode for c in 'wax+') and not os.path.abspath(str(f)).startswith(HERE+'/c417'): raise PermissionError(f'write blocked: {f}')
    return _open(f, mode, *a, **k)
builtins.open = _guard
BC = '/workspace/coach_package/build'; sys.path.insert(0, BC); C = '/workspace/coach_package/calcs/'
FLAGS = dict(C45_F5=1, C45_SCP13=1, C46_F6=1, C47_F7=1, C48_F7R2=1, C48_F7R2B=1, C49_F7R3=1, C410_F7R4=1, C410_F7R4B=1)
def load(heavy, light, r5=1, r5f=1):
    src = open(BC + '/c42_calc.py').read().replace('/workspace/coach_package/notes/mass_fitout.json', heavy).replace('/workspace/coach_package/calcs/c42_mass_light255.json', light)
    src = src[:src.index('# ---- wheel loads + summer cap')]
    for k, v in dict(FLAGS, C411_F7R5=r5, C412_F7R5F=r5f).items(): os.environ[k] = str(v)
    for m in list(sys.modules):
        if m in ('c42_items', 'hvac_R', 'fitout'): sys.modules.pop(m)
    G = {'__name__': 'x'}
    with contextlib.redirect_stdout(io.StringIO()): exec(compile(src, 'c42_calc.py', 'exec'), G)
    return G
LIM = 16.6
def run(G, MFsel):
    H = G[MFsel]; KEY = G['KEY']
    def wmax(ty, extra=()):
        MF = copy.deepcopy(H); key = KEY[ty]; acc = ty != 'regular'
        MF[key + '_loaded_kg'] += sum(e[1] for e in extra)
        base = G['C42'].ITEMS[:]
        try:
            G['C42'].ITEMS += [e + (('A' if acc else 'R'),) for e in extra]
            return G['placed'](ty, MF, True, 37.5)[0]
        finally:
            G['C42'].ITEMS[:] = base
    return H, KEY, wmax

G = load(C + 'c411_F7r5_mass_heavy.json', C + 'c411_F7r5_mass_light255.json'); H, KEY, wmax = run(G, 'HEAVY')
fix_R=[('d',2.31,1150.0,y,650.0) for y in (813.0,-813.0)]*1
O={}
for ty in KEY:
    acc = ty!='regular'
    dbl=[('d',2.31,x,y,650.0) for x in (1150.0,9010.0) for y in (813.0,-813.0)]
    ret=[('r',0.3,x,1380.0,1830.0) for x in (595.0,9565.0)]
    r5a=[('a',-5.0,1883.0,1396.0,800.0)] if acc else []
    # ML-2: S1-end lug +0.3 kg per non-boarding opening (C4.16 s5: X1123-1143, Y1372-1396; Z not defined -> 1300 ASSUMED, no static effect)
    lug=[('l',0.3,x,y,1300.0) for x in (1133.0,10160.0-1133.0) for y in ((1384.0,-1384.0) if acc else (1384.0,))]
    base=max(wmax(ty).values()); b5=max(wmax(ty,dbl+ret+r5a).values()); m2=max(wmax(ty,dbl+ret+r5a+lug).values())
    O[ty]=dict(r5=round((LIM-base)*1000), r5b=round((LIM-b5)*1000), ml2_with_lugs=round((LIM-m2)*1000), lug_count=len(lug), lug_kg=round(0.3*len(lug),2))
json.dump(O,open(HERE+'/c417_wheels_ml2.json','w')); print(O)

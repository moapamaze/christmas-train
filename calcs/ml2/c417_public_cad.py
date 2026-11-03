"""ML-2 public CAD regeneration (2026-11-02). Coaches = L3 ref coach (l3_ref/build/model.py) + SCP-04/05 (fitout.apply_scp04_05)
+ C4.12 F7 r5 final additions (c412_cad.parts, unchanged source) + F7 r5b changes from coach_package/notes/c415_F7r5b_notes.md
and c416_F7r5b_addendum.md: (1) PL3/8 x 6 x 8 doublers 4/coach at X1150/X9010 on the main-rail inboard face Y+-813, Z650
(203 along X, 152 along Z, 9.5 thick); (2) mid bar +10 mm Y (CL Y1390, outer face Y1411) with its saddles; (3) S1-end saddle replaced
by the fixed end-wall lug X1123-1143 Y1372-1396 (Z band taken from the saddle it replaces - ASSUMED, not in the notes).
Not modelled (no geometry in source): r5b lanyard hitch-pin retainers, the removable lug socket on the mid bar. Interiors not included
(public model). Loco + tender = renders_work/model.py primitive model (unchanged; sand already absent, dome cosmetic only).
Outputs to coach_package/cad_ml2/ only. NOT PE-reviewed."""
import sys, importlib.util, copy
sys.path.insert(0, '/workspace/coach_package/l3_ref/build'); sys.path.insert(0, '/workspace/coach_package/build')
import cadquery as cq
from build_cad import build, F
from model import coach
spec = importlib.util.spec_from_file_location('rw_model', '/workspace/renders_work/model.py'); RW = importlib.util.module_from_spec(spec); spec.loader.exec_module(RW)
src = open('/workspace/coach_package/build/c412_cad.py').read(); src = src[:src.index('\nfor name, acc in ((')]
G = {'__name__': 'c412'}; exec(compile(src, 'c412_cad.py', 'exec'), G); parts, bx = G['parts'], G['bx']
OUT = '/workspace/coach_package/cad_ml2/'
def r5b(add):
    out = []
    for q in add:
        n = q['name']
        if n.startswith('C4.11 stock MID bar') or n.startswith('C4.11 mid-bar stock gravity lift-off saddle'):
            q = dict(q); sy = 1 if q['y0'] > 0 else -1
            if n.startswith('C4.11 mid-bar stock'):
                a_end = q['x0'] < 5000
                s1 = (a_end and q['x0'] > 1000) or ((not a_end) and q['x0'] < 9100)   # S1 (end-wall) side saddle
                if s1:
                    x0, x1 = (1123.0, 1143.0) if a_end else (10160.0 - 1143.0, 10160.0 - 1123.0)
                    out.append(bx(x0, x1, sy*1372.0, sy*1396.0, q['z0'], q['z1'], f"F7r5b S1-END LUG flat bar on the end-wall corner member X{x0:.0f}-{x1:.0f} Y{sy*1372:+.0f}..{sy*1396:+.0f} (Z band of the replaced saddle - ASSUMED), 6 mm fillet; member TBC in CAD; replaces the S1-end saddle; 0.3 kg (ML-2)"))
                    continue
            q['y0'] += 10.0 * sy; q['y1'] += 10.0 * sy; q['name'] = 'F7r5b +10 mm Y (CL Y1390, outer face Y1411) - ' + n
        out.append(q)
    for x in (1150.0, 9010.0):
        for sy in (1, -1):
            out.append(bx(x - 101.5, x + 101.5, sy*803.7, sy*813.2, 650 - 76.0, 650 + 76.0, f"F7r5b knee-brace node DOUBLER PL3/8 x 6 x 8 (2.31 kg) main-rail inboard face X{x:.0f} Y{sy*813:+.0f} Z650, 6 mm fillet all round to the rail, brace-to-doubler 8 mm"))
    return out
def coach_ml2(acc):
    car = [q for q in F.apply_scp04_05(coach(acc)) if not str(q.get('name', '')).startswith('SCP-03 PROPOSED bridge receiver')]
    return car, r5b(parts(acc))
def save(name, prims, ff=0):
    a, m = build(name, prims, ff); a.save(OUT + name + '.step'); a.save(OUT + name + '.glb'); print(name, len(prims), flush=True); return a
def shift(prims, dx): return RW.shift(prims, dx=dx)
if __name__ == '__main__':
    reg, ra = coach_ml2(False); acc, aa = coach_ml2(True)
    save('PF-C300_coach_regular', reg + ra, len(reg)); save('PF-C300A_coach_accessible', acc + aa, len(acc))
    uf = [q for q in reg if q['grp'] in ('frame', 'coupler', 'deck')] + [q for q in ra if any(k in q['name'] for k in ('KNEE BRACE', 'DOUBLER', 'CH-3', 'diaphragm'))]
    save('PF-C310_coach_underframe', uf)
    full = cq.Assembly(name='PF-A000_train')
    for lab, prims, xo in RW.consist():
        if lab.startswith('Coach'):
            c, ad = (acc, aa) if 'accessible' in lab else (reg, ra); prims = c + ad
        a, m = build(lab, shift(prims, xo)); full.add(a, name=lab)
    a, m = build('couplers', RW.couplers()); full.add(a, name='couplers')
    full.save(OUT + 'PF-A000_train_assembly.step'); full.save(OUT + 'PF-A000_train_assembly.glb'); print('PF-A000 done', flush=True)

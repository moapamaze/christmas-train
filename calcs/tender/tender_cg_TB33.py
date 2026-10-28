"""Tender TB-3.4 (file name kept) CG and axle / wheel loads on the REAL T2 structure CG (Steering 15, 28 Oct 2026).
Structure masses = T2 ledger (calcs/tender_mass_T2.json); structure CGs = volume centroids of the model primitives (build/model.py tender()).
Placed equipment = Tender Bot TB-3.2 aggregate (1,981.5 kg at [2211, +40, 1513]) with the 100 kg placeholder replaced by the
TB-3.3 under-deck assembly 154.4 kg at [2524, 32, 648] and the 1/0 start cable 1.7 kg. Remainder to 8,451 kg = unplaced items (ASSUMED at the bay centroid).
Coordinates: X from the tender front pin (pivots X1200 / 3800), Y + right, Z above top of rail."""
import sys, json, math
sys.path.insert(0, '/workspace/train/build')
from model import tender, GAUGE
P = tender()
def vol_c(p):
    if p['t'] == 'B':
        dx, dy, dz = p['x1']-p['x0'], p['y1']-p['y0'], p['z1']-p['z0']; v = dx*dy*dz
        if p.get('hss'):
            ax, t = p['hss']; ix, iy, iz = dx-2*t, dy-2*t, dz-2*t
            if ax == 'x': ix = dx
            if ax == 'y': iy = dy
            if ax == 'z': iz = dz
            if ix > 0 and iy > 0 and iz > 0: v -= ix*iy*iz
        return v, ((p['x0']+p['x1'])/2, (p['y0']+p['y1'])/2, (p['z0']+p['z1'])/2)
    L = p['a1']-p['a0']; v = math.pi*(p['r']**2-p.get('rin', 0)**2)*L; m = (p['a0']+p['a1'])/2
    c = {'y': (p['c1'], m, p['c2']), 'x': (m, p['c1'], p['c2']), 'z': (p['c1'], p['c2'], m)}[p['axis']]
    return v, c
def cen(sel):
    V = 0; S = [0, 0, 0]
    for p in P:
        if sel(p):
            v, c = vol_c(p); V += v
            for k in range(3): S[k] += v*c[k]
    return [S[k]/V for k in range(3)]
nm = lambda p: p['name']
C = dict(
  wheel=cen(lambda p: p['grp'] == 'wheel'), axle=cen(lambda p: p['grp'] == 'axle'),
  truck=cen(lambda p: p['grp'] == 'truck'),
  frame=cen(lambda p: p['grp'] == 'frame' and 'drop box' not in nm(p) and 'PF-DB' not in nm(p) and 'pocket' not in nm(p)),
  dropbox=cen(lambda p: p['grp'] in ('frame', 'coupler', 'pin') and ('drop box' in nm(p) or 'PF-DB' in nm(p) or 'pocket' in nm(p))),
  deck=cen(lambda p: p['grp'] == 'deck'),
  skin=cen(lambda p: ('skin' in nm(p) or 'flat roof' in nm(p)) and p['grp'] in ('body', 'roof')),
  posts=cen(lambda p: ('post' in nm(p) or 'bow' in nm(p)) and p['grp'] in ('body', 'roof')),
  cover=cen(lambda p: p['grp'] == 'trim'),
  body=cen(lambda p: p['grp'] in ('body', 'roof')))
piv = (1200.0, 3800.0)
tc = lambda z: [2500.0, 0.0, z]
T2 = json.load(open('/workspace/train/calcs/tender_mass_T2.json'))['ledger']
g = {r['item']: r['kg'] for k in ('Trucks (2)', 'Frame + deck', 'Body') for r in T2[k]}
S = [  # (item, kg, cg, basis)
 ("Wheels 8 x Ø600", g["Wheels 8 \u00d7 \u00d8600 plate-web"], C['wheel'], "T2 ledger / model centroid"),
 ("Axles 4 x Ø110", g["Axles 4 \u00d7 \u00d8110"], C['axle'], "T2 ledger / model centroid"),
 ("Truck frames, axleboxes, centre plates", g["Truck frames, axleboxes, centre plates"], C['truck'], "T2 ledger / model centroid"),
 ("Springs, discs, calipers, spring-brake chambers", 300, tc(450), "ASSUMED at the truck centres, Z450"),
 ("Main rails, crossmembers, bolsters", g["Main rails, crossmembers, fish-belly bolsters (B1)"], C['frame'], "model centroid"),
 ("PF-DB drop boxes and pockets", g["PF-DB drop boxes and pockets"], C['dropbox'], "model centroid"),
 ("Deck plate + cross-bearers", g["Deck 6 mm tread plate + 7 C6x8.2 cross-bearers (D1)"], C['deck'], "model centroid"),
 ("Deck pattern, clips, welds", 35.8, C['deck'], "ASSUMED at deck centroid"),
 ("Skin 10 ga sides, ends, roof", 753.0, C['skin'], "model centroid"),
 ("Posts + roof bows", 284.0, C['posts'], "model centroid"),
 ("Door frames, bolts, clips", 40, C['body'], "ASSUMED at body centroid"),
 ("Lining 50 mm + liner", 275.0, C['skin'], "ASSUMED at skin centroid"),
 ("Coal-effect cover", 126.5, C['cover'], "model centroid"),
 ("Cover supports, coating, trim", 40, C['cover'], "ASSUMED at cover centroid"),
 ("Doors, hinges, latches, paint", 100, C['body'], "ASSUMED at body centroid"),
]
# truck items: the model centroid of both trucks is mid-pivots by symmetry -> correct for mass, but the axle split needs the per-truck share
E0 = (1981.5, [2211, 40, 1513])
E = [("Placed equipment TB-3.2 (Tender Bot, incl. 100 kg transformer placeholder)", E0[0], E0[1], "Tender Bot TB-3.2"),
     ("less transformer placeholder", -100.0, [2500, 0, 670], "TB-3.2"),
     ("Under-deck transformer assembly TB-3.4 (Acme T2535173S, isolators, bolted cradle + box rails, 3 mm shield 450 x 1,120, inrush limiter on the cradle)", 168.7, [2502, 24, 608], "Tender Bot TB-3.4 (Steering 16)"),
     ("1/0 start cable 2 x 1.5 m", 1.7, [2900, 725, 1240], "Tender Bot TB-3.3 (location ASSUMED)")]
TOTAL = 8465.3   # TB-3.4 (Steering 16)
ms = sum(r[1] for r in S); me = sum(r[1] for r in E)
rem = TOTAL - ms - me
R = [("Unplaced: mounts, exhaust, ducts, hoses, cabling, fluids not in the placed list, misc. (balance to 8,465.3)", rem, [2500, 0, 1500], "ASSUMED at bay centroid, Z1500")]
rows = S + E + R
M = sum(r[1] for r in rows)
cg = [sum(r[1]*r[2][k] for r in rows)/M for k in range(3)]
# sensitivity: remainder high (Z2000) / low (Z1100)
def cgz(zrem): return (sum(r[1]*r[2][2] for r in S+E) + rem*zrem)/M
gN = 9.80665
W = M*gN/1000
Rf = W*(piv[1]-cg[0])/(piv[1]-piv[0]); Rr = W-Rf
b = 2*(GAUGE/2+33)   # lateral contact-point span ~980 mm ASSUMED (36 in gauge, 1:20 tread)
def wheels(Rt):
    ax = Rt/2; dQ = ax*cg[1]/b
    return dict(axle=round(ax, 2), right=round(ax/2+dQ, 2), left=round(ax/2-dQ, 2))
out = dict(rev="TB-3.4", date="2026-10-28", total_kg=round(M, 1), structure_kg=round(ms, 1), placed_equipment_kg=round(me, 1),
  unplaced_kg=round(rem, 1), cg_mm=[round(c, 1) for c in cg], cg_z_range_mm=[round(cgz(1100)), round(cgz(2000))],
  structure_cg_mm=[round(sum(r[1]*r[2][k] for r in S)/ms, 1) for k in range(3)],
  equipment_cg_mm=[round(sum(r[1]*r[2][k] for r in E)/me, 1) for k in range(3)],
  centroids_mm={k: [round(x, 1) for x in v] for k, v in C.items()},
  W_kN=round(W, 2), truck_kN=dict(front=round(Rf, 2), rear=round(Rr, 2)), front_share=round(Rf/W, 4),
  axle_wheel_kN=dict(front_truck=wheels(Rf), rear_truck=wheels(Rr)),
  max_wheel_kN=max(wheels(Rf)['right'], wheels(Rr)['right'], wheels(Rf)['left'], wheels(Rr)['left']),
  min_wheel_kN=min(wheels(Rf)['right'], wheels(Rr)['right'], wheels(Rf)['left'], wheels(Rr)['left']),
  uniform_wheel_kN=round(W/8, 2), rail_basis_kN=26.0,
  contact_span_mm_ASSUMED=round(b), note="Replaces the ASSUMED tender CG height 0.95 m and the uniform W/8 wheel load in the route checks. Truck pitch and spring-load sharing inside a truck are neglected (equal axles per truck).",
  rows=[dict(item=r[0], kg=round(r[1], 1), cg=[round(x) for x in r[2]], basis=r[3]) for r in rows])
json.dump(out, open('/workspace/train/calcs/tender/tender_cg_TB33.json', 'w'), indent=1, ensure_ascii=False)
for k in ('total_kg', 'structure_kg', 'placed_equipment_kg', 'unplaced_kg', 'cg_mm', 'cg_z_range_mm', 'structure_cg_mm', 'equipment_cg_mm', 'W_kN', 'truck_kN', 'axle_wheel_kN', 'max_wheel_kN', 'min_wheel_kN', 'uniform_wheel_kN'):
    print(k, out[k])
print(out['centroids_mm'])

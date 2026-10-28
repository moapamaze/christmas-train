"""PF-CT R2 loco structural-body study: 4 options, checks, mass, hours, formability.
Preliminary, not for construction until PE stamped. All unit-hour rates are ASSUMED estimates."""
import json, math
g = 9.81; E = 200000.0; nu = 0.3
FY = dict(A36=250, A572=345, A500C=345)
# ---------------- R2 geometry / loads (model.py, calcs.py) ----------------
L = 10600.0; x0 = 300.0; piv = (4075.0, 7275.0); a_f = piv[0]-x0; a_r = x0+L-piv[1]
m_sprung = 8439.0; w = m_sprung*g/L                       # N/mm, both sides
M_ovh = w*max(a_f, a_r)**2/2                              # N.mm static
M_v = 2.0*M_ovh                                           # x2.0 vertical (R2 C4 basis)
dM_fat = 0.6*M_ovh                                        # +/-0.3 g range (ASSUMED)
R_rear = m_sprung*g*0.5                                   # approx bolster reaction
V_v = 2.0*R_rear
F_s, F_u = 70e3, 200e3; z_cpl = 550.0
m_loco_R2 = 16810.0; m_ballast_R2 = 1500.0
T_jack = (m_loco_R2*g/4)*2200.0                            # 3-point jacking twist (accidental)
R_shell = 820.0; L_shell = 7400.0; A_shell = math.pi*2*R_shell*L_shell/1e6  # m2
A_cab = 22.0; A_skirt = 12.7
rho = 7.85e-6  # kg/mm3
def tube_mass(t): return math.pi*2*R_shell*L_shell*t*rho
res = {}
# ---------------- Option C (R2 conventional) ----------------
S_rail = 617237.0; A_rail = 7786.0
sC = M_v/(2*S_rail)
zNA_C = 1497.5
sC_u = F_u/(2*A_rail) + F_u*(zNA_C-z_cpl)/(2*S_rail)*0.5 + 0  # drop box spreads into both rails; R2 C4b carried as reported
F_c = T_jack/1700.0; M_tw = F_c*3200/4
res["C"] = dict(
  name="C  R2 conventional: HSS12x6 frame + 3 mm cosmetic body",
  bend=sC/1e0, bend_allow=0.6*345, draw_s=116.8, draw_u=225.0, draw_allow_u=345,
  torsion=M_tw/S_rail, buckling="n/a (cosmetic 3 mm skin; oil-canning only)",
  fat_range=0.6*M_ovh/(2*S_rail), fat_cat="E (crossmember/gusset fillet attachments >100 mm on HSS wall), CAFT 31 MPa",
)
res["C2"] = dict(res["C"]); res["C2"]["name"] = "C2 R2 HSS frame (unchanged) + 4.8 mm cosmetic shell bolted on flat CNC rings"
res["C2"]["buckling"] = "n/a (cosmetic 4.8 mm, bolted, R/t 171: no oil-canning)"
# ---------------- Option D (heavy plate frame + cosmetic bolted shell) ----------------
tP, hP = 20.0, 500.0; S_P = tP*hP**2/6; A_P = tP*hP
zNA_D = 1650-hP/2
sD = M_v/(2*S_P)
sD_u = F_u/(2*A_P) + F_u*(zNA_D-z_cpl)/(2*S_P) + 1.3*M_ovh/(2*S_P)
sD_s = F_s/(2*A_P) + F_s*(zNA_D-z_cpl)/(2*S_P) + 1.3*M_ovh/(2*S_P)
res["D"] = dict(
  name="D  Heavy plate frame (2 x PL20x500 A572-50) + 4.8 mm cosmetic shell bolted on flat CNC rings",
  bend=sD, bend_allow=0.6*345, draw_s=sD_s, draw_u=sD_u, draw_allow_u=345,
  torsion=M_tw/S_P, buckling=f"web h/t = {hP/tP:.0f} (compact, no stiffeners needed)",
  fat_range=dM_fat/(2*S_P), fat_cat="C (stretcher end fillets, short attachments) - CAFT 69 MPa; few details",
)
# ---------------- Option A (full thin stressed skin) ----------------
tA = 5.0
A_t = 2*math.pi*R_shell*tA; A_deck = 2500*6.0; A_sk = 2*550*4.0
zNA_A = (A_t*2560 + A_deck*1650 + A_sk*1375)/(A_t+A_deck+A_sk)
I_A = math.pi*R_shell**3*tA + A_t*(2560-zNA_A)**2 + A_deck*(1650-zNA_A)**2 + 4.0*2*550**3/12 + A_sk*(1375-zNA_A)**2
S_A = I_A/(2560+R_shell-zNA_A); S_Abot = I_A/(zNA_A-1100)
sA = M_v/min(S_A, S_Abot)
sA_u = F_u/(A_t+A_deck+A_sk) + F_u*(zNA_A-z_cpl)/S_Abot
sig_cr_cyl = 0.605*E*tA/R_shell*0.30   # knockdown 0.30 (ASSUMED, NASA SP-8007 order)
ks = 5.34+4/(600/550)**2; tau_cr = ks*math.pi**2*E/(12*(1-nu**2))*(4/550)**2
tau_sk = (V_v/2)/(550*4)
q = T_jack/(2*math.pi*R_shell**2); tau_t = q/tA
res["A"] = dict(
  name="A  Full stressed skin: 5 mm shell + 4 mm skirts + structural cab, 13 rings, 8 stringers",
  bend=sA, bend_allow=0.6*345, draw_s=sA_u*F_s/F_u, draw_u=sA_u, draw_allow_u=345,
  torsion=tau_t, buckling=f"shell local sigma_cr {sig_cr_cyl:.0f} MPa (kd 0.30) vs bending {M_v/S_A:.0f}; skirt shear tau_cr {tau_cr:.0f} vs {tau_sk:.0f} MPa (FS {tau_cr/tau_sk:.1f}); cab door openings + hatches NOT checkable by hand -> FEA",
  fat_range=dM_fat/S_Abot, fat_cat="E/E' (stitch-welded rings/stringers, hatch doublers, Kt~3 at cut-outs) - CAFT 18-31 MPa local; needs FEA hot-spot",
  zNA=zNA_A, ecc=zNA_A-z_cpl,
)
# ---------------- Option B (hybrid: light sill + thick structural shell) ----------------
tB = 10.0
A_sill = 2*305*10 + 2*250*12; I_sill = 2*10*305**3/12 + 2*250*12*(152.5)**2
A_tB = 2*math.pi*R_shell*tB
zNA_B = (A_tB*2560 + A_sill*1497.5)/(A_tB+A_sill)
I_B = math.pi*R_shell**3*tB + A_tB*(2560-zNA_B)**2 + I_sill + A_sill*(1497.5-zNA_B)**2
S_Bbot = I_B/(zNA_B-1345)
sB = M_v/S_Bbot
sB_u = F_u/(A_tB+A_sill) + F_u*(zNA_B-z_cpl)/S_Bbot   # composite only if shear-connected (FEA)
S_sill = I_sill/152.5
sB_sill_u = F_u/A_sill + F_u*(1497.5-z_cpl)/S_sill    # if sill alone (cab zone, no shell aft of x 8000)
res["B"] = dict(
  name="B  Hybrid: light centre sill (box 250x305 PL10/PL12) + 10 mm structural rolled shell + structural cab",
  bend=sB, bend_allow=0.6*345, draw_s=sB_sill_u*F_s/F_u, draw_u=sB_sill_u, draw_allow_u=345,
  torsion=T_jack/(2*math.pi*R_shell**2)/tB, buckling=f"10 mm shell R/t {R_shell/tB:.0f}: no stiffeners; sill alone carries drawbar aft of cab front (no shell there)",
  fat_range=dM_fat/S_Bbot, fat_cat="C/D at shell-to-sill saddles and ring welds; load sharing needs FEA",
  zNA=zNA_B,
)
# ---------------- mass (kg) ----------------
mass = {
 "C": dict(frame=3815, body=1900, ballast=1500),
 "C2": dict(frame=3815, body=round(tube_mass(4.8)+13*35+130+900), ballast=None),
 "D": dict(frame=round(2*10600*hP*tP*rho + 6*150 + 1248 + 500), body=round(tube_mass(4.8)+13*35+130+900), ballast=None),
 "A": dict(frame=round(1248+2*250+700+150+400+36*5), body=round(tube_mass(5)+13*40+8*7400*5/1000+900+150), ballast=None),
 "B": dict(frame=round(10600*A_sill*rho+400+254+160+1248+360), body=round(tube_mass(10)+5*60+900+120), ballast=None),
}
struct_C = mass["C"]["frame"]+mass["C"]["body"]
for k,m in mass.items():
    s = m["frame"]+m["body"]
    if m["ballast"] is None: m["ballast"] = max(0, round(m_ballast_R2 - (s-struct_C)))
    m["struct"] = s; m["total_steel"] = s+m["ballast"]
    m["loco"] = round(m_loco_R2 + (m["total_steel"] - (struct_C+m_ballast_R2)))
# ---------------- adhesion ----------------
m_trailing = 8160 + 3*13200 + 11000 + 2200
def need(mass_t, f): return f*mass_t*g
mu_dry, mu_wet = 0.25, 0.15
m_min_dry = 0.0408*m_trailing/(mu_dry-0.0408); m_min_wet = 0.0196*m_trailing/(mu_wet-0.0196)
adh = dict(trailing=m_trailing, min_loco_dry2=round(m_min_dry), min_loco_wet_level=round(m_min_wet),
           train_R2=m_loco_R2+m_trailing, TE_2pct=round(0.0408*(m_loco_R2+m_trailing)*g/1000,2),
           TE_level=round(0.0196*(m_loco_R2+m_trailing)*g/1000,2), motor_350=31.75, motor_400=36.3)
# ---------------- fabrication hours model (ASSUMED unit rates) ----------------
U = dict(cut=0.4, cut_heavy=0.6, saw=0.4, roll_thin=3, roll_med=5, roll_heavy_coord=4, prebend=1.0, brake=0.3,
         fit_light=0.5, fit_heavy=0.9, fit_skin=2.0, weld_kg_h=1.4, weld_min=0.12, stitch=0.35,
         cjp_thin=0.8, cjp_12=1.4, vt=0.05, mt_ut=0.5)
def fillet_h(a, m_): return m_*max(U["weld_min"], 0.5*a*a*7.85e-3*1.15/U["weld_kg_h"])
def frame_h(k):
    h = dict(cut=0, form=0, fit=0, weld=0, distortion=0, finish=0, inspect=0, machine=0)
    if k=="HSS":
        h.update(cut=20*U["saw"]+31*U["cut"], fit=25*U["fit_heavy"]+26*U["fit_light"],
                 weld=fillet_h(8,30)+fillet_h(6,22)+fillet_h(10,8), distortion=6, inspect=60*U["vt"]+18*U["mt_ut"]+8, machine=16)
    if k=="PLATE":
        h.update(cut=2*3.0+26*U["cut_heavy"]+15*U["cut"], fit=2*3.0+26*U["fit_heavy"]+15*U["fit_light"],
                 weld=fillet_h(10,24)+fillet_h(8,20)+fillet_h(6,12), distortion=2, inspect=56*U["vt"]+16*U["mt_ut"]+8, machine=20)
    return h
def body_h(k):
    h = dict(cut=0, form=0, fit=0, weld=0, distortion=0, finish=0, inspect=0, machine=0)
    if k=="COS3":
        h.update(cut=90*U["cut"]*0.6, form=4*U["roll_thin"]+4*U["prebend"]+30*U["brake"], fit=120*U["fit_light"]+8*U["fit_skin"],
                 weld=120*U["stitch"]*0.8+4*5.15*U["cjp_thin"]*0.7, distortion=(A_shell+A_cab)*0.8, finish=(A_shell+A_cab)*0.6, inspect=120*U["vt"]+6)
    if k=="COS48":
        h.update(cut=60*U["cut"]*0.6+13*U["cut"], form=3*U["roll_thin"]+3*U["prebend"]+20*U["brake"],
                 fit=100*U["fit_light"]+6*U["fit_skin"]*0.6+390*0.04, weld=60*U["stitch"]*0.8+3*2.44*U["cjp_thin"],
                 distortion=A_shell*0.2+A_cab*0.5, finish=A_shell*0.3+A_cab*0.45, inspect=60*U["vt"]+6)
    return h
def add(a,b): return {k:a[k]+b[k] for k in a}
def hours(o):
    if o=="C": h = add(frame_h("HSS"), body_h("COS3"))
    elif o=="C2": h = add(frame_h("HSS"), body_h("COS48"))
    elif o=="D": h = add(frame_h("PLATE"), body_h("COS48"))
    elif o=="A":
        h = dict(cut=190*U["cut"], form=6*U["roll_thin"]+6*U["prebend"]+(39+8+36)*U["brake"]*1.3,
                 fit=20*U["fit_heavy"]+170*U["fit_light"]+16*U["fit_skin"]+24,
                 weld=33*U["cjp_thin"]+(67+59+80+60)*U["stitch"]+16*U["stitch"]*1.5+fillet_h(8,40),
                 distortion=(A_shell+A_cab+A_skirt)*1.5, finish=(A_shell+A_cab+A_skirt)*0.8,
                 inspect=370*U["vt"]+93*U["mt_ut"]+30, machine=28)
    elif o=="B":
        h = dict(cut=110*U["cut"]+20*U["cut_heavy"], form=3*U["roll_med"]+3*2+5*U["brake"]*2+16,   # rolled IN-HOUSE at CWF boiler shop (owner 27 Oct)
                 fit=40*U["fit_heavy"]+80*U["fit_light"]+3*6+24,
                 weld=(2*5.15+3*2.44)*0.9+   # boiler-shop CJP seams on rolls/positioner (0.9 h/m)
                 fillet_h(8,60)+fillet_h(6,30)+60*U["stitch"],
                 distortion=A_shell*0.2+A_cab*1.2, finish=A_shell*0.35+A_cab*0.6,
                 inspect=200*U["vt"]+58*U["mt_ut"]+20, machine=24)
    h = {k: round(v) for k,v in h.items()}; h["total"] = sum(h.values()); return h
fab = {o: hours(o) for o in ["C","C2","D","B","A"]}
# engineering / PE / FEA / County QA hours (ASSUMED estimates, ranges -> mid used)
eng = {
 "C": dict(design=(30,50), fea=(0,8), pe=(30,50), qa=(30,45), test=(0,0)),
 "C2": dict(design=(38,60), fea=(0,8), pe=(32,54), qa=(30,45), test=(0,0)),
 "D": dict(design=(50,80), fea=(8,16), pe=(30,50), qa=(25,40), test=(0,0)),
 "A": dict(design=(200,300), fea=(150,220), pe=(100,160), qa=(80,120), test=(30,50)),
 "B": dict(design=(120,180), fea=(70,110), pe=(60,100), qa=(50,80), test=(10,20)),
}
for o,e in eng.items():
    e["lo"] = sum(v[0] for v in e.values() if isinstance(v,tuple)); e["hi"] = sum(v[1] for k,v in e.items() if isinstance(v,tuple))
    e["mid"] = round((e["lo"]+e["hi"])/2)
# ---------------- shell formability (R2 shell is Ø1,640) ----------------
form = []
for t, desc in [(3.0,"10 ga / 3 mm sheet"),(4.8,"3/16 in"),(6.0,"1/4 in"),(10.0,"3/8 in"),(12.0,"1/2 in"),(20.0,"3/4 in"),(25.0,"1 in")]:
    strain = t/(2*R_shell+t)*100
    form.append(dict(t=t, desc=desc, R_over_t=round(R_shell/t), strain_pct=round(strain,2), shell_kg=round(tube_mass(t)),
                     flat_spot_mm=round(1.5*t) if t>6 else round(2*t)))
out = dict(res=res, mass=mass, adh=adh, fab=fab, eng=eng, form=form, U=U,
           loads=dict(M_ovh_kNm=M_ovh/1e6, M_v_kNm=M_v/1e6, T_jack_kNm=T_jack/1e6, V_v_kN=V_v/1e3, A_shell=A_shell),
           extra=dict(sig_cr_cyl=sig_cr_cyl, tau_cr=tau_cr, tau_sk=tau_sk, zNA_A=zNA_A, zNA_B=zNA_B, sB_comp=sB_u))
json.dump(out, open("/workspace/train/calcs/structural_body_study.json","w"), indent=1, default=float)
for k in ["C","C2","D","B","A"]:
    r = res[k]; print(k, r["name"]); print("  bend %.1f/%.0f draw s %.1f u %.1f tors %.1f fat %.1f" % (r["bend"], r["bend_allow"], r["draw_s"], r["draw_u"], r["torsion"], r["fat_range"]))
    print("  mass", mass[k]); print("  fab", fab[k]); print("  eng", eng[k]["lo"], eng[k]["hi"], eng[k]["mid"])
print(adh); print(out["loads"]); print(out["extra"])
for f in form: print(f)

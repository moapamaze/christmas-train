"""C3 preliminary equilibrium and gross elastic section screens; NOT a joint acceptance.
Units N,m; reported MPa. Reproducible with Python standard library only.
"""
import json, math, itertools
from pathlib import Path
D=Path(__file__).resolve().parent
inch=.0254; lbf=4.4482216152605; g=9.80665
mass=210; xfoot=62.5; zsole=32.25; xpost=61.25; zrail=29.503937007874015
# Candidate catalog properties, Atlas A500 table, inspected 2026-10-19.
post={'A_in2':1.19,'S_in3':.641,'I_in4':.641,'wall_nom_in':.1875,'wall_design_in':.174}
rail={'A_in2':1.54,'Sstrong_in3':1.18,'Sweak_in3':.932,'J_in4':2.05,'C_in3':1.78,'wall_design_in':.174}
loads=[]
for sx,sy,down in itertools.product((-1,1),(-1,1),(0,1.5)):
 loads.append({'case':f'inertia_x{sx:+d}_y{sy:+d}_down{down:g}g','F_N':[sx*mass*g,sy*.5*mass*g,-down*mass*g],'point_in':[72,-32,62.25],'basis':'Analyst comparison; not regulatory certification load'})
for sx in (-1,1): loads.append({'case':f'backrest_{sx:+d}','F_N':[sx*300*lbf,0,0],'point_in':[62.25,-32,67],'basis':'APTA comparison only, separate static case'})
loads.append({'case':'front_edge_450lbf','F_N':[0,0,-450*lbf],'point_in':[82,-32,50],'basis':'450lbf at conservative front-edge resultant; actual5x5patch separately defined in mechanism'})
# Transverse occupancy sensitivity: occupant CG to +/-9.5in, assembly CG stayscentered.
# The combined inertia resultant moves9.5*145/210; front/back applied loads also checked at+/-9.5in.
base_loads=list(loads)
for ld in base_loads:
 for side in (-1,1):
  q=dict(ld);q['point_in']=list(ld['point_in'])
  shift=9.5*145/mass if ld['case'].startswith('inertia') else 9.5
  q['point_in'][1]=-32+side*shift;q['case']+=f'_offset{side:+d}'
  q['basis']+='; analyst transverse offset sensitivity'
  loads.append(q)
results=[]
for ld in loads:
 fx,fy,fz=ld['F_N'];xp,yp,zp=ld['point_in']; ex=(xp-xfoot)*inch;ez=(zp-zsole)*inch
 M=[-ez*fy,ez*fx-ex*fz,ex*fy]
 ey=(yp+32)*inch
 for alpha in (0,.5,1):
  for side in (-1,1):
   # alpha: fraction of roll resolved by axial reaction couple between24in foot centres.
   # Report load delivered to foundation, not the opposite support reaction.
   w=.5+side*ey/(24*inch)
   footF=[w*fx,w*fy,w*fz+side*alpha*M[0]/(24*inch)]
   footM=[(1-alpha)*w*M[0],w*M[1],w*M[2]]
   ax=1.75*inch;ay=2*inch
   signed=[footF[2]/4 + footM[0]*y/(4*ay**2)-footM[1]*x/(4*ax**2) for x,y in itertools.product((-ax,ax),(-ay,ay))]
   # Positive denotes upward load/bolt tension; negative compression. Compression credit ignored in screen.
   ideal=max(0,footF[2])/4+abs(footM[0])/(4*ay)+abs(footM[1])/(4*ax)
   # Equal stiffness elastic group in-plane shear; no friction credit.
   J=4*(ax*ax+ay*ay)
   shear=max(math.hypot(footF[0]/4-footM[2]*y/J,footF[1]/4+footM[2]*x/J) for x,y in itertools.product((-ax,ax),(-ay,ay)))
   # Transport moments to rail centre and post base; preserve forces.
   mr=[footM[0]-(zsole-zrail)*inch*footF[1],footM[1]+(zsole-zrail)*inch*footF[0],footM[2]]
   # moment about post centre atsole datum; rearpost adds positive downward-load moment.
   mp=[footM[0],footM[1]-(xfoot-xpost)*inch*footF[2],footM[2]+(xfoot-xpost)*inch*footF[1]]
   postStress=abs(footF[2])/(post['A_in2']*inch**2)/1e6+(abs(mp[0])+abs(mp[1]))/(post['S_in3']*inch**3)/1e6
   # Point force + couple on simply-supported rail. Actual end joints must carry listed shear/torsion.
   rails=[]
   for loc,L,a in [('seat1',21,15.5),('seat2_translation66',22,10.5)]:
    L*=inch;a*=inch;b=L-a
    # Rz balances appliedFz and appliedMy (right-hand aboutY).
    Rright=(-footF[2]*a+mr[1])/L; Rleft=-footF[2]-Rright
    maxMb=max(abs(Rleft*a),abs(Rright*b))
    # LateralFy producesweak-axis bending and appliedMz.
    Qright=(-footF[1]*a-mr[2])/L;Qleft=-footF[1]-Qright
    maxMw=max(abs(Qleft*a),abs(Qright*b))
    # Both ends torsionally fixed, constantGJ. Release oneend: survivingend takesalltorque.
    Ta=mr[0]*b/L;Tb=mr[0]*a/L
    twist=abs(mr[0])*a*b/(L*77e9*rail['J_in4']*inch**4)
    tau=abs(mr[0])/(rail['C_in3']*inch**3)/1e6 # full torque, conservative over two-end split
    sigma=maxMb/(rail['Sstrong_in3']*inch**3)/1e6+maxMw/(rail['Sweak_in3']*inch**3)/1e6+abs(footF[0])/(rail['A_in2']*inch**2)/1e6
    rails.append({'seat':loc,'Rz_left_right_N':[Rleft,Rright],'Ry_left_right_N':[Qleft,Qright],'end_torque_both_fixed_Nm':[Ta,Tb],'one_end_torque_bound_Nm':abs(mr[0]),'twist_both_fixed_deg':twist*180/math.pi,'strong_bending_max_Nm':maxMb,'weak_bending_max_Nm':maxMw,'normal_stress_envelope_MPa':sigma,'full_torque_shear_MPa':tau,'von_mises_gross_bound_MPa':math.sqrt(sigma*sigma+3*tau*tau)})
   results.append({'case':ld['case'],'roll_axial_fraction':alpha,'foot_y':-32+12*side,'F_N':footF,'M_sole_Nm':footM,'M_rail_Nm':mr,'M_post_Nm':mp,'ideal_bolt_tension_no_compression_credit_N':ideal,'ideal_signed_corner_N':signed,'max_bolt_shear_N':shear,'post_gross_stress_MPa':postStress,'rails':rails})
# Geometry/gross strip screens; width explicitly assumed, not validated by plate FE.
P=max(r['ideal_bolt_tension_no_compression_credit_N'] for r in results)
plate=[]
for q in (1,1.5,2):
 for t in (.5,.625,.75,.875,1):
  for name,lever,width in [('cap_wing_to_railwall',1,2.5-.5625),('sole_from_central_front_rib',1.75,2.5-.5625)]:
   stress=6*(P*q)*(lever*inch)/((width*inch)*(t*inch)**2)/1e6
   plate.append({'path':name,'t_in':t,'effective_net_strip_width_in':width,'lever_in':lever,'assumed_amplification':q,'force_N':P*q,'elastic_strip_stress_MPa':stress,'limit':'Effective width and load sharing assumed; excludes contact, prying interaction, 2D plate yield lines, weld toe and fatigue; q is sensitivity, not verified bound'})
allrails=[r for c in results for r in c['rails']]
env={'max_ideal_bolt_tension_N':P,'max_bolt_shear_N':max(r['max_bolt_shear_N'] for r in results),'max_post_gross_stress_MPa':max(r['post_gross_stress_MPa'] for r in results),'max_rail_normal_MPa':max(r['normal_stress_envelope_MPa'] for r in allrails),'max_rail_full_torque_shear_MPa':max(r['full_torque_shear_MPa'] for r in allrails),'max_rail_von_mises_MPa':max(r['von_mises_gross_bound_MPa'] for r in allrails),'max_rail_end_vertical_abs_N':max(abs(v) for r in allrails for v in r['Rz_left_right_N']),'max_rail_end_horizontal_abs_N':max(abs(v) for r in allrails for v in r['Ry_left_right_N']),'max_rail_one_end_torque_Nm':max(r['one_end_torque_bound_Nm'] for r in allrails),'max_rail_both_fixed_twist_deg':max(r['twist_both_fixed_deg'] for r in allrails)}
checks={'case_count':len(loads),'foot_case_count':len(results),'moment_equilibrium_verified':True,'checks':[]}
# Recoverforce andmoment at24in pairedfeet for allcases/splits.
for ld in loads:
 for a in (0,.5,1):
  rows=[r for r in results if r['case']==ld['case'] and r['roll_axial_fraction']==a]
  F=[sum(r['F_N'][i] for r in rows) for i in range(3)]
  Mx=sum(r['M_sole_Nm'][0]+(r['foot_y']+32)*inch*r['F_N'][2] for r in rows)
  Mx0=(ld['point_in'][1]+32)*inch*ld['F_N'][2]-(ld['point_in'][2]-zsole)*inch*ld['F_N'][1]
  My=sum(r['M_sole_Nm'][1] for r in rows)
  Mz=sum(r['M_sole_Nm'][2]-(r['foot_y']+32)*inch*r['F_N'][0] for r in rows)
  My0=(ld['point_in'][2]-zsole)*inch*ld['F_N'][0]-(ld['point_in'][0]-xfoot)*inch*ld['F_N'][2]
  Mz0=(ld['point_in'][0]-xfoot)*inch*ld['F_N'][1]-(ld['point_in'][1]+32)*inch*ld['F_N'][0]
  assert abs(My-My0)<1e-8 and abs(Mz-Mz0)<1e-8
  for r in rows:
   for rr in r['rails']:
    L,a={'seat1':(21,15.5),'seat2_translation66':(22,10.5)}[rr['seat']]; L*=inch;a*=inch
    Rl,Rr=rr['Rz_left_right_N'];Ql,Qr=rr['Ry_left_right_N']
    assert abs(Rl+Rr+r['F_N'][2])<1e-8
    assert abs(r['M_rail_Nm'][1]-a*r['F_N'][2]-L*Rr)<1e-8
    assert abs(Ql+Qr+r['F_N'][1])<1e-8
    assert abs(r['M_rail_Nm'][2]+a*r['F_N'][1]+L*Qr)<1e-8
    assert abs(sum(rr['end_torque_both_fixed_Nm'])-r['M_rail_Nm'][0])<1e-8
  assert max(abs(F[i]-ld['F_N'][i]) for i in range(3))<1e-8
  assert abs(Mx-Mx0)<1e-8
checks['checks']=['All load-case force equilibrium','All three moment component equilibria with roll partition and transverse offset','Explicit rail vertical and lateral force, bending and torsion equilibrium residual assertions','No friction contribution assigned','No compression credit in quoted bolt tension']
out={'revision':'C3-FND-R0','status':'PRELIMINARY GEOMETRY AND DEMAND SCREEN; NOT FABRICATION RELEASE','mass_basis_kg':{'occupant':145,'assembly_allowance':65,'total':210},'foot_center_in':[62.5,-44,32.25],'second_foot_y':-20,'seat2_translation_in':[66,0,0],'post_center_x_in':61.25,'bolts':{'pattern_in':[3.5,4],'diameter_in':.5,'holes_in':.5625},'sections':{'post_2sq_3_16':post,'rail_3x2_3_16':rail},'loads':loads,'envelope':env,'foot_cases':results,'plate_sensitivity':plate,'verification':checks,'excluded':['Bolted joint contact and prying solution','Actual weld design, rail end connection and crossmember wall resistance','Post hinge bracket/stop loads and local stress concentrations','Material grade acceptance, fatigue, corrosion, fabrication tolerance','Upholstery mass and final seat mass','Crashworthiness or code compliance approval']}
(D/'foundation-screen.json').write_text(json.dumps(out,indent=2))
print(json.dumps(env,indent=2))
print('Selected plate at2.0 sensitivity:',[(x['path'],x['t_in'],round(x['elastic_strip_stress_MPa'],1)) for x in plate if ((x['path'].startswith('cap') and x['t_in']==.75) or (x['path'].startswith('sole') and x['t_in']==1)) and x['assumed_amplification']==2])

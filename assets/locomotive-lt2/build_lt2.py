"""LT2 preliminary frame and removable-skid CAD. Run from any working directory.
All solids, meshes, member schedule and dimensioned SVGs derive from this file.
No fabrication approval, final running gear, bearing fit or OEM mount is asserted.
"""
from pathlib import Path
import json,math,hashlib
import numpy as np
import cadquery as cq

P=Path(__file__).resolve().parent
def js(n,v): (P/n).write_text(json.dumps(v,indent=2)+'\n')
inch=25.4; rho=7.85e-6; gg=9.80665
params={'issue':'PF-LOCO-LT2-R0','date':'2026-10-19','units':'mm','datum':'X aft from LT1 nose; Y left; Z above rail top',
 'frame_x':[300,9500],'main_rail_y':[-850,850],'frame_top_z':1650,
 'main_section':'HSS12x6x3/8','support_x':[1200,3300,6000,8300],
 'crossmember_x':[600,1800,2400,4500,5100,7200,9000,9300],
 'joint_end_gap_each_mm':1.0,'skid_support_x':[2400,4500],'skid_runner_y':[-500,500],
 'skid_runner_x':[2280,4620],'frame_side_mount_holes':{'diameter':18,'count':8,'y_offsets_from_runner':[-70,70]},
 'skid_fastener_proposal':'Eight M16 class8.8 through bolts; final standard, length, locking and preload unresolved',
 'construction_approved':False,'provenance':'LT2 raised-frame alternative reconciles DT2 reference solids; no coach or drivetrain geometry overwritten. Support hardware and final ride height unaccepted.'}
sections={'main':{'name':'HSS12x6x3/8','h':304.8,'w':152.4,'t':9.525,'lb_ft':42.79,'I_in4':215,'S_in3':35.8},
 'cross':{'name':'HSS8x4x1/4','h':203.2,'w':101.6,'t':6.35,'lb_ft':19.02,'I_in4':42.5,'S_in3':10.6},
 'skid':{'name':'HSS4x2x1/4','h':101.6,'w':50.8,'t':6.35,'lb_ft':8.81,'I_in4':4.49,'S_in3':2.25}}
parts=[]; shapes=[]
def box(l,w,h,x,y,z):return cq.Workplane('XY').box(l,w,h).translate((x,y,z)).val()
def vertical_cyl(r,h,x,y,z):return cq.Workplane('XY').circle(r).extrude(h).translate((x,y,z-h/2)).val()
def hss(L,sec,x,y,z,axis='x'):
 a=sections[sec];d=(L,a['w'],a['h']) if axis=='x' else(a['w'],L,a['h']);t=a['t']
 inn=(L+2,a['w']-2*t,a['h']-2*t) if axis=='x' else(a['w']-2*t,L+2,a['h']-2*t)
 outer=cq.Workplane('XY').box(*d).edges('|'+axis.upper()).fillet(2*t)
 inner=cq.Workplane('XY').box(*inn).edges('|'+axis.upper()).fillet(t)
 return outer.cut(inner).translate((x,y,z)).val()
def add(id,name,group,shape,material,definition,section=None,length=None,holes=None):
 bb=shape.BoundingBox();vol=shape.Volume();mass=vol*rho
 row={'id':id,'name':name,'group':group,'material':material,'definition':definition,'length_mm':length,'section':section,'holes':holes or [],
 'bounds_mm':{'x':[bb.xmin,bb.xmax],'y':[bb.ymin,bb.ymax],'z':[bb.zmin,bb.zmax]},'volume_mm3':vol,'geometric_mass_kg':mass,
 'mass_note':'Nominal solid volume ×7850kg/m³; model uses rounded corners2t outside/t inside for HSS. Catalog mass kept separately. No weld/bolt/coating mass included.'}
 if section:row['catalog_mass_kg']=sections[section]['lb_ft']*0.45359237/0.3048*length/1000
 parts.append(row);shapes.append(shape);return row
def drilled(shape,coords,d,z,h):
 for x,y in coords:shape=shape.cut(vertical_cyl(d/2,h+4,x,y,z))
 return shape
material='ASTM A500 Grade C — preliminary material selection'
plate='ASTM A572 Grade50 plate — preliminary material selection; toughness and mill certificates required'
top=1650; mainz=top-304.8/2; gap=1700-152.4-2
for side,y in [('L',850),('R',-850)]:
 add('LT2-LR-'+side,'Continuous main side rail','main',hss(9200,'main',4900,y,mainz),material,'No main-rail splice proposed. 9,200mm nominal member length; final fit-up and cutting tolerance to release.','main',9200)
for i,x in enumerate(params['support_x']):
 add(f'LT2-B{i+1}','Body support crossmember','support',hss(gap,'main',x,0,mainz,'y'),material,'1mm nominal assembly gap each end; support loads and mating DT hardware not yet accepted.','main',gap)
 for side,y in [('L',938.9),('R',-938.9)]:
  add(f'LT2-D{i+1}-{side}','Outer rail doubler proposal','doubler',box(500,25.4,304.8,x,y,mainz),plate,'500×304.8×25.4. Outer-face reinforcement only; does not establish inner-wall punching or complete bolster load path.')
 size,t=(600,19.05) if i in [1,2] else(400,12.7)
 add(f'LT2-S{i+1}','Underside interface pad blank','pad',box(size,size,t,x,0,top-304.8-t/2),plate,f'{size}×{size}×{t}. Undrilled DT interface; footprint is a proposal, not a bearing or pivot assembly.')
for i,x in enumerate(params['crossmember_x']):
 holes=[(x,y+d)for y in [-500,500]for d in [-70,70]] if x in [2400,4500] else []
 sh=hss(gap,'cross',x,0,top-203.2/2,'y')
 if holes:sh=drilled(sh,holes,26,top-203.2/2,203.2)
 add(f'LT2-C{i+1}','Equipment/body crossmember','cross',sh,material,'203.2mm deep; mounting stations have Ø26 sleeve receiving holes through both walls. Sleeve/wall weld and local flexibility not qualified.','cross',gap,[{'x':a,'y':b,'diameter_mm':26}for a,b in holes])
# Removable skid frame; frame-side hardpoints are defined, OEM engine holes remain blank.
for side,y in [('L',500),('R',-500)]:
 add('LT2-KR-'+side,'Removable skid runner','skid',hss(2340,'skid',3450,y,1726.2),material,'Runner bottom1675.4; top1777.0. Physical model only; torsional adapter/engine mounting still DT input.','skid',2340)
for i,x in enumerate([2400,4500]):
 add(f'LT2-KC{i+1}','Skid cross tie','skid',hss(947.2,'skid',x,0,1726.2,'y'),material,'1mm end gaps at runner inner faces; qualify weld details.','skid',947.2)
 for side,y in [('L',500),('R',-500)]:
  xy=[(x,y-70),(x,y+70)];prefix=f'LT2-M{i+1}-{side}'
  for name,z,group in [('CAP',1656.35,'mount'),('FOOT',1669.05,'skid'),('BACK',1440.45,'mount')]:
   sh=drilled(box(240,220,12.7,x,y,z),xy,18,z,12.7)
   add(prefix+'-'+name,name.lower()+' plate','skid' if name=='FOOT' else group,sh,plate,'240×220×12.7; two Ø18 through holes at Y±70 from local centre. Nominal custom interface; release tolerance/preload not assigned.',holes=[{'x':a,'y':b,'diameter_mm':18}for a,b in xy])
  for j,(hx,hy) in enumerate(xy):
   sh=vertical_cyl(12.7,203.2,hx,hy,1548.4).cut(vertical_cyl(9,207.2,hx,hy,1548.4))
   add(prefix+f'-SL{j+1}','Through-wall compression sleeve','sleeve',sh,'Steel sleeve stock — final grade/process unresolved','OD25.4 / ID18 / length203.2, nominal. 0.3mm radial gap in Ø26 wall holes; retention/finish/welding must be developed. Do not tighten bolts against unsupported tube walls.')
for i,x in enumerate([2850,4050]):
 for side,y in [('L',500),('R',-500)]:
  add(f'LT2-EP{i+1}-{side}','Engine isolator pad blank','skid',box(200,150,12.7,x,y,1783.35),plate,'200×150×12.7 undrilled pad. OEM mount positions, isolation stiffness, engine rotation and adapter loads are NOT selected.')

js('parameters.json',params);js('sections.json',sections);js('parts.json',{'issue':params['issue'],'parts':parts})
assembly=cq.Compound.makeCompound(shapes);cq.exporters.export(assembly,str(P/'LT2-frame-and-skid-R0.step'))
skidshapes=[s for s,p in zip(shapes,parts)if p['group']=='skid'];cq.exporters.export(cq.Compound.makeCompound(skidshapes),str(P/'LT2-engine-skid-R0.step'))
# The frame viewer already used by the Site expects inches; this is an explicit mm->in conversion.
groups=[('main','Main rails','#426474',[0,0,0]),('support','Support crossmembers','#718991',[0,0,-12]),('cross','Equipment crossmembers','#93aaa9',[0,0,8]),('doubler','Outer rail doublers','#ba8b45',[0,10,0]),('pad','Undrilled support pads','#d1aa6d',[0,0,-25]),('mount','Frame-side skid mounts','#8e956a',[0,0,12]),('sleeve','Compression sleeves','#c0b38c',[0,0,20]),('skid','Removable engine skid','#546c4e',[0,0,40])]
model={'schemaVersion':3,'units':'inches','title':'LT2 locomotive frame / removable skid','coordinate_system':params['datum']+'; viewer coordinates converted to inches','groups':[{'id':i,'label':l,'explosion_vector_in':v,'default_visible':True}for i,l,c,v in groups],'parts':[],'notes':['Physical candidate solids. No drivetrain or OEM geometry has been overwritten.','No fabrication release; source CAD in mm, viewer in inches.']}
for row,shape in zip(parts,shapes):
 verts,tri=shape.tessellate(1.0);bb=row['bounds_mm'];cen=[sum(bb[a])/2/25.4 for a in ['x','y','z']]
 model['parts'].append({'id':row['id'],'name':row['name'],'group':row['group'],'positions':[v/25.4 for pt in verts for v in pt.toTuple()],'indices':[i for t in tri for i in t],
 'centre_in':cen,'dimensions_xyz_in':[(bb[a][1]-bb[a][0])/25.4 for a in ['x','y','z']],'bounds_in':{a:[x/25.4 for x in bb[a]]for a in bb},'color':next(c for i,l,c,v in groups if i==row['group']),
 'metadata':{'material':{'candidate':row['material'],'status':'Candidate; no purchased mill certification'},'definition':row['definition'],'evidence':row['definition'],
 'section':{'id':row['section'],'label':sections[row['section']]['name'] if row['section'] else 'Custom plate or sleeve','nominal_wall_in':sections[row['section']]['t']/25.4 if row['section'] else None,'status':'Nominal solid; see part schedule'},
 'length':{'value_in':row['length_mm']/25.4 if row['length_mm'] else None,'meaning':'Nominal modeled length','status':'Cutting tolerance not released'},
 'catalog_mass_kg':row.get('catalog_mass_kg'),'catalog_lb_ft':sections[row['section']]['lb_ft'] if row['section'] else None,
 'source_refs':[{'id':'LT2','label':'Nominal geometry and individual part definition','path':'assets/locomotive-lt2/parts.json'},{'id':'CAD','label':'Reproducible solid-model source','path':'assets/locomotive-lt2/build_lt2.py'}],
 'engineering_status':'Preliminary physical proposal; load-path and manufacturing release incomplete','release_status':'NOT RELEASED FOR FABRICATION','geometric_mass_kg':row['geometric_mass_kg']}})
js('model.json',model)

# Piecewise Euler-Bernoulli paired-rail model with unilateral vertical support springs.
# This is longitudinal symmetric bending only; no roll, lateral, local-shell or rail-contact model.
frame_mass=sum(p['geometric_mass_kg']for p in parts)
ledger=[{'name':'Modeled frame, support pads and skid','kg':frame_mass,'x':sum(p['geometric_mass_kg']*sum(p['bounds_mm']['x'])/2 for p in parts)/frame_mass},
 {'name':'Cab and decorative enclosure allowance','kg':1100,'x':6100}, {'name':'Traction engine/pump/adapter allowance','kg':600,'x':3400},
 {'name':'Cooling / oil / air allowance','kg':350,'x':5200},{'name':'Electrical / controls allowance','kg':200,'x':6500},
 {'name':'Crew allowance','kg':200,'x':8500},{'name':'Operating fluids/fuel allowance','kg':450,'x':4200},
 {'name':'Other installed equipment allowance','kg':450,'x':5000}]
balance=6750-sum(r['kg']for r in ledger);assert balance>0
ledger.append({'name':'Unallocated sprung-mass balance — not specified ballast','kg':balance,'x':4500})
# Main rails carry their own mass along their length. Other individual steel parts
# are concentrated at their own centres, not all at the assembly centre of mass.
loads=ledger[1:].copy()
for p in parts:
 lo,hi=p['bounds_mm']['x']; n=46 if p['group']=='main' else 1
 for i in range(n):loads.append({'name':p['id'],'kg':p['geometric_mass_kg']/n,'x':round(lo+(i+.5)*(hi-lo)/n,4)})
supports=[{'id':s,'x':x,'target_sprung_kg':m,'equivalent_k_N_mm':m*gg/50,'running_gear_mass_kg':u}for s,x,m,u in zip(['Leading','Powered A','Powered B','Trailing'],[1200,3300,6000,8300],[350,2800,2800,800],[250,2200,2200,600])]
def kbeam(EI,L):
 return EI/L**3*np.array([[12,6*L,-12,6*L],[6*L,4*L*L,-6*L,2*L*L],[-12,-6*L,12,-6*L],[6*L,2*L*L,-6*L,4*L*L]])
def analyze(name,factor=1,settle=None,removed=()):
 settle=settle or {};points=list(np.arange(300,9501,200))+[9500]+[s['x']for s in supports]+[r['x']for r in loads]
 nodes=np.array(sorted(set(points)));N=len(nodes);K0=np.zeros((2*N,2*N));F=np.zeros(2*N);EI=200000*2*215*25.4**4
 elements=[]
 for i in range(N-1):
  idx=np.array([2*i,2*i+1,2*i+2,2*i+3]);k=kbeam(EI,nodes[i+1]-nodes[i]);K0[np.ix_(idx,idx)]+=k;elements.append((idx,k))
 for r in loads:F[2*np.searchsorted(nodes,r['x'])]+=r['kg']*gg*factor
 active=set(range(4))-set(removed)
 for _ in range(8):
  K=K0.copy();rhs=F.copy()
  for j in active:
   s=supports[j];d=2*np.searchsorted(nodes,s['x']);k=s['equivalent_k_N_mm'];K[d,d]+=k;rhs[d]+=k*settle.get(j,0)
  u=np.linalg.solve(K,rhs)
  R=[supports[j]['equivalent_k_N_mm']*(u[2*np.searchsorted(nodes,supports[j]['x'])]-settle.get(j,0)) if j in active else 0 for j in range(4)]
  neg={j for j in active if R[j]<-1e-5}
  if not neg:break
  active-=neg
 else:raise ValueError('unilateral solver did not converge')
 forces=[k@u[idx] for idx,k in elements];M=max(abs(v[i])for v in forces for i in [1,3]);stress=M/(2*35.8*25.4**3)
 ia=np.searchsorted(nodes,3300);ib=np.searchsorted(nodes,6000);line=u[2*ia]+(nodes-3300)*(u[2*ib]-u[2*ia])/2700
 rows=[{'support':s['id'],'reaction_kN':R[i]/1000,'deflection_at_support_mm':u[2*np.searchsorted(nodes,s['x'])],'ground_offset_mm':settle.get(i,0),'equivalent_spring_compression_mm':u[2*np.searchsorted(nodes,s['x'])]-settle.get(i,0) if i in active else 0,'active':i in active}for i,s in enumerate(supports)]
 total=sum(R);moment=sum(R[i]*s['x']for i,s in enumerate(supports));load=sum(r['kg']*gg*factor for r in loads);lm=sum(r['kg']*gg*factor*r['x']for r in loads)
 assert abs(total-load)<.02;assert abs(moment-lm)<100
 return {'case':name,'vertical_factor':factor,'reactions':rows,'max_pair_rail_bending_kNm':M/1e6,'nominal_each_rail_bending_stress_MPa':stress,'max_vertical_displacement_mm':float(max(abs(u[::2]))),'max_shape_departure_from_drive_support_chord_mm':float(max(abs(u[::2]-line))),'balance_force_N':total-load,'balance_moment_Nmm':moment-lm,'computed_powered_mass_equivalent_kg':(R[1]+R[2])/gg+4400 if factor==1 else None,'active_support_count':len(active)}
cases=[analyze('Level support plane / 1g'),analyze('Level support plane / 2g vertical load',2),analyze('Leading support base lowered25mm',settle={0:25}),analyze('Powered A support base lowered25mm',settle={1:25}),analyze('Trailing support base lowered25mm',settle={3:25}),analyze('Leading support unavailable',removed=(0,)),analyze('Powered A support unavailable',removed=(1,))]
loadcalc={'issue':params['issue'],'modeled_mass_kg':frame_mass,'sprung_mass_kg':6750,'running_gear_allowance_kg':5250,'full_loco_trial_kg':12000,'ledger':ledger,'sprung_CG_x_mm':sum(r['kg']*r['x']for r in ledger)/6750,'support_trials':supports,'cases':cases,'method':'Two continuous main rails represented by one equivalent Euler-Bernoulli beam: E200GPa; I=2×215in^4; unilateral linear vertical support springs. Point masses at listed X. No lateral/roll/axle force model.',
 'limits':['Equivalent support rates derive from assumed50mm static compression; NOT selected coil spring rates. No primary/secondary series stiffness or damping selected.','Frame gross12t includes5.25t lower running-gear allowance. Those lower masses are excluded from frame bending loads.','2g is a designer sensitivity, not an adopted code/load factor. Disabled-support cases are analytical faults, not permission for operation.','Maximum displacement includes spring settlement. Chord departure isolates approximate frame shape; neither is a released serviceability limit.','Stress is nominal elastic bending only. No strength utilization ratio or fatigue life is established. Local HSS walls, bolster torsion, welds, couplers and twist are unverified.','Unallocated mass is a budget gap with an assumed X for sensitivity. It is not authority to add ballast.']}
loadcalc['load_discretization']='Main-rail self mass at 46 equal segment centres per rail; other modeled steel at each part centre. Equipment allowances at listed X.'
js('load-and-suspension.json',loadcalc)
mount={'issue':params['issue'],'total_supported_skid_mass_trial_kg':750,'CG_height_above_mount_plane_mm':600,'mount_x_spacing_mm':2100,'mount_y_spacing_mm':1000,'vertical_comparison_g':2,'longitudinal_comparison_g':1,'lateral_comparison_g':.5,
 'max_compression_per_foot_kN':(750*gg*2/4+750*gg*600/(2*2100)+750*gg*.5*600/(2*1000))/1000,
 'uplift_case_per_bolt_kN':(750*gg/4+750*gg*600/(2*2100)+750*gg*.5*600/(2*1000))/2/1000,
 'direct_shear_per_bolt_kN':math.hypot(750*gg,750*gg*.5)/8/1000,
 'limits':'Comparison demands only: ideal rigid skid/equal fastener sharing. No prying, engine torque/transient, vibration, bolt preload, fatigue, sleeve-weld or local crossmember-wall verification. Uplift case uses net1g upward plus the same horizontal loads; not a prescribed service combination.'}
js('mount-demand.json',mount)

# SVG drawings from parameters/part envelopes; all text at a readable drawing scale.
def start(title,sub,w=1700,h=1050):
 return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><style>text{{font-family:Arial,sans-serif;fill:#17364a}}.t{{font-size:19px}}.s{{font-size:16px}}.d{{stroke:#9b6d2e;stroke-width:1.4;fill:none}}.l{{stroke:#17364a;stroke-width:2;fill:none}}</style><rect width="100%" height="100%" fill="#fffef9"/><text x="45" y="45" font-size="29" font-weight="bold">{title}</text><text x="45" y="78" class="t">{sub}</text>']
def txt(a,x,y,t,cls='t'):a.append(f'<text x="{x}" y="{y}" class="{cls}">{t}</text>')
def dim(a,x1,x2,y,t):a.append(f'<path class="d" d="M{x1},{y-8}v16M{x2},{y-8}v16M{x1},{y}H{x2}"/>');txt(a,(x1+x2)/2-45,y-11,t,'s')
a=start('LT2-A01 · Main-frame plan and station schedule','Physical preliminary members · mm unless marked · NOT RELEASED FOR FABRICATION')
sx=.15;X=lambda x:90+(x-300)*sx;Y=lambda y:360-y*sx
colors={i:c for i,l,c,v in groups}
for row in parts:
 if row['group'] not in ['main','support','cross','doubler','pad']:continue
 bb=row['bounds_mm'];a.append(f'<rect x="{X(bb["x"][0])}" y="{Y(bb["y"][1])}" width="{(bb["x"][1]-bb["x"][0])*sx}" height="{(bb["y"][1]-bb["y"][0])*sx}" fill="{colors[row["group"]]}" stroke="#17364a"/>')
for i,x in enumerate(params['support_x']):
 a.append(f'<path class="d" d="M{X(x)},140V530"/>');txt(a,X(x)-40,135,f'B{i+1} / X{x}','s')
for i,x in enumerate(params['crossmember_x']):txt(a,X(x)-16,555,f'C{i+1}','s')
dim(a,X(300),X(9500),600,'9,200 (362.20 in)')
txt(a,45,670,'Main rails: two HSS12×6×3/8 · centres Y±850 · 1,700 centre spacing · 1,852.4 overall rail width')
txt(a,45,708,'Support crossmembers B1–B4: HSS12×6×3/8 · 1,545.6 nominal length · 1mm joint gap each end')
txt(a,45,746,'Equipment crossmembers C1–C8: HSS8×4×1/4 · X600 / 1800 / 2400 / 4500 / 5100 / 7200 / 9000 / 9300')
txt(a,45,784,'Rail/support top Z1,650; bottom Z1345.2. Equipment crossmember bottom Z1446.8. LT1 support stations retained.')
txt(a,45,822,'Gold squares = undrilled support-pad proposals. Mating yaw bearing, side supports, retention and suspension remain DT interfaces.')
txt(a,45,875,'No coupler/draft structure, pilot support, cab outriggers or complete lifting points are included. Do not lift from unqualified pads.')
txt(a,45,985,'PF-LOCO-LT2-R0 · Source: build_lt2.py / parameters.json / parts.json · Dimensions are proposals, not manufacturing tolerances','s')
(P/'LT2-A01-frame.svg').write_text(''.join(a)+'</svg>')
a=start('LT2-J01 · Removable engine skid / frame-side connection','Two mounting stations X2,400 / X4,500; four feet and eight M16 candidate bolts · mm')
# Enlarged actual section at one foot, viewed along X. Same Z/width as CAD.
sy=1.4; zz=lambda z:720-(z-1400)*sy; yy=lambda y:410+y*sy
for name,y,z,w,h,col in [('crossmember',0,1548.4,500,203.2,'#8aa1a4'),('back',0,1440.45,220,12.7,'#c4a66d'),('cap',0,1656.35,220,12.7,'#c4a66d'),('foot',0,1669.05,220,12.7,'#718b69'),('runner',0,1726.2,50.8,101.6,'#718b69')]:
 a.append(f'<rect x="{yy(y-w/2)}" y="{zz(z+h/2)}" width="{w*sy}" height="{h*sy}" fill="{col}" stroke="#17364a" stroke-width="2"/>')
# Hollow crossmember section and runner section.
a.append(f'<rect x="{yy(-250)}" y="{zz(1643.65)}" width="{500*sy}" height="{190.5*sy}" fill="#fffef9" stroke="#17364a"/>')
a.append(f'<rect x="{yy(-19.05)}" y="{zz(1770.65)}" width="{38.1*sy}" height="{88.9*sy}" fill="#fffef9" stroke="#17364a"/>')
for y in [-70,70]:
 a.append(f'<rect x="{yy(y-12.7)}" y="{zz(1650)}" width="{25.4*sy}" height="{203.2*sy}" fill="#adab8e" stroke="#17364a"/>')
 a.append(f'<path d="M{yy(y)},{zz(1700)}V{zz(1415)}" stroke="#273a42" stroke-width="8"/>')
 a.append(f'<rect x="{yy(y-12)}" y="{zz(1685.4)}" width="{24*sy}" height="{10*sy}" fill="#273a42"/><rect x="{yy(y-12)}" y="{zz(1434.1)}" width="{24*sy}" height="{13*sy}" fill="#273a42"/>')
dim(a,yy(-70),yy(70),790,'140 bolt pitch')
notes=['Skid runner: HSS4×2×1/4; top Z1,777.0','Foot plate: 240×220×12.7; two Ø18 holes','Cap plate: 240×220×12.7; top Z1,662.7','Crossmember: HSS8×4×1/4; top Z1,650','Sleeve: OD25.4 / ID18 / length203.2','Back plate: 240×220×12.7; bottom Z1434.1','Frame-side hole grid: X2400/4500, Y±430/±570','Bolt length, lock/preload and washer stack unresolved','Engine-side pad blanks stay undrilled for OEM mounts']
for i,n in enumerate(notes):txt(a,850,190+i*53,n)
txt(a,45,865,'Section follows the actual pad/sleeve stack; bolt shapes are identification proxies. No OEM isolator or engine-bolt pattern is implied.')
txt(a,45,906,'Sleeves bypass hollow walls in clamp compression. Their wall retention, end contact, welds and local bending still need design verification.')
txt(a,45,985,'PF-LOCO-LT2-R0 · Not released for manufacture · No torque value assigned before finish, preload and clamp-stack validation','s')
(P/'LT2-J01-skid.svg').write_text(''.join(a)+'</svg>')
a=start('LT2-P01 · Custom skid plate and sleeve definitions','Nominal physical parts from the CAD source · no released fit/position tolerances')
# Plate plan: x dimension horizontal, y vertical.
px=130;py=185;scale=2
a.append(f'<rect x="{px}" y="{py}" width="480" height="440" fill="#dbe4df" stroke="#17364a" stroke-width="3"/>')
for y in [40,180]:a.append(f'<circle cx="{px+240}" cy="{py+y*2}" r="18" fill="#fffef9" stroke="#17364a" stroke-width="3"/>')
dim(a,px,px+480,670,'240');a.append(f'<path class="d" d="M{px-30},{py}H{px-10}M{px-30},{py+440}H{px-10}M{px-20},{py}V{py+440}"/>');txt(a,50,420,'220')
txt(a,125,725,'CAP / FOOT / BACK: 12 pieces total')
txt(a,125,760,'Two Ø18 holes at local X120, Y40 / Y180')
txt(a,125,795,'12.7mm A572 Grade50 plate proposal')
a.append('<rect x="950" y="200" width="50.8" height="406.4" fill="#b4b89b" stroke="#17364a" stroke-width="3"/><rect x="957.4" y="200" width="36" height="406.4" fill="#fffef9" stroke="#17364a"/>')
txt(a,1110,280,'Eight sleeves');txt(a,1110,330,'OD25.4 / ID18');txt(a,1110,380,'Length203.2');txt(a,1110,430,'Stock grade and finish unresolved')
txt(a,850,725,'Frame wall receiving holes Ø26; radial gap0.3mm')
txt(a,850,765,'Do not infer a press fit or a qualified sleeve weld')
txt(a,45,885,'Proposed fabrication route: cut plate blanks → locate/bore holes → dry-fit sleeves and backing → qualify attachment/retention → inspect.')
txt(a,45,930,'Saw/bore/weld tolerances and acceptance limits must be assigned with actual stock, welding sequence and engine vibration loads.')
txt(a,45,985,'PF-LOCO-LT2-R0 · Main frame and bolsters require separate structural/fatigue/local-wall review before release','s')
(P/'LT2-P01-plates.svg').write_text(''.join(a)+'</svg>')

sources={'checked':'2026-10-19','sources':[{'id':'ST1','url':'https://www.atlastube.com/wp-content/uploads/2018/04/Atlas-HSS-Section-Properties-A500-Rectangles.pdf','use':'Pages2/3/5: HSS12×6×3/8 W42.79lb/ft,I215in4,S35.8in3; HSS8×4×1/4 W19.02,I42.5,S10.6; HSS4×2×1/4 W8.81,I4.49,S2.25. Catalog properties used for global beam, nominal modeled solids for geometric takeoff.'},
 {'id':'ST2','url':'https://steeltubeinstitute.org/resources/astm-a500/','use':'A500 GradeC50ksi yield;0.93 nominal wall design convention and corner-property caveats. Not a rail fatigue qualification.'},
 {'id':'ST3','url':'https://www.ssab.com/en-us/brands-and-products/commercial-steel/structural-steel/astm-a572/grade-50','use':'Grade50 plate manufacturer range and50ksi specified yield. Notch toughness must be specified for application.'},
 {'id':'ST4','url':'https://www.bossard.com/us-en/knowledge-hub/resources/technical-information/','use':'Fastening engineering reference; M16 class8.8 here is a preliminary proposal, not a verified complete joint or quoted order code.'}]}
js('sources.json',sources)
js('release-and-interfaces.json',{'issue':params['issue'],'delivered':['Physical hollow frame, support pads/doublers and removable skid solids','Frame station, skid section and custom plate/sleeve drawings','Selectable rotatable part model and STEP files','Symmetric vertical support sensitivity and skid mount force estimates'],
 'not_delivered':['Complete suspension springs/dampers/guides/retention','Wheelsets or gearbox/motor mounts owned by DT','Coupler/draft load path and full tender chassis','Final engine isolator and OEM mating holes','Qualified weld/tolerance/preload schedule','Fatigue/local-wall/twist/lateral acceptance'],
 'connection_schedule':[{'id':'W01','location':'Crossmember ends to main-rail inner side walls','proposal':'6mm continuous fillet on accessible perimeter,1mm fit-up gap study','status':'Unverified candidate; effective weld length, tube corner transitions, fatigue, HSS wall plastification/punching and WPS require calculation/review.'},{'id':'W02','location':'Support crossmembers, rail doublers and underside pads','proposal':'No universal weld size selected','status':'Direct support/load path depends on DT reactions, support bearing and retention. Do not substitute W01.'},{'id':'W03','location':'Skid runner/cross-tie and foot plates','proposal':'6mm accessible fillet candidate','status':'Engine vibration, reversal, fatigue, thin-wall interaction and complete weld path unverified.'},{'id':'W04','location':'Sleeve to crossmember walls / cap / backing','proposal':'Retention detail unselected','status':'No bolt tightening until sleeves are retained, full contact verified and joint approved.'}],
 'DT_handoff':{'frame_top_z':1650,'main_rail_centres_y':[-850,850],'rail_inner_faces_y':[-773.8,773.8],'rail_bottom_z':1345.2,'support_x':[1200,3300,6000,8300],'driven_support_pad_bottom_z':1326.15,'driven_support_pad_footprint_mm':[600,600],'holes':'none in support pads; DT2 top plate at1170 leaves156.15mm nominal support-stack reservation; bearing/pivot/retention dimensions required','service_notes':'Skid removable upward after shell removal; actual lift/rotation, shafts, hoses and CG need OEM coordination'},
 'construction_approved':False})
print(json.dumps({'parts':len(parts),'frame_geometric_mass_kg':frame_mass,'unallocated_sprung_mass_kg':balance,'level':cases[0],'mount':mount}))

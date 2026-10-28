"""C2.1 R0: proposed regular-coach bench and four-bolt steel floor bypass.
Canonical CAD in inches; STEP mm. Run with CadQuery 2.7. Preliminary, not released.
Nominal purchased hardware envelopes identify the family, not a supplier exact model.
"""

# Hosting transport: retain hashes of decoded source bytes after gzip packaging.
import gzip as _transport_gzip
def _transport_bytes(path):
    return path.read_bytes() if path.exists() else _transport_gzip.decompress(path.with_name(path.name + '.gz').read_bytes())

from pathlib import Path
import gzip
import json,math,copy,collections,ast
import cadquery as cq
import numpy as np
from PIL import Image,ImageDraw
# Lossless transport packaging; raw CAD/JSON payloads are preserved byte for byte.
def write_gzip(path, payload):
 compressed=gzip.compress(payload,compresslevel=9,mtime=0)
 assert gzip.decompress(compressed)==payload
 packed=path.with_name(path.name+'.gz')
 packed.write_bytes(compressed)
 assert gzip.decompress(packed.read_bytes())==payload
 if path.exists():path.unlink()
H=Path(__file__).resolve().parent;D=H.parents[1];MM=25.4
P={'revision':'PF-3O2-C21-R0','units':'inches','date':'2026-10-19','prototype_origin':'bench row X0; right-side Y12..52; Z above rail',
 'row_x':[41,73,105,137,169,201,233,265],'feet_x':[-8,8],'feet_y':[20,44],
 'floor_z':32,'steel_top_z':31.003937007874015,'cap_size':[3.5,6,.625],
 'sole_size':[3.5,6,.5],'sole_under_z':32.25,'sole_top_z':32.75,
 'bolt_xy_offsets':[[-.875,-2],[-.875,2],[.875,-2],[.875,2]],'hole_diameter':.5625,
 'spacer_OD':1,'spacer_ID':.5625,'spacer_length':None,
 'panel_opening':[3.875,6.375],'seat_top_z':50,'back_top_z':70,
 'seat_pan_bounds':{'x':[-10,6.875],'y':[12,52],'z':[48,48.125]},
 'back_pan_bounds':{'x':[6.875,7],'y':[12,52],'z':[50.25,70]},
 'seat_pad_bounds':{'x':[-10,5.875],'y':[12,52],'z':[48.125,50]},
 'back_pad_bounds':{'x':[5.875,6.875],'y':[12,52],'z':[50.25,70]},
 'pad_status':'Geometry proposal only: upholstery, foam, fire performance and retention unfinished',
 'washer_display_t':.125,'washer_actual_t_range':[.097,.177],'bolt_length':3.0,
 'hss_corner_model':'Nominal 2t outer / t inner; supplied section is not asserted'}
P['cap_top_z']=P['steel_top_z']+P['cap_size'][2]
P['spacer_length']=P['sole_under_z']-P['cap_top_z']
P['brace_workpoints_in']={'BZ1':[[-8,20,35.25],[8,20,47.25]],'BZ2':[[-8,44,35.25],[8,44,47.25]],'BV1':[[8,20,35.25],[8,32,47.25]],'BV2':[[8,44,35.25],[8,32,47.25]]}
P['brace_section_in']=[1.25,1.25,.125]
P['rib_thickness_in']=.375
P['socket_envelope']={'diameter_in':1.25,'rib_side_clearance_in':.0625,'approach':'Coaxial vertically above / below bolt; nominal uncoated geometric envelope only','excludes':'Actual vendor socket and ratchet, weld fillets, fabrication tolerance and service reach'}
P['status']='PROPOSED C2.1 CANDIDATE; NOT FOR FABRICATION'
P['version_notes']=['C2 predecessor preserved. C2.1 adds four coped braces and eight upper/eight lower beveled ribs per bench.','5/8in cap,1/2in sole and3/8in ribs are a candidate with local bending/weld/rail fatigue checks outstanding.','Derived15.775mm spacer maintains sole underside32.25. Existing bolt pattern retained.']
parts=[];S={};edges={};families={}
colors={'frame':'#35695a','hardpoint':'#a07a36','hardware':'#8b9598','pan':'#b7b7ad','padding':'#8a3731','context':'#7d8d90','floor':'#b69f78'}
groups=[{'id':k,'label':v,'explosion_vector_in':e,'default_visible':k not in ('padding',)} for k,v,e in [
 ('frame','Bench welded tube frame',[0,0,0]),('hardpoint','Four-bolt feet / steel bypass',[0,0,-8]),('hardware','Nominal commercial fasteners',[0,8,-5]),
 ('pan','Removable seat / back plates',[-5,0,6]),('padding','Upholstery geometry proposal',[-8,0,8]),('context','Underframe context',[0,0,-12]),('floor','Floor context',[0,0,-6])]]
def box(b):return cq.Solid.makeBox(*[(b[a][1]-b[a][0])*MM for a in 'xyz'],cq.Vector(*[b[a][0]*MM for a in 'xyz']))
def cyl(r,l,p,a=(0,0,1)):return cq.Solid.makeCylinder(r*MM,l*MM,cq.Vector(*[v*MM for v in p]),cq.Vector(*a))
def hollow(b,a,t):
 s=box(b);v={k:[b[k][0]+t,b[k][1]-t] for k in 'xyz'};v[a]=[b[a][0]-1,b[a][1]+1]
 return cq.Workplane(obj=s).edges('|'+a.upper()).fillet(2*t*MM).val().cut(cq.Workplane(obj=box(v)).edges('|'+a.upper()).fillet(t*MM).val())
def edgecache(s):
 return [[[p.x/MM,p.y/MM,p.z/MM] for p in [e.positionAt(t) for t in np.linspace(0,1,2 if e.geomType()=='LINE' else 21)]] for e in s.Edges()]
def add(pid,fam,name,g,s,definition,material,density=7850):
 assert s.isValid(),pid
 vv,ff=s.tessellate(.55,.12);bb=s.BoundingBox();b={a:[getattr(bb,a+'min')/MM,getattr(bb,a+'max')/MM] for a in 'xyz'}
 meta={'kind':'custom_part' if g not in ('hardware','padding','context','floor') else g,'family':fam,'material':{'candidate':material},'definition':definition,
       'solid_mass_kg':s.Volume()/1e9*density,'engineering_status':'PRELIMINARY DESIGN; NOT RELEASED','release_status':'NOT FOR CONSTRUCTION'}
 p={'id':pid,'name':name,'group':g,'positions':[round(v,6) for q in vv for v in (q.x/MM,q.y/MM,q.z/MM)],'indices':[v for f in ff for v in f],
 'bounds_in':b,'centre_in':[(lo+hi)/2 for lo,hi in b.values()],'dimensions_xyz_in':[hi-lo for lo,hi in b.values()],
 'color':colors[g],'opacity':1,'metadata':meta,'display_only':g in ('padding','context','floor')}
 parts.append(p);S[pid]=s;edges[pid]=edgecache(s)
 if fam not in families:families[fam]={'id':fam,'name':name,'quantity_per_bench':0,'material':material,'definition':definition,'representative':pid}
 families[fam]['quantity_per_bench']+=1
 return s
def tube(pid,fam,b,a,w):
 sh=hollow(b,a,.125);bores=[]
 if pid.startswith('BACK-') and pid[-1:] in ('1','3'):
  y=14.25 if pid.endswith('1') else 49.75;z=58.75 if 'MID' in pid else 69.25
  sh=sh.cut(cyl(.25,3,(6,y,z),(1,0,0)));bores=[{'axis':'x','y':y,'z':z,'diameter':.5}]
 s=add(pid,fam,f'HSS {w} square x 1/8','frame',sh,{'section_in':[w,w,.125],'length_in':b[a][1]-b[a][0],'axis':a,'sleeve_bores':bores,'end_prep':'Square cut; nominal corner contact requires fit-up/WPS review'},'ASTM A500 Grade C')
 parts[-1]['metadata']['catalog_mass_kg']=(b[a][1]-b[a][0])/12*(2.2 if w==1.5 else 3.05)*.45359237
 return s
def plate(pid,fam,b,holes,g='hardpoint',axis='z',material='ASTM A36',density=7850):
 s=box(b);inds={'x':('y','z'),'y':('x','z'),'z':('x','y')}[axis];vec={'x':(1,0,0),'y':(0,1,0),'z':(0,0,1)}[axis]
 for u,v,d in holes:
  xyz={axis:b[axis][0]-1,inds[0]:u,inds[1]:v};s=s.cut(cyl(d/2,b[axis][1]-b[axis][0]+2,[xyz[k] for k in 'xyz'],vec))
 return add(pid,fam,fam+' plate',g,s,{'bounds_in':b,'hole_axis':axis,'holes':holes,'hole_axes':list(inds),'profile':'Rectangular blank; break edges after cutting'},material,density)
def triangular_rib(pid,fam,x,vertices,definition):
 sh=cq.Workplane(cq.Plane(origin=((x-P['rib_thickness_in']/2)*MM,0,0),xDir=(0,1,0),normal=(1,0,0))).polyline([(y*MM,z*MM) for y,z in vertices]).close().extrude(P['rib_thickness_in']*MM).val()
 definition={**definition,'thickness_in':P['rib_thickness_in'],'x_limits_in':[x-P['rib_thickness_in']/2,x+P['rib_thickness_in']/2],'profile_yz_in':vertices,'end_prep':'Deburred four-point blank; weld sizes, returns and fatigue detail open'}
 return add(pid,fam,'Beveled plate rib, proposed','hardpoint',sh,definition,'ASTM A36 candidate')
def outer_hss(p):
 b=p['bounds_in'];d=p['metadata']['definition'];axis=d['axis'];t=d['section_in'][2]
 return cq.Workplane(obj=box(b)).edges('|'+axis.upper()).fillet(2*t*MM).val()
def coped_brace(pid,fam,ends):
 p0=np.array(ends[0],float);p1=np.array(ends[1],float);d=p1-p0;length=float(np.linalg.norm(d));u=d/length
 xd=(0,1,0) if abs(u[1])<1e-9 else (1,0,0)
 plane=cq.Plane(origin=cq.Vector(*[v*MM for v in p0]),xDir=cq.Vector(*xd),normal=cq.Vector(*u))
 w=P['brace_section_in'][0];t=P['brace_section_in'][2]
 raw=cq.Workplane(plane).rect(w*MM,w*MM).extrude(length*MM)
 # Round the same nominal section corners as all retained HSS, then hollow it.
 axial=[e for e in raw.val().Edges() if e.geomType()=='LINE' and abs(e.Length()-length*MM)<1e-5]
 raw=raw.newObject(axial).fillet(.25*MM).val()
 inn=cq.Workplane(plane).rect((w-2*t)*MM,(w-2*t)*MM).extrude(length*MM)
 axial=[e for e in inn.val().Edges() if e.geomType()=='LINE' and abs(e.Length()-length*MM)<1e-5]
 inn=inn.newObject(axial).fillet(.125*MM).val()
 sh=raw.cut(inn);nominal_section_area=sh.Volume()/(length*MM);cope=[]
 for p in list(parts):
  if p['group']=='frame' and 'axis' in p['metadata']['definition']:
   envelope=outer_hss(p)
   if sh.intersect(envelope).Volume()>1e-5:
    sh=sh.cut(envelope);cope.append(p['id'])
 if pid in ('BV1','BV2'):
  sh=sh.intersect(box({'x':[-100,100],'y':[-100,32] if pid=='BV1' else [32,100],'z':[-100,100]}))
 assert len(sh.Solids())==1,(pid,len(sh.Solids()))
 localshape=plane.toLocalCoords(sh);bb=localshape.BoundingBox();span=(bb.zmax-bb.zmin)/MM
 add(pid,fam,'Coped 1.25 x 1.25 x 1/8 HSS brace','frame',sh,{'section_in':[w,w,t],'workpoints_in':ends,'workpoint_length_in':length,'axis_unit':u.tolist(),'axial_envelope_in':span,'cope_to_members':cope,'apex_miter':'Rear V: commonY32plane trims cornerlands to zerooverlap; receiving rail cope retained' if pid.startswith('BV') else None,'end_prep':'CAD coping follows nominal receiving HSS outer rounded faces; workpoint length is NOT a saw-cut length. Verify measured section and trial fit.','weld_status':'Exact weld throat, root gap, toe transitions, access and fatigue detail unresolved'},'ASTM A500 Grade C candidate')
 parts[-1]['metadata']['catalog_mass_kg']=sh.Volume()/nominal_section_area/MM/12*1.78*.45359237
 parts[-1]['metadata']['catalog_linear_lb_per_ft']=1.78
 parts[-1]['metadata']['catalog_mass_basis']='Equivalent uncut stock length from exact coped volume divided by nominal section area;1.78lb/ft candidate catalog weight'
 return sh
def hexsolid(af,h,x,y,z):
 r=af/math.sqrt(3);pts=[((x+r*math.cos(math.pi/6+i*math.pi/3))*MM,(y+r*math.sin(math.pi/6+i*math.pi/3))*MM) for i in range(6)]
 return cq.Workplane('XY').polyline(pts).close().extrude(h*MM).translate((0,0,z*MM)).val()
# 4 feet. Revised mounting pattern is not mixed with earlier I1 geometry.
for fi,(x,y) in enumerate([(x,y) for x in P['feet_x'] for y in P['feet_y']],1):
 k=f'F{fi}';holes=[(x+dx,y+dy,P['hole_diameter']) for dx,dy in P['bolt_xy_offsets']]
 plate(k+'-CAP','HP01',{'x':[x-1.75,x+1.75],'y':[y-3,y+3],'z':[P['steel_top_z'],P['cap_top_z']]},holes)
 plate(k+'-SOLE','HP02',{'x':[x-P['sole_size'][0]/2,x+P['sole_size'][0]/2],'y':[y-P['sole_size'][1]/2,y+P['sole_size'][1]/2],'z':[P['sole_under_z'],P['sole_top_z']]},holes)
 for sign in (-1,1):
  yy=[y-1.25,y-1] if sign<0 else [y+1,y+1.25]
  plate(k+f'-CHEEK{sign}','HP03',{'x':[x-1.5,x+1.5],'y':yy,'z':[P['steel_top_z']-2,P['steel_top_z']]},[])
 for hi,(xx,yy,dd) in enumerate(holes,1):
  add(k+f'-SP{hi}','HP04','Machined rigid spacer','hardpoint',cyl(.5,P['spacer_length'],(xx,yy,P['cap_top_z'])).cut(cyl(.28125,P['spacer_length']+2,(xx,yy,P['cap_top_z']-1))),
   {'OD_in':1,'ID_in':.5625,'nominal_length_in':P['spacer_length'],'nominal_length_mm':P['spacer_length']*MM,'fit':'Finish matched set after weld distortion/actual floor stack measured. Preliminary length tolerance +/-0.05 mm, within-set spread<=0.05 mm; no interference fit.'},'ASTM A36 machined bar; verify machinability/certification')
  wt=P['washer_display_t'];top=P['sole_top_z']+wt
  for wh,z in [('TOP',P['sole_top_z']),('LOW',P['steel_top_z']-wt)]:
   add(k+f'-WA{hi}-{wh}','HW02','F436 nominal washer','hardware',cyl(.53125,wt,(xx,yy,z)).cut(cyl(.265625,wt+2,(xx,yy,z-1))),
    {'OD_in':1.0625,'ID_in':.53125,'display_t_in':wt,'delivered_t_range_in':[.097,.177],'catalog_example':'Portland Bolt plain 16440; availability not confirmed'},'ASTM F436 candidate')
  shaft=cyl(.25,3.0,(xx,yy,top-3.0));head=hexsolid(.75,.3125,xx,yy,top)
  add(k+f'-BOLT{hi}','HW01','1/2-13 x 3 hex cap screw','hardware',shaft.fuse(head),
   {'nominal_diameter':.5,'length_under_head':3.0,'AF':.75,'head_height':.3125,'threaded_length':1.25,'thread_geometry':'Cylindrical major-diameter envelope; threads not modeled','spec':'SAE J429 Grade 8 candidate; coating and locking procedure unresolved'},'SAE J429 Grade 8 candidate')
  z=P['steel_top_z']-wt-.4375
  nut=hexsolid(.75,.4375,xx,yy,z).cut(cyl(.25,.6375,(xx,yy,z-.1)))
  add(k+f'-NUT{hi}','HW03','1/2-13 standard hex nut envelope','hardware',nut,{'AF_in':.75,'nominal_height_in':.4375,'thread':'Bore represents thread major envelope','locking':'J995 Grade8 ordinary nut geometry only; positive locking system still to select. Not a locknut model.'},'SAE J995 Grade 8 candidate')
# Candidate ribs: lower triangular brackets reach from cap underside to existing rail cheeks.
for fi,(x,y) in enumerate([(x,y) for x in P['feet_x'] for y in P['feet_y']],1):
 for sign in (-1,1):
  name='L' if sign<0 else 'R';z=P['steel_top_z'];yy=lambda r:y+sign*r
  triangular_rib(f'F{fi}-LOW-RIB-{name}','HP05',x,[(yy(1.25),z),(yy(3),z),(yy(2),z-1.75),(yy(1.25),z-1.75)],{'location':'Under cap, contacts cheek at local Y±1.25','nominal_legs_in':[1.75,1.75],'full_depth_through_local_abs_y_in':2,'tail_end_local_abs_y_in':3})
  z=P['sole_top_z'];half=.75 if x<0 else 1
  triangular_rib(f'F{fi}-UP-RIB-{name}','HP06F' if x<0 else 'HP06R',x,[(yy(half),z),(yy(2.875),z),(yy(2),z+1.75),(yy(half),z+1.75)],{'location':'Above sole, contacts leg face; outside bolt socket swept cylinder','nominal_legs_in':[2.875-half,1.75],'full_depth_through_local_abs_y_in':2,'tail_end_local_abs_y_in':2.875})
# Bench metal frame: front feet and continuous rear uprights.
for j,y in enumerate(P['feet_y'],1):
 tube(f'FRONT-LEG{j}','BF01',{'x':[-8.75,-7.25],'y':[y-.75,y+.75],'z':[P['sole_top_z'],46.5]},'z',1.5)
 tube(f'REAR-LEG{j}','BF02',{'x':[7,9],'y':[y-1,y+1],'z':[P['sole_top_z'],70]},'z',2)
tube('SEAT-FRONT','BF03',{'x':[-8.75,-7.25],'y':[12.125,51.875],'z':[46.5,48]},'y',1.5)
for j,y in enumerate((12.875,51.125),1):
 tube(f'SEAT-SIDE{j}','BF04',{'x':[-7.25,7.25],'y':[y-.75,y+.75],'z':[46.5,48]},'x',1.5)
tube('SEAT-MID','BF05',{'x':[-.75,.75],'y':[13.625,50.375],'z':[46.5,48]},'y',1.5)
for j,(y0,y1) in enumerate([(12.125,19),(21,43),(45,51.875)],1):
 tube(f'SEAT-REAR{j}','BF06' if j!=2 else 'BF07',{'x':[7.25,8.75],'y':[y0,y1],'z':[46.5,48]},'y',1.5)
 for tag,z in [('MID',58),('TOP',68.5)]:
  tube(f'BACK-{tag}{j}','BF08' if j!=2 else 'BF09',{'x':[7,8.5],'y':[y0,y1],'z':[z,z+1.5]},'y',1.5)
# C2.1 diagonal members are exact hollow solids coped to existing receiving outer faces.
for pid,ends in P['brace_workpoints_in'].items():coped_brace(pid,'BF10' if pid.startswith('BZ') else 'BF11',ends)
# Face-mounted tabs: quarter-inch bolts can be removed without drilling a blind tube wall.
seat_holes=[(x,y,.28125) for x in (-4.5,3.5) for y in (14.375,49.625)]
for n,(x,y,d) in enumerate(seat_holes,1):
 yy=[13.625,15.125] if y<32 else [48.875,50.375]
 plate(f'SEAT-TAB{n}','BP03',{'x':[x-.75,x+.75],'y':yy,'z':[47.8125,48]},[(x,y,d)],g='frame')
plate('SEAT-PAN','BP01',P['seat_pan_bounds'],seat_holes,g='pan',material='5052-H32 aluminum, proposed',density=2680)
backholes=[(y,z,.28125) for y in (14.25,49.75) for z in (58.75,69.25)]
for n,(y,z,d) in enumerate(backholes,1):
 add(f'BACK-SLEEVE{n}','BP04','Back panel through-tube spacer','frame',cyl(.25,1.5,(7,y,z),(1,0,0)).cut(cyl(.140625,3,(6,y,z),(1,0,0))),
  {'OD_in':.5,'ID_in':.28125,'length_in':1.5,'axis':'x','y':y,'z':z,'fit':'Nominal bore/OD shown. Match actual outside tube width, flush ends; slip-fit proposal, exact production fit and clamp torque to validate. Captured by panel/washer during assembly.'},'ASTM A36 machined bar')
plate('BACK-PAN','BP02',P['back_pan_bounds'],backholes,g='pan',axis='x',material='5052-H32 aluminum, proposed',density=2680)
# Upright top cap blanks: cosmetic edge finish/retention developed with bench weld procedure.
for j,y in enumerate((20,44),1):plate(f'BACK-CAP{j}','BP05',{'x':[7,9],'y':[y-1,y+1],'z':[70,70.0625]},[],g='frame')
for pid,bb in [('SEAT-PAD',P['seat_pad_bounds']),('BACK-PAD',P['back_pad_bounds'])]:
 sh=box(bb)
 try:sh=cq.Workplane(obj=sh).edges().fillet(.15*MM).val()
 except Exception:pass
 add(pid,pid,'Upholstery shape — specification incomplete','padding',sh,{'bounds_in':bb,'status':P['pad_status']},'Foam/upholstery grade, cover, attachment and fire evidence unresolved',50)
# Targeted context: actual representative source rails transformed from bench row X41.
frame=json.loads(_transport_bytes(D/'assets/models3d/frame-J1a.json').decode());ctx=[]
for p in frame['parts']:
 b=p['bounds_in']
 if b['x'][1]<28 or b['x'][0]>54 or b['y'][1]<15 or b['y'][0]>49:continue
 b=copy.deepcopy(b);b['x']=[max(b['x'][0],28)-41,min(b['x'][1],54)-41];b['y']=[max(b['y'][0],15),min(b['y'][1],49)]
 if min(b[k][1]-b[k][0] for k in 'xyz')<=0:continue
 # Clip a full source solid so cross-section is not changed by the drawing crop.
 sh=hollow(p['bounds_in'],p['metadata']['section']['orientation']['longitudinal_axis'],p['metadata']['section']['nominal_wall_in']).translate((-41*MM,0,0))
 sh=sh.intersect(box(b))
 add('CTX-'+p['id'],'CONTEXT','Retained rail/crossmember crop','context',sh,{'source':'frame-J1a.json','id':p['id'],'crop':'View crop only, not cut length'},'Retained nominal HSS study')
fl=box({'x':[-13,13],'y':[12,52],'z':[31.1220472441,31.8720472441]})
for x in P['feet_x']:
 for y in P['feet_y']:fl=fl.cut(box({'x':[x-1.9375,x+1.9375],'y':[y-3.1875,y+3.1875],'z':[30,33]}))
add('FLOOR-PANEL','CONTEXT','Floor panel with revised openings','floor',fl,{'thickness_in':.75,'opening_in':P['panel_opening'],'source':'H-P125 envelope, not qualified panel edge closure'},'Floor panel envelope — core/edge closeout unresolved',200)
# True half-solid section at local X=-8, across front foot pair. No guessed internal geometry.
clip=box({'x':[-8,0],'y':[15,25],'z':[27,36]})
for pid,sh in S.items():
 if pid.startswith('F1-') or pid in ('FRONT-LEG1','FLOOR-PANEL') or pid.startswith('CTX-S20'):
  sec=sh.intersect(clip)
  if sec.Volume()>1e-8:edges['SECTION-'+pid]=edgecache(sec)
P['section_description']='True CAD half-solid cut at X=-8 through front foot F1; look along X toward +X; cropped Y15..25, Z27..36.'
model={'schemaVersion':3,'units':'inches','title':'C2.1 braced two-adult bench / ribbed floor bypass','coordinate_system':P['prototype_origin'],'groups':groups,'parts':parts,'notes':['Preliminary custom bench geometry. Padding and context groups are references.','Metal joints, panel bolts, locking and fatigue/proof validation remain incomplete; not a complete released seat.','Purchased hardware uses documented nominal family envelopes; display washers .125in are not exact supplied thickness.']}
write_gzip(H/'model.json',json.dumps(model,separators=(',',':')).encode())
(H/'parts.json').write_text(json.dumps([{k:p[k] for k in ('id','name','group','bounds_in','metadata')} for p in parts],indent=2))
(H/'parameters.json').write_text(json.dumps(P,indent=2));(H/'drawing-edges.json').write_text(json.dumps(edges,separators=(',',':')))
(H/'bom.json').write_text(json.dumps(list(families.values()),indent=2))
physical=[S[p['id']] for p in parts if not p['display_only']]
cq.exporters.export(cq.Compound.makeCompound(physical),str(H/'C21-bench-and-hardpoints-R0.step'))
write_gzip(H/'C21-bench-and-hardpoints-R0.step',(H/'C21-bench-and-hardpoints-R0.step').read_bytes())
cq.exporters.export(cq.Compound.makeCompound([S[p['id']] for p in parts if p['id'].startswith('F1-')]),str(H/'C21-HP01-hardpoint-R0.step'))
# 1:1 DXF blanks: outlines and holes in local blank coordinates, excluding contextual geometry.
def dxf(pid,axis):
 sh=S[pid];inds={'z':('x','y'),'x':('y','z')}[axis];a,c=inds
 ds=next(p['metadata']['definition'] for p in parts if p['id']==pid);b=ds['bounds_in'];w=b[a][1]-b[a][0];h=b[c][1]-b[c][0]
 lines=['0','SECTION','2','HEADER','9','$INSUNITS','70','1','0','ENDSEC','0','SECTION','2','ENTITIES']
 for x0,y0,x1,y1 in [(0,0,w,0),(w,0,w,h),(w,h,0,h),(0,h,0,0)]:lines+=['0','LINE','8','PROFILE','10',str(x0),'20',str(y0),'11',str(x1),'21',str(y1)]
 for u,v,d in ds.get('holes',[]):lines+=['0','CIRCLE','8','HOLES','10',str(u-b[a][0]),'20',str(v-b[c][0]),'40',str(d/2)]
 lines+=['0','ENDSEC','0','EOF'];(H/(ds.get('part','')+pid+'-blank.dxf')).write_text('\n'.join(lines)+'\n')
def rib_dxf(pid):
 ds=next(p['metadata']['definition'] for p in parts if p['id']==pid);v=ds['profile_yz_in'];mn=[min(p[i] for p in v) for i in range(2)]
 pts=[[p[i]-mn[i] for i in range(2)] for p in v]
 lines=['0','SECTION','2','HEADER','9','$INSUNITS','70','1','0','ENDSEC','0','SECTION','2','ENTITIES']
 for a,b in zip(pts,pts[1:]+pts[:1]):lines+=['0','LINE','8','PROFILE','10',str(a[0]),'20',str(a[1]),'11',str(b[0]),'21',str(b[1])]
 lines+=['0','ENDSEC','0','EOF'];(H/(pid+'-blank.dxf')).write_text('\n'.join(lines)+'\n')
for pid in ['F1-LOW-RIB-R','F1-UP-RIB-R','F3-UP-RIB-R']:rib_dxf(pid)
for pid,a in [('F1-CAP','z'),('F1-SOLE','z'),('SEAT-PAN','z'),('BACK-PAN','x')]:dxf(pid,a)
# Raster illustration directly from tessellated solids; not generated imagery.
def render(path,chosen,width=1500,height=1100):
 u=np.array([.80,-.60,0.]);v=np.array([.24,.32,.916515]);view=np.cross(u,v);allv=[]
 for p in chosen:
  vv=np.array(p['positions']).reshape(-1,3);pp=np.column_stack([vv@u,-vv@v]);allv.extend(pp)
 a=np.array(allv);lo=a.min(0);hi=a.max(0);scale=min((width-120)/(hi[0]-lo[0]),(height-120)/(hi[1]-lo[1]));o=np.array([width/2,height/2])-(hi+lo)/2*scale
 # A depth buffer prevents large plate triangles from incorrectly covering nearer tubes.
 pixels=np.empty((height,width,3),dtype=np.uint8);pixels[:]=[243,241,234]
 depth=np.full((height,width),-np.inf)
 for p in chosen:
  vv=np.array(p['positions']).reshape(-1,3);pp=np.column_stack([vv@u,-vv@v])*scale+o;zz=vv@view
  for face in np.array(p['indices']).reshape(-1,3):
   tri=vv[face];n=np.cross(tri[1]-tri[0],tri[2]-tri[0]);nn=np.linalg.norm(n)
   if nn<1e-10:continue
   pts=pp[face];x0=max(0,int(np.floor(pts[:,0].min())));x1=min(width-1,int(np.ceil(pts[:,0].max())));y0=max(0,int(np.floor(pts[:,1].min())));y1=min(height-1,int(np.ceil(pts[:,1].max())))
   if x1<x0 or y1<y0:continue
   A,B,C=pts;den=(B[1]-C[1])*(A[0]-C[0])+(C[0]-B[0])*(A[1]-C[1])
   if abs(den)<1e-10:continue
   yy,xx=np.mgrid[y0:y1+1,x0:x1+1];xx=xx+.5;yy=yy+.5
   aa=((B[1]-C[1])*(xx-C[0])+(C[0]-B[0])*(yy-C[1]))/den
   bb=((C[1]-A[1])*(xx-C[0])+(A[0]-C[0])*(yy-C[1]))/den;cc=1-aa-bb
   z=aa*zz[face[0]]+bb*zz[face[1]]+cc*zz[face[2]];old=depth[y0:y1+1,x0:x1+1]
   mask=(aa>=-1e-7)&(bb>=-1e-7)&(cc>=-1e-7)&(z>old)
   shade=.60+.35*abs(float(n/nn@np.array([.2,-.4,.8944])));col=[min(255,int(int(p['color'][j:j+2],16)*shade+20)) for j in (1,3,5)]
   old[mask]=z[mask];pixels[y0:y1+1,x0:x1+1][mask]=col
 Image.fromarray(pixels).save(path)
render(H/'C21-bench-assembled.png',[p for p in parts if p['group'] not in ('context','floor')])
render(H/'C21-bench-exposed.png',[p for p in parts if p['group'] not in ('padding','pan','context','floor')])
render(H/'C21-foot-detail.png',[p for p in parts if p['id'].startswith('F1-')],1100,900)
# Full coach browser geometry reuses retained C1 physical parts; seat reference boxes are removed.
c1=json.loads(gzip.decompress((D/'assets/coach-body-c1/model.json.gz').read_bytes()));coach=[]
for p in c1['parts']:
 if p['group'] in ('seats','scale','floor'):continue
 coach.append(p)
for n,x in enumerate(P['row_x'],1):
 for side,dy in [('R',0),('L',-64)]:
  for p in parts:
   if p['group'] in ('context','floor'):continue
   q=copy.deepcopy(p);q['id']=f'C21-{n:02}{side}-'+p['id'];v=np.array(q['positions']).reshape(-1,3)+[x,dy,0];q['positions']=v.reshape(-1).tolist()
   q['group']='c21-'+p['group'];q['centre_in']=[p['centre_in'][i]+[x,dy,0][i] for i in range(3)]
   q['bounds_in']={a:[b+x if a=='x' else b+dy if a=='y' else b for b in p['bounds_in'][a]] for a in 'xyz'}
   q['metadata']['location']={'bench':f'{n:02}{side}','offset_xyz_in':[x,dy,0]};coach.append(q)
# Recreate only floor panel geometry with both C1 bracket notches and C2 expanded seat openings.
panels=json.loads((D/'assets/body-o1/audit-and-calculations.json').read_text())['panels']
for pp in panels:
 x0,x1,y0,y1=pp['bounds_xy_in'];sh=box({'x':[x0,x1],'y':[y0,y1],'z':[31.1220472441,31.8720472441]})
 for x in P['row_x']:
  for dx in P['feet_x']:
   for y in [-44,-20,20,44]:
    if x+dx+1.9375<x0 or x+dx-1.9375>x1 or y+3.1875<y0 or y-3.1875>y1:continue
    sh=sh.cut(box({'x':[x+dx-1.9375,x+dx+1.9375],'y':[y-3.1875,y+3.1875],'z':[30,33]}))
 for xp in [25,57,89,121,153,185,217,249,281]:
  for sg in [-1,1]:
   yy=[49.5,56] if sg>0 else [-56,-49.5];sh=sh.cut(box({'x':[xp-2.625,xp+2.625],'y':yy,'z':[30,33]}))
 vv,ff=sh.tessellate(.6,.12);q={'id':'C21-'+pp['id'],'name':'Floor panel with C2.1/C1 notches','group':'floor','positions':[v for pt in vv for v in (pt.x/MM,pt.y/MM,pt.z/MM)],'indices':[v for f in ff for v in f],'color':'#b69f78','opacity':1,'bounds_in':{'x':[x0,x1],'y':[y0,y1],'z':[31.1220472441,31.8720472441]},'centre_in':[(x0+x1)/2,(y0+y1)/2,31.4970472441],'dimensions_xyz_in':[x1-x0,y1-y0,.75],'metadata':{'definition':{'C2_opening_in':P['panel_opening'],'edge_closeout':'Unresolved, not yet released'},'material':{'candidate':'H-P125 floor panel alternative'}}};coach.append(q)
cg=[g for g in c1['groups'] if g['id'] not in ('seats','scale')]+[{**g,'id':'c21-'+g['id']} for g in groups if g['id'] not in ('context','floor')]
(H/'coach-assembly.json').write_text(json.dumps({'schema':'C21-instance-assembly-1','title':'C1 body with C2.1 physical benches / revised floor openings','base_model':'../coach-body-c1/model.json.gz','bench_model':'model.json.gz','base_excluded_groups':['seats','scale','floor'],'bench_excluded_groups':['context','floor'],'instances':[{'id':f'C21-{n:02}{side}','translation_in':[x,dy,0]} for n,x in enumerate(P['row_x'],1) for side,dy in [('R',0),('L',-64)]],'groups':cg,'floor_parts':[p for p in coach if p['group']=='floor'],'notes':['Same C2.1 bench geometry placed 16 times; no separate redrawn model.','C1 body connections, complete trucks, stairs, couplings and HVAC are still unfinished.']},separators=(',',':')))
# Full coach uses the same instanced browser mesh; software raster omitted to avoid redundant heavy export.
# Positive-volume interference within new bench parts; compatible threaded envelopes excluded.
over=[]
checked=[p for p in parts if p['group'] not in ('hardware','padding')]
for i,a in enumerate(checked):
 for b in checked[i+1:]:
  if a['group'] in ('context','floor') and b['group'] in ('context','floor'):continue
  if all(min(a['bounds_in'][k][1],b['bounds_in'][k][1])-max(a['bounds_in'][k][0],b['bounds_in'][k][0])>.003 for k in 'xyz'):
   vol=S[a['id']].intersect(S[b['id']]).Volume()/MM**3
   if vol>1e-5:over.append({'a':a['id'],'b':b['id'],'in3':vol})
socket_hits=[]
for fi,(x,y) in enumerate([(x,y) for x in P['feet_x'] for y in P['feet_y']],1):
 for bi,(dx,dy) in enumerate(P['bolt_xy_offsets'],1):
  for side,z,length in [('upper_6in',P['sole_top_z']+.125,6),('upper_short_2in',P['sole_top_z']+.125,2),('lower',P['steel_top_z']-4,3.875)]:
   env=cyl(.625,length,(x+dx,y+dy,z))
   for p in parts:
    if p['group'] not in ('frame','hardpoint','context','floor'):continue
    if p['id'].endswith('-CAP') or p['id'].endswith('-SOLE') or '-SP' in p['id']:continue
    bb=p['bounds_in']
    if bb['x'][1]<x+dx-.625 or bb['x'][0]>x+dx+.625 or bb['y'][1]<y+dy-.625 or bb['y'][0]>y+dy+.625 or bb['z'][1]<z or bb['z'][0]>z+length:continue
    vol=env.intersect(S[p['id']]).Volume()/MM**3
    if vol>1e-5:socket_hits.append({'foot':fi,'bolt':bi,'side':side,'part':p['id'],'in3':vol})
contacts=[]
for pid in P['brace_workpoints_in']:
 for rec in next(p for p in parts if p['id']==pid)['metadata']['definition']['cope_to_members']:
  contacts.append({'brace':pid,'receiving_part':rec,'minimum_distance_in':S[pid].distance(S[rec])/MM,'interference_in3':S[pid].intersect(S[rec]).Volume()/MM**3})
contacts.append({'brace':'BV1','receiving_part':'BV2 apex miter','minimum_distance_in':S['BV1'].distance(S['BV2'])/MM,'interference_in3':S['BV1'].intersect(S['BV2']).Volume()/MM**3})
(H/'joint-geometry.json').write_text(json.dumps({'brace_receiving_contacts':contacts,'socket_envelope_hits':socket_hits,'socket_nominal_rib_clearance_in':.0625,'cope_clearance_note':'Rebuilt receiving envelopes yield approximately0.00010577in (0.00269mm) CAD residual clearance at brace faces; not a specified production weld-root gap. Actual HSS/WPS/fit tolerances remain open.','notes':['Zero distance only verifies nominal contact; weld throat and fatigue not qualified.','1.25in OD cylinder is a preliminary socket envelope. Ratchet and technician reach not modeled.']},indent=2))
mass=collections.defaultdict(float)
for p in parts:
 if p['group'] not in ('context','floor','padding'):mass[p['group']]+=p['metadata'].get('catalog_mass_kg',p['metadata']['solid_mass_kg'])
verification={'valid_solids':all(s.isValid() for s in S.values()),'prototype_mesh_parts':len(parts),'coach_mesh_parts':len(coach),'new_bench_intersections':over,'scope':'New non-hardware solids, including cropped source rails and floor. Thread mating excluded; nominal CAD only. Not a complete tolerance, weld or passenger-envelope test.','mass_per_bench_kg_by_group':dict(mass),'socket_envelope_hits':socket_hits,'mass_inclusions':'Catalog HSS + CAD plate/nominal hardware; excludes upholstery, finish, sealing boots, small panel hardware and all undeveloped local reinforcements.'}
(H/'verification.json').write_text(json.dumps(verification,indent=2));print(json.dumps(verification))

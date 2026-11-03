"""C3 R0 folding-seat CAD. Dimensional inputs inches; CAD/STEP mm; web mesh and DXF inches. Preliminary review only."""
from pathlib import Path
import json, math, copy, collections
import cadquery as cq
import numpy as np
from PIL import Image
H=Path(__file__).resolve().parent;D=H.parents[1];MM=25.4
P={'revision':'PF-3O2-C3-R0','units':'inches','status':'PRELIMINARY — NOT FOR FABRICATION','floor_z':32,'hinge_axis':[64,-32,48.5],'rotation_axis':'global +Y; physical stow angle -90deg','seat_pan_bounds':{'x':[62.5,82],'y':[-44,-20],'z':[48.5,48.625]},'cushion_bounds':{'x':[62.5,82],'y':[-44,-20],'z':[48.625,50]},'back_face_x':62.25,'back_bottom_z':50.25,'mechanism_centers_y':[-45,-19],'hinge_pin_dia':.75,'hinge_bushing_OD':1,'hinge_bushing_ID':.753,'moving_sector_t':.5,'sector_R':1.75,'clevis_t':.375,'running_gap_each_side':.0625,'latch_pin_dia':.625,'latch_hole_dia':.65625,'latch_radius':1.15,'fixed_latch_xz':[64-1.15/math.sqrt(2),48.5+1.15/math.sqrt(2)],'deployed_stop_xz':[[65,65.5],[48,48.5]],'stowed_stop_xz':[[64,64.5],[47.125,47.625]],'support_strip':{'x':[60,66],'y':[-52,-16]},'feet':[[62.5,-44],[62.5,-20]],'cap_size':[5,6,.75],'sole_size':[5,6,1],'bolt_offsets':[[-1.75,-2],[-1.75,2],[1.75,-2],[1.75,2]],'steel_top_z':31.003937007874,'sole_under_z':32.25,'sole_top_z':33.25,'mount_status':'Proposed two-foot cantilever foundation; separate from regular-bench C2.1','back_top_z':70,'states_deg':[0,45,90]}
P['cap_top_z']=P['steel_top_z']+.75;P['spacer_length']=P['sole_under_z']-P['cap_top_z']
S={};parts=[];edges={};families={};moving=[];latches=[]
colors={'fixed':'#35695a','moving':'#498b70','hardware':'#83949b','mount':'#b28a42','pan':'#b7b7ad','padding':'#8d3d38','guard':'#d4b05f','context':'#87969c','floor':'#b69f78'}
groups=[{'id':k,'label':v,'explosion_vector_in':e,'default_visible':k not in ('padding','guard')} for k,v,e in [('fixed','Fixed uprights and clevises',[0,0,0]),('moving','Folding frame and sectors',[4,0,5]),('hardware','Hinge bushings, pins and retained locks',[0,-7,0]),('mount','Proposed steel floor bypass',[0,0,-6]),('pan','Seat and back pans',[4,0,8]),('padding','Cushion proposal',[7,0,12]),('guard','Pinch covers—review incomplete',[0,5,3]),('context','Retained steel rail context',[0,0,-10]),('floor','Floor context',[0,0,-7])]]
def box(b):return cq.Solid.makeBox(*[(b[a][1]-b[a][0])*MM for a in 'xyz'],cq.Vector(*[b[a][0]*MM for a in 'xyz']))
def cyl(r,l,p,a=(0,0,1)):return cq.Solid.makeCylinder(r*MM,l*MM,cq.Vector(*[v*MM for v in p]),cq.Vector(*a))
def hollow(b,a,t):
 s=box(b);inn={k:[b[k][0]+t,b[k][1]-t] for k in 'xyz'};inn[a]=[b[a][0]-1,b[a][1]+1]
 return cq.Workplane(obj=s).edges('|'+a.upper()).fillet(2*t*MM).val().cut(cq.Workplane(obj=box(inn)).edges('|'+a.upper()).fillet(t*MM).val())
def ec(s):return [[[p.x/MM,p.y/MM,p.z/MM] for p in [e.positionAt(t) for t in np.linspace(0,1,2 if e.geomType()=='LINE' else 25)]] for e in s.Edges()]
def mesh(pid,name,g,s,d,material='ASTM A36 candidate',density=7850,move=False):
 assert s.isValid(),pid
 vv,ff=s.tessellate(.7,.16);bb=s.BoundingBox();b={a:[getattr(bb,a+'min')/MM,getattr(bb,a+'max')/MM] for a in 'xyz'}
 p={'id':pid,'name':name,'group':g,'positions':[round(v,6) for q in vv for v in (q.x/MM,q.y/MM,q.z/MM)],'indices':[v for f in ff for v in f],'bounds_in':b,'centre_in':[(lo+hi)/2 for lo,hi in b.values()],'dimensions_xyz_in':[hi-lo for lo,hi in b.values()],'color':colors[g],'opacity':1,'display_only':g in ('padding','context','floor'),'metadata':{'family':d.get('family',pid),'material':{'candidate':material},'definition':d,'solid_mass_kg':s.Volume()/1e9*density,'moving':move,'engineering_status':'PRELIMINARY — NOT RELEASED'}}
 parts.append(p);S[pid]=s;edges[pid]=ec(s)
 if move:moving.append(pid)
 fam=d.get('family',pid)
 if fam not in families:families[fam]={'id':fam,'name':name,'quantity_per_fold_seat':0,'material':material,'definition':d,'representative':pid}
 families[fam]['quantity_per_fold_seat']+=1
 return s

def plate(pid,g,b,holes=[],axis='z',material='ASTM A36 candidate',density=7850,move=False,extra={}):
 s=box(b);inds={'x':('y','z'),'y':('x','z'),'z':('x','y')}[axis];v={'x':(1,0,0),'y':(0,1,0),'z':(0,0,1)}[axis]
 for u,w,d in holes:
  q={axis:b[axis][0]-1,inds[0]:u,inds[1]:w};s=s.cut(cyl(d/2,b[axis][1]-b[axis][0]+2,[q[a] for a in 'xyz'],v))
 return mesh(pid,pid.replace('-',' '),g,s,{'bounds_in':b,'holes':holes,'hole_axis':axis,**extra},material,density,move)
def tube(pid,g,b,a,t=.125,move=False):return mesh(pid,'Rounded hollow structural tube',g,hollow(b,a,t),{'section_in':[b[k][1]-b[k][0] for k in 'xyz' if k!=a]+[t],'axis':a,'length_in':b[a][1]-b[a][0]},'ASTM A500 Grade C candidate',7850,move)
def profile_xz(points,y,t):return cq.Workplane(cq.Plane(origin=(0,y*MM,0),xDir=(1,0,0),normal=(0,-1,0))).polyline([(x*MM,z*MM) for x,z in points]).close().extrude(-t*MM).val()
def ring(od,id,l,p,axis=(0,1,0)):return cyl(od/2,l,p,axis).cut(cyl(id/2,l+2,tuple(p[i]-axis[i] for i in range(3)),axis))
# Floor bypass, all occupied envelopes fit the permanent 6in strip.
for i,(x,y) in enumerate(P['feet'],1):
 holes=[(x+dx,y+dy,.5625) for dx,dy in P['bolt_offsets']]
 plate(f'F{i}-CAP','mount',{'x':[x-2.5,x+2.5],'y':[y-3,y+3],'z':[P['steel_top_z'],P['cap_top_z']]},holes,extra={'family':'M-CAP','status':P['mount_status']})
 plate(f'F{i}-SOLE','mount',{'x':[x-2.5,x+2.5],'y':[y-3,y+3],'z':[32.25,33.25]},holes,extra={'family':'M-SOLE','status':P['mount_status']})
 for sy in (-1,1):
  yy=[y-1.375,y-1] if sy<0 else [y+1,y+1.375]
  plate(f'F{i}-CHEEK{sy}','mount',{'x':[x-2.5,x+2.5],'y':yy,'z':[28.003937,P['steel_top_z']]},extra={'family':'M-CHEEK','role':'Rail side cheek; weld and rail transfer subject to foundation screen'})
 for j,(xx,yy,d) in enumerate(holes,1):
  mesh(f'F{i}-SP{j}','Machined floor bypass spacer','mount',ring(1,.5625,P['spacer_length'],(xx,yy,P['cap_top_z']),(0,0,1)),{'family':'M-SPACER','OD_in':1,'ID_in':.5625,'length_in':P['spacer_length'],'fit':'Matched finished set after actual weld/floor measurements'})
  for t,z in [('TOP',33.25),('LOW',P['steel_top_z']-.125)]:mesh(f'F{i}-W{j}-{t}','Nominal F436 washer','hardware',ring(1.0625,.53125,.125,(xx,yy,z),(0,0,1)),{'family':'M-WASHER','OD_in':1.0625,'ID_in':.53125,'display_t_in':.125,'actual_t_range_in':[.097,.177]},'ASTM F436 candidate')
  sh=cyl(.25,3.25,(xx,yy,30.125)).fuse(cyl(.4375,.3125,(xx,yy,33.375)))
  mesh(f'F{i}-B{j}','1/2in candidate bolt envelope','hardware',sh,{'family':'M-BOLT','diameter_in':.5,'under_head_in':3.25,'head':'Simplified round clearance envelope; select certified bolt and locking detail'},'SAE J429 Grade 8 candidate')
  mesh(f'F{i}-N{j}','Nut envelope—locking unresolved','hardware',ring(.875,.5,.4375,(xx,yy,P['steel_top_z']-.5625),(0,0,1)),{'family':'M-NUT','locking':'Positive locking detail not selected'},'SAE J995 Grade 8 candidate')
 plate(f'F{i}-BOTTOM-TIE','mount',{'x':[x-2.5,x+2.5],'y':[y-1.375,y+1.375],'z':[27.628937,28.003937]},extra={'family':'M-BOTTOM-TIE','role':'Closed rail saddle tie; weld/end transfer unqualified'})
 for sign in (-1,1):
  verts=[(y+sign*1.375,29.003937),(y+sign*1.375,P['steel_top_z']),(y+sign*3,P['steel_top_z'])]
  rib=cq.Workplane(cq.Plane(origin=((x-.25)*MM,0,0),xDir=(0,1,0),normal=(1,0,0))).polyline([(yy*MM,zz*MM) for yy,zz in verts]).close().extrude(.5*MM).val()
  mesh(f'F{i}-LOW-RIB{sign}','Cap wing rib','mount',rib,{'family':'M-LOW-RIB','profile_yz_in':verts,'x_limits_in':[x-.25,x+.25],'thickness_in':.5,'role':'Cap wing to rail side cheek; welding unqualified'})
 # Post aft of pivot; both feet align existing rails in Y.
 tube(f'POST{i}','fixed',{'x':[60.25,62.25],'y':[y-1,y+1],'z':[33.25,70]},'z',.1875)
 # Forward post-to-sole stiffener, outside bolt approaches.
 rib=profile_xz([(62.25,33.25),(65,33.25),(65,33.75),(62.25,36.25)],y-.25,.5)
 mesh(f'F{i}-UP-RIB','Forward post triangular rib','mount',rib,{'family':'M-UP-RIB','profile_xz_in':[[62.25,33.25],[65,33.25],[65,33.75],[62.25,36.25]],'thickness_in':.5,'role':'Proposed load path; weld/root access and plate contact unresolved'})
 # Rail context cropped only, not a stock cut length.
 tube(f'CTX-RAIL{i}','context',{'x':[57,70],'y':[y-1,y+1],'z':[28.003937,P['steel_top_z']]},'x',.1875)
# Upright back structure. Back pads have a 1/4in nominal separation from stowed seat padding.
for z in (51,68.5):tube('BACK-RAIL-'+str(z),'fixed',{'x':[60.25,61.75],'y':[-43,-21],'z':[z,z+1.5]},'y')
plate('BACK-PAN','pan',{'x':[61.75,61.875],'y':[-43,-21],'z':[50.25,70]},axis='x',material='5052-H32 aluminum candidate',density=2680,extra={'fastening':'Panel retention tabs/bolts remain to develop'})
plate('BACK-PAD','padding',{'x':[61.875,62.25],'y':[-43,-21],'z':[50.25,70]},axis='x',material='Upholstery envelope; foam/cover/retention not specified',density=50)
# Seat welded frame — square cuts meet at faces, no interpenetrating tubes.
tube('MOV-REAR','moving',{'x':[62.5,64],'y':[-44,-20],'z':[47,48.5]},'y',move=True)
tube('MOV-FRONT','moving',{'x':[80.5,82],'y':[-44,-20],'z':[47,48.5]},'y',move=True)
for j,y in enumerate((-44,-21.5),1):tube(f'MOV-SIDE{j}','moving',{'x':[64,80.5],'y':[y,y+1.5],'z':[47,48.5]},'x',move=True)
tube('MOV-MID','moving',{'x':[71.5,73],'y':[-42.5,-21.5],'z':[47,48.5]},'y',move=True)
plate('MOV-PAN','pan',P['seat_pan_bounds'],material='5052-H32 aluminum candidate',density=2680,move=True,extra={'fastening':'Removable pan tabs/bolts remain to detail; 1.5in rear overhang supported by rear cross tube'})
pad=box(P['cushion_bounds'])
for yy in ([-44,-42.875],[-21.125,-20]):pad=pad.cut(box({'x':[62.4,64],'y':yy,'z':[48.5,50.1]}))
mesh('MOV-PAD','Seat cushion with rear corner clearances','padding',pad,{'bounds_in':P['cushion_bounds'],'rear_corner_cutouts_in':{'x':[62.5,64],'y':[[-44,-42.875],[-21.125,-20]]},'status':'Foam/cover/retention not specified; notch edges and comfort require mockup'},'Upholstery envelope',50,True)
# Two independent hinge/stop/positive-lock modules.
for i,y in enumerate(P['mechanism_centers_y'],1):
 c0=y-.25;c1=y+.25;cheeks=[(c0-.0625-.375,c0-.0625),(c1+.0625,c1+.0625+.375)]
 # Upper semicircle plus central boss; two latch bores index 0 and 90 degrees.
 sector=cyl(1.75,.5,(64,c0,48.5),(0,1,0)).intersect(box({'x':[62,66],'y':[c0-.1,c1+.1],'z':[48.5,51]})).fuse(cyl(.75,.5,(64,c0,48.5),(0,1,0)))
 tang=box({'x':[65.5625,68.25],'y':[c0,c1],'z':[47,49]});sector=sector.fuse(tang)
 sector=sector.cut(cyl(.5,2,(64,c0-.5,48.5),(0,1,0)))
 for angle in (45,135):
  xx=64+1.15*math.cos(math.radians(angle));zz=48.5+1.15*math.sin(math.radians(angle));sector=sector.cut(cyl(.65625/2,2,(xx,c0-.5,zz),(0,1,0)))
 mesh(f'MOV-SECTOR{i}','Upper semicircular sector and frame tang','moving',sector,{'family':'H-SECTOR','radius_in':1.75,'thickness_in':.5,'boss_radius_in':.75,'hinge_bore_in':1,'latch_pitch_radius_in':1.15,'latch_angles_deg':[45,135],'latch_bores_in':.65625,'stop_arm_in':1.25,'tang_bounds_in':{'x':[65.5625,68.25],'z':[47,49]}},move=True)
 # Connector bridges the outboard sector tang to the corresponding seat side face.
 yy=[c1,-44] if i==1 else [-20,c0]
 plate(f'MOV-TIE{i}','moving',{'x':[67.25,68.25],'y':yy,'z':[47,48.5]},move=True,extra={'family':'H-TIE','role':'Welded stepped tie from sector tang to side rail; no weld sized'})
 for j,(a,b) in enumerate(cheeks,1):
  holes=[(64,48.5,.78125),(*P['fixed_latch_xz'],.65625)]
  plate(f'H{i}-CHEEK{j}','fixed',{'x':[62.25,65.75],'y':[a,b],'z':[46.25,50.75]},holes,axis='y',extra={'family':'H-CHEEK','load_path':'One cheek directly meets post face; top bridge and stop blocks connect the pair'})
 # Top bridge leaves at least 0.125 to sector arc at full travel.
 plate(f'H{i}-TOP-BRIDGE','fixed',{'x':[62.25,62.625],'y':[cheeks[0][1],cheeks[1][0]],'z':[50.375,50.75]},extra={'family':'H-BRIDGE','role':'Cheek spacing tie; nominal sector radial clearance .125in'})
 plate(f'H{i}-STOP-DOWN','fixed',{'x':[65,65.5],'y':[cheeks[0][1],cheeks[1][0]],'z':[48,48.5]},extra={'family':'H-STOP-D','role':'Hard down stop; moving radial face carries downward load; latch is separate'})
 plate(f'H{i}-STOP-UP','fixed',{'x':[64,64.5],'y':[cheeks[0][1],cheeks[1][0]],'z':[47.125,47.625]},extra={'family':'H-STOP-U','role':'Hard stowed stop; contact at moving sector radial face at -90deg'})
 mesh(f'H{i}-BUSH','Replaceable plain sleeve bushing','hardware',ring(1,.753,.5,(64,c0,48.5)),{'family':'H-BUSH','OD_in':1,'ID_in':.753,'length_in':.5,'fit':'Nominal diameters only; final fits, lubricant and retention to select'},'Bronze candidate',8800,True)
 pinstart=cheeks[0][0]-.125;pinend=cheeks[1][1]+.25
 pin=cyl(.375,pinend-pinstart,(64,pinstart,48.5),(0,1,0)).fuse(cyl(.625,.125,(64,pinstart-.125,48.5),(0,1,0)))
 mesh(f'H{i}-PIN','3/4in hinge pin with head envelope','hardware',pin,{'family':'H-PIN','diameter_in':.75,'shank_length_in':pinend-pinstart,'retention':'Head plus retained end washer; positive end fastener detail not finalized'},'Certified alloy steel pin candidate')
 mesh(f'H{i}-PIN-RETAINER','Retained washer envelope','hardware',ring(1.25,.78125,.125,(64,pinend-.125,48.5)),{'family':'H-RETAINER','retention':'Positive fastener/cotter not yet detailed'},'Steel candidate')
 lx,lz=P['fixed_latch_xz'];lpstart=cheeks[0][0]-.375;length=cheeks[1][1]+.125-lpstart
 lp=cyl(.3125,length,(lx,lpstart,lz),(0,1,0)).fuse(cyl(.4375,.1875,(lx,lpstart-.1875,lz),(0,1,0)))
 if i==2:
  lpstart=cheeks[0][0]-.125;length=cheeks[1][1]+.375-lpstart
  lp=cyl(.3125,length,(lx,lpstart,lz),(0,1,0)).fuse(cyl(.4375,.1875,(lx,lpstart+length,lz),(0,1,0)))
 mesh(f'H{i}-LOCK','5/8in positive lock pin — capture unfinished','hardware',lp,{'family':'H-LOCK','diameter_in':.625,'index_states_deg':[0,90],'actuation':'Two manual positive locking pins; withdraw outward during motion; captive/anti-release design unfinished','retention':'Captive sleeve and anti-release detent not supplier-selected'},'Alloy steel candidate')
 latches.append(f'H{i}-LOCK')
 # Outer guards are real plates, with only pin access openings; finger safety still unqualified.
 for j,(a,b) in enumerate(cheeks,1):
  gy=a-.1875 if j==1 else b+.125
  plate(f'H{i}-GUARD{j}','guard',{'x':[62.25,65.875],'y':[gy,gy+.0625],'z':[46.125,50.875]},[(64,48.5,1.3125),(lx,lz,1)],axis='y',material='5052-H32 aluminum candidate',density=2680,extra={'family':'H-GUARD','status':'Face cover proposal only; exposed underside/tang and pin holes need finger/pinch validation; mounting screws not developed'})
# Floor opening leaves each sole above the surface; floors carry no seat-anchor loads.
floor=box({'x':[57,70],'y':[-50,-14],'z':[31.1220472441,32]})
for x,y in P['feet']:floor=floor.cut(box({'x':[x-2.625,x+2.625],'y':[y-3.125,y+3.125],'z':[30,33]}))
mesh('FLOOR','Floor panel with isolated mount cutouts','floor',floor,{'thickness_in':32-31.1220472441,'openings_in':[5.25,6.25],'status':'Floor edge closeout/seal/boots not engineered'},'Panel stack envelope',200)
# Serialize canonical reference before expensive checks, for common drawing consumers.
def writej(n,o):
 import gzip
 raw=(json.dumps(o,separators=(',',':')) if n.startswith(('model','drawing-edges')) else json.dumps(o,indent=2)).encode()
 if n.startswith('model-'):
  packed=gzip.compress(raw,compresslevel=9,mtime=0);assert gzip.decompress(packed)==raw
  (H/(n+'.gz')).write_bytes(packed)
  if (H/n).exists():(H/n).unlink()
 else:(H/n).write_bytes(raw)
model={'schemaVersion':3,'units':'inches','title':'C3 forward-facing folding seat / two-foot foundation','coordinate_system':'Coach coordinates; X forward, Y transverse, Z above rail','groups':groups,'parts':parts,'notes':['Real nominal solids; preliminary mechanism and mounting proposal.','Hardware envelopes are not supplier exact parts. Welds, positive retention, guarding and cycle/proof tests unresolved.','Seat rotates -90deg about global Y. Retract both locks before motion.']}
writej('parameters.json',P);writej('parts.json',[{k:p[k] for k in ('id','name','group','bounds_in','metadata')} for p in parts]);writej('drawing-edges.json',edges);writej('bom.json',list(families.values()))
print('CANONICAL_WRITTEN',len(parts),flush=True)
# State meshes and edge collections share one kinematic transform.
def rotated(s,angle):return s.rotate((64*MM,0,48.5*MM),(64*MM,MM,48.5*MM),-angle)
def state(angle):
 ss={};pp=copy.deepcopy(parts)
 for p in pp:
  pid=p['id'];sh=rotated(S[pid],angle) if pid in moving else S[pid]
  if pid in latches and angle not in (0,90):sh=sh.translate((0,(-1.75 if pid.startswith('H1') else 1.75)*MM,0))
  ss[pid]=sh
  if pid in moving or pid in latches:
   vv,ff=sh.tessellate(.7,.16);p['positions']=[round(v,6) for q in vv for v in (q.x/MM,q.y/MM,q.z/MM)];p['indices']=[v for f in ff for v in f];bb=sh.BoundingBox();p['bounds_in']={a:[getattr(bb,a+'min')/MM,getattr(bb,a+'max')/MM] for a in 'xyz'};p['centre_in']=[sum(p['bounds_in'][a])/2 for a in 'xyz']
 return ss,pp
states={}
for a in (0,45,90):
 ss,pp=state(a);states[a]=(ss,pp);m=copy.deepcopy(model);m['parts']=pp;m['title']=f'C3 folding seat {a}deg';writej({0:'model-deployed.json',45:'model-mid.json',90:'model-stowed.json'}[a],m)
 writej(f'drawing-edges-{a}.json',{k:ec(s) for k,s in ss.items()})
 if a in (0,90):cq.exporters.export(cq.Compound.makeCompound([s for k,s in ss.items() if next(p for p in parts if p['id']==k)['group'] not in ('padding','context','floor')]),str(H/f'C3-fold-seat-{a}-R0.step'))
# Generate generic 1:1 part blank DXF for simple plates; no fabrication release.
for pid in ('MOV-PAN','BACK-PAN','F1-CAP','F1-SOLE','H1-CHEEK1'):
 p=next(p for p in parts if p['id']==pid);d=p['metadata']['definition'];b=d['bounds_in'];axis=d['hole_axis'];uv={'x':('y','z'),'y':('x','z'),'z':('x','y')}[axis];w=b[uv[0]][1]-b[uv[0]][0];h=b[uv[1]][1]-b[uv[1]][0]
 lines=['0','SECTION','2','HEADER','9','$INSUNITS','70','1','0','ENDSEC','0','SECTION','2','ENTITIES']
 for x0,y0,x1,y1 in [(0,0,w,0),(w,0,w,h),(w,h,0,h),(0,h,0,0)]:lines+=['0','LINE','8','PROFILE','10',str(x0),'20',str(y0),'11',str(x1),'21',str(y1)]
 for x,y,dia in d.get('holes',[]):lines+=['0','CIRCLE','8','HOLES','10',str(x-b[uv[0]][0]),'20',str(y-b[uv[1]][0]),'40',str(dia/2)]
 lines+=['0','ENDSEC','0','EOF'];(H/f'{pid}-blank.dxf').write_text('\n'.join(lines)+'\n')
# Bbox-pruned exact intersections. Connected contacts are not penetration.
def bb(s):
 q=s.BoundingBox();return np.array([[q.xmin,q.xmax],[q.ymin,q.ymax],[q.zmin,q.zmax]])
def overlap(a,b):return np.all(np.minimum(a[:,1],b[:,1])-np.maximum(a[:,0],b[:,0])>1e-5)
collisions=[];sweep=[];fixedids=[p['id'] for p in parts if p['id'] not in moving and p['id'] not in latches and p['group'] not in ('context','floor')]
for a in range(0,91,5):
 ms={k:rotated(S[k],a) for k in moving};hits=[]
 for mid,sh in ms.items():
  mb=bb(sh)
  for fid in fixedids:
   if overlap(mb,bb(S[fid])):
    vol=sh.intersect(S[fid]).Volume()/MM**3
    if vol>1e-6:hits.append({'moving':mid,'fixed':fid,'overlap_in3':vol})
 sweep.append({'angle_deg':a,'penetrations':hits});collisions.extend([{'angle_deg':a,**h} for h in hits])
 # Locks must be removed and re-engaged only at indexed endpoints.
# Static physical-part checks, excluding ring pin intended running-fit contacts.
static=[]
physical=[p for p in parts if p['group'] not in ('context','floor','padding')]
for i,p in enumerate(physical):
 for q in physical[i+1:]:
  if not overlap(bb(S[p['id']]),bb(S[q['id']])):continue
  v=S[p['id']].intersect(S[q['id']]).Volume()/MM**3
  if v>1e-6:static.append({'a':p['id'],'b':q['id'],'overlap_in3':v})
fixedbounds=bb(cq.Compound.makeCompound([S[p['id']] for p in physical if p['id'] not in moving]))/MM
stowedbounds=bb(cq.Compound.makeCompound([states[90][0][p['id']] for p in physical]))/MM
moveCG=np.zeros(3);moveMass=0
for p in parts:
 if p['id'] in moving:
  mass=p['metadata']['solid_mass_kg'];cent=S[p['id']].Center();moveCG+=mass*np.array([cent.x/MM,cent.y/MM,cent.z/MM]);moveMass+=mass
moveCG/=moveMass
lockchecks=[]
for angle in (0,45,90):
 ss,pp=states[angle]
 for lockid in latches:
  for p in pp:
   if p['id']==lockid or p['group'] in ('context','floor'):continue
   if overlap(bb(ss[lockid]),bb(ss[p['id']])):
    vol=ss[lockid].intersect(ss[p['id']]).Volume()/MM**3
    if vol>1e-6:lockchecks.append({'angle_deg':angle,'lock':lockid,'other':p['id'],'overlap_in3':vol})
writej('verification.json',{'lock_state_penetrations':lockchecks,'fixed_bounds_in':{a:fixedbounds[i].tolist() for i,a in enumerate('xyz')},'stowed_complete_physical_bounds_in':{a:stowedbounds[i].tolist() for i,a in enumerate('xyz')},'moving_mass_with_padding_kg':moveMass,'moving_center_of_mass_deployed_in':moveCG.tolist(),'revision':P['revision'],'all_solids_valid':all(s.isValid() for s in S.values()),'solid_part_count':len(parts),'physical_mass_kg':sum(p['metadata']['solid_mass_kg'] for p in physical),'moving_mass_kg_excluding_padding':sum(p['metadata']['solid_mass_kg'] for p in physical if p['id'] in moving),'static_penetrations':static,'sweep_angles_deg':list(range(0,91,5)),'sweep_penetrations':collisions,'sweep_results':sweep,'limitations':['Sampled5deg exact solid intersection is not continuous swept-volume proof or tolerance analysis.','Running clearances are not evidence of finger safety.','Pins withdrawn in transit; only endpoints are lockable.','Welds, lock capture/anti-release, fatigue, ergonomics and tests remain incomplete.']})
print('VERIFY',len(static),len(collisions),flush=True)
# Direct CAD raster with z-buffer; no generated-image geometry.
def render(path,chosen,width=1350,height=1000):
 u=np.array([.8,-.6,0]);v=np.array([.24,.32,.916515]);view=np.cross(u,v);allv=[]
 for p in chosen:
  vv=np.array(p['positions']).reshape(-1,3);allv.extend(np.column_stack([vv@u,-vv@v]))
 a=np.array(allv);lo=a.min(0);hi=a.max(0);scale=min((width-100)/(hi[0]-lo[0]),(height-100)/(hi[1]-lo[1]));o=np.array([width/2,height/2])-(hi+lo)/2*scale
 pixels=np.empty((height,width,3),dtype=np.uint8);pixels[:]=[243,241,234];depth=np.full((height,width),-np.inf)
 for p in chosen:
  vv=np.array(p['positions']).reshape(-1,3);pp=np.column_stack([vv@u,-vv@v])*scale+o;zz=vv@view
  for face in np.array(p['indices']).reshape(-1,3):
   tri=vv[face];n=np.cross(tri[1]-tri[0],tri[2]-tri[0]);nn=np.linalg.norm(n)
   if nn<1e-10:continue
   pts=pp[face];x0=max(0,int(np.floor(pts[:,0].min())));x1=min(width-1,int(np.ceil(pts[:,0].max())));y0=max(0,int(np.floor(pts[:,1].min())));y1=min(height-1,int(np.ceil(pts[:,1].max())))
   if x1<x0 or y1<y0:continue
   A,B,C=pts;den=(B[1]-C[1])*(A[0]-C[0])+(C[0]-B[0])*(A[1]-C[1])
   if abs(den)<1e-10:continue
   yy,xx=np.mgrid[y0:y1+1,x0:x1+1];xx=xx+.5;yy=yy+.5;aa=((B[1]-C[1])*(xx-C[0])+(C[0]-B[0])*(yy-C[1]))/den;bbv=((C[1]-A[1])*(xx-C[0])+(A[0]-C[0])*(yy-C[1]))/den;cc=1-aa-bbv;z=aa*zz[face[0]]+bbv*zz[face[1]]+cc*zz[face[2]];old=depth[y0:y1+1,x0:x1+1];mask=(aa>=-1e-7)&(bbv>=-1e-7)&(cc>=-1e-7)&(z>old);shade=.60+.35*abs(float(n/nn@np.array([.2,-.4,.8944])));col=[min(255,int(int(p['color'][j:j+2],16)*shade+20)) for j in (1,3,5)];old[mask]=z[mask];pixels[y0:y1+1,x0:x1+1][mask]=col
 Image.fromarray(pixels).save(path)
for a in (0,45,90):render(H/f'C3-fold-{a}.png',[p for p in states[a][1] if p['group'] not in ('context','floor','guard')])
render(H/'C3-mechanism.png',[p for p in parts if p['id'].startswith('H1-') or p['id'] in ('MOV-SECTOR1','MOV-TIE1')],1100,900)
print('DONE',flush=True)

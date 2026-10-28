"""C3.1 nominal CAD detail development. Requires preserved C3 source alongside.
Dimensional inputs inches; CAD/STEP millimetres; web/DXF inches. Not released.
"""
from pathlib import Path
import json,math,copy,collections,ast,gzip,zipfile,hashlib
import cadquery as cq
import numpy as np
H=Path(__file__).resolve().parent
baseline=H.parent/'coach-accessible-c3'/'build_c3.py'
source=baseline.read_text();prefix=source.split('# Serialize canonical reference')[0]
# Reparameterize the preserved baseline text in memory; never edit C3 artifacts.
prefix=prefix.replace("'sector_R':1.75","'sector_R':1.70").replace("sector=cyl(1.75,.5","sector=cyl(1.70,.5").replace("'radius_in':1.75","'radius_in':1.70")
prefix=prefix.replace("'cap_size':[5,6,.75]","'cap_size':[5,6,.875]").replace("'sole_size':[5,6,1]","'sole_size':[5,6,1.125]")
prefix=prefix.replace("[[-1.75,-2],[-1.75,2],[1.75,-2],[1.75,2]]","[[-1.75,-2.25],[-1.75,2.25],[1.75,-2.25],[1.75,2.25]]")
prefix=prefix.replace("'sole_top_z':33.25","'sole_top_z':33.375").replace("P['steel_top_z']+.75","P['steel_top_z']+.875")
prefix=prefix.replace("[32.25,33.25]","[32.25,33.375]").replace("('TOP',33.25)","('TOP',33.375)").replace("[33.25,70]","[33.375,70]")
exec(compile(prefix,str(baseline),'exec'),globals())
P.update(revision='PF-3O2-C31-R0',status='PRELIMINARY DETAIL DEVELOPMENT — NOT FOR FABRICATION')
P['baseline_source']='../coach-accessible-c3/build_c3.py'
P['baseline_source_sha256']=hashlib.sha256(baseline.read_bytes()).hexdigest()
colors.update({'flexible':'#4d6068','weld':'#b8a25a','indicator':'#2a8c4a'})
groups.extend([{'id':'flexible','label':'Rear flexible gap curtain','explosion_vector_in':[0,0,3],'default_visible':True},{'id':'weld','label':'Proposed weld volumes','explosion_vector_in':[0,0,0],'default_visible':False},{'id':'indicator','label':'Positive lock witness','explosion_vector_in':[0,0,0],'default_visible':True}])

# Keep common family identifiers and stable inherited part IDs where feasible.
def forget(pid):
 global parts
 parts=[p for p in parts if p['id']!=pid];S.pop(pid,None);edges.pop(pid,None)
 if pid in moving:moving.remove(pid)
 if pid in latches:latches.remove(pid)
def revise(pid,shape,definition={}):
 old=next(p for p in parts if p['id']==pid);md=old['metadata'];density=md['solid_mass_kg']/(S[pid].Volume()/1e9);wasmoving=pid in moving
 forget(pid);return mesh(pid,old['name'],old['group'],shape,{**md['definition'],**definition},md['material']['candidate'],density,wasmoving)
def writej(n,obj):
 (H/n).write_text(json.dumps(obj,separators=(',',':')) if n.startswith(('model','drawing-edges')) else json.dumps(obj,indent=2))
def compressed_json(n,obj):
 with gzip.open(H/n,'wt',encoding='utf8',compresslevel=9) as f:json.dump(obj,f,separators=(',',':'))
def screw_m4(pid,x,y,z,direction,length_mm=10):
 # y is under-head plane; direction points into the threaded receiving part.
 d=(0,direction,0);sh=cyl(2/MM,length_mm/MM,(x,y,z),d)
 head=cyl(3.8/MM,2.2/MM,(x,y,z),(0,-direction,0))
 # 2.5mm hex drive, 1.3mm modeled engagement, open at top of the head.
 rr=2.5/MM/math.sqrt(3);pts=[(x+rr*math.cos(math.pi/6+i*math.pi/3),z+rr*math.sin(math.pi/6+i*math.pi/3)) for i in range(6)]
 ytop=y-direction*2.2/MM
 hexcut=profile_xz(pts, min(ytop,ytop+direction*1.3/MM),1.3/MM)
 sh=sh.fuse(head).cut(hexcut)
 return mesh(pid,'M4 x 10 ISO 7380 button-head screw','hardware',sh,{'family':'G-M4-10','nominal_thread_mm':[4,.7],'length_under_head_mm':length_mm,'head_diameter_mm':7.6,'head_height_mm':2.2,'hex_drive_mm':2.5,'thread_model':'Major-diameter envelope; mating blind hole uses same envelope, not literal thread helix','source':'https://www.kotadiafasteners.com/technical-data/iso-7380-specifications-button-head-socket/','retention':'Compatible locking compound with witness mark; final installation specification/proof unresolved'},'Steel ISO 7380-1 candidate')

# Attach fixed cheek guards with four physically modeled standoffs and blind tapped screws.
# C3 face covers had no fixings; replace them and update receiving cheeks.
guard_fixings=[]
for i,y in enumerate(P['mechanism_centers_y'],1):
 cheeks=[(y-.6875,y-.3125),(y+.3125,y+.6875)]
 for j,(a,b) in enumerate(cheeks,1):
  pid=f'H{i}-GUARD{j}';forget(pid)
  outward=-1 if j==1 else 1;far_side=(i==1 and j==2) or (i==2 and j==1)
  gap=.0625 if far_side else .3;face=a if outward<0 else b
  g0=face-gap-.0625 if outward<0 else face+gap
  gb={'x':[62.25,65.875],'y':[g0,g0+.0625],'z':[46.125,51.125]}
  sh=box(gb);lx,lz=P['fixed_latch_xz']
  sh=sh.cut(cyl(1.3125/2,2,(64,g0-.5,48.5),(0,1,0)))
  if far_side:
   sh=sh.cut(box({'x':[63.25,63.625],'y':[g0-.1,g0+.2],'z':[50.7,51.125]}))
   sh=sh.cut(box({'x':[lx-1.05,lx+.2],'y':[g0-.1,g0+.2],'z':[48,51.125]})).cut(cyl(.75/2,2,(lx,g0-.5,lz),(0,1,0)))
  else:sh=sh.cut(cyl(1.0625/2,2,(lx,g0-.5,lz),(0,1,0)))
  corners=[(62.5,46.5),(65.5,46.5),(65.5,48.5),(65.5,50.5)] if far_side else [(62.5,46.5),(65.5,46.5),(62.5,50.5),(65.5,50.5)]
  cheek=S[f'H{i}-CHEEK{j}']
  for k,(x,z) in enumerate(corners,1):
   sh=sh.cut(cyl(4.5/MM/2,2,(x,g0-.5,z),(0,1,0)))
   shaft_top=g0 if outward<0 else g0+.0625
   # Stop the major-diameter blind hole 7.2mm into the receiving 9.525mm cheek.
   cheek=cheek.cut(cyl(2/MM,7.2/MM,(x,face,z),(0,-outward,0)))
   spstart=face-gap if outward<0 else face
   mesh(f'G{i}-{j}-SP{k}','Guard stand-off washer','guard',ring(.375,4.5/MM,gap,(x,spstart,z)),{'family':'G-STANDOFF-'+str(gap),'OD_in':.375,'ID_mm':4.5,'length_in':gap,'role':'Solid standoff; clamps cover without distorting it'},'Steel candidate')
   screw_m4(f'G{i}-{j}-SC{k}',x,shaft_top,z,-outward,10 if far_side else 16)
   guard_fixings.append({'guard':pid,'cheek':f'H{i}-CHEEK{j}','x':x,'z':z,'blind_depth_mm':7.2,'screw':'M4x10' if far_side else 'M4x16','standoff_in':gap})
  revise(f'H{i}-CHEEK{j}',cheek,{'guard_attachment':'Four blind M4x0.7 tapped holes; model uses thread major envelope','guard_hole_depth_mm':7.2})
  mesh(pid,'Fixed cheek cover with inspection opening','guard',sh,{'family':'G-FIXED-FAR' if far_side else 'G-FIXED-OUTER','bounds_in':gb,'thickness_in':.0625,'fasteners':[q for q in guard_fixings if q['guard']==pid],'inspection':'Far-side cotter/engagement witness opening; primary cheek remains behind opening','status':'Finger/probe and servicing tests remain required'},'Transparent polycarbonate candidate; impact/fire/weather qualification open' if not far_side else '5052-H32 aluminum candidate',1200 if not far_side else 2680)
P['guard_fasteners']=guard_fixings

# Detail modules supplied by collaborating mechanical/foundation checks are inserted here.
for optional_module in ('mechanism_geometry.py','foundation_geometry.py','rear_guard_geometry.py'):
 path=H/optional_module
 if path.exists():exec(compile(path.read_text(),str(path),'exec'),globals())

# Recompute family BOM after replacement to avoid stale inherited counts.
families={}
for p in parts:
 md=p['metadata'];f=md.get('family',p['id'])
 if f not in families:families[f]={'id':f,'name':p['name'],'group':p['group'],'quantity_per_prototype':0,'material':md['material'],'definition':md['definition'],'status':'PRELIMINARY — NOT PROCUREMENT RELEASED'}
 families[f]['quantity_per_prototype']+=1
model={'schemaVersion':3,'units':'inches','title':'C3.1 folding seat with physical retention and guards','coordinate_system':'Coach X longitudinal, Y transverse, Z above rail','groups':groups,'parts':parts,'notes':['C3.1 physical detailing candidate; not released.','Flexible surfaces are modeled shapes for clearance review, not validated material behavior.']}
writej('parameters.json',P);writej('parts.json',[{k:p[k] for k in ('id','name','group','bounds_in','metadata')} for p in parts]);writej('bom.json',list(families.values()))
print('C31_CANONICAL',len(parts),flush=True)
# Continue with verified state/export routines after candidate modules freeze.
exec(compile((H/'verify_export.py').read_text(),str(H/'verify_export.py'),'exec'),globals())

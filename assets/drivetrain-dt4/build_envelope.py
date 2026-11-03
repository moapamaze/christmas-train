"""DT4 R2 catalog-reference CAD. Nominal interfaces + clearly marked reservations.
Motor profile segments are illustrative; configured OEM CAD is still required.
"""
from pathlib import Path
import cadquery as cq
import math,json
P=Path(__file__).resolve().parent
assembly=cq.Assembly(name='DT4_R2_REFERENCE_ASSEMBLY');parts=[];shapes=[]
def add(name,shape,category,color,status,axle=0,explode=0,side=1):
 assembly.add(shape,name=name,color=cq.Color(*color));shapes.append(shape)
 v,t=shape.tessellate(3,.25)
 parts.append(dict(id=name,name=name.replace('_',' '),category=category,color=color,status=status,axle=axle,explode=explode,side=side,vertices=[[a.x,a.y,a.z]for a in v],triangles=t))
def box(x,y,z,a,b,c):return cq.Workplane().box(a,b,c).translate((x,y,z)).val()
def cyl(x,y,z,r,l):return cq.Solid.makeCylinder(r,l,cq.Vector(x,y,z),cq.Vector(0,1,0))
for y in [-730,730]:add('Frame_reference_'+str(y),box(0,y,1050,2000,100,200),'frame',[.55,.63,.67],'Inherited frame reference; mounting and reactions not accepted.')
for i,(x,side)in enumerate([(-700,1),(700,-1)],1):
 def oriented(a,b,r):return cyl(x,a if side==1 else -b,500,r,b-a)
 add('Axle_'+str(i),cyl(x,-840,500,60,1680),'wheel',[.46,.54,.59],'Unstepped axle envelope. Seats, ends and retention unfinished.',i)
 for j,y in enumerate([-507.2,507.2]):
  add(f'Wheel_{i}_{j}',cyl(x,y-50,500,500,100),'wheel',[.25,.40,.47],'Ø1000 wheel blank; railway profile and press fit unfinished.',i)
  add(f'Axlebox_reserve_{i}_{j}',box(x,(-730 if j==0 else 730),500,190,180,190),'reserve',[.85,.63,.25],'Axlebox space only; bearings, guides and motor carrier not selected.',i)
 common='MS05 catalog reference, not OEM manufacturing geometry. '
 add(f'Motor_body_{i}',oriented(1018.5,1138,116),'motor',[.13,.50,.48],common+'Ø232 reference body; segment length is illustrative within 206 mount-to-rear envelope.',i,320,side)
 add(f'Motor_rear_cover_{i}',oriented(1138,1208,85),'motor',[.19,.60,.56],common+'Illustrative rear shape; actual port bosses and sensor geometry require configured CAD.',i,440,side)
 flange=oriented(1002,1018.5,150)
 # Visual reference holes; paired pattern read from catalog, NOT a drilling template.
 for ang in [-30,-10,10,30,150,170,190,210]:
  a=math.radians(ang);flange=flange.cut(cyl(x+132.5*math.cos(a),1001 if side==1 else -1019.5,500+132.5*math.sin(a),8.75,18.5))
 add(f'Motor_mount_flange_{i}',flange,'motor',[.17,.42,.44],common+'Ø300 bound; eight Ø17.5 holes on Ø265 PCD. Pair angles are visual references pending OEM confirmation.',i,220,side)
 add(f'Motor_pilot_{i}',oriented(979,1002,100),'motor',[.40,.73,.70],common+'Ø200 pilot, 23 projection; mounting face Y±1002.',i,220,side)
 add(f'Motor_front_housing_{i}',oriented(940,979,58),'motor',[.24,.56,.53],common+'Illustrative front housing; axial profile unfinished.',i,220,side)
 add(f'Motor_output_shaft_{i}',oriented(900,979,27.5),'shaft',[.66,.74,.75],common+'Ø55 spline bound only, no teeth. Spline DIN5480 m3 z17; actual usable engagement must be verified.',i,160,side)
 add(f'Coupling_reserve_{i}',oriented(800,940,80),'reserve',[.93,.62,.17],'Ø160 ×140 reservation, NOT a selected coupling. Deliberate shaft-envelope overlap.',i,75,side)
 carrier=oriented(982,1002,175).cut(oriented(981,1003,100.5))
 add(f'Flange_carrier_space_{i}',carrier,'reserve',[.72,.42,.72],'Purple ring reserves flange-carrier space only. Ø350/Ø201 ×20 are study bounds, NOT a designed plate. Support back to axlebox, bolts and torque restraint are missing.',i,120,side)
assembly.save(str(P/'DT4-envelope.step'))
(P/'model.json').write_text(json.dumps(dict(revision='DT4-R2-reference',parts=parts),separators=(',',':')))
b=assembly.toCompound().BoundingBox()
(P/'cad-verification.json').write_text(json.dumps(dict(revision='DT4-R2',part_count=len(parts),all_shapes_valid=all(s.isValid()for s in shapes),assembly_extent_mm=[b.xlen,b.ylen,b.zlen],scope='Solid validity and nominal interface dimensions only. Carrier and coupling are reserved spaces; no strength or interference acceptance.',motor_max_Y_mm=1208,static_body_gap_mm=92),indent=2))
print('Exported',len(parts),'reference parts; shapes valid:',all(s.isValid()for s in shapes))

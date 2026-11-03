
# Hosting transport: retain hashes of decoded source bytes after gzip packaging.
import gzip as _transport_gzip
def _transport_bytes(path):
    return path.read_bytes() if path.exists() else _transport_gzip.decompress(path.with_name(path.name + '.gz').read_bytes())

import gzip
"""PF-3O2-C1 R0. Editable preliminary coach body geometry, in inches.
Run with CadQuery 2.7: python build_c1.py. STEP is millimetres; browser mesh inches.
One canonical solid per physical part supplies STEP, web mesh and drawing projections.
No construction or operating approval is implied. See design-record.json.
"""
from pathlib import Path
import json, math, collections, html, base64
import cadquery as cq
import numpy as np
from PIL import Image, ImageDraw

HERE=Path(__file__).resolve().parent
DIST=HERE.parents[1]
MM=25.4
P={'floor_z':32.,'body_x':[-3.,309.], 'clear_y':[-52.,52.],
   'post_x':[-1.5,25.,57.,89.,121.,153.,185.,217.,249.,281.,307.5],
   'seat_x':[41.,73.,105.,137.,169.,201.,233.,265.],
   'post_y':53.625,'post_bottom':34.25,'eave_z':110.,
   'roof_halfspan':54.625,'roof_crown':120.61417322834646,
   'roof_spring_z':112.,'raised_inside_z':132.,'raised_outside_z':134.,
   'window_clear_z':[64.,96.],'door_clear_width':32.,'door_clear_height':80.,
   'steel_density_kg_m3':7850., 'aluminum_density_kg_m3':2680.,
   'round_HSS_outer_radius_factor':2.,'nominal_HSS_wall_model':True}
parts=[]; solids={}; edges={}
groups=[('underframe','Retained J1a members',[0,0,-20]),('walls','Wall structure',[0,28,0]),
 ('roof','Roof structure',[0,0,45]),('skin','Enclosure panels',[0,-45,0]),
 ('glazing','Window panes',[0,55,0]),('doors','Door leaves — hardware incomplete',[-24,0,0]),
 ('joint','C1-J01 direct post/frame brackets',[0,15,0]),('floor','Floor layers',[0,0,-8]),
 ('seats','32 seat space references',[0,0,10]),('scale','Six adult scale references',[0,0,0])]
G={x[0]:{'id':x[0],'label':x[1],'explosion_vector_in':x[2]} for x in groups}
COL={'underframe':'#677a7c','walls':'#315e52','roof':'#8b6d44','skin':'#9a292b',
 'glazing':'#86b8c1','doors':'#b88543','joint':'#bfa55b','floor':'#746a55','seats':'#b99060','scale':'#475c81'}
def box(b):
 return cq.Solid.makeBox(*[(b[k][1]-b[k][0])*MM for k in 'xyz'],cq.Vector(*[b[k][0]*MM for k in 'xyz']))
def cyl(r,l,p,axis):
 return cq.Solid.makeCylinder(r*MM,l*MM,cq.Vector(*[v*MM for v in p]),cq.Vector(*axis))
def hollow(b,axis,t,rounded=False):
 s=box(b); sub={k:[b[k][0]+t,b[k][1]-t] for k in 'xyz'};sub[axis]=[b[axis][0]-1,b[axis][1]+1]
 if not rounded:return s.cut(box(sub))
 # Nominal corner representation, not an asserted delivered tube corner radius.
 outer=cq.Workplane(obj=s).edges('|'+axis.upper()).fillet(2*t*MM).val()
 inside=cq.Workplane(obj=box(sub)).edges('|'+axis.upper()).fillet(t*MM).val()
 return outer.cut(inside)
def add(pid,name,group,s,bom,material='ASTM A500 Grade C — preliminary selection',status='PRELIMINARY PART GEOMETRY; NOT RELEASED',density=7850,opacity=1):
 assert pid not in solids,pid
 assert s.isValid(),pid
 v,f=s.tessellate(.65,.12)
 vv=[[a.x/MM,a.y/MM,a.z/MM] for a in v]
 bb=s.BoundingBox();b={k:[getattr(bb,k+'min')/MM,getattr(bb,k+'max')/MM] for k in 'xyz'}
 meta={'kind':'custom_part','engineering_status':status,'release_status':'NOT FOR CONSTRUCTION',
  'material':{'candidate':material,'status':'Designer proposal; verify supplied certification and later engineering review'},
  'definition':bom,'solid_mass_kg':s.Volume()/1e9*density,
  'source_refs':[{'id':'C1','label':'Canonical editable solid builder','path':'assets/coach-body-c1/build_c1.py'}]}
 parts.append({'id':pid,'name':name,'group':group,'positions':[round(c,6) for p in vv for c in p],
  'indices':[i for face in f for i in face],'color':COL[group],'opacity':opacity,'bounds_in':b,
  'centre_in':[(a+z)/2 for a,z in b.values()],'dimensions_xyz_in':[z-a for a,z in b.values()],
  'metadata':meta,'display_only':group in ('scale','seats'),'change_status':'C1 R0 proposed physical geometry' if group not in ('scale','seats') else 'REFERENCE SPACE ONLY'})
 solids[pid]=s
 ed=[]
 for e in s.Edges():
  try:
   pts=[e.positionAt(t) for t in np.linspace(0,1,2 if e.geomType()=='LINE' else 25)]
   ed.append([[p.x/MM,p.y/MM,p.z/MM] for p in pts])
  except Exception:pass
 edges[pid]=ed
 return s
def tube(pid,group,b,axis,t,section,lb_ft=None):
 l=b[axis][1]-b[axis][0]
 s=add(pid,section,group,hollow(b,axis,t,True),{'section':section,'axis':axis,'nominal_length_in':l,
  'end_prep':'Square end planes shown; final fit and weld development required','nominal_wall_in':t,
  'corner_model':'Outer radius 2t / inner t for visualization, not delivered geometry'},density=7850)
 if lb_ft:parts[-1]['metadata']['catalog_mass_kg']=l/12*lb_ft*.45359237
 return s
def plate(pid,group,b,holes=(),material='ASTM A36 plate — preliminary selection'):
 s=box(b)
 for x,z,d in holes:s=s.cut(cyl(d/2,b['y'][1]-b['y'][0]+2,(x,b['y'][0]-1,z),(0,1,0)))
 add(pid,'Plate '+pid.split('-')[0],group,s,{'bounds_in':b,'Y_axis_through_holes_X_Z_diameter_in':list(holes)},material)
 return s
def roofstrip(x0,x1,y0,y1,ro,ri,zc):
 # Circular roof patch extruded along coach X; analytic circular edges retained in STEP.
 def z(y,r):return zc+math.sqrt(r*r-y*y)
 a=cq.Vector(x0*MM,y0*MM,z(y0,ro)*MM);b=cq.Vector(x0*MM,y1*MM,z(y1,ro)*MM)
 c=cq.Vector(x0*MM,y1*MM,z(y1,ri)*MM);d=cq.Vector(x0*MM,y0*MM,z(y0,ri)*MM)
 w=cq.Wire.assembleEdges([cq.Edge.makeThreePointArc(a,cq.Vector(x0*MM,((y0+y1)/2)*MM,z((y0+y1)/2,ro)*MM),b),cq.Edge.makeLine(b,c),cq.Edge.makeThreePointArc(c,cq.Vector(x0*MM,((y0+y1)/2)*MM,z((y0+y1)/2,ri)*MM),d),cq.Edge.makeLine(d,a)])
 return cq.Solid.extrudeLinear(w,[],cq.Vector((x1-x0)*MM,0,0))
h=P['roof_crown']-112.;a=P['roof_halfspan'];R=(a*a+h*h)/(2*h);ZC=P['roof_crown']-R
P['roof_outer_radius_in']=R;P['roof_center_z_in']=ZC

# Retain every J1a nominal member. Drill only the two perimeter rails for C1-J01.
frame=json.loads(_transport_bytes(DIST/'assets/models3d/frame-J1a.json').decode())
for p in frame['parts']:
 b=p['bounds_in'];axis=p.get('axis',p['metadata']['section']['orientation']['longitudinal_axis']);t=p['metadata']['section']['nominal_wall_in']
 s=hollow(b,axis,t)
 if b['y'] in ([53,55],[-55,-53]):
  for x in P['post_x'][1:-1]:
   for dx in (-1.25,1.25):
    for z in (28.,30.):s=s.cut(cyl(.375,4,(x+dx,b['y'][0]-1,z),(0,1,0)))
 add('J1a-'+p['id'],p['name'],'underframe',s,{'predecessor_id':p['id'],'section':p['metadata']['section'],
  'revision':'C1 sleeve bores added only to perimeter rails; other nominal shells retained'},status='Retained unapproved underframe study; joints and global frame acceptance incomplete')
 parts[-1]['metadata']['catalog_mass_kg']=p['metadata'].get('catalog_mass_kg')

for side,sgn in [('R',1),('L',-1)]:
 yc=sgn*P['post_y'];yl=[yc-1.5,yc+1.5]
 for tag,z0,z1 in [('sill',32,34),('eave',110,112)]:
  tube('W-'+side+'-'+tag,'walls',{'x':[-3,309],'y':yl,'z':[z0,z1]},'x',.1875,'HSS 3 x 2 x 3/16',5.59)
 for n,x in enumerate(P['post_x']):
  b={'x':[x-1,x+1],'y':yl,'z':[34.25,110]};s=hollow(b,'z',.1875,True)
  if n not in (0,10):
   for z in (36,40):s=s.cut(cyl(.375,5,(x,yl[0]-1,z),(0,1,0)))
  add(f'W-{side}-P{n+1:02}', 'Side post HSS 3 x 2 x 3/16','walls',s,
   {'nominal_length_in':75.75,'section':'3 in Y x 2 in X x 3/16 nominal wall','sleeve_OD_bores_in':.75 if n not in (0,10) else None,'bore_z_in':[36,40] if n not in (0,10) else [],'end_receiver':'Unfinished; no abandoned standard-J01 bores' if n in (0,10) else 'Interior J01 candidate'},density=7850)
  parts[-1]['metadata']['catalog_mass_kg']=75.75/12*5.59*.45359237
  capwidth=3 if n in (0,10) else 4
  capb={'x':[x-capwidth/2,x+capwidth/2],'y':yl,'z':[34,34.25]}
  add(f'JC-{side}-{n+1:02}','Post cap / gravity saddle plate','joint',box(capb),{'blank_in':[capwidth,3,.25],
   'connection':'Post sits on cap. Sill crown contact and end welds need actual supplied corner geometry. Not a sharp all-around sill weld.'},'ASTM A36 plate — preliminary selection')
  # End receivers need a distinct connection: standard J01 would intersect T-3 / T309.
  if n in (0,10):continue
  # Direct post-to-underframe channel strap. Two rows in each member; not one fictitious global bolt group.
  holes=[(x,36,.5625),(x,40,.5625)]+[(x+dx,z,.5625) for dx in (-1.25,1.25) for z in (28,30)]
  yweb=[51.625,52.] if sgn==1 else [-52.,-51.625]
  plate(f'JW-{side}-{n+1:02}','joint',{'x':[x-2.5,x+2.5],'y':yweb,'z':[26.5,41.5]},holes)
  for j,xx in enumerate((x-2.125,x+2.125)):
   yy=[49.625,51.625] if sgn==1 else [-51.625,-49.625]
   plate(f'JR-{side}-{n+1:02}-{j}','joint',{'x':[xx-.09375,xx+.09375],'y':yy,'z':[26.5,41.5]})
  for tag,zz,xxw,yy,hh in [('U',[34.5,41.5],2.5,[55.125,55.5],holes[:2]),('D',[27,31],5,[55,55.375],holes[2:])]:
   yy=yy if sgn==1 else [-yy[1],-yy[0]]
   plate(f'JB-{side}-{n+1:02}-{tag}','joint',{'x':[x-xxw/2,x+xxw/2],'y':yy,'z':zz},hh)
  for tag,zz,xxw,yy,hh in [('U',[34.5,41.5],2.5,[52,52.125],holes[:2]),('D',[27,31],5,[52,53],holes[2:])]:
   yy=yy if sgn==1 else [-yy[1],-yy[0]]
   plate(f'JS-{side}-{n+1:02}-{tag}','joint',{'x':[x-xxw/2,x+xxw/2],'y':yy,'z':zz},hh)
  for k,(hx,hz,_) in enumerate(holes):
   y0=52.125 if k<2 else 53.;ln=3. if k<2 else 2.;y0=y0 if sgn==1 else -y0-ln
   s=cyl(.375,ln,(hx,y0,hz),(0,1,0)).cut(cyl(.265625,ln+2,(hx,y0-1,hz),(0,1,0)))
   add(f'JU-{side}-{n+1:02}-{k}','Through-wall crush sleeve','joint',s,{'OD_in':.75,'ID_in':.53125,'nominal_length_in':ln,
     'fit':'Match measured member outside width, ends flush; no press fit prescribed','bolt':'1/2-13 SAE J429 Grade 8 candidate; actual bolt/nut/washer/length/tightening not selected'},'Machined weldable steel; certified grade and retention weld to be selected')
 # Window rails are interrupted by posts; do not overlap a longitudinal tube through a post.
 for i,(x0,x1) in enumerate(zip(P['post_x'][:-1],P['post_x'][1:])):
  for tag,z in [('lower',63),('upper',97)]:
   tube(f'WV-{side}-{i+1:02}-{tag}','walls',{'x':[x0+1,x1-1],'y':yl,'z':[z-1,z+1]},'x',.125,'HSS 3 x 2 x 1/8',3.90)
 # Skin bands/pier panels: actual thickness and openings, attachment not yet developed.
 y0=55.125 if sgn==1 else -55.1875
 for tag,z0,z1 in [('lower',34,62),('upper',98,112)]:
  for i,(x0,x1) in enumerate(zip([-3,57,121,185,249],[57,121,185,249,309])):
   add(f'SK-{side}-{tag}-{i+1}','Aluminum outer skin panel','skin',box({'x':[x0+.03125,x1-.03125],'y':[y0,y0+.0625],'z':[z0,z1]}),{'nominal_thickness_in':.0625,'joint_gap_in':.0625,'attachment':'Fastener/bond and thermal movement detail not yet defined'},'5052-H32 aluminum — proposed sheet',density=2680)
 for i,x in enumerate(P['seat_x']):
  # Clear opening between post faces is 30 x 32. Pane overlaps 3/4 per edge; no fabricated window cartridge is implied.
  yy=[55.25,55.25+6/MM] if sgn==1 else [-55.25-6/MM,-55.25]
  add(f'GL-{side}-{i+1:02}','Side glazing blank — retention incomplete','glazing',box({'x':[x-15.75,x+15.75],'y':yy,'z':[63.25,96.75]}),{'blank_in':[31.5,33.5,6/MM],'clear_opening_in':[30,32],'edge_overlap_in':.75,'mounting_plane':'Outboard pane inner face |Y|55.25, 1/16 nominal gap from outer skin. No pane buried in structural HSS. Gasket/retainer not selected.','open_items':'Glazing safety/fire suitability, retainer, gasket, thermal allowance, replacement and emergency exit hardware'},'6 mm polycarbonate — material alternative, unselected',density=1200,opacity=.42)
 # Vertical outer skin on occupied-window piers and blank end bays.
 for i,(x0,x1) in enumerate([(-3,26),(56,58),(88,90),(120,122),(152,154),(184,186),(216,218),(248,250),(280,309)]):
  add(f'SK-{side}-pier-{i+1}','Window pier skin','skin',box({'x':[x0,x1],'y':[y0,y0+.0625],'z':[62,98]}),{'sheet_thickness_in':.0625,'attachment':'Not yet developed'},'5052-H32 aluminum — proposed sheet',density=2680)

# Roof hoops and skins. Central hoop cutouts at both raised end roofs are real omissions, not intersecting boxes.
for n,x in enumerate(P['post_x']):
 raised=x<=25 or x>=281
 ranges=[(-a,-27),(27,a)] if raised else [(-a,a)]
 for j,(y0,y1) in enumerate(ranges):
  outside=roofstrip(x-1,x+1,y0,y1,R,R-2,ZC)
  # Hollow the ring tube across X and radial depth, leaving actual nominal walls.
  void=roofstrip(x-.875,x+.875,y0-.01,y1+.01,R-.125,R-1.875,ZC)
  hoop=outside.cut(void)
  for yy in (-53.625,53.625):
   receiver=box({'x':[x-2,x+2],'y':[yy-1.5,yy+1.5],'z':[110,112]})
   receiver=cq.Workplane(obj=receiver).edges('|X').fillet(.375*MM).val()
   hoop=hoop.cut(receiver)
  add(f'RF-{n+1:02}-{j}','Curved roof hoop segment','roof',hoop,{'outer_radius_in':R,'radial_depth_in':2,'X_width_in':2,'nominal_wall_in':.125,'y_end_limits_in':[y0,y1],'process':'Roll formed/bent tube, nominal cope to eave outer envelope. Actual receiving corners, thinning, springback, weld and structural properties to be validated'})
for n,(x0,x1) in enumerate([(-3,25),(25,89),(89,153),(153,217),(217,281),(281,309)]):
 for j,(y0,y1) in enumerate([(-a,-27),(27,a)] if n in (0,5) else [(-a,a)]):
  add(f'RS-{n+1}-{j}','Curved roof sheet','skin',roofstrip(x0+.03125,x1-.03125,y0,y1,R+.0625,R,ZC),{'sheet_thickness_in':.0625,'outer_radius_in':R+.0625,'joint_and_attachment':'Seam fasteners/sealant/movement/flashing and purlin support development incomplete'},'5052-H32 aluminum — proposed sheet',density=2680)
for e,(x0,x1) in enumerate([(-3,25),(281,309)]):
 for yy in (-26,26):
  tube(f'RH-{e}-long-{yy}','roof',{'x':[x0,x1],'y':[yy-1,yy+1],'z':[132,134]},'x',.125,'HSS 2 x 2 x 1/8')
 for xx in (x0+1,x1-1):
  tube(f'RH-{e}-cross-{xx}','roof',{'x':[xx-1,xx+1],'y':[-25,25],'z':[132,134]},'y',.125,'HSS 2 x 2 x 1/8')
  for yy in (-26,26):
   tube(f'RH-{e}-post-{xx}-{yy}','roof',{'x':[xx-1,xx+1],'y':[yy-1,yy+1],'z':[112,132]},'z',.125,'HSS 2 x 2 x 1/8')
 add(f'RH-{e}-top','Raised roof top sheet','skin',box({'x':[x0,x1],'y':[-27,27],'z':[134,134.0625]}),{'nominal_blank_in':[x1-x0,54,.0625],'seams':'Return flashing, sidewall curved trim and HVAC condensation details incomplete'},'5052-H32 aluminum — proposed sheet',density=2680)
 for sg in (-1,1):
  yy=[27,27.0625] if sg==1 else [-27.0625,-27]
  zb=ZC+math.sqrt((R+.0625)**2-27**2)
  add(f'RH-{e}-side-{sg}','Raised roof side closure sheet','skin',box({'x':[x0,x1],'y':yy,'z':[zb,134]}),{'sheet_thickness_in':.0625,'bottom_z_in':zb,'seam':'Seal/flashing/fastener details incomplete'},'5052-H32 aluminum — proposed sheet',density=2680)
 # Curved-bottom raised-roof return closure, on the inner end of each raised hood.
 xr=x1 if e==0 else x0-.0625
 def cv(y,z):return cq.Vector(xr*MM,y*MM,z*MM)
 zb=lambda y:ZC+math.sqrt((R+.0625)**2-y*y)
 wire=cq.Wire.assembleEdges([cq.Edge.makeLine(cv(-27,134),cv(27,134)),cq.Edge.makeLine(cv(27,134),cv(27,zb(27))),cq.Edge.makeThreePointArc(cv(27,zb(27)),cv(0,zb(0)),cv(-27,zb(-27))),cq.Edge.makeLine(cv(-27,zb(-27)),cv(-27,134))])
 add(f'RH-{e}-return','Raised roof curved-bottom return sheet','skin',cq.Solid.extrudeLinear(wire,[],cq.Vector(.0625*MM,0,0)),{'thickness_in':.0625,'width_in':54,'top_z_in':134,'bottom_radius_in':R+.0625,'attachment':'Incomplete'},'5052-H32 aluminum — proposed sheet',density=2680)
 # End gable with analytic roof shoulders and raised central crown, no open roof end.
 xf=-3.0625 if e==0 else 309
 def gv(y,z):return cq.Vector(xf*MM,y*MM,z*MM)
 ze=lambda y:ZC+math.sqrt(R**2-y*y)
 wire=cq.Wire.assembleEdges([cq.Edge.makeLine(gv(-a,112),gv(a,112)),
  cq.Edge.makeThreePointArc(gv(a,112),gv((a+27)/2,ze((a+27)/2)),gv(27,ze(27))),
  cq.Edge.makeLine(gv(27,ze(27)),gv(27,134)),cq.Edge.makeLine(gv(27,134),gv(-27,134)),
  cq.Edge.makeLine(gv(-27,134),gv(-27,ze(-27))),
  cq.Edge.makeThreePointArc(gv(-27,ze(-27)),gv(-(a+27)/2,ze(-(a+27)/2)),gv(-a,112))])
 add(f'EG-{e}','Shaped end gable sheet','skin',cq.Solid.extrudeLinear(wire,[],cq.Vector(.0625*MM,0,0)),{'thickness_in':.0625,'shoulder_radius_in':R,'hood_width_in':54,'top_z_in':134,'attachment':'Incomplete'},'5052-H32 aluminum — proposed sheet',density=2680)
 # Actual end door jambs and header; end cladding kept off clear doorway.
 xx=-1.5 if e==0 else 307.5
 for yy in (-17,17):
  tube(f'ED-{e}-jamb-{yy}','walls',{'x':[xx-1,xx+1],'y':[yy-1,yy+1],'z':[32,112]},'z',.125,'HSS 2 x 2 x 1/8')
 tube(f'ED-{e}-header','walls',{'x':[xx-1,xx+1],'y':[-18,18],'z':[112,114]},'y',.125,'HSS 2 x 2 x 1/8')
 for sg in (-1,1):
  yy=[18,52.125] if sg==1 else [-52.125,-18]
  for zz in (32,110):tube(f'ED-{e}-rail-{sg}-{zz}','walls',{'x':[xx-1,xx+1],'y':yy,'z':[zz,zz+2]},'y',.125,'HSS 2 x 2 x 1/8')
  ex=[-3.0625,-3] if e==0 else [309,309.0625]
  add(f'ES-{e}-{sg}','End wall sheet','skin',box({'x':ex,'y':yy,'z':[34,112]}),{'nominal_thickness_in':.0625,'attachment':'Not yet developed'},'5052-H32 aluminum — proposed sheet',density=2680)
 # Door leaf is constructed as rails/panel; no generic latch/hinge is misrepresented as selected hardware.
 for yy in (-15.375,15.375):tube(f'DR-{e}-stile-{yy}','doors',{'x':[xx-.75,xx+.75],'y':[yy-.5,yy+.5],'z':[32.25,111.75]},'z',.083,'HSS 1.5 x 1 x .083')
 for z in (32.75,111.25):tube(f'DR-{e}-rail-{z}','doors',{'x':[xx-.75,xx+.75],'y':[-14.875,14.875],'z':[z-.5,z+.5]},'y',.083,'HSS 1.5 x 1 x .083')
 add(f'DR-{e}-panel','Door infill blank','doors',box({'x':[xx-.8125,xx-.75],'y':[-15.875,15.875],'z':[32.25,111.75]}),{'door_leaf_width_in':31.75,'door_leaf_height_in':79.5,'unresolved':'Hinges, latch, closer, emergency opening, glazing and swept path not selected'},'5052-H32 aluminum — proposed sheet',density=2680)

# Retain floor datum; do not pretend the audited seat hardpoint conflict has been solved.
for i,(x0,x1) in enumerate(zip([-3,45,93,141,189,237,285],[45,93,141,189,237,285,309])):
 for j,(y0,y1) in enumerate([(-55,-34),(-34,34),(34,55)]):
  fs=box({'x':[x0+.0625,x1-.0625],'y':[y0+.0625,y1-.0625],'z':[31.1220472441,31.8720472441]})
  if j in (0,2):
   for xp in P['post_x']:
    notch_y=[49.5,56.] if j==2 else [-56.,-49.5]
    if xp in P['post_x'][1:-1]:fs=fs.cut(box({'x':[xp-2.625,xp+2.625],'y':notch_y,'z':[30,33]}))
  add(f'FL-{i+1}-{j+1}','Floor panel envelope with J01 cutouts','floor',fs,{'panel_thickness_in':.75,'J01_notches':'5.25 in X width at interior posts; outboard from |Y|49.5. Final sealed closeout/cover and edge reinforcement incomplete.','status':'Retained H1 floor-panel thickness and support study; edge closeouts and attachment incomplete'},'Honeycomb panel construction not qualified',density=100)
for i,x in enumerate(P['seat_x']):
 for side,yy in [('L',[-52,-12]),('R',[12,52])]:
  add(f'SEAT-{side}-{i+1}','Two-adult bench space reference','seats',box({'x':[x-10,x+10],'y':yy,'z':[48,50]}),{'places':2,'seat_top_above_floor_in':18,'reference_only':'Not a fabricated bench or resolved seat/floor attachment'},'SPACE REFERENCE ONLY',density=0,opacity=.32)
# Exactly six adult proxies from retained source, each selected as a labelled reference only.
old=json.loads(_transport_bytes(DIST/'assets/models/regular-coach.json').decode())
adult=[p for p in old['parts'] if p.get('group')=='scaleProxies']
if not adult:adult=[p for p in old['parts'] if any(w in p.get('name','').lower() for w in ('adult','person'))]
for n,p in enumerate(adult):
 v=np.array(p['positions']).reshape(-1,3);v[:,2]+=4
 b={k:[float(v[:,i].min()),float(v[:,i].max())] for i,k in enumerate('xyz')}
 q={'id':'HUMAN-'+str(n+1),'name':p.get('name','Adult scale proxy'),'group':'scale','positions':v.flatten().tolist(),'indices':p['indices'],'color':COL['scale'],'opacity':.45,'bounds_in':b,'centre_in':[(a+z)/2 for a,z in b.values()],'dimensions_xyz_in':[z-a for a,z in b.values()],'display_only':True,'change_status':'Inherited illustrative scale only','metadata':{'kind':'reference','engineering_status':'Illustrative adult proxy, not anthropometric validation','release_status':'REFERENCE ONLY','definition':{'source':'retained regular-coach.json; z translated +4 in'}}}
 parts.append(q)

# Cut small service openings into outer lower skins around external upper backplates.
# Re-tessellate only revised parts, preserving one solid definition for every output.
for p in list(parts):
 if p['id'].startswith('SK-') and '-lower-' in p['id']:
  sh=solids[p['id']]
  for xp in P['post_x'][1:-1]:
   sh=sh.cut(box({'x':[xp-1.375,xp+1.375],'y':[-56,56],'z':[34.375,41.625]}))
  oldp=p;parts.remove(p);solids.pop(p['id']);edges.pop(p['id'])
  add(p['id'],p['name'],p['group'],sh,{**p['metadata']['definition'],'J01_notches':'2.75 x 7.25 in skin service opening at each post; sealed removable cover not yet developed'},p['metadata']['material']['candidate'],density=2680)
for g in ('skin','glazing','doors','scale','seats'):G[g]['default_visible']=False
model={'schemaVersion':3,'units':'inches','coordinate_system':'X forward wall 0 to rear 306; Y transverse, positive vehicle right; Z above rail. Finished floor study Z32 in.','title':'C1 regular coach body / retained J1a underframe','groups':list(G.values()),'parts':parts,
 'notes':['New physical body, roof and C1-J01 bracket proposal, with honest omissions.','Underframe nominal shells retained; perimeter sleeve bores revised.','No bogie, brake, coupling, stair, bench mechanism, HVAC installation, insulation, liner or finished joinery is claimed complete.','Sharp J1a corners and nominal rounded body HSS are representations, not delivered stock geometry.','Seat and human groups are explicit space references, excluded from STEP and mass.'],
 'sources':[{'id':'Atlas','label':'Atlas nominal rectangular HSS catalog','url':'https://www.atlastube.com/wp-content/uploads/2018/04/A500-Rectangle-Current.pdf'}]}
(HERE/'model.json.gz').write_bytes(gzip.compress(json.dumps(model,separators=(',',':')).encode(),compresslevel=9,mtime=0))
(HERE/'drawing-edges.json.gz').write_bytes(gzip.compress(json.dumps(edges,separators=(',',':')).encode(),compresslevel=9,mtime=0))
(HERE/'parameters.json').write_text(json.dumps(P,indent=2))
(HERE/'parts.json').write_text(json.dumps([{k:p[k] for k in ('id','name','group','bounds_in','metadata')} for p in parts],indent=2))
cq.exporters.export(cq.Compound.makeCompound([s for k,s in solids.items() if not k.startswith('SEAT-')]),str(HERE/'C1-regular-coach-body-R0.step'))
import gzip
_step=HERE/'C1-regular-coach-body-R0.step'
(HERE/'C1-regular-coach-body-R0.step.gz').write_bytes(gzip.compress(_step.read_bytes(),compresslevel=9,mtime=0))
_step.unlink()
cq.exporters.export(cq.Compound.makeCompound([s for k,s in solids.items() if k.startswith(('JW-R-04','JR-R-04','JB-R-04','JS-R-04','JU-R-04','JC-R-04','W-R-P04'))]),str(HERE/'C1-J01-post-connection-R0.step'))

# CPU raster from exported tessellation; same geometry as rotatable model, not a generated rendering.
def render(path,select,width=1800,height=850,mode='iso'):
 chosen=[p for p in parts if select(p)];verts=[];polys=[]
 u=np.array([.80,-.60,0.]) if mode=='iso' else np.array([1.,0,0]);v=np.array([.24,.32,.916515]) if mode=='iso' else np.array([0.,0,1.]);view=np.cross(u,v)
 for p in chosen:
  vv=np.array(p['positions']).reshape(-1,3);pp=np.column_stack([vv@u,-vv@v]);verts.extend(pp)
  f=np.array(p['indices']).reshape(-1,3)
  for face in f:
   tri=vv[face];normal=np.cross(tri[1]-tri[0],tri[2]-tri[0]);nn=np.linalg.norm(normal)
   if nn<1e-10:continue
   shade=.60+.35*abs(float(normal/nn@np.array([.2,-.4,.8944])))
   color=tuple(min(255,int(int(p['color'][j:j+2],16)*shade+25)) for j in (1,3,5))
   polys.append((float(tri.mean(0)@view),pp[face],color))
 vv=np.array(verts);lo=vv.min(0);hi=vv.max(0);sc=min((width-100)/(hi[0]-lo[0]),(height-100)/(hi[1]-lo[1]));origin=np.array([width/2,height/2])-(hi+lo)/2*sc
 im=Image.new('RGB',(width,height),'#f2f1eb');d=ImageDraw.Draw(im)
 for z,poly,col in sorted(polys,key=lambda q:q[0]):d.polygon([tuple(a*sc+origin) for a in poly],fill=col)
 im.save(path)
render(HERE/'C1-body-cutaway.png',lambda p:p['group'] not in ('skin','glazing','doors','scale','seats'))
render(HERE/'C1-body-enclosed.png',lambda p:p['group'] not in ('scale','seats','joint'))

def txt(x,y,s,size=16,weight='normal',color='#203a36'):
 return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}">{html.escape(str(s))}</text>'
def line(x1,y1,x2,y2,color='#2e504a',w=1):return f'<path d="M{x1},{y1}L{x2},{y2}" fill="none" stroke="{color}" stroke-width="{w}"/>'
def dim(x1,y1,x2,y2,label):
 return line(x1,y1,x2,y2,'#a34e24')+line(x1-4,y1-4,x1+4,y1+4,'#a34e24')+line(x2-4,y2-4,x2+4,y2+4,'#a34e24')+txt((x1+x2)/2+7,(y1+y2)/2-7,label,14,color='#a34e24')
def projection(ids,axes,rect):
 # True CAD edge projections; holes and hollow sections preserved. Wire projections show back edges too.
 ee=[e for pid in ids for e in edges.get(pid,[])];vv=np.array([p for e in ee for p in e]);a,b=axes
 lo=np.array([vv[:,a].min(),vv[:,b].min()]);hi=np.array([vv[:,a].max(),vv[:,b].max()]);x,y,w,h=rect
 sc=min(w/(hi[0]-lo[0]),h/(hi[1]-lo[1]));origin=np.array([x,y+h])+np.array([-lo[0]*sc,lo[1]*sc])
 out=''
 for e in ee:
  pts=[(p[a]*sc+origin[0],-p[b]*sc+origin[1]) for p in e]
  out+='<polyline points="'+' '.join(f'{xx:.2f},{yy:.2f}' for xx,yy in pts)+'" fill="none" stroke="#294d48" stroke-width=".65"/>'
 return out,lambda p:(p[0]*sc+origin[0],-p[1]*sc+origin[1]),sc
def sheet(name,title,body,notes):
 s='<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1200" viewBox="0 0 1800 1200"><rect width="1800" height="1200" fill="white"/><g font-family="Arial,sans-serif">'
 s+=txt(45,48,'PULSIPHER FARMS · CUSTOM PASSENGER TRAIN',17,'bold')+txt(45,83,title,29,'bold')
 s+=txt(45,111,'C1 R0 · 19 OCT 2026 · INCHES UNLESS MARKED · PRELIMINARY DESIGN — NOT FOR CONSTRUCTION',15,color='#963d24')+body
 for i,n in enumerate(notes):s+=txt(45,1040+i*24,n,15)
 s+=line(40,1150,1760,1150)+txt(45,1177,name+' · Canonical source: build_c1.py / parameters.json / parts.json · Dimensions govern; do not scale.',15)
 s+='</g></svg>';(HERE/(name+'.svg')).write_text(s)
ids=[p['id'] for p in parts if p['group'] not in ('floor','scale','seats','joint','glazing')]
out,xy,sc=projection(ids,(0,2),(65,170,1400,490))
out+=txt(70,155,'SIDE ELEVATION · CAD edges, including rear edges',18,'bold')
out+=dim(*xy((-3,145)),*xy((309,145)),'312 BODY SILL / END DATUM LENGTH')
out+=dim(*xy((-47,19)),*xy((353,19)),'400 UNDERFRAME / END-PLATFORM ENVELOPE')
for x in P['seat_x']:out+=txt(*xy((x-10,70)),str(int(x)),12)
out+=txt(70,730,'Window centres X: 41, 73, 105, 137, 169, 201, 233, 265 · 32 pitch · 8 windows / side',17)
out+=txt(70,760,'Clear opening 30 W x 32 H · Z64–96 · glazing blank 31.5 x 33.5 x 6 mm; retainers still to develop',17)
endids=[p['id'] for p in parts if p['group'] in ('walls','roof','doors') and p['bounds_in']['x'][0]<0]
ee,ex,ss=projection(endids,(1,2),(1500,180,220,570));out+=ee+txt(1465,155,'END / RAISED ROOF',17,'bold')
out+=dim(*ex((-52,135)),*ex((52,135)),'104 CLEAR CABIN')
out+=txt(1460,810,'Door: 32 clear W',16)+txt(1460,836,'80 clear H proposed',16)+txt(1460,862,'Finished floor Z32',16)+txt(1460,888,'Raised inner roof Z132',16)
out+=txt(70,825,'BODY POST STATIONS X',18,'bold')
out+=txt(70,855,', '.join(str(x) for x in P['post_x']),17)
out+=txt(70,905,'Normal boarding stays on one physical coach side. The left/right side and all emergency-exit hardware remain to be assigned.',17)
sheet('C1-A01','Regular coach · body and underframe general arrangement',out,[
 '32 places retained: sixteen two-person bench spaces at inherited centres. Seat frames/mounts are not yet this issue’s fabricated parts.',
 'Side skin width 110.375; glazing width 110.972; local brackets 111.000. End skin planes X−3.0625 / 309.0625.',
 'Floor Z32 remains a packaging datum with no accepted empty/loaded suspension state. Actual trucks, couplers and stairs omitted.',
 'Raised-roof dimensions are designer packaging selections. Mini-split OEM clearances, mounts, condensate and ventilation remain unresolved.'])
out='<image href="data:image/png;base64,'+base64.b64encode((HERE/'C1-body-cutaway.png').read_bytes()).decode()+'" x="55" y="140" width="1690" height="780"/>'
out+=txt(70,960,'Hollow members, cut roof segments, cap plates, sleeve bores and bracket plates are actual exported solids.',18,'bold')
sheet('C1-A02','Regular coach · physical framing assembly / cutaway',out,[
 'Same solid source as STEP, browser model and part sheets. This cutaway hides glazing and skins to expose the frame.',
 'Green: body framing. Bronze: roof. Gold: J01 bracket candidates. Grey: retained J1a nominal underframe.',
 'HSS model radii are nominal visualization selections; do not machine or qualify supplied tube from these radii.',
 'J01 does not complete all body load cases. Side skins, liners, insulation, window/door hardware and frame joints remain unfinished.'])
prototype=[p['id'] for p in parts if p['id'].startswith(('JW-R-04','JR-R-04','JB-R-04','JS-R-04','JU-R-04','JC-R-04'))]
# Crop only the drawing's post and perimeter context. The source parts and STEP remain uncut.
context_ids=['W-R-P04']+[p['id'] for p in parts if p['group']=='underframe' and all(abs(v-t)<1e-3 for v,t in zip(p['bounds_in']['y'],[53.,55.]))]
for pid in context_ids:
 vid='VIEW-'+pid
 if vid not in edges:
  clip=box({'x':[85,93],'y':[49,56],'z':[25.5,43]});section=solids[pid].intersect(clip)
  edges[vid]=[[[p.x/MM,p.y/MM,p.z/MM] for p in [e.positionAt(t) for t in np.linspace(0,1,2 if e.geomType()=='LINE' else 25)]] for e in section.Edges()]
 prototype.append(vid)
(HERE/'drawing-edges.json.gz').write_bytes(gzip.compress(json.dumps(edges,separators=(',',':')).encode(),compresslevel=9,mtime=0))
out,xy,s=projection(prototype,(0,2),(70,230,600,650));out+=txt(70,155,'J01 FRONT (X–Z) · RIGHT POST X89',18,'bold')
out+=dim(*xy((86.5,44)),*xy((91.5,44)),'5.000 WEB WIDTH')
out+=dim(*xy((94,26.5)),*xy((94,41.5)),'15.000 WEB / RIB HEIGHT')
for z in (28,30,36,40):out+=txt(*xy((94,z)),f'Z{z}',15)
ee,ex,_=projection(prototype,(1,2),(790,230,340,650));out+=ee+txt(790,155,'SIDE (Y–Z) · DIRECT LOAD PATH',18,'bold')
out+=txt(1220,190,'NUMBERED PART FAMILY / EACH POST',19,'bold')
rows=['1 JW: A36 web 5 x 15 x 3/8; 6 holes Ø9/16',
 '2 JR: 2 ribs A36 15 x 2 x 3/16',
 '3 JB-U: backing 2.5 x 7 x 3/8; 2 holes',
 '4 JB-D: backing 5 x 4 x 3/8; 4 holes',
 '5 JS-U: shim 2.5 x 7 x 1/8; 2 holes',
 '6 JS-D: spacer 5 x 4 x 1; 4 holes',
 '7 JU-U: 2 sleeves Ø.750 / Ø.53125 x 3',
 '8 JU-D: 4 sleeves Ø.750 / Ø.53125 x 2',
 '9 JC: cap plate 4 x 3 x 1/4',
 '10 Post: HSS 3(Y) x 2(X) x 3/16 x 75.75',
 '11 Six 1/2-13 Grade 8 bolt sets: candidates',
 'Bolt/nut/washer dimensions not falsely modeled.',
 '18 interior joints. Four end receivers unfinished.']
for i,r in enumerate(rows):out+=txt(1200,225+i*34,r,15)
out+=txt(1200,715,'Primary load path:',19,'bold')
for i,r in enumerate(['Post upper two-row clamp → ribbed web →','lower four-bolt attachment → perimeter rail.','Upper lever arm 4; lower row spacing 2.',
 'Do not use separation between members as','the bolt-group moment arm. Local contact,','prying, wall bearing and fatigue still need review.']):out+=txt(1200,752+i*28,r,16)
for number,target,labelpos in [(1,(51.8,38),(690,235)),(2,(50.6,32.5),(690,470)),(3,(55.3,39),(1130,280)),(4,(55.2,29.5),(1130,725)),(5,(52.06,36.8),(690,330)),(6,(52.5,28.8),(690,790)),(7,(53.5,40),(1130,210)),(8,(54,28),(1130,820)),(9,(53.5,34.12),(1130,535))]:
 tx,ty=ex(target);lx,ly=labelpos
 out+=line(tx,ty,lx,ly,'#a34e24')+f'<circle cx="{lx}" cy="{ly}" r="12" fill="white" stroke="#a34e24"/>'+txt(lx-5,ly+5,number,14,'bold')
sheet('C1-J01','Body post to underframe · assembled candidate connection',out,[
 'Post/frame context is cropped for this view; the visible crop boundaries are not physical part ends.',
 'Sleeve bores Ø.750 nominal in both HSS walls; sleeves ID .53125. Match sleeve length to measured tube outside width; ends flush.',
 'No interference fit, bolt torque, preload, proof rating, sleeve grade or weld procedure is asserted. Bolts omitted rather than invented.',
 'Web/rib continuous 3/16 E70 fillets are a proposed trial for later joint review; no released weld capacity or fatigue acceptance.',
 'Cap carries assembly/gravity contact. Actual sill crown and cap end-weld/load distribution must replace nominal corner assumptions.'])
# Actual individual web blank: 1:1 coordinate data recorded separately for cutting review.
holelocal=[(2.5,9.5,.5625),(2.5,13.5,.5625),(1.25,1.5,.5625),(1.25,3.5,.5625),(3.75,1.5,.5625),(3.75,3.5,.5625)]
out=txt(70,165,'JW WEB BLANK · FRONT / HOLE COORDINATES FROM LOWER-LEFT',19,'bold')
sx=47;xx=90;yy=920
out+=f'<rect x="{xx}" y="{yy-15*sx}" width="{5*sx}" height="{15*sx}" fill="#faf7ed" stroke="#244d44" stroke-width="2"/>'
for n,(x,z,d) in enumerate(holelocal):
 out+=f'<circle cx="{xx+x*sx}" cy="{yy-z*sx}" r="{d/2*sx}" fill="white" stroke="#244d44"/>'+txt(xx+x*sx+20,yy-z*sx+5,n+1,17)
out+=dim(xx,yy+35,xx+5*sx,yy+35,'5.000')+dim(xx+5*sx+42,yy,xx+5*sx+42,yy-15*sx,'15.000')
for tx,label in [(570,'HOLE'),(680,'X'),(810,'Z'),(950,'DIA')]:out+=txt(tx,190,label,18,'bold')
for n,(x,z,d) in enumerate(holelocal):
 for tx,value in [(570,str(n+1)),(680,f'{x:.3f}'),(810,f'{z:.3f}'),(950,f'{d:.4f}')]:out+=txt(tx,230+n*36,value,18)
out+=txt(570,500,'Material: ASTM A36 plate, nominal 3/8 thick',18,'bold')
out+=txt(570,535,'Quantity: 18 interior webs; mirrored installation does not change hole pattern.',17)
out+=txt(570,580,'Proposed shop targets (designer choices, not OEM tolerances):',18,'bold')
for i,r in enumerate(['Profile ±1/32; hole centres ±1/64 to common lower-left datum; deburr all edges.',
 'Bore sleeve holes together through both measured HSS walls in a rigid drill jig.',
 'Do not use profile tolerance as a bolt or sleeve fit. Sleeve bore/OD manufacturing fits need process trials.',
 'Trial assembly before coating. Record sleeve end flushness, web/shim bearing and hole alignment.',
 'Rib location: centres X±2.125 from post axis. Ribs project 2.000 inside from web inner face.',
 'Proposed 3/16 E70 web/rib fillets require procedure, effective length and distortion review.',
 'Do not weld this bracket to an occupied or finished coach; manufacturing sequence still to be released.']):out+=txt(570,620+i*40,r,16)
sheet('C1-P01','JW web and J01 manufacturing definition · preliminary',out,[
 'Canonical hole table: J01-web-cutting.json. STEP contains actual holes and hollow sleeves. Cutting geometry is a proposal for review.',
 'A builder can identify and quote these blanks; this does not release the assembled passenger vehicle or its connections.',
 'Verify actual bolt standards, plate/tube properties, local wall effects, clamp mechanism and reversing/fatigue cases before production.',
 'Precision sleeves and coordinated drilling are subcontract tasks unless the farm’s tooling and inspection capability are demonstrated.'])
(HERE/'J01-web-cutting.json').write_text(json.dumps({'units':'inches','part':'JW','blank':[5,15,.375],'quantity':18,'origin':'lower-left front face','through_holes':[{'id':i+1,'x':x,'z':z,'diameter':d} for i,(x,z,d) in enumerate(holelocal)],'release':'PRELIMINARY NOT RELEASED'},indent=2))
# Physical exports and arithmetic checks, independent of apparent rendering quality.
def positive_overlap(sa,sb):
 ba,bb=sa.BoundingBox(),sb.BoundingBox()
 if any(min(getattr(ba,a+'max'),getattr(bb,a+'max'))-max(getattr(ba,a+'min'),getattr(bb,a+'min'))<.005 for a in 'xyz'):return 0.
 return sa.intersect(sb).Volume()/MM**3
interface_checks=[]
for pid,sa in solids.items():
 if pid.startswith(('JW-','JR-','JS-','JB-')):
  for fid,sb in solids.items():
   if fid.startswith('J1a-'):
    vol=positive_overlap(sa,sb)
    if vol>1e-6:interface_checks.append({'part':pid,'host':fid,'overlap_in3':vol})
for pid,sa in solids.items():
 if pid.startswith('GL-'):
  for fid,sb in solids.items():
   if fid.startswith(('W-','WV-')):
    vol=positive_overlap(sa,sb)
    if vol>1e-6:interface_checks.append({'part':pid,'host':fid,'overlap_in3':vol})
(HERE/'interface-check.json').write_text(json.dumps({'scope':'Positive-volume J01 web/rib/shim/backing versus retained frame, and glazing versus structural wall tubes. Not a complete coach clash or tolerance check.','unintended_overlap_records':interface_checks,'pass':not interface_checks,'excluded':'Contact surfaces, roof joint stiffness/welds, door motion, actual bolt/socket tools, floor panel edge support, running gear and all undeveloped interfaces'},indent=2))
wind=1000.;L=75.75*.0254;trib=32*.0254;q=wind*trib;V=q*L;M=q*L*L/2
I=1.77*.0254**4;S=1.18*.0254**3
webA=5*.375;ribA=2*.1875*2;cent=(webA*.1875+ribA*1.375)/(webA+ribA)
Ic=5*.375**3/12+webA*(.1875-cent)**2+2*(.1875*2**3/12+.375*(1.375-cent)**2)
mass=collections.defaultdict(float)
for p in parts:
 if p['group'] not in ('scale','seats'):mass[p['group']]+=p['metadata'].get('catalog_mass_kg') or p['metadata'].get('solid_mass_kg',0)
calc={'date':'2026-10-19','analyst_case':'1 kPa transverse pressure on isolated fixed-base/free-tip post, 32 in tributary width. Not a site wind code selection.',
 'post':{'length_in':75.75,'q_N_m':q,'shear_N':V,'base_moment_N_m':M,'stress_MPa':M/S/1e6,'tip_deflection_mm':q*L**4/(8*200e9*I)*1000,'I_in4':1.77,'S_in3':1.18},
 'channel_gross_section':{'centroid_depth_in':cent,'I_in4':Ic,'S_min_in3':Ic/max(cent,2.375-cent),'reference_gross_stress_MPa':(M+V*(34.25-29)*.0254)/(Ic/max(cent,2.375-cent)*.0254**3)/1e6,'limits':'Gross elastic section only; holes, weld transfer, local web bending, prying/contact, buckling and fatigue not passed. A single assumed effective-width plate-strip calculation is not a stiffness/contact solution.'},
 'connection_demands':{'upper_group_center_z_in':38,'lower_group_center_z_in':29,
 'upper_moment_N_m':M-V*(38-34.25)*.0254,'lower_moment_N_m':M+V*(34.25-29)*.0254,
 'upper_signed_normal_reactions_N':[V/2+(M-V*(38-34.25)*.0254)/(4*.0254),V/2-(M-V*(38-34.25)*.0254)/(4*.0254)],
 'lower_signed_normal_reactions_N_each_bolt':[V/4+(M+V*(34.25-29)*.0254)/(4*.0254),V/4-(M+V*(34.25-29)*.0254)/(4*.0254)],
 'interpretation':'Distinct ideal rigid groups. Negative reaction requires compression/contact, not negative bolt tension. Actual prying/contact/stiffness, local web bending and perimeter-rail torsion are not passed.'},
 'mass_by_group_kg':dict(mass),'mass_limits':'Partial member/panel nominal budget only, using catalog where provided and nominal CAD density otherwise. Excludes bought hardware, many body attachments, liners/insulation, complete seats, trucks, brakes, HVAC and service equipment. Not coach tare.',
 'glazing_clear_area_m2':16*30*32*.0254**2,'critical_unfinished':['All J01 local HSS wall/contact/bolt/preload/weld/fatigue and global load paths','Window and door retention/emergency hardware','Roof strength, roof/end wall/purlin/skin/liner/insulation attachments and weathering','Bench/floor actual hardpoint collision and seat construction','Truck / wheel / axle / suspension / brake actual interfaces','Normal boarding side, stair/platform and emergency evacuation geometry','HVAC model and manufacturer mobile application/clearances/ventilation/condensate'],
 'checks':{'physical_solids_valid':all(s.isValid() for s in solids.values()),'unique_ids':len({p['id'] for p in parts})==len(parts),'post_count':22,'interior_J01_count':18,'special_end_receivers_undefined':4,'regular_places_reference':32,'physical_solids':sum(not k.startswith('SEAT-') for k in solids),'reference_solids':16,'web_mesh_parts':len(parts),'targeted_interface_overlap_pass':not interface_checks}}
(HERE/'calculations.json').write_text(json.dumps(calc,indent=2))
print(json.dumps({'generated_parts':len(parts),'physical_solids':len(solids),'drawings':4,'valid':calc['checks'],'mass_by_group_kg':dict(mass)}))

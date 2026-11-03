"""Reproducible suspension load study and retained-body interface drawing.
No dimensions of unselected suspension parts are generated.
"""

# Hosting transport: retain hashes of decoded source bytes after gzip packaging.
import gzip as _transport_gzip
def _transport_bytes(path):
    return path.read_bytes() if path.exists() else _transport_gzip.decompress(path.with_name(path.name + '.gz').read_bytes())

from pathlib import Path
import json, math, hashlib, html

ROOT=Path(__file__).resolve().parent
DIST=ROOT.parent.parent
G=9.80665
mass_path=DIST/'assets/brake-selection-l2/calculations/predecessor_mass_basis.json'
frame_path=DIST/'assets/models3d/frame-J1a.json'
mass=json.loads(mass_path.read_text())['configuration']
frame=json.loads(_transport_bytes(frame_path).decode())
def save(name,obj):
    (ROOT/name).write_text(json.dumps(obj,indent=2)+'\n')

inputs={
 'issue':'3L.3-S0','date':'2026-10-19','scope':'Suspension load specification and body-interface dimensional audit; not complete truck fabrication drawings',
 'units':'mm, N, kg, Hz unless noted','gravity_m_s2':G,
 'mass_provenance':{'path':str(mass_path.relative_to(DIST)),'sha256':hashlib.sha256(mass_path.read_bytes()).hexdigest(),'status':'Inherited allocations, not weighed or rated'},
 'frame_provenance':{'path':str(frame_path.relative_to(DIST)),'sha256':hashlib.sha256(_transport_bytes(frame_path)).hexdigest(),'status':frame['status']},
 'architecture':'Develop guided primary coil suspension, with springs between axlebox saddles and bogie frame; body supported through a separately retained center-bearing/pivot and controlled sidebearers. Equalization and secondary suspension remain alternatives pending twist/ride analysis.',
 'spring_count_per_truck_trial':8,'spring_count_basis':'Two coils per axlebox, four axleboxes per truck, for this calculation only; not a final hardware selection.',
 'unsprung_mass_per_truck_sensitivity_kg':[300,600,900,1200],
 'unsprung_mass_definition':'Wheelsets, axleboxes and all brake/carrier mass that moves with the axleboxes. Include effective participating spring mass in refined dynamics. These trial masses are not a verified range.',
 'loaded_bounce_frequency_sensitivity_Hz':[1.8,2.0,2.2],
 'frequency_status':'Analyst-selected sensitivity points, not a comfort standard or approved target.',
 'example_unsprung_mass_per_truck_kg':900,'example_loaded_frequency_Hz':2.0,
 'limitations':['Uniform loading and equal spring rates; vertical heave only; no roll, pitch, yaw, track twist, friction, damping, load redistribution or resonance acceptance.','Upper mass cases are design screens, not normal operating passenger loads.','Do not subtract only unsprung mass to calculate the body center-bearing force: the complete truck mass must be removed for that interface.','The existing 32-inch floor reference has no accepted load state. Loaded/empty operating floor heights remain to be fixed.'],
 'owner_visual_reference':{'date':'2026-10-19','use':'Appearance and drawing communication only','references':['TurboSquid complete bogie screenshot','Manchester wheel orthographic/section screenshot','Cults3D complete wagon screenshot','Rimutaka locomotive chassis and cab CAD screenshot'],'forbidden_inferences':['Do not scale screenshot geometry.','Do not import wheel profiles, spring arrangement, dimensions, material or load ratings.','Do not select spoked coach wheels because the example shows spokes.'],'required_output':'Recognizable assembled 3D truck and coordinated dimensioned orthographic, section and mounting/part drawings from the same supported geometry. Show purchased brakes only in train-installation context; no standalone drum-internals teardown.'},
 'release':{'spring_selected':False,'mounts_dimensioned_for_fabrication':False,'complete_truck_drawings':False,'fabrication_approved':False}
}
rows=[]
for coach,tare,full in [('regular',mass['regular_tare_allocation_kg'],mass['regular_upper_design_case_kg']),('accessible',mass['accessible_tare_allocation_kg'],mass['accessible_upper_design_case_kg'])]:
 for u in inputs['unsprung_mass_per_truck_sensitivity_kg']:
  for f in inputs['loaded_bounce_frequency_sensitivity_Hz']:
   ms=full/2-u;me=tare/2-u;n=8
   k=(2*math.pi*f)**2*ms/n/1000
   fl=ms*G/n;fe=me*G/n
   rows.append({'coach':coach,'tare_coach_kg':tare,'upper_coach_kg':full,'unsprung_trial_per_truck_kg':u,'sprung_upper_per_truck_kg':ms,'sprung_tare_per_truck_kg':me,'loaded_frequency_trial_Hz':f,'per_coil_rate_N_mm':k,'per_coil_tare_force_N':fe,'per_coil_upper_force_N':fl,'tare_static_compression_mm':fe/k,'upper_static_compression_mm':fl/k,'tare_to_upper_height_change_mm':(fl-fe)/k,'tare_frequency_Hz':f*math.sqrt(ms/me)})
examples=[r for r in rows if r['unsprung_trial_per_truck_kg']==900 and r['loaded_frequency_trial_Hz']==2]
results={'formulas':{'sprung_mass_per_truck':'m_s = M_coach/2 - m_unsprung','coil_rate':'k = (2*pi*f)^2*m_s/(8*1000) N/mm','coil_force':'F = m_s*g/8 N','compression':'delta = F/k mm','height_change':'Delta_h = (M_upper-M_tare)*g/(16*k) mm','empty_frequency':'f_empty = f_upper*sqrt(m_s_upper/m_s_empty)'},'sensitivity_rows':rows,'examples':examples,'interpretation':'Results specify a load/rate problem for spring development. They do not size the wire, spring seats, guides, dampers, bolts or welds.'}
save('inputs.json',inputs);save('calculations.json',results)

body={'coordinate_system':'Retained F1: x=front inside wall, positive rearward; y=coach centerline; z=rail top. All coordinates here refer to the existing body study, not final suspension mounts.',
 'reference_dimensions_mm':{'body_pivot_station_x':[45*25.4,261*25.4],'pivot_station_spacing':216*25.4,'main_girder_center_y':[-34*25.4,34*25.4],'main_girder_inner_y':[-32*25.4,32*25.4],'body_bolster_underside_z':19.003937007874015*25.4,'steel_top_z':31.003937007874015*25.4,'floor_reference_z':32*25.4,'central_bolster_x_width':4*25.4,'central_bolster_y_span':64*25.4,'central_bolster_z_depth':12*25.4},
 'reference_sections':'Retained J1a HSS12x4x1/4 nominal. Grade, delivered section, local reinforcement and welds remain unaccepted.',
 'new_suspension_interface_dimensions':{'truck_wheelbase_mm':None,'axlebox_centres_y_mm':None,'spring_centres_x_y_mm':None,'upper_seat_z_mm':None,'lower_seat_z_mm':None,'spring_installed_height_mm':None,'spring_diameter_mm':None,'spring_seat_plate_thickness_mm':None,'damper_eye_centres_mm':None,'center_bearing_stack_mm':None,'pivot_pin_diameter_mm':None,'sidebearer_y_mm':None,'sidebearer_gap_or_preload':None,'mount_bolt_holes_mm':None,'mount_weld_sizes_mm':None},
 'height_checks':[{'wheel_diameter_study_mm':d,'axle_z_mm':d/2,'bolster_bottom_minus_axle_z_mm':19.003937007874015*25.4-d/2} for d in [500,600]],
 'height_check_limitation':'232.7/182.7mm are datum differences only, not available spring height. Bolster is between axles; a collision exists only where moving volumes overlap. Bearing/seat/guide/frame/center-bearing stack and motion must be resolved in 3D.',
 'mount_load_path':[
 {'id':'S01','part':'Coach body bolster and local reinforcement','connects':'Body main girders to upper center-bearing assembly','definition_needed':'Center-bearing footprint, full truck mass, vertical/longitudinal/lateral/roll loads, local HSS wall/diaphragm and fatigue checks. Do not drill a kingpin hole through an unreinforced tube wall.'},
 {'id':'S02','part':'Center bearing, retained pivot and sidebearers','connects':'Coach bolster to bogie crossmember; permits yaw and specified pitch/roll','definition_needed':'Vertical load sharing, bearing area/material, pivot shear/bending/retention, sidebearer gap or preload, articulation and wear. A plain bolt is not a complete body support.'},
 {'id':'S03','part':'Upper spring seats and guide structure','connects':'Bogie side frame to each spring top','definition_needed':'Spring working diameter/end geometry, local plate bending, spring lateral force, guide/brake loads and continuous load path into frame webs.'},
 {'id':'S04','part':'Lower spring saddles','connects':'Each spring bottom to nonrotating axlebox','definition_needed':'Bearing housing shape and retention, seat offsets, combined vertical/brake moment loads. No welding seats to a rotating axle.'},
 {'id':'S05','part':'Axlebox guides, wear liners and retention','connects':'Axlebox to bogie frame while permitting designed travel and wheelset articulation','definition_needed':'Lateral/longitudinal force path, permitted angular motion, clearances, replaceable wear surfaces and drop-out retention. Brake reaction must not add a conflicting constraint.'},
 {'id':'S06','part':'Dampers, bump stops and rebound stops','connects':'Bogie frame to axlebox or assigned sprung member','definition_needed':'Motion ratio, damper force/velocity curve, full travel, angular limits, stop energy and load. Damper must not act as a travel stop unless rated to do so.'},
 {'id':'S07','part':'Installed D1 brake carrier, cam/chamber supports and hoses','connects':'Nonrotating axlebox/carrier to brake torque path and frame air supply','definition_needed':'Actual OEM envelope and interfaces; full suspension travel, yaw and service-removal clearance. Retain drum/hub extraction as one unit.'}
 ]}
save('body_interfaces.json',body)
sources=[{'id':'SRC-SKF','publisher':'SKF','url':'https://evolution.skf.com/us/the-evolution-of-railway-axlebox-technology-3/','published':'2010-12-07','checked':'2026-10-19','use':'Wheelset bearings in axleboxes; springs connect axleboxes and running gear. No dimensions transferred.'},{'id':'SRC-CFD','publisher':'CFD','url':'https://www.cfd.group/rolling-stock/railcar-bogie','checked':'2026-10-19','use':'Real passenger bogie example with primary coils and dampers; two-stage suspension is a comparison, not selected equipment.'},{'id':'SRC-LEE','publisher':'Lee Spring','url':'https://www.leespring.com/sites/default/files/2021-02/compression-springs-lee-spring-us.pdf','checked':'2026-10-19','use':'Definitions of rate, free length and solid height; avoid operation at solid. No catalog spring selected.'}]
save('sources.json',sources)

# Dimensioned actual retained body geometry, not fabricated suspension proxies.
S=['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1100" viewBox="0 0 1600 1100"><defs><marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#176b78"/></marker></defs><rect width="1600" height="1100" fill="white"/><style>text{font-family:Arial,sans-serif;fill:#172d39}.small{font-size:19px}.dim{font-size:21px;fill:#176b78}.line{stroke:#176b78;stroke-width:1.5}.ext{stroke:#8799a1;stroke-width:1}.center{stroke:#bd6d17;stroke-width:1.5;stroke-dasharray:12 5 2 5}</style>']
def text(x,y,t,size=21,cls=''):
 S.append(f'<text x="{x}" y="{y}" font-size="{size}" class="{cls}">{html.escape(t)}</text>')
def line(x1,y1,x2,y2,cls='line',arrows=False):
 S.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cls}"'+(' marker-start="url(#arrow)" marker-end="url(#arrow)"' if arrows else '')+'/>')
def dh(a,b,y,label,base):
 line(a,base,a,y+8,'ext');line(b,base,b,y+8,'ext');line(a,y,b,y,arrows=True);text((a+b)/2-len(label)*5.1,y-10,label,21,'dim')
text(50,52,'PF–3L.3–S01  |  COACH-TO-TRUCK BODY DATUMS',30)
text(50,84,'REFERENCE GEOMETRY ONLY · J1a retained study · millimetres [inches] · NOT FOR FABRICATION',21)
text(50,126,'A. BODY PLAN — truck center stations; these are not a mounting-hole pattern',23)
ox,oy,sc=210,340,2.95
def X(v):return ox+v*sc
def Y(v):return oy-v*sc
for p in frame['parts']:
 if p['group'] not in ['frame_main','frame_bolsters','frame_perimeter']:continue
 b=p['bounds_in'];x=X(b['x'][0]);y=Y(b['y'][1]);w=(b['x'][1]-b['x'][0])*sc;h=(b['y'][1]-b['y'][0])*sc
 color='#d68a32' if p['group']=='frame_bolsters' else '#d5dfe2'
 S.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}" stroke="#334b56" stroke-width="1.4"/>')
for station in [0,45,261]:line(X(station),165,X(station),555,'center')
line(55,oy,1290,oy,'center')
for st in [45,261]:
 S.append(f'<circle cx="{X(st)}" cy="{oy}" r="12" fill="white" stroke="#ad5810" stroke-width="2"/>')
text(X(0)-8,607,'x=0 front inside wall',19)
text(X(45)+16,330,'FRONT',19);text(X(261)+16,330,'REAR',19)
dh(X(45),X(261),152,'5486.4 [216] centers',178)
dh(X(0),X(45),538,'1143 [45]',500)
dh(X(0),X(261),576,'6629.4 [261] from datum',500)
text(1320,208,'Main girders:',20);text(1320,240,'y = ±863.6',21);text(1320,268,'[±34]',21)
text(1320,320,'Bolster width:',20);text(1320,352,'101.6 [4]',21)
text(1320,410,'Center symbols',19);text(1320,436,'locate axes only.',19);text(1320,462,'Bearing footprint',19);text(1320,488,'is not selected.',19)
text(50,630,'B. SECTION AT BODY BOLSTER — central span between main girdder inner faces'.replace('girdder','girder'),23)
sx,sy,ss=170,940,0.42
def YY(v):return sx+(v+914.4)*ss
def ZZ(v):return sy-(v-350)*ss
z0=body['reference_dimensions_mm']['body_bolster_underside_z'];z1=body['reference_dimensions_mm']['steel_top_z']
for lo,hi in [(-914.4,-812.8),(-812.8,812.8),(812.8,914.4)]:
 S.append(f'<rect x="{YY(lo)}" y="{ZZ(z1)}" width="{(hi-lo)*ss}" height="{(z1-z0)*ss}" fill="#e2e8eb" stroke="#334b56" stroke-width="2"/>')
# Show HSS voids: longitudinal section of bolster and transverse sections of girders.
for lo,hi in [(-914.4,-812.8),(-812.8,812.8),(812.8,914.4)]:
 inset=6.35
 S.append(f'<rect x="{YY(lo+inset)}" y="{ZZ(z1-inset)}" width="{(hi-lo-2*inset)*ss}" height="{(z1-z0-2*inset)*ss}" fill="white" stroke="#334b56" stroke-width="1"/>')
line(YY(0),690,YY(0),1020,'center');line(YY(-914.4),ZZ(812.8),YY(914.4),ZZ(812.8))
dh(YY(-812.8),YY(812.8),990,'1625.6 [64] central bolster span',ZZ(z0))
text(980,710,'Floor reference z = 812.8 [32]',22)
text(980,746,'Steel top z = 787.5 [31.004]',22)
text(980,782,'Bolster underside z = 482.7 [19.004]',22)
text(980,828,'Retained nominal HSS 12 × 4 × 1/4.',20)
text(980,858,'Local bearing plate, diaphragms, pivot,',20)
text(980,886,'sidebearers, holes and welds: unresolved.',20)
line(YY(0),ZZ(z0),YY(0),936,arrows=True)
text(360,943,'S01 / S02: body-to-truck connection here',20)
line(40,1030,1560,1030,'ext')
text(50,1060,'Do not scale. Drawing records inherited body datums, not a completed spring mount or approved member size.',20)
text(50,1088,'Source: frame-J1a.json; see body_interfaces.json. Floor reference load state and complete suspension stack remain open.',18)
S.append('</svg>');(ROOT/'S01-body-datums.svg').write_text(''.join(S))

checks={'issue':'3L.3-S0','arithmetic_checks':[],'scope':'Automated consistency only; no engineering or visual approval'}
for r in rows:
 assert r['sprung_tare_per_truck_kg']>0
 assert abs(r['per_coil_upper_force_N']*8-r['sprung_upper_per_truck_kg']*G)<1e-7
 assert abs(r['upper_static_compression_mm']-1000*G/(2*math.pi*r['loaded_frequency_trial_Hz'])**2)<1e-9
checks['arithmetic_checks']=['All 24 cases have positive sprung mass.','Coil forces recover uniform truck sprung weight.','Static deflection agrees with g/(2*pi*f)^2.','Body stations agree with retained frame model.']
assert any(p['centre_in'][0]==45 for p in frame['parts'] if p['group']=='frame_bolsters')
save('validation.json',checks)
print(json.dumps({'cases':len(rows),'examples':examples,'drawing':'S01-body-datums.svg'}))

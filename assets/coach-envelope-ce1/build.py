"""CE1: deterministic enclosure sections and bounded thermal/mass coordination.
Run from any directory. Does not alter retained C1/CI3 structural CAD.
"""
from pathlib import Path
import gzip, hashlib, html, json, math, re

ROOT=Path(__file__).resolve().parents[2]; D=ROOT/'dist'; HERE=Path(__file__).parent
OUT=D/'assets/coach-envelope-ce1'; OUT.mkdir(parents=True,exist_ok=True)
source=D/'assets/coach-body-c1/parts.json.gz'
for evidence in ['floor-projection.json','floor_projection.py']:
 (OUT/evidence).write_bytes((HERE/evidence).read_bytes())
parts=json.loads(gzip.decompress(source.read_bytes()))
IN=.0254; AL=2680; WOOL=64; liner=.040; floor=32.
R=177.50366311097392; ZC=-56.88948988262746; RI=R-2-1-liner
wall_y=52.125-1-liner; bench_y=50.75
def head(y): return ZC+math.sqrt(RI*RI-y*y)-floor
geometry=dict(floor_z_in=floor,finished_wall_y_in=wall_y,finished_width_in=2*wall_y,
 finished_length_in=305.46-.54,center_headroom_in=head(0),aisle_edge_headroom_in=head(12),
 local_eave_headroom_in=110-1-liner-floor,raised_headroom_in=132-1-liner-floor,
 bench_width_in=bench_y-12,bench_wall_gap_in=wall_y-bench_y,aisle_width_in=24,
 bracket_box_inner_y_in=49.625-1-liner,bracket_box_top_z_in=41.5+1+liner,
 floor_panel_bottom_z_in=31.003937007874+3/25.4,floor_panel_top_z_in=31.003937007874+3/25.4+.75,
 floor_insulation_bottom_z_in=31.003937007874+3/25.4-2,
 mini_split_bottom_above_floor_in=132-1-liner-floor-4-12.1875)
areas={}
for prefix in ['SK','RS','RH','EG','ES']:
 areas[prefix]=sum(p['metadata']['solid_mass_kg'] for p in parts if p['group']=='skin' and p['id'].startswith(prefix+'-'))/(AL*(1/16)*IN)
old_floor_mass=sum(p['metadata']['solid_mass_kg'] for p in parts if p['group']=='floor')
areas=dict(side_wall=areas['SK'],roof=areas['RS']+areas['RH'],end_wall=areas['EG']+areas['ES'],
 door=2*32*80*IN**2,window=16*30*32*IN**2,
 floor=geometry['finished_length_in']*geometry['finished_width_in']*IN**2,
 floor_panel_takeoff=old_floor_mass/(100*.75*IN))
# One-dimensional parallel path screen. Direct bridges are explicit sensitivities,
# not measured fractions. Treat steel as solid through-depth, ignoring hollow HSS R.
def u(cavity,ci,frame,direct,film):
 bay=film+.04+(cavity+ci)*.74
 steel=film+.04+ci*.74+cavity*IN/45
 bypass=film+.04+(cavity+ci)*IN/45
 return (1-direct)*((1-frame)/bay+frame/steel)+direct/bypass
thermal_sets={}
for name,fw,fr,bridge,ff,glass in [('study',.20,.12,.02,.60,2.7),('conservative',.30,.20,.05,.50,5.7)]:
 vals=dict(side_wall=u(3,1,fw,bridge,.13),roof=u(2,1,fr,bridge,.10),
  end_wall=u(2,1,fw,bridge,.13),door=u(1,0,.20,.02,.13),
  floor=ff/(.10+.04+2*.74)+(1-ff)/(.10+.04),window=glass)
 thermal_sets[name]=dict(u_w_m2k=vals,ua_w_k=sum(areas[k]*v for k,v in vals.items()),
  frame_fraction_wall=fw,frame_fraction_roof=fr,direct_bridge_fraction=bridge,
  floor_insulated_fraction=ff)
thermal_sets['old_u_same_geometry']=dict(u_w_m2k={k:(2.7 if k=='window' else 1.5) for k in thermal_sets['study']['u_w_m2k']})
thermal_sets['old_u_same_geometry']['ua_w_k']=sum(areas[k]*v for k,v in thermal_sets['old_u_same_geometry']['u_w_m2k'].items())
thermal_sets['limited_floor']=dict(thermal_sets['study'])
thermal_sets['limited_floor']['u_w_m2k']=dict(thermal_sets['study']['u_w_m2k'])
thermal_sets['limited_floor']['u_w_m2k']['floor']=.25/(.10+.04+2*.74)+.75/(.10+.04)
thermal_sets['limited_floor']['floor_insulated_fraction']=.25
thermal_sets['limited_floor']['ua_w_k']=sum(areas[k]*v for k,v in thermal_sets['limited_floor']['u_w_m2k'].items())
conditions=[('85°F evening',85,75,False,False,0),('95°F evening',95,75,False,False,0),
 ('95°F sun',95,75,False,True,0),('110°F sun',110,75,False,True,0),
 ('110°F sun + humidity stress',110,75,False,True,.006),('20°F occupied heating',20,68,True,False,0)]
cases=[]
for name,t in thermal_sets.items():
 for cfm in [300,400]:
  for label,out,inside,heat,sun,dw in conditions:
   dt=abs(out-inside)/1.8; q=cfm/2118.880003
   p=dict(conduction=t['ua_w_k']*dt/1000,ventilation=1.2*1.006*q*dt,
    doors=1.2*1.006*.03*dt,people_sensible=(-1 if heat else 1)*37*.075,
    people_latent=0 if heat else 37*.045,equipment=(-1 if heat else 1)*.420,
    solar=(areas['window']*.5*500+areas['roof']*t['u_w_m2k']['roof']*20)/1000 if sun else 0,
    outside_latent=0 if heat else 1.2*(q+.03)*2501*dw)
   kw=max(0,sum(p.values()))*(1 if heat else 1.15)
   cases.append(dict(envelope=name,condition=label,cfm=cfm,parts_kw=p,kw=kw,btuh=kw*3412.141633))
def case(label,name='study',cfm=300):return next(c for c in cases if c['condition']==label and c['envelope']==name and c['cfm']==cfm)
# Gross liner area equals extracted outer sheet area: conservative procurement proxy,
# not an exact inner skin cut list. Cavity fractions below are quantity assumptions.
mass=dict(wall_roof_end_liners_kg=(areas['side_wall']+areas['roof']+areas['end_wall'])*liner*IN*AL,
 door_liners_kg=areas['door']*liner*IN*AL,
 wall_insulation_kg=areas['side_wall']*(3*.8+1)*IN*WOOL,
 roof_insulation_kg=areas['roof']*(2*.88+1)*IN*WOOL,
 end_insulation_kg=areas['end_wall']*(2*.8+1)*IN*WOOL,
 door_insulation_kg=areas['door']*1*.8*IN*WOOL,
 floor_insulation_kg=areas['floor']*.60*2*IN*WOOL,
 floor_trays_kg=areas['floor']*.60*liner*IN*AL,
 replacement_floor_panel_delta_kg=areas['floor_panel_takeoff']*4.6-old_floor_mass,
 rubber_finish_kg=areas['floor_panel_takeoff']*4.17,
 unmodeled_fixings_closeouts_seals_adhesive_reserve_kg=60)
mass['subtotal_increment_kg']=sum(mass.values())
mass['quantity_fit_allowance_kg']=.10*(mass['subtotal_increment_kg']-60)
mass['screen_increment_with_allowance_kg']=mass['subtotal_increment_kg']+mass['quantity_fit_allowance_kg']
data=dict(revision='CE1',date='2026-10-26',status='CONSTRUCTION PROPOSAL; NOT FABRICATION RELEASE',
 geometry=geometry,areas_m2=areas,thermal_sets=thermal_sets,cases=cases,mass=mass,
 basis=dict(thermal_people=37,airflow_cfm=[300,400],recovery=0,cooling_allowance=1.15,
 cabin_equipment_w=420,door_leakage_m3s=.03,glass_shgc=.5,rockboard_rsi_per_in=.74,
 steel_k_w_mk=45,film_r_m2k=dict(wall_inside=.13,roof_inside=.10,floor_inside=.10,outside=.04),
 floor_panel_thermal_credit=0,assembly_u_status='1D screening only; 2D bridges, fasteners, openings and moisture not qualified',
 floor_clear_fraction_basis='Current static bounding-box union: 61.847% with 0.25in XY allowance; use60% study/50% sensitivity. Moving/service envelopes excluded.'),
 limitations=['Regular C1 envelope only; ADA cutouts, seats, turning and bridge interfaces require separate integration.',
 'No heat-recovery cabinet selected. Compact powered roof intake/exhaust remain unselected; no recovery credit.',
 'Neither300CFM nor400CFM is an adopted ventilation rate. Eight mini-splits and35kW generator remain provisional.',
 'Final glazing, floor support/point-load capacity, fastening and transport fire qualification remain open.',
 'Thermal outputs are delivered steady-state loads, not electrical input or equipment selection.',
 'No whole-coach mass/CG or suspension acceptance; do not add historicalCL3 cabinet reserve as installed equipment.'],
 source_sha256={str(source.relative_to(ROOT)):hashlib.sha256(source.read_bytes()).hexdigest()})

# Draw sections from the same dimensions used by the calculation, with uncluttered
# separate enlarged assembly keys. All units inches unless explicitly millimeters.
COL={'ink':'#17364a','wool':'#e7c673','steel':'#688592','liner':'#287f77','skin':'#9ca8ad','paper':'#faf8f1'}
def start(title,subtitle,h=820):
 return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 {h}" role="img"><title>{html.escape(title)}</title><desc>{html.escape(subtitle)}</desc><defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="3.5" refY="3.5" orient="auto-start-reverse"><path d="M0 0L7 3.5L0 7" fill="#17364a"/></marker><pattern id="wool" width="12" height="12" patternUnits="userSpaceOnUse"><path d="M0 12L12 0" stroke="#c0a24f" stroke-width="1"/></pattern></defs><style>text{{font-family:Arial,sans-serif;fill:#17364a}}.title{{font-size:29px;font-weight:700}}.sub{{font-size:16px}}.note{{font-size:17px}}.small{{font-size:14px}}.dim{{stroke:#17364a;stroke-width:1;marker-start:url(#arrow);marker-end:url(#arrow)}}.thin{{stroke:#688592;stroke-width:1;fill:none}}</style><rect width="1200" height="{h}" fill="#faf8f1"/><text x="35" y="46" class="title">{html.escape(title)}</text><text x="35" y="77" class="sub">{html.escape(subtitle)}</text>']
def txt(s,x,y,t,cl='note'):s.append(f'<text x="{x}" y="{y}" class="{cl}">{html.escape(str(t))}</text>')
def rect(s,x,y,w,h,fill,stroke='#17364a'):s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}"/>')
def line(s,x1,y1,x2,y2,cl='thin'):s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cl}"/>')
def finish(s,name,h=820):txt(s,35,h-22,'CE1 · 26 OCT 2026 · DIMENSIONED COORDINATION PROPOSAL · NOT FOR CONSTRUCTION','small');s.append('</svg>');(OUT/name).write_text('\n'.join(s))
s=start('CE1-A01 / Finished coach cross-section','Regular coach · main roof bay · generated from C1 radii and CE1 lining offsets')
sc=5.4; ox=355; oy=670
def X(y):return ox+y*sc
def Y(z):return oy-(z-32)*sc
def arc(rad,ymin,ymax):return [(X(y),Y(ZC+math.sqrt(rad*rad-y*y))) for y in [ymin+(ymax-ymin)*i/120 for i in range(121)]]
def band(r1,r2,fill):
 pts=arc(r1,-54.625,54.625)+arc(r2,-54.625,54.625)[::-1]
 s.append('<polygon points="'+' '.join(f'{x:.3f},{y:.3f}' for x,y in pts)+f'" fill="{fill}" stroke="#17364a" stroke-width=".7"/>')
band(R+.0625,R,'#9ca8ad');band(R,R-2,'#e7c673');band(R-2,R-3,'#f4dd9c');band(R-3,RI,'#287f77')
for sign in [-1,1]:
 for lo,hi,fill in [(52.125,55.125,'#e7c673'),(51.125,52.125,'#f4dd9c'),(51.085,51.125,'#287f77')]:
  xx=sign*lo if sign>0 else -hi;rect(s,X(xx),Y(110),(hi-lo)*sc,(110-32)*sc,fill)
 rect(s,X(12 if sign>0 else -bench_y),Y(49),geometry['bench_width_in']*sc,3*sc,'#b79a77')
 # Original bench outline demonstrates real fit conflict.
 xx=12 if sign>0 else -52
 s.append(f'<rect x="{X(xx)}" y="{Y(49)}" width="{40*sc}" height="{3*sc}" fill="none" stroke="#b55743" stroke-dasharray="5 3"/>')
rect(s,X(-wall_y),Y(32),2*wall_y*sc,.878*sc,'#688592')
line(s,X(-12),Y(44),X(12),Y(44),'dim');txt(s,X(-9),Y(39),'24″ aisle','small')
line(s,X(0),Y(32),X(0),Y(32+head(0)),'dim');txt(s,367,390,f'{head(0):.2f}″','note')
line(s,X(-wall_y),715,X(wall_y),715,'dim');txt(s,224,742,f'{2*wall_y:.2f}″ finished width')
txt(s,720,160,'HEADROOM FROM FINISHED FLOOR')
for i,t in enumerate([f'Center: {head(0):.2f}″ (7′ 1.57″)',f'24″ aisle edge: {head(12):.2f}″',f'Local eave soffit: {geometry["local_eave_headroom_in"]:.2f}″',f'Raised end: {geometry["raised_headroom_in"]:.2f}″', 'Before lights, grilles, tolerances or deflection.']):txt(s,720,197+30*i,t,'note' if i<4 else 'small')
txt(s,720,385,'SEAT COORDINATION CHANGE')
for i,t in enumerate(['Proposed bench: 38.75″ wide.', 'Inner edge stays at Y ±12″.', 'Outer edge becomes Y ±50.75″.', '0.335″ nominal wall gap.', 'Red dashed outline: existing 40″ bench.', 'Shorten pan and outboard steel; retain feet.', 'Seat strength and capacity review remains open.']):txt(s,720,420+27*i,t,'small')
txt(s,720,655,'J01 brackets are between rows; local boxes', 'small');txt(s,720,678,'reduce width to 97.17″ below Z42.54″.', 'small')
finish(s,'CE1-A01.svg')

s=start('CE1-D01 / Wall, roof and opening construction','Layer thicknesses are the proposed construction basis; enlarged keys are not to scale')
def stack(x,y,title,rows):
 txt(s,x,y,title)
 for i,(label,color) in enumerate(rows):
  rect(s,x,y+23+i*53,465,43,color);txt(s,x+12,y+50+i*53,label,'small')
stack(35,125,'SIDE WALL · OUTSIDE → INSIDE',[( '1/16″ retained aluminum exterior skin','#cbd2d4'),('3″ mineral wool between HSS wall members','#e7c673'),('1″ continuous mineral wool inside steel','#f4dd9c'),('.040″ removable 5052-H32 aluminum lining','#c7e3dc')])
stack(660,125,'MAIN ROOF · OUTSIDE → INSIDE',[('1/16″ retained curved aluminum roof','#cbd2d4'),('2″ mineral wool between roof hoops','#e7c673'),('1″ continuous mineral wool below hoops','#f4dd9c'),('.040″ curved removable aluminum lining','#c7e3dc')])
txt(s,35,405,'END WALL / DOOR EXCEPTIONS')
for i,t in enumerate(['End frame is 2″ deep: use 2″ cavity + 1″ continuous + .040″ lining.', 'Finished end planes X0.54″ and X305.46″; clear length304.92″.', 'Moving 1.5″ door leaf: 1″ cavity board + .040″ inside skin; no extra 1″ overlay.', 'Door-edge structure and seals retain clear openings; leaf/hardware detail still open.']):txt(s,35,441+i*27,t,'small')
txt(s,35,584,'SEALED OPENINGS / REMOVABLE PANELS')
for i,t in enumerate(['Return the lining to a gasketed, independently supported window frame; do not cover the glazing opening.', 'Seal interior liner joints and penetrations as the air-control layer; use removable gasketed joint covers.', 'Mechanically retain wool. Liner clips land on steel with rigid isolated spacers inside the 1″ layer.', 'Do not clamp or hang seats, HVAC, grilles or handrails from soft insulation or thin lining.', 'Weather-seal exterior laps and curbs; provide a drained sill path outward and removable inspection access.', 'No added polyethylene layer specified. Check seasonal condensation before closing both metal skins.']):txt(s,35,620+i*26,t,'small')
finish(s,'CE1-D01.svg')

s=start('CE1-D02 / Floor cassette and hardpoint detail','Keep the finished walking surface at Z32.000″ · insulation fits below the existing deck')
stack(35,125,'TOP → BOTTOM IN AN OPEN FRAME BAY', [('2.5 mm rubber finish + 0.75 mm adhesive budget','#b79a77'),('3/4″ aluminum honeycomb structural panel','#cbd2d4'),('2″ mineral wool below deck, clear of frame','#e7c673'),('.040″ removable protective aluminum tray','#c7e3dc')])
txt(s,650,125,'FIXED DATUMS')
for i,t in enumerate(['Finished floor: Z32.000″',f'Panel top: Z{geometry["floor_panel_top_z_in"]:.3f}″',f'Panel underside: Z{geometry["floor_panel_bottom_z_in"]:.3f}″','Frame top: Z31.004″ + 3 mm support pad',f'Wool underside: Z{geometry["floor_insulation_bottom_z_in"]:.3f}″',f'Tray underside: Z{geometry["floor_insulation_bottom_z_in"]-.04:.3f}″']):txt(s,650,164+i*31,t,'note')
txt(s,35,420,'FRAME / FASTENERS / THRESHOLDS')
for i,t in enumerate(['Each panel edge needs support and a sealed closeout; supplier inserts carry point loads without crushing core.', 'Seat feet and accessible securement loads go into retained steel hardpoints, through isolated sealed sleeves.', 'No floor insulation is placed between the structural deck and its supports; retain the 3 mm support isolation.', 'Removable bay trays attach to frame-side brackets and closeouts, not to unsupported honeycomb skins.', 'Terminate cassettes clear of CI2/CI3 bridges, bolsters, brackets, moving trucks, brake hoses and service paths.', 'Keep entrance and bridge thresholds flush. The proposed adhesive allowance must match the selected system.', 'Open honeycomb edges, cutouts and penetrations require sealed closure; floor seams need a compatible seal.']):txt(s,35,457+i*29,t,'small')
rect(s,35,683,1125,75,'#f4e8cb');txt(s,53,711,'Provisional insulation coverage: 60% of finished floor area.', 'note');txt(s,53,739,'This deliberately keeps exposed steel in the heat-loss model. Static fit is screened; moving/service clearance is not accepted.','small')
finish(s,'CE1-D02.svg')

css='''body{color:#17364a}.ce-hero{max-width:870px}.ce-hero h1{font-size:clamp(2.2rem,5vw,3.7rem);line-height:1.06}.ce-lead{font-size:1.15rem;line-height:1.6}p,li{line-height:1.65}.ce-nav{display:flex;flex-wrap:wrap;gap:1rem;margin:1.5rem 0}.ce-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem}.ce-card{padding:1.3rem;background:#e8eee8;border:1px solid #c7d4cc;border-radius:7px}.ce-card strong{display:block;font-size:1.9rem}.ce-note{padding:1.1rem 1.3rem;background:#f7edd8;border-left:4px solid #b18342;margin:1.5rem 0}.ce-good{background:#e8eee8;border-left-color:#347462}h2{margin-top:2.6rem}.ce-figure{margin:1.5rem 0;border:1px solid #c7d4cc;background:#faf8f1;border-radius:7px;overflow:hidden}.ce-figure img{width:100%;height:auto;display:block}.ce-figure figcaption{padding:.8rem 1rem;font-size:.9rem}.ce-table{overflow:auto;border:1px solid #c7d4cc;border-radius:6px;margin:1.2rem 0}table{border-collapse:collapse;width:100%;min-width:640px}td,th{padding:.85rem;text-align:left;vertical-align:top;border-bottom:1px solid #d3ded8}th{background:#e8eee8}a{color:#165b70}.ce-small{font-size:.9rem;color:#53675f}.ce-source{overflow-wrap:anywhere}.ce-selector{display:flex;flex-wrap:wrap;gap:1rem;margin:1.2rem 0}.ce-selector label{display:grid;gap:.35rem}.ce-selector select{font:inherit;padding:.65rem;border:1px solid #688592;border-radius:5px;background:white}details{border:1px solid #c7d4cc;padding:1rem;margin:1rem 0}summary{cursor:pointer;font-weight:700}@media(max-width:700px){.ce-cards{grid-template-columns:1fr}.ce-card strong{font-size:1.6rem}td,th{padding:.7rem}}'''
(D/'coach-envelope.css').write_text(css)
def page(title,body):return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>{title} · Pulsipher Farms</title><link rel="stylesheet" href="site-shell.css?v=cleanup1"><link rel="stylesheet" href="coach-envelope.css"></head><body class="pf-portal"><a class="pf-skip" href="#content">Skip to content</a><header class="pf-header"><a class="pf-brand" href="index.html"><b>PF</b><span>PULSIPHER FARMS<small>TRAIN DESIGN WORKSHOP</small></span></a><nav class="pf-nav"><a href="coaches.html">Coaches</a><a href="drawings.html">Drawings &amp; 3D</a><a href="engineering-index.html">Engineering</a></nav></header><main class="pf-main" id="content">{body}</main><footer class="pf-footer"><span>CE1 · Development construction proposal</span><a href="archive.html">Previous versions</a></footer></body></html>'''
def table(headers,rows):return '<div class="ce-table"><table><thead><tr>'+''.join('<th>'+x+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(c)+'</td>' for c in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def fig(name,caption):return f'<figure class="ce-figure"><a href="assets/coach-envelope-ce1/{name}.svg"><img src="assets/coach-envelope-ce1/{name}.svg" alt="{html.escape(caption)}"></a><figcaption>{caption} · <a href="assets/coach-envelope-ce1/{name}.svg">Open full drawing</a></figcaption></figure>'
body=f'''<section class="ce-hero"><p class="pf-eyebrow">CE1 · COACH ENCLOSURE · 26 OCTOBER 2026</p><h1>Build the enclosure into the dimensions.</h1><p class="ce-lead">A defined wall, roof and floor proposal for the enclosed coaches: mineral-wool insulation, removable aluminum lining and an insulated floor that keeps the existing boarding height. This sets a construction basis for the next headroom and HVAC review.</p></section><nav class="ce-nav"><a href="#layers">Construction</a><a href="#fit">Interior fit</a><a href="#floor">Floor</a><a href="#climate">HVAC implications</a><a href="coach-envelope-engineering.html">Calculations &amp; sources →</a></nav><div class="ce-cards"><div class="ce-card"><strong>7′ 1.57″</strong>Main-roof center headroom after lining.</div><div class="ce-card"><strong>102.17″</strong>Finished clear width above local bracket boxes.</div><div class="ce-card"><strong>Same floor height</strong>Insulation below the walking deck.</div></div><p class="ce-note">These are proposed finished dimensions, not an approved coach build. The sections below add the missing enclosure detail; the retained whole-coach CAD still contains the earlier bare shell and 40″ benches.</p>
<h2 id="layers">Construction from outside to inside</h2>'''
body+=table(['Assembly','Proposed layers','Total / consequence'],[
 ['Side walls','1/16″ aluminum exterior • 3″ cavity mineral wool • 1″ continuous mineral wool • .040″ aluminum lining','4.1025″ from exterior face to finished interior. Adds1.040″ inside the steel.'],
 ['Curved roof','1/16″ aluminum exterior • 2″ cavity mineral wool • 1″ continuous mineral wool • .040″ aluminum lining','3.1025″ radial build; continuous layer follows the roof curve.'],
 ['End walls','Retained exterior • 2″ cavity mineral wool • 1″ continuous layer • .040″ lining','End framing is shallower than the side posts. Keep doorway returns outside clear openings.'],
 ['Door leaves','Retained1.5″ leaf • 1″ cavity mineral wool • .040″ interior lining','No continuous1″ overlay across moving leaves. Seals and hardware remain to detail.'],
 ['Floor','2.5mm rubber + adhesive budget • 3/4″ aluminum honeycomb deck • 2″ wool in clear bays • .040″ protective trays','Deck stays at the existing datum; insulation is discontinuous around steel and moving/service equipment.']])
body+='''<p>Use <strong>ROCKWOOL Rockboard40</strong> as the insulation candidate and <strong>.040″5052-H32 aluminum</strong> for removable interior panels. A painted lining provides the finished interior surface; the exterior’s four retained color references are unchanged. The wool must be mechanically retained and fully enclosed. No exposed insulation faces the passengers or ventilation air path.</p><p>Mount the lining on rigid, isolated clips or spacers within the1″ continuous layer. Soft mineral wool carries no mounting load. Seats, mini-splits, handrails and roof fans attach to the steel structure through separately designed hardpoints. Any added furring depth requires a new headroom calculation.</p>'''
body+=fig('CE1-D01','Wall, roof, end-wall and opening assembly keys')
body+='<h2 id="fit">The wall lining changes the benches</h2><p>The current40″ benches reach Y±52″. The new wall surface is at Y±51.085″, producing a0.915″ overlap. The proposed correction keeps the24″ aisle and the existing feet, but shortens each bench’s outer steel, pan and pad to <strong>38.75″ wide</strong>. That leaves a0.335″ nominal wall gap. Seat strength, comfort and actual passenger capacity must be checked with this revision.</p>'
body+=fig('CE1-A01','Dimensioned finished section; current bench outline shown dashed')
body+=table(['Location','Nominal finished clearance','What it means'],[
 ['Main roof center',f'{head(0):.2f}″','Before fixtures and tolerances.'],['Edge of actual24″ aisle',f'{head(12):.2f}″','Use the actual aisle; the32″ regular end door is a different dimension.'],
 ['Local eave soffit',f'{geometry["local_eave_headroom_in"]:.2f}″','Low edge above seats; not standing aisle headroom.'],['Raised end roof','98.96″','Preserves the above-door mini-split investigation.'],
 ['Finished body length','304.92″','End-wall inner faces at X0.54″ /305.46″.'],['Local floor bracket boxes','97.17″ clear between boxes','J01 pockets are between seat rows and extend to Z42.54″; no accepted ADA route check.']])
body+='''<p>At a raised end, a12-3/16″ indoor unit with a4″ top-clearance reservation would have its bottom about<strong>82.77″ above the floor</strong>. That leaves only2.77″ above an80″ door before trim and supports. This supports continued mini-split packaging; it does not establish a final model, air throw or installation clearance.</p><p class="ce-note">The accessible coach needs its own finished-shell check:36″ boarding route,78″ side-door height, offset end doors, folded seats, wheelchair turning and securement. The C3.1 pin-withdrawal envelope has only1.085″ to the proposed wall; hand/tool access remains unresolved. Do not apply the regular bench change to the ADA seats automatically.</p>
<h2 id="floor">Keep insulation below the floor</h2><p>The candidate deck is a3/4″ <strong>PlascoreAA3.6-80 aluminum honeycomb panel</strong>, with2.5mm <strong>AltroTransflorMotus</strong> rubber flooring. A0.75mm adhesive/leveling budget completes the existing3.25mm finish space. The selected adhesive system must fit that budget; no raised threshold is accepted by this proposal.</p>'''
body+=fig('CE1-D02','Floor datums, removable underside cassettes and load-path requirements')
body+=f'''<p>Floor insulation cannot run through the frame. A static projection check leaves61.85% clear after provisional gaps; use<strong>60% coverage</strong> for this study, with50% and25% sensitivity cases. The cassette layout still needs moving-truck, brake-hose, debris, drainage and service clearance checks. Honeycomb edges need sealed closeouts, and panel joints and hardpoints need supported load paths.</p><p>The floor panel’s catalog coupon properties do not establish passenger-floor or wheelchair point-load capacity. Confirm actual support spans, deflection, local crushing, inserts and adhesives before ordering. The insulation is not a structural core or support pad.</p>
<h2>Water, air and service access</h2><p>Make the removable interior lining a sealed air-control layer with gasketed seams and sealed penetrations. Weather-seal the exterior, drain window sills outward, isolate dissimilar metals and provide removable access at roof penetrations, drains, door hardware and frame connections. Assemble dry and check seasonal condensation before closing two metal skins; no added interior polyethylene layer is specified.</p><p>Roof fans need flashed curbs and steel-supported mounts. Mini-split condensate drains require continuous fall, insulation where condensation can occur, accessible traps if required by the manufacturer, and protected discharge away from boarding surfaces. Their exact routes remain open.</p>
<h2 id="climate">What this changes for HVAC</h2><p>The earlier generic opaqueU=1.5 assumption is replaced by assembly-based screening, including steel and uninsulated floor paths. Whole-wall performance is lower than the insulation’s advertised R-value. Window construction, edge losses and attachment bridges still matter.</p><p class="ce-note ce-good"><strong>Current direction:</strong> retain mini-splits and develop compact powered roof intake and powered exhaust. The earlierCL3 rear heat-recovery cabinet does not fit the user’s preferred arrangement and is superseded. This study takes<strong>zero heat-recovery credit</strong>. Airflow and fan selection remain open.</p>'''
body+=table(['Regular coach •300CFM study','EarlierU on same geometry','CE1 assembly screen'],[[label,f'{case(label,"old_u_same_geometry")["btuh"]:,.0f}BTU/h',f'{case(label)["btuh"]:,.0f}BTU/h'] for label in ['95°F evening','95°F sun','110°F sun','20°F occupied heating']])
body+=f'''<p class="ce-small">37 people as a heat-load allowance; not approved occupancy. Dry cooling includes occupant moisture, and15% cooling allowance. Winter is occupied steady state, not warm-up. These are regular-coach screening results. ADA construction and final outdoor-air requirements are not resolved.</p><p>The proposed enclosure adds approximately<strong>{mass['screen_increment_with_allowance_kg']:.0f}kg ({mass['screen_increment_with_allowance_kg']*2.2046226:.0f}lb) per regular coach</strong> over the incomplete C1 mass model, including replacement deck delta, floor finish, fixings reserve and10% quantity allowance. This is a material budget, not a complete weighed coach or an accepted suspension load.</p><p><strong>Eight mini-splits and the35kW generator remain candidates.</strong> Finalize glazing, floor support and underside fit, ADA clearances, ventilation flow and actual high/low-ambient HVAC inputs before selecting equipment. <a href="coach-envelope-engineering.html">Inspect assumptions, sensitivities and the mass breakdown →</a></p>'''
(D/'coach-envelope.html').write_text(page('Coach enclosure construction',body))

eng='''<p class="pf-eyebrow">CE1 · ENGINEERING RECORD · 26 OCTOBER2026</p><h1>Enclosure geometry, mass and heat loss.</h1><p class="ce-lead">A reproducible regular-coach screen tied to the proposed construction sections. Geometry comes from C1; the floor fit reservation also considers currentCI2/CI3 parts. Retained structural CAD is not regenerated.</p><nav class="ce-nav"><a href="coach-envelope.html">Construction drawings →</a><a href="#thermal">Thermal model</a><a href="#mass">Mass</a><a href="#sources">Sources</a><a href="assets/coach-envelope-ce1/analysis.json">Calculation dataJSON</a><a href="assets/coach-envelope-ce1/build.py">Reproducible source</a></nav><h2>Geometry method</h2><p>C1 roof outer radius177.503663″ and centerZ−56.889490″; subtract2″ hoop depth,1″ continuous insulation and.040″ lining. Headroom at transverseY is Zcenter+√(Rinside²−Y²)−32″. Finished side-wall planes are±(52.125−1−.040)″. No extra furring layer is hidden in these dimensions.</p><p>Side, end and curved/raised roof areas are extracted from retained skin solid masses divided by2680kg/m³×1/16″. Window area is the16 clear30×32″ openings. Door heat-transfer area uses two32×80″ apertures. Small sheet overlaps, trim and frame edges remain approximate; this is a surface takeoff proxy, not a certified envelope model.</p>'''
eng+=table(['Surface','Area m²'],[[k.replace('_',' '),f'{v:.3f}'] for k,v in areas.items()])
eng+='''<h2 id="thermal">Assembly heat-transfer screen</h2><p>Mineral-wool resistance is0.74m²K/W per inch. Parallel paths combine insulated bays and steel members; a separate2% /5% direct-bridge sensitivity covers local penetrations. Steel conductivity45W/mK and inside/outside surface films are engineering assumptions. Hollow steel is conservatively treated as solid through-depth. Floor and roof inside films use0.10m²K/W for all cases, deliberately avoiding a downward-flow film credit in cooling. A1D model cannot capture lateral heat spreading through steel, so these values remain screening inputs. The higher-loss scenario is not a proven upper bound.</p><p>Study frame fractions:20% walls/ends and12% roof. Higher-loss fractions:30% /20%, with higher windowU. Door frame fraction20%;1″ cavity insulation and no continuous layer. Floor study60% insulated, sensitivity50%;<strong>no thermal resistance credited to the honeycomb, rubber, exposed steel or tray</strong>. This keeps the unresolved floor conservative. These fractions are not all measured takeoffs.</p><p>The additional25% floor-insulated case represents substantial underside exclusion. Removing the full-width CI3 body-check intervals over both bogies leaves23.49% clear; those intervals are study windows, not measured swept envelopes. The25% case is a rounded sensitivity, not a cleared cassette layout.</p>'''
eng+=table(['Assembly','Study U','Higher-loss U','Units'],[[k.replace('_',' '),f'{v:.3f}',f'{thermal_sets["conservative"]["u_w_m2k"][k]:.3f}','W/m²K'] for k,v in thermal_sets['study']['u_w_m2k'].items()])
eng+=f'''<p>Study envelopeUA={thermal_sets['study']['ua_w_k']:.1f}W/K; higher-loss sensitivity={thermal_sets['conservative']['ua_w_k']:.1f}W/K. Raw side-wall insulationR16.8 and roofR12.6 exclude steel, films, openings and fastening. They are not whole-assembly ratings.</p><h3>Choose a sensitivity</h3><div class="ce-selector"><label>Envelope<select id="ce-envelope"><option value="study">CE1 study</option><option value="conservative">CE1 higher-loss assumptions + windows</option><option value="limited_floor">CE1 with only25% floor insulated</option><option value="old_u_same_geometry">EarlierU on updated geometry</option></select></label><label>Fresh-air study flow<select id="ce-flow"><option value="300">300CFM</option><option value="400">400CFM</option></select></label></div><div id="ce-results" aria-live="polite"></div><noscript><p>JavaScript is needed for the sensitivity selector. <a href="assets/coach-envelope-ce1/analysis.json">All results are available in the calculationJSON.</a></p></noscript>
<p>Each case uses37 thermal people at75W sensible/45W latent,420W internal equipment,0.03m³/s average door infiltration,1.2kg/m³ air density and1.006kJ/kgK specific heat. Cooling includes15% allowance. Solar applies500W/m² to all clear glazing atSHGC0.5 plus20K roof sol-air increment; this is a stress assumption, not orientation-specific exposure. Opaque-wall solar and thermal storage are omitted. Humidity stress adds0.006kg/kg across ventilation and infiltration. No recovery is credited.</p><p>Uwindow2.7 andSHGC0.5 remain unconfirmed; higher-lossU5.7 is shown separately. The earlier6mm polycarbonate alternative does not demonstrateU2.7. Actual glazing, framed opening size, safety performance and mass must be selected together. Comparison against earlierU uses the same updated areas to isolate construction effects; it will differ from archivedCL2’s rectangular model.</p><p>Winter results subtract occupied sensible gains and show steady-state demand only. Empty preheating, door cycling, moisture, solar storage and heat-pump defrost are not modeled. ThermalBTU/h cannot be used as generator electrical input. No four-coach total is asserted before ADA envelope coordination.</p>
<h2 id="mass">Increment over the incomplete C1 model</h2>'''
eng+=table(['Material / allowance','kg per regular coach'],[[k.replace('_',' '),f'{v:.1f}'] for k,v in mass.items()])
eng+='''<p>Insulation quantities use the stated cavity fractions; liners use outer-sheet area as a gross procurement proxy. Floor panels and finish use the actual retained panel area including its outboard shape; floor insulation/trays use the finished rectangle. The60kg reserve covers supports, inserts, closures, adhesive and seals;10% is then applied to calculated material quantities. These are visible allowances, not measured hardware. Existing exterior skins, frame, glazing and door-frame masses remain in C1. Deck delta replaces its generic100kg/m³ placeholder; do not add the complete new deck twice.</p><h2>Unresolved construction gates</h2><ul><li>Check honeycomb spans, concentrated loads, inserts, edge supports and finish/adhesive compatibility. A catalog panel is not an accepted floor design.</li><li>Confirm liner clip stiffness, vibration retention, panel span, edges, fasteners, metal isolation and bracket boxing. Wool is not a spacer or fastening substrate.</li><li>Integrate38.75″ regular benches in structuralCAD and review seat capacity; retain existing24″ aisle and feet.</li><li>Integrate the separateADA enclosure, door returns, fold-down seats, wheelchair paths and pin/hand access.</li><li>Resolve truck motion, brake routes and service removals before underside trays are placed. No obstruction is accepted in those envelopes.</li><li>Complete whole-coach mass/CG, suspension and braking review with the added enclosure budget.</li><li>Select glazing, test moisture/air sealing and qualify the assembled transport materials. Individual product fire ratings do not qualify the full vehicle.</li><li>Verify ventilation duty, actual fan curves/noise, roof curb/support details, mini-split performance and installed generator output.</li></ul><h2 id="sources">Primary product references</h2><p>Product references establish candidate material properties only. They do not approve rail/mobile installation.</p><ol class="ce-source"><li><a href="https://www.rockwool.com/siteassets/o2-rockwool/documentation/technical-data-sheets/commercial/rockboard-40-multi-purpose-board-insulation-techdata.pdf">ROCKWOOL Rockboard40 technical data, April2026</a>:64kg/m³; RSI0.74 per inch;4.3kPa at10% compression. E84 indices0/0 and noncombustibility classification are material data.</li><li><a href="https://www.rockwool.com/siteassets/o2-rockwool/documentation/technical-guides/commercial/board-insulation-attachment-guide.pdf">ROCKWOOL attachment guide</a>: mechanical retention principle. Building guidance does not provide the vehicle fastener schedule.</li><li><a href="https://www.rockwool.com/siteassets/o2-rockwool/documentation/technical-bulletins/commercial/bending-stone-wool-insulation-for-curved-designs.pdf">ROCKWOOL curved insulation guidance</a>: use staggered layers and retained joints; confirm the actual thin-board roof mock-up.</li><li><a href="https://plascore.com/composite-panels/base-panels/">Plascore standard base panels</a>:AA3.6-80,0.020″ aluminum faces, aluminum honeycomb and epoxy;3/4″ panel4.6kg/m². Supplied open edges require closeouts. Coupon properties are not allowable floor spans.</li><li><a href="https://www.altro.com/getmedia/c848bb1b-08be-49ee-973e-298f0d5e7875/Altro-Technical-Data-Sheet-Transflor-Motus.pdf?ext=.pdf">AltroTransflorMotus technical data</a>:2.5mm,4.17kg/m²; transport fire-test results apply to the product and stated testing, not the entire assembled floor.</li><li><a href="https://www.almexa.com.mx/en/alloys/5052-aluminum/">Almexa5052 aluminum data</a>: density2680kg/m³ used for liner/tray mass.</li></ol><p class="ce-small">Source and result records are preserved withCE1. C1 /C2.1 /CI2 /CI3 remain the underlying structural work. CL3 cabinet documents are retained as superseded history.</p><script type="module" src="coach-envelope.js"></script>'''
eng=eng.replace('<h2 id="mass">','<p><a href="assets/coach-envelope-ce1/floor-projection.json">Static floor projection, source hashes and limits (JSON)</a> · <a href="assets/coach-envelope-ce1/floor_projection.py">Projection source</a></p><h2 id="mass">')
(D/'coach-envelope-engineering.html').write_text(page('Coach enclosure engineering',eng))
(D/'coach-envelope.js').write_text('''const envelope=document.querySelector('#ce-envelope'),flow=document.querySelector('#ce-flow'),out=document.querySelector('#ce-results');
try{const response=await fetch('assets/coach-envelope-ce1/analysis.json');if(!response.ok)throw Error('Calculation data unavailable');const data=await response.json();function render(){const cases=data.cases.filter(c=>c.envelope===envelope.value&&c.cfm===Number(flow.value));out.innerHTML='<div class="ce-table"><table><thead><tr><th>Condition</th><th>Delivered kW</th><th>BTU/h</th><th>Ventilation sensible kW</th></tr></thead><tbody>'+cases.map(c=>`<tr><td>${c.condition}</td><td>${c.kw.toFixed(2)}</td><td>${Math.round(c.btuh).toLocaleString()}</td><td>${c.parts_kw.ventilation.toFixed(2)}</td></tr>`).join('')+'</tbody></table></div>';}envelope.addEventListener('change',render);flow.addEventListener('change',render);render();}catch(e){out.textContent='Calculation data could not load. Use the calculation JSON link above.';}
''')

# Check consequential accounting, geometry and sensitivity invariants.
assert math.isclose(geometry['finished_width_in'],102.17,abs_tol=1e-9)
assert math.isclose(geometry['floor_panel_top_z_in']+3.25/25.4,32,abs_tol=1e-8)
assert head(0)>head(12)>geometry['local_eave_headroom_in']
assert bench_y<wall_y and geometry['aisle_width_in']==24
for label,*_ in conditions:
 assert case(label,cfm=400)['kw']>case(label,cfm=300)['kw']
 assert case(label,'conservative')['kw']>case(label,'study')['kw']
for c in cases:
 assert math.isfinite(c['kw']) and c['kw']>=0
data['verification']=dict(finite_cases=len(cases),floor_datum_retained=True,aisle_retained=True,
 airflow_and_envelope_sensitivities_monotonic=True,source_model_changed=False,whole_coach_clearance_accepted=False)
(OUT/'analysis.json').write_text(json.dumps(data,indent=2)+'\n');(HERE/'analysis.json').write_text(json.dumps(data,indent=2)+'\n')
(OUT/'build.py').write_bytes(Path(__file__).read_bytes())

# Current navigation supersedes cabinet direction without erasing historical work.
banner='''<aside data-ce1-note style="margin:1.2rem 0;padding:1rem 1.2rem;background:#e8eee8;border-left:4px solid #347462"><strong>CE1 · Insulated coach enclosure.</strong> Finished wall/roof/floor sections, headroom, bench fit and assembly heat-loss screening. Current ventilation direction: compact powered roof intake/exhaust; CL3 cabinet is superseded. Eight mini-splits, airflow and35kW remain provisional. <a href="coach-envelope.html">Current construction proposal →</a></aside>'''
targets=['index.html','coaches.html','engineering-index.html','coach-regular.html','coach-accessible.html','coach-c1.html','coach-c21.html','coach-climate.html','coach-climate-engineering.html','coach-ventilation.html','coach-ventilation-engineering.html','coach-ventilation-system.html','coach-ventilation-system-engineering.html','tender-lt45.html','tender-lt45-engineering.html']
for name in targets:
 p=D/name
 if not p.exists():continue
 t=p.read_text();t=re.sub(r'<aside data-ce1-note\b.*?</aside>','',t,flags=re.S)
 t=re.sub(r'<aside data-cl3-note\b.*?</aside>','',t,flags=re.S)
 t=re.sub(r'(<main\b[^>]*>)',lambda m:m.group(1)+banner,t,count=1)
 p.write_text(t)
p=D/'assets/site-organization/current-selection.json';j=json.loads(p.read_text())
j.update(coachEnvelopePage='coach-envelope.html',coachEnvelopeEngineeringPage='coach-envelope-engineering.html',
 coachEnvelopeStatus='CE1 proposed wall/roof/floor construction and regular-coach finished-envelope screen. Bench narrowing and ADA integration pending; floor support, underside motion, glazing and whole-vehicle mass acceptance open.',
 coachVentilationPage='coach-envelope.html#climate',coachVentilationEngineeringPage='coach-envelope-engineering.html#thermal',
 coachVentilationStatus='Compact powered roof intake/exhaust direction with mini-splits. CL3 rear heat-recovery cabinet superseded for fit. No recovery credited;300/400CFM study only; fans, eight mini-splits and35kW unconfirmed.')
if 'coach-envelope-ce1' not in j['currentDrawingPackages']:j['currentDrawingPackages'].insert(0,'coach-envelope-ce1')
p.write_text(json.dumps(j,indent=2)+'\n')
p=D/'assets/site-organization/current-drawing-catalog.json';j=json.loads(p.read_text());j['packages']=[x for x in j['packages'] if x['id']!='coach-envelope-ce1']
j['packages'].insert(0,dict(id='coach-envelope-ce1',title='Coach enclosure construction · CE1',engineering='coach-envelope-engineering.html',fabricationPage='coach-envelope.html',note='Proposed finished sections. Regular bench revision, ADA integration and engineering acceptance remain open; not for construction.',sheets=[dict(id=n,title=t,image='assets/coach-envelope-ce1/'+n+'.svg',original='assets/coach-envelope-ce1/'+n+'.svg',kind='Dimensioned construction proposal') for n,t in [('CE1-A01','Finished coach section'),('CE1-D01','Wall and roof construction'),('CE1-D02','Floor cassette and hardpoints')]]))
p.write_text(json.dumps(j,indent=2)+'\n')
print(json.dumps(dict(geometry=geometry,ua={k:v['ua_w_k'] for k,v in thermal_sets.items()},mass_increment_kg=mass['screen_increment_with_allowance_kg'],checks=data['verification']),indent=2))

# Typography pass on this issue's human-facing output; never alter URLs/attributes.
from html.parser import HTMLParser
def prose_spacing(t):
 for old,new in [('Rockboard40','Rockboard 40'),('PlascoreAA3.6-80','Plascore AA3.6-80'),('AltroTransflorMotus','Altro Transflor Motus'),('Almexa5052','Almexa 5052'),('ROCKWOOL Rockboard40','ROCKWOOL Rockboard 40'),('earlierCL3','earlier CL3'),('currentCI2','current CI2'),('the16','the 16'),('eachinch','each inch'),('the1″','the 1″'),('CE1with','CE1 with'),('A1D','A 1D'),('EarlierU','Earlier U'),('opaqueU','opaque U'),('A0.','A 0.'),('Retained1','Retained 1'),('continuous1','continuous 1'),('actual24','actual 24'),('″5052','″ 5052'),('check:36','check: 36'),('route,78','route, 78'),('•300','• 300'),('study60','study 60'),('fractions:20','fractions: 20'),('fractions:30','fractions: 30'),('inch.','inch.'),('windowU','window U'),('higher-lossU','higher-loss U'),('Study envelopeUA','Study envelope UA'),('insulationR','insulation R'),('roofR','roof R'),('atSHGC','at SHGC'),('dataJSON','data JSON'),('calculationJSON','calculation JSON'),('theADA','the ADA'),('caseonly','case only')]:t=t.replace(old,new)
 t=re.sub(r'\b(the|a|an|its|only|above|below|adds|Adds|use|Use|and|per|all|with|leaves|is|at|from|to|by|of|minus|plus|over|about|uses|fraction|fractions|study|sensitivity|remaining|retain|existing|current|proposed|width|length|height|area|mass|than|intervals|inch|floor|panel|budget|incorporates|includes|subtract|Subtract|subtracts|adds|Adding|applies|points|stated|geometry|days|of|total|window|door|roof|liner|wall|steel|wool|basis|during|across|for|over|under|curve|doorway|cabin|after|within)(?=\d|\.\d)',r'\1 ',t)
 t=re.sub(r'(\d)(?=(?:CFM|BTU/h|kW|kg|mm|m²|m³|lb|W/m|W/K|W sensible|W latent|W internal|W cabin|W sensible|W equipment|kg/m|kPa|kJ))',r'\1 ',t)
 t=re.sub(r'(″)(?=[A-Za-z])',r'\1 ',t)
 t=re.sub(r'(\d)(?=(?:people|total|per|through|inches|inch|times|percent|regular|internal|clear|cavity|continuous|cabin))',r'\1 ',t)
 t=re.sub(r'([a-z]{2,})(?=\d)',r'\1 ',t)
 t=re.sub(r'(OCTOBER)(?=\d)',r'\1 ',t)
 t=t.replace('structuralCAD','structural CAD').replace('separateADA','separate ADA').replace('withCE1','with CE1').replace('andSHGC','and SHGC').replace('ThermalBTU','Thermal BTU').replace('archivedCL2','archived CL2').replace('RSI0.74','RSI 0.74')
 return t
for target in [D/'coach-envelope.html',D/'coach-envelope-engineering.html',*OUT.glob('*.svg')]:
 raw=target.read_text();raw=re.sub(r'(?<=>)[^<]+(?=<)',lambda m:prose_spacing(m.group()),raw);target.write_text(raw)
(OUT/'build.py').write_bytes(Path(__file__).read_bytes())

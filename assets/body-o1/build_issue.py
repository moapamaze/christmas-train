"""PF-3O1-R0: audit preserved geometry, not a new fabrication release.
Run from any directory. All outputs stay in this Site repository.
"""
from pathlib import Path
import hashlib, html, json, math, re, zipfile
P=Path(__file__).resolve().parent; D=P.parent.parent; E=html.escape
def save(name,data):
    (P/name).write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
manifest=[]
def recover(archive,member,name):
    p=D/'assets/files'/archive
    raw=zipfile.ZipFile(p).read(member)
    (P/name).write_bytes(raw)
    manifest.append(dict(archive='assets/files/'+archive,archive_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),member=member,preserved_as=name,member_sha256=hashlib.sha256(raw).hexdigest()))
    return json.loads(raw)
G=recover('Stage2_Technical_CAD_Review_R0.zip','Stage2_Geometry_R0.json','inherited-stage2-geometry.json')
I=recover('Christmas_Train_Phase3J_Technical_Source_R0.zip','source/body_i.json','inherited-body-I1.json')
H=recover('Christmas_Train_Phase3H_Technical_Source_R0.zip','phase3h/research/body_h_inputs.json','inherited-body-H-inputs.json')
save('source-manifest.json',manifest)
S=I['details']['seat']; byid={x['id']:x for x in S['components']}
sole=byid['I-SH1-SOLE'];cap=byid['I-SH1-CAP'];opening=S['panel_opening_in']; mm=25.4
length=lambda p,a:p['bounds_in'][a][1]-p['bounds_in'][a][0]
overlap={a:(length(sole,a)-opening['size_xy'][i])/2 for i,a in enumerate('xy')}
clearance={a:(opening['size_xy'][i]-length(cap,a))/2 for i,a in enumerate('xy')}
feet=I['seat_feet']; panels=[]
xb=[-3,45,93,141,189,237,285,309];yb=[-55,-34,34,55]
for n,(a,b) in enumerate(zip(xb,xb[1:]),1):
    for letter,(c,d) in zip('LCR',zip(yb,yb[1:])):
        bounds=[a+.0625,b-.0625,c+.0625,d-.0625]
        contained=[f['id'] for f in feet if bounds[0]<f['center_in'][0]<bounds[1] and bounds[2]<f['center_in'][1]<bounds[3]]
        panels.append(dict(id=f'HP{n:02}{letter}',bounds_xy_in=bounds,seat_opening_count=len(contained),feet=contained))
assert len(feet)==64 and sum(p['seat_opening_count'] for p in panels)==64
assert all(p['seat_opening_count']==6 for p in panels if p['id'] in ['HP02C','HP03C','HP04C','HP05C','HP06C'])
assert sole['bounds_in']['z'][0]==32 and overlap=={'x':.75,'y':.125} and clearance=={'x':.125,'y':.125}
# Analyst probes only: separate panel and supporting-steel temperatures.
thermal=[]
for tp,ts in [(-40,-40),(20,20),(60,60),(60,30),(30,60)]:
    ep=23e-6*tp;es=12e-6*ts
    for kind,li,lj,g0 in [('equal longitudinal seam',47.875,47.875,.125),('last longitudinal seam',47.875,23.875,.125),('central/wing seam',67.875,20.875,.125)]:
        gap=g0*(1+es)-(ep-es)*(li+lj)/2
        thermal.append(dict(case=kind,panel_deltaT_K=tp,steel_deltaT_K=ts,restraint='one center locator per panel, free sliding elsewhere; NOT existing proven restraint',gap_mm=gap*mm,closure_mm=(g0-gap)*mm))
opening_moves=[]
for p in panels:
    x0,x1,y0,y1=p['bounds_xy_in']; qx=(x0+x1)/2;qy=(y0+y1)/2
    for footid in p['feet']:
        f=next(f for f in feet if f['id']==footid);x,y,_=f['center_in']
        dx=abs((23-12)*1e-6*60*(x-qx));dy=abs((23-12)*1e-6*60*(y-qy))
        # Required clearance at opening edge also includes opening vs cap size strain.
        rx=.125+23e-6*60*(2.75/2)-12e-6*60*(2.5/2)-dx
        ry=.125+23e-6*60*(6.25/2)-12e-6*60*(6/2)-dy
        opening_moves.append(dict(foot=f['id'],panel=p['id'],assumed_panel_locator_xy_in=[qx,qy],relative_center_shift_mm=[dx*mm,dy*mm],minimum_side_clearance_before_tolerances_mm=[rx*mm,ry*mm]))
calc=dict(issue='PF-3O1-R0',date='2026-10-19',type='inherited geometry audit and explicitly trial thermal sensitivities',fabrication_release=False,
    measured_from_source=dict(soleplate_size_in=[length(sole,a) for a in 'xyz'],opening_size_in=opening['size_xy'],cap_size_in=[length(cap,a) for a in 'xyz'],sole_overlap_each_side_in=overlap,opening_to_cap_clearance_each_side_in=clearance,sole_underside_z_in=32,finished_floor_z_in=32,nominal_vertical_isolation_mm=0,spacer_nominal_mm=(32-cap['bounds_in']['z'][1])*mm),
    cabin=dict(clear_length_in=G['clear_length_in'],clear_width_in=G['clear_width_in'],regular_guests=sum(x['seats'] for x in G['regular_seats']),accessible_fixed_guests=sum(x['seats'] for x in G['accessible_seats']),wheelchair_spaces=len(G['wheelchair_reserved_bays']),regular_pitch_in=32,seat_envelope_depth_in=20,between_envelope_gap_in=12,regular_aisle_in=24,accessible_aisle_y_in=[-12,24],accessible_enddoor_y_in=[-12,24],sideopening_x_in=[9,51],end_clear_in=31,straight_30ft_bench_fits=False),
    panels=panels,thermal_assumptions=dict(alpha_panel_per_K=23e-6,alpha_steel_per_K=12e-6,status='analyst sensitivity only; project material CTE and temperature envelopes unverified',assembly_temperature_C=None,actual_locator_topology=None,accepted_minimum_gap_mm=None),thermal_cases=thermal,opening_motion_cases=opening_moves,
    global_single_anchor_half_length_probe_mm=(23-12)*1e-6*60*312/2*mm,
    tolerance_equations=dict(seam='g_min = g_thermal - adverse anchor-position error - half sum of finished-length errors - skew/deformation/seal/migration allowances',opening='c_min,x = c0,x + epsilon_panel*opening_halfwidth - epsilon_steel*cap_halfwidth - abs(relative opening-center shift) - adverse dimensional/position/angular/deformation allowances',vertical='c_min,z = z_sole_under,min - z_finished_floor,max - adverse relative loaded deflection; require engineer-defined positive minimum',general_thermal='g = g0 + u_steel(qj)-u_steel(qi) + epsilon_j*(aj-qj) - epsilon_i*(bi-qi)',center_located='g = g0*(1+epsilon_steel) - (epsilon_panel-epsilon_steel)*(Li+Lj)/2'),
    limitations=['No locator, sliding fastener, adhesive, insert, edge closeout or actual tolerance selected.','No uniform-CTE claim for the composite panel. No statistical tolerance credit.','Nominal contact is not a positive-volume CAD clash; a bypass still needs positive clearance through tolerances and loads.','Six openings on many central panels make free-center-anchored behavior a sensitivity, not a model of the actual finished floor.'])
save('audit-and-calculations.json',calc)
sources=[
 dict(id='O-S01',authority='Plascore',url='https://plascore.com/composite-panels/base-panels/',checked='2026-10-19',publication='not stated',finding='AA3.6-80 base panel is an aluminum sandwich; listed values are typical. Open supplied edges need application-specific finishing. Project CTE, inserts and tolerances are not supplied here.'),
 dict(id='O-S02',authority='Sika',url='https://industry.sika.com/dam/dms/us01/o/sikaflex-252.pdf',checked='2026-10-19',publication='2025-04 version04.01',finding='Requires compatibility and adhesion tests on actual substrates and conditions. Elongation at break is not an allowable cyclic floor-joint shear movement.'),
 dict(id='O-S03',authority='Sika',url='https://usa.sika.com/dam/dms/us01/0/General-Guideline-Bonding-Sealing-1-Component-Sikaflex-US-12-25.pdf',checked='2026-10-19',publication='2025-03 version6.1',finding='Bond geometry must accommodate movement and cure; generic guidance does not approve the inherited3mm stack.'),
 dict(id='O-S04',authority='Gerflor',url='https://cdn.gerflor.com/media/2/37754/installation%20guide%20tarabus%20-%20eng.pdf',checked='2026-10-19',publication='not established',finding='Subfloor and finish preparation guidance is not permission to bridge a moving structural-panel seam. Specific compatible joint treatment remains necessary.'),
 dict(id='O-S05',authority='US Access Board',url='https://www.access-board.gov/ada/chapter/ch10/',checked='2026-10-19',publication='2010 Standards text; checked current official page',finding='Section1002 includes amusement-ride vehicle/boarding provisions. Its side-entry advisory example is not a universal wheelchair-bay rule. Authority must determine amusement versus transportation applicability.'),
 dict(id='O-S06',authority='US Access Board',url='https://www.access-board.gov/ada/guides/chapter-10-amusement-rides/',checked='2026-10-19',publication='not stated',finding='Distinguishes amusement rides from primarily transportation systems. This report makes no jurisdiction determination.')]
save('sources.json',sources)
gates=[
 ('O-G01','Seat-to-floor load bypass','Structural engineer + seat/panel detail designer','Revise coupled sole/cap/spacer/opening/seal stack. Specify positive clearance under tolerances, seat loads and floor deflection; retain seat elevation or explicitly revise it. Do not add an arbitrary shim.','64 feet in regular coach; accessible layout needs its own schedule.'),
 ('O-G02','Panel movement and retention','Panel/finish/adhesive manufacturers + vehicle structural/materials engineer','Directional CTE, thermal envelopes, actual locator/sliding/adhesive topology, insert/closeout geometry, fastener grip/preload, seam/penetration seal movement and qualification tests.','No slot, bolt length, gap tolerance or adhesive strain selected.'),
 ('O-G03','Body structure','Vehicle structural engineer','Wall/roof/sill/door-frame physical sections, material joints, passenger and HVAC loads, fatigue, glazing retention and emergency egress.','3in wall and old roof blocks are reservations, not buildable construction.'),
 ('O-G04','Accessible boarding and circulation','Responsible accessibility authority + vehicle/boarding designers','Applicable vehicle regime; actual loaded floor range; lifts/ramps, hardware protrusions, swept wheelchair maneuvering, companion arrangement, securement and evacuation.','End doors already match the+6in aisle centerline; no fictitious alignment change needed.'),
 ('O-G05','Floor datum across suspension states','Vehicle dynamics/structure + station designers','Accepted empty/loaded/max-bump floor/threshold elevations and roll/twist envelopes coordinated to truck and station.','Inherited32in has no accepted load state; do not set platform elevation from it.')]
save('decisions-and-test-record.json',dict(issue=calc['issue'],review_issue_complete=True,phase3O_complete=False,approved_for_fabrication=False,retained=['J1a frame source','104x306in clear cabin as packaging study','Existing accessible door offset','All predecessor parts and revision history'],rejected=['Claim that zero-contact clearance completes a seat load bypass','Treating every panel as proven freely center-located','Using finish-edge gaps or adhesive break elongation as structural-joint allowances'],gates=[dict(id=a,interface=b,accountable=c,evidence=d,scope=e) for a,b,c,d,e in gates],prototype_sequence=['Resolve paper vertical stack and complete bolted/welded load path first.','Build one reviewed seat-hardpoint/panel-joint coupon with exact production materials, closeouts, coatings, adhesives and fasteners. Farm crew may assist assembly and record dimensions under specialist direction.','Measure as-built clearances, flatness, joint openings, assembly temperature, bolt/insert configuration and baseline displacement.','Engineer defines seat/floor proof and cyclic load cases, thermal/wet cycles and acceptance values before testing. Instrument both seat-to-frame and seat-to-floor transfer; do not infer isolation from a drawing.','Record hot/cold gaps, movement, panel/finish damage, moisture ingress, fastener retention and accessible service. Engineer dispositions results before release.'],acceptance_limits={'seat_to_floor_transfer':None,'minimum_vertical_clearance_mm':None,'minimum_seam_clearance_mm':None,'joint_cycle_count':None,'proof_load_N':None},next='3P.1 thermal/electrical source reconciliation. Resume custom floor/body detail after these actual interface choices; whole truck/drive remain held only where dependent.'))
# Drawing is a truthful section of the existing trial part, not new selected geometry.
out=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1240 960"><style>text{font:17px Arial;fill:#173344}.small{font-size:14px}.title{font-size:25px;font-weight:bold}.dim{stroke:#173344;stroke-width:1;fill:none}.steel{fill:#afbdc8;stroke:#173344;stroke-width:1.5}.floor{fill:#e4cd98;stroke:#735b32}.ghost{fill:none;stroke:#a1472a;stroke-width:2;stroke-dasharray:7 5}</style><rect width="1240" height="960" fill="#fff"/>']
def text(x,y,s,cl=''):out.append(f'<text x="{x}" y="{y}" class="{cl}">{E(s)}</text>')
def rect(x,y,w,h,cl):out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="{cl}"/>')
text(35,40,'O1-A01 · Existing I-SH1 seat/floor interface audit','title');text(35,68,'19 Oct 2026 · inches unless noted · inherited trial geometry · NOT FOR FABRICATION')
text(35,105,'PLAN · soleplate shown translucent / floor opening dashed')
scale=50; px=lambda x:250+(x-97)*scale;py=lambda y:300-(y-20)*scale
rect(px(94.875),py(23.25),4.25*scale,6.5*scale,'steel')
rect(px(95.625),py(23.125),2.75*scale,6.25*scale,'ghost')
rect(px(95.75),py(23),2.5*scale,6*scale,'dim')
for y in [18,22]:out.append(f'<circle cx="{px(97)}" cy="{py(y)}" r="{.5625*scale/2}" fill="white" stroke="#173344"/>')
text(35,500,'01 Sole: 4.25 × 6.50 × 0.25; two Ø0.5625 study holes')
text(35,526,'02 Cap: 2.50 × 6.00 × 0.375; matching study holes')
text(35,552,'Opening 2.75 × 6.25; x/y overlap each side = 0.75 / 0.125')
text(35,578,'Cap-to-opening nominal clearance = 0.125 each side')
text(590,105,'SECTION A–A · x=97, looking along x; y/z true proportions')
yz=70; Y=lambda y:900+(y-20)*yz;Z=lambda z:370-(z-31)*yz
for lo,hi in [(15.7,16.875),(23.125,24.3)]:
 rect(Y(lo),Z(31.8720472441),(hi-lo)*yz,.75*yz,'floor')
 rect(Y(lo),Z(32),(hi-lo)*yz,(32-31.8720472441)*yz,'floor')
for p in S['components']:
 if p['shape']=='box':
  b=p['bounds_in'];rect(Y(b['y'][0]),Z(b['z'][1]),length(p,'y')*yz,length(p,'z')*yz,'steel')
  for h in p.get('holes',[]):
   yy=h['center_xy_in'][1];rr=h['diameter_in']/2
   rect(Y(yy-rr),Z(b['z'][1]),2*rr*yz,length(p,'z')*yz,'')
   out[-1]=out[-1].replace('class=""','fill="white" stroke="#173344"')
 else:
  y=p['center_xy_in'][1];a,b=p['z_bounds_in'];o=p['outer_diameter_in']/2;i=p['inner_diameter_in']/2
  for lo,hi in [(y-o,y-i),(y+i,y+o)]:rect(Y(lo),Z(b),(hi-lo)*yz,(b-a)*yz,'steel')
# HSS section with nominal walls; corner profile deliberately not invented.
b=S['reference_components'][0]['bounds_in'];rect(Y(19),Z(b['z'][1]),2*yz,3*yz,'steel');rect(Y(19+.1875),Z(b['z'][1]-.1875),(2-.375)*yz,(3-.375)*yz,'')
out[-1]=out[-1].replace('class=""','fill="white" stroke="#173344"')
out.append(f'<path d="M{Y(15.7)} {Z(32)} H{Y(24.3)}" stroke="#b13020" stroke-width="3"/>')
out.append(f'<path d="M{px(97)} 125 V475" stroke="#173344" stroke-dasharray="10 4 2 4"/>');text(px(97)+8,128,'A');text(px(97)+8,485,'A')
for yy,zz,label,tx,ty in [(23,32.125,'01',1140,250),(22.8,31.2,'02',1130,400),(22.5,31.68,'03',1140,345),(21.1,30,'04',1090,470),(20,28.3,'05',990,570)]:
 out.append(f'<path d="M{Y(yy)} {Z(zz)} L{tx-8} {ty-6}" class="dim"/>');text(tx,ty,label)
text(590,610,'Red: floor top and sole underside share z=32.000')
text(590,637,'No positive vertical isolation: nominal contact, not volume clash.')
text(590,664,'03 Spacers: OD1 / ID0.5625 × 15.775 mm nominal')
text(590,691,'04 Cheeks: 2.50 × 2.00 × 0.1875 (two)')
text(590,718,'05 Rail: HSS3 × 2 × 3/16 trial; corner fit unresolved')
text(35,763,'READER CHECK: actual plates, bores, spacers and mating planes are identifiable; bolts, locking, welds,')
text(35,790,'edge closeouts and seals are NOT fully defined. Nothing on this sheet authorizes making/installing the mount.')
text(35,828,'Required revision: resolve loaded vertical clearance, seat elevation, penetration/seal movement and full load path together.')
text(35,856,'Do not fix this by adding an arbitrary shim, rigidly filling seams, clamping skins, or assuming round holes permit sliding.')
text(35,900,'Source: preserved body_i.json / details.seat; all views derived from the same audited coordinates.','small')
text(35,926,'No new plate, hole, weld, material or fastener selection. HSS corner radius and hardware omitted openly.','small')
out.append('</svg>');(P/'O1-A01-seat-floor-audit.svg').write_text(''.join(out))
# Entire cabin plans generated directly from recovered Stage2 seat coordinates.
out=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1240 1100"><style>text{font:17px Arial;fill:#173344}.title{font-size:25px;font-weight:bold}.small{font-size:14px}.box{fill:#edf3f4;stroke:#173344;stroke-width:2}.seat{fill:#a8c9cf;stroke:#173344}.bay{fill:#f6dfb2;stroke:#a06b27;stroke-dasharray:6 4}</style><rect width="1240" height="1100" fill="white"/>']
text(30,38,'O1-A02 · Retained cabin space audit — not body construction','title');text(30,67,'306 × 104 in clear study envelope; actual hardware, structure and egress still need coordinated detail')
for k,(seats,yc,title) in enumerate([(G['regular_seats'],300,'REGULAR · 32 guests / 16 two-adult benches'),(G['accessible_seats'],755,'ACCESSIBLE · 11 fixed guests + 2 wheelchair spaces')]):
 text(30,yc-190,title)
 sc=3.2;X=lambda x:75+x*sc;Yp=lambda y:yc-y*sc
 rect(X(0),Yp(52),306*sc,104*sc,'box')
 for n,s in enumerate(seats,1):
  rect(X(s['x']),Yp(s['y']+s['w']),s['l']*sc,s['w']*sc,'seat')
  text(X(s['x'])+3,Yp(s['y']+s['w']/2),str(n),'small')
 if k:
  for s in G['wheelchair_reserved_bays']:
   rect(X(s['x']),Yp(s['y']+s['w']),s['l']*sc,s['w']*sc,'bay')
  text(X(65),Yp(-32),'2 × 60 × 36 reserved bays','small')
  text(X(182),Yp(5),'36 aisle; y=-12..+24','small')
  for x in [0,306]:out.append(f'<path d="M{X(x)} {Yp(-12)} V{Yp(24)}" stroke="white" stroke-width="5"/>')
  for y in [-52,52]:out.append(f'<path d="M{X(9)} {Yp(y)} H{X(51)}" stroke="white" stroke-width="5"/>')
  out.append(f'<circle cx="{X(30)}" cy="{Yp(6)}" r="{30*sc}" fill="none" stroke="#a06b27" stroke-dasharray="7 4"/>')
  text(X(5),Yp(6),'Ø60 study','small')
  text(30,yc+198,'End doors:36 clear, centerline y=+6; already aligned. Both side openings x=9..51 (42 in).')
 else:
  for x in [0,306]:out.append(f'<path d="M{X(x)} {Yp(-16)} V{Yp(16)}" stroke="white" stroke-width="5"/>')
  text(X(100),Yp(0),'24 aisle · 32 pitch · 20 seat depth','small');text(30,yc+198,'31 in end lobbies; 20 in nominal bench width per adult. No verified knee, coat or evacuation clearance.')
text(30,1030,'Units in inches. Seats and bays are space envelopes, not detailed physical furniture or accessibility approval.')
text(30,1066,'Source: preserved Stage2_Geometry_R0.json. 32 in later floor datum remains unaccepted at any suspension load state.','small')
out.append('</svg>');(P/'O1-A02-cabin-audit.svg').write_text(''.join(out))
rows=''.join(f'<tr><td>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td><td>{E(d)}</td></tr>' for a,b,c,d,_ in gates)
src=''.join(f'<li><a href="{s["url"]}" target="_blank" rel="noopener">{E(s["id"]+" · "+s["authority"])}</a>. {E(s["finding"])} Checked19October2026; {E(s["publication"])}.</li>' for s in sources)
trows=''.join(f'<tr><td>{E(t["case"])}</td><td>{t["closure_mm"]:.4f}</td><td>{t["gap_mm"]:.4f}</td></tr>' for t in thermal if t['panel_deltaT_K']==60 and t['steel_deltaT_K']==60)
issue=f'''<!-- O1 ISSUE START --><section id="coachbody" class="panel" aria-labelledby="coachbody-title"><div class="section-heading"><p class="eyebrow">3O.1 · COMPLETED AUDIT ISSUE · 19 OCTOBER 2026</p><h1 id="coachbody-title">Preserve useful space. Correct the actual floor connection.</h1><p>This is a completed source/connection audit, <strong>not completed Phase3O or new fabrication drawings</strong>. The saved geometry reveals a real zero-clearance seat/floor conflict. No unsupported mount dimensions have been added.</p></div>
<article id="coachbody-floor" class="card build-notice"><h2>The saved seat soleplate can contact the floor</h2><p>The 4.25 × 6.50 × 0.25 in soleplate overlaps its 2.75 × 6.25 in floor opening by 0.75 in per x end and 0.125 in per y side. Its underside and the finished floor both lie at z=32.000 in: <strong>nominal vertical isolation is zero</strong>. This is plane contact, not a positive-volume CAD clash. Tolerances, bow and loaded deflection can put seat load into the panel or clamp its thermal movement. The previous “floor bypass” is therefore not a completed isolated connection.</p><p>The section below uses the actual preserved I1 plates, bores, hollow spacers and rail envelope, not a substitute brake-style diagram. It exposes the problem; it does not approve the inherited mount.</p><img src="assets/body-o1/O1-A01-seat-floor-audit.svg" alt="Plan and cutaway section of the actual inherited I-SH1 plate and spacer geometry showing zero seat-to-floor isolation" style="width:100%"><p><a href="assets/body-o1/O1-A01-seat-floor-audit.svg" target="_blank">Open full-size coordinate-derived section ↗</a> · <a href="#connections">Retained rotatable I1 connection study</a></p></article>
<article id="coachbody-space" class="card"><h2>What the current interior actually contains</h2><p>The retained clear study cabin is306 ×104in (25ft6in ×8ft8in), not a30ft-long seating compartment. Regular:32guests, sixteen40in two-adult benches,32in pitch,20in seat envelope depth,24in central aisle and31in end clear zones. The12in gap between consecutive seat envelopes is not a verified knee/coat or evacuation clearance.</p><p>Accessible:11fixed seats plus2reserved wheelchair spaces. The36in aisle and36in end doors already share the same+6in offset centerline. There is <strong>no door/aisle alignment defect to fix</strong>. Source side openings are42in wide at x=9..51in. Hardware, actual maneuvering, securement/companion arrangement and boarding/evacuation still need detailed coordination and an applicable-requirements determination.</p><img src="assets/body-o1/O1-A02-cabin-audit.svg" alt="Regular and accessible coordinate-derived cabin plans with seats numbered, retained aisles and wheelchair bays" style="width:100%"><p>These are audited space envelopes, not physical seat/body fabrication geometry. The3in wall, roof envelope and old28in floor models do not define the new load-bearing body. The later32in floor datum has no accepted empty/loaded suspension state. No station threshold may be fixed from it.</p></article>
<article id="coachbody-movement" class="card"><h2>Twenty-one panels need an actual movement and retention scheme</h2><p>Five central panels each contain six frame-referenced seat penetrations. A floor panel is not proven to expand freely about one center just because its seams have gaps. The inherited round-hole clip/insert, finish/adhesive continuity and overlapping soleplates can introduce restraints.</p><p>For a single center locator per freely sliding panel, <code>g = g₀(1+εsteel) − (εpanel−εsteel)(Lᵢ+Lⱼ)/2</code>. The full record also covers arbitrary anchor locations and opening-to-cap motion. Multiple rigid anchors require thermal-stress analysis, not just free-expansion arithmetic.</p><p>Illustration only:αpanel=23 andαsteel=12µm/m/K, both+60K. These are analyst inputs, not measured composite properties or selected temperature limits. Starting seam3.175mm:</p><div class="table-wrap"><table><thead><tr><th>Center-located sensitivity</th><th>Closure mm</th><th>Nominal remaining mm</th></tr></thead><tbody>{trows}</tbody></table></div><p>No tolerance or seal/creep/skew allowance has yet been deducted. A different global single-anchor half-length model gives2.6152mm mismatch at156in, greater than the inherited1.5875mm perimeter inset. These two models describe different restraints; do not combine them or conclude that a particular gap is adequate. All64penetrations are separately evaluated in the editable record under the center-locator probe only.</p><p>A structural panel seam is not a vinyl finish-edge gap. A manufacturer’s tensile elongation at break is not a cyclic bond-shear allowance. New seam treatment, inserts, closeouts, fastener preload, coatings, moisture isolation and floor retention must work as one system.</p></article>
<article id="coachbody-release" class="card"><h2>Precise correction and release work</h2><div class="table-wrap"><table><thead><tr><th>Gate</th><th>Interface</th><th>Accountable specialist</th><th>Required evidence / work</th></tr></thead><tbody>{rows}</tbody></table></div><p><strong>Prototype route:</strong> resolve the vertical stack/load path first; then build a reviewed seat-hardpoint/panel-joint coupon with production materials and closeouts. Record dimensions, temperature, floor/seat displacements and hot/cold seam/penetration clearances. Engineer-set proof, cyclic, moisture, thermal and retention acceptance limits are still null. Farm crew can assist the reviewed mockup and record measurements; structural, materials and accessibility specialists own the safety-critical design and acceptance.</p><h3>Dated primary evidence</h3><ol>{src}</ol><div class="actions"><a class="button" href="assets/body-o1/audit-and-calculations.json">Geometry and64penetration /15seam-case calculations</a><a class="button" href="assets/body-o1/build_issue.py">Editable audit / drawing generator</a><a class="button" href="assets/body-o1/source-manifest.json">Preserved source paths and hashes</a><a class="button" href="assets/body-o1/decisions-and-test-record.json">Correction, responsibilities and test record</a></div><p>Reader check: parts and current mating/contact planes can be identified. Builders still cannot make a released seat mount from this audit: hardware, weld/prying/fatigue design, floor closeouts and positive isolation are unresolved. Arithmetic and legible SVG are not fabrication acceptance.</p><p><strong>Next:</strong>3P.1 reconciles recovered thermal and electrical budgets, including removal of obsolete hydraulic-brake pump assumptions from the current air-braked configuration. 3L/3M/3N/3O remain in development; no dependent mount or passenger-operation release is implied.</p></article></section><!-- O1 ISSUE END -->'''
index=D/'index.html';s=index.read_text()
if '<!-- O1 ISSUE START -->' in s:s=re.sub(r'<!-- O1 ISSUE START -->.*?<!-- O1 ISSUE END -->',lambda _:issue,s,flags=re.S)
else:s=s.replace('<section id="propulsion"',issue+'\n<section id="propulsion"',1)
assert '<!-- O1 ISSUE START -->' in s
if 'data-tab="coachbody"' not in s:s=s.replace('<a href="#propulsion" data-tab="propulsion">','<a href="#coachbody" data-tab="coachbody"><span>3O.1</span>Coach interior / floor audit</a>\n<a href="#propulsion" data-tab="propulsion">',1)
index.write_text(s)
app=D/'app.js';s=app.read_text();s=s.replace("const tab = rawTab.startsWith('propulsion-')", "const tab = rawTab.startsWith('coachbody-') ? 'coachbody' : rawTab.startsWith('propulsion-')");s=s.replace("if(rawTab.startsWith('propulsion-')", "if(rawTab.startsWith('coachbody-')||rawTab.startsWith('propulsion-')");app.write_text(s)
if "coachbody:'" not in s:
 s=s.replace('const sections = {',"const sections = {coachbody:'Coach space and floor connection audit',",1);app.write_text(s)
statep=D/'assets/engineering-program-state.json';raw=statep.read_text();state=json.loads(raw)
if not (P/'predecessor-program-R11.json').exists():(P/'predecessor-program-R11.json').write_text(raw)
state.update(revision='PROGRAM-R12',latest_issue_url='https://pulsipher-train-review.fixinitcheap.chatgpt.site/#coachbody-floor',execution_note='3O.1 source/space/floor-contact audit complete; no full3O or fabrication completion. Found zero-clearance sole/floor contact and unclosed multi-penetration movement restraint. Continue independent3P thermal/electrical reconciliation while exact structural/panel/truck inputs remain held.')
state['current_independent_issue']={'stage':'3O.1','issue':'PF-3O1-R0','path':'assets/body-o1','review_issue_complete':True,'complete_body_phase':False,'approved_for_fabrication':False,'completed_scope':['Recovered body/interior coordinate and source audit','Actual seat sole/cap/floor contact finding with matched plan/section','21panel/64penetration and15thermal seam sensitivities','Exact correction and prototype evidence responsibilities']}
o=next(x for x in state['stage_map'] if x['id']=='3O');o.update(status='source_space_and_floor_connection_audit_complete_physical_body_open',desktop_issue_complete=False);o.setdefault('evidence',[])
if 'assets/body-o1' not in o['evidence']:o['evidence'].append('assets/body-o1')
state['next_worker'].update(stage='3P',substage='3P.1',start_from='assets/body-o1/decisions-and-test-record.json; original3F systems_f_inputs/calculations and frozen thermal sources',first_deliverable='Reconcile occupancy/envelope/ventilation/auxiliary heat and actual electrical boundaries. Remove obsolete hydraulic-brake load allocation from current air-braked schedule without inventing compressor demand.',independent_follow_on='Continue supported HVAC/electrical physical interfaces and remaining subsystems. Resume body mount revision only with real closeout/insert, tolerance, thermal and structural evidence; no arbitrary shim or slotted-hole selection.')
state['publication_state'].update(prepared_stage='3O.1 / body-interior and floor connection audit',prepared_route='#coachbody-floor',status='prepared_for_publication',native_deployment_verified_in_this_file=False)
state['continuation_checkpoint']={'completed':'3O.1 audit, not full3O. No new fabricated geometry released.','finding':'I-SH1 sole has zero nominal vertical isolation and overlaps floor opening; central floor panels have multiple steel-referenced penetrations.','next':'3P.1 current thermal/electrical reconciliation; inspect original3F before reuse.','outstanding_evidence':'O-G01–05 plus existing L/M/N gates; exact controlled supplier geometry and engineer/test acceptance.','preserve':'All predecessor source/parts and actual accessible door offset. Site-only technical publication; no budget/outreach.'}
save('change-record.json',dict(issue=calc['issue'],source_commit='bfab04b91917ce1bb6c4a0f8d2554d02961b23f9',new_fabrication_geometry=False,geometry_findings=calc['measured_from_source'],prior_versions_preserved=True))
statep.write_text(json.dumps(state,indent=2)+'\n')
print('Built3O.1 audit, two coordinate-derived audit sheets and PROGRAM-R12. Publication pending.')

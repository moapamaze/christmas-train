"""CL4: bounded equipment and above-door fit review. No coach CAD is altered.
Run after CE1 when rebuilding the current status/navigation overlays.
"""
from pathlib import Path
import json, html, re, shutil

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D = ROOT / 'dist'
OUT = D / 'assets/coach-climate-cl4'
OUT.mkdir(parents=True, exist_ok=True)
audit = json.loads((HERE / 'fit-audit.json').read_text())
g = audit['regular']
w = g['proposed_finished_hood_width_in']
h = g['height_above_clear_door_in']
depth = g['proposed_pocket_depth_in']
mm = 1 / 25.4
sources = {
 'ch_product': 'https://cooperandhunter.us/product/ch-rsh60lcfc',
 'ch_submittal': 'https://media.cooperandhunter.us/4292/CH-R60LCU-230VO-%2B-CH-RSH60LCFC.pdf',
 'ch_leaflet': 'https://media.cooperandhunter.us/4291/Floor-Ceiling-Leaflet-2025.pdf',
 'ch_manual': 'https://media.cooperandhunter.us/4289/Installation-manual-LCFC.pdf',
 'ch_performance': 'https://media.cooperandhunter.us/6626/FLOOR_CEILING_Coil_Performance_R454B_36-60K_Regular_05_COOLING-60K-RH__CH-RSH60LCFC.pdf',
 'bosch_submittal': 'https://www.bosch-homecomfort.com/us/media/country_pool/documents/engineering-submittal-sheets/ductless-minisplits/36k_single_zone_light-commercial_wall_ess_en_01.2026.pdf',
 'bosch_manual': 'https://www.bosch-homecomfort.com/us/media/country_pool/documents/installation-manuals/ductless-minisplits/climate5000_gen4_wall_ductless_single-split_iom_en_04.2026.pdf',
 'gree_submittal': 'https://www.greecomfort.com/assets/our-products/livo-r32/documents/livo-r32-submittal-36mbh-230v-a.pdf',
 'gree_manual': 'https://www.greecomfort.com/assets/our-products/livo-r32/documents/livo-r32-installation-owner-s-manual-indoor-a.pdf'
}
data = {
 'revision': 'CL4', 'date_local': '2026-10-25', 'timezone': 'America/Los_Angeles',
 'status': 'NO ACCEPTED MODEL; EXISTING ABOVE-DOOR INSTALLATION NOT VERIFIED',
 'direction': 'Four single-zone systems, one per coach, preferred for investigation; eight is not an accepted requirement.',
 'generator_target_kw': 35, 'generator_confirmed': False,
 'regular_geometry': {'finished_width_in': w, 'above_door_height_in': h, 'pocket_depth_in': depth,
   'ceiling_aff_in': 98.96, 'door_clear_height_in': 80, 'header_top_aff_in': 82},
 'cooper_hunter': {'indoor': 'CH-RSH60LCFC', 'outdoor': 'CH-R60LCU-230VO',
   'width_in': 64.96, 'depth_in': 26.57, 'height_in': 9.25, 'seer2': 19.5, 'eer2': 9.5,
   'rated_cooling_btuh': 54000, 'rated_cooling_input_w': 5625,
   'clearance_each_side_in': 35*mm, 'clearance_top_in': 35*mm, 'clearance_front_in': 1000*mm,
   'body_width_deficit_in': 64.96-w, 'body_depth_deficit_in': 26.57-depth,
   'required_finished_width_in': 64.96+70*mm,
   'minimum_structural_hood_width_in': 64.96+70*mm+6.08,
   'ceiling_fit_only_bottom_aff_in': 98.96-35*mm-9.25,
   'capacity_110f_btuh': 41200, 'capacity_table_return_db_f': 80,
   'capacity_table_return_wb_f': 67, 'capacity_table_airflow_cfm': 1365,
   'study_110f_sun_btuh': 55866,
   'result': 'REJECTED for existing location and provisional hot-sun capacity. No mobile qualification found.'},
 'bosch': {'indoor': 'BMS500-AAU036-1AHWXD', 'outdoor': 'BMS500-AAS036-1CSXRD',
   'width_in': 44.88, 'height_in': 14.61, 'depth_in': 11.22, 'seer2': 19,
   'rated_cooling_btuh': 36000, 'side_clearance_each_in': 4.75, 'usual_top_clearance_in': 5.9,
   'required_width_in': 44.88+2*4.75, 'required_above_door_height_in': 14.61+5.9,
   'figure_5_minimum_bottom_aff_in': 90.55,
   'result': 'REJECTED. Width fails; normal top clearance fails; manual excludes doorway and vibrating locations. Reduced-top provision does not resolve these.'},
 'gree': {'indoor': 'LIV36HP230V1R32AH', 'outdoor': 'LIV36HP230V1R32AO',
   'width_in': 42+7/16, 'height_in': 13+7/64, 'depth_in': 9+11/16,
   'rated_cooling_btuh': 33600, 'seer2': 21,
   'result': 'REJECTED. Installation manual prohibits moving bases and conflicts with submittal clearances.'},
 'ada': 'C4 has offset 78in end doors and no modeled C1 raised hood. Requires separate layout.',
 'sources': sources, 'source_model_changed': False
}
assert round(w, 2) == 47.92 and round(h, 2) == 18.96 and round(depth, 2) == 21.42
assert data['cooper_hunter']['required_finished_width_in'] > w
assert data['bosch']['required_width_in'] > w
assert data['cooper_hunter']['capacity_110f_btuh'] < data['cooper_hunter']['study_110f_sun_btuh']
for folder in [HERE, OUT]:
 (folder/'analysis.json').write_text(json.dumps(data, indent=2)+'\n')
shutil.copyfile(HERE/'fit-audit.json', OUT/'fit-audit.json')

# Equal-scale front comparison. Geometry is dimensional, not a product rendering.
svg = ['''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 650" role="img"><title>CL4-A01: above-door fit comparison</title><desc>The 64.96 inch Cooper and Hunter head exceeds the 47.92 inch finished hood. Bosch 36k fits as a case but fails installation clearance.</desc><style>text{font-family:Arial,sans-serif;fill:#17364a}.title{font-size:28px;font-weight:700}.label{font-size:18px}.small{font-size:15px}.dim{stroke:#17364a;stroke-width:1;marker-start:url(#a);marker-end:url(#a)}</style><defs><marker id="a" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto-start-reverse"><path d="M0 0L6 3L0 6Z" fill="#17364a"/></marker></defs><rect width="1200" height="650" fill="#faf8f1"/><text x="35" y="45" class="title">CL4-A01 / One indoor unit above the door</text><text x="35" y="76" class="label">Regular coach · CE1 finished construction · both panels at the same scale</text>''']
scale = 6
Y = lambda aff: 360-(aff-60)*scale
for cx, title, uw, uh, tc, side, name in [
 (300, 'C&H 60k-class ceiling unit', 64.96, 9.25, 35*mm, 35*mm, '64.96″ case'),
 (900, 'Bosch 36k wall unit', 44.88, 14.61, 5.9, 4.75, '44.88″ case')]:
 left = cx-w*scale/2
 top = Y(98.96)
 bodytop = top+tc*scale
 svg += [f'<text x="{cx}" y="115" text-anchor="middle" class="label">{html.escape(title)}</text>',
 f'<rect x="{left}" y="{top}" width="{w*scale}" height="{h*scale}" fill="#e8eee8" stroke="#347462" stroke-width="3"/>',
 f'<rect x="{cx-16*scale}" y="{Y(80)}" width="{32*scale}" height="120" fill="#edf0ef" stroke="#688592"/>',
 f'<rect x="{cx-(uw/2+side)*scale}" y="{top}" width="{(uw+2*side)*scale}" height="{(uh+tc)*scale}" fill="none" stroke="#b55743" stroke-dasharray="7 4" stroke-width="2"/>',
 f'<rect x="{cx-uw*scale/2}" y="{bodytop}" width="{uw*scale}" height="{uh*scale}" fill="#f5d9cc" fill-opacity=".9" stroke="#b55743" stroke-width="2"/>',
 f'<text x="{cx}" y="{bodytop+uh*scale/2+6}" text-anchor="middle" class="label">{name}</text>',
 f'<line x1="{cx-230}" y1="{Y(80)}" x2="{cx+230}" y2="{Y(80)}" stroke="#17364a" stroke-dasharray="3 4"/>',
 f'<text x="{cx}" y="{Y(80)+80}" text-anchor="middle" class="label">32″ clear end door</text>',
 f'<text x="{cx}" y="{Y(80)+104}" text-anchor="middle" class="small">80″ above finished floor</text>',
 f'<line x1="{left}" y1="400" x2="{left+w*scale}" y2="400" class="dim"/>',
 f'<text x="{cx}" y="427" text-anchor="middle" class="label">47.92″ finished hood width</text>']
svg += ['''<text x="70" y="470" class="label">Body is 17.04″ wider than the pocket.</text><text x="70" y="497" class="small">67.72″ clear width needed with 35 mm side gaps.</text><text x="70" y="524" class="small">26.57″ depth exceeds the 21.42″ pocket.</text><text x="670" y="470" class="label">54.38″ width needed with side clearances.</text><text x="670" y="497" class="small">Usual top gap puts the bottom below the door top.</text><text x="670" y="524" class="small">OEM doorway / vibration restrictions also apply.</text><rect x="70" y="559" width="18" height="18" fill="#e8eee8" stroke="#347462"/><text x="100" y="574" class="small">Existing finished pocket</text><rect x="340" y="559" width="18" height="18" fill="#f5d9cc" stroke="#b55743"/><text x="370" y="574" class="small">Unit body</text><path d="M560 568h35" stroke="#b55743" stroke-dasharray="7 4"/><text x="610" y="574" class="small">Published clearance envelope</text><text x="35" y="622" class="small">25 OCT 2026 PDT · FIT REVIEW ONLY · ADA HOOD NOT PRESENT IN CURRENT MODEL · NO FABRICATION RELEASE</text></svg>''']
(OUT/'CL4-A01.svg').write_text('\n'.join(svg))

def link(key, label): return f'<a href="{html.escape(sources[key], quote=True)}" target="_blank" rel="noopener">{label}</a>'
body = '''<section class="ce-hero"><p class="pf-eyebrow">CL4 · ABOVE-DOOR EQUIPMENT REVIEW · 25 OCTOBER 2026 PDT</p><h1>One per coach: the existing pocket does not fit.</h1><p class="ce-lead">Four larger single-zone mini-splits remain the preferred direction to investigate. This check found no verified single indoor unit that meets the hot-weather study load and the current above-door installation requirements.</p></section><nav class="ce-nav"><a href="#fit">Fit drawing</a><a href="#units">Actual equipment</a><a href="#capacity">Cooling capacity</a><a href="coach-envelope.html">Enclosure construction</a><a href="#sources">Sources &amp; data</a></nav><div class="ce-cards"><div class="ce-card"><strong>47.92″</strong>Finished width inside regular-coach raised hood.</div><div class="ce-card"><strong>18.96″</strong>Ceiling above the 80″ clear door opening.</div><div class="ce-card"><strong>21.42″</strong>Nominal depth to the lined inner return.</div></div><p class="ce-note"><strong>No equipment selected.</strong> The earlier eight-unit arrangement is not a demonstrated requirement. The 35-kW generator target stays provisional. This review supersedes the earlier generic above-door fit assumption; it does not change the retained coach frame.</p><h2 id="fit">Check the case and the installation space</h2><figure class="ce-figure"><a href="assets/coach-climate-cl4/CL4-A01.svg"><img src="assets/coach-climate-cl4/CL4-A01.svg" alt="Dimensioned comparison showing the large ceiling head wider than the hood and the smaller Bosch unit failing installation clearance"></a><figcaption>Green: current lined pocket. Orange: unit case. Dashed: manufacturer clearance envelope. Open drawing for full size.</figcaption></figure><p>The 54″ structural hood narrows to 47.92″ after the two 2″ side-frame depths, 1″ continuous insulation and .040″ liners. Its finished ceiling is 98.96″ above the floor. The door header extends to 82″, leaving 16.96″ above the header itself. Hood-side and return finishes are consistent CE1 reservations; installed trim and supports are not modeled.</p><p>The lower main roof meets the return at approximately 85.57″ above the floor at center. A unit inside this raised pocket can therefore have its discharge, intake or filter access obstructed even when its outer case fits. A real installation needs an open air path and service space.</p><p class="ce-note"><strong>Accessible coach is different.</strong> The C4 model has offset 78″ end doors and no modeled raised hood. The regular-coach dimensions cannot establish fit for the fourth coach.</p><h2 id="units">Three actual single-head candidates</h2><div class="ce-table"><table><thead><tr><th>Matched system</th><th>Capacity / efficiency</th><th>Indoor case, W × H × D</th><th>Disposition</th></tr></thead><tbody><tr><td><strong>Cooper &amp; Hunter</strong><br>CH-RSH60LCFC<br>+ CH-R60LCU-230VO</td><td>54,000 BTU/h rated cooling<br>19.5 SEER2</td><td>64.96″ × 9.25″ × 26.57″<br>Ceiling orientation</td><td><strong>Does not fit.</strong> Body is 17.04″ too wide and 5.15″ deeper than the pocket.</td></tr><tr><td><strong>Bosch Climate 5000</strong><br>BMS500-AAU036-1AHWXD<br>+ BMS500-AAS036-1CSXRD</td><td>36,000 BTU/h rated cooling<br>19 SEER2</td><td>44.88″ × 14.61″ × 11.22″</td><td><strong>Installation fails.</strong> Case fits alone; normal clearance envelope needs 54.38″ width and 20.51″ above the door.</td></tr><tr><td><strong>GREE Livo 36 R32</strong><br>LIV36HP230V1R32AH<br>+ LIV36HP230V1R32AO</td><td>33,600 BTU/h rated cooling<br>21 SEER2</td><td>42.44″ × 13.11″ × 9.69″</td><td><strong>Rejected for this application.</strong> Moving-base prohibition and conflicting clearance documents.</td></tr></tbody></table></div>'''
body += f'''<p><strong>C&amp;H ceiling unit:</strong> its manual calls for 35 mm top and side gaps and 1,000 mm forward space. That means at least <strong>67.72″ clear hood width</strong>, or about <strong>73.80″ outside the structural sides</strong> with the present construction—19.80″ wider than the current frame. This is a geometric minimum, not a roof redesign. The manual also specifies at least 2.2 m room height; the main-roof center is only 2.174 m. Mobile suitability has not been established. {link('ch_manual','Installation manual, printed pp. 4 and 14')}.</p><p><strong>Bosch wall unit:</strong> the manual’s normal drawing uses 4.75″ side gaps, 5.9″ above and 90.55″ minimum bottom height. It describes a reduced top-gap option, with service/performance qualifications; that does not solve the width failure. It also excludes doorway locations and requires a non-vibrating mounting location. The earlier 29.5-ft throw example was not a valid installation selection. {link('bosch_manual','Installation manual, p. 14')}.</p><p><strong>GREE wall unit:</strong> the submittal’s smaller gaps conflict with the installation manual’s 6″ top/side gaps and 98″ mounting height. More decisively, the manual excludes moving bases such as trucks. We cannot accept the favorable submittal alone. {link('gree_manual','Installation manual, printed pp. 16–17')}.</p>'''
body += f'''<h2 id="capacity">The “60k” label does not establish summer capacity</h2><p>The C&amp;H pair is rated for 54,000 BTU/h cooling; 60,000 is its rated heating figure. Its extended table gives <strong>41,200 BTU/h cooling at 110°F outdoors</strong>, at 1,365 CFM with 80°F dry-bulb / 67°F wet-bulb return air. Our CE1 110°F-sun study requires approximately <strong>55,866 BTU/h</strong> to target 75°F indoors. Those return conditions differ, so this is a rejection screen rather than an exact selection calculation: the published warmer-cabin point already falls short. {link('ch_performance','OEM cooling table, page 6')}.</p><div class="ce-table"><table><thead><tr><th>CE1 regular-coach condition</th><th>Provisional cooling load</th></tr></thead><tbody><tr><td>85°F evening</td><td>26,455 BTU/h</td></tr><tr><td>95°F evening</td><td>33,841 BTU/h</td></tr><tr><td>95°F sun</td><td>44,788 BTU/h</td></tr><tr><td>110°F sun</td><td>55,866 BTU/h</td></tr><tr><td>110°F sun + humidity stress</td><td>67,990 BTU/h</td></tr></tbody></table></div><p class="ce-small">300 CFM outdoor air is a study assumption, not an accepted ventilation rate. 37 thermal occupants is not an approved capacity. Cooling includes a 15% allowance; glazing and operating design conditions remain unresolved. No heat recovery is credited. These are regular-coach studies, not final HVAC selections.</p><h2>What this means for the design</h2><p>Keep one system per coach as the preferred investigation. A single larger indoor unit will require a different mounting space or a redesigned end roof, plus a clear air path. Select against confirmed outdoor-air flow, operating temperature, sensible/latent load and manufacturer mobile-installation conditions before changing the frame. A smaller unit could suit a restricted mild-weather operating case, but that case has not been adopted.</p><p><strong>Do not finalize the generator from these rejected units.</strong> The C&amp;H submittal’s 5,625 W nominal cooling input is an operating point; circuit ampacity and seasonal SEER2 are not generator load estimates. Use actual selected-system electrical performance, ventilation loads and generator derating before confirming 35 kW.</p><h2 id="sources">Primary sources and reproducible record</h2><ul><li>{link('ch_product','C&H product and document index')} · {link('ch_submittal','matched submittal')} · {link('ch_leaflet','2025 efficiency leaflet')} · {link('ch_manual','installation')} · {link('ch_performance','extended cooling')}</li><li>{link('bosch_submittal','Bosch 36k submittal')} · {link('bosch_manual','April 2026 installation manual')}</li><li>{link('gree_submittal','GREE Livo 36 submittal')} · {link('gree_manual','installation manual')}</li><li><a href="assets/coach-climate-cl4/fit-audit.json">Geometry audit and source hashes</a> · <a href="assets/coach-climate-cl4/analysis.json">Equipment / fit data</a> · <a href="assets/coach-climate-cl4/build.py">Reproducible source</a></li><li><a href="coach-envelope-engineering.html">CE1 load assumptions and sensitivities</a></li></ul><p class="ce-small">Manufacturer documents reviewed 25 October 2026 PDT. No supplier response or rail-service acceptance is implied. No CAD frame, mounting rail, drain, refrigerant line, roof fan or electrical connection is released by this review.</p>'''
page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Above-door mini-split fit · Pulsipher Farms</title><link rel="stylesheet" href="site-shell.css?v=cleanup1"><link rel="stylesheet" href="coach-envelope.css"></head><body class="pf-portal"><a class="pf-skip" href="#content">Skip to content</a><header class="pf-header"><a class="pf-brand" href="index.html"><b>PF</b><span>PULSIPHER FARMS<small>TRAIN DESIGN WORKSHOP</small></span></a><nav class="pf-nav"><a href="coaches.html">Coaches</a><a href="drawings.html">Drawings &amp; 3D</a><a href="engineering-index.html">Engineering</a></nav></header><main class="pf-main" id="content">{body}</main><footer class="pf-footer"><span>CL4 · Equipment fit review · No selected model</span><a href="archive.html">Previous versions</a></footer></body></html>'''
(D/'coach-hvac-fit.html').write_text(page)
banner = '''<aside data-cl4-note style="margin:1.2rem 0;padding:1rem 1.2rem;background:#f7edd8;border-left:4px solid #b18342"><strong>CL4 · One mini-split per coach is the preferred investigation.</strong> Actual equipment review found no verified single-head fit above the existing door. Model, capacity and 35-kW generator remain unconfirmed. <a href="coach-hvac-fit.html">See the dimensioned fit check →</a></aside>'''
targets = ['index.html','coaches.html','engineering-index.html','coach-regular.html','coach-accessible.html','coach-c1.html','coach-c21.html','coach-climate.html','coach-climate-engineering.html','coach-ventilation.html','coach-ventilation-engineering.html','coach-ventilation-system.html','coach-ventilation-system-engineering.html','tender-lt45.html','tender-lt45-engineering.html','coach-envelope.html','coach-envelope-engineering.html']
for name in targets:
 p = D/name
 if not p.exists(): continue
 t = p.read_text()
 t = re.sub(r'<aside data-cl4-note\b.*?</aside>', '', t, flags=re.S)
 t = t.replace('Eight mini-splits, airflow and 35kW remain provisional.', 'Airflow and 35 kW remain provisional; see CL4 for the current unit-count direction.')
 t = t.replace('Eight mini-splits and the 35kW generator remain candidates.', 'CL4 supersedes the eight-unit assumption: one per coach is preferred for investigation; no model is accepted and 35 kW stays provisional.')
 t = re.sub(r'(<main\b[^>]*>)', lambda m:m.group(1)+banner, t, count=1)
 p.write_text(t)
p = D/'assets/site-organization/current-selection.json'
j = json.loads(p.read_text())
j.update(coachHVACPage='coach-hvac-fit.html', coachHVACStatus=data['direction']+' CL4 rejects reviewed existing above-door installations; no model accepted. 35 kW remains provisional.', coachVentilationStatus='Compact powered roof intake/exhaust direction with mini-splits. CL3 rear cabinet superseded. No heat recovery credited; 300/400 CFM studies only. One system per coach preferred, model and 35 kW unconfirmed.')
if 'coach-climate-cl4' not in j['currentDrawingPackages']: j['currentDrawingPackages'].insert(0,'coach-climate-cl4')
p.write_text(json.dumps(j, indent=2)+'\n')
p = D/'assets/site-organization/current-drawing-catalog.json'
j = json.loads(p.read_text()); j['packages'] = [x for x in j['packages'] if x['id'] != 'coach-climate-cl4']
j['packages'].insert(0,dict(id='coach-climate-cl4', title='Above-door mini-split fit · CL4', engineering='coach-hvac-fit.html', fabricationPage='coach-hvac-fit.html', note='No selected system. Existing pocket fails reviewed installations; ADA requires separate hood design.', sheets=[dict(id='CL4-A01', title='Actual indoor units versus finished hood', image='assets/coach-climate-cl4/CL4-A01.svg', original='assets/coach-climate-cl4/CL4-A01.svg', kind='Dimensioned rejection screen; not construction release')]))
p.write_text(json.dumps(j, indent=2)+'\n')
shutil.copyfile(Path(__file__), OUT/'build.py')
print(json.dumps({'page':'coach-hvac-fit.html','geometry_in':[w,h,depth], 'no_selected_equipment':True}))

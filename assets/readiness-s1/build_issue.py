"""Build the controlled drawing/readiness index; never changes engineering geometry.

Reads preserved Site files and named archive members, hashes them, and renders
the same authored package records into HTML and JSON. No drawing or component
is promoted to fabrication release by passing this script.
"""

# Hosting transport: retain hashes of decoded source bytes after gzip packaging.
import gzip as _transport_gzip
def _transport_bytes(path):
    return path.read_bytes() if path.exists() else _transport_gzip.decompress(path.with_name(path.name + '.gz').read_bytes())

from pathlib import Path
import collections, hashlib, html, json, re, zipfile

P = Path(__file__).resolve().parent
D = P.parent.parent
A = D / 'assets'
E = html.escape
ISSUE = 'PF-3S1-READINESS-R0'
existing_state=json.loads((A/'engineering-program-state.json').read_text())
if int(existing_state['revision'].rsplit('R',1)[1])>17:
    raise RuntimeError('A newer program revision exists. Do not rerun this predecessor issuer or overwrite newer work.')

def read(path):
    return json.loads(_transport_bytes(A/path).decode())

def save(name, data):
    (P/name).write_text(json.dumps(data, indent=2, allow_nan=False)+'\n')

sources = {}
def evidence(path, member=None, purpose='Source evidence, not approval'):
    key = path + ('::'+member if member else '')
    if key not in sources:
        raw = _transport_bytes(A/path)
        item = dict(id=f'EV-{len(sources)+1:03}', path='assets/'+path,
                    file_sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw), purpose=purpose)
        if member:
            with zipfile.ZipFile(A/path) as z:
                content = z.read(member)
            item.update(archive_member=member, member_sha256=hashlib.sha256(content).hexdigest(), member_bytes=len(content))
        sources[key] = item
    return sources[key]['id']

def ev(path, member=None):
    return evidence(path, member)

JZIP='files/Christmas_Train_Phase3J_Technical_Source_R0.zip'
EZIP='files/Christmas_Train_Phase3E_Technical_Source_R0.zip'
FZIP='files/Christmas_Train_Phase3F_Technical_Source_R0.zip'
packages=[]
def package(id, title, classification, page, actual, omission, refs, role, gates, next_work):
    packages.append(dict(id=id,title=title,geometry_class=classification,page=page,
        actual_definition=actual,not_defined_or_not_demonstrated=omission,evidence_ids=refs,
        responsible_disciplines=role,release_gate_ids=gates,independent_next_work=next_work,
        fabrication_drawing_complete=False,fabrication_release=False,
        actual_test_acceptance_evidence=None,reader_check='Not passed: omitted interfaces/criteria listed; source existence is not buildability.'))

package('PK-01','Regular-coach underframe J1a','trial physical member geometry','#framej',
 '110 nominal HSS member shells: 16 CM6 and 52 S32 substitutions plus42 retained members. Archive register contains member IDs, orientation, dimensions, bounds, material candidates and connections. Catalog-member subtotal1816.347kg is not coach tare.',
 'End planes are not saw lengths. Register explicitly excludes I-BA angles, I-BT boxes, I-SH1 hardpoints, weld solids, bogie mounts, couplings and brakes. No released joints, WPS, local-wall/fatigue acceptance or complete assembled frame.',
 [ev('models3d/frame-J1a.json'),ev(JZIP,'models/Phase3J_J1a_Member_Register_R0.json'),ev(JZIP,'models/Phase3J_J1a_Integrated_Underframe_Study_R0.step'),ev(JZIP,'drawings/Stage3J_J1a_Plan_Actual_Inches_R0.dxf')],
 'Vehicle structural engineer + qualified fabricator/welding and inspection specialists',['SG-LOAD','SG-TRUCK','SG-JOINT','SG-QA'],
 'Reconcile every connection ID to one actual detail and drawing; integrate accepted supports and loads before machining/cutting release.')
package('PK-02','Local frame connections I1','trial physical local assemblies','#connections',
 'Six local assembly studies and160 mesh objects include receivers, branches and weld-volume representations. Sections, angles, tapered boxes, seat hardpoints and floor clips are inspectable in assembled/exploded views.',
 '160 mesh objects are not160 purchasable or fabricated parts. These details are NOT installed in the110-member J1a model. Represented weld volumes are not accepted weld sizes/procedures or demonstrated capacity.',
 [ev('models3d/connections-I1.json')],
 'Vehicle structural engineer + welding engineer + fabricator',['SG-JOINT','SG-FLOOR','SG-QA'],
 'Complete one load-path connection after its receiving members, stiffness, design loads, fit-up and inspection basis are accepted.')
package('PK-03','Accessible coach structure and seat/boarding layout','layout and ground-level mockup geometry','#phase3e',
 'Separate two-wheelchair-bay layout, shifted aisle/end-door datum and companion seating studies. Stage2 accessible viewer has31display objects and an earlier28in floor, not a coordinated32in load-state vehicle.3E mockup provides11fixed places in8seat assemblies plus2wheelchair bays; actual-inch DXF and canonical coordinates exist. Observation/device/chair forms are blank records.',
 'Do not copy regular-coach seat feet/support schedule into this car. No accepted wheelchair/lift point loads, independent accessible frame/joint schedule or signed occupied circulation/evacuation result. Sparse DXF labels require the coordinate table. Different source floor datums must not be interpreted as one accepted geometry.',
 [ev('models/accessible-coach.json'),ev(EZIP,'phase3e/source/mockup_layouts.json'),ev(EZIP,'phase3e/drawings/Stage3E_Accessible_Mockup_Actual_Inches_R0.dxf'),ev('body-o1/decisions-and-test-record.json')],
 'Vehicle structural/accessibility designers + responsible authority',['SG-ACCESS','SG-LOAD','SG-TRUCK','SG-JOINT'],
 'Use existing full-size mockup protocol; map actual accepted seat, wheelchair, boarding and evacuation loads to a separate support schedule. Do not issue a duplicate mockup.')
package('PK-04','Complete two-axle coach truck','display-only assembly plus separate load/motion studies','#brakeselection-runninggear',
 'G1 visualizes truck yaw. Later3L.3-S0/S1 analyze body datum, trial coil loads, bearing candidates, axle sensitivity and guide/brake motion interfaces.',
 'G1 596mm wheels,1165mm wheelbase,2in axle and displayed hardware are not selected sizes. No complete physical axlebox, guide, spring/damper, stops/retention, frame, pivot/sidebearer or brake assembly has been defined.',
 [ev('models3d/bogie-G1.json'),ev('suspension-l3/running_gear_inputs_S1.json'),ev('suspension-l3/motion_interfaces_S1.json'),ev('suspension-l3/bearing_candidates_S1.json')],
 'Rail vehicle/running-gear and dynamics engineers + bearing/brake/spring suppliers',['SG-WHEEL','SG-BEARING','SG-TRUCK','SG-D1'],
 'Close wheel/bearing/axlebox package and masses, then compatible guide articulation, brake reaction and twist/roll response; actual spring/damper envelopes precede mount sizes.')
package('PK-05','Rail wheels, rotating axles and removable drum hubs','manufacturing requirements and bounded calculations','#brakeselection-axlescreen',
 'Wheel manufacturing traveler and dimension matrix identify missing evidence; S1 axle/bearing sensitivities are preserved. D1 service concept keeps wheel and bearing installed while custom outboard hub/drum are removed together.',
 'No selected rail profile/back-to-back/wear limits, wheel-seat fit, axle fatigue/retention detail or hub joint. A semi-trailer stationary spindle arrangement cannot be copied onto a rotating rail axle.',
 [ev('fabrication-l1/wheel_fabrication/drawing_dimension_matrix.json'),ev('fabrication-l1/wheel_fabrication/manufacturing_traveler.json'),ev('suspension-l3/running_gear_results_S1.json'),ev('brake-selection-l2/selection.json')],
 'Wheelset/rail contact engineer + specialist wheel/axle manufacturer and NDT inspector',['SG-WHEEL','SG-BEARING','SG-D1','SG-QA'],
 'Complete exact wheel/rail and bearing arrangements before selecting journal, wheel-seat, hub-joint and machining fits; never derive dimensions from screenshots.')
package('PK-06','D1 installed coach brakes and custom supports','documented family match; schematic mounting/service studies','#brakeselection',
 'Dexter12.25×4 PQ S-cam with documentedType20/24 combination chamber is preferred coach prototype family:2brakes/axle,8/coach,32coach chambers. OEM drum-face orientation retained.',
 'L2-M01/M02/M03 are schematics, not fabrication drawings. Exact drum/pilot/holes, spider/cam/chamber envelopes, maximum torque curves, reverse modulation, custom hub/carrier/reaction geometry remain held. Locomotive package is separate.',
 [ev('brake-selection-l2/selection.json'),ev('brake-selection-l2/air_budget.json'),ev('drawing-quality-q1/drawing_audit.json'),ev('hardware-reference-q2/source_and_scope.json')],
 'Brake/running-gear engineers + Dexter/application evidence + qualified fabricator',['SG-D1','SG-TRUCK','SG-PNEUMATIC','SG-QA'],
 'Use controlled delivered D1 interfaces and full service/spring/fault torque with axlebox/guide motions; do not add an independently rigid reaction that locks suspension.')
package('PK-07','Air trainlines, control and stored energy','functional architecture and bounded demand budget','#phase3k',
 '3K contains trainline/state/failure architecture and test planning.3L.2 updates catalog-volume interfaces to32coach chambers; locomotive actuators and complete installed lines/valves remain separate.',
 'Functional topology is not a final port/plumbing or safety-controller implementation. Catalog volume sums do not validate charging, separation response, trapped pressure, brake balance, emergency timing or holding.',
 [ev('phase3k/brake-states.json'),ev('brake-selection-l2/air_budget.json')],
 'Rail brake/control engineer + pneumatic application specialists',['SG-PNEUMATIC','SG-D1','SG-POWER','SG-TEST'],
 'Freeze actual locomotive+coach valves/chambers, lengths/volumes and power allocation; prepare instrumented full-consist failure tests with accepted limits before operation.')
package('PK-08','Drawbar DB-01 and frame coupling joints','trial nominal physical part; incomplete assembly','#couplings',
 'DB-01 has editable nominal solid/profile and bounded train/part force cases. SKF GE60 ES-2RS is a catalog bearing comparison, not a selected joint.',
 'No released eye fit, retainers, pins/clevises, draft gear, frame attachment, secondary restraint or full-motion guards. Nominal DXF is not an NC cutting file; bearing catalog ratings are not coupling allowable loads.',
 [ev('coupling-m1/design_inputs.json'),ev('coupling-m1/DB01_STUDY_NOT_FOR_FABRICATION.step'),ev('coupling-m1/part_and_release_register.json'),ev('coupling-m1/train_force_basis.json')],
 'Vehicle structural/dynamics engineer + joint/bearing specialist',['SG-COUPLING','SG-LOAD','SG-JOINT','SG-TEST'],
 'Close complete pin/clevis/bearing/retention and frame load path under tension, compression, slack, fatigue and accepted articulation; then revise part and actual drawings.')
package('PK-09','Locomotive frame, powered running gear and propulsion','component matching and alternative studies','#propulsion',
 'Conditional hydrostatic lead: Kubota V3307-CR-TI-E5, Danfoss H1P045/H1B110 matching studies. Single-motor mechanically supported distribution is comparison lead; electric and mechanical routes retained.',
 'Not exact order codes or a construction-ready drive. No accepted continuous installed engine duty, complete powered chassis, supported reduction, adapter, mounts, cooling/exhaust, tank endurance or operator visibility envelope.',
 [ev('propulsion-n1/interfaces-and-release.json'),ev('propulsion-n2/decision-and-interface-register.json'),ev('propulsion-n3/decision-and-next.json')],
 'Drivetrain/running-gear engineers + engine/hydraulic application specialists',['SG-DRIVE','SG-LOAD','SG-WHEEL','SG-JOINT','SG-TEST'],
 'Obtain exact shaft/housing/continuous maps and vehicle arrangement; coordinate motor/reduction/axle relative motion and exhaust/cooling with occupied cars before physical adapter/frame detail.')
package('PK-10','Floor panels, seat hardpoints and seams','trial physical local parts with recorded interference problem','#coachbody',
 'O1 reproduces actual I-SH1 sole/opening stack: nominal zero vertical isolation is not a working clearance. Regular coach has64 seat-foot penetrations;21panel thermal sensitivities are not joint qualification.',
 'No accepted stack with positive tolerance/load/thermal clearance, panel inserts/edge closeouts, fastener grip/locking, movement topology or moisture-qualified joint. Accessible car requires its own mapping.',
 [ev('body-o1/audit-and-calculations.json'),ev('body-o1/decisions-and-test-record.json'),ev('body-o1/inherited-body-I1.json')],
 'Vehicle structural/materials engineer + seat/panel/adhesive suppliers',['SG-FLOOR','SG-ACCESS','SG-JOINT','SG-TEST'],
 'Resolve actual coupled hardpoint/panel stack and load bypass, then one exact production-material seat/panel coupon with defined proof/cyclic/thermal/wet acceptance.')
package('PK-11','Body, doors, glazing and historical locomotive shell','space reservations and partial component studies','#parts',
 'H1 indexes body/interior component envelopes; earlier coach views show adult-scale space studies. Three-inch wall and roof envelopes reserve space for structure, insulation and services.',
 'No complete physical wall/roof framing or skin joints, glazing retention, door mechanism/interlocks, fire/material basis, drainage/weather seal or locomotive historical shell fabrication set. Appearance does not resolve structural or evacuation details.',
 [ev('models3d/fabrication-H1.json'),ev('body-o1/decisions-and-test-record.json')],
 'Vehicle/body structural and materials engineers + door/glazing specialists',['SG-BODY','SG-ACCESS','SG-POWER','SG-QA'],
 'Define actual sections and load-bearing door/roof/HVAC rings from accepted packaging; coordinate emergency openings, weathering and maintainable joints.')
package('PK-12','HVAC, outside air and roof mounting','load reconciliation and actual-manual interface audit','#systems',
 'P1 separates obsolete hydraulic pump loads and heat-placement accounting. P2 audits Dometic installation data and roof/ADB/ventilation/service interfaces.',
 'No selected unit counts or roof ring/fasteners. Linked opening/clearance variants require exact configuration closure. Recirculation is not outside air; roof projection/headroom and condensate routes remain coordinated design inputs.',
 [ev('systems-p1/decision-and-next.json'),ev('systems-p2/inputs-and-evidence.json'),ev('systems-p2/physical-interfaces.json')],
 'HVAC/electrical + body structural engineers and actual HVAC supplier',['SG-HVAC','SG-BODY','SG-POWER','SG-TEST'],
 'Accept climate/occupancy/door/ventilation duty and exact unit/ADB manual; complete support, gasket stack, intake/exhaust separation and real ventilation paths.')
package('PK-13','Hotel supply, DC reserve and electrical installation','conditional demand budgets and physical requirements','#systems',
 'P1 records heat and electrical allocation boundaries, including charger and brake-compressor coordination. Earlier6A nonpump reserve is an unvalidated allocation, not a tested battery design.',
 'No selected generator/battery/charger, one-line, wire/breaker sizes, connector pinout, fault/bond/neutral regime or emergency-light duration. Hydraulic DC-B07 pump load is superseded in current configuration.',
 [ev('systems-p1/inherited-system-register.json'),ev('systems-p1/inputs-and-heat-placement.json'),ev('systems-p1/decision-and-next.json')],
 'Electrical engineer + brake/HVAC/propulsion engineers and authority',['SG-POWER','SG-PNEUMATIC','SG-TEST'],
 'Consolidate actual nameplate/start/fault loads and supply assignment; complete distribution, moving connections, bonding, isolation and cold/aged reserve with engineer-set tests.')
package('PK-14','End platforms, stairs, guards and boarding','walking-plane and installation reservations','#trackcivil-boarding',
 '3F has actual-inch walking-plane DXFs for32/36in floor studies and station/lift comparison;3E already defines ground-level occupied mockups.',
 'No accepted loaded floor range, physical stair mechanism/stow lock, hinge/frame mounts, guards/gates or moving clearance.7inrise/11ingoing benchmark is not an adopted vehicle code.44in platform is only a reservation.',
 [ev(FZIP,'phase3f/drawings/Stage3F_Stair_32in_Walking_Planes_Actual_Inches_R0.dxf'),ev(FZIP,'phase3f/drawings/Stage3F_Accessible_Station_Reservations_Actual_Inches_R0.dxf'),ev('track-r1/boarding-continuity.json')],
 'Vehicle/boarding structural and accessibility designers + responsible authority',['SG-ACCESS','SG-TRUCK','SG-JOINT','SG-TEST'],
 'Set actual stopped/traveling modes and mechanism, floor states, loads and accepted boarding criteria before hinges/bolts/welds; do not redraw the existing mockup as new fabrication.')
package('PK-15','Track, formation, crossings and stations','survey tools and component data audit; no site alignment','#trackcivil',
 'R1 provides local geometry checker, survey specification and work hold points. R2 records actual paper/CAD mismatch, joint-kit differences,18bounded support cases and12technical procurement interfaces.',
 'No actual survey/site route/soil/drainage design, selected rail/ties/fasteners or turnout/crossing/station construction set.30ASCE linkedIGES is quarantined:88.9mm versus79.375mm paper height/base.',
 [ev('track-r1/survey-and-civil-request.json'),ev('track-r1/crew-specialist-holdpoints.json'),ev('track-r2/rail-data-disposition.json'),ev('track-r2/technical-procurement-schedule.json')],
 'Licensed survey/civil + track/vehicle engineers and authority',['SG-SITE','SG-WHEEL','SG-TRACK','SG-ACCESS','SG-OPS'],
 'Complete real ground-level survey/datum and track/vehicle compatibility; freeze matched rail/joint/fastening and accepted proof-section design before installation release.')
package('PK-16','Fabrication methods, traceability and installation','controlled development scope and blank records','#fabrication',
 'Custom-fabrication master preserves part-ID hierarchy and specialist responsibilities.3F already contains material traceability, weld-joint release and prototype fabrication traveler forms.',
 'Blank forms are not completed inspection, qualified WPS/PQR, material certification or accepted as-built records. No safety-critical shop work is authorized by source availability.',
 [ev('fabrication-l1/fabrication_master/master.json'),ev(FZIP,'phase3f/forms/F1_Material_Traceability_R0.csv'),ev(FZIP,'phase3f/forms/F1_Weld_Joint_Release_R0.csv'),ev(FZIP,'phase3f/forms/F1_Prototype_Fabrication_Traveler_R0.csv')],
 'Responsible engineers + qualified fabricator/welding/machining/NDT specialists',['SG-QA','SG-JOINT','SG-TEST'],
 'Create consolidated per-assembly manufacturing/inspection plan using existing forms, after accepted drawing revision; define hold/witness points without inventing acceptance values.')
package('PK-17','Operations, maintenance, emergency response and commissioning','existing evidence forms; integrated train procedures incomplete','#build',
 '3E/3F contain instrumentation, configuration, deviation/regression and readiness/witness records. R2 separates normal leading-locomotive operation from unapproved reversing/shunting alternatives.',
 'No signed operating rulebook, staffing qualifications, dispatch/separation scheme, brake/evacuation acceptance values, actual test results or authority/insurance operating acceptance. Future second-train service is not cleared.',
 [ev(EZIP,'phase3e/forms/As_Built_Configuration_Register_R0.csv'),ev(EZIP,'phase3e/forms/Deviation_Impact_and_Regression_R0.csv'),ev(EZIP,'phase3e/forms/Test_Readiness_and_Witness_R0.csv'),ev('track-r2/topology-and-operating-decision.json')],
 'Operator/owner + responsible vehicle/track/control engineers + authority/emergency/insurer roles as applicable',['SG-OPS','SG-TEST','SG-QA'],
 'Complete integrated pre-service/shift/defect/emergency and staged commissioning development using controlled actual configuration; existing blank records must not be republished as test results.')

# Consolidated closure evidence, not fictional supplier requests already sent.
gates=[]
def gate(id, title, role, evidence_text, upstream=()):
    gates.append(dict(id=id,title=title,accountable_disciplines=role,closure_evidence=evidence_text,
        prerequisite_gate_ids=list(upstream),state='open',accepted_evidence=None,
        acceptance_authority_named_person=None,affected_package_ids=[p['id'] for p in packages if id in p['release_gate_ids']]))
gate('SG-LOAD','Accepted duty, mass/CG and governing load basis','Vehicle structural/dynamics engineers',
 'Controlled normal/fault/maintenance/transport load cases and fatigue spectrum; actual individual mass/CG allocation and wheel loads, including locomotive. Upper mass calculations are not measured tare or ratings.')
gate('SG-WHEEL','Coordinated wheel/rail contact and gauge','Rail vehicle + track engineers, wheel manufacturer',
 'Controlled new/worn wheel and rail profiles, back-to-back/gauge/reference definitions, flange/guard/frog clearances, minimum curve/transition and contact/stability assessment; accepted material/manufacturing basis.',('SG-LOAD',))
gate('SG-BEARING','Bearing/rotating axle/axlebox package','Wheelset engineer + bearing application specialist',
 'Exact bearing designation/arrangement, life/load/deflection, fits/shoulders/radii/seals/setting/retention and controlled source CAD; accepted axle strength/fatigue and wheel-seat assembly/inspection procedure.',('SG-LOAD','SG-WHEEL'))
gate('SG-D1','Delivered D1 interfaces and all applied torque','Brake/running-gear engineers + actual OEM evidence',
 'Exact assembled drum hub pilot/bolt/mating-face/service envelope; spider/cam/chamber geometry, service/spring force-stroke/torque including reverse/low-pressure/fault behavior; complete hub retention and stationary carrier interfaces.',('SG-BEARING',))
gate('SG-TRUCK','Suspension, guides, brake reaction and body support','Running-gear/dynamics/structural engineers',
 'Whole-truck sprung/unsprung mass/CG; compatible guide tilt/travel and brake reaction; spring/damper curves and working envelopes; stops/retention, pivot/sidebearer law, empty/loaded/bump/roll/twist wheel-load/stability; exact physical joints.',('SG-LOAD','SG-BEARING','SG-D1'))
gate('SG-COUPLING','Complete articulated coupling and load path','Vehicle structural/dynamics engineer + joint specialist',
 'Accepted tension/compression/slack/fault/fatigue and articulation; complete bearing/fit/retainers/pin/clevis/draft gear/secondary restraint/frame attachment/guards and service access; actual assembly drawing and tests.',('SG-LOAD','SG-TRUCK'))
gate('SG-DRIVE','Actual continuous engine and drive installation','Drivetrain engineer + engine/hydraulic/electrical application specialists',
 'Exact order-code shaft/housing and continuous torque/power/heat maps, derating/torsion; powered axle arrangement, supported reduction and motion, drive limits/reversing/failure control, cooling/fuel/exhaust and service/visibility interfaces.',('SG-LOAD','SG-WHEEL'))
gate('SG-FLOOR','Positive seat/floor isolation and panel joints','Structural/materials engineer + seat/panel/adhesive suppliers',
 'Revised coupled hardpoint/panel/fastener/seal stack under tolerances/loads/thermal movement; accepted panel closeouts/inserts/retention and exact production-material proof/cyclic/thermal/wet evidence. Accessible schedule separately.',('SG-LOAD',))
gate('SG-BODY','Physical walls, roof, openings and shell','Vehicle/body structural/materials engineers',
 'Actual sections/materials/joints, roof/HVAC loads, doors/locks/emergency egress/glazing retention/fire-weather/drainage/service details and fatigue; complete source geometry, BOM and recognizable coordinated drawings.',('SG-LOAD','SG-FLOOR'))
gate('SG-HVAC','Accepted climate, outdoor air and actual HVAC','Mechanical/HVAC engineer + actual unit supplier',
 'Design weather/occupancy/door duty and outdoor airflow; exact unit/ADB hardware/manual revision, net sensible/latent/heating/start/nameplate data, roof clamp stack/service paths and exhaust/condensate separation.',('SG-BODY',))
gate('SG-PNEUMATIC','Complete stored air and brake control','Rail brake/control engineer + pneumatic application specialists',
 'Full32coach chamber plus separate locomotive/lines/valves inventory, volumes/timing/leak/duty and compressor/reservoir/protection allocation; actual port/hose/state/failure design, isolated/trapped pressure and separation both portions.',('SG-D1',))
gate('SG-POWER','Electrical distribution, bonding and reserve','Electrical engineer + authority and brake/HVAC/drive engineers',
 'Selected actual generator/charger/DC loads including compressor assigned once; one-line, fault/voltage-drop/start recovery, neutral/bonding/protection, moving cables/pinouts/isolation and cold/aged emergency reserve/lighting.',('SG-HVAC','SG-PNEUMATIC','SG-DRIVE'))
gate('SG-SITE','Actual survey, terrain, formation and access','Licensed surveyor + civil/geotechnical/track designers',
 'Controlled property/topographic ground-distance/vertical datum survey and benchmarks, boundaries/utilities/soil/drainage/crossings/emergency access; NorthPole location when owner supplies it.0%target is not a measured profile.')
gate('SG-TRACK','Matched track component and alignment design','Track/civil/vehicle engineers + exact component suppliers',
 'Resolve rail CAD/paper identity and joint-kit differences; accepted rail condition/profile/steel/joints/ties/fastenings/ballast/subgrade, alignment/transitions/turnouts/crossings/clearances and gauge-restraint/thermal/drainage/proof-section acceptance.',('SG-SITE','SG-WHEEL'))
gate('SG-ACCESS','Applicable boarding/evacuation and real mechanisms','Responsible authority + accessibility/vehicle/boarding designers',
 'Recorded jurisdiction/applicable vehicle/station requirements; actual empty/loaded/bump floor/threshold range, station gap/bridge/lift/ramp, separate occupied-chair/companion circulation and failure evacuation; physical stair/guard/gate stow locks and full-motion mounts.',('SG-TRUCK','SG-BODY','SG-SITE'))
gate('SG-JOINT','Coordinated actual fabrication drawing and joint release','Responsible subsystem/structural engineer + qualified fabricator',
 'Per-part material/heat/toughness, datum, machining/fits/tolerances/finish, exact mating parts/fasteners/locking or weld design/WPS, assembly access and distortion strategy; complete load path, source-consistent views/BOM and practical builder review. Not closed by a model hash.')
gate('SG-QA','Manufacturing and configuration evidence','Responsible engineers + qualified fabrication/inspection team',
 'Released revision and accepted supplier certificates, qualified processes/personnel, material traceability, actual dimension/weld/NDT/assembly/retention inspection, nonconformance disposition and controlled as-built configuration; signed hold-point release.',('SG-JOINT',))
gate('SG-OPS','Authority and integrated operating/maintenance rules','Owner/operator + responsible authorities, engineers, emergency/insurance roles',
 'Written jurisdiction/applicability determination and required approvals; accepted route occupancy/dispatch, staffing/training, inspection/defect limits, protected boarding, emergency/rescue/towing/reversing rules, maintenance and actual configured manuals. No presumed FRA or amusement exemption.',('SG-TRACK','SG-ACCESS','SG-POWER','SG-PNEUMATIC'))
gate('SG-TEST','Controlled acceptance and commissioning evidence','Responsible engineers + independent/authority witnesses as applicable',
 'Approved safe test configurations/methods/instrumentation, numerical acceptance criteria and witness plan before tests; actual traceable results for structure, wheel loads/twist, articulation, empty/loaded forward/reverse/fault braking/parking/air timing/heat, power/HVAC/egress and route operation; formal disposition and operating release.',('SG-QA','SG-OPS','SG-COUPLING','SG-DRIVE'))

audit=dict(issue=ISSUE,review_date='2026-10-19',scope='Controlled current evidence and drawing-readiness index; no new part geometry, fabrication drawing or release.',
    packages=packages,source_manifest=list(sources.values()),
    totals=dict(packages=len(packages),fabrication_complete_claims=0,fabrication_releases=0,actual_accepted_test_records=0),
    count_semantics='Mesh objects/member counts are audited representations, not purchased-piece quantities, released BOMs or a completion percentage.',
    all_requested_subsystems_complete=False,supportable_desktop_program_complete=False)
save('package-and-source-index.json',audit)
save('release-evidence-register.json',dict(issue=ISSUE,scope='Consolidated working closure register across current packages; not an authority approval register or a claim that all engineering details have been enumerated.',gates=gates,closure_rule='Only actual accepted dated evidence with responsible professional/authority disposition may close a gate. Interacting designs require iteration; prerequisite graph is a release-order aid, not a one-pass design algorithm.'))

changes=[
 ('Historical hydraulic brake boxes / DC-B07 load','Superseded in current configuration','D1 air service / spring parking, actual compressor and power allocation still open','PK-06','PK-13'),
 ('Tolomatic ME220 MEFI mounting/rotor/linkage','Earlier alternative only','Do not mix its interfaces into D1 drum carrier or hub','PK-06','PK-05'),
 ('G1 visible wheels/axles/springs/bearings','Display-only','3L.3 physical package/motion work governs dependent next detail; no adopted G1 sizes','PK-04','PK-05'),
 ('J1a110 members + local I1details','Separate study representations','Do not claim I1details/brakes/truck/couplings are installed in J1a','PK-01','PK-02'),
 ('Nominal32in floor','Unaccepted load-state datum','No station height or stair mount release from this value','PK-04','PK-14'),
 ('D1 coach chamber total','32coach chambers, not total train actuators','Add separate actual locomotive package and lines/valves, not a guessed loco count','PK-06','PK-07'),
 ('Linked30ASCE IGES','Quarantined, not accepted geometry','Resolve88.9mmCAD versus79.375mm paper before modeling/ordering a matched rail','PK-15','PK-05'),
 ('Full-size occupied mockup','Existing3E protocol preserved','No observed result claimed and no duplicate new mockup issue','PK-03','PK-14')]
save('configuration-dispositions.json',dict(issue=ISSUE,items=[dict(item=a,status=b,current_rule=c,affected_packages=[d,e]) for a,b,c,d,e in changes],changes_to_selected_hardware=False))

byid={s['id']:s for s in sources.values()}
def source_links(ids):
    return '<ul>'+''.join('<li><a href="'+E(byid[i]['path'])+'">'+E(i+' · '+byid[i]['path'].split('/')[-1])+'</a>'+('<br>Archive member: <code>'+E(byid[i]['archive_member'])+'</code>' if byid[i].get('archive_member') else '')+'</li>' for i in ids)+'</ul>'
cards=[]
for p in packages:
    cards.append(f'''<article class="card" id="readiness-{p['id'].lower()}"><p class="eyebrow">{E(p['id'])} · {E(p['geometry_class'])}</p><h2>{E(p['title'])}</h2><p><strong>Actually present:</strong> {E(p['actual_definition'])}</p><p><strong>Not build-ready:</strong> {E(p['not_defined_or_not_demonstrated'])}</p><p><strong>Responsible disciplines:</strong> {E(p['responsible_disciplines'])}. Named acceptance professional: not assigned in this record.</p><p><strong>Next useful detail:</strong> {E(p['independent_next_work'])}</p><p>Release dependencies: {', '.join('<a href="#readiness-'+g.lower()+'">'+g+'</a>' for g in p['release_gate_ids'])}. No completed fabrication drawing, fabrication release or accepted physical test is asserted for this package.</p><a class="button" href="{E(p['page'])}">Open existing assembly / review page</a><details><summary>Exact source evidence and archive members</summary>{source_links(p['evidence_ids'])}</details></article>''')
gate_rows=''.join(f'''<tr id="readiness-{g['id'].lower()}"><td>{E(g['id'])}<br>{E(g['title'])}</td><td>{E(g['accountable_disciplines'])}</td><td>{E(g['closure_evidence'])}<br>Prerequisite closure: {E(', '.join(g['prerequisite_gate_ids']) or 'accepted project basis; no preceding gate assigned')}.</td><td>{', '.join('<a href="#readiness-'+x.lower()+'">'+x+'</a>' for x in g['affected_package_ids'])}</td></tr>''' for g in gates)
change_rows=''.join(f'<tr><td>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td></tr>' for a,b,c,d,e in changes)
issue=f'''<!-- S1 ISSUE START --><section id="readiness" class="panel"><div class="section-heading"><p class="eyebrow">3S.1 · CONTROLLED SOURCE / DRAWING READINESS · 19 OCTOBER 2026</p><h1>What is actually drawn—and what is still missing?</h1><p>This is a traceable index of17current packages, not another schematic or a new fabrication drawing. It links the exact existing source, model and drawing evidence to the physical connections still needed. All17packages remain unreleased; the whole desktop program is not complete.</p></div><article class="card build-notice"><h2>Start here, Ralph and fabricators</h2><p>A rotatable model may show a space reservation, a trial physical part or a display-only mechanism. None automatically supplies materials, fits, joints or an accepted load path. The list below says which kind you are opening. Sources are preserved—not silently replaced.</p><p><strong>Specific audit:</strong> J1a has110 nominal members; the register expressly omits the separate I1connection details, bogie mounts, couplings and brakes. I1has six local assemblies and160mesh objects, including weld representations—not160released fabricated pieces. No completion percentage is inferred.</p><p>Existing sources use explicit inches/mm as stated in each file. Exact source hashes and archive-member hashes are in the index. A hash confirms identity, not correctness, approval or physical fit. Linked archive members are identified so reviewers do not have to guess which STEP/DXF/register belongs to a study.</p><div class="actions"><a class="button" href="#readiness-register">Consolidated closure register</a><a class="button" href="assets/readiness-s1/package-and-source-index.json">Editable package / source index</a><a class="button" href="assets/readiness-s1/release-evidence-register.json">Editable release / evidence register</a></div></article><article class="card"><h2>Current configuration controls</h2><p>36in gauge remains under evaluation. One diesel locomotive plus3regular and1accessible coach;0%longitudinal target. NorthPole location deferred. Custom fabrication is the primary route. Public content is technical only.</p><div class="table-wrap"><table><thead><tr><th>Inherited item</th><th>Status</th><th>Current control</th></tr></thead><tbody>{change_rows}</tbody></table></div></article><article class="card"><h2>Choose the assembly</h2><ul>{''.join('<li><a href="#readiness-'+p['id'].lower()+'">'+E(p['id']+' · '+p['title'])+'</a></li>' for p in packages)}</ul></article>{''.join(cards)}<article id="readiness-register" class="card"><h2>One closure register:19open evidence gates</h2><p>These are accountable disciplines, not invented appointments. No supplier return, signed approval, physical test or acceptance value has been fabricated. A gate closes only against actual accepted evidence and a controlled revision. Interacting designs require iteration; prerequisite links are a release-order aid, not a promise that design can proceed in one pass.</p><div class="table-wrap"><table><thead><tr><th>Gate · open</th><th>Responsible disciplines</th><th>Exact closure evidence</th><th>Current affected packages</th></tr></thead><tbody>{gate_rows}</tbody></table></div></article><article class="card"><h2>What a completed drawing must establish</h2><p>Recognizable full assembly and cutaway/context; numbered physical parts matching its BOM; coordinated plan/elevation/section/details from the same geometry; actual mating faces, fasteners/retention, travel/service access; supported material, datum, dimensions/fits/tolerances, weld/joint specification and inspection points. Practical reader check: a builder can identify each part, each connection and what can be made without guessing. Drawing completeness and professional fabrication release are separate decisions.</p><p>This index checks file identity, source linkage, package/gate coverage and current configuration consistency—not practical drawing completeness. No new assembly is called buildable. Browser interaction remains unverified because managed preview could not start; the index is static HTML using existing Site navigation.</p><p><strong>Next3S.2:</strong> integrate fabrication/inspection travelers and assembly/installation/commissioning sequence using existing blank forms. Then continue supportable operations/emergency/maintenance/acceptance procedures. Do not repeat cosmetic HOLD sheets or call this completed3S,3L or a finished desktop package.</p><div class="actions"><a class="button" href="assets/readiness-s1/configuration-dispositions.json">Configuration dispositions</a><a class="button" href="assets/readiness-s1/build_issue.py">Editable index generator</a><a class="button" href="assets/readiness-s1/check_issue.py">Readiness source checks</a></div></article></section><!-- S1 ISSUE END -->'''
index=D/'index.html';s=index.read_text()
if '<!-- S1 ISSUE START -->' in s:s=re.sub(r'<!-- S1 ISSUE START -->.*?<!-- S1 ISSUE END -->',lambda _:issue,s,flags=re.S)
else:s=s.replace('<!-- R1 ISSUE START -->',issue+'\n<!-- R1 ISSUE START -->',1)
if 'data-tab="readiness"' not in s:s=s.replace('<a href="#fabrication" data-tab="fabrication">','<a href="#readiness" data-tab="readiness"><span>3S.1</span>Start here: build readiness</a>\n<a href="#fabrication" data-tab="fabrication">',1)
index.write_text(s)
app=D/'app.js';s=app.read_text()
if "readiness:'" not in s:s=s.replace('const sections = {',"const sections = {readiness:'Actual source and build readiness',",1)
if "rawTab.startsWith('readiness-') ?" not in s:s=s.replace("const tab = rawTab.startsWith('trackcivil-')", "const tab = rawTab.startsWith('readiness-') ? 'readiness' : rawTab.startsWith('trackcivil-')",1)
if "if(rawTab.startsWith('readiness-')" not in s:s=s.replace("if(rawTab.startsWith('trackcivil-')", "if(rawTab.startsWith('readiness-')||rawTab.startsWith('trackcivil-')",1)
app.write_text(s)

statep=A/'engineering-program-state.json';raw=statep.read_text();state=json.loads(raw)
if not(P/'predecessor-program-R16.json').exists():(P/'predecessor-program-R16.json').write_text(raw)
state.update(revision='PROGRAM-R17',latest_issue_url='https://pulsipher-train-review.fixinitcheap.chatgpt.site/#readiness',execution_note='3S.1 bounded current-source/drawing-readiness index issued:17packages,19open closure gates, exact file/archive-member hashes and8configuration controls. No new fabrication geometry or release; desktop program incomplete. Next3S.2 integrated manufacturing/inspection and assembly/installation/commissioning sequence using existing3E/3F records.')
state['current_independent_issue']=dict(stage='3S.1',issue=ISSUE,path='assets/readiness-s1',review_issue_complete=True,complete_phase3S=False,approved_for_fabrication=False,completed_scope=['17actual package/source readiness records','19consolidated open evidence gates with prerequisites and affected packages','Exact evidence/archive-member identity audit','8current configuration dispositions'])
sstate=next(s for s in state['stage_map'] if s['id']=='3S')
sstate['status']='bounded_source_readiness_index_complete_coordinated_design_release_open'
if 'assets/readiness-s1' not in sstate['evidence']:sstate['evidence'].append('assets/readiness-s1')
state['next_worker']['first_priority_correction']='3E E03 hydraulic actuator/blocked-drain/auxiliary-release test is obsolete for current D1. Create an exact current-configuration commissioning/change-impact crosswalk using3Everification,3Jprototype and3Kcontrol records; no hydraulic-to-pneumatic relabeling and no unapproved bench instructions.'
state['next_worker'].update(stage='3S',substage='3S.2',start_from='PROGRAM-R17; assets/readiness-s1; preserved3E/3F forms and existingfabrication master; all latest subsystem source',first_deliverable='Integrate exact per-assembly fabrication/inspection traveler and assembly/installation/commissioning release sequence using existing forms; no duplicate empty forms or unsupported process/acceptance values.',independent_follow_on='Complete supportable operating/maintenance/emergency and commissioning procedures with controlled configurations, role assignments and explicit engineer-set acceptance gates. Continue real engineering only where supported; avoid repeated cosmetic HOLDs.')
state['continuation']['next_scheduled_work_after_current_issue']='3S.2'
state['last_verified_deployment']=dict(version_number=28,commit_sha='3117c8fd091f818c8acb1bb6e1522034bcd71d8f',deployment_id='appgdep_6ad60bca56248191962fd5bd95b6e1ea',status='succeeded',verified_utc='2026-10-19T12:23:50.465989+00:00',scope='3R.2;3S.1 publication pending')
state['publication_state'].update(prepared_stage='3S.1 controlled build-readiness/source index',prepared_route='#readiness',status='prepared_for_publication',native_deployment_verified_in_this_file=False)
state['continuation_checkpoint']=dict(completed='3S.1 bounded source/configuration/drawing-readiness index;17packages/19open gates; not complete3S or desktop program.',next='3S.2 integrated fabrication/inspection traveler and assembly/installation/commissioning sequence, then operations/maintenance/emergency/acceptance development. Audit existing3E/3F records before creating new forms.',exact_new_evidence='J1a source110members expressly omits I1local details/brakes/trucks/couplings. I1sixlocal assemblies160meshobjects include weld representations. No model-object count is a released BOM.',current_sources=['assets/readiness-s1','assets/engineering-program-state.json','all linked current subsystem source and preserved3E/3F/3I/3J archives'],holds='All19consolidated closure gates open; actual supplier interfaces, mass/duty/motion, professional design and release, survey/authority and physical tests remain unresolved. No fabrication, operation or desktop completion claimed.',avoid='No duplicatedmockup, newcosmeticHOLDs, falsegeometry/readiness passes, purchasedcompletebogie substitution, business projections, outreach/orders or standalonechat/Librarydeliverables.',remaining_independent_work=True,automation_pause=False,publication='Prepared3S.1; native save/deploy result authoritative. Confirm latest before resuming, never roll back newer work.')
save('change-record.json',dict(issue=ISSUE,date='2026-10-19',predecessor_commit='3117c8fd091f818c8acb1bb6e1522034bcd71d8f',all_predecessor_files_preserved=True,new_fabrication_geometry=False,drawing_complete_claim=False,review_scope_complete=True,desktop_program_complete=False,next='3S.2'))
statep.write_text(json.dumps(state,indent=2)+'\n')
print(f'Built {ISSUE}: {len(packages)} packages, {len(sources)} source entries, {len(gates)} open gates. Publication pending.')

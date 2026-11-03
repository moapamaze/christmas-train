"""Rebuild LT1 layout, calculations and review records. Millimetres, not a cutting file."""
from pathlib import Path
import json, math, hashlib

P=Path(__file__).resolve().parent
def write(name,obj):
    (P/name).write_text(json.dumps(obj,indent=2)+'\n')

basis={
 'issue':'PF-LOCO-LT1-R0','date':'2026-10-19','status':'Preliminary arrangement; not for fabrication',
 'scope':'Locomotive/tender frame, appearance and packaging. Separate coach and DT1 drivetrain workstreams retain their detailed designs. LT1 running-gear layout is a proposal for DT-01 reconciliation.',
 'source_commit':'e7b1ff0288c02f9d45cbc23064122c903346ee83','recovered_program':'PROGRAM-R30',
 'units':'mm','datum':'X aft from locomotive nose, Y left from centreline, Z above rail top',
 'owner_basis':{'gauge':914.4,'grade_percent':0,'regular_cars':3,'accessible_cars':1,'appearance':'Polar Express / Pere Marquette 1225 reference; replaces Jupiter for this locomotive','traction':'Diesel with hydrostatic development lead'},
 'proposed_geometry':{
 'loco_length':9600,'tender_start':10200,'tender_length':5000,'overall_length':15200,'width':2600,'max_height':3400,
 'boiler_start':1600,'boiler_end':7400,'boiler_diameter':1700,'boiler_center_z':2050,
 'cab_start':7300,'cab_end':9500,'cab_floor_z':1150,'cab_roof_z':3300,
 'drive_wheel_diameter':1000,'small_wheel_diameter':600,
 'powered_truck_centres':[3300,6000],'powered_truck_wheelbase':1200,'drive_axles':[2700,3900,5400,6600],
 'leading_axles':[1200],'trailing_axles':[7900,8700],'tender_axles':[10900,11900,13500,14500],
 'tender_truck_centres':[11400,14000],'tender_truck_wheelbase':1000,
 'tender_height':2700,'coupling_gap':600,'drawing_coupler_z_proxy':650,
 'rail_head_width_visual_proxy':50,'wheel_width_visual_proxy':100},
 'geometry_status':'All arrangement dimensions are new designer proposals, not OEM mounting dimensions or released tolerances. Coupler Z is a drawing proxy only, not an interface agreement.',
 'running_gear':'2-(4+4)-4 appearance: one leading axle, two swiveling two-axle powered trucks, one two-axle trailing truck. Four large driving axles; not a literal rigid 2-8-4 replica.',
 'drive_architecture':'One pump; two H1B110 motors in parallel, each at maximum displacement driving a two-axle truck through a nominal 7.5:1 total reduction. Circuit and gear distribution remain unselected. DT1 retains single motor mechanically distributed drive as its current lead; LT1 two-motor option is a packaging alternative awaiting DT1 reconciliation, not an accepted replacement.',
 'rod_rule':'No rod bridges the two powered trucks. R0 omits moving cosmetic rods; short truck-local rods require separate retention, articulation and guarding design.',
 'mass_proposal_kg':{'loco_total':12000,'loco_on_powered_axles':10000,'loco_leading_support':600,'loco_trailing_support':1400,'tender_total':2500},
 'mass_status':'Load allocation study only. No component mass takeoff, ballast design, support stiffness solution or as-built weighing. Four independent loco support groups require compliant/equalized load sharing and wheel-unloading review.',
 'construction_approved':False,
 'next_work':['Resolve common coach mass and accepted curve envelope','Compare rigid 2-8-4 against articulated layout using wheel/rail and support model','Develop locomotive load ledger, frame and suspension load paths','Obtain engine/pump/motor installation CAD and matched reversing circuit','Develop measured component and custom-part drawings after interfaces converge']
}
write('basis.json',basis)
g=basis['proposed_geometry']
eta=.95*.90*.95*.90*.95
q=45*2600*.95/1000
motor_rpm=q/2*1000*.95/110
speed=motor_rpm/7.5*math.pi/60
torque=300*110/(20*math.pi)*.90
force=2*torque*7.5*.95/.5
shaft=55.4-10
curves=[]
for R in [20,30,45]:
    curves.append({'radius_m':R,'powered_truck_angle_relative_body_deg':math.degrees(math.asin(2.7/(2*R))),
      'truck_wheelbase_mid_ordinate_mm':1000*(R-math.sqrt(R*R-.6*.6)),
      'rigid_four_axle_span_mid_ordinate_mm':1000*(R-math.sqrt(R*R-1.95*1.95)),
      'body_mid_ordinate_between_drive_pivots_mm':1000*(R-math.sqrt(R*R-1.35*1.35))})
cases=[]
for mass in [54755,65100,67500]:
 for extra in [0,2000,5000]:
    fr=mass*9.80665*.005+extra
    fs=mass*9.80665*.01+extra
    cases.append({'mass_kg':mass,'extra_drag_N':extra,'run_force_N':fr,'start_force_N':fs,
      'cruise_engine_kW':fr*speed/1000/eta+10,
      'launch_acceleration_m_s2_at_mu015':(min(force,10000*9.80665*.15)-fs)/mass,
      'launch_acceleration_m_s2_at_mu010':(min(force,10000*9.80665*.10)-fs)/mass})
calcs={'issue':basis['issue'],'assumptions':{'pump_cc':45,'pump_rpm':2600,'motor_count':2,'each_motor_cc':110,'ratio':7.5,'wheel_m':1,'pressure_bar':300,'pump_eta_v':.95,'pump_eta_m':.90,'motor_eta_v':.95,'motor_eta_t':.90,'gear_eta':.95,'auxiliary_kW':10,'gross_intermittent_engine_kW':55.4,'powered_mass_trial_kg':10000},
 'results':{'pump_flow_l_min':q,'each_motor_rpm':motor_rpm,'speed_m_s':speed,'speed_mph':speed/0.44704,'force_N':force,'total_wheel_torque_Nm':force*.5,'overall_efficiency':eta,'full_flow_pressure_limit_bar':shaft*600000*.90/(45*2600),'pump_cc_at_300bar_power_limit':shaft*600000*.90/(300*2600),'speed_mph_at_300bar_power_limit':speed/0.44704*(shaft*600000*.90/(300*2600))/45,'min_adhesive_mass_at_mu015_kg':force/(.15*9.80665),'main_loop_heat_kW':shaft*(1-.95*.90*.95*.90),'gear_heat_kW':shaft*.95*.90*.95*.90*(1-.95),'one_branch_all_flow_rpm_at_110cc':q*1000*.95/110,'one_branch_all_flow_rpm_at_22cc':q*1000*.95/22,'powered_axle_load_trial_kg':2500},
 'mass_cases':cases,'curve_cases':curves,
 'interpretation':[
 'Two motors share flow; 1000mm wheels and 7.5:1 preserve the old 600mm/9:1/single-motor ideal force and speed. This is an analytical rematch, not a supplier-approved design.',
 '7.5mph and 300bar cannot occur simultaneously within the 55.4kW gross intermittent budget. Installed continuous power is unknown.',
 'Parallel branch overspeed and reverse/retarding flow must be controlled. Generic flow divider not selected; no credit for equal sharing under faults.',
 '300bar is a calculation point, not a relief setting. Constant efficiency assumptions do not establish stall or creeping torque.',
 '67,500kg adds a 2,400kg seat-growth sensitivity to the old 65,100kg case: 3 x (1,040 - 240). This may double-count existing growth margins; it is not a revised rated gross mass.',
 'The old 14,500kg locomotive/hotel allowance is provisionally split 12,000/2,500 between locomotive and tender. Tender creates a sixth braked vehicle and another separation point. Do not add tender mass a second time.',
 'Latest R30/DT1 direction: evaluate generation from propulsion diesel first. Hotel shaft demand is additional to the 10kW traction auxiliary allowance. Tender generator bay is an optional fallback reservation only; selected generator kW is null.',
 'Curve mid-ordinate is chord geometry only, not required wheelset lateral travel, flange clearance or proof of curving. Wheel profile, gauge widening, lead/trailer yaw, suspension, end swing and couplings require full swept analysis.'
 ],'formulas':['Q = Dp * np * eta_pv / 1000 (L/min)','nm = (Q / 2) * 1000 * eta_mv / Dm','v = (nm/i)*pi*d/60','Tm = dp_bar * Dm_cc * eta_mt / (20*pi)','F = 2 * Tm * i * eta_g / (d/2)','P_engine = F_running*v/(1000*eta_total) + P_aux','a = (min(F_drive,mu*m_powered*g)-F_start)/m_train','mid ordinate = R - sqrt(R^2-(L/2)^2)']}
write('calculations.json',calcs)
interfaces=[
 ['IF01','Gauge','914.4 mm owner working basis','Wheel back-to-back, tread/flange profile, rail section and check gauge unassigned','Both vehicle workstreams / track'],
 ['IF02','Mass','65,100 kg historical upper case; 67,500 kg sensitivity','Coach C2 seating growth, accessible seating, HVAC, generator and tender allocation must reconcile','Coach + locomotive'],
 ['IF03','Coupler','Height and type unresolved; 650 mm drawing proxy only','Coach J1 and loco/tender interfaces need matched ratings, yaw/pitch/roll, draft gear and retention','Coupling engineer'],
 ['IF04','Coupler force','Coach tail mass 50,600 kg historical; 53,000 kg seat-growth probe','At 0.1 m/s² and start c=.01 plus all 2kN drag downstream: 12.02 / 12.50 kN. Tender-front adds 2,500 kg. Shock, slack and fault/compressive loads still open','Both workstreams'],
 ['IF05','Brakes','Air service / spring-applied air-released parking; retained CR-G01','Add tender as sixth vehicle; BP/MR and supervised emergency continuity through both new joints; connector/pressure/line sizes held','Brake integration'],
 ['IF06','Electrical','Shared propulsion/generation diesel evaluation first; 120/240V 60Hz proposal','Exact voltage/current/grounding/protection/interlocks/connector pinout unresolved; no passenger HVAC counted in traction allowance','Electrical + coach HVAC'],
 ['IF07','Curves','20/30/45 m sensitivity; no approved minimum radius','Survey, track design, coach sweep and this locomotive/tender swept envelope must agree','Track + both vehicles'],
 ['IF08','Clearance','Proposed locomotive/tender width 2,600 mm, highest point 3,400 mm','Does not include dynamic roll/yaw, mirror/handrail/guard projection, structure gauge or route clearance','Both workstreams / track'],
 ['IF09','Operating limits','7.5 mph calculation speed; zero grade target','Route speed, acceleration, stops, reverse/push operation and construction grade tolerances not approved','Operations / vehicle'],
 ['IF10','Work ownership','LT1 owns locomotive and tender only','Passenger car drawings and shared PROGRAM-R30 are preserved; this register is a handoff, not live synchronization between chats','Owner / both chats']]
write('interfaces.json',{'issue':basis['issue'],'columns':['id','interface','retained_or_proposed','open_input','owner'],'rows':interfaces})
conflicts=[
 ['Appearance','Jupiter','Polar Express / 1225 appearance per current owner direction'],
 ['Running gear','600 mm wheels, one motor, 9:1 workbook','LT1 trial: 1,000 mm drive wheels, two 110cc motors, 7.5:1 each. Recalculated, not silently substituted'],
 ['Brake system','Older hydraulic preference','Superseded by CR-G01 air service and spring parking'],
 ['Vehicle count','Locomotive plus four coaches = five','Separate tender adds sixth braked vehicle and one more coupling/separation test'],
 ['Mass','65,100 kg treated as fixed upper mass','Still provisional; C2 seat growth and tender/hotel allocation need reconciliation'],
 ['Latest source','Older Library phases 3E/3F','Current site PROGRAM-R30 and later N1–N3 studies control recovery'],
 ['Published workflow','Single whole-train continuation record','Preserve separate coach and DT1 drivetrain workstreams; LT1 packaging proposals need interface reconciliation'],
 ['Generation','Earlier dedicated hotel diesel recommendation','R30/DT1 owner direction: evaluate propulsion-diesel generation first; tender generator only a fallback'],
 ['Motor count','DT1 single-motor lead','LT1 two-motor rematch is an alternative for articulation packaging, not a replacement accepted by DT1']]
write('recovery-and-conflicts.json',{'issue':basis['issue'],'conflicts':conflicts,'read_sources':['Train_Danfoss_Matching_Calculation_R0.xlsx (current Library text)','Phase3F Prototype Integration R0, pages1–5','Phase3K Air Brake Integration R0, pages1–3','Site PROGRAM-R30','Site propulsion-n1 inputs and sources','Site propulsion-n2 decisions and interfaces','Site README and C1/C2 source','Current R30 recovery and DT1 drivetrain coordination record'],'preservation':'Original files unchanged; standalone LT1 pages and records added.'})
parts=[
 ['LT-F01','Locomotive chassis',1,'Custom','Steel structural assembly; member/joint sizing deferred until axle loads and support stiffness solved','Material family proposal only; no cut list'],
 ['LT-R01','Powered truck assembly',2,'Specialist/custom integration','1,200 mm axle spacing; two 1,000 mm wheelsets each; center/pivot/side-support and springs to develop','No wheel/axle/bearing fit or motor mount released'],
 ['LT-R02','Leading truck',1,'Specialist/custom integration','One 600 mm wheelset; pivot station X1,200','Yaw/retention/support not yet detailed'],
 ['LT-R03','Trailing truck',1,'Specialist/custom integration','Two 600 mm wheelsets; axle stations X7,900 / 8,700','Load sharing and suspension unresolved'],
 ['LT-R04','Tender truck',2,'Specialist/custom integration','Two 600 mm wheelsets each; 1,000 mm wheelbase','Same gauge/profile interface as train; lower load does not permit assumed coach geometry'],
 ['LT-P01','Kubota V3307-CR-TI-E5 engine',1,'Purchase candidate','55.4kW gross intermittent at2,600rpm; published envelope with aftertreatment856×557×749mm, excludes cooling fan','OEM package, continuous duty and cooling acceptance required'],
 ['LT-P02','Danfoss H1P045 pump',1,'Purchase candidate','45cc/rev study; configuration/control/shaft/charge pump unselected','Matched engine adapter and torsional coupling required'],
 ['LT-P03','Danfoss H1B110 motor',2,'Purchase candidate','110cc/rev each study; parallel circuit','No generic series motor or fixed divider substitution'],
 ['LT-P04','Reduction / axle distribution',2,'Specialist designed or purchase','7.5:1 overall per truck proposal, four driven axles total','Bearings, torque reaction, plunge/angles and reversing loads to size'],
 ['LT-B01','Matched air brake system',1,'Purchase + engineered integration','Locomotive + tender + four coach service, emergency and parking coordination','Brake chambers alone are not complete systems'],
 ['LT-C01','Removable decorative shell',1,'Custom','1,700 mm cylindrical shell; matte black finish; nonpressure enclosure','Proposed 2mm 5052-H32 skin, ribs/fasteners/hot-zone lining to design; not structural load carrier'],
 ['LT-C02','Cab and operator station',1,'Custom','2,200mm length; 2,600mm external width; floor1,150 / roof3,300mm','Actual clear standing space, doors, seats, sightlines, escape and hot/noise barriers to resolve'],
 ['LT-T01','Tender chassis/body',1,'Custom','5,000×2,600mm footprint; body top2,700mm','Frame and lifting/tie-down joints not detailed'],
 ['LT-T02','Fuel/service module',1,'Purchase + engineered integration','Tender low service zone; capacity unselected','Fuel may move to loco if cross-coupling line risk/installation requirements govern'],
 ['LT-T03','Hotel generation / utility module',1,'Purchase candidate not selected','Shared-engine generator integration first; tender bay reserved only for fallback separate genset or utilities','Sizing requires current mini-split loads; full module, fuel and exhaust count in tender mass'],
 ['LT-E01','Controls, cooling and electrical',1,'Integrated package','Traction inhibition, overspeed, emergency stop, compressor, oil/engine cooling, lighting and batteries','Exact ratings, wire sizes, hoses, ports and circuit drawings held']]
write('component-schedule.json',{'issue':basis['issue'],'columns':['id','assembly','quantity','make_buy','definition','status'],'rows':parts,'pricing':'No verified quotations recovered for this exact locomotive configuration. No invented unit prices or total. Supplier references are inquiry leads, not stock or application acceptance.','cost_next':'Price the exact running gear, gearboxes, matched hydraulic package and generator first; then take off structural steel and enclosure sheet from developed parts.'})
sources=[
 ['S01','Steam Railroading Institute','https://michigansteamtrain.com/equipment/','1225 is the film visual/sound prototype, 2-8-4; reference overall101ft and height15ft8in. LT1 is a compact reinterpretation, not scaled replica.'],
 ['S02','Kubota','https://engine.kubota.com/products/detail?id=212&ln=en','Engine catalog power, speed, envelope, mass and intermittent rating footnote rechecked19Oct2026.'],
 ['S03','Danfoss H1P technical information','https://assets.danfoss.com/documents/latest/505211/BC152886483105en-001701.pdf','Primary pump document; earlier N1 controlled source register retained.'],
 ['S04','Danfoss H1B','https://www.danfoss.com/en/products/dps/motors/mobile-motors/mobile-piston-motors/variable-displacement-axial-piston-motors/h1b-bent-axis-variable-motors/','Current manufacturer family includes110cc. Exact configuration and installation drawing remain open.'],
 ['S05','Danfoss circuit recommendations','https://assets.danfoss.com/documents/latest/284995/BC152886483346en-000202.pdf','Recovered N2 reference: parallel flow sharing, series drawbacks and reversing/retarding circuit review. Not new application approval.']]
write('sources.json',{'date':'2026-10-19','sources':sources})

# Exact coordinated arrangement drawings. Drawing geometry uses the same dimensions as model.json.
write('model.json',basis)
def svg_start(title,sub,w=1600,h=850):
 return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><style>text{{font-family:Arial,sans-serif;fill:#17364a}}.t{{font-size:18px}}.s{{font-size:15px}}.d{{stroke:#9a691e;stroke-width:1.3;fill:none}}.body{{fill:#35434b;stroke:#182c38;stroke-width:2}}.line{{stroke:#17364a;fill:none;stroke-width:2}}</style><rect width="100%" height="100%" fill="#fffef9"/><text x="40" y="42" font-size="28" font-weight="bold">{title}</text><text x="40" y="70" class="t">{sub}</text>']
def text_(a,x,y,s,cl='t'):a.append(f'<text x="{x}" y="{y}" class="{cl}">{s}</text>')
def dim(a,x1,x2,y,s):
 a.append(f'<path class="d" d="M{x1},{y-8}v16 M{x2},{y-8}v16 M{x1},{y}H{x2}"/>');text_(a,(x1+x2)/2-40,y-10,s,'s')
a=svg_start('LT1-A01 · Locomotive + tender / side arrangement','R0 · 19 October 2026 · Proposed dimensions in mm · PRELIMINARY — NOT FOR FABRICATION')
s=.095; ox=70; rail=460
X=lambda x:ox+x*s
Z=lambda z:rail-z*s
def rect(x,z,l,h,fill='#35434b'):
 a.append(f'<rect x="{X(x)}" y="{Z(z+h)}" width="{l*s}" height="{h*s}" fill="{fill}" stroke="#17364a"/>')
rect(350,850,9200,280);rect(1600,1200,5800,1700);rect(7300,1150,2200,2150)
rect(7500,2200,650,750,'#bcd5df');rect(8350,2200,850,750,'#bcd5df')
rect(1950,2850,350,550);rect(3650,2850,500,280);rect(5400,2850,450,260)
rect(10200,750,5000,1950);rect(10300,2600,1700,100)
rect(1540,1950,80,400,'#f7e2a9')
for xx in [1900,3500,5200,7000]:
 a.append(f'<path d="M{X(xx)},{Z(1200)}V{Z(2900)}" stroke="#85949a" stroke-width="2"/>')
a.append(f'<path d="M{X(2300)},{Z(2500)}H{X(6900)}" stroke="#b2bdc2" stroke-width="3"/>')
rect(1700,1185,5600,70,'#172b37');rect(1575,520,750,460)
a.append(f'<path class="line" d="M{X(0)},{Z(150)} L{X(350)},{Z(850)} L{X(1050)},{Z(850)}"/>')
for xs,r in [(g['drive_axles'],500),(g['leading_axles']+g['trailing_axles']+g['tender_axles'],300)]:
 for x in xs:
  a.append(f'<circle cx="{X(x)}" cy="{Z(r)}" r="{r*s}" fill="#d7dce0" stroke="#17364a" stroke-width="4"/>')
  for t in range(0,180,30):
   u=math.cos(math.radians(t))*r*s*.9;v=math.sin(math.radians(t))*r*s*.9
   a.append(f'<path class="line" d="M{X(x)-u},{Z(r)-v}L{X(x)+u},{Z(r)+v}"/>')
  a.append(f'<circle cx="{X(x)}" cy="{Z(r)}" r="7" fill="#17364a"/>')
a.append(f'<path class="line" d="M40,{rail}H1560 M{X(9600)},{Z(650)}H{X(10200)}"/>')
dim(a,X(0),X(9600),525,'9,600 locomotive');dim(a,X(9600),X(10200),490,'600 gap');dim(a,X(10200),X(15200),525,'5,000 tender');dim(a,X(0),X(15200),570,'15,200 total (49 ft 10 in)')
for x,label in [(1200,'Leading'),(3300,'Powered A'),(6000,'Powered B'),(8300,'Trailing'),(11400,'Tender A'),(14000,'Tender B')]:
 a.append(f'<path class="d" d="M{X(x)},465v25"/>');text_(a,X(x)-32,510,label,'s')
text_(a,40,630,'Four Ø1,000 driving axles in two swiveling trucks · each powered truck wheelbase 1,200 · powered pivots 2,700 apart')
text_(a,40,665,'Small wheels Ø600 · cab floor Z1,150 / roof Z3,300 · maximum stack height Z3,400 · overall width 2,600')
text_(a,40,700,'No cross-truck connecting rod. Brakes, suspension hardware, flange profile and final couplers are not detailed in this layout.')
text_(a,40,735,'Exterior compresses the 1225 reference proportions. Drawing is dimensioned project geometry, not a traced movie blueprint.')
text_(a,40,795,'PF-LOCO-LT1-R0 · X from nose / Z above rail · Coupler Z650 shown only as an unagreed drawing proxy','s')
(P/'LT1-A01-side.svg').write_text(''.join(a)+'</svg>')

a=svg_start('LT1-A02 · Plan / installation zones','Same LT1 geometry · Approximate installation reservations; not delivered-component CAD')
Y=lambda y:330-y*.095
def planbox(x,y,l,w,color,label):
 a.append(f'<rect x="{X(x)}" y="{Y(y+w/2)}" width="{l*s}" height="{w*s}" fill="{color}" stroke="#17364a"/>');text_(a,X(x)+7,Y(y)+5,label,'s')
planbox(0,0,9600,2600,'#edf0f0','');planbox(10200,0,5000,2600,'#edf0f0','')
planbox(1400,0,800,1100,'#d1e4da','Cooling');planbox(2400,0,2100,1200,'#f1d4a2','Engine / pump');planbox(4900,0,1700,1200,'#d1e4da','Oil / air');planbox(7300,0,2200,2600,'#bcd5df','Operator cab');planbox(10500,0,1400,1500,'#f1d4a2','Fuel / service');planbox(12500,0,2300,1800,'#d1e4da','Utility / option')
for x in g['powered_truck_centres']+g['tender_truck_centres']:
 a.append(f'<circle cx="{X(x)}" cy="330" r="10" fill="none" stroke="#9a691e" stroke-width="3"/>')
for y in [-457.2,457.2]:a.append(f'<path d="M40,{Y(y)}H1560" stroke="#607582" stroke-dasharray="8 7"/>')
dim(a,X(3300),X(6000),490,'2,700 powered pivot spacing')
text_(a,40,555,'Orange = combustion/fuel service zones · green = cooling/utility zones · blue = cab · circles = main powered / tender pivots')
text_(a,40,595,'Engine zone reserves adapter, hoses and service space beyond the published 856 × 557 × 749 engine envelope; fan is excluded by OEM.')
text_(a,40,635,'Boiler shell is a ventilated, nonpressure cover. Provide removable sides/top; protect cab from DPF/exhaust heat and direct fumes away.')
text_(a,40,675,'Tender rear utility / optional-generator bay is a reservation only: real airflow, exhaust, fuel capacity, service-door swing and unit dimensions remain open.')
text_(a,40,715,'Rail dashed lines show gauge references, not wheel-back spacing. Nothing in this sheet defines final wheel profile or flange clearances.')
text_(a,40,795,'PF-LOCO-LT1-R0 · X longitudinal / Y lateral · enclosure access and all moving envelopes require coordinated detail','s')
(P/'LT1-A02-plan.svg').write_text(''.join(a)+'</svg>')

a=svg_start('LT1-A03 · Powered truck / frame connection concept','Functional load paths and proposed stations · connection sizing is not released')
for x,label in [(320,'Truck A · X3,300'),(1080,'Truck B · X6,000')]:
 a.append(f'<rect x="{x-220}" y="230" width="440" height="35" fill="#17364a"/><rect x="{x-190}" y="360" width="380" height="35" fill="#607582"/>')
 for xx in [x-145,x+145]:
  a.append(f'<circle cx="{xx}" cy="440" r="70" fill="#d6dee2" stroke="#17364a" stroke-width="3"/><path d="M{xx},280v65" stroke="#9a691e" stroke-width="12" stroke-dasharray="5 5"/>')
 a.append(f'<path d="M{x},265v95" stroke="#bd6c35" stroke-width="10"/>');text_(a,x-150,195,label)
 text_(a,x-220,560,'1,200 axle spacing / Ø1,000 wheels')
text_(a,55,120,'Main frame → vertical load supports / suspension → truck frame → axlebox springs → bearings / axle → wheels → rail')
text_(a,55,610,'Yaw pivot and separate traction/brake reaction transfer must allow bounce, roll and lateral movement without binding.')
text_(a,55,650,'Motor and supported reduction ride on the truck. Final axle drives need articulated joints and torque reaction members.')
text_(a,55,690,'Four locomotive support groups require a stiffness/equalization solution; the drawn springs do not establish load sharing.')
text_(a,55,730,'Spring rates, travel, pivot/side-bearing sizes, retaining joints, welds, bolt patterns and fit tolerances are deliberately not assigned.')
text_(a,55,795,'PF-LOCO-LT1-R0 · Diagram is functional and not to scale; use A01/A02 for arrangement stations','s')
(P/'LT1-A03-supports.svg').write_text(''.join(a)+'</svg>')

write('workstream-state.json',{'issue':basis['issue'],'completed_scope':['Recovery and conflict register','Dimensioned first side/plan layout','Rotatable matching arrangement model','Two-motor drivetrain rematch and curve/mass sensitivity','Shared interface and preliminary component schedules','Concurrent R30 and DT1 work preserved; shared-generation direction applied'], 'not_complete':['Complete locomotive engineering','Fabrication part drawings','Final parts pricing','Brake/structure/drive acceptance','Commissioning'],'source_owner':'Locomotive chat; separate coach chat owns cars','shared_program_file_edited':False,'background_task_created':False,'approved_for_fabrication':False,'next':basis['next_work']})
print(json.dumps({'created_issue':basis['issue'],'speed_mph':speed/.44704,'force_kN':force/1000,'curve30':curves[1]}))

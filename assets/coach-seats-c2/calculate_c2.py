"""Traceable preliminary load/fit screens; not a seat or attachment certification."""
from pathlib import Path
import json,math
H=Path(__file__).resolve().parent
P=json.loads((H/'parameters.json').read_text());V=json.loads((H/'verification.json').read_text())
g=9.80665;inch=.0254;lbf=4.4482216152605
metal=sum(V['mass_per_bench_kg_by_group'].values());mass=355 # 2 x145 kg occupants +65 kg seat assembly allowance
Fx=mass*g;Fz=mass*g*1.5;Fy=mass*g*.5
rows=[]
for name,xforce,yforce,zforce,height in [('analyst inertia',Fx,Fy,Fz,30),('comparison backrest forward',600*lbf,0,0,34.75),('comparison backrest reverse',-600*lbf,0,0,34.75)]:
 Mx=yforce*height*inch;My=xforce*height*inch
 # Equal-stiffness rigid-footprint axial reaction distribution only, not local fixed-foot moments.
 reactions=[]
 for x in (-8,8):
  for y in (-12,12):reactions.append({'foot_xy_relative_in':[x,y],'N_N':zforce/4+My*x/(4*8**2*inch)+Mx*y/(4*12**2*inch)})
 rows.append({'case':name,'Fx_N':xforce,'Fy_N':yforce,'Fz_N':zforce,'load_height_above_sole_in':height,'Mx_Nm':Mx,'My_Nm':My,'ideal_axial_foot_reactions':reactions,'limit':'Rigid footprint equal axial stiffness only. Sign changes imply uplift. Local moment restraint and real stiffness are separate cases.'})
backforce=600*lbf;localH=backforce/2;localM=localH*(67-32.25)*inch
bolttension=localM/(1.75*inch*2)
cap_wing_b=1.75*inch;cap_t=.75*inch;cap_lever=1*inch
capstress=6*bolttension*cap_lever/(cap_wing_b*cap_t**2)/1e6
# Concurrent X/Y inertia: half of each total moment assigned to each rear foot.
# Symmetric four-bolt rigid plate sensitivity; no gravity or preload credit.
combinedMy=Fx*30*inch/2;combinedMx=Fy*30*inch/2
combinedBolt=combinedMy/(4*.875*inch)+combinedMx/(4*2*inch)
combinedStrip=6*combinedBolt*cap_lever/(cap_wing_b*cap_t**2)/1e6
# Fore-aft couple across cap transferred to two cheeks: also screen a short longitudinal plate lever.
bolt_area=.1419*inch**2;proof=120000*6894.757293168*bolt_area
railS=1.18*inch**3
frontP=450*lbf;frontM=frontP*(24*inch)/4
I15=.188*inch**4;S15=.251*inch**3;I2=.486*inch**4;S2=.486*inch**3
grip0=.75+P['spacer_length']+.75;grips=[grip0+2*t for t in (.097,.177)]
calcs={'issue':'PF-3O2-C2-R0','date':'2026-10-19','classification':'Designer-selected preliminary sizing and catalog comparisons; not approved load cases',
 'mass':{'occupants_kg_each':145,'occupants':2,'metal_bench_and_hardpoints_kg':metal,'allowance_complete_bench_kg':65,'allowance_remaining_kg':65-metal,
 'sixteen_metal_benches_kg':metal*16,'old_15kg_per_bench_allowance_rejected':True,'new_trial_complete_regular_seating_kg':1040,
 'note':'1040kg includes all hardpoints and65kg/bench analyst allowance; does not add the old I1hardpoints again. Reconcile whole-coach mass/CG and brake/propulsion/HVAC loads. 65kg is not a measured tare or completed BOM.'},
 'analyst_loads':{'g_m_s2':g,'mass_total_kg':mass,'vertical_g':1.5,'longitudinal_g':1,'lateral_g':.5,'force_height_above_sole_in':30,'load_combination':'Concurrent analytical sensitivity only; not a selected governing code combination'},
 'rigid_footprint_cases':rows,
 'comparison_backrest':{'source':'APTA PR-CS-S-016-99 Rev3.1 section3.1.1, comparison only','two_places_force_N':backforce,'application_z_in':67,
 'rear_fixed_foot_bound':{'horizontal_N_per_rear_foot':localH,'moment_Nm_per_rear_foot_at_sole_under':localM,'ideal_bolt_tension_N_each_in_tension_row':bolttension,'bolt_rows_X_spacing_in':1.75,'tension_bolts_each_row':2,
 'bolt_material_proof_force_N':proof,'demand_to_material_proof_ratio_no_prying':bolttension/proof,'twofold_demand_sensitivity_ratio':2*bolttension/proof,
 'cap_wing_strip_MPa':capstress,'strip_width_in':1.75,'strip_lever_in':1,'strip_thickness_in':.75,'strip_note':'Illustrative gross elastic strip; real effective width, two-way bending, holes, contact and prying NOT established. Not an allowable or joint pass.'},
 'rear_HSS_gross_stress_MPa':localH*(67-33)*inch/S2/1e6,'rear_HSS_ideal_cantilever_deflection_mm':localH*((67-33)*inch)**3/(3*200e9*I2)*1000,
 'note':'Both back-force signs; no occupant gravity credited to suppress uplift. Frame stiffness does not prove all force uses the full16in front/rear lever. Dynamic occupant protection and fatigue remain open.'},
 'combined_local_fixed_foot_sensitivity':{'source':'Analyst simultaneous inertia case; rear-only half sharing bound, not established stiffness distribution','My_Nm_per_rear_foot':combinedMy,'Mx_Nm_per_rear_foot':combinedMx,'bolt_x_offset_in':.875,'bolt_y_offset_in':2,'maximum_corner_tension_N':combinedBolt,'equation':'Tmax=My/(4*a)+Mx/(4*b), a=0.875in,b=2in; symmetric group, no gravity/preload credit','gross_cap_strip_MPa':combinedStrip,'strip_thickness_in':.75,'governs_among_screened_local_bolt_cases':True,'limit':'Not a complete force envelope or joint strength pass. Contact, prying, biaxial effective width, holes, welds, rail wall, fatigue and real frame/foot stiffness remain open.'},
 'comparison_front_edge':{'source':'APTA section3.1.3 comparison,450lbf/place on5x5in patches nearfrontedge',
 'total_N':2*frontP,'one_patch_N':frontP,'front_beam_single_patch_at_midspan_MPa':frontM/S15/1e6,
 'two_patches_collapsed_at_midspan_MPa_conservative_for_24in_simple_span':2*frontM/S15/1e6,
 'two_patch_deflection_mm':2*frontP*(24*inch)**3/(48*200e9*I15)*1000,
 'limit':'Ideal front rail simple support24in. Actual overhang, pan plate contact, patch coordinates, welds, uplift and all adjacent members must be tested/reviewed. Total-force coincidence does not make inertia case equivalent.'},
 'fit':{'old_floor_clearance_mm':0,'new_nominal_floor_clearance_mm':6.35,'cap_to_panel_nominal_edge_gap_mm':4.7625,
 'floor_gap_equation':'6.35mm minus measured adverse floor stack, spacer/sole/cap flatness and weld/loaded relative deflection must exceed engineer-selected minimum',
 'example_adverse_budget_mm':{'floor_stack':1.5,'support_stack':.5,'relative_deflection':1.5,'remaining':2.85,'status':'Allocated target only; not measured/accepted tolerance evidence'},
 'cap_nearest_crossmember_nominal_clearance_in':.25,'cheek_nearest_crossmember_nominal_clearance_in':.5,'sole_between_rows_clearance_in':11.5,
 'through_stack_without_washers_in':grip0,'grip_range_in_washer_limits_only':grips,'bolt_proposed_length_in':3.0,'ordinary_nut_nominal_height_in':.4375,
 'thread_protrusion_range_in':[3.0-grips[1]-.4375,3.0-grips[0]-.4375],
 'note':'Protrusion excludes bolt length/nut tolerances and locking-device changes. Use exact hardware drawing before final length/torque. Socket trial OD1.25in leaves.125in at cheek; exact socket profile and axial insertion access still require trial.'},
 'released':False,'required_next_checks':['Compare lighter braced seat frame and realistic joint stiffness before any further plate-thickness iteration; current metal leaves little complete-seat mass allowance','Seat-frame and foot joint stiffness/prying model including both signs and lateral load','Local cap/sole/cheek and HSS rail wall/corner/rail-end load transfer','Panel bolt groups, pan/back local plate bending, contact and foam/edge treatment','Weld group effective lengths, qualified process and fatigue','Positive fastener locking and exact grip/torque sequence','Thermal and loaded floor isolation, sealed nonstructural closeout','Full-size two-adult comfort and aisle/row egress trials','Complete mass/CG coordination and instrumented prototype proof/fatigue/retention acceptance']}
(H/'calculations.json').write_text(json.dumps(calcs,indent=2))
print(json.dumps({'metal_bench_kg':metal,'local_bolt_N':bolttension,'rear_post_MPa':calcs['comparison_backrest']['rear_HSS_gross_stress_MPa'],'cap_strip_MPa':capstress,'grip_in':grips}))

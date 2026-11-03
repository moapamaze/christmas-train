"""C3 preliminary mechanism screens. Units lbf, inch, psi unless tagged.

These are transparent statics and member screens, not a code design, fatigue
assessment, fit approval, or physical test. Re-run after geometry changes.
"""
from pathlib import Path
import json, math, csv

OUT = Path(__file__).parent
LBF_PER_KG = 2.20462262185
E = 29_000_000

def pin_screen(force, diameter, span=1.0):
    # Conservative center-point force between cheek bearing centroids.
    area=math.pi*diameter**2/4
    moment=force*span/4
    sigma=32*moment/(math.pi*diameter**3)
    tau=force/(2*area)
    return dict(force_lbf=force,diameter_in=diameter,
                cheek_centroid_span_in=span,bending_moment_lbf_in=moment,
                bending_stress_psi=sigma,double_shear_stress_psi=tau,
                von_mises_screen_psi=math.sqrt(sigma*sigma+3*tau*tau),
                min_yield_procurement_target_psi=90_000,
                limit="Point-force beam and nominal shear; excludes notch, hole clearance, wear, fatigue and impact.")

vertical=[]
for share in (.5,.75,1.0):
    load=450*share
    moment=load*18
    stop=moment/1.25
    hinge=stop-load
    vertical.append(dict(side_share=share,applied_front_force_lbf=load,
      cantilever_moment_lbf_in=moment,stop_force_lbf=stop,
      hinge_force_lbf=hinge,hinge_pin=pin_screen(hinge,.75),
      pin_bushing_projected_pressure_psi=hinge/(.75*.5),
      sector_bore_projected_bearing_psi=hinge/(1.0*.5),
      fixed_cheek_bearing_psi=hinge/(2*.75*.375),
      stop_nominal_contact_pressure_psi=stop/(.5*.5),
      side_frame_bending_psi=moment/.251,
      moving_tang_root_moment_lbf_in=load*(18-1.5625),
      old_1p5in_tang_bending_psi=load*(18-1.5625)/(.5*1.5**2/6),
      proposed_2in_tang_bending_psi=load*(18-1.5625)/(.5*2**2/6),
      side_frame_elastic_tip_deflection_in=load*18**3/(3*E*.188)))

stop_edge=[]
for arm in (1.0,1.25,1.5):
    stop=450*18/arm
    hinge=stop-450
    stop_edge.append(dict(effective_arm_in=arm,side_share=1.0,stop_force_lbf=stop,hinge_force_lbf=hinge,hinge_pin=pin_screen(hinge,.75),nominal_mean_pressure_full_land_psi=stop/.25,warning='Contact arm and area are not independent. Edge contact may have much higher local pressure than this hypothetical full-land mean; pressure and indentation are not validated.'))

locks=[]
for name,mass,g,lever in [
    ('stowed_pan_inertial_screen',20,3,9),
    ('deployed_captured_load_or_misuse_upward_screen',165,1.5,9)]:
    total_moment=mass*LBF_PER_KG*g*lever
    for share in (.5,.75,1.0):
        force=total_moment*share/1.15
        locks.append(dict(case=name,mass_kg=mass,analyst_acceleration_g=g,
          CG_lever_in=lever,side_share=share,lock_radius_in=1.15,
          lock_tangential_force_lbf=force,
          half_inch_pin=pin_screen(force,.5),
          five_eighth_inch_pin=pin_screen(force,.625),
          five_eighth_moving_lug_bearing_psi=force/(.625*.5),
          radial_edge_ligament_in=1.75-1.15-.65625/2,
          simple_two_plane_edge_shear_psi=force/(2*(1.75-1.15-.65625/2)*.5)))

cad_mass=13.149250960892617
cad_cg_x=71.5054854343195
cad_cg_z=48.04398298306847
cad_dx=cad_cg_x-64
cad_dz=cad_cg_z-48.5
cad_radial=math.hypot(cad_dx,cad_dz)

support_mass=210
W=support_mass*LBF_PER_KG
my=W*30+(1.5*W)*9.5
mx=.5*W*30
support=dict(mass_kg=support_mass,occupant_kg=145,assembly_allowance_kg=65,
    horizontal_force_X_lbf=W,horizontal_force_Y_lbf=.5*W,
    vertical_down_force_lbf=1.5*W,force_height_above_sole_in=30,
    vertical_CG_X_in=72,sole_center_X_in=62.5,sole_datum_Z_in=32.25,
    total_pitch_moment_lbf_in=my,total_roll_moment_lbf_in=mx,
    equal_share_pitch_per_foot_lbf_in=my/2,
    equal_share_roll_per_foot_lbf_in=mx/2,
    bolt_pattern_in=[3.5,4.0],
    foundation_reference='foundation-screen.json owns final bolt/contact demands. Older duplicated3336/1885lbf handoffs are withdrawn after bolt-pitch and foot-position updates.',
    warning="Handoff only. Independent foundation analysis owns foot load distribution, prying, contact, plate/rail/weld checks. Roll can redistribute into axial reactions across the two feet. C2.1 braced reactions do not apply.")

result=dict(revision='PF-3O2-C3-MECH-R0',status='PROPOSED ENGINEERING SCREEN; NOT FOR FABRICATION',
    units='lbf, inch, psi unless explicitly tagged',
    assumptions=dict(front_load_lbf=450,front_lever_from_hinge_in=18,
      stop_effective_arm_in=1.25,stop_contact_land_in=[.5,.5],
      hinge_diameter_in=.75,sector_bore_diameter_in=1.0,
      bronze_bushing_OD_in=1.0,bronze_bushing_ID_in=.753,
      moving_sector_thickness_in=.5,
      fixed_cheek_thickness_each_in=.375,running_gap_each_in=.0625,
      fixed_cheek_centroid_span_in=1.0,sector_radius_in=1.75,
      lock_circle_radius_in=1.15,recommended_lock_diameter_in=.625,
      proposed_lock_hole_diameter_in=.65625,moving_tang_depth_in=2.0,moving_tang_start_from_hinge_in=1.5625,
      pin_minimum_yield_target_psi=90000,A36_plate_yield_comparison_psi=36000,
      HSS_A500_Grade_C_yield_comparison_psi=50000,
      side_frame_HSS='1.5 x 1.5 x nominal 1/8, Atlas A500 catalog I=.188 in^4, S=.251 in^3',
      mass_notice='20kg moving pan and 65kg whole assembly are allowances, not CAD masses.',
      upward_load_notice='Unrestrained occupants do not normally pull a pan upward after contact is lost. The 165kg upward case is a deliberately assumed captured-load/misuse envelope, not a predicted occupant load or restraint design.'),
    front_edge_cases=vertical,stop_contact_arm_sensitivity=stop_edge,lock_cases=locks,foundation_handoff=support,
    cad_mass_reconciliation=dict(physical_metal_kg=54.05593160109914,
      moving_metal_kg=12.62579948763637,moving_with_placeholder_padding_kg=cad_mass,
      moving_CG_deployed_in=[cad_cg_x,-32,cad_cg_z],
      whole_assembly_allowance_kg=65,moving_assembly_allowance_kg=20,
      whole_remaining_allowance_kg=65-54.05593160109914,
      moving_remaining_allowance_kg=20-cad_mass,
      note='CAD mass excludes unspecified retention, welds, finish and final upholstery properties; padding modeled with assumed density.'),
    handling=dict(cad_nominal_deployed_tangential_hand_force_lbf=cad_mass*LBF_PER_KG*cad_dx/18,
      cad_peak_tangential_hand_force_lbf=cad_mass*LBF_PER_KG*cad_radial/18,
      cad_peak_angle_deg=math.degrees(math.atan2(-cad_dz,cad_dx)),
      cad_gravity_energy_change_J=cad_mass*9.80665*(cad_dx-cad_dz)*.0254,
      hand_force_basis='Force perpendicular to an18in radius; gravity only, friction/pin binding/guard drag excluded.',
      moving_mass_allowance_kg=20,CG_lever_in=9,hand_lever_in=18,
      worst_horizontal_hand_force_lbf=20*LBF_PER_KG*9/18,
      max_gravitational_energy_J=20*9.80665*9*.0254,
      note='No gas spring, damper or automatic return selected. Crew must control travel; effort and access need full-size verification.'),
    conclusions=[
      'Near-edge stop arm1.0in raises the one-side hinge nominal combined stress to48.5ksi; pressure/contact requires separate verification and is not passed by this screen.',
      'Keep a separate metal bearing stop for deployed occupant load; lock pins prevent rotation and do not substitute for the normal downward bearing stop.',
      'Screen 50%, 75% and 100% one-side loading. The 100% case is an asymmetry bound for these local parts; the complete seat frame load path is not solved.',
      '3/4in hinge pin has38.3ksi nominal combined stress in the one-sided 450lbf screen. Require a specified certified pin material; generic ungraded pin substitution is not acceptable.',
      'Recommend 5/8in positive pins because the analyst one-pin upward screen increases 1/2in pin bending substantially.',
      'The 1.5in HSS rail screen uses its full 18in cantilever and does not credit pan or opposite-side rail sharing.',
      'Tang increased from1.5to2.0in depth after one-side450lbf gross bending changed from39.5to22.2ksi; transition/weld verification still required.',
      'Local sector/tang transition, weld groups, cheek net sections, contact indentation, fixed-post torsion and base joint flexibility remain to be solved.',
      'Bronze bushing grade, operating fit, pressure/wear and lubrication limits remain unspecified; projected pressure is not a bushing acceptance check.',
      'Material-yield comparisons are not allowable passenger-seat loads or evidence of compliance.'
    ])
(OUT/'mechanism-calculations.json').write_text(json.dumps(result,indent=2)+'\n')
with (OUT/'mechanism-load-screen.csv').open('w',newline='') as f:
    cols=['side_share','applied_front_force_lbf','stop_force_lbf','hinge_force_lbf','pin_bushing_projected_pressure_psi','fixed_cheek_bearing_psi','stop_nominal_contact_pressure_psi','side_frame_bending_psi','side_frame_elastic_tip_deflection_in']
    w=csv.DictWriter(f,cols);w.writeheader()
    for row in vertical:w.writerow({c:row[c] for c in cols})

# Verification: moment equilibrium, force equilibrium and correct quadratic /
# cubic diameter scaling. These tests address calculation failure, not the design.
checks=[]
for c in vertical:
    checks += [abs(c['stop_force_lbf']*1.25-c['applied_front_force_lbf']*18)<1e-8,
               abs(c['stop_force_lbf']-c['hinge_force_lbf']-c['applied_front_force_lbf'])<1e-8]
checks.append(abs(pin_screen(100,.5)['bending_stress_psi']/pin_screen(100,1)['bending_stress_psi']-8)<1e-10)
checks.append(abs(pin_screen(100,.5)['double_shear_stress_psi']/pin_screen(100,1)['double_shear_stress_psi']-4)<1e-10)
assert all(checks)
(OUT/'calculation-verification.json').write_text(json.dumps({'checks_passed':len(checks),'scope':'Statics equilibrium and diameter scaling only; no physical validation.'},indent=2)+'\n')
print(json.dumps({'front_case_100pct':vertical[-1],'critical_lock_case':locks[-1],'foundation_handoff':support,'checks_passed':len(checks)},indent=2))

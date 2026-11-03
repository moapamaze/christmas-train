from pathlib import Path
import hashlib,json,math
P=Path(__file__).resolve().parent;D=P.parent.parent
I=json.loads((P/'inputs-and-sources.json').read_text());B=json.loads((D/'assets/propulsion-n1/inputs.json').read_text());H=json.loads((D/'assets/propulsion-n1/calculations.json').read_text())
m=I['comparison_mass_kg'];g=B['g_m_s2'];R=B['wheel_diameter_mm']/2000
running=m*g*I['running_coefficient']+I['extra_resistance_N'];start=m*g*I['starting_coefficient']+I['extra_resistance_N']
eel=math.prod(I['electric_efficiency_probes'].values());modes=[('hydrostatic inherited constant efficiencies',H['shaft_to_wheel_efficiency'])]+[(f'locked mechanical assumed{e:.2f}',e) for e in I['mechanical_locked_efficiency_probes']]+[('diesel-electric assumed chain',eel)]
power=[]
for name,eff in modes:
 for mph in I['speed_probes_mph']:
  v=mph*.44704;wheel=running*v/1000
  power.append({'mode':name,'speed_mph':mph,'wheel_power_kW':wheel,'assumed_efficiency':eff,'main_drive_shaft_kW':wheel/eff,'engine_with_normalized_aux_kW':wheel/eff+I['shared_auxiliary_normalization_kW'],'meaning':'Normalization, not actual package selection, efficiency or fuel performance.'})
rpmwheel=7.5*.44704/(2*math.pi*R)*60
ratio_e=I['electric_gearing_probe']['motor_base_rpm']/rpmwheel
gear=I['electric_gearing_probe']['gear_efficiency']
electric={'ratio_matched_to_catalog_base_speed_trial':ratio_e,'catalog_rated_torque_wheel_force_proxy_N':78.6*ratio_e*gear/R,'catalog_peak_torque_wheel_force_proxy_N':173*ratio_e*gear/R,'required_steady_motor_torque_at_7p5_Nm':running*R/(ratio_e*gear),'required_breakaway_plus_0p1_motor_torque_Nm':(start+m*.1)*R/(ratio_e*gear),'motor_rpm_at_0p25mph':6500*.25/7.5,'not_verified':'Catalog rated torque is not accepted standstill/low-speed torque or a complete system capability. Peak duration and inverter current/thermal duty unknown.'}
electric['gross_engine_budget_limited_wheel_kW']=45.4*eel
electric['gross_engine_budget_limited_force_at_7p5_N']=45.4*eel*1000/(7.5*.44704)
electric['not_verified']+=' Peak torque cannot be combined with rated speed. The engine/generator chain limits system power below the motor nameplate.'
main55=B['engine_budget_trials_kW'][-1]-B['traction_auxiliary_allowance_kW'];engine_torque=main55*1000/(2*math.pi*2600/60)
ratio_m=2600/rpmwheel
required_launch=start+m*.1
mechanical={'engine_main_shaft_allocation_kW':main55,'engine_speed_point_rpm':2600,'mean_main_shaft_torque_proxy_Nm':engine_torque,'total_ratio_for_7p5mph_at2600rpm':ratio_m,'force_proxy_with_gear_eff_0p95_N':engine_torque*ratio_m*.95/R,'required_total_ratio_for_0p1_launch_proxy':required_launch*R/(engine_torque*.95),'note':'Rigid speed/torque comparison only. A fixed coupled ratio cannot launch from zero without a clutch/converter or other launch device; no clutch slipping or converter map modeled.'}
v=7.5*.44704
energy={'speed_mph':7.5,'translational_energy_kJ':.5*m*v*v/1000,'energy_kWh':.5*m*v*v/3.6e6,'rotating_inertia_included':False,'regeneration_credit':0,'note':'Stored kinetic energy, not a braking resistor/battery rating. Independent air brakes retained. Dump/battery capacity, peak electrical power and repeat duty unresolved.'}
for k in power:assert abs(k['main_drive_shaft_kW']*k['assumed_efficiency']-k['wheel_power_kW'])<1e-10
assert electric['catalog_rated_torque_wheel_force_proxy_N']>required_launch
out={'issue':I['issue'],'date_utc':I['checked_utc'],'basis_input_sha256':hashlib.sha256((D/'assets/propulsion-n1/inputs.json').read_bytes()).hexdigest(),'comparison_power_cases':power,'electric_chain_assumed_efficiency':eel,'electric_gearing_comparison':electric,'mechanical_gearing_comparison':mechanical,'kinetic_energy':energy,'selected_final_drive':None,'fabrication_release':False}
(P/'calculations.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n');print(json.dumps(out,indent=2))

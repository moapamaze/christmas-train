"""Independent closed-form fixtures, force-space solution and invariants.

These validate algebra/numerics, NOT rail safety or a physical design.
"""
from pathlib import Path
import copy,hashlib,json,math,sys
import numpy as np
sys.dont_write_bytecode=True
from equilibrium import solve,InputError
P=Path(__file__).resolve().parent;raw=json.loads((P/'synthetic-fixtures.json').read_text());fixtures={f['id']:f for f in raw['fixtures']};checks=[]
def check(name,condition):
 if not condition:raise AssertionError(name)
 checks.append(name)
def close(name,got,expected):check(name,bool(np.allclose(got,expected,rtol=1e-10,atol=1e-7)))
r={name:solve(f) for name,f in fixtures.items()}
expected={
 'flat':([10000]*4,[12000]*4,[-.1,0,0,0]),
 'affine-plane':([10000]*4,[12000]*4,[-.07,.01,.02,0]),
 'diagonal-rigid':([8000,12000,12000,8000],[9000,15000,15000,9000],[-.1,0,0,0]),
 'diagonal-eta1':([9000,11000,11000,9000],[10500,13500,13500,10500],[-.1,0,0,.01]),
 'diagonal-free-warp-limit':([10000]*4,[12000]*4,[-.1,0,0,.02]),
 'crosslevel-roll-restraint':([10750,9250,10750,9250],[13125,10875,13125,10875],[-.1,0,.01,0]),
 'offset-downward-load':([34000/3,26000/3]*2,[14000,10000]*2,[-.1,0,-.017777777777777778,0]),
 'diagonal-with-roll-restraint':([8000,12000,12000,8000],[9000,15000,15000,9000],[-.1,0,0,0]),
 'contact-loss-diagnostic':([1000,19000,19000,1000],[-1500,25500,25500,-1500],[-.01,0,0,0]),
 'one-rail-contact-raised':([10750,9250,9250,10750],[13125,10875,10875,13125],[-.095,-.005,.01,0])}
for name,(F,Q,q) in expected.items():
 close(name+' independent spring force',r[name]['corner_spring_forces_N'],F)
 close(name+' independent wheel reaction',r[name]['wheel_vertical_reactions_N'],Q)
 close(name+' independent frame displacement',list(r[name]['frame_displacements'].values()),q)
 close(name+' generalized equilibrium',r[name]['normalized_generalized_balance_residual_N'],0)
 close(name+' global force/moment',list(r[name]['global_balance_residual'].values()),0)
 for a in r[name]['axle_balances']:
  close(name+' '+a['axle']+' force balance',a['vertical_balance_residual_N'],0)
  close(name+' '+a['axle']+' moment balance',a['roll_balance_residual_Nm'],0)
 check(name+' no false rail/fabrication/operation approval',r[name]['approved_for_fabrication'] is False and r[name]['approved_for_operation'] is False and r[name]['vehicle_roll_stability_assessed'] is False)
check('Contact diagnostic: positiveF but negativeQ',min(r['contact-loss-diagnostic']['corner_spring_forces_N'])>0 and min(r['contact-loss-diagnostic']['wheel_vertical_reactions_N'])<0)
check('Contact diagnostic invalid notclamped',r['contact-loss-diagnostic']['active_contact_assumption_valid'] is False and r['contact-loss-diagnostic']['negative_or_zero_values_clamped'] is False)
close('Body roll restraint cannot cure pure diagonal warp',r['diagonal-with-roll-restraint']['wheel_vertical_reactions_N'],r['diagonal-rigid']['wheel_vertical_reactions_N'])
close('Exact roll boundary moment',r['crosslevel-roll-restraint']['body_roll_boundary_moment_Nm'],2250)

# A different solution route: equilibrium fixes force components F0; compatibility
# determines its remaining diagonal scalar t. No matrix solve is used here.
rng=np.random.default_rng(73192);xs=np.array([-1,-1,1,1]);ys=np.array([1,-1,1,-1]);ss=xs*ys
for n in range(36):
 f=copy.deepcopy(fixtures['flat']);k=rng.uniform(70000,140000,4);f['corner_rates_N_per_m']=k.tolist()
 for axle in ['front','rear']:
  f['rail_heights_m'][axle]={side:float(rng.uniform(-.006,.006)) for side in ['left','right']}
 for load in f['sprung_loads']:load['x_m']=float(rng.uniform(-.05,.05));load['y_m']=float(rng.uniform(-.05,.05))
 f['extra_downward_slope_moments_Nm']=dict(pitch=float(rng.uniform(-100,100)),roll=float(rng.uniform(-100,100)))
 if n%3:
  f['constraints'].update(frame_warp='single_compliant_mode',warp_K_N_per_m=0 if n%3==1 else float(rng.uniform(10000,900000)))
 for axle in ['front','rear']:
  f['unsprung_axle_loads'][axle]['cg_y_m']=float(rng.uniform(-.03,.03))
  f['unsprung_axle_loads'][axle]['additional_downward_roll_moment_Nm']=float(rng.uniform(-30,30))
 got=solve(f);a=f['geometry']['axle_half_spacing_m'];bs=f['geometry']['spring_half_span_m'];bw=f['geometry']['wheel_contact_half_span_m']
 W=sum(t['vertical_down_N'] for t in f['sprung_loads']);fp=(sum(t['vertical_down_N']*t['x_m'] for t in f['sprung_loads'])+f['extra_downward_slope_moments_Nm']['pitch'])/a;fr=(sum(t['vertical_down_N']*t['y_m'] for t in f['sprung_loads'])+f['extra_downward_slope_moments_Nm']['roll'])/bs
 F0=(W+xs*fp+ys*fr)/4
 u=[]
 for ax in ['front','rear']:
  h=f['rail_heights_m'][ax];mean=(h['left']+h['right'])/2;dh=h['right']-h['left'];u.extend([mean+bs*dh/(2*bw),mean-bs*dh/(2*bw)])
 numerator=np.dot(ss,u)-np.dot(ss,F0/k)
 if f['constraints']['frame_warp']=='rigid':t=numerator/np.sum(1/k)
 elif f['constraints']['warp_K_N_per_m']==0:t=0
 else:t=numerator/(np.sum(1/k)+16/f['constraints']['warp_K_N_per_m'])
 Fcheck=F0+ss*t
 close('Force-space independent solution'+str(n),got['corner_spring_forces_N'],Fcheck)
 close('Randomglobal'+str(n),list(got['global_balance_residual'].values()),0)
 check('Randomactivecontact'+str(n),got['active_contact_assumption_valid'])
 # Shift all rail elevations: only heave changes.
 shifted=copy.deepcopy(f)
 for ax in shifted['rail_heights_m']:
  for side in shifted['rail_heights_m'][ax]:shifted['rail_heights_m'][ax][side]+=.04
 rs=solve(shifted);close('Uniformelevationforces'+str(n),rs['wheel_vertical_reactions_N'],got['wheel_vertical_reactions_N'])
 close('Uniformelevationheave'+str(n),rs['frame_displacements']['heave_compression_datum_m']-got['frame_displacements']['heave_compression_datum_m'],.04)
 # Reflection in y reverses left/right, load eccentricity and warp/roll signs.
 mirrored=copy.deepcopy(f);mirrored['corner_rates_N_per_m']=[f['corner_rates_N_per_m'][i] for i in [1,0,3,2]]
 for ax in mirrored['rail_heights_m']:
  h=f['rail_heights_m'][ax];mirrored['rail_heights_m'][ax]=dict(left=h['right'],right=h['left'])
  mirrored['unsprung_axle_loads'][ax]['cg_y_m']*=-1;mirrored['unsprung_axle_loads'][ax]['additional_downward_roll_moment_Nm']*=-1
 for l in mirrored['sprung_loads']:l['y_m']*=-1
 mirrored['extra_downward_slope_moments_Nm']['roll']*=-1;mirrored['constraints']['body_roll_reference_slope']*=-1
 rm=solve(mirrored);close('Mirrorwheel'+str(n),rm['wheel_vertical_reactions_N'],[got['wheel_vertical_reactions_N'][i] for i in [1,0,3,2]])
 close('Mirrorroll'+str(n),rm['frame_displacements']['roll_elevation_slope'],-got['frame_displacements']['roll_elevation_slope'])

bad=[]
for val in [0,-1,math.nan,math.inf,True,None,10**400]:
 f=copy.deepcopy(fixtures['flat']);f['corner_rates_N_per_m'][0]=val;bad.append(('rate'+str(val)[:12],f))
for key,val in [('axle_half_spacing_m',0),('spring_half_span_m',-1),('wheel_contact_half_span_m',None)]:
 f=copy.deepcopy(fixtures['flat']);f['geometry'][key]=val;bad.append((key,f))
f=copy.deepcopy(fixtures['flat']);f['units']='mm_N';bad.append(('mmunits',f))
f=copy.deepcopy(fixtures['flat']);f['geometry']['nominal_gauge_m']=.9144;bad.append(('gaugeisspan',f))
for c in [dict(frame_warp='rigid',warp_K_N_per_m=1),dict(frame_warp='single_compliant_mode',warp_K_N_per_m=None),dict(frame_warp='single_compliant_mode',warp_K_N_per_m=-1),dict(body_roll_K_Nm_per_rad=-1),dict(body_roll_K_Nm_per_rad=1e30)]:
 f=copy.deepcopy(fixtures['flat']);f['constraints'].update(c);bad.append(('constraint'+str(c),f))
f=copy.deepcopy(fixtures['flat']);f['corner_rates_N_per_m']=[1,2,3];bad.append(('ratelen',f))
f=copy.deepcopy(fixtures['flat']);f['rail_heights_m']['front']={'left':0,'right':1e308};f['rail_heights_m']['rear']={'left':1e308,'right':1e308};bad.append(('derivedoverflow',f))
for name,f in bad:
 rejected=False
 try:
  with np.errstate(over='ignore',invalid='ignore',divide='ignore'):solve(f)
 except (InputError,KeyError):rejected=True
 check('Rejected '+name,rejected)

report=dict(issue=raw['issue'],check_count=len(checks),checks_passed=checks,engine_sha256=hashlib.sha256((P/'equilibrium.py').read_bytes()).hexdigest(),fixtures_sha256=hashlib.sha256((P/'synthetic-fixtures.json').read_bytes()).hexdigest(),validation='10 independent closed-form fixtures;36unequal-rate/offset/moment force-space solutions; elevation and mirror invariants; each axle/global equilibrium; invalid-input/contact diagnostics.',numerical_comparison_tolerances=dict(relative=1e-10,absolute=1e-7,meaning='Floating point comparison only, NOT a physical safety or inspection tolerance.'),no_project_hardware_selected=True,actual_physical_tests=False)
(P/'analytical-test-results.json').write_text(json.dumps(report,indent=2)+'\n')
print(f'Passed {len(checks)} independent analytic/numerical checks. No rail acceptance or actual test result.')

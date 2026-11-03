"""Independent analytical checks; synthetic constants, NOT hardware acceptance."""
from pathlib import Path
import copy,hashlib,json,math,random,sys
sys.dont_write_bytecode=True
from sidebearer_equilibrium import solve_support,InputError
P=Path(__file__).resolve().parent
fixtures=json.loads((P/'synthetic-support-fixtures.json').read_text())['fixtures']
checks=[]
def check(name,condition):
    if not condition:raise AssertionError(name)
    checks.append(name)
def close(name,actual,expected):
    check(name,math.isclose(actual,expected,rel_tol=1e-9,abs_tol=1e-7))
expected=[(0,0,0,30000),(.005,0,0,30000),(.01,0,0,30000),(.015,2250,0,27750),(-.015,0,2250,27750),(.01,4500,0,25500),(.015,2250,0,-250),(.025,2250,0,27750),(0,0,0,30000),(.012,3600,0,26400),(-.018,0,900,29100),(0,0,0,30000),(.015,2250,0,0)]
for f,e in zip(fixtures,expected):
    r=solve_support(f);t=r['truck_equilibrium'];name=f['id']
    for key,actual,want in zip(['roll','right','left','center'],[t['frame_displacements']['roll_elevation_slope'],r['sidebearer_right_down_on_truck_N'],r['sidebearer_left_down_on_truck_N'],r['center_bearing_vertical_N']],e):close(name+' '+key,actual,want)
    close(name+' vertical body balance',r['body_vertical_balance_residual_N'],0)
    close(name+' side law moment',r['constitutive_moment_residual_Nm'],0)
    total=sum(x['vertical_down_N'] for x in f['truck']['sprung_loads'])+sum(x['vertical_down_N'] for x in f['truck']['unsprung_axle_loads'].values())
    close(name+' body force counted once',sum(t['wheel_vertical_reactions_N']),total)
    close(name+' external body moment',r['required_external_body_roll_moment_about_x_Nm'],-r['sidebearer_downward_roll_moment_on_truck_Nm'])
    check(name+' one physical root',r['distinct_physical_root_count']==1)
    check(name+' no approval or clamping',not r['approved_for_fabrication'] and not r['approved_for_operation'] and not r['center_or_wheel_negative_values_clamped'])
    if name.startswith('center-'):
        check(name+' invalid center with positive wheels',not r['center_contact_assumption_valid'] and min(t['wheel_vertical_reactions_N'])>0)
    if name=='exact-onset':check('Onset labels deduplicated',r['consistent_branch_label_count']==2)
    if name=='zero-gap-flat-boundary':check('Four zero-force labels deduplicated',r['consistent_branch_label_count']==4)
    if name=='diagonal-open-gap':
        for i,q in enumerate([9000,15000,15000,9000]):close('Diagonal wheel '+str(i),t['wheel_vertical_reactions_N'][i],q)

# Independent scalar monotonic moment equation, not active-set branch enumeration.
rng=random.Random(20261019)
for i in range(60):
    f=copy.deepcopy(fixtures[0]);gamma=rng.uniform(-.05,.05);bodyroll=rng.uniform(-.02,.02)
    f['sidebearers']['body_reference_slope']=bodyroll
    for axle in f['truck']['rail_heights_m'].values():axle.update(left=-.5*gamma,right=.5*gamma)
    for side in ['right','left']:
        f['sidebearers'][side]=dict(half_span_m=rng.uniform(.3,.9),gap_m=rng.uniform(0,.012),rate_N_per_m=rng.uniform(1e5,2e6))
    R=f['sidebearers']['right'];L=f['sidebearers']['left'];Kprimary=4*100000*.75**2
    def residual(phi):
        return Kprimary*(gamma-phi)-R['half_span_m']*R['rate_N_per_m']*max(R['half_span_m']*(phi-bodyroll)-R['gap_m'],0)+L['half_span_m']*L['rate_N_per_m']*max(-L['half_span_m']*(phi-bodyroll)-L['gap_m'],0)
    lo,hi=-1.,1.
    check(f'Independent bracket {i}',residual(lo)>0 and residual(hi)<0)
    for _ in range(90):
        mid=(lo+hi)/2
        if residual(mid)>0:lo=mid
        else:hi=mid
    r=solve_support(f);phi=r['truck_equilibrium']['frame_displacements']['roll_elevation_slope']
    close(f'Independent scalar root {i}',phi,(lo+hi)/2)
    close(f'Independent scalar moment {i}',residual(phi),0)

mutations=[('negative gap',lambda f:f['sidebearers']['right'].update(gap_m=-.001)),('zero rate',lambda f:f['sidebearers']['left'].update(rate_N_per_m=0)),('zero halfspan',lambda f:f['sidebearers']['right'].update(half_span_m=0)),('missing body',lambda f:f['sidebearers'].update(body_load_id='absent')),('offcenter body',lambda f:f['truck']['sprung_loads'][0].update(y_m=.01)),('base roll conflict',lambda f:f['truck']['constraints'].update(body_roll_K_Nm_per_rad=1)),('units',lambda f:f.update(units='inch')),('bool rate',lambda f:f['sidebearers']['right'].update(rate_N_per_m=True)),('NaN gap',lambda f:f['sidebearers']['right'].update(gap_m=float('nan'))),('Inf body roll',lambda f:f['sidebearers'].update(body_reference_slope=float('inf')))]
for name,mutate in mutations:
    f=copy.deepcopy(fixtures[0]);mutate(f)
    try:solve_support(f)
    except (InputError,KeyError,TypeError):check('Rejected '+name,True)
    else:check('Rejected '+name,False)
out=dict(issue='PF-3L3-S3-SUPPORT-R0',check_count=len(checks),checks_passed=checks,wrapper_sha256=hashlib.sha256((P/'sidebearer_equilibrium.py').read_bytes()).hexdigest(),base_engine_sha256=hashlib.sha256((P.parent/'truck-twist-l3s2/equilibrium.py').read_bytes()).hexdigest(),fixtures_sha256=hashlib.sha256((P/'synthetic-support-fixtures.json').read_bytes()).hexdigest(),scope='13 analytical fixtures,60 independent scalar roots and invalid inputs; no actual hardware/physical test or safety acceptance.')
(P/'analytical-test-results.json').write_text(json.dumps(out,indent=2)+'\n')
print('Passed',len(checks),'analytical checks; no project support selected.')

"""Frictionless gapped sidebearer/center-support study; NOT a selected design.

Requires Python3/NumPy and the preserved3L.3-S2 equilibrium.py. Retain the Site
source directory layout (or put equilibrium.py beside this file). Bodyroll is
externally prescribed; this does NOT solve whole-coach/other-truck equilibrium.
"""
from pathlib import Path
import argparse,copy,itertools,json,math,sys
sys.dont_write_bytecode=True
sys.path.append(str(Path(__file__).resolve().parent.parent/'truck-twist-l3s2'))
from equilibrium import solve,number,fields,InputError

def solve_support(data):
    if data.get('units')!='SI_m_N':raise InputError('Sidebearer wrapper units must be SI_m_N')
    base=data['truck'];law=data['sidebearers']
    fields(law,['body_load_id','body_reference_slope','right','left'],'sidebearers')
    if number(base['constraints']['body_roll_K_Nm_per_rad'],'base artificial roll K')!=0 or number(base['constraints']['body_roll_reference_slope'],'base artificial roll reference')!=0:
        raise InputError('Remove artificial base roll restraint/reference before substituting the explicit sidebearer law')
    bodyloads=[r for r in base['sprung_loads'] if r['id']==law['body_load_id']]
    if len(bodyloads)!=1:raise InputError('Exactly one explicit body reaction load ID required')
    body=bodyloads[0]
    if body['x_m']!=0 or body['y_m']!=0:raise InputError('This model requires the prescribed body reaction at the ideal center support x=y0')
    Wbody=number(body['vertical_down_N'],'body reaction',positive=True)
    phibody=number(law['body_reference_slope'],'prescribed body roll')
    side={}
    for label in ['right','left']:
        v=law[label];fields(v,['half_span_m','gap_m','rate_N_per_m'],label+' sidebearer')
        side[label]=dict(b=number(v['half_span_m'],label+' halfspan',positive=True),g=number(v['gap_m'],label+' gap',nonnegative=True),k=number(v['rate_N_per_m'],label+' rate',positive=True))
    roots=[];attempts=[]
    # Four branch equations. At exact onset several labels can denote the SAME
    # zero-force physical solution; roots are deduplicated, not called ambiguous.
    for ar,al in itertools.product([False,True],repeat=2):
        R=side['right'];L=side['left']
        K=(R['k']*R['b']**2 if ar else 0)+(L['k']*L['b']**2 if al else 0)
        offset=(R['k']*R['b']*R['g'] if ar else 0)-(L['k']*L['b']*L['g'] if al else 0)
        equivalent_ref=phibody+offset/K if K else phibody
        f=copy.deepcopy(base);f['constraints'].update(body_roll_K_Nm_per_rad=K,body_roll_reference_slope=equivalent_ref)
        result=solve(f);phi=result['frame_displacements']['roll_elevation_slope'];relative=phi-phibody
        dr=R['b']*relative-R['g'];dl=-L['b']*relative-L['g']
        # Tolerance ONLY handles floating-point branch-boundary classification.
        # max(delta,0) is the DEFINED unilateral sidebearer law, never wheel-Q clamping.
        tolerance_m=1e-12
        consistent=(dr>=-tolerance_m if ar else dr<=tolerance_m) and (dl>=-tolerance_m if al else dl<=tolerance_m)
        Fr=R['k']*max(dr,0);Fl=L['k']*max(dl,0);moment=R['b']*Fr-L['b']*Fl
        mismatch=result['body_roll_boundary_moment_Nm']-moment
        scale=max(Wbody*max(R['b'],L['b']),1.)
        consistent=bool(consistent and math.isfinite(mismatch) and abs(mismatch)<=1e-9*scale)
        attempt=dict(assumed_right_active=ar,assumed_left_active=al,gap_consistent=consistent,raw_compression_right_m=dr,raw_compression_left_m=dl,equivalent_roll_K_Nm_per_rad=K,equivalent_roll_reference_slope=equivalent_ref,constitutive_moment_mismatch_Nm=mismatch)
        attempts.append(attempt)
        if consistent:roots.append(dict(truck=result,force_right_N=Fr,force_left_N=Fl,side_moment_Nm=moment,attempt=attempt))
    if not roots:raise InputError('No consistent sidebearer branch; numerical/model assumptions need review')
    physical=[]
    for r in roots:
        phi=r['truck']['frame_displacements']['roll_elevation_slope']
        duplicate=any(abs(phi-t['truck']['frame_displacements']['roll_elevation_slope'])<=1e-11 and abs(r['force_right_N']-t['force_right_N'])<=1e-6 and abs(r['force_left_N']-t['force_left_N'])<=1e-6 and all(abs(q1-q2)<=1e-6 for q1,q2 in zip(r['truck']['wheel_vertical_reactions_N'],t['truck']['wheel_vertical_reactions_N'])) for t in physical)
        if not duplicate:physical.append(r)
    if len(physical)!=1:raise InputError('Multiple distinct physical roots; do not choose one silently')
    root=physical[0];Fr=root['force_right_N'];Fl=root['force_left_N'];center=Wbody-Fr-Fl
    if not all(math.isfinite(v) for v in [Fr,Fl,center,root['side_moment_Nm']]):raise InputError('Nonfinite support result')
    center_resolution=1e-10*max(Wbody,Fr+Fl,1.)
    center_positive=center>center_resolution
    valid=bool(center_positive and root['truck']['active_contact_assumption_valid'])
    return dict(id=data.get('id'),units='SI_m_N',model='ideal maintained center contact + frictionless no-preload gapped sidebearers; externally prescribed bodyroll',
        truck_equilibrium=root['truck'],sidebearer_right_down_on_truck_N=Fr,sidebearer_left_down_on_truck_N=Fl,
        prescribed_body_vertical_down_N=Wbody,center_bearing_vertical_N=center,
        body_vertical_balance_residual_N=center+Fr+Fl-Wbody,
        sidebearer_downward_roll_moment_on_truck_Nm=root['side_moment_Nm'],
        required_external_body_roll_moment_about_x_Nm=-root['side_moment_Nm'],
        external_body_reaction_meaning='Opposes the upward sidebearer moment acting on the prescribed body. Its source/other truck/body torsion is NOT solved or designed here.',
        active_set_attempts=attempts,consistent_branch_label_count=len(roots),distinct_physical_root_count=len(physical),
        constitutive_moment_residual_Nm=root['attempt']['constitutive_moment_mismatch_Nm'],
        center_contact_assumption_valid=bool(center_positive),support_and_wheel_contact_assumptions_valid=valid,
        center_positive_numerical_resolution_N=center_resolution,numerical_resolution_meaning='Floating-point zero classification only; NOT accepted bearing load margin or safety criterion.',
        center_or_wheel_negative_values_clamped=False,
        validity='Only maintained linear support/contact assumptions; NOT vehicle safety' if valid else 'OUTSIDE maintained center/spring/wheel contact assumptions. No lifted-center/detached-wheel redistribution or pivot-tension solution.',
        whole_coach_roll_equilibrium_solved=False,actual_sidebearer_selected=False,pivot_tension_or_retention_capacity=None,
        approved_for_fabrication=False,approved_for_operation=False)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');p.add_argument('--fixture');a=p.parse_args()
    data=json.loads(Path(a.input).read_text())
    if a.fixture:data=next(f for f in data['fixtures'] if f['id']==a.fixture)
    try:print(json.dumps(solve_support(data),indent=2,allow_nan=False))
    except (InputError,KeyError,TypeError) as e:p.exit(2,'Input/solution rejected: '+str(e)+'\n')

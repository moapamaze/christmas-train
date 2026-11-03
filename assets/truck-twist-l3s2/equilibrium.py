"""Four-corner vertical equilibrium study, SI metres/Newtons.

Dependencies: Python3 + NumPy. No CAD geometry, spring selection, dynamic
stability assessment or rail acceptance is supplied by this calculation.
Run read-only: python equilibrium.py synthetic-fixtures.json --fixture flat
"""
import argparse,json,math
from pathlib import Path
import numpy as np

class InputError(ValueError):pass
def number(value,label,positive=False,nonnegative=False):
    if isinstance(value,bool) or not isinstance(value,(int,float)):
        raise InputError(label+' must be a finite number, not null/bool/string')
    try:v=float(value)
    except (OverflowError,ValueError):raise InputError(label+' exceeds finite arithmetic range')
    if not math.isfinite(v):raise InputError(label+' must be finite')
    if positive and v<=0:raise InputError(label+' must be positive')
    if nonnegative and v<0:raise InputError(label+' must be nonnegative')
    return v
def fields(obj,names,label):
    if not isinstance(obj,dict) or set(obj)!=set(names):raise InputError(label+' requires exactly '+','.join(names))

def solve(data):
    if data.get('units')!='SI_m_N':raise InputError('units must be SI_m_N; do not silently convert gauge, inches or mm')
    g=data['geometry'];fields(g,['axle_half_spacing_m','spring_half_span_m','wheel_contact_half_span_m'],'geometry')
    a=number(g['axle_half_spacing_m'],'a',positive=True)
    bs=number(g['spring_half_span_m'],'bs',positive=True)
    bw=number(g['wheel_contact_half_span_m'],'bw',positive=True)
    rates=data['corner_rates_N_per_m']
    if not isinstance(rates,list) or len(rates)!=4:raise InputError('Exactly four aggregate spring rates required, orderFR,FL,RR,RL')
    k=np.array([number(x,'corner rate',positive=True) for x in rates])
    names=['FR','FL','RR','RL'];xs=np.array([-1.,-1.,1.,1.]);ys=np.array([1.,-1.,1.,-1.])
    x=a*xs;y=bs*ys;s=xs*ys
    rails=data['rail_heights_m'];fields(rails,['front','rear'],'rail_heights_m')
    lower=[];rail_info=[]
    for axle in ['front','rear']:
        h=rails[axle];fields(h,['left','right'],'rail '+axle)
        left=number(h['left'],'rail left');right=number(h['right'],'rail right')
        mean=(left+right)/2;slope=(right-left)/(2*bw)
        lower.extend([mean+bs*slope,mean-bs*slope])
        rail_info.append(dict(axle=axle,mean_height_m=mean,crosslevel_right_minus_left_m=right-left,axle_elevation_slope=slope))
    u=np.array(lower)
    loads=data['sprung_loads']
    if not isinstance(loads,list) or not loads:raise InputError('Explicit sprung loads required: body reaction and sprung truck weight separately')
    load_rows=[]
    for load in loads:
        fields(load,['id','vertical_down_N','x_m','y_m'],'sprung load')
        load_rows.append([number(load['vertical_down_N'],'load',nonnegative=True),number(load['x_m'],'loadx'),number(load['y_m'],'loady')])
    W=sum(r[0] for r in load_rows)
    if W<=0:raise InputError('Total sprung downward load must be positive')
    c=data['constraints'];fields(c,['body_roll_K_Nm_per_rad','body_roll_reference_slope','frame_warp','warp_K_N_per_m'],'constraints')
    Kr=number(c['body_roll_K_Nm_per_rad'],'roll stiffness',nonnegative=True)
    phiref=number(c['body_roll_reference_slope'],'body roll reference')
    if c['frame_warp'] not in ['rigid','single_compliant_mode']:raise InputError('frame_warp must be rigid or single_compliant_mode')
    compliant=c['frame_warp']=='single_compliant_mode'
    if compliant:Kw=number(c['warp_K_N_per_m'],'warp stiffness',nonnegative=True)
    else:
        if c['warp_K_N_per_m'] is not None:raise InputError('Rigid frame removes warpDOF; set unused warp_K to null, not a huge number')
        Kw=None
    moments=data['extra_downward_slope_moments_Nm'];fields(moments,['pitch','roll'],'extra moments')
    Mp=number(moments['pitch'],'extra downward pitch moment');Mr=number(moments['roll'],'extra downward roll moment')
    # Normalized unknowns [h,a*theta,bs*phi,w] all have metres as units.
    # C then has N/m units, preventing mixed-unit conditioning diagnostics.
    Bfull=np.column_stack([np.ones(4),xs,ys,s]);B=Bfull if compliant else Bfull[:,:3]
    diag=[0.,0.,Kr/bs/bs]+([Kw] if compliant else [])
    C=np.diag(diag);ref=np.array([0.,0.,bs*phiref]+([0.] if compliant else []))
    f=np.array([W,(sum(F*xx for F,xx,yy in load_rows)+Mp)/a,(sum(F*yy for F,xx,yy in load_rows)+Mr)/bs]+([0.] if compliant else []))
    matrix=B.T@(k[:,None]*B)+C;rhs=B.T@(k*u)-f+C@ref
    if not all(np.isfinite(v).all() for v in [u,matrix,rhs]):raise InputError('Nonfinite derived input/matrix; arithmetic range exceeded')
    ev=np.linalg.eigvalsh(matrix);cond=float(ev[-1]/ev[0]) if ev[0]>0 else math.inf
    if not math.isfinite(cond) or cond>1e12:raise InputError('Singular/numerically ill-conditioned normalized equilibrium; no engineering limit inferred')
    q=np.linalg.solve(matrix,rhs);frame=B@q;compression=u-frame;F=k*compression
    if not all(np.isfinite(v).all() for v in [q,frame,compression,F]):raise InputError('Nonfinite derived solution')
    residual=B.T@F-f-C@(q-ref)
    unsprung=data['unsprung_axle_loads'];fields(unsprung,['front','rear'],'unsprung_axle_loads')
    axle_out=[];Q=[]
    for n,axle in enumerate(['front','rear']):
        r=unsprung[axle];fields(r,['vertical_down_N','cg_y_m','additional_downward_roll_moment_Nm'],'unsprung '+axle)
        Wu=number(r['vertical_down_N'],'unsprung load',nonnegative=True);yu=number(r['cg_y_m'],'unsprungCG');Mu=number(r['additional_downward_roll_moment_Nm'],'axle moment')
        fr,fl=F[2*n:2*n+2];total=fr+fl+Wu;demand=bs*(fr-fl)+Wu*yu+Mu
        qr=(total+demand/bw)/2;ql=(total-demand/bw)/2
        Q.extend([qr,ql])
        axle_out.append(dict(axle=axle,unsprung_down_N=Wu,unsprung_down_roll_moment_Nm=Wu*yu+Mu,
            spring_force_right_N=float(fr),spring_force_left_N=float(fl),wheel_vertical_right_N=float(qr),wheel_vertical_left_N=float(ql),
            vertical_balance_residual_N=float(qr+ql-total),roll_balance_residual_Nm=float(bw*(qr-ql)-demand)))
    Q=np.array(Q);phi=float(q[2]/bs);theta=float(q[1]/a)
    if not all(math.isfinite(v) for v in [phi,theta]):raise InputError('Nonfinite slope: numerical geometry range exceeded')
    roll_boundary=Kr*(phi-phiref)
    total_down=W+sum(t['unsprung_down_N'] for t in axle_out)
    global_vertical=float(Q.sum()-total_down)
    global_pitch=float(np.dot(x,Q)-(sum(v[0]*v[1] for v in load_rows)+Mp+sum((-a if i==0 else a)*t['unsprung_down_N'] for i,t in enumerate(axle_out))))
    global_roll=float(np.dot(bw*ys,Q)-(sum(v[0]*v[2] for v in load_rows)+Mr+roll_boundary+sum(t['unsprung_down_roll_moment_Nm'] for t in axle_out)))
    numerical_scale=max(total_down,1.)
    if not np.isfinite(Q).all() or not all(math.isfinite(v) for v in [global_vertical,global_pitch,global_roll]) or max(abs(global_vertical),float(np.max(np.abs(residual))))>1e-9*numerical_scale:
        raise InputError('Numerical equilibrium failed; this is not an engineering acceptance test')
    allpositive=bool(np.all(F>0) and np.all(Q>0))
    return dict(id=data.get('id'),units='SI_m_N',analysis='small-displacement vertical equilibrium only',
        corner_order=names,normalized_matrix_N_per_m=matrix.tolist(),normalized_rhs_N=rhs.tolist(),normalized_condition_number=cond,
        frame_displacements=dict(heave_compression_datum_m=float(q[0]),pitch_elevation_slope=theta,roll_elevation_slope=phi,warp_mode_amplitude_m=float(q[3]) if compliant else 0.),
        rail_input_interpretation=rail_info,lower_seat_heights_m=u.tolist(),upper_seat_datum_heights_m=frame.tolist(),linear_spring_compressions_m=compression.tolist(),
        corner_spring_forces_N=F.tolist(),wheel_vertical_reactions_N=Q.tolist(),axle_balances=axle_out,
        body_roll_boundary_moment_Nm=roll_boundary,normalized_generalized_balance_residual_N=residual.tolist(),
        global_balance_residual=dict(vertical_N=global_vertical,pitch_Nm=global_pitch,roll_Nm=global_roll),
        active_contact_assumption_valid=allpositive,
        validity='Positive compression/vertical contact within this linear model ONLY; not vehicle safety' if allpositive else 'OUTSIDE assumed compression/contact regime. Negative/zero values retained as diagnostic; NO detachment or redistribution solution.',
        negative_or_zero_values_clamped=False,vehicle_roll_stability_assessed=False,wheel_rail_adhesion_or_flange_climb_assessed=False,
        accepted_spring_or_track_limit=None,approved_for_fabrication=False,approved_for_operation=False)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('input');parser.add_argument('--fixture');args=parser.parse_args()
    data=json.loads(Path(args.input).read_text())
    if args.fixture:data=next(v for v in data['fixtures'] if v['id']==args.fixture)
    try:print(json.dumps(solve(data),indent=2,allow_nan=False))
    except (InputError,KeyError,TypeError,np.linalg.LinAlgError) as e:parser.exit(2,'Input/solution rejected: '+str(e)+'\n')

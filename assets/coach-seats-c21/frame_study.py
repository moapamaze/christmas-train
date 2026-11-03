"""C2.1 3D elastic beam/spring comparison; NOT joint design or construction release.
SI calculation; inch geometry. Reproducible numpy/scipy model with 6DOF/node.
"""
from pathlib import Path
import numpy as np
from scipy.linalg import cho_factor,cho_solve
import json, math, csv
H=Path(__file__).resolve().parent
IN=.0254; LBF=4.4482216152605; E=200e9; NU=.3; G=E/(2*(1+NU))
# Atlas primary catalog p4 (1-based). Design section properties; NOT sharp-box estimates.
SECTIONS={
 'HSS1.5x1.5x1/8':dict(A_in2=.61,I_in4=.188,S_in3=.251,J_in4=.316,C_in3=.438,lb_ft=2.20),
 'HSS2x2x1/8':dict(A_in2=.84,I_in4=.486,S_in3=.486,J_in4=.796,C_in3=.817,lb_ft=3.05),
 'HSS1.25x1.25x1/8':dict(A_in2=.49,I_in4=.102,S_in3=.163,J_in4=.174,C_in3=.292,lb_ft=1.78),
}
S15='HSS1.5x1.5x1/8'; S2='HSS2x2x1/8'

def element(pa,pb,sec):
    """Local axes x along member; isotropic square section avoids orientation ambiguity.
    Cubic Euler-Bernoulli transverse interpolation, linear axial/torsional interpolation.
    """
    d=np.array(pb)-np.array(pa);L=np.linalg.norm(d);ex=d/L
    ref=np.array([0.,0.,1.]) if abs(ex[2])<.9 else np.array([0.,1.,0.])
    ey=np.cross(ref,ex);ey/=np.linalg.norm(ey);ez=np.cross(ex,ey);R=np.array([ex,ey,ez])
    T=np.zeros((12,12))
    for q in (0,3,6,9):T[q:q+3,q:q+3]=R
    s=SECTIONS[sec];A=s['A_in2']*IN**2;I=s['I_in4']*IN**4;J=s['J_in4']*IN**4
    k=np.zeros((12,12))
    k[np.ix_([0,6],[0,6])]=E*A/L*np.array([[1,-1],[-1,1]])
    k[np.ix_([3,9],[3,9])]=G*J/L*np.array([[1,-1],[-1,1]])
    k[np.ix_([1,5,7,11],[1,5,7,11])]=E*I/L**3*np.array([[12,6*L,-12,6*L],[6*L,4*L**2,-6*L,2*L**2],[-12,-6*L,12,-6*L],[6*L,2*L**2,-6*L,4*L**2]])
    k[np.ix_([2,4,8,10],[2,4,8,10])]=E*I/L**3*np.array([[12,-6*L,-12,-6*L],[-6*L,4*L**2,6*L,2*L**2],[-12,6*L,12,6*L],[-6*L,2*L**2,6*L,4*L**2]])
    return k,T,L

class Bench:
 def __init__(self,braced,sole_top=32.75,brace_section=S15,brace_end_k=None):
    self.nodes=[];self.lookup={};self.members=[];self.feet=[];self.sole_top=sole_top;self.braced=braced;self.brace_end_k=brace_end_k
    def node(x,y,z):
      key=tuple(round(v,8) for v in (x,y,z))
      if key not in self.lookup:self.lookup[key]=len(self.nodes);self.nodes.append(key)
      return self.lookup[key]
    self.node=node
    def line(tag,points,sec):
      for j,(p,q) in enumerate(zip(points[:-1],points[1:])):
       self.members.append(dict(id=f'{tag}-{j+1}',a=node(*p),b=node(*q),section=sec,family=tag.split('_')[0]))
    # Tube centreline intersections; rigid welded joints; pan/back are NOT diaphragms.
    ys=[12.875,20,22,32,42,44,51.125]
    for y in [20,44]:
      self.feet += [node(-8,y,sole_top),node(8,y,sole_top)]
      line(f'frontleg_{y}',[(-8,y,z) for z in [sole_top,35.25,47.25]],S15)
      line(f'rearleg_{y}',[(8,y,z) for z in [sole_top,35.25,47.25,58.75,62.25,67,69.25,70]],S2)
    for x in [-8,0,8]:line(f'seatrail_{x}',[(x,y,47.25) for y in ys],S15)
    for y in [12.875,51.125]:line(f'seatside_{y}',[(x,y,47.25) for x in [-8,0,8]],S15)
    for z in [58.75,69.25]:line(f'backrail_{z}',[(8,y,z) for y in ys],S15)
    if braced:
      for y in [20,44]:line(f'braceXZ_{y}',[(-8,y,35.25),(8,y,47.25)],brace_section)
      for y in [20,44]:line(f'braceYZ_{y}',[(8,y,35.25),(8,32,47.25)],brace_section)
    self.xyz=np.array(self.nodes)*IN;self.nd=len(self.nodes)*6;self.K=np.zeros((self.nd,self.nd))
    for m in self.members:
      a,b=m['a'],m['b'];k,T,L=element(self.xyz[a],self.xyz[b],m['section']);ix=np.r_[np.arange(a*6,a*6+6),np.arange(b*6,b*6+6)]
      keff=k.copy(); recovery=np.eye(12)
      if m['family'].startswith('brace') and brace_end_k is not None:keff,recovery=condense_end_springs(k,brace_end_k)
      self.K[np.ix_(ix,ix)]+=T.T@keff@T;m.update(k=k,keff=keff,recovery=recovery,T=T,L=L,ix=ix)
 def loads(self):
    n=self.nd;cases={}
    def fadd(f,point,force):i=self.lookup[tuple(float(v) for v in point)];f[i*6:i*6+3]+=force
    for sign in [1,-1]:
      f=np.zeros(n)
      for y in [20,44]:fadd(f,(8,y,67),(sign*300*LBF,0,0))
      cases['back_'+('forward' if sign>0 else 'reverse')]=f
    mg=355*9.80665
    for sx in [-1,1]:
      for sy in [-1,1]:
       for vz in [0,1.5]:
        f=np.zeros(n)
        for y in [20,44]:
         fadd(f,(8,y,62.25),(sx*mg/2,sy*mg*.5/2,0))
         # Transfer horizontal resultant from chosen CG X0 to rear-post load path X8.
         i=self.lookup[(8.,float(y),62.25)];f[i*6+5]+=-8*IN*(sy*mg*.5/2)
         fadd(f,(0,y,47.25),(0,0,-vz*mg/2))
        cases[f'inertia_x{sx:+}_y{sy:+}_down{vz:g}g']=f
    for sy in [-1,1]:
      f=np.zeros(n)
      for y in [20,44]:
       fadd(f,(8,y,62.25),(0,sy*mg*.5/2,0));i=self.lookup[(8.,float(y),62.25)];f[i*6+5]+=-8*IN*(sy*mg*.5/2)
      cases[f'lateral_y{sy:+}']=f
    f=np.zeros(n)
    for y in [22,42]:
      fadd(f,(-8,y,47.25),(0,0,-450*LBF));i=self.lookup[(-8.,float(y),47.25)];f[i*6+4]+=.5*IN*450*LBF
    cases['front_edge_aggregate']=f
    f=np.zeros(n)
    for y in [20,44]:fadd(f,(0,y,47.25),(0,0,-1.5*mg/2))
    cases['vertical_1.5g']=f
    return cases
 def solve(self,krot,kt=5e7,kz=1e8,rotation_factors=None,axial_factors=None):
    K=self.K.copy();spring=np.zeros(self.nd)
    for j,i in enumerate(self.feet):
      rf=1 if rotation_factors is None else rotation_factors[j]
      zf=1 if axial_factors is None else axial_factors[j]
      vals=[kt,kt,kz*zf,krot*rf,krot*rf,krot*rf]
      spring[i*6:i*6+6]=vals
    K+=np.diag(spring);fac=cho_factor(K,check_finite=False)
    cases=self.loads();F=np.stack(list(cases.values()),axis=1);U=cho_solve(fac,F,check_finite=False)
    results=[]
    for col,(name,f) in enumerate(cases.items()):
      u=U[:,col];r=-spring*u;feet=[];maxeq=0;worst=None;maxbrace=0
      for j,i in enumerate(self.feet):
       val=r[i*6:i*6+6];mom=val[3:].copy()
       # Translate support moments at sole TOP to sole underside. External support
       # reaction transferred through 0.5 in steel leg/sole zone; r x F included.
       dz=(self.sole_top-32.25)*IN
       mom_under=mom+np.cross([0,0,dz],val[:3])
       feet.append(dict(solver_foot_index=j+1,cad_foot_id={(-8,20):'F1',(-8,44):'F2',(8,20):'F3',(8,44):'F4'}[tuple(self.nodes[i][:2])],xyz_in=self.nodes[i],support_reaction_force_N=val[:3].tolist(),support_reaction_moment_at_sole_top_Nm=mom.tolist(),support_reaction_moment_at_sole_under_Nm=mom_under.tolist(),displacement_mm=(u[i*6:i*6+3]*1000).tolist(),rotation_mrad=(u[i*6+3:i*6+6]*1000).tolist()))
      mems=[]
      for m in self.members:
       ef=m['k']@m['recovery']@m['T']@u[m['ix']];s=SECTIONS[m['section']];A=s['A_in2']*IN**2;S=s['S_in3']*IN**3;C=s['C_in3']*IN**3
       # Conservative extreme-corner normal stress of square section, not code utilization.
       normal=max(abs(ef[0])/A+(abs(ef[4])+abs(ef[5]))/S,abs(ef[6])/A+(abs(ef[10])+abs(ef[11]))/S)/1e6
       shearT=max(abs(ef[3]),abs(ef[9]))/C/1e6
       mems.append(dict(id=m['id'],section=m['section'],end_forces_local_N_Nm=ef.tolist(),gross_corner_normal_MPa=normal,gross_torsion_shear_MPa=shearT))
       if normal>maxeq:maxeq=normal;worst=m['id']
       if m['family'].startswith('brace'):maxbrace=max(maxbrace,abs(ef[0]),abs(ef[6]))
      applied_force=np.sum(f.reshape(-1,6)[:,:3],axis=0);reaction_force=np.sum(r.reshape(-1,6)[:,:3],axis=0)
      applied_m=np.sum(np.cross(self.xyz,f.reshape(-1,6)[:,:3])+f.reshape(-1,6)[:,3:],axis=0)
      reaction_m=np.sum(np.cross(self.xyz,r.reshape(-1,6)[:,:3])+r.reshape(-1,6)[:,3:],axis=0)
      err=max(np.max(np.abs(applied_force+reaction_force)),np.max(np.abs(applied_m+reaction_m)))
      nodes=u.reshape(-1,6);forcepoints=np.where(np.linalg.norm(f.reshape(-1,6)[:,:3],axis=1)>0)[0]
      results.append(dict(case=name,krot_Nm_per_rad=krot,kt_N_m=kt,kz_N_m=kz,rotation_factors=rotation_factors,axial_factors=axial_factors,spring_factor_order_cad_ids=['F1','F3','F2','F4'],
       max_loaded_point_horizontal_displacement_mm=float(np.max(np.linalg.norm(nodes[forcepoints,:2],axis=1))*1000),max_node_displacement_mm=float(np.max(np.linalg.norm(nodes[:,:3],axis=1))*1000),
       max_foot_bending_moment_Nm=float(max(np.linalg.norm(q['support_reaction_moment_at_sole_under_Nm'][:2]) for q in feet)),
       max_foot_axial_tension_N=float(max(0,max(-q['support_reaction_force_N'][2] for q in feet))),
       max_foot_compression_N=float(max(q['support_reaction_force_N'][2] for q in feet)),
       max_brace_axial_magnitude_N=float(maxbrace),max_gross_corner_normal_MPa=maxeq,worst_member=worst,equilibrium_max_abs_error_N_or_Nm=float(err),feet=feet,members=mems))
    return results

def condense_end_springs(k,end_k):
    # External12 local DOF, internal6 beam end rotations; translations continuous.
    # Independent three-axis rotation springs between beam and welded frame node.
    rots=[3,4,5,9,10,11];trans=[0,1,2,6,7,8]
    B=np.zeros((12,18));C=np.zeros((6,18))
    for i in trans:B[i,i]=1
    for j,i in enumerate(rots):B[i,12+j]=1;C[j,i]=-1;C[j,12+j]=1
    KK=B.T@k@B+end_k*C.T@C
    Kii=KK[12:,12:];Kie=KK[12:,:12]
    inv=np.linalg.pinv(Kii,rcond=1e-12) if end_k==0 else np.linalg.inv(Kii)
    rec=np.vstack([np.eye(12),-inv@Kie]);keff=KK[:12,:12]-KK[:12,12:]@inv@Kie
    return .5*(keff+keff.T),B@rec

def check_element():
    # Independent closed-form cantilever checks: axial, two bending planes,torsion.
    s=SECTIONS[S2];length=.8;k,T,L=element([0,0,0],[length,0,0],S2);K=(T.T@k@T)[6:,6:]
    vals={};loads=[(0,1000,1000*length/(E*s['A_in2']*IN**2)),(1,1000,1000*length**3/(3*E*s['I_in4']*IN**4)),(2,1000,1000*length**3/(3*E*s['I_in4']*IN**4)),(3,100,100*length/(G*s['J_in4']*IN**4))]
    for dof,force,expected in loads:
      f=np.zeros(6);f[dof]=force;u=np.linalg.solve(K,f);vals[str(dof)]=dict(actual=float(u[dof]),expected=expected,relative_error=float(abs(u[dof]/expected-1)))
    # Arbitrarily rotated beam: compare end translation against vector formula.
    a=np.array([.1,.2,.3]);b=np.array([.5,.7,.9]);k,T,L=element(a,b,S2);K=(T.T@k@T)[6:,6:];f=np.array([400.,-300.,100.,0,0,0]);u=np.linalg.solve(K,f);ex=(b-a)/L;axial=ex*(f[:3]@ex);trans=f[:3]-axial;expected=axial*L/(E*s['A_in2']*IN**2)+trans*L**3/(3*E*s['I_in4']*IN**4)
    vals['rotated']=dict(actual=u[:3].tolist(),expected=expected.tolist(),relative_error=float(np.linalg.norm(u[:3]-expected)/np.linalg.norm(expected)))
    assert max(v['relative_error'] for v in vals.values())<1e-10
    # Check exact released-rotation limit -> axial truss only.
    k,T,L=element([0,0,0],[.8,0,0],S2);kr,rec=condense_end_springs(k,0);expected=np.zeros((12,12));expected[np.ix_([0,6],[0,6])]=E*s['A_in2']*IN**2/.8*np.array([[1,-1],[-1,1]])
    vals['brace_all_rotation_release']=dict(max_abs_matrix_error_N_or_Nm=float(np.max(abs(kr-expected))),relative_error=float(np.max(abs(kr-expected))/np.max(abs(expected))))
    assert vals['brace_all_rotation_release']['relative_error']<1e-10
    # Independently check zero strain rigid-body translation and infinitesimal rotation.
    a=np.array([.1,.2,.3]);b=np.array([.5,.7,.9]);k,T,L=element(a,b,S2);q=np.zeros(12);omega=np.array([.01,-.02,.03]);q[:3]=np.cross(omega,a)+[.04,.02,-.03];q[3:6]=omega;q[6:9]=np.cross(omega,b)+[.04,.02,-.03];q[9:]=omega
    vals['rigid_body_patch']=dict(max_abs_endforce_N_or_Nm=float(np.max(abs(k@T@q))))
    assert vals['rigid_body_patch']['max_abs_endforce_N_or_Nm']<1e-6
    return vals

def main():
    studies=[];geoms=[]
    profiles=[('rotation_sweep',k,5e7,1e8,None,None) for k in [0,1e3,1e4,1e5,1e6,1e7]]
    profiles += [('soft_axial',1e4,5e7,1e7,None,None),('stiff_axial',1e4,5e7,1e9,None,None),('mixed_feet',1e4,5e7,1e8,[1,10,1,.1],[1,1,.2,1])]
    variants=[(False,33,'C2_original_unbraced_0.75in',None),(False,32.75,'C21_unbraced_control_0.5in',None),(True,32.75,'C21_braced_0.5in',None),(True,32.625,'C21_braced_0.375in',None),(True,33,'C21_braced_0.75in',None)]
    variants += [(True,32.75,'C21_braced_0.5in_endrot_'+str(k),k) for k in [0,1e2,1e3,1e4,1e5]]
    variants=[v+(S15,) for v in variants]
    variants += [(True,top,'C21_braced_'+str(t)+'in_brace1.25_endrot_'+str(k),k,'HSS1.25x1.25x1/8') for top,t in [(32.75,.5),(32.625,.375)] for k in [None,0,1e3,1e4,1e5]]
    for braced,top,label,bek,bsec in variants:
     b=Bench(braced,top,brace_section=bsec,brace_end_k=bek)
     geoms.append(dict(variant=label,brace_end_k_Nm_rad=bek,sole_top_in=top,nodes_in=b.nodes,feet_node_indices=b.feet,members=[{key:m[key] for key in ['id','a','b','section','family']} for m in b.members],centreline_tube_mass_kg=sum(m['L']/IN/12*SECTIONS[m['section']]['lb_ft']*.45359237 for m in b.members)))
     for name,kr,kt,kz,rf,af in profiles:
      rr=b.solve(kr,kt,kz,rf,af)
      for r in rr:r['variant']=label;r['support_profile']=name;r['brace_end_k_Nm_rad']=bek
      studies+=rr
    # Supplementary one-brace-family removal helps isolate directionality without changing supports.
    check=check_element()
    output=dict(issue='PF-3O2-C2.1-R0',status='PRELIMINARY COMPARISON; NOT FOR CONSTRUCTION',date='2026-10-19',
      method='3D linear elastic Euler-Bernoulli frame, six DOF/node, rigid beam intersections, independent finite translational/rotational springs at four leg bases; no pan/back diaphragm stiffness.',
      sections_catalog=SECTIONS,material=dict(E_Pa=E,poisson=NU,G_Pa=G),
      load_basis=dict(inertia_mass_kg=355,mass_basis='Same conservative C2 290kg occupants +65kg bench budget for every variant; no mass-reduction credit.',Fx_g=1,Fy_g=.5,Fz_down_g=[0,1.5],inertia_horizontal_z_in=62.25,inertia_CG_x_in=0,front_edge_patch_centres_xyz_in=[[-7.5,22,50],[-7.5,42,50]],front_edge_patch_size_in=[5,5],vertical_at_seat_x_in=0,vertical_z_in=47.25,backrest_force_lbf=600,backrest_z_in=67),
      limitations=[
       'Rotation springs are deliberately swept analyst parameters, not properties proven by plate thickness. No selected case is called actual joint stiffness.',
       'All support springs are bilateral, linear and independent. Uplift contact, bolt preload/loss, slip, hole clearance, prying, weld/rail flexibility and coupled support terms are NOT solved.',
       'Main welded frame joints are rigid at centreline intersections. Additional brace-end spring cases (0,100,1000,10000,100000Nm/rad) isolate ideal pins and semi-rigid brace endings; these do not calibrate actual welded-joint stiffness. Local HSS wall flexibility, brace fit-up eccentricity, panel bending, bolt fasteners, fatigue, buckling and nonlinear/P-delta behavior are excluded.',
       'Front edge loads use5x5in proposed patch centres X-7.5/Y22,42 so forward patch edge alignsX-10 seat edge. Transfer force+moment to X-8 front rail workpoints preserves chosen resultant, not local pan contact/bending. Backloads use rearpostsY20/44 as global-resultant surrogate for seat middlesY22/42; local back-panel load spread remains unproven.',
       'Rear back rails idealized on rear-post X8 centreline although legacy rails have X7.75 centroid. This0.25in eccentricity is not modeled.',
       'Beam gross corner stresses add absolute biaxial bending and axial components. These are screening demands, not code utilizations, allowable capacities, joint passes or certification.',
       'Nonstructural floor carries no bench load; any solid/boot contact with floor would invalidate this model.',
       'Foot reaction moments are computed at sole top and separately transferred to sole underside including horizontal-force eccentricity; cap/cheek/rail-wall demands need their own downstream model.',
       'Model results alone do not justify changing cap/sole thickness. Use envelope reactions for local contact/plate/bolt/weld/rail analysis and confirm with a full-size instrumented test.'
      ],validation=check,geometries=geoms,results=studies)
    (H/'frame-study.json').write_text(json.dumps(output,indent=2))
    short=[{k:r[k] for k in ['variant','support_profile','case','krot_Nm_per_rad','kt_N_m','kz_N_m','max_loaded_point_horizontal_displacement_mm','max_foot_bending_moment_Nm','max_foot_axial_tension_N','max_foot_compression_N','max_brace_axial_magnitude_N','max_gross_corner_normal_MPa','worst_member','equilibrium_max_abs_error_N_or_Nm']} for r in studies]
    with (H/'frame-study-summary.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=short[0].keys());w.writeheader();w.writerows(short)
    (H/'frame-geometry.json').write_text(json.dumps(geoms,indent=2))
    print(json.dumps(dict(cases=len(studies),max_equilibrium_error=max(r['equilibrium_max_abs_error_N_or_Nm'] for r in studies),validation=check),indent=2))
    for label in ['C2_original_unbraced_0.75in','C21_braced_0.5in']:
     print(label)
     for r in studies:
      if r['variant']==label and r['support_profile']=='rotation_sweep' and r['case']=='back_forward':print('k',r['krot_Nm_per_rad'],'def',round(r['max_loaded_point_horizontal_displacement_mm'],3),'Mfoot',round(r['max_foot_bending_moment_Nm'],2),'tension',round(r['max_foot_axial_tension_N'],2),'stress',round(r['max_gross_corner_normal_MPa'],2),r['worst_member'])
if __name__=='__main__':main()

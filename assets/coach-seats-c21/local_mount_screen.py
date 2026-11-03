"""C2.1 preliminary ribbed mount screen. Units N, mm, MPa, Nmm internally.

Not a joint capacity calculation. The variable alpha is an explicit bolt/contact
force amplification sensitivity, not a bound on prying. Frame force inputs must
be reported about the sole UNDERSIDE datum. Positive N means uplift.
"""
import json, math, sys
from pathlib import Path

IN = 25.4
E = 200000.0
G = dict(plate_t=.5*IN, sole_t=.5*IN, cap_t=.625*IN, rib_t=.375*IN, rib_depth=1.75*IN,
         bolt_a=.875*IN, bolt_b=2*IN, bolt_hole=.5625*IN,
         plate_width=1.75*IN, plate_net_width=(1.75-.5625)*IN,
         plate_span=(.875-.1875)*IN, upper_front_rib_span=1.25*IN,
         upper_rear_rib_span=1*IN, lower_rib_span=.75*IN,
         bolt_stress_area=.1419*IN*IN,
         effective_bolt_length=(1.746062992126+.5)*IN)

def strip(force, width, thickness=None):
    thickness=G['sole_t'] if thickness is None else thickness
    i=width*thickness**3/12
    return dict(thickness_mm=thickness,stress_MPa=6*force*G['plate_span']/(width*thickness**2),
                deflection_mm=force*G['plate_span']**3/(3*E*i))

def rib(force_each, span):
    """Two equally loaded bolts per rib; summed absolute load sensitivity."""
    force=2*force_each
    i=G['rib_t']*G['rib_depth']**3/12
    sigma=6*force*span/(G['rib_t']*G['rib_depth']**2)
    tau=1.5*force/(G['rib_t']*G['rib_depth'])
    return dict(stress_MPa=sigma,max_rectangular_shear_MPa=tau,
                von_mises_bending_shear_MPa=(sigma*sigma+3*tau*tau)**.5,
                deflection_mm=force*span**3/(3*E*i),
                section='Full1.75in depth through boltline; bevel beyond loaded segment',
                limit='Opposite-sign bolt loads can twist plate/rib; torsion and root weld/leg wall interaction are not bounded by this bending/shear screen.')

def screen(case):
    n=case.get('N_N',0); mx=case.get('Mx_Nm',0)*1000; my=case.get('My_Nm',0)*1000
    # Absolute moment combination; do not credit compression/gravity against uplift.
    t0=max(n,0)/4+abs(mx)/(4*G['bolt_b'])+abs(my)/(4*G['bolt_a'])
    c0=abs(n)/4+abs(mx)/(4*G['bolt_b'])+abs(my)/(4*G['bolt_a'])
    thickness=G['cap_t'] if case.get('datum','').startswith('cap') else G['sole_t']
    rows=[]
    for alpha in (1,1.5,2):
        f=alpha*c0
        rows.append(dict(amplification_sensitivity=alpha,
            bolt_tension_sensitivity_N=alpha*t0,
            absolute_bolt_contact_sensitivity_N=f,
            plate_net_strip=strip(f,G['plate_net_width'],thickness),
            plate_gross_strip=strip(f,G['plate_width'],thickness),
            upper_front_rib=rib(f,G['upper_front_rib_span']),
            upper_rear_rib=rib(f,G['upper_rear_rib_span']),
            lower_rib=rib(f,G['lower_rib_span'])))
    return dict(input=case,no_compression_credit_tension_N=t0,
                absolute_connection_force_N=c0,sensitivity=rows)

limitations=[
 'Strip width is an analyst conservative screen, not a demonstrated effective width or yield-line model.',
 'Both plates span from bolt center to central rib face. Two-way bending and local washer/spacer annular bearing are not solved.',
 'The actual contacts are four steel spacer annuli. Outer sole edges do not touch floor or provide compression toes.',
 'Force amplification1/1.5/2 is a sensitivity study, not a proved upper bound on bolt prying.',
 'Bolts sharing a rib create coupled displacement; scalar spring estimates are not calibrated joint stiffness.',
 'Rib-root welds, cap/cheek welds, post-wall plastification, rail-wall yielding and rail-end torsion remain separate checks.',
 'Do not treat a material yield-stress comparison or bolt proof strength as allowable passenger-seat joint strength.'
]
sources=[
 dict(url='https://steeltubeinstitute.org/resources/hss-bolted-connections-keep-it-together-with-a-bolt-of-confidence/',
      use='Primary STI March2026 guidance: end plates need prying evaluation; HSS flat/corner geometry and local wall limit states matter.'),
 dict(url='https://steeltubeinstitute.org/resources/rectangular-hss-bolted-end-plate-connections-under-bending-moment/',
      use='Primary STI December2025 paper: contact compression and bolt tension redistribute under bending; published design models have geometry limits. This mount is not asserted to satisfy those limits.'),
 dict(url='https://steeltubeinstitute.org/resources/connecting-hollow-structural-section-members-bolts/',
      use='Primary STI through-bolt guidance used to reject unsupported bolts across hollow gaps without reinforcement; current four spacers are solid steel clamp paths.')]

def result(cases):
    p=strip(1000,G['plate_net_width'])
    uf=rib(1000,G['upper_front_rib_span']);lo=rib(1000,G['lower_rib_span'])
    cb=1000*G['effective_bolt_length']/(E*G['bolt_stress_area'])
    cap_p=strip(1000,G['plate_net_width'],G['cap_t'])
    compliance=p['deflection_mm']+cap_p['deflection_mm']+uf['deflection_mm']+lo['deflection_mm']+cb
    k=1000/compliance
    return dict(issue='C2.1 independent local mount screen R0',units='N,mm,MPa unless suffix states otherwise',
        geometry=G,per_kN=dict(sole_plate=p,cap_plate=cap_p,upper_front_rib=uf,upper_rear_rib=rib(1000,G['upper_rear_rib_span']),lower_rib=lo),
        scalar_stiffness_estimate=dict(compliance_mm_per_kN=compliance,per_bolt_N_per_mm=k,
            Ktheta_y_kNm_per_rad=4*k*G['bolt_a']**2/1e6,
            Ktheta_x_kNm_per_rad=4*k*G['bolt_b']**2/1e6,
            limitation='Exploratory scale only; shared-rib coupling, leg/rail wall, weld, preload and contact are omitted.'),
        cases=[screen(c) for c in cases],limitations=limitations,sources=sources,
        engineering_approved=False,fabrication_approved=False)

if __name__=='__main__':
    cases=json.loads(Path(sys.argv[1]).read_text()) if len(sys.argv)>1 else [
      dict(name='illustrative2kN direct force perbolt',N_N=8000),
      dict(name='inherited local combined moment sensitivity',Mx_Nm=663.199222875,My_Nm=1326.39844575)]
    print(json.dumps(result(cases),indent=2))

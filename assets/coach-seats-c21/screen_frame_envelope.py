"""Read final independently solved1.25in-brace forces and screen three datums."""
import json,gzip
from pathlib import Path
import local_mount_screen as m
folder=Path(__file__).resolve().parent
source=folder/'braced-reactions.json'
a=json.loads(source.read_text() if source.exists() else gzip.decompress(source.with_name(source.name+'.gz').read_bytes()).decode());cases=[]
for c in a['cases']:
    if not c.get('variant','').startswith('C21_braced_0.5in_brace1.25_'):continue
    for f in c['feet']:
        F=[-v for v in f['support_reaction_force_N']]
        M=[-v for v in f['support_reaction_moment_at_sole_under_Nm']]
        x,y,z=f['xyz_in']
        cad={(-8,20):'F1',(-8,44):'F2',(8,20):'F3',(8,44):'F4'}[(int(x),int(y))]
        assert cad==f['cad_foot_id']
        base=dict(name=c['case'],variant=c['variant'],support_profile=c.get('support_profile'),
          brace_end_k_Nm_rad=c.get('brace_end_k_Nm_rad'),krot_Nm_per_rad=c['krot_Nm_per_rad'],
          solver_foot_index=f['solver_foot_index'],CAD_foot=cad,xyz_in=f['xyz_in'],
          N_N=F[2],Fx_N=F[0],Fy_N=F[1],Mx_Nm=M[0],My_Nm=M[1],Mz_Nm=M[2])
        for datum,z in [('sole_underside',32.25),('cap_top',31.628937007874),('cap_underside',31.003937007874)]:
            h=(32.25-z)*.0254
            # Change wrench reference from sole underside to a lower cap datum.
            q=dict(base,datum=datum,datum_Z_in=z,Mx_Nm=M[0]-h*F[1],My_Nm=M[1]+h*F[0])
            cases.append(q)
r=m.result(cases)
(folder/'final-concurrent-foot-inputs.json').write_text(json.dumps(cases,indent=2))
(folder/'final-concurrent-local-screen.json').write_text(json.dumps(r,indent=2))
summaries={}
for datum in ['sole_underside','cap_top','cap_underside']:
    subset=[c for c in r['cases'] if c['input']['datum']==datum]
    summaries[datum]={}
    for key in ['no_compression_credit_tension_N','absolute_connection_force_N']:
        summaries[datum][key]=max(subset,key=lambda c:c[key])
small=dict(case_foot_datum_count=len(cases),frame_case_count=len(cases)//12,
    selected_braces='1.25sq nominal1/8',envelopes=summaries,limitations=r['limitations'],
    geometry=r['geometry'],sources=r['sources'],source=str(source))
(folder/'final-mount-envelope.json').write_text(json.dumps(small,indent=2))
for datum,ss in summaries.items():
    print(datum)
    for key,q in ss.items():
        print(key,round(q[key],3),q['input']['variant'],q['input']['CAD_foot'],q['input']['name'])
        at=q['sensitivity'][-1]
        print('2x netstrip',round(at['plate_net_strip']['stress_MPa'],3),
              'upperfrontVM',round(at['upper_front_rib']['von_mises_bending_shear_MPa'],3),
              'lowerVM',round(at['lower_rib']['von_mises_bending_shear_MPa'],3))
print('case_foot_datum_count',len(cases))

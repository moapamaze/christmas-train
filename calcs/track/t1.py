import time, route_check as R, numpy as np, json
V=R.build_vehicles()
TL=None
def run(A, rev=False, rng=None, step=1000.):
    t=time.time(); r=R.sweep(A,V,step=step,reverse=rev,s_range=rng); 
    print(A['tag'], 'rev' if rev else 'fwd', round(time.time()-t,1),'s')
    for k,v in r['res'].items(): print(f"  {k:14s} out {v['out']:7.1f} ({v['out_nm'][:30]}, R{v.get('out_R',0):.0f}) in {v['inn']:7.1f} ({v['inn_nm'][:30]}) low_out {v['low_out']:.0f} low_in {v['low_inn']:.0f}")
    for i,c in enumerate(r['cpl']): print('  cpl',i,{k:(round(x,2) if isinstance(x,float) else x) for k,x in c.items()})
    print('  lead',r['lead']); print('  yaw',{k:round(x,2) for k,x in r['yaw'].items()})
    return r
for R_ in (100,50,45):
    A=R.load_alignment(f'R{R_}',R.synth_els([('T',80),('C',R_,180,'L'),('T',80)]))
    run(A, rng=(60000, 80000+R_*np.pi*1000+50000), step=2000.)

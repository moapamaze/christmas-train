import json,math,itertools
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Polygon,Circle
H=Path(__file__).parent
P=json.loads((H/'layout-proposal.json').read_text())

def poly(p):
 x,y,t=p;t=math.radians(t);c=math.cos(t);s=math.sin(t)
 return np.array([[x+u*c-v*s,y+u*s+v*c] for u,v in [(-12,-15),(36,-15),(36,15),(-12,15)]])
def rect(v):
 x0,x1,y0,y1=v;return np.array([[x0,y0],[x1,y0],[x1,y1],[x0,y1]])
def point_segment(p,a,b):
 d=b-a;t=np.clip(np.dot(p-a,d)/np.dot(d,d),0,1);return float(np.linalg.norm(p-(a+t*d)))
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def seg_inter(a,b,c,d):
 ab=b-a;cd=d-c;den=cross(ab,cd)
 if abs(den)<1e-9:return False
 t=cross(c-a,cd)/den;u=cross(c-a,ab)/den
 return -1e-9<=t<=1+1e-9 and -1e-9<=u<=1+1e-9
def inside(p,pg):
 cs=[cross(pg[(i+1)%4]-pg[i],p-pg[i]) for i in range(4)]
 return min(cs)>=-1e-8 or max(cs)<=1e-8
def distance(a,b):
 if inside(a[0],b) or inside(b[0],a):return 0.
 for i in range(4):
  for j in range(4):
   if seg_inter(a[i],a[(i+1)%4],b[j],b[(j+1)%4]):return 0.
 return min([point_segment(p,b[i],b[(i+1)%4]) for p in a for i in range(4)]+[point_segment(p,a[i],a[(i+1)%4]) for p in b for i in range(4)])
def samples(path):
 out=[];errs=[]
 for i,(a,b) in enumerate(zip(path[:-1],path[1:])):
  x,y,t=a['axle_x'],a['axle_y'],a['heading_deg'];xx,yy,tt=b['axle_x'],b['axle_y'],b['heading_deg'];dt=(tt-t+180)%360-180;d=math.hypot(xx-x,yy-y);action=b['action_from_previous']
  if action in ['F','B']:
   heading=np.array([math.cos(math.radians(t)),math.sin(math.radians(t))]);travel=np.array([xx-x,yy-y]);lateral=abs(cross(heading,travel));errs.append(lateral)
   assert abs(dt)<1e-8 and lateral<1e-7 and np.dot(heading,travel)*(1 if action=='F' else -1)>0
  elif action.startswith('ARC_'):
   cx,cy=b['arc_center_xy'];rr=b['arc_radius_in'];assert abs(math.hypot(x-cx,y-cy)-rr)<1e-7 and abs(math.hypot(xx-cx,yy-cy)-rr)<1e-7
   mid=math.radians(t+dt/2);heading=np.array([math.cos(mid),math.sin(mid)]);travel=np.array([xx-x,yy-y]);lateral=abs(cross(heading,travel));errs.append(lateral);assert lateral<1e-7 and np.dot(heading,travel)<0
  else:assert d<1e-8
  n=max(1,math.ceil(d/.25),math.ceil(abs(dt)/.25))
  for j in range(n):
   q=j/n
   if action.startswith('ARC_'):
    aa=math.radians(t+dt*q);out.append((cx+rr*math.sin(aa),cy-rr*math.cos(aa),t+dt*q))
   else:out.append((x+(xx-x)*q,y+(yy-y)*q,t+dt*q))
 out.append((path[-1]['axle_x'],path[-1]['axle_y'],path[-1]['heading_deg']))
 return out,max(errs,default=0)
reports=[]
fig,axs=plt.subplots(2,1,figsize=(16,12))
for bay,ax in enumerate(axs,1):
 D=json.loads((H/f'path-bay{bay}.json').read_text());assert D['found'];pp=D['path'];poses,lateral=samples(pp);obs=[rect(o) for o in D['obstacles']]
 minmargin=1e9;worst=None;hits=0
 for i,p in enumerate(poses):
  q=poly(p)
  for j,o in enumerate(obs):
   #quickaxisdistance lowerbound;skiponlyifcannotbeatcurrentmin
   dx=max(o[:,0].min()-q[:,0].max(),q[:,0].min()-o[:,0].max(),0);dy=max(o[:,1].min()-q[:,1].max(),q[:,1].min()-o[:,1].max(),0)
   if math.hypot(dx,dy)>minmargin:continue
   d=distance(q,o)
   if d<minmargin:minmargin=d;worst={'sample':i,'obstacle_index':j,'pose':p}
   if d<1e-7:hits+=1
 #separateotherbayoccupiedfold-seat check,conservative30widefulluserenvelope
 other=2 if bay==1 else 1;st=60 if other==1 else 126
 foldob=rect((st,st+34,-49,-19));foldmargin=min(distance(poly(p),foldob) for p in poses)
 other_path=json.loads((H/f'path-bay{other}.json').read_text())['path'][-1]
 actual_other=poly((other_path['axle_x'],other_path['axle_y'],other_path['heading_deg']))
 actual_other_margin=min(distance(poly(p),actual_other) for p in poses)
 final=poly(poses[-1]);b=P['wheelchair_bays'][bay-1]
 insidebay=final[:,0].min()>=b['x'][0] and final[:,0].max()<=b['x'][1] and final[:,1].min()>=b['y'][0] and final[:,1].max()<=b['y'][1]
 #0.25intranslation/0.25degrotationsampling=>nearest sample excursion <=0.125in; rotation39inradius*.125deg=.0851in
 max_corner_radius=max(math.hypot(36,abs(q.get('arc_radius_in',0))+15) for q in pp)
 correction=max(.125,max_corner_radius*math.radians(.125))
 rep={'bay':bay,'independent_collision_verifier':'Convex polygon edge intersections, point containment and exact segment distances; separate from search SAT','sample_count':len(poses),'sample_step_limit_in':.25,'sample_angle_limit_deg':.25,'collision_count':hits,'minimum_sampled_distance_to_raw_obstacles_in':minmargin,'maximum_corner_radius_about_rotation_center_in':max_corner_radius,'between_sample_distance_bound_in':correction,'conservative_continuous_clearance_lower_bound_in':max(0,minmargin-correction),'worst_case':worst,'max_sideways_step_error_in':lateral,'parked_body_bounds':{'x':[float(final[:,0].min()),float(final[:,0].max())],'y':[float(final[:,1].min()),float(final[:,1].max())]},'parked_inside_assigned60x36bay':bool(insidebay),'other_bay_occupied_fold_proxy':{'x':[st,st+34],'y':[-49,-19],'minimum_sampled_distance_in':foldmargin,'continuous_lower_bound_in':max(0,foldmargin-correction)},'forward_steps':sum(p['action_from_previous']=='F' for p in pp),'reverse_steps':sum(p['action_from_previous']=='B' for p in pp),'pivot_steps':sum(p['action_from_previous'] in ['L','R'] for p in pp),'travel_direction_reversals':len(list(itertools.groupby('B' if p['action_from_previous'].startswith('ARC_B') else p['action_from_previous'] for p in pp[1:] if p['action_from_previous'] in ['F','B'] or p['action_from_previous'].startswith('ARC_'))))-1,'path_pose_count':len(pp),'action_run_count':len(list(itertools.groupby(p['action_from_previous'] for p in pp[1:]))),'other_bay_at_actual_computed_parked_pose':{'minimum_sampled_distance_in':actual_other_margin,'continuous_lower_bound_in':max(0,actual_other_margin-correction)},'exit':'Exact time reversal follows same collision-free sweep; controls and crew assistance are not validated.'}
 reports.append(rep)
 #Renderlayout andverifiedpath; onlyrepresentativebodyposes soaxesremainlegible
 ax.set_aspect('equal');ax.add_patch(Rectangle((0,-52),306,104,facecolor='#f8f8f2',edgecolor='#233d3a',linewidth=1.6))
 ax.add_patch(Rectangle((0,-12),306,36,facecolor='#e7f0e8',edgecolor='none'))
 for s in P['fixed_seats']:
  ax.add_patch(Rectangle((s['x'],s['y']),s['l'],s['w'],facecolor='#b5b8b2',edgecolor='#5a625b',linewidth=.5))
  ax.add_patch(Rectangle((s['x']+s['l'],s['y']),9.5,s['w'],facecolor='#e7d7b5',edgecolor='#a28955',linewidth=.4,alpha=.7))
 for b in P['wheelchair_bays']:
  ax.add_patch(Rectangle((b['x'][0],b['y'][0]),60,36,facecolor='#dce9ef',edgecolor='#4f8c9c',linewidth=.7))
  ax.text(sum(b['x'])/2,-43,b['id'],ha='center',fontsize=8,color='#396274')
  ax.add_patch(Rectangle((b['seat_strip_x'][0],-52),6,36,facecolor='#995c46',edgecolor='none'))
 for s in P['fixed_seats']:
  ax.add_patch(Rectangle((s['x'],s['y']),s['l'],s['w'],facecolor='#b5b8b2',edgecolor='#5a625b',linewidth=.5))
 ax.add_patch(Circle((30,6),30,fill=False,edgecolor='#75a289',linestyle=':',linewidth=.8))
 other=D['other_occupied_proxy'];ax.add_patch(Rectangle((other['x'][0],other['y'][0]),48,30,facecolor='#426b7d',edgecolor='#254453',alpha=.85));ax.text(sum(other['x'])/2,-35,'OTHER\nOCCUPIED',ha='center',va='center',color='white',fontsize=7)
 idx=sorted(set([0,len(poses)-1]+[int(j*(len(poses)-1)/8) for j in range(1,8)]))
 for i in idx:ax.add_patch(Polygon(poly(poses[i]),fill=False,edgecolor='#d18b3e',linewidth=.7,alpha=.7))
 xy=np.array([[p['axle_x'],p['axle_y']] for p in pp]);ax.plot(xy[:,0],xy[:,1],color='#a45424',linewidth=1.4);ax.scatter(xy[[0,-1],0],xy[[0,-1],1],color='#a45424',s=18)
 ax.add_patch(Polygon(poly(poses[-1]),fill=False,edgecolor='#af4f1c',linewidth=2))
 ax.plot([9,51],[-52,-52],color='white',linewidth=3);ax.text(30,-62,'42 in opening\n30 in proxy width',ha='center',fontsize=8)
 ax.text(230,4,'36 in route',ha='center',fontsize=8,color='#436650')
 ax.set_xlim(-5,310);ax.set_ylim(-105,58);ax.set_title(f'Bay {bay}: verified rigid-proxy entry while other bay occupied',loc='left',fontsize=13,color='#1b4239');ax.set_xlabel('Coach X (in)');ax.set_ylabel('Coach Y (in)');ax.grid(alpha=.12)
fig.suptitle('C3 maneuvering study · forward/reverse + rear-axle pivots · no lateral sliding',x=.5,y=.99,fontsize=16,color='#173c35')
fig.text(.5,.015,'30 × 48 in rigid proxy. Rear axle 12 in from rear, 36 in front overhang. Door leaf, securement hardware and actual wheel/caster behavior unresolved.',ha='center',fontsize=9)
fig.tight_layout(rect=[0,.035,1,.965]);fig.savefig(H/'C3-path-study.svg');fig.savefig(H/'C3-path-study.webp',dpi=160);plt.close(fig)
R={'status':'Conditional geometric maneuvering screen; not accessibility acceptance or physical wheelchair validation','proxy':{'width_in':30,'length_in':48,'rear_axle_from_rear_in':12,'front_overhang_in':36,'body_corner_radius_about_axle_in':39},'search_modes':'Forward/reverse 3 in segments parallel to current heading, with in-place axle pivots. Bay 1 uses a 7.5 degree heading lattice with its shunting tail replaced by a reverse circular arc; Bay 2 uses 15 degrees. No sideways translations.','obstacle_basis':'All fixed-seat envelopes and 9.5 in forward leg reservations; full stowed strips; coach walls and 42 in negative-Y side opening; other occupied 30 x 48 in proxy. Both folding seats fully stowed except separate other-folding-seat proxy screen.','normal_boarding_side_assumption':'NegativeY opening. Recheck mirroredpositiveYboarding ifselected.','reports':reports,'limits':['Actual mobility devices can exceed30x48in and have different axle/caster locations; validate representativedevicefamilies andfull-size mockup.','Pivots assume differential-wheel ability aroundrearaxle; self-propelled/assisted operation, caster sweep, anti-tip hardware andfootrests arenot separately validated.','Door leaves/handles/threshold/lift/bridge andsecurementhardware are notyetmodeled.','Parked shoulder locations andcompanion alignment are illustrative, not anthropometric acceptance.','Search and analytic arc prove existence for this proxy only. Both approaches use one travel-direction reversal; steering steps are geometric paths, not operating instructions. Practical controls, effort and usability still need full-size trials.']}
R['sampling_bound_note']='The reserve is the maximum of half the0.25in translation interval and the largest corner radius about each actual rotation center times half the0.25degree angular interval. For a reverse arc, radius=sqrt(36^2+(15+R)^2); thus the currentR10.4848in arc uses44.1075in, and0.125in remains governing.'
R['layout_change_experiment_disposition']='A two-inch longer first bay was considered but not adopted. Analytic arc smoothing resolved lattice-induced shunting within the original60x36in bay.'
R['reports'][0]['analytic_reverse_arc']={'radius_in':10.484767898195344,'sweep_deg':90,'arc_length_in':10.484767898195344*math.pi/2,'replaces':'Discrete predecessor tail with15travel-direction reversals'}
(H/'maneuvering-verification.json').write_text(json.dumps(R,indent=2))
print(json.dumps(reports,indent=2))

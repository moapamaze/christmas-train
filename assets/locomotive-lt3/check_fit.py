"""Kinematic clearance screens, not a complete vehicle contact/dynamic solution."""
from pathlib import Path
import json,math,itertools
import numpy as np
P=Path(__file__).resolve().parent
def rx(a):
 c,s=math.cos(a),math.sin(a);return np.array([[1,0,0],[0,c,-s],[0,s,c]])
def ry(a):
 c,s=math.cos(a),math.sin(a);return np.array([[c,0,s],[0,1,0],[-s,0,c]])
def rz(a):
 c,s=math.cos(a),math.sin(a);return np.array([[c,-s,0],[s,c,0],[0,0,1]])
origin=np.array([0.,0.,1335.])
def corners(x,y,z,l,w,h):return np.array(list(itertools.product([x-l/2,x+l/2],[y-w/2,y+w/2],[z-h/2,z+h/2])))
worst={'body_adapter_to_fork_vertical_mm':1e6,'body_pendant_to_yaw_cap_vertical_mm':1e6,'ring_to_yaw_cap_vertical_mm':1e6,'catch_window_X_margin_mm':1e6,'catch_window_Y_margin_mm':1e6,'catch_head_vertical_gap_mm':1e6,'side_shoe_X_overlap_margin_mm':1e6,'side_shoe_Y_overlap_margin_mm':1e6}
max_side_compression=0;cases=0
for yaw,roll,pitch in itertools.product(np.linspace(-8,8,9),np.linspace(-2,2,5),np.linspace(-2,2,5)):
 Y,X,Z=rz(math.radians(yaw)),rx(math.radians(roll)),ry(math.radians(pitch));R=Y@X@Z
 def move(points,M=R):return (points-origin)@M.T+origin
 adapter=move(corners(0,0,1441.15,400,400,20));tongue=move(corners(0,0,(1431.15+1275)/2,120,150,1431.15-1275))
 worst['body_adapter_to_fork_vertical_mm']=min(worst['body_adapter_to_fork_vertical_mm'],adapter[:,2].min()-1412.5)
 worst['body_pendant_to_yaw_cap_vertical_mm']=min(worst['body_pendant_to_yaw_cap_vertical_mm'],tongue[:,2].min()-1264)
 ring=move(corners(0,0,1335,320,320,120),Y@X)
 worst['ring_to_yaw_cap_vertical_mm']=min(worst['ring_to_yaw_cap_vertical_mm'],ring[:,2].min()-1264)
 for sign in [-1,1]:
  # Vertical stud transformed into body frame; intersect at catch plate midplane.
  base=np.array([sign*450,0,1170]);b=R.T@(base-origin)+origin;v=R.T@np.array([0,0,1]);u=b+v*((1470-b[2])/v[2])
  # Radius projection expanded conservatively for tilt, plus full plate thickness slope.
  rad=12/abs(v[2]);dx=abs(u[0]-sign*450)+rad+10*abs(v[0]/v[2]);dy=abs(u[1])+rad+10*abs(v[1]/v[2])
  worst['catch_window_X_margin_mm']=min(worst['catch_window_X_margin_mm'],35-dx)
  worst['catch_window_Y_margin_mm']=min(worst['catch_window_Y_margin_mm'],90-dy)
  plate=move(corners(sign*450,0,1470,320,300,20))
  worst['catch_head_vertical_gap_mm']=min(worst['catch_head_vertical_gap_mm'],1515-plate[:,2].max())
  # All cap corners transformed into body shoe coordinates for finite-pad overlap.
  cp=corners(0,sign*550,1445.15,120,120,0)
  local=(cp-origin)@R+origin
  worst['side_shoe_X_overlap_margin_mm']=min(worst['side_shoe_X_overlap_margin_mm'],200-max(abs(local[:,0])))
  worst['side_shoe_Y_overlap_margin_mm']=min(worst['side_shoe_Y_overlap_margin_mm'],120-max(abs(local[:,1]-sign*550)))
  # Plane height of underside of tilted body shoe at each cap corner.
  n=R@np.array([0,0,1]);pt=move(np.array([[0,sign*550,1451.15]]))[0]
  for q in cp:
   planeZ=pt[2]-(n[0]*(q[0]-pt[0])+n[1]*(q[1]-pt[1]))/n[2]
   max_side_compression=max(max_side_compression,1445.15-planeZ)
 cases+=1
radial=897.5-math.hypot(550,2915-2350)
report={'issue':'PF-LOCO-LT3-R0','sampled_combinations':cases,'yaw_deg':[-8,8],'roll_deg':[-2,2],'pitch_deg':[-2,2],'minimum_margins':worst,
 'maximum_cap_edge_compression_demand_mm':max_side_compression,'side_elastomer_trial_compression_limit_mm':20,
 'powerpack_corner_to_shell_radial_margin_mm':radial,'engine_opening_X_mm':[1600,5800],'skid_X_mm':[2280,4620],'engine_opening_note':'Remove both half-panels and their detachable ribs in bays1–3. Hoist, sling, engine CG, lifting points and hoses not qualified.',
 'passed_specific_screens':bool(all(v>0 for v in worst.values()) and max_side_compression<20 and radial>0),
 'not_checked':['Complete swept-solid collision detection','Unmodeled bearing covers, fasteners, lubrication hardware, guides and stops at maximum fault travel','Wheel/rail contact, curving forces and stability','Side-bearing pressure distribution and actual rubber deformation','Primary spring/damper motion ratios and actual axlebox guides','Leading/trailing running gear, ladder sweep and tender/coupler clearance'],
 'status':'Sampled geometric screens only; positive margins are not an engineering release.'}
(P/'fit-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

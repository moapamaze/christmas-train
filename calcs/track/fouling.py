"""Fouling point / clearance mark for the #8 turnouts (Rail Bot, Steering 14c). Verification of 34.0 m."""
import json, math
dyn = 1696.0; extra = 200.0
centres_req = 2 * dyn + extra                       # 3,592 -> mark at 3.6 m track centres
N = 8; G = 0.9144
theta = 2 * math.atan(1 / (2 * N))                  # frog angle
R = 1.45 * G * N * N                                # lead radius per track_structure/track_calc.py (~84.9 m)
x_c = R * math.sin(theta); y_c = R * (1 - math.cos(theta))   # end of the closure curve (tangent to the frog angle)
x_mark = x_c + (3.6 - y_c) / math.tan(theta)
# R80 working layout: loco end throw scales ~1/R from the R100 basis (148 mm in 1,696)
throw80 = 148 * 100 / 80; d_dyn80 = throw80 - 148
out = dict(dynamic_half=dyn, allowance=extra, centres_required_mm=centres_req, centres_mark_m=3.6, frog_angle_deg=round(math.degrees(theta), 3),
           lead_radius_m=round(R, 1), closure_end=[round(x_c, 2), round(y_c, 3)], x_mark_from_points_m=round(x_mark, 2), rail_bot_m=34.0,
           r80_extra_end_throw_mm=round(d_dyn80, 1), r80_note=f"If either track is on R80 at the mark, add ~{d_dyn80:.0f} mm per side (loco end throw {throw80:.0f} vs 148 at R100) - within the 200 mm allowance ({2*d_dyn80:.0f} < 200); level layout F, owner pending.",
           basis="Clearance mark where track centres = 2 x 1,696 dynamic half-width + 200 mm = 3,592 -> 3.6 m; #8 (frog 7.153 deg), closure curve R ~84.9 m tangent at the points then straight at the frog angle; straight main.")
json.dump(out, open("/workspace/train/calcs/track/fouling.json", "w"), indent=1)
print(out)

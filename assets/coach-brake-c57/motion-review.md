# C5.7 body-to-truck hose movement review

Discrete body-to-truck hose and support geometry screening. No fabrication or operating approval.

45 body postures × 32 primary/wear postures = 1440 combined configurations. 90 supply curves and 64 local curves were regenerated with constant geometric free length.
Supply minimum bend radius: 51.828 mm; local minimum: 66.676 mm. Catalog nominal comparison: 45 mm, without claiming dynamic-duty approval.
Supply-to-supply free-curve clearance lower bound: 44.205 mm. Maximum length residual: 1e-09 mm.

Maximum supply end-clock mismatch change after rotation-minimizing transport: 21.084 degrees. This is an unresolved geometric torsion-compatibility diagnostic, not a permitted hose twist or an elastic stress calculation. The fittings are not credited as live swivels.

Positive intersections: nominal new hardware 0, rigid movement 0, supply hose 0, revised local hose/all hardware 0, supply/local hose 0, local/local hose 0. Calculation errors: 0.

## Connection review

227 nominal contacts; 0 new rigid parts lack a contact path to retained geometry. These are exact CAD-contact observations, not joint-strength findings.

## Shared-pose model

yaw+7-bodyroll+2-axleroll+2-jounce-wear25.4. All stated components share the same body posture, primary travel and wear offset. The JSON stores the exact transforms and regenerated curves.

## Limits

- The 45 body postures combine five yaw values with zero tilt or a 2 degree resultant tilt cone at eight azimuths; independent 2 degree roll plus 2 degree pitch is not used.
- All 32 primary suspension/wear states are combined wherever relative geometry requires it, yielding 1440 distinct body/primary configurations. These are discrete configurations, not a continuous sweep.
- Body and truck move together in primary heave. Supply endpoints articulate only through the declared body-to-truck yaw/tilt transform. Primary travel affects clearance to the axle, chamber, link, and preserved local hoses.
- Constant-length Bezier curves preserve endpoint tangents but do not solve material twist, pressure growth, clamp friction, strain, whipping, fatigue, drainage, or actual installed-hose equilibrium.
- The Bishop-frame diagnostic measures the change in rigid-end clock mismatch after rotation-minimizing transport along the geometric centerline. Any nonzero result is unresolved torsional compatibility; no allowable twist or live-swivel rotation is credited.
- Geometric free lengths and straight leads are not production cut lengths. Crimp insertion, actual interfaces, tolerances, slack allowance and supplier-approved rail dynamic duty remain open.
- A positive modeled clearance is not a tolerance or maintenance allowance. Purchased external profiles, elbow/fitting engagement, port assignment, valve/control topology and upstream coach plumbing remain provisional.
- The relocated C56 local air hardware and regenerated local hoses are checked anew against all relevant current fixed, primary-moving and body targets. No previous local-hose clearance result is used to cover the revised geometry.
- C5 body-context/upper-joint geometry and the isolated C54 brake axle remain the coordinate reference. Separate CW3 wheelset study and whole-coach flexible pipes are not substituted or accepted by this local audit.
- Opposite axle and spring-coil deformation are not independently re-solved. Existing C56 structural force, fit, preload, fatigue and supplier holds remain open. No brake station is duplicated.

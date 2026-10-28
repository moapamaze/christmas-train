# C5.6 local hose and support motion review

Bounded local hose/support motion audit. No fabrication or operating approval.

64 constant-length hose curves across 16 suspension/maintenance poses and two wear offsets. Minimum bend radius 72.038 mm, compared with 45 mm nominal catalogue minimum; maximum arc-length residual 1.13e-10 mm.
Mutual free-curve hose clearance lower bound 20.350 mm. Hose exact collision tests 386, positive pairs 0; new support/moving-member tests 0, positive pairs 0; body-turning tests 0, positive pairs 0.

## Turning boundary

The new local anchors and both chamber hoses turn with the truck. The yaw samples check their position against the retained body geometry. No body-to-truck supply loop is modeled or accepted; the upstream anchor ends remain open interfaces.

## Nominal hardware interfaces

94 exact new-hardware pair tests recorded 0 positive intersections. Each appears in the JSON record; unknown threaded/OEM contact is not silently accepted.

## Limits

- Reported structural/body gap values are conservative expanded Bezier-hull/AABB lower bounds, not exact minimum surface distances.
- Sixteen suspension/maintenance poses, two wear offsets, five yaw angles and three body-roll angles are discrete development samples, not continuous swept-volume certification.
- Local frame-to-chamber hoses have truck-fixed anchor fittings. Both ends yaw with the truck; these curves do not represent or qualify the still-unmodeled body-to-truck air-supply flex loop.
- Upstream anchor ports are open connection boundaries. Valve topology, service/parking circuit assignment, body supply anchors and emergency/parking control logic remain unresolved.
- Constant-length cubic curves preserve analytic endpoint tangents. Actual hose torsion, pressure growth, friction through clamps, fatigue, straight-lead requirements, heat and abrasion allowances require supplier/physical validation.
- Geometric free-curve length and modeled straight leads are not a production hose cut length: fitting insertion, crimp assembly, pressure growth and installation tolerances are unresolved.
- Thread engagement and OEM caliper/chamber/rotor outlines remain unqualified. Separate nonphysical interface reservations are excluded from material collision tests but remain open mating interfaces.
- Opposite axle and coil shapes remain nominal; wheel profiles and current alternative wheelset-study candidates are not integrated into this frozen C5 truck reference.
- Unchanged C55 core mounting strength, fatigue, bearing fits, key load sharing and overall brake loads are inherited unresolved holds; this review grants no fabrication or operation approval.

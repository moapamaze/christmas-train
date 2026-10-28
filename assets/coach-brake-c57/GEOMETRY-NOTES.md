# C5.7 body-to-truck air connection

This revision adds two candidate supply hoses and their installed supports to the first brake installation. It also shifts the existing fixed local air assembly 50 mm toward positive X to clear the body adapter through combined yaw and tilt. The air baseplate is extended, and the two local free hose curves are regenerated. All 105 selected primary mounting parts remain unchanged: no axle, bearing, hub, caliper carrier, reaction link or frame member is resized. Other brake stations are not copied.

## Installed path

The body support bears against the actual positive-X face of the retained C5 body bolster at X50.8 mm. Its six-millimetre backing plate occupies Z690–780 mm. A six-millimetre overhead shelf and two side gussets carry the twin bulkhead anchor plate at X528–534 mm, with ports at Z740 mm. The body ends point toward negative X; their 70 mm exposed straight leads pass through upside-down STAUFF smooth guide blocks before reaching X390 mm. The shelf sits above the hoses at Z760.75–766.75 mm. The bracket spans Y−260 to −105 mm; its underside gussets sit outside the guide and weld-base envelopes. Its overhang and welds require air-line loads, material and fatigue qualification.

At the truck, source-grounded Parker 2202P-6-6 street elbows turn the open C5.6 coupling ports upward and backward. Straight adapter/swivel chains would have aimed the hoses into the existing centre crossbeam. Each elbow is followed by the retained 017M/17B25 fitting family and a 70 mm exposed straight lead. A central 12 mm gusset supports the short twin-guide shelf. Its root contacts the back face of the existing C5.6 AIR-ANCHOR-PLATE at local q=0, v=−10 to +20 mm; no new hole or reshaping of that plate is made. The gusset bends around the anchor-plate upper edge and supports the back of the guide shelf, avoiding the guide bores. Nominal fitting thread engagements remain scenarios.

The relocated local air origin is (270, 0, 450) mm. The extended AIR-SUPPORT-BASE occupies X160–296.2 mm, with its original supported span ending at X246.2 mm. Its three original beam attachment welds stay in place on the unchanged HSS. No weld is invented beneath the 50 mm plate overhang. Air-support bending, fatigue and weld capacity remain open. The local chamber endpoints stay fixed to the same moving assembly; only their truck-side controls and support points shift.

The new free hoses run from truck endpoints (194.5516, −150/−215, 569.0933) mm to body endpoints (390, −150/−215, 740) mm. Nominal cubic handles are 160 and 90 mm. Each nominal free portion measures 321.0109 mm; each end also has a separately modeled 70 mm straight lead. These are exposed geometric lengths, **not** hose cutting instructions. Manufacturer crimp data, insertion, free-length requirements and pressure growth remain unresolved.

A three-millimetre stand-off guard with six-millimetre corner radii sits between the body bolster and the free hoses. It attaches to the body backing plate with actual welded tabs. Hose contact with the guard is not intended or credited as acceptable; the motion review must keep it clear.

## Kinematic boundary

The model is expressed in the nominal C5 truck frame. The body rotates about the actual spherical centre (0, 0, 830.7) mm. The independent check uses yaw relative to the truck and a two-degree resultant tilt cone. Primary axle travel moves the axle, brake chamber and existing local hoses relative to the truck; it must not be added again as body-to-truck anchor heave.

The body and truck fitting axes are fixed to their respective mounts. A 17B25 installation swivel is **not** a continuously rotating hose joint. A collision-free constant-length centreline does not establish acceptable hose twist, pressure flex, fatigue, abrasion or life. Those are separate manufacturer/prototype holds. Physical port labels PORT97 and PORT116 remain unassigned until ZF confirms the service and spring-release identities.

## Source and preservation

The builder imports the frozen C5.6 BREP and duplicates existing fitting/guide dimensional envelopes with declared rigid transforms. Source-controlled envelope dimensions are distinguished from unresolved local profiles. Only M, N and D are sourced for the new 2202P elbow; its outer extrusion profile, thread outline and counterbore details are provisional. The detailed hardware record is `research-air-hardware.json`.

The checkpoint contains 279 valid parts. The 199 parent parts are partitioned into 156 unchanged shapes, 40 rigidly relocated air parts and three revised shapes: the baseplate and two local free hoses. There are 80 additions. Of the 156 unchanged shapes, 154 retain identical BREP serialization. The two unchanged chamber-fitting shapes have different serialization after import/export sharing, but zero Boolean symmetric difference and matching volumes/bounds. `interface-geometry-preservation.json` records this explicitly. The 105 selected primary mounting parts remain in the unchanged category.

Intended contact pairs in the geometry contract identify actual bracket/weld, bulkhead, guide and hose-end connections for independent review. A listed pair is an expected interface, not a substitute for testing its final shape. All engineering conclusions must bind the final checkpoint hash after contact and movement review.

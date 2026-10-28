# C3 folding-seat foundation — preliminary issue R0

The folding seat uses two cantilever posts and two reinforced floor mounts. No supporting leg remains in the wheelchair bay. This is a new foundation, not a reuse of the four-foot C2.1 bench approval: C2.1 was itself preliminary, and its braces and reactions do not apply here.

## Coordinated candidate dimensions

Dimensions are inches, with Z measured above rail. Seat 1 hinge is X64. The second assembly translates +66 in X, putting its hinge at130.

| Item | Candidate |
|---|---|
| Floor foot centers | X62.50, Y−44/−20; second seat X128.50 |
| Post center | X61.25, same Y; HSS2×2×3/16 |
| Cap plate | A36,5×6×3/4; X60–65; Z31.003937–31.753937 |
| Sole plate | A36,5×6×1; X60–65; Z32.25–33.25 |
| Four bolts per foot | Proposed1/2-13×3.25 SAE Grade8; exact locking hardware and installation remain open |
| Bolt-hole pattern |3.5X×4Y rectangle;9/16 holes; offsets X±1.75,Y±2 |
| Four load-bypass spacers | OD1,ID9/16,L0.496063in=12.6mm |
| Rail side cheeks | Two per foot,5X×3Z×3/8Y; outside HSS rail sidewalls |
| Bottom tie |5X×2.75Y×3/8Z under HSS rail |
| Upper/lower ribs | Proposed1/2in plates; actual shapes in CAD; rib and weld resistance remains unverified |

The HSS seat rail is3in high and2in wide, from Z28.003937 to31.003937. The two3/8in cheeks and bottom plate make a closed saddle with the cap. Lower wing ribs support the overhanging cap. A front upper rib connects each sole to its post. Four spacers carry bolt clamping and seat loads across the floor opening; no structural capacity is assigned to the floor panel or its finish. Post rear face X60.25 leaves0.25in sole land for a proposed rear weld; the plate rear edge is exactly at X60, so there is **zero allowance for fabrication error at the rear boundary of the reserved strip**.

The1in sole supersedes the initially proposed3/4in and7/8in soles. It addresses the increased demand in the transverse occupancy sensitivity. It is not a finding that the whole joint passes.

## Loads and results

The analyst comparison uses145kg occupant plus65kg complete-seat allowance. Horizontal forces are±1g longitudinal and±0.5g lateral, applied at X72,Z62.25. Both0g and1.5g downward vertical cases are included. The occupied seat has not been weighed; increase the allowance and rerun if the completed assembly exceeds65kg.

Separate static comparisons use300lbf at the back at Z67 in both longitudinal signs, and450lbf downward with a conservative resultant at the seat front X82. These values are taken from APTA PR-CS-S-016-99 Rev3.1 for comparison. Its stated scope does not establish applicability to this private tourist railway, and these calculations do not establish compliance or replace physical testing.

The sensitivity includes an occupant CG displaced±9.5in across the24in seat, with the65kg assembly remaining centered. The resulting inertia-load CG shifts±6.560in. Front/back applied-load sensitivities also use±9.5in. The front5in patch can lie within the seat at those transverse positions. Linear tributary weights split forces between the two posts. Three alternative partitions carry0%,50% or100% of the lateral roll moment through the24in axial foot couple; the remainder acts locally at each foot. These are equilibrium-consistent load-sharing assumptions, not a stiffness solution. They do not cover a broken support, every possible asymmetric mechanism reaction, or impact while folding.

| Envelope, including transverse sensitivity | Result |
|---|---:|
| Ideal corner-bolt tension, without compression credit or prying |13.053kN |
| Ideal bolt-group shear, without friction credit |1.148kN |
| Gross2×2×3/16 post normal-stress sum |238.5MPa |
| Gross seat-rail normal/torsion equivalent-stress envelope |93.4MPa |
| Largest individual rail-end vertical reaction magnitude |6.277kN |
| Largest rail-end transverse reaction magnitude |0.948kN |
| Full torque that one rail end may have to carry |0.662kNm |

Plate screens use an assumed net strip width of2.5−9/16=1.9375in, with a1in cap-wing lever and1.75in sole-to-front-rib lever. At twice the ideal corner load, the3/4in cap screen is222.8MPa and the1in sole screen is219.3MPa. The factor2 is only a sensitivity to possible additional force; it does not bound actual prying. Effective width, contact, two-dimensional plate behavior, rib force transfer and local weld/HSS behavior require a joint analysis. Comparing a gross elastic stress with material yield alone is not a design-code acceptance.

## Actual path into the coach frame

Seat loads pass through the hinge/stop structure and posts, the sole/ribs, bolts and spacers, the cap and saddle, and into the longitudinal HSS3×2×3/16 seat rails. The first pair of rail segments runs X47–68; the second pair runs X118–140. Seat-rail bending distributes vertical force and pitching moment to their ends. Lateral roll can also impose torsion along those rails.

The numerical rail screen assumes vertical/lateral simple supports and examines both torsionally fixed ends plus the full torque assigned to one end. Neither torsional restraint nor joint stiffness has been established for the retained J1a end connections. If both ends offer no effective torsional restraint, the seat cannot rely on the calculated small twist. The93.4MPa gross rail value therefore **does not approve the load path into the crossmembers**.

At Y−44, some rail ends meet HSS4×2×1/8 outer crossmembers; the Y−20 rails meet deeper central members. Existing end connections have no accepted weld or local-wall design. They must be developed for the listed forces and torque, combined with the other applicable coach-frame loads.

A separate reinforcement proposal is a3/8in face plate,6in wide in Y and full crossmember height, with two1/4in internal diaphragms at Yfoot±2in joining all four crossmember walls. It would require rail-end cutbacks by the face-plate thickness, fabrication access and engineered diaphragm/weld detailing. It is **not included in the current CAD, mass, or stiffness assumptions**. The current issue preserves J1a rather than quietly substituting an unverified connection.

## Hardware and limits

With the1in sole, total stack through cap, spacer, sole, two F436 washers and the previously modeled ordinary nut is2.877563–3.037563in, using washer thickness0.097–0.177in and nut height0.4375in. A3.25in bolt projects0.212437–0.372437in beyond that nut, about2.76–4.84 threads at13TPI. This checks that trial envelope only. The selected positive-locking nut, actual threaded length, shank/shear planes, tool approach, torque/preload and corrosion treatment remain to be coordinated. No torque is issued.

Still unfinished: bolt/contact/prying analysis; rib strength and stiffness; post/hinge local stress; all weld groups; saddle-to-rail transfer; crossmember local behavior; actual rail-end connections; fatigue; physical seat tests; pinch guards/boots and final fabrication tolerances. The two mounts and their surrounding structure should remain a preliminary candidate until those items are resolved.

## Reproducibility

`foundation_screen.py` regenerates `foundation-screen.json` using Python's standard library. It asserts all three force and moment equilibria for the paired feet and vertical/lateral bending and torsion balances for each rail case. There are33 external-load cases,198 foot/load-sharing cases and396 rail cases. No friction resistance or verified prying reduction is credited.

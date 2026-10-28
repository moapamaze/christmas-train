# C5.5 geometry gap review

C5.5 changes the air interfaces of one installation. It preserves C5.4 custom metal, the revised axle keyway, bearing stack, hub, torque link and frame support. It does not establish a commercially qualified brake package.

## Four inherited envelope intersections

| C5.4 pair | Volume, mm³ | Cause and C5.5 treatment |
|---|---:|---|
| Chamber intermediate envelope / fitting at station 97 | 983.002 | An assumed 8 mm male-thread insertion intersects an unbored chamber cylinder. Separate the unresolved thread-interface reservation from the external fitting. Do not invent a port cavity. |
| Chamber intermediate envelope / fitting at station 116 | 983.056 | Same unresolved mating interface. Exact boss section, engagement and thread sealing/clocking are still required. |
| Fitting / hose at station 97 | 27.708 | The swept profile used a sampled chord, tilted 3.261° from the port axis. Exact Bezier geometry with the analytic tangent removes this modeling artifact. |
| Fitting / hose at station 116 | 27.743 | Same artifact, with 3.265° tilt. Scratch exact-solid tests produced zero intersection for both corrected mouths. |

The first two findings were not evidence of two known pieces of metal occupying the same space. Separating the reservations does not prove the real threaded joints fit. The last two were reproducible CAD construction errors.

## Source corrections and component boundaries

The controlled WABCO 9253800230 GA row for **9253800250** gives the port-face construction as **89 mm radial ordinate, ±25 mm tangential offset, at 97/116 mm behind the mounting face**. C5.4 used an unsupported 88 mm radial ordinate. C5.5 corrects it by 1 mm along the actual port normal. The 300° clocking is retained.

The PAN17 manual defines cast **11 as service** and **12 as spring/parking**. Neither the available GA nor the manual establishes the cast-number assignment to the 97/116 mm stations. C5.5 therefore labels geometry by station, not by an unverified air-circuit function.

The fitting remains Parker **10125-6-6B-VS**: published overall length 44 mm and AF 17.4625 mm. Exact crimp shell, hex lengths and installed NPTF engagement are unavailable. The inherited 8 mm insertion is retained only as an explicit placement scenario. Hose **271-6** has nominal OD 19 mm and catalogue minimum bend radius 45 mm. Its new CAD is an annular, exact cubic sweep.

## Moving hoses

A fixed remote endpoint and tangent plus the transformed chamber endpoint/tangent define a candidate constant-length family. Keep the initial handle at 150 mm; solve the final handle for the same integrated curve length. The C5.4 pilot calculation covered 10 suspension poses and both wear limits: minimum radii were 79.0 and 83.8 mm. Simply dragging the first two control points changed length by about −24 to +19 mm and was rejected.

C5.5 must recompute those results after the datum correction, then check both hoses against each other, custom parts and the complete retained C5 truck/body. Sampling is a diagnostic, not a physical hose acceptance. Actual fixed couplings, clamp lead lengths, torsion limits, rub clearance, manufacturing allowance and flex validation remain missing.

## Service access

The PAN17 pad procedure retains the chamber, removes the retainer and three springs, retracts adjustment, slides the caliper in both directions, and removes pads/pressure plate. Its vehicle procedure removes the road wheel. The railway installation cannot inherit an on-car service claim from this manual. C5.4's single generic pad-withdrawal box is removed because it does not represent that sequence.

Tool interfaces are AF 8 mm at the adjuster, AF 17 mm at the lining retainer bolt and AF 24 mm at the chamber nuts. These values do not define wrench swings or socket/hand envelopes. Chamber removal requires isolated air, mechanical spring release, disconnected hoses and mounting-nut removal. A 43 mm axial translation only clears the published stud projection from an ideal mounting plane; actual caliper seats, nuts, tools and the complete removal route remain open.

## Primary records

- WABCO chamber GA: `../coach-brake-c54/source-evidence/wabco9253800230-GA.pdf`; https://www.wabco-customercentre.com/catalog/docs/9253800230____053_dascheck_l4_page-1---notset_tif.pdf
- WABCO PAN17 manual, 2nd edition 10/2013, PDF pages 14–17 and 34–38: https://www.ridewellcorp.com/manuals/Wabco%20PAN%2017_IM_2ndEd_10-2013.pdf
- Parker 4400 catalogue, hose 271 and Series 25 fitting tables: https://www.parker.com/content/dam/Parker-com/Literature/Hose-Products-Division/Catalog-4400-PDF-Files/HPD_4400_Catalog.pdf
- C5.4 `independent-review.json`, `geometry-contract.json`, `checkpoint.brep`; C5.5 `patch-audit.json` and `hose-motion-review.json` record geometry-specific evidence.

# C3.1 folding-seat foundation — preliminary detail record

Revision C31-FND-R1. This is a dimensioned candidate and a set of conditional structural comparisons, not a fabrication release or a claim that the complete coach connection meets an accepted railway standard.

The seat load path is post and gussets → sole → bolts and machined spacers → cap and ribbed saddle → existing HSS seat rail → external closed collars → existing crossmembers. The timber/composite floor receives no seat-anchor strength credit. The two-foot cantilever does not reuse the C2.1 braced four-foot connection approval.

## Controlled geometry

First-seat feet remain at X62.5, Y−44/−20 in; second-seat feet are X128.5. Posts remain X61.25/127.25. Cap and sole stay X60..65 in for the first seat, 5 × 6 in in plan. The cap is 7/8 in thick; the sole is 1⅛ in thick at Z32.25..33.375. The four bolt centers are X±1.75, Y±2.25 about each foot, in 9/16 in holes. This gives a 3.5 × 4.5 in pattern, 0.46875 in hole-edge ligament and 0.2345 in minimum nominal nut-flange edge clearance.

Saddle cheeks and bottom tie start at X60.1875 and finish at X65. The aft 3/16 in rail-side weld ends at X60 exactly. The cap/sole and this weld therefore have zero nominal aft strip margin; fabrication tolerance has not been solved. The bottom tie is 3.25 in wide so its external 1/4 in closure fillets have a real ledge. The forward rib has a 4.5 in root height and 1.5 in tip height. Two 1/4 in side gussets per post are included. Detailed polygons and weld IDs are in foundation-geometry.json; foundation_detail_cad.py builds the foot preparation and weld envelopes.

Each rail-end collar has two 3/8 in full-height external faceplates and 1/4 in top/bottom closures, 4 in wide in Y. X45 uses the actual 12 × 4 in bolster; the outer Y−44 stations at X69/117/141 use 4 × 2 in crossmembers; the Y−20 stations use 6 × 2 in crossmembers. No internal diaphragm or cut into the closed crossmember is assumed. All twelve affected longitudinal rail segments are trimmed at the new collar faces. The first loaded span is X47.375..67.625; the second is X118.375..139.625. Neighboring rail ends also require welds; their other seat/floor demands remain outside the seat-only screen.

Collar corners and cap-to-cheek seams use an exterior 45° bevel, 1/4 in preparation depth, 1/8 in root land and zero nominal root gap. The proposal uses FCAW/GMAW in flat/horizontal position, flush fill and only 3/16 in effective throat in the calculation. This requires a qualified procedure for the actual joint; a rendered groove does not prove penetration. Rail-end welds are 3/16 in fillets on the four workable flats. Collar-to-parent end welds are 1/8 in on the 1/8 in crossmembers and 3/16 in on the thicker members. Actual corner radii, wall thickness and fit-up must be measured; rounded-corner weld length is not counted.

## Load basis and calculation limits

The revised inertia comparison uses 145 kg occupant + 90 kg complete seat/foundation allowance = 235 kg, at the same conservative elevated CG. The 90 kg allocation includes the seat, its saddle hardware, a per-seat allocation of collar/floor steel, padding, welds, retention and finish; it is not an additional 90 kg on top of the modeled assembly. Actual coach BOM mass counts collar and floor pieces once. Bare collar plate blanks total 27.529 kg per coach before bevel removal/weld addition; floor covers/supports total 7.753 kg before welds. Final CAD masses and remaining allowance are recorded by the geometry build.

There are 33 load cases and 198 foot cases. The analyst inertia comparison is ±1g longitudinal, ±0.5g lateral and 0 or 1.5g downward. Separate 450 lbf front-edge and ±300 lbf backrest cases remain comparisons only. Transverse occupant/patch offsets and three roll-transfer fractions are included. These are equilibrium-consistent sensitivities, not a validated stiffness distribution, seat failure-case proof or crash certification. A 36-combination rotational-spring sweep at each span end adds 28,512 rail-end states. Full foot axial force and torsion may be assigned to either individual end for its envelope; these independent end maxima are not asserted to occur simultaneously in one physical load case.

| Quantity | Revised demand |
|---|---:|
| Ideal bolt tension, no compression credit | 13.701 kN |
| Bolt in-plane shear | 1.188 kN |
| Bolt tension at explicit 2× prying sensitivity | 27.401 kN |
| Cap / sole strip stress at that 2× sensitivity | 214.7 / 207.8 MPa |
| Post gross elastic stress at actual base elevation | 249.9 MPa |
| Rail gross elastic von Mises envelope | 99.8 MPa |
| Rail-end vertical / horizontal component envelope | 8.109 / 1.177 kN |
| Rail-end torsion / bending component envelope | 0.713 / 0.813 kN·m |

The factor 2 is a sensitivity, not an established prying upper bound. Effective plate-strip widths, contact and load sharing remain assumptions. The post stress is below candidate A500 C nominal yield, but is not presented as an ASD/code pass: the analyst load combinations and acceptance method have not been agreed.

| Local weld comparison | Peak elastic traction |
|---|---:|
| Post/upper-rib/side-gusset base group | 73.4 MPa |
| Upper rib 4.5 in root, 3/16 fillets | 109.2 MPa |
| Side gusset roots, 3/16 fillets | 70.9 MPa |
| Cap-to-cheek 3/16 effective PJP | 102.5 MPa |
| Saddle-to-rail side-flat fillets | 83.5 MPa |
| Rail-end four-flat 3/16 fillet group | 96.1 MPa |
| Lower wing root, 5/16 fillets, 2× sensitivity | 135.2 MPa |
| Collar end weld, seat-only component envelope | 43.6 MPa |
| Collar corner grooves, seat-only component envelope | 34.7 MPa |

These are compared with 0.6 × E70 / 2 = 144.8 MPa as an ASD-style weld comparison, without a directional strength increase. They assume compatible elastic weld-group action and do not establish parent-wall resistance or fatigue strength. Segment-end stress peaks are evaluated; equilibrium residuals over 198 independent weld-group cases are below 1e−7 N/N·m. Upper/side rib gross root screens are 78.4/122.7 MPa; the lower wing gross root at the 2× sensitivity is 133.6 MPa.

A separate Navier plate calculation screens the 3/8 in collar faces under the rail-end normal-load distributions. With all four face edges translationally supported, 161-term maxima are 120.0, 138.4 and 139.5 MPa for 4, 6 and 12 in face heights. The largest 81→161-term change is 0.25%. This conditional comparison does not prove the real collar/HSS edge stiffness. Equivalent distributed parent-wall transfer tractions are at most 33.2 MPa seat-only; these are not punching, plastification or local-wall resistance checks. Existing chord stress, adjacent rail loads, weld-root bending, global floor/bolster loading and fatigue remain separate gates.

## Floor transition

Full-depth floor cutouts replace the former partial relief. Each collar receives a flush 3/8 in steel cover at Z31.625..32, supported by two 1/2 in wide steel strips at Y±1.5 on the collar cap. The cover is (crossmember X width + 1.25) × 4.5 in. Strip-to-cover fillets are 3/16 in; strip-to-cap fillets are 1/8 in. The 1/16 in perimeter joint is filled flush with a traffic-rated compatible elastomer seal. Target zero step at the actual finished floor; the proposed maximum construction mismatch is 1 mm, subject to the floor acceptance requirements. Anti-slip finish and seal product remain to be selected. Open ends below the cover avoid an enclosed water pocket; cut-edge coatings must be restored after weld inspection. No structural credit is assigned to the cut floor edges.

The separate local floor comparison puts 450 lbf in one 1 in plate strip: both the conservative 3 in span and 3/4 in edge cantilever give 99.3 MPa. Applying that floor load concurrently at the cover corners with the seat component envelope raises the maximum collar end-weld comparison to 48.0 MPa and equivalent parent-wall transfer traction to 36.5 MPa. This is not a whole-floor, wheelchair restraint or global underframe acceptance.

## Bolts, locking and maintenance

Candidate hardware is 1/2-13 × 3.5 in SAE J429 Grade 8 hex cap screws, ASTM F436 hardened washers above and below, and STANLEY Spiralock F08130M flange locking nuts. The manufacturer catalog identifies the nut as compatible with standard UN external threads and Grade 8-equivalent properties. Its maximum flange diameter is 1.031 in, AF is 3/4 in, and height is 0.437..0.458 in. Final certificates, supply and installation qualification remain required.

The steel grip excluding washers is 2.371063 in. With the catalog washer and nut ranges, the stack is 3.002063..3.183063 in and nominal thread projection from a 3.5 in bolt is 0.316937..0.497937 in. A 1.25 in nominal threaded length covers the nut; runout/actual screw tolerances require final procurement confirmation. Do not substitute the former 3.25 in bolt. The 2× external tension comparison is 299.3 MPa on the thread stress area, against 827.4 MPa proof stress; installation preload and joint stiffness still have to be included before selecting torque. No torque value is issued.

The actual selected service envelope is the Tekton SHD23019 deep 3/4 in socket, 1.02 in OD × 3 in long, with 1.1 in hex depth. Both bolt head and nut require access: restrain the head above and drive the nut from below. The nominal closest side-gusset/toe and widened-bottom-tie clearances are 0.115 in. CAD must check the complete axial insertion/removal path and both-ended counterhold, including C5 truck parts. Support the seat and remove its floor boot/closeout before loosening; inspect witness marks, corrosion, washer seating and locknut condition during service. Witness marks are inspection aids, not the locking mechanism. No vibration, reuse or maintenance interval is claimed without an agreed qualification test.

## Assembly and unresolved interfaces

Build the collar around the crossmember before installing adjacent longitudinal seat rails. Prepare and clamp the external faces, complete the qualified groove seams and end welds, inspect, then fit and weld all twelve trimmed rail segments. Assemble the cap/cheek groove before the lower wing ribs obstruct it. Complete saddle and foot welds in a controlled fixture, inspect and coat, measure the actual steel-to-floor stack, machine matched spacers, install the trial seat and perform the qualified hardware procedure. Fit the flush steel floor transitions and final seals after structural inspection.

C45_20 has bottom closure Z476.35..482.7 mm and overlaps the baseline C5 sidebearer footprint. C5 is developing a collar-aware wear-track interface; no complete underframe collision-free claim is made. The C31 collar bottom must not be removed to clear a truck part without reanalysis. Final tool access, WPS/inspection, HSS local-wall effects, contact/prying/preload, fatigue, dynamic retention, floor acceptance and accepted vehicle load criteria remain review and test gates.

## Reproduction and sources

Run foundation_screen.py, rail_joint_study.py, joint_details_screen.py, collar_face_screen.py, floor_transition_screen.py and detail_verification.py with Python, NumPy and SciPy. write_geometry.py regenerates the canonical geometry JSON. The rail-end state file is also supplied compressed; all detailed load cases and assumptions are retained.

Primary sources checked 19 October 2026:

- Steel Tube Institute, [Design of Fillet Welds to Rectangular HSS](https://steeltubeinstitute.org/resources/design-of-fillet-welds-to-rectangular-hss/): effective length and no directional strength increase for these HSS welds.
- Steel Tube Institute, [Full-Capacity Welds: CJP vs. Fillet vs. Fillet-Reinforced PJP](https://steeltubeinstitute.org/resources/full-capacity-welds-cjp-vs-fillet-vs-fillet-reinforced-pjp/), November 2024: process-specific bevel, root land and fit-up guidance; no assertion that this custom joint is automatically prequalified.
- Steel Tube Institute, [Transverse Flange Plate Design Example](https://steeltubeinstitute.org/resources/hss-moment-connections-design-examples-transverse-flange-plates/), July 2025: local HSS limit states and chord stress interaction.
- [STANLEY Spiralock catalog](https://www.stanleyengineeredfastening.com/-/media/Web/SEF/Resources/Docs/Spiralock/Spiralock_Catalog_EN_NA_2.pdf), flange-nut table and torque/tension guidance.
- [Tekton SHD23019 drawing](https://images.tekton.com/assets/SHD23019_spec.jpg): actual socket envelope.
- [Portland Bolt SAE J429](https://www.portlandbolt.com/technical/specifications/sae-j429/), [F436 washers](https://www.portlandbolt.com/products/washers/hardened-round/) and [hex bolt thread lengths](https://www.portlandbolt.com/products/bolts/hex/).
- Mayuresh Patil, Georgia Tech, [Plate Theory](https://bpb-us-e1.wpmucdn.com/sites.gatech.edu/dist/f/1836/files/2021/11/Lecture27Plate.pdf), 2021: classical plate equilibrium, constitutive relations and Navier solution.
- Atlas A500 section property tables and the preserved C3 load-comparison source record remain applicable. AISC official full-specification downloads were inaccessible in this session; the accessible STI primary technical articles are identified above. No fabricated claim of having read the unavailable specification is made.

# C5 body attachment — R1 preliminary handoff

This is a concrete custom connection for design review, not a fabrication release. Dimensions are millimetres in the C5 local coordinate system. The controlled schedule is `body-interface-geometry.json`; reproducible load comparisons are in `body_interface_screen.py`, `body-interface-screen.json`, `body_interface_collar_screen.py` and `body-interface-collar-screen.json`.

## Physical load paths

The 240/180 mm spherical upper annulus bears against an 18 mm A572 Grade 50 candidate adapter, 280 × 440 mm, at Z464.7–482.7. Its outer edge has a proposed continuous 6 mm fillet. Two 10 mm external cheeks run 440 mm along the body bolster and 100 mm up its side faces. Their 6 mm base, top and end fillets provide a defined connection to the existing nominal 12 × 4 × 1/4-inch HSS. Vertical end seams avoid the nominal rounded corner. The supplied HSS wall, corner radius, seam, weldability and chord stresses still require verification.

Four M16 × 2 × 345 class 8.8 candidate bolts at X±18/Y±160 pass through Ø26/18 sleeves and the adapter. Each sleeve spans the full 304.8 mm body bolster depth; Ø28 root holes and flush annular partial-joint-penetration (PJP) end welds are defined. Each HSS outer surface receives a 45° × 3 mm countersink to Ø34, leaving a 1 mm radial root gap to the Ø26 sleeve. Fill is machined flush. Only 2.121 mm effective throat is credited in the comparison, subject to a qualified custom welding procedure; this is not asserted to be a prequalified groove. This is a distinct mechanical retention path. The calculation does not establish that the bolted and welded paths share load in a particular proportion, or qualify either as redundant. Upper sleeve welds must be prepared and finished to preserve a flat nut-bearing face and the required effective weld section.

The front negative-Y weartrack is pocketed to fit the unchanged C31 collar bottom. Its underside remains Z470.7, its general top Z482.7, and the pocket top Z476.35; 5.65 mm remains beneath the collar. The 280 × 150 mm track wings are attached with 12 mm gussets having 160 mm roots, 15 mm tips, and 6 mm double root/base fillets. Negative gusset centres are Y−540/−473; positive centres are Y465/535. The negative root weld has 3.8 mm nominal clearance to the collar end. These roots transfer force into the actual collar or bolster side faces. Local track bending, collar plate bending and HSS local capacity are separate unresolved checks.

## Defined development forces

The current truck allocation is 2,000 kg, with 1,400 kg unsprung. For attachment comparisons, the earlier 9,600 kg body allocation is deliberately retained for compression and horizontal force: the longitudinal CG offset probe gives 55.652 kN static per more heavily loaded pivot; 2× and 3× comparisons are 111.303 and 166.955 kN. The current 9,200 kg body would give lower values. Both independent horizontal components are ±14.122 kN. Their simultaneous use is a rectangular component envelope, not an asserted operating vector.

The separate lifting retention probe is updated to 2 × 2,000 kg × g = **39.2266 kN per truck**. This is not an operational uplift bound. Sidebearer vertical probes are 20 and 30 kN per pad. The screen retains the larger former 100 × 60 mm footprint through ±7° yaw, although the current pad is 100 × 50 mm. Both horizontal friction components are independently set to ±0.2R; their combined resultant exceeds a circular coefficient-0.2 friction cone and is intentionally conservative. The load acts at Z470.7, 12 mm below the gusset base at Z482.7; this offset is included in root/base weld and gross-root moments. No accepted load spectrum or fatigue category follows from these probes.

## Conditional comparison results

| Item | Result | Boundary |
|---|---:|---|
| Adapter 18 mm one-way overhang | 169.3 / 254.0 MPa at 2× / 3× compression | Uniform annulus pressure; rocking and nonuniform contact unresolved |
| Annulus mean pressure | 5.62 / 8.44 MPa | Mean projected-area pressure, not contact-fatigue approval |
| Adapter-to-cheek 6 mm weld | 37.9 / 52.7 MPa | Elastic full-group sharing |
| Cheek-to-parent 6 mm weld | 34.7 / 44.8 MPa | HSS parent-wall and chord interaction separate |
| Spherical upper annulus 6 mm weld | 40.5 / 57.7 MPa | Actual bearing material and welding procedure required |
| Main M16 ideal maximum tension | 24.644 kN | Lift plus both horizontal components; no compression/friction credit |
| Main M16 2× prying sensitivity | 49.288 kN; 313.9 MPa external thread stress | 2× is not a demonstrated bound; preload is additional |
| Sleeve flush PJP, 2.121 mm credited throat, at ideal tension | 142.24 MPa | Close to 144.79 MPa comparison; groove penetration and local wall remain held; no 2× pass |
| 30 kN negative / positive gusset root weld | 128.28 / 130.47 MPa | Independent full friction components |
| 30 kN negative / positive gusset base weld | 141.11 / 121.17 MPa | Force plane 12 mm below gusset base; negative side is close to 144.79 MPa comparison |
| 30 kN negative / positive gross gusset stress | 152.13 / 157.13 MPa | Both bending directions plus thin-rectangle torsional shear from the 12 mm vertical offset |
| Kingpin M12 2× sensitivity | 19.613 kN per bolt; 232.7 MPa | Four equal bolts, flange contact/prying unresolved |
| Kingpin internal thread simple shear | 84.42 MPa | Cylindrical approximation, not standard thread-stripping verification |
| C45_20 end weld: seat envelope + floor + 30 kN pad | 23.91 MPa | Rigid collar distribution; local load introduction unresolved |

E70 weld stress uses 0.6Fexx/2 = 144.79 MPa with no directional bonus. That is a stated comparison, not the selected railway acceptance criterion. Main bolt proof comparison uses the lower general class-8.8 proof stress of 580 MPa: 91.06 kN by area multiplication for M16 and 48.894 kN for M12. The manufacturer table rounds these to 91.0 and 48.9 kN and lists different structural-bolting values; no structural-bolting system certification is claimed. The sleeves would reach 329.4 MPa if loaded to the full nominal M16 proof load. That is not an allowed installation preload. Joint contact, stiffness, preload and local bearing require an integrated check.

The collar combined screen deliberately combines independent seat reaction maxima, a 450 lbf local floor load and the sidebearer probe. It is a sensitivity envelope, not a concurrent vehicle load case. Its 13.64 MPa equivalent distributed parent-wall transfer is not a parent-wall capacity result. It does not cover neighboring rail reactions or the complete body bolster.

## Hardware, locking and access

The main bolt steel grip is 322.8 mm: 304.8 mm sleeve/body depth plus 18 mm adapter. With the 3 mm lower washer, the underhead datum is Z461.7 and the 345 mm bolt tip is Z806.7. The STANLEY Spiralock M16200M nut has a 34.5 mm maximum flange, 24 mm AF and 15.3–16 mm height. It bears directly on the finished upper face; no upper washer is included. Minimum nominal projection is 3.2 mm, or 1.6 thread pitches. Bolt length, thread runout, coating, nut tolerance, certified compatibility and supplier installation procedure remain procurement gates. No torque is issued.

The kingpin flange is Z448.7–464.7. Four M12 × 1.75 × 35 bolts use 2.5 mm washers and a 2 mm common bend-tab plate beneath the 16 mm flange. Nominal engagement in through-tapped adapter holes is 14.5 mm, leaving 3.5 mm tip clearance below the adapter top. The Ø150/52 tab plate has four Ø14 holes and integral tabs bent against head flats after qualified tightening; tab material and durability remain to qualify. The separate lower retention washer remains Z190.7–206.7 with its 8 mm nominal gap.

Two actual floor hatches at Y±160 provide access to the upper nuts. Each has a 200 × 120 × 8 mm flush cover at Z804.8–812.8, a 6 mm steel base with a 90 × 60 mm central tool opening, and an 11.3 mm high perimeter standoff. Four M6 × 1 × 16 countersunk candidate screws provide nominal 8 mm engagement and 3.3 mm bottom clearance. Two Ø22 × 4.5 mm blind underside pockets clear the M16 tips by 2.6 mm nominally and leave 3.5 mm plate. This residual thickness and the supported floor assembly remain a local floor proof hold. The cover must not bear on the bolt tips. A 34 mm reserved socket envelope fits the opening by 10 mm at the outer X edge; it is a design reservation, not a claimed manufacturer tool dimension. Complete upper/lower tool insertion, counterhold and body/truck clearance remain subject to the combined CAD check.

Assembly requires an independently supported body and removed truck for structural welding or major fastener replacement. Sleeve fit, weld access, bore alignment, flush bearing surfaces, adapter/cheek distortion and bearing concentricity must be controlled before coating. Inspect welds before sealing or closure. Install bolts to the qualified supplier preload process, apply witness marks, form fresh locking tabs, then fit sealed flush antislip covers and verify tip clearance. Final weather/fire-compatible seals, coating restoration, inspection intervals and replacement criteria remain open.

## Primary sources

- [Bossard, January 2025 screw properties and proof loads](https://assets.eu.ctfassets.net/0vp0u5uh75zd/1VPwGxSRcAQdDRArMtTqeY/8fe01cf6ef692e134b45f895fb69fe97/012_016_Screws_property_class46_Fastening_EN_01_2025.pdf): inspected current pages 12–14 for class 8.8 and stress areas. Earlier Bossard URLs returned 404 and are not the evidence link.
- [STANLEY Spiralock catalog](https://www.stanleyengineeredfastening.com/-/media/Web/SEF/Resources/Docs/Spiralock/Spiralock_Catalog_EN_NA_2.pdf): M16200M catalog geometry and compatibility; installed-joint behavior is not inferred from nut dimensions.
- [Steel Tube Institute, design of fillet welds to rectangular HSS](https://steeltubeinstitute.org/resources/design-of-fillet-welds-to-rectangular-hss/): weld and parent-HSS limit states are distinct.

Accepted railway loads, fatigue, local HSS and collar behavior, nonlinear bearing/contact, qualified fastening processes, actual supplied material and the complete body/truck proof remain unresolved. These are limits of this handoff, not hidden assumptions of a passed assembly.

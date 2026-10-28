# C55 first-brake strength-gap review

**No metal change or mounted-brake rating is justified yet.** The exact maximum service and parking outputs remain unconfirmed, and simultaneous service/spring action has not been excluded by a selected anti-compounding circuit. The controlled WABCO 40175072 GA, callout 1, limits the specified carrier connection to 10 kNm; this is not an actuator-output or combined-force cap. The final input envelope must remain within that connection limit. Reinforcing custom metal cannot raise the OEM limit.

The largest reported nominal metal stress is at the 100 mm axle/hub key contact; 30 mm pin bending and the web-to-barrel weld also need material-based limits. Their actual capacity ranking is unresolved because the relevant allowables are unspecified. The largest unresolved mechanism is the split hub/shaft load path; the mounted bearings also need low-load, fit and thermal-clearance disposition before their catalog ratings can be used.

## Load-dependent screens

With T in kNm per disc, the existing pose grid gives the following upper screens. They include the separate 50 kg gravity probe at its assumed CG; actual shock, actual mass/CG and any smaller pad radius require new calculation.

| Item | Demand expression | 10 kNm reference |
|---|---:|---:|
| Outer radial bearing |15.54491T + 0.68158 kN |156.13 kN actual grid |
| Pin combined stress |22.43944T + 1.10013 MPa |225.49 MPa actual grid |
| Key projected bearing |34.7222T MPa |347.22 MPa |
| Key shear |9.92063T MPa |99.21 MPa |
| Web/barrel candidate 6 mm fillet |14.9024T MPa, braking resultant only |149.02 MPa |

There is no approved allowable for the key, pin, custom plates, hub or welds. The key allowable must cover the weakest of shaft, key and hub contact material; a harder key alone does not qualify the other two. The rotor-bolt and split-joint load paths need separate equilibrium and preload/contact calculations.

## Catalog-based torque thresholds only

SKF static-factor guidance varies with load certainty and tolerated permanent deformation. For continuous motion with low load certainty, its table gives progressively stricter factors 2.5, 3 and 4. Those factors produce these conditional radial-bearing thresholds using 255 kN C0 and the bound above:

| Static factor | Conditional torque ceiling |
|---:|---:|
| 2.5 |6.518 kNm |
| 3 |5.424 kNm |
| 4 |4.057 kNm |

These are bearing static checks, **not system ratings** or an adopted operating pressure. Catalog dynamic C=99 kN is not an allowable force. Bearing life requires the rotational duty/load spectrum, lubrication, contamination and temperature; SKF basic roller life uses (C/P)^(10/3). [SKF static guidance; SKF life]

SKF also estimates minimum loads of **1.98 kN radial** and **0.340 kN axial** for these selected bearings. The current 50 kg coasting probe gives outer radial no more than 0.682 kN and nominal axial zero. Obtain supplier disposition for low-load coasting and the actual speed/grease before retaining the arrangement. Do not cure this by an uncalculated hard preload. [SKF minimum load]

## Correct the screw screen before using it

The exact M14×1.5 fine thread has catalog tensile area 125 mm²; C54 used the 115 mm² coarse-thread value. If threads cross the plate/caliper shear plane, a plain 14 mm shank area is also inappropriate. Basic external-root geometry gives 116.13 mm²; the actual screw tolerance and thread root still need its drawing. [M14 fine thread]

| Disc torque | Plain-shank shear | Basic thread-root shear | Axial external-load stress using 125 mm² |
|---:|---:|---:|---:|
|1 kNm | 10.28 MPa |13.63 MPa |3.67 MPa |
|3 kNm |30.84 MPa |40.88 MPa |11.01 MPa |
|6 kNm |61.68 MPa |81.77 MPa |22.02 MPa |
| 10 kNm | 102.80 MPa |136.28 MPa |36.69 MPa |

These are external-load stresses, not preload or bolt-connection acceptance. The controlled GA specifies Albion NJJ4163 screws with 18 mm wrench size, M14×1.5 grade 10.9, oiled; it requires 205–225 Nm tightening in the specified order and 18 mm minimum engagement. A 30 mm screw through 12 mm plate supplies only 18 mm nominal penetration; the GA does not establish the available full-thread depth or entry chamfer. Verify the worst-case stack and bottoming before selecting length. The two smallest crescent edge ligaments are only 6.578 mm; actual plate prying/bearing/breakout analysis must replace arbitrary strip probes. [WABCO carrier interface]

## Specific closure work

| Connection | What must close |
|---|---|
| Keyed axle and split hub | Specify shaft/key/hub material condition and keyway roots. Solve both hub halves, split-screw preload/contact and rotor attachment. Recheck rotating axle bending/fatigue under wheel loads and brake-bearing reactions; pure torsion is insufficient. |
| Needle-bearing seats | Specify 100/120/150 mm fits, split closure, seat roundness/stiffness and post-weld machining. Verify residual internal clearance at hot/cold limits and supplier low-load suitability. |
| Opposed thrust stacks | Replace zero nominal axial clearance with a controlled measured end-float/preload design. The 175 mm path changes 0.21 mm for an illustrative 100 K steel differential; this is not a proposed tolerance. Include thermal force when checking covers, M4/M6 retention and collars. |
| Carrier and frame welds | Establish actual accessible bead paths, WPS/base metals/filler and fatigue detail. Analyze supporting barrel wall, 12 mm side webs and local plates with existing truck loads. Add caliper/chamber gravity and shock at real CG. Full 19,348.8 mm² endplate backing proves contact only. |
|30 mm pins and retainers | Establish material/heat treatment, contact/clearance and bending fatigue. The 45 mm support-span model is bending-controlled. Select and verify actual cotter/washer retention. |

The exact 9253800250 chamber catalog mass is 7.0 kg, but its controlled CG is unavailable. A shell-envelope centroid cannot substitute for it. Fit selection must account for ring expansion, seat discontinuity, temperature and remaining bearing clearance. [SKF fits]

## Concrete bearing-mount simplification to assess

A one-piece OD 120 / ID 100 mm sleeve still cannot pass the retained Ø110 mm wheel seat after wheel removal. That axle shoulder is why a split reducer is needed.

A continuous OD 120 / ID 110.5 mm outer sleeve over a uniform split Ø100→110.5 mm inner adapter could give continuous bearing/seal seats and avoid the five stepped assembly stages. Its outer wall is only 4.75 mm: sleeve distortion, both interface fits, creep, axial backing and thermal clearance need analysis before adoption. A revised axle with integral Ø120 mm bearing/seal seats would eliminate both reducer interfaces, but requires a new axle drawing, transitions and fatigue review. Neither concept is a released geometry change.

## Completion sequence

1. Freeze the exact package and upper service, parking and combined/fault loads; use lower friction/force separately for required stopping and grade holding. Include pressure protection, real mass/CG and duty.
2. Resolve bearing minimum-load/seat/axial-clearance questions and specify materials, fasteners and weld criteria.
3. Recalculate all local connections and axle fatigue at those bounds; change only parts that fail an explicit criterion.
4. Build one reviewed development installation and verify assembly, cold/hot drag/end float, runout, retention and mount deflection at an agreed proof load. Complete the defined thermal/cyclic test and inspection; a static proof does not demonstrate fatigue life.
5. Repeat the installation only after that evidence closes.

## Evidence

Reviewed C54 BREP: `b6b69ce320f0c9784d3920b1f536ae7e7a7254beca531cdab801303b2e7b4337`. C54 CAD/public files were not modified. The JSON preserves exact demand coefficients, source facts, hashes and unresolved inputs.

- SKF static guidelines: https://cdn.skfmediahub.skf.com/api/public/0901d196802809de/pdf_preview_medium/Rolling_bearings_-_17000_1_EN_pdf_preview_medium.pdf; page 107
- SKF minimum load: https://www.skf.com/binaries/pub12/Images/0901d196803e7d9e-Catalogue---Needle-roller-bearings-06003-EN_tcm_12-271146.pdf; page 33
- SKF fits: https://cdn.skfmediahub.skf.com/api/public/0901d1968024f02a/pdf_preview_medium/0901d1968024f02a_pdf_preview_medium.pdf
- SKF life: https://cdn.skfmediahub.skf.com/api/public/0901d19680495562/pdf_preview_medium/0901d19680495562_pdf_preview_medium.pdf
- M14 fine thread: https://www.bossard.com/-/media/bossard-group/website/documents/technical-resources_old/screws-property-class-46-to-129.pdf; page F.041
- WABCO carrier interface: ../coach-brake-c54/source-evidence/wabco40175072-GA.pdf

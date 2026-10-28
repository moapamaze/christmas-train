# C55 exact chamber research

**Decision: retain WABCO9253800250/9253800240 as the legacy PAN17/WABCO232/20-24 engineering reference. This is a hold, not a purchased-package or fabrication release.** Research date:2026-10-20. No supplier messages or purchases were made.

ZF now publicly lists9253800460 as the open-hole alternative to0250, and9253800450 to0240. This is an exact manufacturer relationship, recovered from the public product page’s `extendedModel.extProdData.AlternativeProductsInfo`; it is labelled an alternative, not a formal supersession. The new family drawing explicitly includes0460/0450. It does not provide the missing guaranteed maximum force data or establish readily available stock of the exact pair. Therefore it is a credible replacement candidate, not a reason to silently substitute another chamber in C55.

| Item | Controlled or verified evidence | Remaining limit |
|---|---|---|
| Service/spring pressure | Both GAs specify8bar working and10bar temporary | Temporary duty/duration and maximum transmitted force unknown |
| Service output | Informational curves at1.38,2.76,4.14,5.52 and6.59bar | No guaranteed maximum at8 or10bar; no extrapolation used |
| Parking output | LegacyGA has informational spring plots | No certified full-stroke maximum/tolerance bound; newGA has no parking plot |
| Compounding | ZF iEBS manual§4.2.6 describes a system function preventing additive chamber forces | Coach circuit and fault behavior unselected; intrinsic chamber protection not established |
| Mass |0250catalog7.0kg;0460catalog7.2kg | Exact CG/inertia and supported assembly CG not supplied |
| Mount |120.7±0.3mm stud pitch, M16×1.5,43mm projection,15±0.5mm R8 pushrod | Exact caliper mating centre, torque-policy resolution and tolerance stack remain open |
| Ports |3/8-18NPTF,97/116mm axial stations,89mm above axis and±25mm lateral offsets in main view | Which real boss is cast11/12, tap depth and fitting insertion remain open |
| Caging |89mm rear projection drawn | Full removal/wrench/hand envelope not controlled |

The main0460/0450 envelope matches the published legacy dimensions:240.5mm mount-face-to-body-end,Ø184maximum circular body,Ø158.5rear shell,Ø153front,Ø54×4.1pilot andR110stored-hardware bound. The selected0460 row has300°port clocking;0450 has60°; both clamp angles are270°. The new rear shell has fourØ6breather holes and an explicitly labelled1/2ACMErelease mechanism. These details and drainage attitude still require exact-variant verification before substitution. Catalog package-size fields were not used as body dimensions.

The89mmport-face dimension supports C55’s correction of the earlier88mmplacement. It does not close guessed boss topology or service/spring hose identification. The caliper chamber-axis radial coordinate191.5mm and9°inclination are dimensioned; the existing axialq134.011mm placement remains a provisional interpretation of the129.6mm endpoint, not a controlled OEM datum.

The iEBS anti-compounding function feeds release air into the spring chamber during service application. It belongs to the brake control system. An internal breather valve does not prove anti-compounding. Simultaneous and fault loads therefore remain in the unresolved structural load envelope. Nominal20-square-inch chamber area, another PAN17 variant’s ratio, family torque ratings and generic spring warnings were not used as substitute maxima.

## Availability and package choice

The fresh Country Supply page at the oldS-38724-LURL now displays **S-42279-L,[price removed]In stock**, while the description still namesS-38724-L. This supersedes the earlier observed out-of-stock page, but the conflicting part labels cannot establish0250or0460stock. No manufacturer mapping forS-42279-Lwas found. FleetPride’s0250listing reports no displayed pickup/shipping availability forDallas75247. ZF’s active catalog/login/cart fields are not inventory confirmation. No exact0460/0450pair stock or lead time was verified.

Current HendricksonL949identifies2224TLD2H-4627/-4628 asS-40979-L/R. The newerL1259RevH ordering guide calls forWABCO238with22/24;L949’sS-41159-1pad kit isWABCO232. Exact238kit, exact22/24GA and maximum-force data remain absent. These packages must not be mixed. TSE2016HTND2-3710has a manufacturer-listed8-week lead time but different5/8-11UNCstuds and no verified complete exactPAN17substitution; it is not adopted.

## Unsent manufacturer request

The public0250product page verifies `naspecs.zf@zf.com` for specifications and `nacustomercare.zf@zf.com` for technical support. The following is a prepared request only; it has not been sent.

Subject: Exact PAN17 brake package and TRISTOP 9253800250/0240 or 0460/0450 engineering data

To: naspecs.zf@zf.com
Cc: nacustomercare.zf@zf.com

We are developing an air-service, spring-parking brake installation for a passenger-coach rail truck. The current engineering reference is PAN17 calipers 40175072/40175073, the historical Hendrickson WABCO232/20-24 package, and WABCO chambers 9253800250/9253800240. This is a custom application and is not being represented as an approved road or rail installation.

Your public catalog lists 9253800460 and 9253800450 as open-hole alternatives. Please confirm whether these exact parts are approved replacements in this exact caliper/pad package, identify every changed mating or brake component, and advise current production status, authorized supply route, exact stocked SKU and lead time. We have not ordered parts.

Please provide controlled drawings/CAD and guaranteed engineering data for the selected exact suffixes:

1. Service pushrod force versus stroke at 8 bar working pressure and 10 bar temporary pressure, including maximum and minimum tolerances, return-spring effects, temperature variation, permitted temporary-pressure duration/duty, and the maximum physically transmitted output force. The public GA graphs stop at 6.59 bar and are marked informational.
2. Parking-spring output versus the full usable stroke with maximum/minimum tolerances, release-pressure limits and residual output during partial release. Include allowable simultaneous service/spring loading, worst-case compounded output, and the required anti-compounding circuit and fault assumptions.
3. For 40175072/40175073 with the exact approved pad compound and 325 mm rotor: allowable chamber input force/stroke, pushrod-to-clamp transfer relation including efficiency and tolerances, service/parking torque limits and relevant friction bounds. Please identify whether the newer 22/24 plus WABCO 238 package is required and give exact replacement SKUs if so.
4. Exact chamber mounting-face centre relative to the caliper carrier/axle datum, hole/pilot tolerances, pushrod contact geometry, permitted flange gap, fasteners and final nut torque. Please reconcile the chamber GA 169.5–203.4 Nm range with the caliper GA 180–210 Nm range and confirm the applicable no-washer instruction.
5. Controlled physical identification of port 11 (service) and port 12 (spring release) at the 97 mm and 116 mm axial stations; tap depth, boss envelope and permissible fitting insertion/torque; port 300-degree versus 60-degree handedness; and permissible installed attitude, bottom-breather opening and drainage requirements throughout suspension travel.
6. Full caging-bolt storage/removal/release sweep, wrench and hand access, clamp hardware projection and permissible service procedures. The drawn 89 mm projection alone does not establish removal/tool clearance. Confirm relevant differences between the legacy and open-hole mechanisms.
7. Exact chamber and supported caliper masses, centres of gravity/inertias, permitted vibration/shock environment, mounting-fatigue limits and any application limitations affecting this passenger-coach rail installation.

Please identify the document revision and exact part suffix covered by each answer. We can supply the installation section and suspension/wear envelope for application review once the controlled mating data is established.

Thank you.

## Evidence register

- **ZF0250** — [manufacturer exact product page](https://www.wabco-customercentre.com/catalog/en_US/9253800250); SHA-256 `f1896cb11c015960b5331bd6fb54f98ea6fcb4b2dcd16b2d480c2d11c75b9391`
- **ZF0240** — [manufacturer exact product page](https://www.wabco-customercentre.com/catalog/en_US/9253800240); SHA-256 `06e78c42d71431683233494ed46aa2891177362991487b5271d917943941e0cb`
- **ZF0460** — [manufacturer exact product page](https://www.wabco-customercentre.com/catalog/en_US/9253800460); SHA-256 `f1653701306e443c291c9e12c1bc3a215307168f8b25b1c6f2b5e3ab817a7afb`
- **GA0230** — [manufacturer controlled family drawing including explicit 0250/0240 rows](https://www.wabco-customercentre.com/catalog/docs/9253800230____053_dascheck_l4_page-1---notset_tif.pdf); SHA-256 `92981a1e051a4c5704615cf832b52f948d8f90cab4fdaf33099422b152fbd53f`
- **GA0420** — [manufacturer controlled family drawing including explicit 0460/0450 rows](https://www.wabco-customercentre.com/catalog/docs/9253800420____053_dascheck_-3_page-1---notset_tif.pdf); SHA-256 `0ab91185498703dcd8e0025fcdbd77934e878150167a908bd98dffce7f534b91`
- **ZF_iEBS** — [manufacturer system description; section4.2.6 printed page110](https://www.wabco-customercentre.com/catalog/docs/8150102523.pdf); SHA-256 `a5d98632572feabb0458b8545d0c7ebaf0469b15c9686031296b905588b77d3d`
- **ZF_install** — [manufacturer chamber installation service hint](https://www.wabco-customercentre.com/catalog/docs/doc000132_ml.pdf); SHA-256 `75f0453a6add4f7fab58a7d59d5a90e1a59bb3f1b6e1cb07b91f45772f434452`
- **legacyOEM** — [historical OEM exact PAN17 chamber package](https://digital.hendrickson-intl.com/view/513311/365/)
- **L949T** — [current OEM catalog; PAN17 22/24 chamber table p15 and232 pad table p11](https://www.hendrickson-intl.com/getattachment/54c582a0-10e2-4fe2-9e8f-f4e33f9fccb4/L949.pdf)
- **L1259H** — [OEM ordering guide RevH Oct2026; current PAN17 238/22-24 package; exact238 kit unresolved](https://www.hendrickson-intl.com/getattachment/c1e7664c-224b-4f6f-bbed-918851ac5d31/L1259-Rev-H-PAN17-Ordering-Guide-WEB.pdf)
- **Sealco** — [manufacturer system-function explanation; not selected coach circuit](https://sealcocvp.com/?catalog=compounding-anti-compounding-feature)
- **CountrySupply** — [seller availability only; conflicting exact-SKU labeling](https://www.country-supply.com/product/hendrickson-brake-chamber-type-20-24-left-s-38724-l/)
- **FleetPride0250** — [seller availability only](https://www.fleetpride.com/parts/wabco-diaphragm-9253800250)
- **TSE3710** — [manufacturer alternative candidate, not selected](https://www.tsebrakes.com/brake-chambers/hot-high-output-technology/2016HTND2-3710)
- **TSE2026** — [manufacturer family brochure; not exact4627/4628 qualification](https://www.tsebrakes.com/medias/iw/TSE-SalesSheetsTSE-HOT-Web-2026.pdf)
- **TSEinstall** — [manufacturer generic installation guide; not WABCO instructions](https://www.tsebrakes.com/medias/iw/TSE_Disc_Brake_Installation_Instructions_1_1_1.pdf)

The JSON report contains exact source hashes, the manufacturer alternative mappings, machine-readable unresolved force fields and the complete request. The retained C54 controlled drawings remain unchanged.

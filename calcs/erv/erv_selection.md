# PF-CT coach ERV selection (rev L2 + ERV)
Pulsipher Farms Christmas Train — preliminary, not for construction until PE stamped

## Fresh-air sizing (ASHRAE 62.1-2022 Table 6-1 style, see erv_sizing.py / .json)
- Rp 3.8 L/s·person, Ra 0.3 L/s·m², cabin 20.5 m², Ez 1.0 (low-level side supply) — rates ASSUMED as transportation-waiting analogue, PE to confirm.
- Regular coach (33 occ.): 131.5 L/s (279 cfm). Accessible coach (14 occ.): 59.3 L/s (126 cfm). Train 454 L/s vs plan 847.5 L/s.
- Required recovery effectiveness to hold 34.4 kW at plan OA: 0.344 (incl. ERV fan power); 0.393 at COP 3. At 62.1 OA the no-ERV demand is 32.19 kW (ERV not needed for the limit, kept for margin).

## Selected: RenewAire HE05IN (one per coach, low clerestory roof pod, top ≤ 3,450 ARL)
- 120 V 1-ph 60 Hz; 120–375 cfm; 2 × EC motors (≤ 343 W on the submittal curve); 880 × 956 × 307 mm; 43 kg.
- Static-plate enthalpy core, AHRI 1060 certified core L62-G5. Effectiveness at 300 cfm / 43 °C not in the submittal → ε 0.55 ASSUMED, AWAIT RenewAire selection printout.
- Why roof pod: no ceiling plenum (≈102 mm), end-hood pocket 1,217 × 544 × 431 mm too shallow. Separate OA/EA louvres (62.1 Table 5-1), PE to confirm separation.
- https://renewaire.com/product/he05in/ · https://renewaire.com/wp-content/uploads/2025/05/Submittal-HE05IN-Feb2025.pdf

## Alternatives considered
| Unit | Power | Airflow | Effectiveness | Size / mass | Why not | Link |
|---|---|---|---|---|---|---|
| Mitsubishi Lossnay LGH-F300RVX2-E | 208/230 V | 300 cfm | enthalpy cooling 50 % at 300 cfm | 331 × 1063 × 1046 mm, 34 kg | intake limit 40 °C / 80 % RH < 43 °C design | https://www.mitsubishitechinfo.ca/sites/default/files/SB_LGH-F300RVX2-E_202411_0.pdf (not verified from box: TLS error) |
| Fantech ATMO 300E-EC | 120 V | 301 cfm at 0.4 in | TRE 58 % at 178 cfm (cooling) | 546 × 606 × 430 mm, 27 kg | residential, too tall for a low pod | https://www.fantech.net/en-us/products/fresh-air-appliances/atmo |
| Panasonic FV-10VEC2 | 120 V | 100 cfm | TRE ≥ 60 % at 49 cfm | 724 × 584 × 225 mm, 22 kg | 3 per coach needed | https://iaq.na.panasonic.com/erv/intelli-balance-100-any-climate-corded |
| Daikin VAM650J | 230 V 50 Hz | 650 m³/h | enthalpy cooling 59–73 % | 368 × 1354 × 920 mm, 61.5 kg | 50 Hz only | https://www.daikin.co.uk/content/dam/dauk/document-library/data-sheet/ac/Ventilation/VAM-J_Datasheet_1072.pdf |
| 12/24 V DC units | — | — | — | — | none found at ~280 cfm | — |

No prices in this file (owner Costs Page only).

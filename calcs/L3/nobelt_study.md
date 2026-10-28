# No-belt drive study (28 Oct 2026) - STUDY ONLY (site, drawings, zip unchanged)
Envelope: build/model.py `nobelt_option_prims()` / `nobelt_envelope_check()` (appended; not called by the drawing build).
Run: `python3 calcs/L3/nobelt_study.py` -> nobelt_study.json. Gaps are bounding-box (conservative); <0 = clash.

| Option | Fit (min gap) | Start pull vs 31.5 kN | Gearbox / chain margin | Major parts per axle | Verdict |
|---|---|---|---|---|---|
| (a) TA7315H clocked, H1B110 in line | FAIL at every angle (-36 to -64 mm: horn cheek / wheel rim) | 37.9 (adh-capped) | as L3 | - | no |
| (b) H1B080 SAE/DIN in line | FAIL (-26 mm horn cheek) | 32.0 @350 bar (1.01) / 36.6 @400 (1.16) | TA ok | - | no |
| (b') H1B080 cartridge, input straight down, Dodge-shortened input shaft (Y+40) | +14 mm (axlebox); disc must move to Y+20..45 and shrink to Ø320 | 32.0 @350 (1.01) / 36.6 @400 | TA ok | ~7 | only with 3 vendor specials; not recommended |
| fixed 80 cc bent-axis, input down | +25 mm | 32 | TA ok | ~7 | top speed ~4.5 mph - fails 6 mph |
| (c) TA 5:1 + MS05 in line | FAIL (-62 to -128 mm) | 37.9 | 0.65-0.79 use (AWAIT Dodge <90 rpm) | - | no |
| (d) helical-bevel shaft-mount (NORD SK 9082.1 / SEW KA157) | housing +35; H1B motors from both axles clash (-69) unless staggered | 37.9 | SK9082.1 0.85 / KA157 0.61 at adhesion x1.6; SK9072.1/KA127 1.29 = overload | ~5 | 600-700 kg per axle, Ø110 seat (SK9082.1) - no |
| CHAIN: MS05 468/234 2-speed + brake, ANSI 120-2 15T/45T, no gearbox | +15 sprocket, +25 motor/transom, guard +3 to spring reservation (notch) | 37.9 (theory 38.5; 33.0 @300 bar) = 1.20 | chain SF on ultimate 10.2 at slip, 7.9 at relief | ~7 | RECOMMENDED if owner accepts chain upkeep |
| L3 belt (current) | fits | 37.9 | as approved | ~11 | fallback |
| L2 custom spur case | fits (earlier study) | marginal start eta | custom | many machined | last |

Chain details: Ø546 PD axle sprocket (OD~580) on a pressed hub (no keyway), 15T motor sprocket (PD183), centres ~450 mm (11.8 pitches, short - faster wear),
wrap 132 deg, chain 1.0 m/s at 6 mph, pull 25.2 kN at wheel slip / 32.7 kN at relief. Motor on truck frame (sprung); horizontal chain line so
spring travel 25 mm changes centres <1 mm. 6 mph: motor 106 rpm, 104 L/min in small displacement -> pump stop ~42 cc; full displacement ~3.8 mph.
MS05 T04 brake: park 52 kN (need 23.2), emergency 45 kN (max 10 uses) - keep axle disc + calipers for service/emergency.

# C5.6 air hardware — source review

Use the Parker 271-6 hose with a fixed-side **17B25-8-6B swivel**, **017M-6-8B adapter** and **207ACBH-6 anchor coupling**. The swivel permits disconnection without rotating the hose. The 25 Series catalog confirms the hose/end family; this does not qualify the whole railway installation.

| Part | Source-controlled dimensions | Remaining uncertainty |
|---|---|---|
| 10125-6-6B-VS | 3/8-18NPTF; A44, B25mm; AF17.4625mm | Shell OD, segment lengths, engagement |
| 17B25-8-6B | 3/4-20UNEF; A40, B22mm; AF22.225mm | Mated overlap, shell OD and crimp |
| 017M-6-8B | 3/8-18NPTF to3/4-20UNEF; L29mm; AF19.05mm | Engagement and hex length |
| 207ACBH-6 | BodyL33.274; bodyAF28.575; nutAF31.75; hole25.4; max panel15.748mm | Exact body/nut axial widths and locking |

A/B drawing datums are recorded in the JSON. B locates the shell region, **not the hose cut end**. Do not add overall lengths without joint overlap. The Karrykrimp2 reference table separately gives22.225mm hose insertion for25Series/-6; with shell endx314, the reference cut end isx291.775 rather thanx296. An older UK anchor table rounds L to34mm: retain the selected US table rather than mixing regional dimensions.

Use **STAUFF319-SA87-H** as a sliding hose guide: Ø19 bore; body50×30×35.5mm; bolt pitch33mm. Pair with SP-3-M-W2 base50×30×3mm (Ø12 bosses projecting6.5mm), DP-3-W3 cap48×30×3mm with Ø7 holes, and two M6×40 grade8.8 bolts. Bore mid-height17.75mm is inferred from drawing symmetry; relief-pocket details remain simplified. The manufacturer specifies sliding installation, not axial/torsional anchoring. Its PP/PA torque table does not qualify this elastomer guide.

The proposed fixed-end8mm NPTF and7mm swivel overlaps are **installation scenarios**, not manufacturer values. The manufacturer Karrykrimp2 reference chart gives die80C-Y06/silver85C-R01 and0.680–0.700in(17.272–17.780mm) across the crimp flats. That does not define the full shell/flare maximum OD, and current CrimpSource production verification is still required. Final thread engagement, hose cut length, pressure flex, guide torque, full movement and exact chamber circuit identity remain open. Catalog presence is not inventory confirmation.

Sources: [Parker4400 pp51,63–64](https://www.parker.com/content/dam/Parker-com/Literature/Hose-Products-Division/Catalog-4400-PDF-Files/HPD_4400_Catalog.pdf); [Parker0700 N40/PDF42](https://www.parker.com/content/dam/Parker-com/Literature/Literature-Files/pneumatic/Literature/FRL/0700P/0700P_Tubing_Fittings.pdf); [STAUFF catalog pp15,20,28,178,185](https://cdn-assets.stauff.com/pdfcatalogs/en/STAUFF-Catalogue-1-STAUFF-Clamps-English.pdf); [exact guide](https://stauff.com/en/products/1130006811).

Additional source: [Parker Karrykrimp2 bulletin4480-T31 pp9–10](https://www.parker.com/content/dam/Parker-com/Literature/Hose-Products-Division/Karrykrimp2-Technical-Manual-4480-T31.pdf).

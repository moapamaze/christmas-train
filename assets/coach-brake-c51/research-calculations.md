# C5.1 brake architecture: independent force and heat comparison

This issue calculates working demand for the current **13,200 kg regular** and **11,000 kg accessible** upper coach allocations, four axles per coach and nominal **600 mm wheels**. It does not select a brake, establish component strength or approve operation. The 5% rotational-inertia allowance is assumed; actual wheelset and brake inertia remain unknown. No superseded empty-coach mass is used.

Level-track demand (zero grade):

| Coach | Deceleration | Torque per axle | Torque per wheel | Tread tangential force per wheel |
|---|---:|---:|---:|---:|
| Regular | 0.5 m/s² | 519.750 Nm | 259.875 Nm | 866.25 N |
| Regular | 0.7 m/s² | 727.650 Nm | 363.825 Nm | 1212.75 N |
| Accessible | 0.5 m/s² | 433.125 Nm | 216.562 Nm | 721.88 N |
| Accessible | 0.7 m/s² | 606.375 Nm | 303.187 Nm | 1010.62 N |

For the regular coach at 0.7 m/s², a single tread shoe needs **8.085 / 4.851 / 3.465 kN normal force per wheel** for assumed block friction of **0.15 / 0.25 / 0.35**. These are lining sensitivities, not selected coefficients. An ideally equalized opposed clasp arrangement uses the same total normal force, divided between its two shoes.

One disc per axle carries the full axle torque. At effective contact radii of 150 / 175 / 200 mm, the regular 0.7 m/s² case requires total tangential pad forces of **4.851 / 4.158 / 3.638 kN**. Effective radius is the torque-weighted radius of the actual pad contact, not simply rotor outer radius. Pad-normal force requires a selected pad friction coefficient. Supplier “clamping force” conventions must be checked because some describe a per-face force and others the summed force.

At 7.5 mph on level track (zero grade), full-stop heat input is:

| Coach | Whole coach | Per axle / one disc per axle | Per wheel / two equally sharing discs per axle |
|---|---:|---:|---:|
| Regular | 77.902 kJ | 19.475 kJ | 9.738 kJ |
| Accessible | 64.918 kJ | 16.230 kJ | 8.115 kJ |

Heat input does not establish temperatures, fade or cooling. Tread braking puts heat into the wheel and requires compatible wheel material, tread profile and friction blocks. Disc braking transfers the friction duty to a rotor but still requires a qualified rotor, hub and caliper installation.

A single shoe at the front or rear point on the horizontal wheel diameter applies a vertical friction force as well as its horizontal normal force. At 0.7 m/s², the regular-coach vertical component is **±1.213 kN per wheel**, approximately **7.50%** of the ideal static wheel load; the accessible-coach component is ±1.011 kN at the same percentage. Travel direction changes the sign. These are isolated force components, not predicted wheel unloading. An opposed, equally loaded clasp can cancel the force resultants while adding braking torque; real friction, wear and rigging imbalance must be considered. At other shoe angles, the normal force also has a vertical component.

**Suspension tracking is separate from wear adjustment.** A slack adjuster manages stroke consumed by wear. It does not establish shoe or caliper alignment through the current +35 mm jounce, −40 mm regular / −30 mm accessible rebound, axle tilt and lateral movement. A tread arrangement needs defined hangers or a suitable flexible brake unit. A disc arrangement needs a defined suspended/floating or axle-following caliper support. A drop-prevention catcher is not automatically a second functional brake or independent torque path.

**Maximum actuator output sets the mounting load.** No actuator, lever ratio, maximum pressure or spring-parking force curve is selected here. Once selected, the maximum credible output—including pressure faults, stroke, tolerances, reverse operation, unequal/seized shoes and permitted service/parking superposition—must determine the beam, hanger, pin, bracket, hub and axle loads. The working torques in this table must not be used as those component load limits. A service-only air chamber does not satisfy the separate spring-parking requirement.

The companion JSON contains four working cases, twelve tread-friction cases, twelve effective-radius disc cases, full formulas, source hashes and 36 arithmetic consistency checks. These checks verify arithmetic only. Current C5 mass and wheel inputs are taken from `dist/assets/coach-truck-c5/design-record.json`; the retained speed/deceleration comparison is documented in `dist/assets/brake-selection-l2/calculations/brake_selection_inputs_R0.json`.

Manufacturer context: [Knorr-Bremse TreadAct Compact](https://rail.knorr-bremse.com/media/2000_products/2900d_product_broschures/p-1302_treadact_compact.pdf) and [Wabtec bogie brake equipment](https://www.wabteccorp.com/transit-rail/braking-systems/bogie-brake-equipment). These establish available railway architectures, not fit or acceptance for this coach.

A documented actuator example is [ZF WABCO 4231040170 Type 16](https://www.wabco-customercentre.com/catalog/docs/4231040170____005_drw_c6.pdf), a service-only chamber. Its drawing gives 8 bar normal pressure, 10 bar temporarily and at least 57 mm stroke. Force-curve reference labels are 6,080 N at 6 bar and 8,150 N at 8 bar; these are not constant forces or maximum ratings. The ±5% tolerance applies only over 10–40 mm stroke, and no 10 bar force curve was retrieved.

Using the stated 136 mm chamber inner diameter gives a deliberately conservative **static pressure-area screening value of14.527 kN at10 bar**, ignoring return-spring force and friction. This is an analytical assumption, not a manufacturer output rating; the effective-area bound needs confirmation. Impact, inertia, stops and installation loads remain additional. The example supplies no spring-parking function and is not selected for this vehicle.

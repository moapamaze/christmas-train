"""Coach ERV sizing - Pulsipher Farms Christmas Train (preliminary, not for construction until PE stamped).
Basis: systems-p1 coach-climate plan (110 F / 75 F, dT 19.44 K, dw 0.006 kg/kg humid stress, 15 % allowance, COP 2.5),
plan hot-humid demand 39.7 kW electric, genset 35 kW continuous, target 34.4 kW running (pe_calcs G1-c).
ASHRAE 62.1-2022 Table 6-1 'Transportation waiting' used as analog (no railcar category): Rp 3.8 L/s.person, Ra 0.3 L/s.m2."""
import json
rho, cp, hfg = 1.2, 1.006, 2501.0
dT, dw, allow, COP = 19.44, 0.006, 1.15, 2.5
Rp, Ra, Az = 3.8, 0.3, 20.5          # cabin 221 ft2 = 20.5 m2 (CL2)
coaches = {"regular": {"n": 3, "Pz": 33, "basis_Ls": 247.5}, "accessible": {"n": 1, "Pz": 14, "basis_Ls": 105.0}}
w_per_Ls = (rho*cp*dT + rho*hfg*dw)            # W thermal per L/s OA
we_per_Ls = w_per_Ls*allow/COP                 # W electric per L/s
out = {"per_coach": {}, "inputs": dict(Rp=Rp, Ra=Ra, Az_m2=Az, dT=dT, dw=dw, allow=allow, COP=COP)}
tot62 = tot_b = 0
for k, c in coaches.items():
    Vbz = Rp*c["Pz"] + Ra*Az
    out["per_coach"][k] = dict(n=c["n"], Pz=c["Pz"], Vbz_Ls=round(Vbz, 1), Voz_cool_Ls=round(Vbz/1.0, 1), Voz_cool_cfm=round(Vbz/1.0*2.119, 0),
                               Voz_heat_ceiling_Ls=round(Vbz/0.8, 1), basis_Ls=c["basis_Ls"])
    tot62 += c["n"]*Vbz; tot_b += c["n"]*c["basis_Ls"]
D0, target = 39.7, 34.4
def case(Q):
    Pe = Q*we_per_Ls/1000                       # OA electric share at Q
    D_noerv = D0 - (tot_b - Q)*we_per_Ls/1000   # plan demand scaled to this OA
    eps = max(0.0, (D_noerv - target)/Pe)
    return dict(OA_Ls=round(Q, 1), OA_thermal_kW=round(Q*w_per_Ls/1000, 2), OA_electric_kW=round(Pe, 2),
                demand_no_erv_kW=round(D_noerv, 2), eps_required=round(eps, 3))
out["W_th_per_Ls"] = round(w_per_Ls, 2); out["W_el_per_Ls"] = round(we_per_Ls, 2)
out["basis_848"] = case(tot_b); out["ashrae621"] = case(tot62)
# COP 3 sensitivity on the basis flow (pe_calcs old method)
out["basis_848_COP3"] = dict(eps_required=round((D0-target)/(tot_b*w_per_Ls*allow/3.0/1000), 3))
# selected unit: RenewAire HE05IN, eps_total ASSUMED 0.55 cooling (AWAIT RenewAire selection printout); fan <=340 W vs 250 W allowance
eps_sel, fan_sel, fan_allow = 0.55, 0.340, 0.250
fan_kw = (3*fan_sel + 0.25) - 4*fan_allow       # accessible coach unit runs ~126 cfm -> ~250 W (submittal curve)
for key in ("basis_848", "ashrae621"):
    c = out[key]; c["eps_sel"] = eps_sel
    c["erv_saving_kW"] = round(eps_sel*c["OA_electric_kW"], 2)
    c["fan_delta_kW"] = round(fan_kw, 2)
    c["demand_with_erv_kW"] = round(c["demand_no_erv_kW"] - c["erv_saving_kW"] + fan_kw, 2)
    c["eps_required_incl_fan"] = round(max(0, (c["demand_no_erv_kW"] + fan_kw - target)/c["OA_electric_kW"]), 3)
out["selected"] = dict(model="RenewAire HE05IN", qty="1 per coach (4)", flow_regular_cfm=279, flow_accessible_cfm=126,
    range_cfm="120-375", volts="120 V 1-ph 60 Hz", power_W="<=343 (submittal curve, full ESP); 2 x 220 W EC",
    dims_mm="880 x 956 x 307 H (34-5/8 x 37-5/8 x 12.1 in)", mass_kg=43, eps_total="ASSUMED 0.55 cooling - AWAIT RenewAire selection printout (AHRI 1060 core L62-G5)",
    location="roof clerestory pod, top <= 3,450 ARL (coach peak 3,089; loco roof 3,700; K-401 overhead 4,300)",
    links=["https://renewaire.com/product/he05in/", "https://renewaire.com/wp-content/uploads/2025/05/Submittal-HE05IN-Feb2025.pdf"])
json.dump(out, open("/workspace/train/calcs/erv/erv_sizing.json", "w"), indent=1)
print(json.dumps(out, indent=1))

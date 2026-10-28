"""Check of the owner's plan direct drive (DT4 R1 / DT5 R1: 4 x Poclain MS05 376 cc, 1:1, axle-end) against the R2/T2 basis on Ø1,450 drivers."""
import math, json
g=9.81
m_train = 77.8-8.16+json.load(open("/workspace/train/calcs/tender_mass_T2.json"))["total_kg"]/1000  # t, loco+4 loaded coaches+stairs+T2 tender
W = m_train*g  # kN
need2 = W*0.0408; adh_dry=35.8; adh_wet=21.5
def F(n,cc,p,eta,D,ratio=1.0): return n*p/10*cc/(2*math.pi)*eta*ratio/(D/2000)/1000
r={}
r["train_t"]=round(m_train,3); r["need_2pct_start_kN"]=round(need2,2)
# his own numbers reproduced
r["plan_DT4_4x376_300bar_eta090_D1000"]=round(F(4,376,300,0.90,1000),2)   # plan says 12.93
r["plan_DT4_4x468_300bar_eta090_D1000"]=round(F(4,468,300,0.90,1000),2)   # plan says 16.09
r["plan_LT12_3x376_300bar_eta090_D1450"]=round(F(3,376,300,0.90,1450),2)  # plan says 'about 8.0'
r["plan_1pct_grade_65t1_kN"]=round(65.1*9.80665*0.01,2)                   # plan says 6.38
r["plan_LT12_adverse_launch_65t1"]=round(1.15*(65100*9.80665*0.025+65100*0.05)/1000,2)  # 22.10
r["plan_LT12_severe_launch_65t1"]=round(1.15*(65100*9.80665*0.018+65100*0.05)/1000,2)   # 16.96
# his method at our mass, on 2%
r["plan_method_severe_launch_plus2pct_ourmass"]=round(1.15*(m_train*1000*g*(0.018+0.02)+m_train*1000*0.05)/1000,2)
r["plan_method_steady_2pct_ourmass"]=round(1.15*(m_train*1000*g*(0.007+0.02))/1000,2)
# his drive on the Ø1,450 drivers
cases={}
for lab,(n,cc,p) in {"4x376 @300 (plan)":(4,376,300),"4x376 @350":(4,376,350),"4x376 @380 (H1P053 working)":(4,376,380),"4x376 @450 (MS05 max)":(4,376,450),
                     "4x468 @450":(4,468,450),"4x560 @450 (largest MS05)":(4,560,450),"4x750 MSE05 @350 (adopted L1)":(4,750,350),"4x750 MSE05 @380":(4,750,380),"4x750 MSE05 @400 (max)":(4,750,400),
                     "4x1146 MSE08 @350":(4,1146,350),"4x1146 MSE08 @380":(4,1146,380),"4x1248 MSE08 @350":(4,1248,350),"4x1248 MSE08 @380":(4,1248,380),"4x1259 MS11 @380":(4,1259,380)}.items():
    cases[lab]={f"eta{e}":round(F(n,cc,p,e,1450),2) for e in (0.95,0.90,0.80)}
r["on_D1450"]=cases
# planetary hub on MSE05 750
r["ratio_needed_MSE05_750_350bar"]={f"eta{e}":round(need2/F(4,750,350,e,1450),3) for e in (0.95,0.90,0.80)}
r["ratio_needed_MS05_376_380bar"]={f"eta{e}":round(need2/F(4,376,380,e,1450),3) for e in (0.95,0.90,0.80)}
r["cc_needed_1to1_380bar"]={f"eta{e}":round(need2/F(4,1,380,e,1450)) for e in (0.95,0.90,0.80)}
# speed/flow
v=7.5*0.44704; n_w=v/(math.pi*1.45)*60
r["wheel_rpm_7p5mph"]=round(n_w,1)
for cc in (376,573,624,1146,1248): r[f"flow_7p5mph_4x{cc}_Lmin"]=round(4*cc/1000*n_w/0.95,1)
r["H1P053_flow_2600_Lmin"]=round(53.8*2600/1000*0.95,1)
# speed at which 35 kW pump allowance holds full 2% start pull (hyd eff 0.855*0.855 ~0.73)
r["speed_at_31kN_35kW_mph"]=round(35*0.855*0.855/need2/0.44704,2)
json.dump(r,open("/workspace/train/calcs/F25/plan_direct_drive_check.json","w"),indent=1)
print(json.dumps(r,indent=1))

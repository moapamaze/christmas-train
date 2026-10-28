import json, math
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Wedge
d = json.load(open("structural_body_study.json"))
R, M, F, EN, FO = d["res"], d["mass"], d["fab"], d["eng"], d["form"]
order = ["C2","D","C","B","A"]
label = {"C":"1 R2 as drawn (HSS frame + 3 mm welded cosmetic body)",
         "C2":"2 R2 HSS frame + 4.8 mm bolted cosmetic shell",
         "D":"3 Heavy plate frame + 4.8 mm bolted cosmetic shell",
         "B":"4 Hybrid: light sill + 10 mm structural rolled shell",
         "A":"5 Full thin stressed skin (5 mm)"}
short = {"C":"1 R2 as drawn","C2":"2 R2 frame + better shell","D":"3 Heavy plate frame + better shell","B":"4 Hybrid thick structural shell","A":"5 Full stressed skin"}
look = {"C":(2,"3 mm skin welded to HSS hoops: oil-canning and weld show-through (dimples) likely; flat 3 mm cab panels drum"),
        "C2":(4.5,"4.8 mm skin, no welds on the visible face (bolted/riv-nut to CNC rings); true round, lap bands can read as boiler bands"),
        "D":(5,"Same clean shell as 2, plus real-looking plate frames under the running boards"),
        "B":(4,"10 mm shell very true, no oil-canning; seams need grinding; structural cab gets welded doublers that show"),
        "A":(2,"5 mm skin stitch-welded to 13 rings + 8 stringers: 'hungry-horse' ripple, hatch doublers, straightening marks")}
appr = {"C":"Easy: hand calcs done (R2 C4/C5/C8)","C2":"Easy: R2 calcs + ring/fastener check","D":"Easy: plain beam + plate, hand calcs; small drag-box FEA optional",
        "B":"Medium: shared load path sill/shell needs FEA and shear-connector design","A":"Hard: FEA incl. buckling, hatch/cut-out and fatigue hot-spot; likely proof-load test"}
simp = {"C":4,"C2":5,"D":5,"B":3,"A":1}
allin = {k: F[k]["total"]+EN[k]["mid"] for k in order}
rank = sorted(order, key=lambda k: allin[k])
# ---------- sketch ----------
fig, axs = plt.subplots(1,5, figsize=(20,5.4))
def base(ax, t):
    ax.set_xlim(-1500,1500); ax.set_ylim(900,3500); ax.set_aspect("equal"); ax.axis("off"); ax.set_title(t, fontsize=9)
    ax.plot([-1500,1500],[0+1000,1000],lw=0)
def shell(ax, t, col, ls="-"):
    ax.add_patch(Circle((0,2560),820,fill=False,lw=max(0.8,t/2.5),ec=col,ls=ls))
def deck(ax, t=6): ax.add_patch(Rectangle((-1250,1650),2500,t*4,fc="#555"))
for ax,k in zip(axs,order):
    base(ax, short[k])
    if k in ("C","C2"):
        for y in (-850,850): ax.add_patch(Rectangle((y-76,1345),152,305,fill=False,lw=2,ec="#1f4e79"))
        deck(ax)
        if k=="C": shell(ax,3,"#c00",ls="--"); ax.text(0,2560,"3 mm cosmetic\nwelded to HSS hoops",ha="center",fontsize=7)
        else: shell(ax,4.8,"#2a7"); ax.add_patch(Circle((0,2560),790,fill=False,lw=4,ec="#999")); ax.text(0,2560,"4.8 mm shell\nbolted on PL10\nflat CNC rings",ha="center",fontsize=7)
        ax.text(0,1200,"2 x HSS12x6x3/8 rails\n(structure)",ha="center",fontsize=7,color="#1f4e79")
    if k=="D":
        for y in (-850,850): ax.add_patch(Rectangle((y-10,1150),20,500,fc="#1f4e79"))
        deck(ax); shell(ax,4.8,"#2a7"); ax.add_patch(Circle((0,2560),790,fill=False,lw=4,ec="#999"))
        ax.text(0,2560,"4.8 mm shell\nbolted on rings",ha="center",fontsize=7)
        ax.text(0,1000,"2 x PL20x500 A572-50\nplate frames (structure)",ha="center",fontsize=7,color="#1f4e79")
    if k=="B":
        ax.add_patch(Rectangle((-125,1345),250,305,fill=False,lw=2.5,ec="#1f4e79")); deck(ax)
        shell(ax,10,"#1f4e79"); ax.add_patch(Rectangle((-500,1650),1000,120,fc="#88a"))
        ax.text(0,2560,"10 mm STRUCTURAL\nrolled shell",ha="center",fontsize=7,color="#1f4e79")
        ax.text(0,1150,"centre sill 250x305\n+ saddles to shell",ha="center",fontsize=7,color="#1f4e79")
    if k=="A":
        deck(ax); shell(ax,5,"#1f4e79")
        for y in (-1250,1250): ax.add_patch(Rectangle((y-2,1100),4*3,550,fc="#1f4e79"))
        for a in range(0,360,45):
            x=780*math.cos(math.radians(a)); z=2560+780*math.sin(math.radians(a)); ax.add_patch(Rectangle((x-20,z-20),40,40,fc="#c60"))
        ax.text(0,2560,"5 mm skin + 13 rings\n+ 8 stringers\n+ 4 mm skirts\n(all structure)",ha="center",fontsize=7,color="#1f4e79")
    ax.text(0,3420,f"all-in ~{allin[k]} h · look {look[k][0]}/5",ha="center",fontsize=8,weight="bold")
fig.suptitle("PF-CT R2 loco — body/frame options, section at mid-hood (Z above rail, mm). Blue = load-carrying, grey/green = cosmetic\nPulsipher Farms Christmas Train — preliminary, not for construction until PE stamped", fontsize=9)
plt.tight_layout(); plt.savefig("structural_body_section.png", dpi=130)
# ---------- costs (owner page only) ----------
shop=(80,110); eng_r=150; pe_r=200; cty=110; plate=(0.67,1.03); hss=(1.00,1.20)
cost={}
for k in order:
    e=EN[k]; mid=lambda v:(v[0]+v[1])/2
    lab=[F[k]["total"]*shop[0],F[k]["total"]*shop[1]]
    en=(mid(e["design"])+mid(e["fea"])+mid(e["test"]))*eng_r + mid(e["pe"])*pe_r + mid(e["qa"])*cty
    hss_kg = 2229 if k in ("C","C2") else 0
    plate_kg = M[k]["total_steel"]-hss_kg
    mat=[plate_kg*2.2046*plate[0]+hss_kg*2.2046*hss[0], plate_kg*2.2046*plate[1]+hss_kg*2.2046*hss[1]]
    out_roll=(0,0)   # CWF rolls in-house (owner 27 Oct): no outside roll shop
    cost[k]=dict(lab=lab,eng=en,mat=mat,roll=out_roll,tot=[lab[0]+en+mat[0]+out_roll[0],lab[1]+en+mat[1]+out_roll[1]])
json.dump(dict(cost=cost,allin=allin,rank=rank),open("structural_body_costs_OWNER_ONLY.json","w"),indent=1)
for k in order: print(k, allin[k], {a:[round(x) for x in (v if isinstance(v,list) or isinstance(v,tuple) else [v])] for a,v in cost[k].items()})
print(rank)

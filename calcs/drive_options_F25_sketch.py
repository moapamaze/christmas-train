"""Simple layout sketches for F25 options (not to final detail). Geometry from model.py rev L1 + catalog envelopes."""
import math, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon
R = 725; ZA = 725; HB = 775
TB = "Pulsipher Farms Christmas Train — preliminary, not for construction until PE stamped"
def base_side(ax, title):
    ax.set_title(title, fontsize=9)
    ax.axhline(0, color="k", lw=1.5); ax.text(-1580, 15, "rail top Z0", fontsize=6)
    ax.axhline(1605, color="0.5", lw=1, ls="--"); ax.text(-1580, 1620, "running board Z1,605", fontsize=6)
    for x in (-HB, HB):
        ax.add_patch(Circle((x, ZA), R, fill=False, lw=1.2, ec="0.35"))
        ax.add_patch(Circle((x, ZA), 65, fc="0.6", ec="k"))
    ax.add_patch(Rectangle((-1100, 1000), 2200, 110, fc="none", ec="b", ls="--", lw=0.8))
    ax.add_patch(Rectangle((-150, 850), 300, 200, fc="#cde", ec="b", lw=0.8)); ax.text(-140, 1060, "transom", fontsize=6, color="b")
    ax.text(-1080, 1120, "inside sideframe (behind wheel)", fontsize=6, color="b")
    ax.set_xlim(-1650, 1650); ax.set_ylim(-80, 1720); ax.set_aspect("equal"); ax.tick_params(labelsize=6)
def base_end(ax, title):
    ax.set_title(title, fontsize=9)
    ax.axhline(0, color="k", lw=1.5)
    ax.add_patch(Rectangle((427, ZA - R), 120, 2 * R, fc="0.85", ec="0.35")); ax.text(430, 1480, "wheel Ø1,450\nY427–547", fontsize=6)
    ax.add_patch(Rectangle((0, ZA - 65), 610, 130, fc="0.6", ec="k", alpha=0.6))
    ax.add_patch(Rectangle((270, ZA - 105), 120, 210, fc="#cde", ec="b")); ax.text(250, ZA - 160, "axlebox\nY270–390", fontsize=6, color="b")
    ax.add_patch(Rectangle((330, 1000), 30, 110, fc="#cde", ec="b"))
    ax.add_patch(Rectangle((555, ZA - 335), 30, 70, fc="#c96", ec="k")); ax.text(590, ZA - 380, "side rod Y555–585\n(sweeps r300)", fontsize=6)
    ax.add_patch(Rectangle((0, 850), 330, 200, fc="none", ec="b", ls="--")); ax.text(10, 1060, "transom (beyond)", fontsize=6, color="b")
    ax.axvline(1300, color="r", lw=0.8, ls=":"); ax.text(1305, 300, "body half-width Y1,300", fontsize=6, color="r", rotation=90)
    ax.axvline(1250, color="0.5", lw=0.8, ls="--"); ax.text(1200, 1640, "board Y1,250", fontsize=6)
    ax.axvline(0, color="k", lw=0.5, ls="-."); ax.text(5, -60, "CL", fontsize=6)
    ax.set_xlim(-60, 1500); ax.set_ylim(-80, 1720); ax.set_aspect("equal"); ax.tick_params(labelsize=6)
def figure(fn, sup, side, end, note):
    fig, (a, b) = plt.subplots(1, 2, figsize=(13, 6.2), gridspec_kw=dict(width_ratios=[3300, 1560]))
    base_side(a, "Side elevation, one powered truck (mm)"); base_end(b, "Half end section at axle (mm)")
    side(a); end(b)
    fig.suptitle(sup, fontsize=11, weight="bold")
    fig.text(0.01, 0.05, note, fontsize=7, va="bottom", wrap=True)
    fig.text(0.01, 0.01, TB, fontsize=7, style="italic")
    fig.tight_layout(rect=(0, 0.1, 1, 0.95)); fig.savefig(fn, dpi=130); plt.close(fig)
# ---- A: axle-hung oil-bath chain case, 16T:28T RS140-2, case tilted 15 deg down toward truck centre
def A_side(a):
    for s in (1, -1):
        xa = s * HB; c = 400; ang = math.radians(15)
        xm = xa - s * c * math.cos(ang); zm = ZA - c * math.sin(ang)
        a.add_patch(Circle((xa, ZA), 199, fill=False, ec="g", lw=1.2))
        a.add_patch(Circle((xm, zm), 150, fc="#f9c", ec="m")); a.text(xm - 100, zm - 15, "MSE05\nØ300", fontsize=6)
        a.add_patch(Circle((xm, zm), 114, fill=False, ec="g", ls=":"))
        # case outline
        a.plot([xa, xm], [ZA + 240, zm + 165], color="g", lw=0.8); a.plot([xa, xm], [ZA - 240, zm - 165], color="g", lw=0.8)
        # nose link to transom
        a.plot([xm - s * 60, s * 150], [zm + 120, 900], color="m", lw=2)
    a.annotate("motor top Z771 vs transom underside Z850: 79 clear", (-389, 771), (-560, 1290), fontsize=6, arrowprops=dict(arrowstyle="->", lw=0.6))
    a.annotate("28T RS140 axle sprocket Ø397 PD\n(case bottom ≈ Z485, 485 above rail)", (775, 526), (200, 180), fontsize=6, arrowprops=dict(arrowstyle="->", lw=0.6))
    a.text(-1600, 1450, "Case hung on axle (2 bearings), nose link to transom.\nNothing outboard of the wheels.", fontsize=7, color="g")
def A_end(b):
    b.add_patch(Rectangle((-0, ZA - 240), 150, 480, fc="#dfd", ec="g")); b.text(5, ZA + 250, "chain case\nY0–150", fontsize=6, color="g")
    b.add_patch(Rectangle((-0, 621 - 150), 0, 0))
    b.add_patch(Rectangle((-220, 471), 370, 300, fc="#f9c", ec="m", alpha=0.5))
    b.text(-50, 420, "motor body (beyond, 386 toward truck centre)\nY −220…150, 50 to opposite axlebox", fontsize=6, color="m")
    b.add_patch(Rectangle((180, ZA - 162), 22, 324, fc="0.4", ec="k")); b.text(150, ZA + 175, "Ø325 rotor", fontsize=6)
    b.text(620, ZA + 40, "wheel face, crank pin\n& rods only — clean", fontsize=7, color="g")
    b.set_xlim(-260, 1500)
figure("/workspace/train/calcs/F25/F25_A_sketch.png", "Option A — 1.75:1 inboard chain per axle, 4 × MSE05 (axle-hung case, nose-suspended)",
       A_side, A_end, "RS140-2 duplex 16T:28T (Ø228/Ø397 PD), c≈400, oil-bath case on axle, rubber-bushed nose link to transom; chain pull 40.0 kN at 400 bar "
       "(Tsubaki RS140-2 max allowable 68.4 kN). Axle sprocket on keyless locking assembly or key 32×18×150 (90 MPa). Motor shaft version, radial load AWAIT Poclain. "
       "Removes DT5 outboard cartridge, KTR coupling (C7c) and hub key (C7k).")
# ---- B: outboard 1:1 MSE08
def B_side(a):
    for s in (1, -1):
        a.add_patch(Circle((s * HB, ZA), 167, fc="#f9c", ec="m", alpha=0.7)); a.text(s * HB - 90, ZA - 10, "MSE08\nØ335", fontsize=6)
    a.add_patch(Rectangle((-1300, 160), 2600, 60, fc="#fc9", ec="r")); a.text(-1280, 230, "outside torque bar + cross-member under rods, between wheels (needed: arm cannot pass wheel/rods)", fontsize=6, color="r")
    for s in (1, -1):
        a.plot([s * HB, s * HB], [ZA - 170, 220], color="r", lw=2)
def B_end(b):
    b.add_patch(Rectangle((590, ZA - 120), 134, 240, fc="#cde", ec="b")); b.text(595, ZA + 130, "cartridge", fontsize=6)
    b.add_patch(Rectangle((744, ZA - 110), 186, 220, fc="#ffd", ec="k")); b.text(744, ZA - 160, "coupling ≥12 kN·m", fontsize=6)
    b.add_patch(Rectangle((950, ZA - 175), 20, 350, fc="0.6", ec="k"))
    b.add_patch(Rectangle((970, ZA - 167), 418, 335, fc="#f9c", ec="m")); b.text(980, ZA + 180, "MSE08 shaft motor\nL418, 85 kg → Y1,388", fontsize=6, color="m")
    b.add_patch(Rectangle((360, 160), 1000, 60, fc="#fc9", ec="r")); b.text(380, 120, "torque bar route under rods", fontsize=6, color="r")
    b.annotate("88 past body line", (1388, 900), (1320, 1300), fontsize=6, color="r", arrowprops=dict(arrowstyle="->", lw=0.6))
figure("/workspace/train/calcs/F25/F25_B_sketch.png", "Option B — 1:1 direct, 4 × MSE08 1,146–1,248 cc on the axle ends (outboard)",
       B_side, B_end, "Shaft motor Ø335 × 418 (2-speed, brake) 85 kg per axle end, DT5-style cartridge + coupling: reaches Y≈1,390 (body 1,300, board 1,250). "
       "Torque reaction cannot cross the rotating wheel and side rods to the inside frame, so an outside torque bar under the rods is needed. Coupling must carry ≥ 7,945 × 1.5 ≈ 11.9 kN·m (KTR AWAIT).")
# ---- C: plan LT25 jackshaft
def C_side(a):
    a.add_patch(Circle((0, 560), 128, fill=False, ec="g")); a.add_patch(Circle((0, 560), 219, fill=False, ec="g", ls=":"))
    a.text(-120, 300, "jackshaft Z560\n21T ×2 + 36T", fontsize=6, color="g")
    for s in (1, -1):
        a.add_patch(Circle((s * HB, ZA), 297, fill=False, ec="g", lw=1.2))
        a.plot([0, s * HB], [560 + 128, ZA + 297], color="g", lw=0.8); a.plot([0, s * HB], [560 - 128, ZA - 297], color="g", lw=0.8)
    a.add_patch(Circle((-420, 760), 150, fc="#f9c", ec="m", alpha=0.6)); a.text(-500, 740, "MS05 560", fontsize=6)
    a.text(-1600, 1450, "One motor per truck → jackshaft (1.714) → two axle chains 21/49 RS120 (2.333).\nAll inboard; chain tensioners for primary travel.", fontsize=7, color="g")
def C_end(b):
    for y, lab in ((40, "axle chain 1"), (110, "1st stage"), (180, "axle chain 2")):
        b.add_patch(Rectangle((y, 420), 40, 600, fc="#dfd", ec="g"))
    b.text(0, 1030, "3 chain planes + motor\nin Y 0–270 (very tight)", fontsize=6, color="g")
    b.add_patch(Rectangle((-220, 610), 370, 300, fc="#f9c", ec="m", alpha=0.4))
    b.text(620, ZA + 40, "wheel face, crank pin\n& rods only — clean", fontsize=7, color="g")
    b.set_xlim(-260, 1500)
figure("/workspace/train/calcs/F25/F25_C_sketch.png", "Option C — plan LT23–LT25: 2 × MS05 560 cc, 4:1 via jackshaft + chains",
       C_side, C_end, "49T RS120 axle sprocket Ø595 PD; axle chain pull 18.8 kN at 350 bar (RS120 single 30.4 kN allowable). Start 25.9–30.8 kN at 350 bar (short of 31.2). "
       "Flow 208 L/min at 7.5 mph with single-speed 560 cc → 4.0 mph on H1P045, 5.4 on H1P060; 2-speed MS05 (280 cc) would restore ~8 mph (AWAIT Poclain).")
print("ok")

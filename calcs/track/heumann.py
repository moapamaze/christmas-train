import math
from scipy.optimize import brentq
def heumann(wb, R=None, sigma=0.0124, e=0.49, mu=0.3):
    """Quasi-static (Heumann) curving of a rigid 2-axle truck, zero cant deficiency, full creep saturation
    (dry-rail upper bound). wb, R, sigma, e in m. Returns dict(YQ1 lead-outer, YQ2 trail-inner, pole, mode, aoa_mrad)."""
    W = [(0, e), (0, -e), (-wb, e), (-wb, -e)]
    def sums(xp):
        dxs = [x - xp for x, y in W]; ds = [math.hypot(x - xp, y) for x, y in W]
        return sum(dx / d for dx, d in zip(dxs, ds)), sum(ds)
    xp = brentq(lambda xp: (-xp) * sums(xp)[0] - sums(xp)[1], -wb * 3, -1e-6)
    pole = -xp; mode = "free"; Y2 = 0.0
    if R is not None:
        pg = wb / 2 + R * sigma / wb
        if pole > pg:
            pole = pg; mode = "chord"
    sl, sd = sums(-pole)
    if mode == "free":
        Y1 = mu * sd / pole
    else:
        Y1 = (mu * sd + mu * sl * (wb - pole)) / wb; Y2 = Y1 - mu * sl
    aoa = pole / R * 1000 if R else None
    return dict(YQ1=Y1, YQ2=Y2, pole=pole, mode=mode, aoa_mrad=aoa)
def nadal(gam=70, mu=0.3):
    t = math.tan(math.radians(gam)); return (t - mu) / (1 + mu * t)

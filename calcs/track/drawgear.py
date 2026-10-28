"""Independent drawgear slack check (RT1 28 Oct 2026) - 6 lumped masses, piecewise-linear gap springs, viscous damping zeta 0.05.
Cases: (1) start snatch on 2% with the slack bunched, TE ramp 0.5 s; (2) emergency run-in on 2% down from 6 mph with the slack
stretched, loco 1.03 m/s2 vs cars 0.69 m/s2 (PE B1 / Stress Bot), brake applied 0.3 s + 0.25 s/car.  k, slack ASSUMED sweeps."""
import numpy as np, json
g = 9.80665
M = np.array([17667, 8304, 13200, 13200, 13200, 11000], float)
def sim(k_kNmm, s_mm, mode, F=37.9e3, ramp=0.5, decel=(1.03, 0.69), zeta=0.05, T=6.0, dt=1e-4, grade=0.02, tp=0.25):
    k = k_kNmm * 1e6; s = s_mm / 1000; n = len(M)
    mr = M[:-1] * M[1:] / (M[:-1] + M[1:]); c = 2 * zeta * np.sqrt(k * mr)
    x = np.zeros(n); v = np.zeros(n)
    if mode == "start": x = -np.arange(n) * 0.0 + np.arange(n) * s       # bunched: car i is s closer per joint (compression side)
    else: v[:] = 6 * 0.44704; x = -np.arange(n) * s                        # stretched
    peakT = peakC = 0.0
    for i in range(int(T / dt)):
        t = i * dt
        d = x[:-1] - x[1:]                    # >0 tension (front ahead), measured from nominal
        f = np.where(d > s, k * (d - s), np.where(d < -s, k * (d + s), 0.0))
        engaged = np.abs(d) > s
        f = f + np.where(engaged, c * (v[:-1] - v[1:]), 0.0)
        Fn = np.zeros(n); Fn[:-1] -= f; Fn[1:] += f
        if mode == "start":
            Fn[0] += F * min(t / ramp, 1.0)
            Fn -= M * g * (0.0208 + grade)
            stuck = (v <= 0) & (Fn < 0); a = np.where(stuck, 0, Fn / M); v = np.where(stuck, 0, v)
        else:
            on = t >= 0.3 + np.arange(n) * tp
            dec = np.where(on, np.array([decel[0]] + [decel[1]] * (n - 1)), 0.0)
            a = Fn / M - dec * np.sign(v) * (v > 0) + g * (grade - 0.005)
            if (v <= 0.001).all() and t > 1: break
        v = v + a * dt; x = x + v * dt
        peakT = max(peakT, f.max()); peakC = max(peakC, -f.min())
    return round(peakT / 1e3, 1), round(peakC / 1e3, 1)
out = []
for k in (20, 50, 200):
    for sl in (0.0, 0.5, 1.0, 2.0, 5.0, 10.0):
        st = sim(k, sl, "start"); ru = sim(k, sl, "run"); rm = sim(k, sl, "run", decel=(0.69, 0.69))
        out.append(dict(k=k, slack=sl, start_T=st[0], runin_C=ru[1], runin_C_matched=rm[1]))
        print(out[-1], flush=True)
json.dump(out, open("drawgear.json", "w"), indent=1)

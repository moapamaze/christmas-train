import csv, json
out = {}
for t in "ABCD":
    r = list(csv.DictReader(open(f"/workspace/route_redline/{t}_profile_5m.csv")))
    ch = [float(x['chainage_m']) for x in r]; z = [float(x['design_m']) for x in r]; n = len(r)
    for d in (1, -1):
        best = (0, 0, 0)
        for i in range(n):
            fall = 0; j = i; length = 0
            while length < 2000:
                k = (j + d) % n; dz = z[k] - z[j]
                if dz / 5.0 > -0.005: break
                fall -= dz; length += 5.0; j = k
            if fall > best[0]: best = (fall, length, ch[i])
        out[f"{t}{'+' if d > 0 else '-'}"] = dict(fall_m=round(best[0], 2), length_m=best[1], from_ch=best[2], avg_pct=round(100 * best[0] / max(best[1], 1), 2))
        print(t, d, out[f"{t}{'+' if d > 0 else '-'}"])
json.dump(out, open("descents.json", "w"), indent=1)

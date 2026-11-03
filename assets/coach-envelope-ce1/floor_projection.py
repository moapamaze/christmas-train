"""Reproduce CE1's bounded regular-coach underfloor area screen.

Run from any directory: python cad/coach-envelope-ce1/floor_projection.py
Uses only the Python standard library and existing JSON meshes/bounds. No CAD
rebuild, swept-solid calculation, source-model edit, or fabrication acceptance.
Writes only the adjacent floor-projection.json.
"""
from pathlib import Path
import gzip
import hashlib
import json
import math

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUTPUT = HERE / "floor-projection.json"
RECT = (0.54, 305.46, -51.085, 51.085)  # xmin, xmax, ymin, ymax; inches
SLAB = (29.1220472441, 31.1220472441)
AREA = (RECT[1] - RECT[0]) * (RECT[3] - RECT[2])
POSTS = [25, 57, 89, 121, 153, 185, 217, 249, 281]
PIVOTS = [45, 261]
Z_OVERLAP_EPS = 1e-6
INPUTS = {}


def read(relative):
    path = ROOT / relative
    raw = path.read_bytes()
    INPUTS[relative] = {
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
    }
    return json.loads(gzip.decompress(raw) if relative.endswith(".gz") else raw)


def remember(relative):
    raw = (ROOT / relative).read_bytes()
    INPUTS[relative] = {
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
        "role": "Coordination reference; no code from this file is executed.",
    }


def bounds(part):
    if "bounds_in" in part:
        return part["bounds_in"]
    # Some C5 state overrides carry positions without precomputed bounds.
    return {
        axis: [min(part["positions"][i::3]), max(part["positions"][i::3])]
        for i, axis in enumerate("xyz")
    }


def translated(part, offset, prefix=""):
    old = bounds(part)
    return {
        "id": prefix + part["id"],
        "group": part["group"],
        "bounds_in": {
            axis: [v + offset[i] for v in old[axis]]
            for i, axis in enumerate("xyz")
        },
    }


def clip(rect):
    q = (
        max(rect[0], RECT[0]), min(rect[1], RECT[1]),
        max(rect[2], RECT[2]), min(rect[3], RECT[3]),
    )
    return q if q[0] < q[1] and q[2] < q[3] else None


def projections(parts, margin=0.0):
    """AABB XY projections of parts with positive overlap in the Z slab."""
    result = []
    for part in parts:
        b = bounds(part)
        overlap = min(b["z"][1], SLAB[1]) - max(b["z"][0], SLAB[0])
        if overlap <= Z_OVERLAP_EPS:
            continue
        rectangle = clip((
            b["x"][0] - margin, b["x"][1] + margin,
            b["y"][0] - margin, b["y"][1] + margin,
        ))
        if rectangle:
            result.append(rectangle)
    return result


def union_area(rectangles):
    """Exact rectangle union by X slabs and merged Y intervals; no sampling."""
    rectangles = [r for candidate in rectangles if (r := clip(candidate))]
    xs = sorted({x for r in rectangles for x in r[:2]})
    area = 0.0
    for left, right in zip(xs, xs[1:]):
        end = -math.inf
        length = 0.0
        intervals = sorted(
            (r[2], r[3]) for r in rectangles if r[0] < right and r[1] > left
        )
        for low, high in intervals:
            length += max(0.0, high - max(low, end))
            end = max(end, high)
        area += (right - left) * length
    return area


def area_result(rectangles):
    clipped = [r for candidate in rectangles if (r := clip(candidate))]
    obstructed = union_area(clipped)
    free = AREA - obstructed
    return {
        "clipped_rectangle_count": len(clipped),
        "blocked_area_in2": obstructed,
        "clear_area_in2": free,
        "clear_area_ft2": free / 144,
        "clear_area_m2": free * 0.00064516,
        "clear_fraction": free / AREA,
        "clear_percent": 100 * free / AREA,
    }


def build():
    c1 = read("dist/assets/coach-body-c1/model.json.gz")["parts"]
    ci2 = read("dist/assets/coach-installation-ci2/replacement-model.json.gz")
    ci3 = read("dist/assets/coach-installation-ci3/frame-update.json.gz")
    bench = read("dist/assets/coach-seats-c21/model.json.gz")["parts"]
    instances = read("dist/assets/coach-seats-c21/coach-assembly.json")["instances"]
    truck = read("dist/assets/coach-truck-c5/model-full.json.gz")["parts"]
    plain = read("dist/assets/coach-truck-c5/model-interface-plain.json.gz")
    for path in [
        "dist/coach-complete.js", "dist/coach-frame-ci2.js",
        "dist/coach-boarding.js", "cad/coach-installation-ci3/check_revision.py",
    ]:
        remember(path)

    removed2, removed3 = set(ci2["removed_ids"]), set(ci3["removed_ids"])
    frame = [
        p for p in c1 if p["group"] == "underframe"
        and p["id"].removeprefix("J1a-") not in removed2
        and p["id"] not in {"J1a-T45_1", "J1a-T261_1"}
    ]
    frame += [p for p in ci2["parts"] if p["id"] not in removed3]
    frame += ci3["parts"]  # Already global coach inches: no translation.
    joints = [p for p in c1 if p["group"] == "joint"]

    # Apply the plain C5 state. Body-attached bolsters/access bases project into
    # this slab; other retained C5 context is excluded, avoiding duplicate frame.
    overridden = {p["id"] for p in plain["part_overrides"]}
    drop = set(plain["removed_part_ids"]) | overridden
    truck = [p for p in truck if p["id"] not in drop] + plain["part_overrides"]
    attached = [
        p for p in truck if p.get("metadata", {}).get("kinematics") == "body"
        and (not p["id"].startswith("CTX-") or p["id"] == "CTX-BODY-BOLSTER")
    ]
    for pivot in PIVOTS:
        frame += [translated(p, [pivot, 0, 0], f"P{pivot}-") for p in attached]

    feet, all_benches, opening_keepouts = [], [], []
    for instance in instances:
        offset = instance["translation_in"]
        for p in bench:
            if p["group"] in {"context", "floor"}:
                continue
            q = translated(p, offset, instance["id"] + "-")
            all_benches.append(q)
            if p["group"] in {"hardpoint", "hardware"}:
                feet.append(q)
            if p["group"] == "hardpoint" and p["id"].endswith("-CAP"):
                b = q["bounds_in"]
                opening_keepouts.append((
                    b["x"][0] - 0.1875, b["x"][1] + 0.1875,
                    b["y"][0] - 0.1875, b["y"][1] + 0.1875,
                ))

    boxes = []
    for post in POSTS:
        for sign in [-1, 1]:
            boxes.append({
                "id": f"J01-{post}-{'L' if sign < 0 else 'R'}",
                "bounds_in": {
                    "x": [post - 3.54, post + 3.54],
                    "y": [48.585, 51.085] if sign > 0 else [-51.085, -48.585],
                    "z": [32, 42.54],
                },
            })
    # Box footprints are deliberately omitted from insulation even though the
    # visible boxes start at Z32, above this insulation slab.
    box_keepouts = [tuple(p["bounds_in"]["x"] + p["bounds_in"]["y"]) for p in boxes]
    keepouts = box_keepouts + opening_keepouts
    physical = frame + joints + feet
    baseline = projections(physical) + keepouts
    margin_quarter = projections(physical, 0.25) + keepouts
    results = {
        "frame_and_plain_bolsters_access_bases": area_result(projections(frame)),
        "plus_J01_steel": area_result(projections(frame + joints)),
        "plus_all_regular_C21_hardpoints": area_result(projections(physical)),
        "plus_joint_boxes_and_floor_opening_keepouts": area_result(baseline),
    }
    for margin in [0.125, 0.25, 0.5]:
        results[f"part_bounds_margin_{margin:g}_in"] = area_result(
            projections(physical, margin) + keepouts
        )

    # Exact selected body-check intervals in CI3 check_revision.py. These are
    # NOT moving-truck swept envelopes. Broad omission is a sensitivity case.
    study_intervals = [[x - 1393 / 25.4, x + 1457 / 25.4] for x in PIVOTS]
    exclusion_results = {}
    for half_width in [36, 51.085]:
        omissions = [(low, high, -half_width, half_width) for low, high in study_intervals]
        exclusion_results[f"half_width_{half_width:g}_in"] = {
            "no_extra_margin": area_result(baseline + omissions),
            "quarter_in_part_margin": area_result(margin_quarter + omissions),
        }

    intersections = []
    closest = (math.inf, None)
    for box in boxes:
        b = box["bounds_in"]
        for part in all_benches:
            p = part["bounds_in"]
            gap = [max(0, b[a][0] - p[a][1], p[a][0] - b[a][1]) for a in "xyz"]
            distance = math.sqrt(sum(g * g for g in gap))
            if distance < closest[0]:
                closest = (distance, {
                    "box": box["id"], "bench_part": part["id"],
                    "axis_gaps_xyz_in": gap,
                })
            if not any(gap):
                intersections.append([box["id"], part["id"]])

    return {
        "revision": "CE1-floor-projection-R0",
        "status": "STATIC ENVELOPE AND AREA SCREEN; NOT FIT, MOTION OR FABRICATION ACCEPTANCE",
        "reproduce": "python cad/coach-envelope-ce1/floor_projection.py",
        "inputs": INPUTS,
        "geometry": {
            "finished_interior_rectangle_xy_in": list(RECT),
            "candidate_insulation_slab_z_in": list(SLAB),
            "total_area_in2": AREA, "total_area_ft2": AREA / 144,
            "total_area_m2": AREA * 0.00064516,
            "intersection_z_epsilon_in": Z_OVERLAP_EPS,
            "bench_instances": len(instances),
            "hardpoint_opening_keepouts": len(opening_keepouts),
            "J01_box_keepouts": len(box_keepouts),
            "floor_opening_nominal_xy_in": [3.875, 6.375],
            "J01_box_half_length_in": 3.54,
            "J01_box_inner_abs_y_in": 48.585,
            "J01_box_top_z_in": 42.54,
        },
        "method": [
            "Project full XY axis-aligned bounds of every selected part intersecting the candidate Z interval.",
            "Clip to finished interior rectangle and compute exact rectangle union by X slabs and merged Y intervals; never sum overlapping areas.",
            "Apply CI2/CI3 common-frame replacements in the sequence used by coach-complete.js. CI2/CI3 meshes are already global coach inches.",
            "Replace original central T45/T261 with plain C5 body bolsters and body-attached C5 hardware/access bases translated to X45/261. Other C5 context and moving parts are excluded.",
            "Use C21 actual instance translations including Y=-64 on the left; feet remain in existing positions under the proposed narrower upper benches.",
            "Add all64 floor-opening rectangles and18 proposed J01-box footprints as omission zones, even where their physical material lies outside the slab.",
            "Quarter-inch fitting margin expands each intersecting physical part in XY. Keepouts are then unioned without a second margin.",
            "CB2 perimeter/stair modifications lie outside this interior rectangle and do not change this area calculation.",
        ],
        "results": results,
        "bogie_study_exclusion_sensitivity": {
            "source": "cad/coach-installation-ci3/check_revision.py: pivot-1393mm to pivot+1457mm",
            "qualification": "Selected body-study intervals; these are not verified truck swept envelopes.",
            "unclipped_x_intervals_in": study_intervals,
            "results": exclusion_results,
        },
        "provisional_screen_at_60_percent": {
            "insulated_fraction": 0.6, "uninsulated_fraction": 0.4,
            "insulated_area_ft2": AREA / 144 * 0.6,
            "insulated_area_m2": AREA * 0.00064516 * 0.6,
            "two_in_insulation_volume_m3": AREA * 0.00064516 * 0.6 * 0.0508,
            "qualification": "Scenario below61.847% static allowance; not a verified installed fraction. Evaluate limited-floor sensitivity separately.",
        },
        "J01_box_to_existing_bench_screen": {
            "box_aabb_intersections": intersections,
            "minimum_aabb_separation_in": closest[0],
            "closest_pair": closest[1],
            "qualification": "No AABB intersections is a sufficient nominal static separation result for these listed envelopes only; no tooling, occupant, tolerance or service proof.",
        },
        "limits": [
            "AABB projection is conservative for rounded, hollow and irregular parts; this is not an exact solid-sectional area.",
            "Clear fraction means free from selected static projected envelopes, not an accepted insulation/tray footprint. Unmodeled obstructions can reduce it.",
            "No truck sweep, brake hose/chamber sweep, installation/service allowance, fastener access, panel support or tray retention is qualified.",
            "C5 body-fixed reference components are included; later C57 brake/service routing and other equipment are not represented by this calculation.",
            "Accessible coach collars, folding seats, securement and side-door foundations require a separate layout calculation. Do not apply this fraction as accessible-coach acceptance.",
            "No thermal bridge analysis is performed; the uninsulated fraction must not be interpreted as steel area alone.",
            "Areas cover the finished interior rectangle, not exterior platform deck or the full purchased floor-panel takeoff.",
        ],
    }


if __name__ == "__main__":
    result = build()
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    normal = result["results"]["part_bounds_margin_0.25_in"]["clear_percent"]
    broad = result["bogie_study_exclusion_sensitivity"]["results"]["half_width_51.085_in"]["quarter_in_part_margin"]["clear_percent"]
    print(f"Quarter-inch static allowance: {normal:.6f}%")
    print(f"With broad bogie-study omission: {broad:.6f}%")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")

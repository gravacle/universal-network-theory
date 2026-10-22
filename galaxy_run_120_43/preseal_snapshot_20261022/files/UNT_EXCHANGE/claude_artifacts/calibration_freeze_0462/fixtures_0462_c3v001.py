#!/usr/bin/env python3
# fixtures_0462_c3v001.py -- independent fixtures for dispatch 0462 (Claude3 lane, UNT program).
#
# Targets: calibration_region_engine_c3v001.py (Module 1) and prediction_freeze_c3v001.py (Module 2).
# Written from INTERFACE_0462_V001.md alone, before either module was read. Synthetic forward models
# only. Never any NGC3198 velocity. Never a project run. The only real inputs are the frozen DDO154
# calibration observation region (calibration data, allowed) and the NGC3198 TARGET-FREE query manifest.
#
# Usage:
#   OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -I -B fixtures_0462_c3v001.py \
#       <artifact_dir> <scratch_dir> [--results-out <path>]
#
# Writes manifests and scratch files only under <scratch_dir>. Writes nothing into <artifact_dir>
# unless --results-out points there (the results JSON only).

import sys, os, json, math, hashlib, importlib.util, traceback, copy
import numpy as np

REGION_PATH = ("/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/"
               "FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/DDO154_CALIBRATION_OBSERVATION_REGION_V001.json")
REGION_SHA = "13c16a6394fde450c9c1d9b258a8fb5dd01d80ce275a54d9761a285f76145b6d"
MANIFEST_PATH = ("/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/"
                 "FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json")
MANIFEST_SHA = "a293651733ba2e6cff5e313d060521d8481bac39bf6f0af540d0108538535494"
WRONG_SHA = "0" * 64
BOUNDS_SEMANTICS = "COMPUTATIONAL_TRIAL_BOX_NOT_EMPIRICAL_BOUNDS"
ENGINE_FILE = "calibration_region_engine_c3v001.py"
FREEZE_FILE = "prediction_freeze_c3v001.py"
FORBIDDEN = {"vobs", "vobs_km_s", "observed_velocity", "observed_km_s", "error_v_km_s", "velocity_error",
             "chi2", "residual_km_s", "vgas", "vdisk", "vbul", "vgas_km_s", "vdisk_km_s", "vbulge_km_s",
             "target_rows", "targets", "target_velocity", "target_velocities"}

# ----------------------------------------------------------------------------------------------------
# generic helpers
# ----------------------------------------------------------------------------------------------------

def cj(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False)

def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()

def sha256_file(p):
    with open(p, "rb") as f:
        return sha256_bytes(f.read())

def getidx(d, k):
    """Look up a direction index in a dict keyed by int or by str."""
    if not isinstance(d, dict):
        return None
    if k in d:
        return d[k]
    if str(k) in d:
        return d[str(k)]
    return None

def is_num(x):
    return isinstance(x, (int, float, np.integer, np.floating)) and not isinstance(x, (bool, np.bool_))

def is_finite_num(x):
    return is_num(x) and math.isfinite(float(x))

def find_forbidden_keys(obj, path=""):
    hits = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{path}/{k}"
            if isinstance(k, str) and k.lower() in FORBIDDEN:
                hits.append(p)
            hits.extend(find_forbidden_keys(v, p))
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            hits.extend(find_forbidden_keys(v, f"{path}[{i}]"))
    return hits

def close(a, b, tol):
    try:
        return abs(float(a) - float(b)) <= tol
    except Exception:
        return False

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def snapshot_dir(d):
    out = {}
    for root, _dirs, files in os.walk(d):
        for fn in files:
            p = os.path.join(root, fn)
            try:
                st = os.stat(p)
                out[p] = (st.st_size, st.st_mtime_ns)
            except OSError:
                out[p] = None
    return out

class Case:
    def __init__(self, cid, name):
        self.id = cid
        self.name = name
        self.checks = []
        self.numbers = {}
        self.notes = []
        self.error = None

    def check(self, label, cond, detail=None):
        ok = bool(cond)
        entry = {"label": label, "ok": ok}
        if detail is not None:
            entry["detail"] = detail
        self.checks.append(entry)
        return ok

    def note(self, s):
        self.notes.append(str(s))

    def status(self):
        if self.error:
            return "ERROR"
        if not self.checks:
            return "SKIP"
        return "PASS" if all(c["ok"] for c in self.checks) else "FAIL"

    def as_dict(self):
        failed = [c for c in self.checks if not c["ok"]]
        return {"id": self.id, "name": self.name, "status": self.status(),
                "n_checks": len(self.checks), "n_failed": len(failed),
                "failed_checks": failed, "checks": self.checks, "numbers": self.numbers,
                "notes": self.notes, "error": self.error}

# ----------------------------------------------------------------------------------------------------
# synthetic coordinates and analytic toy forward (Module 1 fixtures)
# ----------------------------------------------------------------------------------------------------

def _nat_at_u(lo, hi, transform, u):
    if transform == "log":
        return math.exp(math.log(lo) + u * (math.log(hi) - math.log(lo)))
    return lo + u * (hi - lo)

COORDS = [
    {"name": "amp_scale", "transform": "log", "lower": 10.0, "upper": 100.0, "role": "free",
     "trial_value": _nat_at_u(10.0, 100.0, "log", 0.5)},
    {"name": "tilt", "transform": "linear", "lower": -1.0, "upper": 1.0, "role": "free", "trial_value": 0.0},
    {"name": "distance_Mpc", "transform": "log", "lower": 3.0, "upper": 5.5, "role": "nuisance",
     "trial_value": _nat_at_u(3.0, 5.5, "log", 0.5)},
    {"name": "dead_knob", "transform": "linear", "lower": 0.0, "upper": 1.0, "role": "free", "trial_value": 0.5},
    {"name": "held_constant", "transform": "linear", "lower": 0.0, "upper": 2.0, "role": "fixed", "trial_value": 1.0},
]
VARYING = [c for c in COORDS if c["role"] != "fixed"]
NVAR = len(VARYING)          # 4
NULL_COL = 3                 # 'dead_knob' has an exactly-zero column in the toy map
CENTRE = [0.5, 0.5, 0.5, 0.5]
ALPHAS = [10.0, 12.0, 14.0]
P0 = [1.0] * 12
P1 = [1.0] * 6 + [-1.0] * 6
P2 = [1.0 if r % 2 == 0 else -1.0 for r in range(12)]
PATTERNS = [P0, P1, P2]

def u_from_natural(coord, v):
    if coord["transform"] == "log":
        return (math.log(v) - math.log(coord["lower"])) / (math.log(coord["upper"]) - math.log(coord["lower"]))
    return (v - coord["lower"]) / (coord["upper"] - coord["lower"])

def natural_from_u(coord, u):
    return _nat_at_u(coord["lower"], coord["upper"], coord["transform"], u)

class FixtureForwardError(RuntimeError):
    pass

class ToyForward:
    """speeds_r = obs_r + sigma_r * (sum_j ALPHAS[j]*PATTERNS[j][r]*(u_j - CENTRE_j)) + offset_r; column 3 is exactly zero."""

    def __init__(self, rows, offsets=None, fail_rules=None):
        self.rows = rows
        self.offsets = offsets or {}
        self.fail_rules = fail_rules or {}
        self.calls = 0
        self.fixed_violations = 0
        self.missing_name_calls = 0
        self.raised = 0
        self.nan_returned = 0
        self.dropped = 0

    def u_from_theta(self, theta):
        return [u_from_natural(c, float(theta[c["name"]])) for c in VARYING]

    def speeds_from_u(self, u):
        d = [float(u[j]) - CENTRE[j] for j in range(NVAR)]
        out = {}
        for r, row in enumerate(self.rows):
            lin = 0.0
            for j in range(3):
                lin += ALPHAS[j] * PATTERNS[j][r] * d[j]
            out[row["id"]] = row["obs"] + row["sigma"] * lin + self.offsets.get(row["id"], 0.0)
        return out

    def speeds_from_theta(self, theta):
        return self.speeds_from_u(self.u_from_theta(theta))

    def admitted_speeds(self, sp):
        for row in self.rows:
            v = sp.get(row["id"])
            if v is None or not math.isfinite(v):
                return False
            if not (row["low"] <= v <= row["high"]):
                return False
        return True

    def jacobian_expected(self):
        J = []
        for r, row in enumerate(self.rows):
            J.append([row["sigma"] * ALPHAS[j] * PATTERNS[j][r] for j in range(3)] + [0.0])
        return J

    def __call__(self, theta_natural):
        self.calls += 1
        if not isinstance(theta_natural, dict):
            self.missing_name_calls += 1
            return {"speeds_km_s": {}, "valid": False, "reasons": ["theta_natural is not a dict"]}
        missing = [c["name"] for c in COORDS if c["name"] not in theta_natural]
        if missing:
            self.missing_name_calls += 1
            return {"speeds_km_s": {}, "valid": False, "reasons": ["missing coordinates: " + ",".join(missing)]}
        fx = theta_natural["held_constant"]
        if not (is_num(fx) and abs(float(fx) - 1.0) < 1e-12):
            self.fixed_violations += 1
        u = self.u_from_theta(theta_natural)
        rules = self.fail_rules
        if "raise_if" in rules and rules["raise_if"](u):
            self.raised += 1
            raise FixtureForwardError("fixture forward raised deliberately at u=%s" % ([round(x, 6) for x in u],))
        sp = self.speeds_from_u(u)
        if "nan_if" in rules and rules["nan_if"](u):
            self.nan_returned += 1
            sp[rules["nan_row"]] = float("nan")
        if "drop_if" in rules and rules["drop_if"](u):
            self.dropped += 1
            del sp[rules["drop_row"]]
        return {"speeds_km_s": sp, "valid": True, "reasons": []}

def analytic_line_interval(toy, a, v):
    """Admitted t-interval along a + t v (closed rectangles, box [0,1]^n). Returns (t_lo, t_hi, box_lo, box_hi)."""
    sa = toy.speeds_from_u(a)
    t_lo, t_hi = -math.inf, math.inf
    for r, row in enumerate(toy.rows):
        slope = row["sigma"] * sum(ALPHAS[j] * PATTERNS[j][r] * float(v[j]) for j in range(3))
        if abs(slope) < 1e-15:
            continue
        t1 = (row["low"] - sa[row["id"]]) / slope
        t2 = (row["high"] - sa[row["id"]]) / slope
        lo, hi = (t1, t2) if t1 <= t2 else (t2, t1)
        t_lo, t_hi = max(t_lo, lo), min(t_hi, hi)
    box_lo = box_hi = False
    for j in range(NVAR):
        vj = float(v[j])
        if vj > 1e-15:
            hi_t = (1.0 - a[j]) / vj
            lo_t = (0.0 - a[j]) / vj
        elif vj < -1e-15:
            hi_t = (0.0 - a[j]) / vj
            lo_t = (1.0 - a[j]) / vj
        else:
            continue
        if hi_t < t_hi:
            t_hi, box_hi = hi_t, True
        if lo_t > t_lo:
            t_lo, box_lo = lo_t, True
    return t_lo, t_hi, box_lo, box_hi

def march_resolution(t_star, step, bisection_steps):
    """Resolution of doubling-march + bisection for a boundary at distance t_star >= 0."""
    t_star = abs(float(t_star))
    if t_star < step:
        width = step
    else:
        m = int(math.floor(math.log2(t_star / step)))
        width = step * (2.0 ** m)
    return width / (2.0 ** bisection_steps)

def read_region_rows():
    with open(REGION_PATH, "rb") as f:
        raw = f.read()
    assert sha256_bytes(raw) == REGION_SHA, "region file hash changed; refusing"
    doc = json.loads(raw.decode("utf-8"))
    rows = []
    for r in doc["rows"]:
        rows.append({"id": r["id"], "obs": float(r["observed_speed_km_s"]), "sigma": float(r["quoted_random_sigma_km_s"]),
                     "low": float(r["conditional_random_acceptance_low_km_s"]),
                     "high": float(r["conditional_random_acceptance_high_km_s"]),
                     "radius": float(r["reference_radius_kpc"])})
    return rows, doc

def read_manifest_ids():
    with open(MANIFEST_PATH, "rb") as f:
        raw = f.read()
    assert sha256_bytes(raw) == MANIFEST_SHA, "manifest hash changed; refusing"
    doc = json.loads(raw.decode("utf-8"))
    rows = sorted(doc["rows"], key=lambda r: int(r["data_row_index"]))
    return [r["query_id"] for r in rows], {r["query_id"]: r["Rad_text"] for r in rows}, doc.get("rad_unit")

ENGINE_CFG = dict(budget=400, rel_step=0.02, min_step=1e-6, max_halvings=6, null_tolerance=1e-6,
                  repair_iterations=12, max_repair_step=0.3, march_step=0.04, bisection_steps=8,
                  design_count=40, rng_seed=7)

def run_engine(ctx, toy, u_seed, **overrides):
    cfg = dict(ENGINE_CFG)
    cfg.update(overrides)
    return ctx["engine"].run_calibration_region(
        forward=toy, coordinates=copy.deepcopy(COORDS), observation_region_path=REGION_PATH,
        observation_region_sha256=cfg.pop("sha", REGION_SHA), u_seed=u_seed, **cfg)

# ----------------------------------------------------------------------------------------------------
# Module 1 fixtures
# ----------------------------------------------------------------------------------------------------

def log_entries(run):
    log = run.get("evaluation_log")
    return log if isinstance(log, list) else []

def case_E0(ctx, c):
    """Spec helpers: make_coordinate_spec / to_natural / to_unit / classify_prediction / load_observation_region."""
    eng = ctx["engine"]
    rows = ctx["rows"]
    spec = eng.make_coordinate_spec(coordinates=copy.deepcopy(COORDS))
    c.check("spec ok", spec.get("ok") is True, spec.get("reasons"))
    c.check("varying_names ordered as given", spec.get("varying_names") == [x["name"] for x in VARYING], spec.get("varying_names"))
    c.check("fixed_names", spec.get("fixed_names") == ["held_constant"], spec.get("fixed_names"))
    c.check("nuisance_names", spec.get("nuisance_names") == ["distance_Mpc"], spec.get("nuisance_names"))
    c.check("bounds_semantics constant", spec.get("bounds_semantics") == BOUNDS_SEMANTICS, spec.get("bounds_semantics"))
    bad1 = copy.deepcopy(COORDS); bad1[0]["lower"] = 0.0
    r1 = eng.make_coordinate_spec(coordinates=bad1)
    c.check("log coordinate with lower=0 refused (ok False, no raise)", r1.get("ok") is False, r1.get("reasons"))
    bad2 = copy.deepcopy(COORDS); bad2[1]["lower"] = 1.0; bad2[1]["upper"] = 1.0
    r2 = eng.make_coordinate_spec(coordinates=bad2)
    c.check("linear coordinate with lower==upper refused", r2.get("ok") is False, r2.get("reasons"))
    bad3 = copy.deepcopy(COORDS); bad3[2]["role"] = "wobbly"
    r3 = eng.make_coordinate_spec(coordinates=bad3)
    c.check("unknown role refused", r3.get("ok") is False, r3.get("reasons"))
    if spec.get("ok") is True:
        u = [0.5, 0.5, 0.5, 0.5]
        tn = eng.to_natural(spec=spec, u=u)
        c.check("to_natural ok", tn.get("ok") is True, tn.get("reasons"))
        th = tn.get("theta_natural") or {}
        c.check("theta_natural carries all 5 coordinates", sorted(th.keys()) == sorted(x["name"] for x in COORDS), sorted(th.keys()))
        c.check("fixed coordinate inserted at trial_value", close(th.get("held_constant"), 1.0, 1e-12), th.get("held_constant"))
        c.check("log coordinate at u=0.5 is geometric mean", close(th.get("amp_scale"), math.sqrt(1000.0), 1e-9), th.get("amp_scale"))
        c.check("linear coordinate at u=0.5 is midpoint", close(th.get("tilt"), 0.0, 1e-12), th.get("tilt"))
        c.check("theta_internal is a list", isinstance(tn.get("theta_internal"), list))
        tu = eng.to_unit(spec=spec, theta_natural=th)
        c.check("to_unit ok", tu.get("ok") is True, tu.get("reasons"))
        uu = tu.get("u") or []
        c.check("to_unit round trip within 1e-12", len(uu) == 4 and all(close(uu[j], u[j], 1e-12) for j in range(4)), uu)
        c.numbers["roundtrip_u"] = [float(x) for x in uu] if uu else None
    # classify_prediction on toy predictions
    toy = ToyForward(rows)
    rect = {r["id"]: [r["low"], r["high"]] for r in rows}
    ids = [r["id"] for r in rows]
    sp_centre = toy.speeds_from_u(CENTRE)
    r = eng.classify_prediction(prediction={"speeds_km_s": sp_centre, "valid": True, "reasons": []}, rectangles=rect, row_ids=ids)
    c.check("classify: centre admitted", r.get("ok") is True and r.get("valid") is True and r.get("admitted") is True, {k: r.get(k) for k in ("ok", "valid", "admitted", "reasons")})
    ri = r.get("row_inside") or {}
    c.check("classify: row_inside all True at centre", all(ri.get(i) is True for i in ids), ri)
    sp_out = dict(sp_centre); sp_out[ids[3]] = rows[3]["high"] + 1e-6
    r = eng.classify_prediction(prediction={"speeds_km_s": sp_out, "valid": True, "reasons": []}, rectangles=rect, row_ids=ids)
    c.check("classify: one row above high -> not admitted, valid", r.get("valid") is True and r.get("admitted") is False, {k: r.get(k) for k in ("valid", "admitted")})
    c.check("classify: row_inside flags that row only", (r.get("row_inside") or {}).get(ids[3]) is False and all((r.get("row_inside") or {}).get(i) is True for i in ids if i != ids[3]), r.get("row_inside"))
    sp_edge = dict(sp_centre); sp_edge[ids[5]] = rows[5]["high"]
    r = eng.classify_prediction(prediction={"speeds_km_s": sp_edge, "valid": True, "reasons": []}, rectangles=rect, row_ids=ids)
    c.check("classify: closed interval (value == high admitted)", r.get("admitted") is True, r.get("admitted"))
    sp_nan = dict(sp_centre); sp_nan[ids[7]] = float("nan")
    r = eng.classify_prediction(prediction={"speeds_km_s": sp_nan, "valid": True, "reasons": []}, rectangles=rect, row_ids=ids)
    c.check("classify: NaN -> valid False, not admitted", r.get("valid") is False and r.get("admitted") is not True, {k: r.get(k) for k in ("valid", "admitted", "reasons")})
    sp_miss = dict(sp_centre); del sp_miss[ids[9]]
    r = eng.classify_prediction(prediction={"speeds_km_s": sp_miss, "valid": True, "reasons": []}, rectangles=rect, row_ids=ids)
    c.check("classify: missing id -> valid False, not admitted", r.get("valid") is False and r.get("admitted") is not True, {k: r.get(k) for k in ("valid", "admitted", "reasons")})
    r = eng.classify_prediction(prediction={"speeds_km_s": sp_centre, "valid": False, "reasons": ["root says no"]}, rectangles=rect, row_ids=ids)
    c.check("classify: valid False flag honoured", r.get("valid") is False and r.get("admitted") is not True, {k: r.get(k) for k in ("valid", "admitted")})
    r = eng.classify_prediction(prediction="garbage", rectangles=rect, row_ids=ids)
    c.check("classify: wrong type -> valid False, no raise", r.get("valid") is False and r.get("admitted") is not True, {k: r.get(k) for k in ("ok", "valid", "admitted")})
    # load_observation_region with the correct hash
    reg = eng.load_observation_region(path=REGION_PATH, expected_sha256=REGION_SHA)
    c.check("load_observation_region ok", reg.get("ok") is True, reg.get("reasons"))
    c.check("region sha256 reported", reg.get("sha256") == REGION_SHA, reg.get("sha256"))
    c.check("row_ids in file order (12)", reg.get("row_ids") == ids, reg.get("row_ids"))
    rr = reg.get("rectangles") or {}
    c.check("rectangles bound exactly", all(i in rr and close(rr[i][0], rect[i][0], 0.0) and close(rr[i][1], rect[i][1], 0.0) for i in ids), None)
    c.check("sigmas bound exactly", all(close((reg.get("sigmas") or {}).get(i), rows[k]["sigma"], 0.0) for k, i in enumerate(ids)), reg.get("sigmas"))
    c.check("observed bound exactly", all(close((reg.get("observed") or {}).get(i), rows[k]["obs"], 0.0) for k, i in enumerate(ids)), reg.get("observed"))
    c.check("reference_radius_kpc bound", all(close((reg.get("reference_radius_kpc") or {}).get(i), rows[k]["radius"], 0.0) for k, i in enumerate(ids)), reg.get("reference_radius_kpc"))
    c.check("statistical_choice carried", isinstance(reg.get("statistical_choice"), dict) and close(reg["statistical_choice"].get("marginal_quantile"), 2.865260238532134, 0.0), None)
    c.check("distance_summary and forward_coordinates carried", isinstance(reg.get("distance_summary"), dict) and isinstance(reg.get("forward_coordinates"), dict), None)

def check_points_against_toy(c, toy, run, label):
    """Every engine-labelled admitted point satisfies all 12 rectangles under my own toy; every rejected one violates >= 1."""
    ex = run.get("exploration") or {}
    adm = ex.get("admitted_points") or []
    rej = ex.get("rejected_points") or []
    bad_adm, bad_rej = [], []
    for p in adm:
        sp = toy.speeds_from_theta(p["theta_natural"])
        if not toy.admitted_speeds(sp):
            bad_adm.append(p.get("log_index"))
        sp_u = toy.speeds_from_u(p["u"])
        if not toy.admitted_speeds(sp_u):
            bad_adm.append(("u-recompute", p.get("log_index")))
    for p in rej:
        th = p.get("theta_natural")
        if th is None:
            continue
        try:
            sp = toy.speeds_from_theta(th)
        except Exception:
            continue
        if toy.admitted_speeds(sp) and not toy.fail_rules:
            bad_rej.append(p.get("log_index"))
    c.numbers[label + "_admitted_count"] = len(adm)
    c.numbers[label + "_rejected_count"] = len(rej)
    c.check(label + ": every admitted point satisfies all 12 rectangles (toy recompute)", not bad_adm, bad_adm[:10])
    c.check(label + ": every rejected point violates >= 1 rectangle (toy recompute)", not bad_rej, bad_rej[:10])
    # log consistency: every log entry labelled admitted True must be admitted by the toy
    bad_log = []
    for e in log_entries(run):
        if e.get("admitted") is True:
            try:
                if not toy.admitted_speeds(toy.speeds_from_theta(e["theta_natural"])):
                    bad_log.append(e.get("index"))
            except Exception as exc:
                bad_log.append((e.get("index"), repr(exc)))
    c.check(label + ": every log entry labelled admitted is admitted (toy recompute)", not bad_log, bad_log[:10])

def case_E1(ctx, c):
    rows = ctx["rows"]
    toy = ToyForward(rows)
    run = run_engine(ctx, toy, [None] * NVAR)
    ctx["store"]["E1_run"] = run
    ctx["store"]["E1_toy"] = toy
    c.numbers["evaluations_used"] = run.get("evaluations_used")
    c.numbers["forward_calls_counted_by_toy"] = toy.calls
    c.check("ok True", run.get("ok") is True, run.get("reasons"))
    c.check("status COMPLETE", run.get("status") == "COMPLETE", run.get("status"))
    c.check("ngc3198_access == 'NONE'", run.get("ngc3198_access") == "NONE", run.get("ngc3198_access"))
    c.check("bounds_semantics constant on run", run.get("bounds_semantics") == BOUNDS_SEMANTICS, run.get("bounds_semantics"))
    c.check("evaluations_used == toy call count", run.get("evaluations_used") == toy.calls, (run.get("evaluations_used"), toy.calls))
    c.check("evaluation_log length == evaluations_used", len(log_entries(run)) == run.get("evaluations_used"), len(log_entries(run)))
    c.check("budget echoed", run.get("budget") == ENGINE_CFG["budget"], run.get("budget"))
    c.check("fixed coordinate always passed at trial value", toy.fixed_violations == 0 and toy.missing_name_calls == 0, (toy.fixed_violations, toy.missing_name_calls))
    # Jacobian
    jac = run.get("jacobian") or {}
    c.check("jacobian ok, seed valid and admitted", jac.get("ok") is True and jac.get("seed_valid") is True and jac.get("seed_admitted") is True, {k: jac.get(k) for k in ("ok", "seed_valid", "seed_admitted", "reasons")})
    c.check("no failed columns", (jac.get("failed_columns") or []) == [], jac.get("failed_columns"))
    Jexp = toy.jacobian_expected()
    J = jac.get("jacobian_u")
    jac_err = None
    if isinstance(J, list) and len(J) == 12 and all(isinstance(r, list) and len(r) == NVAR for r in J):
        jac_err = max(abs(float(J[r][j]) - Jexp[r][j]) for r in range(12) for j in range(NVAR))
        null_col_max = max(abs(float(J[r][NULL_COL])) for r in range(12))
    else:
        null_col_max = None
    c.numbers["jacobian_max_abs_error"] = jac_err
    c.numbers["jacobian_null_column_max_abs"] = null_col_max
    c.check("jacobian_u is 12x4 and matches the affine map within 1e-6", jac_err is not None and jac_err < 1e-6, jac_err)
    c.check("null column entries |.| < 1e-8", null_col_max is not None and null_col_max < 1e-8, null_col_max)
    f0 = jac.get("f0") or {}
    c.check("f0 equals observed speeds (seed at rectangle centres) within 1e-9", all(close(f0.get(r["id"]), r["obs"], 1e-9) for r in rows), None)
    # identifiability
    idf = run.get("identifiability") or {}
    c.check("identifiability ok", idf.get("ok") is True, idf.get("reasons"))
    ident = idf.get("identified") or []
    nnull = idf.get("near_null") or []
    c.numbers["identified"] = ident
    c.numbers["near_null"] = nnull
    c.check("identified count == 3", len(ident) == 3, ident)
    c.check("exactly one near-null direction", len(nnull) == 1, nnull)
    sv = idf.get("singular_values") or []
    c.numbers["singular_values"] = [float(s) for s in sv] if sv else None
    exp_sv = sorted([a * math.sqrt(12.0) for a in ALPHAS], reverse=True)
    c.numbers["singular_values_expected_identified"] = exp_sv
    if len(sv) == 4:
        got_ident = sorted([float(sv[i]) for i in ident], reverse=True) if len(ident) == 3 else None
        c.check("identified singular values == alpha*sqrt(12) within 1e-6", got_ident is not None and all(abs(got_ident[k] - exp_sv[k]) < 1e-6 for k in range(3)), got_ident)
        c.check("null singular value < 1e-6 * s_max", len(nnull) == 1 and float(sv[nnull[0]]) < 1e-6 * max(float(s) for s in sv), [float(sv[i]) for i in nnull])
    else:
        c.check("singular_values has 4 entries", False, sv)
    rv = idf.get("right_vectors") or []
    dot_null = None
    if len(nnull) == 1 and len(rv) == 4:
        vnull = [float(x) for x in rv[nnull[0]]]
        dot_null = abs(vnull[NULL_COL]) / math.sqrt(sum(x * x for x in vnull))
    c.numbers["null_direction_abs_dot_e3"] = dot_null
    c.check("near-null direction aligned with the zero column (|dot| > 0.999)", dot_null is not None and dot_null > 0.999, dot_null)
    cn = idf.get("condition_numbers")
    c.numbers["condition_numbers"] = cn
    if len(nnull) == 1 and isinstance(cn, list) and len(cn) == 4:
        cnull = cn[nnull[0]]
        c.check("null condition number is 'inf' string or > 1e6", cnull == "inf" or (is_num(cnull) and float(cnull) > 1e6), cnull)
    sj = idf.get("scaled_jacobian")
    if isinstance(sj, list) and len(sj) == 12 and J is not None and jac_err is not None:
        err = max(abs(float(sj[r][j]) - float(J[r][j]) / rows[r]["sigma"]) for r in range(12) for j in range(NVAR))
        c.check("scaled_jacobian == diag(1/sigma) J within 1e-9", err < 1e-9, err)
    # exploration
    ex = run.get("exploration") or {}
    c.check("exploration ok, COMPLETE, not empty", ex.get("ok") is True and ex.get("status") == "COMPLETE" and ex.get("empty_region") is False, {k: ex.get(k) for k in ("ok", "status", "empty_region", "stage_reached")})
    anchor = ex.get("anchor") or {}
    c.check("anchor admitted (seed is admitted)", anchor.get("admitted") is True, anchor.get("admitted"))
    au = [float(x) for x in (anchor.get("u") or [])]
    c.check("anchor u == trial u (0.5 each) within 1e-12", len(au) == NVAR and all(abs(au[j] - 0.5) < 1e-12 for j in range(NVAR)), au)
    check_points_against_toy(c, toy, run, "E1")
    adm = ex.get("admitted_points") or []
    c.check("admitted points non-empty and anchor among them", len(adm) >= 1 and any(all(abs(float(p["u"][j]) - au[j]) < 1e-12 for j in range(NVAR)) for p in adm), len(adm))
    li = [p.get("log_index") for p in adm] + [p.get("log_index") for p in (ex.get("rejected_points") or [])]
    c.check("log_index unique across admitted+rejected", len(li) == len(set(li)), len(li) - len(set(li)))
    # hull box vs analytic boundary along each identified direction
    hull = ex.get("hull_box") or {}
    bnd = ex.get("boundary") or {}
    per_dir = []
    all_ok = True
    if len(rv) == 4 and len(au) == NVAR:
        for k in ident:
            v = [float(x) for x in rv[k]]
            t_lo, t_hi, box_lo, box_hi = analytic_line_interval(toy, au, v)
            res_hi = march_resolution(t_hi, ENGINE_CFG["march_step"], ENGINE_CFG["bisection_steps"])
            res_lo = march_resolution(-t_lo, ENGINE_CFG["march_step"], ENGINE_CFG["bisection_steps"])
            hb = getidx(hull, k) or {}
            bb = getidx(bnd, k) or {}
            hmin, hmax = hb.get("min"), hb.get("max")
            ok_hi = is_finite_num(hmax) and abs(float(hmax) - t_hi) <= 2 * res_hi + 1e-9
            ok_lo = is_finite_num(hmin) and abs(float(hmin) - t_lo) <= 2 * res_lo + 1e-9
            all_ok = all_ok and ok_hi and ok_lo
            per_dir.append({"direction_index": k, "vector_u": v, "analytic_t_min": t_lo, "analytic_t_max": t_hi,
                            "box_binding": [box_lo, box_hi], "hull_min": hmin, "hull_max": hmax,
                            "boundary_minus": bb.get("minus"), "boundary_plus": bb.get("plus"),
                            "tolerance_min": 2 * res_lo, "tolerance_max": 2 * res_hi, "ok": ok_lo and ok_hi})
    c.numbers["hull_vs_analytic"] = per_dir
    c.check("hull_box extents match analytic boundary within 2*bisection resolution (all identified directions)", len(per_dir) == 3 and all_ok, [d for d in per_dir if not d["ok"]])
    c.check("no box edge binds in E1 (fixture design)", all(not d["box_binding"][0] and not d["box_binding"][1] for d in per_dir), None)
    # unidentified direction carried
    ud = ex.get("unidentified_directions") or []
    c.numbers["unidentified_directions"] = ud
    c.check("exactly one unidentified direction carried", len(ud) == 1, len(ud))
    if len(ud) == 1 and len(nnull) == 1:
        u0 = ud[0]
        c.check("unidentified index == near_null index", u0.get("index") == nnull[0], u0.get("index"))
        vv = [float(x) for x in (u0.get("vector_u") or [])]
        c.check("unidentified vector aligned with e3", len(vv) == NVAR and abs(vv[NULL_COL]) / math.sqrt(sum(x * x for x in vv)) > 0.999, vv)
        c.check("sensitivity ~ 0 (< 1e-6)", is_finite_num(u0.get("sensitivity")) and float(u0["sensitivity"]) < 1e-6, u0.get("sensitivity"))
        tp = u0.get("trial_projection")
        exp_abs = abs(sum(0.5 * vv[j] for j in range(NVAR))) if len(vv) == NVAR else None
        conv = None
        if is_finite_num(tp) and exp_abs is not None:
            if abs(abs(float(tp)) - exp_abs) < 1e-6:
                conv = "u_trial.v"
            elif abs(float(tp)) < 1e-9:
                conv = "(u_trial-anchor).v (=0 here)"
        c.numbers["trial_projection_convention"] = conv
        c.check("trial_projection finite and equal to u_trial.v or (u_trial-anchor).v", conv is not None, (tp, exp_abs))
        c.check("singular_value carried on unidentified direction", is_finite_num(u0.get("singular_value")), u0.get("singular_value"))
    # evaluation log shape
    bad = []
    for e in log_entries(run):
        for key in ("index", "purpose", "u", "theta_internal", "theta_natural", "prediction", "valid", "admitted", "reasons", "exception"):
            if key not in e:
                bad.append((e.get("index"), key))
    c.check("every evaluation_log entry has the 10 interface keys", not bad, bad[:10])
    purposes = sorted(set(str(e.get("purpose")) for e in log_entries(run)))
    c.numbers["log_purposes"] = purposes
    c.check("evaluations_used <= budget", run.get("evaluations_used", 10 ** 9) <= ENGINE_CFG["budget"], run.get("evaluations_used"))
    # JSON-serialisable
    try:
        cj(run)
        c.check("run result is canonical-JSON serialisable (no NaN/inf, no numpy)", True)
    except Exception as exc:
        c.check("run result is canonical-JSON serialisable (no NaN/inf, no numpy)", False, repr(exc))

def case_E2(ctx, c):
    rows = ctx["rows"]
    toy = ToyForward(rows)
    seed = [0.6, 0.6, 0.6, 0.5]
    sp = toy.speeds_from_u(seed)
    c.check("fixture: shifted seed is not admitted under the toy", not toy.admitted_speeds(sp))
    run = run_engine(ctx, toy, seed)
    ex = run.get("exploration") or {}
    c.numbers["evaluations_used"] = run.get("evaluations_used")
    c.check("ok True", run.get("ok") is True, run.get("reasons"))
    c.check("status COMPLETE", run.get("status") == "COMPLETE", run.get("status"))
    c.check("empty_region False", ex.get("empty_region") is False, ex.get("empty_region"))
    c.check("anchor reported not admitted", (ex.get("anchor") or {}).get("admitted") is False, (ex.get("anchor") or {}).get("admitted"))
    jac = run.get("jacobian") or {}
    c.check("seed_admitted False in jacobian", jac.get("seed_admitted") is False, jac.get("seed_admitted"))
    adm = ex.get("admitted_points") or []
    c.check("repair found >= 1 admitted point", len(adm) >= 1, len(adm))
    check_points_against_toy(c, toy, run, "E2")
    if adm:
        first = adm[0]
        c.numbers["first_admitted_u"] = [float(x) for x in first["u"]]
        c.numbers["first_admitted_log_index"] = first.get("log_index")
        c.check("first admitted point lies in the box", all(0.0 <= float(x) <= 1.0 for x in first["u"]))
        # the null coordinate must not have been moved by the repair (restricted to identified directions)
        c.check("repair did not move the null coordinate (|u3-0.5|<1e-9)", abs(float(first["u"][NULL_COL]) - 0.5) < 1e-9, float(first["u"][NULL_COL]))
    rp = [e for e in log_entries(run) if "repair" in str(e.get("purpose", "")).lower()]
    c.numbers["repair_log_entries"] = len(rp)
    c.check("evaluation_log length == evaluations_used", len(log_entries(run)) == run.get("evaluations_used"), len(log_entries(run)))

def _e3_run_and_check(ctx, c, tag, offsets, expect_repair_evaluations):
    rows = ctx["rows"]
    toy = ToyForward(rows, offsets=offsets)
    run = run_engine(ctx, toy, [None] * NVAR)
    ex = run.get("exploration") or {}
    log = log_entries(run)
    c.numbers[tag] = {"evaluations_used": run.get("evaluations_used"), "status": run.get("status"), "ok": run.get("ok"),
                      "empty_region": ex.get("empty_region"), "stage_reached": ex.get("stage_reached"),
                      "repair_log_entries": len([e for e in log if "repair" in str(e.get("purpose", "")).lower()]),
                      "rejected_points": len(ex.get("rejected_points") or []), "offsets_in_sigma_units": {k: v for k, v in offsets.items()}}
    c.check(tag + ": status NO_ADMITTED_POINT", run.get("status") == "NO_ADMITTED_POINT", run.get("status"))
    c.check(tag + ": empty_region True", ex.get("empty_region") is True, ex.get("empty_region"))
    c.check(tag + ": no admitted points", not (ex.get("admitted_points") or []), len(ex.get("admitted_points") or []))
    c.check(tag + ": evaluation_log length == evaluations_used == toy calls", len(log) == run.get("evaluations_used") == toy.calls, (len(log), run.get("evaluations_used"), toy.calls))
    c.check(tag + ": no log entry labelled admitted", all(e.get("admitted") is not True for e in log), None)
    bad = [e.get("index") for e in log if toy.admitted_speeds(toy.speeds_from_theta(e["theta_natural"]))]
    c.check(tag + ": toy recompute: no evaluated point is admitted", not bad, bad)
    c.check(tag + ": rejected_points preserved (>=1)", len(ex.get("rejected_points") or []) >= 1, len(ex.get("rejected_points") or []))
    c.check(tag + ": evaluations_used <= budget", run.get("evaluations_used", 10 ** 9) <= ENGINE_CFG["budget"])
    c.check(tag + ": jacobian stage completed (9 evaluations) before the repair", (run.get("jacobian") or {}).get("ok") is True and len(log) >= 9, len(log))
    nrep = c.numbers[tag]["repair_log_entries"]
    if expect_repair_evaluations:
        c.check(tag + ": repair steps were evaluated (>=1 repair-purpose entry, <= repair_iterations)", 1 <= nrep <= ENGINE_CFG["repair_iterations"], nrep)
        c.check(tag + ": every repair point lies in the box", all(all(0.0 <= float(x) <= 1.0 for x in e["u"]) for e in log if "repair" in str(e.get("purpose", "")).lower()), None)
        c.check(tag + ": repair never moved the null coordinate (|u3-0.5|<1e-9)", all(abs(float(e["u"][NULL_COL]) - 0.5) < 1e-9 for e in log if "repair" in str(e.get("purpose", "")).lower()), None)
    else:
        c.note(tag + ": Gauss-Newton step is exactly zero by construction (S^T r = 0); repair-purpose entries = %d (not judged)" % nrep)
    c.note(tag + ": ok=%r for the empty-region result (interface does not fix ok for a registered empty region; not judged)" % run.get("ok"))

def case_E3(ctx, c):
    rows = ctx["rows"]
    z = ctx["z"]
    c.check("fixture: conflicting rows 0 and 2 have identical pattern rows", all(PATTERNS[j][0] == PATTERNS[j][2] for j in range(3)))
    # E3a (primary): same linear form q for rows 0 and 2; row 0 needs q in [-4z,-2z], row 2 needs q in [4z,6z]: disjoint,
    # and the least-squares (Gauss-Newton) target q = +z is nonzero, so repair steps are evaluated and all fail.
    _e3_run_and_check(ctx, c, "E3a_asymmetric", {rows[0]["id"]: +3.0 * z * rows[0]["sigma"], rows[2]["id"]: -5.0 * z * rows[2]["sigma"]}, True)
    # E3b (soft): opposite offsets +-3z make S^T r = 0 exactly; the Gauss-Newton step is zero and an implementation may stop early.
    _e3_run_and_check(ctx, c, "E3b_symmetric_zero_step", {rows[0]["id"]: +3.0 * z * rows[0]["sigma"], rows[2]["id"]: -3.0 * z * rows[2]["sigma"]}, False)

def case_E4(ctx, c):
    rows = ctx["rows"]
    ids = [r["id"] for r in rows]
    rules = {"raise_if": lambda u: u[0] > 0.72,
             "nan_if": lambda u: u[1] < 0.25, "nan_row": ids[5],
             "drop_if": lambda u: u[2] > 0.75, "drop_row": ids[7]}
    toy = ToyForward(rows, fail_rules=rules)
    run = run_engine(ctx, toy, [None] * NVAR)
    ex = run.get("exploration") or {}
    log = log_entries(run)
    c.numbers["evaluations_used"] = run.get("evaluations_used")
    c.numbers["toy_raised"] = toy.raised
    c.numbers["toy_nan_returned"] = toy.nan_returned
    c.numbers["toy_dropped"] = toy.dropped
    c.check("run completes: ok True, status COMPLETE", run.get("ok") is True and run.get("status") == "COMPLETE", (run.get("ok"), run.get("status"), run.get("reasons")))
    c.check("fixture exercised: >=1 raise, >=1 NaN, >=1 missing id", toy.raised >= 1 and toy.nan_returned >= 1 and toy.dropped >= 1, (toy.raised, toy.nan_returned, toy.dropped))
    c.check("evaluation_log length == toy calls (raising calls logged too)", len(log) == toy.calls, (len(log), toy.calls))
    invalid = [e for e in log if e.get("valid") is not True]
    c.numbers["invalid_log_entries"] = len(invalid)
    c.check("invalid log entries == raised + nan + dropped", len(invalid) == toy.raised + toy.nan_returned + toy.dropped, (len(invalid), toy.raised + toy.nan_returned + toy.dropped))
    c.check("no invalid entry is admitted", all(e.get("admitted") is not True for e in invalid), None)
    c.check("every invalid entry has reasons or exception text", all((e.get("reasons") and len(e.get("reasons")) > 0) or e.get("exception") for e in invalid), None)
    exc_entries = [e for e in log if e.get("exception")]
    c.numbers["exception_entries"] = len(exc_entries)
    c.check("exception entries == raised, text mentions FixtureForwardError or its message", len(exc_entries) == toy.raised and all(("FixtureForwardError" in str(e["exception"])) or ("deliberately" in str(e["exception"])) for e in exc_entries), [str(e.get("exception"))[:120] for e in exc_entries[:3]])
    c.check("exception entries have prediction None and valid False", all(e.get("prediction") is None and e.get("valid") is False for e in exc_entries), None)
    # toy-side recomputation of the invalid classes
    nan_entries, drop_entries = [], []
    for e in log:
        if e.get("exception"):
            continue
        u = toy.u_from_theta(e["theta_natural"])
        if rules["nan_if"](u):
            nan_entries.append(e)
        if rules["drop_if"](u):
            drop_entries.append(e)
    c.check("NaN-row evaluations logged valid False with a reason", all(e.get("valid") is False and e.get("reasons") for e in nan_entries) and len(nan_entries) == toy.nan_returned, (len(nan_entries), toy.nan_returned))
    c.check("missing-id evaluations logged valid False with a reason", all(e.get("valid") is False and e.get("reasons") for e in drop_entries) and len(drop_entries) == toy.dropped, (len(drop_entries), toy.dropped))
    # rejected/admitted lists: admitted must all be truly admitted
    adm = ex.get("admitted_points") or []
    bad = [p.get("log_index") for p in adm if not toy.admitted_speeds(toy.speeds_from_theta(p["theta_natural"]))]
    c.check("admitted points all truly admitted under the toy", not bad, bad)
    c.numbers["admitted_count"] = len(adm)
    c.numbers["rejected_count"] = len(ex.get("rejected_points") or [])
    c.check("invalid evaluations never appear in admitted_points", all(toy.admitted_speeds(toy.speeds_from_theta(p["theta_natural"])) for p in adm), None)
    try:
        cj(run)
        c.check("result JSON-serialisable", True)
    except Exception as exc:
        c.check("result JSON-serialisable", False, repr(exc))

def case_E5(ctx, c):
    rows = ctx["rows"]
    for budget in (30, 5):
        toy = ToyForward(rows)
        run = run_engine(ctx, toy, [None] * NVAR, budget=budget)
        ex = run.get("exploration") or {}
        log = log_entries(run)
        tag = "budget%d" % budget
        c.numbers[tag] = {"status": run.get("status"), "stage_reached": ex.get("stage_reached", run.get("stage_reached")),
                          "evaluations_used": run.get("evaluations_used"), "log_len": len(log), "toy_calls": toy.calls,
                          "admitted": len(ex.get("admitted_points") or []), "rejected": len(ex.get("rejected_points") or []),
                          "ok": run.get("ok")}
        c.check(tag + ": status BUDGET_EXHAUSTED", run.get("status") == "BUDGET_EXHAUSTED", run.get("status"))
        c.check(tag + ": evaluations_used == budget", run.get("evaluations_used") == budget, run.get("evaluations_used"))
        c.check(tag + ": evaluation_log length == budget", len(log) == budget, len(log))
        c.check(tag + ": toy never called more than budget", toy.calls == budget, toy.calls)
        sr = ex.get("stage_reached", run.get("stage_reached"))
        c.check(tag + ": stage_reached present (non-empty)", sr not in (None, ""), sr)
        if budget == 30:
            adm = ex.get("admitted_points") or []
            rej = ex.get("rejected_points") or []
            c.check(tag + ": partial admitted list preserved (anchor admitted, >=1)", len(adm) >= 1, len(adm))
            c.check(tag + ": partial admitted/rejected points have log_index < budget", all(isinstance(p.get("log_index"), int) and 0 <= p["log_index"] < budget for p in adm + rej), None)
            # consistency with log entries: an admitted point's u must appear in the log as admitted
            def _in_log(p, flag):
                for e in log:
                    if len(e.get("u", [])) == NVAR and all(abs(float(e["u"][j]) - float(p["u"][j])) < 1e-12 for j in range(NVAR)) and e.get("admitted") is flag:
                        return True
                return False
            c.check(tag + ": admitted points match admitted log entries", all(_in_log(p, True) for p in adm), None)
            c.check(tag + ": rejected points match non-admitted log entries", all(_in_log(p, False) or _in_log(p, None) for p in rej), None)
            check_points_against_toy(c, toy, run, "E5b30")
            c.check(tag + ": jacobian completed before exhaustion (9 evaluations)", (run.get("jacobian") or {}).get("ok") is True, (run.get("jacobian") or {}).get("reasons"))

def case_E6(ctx, c):
    rows = ctx["rows"]
    t1 = ToyForward(rows)
    r1 = run_engine(ctx, t1, [None] * NVAR)
    t2 = ToyForward(rows)
    r2 = run_engine(ctx, t2, [None] * NVAR)
    try:
        s1, s2 = cj(r1), cj(r2)
    except Exception as exc:
        c.check("results canonical-JSON serialisable", False, repr(exc))
        return
    c.numbers["len_json_run1"] = len(s1)
    c.numbers["len_json_run2"] = len(s2)
    c.numbers["sha256_run1"] = sha256_bytes(s1.encode("utf-8"))
    c.numbers["sha256_run2"] = sha256_bytes(s2.encode("utf-8"))
    same = s1 == s2
    c.check("two identical configurations give byte-identical canonical JSON", same)
    if not same:
        diffs = []
        def walk(a, b, path):
            if len(diffs) > 20:
                return
            if isinstance(a, dict) and isinstance(b, dict):
                for k in sorted(set(a) | set(b)):
                    walk(a.get(k), b.get(k), path + "/" + str(k))
            elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
                for i, (x, y) in enumerate(zip(a, b)):
                    walk(x, y, path + "[%d]" % i)
            elif a != b:
                diffs.append(path)
        walk(r1, r2, "")
        c.numbers["first_differing_paths"] = diffs
    c.check("same evaluation count both runs", r1.get("evaluations_used") == r2.get("evaluations_used") == t1.calls == t2.calls, (r1.get("evaluations_used"), r2.get("evaluations_used")))
    # also: E1 stored run must equal these (same config)
    e1 = ctx["store"].get("E1_run")
    if e1 is not None:
        try:
            c.check("E1 run equals E6 runs (same configuration)", cj(e1) == s1)
        except Exception as exc:
            c.check("E1 run equals E6 runs (same configuration)", False, repr(exc))

def case_E7(ctx, c):
    rows = ctx["rows"]
    toy = ToyForward(rows)
    run = run_engine(ctx, toy, [None] * NVAR, sha=WRONG_SHA)
    c.numbers["ok"] = run.get("ok")
    c.numbers["toy_calls"] = toy.calls
    c.numbers["evaluations_used"] = run.get("evaluations_used")
    c.check("wrong region hash -> ok False", run.get("ok") is False, run.get("reasons"))
    c.check("reasons non-empty", bool(run.get("reasons")), run.get("reasons"))
    c.check("forward never called", toy.calls == 0, toy.calls)
    c.check("evaluations_used is 0 or absent", run.get("evaluations_used") in (0, None), run.get("evaluations_used"))
    c.check("evaluation_log empty or absent", not log_entries(run), len(log_entries(run)))
    reg = ctx["engine"].load_observation_region(path=REGION_PATH, expected_sha256=WRONG_SHA)
    c.check("load_observation_region refuses wrong hash", reg.get("ok") is False, reg.get("reasons"))
    reg2 = ctx["engine"].load_observation_region(path=REGION_PATH + ".does_not_exist", expected_sha256=REGION_SHA)
    c.check("load_observation_region on a missing file -> ok False, no raise", reg2.get("ok") is False, reg2.get("reasons"))

# ----------------------------------------------------------------------------------------------------
# Module 2 fixtures
# ----------------------------------------------------------------------------------------------------

class ToyNgc:
    """Synthetic 43-query forward keyed by the real query ids. v_q = 150 + 10 a + 3 b (k+1)/43 + 0.5 sin(k+1)."""

    def __init__(self, qids, raise_a=None, nan_a=None, nan_query=None):
        self.qids = list(qids)
        self.raise_a = raise_a
        self.nan_a = nan_a
        self.nan_query = nan_query
        self.calls = 0
        self.raised = 0

    def speeds(self, theta):
        a, b = float(theta["a"]), float(theta["b"])
        return {q: 150.0 + 10.0 * a + 3.0 * b * (k + 1) / 43.0 + 0.5 * math.sin(k + 1) for k, q in enumerate(self.qids)}

    def __call__(self, theta_natural):
        self.calls += 1
        a = float(theta_natural["a"])
        if self.raise_a is not None and abs(a - self.raise_a) < 1e-12:
            self.raised += 1
            raise FixtureForwardError("fixture forward_ngc raised deliberately at a=%r" % a)
        sp = self.speeds(theta_natural)
        if self.nan_a is not None and abs(a - self.nan_a) < 1e-12:
            sp[self.nan_query] = float("nan")
        return {"speeds_km_s": sp, "valid": True, "reasons": []}

def make_points(n):
    pts = []
    for i in range(n):
        a = 0.1 * i + 0.05
        b = 0.5 - 0.07 * i
        pts.append({"u": [a, b, 0.5], "theta_natural": {"a": a, "b": b, "c": 0.5}, "role": "interior", "log_index": 10 + 3 * i})
    return pts

def medians(vals):
    """All median conventions I will accept for an even count: numpy mean-of-middle, lower, upper. Odd: one value."""
    s = sorted(vals)
    n = len(s)
    if n == 0:
        return []
    if n % 2 == 1:
        return [s[n // 2]]
    return [0.5 * (s[n // 2 - 1] + s[n // 2]), s[n // 2 - 1], s[n // 2]]

def case_F1(ctx, c):
    frz = ctx["freeze"]
    r = frz.load_query_manifest(path=MANIFEST_PATH, expected_sha256=MANIFEST_SHA)
    c.check("ok True with the correct hash", r.get("ok") is True, r.get("reasons"))
    c.check("sha256 reported", r.get("sha256") == MANIFEST_SHA, r.get("sha256"))
    exp_ids = ["NGC3198-Q%02d" % k for k in range(1, 44)]
    c.check("43 ids in order Q01..Q43", r.get("query_ids") == exp_ids, (r.get("query_ids") or [])[:5])
    c.check("query_ids equal my own parse of the manifest", r.get("query_ids") == ctx["qids"], None)
    rt = r.get("radii_text") or {}
    c.check("radii_text bound (Q01 -> '0.32', Q43 -> '44.08')", rt.get("NGC3198-Q01") == "0.32" and rt.get("NGC3198-Q43") == "44.08", (rt.get("NGC3198-Q01"), rt.get("NGC3198-Q43")))
    c.check("rad_unit kpc", r.get("rad_unit") == "kpc", r.get("rad_unit"))
    c.check("no velocity-like key in the load result", not find_forbidden_keys(r), find_forbidden_keys(r))
    rw = frz.load_query_manifest(path=MANIFEST_PATH, expected_sha256=WRONG_SHA)
    c.check("wrong hash refused (ok False)", rw.get("ok") is False, rw.get("reasons"))
    c.check("wrong hash: no query_ids returned", not rw.get("query_ids"), rw.get("query_ids"))
    rm = frz.load_query_manifest(path=MANIFEST_PATH + ".missing", expected_sha256=MANIFEST_SHA)
    c.check("missing file -> ok False, no raise", rm.get("ok") is False, rm.get("reasons"))
    ctx["store"]["qids_mod"] = r.get("query_ids") if r.get("ok") is True else None

def synthetic_exploration():
    a = [0.5, 0.5, 0.5]
    def pt(li, du):
        u = [a[j] + du[j] for j in range(3)]
        return {"u": u, "theta_internal": list(u), "theta_natural": {"a": u[0], "b": u[1], "c": u[2]},
                "prediction": {"speeds_km_s": {"R1": 1.0 + u[0], "R2": 2.0 + u[1]}, "valid": True, "reasons": []},
                "log_index": li}
    adm = [pt(9, [0.0, 0.0, 0.0]),          # anchor
           pt(10, [0.3, 0.0, 0.0]),         # max e0
           pt(12, [-0.2, 0.0, 0.0]),        # min e0
           pt(14, [0.0, 0.25, 0.0]),        # max e1
           pt(16, [0.0, -0.15, 0.0]),       # min e1
           pt(20, [0.1, 0.05, 0.0]), pt(21, [-0.05, 0.1, 0.0]), pt(25, [0.02, -0.1, 0.0]), pt(30, [0.15, 0.15, 0.0])]
    rej = [pt(11, [0.35, 0.0, 0.0]), pt(13, [-0.25, 0.0, 0.0]), pt(15, [0.0, 0.3, 0.0]), pt(17, [0.0, -0.2, 0.0])]
    ident = {"ok": True, "scaled_jacobian": [[5.0, 0.0, 0.0], [0.0, 3.0, 0.0]], "singular_values": [5.0, 3.0, 0.0],
             "right_vectors": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]], "identified": [0, 1], "near_null": [2],
             "condition_numbers": [1.0, 5.0 / 3.0, "inf"], "null_tolerance": 1e-6, "reasons": []}
    X = {"ok": True, "status": "COMPLETE", "stage_reached": "hull", "anchor": {"u": a, "theta_natural": {"a": 0.5, "b": 0.5, "c": 0.5}, "admitted": True},
         "admitted_points": adm, "rejected_points": rej,
         "boundary": {0: {"minus": 0.2, "plus": 0.3}, 1: {"minus": 0.15, "plus": 0.25}},
         "hull_box": {0: {"min": -0.2, "max": 0.3}, 1: {"min": -0.15, "max": 0.25}},
         "unidentified_directions": [{"index": 2, "vector_u": [0.0, 0.0, 1.0], "singular_value": 0.0, "trial_projection": 0.5, "sensitivity": 0.0}],
         "evaluations_used": 31, "empty_region": False, "reasons": [],
         "identifiability": ident, "right_vectors": ident["right_vectors"], "identified": [0, 1], "near_null": [2],
         "identified_directions": [{"index": 0, "vector_u": [1.0, 0.0, 0.0], "singular_value": 5.0}, {"index": 1, "vector_u": [0.0, 1.0, 0.0], "singular_value": 3.0}]}
    R = dict(X)
    R["exploration"] = copy.deepcopy(X)
    R["identifiability"] = ident
    R["bounds_semantics"] = BOUNDS_SEMANTICS
    expected = {"hull": {10, 12, 14, 16}, "anchor": 9, "interior_pool": [20, 21, 25, 30]}
    return R, expected

def call_select(frz, run_like, interior_count):
    r = frz.select_representative_points(exploration=run_like, interior_count=interior_count)
    layout = "run_result"
    if r.get("ok") is not True and isinstance(run_like.get("exploration"), dict):
        r2 = frz.select_representative_points(exploration=run_like["exploration"], interior_count=interior_count)
        if r2.get("ok") is True:
            return r2, "exploration_subdict"
        return r, layout + " (both layouts refused: " + str(r.get("reasons")) + " | " + str(r2.get("reasons")) + ")"
    return r, layout

def case_F2(ctx, c):
    frz = ctx["freeze"]
    R, exp = synthetic_exploration()
    r, layout = call_select(frz, R, 2)
    c.numbers["layout_accepted"] = layout
    c.check("ok True (interior_count=2)", r.get("ok") is True, r.get("reasons"))
    pts = r.get("points") or []
    roles = [p.get("role") for p in pts]
    li = [p.get("log_index") for p in pts]
    c.numbers["roles"] = roles
    c.numbers["log_indices"] = li
    c.numbers["hull_vertex_count"] = r.get("hull_vertex_count")
    c.numbers["interior_count_used"] = r.get("interior_count_used")
    hull_li = {p.get("log_index") for p in pts if p.get("role") == "hull_vertex"}
    c.check("all four hull vertices present with role hull_vertex", hull_li == exp["hull"], sorted(hull_li, key=str))
    c.check("hull_vertex_count == 4", r.get("hull_vertex_count") == 4, r.get("hull_vertex_count"))
    c.check("anchor present with role anchor", any(p.get("role") == "anchor" and p.get("log_index") == exp["anchor"] for p in pts), None)
    interior = [p for p in pts if p.get("role") == "interior"]
    c.check("interior count respected (2 interior points)", len(interior) == 2 and r.get("interior_count_used") == 2, (len(interior), r.get("interior_count_used")))
    c.check("interior points drawn from the remaining admitted points", all(p.get("log_index") in exp["interior_pool"] for p in interior), [p.get("log_index") for p in interior])
    c.check("interior points in ascending log_index", [p.get("log_index") for p in interior] == sorted(p.get("log_index") for p in interior), None)
    c.check("no duplicate log_index", len(li) == len(set(li)), li)
    c.check("total points == 7", len(pts) == 7, len(pts))
    c.check("order: hull vertices, then anchor, then interior", roles == ["hull_vertex"] * 4 + ["anchor"] + ["interior"] * 2, roles)
    c.check("each point carries u and theta_natural", all(isinstance(p.get("u"), list) and isinstance(p.get("theta_natural"), dict) for p in pts), None)
    r_all, _ = call_select(frz, R, 100)
    pts_all = r_all.get("points") or []
    c.check("interior_count=100 -> all 4 remaining points used (9 total)", r_all.get("ok") is True and len(pts_all) == 9 and r_all.get("interior_count_used") == 4, (len(pts_all), r_all.get("interior_count_used")))
    r0, _ = call_select(frz, R, 0)
    c.check("interior_count=0 -> hull vertices + anchor only (5)", r0.get("ok") is True and len(r0.get("points") or []) == 5, len(r0.get("points") or []))
    # duplicate removal: a point that is extreme in both directions and also the anchor as an extreme
    R2, _ = synthetic_exploration()
    X2 = R2["exploration"]
    for tgt in (R2, X2):
        tgt["admitted_points"] = [p for p in tgt["admitted_points"] if p["log_index"] not in (10, 14)]
        both = {"u": [0.8, 0.75, 0.5], "theta_internal": [0.8, 0.75, 0.5], "theta_natural": {"a": 0.8, "b": 0.75, "c": 0.5},
                "prediction": {"speeds_km_s": {"R1": 1.8, "R2": 2.75}, "valid": True, "reasons": []}, "log_index": 40}
        tgt["admitted_points"].append(both)
        tgt["hull_box"] = {0: {"min": -0.2, "max": 0.3}, 1: {"min": -0.15, "max": 0.25}}
    rd, _ = call_select(frz, R2, 2)
    pd = rd.get("points") or []
    lid = [p.get("log_index") for p in pd]
    c.check("shared extreme point: ok, no duplicate log_index", rd.get("ok") is True and len(lid) == len(set(lid)), lid)
    c.check("shared extreme point appears once as hull_vertex", sum(1 for p in pd if p.get("log_index") == 40) == 1 and any(p.get("log_index") == 40 and p.get("role") == "hull_vertex" for p in pd), lid)
    c.numbers["shared_extreme_hull_vertex_count_reported"] = rd.get("hull_vertex_count")
    # F2b: the real E1 exploration (if available)
    e1 = ctx["store"].get("E1_run")
    if e1 is not None and e1.get("ok") is True:
        rr, layout_e1 = call_select(frz, e1, 5)
        c.numbers["E1_layout_accepted"] = layout_e1
        c.check("E1 exploration: ok", rr.get("ok") is True, rr.get("reasons"))
        ppts = rr.get("points") or []
        lie = [p.get("log_index") for p in ppts]
        c.check("E1 exploration: no duplicate log_index", len(lie) == len(set(lie)), None)
        ex = e1.get("exploration") or {}
        idf = e1.get("identifiability") or {}
        au = [float(x) for x in ex["anchor"]["u"]]
        adm = ex.get("admitted_points") or []
        rv = idf.get("right_vectors") or []
        ok_all = True
        detail = []
        for k in idf.get("identified") or []:
            v = [float(x) for x in rv[k]]
            proj = [(sum((float(p["u"][j]) - au[j]) * v[j] for j in range(NVAR)), p["log_index"]) for p in adm]
            pmin = min(x for x, _ in proj); pmax = max(x for x, _ in proj)
            hv = [p for p in ppts if p.get("role") == "hull_vertex"]
            hp = [sum((float(p["u"][j]) - au[j]) * v[j] for j in range(NVAR)) for p in hv]
            has_min = any(abs(x - pmin) < 1e-12 for x in hp)
            has_max = any(abs(x - pmax) < 1e-12 for x in hp)
            ok_all = ok_all and has_min and has_max
            detail.append({"k": k, "pmin": pmin, "pmax": pmax, "has_min": has_min, "has_max": has_max})
        c.numbers["E1_hull_check"] = detail
        c.check("E1 exploration: returned hull vertices attain min and max projection per identified direction", ok_all and bool(detail), detail)
        c.check("E1 exploration: anchor present", any(p.get("role") == "anchor" for p in ppts), None)
        c.check("E1 exploration: interior_count_used <= 5", (rr.get("interior_count_used") or 0) <= 5, rr.get("interior_count_used"))
        ctx["store"]["E1_points"] = ppts
    else:
        c.note("E1 run unavailable; F2b on the real exploration skipped")

def case_F3(ctx, c):
    frz = ctx["freeze"]
    qids = ctx["store"].get("qids_mod") or ctx["qids"]
    # F3a: all valid, 5 points
    pts = make_points(5)
    fwd = ToyNgc(qids)
    r = frz.evaluate_envelopes(forward_ngc=fwd, points=pts, query_ids=qids, budget=50)
    c.check("F3a ok, COMPLETE", r.get("ok") is True and r.get("status") == "COMPLETE", (r.get("ok"), r.get("status"), r.get("reasons")))
    c.check("F3a evaluations_used == 5 == toy calls", r.get("evaluations_used") == 5 == fwd.calls, (r.get("evaluations_used"), fwd.calls))
    c.check("F3a evaluation_log length 5", len(r.get("evaluation_log") or []) == 5, len(r.get("evaluation_log") or []))
    pp = r.get("per_point") or []
    c.check("F3a per_point: 5 entries, point_index 0..4, all valid", [p.get("point_index") for p in pp] == list(range(5)) and all(p.get("valid") is True for p in pp), [(p.get("point_index"), p.get("valid")) for p in pp])
    env = r.get("envelopes") or {}
    c.check("F3a envelopes cover exactly the 43 query ids", sorted(env.keys()) == sorted(qids), len(env))
    sp = [fwd.speeds(p["theta_natural"]) for p in pts]
    bad = []
    for q in qids:
        vals = [s[q] for s in sp]
        e = env.get(q) or {}
        ok = (close(e.get("min"), min(vals), 1e-9) and close(e.get("max"), max(vals), 1e-9)
              and close(e.get("central"), medians(vals)[0], 1e-9) and e.get("n_points") == 5 and e.get("n_valid") == 5 and e.get("valid") is True)
        if not ok:
            bad.append((q, e, min(vals), max(vals), medians(vals)[0]))
    c.check("F3a per-query min/max/central(median)/n_points/n_valid/valid match recomputation", not bad, bad[:3])
    c.numbers["F3a_example_Q01"] = env.get(qids[0])
    ctx["store"]["env_A"] = env
    ctx["store"]["points_A"] = pts
    # F3b: 6 points, point 2 raises
    pts = make_points(6)
    fwd = ToyNgc(qids, raise_a=pts[2]["theta_natural"]["a"])
    r = frz.evaluate_envelopes(forward_ngc=fwd, points=pts, query_ids=qids, budget=50)
    pp = r.get("per_point") or []
    c.check("F3b run completes (status COMPLETE), toy raised once", r.get("status") == "COMPLETE" and fwd.raised == 1, (r.get("status"), fwd.raised, r.get("reasons")))
    p2 = next((p for p in pp if p.get("point_index") == 2), None)
    c.check("F3b per_point[2] valid False with exception text", p2 is not None and p2.get("valid") is False and bool(p2.get("exception")) and ("FixtureForwardError" in str(p2.get("exception")) or "deliberately" in str(p2.get("exception"))), p2)
    c.check("F3b other points valid", all(p.get("valid") is True for p in pp if p.get("point_index") != 2) and len(pp) == 6, [(p.get("point_index"), p.get("valid")) for p in pp])
    env = r.get("envelopes") or {}
    c.check("F3b every query valid False (a raising point invalidates every query)", bool(env) and all((env.get(q) or {}).get("valid") is False for q in qids), [(q, (env.get(q) or {}).get("valid")) for q in qids[:3]])
    c.check("F3b n_valid == 5, n_points == 6 for every query", all((env.get(q) or {}).get("n_valid") == 5 and (env.get(q) or {}).get("n_points") == 6 for q in qids), env.get(qids[0]))
    sp = [fwd.speeds(p["theta_natural"]) for i, p in enumerate(pts) if i != 2]
    bad = []
    for q in qids:
        vals = [s[q] for s in sp]
        e = env.get(q) or {}
        for key, expv in (("min", min(vals)), ("max", max(vals)), ("central", medians(vals)[0])):
            if e.get(key) is not None and not close(e.get(key), expv, 1e-9):
                bad.append((q, key, e.get(key), expv))
    c.check("F3b numbers, where reported, are over the 5 valid points", not bad, bad[:3])
    c.numbers["F3b_example_Q01"] = env.get(qids[0])
    # F3c: 7 points, point 4 returns NaN for Q17 only
    pts = make_points(7)
    nanq = qids[16]
    fwd = ToyNgc(qids, nan_a=pts[4]["theta_natural"]["a"], nan_query=nanq)
    r = frz.evaluate_envelopes(forward_ngc=fwd, points=pts, query_ids=qids, budget=50)
    pp = r.get("per_point") or []
    env = r.get("envelopes") or {}
    c.check("F3c completes", r.get("status") == "COMPLETE" and fwd.calls == 7, (r.get("status"), fwd.calls, r.get("reasons")))
    c.check("F3c Q17 valid False", (env.get(nanq) or {}).get("valid") is False, env.get(nanq))
    others = [q for q in qids if q != nanq]
    reading = None
    if all((env.get(q) or {}).get("valid") is True for q in others):
        reading = "per-query (other queries valid, 7 points)"
    elif all((env.get(q) or {}).get("valid") is False for q in others):
        reading = "per-point (the NaN point invalidates every query, 6 valid)"
    c.numbers["F3c_reading"] = reading
    c.numbers["F3c_point4"] = next((p for p in pp if p.get("point_index") == 4), None)
    c.check("F3c other queries uniformly valid (per-query reading) or uniformly invalid (per-point reading)", reading is not None, [(q, (env.get(q) or {}).get("valid")) for q in others[:3]])
    sp_all = [fwd.speeds(p["theta_natural"]) for p in pts]
    sp_5 = [s for i, s in enumerate(sp_all) if i != 4]
    bad = []
    for q in others:
        e = env.get(q) or {}
        vals = [s[q] for s in sp_all] if reading and reading.startswith("per-query") else [s[q] for s in sp_5]
        okq = close(e.get("min"), min(vals), 1e-9) and close(e.get("max"), max(vals), 1e-9) and any(close(e.get("central"), m, 1e-9) for m in medians(vals))
        if not okq:
            bad.append((q, e, min(vals), max(vals), medians(vals)))
    c.check("F3c numbers for the other queries match recomputation under the reported reading", reading is not None and not bad, bad[:2])
    e17 = env.get(nanq) or {}
    vals17 = [s[nanq] for s in sp_5]
    c.check("F3c Q17 n_valid == 6 (NaN point excluded)", e17.get("n_valid") == 6 and e17.get("n_points") == 7, e17)
    c.check("F3c Q17 numbers, if reported, are over the 6 finite values", all(e17.get(k) is None or close(e17.get(k), ev, 1e-9) for k, ev in (("min", min(vals17)), ("max", max(vals17)))) and (e17.get("central") is None or any(close(e17.get("central"), m, 1e-9) for m in medians(vals17))), e17)
    ctx["store"]["env_C"] = env
    # F3d: budget exhaustion
    pts = make_points(7)
    fwd = ToyNgc(qids)
    r = frz.evaluate_envelopes(forward_ngc=fwd, points=pts, query_ids=qids, budget=3)
    c.numbers["F3d"] = {"status": r.get("status"), "ok": r.get("ok"), "evaluations_used": r.get("evaluations_used"), "per_point_len": len(r.get("per_point") or []), "log_len": len(r.get("evaluation_log") or []), "toy_calls": fwd.calls}
    c.check("F3d status BUDGET_EXHAUSTED", r.get("status") == "BUDGET_EXHAUSTED", r.get("status"))
    c.check("F3d evaluations_used == 3 == toy calls", r.get("evaluations_used") == 3 == fwd.calls, (r.get("evaluations_used"), fwd.calls))
    c.check("F3d partial results preserved: >=3 per_point entries, 3 log entries, envelopes present", len(r.get("per_point") or []) >= 3 and len(r.get("evaluation_log") or []) == 3 and isinstance(r.get("envelopes"), dict) and len(r["envelopes"]) == 43, None)
    env = r.get("envelopes") or {}
    sp3 = [fwd.speeds(p["theta_natural"]) for p in pts[:3]]
    bad = []
    for q in qids:
        e = env.get(q) or {}
        vals = [s[q] for s in sp3]
        if e.get("min") is not None and not (close(e.get("min"), min(vals), 1e-9) and close(e.get("max"), max(vals), 1e-9)):
            bad.append((q, e))
    c.check("F3d partial min/max (where reported) are over the 3 evaluated points", not bad, bad[:2])
    c.check("F3d per-query n_valid == 3 and valid True ('every evaluated point' rule) for all queries", all((env.get(q) or {}).get("n_valid") == 3 and (env.get(q) or {}).get("valid") is True for q in qids), [(q, env.get(q)) for q in qids[:2]])
    c.numbers["F3d_n_points_reported"] = (env.get(qids[0]) or {}).get("n_points")
    c.note("F3d: under BUDGET_EXHAUSTED the per-query valid flag is True whenever every *evaluated* point was finite (interface wording); callers must gate on status, not on valid")
    ctx["store"]["env_D_partial"] = env
    # bad input: wrong-type forward result
    r = frz.evaluate_envelopes(forward_ngc=lambda th: "nonsense", points=make_points(2), query_ids=qids, budget=5)
    c.check("F3e forward returning a non-dict -> points invalid, no raise", all(p.get("valid") is False for p in (r.get("per_point") or [])) and len(r.get("per_point") or []) == 2, r.get("per_point"))

def build_parameter_region(ctx):
    e1 = ctx["store"].get("E1_run")
    if e1 is not None and e1.get("ok") is True:
        ex = e1["exploration"]
        return {"source": "FIXTURE_E1_SYNTHETIC_TOY", "hull_box": ex.get("hull_box"), "boundary": ex.get("boundary"),
                "unidentified_directions": ex.get("unidentified_directions"), "anchor_u": ex["anchor"]["u"],
                "admitted_count": len(ex.get("admitted_points") or []), "identified": e1["identifiability"].get("identified"),
                "near_null": e1["identifiability"].get("near_null"), "bounds_semantics": BOUNDS_SEMANTICS}
    return {"source": "FIXTURE_SYNTHETIC", "hull_box": {"0": {"min": -0.2, "max": 0.3}}, "bounds_semantics": BOUNDS_SEMANTICS}

def write_manifest(ctx, out_path, env, notes, parameter_region=None, code_files=None, input_files=None):
    frz = ctx["freeze"]
    qids = ctx["store"].get("qids_mod") or ctx["qids"]
    return frz.write_freeze_manifest(
        out_path=out_path,
        parameter_region=parameter_region if parameter_region is not None else build_parameter_region(ctx),
        alternatives={"state": "FIXTURE_SYNTHETIC_STATE", "source": "FIXTURE_SYNTHETIC_SOURCE", "approximation": "FIXTURE_SYNTHETIC_APPROXIMATION"},
        observation_rule=copy.deepcopy(ctx["region_doc"]["statistical_choice"]),
        envelopes=env, query_ids=qids,
        code_files=code_files if code_files is not None else [ctx["engine_path"], ctx["freeze_path"]],
        input_files=input_files if input_files is not None else [REGION_PATH, MANIFEST_PATH],
        notes=notes)

def case_F4(ctx, c):
    qids = ctx["store"].get("qids_mod") or ctx["qids"]
    env = ctx["store"].get("env_A")
    if env is None:
        c.check("F3a envelopes available", False, "F3a did not produce envelopes")
        return
    out = os.path.join(ctx["scratch"], "FREEZE_MANIFEST_FIXTURE_A.json")
    if os.path.exists(out):
        os.remove(out)
    r = write_manifest(ctx, out, env, {"fixture": "F4 synthetic", "detail": {"kind": "toy", "depth": {"ok": True}}})
    c.check("write ok", r.get("ok") is True, r.get("reasons"))
    c.check("path echoed", r.get("path") == out, r.get("path"))
    c.check("file exists", os.path.exists(out))
    if not os.path.exists(out):
        return
    raw = open(out, "rb").read()
    c.check("bytes_written == file size", r.get("bytes_written") == len(raw), (r.get("bytes_written"), len(raw)))
    man = json.loads(raw.decode("utf-8"))
    c.check("file is canonical JSON bytes", cj(man).encode("utf-8") == raw)
    c.check("schema FREEZE_MANIFEST_C3V001", man.get("schema") == "FREEZE_MANIFEST_C3V001", man.get("schema"))
    c.check("units km/s, semantics TOTAL_OBSERVABLE", man.get("units") == "km/s" and man.get("semantics") == "TOTAL_OBSERVABLE", (man.get("units"), man.get("semantics")))
    c.check("target_velocities_included False", man.get("target_velocities_included") is False, man.get("target_velocities_included"))
    c.check("within_error_rule string present", isinstance(man.get("within_error_rule"), str) and "sigma" in man["within_error_rule"], man.get("within_error_rule"))
    c.check("query_ids in manifest order", man.get("query_ids") == qids, None)
    preds = man.get("predictions") or []
    c.check("43 predictions ordered by query_ids", [p.get("id") for p in preds] == qids, [p.get("id") for p in preds][:3])
    bad = []
    for p in preds:
        e = env.get(p.get("id")) or {}
        if not (close(p.get("velocity"), e.get("central"), 0.0) and close(p.get("band_low"), e.get("min"), 0.0) and close(p.get("band_high"), e.get("max"), 0.0)
                and p.get("n_points") == e.get("n_points") and p.get("n_valid") == e.get("n_valid") and p.get("valid") == e.get("valid")):
            bad.append((p, e))
    c.check("prediction fields equal the envelopes (velocity=central, band=min/max, counts, valid)", not bad, bad[:2])
    rec = man.get("manifest_sha256")
    body = {k: v for k, v in man.items() if k != "manifest_sha256"}
    my = sha256_bytes(cj(body).encode("utf-8"))
    c.numbers["manifest_sha256_recorded"] = rec
    c.numbers["manifest_sha256_recomputed"] = my
    c.check("manifest_sha256 == sha256(canonical JSON without that key)", rec == my)
    c.check("returned manifest_sha256 equals recorded", r.get("manifest_sha256") == rec, r.get("manifest_sha256"))
    pins = man.get("pins") or {}
    cf = {p.get("path"): p.get("sha256") for p in pins.get("code_files") or []}
    inf = {p.get("path"): p.get("sha256") for p in pins.get("input_files") or []}
    c.check("code pins hashed from bytes", cf.get(ctx["engine_path"]) == ctx["engine_sha"] and cf.get(ctx["freeze_path"]) == ctx["freeze_sha"], cf)
    c.check("input pins hashed from bytes", inf.get(REGION_PATH) == REGION_SHA and inf.get(MANIFEST_PATH) == MANIFEST_SHA, inf)
    c.check("no forbidden key anywhere in the manifest", not find_forbidden_keys(man), find_forbidden_keys(man))
    c.check("parameter_region, alternatives, observation_rule, notes, created_utc present", all(k in man for k in ("parameter_region", "alternatives", "observation_rule", "notes", "created_utc")), [k for k in ("parameter_region", "alternatives", "observation_rule", "notes", "created_utc") if k not in man])
    ctx["store"]["manifest_A"] = out
    # refuse when out_path exists
    r2 = write_manifest(ctx, out, env, {"fixture": "overwrite attempt"})
    c.check("refuses when out_path exists", r2.get("ok") is False, r2.get("reasons"))
    c.check("existing file untouched", open(out, "rb").read() == raw)
    # forbidden key nested in notes
    out_f = os.path.join(ctx["scratch"], "FREEZE_MANIFEST_FIXTURE_FORBIDDEN.json")
    r3 = write_manifest(ctx, out_f, env, {"fixture": "F4", "detail": {"vobs": [1.0, 2.0]}})
    c.check("refuses forbidden key 'vobs' nested in notes", r3.get("ok") is False, r3.get("reasons"))
    c.check("no file written on refusal", not os.path.exists(out_f))
    out_f2 = os.path.join(ctx["scratch"], "FREEZE_MANIFEST_FIXTURE_FORBIDDEN2.json")
    pr = build_parameter_region(ctx); pr["nested"] = {"deeper": {"Target_Rows": []}}
    r4 = write_manifest(ctx, out_f2, env, {"fixture": "F4"}, parameter_region=pr)
    c.check("refuses forbidden key 'Target_Rows' (case-insensitive) nested in parameter_region", r4.get("ok") is False and not os.path.exists(out_f2), r4.get("reasons"))
    # envelopes not covering exactly query_ids
    env_short = {q: env[q] for q in qids[:-1]}
    out_s = os.path.join(ctx["scratch"], "FREEZE_MANIFEST_FIXTURE_SHORT.json")
    r5 = write_manifest(ctx, out_s, env_short, {"fixture": "F4"})
    c.check("refuses envelopes missing one query", r5.get("ok") is False and not os.path.exists(out_s), r5.get("reasons"))
    env_extra = dict(env); env_extra["NGC3198-Q44"] = env[qids[0]]
    out_x = os.path.join(ctx["scratch"], "FREEZE_MANIFEST_FIXTURE_EXTRA.json")
    r6 = write_manifest(ctx, out_x, env_extra, {"fixture": "F4"})
    c.check("refuses envelopes with an extra query", r6.get("ok") is False and not os.path.exists(out_x), r6.get("reasons"))
    # unreadable listed file
    out_u = os.path.join(ctx["scratch"], "FREEZE_MANIFEST_FIXTURE_UNREADABLE.json")
    r7 = write_manifest(ctx, out_u, env, {"fixture": "F4"}, code_files=[ctx["engine_path"], os.path.join(ctx["scratch"], "no_such_code_file.py")])
    c.check("refuses an unreadable listed code file", r7.get("ok") is False and not os.path.exists(out_u), r7.get("reasons"))
    # observation only: are BUDGET_EXHAUSTED (partial) envelopes accepted by the writer?
    env_d = ctx["store"].get("env_D_partial")
    if env_d is not None:
        out_d = os.path.join(ctx["scratch"], "FREEZE_MANIFEST_FIXTURE_D_PARTIAL.json")
        rd = write_manifest(ctx, out_d, env_d, {"fixture": "F4 partial (budget-exhausted) envelopes"})
        c.numbers["partial_envelopes_manifest_accepted"] = rd.get("ok")
        c.note("observation (not judged): write_freeze_manifest %s a manifest built from BUDGET_EXHAUSTED envelopes (3 of 7 points evaluated, every query valid True); reasons=%s" % ("accepted" if rd.get("ok") is True else "refused", rd.get("reasons")))
    # manifest C (with the invalid Q17 from F3c)
    env_c = ctx["store"].get("env_C")
    if env_c is not None:
        out_c = os.path.join(ctx["scratch"], "FREEZE_MANIFEST_FIXTURE_C.json")
        if os.path.exists(out_c):
            os.remove(out_c)
        rc = write_manifest(ctx, out_c, env_c, {"fixture": "F4 manifest with an invalid query"})
        c.check("manifest with an invalid query (Q17) is writable", rc.get("ok") is True and os.path.exists(out_c), rc.get("reasons"))
        if rc.get("ok") is True:
            mc = json.loads(open(out_c, "rb").read().decode("utf-8"))
            p17 = next((p for p in mc.get("predictions") or [] if p.get("id") == qids[16]), None)
            c.check("manifest C: Q17 prediction carries valid False", p17 is not None and p17.get("valid") is False, p17)
            ctx["store"]["manifest_C"] = out_c
    # manifest P with a scratch input file pinned (for pin tamper in F6)
    pin_file = os.path.join(ctx["scratch"], "pinned_input_fixture.txt")
    with open(pin_file, "wb") as f:
        f.write(b"fixture pinned input v1\n")
    out_p = os.path.join(ctx["scratch"], "FREEZE_MANIFEST_FIXTURE_P.json")
    if os.path.exists(out_p):
        os.remove(out_p)
    rp = write_manifest(ctx, out_p, env, {"fixture": "F4 pin tamper target"}, input_files=[REGION_PATH, MANIFEST_PATH, pin_file])
    c.check("manifest P written with a scratch pinned input", rp.get("ok") is True and os.path.exists(out_p), rp.get("reasons"))
    if rp.get("ok") is True:
        ctx["store"]["manifest_P"] = out_p
        ctx["store"]["pin_file"] = pin_file

def make_targets(man, sigma=2.0):
    """Synthetic target rows in manifest order. Rows 0..19 within sigma, the rest outside; row 30 observed == 0."""
    rows = []
    for k, p in enumerate(man["predictions"]):
        v = p.get("velocity")
        base = float(v) if is_finite_num(v) else 150.0
        if k == 30:
            obs = 0.0
        elif k < 20:
            obs = base + 0.5 * (1 if k % 2 == 0 else -1)
        else:
            obs = base + 3.0 * (1 if k % 2 == 0 else -1)
        rows.append({"id": p["id"], "velocity": obs, "sigma": sigma})
    return rows

def expected_score(man, targets):
    within = 0
    overlap_valid = 0
    overlap_all = 0
    rows = []
    for p, t in zip(man["predictions"], targets):
        valid = p.get("valid") is True
        v = p.get("velocity")
        obs, sig = float(t["velocity"]), float(t["sigma"])
        w = valid and is_finite_num(v) and abs(float(v) - obs) <= sig
        lo, hi = p.get("band_low"), p.get("band_high")
        ov = is_finite_num(lo) and is_finite_num(hi) and float(hi) >= obs - sig and float(lo) <= obs + sig
        within += 1 if w else 0
        overlap_all += 1 if ov else 0
        overlap_valid += 1 if (ov and valid) else 0
        rows.append({"id": p["id"], "within": w, "overlap": ov, "valid": valid})
    return within, overlap_valid, overlap_all, rows

def case_F5(ctx, c):
    frz = ctx["freeze"]
    path = ctx["store"].get("manifest_A")
    if path is None:
        c.check("manifest A available", False, "F4 did not write manifest A")
        return
    man = json.loads(open(path, "rb").read().decode("utf-8"))
    v = frz.verify_freeze_manifest(freeze_manifest_path=path)
    c.check("verify ok on the untouched manifest", v.get("ok") is True, v.get("reasons"))
    c.check("verify: recomputed == recorded == my recomputation", v.get("manifest_sha256_recomputed") == v.get("manifest_sha256_recorded") == man.get("manifest_sha256"), (v.get("manifest_sha256_recomputed"), v.get("manifest_sha256_recorded")))
    pv = v.get("pins_verified") or []
    c.check("verify: 4 pins verified, all ok, recorded == actual", len(pv) == 4 and all(p.get("ok") is True and p.get("recorded") == p.get("actual") for p in pv), pv)
    targets = make_targets(man)
    exp_within, exp_ov_valid, exp_ov_all, exp_rows = expected_score(man, targets)
    s = frz.score_after_freeze(freeze_manifest_path=path, target_rows=targets)
    c.numbers["score_A"] = {k: s.get(k) for k in ("ok", "refused", "within_error_count", "band_overlap_count", "invalid_count", "n_rows", "error_model", "manifest_sha256")}
    c.numbers["expected_A"] = {"within": exp_within, "band_overlap_valid_only": exp_ov_valid, "band_overlap_all": exp_ov_all}
    c.check("score ok, not refused", s.get("ok") is True and s.get("refused") is False, (s.get("ok"), s.get("refused"), s.get("reasons")))
    c.check("n_rows 43 and 43 row entries", s.get("n_rows") == 43 and len(s.get("rows") or []) == 43, (s.get("n_rows"), len(s.get("rows") or [])))
    c.check("error_model string", s.get("error_model") == "CONDITIONAL_QUOTED_SIGMA_DIAGONAL_ONLY", s.get("error_model"))
    c.check("manifest_sha256 reported equals the manifest's", s.get("manifest_sha256") == man.get("manifest_sha256"), s.get("manifest_sha256"))
    c.check("within_error_count == my recomputation (20 within on all-valid manifest)", s.get("within_error_count") == exp_within == 20, (s.get("within_error_count"), exp_within))
    c.check("band_overlap_count reported separately and equals my recomputation", s.get("band_overlap_count") in (exp_ov_valid, exp_ov_all), (s.get("band_overlap_count"), exp_ov_valid, exp_ov_all))
    c.check("invalid_count == 0", s.get("invalid_count") == 0, s.get("invalid_count"))
    fields = ["id", "observed_speed_km_s", "predicted_speed_km_s", "band_low_km_s", "band_high_km_s", "quoted_sigma_km_s",
              "signed_residual_km_s", "sigma_ratio", "fractional_error", "valid", "within_error", "band_overlaps_error_bar"]
    rows = s.get("rows") or []
    missing = [(r.get("id"), f) for r in rows for f in fields if f not in r]
    c.check("per-row: all 12 fields present for all 43 rows", not missing and len(rows) == 43, missing[:5])
    c.check("per-row ids in manifest order", [r.get("id") for r in rows] == man["query_ids"], None)
    bad = []
    for k, (r, t, p, er) in enumerate(zip(rows, targets, man["predictions"], exp_rows)):
        obs = float(t["velocity"]); pred = p["velocity"]
        res = float(pred) - obs
        ok = (close(r.get("observed_speed_km_s"), obs, 0.0) and close(r.get("predicted_speed_km_s"), pred, 0.0)
              and close(r.get("quoted_sigma_km_s"), 2.0, 0.0) and close(r.get("signed_residual_km_s"), res, 1e-9)
              and close(r.get("sigma_ratio"), res / 2.0, 1e-9) and r.get("valid") is True and r.get("within_error") is er["within"]
              and r.get("band_overlaps_error_bar") is er["overlap"] and close(r.get("band_low_km_s"), p["band_low"], 0.0) and close(r.get("band_high_km_s"), p["band_high"], 0.0))
        if k == 30:
            ok = ok and r.get("fractional_error") is None
        else:
            ok = ok and close(r.get("fractional_error"), res / obs, 1e-12)
        if not ok:
            bad.append((k, r, er))
    c.check("per-row numbers: residual, sigma_ratio, fractional_error (None at observed 0), within, overlap all match", not bad, bad[:2])
    # refusals
    t_swap = copy.deepcopy(targets); t_swap[0], t_swap[1] = t_swap[1], t_swap[0]
    s1 = frz.score_after_freeze(freeze_manifest_path=path, target_rows=t_swap)
    c.check("refuses id order mismatch", s1.get("refused") is True and not s1.get("rows"), (s1.get("refused"), s1.get("reasons")))
    t_sig = copy.deepcopy(targets); t_sig[5]["sigma"] = 0.0
    s2 = frz.score_after_freeze(freeze_manifest_path=path, target_rows=t_sig)
    c.check("refuses sigma == 0", s2.get("refused") is True and not s2.get("rows"), (s2.get("refused"), s2.get("reasons")))
    t_neg = copy.deepcopy(targets); t_neg[6]["sigma"] = -1.0
    s2b = frz.score_after_freeze(freeze_manifest_path=path, target_rows=t_neg)
    c.check("refuses sigma < 0", s2b.get("refused") is True, (s2b.get("refused"), s2b.get("reasons")))
    t_nan = copy.deepcopy(targets); t_nan[7]["velocity"] = float("nan")
    s3 = frz.score_after_freeze(freeze_manifest_path=path, target_rows=t_nan)
    c.check("refuses non-finite velocity", s3.get("refused") is True and not s3.get("rows"), (s3.get("refused"), s3.get("reasons")))
    t_inf = copy.deepcopy(targets); t_inf[8]["sigma"] = float("inf")
    s3b = frz.score_after_freeze(freeze_manifest_path=path, target_rows=t_inf)
    c.check("refuses non-finite sigma", s3b.get("refused") is True, (s3b.get("refused"), s3b.get("reasons")))
    s4 = frz.score_after_freeze(freeze_manifest_path=path, target_rows=targets[:42])
    c.check("refuses 42 rows", s4.get("refused") is True, (s4.get("refused"), s4.get("reasons")))
    t_id = copy.deepcopy(targets); t_id[3]["id"] = "NGC3198-Q99"
    s5 = frz.score_after_freeze(freeze_manifest_path=path, target_rows=t_id)
    c.check("refuses a wrong id", s5.get("refused") is True, (s5.get("refused"), s5.get("reasons")))
    s6 = frz.score_after_freeze(freeze_manifest_path=path + ".missing", target_rows=targets)
    c.check("refuses a missing manifest path (no raise)", s6.get("refused") is True or s6.get("ok") is False, (s6.get("refused"), s6.get("ok")))
    # invalid query never within error (manifest C)
    pc = ctx["store"].get("manifest_C")
    if pc is None:
        c.note("manifest C unavailable; invalid-never-within check on manifest C skipped")
        return
    mc = json.loads(open(pc, "rb").read().decode("utf-8"))
    vc = frz.verify_freeze_manifest(freeze_manifest_path=pc)
    c.check("manifest C verifies", vc.get("ok") is True, vc.get("reasons"))
    tc = make_targets(mc)
    k17 = mc["query_ids"].index(ctx["qids"][16])
    p17 = mc["predictions"][k17]
    tc[k17]["velocity"] = float(p17["velocity"]) if is_finite_num(p17.get("velocity")) else 150.0
    tc[k17]["sigma"] = 1.0e6
    exp_w, exp_ov_v, exp_ov_a, exp_rows_c = expected_score(mc, tc)
    sc = frz.score_after_freeze(freeze_manifest_path=pc, target_rows=tc)
    c.numbers["score_C"] = {k: sc.get(k) for k in ("ok", "refused", "within_error_count", "band_overlap_count", "invalid_count", "n_rows")}
    c.numbers["expected_C"] = {"within": exp_w, "band_overlap_valid_only": exp_ov_v, "band_overlap_all": exp_ov_a, "n_invalid_predictions": sum(1 for p in mc["predictions"] if p.get("valid") is not True)}
    c.check("manifest C scored (ok, not refused)", sc.get("ok") is True and sc.get("refused") is False, (sc.get("ok"), sc.get("refused"), sc.get("reasons")))
    rc = sc.get("rows") or []
    r17 = rc[k17] if len(rc) == 43 else None
    c.check("invalid Q17 row: valid False and within_error False although |residual| << sigma", r17 is not None and r17.get("valid") is False and r17.get("within_error") is False, r17)
    c.check("manifest C within_error_count == my recomputation from the manifest's valid flags", sc.get("within_error_count") == exp_w, (sc.get("within_error_count"), exp_w))
    c.check("manifest C invalid_count == number of invalid predictions", sc.get("invalid_count") == c.numbers["expected_C"]["n_invalid_predictions"], sc.get("invalid_count"))
    c.check("manifest C band_overlap_count reported and equals a recomputation", sc.get("band_overlap_count") in (exp_ov_v, exp_ov_a), (sc.get("band_overlap_count"), exp_ov_v, exp_ov_a))
    c.check("manifest C rows: within_error False for every invalid row", all(r.get("within_error") is False for r in rc if r.get("valid") is not True) and len(rc) == 43, None)

def case_F6(ctx, c):
    frz = ctx["freeze"]
    path = ctx["store"].get("manifest_A")
    if path is None:
        c.check("manifest A available", False, "F4 did not write manifest A")
        return
    raw = open(path, "rb").read()
    key = b'"velocity":'
    i = raw.find(key)
    c.check("found a velocity field to tamper", i >= 0, i)
    if i < 0:
        return
    j = i + len(key)
    while j < len(raw) and raw[j:j + 1] in (b" ", b"-"):
        j += 1
    # change the first digit after the decimal point if present, else the first digit
    k = j
    while k < len(raw) and raw[k:k + 1] != b"." and raw[k:k + 1].isdigit():
        k += 1
    pos = k + 1 if raw[k:k + 1] == b"." and raw[k + 1:k + 2].isdigit() else j
    old = raw[pos:pos + 1]
    new = b"4" if old != b"4" else b"5"
    tampered = raw[:pos] + new + raw[pos + 1:]
    tp = os.path.join(ctx["scratch"], "FREEZE_MANIFEST_FIXTURE_A_TAMPERED.json")
    with open(tp, "wb") as f:
        f.write(tampered)
    c.numbers["tamper_byte_offset"] = pos
    c.numbers["tamper_old_new"] = [old.decode(), new.decode()]
    try:
        mt = json.loads(tampered.decode("utf-8"))
        parses = True
    except Exception:
        parses = False
        mt = None
    c.check("tampered copy still parses as JSON (one digit changed)", parses)
    c.check("tampered copy differs from the original in exactly one byte", len(tampered) == len(raw) and sum(1 for x, y in zip(tampered, raw) if x != y) == 1)
    v = frz.verify_freeze_manifest(freeze_manifest_path=tp)
    c.numbers["tampered_verify"] = {k: v.get(k) for k in ("ok", "manifest_sha256_recomputed", "manifest_sha256_recorded")}
    c.check("verify ok False on the tampered copy", v.get("ok") is False, v.get("reasons"))
    c.check("recomputed != recorded", v.get("manifest_sha256_recomputed") != v.get("manifest_sha256_recorded"), None)
    if mt is not None:
        man = json.loads(raw.decode("utf-8"))
        s = frz.score_after_freeze(freeze_manifest_path=tp, target_rows=make_targets(man))
        c.check("score refused True on the tampered copy", s.get("refused") is True, (s.get("refused"), s.get("reasons")))
        c.check("score on the tampered copy returns no rows and no within_error_count", not s.get("rows") and s.get("within_error_count") in (None, 0), (len(s.get("rows") or []), s.get("within_error_count")))
    # pin tamper: the manifest's own hash still verifies but a pinned input changed
    pp = ctx["store"].get("manifest_P")
    pin_file = ctx["store"].get("pin_file")
    if pp and pin_file:
        with open(pin_file, "wb") as f:
            f.write(b"fixture pinned input v2 (tampered)\n")
        v2 = frz.verify_freeze_manifest(freeze_manifest_path=pp)
        pv = v2.get("pins_verified") or []
        bad_pins = [p for p in pv if p.get("ok") is not True]
        c.numbers["pin_tamper_verify"] = {"ok": v2.get("ok"), "bad_pins": bad_pins, "recomputed_eq_recorded": v2.get("manifest_sha256_recomputed") == v2.get("manifest_sha256_recorded")}
        c.check("pin tamper: manifest hash still recomputes equal", v2.get("manifest_sha256_recomputed") == v2.get("manifest_sha256_recorded"))
        c.check("pin tamper: verify ok False with the pinned file flagged", v2.get("ok") is False and len(bad_pins) == 1 and bad_pins[0].get("path") == pin_file, bad_pins)
        man_p = json.loads(open(pp, "rb").read().decode("utf-8"))
        s2 = frz.score_after_freeze(freeze_manifest_path=pp, target_rows=make_targets(man_p))
        c.check("pin tamper: score refused True", s2.get("refused") is True, (s2.get("refused"), s2.get("reasons")))
    else:
        c.note("manifest P unavailable; pin-tamper sub-case skipped")
    # whole-file tamper that keeps canonical form: re-dump with one changed value (hash key untouched)
    man = json.loads(raw.decode("utf-8"))
    man["notes"] = {"fixture": "edited after freeze"}
    tp2 = os.path.join(ctx["scratch"], "FREEZE_MANIFEST_FIXTURE_A_EDITED_NOTES.json")
    with open(tp2, "wb") as f:
        f.write(cj(man).encode("utf-8"))
    v3 = frz.verify_freeze_manifest(freeze_manifest_path=tp2)
    c.check("edited notes (canonical re-dump, old hash kept): verify ok False", v3.get("ok") is False, v3.get("reasons"))
    s3 = frz.score_after_freeze(freeze_manifest_path=tp2, target_rows=make_targets(man))
    c.check("edited notes: score refused True", s3.get("refused") is True, (s3.get("refused"), s3.get("reasons")))

# ----------------------------------------------------------------------------------------------------
# driver
# ----------------------------------------------------------------------------------------------------

def case_X0(ctx, c):
    """Import inertness and static source checks (done after the fixture script was written)."""
    c.check("artifact directory listing unchanged by importing both modules", ctx["snap_before"] == ctx["snap_after"],
            sorted(set(ctx["snap_after"]) ^ set(ctx["snap_before"])))
    c.check("no stdout/stderr output at import", ctx["import_output"] == "", ctx["import_output"][:200])
    for tag, path in (("engine", ctx["engine_path"]), ("freeze", ctx["freeze_path"])):
        src = open(path, "r", encoding="utf-8").read()
        c.check(tag + ": no __main__ block", "__main__" not in src)
        c.check(tag + ": no scipy import", not any(l.strip().startswith(("import scipy", "from scipy")) for l in src.splitlines()))
        c.check(tag + ": no subprocess/threading/multiprocessing/concurrent import",
                not any(("import " + m) in src or ("from " + m) in src for m in ("subprocess", "threading", "multiprocessing", "concurrent")))
        c.check(tag + ": no network/socket import", not any(("import " + m) in src or ("from " + m) in src for m in ("socket", "urllib", "http", "requests")))
    eng, frz = ctx["engine"], ctx["freeze"]
    for name in ("load_observation_region", "make_coordinate_spec", "to_natural", "to_unit", "classify_prediction",
                 "finite_difference_jacobian", "identifiability_report", "explore_region", "run_calibration_region"):
        c.check("engine exposes " + name, callable(getattr(eng, name, None)))
    for name in ("load_query_manifest", "select_representative_points", "evaluate_envelopes", "write_freeze_manifest",
                 "verify_freeze_manifest", "score_after_freeze"):
        c.check("freeze exposes " + name, callable(getattr(frz, name, None)))
    # keyword-only, no defaults: positional call must fail with TypeError
    try:
        eng.load_observation_region(REGION_PATH, REGION_SHA)
        c.check("engine functions are keyword-only (positional call raises TypeError)", False)
    except TypeError:
        c.check("engine functions are keyword-only (positional call raises TypeError)", True)
    except Exception as exc:
        c.check("engine functions are keyword-only (positional call raises TypeError)", False, repr(exc))
    try:
        frz.load_query_manifest(MANIFEST_PATH, MANIFEST_SHA)
        c.check("freeze functions are keyword-only (positional call raises TypeError)", False)
    except TypeError:
        c.check("freeze functions are keyword-only (positional call raises TypeError)", True)
    except Exception as exc:
        c.check("freeze functions are keyword-only (positional call raises TypeError)", False, repr(exc))
    try:
        eng.load_observation_region(path=REGION_PATH)
        c.check("missing keyword argument raises TypeError (no defaults)", False)
    except TypeError:
        c.check("missing keyword argument raises TypeError (no defaults)", True)
    except Exception as exc:
        c.check("missing keyword argument raises TypeError (no defaults)", False, repr(exc))

CASES = [
    ("X0", "import inertness, static source checks, API surface", case_X0),
    ("E0", "engine helpers: spec, to_natural/to_unit, classify_prediction, load_observation_region", case_E0),
    ("E1", "analytic toy: known admitted cross-polytope and exact null direction", case_E1),
    ("E2", "seed not admitted, region nonempty: repair finds an admitted point", case_E2),
    ("E3", "empty region: two rows forced to conflict", case_E3),
    ("E4", "forward failures: exception, NaN row, missing id", case_E4),
    ("E5", "budget exhaustion with partial results preserved", case_E5),
    ("E6", "determinism: identical canonical JSON on repeat", case_E6),
    ("E7", "hash guard: wrong region sha256 -> ok False, no evaluation", case_E7),
    ("F1", "load_query_manifest: real target-free manifest, wrong hash refused", case_F1),
    ("F2", "select_representative_points on a synthetic exploration (and the E1 exploration)", case_F2),
    ("F3", "evaluate_envelopes: all valid, raise, NaN, budget exhaustion", case_F3),
    ("F4", "write_freeze_manifest: content, hash, ordering, refusals", case_F4),
    ("F5", "verify + score: refusals, per-row fields, within-error and band-overlap counts, invalid never within", case_F5),
    ("F6", "tamper detection: one byte flipped, pinned input changed, notes edited", case_F6),
]

def main(argv):
    args = [a for a in argv[1:]]
    results_out = None
    if "--results-out" in args:
        i = args.index("--results-out")
        results_out = args[i + 1]
        del args[i:i + 2]
    if len(args) != 2:
        sys.stderr.write("usage: fixtures_0462_c3v001.py <artifact_dir> <scratch_dir> [--results-out <path>]\n")
        return 2
    artifact_dir, scratch = os.path.abspath(args[0]), os.path.abspath(args[1])
    if os.path.commonpath([scratch, artifact_dir]) == artifact_dir:
        sys.stderr.write("refusing: scratch directory must not lie inside the artifact directory\n")
        return 2
    os.makedirs(scratch, exist_ok=True)
    engine_path = os.path.join(artifact_dir, ENGINE_FILE)
    freeze_path = os.path.join(artifact_dir, FREEZE_FILE)
    for p in (engine_path, freeze_path):
        if not os.path.exists(p):
            sys.stderr.write("missing module: %s\n" % p)
            return 3
    engine_sha, freeze_sha = sha256_file(engine_path), sha256_file(freeze_path)
    snap_before = snapshot_dir(artifact_dir)
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        engine = load_module("calibration_region_engine_c3v001", engine_path)
        freeze = load_module("prediction_freeze_c3v001", freeze_path)
    snap_after = snapshot_dir(artifact_dir)
    rows, region_doc = read_region_rows()
    qids, radii, rad_unit = read_manifest_ids()
    ctx = {"engine": engine, "freeze": freeze, "engine_path": engine_path, "freeze_path": freeze_path,
           "engine_sha": engine_sha, "freeze_sha": freeze_sha, "scratch": scratch, "rows": rows, "region_doc": region_doc,
           "z": float(region_doc["statistical_choice"]["marginal_quantile"]), "qids": qids, "store": {},
           "snap_before": snap_before, "snap_after": snap_after, "import_output": buf.getvalue()}
    results = []
    for cid, name, fn in CASES:
        c = Case(cid, name)
        try:
            fn(ctx, c)
        except Exception:
            c.error = traceback.format_exc()
        results.append(c.as_dict())
        print("%-3s %-5s %3d checks %2d failed  %s" % (cid, c.status(), len(c.checks), sum(1 for k in c.checks if not k["ok"]), name))
        for k in c.checks:
            if not k["ok"]:
                print("      FAILED: %s -> %s" % (k["label"], str(k.get("detail"))[:400]))
        if c.error:
            print("      ERROR: " + c.error.strip().splitlines()[-1])
    summary = {s: sum(1 for r in results if r["status"] == s) for s in ("PASS", "FAIL", "ERROR", "SKIP")}
    out = {"schema": "FIXTURE_RESULTS_0462_V001",
           "fixture_script": {"path": os.path.abspath(__file__), "sha256": sha256_file(os.path.abspath(__file__))},
           "modules": {"engine": {"path": engine_path, "sha256": engine_sha}, "freeze": {"path": freeze_path, "sha256": freeze_sha}},
           "inputs": {"region": {"path": REGION_PATH, "sha256": REGION_SHA}, "query_manifest": {"path": MANIFEST_PATH, "sha256": MANIFEST_SHA}},
           "runtime": {"python": sys.version.split()[0], "numpy": np.__version__, "threads_env": {k: os.environ.get(k) for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")}},
           "artifact_dir_listing_changed_by_import": snap_before != snap_after,
           "scratch_dir": scratch, "cases": results, "summary": summary,
           "ngc3198_target_velocities_read": False, "project_runs": 0}
    text = json.dumps(out, indent=1, sort_keys=True, allow_nan=False, default=lambda o: (o.tolist() if hasattr(o, "tolist") else str(o)))
    if results_out:
        with open(results_out, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        print("results written: %s (sha256 %s)" % (results_out, sha256_bytes((text + "\n").encode("utf-8"))))
    else:
        p = os.path.join(scratch, "FIXTURE_RESULTS_0462_V001.json")
        with open(p, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        print("results written: %s" % p)
    print("summary: %s" % json.dumps(summary, sort_keys=True))
    return 0 if summary["FAIL"] == 0 and summary["ERROR"] == 0 else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv))

"""M2 implementation fixtures for whole-path residence transports (0457 Claude4 review, helper M2).

(a) Birth CONTROL: runs the pinned reviewed Birth transport (SHA256 6f866bda...) through the same
    harness to validate it before the author module exists.
(b) ADMISSION catalogue: any module exposing move(run, path, rng, diag, sampler, owner_roster),
    loaded by path (never edited), against the synthetic double M2_sampler_double_v001.py and its
    raw-physics oracle; includes an exact detailed-balance enumeration (black-box kernel).
(c) Mutants of a TEST-ONLY transcription of the 0456 contract formula (not a deliverable
    implementation; independent of the author code) to show the harness detects each defect.
Synthetic tiny states only: no project sampler, no L4/production run, no project arrays, no target
data. Single thread. Import of this file loads only the double.

CLI (python = .../codex-primary-runtime/dependencies/python/bin/python3 -I -B):
  M2_fixtures_v001.py --birth-control --reference --mutants --out M2_results_birth_control_v001.json
  M2_fixtures_v001.py --module PATH [--expect-sha SHA256] --out JSON   # admission catalogue on PATH
"""
import argparse
import ast
import copy
import hashlib
import importlib.util
import json
import math
import platform
import re
import sys
import time
import traceback
from pathlib import Path

sys.dont_write_bytecode = True

import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
DOUBLE_PATH = HERE / "M2_sampler_double_v001.py"
BIRTH_PATH = Path("/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/"
                  "FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/coefficient_method/"
                  "owned_worldline_birth_residence_transport_v001.py")
BIRTH_SHA = "6f866bda7eda7b56cb9ae7a1247cb365c16c9b40cb996af650452f8823f9f6e8"


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


D = load_module(DOUBLE_PATH, "m2_sampler_double_v001")

BETA = 1.3
T2 = (0.41, 0.97)
T4 = (0.21, 0.52, 0.77, 1.09)

_AMP = {"kappa": {"A0": 0.7, "A1": 1.3, "B0": 0.9, "A0.n": 1.1},
        "g": {"A0": 0.6, "A1": 0.8, "B0": 1.2, "A0.n": 0.5},
        "t": {0: 0.9, 1: 1.1, 2: 0.7, 3: 0.6}, "h": {0: 0.4, 1: 0.5, 2: 0.45, 3: 0.3},
        "eps": {"A0": 0.8}}
_ENERGY = {"p": {"A0": 0.3, "A1": -0.2, "B0": 0.15, "A0.n": 0.1},
           "q": {"A0": 0.25, "A1": 0.1, "B0": -0.05, "A0.n": 0.2},
           "s": {"A0": -0.4, "A1": 0.35, "B0": 0.2, "A0.n": -0.1},
           "U": 0.45, "slot": 0.6, "inc": {0: 0.12, 1: -0.08, 2: 0.05, 3: 0.07}}
_MULT = {"flip_s": 0.3, "hop_a": 0.3, "hop_s": 0.2, "bind_a": 0.5, "bind_s": 0.25,
         "adm_a": 0.4, "adm_s": 0.3, "birth_a": 0.35}
_SRC = {"N_adm": 0.17, "N_part": -0.11}

SPEC_MAIN = dict(originals=("A0", "A1", "B0"),
                 births={"A0": {"cuts": [0, 2], "newborn": "A0.n", "newborn_edge": 3}},
                 edges=[("A0", "A1"), ("A1", "B0"), ("A0", "B0"), ("A0", "A0.n")],
                 amp=_AMP, energy=_ENERGY, sources=_SRC, mult=_MULT, adm_cap=2)
SPEC_DB3 = dict(originals=("A0", "A1", "B0"), edges=[("A0", "A1")], hop_edges=[0], flip_edges=[0],
                bind_vertices=["B0"], admission_vertices=["A0", "A1", "B0"],
                amp=_AMP, energy=_ENERGY, sources=_SRC, mult=_MULT, adm_cap=2)
SPEC_DBL = dict(originals=("A0", "B0"), edges=[], hop_edges=[], flip_edges=[], bind_vertices=["B0"],
                admission_vertices=["A0", "B0"], amp=_AMP, energy=_ENERGY, sources=_SRC, mult=_MULT,
                adm_cap=None, variants={"ladder": True})
SPEC_DBB = dict(originals=("A0", "A1", "B0"),
                births={"A0": {"cuts": [0, 1], "newborn": "A0.n", "newborn_edge": 2}},
                edges=[("A0", "A1"), ("A0", "B0"), ("A0", "A0.n")], hop_edges=[], flip_edges=[0, 1, 2],
                bind_vertices=[], admission_vertices=["A1"],
                amp={**_AMP, "h": {0: 0.4, 1: 0.45, 2: 0.3}}, energy={**_ENERGY, "inc": {0: 0.12, 1: 0.05, 2: 0.07}},
                sources=_SRC, mult=_MULT, adm_cap=2)
SPECS = {"MAIN": SPEC_MAIN, "DB3": SPEC_DB3, "DBL": SPEC_DBL, "DBB": SPEC_DBB}
_MODELS = {}


def model(name, **variants):
    key = (name, tuple(sorted((k, repr(v)) for k, v in variants.items())))
    if key not in _MODELS:
        spec = copy.deepcopy(SPECS[name])
        spec["variants"] = {**spec.get("variants", {}), **variants}
        _MODELS[key] = D.ToyModel(spec)
    return _MODELS[key]


def ADM(lab):
    return ("admission", ("vertex", lab))


def BIND(lab):
    return ("bind", ("vertex", lab))


def EOWN(kind, m, c):
    return (kind, ("edge", m.edges[c]))


def BOWN(m, o, c):
    return ("birth", o, (m.edges[c],))


# ----------------------------------------------------------------------------------------------
# Subjects
# ----------------------------------------------------------------------------------------------


class Subject:
    def __init__(self, name, move, rule, roster=("A0", "A1", "B0"), path=None):
        self.name, self.move, self.rule, self.roster, self.path = name, move, rule, roster, path


def birth_subject():
    sha = sha256_file(BIRTH_PATH)
    if sha != BIRTH_SHA:
        raise SystemExit(f"pinned Birth transport hash mismatch: {sha}")
    mod = load_module(BIRTH_PATH, "pinned_birth_residence_transport_v001")
    return Subject("pinned_birth_v001", mod.move, "birth", path=str(BIRTH_PATH))


def ref_admission_move(run, path, rng, diag, sampler, owner_roster, _mut=frozenset()):
    """TEST-ONLY transcription of the 0456 contract on the pinned Birth scaffold (not a deliverable;
    written from 0456 and the Birth reference, independent of the author module). `_mut` injects
    one named defect for mutation testing."""
    pre = "admission_residence_"

    def tick(name):
        diag[pre + name] = diag.get(pre + name, 0) + 1

    def fail(message):
        raise sampler._Stop("failed", run["stage"], message)

    def reject(reason):
        tick(reason)
        tick("rejected")
        return path, "rejected"

    def mark(state, kind, owner):
        sampler._budget_check(run, "before", "admission residence marked enumeration")
        groups = sampler._record_groups(run, kind, owner)
        cs, _ = sampler._palette_channels(run, state, groups)
        return sampler._unique_mark(run, cs, kind, owner, "admission residence replay")

    def own(v):
        return ("vertex", v) if "bare_owner" in _mut else ("admission", ("vertex", v))

    def roster(state, v):
        sampler._budget_check(run, "before", "admission residence vertex enumeration")
        if v not in run["group"]:
            fail("Unknown permanent vertex label")
        cs, _ = sampler._palette_channels(run, state, frozenset((run["group"][v],)))
        o = own(v)
        sel = [ch for ch in cs if ch["kind"] in ("admit", "admit_rev") and sampler._keys_equal(run, ch["owner"], o)]
        for ch in sel:
            sampler._unique_mark(run, sel, ch["kind"], ch["owner"], "admission residence roster")
        return sel

    sampler._budget_check(run, "before", "admission residence proposal")
    if not isinstance(owner_roster, tuple) or not owner_roster or len(set(owner_roster)) != len(owner_roster):
        fail("Freeze unique permanent original-vertex tuple before measurement")
    segs, events, times = path["segments"], path["events"], path["times"]
    k = len(events)
    if len(times) != k or len(segs) != k + 1:
        fail("Malformed closed path")
    if k > run["caps"]["max_events_per_path"]:
        raise sampler._Stop("incomplete", run["stage"], "Existing path exceeds event cap")
    sampler._check_times(run, times, run["beta"])
    if not sampler._keys_equal(run, segs[0]["key"], segs[-1]["key"]):
        fail("Original path not closed")
    tick("attempts")
    if "eligible_roster" in _mut:
        elig = [v for v in owner_roster if roster(segs[0]["state"], v)]
        if not elig:
            return reject("empty_reference_owner")
        v = elig[int(rng.integers(0, len(elig)))]
    else:
        v = owner_roster[int(rng.integers(0, len(owner_roster)))]
    old_roster = roster(segs[0]["state"], v)
    if not old_roster and "resample_empty" in _mut:
        for _ in range(2 * len(owner_roster)):
            v = owner_roster[int(rng.integers(0, len(owner_roster)))]
            old_roster = roster(segs[0]["state"], v)
            if old_roster:
                break
    if not old_roster:
        return reject("empty_reference_owner")
    chosen = old_roster[int(rng.integers(0, len(old_roster)))]
    kind, owner = chosen["kind"], chosen["owner"]
    inverse_kind = "admit_rev" if kind == "admit" else "admit"
    tick(kind + "_selected")
    transformed = []
    for i, old in enumerate(segs):
        if "ref_dwell_only" in _mut and 0 < i < len(segs) - 1:
            transformed.append(old)
            continue
        ch = mark(old["state"], kind, owner)
        if ch is None:
            return reject("dwell_guard")
        new = sampler._segment_core(run, ch["target"])
        if "stale_reads" in _mut:
            new = dict(new, row=old["row"], Da=old["Da"])
        back = mark(new["state"], inverse_kind, owner)
        if back is None:
            return reject("inverse_guard")
        if "no_target_check" not in _mut and not sampler._keys_equal(run, sampler._target_key(run, back), old["key"]):
            return reject("inverse_canonical_target")
        transformed.append(new)
    if not sampler._keys_equal(run, transformed[0]["key"], transformed[-1]["key"]):
        fail("Transformed path not closed")
    new_roster = roster(transformed[0]["state"], v)
    reverse = sampler._unique_mark(run, new_roster, inverse_kind, owner, "admission residence reverse selection")
    if reverse is None or ("no_target_check" not in _mut and not sampler._keys_equal(
            run, sampler._target_key(run, reverse), segs[0]["key"])):
        return reject("reverse_selection")
    ends = [0.0] + list(times) + [run["beta"]]
    nf, nr = len(old_roster), len(new_roster)
    terms = [math.log(nr) - math.log(nf)] if "count_inverted" in _mut else [math.log(nf) - math.log(nr)]
    sgn = 1.0 if "D_sign" in _mut else -1.0
    for i, (old, new) in enumerate(zip(segs, transformed)):
        if "wrap_dwell_omitted" in _mut and i == len(segs) - 1:
            continue
        dt = run["beta"] / len(segs) if "uniform_dt" in _mut else ends[i + 1] - ends[i]
        terms.append(sgn * dt * (new["D"] - old["D"]))
    new_events = []
    for i, ev in enumerate(events):
        before = mark(segs[i]["state"], ev["kind"], ev["owner"])
        if before is None or not sampler._keys_equal(run, sampler._target_key(run, before), segs[i + 1]["key"]) \
                or before["W"] != ev["W"]:
            fail("Stored primitive mark/rate inconsistent")
        after = mark(transformed[i]["state"], ev["kind"], ev["owner"])
        if after is None or not sampler._keys_equal(run, sampler._target_key(run, after), transformed[i + 1]["key"]):
            return reject("event_replay")
        if "W_omitted" not in _mut:
            terms.append(math.log(after["W"]) - math.log(before["W"]))
        new_events.append(sampler._event_from_channel(run, after))
    if "extra_amplitude" in _mut:
        terms.append(math.log(chosen["W"]))
    if "extra_time_density" in _mut:
        terms.append(math.log(run["beta"]))
    logratio = math.fsum(terms)
    if not math.isfinite(logratio):
        fail("Nonfinite admission residence MH ratio")
    tick("legal_transport")
    diag[pre + "last_proposal"] = dict(kind=kind, vertex=v, forward_count=nf, reverse_count=nr,
                                       log_mh_ratio=logratio)
    if logratio < 0 and not float(rng.random()) < math.exp(logratio):
        return reject("metropolis")
    delta = [math.fsum((ends[i + 1] - ends[i]) * (float(new["row"][j]) - float(old["row"][j]))
                       for i, (old, new) in enumerate(zip(segs, transformed)))
             for j in range(len(segs[0]["row"]))]
    if not all(math.isfinite(x) for x in delta):
        fail("Nonfinite read change")

    def accumulate():
        net = diag.setdefault(pre + "read_integral_change_sum", [0.0] * len(delta))
        absolute = diag.setdefault(pre + "absolute_read_integral_change_sum", [0.0] * len(delta))
        for j, x in enumerate(delta):
            net[j] += x
            absolute[j] += abs(x)
        tick("accepted_changed")
        tick(kind + "_accepted_changed")

    if "diag_before_commit" in _mut:
        accumulate()
        sampler._budget_check(run, "before", "admission residence atomic commit")
    else:
        sampler._budget_check(run, "before", "admission residence atomic commit")
        accumulate()
    if "inplace_commit" in _mut:
        path["segments"][:] = transformed
        path["events"][:] = new_events
        return path, "changed"
    return {"segments": transformed, "events": new_events, "times": list(times)}, "changed"


MUTANTS = {
    "D_sign": "sign of the D-integral term flipped",
    "count_inverted": "count ratio inverted (log N_rev - log N_fwd)",
    "W_omitted": "event W ratio omitted",
    "extra_amplitude": "extra admission amplitude factor log W(chosen mark)",
    "extra_time_density": "extra time-density/event-insertion factor log beta",
    "no_target_check": "inverse/reverse target-key checks removed (non-inverse accepted)",
    "ref_dwell_only": "only reference (and wrap) dwell transformed; interior dwells copied",
    "eligible_roster": "vertex drawn only among currently eligible vertices",
    "resample_empty": "empty owner resampled instead of self-loop",
    "bare_owner": "roster filtered on bare ('vertex', v) owner (inert-move failure mode)",
    "stale_reads": "transformed segment keeps old row/Da (not source-dependent)",
    "diag_before_commit": "accepted diagnostics mutated before final commit budget check",
    "inplace_commit": "accepted proposal written into the input path in place",
    "wrap_dwell_omitted": "D integral omits the wrap dwell [t_k, beta) (rooted time coordinates misused)",
    "uniform_dt": "D integral uses beta/(k+1) per dwell instead of actual rooted dwell lengths",
}


def ref_subject(mut=None):
    muts = frozenset() if mut is None else frozenset((mut,))

    def mv(run, path, rng, diag, sampler, owner_roster):
        return ref_admission_move(run, path, rng, diag, sampler, owner_roster, _mut=muts)
    return Subject("reference_transcription" if mut is None else "mutant:" + mut, mv, "admission")


# ----------------------------------------------------------------------------------------------
# Invocation and checks
# ----------------------------------------------------------------------------------------------


def invoke(subject, m, path_factory, ints=(), reals=(), hook=None, caps=None, diag=None, rng=None,
           roster=None, beta=BETA, run_mutator=None):
    run = D.make_run(m, beta=beta)
    sampler = D.make_sampler()
    path = path_factory(run, sampler)
    if run_mutator is not None:
        run_mutator(run)
    run["budget_log"] = []
    base = run["counters"]["channel_enumerations"]
    if caps is not None:
        run["caps"].update(caps(base) if callable(caps) else caps)
    run["budget_hook"] = hook
    diag = {} if diag is None else diag
    snap = copy.deepcopy(path)
    ids = D.path_ids(path)
    diag0 = copy.deepcopy(diag)
    api0 = dict(vars(sampler))
    rng = D.ScriptedRNG(ints, reals) if rng is None else rng
    roster = subject.roster if roster is None else roster
    res = {"outcome": None, "ret_path": None, "exc_type": None, "status": None, "message": None}
    try:
        ret = subject.move(run, path, rng, diag, sampler, roster)
        if isinstance(ret, tuple) and len(ret) == 2 and ret[1] in ("changed", "rejected"):
            res["outcome"], res["ret_path"] = ret[1], ret[0]
        else:
            res["outcome"], res["message"] = "bad_return", repr(ret)[:200]
    except D._Stop as exc:
        res.update(outcome="stop", exc_type=type(exc).__name__, status=exc.status, message=str(exc.message)[:300])
    except D.RNGExhausted as exc:
        res.update(outcome="rng_script_mismatch", message=repr(exc.args)[:200])
    except Exception as exc:  # noqa: BLE001 - recorded, never swallowed silently
        res.update(outcome="error", exc_type=type(exc).__name__, message=str(exc)[:300])
    ok, where = D.deep_equal(path, snap)
    api1 = vars(sampler)
    res.update(input_unchanged=ok, input_diff=where, ids_unchanged=D.path_ids(path) == ids,
               sampler_unpatched=set(api1) == set(api0) and all(api1[k] is api0[k] for k in api0),
               rng_log=list(rng.log), budget_log=list(run["budget_log"]),
               enumerations=run["counters"]["channel_enumerations"] - base,
               diag=diag, diag0=diag0, path=path, snap=snap, run=run)
    return res


def pf_build(xs0, evs, times, share_wrap=False, mutate=None):
    def f(run, sampler):
        p = D.build_path(run, sampler, xs0, evs, times, share_wrap=share_wrap)
        if mutate is not None:
            mutate(p, run, sampler)
        return p
    return f


def pf_copy(path):
    return lambda run, sampler: copy.deepcopy(path)


def ostr(res):
    return " ".join(str(x) for x in (res["outcome"], res["exc_type"], res["status"], res["message"]) if x)


def _jsonable(x, depth=0):
    if depth > 14:
        return repr(x)[:200]
    if x is None or isinstance(x, (bool, int, str)):
        return x
    if isinstance(x, float):
        return x if math.isfinite(x) else repr(x)
    if isinstance(x, np.integer):
        return int(x)
    if isinstance(x, np.floating):
        return _jsonable(float(x))
    if isinstance(x, np.ndarray):
        return [_jsonable(v, depth + 1) for v in x.tolist()]
    if isinstance(x, dict):
        return {(k if isinstance(k, str) else repr(k)): _jsonable(v, depth + 1) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v, depth + 1) for v in x]
    if isinstance(x, (set, frozenset)):
        return sorted(repr(v) for v in x)
    return repr(x)[:300]


class Fx:
    def __init__(self, fid, title, category="required"):
        self.fid, self.title, self.category = fid, title, category
        self.checks, self.notes = [], []

    def check(self, name, ok, detail=None):
        self.checks.append({"name": name, "ok": bool(ok), "detail": _jsonable(detail)})
        return bool(ok)

    def note(self, s):
        self.notes.append(_jsonable(s))

    def result(self):
        passed = None if self.category == "info" else all(c["ok"] for c in self.checks)
        return {"id": self.fid, "title": self.title, "category": self.category, "passed": passed,
                "failed_checks": [c for c in self.checks if not c["ok"]],
                "n_checks": len(self.checks), "checks": self.checks, "notes": self.notes}


_LOGMH_KEY = re.compile(r"(log.*(mh|ratio|metropolis))|(mh.*ratio)", re.I)
_ACCEPT_KEY = re.compile(r"accept|changed|commit|integral", re.I)


def _walk(d, prefix=""):
    if isinstance(d, dict):
        for k, v in d.items():
            yield from _walk(v, f"{prefix}.{k}" if prefix else str(k))
    else:
        yield prefix, d


def find_logmh(diag, diag0):
    before = dict(_walk(diag0))
    cands = [(k, v) for k, v in _walk(diag) if isinstance(v, (int, float)) and not isinstance(v, bool)
             and _LOGMH_KEY.search(k.split(".")[-1] if "." in k else k) and before.get(k) != v]
    if len(cands) == 1:
        return float(cands[0][1])
    return None


def diag_changes(diag, diag0):
    before = dict(_walk(diag0))
    out = []
    for k, v in _walk(diag):
        if k not in before:
            out.append(k)
        else:
            ok, _ = D.deep_equal(v, before[k]) if type(v) is type(before[k]) else (False, None)
            if not ok:
                out.append(k)
    return out


def common(fx, res, tag=""):
    fx.check(tag + "input_path_unchanged", res["input_unchanged"], res["input_diff"])
    fx.check(tag + "input_object_ids_unchanged", res["ids_unchanged"])
    fx.check(tag + "sampler_not_patched", res["sampler_unpatched"])


def int_draws(res):
    return [e for e in res["rng_log"] if e[0] in ("integers", "choice")]


def check_draws(fx, res, n_roster, nf, tag=""):
    d = int_draws(res)
    fx.check(tag + "first_draw_uniform_over_full_frozen_roster", bool(d) and d[0][1] == 0 and d[0][2] == n_roster, d[:4])
    if nf is not None:
        if len(d) >= 2:
            fx.check(tag + "mark_draw_uniform_over_actual_marks_at_vertex", d[1][1] == 0 and d[1][2] == nf, d[:4])
        else:
            fx.check(tag + "mark_draw_skipped_only_if_single_mark", nf == 1, d)


def expected_path(m, ys0, evs, times):
    run = D.make_run(m)
    return D.build_path(run, D.make_sampler(), ys0, evs, times)


def expect_changed(fx, m, res, oracle, evs, times, tag=""):
    fx.check(tag + "outcome_changed", res["outcome"] == "changed", ostr(res))
    common(fx, res, tag)
    if res["outcome"] != "changed":
        return None
    newp = res["ret_path"]
    if not fx.check(tag + "returns_new_path_dict", isinstance(newp, dict) and newp is not res["path"]
                    and {"segments", "events", "times"} <= set(newp)):
        return None
    fx.check(tag + "times_new_list_equal_values", type(newp["times"]) is list and newp["times"] is not res["path"]["times"]
             and newp["times"] == list(res["snap"]["times"]), newp["times"])
    fx.check(tag + "event_count_preserved", len(newp["events"]) == len(res["snap"]["events"]))
    fx.check(tag + "segment_count_preserved", len(newp["segments"]) == len(res["snap"]["segments"]))
    fx.check(tag + "no_input_segment_or_event_object_reused",
             not any(s is t for s in newp["segments"] for t in res["path"]["segments"])
             and not any(e is f for e in newp["events"] for f in res["path"]["events"]))
    fx.check(tag + "proposal_states_equal_oracle", D.path_states(m, newp) == tuple(oracle["ys"]),
             {"module": D.path_states(m, newp), "oracle": oracle["ys"]})
    exp = expected_path(m, oracle["ys"][0], evs, times)
    ok, where = D.deep_equal(newp["segments"], exp["segments"])
    fx.check(tag + "segments_equal_actual_segment_core_of_transformed_states", ok, where)
    ok, where = D.deep_equal(newp["events"], exp["events"])
    fx.check(tag + "events_equal_event_from_channel_of_replayed_marks", ok, where)
    fx.check(tag + "replayed_event_kind_owner_preserved",
             [(e["kind"], e["owner"]) for e in newp["events"]] == [(e["kind"], e["owner"]) for e in res["snap"]["events"]])
    fx.check(tag + "replayed_W_equal_oracle", [e["W"] for e in newp["events"]] == oracle["new_w"],
             {"module": [e["W"] for e in newp["events"]], "oracle": oracle["new_w"]})
    return newp


def expect_rejected(fx, res, tag=""):
    fx.check(tag + "outcome_rejected_selfloop", res["outcome"] == "rejected", ostr(res))
    common(fx, res, tag)
    if res["outcome"] == "rejected":
        rp = res["ret_path"]
        ok, where = D.deep_equal(rp, res["snap"]) if isinstance(rp, dict) else (False, "not a dict")
        fx.check(tag + "returned_path_equals_input", ok, where)
        fx.note(f"{tag}returns_input_object={rp is res['path']}; uniform_drawn={any(e[0] == 'random' for e in res['rng_log'])}; "
                f"diag_changes={diag_changes(res['diag'], res['diag0'])}")


def expect_stop(fx, res, statuses=("failed",), tag=""):
    fx.check(tag + "raises_Stop_" + "/".join(statuses), res["outcome"] == "stop" and res["status"] in statuses, ostr(res))
    common(fx, res, tag)


def check_logmh(fx, subject, m, pf, vidx, midx, L, res_forced, tag=""):
    Ld = find_logmh(res_forced["diag"], res_forced["diag0"])
    if Ld is not None:
        fx.check(tag + "diag_logmh_equals_oracle", abs(Ld - L) <= 1e-12 * (1.0 + abs(L)), {"diag": Ld, "oracle": L})
    else:
        fx.note(tag + "no unambiguous diag log-MH entry; black-box acceptance bracketing only")
    if L < 0:
        th = math.exp(L)
        r_in = invoke(subject, m, pf, ints=[vidx, midx], reals=[th * (1 - 1e-9)])
        fx.check(tag + "accepts_u_just_below_exp_oracle_logmh", r_in["outcome"] == "changed", ostr(r_in))
        u_out = th * (1 + 1e-9)
        if u_out < 1.0:
            r_out = invoke(subject, m, pf, ints=[vidx, midx], reals=[u_out])
            fx.check(tag + "rejects_u_just_above_exp_oracle_logmh", r_out["outcome"] == "rejected", ostr(r_out))
            common(fx, r_out, tag + "metropolis_reject:")
    else:
        r_hi = invoke(subject, m, pf, ints=[vidx, midx], reals=[1.0 - 1e-12])
        fx.check(tag + "accepts_u_near_one_when_oracle_logmh_nonnegative", r_hi["outcome"] == "changed", ostr(r_hi))
    return Ld


def legal_case(fx, subject, m, xs0, evs, times, label, midx, tag="", share_wrap=False):
    xs = _states_of(m, xs0, evs)
    o = D.oracle_transport(m, BETA, xs, evs, times, subject.rule, label, midx)
    if not fx.check(tag + "fixture_valid_oracle_legal", o["status"] == "legal", o["status"]):
        return o, None, None
    fx.check(tag + "oracle_difference_form_equals_path_weight_form",
             abs(o["logmh"] - o["logmh_pi_form"]) <= 1e-12 * (1 + abs(o["logmh"])), [o["logmh"], o["logmh_pi_form"]])
    fx.note({tag + "oracle": {k: o[k] for k in ("logmh", "nf", "nr", "count_term", "d_term", "w_term")}})
    vidx = subject.roster.index(label)
    pf = pf_build(xs0, evs, times, share_wrap=share_wrap)
    res = invoke(subject, m, pf, ints=[vidx, midx], reals=[0.0])
    newp = expect_changed(fx, m, res, o, evs, times, tag)
    check_draws(fx, res, len(subject.roster), o["nf"], tag)
    Ld = check_logmh(fx, subject, m, pf, vidx, midx, o["logmh"], res, tag)
    return o, newp, Ld


def selfloop_case(fx, subject, m, xs0, evs, times, label, midx, reason, tag=""):
    xs = _states_of(m, xs0, evs)
    o = D.oracle_transport(m, BETA, xs, evs, times, subject.rule, label, midx)
    fx.check(tag + "fixture_valid_oracle_" + reason, o["status"] == reason, o["status"])
    vidx = subject.roster.index(label)
    res = invoke(subject, m, pf_build(xs0, evs, times), ints=[vidx, midx], reals=[0.0])
    expect_rejected(fx, res, tag)
    return res


def _states_of(m, x0, evs):
    xs = [x0]
    for kind, owner in evs:
        xs.append(D.raw_marks(m, xs[-1])[(kind, owner)][0])
    if xs[-1] != x0:
        raise ValueError("fixture path not closed")
    return xs


def composition_case(fx, subject, m, xs0, evs, times, label, midx, tag="", share_wrap=False):
    o, newp, Lf = legal_case(fx, subject, m, xs0, evs, times, label, midx, tag + "fwd:", share_wrap)
    if newp is None:
        return
    inv = D.INVERSE[o["kind"]]
    r1 = D.ROSTER_RULES[subject.rule](m, o["ys"][0], label)
    ridx = r1.index((inv, o["owner"]))
    xs = _states_of(m, xs0, evs)
    orev = D.oracle_transport(m, BETA, o["ys"], evs, times, subject.rule, label, ridx)
    fx.check(tag + "oracle_reverse_legal_and_reciprocal", orev["status"] == "legal"
             and orev["ys"] == xs and abs(orev["logmh"] + o["logmh"]) <= 1e-12 * (1 + abs(o["logmh"])),
             [orev.get("status"), orev.get("logmh"), o["logmh"]])
    vidx = subject.roster.index(label)
    pf = pf_copy(newp)
    res = invoke(subject, m, pf, ints=[vidx, ridx], reals=[0.0])
    fx.check(tag + "rev:outcome_changed", res["outcome"] == "changed", ostr(res))
    common(fx, res, tag + "rev:")
    if res["outcome"] == "changed":
        orig = D.build_path(D.make_run(m), D.make_sampler(), xs0, evs, times)
        ok, where = D.deep_equal(res["ret_path"], orig)
        fx.check(tag + "forward_then_reverse_returns_original_path_exactly", ok, where)
        Lr = find_logmh(res["diag"], res["diag0"])
        if Lf is not None and Lr is not None:
            fx.check(tag + "diag_logmh_reciprocal", abs(Lf + Lr) <= 1e-12 * (1 + abs(Lf)), [Lf, Lr])
    check_draws(fx, res, len(subject.roster), orev.get("nf"), tag + "rev:")
    check_logmh(fx, subject, m, pf, vidx, ridx, orev["logmh"], res, tag + "rev:")


def budget_sweep(fx, subject, m, pf, ints, reals, tag="", expect_final=None):
    base = invoke(subject, m, pf, ints=ints, reals=reals, hook=D.CountingHook(None))
    n = base["run"]["counters"]["budget_checks"]
    fx.note({tag + "baseline_outcome": base["outcome"], tag + "budget_checkpoints": n,
             tag + "last_checkpoint": base["budget_log"][-1] if base["budget_log"] else None})
    if expect_final is not None:
        fx.check(tag + "baseline_outcome_" + expect_final, base["outcome"] == expect_final, ostr(base))
    fx.check(tag + "has_budget_checkpoints", n > 0, n)
    flagged = []
    for t in range(1, n + 1):
        r = invoke(subject, m, pf, ints=ints, reals=reals, hook=D.CountingHook(t))
        ok = r["outcome"] == "stop" and r["exc_type"] == "_BudgetStop" and r["status"] == "incomplete"
        fx.check(f"{tag}interrupt@{t}:{r['budget_log'][-1] if r['budget_log'] else '?'}:BudgetStop_propagated", ok, ostr(r))
        common(fx, r, f"{tag}interrupt@{t}:")
        acc = [k for k in diag_changes(r["diag"], r["diag0"]) if _ACCEPT_KEY.search(k)]
        if acc:
            flagged.append((t, r["budget_log"][-1] if r["budget_log"] else None, acc))
    return base, flagged


def enum_sweep(fx, subject, m, pf, ints, reals, tag=""):
    base = invoke(subject, m, pf, ints=ints, reals=reals)
    e = base["enumerations"]
    fx.check(tag + "has_enumerations", e > 0, e)
    for t in range(e):
        r = invoke(subject, m, pf, ints=ints, reals=reals, caps=lambda b, t=t: {"max_channel_enumerations": b + t})
        fx.check(f"{tag}enumcap@{t}:Stop_incomplete", r["outcome"] == "stop" and r["status"] == "incomplete", ostr(r))
        common(fx, r, f"{tag}enumcap@{t}:")


# ----------------------------------------------------------------------------------------------
# Exact detailed balance (black-box kernel) on enumerable doubles
# ----------------------------------------------------------------------------------------------


def enumerate_paths(m, with_k2=True):
    out = []
    for x in m.all_states():
        out.append(((x,), (), ()))
        if with_k2:
            for (k1, o1, y, _w) in D.raw_marks_ordered(m, x):
                for (k2, o2, z, _w2) in D.raw_marks_ordered(m, y):
                    if z == x:
                        out.append(((x, y, x), ((k1, o1), (k2, o2)), T2))
    return out


def psig(m, path):
    return (D.path_states(m, path), tuple((e["kind"], e["owner"]) for e in path["events"]))


def oracle_kernel(m, paths, roster, rule):
    K, legal = {}, {}
    for xs, evs, times in paths:
        row, lm = {}, {}
        for lab in roster:
            r0 = D.ROSTER_RULES[rule](m, xs[0], lab)
            for j in range(len(r0)):
                o = D.oracle_transport(m, BETA, list(xs), list(evs), times, rule, lab, j)
                if o["status"] != "legal":
                    continue
                ys = (tuple(o["ys"]), tuple(evs))
                row[ys] = row.get(ys, 0.0) + (1.0 / len(roster)) * (1.0 / len(r0)) * math.exp(min(o["logmh"], 0.0))
                lm[ys] = o["logmh"]
        K[(tuple(xs), tuple(evs))] = row
        legal[(tuple(xs), tuple(evs))] = lm
    return K, legal


def module_kernel(subject, m, paths, roster, legal_hint, full_bisect=False):
    K, stats = {}, {"runs": 0, "errors": [], "leaves": 0, "need_u": 0, "bracket_confirmed": 0, "bisected": 0}
    for xs, evs, times in paths:
        sx = (tuple(xs), tuple(evs))
        pf = pf_build(xs[0], list(evs), times)
        row, stack = {}, [((), 1.0)]
        while stack:
            prefix, prob = stack.pop()
            stats["runs"] += 1
            try:
                res = invoke(subject, m, pf, rng=D.ScriptedRNG(prefix, (), branch=True), roster=roster)
            except D.NeedBranch as nb:
                if len(prefix) >= 4:
                    stats["errors"].append((sx, prefix, "more than 4 integer draws in one move (DFS depth cap)"))
                    continue
                for v in range(nb.low, nb.high):
                    stack.append((prefix + (v,), prob / (nb.high - nb.low)))
                continue
            except D.NeedU:
                stats["need_u"] += 1
                theta, ys, how = _threshold(subject, m, pf, prefix, roster, legal_hint.get(sx, {}), full_bisect, stats)
                if ys is not None and theta > 0.0:
                    row[ys] = row.get(ys, 0.0) + prob * theta
                stats["leaves"] += 1
                continue
            stats["leaves"] += 1
            if res["outcome"] == "changed":
                ys = psig(m, res["ret_path"])
                row[ys] = row.get(ys, 0.0) + prob
            elif res["outcome"] != "rejected":
                stats["errors"].append((sx, prefix, ostr(res)))
            if not (res["input_unchanged"] and res["ids_unchanged"]):
                stats["errors"].append((sx, prefix, "input mutated"))
        K[sx] = row
    return K, stats


def _threshold(subject, m, pf, prefix, roster, hints, full_bisect, stats):
    def run_u(u):
        stats["runs"] += 1
        return invoke(subject, m, pf, rng=D.ScriptedRNG(prefix, (u,), branch=True), roster=roster)

    try:
        r = run_u(1.0 - 2.0 ** -53)
        if r["outcome"] == "changed":
            return 1.0, psig(m, r["ret_path"]), "u~1"
        r = run_u(5e-324)
        if r["outcome"] != "changed":
            return 0.0, None, "never"
        ys = psig(m, r["ret_path"])
        if not full_bisect and ys in hints and hints[ys] < 0:
            th = math.exp(hints[ys])
            a = run_u(th * (1 - 1e-10))
            b = run_u(th * (1 + 1e-10)) if th * (1 + 1e-10) < 1 else None
            if a["outcome"] == "changed" and (b is None or b["outcome"] == "rejected"):
                stats["bracket_confirmed"] += 1
                return th, ys, "bracket"
        stats["bisected"] += 1
        lo, hi = -745.0, math.log1p(-2.0 ** -53)
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            r = run_u(math.exp(mid))
            if r["outcome"] == "changed":
                lo = mid
            else:
                hi = mid
        return math.exp(0.5 * (lo + hi)), ys, "bisect"
    except (D.NeedBranch, D.NeedU):
        stats["errors"].append(("unexpected draw after uniform", prefix))
        return 0.0, None, "error"


def db_check(m, K, logpi, tol=1e-9):
    viol, pairs = [], 0
    for sx, row in K.items():
        for sy, kxy in row.items():
            if sy == sx:
                continue
            if sy not in K:
                viol.append(("escape_outside_enumerated_space", sx, sy))
                continue
            kyx = K[sy].get(sx, 0.0)
            pairs += 1
            if kyx == 0.0:
                viol.append(("no_reverse_transition", sx, sy, kxy))
                continue
            d = (logpi[sx] + math.log(kxy)) - (logpi[sy] + math.log(kyx))
            if abs(d) > tol:
                viol.append(("imbalance", sx, sy, d))
    return pairs, viol


def kernel_compare(Kmod, Kor, tol=1e-9):
    bad = []
    for sx in Kor:
        a, b = Kmod.get(sx, {}), Kor[sx]
        for sy in set(a) | set(b):
            if sy == sx:
                continue
            x, y = a.get(sy, 0.0), b.get(sy, 0.0)
            if abs(x - y) > tol * max(abs(y), 1e-300) and not (x == 0.0 and y == 0.0):
                bad.append((sx, sy, x, y))
    return bad


def db_fixture(fx, subject, spec_name, roster, full_bisect=False, with_k2=True, **variants):
    m = model(spec_name, **variants)
    paths = enumerate_paths(m, with_k2)
    logpi = {(tuple(xs), tuple(evs)): D.oracle_log_pi(m, BETA, list(xs), list(evs), times) for xs, evs, times in paths}
    Kor, legal = oracle_kernel(m, paths, roster, subject.rule)
    p_or, v_or = db_check(m, Kor, logpi)
    fx.check("oracle_kernel_satisfies_detailed_balance", not v_or, {"pairs": p_or, "violations": v_or[:3]})
    t0 = time.perf_counter()
    Kmod, stats = module_kernel(subject, m, paths, roster, legal, full_bisect=full_bisect)
    p_mod, v_mod = db_check(m, Kmod, logpi)
    bad = kernel_compare(Kmod, Kor)
    fx.check("module_run_errors_none", not stats["errors"], stats["errors"][:3])
    fx.check("module_kernel_satisfies_detailed_balance", not v_mod,
             {"pairs": p_mod, "n_violations": len(v_mod), "examples": v_mod[:3]})
    fx.check("module_kernel_equals_oracle_kernel", not bad, {"n_mismatch": len(bad), "examples": bad[:3]})
    nonzero = sum(1 for sx, row in Kmod.items() for sy in row if sy != sx)
    fx.check("module_kernel_nontrivial", nonzero > 0, nonzero)
    fx.note({"double": spec_name, "variants": variants, "paths": len(paths), "states": len(m.all_states()),
             "oracle_pairs": p_or, "module_pairs": p_mod, "nonzero_offdiag_entries": nonzero,
             "stats": {k: v for k, v in stats.items() if k != "errors"},
             "kernel_seconds": round(time.perf_counter() - t0, 2), "full_bisect": full_bisect})


# ----------------------------------------------------------------------------------------------
# Static checks
# ----------------------------------------------------------------------------------------------


def static_checks(path):
    src = Path(path).read_text()
    tree = ast.parse(src)
    out = {"top_level_non_definition": [], "imports": [], "hardcoded_state_key_index_reads": [],
           "bit_count_uses": [], "owner_tuple_index_reads": [], "sampler_attribute_writes": [],
           "global_statements": [], "move_signature": None}
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            out["imports"].append(ast.unparse(node))
            continue
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            if isinstance(node, ast.FunctionDef) and node.name == "move":
                out["move_signature"] = [a.arg for a in node.args.args]
            continue
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            continue
        if isinstance(node, (ast.Assign, ast.AnnAssign)) and node.value is not None and _const_expr(node.value):
            continue
        if isinstance(node, ast.If) and "__name__" in ast.unparse(node.test):
            continue
        out["top_level_non_definition"].append((node.lineno, type(node).__name__))
    for node in ast.walk(tree):
        if isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Constant) \
                and isinstance(node.slice.value, int) and not isinstance(node.slice.value, bool):
            inner = node.value
            if isinstance(inner, ast.Subscript) and isinstance(inner.slice, ast.Constant):
                if inner.slice.value in ("key", "state", "target"):
                    out["hardcoded_state_key_index_reads"].append((node.lineno, ast.unparse(node)))
                elif inner.slice.value == "owner":
                    out["owner_tuple_index_reads"].append((node.lineno, ast.unparse(node)))
            elif isinstance(inner, ast.Name) and inner.id in ("key", "state", "x", "y", "old_key", "new_key"):
                out["hardcoded_state_key_index_reads"].append((node.lineno, ast.unparse(node)))
        if isinstance(node, ast.Attribute) and node.attr == "bit_count":
            out["bit_count_uses"].append((node.lineno, ast.unparse(node)))
        if isinstance(node, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for tg in targets:
                for sub in ast.walk(tg):
                    if isinstance(sub, ast.Attribute) and isinstance(sub.value, ast.Name) and sub.value.id == "sampler":
                        out["sampler_attribute_writes"].append((node.lineno, ast.unparse(tg)))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ("setattr", "delattr") \
                and node.args and isinstance(node.args[0], ast.Name) and node.args[0].id == "sampler":
            out["sampler_attribute_writes"].append((node.lineno, ast.unparse(node)))
        if isinstance(node, (ast.Global, ast.Nonlocal)):
            out["global_statements"].append((node.lineno, ast.unparse(node)))
    return out


def _const_expr(node):
    try:
        ast.literal_eval(node)
        return True
    except Exception:
        pass
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
            and node.func.id in ("frozenset", "tuple", "set", "dict", "list") and not node.keywords:
        return all(_const_expr(a) for a in node.args)
    return isinstance(node, (ast.Constant, ast.Name, ast.Attribute))


def static_fixture(fx, path, expect_clean=True):
    s = static_checks(path)
    fx.check("move_signature", s["move_signature"] == ["run", "path", "rng", "diag", "sampler", "owner_roster"],
             s["move_signature"])
    fx.check("import_inert_top_level", not s["top_level_non_definition"], s["top_level_non_definition"])
    fx.check("no_project_imports", not any(re.search(r"owned_|pairallk|importlib|sampler", i) for i in s["imports"]),
             s["imports"])
    clean = not s["hardcoded_state_key_index_reads"] and not s["bit_count_uses"]
    if expect_clean:
        fx.check("no_hardcoded_state_or_key_tuple_index_reads", clean,
                 {"index_reads": s["hardcoded_state_key_index_reads"], "bit_count": s["bit_count_uses"]})
    else:
        fx.check("detector_positive_control_flags_known_key_index_read", not clean,
                 {"index_reads": s["hardcoded_state_key_index_reads"], "bit_count": s["bit_count_uses"]})
    fx.check("no_sampler_attribute_writes", not s["sampler_attribute_writes"], s["sampler_attribute_writes"])
    fx.check("no_global_statements", not s["global_statements"], s["global_statements"])
    fx.note({"owner_tuple_index_reads(info)": s["owner_tuple_index_reads"], "imports": s["imports"]})


# ----------------------------------------------------------------------------------------------
# Fixture runner (per-fixture isolation: a harness exception is a recorded failed check)
# ----------------------------------------------------------------------------------------------


def run_fixtures(builders):
    out = []
    for fid, title, cat, fn in builders:
        fx = Fx(fid, title, cat)
        t0 = time.perf_counter()
        try:
            fn(fx)
        except Exception as exc:  # noqa: BLE001
            fx.check("fixture_completed_without_exception", False,
                     f"{type(exc).__name__}: {exc} | {traceback.format_exc()[-1500:]}")
        fx.note({"seconds": round(time.perf_counter() - t0, 3)})
        out.append(fx.result())
    return out


# ----------------------------------------------------------------------------------------------
# Admission catalogue
# ----------------------------------------------------------------------------------------------


def admission_catalogue(subject, with_db=True, quick=False):
    S = subject
    m = model("MAIN")
    st = m.make_state
    x_b0 = st(inc={0, 1, 2}, p={"B0"}, s={"B0"})
    k4 = (st(inc={0, 1, 2}, p={"B0"}),
          [("admit", ADM("A0")), ("bind", BIND("B0")), ("admit_rev", ADM("A0")), ("bind", BIND("B0"))], T4)
    k2b = (x_b0, [("bind", BIND("B0")), ("bind", BIND("B0"))], T2)

    def a01(fx):
        o, _, _ = legal_case(fx, S, m, x_b0, [], (), "A1", 0)
        fx.check("fixture_sensitivity_pure_diagonal", o.get("w_term") == 0.0 and o.get("count_term") == 0.0
                 and o.get("d_term", 0.0) != 0.0, o.get("d_term"))

    def a02(fx):
        legal_case(fx, S, m, st(inc={0, 1, 2}, p={"A1", "B0"}, s={"A1", "B0"}), [], (), "A1", 0)

    def a03(fx):
        composition_case(fx, S, m, x_b0, [], (), "A1", 0)

    def a04(fx):
        composition_case(fx, S, m, k4[0], k4[1], k4[2], "A1", 0)
        xs = _states_of(m, k4[0], k4[1])
        o = D.oracle_transport(m, BETA, xs, k4[1], k4[2], "admission", "A1", 0)
        fx.check("fixture_sensitivity_w_term_nonzero_and_dD_nonuniform", o["w_term"] != 0.0
                 and len({D.D_raw(m, y) - D.D_raw(m, x) for x, y in zip(xs, o["ys"])}) > 1, o["w_term"])

    def a05(fx):
        composition_case(fx, S, m, st(inc={0, 1, 2}),
                         [("birth", BOWN(m, "A0", 0)), ("birth_rev", BOWN(m, "A0", 0))], T2, "B0", 0)

    def a06(fx):
        selfloop_case(fx, S, m, st(inc={0, 1, 2}), [("admit", ADM("A1")), ("admit_rev", ADM("A1"))], T2,
                      "A1", 0, "dwell_guard")

    def a07(fx):
        selfloop_case(fx, S, m, st(inc={0, 1, 2}, p={"A0"}),
                      [("hop", EOWN("hop", m, 0)), ("hop", EOWN("hop", m, 0))], T2, "A1", 0, "dwell_guard")

    def a08(fx):
        selfloop_case(fx, S, m, x_b0, [("admit", ADM("A0")), ("admit_rev", ADM("A0"))], T2, "A1", 0, "dwell_guard")

    def a09(fx):
        selfloop_case(fx, S, m, st(inc={0, 1, 2}, p={"A1"}, s={"A1"}),
                      [("bind", BIND("A1")), ("bind", BIND("A1"))], T2, "A1", 0, "event_replay")

    def a10(fx):
        selfloop_case(fx, S, m, x_b0, [("flip", EOWN("flip", m, 0)), ("flip", EOWN("flip", m, 0))], T2,
                      "A1", 0, "event_replay")

    def a11(fx):
        mv = model("MAIN", admit_rev_resets_edge=1)
        selfloop_case(fx, S, mv, mv.make_state(inc={0, 2}),
                      [("flip", EOWN("flip", mv, 1)), ("flip", EOWN("flip", mv, 1))], T2, "A1", 0,
                      "inverse_canonical_target", tag="interior:")
        selfloop_case(fx, S, mv, mv.make_state(inc={0, 1, 2}), [], (), "A1", 0, "inverse_canonical_target",
                      tag="reference:")

    def a12(fx):
        r = selfloop_case(fx, S, m, st(inc={0, 1, 2}, p={"A1"}), [], (), "A1", 0, "empty_reference_owner")
        fx.check("exactly_one_integer_draw_no_resampling", len(int_draws(r)) == 1 and int_draws(r)[0][2] == 3,
                 r["rng_log"])
        fx.note({"uniform_drawn_on_empty_owner": any(e[0] == "random" for e in r["rng_log"])})

    def a13(fx):
        r = selfloop_case(fx, S, m, st(inc={0, 1, 2}, p={"A0", "B0"}, s={"A0", "B0"}), [], (), "A1", 0,
                          "empty_reference_owner")
        fx.check("exactly_one_integer_draw_no_resampling", len(int_draws(r)) == 1, r["rng_log"])

    def a14(fx):
        x14 = st(slots=(1,), inc={1, 2})
        fx.check("fixture_valid_group_palette_has_two_admission_marks",
                 len([1 for (k, o_, _t, _w) in D.raw_marks_ordered(m, x14)
                      if k == "admit" and m.group[o_[1][1]] == "A0"]) == 2)
        legal_case(fx, S, m, x14, [], (), "A0", 0)

    def a15(fx):
        ml = model("MAIN", ladder=True)
        composition_case(fx, S, ml, ml.make_state(inc={0, 1, 2}), [], (), "A1", 0, tag="lvl0->1:")
        composition_case(fx, S, ml, ml.make_state(inc={0, 1, 2}, p={"A1"}, s={"A1"}), [], (), "A1", 0,
                         tag="lvl1->2:")
        legal_case(fx, S, ml, ml.make_state(inc={0, 1, 2}, p={"A1", "B0"}, s={"A1", "B0"}), [], (), "A1", 1,
                   tag="lvl1->0:")

    def a16(fx):
        expect_stop(fx, invoke(S, model("MAIN", nonfinite_D_when_A=2), pf_build(x_b0, [], ()), ints=[1, 0], reals=[0.0]))

    def a17(fx):
        expect_stop(fx, invoke(S, model("MAIN", nonfinite_W=("bind", 2)), pf_build(*k2b), ints=[1, 0], reals=[0.0]))

    def a18(fx):
        expect_stop(fx, invoke(S, model("MAIN", huge_D_when_A={1: -1e308, 2: 1e308}), pf_build(x_b0, [], ()),
                               ints=[1, 0], reals=[0.0]))

    def a18i(fx):
        mh = D.ToyModel({**copy.deepcopy(SPEC_MAIN), "adm_cap": None,
                         "variants": {"huge_D_when_A": {1: -1e308, 2: 1e308, 3: -1e308}}})
        r = invoke(S, mh, pf_build(x_b0, [("admit", ADM("A0")), ("admit_rev", ADM("A0"))], T2), ints=[1, 0], reals=[0.0])
        fx.note({"outcome": ostr(r), "input_unchanged": r["input_unchanged"]})

    def a19(fx):
        expect_stop(fx, invoke(S, model("MAIN", read_fail_when_A=2), pf_build(x_b0, [], ()), ints=[1, 0], reals=[0.0]))

    flagged_all = {}

    def a20(fx):
        _, f1 = budget_sweep(fx, S, m, pf_build(*k4), [1, 0], [0.0], tag="accept:", expect_final="changed")
        _, f2 = budget_sweep(fx, S, m, pf_build(st(inc={0, 1, 2}, p={"A1"}, s={"A1"}),
                                                [("bind", BIND("A1")), ("bind", BIND("A1"))], T2),
                             [1, 0], [0.0], tag="replayfail:", expect_final="rejected")
        _, f3 = budget_sweep(fx, S, m, pf_build(st(inc={0, 1, 2}, p={"A1"}), [], ()), [1, 0], [0.0], tag="empty:",
                             expect_final="rejected")
        flagged_all["v"] = f1 + f2 + f3

    def a20d(fx):
        if "v" not in flagged_all:
            _, f1 = budget_sweep(Fx("tmp", ""), S, m, pf_build(*k4), [1, 0], [0.0])
            flagged_all["v"] = f1
        fx.check("no_accepted_type_diagnostic_mutated_under_any_interruption", not flagged_all["v"], flagged_all["v"])

    def a21(fx):
        enum_sweep(fx, S, m, pf_build(*k4), [1, 0], [0.0])

    def a22(fx):
        expect_stop(fx, invoke(S, m, pf_build(*k4), ints=[1, 0], reals=[0.0], caps={"max_events_per_path": 3}),
                    ("incomplete",), tag="event_cap:")

        def drop_time(p, run, s):
            p["times"] = p["times"][:-1]

        def unclose(p, run, s):
            p["segments"][-1] = s._segment_core(run, p["segments"][1]["state"])

        def swap_times(p, run, s):
            p["times"] = [p["times"][1], p["times"][0]]
        expect_stop(fx, invoke(S, m, pf_build(*k2b, mutate=drop_time), ints=[1, 0], reals=[0.0]), tag="times_len:")
        expect_stop(fx, invoke(S, m, pf_build(*k2b, mutate=unclose), ints=[1, 0], reals=[0.0]), tag="not_closed:")
        expect_stop(fx, invoke(S, m, pf_build(*k2b, mutate=swap_times), ints=[1, 0], reals=[0.0]), tag="times_order:")
        expect_stop(fx, invoke(S, m, pf_build(x_b0, [], ()), ints=[0, 0], reals=[0.0], roster=("Z9",)),
                    tag="unknown_label:")

    def a22r(fx):
        for tg, ros in (("list:", ["A0", "A1", "B0"]), ("empty:", ()), ("duplicate:", ("A0", "A1", "A1"))):
            expect_stop(fx, invoke(S, m, pf_build(x_b0, [], ()), ints=[1, 0], reals=[0.0], roster=ros), tag=tg)

    def a23(fx):
        def tamper_w(p, run, s):
            p["events"][1] = dict(p["events"][1], W=p["events"][1]["W"] * (1 + 1e-12))

        def tamper_owner(p, run, s):
            p["events"][1] = dict(p["events"][1], owner=BIND("A1"))  # no bind mark at A1 (p=0): missing

        def tamper_target(p, run, s):
            p["events"][1] = dict(p["events"][1], kind="flip", owner=EOWN("flip", m, 2))
        for tg, fn in (("W:", tamper_w), ("owner:", tamper_owner), ("target:", tamper_target)):
            expect_stop(fx, invoke(S, m, pf_build(*k4, mutate=fn), ints=[1, 0], reals=[0.0]), tag=tg)

    def a24(fx):
        composition_case(fx, S, m, k4[0], k4[1], k4[2], "A1", 0, share_wrap=True)

    def a25(fx):
        mo = model("MAIN", opaque=True)
        legal_case(fx, S, mo, x_b0, [], (), "A1", 0, tag="k0:")
        composition_case(fx, S, mo, k4[0], k4[1], k4[2], "A1", 0, tag="k4:")

    def a26(fx):
        expect_stop(fx, invoke(S, model("MAIN", dup_admission="A1"), pf_build(x_b0, [], ()), ints=[1, 0], reals=[0.0]))

    def a27(fx):
        n_ok = n_tot = 0
        for p_, s_ in ((set(), set()), ({"B0"}, {"B0"}), ({"A0"}, {"A0"}), ({"A0", "A1"}, {"A0", "A1"}),
                       ({"B0"}, set())):
            x = st(inc={0, 1, 2}, p=p_, s=s_)
            for lab in S.roster:
                if not D.roster_admission(m, x, lab):
                    continue
                o = D.oracle_transport(m, BETA, [x], [], (), "admission", lab, 0)
                if o["status"] == "legal":
                    n_tot += 1
                    u = 0.5 * math.exp(min(o["logmh"], 0.0))
                    r = invoke(S, m, pf_build(x, [], ()), ints=[S.roster.index(lab), 0], reals=[u])
                    n_ok += r["outcome"] == "changed"
        fx.check("all_legal_proposals_with_u_below_threshold_change", n_tot > 0 and n_ok == n_tot, [n_ok, n_tot])
        m3 = model("DB3")
        run = D.make_run(m3)
        sam = D.make_sampler()
        path = D.build_path(run, sam, m3.make_state(inc={0}), [], [])
        rng = np.random.default_rng(20261016)
        changed, dg, err = 0, {}, None
        try:
            for _ in range(300):
                path, oc = S.move(run, path, rng, dg, sam, ("A0", "A1", "B0"))
                changed += oc == "changed"
        except Exception as exc:  # noqa: BLE001
            err = f"{type(exc).__name__}: {exc}"
        fx.check("numpy_rng_chain_300_moves_runs_and_changes_sometimes", err is None and changed > 0, [changed, err])
        fx.note({"chain_changed_fraction": changed / 300.0})

    def a28(fx):
        diagnostics_fixture(fx, S, m, x_b0, k4)

    def a33i(fx):
        def nogroup(run):
            run["group"] = None
        probes = {}
        r = invoke(S, m, pf_build(x_b0, [], ()), ints=[1, 0], reals=[0.0], run_mutator=nogroup)
        probes["run_group_None"] = [ostr(r), r["input_unchanged"]]
        r = invoke(S, m, pf_build(x_b0, [], ()), ints=[1, 0], reals=[0.0], roster=("A0", "A1", "A0.n"))
        probes["newborn_label_in_roster_unchosen"] = [ostr(r), r["input_unchanged"]]
        dg = {"admission_residence_read_integral_change_sum": [0.0] * 3,
              "admission_residence_absolute_read_integral_change_sum": [0.0] * 3}
        r = invoke(S, m, pf_build(x_b0, [], ()), ints=[1, 0], reals=[0.0], diag=dg)
        probes["preexisting_wrong_length_read_sums"] = [ostr(r), r["input_unchanged"],
                                                        "diag_changes=%s" % diag_changes(r["diag"], r["diag0"])]
        r = invoke(S, model("MAIN", admission_family={"A1": "adm"}), pf_build(x_b0, [], ()), ints=[1, 0], reals=[0.0])
        probes["non_V003_admission_owner_family_at_chosen_vertex"] = [ostr(r), r["input_unchanged"]]
        fx.note(probes)

    builders = [
        ("A01", "zero-event admit: exact diagonal ratio, draws, logMH vs oracle", "required", a01),
        ("A02", "zero-event admit_rev: logMH >= 0 branch", "required", a02),
        ("A03", "composition zero-event: exact return, reciprocal logMH", "required", a03),
        ("A04", "composition nonempty k=4: per-dwell D varies, admission+bind W change", "required", a04),
        ("A05", "nonempty k=2 Birth/birth_rev events replayed under admission", "required", a05),
        ("A06", "dwell guard: admission events at v mid-path", "required", a06),
        ("A07", "dwell guard: hop makes v (1,0) mid-path", "required", a07),
        ("A08", "dwell guard: zero multiplier (cap) removes mark in one dwell", "required", a08),
        ("A09", "replay impossible: bind at v after admit_rev", "required", a09),
        ("A10", "replay impossible: flip multiplier becomes 0", "required", a10),
        ("A11", "inverse-canonical mismatch (defect-injected double)", "required", a11),
        ("A12", "empty owner (1,0): self-loop, one draw, no resampling", "required", a12),
        ("A13", "empty owner by zero multiplier: self-loop, one draw", "required", a13),
        ("A14", "roster = exact owner ('admission',('vertex',v)); same-group newborn mark excluded", "contract", a14),
        ("A15", "roster factors N_fwd != N_rev (ladder-extended double)", "required", a15),
        ("A16", "nonfinite D at transformed state -> hard failure", "required", a16),
        ("A17", "nonfinite W on transformed states -> hard failure", "required", a17),
        ("A18", "finite D with overflowing difference -> module finite check", "required", a18),
        ("A18i", "INFO: opposite-sign overflowing terms (fsum inf-inf)", "info", a18i),
        ("A19", "source/read failure at transformed state -> hard failure", "required", a19),
        ("A20", "budget interruption at every checkpoint: path atomic", "required", a20),
        ("A20d", "budget interruption: no accepted-type diagnostic mutated (diagnostic atomicity)", "contract", a20d),
        ("A21", "enumeration-cap interruption at every enumeration", "required", a21),
        ("A22", "event cap / malformed path / unknown label -> Stop", "template", a22),
        ("A22r", "owner_roster must be a frozen unique nonempty tuple", "required", a22r),
        ("A23", "stored-event inconsistency (W, owner, target) -> hard failure", "template", a23),
        ("A24", "rotated path (shared first/wrap segment): composition exact", "required", a24),
        ("A25", "opaque state/key objects: no hard-coded tuple reads", "required", a25),
        ("A26", "duplicate admission mark (ambiguous) -> hard failure", "required", a26),
        ("A27", "sampler-level owner format: legal proposals change (inert detector)", "required", a27),
        ("A28", "diagnostics: counters + read-integral change equal oracle", "contract", a28),
        ("A33i", "INFO probes: group None, newborn label in roster, wrong-length read sums, non-V003 owner family",
         "info", a33i),
    ]
    if S.path is not None:
        builders.append(("A29", "static AST checks", "required", lambda fx: static_fixture(fx, S.path, True)))
    if with_db:
        builders += [
            ("A30", "exact DB + kernel == oracle on DB3 (3 vertices, cap, hop/flip/bind)", "required",
             lambda fx: db_fixture(fx, S, "DB3", ("A0", "A1", "B0"))),
            ("A31", "exact DB + kernel == oracle on DBL (ladder: N_fwd != N_rev)", "required",
             lambda fx: db_fixture(fx, S, "DBL", ("A0", "B0"), full_bisect=not quick)),
            ("A32", "exact DB on defect-injected DB3 (admit_rev not an exact inverse): guards keep DB", "required",
             lambda fx: db_fixture(fx, S, "DB3", ("A0", "A1", "B0"), admit_rev_resets_edge=0)),
        ]
    return run_fixtures(builders)


def diagnostics_fixture(fx, S, m, x_b0, k4):
    dg = {}
    seq = [(x_b0, [], (), "A1", "changed"), (m.make_state(inc={0, 1, 2}, p={"A1"}), [], (), "A1", "rejected"),
           (k4[0], k4[1], k4[2], "A1", "changed")]
    net = np.zeros(len(D.READ_LABELS))
    absolute = np.zeros(len(D.READ_LABELS))
    for x0, evs, times, lab, want in seq:
        r = invoke(S, m, pf_build(x0, evs, times), ints=[S.roster.index(lab), 0], reals=[0.0], diag=dg)
        fx.check(f"sequence_outcome_{want}", r["outcome"] == want, ostr(r))
        if want == "changed":
            xs = _states_of(m, x0, evs)
            o = D.oracle_transport(m, BETA, xs, evs, times, "admission", lab, 0)
            ends = [0.0] + list(times) + [BETA]
            dv = np.array([math.fsum((ends[i + 1] - ends[i]) * (m.reads(y)[lb] - m.reads(x)[lb])
                                     for i, (x, y) in enumerate(zip(xs, o["ys"]))) for lb in D.READ_LABELS])
            net += dv
            absolute += np.abs(dv)
    keys = [k for k, _ in _walk(dg)]
    fx.check("has_selection_or_attempt_counter", any(re.search(r"select|chosen|propos|attempt", k, re.I) for k in keys), keys)
    fx.check("has_rejection_or_selfloop_counter", any(re.search(r"reject|self.?loop", k, re.I) for k in keys), keys)
    fx.check("has_accepted_counter", any(re.search(r"accept|changed", k, re.I) for k in keys), keys)
    vec = [(k, v) for k, v in _walk(dg) if isinstance(v, (list, tuple, np.ndarray)) and len(v) == len(D.READ_LABELS)]
    fx.check("net_read_integral_change_matches_oracle",
             any(np.allclose(np.asarray(v, float), net, rtol=0, atol=1e-12) for _, v in vec),
             {"oracle": net, "diag_vectors": vec})
    fx.check("absolute_read_integral_change_matches_oracle",
             any(np.allclose(np.asarray(v, float), absolute, rtol=0, atol=1e-12) for _, v in vec), {"oracle": absolute})
    fx.note({"diag_keys": keys})


# ----------------------------------------------------------------------------------------------
# Birth control (pinned reviewed module)
# ----------------------------------------------------------------------------------------------


def birth_control(S, with_db=True):
    m = model("MAIN")
    st = m.make_state
    x0 = st(inc={0, 1, 2}, p={"B0"}, s={"B0"})
    k4 = (st(inc={0, 1, 2}, p={"A1"}),
          [("bind", BIND("A1")), ("admit", ADM("B0")), ("bind", BIND("A1")), ("admit_rev", ADM("B0"))], T4)
    obs = {}

    def b01(fx):
        legal_case(fx, S, m, x0, [], (), "A0", 0, tag="cut0:")
        legal_case(fx, S, m, x0, [], (), "A0", 1, tag="cut2:")

    def b02(fx):
        legal_case(fx, S, m, st(slots=(1,), inc={1, 2}), [], (), "A0", 0)

    def b03(fx):
        composition_case(fx, S, m, x0, [], (), "A0", 0, tag="k0:")
        composition_case(fx, S, m, k4[0], k4[1], k4[2], "A0", 0, tag="k4:")
        composition_case(fx, S, m, k4[0], k4[1], k4[2], "A0", 1, tag="k4rot:", share_wrap=True)
        xs = _states_of(m, k4[0], k4[1])
        o = D.oracle_transport(m, BETA, xs, k4[1], k4[2], "birth", "A0", 0)
        fx.check("fixture_sensitivity_w_term_nonzero", o["w_term"] != 0.0, o["w_term"])

    def b04(fx):
        selfloop_case(fx, S, m, st(inc={0, 1, 2}), [("flip", EOWN("flip", m, 0)), ("flip", EOWN("flip", m, 0))], T2,
                      "A0", 0, "dwell_guard", tag="dwell:")
        selfloop_case(fx, S, m, st(inc={0, 1, 2}, p={"A0"}), [("hop", EOWN("hop", m, 0)), ("hop", EOWN("hop", m, 0))],
                      T2, "A0", 0, "event_replay", tag="replay:")
        r = selfloop_case(fx, S, m, x0, [], (), "A1", 0, "empty_reference_owner", tag="empty:")
        fx.check("empty:exactly_one_integer_draw", len(int_draws(r)) == 1, r["rng_log"])

    def b05(fx):
        _, flagged = budget_sweep(fx, S, m, pf_build(*k4), [0, 0], [0.0], tag="accept:", expect_final="changed")
        obs["flagged"] = flagged
        fx.note({"OBSERVED_accepted_type_diag_mutated_before_commit_checkpoint": flagged})

    def b06(fx):
        enum_sweep(fx, S, m, pf_build(*k4), [0, 0], [0.0])

    def b07(fx):
        expect_stop(fx, invoke(S, model("MAIN", nonfinite_D_when_S=1), pf_build(x0, [], ()), ints=[0, 0], reals=[0.0]),
                    tag="nonfinite_D:")
        expect_stop(fx, invoke(S, model("MAIN", read_fail_when_S=1), pf_build(x0, [], ()), ints=[0, 0], reals=[0.0]),
                    tag="read_fail:")

    def b07t(fx):
        def tamper_w(p, run, s):
            p["events"][1] = dict(p["events"][1], W=p["events"][1]["W"] * (1 + 1e-12))
        expect_stop(fx, invoke(S, m, pf_build(*k4, mutate=tamper_w), ints=[0, 0], reals=[0.0]), tag="tamper_W:")

    def b08(fx):
        r = invoke(S, model("MAIN", opaque=True), pf_build(x0, [], ()), ints=[0, 0], reals=[0.0])
        fx.check("detector_fires_on_known_key6_read", r["outcome"] == "error" and r["exc_type"] == "TypeError", ostr(r))
        fx.check("input_unchanged_even_on_detector_error", r["input_unchanged"] and r["ids_unchanged"])

    builders = [
        ("B01", "zero-event Birth via cut0/cut2: diagonal ratio + count factor log 2", "required", b01),
        ("B02", "zero-event birth_rev: count factor log(1/2)", "required", b02),
        ("B03", "composition k=0, k=4 (bind/admission W change), rotated shared segment", "required", b03),
        ("B04", "guards: dwell, replay impossible, empty owner (one draw)", "required", b04),
        ("B05", "budget interruption at every checkpoint: path atomic", "required", b05),
        ("B06", "enumeration-cap interruption at every enumeration", "required", b06),
        ("B07", "nonfinite D / read failure at transformed state -> hard failure", "required", b07),
        ("B07t", "stored-event W tamper -> hard failure", "template", b07t),
        ("B08", "opaque-key detector positive control (Birth key[6] read must be caught)", "required", b08),
        ("B09", "static AST detector positive control (Birth key[6].bit_count flagged)", "required",
         lambda fx: static_fixture(fx, BIRTH_PATH, expect_clean=False)),
    ]
    if with_db:
        builders.append(("B10", "exact DB + kernel == oracle on DBB (full black-box bisection)", "required",
                         lambda fx: db_fixture(fx, S, "DBB", ("A0", "A1"), full_bisect=True)))
    return run_fixtures(builders), obs


# ----------------------------------------------------------------------------------------------
# Driver
# ----------------------------------------------------------------------------------------------


AUTHOR_MUTATIONS_C3V001 = [
    ("D_sign", "terms.append(-(ends[i+1]-ends[i])*(new['D']-old['D']))",
     "terms.append((ends[i+1]-ends[i])*(new['D']-old['D']))"),
    ("count_inverted", "terms = [math.log(len(old_roster)) - math.log(len(new_roster))]",
     "terms = [math.log(len(new_roster)) - math.log(len(old_roster))]"),
    ("W_omitted", "terms.append(math.log(after['W']) - math.log(before['W']))", "pass"),
    ("extra_amplitude", "logratio = math.fsum(terms)", "logratio = math.fsum(terms + [math.log(chosen['W'])])"),
    ("extra_time_density", "logratio = math.fsum(terms)", "logratio = math.fsum(terms + [math.log(run['beta'])])"),
    ("no_target_check",
     "        if not sampler._keys_equal(run, sampler._target_key(run, back), old['key']):\n"
     "            return reject('inverse_canonical_target')\n", ""),
    ("no_reverse_target_check",
     "if reverse is None or not sampler._keys_equal(run, sampler._target_key(run, reverse), segs[0]['key']):",
     "if reverse is None:"),
    ("ref_dwell_only",
     "    for old in segs:\n        sampler._budget_check(run, 'between', 'admission residence dwell transforms')\n",
     "    for _i, old in enumerate(segs):\n        if 0 < _i < len(segs) - 1:\n            transformed.append(old)\n"
     "            continue\n        sampler._budget_check(run, 'between', 'admission residence dwell transforms')\n"),
    ("eligible_roster", "    vertex = owner_roster[int(rng.integers(0, len(owner_roster)))]\n",
     "    _elig = [v for v in owner_roster if roster(segs[0]['state'], v)]\n    if not _elig:\n"
     "        return reject('empty_reference_vertex')\n    vertex = _elig[int(rng.integers(0, len(_elig)))]\n"),
    ("resample_empty", "    if not old_roster:\n        return reject('empty_reference_vertex')\n",
     "    for _ in range(2 * len(owner_roster)):\n        if old_roster:\n            break\n"
     "        vertex = owner_roster[int(rng.integers(0, len(owner_roster)))]\n"
     "        old_roster = roster(segs[0]['state'], vertex)\n"
     "    if not old_roster:\n        return reject('empty_reference_vertex')\n"),
    ("bare_owner", "owner = (ADMISSION_FAMILY, ('vertex', vertex))", "owner = ('vertex', vertex)"),
    ("group_level_roster", "            if sampler._keys_equal(run, ch['owner'], owner):",
     "            if True:"),
    ("stale_reads", "new = sampler._segment_core(run, ch['target'])",
     "new = dict(sampler._segment_core(run, ch['target']), row=old['row'], Da=old['Da'])"),
    ("diag_before_commit", "    sampler._budget_check(run, 'before', 'admission residence atomic commit')\n", ""),
    ("inplace_commit", "    return {'segments': transformed, 'events': new_events, 'times': list(times)}, 'changed'",
     "    segs[:] = transformed\n    events[:] = new_events\n    return path, 'changed'"),
    ("times_not_copied", "'times': list(times)}", "'times': times}"),
    ("wrap_dwell_omitted", "    for i, (old, new) in enumerate(zip(segs, transformed)):\n        terms.append(",
     "    for i, (old, new) in enumerate(zip(segs[:-1], transformed[:-1])):\n        terms.append("),
    ("uniform_dt", "terms.append(-(ends[i+1]-ends[i])*(new['D']-old['D']))",
     "terms.append(-(run['beta']/len(segs))*(new['D']-old['D']))"),
]


def behavior_diff(base, other):
    """Exhaustive behavioral comparison of two modules on every enumerated path of DB3, defect-DB3 and DBL,
    every vertex/mark prefix and u in {0, 0.5, 0.999}: outcome, Stop status/message, returned path, diag, draws."""
    n = diff = 0
    example = None
    for name, var in (("DB3", {}), ("DB3", {"admit_rev_resets_edge": 0}), ("DBL", {})):
        m = model(name, **var)
        ros = ("A0", "A1", "B0") if name == "DB3" else ("A0", "B0")
        for xs, evs, times in enumerate_paths(m):
            for vi in range(len(ros)):
                for mi in (0, 1):
                    for u in (0.0, 0.5, 0.999):
                        pf = pf_build(xs[0], list(evs), times)
                        a = invoke(base, m, pf, ints=[vi, mi], reals=[u], roster=ros)
                        b = invoke(other, m, pf, ints=[vi, mi], reals=[u], roster=ros)
                        n += 1
                        same = (a["outcome"], a["status"], a["message"]) == (b["outcome"], b["status"], b["message"])
                        if same and a["outcome"] == "changed":
                            same = D.deep_equal(a["ret_path"], b["ret_path"])[0]
                        same = same and D.deep_equal(a["diag"], b["diag"])[0] and a["rng_log"] == b["rng_log"]
                        if not same:
                            diff += 1
                            example = example or (name, var, xs, evs, vi, mi, u, ostr(a), ostr(b))
    return {"comparisons": n, "behavioral_differences": diff, "first_difference": example}


def author_mutants(base_path, out_dir, with_db=True):
    """Mutants of a COPY of the author logic, written only under out_dir (never the author files)."""
    src = Path(base_path).read_text()
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = {}
    for name, old, new in AUTHOR_MUTATIONS_C3V001:
        if src.count(old) != 1:
            rows[name] = {"applicable": False, "reason": f"pattern occurs {src.count(old)} times"}
            continue
        text = src.replace(old, new)
        if name == "diag_before_commit":
            text = text.replace("    tick('accepted_changed'); tick(kind + '_accepted_changed')\n",
                                "    tick('accepted_changed'); tick(kind + '_accepted_changed')\n"
                                "    sampler._budget_check(run, 'before', 'admission residence atomic commit')\n")
        mp = out_dir / f"mut_{name}.py"
        mp.write_text(text)
        try:
            mod = load_module(mp, f"author_mutant_{name}")
        except Exception as exc:  # noqa: BLE001
            rows[name] = {"applicable": True, "detected": True, "reason": f"does not load: {exc}"}
            continue
        res = admission_catalogue(Subject("author_mutant:" + name, mod.move, "admission", path=str(mp)),
                                  with_db=with_db, quick=True)
        failed = [r["id"] for r in res if r["category"] != "info" and not r["passed"]]
        dbv = {}
        for r in res:
            if r["id"] in ("A30", "A31", "A32"):
                c = {x["name"]: x["ok"] for x in r["checks"]}
                dbv[r["id"]] = {"detailed_balance": c.get("module_kernel_satisfies_detailed_balance"),
                                "kernel_equals_oracle": c.get("module_kernel_equals_oracle_kernel")}
        rows[name] = {"applicable": True, "detected": bool(failed), "failing_fixtures": failed, "db_status": dbv,
                      "mutated_sha256": sha256_file(mp),
                      "first_failed_checks": {r["id"]: [c["name"] for c in r["failed_checks"][:3]]
                                              for r in res if r["id"] in failed}}
        if not failed:
            base_mod = load_module(base_path, "author_base_for_equivalence")
            rows[name]["equivalence_probe"] = behavior_diff(Subject("base", base_mod.move, "admission"),
                                                            Subject("mut", mod.move, "admission"))
            rows[name]["equivalent_mutant"] = rows[name]["equivalence_probe"]["behavioral_differences"] == 0
    return rows


def summarize(results):
    out = {"n_checks": sum(r["n_checks"] for r in results)}
    for cat in ("required", "contract", "template"):
        rs = [r for r in results if r["category"] == cat]
        out[cat] = {"n": len(rs), "passed": sum(1 for r in rs if r["passed"]),
                    "failed": [r["id"] for r in rs if not r["passed"]]}
    out["info"] = [r["id"] for r in results if r["category"] == "info"]
    return out


def env():
    return {"python": sys.version.split()[0], "numpy": np.__version__, "platform": platform.platform(),
            "double_path": str(DOUBLE_PATH), "double_sha256": sha256_file(DOUBLE_PATH),
            "fixtures_sha256": sha256_file(Path(__file__)), "birth_reference_sha256": sha256_file(BIRTH_PATH)}


def main(argv=None):
    ap = argparse.ArgumentParser(description="0457 M2 residence-transport fixtures")
    ap.add_argument("--module", help="admission transport module path (loaded by path, never edited)")
    ap.add_argument("--expect-sha", help="refuse unless the module SHA256 equals this")
    ap.add_argument("--birth-control", action="store_true")
    ap.add_argument("--reference", action="store_true", help="admission catalogue on the test-only transcription")
    ap.add_argument("--mutants", action="store_true")
    ap.add_argument("--no-db", action="store_true")
    ap.add_argument("--author-mutants", metavar="DIR",
                    help="with --module: mutate a COPY of the module text into DIR (scratch) and run the catalogue")
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    t0 = time.perf_counter()
    report = {"artifact": "0457 Claude4 review helper M2 fixtures", "environment": env(), "beta": BETA,
              "scope": "synthetic double only; no project sampler, L4, project arrays or target data"}
    if a.birth_control:
        S = birth_subject()
        res, obs = birth_control(S, with_db=not a.no_db)
        report["birth_control"] = {"module": str(BIRTH_PATH), "sha256": BIRTH_SHA, "summary": summarize(res),
                                   "observations": obs, "fixtures": res}
    if a.reference:
        res = admission_catalogue(ref_subject(), with_db=not a.no_db)
        report["reference_transcription"] = {"summary": summarize(res), "fixtures": res,
                                             "scope": "test-only transcription of the 0456 contract; positive control"}
    if a.mutants:
        rows = {}
        for name, desc in MUTANTS.items():
            res = admission_catalogue(ref_subject(name), with_db=not a.no_db, quick=True)
            failed = [r["id"] for r in res if r["category"] != "info" and not r["passed"]]
            dbv = {}
            for r in res:
                if r["id"] in ("A30", "A31", "A32"):
                    c = {x["name"]: x["ok"] for x in r["checks"]}
                    dbv[r["id"]] = {"detailed_balance": c.get("module_kernel_satisfies_detailed_balance"),
                                    "kernel_equals_oracle": c.get("module_kernel_equals_oracle_kernel")}
            rows[name] = {"description": desc, "detected": bool(failed), "failing_fixtures": failed,
                          "db_status": dbv,
                          "first_failed_checks": {r["id"]: [c["name"] for c in r["failed_checks"][:4]]
                                                  for r in res if r["id"] in failed}}
        report["mutants"] = rows
    if a.module:
        p = Path(a.module).resolve()
        sha = sha256_file(p)
        if a.expect_sha and sha != a.expect_sha:
            raise SystemExit(f"module SHA256 {sha} != expected {a.expect_sha}")
        mod = load_module(p, "admission_module_under_test")
        S = Subject("module_under_test", mod.move, "admission", path=str(p))
        res = admission_catalogue(S, with_db=not a.no_db)
        report["module_under_test"] = {"path": str(p), "sha256": sha, "summary": summarize(res), "fixtures": res}
        if a.author_mutants:
            report["author_logic_mutants"] = {"base_sha256": sha, "scratch_dir": a.author_mutants,
                                              "rows": author_mutants(p, a.author_mutants, with_db=not a.no_db)}
        report["module_under_test"]["sha256_after_run"] = sha256_file(p)
    report["seconds"] = round(time.perf_counter() - t0, 2)
    Path(a.out).write_text(json.dumps(_jsonable(report), indent=1, sort_keys=False) + "\n")
    for k in ("birth_control", "reference_transcription", "module_under_test"):
        if k in report:
            print(k, json.dumps(report[k]["summary"]))
    if "author_logic_mutants" in report:
        for k, v in report["author_logic_mutants"]["rows"].items():
            print("author-mutant", k, v.get("applicable"), "detected" if v.get("detected") else "NOT DETECTED",
                  v.get("failing_fixtures"), v.get("db_status"), v.get("reason", ""),
                  v.get("equivalence_probe", ""))
    if "mutants" in report:
        for k, v in report["mutants"].items():
            print("mutant", k, "detected" if v["detected"] else "NOT DETECTED", v["failing_fixtures"], v["db_status"])
    print("seconds", report["seconds"])


if __name__ == "__main__":
    main()

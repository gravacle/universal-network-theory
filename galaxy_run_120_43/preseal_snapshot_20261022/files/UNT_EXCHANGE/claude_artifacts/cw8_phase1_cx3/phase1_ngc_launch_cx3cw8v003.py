"""P-112 Phase-1 launch custody. Invoked by the scientific launch owner only.

Implements A223 and the nine ROUND5 binding amendments. No function below starts
a scientific process on import. Runtime files are exclusive, fsynced and 0444.
"""
import argparse
import copy
import contextvars
import functools
import fcntl
import datetime as dt
import hashlib
import json
import math
import os
import re
import stat
import shutil
import signal
import subprocess
import sys
import time
import types
from pathlib import Path

PY = "/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"
A = "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/"
V006 = "/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md"
TOOL_NAME = "P112_LAUNCHER_CX3CW8V003"
RAM = 137438953472
DISK_RESERVE = 21474836480
SEED_KEY = "968c915bece706ea1d6c0fa15357984884a87443e7c19eebd104230c9c961981"
TWIN = "S0_SEED_CW8_TWIN"
CAPS = {
    "serial": {"wall_cap_s": 610324, "rss_cap_bytes": RAM, "output_cap_bytes": 146028888064},
    "twin": {"wall_cap_s": 22752, "rss_cap_bytes": RAM * 11, "output_cap_bytes": 34359738368},
}
THREAD_ENV = ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
              "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
NAME_RE = re.compile(r"^[A-Z0-9][A-Z0-9_]*$")
KIT_ATTEMPT_RE = re.compile(
    r"^(?P<name>S0_(?:SEED|J0|J1|J2)_SERIAL|S0_SEED_CW8_TWIN)_"
    r"(?P<kind>LAUNCH|MISLAUNCH)_C2V003A_A(?P<k>[1-9][0-9]?)\.json$")
OWN_ATTEMPT_RE = re.compile(
    r"^P112_(?P<name>[A-Z0-9][A-Z0-9_]*)_(?P<kind>LAUNCH|MISLAUNCH)_"
    r"CX2V001_A(?P<k>[1-9][0-9]*)\.json$")
RESIDUAL_RE = re.compile(r"^RESIDUAL_RETRY ([A-Z0-9][A-Z0-9_]*) ([1-9][0-9]*)$")
TOOL_PIN_RE = re.compile(r"^TOOL_PIN ([A-Z0-9][A-Z0-9_]*) ([0-9a-f]{64}) (/.*\S)$")
ENTRY_RE = re.compile(r"^## A[0-9]+(?:[: \t]|$)")
MONITOR_SCHEMA = "UNT_GALAXY_M0_MONITOR_RECEIPT_C2V001"
SERIAL_FILE = "CALL_A_K32_A2_HEADLINE_C2V001.json"
TWIN_FILE = "CALL_A_K32_A2_HEADLINE_CW8_TWIN_C2V001.json"
FILL_FILE = "FILL_RECEIPT_C2V001.json"
LEAF = ("numerics", "route_a", "column_workers")
RECEIPT_KEYS = {k: k for k in (
    "time_utc", "spec_sha256", "theta_sha256", "rss_cap_bytes", "wall_cap_s",
    "output_cap_bytes", "host_ram_bytes", "other_ngc_processes_max")}
RECEIPT_KEYS["status"] = "raw_status"

# Literal exact-string map. No wildcard or default class is permitted.
STATUS_CLASSES = {
    "FINISHED|COMPLETED": "FINISHED",
    "FINISHED|COMPLETED_INVALID": "FINISHED",
    "CHILD_FAILED|FAILED": "FAILED",
    "CHILD_FAILED|FAILED_AT_STAGE": "FAILED",
    "CHILD_FAILED|ROUTE_A_NO_FIXED_POINT": "FAILED",
    "CHILD_FAILED|NONE|EXIT": "FAILED",
    "STOPPED_WALL_CAP|COMPLETED": "CAP",
    "STOPPED_WALL_CAP|COMPLETED_INVALID": "CAP",
    "STOPPED_WALL_CAP|FAILED": "CAP",
    "STOPPED_WALL_CAP|FAILED_AT_STAGE": "CAP",
    "STOPPED_WALL_CAP|ROUTE_A_NO_FIXED_POINT": "CAP",
    "STOPPED_WALL_CAP|REFUSED": "CAP",
    "STOPPED_WALL_CAP|BLOCKED": "CAP",
    "STOPPED_WALL_CAP|UNREADABLE_FINISH": "CAP",
    "STOPPED_WALL_CAP|RESULT_HASH_MISMATCH": "CAP",
    "STOPPED_WALL_CAP|NONE": "CAP",
    "STOPPED_RSS_CAP|COMPLETED": "CAP",
    "STOPPED_RSS_CAP|COMPLETED_INVALID": "CAP",
    "STOPPED_RSS_CAP|FAILED": "CAP",
    "STOPPED_RSS_CAP|FAILED_AT_STAGE": "CAP",
    "STOPPED_RSS_CAP|ROUTE_A_NO_FIXED_POINT": "CAP",
    "STOPPED_RSS_CAP|REFUSED": "CAP",
    "STOPPED_RSS_CAP|BLOCKED": "CAP",
    "STOPPED_RSS_CAP|UNREADABLE_FINISH": "CAP",
    "STOPPED_RSS_CAP|RESULT_HASH_MISMATCH": "CAP",
    "STOPPED_RSS_CAP|NONE": "CAP",
    "STOPPED_OUTPUT_CAP|COMPLETED": "OUTPUT_CAP",
    "STOPPED_OUTPUT_CAP|COMPLETED_INVALID": "OUTPUT_CAP",
    "STOPPED_OUTPUT_CAP|FAILED": "OUTPUT_CAP",
    "STOPPED_OUTPUT_CAP|FAILED_AT_STAGE": "OUTPUT_CAP",
    "STOPPED_OUTPUT_CAP|ROUTE_A_NO_FIXED_POINT": "OUTPUT_CAP",
    "STOPPED_OUTPUT_CAP|REFUSED": "OUTPUT_CAP",
    "STOPPED_OUTPUT_CAP|BLOCKED": "OUTPUT_CAP",
    "STOPPED_OUTPUT_CAP|UNREADABLE_FINISH": "OUTPUT_CAP",
    "STOPPED_OUTPUT_CAP|RESULT_HASH_MISMATCH": "OUTPUT_CAP",
    "STOPPED_OUTPUT_CAP|NONE": "OUTPUT_CAP",
    "CHILD_FAILED|REFUSED": "INFRA",
    "CHILD_FAILED|BLOCKED": "INFRA",
    "CHILD_FAILED|NONE|SIGNAL": "INFRA",
    "CHILD_FAILED|UNREADABLE_FINISH": "INFRA",
    "CHILD_FAILED|RESULT_HASH_MISMATCH": "INFRA",
    "CHILD_FAILED|COMPLETED": "INFRA",
    "CHILD_FAILED|COMPLETED_INVALID": "INFRA",
    "FINISHED|NONE": "INFRA",
    "FINISHED|UNREADABLE_FINISH": "INFRA",
    "FINISHED|RESULT_HASH_MISMATCH": "INFRA",
    "FINISHED|FAILED": "INFRA",
    "FINISHED|FAILED_AT_STAGE": "INFRA",
    "FINISHED|ROUTE_A_NO_FIXED_POINT": "INFRA",
    "FINISHED|REFUSED": "INFRA",
    "FINISHED|BLOCKED": "INFRA",
    "MISLAUNCH": "INFRA",
    "MONITOR_REFUSED": "INFRA",
    "TWIN_PLANNED_STOP": "PLANNED_STOP",
}
STATUS_MAP_SHA = "c36c37886aa67db763160681be99904c3ae9f22ebb51f3e841adadfa0e1cdb54"


class Refusal(ValueError):
    def __init__(self, code, detail=None):
        self.code, self.detail = code, detail
        super().__init__(code if detail is None else "%s: %s" % (code, detail))


def need(condition, code, detail=None):
    if not condition:
        raise Refusal(code, detail)


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


assert len(STATUS_CLASSES) == 54 and len(canonical(STATUS_CLASSES)) == 2052
assert sha(canonical(STATUS_CLASSES)) == STATUS_MAP_SHA


def no_dupes(pairs):
    result = {}
    for k, v in pairs:
        need(k not in result, "JSON_DUPLICATE_KEY", k)
        result[k] = v
    return result


def strict_json(raw):
    def bad_constant(value):
        raise Refusal("JSON_NONFINITE", value)
    try:
        return json.loads(raw, object_pairs_hook=no_dupes, parse_constant=bad_constant)
    except (ValueError, UnicodeError) as e:
        if isinstance(e, Refusal):
            raise
        raise Refusal("JSON_PARSE", type(e).__name__) from e


def keys(obj, expected, where):
    need(type(obj) is dict and set(obj) == set(expected), "EXACT_KEYS", where)


def date_u():
    return subprocess.check_output(
        ["/bin/date", "-u"], text=True, env=dict(os.environ, LC_ALL="C")).strip()


def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def timestamp(value, whole=False):
    pattern = r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ" if whole else (
        r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d{1,6})?Z")
    need(isinstance(value, str) and re.fullmatch(pattern, value), "UTC_FORMAT", value)
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    except ValueError as e:
        raise Refusal("UTC_FORMAT", value) from e


def encoded(obj):
    return (json.dumps(obj, sort_keys=True, indent=1, allow_nan=False) + "\n").encode()


def write_x_bytes(path, raw):
    path = Path(path)
    need(path.is_absolute(), "OUTPUT_ABSOLUTE", str(path))
    need(os.path.realpath(path.parent) == str(path.parent), "OUTPUT_PARENT_SYMLINK")
    with path.open("xb") as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
        os.fchmod(f.fileno(), 0o444)
    try:
        fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    except OSError:
        # Some mount types do not support directory fsync; the file is fsynced.
        pass
    return {"path": str(path), "sha256": sha(raw)}


def write_x(path, obj):
    need(type(obj) is dict and isinstance(obj.get("date_u"), str), "RECORD_DATE_U")
    return write_x_bytes(path, encoded(obj))


def path_rules(path, where="PATH"):
    need(isinstance(path, str) and os.path.isabs(path) and os.path.normpath(path) == path,
         "PATH_ABSOLUTE_NORMALIZED", where)
    parts = Path(path).parts
    low = path.lower()
    need("runs_ext" not in parts, "PATH_RUNS_EXT", where)
    need(not any(p.lower() == "v007_postseal_records" for p in parts), "PATH_V007_POSTSEAL", where)
    need(not any(p.lower().startswith("uvt_") for p in parts), "PATH_UVT", where)
    need("unt_internal_runs" not in low and "kmax_a2f10_c5h" not in low,
         "PATH_PROTECTED_TREE", where)
    need(not any("ngc3198" in p.lower() for p in parts), "PATH_NGC3198", where)
    need(not (path == str(Path.home() / ".codex") or
              path.startswith(str(Path.home() / ".codex") + "/")), "PATH_CODEX", where)
    return path


READ_RUN_ROOTS = set()


def guard_read(path):
    # Check both spellings before opening bytes, including a symlink alias.
    for candidate in dict.fromkeys((str(path), os.path.realpath(path))):
        path_rules(candidate, "read")
        parts = [p.lower() for p in Path(candidate).parts]
        base = Path(candidate).name.lower()
        need("a_side" not in parts and "stages" not in parts, "FORBIDDEN_READ_PATH")
        need(base not in ("result.json", "finish.json", "progress.jsonl"), "FORBIDDEN_RESULT_READ")
        need(not base.startswith(("freeze_expected_inputs_", "dryrun_freeze_", "freeze_manifest")), "FORBIDDEN_SEALED_READ")
        for root in READ_RUN_ROOTS:
            if candidate.startswith(root + "/"):
                need(str(Path(candidate).parent) == root and candidate.endswith(
                    (".receipt.json", ".receipt.json.launch.json", ".attempt_receipt.json", ".solo.json")),
                    "FORBIDDEN_OUTDIR_READ")


def is_pin(pin):
    return (type(pin) is dict and set(pin) == {"path", "sha256"} and
            isinstance(pin["path"], str) and os.path.isabs(pin["path"]) and
            isinstance(pin["sha256"], str) and HEX64.fullmatch(pin["sha256"]) is not None)


_READ_CONTEXT = contextvars.ContextVar("p112_read_context", default=None)


def read_scope(function):
    """One immutable-input byte snapshot for one public operation (0785)."""
    @functools.wraps(function)
    def scoped(*args, **kwargs):
        if _READ_CONTEXT.get() is not None:
            return function(*args, **kwargs)
        token = _READ_CONTEXT.set({"snapshots": {}, "observations": {"counts": {}, "last_observation": {}}})
        try:
            return function(*args, **kwargs)
        finally:
            _READ_CONTEXT.reset(token)
    return scoped


def read_and_pin(path, decode=True):
    """Guard, read once, hash and parse the same immutable-input buffer."""
    path = str(path)
    guard_read(path)
    context = _READ_CONTEXT.get()
    snapshots = context["snapshots"] if context is not None else None
    cache_key = path if snapshots is not None and path in snapshots else os.path.realpath(path)
    if snapshots is not None and cache_key in snapshots:
        raw = snapshots[cache_key]
    else:
        raw = Path(path).read_bytes()
    if snapshots is not None:
        snapshots[cache_key] = raw
        snapshots[path] = raw
    pin = {"path": path, "sha256": sha(raw)}
    return pin, strict_json(raw) if decode else raw


def guard_record(path):
    path = str(path)
    guard_read(path)
    need(os.path.realpath(path) == path, "RECORD_SYMLINK", path)
    need(os.stat(path).st_nlink == 1, "RECORD_NLINK", path)
    return path


def read_record(path, decode=True):
    """Immutable monitor/work metadata additionally forbids symlink aliases."""
    return read_and_pin(guard_record(path), decode=decode)


def observe_file(path, kind, *, v006=False):
    """A changing file is read once for each observation, never through the snapshot cache."""
    path = str(path)
    if v006 and path == V006:
        need(os.path.realpath(path) == path, "V006_PATH")
    else:
        guard_record(path)
    raw = Path(path).read_bytes()
    pin = {"path": path, "sha256": sha(raw)}
    context = _READ_CONTEXT.get()
    if context is not None:
        report = context["observations"]
        report["counts"][kind] = report["counts"].get(kind, 0) + 1
        report["last_observation"][kind] = {"kind": kind, "pin": pin, "bytes": len(raw)}
    return raw, pin


def observation_report():
    context = _READ_CONTEXT.get()
    return copy.deepcopy(context["observations"]) if context is not None else {"counts": {}, "last_observation": {}}


def read_pin(pin, decode=True):
    need(is_pin(pin), "PIN_FORM", pin)
    actual, raw = read_and_pin(pin["path"], decode=False)
    need(actual["sha256"] == pin["sha256"], "PIN_SHA_MISMATCH", pin["path"])
    return strict_json(raw) if decode else raw


def pin_of(path):
    return read_and_pin(path, decode=False)[0]


def load_verified(pin, name):
    raw = read_pin(pin, decode=False)
    module = types.ModuleType(name)
    module.__file__ = pin["path"]
    exec(compile(raw, pin["path"], "exec"), module.__dict__)
    return module


def fhex(value, where):
    need(type(value) in (int, float), "THETA_NOT_NUMERIC", where)
    f = float(value)
    need(math.isfinite(f), "THETA_NONFINITE", where)
    return f.hex()


def equal_hex(left, right, where):
    need(fhex(left, where) == fhex(right, where), "THETA_BITS_MISMATCH", where)


def equal_theta(left, right, where):
    need(type(left) is dict and type(right) is dict and set(left) == set(right),
         "THETA_KEY_SET", where)
    for key in sorted(left):
        equal_hex(left[key], right[key], where + "." + key)


def tool_gate(text, own_pin):
    entry, matches, malformed = False, [], False
    for line in text.split("\n"):
        line = line.rstrip("\r")
        if line.startswith("## "):
            entry = ENTRY_RE.match(line) is not None
        if line.startswith("TOOL_PIN " + TOOL_NAME):
            # A version successor is an independent name, not this version.
            word = line.split(maxsplit=2)
            if len(word) > 1 and word[1] != TOOL_NAME:
                continue
            match = TOOL_PIN_RE.fullmatch(line)
            if not entry or match is None:
                malformed = True
            else:
                matches.append({"path": match[3], "sha256": match[2]})
    need(not malformed, "TOOL_PIN_MISMATCH")
    need(len(matches) <= 1, "TOOL_PIN_DUPLICATE")
    need(matches, "TOOL_PIN_MISSING")
    need(matches[0] == own_pin and os.path.realpath(matches[0]["path"]) == own_pin["path"],
         "TOOL_PIN_MISMATCH")
    return matches[0]


def residual_lines(text):
    result, entry = set(), False
    for line in text.split("\n"):
        line = line.rstrip("\r")
        if line.startswith("## "):
            entry = ENTRY_RE.match(line) is not None
        if line.startswith("RESIDUAL_RETRY"):
            m = RESIDUAL_RE.fullmatch(line)
            need(entry and m is not None, "RESIDUAL_RETRY_MALFORMED", line)
            result.add((m[1], int(m[2])))
    return result


def monitor_receipt(raw):
    rec = strict_json(raw)
    need(type(rec) is dict and rec.get("schema") == MONITOR_SCHEMA, "MONITOR_RECEIPT_SCHEMA")
    core = {k: v for k, v in rec.items() if k != "receipt_sha256"}
    need(rec.get("receipt_sha256") == sha(canonical(core)), "MONITOR_RECEIPT_SELF_HASH")
    # Deliberately not root_monitor.verify_receipt: it opens result.json.
    return rec


def raw_status(rec, *, name, attempt, outdir, receipt, launch_pin, child_pid,
               mislaunch=None, stop=None):
    if mislaunch is not None:
        bound = (mislaunch.get("name") == name and mislaunch.get("attempt") == attempt and
                 mislaunch.get("outdir") == outdir and mislaunch.get("receipt") == receipt)
        lj = mislaunch.get("launch_json") or {}
        if lj.get("sha256") is not None:
            bound = bound and lj["sha256"] == launch_pin["sha256"]
        if lj.get("child_pid") is not None:
            bound = bound and lj["child_pid"] == child_pid
        need(bound, "MISLAUNCH_NOT_BOUND")
        return "MISLAUNCH", "INFRA"
    if name == TWIN and stop is not None:
        need(type(stop) is dict and stop.get('schema') == 'UNT_S0_TWIN_KILL_RECORD_C2V003A' and
             stop.get('reason') == 'ITERATION_0001_COMPLETED_AND_SIDECAR' and
             stop.get('outdir') == outdir and stop.get('launch_json') == launch_pin and
             type(stop.get('pgid')) is int and stop['pgid'] == child_pid and
             stop.get('result') in ('KILLED_TERM', 'KILLED_KILL') and
             isinstance(stop.get('date_u'), str) and bool(stop['date_u']), 'TWIN_STOP_NOT_BOUND')
        return 'TWIN_PLANNED_STOP', 'PLANNED_STOP'
    # A248: STOPPED_* by itself is never evidence of the designed twin stop.
    driver = rec.get("driver_status")
    need(driver is None or isinstance(driver, str), "DRIVER_STATUS_FORM")
    raw = str(rec.get("status")) + "|" + (driver if driver is not None else "NONE")
    if raw == "CHILD_FAILED|NONE":
        need(type(rec.get("exit_code")) is int, "EXIT_CODE_FORM")
        raw += "|SIGNAL" if rec["exit_code"] < 0 else "|EXIT"
    need(raw in STATUS_CLASSES, "RECEIPT_STATUS_UNMAPPED", raw)
    return raw, STATUS_CLASSES[raw]



def sample_value(sample, rec):
    if sample is None:
        return None
    if sample.get("complete") is not True:
        return None
    try:
        p = sample["poll_s"]
        gap = sample["largest_gap_s"]
        need(type(p) in (int, float) and math.isfinite(p) and 0 < p <= 10, "SAMPLE_POLL")
        need(type(gap) in (int, float) and math.isfinite(gap) and gap >= 0, "SAMPLE_GAP")
        if gap > 2 * p:
            return None
        if math.floor(timestamp(sample["first_utc"])) >= timestamp(rec["utc_start"], whole=True):
            return None
        if math.floor(timestamp(sample["last_utc"])) <= timestamp(rec["utc_end"], whole=True):
            return None
        count = sample["max_other_ngc_processes"]
        need(type(count) is int and count >= 0, "SAMPLE_COUNT")
        need(type(sample["n_samples"]) is int and sample["n_samples"] >= 2, "SAMPLE_N")
        return count
    except (KeyError, Refusal):
        return None


def first_caps(name, column_workers=1):
    caps = dict(CAPS["twin" if name == TWIN else "serial"])
    caps["rss_cap_bytes"] = cw8_rss(name, column_workers)
    return caps


def caps_of(receipt):
    return {k: receipt[k] for k in CAPS["serial"]}


def terminal_prefix(actual, name, authenticated_causes=None):
    """Only natural completion, evidenced twin stop, or reproduced model outcomes."""
    for i, current in enumerate(actual):
        cls = current.get('status_class')
        if current.get('_known_nonphysics'):
            continue
        if cls == 'FINISHED':
            return {'index': i, 'disposition': 'FINISHED'}
        if cls == 'PLANNED_STOP':
            need(name == TWIN, 'PLANNED_STOP_NOT_TWIN')
            need(is_pin(current.get('pins', {}).get('stop_record')), 'TWIN_STOP_NOT_BOUND')
            return {'index': i, 'disposition': 'PLANNED_STOP'}
        if i == 0 or cls != 'FAILED':
            continue
        previous = actual[i - 1]
        identity = _authenticated_identity(current, authenticated_causes)
        if identity is None or identity != _authenticated_identity(previous, authenticated_causes):
            continue
        if current['pins']['monitor_receipt']['sha256'] == previous['pins']['monitor_receipt']['sha256']:
            continue
        if len({r.get('spec_sha256') for r in actual[:i + 1]}) != 1:
            continue
        if any(r.get('solo_mode') is not True or type(r.get('other_ngc_processes_max')) is not int
               or r['other_ngc_processes_max'] != 0 for r in (previous, current)):
            continue
        if current.get('host_ram_bytes') != RAM or \
                current.get('rss_cap_bytes') != cw8_rss(name, current.get('_verified_column_workers', 1)):
            continue
        return {'index': i, 'disposition': 'RULE_C_INVALID',
                'model_identity': list(identity), 'counted_attempts': [i - 1, i]}
    return None



def next_attempt(name, records, actual, residuals, trailing_nonattempt=None, *,
                 phase_ceiling_utc, now_utc, monitor_ceiling_utc=None,
                 authenticated_causes=None, root_hold_release=False,
                 has_monitor_refusal=False, column_workers=1):
    """Pure prospective decision; every invocation launches at most one root-chosen attempt.

    A270: Phase 2 is the only admission and monitor ceiling. Phase 1
    is a reporting cutoff, including for first admissions and reruns.
    """
    terminal = terminal_prefix(actual, name, authenticated_causes)
    need(terminal is None, 'ATTEMPT_AFTER_TERMINAL', terminal)
    need(not held_for_fix(actual) or root_hold_release, 'HELD_FOR_FIX')
    need(not held_for_cause(actual, authenticated_causes), 'HELD_FOR_CAUSE')
    need(monitor_ceiling_utc is not None, 'MONITOR_PHASE2_CEILING_REQUIRED')
    wall = remaining_wall(monitor_ceiling_utc, now_utc)
    ks = [r['attempt'] for r in records] + [k for n, k in residuals if n == name]
    k = max(ks, default=0) + 1
    if name.startswith('S0_'):
        need(any(r['origin'] == 'P112' or r['outcome'] == 'LAUNCH' for r in records)
             or any(n == name for n, _ in residuals), 'KIT_RELAUNCH_OWNS')
    retry = bool(records or actual or trailing_nonattempt is not None or residuals or has_monitor_refusal)
    caps = first_caps(name, column_workers)
    basis = []
    if trailing_nonattempt is not None:
        caps = dict(trailing_nonattempt['caps'])
    elif actual:
        previous = actual[-1]
        caps = caps_of(previous)
        if previous['status_class'] == 'OUTPUT_CAP':
            caps['output_cap_bytes'] *= 2
        basis = [r['receipt_pin'] for r in actual if is_pin(r.get('receipt_pin'))]
    caps['rss_cap_bytes'] = cw8_rss(name, column_workers)
    caps['wall_cap_s'] = wall
    return {
        'attempt': k, 'caps': caps, 'solo_mode': retry,
        # No unrun attempt can already be counted as reproduced.
        'counted_rerun': False, 'rule_c_basis': basis,
        'phase_ceiling_utc': phase_ceiling_utc, 'monitor_ceiling_utc': monitor_ceiling_utc,
        'decision_utc': now_utc,
        'model_confirmation_rerun': bool(actual and _authenticated_identity(actual[-1], authenticated_causes)),
    }



def attempt_volume(config, origin):
    return config["run_volume"] if origin == "P112" else str(Path(config["s0"]["run_root"]).parent)


def absent_paths(outdir):
    receipt = outdir + ".receipt.json"
    return {"outdir": outdir, "receipt": receipt, "launch_json": receipt + ".launch.json",
            "receipt_stdout": receipt + ".stdout.txt", "receipt_stderr": receipt + ".stderr.txt"}


def entry_reuse(old, new, records, refusals, k):
    need(old.get("spec", {}).get("sha256") == new["spec"]["sha256"] and
         old.get("point_key", old.get("theta_key")) == new["point_key"] and
         old.get("v006_spec_pin") == new["v006_spec_pin"] and
         old.get("v006_handoff_pin") == new["v006_handoff_pin"],
         "REGISTRY_ENTRY_EXISTS_FOR_ANOTHER_SPEC")
    need(not records, "ALREADY_LAUNCHED")
    need(all(r["attempt"] == k for r in refusals), "REFUSAL_ATTEMPT_MISMATCH")
    return "ALREADY_REGISTERED_SAME_SPEC"


# Byte-pinned sources, generated Tue Oct 20 17:33:02 UTC 2026
SOURCE_PINS = {'galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py', 'sha256': '577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377'}, 'root_monitor_c2v001.py': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/galaxy_m0_forward_c2_0466/root_monitor_c2v001.py', 'sha256': 'ba031c2340057d88ee399138cc645012a93aa7dc3eb7c9bba56d112c94a47107'}, 's0_kit_c2v003a.py': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s0_launch_kit_c2/s0_kit_c2v003a.py', 'sha256': 'fdc0ee6c833072b40991750f8df1122a1b51910986f01af3480a73cccfbed550'}, 'launch_s0_serial_root_c2v003a.sh': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s0_launch_kit_c2/launch_s0_serial_root_c2v003a.sh', 'sha256': '621263a21b813e8c71762cea57b0efc6ba36aecb1cf9023cc788f9133c3a96c2'}, 'launch_twin_root_c2v003a.sh': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s0_launch_kit_c2/launch_twin_root_c2v003a.sh', 'sha256': 'f199544db9fe40a4fedbe7647d52ad4bd8dacb13a9aa9c1b9ab4ad0198e7769f'}, 'twin_kill_watch_c2v003a.sh': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s0_launch_kit_c2/twin_kill_watch_c2v003a.sh', 'sha256': 'a3d70bec454691b6dcfcb8a9bbfe40d50b71cb85da564fc4ab803b55b02de925'}, 's0_prelaunch_record_c2v001.py': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s0_launch_kit_c2/s0_prelaunch_record_c2v001.py', 'sha256': 'a10965b7a508f106e3d153632d2b1a39a427d9106fa2de3c9e09d92b85bcb59a'}, 'README_S0_LAUNCH_KIT_C2V003A.md': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s0_launch_kit_c2/README_S0_LAUNCH_KIT_C2V003A.md', 'sha256': '42978c3f938b1bf45a6a45b623e6f8ad25c5a333f8ecaef9a6cf657206f10b0e'}, 'fill_step5_c2v001.py': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step5_path_c2/tools/fill_step5_c2v001.py', 'sha256': 'ec417e76509427d8e942f52f02e9862a0277c90e3b92014c48b44a2efad61783'}, 'dry_one_c2v001.py': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step5_path_c2/tools/dry_one_c2v001.py', 'sha256': 'aac20dd3ca18bb609b37216f552aeb5a6b9f37147e17fc5501ea3c8d0842596b'}, 'phase1_point_handoffs_c2v001.py': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step5_path_c2/tools/phase1_point_handoffs_c2v001.py', 'sha256': '7d3b7c3c86204ca98b7fb87e39b11b544f3ee6069f8b34909e4c7810c00667cb'}, 'README_STEP5_PATH_C2V001.md': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step5_path_c2/README_STEP5_PATH_C2V001.md', 'sha256': 'fba1a70a91f70b36b0f8035bb9ade5ec78bd8a44667954bd877c03d02c2eb1cd'}, 'POLICY_C2V001.json': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step5_path_c2/POLICY_C2V001.json', 'sha256': '0c781a17548150831a7e10b8dd9d27897b856ab21398ee277fab3d2bbc4287e9'}, 'TEMPLATE_A_K32_A2_HEADLINE_C2V001.json': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step5_path_c2/templates/TEMPLATE_A_K32_A2_HEADLINE_C2V001.json', 'sha256': '68a19360d49f4dc547608ca8b2cec7116bed03b0f0cb947bb55e2aa1c61c13fb'}, 'TEMPLATE_A_K32_A2_HEADLINE_CW8_TWIN_C2V001.json': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step5_path_c2/templates/TEMPLATE_A_K32_A2_HEADLINE_CW8_TWIN_C2V001.json', 'sha256': '1aa662697fe259bd8c1bb9a4bda6170fdfabcc31e10a56a049a02c2f93961783'}, 'CAPS_S45_C2V003.json': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/sched_s45_c2/v003/CAPS_S45_C2V003.json', 'sha256': '35f66b6a3152f985fe6edcbaeda2950e5b17e9f9f6026e5f6201052db1508f64'}, 'LO_NGC_K32_CERT_V001.json': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_ngc_k32/gates/LO_NGC_K32_CERT_V001.json', 'sha256': '07745bbf6d5c35d5a8568de7fc9e78b8c3bd8c3e371680dc8869c42a893c0382'}, 'S0_C2V001.json': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/phase1_c2/S0_RECORD_ROOT_V001/S0_C2V001.json', 'sha256': '1be5ed709cdb49106652beb76baaafc1c257e760d8cda2c62c18ea6fb2e88143'}, 'phase1_c2v003b.py': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/phase1_c2/phase1_c2v003b.py', 'sha256': '7d891ff7d81b0e9d103707d79c7a057cedc6dc1e893a0f4e9372a51d0b796dd4'}, 'README_PHASE1_C2V003B.md': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/phase1_c2/README_PHASE1_C2V003B.md', 'sha256': 'cf3a4de73067529308c3f744261e641aa7f9d61b0b21e45338a60a22ad6ae3b0'}, 'calibration_orchestrator_c2v005.py': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py', 'sha256': 'c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d'}, 'roster_builder_c2v006.py': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/runbook_v002_c2/roster_builder_c2v006.py', 'sha256': '0cc731065d1f00e1549cb7b9442c901da0a35f48c8a03d67f14701f652ad0aa2'}, 'RUNBOOK_V002_C2V006.md': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/runbook_v002_c2/RUNBOOK_V002_C2V006.md', 'sha256': 'e162db3e7bcaf348db2455aac9032ac8b0c57bb536ec97d043b6d9aad084349b'}, 'README_RUNBOOK_V002_C2V006.md': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/runbook_v002_c2/README_RUNBOOK_V002_C2V006.md', 'sha256': '730bc14ce973f5eb61ff753541e31d0a9fa26d0f94acaf95b172ef7d26279b8f'}, 'interface_proof_c2v006.py': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/runbook_v002_c2/interface_proof_c2v006.py', 'sha256': '9b3772cfc6cfcb3a9f5d89497c9b855e17f3508e3474c1ca1c961f9520e6402d'}, 'test_runbook_v002_c2v006.py': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/runbook_v002_c2/test_runbook_v002_c2v006.py', 'sha256': '88d79035bab8f78131a44d4f03cd209b85ca9245799d3e489441deee5d31268e'}, 'prediction_freeze_c2v003g_cx3v001.py': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/prediction_freeze_c2v003g_cx3v001.py', 'sha256': '48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405'}, 'FREEZE_SPEC_OF_RECORD_C2V004.json': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s0_launch_kit_c2/FREEZE_SPEC_OF_RECORD_C2V004.json', 'sha256': 'e2a7650e166a9230138ffd16453ac8fdabab41a8695169844940c4c061a894ec'}, 'A133_TWO_PHASE_PROTOCOL_V001.md': {'path': '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/A133_TWO_PHASE_PROTOCOL_V001.md', 'sha256': 'cd92ef914a0d562f0392080ebf709b5fdb1d85ef7f7b4493ee143fe782cfac17'}, 'PREREG_MISS_READING_R3A.md': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/miss_reading_prereg_c4/r3a_sc3/PREREG_MISS_READING_R3A.md', 'sha256': 'c64f65a357a0d3b44b362795fe7793576ba0ff6a71f1bafd2357573e2eb376c8'}, 'eps_ngc_point_c4v002.py': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_point_producer_c4/s0/build_c4v001/tools/eps_ngc_point_c4v002.py', 'sha256': '8972822b5439e184297b4a5dbb552983ddb806804565ee1cc26691b680147235'}, 'gq_binding_c4v002.py': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_point_producer_c4/s0/build_c4v001/tools/gq_binding_c4v002.py', 'sha256': 'f4ee064d9da414d9b98581ff6c1e374aab566950d9faf2e978342bc9a5dba0b1'}, 'ngc_rho_producer_c3v003.py': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/ngc_rho_c3v003/ngc_rho_producer_c3v003.py', 'sha256': 'd3d0f3ddda8be2e3d4b0e0732e5237a602cb3b1fb99d7921e8c10a886420a3c4'}, 'ngc_rho_stage_c3v003.py': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/ngc_rho_c3v003/ngc_rho_stage_c3v003.py', 'sha256': '496d2a215145fb25aadbc4623b8930134cc2679cf1fe8097c65bf84cab450090'}, 'ngc_lo_slot_proof_c3v003.py': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/ngc_rho_c3v003/ngc_lo_slot_proof_c3v003.py', 'sha256': 'ada31d121871598aa0cd7db5137691502421c873cc75bdf331706501d3f3310a'}, 'ngc_acceptance_handoff_c2v005.py': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_acceptance_c2/ngc_acceptance_handoff_c2v005.py', 'sha256': '7077ad9337d48b444bb724b3d0dca531e615bbb09656fa00ba453bacf2e634b1'}, 'ngc_lo_state_adapter_c2v003a.py': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_acceptance_c2/ngc_lo_state_adapter_c2v003a.py', 'sha256': '9c4b6dfc591cfd5c372416beb936d5d903540e5fc41e4a327b428d7ba5001eb2'}, 'ngc_roster_recipes_c2v002.py': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_acceptance_c2/ngc_roster_recipes_c2v002.py', 'sha256': 'c700f469314d73e90cd2498cdbea5b7f69fbbd9b61676468ea5e37356939978e'}, 'ngc_acceptance_handoff_c2v003a.py': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_acceptance_c2/ngc_acceptance_handoff_c2v003a.py', 'sha256': '7c54fd6fcc3defbc6728a35fd5125eb0d2fba23b735a38af6ac8de2094c04427'}, 'values_writer_c2v004_cx2v002.py': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/values_writer_cx2/values_writer_c2v004_cx2v002.py', 'sha256': '26319ecbfaf944c80c5df91a0c592899727e6ff9f5177404ebc49309bd906f0e'}, 'extract_carriers_cx3v005.py': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step5_ngc_route_ab_readiness_cx3/carriers_0606_v001/tools/extract_carriers_cx3v005.py', 'sha256': '50c7db5fbc2eb2cce17dcbb53ba1186bfdbc635a4098b0eb33ebd1402829732f'}, 'extract_carriers_c2v001.py': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step5_path_c2/tools/extract_carriers_c2v001.py', 'sha256': '8acd21c7b8c2c1d96038a6d1eee9cbf68c25e556ae4da59bea8b70f09c1c602a'}}
DECLARED_TOOLS = [{'tool': 'galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001', 'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py', 'sha256': '577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377', 'driver_only': True}, {'tool': 'eps_ngc_point_c4v002', 'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_point_producer_c4/s0/build_c4v001/tools/eps_ngc_point_c4v002.py', 'sha256': '8972822b5439e184297b4a5dbb552983ddb806804565ee1cc26691b680147235', 'driver_only': False}, {'tool': 'gq_binding_c4v002', 'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_point_producer_c4/s0/build_c4v001/tools/gq_binding_c4v002.py', 'sha256': 'f4ee064d9da414d9b98581ff6c1e374aab566950d9faf2e978342bc9a5dba0b1', 'driver_only': False}, {'tool': 'ngc_rho_producer_c3v003', 'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/ngc_rho_c3v003/ngc_rho_producer_c3v003.py', 'sha256': 'd3d0f3ddda8be2e3d4b0e0732e5237a602cb3b1fb99d7921e8c10a886420a3c4', 'driver_only': False}, {'tool': 'ngc_rho_stage_c3v003', 'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/ngc_rho_c3v003/ngc_rho_stage_c3v003.py', 'sha256': '496d2a215145fb25aadbc4623b8930134cc2679cf1fe8097c65bf84cab450090', 'driver_only': False}, {'tool': 'ngc_lo_slot_proof_c3v003', 'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/ngc_rho_c3v003/ngc_lo_slot_proof_c3v003.py', 'sha256': 'ada31d121871598aa0cd7db5137691502421c873cc75bdf331706501d3f3310a', 'driver_only': False}, {'tool': 'ngc_acceptance_handoff_c2v005', 'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_acceptance_c2/ngc_acceptance_handoff_c2v005.py', 'sha256': '7077ad9337d48b444bb724b3d0dca531e615bbb09656fa00ba453bacf2e634b1', 'driver_only': False}, {'tool': 'ngc_lo_state_adapter_c2v003a', 'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_acceptance_c2/ngc_lo_state_adapter_c2v003a.py', 'sha256': '9c4b6dfc591cfd5c372416beb936d5d903540e5fc41e4a327b428d7ba5001eb2', 'driver_only': False}, {'tool': 'ngc_roster_recipes_c2v002', 'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_acceptance_c2/ngc_roster_recipes_c2v002.py', 'sha256': 'c700f469314d73e90cd2498cdbea5b7f69fbbd9b61676468ea5e37356939978e', 'driver_only': False}, {'tool': 'ngc_acceptance_handoff_c2v003a', 'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_acceptance_c2/ngc_acceptance_handoff_c2v003a.py', 'sha256': '7c54fd6fcc3defbc6728a35fd5125eb0d2fba23b735a38af6ac8de2094c04427', 'driver_only': False}, {'tool': 'values_writer_c2v004_cx2v002', 'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/values_writer_cx2/values_writer_c2v004_cx2v002.py', 'sha256': '26319ecbfaf944c80c5df91a0c592899727e6ff9f5177404ebc49309bd906f0e', 'driver_only': False}, {'tool': 'extract_carriers_cx3v005', 'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step5_ngc_route_ab_readiness_cx3/carriers_0606_v001/tools/extract_carriers_cx3v005.py', 'sha256': '50c7db5fbc2eb2cce17dcbb53ba1186bfdbc635a4098b0eb33ebd1402829732f', 'driver_only': False}, {'tool': 'extract_carriers_c2v001', 'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step5_path_c2/tools/extract_carriers_c2v001.py', 'sha256': '8acd21c7b8c2c1d96038a6d1eee9cbf68c25e556ae4da59bea8b70f09c1c602a', 'driver_only': False}]
DECLARED_LIST_SHA = sha(canonical(DECLARED_TOOLS))
REAL = {
    'driver': SOURCE_PINS['galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py'],
    'monitor': SOURCE_PINS['root_monitor_c2v001.py'],
    'kit': SOURCE_PINS['s0_kit_c2v003a.py'],
    'writer': SOURCE_PINS['s0_prelaunch_record_c2v001.py'],
    'twin_watch': SOURCE_PINS['twin_kill_watch_c2v003a.sh'],
    'dry_harness': SOURCE_PINS['dry_one_c2v001.py'],
    'builder': SOURCE_PINS['roster_builder_c2v006.py'],
    'orchestrator': SOURCE_PINS['calibration_orchestrator_c2v005.py'],
    'policy': SOURCE_PINS['POLICY_C2V001.json'],
    'lo': SOURCE_PINS['LO_NGC_K32_CERT_V001.json'],
    's0': SOURCE_PINS['S0_C2V001.json'],
    'caps': SOURCE_PINS['CAPS_S45_C2V003.json'],
    'spec_of_record': SOURCE_PINS['FREEZE_SPEC_OF_RECORD_C2V004.json'],
}


# Validation component. Composed after the core and the pinned source constants.
PRIMARY = "BR_A_F10_PRIMARY"
CONFIG_KEYS = (
    "schema", "python", "v006", "v006_copy_dir", "run_volume", "run_root",
    "p112_launch_root", "s0", "host_ram_bytes_expected", "plan_output_primary",
    "plan_build_record", "selection", "fdplan", "spec_of_record", "at0a_pass",
    "members", "f_points", "phase1_ceiling_utc", "phase2_ceiling_utc", "cause_records", "root_stop_records")


def theta_key(theta):
    """Verbatim algorithm of pinned orchestrator c2v005 theta_key."""
    th = {str(k): float(v) for k, v in theta.items()}
    for k, v in th.items():
        need(math.isfinite(v), "THETA_NONFINITE", k)
    return sha(canonical({"schema": "DDO154_CALIBRATION_THETA_KEY_C2V001", "theta": th}))


def dig(obj, path):
    try:
        for key in path:
            obj = obj[key]
        return obj
    except (KeyError, TypeError):
        raise Refusal("MISSING_FIELD", ".".join(path)) from None


def check_geometry(spec, seed_spec, theta_ngc=None):
    for coord, fixed in (("distance_Mpc", 13.8), ("inclination_deg", 72.0)):
        value = dig(spec, ("physical", coord))
        equal_hex(value, fixed, "geometry." + coord)
        equal_hex(value, dig(seed_spec, ("physical", coord)), "seed." + coord)
        if theta_ngc is not None:
            # The saved PLAN is authoritative. Permit the two explicit field
            # spellings; ambiguous or missing nuisance fields fail closed.
            names = [n for n in (coord, "ngc3198_" + coord) if n in theta_ngc]
            need(len(names) == 1, "PLAN_NUISANCE_FIELD", coord)
            equal_hex(value, theta_ngc[names[0]], "PLAN.theta_ngc." + names[0])


def check_derivation(theta, spec):
    physical = spec["physical"]
    values = {
        "Eref_J": theta["Eref_base_J"], "ell_F_m": theta["ell_F_m"],
        "gamma": theta["gamma_over_Eref"] * theta["Eref_base_J"],
        "common_scale_s": theta["common_scale_s"],
        "entropy_K_factor": theta["entropy_K_factor"],
    }
    for coord, expected in values.items():
        equal_hex(physical.get(coord), expected, "spec.physical." + coord)


def check_theta_hex(theta, expected):
    need(type(expected) is dict and set(theta) == set(expected), "FDPLAN_THETA_KEY_SET")
    for coord in sorted(theta):
        need(fhex(theta[coord], coord) == expected[coord], "FDPLAN_THETA_HEX", coord)


def check_member_theta(member, fd, handoff, export, spec, seed_spec, cfg, order, builder):
    identity = (member.get("log_index"), member.get("role"), order)
    need(identity == (cfg["log_index"], cfg["role"], cfg["order"]), "MEMBER_IDENTITY")
    need(member.get("member_id") == cfg["member_id"], "MEMBER_IDENTITY")
    need(fd.get("log_index") == identity[0] and fd.get("role") == identity[1], "FDPLAN_MEMBER_IDENTITY")
    need(handoff.get("log_index") == identity[0], "HANDOFF_MEMBER_IDENTITY")
    if "order" in member:
        need(member["order"] == order, "MEMBER_ORDER")
    if "order" in fd:
        need(fd["order"] == order, "FDPLAN_MEMBER_ORDER")
    points = [p for p in export.get("admitted_points", []) if p.get("log_index") == identity[0]]
    need(len(points) == 1, "EXPORT_MEMBER_NOT_UNIQUE")
    theta = member["theta_engine"]
    equal_theta(theta, points[0]["theta_natural"], "export.theta_natural")
    check_theta_hex(theta, fd["theta_hex"])
    if "theta_natural" in fd:
        equal_theta(theta, fd["theta_natural"], "fdplan.theta_natural")
    key = theta_key(theta)
    need(key == fd["key"], "FDPLAN_POINT_KEY")
    check_derivation(theta, spec)
    check_geometry(spec, seed_spec, member["theta_ngc"])
    need(all(type(v) is float and math.isfinite(v) for v in member["theta_ngc"].values()),
         "PLAN_THETA_NGC_EXACT_FLOAT")
    return {"point_key": key, "theta_sha256": builder.theta_sha256(member["theta_ngc"]),
            "identity": list(identity), "checks": ["export_bits", "fdplan_bits", "key",
                "derived_spec_bits", "gamma_IEEE_product", "geometry_bits", "parsed_PLAN_theta_ngc_hash"]}


def check_f_theta(fd, handoff, spec, seed_spec, label):
    need(fd.get("role") == label, "F_IDENTITY")
    theta = {k: float.fromhex(v) for k, v in fd["theta_hex"].items()}
    if "theta_natural" in fd:
        equal_theta(theta, fd["theta_natural"], "F.theta_natural")
    key = theta_key(theta)
    need(key == fd["key"] == handoff["point_key"], "F_POINT_KEY")
    check_derivation(theta, spec)
    check_geometry(spec, seed_spec)
    return {"point_key": key, "theta_sha256": key, "identity": label,
            "checks": ["F_theta_hex", "handoff_point_key", "derived_spec_bits", "geometry_bits"]}


def strip_leaf(spec):
    obj = copy.deepcopy(spec)
    leaf = obj["numerics"]["route_a"].pop("column_workers")
    return obj, leaf


def fill_check(handoff, handoff_pin, serial, twin, fill_receipt, key, eps, lo, schema, synthetic=False):
    need(handoff.get("schema") == schema, "HANDOFF_SCHEMA")
    want_mode = "ADMITTED" if schema == "UNT_STEP5_ADMITTED_POINT_HANDOFF_CX3V001" else "PHASE1_POINT"
    need(handoff.get("mode") == ("SYNTHETIC_DRY_ONLY" if synthetic else want_mode), "HANDOFF_MODE")
    need(handoff.get("driver_branch") == "cx3r008", "HANDOFF_DRIVER_BRANCH")
    need(handoff.get("certificate_pins") == {"eps_certificate": eps, "lo_certificate": lo},
         "HANDOFF_CERTIFICATES")
    need(fill_receipt.get("schema") == "UNT_STEP5_FILLED_SPECS_C2V001", "FILL_SCHEMA")
    need(fill_receipt.get("launch_authorized") is False, "FILL_LAUNCH_AUTHORIZED")
    need(fill_receipt.get("handoff_pin") == handoff_pin, "FILL_HANDOFF_PIN")
    need(fill_receipt.get("theta_key") == key, "FILL_POINT_KEY")
    need(fill_receipt.get("pending_certificates") == [], "FILL_PENDING_CERTIFICATES")
    for tag, spec, leaf in (("serial", serial, 1), ("twin", twin, 8)):
        need(type(dig(spec, LEAF)) is int and dig(spec, LEAF) == leaf, "SPEC_LEAF", tag)
        need(dig(spec, ("numerics", "uv_tail", "eps_certificate")) == eps, "SPEC_EPS_PIN", tag)
        need(dig(spec, ("numerics", "uv_tail", "lo_certificate")) == lo, "SPEC_LO_PIN", tag)
        need(spec.get("label") == "step5 A_K32_A2_HEADLINE theta_key=" + key, "SPEC_LABEL_KEY", tag)
    need(canonical(strip_leaf(serial)[0]) == canonical(strip_leaf(twin)[0]), "SPEC_PAIR_DIFFERENCE")
    return {"schema": "P112_FILL_CHECK_CX2V001", "ok": True, "point_key": key, "date_u": date_u()}


def dry_verdict(log, readiness, spec_pin, driver_pin):
    checks = {
        "harness_exit_0": log.get("exit") == 0,
        "no_fence_denial": log.get("blocked") == [],
        "ctx_simulate_only": bool(log.get("ctx_modes")) and set(log.get("ctx_modes")) == {"simulate"},
        "driver_sha": log.get("driver_sha256") == driver_pin["sha256"],
        "spec_sha": log.get("spec_sha256") == spec_pin["sha256"],
        "executed_stages_0": readiness.get("executed_stages") == 0,
        "binding_blockers_empty": readiness.get("binding_blockers") == [],
        "source_build_blockers_empty": readiness.get("source_build_blockers") == [],
        "future_deps_only_pending_route_a": {
            x.get("class") for x in readiness.get("future_stage_dependencies", [])} <= {"PENDING_ROUTE_A_OUTPUTS"},
        "planned_route_a": readiness.get("planned_route_a") is True,
    }
    bad = [k for k, v in checks.items() if not v]
    need(not bad, "DRY_VERDICT_REFUSED", bad)
    return {"schema": "P112_DRY_VERDICT_CX2V001", "ok": True, "checks": checks, "date_u": date_u()}


def synthetic_fence(pins, config):
    for key in ("driver", "monitor", "dry_harness"):
        need(is_pin(pins.get(key)), "SYNTHETIC_PIN_FORM", key)
        need(pins[key]["sha256"] != REAL[key]["sha256"] and
             os.path.realpath(pins[key]["path"]) != os.path.realpath(REAL[key]["path"]),
             "SYNTHETIC_REAL_TOOL", key)
    need(not re.search(r"root_monitor_c2v[0-9]+\.py", pins["monitor"]["path"]),
         "SYNTHETIC_REAL_MONITOR_NAME")
    def visit(obj):
        if isinstance(obj, str):
            need(not obj.startswith("/Volumes/") and obj != "/Volumes", "SYNTHETIC_VOLUMES")
        elif isinstance(obj, dict):
            for value in obj.values():
                visit(value)
        elif isinstance(obj, list):
            for value in obj:
                visit(value)
    visit(pins)
    visit(config)
    need(config.get("v006") != V006, "SYNTHETIC_REAL_V006")


class System:
    """Production OS interface; a synthetic subclass must fence all executable pins."""
    synthetic = False

    def mounted(self, volume):
        return os.path.realpath(volume) == volume and os.path.ismount(volume)

    def free(self, volume):
        return shutil.disk_usage(volume).free

    def ram(self):
        return int(subprocess.check_output(["/usr/sbin/sysctl", "-n", "hw.memsize"], text=True).strip())

    def processes(self):
        p = subprocess.run(["/bin/ps", "-axww", "-o", "pid=,ppid=,pgid=,command="],
                           capture_output=True, text=True, encoding="utf-8", errors="surrogateescape", timeout=30)
        need(p.returncode == 0, "PS_FAILED")
        return parse_ps(p.stdout)

    def utc(self):
        return utc()

    def monotonic(self):
        return time.monotonic()

    def sleep(self, seconds):
        time.sleep(seconds)


def mount_first(config, origin, system):
    volume = attempt_volume(config, origin)
    need(system.mounted(volume), "RUN_VOLUME_NOT_MOUNTED", volume)
    need(os.path.realpath(volume) == volume, "RUN_VOLUME_NOT_MOUNTED", volume)
    return volume


def disk_check(config, outdir, caps, system):
    volume = mount_first(config, "P112", system)
    paths = absent_paths(outdir)
    if not os.path.lexists(paths["launch_json"]) and (
            os.path.lexists(paths["receipt_stdout"]) or os.path.lexists(paths["receipt_stderr"])):
        raise Refusal("MONITOR_STARTED_NO_LAUNCH_JSON")
    need(not os.path.lexists(paths["launch_json"]), "LAUNCH_RECORD_MISSING")
    for label, path in paths.items():
        need(not os.path.lexists(path), "OUTPUT_EXISTS", label)
    free = system.free(volume)
    need(free >= caps["output_cap_bytes"] + DISK_RESERVE, "DISK_FREE")
    return {"mount_point": volume, "free_bytes": free, "required_bytes": caps["output_cap_bytes"] + DISK_RESERVE}


def read_v006(path, kind="v006_gate"):
    need(os.path.isabs(path) and os.path.realpath(path) == path, "V006_PATH")
    return observe_file(path, kind, v006=True)[0]


def compact_pin(parsed):
    return {k: parsed[k] for k in ("path", "sha256")}


class Context:
    @read_scope
    def __init__(self, config_pin, *, system=None, synthetic_pins=None):
        self.system = system or System()
        self.config_pin = config_pin
        self.cfg = read_pin(config_pin)
        c = self.cfg
        keys(c, CONFIG_KEYS, "config")
        need(c["schema"] in ("P112_CONFIG_CX2V004", "P112_CONFIG_CX3CW8V001"), "CONFIG_SCHEMA")
        validate_policy_config(c)
        need(c["python"] == PY, "CONFIG_PYTHON")
        need(c["host_ram_bytes_expected"] == RAM, "CONFIG_RAM")
        keys(c["s0"], ("launch_root", "run_root"), "config.s0")
        need(isinstance(c["p112_launch_root"], str), "PATH_ABSOLUTE_NORMALIZED", "p112_launch_root")
        need(not c["p112_launch_root"].startswith("/Volumes/"), "LAUNCH_ROOT_EXTERNAL")
        self.pins = dict(REAL)
        if synthetic_pins is not None:
            need(self.system.synthetic, "SYNTHETIC_SYSTEM_REQUIRED")
            synthetic_fence(synthetic_pins, c)
            self.pins.update(synthetic_pins)
        else:
            need(not self.system.synthetic, "SYNTHETIC_PINS_REQUIRED")
        self.synthetic = self.system.synthetic
        need(self.synthetic or c["v006"] == V006, "V006_CONFIG_PATH")
        for key in ("run_root", "p112_launch_root", "v006_copy_dir", "run_volume"):
            path_rules(c[key], key)
            need(os.path.realpath(c[key]) == c[key], "CONFIG_SYMLINK", key)
        for key in ("launch_root", "run_root"):
            path_rules(c["s0"][key], "s0." + key)
            need(os.path.realpath(c["s0"][key]) == c["s0"][key], "CONFIG_SYMLINK", "s0." + key)
        need(Path(c["run_root"]).parent == Path(c["run_volume"]) and
             Path(c["run_root"]).name.startswith("NGC_"), "RUN_ROOT_LAYOUT")
        for root in (c["run_root"], c["s0"]["run_root"]):
            need(not c["v006_copy_dir"].startswith(root + "/") and c["v006_copy_dir"] != root,
                 "CUTOFF_COPY_IN_RUN_TREE")
        READ_RUN_ROOTS.update((c["run_root"], c["s0"]["run_root"]))
        self.own_pin = pin_of(str(Path(__file__).resolve()))
        self.v006_raw = read_v006(c["v006"])
        self.v006_text = self.v006_raw.decode()
        writer = load_verified(self.pins["writer"], "_p112_verified_pin_parser")
        self.vpins = writer.parse_v006_pins(self.v006_raw)["pins"]
        self.builder = load_verified(self.pins["builder"], "_p112_verified_builder")
        self._calls = None

    def gate(self):
        return tool_gate(self.v006_text, self.own_pin)

    def residuals(self):
        return residual_lines(self.v006_text)

    def write(self, path, obj):
        path = str(path)
        path_rules(path, "output")
        kit_launches = self.cfg["s0"]["launch_root"] + "/launches"
        need(path != kit_launches and not path.startswith(kit_launches + "/"), "WRITE_KIT_LAUNCHES")
        allowed = (path.startswith(self.cfg["p112_launch_root"] + "/") or
                   path.startswith(self.cfg["v006_copy_dir"] + "/"))
        for root, origin in ((self.cfg["run_root"], "P112"), (self.cfg["s0"]["run_root"], "KIT")):
            if str(Path(path).parent) == root and path.endswith((".solo.json", ".attempt_receipt.json")):
                mount_first(self.cfg, origin, self.system)
                allowed = True
        need(allowed, "WRITE_SCOPE")
        if (type(obj) is dict and obj.get("schema") != "MONITOR_REFUSED_ATTEMPT_RECORD_C2V001"
                and not path.endswith(".observations.json")):
            obj = dict(obj, observations=observation_report())
        return write_x(path, obj)

    def record_paths(self, name=None):
        result = []
        for root, regex, origin in (
                (self.cfg["s0"]["launch_root"], KIT_ATTEMPT_RE, "KIT"),
                (self.cfg["p112_launch_root"], OWN_ATTEMPT_RE, "P112")):
            folder = Path(root) / "launches"
            if not folder.is_dir():
                continue
            for p in sorted(folder.iterdir()):
                m = regex.fullmatch(p.name)
                if m and (name is None or m["name"] == name):
                    result.append({"path": str(p), "name": m["name"], "outcome": m["kind"],
                                   "attempt": int(m["k"]), "origin": origin})
        return sorted(result, key=lambda r: (r["name"], r["attempt"], r["origin"]))

    def records(self, name=None):
        records, seen = [], set()
        for row in self.record_paths(name):
            key = row["name"], row["attempt"]
            need(key not in seen, "ATTEMPT_RECORD_NOT_UNIQUE", key)
            seen.add(key)
            pin, obj = read_record(row["path"])
            need(obj.get("name") == row["name"] and obj.get("attempt") == row["attempt"],
                 "ATTEMPT_FILENAME_BINDING")
            schema = ("UNT_P112_" + row["outcome"] + "_RECORD_CX2V001" if row["origin"] == "P112" else
                      "UNT_S0_" + row["outcome"] + "_RECORD_C2V003A")
            need(obj.get("schema") == schema, "ATTEMPT_RECORD_SCHEMA")
            records.append(dict(obj, origin=row["origin"], outcome=row["outcome"], record_pin=pin))
        return records

    def seed_check(self):
        p = Path(self.cfg["s0"]["launch_root"]) / "M15_PRELAUNCH_RECORD_C2V001.json"
        pin, obj = read_and_pin(p)
        need(obj.get("schema") == "UNT_M15_PRELAUNCH_RECORD_C2V001", "M15_SCHEMA")
        need(any(r["outcome"] == "LAUNCH" for r in self.record_paths("S0_SEED_SERIAL")
                 if r["origin"] == "KIT"), "SEED_SERIAL_NOT_LAUNCHED_FIRST")
        return pin, obj

    def kit_entries(self):
        result = {}
        folder = Path(self.cfg["s0"]["launch_root"]) / "registry"
        for name in ("S0_SEED_SERIAL", "S0_J0_SERIAL", "S0_J1_SERIAL", "S0_J2_SERIAL", TWIN):
            p = folder / (name + "_C2V003A.json")
            if not p.exists():
                continue
            pin, entry = read_and_pin(p)
            need(entry.get("schema") == "UNT_S0_LAUNCH_REGISTRY_ENTRY_C2V003A" and entry.get("name") == name,
                 "KIT_REGISTRY_SCHEMA")
            result[name] = (entry, pin)
        return result

    def get_vpin(self, kind, name):
        pin = self.vpins[kind].get(name)
        need(pin is not None, "V006_PIN_MISSING", kind + " " + name)
        return compact_pin(pin)

    def calls(self):
        if self._calls is not None:
            return self._calls
        c = self.cfg
        plan = read_pin(c["plan_output_primary"])
        build = read_pin(c["plan_build_record"])
        selection = read_pin(c["selection"])
        fd = read_pin(c["fdplan"])
        at0 = read_pin(c["at0a_pass"])
        need(at0.get("schema") == "PHASE1_AT0A_C2V001" and at0.get("outcome") == "PASS", "AT0A_NOT_PASS")
        need(build.get("status") == "BUILT" and build.get("stage") == "PLAN" and
             build.get("phase") == "PHASE_1", "PLAN_BUILD_RECORD")
        need(c["spec_of_record"] == self.pins["spec_of_record"], "SPEC_OF_RECORD")
        read_pin(c["spec_of_record"], decode=False)
        need(plan.get("ok") is True and plan.get("budget") == 0 and plan.get("evaluations_used") == 0,
             "PLAN_NOT_BUDGET_ZERO")
        members = plan.get("members")
        need(type(members) is list and members and all(m.get("evaluated") is False for m in members),
             "PLAN_NOT_VALUE_FREE")
        need(fd.get("schema") == "PHASE1_FDPLAN_C2V001", "FDPLAN_SCHEMA")
        need(len(members) == len(c["members"]) == len(fd["members"]), "MEMBER_COUNT")
        sel = selection.get("points")
        need(type(sel) is list and len(sel) == len(members), "SELECTION_MEMBERS")
        kit = self.kit_entries()
        need("S0_SEED_SERIAL" in kit, "SEED_REGISTRY_MISSING")
        seed_spec = read_pin(kit["S0_SEED_SERIAL"][0]["spec"])
        calls, seen = [], {}
        for order, (m, fdm, cfg, sm) in enumerate(zip(members, fd["members"], c["members"], sel)):
            keys(cfg, ("log_index", "role", "order", "member_id", "handoff", "fill_dir", "eps", "gq"), "member")
            need((sm.get("log_index"), sm.get("role")) == (m.get("log_index"), m.get("role")), "SELECTION_IDENTITY")
            name = "P1_M%04d" % cfg["log_index"]
            handoff = read_pin(cfg["handoff"])
            export = read_pin(handoff["source_export_pin"])
            spec, sp, fill, fc, certificate_docs = self.read_fill(cfg)
            check = check_member_theta(m, fdm, handoff, export, spec, seed_spec, cfg, order, self.builder)
            call = self.finish_call(name, cfg, handoff, spec, sp, fill, fc, check, "MEMBER", PRIMARY,
                                    m["member_id"], kit, certificate_docs)
            need(check["point_key"] not in seen, "DUPLICATE_MEMBER_POINT")
            seen[check["point_key"]] = call
            calls.append(call)
        need([f["label"] for f in c["f_points"]] == ["F0", "F1", "F2"], "F_LABELS")
        need(len(fd["F"]) == 3, "F_COUNT")
        for fdm, cfg in zip(fd["F"], c["f_points"]):
            keys(cfg, ("label", "handoff", "fill_dir", "eps", "gq"), "F")
            handoff = read_pin(cfg["handoff"])
            need(handoff.get("source_pin") == c["fdplan"], "F_SOURCE_FDPLAN")
            spec, sp, fill, fc, certificate_docs = self.read_fill(cfg)
            check = check_f_theta(fdm, handoff, spec, seed_spec, cfg["label"])
            if check["point_key"] in seen:
                # An F at an existing theta is the existing call. Validate the
                # supplied point evidence, but require no pin/entry for a call
                # that will never be launched under its own F name.
                for certificate in ("eps", "gq"):
                    need(dig(certificate_docs[certificate], ("point", "key")) == check["point_key"],
                         "CERTIFICATE_POINT_KEY", certificate)
                fill_check(handoff, cfg["handoff"], *fill, check["point_key"], cfg["eps"], self.pins["lo"],
                           "UNT_STEP5_PHASE1_POINT_HANDOFF_C2V001", self.synthetic)
                seen[check["point_key"]].setdefault("serves", []).append(cfg["label"])
                continue
            call = self.finish_call("P1_" + cfg["label"], cfg, handoff, spec, sp, fill, fc,
                                    check, "OTHER", None, cfg["label"], kit, certificate_docs)
            calls.append(call)
            seen[check["point_key"]] = call
        need(TWIN in kit, "TWIN_REGISTRY_MISSING")
        entry, ep = kit[TWIN]
        spec = read_pin(entry["spec"])
        need(entry.get("theta_key") == SEED_KEY and dig(spec, LEAF) == 8, "TWIN_REGISTRY_BINDING")
        need(entry["spec"] == self.get_vpin("SPEC_PIN", TWIN), "TWIN_SPEC_V006")
        calls.append({"name": TWIN, "kind": "OTHER", "alternative": None, "key": TWIN, "point_key": SEED_KEY,
                      "theta_sha256": SEED_KEY, "entry": entry, "entry_pin": ep, "spec": entry["spec"],
                      "spec_doc": spec, "origin": "KIT"})
        self._calls = calls
        return calls

    def read_fill(self, cfg):
        folder = path_rules(cfg["fill_dir"], "fill_dir")
        need(Path(folder).is_dir() and os.path.realpath(folder) == folder, "FILL_DIR_REAL")
        certificates = {key: read_pin(cfg[key]) for key in ("eps", "gq")}
        read_pin(self.pins["lo"], decode=False)
        sp, serial = read_and_pin(Path(folder) / SERIAL_FILE)
        _, twin = read_and_pin(Path(folder) / TWIN_FILE)
        fp, receipt = read_and_pin(Path(folder) / FILL_FILE)
        return serial, sp, (serial, twin, receipt), fp, certificates

    def finish_call(self, name, cfg, handoff, spec, spec_pin, fill, fill_pin, check, kind, alternative, key, kit, certificate_docs):
        point_key = check["point_key"]
        for certificate in ("eps", "gq"):
            obj = certificate_docs[certificate]
            need(dig(obj, ("point", "key")) == point_key, "CERTIFICATE_POINT_KEY", certificate)
        schema = ("UNT_STEP5_ADMITTED_POINT_HANDOFF_CX3V001" if kind == "MEMBER" else
                  "UNT_STEP5_PHASE1_POINT_HANDOFF_C2V001")
        fc = fill_check(handoff, cfg["handoff"], *fill, point_key, cfg["eps"], self.pins["lo"], schema, self.synthetic)
        hits = [(n, e, p) for n, (e, p) in kit.items() if n != TWIN and e.get("theta_key") == point_key]
        need(len(hits) <= 1, "KIT_POINT_DUPLICATE")
        entry, ep = None, None
        original_name = name
        if hits:
            name, entry, ep = hits[0]
            kit_spec = read_pin(entry["spec"])
            # Equal key is not sufficient: independently compare every physical bit.
            need(set(kit_spec["physical"]) == set(spec["physical"]), "KIT_PHYSICAL_KEYS")
            for coord in spec["physical"]:
                equal_hex(kit_spec["physical"][coord], spec["physical"][coord], "kit.spec." + coord)
            need(entry["spec"] == self.get_vpin("SPEC_PIN", name), "KIT_SPEC_V006")
            spec_pin, spec = entry["spec"], kit_spec
            hp = entry["v006_handoff_pin"]
        else:
            hp = self.get_vpin("HANDOFF_PIN", name)
            need(hp == cfg["handoff"], "HANDOFF_V006_PIN")
            need(spec_pin == self.get_vpin("SPEC_PIN", name), "SPEC_V006_PIN")
        return cw8_apply_choice(self, {"name": name, "configured_name": original_name, "kind": kind, "alternative": alternative, "key": key,
                "point_key": point_key, "theta_sha256": check["theta_sha256"], "theta_check": check,
                "fill_check": fc, "fill_receipt": fill_pin, "spec": spec_pin, "spec_doc": spec,
                "handoff": cfg["handoff"], "v006_handoff_pin": hp, "v006_spec_pin": self.get_vpin("SPEC_PIN", name),
                "certificates": {"eps": cfg["eps"], "gq": cfg["gq"], "lo": self.pins["lo"]},
                "entry": entry, "entry_pin": ep, "origin": "KIT" if hits else "P112"})

    def call(self, name):
        hits = [c for c in self.calls() if c["name"] == name]
        need(len(hits) == 1, "CALL_NOT_IN_ACTUAL_SET", name)
        return hits[0]


# Process qualification and the detached, validity-only sampler.


def parse_ps(text):
    rows = []
    for line in text.splitlines():
        if not line.strip():
            continue
        parts = line.strip().split(None, 3)
        need(len(parts) in (3, 4) and all(x.isdigit() for x in parts[:3]), "PS_PARSE")
        pid, ppid, pgid = map(int, parts[:3])
        need(pid > 0 and ppid >= 0 and pgid >= 0, "PS_PARSE")
        rows.append({"pid": pid, "ppid": ppid, "pgid": pgid, "command": parts[3] if len(parts) == 4 else ""})
    need(len({r["pid"] for r in rows}) == len(rows), "PS_DUPLICATE_PID")
    return rows


def command_argv(row):
    # ps renders command text; it is not shell-quoted input (0789 F-d).
    return row["command"].split()


def has_arg(command, value):
    # ps command strings do not necessarily quote paths containing spaces.
    return re.search(r"(?<!\S)" + re.escape(value) + r"(?!\S)", command) is not None


def qualified_process(rows, pid, tool, outdir, role):
    if type(pid) is not int or pid <= 1:
        return None
    for row in rows:
        if row["pid"] != pid or not has_arg(row["command"], tool):
            continue
        if role == "monitor":
            matches = has_arg(row["command"], "--receipt " + outdir + ".receipt.json")
        elif role == "sampler":
            matches = has_arg(row["command"], "_sampler") and has_arg(row["command"], "--outdir " + outdir)
        elif role == "watch":
            matches = has_arg(row["command"], "--outdir " + outdir)
        elif role == "invocation":
            matches = has_arg(row["command"], "launch")
        else:
            raise Refusal("PROCESS_ROLE")
        if matches:
            return row
    return None


def matching_monitors(rows, monitor, outdir):
    return [r for r in rows if has_arg(r["command"], monitor) and
            has_arg(r["command"], "--receipt " + outdir + ".receipt.json")]


def exact_monitor_matches(rows, argv):
    if type(argv) is not list or not argv or any(type(arg) is not str for arg in argv):
        return []
    command = " ".join(argv)
    return [row for row in rows if type(row.get("pid")) is int and row["pid"] > 1 and
            row.get("pgid") == row["pid"] and row.get("command") == command]


def record_monitor_argv(record):
    return monitor_command({"driver": record["driver"], "monitor": record["monitor"]},
                           record["spec"], record["outdir"], record["caps"])


def live_monitor(rows, pid, monitor, outdir, *, argv=None):
    if pid is not None:
        return qualified_process(rows, pid, monitor, outdir, "monitor")
    matches = exact_monitor_matches(rows, argv)
    need(len(matches) <= 1, "MULTIPLE_MONITORS")
    return matches[0] if matches else None


def descendants(rows, root):
    own = {root} if type(root) is int else set()
    changed = True
    while changed:
        before = len(own)
        own.update(r["pid"] for r in rows if r["ppid"] in own)
        changed = len(own) > before
    return own


PROCESS_IDENTITY_MAX_BYTES = 8 * 1024 * 1024


class ProcessCounter:
    def __init__(self, declared=None, synthetic=False):
        self.synthetic = synthetic
        self.declared = DECLARED_TOOLS if declared is None else declared
        self.cache = {}
        self.by_real = {os.path.realpath(t["path"]): t for t in self.declared}
        self.by_sha = {t["sha256"]: t for t in self.declared}

    def identify(self, path):
        if not os.path.isabs(path) or (self.synthetic and (path == "/Volumes" or path.startswith("/Volumes/"))):
            return None
        if os.path.realpath(path) in self.by_real:
            return self.by_real[os.path.realpath(path)]
        try:
            guard_read(path)
            # Do not inspect arbitrary data arguments. Listed tools are scripts.
            if not path.endswith((".py", ".sh")):
                return None
            st = os.stat(path)
            if not stat.S_ISREG(st.st_mode) or st.st_size > PROCESS_IDENTITY_MAX_BYTES:
                return None
            key = (path, st.st_dev, st.st_ino, st.st_mtime_ns, st.st_ctime_ns, st.st_size)
            if key not in self.cache:
                # O_NONBLOCK prevents a replacement FIFO from blocking open;
                # fstat qualifies the descriptor before any bytes are read.
                fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
                try:
                    opened = os.fstat(fd)
                    opened_key = (path, opened.st_dev, opened.st_ino, opened.st_mtime_ns,
                                  opened.st_ctime_ns, opened.st_size)
                    if (not stat.S_ISREG(opened.st_mode) or opened.st_size > PROCESS_IDENTITY_MAX_BYTES
                            or opened_key != key):
                        return None
                    with os.fdopen(fd, "rb", closefd=False) as stream:
                        raw = stream.read(PROCESS_IDENTITY_MAX_BYTES + 1)
                    if len(raw) > PROCESS_IDENTITY_MAX_BYTES:
                        return None
                    self.cache[key] = sha(raw)
                finally:
                    os.close(fd)
            return self.by_sha.get(self.cache[key])
        except (OSError, Refusal):
            return None

    def count(self, rows, own_root=None, excluded_pids=()):
        own = descendants(rows, own_root) | set(excluded_pids)
        found = []
        for row in rows:
            if row["pid"] in own:
                continue
            try:
                argv = command_argv(row)
                tool = None
                for index, arg in enumerate(argv):
                    hit = self.identify(arg)
                    if hit is None:
                        continue
                    if hit["driver_only"] and (index + 1 >= len(argv) or argv[index + 1] not in ("run", "_stage")):
                        continue
                    tool = hit
                    break
                if tool is not None:
                    found.append({"pid": row["pid"], "tool": tool["tool"]})
            except (ValueError, OSError, TypeError, KeyError):
                # A malformed/uninspectable individual command is uncounted.
                # ps acquisition/parsing still succeeded for this sample.
                continue
        return found


def monitor_command(pins, spec, outdir, caps):
    argv = [PY, "-I", "-B", pins["monitor"]["path"]]
    values = (("driver", pins["driver"]["path"]), ("driver-sha256", pins["driver"]["sha256"]),
              ("spec", spec["path"]), ("outdir", outdir), ("receipt", outdir + ".receipt.json"),
              ("wall-cap-s", str(caps["wall_cap_s"])), ("rss-cap-bytes", str(caps["rss_cap_bytes"])),
              ("output-cap-bytes", str(caps["output_cap_bytes"])))
    for flag, value in values:
        argv.extend(["--" + flag, value])
    return argv


def driver_command(pins, spec, outdir):
    return [PY, "-I", "-B", pins["driver"]["path"], "run", "--spec", spec["path"], "--outdir", outdir]


def check_monitor_command(argv, pins, spec, outdir, caps, name, column_workers=1):
    need(argv == monitor_command(pins, spec, outdir, caps), "MONITOR_ARGV")
    for value in argv:
        if value.startswith("/"):
            path_rules(value, "monitor argv")
    need(caps["rss_cap_bytes"] == cw8_rss(name, column_workers), "RSS_CAP_NOT_CALL_CAP")
    for key, value in caps.items():
        need(type(value) is int and value > 0, "CAP_FORM", key)


def validate_launch_json(lj):
    need(type(lj) is dict, "LAUNCH_JSON_FORM")
    types = {"pins": dict, "caps": dict, "command": list, "utc": str,
             "schema": str, "child_pid": int, "retries_allowed": int}
    for key, expected in types.items():
        if key in lj:
            need(type(lj[key]) is expected, "LAUNCH_JSON_FIELD_FORM", key)
    if "command" in lj:
        need(all(type(x) is str for x in lj["command"]), "LAUNCH_JSON_FIELD_FORM", "command")
    for key, value in lj.get("pins", {}).items():
        if key in ("driver", "monitor", "spec"):
            need(is_pin(value), "LAUNCH_JSON_FIELD_FORM", "pins." + key)
        elif key == "python":
            need(type(value) is str, "LAUNCH_JSON_FIELD_FORM", "pins.python")
    for key, value in lj.get("caps", {}).items():
        if key == "poll_s":
            need(type(value) in (int, float) and math.isfinite(value), "LAUNCH_JSON_FIELD_FORM", "caps.poll_s")
        elif key in ("wall_cap_s", "rss_cap_bytes", "output_cap_bytes"):
            need(type(value) in (int, float) and math.isfinite(value), "LAUNCH_JSON_FIELD_FORM", "caps." + key)
    return lj


def launch_checks(lj, plan, m15):
    validate_launch_json(lj)
    pins = lj.get("pins", {}) if type(lj) is dict else {}
    try:
        epoch = timestamp(lj.get("utc"), whole=True)
    except (Refusal, AttributeError):
        epoch = None
    return {
        "schema": type(lj) is dict and lj.get("schema") == MONITOR_SCHEMA + "_LAUNCH",
        "command_is_planned": lj.get("command") == driver_command(plan["pins"], plan["spec"], plan["outdir"]),
        "driver_pin": pins.get("driver") == plan["pins"]["driver"],
        "spec_pin": pins.get("spec") == plan["spec"],
        "monitor_pin": pins.get("monitor") == plan["pins"]["monitor"],
        "caps": type(lj.get("caps")) is dict and all(lj["caps"].get(k) == v for k, v in plan["caps"].items()),
        "rss_cap_is_call_cap": (lj.get("caps") or {}).get("rss_cap_bytes") == cw8_rss(plan["name"], cw8_plan_workers(plan)),
        "retries_0": type(lj.get("retries_allowed")) is int and lj.get("retries_allowed") == 0,
        "child_pid": type(lj.get("child_pid")) is int and lj["child_pid"] > 1,
        "m15_record_precedes_launch": epoch is not None and epoch > int(m15["date_u_epoch_s"]),
    }


def try_launch_json(path):
    # Each successful open is a distinct volatile observation. Guard failures
    # propagate; absent files may be polled without inventing a byte snapshot.
    try:
        raw, _ = observe_file(path, "launch_json")
    except OSError:
        return None, None
    try:
        doc = strict_json(raw)
    except Refusal:
        return raw, None
    return raw, validate_launch_json(doc)


def wait_launch_json(path, system, bound=300, poll=0.2):
    first = system.monotonic()
    n = 0
    while True:
        n += 1
        raw, doc = try_launch_json(path)
        elapsed = system.monotonic() - first
        if doc is not None or elapsed >= bound:
            return raw, doc, {"polls": n, "bound_s": bound, "poll_s": poll, "waited_s": elapsed}
        system.sleep(poll)


def stop_qualified(system, pid, predicate, group=False):
    """Qualification is rechecked before each signal; unrelated PID reuse is never signalled."""
    def alive():
        return next((r for r in system.processes() if r["pid"] == pid and predicate(r)), None)
    row = alive()
    if row is None:
        return "NOT_KILLED_TARGET_REFUSED"
    need(not group or row["pgid"] == pid, "NOT_GROUP_LEADER")
    send = os.killpg if group else os.kill
    try:
        send(pid, signal.SIGTERM)
    except ProcessLookupError:
        return "ALREADY_ENDED"
    until = system.monotonic() + 15
    while system.monotonic() < until and alive() is not None:
        system.sleep(0.2)
    if alive() is not None:
        try:
            send(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        result = "KILLED_KILL"
    else:
        result = "KILLED_TERM"
    until = system.monotonic() + 15
    while system.monotonic() < until and alive() is not None:
        system.sleep(0.2)
    need(alive() is None, "PROCESS_STILL_ALIVE_AFTER_STOP")
    return result


def enforce_solo(ctx, requested_solo, rows=None, requested_outdir=None, own_work=None):
    rows = ctx.system.processes() if rows is None else rows
    for rec in ctx.records():
        if not rec.get("solo_mode"):
            continue
        if live_monitor(rows, rec.get("monitor_pid"), rec["monitor"]["path"], rec["outdir"],
                        argv=record_monitor_argv(rec) if rec.get("monitor_pid") is None else None):
            raise Refusal("SOLO_RERUN_ACTIVE", rec["name"])
    # The monitor can be alive before its LAUNCH record is written. The
    # exclusive work plan closes that window, including interrupted launches.
    work_root = Path(ctx.cfg["p112_launch_root"]) / "work"
    for path in sorted(work_root.glob("*/plan.json")):
        try:
            _, plan = read_record(path)
        except (Refusal, OSError):
            raise Refusal("INFLIGHT_PLAN_UNREADABLE", str(path)) from None
        if plan.get("schema") != "UNT_P112_LAUNCH_PLAN_CX2V001":
            continue
        monitor = (plan.get("pins") or {}).get("monitor", {}).get("path", ctx.pins["monitor"]["path"])
        active_monitor = bool(matching_monitors(rows, monitor, plan["outdir"]))
        active_invocation = plan.get("invocation_pid") != os.getpid() and any(
            r["pid"] == plan.get("invocation_pid") and r["command"] == plan.get("invocation_command") for r in rows)
        if (active_monitor or active_invocation) and plan.get("solo_mode") is True:
            raise Refusal("SOLO_RERUN_ACTIVE", plan.get("name"))
        if requested_outdir == plan["outdir"]:
            active_sampler = False
            sample_start = path.parent / "sampler_first_sample.json"
            if str(path.parent) != own_work and sample_start.is_file():
                _, sample = read_record(sample_start)
                active_sampler = qualified_process(rows, sample.get("sampler_pid"), ctx.own_pin["path"],
                                                   plan["outdir"], "sampler") is not None
            if active_monitor or active_invocation or active_sampler:
                raise Refusal("INVOCATION_ALREADY_ACTIVE", plan.get("name"))
    if requested_solo:
        need(not ProcessCounter(synthetic=ctx.synthetic).count(rows), "OTHER_NGC_PROCESS_ALIVE")


@read_scope
def sampler(ctx, plan, work, poll_s=5):
    """Only monitor records are read. All outdir tests are existence checks."""
    need(type(poll_s) in (int, float) and 0 < poll_s <= 10, "SAMPLER_POLL")
    ctx.gate()
    name, k, outdir = plan["name"], plan["attempt"], plan["outdir"]
    need(plan["config"] == ctx.config_pin, "SAMPLER_CONFIG_BINDING")
    receipt, launch_path = outdir + ".receipt.json", outdir + ".receipt.json.launch.json"
    counter = ProcessCounter(synthetic=ctx.synthetic)
    first_utc = last_utc = None
    last_mono, max_gap, max_other, n = None, 0.0, 0, 0
    complete, nonzero = True, []
    own_root = None
    seen_monitor, started, ended = False, None, None
    receipt_seen_at, gone_mounted_s = None, 0.0
    last_mount_mono = None
    launch_snapshot = None
    monitor_identity = None
    bootstrap = plan
    bootstrap_pin, _ = read_record(str(Path(work) / 'plan.json'))
    committed = False
    mp = Path(work) / "monitor_pid.json"
    while True:
        tick, stamp = ctx.system.monotonic(), utc()
        ps_ok = True
        try:
            # Only failure to obtain or parse this ps observation affects
            # completeness. Command tokenization and metadata are separate.
            rows = ctx.system.processes()
        except (Refusal, OSError):
            rows = []
            ps_ok, complete = False, False
        mounted = ctx.system.mounted(ctx.cfg["run_volume"])
        if not committed:
            final = observe_launch_commit(ctx, bootstrap, bootstrap_pin, work)
            if final is not None:
                plan, final_pin = final
                committed = True
        if monitor_identity is None and mp.exists():
            _, monitor_identity = read_record(mp)
            need(type(monitor_identity) is dict and type(monitor_identity.get("monitor_pid")) is int
                 and monitor_identity["monitor_pid"] > 1, "MONITOR_PID_FORM")
            need(committed and monitor_identity.get("plan") == final_pin, "SAMPLER_FINAL_PLAN_BINDING")
        if monitor_identity is not None:
            mons = [row for row in matching_monitors(rows, ctx.pins["monitor"]["path"], outdir)
                    if row["pid"] == monitor_identity["monitor_pid"]]
        else:
            mons = exact_monitor_matches(rows, plan.get("monitor_argv"))
        # No row-count refusal: liveness probes must never terminate sampling.
        seen_monitor = seen_monitor or bool(mons)
        if mounted and launch_snapshot is None:
            raw, lj = try_launch_json(launch_path)
            if lj is not None:
                launch_snapshot = (raw, lj)
        lj = launch_snapshot[1] if launch_snapshot is not None else None
        if lj is not None:
            own_root = lj.get("child_pid")
            started = lj.get("utc")
            seen_monitor = True
        elif mons:
            own_root = mons[0]["pid"]
        other = counter.count(rows, own_root, (os.getpid(),))
        n += 1
        first_utc = stamp if first_utc is None else first_utc
        last_utc = stamp
        if last_mono is not None:
            max_gap = max(max_gap, tick - last_mono)
        last_mono = tick
        max_other = max(max_other, len(other))
        if other:
            nonzero.append({"utc": stamp, "count": len(other), "processes": other})
        if n == 1:
            ctx.write(str(Path(work) / "sampler_first_sample.json"),
                      {"schema": "P112_SAMPLER_FIRST_CX2V001", "ok": ps_ok, "utc": stamp,
                       "monotonic": ctx.system.monotonic(), "sampler_pid": os.getpid(), "date_u": date_u()})
            if not ps_ok:
                return {"status": "FIRST_SAMPLE_FAILED_NO_SOLO_FILE"}
        if mounted and ps_ok:
            if os.path.isfile(receipt):
                if receipt_seen_at is None:
                    receipt_seen_at = tick
                if not mons and tick - receipt_seen_at >= 1:
                    receipt_pin, receipt_raw = read_record(receipt, decode=False)
                    rec = monitor_receipt(receipt_raw)
                    started, ended = rec["utc_start"], rec["utc_end"]
                    result = {
                        "schema": "STEP5_SOLO_SAMPLE_CX2V001", "name": name, "attempt": k, "outdir": outdir,
                        "declared_list_sha256": DECLARED_LIST_SHA, "poll_s": poll_s, "n_samples": n,
                        "first_utc": first_utc, "last_utc": last_utc, "monitor_start_utc": started,
                        "monitor_end_utc": ended, "largest_gap_s": max_gap, "complete": complete,
                        "max_other_ngc_processes": max_other, "nonzero_samples": nonzero,
                        "own_tree_root_pid": own_root, "writer": ctx.own_pin, "date_u": date_u(),
                        "monitor_receipt": receipt_pin, "observations": observation_report()}
                    return ctx.write(outdir + ".solo.json", result)
            if not mons and seen_monitor and not os.path.lexists(launch_path):
                return {"status": "MONITOR_REFUSED_NO_SOLO_FILE"}
            if not mons and seen_monitor and not os.path.isfile(receipt):
                if last_mount_mono is not None:
                    gone_mounted_s += tick - last_mount_mono
                if gone_mounted_s >= 60:
                    return {"status": "MONITOR_ENDED_NO_RECEIPT_NO_SOLO_FILE"}
            else:
                gone_mounted_s = 0.0
            last_mount_mono = tick if not mons else None
            # Monitor can refuse before any sample observes it; the immutable
            # monitor_pid record plus an absent qualified process settles that.
            if not seen_monitor and monitor_identity is not None and not mons:
                seen_monitor = True
            inv = Path(work) / "invocation.json"
            if not seen_monitor and monitor_identity is None:
                invocation = read_record(inv)[1] if inv.exists() else plan
                ip, command = invocation.get("invocation_pid"), invocation.get("invocation_command")
                if ip is not None and command is not None and not any(
                        r["pid"] == ip and r["command"] == command for r in rows):
                    return {"status": "INVOCATION_ENDED_BEFORE_MONITOR_NO_SOLO_FILE"}
        else:
            last_mount_mono = None
        ctx.system.sleep(max(0.0, poll_s - (ctx.system.monotonic() - tick)))



# Attempt custody and history. The absence decisions all follow mount_first.


def own_registry_path(ctx, name):
    return str(Path(ctx.cfg["p112_launch_root"]) / "registry" / ("P112_" + name + "_CX2V001.json"))


def registered_entry(ctx, call):
    if call.get("entry_pin") is not None:
        return call["entry"], call["entry_pin"]
    p = own_registry_path(ctx, call["name"])
    need(Path(p).is_file(), "REGISTRY_ENTRY_MISSING", call["name"])
    pin, entry = read_record(p)
    need(entry.get("schema") == "UNT_P112_LAUNCH_REGISTRY_ENTRY_CX2V001", "REGISTRY_SCHEMA")
    need(entry.get("name") == call["name"] and entry.get("spec") == call["spec"] and
         entry.get("point_key") == call["point_key"] and entry.get("theta_sha256") == call["theta_sha256"],
         "REGISTRY_CALL_BINDING")
    cw8_check_role(call, entry.get("worker_role"))
    return entry, pin


def planned_origin(name, k, records, residuals):
    hit = [r for r in records if r["attempt"] == k]
    need(len(hit) <= 1, "ATTEMPT_RECORD_NOT_UNIQUE")
    if hit:
        return hit[0]["origin"]
    if not name.startswith("S0_"):
        return "P112"
    earlier = [r for r in records if r["attempt"] < k]
    takeover = (any(r["origin"] == "P112" or r["outcome"] == "LAUNCH" for r in earlier) or
                any(n == name and x < k for n, x in residuals))
    return "P112" if takeover else "KIT"


def planned_outdir(ctx, name, k, origin):
    need(NAME_RE.fullmatch(name) is not None and type(k) is int and k >= 1, "NAME_ATTEMPT")
    if origin == "P112":
        return str(Path(ctx.cfg["run_root"]) / ("NGC_P1_" + name + "_RUN_CX2V001_A%d" % k))
    # The kit's run_name_for spelling is NGC_P1_S0_<ROLE>_SERIAL_RUN...
    return str(Path(ctx.cfg["s0"]["run_root"]) / ("NGC_P1_" + name + "_RUN_C2V003A_A%d" % k))


def validate_record_location(ctx, rec):
    expected = planned_outdir(ctx, rec["name"], rec["attempt"], rec["origin"])
    need(rec["outdir"] == expected and rec["receipt"] == expected + ".receipt.json",
         "ATTEMPT_PATH_BINDING")
    need((rec.get("launch_json") or {}).get("path") == expected + ".receipt.json.launch.json",
         "ATTEMPT_LAUNCH_JSON_PATH")


def refusal_observations(record_path, rec):
    rule = rec.get("rule")
    matches = re.findall(r"(?:^|\s)observations_sha256=([0-9a-f]{64})(?=\s|$)", rule) if isinstance(rule, str) else []
    need(len(matches) == 1, "OBSERVATIONS_RULE_SHA")
    path = str(record_path) + ".observations.json"
    need(Path(path).is_file(), "OBSERVATIONS_SIBLING_MISSING", path)
    pin, report = read_record(path)
    need(pin["sha256"] == matches[0], "OBSERVATIONS_SIBLING_SHA", path)
    need(type(report) is dict and type(report.get("counts")) is dict and
         type(report.get("last_observation")) is dict, "OBSERVATIONS_FORM")
    counts, last = report["counts"], report["last_observation"]
    need(set(counts) == set(last), "OBSERVATIONS_FORM")
    for kind, count in counts.items():
        item = last[kind]
        need(isinstance(kind, str) and kind and type(count) is int and count >= 1 and
             type(item) is dict and item.get("kind") == kind and is_pin(item.get("pin")) and
             type(item.get("bytes")) is int and item["bytes"] >= 0, "OBSERVATIONS_FORM")
    return pin, report


def refusal_records(ctx, name, records):
    found = []
    expected_keys = ("schema", "name", "attempt", "launcher", "writer", "plan",
                     "monitor_stdout", "monitor_stderr", "absent", "date_u", "rule")
    for root, subdir, origin in ((ctx.cfg["p112_launch_root"], "launches", "P112"),
                                 (ctx.cfg["s0"]["launch_root"], "monitor_refused", "KIT")):
        folder = Path(root) / subdir
        if not folder.is_dir():
            continue
        stem = ("P112_" + name + "_MONITOR_REFUSED_CX2V001_A" if origin == "P112" else
                name + "_MONITOR_REFUSED_C2V003A_A")
        for sibling in sorted(folder.glob(stem + "*.json.observations.json")):
            if re.fullmatch(re.escape(stem) + r"([1-9][0-9]*)\.json\.observations\.json", sibling.name):
                parent = str(sibling)[:-len(".observations.json")]
                need(os.path.lexists(parent), "ORPHAN_OBSERVATIONS_SIBLING", str(sibling))
        for p in sorted(folder.glob(stem + "*.json")):
            match = re.fullmatch(re.escape(stem) + r"([1-9][0-9]*)\.json", p.name)
            if not match:
                continue
            rec_pin, rec = read_record(p)
            keys(rec, expected_keys, "monitor_refused")
            k = int(match[1])
            need(rec["schema"] == "MONITOR_REFUSED_ATTEMPT_RECORD_C2V001" and
                 rec["name"] == name and rec["attempt"] == k, "MONITOR_REFUSED_RECORD_BINDING")
            need(rec["launcher"] == ("P112_CX2V001" if origin == "P112" else "KIT_C2V003A"),
                 "MONITOR_REFUSED_LAUNCHER")
            writer = {"name": TOOL_NAME, "sha256": ctx.own_pin["sha256"]} if origin == "P112" else {
                "name": "ROOT", "sha256": None}
            need(rec["writer"] == writer, "MONITOR_REFUSED_WRITER")
            observations_pin, observations = refusal_observations(p, rec)
            guard_record(rec["plan"]["path"])
            plan = read_pin(rec["plan"])
            outdir = planned_outdir(ctx, name, k, origin)
            need(plan.get("outdir") == outdir and plan.get("attempt") == k, "MONITOR_REFUSED_PLAN")
            paths = absent_paths(outdir)
            keys(rec["absent"], paths, "monitor_refused.absent")
            need(rec["absent"] == paths, "MONITOR_REFUSED_ABSENT_PATHS")
            mount_first(ctx.cfg, origin, ctx.system)
            relaunched = (any(r["attempt"] == k for r in records) or
                          os.path.lexists(paths["receipt_stdout"]) or os.path.lexists(paths["receipt_stderr"]))
            if not relaunched:
                need(not any(os.path.lexists(p) for p in paths.values()), "MONITOR_REFUSED_ABSENT_EXISTS")
            for key in ("monitor_stdout", "monitor_stderr"):
                need(is_pin(rec[key]), "MONITOR_REFUSED_LOG_PIN_FORM")
                need(Path(rec[key]["path"]).parent == Path(rec["plan"]["path"]).parent and
                     Path(rec[key]["path"]).name == key.replace("_", ".") + ".txt",
                     "MONITOR_REFUSED_LOG_PATH")
                # 0782: permission is per refusal invocation, not the shared
                # same-k receipt paths. Hash only that old work directory.
                need(Path(rec[key]["path"]).is_file(), "WORK_LOG_MISSING")
                read_pin(rec[key], decode=False)
            found.append({"attempt": k, "origin": origin, "reason": "MONITOR_REFUSED",
                          "record_pin": rec_pin, "plan_pin": rec["plan"], "caps": plan["caps"],
                          "solo_mode": plan.get("solo_mode", False), "log_rehash_deferred": False,
                          "observations_pin": observations_pin})
    return found


def honor_residual(ctx, call, k, records, residuals, rows):
    name = call["name"]
    origin = planned_origin(name, k, records, residuals)
    mount_first(ctx.cfg, origin, ctx.system)
    outdir = planned_outdir(ctx, name, k, origin)
    paths = absent_paths(outdir)
    need(not os.path.lexists(paths["receipt"]), "RESIDUAL_RETRY_NOT_RESIDUAL")
    hits = [r for r in records if r["attempt"] == k]
    monitors = matching_monitors(rows, ctx.pins["monitor"]["path"], outdir)
    command = " ".join(driver_command(ctx.pins, call["spec"], outdir))
    need(not monitors and not any(r["command"] == command for r in rows),
         "RESIDUAL_ATTEMPT_PROCESS_ALIVE")
    if hits:
        rec = hits[0]
        need(live_monitor(rows, rec.get("monitor_pid"), rec["monitor"]["path"], outdir, argv=record_monitor_argv(rec) if rec.get("monitor_pid") is None else None) is None,
             "RESIDUAL_RETRY_NOT_RESIDUAL")
        caps, solo = rec["caps"], rec.get("solo_mode", False)
    else:
        need(not os.path.lexists(paths["launch_json"]) and (
            os.path.lexists(paths["receipt_stdout"]) or os.path.lexists(paths["receipt_stderr"])),
            "RESIDUAL_RETRY_NOT_RESIDUAL")
        prior = history(ctx, call, before=k, rows=rows, inspect_next=False)
        # The root's line admits takeover even if the prior call was kit-owned.
        if prior["actual"] or prior["trailing_nonattempt"]:
            ownership = list(prior["records"])
            if origin == "KIT" and not any(r["outcome"] == "LAUNCH" for r in ownership):
                provisional = first_caps(name)
                decision = {"caps": provisional, "solo_mode": False}
            else:
                # Historical caps come from the saved invocation, never today's clock.
                decision = saved_residual_plan(ctx, name, k, outdir)
            caps, solo = decision["caps"], decision["solo_mode"]
        else:
            if origin == 'P112':
                saved = saved_residual_plan(ctx, name, k, outdir)
                caps, solo = saved['caps'], saved['solo_mode']
            else:
                caps, solo = first_caps(name), False
    return {"attempt": k, "origin": origin, "reason": "RESIDUAL_RETRY",
            "line": "RESIDUAL_RETRY %s %d" % (name, k), "outdir": outdir,
            "caps": caps, "solo_mode": solo}



@read_scope
def history(ctx, call, *, before=None, rows=None, inspect_next=True, assembly=False, allow_incomplete=False):
    name = call["name"]
    residuals = {(n, k) for n, k in ctx.residuals() if n == name and (before is None or k < before)}
    records = [r for r in ctx.records(name) if before is None or r["attempt"] < before]
    rows = ctx.system.processes() if rows is None else rows
    actual, nonattempts, closed_pins, trailing = [], [], [], None
    pending = []
    refusals = refusal_records(ctx, name, records)
    nonattempts.extend(r for r in refusals if before is None or r["attempt"] < before)
    ks = sorted({r["attempt"] for r in records} | {k for _, k in residuals})
    for k in ks:
        hits = [r for r in records if r["attempt"] == k]
        if (name, k) in residuals:
            nonattempt = honor_residual(ctx, call, k, records, residuals, rows)
            nonattempts.append(nonattempt)
            trailing = nonattempt
            continue
        rec = hits[0]
        validate_record_location(ctx, rec)
        cw8_check_attempt(ctx, call, rec)
        mount_first(ctx.cfg, rec["origin"], ctx.system)
        receipt_path = rec["receipt"]
        if not Path(receipt_path).is_file():
            live = live_monitor(rows, rec.get("monitor_pid"), rec["monitor"]["path"], rec["outdir"], argv=record_monitor_argv(rec) if rec.get("monitor_pid") is None else None)
            state = "ATTEMPT_ACTIVE" if live else "MONITOR_ENDED_NO_RECEIPT"
            if allow_incomplete:
                pending.append({'attempt': k, 'status': state, 'record': rec['record_pin']})
                continue
            raise Refusal(state, (name, k))
        monitor_pin, monitor_raw = read_record(receipt_path, decode=False)
        monitor = monitor_receipt(monitor_raw)
        is_directory = Path(rec["outdir"]).is_dir() and os.path.realpath(rec["outdir"]) == rec["outdir"]
        spec_match = monitor.get("pins", {}).get("spec", {}).get("sha256") == call["spec"]["sha256"]
        if not is_directory or not spec_match:
            nonattempt = {"attempt": k, "origin": rec["origin"], "reason": "NO_RUN_DIRECTORY" if not is_directory else "OFF_SPEC",
                          "record_pin": rec["record_pin"], "monitor_receipt": monitor_pin,
                          "caps": rec["caps"], "solo_mode": rec.get("solo_mode", False)}
            nonattempts.append(nonattempt)
            trailing = nonattempt
            continue
        path = rec["outdir"] + ".attempt_receipt.json"
        if not Path(path).is_file() and allow_incomplete:
            pending.append({'attempt': k, 'status': 'ATTEMPT_NEEDS_CLOSE',
                            'record': rec['record_pin'], 'monitor_receipt': monitor_pin})
            continue
        need(Path(path).is_file(), "ATTEMPT_NEEDS_CLOSE", (name, k))
        pin, closed_raw = read_record(path, decode=False)
        closed_pins.append(pin)
        obj = strict_json(closed_raw)
        actual.append(verify_closed_receipt(ctx, call, rec, monitor_pin, monitor, pin, obj))
        trailing = None
    if inspect_next:
        next_k = max(ks, default=0) + 1
        origin = planned_origin(name, next_k, records, residuals)
        mount_first(ctx.cfg, origin, ctx.system)
        outdir = planned_outdir(ctx, name, next_k, origin)
        paths = absent_paths(outdir)
        if os.path.lexists(paths["launch_json"]):
            raise Refusal("LAUNCH_RECORD_MISSING", (name, next_k))
        if os.path.lexists(paths["receipt_stdout"]) or os.path.lexists(paths["receipt_stderr"]):
            raise Refusal("MONITOR_STARTED_NO_LAUNCH_JSON", (name, next_k))
    streak = 0
    # Same-k refusals are non-attempts but do not separate actual pairs.
    actual_ks = {r["attempt"] for r in actual}
    for k in sorted(set(ks) | {r["attempt"] for r in refusals}, reverse=True):
        if k in actual_ks:
            break
        streak += sum(1 for r in nonattempts if r["attempt"] == k)
    return {"records": records, "actual": actual, "closed_pins": closed_pins, "nonattempts": nonattempts,
            "residuals": residuals, "trailing_nonattempt": trailing,
            "consecutive_nonattempts": streak, "refusals": refusals, "pending": pending}



@read_scope
def record_monitor_refused(ctx, plan_pin, work):
    ctx.gate()
    guard_record(plan_pin["path"])
    plan = read_pin(plan_pin)
    need(plan.get("schema") == "UNT_P112_LAUNCH_PLAN_CX2V001", "PLAN_SCHEMA")
    need(plan["config"] == ctx.config_pin, "PLAN_CONFIG_BINDING")
    name, k, outdir = plan["name"], plan["attempt"], plan["outdir"]
    need(outdir == planned_outdir(ctx, name, k, "P112"), "PLAN_OUTDIR_BINDING")
    mount_first(ctx.cfg, "P112", ctx.system)
    paths = absent_paths(outdir)
    need(not matching_monitors(ctx.system.processes(), ctx.pins["monitor"]["path"], outdir), "MONITOR_STILL_ALIVE")
    if not os.path.lexists(paths["launch_json"]) and (
            os.path.lexists(paths["receipt_stdout"]) or os.path.lexists(paths["receipt_stderr"])):
        raise Refusal("MONITOR_STARTED_NO_LAUNCH_JSON")
    need(not any(os.path.lexists(p) for p in paths.values()), "MONITOR_REFUSED_ABSENT_EXISTS")
    path = str(Path(ctx.cfg["p112_launch_root"]) / "launches" /
               ("P112_%s_MONITOR_REFUSED_CX2V001_A%d.json" % (name, k)))
    need(not os.path.lexists(path), "MONITOR_REFUSED_TWICE")
    need(not os.path.lexists(path + ".observations.json"), "ORPHAN_OBSERVATIONS_SIBLING", path)
    need(Path(plan_pin["path"]).parent == Path(work), "MONITOR_REFUSED_WORK")
    rec = {"schema": "MONITOR_REFUSED_ATTEMPT_RECORD_C2V001", "name": name, "attempt": k,
           "launcher": "P112_CX2V001", "writer": {"name": TOOL_NAME, "sha256": ctx.own_pin["sha256"]},
           "plan": plan_pin, "monitor_stdout": pin_of(str(Path(work) / "monitor.stdout.txt")),
           "monitor_stderr": pin_of(str(Path(work) / "monitor.stderr.txt")), "absent": paths,
           "date_u": date_u(), "rule": "A223 D7: no monitor launch or output; k is not consumed."}
    report = dict(observation_report(), date_u=date_u())
    observations_pin = ctx.write(path + ".observations.json", report)
    rec["rule"] += " observations_sha256=" + observations_pin["sha256"]
    return ctx.write(path, rec)


@read_scope
def status(ctx):
    result = []
    now = ctx.system.utc()
    timestamp(now)
    ctx._policy_now_utc = now
    try:
        ctx.residuals()
    except Refusal as error:
        return {'status': error.code, 'detail': error.detail}
    for call in ctx.calls():
        try:
            hist = history(ctx, call, inspect_next=False, allow_incomplete=True)
            causes = authenticated_causes(ctx, hist['actual'])
            phase = phase_disposition(hist['actual'], call['name'],
                                      ctx.cfg['phase1_ceiling_utc'], now, causes)
            decision, problem = None, None
            if phase['status'] == 'NOT_TERMINAL':
                if hist['pending']:
                    problem = hist['pending'][-1]['status']
                else:
                    try:
                        decision = decision_for(ctx, call, hist)
                    except Refusal as error:
                        problem = error.code
            result.append({
                'name': call['name'],
                'status': problem or ('READY' if decision is not None else phase['status']),
                'attempts': [{'attempt': a['attempt'], 'raw_status': a['raw_status'],
                              'status_class': a['status_class'],
                              'nonphysics': a.get('_known_nonphysics', False)} for a in hist['actual']],
                'terminal': phase['terminal'], 'next': decision, 'phase_1': phase,
                'pending': hist['pending'], 'nonattempts': hist['nonattempts'],
                'consecutive_nonattempts': hist['consecutive_nonattempts'],
            })
        except Refusal as error:
            result.append({'name': call['name'], 'status': error.code, 'detail': error.detail})
    return {'schema': 'P112_STATUS_CX2V004', 'calls': result, 'date_u': date_u(),
            'as_of_utc': now, 'phase1_ceiling_utc': ctx.cfg['phase1_ceiling_utc'],
            'phase2_ceiling_utc': ctx.cfg['phase2_ceiling_utc'], 'stop_requested': False,
            'advisory': True, 'launch_authorized': False, 'observations': observation_report()}



# Receipt projection, actual-set registry assembly and the one cutoff copy.


def bound_stop_record(ctx, record, launch_pin):
    if record["name"] != TWIN:
        return None, None
    root = ctx.cfg["p112_launch_root"] if record["origin"] == "P112" else ctx.cfg["s0"]["launch_root"]
    folder = Path(root) / "twin_kill"
    if not folder.is_dir():
        return None, None
    hits = []
    for p in sorted(folder.glob("TWIN_KILL_RECORD_*.json")):
        # No run files are followed; these are kit records in the launch root.
        pin, doc = read_record(p)
        if doc.get("outdir") == record["outdir"]:
            need(doc.get("reason") == "ITERATION_0001_COMPLETED_AND_SIDECAR" and
                 (doc.get("launch_json") or {}).get("sha256") == launch_pin["sha256"],
                 "TWIN_STOP_NOT_BOUND")
            hits.append((doc, pin))
    need(len(hits) <= 1, "TWIN_STOP_NOT_UNIQUE")
    return hits[0] if hits else (None, None)


@read_scope
def close_attempt(ctx, name, k):
    ctx.gate()
    records = ctx.records(name)
    hits = [r for r in records if r["attempt"] == k]
    origin = planned_origin(name, k, records, ctx.residuals())
    volume = mount_first(ctx.cfg, origin, ctx.system)
    outdir = planned_outdir(ctx, name, k, origin)
    if not hits:
        need(not os.path.lexists(outdir + ".receipt.json.launch.json"), "LAUNCH_RECORD_MISSING")
        raise Refusal("ATTEMPT_RECORD_MISSING")
    need(len(hits) == 1, "ATTEMPT_RECORD_NOT_UNIQUE")
    record = hits[0]
    validate_record_location(ctx, record)
    rows = ctx.system.processes()
    if not Path(record["receipt"]).is_file():
        live = live_monitor(rows, record.get("monitor_pid"), record["monitor"]["path"], outdir, argv=record_monitor_argv(record) if record.get("monitor_pid") is None else None)
        raise Refusal("MONITOR_RECEIPT_MISSING" if live else "MONITOR_ENDED_NO_RECEIPT")
    need((name, k) not in ctx.residuals(), "RESIDUAL_RETRY_NOT_RESIDUAL")
    receipt_pin, receipt_raw = read_record(record["receipt"], decode=False)
    monitor = monitor_receipt(receipt_raw)
    if name == TWIN:
        need(qualified_process(rows, record.get("watch_pid"), ctx.pins["twin_watch"]["path"], outdir, "watch") is None,
             "TWIN_WATCH_STILL_ALIVE")
    if origin == "P112":
        need(qualified_process(rows, record.get("sampler_pid"), ctx.own_pin["path"], outdir, "sampler") is None,
             "SAMPLER_STILL_ALIVE")
    # Mapping precedes every receipt write, including kit receipts.
    call = ctx.call(name)
    entry, entry_pin = registered_entry(ctx, call)
    cw8_check_attempt(ctx, call, record)
    need(Path(outdir).is_dir() and os.path.realpath(outdir) == outdir, "NOT_AN_ATTEMPT", "NO_RUN_DIRECTORY")
    need(monitor.get("pins", {}).get("spec", {}).get("sha256") ==
         entry["spec"]["sha256"] == call.get("v006_spec_pin", call["spec"])["sha256"],
         "NOT_AN_ATTEMPT", "OFF_SPEC")
    host_ram = ctx.system.ram()
    need(host_ram == (record.get("host_ram_bytes") if origin == "P112" else RAM) == RAM, "HOST_RAM_MISMATCH")
    launch_path = outdir + ".receipt.json.launch.json"
    launch_pin, lj = read_record(launch_path)
    validate_launch_json(lj)
    need(record["launch_json"].get("sha256") in (None, launch_pin["sha256"]), "LAUNCH_JSON_RECORD_PIN")
    need(monitor.get("child_pid") == lj.get("child_pid"), "MONITOR_CHILD_BINDING")
    need(monitor.get("pins", {}).get("driver") == ctx.pins["driver"] and
         monitor.get("pins", {}).get("monitor") == ctx.pins["monitor"], "MONITOR_TOOL_PINS")
    stop, stop_pin = bound_stop_record(ctx, record, launch_pin)
    raw, cls = raw_status(monitor, name=name, attempt=k, outdir=outdir, receipt=record["receipt"],
                         launch_pin=launch_pin, child_pid=monitor["child_pid"],
                         mislaunch=record if record["outcome"] == "MISLAUNCH" else None, stop=stop)
    sample, sample_pin = None, None
    sp = outdir + ".solo.json"
    if Path(sp).is_file():
        sample_pin, sample = read_record(sp)
        need(sample.get("schema") == "STEP5_SOLO_SAMPLE_CX2V001" and
             sample.get("name") == name and sample.get("attempt") == k and sample.get("outdir") == outdir and
             sample.get("declared_list_sha256") == DECLARED_LIST_SHA, "SOLO_SAMPLE_BINDING")
        need(sample.get("monitor_receipt") == receipt_pin, "SOLO_SAMPLE_MONITOR_RECEIPT")
    timestamp(monitor["utc_end"], whole=True)
    timestamp(lj["utc"], whole=True)
    result = {
        "schema": "STEP5_ATTEMPT_RECEIPT_C2V001", "worker_role": cw8_role(call), "raw_status": raw, "status_class": cls,
        "time_utc": monitor["utc_end"], "launch_utc": lj["utc"],
        "spec_sha256": monitor["pins"]["spec"]["sha256"], "theta_sha256": call["theta_sha256"],
        "point_key": call["point_key"], **{key: monitor["caps"][key] for key in CAPS["serial"]},
        "host_ram_bytes": host_ram, "other_ngc_processes_max": sample_value(sample, monitor),
        "call": {key: call[key] for key in ("name", "kind", "alternative", "key")}, "attempt": k, "run_dir": outdir,
        "solo_mode": record.get("solo_mode", False), "counted_rerun": record.get("counted_rerun", False),
        "run_volume_at_close": {"mount_point": volume, "mounted": True, "free_bytes": ctx.system.free(volume)},
        "pins": {"monitor_receipt": receipt_pin, "launch_json": launch_pin, "launch_record": record["record_pin"],
                 "registry_entry": entry_pin, "solo_sample": sample_pin, "stop_record": stop_pin,
                 "result": monitor.get("result"), "status_map_sha256": STATUS_MAP_SHA,
                 "config": ctx.config_pin, "writer": ctx.own_pin},
        "date_u": date_u()}
    path = outdir + ".attempt_receipt.json"
    need(not os.path.lexists(path), "ATTEMPT_ALREADY_CLOSED")
    pin = ctx.write(path, result)
    cutoff = maybe_cutoff(ctx)
    return {"receipt": pin, "cutoff": cutoff, "raw_status": raw, "status_class": cls}


def terminal_set(ctx):
    terms = []
    for call in ctx.calls():
        h = history(ctx, call, inspect_next=False)
        eligible = [r for r in h['actual'] if timestamp(r['time_utc'], whole=True) <= timestamp(ctx.cfg['phase1_ceiling_utc'])]
        term = terminal_prefix(eligible, call['name'], authenticated_causes(ctx, eligible))
        if term is None:
            return None
        need(term["index"] == len(h["actual"]) - 1, "ATTEMPT_AFTER_TERMINAL", call["name"])
        receipt = h["actual"][term["index"]]
        terms.append({"name": call["name"], "time_utc": receipt["time_utc"],
                      "receipt": receipt["receipt_pin"], "disposition": term["disposition"]})
    return terms



def cutoff_path(ctx):
    return str(Path(ctx.cfg["p112_launch_root"]) / "assembly" / "STEP4_CUTOFF_RECORD_C2V001.json")


@read_scope
def write_cutoff(ctx, terms):
    ctx.gate()
    need(not os.path.lexists(cutoff_path(ctx)), "CUTOFF_ALREADY_WRITTEN")
    need(terms, "TERMINAL_SET_EMPTY")
    latest = max(terms, key=lambda t: timestamp(t["time_utc"], whole=True))["time_utc"]
    raw = read_v006(ctx.cfg["v006"], kind="v006_cutoff")
    digest = sha(raw)
    folder = Path(ctx.cfg["v006_copy_dir"])
    need(folder.is_dir() and os.path.realpath(folder) == str(folder), "CUTOFF_COPY_DIR")
    p = folder / ("V006_CUTOFF_COPY_" + digest + ".md")
    if os.path.lexists(p):
        need(p.is_file(), "CUTOFF_COPY_EXISTS_DIFFERENT")
        _, copied = read_record(p, decode=False)
        need(copied == raw, "CUTOFF_COPY_EXISTS_DIFFERENT")
    else:
        write_x_bytes(p, raw)  # The exact buffer hashed above; no source reread.
        _, copied = read_record(p, decode=False)
    need(sha(copied) == digest and len(copied) == len(raw), "CUTOFF_COPY_VERIFY")
    record = {"schema": "STEP4_CUTOFF_RECORD_C2V001", "T": latest,
              "terminal_attempt_receipts": [t["receipt"] for t in terms],
              "copy": {"path": str(p), "sha256": digest, "bytes": len(raw)},
              "precheck_summary": terms, "date_u": date_u(), "advisory": True,
              "observations": observation_report()}
    return ctx.write(cutoff_path(ctx), record)


def maybe_cutoff(ctx):
    if os.path.lexists(cutoff_path(ctx)):
        return {"status": "ALREADY_WRITTEN", "pin": pin_of(cutoff_path(ctx))}
    try:
        terms = terminal_set(ctx)
    except Refusal as e:
        return {"status": "NOT_READY", "reason": e.code}
    return write_cutoff(ctx, terms) if terms else {"status": "NOT_READY"}


def outside_stop_records(ctx, name):
    folder = Path(ctx.cfg["p112_launch_root"]) / "outside_set_stop"
    if not folder.is_dir():
        return []
    result = []
    for p in sorted(folder.glob(name + "_A*_CX2V001.json")):
        pin, doc = read_record(p)
        need(doc.get("schema") == "S0_OUTSIDE_SET_STOP_RECORD_C2V001" and doc.get("name") == name,
             "OUTSIDE_STOP_SCHEMA")
        need(doc.get("plan_output_primary") == ctx.cfg["plan_output_primary"] and
             doc.get("fdplan") == ctx.cfg["fdplan"], "OUTSIDE_STOP_MAPPING_PINS")
        result.append((doc, pin))
    return result


def registry_bytes(ctx):
    ctx.residuals()  # A malformed line refuses assembly, not just launch.
    calls, sources, mappings, excluded, nonattempts = [], [], [], [], []
    for call in ctx.calls():
        h = history(ctx, call, assembly=True)
        entry, pin = registered_entry(ctx, call)
        calls.append({"alternative": call["alternative"], "kind": call["kind"], "key": call["key"],
                      "theta_sha256": call["theta_sha256"], "spec_sha256": entry["spec"]["sha256"]})
        if is_pin(call.get("worker_choice")) and call["worker_choice"] not in sources:
            sources.append(call["worker_choice"])
        sources.extend([pin] + h["closed_pins"] + [r["record_pin"] for r in h["records"]])
        nonattempts.extend(dict(n, name=call["name"]) for n in h["nonattempts"])
        if call["origin"] == "KIT" and call["kind"] == "MEMBER":
            mappings.append({"name": call["name"], "key": call["key"], "theta_check": call["theta_check"]})
    actual_names = {c["name"] for c in ctx.calls()}
    for name, (entry, pin) in ctx.kit_entries().items():
        if name in actual_names:
            continue
        stops = outside_stop_records(ctx, name)
        need(stops, "OUTSIDE_SET_STOP_REQUIRED", name)
        excluded.append({"name": name, "registry_entry": pin, "stop_records": [p for _, p in stops]})
        sources.extend([pin] + [p for _, p in stops])
    doc = {"schema": "STEP5_LAUNCH_REGISTRY_C2V003", "phase": "PHASE_1", "calls": calls}
    evidence = {"schema": "STEP5_REGISTRY_ASSEMBLY_RECORD_CX2V001", "sources": sources,
                "plan_output_primary": ctx.cfg["plan_output_primary"], "fdplan": ctx.cfg["fdplan"],
                "selection": ctx.cfg["selection"], "plan_build_record": ctx.cfg["plan_build_record"],
                "v006_sha256": sha(ctx.v006_raw), "s0_member_mappings": mappings,
                "excluded_serials": excluded, "nonattempts": nonattempts, "date_u": date_u()}
    return encoded(doc), evidence


@read_scope
def assemble_registry(ctx, verify=False):
    ctx.gate()
    raw, evidence = registry_bytes(ctx)
    folder = Path(ctx.cfg["p112_launch_root"]) / "assembly"
    p = folder / "STEP5_LAUNCH_REGISTRY_PHASE1_CX2V001.json"
    if verify:
        need(p.is_file(), "REGISTRY_BYTE_VERIFY")
        registry_pin, registry_raw = read_record(p, decode=False)
        need(registry_raw == raw, "REGISTRY_BYTE_VERIFY")
        return {"status": "VERIFIED", "registry": registry_pin, "observations": observation_report()}
    record_path = folder / "STEP5_REGISTRY_ASSEMBLY_RECORD_CX2V001.json"
    need(not os.path.lexists(p) and not os.path.lexists(record_path), "ASSEMBLY_ALREADY_EXISTS")
    # Registry is an exact c2v006 schema and therefore cannot carry date_u.
    pin = write_x_bytes(p, raw)
    evidence["registry"] = pin
    return {"registry": pin, "assembly_record": ctx.write(str(record_path), evidence)}


# Root-invoked one-attempt launch path. No automatic retry occurs here.


def child_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("PYTHON")}
    env.update({key: "1" for key in THREAD_ENV})
    return env


def create_layout(ctx):
    root = Path(ctx.cfg["p112_launch_root"])
    need(root.is_dir() and os.path.realpath(root) == str(root), "LAUNCH_ROOT_REAL")
    for sub in ("registry", "launches", "work", "twin_kill", "outside_set_stop", "assembly"):
        p = root / sub
        if not p.exists():
            p.mkdir()
        need(p.is_dir() and os.path.realpath(p) == str(p), "LAUNCH_SUBDIR_REAL", sub)


def new_work(ctx, name, k):
    root = Path(ctx.cfg["p112_launch_root"]) / "work"
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    p = root / ("%s_A%d_%s_%d" % (name, k, stamp, os.getpid()))
    p.mkdir()
    return p


def new_log(path):
    f = open(path, "xb", buffering=0)
    f.write(("date -u: " + date_u() + "\n").encode())
    os.fsync(f.fileno())
    os.fchmod(f.fileno(), 0o444)
    return f


def run_dry(ctx, call, work):
    need(dig(read_pin(call["spec"]), LEAF) == cw8_workers(call), "CW8_DRY_EXPECTED_LEAF")
    for key in ("driver", "dry_harness"):
        read_pin(ctx.pins[key], decode=False)
    folder = Path(work) / "dry"
    folder.mkdir()
    report, log = folder / "report", folder / "log.json"
    argv = [PY, "-I", "-B", ctx.pins["dry_harness"]["path"], ctx.pins["driver"]["path"],
            ctx.pins["driver"]["sha256"], call["spec"]["path"], call["spec"]["sha256"], str(report), str(log)]
    with new_log(Path(work) / "dry.stdout.txt") as stdout:
        proc = subprocess.run(argv, env=child_env(), stdout=stdout, stderr=subprocess.STDOUT)
        os.fsync(stdout.fileno())
    need(proc.returncode == 0, "DRY_HARNESS_EXIT")
    lp, log_doc = read_record(log)
    rp, readiness_doc = read_record(report / "NGC_SOURCE_BUILD_READINESS.json")
    verdict = dry_verdict(log_doc, readiness_doc, call["spec"], ctx.pins["driver"])
    verdict.update({"worker_role": cw8_role(call), "expected_leaf": cw8_workers(call), "log": lp, "readiness": rp, "spec": call["spec"], "driver": ctx.pins["driver"]})
    return ctx.write(str(Path(work) / "dry_verdict.json"), verdict)


def watch_check(ctx):
    pin = ctx.get_vpin("WATCH_PIN", "MEMORY_WATCH")
    read_pin(pin, decode=False)
    rows = ctx.system.processes()
    need(any(has_arg(r["command"], pin["path"]) for r in rows), "MEMORY_WATCH_NOT_RUNNING")
    return pin


def own_process_command(ctx):
    rows = [r for r in ctx.system.processes() if r["pid"] == os.getpid()]
    need(len(rows) == 1, "INVOCATION_PROCESS_NOT_VISIBLE")
    return rows[0]["command"]


def make_plan(ctx, call, decision, work, m15_pin, m15):
    name, k = call["name"], decision["attempt"]
    outdir = planned_outdir(ctx, name, k, "P112")
    return {"schema": "UNT_P112_LAUNCH_PLAN_CX2V001", "name": name, "attempt": k,
            "kind": call["kind"], "alternative": call["alternative"], "key": call["key"],
            "point_key": call["point_key"], "theta_sha256": call["theta_sha256"],
            "worker_role": cw8_role(call), "spec": call["spec"], "pins": {k: ctx.pins[k] for k in ("driver", "monitor")},
            "outdir": outdir, "receipt": outdir + ".receipt.json", "launch_json": outdir + ".receipt.json.launch.json",
            "caps": decision["caps"], "caps_basis": {'rule': 'A249: Phase 1 reporting only; monitor wall uses remaining Phase 2',
                'decision_utc': decision['decision_utc'],
                'phase1_ceiling_utc': ctx.cfg['phase1_ceiling_utc'],
                'phase2_ceiling_utc': ctx.cfg['phase2_ceiling_utc'], 'phase1_requests_stop': False},
            "solo_mode": decision["solo_mode"], "counted_rerun": decision["counted_rerun"],
            "rule_c_basis": decision["rule_c_basis"], "m15_record": m15_pin,
            "m15_epoch": m15["date_u_epoch_s"], "host_ram_bytes": ctx.system.ram(),
            "config": ctx.config_pin, "work": str(work), "invocation_utc": decision["decision_utc"], "date_u": date_u(),
            "invocation_pid": os.getpid(), "invocation_command": own_process_command(ctx),
            "synthetic": ctx.synthetic, "synthetic_pins": getattr(ctx, "synthetic_pin", None),
            "monitor_argv": monitor_command(ctx.pins, call["spec"], outdir, decision["caps"])}



def register_call(ctx, call, plan, dry_pin, work, hist):
    if call["origin"] == "KIT":
        return registered_entry(ctx, call)[1]
    path = own_registry_path(ctx, call["name"])
    if os.path.lexists(path):
        old_pin, old = read_record(path)
        if hist["records"] or hist["residuals"]:
            need(old.get("spec") == call["spec"] and old.get("point_key") == call["point_key"] and
                 old.get("theta_sha256") == call["theta_sha256"] and
                 old.get("v006_spec_pin") == call["v006_spec_pin"] and
                 old.get("v006_handoff_pin") == call["v006_handoff_pin"], "REGISTRY_CALL_BINDING")
        else:
            reuse = entry_reuse(old, call, hist["records"], hist["refusals"], plan["attempt"])
            print(json.dumps({"status": reuse, "name": call["name"], "attempt": plan["attempt"],
                              "registry_entry": old_pin}, sort_keys=True), file=sys.stderr)
        cw8_check_role(call, old.get("worker_role"))
        return old_pin
    need(not hist["records"] and not hist["residuals"], "RETRY_REGISTRY_ENTRY_MISSING")
    fc_pin = ctx.write(str(Path(work) / "fill_check.json"), call["fill_check"])
    tc = dict(call["theta_check"], schema="P112_THETA_CHECK_CX2V001", date_u=date_u())
    tc_pin = ctx.write(str(Path(work) / "theta_check.json"), tc)
    record = {key: call[key] for key in (
        "name", "kind", "alternative", "key", "point_key", "theta_sha256", "spec",
        "v006_spec_pin", "v006_handoff_pin", "handoff", "certificates")}
    record.update({"worker_role": cw8_role(call), "schema": "UNT_P112_LAUNCH_REGISTRY_ENTRY_CX2V001", "plan_output_primary": ctx.cfg["plan_output_primary"],
                   "fdplan": ctx.cfg["fdplan"], "driver": ctx.pins["driver"], "fill_check": fc_pin,
                   "dry_verdict": dry_pin, "theta_check": tc_pin, "registered_at_attempt": plan["attempt"],
                   "config": ctx.config_pin, "date_u": date_u()})
    return ctx.write(path, record)


KIT_KILL_TARGET_TIMEOUT_S = 30


def kit_kill_target(ctx, plan, monitor_pid=None, *, launch_snapshot=None):
    read_pin(ctx.pins["kit"], decode=False)
    argv = [PY, "-I", "-B", ctx.pins["kit"]["path"], "kill-target", "--launch-json", plan["launch_json"],
            "--spec-sha256", plan["spec"]["sha256"], "--expect-leaf", str(cw8_plan_workers(plan))]
    if monitor_pid is not None:
        argv += ["--mon-pid", str(monitor_pid)]
    refused = {"result": "NOT_KILLED_TARGET_REFUSED", "pgid": None, "mon_pid_supplied": monitor_pid}
    try:
        p = subprocess.run(argv, env=child_env(), capture_output=True, timeout=KIT_KILL_TARGET_TIMEOUT_S)
    except (subprocess.TimeoutExpired, OSError):
        return refused
    command = " ".join(driver_command(ctx.pins, plan["spec"], plan["outdir"]))
    if p.returncode == 1:
        try:
            failure = strict_json(p.stderr)
        except Refusal:
            failure = None
        if type(failure) is dict and failure.get("alive") is False:
            if launch_snapshot is None:
                _, lj = read_record(plan["launch_json"])
            else:
                _, lj = launch_snapshot
            if lj is None:
                return refused
            validate_launch_json(lj)
            child_pid = lj.get("child_pid")
            if type(child_pid) is not int or child_pid <= 1:
                return refused
            rows = ctx.system.processes()
            if not any(r["pid"] == child_pid or r["command"] == command for r in rows):
                return {"result": "ALREADY_ENDED", "pgid": None, "mon_pid_supplied": monitor_pid}
    if p.returncode != 0 or not p.stdout.strip().isdigit():
        return refused
    pid = int(p.stdout.strip())
    predicate = lambda r: r["command"] == command and r["pgid"] == pid and (
        monitor_pid is None or r["ppid"] == monitor_pid)
    result = stop_qualified(ctx.system, pid, predicate, group=True)
    return {"result": result, "pgid": pid, "mon_pid_supplied": monitor_pid}


def stop_launch_failure(ctx, plan, monitor_pid, raw, lj):
    rows = ctx.system.processes()
    qualified = live_monitor(rows, monitor_pid, ctx.pins["monitor"]["path"], plan["outdir"],
                             argv=plan.get("monitor_argv"))
    monitor_stopped = False
    if lj is None:
        if qualified is not None:
            command = qualified["command"]
            stop_qualified(ctx.system, qualified["pid"], lambda r: r["command"] == command)
            monitor_stopped = True
        # A fresh post-bound/post-stop observation is explicitly allowed by
        # 0785. This buffer is returned for both checking and record custody.
        raw, lj = try_launch_json(plan["launch_json"])
    if lj is not None:
        stop = kit_kill_target(ctx, plan, None if monitor_stopped or qualified is None else qualified["pid"],
                               launch_snapshot=(raw, lj))
    elif os.path.lexists(plan["launch_json"]):
        command = " ".join(driver_command(ctx.pins, plan["spec"], plan["outdir"]))
        leaders = [r for r in ctx.system.processes() if r["command"] == command and r["pid"] == r["pgid"]]
        results = []
        for row in leaders:
            result = stop_qualified(ctx.system, row["pid"], lambda r: r["command"] == command and r["pid"] == r["pgid"],
                                    group=True)
            results.append({"pgid": row["pid"], "result": result})
        stop = {"result": results[-1]["result"] if results else "NOT_KILLED_TARGET_REFUSED",
                "pgid": results[-1]["pgid"] if results else None, "orphan_stops": results,
                "mon_pid_supplied": None}
    else:
        need(not matching_monitors(ctx.system.processes(), ctx.pins["monitor"]["path"], plan["outdir"]),
             "MONITOR_STILL_ALIVE")
        return None, raw, lj
    start = ctx.system.monotonic()
    while ctx.system.monotonic() - start < 60:
        mount_first(ctx.cfg, "P112", ctx.system)
        if Path(plan["receipt"]).exists():
            break
        ctx.system.sleep(0.2)
    return stop, raw, lj


def write_launch_record(ctx, plan, plan_pin, entry_pin, monitor_pid, sampler_pid, watch_pid, checks, stop=None,
                        *, snapshot, monitor_pid_source="monitor_pid.json", wait=None):
    name, k = plan["name"], plan["attempt"]
    need(not any(r["attempt"] == k for r in ctx.record_paths(name)), "ATTEMPT_ALREADY_RECORDED")
    mount_first(ctx.cfg, "P112", ctx.system)
    call = ctx.call(name)
    cw8_check_role(call, plan.get("worker_role"))
    need(name == TWIN or watch_pid is None, "CW8_FULL_CALL_TWIN_WATCHER")
    raw, lj = snapshot
    if lj is not None:
        validate_launch_json(lj)
    outcome = "LAUNCH" if checks and all(checks.values()) and stop is None else "MISLAUNCH"
    need(outcome == "LAUNCH" or os.path.lexists(plan["launch_json"]), "NO_MISLAUNCH_WITHOUT_LAUNCH_JSON")
    record = {key: plan[key] for key in ("name", "attempt", "outdir", "receipt", "spec", "caps",
              "caps_basis", "m15_record", "host_ram_bytes", "solo_mode", "counted_rerun", "rule_c_basis", "config")}
    record.update({"worker_role": cw8_role(call), "schema": "UNT_P112_" + outcome + "_RECORD_CX2V001", "outcome": outcome,
                   "launch_json": {"path": plan["launch_json"], "sha256": sha(raw) if raw is not None else None,
                                   "utc": (lj or {}).get("utc"), "child_pid": (lj or {}).get("child_pid")},
                   "driver": ctx.pins["driver"], "monitor": ctx.pins["monitor"], "monitor_pid": monitor_pid,
                   "sampler_pid": sampler_pid, "watch_pid": watch_pid, "registry_entry": entry_pin,
                   "launch_check": {"verdict": "CONFIRMED" if outcome == "LAUNCH" else "MISLAUNCH",
                                    "checks": checks, "failed": [k for k, v in checks.items() if not v]},
                   "plan": plan_pin, "status_map_sha256": STATUS_MAP_SHA, "date_u": date_u(),
                   "monitor_pid_source": monitor_pid_source, "launch_wait": wait,
                   "observations": observation_report()})
    if stop is not None:
        record["stop"] = stop
    p = Path(ctx.cfg["p112_launch_root"]) / "launches" / ("P112_%s_%s_CX2V001_A%d.json" % (name, outcome, k))
    return ctx.write(str(p), record)


@read_scope
def finish_launch(ctx, plan, plan_pin, entry_pin, monitor_pid, sampler_pid, *, resume=False,
                  monitor_pid_source="monitor_pid.json") :
    cw8_check_role(ctx.call(plan["name"]), plan.get("worker_role"))
    mount_first(ctx.cfg, "P112", ctx.system)
    m15 = read_pin(plan["m15_record"])
    raw, lj, wait = wait_launch_json(plan["launch_json"], ctx.system)
    checks = launch_checks(lj, plan, m15) if lj is not None else {"launch_json_parseable": False}
    if all(checks.values()):
        watch_pid = None
        if plan["name"] == TWIN:
            read_pin(ctx.pins["twin_watch"], decode=False)
            argv = ["/bin/bash", ctx.pins["twin_watch"]["path"], "--launch-root", ctx.cfg["p112_launch_root"],
                    "--launch-json", plan["launch_json"], "--outdir", plan["outdir"],
                    "--twin-spec-sha256", plan["spec"]["sha256"],
                    "--kill", "--max-wait-s", str(plan["caps"]["wall_cap_s"])]
            if monitor_pid is not None:
                argv += ["--mon-pid", str(monitor_pid)]
            # Resume must never start two kill watches; qualify an existing one.
            live = [r for r in ctx.system.processes() if has_arg(r["command"], ctx.pins["twin_watch"]["path"]) and
                    has_arg(r["command"], "--outdir " + plan["outdir"])]
            need(len(live) <= 1, "TWIN_WATCH_DUPLICATE")
            if live:
                watch_pid = live[0]["pid"]
            elif not resume or not Path(plan["receipt"]).exists():
                with new_log(Path(plan["work"]) / ("twin_watch_resume.stdout.txt" if resume else "twin_watch.stdout.txt")) as f:
                    watch_pid = subprocess.Popen(argv, env=child_env(), stdout=f, stderr=subprocess.STDOUT,
                                                 start_new_session=True).pid
        return write_launch_record(ctx, plan, plan_pin, entry_pin, monitor_pid, sampler_pid, watch_pid, checks,
                                   snapshot=(raw, lj), monitor_pid_source=monitor_pid_source, wait=wait)
    within_bound = lj is not None
    stop, raw, lj = stop_launch_failure(ctx, plan, monitor_pid, raw, lj)
    if stop is None:
        return record_monitor_refused(ctx, plan_pin, plan["work"])
    checks = launch_checks(lj, plan, m15) if lj is not None else {"launch_json_parseable": False}
    checks["launch_json_within_bound"] = within_bound
    return write_launch_record(ctx, plan, plan_pin, entry_pin, monitor_pid, sampler_pid, None, checks, stop,
                               snapshot=(raw, lj), monitor_pid_source=monitor_pid_source, wait=wait)


@read_scope
def launch_resume(ctx, name, k):
    ctx.gate()
    mount_first(ctx.cfg, "P112", ctx.system)
    need(not any(r["attempt"] == k for r in ctx.record_paths(name)), "ATTEMPT_ALREADY_RECORDED")
    outdir = planned_outdir(ctx, name, k, "P112")
    need(os.path.lexists(outdir + ".receipt.json.launch.json"), "RESUME_LAUNCH_JSON_MISSING")
    candidates = []
    refused_plans = {r["plan_pin"]["path"] for r in refusal_records(ctx, name, ctx.records(name))}
    for p in (Path(ctx.cfg["p112_launch_root"]) / "work").glob(name + "_A%d_*/plan.json" % k):
        if str(p) in refused_plans:
            continue
        pin, plan = read_record(p)
        inv = p.parent / "invocation.json"
        mp = p.parent / "monitor_pid.json"
        if plan.get("name") == name and plan.get("attempt") == k and inv.is_file():
            plan, pin = read_launch_commit(ctx, plan, pin, p.parent)
            invocation = read_record(inv)[1]
            monitor_record = read_record(mp)[1] if mp.is_file() else None
            candidates.append((plan["invocation_utc"], plan, pin, invocation, monitor_record))
    need(candidates, "RESUME_INVOCATION_MISSING")
    _, plan, pin, invocation, mp = max(candidates, key=lambda x: x[0])
    need(plan["config"] == ctx.config_pin and plan["outdir"] == outdir and
         invocation["planned_monitor_argv"] == plan["monitor_argv"] and
         invocation.get("plan") == pin and (mp is None or mp.get("plan") == pin) and
         plan["pins"] == {key: ctx.pins[key] for key in ("driver", "monitor")}, "RESUME_PLAN_BINDING")
    rows = ctx.system.processes()
    need(isinstance(invocation.get("invocation_command"), str), "RESUME_INVOCATION_COMMAND_MISSING")
    need(not any(r["pid"] == invocation["invocation_pid"] and r["command"] == invocation["invocation_command"]
                 for r in rows), "RESUME_INVOCATION_ALIVE")
    call = ctx.call(name)
    entry, entry_pin = registered_entry(ctx, call)
    need(plan["spec"] == call["spec"], "RESUME_SPEC_BINDING")
    cw8_check_role(call, plan.get("worker_role"))
    if mp is None:
        matches = exact_monitor_matches(rows, plan.get("monitor_argv"))
        need(len(matches) <= 1, "MULTIPLE_MONITORS")
        monitor_pid = matches[0]["pid"] if matches else None
        pid_source = "command_line" if matches else "no_live_match"
    else:
        monitor_pid, pid_source = mp["monitor_pid"], "monitor_pid.json"
    return finish_launch(ctx, plan, pin, entry_pin, monitor_pid, invocation["sampler_pid"], resume=True,
                         monitor_pid_source=pid_source)



@read_scope
def launch(ctx, name, attempt=None, dry=False, resume=False):
    ctx._policy_now_utc = ctx.system.utc()
    timestamp(ctx._policy_now_utc)
    if resume:
        need(not dry and type(attempt) is int, "RESUME_ARGUMENTS")
        return launch_resume(ctx, name, attempt)
    if not dry:
        ctx.gate()
    ctx.residuals()
    m15_pin, m15 = ctx.seed_check()
    call = ctx.call(name)
    if not dry:
        call = cw8_ensure_default(ctx, call)
    hist = history(ctx, call)
    decision = decision_for(ctx, call, hist)
    need(attempt is None or attempt == decision["attempt"], "ATTEMPT_NUMBER")
    outdir = planned_outdir(ctx, name, decision["attempt"], "P112")
    disk = disk_check(ctx.cfg, outdir, decision["caps"], ctx.system)
    need(ctx.system.ram() == RAM, "HOST_RAM_MISMATCH")
    watch_check(ctx)
    enforce_solo(ctx, decision["solo_mode"], requested_outdir=outdir)
    for key in ("driver", "monitor"):
        read_pin(ctx.pins[key], decode=False)
    check_monitor_command(monitor_command(ctx.pins, call["spec"], outdir, decision["caps"]),
                          ctx.pins, call["spec"], outdir, decision["caps"], name, cw8_workers(call))
    create_layout(ctx)
    work = new_work(ctx, name, decision["attempt"])
    plan = make_plan(ctx, call, decision, work, m15_pin, m15)
    plan["disk_check"] = disk
    plan["dry_only"] = bool(dry)
    plan_pin = ctx.write(str(work / "plan.json"), plan)
    dry_pin = run_dry(ctx, call, work)
    if dry:
        return {"status": "DRY_NOT_LAUNCHED", "plan": plan_pin, "dry_verdict": dry_pin}
    entry_pin = register_call(ctx, call, plan, dry_pin, work, hist)
    sampler_argv = [PY, "-I", "-B", ctx.own_pin["path"], "_sampler", "--config", ctx.config_pin["path"],
                    "--config-sha256", ctx.config_pin["sha256"], "--plan", plan_pin["path"],
                    "--plan-sha256", plan_pin["sha256"], "--outdir", outdir, "--poll-s", "5"]
    if getattr(ctx, "synthetic_pin", None):
        sampler_argv += ["--synthetic-pins", ctx.synthetic_pin["path"], "--synthetic-pins-sha256", ctx.synthetic_pin["sha256"]]
    with new_log(work / "sampler.stdout.txt") as f:
        sampler_pid = subprocess.Popen(sampler_argv, env=child_env(), stdout=f, stderr=subprocess.STDOUT,
                                       start_new_session=True).pid
    first_path = work / "sampler_first_sample.json"
    start = ctx.system.monotonic()
    while not first_path.exists() and ctx.system.monotonic() - start < 60:
        ctx.system.sleep(0.05)
    need(first_path.is_file(), "SAMPLER_FIRST_SAMPLE_MISSING")
    _, first = read_record(first_path)
    need(first.get("ok") is True, "SAMPLER_FIRST_SAMPLE_FAILED")
    remaining = 1.0 - (ctx.system.monotonic() - first["monotonic"])
    if remaining > 0:
        ctx.system.sleep(remaining)
    # Recheck all resource and solo predicates immediately before this single launch.
    disk_check(ctx.cfg, outdir, decision["caps"], ctx.system)
    enforce_solo(ctx, decision["solo_mode"], requested_outdir=outdir, own_work=str(work))
    # A249: bind one final argv after dry checks and sampler startup.
    plan, plan_pin = write_launch_commit(ctx, plan, plan_pin, work, ctx.system.utc())
    invocation = {"schema": "P112_INVOCATION_CX2V001", "invocation_pid": os.getpid(),
                  "invocation_command": plan["invocation_command"],
                  "sampler_pid": sampler_pid, "planned_monitor_argv": plan["monitor_argv"],
                  "plan": plan_pin, "date_u": date_u()}
    ctx.write(str(work / "invocation.json"), invocation)
    with new_log(work / "monitor.stdout.txt") as so, new_log(work / "monitor.stderr.txt") as se:
        argv = ["/usr/bin/nohup"] + plan["monitor_argv"]
        proc = subprocess.Popen(argv, env=child_env(), stdout=so, stderr=se, start_new_session=True)
    ctx.write(str(work / "monitor_pid.json"), {"schema": "P112_MONITOR_PID_CX2V001",
              "monitor_pid": proc.pid, "plan": plan_pin, "date_u": date_u()})
    if not ctx.synthetic:
        subprocess.Popen(["/usr/bin/caffeinate", "-i", "-w", str(proc.pid)],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    return finish_launch(ctx, plan, plan_pin, entry_pin, proc.pid, sampler_pid)



# Command surface and explicit synthetic execution fence.


class SyntheticSystem(System):
    synthetic = True

    def __init__(self, fixture):
        keys(fixture, ("mount_points", "free_bytes", "host_ram_bytes"), "synthetic.system")
        self.fixture = fixture
        for p in fixture["mount_points"]:
            path_rules(p, "synthetic mount")
            need(not p.startswith("/Volumes"), "SYNTHETIC_VOLUMES")

    def mounted(self, volume):
        return volume in self.fixture["mount_points"] and Path(volume).is_dir() and os.path.realpath(volume) == volume

    def free(self, volume):
        return self.fixture["free_bytes"]

    def ram(self):
        return self.fixture["host_ram_bytes"]


@read_scope
def stop_outside_set(ctx, name, attempt=None):
    ctx.gate()
    need(name in ("S0_SEED_SERIAL", "S0_J0_SERIAL", "S0_J1_SERIAL", "S0_J2_SERIAL"), "OUTSIDE_STOP_NAME")
    need(name not in {c["name"] for c in ctx.calls()}, "OUTSIDE_STOP_IN_ACTUAL_SET")
    records = ctx.records(name)
    need(records, "OUTSIDE_STOP_NO_RECORD")
    record = max(records, key=lambda r: r["attempt"]) if attempt is None else next(
        (r for r in records if r["attempt"] == attempt), None)
    need(record is not None, "OUTSIDE_STOP_ATTEMPT")
    mount_first(ctx.cfg, record["origin"], ctx.system)
    validate_record_location(ctx, record)
    entry, entry_pin = ctx.kit_entries()[name]
    read_pin(entry["spec"])
    need(entry["spec"] == ctx.get_vpin("SPEC_PIN", name), "OUTSIDE_STOP_SPEC_PIN")
    plan = {"name": name, "launch_json": record["outdir"] + ".receipt.json.launch.json",
            "outdir": record["outdir"], "spec": entry["spec"]}
    result = kit_kill_target(ctx, plan, record["monitor_pid"])
    need(result["result"] != "NOT_KILLED_TARGET_REFUSED", "OUTSIDE_STOP_TARGET_REFUSED")
    rec = {"schema": "S0_OUTSIDE_SET_STOP_RECORD_C2V001", "name": name, "attempt": record["attempt"],
           "launch_json": read_record(plan["launch_json"], decode=False)[0], "outdir": record["outdir"], "pgid": result["pgid"],
           "result": result["result"], "plan_output_primary": ctx.cfg["plan_output_primary"],
           "fdplan": ctx.cfg["fdplan"], "rule": "A133 L103: outputs kept and never read.", "date_u": date_u()}
    p = Path(ctx.cfg["p112_launch_root"]) / "outside_set_stop" / (
        "%s_A%d_CX2V001.json" % (name, record["attempt"]))
    return ctx.write(str(p), rec)


@read_scope
def cli(argv=None):
    ap = argparse.ArgumentParser(description="P-112: root-invoked Phase-1 custody, A248/A249; no Phase-1 boundary stop.")
    ap.add_argument("command", choices=("launch", "close-attempt", "assemble-registry", "stop-outside-set",
                                        "record-monitor-refused", "status", "_sampler", "select-workers"))
    ap.add_argument("--config", required=True)
    ap.add_argument("--config-sha256", required=True)
    ap.add_argument("--name")
    ap.add_argument("--forecast")
    ap.add_argument("--forecast-sha256")
    ap.add_argument("--attempt", type=int)
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--plan")
    ap.add_argument("--plan-sha256")
    ap.add_argument("--outdir")
    ap.add_argument("--work")
    ap.add_argument("--poll-s", type=float, default=5)
    ap.add_argument("--synthetic-pins")
    ap.add_argument("--synthetic-pins-sha256")
    args = ap.parse_args(argv)
    try:
        synthetic_pin, overrides, system = None, None, None
        if args.synthetic_pins:
            synthetic_pin = {"path": args.synthetic_pins, "sha256": args.synthetic_pins_sha256}
            data = read_pin(synthetic_pin)
            keys(data, ("schema", "pins", "system", "date_u"), "synthetic manifest")
            need(data["schema"] == "P112_SYNTHETIC_PINS_CX2V001", "SYNTHETIC_SCHEMA")
            overrides, system = data["pins"], SyntheticSystem(data["system"])
        else:
            need(args.synthetic_pins_sha256 is None, "SYNTHETIC_SHA_WITHOUT_FILE")
        ctx = Context({"path": args.config, "sha256": args.config_sha256}, system=system, synthetic_pins=overrides)
        ctx.synthetic_pin = synthetic_pin
        need(not args.dry or args.command == "launch", "DRY_COMMAND")
        need(not args.resume or args.command == "launch", "RESUME_COMMAND")
        need(not args.verify or args.command == "assemble-registry", "VERIFY_COMMAND")
        if args.command in ("launch", "close-attempt", "stop-outside-set"):
            need(args.name is not None and NAME_RE.fullmatch(args.name), "NAME_REQUIRED")
        need(args.command == "select-workers" or (args.forecast is None and args.forecast_sha256 is None), "CW8_FORECAST_COMMAND")
        if args.command == "select-workers":
            need(args.name is None and args.attempt is None and not args.dry and not args.resume, "CW8_SELECT_ARGUMENTS")
            need((args.forecast is None) == (args.forecast_sha256 is None), "CW8_FORECAST_ARGUMENTS")
            forecast = ({"path": args.forecast, "sha256": args.forecast_sha256}
                        if args.forecast is not None else None)
            result = select_workers(ctx, forecast)
        elif args.command == "launch":
            result = launch(ctx, args.name, args.attempt, args.dry, args.resume)
        elif args.command == "close-attempt":
            need(type(args.attempt) is int and args.attempt >= 1, "ATTEMPT_REQUIRED")
            result = close_attempt(ctx, args.name, args.attempt)
        elif args.command == "assemble-registry":
            result = assemble_registry(ctx, args.verify)
        elif args.command == "stop-outside-set":
            result = stop_outside_set(ctx, args.name, args.attempt)
        elif args.command == "record-monitor-refused":
            need(args.plan and args.plan_sha256 and args.work, "REFUSAL_ARGUMENTS")
            result = record_monitor_refused(ctx, {"path": args.plan, "sha256": args.plan_sha256}, args.work)
        elif args.command == "_sampler":
            need(args.plan and args.plan_sha256 and args.outdir, "SAMPLER_ARGUMENTS")
            guard_record(args.plan)
            plan = read_pin({"path": args.plan, "sha256": args.plan_sha256})
            need(plan["outdir"] == args.outdir, "SAMPLER_OUTDIR")
            result = sampler(ctx, plan, plan["work"], poll_s=args.poll_s)
        else:
            result = status(ctx)
        print(json.dumps(result, sort_keys=True, allow_nan=False))
        return 0
    except (Refusal, OSError, KeyError, TypeError, ValueError) as e:
        print(json.dumps({"status": "REFUSED", "code": e.code if isinstance(e, Refusal) else type(e).__name__,
                          "detail": str(e)}, sort_keys=True))
        return 2




MODEL_FAILURE_CODES = frozenset({
    'ROUTE_A_NO_FIXED_POINT', 'ITERATION_BUDGET_EXHAUSTED',
})


MODEL_DRIVER_STATUSES = frozenset({
    'ROUTE_A_NO_FIXED_POINT', 'FAILED', 'FAILED_AT_STAGE',
})


LAUNCH_COMMIT_SCHEMA = 'P112_LAUNCH_COMMIT_CX2V004'


CAUSE_KEYS = ('status', 'failing_stage', 'failure_code', 'exception_class', 'raise_site',
              'bound_shas', 'model_outcome', 'model_outcome_reason')


CAUSE_SHA_KEYS = ('receipt', 'result', 'finish', 'spec', 'driver')


KNOWN_NONPHYSICS_CAUSES = frozenset({
    'NONPHYSICS_OR_NOT_FAILED', 'SIGNAL_OR_EXIT_UNAUTHENTICATED',
    'A248_EXCLUDED_SOURCE_PREPARATION', 'SIGNAL_KILLED_STAGE',
})


PHASE1_CEILING_UTC = '2026-11-06T05:59:00Z'


PHASE2_CEILING_UTC = '2026-12-01T05:59:00Z'



def saved_residual_plan(ctx, name, k, outdir):
    found = []
    root = Path(ctx.cfg['p112_launch_root']) / 'work'
    for path in sorted(root.glob(name + '_A%d_*/plan.json' % k)):
        inv = path.parent / 'invocation.json'
        if not inv.is_file():
            continue
        pin, plan = read_record(path)
        plan, pin = read_launch_commit(ctx, plan, pin, path.parent)
        _, invocation = read_record(inv)
        need(invocation.get('plan') == pin and invocation.get('planned_monitor_argv') == plan['monitor_argv'],
             'RESIDUAL_PLAN_BINDING')
        if plan.get('name') == name and plan.get('attempt') == k and plan.get('outdir') == outdir:
            found.append(plan)
    need(len(found) == 1, 'RESIDUAL_PLAN_NOT_UNIQUE')
    return found[0]


def _authenticated_identity(receipt, authenticated):
    if receipt.get('_known_nonphysics') or receipt.get('status_class') != 'FAILED':
        return None
    pin = receipt.get('receipt_pin')
    if not is_pin(pin) or not isinstance(authenticated, dict):
        return None
    evidence = authenticated.get((pin['path'], pin['sha256']))
    if not isinstance(evidence, dict) or set(evidence) != {'cause', 'cause_pin', 'monitor_receipt'}:
        return None
    cause = evidence['cause']
    if not is_pin(evidence['cause_pin']) or not is_pin(evidence['monitor_receipt']) or \
            type(cause) is not dict or set(cause) != set(CAUSE_KEYS) or cause['model_outcome'] is not True:
        return None
    bound = cause['bound_shas']
    if type(bound) is not dict or set(bound) != set(CAUSE_SHA_KEYS) or \
            not all(isinstance(bound[k], str) and HEX64.fullmatch(bound[k]) for k in CAUSE_SHA_KEYS):
        return None
    if bound['receipt'] != evidence['monitor_receipt']['sha256'] or \
            bound['spec'] != receipt['spec_sha256'] or \
            receipt.get('raw_status') != 'CHILD_FAILED|' + str(cause['status']) or \
            cause['status'] != 'ROUTE_A_NO_FIXED_POINT' or cause['failure_code'] not in MODEL_FAILURE_CODES:
        return None
    fields = ('status', 'failing_stage', 'failure_code', 'exception_class', 'raise_site')
    if any(not isinstance(cause[k], str) or not cause[k] for k in fields):
        return None
    return (bound['spec'], bound['driver']) + tuple(cause[k] for k in fields)


def held_for_fix(actual):
    if len(actual) < 2:
        return False
    a, b = actual[-2:]
    return (b.get('raw_status') in ('CHILD_FAILED|REFUSED', 'CHILD_FAILED|BLOCKED') and
            a.get('raw_status') == b['raw_status'] and
            a.get('spec_sha256') == b.get('spec_sha256'))


def held_for_cause(actual, authenticated_causes=None):
    if len(actual) < 2 or held_for_fix(actual):
        return False
    a, b = actual[-2:]
    if a.get('_known_nonphysics') or b.get('_known_nonphysics'):
        return False
    if not (a.get('status_class') == b.get('status_class') == 'FAILED' and
            a.get('raw_status') == b.get('raw_status') and
            a.get('raw_status') != 'CHILD_FAILED|NONE|EXIT' and
            a.get('spec_sha256') == b.get('spec_sha256')):
        return False
    if any(r.get('solo_mode') is not True or type(r.get('other_ngc_processes_max')) is not int
           or r['other_ngc_processes_max'] != 0 for r in (a, b)):
        return False
    # Only an authentication adapter supplies this map. A validated non-model
    # decision may occupy its key with None; absent/unauthenticated is missing.
    known = authenticated_causes if isinstance(authenticated_causes, dict) else {}
    return any(not is_pin(r.get('receipt_pin')) or
               (r['receipt_pin']['path'], r['receipt_pin']['sha256']) not in known for r in (a, b))


def remaining_wall(ceiling_utc, now_utc):
    remaining = math.floor(timestamp(ceiling_utc, whole=True) - timestamp(now_utc))
    need(remaining > 0, 'UNEVALUATED_SCHEDULE_CEILING')
    return remaining


def phase_disposition(actual, name, phase_ceiling_utc, now_utc, authenticated_causes=None):
    """A reporting snapshot only; it never requests a process stop."""
    cutoff = timestamp(phase_ceiling_utc, whole=True)
    eligible = [r for r in actual if timestamp(r['time_utc'], whole=True) <= cutoff]
    term = terminal_prefix(eligible, name, authenticated_causes)
    if term is not None:
        return {'status': 'TERMINAL', 'terminal': term, 'stop_requested': False}
    hold = ('HELD_FOR_FIX' if held_for_fix(actual) else
            'HELD_FOR_CAUSE' if held_for_cause(actual, authenticated_causes) else None)
    if hold is not None:
        return {'status': hold, 'terminal': None, 'stop_requested': False}
    if timestamp(now_utc) >= cutoff:
        return {'status': 'UNEVALUATED_SCHEDULE_CEILING', 'terminal': None,
                'continues_for_next_phase': True, 'stop_requested': False}
    return {'status': 'NOT_TERMINAL', 'terminal': None, 'stop_requested': False}


def fresh_launch_plan(ctx, bootstrap, now_utc):
    seconds = remaining_wall(ctx.cfg['phase2_ceiling_utc'], now_utc)
    need(seconds <= bootstrap['caps']['wall_cap_s'], 'LAUNCH_CLOCK_MOVED_BACKWARD')
    plan = copy.deepcopy(bootstrap)
    plan['caps']['wall_cap_s'] = seconds
    plan['caps_basis'] = {
        'rule': 'A249: Phase 1 reporting only; monitor wall uses remaining Phase 2',
        'decision_utc': now_utc,
        'phase1_ceiling_utc': ctx.cfg['phase1_ceiling_utc'],
        'phase2_ceiling_utc': ctx.cfg['phase2_ceiling_utc'],
        'phase1_requests_stop': False,
    }
    plan['invocation_utc'] = now_utc
    plan['date_u'] = date_u()
    plan['monitor_argv'] = monitor_command(ctx.pins, plan['spec'], plan['outdir'], plan['caps'])
    return plan


def _commit_plan_check(ctx, bootstrap, bootstrap_pin, commit, plan, plan_pin, work):
    keys(commit, ('schema', 'bootstrap_plan', 'launch_plan', 'date_u', 'observations'), 'launch commit')
    need(commit['schema'] == LAUNCH_COMMIT_SCHEMA and commit['bootstrap_plan'] == bootstrap_pin and
         commit['launch_plan'] == plan_pin, 'LAUNCH_COMMIT_BINDING')
    need(plan_pin['path'] == str(Path(work) / 'launch_plan.json'), 'LAUNCH_COMMIT_RESIDENCE')
    changed = {'caps', 'caps_basis', 'invocation_utc', 'date_u', 'monitor_argv', 'observations'}
    need(set(plan) - {'observations'} == set(bootstrap) - {'observations'} and all(
        plan[k] == bootstrap[k] for k in plan if k not in changed), 'LAUNCH_COMMIT_FIXED_FIELDS')
    need(set(plan['caps']) == set(bootstrap['caps']) and all(
        plan['caps'][k] == bootstrap['caps'][k] for k in plan['caps'] if k != 'wall_cap_s'),
        'LAUNCH_COMMIT_MACHINE_CAPS')
    basis = plan['caps_basis']
    keys(basis, ('rule', 'decision_utc', 'phase1_ceiling_utc', 'phase2_ceiling_utc',
                 'phase1_requests_stop'), 'launch caps basis')
    need(basis['phase1_ceiling_utc'] == ctx.cfg['phase1_ceiling_utc'] and
         basis['phase2_ceiling_utc'] == ctx.cfg['phase2_ceiling_utc'] and
         basis['phase1_requests_stop'] is False and
         basis['decision_utc'] == plan['invocation_utc'], 'LAUNCH_COMMIT_CEILINGS')
    need(timestamp(plan['invocation_utc']) >= timestamp(bootstrap['invocation_utc']),
         'LAUNCH_CLOCK_MOVED_BACKWARD')
    need(plan['caps']['wall_cap_s'] == remaining_wall(
        ctx.cfg['phase2_ceiling_utc'], basis['decision_utc']) and
        plan['caps']['wall_cap_s'] <= bootstrap['caps']['wall_cap_s'], 'LAUNCH_COMMIT_WALL')
    need(plan['monitor_argv'] == monitor_command(ctx.pins, plan['spec'], plan['outdir'], plan['caps']),
         'LAUNCH_COMMIT_ARGV')
    return plan, plan_pin


@read_scope
def write_launch_commit(ctx, bootstrap, bootstrap_pin, work, now_utc):
    ctx.gate()
    work = str(Path(work))
    need(bootstrap_pin['path'] == str(Path(work) / 'plan.json'), 'LAUNCH_BOOTSTRAP_RESIDENCE')
    need(bootstrap['config'] == ctx.config_pin and bootstrap['work'] == work, 'LAUNCH_BOOTSTRAP_BINDING')
    saved_pin, saved_bootstrap = read_record(bootstrap_pin['path'])
    need(saved_pin == bootstrap_pin and
         {k: v for k, v in saved_bootstrap.items() if k != 'observations'} ==
         {k: v for k, v in bootstrap.items() if k != 'observations'}, 'LAUNCH_BOOTSTRAP_BYTES')
    path = str(Path(work) / 'LAUNCH_COMMIT.json')
    final_path = str(Path(work) / 'launch_plan.json')
    need(not os.path.lexists(path) and not os.path.lexists(final_path), 'LAUNCH_COMMIT_EXISTS')
    plan = fresh_launch_plan(ctx, bootstrap, now_utc)
    pin = ctx.write(final_path, plan)
    # Context.write adds only the observation report. Verify the actual saved
    # bytes and use them for all subsequent bindings.
    checked_pin, checked = read_record(final_path)
    need(pin == checked_pin, 'LAUNCH_COMMIT_SAVED_PLAN')
    commit = {
        'schema': LAUNCH_COMMIT_SCHEMA, 'bootstrap_plan': bootstrap_pin,
        'launch_plan': checked_pin, 'date_u': date_u(),
    }
    ctx.write(path, commit)
    _, saved_commit = read_record(path)
    return _commit_plan_check(ctx, bootstrap, bootstrap_pin, saved_commit, checked, checked_pin, work)


def read_launch_commit(ctx, bootstrap, bootstrap_pin, work, *, snapshot=None):
    path = str(Path(work) / 'LAUNCH_COMMIT.json')
    if snapshot is None:
        _, commit = read_record(path)
    else:
        commit = snapshot
    need(type(commit) is dict and is_pin(commit.get('launch_plan')), 'LAUNCH_COMMIT_FORM')
    # Validate residence before following the pin.
    need(commit['launch_plan']['path'] == str(Path(work) / 'launch_plan.json'), 'LAUNCH_COMMIT_RESIDENCE')
    pin, raw = read_record(commit['launch_plan']['path'], decode=False)
    need(pin == commit['launch_plan'], 'LAUNCH_COMMIT_PIN')
    plan = strict_json(raw)
    return _commit_plan_check(ctx, bootstrap, bootstrap_pin, commit, plan, pin, work)


def observe_launch_commit(ctx, bootstrap, bootstrap_pin, work):
    """One volatile poll; a validated commit is thereafter reused by sampler."""
    path = str(Path(work) / 'LAUNCH_COMMIT.json')
    if not os.path.lexists(path):
        return None
    raw, _ = observe_file(path, 'launch_commit')
    try:
        commit = strict_json(raw)
    except Refusal as exc:
        if exc.code == 'JSON_PARSE':
            return None
        raise
    return read_launch_commit(ctx, bootstrap, bootstrap_pin, work, snapshot=commit)


def read_cause_inputs(ctx):
    result = {}
    for pin in ctx.cfg['cause_records']:
        cause = read_pin(pin)
        keys(cause, CAUSE_KEYS, 'value-free cause')
        keys(cause['bound_shas'], CAUSE_SHA_KEYS, 'cause bindings')
        need(type(cause['model_outcome']) is bool and
             isinstance(cause['model_outcome_reason'], str), 'CAUSE_FORM')
        for key in ('status', 'failing_stage', 'failure_code', 'exception_class', 'raise_site'):
            need(cause[key] is None or isinstance(cause[key], str), 'CAUSE_FORM', key)
        for key, value in cause['bound_shas'].items():
            need(value is None or isinstance(value, str) and HEX64.fullmatch(value), 'CAUSE_SHA_FORM', key)
        receipt_sha = cause['bound_shas']['receipt']
        need(receipt_sha is not None and receipt_sha not in result, 'CAUSE_RECEIPT_NOT_UNIQUE')
        result[receipt_sha] = (cause, pin)
    return result


def authenticated_causes(ctx, actual):
    """Map bound causes; explicit non-model records release cause holds without counting."""
    inputs = read_cause_inputs(ctx)
    mapped = {}
    for receipt in actual:
        pin = receipt['receipt_pin']
        key = (pin['path'], pin['sha256'])
        monitor = receipt['_verified_monitor']
        if receipt.get('_known_nonphysics'):
            mapped[key] = None
            continue
        source = inputs.get(receipt['pins']['monitor_receipt']['sha256'])
        if source is None:
            continue
        cause, source_pin = source
        bindings = cause['bound_shas']
        need(bindings['spec'] == receipt['spec_sha256'] and
             bindings['driver'] == monitor['pins']['driver']['sha256'], 'CAUSE_SCIENCE_BINDING')
        need(cause['status'] == monitor.get('driver_status'), 'CAUSE_STATUS_BINDING')
        if bindings['result'] is not None:
            need(is_pin(monitor.get('result')) and bindings['result'] == monitor['result']['sha256'],
                 'CAUSE_RESULT_BINDING')
        if not cause['model_outcome']:
            # A270: retain the pinned record, but release an uncounted solo
            # retry even when its reason awaits later readable classification.
            mapped[key] = None
            continue
        need(all(isinstance(bindings[k], str) and HEX64.fullmatch(bindings[k])
                 for k in CAUSE_SHA_KEYS), 'CAUSE_BOUND_SHA_MISSING')
        need(cause['failure_code'] in MODEL_FAILURE_CODES and
             cause['status'] == 'ROUTE_A_NO_FIXED_POINT' and
             all(isinstance(cause[k], str) and bool(cause[k])
                 for k in ('failing_stage', 'exception_class', 'raise_site')),
             'CAUSE_MODEL_IDENTITY')
        need(monitor.get('status') == 'CHILD_FAILED' and
             monitor.get('stop_reason') is None and type(monitor.get('exit_code')) is int and
             monitor['exit_code'] > 0 and monitor['exit_code'] not in (137, 143), 'CAUSE_NONPHYSICS_END')
        mapped[key] = {'cause': cause, 'cause_pin': source_pin,
                       'monitor_receipt': receipt['pins']['monitor_receipt']}
    return mapped


def bound_root_stop(ctx, receipt):
    """Explicit root stop evidence preempts natural completion and a planned twin stop."""
    hits = []
    for pin in ctx.cfg['root_stop_records']:
        doc = read_pin(pin)
        keys(doc, ('schema', 'date_u', 'call', 'launch_json', 'registration'), 'root stop')
        need(doc['schema'] == 'ROOT_NONPHYSICS_STOP_C2V001', 'ROOT_STOP_SCHEMA')
        if doc['launch_json'] != receipt['pins']['launch_json']:
            continue
        need(doc['call'] == receipt['call'], 'ROOT_STOP_CALL_BINDING')
        need(timestamp(receipt['launch_utc'], whole=True) <= timestamp(doc['date_u']) <= timestamp(receipt['time_utc'], whole=True), 'ROOT_STOP_OUTSIDE_ATTEMPT')
        read_pin(doc['registration'], decode=False)
        hits.append(pin)
    need(len(hits) <= 1, 'ROOT_STOP_NOT_UNIQUE')
    return hits[0] if hits else None


def verify_closed_receipt(ctx, call, record, monitor_pin, monitor, closed_pin, obj):
    """Reproduce the policy-bearing projection from adjacent custody records only."""
    name, k, outdir = record['name'], record['attempt'], record['outdir']
    verified_workers = cw8_check_attempt(ctx, call, record, obj)
    need(obj.get('schema') == 'STEP5_ATTEMPT_RECEIPT_C2V001' and
         obj.get('call') == {key: call[key] for key in ('name', 'kind', 'alternative', 'key')} and
         obj.get('attempt') == k and obj.get('run_dir') == outdir and
         obj.get('spec_sha256') == call['spec']['sha256'] and
         obj.get('theta_sha256') == call['theta_sha256'] and
         obj.get('point_key') == call['point_key'], 'ATTEMPT_RECEIPT_BINDING')
    launch_pin, launch = read_record(outdir + '.receipt.json.launch.json')
    validate_launch_json(launch)
    need(record['launch_json'].get('sha256') in (None, launch_pin['sha256']), 'LAUNCH_JSON_RECORD_PIN')
    need(monitor.get('child_pid') == launch.get('child_pid'), 'MONITOR_CHILD_BINDING')
    need(all(launch.get('pins', {}).get(key) == monitor.get('pins', {}).get(key) for key in ('driver', 'monitor', 'spec')) and
         all(launch.get('caps', {}).get(key) == monitor['caps'].get(key) == record['caps'].get(key) for key in CAPS['serial']), 'LAUNCH_MONITOR_METADATA_BINDING')
    need(monitor.get('pins', {}).get('driver') == record['driver'] == ctx.pins['driver'] and
         monitor.get('pins', {}).get('monitor') == record['monitor'] == ctx.pins['monitor'], 'MONITOR_TOOL_PINS')
    stop, stop_pin = bound_stop_record(ctx, record, launch_pin)
    raw, cls = raw_status(monitor, name=name, attempt=k, outdir=outdir, receipt=record['receipt'],
                         launch_pin=launch_pin, child_pid=monitor['child_pid'],
                         mislaunch=record if record['outcome'] == 'MISLAUNCH' else None, stop=stop)
    sample, sample_pin = None, None
    sp = outdir + '.solo.json'
    if Path(sp).is_file():
        sample_pin, sample = read_record(sp)
        need(sample.get('schema') == 'STEP5_SOLO_SAMPLE_CX2V001' and
             sample.get('name') == name and sample.get('attempt') == k and sample.get('outdir') == outdir and
             sample.get('declared_list_sha256') == DECLARED_LIST_SHA and
             sample.get('monitor_receipt') == monitor_pin, 'SOLO_SAMPLE_BINDING')
    expected = dict(raw_status=raw, status_class=cls, time_utc=monitor['utc_end'],
                    launch_utc=launch['utc'], host_ram_bytes=RAM,
                    other_ngc_processes_max=sample_value(sample, monitor),
                    solo_mode=record.get('solo_mode', False),
                    counted_rerun=record.get('counted_rerun', False),
                    **{key: monitor['caps'][key] for key in CAPS['serial']})
    need(all(obj.get(key) == value and type(obj.get(key)) is type(value)
             for key, value in expected.items()), 'ATTEMPT_PROJECTION_MISMATCH')
    pins = obj.get('pins', {})
    need(pins.get('monitor_receipt') == monitor_pin and pins.get('launch_json') == launch_pin and
         pins.get('launch_record') == record['record_pin'] and pins.get('solo_sample') == sample_pin and
         pins.get('stop_record') == stop_pin and pins.get('result') == monitor.get('result') and
         pins.get('status_map_sha256') == STATUS_MAP_SHA, 'ATTEMPT_SOURCE_BINDING')
    timestamp(monitor['utc_end'], whole=True)
    root_stop = bound_root_stop(ctx, obj)
    ex = monitor.get('exit_code')
    # A legitimate watch record overrides its own signal only. An explicit
    # root stop, missing/invalid exit, or a monitor stop without watch is nonphysics.
    nonphysics = bool(root_stop) or (cls != 'PLANNED_STOP' and (
        monitor.get('stop_reason') is not None or type(ex) is not int or ex < 0 or ex in (137, 143)))
    nonphysics = nonphysics or raw == 'CHILD_FAILED|NONE|EXIT' or cls in ('CAP', 'OUTPUT_CAP', 'INFRA')
    return dict(obj, receipt_pin=closed_pin, _verified_monitor=monitor,
                _verified_column_workers=verified_workers,
                _known_nonphysics=nonphysics, _root_stop=root_stop)


def validate_policy_config(config):
    need(config['phase1_ceiling_utc'] == PHASE1_CEILING_UTC and
         config['phase2_ceiling_utc'] == PHASE2_CEILING_UTC, 'PHASE_CEILING_CONFIG')
    for field in ('cause_records', 'root_stop_records'):
        pins = config[field]
        need(type(pins) is list and all(is_pin(p) for p in pins), 'POLICY_INPUT_PINS', field)
        need(len({p['path'] for p in pins}) == len(pins), 'POLICY_INPUT_DUPLICATE', field)
        for pin in pins:
            guard_record(pin['path'])


def command_now(ctx):
    if not hasattr(ctx, '_policy_now_utc'):
        ctx._policy_now_utc = ctx.system.utc()
        timestamp(ctx._policy_now_utc)
    return ctx._policy_now_utc


def decision_for(ctx, call, hist, *, now_utc=None):
    need(not hist.get('pending'), 'ATTEMPT_INCOMPLETE', hist.get('pending'))
    return next_attempt(call['name'], hist['records'], hist['actual'], hist['residuals'],
                        hist['trailing_nonattempt'],
                        phase_ceiling_utc=ctx.cfg['phase1_ceiling_utc'],
                        monitor_ceiling_utc=ctx.cfg['phase2_ceiling_utc'],
                        now_utc=command_now(ctx) if now_utc is None else now_utc,
                        authenticated_causes=authenticated_causes(ctx, hist['actual']),
                        has_monitor_refusal=bool(hist.get('refusals')), column_workers=cw8_workers(call))


# Conditional full-call cw8 execution policy, composed without runtime imports.
CW8_SOURCE_PINS = {'driver': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py', 'sha256': '577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377'}, 'comparator': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step5_path_c2/tools/compare_identity_pair_c2v001.py', 'sha256': '8e857fff5c2bc16574238cd4fb5c2c510815efe60764f6027d9addd944be0178'}, 'checkpoint_module': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v003.py', 'sha256': '069b393560003fc200932e2d17fa84ee750043fa2132f2cadd459915fb99b114'}, 'serial_worker': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/prep_loader_fix/ngc43_coupled_root_worker_uvtail_ro1_cx3v011_r5cx3v001_cx3v005.py', 'sha256': 'ee27227c2cee3093589ae6b6546a0d88a1bbe20c47ba4dacff497ad7cc80189f'}, 'parallel_worker': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/prep_loader_fix/ngc43_coupled_root_worker_parallel_uvtail_ro1_cx3v011_r5cx3v001_cx3v005.py', 'sha256': '293a417f493fee2b59176bc60873fa3cdea5e586f375efbe51cbd10651e045b1'}, 'serial_solver': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/route_a/coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_uvtail_c2v001.py', 'sha256': '8ef3079b0a23c32c688605e96eb5b79beb79768578cc7aef22ea087c7ae12469'}, 'parallel_solver': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/route_a/coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_parallel_uvtail_c2v001.py', 'sha256': '7667025bd9382a58688153fde98bf90f2b67d27baa39a939982631c305c229db'}}

"""Source component for the P112 successor; composed into its verified namespace.

No import side effects. Every runtime input goes through P112's single-buffer
reader. Only metadata selection is added; the root retains launch ownership.
"""

CW8_LICENSE_SCHEMA = "CW8_PHASE1_LICENSE_CX3V001"
CW8_FORECAST_SCHEMA = "CW8_PHASE1_FORECAST_CX3V001"
CW8_CHOICE_SCHEMA = "CW8_PHASE1_CHOICE_CX3V001"
CW8_EQUAL = "SERIAL_EQUALS_PARALLEL_BITWISE_TAIL_ON"
CW8_RSS_MULTIPLIER = 11  # A177/A260 accounting, accepted in 0825; requires the root license.
CW8_MAX_FORECAST_AGE_S = 900
CW8_SCOPE_KEYS = ("plan_output_primary", "plan_build_record", "selection", "fdplan",
                  "spec_of_record", "at0a_pass", "members", "f_points")
CW8_COSTS = {
    "expectation": {"serial_h": 31.90, "parallel_a_h": 5.84, "parallel_tail_h": 15.74},
    "upper": {"serial_h": 84.77, "parallel_a_h": 17.52, "parallel_tail_h": 34.33},
}

# CW8_SOURCE_PINS is inserted by the build script, from exact source bytes.


def cw8_scope(ctx):
    return {key: ctx.cfg[key] for key in CW8_SCOPE_KEYS}


def cw8_root_license_pin(text):
    """One exact root registration, inside an A-numbered section."""
    section, found = None, []
    for line in text.splitlines():
        if line.startswith("## "):
            match = re.match(r"## (A[0-9]+)(?=[:\s]|$)", line)
            section = match[1] if match else None
        if not line.startswith("CW8_LICENSE_PIN"):
            continue
        match = re.fullmatch(r"CW8_LICENSE_PIN path=(/.*\S) sha256=([0-9a-f]{64})", line)
        need(match is not None and section is not None, "CW8_LICENSE_REGISTRATION_FORM")
        found.append({"path": match[1], "sha256": match[2]})
    need(len(found) <= 1, "CW8_LICENSE_REGISTRATION_DUPLICATE")
    return found[0] if found else None


def cw8_leaf_span(raw):
    """Locate the JSON value structurally, without reserializing any other byte."""
    text = raw.decode("utf-8")
    strict_json(raw)  # Duplicate keys and nonfinite numbers refuse first.
    decoder, spans = json.JSONDecoder(), []

    def ws(i):
        while i < len(text) and text[i] in " \t\r\n":
            i += 1
        return i

    def walk(i, path):
        i = ws(i)
        start = i
        if text[i] == "{":
            i = ws(i + 1)
            while text[i] != "}":
                key, i = decoder.raw_decode(text, i)
                i = ws(i)
                need(text[i] == ":", "CW8_SPEC_JSON")
                i = ws(walk(i + 1, path + (key,)))
                if text[i] == "}":
                    break
                need(text[i] == ",", "CW8_SPEC_JSON")
                i = ws(i + 1)
            end = i + 1
        elif text[i] == "[":
            i, index = ws(i + 1), 0
            while text[i] != "]":
                i = ws(walk(i, path + (index,)))
                index += 1
                if text[i] == "]":
                    break
                need(text[i] == ",", "CW8_SPEC_JSON")
                i = ws(i + 1)
            end = i + 1
        else:
            _, end = decoder.raw_decode(text, i)
        if path == LEAF:
            spans.append((len(text[:start].encode("utf-8")),
                          len(text[:end].encode("utf-8"))))
        return end

    walk(0, ())
    need(len(spans) == 1, "CW8_SPEC_LEAF_NOT_UNIQUE")
    return spans[0]


def cw8_spec_pair(serial_raw, parallel_raw):
    serial, parallel = strict_json(serial_raw), strict_json(parallel_raw)
    need(type(dig(serial, LEAF)) is int and dig(serial, LEAF) == 1, "CW8_SERIAL_LEAF")
    need(type(dig(parallel, LEAF)) is int and dig(parallel, LEAF) == 8, "CW8_PARALLEL_LEAF")
    start, end = cw8_leaf_span(serial_raw)
    need(serial_raw[start:end] == b"1" and
         serial_raw[:start] + b"8" + serial_raw[end:] == parallel_raw,
         "CW8_NONWORKER_BYTES_CHANGED")
    return parallel


def cw8_authenticate(ctx, license_pin):
    """A root-pinned comparator attestation, never its underlying run trees."""
    need(is_pin(license_pin), "CW8_LICENSE_MISSING")
    need(cw8_root_license_pin(ctx.v006_text) == license_pin, "CW8_LICENSE_NOT_ROOT_PINNED")
    obj = read_pin(license_pin)
    keys(obj, ("schema", "date_u", "scope", "comparator_record", "source_pins",
               "seed_serial_spec", "seed_twin_spec", "full_rss_multiplier"), "cw8 license")
    need(obj["schema"] == CW8_LICENSE_SCHEMA and obj["scope"] == "FULL_MEMBER_F_CALLS_ONLY",
         "CW8_LICENSE_SCOPE")
    need(type(obj["full_rss_multiplier"]) is int and
         obj["full_rss_multiplier"] == CW8_RSS_MULTIPLIER, "CW8_RSS_RULING_REQUIRED")
    need(obj["source_pins"] == CW8_SOURCE_PINS, "CW8_WORKER_SOURCE_PINS")
    need(ctx.pins["driver"] == CW8_SOURCE_PINS["driver"], "CW8_DRIVER_PIN")
    serial_pin = ctx.get_vpin("SPEC_PIN", "S0_SEED_SERIAL")
    twin_pin = ctx.get_vpin("SPEC_PIN", TWIN)
    need(obj["seed_serial_spec"] == serial_pin and obj["seed_twin_spec"] == twin_pin,
         "CW8_SEED_SPEC_PINS")
    # Verify the seed pair's actual spec bytes without opening either run.
    cw8_spec_pair(read_pin(serial_pin, decode=False), read_pin(twin_pin, decode=False))
    record = read_pin(obj["comparator_record"])
    need(type(record) is dict, "CW8_COMPARATOR_FORM")
    need(record.get("schema") == "UNT_STEP5_NGC_IDENTITY_PAIR_RECORD_C2V001",
         "CW8_COMPARATOR_SCHEMA")
    need(record.get("verdict") == CW8_EQUAL, "CW8_COMPARATOR_" + str(record.get("verdict")))
    need(record.get("bitwise_equal") is True, "CW8_COMPARATOR_NOT_BITWISE_EQUAL")
    need(record.get("iterations_compared") == [0, 1] and
         all(type(x) is int for x in record["iterations_compared"]), "CW8_TWO_ITERATIONS_REQUIRED")
    expected = {"driver": CW8_SOURCE_PINS["driver"],
                "checkpoint_module": CW8_SOURCE_PINS["checkpoint_module"],
                "tool": CW8_SOURCE_PINS["comparator"],
                "serial_spec": serial_pin, "twin_spec": twin_pin}
    need(record.get("pins") == expected, "CW8_COMPARATOR_PINS")
    checks = record.get("checks")
    need(type(checks) is dict and checks and all(v is True for v in checks.values()) and
         record.get("differing_files") == [] and record.get("not_ready") == [] and
         record.get("values_printed") is False, "CW8_COMPARATOR_CHECKS")
    # The comparator attests worker/solver custody. Verify the fixed source bytes
    # as well; none is imported or executed by this authorization check.
    for source_pin in CW8_SOURCE_PINS.values():
        read_pin(source_pin, decode=False)
    return obj


def cw8_schedule(n, available_cores, workers, cost):
    """0818 uniform-call planning model: eight-core A then one-core tail."""
    need(type(n) is int and 1 <= n <= 3, "CW8_MODEL_COHORT_OUT_OF_SCOPE")
    need(type(available_cores) is int and 12 <= available_cores <= 18,
         "CW8_MODEL_LOAD_OUT_OF_SCOPE")
    if workers == 1:
        return cost["serial_h"]  # At most three calls, at least twelve cores.
    need(workers == 8, "CW8_MODEL_WORKERS")
    # All tails retain a core immediately when their A stage finishes. An A
    # completion releases seven cores. The next A starts only if eight are free.
    time, pending, active, completion = 0.0, n, [], []
    while pending or active:
        busy = sum(item[1] for item in active)
        while pending and busy + 8 <= available_cores:
            active.append((time + cost["parallel_a_h"], 8, "A"))
            busy += 8
            pending -= 1
        need(active, "CW8_MODEL_NO_FEASIBLE_SCHEDULE")
        time = min(item[0] for item in active)
        ended, active = ([x for x in active if x[0] == time],
                         [x for x in active if x[0] != time])
        for _, cores, stage in ended:
            if stage == "A":
                active.append((time + cost["parallel_tail_h"], 1, "TAIL"))
            else:
                completion.append(time)
    return max(completion)


def cw8_predict(forecast, names, now_utc):
    keys(forecast, ("schema", "date_u", "observed_utc", "calls", "host_cores",
                    "cores_in_use", "remaining_barrier_h", "scope"), "cw8 forecast")
    need(forecast["schema"] == CW8_FORECAST_SCHEMA, "CW8_FORECAST_SCHEMA")
    need(type(forecast["calls"]) is list and forecast["calls"] == sorted(names),
         "CW8_FORECAST_CALL_SET")
    need(forecast["host_cores"] == 18 and type(forecast["host_cores"]) is int,
         "CW8_MODEL_HOST")
    used = forecast["cores_in_use"]
    need(type(used) is int and 0 <= used <= 6, "CW8_MODEL_LOAD_OUT_OF_SCOPE")
    age = timestamp(now_utc) - timestamp(forecast["observed_utc"])
    need(0 <= age <= CW8_MAX_FORECAST_AGE_S, "CW8_FORECAST_STALE_OR_FUTURE")
    barrier = forecast["remaining_barrier_h"]
    need(type(barrier) is dict and set(barrier) == set(CW8_COSTS),
         "CW8_FORECAST_BARRIER")
    predictions = {}
    for scenario, cost in CW8_COSTS.items():
        r = barrier[scenario]
        need(type(r) in (int, float) and math.isfinite(r) and r >= 0, "CW8_FORECAST_BARRIER")
        serial = max(r, cw8_schedule(len(names), 18 - used, 1, cost))
        parallel = max(r, cw8_schedule(len(names), 18 - used, 8, cost))
        predictions[scenario] = {
            "serial_makespan_h": serial, "cw8_makespan_h": parallel,
            "predicted_saving_h": serial - parallel,
        }
    # No gain hidden behind S0 and no expectation/upper tradeoff.
    choose = all(v["predicted_saving_h"] > 0 for v in predictions.values())
    return {"column_workers": 8 if choose else 1,
            "reason": "PREDICTED_MAKESPAN_SHORTER" if choose else "NO_STRICT_MAKESPAN_GAIN",
            "scenarios": predictions, "model": "0818_UNIFORM_CALLS_1_TO_3_CORES_12_TO_18",
            "measured_speedup": False}


def cw8_choice_directory(ctx):
    return Path(ctx.cfg["p112_launch_root"]) / "worker_choices"


def cw8_saved_choices(ctx):
    directory = cw8_choice_directory(ctx)
    if not directory.exists():
        return {}
    need(directory.is_dir() and os.path.realpath(directory) == str(directory), "CW8_CHOICE_DIRECTORY")
    found = {}
    for path in sorted(directory.glob("CHOICE_*.json")):
        pin, doc = read_record(path)
        need(doc.get("schema") == CW8_CHOICE_SCHEMA and doc.get("scope") == cw8_scope(ctx),
             "CW8_CHOICE_SCOPE")
        need(doc.get("producer") == ctx.own_pin, "CW8_CHOICE_PRODUCER")
        rows = doc.get("calls")
        need(type(rows) is list and rows, "CW8_CHOICE_CALLS")
        for row in rows:
            name = row.get("name")
            need(type(name) is str and NAME_RE.fullmatch(name) and not name.startswith("S0_"),
                 "CW8_CHOICE_NAME")
            need(name not in found, "CW8_CHOICE_DUPLICATE", name)
            found[name] = (row, doc, pin)
    return found


def cw8_apply_choice(ctx, call):
    if call["origin"] != "P112":
        return call  # S0 ownership and worker/spec history are unchanged.
    found = cw8_saved_choices(ctx)
    if call["name"] not in found:
        return call
    row, doc, choice_pin = found[call["name"]]
    keys(row, ("name", "point_key", "theta_sha256", "serial_spec", "spec",
               "column_workers"), "cw8 choice row")
    need(row["serial_spec"] == call["spec"] and row["point_key"] == call["point_key"] and
         row["theta_sha256"] == call["theta_sha256"], "CW8_CHOICE_CALL_BINDING")
    workers = row["column_workers"]
    need(type(workers) is int and workers in (1, 8), "CW8_CHOICE_WORKERS")
    if workers == 1:
        need(row["spec"] == call["spec"], "CW8_SERIAL_SPEC_CHANGED")
    else:
        cw8_authenticate(ctx, doc.get("license"))
        forecast = read_pin(doc["forecast"])
        need(forecast.get("scope") == cw8_scope(ctx), "CW8_FORECAST_SCOPE")
        prediction = cw8_predict(forecast, [r["name"] for r in doc["calls"]],
                                 doc["selected_at_utc"])
        need(prediction == doc.get("prediction") and prediction["column_workers"] == 8 and
             all(r.get("column_workers") == 8 for r in doc["calls"]), "CW8_CHOICE_NOT_DERIVED")
        chosen_pin = ctx.get_vpin("SPEC_PIN", call["name"] + "_FULL_CW8")
        need(row["spec"] == chosen_pin, "CW8_FULL_SPEC_ROOT_PIN")
        chosen_spec = cw8_spec_pair(read_pin(call["spec"], decode=False),
                                    read_pin(chosen_pin, decode=False))
        call = dict(call, spec=chosen_pin, spec_doc=chosen_spec, v006_spec_pin=chosen_pin)
    return dict(call, worker_choice=choice_pin, serial_spec=row["serial_spec"])


def cw8_workers(call):
    workers = dig(call["spec_doc"], LEAF)
    need(type(workers) is int and workers in (1, 8), "CW8_WORKER_LEAF")
    if call["name"] == TWIN:
        need(workers == 8 and call["origin"] == "KIT", "CW8_TWIN_IDENTITY")
    elif workers == 8:
        need(call["origin"] == "P112" and is_pin(call.get("worker_choice")),
             "CW8_FULL_CALL_UNAUTHORIZED")
    return workers


def cw8_role(call):
    return {"kind": "IDENTITY_TWIN" if call["name"] == TWIN else "FULL",
            "column_workers": cw8_workers(call), "choice": call.get("worker_choice")}


def cw8_check_role(call, saved, *, allow_legacy=True):
    expected = cw8_role(call)
    if saved is None and allow_legacy and call.get("worker_choice") is None:
        return expected  # Original serial or authentic S0 twin custody.
    need(saved == expected, "CW8_ROLE_CUSTODY")
    return expected


def cw8_rss(name, workers=1):
    need(type(workers) is int and workers in (1, 8), "CW8_RSS_WORKERS")
    return RAM * (CW8_RSS_MULTIPLIER if name == TWIN or workers == 8 else 1)


def cw8_plan_workers(plan):
    role = plan.get("worker_role")
    if role is None:
        return 8 if plan["name"] == TWIN else 1
    need(type(role) is dict and set(role) == {"kind", "column_workers", "choice"},
         "CW8_PLAN_ROLE")
    workers = role["column_workers"]
    need(type(workers) is int and workers in (1, 8), "CW8_PLAN_WORKERS")
    need(role["kind"] == ("IDENTITY_TWIN" if plan["name"] == TWIN else "FULL"),
         "CW8_PLAN_ROLE")
    need(dig(read_pin(plan["spec"]), LEAF) == workers, "CW8_PLAN_SPEC_LEAF")
    if workers == 8 and plan["name"] != TWIN:
        need(is_pin(role["choice"]), "CW8_PLAN_UNAUTHORIZED")
        choice = read_pin(role["choice"])
        rows = [r for r in choice.get("calls", []) if r.get("name") == plan["name"]]
        need(len(rows) == 1 and rows[0].get("spec") == plan["spec"] and
             rows[0].get("column_workers") == 8, "CW8_PLAN_CHOICE_BINDING")
    return workers


def cw8_only_dry_preparation(ctx, call):
    """Recognize new, explicitly dry-only preparation without changing its files.

    Old unlabelled work is kept on its serial path. A saved invocation, sampler,
    monitor or final launch commit always prevents reassignment.
    """
    work = Path(ctx.cfg["p112_launch_root"]) / "work"
    if not work.exists():
        return True
    for folder in sorted(work.glob(call["name"] + "_A*")):
        if not folder.is_dir() or os.path.realpath(folder) != str(folder):
            return False
        if any((folder / p).exists() for p in (
                "invocation.json", "sampler_first_sample.json", "monitor_pid.json",
                "LAUNCH_COMMIT.json", "sampler.stdout.txt", "monitor.stdout.txt", "monitor.stderr.txt")):
            return False
        if not (folder / "plan.json").is_file():
            return False
        _, plan = read_record(folder / "plan.json")
        if not (plan.get("dry_only") is True and plan.get("name") == call["name"] and
                plan.get("attempt") == 1 and plan.get("config") == ctx.config_pin and
                plan.get("spec") == call["spec"] and plan.get("worker_role") == cw8_role(call)):
            return False
    return True


def cw8_admission_clear(ctx, call):
    need(call["origin"] == "P112" and not call["name"].startswith("S0_"),
         "CW8_EXISTING_S0_ROLE")
    name = call["name"]
    need(not ctx.record_paths(name) and not any(n == name for n, _ in ctx.residuals()) and
         not Path(own_registry_path(ctx, name)).exists(), "CW8_ROLE_ALREADY_STARTED")
    # Early refusal/launch preparation fixes the role. Explicit dry-only
    # preparation is independently recognizable and carries no attempt.
    need(cw8_only_dry_preparation(ctx, call), "CW8_ROLE_ALREADY_PREPARED")


def cw8_choice_lock(function):
    """Serialize choice discovery and exclusive publication on this launch root.

    The persistent empty lock inode is never replaced, truncated or removed.
    Lock acquisition precedes reading choices; a waiting Context must discard
    its cached call list before reconstructing the now-current durable roles.
    """
    @functools.wraps(function)
    def locked(ctx, *args, **kwargs):
        root = Path(ctx.cfg["p112_launch_root"])
        need(root.is_dir() and os.path.realpath(root) == str(root),
             "CW8_CHOICE_LOCK_ROOT")
        path = root / ".worker_choices.lock"
        path_rules(str(path), "worker choice lock")
        flags = os.O_RDONLY | os.O_NOFOLLOW
        try:
            fd = os.open(path, flags | os.O_CREAT | os.O_EXCL, 0o444)
        except FileExistsError:
            fd = os.open(path, flags)
        try:
            info = os.fstat(fd)
            need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1,
                 "CW8_CHOICE_LOCK_FILE")
            fcntl.flock(fd, fcntl.LOCK_EX)
            current = os.stat(path, follow_symlinks=False)
            need((current.st_dev, current.st_ino) == (info.st_dev, info.st_ino),
                 "CW8_CHOICE_LOCK_IDENTITY")
            ctx._calls = None
            return function(ctx, *args, **kwargs)
        finally:
            os.close(fd)
    return locked


@read_scope
@cw8_choice_lock
def select_workers(ctx, forecast_pin=None, *, serial_name=None):
    """Root-invoked metadata operation. Writes one immutable cohort record."""
    ctx.gate()
    calls = ctx.calls()
    saved = cw8_saved_choices(ctx)
    if serial_name is not None:
        call = ctx.call(serial_name)
        if serial_name in saved:
            return {"status": "ALREADY_SELECTED", "choice": saved[serial_name][2]}
        selected = [call]
    else:
        selected = [c for c in calls if c["origin"] == "P112" and c["name"] not in saved and
                    not ctx.record_paths(c["name"]) and
                    not Path(own_registry_path(ctx, c["name"])).exists()]
    need(selected, "CW8_NO_NEW_CALLS")
    for call in selected:
        cw8_admission_clear(ctx, call)
    now = ctx.system.utc()
    license_pin, prediction = None, {"column_workers": 1, "reason": "NO_SELECTION_INPUT"}
    if serial_name is None:
        try:
            license_pin = cw8_root_license_pin(ctx.v006_text)
            cw8_authenticate(ctx, license_pin)
            need(is_pin(forecast_pin), "CW8_FORECAST_MISSING")
            forecast = read_pin(forecast_pin)
            need(type(forecast) is dict, "CW8_FORECAST_FORM")
            need(forecast.get("scope") == cw8_scope(ctx), "CW8_FORECAST_SCOPE")
            prediction = cw8_predict(forecast, [c["name"] for c in selected], now)
            if prediction["column_workers"] == 8:
                for call in selected:
                    pin = ctx.get_vpin("SPEC_PIN", call["name"] + "_FULL_CW8")
                    cw8_spec_pair(read_pin(call["spec"], decode=False), read_pin(pin, decode=False))
        except (Refusal, OSError, ValueError, KeyError, TypeError,
                AttributeError, OverflowError, RecursionError) as exc:
            prediction = {"column_workers": 1,
                          "reason": exc.code if isinstance(exc, Refusal) else type(exc).__name__}
    workers = prediction["column_workers"]
    rows = []
    for call in sorted(selected, key=lambda c: c["name"]):
        rows.append({key: call[key] for key in ("name", "point_key", "theta_sha256")})
        rows[-1].update(serial_spec=call["spec"], column_workers=workers,
                        spec=(ctx.get_vpin("SPEC_PIN", call["name"] + "_FULL_CW8")
                              if workers == 8 else call["spec"]))
    record = {"schema": CW8_CHOICE_SCHEMA, "producer": ctx.own_pin, "scope": cw8_scope(ctx),
              "selected_at_utc": now, "date_u": date_u(), "license": license_pin,
              "forecast": forecast_pin, "prediction": prediction, "calls": rows}
    directory = cw8_choice_directory(ctx)
    if not directory.exists():
        directory.mkdir()
    need(directory.is_dir() and os.path.realpath(directory) == str(directory), "CW8_CHOICE_DIRECTORY")
    # One cohort record is the authority for every row. There is no multi-file
    # commit window in which a partial cohort could be silently re-optimized.
    destination = directory / ("CHOICE_" + sha(canonical(record)) + ".json")
    pin = ctx.write(str(destination), record)
    ctx._calls = None
    ctx.calls()  # Reconstruct using the durable bytes before returning.
    return {"status": "SELECTED", "choice": pin, "column_workers": workers,
            "reason": prediction["reason"], "names": [r["name"] for r in rows]}


def cw8_ensure_default(ctx, call):
    """A new root launch with no selection gets an explicit serial record."""
    if call["origin"] != "P112" or call.get("worker_choice") is not None:
        return call
    name = call["name"]
    if (ctx.record_paths(name) or Path(own_registry_path(ctx, name)).exists() or
            any(n == name for n, _ in ctx.residuals()) or
            not cw8_only_dry_preparation(ctx, call)):
        return call  # Historical serial custody/preparation cannot be upgraded.
    select_workers(ctx, serial_name=call["name"])
    return ctx.call(call["name"])


def cw8_check_attempt(ctx, call, record, closed=None):
    role = cw8_check_role(call, record.get("worker_role"))
    spec = record.get("spec", call["spec"])
    # S0 relaunches fill identical bytes under a fresh work directory.
    need(is_pin(spec) and spec["sha256"] == call["spec"]["sha256"],
         "CW8_ATTEMPT_RAW_SPEC")
    need(record["caps"]["rss_cap_bytes"] == cw8_rss(call["name"], role["column_workers"]),
         "CW8_ATTEMPT_RSS")
    if call["name"] != TWIN:
        need(record.get("watch_pid") is None, "CW8_FULL_CALL_TWIN_WATCHER")
    if closed is not None:
        cw8_check_role(call, closed.get("worker_role"))
    return role["column_workers"]


if __name__ == "__main__":
    sys.exit(cli())

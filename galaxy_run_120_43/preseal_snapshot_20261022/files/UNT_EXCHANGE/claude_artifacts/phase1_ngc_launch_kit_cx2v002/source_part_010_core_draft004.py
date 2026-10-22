"""P-112 Phase-1 launch custody. Invoked by the scientific launch owner only.

Implements A223 and the nine ROUND5 binding amendments. No function below starts
a scientific process on import. Runtime files are exclusive, fsynced and 0444.
"""
import argparse
import copy
import contextvars
import functools
import datetime as dt
import hashlib
import json
import math
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import time
import types
from pathlib import Path

PY = "/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"
A = "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/"
V006 = ("/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/"
        "CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md")
TOOL_NAME = "P112_LAUNCHER_CX2V002"
IMPLEMENTATION_REVISION = "CX2V002"  # Existing record formats retain their schema identifiers.
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
    cache_key = path
    if snapshots is not None and cache_key in snapshots:
        raw = snapshots[cache_key]
    else:
        raw = Path(path).read_bytes()
        if snapshots is not None:
            snapshots[cache_key] = raw
    pin = {"path": path, "sha256": sha(raw)}
    return pin, strict_json(raw) if decode else raw


def guard_record(path):
    path = str(path)
    guard_read(path)
    need(os.path.realpath(path) == path, "RECORD_SYMLINK", path)
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
    if name == TWIN:
        if stop is not None:
            need(stop.get("reason") == "ITERATION_0001_COMPLETED_AND_SIDECAR" and
                 stop.get("outdir") == outdir and
                 (stop.get("launch_json") or {}).get("sha256") == launch_pin["sha256"],
                 "TWIN_STOP_NOT_BOUND")
        if stop is not None or str(rec.get("status", "")).startswith("STOPPED_"):
            return "TWIN_PLANNED_STOP", "PLANNED_STOP"
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


def first_caps(name):
    return dict(CAPS["twin" if name == TWIN else "serial"])


def caps_of(receipt):
    return {k: receipt[k] for k in CAPS["serial"]}


def terminal_prefix(actual, name):
    """Advisory A223 terminal disposition, earliest prefix; non-attempts omitted."""
    for i, cur in enumerate(actual):
        cls = cur["status_class"]
        if cls == "FINISHED":
            return {"index": i, "disposition": "FINISHED"}
        if cls == "PLANNED_STOP":
            need(name == TWIN, "PLANNED_STOP_NOT_TWIN")
            return {"index": i, "disposition": "PLANNED_STOP"}
        if i == 0:
            continue
        prev, first = actual[i - 1], actual[0]
        same_spec = len({r["spec_sha256"] for r in actual[:i + 1]}) == 1
        same_raw = prev["raw_status"] == cur["raw_status"]
        zero = (type(prev.get("other_ngc_processes_max")) is int and
                type(cur.get("other_ngc_processes_max")) is int and
                prev["other_ngc_processes_max"] == cur["other_ngc_processes_max"] == 0)
        if cls in ("FAILED", "CAP", "OUTPUT_CAP"):
            cap_ok = (cur.get("rss_cap_bytes") == cur.get("host_ram_bytes", 0) * (11 if name == TWIN else 1)
                      and cur.get("host_ram_bytes") == RAM
                      and cur.get("wall_cap_s") == 2 * first["wall_cap_s"])
            if cls == "OUTPUT_CAP":
                cap_ok = cap_ok and cur["output_cap_bytes"] > first["output_cap_bytes"]
            if prev["status_class"] == cls and same_raw and same_spec and zero and cap_ok:
                return {"index": i, "disposition": "RULE_C_INVALID"}
        if cur["raw_status"] in ("CHILD_FAILED|REFUSED", "CHILD_FAILED|BLOCKED"):
            if (same_raw and same_spec and zero and cur.get("solo_mode") is True and
                    prev.get("solo_mode") is True and caps_of(cur) == caps_of(prev)):
                return {"index": i, "disposition": "UNEVALUATED_INFRA_REPEAT"}
    return None


def next_attempt(name, records, actual, residuals, trailing_nonattempt=None):
    """Pure numbering/ownership/cap decision; filesystem conditions are checked first."""
    terminal = terminal_prefix(actual, name)
    need(terminal is None, "ATTEMPT_AFTER_TERMINAL", terminal)
    ks = [r["attempt"] for r in records] + [k for n, k in residuals if n == name]
    k = max(ks, default=0) + 1
    if name.startswith("S0_"):
        need(any(r["origin"] == "P112" or r["outcome"] == "LAUNCH" for r in records) or
             any(n == name for n, _ in residuals), "KIT_RELAUNCH_OWNS")
    caps, solo, counted, basis = first_caps(name), False, False, []
    if trailing_nonattempt is not None:
        caps = dict(trailing_nonattempt["caps"])
        solo = trailing_nonattempt.get("solo_mode", False)
    elif actual:
        last, first = actual[-1], actual[0]
        caps, solo = caps_of(last), last.get("solo_mode", False)
        if last["status_class"] in ("FAILED", "CAP", "OUTPUT_CAP"):
            caps["wall_cap_s"] = first["wall_cap_s"] * 2
            caps["rss_cap_bytes"] = RAM * (11 if name == TWIN else 1)
            if last["status_class"] == "OUTPUT_CAP":
                caps["output_cap_bytes"] = first["output_cap_bytes"] * 2
            solo, counted = True, True
            basis = [r["receipt_pin"] for r in actual if "receipt_pin" in r]
        elif last["raw_status"] in ("CHILD_FAILED|REFUSED", "CHILD_FAILED|BLOCKED"):
            solo = True
    return {"attempt": k, "caps": caps, "solo_mode": solo, "counted_rerun": counted,
            "rule_c_basis": basis}


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

"""Root verify (Claude2 lineage), P-112 CX2V002: fresh adversarial lens (synthetic only).

Every case asserts what the rulings of record require (A223, A226 item 1, A229, 0784, 0785, 0786).
A FAIL row is a deviation; `severity_if_fail` says how root should weigh it. Synthetic only: fixtures
are built by the vendor's own fixture builders under --out (exclusive create); only processes started
here are signalled; no network; no NGC3198 data, run trees, V007_POSTSEAL_RECORDS or ~/.codex.
An audit hook watches every open made by P-112 code (path, realpath and inode) for forbidden targets
and counts reads per public operation. Pinned-file changes between reads are simulated in memory by
patching Path.read_bytes; the only on-disk change is to a writable synthetic file created here (A04d).
"""
import argparse
import ast
import contextlib
import hashlib
import io
import json
import os
import pathlib
import re
import signal
import subprocess
import sys
import time
import traceback
import types
from collections import Counter
from pathlib import Path

KIT = "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/phase1_ngc_launch_kit_cx2v002/"
TOOL = KIT + "phase1_ngc_launch_cx2v002.py"
TOOL_SHA = "65ac534953678ee845910d0a32e41b71deff142b660b3efbed68e302a33777aa"
TESTS = KIT + "test_phase1_ngc_launch_cx2v002.py"
TESTS_SHA = "920cf3ef94e9ce5a46479c99d6c6f9684827d55e262759fc591ef57bc6699a2e"
V006 = ("/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/"
        "CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md")
PY = "/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"
OUTDIR_COMPONENT = re.compile(r"^NGC_P1_.+_RUN_(?:CX2V001|C2V003A)_A[0-9]+$")
PIN_LINE = "TOOL_PIN P112_LAUNCHER_CX2V002 %s %s" % (TOOL_SHA, TOOL)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def verified(path, want):
    raw = Path(path).read_bytes()
    if sha(raw) != want:
        raise SystemExit("PIN_MISMATCH " + path)
    return raw


def date_u():
    return subprocess.check_output(["/bin/date", "-u"], env=dict(os.environ, LC_ALL="C"), text=True).strip()


def forbidden_reason(path):
    if path == V006:
        return None
    parts = Path(path).parts
    low = [p.lower() for p in parts]
    base = low[-1] if low else ""
    if base in ("result.json", "finish.json", "progress.jsonl"):
        return "RESULT_FILE"
    if "stages" in low or "a_side" in low:
        return "STAGES_OR_A_SIDE"
    if any("ngc3198" in p for p in low):
        return "NGC3198_COMPONENT"
    if "v007_postseal_records" in low or ".codex" in low or "runs_ext" in low:
        return "SEALED_OR_CODEX"
    if path.endswith((".receipt.json.stdout.txt", ".receipt.json.stderr.txt")):
        return "RECEIPT_STDIO"
    for p in parts[:-1]:
        if OUTDIR_COMPONENT.match(p):
            return "INSIDE_OUTDIR"
    return None


class Audit:
    """Watches opens made with a P-112 frame on the stack. Classifies volatile/counter/self reads."""

    def __init__(self):
        self.case = "setup"
        self.opens = []
        self.forbidden = []
        self.forbidden_inodes = {}
        self.op = None
        self.op_reads = []
        self.busy = False

    def register_forbidden_tree(self, outdir, receipt=None):
        for base, _, files in os.walk(outdir):
            for name in files:
                p = os.path.join(base, name)
                st = os.stat(p)
                self.forbidden_inodes[(st.st_dev, st.st_ino)] = p
        if receipt:
            for suffix in (".stdout.txt", ".stderr.txt"):
                p = receipt + suffix
                if os.path.exists(p):
                    st = os.stat(p)
                    self.forbidden_inodes[(st.st_dev, st.st_ino)] = p

    def hook(self, event, args):
        if self.busy or event != "open" or not isinstance(args[0], (str, bytes)):
            return
        self.busy = True
        try:
            frame = sys._getframe(1)
            names, ours = [], False
            while frame is not None:
                if frame.f_code.co_filename == TOOL:
                    ours = True
                    names.append(frame.f_code.co_name)
                frame = frame.f_back
            if not ours:
                return
            path = os.fsdecode(args[0])
            mode, flags = args[1], args[2] if len(args) > 2 else 0
            if isinstance(mode, str):
                is_read = ("r" in mode or "+" in mode) and not any(c in mode for c in "wxa")
            else:
                is_read = not (flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT))
            real = os.path.realpath(path)
            try:
                st = os.stat(path)
                inode = (st.st_dev, st.st_ino)
                is_dir = os.path.isdir(path)
            except OSError:
                inode, is_dir = None, False
            row = {"case": self.case, "path": path, "realpath": real, "inode": inode, "read": is_read,
                   "dir": is_dir, "volatile": "observe_file" in names, "counter": "identify" in names,
                   "self": real == TOOL, "functions": names[:4]}
            self.opens.append(row)
            if self.op is not None and is_read and not is_dir:
                self.op_reads.append(row)
            reason = None
            for spelling in dict.fromkeys((path, real)):
                reason = forbidden_reason(spelling)
                if reason:
                    break
            if reason is None and inode is not None and inode in self.forbidden_inodes:
                reason = "FORBIDDEN_INODE(" + self.forbidden_inodes[inode] + ")"
            if reason is not None:
                self.forbidden.append({"case": self.case, "path": path, "realpath": real, "reason": reason,
                                       "functions": names[:4]})
        finally:
            self.busy = False

    def forbidden_in(self, case):
        return [x for x in self.forbidden if x["case"] == case]

    @contextlib.contextmanager
    def operation(self, label):
        self.op, self.op_reads = label, []
        try:
            yield self
        finally:
            self.op = None

    def duplicate_immutable_reads(self, reads=None):
        rows = [r for r in (self.op_reads if reads is None else reads)
                if not r["volatile"] and not r["counter"] and not r["self"]]
        out = {}
        for key in ("path", "realpath", "inode"):
            counts = Counter(str(r[key]) for r in rows if r[key] is not None)
            dup = {k: n for k, n in counts.items() if n > 1}
            if dup:
                out[key] = dup
        return out, len(rows)


@contextlib.contextmanager
def swap_reads(target, fn):
    """fn(n, raw_or_None) -> bytes, or raises. Simulates a file that changes between reads (memory only)."""
    original = pathlib.Path.read_bytes
    state = {"n": 0, "shas": []}

    def patched(self):
        if str(self) == str(target):
            state["n"] += 1
            raw = original(self) if os.path.exists(str(self)) else None
            out = fn(state["n"], raw)
            state["shas"].append(sha(out))
            return out
        return original(self)
    pathlib.Path.read_bytes = patched
    try:
        yield state
    finally:
        pathlib.Path.read_bytes = original


class Runner:
    def __init__(self, audit):
        self.audit, self.rows = audit, []

    def case(self, name, lens, severity, action):
        self.audit.case = name
        row = {"name": name, "lens": lens, "severity_if_fail": severity}
        try:
            observed = action()
            row.update(status="PASS", observed=observed)
        except AssertionError as e:
            row.update(status="FAIL", observed=e.args[0] if e.args else None)
        except Exception as e:  # harness error, reported as such
            row.update(status="ERROR", observed=repr(e), trace=traceback.format_exc(limit=8)[-3000:])
        forbidden = self.audit.forbidden_in(name)
        if forbidden:
            row["forbidden_opens"] = forbidden
            if row["status"] == "PASS":
                row["status"] = "FAIL"
                row["observed"] = {"passed_but_forbidden_open": row["observed"]}
        self.rows.append(row)
        self.audit.case = "between:" + name
        return row


def expect_refusal(M, action):
    try:
        result = action()
    except M.Refusal as e:
        return e.code
    return {"no_refusal": True, "result": result if isinstance(result, (str, dict, list, type(None))) else repr(result)}


def outcome_of(M, action):
    try:
        result = action()
    except M.Refusal as e:
        return {"refusal": e.code}
    except Exception as e:
        return {"exception": type(e).__name__, "detail": str(e)[:200]}
    return {"result": result if isinstance(result, (str, dict, list, type(None), int)) else repr(result)}


def accelerate(system, rows_fn=None, step=None, max_sleeps=6000):
    clock = {"now": 0.0, "polls": 0, "sleeps": 0}
    system.monotonic = lambda: clock["now"]

    def sleep(seconds):
        clock["sleeps"] += 1
        if clock["sleeps"] > max_sleeps:
            raise RuntimeError("no decision after %d sleeps" % max_sleeps)
        clock["now"] += seconds if step is None else step
    system.sleep = sleep
    if rows_fn is not None:
        def processes():
            clock["polls"] += 1
            return [dict(r) for r in rows_fn(clock["polls"])]
        system.processes = processes
    return clock


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = Path(a.out)
    verified(TOOL, TOOL_SHA)
    tests_raw = verified(TESTS, TESTS_SHA)
    started = date_u()
    audit = Audit()
    sys.addaudithook(audit.hook)
    T = types.ModuleType("_rootverify_c2v002_vendor_fixtures")
    T.__file__ = TESTS
    exec(compile(tests_raw, TESTS, "exec"), T.__dict__)
    suite = T.Suite(TOOL, str(out), TOOL_SHA)  # verifies tool bytes, execs them, mkdir(out) exclusive
    M = suite.module
    R = Runner(audit)
    own_pin = {"path": TOOL, "sha256": TOOL_SHA}
    live = []

    def start(argv, **kw):
        p = subprocess.Popen(argv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                             start_new_session=True, **kw)
        live.append(p)
        return p

    def stop(p):
        if p.poll() is None:
            p.terminate()
            try:
                p.wait(timeout=5)
            except subprocess.TimeoutExpired:
                p.kill()
                p.wait(timeout=5)

    def stub_kit(label, source):
        return suite.raw_write(suite.root / ("stub_kit_" + label + ".py"), source.encode())

    def production_roots(f):
        # Production Context.__init__ registers both run roots for guard_read; the vendor's FixtureContext
        # skips __init__, so register them here to test production guard behaviour.
        M.READ_RUN_ROOTS.update((f.ctx.cfg["run_root"], f.ctx.cfg["s0"]["run_root"]))
        if os.path.isdir(f.outdir):
            audit.register_forbidden_tree(f.outdir, f.outdir + ".receipt.json")
        return f

    def rfix(label, **kw):
        return production_roots(T.receipt_fixture(suite, label, **kw))

    def resfix(label, **kw):
        return production_roots(T.resume_fixture(suite, label, **kw))

    # ===================================================================== 1. volatile observation pinning
    def a01():
        f = resfix("A01_volatile_launch_json_polls")
        target = f.outdir + ".receipt.json.launch.json"
        real = Path(target).read_bytes()
        changed = (json.dumps(dict(json.loads(real), rv_changed_after_parse=True), sort_keys=True) + "\n").encode()

        def seq(n, raw):
            if n == 1:
                raise FileNotFoundError(target)
            if n == 2:
                return real[: len(real) // 2]
            if n == 3:
                return real
            return changed
        accelerate(f.ctx.system)
        with swap_reads(target, seq) as st:
            pin = M.launch_resume(f.ctx, f.name, 1)
        rec = json.loads(Path(pin["path"]).read_bytes())
        obs = rec["observations"]
        observed = {"tool_reads_of_launch_json": st["n"], "outcome": rec["outcome"],
                    "record_launch_json_sha256": rec["launch_json"]["sha256"], "parsed_buffer_sha256": sha(real),
                    "observation_count": obs["counts"].get("launch_json"),
                    "last_observation_sha256": obs["last_observation"]["launch_json"]["pin"]["sha256"],
                    "launch_wait_polls": rec["launch_wait"]["polls"],
                    "record_utc_matches_buffer": rec["launch_json"]["utc"] == json.loads(real)["utc"]}
        assert (st["n"] == 3 and rec["outcome"] == "LAUNCH" and rec["launch_json"]["sha256"] == sha(real)
                and obs["counts"]["launch_json"] == 2 and observed["last_observation_sha256"] == sha(real)
                and observed["record_utc_matches_buffer"] and rec["launch_wait"]["polls"] == 3), observed
        return observed
    R.case("A01_launch_json_absent_then_partial_then_valid_pin_equals_checked_observation",
           "volatile", "BLOCKING", a01)

    def post_bound(label, fresh_parseable):
        f = resfix(label)
        target = f.outdir + ".receipt.json.launch.json"
        real = Path(target).read_bytes()
        partial1 = real[: len(real) // 3]
        partial2 = real[: len(real) // 2] + b"#"
        stub = stub_kit(label, "import sys\nsys.stderr.write('{\"alive\": false}')\nsys.exit(1)\n")
        f.ctx.pins = dict(f.ctx.pins, kit=stub)

        def seq(n, raw):
            if n <= 4:
                return partial1
            if n == 5:
                return real if fresh_parseable else partial2
            return b'{"rv_reread_after_fresh_observation": true}\n'
        accelerate(f.ctx.system, rows_fn=lambda n: [], step=100.0)
        with swap_reads(target, seq) as st:
            pin = M.launch_resume(f.ctx, f.name, 1)
        rec = json.loads(Path(pin["path"]).read_bytes())
        fresh = real if fresh_parseable else partial2
        obs = rec["observations"]
        observed = {"tool_reads": st["n"], "outcome": rec["outcome"], "stop": rec.get("stop"),
                    "record_sha256": rec["launch_json"]["sha256"], "fresh_observation_sha256": sha(fresh),
                    "bound_observation_sha256": sha(partial1),
                    "count": obs["counts"].get("launch_json"),
                    "last_sha256": obs["last_observation"]["launch_json"]["pin"]["sha256"],
                    "checks": rec["launch_check"]["checks"]}
        ok = (st["n"] == 5 and rec["outcome"] == "MISLAUNCH" and rec["launch_json"]["sha256"] == sha(fresh)
              and obs["counts"]["launch_json"] == 5 and observed["last_sha256"] == sha(fresh)
              and rec["launch_check"]["checks"].get("launch_json_within_bound") is False)
        if fresh_parseable:
            ok = ok and rec["launch_json"]["utc"] == json.loads(real)["utc"] and rec["stop"]["result"] == "ALREADY_ENDED"
        else:
            ok = ok and rec["launch_json"]["utc"] is None and rec["launch_check"]["checks"]["launch_json_parseable"] is False
        assert ok, observed
        return observed
    R.case("A02_post_bound_fresh_parseable_observation_is_the_pinned_and_checked_buffer", "volatile",
           "BLOCKING", lambda: post_bound("A02_post_bound_parseable", True))
    R.case("A03_post_bound_fresh_unparseable_observation_is_pinned_not_the_bound_buffer", "volatile",
           "BLOCKING", lambda: post_bound("A03_post_bound_unparseable", False))

    # ===================================================================== 2. cutoff copy bytes vs hash
    def cutoff_terms(f):
        return [{"name": f.name, "time_utc": f.rec["utc_end"], "receipt": f.entry_pin, "disposition": "FINISHED"}]

    def a04():
        f = rfix("A04_cutoff_copy_buffer")
        source = f.ctx.cfg["v006"]
        first = Path(source).read_bytes()
        later = first + b"\n## A1000: synthetic later entry\n"
        with swap_reads(source, lambda n, raw: first if n == 1 else later) as st:
            pin = M.write_cutoff(f.ctx, cutoff_terms(f))
        doc = json.loads(Path(pin["path"]).read_bytes())
        copy_raw = Path(doc["copy"]["path"]).read_bytes()
        last = doc["observations"]["last_observation"]["v006_cutoff"]
        observed = {"source_reads": st["n"], "copy_sha256_on_disk": sha(copy_raw), "record_copy_sha256": doc["copy"]["sha256"],
                    "observation_sha256": last["pin"]["sha256"], "hashed_buffer_sha256": sha(first),
                    "copy_bytes": len(copy_raw), "record_bytes": doc["copy"]["bytes"],
                    "copy_name_digest_ok": Path(doc["copy"]["path"]).name == "V006_CUTOFF_COPY_%s.md" % sha(first),
                    "copy_nlink": os.stat(doc["copy"]["path"]).st_nlink,
                    "copy_inode_differs_from_source": os.stat(doc["copy"]["path"]).st_ino != os.stat(source).st_ino}
        assert (st["n"] == 1 and copy_raw == first and doc["copy"]["sha256"] == sha(first) == last["pin"]["sha256"]
                and doc["copy"]["bytes"] == len(first) and observed["copy_name_digest_ok"]
                and observed["copy_inode_differs_from_source"]), observed
        return observed
    R.case("A04a_cutoff_copy_written_from_the_hashed_observation_not_a_reread", "cutoff", "BLOCKING", a04)

    def planted_copy(label, how):
        f = rfix(label)
        source = f.ctx.cfg["v006"]
        raw = Path(source).read_bytes()
        p = Path(f.ctx.cfg["v006_copy_dir"]) / ("V006_CUTOFF_COPY_" + sha(raw) + ".md")
        if how == "different_bytes":
            suite.raw_write(p, raw + b"tamper\n")
        elif how == "symlink_to_source":
            os.symlink(source, p)
        return f, M.write_cutoff, p

    def a04b():
        got = {}
        for how, want in (("different_bytes", "CUTOFF_COPY_EXISTS_DIFFERENT"), ("symlink_to_source", "RECORD_SYMLINK")):
            f, fn, p = planted_copy("A04b_planted_" + how, how)
            got[how] = expect_refusal(M, lambda f=f: fn(f.ctx, cutoff_terms(f)))
            got[how + "_record_written"] = os.path.lexists(M.cutoff_path(f.ctx))
        observed = {"results": got}
        assert (got["different_bytes"] == "CUTOFF_COPY_EXISTS_DIFFERENT" and got["symlink_to_source"] == "RECORD_SYMLINK"
                and not got["different_bytes_record_written"] and not got["symlink_to_source_record_written"]), observed
        return observed
    R.case("A04b_planted_cutoff_copy_different_or_symlinked_refuses", "cutoff", "FIX", a04b)

    def a04c():
        # A pre-existing copy that is a HARD LINK of the (growing) V006 file is accepted as the copy.
        f = rfix("A04c_planted_hardlink_copy")
        writable = Path(f.root) / "V006_writable_synthetic.md"
        base = Path(f.ctx.cfg["v006"]).read_bytes()
        with writable.open("xb") as h:
            h.write(base)
        f.ctx.cfg["v006"] = str(writable)
        p = Path(f.ctx.cfg["v006_copy_dir"]) / ("V006_CUTOFF_COPY_" + sha(base) + ".md")
        os.link(writable, p)
        result = outcome_of(M, lambda: M.write_cutoff(f.ctx, cutoff_terms(f)))
        with writable.open("ab") as h:  # synthetic, writable file created above
            h.write(b"\n## A1001: appended after the cutoff\n")
        after = Path(p).read_bytes()
        observed = {"write_cutoff": "WRITTEN" if "result" in result else result,
                    "copy_nlink_at_accept": os.stat(p).st_nlink,
                    "copy_sha_after_V006_append_equals_record": sha(after) == sha(base)}
        assert "result" not in result or observed["copy_sha_after_V006_append_equals_record"], observed
        return observed
    R.case("A04c_preexisting_hardlinked_cutoff_copy_is_not_accepted", "cutoff", "NOTE", a04c)

    # ===================================================================== 3. sibling observation receipts
    def refusal_variant(label, origin, sibling="valid", placement="file", rule="ok", counts=None):
        name = "S0_J0_SERIAL" if origin == "KIT" else "P1_M0001"
        f = rfix(label, origin=origin, name=name, mode="FAILED")
        M.close_attempt(f.ctx, name, 1)
        root = Path(f.ctx.cfg["s0"]["launch_root"] if origin == "KIT" else f.ctx.cfg["p112_launch_root"])
        work = root / "work" / "rv_refusal"
        work.mkdir()
        outdir = M.planned_outdir(f.ctx, name, 2, origin)
        plan = {"schema": "UNT_P112_LAUNCH_PLAN_CX2V001", "name": name, "attempt": 2, "outdir": outdir,
                "config": f.ctx.config_pin, "caps": M.first_caps(name), "solo_mode": False}
        pp = suite.raw_write(work / "plan.json", M.encoded(plan))
        so = suite.raw_write(work / "monitor.stdout.txt", b"synthetic refusal\n")
        se = suite.raw_write(work / "monitor.stderr.txt", b"")
        path = (root / "monitor_refused" / (name + "_MONITOR_REFUSED_C2V003A_A2.json") if origin == "KIT" else
                root / "launches" / ("P112_" + name + "_MONITOR_REFUSED_CX2V001_A2.json"))
        sib = Path(str(path) + ".observations.json")
        good_pin = {"path": str(work / "plan.json"), "sha256": pp["sha256"]}
        report = {"counts": counts or {}, "last_observation": {k: {"kind": k, "pin": good_pin, "bytes": 10}
                                                                for k in (counts or {})}, "date_u": M.date_u()}
        raw = {"valid": M.encoded(report),
               "dupkey": b'{"counts": {}, "counts": {}, "last_observation": {}}\n',
               "nan": b'{"counts": {"x": NaN}, "last_observation": {}}\n',
               "relpin": M.encoded({"counts": {"k": 1}, "last_observation": {
                   "k": {"kind": "k", "pin": {"path": "rel/plan.json", "sha256": "0" * 64}, "bytes": 1}}}),
               "boolcount": M.encoded({"counts": {"k": True}, "last_observation": {
                   "k": {"kind": "k", "pin": good_pin, "bytes": 1}}}),
               "list": b"[]\n"}[sibling]
        if placement == "file":
            suite.raw_write(sib, raw)
        elif placement == "symlink":
            target = suite.raw_write(work / "sibling_target.json", raw)
            os.symlink(target["path"], sib)
        elif placement == "dir":
            sib.mkdir()
        digest = sha(raw)
        text = {"ok": "synthetic D7 observations_sha256=" + digest,
                "dup": "synthetic D7 observations_sha256=%s observations_sha256=%s" % (digest, digest),
                "glued": "synthetic D7 xobservations_sha256=" + digest,
                "period": "synthetic D7 observations_sha256=" + digest + ".",
                "upper": "synthetic D7 observations_sha256=" + digest.upper(),
                "two_different": "synthetic D7 observations_sha256=%s observations_sha256=%s" % (digest, "0" * 64)}[rule]
        rec = {"schema": "MONITOR_REFUSED_ATTEMPT_RECORD_C2V001", "name": name, "attempt": 2,
               "launcher": "KIT_C2V003A" if origin == "KIT" else "P112_CX2V001",
               "writer": {"name": "ROOT", "sha256": None} if origin == "KIT" else {"name": M.TOOL_NAME, "sha256": TOOL_SHA},
               "plan": pp, "monitor_stdout": so, "monitor_stderr": se, "absent": M.absent_paths(outdir),
               "date_u": M.date_u(), "rule": text}
        suite.raw_write(path, M.encoded(rec))
        return f

    def a05():
        variants = [
            ("symlink_sibling", dict(placement="symlink"), "RECORD_SYMLINK"),
            ("directory_sibling", dict(placement="dir"), "OBSERVATIONS_SIBLING_MISSING"),
            ("duplicate_key_sibling", dict(sibling="dupkey"), "JSON_DUPLICATE_KEY"),
            ("nan_sibling", dict(sibling="nan"), "JSON_NONFINITE"),
            ("relative_pin_sibling", dict(sibling="relpin"), "OBSERVATIONS_FORM"),
            ("bool_count_sibling", dict(sibling="boolcount"), "OBSERVATIONS_FORM"),
            ("list_sibling", dict(sibling="list"), "OBSERVATIONS_FORM"),
            ("rule_token_twice_same_sha", dict(rule="dup"), "OBSERVATIONS_RULE_SHA"),
            ("rule_token_twice_different", dict(rule="two_different"), "OBSERVATIONS_RULE_SHA"),
            ("rule_token_glued_prefix", dict(rule="glued"), "OBSERVATIONS_RULE_SHA"),
            ("rule_token_uppercase_hex", dict(rule="upper"), "OBSERVATIONS_RULE_SHA"),
        ]
        got, bad = {}, {}
        for origin in ("P112", "KIT"):
            for label, kw, want in variants:
                f = refusal_variant("A05_%s_%s" % (origin, label), origin, **kw)
                status = M.status(f.ctx)["calls"][0]["status"]
                verify = expect_refusal(M, lambda f=f: M.assemble_registry(f.ctx, verify=True))
                got[origin + ":" + label] = {"status": status, "verify": verify}
                if status != want:
                    bad[origin + ":" + label] = {"want": want, "status": status}
        observed = {"results": got, "mismatches": bad}
        assert not bad, observed
        return observed
    R.case("A05_sibling_tamper_matrix_fresh_variants_P112_and_root_written_KIT", "sibling", "FIX", a05)

    def a05b():
        # Root writes free-form rule text; a sentence-final period after the sha is a natural form.
        got = {}
        for origin in ("P112", "KIT"):
            f = refusal_variant("A05b_%s_period" % origin, origin, rule="period")
            got[origin] = M.status(f.ctx)["calls"][0]["status"]
        observed = {"status_with_period_after_sha": got,
                    "note": "fail-closed; a root-written KIT record is immutable, so a malformed rule blocks the call"}
        assert all(v == "OBSERVATIONS_RULE_SHA" for v in got.values()), observed
        return observed
    R.case("A05b_rule_token_followed_by_period_refuses_fail_closed", "sibling", "INFO", a05b)

    def a06():
        f = T.observation_refusal_fixture(suite, "A06_sibling_then_crash", variant="emit")
        original = f.ctx.write
        state = {"n": 0}

        def crashing(path, obj):
            if str(path).endswith("_A2.json"):
                raise OSError("rv simulated crash between sibling and record")
            return original(path, obj)
        f.ctx.write = crashing
        first = outcome_of(M, lambda: M.record_monitor_refused(f.ctx, f.refusal_plan, str(f.refusal_work)))
        f.ctx.write = original
        sibling = Path(f.ctx.cfg["p112_launch_root"]) / "launches" / "P112_P1_M0001_MONITOR_REFUSED_CX2V001_A2.json.observations.json"
        retry = outcome_of(M, lambda: M.record_monitor_refused(f.ctx, f.refusal_plan, str(f.refusal_work)))
        st = M.status(f.ctx)["calls"][0]
        observed = {"first_call": first, "orphan_sibling_exists": sibling.exists(), "retry": retry,
                    "status_after": {"status": st["status"], "next_attempt": (st.get("next") or {}).get("attempt"),
                                     "nonattempts": len(st.get("nonattempts") or [])}}
        assert ("result" in retry) or ("refusal" in retry), observed
        return observed
    R.case("A06_interrupted_between_sibling_and_record_retry_is_recoverable_or_named", "sibling", "NOTE", a06)

    def a07():
        got = {}
        f = refusal_variant("A07_KIT_root_counts", "KIT", counts={"root_existence_check": 5, "root_mount_check": 1})
        got["root_sibling_with_root_kinds"] = M.status(f.ctx)["calls"][0]["status"]
        g = refusal_variant("A07_P112_valid", "P112")
        got["p112_valid"] = M.status(g.ctx)["calls"][0]["status"]
        observed = {"results": got}
        assert got["root_sibling_with_root_kinds"] == "READY" and got["p112_valid"] == "READY", observed
        return observed
    R.case("A07_root_written_KIT_sibling_with_root_observation_kinds_accepted", "sibling", "FIX", a07)

    # ===================================================================== 4. TOOL_PIN gate, F2 lines, F5 boundary
    def a08():
        cx1 = "TOOL_PIN P112_LAUNCHER_CX2V001 a72d96c150ca1c638474cddba23f5264374c7ae9aa285c3d38ebfb3e61519bb1 " \
              "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/phase1_ngc_launch_kit_cx2/phase1_ngc_launch_cx2v001.py"
        variant_case = TOOL.replace("/Users/bgm/Research/", "/Users/bgm/research/")
        cases = {
            "valid": ("## A232: adopt\n" + PIN_LINE + "\n", "PASS"),
            "valid_under_A108_continued": ("## A108 continued\n" + PIN_LINE + "\n", "PASS"),
            "valid_CRLF_file": ("## A232: adopt\r\n" + PIN_LINE + "\r\n", "PASS"),
            "valid_double_trailing_CR": ("## A232: adopt\n" + PIN_LINE + "\r\r\n", "PASS"),
            "pin_then_U2028_tail_same_line": ("## A232: adopt\n" + PIN_LINE + "\u2028trailing words\n", "TOOL_PIN_MISMATCH"),
            "pin_then_midline_CR_tail": ("## A232: adopt\n" + PIN_LINE + "\rtrailing\n", "TOOL_PIN_MISMATCH"),
            "NBSP_separator": ("## A232: adopt\nTOOL_PIN P112_LAUNCHER_CX2V002\u00a0%s %s\n" % (TOOL_SHA, TOOL), "TOOL_PIN_MISMATCH"),
            "VT_separator": ("## A232: adopt\nTOOL_PIN P112_LAUNCHER_CX2V002\x0b%s %s\n" % (TOOL_SHA, TOOL), "TOOL_PIN_MISMATCH"),
            "only_CX2V001_line": ("## A232: adopt\n" + cx1 + "\n", "TOOL_PIN_MISSING"),
            "CX2V001_and_CX2V002": ("## A232: adopt\n" + cx1 + "\n" + PIN_LINE + "\n", "PASS"),
            "case_variant_path": ("## A232: adopt\nTOOL_PIN P112_LAUNCHER_CX2V002 %s %s\n" % (TOOL_SHA, variant_case), "TOOL_PIN_MISMATCH"),
            "dotted_heading": ("## A232. adopt\n" + PIN_LINE + "\n", "TOOL_PIN_MISMATCH"),
            "paren_heading": ("## A232(adopt)\n" + PIN_LINE + "\n", "TOOL_PIN_MISMATCH"),
            "two_space_heading_after_entry": ("## A231: x\n##  A232: adopt\n" + PIN_LINE + "\n", "TOOL_PIN_MISMATCH"),
            "BOM_before_heading": ("\ufeff## A232: adopt\n" + PIN_LINE + "\n", "TOOL_PIN_MISMATCH"),
            "pin_in_code_fence_whole_line": ("## A232: adopt\n```\n" + PIN_LINE + "\n```\n", "PASS"),
            "duplicate_across_A108_continued": ("## A232: adopt\n" + PIN_LINE + "\n## A108 continued\n" + PIN_LINE + "\n", "TOOL_PIN_DUPLICATE"),
            "uppercase_name_suffix_malformed_INFO": ("## A232: adopt\n" + PIN_LINE + "\nTOOL_PIN P112_LAUNCHER_CX2V002X not-a-pin\n", "PASS"),
        }
        got, bad = {}, {}
        for label, (text, want) in cases.items():
            r = expect_refusal(M, lambda text=text: M.tool_gate(text, own_pin))
            got[label] = "PASS" if isinstance(r, dict) else r
            if got[label] != want:
                bad[label] = {"want": want, "got": got[label]}
        kit = M.load_verified(M.REAL["writer"], "_rv_kit_pin_parser")
        kit_ok = kit.parse_v006_pins(("## A232: adopt\n" + PIN_LINE + "\n").encode())["pins"]
        observed = {"results": got, "mismatches": bad,
                    "kit_parser_ignores_TOOL_PIN": all(not v for v in kit_ok.values()),
                    "info": "a malformed line whose name token is P112_LAUNCHER_CX2V002X is ignored as another tool's line"}
        assert not bad and observed["kit_parser_ignores_TOOL_PIN"], observed
        return observed
    R.case("A08_TOOL_PIN_CX2V002_gate_under_F2_line_rules_fresh_matrix", "gate", "BLOCKING", a08)

    def a08b():
        f = T.full_launch_fixture(suite, "A08b_F5_boundary")
        variant = V006.replace("/Users/bgm/Research/", "/Users/bgm/research/")
        cfg = dict(f.config_doc, v006=variant)
        pin = suite.raw_write(f.root / "CONFIG_case_variant_v006.json", M.encoded(cfg))
        production = expect_refusal(M, lambda: M.Context(pin, system=M.System()))
        cfg_exact = dict(f.config_doc, v006=V006)
        pin2 = suite.raw_write(f.root / "CONFIG_exact_v006_synthetic.json", M.encoded(cfg_exact))
        synthetic_exact = expect_refusal(M, lambda: M.Context(pin2, system=M.SyntheticSystem(M.read_pin(f.synthetic)["system"]),
                                                              synthetic_pins=f.overrides))
        fence_variant = expect_refusal(M, lambda: M.synthetic_fence(f.overrides, cfg))
        same_inode = os.stat(variant).st_ino == os.stat(V006).st_ino
        read_variant = expect_refusal(M, lambda: M.read_v006(variant))
        dotted = V006.replace("/CLAUDE2/", "/CLAUDE2/./")
        read_dotted = expect_refusal(M, lambda: M.read_v006(dotted))
        v006_opens = [o for o in audit.opens if o["case"] == R.audit.case and os.path.realpath(o["path"]).lower() == V006.lower()]
        observed = {"production_case_variant_config": production, "synthetic_exact_V006": synthetic_exact,
                    "synthetic_fence_on_case_variant": fence_variant if isinstance(fence_variant, str) else "NOT_REFUSED",
                    "case_variant_is_same_file_on_this_FS": same_inode,
                    "read_v006_case_variant": read_variant, "read_v006_dotted_spelling": read_dotted,
                    "tool_opens_of_real_V006": len(v006_opens)}
        assert (production == "V006_CONFIG_PATH" and synthetic_exact == "SYNTHETIC_REAL_V006"
                and read_variant == "PATH_NGC3198" and read_dotted == "V006_PATH" and not v006_opens), observed
        return observed
    R.case("A08b_F5_V006_constant_and_synthetic_boundary_case_variant_and_spellings", "gate", "BLOCKING", a08b)

    # ===================================================================== 5. F1 symlinks at further read sites; hard links
    def a09():
        got, bad = {}, {}

        def note(label, value, want):
            got[label] = value
            if want is not None and value != want:
                bad[label] = {"want": want, "got": value}

        # (1) history: attempt receipt created as a symlink (benign target)
        h = rfix("A09_attempt_receipt_symlink")
        tgt = suite.raw_write(Path(h.root) / "attempt_receipt_target.json", b'{"schema": "STEP5_ATTEMPT_RECEIPT_C2V001"}\n')
        os.symlink(tgt["path"], h.outdir + ".attempt_receipt.json")
        note("history_attempt_receipt_symlink", M.status(h.ctx)["calls"][0]["status"], "RECORD_SYMLINK")
        # (2) close_attempt: .launch.json alias (benign target with identical bytes; fixture file renamed)
        m = rfix("A09_close_launch_json_symlink")
        moved = str(Path(m.root) / "launch_json_moved_outside_run_root.json")
        os.rename(m.outdir + ".receipt.json.launch.json", moved)
        os.symlink(moved, m.outdir + ".receipt.json.launch.json")
        note("close_launch_json_symlink", expect_refusal(M, lambda: M.close_attempt(m.ctx, m.name, 1)), "RECORD_SYMLINK")
        # (3)(4)(5) refusal record monitor logs aliased
        for label, target_kind, want in (("into_outdir_result", "outdir", "FORBIDDEN_RESULT_READ"),
                                         ("into_receipt_stdout", "receipt_stdout", "FORBIDDEN_OUTDIR_READ"),
                                         ("benign_outside_run_roots", "benign", None)):
            n = rfix("A09_refusal_log_" + label, mode="FAILED")
            M.close_attempt(n.ctx, n.name, 1)
            work = Path(n.ctx.cfg["p112_launch_root"]) / "work" / "rv_log_alias"
            work.mkdir()
            outdir2 = M.planned_outdir(n.ctx, n.name, 2, "P112")
            plan = {"schema": "UNT_P112_LAUNCH_PLAN_CX2V001", "name": n.name, "attempt": 2, "outdir": outdir2,
                    "config": n.ctx.config_pin, "caps": M.first_caps(n.name), "solo_mode": False}
            pp = suite.raw_write(work / "plan.json", M.encoded(plan))
            if target_kind == "outdir":
                target = n.outdir + "/result.json"
            elif target_kind == "receipt_stdout":
                target = n.outdir + ".receipt.json.stdout.txt"
            else:
                target = suite.raw_write(Path(n.root) / "benign_log.txt", b"benign\n")["path"]
            os.symlink(target, work / "monitor.stdout.txt")
            se = suite.raw_write(work / "monitor.stderr.txt", b"")
            so_pin = {"path": str(work / "monitor.stdout.txt"), "sha256": sha(Path(target).read_bytes()) if target_kind == "benign" else "0" * 64}
            report = M.encoded({"counts": {}, "last_observation": {}, "date_u": M.date_u()})
            path = Path(n.ctx.cfg["p112_launch_root"]) / "launches" / "P112_P1_M0001_MONITOR_REFUSED_CX2V001_A2.json"
            op = suite.raw_write(str(path) + ".observations.json", report)
            rec = {"schema": "MONITOR_REFUSED_ATTEMPT_RECORD_C2V001", "name": n.name, "attempt": 2, "launcher": "P112_CX2V001",
                   "writer": {"name": M.TOOL_NAME, "sha256": TOOL_SHA}, "plan": pp, "monitor_stdout": so_pin,
                   "monitor_stderr": se, "absent": M.absent_paths(outdir2), "date_u": M.date_u(),
                   "rule": "rv observations_sha256=" + op["sha256"]}
            suite.raw_write(path, M.encoded(rec))
            note("refusal_log_symlink_" + label, M.status(n.ctx)["calls"][0]["status"], want)
        # (6) enforce_solo: another invocation's plan.json aliased
        e = rfix("A09_enforce_solo_plan_symlink")
        wk = Path(e.ctx.cfg["p112_launch_root"]) / "work" / "other_invocation"
        wk.mkdir()
        tgt = suite.raw_write(Path(e.root) / "plan_target.json", M.encoded({"schema": "UNT_P112_LAUNCH_PLAN_CX2V001",
                                                                             "outdir": "/x", "solo_mode": False}))
        os.symlink(tgt["path"], wk / "plan.json")
        note("enforce_solo_plan_symlink", expect_refusal(M, lambda: M.enforce_solo(e.ctx, False, rows=[])), "INFLIGHT_PLAN_UNREADABLE")
        # (7) enforce_solo: same-outdir plan with aliased sampler_first_sample.json
        s = rfix("A09_enforce_solo_first_sample_symlink")
        outdir2 = M.planned_outdir(s.ctx, s.name, 2, "P112")
        wk = Path(s.ctx.cfg["p112_launch_root"]) / "work" / "same_outdir"
        wk.mkdir()
        suite.raw_write(wk / "plan.json", M.encoded({"schema": "UNT_P112_LAUNCH_PLAN_CX2V001", "outdir": outdir2,
                                                     "solo_mode": False, "invocation_pid": 1, "invocation_command": "x"}))
        tgt = suite.raw_write(Path(s.root) / "first_sample_target.json", M.encoded({"sampler_pid": 900123}))
        os.symlink(tgt["path"], wk / "sampler_first_sample.json")
        note("enforce_solo_first_sample_symlink", expect_refusal(M, lambda: M.enforce_solo(
            s.ctx, False, rows=[], requested_outdir=outdir2, own_work="/nonexistent")), "RECORD_SYMLINK")
        # (8) registered_entry: own registry entry aliased
        r = rfix("A09_registry_entry_symlink", record=False)
        reg = M.own_registry_path(r.ctx, r.name)
        os.rename(reg, reg + ".moved")
        os.symlink(reg + ".moved", reg)
        r.call["entry_pin"] = None
        note("registered_entry_symlink", expect_refusal(M, lambda: M.registered_entry(r.ctx, r.call)), "RECORD_SYMLINK")
        # (9) outside-set stop record aliased
        o = rfix("A09_outside_stop_symlink")
        folder = Path(o.ctx.cfg["p112_launch_root"]) / "outside_set_stop"
        tgt = suite.raw_write(Path(o.root) / "stop_target.json", M.encoded({"schema": "S0_OUTSIDE_SET_STOP_RECORD_C2V001"}))
        os.symlink(tgt["path"], folder / "S0_J1_SERIAL_A1_CX2V001.json")
        note("outside_stop_record_symlink", expect_refusal(M, lambda: M.outside_stop_records(o.ctx, "S0_J1_SERIAL")), "RECORD_SYMLINK")
        # (10) assemble --verify: registry file aliased (identical bytes)
        v = rfix("A09_verify_registry_symlink")
        M.close_attempt(v.ctx, v.name, 1)
        res = M.assemble_registry(v.ctx)
        regp = res["registry"]["path"]
        os.rename(regp, regp + ".moved")
        os.symlink(regp + ".moved", regp)
        note("verify_registry_symlink", expect_refusal(M, lambda: M.assemble_registry(v.ctx, verify=True)), "RECORD_SYMLINK")
        # (11) twin kill record aliased
        t = rfix("A09_twin_kill_symlink", name=M.TWIN)
        folder = Path(t.ctx.cfg["p112_launch_root"]) / "twin_kill"
        tgt = suite.raw_write(Path(t.root) / "kill_target.json", M.encoded({"outdir": t.outdir}))
        os.symlink(tgt["path"], folder / "TWIN_KILL_RECORD_rv.json")
        rec = dict(t.record, origin="P112")
        note("twin_kill_record_symlink", expect_refusal(M, lambda: M.bound_stop_record(t.ctx, rec, t.launch_pin)), "RECORD_SYMLINK")
        # (12) maybe_cutoff ALREADY_WRITTEN record aliased (pin_of follows a symlink; informational)
        c = rfix("A09_cutoff_record_symlink")
        cp = M.cutoff_path(c.ctx)
        tgt = suite.raw_write(Path(c.root) / "cutoff_target.json", b'{"schema": "STEP4_CUTOFF_RECORD_C2V001"}\n')
        os.symlink(tgt["path"], cp)
        got["INFO_maybe_cutoff_follows_symlinked_record"] = outcome_of(M, lambda: M.maybe_cutoff(c.ctx))
        observed = {"results": got, "mismatches": bad}
        assert not bad, observed
        return observed
    R.case("A09_F1_symlink_sweep_at_further_monitor_work_record_read_sites", "blinding", "FIX", a09)

    def a10():
        got = {}
        f = rfix("A10_hardlink_receipt_to_result", no_receipt=True)
        os.link(f.outdir + "/result.json", f.outdir + ".receipt.json")
        before = len(audit.forbidden_in(R.audit.case))
        got["status_with_hardlinked_receipt"] = M.status(f.ctx)["calls"][0]["status"]
        hits = audit.forbidden_in(R.audit.case)[before:]
        g = rfix("A10_hardlink_launch_json_to_result")
        alias = M.planned_outdir(g.ctx, g.name, 2, "P112") + ".receipt.json.launch.json"
        os.link(g.outdir + "/result.json", alias)
        b2 = len(audit.forbidden_in(R.audit.case))
        raw, doc = M.try_launch_json(alias)
        hits2 = audit.forbidden_in(R.audit.case)[b2:]
        got["try_launch_json_parsed_result_bytes"] = doc is not None
        observed = {"results": got, "forbidden_inode_opens": len(hits) + len(hits2),
                    "fix": "refuse a monitor/work record whose st_nlink != 1 (fstat after open) before reading"}
        assert len(hits) + len(hits2) == 0, observed
        return observed
    R.case("A10_hardlink_alias_into_outdir_is_not_opened", "blinding", "NOTE", a10)

    # ===================================================================== 6. ps rows: bytes, quoting, blank argv
    tool_path = suite.root / "rv_synthetic_listed_tool.py"
    tool_pin = suite.raw_write(tool_path, b"# synthetic listed tool, never executed\n")
    declared = [{"tool": "rv_synthetic_listed", "path": tool_pin["path"], "sha256": tool_pin["sha256"], "driver_only": False}]

    def rows_for(pids):
        return [r for r in M.System().processes() if r["pid"] in pids]

    def a11():
        argv = [PY.encode(), b"-I", b"-B", b"-c", b"import time; time.sleep(30)", b"bad\xffbyte", b"Brian's",
                b"back\\slash", b"new\nline", b"tab\there", os.fsencode(tool_pin["path"])]
        p = start(argv)
        try:
            time.sleep(0.5)
            rows = rows_for({p.pid})
            counter = M.ProcessCounter(declared=declared, synthetic=True)
            found = counter.count(rows)
            observed = {"row": rows[0]["command"][-90:] if rows else None,
                        "count": len(found), "surrogate_in_row": bool(rows and "\udcff" in rows[0]["command"])}
        finally:
            stop(p)
        assert rows and len(found) == 1, observed
        return observed
    R.case("A11a_surrogateescape_quote_backslash_newline_row_counts_listed_tool_no_crash", "ps", "BLOCKING", a11)

    def a11b():
        argv = [PY, "-I", "-B", "-c", "import time; time.sleep(30)", "it's", tool_pin["path"], "lane's"]
        p = start(argv)
        try:
            time.sleep(0.5)
            rows = rows_for({p.pid})
            found = M.ProcessCounter(declared=declared, synthetic=True).count(rows)
            tokens = M.command_argv(rows[0])
            observed = {"ps_row_tail": rows[0]["command"][-80:], "count_with_tool_shlex_first": len(found),
                        "listed_path_is_a_token": tool_pin["path"] in tokens,
                        "count_if_whitespace_split": int(tool_pin["path"] in rows[0]["command"].split())}
        finally:
            stop(p)
        assert len(found) == 1, observed
        return observed
    R.case("A11b_balanced_apostrophes_around_listed_path_do_not_hide_it", "ps", "FIX", a11b)

    def a11c():
        p = start([" "], executable="/bin/cat", stdin=subprocess.PIPE, env={})
        try:
            time.sleep(0.5)
            raw = subprocess.run(["/bin/ps", "-axww", "-o", "pid=,ppid=,pgid=,command="], capture_output=True).stdout
            line = next((l for l in raw.splitlines() if l.strip().split(None, 1)[0] == str(p.pid).encode()), None)
            result = outcome_of(M, lambda: M.System().processes())
            solo = outcome_of(M, lambda: M.ProcessCounter(synthetic=True).count(M.System().processes()))
        finally:
            p.stdin.close()
            stop(p)
        observed = {"ps_line": repr(line), "System.processes": result if "result" not in result else "PARSED",
                    "consequence": "while such a process exists every poll is ps_ok=false (sample null) and launch/enforce_solo refuse",
                    "count_call": solo if "result" not in solo else "PARSED"}
        assert "result" in result, observed
        return observed
    R.case("A11c_unrelated_process_with_blank_argv_does_not_fail_ps_parse", "ps", "FIX", a11c)

    def a11d():
        f = rfix("A11d_sampler_blank_argv_midrun")
        work = Path(f.root) / "launch_root" / "work" / "blank_argv"
        work.mkdir()
        plan = {"name": f.name, "attempt": 1, "outdir": f.outdir, "config": f.ctx.config_pin}
        clock = {"now": 0.0, "polls": 0}
        holder = {}
        real_ps = M.System().processes

        def processes():
            clock["polls"] += 1
            if clock["polls"] == 2:
                holder["p"] = start([" "], executable="/bin/cat", stdin=subprocess.PIPE, env={})
                time.sleep(0.4)
            if clock["polls"] == 3 and "p" in holder:
                holder["p"].stdin.close()
                stop(holder["p"])
            return real_ps()
        f.ctx.system.processes = processes
        f.ctx.system.monotonic = lambda: clock["now"]
        f.ctx.system.sleep = lambda s: clock.update(now=clock["now"] + s)
        try:
            pin = M.sampler(f.ctx, plan, str(work), poll_s=1)
        finally:
            if "p" in holder:
                holder["p"].stdin.close() if holder["p"].stdin and not holder["p"].stdin.closed else None
                stop(holder["p"])
        sample = json.loads(Path(pin["path"]).read_bytes()) if isinstance(pin, dict) and "path" in pin else pin
        value = M.sample_value(sample, f.rec) if isinstance(sample, dict) and "complete" in sample else None
        observed = {"complete": sample.get("complete") if isinstance(sample, dict) else sample,
                    "polls": clock["polls"], "other_ngc_processes_max_at_close": value}
        assert isinstance(sample, dict) and sample.get("complete") is True and value == 0, observed
        return observed
    R.case("A11d_blank_argv_process_mid_attempt_does_not_null_the_sample", "ps", "FIX", a11d)

    def a11e():
        import threading
        fifo = suite.root / "rv_fifo_named_like_a_script.py"
        os.mkfifo(fifo)
        p = start([PY, "-I", "-B", "-c", "import time; time.sleep(30)", str(fifo)])
        box = {}
        try:
            time.sleep(0.5)
            rows = rows_for({p.pid})

            def run():
                box["found"] = M.ProcessCounter(synthetic=True).count(rows)
            th = threading.Thread(target=run, daemon=True)
            th.start()
            th.join(3.0)
            hung = th.is_alive()
            if hung:  # release the blocked reader: open and close the write end (EOF)
                fd = os.open(fifo, os.O_WRONLY | os.O_NONBLOCK)
                os.close(fd)
                th.join(5.0)
        finally:
            stop(p)
        observed = {"counter_blocked_on_fifo_argument_for_3s": hung, "released_by_harness": hung and not th.is_alive(),
                    "consequence": "the sampler stops polling while blocked: largest gap > 2*poll_s gives a null sample"}
        assert not hung, observed
        return observed
    R.case("A11e_unrelated_process_naming_a_FIFO_with_py_suffix_does_not_block_the_counter", "ps", "NOTE", a11e)

    # ===================================================================== 7. decoy command lines (F3 + sampler)
    def decoy_row(pid, monitor, receipt):
        return {"pid": pid, "ppid": 1, "pgid": pid - 7, "command": "/usr/bin/pgrep -fl " + monitor + " --receipt " + receipt}

    def a12():
        f = resfix("A12_resume_without_monitor_pid_decoy", missing_monitor_pid=True)
        monitor = f.ctx.pins["monitor"]["path"]
        receipt = f.outdir + ".receipt.json"
        f.ctx.system.rows = [decoy_row(900777, monitor, receipt)]
        pin = M.launch_resume(f.ctx, f.name, 1)
        rec = json.loads(Path(pin["path"]).read_bytes())
        k = resfix("A12_resume_decoy_plus_real_monitor", missing_monitor_pid=True)
        real_row = {"pid": 900779, "ppid": 1, "pgid": 900779, "command": " ".join(k.plan["monitor_argv"])}
        k.ctx.system.rows = [real_row, decoy_row(900780, k.ctx.pins["monitor"]["path"], k.outdir + ".receipt.json")]
        both = expect_refusal(M, lambda: M.launch_resume(k.ctx, k.name, 1))
        g = rfix("A12_null_pid_status_with_decoy", no_receipt=True, record=False)
        suite.raw_write(g.record_path, M.encoded(dict(g.record, monitor_pid=None)))
        g.ctx.system.rows = [decoy_row(900778, g.ctx.pins["monitor"]["path"], g.outdir + ".receipt.json")]
        st = M.status(g.ctx)["calls"][0]["status"]
        # live decoy on the real ps
        d = start([PY, "-I", "-B", "-c", "import time; time.sleep(20)", monitor, "--receipt", receipt])
        try:
            time.sleep(0.5)
            live_match = [r["pid"] for r in M.matching_monitors(M.System().processes(), monitor, f.outdir)]
        finally:
            stop(d)
        observed = {"resume_monitor_pid": rec["monitor_pid"], "resume_pid_source": rec["monitor_pid_source"],
                    "resume_with_real_monitor_and_decoy": both,
                    "status_null_pid_with_decoy": st, "live_inert_decoy_matched": d.pid in live_match,
                    "planned_monitor_argv_exact_match_would_reject": True}
        assert rec["monitor_pid"] is None and st == "MONITOR_ENDED_NO_RECEIPT", observed
        return observed
    R.case("A12_resume_without_monitor_pid_json_rejects_decoy_with_similar_command", "F3", "FIX", a12)

    def a13():
        f = rfix("A13_sampler_decoy_mid_attempt")
        monitor = f.ctx.pins["monitor"]["path"]
        receipt = f.outdir + ".receipt.json"
        monitor_row = {"pid": 900801, "ppid": 1, "pgid": 900801,
                       "command": " ".join(M.monitor_command(f.ctx.pins, f.call["spec"], f.outdir, M.first_caps(f.name)))}
        work = Path(f.root) / "launch_root" / "work" / "decoy"
        work.mkdir()
        plan = {"name": f.name, "attempt": 1, "outdir": f.outdir, "config": f.ctx.config_pin}

        def rows(n):
            if n == 1:
                return [monitor_row]
            if n == 2:
                return [monitor_row, decoy_row(900802, monitor, receipt)]
            return []
        accelerate(f.ctx.system, rows_fn=rows)
        result = outcome_of(M, lambda: M.sampler(f.ctx, plan, str(work), poll_s=1))
        solo = os.path.exists(f.outdir + ".solo.json")
        f.ctx.system.processes = lambda: []
        closed = outcome_of(M, lambda: M.close_attempt(f.ctx, f.name, 1))
        value = None
        if "result" in closed:
            value = json.loads(Path(closed["result"]["receipt"]["path"]).read_bytes())["other_ngc_processes_max"]
        planned = " ".join(M.monitor_command(f.ctx.pins, f.call["spec"], f.outdir, M.first_caps(f.name)))
        both = [monitor_row, decoy_row(900802, monitor, receipt)]
        exact = [r["pid"] for r in both if r["command"] == planned and r["pid"] == r["pgid"]]
        observed = {"sampler": result.get("refusal") or ("WROTE" if "result" in result else result),
                    "solo_json_written": solo, "other_ngc_processes_max_at_close": value,
                    "naming_matches_with_decoy": [r["pid"] for r in M.matching_monitors(both, monitor, f.outdir)],
                    "exact_planned_argv_and_group_leader_matches": exact,
                    "trigger": "any process whose argv names the monitor path and '--receipt <receipt>' (e.g. a pgrep/grep of the full command)"}
        assert solo and value == 0, observed
        return observed
    R.case("A13_transient_decoy_command_line_does_not_kill_sampler_or_null_sample", "sampler", "FIX", a13)

    # ===================================================================== 8. kill-target exit 1
    def a14():
        f = rfix("A14_kill_target_exit_one")
        sleeper = suite.raw_write(Path(f.root) / "inert_planned_driver.py", b"import time\ntime.sleep(30)\n")
        f.ctx.pins = dict(f.ctx.pins, driver=sleeper)
        plan = {"name": f.name, "launch_json": f.outdir + ".receipt.json.launch.json", "spec": f.call["spec"], "outdir": f.outdir}
        variants = {
            "warning_then_json": ("import sys\nsys.stderr.write('warning: x\\n{\"alive\": false}\\n')\nsys.exit(1)\n", "NOT_KILLED_TARGET_REFUSED"),
            "two_json_lines": ("import sys\nsys.stderr.write('{\"alive\": false}\\n{\"alive\": false}\\n')\nsys.exit(1)\n", "NOT_KILLED_TARGET_REFUSED"),
            "alive_zero": ("import sys\nsys.stderr.write('{\"alive\": 0}')\nsys.exit(1)\n", "NOT_KILLED_TARGET_REFUSED"),
            "alive_null": ("import sys\nsys.stderr.write('{\"alive\": null}')\nsys.exit(1)\n", "NOT_KILLED_TARGET_REFUSED"),
            "exit3_alive_false": ("import sys\nsys.stderr.write('{\"alive\": false}')\nsys.exit(3)\n", "NOT_KILLED_TARGET_REFUSED"),
            "duplicate_alive_key": ("import sys\nsys.stderr.write('{\"alive\": false, \"alive\": false}')\nsys.exit(1)\n", "NOT_KILLED_TARGET_REFUSED"),
            "non_utf8_stderr": ("import sys\nsys.stderr.buffer.write(b'\\xff{\"alive\": false}')\nsys.exit(1)\n", "NOT_KILLED_TARGET_REFUSED"),
        }
        got, bad = {}, {}
        for label, (src, want) in variants.items():
            f.ctx.pins = dict(f.ctx.pins, kit=stub_kit("A14_" + label, src))
            r = outcome_of(M, lambda: M.kit_kill_target(f.ctx, plan))
            got[label] = r["result"]["result"] if "result" in r else r
            if got[label] != want:
                bad[label] = {"want": want, "got": got[label]}
        # Kit reports alive:false (exit 1) while the planned driver command is visibly alive.
        argv = M.driver_command(f.ctx.pins, f.call["spec"], f.outdir)
        d = start(argv)
        try:
            time.sleep(0.5)
            visible = [r["pid"] for r in M.System().processes() if r["command"] == " ".join(argv) and r["pid"] == r["pgid"]]
            f.ctx.pins = dict(f.ctx.pins, kit=stub_kit("A14_lying_alive_false", "import sys\nsys.stderr.write('{\"alive\": false}')\nsys.exit(1)\n"))
            r = outcome_of(M, lambda: M.kit_kill_target(f.ctx, plan))
            got["kit_alive_false_while_planned_driver_visible"] = {"result": r.get("result", r), "visible_pids": visible,
                                                                   "still_alive_after": d.poll() is None}
            if r.get("result", {}).get("result") == "ALREADY_ENDED" and visible:
                bad["kit_alive_false_while_planned_driver_visible"] = {"want": "cross-check own ps before ALREADY_ENDED",
                                                                       "got": "ALREADY_ENDED"}
        finally:
            stop(d)
        observed = {"results": got, "mismatches": bad}
        assert not bad, observed
        return observed
    R.case("A14_kill_target_exit_one_variants_and_no_cross_check_of_alive_false", "F4", "FIX", a14)

    # ===================================================================== 9. malformed-shape parseable launch.json
    def a15():
        f = resfix("A15_launch_json_wrong_shapes")
        target = f.outdir + ".receipt.json.launch.json"
        accelerate(f.ctx.system, rows_fn=lambda n: [], step=100.0)
        f.ctx.pins = dict(f.ctx.pins, kit=stub_kit("A15", "import sys\nsys.stderr.write('{\"alive\": false}')\nsys.exit(1)\n"))
        with swap_reads(target, lambda n, raw: b'{"pins": [1], "caps": [1], "utc": 5, "child_pid": 7}\n'):
            r1 = outcome_of(M, lambda: M.launch_resume(f.ctx, f.name, 1))
        g = rfix("A15_close_launch_json_list")
        with swap_reads(g.outdir + ".receipt.json.launch.json", lambda n, raw: b"[]\n"):
            r2 = outcome_of(M, lambda: M.close_attempt(g.ctx, g.name, 1))
        cli_catches = "AttributeError" in Path(TOOL).read_text().split("def cli(")[1]
        observed = {"resume_with_dict_but_list_fields": r1, "close_with_list_launch_json": r2,
                    "cli_except_tuple_catches_AttributeError": cli_catches}
        assert "exception" not in r1 and "exception" not in r2, observed
        return observed
    R.case("A15_parseable_launch_json_with_wrong_field_shapes_refuses_not_crashes", "volatile", "NOTE", a15)

    # ===================================================================== 10. static + audit-hook single-read inventory
    def a16_static():
        src = Path(TOOL).read_text()
        tree = ast.parse(src)
        parents = {}
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                parents[child] = node

        def enclosing(node):
            while node in parents:
                node = parents[node]
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    return node.name
            return "<module>"
        sites = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                fn = node.func
                label = None
                if isinstance(fn, ast.Attribute) and fn.attr in ("read_bytes", "read_text", "open"):
                    label = fn.attr
                elif isinstance(fn, ast.Name) and fn.id == "open":
                    label = "open"
                elif isinstance(fn, ast.Attribute) and fn.attr == "open" and isinstance(fn.value, ast.Name) and fn.value.id == "os":
                    label = "os.open"
                if label:
                    sites.append({"line": node.lineno, "call": label, "function": enclosing(node)})
        allowed = {"read_and_pin": "immutable snapshot", "observe_file": "volatile observation",
                   "identify": "counter identity probe", "write_x_bytes": "write/dir-fsync",
                   "new_log": "write log", "create_layout": "mkdir"}
        unexpected = [s for s in sites if s["function"] not in allowed]
        observed = {"read_open_sites": sites, "unexpected_sites": unexpected,
                    "classes": {k: v for k, v in allowed.items()}}
        assert not unexpected, observed
        return observed
    R.case("A16a_static_inventory_every_byte_read_goes_through_one_of_three_readers", "single-read", "BLOCKING", a16_static)

    def audited(label, fn):
        with audit.operation(label):
            result = outcome_of(M, fn)
        dup, n = audit.duplicate_immutable_reads()
        vol = [r for r in audit.op_reads if r["volatile"]]
        return {"label": label, "outcome": "OK" if "result" in result else result, "immutable_reads": n,
                "duplicates": dup, "volatile_reads": len(vol),
                "counter_reads": len([r for r in audit.op_reads if r["counter"]])}

    def cli_op(label, f, args, expect_codes=()):
        common = ["--config", f.config["path"], "--config-sha256", f.config["sha256"],
                  "--synthetic-pins", f.synthetic["path"], "--synthetic-pins-sha256", f.synthetic["sha256"]]
        buf = io.StringIO()

        def run():
            with contextlib.redirect_stdout(buf):
                rc = M.cli([args[0]] + common + list(args[1:]))
            return {"rc": rc, "out": json.loads(buf.getvalue().strip().splitlines()[-1])}
        with audit.operation(label):
            res = outcome_of(M, run)
        dup, n = audit.duplicate_immutable_reads()
        v006 = [r for r in audit.op_reads if r["path"] == f.config_doc["v006"]]
        out = res.get("result") or {}
        ok = out.get("rc") == 0 or (out.get("out") or {}).get("code") in expect_codes
        return {"label": label, "outcome": "OK" if ok else res, "rc": out.get("rc"),
                "code": (out.get("out") or {}).get("code"), "immutable_reads": n, "duplicates": dup,
                "v006_reads": len(v006), "v006_reads_volatile": all(r["volatile"] for r in v006),
                "volatile_reads": len([r for r in audit.op_reads if r["volatile"]]),
                "counter_reads": len([r for r in audit.op_reads if r["counter"]]),
                "result": out.get("out")}

    def a16_dynamic():
        ops = []
        f = T.full_launch_fixture(suite, "A16_full")
        M.READ_RUN_ROOTS.update((f.config_doc["run_root"], f.config_doc["s0"]["run_root"]))
        ops.append(cli_op("cli_status", f, ["status"]))
        watch = start([PY, "-I", "-B", f.watch["path"]])
        live_rec = {}
        try:
            time.sleep(0.3)
            ops.append(cli_op("cli_launch_dry", f, ["launch", "--name", f.name, "--dry"]))
            # new_work names <name>_A<k>_<UTC second>_<pid>; separate CLI processes never share a pid, but this
            # in-process harness does, so wait past the second boundary (INFO, not a production path).
            time.sleep(1.2)
            op = cli_op("cli_launch_live_synthetic", f, ["launch", "--name", f.name, "--attempt", "1"])
            ops.append(op)
            live_rec["pin"] = op.get("result")
            outdir = str(Path(f.config_doc["run_root"]) / "NGC_P1_P1_M0001_RUN_CX2V001_A1")
            until = time.monotonic() + 40
            while not Path(outdir + ".solo.json").is_file() and time.monotonic() < until:
                time.sleep(0.2)
            time.sleep(0.8)
            if os.path.isdir(outdir):
                audit.register_forbidden_tree(outdir, outdir + ".receipt.json")
            ops.append(cli_op("cli_close_attempt_live", f, ["close-attempt", "--name", f.name, "--attempt", "1"]))
            ops.append(cli_op("cli_status_after_close", f, ["status"]))
            ops.append(cli_op("cli_assemble_registry_not_ready", f, ["assemble-registry"],
                              expect_codes=("REGISTRY_ENTRY_MISSING",)))
        finally:
            stop(watch)
        v006_reads = [o["v006_reads"] for o in ops]
        g = rfix("A16_receipt")
        ops.append(audited("close_attempt_receipt_fixture", lambda: M.close_attempt(g.ctx, g.name, 1) and "ok"))
        ops.append(audited("assemble_registry", lambda: M.assemble_registry(g.ctx) and "ok"))
        ops.append(audited("assemble_registry_verify", lambda: M.assemble_registry(g.ctx, verify=True) and "ok"))
        ops.append(audited("status_receipt_fixture", lambda: M.status(g.ctx) and "ok"))
        h = resfix("A16_resume", missing_monitor_pid=True)
        ops.append(audited("launch_resume", lambda: M.launch_resume(h.ctx, h.name, 1) and "ok"))
        e = T.observation_refusal_fixture(suite, "A16_refusal_emit", variant="emit")
        ops.append(audited("record_monitor_refused", lambda: M.record_monitor_refused(e.ctx, e.refusal_plan, str(e.refusal_work)) and "ok"))
        ops.append(audited("status_after_refusal", lambda: M.status(e.ctx) and "ok"))
        s = rfix("A16_sampler")
        work = Path(s.root) / "launch_root" / "work" / "audit_sampler"
        work.mkdir()
        mp = suite.raw_write(work / "monitor_pid.json", M.encoded({"monitor_pid": 900991}))
        accelerate(s.ctx.system, rows_fn=lambda n: [])
        ops.append(audited("sampler", lambda: M.sampler(s.ctx, {"name": s.name, "attempt": 1, "outdir": s.outdir,
                                                                 "config": s.ctx.config_pin}, str(work), poll_s=1) and "ok"))
        c = rfix("A16_cutoff")
        ops.append(audited("write_cutoff", lambda: M.write_cutoff(c.ctx, cutoff_terms(c)) and "ok"))
        bad = [o for o in ops if o and (o["duplicates"] or o["outcome"] != "OK")]
        live = live_rec.get("pin") or {}
        observed = {"operations": [o for o in ops if o], "violations": bad,
                    "cli_v006_reads_per_operation": v006_reads,
                    "live_launch_record_outcome": json.loads(Path(live["path"]).read_bytes())["outcome"] if live.get("path") else None}
        assert not bad and all(n == 1 for n in v006_reads) and observed["live_launch_record_outcome"] == "LAUNCH", observed
        return observed
    R.case("A16b_audit_hook_single_read_inventory_path_realpath_inode_per_operation", "single-read", "BLOCKING", a16_dynamic)

    # ----------------------------------------------------------------- finish
    for p in live:
        stop(p)
    finished = date_u()
    rows = R.rows
    summary = Counter(r["status"] for r in rows)
    result = {"schema": "ROOTVERIFY_P112_CX2V002_FRESH_ADVERSARIAL_C2V001", "date_u_start": started, "date_u_end": finished,
              "tool": own_pin, "tests": {"path": TESTS, "sha256": TESTS_SHA},
              "harness": {"path": str(Path(__file__).resolve()), "sha256": sha(Path(__file__).read_bytes())},
              "summary": dict(summary), "cases": rows,
              "forbidden_opens_total": len(audit.forbidden),
              "forbidden_opens_outside_cases": [x for x in audit.forbidden if not x["case"].startswith(("A", "between"))],
              "tool_opens_total": len(audit.opens),
              "live_processes_left": [p.pid for p in live if p.poll() is None]}
    raw = (json.dumps(result, sort_keys=True, indent=1, default=str) + "\n").encode()
    with (out / "ROOTVERIFY_FRESH_ADVERSARIAL_RESULT.json").open("xb") as h:
        h.write(raw)
        h.flush()
        os.fsync(h.fileno())
    os.chmod(out / "ROOTVERIFY_FRESH_ADVERSARIAL_RESULT.json", 0o444)
    print(json.dumps({"summary": dict(summary), "result_sha256": sha(raw),
                      "fails": [(r["name"], r["status"]) for r in rows if r["status"] != "PASS"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

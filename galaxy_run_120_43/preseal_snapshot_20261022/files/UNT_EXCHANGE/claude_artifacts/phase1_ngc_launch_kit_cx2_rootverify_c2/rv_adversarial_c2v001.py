"""Root verify (Claude2 lineage), P-112 CX2V001: adversarial synthetic tests.

Each case asserts the behaviour the spec of record requires (brief V005 + ROUND5 + 0782 + A223 + A226 item 1).
A FAIL row is a confirmed deviation; `severity` says how root should weigh it. Synthetic only: every file is
created under --out by exclusive create; only processes started here are signalled; no network; no NGC3198
data, run trees, V007_POSTSEAL_RECORDS or ~/.codex are opened (an audit hook checks P-112 opens, by path and
realpath). Pinned-file changes between two reads are simulated by patching Path.read_bytes in memory; no
fixture file is modified or deleted.
"""
import argparse
import contextlib
import hashlib
import io
import json
import math
import os
import pathlib
import re
import signal
import subprocess
import sys
import time
import traceback
import types
from pathlib import Path

KIT = "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/phase1_ngc_launch_kit_cx2/"
TOOL = KIT + "phase1_ngc_launch_cx2v001.py"
TOOL_SHA = "a72d96c150ca1c638474cddba23f5264374c7ae9aa285c3d38ebfb3e61519bb1"
TESTS = KIT + "test_phase1_ngc_launch_cx2v001.py"
TESTS_SHA = "fd50301bbbe4e4d6e91ad30a4881eaab6f54a1ab77a1856edea04b9d9670b76e"
V006 = ("/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/"
        "CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md")
OUTDIR_COMPONENT = re.compile(r"^NGC_P1_.+_RUN_(?:CX2V001|C2V003A)_A[0-9]+$")
PIN_LINE = "TOOL_PIN P112_LAUNCHER_CX2V001 %s %s" % (TOOL_SHA, TOOL)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def verified(path, want):
    raw = Path(path).read_bytes()
    if sha(raw) != want:
        raise SystemExit("PIN_MISMATCH " + path)
    return raw


def forbidden_reason(path):
    if path == V006:
        return None
    parts = Path(path).parts
    low = [p.lower() for p in parts]
    base = low[-1] if low else ""
    if base in ("result.json", "finish.json", "progress.jsonl"):
        return "RESULT_FILE"
    if "stages" in low:
        return "STAGES"
    if any("ngc3198" in p for p in low):
        return "NGC3198_COMPONENT"
    if "v007_postseal_records" in low or "a_side" in low or ".codex" in low:
        return "SEALED_OR_CODEX"
    if path.endswith((".receipt.json.stdout.txt", ".receipt.json.stderr.txt")):
        return "RECEIPT_STDIO"
    for p in parts[:-1]:
        if OUTDIR_COMPONENT.match(p):
            return "INSIDE_OUTDIR"
    return None


class Audit:
    def __init__(self):
        self.case = "setup"
        self.opens = []
        self.forbidden = []

    def hook(self, event, args):
        if event != "open" or not isinstance(args[0], (str, bytes)):
            return
        frame = sys._getframe(1)
        while frame is not None and frame.f_code.co_filename != TOOL:
            frame = frame.f_back
        if frame is None:
            return
        path = args[0].decode() if isinstance(args[0], bytes) else args[0]
        real = os.path.realpath(path)
        self.opens.append((self.case, path, args[1]))
        for spelling in dict.fromkeys((path, real)):
            reason = forbidden_reason(spelling)
            if reason is not None:
                self.forbidden.append({"case": self.case, "path": path, "realpath": real, "reason": reason})
                break

    def reads(self, case, target):
        return sum(1 for c, p, m in self.opens if c == case and p == target and isinstance(m, str) and "r" in m)

    def forbidden_in(self, case):
        return [x for x in self.forbidden if x["case"] == case]


@contextlib.contextmanager
def swap_reads(target, switch_at, mutate):
    """Simulate a pinned file whose bytes change between two reads in one process (in memory only)."""
    original = pathlib.Path.read_bytes
    state = {"n": 0, "shas": []}

    def patched(self):
        raw = original(self)
        if str(self) == target:
            state["n"] += 1
            if state["n"] >= switch_at:
                raw = mutate(raw)
            state["shas"].append(sha(raw))
        return raw
    pathlib.Path.read_bytes = patched
    try:
        yield state
    finally:
        pathlib.Path.read_bytes = original


def add_key(raw):
    doc = json.loads(raw)
    doc["rv_changed_between_reads"] = True
    return (json.dumps(doc, sort_keys=True, indent=1) + "\n").encode()


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
        except Exception as e:  # unexpected error is a harness failure, reported as such
            row.update(status="ERROR", observed=repr(e), trace=traceback.format_exc(limit=6))
        forbidden = self.audit.forbidden_in(name)
        if forbidden:
            row["forbidden_opens"] = forbidden
        self.rows.append(row)
        self.audit.case = "between:" + name
        return row


def expect_refusal(M, action):
    try:
        result = action()
    except M.Refusal as e:
        return e.code
    return {"no_refusal": True, "result": result if isinstance(result, (str, dict, list, type(None))) else repr(result)}


def wait_until(predicate, timeout):
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        if predicate():
            return True
        time.sleep(0.1)
    return predicate()


def pid_alive(pid):
    out = subprocess.run(["/bin/ps", "-o", "pid=", "-p", str(pid)], capture_output=True, text=True).stdout
    return bool(out.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = Path(a.out)
    verified(TOOL, TOOL_SHA)
    tests_raw = verified(TESTS, TESTS_SHA)
    started = subprocess.check_output(["/bin/date", "-u"], env=dict(os.environ, LC_ALL="C"), text=True).strip()
    audit = Audit()
    sys.addaudithook(audit.hook)
    T = types.ModuleType("_rootverify_vendor_fixtures")
    T.__file__ = TESTS
    exec(compile(tests_raw, TESTS, "exec"), T.__dict__)
    suite = T.Suite(TOOL, str(out), TOOL_SHA)  # verifies the tool bytes and execs them; mkdir(out) must be new
    M = suite.module
    R = Runner(audit)
    own_pin = {"path": TOOL, "sha256": TOOL_SHA}
    live = []  # every process this harness starts

    def start(argv):
        p = subprocess.Popen(argv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        live.append(p)
        return p

    # ------------------------------------------------------------------ lens 1: A226 single-read
    def rv01():
        f = T.resume_fixture(suite, "RV01_launch_record_double_read")
        target = f.outdir + ".receipt.json.launch.json"
        checked = Path(target).read_bytes()
        with swap_reads(target, 2, add_key) as st:
            rec = M.read_pin(M.launch_resume(f.ctx, f.name, 1))
        observed = {"p112_reads_of_launch_json": st["n"], "verdict": rec["launch_check"]["verdict"],
                    "checked_bytes_sha256": sha(checked), "record_launch_json_sha256": rec["launch_json"]["sha256"],
                    "sites": "checked: finish_launch->wait_launch_json L1980 (try_launch_json L1123); "
                             "recorded: write_launch_record L1956 (and L1960)"}
        assert rec["launch_json"]["sha256"] == sha(checked), observed
        return observed
    R.case("RV01_A226_LAUNCH_record_pins_the_checked_launch_json", "A226", "BLOCKING", rv01)

    def rv02():
        f = T.receipt_fixture(suite, "RV02_nonattempt_receipt_double_read", off_spec=True)
        target = f.outdir + ".receipt.json"
        classified = Path(target).read_bytes()
        with swap_reads(target, 2, add_key) as st:
            h = M.history(f.ctx, f.call)
        n = h["nonattempts"][0]
        observed = {"reason": n["reason"], "p112_reads_of_receipt": st["n"], "classified_sha256": sha(classified),
                    "pinned_sha256": n["monitor_receipt"]["sha256"],
                    "sites": "classified: history L1469-1471; pinned: history L1474 pin_of(receipt_path)"}
        assert n["monitor_receipt"]["sha256"] == sha(classified), observed
        return observed
    R.case("RV02_A226_nonattempt_pin_is_the_classified_receipt", "A226", "BLOCKING", rv02)

    def rv03():
        f = T.receipt_fixture(suite, "RV03_verify_double_read")
        M.close_attempt(f.ctx, f.name, 1)
        M.assemble_registry(f.ctx)
        target = str(Path(f.ctx.cfg["p112_launch_root"]) / "assembly" / "STEP5_LAUNCH_REGISTRY_PHASE1_CX2V001.json")
        compared = Path(target).read_bytes()
        with swap_reads(target, 2, lambda raw: raw + b" ") as st:
            result = M.assemble_registry(f.ctx, verify=True)
        observed = {"status": result["status"], "p112_reads": st["n"], "compared_sha256": sha(compared),
                    "reported_pin_sha256": result["registry"]["sha256"],
                    "sites": "compared: assemble_registry L1771; pinned: L1773 pin_of(p)"}
        assert result["registry"]["sha256"] == sha(compared), observed
        return observed
    R.case("RV03_A226_verify_reports_the_compared_registry_bytes", "A226", "BLOCKING", rv03)

    def rv04():
        f = T.receipt_fixture(suite, "RV04_control_pin_then_verified_read")
        target = str(f.record_path)
        with swap_reads(target, 2, add_key):
            code_records = expect_refusal(M, lambda: f.ctx.records(f.name))
        target = f.outdir + ".receipt.json"
        with swap_reads(target, 2, add_key):
            code_close = expect_refusal(M, lambda: M.close_attempt(f.ctx, f.name, 1))
        observed = {"records_pin_of_then_read_pin": code_records, "close_receipt_pin_of_then_read_pin": code_close}
        assert code_records == "PIN_SHA_MISMATCH" and code_close == "PIN_SHA_MISMATCH", observed
        return observed
    R.case("RV04_A226_control_pin_of_then_read_pin_fails_closed", "A226", "NOTE", rv04)

    # ------------------------------------------------------------------ lens 2: blinding (symlink aliases)
    def rv05():
        f = T.receipt_fixture(suite, "RV05_receipt_symlink_into_outdir", no_receipt=True)
        os.symlink(f.outdir + "/finish.json", f.outdir + ".receipt.json")
        before = len(audit.forbidden_in(R.audit.case))
        status = M.status(f.ctx)
        hits = audit.forbidden_in(R.audit.case)[before:]
        observed = {"status": status["calls"][0]["status"], "forbidden_opens": hits,
                    "site": "history L1469 Path(receipt_path).read_bytes() has no guard_read"}
        assert not hits, observed
        return observed
    R.case("RV05_blinding_status_never_opens_outdir_via_receipt_alias", "blinding", "FIX", rv05)

    def rv06():
        g = T.receipt_fixture(suite, "RV06_launch_json_alias_into_outdir", mode="COMPLETED")
        # A new attempt path k=2 whose launch.json is an alias of attempt 1's outdir/result.json.
        outdir2 = M.planned_outdir(g.ctx, g.name, 2, "P112")
        os.symlink(g.outdir + "/result.json", outdir2 + ".receipt.json.launch.json")
        before = len(audit.forbidden_in(R.audit.case))
        raw, doc = M.try_launch_json(outdir2 + ".receipt.json.launch.json")
        hits = audit.forbidden_in(R.audit.case)[before:]
        observed = {"parsed_alias": doc is not None, "forbidden_opens": hits,
                    "site": "try_launch_json L1123 (used by sampler L1234, finish_launch, stop_launch_failure, "
                            "write_launch_record) has no guard_read"}
        assert not hits, observed
        return observed
    R.case("RV06_blinding_launch_json_reader_never_follows_alias_into_outdir", "blinding", "FIX", rv06)

    def rv07():
        g = T.receipt_fixture(suite, "RV07b_alias_target")
        # close_attempt reads through pin_of/read_pin -> guard_read: an alias of .solo.json into an outdir refuses.
        h = T.receipt_fixture(suite, "RV07c_solo_alias")
        os.symlink(g.outdir + "/result.json", h.outdir + ".solo.json")
        before = len(audit.forbidden_in(R.audit.case))
        code = expect_refusal(M, lambda: M.close_attempt(h.ctx, h.name, 1))
        hits = audit.forbidden_in(R.audit.case)[before:]
        observed = {"close_with_solo_alias": code, "forbidden_opens": hits}
        assert code == "FORBIDDEN_RESULT_READ" and not hits, observed
        return observed
    R.case("RV07_blinding_guarded_reads_refuse_alias_control", "blinding", "NOTE", rv07)

    # ------------------------------------------------------------------ lens 3: TOOL_PIN spoofing
    def rv08():
        accepted = {}
        for label, sep in (("U+2028", " "), ("U+2029", " "), ("FF", "\x0c"), ("VT", "\x0b"),
                           ("RS", "\x1e"), ("FS", "\x1c"), ("GS", "\x1d"), ("NEL", "\x85"), ("lone_CR", "\r")):
            text = "## A999: synthetic\nRoot writes the adoption line later, as in" + sep + PIN_LINE + "\n"
            accepted[label] = expect_refusal(M, lambda text=text: M.tool_gate(text, own_pin))
        kit = M.load_verified(M.REAL["writer"], "_rv_kit_pin_parser")
        spec_line = "SPEC_PIN P1_M0001 %s /synthetic/spec.json" % ("a" * 64)
        kit_view = kit.parse_v006_pins(("## A999: synthetic\nmention " + spec_line + "\n").encode())["pins"]["SPEC_PIN"]
        observed = {"gate_result_per_separator": {k: (v if isinstance(v, str) else "ACCEPTED_AS_PIN_LINE")
                                                   for k, v in accepted.items()},
                    "kit_parser_same_layout_sees_pin": bool(kit_view),
                    "site": "tool_gate L293 and residual_lines L316 use str.splitlines(); the kit splits on '\\n'"}
        assert all(v == "TOOL_PIN_MISSING" for v in accepted.values()), observed
        return observed
    R.case("RV08_TOOL_PIN_mid_line_mention_behind_unicode_or_control_separator", "TOOL_PIN", "FIX", rv08)

    def rv09():
        sha_up = TOOL_SHA.upper()
        cases = {
            "valid": ("## A999: x\n" + PIN_LINE + "\n", "PASS"),
            "valid_under_A108_continued": ("## A108 continued\n" + PIN_LINE + "\n", "PASS"),
            "valid_CRLF": ("## A999: x\r\n" + PIN_LINE + "\r\n", "PASS"),
            "near_miss_longer_name": ("## A999: x\nTOOL_PIN P112_LAUNCHER_CX2V0010 %s %s\n" % (TOOL_SHA, TOOL), "TOOL_PIN_MISSING"),
            "near_miss_suffix_X": ("## A999: x\nTOOL_PIN P112_LAUNCHER_CX2V001X %s %s\n" % (TOOL_SHA, TOOL), "TOOL_PIN_MISSING"),
            "successor_name_ignored": ("## A999: x\n" + PIN_LINE + "\nTOOL_PIN P112_LAUNCHER_CX2V002 %s %s\n" % ("b" * 64, TOOL), "PASS"),
            "tab_separator": ("## A999: x\nTOOL_PIN P112_LAUNCHER_CX2V001\t%s %s\n" % (TOOL_SHA, TOOL), "TOOL_PIN_MISMATCH"),
            "trailing_space": ("## A999: x\n" + PIN_LINE + " \n", "TOOL_PIN_MISMATCH"),
            "upper_sha": ("## A999: x\nTOOL_PIN P112_LAUNCHER_CX2V001 %s %s\n" % (sha_up, TOOL), "TOOL_PIN_MISMATCH"),
            "relative_path": ("## A999: x\nTOOL_PIN P112_LAUNCHER_CX2V001 %s rel/tool.py\n" % TOOL_SHA, "TOOL_PIN_MISMATCH"),
            "mid_line_backticks": ("## A999: x\nRoot writes `" + PIN_LINE + "` later.\n", "TOOL_PIN_MISSING"),
            "indented_ignored": ("## A999: x\n  " + PIN_LINE + "\n", "TOOL_PIN_MISSING"),
            "two_identical_pins": ("## A999: x\n" + PIN_LINE + "\n## A1000: y\n" + PIN_LINE + "\n", "TOOL_PIN_DUPLICATE"),
            "valid_plus_bad_second": ("## A999: x\n" + PIN_LINE + "\nTOOL_PIN P112_LAUNCHER_CX2V001 %s %s\n" % ("c" * 64, TOOL), "TOOL_PIN_DUPLICATE"),
            "before_any_heading": (PIN_LINE + "\n## A999: x\n", "TOOL_PIN_MISMATCH"),
            "under_non_entry_heading": ("## Notes\n" + PIN_LINE + "\n", "TOOL_PIN_MISMATCH"),
            "other_sha": ("## A999: x\nTOOL_PIN P112_LAUNCHER_CX2V001 %s %s\n" % ("d" * 64, TOOL), "TOOL_PIN_MISMATCH"),
            "other_realpath": ("## A999: x\nTOOL_PIN P112_LAUNCHER_CX2V001 %s %s\n" % (TOOL_SHA, TOOL + ".copy"), "TOOL_PIN_MISMATCH"),
        }
        got = {}
        for label, (text, want) in cases.items():
            r = expect_refusal(M, lambda text=text: M.tool_gate(text, own_pin))
            got[label] = "PASS" if isinstance(r, dict) else r
        link = out / "rv09_tool_symlink.py"
        os.symlink(TOOL, link)
        r = expect_refusal(M, lambda: M.tool_gate("## A999: x\nTOOL_PIN P112_LAUNCHER_CX2V001 %s %s\n" % (TOOL_SHA, link), own_pin))
        got["symlink_path_not_realpath"] = "PASS" if isinstance(r, dict) else r
        cases["symlink_path_not_realpath"] = (None, "TOOL_PIN_MISMATCH")
        r = expect_refusal(M, lambda: M.tool_gate("## A230. dotted entry heading\n" + PIN_LINE + "\n", own_pin))
        got["kit_style_dotted_heading_INFO"] = "PASS" if isinstance(r, dict) else r
        bad = {k: (got[k], w) for k, (_, w) in cases.items() if got[k] != w}
        observed = {"results": got, "mismatches": bad,
                    "info": "a '## A230.' heading is an entry for the kit ENTRY_RE but not for P-112 (fail-closed)"}
        assert not bad, observed
        return observed
    R.case("RV09_TOOL_PIN_near_miss_grammar_matrix", "TOOL_PIN", "BLOCKING", rv09)

    def rv10():
        good = "## A999: x\nRESIDUAL_RETRY P1_M0001 1\nRESIDUAL_RETRY P1_M0001 1\n"
        got = {"valid_and_duplicate_act_as_one": sorted(M.residual_lines(good))}
        for label, text in (("leading_zero", "## A999: x\nRESIDUAL_RETRY P1_M0001 01\n"),
                            ("trailing_space", "## A999: x\nRESIDUAL_RETRY P1_M0001 1 \n"),
                            ("lower_name", "## A999: x\nRESIDUAL_RETRY p1_m0001 1\n"),
                            ("k_zero", "## A999: x\nRESIDUAL_RETRY P1_M0001 0\n"),
                            ("before_heading", "RESIDUAL_RETRY P1_M0001 1\n## A999: x\n")):
            got[label] = expect_refusal(M, lambda text=text: M.residual_lines(text))
        for label, text in (("indented", "## A999: x\n  RESIDUAL_RETRY P1_M0001 1\n"),
                            ("mid_line", "## A999: x\nroot may write RESIDUAL_RETRY P1_M0001 1 later\n")):
            got[label] = sorted(M.residual_lines(text))
        got["mid_line_behind_U+2028"] = sorted(M.residual_lines("## A999: x\nquote RESIDUAL_RETRY P1_M0001 1\n"))
        got["INFO_RESIDUAL_RETRY_underscore_word"] = expect_refusal(
            M, lambda: M.residual_lines("## A999: x\nRESIDUAL_RETRY_LINES are parsed anchored\n"))
        observed = {"results": got}
        ok = (got["valid_and_duplicate_act_as_one"] == [["P1_M0001", 1]] and
              all(got[k] == "RESIDUAL_RETRY_MALFORMED" for k in
                  ("leading_zero", "trailing_space", "lower_name", "k_zero", "before_heading")) and
              got["indented"] == [] and got["mid_line"] == [] and got["mid_line_behind_U+2028"] == [])
        assert ok, observed
        return observed
    R.case("RV10_RESIDUAL_RETRY_anchored_parse_matrix", "RESIDUAL_RETRY", "FIX", rv10)

    # ------------------------------------------------------------------ lens 3: sampler / solo / ps
    apostrophe_row = {"pid": 777001, "ppid": 1, "pgid": 777001,
                      "command": "/bin/bash -lc echo Brian's lane note"}
    clean_row = {"pid": 777002, "ppid": 1, "pgid": 777002, "command": "/bin/sleep 600"}

    def rv11():
        p = start([M.PY, "-I", "-B", "-c", "import time; time.sleep(20)", "Bob" + chr(39) + "s file"])
        try:
            time.sleep(0.4)
            rows = M.System().processes()
            row = [r for r in rows if r["pid"] == p.pid][0]
            code = expect_refusal(M, lambda: M.command_argv(row))
        finally:
            p.terminate()
            p.wait(timeout=5)
        observed = {"real_ps_row": row["command"][-40:], "command_argv": code,
                    "consequence": "ProcessCounter.count raises; the sampler marks the poll failed"}
        assert code != "PS_COMMAND_PARSE", observed
        return observed
    R.case("RV11_real_ps_row_with_apostrophe_is_not_a_ps_failure", "sampler", "BLOCKING", rv11)

    class NoDecision(Exception):
        pass

    def accelerate(f, rows_by_poll, max_sleeps=None):
        clock = {"now": 0.0, "polls": 0, "sleeps": 0}
        system = f.ctx.system
        system.monotonic = lambda: clock["now"]

        def sleep(seconds):
            clock["sleeps"] += 1
            if max_sleeps is not None and clock["sleeps"] > max_sleeps:
                raise NoDecision("sampler made no decision")
            clock["now"] += seconds
        system.sleep = sleep

        def processes():
            clock["polls"] += 1
            return list(rows_by_poll(clock["polls"]))
        system.processes = processes
        return clock

    def sampler_fixture(label):
        f = T.receipt_fixture(suite, label)
        work = f.root / "launch_root" / "work" / "rv_sampler"
        work.mkdir()
        plan = {"name": f.name, "attempt": 1, "outdir": f.outdir, "config": f.ctx.config_pin}
        return f, work, plan

    def rv12():
        f, work, plan = sampler_fixture("RV12_transient_apostrophe_row")
        accelerate(f, lambda n: [clean_row, apostrophe_row] if n in (2, 3) else [clean_row])
        pin = M.sampler(f.ctx, plan, str(work), poll_s=1)
        sample = M.read_pin(pin)
        rec = M.monitor_receipt(Path(f.outdir + ".receipt.json").read_bytes())
        ts = M.timestamp
        fmt = lambda t: M.dt.datetime.fromtimestamp(t, M.dt.timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")
        aligned = dict(sample, first_utc=fmt(ts(rec["utc_start"]) - 2), last_utc=fmt(ts(rec["utc_end"]) + 2))
        observed = {"complete": sample["complete"], "max_other_ngc_processes": sample["max_other_ngc_processes"],
                    "value_with_honest_lead_tail": M.sample_value(aligned, rec),
                    "same_with_complete_true": M.sample_value(dict(aligned, complete=True), rec)}
        assert sample["complete"] is True, observed
        return observed
    R.case("RV12_unrelated_apostrophe_process_does_not_null_the_sample", "sampler", "BLOCKING", rv12)

    def rv13():
        f, work, plan = sampler_fixture("RV13_persistent_apostrophe_row")
        clock = accelerate(f, lambda n: [clean_row, apostrophe_row] if n >= 2 else [clean_row], max_sleeps=400)
        try:
            M.sampler(f.ctx, plan, str(work), poll_s=1)
            decided = True
        except NoDecision:
            decided = False
        observed = {"sampler_decided_within_400_polls": decided, "polls": clock["polls"],
                    "solo_written": Path(f.outdir + ".solo.json").exists(),
                    "consequence": "close-attempt refuses SAMPLER_STILL_ALIVE while such a process lives"}
        assert decided, observed
        return observed
    R.case("RV13_sampler_ends_after_receipt_despite_unparseable_row", "sampler", "BLOCKING", rv13)

    def rv14():
        f, work, plan = sampler_fixture("RV14_first_sample_apostrophe")
        accelerate(f, lambda n: [clean_row, apostrophe_row])
        result = M.sampler(f.ctx, plan, str(work), poll_s=1)
        solo = expect_refusal(M, lambda: M.enforce_solo(f.ctx, True, rows=[clean_row, apostrophe_row]))
        observed = {"sampler": result.get("status", result), "launch_consequence": "SAMPLER_FIRST_SAMPLE_FAILED",
                    "enforce_solo_no_listed_process": solo}
        assert result.get("status") is None and isinstance(solo, dict), observed
        return observed
    R.case("RV14_first_sample_and_solo_check_tolerate_unparseable_row", "sampler", "BLOCKING", rv14)

    def rv15():
        f = T.receipt_fixture(suite, "RV15_counter_matrix")
        d = f.root / "counter"
        d.mkdir()
        drv = suite.raw_write(d / "synthetic_listed_driver.py", b"# synthetic listed driver\n")
        tool = suite.raw_write(d / "synthetic_listed_tool.py", b"# synthetic listed tool\n")
        (d / "space dir").mkdir()
        copy = suite.raw_write(d / "space dir" / "tool copy.py", b"# synthetic listed tool\n")
        link = d / "driver_link.py"
        os.symlink(drv["path"], link)
        declared = [{"tool": "drv", "path": drv["path"], "sha256": drv["sha256"], "driver_only": True},
                    {"tool": "tool", "path": tool["path"], "sha256": tool["sha256"], "driver_only": False}]
        C = M.ProcessCounter(declared=declared, synthetic=True)
        row = lambda pid, cmd, ppid=1: {"pid": pid, "ppid": ppid, "pgid": pid, "command": cmd}
        probes = {
            "driver_run": (row(10, "%s -I -B %s run --spec /s --outdir /o" % (M.PY, drv["path"])), 1),
            "driver__stage": (row(11, "%s -I -B %s _stage /r" % (M.PY, drv["path"])), 1),
            "driver_dry_run": (row(12, "%s -I -B %s dry-run --spec /s" % (M.PY, drv["path"])), 0),
            "monitor_names_driver": (row(13, "%s -I -B /m.py --driver %s --driver-sha256 x" % (M.PY, drv["path"])), 0),
            "symlink_to_driver_run": (row(14, "%s -I -B %s run --spec /s --outdir /o" % (M.PY, link)), 1),
            "listed_tool": (row(15, "%s -I -B %s" % (M.PY, tool["path"])), 1),
            "grep_names_listed_tool_INFO": (row(16, "/usr/bin/grep x %s" % tool["path"]), 1),
            "own_tree_child": (row(18, "%s -I -B %s run --spec /s --outdir /o" % (M.PY, drv["path"]), ppid=17), 0),
        }
        got = {}
        for label, (r, want) in probes.items():
            own = 17 if label == "own_tree_child" else None
            got[label] = (len(C.count([r], own_root=own)), want)
        notes = {"byte_copy_under_path_with_space": len(C.count([row(19, "%s -I -B %s" % (M.PY, copy["path"]))])),
                 "relative_path_from_tool_cwd": len(C.count([row(20, "%s -I -B synthetic_listed_tool.py" % M.PY)]))}
        bad = {k: v for k, v in got.items() if v[0] != v[1]}
        observed = {"results": got, "lower_bound_notes": notes, "mismatches": bad}
        assert not bad, observed
        return observed
    R.case("RV15_solo_mode_process_detection_matrix", "solo", "BLOCKING", rv15)

    def rv16():
        variants = {}
        for label, rows in (
                ("near_miss_A10_outdir", lambda f: [{"pid": 900002, "ppid": 1, "pgid": 900002, "command":
                    "%s -I -B %s _sampler --outdir %s0" % (M.PY, TOOL, f.outdir)}]),
                ("other_tool_copy", lambda f: [{"pid": 900002, "ppid": 1, "pgid": 900002, "command":
                    "%s -I -B %s.copy _sampler --outdir %s" % (M.PY, TOOL, f.outdir)}]),
                ("sampler_word_missing", lambda f: [{"pid": 900002, "ppid": 1, "pgid": 900002, "command":
                    "%s -I -B %s status --outdir %s" % (M.PY, TOOL, f.outdir)}]),
                ("CONTROL_true_sampler", lambda f: [{"pid": 900002, "ppid": 1, "pgid": 900002, "command":
                    "%s -I -B %s _sampler --outdir %s --poll-s 5" % (M.PY, TOOL, f.outdir)}])):
            f = T.receipt_fixture(suite, "RV16_" + label)
            f.ctx.system.rows = rows(f)
            r = expect_refusal(M, lambda f=f: M.close_attempt(f.ctx, f.name, 1))
            variants[label] = r if isinstance(r, str) else r["result"]["status_class"]
        observed = {"close_result": variants}
        assert variants == {"near_miss_A10_outdir": "FINISHED", "other_tool_copy": "FINISHED",
                            "sampler_word_missing": "FINISHED", "CONTROL_true_sampler": "SAMPLER_STILL_ALIVE"}, observed
        return observed
    R.case("RV16_reused_pid_sampler_qualification", "reused_pid", "BLOCKING", rv16)

    def rv17():
        f = T.receipt_fixture(suite, "RV17_p112_attempt_kit_volume_absent")
        f.ctx.system.fixture["mount_points"] = [f.ctx.cfg["run_volume"]]
        own = M.close_attempt(f.ctx, f.name, 1)["status_class"]
        g = T.receipt_fixture(suite, "RV17b_kit_attempt_run_volume_absent", origin="KIT", name="S0_J0_SERIAL")
        g.ctx.system.fixture["mount_points"] = [str(Path(g.ctx.cfg["s0"]["run_root"]).parent)]
        kit = M.close_attempt(g.ctx, g.name, 1)["status_class"]
        link = out / "rv17_volume_link"
        os.symlink(f.ctx.cfg["run_volume"], link)
        sysm = M.SyntheticSystem({"mount_points": [str(link)], "free_bytes": 1, "host_ram_bytes": M.RAM})
        cfg = {"run_volume": str(link), "s0": {"run_root": str(link) + "/NGC_X"}}
        sym = expect_refusal(M, lambda: M.mount_first(cfg, "P112", sysm))
        prod = M.System().mounted(str(link))
        h = T.receipt_fixture(suite, "RV17c_residual_kit_volume_absent", origin="KIT", name="S0_J0_SERIAL")
        h.ctx.v006_text += "RESIDUAL_RETRY S0_J0_SERIAL 1\n"
        h.ctx.system.fixture["mount_points"] = [h.ctx.cfg["run_volume"]]
        residual = M.status(h.ctx)["calls"][0]["status"]
        observed = {"p112_attempt_with_kit_volume_absent": own, "kit_attempt_with_run_volume_absent": kit,
                    "symlinked_volume": sym, "production_mounted_on_symlink": prod,
                    "residual_line_with_kit_volume_absent": residual}
        assert (own == "FINISHED" and kit == "FINISHED" and sym == "RUN_VOLUME_NOT_MOUNTED" and prod is False
                and residual == "RUN_VOLUME_NOT_MOUNTED"), observed
        return observed
    R.case("RV17_mount_check_uses_the_attempts_own_volume", "volume", "BLOCKING", rv17)

    # ------------------------------------------------------------------ theta one-ulp
    def rv18():
        B = M.load_verified(M.REAL["builder"], "_rv_builder_theta")
        up = lambda x: math.nextafter(x, math.inf)
        engine = {"Eref_base_J": 2.5, "ell_F_m": 7.0, "gamma_over_Eref": 0.125, "common_scale_s": 1.5,
                  "entropy_K_factor": 3.0}

        def build(**ch):
            th = dict(engine)
            member = {"member_id": "M000", "log_index": 1, "role": "primary_anchor",
                      "theta_engine": dict(th), "theta_ngc": dict(th, ngc3198_distance_Mpc=13.8, ngc3198_inclination_deg=72.0)}
            fd = {"log_index": 1, "role": "primary_anchor", "theta_hex": {k: v.hex() for k, v in th.items()},
                  "key": M.theta_key(th)}
            export = {"admitted_points": [{"log_index": 1, "theta_natural": dict(th)}]}
            spec = {"physical": {"Eref_J": 2.5, "ell_F_m": 7.0, "gamma": 0.125 * 2.5, "common_scale_s": 1.5,
                                 "entropy_K_factor": 3.0, "distance_Mpc": 13.8, "inclination_deg": 72.0}}
            seed = {"physical": {"distance_Mpc": 13.8, "inclination_deg": 72.0}}
            cfg = {"log_index": 1, "role": "primary_anchor", "order": 0, "member_id": "M000"}
            objs = {"member": member, "fd": fd, "export": export, "spec": spec, "seed": seed, "cfg": cfg}
            for k, fn in ch.items():
                fn(objs)
            return objs

        def run(objs):
            return expect_refusal(M, lambda: M.check_member_theta(
                objs["member"], objs["fd"], {"log_index": 1}, objs["export"], objs["spec"], objs["seed"],
                objs["cfg"], 0, B))
        res = {"honest": run(build())}
        res["honest"] = "PASS" if isinstance(res["honest"], dict) else res["honest"]

        def negative_zero(o):
            for th in (o["export"]["admitted_points"][0]["theta_natural"],):
                th["ell_F_m"] = 0.0
            o["member"]["theta_engine"]["ell_F_m"] = -0.0
        variants = {
            "gamma_product_one_ulp": lambda o: o["spec"]["physical"].__setitem__("gamma", up(0.125 * 2.5)),
            "gamma_over_Eref_one_ulp_PLAN_only": lambda o: o["member"]["theta_engine"].__setitem__("gamma_over_Eref", up(0.125)),
            "export_one_ulp": lambda o: o["export"]["admitted_points"][0]["theta_natural"].__setitem__("ell_F_m", up(7.0)),
            "fdplan_hex_one_ulp": lambda o: o["fd"]["theta_hex"].__setitem__("common_scale_s", up(1.5).hex()),
            "PLAN_nuisance_one_ulp": lambda o: o["member"]["theta_ngc"].__setitem__("ngc3198_distance_Mpc", up(13.8)),
            "PLAN_nuisance_both_spellings": lambda o: o["member"]["theta_ngc"].__setitem__("distance_Mpc", 13.8),
            "PLAN_nuisance_int": lambda o: o["member"]["theta_ngc"].__setitem__("ngc3198_inclination_deg", 72),
            "spec_inclination_one_ulp_down": lambda o: o["spec"]["physical"].__setitem__("inclination_deg", math.nextafter(72.0, 0)),
            "seed_distance_one_ulp": lambda o: o["seed"]["physical"].__setitem__("distance_Mpc", up(13.8)),
            "negative_zero_vs_zero": negative_zero,
            "extra_coordinate": lambda o: o["member"]["theta_engine"].__setitem__("extra", 1.0),
            "fdplan_key_from_other_theta": lambda o: o["fd"].__setitem__("key", M.theta_key(dict(engine, ell_F_m=up(7.0)))),
            "fdplan_hex_uppercase_INFO": lambda o: o["fd"]["theta_hex"].__setitem__("ell_F_m", (7.0).hex().upper()),
        }
        for label, fn in variants.items():
            res[label] = run(build(v=fn))
            if isinstance(res[label], dict):
                res[label] = "ACCEPTED"
        accepted = [k for k, v in res.items() if k != "honest" and v == "ACCEPTED"]
        ff = {"role": "F0", "theta_hex": {k: v.hex() for k, v in engine.items()}, "key": M.theta_key(engine)}
        spec = build()["spec"]
        res["F_point_honest"] = "PASS" if isinstance(expect_refusal(M, lambda: M.check_f_theta(
            ff, {"point_key": ff["key"]}, spec, build()["seed"], "F0")), dict) else "REFUSED"
        res["F_point_key_one_ulp_theta"] = expect_refusal(M, lambda: M.check_f_theta(
            ff, {"point_key": M.theta_key(dict(engine, ell_F_m=up(7.0)))}, spec, build()["seed"], "F0"))
        observed = {"results": res, "accepted_variants": accepted}
        assert res["honest"] == "PASS" and not accepted and res["F_point_honest"] == "PASS" and \
            res["F_point_key_one_ulp_theta"] == "F_POINT_KEY", observed
        return observed
    R.case("RV18_theta_one_ulp_and_signed_zero_matrix", "theta", "BLOCKING", rv18)

    # ------------------------------------------------------------------ MISLAUNCH / kill-target
    def rv19():
        f = T.receipt_fixture(suite, "RV19_kill_target_mapping")
        target = start(["/bin/sleep", "60"])
        stand_in = suite.raw_write(f.root / "kit_stand_in_uncaught_exception.py",
                                   b"raise RuntimeError('simulated: kit ps_field TimeoutExpired is uncaught')\n")
        f.ctx.pins = dict(f.ctx.pins, kit=stand_in)
        lj = {"schema": M.MONITOR_SCHEMA + "_LAUNCH", "child_pid": target.pid, "command": ["/bin/sleep", "61"],
              "pins": {"spec": f.call["spec"]}}
        lj_pin = suite.raw_write(f.root / "rv19_launch.json", M.encoded(lj))
        plan = {"name": f.name, "launch_json": lj_pin["path"], "spec": f.call["spec"], "outdir": f.outdir}
        crash = M.kit_kill_target(f.ctx, plan, None)
        f.ctx.pins = dict(f.ctx.pins, kit=M.REAL["kit"])
        real = M.kit_kill_target(f.ctx, plan, None)
        alive = target.poll() is None
        observed = {"kit_uncaught_exception_exit_1_maps_to": crash["result"],
                    "real_kit_pid_reuse_maps_to": real["result"], "target_alive_after_both": alive,
                    "site": "kit_kill_target L1905: returncode 1 -> ALREADY_ENDED without reading the kit's alive flag"}
        assert crash["result"] != "ALREADY_ENDED" and real["result"] == "NOT_KILLED_TARGET_REFUSED" and alive, observed
        return observed
    R.case("RV19_kill_target_exit_1_is_not_proof_the_target_ended", "MISLAUNCH", "FIX", rv19)

    def rv20():
        f = T.receipt_fixture(suite, "RV20_mon_pid_rules")
        calls = []
        orig_kt, orig_sq = M.kit_kill_target, M.stop_qualified
        M.kit_kill_target = lambda ctx, plan, monitor_pid=None: calls.append(("kill_target", monitor_pid)) or {
            "result": "KILLED_TERM", "pgid": 1, "mon_pid_supplied": monitor_pid}
        M.stop_qualified = lambda system, pid, predicate, group=False: calls.append(("stop_monitor", pid)) or "KILLED_TERM"
        try:
            mon = {"pid": 900001, "ppid": 1, "pgid": 900001, "command": "%s -I -B %s --receipt %s.receipt.json" % (
                M.PY, f.ctx.pins["monitor"]["path"], f.outdir)}
            plan = {"name": f.name, "launch_json": f.outdir + ".receipt.json.launch.json", "spec": f.call["spec"],
                    "outdir": f.outdir, "receipt": f.outdir + ".receipt.json"}
            f.ctx.system.rows = [mon]
            M.stop_launch_failure(f.ctx, plan, 900001, True)
            parsed_mismatch = list(calls)
            calls.clear()
            M.stop_launch_failure(f.ctx, plan, 900001, False)
            bound_unparsed = list(calls)
            calls.clear()
            f.ctx.system.rows = [dict(mon, command="/bin/sleep 60")]
            M.stop_launch_failure(f.ctx, plan, 900001, True)
            reused = list(calls)
        finally:
            M.kit_kill_target, M.stop_qualified = orig_kt, orig_sq
        observed = {"parsed_mismatch_live_monitor": parsed_mismatch, "unparsed_at_bound_live_monitor": bound_unparsed,
                    "reused_monitor_pid": reused}
        assert (parsed_mismatch == [("kill_target", 900001)] and
                bound_unparsed == [("stop_monitor", 900001), ("kill_target", None)] and
                reused == [("kill_target", None)]), observed
        return observed
    R.case("RV20_kill_target_mon_pid_only_while_monitor_qualified", "MISLAUNCH", "BLOCKING", rv20)

    # ------------------------------------------------------------------ interrupted launch / resume (live, synthetic)
    def live_context(label):
        f = T.full_launch_fixture(suite, label)
        M.synthetic_fence(f.overrides, f.config_doc)
        system = M.SyntheticSystem(M.read_pin(f.synthetic)["system"])
        ctx = M.Context(f.config, system=system, synthetic_pins=f.overrides)
        ctx.synthetic_pin = f.synthetic
        watch = start([M.PY, "-I", "-B", f.watch["path"]])
        time.sleep(0.2)
        return f, ctx, watch

    def child_launch(ctx, name, die_on):
        pid = os.fork()
        if pid == 0:
            try:
                if die_on == "monitor_pid":
                    orig = ctx.write

                    def w(path, obj):
                        if str(path).endswith("/monitor_pid.json"):
                            os._exit(9)
                        return orig(path, obj)
                    ctx.write = w
                else:
                    orig_nl = M.new_log

                    def nl(path):
                        if Path(path).name == "monitor.stdout.txt":
                            os._exit(9)
                        return orig_nl(path)
                    M.new_log = nl
                with open(os.devnull, "w") as dn, contextlib.redirect_stdout(dn), contextlib.redirect_stderr(dn):
                    M.launch(ctx, name, 1)
                os._exit(0)
            except BaseException:
                os._exit(3)
        _, status = os.waitpid(pid, 0)
        return os.waitstatus_to_exitcode(status)

    def sampler_pid_of(work):
        p = work / "sampler_first_sample.json"
        return json.loads(p.read_bytes())["sampler_pid"] if p.is_file() else None

    def rv21():
        f, ctx, watch = live_context("RV21_killed_between_popen_and_monitor_pid")
        try:
            name = f.name
            exit_code = child_launch(ctx, name, "monitor_pid")
            outdir = M.planned_outdir(ctx, name, 1, "P112")
            works = sorted((Path(ctx.cfg["p112_launch_root"]) / "work").glob(name + "_A1_*"))
            work = works[-1]
            wait_until(lambda: Path(outdir + ".receipt.json").is_file(), 40)
            sp = sampler_pid_of(work)
            wait_until(lambda: sp is None or not pid_alive(sp), 40)
            state = {"child_exit": exit_code, "launch_json": Path(outdir + ".receipt.json.launch.json").is_file(),
                     "receipt": Path(outdir + ".receipt.json").is_file(),
                     "invocation_json": (work / "invocation.json").is_file(),
                     "monitor_pid_json": (work / "monitor_pid.json").is_file(),
                     "launch_records": [r["path"] for r in ctx.record_paths(name)]}
            resume = expect_refusal(M, lambda: M.launch_resume(ctx, name, 1))
            status = [c["status"] for c in M.status(ctx)["calls"] if c["name"] == name][0]
            relaunch = expect_refusal(M, lambda: M.launch(ctx, name))
            close = expect_refusal(M, lambda: M.close_attempt(ctx, name, 1))
            ctx.v006_text += "RESIDUAL_RETRY %s 1\n" % name
            residual = [c["status"] for c in M.status(ctx)["calls"] if c["name"] == name][0]
            observed = {"state": state, "resume": resume if isinstance(resume, str) else "LAUNCH_RECORD_WRITTEN",
                        "status": status, "launch": relaunch, "close_attempt": close,
                        "status_with_RESIDUAL_RETRY_line": residual,
                        "rule": "ROUND5 item 1(b): resume is admitted when launch.json exists, no record exists and "
                                "the invocation is gone; the code also requires monitor_pid.json (L2022)"}
            assert isinstance(resume, dict), observed
            return observed
        finally:
            watch.terminate()
    R.case("RV21_interrupted_after_monitor_popen_keeps_a_legal_next_step", "interrupted_launch", "FIX", rv21)

    def rv22():
        f, ctx, watch = live_context("RV22_killed_before_monitor_start")
        try:
            name = f.name
            exit_code = child_launch(ctx, name, "monitor_start")
            work_root = Path(ctx.cfg["p112_launch_root"]) / "work"
            first = sorted(work_root.glob(name + "_A1_*"))[-1]
            sp = sampler_pid_of(first)
            ended = wait_until(lambda: sp is None or not pid_alive(sp), 40)
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                rec = M.read_pin(M.launch(ctx, name, 1))
            outdir = M.planned_outdir(ctx, name, 1, "P112")
            wait_until(lambda: Path(outdir + ".solo.json").is_file(), 40)
            works = sorted(work_root.glob(name + "_A1_*"))
            sp2 = sampler_pid_of(works[-1])
            wait_until(lambda: sp2 is None or not pid_alive(sp2), 40)
            closed = M.close_attempt(ctx, name, 1)
            observed = {"child_exit": exit_code, "old_sampler_ended_by_itself": ended,
                        "relaunch_outcome": rec["outcome"], "attempt": rec["attempt"],
                        "reported_same_spec": "ALREADY_REGISTERED_SAME_SPEC" in err.getvalue(),
                        "work_dirs_for_k1": len(works), "close": closed["status_class"]}
            assert (exit_code == 9 and ended and rec["outcome"] == "LAUNCH" and rec["attempt"] == 1 and
                    observed["reported_same_spec"] and len(works) == 2 and closed["status_class"] == "FINISHED"), observed
            return observed
        finally:
            watch.terminate()
    R.case("RV22_interrupted_before_monitor_start_relaunches_same_k", "interrupted_launch", "BLOCKING", rv22)

    def rv23():
        f = T.resume_fixture(suite, "RV23_resume_picks_live_invocation")
        older = f.work.parent / (f.name + "_A1_OLDER_UNRECORDED_REFUSAL_900005")
        older.mkdir()
        plan = dict(f.plan, work=str(older), invocation_utc="2026-01-01T00:00:00.000000Z")
        plan_pin = suite.raw_write(older / "plan.json", M.encoded(plan))
        suite.raw_write(older / "invocation.json", M.encoded({
            "invocation_pid": 900005, "invocation_command": "gone", "sampler_pid": 900006,
            "planned_monitor_argv": plan["monitor_argv"], "plan": plan_pin, "date_u": M.date_u()}))
        suite.raw_write(older / "monitor_pid.json", M.encoded({"monitor_pid": 900007, "plan": plan_pin,
                                                                "date_u": M.date_u()}))
        rec = M.read_pin(M.launch_resume(f.ctx, f.name, 1))
        observed = {"outcome": rec["outcome"], "record_plan_is_interrupted_invocation": rec["plan"] == f.plan_pin,
                    "monitor_pid": rec["monitor_pid"]}
        assert rec["outcome"] == "LAUNCH" and rec["plan"] == f.plan_pin and rec["monitor_pid"] == 900001, observed
        return observed
    R.case("RV23_resume_binds_the_invocation_that_started_the_monitor", "interrupted_launch", "BLOCKING", rv23)

    # ------------------------------------------------------------------ lens 4: launch without the TOOL_PIN gate
    def rv24():
        src = Path(TOOL).read_text()
        has_constant = V006 in src
        fake = suite.raw_write(out / "rv24_not_V006.md", ("## A1: anything\n" + PIN_LINE + "\n").encode())
        raw = M.read_v006(fake["path"])
        gate = M.tool_gate(raw.decode(), own_pin)
        observed = {"tool_carries_V006_path_constant": has_constant, "gate_passes_on_arbitrary_file": gate == own_pin,
                    "site": "Context.__init__ L755: config['v006'] is any absolute realpath; the kit pins REAL['v006']",
                    "scope": "production config is root-written and sha-pinned per call; synthetic mode is fenced"}
        assert has_constant, observed
        return observed
    R.case("RV24_gate_reads_the_program_V006_not_any_configured_file", "TOOL_PIN_bypass", "FIX", rv24)

    def rv25():
        found = []
        f = T.receipt_fixture(suite, "RV25_gate_coverage")
        f.ctx.v006_text = "## A999: no pin\n"
        for label, fn in (("launch", lambda: M.launch(f.ctx, f.name)),
                          ("resume", lambda: M.launch_resume(f.ctx, f.name, 1)),
                          ("close", lambda: M.close_attempt(f.ctx, f.name, 1)),
                          ("assemble", lambda: M.assemble_registry(f.ctx)),
                          ("verify", lambda: M.assemble_registry(f.ctx, verify=True)),
                          ("outside", lambda: M.stop_outside_set(f.ctx, "S0_J0_SERIAL")),
                          ("refused", lambda: M.record_monitor_refused(f.ctx, {}, str(f.root))),
                          ("sampler", lambda: M.sampler(f.ctx, {}, str(f.root))),
                          ("cutoff", lambda: M.write_cutoff(f.ctx, [{"time_utc": "2026-10-20T00:00:00Z"}]))):
            found.append((label, expect_refusal(M, fn)))
        import ast
        popen_sites = [n.lineno for n in ast.walk(ast.parse(Path(TOOL).read_text()))
                       if isinstance(n, ast.Call) and getattr(n.func, "attr", None) == "Popen"]
        observed = {"no_pin_results": dict(found), "Popen_lines": popen_sites,
                    "Popen_reachability": "L1998 twin watch and L2076/L2098 sampler/monitor: only after ctx.gate() "
                                          "(launch L2045, resume L2008); L2102 caffeinate follows the monitor"}
        assert all(code == "TOOL_PIN_MISSING" for _, code in found), observed
        return observed
    R.case("RV25_every_writing_or_launching_path_is_gated", "TOOL_PIN_bypass", "BLOCKING", rv25)

    for p in live:
        if p.poll() is None:
            p.terminate()
            try:
                p.wait(timeout=5)
            except subprocess.TimeoutExpired:
                p.kill()
    finished = subprocess.check_output(["/bin/date", "-u"], env=dict(os.environ, LC_ALL="C"), text=True).strip()
    record = {"schema": "P112_ROOTVERIFY_ADVERSARIAL_C2V001", "started_date_u": started, "date_u": finished,
              "tool": {"path": TOOL, "sha256": TOOL_SHA}, "fixtures_from": {"path": TESTS, "sha256": TESTS_SHA},
              "harness": {"path": str(Path(__file__).resolve()), "sha256": sha(Path(__file__).read_bytes())},
              "cases": R.rows, "p112_open_events": len(audit.opens), "forbidden_opens": audit.forbidden,
              "summary": {s: [r["name"] for r in R.rows if r["status"] == s] for s in ("PASS", "FAIL", "ERROR")}}
    raw = (json.dumps(record, sort_keys=True, indent=1, default=repr) + "\n").encode()
    with (out / "ROOTVERIFY_ADVERSARIAL_RESULT.json").open("xb") as fh:
        fh.write(raw)
        fh.flush()
        os.fsync(fh.fileno())
        os.fchmod(fh.fileno(), 0o444)
    print(json.dumps({"cases": len(R.rows), "summary": record["summary"], "result_sha256": sha(raw)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

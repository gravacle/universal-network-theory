"""Exclusive synthetic test runner for the draft P112 implementation."""
import argparse
import ast
import hashlib
import json
import os
import subprocess
import traceback
import types
from pathlib import Path


def hash_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def exclusive(path, raw):
    with Path(path).open("xb") as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
        os.fchmod(f.fileno(), 0o444)
    return {"path": str(path), "sha256": hash_bytes(raw)}


class Suite:
    def __init__(self, tool, root, tool_sha):
        self.tool_path, self.root = Path(tool), Path(root)
        raw = self.tool_path.read_bytes()
        if hash_bytes(raw) != tool_sha:
            raise ValueError("tool pin mismatch")
        self.tool_sha = tool_sha
        self.module = types.ModuleType("_p112_synthetic_review")
        self.module.__file__ = str(self.tool_path)
        exec(compile(raw, str(self.tool_path), "exec"), self.module.__dict__)
        self.root.mkdir()
        self.rows, self.interfaces = [], {}
        self.refusals, self.current_case = {}, "fixture_setup"
        old_init = self.module.Refusal.__init__
        def tracked(error, code, detail=None):
            self.refusals.setdefault(code, set()).add(self.current_case)
            old_init(error, code, detail)
        self.module.Refusal.__init__ = tracked

    def eq(self, left, right):
        if left != right:
            raise AssertionError((left, right))

    def refuses(self, code, action):
        try:
            action()
        except self.module.Refusal as e:
            self.eq(e.code, code)
            return
        raise AssertionError("expected " + code)

    def any_refusal(self, action):
        try:
            action()
        except self.module.Refusal:
            return
        raise AssertionError("expected a refusal")

    def raw_write(self, path, raw):
        return exclusive(path, raw)

    def bytes_fixture(self, name, raw):
        path = self.root / name
        return exclusive(path, raw)

    def fixture(self, name, obj):
        return self.bytes_fixture(name, self.module.encoded(obj))

    def case(self, name, action):
        if any(r["name"] == name for r in self.rows):
            raise AssertionError("duplicate test " + name)
        self.current_case = name
        try:
            action()
            self.rows.append({"name": name, "status": "PASS"})
        except Exception as e:
            self.rows.append({"name": name, "status": "FAIL", "detail": repr(e),
                              "trace": traceback.format_exc(limit=5)})
        finally:
            self.current_case = "fixture_setup"



"""Synthetic P112 test component: deterministic arithmetic and custody contracts."""


def core_cases(suite):
    M = suite.module
    case, fail = suite.case, suite.refuses
    case("S01_literal_status_map", lambda: (
        suite.eq(len(M.STATUS_CLASSES), 54),
        suite.eq(len(M.canonical(M.STATUS_CLASSES)), 2052),
        suite.eq(M.sha(M.canonical(M.STATUS_CLASSES)), "c36c37886aa67db763160681be99904c3ae9f22ebb51f3e841adadfa0e1cdb54")))
    bind = dict(name="P1_M0001", attempt=2, outdir="/synthetic/NGC_RUN_A2",
                receipt="/synthetic/NGC_RUN_A2.receipt.json",
                launch_pin={"path": "/synthetic/NGC_RUN_A2.receipt.json.launch.json", "sha256": "a" * 64}, child_pid=123)
    drivers = ("COMPLETED", "COMPLETED_INVALID", "FAILED", "FAILED_AT_STAGE", "ROUTE_A_NO_FIXED_POINT",
               "REFUSED", "BLOCKED", "UNREADABLE_FINISH", "RESULT_HASH_MISMATCH", None)
    for cap, cls in (("WALL_CAP", "CAP"), ("RSS_CAP", "CAP"), ("OUTPUT_CAP", "OUTPUT_CAP")):
        for driver in drivers:
            case("S01_%s_%s" % (cap, driver), lambda cap=cap, cls=cls, driver=driver:
                 suite.eq(M.raw_status({"status": "STOPPED_" + cap, "driver_status": driver, "exit_code": -15}, **bind),
                          ("STOPPED_" + cap + "|" + (driver or "NONE"), cls)))
    for driver in drivers:
        if driver in ("COMPLETED", "COMPLETED_INVALID"):
            expected = "FINISHED"
        else:
            expected = "INFRA"
        case("S01_FINISHED_%s" % driver, lambda driver=driver, expected=expected:
             suite.eq(M.raw_status({"status": "FINISHED", "driver_status": driver, "exit_code": 0}, **bind)[1], expected))
    for driver in drivers:
        expected = "FAILED" if driver in ("FAILED", "FAILED_AT_STAGE", "ROUTE_A_NO_FIXED_POINT", None) else "INFRA"
        case("S01_CHILD_FAILED_%s" % driver, lambda driver=driver, expected=expected:
             suite.eq(M.raw_status({"status": "CHILD_FAILED", "driver_status": driver, "exit_code": 1}, **bind)[1], expected))
    case("S01_signal", lambda: suite.eq(M.raw_status(
        {"status": "CHILD_FAILED", "driver_status": None, "exit_code": -9}, **bind), ("CHILD_FAILED|NONE|SIGNAL", "INFRA")))
    case("S02_unmapped", lambda: fail("RECEIPT_STATUS_UNMAPPED", lambda: M.raw_status(
        {"status": "FINISHED", "driver_status": "UNKNOWN"}, **bind)))
    mis = {k: bind[k] for k in ("name", "attempt", "outdir", "receipt")}
    mis["launch_json"] = dict(bind["launch_pin"], child_pid=123)
    cap_rec = {"status": "STOPPED_WALL_CAP", "driver_status": "FAILED", "exit_code": -15}
    case("S03_mislaunch_precedence", lambda: suite.eq(M.raw_status(cap_rec, **bind, mislaunch=mis), ("MISLAUNCH", "INFRA")))
    tb = dict(bind, name=M.TWIN)
    stop = {"reason": "ITERATION_0001_COMPLETED_AND_SIDECAR", "outdir": bind["outdir"], "launch_json": bind["launch_pin"]}
    case("S03_twin_kill_signal", lambda: suite.eq(M.raw_status(
        {"status": "CHILD_FAILED", "driver_status": None, "exit_code": -9}, **tb, stop=stop),
        ("TWIN_PLANNED_STOP", "PLANNED_STOP")))
    case("S03_twin_cap_no_kill", lambda: suite.eq(M.raw_status(cap_rec, **tb), ("TWIN_PLANNED_STOP", "PLANNED_STOP")))
    for key, value in (("name", "P1_M0002"), ("attempt", 1), ("outdir", "/another"), ("receipt", "/another.receipt")):
        bad = dict(mis, **{key: value})
        case("S04_mislaunch_" + key, lambda bad=bad: fail("MISLAUNCH_NOT_BOUND", lambda: M.raw_status(cap_rec, **bind, mislaunch=bad)))
    for key, value in (("sha256", "b" * 64), ("child_pid", 124)):
        bad = dict(mis, launch_json=dict(mis["launch_json"], **{key: value}))
        case("S04_mislaunch_launch_" + key, lambda bad=bad: fail(
            "MISLAUNCH_NOT_BOUND", lambda: M.raw_status(cap_rec, **bind, mislaunch=bad)))
    for key, value in (("reason", "OTHER"), ("outdir", "/other"), ("launch_json", {"sha256": "b" * 64})):
        bad = dict(stop, **{key: value})
        case("S04_stop_" + key, lambda bad=bad: fail("TWIN_STOP_NOT_BOUND", lambda: M.raw_status(cap_rec, **tb, stop=bad)))

    monitor = {"utc_start": "2026-10-20T10:00:01Z", "utc_end": "2026-10-20T10:00:10Z"}
    sample = {"complete": True, "poll_s": 5, "largest_gap_s": 5.0, "n_samples": 4,
              "first_utc": "2026-10-20T10:00:00.500000Z", "last_utc": "2026-10-20T10:00:11.100000Z",
              "max_other_ngc_processes": 0}
    case("P09_whole_second_coverage", lambda: suite.eq(M.sample_value(sample, monitor), 0))
    case("P03_C14_absent_sample", lambda: suite.eq(M.sample_value(None, monitor), None))
    for label, changes in (
            ("P02_gap", {"largest_gap_s": 10.0001}), ("P06_incomplete", {"complete": False}),
            ("P06_first_after", {"first_utc": "2026-10-20T10:00:02.000000Z"}),
            ("P06_last_before", {"last_utc": "2026-10-20T10:00:09.000000Z"}),
            ("P08_first_same_second", {"first_utc": "2026-10-20T10:00:01.000001Z"}),
            ("P08_last_same_second", {"last_utc": "2026-10-20T10:00:10.999999Z"})):
        bad = dict(sample, **changes)
        case(label, lambda bad=bad: suite.eq(M.sample_value(bad, monitor), None))
    case("P02_gap_exactly_twice_passes", lambda: suite.eq(M.sample_value(dict(sample, largest_gap_s=10), monitor), 0))

    own = {"path": str(suite.tool_path), "sha256": suite.tool_sha}
    line = "TOOL_PIN P112_LAUNCHER_CX2V002 " + own["sha256"] + " " + own["path"]
    good = "## A999: synthetic\n" + line + "\n"
    case("L01_missing", lambda: fail("TOOL_PIN_MISSING", lambda: M.tool_gate("## A999: none\n", own)))
    case("L02_sha", lambda: fail("TOOL_PIN_MISMATCH", lambda: M.tool_gate(good.replace(own["sha256"], "0" * 64), own)))
    case("L02_path", lambda: fail("TOOL_PIN_MISMATCH", lambda: M.tool_gate(good.replace(own["path"], "/different"), own)))
    case("L03_duplicate", lambda: fail("TOOL_PIN_DUPLICATE", lambda: M.tool_gate(good + line + "\n", own)))
    case("L05_successor_ignored", lambda: suite.eq(M.tool_gate(good + line.replace("CX2V002", "CX2V003") + "\n", own), own))
    case("L07_midline_ignored", lambda: suite.eq(M.tool_gate(
        "## A998: test\nText mentions TOOL_PIN and RESIDUAL_RETRY inside prose.\n" + good, own), own))
    for label, text in (("uppercase", line.replace(own["sha256"], own["sha256"].upper())),
                        ("relative", line.replace(own["path"], "relative.py")), ("no_entry", line),
                        ("trailing", good.rstrip("\n") + " ")):
        case("L07_" + label, lambda text=text: fail("TOOL_PIN_MISMATCH", lambda: M.tool_gate(text, own)))
    case("N14_residual_malformed", lambda: fail("RESIDUAL_RETRY_MALFORMED", lambda: M.residual_lines(
        "## A999: root\nRESIDUAL_RETRY P1_M0001 01\n")))
    case("N14_residual_dedup", lambda: suite.eq(M.residual_lines(
        "## A999: root\nRESIDUAL_RETRY P1_M0001 1\nRESIDUAL_RETRY P1_M0001 1\n"), {("P1_M0001", 1)}))
    case("L07_residual_midline", lambda: suite.eq(M.residual_lines("## A999: root\nText RESIDUAL_RETRY P1_M0001 1\n"), set()))
    for label, path in (("V01_component", "/synthetic/NGC3198/a"), ("V02_runs_ext", "/synthetic/runs_ext/a"),
                        ("V01_case", "/synthetic/nGc3198_private/a")):
        case(label, lambda path=path: suite.any_refusal(lambda: M.path_rules(path)))

    def receipt(raw="CHILD_FAILED|FAILED", solo=False, count=1, wall=610324, out=146028888064, spec="a" * 64):
        return {"raw_status": raw, "status_class": M.STATUS_CLASSES[raw], "spec_sha256": spec,
                "rss_cap_bytes": M.RAM, "wall_cap_s": wall, "output_cap_bytes": out, "host_ram_bytes": M.RAM,
                "other_ngc_processes_max": count, "solo_mode": solo}
    def records(n, origin="P112"):
        return [{"attempt": k, "origin": origin, "outcome": "LAUNCH"} for k in range(1, n + 1)]
    first = receipt()
    rerun = receipt(solo=True, count=0, wall=1220648)
    case("K01_serial_rule_c_caps", lambda: suite.eq(M.next_attempt("P1_M0001", records(1), [first], set())["caps"],
        {"wall_cap_s": 1220648, "rss_cap_bytes": M.RAM, "output_cap_bytes": 146028888064}))
    case("K01_output_doubled", lambda: suite.eq(M.next_attempt("P1_M0001", records(1),
        [receipt("STOPPED_OUTPUT_CAP|FAILED")], set())["caps"]["output_cap_bytes"], 292057776128))
    for status in ("CHILD_FAILED|REFUSED", "CHILD_FAILED|BLOCKED"):
        refused = receipt(status)
        solo1 = receipt(status, True, 0)
        solo2 = receipt(status, True, 0)
        case("K01_solo_retry_" + status, lambda refused=refused: (
            suite.eq(M.next_attempt("P1_M0001", records(1), [refused], set())["solo_mode"], True),
            suite.eq(M.next_attempt("P1_M0001", records(1), [refused], set())["caps"], M.first_caps("P1_M0001"))))
        case("N07_terminal_" + status, lambda refused=refused, solo1=solo1, solo2=solo2:
             suite.eq(M.terminal_prefix([refused, solo1, solo2], "P1_M0001"),
                      {"index": 2, "disposition": "UNEVALUATED_INFRA_REPEAT"}))
        case("N07_terminal_no_retry_" + status, lambda refused=refused, solo1=solo1, solo2=solo2:
             suite.any_refusal(lambda: M.next_attempt("P1_M0001", records(3), [refused, solo1, solo2], set())))
    case("N08_different_raw", lambda: suite.eq(M.terminal_prefix([
        receipt("CHILD_FAILED|REFUSED", True, 0), receipt("CHILD_FAILED|BLOCKED", True, 0)], "P1_M0001"), None))
    for label, changes in (("non_solo", {"solo_mode": False}), ("null_sample", {"other_ngc_processes_max": None}),
                            ("different_caps", {"wall_cap_s": 610325})):
        one = receipt("CHILD_FAILED|REFUSED", True, 0)
        two = dict(one, **changes)
        case("N08_" + label, lambda one=one, two=two: suite.eq(M.terminal_prefix([one, two], "P1_M0001"), None))
    infra = receipt("CHILD_FAILED|NONE|SIGNAL", True, 0, 1220648)
    case("N15_infra_separates_rule_c", lambda: (
        suite.eq(M.terminal_prefix([first, rerun, infra, rerun], "P1_M0001"), None),
        suite.eq(M.next_attempt("P1_M0001", records(4), [first, rerun, infra, rerun], set())["attempt"], 5)))
    case("N06_rule_c_terminal", lambda: suite.eq(M.terminal_prefix([first, rerun, rerun], "P1_M0001"),
                                                {"index": 2, "disposition": "RULE_C_INVALID"}))
    case("N01_kit_numbering", lambda: suite.eq(M.next_attempt("S0_J0_SERIAL", [
        {"attempt": 1, "origin": "KIT", "outcome": "MISLAUNCH"},
        {"attempt": 2, "origin": "KIT", "outcome": "LAUNCH"}], [first], set())["attempt"], 3))
    case("N11_kit_carveout", lambda: fail("KIT_RELAUNCH_OWNS", lambda: M.next_attempt(
        "S0_J0_SERIAL", [{"attempt": 1, "origin": "KIT", "outcome": "MISLAUNCH"}], [], set())))
    case("N16_residual_numbering", lambda: suite.eq(M.next_attempt("S0_J0_SERIAL", [], [], {("S0_J0_SERIAL", 1)})["attempt"], 2))
    case("N12_nonattempt_preserves_solo_caps", lambda: suite.eq(M.next_attempt("P1_M0001", records(2), [first], set(),
        {"caps": M.caps_of(rerun), "solo_mode": True})["caps"], M.caps_of(rerun)))
    case("K01_infra_preserves_caps", lambda: suite.eq(M.next_attempt("P1_M0001", records(2), [first, infra], set())["caps"],
                                                    M.caps_of(infra)))
    twin_first = dict(first, wall_cap_s=22752, rss_cap_bytes=M.RAM * 11, output_cap_bytes=34359738368)
    case("K01_twin_rerun", lambda: suite.eq(M.next_attempt(M.TWIN, records(1, "KIT"), [twin_first], set())["caps"],
        {"wall_cap_s": 45504, "rss_cap_bytes": M.RAM * 11, "output_cap_bytes": 34359738368}))
    case("K05_twin_terminal", lambda: suite.any_refusal(lambda: M.next_attempt(M.TWIN, records(1, "KIT"),
        [dict(twin_first, raw_status="TWIN_PLANNED_STOP", status_class="PLANNED_STOP")], set())))
    old = {"spec": {"sha256": "a" * 64}, "point_key": "b" * 64, "v006_spec_pin": {"sha256": "a" * 64},
           "v006_handoff_pin": {"sha256": "c" * 64}}
    case("N04_interrupted_entry_reuse", lambda: suite.eq(M.entry_reuse(old, old, [], [], 1), "ALREADY_REGISTERED_SAME_SPEC"))
    case("N04_refusal_entry_reuse", lambda: suite.eq(M.entry_reuse(old, old, [], [{"attempt": 1}], 1),
                                                  "ALREADY_REGISTERED_SAME_SPEC"))
    case("N09_existing_attempt", lambda: fail("ALREADY_LAUNCHED", lambda: M.entry_reuse(old, old, records(1), [], 1)))
    bad = dict(old, spec={"sha256": "d" * 64})
    case("N09_other_spec", lambda: fail("REGISTRY_ENTRY_EXISTS_FOR_ANOTHER_SPEC", lambda: M.entry_reuse(old, bad, [], [], 1)))


"""Synthetic θ, interface and process-table tests; no live scientific driver."""


def theta_cases(suite):
    import copy
    import math
    M, case, fail = suite.module, suite.case, suite.refuses
    B = M.load_verified(M.REAL["builder"], "_synthetic_p112_builder_contract")
    theta = {"Eref_base_J": 2.5, "ell_F_m": 7.0, "gamma_over_Eref": 0.125,
             "common_scale_s": 1.5, "entropy_K_factor": 3.0}
    theta.update({"synthetic_extra_%02d" % i: float(i) / 8.0 for i in range(8)})
    ngc = dict(theta, ngc3198_distance_Mpc=13.8, ngc3198_inclination_deg=72.0)
    spec = {"physical": {"Eref_J": 2.5, "ell_F_m": 7.0, "gamma": 0.3125, "common_scale_s": 1.5,
                         "entropy_K_factor": 3.0, "distance_Mpc": 13.8, "inclination_deg": 72.0}}
    cfg = {"log_index": 17, "role": "primary_anchor", "order": 0, "member_id": "M000"}
    hand = {"log_index": 17}
    member = dict(cfg, theta_engine=theta, theta_ngc=ngc)
    fd = {"log_index": 17, "role": "primary_anchor", "theta_hex": {k: v.hex() for k, v in theta.items()},
          "theta_natural": dict(theta), "key": M.theta_key(theta)}
    export = {"admitted_points": [{"log_index": 17, "theta_natural": dict(theta)}]}
    def check(m=member, f=fd, h=hand, e=export, s=spec, c=cfg):
        return M.check_member_theta(m, f, h, e, s, spec, c, 0, B)
    case("T01_member", lambda: suite.eq(check()["point_key"], fd["key"]))
    case("T13_thirteen_coordinates", lambda: suite.eq(check()["theta_sha256"], B.theta_sha256(ngc)))
    parent = M.load_verified(M.REAL["orchestrator"], "_synthetic_p112_theta_key_parent")
    case("T13_program_key_equal_pinned_parent", lambda: suite.eq(M.theta_key(theta), parent.theta_key(theta)))
    case("T13_program_and_builder_keys_differ", lambda: suite.eq(M.theta_key(theta) != B.theta_sha256(ngc), True))
    for coord in theta:
        m = copy.deepcopy(member)
        m["theta_engine"][coord] = math.nextafter(theta[coord], math.inf)
        case("T02_PLAN_ulp_" + coord, lambda m=m: fail("THETA_BITS_MISMATCH", lambda: check(m=m)))
        e = copy.deepcopy(export)
        e["admitted_points"][0]["theta_natural"][coord] = math.nextafter(theta[coord], math.inf)
        case("T03_export_ulp_" + coord, lambda e=e: fail("THETA_BITS_MISMATCH", lambda: check(e=e)))
        f = copy.deepcopy(fd)
        f["theta_hex"][coord] = math.nextafter(theta[coord], math.inf).hex()
        case("T04_fdplan_ulp_" + coord, lambda f=f: fail("FDPLAN_THETA_HEX", lambda: check(f=f)))
    for coord in ("Eref_J", "ell_F_m", "gamma", "common_scale_s", "entropy_K_factor"):
        s = copy.deepcopy(spec)
        s["physical"][coord] = math.nextafter(s["physical"][coord], math.inf)
        case("T05_spec_ulp_" + coord, lambda s=s: fail("THETA_BITS_MISMATCH", lambda: check(s=s)))
    for coord in ("distance_Mpc", "inclination_deg"):
        s = copy.deepcopy(spec)
        s["physical"][coord] = math.nextafter(s["physical"][coord], math.inf)
        case("T06_geometry_ulp_" + coord, lambda s=s: fail("THETA_BITS_MISMATCH", lambda: check(s=s)))
    e = copy.deepcopy(export)
    e["admitted_points"][0]["theta_natural"]["synthetic_extra_00"] = -0.0
    case("T07_signed_zero", lambda: fail("THETA_BITS_MISMATCH", lambda: check(e=e)))
    for label in ("extra", "missing"):
        m = copy.deepcopy(member)
        if label == "extra":
            m["theta_engine"]["another"] = 1.0
        else:
            del m["theta_engine"]["ell_F_m"]
        case("T08_keyset_" + label, lambda m=m: fail("THETA_KEY_SET", lambda: check(m=m)))
    for label, changes in (("index", {"log_index": 18}), ("role", {"role": "wrong"}), ("order", {"order": 1}),
                            ("member_id", {"member_id": "M001"})):
        c = dict(cfg, **changes)
        case("T09_identity_" + label, lambda c=c: fail("MEMBER_IDENTITY", lambda: check(c=c)))
    fdp = dict(fd, role="F0")
    fh = {"point_key": fd["key"]}
    case("T01_F0", lambda: suite.eq(M.check_f_theta(fdp, fh, spec, spec, "F0")["theta_sha256"], fd["key"]))
    f = copy.deepcopy(fdp)
    f["theta_hex"]["ell_F_m"] = math.nextafter(7.0, math.inf).hex()
    case("T04_F_ulp", lambda: fail("THETA_BITS_MISMATCH", lambda: M.check_f_theta(f, fh, spec, spec, "F0")))
    changed = dict(ngc, synthetic_extra_07=math.nextafter(ngc["synthetic_extra_07"], math.inf))
    case("T12_changed_theta_ngc_digest", lambda: suite.eq(B.theta_sha256(changed) != B.theta_sha256(ngc), True))
    # 0782: this helper deliberately accepts a different shape-valid digest.
    for label, digest in (("honest", B.theta_sha256(ngc)), ("changed", B.theta_sha256(changed))):
        reg = {"schema": "STEP5_LAUNCH_REGISTRY_C2V003", "phase": "PHASE_1",
               "calls": [{"alternative": "BR_A_F10_PRIMARY", "kind": "MEMBER", "key": "M000",
                          "theta_sha256": digest, "spec_sha256": "a" * 64}]}
        pin = suite.fixture("registry_" + label + ".json", reg)
        case("R01_T12_helper_shape_" + label, lambda pin=pin, digest=digest:
             suite.eq(B._launch_registry(pin, "PHASE_1")[0][("BR_A_F10_PRIMARY", "MEMBER", "M000")]["theta_sha256"], digest))
    # Full builder assembly is prohibited: it would load v003g / slots.
    suite.interfaces["registry_theta_limitation"] = (
        "TESTED: _launch_registry accepts either shape-valid digest. UNTESTED: real PLAN agreement; "
        "deciding test is root's first real Phase-1 registry assembly (0782).")


def process_cases(suite):
    M, case, fail = suite.module, suite.case, suite.refuses
    import os
    from pathlib import Path
    tools = []
    for i, title in enumerate(("driver", "values_writer_c2v004", "handoff_c2v003a", "producer")):
        raw = ("# synthetic inert fixture " + title + "\n").encode()
        path = suite.bytes_fixture("proc_%d.py" % i, raw)
        tools.append({"tool": title, "path": path["path"], "sha256": path["sha256"], "driver_only": i == 0})
    alias = suite.bytes_fixture("byte_alias.py", Path(tools[1]["path"]).read_bytes())
    counter = M.ProcessCounter(tools)
    def row(pid, command, ppid=1):
        return {"pid": pid, "ppid": ppid, "pgid": pid, "command": command}
    rows = [
        row(10, M.PY + " -I -B " + tools[0]["path"] + " run --spec /fake/spec --outdir /fake/out"),
        row(11, M.PY + " -I -B " + tools[0]["path"] + " _stage", 10),
        row(12, M.PY + " -I -B " + tools[0]["path"] + " dry-run"),
        row(13, M.PY + " -I -B " + alias["path"]),
        row(14, M.PY + " -I -B " + tools[2]["path"]),
        row(15, M.PY + " -I -B /fake/root_monitor_c2v001.py --receipt /fake/NGC.receipt.json"),
        row(16, M.PY + " -I -B /fake/dry_one_c2v001.py"),
        row(17, "/bin/bash /fake/twin_kill_watch_c2v003a.sh"),
        row(18, M.PY + " -I -B /fake/phase1_ngc_launch_cx2v001.py _sampler --outdir /fake/NGC"),
    ]
    case("P01_sha_alias_and_exclusions", lambda: suite.eq(
        [r["pid"] for r in counter.count(rows, own_root=10)], [13, 14]))
    case("P01_driver_run_and_stage_counted_elsewhere", lambda: suite.eq(
        [r["pid"] for r in counter.count(rows)], [10, 11, 13, 14]))
    case("P01_values_and_old_handoff_in_real_list", lambda: suite.eq(
        {"values_writer_c2v004_cx2v002", "ngc_acceptance_handoff_c2v003a"} <=
        {x["tool"] for x in M.DECLARED_TOOLS}, True))
    case("P01_declared_list_thirteen", lambda: suite.eq(len(M.DECLARED_TOOLS), 13))
    case("P01_ppid_transitive_closure", lambda: suite.eq(M.descendants(
        [row(1, "a", 0), row(2, "b", 1), row(3, "c", 2), row(4, "d", 3)], 1), {1, 2, 3, 4}))
    case("P01_ps_strict", lambda: fail("PS_PARSE", lambda: M.parse_ps("12 broken command\n")))
    outdir = "/synthetic/NGC_RUN"
    monitor = "/synthetic/synthetic_monitor.py"
    case("N14_reused_monitor_pid", lambda: suite.eq(
        M.qualified_process([row(200, "/bin/sleep 60")], 200, monitor, outdir, "monitor"), None))
    case("C06_reused_sampler_pid", lambda: suite.eq(
        M.qualified_process([row(200, "/bin/sleep 60")], 200, str(suite.tool_path), outdir, "sampler"), None))
    actual_monitor = row(200, M.PY + " -I -B " + monitor + " --receipt " + outdir + ".receipt.json")
    case("N14_qualified_monitor", lambda: suite.eq(
        M.qualified_process([actual_monitor], 200, monitor, outdir, "monitor")["pid"], 200))
    config = {"run_volume": str(suite.root / "volume"), "s0": {"run_root": str(suite.root / "kit_volume" / "NGC_KIT")}}
    (suite.root / "volume").mkdir()
    (suite.root / "kit_volume").mkdir()
    system = M.SyntheticSystem({"mount_points": [config["run_volume"]], "free_bytes": 313532612608, "host_ram_bytes": M.RAM})
    case("N19_wrong_volume_mounted", lambda: fail("RUN_VOLUME_NOT_MOUNTED", lambda: M.mount_first(config, "KIT", system)))
    cap = {"wall_cap_s": 1220648, "rss_cap_bytes": M.RAM, "output_cap_bytes": 292057776128}
    target = str(suite.root / "volume" / "NGC_RUN")
    case("K02_exact_292GiB", lambda: suite.eq(M.disk_check(config, target, cap, system)["free_bytes"], 313532612608))
    smaller = M.SyntheticSystem({"mount_points": [config["run_volume"]], "free_bytes": 313532612607, "host_ram_bytes": M.RAM})
    case("K02_292GiB_minus_one", lambda: fail("DISK_FREE", lambda: M.disk_check(config, target, cap, smaller)))
    pins = {"driver": {"path": "/synthetic/driver.py", "sha256": "a" * 64},
            "monitor": {"path": "/synthetic/monitor.py", "sha256": "b" * 64}}
    spec = {"path": "/synthetic/spec.json", "sha256": "c" * 64}
    for name, wrong in ((M.TWIN, M.RAM), ("P1_M0001", M.RAM * 11)):
        caps = dict(M.first_caps(name), rss_cap_bytes=wrong)
        argv = M.monitor_command(pins, spec, target, caps)
        case("K03_K04_" + name, lambda name=name, caps=caps, argv=argv: fail(
            "RSS_CAP_NOT_CALL_CAP", lambda: M.check_monitor_command(argv, pins, spec, target, caps, name)))
    for real in ("driver", "monitor", "dry_harness"):
        fake = {k: {"path": "/synthetic/" + k + ".py", "sha256": "f" * 64} for k in ("driver", "monitor", "dry_harness")}
        fake[real] = M.REAL[real]
        case("V04_real_" + real, lambda fake=fake: fail("SYNTHETIC_REAL_TOOL", lambda: M.synthetic_fence(fake, {})))
    fake = {k: {"path": "/synthetic/" + k + ".py", "sha256": "f" * 64} for k in ("driver", "monitor", "dry_harness")}
    fake["monitor"]["path"] = "/synthetic/root_monitor_c2v999.py"
    case("V04_monitor_name", lambda: fail("SYNTHETIC_REAL_MONITOR_NAME", lambda: M.synthetic_fence(fake, {})))
    fake["monitor"]["path"] = "/synthetic/monitor.py"
    case("V04_volumes", lambda: fail("SYNTHETIC_VOLUMES", lambda: M.synthetic_fence(fake, {"run_volume": "/Volumes/Fake"})))


"""Real-format receipts from the pinned monitor with an inert synthetic driver."""
SYNTHETIC_DRIVER = r'''import argparse, hashlib, json, os, signal, sys
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument("command")
p.add_argument("--spec")
p.add_argument("--outdir")
a=p.parse_args()
spec=json.loads(Path(a.spec).read_bytes())
mode=spec.get("fixture_mode","COMPLETED")
if mode=="EXIT_BEFORE_MKDIR":sys.exit(1)
if mode=="SIGNAL_BEFORE_MKDIR":os.kill(os.getpid(),signal.SIGTERM)
d=Path(a.outdir);d.mkdir()
result=json.dumps({"synthetic_sentinel":"P112_PRIVATE_SENTINEL_MUST_NOT_BE_READ"},sort_keys=True).encode()
with (d/"result.json").open("xb") as f:f.write(result)
finish={"status":mode,"result_sha256":hashlib.sha256(result).hexdigest()}
with (d/"finish.json").open("x") as f:json.dump(finish,f)
sys.exit(0 if mode in ("COMPLETED","COMPLETED_INVALID") else 1)
'''


def receipt_fixture(suite, label, *, origin="P112", name="P1_M0001", outcome="LAUNCH",
                    mode="COMPLETED", record=True, broken_hash=False, no_receipt=False, off_spec=False,
                    sample=None, ram=None, receipt_changes=None):
    import types
    from pathlib import Path
    M = suite.module
    root = suite.root / label
    root.mkdir()
    for dirname in ("volume", "kit_volume", "launch_root", "kit_launch_root", "copies"):
        (root / dirname).mkdir()
    for volume in ("volume", "kit_volume"):
        (root / volume / "NGC_RUNS").mkdir()
    for launchroot in ("launch_root", "kit_launch_root"):
        for folder in ("registry", "launches", "work", "twin_kill", "outside_set_stop", "assembly", "monitor_refused"):
            (root / launchroot / folder).mkdir()
    def put(name, obj):
        return suite.raw_write(root / name, M.encoded(obj))
    driver = suite.raw_write(root / "inert_synthetic_driver.py", SYNTHETIC_DRIVER.encode())
    spec = put("spec.json", {"fixture_mode": mode, "numerics": {"route_a": {"column_workers": 8 if name == M.TWIN else 1}}})
    registered_spec = put("other_spec.json", {"fixture_mode": "OTHER"}) if off_spec else spec
    class FakeSystem(M.SyntheticSystem):
        def __init__(self):
            super().__init__({"mount_points": [str(root / "volume"), str(root / "kit_volume")],
                              "free_bytes": 1 << 50, "host_ram_bytes": M.RAM if ram is None else ram})
            self.rows = []
        def processes(self):
            return list(self.rows)
    class FixtureContext(M.Context):
        def __init__(self):
            self.system, self.synthetic = FakeSystem(), True
            self.pins = dict(M.REAL, driver=driver)
            self.own_pin = {"path": str(suite.tool_path), "sha256": suite.tool_sha}
            self.cfg = {"python": M.PY, "run_volume": str(root / "volume"), "run_root": str(root / "volume" / "NGC_RUNS"),
                        "p112_launch_root": str(root / "launch_root"), "v006_copy_dir": str(root / "copies"),
                        "s0": {"launch_root": str(root / "kit_launch_root"), "run_root": str(root / "kit_volume" / "NGC_RUNS")},
                        "plan_output_primary": put("PLAN.json", {"members": [], "budget": 0}),
                        "fdplan": put("FDPLAN.json", {"members": [], "F": []}),
                        "selection": put("selection.json", {"points": []}),
                        "plan_build_record": put("plan_build.json", {"status": "BUILT"})}
            text = "## A999: synthetic root\nTOOL_PIN P112_LAUNCHER_CX2V002 %s %s\n" % (suite.tool_sha, suite.tool_path)
            self.cfg["v006"] = suite.raw_write(root / "V006.md", text.encode())["path"]
            self.v006_raw, self.v006_text = text.encode(), text
            self.config_pin = put("config.json", self.cfg)
            self.mapping_block = None
            self._fixture_calls = []
            self._fixture_kit = {}
        def calls(self):
            if self.mapping_block:
                raise M.Refusal(self.mapping_block)
            return self._fixture_calls
        def get_vpin(self, kind, query_name):
            if kind == "SPEC_PIN" and query_name == name:
                return registered_spec
            raise M.Refusal("V006_PIN_MISSING")
        def kit_entries(self):
            return self._fixture_kit
    ctx = FixtureContext()
    outdir = M.planned_outdir(ctx, name, 1, origin)
    monitor = M.load_verified(M.REAL["monitor"], "_p112_verified_synthetic_monitor")
    raw_receipt = str(root / "raw_monitor.receipt.json")
    rec = monitor.run_monitored(driver=driver["path"], driver_sha256=driver["sha256"], spec=spec["path"],
                                outdir=outdir, receipt=raw_receipt, poll_s=0.01,
                                **M.first_caps(name))
    suite.eq(rec["schema"], M.MONITOR_SCHEMA)
    if receipt_changes is not None:
        receipt_changes(rec)
        rec["receipt_sha256"] = M.sha(M.canonical({k:v for k,v in rec.items() if k != "receipt_sha256"}))
    final_receipt = outdir + ".receipt.json"
    if not no_receipt:
        receipt_bytes = M.encoded(rec) if receipt_changes is not None else Path(raw_receipt).read_bytes()
        if broken_hash:
            bad = dict(rec, receipt_sha256="0" * 64)
            receipt_bytes = M.encoded(bad)
        suite.raw_write(Path(final_receipt), receipt_bytes)
    lj_raw = Path(raw_receipt + ".launch.json").read_bytes()
    lj_pin = suite.raw_write(Path(final_receipt + ".launch.json"), lj_raw)
    lj = M.strict_json(lj_raw)
    # Existence-only launch-side outputs. P112 must never open these.
    suite.raw_write(Path(final_receipt + ".stdout.txt"), b"FORBIDDEN_STDOUT_CONTENT\n")
    suite.raw_write(Path(final_receipt + ".stderr.txt"), b"FORBIDDEN_STDERR_CONTENT\n")
    call = {"name": name, "kind": "OTHER" if name == M.TWIN else "MEMBER", "alternative": None if name == M.TWIN else M.PRIMARY,
            "key": name if name == M.TWIN else "M000", "point_key": "c" * 64, "theta_sha256": "b" * 64,
            "spec": registered_spec, "origin": origin, "theta_check": {"fixture": True}}
    entry = {"schema": "UNT_S0_LAUNCH_REGISTRY_ENTRY_C2V003A" if origin == "KIT" else "UNT_P112_LAUNCH_REGISTRY_ENTRY_CX2V001",
             "name": name, "spec": registered_spec, "point_key": call["point_key"], "theta_key": call["point_key"],
             "theta_sha256": call["theta_sha256"], "v006_spec_pin": registered_spec}
    entry_path = (root / "kit_launch_root" / "registry" / (name + "_C2V003A.json") if origin == "KIT" else
                  Path(M.own_registry_path(ctx, name)))
    entry_pin = suite.raw_write(entry_path, M.encoded(entry))
    call.update({"entry": entry if origin == "KIT" else None, "entry_pin": entry_pin if origin == "KIT" else None})
    ctx._fixture_calls = [call]
    if origin == "KIT":
        ctx._fixture_kit[name] = (entry, entry_pin)
    record_doc = {
        "schema": "UNT_" + ("S0_" + outcome + "_RECORD_C2V003A" if origin == "KIT" else "P112_" + outcome + "_RECORD_CX2V001"),
        "name": name, "attempt": 1, "outcome": outcome, "outdir": outdir, "receipt": final_receipt,
        "launch_json": dict(lj_pin, utc=lj["utc"], child_pid=lj["child_pid"]),
        "spec": registered_spec, "driver": driver, "monitor": M.REAL["monitor"], "caps": M.first_caps(name),
        "monitor_pid": 900001, "sampler_pid": 900002, "watch_pid": 900003 if name == M.TWIN else None,
        "host_ram_bytes": M.RAM, "solo_mode": False, "counted_rerun": False,
        "registry_entry": entry_pin, "date_u": M.date_u()}
    record_name = ("%s_%s_C2V003A_A1.json" % (name, outcome) if origin == "KIT" else
                   "P112_%s_%s_CX2V001_A1.json" % (name, outcome))
    record_path = root / ("kit_launch_root" if origin == "KIT" else "launch_root") / "launches" / record_name
    if record:
        suite.raw_write(record_path, M.encoded(record_doc))
    if sample is not None:
        start, end = M.timestamp(rec["utc_start"]), M.timestamp(rec["utc_end"])
        fmt = lambda t: M.dt.datetime.fromtimestamp(t, M.dt.timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")
        s = {"schema": "STEP5_SOLO_SAMPLE_CX2V001", "name": name, "attempt": 1, "outdir": outdir,
             "declared_list_sha256": M.DECLARED_LIST_SHA, "poll_s": 5, "n_samples": 3,
             "first_utc": fmt(start - 2), "last_utc": fmt(end + 2), "largest_gap_s": 5.0,
             "complete": True, "max_other_ngc_processes": 0, "nonzero_samples": [], "writer": ctx.own_pin,
             "date_u": M.date_u()}
        s.update(sample)
        suite.raw_write(Path(outdir + ".solo.json"), M.encoded(s))
    return types.SimpleNamespace(ctx=ctx, name=name, root=root, outdir=outdir, rec=rec, record=record_doc,
                                 record_path=record_path, call=call, entry_pin=entry_pin, launch_pin=lj_pin)


"""Receipt/registry integration tests. All output trees are synthetic fixtures."""


def close_cases(suite):
    import json
    import sys
    from pathlib import Path
    M, case, fail = suite.module, suite.case, suite.refuses
    audit = []
    synthetic_outdirs = []
    def hook(event, args):
        if event != "open" or not isinstance(args[0], (str, bytes)):
            return
        path = args[0].decode() if isinstance(args[0], bytes) else args[0]
        frame = sys._getframe(1)
        from_p112 = False
        while frame:
            if frame.f_code.co_filename == str(suite.tool_path):
                from_p112 = True
                break
            frame = frame.f_back
        if not from_p112:
            return
        audit.append(path)
        if any(path.startswith(p + "/") for p in synthetic_outdirs):
            raise AssertionError("P112 opened synthetic outdir contents: " + path)
        if path.endswith((".receipt.json.stdout.txt", ".receipt.json.stderr.txt")):
            raise AssertionError("P112 opened receipt stdout/stderr: " + path)
    sys.addaudithook(hook)
    def fixture(label, **kwargs):
        f = receipt_fixture(suite, label, **kwargs)
        synthetic_outdirs.append(f.outdir)
        return f
    def no_write(f, code, action=None):
        before = {str(p) for p in f.root.rglob("*")}
        fail(code, action or (lambda: M.close_attempt(f.ctx, f.name, 1)))
        suite.eq({str(p) for p in f.root.rglob("*")}, before)
    honest = fixture("C01_own")
    case("C01_own_real_monitor", lambda: suite.eq(M.close_attempt(honest.ctx, honest.name, 1)["status_class"], "FINISHED"))
    case("C12_second_close_no_write", lambda: no_write(honest, "ATTEMPT_ALREADY_CLOSED"))
    kit = fixture("C01_kit", origin="KIT", name="S0_SEED_SERIAL")
    case("C01_kit_real_monitor", lambda: suite.eq(M.close_attempt(kit.ctx, kit.name, 1)["status_class"], "FINISHED"))
    f = fixture("C02_missing_monitor", no_receipt=True)
    case("C02_missing_receipt_no_write", lambda: no_write(f, "MONITOR_ENDED_NO_RECEIPT"))
    f = fixture("C03_missing_launch_record", record=False)
    case("C03_N20_missing_launch_record", lambda: no_write(f, "LAUNCH_RECORD_MISSING"))
    f = fixture("C04_two_records")
    bad = dict(f.record, schema="UNT_P112_MISLAUNCH_RECORD_CX2V001", outcome="MISLAUNCH")
    suite.raw_write(f.record_path.with_name("P112_" + f.name + "_MISLAUNCH_CX2V001_A1.json"), M.encoded(bad))
    case("C04_two_records_no_write", lambda: no_write(f, "ATTEMPT_RECORD_NOT_UNIQUE"))
    f = fixture("C05_twin_watch", name=M.TWIN, origin="KIT")
    f.ctx.system.rows = [{"pid": 900003, "ppid": 1, "pgid": 900003, "command":
                         "/bin/bash " + M.REAL["twin_watch"]["path"] + " --outdir " + f.outdir}]
    case("C05_live_watch_no_write", lambda: no_write(f, "TWIN_WATCH_STILL_ALIVE"))
    f = fixture("C06_sampler")
    f.ctx.system.rows = [{"pid": 900002, "ppid": 1, "pgid": 900002, "command":
                         M.PY + " -I -B " + str(suite.tool_path) + " _sampler --outdir " + f.outdir}]
    case("C06_live_sampler_no_write", lambda: no_write(f, "SAMPLER_STILL_ALIVE"))
    f = fixture("C06_reused_sampler")
    f.ctx.system.rows = [{"pid": 900002, "ppid": 1, "pgid": 900002, "command": "/bin/sleep 60"}]
    case("C06_reused_pid_passes", lambda: suite.eq(M.close_attempt(f.ctx, f.name, 1)["status_class"], "FINISHED"))
    f = fixture("C07_no_mapping", origin="KIT", name="S0_J0_SERIAL")
    f.ctx.mapping_block = "PLAN_MAPPING_MISSING"
    case("C07_mapping_before_write", lambda: no_write(f, "PLAN_MAPPING_MISSING"))
    f = fixture("C08_outside_set", origin="KIT", name="S0_J0_SERIAL")
    f.ctx._fixture_calls = []
    case("C08_outside_set_no_write", lambda: no_write(f, "CALL_NOT_IN_ACTUAL_SET"))
    f = fixture("C09_off_spec", off_spec=True)
    case("C09_off_spec_no_write", lambda: no_write(f, "NOT_AN_ATTEMPT"))
    for mode in ("EXIT_BEFORE_MKDIR", "SIGNAL_BEFORE_MKDIR"):
        f = fixture("C10_" + mode, mode=mode)
        case("C10_N17_" + mode, lambda f=f: no_write(f, "NOT_AN_ATTEMPT"))
        case("N17_next_legal_" + mode, lambda f=f: suite.eq(M.next_attempt(
            f.name, M.history(f.ctx, f.call)["records"], [], set(),
            M.history(f.ctx, f.call)["trailing_nonattempt"])["attempt"], 2))
    f = fixture("C11_self_hash", broken_hash=True)
    case("C11_self_hash_no_write", lambda: no_write(f, "MONITOR_RECEIPT_SELF_HASH"))
    f = fixture("C13_wrong_ram", ram=M.RAM + 1)
    case("C13_ram_no_write", lambda: no_write(f, "HOST_RAM_MISMATCH"))
    for label, sample in (
            ("absent", None), ("incomplete", {"complete": False}), ("gap", {"largest_gap_s": 100.0}),
            ("first", {"first_utc": "2099-01-01T00:00:00.000000Z"}),
            ("last", {"last_utc": "2000-01-01T00:00:00.000000Z"})):
        f = fixture("C14_" + label, sample=sample)
        def check(f=f):
            result = M.close_attempt(f.ctx, f.name, 1)
            doc = M.read_pin(result["receipt"])
            suite.eq(doc["other_ngc_processes_max"], None)
        case("C14_null_" + label + "_still_closes", check)
    f = fixture("C14_valid_sample", sample={})
    case("C14_complete_sample_zero", lambda: suite.eq(M.read_pin(
        M.close_attempt(f.ctx, f.name, 1)["receipt"])["other_ngc_processes_max"], 0))
    # Gate checks happen before every write-producing public operation.
    f = fixture("L06_missing_gate")
    f.ctx.v006_text = "## A999: synthetic without TOOL_PIN\n"
    for command, action in (
            ("close", lambda: M.close_attempt(f.ctx, f.name, 1)),
            ("assembly", lambda: M.assemble_registry(f.ctx)),
            ("verify", lambda: M.assemble_registry(f.ctx, verify=True)),
            ("outside", lambda: M.stop_outside_set(f.ctx, "S0_J0_SERIAL")),
            ("monitor_refused", lambda: M.record_monitor_refused(f.ctx, {}, str(f.root)))):
        case("L06_" + command + "_no_write", lambda action=action: no_write(f, "TOOL_PIN_MISSING", action))
    f = fixture("N19_unmounted", origin="KIT", name="S0_J0_SERIAL")
    f.ctx.system.fixture["mount_points"] = [f.ctx.cfg["run_volume"]]
    case("N19_close_correct_kit_volume", lambda: no_write(f, "RUN_VOLUME_NOT_MOUNTED"))
    case("N19_status_correct_kit_volume", lambda: suite.eq(M.status(f.ctx)["calls"][0]["status"], "RUN_VOLUME_NOT_MOUNTED"))
    f.ctx.system.fixture["mount_points"].append(str(Path(f.ctx.cfg["s0"]["run_root"]).parent))
    case("N19_mount_restored_closes", lambda: suite.eq(M.close_attempt(f.ctx, f.name, 1)["status_class"], "FINISHED"))
    # Byte verification and the real builder's nine-role interface.
    B = M.load_verified(M.REAL["builder"], "_p112_receipt_contract_builder")
    receipt = M.pin_of(honest.outdir + ".attempt_receipt.json")
    cfg = B._receipt_cfg(M.RECEIPT_KEYS, M.STATUS_CLASSES)
    case("R02_builder_nine_roles", lambda: (
        suite.eq(B._receipt(receipt, cfg, "synthetic")[1], "FINISHED|COMPLETED"),
        suite.eq(B._receipt(receipt, cfg, "synthetic")[5]["theta_sha256"], "b" * 64)))
    suite.interfaces["receipt_residence"] = (
        "TESTED helper projection reads nine roles. c2v006 _terminal requires receipt inside run_dir; "
        "P112's true sibling residence needs root's c2v007. Full assembly was not called.")
    case("R01_assembled_real_builder", lambda: suite.eq(len(B._launch_registry(
        M.assemble_registry(honest.ctx)["registry"], "PHASE_1")[0]), 1))
    case("R03_honest_verify", lambda: suite.eq(M.assemble_registry(honest.ctx, verify=True)["status"], "VERIFIED"))
    f = fixture("R03_changed_registry")
    M.close_attempt(f.ctx, f.name, 1)
    raw, _ = M.registry_bytes(f.ctx)
    bad = json.loads(raw)
    bad["calls"][0]["theta_sha256"] = "d" * 64
    p = Path(f.ctx.cfg["p112_launch_root"]) / "assembly" / "STEP5_LAUNCH_REGISTRY_PHASE1_CX2V001.json"
    suite.raw_write(p, M.encoded(bad))
    case("R03_T12_changed_digest_verify_refuses", lambda: no_write(f, "REGISTRY_BYTE_VERIFY",
        lambda: M.assemble_registry(f.ctx, verify=True)))
    case("G02_no_second_cutoff", lambda: fail("CUTOFF_ALREADY_WRITTEN",
        lambda: M.write_cutoff(honest.ctx, [{"time_utc": "2026-10-20T00:00:00Z"}])))
    f = fixture("G01_max_cutoff")
    terms = [{"name": "newer_already_closed", "time_utc": "2026-10-20T16:00:00Z", "receipt": receipt, "disposition": "FINISHED"},
             {"name": "older_completing", "time_utc": "2026-10-20T15:00:00Z", "receipt": receipt, "disposition": "FINISHED"}]
    case("G01_T_is_set_maximum", lambda: suite.eq(M.read_pin(M.write_cutoff(f.ctx, terms))["T"], "2026-10-20T16:00:00Z"))
    def no_sentinel():
        for outdir in synthetic_outdirs:
            p = Path(outdir + ".attempt_receipt.json")
            if p.exists():
                suite.eq(b"P112_PRIVATE_SENTINEL_MUST_NOT_BE_READ" in p.read_bytes(), False)
        suite.eq(any(p.endswith("/result.json") for p in audit), False)
    case("V03_no_output_opens_or_sentinel_projection", no_sentinel)
    suite.interfaces["P112_open_audit"] = {"p112_open_events": len(audit), "forbidden_output_opens": 0}


"""Refusal/residual custody tests, including the binding 0782 log ruling."""


def history_cases(suite):
    from pathlib import Path
    import copy
    M, case, fail = suite.module, suite.case, suite.refuses
    def own_refusal_fixture(label, *, extra=False, missing_absent=False, bad_log=False, missing_log=False,
                            origin="P112", relaunched=False):
        name = "S0_J0_SERIAL" if origin == "KIT" else "P1_M0001"
        f = receipt_fixture(suite, label, origin=origin, name=name, mode="FAILED")
        M.close_attempt(f.ctx, f.name, 1)
        k = 1 if relaunched else 2
        outdir = M.planned_outdir(f.ctx, name, k, origin)
        root = Path(f.ctx.cfg["s0"]["launch_root"] if origin == "KIT" else f.ctx.cfg["p112_launch_root"])
        work = root / "work" / "refused_invocation"
        work.mkdir()
        plan = {"schema": "S0_LAUNCH_PLAN_C2V003A" if origin == "KIT" else "UNT_P112_LAUNCH_PLAN_CX2V001",
                "name": name, "attempt": k, "outdir": outdir, "config": f.ctx.config_pin,
                "caps": M.first_caps(name), "solo_mode": False, "date_u": M.date_u()}
        plan_pin = suite.raw_write(work / "plan.json", M.encoded(plan))
        text = b"synthetic monitor refusal\n"
        stdout = {"path": str(work / "monitor.stdout.txt"), "sha256": M.sha(text)}
        if not missing_log:
            suite.raw_write(work / "monitor.stdout.txt", text + (b"x" if bad_log else b""))
        stderr = suite.raw_write(work / "monitor.stderr.txt", b"")
        rec = {"schema": "MONITOR_REFUSED_ATTEMPT_RECORD_C2V001", "name": name, "attempt": k,
               "launcher": "KIT_C2V003A" if origin == "KIT" else "P112_CX2V001",
               "writer": {"name": "ROOT", "sha256": None} if origin == "KIT" else
               {"name": M.TOOL_NAME, "sha256": suite.tool_sha},
               "plan": plan_pin, "monitor_stdout": stdout, "monitor_stderr": stderr,
               "absent": M.absent_paths(outdir), "date_u": M.date_u(), "rule": "SYNTHETIC D7 fixture"}
        if extra:
            rec["extra"] = "not allowed"
        if missing_absent:
            del rec["absent"]["receipt_stdout"]
        path = (root / "monitor_refused" / ("%s_MONITOR_REFUSED_C2V003A_A%d.json" % (name, k)) if origin == "KIT" else
                root / "launches" / ("P112_%s_MONITOR_REFUSED_CX2V001_A%d.json" % (name, k)))
        suite.raw_write(path, M.encoded(rec))
        f.refusal_plan, f.refusal_work, f.refusal_outdir, f.refusal_k = plan_pin, work, outdir, k
        return f
    f = own_refusal_fixture("N04_own_refusal")
    case("N04_refusal_does_not_consume_k", lambda: suite.eq(
        M.next_attempt(f.name, M.history(f.ctx, f.call)["records"], M.history(f.ctx, f.call)["actual"], set())["attempt"], 2))
    case("N04_refusal_no_solo_file", lambda: suite.eq(Path(f.refusal_outdir + ".solo.json").exists(), False))
    case("N05_refusal_twice_no_overwrite", lambda: fail("MONITOR_REFUSED_TWICE",
        lambda: M.record_monitor_refused(f.ctx, f.refusal_plan, str(f.refusal_work))))
    case("N05_next_attempt_still_admitted", lambda: suite.eq(M.status(f.ctx)["calls"][0]["next"]["attempt"], 2))
    f = own_refusal_fixture("N10_root_kit_refusal", origin="KIT")
    case("N10_root_kit_record_accepted", lambda: suite.eq(
        M.refusal_records(f.ctx, f.name, f.ctx.records(f.name))[0]["reason"], "MONITOR_REFUSED"))
    for label, kwargs, code in (
            ("extra_key", {"extra": True}, "EXACT_KEYS"),
            ("missing_absent", {"missing_absent": True}, "EXACT_KEYS"),
            ("changed_old_log", {"bad_log": True}, "PIN_SHA_MISMATCH"),
            ("missing_old_log", {"missing_log": True}, "WORK_LOG_MISSING")):
        f = own_refusal_fixture("N10_" + label, origin="KIT", **kwargs)
        case("N10_0782_" + label, lambda f=f, code=code: fail(code,
            lambda: M.refusal_records(f.ctx, f.name, f.ctx.records(f.name))))
    f = own_refusal_fixture("N10_relaunch_matches_old_logs", origin="KIT", relaunched=True)
    case("N10_0782_relaunch_old_logs_rehashed", lambda: suite.eq(
        M.refusal_records(f.ctx, f.name, f.ctx.records(f.name))[0]["log_rehash_deferred"], False))
    case("N10_0782_status_relaunch_accepted", lambda: suite.eq(M.status(f.ctx)["calls"][0]["status"], "READY"))
    case("N10_0782_assembly_relaunch_accepted", lambda: suite.eq(
        M.registry_bytes(f.ctx)[1]["nonattempts"][0]["reason"], "MONITOR_REFUSED"))
    f = own_refusal_fixture("N10_relaunch_old_log_changed", origin="KIT", relaunched=True, bad_log=True)
    case("N10_0782_relaunch_changed_byte_refused", lambda: fail("PIN_SHA_MISMATCH",
        lambda: M.refusal_records(f.ctx, f.name, f.ctx.records(f.name))))
    f = own_refusal_fixture("N10_absent_path_exists")
    suite.raw_write(Path(f.refusal_outdir + ".receipt.json"), b"synthetic existence marker")
    case("N10_absent_rechecked_before_relaunch", lambda: fail("MONITOR_REFUSED_ABSENT_EXISTS",
        lambda: M.refusal_records(f.ctx, f.name, f.ctx.records(f.name))))

    # Residual: monitor receipt absent on a mounted volume, qualified monitor gone.
    for origin, name in (("P112", "P1_M0001"), ("KIT", "S0_J0_SERIAL")):
        f = receipt_fixture(suite, "N14_" + origin, origin=origin, name=name, no_receipt=True)
        case("N14_status_" + origin, lambda f=f: suite.eq(M.status(f.ctx)["calls"][0]["status"], "MONITOR_ENDED_NO_RECEIPT"))
        f.ctx.system.rows = [{"pid": 900001, "ppid": 1, "pgid": 900001, "command": "/bin/sleep 60"}]
        case("N14_reused_pid_status_" + origin, lambda f=f: suite.eq(
            M.status(f.ctx)["calls"][0]["status"], "MONITOR_ENDED_NO_RECEIPT"))
        f.ctx.v006_text += "RESIDUAL_RETRY %s 1\n" % name
        def next_residual(f=f):
            h = M.history(f.ctx, f.call)
            return M.next_attempt(f.name, h["records"], h["actual"], h["residuals"], h["trailing_nonattempt"])
        case("N14_residual_retry_" + origin, lambda next_residual=next_residual:
             suite.eq(next_residual()["attempt"], 2))
        command = " ".join(M.driver_command(f.ctx.pins, f.call["spec"], f.outdir))
        f.ctx.system.rows = [{"pid": 900010, "ppid": 1, "pgid": 900010, "command": command}]
        case("N14_orphan_blocks_" + origin, lambda f=f: fail("RESIDUAL_ATTEMPT_PROCESS_ALIVE",
                                                           lambda: M.history(f.ctx, f.call)))
        f.ctx.system.rows = []
        case("N14_orphan_gone_" + origin, lambda next_residual=next_residual:
             suite.eq(next_residual()["caps"], M.first_caps(name)))
    f = receipt_fixture(suite, "N14_line_with_receipt")
    f.ctx.v006_text += "RESIDUAL_RETRY %s 1\n" % f.name
    case("N14_receipt_invalidates_line", lambda: fail("RESIDUAL_RETRY_NOT_RESIDUAL", lambda: M.history(f.ctx, f.call)))
    case("N19_assembly_receipt_invalidates_line", lambda: fail("RESIDUAL_RETRY_NOT_RESIDUAL",
                                                              lambda: M.assemble_registry(f.ctx)))
    f.ctx.v006_text += "RESIDUAL_RETRY P1_M0001 01\n"
    case("N14_malformed_launch_refuses_first", lambda: fail("RESIDUAL_RETRY_MALFORMED",
                                                           lambda: M.launch(f.ctx, f.name)))
    case("N19_malformed_assembly_refuses", lambda: fail("RESIDUAL_RETRY_MALFORMED",
                                                      lambda: M.assemble_registry(f.ctx)))
    for outcome in ("LAUNCH", "MISLAUNCH"):
        f = receipt_fixture(suite, "N12_nonattempt_" + outcome, mode="EXIT_BEFORE_MKDIR", outcome=outcome)
        h = M.history(f.ctx, f.call)
        case("N12_N17_no_outdir_" + outcome, lambda h=h: suite.eq(h["actual"], []))
        case("N12_N17_retry_" + outcome, lambda f=f, h=h: suite.eq(M.next_attempt(
            f.name, h["records"], h["actual"], h["residuals"], h["trailing_nonattempt"])["attempt"], 2))
    # A missing launch record is distinct from either residual. Resume owns it.
    f = receipt_fixture(suite, "N20_missing_launch_record", record=False)
    case("N20_status_missing_launch_record", lambda: suite.eq(M.status(f.ctx)["calls"][0]["status"], "LAUNCH_RECORD_MISSING"))
    f.ctx.v006_text += "RESIDUAL_RETRY %s 1\n" % f.name
    case("N20_launch_json_not_residual", lambda: fail("RESIDUAL_RETRY_NOT_RESIDUAL", lambda: M.history(f.ctx, f.call)))


"""Sampler state-machine and solo interlock tests with an injected clock."""


def sampler_cases(suite):
    from pathlib import Path
    M, case, fail = suite.module, suite.case, suite.refuses
    def accelerated(f, initially_unmounted=False):
        clock = {"now": 0.0, "mount_calls": 0, "restored_at": None}
        f.ctx.system.monotonic = lambda: clock["now"]
        f.ctx.system.sleep = lambda seconds: clock.update(now=clock["now"] + seconds)
        old_mounted = f.ctx.system.mounted
        def mounted(volume):
            clock["mount_calls"] += 1
            if initially_unmounted and clock["now"] < 100:
                return False
            if clock["restored_at"] is None:
                clock["restored_at"] = clock["now"]
            return old_mounted(volume)
        f.ctx.system.mounted = mounted
        return clock
    f = receipt_fixture(suite, "P07_sampler_no_launch_record", mode="FAILED")
    # A new, absent attempt path. Only the synthetic work metadata is written.
    outdir = M.planned_outdir(f.ctx, f.name, 2, "P112")
    work = f.root / "launch_root" / "work" / "sampler_refused"
    work.mkdir()
    suite.raw_write(work / "monitor_pid.json", M.encoded({"monitor_pid": 900001}))
    plan = {"name": f.name, "attempt": 2, "outdir": outdir, "config": f.ctx.config_pin}
    accelerated(f)
    case("P07_sampler_refusal_no_output", lambda: (
        suite.eq(M.sampler(f.ctx, plan, str(work), poll_s=1)["status"], "MONITOR_REFUSED_NO_SOLO_FILE"),
        suite.eq(Path(outdir + ".solo.json").exists(), False)))
    for label, unmounted in (("mounted", False), ("unmounted_then_restored", True)):
        f = receipt_fixture(suite, "N14_sampler_" + label, no_receipt=True)
        work = f.root / "launch_root" / "work" / "sampler_no_receipt"
        work.mkdir()
        plan = {"name": f.name, "attempt": 1, "outdir": f.outdir, "config": f.ctx.config_pin}
        clock = accelerated(f, initially_unmounted=unmounted)
        def check(f=f, work=work, plan=plan, clock=clock, unmounted=unmounted):
            result = M.sampler(f.ctx, plan, str(work), poll_s=1)
            suite.eq(result["status"], "MONITOR_ENDED_NO_RECEIPT_NO_SOLO_FILE")
            suite.eq(Path(f.outdir + ".solo.json").exists(), False)
            suite.eq(clock["now"] >= (160 if unmounted else 60), True)
        case("N14_N19_sampler_wait_" + label, check)
    f = receipt_fixture(suite, "P03_first_ps_failure")
    work = f.root / "launch_root" / "work" / "sampler_first_failure"
    work.mkdir()
    def broken_ps():
        raise M.Refusal("PS_FAILED")
    f.ctx.system.processes = broken_ps
    plan = {"name": f.name, "attempt": 2, "outdir": M.planned_outdir(f.ctx, f.name, 2, "P112"), "config": f.ctx.config_pin}
    case("N04_failed_first_sample_recoverable_no_solo", lambda: (
        suite.eq(M.sampler(f.ctx, plan, str(work), poll_s=1)["status"], "FIRST_SAMPLE_FAILED_NO_SOLO_FILE"),
        suite.eq(Path(plan["outdir"] + ".solo.json").exists(), False)))
    f = receipt_fixture(suite, "P04_solo_guard")
    f.ctx.system.rows = [{"pid": 900010, "ppid": 1, "pgid": 900010,
                         "command": M.PY + " -I -B " + M.REAL["driver"]["path"] + " run --spec /fake/spec --outdir /fake/out"}]
    case("P04_listed_process_blocks_solo", lambda: fail("OTHER_NGC_PROCESS_ALIVE", lambda: M.enforce_solo(f.ctx, True)))
    for label, counted in (("rule_c", True), ("refusal_retry", False)):
        f = receipt_fixture(suite, "P05_active_" + label)
        active = dict(f.record, origin="P112", solo_mode=True, counted_rerun=counted)
        f.ctx.records = lambda name=None, active=active: [active]
        f.ctx.system.rows = [{"pid": 900001, "ppid": 1, "pgid": 900001, "command":
                             M.PY + " -I -B " + M.REAL["monitor"]["path"] + " --receipt " + f.outdir + ".receipt.json"}]
        case("P05_active_solo_" + label, lambda f=f: fail("SOLO_RERUN_ACTIVE", lambda: M.enforce_solo(f.ctx, False)))
    f = receipt_fixture(suite, "N03_kit_write_guard")
    case("N03_no_kit_launch_write", lambda: fail("WRITE_KIT_LAUNCHES", lambda: f.ctx.write(
        str(Path(f.ctx.cfg["s0"]["launch_root"]) / "launches" / "FORBIDDEN.json"), {"date_u": M.date_u()})))
    # Load the kit exactly as allowed; the test calls no run/plan subcommand.
    kit = M.load_verified(M.REAL["kit"], "_synthetic_p112_kit_namespace")
    for name in ("P1_M0001", "S0_SEED_SERIAL", M.TWIN):
        for outcome in ("LAUNCH", "MISLAUNCH", "MONITOR_REFUSED"):
            path = "P112_%s_%s_CX2V001_A1.json" % (name, outcome)
            case("N02_kit_regex_" + name + "_" + outcome, lambda path=path: suite.eq(kit.ATTEMPT_RE.match(path), None))
    plan = {"paths": {"launches_dir": str(Path(f.ctx.cfg["s0"]["launch_root"]) / "launches")}}
    import contextlib, io, types
    plan.update({"schema":"S0_LAUNCH_PLAN_C2V003A", "names":{"spec_pin":"S0_SEED_SERIAL"},
                 "attempt":1,"call":"serial","role":"seed"})
    plan["paths"]["record"] = f.entry_pin["path"]
    plan_pin = suite.raw_write(f.root / "kit_order_check_plan.json", M.encoded(plan))
    def order_output():
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            code = kit.cmd_order_check(types.SimpleNamespace(plan=plan_pin["path"]))
        return code, stream.getvalue()
    order_before = order_output()
    case("N02_kit_order_before_passes", lambda: suite.eq(order_before[0], 0))
    before = kit.attempt_records(plan)
    suite.raw_write(Path(f.ctx.cfg["p112_launch_root"]) / "launches" / "P112_P1_OTHER_LAUNCH_CX2V001_A1.json",
                    M.encoded({"synthetic": True}))
    case("N02_kit_attempt_inventory_unchanged", lambda: suite.eq(kit.attempt_records(plan), before))
    case("N02_kit_order_output_unchanged", lambda: suite.eq(order_output(), order_before))
    for k in ("0", "01", "1", "9", "10", "99", "100"):
        filename = "S0_J0_SERIAL_LAUNCH_C2V003A_A" + k + ".json"
        case("N02_exact_kit_number_grammar_" + k, lambda filename=filename: suite.eq(
            bool(M.KIT_ATTEMPT_RE.fullmatch(filename)), bool(kit.ATTEMPT_RE.fullmatch(filename))))
    suite.interfaces["sampler_clock_tests"] = (
        "TESTED with an injected clock: monitor refusal, first ps failure, 60 mounted seconds, and mount restoration. "
        "These do not claim elapsed wall-clock or production-machine sampling.")


"""A wholly synthetic, file-backed configuration for the public launch CLI."""


def full_launch_fixture(suite, label, duplicate_f0=False):
    import copy
    import types
    from pathlib import Path
    M = suite.module
    root = suite.root / label
    root.mkdir()
    def raw(name, data):
        p = root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        return suite.raw_write(p, data)
    def put(name, obj):
        return raw(name, M.encoded(obj))
    for folder in ("volume/NGC_RUNS", "kit_volume/NGC_RUNS", "launch_root", "kit_root/registry",
                   "kit_root/launches", "copies"):
        (root / folder).mkdir(parents=True, exist_ok=True)
    driver = raw("inert_fixture_driver.py", SYNTHETIC_DRIVER.encode())
    # This wrapper uses the explicitly authorized verified monitor API, on the
    # synthetic driver only. Its own path/pin is used in the monitor's receipts.
    wrapper = '''import hashlib,types
from pathlib import Path
source=Path(%r)
data=source.read_bytes()
assert hashlib.sha256(data).hexdigest()==%r
m=types.ModuleType("_authorized_synthetic_monitor")
m.__file__=__file__
exec(compile(data,str(source),"exec"),m.__dict__)
raise SystemExit(m.main())
''' % (M.REAL["monitor"]["path"], M.REAL["monitor"]["sha256"])
    monitor = raw("synthetic_monitor.py", wrapper.encode())
    dry_source = '''import hashlib,json,sys
from pathlib import Path
driver,driver_sha,spec,spec_sha,report,log=sys.argv[1:]
assert hashlib.sha256(Path(driver).read_bytes()).hexdigest()==driver_sha
assert hashlib.sha256(Path(spec).read_bytes()).hexdigest()==spec_sha
Path(report).mkdir()
r={"executed_stages":0,"binding_blockers":[],"source_build_blockers":[],
   "future_stage_dependencies":[{"class":"PENDING_ROUTE_A_OUTPUTS"}],"planned_route_a":True}
with (Path(report)/"NGC_SOURCE_BUILD_READINESS.json").open("x") as f:json.dump(r,f)
l={"exit":0,"blocked":[],"ctx_modes":["simulate"],"driver_sha256":driver_sha,"spec_sha256":spec_sha}
with Path(log).open("x") as f:json.dump(l,f)
'''
    dry = raw("synthetic_dry_harness.py", dry_source.encode())
    watch = raw("synthetic_passive_watch.py", b"import time\ntime.sleep(120)\n")
    lo = put("synthetic_LO.json", {"schema": "SYNTHETIC_LO_PIN"})
    policy = put("synthetic_policy.json", {"schema": "SYNTHETIC_POLICY_NO_SLOTS"})
    spec_of_record = put("synthetic_spec_of_record.json", {"schema": "SYNTHETIC_SPEC_OF_RECORD"})
    def theta(ell):
        return {"Eref_base_J": 2.5, "ell_F_m": float(ell), "gamma_over_Eref": 0.125,
                "common_scale_s": 1.5, "entropy_K_factor": 3.0}
    def fd_point(th, role, **extra):
        return dict(theta_natural=th, theta_hex={k: v.hex() for k, v in th.items()}, key=M.theta_key(th), role=role, **extra)
    engine = theta(7)
    member = {"member_id": "M000", "log_index": 1, "role": "primary_anchor", "evaluated": False,
              "theta_engine": engine, "theta_ngc": dict(engine, ngc3198_distance_Mpc=13.8, ngc3198_inclination_deg=72.0)}
    plan = put("PLAN_PRIMARY.json", {"ok": True, "budget": 0, "evaluations_used": 0, "members": [member]})
    selection = put("SELECTION.json", {"points": [{"log_index": 1, "role": "primary_anchor"}]})
    build = put("PLAN_BUILD.json", {"status": "BUILT", "stage": "PLAN", "phase": "PHASE_1"})
    export = put("EXPORT.json", {"schema": "UNT_STEP5_ADMITTED_POINT_EXPORT_CX3V001", "target_free": True,
                               "admitted_points": [{"log_index": 1, "theta_natural": engine}]})
    fs = [fd_point(engine if duplicate_f0 and k == 0 else theta(8 + k), "F%d" % k) for k in range(3)]
    fdplan = put("FDPLAN.json", {"schema": "PHASE1_FDPLAN_C2V001",
                               "members": [fd_point(engine, "primary_anchor", log_index=1)], "F": fs})
    at0 = put("AT0A.json", {"schema": "PHASE1_AT0A_C2V001", "outcome": "PASS"})
    lines = ["## A999: SYNTHETIC P112 TEST",
             "TOOL_PIN P112_LAUNCHER_CX2V002 %s %s" % (suite.tool_sha, suite.tool_path),
             "WATCH_PIN MEMORY_WATCH %s %s" % (watch["sha256"], watch["path"])]
    def spec_for(th, key, eps, leaf=1):
        return {"fixture_mode": "COMPLETED", "label": "step5 A_K32_A2_HEADLINE theta_key=" + key,
                "physical": {"Eref_J": th["Eref_base_J"], "ell_F_m": th["ell_F_m"],
                             "gamma": th["gamma_over_Eref"] * th["Eref_base_J"],
                             "common_scale_s": th["common_scale_s"], "entropy_K_factor": th["entropy_K_factor"],
                             "distance_Mpc": 13.8, "inclination_deg": 72.0},
                "numerics": {"route_a": {"column_workers": leaf}, "uv_tail": {"eps_certificate": eps, "lo_certificate": lo}}}
    def fill(name, th, is_member=False):
        key = M.theta_key(th)
        eps = put(name + "/EPS.json", {"point": {"key": key}})
        gq = put(name + "/GQ.json", {"point": {"key": key}})
        hand = {"schema": "UNT_STEP5_ADMITTED_POINT_HANDOFF_CX3V001" if is_member else "UNT_STEP5_PHASE1_POINT_HANDOFF_C2V001",
                "mode": "SYNTHETIC_DRY_ONLY", "driver_branch": "cx3r008",
                "certificate_pins": {"eps_certificate": eps, "lo_certificate": lo}, "policy_pin": policy}
        if is_member:
            hand.update({"log_index": 1, "source_export_pin": export})
        else:
            hand.update({"point_key": key, "source_pin": fdplan})
        hp = put(name + "/HANDOFF.json", hand)
        sp = put(name + "/fill/" + M.SERIAL_FILE, spec_for(th, key, eps))
        put(name + "/fill/" + M.TWIN_FILE, spec_for(th, key, eps, 8))
        put(name + "/fill/" + M.FILL_FILE, {"schema": "UNT_STEP5_FILLED_SPECS_C2V001", "launch_authorized": False,
                                         "handoff_pin": hp, "theta_key": key, "pending_certificates": []})
        lines.extend(["HANDOFF_PIN %s %s %s" % (name, hp["sha256"], hp["path"]),
                      "SPEC_PIN %s %s %s" % (name, sp["sha256"], sp["path"])])
        return {"handoff": hp, "fill_dir": str(root / name / "fill"), "eps": eps, "gq": gq}
    member_cfg = dict(fill("P1_M0001", engine, True), log_index=1, role="primary_anchor", order=0, member_id="M000")
    f_cfg = [dict(fill("P1_F%d" % k, fs[k]["theta_natural"]), label="F%d" % k) for k in range(3)]
    seed_eps = put("SEED_EPS.json", {"point": {"key": M.SEED_KEY}})
    seed_spec = put("SEED_SPEC.json", spec_for(theta(6), M.SEED_KEY, seed_eps))
    twin_spec = put("TWIN_SPEC.json", spec_for(theta(6), M.SEED_KEY, seed_eps, 8))
    for name, sp in (("S0_SEED_SERIAL", seed_spec), (M.TWIN, twin_spec)):
        put("kit_root/registry/" + name + "_C2V003A.json",
            {"schema": "UNT_S0_LAUNCH_REGISTRY_ENTRY_C2V003A", "name": name, "theta_key": M.SEED_KEY,
             "spec": sp, "v006_spec_pin": sp})
        lines.append("SPEC_PIN %s %s %s" % (name, sp["sha256"], sp["path"]))
    put("kit_root/launches/S0_SEED_SERIAL_LAUNCH_C2V003A_A1.json",
        {"schema": "UNT_S0_LAUNCH_RECORD_C2V003A", "name": "S0_SEED_SERIAL", "attempt": 1, "outcome": "LAUNCH",
         "solo_mode": False})
    stamp = M.date_u()
    epoch = int(M.dt.datetime.strptime(stamp, "%a %b %d %H:%M:%S UTC %Y").replace(tzinfo=M.dt.timezone.utc).timestamp())
    put("kit_root/M15_PRELAUNCH_RECORD_C2V001.json",
        {"schema": "UNT_M15_PRELAUNCH_RECORD_C2V001", "date_u": stamp, "date_u_epoch_s": epoch})
    if duplicate_f0:
        lines = [line for line in lines if not line.startswith(("HANDOFF_PIN P1_F0 ", "SPEC_PIN P1_F0 "))]
    v006 = raw("V006.md", ("\n".join(lines) + "\n").encode())
    cfg = {"schema": "P112_CONFIG_CX2V001", "python": M.PY, "v006": v006["path"], "v006_copy_dir": str(root / "copies"),
           "run_volume": str(root / "volume"), "run_root": str(root / "volume" / "NGC_RUNS"),
           "p112_launch_root": str(root / "launch_root"),
           "s0": {"launch_root": str(root / "kit_root"), "run_root": str(root / "kit_volume" / "NGC_RUNS")},
           "host_ram_bytes_expected": M.RAM, "plan_output_primary": plan, "plan_build_record": build,
           "selection": selection, "fdplan": fdplan, "spec_of_record": spec_of_record, "at0a_pass": at0,
           "members": [member_cfg], "f_points": f_cfg}
    config_pin = put("CONFIG.json", cfg)
    overrides = {"driver": driver, "monitor": monitor, "dry_harness": dry, "lo": lo, "policy": policy,
                 "spec_of_record": spec_of_record}
    syn = put("SYNTHETIC_PINS.json", {"schema": "P112_SYNTHETIC_PINS_CX2V001", "pins": overrides, "date_u": M.date_u(),
        "system": {"mount_points": [cfg["run_volume"], str(root / "kit_volume")], "free_bytes": 1 << 50, "host_ram_bytes": M.RAM}})
    return types.SimpleNamespace(root=root, config=config_pin, config_doc=cfg, synthetic=syn,
                                 overrides=overrides, watch=watch, name="P1_M0001")


"""Public CLI integration using synthetic tools, a passive fixture watch and ps."""


def live_launch_cases(suite):
    import json
    import os
    import subprocess
    import time
    from pathlib import Path
    M, case = suite.module, suite.case
    f = full_launch_fixture(suite, "LIVE_SYNTHETIC_LAUNCH")
    # Refuse before any child start if a fixture escaped the dedicated test tree.
    for key in ("driver", "monitor", "dry_harness"):
        suite.eq(f.overrides[key]["path"].startswith(str(suite.root) + "/"), True)
        suite.eq(f.overrides[key]["sha256"] != M.REAL[key]["sha256"], True)
    M.synthetic_fence(f.overrides, f.config_doc)
    system = M.SyntheticSystem(M.read_pin(f.synthetic)["system"])
    ctx = M.Context(f.config, system=system, synthetic_pins=f.overrides)
    ctx.synthetic_pin = f.synthetic
    case("T01_full_file_backed_context", lambda: suite.eq(
        [c["name"] for c in ctx.calls()], ["P1_M0001", "P1_F0", "P1_F1", "P1_F2", M.TWIN]))
    watch = subprocess.Popen([M.PY, "-I", "-B", f.watch["path"]], env=M.child_env(),
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    base = [M.PY, "-I", "-B", str(suite.tool_path)]
    common = ["--config", f.config["path"], "--config-sha256", f.config["sha256"],
              "--synthetic-pins", f.synthetic["path"], "--synthetic-pins-sha256", f.synthetic["sha256"]]
    def invoke(command, *extra):
        p = subprocess.run(base + [command] + common + list(extra), env=M.child_env(),
                           capture_output=True, text=True, timeout=35)
        suite.eq(p.returncode, 0)
        result = json.loads(p.stdout.strip().splitlines()[-1])
        suite.eq("P112_PRIVATE_SENTINEL_MUST_NOT_BE_READ" in p.stdout + p.stderr, False)
        return result
    launch_result = {}
    try:
        time.sleep(0.15)
        def do_launch():
            launch_result.update(invoke("launch", "--name", f.name, "--attempt", "1"))
            rec = M.read_pin(launch_result)
            suite.eq(rec["outcome"], "LAUNCH")
            suite.eq(rec["status_map_sha256"], M.STATUS_MAP_SHA)
        case("P09_public_launch_synthetic", do_launch)
        if not launch_result:
            return
        outdir = str(Path(f.config_doc["run_root"]) / "NGC_P1_P1_M0001_RUN_CX2V001_A1")
        sample_path = Path(outdir + ".solo.json")
        until = time.monotonic() + 25
        while not sample_path.is_file() and time.monotonic() < until:
            time.sleep(0.1)
        def sample_check():
            suite.eq(sample_path.is_file(), True)
            sample = M.read_pin(M.pin_of(sample_path))
            receipt = M.monitor_receipt(Path(outdir + ".receipt.json").read_bytes())
            suite.eq(sample["complete"], True)
            suite.eq(M.sample_value(sample, receipt), 0)
            suite.eq(M.timestamp(sample["first_utc"]) + 1 <= M.timestamp(receipt["utc_start"]) + 1, True)
            suite.eq(M.timestamp(sample["last_utc"]) > M.timestamp(receipt["utc_end"]), True)
        case("P09_live_sampler_lead_tail_zero", sample_check)
        # A small process-exit window remains after writing the sample.
        time.sleep(0.2)
        def do_close():
            result = invoke("close-attempt", "--name", f.name, "--attempt", "1")
            receipt = M.read_pin(result["receipt"])
            suite.eq(receipt["status_class"], "FINISHED")
            suite.eq(receipt["other_ngc_processes_max"], 0)
            suite.eq(receipt["pins"]["result"]["path"], outdir + "/result.json")
        case("C01_P09_public_close_synthetic", do_close)
        case("L04_public_status_without_writes", lambda: suite.eq(
            invoke("status")["schema"], "P112_STATUS_CX2V001"))
    finally:
        # Only the Popen handle of our inert fixture watch is stopped.
        watch.terminate()
        try:
            watch.wait(timeout=3)
        except subprocess.TimeoutExpired:
            watch.kill()
            watch.wait(timeout=3)
    suite.interfaces["live_synthetic_scope"] = (
        "TESTED public CLI with synthetic driver/dry/watch and verified monitor API wrapper. "
        "Production driver, certificates, mounted volumes and scientific behavior remain UNTESTED.")


"""Saved interrupted-launch states; no scientific process is started."""


def resume_fixture(suite, label, *, bad_caps=False, invocation_alive=False, reused_pid=False, invocation_changes=None):
    import os
    from pathlib import Path
    M = suite.module
    f = receipt_fixture(suite, label, record=False)
    work = f.root / "launch_root" / "work" / (f.name + "_A1_SYNTHETIC_900004")
    work.mkdir()
    m15 = {"schema": "UNT_M15_PRELAUNCH_RECORD_C2V001", "date_u": M.date_u(),
           "date_u_epoch_s": int(M.timestamp(f.rec["utc_start"])) - 1}
    m15_pin = suite.raw_write(work / "m15_fixture.json", M.encoded(m15))
    caps = M.first_caps(f.name)
    if bad_caps:
        caps["wall_cap_s"] += 1
    plan = {
        "schema": "UNT_P112_LAUNCH_PLAN_CX2V001", "name": f.name, "attempt": 1,
        "outdir": f.outdir, "receipt": f.outdir + ".receipt.json", "launch_json": f.outdir + ".receipt.json.launch.json",
        "spec": f.call["spec"], "pins": {"driver": f.ctx.pins["driver"], "monitor": f.ctx.pins["monitor"]},
        "caps": caps, "caps_basis": {"rule": "synthetic saved interruption"},
        "m15_record": m15_pin, "host_ram_bytes": M.RAM, "solo_mode": False, "counted_rerun": False,
        "rule_c_basis": [], "config": f.ctx.config_pin, "work": str(work), "invocation_utc": M.utc(), "date_u": M.date_u()}
    plan["monitor_argv"] = M.monitor_command(f.ctx.pins, f.call["spec"], f.outdir, caps)
    plan_pin = suite.raw_write(work / "plan.json", M.encoded(plan))
    old_command = M.PY + " -I -B " + str(suite.tool_path) + " launch --name " + f.name
    inv = {"invocation_pid": 900004, "invocation_command": old_command, "sampler_pid": 900002,
           "planned_monitor_argv": plan["monitor_argv"], "plan": plan_pin, "date_u": M.date_u()}
    if invocation_changes is not None:
        inv.update(invocation_changes)
    suite.raw_write(work / "invocation.json", M.encoded(inv))
    suite.raw_write(work / "monitor_pid.json", M.encoded({"monitor_pid": 900001, "plan": plan_pin, "date_u": M.date_u()}))
    if invocation_alive or reused_pid:
        f.ctx.system.rows = [{"pid": 900004, "ppid": 1, "pgid": 900004,
                             "command": "/bin/sleep 60" if reused_pid else old_command}]
    f.work, f.plan, f.plan_pin = work, plan, plan_pin
    return f


def resume_cases(suite):
    from pathlib import Path
    M, case, fail = suite.module, suite.case, suite.refuses
    f = resume_fixture(suite, "N20_resume_receipt_present")
    case("N20_resume_finished_monitor", lambda: suite.eq(
        M.read_pin(M.launch_resume(f.ctx, f.name, 1))["outcome"], "LAUNCH"))
    case("N20_resume_then_close", lambda: suite.eq(M.close_attempt(f.ctx, f.name, 1)["status_class"], "FINISHED"))
    f = resume_fixture(suite, "N20_resume_live_monitor")
    f.ctx.system.rows = [{"pid": 900001, "ppid": 1, "pgid": 900001, "command":
                         M.PY + " -I -B " + f.ctx.pins["monitor"]["path"] + " --receipt " + f.outdir + ".receipt.json"}]
    case("N20_resume_monitor_still_running", lambda: suite.eq(
        M.read_pin(M.launch_resume(f.ctx, f.name, 1))["outcome"], "LAUNCH"))
    f = resume_fixture(suite, "N20_resume_original_alive", invocation_alive=True)
    case("N20_live_invocation_blocks_resume", lambda: fail("RESUME_INVOCATION_ALIVE",
                                                         lambda: M.launch_resume(f.ctx, f.name, 1)))
    f = resume_fixture(suite, "N20_resume_reused_invocation_pid", reused_pid=True)
    case("N20_reused_invocation_pid_passes", lambda: suite.eq(
        M.read_pin(M.launch_resume(f.ctx, f.name, 1))["outcome"], "LAUNCH"))
    f = resume_fixture(suite, "N20_resume_mismatched_launch", bad_caps=True)
    case("N20_bad_launch_becomes_mislaunch", lambda: suite.eq(
        M.read_pin(M.launch_resume(f.ctx, f.name, 1))["outcome"], "MISLAUNCH"))
    f = resume_fixture(suite, "N20_no_gate")
    f.ctx.v006_text = "## A999: no gate\n"
    case("L06_resume_gated", lambda: fail("TOOL_PIN_MISSING", lambda: M.launch_resume(f.ctx, f.name, 1)))
    f = resume_fixture(suite, "N19_resume_unmounted")
    f.ctx.system.fixture["mount_points"] = []
    case("N19_resume_volume_first", lambda: fail("RUN_VOLUME_NOT_MOUNTED", lambda: M.launch_resume(f.ctx, f.name, 1)))
    suite.interfaces["resume_fixture_scope"] = (
        "TESTED saved interrupted states with real-format monitor records: completed/live monitor, "
        "live/reused invocation pid, mismatch, gate and mount. No actual scientific interruption was induced.")


"""Qualified stop tests against only inert processes created by this suite."""


def stop_cases(suite):
    import json
    import os
    import subprocess
    import time
    from pathlib import Path
    M, case, fail = suite.module, suite.case, suite.refuses
    class FastSystem(M.SyntheticSystem):
        def __init__(self, f):
            super().__init__({"mount_points": [f.ctx.cfg["run_volume"], str(Path(f.ctx.cfg["s0"]["run_root"]).parent)],
                              "free_bytes": 1 << 50, "host_ram_bytes": M.RAM})
            self.clock = 0.0
        def monotonic(self):
            return self.clock
        def sleep(self, seconds):
            self.clock += max(seconds, 20)
            time.sleep(0.05)
    def terminate_handle(p):
        if p is None:
            return
        if p.poll() is None:
            p.terminate()
            try:
                p.wait(timeout=3)
            except subprocess.TimeoutExpired:
                p.kill()
                p.wait(timeout=3)
        else:
            p.wait()
    for variant in ("launch_on_term", "started_without_launch", "refused_no_outputs", "truncated_orphan"):
        f = receipt_fixture(suite, "N18_" + variant, mode="FAILED")
        M.close_attempt(f.ctx, f.name, 1)
        f.ctx.system = FastSystem(f)
        work = f.root / "launch_root" / "work" / ("stop_" + variant)
        work.mkdir()
        outdir = M.planned_outdir(f.ctx, f.name, 2, "P112")
        driver = suite.raw_write(work / "inert_wait_driver.py", b"import time\ntime.sleep(120)\n")
        f.ctx.pins = dict(f.ctx.pins, driver=driver)
        plan = {"schema": "UNT_P112_LAUNCH_PLAN_CX2V001", "name": f.name, "attempt": 2, "outdir": outdir,
                "receipt": outdir + ".receipt.json", "launch_json": outdir + ".receipt.json.launch.json",
                "spec": f.call["spec"], "caps": dict(M.first_caps(f.name), wall_cap_s=1220648),
                "caps_basis": {"rule": "synthetic N18"}, "host_ram_bytes": M.RAM, "solo_mode": True,
                "counted_rerun": True, "rule_c_basis": [], "m15_record": f.entry_pin,
                "config": f.ctx.config_pin, "work": str(work), "date_u": M.date_u()}
        child, mon = None, None
        try:
            if variant in ("launch_on_term", "truncated_orphan"):
                child = subprocess.Popen(M.driver_command(f.ctx.pins, plan["spec"], outdir), env=M.child_env(),
                                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
            lj = {"schema": M.MONITOR_SCHEMA + "_LAUNCH", "utc": f.rec["utc_start"], "child_pid": child.pid if child else 900099,
                  "command": M.driver_command(f.ctx.pins, plan["spec"], outdir),
                  "pins": {"driver": driver, "spec": plan["spec"]}, "caps": plan["caps"], "retries_allowed": 0}
            code = "import json,signal,time\nfrom pathlib import Path\n"
            if variant == "launch_on_term":
                code += ("def stop(sig,frame):\n"
                         " with Path(%r).open('x') as f:json.dump(%r,f)\n"
                         " raise SystemExit(0)\n"
                         "signal.signal(signal.SIGTERM,stop)\n") % (plan["launch_json"], lj)
            elif variant == "started_without_launch":
                code += "with Path(%r).open('x') as f:f.write('FORBIDDEN_RECEIPT_STDOUT')\n" % (plan["receipt"] + ".stdout.txt")
            code += "time.sleep(120)\n"
            mp = suite.raw_write(work / "inert_wait_monitor.py", code.encode())
            f.ctx.pins = dict(f.ctx.pins, monitor=mp)
            plan["pins"] = {"driver": driver, "monitor": mp}
            plan["monitor_argv"] = M.monitor_command(f.ctx.pins, plan["spec"], outdir, plan["caps"])
            plan_pin = suite.raw_write(work / "plan.json", M.encoded(plan))
            suite.raw_write(work / "monitor.stdout.txt", b"SYNTHETIC_MONITOR_LOG\n")
            suite.raw_write(work / "monitor.stderr.txt", b"")
            if variant == "truncated_orphan":
                suite.raw_write(Path(plan["launch_json"]), b'{"truncated":')
                mon_pid = 900099
            else:
                mon = subprocess.Popen(plan["monitor_argv"], env=M.child_env(), stdout=subprocess.DEVNULL,
                                       stderr=subprocess.DEVNULL, start_new_session=True)
                mon_pid = mon.pid
            time.sleep(0.2)
            before = list((f.root / "launch_root" / "launches").iterdir())
            result, checked_raw, checked_lj = M.stop_launch_failure(f.ctx, plan, mon_pid, None, None)
            case("N18_" + variant + "_monitor_stopped_before_record", lambda mon=mon:
                 suite.eq(mon is None or mon.poll() is not None, True))
            if variant in ("launch_on_term", "truncated_orphan"):
                case("N18_" + variant + "_driver_stopped", lambda child=child: suite.eq(child.poll() is not None, True))
                case("N18_" + variant + "_no_mon_pid_after_stop", lambda result=result:
                     suite.eq(result["mon_pid_supplied"], None))
                def record_mislaunch(f=f, plan=plan, plan_pin=plan_pin, mon_pid=mon_pid, result=result):
                    pin = M.write_launch_record(f.ctx, plan, plan_pin, f.entry_pin, mon_pid, 900002, None,
                                                {"launch_json_parseable": False}, result, snapshot=(checked_raw, checked_lj))
                    suite.eq(M.read_pin(pin)["outcome"], "MISLAUNCH")
                    suite.eq(M.status(f.ctx)["calls"][0]["status"], "MONITOR_ENDED_NO_RECEIPT")
                case("N18_" + variant + "_mislaunch_residual", record_mislaunch)
            elif variant == "started_without_launch":
                case("N18_started_is_not_refusal", lambda f=f, plan_pin=plan_pin, work=work:
                     fail("MONITOR_STARTED_NO_LAUNCH_JSON", lambda: M.record_monitor_refused(f.ctx, plan_pin, str(work))))
                case("N18_started_no_record_written", lambda f=f, before=before:
                     suite.eq(list((f.root / "launch_root" / "launches").iterdir()), before))
            else:
                case("N18_clean_refusal_recorded", lambda f=f, plan_pin=plan_pin, work=work:
                     suite.eq(M.read_pin(M.record_monitor_refused(f.ctx, plan_pin, str(work)))["schema"],
                              "MONITOR_REFUSED_ATTEMPT_RECORD_C2V001"))
        finally:
            terminate_handle(mon)
            terminate_handle(child)
    f = receipt_fixture(suite, "N18_unrelated_pid")
    f.ctx.system = FastSystem(f)
    unrelated = subprocess.Popen(["/bin/sleep", "120"], start_new_session=True)
    try:
        outdir = M.planned_outdir(f.ctx, f.name, 2, "P112")
        plan = {"name": f.name, "outdir": outdir, "receipt": outdir + ".receipt.json",
                "launch_json": outdir + ".receipt.json.launch.json", "spec": f.call["spec"]}
        case("N18_unrelated_pid_not_signalled", lambda: (
            suite.eq(M.stop_launch_failure(f.ctx, plan, unrelated.pid, None, None), (None, None, None)),
            suite.eq(unrelated.poll(), None)))
    finally:
        terminate_handle(unrelated)
    suite.interfaces["qualified_stop_scope"] = (
        "TESTED real ps and TERM against suite-created inert monitor/driver groups. "
        "Injected clock advances the 15/60-second bounds; real elapsed timeout duration is not asserted.")


"""Outside-set stop, exclusion and c2v006 receipt-residence interface tests."""


def outside_interface_cases(suite):
    import json
    import os
    import subprocess
    import time
    from pathlib import Path
    M, case, fail = suite.module, suite.case, suite.refuses
    f = receipt_fixture(suite, "O01_in_actual_set", origin="KIT", name="S0_J0_SERIAL")
    case("O01_in_set_refuses", lambda: fail("OUTSIDE_STOP_IN_ACTUAL_SET", lambda: M.stop_outside_set(f.ctx, f.name)))
    for mismatch in (True, False):
        label = "O02_wrong_command" if mismatch else "O03_inert_target"
        f = receipt_fixture(suite, label, origin="KIT", name="S0_J0_SERIAL")
        f.ctx._fixture_calls = []
        f.ctx.system = M.SyntheticSystem({"mount_points": [f.ctx.cfg["run_volume"], str(Path(f.ctx.cfg["s0"]["run_root"]).parent)],
                                         "free_bytes": 1 << 50, "host_ram_bytes": M.RAM})
        driver = suite.raw_write(f.root / "inert_outside_driver.py", b"import time\ntime.sleep(120)\n")
        f.ctx.pins = dict(f.ctx.pins, driver=driver)
        outdir = M.planned_outdir(f.ctx, f.name, 2, "KIT")
        command = M.driver_command(f.ctx.pins, f.call["spec"], outdir)
        proc = subprocess.Popen(["/bin/sleep", "120"] if mismatch else command, env=M.child_env(),
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        try:
            time.sleep(0.1)
            lj = {"schema": M.MONITOR_SCHEMA + "_LAUNCH", "command": command, "child_pid": proc.pid,
                  "pins": {"driver": driver, "spec": f.call["spec"]}, "caps": M.first_caps(f.name),
                  "utc": f.rec["utc_start"], "retries_allowed": 0}
            lp = suite.raw_write(Path(outdir + ".receipt.json.launch.json"), M.encoded(lj))
            rec = dict(f.record, attempt=2, outdir=outdir, receipt=outdir + ".receipt.json",
                       launch_json=dict(lp, child_pid=proc.pid, utc=lj["utc"]), monitor_pid=os.getpid(), driver=driver)
            rp = Path(f.ctx.cfg["s0"]["launch_root"]) / "launches" / (f.name + "_LAUNCH_C2V003A_A2.json")
            suite.raw_write(rp, M.encoded(rec))
            if mismatch:
                case("O02_wrong_command_refuses", lambda: fail("OUTSIDE_STOP_TARGET_REFUSED",
                                                               lambda: M.stop_outside_set(f.ctx, f.name)))
                case("O02_unrelated_process_untouched", lambda: suite.eq(proc.poll(), None))
            else:
                def stopped():
                    result = M.read_pin(M.stop_outside_set(f.ctx, f.name))
                    suite.eq(result["schema"], "S0_OUTSIDE_SET_STOP_RECORD_C2V001")
                    suite.eq(result["result"] in ("KILLED_TERM", "KILLED_KILL"), True)
                    suite.eq(proc.poll() is not None, True)
                case("O03_inert_outside_target_stopped", stopped)
                def excluded():
                    raw, evidence = M.registry_bytes(f.ctx)
                    suite.eq(json.loads(raw)["calls"], [])
                    suite.eq(evidence["excluded_serials"][0]["name"], f.name)
                    suite.eq(len(evidence["excluded_serials"][0]["stop_records"]), 1)
                case("R04_outside_serial_excluded_and_listed", excluded)
        finally:
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait(timeout=3)
            else:
                proc.wait()
    f = receipt_fixture(suite, "R02_receipt_residence")
    result = M.close_attempt(f.ctx, f.name, 1)
    receipt = M.read_pin(result["receipt"])
    inside = suite.raw_write(Path(f.outdir) / "attempt_receipt_inside_synthetic.json", M.encoded(receipt))
    B = M.load_verified(M.REAL["builder"], "_p112_residence_proof_builder")
    cfg = B._receipt_cfg(M.RECEIPT_KEYS, M.STATUS_CLASSES)
    case("R02_inside_fixture_all_nine_roles", lambda: (
        suite.eq(B._receipt(inside, cfg, "synthetic inside")[1], "FINISHED|COMPLETED"),
        suite.eq(B._receipt(inside, cfg, "synthetic inside")[4]["rss_cap_bytes"], M.RAM),
        suite.eq(B._receipt(inside, cfg, "synthetic inside")[5]["theta_sha256"], receipt["theta_sha256"])))
    def outside_rejected():
        try:
            B._terminal([{"run_dir": f.outdir, "receipt": result["receipt"]}], cfg, "true sibling residence", False,
                        {"theta_sha256": receipt["theta_sha256"], "spec_sha256": receipt["spec_sha256"]})
        except B.Refused as e:
            suite.eq(e.code, "RECEIPT_NOT_IN_RUN_DIR")
            return
        raise AssertionError("c2v006 unexpectedly admitted sibling receipt")
    case("R02_true_sibling_requires_c2v007", outside_rejected)
    suite.interfaces["receipt_residence_demonstrated"] = (
        "TESTED c2v006 _receipt on an inside synthetic copy and _terminal rejecting the true sibling "
        "with RECEIPT_NOT_IN_RUN_DIR. No full assembly, v003g or slots access.")


"""File-backed F de-duplication, in-flight windows, and validation boundaries."""


def boundary_cases(suite):
    import copy
    from pathlib import Path
    M, case, fail = suite.module, suite.case, suite.refuses
    f = full_launch_fixture(suite, "F_DUPLICATE_MEMBER", duplicate_f0=True)
    def context():
        return M.Context(f.config, system=M.SyntheticSystem(M.read_pin(f.synthetic)["system"]), synthetic_pins=f.overrides)
    ctx = context()
    def duplicate_check():
        calls = ctx.calls()
        suite.eq([c["name"] for c in calls], ["P1_M0001", "P1_F1", "P1_F2", M.TWIN])
        suite.eq(calls[0]["serves"], ["F0"])
        suite.eq("P1_F0" in ctx.vpins["SPEC_PIN"], False)
    case("T01_F_duplicate_reuses_member_without_F_launch_pins", duplicate_check)
    for label, solo, same, expected in (
        ("solo_invocation", True, False, "SOLO_RERUN_ACTIVE"),
        ("same_outdir", False, True, "INVOCATION_ALREADY_ACTIVE"),
        ("reused_pid", True, False, None),
        ("monitor_before_record", True, False, "SOLO_RERUN_ACTIVE")):
        f2 = receipt_fixture(suite, "P05_inflight_" + label)
        work = f2.root / "launch_root" / "work" / "inflight"
        work.mkdir()
        outdir = M.planned_outdir(f2.ctx, f2.name, 2, "P112")
        command = M.PY + " -I -B /synthetic/p112.py launch --name P1_M0001"
        plan = {"schema": "UNT_P112_LAUNCH_PLAN_CX2V001", "name": f2.name, "outdir": outdir,
                "solo_mode": solo, "invocation_pid": 900019, "invocation_command": command,
                "pins": {"monitor": M.REAL["monitor"]}}
        suite.raw_write(work / "plan.json", M.encoded(plan))
        if label == "monitor_before_record":
            command = M.PY + " -I -B " + M.REAL["monitor"]["path"] + " --receipt " + outdir + ".receipt.json"
        elif label == "reused_pid":
            command = "/bin/sleep 120"
        f2.ctx.system.rows = [{"pid":900019,"ppid":1,"pgid":900019,"command":command}]
        action = lambda f2=f2, same=same, outdir=outdir: M.enforce_solo(f2.ctx, False, requested_outdir=outdir if same else None)
        case("P05_inflight_" + label, (lambda expected=expected, action=action: fail(expected, action)) if expected else action)
    call = ctx.calls()[0]
    cfg = ctx.cfg["members"][0]
    handoff = M.read_pin(cfg["handoff"])
    spec, sp, fill, fc, certs = ctx.read_fill(cfg)
    args = [handoff, cfg["handoff"], *fill, call["point_key"], cfg["eps"], ctx.pins["lo"],
            "UNT_STEP5_ADMITTED_POINT_HANDOFF_CX3V001", True]
    mutations = [
        (0, "schema", "WRONG", "HANDOFF_SCHEMA"),
        (0, "mode", "ADMITTED", "HANDOFF_MODE"),
        (0, "driver_branch", "WRONG", "HANDOFF_DRIVER_BRANCH"),
        (0, "certificate_pins", {}, "HANDOFF_CERTIFICATES"),
        (4, "schema", "WRONG", "FILL_SCHEMA"),
        (4, "launch_authorized", True, "FILL_LAUNCH_AUTHORIZED"),
        (4, "handoff_pin", {}, "FILL_HANDOFF_PIN"),
        (4, "theta_key", "f" * 64, "FILL_POINT_KEY"),
        (4, "pending_certificates", ["eps"], "FILL_PENDING_CERTIFICATES")]
    for index, key, value, code in mutations:
        changed = copy.deepcopy(args)
        changed[index][key] = value
        case("V_fill_" + code, lambda changed=changed, code=code: fail(code, lambda: M.fill_check(*changed)))
    log = {"exit":0,"blocked":[],"ctx_modes":["simulate"],"driver_sha256":ctx.pins["driver"]["sha256"],
           "spec_sha256":sp["sha256"]}
    readiness = {"executed_stages":0,"binding_blockers":[],"source_build_blockers":[],
                 "future_stage_dependencies":[{"class":"PENDING_ROUTE_A_OUTPUTS"}],"planned_route_a":True}
    for side, key, value in (("log","exit",1),("log","blocked",["bad"]),("log","ctx_modes",["real"]),
                            ("log","driver_sha256","f"*64),("log","spec_sha256","f"*64),
                            ("readiness","executed_stages",1),("readiness","binding_blockers",["x"]),
                            ("readiness","source_build_blockers",["x"]),
                            ("readiness","future_stage_dependencies",[{"class":"BAD"}]),
                            ("readiness","planned_route_a",False)):
        docs = {"log":copy.deepcopy(log),"readiness":copy.deepcopy(readiness)}
        docs[side][key] = value
        case("V_dry_" + key, lambda docs=docs: fail("DRY_VERDICT_REFUSED", lambda: M.dry_verdict(
            docs["log"], docs["readiness"], sp, ctx.pins["driver"])))

    for directory, filename, code in (("ordinary", "result.json", "FORBIDDEN_RESULT_READ"),
                                      ("A_SIDE", "source.py", "FORBIDDEN_READ_PATH"),
                                      ("ordinary", "freeze_manifest.json", "FORBIDDEN_SEALED_READ")):
        target = suite.root / ("guard_" + filename) / directory / filename
        target.parent.mkdir(parents=True)
        suite.raw_write(target, b"SYNTHETIC_FORBIDDEN_READ_SENTINEL")
        alias = target.parent.parent / "alias.py"
        alias.symlink_to(target)
        case("V03_guard_symlink_" + filename, lambda alias=alias, code=code: fail(code, lambda: M.pin_of(alias)))
    counter = M.ProcessCounter(declared=[], synthetic=True)
    case("V04_process_counter_never_resolves_Volumes", lambda: suite.eq(counter.identify("/Volumes/SYNTHETIC_NOT_TOUCHED/alias.py"), None))

    f2 = receipt_fixture(suite, "N04_old_sampler_exit_window")
    work = f2.root / "launch_root" / "work" / "old_sampler"
    work.mkdir()
    outdir = M.planned_outdir(f2.ctx, f2.name, 2, "P112")
    suite.raw_write(work / "plan.json", M.encoded({"schema":"UNT_P112_LAUNCH_PLAN_CX2V001",
                    "name":f2.name,"outdir":outdir,"solo_mode":False,"work":str(work)}))
    suite.raw_write(work / "sampler_first_sample.json", M.encoded({"sampler_pid":900031,"ok":True}))
    f2.ctx.system.rows = [{"pid":900031,"ppid":1,"pgid":900031,"command":
                          M.PY+" -I -B "+f2.ctx.own_pin["path"]+" _sampler --outdir "+outdir}]
    case("N04_old_sampler_blocks_same_outdir",lambda:fail("INVOCATION_ALREADY_ACTIVE",
         lambda:M.enforce_solo(f2.ctx,False,requested_outdir=outdir)))
    case("N04_current_sampler_admitted_at_second_check",lambda:M.enforce_solo(
        f2.ctx,False,requested_outdir=outdir,own_work=str(work)))
    f2.ctx.system.rows[0]["command"] = "/bin/sleep 120"
    case("N04_reused_sampler_pid_does_not_block",lambda:M.enforce_solo(f2.ctx,False,requested_outdir=outdir))


"""Targeted counterfactual source mutations; each probe first passes unchanged."""


def mutation_cases(suite):
    import copy
    import types
    from pathlib import Path
    original = suite.tool_path.read_text()
    mutation_rows = []
    serial = [0]

    def child(label, module):
        serial[0] += 1
        s = object.__new__(type(suite))
        s.__dict__ = dict(suite.__dict__)
        s.module = module
        s.root = suite.root / ("mutation_%03d_%s" % (serial[0], label))
        s.root.mkdir()
        s.rows, s.interfaces = [], {}
        return s

    def core_probe(target):
        def probe(s):
            seen = []
            def case(name, action):
                if name == target:
                    seen.append(name)
                    action()
            s.case = case
            core_cases(s)
            s.eq(seen, [target])
        return probe

    def replace_in(source, function, old, new):
        if function is None:
            start, end = 0, len(source)
        else:
            start = source.index("\ndef " + function + "(") + 1
            end = source.find("\ndef ", start + 1)
            end = len(source) if end < 0 else end
        section = source[start:end]
        if section.count(old) != 1:
            raise AssertionError(("mutation site not unique", function, old, section.count(old)))
        return source[:start] + section.replace(old, new, 1) + source[end:]

    def trial(name, function, old, new, probe, import_failure=False):
        def action():
            probe(child(name + "_control", suite.module))
            source = replace_in(original, function, old, new)
            module = types.ModuleType("_p112_mutant_" + name)
            module.__file__ = str(suite.tool_path)
            imported = False
            failure = None
            try:
                exec(compile(source, str(suite.tool_path), "exec"), module.__dict__)
                imported = True
                probe(child(name + "_mutant", module))
            except Exception as error:
                failure = type(error).__name__
            suite.eq(failure is not None, True)
            suite.eq(imported or import_failure, True)
            mutation_rows.append({"name": name, "status": "KILLED", "control": "PASS",
                                  "source_sha256": suite.module.sha(source.encode()),
                                  "function": function, "replace": old, "with": new,
                                  "detection": failure, "imported": imported})
        suite.case("MUTANT_" + name, action)

    trial("wildcard_status", None, "assert len(STATUS_CLASSES) == 54",
          'STATUS_CLASSES["*"] = "INFRA"\nassert len(STATUS_CLASSES) == 54',
          core_probe("S01_literal_status_map"), True)
    trial("swapped_precedence", "raw_status", "if mislaunch is not None:",
          'if mislaunch is not None and not str(rec.get("status", "")).startswith("STOPPED_"):',
          core_probe("S03_mislaunch_precedence"))
    trial("unbound_mislaunch", "raw_status", 'need(bound, "MISLAUNCH_NOT_BOUND")',
          "pass", core_probe("S04_mislaunch_attempt"))
    trial("ignored_sample_gap", "sample_value", "if gap > 2 * p:", "if False:",
          core_probe("P02_gap"))
    trial("undoubled_rerun_wall", "next_attempt", 'caps["wall_cap_s"] = first["wall_cap_s"] * 2',
          'caps["wall_cap_s"] = first["wall_cap_s"]', core_probe("K01_serial_rule_c_caps"))
    trial("twin_rss_at_ram", "next_attempt", 'caps["rss_cap_bytes"] = RAM * (11 if name == TWIN else 1)',
          'caps["rss_cap_bytes"] = RAM', core_probe("K01_twin_rerun"))
    trial("numbering_restarts", "next_attempt", "k = max(ks, default=0) + 1", "k = 1",
          core_probe("N01_kit_numbering"))
    trial("theta_numeric_equality", "equal_hex", "fhex(left, where) == fhex(right, where)",
          "left == right", lambda s: s.refuses("THETA_BITS_MISMATCH", lambda: s.module.equal_hex(-0.0, 0.0, "zero")))

    def disk_probe(s):
        M = s.module
        volume = s.root / "volume"
        volume.mkdir()
        cfg = {"run_volume": str(volume)}
        caps = M.first_caps("P1_M0001")
        caps["output_cap_bytes"] *= 2
        system = M.SyntheticSystem({"mount_points": [str(volume)], "host_ram_bytes": M.RAM,
                                    "free_bytes": caps["output_cap_bytes"] + M.DISK_RESERVE})
        result = M.disk_check(cfg, str(volume / "NGC_SYNTHETIC_RUN"), caps, system)
        s.eq(result["free_bytes"], result["required_bytes"])
    trial("disk_off_by_one", "disk_check", 'free >= caps["output_cap_bytes"] + DISK_RESERVE',
          'free > caps["output_cap_bytes"] + DISK_RESERVE', disk_probe)

    def close_mapping_probe(s):
        M = s.module
        f = receipt_fixture(s, "close_mapping", origin="KIT", name="S0_J0_SERIAL")
        f.ctx.mapping_block = "PLAN_MAPPING_UNAVAILABLE"
        s.refuses("PLAN_MAPPING_UNAVAILABLE", lambda: M.close_attempt(f.ctx, f.name, 1))
        s.eq(Path(f.outdir + ".attempt_receipt.json").exists(), False)
    trial("receipt_before_mapping", "close_attempt", "call = ctx.call(name)",
          'ctx.write(outdir + ".attempt_receipt.json", {"counterfactual_early_write": True})\n    call = ctx.call(name)',
          close_mapping_probe)
    trial("infra_repeat_requires_rule_c", "terminal_prefix",
          'prev.get("solo_mode") is True and caps_of(cur) == caps_of(prev)',
          'prev.get("solo_mode") is True and caps_of(cur) == caps_of(prev) and cur["wall_cap_s"] == 2 * first["wall_cap_s"]',
          core_probe("N07_terminal_CHILD_FAILED|REFUSED"))

    def cutoff_probe(s):
        M = s.module
        f = receipt_fixture(s, "cutoff")
        terms = [{"name": f.name, "time_utc": "2026-10-20T12:00:02Z", "receipt": f.entry_pin},
                 {"name": "P1_F0", "time_utc": "2026-10-20T12:00:01Z", "receipt": f.entry_pin}]
        result = M.read_pin(M.write_cutoff(f.ctx, terms))
        s.eq(result["T"], "2026-10-20T12:00:02Z")
    trial("cutoff_from_completing_receipt", "write_cutoff",
          'latest = max(terms, key=lambda t: timestamp(t["time_utc"], whole=True))["time_utc"]',
          'latest = terms[-1]["time_utc"]', cutoff_probe)

    def gate_probe(s):
        M = s.module
        f = receipt_fixture(s, "close_gate")
        f.ctx.v006_text = "## A999: no tool pin\n"
        s.refuses("TOOL_PIN_MISSING", lambda: M.close_attempt(f.ctx, f.name, 1))
        s.eq(Path(f.outdir + ".attempt_receipt.json").exists(), False)
    trial("gate_on_launch_only", "close_attempt", "ctx.gate()", "pass", gate_probe)
    trial("refused_retry_not_solo", "next_attempt",
          'elif last["raw_status"] in ("CHILD_FAILED|REFUSED", "CHILD_FAILED|BLOCKED"):\n            solo = True',
          'elif last["raw_status"] in ("CHILD_FAILED|REFUSED", "CHILD_FAILED|BLOCKED"):\n            solo = False',
          core_probe("K01_solo_retry_CHILD_FAILED|REFUSED"))
    trial("sample_time_without_floor", "sample_value", 'math.floor(timestamp(sample["last_utc"]))',
          'timestamp(sample["last_utc"])', core_probe("P08_last_same_second"))
    trial("nonattempt_retry_first_caps", "next_attempt", 'caps = dict(trailing_nonattempt["caps"])',
          'caps = first_caps(name)', core_probe("N12_nonattempt_preserves_solo_caps"))
    trial("retry_before_terminal", "next_attempt", 'need(terminal is None, "ATTEMPT_AFTER_TERMINAL", terminal)',
          "pass", core_probe("N07_terminal_no_retry_CHILD_FAILED|REFUSED"))
    trial("nonconsecutive_rule_c_pair", "terminal_prefix", 'for i, cur in enumerate(actual):',
          'actual = [r for r in actual if r["status_class"] != "INFRA"]\n    for i, cur in enumerate(actual):',
          core_probe("N15_infra_separates_rule_c"))

    def missing_receipt_probe(s):
        f = receipt_fixture(s, "missing_receipt", no_receipt=True)
        s.eq(s.module.status(f.ctx)["calls"][0]["status"], "MONITOR_ENDED_NO_RECEIPT")
    trial("ended_monitor_unreported", "history",
          '"ATTEMPT_ACTIVE" if live else "MONITOR_ENDED_NO_RECEIPT"', '"ATTEMPT_ACTIVE"', missing_receipt_probe)

    def sampler_bound_probe(s):
        M = s.module
        f = receipt_fixture(s, "sampler_bound", no_receipt=True)
        work = f.root / "launch_root" / "work" / "bounded"
        work.mkdir()
        plan = {"name": f.name, "attempt": 1, "outdir": f.outdir, "config": f.ctx.config_pin}
        clock = [0.0]
        f.ctx.system.monotonic = lambda: clock[0]
        def sleep(seconds):
            clock[0] += seconds
            if clock[0] > 180:
                raise AssertionError("sampler exceeded injected-clock bound")
        f.ctx.system.sleep = sleep
        s.eq(M.sampler(f.ctx, plan, str(work), poll_s=1)["status"], "MONITOR_ENDED_NO_RECEIPT_NO_SOLO_FILE")
    trial("sampler_waits_forever", "sampler", "if gone_mounted_s >= 60:", "if False:", sampler_bound_probe)

    def residual_probe(s, orphan=False, assembly=False):
        M = s.module
        f = receipt_fixture(s, "residual", no_receipt=orphan)
        f.ctx.v006_text += "RESIDUAL_RETRY %s 1\n" % f.name
        if orphan:
            command = " ".join(M.driver_command(f.ctx.pins, f.call["spec"], f.outdir))
            f.ctx.system.rows = [{"pid": 900011, "ppid": 1, "pgid": 900011, "command": command}]
        s.refuses("RESIDUAL_ATTEMPT_PROCESS_ALIVE" if orphan else "RESIDUAL_RETRY_NOT_RESIDUAL",
                  lambda: M.assemble_registry(f.ctx) if assembly else M.history(f.ctx, f.call))
    trial("residual_with_receipt", "honor_residual",
          'need(not os.path.lexists(paths["receipt"]), "RESIDUAL_RETRY_NOT_RESIDUAL")',
          "pass", residual_probe)
    trial("residual_with_live_driver", "honor_residual",
          'need(not monitors and not any(r["command"] == command for r in rows),\n         "RESIDUAL_ATTEMPT_PROCESS_ALIVE")',
          "pass", lambda s: residual_probe(s, orphan=True))
    trial("residual_number_omitted", "next_attempt",
          'ks = [r["attempt"] for r in records] + [k for n, k in residuals if n == name]',
          'ks = [r["attempt"] for r in records]', core_probe("N16_residual_numbering"))

    def no_outdir_probe(s):
        M = s.module
        f = receipt_fixture(s, "no_outdir", mode="EXIT_BEFORE_MKDIR", outcome="LAUNCH")
        h = M.history(f.ctx, f.call)
        s.eq(h["actual"], [])
        s.eq(M.next_attempt(f.name, h["records"], h["actual"], h["residuals"], h["trailing_nonattempt"])["attempt"], 2)
    trial("nonattempt_launch_is_attempt", "history", "if not is_directory or not spec_match:",
          "if not spec_match:", no_outdir_probe)

    def stopped_monitor_pid_probe(s):
        M = s.module
        f = receipt_fixture(s, "stopped_monitor")
        command = M.PY + " -I -B " + f.ctx.pins["monitor"]["path"] + " --receipt " + f.outdir + ".receipt.json"
        f.ctx.system.rows = [{"pid": 900001, "ppid": 1, "pgid": 900001, "command": command}]
        plan = {"name": f.name, "outdir": f.outdir, "receipt": f.outdir + ".receipt.json",
                "launch_json": f.outdir + ".receipt.json.launch.json", "spec": f.call["spec"]}
        old_stop, old_kill = M.stop_qualified, M.kit_kill_target
        try:
            M.stop_qualified = lambda *args, **kwargs: f.ctx.system.rows.clear()
            M.kit_kill_target = lambda ctx, plan, monitor_pid=None: {"mon_pid_supplied": monitor_pid}
            s.eq(M.stop_launch_failure(f.ctx, plan, 900001, None, None)[0]["mon_pid_supplied"], None)
        finally:
            M.stop_qualified, M.kit_kill_target = old_stop, old_kill
    trial("mon_pid_after_monitor_stopped", "stop_launch_failure",
          'None if monitor_stopped or qualified is None else qualified["pid"]', "monitor_pid",
          stopped_monitor_pid_probe)

    def absent_launch_guard_probe(s):
        M = s.module
        f = receipt_fixture(s, "absent_launch_guard")
        outdir = M.planned_outdir(f.ctx, f.name, 2, "P112")
        plan = dict(f.record, attempt=2, outdir=outdir, receipt=outdir + ".receipt.json",
                    launch_json=outdir + ".receipt.json.launch.json", caps_basis={}, m15_record=f.entry_pin,
                    rule_c_basis=[], config=f.ctx.config_pin)
        before = list((f.root / "launch_root" / "launches").iterdir())
        s.refuses("NO_MISLAUNCH_WITHOUT_LAUNCH_JSON", lambda: M.write_launch_record(
            f.ctx, plan, f.entry_pin, f.entry_pin, 900001, 900002, None, {"parseable":False}, snapshot=(None, None)))
        s.eq(list((f.root / "launch_root" / "launches").iterdir()), before)
    trial("mislaunch_without_launch_json", "write_launch_record",
          'need(outcome == "LAUNCH" or os.path.lexists(plan["launch_json"]), "NO_MISLAUNCH_WITHOUT_LAUNCH_JSON")',
          "pass", absent_launch_guard_probe)

    def unanchored_tool_probe(s):
        M = s.module
        own = {"path": str(s.tool_path), "sha256": s.tool_sha}
        text = "## A999: prose\nThis text includes TOOL_PIN P112_LAUNCHER_CX2V002 %s %s\n" % (s.tool_sha, s.tool_path)
        s.refuses("TOOL_PIN_MISSING", lambda: M.tool_gate(text, own))
    trial("unanchored_tool_pin", "tool_gate", 'for line in text.split("\n"):',
          'for line in text.split("\\n"):\n        line = line[line.find("TOOL_PIN "):] if "TOOL_PIN " in line else line',
          unanchored_tool_probe)
    trial("unanchored_residual", "residual_lines", 'for line in text.split("\n"):',
          'for line in text.split("\\n"):\n        line = line[line.find("RESIDUAL_RETRY "):] if "RESIDUAL_RETRY " in line else line',
          core_probe("L07_residual_midline"))

    def refusal_fixture(s):
        M = s.module
        f = receipt_fixture(s, "refusal_relaunch")
        work = f.root / "launch_root" / "work" / "old_refusal"
        work.mkdir()
        plan = {"outdir": f.outdir, "attempt": 1, "caps": M.first_caps(f.name), "solo_mode":False}
        pin = s.raw_write(work / "plan.json", M.encoded(plan))
        rec = {"schema":"MONITOR_REFUSED_ATTEMPT_RECORD_C2V001", "name":f.name, "attempt":1,
               "launcher":"P112_CX2V001", "writer":{"name":M.TOOL_NAME,"sha256":s.tool_sha},
               "plan":pin,"monitor_stdout":s.raw_write(work / "monitor.stdout.txt",b"synthetic old invocation\n"),
               "monitor_stderr":s.raw_write(work / "monitor.stderr.txt",b""),
               "absent":M.absent_paths(f.outdir),"date_u":M.date_u(),"rule":"synthetic refusal followed by relaunch"}
        s.raw_write(f.root / "launch_root" / "launches" / ("P112_%s_MONITOR_REFUSED_CX2V001_A1.json" % f.name),
                    M.encoded(rec))
        return f

    def relaunched_absence_probe(s):
        M = s.module
        f = refusal_fixture(s)
        s.eq(M.refusal_records(f.ctx, f.name, f.ctx.records(f.name))[0]["reason"], "MONITOR_REFUSED")
    trial("recheck_absence_after_relaunch", "refusal_records", "if not relaunched:", "if True:",
          relaunched_absence_probe)

    def mount_probe(s, refusal=False):
        M = s.module
        f = refusal_fixture(s) if refusal else receipt_fixture(s, "residual_mount", no_receipt=True)
        f.ctx.system.fixture["mount_points"] = []
        if refusal:
            s.refuses("RUN_VOLUME_NOT_MOUNTED", lambda: M.refusal_records(f.ctx, f.name, f.ctx.records(f.name)))
        else:
            f.ctx.v006_text += "RESIDUAL_RETRY %s 1\n" % f.name
            s.refuses("RUN_VOLUME_NOT_MOUNTED", lambda: M.history(f.ctx, f.call, inspect_next=False))
    trial("residual_without_mount", "honor_residual", 'mount_first(ctx.cfg, origin, ctx.system)',
          "pass", mount_probe)
    trial("refusal_without_mount", "refusal_records", 'mount_first(ctx.cfg, origin, ctx.system)',
          "pass", lambda s: mount_probe(s, refusal=True))
    trial("assembly_honors_nonresidual", "history",
          "nonattempt = honor_residual(ctx, call, k, records, residuals, rows)",
          'nonattempt = ({"attempt":k,"caps":hits[0]["caps"],"solo_mode":False,"reason":"RESIDUAL_RETRY"} if assembly else honor_residual(ctx, call, k, records, residuals, rows))',
          lambda s: residual_probe(s, assembly=True))
    trial("interrupted_entry_unrecoverable", "entry_reuse", 'need(not records, "ALREADY_LAUNCHED")',
          'need(not records and refusals, "ALREADY_LAUNCHED")', core_probe("N04_interrupted_entry_reuse"))

    def resume_probe(s):
        f = resume_fixture(s, "resume")
        s.eq(s.module.read_pin(s.module.launch_resume(f.ctx, f.name, 1))["outcome"], "LAUNCH")
    trial("resume_always_refused", "launch_resume", "ctx.gate()",
          'ctx.gate()\n    raise Refusal("COUNTERFACTUAL_RESUME_REFUSED")', resume_probe)

    def reused_pid_probe(s):
        M = s.module
        rows = [{"pid":900001,"ppid":1,"pgid":900001,"command":"/bin/sleep 120"}]
        s.eq(M.qualified_process(rows,900001,M.REAL["monitor"]["path"],"/synthetic/NGC_RUN","monitor"),None)
    trial("bare_monitor_pid", "qualified_process",
          'if row["pid"] != pid or not has_arg(row["command"], tool):',
          'if row["pid"] != pid:\n            continue\n        return row\n        if not has_arg(row["command"], tool):',
          reused_pid_probe)
    suite.interfaces["mutation_tests"] = mutation_rows


"""Public same-k recovery after a synthetic interruption or clean refusal."""


def recovery_live_cases(suite):
    import json
    import subprocess
    import time
    from pathlib import Path
    M = suite.module
    for mode in ("interrupted", "refused"):
        f = full_launch_fixture(suite, "RECOVERY_" + mode)
        helper = """import hashlib,json,sys,types
from pathlib import Path
tool,tool_sha,config,config_sha,syn,syn_sha,mode=sys.argv[1:]
raw=Path(tool).read_bytes()
assert hashlib.sha256(raw).hexdigest()==tool_sha
M=types.ModuleType("_p112_interruption_fixture");M.__file__=tool
exec(compile(raw,tool,"exec"),M.__dict__)
synthetic_pin={"path":syn,"sha256":syn_sha}
data=M.read_pin(synthetic_pin)
ctx=M.Context({"path":config,"sha256":config_sha},system=M.SyntheticSystem(data["system"]),synthetic_pins=data["pins"])
ctx.synthetic_pin=synthetic_pin
ctx.gate()
call=ctx.call("P1_M0001")
hist=M.history(ctx,call)
decision=M.next_attempt(call["name"],hist["records"],hist["actual"],hist["residuals"],hist["trailing_nonattempt"])
M.create_layout(ctx)
work=M.new_work(ctx,call["name"],decision["attempt"])
mp,m15=ctx.seed_check()
plan=M.make_plan(ctx,call,decision,work,mp,m15)
pp=ctx.write(str(work/"plan.json"),plan)
dry=M.run_dry(ctx,call,work)
ep=M.register_call(ctx,call,plan,dry,work,hist)
if mode=="interrupted":
 def broken_ps():raise M.Refusal("PS_FAILED")
 ctx.system.processes=broken_ps
 result=M.sampler(ctx,plan,str(work),poll_s=5)
 assert result["status"]=="FIRST_SAMPLE_FAILED_NO_SOLO_FILE"
else:
 with M.new_log(work/"monitor.stdout.txt"):pass
 with M.new_log(work/"monitor.stderr.txt"):pass
 result=M.record_monitor_refused(ctx,pp,str(work))
print(json.dumps({"entry":ep,"work":str(work),"result":result,"outdir":plan["outdir"]},sort_keys=True))
"""
        hp = suite.raw_write(f.root / "prepare_saved_interruption.py", helper.encode())
        watch = subprocess.Popen([M.PY, "-I", "-B", f.watch["path"]], env=M.child_env(),
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        common = ["--config", f.config["path"], "--config-sha256", f.config["sha256"],
                  "--synthetic-pins", f.synthetic["path"], "--synthetic-pins-sha256", f.synthetic["sha256"]]
        base = [M.PY, "-I", "-B", str(suite.tool_path)]
        saved = {}
        try:
            p = subprocess.run([M.PY, "-I", "-B", hp["path"], str(suite.tool_path), suite.tool_sha,
                                f.config["path"], f.config["sha256"], f.synthetic["path"], f.synthetic["sha256"], mode],
                               env=M.child_env(), capture_output=True, text=True, timeout=35)
            def first_check():
                suite.eq(p.returncode, 0)
                saved.update(json.loads(p.stdout.strip().splitlines()[-1]))
                suite.eq(Path(saved["outdir"] + ".solo.json").exists(), False)
                suite.eq(Path(saved["outdir"] + ".receipt.json.launch.json").exists(), False)
                suite.eq(M.pin_of(saved["entry"]["path"]), saved["entry"])
            suite.case("N04_public_" + mode + "_entry_without_monitor", first_check)
            if not saved:
                continue
            registry_before = sorted((f.root / "launch_root" / "registry").iterdir())
            p = subprocess.run(base + ["launch"] + common + ["--name", f.name, "--attempt", "1"],
                               env=M.child_env(), capture_output=True, text=True, timeout=35)
            result = {}
            def second_check():
                suite.eq(p.returncode, 0)
                result.update(json.loads(p.stdout.strip().splitlines()[-1]))
                suite.eq("ALREADY_REGISTERED_SAME_SPEC" in p.stderr, True)
                rec = M.read_pin(result)
                suite.eq(rec["attempt"], 1)
                suite.eq(rec["outcome"], "LAUNCH")
                suite.eq(rec["registry_entry"], saved["entry"])
                suite.eq(M.pin_of(saved["entry"]["path"]), saved["entry"])
                suite.eq(sorted((f.root / "launch_root" / "registry").iterdir()), registry_before)
                suite.eq(str(Path(rec["plan"]["path"]).parent) != saved["work"], True)
            suite.case("N04_public_" + mode + "_same_k_reuses_entry_new_work", second_check)
            if not result:
                continue
            until = time.monotonic() + 25
            sample_path = Path(saved["outdir"] + ".solo.json")
            while not sample_path.is_file() and time.monotonic() < until:
                time.sleep(0.1)
            suite.case("N04_public_" + mode + "_sampler_completed", lambda: suite.eq(sample_path.is_file(), True))
            time.sleep(0.2)
            p = subprocess.run(base + ["close-attempt"] + common + ["--name", f.name, "--attempt", "1"],
                               env=M.child_env(), capture_output=True, text=True, timeout=35)
            suite.case("N04_public_" + mode + "_closes_after_recovery",
                       lambda: suite.eq((p.returncode, json.loads(p.stdout.strip().splitlines()[-1])["status_class"]),
                                        (0, "FINISHED")))
        finally:
            if watch.poll() is None:
                watch.terminate()
                try:
                    watch.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    watch.kill()
                    watch.wait(timeout=3)
    suite.interfaces["same_k_recovery_scope"] = (
        "TESTED public launch after a separate synthetic invocation exits with a registered entry: "
        "first sampler ps failure, and a D7 monitor-refusal record. Both reuse the pinned entry at k=1, "
        "report ALREADY_REGISTERED_SAME_SPEC, use a new work directory and close successfully. "
        "No real scientific monitor or driver was started.")


"""Remaining named brief cases using local synthetic inputs and saved states."""


def contract_gap_cases(suite):
    import copy
    import math
    import os
    from pathlib import Path
    M, case, fail = suite.module, suite.case, suite.refuses
    f = full_launch_fixture(suite, "T11_kit_mapping")
    def context():
        return M.Context(f.config, system=M.SyntheticSystem(M.read_pin(f.synthetic)["system"]), synthetic_pins=f.overrides)
    ctx = context()
    cfg = ctx.cfg["members"][0]
    spec, spec_pin, fill, fill_pin, certs = ctx.read_fill(cfg)
    handoff = M.read_pin(cfg["handoff"])
    for side, label, code in ((2, "wrong_label", "SPEC_LABEL_KEY"), (2, "wrong_leaf", "SPEC_LEAF"),
                              (2, "wrong_eps", "SPEC_EPS_PIN"), (2, "wrong_lo", "SPEC_LO_PIN"),
                              (3, "pair_difference", "SPEC_PAIR_DIFFERENCE")):
        args = [handoff, cfg["handoff"], *copy.deepcopy(fill), M.theta_key(M.read_pin(ctx.cfg["plan_output_primary"])["members"][0]["theta_engine"]),
                cfg["eps"], ctx.pins["lo"], "UNT_STEP5_ADMITTED_POINT_HANDOFF_CX3V001", True]
        if label == "wrong_label":
            args[side]["label"] = "step5 A_K32_A2_HEADLINE theta_key=" + "f" * 64
        elif label == "wrong_leaf":
            args[side]["numerics"]["route_a"]["column_workers"] = 8
        elif label == "wrong_eps":
            args[side]["numerics"]["uv_tail"]["eps_certificate"] = {}
        elif label == "wrong_lo":
            args[side]["numerics"]["uv_tail"]["lo_certificate"] = {}
        else:
            args[side]["physical"]["ell_F_m"] = math.nextafter(spec["physical"]["ell_F_m"], math.inf)
        case("T10_fill_" + label, lambda args=args, code=code: fail(code, lambda: M.fill_check(*args)))

    for changed in (False, True):
        label = "ulp" if changed else "honest"
        c = context()
        kit = c.kit_entries()
        entry_spec = copy.deepcopy(spec)
        if changed:
            entry_spec["physical"]["ell_F_m"] = math.nextafter(entry_spec["physical"]["ell_F_m"], math.inf)
        sp = suite.fixture("T11_kit_spec_" + label + ".json", entry_spec)
        name = "S0_J0_SERIAL"
        key = M.theta_key(M.read_pin(c.cfg["plan_output_primary"])["members"][0]["theta_engine"])
        entry = {"schema":"UNT_S0_LAUNCH_REGISTRY_ENTRY_C2V003A", "name":name, "theta_key":key,
                 "spec":sp, "v006_spec_pin":sp, "v006_handoff_pin":cfg["handoff"]}
        ep = suite.fixture("T11_kit_entry_" + label + ".json", entry)
        kit[name] = entry, ep
        c.kit_entries = lambda kit=kit: kit
        c.vpins["SPEC_PIN"][name] = sp
        if changed:
            before = {str(p) for p in f.root.rglob("*")}
            case("T11_kit_spec_one_ulp_assembly_refuses", lambda c=c: fail(
                "THETA_BITS_MISMATCH", lambda: M.assemble_registry(c)))
            case("T11_kit_mismatch_writes_nothing", lambda before=before: suite.eq(
                {str(p) for p in f.root.rglob("*")}, before))
        else:
            case("T11_honest_S0_member_mapping", lambda c=c: suite.eq(
                (c.calls()[0]["name"], c.calls()[0]["kind"], c.calls()[0]["origin"]),
                ("S0_J0_SERIAL", "MEMBER", "KIT")))

    f = full_launch_fixture(suite, "L04_dry_without_gate")
    ctx = M.Context(f.config, system=M.SyntheticSystem(M.read_pin(f.synthetic)["system"]), synthetic_pins=f.overrides)
    ctx.v006_text = "## A999: no TOOL_PIN\n"
    ctx.system.processes = lambda: [
        {"pid":os.getpid(),"ppid":1,"pgid":os.getpid(),"command":M.PY + " -I -B /synthetic/test.py"},
        {"pid":900111,"ppid":1,"pgid":900111,"command":M.PY + " -I -B " + f.watch["path"]}]
    case("L04_dry_without_TOOL_PIN", lambda: suite.eq(M.launch(ctx, f.name, dry=True)["status"], "DRY_NOT_LAUNCHED"))
    case("L04_status_without_TOOL_PIN", lambda: suite.eq(M.status(ctx)["calls"][0]["status"], "READY"))
    ctx.system.fixture["mount_points"] = []
    before = {str(p) for p in f.root.rglob("*")}
    ctx.v006_text = Path(f.config_doc["v006"]).read_text()
    case("N19_launch_unmounted_refuses", lambda: fail("RUN_VOLUME_NOT_MOUNTED", lambda: M.launch(ctx, f.name)))
    case("N19_launch_unmounted_no_write", lambda: suite.eq({str(p) for p in f.root.rglob("*")}, before))
    old_record_paths = ctx.record_paths
    ctx.record_paths = lambda name=None: []
    case("N16_seed_launch_required", lambda: fail("SEED_SERIAL_NOT_LAUNCHED_FIRST", ctx.seed_check))
    ctx.record_paths = old_record_paths

    f = receipt_fixture(suite, "N16_kit_started_recordless")
    name = "S0_J0_SERIAL"
    call = dict(f.call, name=name, origin="KIT", entry=M.read_pin(f.entry_pin), entry_pin=f.entry_pin)
    f.ctx._fixture_calls = [call]
    f.ctx._fixture_kit[name] = M.read_pin(f.entry_pin), f.entry_pin
    outdir = M.planned_outdir(f.ctx, name, 1, "KIT")
    suite.raw_write(Path(outdir + ".receipt.json.stdout.txt"), b"SYNTHETIC_UNREADABLE_MONITOR_LOG")
    case("N16_started_without_line_refuses", lambda: fail("MONITOR_STARTED_NO_LAUNCH_JSON",
                                                        lambda: M.history(f.ctx, call)))
    f.ctx.v006_text += "RESIDUAL_RETRY S0_J0_SERIAL 1\n"
    def takeover():
        h = M.history(f.ctx, call)
        decision = M.next_attempt(name, h["records"], h["actual"], h["residuals"], h["trailing_nonattempt"])
        suite.eq((decision["attempt"], decision["caps"], decision["solo_mode"]), (2, M.first_caps(name), False))
        suite.eq(M.planned_origin(name, 2, h["records"], h["residuals"]), "P112")
        suite.eq(M.register_call(f.ctx, call, {"attempt":2}, f.entry_pin, f.root, h), f.entry_pin)
    case("N16_recordless_kit_residual_takeover", takeover)

    for actual_middle in (False, True):
        f = receipt_fixture(suite, "N13_pair_" + str(actual_middle), mode="REFUSED", record=False, sample={})
        first_record = dict(f.record, solo_mode=True)
        suite.raw_write(f.record_path, M.encoded(first_record))
        M.close_attempt(f.ctx, f.name, 1)
        for k in (2, 3):
            outdir = M.planned_outdir(f.ctx, f.name, k, "P112")
            actual = k == 3 or actual_middle
            if actual:
                Path(outdir).mkdir()
            receipt = copy.deepcopy(f.rec)
            receipt["child_pid"] = 900020 + k
            if k == 2:
                receipt.update(status="CHILD_FAILED", driver_status=None, exit_code=1)
            receipt["receipt_sha256"] = M.sha(M.canonical({a:b for a,b in receipt.items() if a != "receipt_sha256"}))
            suite.raw_write(Path(outdir + ".receipt.json"), M.encoded(receipt))
            lj = M.strict_json(
                Path(f.outdir + ".receipt.json.launch.json").read_bytes())
            lj["child_pid"] = receipt["child_pid"]
            lj["command"] = M.driver_command(f.ctx.pins, f.call["spec"], outdir)
            lp = suite.raw_write(Path(outdir + ".receipt.json.launch.json"), M.encoded(lj))
            sample = M.read_pin(M.pin_of(f.outdir + ".solo.json"))
            sample.update(attempt=k, outdir=outdir)
            suite.raw_write(Path(outdir + ".solo.json"), M.encoded(sample))
            outcome = "MISLAUNCH" if k == 2 else "LAUNCH"
            record = dict(f.record, schema="UNT_P112_" + outcome + "_RECORD_CX2V001", outcome=outcome,
                          attempt=k, outdir=outdir, receipt=outdir + ".receipt.json", solo_mode=True,
                          launch_json=dict(lp, child_pid=lj["child_pid"], utc=lj["utc"]))
            suite.raw_write(f.root / "launch_root" / "launches" /
                            ("P112_%s_%s_CX2V001_A%d.json" % (f.name, outcome, k)), M.encoded(record))
            if actual:
                M.close_attempt(f.ctx, f.name, k)
            else:
                fail("NOT_AN_ATTEMPT", lambda: M.close_attempt(f.ctx, f.name, k))
        h = M.history(f.ctx, f.call)
        if actual_middle:
            case("N08_actual_MISLAUNCH_separates_infra_pair", lambda h=h, f=f:
                 suite.eq(M.terminal_prefix(h["actual"], f.name), None))
        else:
            case("N13_nonattempt_MISLAUNCH_does_not_separate", lambda h=h, f=f: (
                suite.eq([r["attempt"] for r in h["actual"]], [1, 3]),
                suite.eq(M.terminal_prefix(h["actual"], f.name)["disposition"], "UNEVALUATED_INFRA_REPEAT")))


"""Malformed-input and configuration refusals; fixtures never replace old bytes."""


def refusal_input_cases(suite):
    import contextlib
    import copy
    import io
    import json
    from pathlib import Path
    M, case, fail = suite.module, suite.case, suite.refuses
    def bad(code, action):
        case("REFUSE_" + code, lambda: fail(code, action))
    bad("JSON_DUPLICATE_KEY", lambda: M.strict_json(b'{"a":1,"a":2}'))
    bad("JSON_NONFINITE", lambda: M.strict_json(b'{"a":NaN}'))
    bad("JSON_PARSE", lambda: M.strict_json(b'{'))
    bad("PIN_FORM", lambda: M.read_pin({}))
    bad("UTC_FORMAT", lambda: M.timestamp("2026-13-01T00:00:00Z"))
    bad("THETA_NOT_NUMERIC", lambda: M.fhex("1.0", "coordinate"))
    bad("THETA_NONFINITE", lambda: M.fhex(float("inf"), "coordinate"))
    bad("MISSING_FIELD", lambda: M.dig({}, ("physical", "gamma")))
    bad("OUTPUT_ABSOLUTE", lambda: M.write_x_bytes("relative.json", b"{}"))
    bad("RECORD_DATE_U", lambda: M.write_x(str(suite.root / "undated.json"), {}))
    bad("PATH_ABSOLUTE_NORMALIZED", lambda: M.path_rules("/synthetic/../invalid"))
    bad("PATH_CODEX", lambda: M.path_rules(str(Path.home() / ".codex" / "DO_NOT_OPEN")))
    bad("PATH_PROTECTED_TREE", lambda: M.path_rules("/synthetic/UNT_INTERNAL_RUNS/DO_NOT_OPEN"))
    bad("PATH_UVT", lambda: M.path_rules("/synthetic/UVT_DO_NOT_OPEN"))
    volume = suite.root / "guard_volume"
    volume.mkdir()
    alias = suite.root / "guard_alias"
    alias.symlink_to(volume, target_is_directory=True)
    bad("OUTPUT_PARENT_SYMLINK", lambda: M.write_x_bytes(alias / "new.json", b"{}"))
    M.READ_RUN_ROOTS.add(str(volume))
    bad("FORBIDDEN_OUTDIR_READ", lambda: M.guard_read(volume / "NGC_RUN" / "anything.txt"))
    bad("PS_DUPLICATE_PID", lambda: M.parse_ps("2 1 2 a\n2 1 2 b\n"))
    case("B4_PS_COMMAND_FALLBACK", lambda: suite.eq(M.command_argv({"command": 'python "unclosed'}), ['python', '"unclosed']))
    bad("PROCESS_ROLE", lambda: M.qualified_process(
        [{"pid":2,"ppid":1,"pgid":2,"command":"/synthetic/tool.py"}],2,"/synthetic/tool.py","/synthetic/run","unknown"))
    bind = dict(name="P1_M0001", attempt=1, outdir="/synthetic/NGC_RUN", receipt="/synthetic/NGC_RUN.receipt.json",
                launch_pin={"path":"/synthetic/launch.json","sha256":"a"*64}, child_pid=2)
    bad("DRIVER_STATUS_FORM", lambda: M.raw_status({"status":"FINISHED","driver_status":17}, **bind))
    bad("EXIT_CODE_FORM", lambda: M.raw_status({"status":"CHILD_FAILED","driver_status":None,"exit_code":None}, **bind))
    bad("MONITOR_RECEIPT_SCHEMA", lambda: M.monitor_receipt(M.encoded({"schema":"WRONG"})))
    bad("PLANNED_STOP_NOT_TWIN", lambda: M.terminal_prefix([{"status_class":"PLANNED_STOP"}], "P1_M0001"))
    bad("REFUSAL_ATTEMPT_MISMATCH", lambda: M.entry_reuse(
        {"spec":{"sha256":"a"*64},"point_key":"b"*64,"v006_spec_pin":{},"v006_handoff_pin":{}},
        {"spec":{"sha256":"a"*64},"point_key":"b"*64,"v006_spec_pin":{},"v006_handoff_pin":{}},
        [],[{"attempt":2}],1))
    sample = {"complete":True,"poll_s":5,"largest_gap_s":5,"n_samples":3,
              "first_utc":"2026-10-20T10:00:00Z","last_utc":"2026-10-20T10:00:12Z","max_other_ngc_processes":0}
    rec = {"utc_start":"2026-10-20T10:00:01Z","utc_end":"2026-10-20T10:00:10Z"}
    for code, key, value in (("SAMPLE_POLL","poll_s",0),("SAMPLE_GAP","largest_gap_s",-1),
                             ("SAMPLE_N","n_samples",1),("SAMPLE_COUNT","max_other_ngc_processes",-1)):
        case("REFUSE_" + code, lambda key=key,value=value: suite.eq(M.sample_value(dict(sample, **{key:value}),rec),None))
    f = full_launch_fixture(suite, "configuration_refusals")
    system_doc = M.read_pin(f.synthetic)["system"]
    def construct(cfg=None, system=None, overrides=None, label="changed"):
        pin = f.config if cfg is None else suite.fixture("config_" + label + ".json", cfg)
        return M.Context(pin, system=M.SyntheticSystem(system_doc) if system is None else system,
                         synthetic_pins=f.overrides if overrides is None else overrides)
    for code, key, value in (
            ("CONFIG_SCHEMA","schema","WRONG"),("CONFIG_PYTHON","python","/synthetic/python"),
            ("CONFIG_RAM","host_ram_bytes_expected",1),("RUN_ROOT_LAYOUT","run_root",str(f.root / "WRONG")),
            ("LAUNCH_ROOT_EXTERNAL","p112_launch_root","/Volumes/P112_SYNTHETIC_NO_ACCESS"),
            ("CUTOFF_COPY_IN_RUN_TREE","v006_copy_dir",f.config_doc["run_root"] + "/copies"),
            ("V006_PATH","v006","relative.md")):
        cfg = copy.deepcopy(f.config_doc)
        cfg[key] = value
        bad(code, lambda cfg=cfg,code=code: construct(cfg, label=code))
    cfg = copy.deepcopy(f.config_doc)
    cfg["v006_copy_dir"] = str(alias)
    bad("CONFIG_SYMLINK", lambda: construct(cfg, label="symlink"))
    bad("SYNTHETIC_PINS_REQUIRED", lambda: M.Context(f.config, system=M.SyntheticSystem(system_doc)))
    bad("SYNTHETIC_SYSTEM_REQUIRED", lambda: M.Context(f.config, system=M.System(), synthetic_pins=f.overrides))
    bad("SYNTHETIC_PIN_FORM", lambda: M.synthetic_fence({}, {}))
    ctx = construct()
    bad("WRITE_SCOPE", lambda: ctx.write(str(suite.root / "outside_context.json"), {"date_u":M.date_u()}))
    bad("V006_PIN_MISSING", lambda: ctx.get_vpin("SPEC_PIN","NOT_A_CONFIGURED_CALL"))
    bad("NAME_ATTEMPT", lambda: M.planned_outdir(ctx,"P1_M0001",0,"P112"))
    bad("MEMORY_WATCH_NOT_RUNNING", lambda: (setattr(ctx.system,"processes",lambda:[]), M.watch_check(ctx)))
    bad("INVOCATION_PROCESS_NOT_VISIBLE", lambda: M.own_process_command(ctx))
    pins = f.overrides
    spec = M.pin_of(Path(f.config_doc["members"][0]["fill_dir"]) / M.SERIAL_FILE)
    caps = M.first_caps(f.name)
    argv = M.monitor_command(pins,spec,str(f.root / "volume" / "NGC_TEST"),caps)
    bad("MONITOR_ARGV", lambda: M.check_monitor_command(argv+["--unknown"],pins,spec,str(f.root / "volume" / "NGC_TEST"),caps,f.name))
    bad_caps = dict(caps,wall_cap_s=0)
    bad("CAP_FORM", lambda: M.check_monitor_command(M.monitor_command(pins,spec,str(f.root / "volume" / "NGC_TEST"),bad_caps),
                                                    pins,spec,str(f.root / "volume" / "NGC_TEST"),bad_caps,f.name))
    occupied = f.root / "volume" / "NGC_OCCUPIED"
    occupied.mkdir()
    bad("OUTPUT_EXISTS", lambda: M.disk_check(ctx.cfg,str(occupied),caps,ctx.system))
    bad("FILL_DIR_REAL", lambda: ctx.read_fill(dict(ctx.cfg["members"][0],fill_dir=str(f.root / "missing_fill"))))
    old_root = ctx.cfg["p112_launch_root"]
    ctx.cfg["p112_launch_root"] = str(f.root / "missing_launch_root")
    bad("LAUNCH_ROOT_REAL", lambda: M.create_layout(ctx))
    ctx.cfg["p112_launch_root"] = old_root
    M.create_layout(ctx)
    broken = Path(old_root) / "work" / "broken_plan"
    broken.mkdir()
    suite.raw_write(broken / "plan.json", b"{")
    bad("INFLIGHT_PLAN_UNREADABLE", lambda: M.enforce_solo(ctx,False,rows=[]))

    common = ["--config",f.config["path"],"--config-sha256",f.config["sha256"],
              "--synthetic-pins",f.synthetic["path"],"--synthetic-pins-sha256",f.synthetic["sha256"]]
    def cli_refuse(code, command, extra):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = M.cli([command]+common+extra)
        suite.eq(status,2)
        suite.eq(json.loads(output.getvalue())["code"],code)
    for code, command, extra in (
            ("DRY_COMMAND","status",["--dry"]),("RESUME_COMMAND","status",["--resume"]),
            ("VERIFY_COMMAND","status",["--verify"]),("NAME_REQUIRED","launch",[]),
            ("ATTEMPT_REQUIRED","close-attempt",["--name",f.name]),
            ("REFUSAL_ARGUMENTS","record-monitor-refused",[]),("SAMPLER_ARGUMENTS","_sampler",[])):
        case("REFUSE_"+code,lambda code=code,command=command,extra=extra:cli_refuse(code,command,extra))
    output = io.StringIO()
    def lone_sha():
        with contextlib.redirect_stdout(output):
            result=M.cli(["status","--config",f.config["path"],"--config-sha256",f.config["sha256"],
                          "--synthetic-pins-sha256","a"*64])
        suite.eq((result,json.loads(output.getvalue())["code"]),(2,"SYNTHETIC_SHA_WITHOUT_FILE"))
    case("REFUSE_SYNTHETIC_SHA_WITHOUT_FILE",lone_sha)
    bad_syn = M.read_pin(f.synthetic)
    bad_syn["schema"] = "WRONG"
    sp = suite.fixture("wrong_synthetic_manifest.json",bad_syn)
    output = io.StringIO()
    def wrong_syn():
        with contextlib.redirect_stdout(output):
            result=M.cli(["status","--config",f.config["path"],"--config-sha256",f.config["sha256"],
                          "--synthetic-pins",sp["path"],"--synthetic-pins-sha256",sp["sha256"]])
        suite.eq((result,json.loads(output.getvalue())["code"]),(2,"SYNTHETIC_SCHEMA"))
    case("REFUSE_SYNTHETIC_SCHEMA",wrong_syn)


"""Refuse invalid PLAN, mapping, certificate and fixed-point custody inputs."""


def refusal_mapping_cases(suite):
    import copy
    from pathlib import Path
    M, case, fail = suite.module, suite.case, suite.refuses
    f = full_launch_fixture(suite, "mapping_refusals")
    system_doc = M.read_pin(f.synthetic)["system"]
    def context():
        return M.Context(f.config, system=M.SyntheticSystem(system_doc), synthetic_pins=f.overrides)
    def bad(code, change, action=None):
        c = context()
        change(c)
        case("REFUSE_"+code,lambda:fail(code,lambda:action(c) if action else c.calls()))
    def changed(c, field, code, edit):
        doc=M.read_pin(c.cfg[field])
        edit(doc)
        c.cfg[field]=suite.fixture("mapping_"+code+".json",doc)
        if code in ("F_IDENTITY", "F_POINT_KEY"):
            cfg=c.cfg["f_points"][0]
            hand=M.read_pin(cfg["handoff"])
            hand["source_pin"]=c.cfg[field]
            cfg["handoff"]=suite.fixture("mapping_f_handoff_"+code+".json",hand)
    tests = (
        ("AT0A_NOT_PASS","at0a_pass",lambda d:d.update(outcome="FAIL")),
        ("PLAN_BUILD_RECORD","plan_build_record",lambda d:d.update(stage="ASSEMBLE")),
        ("PLAN_NOT_BUDGET_ZERO","plan_output_primary",lambda d:d.update(budget=1)),
        ("PLAN_NOT_VALUE_FREE","plan_output_primary",lambda d:d["members"][0].update(evaluated=True)),
        ("MEMBER_COUNT","plan_output_primary",lambda d:d["members"].append(copy.deepcopy(d["members"][0]))),
        ("FDPLAN_SCHEMA","fdplan",lambda d:d.update(schema="WRONG")),
        ("SELECTION_MEMBERS","selection",lambda d:d.update(points=[])),
        ("SELECTION_IDENTITY","selection",lambda d:d["points"][0].update(role="wrong")),
        ("MEMBER_ORDER","plan_output_primary",lambda d:d["members"][0].update(order=1)),
        ("FDPLAN_MEMBER_IDENTITY","fdplan",lambda d:d["members"][0].update(log_index=2)),
        ("FDPLAN_MEMBER_ORDER","fdplan",lambda d:d["members"][0].update(order=1)),
        ("FDPLAN_POINT_KEY","fdplan",lambda d:d["members"][0].update(key="a"*64)),
        ("FDPLAN_THETA_KEY_SET","fdplan",lambda d:d["members"][0]["theta_hex"].pop("ell_F_m")),
        ("PLAN_NUISANCE_FIELD","plan_output_primary",lambda d:d["members"][0]["theta_ngc"].pop("ngc3198_distance_Mpc")),
        ("PLAN_THETA_NGC_EXACT_FLOAT","plan_output_primary",lambda d:d["members"][0]["theta_ngc"].update(untyped_extra=1)),
        ("F_COUNT","fdplan",lambda d:d["F"].pop()),
        ("F_IDENTITY","fdplan",lambda d:d["F"][0].update(role="F1")),
        ("F_POINT_KEY","fdplan",lambda d:d["F"][0].update(key="a"*64)),
    )
    for code,field,edit in tests:
        bad(code,lambda c,code=code,field=field,edit=edit:changed(c,field,code,edit))
    bad("SPEC_OF_RECORD",lambda c:c.cfg.update(spec_of_record={"path":"/synthetic/spec.json","sha256":"a"*64}))
    bad("F_LABELS",lambda c:c.cfg["f_points"][0].update(label="F2"))
    def change_hand(c,code,edit,member=True):
        cfg=c.cfg["members"][0] if member else c.cfg["f_points"][0]
        hand=M.read_pin(cfg["handoff"])
        edit(hand)
        cfg["handoff"]=suite.fixture("handoff_"+code+".json",hand)
    bad("HANDOFF_MEMBER_IDENTITY",lambda c:change_hand(c,"identity",lambda d:d.update(log_index=2)))
    def export_change(c):
        cfg=c.cfg["members"][0]
        hand=M.read_pin(cfg["handoff"])
        export=M.read_pin(hand["source_export_pin"])
        export["admitted_points"]=[]
        hand["source_export_pin"]=suite.fixture("missing_member_export.json",export)
        cfg["handoff"]=suite.fixture("missing_export_handoff.json",hand)
    bad("EXPORT_MEMBER_NOT_UNIQUE",export_change)
    bad("F_SOURCE_FDPLAN",lambda c:change_hand(c,"f_source",lambda d:d.update(source_pin={}),False))
    def cert_change(c):
        c.cfg["members"][0]["eps"]=suite.fixture("wrong_point_certificate.json",{"point":{"key":"a"*64}})
    bad("CERTIFICATE_POINT_KEY",cert_change)
    bad("HANDOFF_V006_PIN",lambda c:c.vpins["HANDOFF_PIN"]["P1_M0001"].update(sha256="a"*64))
    bad("SPEC_V006_PIN",lambda c:c.vpins["SPEC_PIN"]["P1_M0001"].update(sha256="a"*64))
    def kit_override(c,kind):
        kit=c.kit_entries()
        if kind=="missing_seed":
            kit.pop("S0_SEED_SERIAL")
        elif kind=="missing_twin":
            kit.pop(M.TWIN)
        elif kind=="wrong_twin":
            e,p=kit[M.TWIN]
            kit[M.TWIN]=(dict(e,theta_key="a"*64),p)
        else:
            spec,sp,fill,fp,certs=c.read_fill(c.cfg["members"][0])
            key=M.read_pin(c.cfg["fdplan"])["members"][0]["key"]
            if kind=="physical_keys":
                spec["physical"]["additional"]=1.0
                sp=suite.fixture("kit_extra_physical.json",spec)
            entry={"schema":"UNT_S0_LAUNCH_REGISTRY_ENTRY_C2V003A","name":"S0_J0_SERIAL","theta_key":key,
                   "spec":sp,"v006_handoff_pin":c.cfg["members"][0]["handoff"]}
            ep=suite.fixture("kit_override_"+kind+".json",entry)
            kit["S0_J0_SERIAL"]=(entry,ep)
            c.vpins["SPEC_PIN"]["S0_J0_SERIAL"]=dict(sp)
            if kind=="duplicate":
                kit["S0_J1_SERIAL"]=(dict(entry,name="S0_J1_SERIAL"),ep)
            if kind=="vpin":
                c.vpins["SPEC_PIN"]["S0_J0_SERIAL"]["sha256"]="a"*64
        c.kit_entries=lambda:kit
    for code,kind in (("SEED_REGISTRY_MISSING","missing_seed"),("TWIN_REGISTRY_MISSING","missing_twin"),
                      ("TWIN_REGISTRY_BINDING","wrong_twin"),("KIT_PHYSICAL_KEYS","physical_keys"),
                      ("KIT_POINT_DUPLICATE","duplicate"),("KIT_SPEC_V006","vpin")):
        bad(code,lambda c,kind=kind:kit_override(c,kind))
    bad("TWIN_SPEC_V006",lambda c:c.vpins["SPEC_PIN"][M.TWIN].update(sha256="a"*64))
    def duplicate_member(c):
        changed(c,"plan_output_primary","duplicate_plan",lambda d:d["members"].append(copy.deepcopy(d["members"][0])))
        changed(c,"fdplan","duplicate_fd",lambda d:d["members"].append(copy.deepcopy(d["members"][0])))
        changed(c,"selection","duplicate_sel",lambda d:d["points"].append(copy.deepcopy(d["points"][0])))
        other=copy.deepcopy(c.cfg["members"][0])
        other["order"]=1
        c.cfg["members"].append(other)
    bad("DUPLICATE_MEMBER_POINT",duplicate_member)
    def missing_kit_schema(c):
        root=f.root/"bad_kit_root"
        (root/"registry").mkdir(parents=True)
        suite.raw_write(root/"registry"/"S0_SEED_SERIAL_C2V003A.json",M.encoded({"schema":"WRONG"}))
        c.cfg["s0"]["launch_root"]=str(root)
    bad("KIT_REGISTRY_SCHEMA",missing_kit_schema,lambda c:c.kit_entries())
    def missing_m15(c):
        root=f.root/"bad_m15_root"
        root.mkdir()
        suite.raw_write(root/"M15_PRELAUNCH_RECORD_C2V001.json",M.encoded({"schema":"WRONG"}))
        c.cfg["s0"]["launch_root"]=str(root)
    bad("M15_SCHEMA",missing_m15,lambda c:c.seed_check())


"""Saved-record and receipt custody failures, always with new synthetic files."""


def refusal_custody_cases(suite):
    import copy
    from pathlib import Path
    M, case, fail = suite.module, suite.case, suite.refuses
    def bad(code, action):
        case("REFUSE_"+code,lambda:fail(code,action))
    for code, changes in (
            ("ATTEMPT_FILENAME_BINDING",{"attempt":2}),
            ("ATTEMPT_RECORD_SCHEMA",{"schema":"WRONG"}),
            ("LAUNCH_JSON_RECORD_PIN",None)):
        f=receipt_fixture(suite,"record_"+code,record=False)
        rec=copy.deepcopy(f.record)
        if changes is None:
            rec["launch_json"]["sha256"]="a"*64
        else:
            rec.update(changes)
        suite.raw_write(f.record_path,M.encoded(rec))
        bad(code,(lambda f=f:M.close_attempt(f.ctx,f.name,1)) if changes is None else (lambda f=f:f.ctx.records()))
    f=receipt_fixture(suite,"location_refusals")
    bad("ATTEMPT_RECORD_MISSING",lambda:M.close_attempt(f.ctx,f.name,2))
    bad("ATTEMPT_PATH_BINDING",lambda:M.validate_record_location(f.ctx,dict(f.record,origin="P112",outdir="/synthetic/wrong")))
    bad("ATTEMPT_LAUNCH_JSON_PATH",lambda:M.validate_record_location(f.ctx,dict(f.record,origin="P112",launch_json={"path":"/synthetic/wrong"})))
    bad("ATTEMPT_NEEDS_CLOSE",lambda:M.history(f.ctx,f.call))
    bad("REGISTRY_ENTRY_MISSING",lambda:M.registered_entry(f.ctx,dict(f.call,name="P1_M0099")))
    for code, schema in (("REGISTRY_SCHEMA","WRONG"),("REGISTRY_CALL_BINDING","UNT_P112_LAUNCH_REGISTRY_ENTRY_CX2V001")):
        name="P1_M0098" if code=="REGISTRY_SCHEMA" else "P1_M0097"
        entry=dict(M.read_pin(f.entry_pin),name=name,schema=schema,point_key="a"*64)
        suite.raw_write(Path(M.own_registry_path(f.ctx,name)),M.encoded(entry))
        bad(code,lambda name=name:M.registered_entry(f.ctx,dict(f.call,name=name)))
    broken={"schema":"STEP5_ATTEMPT_RECEIPT_C2V001","call":{"name":f.name},"attempt":1,
            "spec_sha256":f.call["spec"]["sha256"],"theta_sha256":"a"*64}
    suite.raw_write(Path(f.outdir+".attempt_receipt.json"),M.encoded(broken))
    bad("ATTEMPT_RECEIPT_BINDING",lambda:M.history(f.ctx,f.call))
    f=receipt_fixture(suite,"live_monitor_missing_receipt",no_receipt=True)
    f.ctx.system.rows=[{"pid":900001,"ppid":1,"pgid":900001,"command":
                       M.PY+" -I -B "+f.ctx.pins["monitor"]["path"]+" --receipt "+f.outdir+".receipt.json"}]
    bad("ATTEMPT_ACTIVE",lambda:M.history(f.ctx,f.call))
    bad("MONITOR_RECEIPT_MISSING",lambda:M.close_attempt(f.ctx,f.name,1))
    for code, edit in (
            ("MONITOR_CHILD_BINDING",lambda d:d.update(child_pid=999999)),
            ("MONITOR_TOOL_PINS",lambda d:d["pins"]["driver"].update(sha256="a"*64))):
        f=receipt_fixture(suite,"monitor_"+code,receipt_changes=edit)
        bad(code,lambda f=f:M.close_attempt(f.ctx,f.name,1))
    f=receipt_fixture(suite,"bad_sample_binding",sample={"name":"P1_OTHER"})
    bad("SOLO_SAMPLE_BINDING",lambda:M.close_attempt(f.ctx,f.name,1))
    f=receipt_fixture(suite,"duplicate_twin_stop",name=M.TWIN,origin="KIT")
    for label in ("ONE","TWO"):
        suite.raw_write(f.root/"kit_launch_root"/"twin_kill"/("TWIN_KILL_RECORD_"+label+".json"),
                        M.encoded({"outdir":f.outdir,"launch_json":f.launch_pin,"reason":"ITERATION_0001_COMPLETED_AND_SIDECAR"}))
    bad("TWIN_STOP_NOT_UNIQUE",lambda:M.close_attempt(f.ctx,f.name,1))
    f=receipt_fixture(suite,"already_assembled")
    M.close_attempt(f.ctx,f.name,1)
    M.assemble_registry(f.ctx)
    bad("ASSEMBLY_ALREADY_EXISTS",lambda:M.assemble_registry(f.ctx))
    f=receipt_fixture(suite,"cutoff_refusals")
    terms=[{"name":f.name,"time_utc":"2026-10-20T12:00:00Z","receipt":f.entry_pin}]
    bad("TERMINAL_SET_EMPTY",lambda:M.write_cutoff(f.ctx,[]))
    original_dir=f.ctx.cfg["v006_copy_dir"]
    f.ctx.cfg["v006_copy_dir"]=str(f.root/"missing_copy_dir")
    bad("CUTOFF_COPY_DIR",lambda:M.write_cutoff(f.ctx,terms))
    f.ctx.cfg["v006_copy_dir"]=original_dir
    expected=Path(original_dir)/("V006_CUTOFF_COPY_"+M.sha(f.ctx.v006_raw)+".md")
    suite.raw_write(expected,b"SYNTHETIC_BAD_COPY")
    bad("CUTOFF_COPY_EXISTS_DIFFERENT",lambda:M.write_cutoff(f.ctx,terms))
    f=receipt_fixture(suite,"cutoff_readback_fault")
    expected=Path(f.ctx.cfg["v006_copy_dir"])/("V006_CUTOFF_COPY_"+M.sha(f.ctx.v006_raw)+".md")
    read_bytes=Path.read_bytes
    def readback_fault():
        # Simulate corrupted readback of this local synthetic copy only.
        Path.read_bytes=lambda path: b"SYNTHETIC_READBACK_FAULT" if path==expected else read_bytes(path)
        try:
            fail("CUTOFF_COPY_VERIFY",lambda:M.write_cutoff(f.ctx,terms))
        finally:
            Path.read_bytes=read_bytes
        suite.eq(Path(M.cutoff_path(f.ctx)).exists(),False)
    case("REFUSE_CUTOFF_COPY_VERIFY",readback_fault)

    for code in ("MONITOR_REFUSED_RECORD_BINDING","MONITOR_REFUSED_LAUNCHER","MONITOR_REFUSED_WRITER",
                 "MONITOR_REFUSED_PLAN","MONITOR_REFUSED_ABSENT_PATHS","MONITOR_REFUSED_LOG_PIN_FORM","MONITOR_REFUSED_LOG_PATH"):
        f=receipt_fixture(suite,"old_refusal_"+code)
        work=f.root/"launch_root"/"work"/"old_refusal"
        work.mkdir()
        outdir=M.planned_outdir(f.ctx,f.name,2,"P112")
        plan={"outdir":outdir,"attempt":2,"caps":M.first_caps(f.name),"solo_mode":False}
        if code=="MONITOR_REFUSED_PLAN":
            plan["outdir"]="/synthetic/wrong"
        pp=suite.raw_write(work/"plan.json",M.encoded(plan))
        rec={"schema":"MONITOR_REFUSED_ATTEMPT_RECORD_C2V001","name":f.name,"attempt":2,"launcher":"P112_CX2V001",
             "writer":{"name":M.TOOL_NAME,"sha256":suite.tool_sha},"plan":pp,
             "monitor_stdout":suite.raw_write(work/"monitor.stdout.txt",b"synthetic refusal\n"),
             "monitor_stderr":suite.raw_write(work/"monitor.stderr.txt",b""),"absent":M.absent_paths(outdir),
             "date_u":M.date_u(),"rule":"synthetic"}
        if code=="MONITOR_REFUSED_RECORD_BINDING":rec["attempt"]=3
        if code=="MONITOR_REFUSED_LAUNCHER":rec["launcher"]="KIT_C2V003A"
        if code=="MONITOR_REFUSED_WRITER":rec["writer"]={"name":"ROOT","sha256":None}
        if code=="MONITOR_REFUSED_ABSENT_PATHS":rec["absent"]["outdir"]="/synthetic/wrong"
        if code=="MONITOR_REFUSED_LOG_PIN_FORM":rec["monitor_stdout"]={}
        if code=="MONITOR_REFUSED_LOG_PATH":rec["monitor_stdout"]=pp
        suite.raw_write(f.root/"launch_root"/"launches"/("P112_"+f.name+"_MONITOR_REFUSED_CX2V001_A2.json"),M.encoded(rec))
        bad(code,lambda f=f:M.refusal_records(f.ctx,f.name,f.ctx.records(f.name)))

    for code in ("PLAN_SCHEMA","PLAN_CONFIG_BINDING","PLAN_OUTDIR_BINDING","MONITOR_REFUSED_WORK","MONITOR_STILL_ALIVE"):
        f=receipt_fixture(suite,"refusal_plan_"+code)
        work=f.root/"launch_root"/"work"/"invocation"
        work.mkdir()
        outdir=M.planned_outdir(f.ctx,f.name,2,"P112")
        plan={"schema":"UNT_P112_LAUNCH_PLAN_CX2V001","name":f.name,"attempt":2,"outdir":outdir,
              "config":f.ctx.config_pin,"caps":M.first_caps(f.name)}
        if code=="PLAN_SCHEMA":plan["schema"]="WRONG"
        if code=="PLAN_CONFIG_BINDING":plan["config"]={}
        if code=="PLAN_OUTDIR_BINDING":plan["outdir"]="/synthetic/wrong"
        if code=="MONITOR_STILL_ALIVE":
            f.ctx.system.rows=[{"pid":900001,"ppid":1,"pgid":900001,"command":
                               M.PY+" -I -B "+f.ctx.pins["monitor"]["path"]+" --receipt "+outdir+".receipt.json"}]
        pp=suite.raw_write(work/"plan.json",M.encoded(plan))
        workarg=str(f.root) if code=="MONITOR_REFUSED_WORK" else str(work)
        bad(code,lambda f=f,pp=pp,workarg=workarg:M.record_monitor_refused(f.ctx,pp,workarg))
    f=receipt_fixture(suite,"outside_refusals",origin="KIT",name="S0_J0_SERIAL")
    f.ctx._fixture_calls=[]
    bad("OUTSIDE_STOP_NAME",lambda:M.stop_outside_set(f.ctx,"P1_M0001"))
    bad("OUTSIDE_STOP_NO_RECORD",lambda:M.stop_outside_set(f.ctx,"S0_J2_SERIAL"))
    bad("OUTSIDE_STOP_ATTEMPT",lambda:M.stop_outside_set(f.ctx,f.name,99))
    bad("OUTSIDE_SET_STOP_REQUIRED",lambda:M.assemble_registry(f.ctx))
    f.ctx.get_vpin=lambda kind,name:{"path":f.call["spec"]["path"],"sha256":"a"*64}
    bad("OUTSIDE_STOP_SPEC_PIN",lambda:M.stop_outside_set(f.ctx,f.name))
    for code in ("OUTSIDE_STOP_SCHEMA","OUTSIDE_STOP_MAPPING_PINS"):
        g=receipt_fixture(suite,"outside_record_"+code,origin="KIT",name="S0_J0_SERIAL")
        record={"schema":"WRONG" if code=="OUTSIDE_STOP_SCHEMA" else "S0_OUTSIDE_SET_STOP_RECORD_C2V001",
                "name":g.name,"plan_output_primary":{},"fdplan":g.ctx.cfg["fdplan"]}
        suite.raw_write(g.root/"launch_root"/"outside_set_stop"/(g.name+"_A1_CX2V001.json"),M.encoded(record))
        bad(code,lambda g=g:M.outside_stop_records(g.ctx,g.name))
    jp=suite.fixture("malformed_launch_json_shape.json",[])
    case("REFUSE_LAUNCH_JSON_FORM",lambda:suite.eq(M.try_launch_json(jp["path"]),(None,None)))


"""Process faults are injected; every possible signal is intercepted locally."""


def refusal_process_cases(suite):
    import contextlib
    import io
    import json
    import os
    import types
    from pathlib import Path
    M, case, fail = suite.module, suite.case, suite.refuses
    def bad(code,action):
        case("REFUSE_"+code,lambda:fail(code,action))
    f=receipt_fixture(suite,"resume_missing_states")
    bad("ATTEMPT_ALREADY_RECORDED",lambda:M.launch_resume(f.ctx,f.name,1))
    bad("RESUME_LAUNCH_JSON_MISSING",lambda:M.launch_resume(f.ctx,f.name,2))
    bad("RESUME_ARGUMENTS",lambda:M.launch(f.ctx,f.name,resume=True))
    f=receipt_fixture(suite,"resume_missing_invocation",record=False)
    bad("RESUME_INVOCATION_MISSING",lambda:M.launch_resume(f.ctx,f.name,1))
    f=resume_fixture(suite,"resume_no_command",invocation_changes={"invocation_command":None})
    bad("RESUME_INVOCATION_COMMAND_MISSING",lambda:M.launch_resume(f.ctx,f.name,1))
    f=resume_fixture(suite,"resume_wrong_config")
    f.ctx.config_pin=f.entry_pin
    bad("RESUME_PLAN_BINDING",lambda:M.launch_resume(f.ctx,f.name,1))
    f=resume_fixture(suite,"resume_changed_spec")
    other=suite.fixture("resume_different_spec.json",{"synthetic":True})
    entry=dict(M.read_pin(f.entry_pin),spec=other)
    ep=suite.fixture("resume_different_entry.json",entry)
    f.call.update(spec=other,entry=entry,entry_pin=ep)
    bad("RESUME_SPEC_BINDING",lambda:M.launch_resume(f.ctx,f.name,1))
    f=receipt_fixture(suite,"missing_retry_registry")
    call=dict(f.call,name="P1_M0099")
    bad("RETRY_REGISTRY_ENTRY_MISSING",lambda:M.register_call(
        f.ctx,call,{"attempt":2},f.entry_pin,f.root,{"records":[f.record],"residuals":set(),"refusals":[]}))
    bad("SAMPLER_POLL",lambda:M.sampler(f.ctx,{},str(f.root),poll_s=11))
    bad("SAMPLER_CONFIG_BINDING",lambda:M.sampler(
        f.ctx,{"name":f.name,"attempt":1,"outdir":f.outdir,"config":{}},str(f.root)))
    work=f.root/"launch_root"/"work"/"multiple_monitors"
    work.mkdir()
    command=M.PY+" -I -B "+f.ctx.pins["monitor"]["path"]+" --receipt "+f.outdir+".receipt.json"
    f.ctx.system.rows=[{"pid":900001,"ppid":1,"pgid":900001,"command":command},
                       {"pid":900002,"ppid":1,"pgid":900002,"command":command}]
    bad("MULTIPLE_MONITORS",lambda:M.sampler(
        f.ctx,{"name":f.name,"attempt":1,"outdir":f.outdir,"config":f.ctx.config_pin},str(work)))
    row={"pid":900005,"ppid":1,"pgid":900006,"command":"/synthetic/inert"}
    f.ctx.system.rows=[row]
    bad("NOT_GROUP_LEADER",lambda:M.stop_qualified(f.ctx.system,900005,lambda r:True,group=True))
    row["pgid"]=row["pid"]
    clock=[0.0]
    f.ctx.system.monotonic=lambda:clock[0]
    f.ctx.system.sleep=lambda seconds:clock.__setitem__(0,clock[0]+20)
    kill=M.os.kill
    signals=[]
    def unresponsive():
        M.os.kill=lambda pid,sig:signals.append((pid,int(sig)))
        try:
            fail("PROCESS_STILL_ALIVE_AFTER_STOP",lambda:M.stop_qualified(f.ctx.system,900005,lambda r:True))
        finally:
            M.os.kill=kill
        suite.eq([p for p,sig in signals],[900005,900005])
    case("REFUSE_PROCESS_STILL_ALIVE_AFTER_STOP",unresponsive)
    f=receipt_fixture(suite,"duplicate_watch",name=M.TWIN)
    outdir=f.outdir
    command="/bin/bash "+f.ctx.pins["twin_watch"]["path"]+" --outdir "+outdir
    f.ctx.system.rows=[{"pid":900001,"ppid":1,"pgid":900001,"command":command},
                       {"pid":900002,"ppid":1,"pgid":900002,"command":command}]
    m15=suite.fixture("watch_m15.json",{"date_u_epoch_s":int(M.timestamp(f.rec["utc_start"]))-1})
    plan=dict(f.record,pins={"driver":f.ctx.pins["driver"],"monitor":f.ctx.pins["monitor"]},
              launch_json=outdir+".receipt.json.launch.json",m15_record=m15)
    bad("TWIN_WATCH_DUPLICATE",lambda:M.finish_launch(f.ctx,plan,f.entry_pin,f.entry_pin,900001,900002))
    outdir=M.planned_outdir(f.ctx,f.name,2,"P112")
    plan=dict(plan,attempt=2,outdir=outdir,launch_json=outdir+".receipt.json.launch.json")
    bad("NO_MISLAUNCH_WITHOUT_LAUNCH_JSON",lambda:M.write_launch_record(
        f.ctx,plan,f.entry_pin,f.entry_pin,900001,900002,None,{"parseable":False},snapshot=(None,None)))

    f=full_launch_fixture(suite,"invocation_faults")
    def context():
        c=M.Context(f.config,system=M.SyntheticSystem(M.read_pin(f.synthetic)["system"]),synthetic_pins=f.overrides)
        c.system.processes=lambda:[
            {"pid":os.getpid(),"ppid":1,"pgid":os.getpid(),"command":M.PY+" -I -B /synthetic/fault_test.py"},
            {"pid":900111,"ppid":1,"pgid":900111,"command":M.PY+" -I -B "+f.watch["path"]}]
        return c
    c=context()
    bad("ATTEMPT_NUMBER",lambda:M.launch(c,f.name,attempt=99))
    dry_failure=suite.bytes_fixture("inert_dry_failure.py",b"raise SystemExit(1)\n")
    c.pins["dry_harness"]=dry_failure
    work=f.root/"dry_failure_work"
    work.mkdir()
    bad("DRY_HARNESS_EXIT",lambda:M.run_dry(c,c.call(f.name),work))
    target=f.root/"layout_target"
    target.mkdir()
    (f.root/"launch_root"/"registry").symlink_to(target,target_is_directory=True)
    bad("LAUNCH_SUBDIR_REAL",lambda:M.create_layout(c))
    plan_pin=suite.fixture("wrong_sampler_outdir_plan.json",{"outdir":"/synthetic/other"})
    output=io.StringIO()
    def wrong_sampler_cli():
        with contextlib.redirect_stdout(output):
            result=M.cli(["_sampler","--config",f.config["path"],"--config-sha256",f.config["sha256"],
                          "--synthetic-pins",f.synthetic["path"],"--synthetic-pins-sha256",f.synthetic["sha256"],
                          "--plan",plan_pin["path"],"--plan-sha256",plan_pin["sha256"],"--outdir","/synthetic/NGC_RUN"])
        suite.eq((result,json.loads(output.getvalue())["code"]),(2,"SAMPLER_OUTDIR"))
    case("REFUSE_SAMPLER_OUTDIR",wrong_sampler_cli)
    for missing in (True,False):
        code="SAMPLER_FIRST_SAMPLE_MISSING" if missing else "SAMPLER_FIRST_SAMPLE_FAILED"
        g=full_launch_fixture(suite,"first_sample_"+code)
        c=M.Context(g.config,system=M.SyntheticSystem(M.read_pin(g.synthetic)["system"]),synthetic_pins=g.overrides)
        c.synthetic_pin=g.synthetic
        clock=[0.0]
        c.system.monotonic=lambda:clock[0]
        c.system.sleep=lambda seconds:clock.__setitem__(0,clock[0]+max(seconds,1))
        c.system.processes=lambda:[
            {"pid":os.getpid(),"ppid":1,"pgid":os.getpid(),"command":M.PY+" -I -B /synthetic/fault_test.py"},
            {"pid":900111,"ppid":1,"pgid":900111,"command":M.PY+" -I -B "+g.watch["path"]}]
        original_popen=M.subprocess.Popen
        def fake_sampler(argv,*args,**kwargs):
            if "_sampler" not in argv:
                return original_popen(argv,*args,**kwargs)
            if not missing:
                pp=Path(argv[argv.index("--plan")+1])
                suite.raw_write(pp.parent/"sampler_first_sample.json",M.encoded({"ok":False}))
            return types.SimpleNamespace(pid=900222)
        def launch_fault():
            M.subprocess.Popen=fake_sampler
            try:
                fail(code,lambda:M.launch(c,g.name))
            finally:
                M.subprocess.Popen=original_popen
            suite.eq(list(Path(c.cfg["run_root"]).iterdir()),[])
        case("REFUSE_"+code,launch_fault)
    suite.interfaces["process_fault_injection"] = (
        "TESTED malformed saved invocation states and injected sampler/process failures. "
        "The unresponsive-process test intercepts both signals; it signals no OS process. "
        "Missing/failed first-sample tests replace only sampler Popen, before any monitor start.")


ALL_GROUPS = ["core_cases","theta_cases","process_cases","close_cases","history_cases","sampler_cases",
              "boundary_cases","live_launch_cases","resume_cases","stop_cases","outside_interface_cases",
              "mutation_cases","recovery_live_cases","contract_gap_cases","refusal_input_cases",
              "refusal_mapping_cases","refusal_custody_cases","refusal_process_cases"]


def main():
    ap=argparse.ArgumentParser(description="Synthetic-only P112 contract tests; no production launch.")
    ap.add_argument("--tool",required=True)
    ap.add_argument("--tool-sha256",required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--run-stamp",required=True)
    ap.add_argument("--run-stamp-sha256",required=True)
    a=ap.parse_args()
    started=subprocess.check_output(["/bin/date","-u"],env=dict(os.environ,LC_ALL="C"),text=True).strip()
    stamp_raw=Path(a.run_stamp).read_bytes()
    if hash_bytes(stamp_raw)!=a.run_stamp_sha256:
        raise ValueError("run stamp pin mismatch")
    stamp=json.loads(stamp_raw)
    suite=Suite(a.tool,a.out,a.tool_sha256)
    for group in ALL_GROUPS:
        try:
            globals()[group](suite)
        except Exception as error:
            suite.rows.append({"name":"GROUP_"+group,"status":"FAIL","detail":repr(error),
                               "trace":traceback.format_exc(limit=5)})
    codes=set()
    for node in ast.walk(ast.parse(suite.tool_path.read_text())):
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Name):
            index=1 if node.func.id=="need" else 0 if node.func.id=="Refusal" else None
            if index is not None and len(node.args)>index:
                for arg in ast.walk(node.args[index]):
                    if isinstance(arg,ast.Constant) and isinstance(arg.value,str):codes.add(arg.value)
    missing=sorted(codes-set(suite.refusals))
    suite.case("EVERY_NAMED_REFUSAL_EXERCISED",lambda:suite.eq(missing,[]))
    record={"schema":"P112_TEST_RECORD_CX2V002","date_u":stamp["date_u"],
            "date_u_meaning":"Common actual suite-start date -u; each execution has separate date -u metadata.",
            "tool_sha256":suite.tool_sha,"test_sha256":hash_bytes(Path(__file__).read_bytes()),
            "run_stamp_sha256":a.run_stamp_sha256,"cases":suite.rows,"interfaces":suite.interfaces,
            "refusal_coverage":{code:sorted(names) for code,names in sorted(suite.refusals.items())},
            "refusal_not_exercised":missing}
    pin=exclusive(suite.root/"TEST_RECORD.json",suite.module.encoded(record))
    finished=subprocess.check_output(["/bin/date","-u"],env=dict(os.environ,LC_ALL="C"),text=True).strip()
    execution={"schema":"P112_TEST_EXECUTION_CX2V002","date_u":finished,"started_date_u":started,
               "tool":{"path":str(suite.tool_path),"sha256":suite.tool_sha},
               "tests":{"path":str(Path(__file__).resolve()),"sha256":record["test_sha256"]},
               "test_record":pin,"fixture_root":str(suite.root)}
    exclusive(suite.root/"EXECUTION_METADATA.json",suite.module.encoded(execution))
    failures=[r for r in suite.rows if r["status"]!="PASS"]
    print(json.dumps({"tested":len(suite.rows),"failed":len(failures),"failures":failures,
                      "refusal_missing":missing,"record":pin}))
    return 1 if failures else 0


if __name__=="__main__":
    raise SystemExit(main())

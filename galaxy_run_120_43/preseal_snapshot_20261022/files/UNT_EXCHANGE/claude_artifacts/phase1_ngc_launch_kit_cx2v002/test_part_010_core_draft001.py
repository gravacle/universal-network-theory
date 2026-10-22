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
    line = "TOOL_PIN P112_LAUNCHER_CX2V001 " + own["sha256"] + " " + own["path"]
    good = "## A999: synthetic\n" + line + "\n"
    case("L01_missing", lambda: fail("TOOL_PIN_MISSING", lambda: M.tool_gate("## A999: none\n", own)))
    case("L02_sha", lambda: fail("TOOL_PIN_MISMATCH", lambda: M.tool_gate(good.replace(own["sha256"], "0" * 64), own)))
    case("L02_path", lambda: fail("TOOL_PIN_MISMATCH", lambda: M.tool_gate(good.replace(own["path"], "/different"), own)))
    case("L03_duplicate", lambda: fail("TOOL_PIN_DUPLICATE", lambda: M.tool_gate(good + line + "\n", own)))
    case("L05_successor_ignored", lambda: suite.eq(M.tool_gate(good + line.replace("CX2V001", "CX2V002") + "\n", own), own))
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

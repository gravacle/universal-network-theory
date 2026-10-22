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
        suite.write_refusal_fixture(path, rec)
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

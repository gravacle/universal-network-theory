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

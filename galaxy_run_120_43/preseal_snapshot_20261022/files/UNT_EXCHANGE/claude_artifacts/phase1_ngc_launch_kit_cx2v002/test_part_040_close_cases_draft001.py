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

"""All changed metadata-read sites and null monitor-PID liveness."""


def metadata_boundary_cases(suite):
    import os
    import types
    from pathlib import Path
    M = suite.module
    for leaf in ("plan.json", "invocation.json", "monitor_pid.json"):
        f = resume_fixture(suite, "F1_resume_" + leaf, alias_record=leaf)
        suite.case("F1_resume_alias_" + leaf, lambda f=f:
                   suite.refuses("RECORD_SYMLINK", lambda: M.launch_resume(f.ctx, f.name, 1)))

    for leaf in ("monitor_pid.json", "invocation.json", "receipt"):
        f = receipt_fixture(suite, "F1_sampler_" + leaf, no_receipt=leaf == "receipt")
        work = f.root / "launch_root" / "work" / "alias"
        work.mkdir()
        k = 1 if leaf == "receipt" else 2
        outdir = M.planned_outdir(f.ctx, f.name, k, "P112")
        if leaf == "receipt":
            target = suite.raw_write(work / "plain_receipt.json", M.encoded(f.rec))
            Path(outdir + ".receipt.json").symlink_to(target["path"])
        else:
            target = suite.raw_write(work / "plain_metadata.json", M.encoded(
                {"monitor_pid": 900991} if leaf == "monitor_pid.json" else
                {"invocation_pid": 900991, "invocation_command": "synthetic ended invocation"}))
            (work / leaf).symlink_to(target["path"])
        clock = [0.0]
        f.ctx.system.monotonic = lambda clock=clock: clock[0]
        f.ctx.system.sleep = lambda seconds, clock=clock: clock.__setitem__(0, clock[0] + seconds)
        plan = {"name": f.name, "attempt": k, "outdir": outdir, "config": f.ctx.config_pin}
        suite.case("F1_sampler_alias_" + leaf, lambda f=f, plan=plan, work=work:
                   suite.refuses("RECORD_SYMLINK", lambda: M.sampler(f.ctx, plan, str(work), poll_s=1)))

    def first_sample_alias():
        f = full_launch_fixture(suite, "F1_first_sample")
        ctx = M.Context(f.config, system=M.SyntheticSystem(M.read_pin(f.synthetic)["system"]),
                        synthetic_pins=f.overrides)
        ctx.synthetic_pin = f.synthetic
        ctx.system.processes = lambda: [
            {"pid": os.getpid(), "ppid": 1, "pgid": os.getpid(), "command": M.PY + " -I -B /synthetic/test.py"},
            {"pid": 900111, "ppid": 1, "pgid": 900111, "command": M.PY + " -I -B " + f.watch["path"]}]
        original = M.subprocess.Popen
        starts = []
        def popen(argv, *args, **kwargs):
            if "_sampler" in argv:
                path = Path(argv[argv.index("--plan") + 1]).parent
                pin = suite.raw_write(path / "plain_first_sample.json", M.encoded({"ok": True, "monotonic": 0}))
                (path / "sampler_first_sample.json").symlink_to(pin["path"])
                return types.SimpleNamespace(pid=900222)
            if argv[0] == "/usr/bin/nohup":
                starts.append(argv)
                raise AssertionError("monitor started despite first-sample alias")
            return original(argv, *args, **kwargs)
        M.subprocess.Popen = popen
        try:
            suite.refuses("RECORD_SYMLINK", lambda: M.launch(ctx, f.name))
        finally:
            M.subprocess.Popen = original
        suite.eq(starts, [])
    suite.case("F1_first_sample_alias_refuses_before_monitor", first_sample_alias)

    f = receipt_fixture(suite, "F3_null_pid_live", no_receipt=True, record=False)
    record = dict(f.record, monitor_pid=None, solo_mode=True)
    suite.raw_write(f.record_path, M.encoded(record))
    command = M.PY + " -I -B " + f.ctx.pins["monitor"]["path"] + " --receipt " + f.outdir + ".receipt.json"
    f.ctx.system.rows = [{"pid": 900994, "ppid": 1, "pgid": 900994, "command": command}]
    suite.case("F3_null_pid_status_live_by_command", lambda:
               suite.eq(M.status(f.ctx)["calls"][0]["status"], "ATTEMPT_ACTIVE"))
    suite.case("F3_null_pid_close_live_by_command", lambda:
               suite.refuses("MONITOR_RECEIPT_MISSING", lambda: M.close_attempt(f.ctx, f.name, 1)))
    suite.case("F3_null_pid_solo_live_by_command", lambda:
               suite.refuses("SOLO_RERUN_ACTIVE", lambda: M.enforce_solo(f.ctx, False)))


def parsed_certificate_mutation_case(suite):
    import types
    probe = successor_probes()["CLEANUP_fill_single_read_MUST_PASS"]
    def action():
        def child(label, module):
            obj = object.__new__(type(suite))
            obj.__dict__ = dict(suite.__dict__)
            obj.root = suite.root / ("parsed_certificate_" + label)
            obj.root.mkdir()
            obj.module, obj.rows, obj.interfaces = module, [], {}
            return obj
        probe(child("control", suite.module))
        source = suite.tool_path.read_text()
        old = "obj = certificate_docs[certificate]"
        new = 'obj = strict_json(Path(cfg[certificate]["path"]).read_bytes())'
        suite.eq(source.count(old), 1)
        source = source.replace(old, new)
        module = types.ModuleType("_p112_certificate_reread_mutant")
        module.__file__ = str(suite.tool_path)
        exec(compile(source, str(suite.tool_path), "exec"), module.__dict__)
        failure = None
        try:
            probe(child("mutant", module))
        except Exception as error:
            failure = type(error).__name__
        suite.eq(failure is not None, True)
        suite.interfaces["parsed_certificate_restoring_mutant"] = {
            "control": "PASS", "status": "KILLED", "source_sha256": suite.module.sha(source.encode()),
            "replace": old, "with": new, "detection": failure, "imported": True}
    suite.case("CX2V002_MUTANT_cleanup_certificate_reread", action)

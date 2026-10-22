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
    trial("unanchored_tool_pin", "tool_gate", 'for line in text.split("\\n"):',
          'for line in text.split("\\n"):\n        line = line[line.find("TOOL_PIN "):] if "TOOL_PIN " in line else line',
          unanchored_tool_probe)
    trial("unanchored_residual", "residual_lines", 'for line in text.split("\\n"):',
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
        s.write_refusal_fixture(f.root / "launch_root" / "launches" / ("P112_%s_MONITOR_REFUSED_CX2V001_A1.json" % f.name), rec)
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

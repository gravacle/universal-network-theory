"""0789 regressions on synthetic states; mutations are imported in memory."""


def v003_probes():
    import contextlib
    import copy
    import os
    import sys
    import types
    from pathlib import Path

    @contextlib.contextmanager
    def forbid_opens(paths):
        watched = {str(p) for p in paths}
        state = {"active": True, "opens": 0}
        def audit(event, args):
            if state["active"] and event == "open" and str(args[0]) in watched:
                state["opens"] += 1
                raise AssertionError("forbidden fixture open")
        sys.addaudithook(audit)
        try:
            yield state
        finally:
            state["active"] = False

    def decoy(s, persistent=True, publish_pid=True):
        M = s.module
        f = receipt_fixture(s, "v003_decoy_%s_%s" % (persistent, publish_pid))
        work = f.root / "launch_root" / "work" / "decoy"
        work.mkdir()
        argv = M.monitor_command(f.ctx.pins, f.call["spec"], f.outdir, f.record["caps"])
        plan = {"name": f.name, "attempt": 1, "outdir": f.outdir,
                "config": f.ctx.config_pin, "monitor_argv": argv}
        clock, pid_written = [0.0], [False]
        f.ctx.system.monotonic = lambda: clock[0]
        f.ctx.system.sleep = lambda seconds: clock.__setitem__(0, clock[0] + seconds)
        def rows():
            if clock[0] > 20:
                raise AssertionError("sampler failed to finish with decoy")
            if publish_pid and clock[0] >= 1 and not pid_written[0]:
                s.raw_write(work / "monitor_pid.json", M.encoded({"monitor_pid": 990001}))
                pid_written[0] = True
            result = []
            if clock[0] < 5:
                result.append({"pid": 990001, "ppid": 1, "pgid": 990001, "command": " ".join(argv)})
            if persistent or clock[0] < 1:
                result.append({"pid": 990002, "ppid": 1, "pgid": 990002,
                               "command": "/usr/bin/pgrep -f " + f.ctx.pins["monitor"]["path"] +
                               " --receipt " + f.outdir + ".receipt.json"})
            return result
        f.ctx.system.processes = rows
        old_utc = M.utc
        start = M.timestamp(f.rec["utc_start"])
        M.utc = lambda: M.dt.datetime.fromtimestamp(start - 2 + clock[0], M.dt.timezone.utc).isoformat().replace("+00:00", "Z")
        try:
            with SuccessorAudit(s) as audit:
                pin = M.sampler(f.ctx, plan, str(work), poll_s=1)
            audit.once()
        finally:
            M.utc = old_utc
        sample = M.read_pin(pin)
        s.eq(sample["complete"], True)
        s.eq(M.sample_value(sample, f.rec), 0)
        s.eq(sample["monitor_receipt"], M.read_record(f.outdir + ".receipt.json")[0])

    def monitor_identity_form(s):
        M = s.module
        f = receipt_fixture(s, "v003_monitor_identity")
        work = f.root / "launch_root" / "work" / "bad_identity"
        work.mkdir()
        s.raw_write(work / "monitor_pid.json", M.encoded({"monitor_pid": "990001"}))
        plan = {"name": f.name, "attempt": 1, "outdir": f.outdir, "config": f.ctx.config_pin}
        s.refuses("MONITOR_PID_FORM", lambda: M.sampler(f.ctx, plan, str(work)))

    def exact_liveness(s):
        M = s.module
        for real in (False, True):
            f = resume_fixture(s, "v003_exact_" + str(real), missing_monitor_pid=True)
            exact = " ".join(f.plan["monitor_argv"])
            decoy = "/usr/bin/pgrep -f " + f.ctx.pins["monitor"]["path"] + " --receipt " + f.outdir + ".receipt.json"
            rows = [{"pid": 990002, "ppid": 1, "pgid": 990002, "command": decoy},
                    {"pid": 990003, "ppid": 1, "pgid": 990004, "command": exact}]
            if real:
                rows.append({"pid": 990001, "ppid": 1, "pgid": 990001, "command": exact})
            f.ctx.system.rows = rows
            got = M.live_monitor(rows, None, f.ctx.pins["monitor"]["path"], f.outdir, argv=f.plan["monitor_argv"])
            s.eq(got["pid"] if got else None, 990001 if real else None)
            doc = M.read_pin(M.launch_resume(f.ctx, f.name, 1))
            s.eq(doc["monitor_pid"], 990001 if real else None)
            s.eq(doc["monitor_pid_source"], "command_line" if real else "no_live_match")
        f = receipt_fixture(s, "v003_null_decoy", no_receipt=True, record=False)
        record = dict(f.record, monitor_pid=None, solo_mode=True)
        s.raw_write(f.record_path, M.encoded(record))
        f.ctx.system.rows = [{"pid": 990002, "ppid": 1, "pgid": 990002,
                             "command": "/usr/bin/pgrep -f " + f.ctx.pins["monitor"]["path"] +
                             " --receipt " + f.outdir + ".receipt.json"}]
        s.eq(M.status(f.ctx)["calls"][0]["status"], "MONITOR_ENDED_NO_RECEIPT")
        s.refuses("MONITOR_ENDED_NO_RECEIPT", lambda: M.close_attempt(f.ctx, f.name, 1))
        M.enforce_solo(f.ctx, False)

    def blank_ps(s):
        M = s.module
        rows = M.parse_ps("990001 1 990001   \n990002 1 990002 /bin/sleep 1\n")
        s.eq(rows[0]["command"], "")
        s.eq(M.command_argv(rows[0]), [])
        s.eq(M.ProcessCounter(declared=[], synthetic=True).count(rows), [])

    def regular_identity(s):
        M = s.module
        listed = s.bytes_fixture("v003_listed.py", b"# synthetic listed file\n")
        duplicate = s.bytes_fixture("v003_copy.py", b"# synthetic listed file\n")
        fifo = s.root / "v003_fifo.py"
        os.mkfifo(fifo)
        sparse = s.root / "v003_oversized.py"
        with sparse.open("xb") as stream:
            stream.truncate(M.PROCESS_IDENTITY_MAX_BYTES + 1)
        declared = [{"tool": "synthetic", **listed, "driver_only": False}]
        counter = M.ProcessCounter(declared=declared, synthetic=True)
        s.eq(counter.identify(duplicate["path"]), declared[0])
        with forbid_opens([fifo, sparse]) as audit:
            s.eq(counter.identify(str(fifo)), None)
            s.eq(counter.identify(str(sparse)), None)
        s.eq(audit["opens"], 0)

    def whitespace(s):
        M = s.module
        pin = s.bytes_fixture("v003_token_tool.py", b"# synthetic token fixture\n")
        declared = [{"tool": "synthetic", **pin, "driver_only": False}]
        row = {"pid": 990001, "ppid": 1, "pgid": 990001,
               "command": "/bin/echo it's " + pin["path"] + " lane's"}
        s.eq(M.command_argv(row), row["command"].split())
        s.eq(len(M.ProcessCounter(declared=declared, synthetic=True).count([row])), 1)

    def kit(s, variant):
        M = s.module
        f = receipt_fixture(s, "v003_kit_" + variant)
        plan = {"name": f.name, "launch_json": f.outdir + ".receipt.json.launch.json",
                "spec": f.call["spec"], "outdir": f.outdir}
        lj = M.read_record(plan["launch_json"])[1]
        exact = " ".join(M.driver_command(f.ctx.pins, plan["spec"], f.outdir))
        if variant == "child_alive":
            f.ctx.system.rows = [{"pid": lj["child_pid"], "ppid": 1, "pgid": lj["child_pid"], "command": "/bin/sleep 10"}]
        elif variant == "command_alive":
            f.ctx.system.rows = [{"pid": 990099, "ppid": 1, "pgid": 990099, "command": exact}]
        else:
            f.ctx.system.rows = []
        old = M.subprocess.run
        calls = []
        def run(argv, **kwargs):
            calls.append(kwargs)
            if variant == "timeout":
                s.eq(kwargs.get("timeout"), M.KIT_KILL_TARGET_TIMEOUT_S)
                raise M.subprocess.TimeoutExpired(argv, kwargs["timeout"])
            s.eq(kwargs.get("text", False), False)
            return types.SimpleNamespace(returncode=1, stdout=b"",
                stderr=b'\xff{"alive":false}' if variant == "bad_utf8" else b'{"alive":false}')
        M.subprocess.run = run
        try:
            got = M.kit_kill_target(f.ctx, plan)["result"]
        finally:
            M.subprocess.run = old
        s.eq(got, "ALREADY_ENDED" if variant == "ended" else "NOT_KILLED_TARGET_REFUSED")
        s.eq(len(calls), 1)

    def launch_shape(s):
        M = s.module
        s.refuses("LAUNCH_JSON_FORM", lambda: M.validate_launch_json([]))
        for bad in ({"pins": [1]}, {"caps": [1]}, {"utc": 5}, {"child_pid": "7"},
                    {"command": [1]}, {"pins": {"driver": []}}, {"caps": {"rss_cap_bytes": "1"}}):
            s.refuses("LAUNCH_JSON_FIELD_FORM", lambda bad=bad: M.validate_launch_json(bad))
        f = resume_fixture(s, "v003_shape_resume")
        with successor_swap(f.outdir + ".receipt.json.launch.json",
                            lambda raw, n: b'{"pins":[1],"caps":[1],"utc":5,"child_pid":7}\n', switch_at=1):
            s.refuses("LAUNCH_JSON_FIELD_FORM", lambda: M.launch_resume(f.ctx, f.name, 1))
        f = receipt_fixture(s, "v003_shape_close")
        with successor_swap(f.outdir + ".receipt.json.launch.json", lambda raw, n: b"[]\n", switch_at=1):
            s.refuses("LAUNCH_JSON_FORM", lambda: M.close_attempt(f.ctx, f.name, 1))

    def orphan(s):
        M = s.module
        f = observation_refusal_fixture(s, "v003_orphan", variant="emit")
        original = f.ctx.write
        def crashing(path, obj):
            if str(path).endswith("_A2.json"):
                raise OSError("synthetic interruption between sibling and parent")
            return original(path, obj)
        f.ctx.write = crashing
        try:
            try:
                M.record_monitor_refused(f.ctx, f.refusal_plan, str(f.refusal_work))
            except OSError:
                pass
            else:
                raise AssertionError("interruption not exercised")
        finally:
            f.ctx.write = original
        parent = Path(f.ctx.cfg["p112_launch_root"]) / "launches" / ("P112_" + f.name + "_MONITOR_REFUSED_CX2V001_A2.json")
        sibling = Path(str(parent) + ".observations.json")
        before = sibling.read_bytes()
        s.eq(parent.exists(), False)
        s.eq(M.status(f.ctx)["calls"][0]["status"], "ORPHAN_OBSERVATIONS_SIBLING")
        s.refuses("ORPHAN_OBSERVATIONS_SIBLING", lambda: M.record_monitor_refused(f.ctx, f.refusal_plan, str(f.refusal_work)))
        s.eq(sibling.read_bytes(), before)

    def hardlinks(s):
        M = s.module
        f = receipt_fixture(s, "v003_hardlinks", no_receipt=True)
        target = Path(f.outdir) / "result.json"
        receipt = Path(f.outdir + ".receipt.json")
        os.link(target, receipt)
        launch = Path(M.planned_outdir(f.ctx, f.name, 2, "P112") + ".receipt.json.launch.json")
        os.link(target, launch)
        with forbid_opens([target, receipt, launch]) as audit:
            s.eq(M.status(f.ctx)["calls"][0]["status"], "RECORD_NLINK")
            s.refuses("RECORD_NLINK", lambda: M.try_launch_json(launch))
        s.eq(audit["opens"], 0)
        g = receipt_fixture(s, "v003_cutoff_hardlink")
        raw = Path(g.ctx.cfg["v006"]).read_bytes()
        harmless = s.bytes_fixture("v003_cutoff_source.md", raw)
        copy_path = Path(g.ctx.cfg["v006_copy_dir"]) / ("V006_CUTOFF_COPY_" + M.sha(raw) + ".md")
        os.link(harmless["path"], copy_path)
        with forbid_opens([copy_path]) as audit:
            s.refuses("RECORD_NLINK", lambda: M.write_cutoff(g.ctx, [
                {"name": g.name, "time_utc": g.rec["utc_end"], "receipt": g.entry_pin, "disposition": "FINISHED"}]))
        s.eq(audit["opens"], 0)

    def s0_realpaths(s):
        M = s.module
        f = full_launch_fixture(s, "v003_s0_realpaths")
        for key in ("launch_root", "run_root"):
            config = copy.deepcopy(f.config_doc)
            original = Path(config["s0"][key])
            alias = f.root / ("s0_alias_" + key)
            alias.symlink_to(original, target_is_directory=True)
            config["s0"][key] = str(alias)
            pin = s.fixture("v003_config_" + key + ".json", config)
            s.refuses("CONFIG_SYMLINK", lambda pin=pin: M.Context(
                pin, system=M.SyntheticSystem(M.read_pin(f.synthetic)["system"]), synthetic_pins=f.overrides))

    def sample_receipt(s):
        M = s.module
        for label, value in (("missing", None), ("wrong", {"path": "/synthetic/other", "sha256": "0" * 64})):
            f = receipt_fixture(s, "v003_sample_" + label, sample={"monitor_receipt": value})
            s.refuses("SOLO_SAMPLE_MONITOR_RECEIPT", lambda: M.close_attempt(f.ctx, f.name, 1))
        f = receipt_fixture(s, "v003_sample_correct", sample={})
        s.eq(M.read_pin(M.close_attempt(f.ctx, f.name, 1)["receipt"])["other_ngc_processes_max"], 0)

    def dead_fields(s):
        import inspect
        s.eq(hasattr(s.module, "IMPLEMENTATION_REVISION"), False)
        s.eq("v006_gate_observation" in inspect.unwrap(s.module.Context.__init__).__code__.co_names, False)

    return {
        "V1_transient_decoy_MUST_PASS": lambda s: decoy(s, persistent=False),
        "V1_persistent_decoy_MUST_PASS": decoy,
        "V1_exact_before_pid_MUST_PASS": lambda s: decoy(s, publish_pid=False),
        "V1_monitor_identity_form": monitor_identity_form,
        "Fa_exact_resume_and_null_pid": exact_liveness,
        "Fb_blank_argv": blank_ps,
        "Fc_regular_bounded_identity": regular_identity,
        "Fd_whitespace_tokens": whitespace,
        "Fe_child_pid_alive": lambda s: kit(s, "child_alive"),
        "Fe_planned_command_alive": lambda s: kit(s, "command_alive"),
        "Fe_non_UTF8_stderr": lambda s: kit(s, "bad_utf8"),
        "Fe_timeout": lambda s: kit(s, "timeout"),
        "Fe_ended_after_ps_check": lambda s: kit(s, "ended"),
        "A15_launch_json_shape": launch_shape,
        "A06_orphan_status_and_retry": orphan,
        "A10_record_and_cutoff_hardlinks": hardlinks,
        "Lens1_s0_realpaths": s0_realpaths,
        "Lens1_sample_receipt_pin": sample_receipt,
        "Lens1_remove_dead_fields": dead_fields,
    }


def v003_regression_cases(suite):
    v003_documentation_cases(suite)
    for name, probe in v003_probes().items():
        suite.case("CX2V003_" + name, lambda probe=probe: probe(suite))


def v003_mutation_cases(suite):
    import ast
    import types
    source = suite.tool_path.read_text()
    probes = v003_probes()
    rows = []
    def child(label, module):
        obj = object.__new__(type(suite))
        obj.__dict__ = dict(suite.__dict__)
        obj.root = suite.root / ("v003_mutation_" + label)
        obj.root.mkdir()
        obj.module, obj.rows, obj.interfaces = module, [], {}
        return obj
    def trial(name, old, new, probe_name):
        def action():
            probe = probes[probe_name]
            probe(child(name + "_control", suite.module))
            suite.eq(source.count(old), 1)
            changed = source.replace(old, new, 1)
            module = types.ModuleType("_v003_mutant_" + name)
            module.__file__ = str(suite.tool_path)
            exec(compile(changed, str(suite.tool_path), "exec"), module.__dict__)
            failure = None
            try:
                probe(child(name + "_mutant", module))
            except Exception as error:
                failure = type(error).__name__
            suite.eq(failure is not None, True)
            rows.append({"name": name, "control": "PASS", "status": "KILLED",
                         "source_sha256": suite.module.sha(changed.encode()), "detection": failure,
                         "replace": old, "with": new, "imported": True})
        suite.case("CX2V003_MUTANT_" + name, action)

    start = source.index("        if monitor_identity is None and mp.exists():")
    end = source.index("        seen_monitor = seen_monitor or bool(mons)", start)
    trial("V1_restore_broad_sampler_and_raise", source[start:end],
          '        mons = matching_monitors(rows, ctx.pins["monitor"]["path"], outdir)\n'
          '        need(len(mons) <= 1, "MULTIPLE_MONITORS")\n', "V1_persistent_decoy_MUST_PASS")
    trial("V1_reread_monitor_identity",
          "if monitor_identity is None and mp.exists():\n            _, monitor_identity = read_record(mp)",
          "if mp.exists():\n            monitor_identity = strict_json(Path(mp).read_bytes())",
          "V1_persistent_decoy_MUST_PASS")
    trial("Fa_null_pid_broad_match", "matches = exact_monitor_matches(rows, argv)",
          "matches = matching_monitors(rows, monitor, outdir)", "Fa_exact_resume_and_null_pid")
    trial("Fa_resume_broad_match", 'matches = exact_monitor_matches(rows, plan.get("monitor_argv"))',
          'matches = matching_monitors(rows, ctx.pins["monitor"]["path"], outdir)', "Fa_exact_resume_and_null_pid")
    trial("Fa_ignore_process_group", 'row.get("pgid") == row["pid"] and row.get("command") == command',
          'row.get("command") == command', "Fa_exact_resume_and_null_pid")
    trial("Fb_reject_blank_argv", "len(parts) in (3, 4)", "len(parts) == 4", "Fb_blank_argv")
    tree = ast.parse(source)
    method = next(n for c in tree.body if isinstance(c, ast.ClassDef) and c.name == "ProcessCounter"
                  for n in c.body if isinstance(n, ast.FunctionDef) and n.name == "identify")
    old_identify = "\n".join(source.splitlines()[method.lineno - 1:method.end_lineno])
    trial("Fc_restore_unbounded_identity", old_identify, '''    def identify(self, path):
        if not os.path.isabs(path) or not path.endswith((".py", ".sh")):
            return None
        guard_read(path)
        return self.by_sha.get(sha(Path(path).read_bytes()))''', "Fc_regular_bounded_identity")
    trial("Fd_restore_shlex", 'return row["command"].split()',
          'return __import__("shlex").split(row["command"])', "Fd_whitespace_tokens")
    trial("Fe_ignore_child_pid", 'r["pid"] == child_pid or r["command"] == command',
          'r["command"] == command', "Fe_child_pid_alive")
    trial("Fe_ignore_planned_command", 'r["pid"] == child_pid or r["command"] == command',
          'r["pid"] == child_pid', "Fe_planned_command_alive")
    trial("Fe_restore_text_stderr", "capture_output=True, timeout=KIT_KILL_TARGET_TIMEOUT_S",
          "capture_output=True, text=True, timeout=KIT_KILL_TARGET_TIMEOUT_S", "Fe_non_UTF8_stderr")
    trial("Fe_remove_timeout", "capture_output=True, timeout=KIT_KILL_TARGET_TIMEOUT_S",
          "capture_output=True", "Fe_timeout")
    trial("A15_skip_shape_validation", '    need(type(lj) is dict, "LAUNCH_JSON_FORM")\n    types =',
          '    return lj\n    types =', "A15_launch_json_shape")
    trial("A06_ignore_orphan_status", 'need(os.path.lexists(parent), "ORPHAN_OBSERVATIONS_SIBLING", str(sibling))',
          "pass", "A06_orphan_status_and_retry")
    trial("A06_retry_orphan_write", 'need(not os.path.lexists(path + ".observations.json"), "ORPHAN_OBSERVATIONS_SIBLING", path)',
          "pass", "A06_orphan_status_and_retry")
    trial("A10_allow_hardlinks", 'need(os.stat(path).st_nlink == 1, "RECORD_NLINK", path)',
          "pass", "A10_record_and_cutoff_hardlinks")
    trial("Lens1_s0_alias", 'need(os.path.realpath(c["s0"][key]) == c["s0"][key], "CONFIG_SYMLINK", "s0." + key)',
          "pass", "Lens1_s0_realpaths")
    trial("Lens1_ignore_sample_receipt", 'need(sample.get("monitor_receipt") == receipt_pin, "SOLO_SAMPLE_MONITOR_RECEIPT")',
          "pass", "Lens1_sample_receipt_pin")
    trial("Lens1_restore_dead_revision", 'TOOL_NAME = "P112_LAUNCHER_CX2V003"',
          'IMPLEMENTATION_REVISION = 3\nTOOL_NAME = "P112_LAUNCHER_CX2V003"', "Lens1_remove_dead_fields")
    trial("Lens1_restore_dead_observation", 'self.v006_text = self.v006_raw.decode()',
          'self.v006_text = self.v006_raw.decode()\n        self.v006_gate_observation = None', "Lens1_remove_dead_fields")
    suite.interfaces["cx2v003_restoring_mutants"] = rows
    v003_documentation_mutants(suite)

"""0784/0785 regressions. All fixtures are synthetic and exclusively created."""


class SuccessorAudit:
    """In-process open audit; child executable reads are disclosed separately."""
    def __init__(self, suite):
        import sys
        self.suite, self.active, self.reads = suite, False, []
        sys.addaudithook(self.hook)

    def hook(self, event, args):
        import os
        import sys
        from pathlib import Path
        if not self.active or event != "open" or not isinstance(args[0], (str, bytes)):
            return
        mode = args[1]
        if isinstance(mode, str) and not ("r" in mode or "+" in mode):
            return
        if mode is None and args[2] & (os.O_WRONLY | os.O_RDWR):
            return
        frame, names, ours = sys._getframe(1), [], False
        while frame is not None:
            if frame.f_code.co_filename == str(self.suite.tool_path):
                ours = True
                names.append(frame.f_code.co_name)
            frame = frame.f_back
        if not ours:
            return
        path = os.fsdecode(args[0])
        real = os.path.realpath(path)
        for spelling in (path, real):
            parts = [x.lower() for x in Path(spelling).parts]
            forbidden = (
                any(x in parts for x in ("v007_postseal_records", "a_side", "runs_ext", "stages", ".codex"))
                or any("ngc3198" in x for x in parts)
                or Path(spelling).name.lower() in ("result.json", "finish.json", "progress.jsonl")
                or spelling.endswith((".receipt.json.stdout.txt", ".receipt.json.stderr.txt"))
                or any(x.startswith("ngc_p1_") and "_run_" in x for x in parts[:-1])
            )
            if forbidden:
                raise AssertionError(("forbidden open", spelling))
        if os.path.isdir(path):
            # write_x_bytes opens parent directories solely for fsync. No
            # pinned file bytes are read by these directory handles.
            return
        self.reads.append({"path": path, "realpath": real, "volatile": "observe_file" in names,
                           "counter": "identify" in names})

    def __enter__(self):
        self.active = True
        return self

    def __exit__(self, *unused):
        self.active = False

    def once(self):
        from collections import Counter
        rows = [r for r in self.reads if not r["volatile"] and not r["counter"]
                and r["path"] != str(self.suite.tool_path)]
        for key in ("path", "realpath"):
            counts = Counter(r[key] for r in rows)
            self.suite.eq({p: n for p, n in counts.items() if n > 1}, {})
        return len(rows)


def successor_swap(target, mutate=None, switch_at=2):
    import contextlib
    import hashlib
    from pathlib import Path
    @contextlib.contextmanager
    def manager():
        original = Path.read_bytes
        state = {"n": 0, "hashes": [], "buffers": []}
        def changed(path):
            raw = original(path)
            if str(path) == str(target):
                state["n"] += 1
                if mutate is not None and state["n"] >= switch_at:
                    raw = mutate(raw, state["n"])
                state["hashes"].append(hashlib.sha256(raw).hexdigest())
                state["buffers"].append(raw)
            return raw
        Path.read_bytes = changed
        try:
            yield state
        finally:
            Path.read_bytes = original
    return manager()


def successor_probes():
    import json
    import os
    import subprocess
    import time
    from pathlib import Path

    def changed_json(raw, count):
        return (json.dumps(dict(json.loads(raw), changed_read=count), sort_keys=True) + "\n").encode()

    def b1(s):
        M = s.module
        f = resume_fixture(s, "RV01")
        path = f.outdir + ".receipt.json.launch.json"
        with successor_swap(path, changed_json) as reads, SuccessorAudit(s) as audit:
            pin = M.launch_resume(f.ctx, f.name, 1)
        doc = M.read_pin(pin)
        s.eq((reads["n"], doc["launch_json"]["sha256"]), (1, reads["hashes"][0]))
        s.eq(doc["launch_json"]["utc"], json.loads(reads["buffers"][0])["utc"])
        s.eq(doc["observations"]["counts"]["launch_json"], 1)
        audit.once()

    def b2(s):
        M = s.module
        f = receipt_fixture(s, "RV02", off_spec=True)
        with successor_swap(f.outdir + ".receipt.json", changed_json) as reads, SuccessorAudit(s) as audit:
            h = M.history(f.ctx, f.call)
        s.eq((reads["n"], h["nonattempts"][0]["monitor_receipt"]["sha256"]), (1, reads["hashes"][0]))
        audit.once()

    def b3(s):
        M = s.module
        f = receipt_fixture(s, "RV03")
        M.close_attempt(f.ctx, f.name, 1)
        M.assemble_registry(f.ctx)
        path = Path(f.ctx.cfg["p112_launch_root"]) / "assembly" / "STEP5_LAUNCH_REGISTRY_PHASE1_CX2V001.json"
        with successor_swap(path, lambda raw, n: raw + b" ") as reads, SuccessorAudit(s) as audit:
            result = M.assemble_registry(f.ctx, verify=True)
        s.eq((reads["n"], result["registry"]["sha256"]), (1, reads["hashes"][0]))
        audit.once()

    def cleanup(s):
        M = s.module
        f = receipt_fixture(s, "RV04")
        with successor_swap(f.record_path, changed_json) as reads, SuccessorAudit(s) as audit:
            records = f.ctx.records(f.name)
        s.eq((reads["n"], records[0]["record_pin"]["sha256"]), (1, reads["hashes"][0]))
        audit.once()
        with successor_swap(f.outdir + ".receipt.json", changed_json) as reads, SuccessorAudit(s) as audit:
            result = M.close_attempt(f.ctx, f.name, 1)
        s.eq(reads["n"], 1)
        s.eq(M.read_pin(result["receipt"])["pins"]["monitor_receipt"]["sha256"], reads["hashes"][0])
        audit.once()

    def f1(s):
        M = s.module
        f = receipt_fixture(s, "RV05", no_receipt=True)
        Path(f.outdir + ".receipt.json").symlink_to(f.outdir + "/finish.json")
        with SuccessorAudit(s):
            result = M.status(f.ctx)
        s.eq(result["calls"][0]["status"], "FORBIDDEN_RESULT_READ")
        g = receipt_fixture(s, "RV06")
        alias = M.planned_outdir(g.ctx, g.name, 2, "P112") + ".receipt.json.launch.json"
        Path(alias).symlink_to(g.outdir + "/result.json")
        with SuccessorAudit(s):
            s.refuses("FORBIDDEN_RESULT_READ", lambda: M.try_launch_json(alias))
        plain = s.fixture("ordinary_record.json", {"saved": True})
        alias = s.root / "ordinary_alias.json"
        alias.symlink_to(plain["path"])
        with SuccessorAudit(s):
            s.refuses("RECORD_SYMLINK", lambda: M.read_record(alias))
            s.refuses("RECORD_SYMLINK", lambda: M.try_launch_json(str(alias)))

    def f2(s):
        M = s.module
        own = {"path": str(s.tool_path), "sha256": s.tool_sha}
        pin = "TOOL_PIN %s %s %s" % (M.TOOL_NAME, s.tool_sha, s.tool_path)
        for sep in ("\u2028", "\u2029", "\f", "\v", "\x1e", "\x1c", "\x1d", "\x85", "\r"):
            text = "## A999: synthetic\nA midline mention" + sep
            s.refuses("TOOL_PIN_MISSING", lambda text=text: M.tool_gate(text + pin + "\n", own))
            s.eq(M.residual_lines(text + "RESIDUAL_RETRY P1_M0001 1\n"), set())
        s.eq(M.tool_gate("## A999: synthetic\r\n" + pin + "\r\n", own), own)
        s.eq(M.residual_lines("## A999: synthetic\r\nRESIDUAL_RETRY P1_M0001 1\r\n"),
             {("P1_M0001", 1)})

    def b4(s, variant="first"):
        M = s.module
        f = receipt_fixture(s, "RV_sampler_" + variant)
        work = f.root / "launch_root" / "work" / "apostrophe"
        work.mkdir()
        clock = {"now": 0.0, "polls": 0}
        row = {"pid": 777001, "ppid": 1, "pgid": 777001, "command": "/bin/bash -lc echo Brian's note"}
        def processes():
            clock["polls"] += 1
            n = clock["polls"]
            return [row] if variant == "first" or (variant == "persistent" and n >= 2) or n in (2, 3) else []
        def sleep(seconds):
            if clock["polls"] > 400:
                raise AssertionError("sampler did not terminate")
            clock["now"] += seconds
        f.ctx.system.monotonic = lambda: clock["now"]
        f.ctx.system.sleep, f.ctx.system.processes = sleep, processes
        plan = {"name": f.name, "attempt": 1, "outdir": f.outdir, "config": f.ctx.config_pin}
        with SuccessorAudit(s) as audit:
            pin = M.sampler(f.ctx, plan, str(work), poll_s=1)
        sample = M.read_pin(pin)
        s.eq((sample["complete"], sample["max_other_ngc_processes"]), (True, 0))
        s.eq(M.command_argv(row), row["command"].split())
        M.enforce_solo(f.ctx, True, rows=[row])
        audit.once()
        s.eq(M.ProcessCounter(synthetic=True).count([dict(row, command="/bad/\0.py")]), [])

    def rv11(s):
        M = s.module
        child = subprocess.Popen([M.PY, "-I", "-B", "-c", "import time; time.sleep(30)", "Bob's file"],
                                 env=M.child_env(), start_new_session=True)
        try:
            time.sleep(0.1)
            row = next(r for r in M.System().processes() if r["pid"] == child.pid)
            s.eq(M.command_argv(row), row["command"].split())
            s.eq(M.ProcessCounter(synthetic=True).count([row]), [])
        finally:
            child.terminate()
            child.wait(timeout=5)

    def f3(s):
        M = s.module
        for live in (False, True):
            f = resume_fixture(s, "F3_" + str(live), missing_monitor_pid=True)
            command = M.PY + " -I -B " + f.ctx.pins["monitor"]["path"] + " --receipt " + f.outdir + ".receipt.json"
            if live:
                f.ctx.system.rows = [{"pid": 900021, "ppid": 1, "pgid": 900021, "command": command}]
            with SuccessorAudit(s) as audit:
                pin = M.launch_resume(f.ctx, f.name, 1)
            doc = M.read_pin(pin)
            s.eq((doc["outcome"], doc["monitor_pid"], doc["monitor_pid_source"]),
                 ("LAUNCH", 900021 if live else None, "command_line" if live else "no_live_match"))
            audit.once()
        rows = [{"pid": 900022, "ppid": 1, "pgid": 900022, "command": command}]
        s.eq(M.live_monitor(rows, None, f.ctx.pins["monitor"]["path"], f.outdir)["pid"], 900022)

    def f4(s):
        M = s.module
        f = receipt_fixture(s, "RV19")
        target = subprocess.Popen(["/bin/sleep", "60"], start_new_session=True)
        try:
            lj = s.fixture("rv19_launch.json", {
                "schema": M.MONITOR_SCHEMA + "_LAUNCH", "child_pid": target.pid,
                "command": ["/bin/sleep", "61"], "pins": {"spec": f.call["spec"]}})
            plan = {"name": f.name, "launch_json": lj["path"], "spec": f.call["spec"], "outdir": f.outdir}
            for label, code, expected in (
                ("crash", "raise RuntimeError('synthetic kit failure')\n", "NOT_KILLED_TARGET_REFUSED"),
                ("alive", "import sys\nsys.stderr.write('{\"alive\": true}')\nsys.exit(1)\n", "NOT_KILLED_TARGET_REFUSED"),
                ("ended", "import sys\nsys.stderr.write('{\"alive\": false}')\nsys.exit(1)\n", "ALREADY_ENDED"),
                ("missing", "import sys\nsys.stderr.write('{}')\nsys.exit(1)\n", "NOT_KILLED_TARGET_REFUSED")):
                kit = s.raw_write(f.root / ("kit_" + label + ".py"), code.encode())
                f.ctx.pins = dict(f.ctx.pins, kit=kit)
                s.eq(M.kit_kill_target(f.ctx, plan)["result"], expected)
            f.ctx.pins = dict(f.ctx.pins, kit=M.REAL["kit"])
            s.eq(M.kit_kill_target(f.ctx, plan)["result"], "NOT_KILLED_TARGET_REFUSED")
            s.eq(target.poll(), None)
        finally:
            target.terminate()
            target.wait(timeout=5)

    def f5(s):
        M = s.module
        f = full_launch_fixture(s, "RV24")
        expected = ("/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/"
                    "FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/"
                    "ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md")
        s.eq(M.V006, expected)
        with SuccessorAudit(s) as audit:
            s.refuses("V006_CONFIG_PATH", lambda: M.Context(f.config, system=M.System()))
        s.eq([r for r in audit.reads if r["path"] == f.config_doc["v006"]], [])
        s.refuses("SYNTHETIC_REAL_V006", lambda: M.synthetic_fence(
            f.overrides, dict(f.config_doc, v006=M.V006)))

    def f6(s):
        M = s.module
        for component in ("V007_POSTSEAL_RECORDS", "v007_postseal_records", "V007_Postseal_Records"):
            s.refuses("PATH_V007_POSTSEAL", lambda component=component:
                      M.path_rules(str(s.root / component / "metadata.json")))

    def immutable_audit(s):
        M = s.module
        pin = s.fixture("immutable.json", {"value": 1})
        alias = s.root / "immutable_alias.json"
        alias.symlink_to(pin["path"])
        @M.read_scope
        def operation():
            left = M.read_pin(pin)
            actual, right = M.read_and_pin(pin["path"])
            s.eq((left, right, actual), ({"value": 1}, {"value": 1}, pin))
            alias_pin, alias_doc = M.read_and_pin(alias)
            s.eq((alias_pin["sha256"], alias_doc), (pin["sha256"], left))
        with successor_swap(pin["path"], changed_json) as reads, SuccessorAudit(s) as audit:
            operation()
        s.eq(reads["n"], 1)
        audit.once()
        # A new operation starts a new snapshot rather than sharing old state.
        with SuccessorAudit(s) as audit:
            operation()
        s.eq(len(audit.reads), 1)

    def volatile_audit(s):
        M = s.module
        pin = s.fixture("volatile.launch.json", {"child_pid": 777001})
        @M.read_scope
        def operation():
            out = []
            for _ in range(2):
                raw, doc = M.try_launch_json(pin["path"])
                report = M.observation_report()
                s.eq(report["last_observation"]["launch_json"]["pin"]["sha256"], M.sha(raw))
                s.eq(doc, json.loads(raw))
                out.append(raw)
            return out, M.observation_report()
        with successor_swap(pin["path"], changed_json, switch_at=1) as reads, SuccessorAudit(s) as audit:
            buffers, report = operation()
        s.eq(reads["n"], 2)
        s.eq(buffers, reads["buffers"])
        s.eq(report["counts"], {"launch_json": 2})
        s.eq(len([r for r in audit.reads if r["volatile"]]), 2)

    def cutoff_audit(s):
        M = s.module
        f = receipt_fixture(s, "G24")
        source = f.ctx.cfg["v006"]
        @M.read_scope
        def operation():
            M.read_v006(source, kind="v006_gate")
            return M.write_cutoff(f.ctx, [{"name": f.name, "time_utc": f.rec["utc_end"],
                                        "receipt": f.entry_pin, "disposition": "FINISHED"}])
        with successor_swap(source, lambda raw, n: raw + ("\nSynthetic observation %d\n" % n).encode(),
                            switch_at=1) as reads, SuccessorAudit(s) as audit:
            pin = operation()
        doc = M.read_pin(pin)
        s.eq(reads["n"], 2)
        s.eq(doc["copy"]["sha256"], reads["hashes"][1])
        s.eq(Path(doc["copy"]["path"]).read_bytes(), reads["buffers"][1])
        s.eq(doc["observations"]["counts"], {"v006_gate": 1, "v006_cutoff": 1})
        audit.once()

    def fill_audit(s):
        M = s.module
        f = full_launch_fixture(s, "cleanup_fill")
        @M.read_scope
        def operation():
            ctx = M.Context(f.config, system=M.SyntheticSystem(M.read_pin(f.synthetic)["system"]),
                            synthetic_pins=f.overrides)
            return ctx.calls()
        with SuccessorAudit(s) as audit:
            calls = operation()
        s.eq(bool(calls), True)
        audit.once()
        for pin in (f.config_doc["members"][0]["eps"], f.config_doc["members"][0]["gq"]):
            s.eq(sum(r["path"] == pin["path"] for r in audit.reads), 1)

    return {
        "B1_RV01_checked_launch_buffer": b1,
        "B2_RV02_classified_receipt_buffer": b2,
        "B3_RV03_verified_registry_buffer": b3,
        "CLEANUP_RV04_single_guarded_read": cleanup,
        "F1_RV05_RV06_record_alias_blinding": f1,
        "F2_RV08_actual_line_grammar": f2,
        "B4_RV11_real_apostrophe_ps": rv11,
        "B4_RV12_transient_apostrophe": lambda s: b4(s, "transient"),
        "B4_RV13_persistent_apostrophe": lambda s: b4(s, "persistent"),
        "B4_RV14_first_apostrophe": lambda s: b4(s, "first"),
        "F3_missing_monitor_pid_recovery": f3,
        "F4_RV19_kit_exit_one_semantics": f4,
        "F5_RV24_production_V006_constant": f5,
        "F6_postseal_component_guard": f6,
        "0785_immutable_audit_MUST_PASS": immutable_audit,
        "0785_volatile_audit_MUST_PASS": volatile_audit,
        "0785_cutoff_audit_MUST_PASS": cutoff_audit,
        "CLEANUP_fill_single_read_MUST_PASS": fill_audit,
    }


def successor_cases(suite):
    for name, probe in successor_probes().items():
        suite.case(name, lambda probe=probe: probe(suite))
    suite.interfaces["cx2v002_regressions"] = (
        "TESTED synthetic saved states and inert processes only. The per-operation audit checks "
        "spelled paths and realpaths in this process; it cannot observe executable reopening "
        "inside child processes. Child executable integrity remains the root envelope's responsibility.")

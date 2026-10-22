"""A real inert interruption and restoring mutants for every required fix."""


def successor_interruption_cases(suite):
    import contextlib
    import json
    import os
    import subprocess
    import time
    from pathlib import Path
    M = suite.module

    def regression():
        f = full_launch_fixture(suite, "RV21_live_interruption")
        ctx = M.Context(f.config, system=M.SyntheticSystem(M.read_pin(f.synthetic)["system"]),
                        synthetic_pins=f.overrides)
        ctx.synthetic_pin = f.synthetic
        M.synthetic_fence(f.overrides, f.config_doc)
        outdir = M.planned_outdir(ctx, f.name, 1, "P112")
        watch = subprocess.Popen([M.PY, "-I", "-B", f.watch["path"]], env=M.child_env(),
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        try:
            time.sleep(0.1)
            child = os.fork()
            if child == 0:
                try:
                    original = ctx.write
                    def interrupted(path, obj):
                        if str(path).endswith("/monitor_pid.json"):
                            os._exit(9)
                        return original(path, obj)
                    ctx.write = interrupted
                    with open(os.devnull, "w") as stream, contextlib.redirect_stdout(stream), contextlib.redirect_stderr(stream):
                        M.launch(ctx, f.name, 1)
                    os._exit(0)
                except BaseException:
                    os._exit(3)
            _, status = os.waitpid(child, 0)
            suite.eq(os.waitstatus_to_exitcode(status), 9)
            works = list((Path(ctx.cfg["p112_launch_root"]) / "work").glob(f.name + "_A1_*"))
            suite.eq(len(works), 1)
            work = works[0]
            suite.eq((work / "invocation.json").is_file(), True)
            suite.eq((work / "monitor_pid.json").exists(), False)
            until = time.monotonic() + 40
            while not Path(outdir + ".solo.json").is_file() and time.monotonic() < until:
                time.sleep(0.1)
            suite.eq(Path(outdir + ".receipt.json").is_file(), True)
            suite.eq(Path(outdir + ".solo.json").is_file(), True)
            with SuccessorAudit(suite) as audit:
                pin = M.launch_resume(ctx, f.name, 1)
            record = M.read_pin(pin)
            suite.eq((record["outcome"], record["monitor_pid"], record["monitor_pid_source"]),
                     ("LAUNCH", None, "no_live_match"))
            audit.once()
            until = time.monotonic() + 10
            while M.qualified_process(ctx.system.processes(), record["sampler_pid"],
                                      str(suite.tool_path), outdir, "sampler") and time.monotonic() < until:
                time.sleep(0.1)
            suite.eq(M.close_attempt(ctx, f.name, 1)["status_class"], "FINISHED")
        finally:
            # Qualification binds cleanup to this exclusively created fixture.
            for role, tool in (("monitor", f.overrides["monitor"]["path"]), ("sampler", str(suite.tool_path))):
                for row in ctx.system.processes():
                    if M.qualified_process([row], row["pid"], tool, outdir, role):
                        M.stop_qualified(ctx.system, row["pid"], lambda r, command=row["command"]: r["command"] == command)
            if watch.poll() is None:
                watch.terminate()
            watch.wait(timeout=5)
    suite.case("F3_RV21_actual_inert_Popen_interruption_resume_close", regression)
    suite.interfaces["RV21_interruption"] = (
        "TESTED an actual forked synthetic invocation exiting after inert monitor Popen and before "
        "monitor_pid.json. Resume and close use the saved invocation and exact launch bytes.")


def successor_mutation_cases(suite):
    import types
    probes = successor_probes()
    original = suite.tool_path.read_text()
    rows = []
    serial = [0]

    def child(name, module):
        serial[0] += 1
        obj = object.__new__(type(suite))
        obj.__dict__ = dict(suite.__dict__)
        obj.module = module
        obj.root = suite.root / ("successor_mutant_%02d_%s" % (serial[0], name))
        obj.root.mkdir()
        obj.rows, obj.interfaces = [], {}
        return obj

    def trial(name, function, old, new, probe_name):
        def action():
            probe = probes[probe_name]
            probe(child(name + "_control", suite.module))
            start = original.index("\ndef " + function + "(") + 1
            end = original.find("\ndef ", start + 1)
            end = len(original) if end < 0 else end
            section = original[start:end]
            suite.eq(section.count(old), 1)
            changed = original[:start] + section.replace(old, new, 1) + original[end:]
            module = types.ModuleType("_p112_successor_mutant_" + name)
            module.__file__ = str(suite.tool_path)
            exec(compile(changed, str(suite.tool_path), "exec"), module.__dict__)
            failure = None
            try:
                probe(child(name + "_mutant", module))
            except Exception as error:
                failure = type(error).__name__
            suite.eq(failure is not None, True)
            rows.append({"name": name, "control": "PASS", "status": "KILLED",
                         "source_sha256": suite.module.sha(changed.encode()),
                         "function": function, "replace": old, "with": new, "detection": failure,
                         "imported": True})
        suite.case("CX2V002_MUTANT_" + name, action)

    trial("B1_launch_reread", "write_launch_record", "raw, lj = snapshot",
          'raw, lj = try_launch_json(plan["launch_json"])', "B1_RV01_checked_launch_buffer")
    trial("B2_receipt_reread", "history", '"monitor_receipt": monitor_pin',
          '"monitor_receipt": {"path": receipt_path, "sha256": sha(Path(receipt_path).read_bytes())}',
          "B2_RV02_classified_receipt_buffer")
    trial("B3_registry_reread", "assemble_registry", '"registry": registry_pin',
          '"registry": {"path": str(p), "sha256": sha(p.read_bytes())}',
          "B3_RV03_verified_registry_buffer")
    trial("B4_command_parse_refusal", "command_argv", 'return row["command"].split()',
          'raise Refusal("PS_COMMAND_PARSE")', "B4_RV14_first_apostrophe")
    trial("F1_unguarded_launch_observation", "observe_file", "guard_record(path)", "pass",
          "F1_RV05_RV06_record_alias_blinding")
    trial("F1_allow_record_alias", "guard_record", 'need(os.path.realpath(path) == path, "RECORD_SYMLINK", path)',
          "pass", "F1_RV05_RV06_record_alias_blinding")
    trial("F2_tool_splitlines", "tool_gate", r'text.split("\n")', "text.splitlines()",
          "F2_RV08_actual_line_grammar")
    trial("F2_residual_splitlines", "residual_lines", r'text.split("\n")', "text.splitlines()",
          "F2_RV08_actual_line_grammar")
    trial("F3_require_monitor_pid_file", "launch_resume", "and inv.is_file():",
          "and inv.is_file() and mp.is_file():", "F3_missing_monitor_pid_recovery")
    trial("F4_any_exit_one_ended", "kit_kill_target",
          'if type(failure) is dict and failure.get("alive") is False:', "if True:",
          "F4_RV19_kit_exit_one_semantics")
    # Context.__init__ is a method; replace through the enclosing class source.
    def production_probe_with_removed_check():
        name = "F5_configured_V006"
        probe = probes["F5_RV24_production_V006_constant"]
        probe(child(name + "_control", suite.module))
        needle = 'need(self.synthetic or c["v006"] == V006, "V006_CONFIG_PATH")'
        suite.eq(original.count(needle), 1)
        changed = original.replace(needle, "pass")
        module = types.ModuleType("_p112_mutant_f5")
        module.__file__ = str(suite.tool_path)
        exec(compile(changed, str(suite.tool_path), "exec"), module.__dict__)
        failure = None
        try:
            probe(child(name + "_mutant", module))
        except Exception as error:
            failure = type(error).__name__
        suite.eq(failure is not None, True)
        rows.append({"name": name, "control": "PASS", "status": "KILLED",
                     "source_sha256": suite.module.sha(changed.encode()),
                     "replace": needle, "with": "pass", "detection": failure, "imported": True})
    suite.case("CX2V002_MUTANT_F5_configured_V006", production_probe_with_removed_check)
    trial("F6_postseal_guard_removed", "path_rules",
          'need("v007_postseal_records" not in parts, "PATH_V007_POSTSEAL", where)', "pass",
          "F6_postseal_component_guard")
    trial("cleanup_pin_then_reread", "read_record",
          "return read_and_pin(guard_record(path), decode=decode)",
          'pin, raw = read_and_pin(guard_record(path), decode=False)\n'
          '    raw = Path(path).read_bytes()\n'
          '    return pin, strict_json(raw) if decode else raw',
          "CLEANUP_RV04_single_guarded_read")
    trial("0785_immutable_cache_bypassed", "read_and_pin",
          "if snapshots is not None and cache_key in snapshots:", "if False:",
          "0785_immutable_audit_MUST_PASS")
    trial("0785_volatile_pin_reread", "observe_file",
          'pin = {"path": path, "sha256": sha(raw)}',
          'pin = {"path": path, "sha256": sha(Path(path).read_bytes())}',
          "0785_volatile_audit_MUST_PASS")
    trial("0785_cutoff_copy_reread", "write_cutoff", "write_x_bytes(p, raw)",
          'write_x_bytes(p, read_v006(ctx.cfg["v006"], kind="v006_cutoff"))',
          "0785_cutoff_audit_MUST_PASS")
    suite.interfaces["cx2v002_restoring_mutants"] = rows

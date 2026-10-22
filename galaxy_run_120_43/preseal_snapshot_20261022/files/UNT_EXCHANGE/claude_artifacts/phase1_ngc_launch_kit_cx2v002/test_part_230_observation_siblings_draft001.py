"""0786 exact-key refusal records and their hashed observation siblings."""


def observation_refusal_fixture(suite, label, *, origin="P112", variant="valid"):
    from pathlib import Path
    M = suite.module
    name = "S0_J0_SERIAL" if origin == "KIT" else "P1_M0001"
    f = receipt_fixture(suite, label, origin=origin, name=name, mode="FAILED")
    M.close_attempt(f.ctx, name, 1)
    root = Path(f.ctx.cfg["s0"]["launch_root"] if origin == "KIT" else f.ctx.cfg["p112_launch_root"])
    work = root / "work" / "observation_refusal"
    work.mkdir()
    outdir = M.planned_outdir(f.ctx, name, 2, origin)
    plan = {"schema": "UNT_P112_LAUNCH_PLAN_CX2V001", "name": name, "attempt": 2,
            "outdir": outdir, "config": f.ctx.config_pin, "caps": M.first_caps(name), "solo_mode": False}
    pp = suite.raw_write(work / "plan.json", M.encoded(plan))
    stdout = suite.raw_write(work / "monitor.stdout.txt", b"synthetic monitor refusal\n")
    stderr = suite.raw_write(work / "monitor.stderr.txt", b"")
    f.refusal_work, f.refusal_plan = work, pp
    if variant == "emit":
        return f
    path = (root / "monitor_refused" / (name + "_MONITOR_REFUSED_C2V003A_A2.json") if origin == "KIT" else
            root / "launches" / ("P112_" + name + "_MONITOR_REFUSED_CX2V001_A2.json"))
    report = {"counts": {}, "last_observation": {}, "date_u": M.date_u()}
    if variant == "form":
        report["counts"] = {"launch_json": 1}
    if variant == "missing":
        digest = "a" * 64
    else:
        op = suite.raw_write(str(path) + ".observations.json", M.encoded(report))
        digest = "0" * 64 if variant == "sha" else op["sha256"]
    rule = "synthetic root D7 observations_sha256=" + digest
    if variant == "rule":
        rule = "synthetic missing observation binding"
    rec = {"schema": "MONITOR_REFUSED_ATTEMPT_RECORD_C2V001", "name": name, "attempt": 2,
           "launcher": "KIT_C2V003A" if origin == "KIT" else "P112_CX2V001",
           "writer": {"name": "ROOT", "sha256": None} if origin == "KIT" else
                     {"name": M.TOOL_NAME, "sha256": suite.tool_sha},
           "plan": pp, "monitor_stdout": stdout, "monitor_stderr": stderr,
           "absent": M.absent_paths(outdir), "date_u": M.date_u(), "rule": rule}
    suite.raw_write(path, M.encoded(rec))
    f.refusal_path = path
    return f


def observation_sibling_probes():
    from pathlib import Path

    def accepted(s):
        M = s.module
        for origin in ("P112", "KIT"):
            f = observation_refusal_fixture(s, "0786_valid_" + origin, origin=origin)
            with SuccessorAudit(s) as audit:
                result = M.status(f.ctx)
            s.eq(result["calls"][0]["status"], "READY")
            s.eq(result["calls"][0]["nonattempts"][0]["observations_pin"]["path"],
                 str(f.refusal_path) + ".observations.json")
            audit.once()
            M.assemble_registry(f.ctx)
            with SuccessorAudit(s) as audit:
                s.eq(M.assemble_registry(f.ctx, verify=True)["status"], "VERIFIED")
            audit.once()

    def refused(s, variant="sha"):
        M = s.module
        code = {"sha": "OBSERVATIONS_SIBLING_SHA", "missing": "OBSERVATIONS_SIBLING_MISSING",
                "rule": "OBSERVATIONS_RULE_SHA", "form": "OBSERVATIONS_FORM"}[variant]
        for origin in ("P112", "KIT"):
            f = observation_refusal_fixture(s, "0786_" + variant + "_" + origin, origin=origin, variant=variant)
            with SuccessorAudit(s) as audit:
                s.eq(M.status(f.ctx)["calls"][0]["status"], code)
            audit.once()
            with SuccessorAudit(s):
                s.refuses(code, lambda: M.assemble_registry(f.ctx, verify=True))

    def emitted(s):
        M = s.module
        f = observation_refusal_fixture(s, "0786_emit", variant="emit")
        order, original = [], f.ctx.write
        def write(path, obj):
            order.append(str(path))
            return original(path, obj)
        f.ctx.write = write
        try:
            with SuccessorAudit(s) as audit:
                pin = M.record_monitor_refused(f.ctx, f.refusal_plan, str(f.refusal_work))
        finally:
            f.ctx.write = original
        s.eq(order, [pin["path"] + ".observations.json", pin["path"]])
        audit.once()
        rec = M.read_pin(pin)
        s.eq(set(rec), {"schema", "name", "attempt", "launcher", "writer", "plan",
                        "monitor_stdout", "monitor_stderr", "absent", "date_u", "rule"})
        op, report = M.read_record(pin["path"] + ".observations.json")
        s.eq("observations_sha256=" + op["sha256"] in rec["rule"], True)
        s.eq((report["counts"], report["last_observation"]), ({}, {}))
        s.eq(M.status(f.ctx)["calls"][0]["status"], "READY")
        # Context.write adds observations to other evidence without changing
        # the exact-key refusal record or its sibling's counts representation.
        p = f.root / "launch_root" / "work" / "other_evidence.json"
        ep = f.ctx.write(str(p), {"schema": "SYNTHETIC_EVIDENCE", "date_u": M.date_u()})
        s.eq(M.read_pin(ep)["observations"], {"counts": {}, "last_observation": {}})

    return {"0786_root_and_P112_siblings_accepted": accepted,
            "0786_missing_sibling_refused": lambda s: refused(s, "missing"),
            "0786_changed_sibling_refused": lambda s: refused(s, "sha"),
            "0786_rule_binding_required": lambda s: refused(s, "rule"),
            "0786_sibling_form_required": lambda s: refused(s, "form"),
            "0786_sibling_written_before_exact_key_record": emitted}


def observation_sibling_cases(suite):
    for name, probe in observation_sibling_probes().items():
        suite.case(name, lambda probe=probe: probe(suite))


def observation_sibling_mutation_cases(suite):
    import types
    probes = observation_sibling_probes()
    original = suite.tool_path.read_text()
    mutations = [
        ("0786_ignore_sibling_sha",
         'need(pin["sha256"] == matches[0], "OBSERVATIONS_SIBLING_SHA", path)',
         "pass", "0786_changed_sibling_refused"),
        ("0786_ignore_missing_sibling",
         'need(Path(path).is_file(), "OBSERVATIONS_SIBLING_MISSING", path)',
         'if not Path(path).is_file(): return {"path": path, "sha256": matches[0]}, {"counts": {}, "last_observation": {}}',
         "0786_missing_sibling_refused"),
        ("0786_parent_written_first",
         'observations_pin = ctx.write(path + ".observations.json", report)',
         'ctx.write(path, rec)\n    observations_pin = ctx.write(path + ".observations.json", report)',
         "0786_sibling_written_before_exact_key_record"),
    ]
    evidence = []
    for name, old, new, probe_name in mutations:
        def action(name=name, old=old, new=new, probe_name=probe_name):
            def child(suffix, module):
                obj = object.__new__(type(suite))
                obj.__dict__ = dict(suite.__dict__)
                obj.module = module
                obj.root = suite.root / (name + "_" + suffix)
                obj.root.mkdir()
                obj.rows, obj.interfaces = [], {}
                return obj
            probe = probes[probe_name]
            probe(child("control", suite.module))
            suite.eq(original.count(old), 1)
            source = original.replace(old, new)
            module = types.ModuleType("_p112_mutant_" + name)
            module.__file__ = str(suite.tool_path)
            exec(compile(source, str(suite.tool_path), "exec"), module.__dict__)
            failure = None
            try:
                probe(child("mutant", module))
            except Exception as error:
                failure = type(error).__name__
            suite.eq(failure is not None, True)
            evidence.append({"name": name, "control": "PASS", "status": "KILLED",
                             "source_sha256": suite.module.sha(source.encode()), "replace": old, "with": new,
                             "detection": failure, "imported": True})
        suite.case("CX2V002_MUTANT_" + name, action)
    suite.interfaces["0786_restoring_mutants"] = evidence

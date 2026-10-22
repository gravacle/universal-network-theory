"""File-backed F de-duplication, in-flight windows, and validation boundaries."""


def boundary_cases(suite):
    import copy
    from pathlib import Path
    M, case, fail = suite.module, suite.case, suite.refuses
    f = full_launch_fixture(suite, "F_DUPLICATE_MEMBER", duplicate_f0=True)
    def context():
        return M.Context(f.config, system=M.SyntheticSystem(M.read_pin(f.synthetic)["system"]), synthetic_pins=f.overrides)
    ctx = context()
    def duplicate_check():
        calls = ctx.calls()
        suite.eq([c["name"] for c in calls], ["P1_M0001", "P1_F1", "P1_F2", M.TWIN])
        suite.eq(calls[0]["serves"], ["F0"])
        suite.eq("P1_F0" in ctx.vpins["SPEC_PIN"], False)
    case("T01_F_duplicate_reuses_member_without_F_launch_pins", duplicate_check)
    for label, solo, same, expected in (
        ("solo_invocation", True, False, "SOLO_RERUN_ACTIVE"),
        ("same_outdir", False, True, "INVOCATION_ALREADY_ACTIVE"),
        ("reused_pid", True, False, None),
        ("monitor_before_record", True, False, "SOLO_RERUN_ACTIVE")):
        f2 = receipt_fixture(suite, "P05_inflight_" + label)
        work = f2.root / "launch_root" / "work" / "inflight"
        work.mkdir()
        outdir = M.planned_outdir(f2.ctx, f2.name, 2, "P112")
        command = M.PY + " -I -B /synthetic/p112.py launch --name P1_M0001"
        plan = {"schema": "UNT_P112_LAUNCH_PLAN_CX2V001", "name": f2.name, "outdir": outdir,
                "solo_mode": solo, "invocation_pid": 900019, "invocation_command": command,
                "pins": {"monitor": M.REAL["monitor"]}}
        suite.raw_write(work / "plan.json", M.encoded(plan))
        if label == "monitor_before_record":
            command = M.PY + " -I -B " + M.REAL["monitor"]["path"] + " --receipt " + outdir + ".receipt.json"
        elif label == "reused_pid":
            command = "/bin/sleep 120"
        f2.ctx.system.rows = [{"pid":900019,"ppid":1,"pgid":900019,"command":command}]
        action = lambda f2=f2, same=same, outdir=outdir: M.enforce_solo(f2.ctx, False, requested_outdir=outdir if same else None)
        case("P05_inflight_" + label, (lambda expected=expected, action=action: fail(expected, action)) if expected else action)
    call = ctx.calls()[0]
    cfg = ctx.cfg["members"][0]
    handoff = M.read_pin(cfg["handoff"])
    spec, sp, fill, fc = ctx.read_fill(cfg)
    args = [handoff, cfg["handoff"], *fill, call["point_key"], cfg["eps"], ctx.pins["lo"],
            "UNT_STEP5_ADMITTED_POINT_HANDOFF_CX3V001", True]
    mutations = [
        (0, "schema", "WRONG", "HANDOFF_SCHEMA"),
        (0, "mode", "ADMITTED", "HANDOFF_MODE"),
        (0, "driver_branch", "WRONG", "HANDOFF_DRIVER_BRANCH"),
        (0, "certificate_pins", {}, "HANDOFF_CERTIFICATES"),
        (4, "schema", "WRONG", "FILL_SCHEMA"),
        (4, "launch_authorized", True, "FILL_LAUNCH_AUTHORIZED"),
        (4, "handoff_pin", {}, "FILL_HANDOFF_PIN"),
        (4, "theta_key", "f" * 64, "FILL_POINT_KEY"),
        (4, "pending_certificates", ["eps"], "FILL_PENDING_CERTIFICATES")]
    for index, key, value, code in mutations:
        changed = copy.deepcopy(args)
        changed[index][key] = value
        case("V_fill_" + code, lambda changed=changed, code=code: fail(code, lambda: M.fill_check(*changed)))
    log = {"exit":0,"blocked":[],"ctx_modes":["simulate"],"driver_sha256":ctx.pins["driver"]["sha256"],
           "spec_sha256":sp["sha256"]}
    readiness = {"executed_stages":0,"binding_blockers":[],"source_build_blockers":[],
                 "future_stage_dependencies":[{"class":"PENDING_ROUTE_A_OUTPUTS"}],"planned_route_a":True}
    for side, key, value in (("log","exit",1),("log","blocked",["bad"]),("log","ctx_modes",["real"]),
                            ("log","driver_sha256","f"*64),("log","spec_sha256","f"*64),
                            ("readiness","executed_stages",1),("readiness","binding_blockers",["x"]),
                            ("readiness","source_build_blockers",["x"]),
                            ("readiness","future_stage_dependencies",[{"class":"BAD"}]),
                            ("readiness","planned_route_a",False)):
        docs = {"log":copy.deepcopy(log),"readiness":copy.deepcopy(readiness)}
        docs[side][key] = value
        case("V_dry_" + key, lambda docs=docs: fail("DRY_VERDICT_REFUSED", lambda: M.dry_verdict(
            docs["log"], docs["readiness"], sp, ctx.pins["driver"])))

    for directory, filename, code in (("ordinary", "result.json", "FORBIDDEN_RESULT_READ"),
                                      ("A_SIDE", "source.py", "FORBIDDEN_READ_PATH"),
                                      ("ordinary", "freeze_manifest.json", "FORBIDDEN_SEALED_READ")):
        target = suite.root / ("guard_" + filename) / directory / filename
        target.parent.mkdir(parents=True)
        suite.raw_write(target, b"SYNTHETIC_FORBIDDEN_READ_SENTINEL")
        alias = target.parent.parent / "alias.py"
        alias.symlink_to(target)
        case("V03_guard_symlink_" + filename, lambda alias=alias, code=code: fail(code, lambda: M.pin_of(alias)))
    counter = M.ProcessCounter(declared=[], synthetic=True)
    case("V04_process_counter_never_resolves_Volumes", lambda: suite.eq(counter.identify("/Volumes/SYNTHETIC_NOT_TOUCHED/alias.py"), None))

    f2 = receipt_fixture(suite, "N04_old_sampler_exit_window")
    work = f2.root / "launch_root" / "work" / "old_sampler"
    work.mkdir()
    outdir = M.planned_outdir(f2.ctx, f2.name, 2, "P112")
    suite.raw_write(work / "plan.json", M.encoded({"schema":"UNT_P112_LAUNCH_PLAN_CX2V001",
                    "name":f2.name,"outdir":outdir,"solo_mode":False,"work":str(work)}))
    suite.raw_write(work / "sampler_first_sample.json", M.encoded({"sampler_pid":900031,"ok":True}))
    f2.ctx.system.rows = [{"pid":900031,"ppid":1,"pgid":900031,"command":
                          M.PY+" -I -B "+f2.ctx.own_pin["path"]+" _sampler --outdir "+outdir}]
    case("N04_old_sampler_blocks_same_outdir",lambda:fail("INVOCATION_ALREADY_ACTIVE",
         lambda:M.enforce_solo(f2.ctx,False,requested_outdir=outdir)))
    case("N04_current_sampler_admitted_at_second_check",lambda:M.enforce_solo(
        f2.ctx,False,requested_outdir=outdir,own_work=str(work)))
    f2.ctx.system.rows[0]["command"] = "/bin/sleep 120"
    case("N04_reused_sampler_pid_does_not_block",lambda:M.enforce_solo(f2.ctx,False,requested_outdir=outdir))

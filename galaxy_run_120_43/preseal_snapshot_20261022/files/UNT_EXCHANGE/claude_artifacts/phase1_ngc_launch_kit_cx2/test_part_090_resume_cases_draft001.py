"""Saved interrupted-launch states; no scientific process is started."""


def resume_fixture(suite, label, *, bad_caps=False, invocation_alive=False, reused_pid=False):
    import os
    from pathlib import Path
    M = suite.module
    f = receipt_fixture(suite, label, record=False)
    work = f.root / "launch_root" / "work" / (f.name + "_A1_SYNTHETIC_900004")
    work.mkdir()
    m15 = {"schema": "UNT_M15_PRELAUNCH_RECORD_C2V001", "date_u": M.date_u(),
           "date_u_epoch_s": int(M.timestamp(f.rec["utc_start"])) - 1}
    m15_pin = suite.raw_write(work / "m15_fixture.json", M.encoded(m15))
    caps = M.first_caps(f.name)
    if bad_caps:
        caps["wall_cap_s"] += 1
    plan = {
        "schema": "UNT_P112_LAUNCH_PLAN_CX2V001", "name": f.name, "attempt": 1,
        "outdir": f.outdir, "receipt": f.outdir + ".receipt.json", "launch_json": f.outdir + ".receipt.json.launch.json",
        "spec": f.call["spec"], "pins": {"driver": f.ctx.pins["driver"], "monitor": f.ctx.pins["monitor"]},
        "caps": caps, "caps_basis": {"rule": "synthetic saved interruption"},
        "m15_record": m15_pin, "host_ram_bytes": M.RAM, "solo_mode": False, "counted_rerun": False,
        "rule_c_basis": [], "config": f.ctx.config_pin, "work": str(work), "invocation_utc": M.utc(), "date_u": M.date_u()}
    plan["monitor_argv"] = M.monitor_command(f.ctx.pins, f.call["spec"], f.outdir, caps)
    plan_pin = suite.raw_write(work / "plan.json", M.encoded(plan))
    old_command = M.PY + " -I -B " + str(suite.tool_path) + " launch --name " + f.name
    inv = {"invocation_pid": 900004, "invocation_command": old_command, "sampler_pid": 900002,
           "planned_monitor_argv": plan["monitor_argv"], "plan": plan_pin, "date_u": M.date_u()}
    suite.raw_write(work / "invocation.json", M.encoded(inv))
    suite.raw_write(work / "monitor_pid.json", M.encoded({"monitor_pid": 900001, "plan": plan_pin, "date_u": M.date_u()}))
    if invocation_alive or reused_pid:
        f.ctx.system.rows = [{"pid": 900004, "ppid": 1, "pgid": 900004,
                             "command": "/bin/sleep 60" if reused_pid else old_command}]
    f.work, f.plan, f.plan_pin = work, plan, plan_pin
    return f


def resume_cases(suite):
    from pathlib import Path
    M, case, fail = suite.module, suite.case, suite.refuses
    f = resume_fixture(suite, "N20_resume_receipt_present")
    case("N20_resume_finished_monitor", lambda: suite.eq(
        M.read_pin(M.launch_resume(f.ctx, f.name, 1))["outcome"], "LAUNCH"))
    case("N20_resume_then_close", lambda: suite.eq(M.close_attempt(f.ctx, f.name, 1)["status_class"], "FINISHED"))
    f = resume_fixture(suite, "N20_resume_live_monitor")
    f.ctx.system.rows = [{"pid": 900001, "ppid": 1, "pgid": 900001, "command":
                         M.PY + " -I -B " + f.ctx.pins["monitor"]["path"] + " --receipt " + f.outdir + ".receipt.json"}]
    case("N20_resume_monitor_still_running", lambda: suite.eq(
        M.read_pin(M.launch_resume(f.ctx, f.name, 1))["outcome"], "LAUNCH"))
    f = resume_fixture(suite, "N20_resume_original_alive", invocation_alive=True)
    case("N20_live_invocation_blocks_resume", lambda: fail("RESUME_INVOCATION_ALIVE",
                                                         lambda: M.launch_resume(f.ctx, f.name, 1)))
    f = resume_fixture(suite, "N20_resume_reused_invocation_pid", reused_pid=True)
    case("N20_reused_invocation_pid_passes", lambda: suite.eq(
        M.read_pin(M.launch_resume(f.ctx, f.name, 1))["outcome"], "LAUNCH"))
    f = resume_fixture(suite, "N20_resume_mismatched_launch", bad_caps=True)
    case("N20_bad_launch_becomes_mislaunch", lambda: suite.eq(
        M.read_pin(M.launch_resume(f.ctx, f.name, 1))["outcome"], "MISLAUNCH"))
    f = resume_fixture(suite, "N20_no_gate")
    f.ctx.v006_text = "## A999: no gate\n"
    case("L06_resume_gated", lambda: fail("TOOL_PIN_MISSING", lambda: M.launch_resume(f.ctx, f.name, 1)))
    f = resume_fixture(suite, "N19_resume_unmounted")
    f.ctx.system.fixture["mount_points"] = []
    case("N19_resume_volume_first", lambda: fail("RUN_VOLUME_NOT_MOUNTED", lambda: M.launch_resume(f.ctx, f.name, 1)))
    suite.interfaces["resume_fixture_scope"] = (
        "TESTED saved interrupted states with real-format monitor records: completed/live monitor, "
        "live/reused invocation pid, mismatch, gate and mount. No actual scientific interruption was induced.")

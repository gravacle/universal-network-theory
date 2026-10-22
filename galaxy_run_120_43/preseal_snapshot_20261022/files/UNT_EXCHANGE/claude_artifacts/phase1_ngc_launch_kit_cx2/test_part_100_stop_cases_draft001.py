"""Qualified stop tests against only inert processes created by this suite."""


def stop_cases(suite):
    import json
    import os
    import subprocess
    import time
    from pathlib import Path
    M, case, fail = suite.module, suite.case, suite.refuses
    class FastSystem(M.SyntheticSystem):
        def __init__(self, f):
            super().__init__({"mount_points": [f.ctx.cfg["run_volume"], str(Path(f.ctx.cfg["s0"]["run_root"]).parent)],
                              "free_bytes": 1 << 50, "host_ram_bytes": M.RAM})
            self.clock = 0.0
        def monotonic(self):
            return self.clock
        def sleep(self, seconds):
            self.clock += max(seconds, 20)
            time.sleep(0.05)
    def terminate_handle(p):
        if p is None:
            return
        if p.poll() is None:
            p.terminate()
            try:
                p.wait(timeout=3)
            except subprocess.TimeoutExpired:
                p.kill()
                p.wait(timeout=3)
        else:
            p.wait()
    for variant in ("launch_on_term", "started_without_launch", "refused_no_outputs", "truncated_orphan"):
        f = receipt_fixture(suite, "N18_" + variant, mode="FAILED")
        M.close_attempt(f.ctx, f.name, 1)
        f.ctx.system = FastSystem(f)
        work = f.root / "launch_root" / "work" / ("stop_" + variant)
        work.mkdir()
        outdir = M.planned_outdir(f.ctx, f.name, 2, "P112")
        driver = suite.raw_write(work / "inert_wait_driver.py", b"import time\ntime.sleep(120)\n")
        f.ctx.pins = dict(f.ctx.pins, driver=driver)
        plan = {"schema": "UNT_P112_LAUNCH_PLAN_CX2V001", "name": f.name, "attempt": 2, "outdir": outdir,
                "receipt": outdir + ".receipt.json", "launch_json": outdir + ".receipt.json.launch.json",
                "spec": f.call["spec"], "caps": dict(M.first_caps(f.name), wall_cap_s=1220648),
                "caps_basis": {"rule": "synthetic N18"}, "host_ram_bytes": M.RAM, "solo_mode": True,
                "counted_rerun": True, "rule_c_basis": [], "m15_record": f.entry_pin,
                "config": f.ctx.config_pin, "work": str(work), "date_u": M.date_u()}
        child, mon = None, None
        try:
            if variant in ("launch_on_term", "truncated_orphan"):
                child = subprocess.Popen(M.driver_command(f.ctx.pins, plan["spec"], outdir), env=M.child_env(),
                                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
            lj = {"schema": M.MONITOR_SCHEMA + "_LAUNCH", "utc": f.rec["utc_start"], "child_pid": child.pid if child else 900099,
                  "command": M.driver_command(f.ctx.pins, plan["spec"], outdir),
                  "pins": {"driver": driver, "spec": plan["spec"]}, "caps": plan["caps"], "retries_allowed": 0}
            code = "import json,signal,time\nfrom pathlib import Path\n"
            if variant == "launch_on_term":
                code += ("def stop(sig,frame):\n"
                         " with Path(%r).open('x') as f:json.dump(%r,f)\n"
                         " raise SystemExit(0)\n"
                         "signal.signal(signal.SIGTERM,stop)\n") % (plan["launch_json"], lj)
            elif variant == "started_without_launch":
                code += "with Path(%r).open('x') as f:f.write('FORBIDDEN_RECEIPT_STDOUT')\n" % (plan["receipt"] + ".stdout.txt")
            code += "time.sleep(120)\n"
            mp = suite.raw_write(work / "inert_wait_monitor.py", code.encode())
            f.ctx.pins = dict(f.ctx.pins, monitor=mp)
            plan["pins"] = {"driver": driver, "monitor": mp}
            plan["monitor_argv"] = M.monitor_command(f.ctx.pins, plan["spec"], outdir, plan["caps"])
            plan_pin = suite.raw_write(work / "plan.json", M.encoded(plan))
            suite.raw_write(work / "monitor.stdout.txt", b"SYNTHETIC_MONITOR_LOG\n")
            suite.raw_write(work / "monitor.stderr.txt", b"")
            if variant == "truncated_orphan":
                suite.raw_write(Path(plan["launch_json"]), b'{"truncated":')
                mon_pid = 900099
            else:
                mon = subprocess.Popen(plan["monitor_argv"], env=M.child_env(), stdout=subprocess.DEVNULL,
                                       stderr=subprocess.DEVNULL, start_new_session=True)
                mon_pid = mon.pid
            time.sleep(0.2)
            before = list((f.root / "launch_root" / "launches").iterdir())
            result = M.stop_launch_failure(f.ctx, plan, mon_pid, parsed=False)
            case("N18_" + variant + "_monitor_stopped_before_record", lambda mon=mon:
                 suite.eq(mon is None or mon.poll() is not None, True))
            if variant in ("launch_on_term", "truncated_orphan"):
                case("N18_" + variant + "_driver_stopped", lambda child=child: suite.eq(child.poll() is not None, True))
                case("N18_" + variant + "_no_mon_pid_after_stop", lambda result=result:
                     suite.eq(result["mon_pid_supplied"], None))
                def record_mislaunch(f=f, plan=plan, plan_pin=plan_pin, mon_pid=mon_pid, result=result):
                    pin = M.write_launch_record(f.ctx, plan, plan_pin, f.entry_pin, mon_pid, 900002, None,
                                                {"launch_json_parseable": False}, result)
                    suite.eq(M.read_pin(pin)["outcome"], "MISLAUNCH")
                    suite.eq(M.status(f.ctx)["calls"][0]["status"], "MONITOR_ENDED_NO_RECEIPT")
                case("N18_" + variant + "_mislaunch_residual", record_mislaunch)
            elif variant == "started_without_launch":
                case("N18_started_is_not_refusal", lambda f=f, plan_pin=plan_pin, work=work:
                     fail("MONITOR_STARTED_NO_LAUNCH_JSON", lambda: M.record_monitor_refused(f.ctx, plan_pin, str(work))))
                case("N18_started_no_record_written", lambda f=f, before=before:
                     suite.eq(list((f.root / "launch_root" / "launches").iterdir()), before))
            else:
                case("N18_clean_refusal_recorded", lambda f=f, plan_pin=plan_pin, work=work:
                     suite.eq(M.read_pin(M.record_monitor_refused(f.ctx, plan_pin, str(work)))["schema"],
                              "MONITOR_REFUSED_ATTEMPT_RECORD_C2V001"))
        finally:
            terminate_handle(mon)
            terminate_handle(child)
    f = receipt_fixture(suite, "N18_unrelated_pid")
    f.ctx.system = FastSystem(f)
    unrelated = subprocess.Popen(["/bin/sleep", "120"], start_new_session=True)
    try:
        outdir = M.planned_outdir(f.ctx, f.name, 2, "P112")
        plan = {"name": f.name, "outdir": outdir, "receipt": outdir + ".receipt.json",
                "launch_json": outdir + ".receipt.json.launch.json", "spec": f.call["spec"]}
        case("N18_unrelated_pid_not_signalled", lambda: (
            suite.eq(M.stop_launch_failure(f.ctx, plan, unrelated.pid, False), None),
            suite.eq(unrelated.poll(), None)))
    finally:
        terminate_handle(unrelated)
    suite.interfaces["qualified_stop_scope"] = (
        "TESTED real ps and TERM against suite-created inert monitor/driver groups. "
        "Injected clock advances the 15/60-second bounds; real elapsed timeout duration is not asserted.")

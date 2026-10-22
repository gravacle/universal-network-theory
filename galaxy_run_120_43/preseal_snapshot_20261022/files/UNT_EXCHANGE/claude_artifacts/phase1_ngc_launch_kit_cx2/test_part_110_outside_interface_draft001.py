"""Outside-set stop, exclusion and c2v006 receipt-residence interface tests."""


def outside_interface_cases(suite):
    import json
    import os
    import subprocess
    import time
    from pathlib import Path
    M, case, fail = suite.module, suite.case, suite.refuses
    f = receipt_fixture(suite, "O01_in_actual_set", origin="KIT", name="S0_J0_SERIAL")
    case("O01_in_set_refuses", lambda: fail("OUTSIDE_STOP_IN_ACTUAL_SET", lambda: M.stop_outside_set(f.ctx, f.name)))
    for mismatch in (True, False):
        label = "O02_wrong_command" if mismatch else "O03_inert_target"
        f = receipt_fixture(suite, label, origin="KIT", name="S0_J0_SERIAL")
        f.ctx._fixture_calls = []
        f.ctx.system = M.SyntheticSystem({"mount_points": [f.ctx.cfg["run_volume"], str(Path(f.ctx.cfg["s0"]["run_root"]).parent)],
                                         "free_bytes": 1 << 50, "host_ram_bytes": M.RAM})
        driver = suite.raw_write(f.root / "inert_outside_driver.py", b"import time\ntime.sleep(120)\n")
        f.ctx.pins = dict(f.ctx.pins, driver=driver)
        outdir = M.planned_outdir(f.ctx, f.name, 2, "KIT")
        command = M.driver_command(f.ctx.pins, f.call["spec"], outdir)
        proc = subprocess.Popen(["/bin/sleep", "120"] if mismatch else command, env=M.child_env(),
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        try:
            time.sleep(0.1)
            lj = {"schema": M.MONITOR_SCHEMA + "_LAUNCH", "command": command, "child_pid": proc.pid,
                  "pins": {"driver": driver, "spec": f.call["spec"]}, "caps": M.first_caps(f.name),
                  "utc": f.rec["utc_start"], "retries_allowed": 0}
            lp = suite.raw_write(Path(outdir + ".receipt.json.launch.json"), M.encoded(lj))
            rec = dict(f.record, attempt=2, outdir=outdir, receipt=outdir + ".receipt.json",
                       launch_json=dict(lp, child_pid=proc.pid, utc=lj["utc"]), monitor_pid=os.getpid(), driver=driver)
            rp = Path(f.ctx.cfg["s0"]["launch_root"]) / "launches" / (f.name + "_LAUNCH_C2V003A_A2.json")
            suite.raw_write(rp, M.encoded(rec))
            if mismatch:
                case("O02_wrong_command_refuses", lambda: fail("OUTSIDE_STOP_TARGET_REFUSED",
                                                               lambda: M.stop_outside_set(f.ctx, f.name)))
                case("O02_unrelated_process_untouched", lambda: suite.eq(proc.poll(), None))
            else:
                def stopped():
                    result = M.read_pin(M.stop_outside_set(f.ctx, f.name))
                    suite.eq(result["schema"], "S0_OUTSIDE_SET_STOP_RECORD_C2V001")
                    suite.eq(result["result"] in ("KILLED_TERM", "KILLED_KILL"), True)
                    suite.eq(proc.poll() is not None, True)
                case("O03_inert_outside_target_stopped", stopped)
                def excluded():
                    raw, evidence = M.registry_bytes(f.ctx)
                    suite.eq(json.loads(raw)["calls"], [])
                    suite.eq(evidence["excluded_serials"][0]["name"], f.name)
                    suite.eq(len(evidence["excluded_serials"][0]["stop_records"]), 1)
                case("R04_outside_serial_excluded_and_listed", excluded)
        finally:
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait(timeout=3)
            else:
                proc.wait()
    f = receipt_fixture(suite, "R02_receipt_residence")
    result = M.close_attempt(f.ctx, f.name, 1)
    receipt = M.read_pin(result["receipt"])
    inside = suite.raw_write(Path(f.outdir) / "attempt_receipt_inside_synthetic.json", M.encoded(receipt))
    B = M.load_verified(M.REAL["builder"], "_p112_residence_proof_builder")
    cfg = B._receipt_cfg(M.RECEIPT_KEYS, M.STATUS_CLASSES)
    case("R02_inside_fixture_all_nine_roles", lambda: (
        suite.eq(B._receipt(inside, cfg, "synthetic inside")[1], "FINISHED|COMPLETED"),
        suite.eq(B._receipt(inside, cfg, "synthetic inside")[4]["rss_cap_bytes"], M.RAM),
        suite.eq(B._receipt(inside, cfg, "synthetic inside")[5]["theta_sha256"], receipt["theta_sha256"])))
    def outside_rejected():
        try:
            B._terminal([{"run_dir": f.outdir, "receipt": result["receipt"]}], cfg, "true sibling residence", False,
                        {"theta_sha256": receipt["theta_sha256"], "spec_sha256": receipt["spec_sha256"]})
        except B.Refused as e:
            suite.eq(e.code, "RECEIPT_NOT_IN_RUN_DIR")
            return
        raise AssertionError("c2v006 unexpectedly admitted sibling receipt")
    case("R02_true_sibling_requires_c2v007", outside_rejected)
    suite.interfaces["receipt_residence_demonstrated"] = (
        "TESTED c2v006 _receipt on an inside synthetic copy and _terminal rejecting the true sibling "
        "with RECEIPT_NOT_IN_RUN_DIR. No full assembly, v003g or slots access.")

"""Public CLI integration using synthetic tools, a passive fixture watch and ps."""


def live_launch_cases(suite):
    import json
    import os
    import subprocess
    import time
    from pathlib import Path
    M, case = suite.module, suite.case
    f = full_launch_fixture(suite, "LIVE_SYNTHETIC_LAUNCH")
    # Refuse before any child start if a fixture escaped the dedicated test tree.
    for key in ("driver", "monitor", "dry_harness"):
        suite.eq(f.overrides[key]["path"].startswith(str(suite.root) + "/"), True)
        suite.eq(f.overrides[key]["sha256"] != M.REAL[key]["sha256"], True)
    M.synthetic_fence(f.overrides, f.config_doc)
    system = M.SyntheticSystem(M.read_pin(f.synthetic)["system"])
    ctx = M.Context(f.config, system=system, synthetic_pins=f.overrides)
    ctx.synthetic_pin = f.synthetic
    case("T01_full_file_backed_context", lambda: suite.eq(
        [c["name"] for c in ctx.calls()], ["P1_M0001", "P1_F0", "P1_F1", "P1_F2", M.TWIN]))
    watch = subprocess.Popen([M.PY, "-I", "-B", f.watch["path"]], env=M.child_env(),
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    base = [M.PY, "-I", "-B", str(suite.tool_path)]
    common = ["--config", f.config["path"], "--config-sha256", f.config["sha256"],
              "--synthetic-pins", f.synthetic["path"], "--synthetic-pins-sha256", f.synthetic["sha256"]]
    def invoke(command, *extra):
        p = subprocess.run(base + [command] + common + list(extra), env=M.child_env(),
                           capture_output=True, text=True, timeout=35)
        suite.eq(p.returncode, 0)
        result = json.loads(p.stdout.strip().splitlines()[-1])
        suite.eq("P112_PRIVATE_SENTINEL_MUST_NOT_BE_READ" in p.stdout + p.stderr, False)
        return result
    launch_result = {}
    try:
        time.sleep(0.15)
        def do_launch():
            launch_result.update(invoke("launch", "--name", f.name, "--attempt", "1"))
            rec = M.read_pin(launch_result)
            suite.eq(rec["outcome"], "LAUNCH")
            suite.eq(rec["status_map_sha256"], M.STATUS_MAP_SHA)
        case("P09_public_launch_synthetic", do_launch)
        if not launch_result:
            return
        outdir = str(Path(f.config_doc["run_root"]) / "NGC_P1_P1_M0001_RUN_CX2V001_A1")
        sample_path = Path(outdir + ".solo.json")
        until = time.monotonic() + 15
        while not sample_path.is_file() and time.monotonic() < until:
            time.sleep(0.1)
        def sample_check():
            suite.eq(sample_path.is_file(), True)
            sample = M.read_pin(M.pin_of(sample_path))
            receipt = M.monitor_receipt(Path(outdir + ".receipt.json").read_bytes())
            suite.eq(sample["complete"], True)
            suite.eq(M.sample_value(sample, receipt), 0)
            suite.eq(M.timestamp(sample["first_utc"]) + 1 <= M.timestamp(receipt["utc_start"]) + 1, True)
            suite.eq(M.timestamp(sample["last_utc"]) > M.timestamp(receipt["utc_end"]), True)
        case("P09_live_sampler_lead_tail_zero", sample_check)
        # A small process-exit window remains after writing the sample.
        time.sleep(0.2)
        def do_close():
            result = invoke("close-attempt", "--name", f.name, "--attempt", "1")
            receipt = M.read_pin(result["receipt"])
            suite.eq(receipt["status_class"], "FINISHED")
            suite.eq(receipt["other_ngc_processes_max"], 0)
            suite.eq(receipt["pins"]["result"]["path"], outdir + "/result.json")
        case("C01_P09_public_close_synthetic", do_close)
        case("L04_public_status_without_writes", lambda: suite.eq(
            invoke("status")["schema"], "P112_STATUS_CX2V001"))
    finally:
        # Only the Popen handle of our inert fixture watch is stopped.
        watch.terminate()
        try:
            watch.wait(timeout=3)
        except subprocess.TimeoutExpired:
            watch.kill()
            watch.wait(timeout=3)
    suite.interfaces["live_synthetic_scope"] = (
        "TESTED public CLI with synthetic driver/dry/watch and verified monitor API wrapper. "
        "Production driver, certificates, mounted volumes and scientific behavior remain UNTESTED.")

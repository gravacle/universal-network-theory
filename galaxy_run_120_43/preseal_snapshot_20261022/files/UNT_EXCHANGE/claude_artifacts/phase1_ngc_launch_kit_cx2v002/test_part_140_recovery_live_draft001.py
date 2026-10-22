"""Public same-k recovery after a synthetic interruption or clean refusal."""


def recovery_live_cases(suite):
    import json
    import subprocess
    import time
    from pathlib import Path
    M = suite.module
    for mode in ("interrupted", "refused"):
        f = full_launch_fixture(suite, "RECOVERY_" + mode)
        helper = """import hashlib,json,sys,types
from pathlib import Path
tool,tool_sha,config,config_sha,syn,syn_sha,mode=sys.argv[1:]
raw=Path(tool).read_bytes()
assert hashlib.sha256(raw).hexdigest()==tool_sha
M=types.ModuleType("_p112_interruption_fixture");M.__file__=tool
exec(compile(raw,tool,"exec"),M.__dict__)
synthetic_pin={"path":syn,"sha256":syn_sha}
data=M.read_pin(synthetic_pin)
ctx=M.Context({"path":config,"sha256":config_sha},system=M.SyntheticSystem(data["system"]),synthetic_pins=data["pins"])
ctx.synthetic_pin=synthetic_pin
ctx.gate()
call=ctx.call("P1_M0001")
hist=M.history(ctx,call)
decision=M.next_attempt(call["name"],hist["records"],hist["actual"],hist["residuals"],hist["trailing_nonattempt"])
M.create_layout(ctx)
work=M.new_work(ctx,call["name"],decision["attempt"])
mp,m15=ctx.seed_check()
plan=M.make_plan(ctx,call,decision,work,mp,m15)
pp=ctx.write(str(work/"plan.json"),plan)
dry=M.run_dry(ctx,call,work)
ep=M.register_call(ctx,call,plan,dry,work,hist)
if mode=="interrupted":
 def broken_ps():raise M.Refusal("PS_FAILED")
 ctx.system.processes=broken_ps
 result=M.sampler(ctx,plan,str(work),poll_s=5)
 assert result["status"]=="FIRST_SAMPLE_FAILED_NO_SOLO_FILE"
else:
 with M.new_log(work/"monitor.stdout.txt"):pass
 with M.new_log(work/"monitor.stderr.txt"):pass
 result=M.record_monitor_refused(ctx,pp,str(work))
print(json.dumps({"entry":ep,"work":str(work),"result":result,"outdir":plan["outdir"]},sort_keys=True))
"""
        hp = suite.raw_write(f.root / "prepare_saved_interruption.py", helper.encode())
        watch = subprocess.Popen([M.PY, "-I", "-B", f.watch["path"]], env=M.child_env(),
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        common = ["--config", f.config["path"], "--config-sha256", f.config["sha256"],
                  "--synthetic-pins", f.synthetic["path"], "--synthetic-pins-sha256", f.synthetic["sha256"]]
        base = [M.PY, "-I", "-B", str(suite.tool_path)]
        saved = {}
        try:
            p = subprocess.run([M.PY, "-I", "-B", hp["path"], str(suite.tool_path), suite.tool_sha,
                                f.config["path"], f.config["sha256"], f.synthetic["path"], f.synthetic["sha256"], mode],
                               env=M.child_env(), capture_output=True, text=True, timeout=35)
            def first_check():
                suite.eq(p.returncode, 0)
                saved.update(json.loads(p.stdout.strip().splitlines()[-1]))
                suite.eq(Path(saved["outdir"] + ".solo.json").exists(), False)
                suite.eq(Path(saved["outdir"] + ".receipt.json.launch.json").exists(), False)
                suite.eq(M.pin_of(saved["entry"]["path"]), saved["entry"])
            suite.case("N04_public_" + mode + "_entry_without_monitor", first_check)
            if not saved:
                continue
            registry_before = sorted((f.root / "launch_root" / "registry").iterdir())
            p = subprocess.run(base + ["launch"] + common + ["--name", f.name, "--attempt", "1"],
                               env=M.child_env(), capture_output=True, text=True, timeout=35)
            result = {}
            def second_check():
                suite.eq(p.returncode, 0)
                result.update(json.loads(p.stdout.strip().splitlines()[-1]))
                suite.eq("ALREADY_REGISTERED_SAME_SPEC" in p.stderr, True)
                rec = M.read_pin(result)
                suite.eq(rec["attempt"], 1)
                suite.eq(rec["outcome"], "LAUNCH")
                suite.eq(rec["registry_entry"], saved["entry"])
                suite.eq(M.pin_of(saved["entry"]["path"]), saved["entry"])
                suite.eq(sorted((f.root / "launch_root" / "registry").iterdir()), registry_before)
                suite.eq(str(Path(rec["plan"]["path"]).parent) != saved["work"], True)
            suite.case("N04_public_" + mode + "_same_k_reuses_entry_new_work", second_check)
            if not result:
                continue
            until = time.monotonic() + 25
            sample_path = Path(saved["outdir"] + ".solo.json")
            while not sample_path.is_file() and time.monotonic() < until:
                time.sleep(0.1)
            suite.case("N04_public_" + mode + "_sampler_completed", lambda: suite.eq(sample_path.is_file(), True))
            time.sleep(0.2)
            p = subprocess.run(base + ["close-attempt"] + common + ["--name", f.name, "--attempt", "1"],
                               env=M.child_env(), capture_output=True, text=True, timeout=35)
            suite.case("N04_public_" + mode + "_closes_after_recovery",
                       lambda: suite.eq((p.returncode, json.loads(p.stdout.strip().splitlines()[-1])["status_class"]),
                                        (0, "FINISHED")))
        finally:
            if watch.poll() is None:
                watch.terminate()
                try:
                    watch.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    watch.kill()
                    watch.wait(timeout=3)
    suite.interfaces["same_k_recovery_scope"] = (
        "TESTED public launch after a separate synthetic invocation exits with a registered entry: "
        "first sampler ps failure, and a D7 monitor-refusal record. Both reuse the pinned entry at k=1, "
        "report ALREADY_REGISTERED_SAME_SPEC, use a new work directory and close successfully. "
        "No real scientific monitor or driver was started.")

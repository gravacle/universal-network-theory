# Root-invoked one-attempt launch path. No automatic retry occurs here.


def child_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("PYTHON")}
    env.update({key: "1" for key in THREAD_ENV})
    return env


def create_layout(ctx):
    root = Path(ctx.cfg["p112_launch_root"])
    need(root.is_dir() and os.path.realpath(root) == str(root), "LAUNCH_ROOT_REAL")
    for sub in ("registry", "launches", "work", "twin_kill", "outside_set_stop", "assembly"):
        p = root / sub
        if not p.exists():
            p.mkdir()
        need(p.is_dir() and os.path.realpath(p) == str(p), "LAUNCH_SUBDIR_REAL", sub)


def new_work(ctx, name, k):
    root = Path(ctx.cfg["p112_launch_root"]) / "work"
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    p = root / ("%s_A%d_%s_%d" % (name, k, stamp, os.getpid()))
    p.mkdir()
    return p


def new_log(path):
    f = open(path, "xb", buffering=0)
    f.write(("date -u: " + date_u() + "\n").encode())
    os.fsync(f.fileno())
    os.fchmod(f.fileno(), 0o444)
    return f


def run_dry(ctx, call, work):
    for key in ("driver", "dry_harness"):
        read_pin(ctx.pins[key], decode=False)
    folder = Path(work) / "dry"
    folder.mkdir()
    report, log = folder / "report", folder / "log.json"
    argv = [PY, "-I", "-B", ctx.pins["dry_harness"]["path"], ctx.pins["driver"]["path"],
            ctx.pins["driver"]["sha256"], call["spec"]["path"], call["spec"]["sha256"], str(report), str(log)]
    with new_log(Path(work) / "dry.stdout.txt") as stdout:
        proc = subprocess.run(argv, env=child_env(), stdout=stdout, stderr=subprocess.STDOUT)
        os.fsync(stdout.fileno())
    need(proc.returncode == 0, "DRY_HARNESS_EXIT")
    lp, rp = pin_of(log), pin_of(report / "NGC_SOURCE_BUILD_READINESS.json")
    verdict = dry_verdict(read_pin(lp), read_pin(rp), call["spec"], ctx.pins["driver"])
    verdict.update({"log": lp, "readiness": rp, "spec": call["spec"], "driver": ctx.pins["driver"]})
    return ctx.write(str(Path(work) / "dry_verdict.json"), verdict)


def watch_check(ctx):
    pin = ctx.get_vpin("WATCH_PIN", "MEMORY_WATCH")
    read_pin(pin, decode=False)
    rows = ctx.system.processes()
    need(any(has_arg(r["command"], pin["path"]) for r in rows), "MEMORY_WATCH_NOT_RUNNING")
    return pin


def own_process_command(ctx):
    rows = [r for r in ctx.system.processes() if r["pid"] == os.getpid()]
    need(len(rows) == 1, "INVOCATION_PROCESS_NOT_VISIBLE")
    return rows[0]["command"]


def make_plan(ctx, call, decision, work, m15_pin, m15):
    name, k = call["name"], decision["attempt"]
    outdir = planned_outdir(ctx, name, k, "P112")
    return {"schema": "UNT_P112_LAUNCH_PLAN_CX2V001", "name": name, "attempt": k,
            "kind": call["kind"], "alternative": call["alternative"], "key": call["key"],
            "point_key": call["point_key"], "theta_sha256": call["theta_sha256"],
            "spec": call["spec"], "pins": {k: ctx.pins[k] for k in ("driver", "monitor")},
            "outdir": outdir, "receipt": outdir + ".receipt.json", "launch_json": outdir + ".receipt.json.launch.json",
            "caps": decision["caps"], "caps_basis": {"rule": "A223 G25; first-attempt caps or identical retry / rule-(c)"},
            "solo_mode": decision["solo_mode"], "counted_rerun": decision["counted_rerun"],
            "rule_c_basis": decision["rule_c_basis"], "m15_record": m15_pin,
            "m15_epoch": m15["date_u_epoch_s"], "host_ram_bytes": ctx.system.ram(),
            "config": ctx.config_pin, "work": str(work), "invocation_utc": utc(), "date_u": date_u(),
            "invocation_pid": os.getpid(), "invocation_command": own_process_command(ctx),
            "synthetic": ctx.synthetic, "synthetic_pins": getattr(ctx, "synthetic_pin", None),
            "monitor_argv": monitor_command(ctx.pins, call["spec"], outdir, decision["caps"])}


def register_call(ctx, call, plan, dry_pin, work, hist):
    if call["origin"] == "KIT":
        return registered_entry(ctx, call)[1]
    path = own_registry_path(ctx, call["name"])
    if os.path.lexists(path):
        old_pin = pin_of(path)
        old = read_pin(old_pin)
        if hist["records"] or hist["residuals"]:
            need(old.get("spec") == call["spec"] and old.get("point_key") == call["point_key"] and
                 old.get("theta_sha256") == call["theta_sha256"] and
                 old.get("v006_spec_pin") == call["v006_spec_pin"] and
                 old.get("v006_handoff_pin") == call["v006_handoff_pin"], "REGISTRY_CALL_BINDING")
        else:
            entry_reuse(old, call, hist["records"], hist["refusals"], plan["attempt"])
        return old_pin
    need(not hist["records"] and not hist["residuals"], "RETRY_REGISTRY_ENTRY_MISSING")
    fc_pin = ctx.write(str(Path(work) / "fill_check.json"), call["fill_check"])
    tc = dict(call["theta_check"], schema="P112_THETA_CHECK_CX2V001", date_u=date_u())
    tc_pin = ctx.write(str(Path(work) / "theta_check.json"), tc)
    record = {key: call[key] for key in (
        "name", "kind", "alternative", "key", "point_key", "theta_sha256", "spec",
        "v006_spec_pin", "v006_handoff_pin", "handoff", "certificates")}
    record.update({"schema": "UNT_P112_LAUNCH_REGISTRY_ENTRY_CX2V001", "plan_output_primary": ctx.cfg["plan_output_primary"],
                   "fdplan": ctx.cfg["fdplan"], "driver": ctx.pins["driver"], "fill_check": fc_pin,
                   "dry_verdict": dry_pin, "theta_check": tc_pin, "registered_at_attempt": plan["attempt"],
                   "config": ctx.config_pin, "date_u": date_u()})
    return ctx.write(path, record)


def kit_kill_target(ctx, plan, monitor_pid=None):
    read_pin(ctx.pins["kit"], decode=False)
    argv = [PY, "-I", "-B", ctx.pins["kit"]["path"], "kill-target", "--launch-json", plan["launch_json"],
            "--spec-sha256", plan["spec"]["sha256"], "--expect-leaf", "8" if plan["name"] == TWIN else "1"]
    if monitor_pid is not None:
        argv += ["--mon-pid", str(monitor_pid)]
    p = subprocess.run(argv, env=child_env(), capture_output=True, text=True)
    if p.returncode == 1:
        return {"result": "ALREADY_ENDED", "pgid": None, "mon_pid_supplied": monitor_pid}
    if p.returncode != 0 or not p.stdout.strip().isdigit():
        return {"result": "NOT_KILLED_TARGET_REFUSED", "pgid": None, "mon_pid_supplied": monitor_pid}
    pid = int(p.stdout.strip())
    command = " ".join(driver_command(ctx.pins, plan["spec"], plan["outdir"]))
    predicate = lambda r: r["command"] == command and r["pgid"] == pid and (
        monitor_pid is None or r["ppid"] == monitor_pid)
    result = stop_qualified(ctx.system, pid, predicate, group=True)
    return {"result": result, "pgid": pid, "mon_pid_supplied": monitor_pid}


def stop_launch_failure(ctx, plan, monitor_pid, parsed):
    rows = ctx.system.processes()
    qualified = qualified_process(rows, monitor_pid, ctx.pins["monitor"]["path"], plan["outdir"], "monitor")
    monitor_stopped = False
    if not parsed and qualified is not None:
        command = qualified["command"]
        stop_qualified(ctx.system, monitor_pid, lambda r: r["command"] == command)
        monitor_stopped = True
    raw, lj = try_launch_json(plan["launch_json"])
    if lj is not None:
        stop = kit_kill_target(ctx, plan, None if monitor_stopped or qualified is None else monitor_pid)
    elif os.path.lexists(plan["launch_json"]):
        command = " ".join(driver_command(ctx.pins, plan["spec"], plan["outdir"]))
        leaders = [r for r in ctx.system.processes() if r["command"] == command and r["pid"] == r["pgid"]]
        results = []
        for row in leaders:
            result = stop_qualified(ctx.system, row["pid"], lambda r: r["command"] == command and r["pid"] == r["pgid"],
                                    group=True)
            results.append({"pgid": row["pid"], "result": result})
        stop = {"result": results[-1]["result"] if results else "NOT_KILLED_TARGET_REFUSED",
                "pgid": results[-1]["pgid"] if results else None, "orphan_stops": results,
                "mon_pid_supplied": None}
    else:
        need(not matching_monitors(ctx.system.processes(), ctx.pins["monitor"]["path"], plan["outdir"]),
             "MONITOR_STILL_ALIVE")
        return None
    start = ctx.system.monotonic()
    while ctx.system.monotonic() - start < 60:
        mount_first(ctx.cfg, "P112", ctx.system)
        if Path(plan["receipt"]).exists():
            break
        ctx.system.sleep(0.2)
    return stop


def write_launch_record(ctx, plan, plan_pin, entry_pin, monitor_pid, sampler_pid, watch_pid, checks, stop=None):
    name, k = plan["name"], plan["attempt"]
    need(not any(r["attempt"] == k for r in ctx.record_paths(name)), "ATTEMPT_ALREADY_RECORDED")
    mount_first(ctx.cfg, "P112", ctx.system)
    raw, lj = try_launch_json(plan["launch_json"])
    outcome = "LAUNCH" if checks and all(checks.values()) and stop is None else "MISLAUNCH"
    need(outcome == "LAUNCH" or os.path.lexists(plan["launch_json"]), "NO_MISLAUNCH_WITHOUT_LAUNCH_JSON")
    if raw is None and os.path.lexists(plan["launch_json"]):
        raw = Path(plan["launch_json"]).read_bytes()
    record = {key: plan[key] for key in ("name", "attempt", "outdir", "receipt", "spec", "caps",
              "caps_basis", "m15_record", "host_ram_bytes", "solo_mode", "counted_rerun", "rule_c_basis", "config")}
    record.update({"schema": "UNT_P112_" + outcome + "_RECORD_CX2V001", "outcome": outcome,
                   "launch_json": {"path": plan["launch_json"], "sha256": sha(raw) if raw is not None else None,
                                   "utc": (lj or {}).get("utc"), "child_pid": (lj or {}).get("child_pid")},
                   "driver": ctx.pins["driver"], "monitor": ctx.pins["monitor"], "monitor_pid": monitor_pid,
                   "sampler_pid": sampler_pid, "watch_pid": watch_pid, "registry_entry": entry_pin,
                   "launch_check": {"verdict": "CONFIRMED" if outcome == "LAUNCH" else "MISLAUNCH",
                                    "checks": checks, "failed": [k for k, v in checks.items() if not v]},
                   "plan": plan_pin, "status_map_sha256": STATUS_MAP_SHA, "date_u": date_u()})
    if stop is not None:
        record["stop"] = stop
    p = Path(ctx.cfg["p112_launch_root"]) / "launches" / ("P112_%s_%s_CX2V001_A%d.json" % (name, outcome, k))
    return ctx.write(str(p), record)


def finish_launch(ctx, plan, plan_pin, entry_pin, monitor_pid, sampler_pid, *, resume=False):
    mount_first(ctx.cfg, "P112", ctx.system)
    m15 = read_pin(plan["m15_record"])
    raw, lj, wait = wait_launch_json(plan["launch_json"], ctx.system)
    checks = launch_checks(lj, plan, m15) if lj is not None else {"launch_json_parseable": False}
    if all(checks.values()):
        watch_pid = None
        if plan["name"] == TWIN:
            read_pin(ctx.pins["twin_watch"], decode=False)
            argv = ["/bin/bash", ctx.pins["twin_watch"]["path"], "--launch-root", ctx.cfg["p112_launch_root"],
                    "--launch-json", plan["launch_json"], "--outdir", plan["outdir"],
                    "--twin-spec-sha256", plan["spec"]["sha256"], "--mon-pid", str(monitor_pid),
                    "--kill", "--max-wait-s", str(plan["caps"]["wall_cap_s"])]
            # Resume must never start two kill watches; qualify an existing one.
            live = [r for r in ctx.system.processes() if has_arg(r["command"], ctx.pins["twin_watch"]["path"]) and
                    has_arg(r["command"], "--outdir " + plan["outdir"])]
            need(len(live) <= 1, "TWIN_WATCH_DUPLICATE")
            if live:
                watch_pid = live[0]["pid"]
            elif not resume or not Path(plan["receipt"]).exists():
                with new_log(Path(plan["work"]) / ("twin_watch_resume.stdout.txt" if resume else "twin_watch.stdout.txt")) as f:
                    watch_pid = subprocess.Popen(argv, env=child_env(), stdout=f, stderr=subprocess.STDOUT,
                                                 start_new_session=True).pid
        return write_launch_record(ctx, plan, plan_pin, entry_pin, monitor_pid, sampler_pid, watch_pid, checks)
    stop = stop_launch_failure(ctx, plan, monitor_pid, lj is not None)
    if stop is None:
        return record_monitor_refused(ctx, plan_pin, plan["work"])
    return write_launch_record(ctx, plan, plan_pin, entry_pin, monitor_pid, sampler_pid, None, checks, stop)


def launch_resume(ctx, name, k):
    ctx.gate()
    mount_first(ctx.cfg, "P112", ctx.system)
    need(not any(r["attempt"] == k for r in ctx.record_paths(name)), "ATTEMPT_ALREADY_RECORDED")
    outdir = planned_outdir(ctx, name, k, "P112")
    need(os.path.lexists(outdir + ".receipt.json.launch.json"), "RESUME_LAUNCH_JSON_MISSING")
    candidates = []
    refused_plans = {r["plan_pin"]["path"] for r in refusal_records(ctx, name, ctx.records(name))}
    for p in (Path(ctx.cfg["p112_launch_root"]) / "work").glob(name + "_A%d_*/plan.json" % k):
        if str(p) in refused_plans:
            continue
        pin = pin_of(p)
        plan = read_pin(pin)
        inv = p.parent / "invocation.json"
        mp = p.parent / "monitor_pid.json"
        if plan.get("name") == name and plan.get("attempt") == k and inv.is_file() and mp.is_file():
            candidates.append((plan["invocation_utc"], plan, pin, strict_json(inv.read_bytes()), strict_json(mp.read_bytes())))
    need(candidates, "RESUME_INVOCATION_MISSING")
    _, plan, pin, invocation, mp = max(candidates, key=lambda x: x[0])
    need(plan["config"] == ctx.config_pin and plan["outdir"] == outdir and
         invocation["planned_monitor_argv"] == plan["monitor_argv"] and
         invocation.get("plan") == pin and mp.get("plan") == pin and
         plan["pins"] == {key: ctx.pins[key] for key in ("driver", "monitor")}, "RESUME_PLAN_BINDING")
    rows = ctx.system.processes()
    need(isinstance(invocation.get("invocation_command"), str), "RESUME_INVOCATION_COMMAND_MISSING")
    need(not any(r["pid"] == invocation["invocation_pid"] and r["command"] == invocation["invocation_command"]
                 for r in rows), "RESUME_INVOCATION_ALIVE")
    call = ctx.call(name)
    entry, entry_pin = registered_entry(ctx, call)
    need(plan["spec"] == call["spec"], "RESUME_SPEC_BINDING")
    return finish_launch(ctx, plan, pin, entry_pin, mp["monitor_pid"], invocation["sampler_pid"], resume=True)


def launch(ctx, name, attempt=None, dry=False, resume=False):
    if resume:
        need(not dry and type(attempt) is int, "RESUME_ARGUMENTS")
        return launch_resume(ctx, name, attempt)
    if not dry:
        ctx.gate()
    ctx.residuals()
    m15_pin, m15 = ctx.seed_check()
    call = ctx.call(name)
    hist = history(ctx, call)
    decision = next_attempt(name, hist["records"], hist["actual"], hist["residuals"], hist["trailing_nonattempt"])
    need(attempt is None or attempt == decision["attempt"], "ATTEMPT_NUMBER")
    outdir = planned_outdir(ctx, name, decision["attempt"], "P112")
    disk = disk_check(ctx.cfg, outdir, decision["caps"], ctx.system)
    need(ctx.system.ram() == RAM, "HOST_RAM_MISMATCH")
    watch_check(ctx)
    enforce_solo(ctx, decision["solo_mode"], requested_outdir=outdir)
    for key in ("driver", "monitor"):
        read_pin(ctx.pins[key], decode=False)
    check_monitor_command(monitor_command(ctx.pins, call["spec"], outdir, decision["caps"]),
                          ctx.pins, call["spec"], outdir, decision["caps"], name)
    create_layout(ctx)
    work = new_work(ctx, name, decision["attempt"])
    plan = make_plan(ctx, call, decision, work, m15_pin, m15)
    plan["disk_check"] = disk
    plan_pin = ctx.write(str(work / "plan.json"), plan)
    dry_pin = run_dry(ctx, call, work)
    if dry:
        return {"status": "DRY_NOT_LAUNCHED", "plan": plan_pin, "dry_verdict": dry_pin}
    entry_pin = register_call(ctx, call, plan, dry_pin, work, hist)
    sampler_argv = [PY, "-I", "-B", ctx.own_pin["path"], "_sampler", "--config", ctx.config_pin["path"],
                    "--config-sha256", ctx.config_pin["sha256"], "--plan", plan_pin["path"],
                    "--plan-sha256", plan_pin["sha256"], "--outdir", outdir, "--poll-s", "5"]
    if getattr(ctx, "synthetic_pin", None):
        sampler_argv += ["--synthetic-pins", ctx.synthetic_pin["path"], "--synthetic-pins-sha256", ctx.synthetic_pin["sha256"]]
    with new_log(work / "sampler.stdout.txt") as f:
        sampler_pid = subprocess.Popen(sampler_argv, env=child_env(), stdout=f, stderr=subprocess.STDOUT,
                                       start_new_session=True).pid
    first_path = work / "sampler_first_sample.json"
    start = ctx.system.monotonic()
    while not first_path.exists() and ctx.system.monotonic() - start < 60:
        ctx.system.sleep(0.05)
    need(first_path.is_file(), "SAMPLER_FIRST_SAMPLE_MISSING")
    first = strict_json(first_path.read_bytes())
    need(first.get("ok") is True, "SAMPLER_FIRST_SAMPLE_FAILED")
    remaining = 1.0 - (ctx.system.monotonic() - first["monotonic"])
    if remaining > 0:
        ctx.system.sleep(remaining)
    # Recheck all resource and solo predicates immediately before this single launch.
    disk_check(ctx.cfg, outdir, decision["caps"], ctx.system)
    enforce_solo(ctx, decision["solo_mode"], requested_outdir=outdir)
    invocation = {"schema": "P112_INVOCATION_CX2V001", "invocation_pid": os.getpid(),
                  "invocation_command": plan["invocation_command"],
                  "sampler_pid": sampler_pid, "planned_monitor_argv": plan["monitor_argv"],
                  "plan": plan_pin, "date_u": date_u()}
    ctx.write(str(work / "invocation.json"), invocation)
    with new_log(work / "monitor.stdout.txt") as so, new_log(work / "monitor.stderr.txt") as se:
        argv = ["/usr/bin/nohup"] + plan["monitor_argv"]
        proc = subprocess.Popen(argv, env=child_env(), stdout=so, stderr=se, start_new_session=True)
    ctx.write(str(work / "monitor_pid.json"), {"schema": "P112_MONITOR_PID_CX2V001",
              "monitor_pid": proc.pid, "plan": plan_pin, "date_u": date_u()})
    if not ctx.synthetic:
        subprocess.Popen(["/usr/bin/caffeinate", "-i", "-w", str(proc.pid)],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    return finish_launch(ctx, plan, plan_pin, entry_pin, proc.pid, sampler_pid)

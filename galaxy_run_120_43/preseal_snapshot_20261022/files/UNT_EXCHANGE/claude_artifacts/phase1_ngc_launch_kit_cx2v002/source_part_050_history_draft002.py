# Attempt custody and history. The absence decisions all follow mount_first.


def own_registry_path(ctx, name):
    return str(Path(ctx.cfg["p112_launch_root"]) / "registry" / ("P112_" + name + "_CX2V001.json"))


def registered_entry(ctx, call):
    if call.get("entry_pin") is not None:
        return call["entry"], call["entry_pin"]
    p = own_registry_path(ctx, call["name"])
    need(Path(p).is_file(), "REGISTRY_ENTRY_MISSING", call["name"])
    pin, entry = read_record(p)
    need(entry.get("schema") == "UNT_P112_LAUNCH_REGISTRY_ENTRY_CX2V001", "REGISTRY_SCHEMA")
    need(entry.get("name") == call["name"] and entry.get("spec") == call["spec"] and
         entry.get("point_key") == call["point_key"] and entry.get("theta_sha256") == call["theta_sha256"],
         "REGISTRY_CALL_BINDING")
    return entry, pin


def planned_origin(name, k, records, residuals):
    hit = [r for r in records if r["attempt"] == k]
    need(len(hit) <= 1, "ATTEMPT_RECORD_NOT_UNIQUE")
    if hit:
        return hit[0]["origin"]
    if not name.startswith("S0_"):
        return "P112"
    earlier = [r for r in records if r["attempt"] < k]
    takeover = (any(r["origin"] == "P112" or r["outcome"] == "LAUNCH" for r in earlier) or
                any(n == name and x < k for n, x in residuals))
    return "P112" if takeover else "KIT"


def planned_outdir(ctx, name, k, origin):
    need(NAME_RE.fullmatch(name) is not None and type(k) is int and k >= 1, "NAME_ATTEMPT")
    if origin == "P112":
        return str(Path(ctx.cfg["run_root"]) / ("NGC_P1_" + name + "_RUN_CX2V001_A%d" % k))
    # The kit's run_name_for spelling is NGC_P1_S0_<ROLE>_SERIAL_RUN...
    return str(Path(ctx.cfg["s0"]["run_root"]) / ("NGC_P1_" + name + "_RUN_C2V003A_A%d" % k))


def validate_record_location(ctx, rec):
    expected = planned_outdir(ctx, rec["name"], rec["attempt"], rec["origin"])
    need(rec["outdir"] == expected and rec["receipt"] == expected + ".receipt.json",
         "ATTEMPT_PATH_BINDING")
    need((rec.get("launch_json") or {}).get("path") == expected + ".receipt.json.launch.json",
         "ATTEMPT_LAUNCH_JSON_PATH")


def refusal_records(ctx, name, records):
    found = []
    expected_keys = ("schema", "name", "attempt", "launcher", "writer", "plan",
                     "monitor_stdout", "monitor_stderr", "absent", "date_u", "rule")
    for root, subdir, origin in ((ctx.cfg["p112_launch_root"], "launches", "P112"),
                                 (ctx.cfg["s0"]["launch_root"], "monitor_refused", "KIT")):
        folder = Path(root) / subdir
        if not folder.is_dir():
            continue
        stem = ("P112_" + name + "_MONITOR_REFUSED_CX2V001_A" if origin == "P112" else
                name + "_MONITOR_REFUSED_C2V003A_A")
        for p in sorted(folder.glob(stem + "*.json")):
            match = re.fullmatch(re.escape(stem) + r"([1-9][0-9]*)\.json", p.name)
            if not match:
                continue
            rec_pin, rec = read_record(p)
            keys(rec, expected_keys, "monitor_refused")
            k = int(match[1])
            need(rec["schema"] == "MONITOR_REFUSED_ATTEMPT_RECORD_C2V001" and
                 rec["name"] == name and rec["attempt"] == k, "MONITOR_REFUSED_RECORD_BINDING")
            need(rec["launcher"] == ("P112_CX2V001" if origin == "P112" else "KIT_C2V003A"),
                 "MONITOR_REFUSED_LAUNCHER")
            writer = {"name": TOOL_NAME, "sha256": ctx.own_pin["sha256"]} if origin == "P112" else {
                "name": "ROOT", "sha256": None}
            need(rec["writer"] == writer, "MONITOR_REFUSED_WRITER")
            plan = read_pin(rec["plan"])
            outdir = planned_outdir(ctx, name, k, origin)
            need(plan.get("outdir") == outdir and plan.get("attempt") == k, "MONITOR_REFUSED_PLAN")
            paths = absent_paths(outdir)
            keys(rec["absent"], paths, "monitor_refused.absent")
            need(rec["absent"] == paths, "MONITOR_REFUSED_ABSENT_PATHS")
            mount_first(ctx.cfg, origin, ctx.system)
            relaunched = (any(r["attempt"] == k for r in records) or
                          os.path.lexists(paths["receipt_stdout"]) or os.path.lexists(paths["receipt_stderr"]))
            if not relaunched:
                need(not any(os.path.lexists(p) for p in paths.values()), "MONITOR_REFUSED_ABSENT_EXISTS")
            for key in ("monitor_stdout", "monitor_stderr"):
                need(is_pin(rec[key]), "MONITOR_REFUSED_LOG_PIN_FORM")
                need(Path(rec[key]["path"]).parent == Path(rec["plan"]["path"]).parent and
                     Path(rec[key]["path"]).name == key.replace("_", ".") + ".txt",
                     "MONITOR_REFUSED_LOG_PATH")
                # 0782: permission is per refusal invocation, not the shared
                # same-k receipt paths. Hash only that old work directory.
                need(Path(rec[key]["path"]).is_file(), "WORK_LOG_MISSING")
                read_pin(rec[key], decode=False)
            found.append({"attempt": k, "origin": origin, "reason": "MONITOR_REFUSED",
                          "record_pin": rec_pin, "plan_pin": rec["plan"], "caps": plan["caps"],
                          "solo_mode": plan.get("solo_mode", False), "log_rehash_deferred": False})
    return found


def honor_residual(ctx, call, k, records, residuals, rows):
    name = call["name"]
    origin = planned_origin(name, k, records, residuals)
    mount_first(ctx.cfg, origin, ctx.system)
    outdir = planned_outdir(ctx, name, k, origin)
    paths = absent_paths(outdir)
    need(not os.path.lexists(paths["receipt"]), "RESIDUAL_RETRY_NOT_RESIDUAL")
    hits = [r for r in records if r["attempt"] == k]
    monitors = matching_monitors(rows, ctx.pins["monitor"]["path"], outdir)
    command = " ".join(driver_command(ctx.pins, call["spec"], outdir))
    need(not monitors and not any(r["command"] == command for r in rows),
         "RESIDUAL_ATTEMPT_PROCESS_ALIVE")
    if hits:
        rec = hits[0]
        need(live_monitor(rows, rec.get("monitor_pid"), rec["monitor"]["path"], outdir) is None,
             "RESIDUAL_RETRY_NOT_RESIDUAL")
        caps, solo = rec["caps"], rec.get("solo_mode", False)
    else:
        need(not os.path.lexists(paths["launch_json"]) and (
            os.path.lexists(paths["receipt_stdout"]) or os.path.lexists(paths["receipt_stderr"])),
            "RESIDUAL_RETRY_NOT_RESIDUAL")
        prior = history(ctx, call, before=k, rows=rows, inspect_next=False)
        # The root's line admits takeover even if the prior call was kit-owned.
        if prior["actual"] or prior["trailing_nonattempt"]:
            ownership = list(prior["records"])
            if origin == "KIT" and not any(r["outcome"] == "LAUNCH" for r in ownership):
                provisional = first_caps(name)
                decision = {"caps": provisional, "solo_mode": False}
            else:
                decision = next_attempt(name, ownership, prior["actual"], prior["residuals"],
                                        prior["trailing_nonattempt"])
            caps, solo = decision["caps"], decision["solo_mode"]
        else:
            caps, solo = first_caps(name), False
    return {"attempt": k, "origin": origin, "reason": "RESIDUAL_RETRY",
            "line": "RESIDUAL_RETRY %s %d" % (name, k), "outdir": outdir,
            "caps": caps, "solo_mode": solo}


@read_scope
def history(ctx, call, *, before=None, rows=None, inspect_next=True, assembly=False):
    name = call["name"]
    residuals = {(n, k) for n, k in ctx.residuals() if n == name and (before is None or k < before)}
    records = [r for r in ctx.records(name) if before is None or r["attempt"] < before]
    rows = ctx.system.processes() if rows is None else rows
    actual, nonattempts, closed_pins, trailing = [], [], [], None
    refusals = refusal_records(ctx, name, records)
    nonattempts.extend(r for r in refusals if before is None or r["attempt"] < before)
    ks = sorted({r["attempt"] for r in records} | {k for _, k in residuals})
    for k in ks:
        hits = [r for r in records if r["attempt"] == k]
        if (name, k) in residuals:
            nonattempt = honor_residual(ctx, call, k, records, residuals, rows)
            nonattempts.append(nonattempt)
            trailing = nonattempt
            continue
        rec = hits[0]
        validate_record_location(ctx, rec)
        mount_first(ctx.cfg, rec["origin"], ctx.system)
        receipt_path = rec["receipt"]
        if not Path(receipt_path).is_file():
            live = live_monitor(rows, rec.get("monitor_pid"), rec["monitor"]["path"], rec["outdir"])
            raise Refusal("ATTEMPT_ACTIVE" if live else "MONITOR_ENDED_NO_RECEIPT", (name, k))
        monitor_pin, monitor_raw = read_record(receipt_path, decode=False)
        monitor = monitor_receipt(monitor_raw)
        is_directory = Path(rec["outdir"]).is_dir() and os.path.realpath(rec["outdir"]) == rec["outdir"]
        spec_match = monitor.get("pins", {}).get("spec", {}).get("sha256") == call["spec"]["sha256"]
        if not is_directory or not spec_match:
            nonattempt = {"attempt": k, "origin": rec["origin"], "reason": "NO_RUN_DIRECTORY" if not is_directory else "OFF_SPEC",
                          "record_pin": rec["record_pin"], "monitor_receipt": monitor_pin,
                          "caps": rec["caps"], "solo_mode": rec.get("solo_mode", False)}
            nonattempts.append(nonattempt)
            trailing = nonattempt
            continue
        path = rec["outdir"] + ".attempt_receipt.json"
        need(Path(path).is_file(), "ATTEMPT_NEEDS_CLOSE", (name, k))
        pin, closed_raw = read_record(path, decode=False)
        closed_pins.append(pin)
        if not assembly:
            obj = strict_json(closed_raw)
            need(obj.get("schema") == "STEP5_ATTEMPT_RECEIPT_C2V001" and
                 obj.get("call", {}).get("name") == name and obj.get("attempt") == k and
                 obj.get("spec_sha256") == call["spec"]["sha256"] and
                 obj.get("theta_sha256") == call["theta_sha256"], "ATTEMPT_RECEIPT_BINDING")
            actual.append(dict(obj, receipt_pin=pin))
        trailing = None
    if inspect_next:
        next_k = max(ks, default=0) + 1
        origin = planned_origin(name, next_k, records, residuals)
        mount_first(ctx.cfg, origin, ctx.system)
        outdir = planned_outdir(ctx, name, next_k, origin)
        paths = absent_paths(outdir)
        if os.path.lexists(paths["launch_json"]):
            raise Refusal("LAUNCH_RECORD_MISSING", (name, next_k))
        if os.path.lexists(paths["receipt_stdout"]) or os.path.lexists(paths["receipt_stderr"]):
            raise Refusal("MONITOR_STARTED_NO_LAUNCH_JSON", (name, next_k))
    streak = 0
    # Same-k refusals are non-attempts but do not separate actual pairs.
    actual_ks = {r["attempt"] for r in actual}
    for k in sorted(set(ks) | {r["attempt"] for r in refusals}, reverse=True):
        if k in actual_ks:
            break
        streak += sum(1 for r in nonattempts if r["attempt"] == k)
    return {"records": records, "actual": actual, "closed_pins": closed_pins, "nonattempts": nonattempts,
            "residuals": residuals, "trailing_nonattempt": trailing,
            "consecutive_nonattempts": streak, "refusals": refusals}


@read_scope
def record_monitor_refused(ctx, plan_pin, work):
    ctx.gate()
    guard_record(plan_pin["path"])
    plan = read_pin(plan_pin)
    need(plan.get("schema") == "UNT_P112_LAUNCH_PLAN_CX2V001", "PLAN_SCHEMA")
    need(plan["config"] == ctx.config_pin, "PLAN_CONFIG_BINDING")
    name, k, outdir = plan["name"], plan["attempt"], plan["outdir"]
    need(outdir == planned_outdir(ctx, name, k, "P112"), "PLAN_OUTDIR_BINDING")
    mount_first(ctx.cfg, "P112", ctx.system)
    paths = absent_paths(outdir)
    need(not matching_monitors(ctx.system.processes(), ctx.pins["monitor"]["path"], outdir), "MONITOR_STILL_ALIVE")
    if not os.path.lexists(paths["launch_json"]) and (
            os.path.lexists(paths["receipt_stdout"]) or os.path.lexists(paths["receipt_stderr"])):
        raise Refusal("MONITOR_STARTED_NO_LAUNCH_JSON")
    need(not any(os.path.lexists(p) for p in paths.values()), "MONITOR_REFUSED_ABSENT_EXISTS")
    path = str(Path(ctx.cfg["p112_launch_root"]) / "launches" /
               ("P112_%s_MONITOR_REFUSED_CX2V001_A%d.json" % (name, k)))
    need(not os.path.lexists(path), "MONITOR_REFUSED_TWICE")
    need(Path(plan_pin["path"]).parent == Path(work), "MONITOR_REFUSED_WORK")
    rec = {"schema": "MONITOR_REFUSED_ATTEMPT_RECORD_C2V001", "name": name, "attempt": k,
           "launcher": "P112_CX2V001", "writer": {"name": TOOL_NAME, "sha256": ctx.own_pin["sha256"]},
           "plan": plan_pin, "monitor_stdout": pin_of(str(Path(work) / "monitor.stdout.txt")),
           "monitor_stderr": pin_of(str(Path(work) / "monitor.stderr.txt")), "absent": paths,
           "date_u": date_u(), "rule": "A223 D7: no monitor launch or output; k is not consumed."}
    return ctx.write(path, rec)


@read_scope
def status(ctx):
    result = []
    try:
        ctx.residuals()
    except Refusal as e:
        return {"status": e.code, "detail": e.detail}
    for call in ctx.calls():
        try:
            h = history(ctx, call)
            terminal = terminal_prefix(h["actual"], call["name"])
            decision = None
            problem = None
            if terminal is None:
                try:
                    decision = next_attempt(call["name"], h["records"], h["actual"], h["residuals"],
                                            h["trailing_nonattempt"])
                except Refusal as e:
                    problem = e.code
            result.append({"name": call["name"], "status": problem or ("TERMINAL" if terminal else "READY"),
                           "attempts": [{"attempt": a["attempt"], "raw_status": a["raw_status"],
                                         "status_class": a["status_class"]} for a in h["actual"]],
                           "terminal": terminal, "next": decision, "nonattempts": h["nonattempts"],
                           "consecutive_nonattempts": h["consecutive_nonattempts"]})
        except Refusal as e:
            result.append({"name": call["name"], "status": e.code, "detail": e.detail})
    return {"schema": "P112_STATUS_CX2V001", "calls": result, "date_u": date_u(),
            "advisory": True, "launch_authorized": False}

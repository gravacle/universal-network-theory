# Receipt projection, actual-set registry assembly and the one cutoff copy.


def bound_stop_record(ctx, record, launch_pin):
    if record["name"] != TWIN:
        return None, None
    root = ctx.cfg["p112_launch_root"] if record["origin"] == "P112" else ctx.cfg["s0"]["launch_root"]
    folder = Path(root) / "twin_kill"
    if not folder.is_dir():
        return None, None
    hits = []
    for p in sorted(folder.glob("TWIN_KILL_RECORD_*.json")):
        # No run files are followed; these are kit records in the launch root.
        pin = pin_of(p)
        doc = read_pin(pin)
        if doc.get("outdir") == record["outdir"]:
            need(doc.get("reason") == "ITERATION_0001_COMPLETED_AND_SIDECAR" and
                 (doc.get("launch_json") or {}).get("sha256") == launch_pin["sha256"],
                 "TWIN_STOP_NOT_BOUND")
            hits.append((doc, pin))
    need(len(hits) <= 1, "TWIN_STOP_NOT_UNIQUE")
    return hits[0] if hits else (None, None)


def close_attempt(ctx, name, k):
    ctx.gate()
    records = ctx.records(name)
    hits = [r for r in records if r["attempt"] == k]
    origin = planned_origin(name, k, records, ctx.residuals())
    volume = mount_first(ctx.cfg, origin, ctx.system)
    outdir = planned_outdir(ctx, name, k, origin)
    if not hits:
        need(not os.path.lexists(outdir + ".receipt.json.launch.json"), "LAUNCH_RECORD_MISSING")
        raise Refusal("ATTEMPT_RECORD_MISSING")
    need(len(hits) == 1, "ATTEMPT_RECORD_NOT_UNIQUE")
    record = hits[0]
    validate_record_location(ctx, record)
    rows = ctx.system.processes()
    if not Path(record["receipt"]).is_file():
        live = qualified_process(rows, record.get("monitor_pid"), record["monitor"]["path"], outdir, "monitor")
        raise Refusal("MONITOR_RECEIPT_MISSING" if live else "MONITOR_ENDED_NO_RECEIPT")
    need((name, k) not in ctx.residuals(), "RESIDUAL_RETRY_NOT_RESIDUAL")
    receipt_pin = pin_of(record["receipt"])
    monitor = monitor_receipt(Path(record["receipt"]).read_bytes())
    if name == TWIN:
        need(qualified_process(rows, record.get("watch_pid"), ctx.pins["twin_watch"]["path"], outdir, "watch") is None,
             "TWIN_WATCH_STILL_ALIVE")
    if origin == "P112":
        need(qualified_process(rows, record.get("sampler_pid"), ctx.own_pin["path"], outdir, "sampler") is None,
             "SAMPLER_STILL_ALIVE")
    # Mapping precedes every receipt write, including kit receipts.
    call = ctx.call(name)
    entry, entry_pin = registered_entry(ctx, call)
    need(Path(outdir).is_dir() and os.path.realpath(outdir) == outdir, "NOT_AN_ATTEMPT", "NO_RUN_DIRECTORY")
    need(monitor.get("pins", {}).get("spec", {}).get("sha256") ==
         entry["spec"]["sha256"] == ctx.get_vpin("SPEC_PIN", name)["sha256"],
         "NOT_AN_ATTEMPT", "OFF_SPEC")
    host_ram = ctx.system.ram()
    need(host_ram == (record.get("host_ram_bytes") if origin == "P112" else RAM) == RAM, "HOST_RAM_MISMATCH")
    launch_path = outdir + ".receipt.json.launch.json"
    launch_pin = pin_of(launch_path)
    lj = read_pin(launch_pin)
    need(record["launch_json"].get("sha256") in (None, launch_pin["sha256"]), "LAUNCH_JSON_RECORD_PIN")
    need(monitor.get("child_pid") == lj.get("child_pid"), "MONITOR_CHILD_BINDING")
    need(monitor.get("pins", {}).get("driver") == ctx.pins["driver"] and
         monitor.get("pins", {}).get("monitor") == ctx.pins["monitor"], "MONITOR_TOOL_PINS")
    stop, stop_pin = bound_stop_record(ctx, record, launch_pin)
    raw, cls = raw_status(monitor, name=name, attempt=k, outdir=outdir, receipt=record["receipt"],
                         launch_pin=launch_pin, child_pid=monitor["child_pid"],
                         mislaunch=record if record["outcome"] == "MISLAUNCH" else None, stop=stop)
    sample, sample_pin = None, None
    sp = outdir + ".solo.json"
    if Path(sp).is_file():
        sample_pin = pin_of(sp)
        sample = read_pin(sample_pin)
        need(sample.get("schema") == "STEP5_SOLO_SAMPLE_CX2V001" and
             sample.get("name") == name and sample.get("attempt") == k and sample.get("outdir") == outdir and
             sample.get("declared_list_sha256") == DECLARED_LIST_SHA, "SOLO_SAMPLE_BINDING")
    timestamp(monitor["utc_end"], whole=True)
    timestamp(lj["utc"], whole=True)
    result = {
        "schema": "STEP5_ATTEMPT_RECEIPT_C2V001", "raw_status": raw, "status_class": cls,
        "time_utc": monitor["utc_end"], "launch_utc": lj["utc"],
        "spec_sha256": monitor["pins"]["spec"]["sha256"], "theta_sha256": call["theta_sha256"],
        "point_key": call["point_key"], **{key: monitor["caps"][key] for key in CAPS["serial"]},
        "host_ram_bytes": host_ram, "other_ngc_processes_max": sample_value(sample, monitor),
        "call": {key: call[key] for key in ("name", "kind", "alternative", "key")}, "attempt": k, "run_dir": outdir,
        "solo_mode": record.get("solo_mode", False), "counted_rerun": record.get("counted_rerun", False),
        "run_volume_at_close": {"mount_point": volume, "mounted": True, "free_bytes": ctx.system.free(volume)},
        "pins": {"monitor_receipt": receipt_pin, "launch_json": launch_pin, "launch_record": record["record_pin"],
                 "registry_entry": entry_pin, "solo_sample": sample_pin, "stop_record": stop_pin,
                 "result": monitor.get("result"), "status_map_sha256": STATUS_MAP_SHA,
                 "config": ctx.config_pin, "writer": ctx.own_pin},
        "date_u": date_u()}
    path = outdir + ".attempt_receipt.json"
    need(not os.path.lexists(path), "ATTEMPT_ALREADY_CLOSED")
    pin = ctx.write(path, result)
    cutoff = maybe_cutoff(ctx)
    return {"receipt": pin, "cutoff": cutoff, "raw_status": raw, "status_class": cls}


def terminal_set(ctx):
    terms = []
    for call in ctx.calls():
        h = history(ctx, call, inspect_next=False)
        term = terminal_prefix(h["actual"], call["name"])
        if term is None:
            return None
        need(term["index"] == len(h["actual"]) - 1, "ATTEMPT_AFTER_TERMINAL", call["name"])
        receipt = h["actual"][term["index"]]
        terms.append({"name": call["name"], "time_utc": receipt["time_utc"],
                      "receipt": receipt["receipt_pin"], "disposition": term["disposition"]})
    return terms


def cutoff_path(ctx):
    return str(Path(ctx.cfg["p112_launch_root"]) / "assembly" / "STEP4_CUTOFF_RECORD_C2V001.json")


def write_cutoff(ctx, terms):
    ctx.gate()
    need(not os.path.lexists(cutoff_path(ctx)), "CUTOFF_ALREADY_WRITTEN")
    need(terms, "TERMINAL_SET_EMPTY")
    latest = max(terms, key=lambda t: timestamp(t["time_utc"], whole=True))["time_utc"]
    raw = read_v006(ctx.cfg["v006"])
    digest = sha(raw)
    folder = Path(ctx.cfg["v006_copy_dir"])
    need(folder.is_dir() and os.path.realpath(folder) == str(folder), "CUTOFF_COPY_DIR")
    p = folder / ("V006_CUTOFF_COPY_" + digest + ".md")
    if os.path.lexists(p):
        need(p.is_file() and p.read_bytes() == raw, "CUTOFF_COPY_EXISTS_DIFFERENT")
    else:
        write_x_bytes(p, raw)  # Exact byte copy; no header can be added.
    copied = p.read_bytes()
    need(sha(copied) == digest and len(copied) == len(raw), "CUTOFF_COPY_VERIFY")
    record = {"schema": "STEP4_CUTOFF_RECORD_C2V001", "T": latest,
              "terminal_attempt_receipts": [t["receipt"] for t in terms],
              "copy": {"path": str(p), "sha256": digest, "bytes": len(raw)},
              "precheck_summary": terms, "date_u": date_u(), "advisory": True}
    return ctx.write(cutoff_path(ctx), record)


def maybe_cutoff(ctx):
    if os.path.lexists(cutoff_path(ctx)):
        return {"status": "ALREADY_WRITTEN", "pin": pin_of(cutoff_path(ctx))}
    try:
        terms = terminal_set(ctx)
    except Refusal as e:
        return {"status": "NOT_READY", "reason": e.code}
    return write_cutoff(ctx, terms) if terms else {"status": "NOT_READY"}


def outside_stop_records(ctx, name):
    folder = Path(ctx.cfg["p112_launch_root"]) / "outside_set_stop"
    if not folder.is_dir():
        return []
    result = []
    for p in sorted(folder.glob(name + "_A*_CX2V001.json")):
        pin = pin_of(p)
        doc = read_pin(pin)
        need(doc.get("schema") == "S0_OUTSIDE_SET_STOP_RECORD_C2V001" and doc.get("name") == name,
             "OUTSIDE_STOP_SCHEMA")
        need(doc.get("plan_output_primary") == ctx.cfg["plan_output_primary"] and
             doc.get("fdplan") == ctx.cfg["fdplan"], "OUTSIDE_STOP_MAPPING_PINS")
        result.append((doc, pin))
    return result


def registry_bytes(ctx):
    ctx.residuals()  # A malformed line refuses assembly, not just launch.
    calls, sources, mappings, excluded, nonattempts = [], [], [], [], []
    for call in ctx.calls():
        h = history(ctx, call, assembly=True)
        entry, pin = registered_entry(ctx, call)
        calls.append({"alternative": call["alternative"], "kind": call["kind"], "key": call["key"],
                      "theta_sha256": call["theta_sha256"], "spec_sha256": entry["spec"]["sha256"]})
        sources.extend([pin] + h["closed_pins"] + [r["record_pin"] for r in h["records"]])
        nonattempts.extend(dict(n, name=call["name"]) for n in h["nonattempts"])
        if call["origin"] == "KIT" and call["kind"] == "MEMBER":
            mappings.append({"name": call["name"], "key": call["key"], "theta_check": call["theta_check"]})
    actual_names = {c["name"] for c in ctx.calls()}
    for name, (entry, pin) in ctx.kit_entries().items():
        if name in actual_names:
            continue
        stops = outside_stop_records(ctx, name)
        need(stops, "OUTSIDE_SET_STOP_REQUIRED", name)
        excluded.append({"name": name, "registry_entry": pin, "stop_records": [p for _, p in stops]})
        sources.extend([pin] + [p for _, p in stops])
    doc = {"schema": "STEP5_LAUNCH_REGISTRY_C2V003", "phase": "PHASE_1", "calls": calls}
    evidence = {"schema": "STEP5_REGISTRY_ASSEMBLY_RECORD_CX2V001", "sources": sources,
                "plan_output_primary": ctx.cfg["plan_output_primary"], "fdplan": ctx.cfg["fdplan"],
                "selection": ctx.cfg["selection"], "plan_build_record": ctx.cfg["plan_build_record"],
                "v006_sha256": sha(ctx.v006_raw), "s0_member_mappings": mappings,
                "excluded_serials": excluded, "nonattempts": nonattempts, "date_u": date_u()}
    return encoded(doc), evidence


def assemble_registry(ctx, verify=False):
    ctx.gate()
    raw, evidence = registry_bytes(ctx)
    folder = Path(ctx.cfg["p112_launch_root"]) / "assembly"
    p = folder / "STEP5_LAUNCH_REGISTRY_PHASE1_CX2V001.json"
    if verify:
        need(p.is_file() and p.read_bytes() == raw, "REGISTRY_BYTE_VERIFY")
        # Verification is gated even though it produces no record.
        return {"status": "VERIFIED", "registry": pin_of(p)}
    record_path = folder / "STEP5_REGISTRY_ASSEMBLY_RECORD_CX2V001.json"
    need(not os.path.lexists(p) and not os.path.lexists(record_path), "ASSEMBLY_ALREADY_EXISTS")
    # Registry is an exact c2v006 schema and therefore cannot carry date_u.
    pin = write_x_bytes(p, raw)
    evidence["registry"] = pin
    return {"registry": pin, "assembly_record": ctx.write(str(record_path), evidence)}

# Command surface and explicit synthetic execution fence.


class SyntheticSystem(System):
    synthetic = True

    def __init__(self, fixture):
        keys(fixture, ("mount_points", "free_bytes", "host_ram_bytes"), "synthetic.system")
        self.fixture = fixture
        for p in fixture["mount_points"]:
            path_rules(p, "synthetic mount")
            need(not p.startswith("/Volumes"), "SYNTHETIC_VOLUMES")

    def mounted(self, volume):
        return volume in self.fixture["mount_points"] and Path(volume).is_dir() and os.path.realpath(volume) == volume

    def free(self, volume):
        return self.fixture["free_bytes"]

    def ram(self):
        return self.fixture["host_ram_bytes"]


@read_scope
def stop_outside_set(ctx, name, attempt=None):
    ctx.gate()
    need(name in ("S0_SEED_SERIAL", "S0_J0_SERIAL", "S0_J1_SERIAL", "S0_J2_SERIAL"), "OUTSIDE_STOP_NAME")
    need(name not in {c["name"] for c in ctx.calls()}, "OUTSIDE_STOP_IN_ACTUAL_SET")
    records = ctx.records(name)
    need(records, "OUTSIDE_STOP_NO_RECORD")
    record = max(records, key=lambda r: r["attempt"]) if attempt is None else next(
        (r for r in records if r["attempt"] == attempt), None)
    need(record is not None, "OUTSIDE_STOP_ATTEMPT")
    mount_first(ctx.cfg, record["origin"], ctx.system)
    validate_record_location(ctx, record)
    entry, entry_pin = ctx.kit_entries()[name]
    read_pin(entry["spec"])
    need(entry["spec"] == ctx.get_vpin("SPEC_PIN", name), "OUTSIDE_STOP_SPEC_PIN")
    plan = {"name": name, "launch_json": record["outdir"] + ".receipt.json.launch.json",
            "outdir": record["outdir"], "spec": entry["spec"]}
    result = kit_kill_target(ctx, plan, record["monitor_pid"])
    need(result["result"] != "NOT_KILLED_TARGET_REFUSED", "OUTSIDE_STOP_TARGET_REFUSED")
    rec = {"schema": "S0_OUTSIDE_SET_STOP_RECORD_C2V001", "name": name, "attempt": record["attempt"],
           "launch_json": read_record(plan["launch_json"], decode=False)[0], "outdir": record["outdir"], "pgid": result["pgid"],
           "result": result["result"], "plan_output_primary": ctx.cfg["plan_output_primary"],
           "fdplan": ctx.cfg["fdplan"], "rule": "A133 L103: outputs kept and never read.", "date_u": date_u()}
    p = Path(ctx.cfg["p112_launch_root"]) / "outside_set_stop" / (
        "%s_A%d_CX2V001.json" % (name, record["attempt"]))
    return ctx.write(str(p), rec)


@read_scope
def cli(argv=None):
    ap = argparse.ArgumentParser(description="P-112: root-invoked Phase-1 launch custody, A223 / 0782.")
    ap.add_argument("command", choices=("launch", "close-attempt", "assemble-registry", "stop-outside-set",
                                        "record-monitor-refused", "status", "_sampler"))
    ap.add_argument("--config", required=True)
    ap.add_argument("--config-sha256", required=True)
    ap.add_argument("--name")
    ap.add_argument("--attempt", type=int)
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--plan")
    ap.add_argument("--plan-sha256")
    ap.add_argument("--outdir")
    ap.add_argument("--work")
    ap.add_argument("--poll-s", type=float, default=5)
    ap.add_argument("--synthetic-pins")
    ap.add_argument("--synthetic-pins-sha256")
    args = ap.parse_args(argv)
    try:
        synthetic_pin, overrides, system = None, None, None
        if args.synthetic_pins:
            synthetic_pin = {"path": args.synthetic_pins, "sha256": args.synthetic_pins_sha256}
            data = read_pin(synthetic_pin)
            keys(data, ("schema", "pins", "system", "date_u"), "synthetic manifest")
            need(data["schema"] == "P112_SYNTHETIC_PINS_CX2V001", "SYNTHETIC_SCHEMA")
            overrides, system = data["pins"], SyntheticSystem(data["system"])
        else:
            need(args.synthetic_pins_sha256 is None, "SYNTHETIC_SHA_WITHOUT_FILE")
        ctx = Context({"path": args.config, "sha256": args.config_sha256}, system=system, synthetic_pins=overrides)
        ctx.synthetic_pin = synthetic_pin
        need(not args.dry or args.command == "launch", "DRY_COMMAND")
        need(not args.resume or args.command == "launch", "RESUME_COMMAND")
        need(not args.verify or args.command == "assemble-registry", "VERIFY_COMMAND")
        if args.command in ("launch", "close-attempt", "stop-outside-set"):
            need(args.name is not None and NAME_RE.fullmatch(args.name), "NAME_REQUIRED")
        if args.command == "launch":
            result = launch(ctx, args.name, args.attempt, args.dry, args.resume)
        elif args.command == "close-attempt":
            need(type(args.attempt) is int and args.attempt >= 1, "ATTEMPT_REQUIRED")
            result = close_attempt(ctx, args.name, args.attempt)
        elif args.command == "assemble-registry":
            result = assemble_registry(ctx, args.verify)
        elif args.command == "stop-outside-set":
            result = stop_outside_set(ctx, args.name, args.attempt)
        elif args.command == "record-monitor-refused":
            need(args.plan and args.plan_sha256 and args.work, "REFUSAL_ARGUMENTS")
            result = record_monitor_refused(ctx, {"path": args.plan, "sha256": args.plan_sha256}, args.work)
        elif args.command == "_sampler":
            need(args.plan and args.plan_sha256 and args.outdir, "SAMPLER_ARGUMENTS")
            guard_record(args.plan)
            plan = read_pin({"path": args.plan, "sha256": args.plan_sha256})
            need(plan["outdir"] == args.outdir, "SAMPLER_OUTDIR")
            result = sampler(ctx, plan, plan["work"], poll_s=args.poll_s)
        else:
            result = status(ctx)
        print(json.dumps(result, sort_keys=True, allow_nan=False))
        return 0
    except (Refusal, OSError, KeyError, TypeError, ValueError) as e:
        print(json.dumps({"status": "REFUSED", "code": e.code if isinstance(e, Refusal) else type(e).__name__,
                          "detail": str(e)}, sort_keys=True))
        return 2


if __name__ == "__main__":
    sys.exit(cli())

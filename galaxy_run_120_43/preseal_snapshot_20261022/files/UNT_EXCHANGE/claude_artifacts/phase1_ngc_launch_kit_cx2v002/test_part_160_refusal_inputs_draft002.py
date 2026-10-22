"""Malformed-input and configuration refusals; fixtures never replace old bytes."""


def refusal_input_cases(suite):
    import contextlib
    import copy
    import io
    import json
    from pathlib import Path
    M, case, fail = suite.module, suite.case, suite.refuses
    def bad(code, action):
        case("REFUSE_" + code, lambda: fail(code, action))
    bad("JSON_DUPLICATE_KEY", lambda: M.strict_json(b'{"a":1,"a":2}'))
    bad("JSON_NONFINITE", lambda: M.strict_json(b'{"a":NaN}'))
    bad("JSON_PARSE", lambda: M.strict_json(b'{'))
    bad("PIN_FORM", lambda: M.read_pin({}))
    bad("UTC_FORMAT", lambda: M.timestamp("2026-13-01T00:00:00Z"))
    bad("THETA_NOT_NUMERIC", lambda: M.fhex("1.0", "coordinate"))
    bad("THETA_NONFINITE", lambda: M.fhex(float("inf"), "coordinate"))
    bad("MISSING_FIELD", lambda: M.dig({}, ("physical", "gamma")))
    bad("OUTPUT_ABSOLUTE", lambda: M.write_x_bytes("relative.json", b"{}"))
    bad("RECORD_DATE_U", lambda: M.write_x(str(suite.root / "undated.json"), {}))
    bad("PATH_ABSOLUTE_NORMALIZED", lambda: M.path_rules("/synthetic/../invalid"))
    bad("PATH_CODEX", lambda: M.path_rules(str(Path.home() / ".codex" / "DO_NOT_OPEN")))
    bad("PATH_PROTECTED_TREE", lambda: M.path_rules("/synthetic/UNT_INTERNAL_RUNS/DO_NOT_OPEN"))
    bad("PATH_UVT", lambda: M.path_rules("/synthetic/UVT_DO_NOT_OPEN"))
    volume = suite.root / "guard_volume"
    volume.mkdir()
    alias = suite.root / "guard_alias"
    alias.symlink_to(volume, target_is_directory=True)
    bad("OUTPUT_PARENT_SYMLINK", lambda: M.write_x_bytes(alias / "new.json", b"{}"))
    M.READ_RUN_ROOTS.add(str(volume))
    bad("FORBIDDEN_OUTDIR_READ", lambda: M.guard_read(volume / "NGC_RUN" / "anything.txt"))
    bad("PS_DUPLICATE_PID", lambda: M.parse_ps("2 1 2 a\n2 1 2 b\n"))
    case("B4_PS_COMMAND_FALLBACK", lambda: suite.eq(M.command_argv({"command": 'python "unclosed'}), ['python', '"unclosed']))
    bad("PROCESS_ROLE", lambda: M.qualified_process(
        [{"pid":2,"ppid":1,"pgid":2,"command":"/synthetic/tool.py"}],2,"/synthetic/tool.py","/synthetic/run","unknown"))
    bind = dict(name="P1_M0001", attempt=1, outdir="/synthetic/NGC_RUN", receipt="/synthetic/NGC_RUN.receipt.json",
                launch_pin={"path":"/synthetic/launch.json","sha256":"a"*64}, child_pid=2)
    bad("DRIVER_STATUS_FORM", lambda: M.raw_status({"status":"FINISHED","driver_status":17}, **bind))
    bad("EXIT_CODE_FORM", lambda: M.raw_status({"status":"CHILD_FAILED","driver_status":None,"exit_code":None}, **bind))
    bad("MONITOR_RECEIPT_SCHEMA", lambda: M.monitor_receipt(M.encoded({"schema":"WRONG"})))
    bad("PLANNED_STOP_NOT_TWIN", lambda: M.terminal_prefix([{"status_class":"PLANNED_STOP"}], "P1_M0001"))
    bad("REFUSAL_ATTEMPT_MISMATCH", lambda: M.entry_reuse(
        {"spec":{"sha256":"a"*64},"point_key":"b"*64,"v006_spec_pin":{},"v006_handoff_pin":{}},
        {"spec":{"sha256":"a"*64},"point_key":"b"*64,"v006_spec_pin":{},"v006_handoff_pin":{}},
        [],[{"attempt":2}],1))
    sample = {"complete":True,"poll_s":5,"largest_gap_s":5,"n_samples":3,
              "first_utc":"2026-10-20T10:00:00Z","last_utc":"2026-10-20T10:00:12Z","max_other_ngc_processes":0}
    rec = {"utc_start":"2026-10-20T10:00:01Z","utc_end":"2026-10-20T10:00:10Z"}
    for code, key, value in (("SAMPLE_POLL","poll_s",0),("SAMPLE_GAP","largest_gap_s",-1),
                             ("SAMPLE_N","n_samples",1),("SAMPLE_COUNT","max_other_ngc_processes",-1)):
        case("REFUSE_" + code, lambda key=key,value=value: suite.eq(M.sample_value(dict(sample, **{key:value}),rec),None))
    f = full_launch_fixture(suite, "configuration_refusals")
    system_doc = M.read_pin(f.synthetic)["system"]
    def construct(cfg=None, system=None, overrides=None, label="changed"):
        pin = f.config if cfg is None else suite.fixture("config_" + label + ".json", cfg)
        return M.Context(pin, system=M.SyntheticSystem(system_doc) if system is None else system,
                         synthetic_pins=f.overrides if overrides is None else overrides)
    for code, key, value in (
            ("CONFIG_SCHEMA","schema","WRONG"),("CONFIG_PYTHON","python","/synthetic/python"),
            ("CONFIG_RAM","host_ram_bytes_expected",1),("RUN_ROOT_LAYOUT","run_root",str(f.root / "WRONG")),
            ("LAUNCH_ROOT_EXTERNAL","p112_launch_root","/Volumes/P112_SYNTHETIC_NO_ACCESS"),
            ("CUTOFF_COPY_IN_RUN_TREE","v006_copy_dir",f.config_doc["run_root"] + "/copies"),
            ("V006_PATH","v006","relative.md")):
        cfg = copy.deepcopy(f.config_doc)
        cfg[key] = value
        bad(code, lambda cfg=cfg,code=code: construct(cfg, label=code))
    cfg = copy.deepcopy(f.config_doc)
    cfg["v006_copy_dir"] = str(alias)
    bad("CONFIG_SYMLINK", lambda: construct(cfg, label="symlink"))
    bad("SYNTHETIC_PINS_REQUIRED", lambda: M.Context(f.config, system=M.SyntheticSystem(system_doc)))
    bad("SYNTHETIC_SYSTEM_REQUIRED", lambda: M.Context(f.config, system=M.System(), synthetic_pins=f.overrides))
    bad("SYNTHETIC_PIN_FORM", lambda: M.synthetic_fence({}, {}))
    ctx = construct()
    bad("WRITE_SCOPE", lambda: ctx.write(str(suite.root / "outside_context.json"), {"date_u":M.date_u()}))
    bad("V006_PIN_MISSING", lambda: ctx.get_vpin("SPEC_PIN","NOT_A_CONFIGURED_CALL"))
    bad("NAME_ATTEMPT", lambda: M.planned_outdir(ctx,"P1_M0001",0,"P112"))
    bad("MEMORY_WATCH_NOT_RUNNING", lambda: (setattr(ctx.system,"processes",lambda:[]), M.watch_check(ctx)))
    bad("INVOCATION_PROCESS_NOT_VISIBLE", lambda: M.own_process_command(ctx))
    pins = f.overrides
    spec = M.pin_of(Path(f.config_doc["members"][0]["fill_dir"]) / M.SERIAL_FILE)
    caps = M.first_caps(f.name)
    argv = M.monitor_command(pins,spec,str(f.root / "volume" / "NGC_TEST"),caps)
    bad("MONITOR_ARGV", lambda: M.check_monitor_command(argv+["--unknown"],pins,spec,str(f.root / "volume" / "NGC_TEST"),caps,f.name))
    bad_caps = dict(caps,wall_cap_s=0)
    bad("CAP_FORM", lambda: M.check_monitor_command(M.monitor_command(pins,spec,str(f.root / "volume" / "NGC_TEST"),bad_caps),
                                                    pins,spec,str(f.root / "volume" / "NGC_TEST"),bad_caps,f.name))
    occupied = f.root / "volume" / "NGC_OCCUPIED"
    occupied.mkdir()
    bad("OUTPUT_EXISTS", lambda: M.disk_check(ctx.cfg,str(occupied),caps,ctx.system))
    bad("FILL_DIR_REAL", lambda: ctx.read_fill(dict(ctx.cfg["members"][0],fill_dir=str(f.root / "missing_fill"))))
    old_root = ctx.cfg["p112_launch_root"]
    ctx.cfg["p112_launch_root"] = str(f.root / "missing_launch_root")
    bad("LAUNCH_ROOT_REAL", lambda: M.create_layout(ctx))
    ctx.cfg["p112_launch_root"] = old_root
    M.create_layout(ctx)
    broken = Path(old_root) / "work" / "broken_plan"
    broken.mkdir()
    suite.raw_write(broken / "plan.json", b"{")
    bad("INFLIGHT_PLAN_UNREADABLE", lambda: M.enforce_solo(ctx,False,rows=[]))

    common = ["--config",f.config["path"],"--config-sha256",f.config["sha256"],
              "--synthetic-pins",f.synthetic["path"],"--synthetic-pins-sha256",f.synthetic["sha256"]]
    def cli_refuse(code, command, extra):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = M.cli([command]+common+extra)
        suite.eq(status,2)
        suite.eq(json.loads(output.getvalue())["code"],code)
    for code, command, extra in (
            ("DRY_COMMAND","status",["--dry"]),("RESUME_COMMAND","status",["--resume"]),
            ("VERIFY_COMMAND","status",["--verify"]),("NAME_REQUIRED","launch",[]),
            ("ATTEMPT_REQUIRED","close-attempt",["--name",f.name]),
            ("REFUSAL_ARGUMENTS","record-monitor-refused",[]),("SAMPLER_ARGUMENTS","_sampler",[])):
        case("REFUSE_"+code,lambda code=code,command=command,extra=extra:cli_refuse(code,command,extra))
    output = io.StringIO()
    def lone_sha():
        with contextlib.redirect_stdout(output):
            result=M.cli(["status","--config",f.config["path"],"--config-sha256",f.config["sha256"],
                          "--synthetic-pins-sha256","a"*64])
        suite.eq((result,json.loads(output.getvalue())["code"]),(2,"SYNTHETIC_SHA_WITHOUT_FILE"))
    case("REFUSE_SYNTHETIC_SHA_WITHOUT_FILE",lone_sha)
    bad_syn = M.read_pin(f.synthetic)
    bad_syn["schema"] = "WRONG"
    sp = suite.fixture("wrong_synthetic_manifest.json",bad_syn)
    output = io.StringIO()
    def wrong_syn():
        with contextlib.redirect_stdout(output):
            result=M.cli(["status","--config",f.config["path"],"--config-sha256",f.config["sha256"],
                          "--synthetic-pins",sp["path"],"--synthetic-pins-sha256",sp["sha256"]])
        suite.eq((result,json.loads(output.getvalue())["code"]),(2,"SYNTHETIC_SCHEMA"))
    case("REFUSE_SYNTHETIC_SCHEMA",wrong_syn)

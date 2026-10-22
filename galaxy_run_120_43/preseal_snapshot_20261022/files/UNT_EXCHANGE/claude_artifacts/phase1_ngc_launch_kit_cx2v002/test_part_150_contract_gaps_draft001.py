"""Remaining named brief cases using local synthetic inputs and saved states."""


def contract_gap_cases(suite):
    import copy
    import math
    import os
    from pathlib import Path
    M, case, fail = suite.module, suite.case, suite.refuses
    f = full_launch_fixture(suite, "T11_kit_mapping")
    def context():
        return M.Context(f.config, system=M.SyntheticSystem(M.read_pin(f.synthetic)["system"]), synthetic_pins=f.overrides)
    ctx = context()
    cfg = ctx.cfg["members"][0]
    spec, spec_pin, fill, fill_pin = ctx.read_fill(cfg)
    handoff = M.read_pin(cfg["handoff"])
    for side, label, code in ((2, "wrong_label", "SPEC_LABEL_KEY"), (2, "wrong_leaf", "SPEC_LEAF"),
                              (2, "wrong_eps", "SPEC_EPS_PIN"), (2, "wrong_lo", "SPEC_LO_PIN"),
                              (3, "pair_difference", "SPEC_PAIR_DIFFERENCE")):
        args = [handoff, cfg["handoff"], *copy.deepcopy(fill), M.theta_key(M.read_pin(ctx.cfg["plan_output_primary"])["members"][0]["theta_engine"]),
                cfg["eps"], ctx.pins["lo"], "UNT_STEP5_ADMITTED_POINT_HANDOFF_CX3V001", True]
        if label == "wrong_label":
            args[side]["label"] = "step5 A_K32_A2_HEADLINE theta_key=" + "f" * 64
        elif label == "wrong_leaf":
            args[side]["numerics"]["route_a"]["column_workers"] = 8
        elif label == "wrong_eps":
            args[side]["numerics"]["uv_tail"]["eps_certificate"] = {}
        elif label == "wrong_lo":
            args[side]["numerics"]["uv_tail"]["lo_certificate"] = {}
        else:
            args[side]["physical"]["ell_F_m"] = math.nextafter(spec["physical"]["ell_F_m"], math.inf)
        case("T10_fill_" + label, lambda args=args, code=code: fail(code, lambda: M.fill_check(*args)))

    for changed in (False, True):
        label = "ulp" if changed else "honest"
        c = context()
        kit = c.kit_entries()
        entry_spec = copy.deepcopy(spec)
        if changed:
            entry_spec["physical"]["ell_F_m"] = math.nextafter(entry_spec["physical"]["ell_F_m"], math.inf)
        sp = suite.fixture("T11_kit_spec_" + label + ".json", entry_spec)
        name = "S0_J0_SERIAL"
        key = M.theta_key(M.read_pin(c.cfg["plan_output_primary"])["members"][0]["theta_engine"])
        entry = {"schema":"UNT_S0_LAUNCH_REGISTRY_ENTRY_C2V003A", "name":name, "theta_key":key,
                 "spec":sp, "v006_spec_pin":sp, "v006_handoff_pin":cfg["handoff"]}
        ep = suite.fixture("T11_kit_entry_" + label + ".json", entry)
        kit[name] = entry, ep
        c.kit_entries = lambda kit=kit: kit
        c.vpins["SPEC_PIN"][name] = sp
        if changed:
            before = {str(p) for p in f.root.rglob("*")}
            case("T11_kit_spec_one_ulp_assembly_refuses", lambda c=c: fail(
                "THETA_BITS_MISMATCH", lambda: M.assemble_registry(c)))
            case("T11_kit_mismatch_writes_nothing", lambda before=before: suite.eq(
                {str(p) for p in f.root.rglob("*")}, before))
        else:
            case("T11_honest_S0_member_mapping", lambda c=c: suite.eq(
                (c.calls()[0]["name"], c.calls()[0]["kind"], c.calls()[0]["origin"]),
                ("S0_J0_SERIAL", "MEMBER", "KIT")))

    f = full_launch_fixture(suite, "L04_dry_without_gate")
    ctx = M.Context(f.config, system=M.SyntheticSystem(M.read_pin(f.synthetic)["system"]), synthetic_pins=f.overrides)
    ctx.v006_text = "## A999: no TOOL_PIN\n"
    ctx.system.processes = lambda: [
        {"pid":os.getpid(),"ppid":1,"pgid":os.getpid(),"command":M.PY + " -I -B /synthetic/test.py"},
        {"pid":900111,"ppid":1,"pgid":900111,"command":M.PY + " -I -B " + f.watch["path"]}]
    case("L04_dry_without_TOOL_PIN", lambda: suite.eq(M.launch(ctx, f.name, dry=True)["status"], "DRY_NOT_LAUNCHED"))
    case("L04_status_without_TOOL_PIN", lambda: suite.eq(M.status(ctx)["calls"][0]["status"], "READY"))
    ctx.system.fixture["mount_points"] = []
    before = {str(p) for p in f.root.rglob("*")}
    ctx.v006_text = Path(f.config_doc["v006"]).read_text()
    case("N19_launch_unmounted_refuses", lambda: fail("RUN_VOLUME_NOT_MOUNTED", lambda: M.launch(ctx, f.name)))
    case("N19_launch_unmounted_no_write", lambda: suite.eq({str(p) for p in f.root.rglob("*")}, before))
    old_record_paths = ctx.record_paths
    ctx.record_paths = lambda name=None: []
    case("N16_seed_launch_required", lambda: fail("SEED_SERIAL_NOT_LAUNCHED_FIRST", ctx.seed_check))
    ctx.record_paths = old_record_paths

    f = receipt_fixture(suite, "N16_kit_started_recordless")
    name = "S0_J0_SERIAL"
    call = dict(f.call, name=name, origin="KIT", entry=M.read_pin(f.entry_pin), entry_pin=f.entry_pin)
    f.ctx._fixture_calls = [call]
    f.ctx._fixture_kit[name] = M.read_pin(f.entry_pin), f.entry_pin
    outdir = M.planned_outdir(f.ctx, name, 1, "KIT")
    suite.raw_write(Path(outdir + ".receipt.json.stdout.txt"), b"SYNTHETIC_UNREADABLE_MONITOR_LOG")
    case("N16_started_without_line_refuses", lambda: fail("MONITOR_STARTED_NO_LAUNCH_JSON",
                                                        lambda: M.history(f.ctx, call)))
    f.ctx.v006_text += "RESIDUAL_RETRY S0_J0_SERIAL 1\n"
    def takeover():
        h = M.history(f.ctx, call)
        decision = M.next_attempt(name, h["records"], h["actual"], h["residuals"], h["trailing_nonattempt"])
        suite.eq((decision["attempt"], decision["caps"], decision["solo_mode"]), (2, M.first_caps(name), False))
        suite.eq(M.planned_origin(name, 2, h["records"], h["residuals"]), "P112")
        suite.eq(M.register_call(f.ctx, call, {"attempt":2}, f.entry_pin, f.root, h), f.entry_pin)
    case("N16_recordless_kit_residual_takeover", takeover)

    for actual_middle in (False, True):
        f = receipt_fixture(suite, "N13_pair_" + str(actual_middle), mode="REFUSED", record=False, sample={})
        first_record = dict(f.record, solo_mode=True)
        suite.raw_write(f.record_path, M.encoded(first_record))
        M.close_attempt(f.ctx, f.name, 1)
        for k in (2, 3):
            outdir = M.planned_outdir(f.ctx, f.name, k, "P112")
            actual = k == 3 or actual_middle
            if actual:
                Path(outdir).mkdir()
            receipt = copy.deepcopy(f.rec)
            receipt["child_pid"] = 900020 + k
            if k == 2:
                receipt.update(status="CHILD_FAILED", driver_status=None, exit_code=1)
            receipt["receipt_sha256"] = M.sha(M.canonical({a:b for a,b in receipt.items() if a != "receipt_sha256"}))
            suite.raw_write(Path(outdir + ".receipt.json"), M.encoded(receipt))
            lj = M.strict_json(
                Path(f.outdir + ".receipt.json.launch.json").read_bytes())
            lj["child_pid"] = receipt["child_pid"]
            lj["command"] = M.driver_command(f.ctx.pins, f.call["spec"], outdir)
            lp = suite.raw_write(Path(outdir + ".receipt.json.launch.json"), M.encoded(lj))
            sample = M.read_pin(M.pin_of(f.outdir + ".solo.json"))
            sample.update(attempt=k, outdir=outdir)
            suite.raw_write(Path(outdir + ".solo.json"), M.encoded(sample))
            outcome = "MISLAUNCH" if k == 2 else "LAUNCH"
            record = dict(f.record, schema="UNT_P112_" + outcome + "_RECORD_CX2V001", outcome=outcome,
                          attempt=k, outdir=outdir, receipt=outdir + ".receipt.json", solo_mode=True,
                          launch_json=dict(lp, child_pid=lj["child_pid"], utc=lj["utc"]))
            suite.raw_write(f.root / "launch_root" / "launches" /
                            ("P112_%s_%s_CX2V001_A%d.json" % (f.name, outcome, k)), M.encoded(record))
            if actual:
                M.close_attempt(f.ctx, f.name, k)
            else:
                fail("NOT_AN_ATTEMPT", lambda: M.close_attempt(f.ctx, f.name, k))
        h = M.history(f.ctx, f.call)
        if actual_middle:
            case("N08_actual_MISLAUNCH_separates_infra_pair", lambda h=h, f=f:
                 suite.eq(M.terminal_prefix(h["actual"], f.name), None))
        else:
            case("N13_nonattempt_MISLAUNCH_does_not_separate", lambda h=h, f=f: (
                suite.eq([r["attempt"] for r in h["actual"]], [1, 3]),
                suite.eq(M.terminal_prefix(h["actual"], f.name)["disposition"], "UNEVALUATED_INFRA_REPEAT")))

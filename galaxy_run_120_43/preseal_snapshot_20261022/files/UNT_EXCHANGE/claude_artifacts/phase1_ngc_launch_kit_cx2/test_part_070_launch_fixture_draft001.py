"""A wholly synthetic, file-backed configuration for the public launch CLI."""


def full_launch_fixture(suite, label):
    import copy
    import types
    from pathlib import Path
    M = suite.module
    root = suite.root / label
    root.mkdir()
    def raw(name, data):
        p = root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        return suite.raw_write(p, data)
    def put(name, obj):
        return raw(name, M.encoded(obj))
    for folder in ("volume/NGC_RUNS", "kit_volume/NGC_RUNS", "launch_root", "kit_root/registry",
                   "kit_root/launches", "copies"):
        (root / folder).mkdir(parents=True, exist_ok=True)
    driver = raw("inert_fixture_driver.py", SYNTHETIC_DRIVER.encode())
    # This wrapper uses the explicitly authorized verified monitor API, on the
    # synthetic driver only. Its own path/pin is used in the monitor's receipts.
    wrapper = '''import hashlib,types
from pathlib import Path
source=Path(%r)
data=source.read_bytes()
assert hashlib.sha256(data).hexdigest()==%r
m=types.ModuleType("_authorized_synthetic_monitor")
m.__file__=__file__
exec(compile(data,str(source),"exec"),m.__dict__)
raise SystemExit(m.main())
''' % (M.REAL["monitor"]["path"], M.REAL["monitor"]["sha256"])
    monitor = raw("synthetic_monitor.py", wrapper.encode())
    dry_source = '''import hashlib,json,sys
from pathlib import Path
driver,driver_sha,spec,spec_sha,report,log=sys.argv[1:]
assert hashlib.sha256(Path(driver).read_bytes()).hexdigest()==driver_sha
assert hashlib.sha256(Path(spec).read_bytes()).hexdigest()==spec_sha
Path(report).mkdir()
r={"executed_stages":0,"binding_blockers":[],"source_build_blockers":[],
   "future_stage_dependencies":[{"class":"PENDING_ROUTE_A_OUTPUTS"}],"planned_route_a":True}
with (Path(report)/"NGC_SOURCE_BUILD_READINESS.json").open("x") as f:json.dump(r,f)
l={"exit":0,"blocked":[],"ctx_modes":["simulate"],"driver_sha256":driver_sha,"spec_sha256":spec_sha}
with Path(log).open("x") as f:json.dump(l,f)
'''
    dry = raw("synthetic_dry_harness.py", dry_source.encode())
    watch = raw("synthetic_passive_watch.py", b"import time\ntime.sleep(120)\n")
    lo = put("synthetic_LO.json", {"schema": "SYNTHETIC_LO_PIN"})
    policy = put("synthetic_policy.json", {"schema": "SYNTHETIC_POLICY_NO_SLOTS"})
    spec_of_record = put("synthetic_spec_of_record.json", {"schema": "SYNTHETIC_SPEC_OF_RECORD"})
    def theta(ell):
        return {"Eref_base_J": 2.5, "ell_F_m": float(ell), "gamma_over_Eref": 0.125,
                "common_scale_s": 1.5, "entropy_K_factor": 3.0}
    def fd_point(th, role, **extra):
        return dict(theta_natural=th, theta_hex={k: v.hex() for k, v in th.items()}, key=M.theta_key(th), role=role, **extra)
    engine = theta(7)
    member = {"member_id": "M000", "log_index": 1, "role": "primary_anchor", "evaluated": False,
              "theta_engine": engine, "theta_ngc": dict(engine, ngc3198_distance_Mpc=13.8, ngc3198_inclination_deg=72.0)}
    plan = put("PLAN_PRIMARY.json", {"ok": True, "budget": 0, "evaluations_used": 0, "members": [member]})
    selection = put("SELECTION.json", {"points": [{"log_index": 1, "role": "primary_anchor"}]})
    build = put("PLAN_BUILD.json", {"status": "BUILT", "stage": "PLAN", "phase": "PHASE_1"})
    export = put("EXPORT.json", {"schema": "UNT_STEP5_ADMITTED_POINT_EXPORT_CX3V001", "target_free": True,
                               "admitted_points": [{"log_index": 1, "theta_natural": engine}]})
    fs = [fd_point(theta(8 + k), "F%d" % k) for k in range(3)]
    fdplan = put("FDPLAN.json", {"schema": "PHASE1_FDPLAN_C2V001",
                               "members": [fd_point(engine, "primary_anchor", log_index=1)], "F": fs})
    at0 = put("AT0A.json", {"schema": "PHASE1_AT0A_C2V001", "outcome": "PASS"})
    lines = ["## A999: SYNTHETIC P112 TEST",
             "TOOL_PIN P112_LAUNCHER_CX2V001 %s %s" % (suite.tool_sha, suite.tool_path),
             "WATCH_PIN MEMORY_WATCH %s %s" % (watch["sha256"], watch["path"])]
    def spec_for(th, key, eps, leaf=1):
        return {"fixture_mode": "COMPLETED", "label": "step5 A_K32_A2_HEADLINE theta_key=" + key,
                "physical": {"Eref_J": th["Eref_base_J"], "ell_F_m": th["ell_F_m"],
                             "gamma": th["gamma_over_Eref"] * th["Eref_base_J"],
                             "common_scale_s": th["common_scale_s"], "entropy_K_factor": th["entropy_K_factor"],
                             "distance_Mpc": 13.8, "inclination_deg": 72.0},
                "numerics": {"route_a": {"column_workers": leaf}, "uv_tail": {"eps_certificate": eps, "lo_certificate": lo}}}
    def fill(name, th, is_member=False):
        key = M.theta_key(th)
        eps = put(name + "/EPS.json", {"point": {"key": key}})
        gq = put(name + "/GQ.json", {"point": {"key": key}})
        hand = {"schema": "UNT_STEP5_ADMITTED_POINT_HANDOFF_CX3V001" if is_member else "UNT_STEP5_PHASE1_POINT_HANDOFF_C2V001",
                "mode": "SYNTHETIC_DRY_ONLY", "driver_branch": "cx3r008",
                "certificate_pins": {"eps_certificate": eps, "lo_certificate": lo}, "policy_pin": policy}
        if is_member:
            hand.update({"log_index": 1, "source_export_pin": export})
        else:
            hand.update({"point_key": key, "source_pin": fdplan})
        hp = put(name + "/HANDOFF.json", hand)
        sp = put(name + "/fill/" + M.SERIAL_FILE, spec_for(th, key, eps))
        put(name + "/fill/" + M.TWIN_FILE, spec_for(th, key, eps, 8))
        put(name + "/fill/" + M.FILL_FILE, {"schema": "UNT_STEP5_FILLED_SPECS_C2V001", "launch_authorized": False,
                                         "handoff_pin": hp, "theta_key": key, "pending_certificates": []})
        lines.extend(["HANDOFF_PIN %s %s %s" % (name, hp["sha256"], hp["path"]),
                      "SPEC_PIN %s %s %s" % (name, sp["sha256"], sp["path"])])
        return {"handoff": hp, "fill_dir": str(root / name / "fill"), "eps": eps, "gq": gq}
    member_cfg = dict(fill("P1_M0001", engine, True), log_index=1, role="primary_anchor", order=0, member_id="M000")
    f_cfg = [dict(fill("P1_F%d" % k, fs[k]["theta_natural"]), label="F%d" % k) for k in range(3)]
    seed_eps = put("SEED_EPS.json", {"point": {"key": M.SEED_KEY}})
    seed_spec = put("SEED_SPEC.json", spec_for(theta(6), M.SEED_KEY, seed_eps))
    twin_spec = put("TWIN_SPEC.json", spec_for(theta(6), M.SEED_KEY, seed_eps, 8))
    for name, sp in (("S0_SEED_SERIAL", seed_spec), (M.TWIN, twin_spec)):
        put("kit_root/registry/" + name + "_C2V003A.json",
            {"schema": "UNT_S0_LAUNCH_REGISTRY_ENTRY_C2V003A", "name": name, "theta_key": M.SEED_KEY,
             "spec": sp, "v006_spec_pin": sp})
        lines.append("SPEC_PIN %s %s %s" % (name, sp["sha256"], sp["path"]))
    put("kit_root/launches/S0_SEED_SERIAL_LAUNCH_C2V003A_A1.json",
        {"schema": "UNT_S0_LAUNCH_RECORD_C2V003A", "name": "S0_SEED_SERIAL", "attempt": 1, "outcome": "LAUNCH",
         "solo_mode": False})
    stamp = M.date_u()
    epoch = int(M.dt.datetime.strptime(stamp, "%a %b %d %H:%M:%S UTC %Y").replace(tzinfo=M.dt.timezone.utc).timestamp())
    put("kit_root/M15_PRELAUNCH_RECORD_C2V001.json",
        {"schema": "UNT_M15_PRELAUNCH_RECORD_C2V001", "date_u": stamp, "date_u_epoch_s": epoch})
    v006 = raw("V006.md", ("\n".join(lines) + "\n").encode())
    cfg = {"schema": "P112_CONFIG_CX2V001", "python": M.PY, "v006": v006["path"], "v006_copy_dir": str(root / "copies"),
           "run_volume": str(root / "volume"), "run_root": str(root / "volume" / "NGC_RUNS"),
           "p112_launch_root": str(root / "launch_root"),
           "s0": {"launch_root": str(root / "kit_root"), "run_root": str(root / "kit_volume" / "NGC_RUNS")},
           "host_ram_bytes_expected": M.RAM, "plan_output_primary": plan, "plan_build_record": build,
           "selection": selection, "fdplan": fdplan, "spec_of_record": spec_of_record, "at0a_pass": at0,
           "members": [member_cfg], "f_points": f_cfg}
    config_pin = put("CONFIG.json", cfg)
    overrides = {"driver": driver, "monitor": monitor, "dry_harness": dry, "lo": lo, "policy": policy,
                 "spec_of_record": spec_of_record}
    syn = put("SYNTHETIC_PINS.json", {"schema": "P112_SYNTHETIC_PINS_CX2V001", "pins": overrides, "date_u": M.date_u(),
        "system": {"mount_points": [cfg["run_volume"], str(root / "kit_volume")], "free_bytes": 1 << 50, "host_ram_bytes": M.RAM}})
    return types.SimpleNamespace(root=root, config=config_pin, config_doc=cfg, synthetic=syn,
                                 overrides=overrides, watch=watch, name="P1_M0001")

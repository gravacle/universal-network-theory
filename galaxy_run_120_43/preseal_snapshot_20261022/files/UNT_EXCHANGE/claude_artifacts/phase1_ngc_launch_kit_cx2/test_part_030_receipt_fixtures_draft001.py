"""Real-format receipts from the pinned monitor with an inert synthetic driver."""
SYNTHETIC_DRIVER = r'''import argparse, hashlib, json, os, signal, sys
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument("command")
p.add_argument("--spec")
p.add_argument("--outdir")
a=p.parse_args()
spec=json.loads(Path(a.spec).read_bytes())
mode=spec.get("fixture_mode","COMPLETED")
if mode=="EXIT_BEFORE_MKDIR":sys.exit(1)
if mode=="SIGNAL_BEFORE_MKDIR":os.kill(os.getpid(),signal.SIGTERM)
d=Path(a.outdir);d.mkdir()
result=json.dumps({"synthetic_sentinel":"P112_PRIVATE_SENTINEL_MUST_NOT_BE_READ"},sort_keys=True).encode()
with (d/"result.json").open("xb") as f:f.write(result)
finish={"status":mode,"result_sha256":hashlib.sha256(result).hexdigest()}
with (d/"finish.json").open("x") as f:json.dump(finish,f)
sys.exit(0 if mode in ("COMPLETED","COMPLETED_INVALID") else 1)
'''


def receipt_fixture(suite, label, *, origin="P112", name="P1_M0001", outcome="LAUNCH",
                    mode="COMPLETED", record=True, broken_hash=False, no_receipt=False, off_spec=False,
                    sample=None, ram=None):
    import types
    from pathlib import Path
    M = suite.module
    root = suite.root / label
    root.mkdir()
    for dirname in ("volume", "kit_volume", "launch_root", "kit_launch_root", "copies"):
        (root / dirname).mkdir()
    for volume in ("volume", "kit_volume"):
        (root / volume / "NGC_RUNS").mkdir()
    for launchroot in ("launch_root", "kit_launch_root"):
        for folder in ("registry", "launches", "work", "twin_kill", "outside_set_stop", "assembly", "monitor_refused"):
            (root / launchroot / folder).mkdir()
    def put(name, obj):
        return suite.raw_write(root / name, M.encoded(obj))
    driver = suite.raw_write(root / "inert_synthetic_driver.py", SYNTHETIC_DRIVER.encode())
    spec = put("spec.json", {"fixture_mode": mode, "numerics": {"route_a": {"column_workers": 8 if name == M.TWIN else 1}}})
    registered_spec = put("other_spec.json", {"fixture_mode": "OTHER"}) if off_spec else spec
    class FakeSystem(M.SyntheticSystem):
        def __init__(self):
            super().__init__({"mount_points": [str(root / "volume"), str(root / "kit_volume")],
                              "free_bytes": 1 << 50, "host_ram_bytes": M.RAM if ram is None else ram})
            self.rows = []
        def processes(self):
            return list(self.rows)
    class FixtureContext(M.Context):
        def __init__(self):
            self.system, self.synthetic = FakeSystem(), True
            self.pins = dict(M.REAL, driver=driver)
            self.own_pin = {"path": str(suite.tool_path), "sha256": suite.tool_sha}
            self.cfg = {"python": M.PY, "run_volume": str(root / "volume"), "run_root": str(root / "volume" / "NGC_RUNS"),
                        "p112_launch_root": str(root / "launch_root"), "v006_copy_dir": str(root / "copies"),
                        "s0": {"launch_root": str(root / "kit_launch_root"), "run_root": str(root / "kit_volume" / "NGC_RUNS")},
                        "plan_output_primary": put("PLAN.json", {"members": [], "budget": 0}),
                        "fdplan": put("FDPLAN.json", {"members": [], "F": []}),
                        "selection": put("selection.json", {"points": []}),
                        "plan_build_record": put("plan_build.json", {"status": "BUILT"})}
            text = "## A999: synthetic root\nTOOL_PIN P112_LAUNCHER_CX2V001 %s %s\n" % (suite.tool_sha, suite.tool_path)
            self.cfg["v006"] = suite.raw_write(root / "V006.md", text.encode())["path"]
            self.v006_raw, self.v006_text = text.encode(), text
            self.config_pin = put("config.json", self.cfg)
            self.mapping_block = None
            self._fixture_calls = []
            self._fixture_kit = {}
        def calls(self):
            if self.mapping_block:
                raise M.Refusal(self.mapping_block)
            return self._fixture_calls
        def get_vpin(self, kind, query_name):
            if kind == "SPEC_PIN" and query_name == name:
                return registered_spec
            raise M.Refusal("V006_PIN_MISSING")
        def kit_entries(self):
            return self._fixture_kit
    ctx = FixtureContext()
    outdir = M.planned_outdir(ctx, name, 1, origin)
    monitor = M.load_verified(M.REAL["monitor"], "_p112_verified_synthetic_monitor")
    raw_receipt = str(root / "raw_monitor.receipt.json")
    rec = monitor.run_monitored(driver=driver["path"], driver_sha256=driver["sha256"], spec=spec["path"],
                                outdir=outdir, receipt=raw_receipt, poll_s=0.01,
                                **M.first_caps(name))
    suite.eq(rec["schema"], M.MONITOR_SCHEMA)
    final_receipt = outdir + ".receipt.json"
    if not no_receipt:
        receipt_bytes = Path(raw_receipt).read_bytes()
        if broken_hash:
            bad = dict(rec, receipt_sha256="0" * 64)
            receipt_bytes = M.encoded(bad)
        suite.raw_write(Path(final_receipt), receipt_bytes)
    lj_raw = Path(raw_receipt + ".launch.json").read_bytes()
    lj_pin = suite.raw_write(Path(final_receipt + ".launch.json"), lj_raw)
    lj = M.strict_json(lj_raw)
    # Existence-only launch-side outputs. P112 must never open these.
    suite.raw_write(Path(final_receipt + ".stdout.txt"), b"FORBIDDEN_STDOUT_CONTENT\n")
    suite.raw_write(Path(final_receipt + ".stderr.txt"), b"FORBIDDEN_STDERR_CONTENT\n")
    call = {"name": name, "kind": "OTHER" if name == M.TWIN else "MEMBER", "alternative": None if name == M.TWIN else M.PRIMARY,
            "key": name if name == M.TWIN else "M000", "point_key": "c" * 64, "theta_sha256": "b" * 64,
            "spec": registered_spec, "origin": origin, "theta_check": {"fixture": True}}
    entry = {"schema": "UNT_S0_LAUNCH_REGISTRY_ENTRY_C2V003A" if origin == "KIT" else "UNT_P112_LAUNCH_REGISTRY_ENTRY_CX2V001",
             "name": name, "spec": registered_spec, "point_key": call["point_key"], "theta_key": call["point_key"],
             "theta_sha256": call["theta_sha256"], "v006_spec_pin": registered_spec}
    entry_path = (root / "kit_launch_root" / "registry" / (name + "_C2V003A.json") if origin == "KIT" else
                  Path(M.own_registry_path(ctx, name)))
    entry_pin = suite.raw_write(entry_path, M.encoded(entry))
    call.update({"entry": entry if origin == "KIT" else None, "entry_pin": entry_pin if origin == "KIT" else None})
    ctx._fixture_calls = [call]
    if origin == "KIT":
        ctx._fixture_kit[name] = (entry, entry_pin)
    record_doc = {
        "schema": "UNT_" + ("S0_" + outcome + "_RECORD_C2V003A" if origin == "KIT" else "P112_" + outcome + "_RECORD_CX2V001"),
        "name": name, "attempt": 1, "outcome": outcome, "outdir": outdir, "receipt": final_receipt,
        "launch_json": dict(lj_pin, utc=lj["utc"], child_pid=lj["child_pid"]),
        "spec": registered_spec, "driver": driver, "monitor": M.REAL["monitor"], "caps": M.first_caps(name),
        "monitor_pid": 900001, "sampler_pid": 900002, "watch_pid": 900003 if name == M.TWIN else None,
        "host_ram_bytes": M.RAM, "solo_mode": False, "counted_rerun": False,
        "registry_entry": entry_pin, "date_u": M.date_u()}
    record_name = ("%s_%s_C2V003A_A1.json" % (name, outcome) if origin == "KIT" else
                   "P112_%s_%s_CX2V001_A1.json" % (name, outcome))
    record_path = root / ("kit_launch_root" if origin == "KIT" else "launch_root") / "launches" / record_name
    if record:
        suite.raw_write(record_path, M.encoded(record_doc))
    if sample is not None:
        start, end = M.timestamp(rec["utc_start"]), M.timestamp(rec["utc_end"])
        fmt = lambda t: M.dt.datetime.fromtimestamp(t, M.dt.timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")
        s = {"schema": "STEP5_SOLO_SAMPLE_CX2V001", "name": name, "attempt": 1, "outdir": outdir,
             "declared_list_sha256": M.DECLARED_LIST_SHA, "poll_s": 5, "n_samples": 3,
             "first_utc": fmt(start - 2), "last_utc": fmt(end + 2), "largest_gap_s": 5.0,
             "complete": True, "max_other_ngc_processes": 0, "nonzero_samples": [], "writer": ctx.own_pin,
             "date_u": M.date_u()}
        s.update(sample)
        suite.raw_write(Path(outdir + ".solo.json"), M.encoded(s))
    return types.SimpleNamespace(ctx=ctx, name=name, root=root, outdir=outdir, rec=rec, record=record_doc,
                                 record_path=record_path, call=call, entry_pin=entry_pin, launch_pin=lj_pin)

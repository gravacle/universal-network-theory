"""Synthetic θ, interface and process-table tests; no live scientific driver."""


def theta_cases(suite):
    import copy
    import math
    M, case, fail = suite.module, suite.case, suite.refuses
    B = M.load_verified(M.REAL["builder"], "_synthetic_p112_builder_contract")
    theta = {"Eref_base_J": 2.5, "ell_F_m": 7.0, "gamma_over_Eref": 0.125,
             "common_scale_s": 1.5, "entropy_K_factor": 3.0}
    theta.update({"synthetic_extra_%02d" % i: float(i) / 8.0 for i in range(8)})
    ngc = dict(theta, ngc3198_distance_Mpc=13.8, ngc3198_inclination_deg=72.0)
    spec = {"physical": {"Eref_J": 2.5, "ell_F_m": 7.0, "gamma": 0.3125, "common_scale_s": 1.5,
                         "entropy_K_factor": 3.0, "distance_Mpc": 13.8, "inclination_deg": 72.0}}
    cfg = {"log_index": 17, "role": "primary_anchor", "order": 0, "member_id": "M000"}
    hand = {"log_index": 17}
    member = dict(cfg, theta_engine=theta, theta_ngc=ngc)
    fd = {"log_index": 17, "role": "primary_anchor", "theta_hex": {k: v.hex() for k, v in theta.items()},
          "theta_natural": dict(theta), "key": M.theta_key(theta)}
    export = {"admitted_points": [{"log_index": 17, "theta_natural": dict(theta)}]}
    def check(m=member, f=fd, h=hand, e=export, s=spec, c=cfg):
        return M.check_member_theta(m, f, h, e, s, spec, c, 0, B)
    case("T01_member", lambda: suite.eq(check()["point_key"], fd["key"]))
    case("T13_thirteen_coordinates", lambda: suite.eq(check()["theta_sha256"], B.theta_sha256(ngc)))
    parent = M.load_verified(M.REAL["orchestrator"], "_synthetic_p112_theta_key_parent")
    case("T13_program_key_equal_pinned_parent", lambda: suite.eq(M.theta_key(theta), parent.theta_key(theta)))
    case("T13_program_and_builder_keys_differ", lambda: suite.eq(M.theta_key(theta) != B.theta_sha256(ngc), True))
    for coord in theta:
        m = copy.deepcopy(member)
        m["theta_engine"][coord] = math.nextafter(theta[coord], math.inf)
        case("T02_PLAN_ulp_" + coord, lambda m=m: fail("THETA_BITS_MISMATCH", lambda: check(m=m)))
        e = copy.deepcopy(export)
        e["admitted_points"][0]["theta_natural"][coord] = math.nextafter(theta[coord], math.inf)
        case("T03_export_ulp_" + coord, lambda e=e: fail("THETA_BITS_MISMATCH", lambda: check(e=e)))
        f = copy.deepcopy(fd)
        f["theta_hex"][coord] = math.nextafter(theta[coord], math.inf).hex()
        case("T04_fdplan_ulp_" + coord, lambda f=f: fail("FDPLAN_THETA_HEX", lambda: check(f=f)))
    for coord in ("Eref_J", "ell_F_m", "gamma", "common_scale_s", "entropy_K_factor"):
        s = copy.deepcopy(spec)
        s["physical"][coord] = math.nextafter(s["physical"][coord], math.inf)
        case("T05_spec_ulp_" + coord, lambda s=s: fail("THETA_BITS_MISMATCH", lambda: check(s=s)))
    for coord in ("distance_Mpc", "inclination_deg"):
        s = copy.deepcopy(spec)
        s["physical"][coord] = math.nextafter(s["physical"][coord], math.inf)
        case("T06_geometry_ulp_" + coord, lambda s=s: fail("THETA_BITS_MISMATCH", lambda: check(s=s)))
    e = copy.deepcopy(export)
    e["admitted_points"][0]["theta_natural"]["synthetic_extra_00"] = -0.0
    case("T07_signed_zero", lambda: fail("THETA_BITS_MISMATCH", lambda: check(e=e)))
    for label in ("extra", "missing"):
        m = copy.deepcopy(member)
        if label == "extra":
            m["theta_engine"]["another"] = 1.0
        else:
            del m["theta_engine"]["ell_F_m"]
        case("T08_keyset_" + label, lambda m=m: fail("THETA_KEY_SET", lambda: check(m=m)))
    for label, changes in (("index", {"log_index": 18}), ("role", {"role": "wrong"}), ("order", {"order": 1}),
                            ("member_id", {"member_id": "M001"})):
        c = dict(cfg, **changes)
        case("T09_identity_" + label, lambda c=c: fail("MEMBER_IDENTITY", lambda: check(c=c)))
    fdp = dict(fd, role="F0")
    fh = {"point_key": fd["key"]}
    case("T01_F0", lambda: suite.eq(M.check_f_theta(fdp, fh, spec, spec, "F0")["theta_sha256"], fd["key"]))
    f = copy.deepcopy(fdp)
    f["theta_hex"]["ell_F_m"] = math.nextafter(7.0, math.inf).hex()
    case("T04_F_ulp", lambda: fail("THETA_BITS_MISMATCH", lambda: M.check_f_theta(f, fh, spec, spec, "F0")))
    changed = dict(ngc, synthetic_extra_07=math.nextafter(ngc["synthetic_extra_07"], math.inf))
    case("T12_changed_theta_ngc_digest", lambda: suite.eq(B.theta_sha256(changed) != B.theta_sha256(ngc), True))
    # 0782: this helper deliberately accepts a different shape-valid digest.
    for label, digest in (("honest", B.theta_sha256(ngc)), ("changed", B.theta_sha256(changed))):
        reg = {"schema": "STEP5_LAUNCH_REGISTRY_C2V003", "phase": "PHASE_1",
               "calls": [{"alternative": "BR_A_F10_PRIMARY", "kind": "MEMBER", "key": "M000",
                          "theta_sha256": digest, "spec_sha256": "a" * 64}]}
        pin = suite.fixture("registry_" + label + ".json", reg)
        case("R01_T12_helper_shape_" + label, lambda pin=pin, digest=digest:
             suite.eq(B._launch_registry(pin, "PHASE_1")[0][("BR_A_F10_PRIMARY", "MEMBER", "M000")]["theta_sha256"], digest))
    # Full builder assembly is prohibited: it would load v003g / slots.
    suite.interfaces["registry_theta_limitation"] = (
        "TESTED: _launch_registry accepts either shape-valid digest. UNTESTED: real PLAN agreement; "
        "deciding test is root's first real Phase-1 registry assembly (0782).")


def process_cases(suite):
    M, case, fail = suite.module, suite.case, suite.refuses
    import os
    from pathlib import Path
    tools = []
    for i, title in enumerate(("driver", "values_writer_c2v004", "handoff_c2v003a", "producer")):
        raw = ("# synthetic inert fixture " + title + "\n").encode()
        path = suite.bytes_fixture("proc_%d.py" % i, raw)
        tools.append({"tool": title, "path": path["path"], "sha256": path["sha256"], "driver_only": i == 0})
    alias = suite.bytes_fixture("byte_alias.py", Path(tools[1]["path"]).read_bytes())
    counter = M.ProcessCounter(tools)
    def row(pid, command, ppid=1):
        return {"pid": pid, "ppid": ppid, "pgid": pid, "command": command}
    rows = [
        row(10, M.PY + " -I -B " + tools[0]["path"] + " run --spec /fake/spec --outdir /fake/out"),
        row(11, M.PY + " -I -B " + tools[0]["path"] + " _stage", 10),
        row(12, M.PY + " -I -B " + tools[0]["path"] + " dry-run"),
        row(13, M.PY + " -I -B " + alias["path"]),
        row(14, M.PY + " -I -B " + tools[2]["path"]),
        row(15, M.PY + " -I -B /fake/root_monitor_c2v001.py --receipt /fake/NGC.receipt.json"),
        row(16, M.PY + " -I -B /fake/dry_one_c2v001.py"),
        row(17, "/bin/bash /fake/twin_kill_watch_c2v003a.sh"),
        row(18, M.PY + " -I -B /fake/phase1_ngc_launch_cx2v001.py _sampler --outdir /fake/NGC"),
    ]
    case("P01_sha_alias_and_exclusions", lambda: suite.eq(
        [r["pid"] for r in counter.count(rows, own_root=10)], [13, 14]))
    case("P01_driver_run_and_stage_counted_elsewhere", lambda: suite.eq(
        [r["pid"] for r in counter.count(rows)], [10, 11, 13, 14]))
    case("P01_values_and_old_handoff_in_real_list", lambda: suite.eq(
        {"values_writer_c2v004_cx2v002", "ngc_acceptance_handoff_c2v003a"} <=
        {x["tool"] for x in M.DECLARED_TOOLS}, True))
    case("P01_declared_list_thirteen", lambda: suite.eq(len(M.DECLARED_TOOLS), 13))
    case("P01_ppid_transitive_closure", lambda: suite.eq(M.descendants(
        [row(1, "a", 0), row(2, "b", 1), row(3, "c", 2), row(4, "d", 3)], 1), {1, 2, 3, 4}))
    case("P01_ps_strict", lambda: fail("PS_PARSE", lambda: M.parse_ps("12 broken command\n")))
    outdir = "/synthetic/NGC_RUN"
    monitor = "/synthetic/synthetic_monitor.py"
    case("N14_reused_monitor_pid", lambda: suite.eq(
        M.qualified_process([row(200, "/bin/sleep 60")], 200, monitor, outdir, "monitor"), None))
    case("C06_reused_sampler_pid", lambda: suite.eq(
        M.qualified_process([row(200, "/bin/sleep 60")], 200, str(suite.tool_path), outdir, "sampler"), None))
    actual_monitor = row(200, M.PY + " -I -B " + monitor + " --receipt " + outdir + ".receipt.json")
    case("N14_qualified_monitor", lambda: suite.eq(
        M.qualified_process([actual_monitor], 200, monitor, outdir, "monitor")["pid"], 200))
    config = {"run_volume": str(suite.root / "volume"), "s0": {"run_root": str(suite.root / "kit_volume" / "NGC_KIT")}}
    (suite.root / "volume").mkdir()
    (suite.root / "kit_volume").mkdir()
    system = M.SyntheticSystem({"mount_points": [config["run_volume"]], "free_bytes": 313532612608, "host_ram_bytes": M.RAM})
    case("N19_wrong_volume_mounted", lambda: fail("RUN_VOLUME_NOT_MOUNTED", lambda: M.mount_first(config, "KIT", system)))
    cap = {"wall_cap_s": 1220648, "rss_cap_bytes": M.RAM, "output_cap_bytes": 292057776128}
    target = str(suite.root / "volume" / "NGC_RUN")
    case("K02_exact_292GiB", lambda: suite.eq(M.disk_check(config, target, cap, system)["free_bytes"], 313532612608))
    smaller = M.SyntheticSystem({"mount_points": [config["run_volume"]], "free_bytes": 313532612607, "host_ram_bytes": M.RAM})
    case("K02_292GiB_minus_one", lambda: fail("DISK_FREE", lambda: M.disk_check(config, target, cap, smaller)))
    pins = {"driver": {"path": "/synthetic/driver.py", "sha256": "a" * 64},
            "monitor": {"path": "/synthetic/monitor.py", "sha256": "b" * 64}}
    spec = {"path": "/synthetic/spec.json", "sha256": "c" * 64}
    for name, wrong in ((M.TWIN, M.RAM), ("P1_M0001", M.RAM * 11)):
        caps = dict(M.first_caps(name), rss_cap_bytes=wrong)
        argv = M.monitor_command(pins, spec, target, caps)
        case("K03_K04_" + name, lambda name=name, caps=caps, argv=argv: fail(
            "RSS_CAP_NOT_CALL_CAP", lambda: M.check_monitor_command(argv, pins, spec, target, caps, name)))
    for real in ("driver", "monitor", "dry_harness"):
        fake = {k: {"path": "/synthetic/" + k + ".py", "sha256": "f" * 64} for k in ("driver", "monitor", "dry_harness")}
        fake[real] = M.REAL[real]
        case("V04_real_" + real, lambda fake=fake: fail("SYNTHETIC_REAL_TOOL", lambda: M.synthetic_fence(fake, {})))
    fake = {k: {"path": "/synthetic/" + k + ".py", "sha256": "f" * 64} for k in ("driver", "monitor", "dry_harness")}
    fake["monitor"]["path"] = "/synthetic/root_monitor_c2v999.py"
    case("V04_monitor_name", lambda: fail("SYNTHETIC_REAL_MONITOR_NAME", lambda: M.synthetic_fence(fake, {})))
    fake["monitor"]["path"] = "/synthetic/monitor.py"
    case("V04_volumes", lambda: fail("SYNTHETIC_VOLUMES", lambda: M.synthetic_fence(fake, {"run_volume": "/Volumes/Fake"})))

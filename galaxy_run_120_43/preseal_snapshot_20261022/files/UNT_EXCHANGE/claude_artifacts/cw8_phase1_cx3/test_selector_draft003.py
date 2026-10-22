"""Synthetic file-backed Context and selector tests. No process/science launch."""
import _strptime
import ast
import collections
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback
import types

HERE = Path(__file__).resolve().parent
ART = HERE.parent
TOOL = HERE / "phase1_ngc_launch_cx3cw8_draft003.py"
TOOL_SHA = "2717daf3117f5f6860e8a585c77344261b62021379751e5b0f8608aa61bfd76c"
FIXTURE = ART / "phase1_ngc_launch_kit_cx2v003/test_phase1_ngc_launch_cx2v003.py"
FIXTURE_SHA = "a3cdbdc661b69bd8830ea0b0f68e02674b5319064c7fb8c7060928d971c73f49"
WORK = Path(sys.argv[1]).resolve()
WORK.mkdir()
NOW = "2026-10-22T00:00:00Z"
DATE = subprocess.check_output(["/bin/date", "-u"], text=True).strip()
fixture_raw = FIXTURE.read_bytes()
assert hashlib.sha256(fixture_raw).hexdigest() == FIXTURE_SHA
raw = TOOL.read_bytes()
assert hashlib.sha256(raw).hexdigest() == TOOL_SHA
M = types.ModuleType("cw8_tested_candidate")
M.__file__ = str(TOOL)
exec(compile(raw, str(TOOL), "exec"), M.__dict__)
ACTUAL_SOURCES = copy.deepcopy(M.CW8_SOURCE_PINS)
SOURCE_CHECKS = []
for key, pin in ACTUAL_SOURCES.items():
    digest = hashlib.sha256(Path(pin["path"]).read_bytes()).hexdigest()
    assert digest == pin["sha256"]
    SOURCE_CHECKS.append({"name": key, **pin, "status": "PASS"})
source = fixture_raw.decode()
tree = ast.parse(source)
names = ("hash_bytes", "error_text", "exclusive", "Suite", "full_launch_fixture")
parts = {n.name: ast.get_source_segment(source, n) for n in tree.body
         if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names}
F = types.ModuleType("synthetic_context_fixture")
F.__dict__.update(Path=Path, hashlib=hashlib, json=json, os=os, types=types,
                  traceback=traceback, SYNTHETIC_DRIVER="# inert, never executed\n")
for name in names:
    segment = parts[name]
    if name == "full_launch_fixture":
        segment = segment.replace("P112_LAUNCHER_CX2V003", "P112_LAUNCHER_CX3CW8V001")
        segment = segment.replace('"schema": "P112_CONFIG_CX2V001"',
                                  '"schema": "P112_CONFIG_CX3CW8V001"')
        segment = segment.replace('    config_pin = put("CONFIG.json", cfg)',
                                  "    cfg.update(phase1_ceiling_utc=M.PHASE1_CEILING_UTC,\n"
                                  "               phase2_ceiling_utc=M.PHASE2_CEILING_UTC,\n"
                                  "               cause_records=[], root_stop_records=[])\n"
                                  '    config_pin = put("CONFIG.json", cfg)')
    exec(compile(segment, str(FIXTURE) + ":" + name, "exec"), F.__dict__)
suite = F.Suite(TOOL, WORK / "fixtures", TOOL_SHA)
# Use the same module for source policy and actual Context reconstruction.
suite.module = M
READS = []
ALLOWED = {str(TOOL), str(Path(__file__).resolve())}
ALLOWED.update(pin["path"] for pin in M.SOURCE_PINS.values() if pin["path"].endswith(".py"))


def audit(event, args):
    if event.startswith("socket.") or event in ("os.rename", "os.remove", "os.rmdir",
                                                "os.system", "os.kill", "os.killpg"):
        raise AssertionError("FENCE: " + event)
    if event == "subprocess.Popen" and args[1] != ["/bin/date", "-u"]:
        raise AssertionError("NO_PROCESS_LAUNCH: " + repr(args[1]))
    if event != "open" or not isinstance(args[0], (str, bytes, os.PathLike)):
        return
    path = os.path.realpath(os.fsdecode(args[0]))
    flags = args[2]
    writing = isinstance(flags, int) and bool(flags & (os.O_WRONLY | os.O_RDWR))
    within = path == str(WORK) or path.startswith(str(WORK) + os.sep)
    if writing:
        if not within or os.path.lexists(path):
            raise AssertionError("EXCLUSIVE_WRITE_FENCE: " + path)
    else:
        if not within and path not in ALLOWED:
            raise AssertionError("READ_FENCE: " + path)
        if Path(path).name in ("result.json", "finish.json"):
            raise AssertionError("RUN_CONTENT_FENCE: " + path)
        if not os.path.isdir(path):
            READS.append(path)


sys.addaudithook(audit)
COUNTER = 0
RESULTS = []


def put(path, obj, raw=False):
    return suite.raw_write(path, obj if raw else M.encoded(obj))


def make_context(n=3, mutate_license=None, mutate_record=None, missing_license=False,
                 wrong_root_pin=False):
    global COUNTER
    COUNTER += 1
    # The inherited fixture has one M plus two distinct F (F0 aliases M).
    f = F.full_launch_fixture(suite, "case_%03d" % COUNTER, duplicate_f0=True)
    sysdata = M.read_pin(f.synthetic)["system"]

    def context(config_pin):
        system = M.SyntheticSystem(sysdata)
        system.processes = lambda: []
        system.utc = lambda: NOW
        return M.Context(config_pin, system=system, synthetic_pins=f.overrides)

    ctx = context(f.config)
    assert len([c for c in ctx.calls() if c["origin"] == "P112"]) == 3
    # Inert source substitutions exercise the same exact-pin code. None of
    # these source stubs is executed. Production constants verified above.
    sources = {"driver": f.overrides["driver"]}
    for key in ACTUAL_SOURCES:
        if key != "driver":
            sources[key] = put(f.root / ("synthetic_" + key + ".py"),
                               ("# inert " + key + "\n").encode(), raw=True)
    M.CW8_SOURCE_PINS = sources
    serial = ctx.get_vpin("SPEC_PIN", "S0_SEED_SERIAL")
    twin = ctx.get_vpin("SPEC_PIN", M.TWIN)
    record = {"schema": "UNT_STEP5_NGC_IDENTITY_PAIR_RECORD_C2V001",
              "verdict": M.CW8_EQUAL, "bitwise_equal": True, "iterations_compared": [0, 1],
              "checks": {"synthetic_saved_attestation": True}, "differing_files": [],
              "not_ready": [], "values_printed": False,
              "pins": {"driver": sources["driver"], "checkpoint_module": sources["checkpoint_module"],
                       "tool": sources["comparator"], "serial_spec": serial, "twin_spec": twin}}
    if mutate_record:
        mutate_record(record)
    record_pin = put(f.root / "synthetic_pair_record.json", record)
    license_doc = {"schema": M.CW8_LICENSE_SCHEMA, "date_u": DATE,
                   "scope": "FULL_MEMBER_F_CALLS_ONLY", "comparator_record": record_pin,
                   "source_pins": sources, "seed_serial_spec": serial, "seed_twin_spec": twin,
                   "full_rss_multiplier": 11}
    if mutate_license:
        mutate_license(license_doc)
    license_pin = put(f.root / "synthetic_license.json", license_doc)
    lines = ctx.v006_text
    for c in ctx.calls():
        if c["origin"] == "P112":
            pin, _ = M.read_and_pin(Path(c["spec"]["path"]).parent / M.TWIN_FILE)
            lines += "SPEC_PIN %s_FULL_CW8 %s %s\n" % (c["name"], pin["sha256"], pin["path"])
    if not missing_license:
        lines += "CW8_LICENSE_PIN path=%s sha256=%s\n" % (
            license_pin["path"], "0"*64 if wrong_root_pin else license_pin["sha256"])
    vp = put(f.root / "V006_CW8.md", lines.encode(), raw=True)
    cfg = dict(f.config_doc, v006=vp["path"])
    cp = put(f.root / "CONFIG_CW8.json", cfg)
    ctx = context(cp)
    f.ctx, f.context, f.config = ctx, context, cp
    f.license, f.record, f.sources = license_pin, record_pin, sources
    return f


def forecast(f, cores=0, barrier=0, **changes):
    names = sorted(c["name"] for c in f.ctx.calls() if c["origin"] == "P112")
    doc = {"schema": M.CW8_FORECAST_SCHEMA, "date_u": DATE, "observed_utc": NOW,
           "calls": names, "host_cores": 18, "cores_in_use": cores,
           "remaining_barrier_h": {"expectation": barrier, "upper": barrier},
           "scope": M.cw8_scope(f.ctx)}
    doc.update(changes)
    return put(f.root / "FORECAST.json", doc)


def case(name, action, expected=None):
    start = len(READS)
    try:
        answer = action()
        assert expected is None, "expected refusal " + str(expected)
        assert answer is not False
        RESULTS.append({"name": name, "status": "PASS", "reads": len(READS)-start})
    except M.Refusal as exc:
        RESULTS.append({"name": name, "status": "PASS" if exc.code == expected else "FAIL",
                        "code": exc.code, "expected": expected})
    except Exception as exc:
        RESULTS.append({"name": name, "status": "FAIL", "error": repr(exc),
                        "trace": traceback.format_exc(limit=4)})


def choose(f, **changes):
    pin = forecast(f, **changes)
    result = M.select_workers(f.ctx, pin)
    return result, M.read_pin(result["choice"])


def fallback(*, reason=None, **fixture_changes):
    f = make_context(**fixture_changes)
    result, record = choose(f)
    assert result["column_workers"] == 1 and all(
        M.cw8_workers(c) == 1 for c in f.ctx.calls() if c["origin"] == "P112")
    if reason:
        assert result["reason"] == reason, result
    assert record["prediction"]["reason"] == result["reason"]


case("missing_license_automatic_serial", lambda: fallback(
    missing_license=True, reason="CW8_LICENSE_MISSING"))
case("wrong_root_pin_automatic_serial", lambda: fallback(wrong_root_pin=True))
for verdict in ("DIFFERENT", "NOT_READY"):
    case(verdict + "_automatic_serial", lambda v=verdict: fallback(
        mutate_record=lambda d: d.update(verdict=v), reason="CW8_COMPARATOR_" + v))
case("one_iteration_automatic_serial", lambda: fallback(
    mutate_record=lambda d: d.update(iterations_compared=[0]), reason="CW8_TWO_ITERATIONS_REQUIRED"))
case("bool_iteration_automatic_serial", lambda: fallback(
    mutate_record=lambda d: d.update(iterations_compared=[False, True]),
    reason="CW8_TWO_ITERATIONS_REQUIRED"))
case("false_bitwise_automatic_serial", lambda: fallback(
    mutate_record=lambda d: d.update(bitwise_equal=False), reason="CW8_COMPARATOR_NOT_BITWISE_EQUAL"))
case("wrong_driver_comparator_automatic_serial", lambda: fallback(
    mutate_record=lambda d: d["pins"].update(driver={"path": "/not-opened.py", "sha256": "f"*64}),
    reason="CW8_COMPARATOR_PINS"))
case("wrong_worker_license_automatic_serial", lambda: fallback(
    mutate_license=lambda d: d.update(source_pins={}), reason="CW8_WORKER_SOURCE_PINS"))
case("rss_not_ruled_automatic_serial", lambda: fallback(
    mutate_license=lambda d: d.update(full_rss_multiplier=1), reason="CW8_RSS_RULING_REQUIRED"))
case("checks_false_automatic_serial", lambda: fallback(
    mutate_record=lambda d: d.update(checks={"bad": False}), reason="CW8_COMPARATOR_CHECKS"))
case("checks_integer_not_bool_automatic_serial", lambda: fallback(
    mutate_record=lambda d: d.update(checks={"bad": 1}), reason="CW8_COMPARATOR_CHECKS"))


def positive():
    f = make_context()
    pin = forecast(f)
    start = len(READS)
    result = M.select_workers(f.ctx, pin)
    counts = collections.Counter(READS[start:])
    assert counts and max(counts.values()) == 1, counts
    assert result["column_workers"] == 8
    restored = f.context(f.config)
    calls = restored.calls()
    for call in calls:
        if call["origin"] != "P112":
            assert call["name"] == M.TWIN and M.cw8_role(call)["kind"] == "IDENTITY_TWIN"
            continue
        assert M.cw8_workers(call) == 8
        assert call["spec"] != call["serial_spec"]
        assert call["spec"] == restored.get_vpin("SPEC_PIN", call["name"]+"_FULL_CW8")
        assert M.cw8_role(call)["choice"] == result["choice"]
    return f, restored, result


case("positive_actual_context_restore_and_single_read", positive)
case("load_12_cores_three_calls_keeps_serial", lambda:
     choose(make_context(), cores=6)[0]["column_workers"] == 1)
case("S0_barrier_masks_gain_keeps_serial", lambda:
     choose(make_context(), barrier=100)[0]["reason"] == "NO_STRICT_MAKESPAN_GAIN")
case("stale_forecast_keeps_serial", lambda:
     choose(make_context(), observed_utc="2026-10-21T00:00:00Z")[0]["reason"] == "CW8_FORECAST_STALE_OR_FUTURE")
case("future_forecast_keeps_serial", lambda:
     choose(make_context(), observed_utc="2026-10-23T00:00:00Z")[0]["reason"] == "CW8_FORECAST_STALE_OR_FUTURE")
case("unknown_load_keeps_serial", lambda:
     choose(make_context(), cores=7)[0]["reason"] == "CW8_MODEL_LOAD_OUT_OF_SCOPE")
case("wrong_cohort_keeps_serial", lambda:
     choose(make_context(), calls=[])[0]["reason"] == "CW8_FORECAST_CALL_SET")


def no_reselection():
    f, ctx, _ = positive()
    ctx.system.utc = lambda: "2026-10-25T00:00:00Z"
    return M.select_workers(ctx, None)


case("existing_choice_not_recomputed_from_later_time", no_reselection, "CW8_NO_NEW_CALLS")


def changed_theta():
    f, ctx, _ = positive()
    call = next(c for c in ctx.calls() if c["origin"] == "P112")
    base = dict(call, spec=call["serial_spec"], theta_sha256="f"*64)
    return M.cw8_apply_choice(ctx, base)


case("equal_point_but_changed_theta_refuses", changed_theta, "CW8_CHOICE_CALL_BINDING")


def raw_pair(extra=False):
    serial = M.encoded({"physical": {"a": 1.25}, "numerics": {"route_a": {"column_workers": 1}}})
    twin = serial.replace(b'"column_workers": 1', b'"column_workers": 8')
    if extra:
        twin = twin.replace(b"1.25", b"1.26")
    return M.cw8_spec_pair(serial, twin)


case("raw_worker_only_pair_passes", raw_pair)
case("other_numeric_byte_change_refuses", lambda: raw_pair(True), "CW8_NONWORKER_BYTES_CHANGED")
case("whitespace_change_refuses", lambda: M.cw8_spec_pair(
    b'{"numerics":{"route_a":{"column_workers":1}}}',
    b'{"numerics": {"route_a":{"column_workers":8}}}'), "CW8_NONWORKER_BYTES_CHANGED")


def roles():
    f, ctx, result = positive()
    call = next(c for c in ctx.calls() if c["origin"] == "P112")
    role = M.cw8_role(call)
    cap = M.first_caps(call["name"], 8)
    assert cap["output_cap_bytes"] == M.CAPS["serial"]["output_cap_bytes"]
    assert cap["rss_cap_bytes"] == M.RAM*11
    assert role["kind"] == "FULL" and call["name"] != M.TWIN
    assert M.cw8_plan_workers({"name":call["name"], "worker_role":role, "spec":call["spec"]}) == 8
    return f, ctx, call, role, cap


case("full_role_full_output_eleven_ram_no_twin_name", roles)
case("full_cw8_without_choice_refuses", lambda: M.cw8_workers(
    {"name":"P1_M0001", "origin":"P112", "spec_doc":{"numerics":{"route_a":{"column_workers":8}}}}),
    "CW8_FULL_CALL_UNAUTHORIZED")


def changed_role(change):
    f, ctx, call, role, cap = roles()
    rec = {"caps": cap, "spec": call["spec"], "worker_role": role, "watch_pid": None}
    change(rec, call)
    return M.cw8_check_attempt(ctx, call, rec)


case("full_call_with_twin_watcher_refuses", lambda: changed_role(
    lambda r,c:r.update(watch_pid=700001)), "CW8_FULL_CALL_TWIN_WATCHER")
case("old_raw_spec_receipt_refuses", lambda: changed_role(
    lambda r,c:r.update(spec=c["serial_spec"])), "CW8_ATTEMPT_RAW_SPEC")
case("full_call_twin_role_refuses", lambda: changed_role(
    lambda r,c:r["worker_role"].update(kind="IDENTITY_TWIN")), "CW8_ROLE_CUSTODY")
case("full_call_one_ram_refuses", lambda: changed_role(
    lambda r,c:r["caps"].update(rss_cap_bytes=M.RAM)), "CW8_ATTEMPT_RSS")


def retry_output():
    _, ctx, call, role, cap = roles()
    actual = [{"status_class":"OUTPUT_CAP", "raw_status":"OUTPUT_CAP|NONE",
               "attempt":1, **cap}]
    answer = M.next_attempt(call["name"], [{"attempt":1,"origin":"P112","outcome":"LAUNCH"}],
                            actual, set(), phase_ceiling_utc=M.PHASE1_CEILING_UTC,
                            monitor_ceiling_utc=M.PHASE2_CEILING_UTC, now_utc=NOW, column_workers=8)
    assert answer["caps"]["output_cap_bytes"] == cap["output_cap_bytes"]*2
    assert answer["caps"]["rss_cap_bytes"] == M.RAM*11
    assert answer["caps"]["wall_cap_s"] == M.remaining_wall(M.PHASE2_CEILING_UTC, NOW)
    assert answer["solo_mode"] is True


case("A244_output_doubles_full_cw8_A249_wall_retained", retry_output)
for n in (1,2,3):
    for available in (12,14,16,18):
        for scenario, cost in M.CW8_COSTS.items():
            expected = ((n+available//8-1)//(available//8))*cost["parallel_a_h"] + cost["parallel_tail_h"]
            case("model_%d_%d_%s" % (n,available,scenario),
                 lambda n=n,a=available,c=cost,e=expected: abs(M.cw8_schedule(n,a,8,c)-e)<1e-10)

"""Additional metadata-only preparation cases, embedded into the selector suite."""


def public_dry(f):
    ctx=f.ctx
    old_dry=M.run_dry
    def inert_dry(c,call,work):
        return c.write(str(Path(work)/"dry_verdict.json"), {
            "schema":"P112_DRY_VERDICT_CX2V001","ok":True,"date_u":DATE,
            "synthetic_no_process":True,"worker_role":M.cw8_role(call),
            "expected_leaf":M.cw8_workers(call),"spec":call["spec"]})
    M.run_dry=inert_dry
    ctx.system.processes=lambda:[
        {"pid":os.getpid(),"ppid":1,"pgid":os.getpid(),"command":"synthetic P112 --dry"},
        {"pid":900071,"ppid":1,"pgid":900071,"command":"python "+f.watch["path"]}]
    try:
        answer=M.launch(ctx,"P1_M0001",dry=True)
    finally:
        M.run_dry=old_dry
        ctx.system.processes=lambda:[]
    assert answer["status"]=="DRY_NOT_LAUNCHED"
    assert M.cw8_saved_choices(ctx)=={}
    plan=M.read_pin(answer["plan"])
    assert plan["dry_only"] is True and plan["worker_role"]["column_workers"]==1
    return plan,answer


def dry_then_select():
    f=make_context()
    plan,_=public_dry(f)
    result,doc=choose(f)
    assert result["column_workers"]==8
    assert f.ctx.call("P1_M0001")["spec"]!=plan["spec"]
    assert M.read_pin(plan["spec"])["numerics"]["route_a"]["column_workers"]==1


case("public_dry_does_not_commit_serial_before_pair",dry_then_select)


def dry_with_process_evidence():
    f=make_context()
    plan,_=public_dry(f)
    put(Path(plan["work"])/"sampler.stdout.txt",b"synthetic process-start evidence\n",raw=True)
    return choose(f)


case("dry_flag_cannot_hide_process_preparation",dry_with_process_evidence,
     "CW8_ROLE_ALREADY_PREPARED")


def legacy_preparation(explicit_select=False):
    f=make_context()
    M.create_layout(f.ctx)
    work=Path(f.ctx.cfg["p112_launch_root"])/"work"/"P1_M0001_A1_OLD"
    work.mkdir()
    put(work/"plan.json",{"schema":"UNT_P112_LAUNCH_PLAN_CX2V001",
                          "name":"P1_M0001","attempt":1})
    call=f.ctx.call("P1_M0001")
    if explicit_select:
        return choose(f)
    assert M.cw8_ensure_default(f.ctx,call) is call
    assert M.cw8_workers(call)==1 and M.cw8_saved_choices(f.ctx)=={}


case("unlabelled_old_preparation_retains_serial",legacy_preparation)
case("unlabelled_old_preparation_cannot_upgrade",lambda:legacy_preparation(True),
     "CW8_ROLE_ALREADY_PREPARED")


def residual_keeps_serial():
    f=make_context()
    call=f.ctx.call("P1_M0001")
    f.ctx.residuals=lambda:{("P1_M0001",1)}
    assert M.cw8_ensure_default(f.ctx,call) is call
    assert M.cw8_saved_choices(f.ctx)=={}


case("historical_residual_never_gets_new_role",residual_keeps_serial)


def default_is_logged():
    f=make_context(missing_license=True)
    call=M.cw8_ensure_default(f.ctx,f.ctx.call("P1_M0001"))
    assert M.cw8_workers(call)==1 and M.is_pin(call["worker_choice"])
    doc=M.read_pin(call["worker_choice"])
    assert doc["prediction"]=={"column_workers":1,"reason":"NO_SELECTION_INPUT"}


case("fresh_default_serial_has_durable_reason",default_is_logged)


report = {"date_u": DATE, "tool": {"path":str(TOOL),"sha256":TOOL_SHA},
          "test": {"path":str(Path(__file__).resolve()),
                   "sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
          "fixture_source": {"path":str(FIXTURE),"sha256":FIXTURE_SHA},
          "fixed_production_sources_verified_from_bytes": SOURCE_CHECKS,
          "scope": "TESTED synthetic metadata only; exact pin constants substituted with inert fixture sources inside test module",
          "UNTESTED": ["production identity record", "real load/timing", "scientific launch",
                       "consumer replay (separate pending test)", "root adoption"],
          "cases": RESULTS, "passed": sum(r["status"]=="PASS" for r in RESULTS),
          "failed": sum(r["status"]!="PASS" for r in RESULTS)}
put(WORK/"EVIDENCE.json", report)
print(json.dumps({"passed":report["passed"],"failed":report["failed"],
                  "failures":[r for r in RESULTS if r["status"]!="PASS"]}, sort_keys=True))
sys.exit(bool(report["failed"]))

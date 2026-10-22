"""Replay saved, synthetic full-call metadata through real P112 and consumers.

No launch entry point, monitor, sampler, driver, comparator, result reader or
scientific engine is executed. Resume is exercised only with saved completed
metadata, ordinary full-call names and an audit fence blocking subprocesses.
"""
import ast
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
fixture_source_path = HERE / "test_selector_cx3v001.py"
fixture_raw = fixture_source_path.read_bytes()
fixture_source = fixture_raw.decode()
prefix = fixture_source.split('\ncase("missing_license_automatic_serial"')[0]
exec(compile(prefix, str(fixture_source_path) + ":definitions", "exec"), globals())
BUILDER = HERE / "roster_builder_c2v007_cx3cw8v001.py"
BUILDER_SHA = "e6102ba15542e6b2a10c073b4f8647c48facaadf2209d664818e81ee6058da31"
ALLOWED.add(str(BUILDER))
braw = BUILDER.read_bytes()
assert hashlib.sha256(braw).hexdigest() == BUILDER_SHA
B = types.ModuleType("cw8_consumer_custody")
B.__file__ = str(BUILDER)
exec(compile(braw, str(BUILDER), "exec"), B.__dict__)
SAVED = []


def source_pin(path):
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def saved_monitor(ctx, call, outdir, caps, *, start="2026-10-22T00:00:12Z",
                  end="2026-10-22T00:00:14Z"):
    Path(outdir).mkdir()
    # Opaque synthetic result bytes exist solely to supply a true byte pin.
    # No tool or test reads these bytes back; the audit fence prohibits it.
    result_pin = put(Path(outdir)/"result.json",
                     {"synthetic": True, "status": "COMPLETED", "valid": False})
    pins = {key: ctx.pins[key] for key in ("driver", "monitor")}
    pins["spec"] = call["spec"]
    launch = {"schema": M.MONITOR_SCHEMA + "_LAUNCH", "utc": start, "child_pid": 900004,
              "pins": pins, "caps": caps, "outdir": outdir, "retries_allowed": 0,
              "command": M.driver_command(pins, call["spec"], outdir)}
    launch_pin = put(Path(outdir+".receipt.json.launch.json"), launch)
    receipt = {"schema": M.MONITOR_SCHEMA, "utc_start": start, "utc_end": end,
               "child_pid": 900004, "pins": pins, "caps": caps, "status": "FINISHED",
               "driver_status": "COMPLETED", "exit_code": 0, "result": result_pin}
    receipt["receipt_sha256"] = M.sha(M.canonical(receipt))
    monitor_pin = put(Path(outdir+".receipt.json"), receipt)
    return launch, launch_pin, receipt, monitor_pin


def save_full(ctx, call, *, legacy_entry=False):
    name = call["name"]
    assert name != M.TWIN
    M.create_layout(ctx)
    hist = M.history(ctx, call)
    decision = M.decision_for(ctx, call, hist, now_utc=NOW)
    work = Path(ctx.cfg["p112_launch_root"])/"work"/(name+"_A1_SAVED")
    work.mkdir()
    m15_pin, m15 = ctx.seed_check()
    own_command = M.PY + " -I -B " + str(TOOL) + " launch --name " + name
    ctx.system.processes = lambda: [{"pid":os.getpid(), "ppid":1, "pgid":os.getpid(),
                                    "command":own_command}]
    plan = M.make_plan(ctx, call, decision, work, m15_pin, m15)
    bootstrap_pin = ctx.write(str(work/"plan.json"), plan)
    dry_pin = ctx.write(str(work/"saved_synthetic_dry.json"), {
        "schema":"P112_DRY_VERDICT_CX2V001", "ok":True, "synthetic":True,
        "worker_role":M.cw8_role(call), "expected_leaf":M.cw8_workers(call),
        "spec":call["spec"], "driver":ctx.pins["driver"], "date_u":DATE})
    if legacy_entry:
        # Model an already-registered ordinary serial, whose immutable entry
        # has no new worker-role field. It is never rewritten.
        assert M.cw8_workers(call) == 1 and call.get("worker_choice") is None
        record = {key:call[key] for key in ("name","kind","alternative","key","point_key",
                  "theta_sha256","spec","v006_spec_pin","v006_handoff_pin","handoff","certificates")}
        record.update(schema="UNT_P112_LAUNCH_REGISTRY_ENTRY_CX2V001",
                      plan_output_primary=ctx.cfg["plan_output_primary"], fdplan=ctx.cfg["fdplan"],
                      driver=ctx.pins["driver"], config=ctx.config_pin, date_u=DATE)
        entry_pin = ctx.write(M.own_registry_path(ctx,name), record)
    else:
        entry_pin = M.register_call(ctx,call,plan,dry_pin,work,hist)
    final, final_pin = M.write_launch_commit(ctx,plan,bootstrap_pin,work,"2026-10-22T00:00:10Z")
    assert final["caps"]["wall_cap_s"] == M.remaining_wall(
        M.PHASE2_CEILING_UTC, "2026-10-22T00:00:10Z")
    assert final["spec"] == call["spec"] and final["worker_role"] == M.cw8_role(call)
    lj, lj_pin, monitor, monitor_pin = saved_monitor(ctx,call,final["outdir"],final["caps"])
    ctx.write(str(work/"invocation.json"), {
        "schema":"P112_INVOCATION_CX2V001","invocation_pid":900005,
        "invocation_command":own_command,"sampler_pid":900002,
        "planned_monitor_argv":final["monitor_argv"],"plan":final_pin,"date_u":DATE})
    ctx.write(str(work/"monitor_pid.json"), {
        "schema":"P112_MONITOR_PID_CX2V001","monitor_pid":900001,"plan":final_pin,"date_u":DATE})
    ctx.system.processes = lambda: []
    before = len(READS)
    launch_record = M.launch_resume(ctx,name,1)
    counts = collections.Counter(READS[before:])
    assert counts and max(counts.values()) == 1, counts
    rec = M.read_pin(launch_record)
    assert rec["outcome"] == "LAUNCH" and rec["watch_pid"] is None
    assert rec["spec"] == call["spec"] and rec["worker_role"] == M.cw8_role(call)
    assert rec["registry_entry"] == entry_pin and rec["plan"] == final_pin
    closed = M.close_attempt(ctx,name,1)
    assert closed["status_class"] == "FINISHED"
    return {"name":name,"receipt":closed["receipt"],"entry":entry_pin,
            "record":launch_record,"bootstrap":bootstrap_pin,"commit":final_pin,
            "raw_spec":call["spec"],"workers":M.cw8_workers(call)}


def save_twin(ctx):
    call = ctx.call(M.TWIN)
    outdir = M.planned_outdir(ctx,M.TWIN,1,"KIT")
    caps = M.first_caps(M.TWIN)
    lj, ljpin, monitor, mpin = saved_monitor(ctx,call,outdir,caps)
    rec = {"schema":"UNT_S0_LAUNCH_RECORD_C2V003A","name":M.TWIN,"attempt":1,
           "outcome":"LAUNCH","outdir":outdir,"receipt":outdir+".receipt.json",
           "launch_json":dict(ljpin,utc=lj["utc"],child_pid=lj["child_pid"]),
           "spec":call["spec"],"driver":ctx.pins["driver"],"monitor":ctx.pins["monitor"],
           "caps":caps,"monitor_pid":900001,"sampler_pid":None,"watch_pid":None,
           "solo_mode":False,"counted_rerun":False,"date_u":DATE}
    rp=put(Path(ctx.cfg["s0"]["launch_root"])/"launches"/
           (M.TWIN+"_LAUNCH_C2V003A_A1.json"),rec)
    closed=M.close_attempt(ctx,M.TWIN,1)
    return {"name":M.TWIN,"receipt":closed["receipt"],"record":rp,
            "raw_spec":call["spec"],"workers":8}


def consumer_factory(f):
    # Only external fixture source pins/system identity are substituted.
    # The successor Context, selector, registry assembler and single-buffer
    # read bridge execute unmodified.
    def make(module, config_pin):
        module.CW8_SOURCE_PINS = copy.deepcopy(f.sources)
        system = module.SyntheticSystem({
            "mount_points":[f.config_doc["run_volume"],str(f.root/"kit_volume")],
            "free_bytes":1<<50,"host_ram_bytes":module.RAM})
        system.processes=lambda:[]
        system.utc=lambda:NOW
        return module.Context(config_pin,system=system,synthetic_pins=f.overrides)
    return make


def integration(mixed=False):
    f=make_context()
    ctx=f.ctx
    saved=[]
    legacy=None
    if mixed:
        call=ctx.call("P1_M0001")
        legacy=save_full(ctx,call,legacy_entry=True)
        saved.append(legacy)
    remaining=sorted(c["name"] for c in ctx.calls() if c["origin"]=="P112" and
                     (legacy is None or c["name"]!=legacy["name"]))
    fp=forecast(f,calls=remaining)
    selection=M.select_workers(ctx,fp)
    assert selection["column_workers"]==8
    if legacy:
        unchanged=ctx.call(legacy["name"])
        assert M.cw8_workers(unchanged)==1 and unchanged["spec"]==legacy["raw_spec"]
        assert M.cw8_ensure_default(ctx,unchanged) is unchanged
        assert M.history(ctx,unchanged,inspect_next=False)["actual"][0]["spec_sha256"]==legacy["raw_spec"]["sha256"]
    for name in remaining:
        saved.append(save_full(ctx,ctx.call(name)))
    saved.append(save_twin(ctx))
    # The synthetic PLAN excludes the seed itself. Model its root stop metadata;
    # no real seed or scientific output is opened or altered.
    put(Path(ctx.cfg["p112_launch_root"])/"outside_set_stop"/"S0_SEED_SERIAL_A1_CX2V001.json",{
        "schema":"S0_OUTSIDE_SET_STOP_RECORD_C2V001","name":"S0_SEED_SERIAL",
        "plan_output_primary":ctx.cfg["plan_output_primary"],"fdplan":ctx.cfg["fdplan"],
        "date_u":DATE,"synthetic":True})
    assembly=M.assemble_registry(ctx)
    assert M.assemble_registry(ctx,verify=True)["status"]=="VERIFIED"
    registry=M.read_pin(assembly["registry"])
    assert {r["spec_sha256"] for r in registry["calls"]}=={r["raw_spec"]["sha256"] for r in saved}
    evidence=M.read_pin(assembly["assembly_record"])
    assert selection["choice"] in evidence["sources"]
    B._registry_context_factory=consumer_factory(f)
    doc={"phase":"PHASE_1","launch_registry":assembly["registry"],
         "registry_verification":{"launcher":ctx.own_pin,"config":ctx.config_pin,
                                  "assembly_record":assembly["assembly_record"]},
         "plan_outputs":{M.PRIMARY:ctx.cfg["plan_output_primary"]}}
    before=len(READS)
    verified=B.verify_launch_registry(doc)
    counts=collections.Counter(READS[before:])
    assert max(counts.values())==1,counts
    assert verified["verdict"]=="BYTE_EQUAL"
    receipt_config=B._receipt_cfg(M.RECEIPT_KEYS,M.STATUS_CLASSES)
    for item in saved:
        before=len(READS)
        result=B.command_snapshot(B._receipt)(item["receipt"],receipt_config,"cw8-synthetic")
        counts=collections.Counter(READS[before:])
        assert max(counts.values())==1,counts
        assert result[2]=="FINISHED"
        assert result[4]["column_workers"]==item["workers"]
        assert result[5]["spec_sha256"]==item["raw_spec"]["sha256"]
        # An independent new Context reproduces exact stored roles.
        restored=consumer_factory(f)(M,ctx.config_pin)
        call=restored.call(item["name"])
        assert call["spec"]==item["raw_spec"] and M.cw8_workers(call)==item["workers"]
    SAVED.append({"mixed_serial_history":mixed,"selection":selection,"assembly":assembly,
                  "receipts":saved,"consumer_verdict":verified})
    return True


case("full_cw8_commit_resume_close_registry_consumer_single_read",integration)
case("serial_history_retained_next_to_new_cw8_custody",
     lambda:integration(mixed=True))


def old_baseline_roles():
    for name,workers in (("P1_M0001",1),(M.TWIN,8)):
        baseline={"kind":"IDENTITY_TWIN" if name==M.TWIN else "FULL",
                  "column_workers":workers,"choice":None}
        for doc_role,record_role in ((None,None),(baseline,None),(baseline,baseline)):
            assert B._cw8_receipt_workers({"worker_role":doc_role},{"name":name},
                None,{"worker_role":record_role},"legacy")==workers
    return True


case("immutable_legacy_entries_allow_explicit_baseline_roles",old_baseline_roles)

report={"date_u":DATE,"scope":__doc__,"tool":{"path":str(TOOL),"sha256":TOOL_SHA},
        "builder":{"path":str(BUILDER),"sha256":BUILDER_SHA},
        "test":source_pin(Path(__file__).resolve()),
        "fixture_source":{"path":str(fixture_source_path),"sha256":hashlib.sha256(fixture_raw).hexdigest()},
        "cases":RESULTS,"passed":sum(r["status"]=="PASS" for r in RESULTS),
        "failed":sum(r["status"]!="PASS" for r in RESULTS),"saved_custody":SAVED,
        "seams":["inert synthetic source pins and SyntheticSystem in actual Context",
                 "saved completed monitor/launch metadata; no process was started",
                 "synthetic dry verdict; numerical dry harness not executed"],
        "UNTESTED":["real identity comparator record","production load/time",
                    "G26/step-7 on these exact cw8 records (separate inherited replay tests exist)",
                    "root adoption and distinct review"]}
put(WORK/"EVIDENCE.json",report)
print(json.dumps({"passed":report["passed"],"failed":report["failed"],
                  "failures":[r for r in RESULTS if r["status"]!="PASS"]},sort_keys=True))
sys.exit(bool(report["failed"]))

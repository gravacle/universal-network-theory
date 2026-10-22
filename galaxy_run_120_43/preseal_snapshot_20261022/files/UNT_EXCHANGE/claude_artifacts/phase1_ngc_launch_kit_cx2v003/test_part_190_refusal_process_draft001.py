"""Process faults are injected; every possible signal is intercepted locally."""


def refusal_process_cases(suite):
    import contextlib
    import io
    import json
    import os
    import types
    from pathlib import Path
    M, case, fail = suite.module, suite.case, suite.refuses
    def bad(code,action):
        case("REFUSE_"+code,lambda:fail(code,action))
    f=receipt_fixture(suite,"resume_missing_states")
    bad("ATTEMPT_ALREADY_RECORDED",lambda:M.launch_resume(f.ctx,f.name,1))
    bad("RESUME_LAUNCH_JSON_MISSING",lambda:M.launch_resume(f.ctx,f.name,2))
    bad("RESUME_ARGUMENTS",lambda:M.launch(f.ctx,f.name,resume=True))
    f=receipt_fixture(suite,"resume_missing_invocation",record=False)
    bad("RESUME_INVOCATION_MISSING",lambda:M.launch_resume(f.ctx,f.name,1))
    f=resume_fixture(suite,"resume_no_command",invocation_changes={"invocation_command":None})
    bad("RESUME_INVOCATION_COMMAND_MISSING",lambda:M.launch_resume(f.ctx,f.name,1))
    f=resume_fixture(suite,"resume_wrong_config")
    f.ctx.config_pin=f.entry_pin
    bad("RESUME_PLAN_BINDING",lambda:M.launch_resume(f.ctx,f.name,1))
    f=resume_fixture(suite,"resume_changed_spec")
    other=suite.fixture("resume_different_spec.json",{"synthetic":True})
    entry=dict(M.read_pin(f.entry_pin),spec=other)
    ep=suite.fixture("resume_different_entry.json",entry)
    f.call.update(spec=other,entry=entry,entry_pin=ep)
    bad("RESUME_SPEC_BINDING",lambda:M.launch_resume(f.ctx,f.name,1))
    f=receipt_fixture(suite,"missing_retry_registry")
    call=dict(f.call,name="P1_M0099")
    bad("RETRY_REGISTRY_ENTRY_MISSING",lambda:M.register_call(
        f.ctx,call,{"attempt":2},f.entry_pin,f.root,{"records":[f.record],"residuals":set(),"refusals":[]}))
    bad("SAMPLER_POLL",lambda:M.sampler(f.ctx,{},str(f.root),poll_s=11))
    bad("SAMPLER_CONFIG_BINDING",lambda:M.sampler(
        f.ctx,{"name":f.name,"attempt":1,"outdir":f.outdir,"config":{}},str(f.root)))
    work=f.root/"launch_root"/"work"/"multiple_monitors"
    work.mkdir()
    command=M.PY+" -I -B "+f.ctx.pins["monitor"]["path"]+" --receipt "+f.outdir+".receipt.json"
    f.ctx.system.rows=[{"pid":900001,"ppid":1,"pgid":900001,"command":command},
                       {"pid":900002,"ppid":1,"pgid":900002,"command":command}]
    bad("MULTIPLE_MONITORS",lambda:M.sampler(
        f.ctx,{"name":f.name,"attempt":1,"outdir":f.outdir,"config":f.ctx.config_pin},str(work)))
    row={"pid":900005,"ppid":1,"pgid":900006,"command":"/synthetic/inert"}
    f.ctx.system.rows=[row]
    bad("NOT_GROUP_LEADER",lambda:M.stop_qualified(f.ctx.system,900005,lambda r:True,group=True))
    row["pgid"]=row["pid"]
    clock=[0.0]
    f.ctx.system.monotonic=lambda:clock[0]
    f.ctx.system.sleep=lambda seconds:clock.__setitem__(0,clock[0]+20)
    kill=M.os.kill
    signals=[]
    def unresponsive():
        M.os.kill=lambda pid,sig:signals.append((pid,int(sig)))
        try:
            fail("PROCESS_STILL_ALIVE_AFTER_STOP",lambda:M.stop_qualified(f.ctx.system,900005,lambda r:True))
        finally:
            M.os.kill=kill
        suite.eq([p for p,sig in signals],[900005,900005])
    case("REFUSE_PROCESS_STILL_ALIVE_AFTER_STOP",unresponsive)
    f=receipt_fixture(suite,"duplicate_watch",name=M.TWIN)
    outdir=f.outdir
    command="/bin/bash "+f.ctx.pins["twin_watch"]["path"]+" --outdir "+outdir
    f.ctx.system.rows=[{"pid":900001,"ppid":1,"pgid":900001,"command":command},
                       {"pid":900002,"ppid":1,"pgid":900002,"command":command}]
    m15=suite.fixture("watch_m15.json",{"date_u_epoch_s":int(M.timestamp(f.rec["utc_start"]))-1})
    plan=dict(f.record,pins={"driver":f.ctx.pins["driver"],"monitor":f.ctx.pins["monitor"]},
              launch_json=outdir+".receipt.json.launch.json",m15_record=m15)
    bad("TWIN_WATCH_DUPLICATE",lambda:M.finish_launch(f.ctx,plan,f.entry_pin,f.entry_pin,900001,900002))
    outdir=M.planned_outdir(f.ctx,f.name,2,"P112")
    plan=dict(plan,attempt=2,outdir=outdir,launch_json=outdir+".receipt.json.launch.json")
    bad("NO_MISLAUNCH_WITHOUT_LAUNCH_JSON",lambda:M.write_launch_record(
        f.ctx,plan,f.entry_pin,f.entry_pin,900001,900002,None,{"parseable":False},snapshot=(None,None)))

    f=full_launch_fixture(suite,"invocation_faults")
    def context():
        c=M.Context(f.config,system=M.SyntheticSystem(M.read_pin(f.synthetic)["system"]),synthetic_pins=f.overrides)
        c.system.processes=lambda:[
            {"pid":os.getpid(),"ppid":1,"pgid":os.getpid(),"command":M.PY+" -I -B /synthetic/fault_test.py"},
            {"pid":900111,"ppid":1,"pgid":900111,"command":M.PY+" -I -B "+f.watch["path"]}]
        return c
    c=context()
    bad("ATTEMPT_NUMBER",lambda:M.launch(c,f.name,attempt=99))
    dry_failure=suite.bytes_fixture("inert_dry_failure.py",b"raise SystemExit(1)\n")
    c.pins["dry_harness"]=dry_failure
    work=f.root/"dry_failure_work"
    work.mkdir()
    bad("DRY_HARNESS_EXIT",lambda:M.run_dry(c,c.call(f.name),work))
    target=f.root/"layout_target"
    target.mkdir()
    (f.root/"launch_root"/"registry").symlink_to(target,target_is_directory=True)
    bad("LAUNCH_SUBDIR_REAL",lambda:M.create_layout(c))
    plan_pin=suite.fixture("wrong_sampler_outdir_plan.json",{"outdir":"/synthetic/other"})
    output=io.StringIO()
    def wrong_sampler_cli():
        with contextlib.redirect_stdout(output):
            result=M.cli(["_sampler","--config",f.config["path"],"--config-sha256",f.config["sha256"],
                          "--synthetic-pins",f.synthetic["path"],"--synthetic-pins-sha256",f.synthetic["sha256"],
                          "--plan",plan_pin["path"],"--plan-sha256",plan_pin["sha256"],"--outdir","/synthetic/NGC_RUN"])
        suite.eq((result,json.loads(output.getvalue())["code"]),(2,"SAMPLER_OUTDIR"))
    case("REFUSE_SAMPLER_OUTDIR",wrong_sampler_cli)
    for missing in (True,False):
        code="SAMPLER_FIRST_SAMPLE_MISSING" if missing else "SAMPLER_FIRST_SAMPLE_FAILED"
        g=full_launch_fixture(suite,"first_sample_"+code)
        c=M.Context(g.config,system=M.SyntheticSystem(M.read_pin(g.synthetic)["system"]),synthetic_pins=g.overrides)
        c.synthetic_pin=g.synthetic
        clock=[0.0]
        c.system.monotonic=lambda:clock[0]
        c.system.sleep=lambda seconds:clock.__setitem__(0,clock[0]+max(seconds,1))
        c.system.processes=lambda:[
            {"pid":os.getpid(),"ppid":1,"pgid":os.getpid(),"command":M.PY+" -I -B /synthetic/fault_test.py"},
            {"pid":900111,"ppid":1,"pgid":900111,"command":M.PY+" -I -B "+g.watch["path"]}]
        original_popen=M.subprocess.Popen
        def fake_sampler(argv,*args,**kwargs):
            if "_sampler" not in argv:
                return original_popen(argv,*args,**kwargs)
            if not missing:
                pp=Path(argv[argv.index("--plan")+1])
                suite.raw_write(pp.parent/"sampler_first_sample.json",M.encoded({"ok":False}))
            return types.SimpleNamespace(pid=900222)
        def launch_fault():
            M.subprocess.Popen=fake_sampler
            try:
                fail(code,lambda:M.launch(c,g.name))
            finally:
                M.subprocess.Popen=original_popen
            suite.eq(list(Path(c.cfg["run_root"]).iterdir()),[])
        case("REFUSE_"+code,launch_fault)
    suite.interfaces["process_fault_injection"] = (
        "TESTED malformed saved invocation states and injected sampler/process failures. "
        "The unresponsive-process test intercepts both signals; it signals no OS process. "
        "Missing/failed first-sample tests replace only sampler Popen, before any monitor start.")

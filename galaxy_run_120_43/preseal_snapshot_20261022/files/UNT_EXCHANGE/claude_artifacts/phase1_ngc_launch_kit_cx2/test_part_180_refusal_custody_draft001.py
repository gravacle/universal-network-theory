"""Saved-record and receipt custody failures, always with new synthetic files."""


def refusal_custody_cases(suite):
    import copy
    from pathlib import Path
    M, case, fail = suite.module, suite.case, suite.refuses
    def bad(code, action):
        case("REFUSE_"+code,lambda:fail(code,action))
    for code, changes in (
            ("ATTEMPT_FILENAME_BINDING",{"attempt":2}),
            ("ATTEMPT_RECORD_SCHEMA",{"schema":"WRONG"}),
            ("LAUNCH_JSON_RECORD_PIN",None)):
        f=receipt_fixture(suite,"record_"+code,record=False)
        rec=copy.deepcopy(f.record)
        if changes is None:
            rec["launch_json"]["sha256"]="a"*64
        else:
            rec.update(changes)
        suite.raw_write(f.record_path,M.encoded(rec))
        bad(code,(lambda f=f:M.close_attempt(f.ctx,f.name,1)) if changes is None else (lambda f=f:f.ctx.records()))
    f=receipt_fixture(suite,"location_refusals")
    bad("ATTEMPT_RECORD_MISSING",lambda:M.close_attempt(f.ctx,f.name,2))
    bad("ATTEMPT_PATH_BINDING",lambda:M.validate_record_location(f.ctx,dict(f.record,origin="P112",outdir="/synthetic/wrong")))
    bad("ATTEMPT_LAUNCH_JSON_PATH",lambda:M.validate_record_location(f.ctx,dict(f.record,origin="P112",launch_json={"path":"/synthetic/wrong"})))
    bad("ATTEMPT_NEEDS_CLOSE",lambda:M.history(f.ctx,f.call))
    bad("REGISTRY_ENTRY_MISSING",lambda:M.registered_entry(f.ctx,dict(f.call,name="P1_M0099")))
    for code, schema in (("REGISTRY_SCHEMA","WRONG"),("REGISTRY_CALL_BINDING","UNT_P112_LAUNCH_REGISTRY_ENTRY_CX2V001")):
        name="P1_M0098" if code=="REGISTRY_SCHEMA" else "P1_M0097"
        entry=dict(M.read_pin(f.entry_pin),name=name,schema=schema,point_key="a"*64)
        suite.raw_write(Path(M.own_registry_path(f.ctx,name)),M.encoded(entry))
        bad(code,lambda name=name:M.registered_entry(f.ctx,dict(f.call,name=name)))
    broken={"schema":"STEP5_ATTEMPT_RECEIPT_C2V001","call":{"name":f.name},"attempt":1,
            "spec_sha256":f.call["spec"]["sha256"],"theta_sha256":"a"*64}
    suite.raw_write(Path(f.outdir+".attempt_receipt.json"),M.encoded(broken))
    bad("ATTEMPT_RECEIPT_BINDING",lambda:M.history(f.ctx,f.call))
    f=receipt_fixture(suite,"live_monitor_missing_receipt",no_receipt=True)
    f.ctx.system.rows=[{"pid":900001,"ppid":1,"pgid":900001,"command":
                       M.PY+" -I -B "+f.ctx.pins["monitor"]["path"]+" --receipt "+f.outdir+".receipt.json"}]
    bad("ATTEMPT_ACTIVE",lambda:M.history(f.ctx,f.call))
    bad("MONITOR_RECEIPT_MISSING",lambda:M.close_attempt(f.ctx,f.name,1))
    for code, edit in (
            ("MONITOR_CHILD_BINDING",lambda d:d.update(child_pid=999999)),
            ("MONITOR_TOOL_PINS",lambda d:d["pins"]["driver"].update(sha256="a"*64))):
        f=receipt_fixture(suite,"monitor_"+code,receipt_changes=edit)
        bad(code,lambda f=f:M.close_attempt(f.ctx,f.name,1))
    f=receipt_fixture(suite,"bad_sample_binding",sample={"name":"P1_OTHER"})
    bad("SOLO_SAMPLE_BINDING",lambda:M.close_attempt(f.ctx,f.name,1))
    f=receipt_fixture(suite,"duplicate_twin_stop",name=M.TWIN,origin="KIT")
    for label in ("ONE","TWO"):
        suite.raw_write(f.root/"kit_launch_root"/"twin_kill"/("TWIN_KILL_RECORD_"+label+".json"),
                        M.encoded({"outdir":f.outdir,"launch_json":f.launch_pin,"reason":"ITERATION_0001_COMPLETED_AND_SIDECAR"}))
    bad("TWIN_STOP_NOT_UNIQUE",lambda:M.close_attempt(f.ctx,f.name,1))
    f=receipt_fixture(suite,"already_assembled")
    M.close_attempt(f.ctx,f.name,1)
    M.assemble_registry(f.ctx)
    bad("ASSEMBLY_ALREADY_EXISTS",lambda:M.assemble_registry(f.ctx))
    f=receipt_fixture(suite,"cutoff_refusals")
    terms=[{"name":f.name,"time_utc":"2026-10-20T12:00:00Z","receipt":f.entry_pin}]
    bad("TERMINAL_SET_EMPTY",lambda:M.write_cutoff(f.ctx,[]))
    original_dir=f.ctx.cfg["v006_copy_dir"]
    f.ctx.cfg["v006_copy_dir"]=str(f.root/"missing_copy_dir")
    bad("CUTOFF_COPY_DIR",lambda:M.write_cutoff(f.ctx,terms))
    f.ctx.cfg["v006_copy_dir"]=original_dir
    expected=Path(original_dir)/("V006_CUTOFF_COPY_"+M.sha(f.ctx.v006_raw)+".md")
    suite.raw_write(expected,b"SYNTHETIC_BAD_COPY")
    bad("CUTOFF_COPY_EXISTS_DIFFERENT",lambda:M.write_cutoff(f.ctx,terms))
    f=receipt_fixture(suite,"cutoff_readback_fault")
    expected=Path(f.ctx.cfg["v006_copy_dir"])/("V006_CUTOFF_COPY_"+M.sha(f.ctx.v006_raw)+".md")
    read_bytes=Path.read_bytes
    def readback_fault():
        # Simulate corrupted readback of this local synthetic copy only.
        Path.read_bytes=lambda path: b"SYNTHETIC_READBACK_FAULT" if path==expected else read_bytes(path)
        try:
            fail("CUTOFF_COPY_VERIFY",lambda:M.write_cutoff(f.ctx,terms))
        finally:
            Path.read_bytes=read_bytes
        suite.eq(Path(M.cutoff_path(f.ctx)).exists(),False)
    case("REFUSE_CUTOFF_COPY_VERIFY",readback_fault)

    for code in ("MONITOR_REFUSED_RECORD_BINDING","MONITOR_REFUSED_LAUNCHER","MONITOR_REFUSED_WRITER",
                 "MONITOR_REFUSED_PLAN","MONITOR_REFUSED_ABSENT_PATHS","MONITOR_REFUSED_LOG_PIN_FORM","MONITOR_REFUSED_LOG_PATH"):
        f=receipt_fixture(suite,"old_refusal_"+code)
        work=f.root/"launch_root"/"work"/"old_refusal"
        work.mkdir()
        outdir=M.planned_outdir(f.ctx,f.name,2,"P112")
        plan={"outdir":outdir,"attempt":2,"caps":M.first_caps(f.name),"solo_mode":False}
        if code=="MONITOR_REFUSED_PLAN":
            plan["outdir"]="/synthetic/wrong"
        pp=suite.raw_write(work/"plan.json",M.encoded(plan))
        rec={"schema":"MONITOR_REFUSED_ATTEMPT_RECORD_C2V001","name":f.name,"attempt":2,"launcher":"P112_CX2V001",
             "writer":{"name":M.TOOL_NAME,"sha256":suite.tool_sha},"plan":pp,
             "monitor_stdout":suite.raw_write(work/"monitor.stdout.txt",b"synthetic refusal\n"),
             "monitor_stderr":suite.raw_write(work/"monitor.stderr.txt",b""),"absent":M.absent_paths(outdir),
             "date_u":M.date_u(),"rule":"synthetic"}
        if code=="MONITOR_REFUSED_RECORD_BINDING":rec["attempt"]=3
        if code=="MONITOR_REFUSED_LAUNCHER":rec["launcher"]="KIT_C2V003A"
        if code=="MONITOR_REFUSED_WRITER":rec["writer"]={"name":"ROOT","sha256":None}
        if code=="MONITOR_REFUSED_ABSENT_PATHS":rec["absent"]["outdir"]="/synthetic/wrong"
        if code=="MONITOR_REFUSED_LOG_PIN_FORM":rec["monitor_stdout"]={}
        if code=="MONITOR_REFUSED_LOG_PATH":rec["monitor_stdout"]=pp
        suite.raw_write(f.root/"launch_root"/"launches"/("P112_"+f.name+"_MONITOR_REFUSED_CX2V001_A2.json"),M.encoded(rec))
        bad(code,lambda f=f:M.refusal_records(f.ctx,f.name,f.ctx.records(f.name)))

    for code in ("PLAN_SCHEMA","PLAN_CONFIG_BINDING","PLAN_OUTDIR_BINDING","MONITOR_REFUSED_WORK","MONITOR_STILL_ALIVE"):
        f=receipt_fixture(suite,"refusal_plan_"+code)
        work=f.root/"launch_root"/"work"/"invocation"
        work.mkdir()
        outdir=M.planned_outdir(f.ctx,f.name,2,"P112")
        plan={"schema":"UNT_P112_LAUNCH_PLAN_CX2V001","name":f.name,"attempt":2,"outdir":outdir,
              "config":f.ctx.config_pin,"caps":M.first_caps(f.name)}
        if code=="PLAN_SCHEMA":plan["schema"]="WRONG"
        if code=="PLAN_CONFIG_BINDING":plan["config"]={}
        if code=="PLAN_OUTDIR_BINDING":plan["outdir"]="/synthetic/wrong"
        if code=="MONITOR_STILL_ALIVE":
            f.ctx.system.rows=[{"pid":900001,"ppid":1,"pgid":900001,"command":
                               M.PY+" -I -B "+f.ctx.pins["monitor"]["path"]+" --receipt "+outdir+".receipt.json"}]
        pp=suite.raw_write(work/"plan.json",M.encoded(plan))
        workarg=str(f.root) if code=="MONITOR_REFUSED_WORK" else str(work)
        bad(code,lambda f=f,pp=pp,workarg=workarg:M.record_monitor_refused(f.ctx,pp,workarg))
    f=receipt_fixture(suite,"outside_refusals",origin="KIT",name="S0_J0_SERIAL")
    f.ctx._fixture_calls=[]
    bad("OUTSIDE_STOP_NAME",lambda:M.stop_outside_set(f.ctx,"P1_M0001"))
    bad("OUTSIDE_STOP_NO_RECORD",lambda:M.stop_outside_set(f.ctx,"S0_J2_SERIAL"))
    bad("OUTSIDE_STOP_ATTEMPT",lambda:M.stop_outside_set(f.ctx,f.name,99))
    bad("OUTSIDE_SET_STOP_REQUIRED",lambda:M.assemble_registry(f.ctx))
    f.ctx.get_vpin=lambda kind,name:{"path":f.call["spec"]["path"],"sha256":"a"*64}
    bad("OUTSIDE_STOP_SPEC_PIN",lambda:M.stop_outside_set(f.ctx,f.name))
    for code in ("OUTSIDE_STOP_SCHEMA","OUTSIDE_STOP_MAPPING_PINS"):
        g=receipt_fixture(suite,"outside_record_"+code,origin="KIT",name="S0_J0_SERIAL")
        record={"schema":"WRONG" if code=="OUTSIDE_STOP_SCHEMA" else "S0_OUTSIDE_SET_STOP_RECORD_C2V001",
                "name":g.name,"plan_output_primary":{},"fdplan":g.ctx.cfg["fdplan"]}
        suite.raw_write(g.root/"launch_root"/"outside_set_stop"/(g.name+"_A1_CX2V001.json"),M.encoded(record))
        bad(code,lambda g=g:M.outside_stop_records(g.ctx,g.name))
    jp=suite.fixture("malformed_launch_json_shape.json",[])
    case("REFUSE_LAUNCH_JSON_FORM",lambda:suite.eq(M.try_launch_json(jp["path"]),(None,None)))

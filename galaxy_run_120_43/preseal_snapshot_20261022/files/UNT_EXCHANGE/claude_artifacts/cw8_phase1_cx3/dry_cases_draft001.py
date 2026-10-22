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

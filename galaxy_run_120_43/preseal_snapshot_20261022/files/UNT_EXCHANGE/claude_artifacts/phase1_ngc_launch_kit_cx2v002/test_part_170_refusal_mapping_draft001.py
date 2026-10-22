"""Refuse invalid PLAN, mapping, certificate and fixed-point custody inputs."""


def refusal_mapping_cases(suite):
    import copy
    from pathlib import Path
    M, case, fail = suite.module, suite.case, suite.refuses
    f = full_launch_fixture(suite, "mapping_refusals")
    system_doc = M.read_pin(f.synthetic)["system"]
    def context():
        return M.Context(f.config, system=M.SyntheticSystem(system_doc), synthetic_pins=f.overrides)
    def bad(code, change, action=None):
        c = context()
        change(c)
        case("REFUSE_"+code,lambda:fail(code,lambda:action(c) if action else c.calls()))
    def changed(c, field, code, edit):
        doc=M.read_pin(c.cfg[field])
        edit(doc)
        c.cfg[field]=suite.fixture("mapping_"+code+".json",doc)
        if code in ("F_IDENTITY", "F_POINT_KEY"):
            cfg=c.cfg["f_points"][0]
            hand=M.read_pin(cfg["handoff"])
            hand["source_pin"]=c.cfg[field]
            cfg["handoff"]=suite.fixture("mapping_f_handoff_"+code+".json",hand)
    tests = (
        ("AT0A_NOT_PASS","at0a_pass",lambda d:d.update(outcome="FAIL")),
        ("PLAN_BUILD_RECORD","plan_build_record",lambda d:d.update(stage="ASSEMBLE")),
        ("PLAN_NOT_BUDGET_ZERO","plan_output_primary",lambda d:d.update(budget=1)),
        ("PLAN_NOT_VALUE_FREE","plan_output_primary",lambda d:d["members"][0].update(evaluated=True)),
        ("MEMBER_COUNT","plan_output_primary",lambda d:d["members"].append(copy.deepcopy(d["members"][0]))),
        ("FDPLAN_SCHEMA","fdplan",lambda d:d.update(schema="WRONG")),
        ("SELECTION_MEMBERS","selection",lambda d:d.update(points=[])),
        ("SELECTION_IDENTITY","selection",lambda d:d["points"][0].update(role="wrong")),
        ("MEMBER_ORDER","plan_output_primary",lambda d:d["members"][0].update(order=1)),
        ("FDPLAN_MEMBER_IDENTITY","fdplan",lambda d:d["members"][0].update(log_index=2)),
        ("FDPLAN_MEMBER_ORDER","fdplan",lambda d:d["members"][0].update(order=1)),
        ("FDPLAN_POINT_KEY","fdplan",lambda d:d["members"][0].update(key="a"*64)),
        ("FDPLAN_THETA_KEY_SET","fdplan",lambda d:d["members"][0]["theta_hex"].pop("ell_F_m")),
        ("PLAN_NUISANCE_FIELD","plan_output_primary",lambda d:d["members"][0]["theta_ngc"].pop("ngc3198_distance_Mpc")),
        ("PLAN_THETA_NGC_EXACT_FLOAT","plan_output_primary",lambda d:d["members"][0]["theta_ngc"].update(untyped_extra=1)),
        ("F_COUNT","fdplan",lambda d:d["F"].pop()),
        ("F_IDENTITY","fdplan",lambda d:d["F"][0].update(role="F1")),
        ("F_POINT_KEY","fdplan",lambda d:d["F"][0].update(key="a"*64)),
    )
    for code,field,edit in tests:
        bad(code,lambda c,code=code,field=field,edit=edit:changed(c,field,code,edit))
    bad("SPEC_OF_RECORD",lambda c:c.cfg.update(spec_of_record={"path":"/synthetic/spec.json","sha256":"a"*64}))
    bad("F_LABELS",lambda c:c.cfg["f_points"][0].update(label="F2"))
    def change_hand(c,code,edit,member=True):
        cfg=c.cfg["members"][0] if member else c.cfg["f_points"][0]
        hand=M.read_pin(cfg["handoff"])
        edit(hand)
        cfg["handoff"]=suite.fixture("handoff_"+code+".json",hand)
    bad("HANDOFF_MEMBER_IDENTITY",lambda c:change_hand(c,"identity",lambda d:d.update(log_index=2)))
    def export_change(c):
        cfg=c.cfg["members"][0]
        hand=M.read_pin(cfg["handoff"])
        export=M.read_pin(hand["source_export_pin"])
        export["admitted_points"]=[]
        hand["source_export_pin"]=suite.fixture("missing_member_export.json",export)
        cfg["handoff"]=suite.fixture("missing_export_handoff.json",hand)
    bad("EXPORT_MEMBER_NOT_UNIQUE",export_change)
    bad("F_SOURCE_FDPLAN",lambda c:change_hand(c,"f_source",lambda d:d.update(source_pin={}),False))
    def cert_change(c):
        c.cfg["members"][0]["eps"]=suite.fixture("wrong_point_certificate.json",{"point":{"key":"a"*64}})
    bad("CERTIFICATE_POINT_KEY",cert_change)
    bad("HANDOFF_V006_PIN",lambda c:c.vpins["HANDOFF_PIN"]["P1_M0001"].update(sha256="a"*64))
    bad("SPEC_V006_PIN",lambda c:c.vpins["SPEC_PIN"]["P1_M0001"].update(sha256="a"*64))
    def kit_override(c,kind):
        kit=c.kit_entries()
        if kind=="missing_seed":
            kit.pop("S0_SEED_SERIAL")
        elif kind=="missing_twin":
            kit.pop(M.TWIN)
        elif kind=="wrong_twin":
            e,p=kit[M.TWIN]
            kit[M.TWIN]=(dict(e,theta_key="a"*64),p)
        else:
            spec,sp,fill,fp=c.read_fill(c.cfg["members"][0])
            key=M.read_pin(c.cfg["fdplan"])["members"][0]["key"]
            if kind=="physical_keys":
                spec["physical"]["additional"]=1.0
                sp=suite.fixture("kit_extra_physical.json",spec)
            entry={"schema":"UNT_S0_LAUNCH_REGISTRY_ENTRY_C2V003A","name":"S0_J0_SERIAL","theta_key":key,
                   "spec":sp,"v006_handoff_pin":c.cfg["members"][0]["handoff"]}
            ep=suite.fixture("kit_override_"+kind+".json",entry)
            kit["S0_J0_SERIAL"]=(entry,ep)
            c.vpins["SPEC_PIN"]["S0_J0_SERIAL"]=dict(sp)
            if kind=="duplicate":
                kit["S0_J1_SERIAL"]=(dict(entry,name="S0_J1_SERIAL"),ep)
            if kind=="vpin":
                c.vpins["SPEC_PIN"]["S0_J0_SERIAL"]["sha256"]="a"*64
        c.kit_entries=lambda:kit
    for code,kind in (("SEED_REGISTRY_MISSING","missing_seed"),("TWIN_REGISTRY_MISSING","missing_twin"),
                      ("TWIN_REGISTRY_BINDING","wrong_twin"),("KIT_PHYSICAL_KEYS","physical_keys"),
                      ("KIT_POINT_DUPLICATE","duplicate"),("KIT_SPEC_V006","vpin")):
        bad(code,lambda c,kind=kind:kit_override(c,kind))
    bad("TWIN_SPEC_V006",lambda c:c.vpins["SPEC_PIN"][M.TWIN].update(sha256="a"*64))
    def duplicate_member(c):
        changed(c,"plan_output_primary","duplicate_plan",lambda d:d["members"].append(copy.deepcopy(d["members"][0])))
        changed(c,"fdplan","duplicate_fd",lambda d:d["members"].append(copy.deepcopy(d["members"][0])))
        changed(c,"selection","duplicate_sel",lambda d:d["points"].append(copy.deepcopy(d["points"][0])))
        other=copy.deepcopy(c.cfg["members"][0])
        other["order"]=1
        c.cfg["members"].append(other)
    bad("DUPLICATE_MEMBER_POINT",duplicate_member)
    def missing_kit_schema(c):
        root=f.root/"bad_kit_root"
        (root/"registry").mkdir(parents=True)
        suite.raw_write(root/"registry"/"S0_SEED_SERIAL_C2V003A.json",M.encoded({"schema":"WRONG"}))
        c.cfg["s0"]["launch_root"]=str(root)
    bad("KIT_REGISTRY_SCHEMA",missing_kit_schema,lambda c:c.kit_entries())
    def missing_m15(c):
        root=f.root/"bad_m15_root"
        root.mkdir()
        suite.raw_write(root/"M15_PRELAUNCH_RECORD_C2V001.json",M.encoded({"schema":"WRONG"}))
        c.cfg["s0"]["launch_root"]=str(root)
    bad("M15_SCHEMA",missing_m15,lambda c:c.seed_check())

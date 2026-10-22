"""Build-only step-4 admission. No import-time I/O or processes.
Root publishes the exact admission bytes independently; an environment hash is a
custody anchor, not a cryptographic identity. Native preflight is always repeated.
"""
import ast, contextlib, hashlib, importlib.util, json, math, os, re, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
PACKET=HERE.parent
AUTHORITY={'identity':'Claude2','role':'coordinator_and_single_scientific_launch_owner'}
R5_SHA='b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6'
REF_SHA='237ef3d41daf4d99b0aafed3e90b27b095a741a9f66ea06ea34f3e44876d47bb'
MONITOR_SHA='ba031c2340057d88ee399138cc645012a93aa7dc3eb7c9bba56d112c94a47107'
FENCE=False
FENCE_INSTALLED=False
class Refusal(ValueError):pass
def require(value,code):
    if value is not True:raise Refusal(code)
def safe_path(value):
    require(isinstance(value,str) and Path(value).is_absolute(),'ABSOLUTE_PATH_REQUIRED')
    p=Path(value);r=p.resolve()
    parts={x.casefold() for x in p.parts}|{x.casefold() for x in r.parts}
    require(not any(x.startswith('uvt_') or x=='kmax_a2f10_c5h_run_v001' or 'ngc3198' in x for x in parts),'PROTECTED_PATH_REFUSED')
    return r
def raw(path):return safe_path(str(path)).read_bytes()
def sha(path):return hashlib.sha256(raw(path)).hexdigest()
def pin(path):return {'path':str(safe_path(str(path))),'sha256':sha(path)}
def verify(ref):
    require(isinstance(ref,dict) and set(ref)=={'path','sha256'},'PIN_REQUIRED')
    require(isinstance(ref['sha256'],str) and re.fullmatch('[0-9a-f]{64}',ref['sha256']) is not None,'SHA256_REQUIRED')
    data=raw(ref['path']);require(hashlib.sha256(data).hexdigest()==ref['sha256'],'PIN_BYTES_CHANGED')
    return data
def _pairs(items):
    d={}
    for k,v in items:
        if k in d:raise Refusal('DUPLICATE_JSON_KEY')
        d[k]=v
    return d
def decode(data):
    return json.loads(data,object_pairs_hook=_pairs,parse_constant=lambda s:(_ for _ in ()).throw(Refusal('NONFINITE_JSON')))
def doc(ref):
    d=decode(verify(ref));require(isinstance(d,dict),'OBJECT_REQUIRED');return d
def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def digest(value):return hashlib.sha256(canonical(value)).hexdigest()
def source_map(cfg):
    refs=cfg.get('sources');require(isinstance(refs,dict) and bool(refs),'SOURCES_REQUIRED')
    for path,h in refs.items():verify({'path':path,'sha256':h})
    return refs
def admitted_source(ref,cfg):
    verify(ref);require(cfg['sources'].get(ref['path'])==ref['sha256'],'SOURCE_NOT_ALLOWLISTED')
def check_review(cfg):
    r=doc(cfg['source_review'])
    require(r.get('schema')=='UNT_STEP4_SOURCE_REVIEW_CX1V001' and r.get('status')=='TESTED' and r.get('verdict')=='PASS','SOURCE_REVIEW_REQUIRED')
    require(r.get('approved_sources')==cfg['sources'] and r.get('blocking_findings')==[],'SOURCE_REVIEW_BINDING')
    require(isinstance(r.get('reviewer'),str) and r['reviewer'] not in ('','Codex1'),'DISTINCT_REVIEW_REQUIRED')
def _audit(event,args):
    if not FENCE:return
    if event in ('subprocess.Popen','os.system','os.fork','os.forkpty','os.posix_spawn','os.exec','socket.connect','socket.bind'):
        raise Refusal('PREFLIGHT_PROCESS_OR_NETWORK_REFUSED')
    if event in ('os.mkdir','os.remove','os.rmdir','os.rename','os.link','os.symlink','os.truncate'):
        raise Refusal('PREFLIGHT_WRITE_REFUSED')
    if event=='open':
        p,mode,flags=args
        if isinstance(p,(str,bytes,os.PathLike)):
            safe_path(os.path.abspath(os.fsdecode(p)))
        if (isinstance(mode,str) and any(c in mode for c in 'wax+')) or (isinstance(flags,int) and flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)):
            raise Refusal('PREFLIGHT_WRITE_REFUSED')
@contextlib.contextmanager
def fence():
    global FENCE,FENCE_INSTALLED
    if not FENCE_INSTALLED:sys.addaudithook(_audit);FENCE_INSTALLED=True
    before=FENCE;FENCE=True
    try:yield
    finally:FENCE=before
def load(ref,cfg,name):
    admitted_source(ref,cfg)
    sp=importlib.util.spec_from_file_location(name,ref['path']);m=importlib.util.module_from_spec(sp)
    sys.modules[name]=m
    exec(compile(verify(ref),ref['path'],'exec'),m.__dict__)
    return m
def positive_gate(g,reason_field='reasons'):
    require(isinstance(g,dict) and g.get('ok') is True and g.get(reason_field)==[],'NATIVE_GATE_REFUSED')
def adoption(cfg,context_module):
    v=cfg['v007']
    for k in ('seal','verdict','prereg','compare','addendum','case_block'):verify(v[k])
    seal=doc(v['seal']);report=doc(v['verdict']);pre=doc(v['prereg'])
    require(seal.get('sealed_by')==AUTHORITY and seal.get('prereg')==v['prereg'] and seal.get('compare')==v['compare'],'SEALED_ROOT_BINDING')
    require(seal.get('driver',{}).get('sha256')==R5_SHA and seal.get('frozen_addendum')==v['addendum'],'SEALED_R5_BINDING')
    require(report.get('test_mode') is False and report.get('decision',{}).get('tests_read') is True and report['decision'].get('outcome')=='ADOPT_TAIL','SEALED_ADOPT_TAIL_REQUIRED')
    require(report.get('script_sha256')==v['compare']['sha256'] and report.get('prereg')==v['prereg'] and report.get('case_block')==v['case_block'],'VERDICT_BYTE_BINDING')
    require(pre.get('binding_inputs',{}).get('case_block')==v['case_block'],'PREREG_CASE_BLOCK_REQUIRED')
    policy=load(cfg['adoption_policy'],cfg,'_step4_adoption_policy')
    key=(v['compare']['sha256'],v['prereg']['sha256'],v['addendum']['sha256'],report.get('schema'),v['verdict']['sha256'])
    require(key in policy.APPROVED_V007_SEALS,'REVIEWED_SEAL_TUPLE_PENDING')
    C=context_module;config=doc(cfg['config']);ncfg=config['numerics']
    require(ncfg.get('verdict_artifact')==v['verdict'] and ncfg.get('sealed_prereg')==v['prereg'] and ncfg.get('compare')==v['compare'],'C1_ADOPTION_BINDING')
    # V007 adopted worker count; the fresh step-4 deciding repeat is not presumed completed.
    n=ncfg['block']['route_a']['column_workers']
    require(type(n) is int and n>0,'ADOPTED_WORKER_COUNT_REQUIRED')
    _,g=policy.check_numerics(ncfg,ncfg['block'],n,O=C.O,validate_block=C.validate_block,driver_sha=R5_SHA,synthetic=False)
    positive_gate(g)
    return config,g

def native_preflight(cfg,call):
    """Actual native policy/certificate/sensitivity calls, not acceptance of a PASS string."""
    spec=doc(call['spec'])
    with fence():
        C=load(cfg['context_module'],cfg,'_step4_context')
        config,ag=adoption(cfg,C)
        tail=spec.get('numerics',{}).get('uv_tail',{}).get('enabled')
        require(spec.get('galaxy')=='DDO154' and spec.get('admit')=={},'FRESH_DDO154_SPEC_REQUIRED')
        require(type(call['tail_on']) is bool,'TAIL_MODE_REQUIRED')
        # Drivers use uv_tail.mode rather than a separate enabled boolean.
        mode=spec.get('numerics',{}).get('uv_tail',{}).get('mode')
        if call['tail_on']:
            require(mode not in (None,'off') and tail is not False,'TAIL_ON_SPEC_REQUIRED')
            require(call['driver']['sha256']==R5_SHA,'TAIL_ON_R5_REQUIRED')
            readiness=config.get('tail_readiness',{})
            for key in ('certificate_registry','certificate_policy_review','custody_deriver','state_enumerator'):
                verify(readiness.get(key))
            producers=readiness.get('approved_certificate_producers')
            require(isinstance(producers,list) and len(producers)>0,'CERTIFICATE_PRODUCERS_REQUIRED')
            for ref in producers:admitted_source(ref,cfg)
            admitted_source(readiness['custody_deriver'],cfg);admitted_source(readiness['state_enumerator'],cfg)
            ctx=C.Context(config)
            pg=ctx.certificate_policy_gate();positive_gate(pg)
            cg=ctx.certificate_check(spec,'prelaunch');positive_gate(cg,'blockers')
            sg=ctx.sensitivity_gate(spec);positive_gate(sg)
            normalized=ctx.prelaunch_check(spec)
            checks={'certificate_policy':pg,'certificate_prelaunch':cg,'sensitivity':sg,'normalized_sha256':digest(normalized)}
        else:
            require(call.get('family')=='DECIDING_III' and mode in (None,'off') and tail is not True,'ONLY_DIII_TAIL_OFF_ALLOWED')
            policy=doc(cfg['tail_off_policy'])
            require(policy.get('schema')=='UNT_STEP4_DIII_POLICY_CX1V001' and policy.get('authority')==AUTHORITY and policy.get('post_adoption_only') is True,'DIII_POLICY_REQUIRED')
            require(policy.get('verdict')=='PASS' and policy.get('status')=='TESTED' and policy.get('cases',{}).get(call['case'])=={'spec':call['spec'],'driver':call['driver']},'DIII_REVIEW_BINDING')
            drv=load(call['driver'],cfg,'_step4_diii_driver')
            normalized=drv.normalize_spec(spec)
            checks={'certificate_policy':'NOT_APPLICABLE_REVIEWED_TAIL_OFF_IDENTITY','certificate_prelaunch':'NOT_APPLICABLE_REVIEWED_TAIL_OFF_IDENTITY','sensitivity':'DECIDING_III_EVIDENCE_GENERATION_ONLY','normalized_sha256':digest(normalized),'tail_off_policy':cfg['tail_off_policy']}
    return {'schema':'UNT_STEP4_PRELAUNCH_CX1V001','case':call['case'],'spec':call['spec'],'driver':call['driver'],'config':cfg['config'],'adoption_verdict':cfg['v007']['verdict'],'checks':checks,'adoption_checked':True}

def validate(plan_ref,producer,*,check_outputs=True,execute_native=True,config_ref=None):
    """No process creation; validation precedes worker, sleep assertion and every monitor."""
    if config_ref is None:
        p=os.environ.get('UNT_STEP4_ADMISSION_PATH','');h=os.environ.get('UNT_STEP4_ADMISSION_SHA256','')
        require(bool(p) and bool(h),'PUBLISHED_STEP4_ADMISSION_PENDING');config_ref={'path':p,'sha256':h}
    cfg=doc(config_ref)
    require(cfg.get('schema')=='UNT_STEP4_ADMISSION_CX1V001' and cfg.get('authority')==AUTHORITY,'ROOT_STEP4_AUTHORITY_REQUIRED')
    require(cfg.get('status')=='ROOT_AUTHORIZED' and cfg.get('plan')==plan_ref,'ROOT_PLAN_BINDING_REQUIRED')
    plan=doc(plan_ref)
    require(plan.get('schema')=='UNT_STEP4_LAUNCH_PLAN_CX1V001' and plan.get('binding_status')=='ROOT_BOUND','UNBOUND_PLAN_REFUSED')
    source_map(cfg);check_review(cfg)
    for k in ('launcher','guard','monitor'):
        admitted_source(plan[k],cfg)
    require(plan['guard']==pin(__file__) and plan['launcher']==pin(producer),'LAUNCHER_GUARD_IDENTITY')
    require(plan['monitor']['sha256']==MONITOR_SHA,'FIXED_REVIEWED_MONITOR_REQUIRED')
    rule=plan.get('route_a_admission',{})
    require(type(rule.get('max_active')) is int and 1<=rule['max_active']<=6,'ROUTE_A_CAP_REQUIRED')
    require(rule==cfg.get('route_a_admission'),'ROOT_RAMP_APPROVAL_REQUIRED')
    require(rule.get('minimum_free_percent')==25 and rule.get('poll_seconds')==60 and rule.get('source')=='/usr/bin/memory_pressure' and rule.get('ramp')=='previous_first_completed_route_a_iteration','RAMP_RULE_REQUIRED')
    require(rule.get('first_case_memory_exemption') is False,'FIRST_MEMORY_BYPASS_REFUSED')
    require(cfg.get('core_priority')=={'normal_qos_required':True,'step2_route_a_inactive':True,'campaign_inactive':True,'background_noncritical_lanes':True,'sleep_assertion_required':True},'CORE_PRIORITY_ATTESTATION_REQUIRED')
    require(plan.get('batch') in ('HEADLINE','DIII','SENS_LO','SENS_HI','POST_S1'),'BATCH_REQUIRED')
    calls=plan.get('calls');require(isinstance(calls,list) and len(calls)>0,'NONEMPTY_CALLS_REQUIRED')
    require(len({c['case'] for c in calls})==len(calls),'DUPLICATE_CASE')
    require(cfg.get('case_order')==[c['case'] for c in calls],'ROOT_ORDER_BINDING')
    outputs=[]
    for call in calls:
        require(call.get('spec_status')=='ROOT_FINAL' and call.get('pending')==[],'PENDING_SPEC_REFUSED')
        require(call['driver']['sha256'] in (R5_SHA,REF_SHA),'EXACT_R5_OR_DIII_REFERENCE_DRIVER_REQUIRED')
        if call['driver']['sha256']==REF_SHA:require(call.get('family')=='DECIDING_III' and call.get('driver_role')=='REFERENCE_V009_GEO' and call['tail_on'] is False,'REFERENCE_DRIVER_SCOPE')
        admitted_source(call['driver'],cfg);verify(call['spec'])
        spec=doc(call['spec']);require(spec.get('physical',{}).get('distance_Mpc')==call.get('distance_Mpc'),'DISTANCE_BINDING')
        caps={k:call.get(k) for k in ('wall_cap_s','rss_cap_bytes','output_cap_bytes')}
        require(all(type(v) is int and v>0 for v in caps.values()),'POSITIVE_INTEGER_CAPS_REQUIRED')
        require(cfg.get('caps',{}).get(call['case'])==caps,'ROOT_CAPS_BINDING')
        approved=cfg.get('calls',{}).get(call['case'])
        require(approved=={'spec':call['spec'],'driver':call['driver'],'prelaunch':call.get('prelaunch')},'ROOT_CALL_BINDING')
        if execute_native:
            require(doc(call['prelaunch'])==native_preflight(cfg,call),'PRELAUNCH_REPLAY_MISMATCH')
        for k in ('outdir','receipt','monitor_log'):outputs.append(safe_path(call[k]))
        outputs.append(safe_path(call['receipt']+'.launch.json'))
    outputs.append(safe_path(plan['launcher_log']))
    require(len(set(outputs))==len(outputs),'ALIASED_OUTPUTS')
    for i,p in enumerate(outputs):
        for q in outputs[i+1:]:require(not p.is_relative_to(q) and not q.is_relative_to(p),'NESTED_OUTPUTS')
    if check_outputs:
        for p in outputs:require(not os.path.lexists(p),'EXISTING_OUTPUT')
    return plan,cfg

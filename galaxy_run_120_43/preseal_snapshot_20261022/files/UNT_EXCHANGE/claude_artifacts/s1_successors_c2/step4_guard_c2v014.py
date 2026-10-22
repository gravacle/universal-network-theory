"""Build-only step-4 admission. No import-time I/O or processes.
Root publishes the exact admission bytes independently; an environment hash is a
custody anchor, not a cryptographic identity. Native preflight is always repeated.

c2v014 = guard013 (593bebb6) with one change (V006 A172, the step-4 packet A166 set): the route-A admission rule
binds only its non-memory fields. route_a_admission keeps max_active (integer 1..6), poll_seconds 60 (the launcher's
one-start-per-poll cadence, launcher L140) and the first-iteration ramp, and root's copy must still equal the plan's.
guard013's memory fields (minimum_free_percent 25, source /usr/bin/memory_pressure, first_case_memory_exemption
false) are no longer required, and a rule that still carries any of them is refused (MEMORY_ADMISSION_FIELD_REFUSED):
launcher015 enforces no memory term, so a plan of record must not state one. Every custody check, core_priority_admission
included, is guard013's, unchanged.
"""
import ast, contextlib, hashlib, importlib.util, importlib.machinery, json, math, os, re, stat, sys, types, threading
from pathlib import Path
HERE=Path(__file__).resolve().parent
PACKET=HERE.parent
AUTHORITY={'identity':'Claude2','role':'coordinator_and_single_scientific_launch_owner'}
R5_SHA='b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6'
REF_SHA='237ef3d41daf4d99b0aafed3e90b27b095a741a9f66ea06ea34f3e44876d47bb'
MONITOR_SHA='ba031c2340057d88ee399138cc645012a93aa7dc3eb7c9bba56d112c94a47107'
FENCE=False
FENCE_INSTALLED=False
FENCE_SOURCES={}
# Exact generated buffer in the independently pinned v006r9 native wrapper.
# This is not an allowance for arbitrary code generation. A changed owner or
# generated buffer needs a reviewed immutable successor to this contract.
GENERATED_COMPILE_CONTRACT={
    '7a6af535805399d49ec3f1c1cbe9e4911d98f6fae0ad50b69a0641214fcd5d4d':frozenset({
        '79e8936d96103b1540987a980b289b6d25e5e25941b02db647f7a833818da0e1'})}
# 0674/Q7: read-only exception for this source, never a UVT run tree.
R1_SOURCE='/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/route_b/uvt_route_b_binding_c2v001_r5.py'
R1_SHA='1e27430c12cc84195b7642fe925bc6f9916a55158ecc02c9fbff9b8564506329'
R1_CHECK=threading.local()
def r1_verified_read():
    # Reject every symlink component before opening the exact source. The audit
    # recursion exemption is thread-local and only for this read-only hash read.
    p=Path(R1_SOURCE)
    for q in reversed((p,*p.parents)):
        require(not stat.S_ISLNK(os.lstat(q).st_mode),'R1_SYMLINK_REFUSED')
    R1_CHECK.active=True
    try:
        fd=os.open(R1_SOURCE,os.O_RDONLY|os.O_NOFOLLOW)
        try:
            require(stat.S_ISREG(os.fstat(fd).st_mode),'R1_REGULAR_SOURCE_REQUIRED')
            chunks=[]
            while True:
                chunk=os.read(fd,1048576)
                if not chunk:break
                chunks.append(chunk)
            data=b''.join(chunks)
        finally:os.close(fd)
    finally:R1_CHECK.active=False
    require(hashlib.sha256(data).hexdigest()==R1_SHA,'R1_SOURCE_BYTES_CHANGED')
    return data
class Refusal(ValueError):pass
def require(value,code):
    if value is not True:raise Refusal(code)
def lexical_path(value):
    require(isinstance(value,str) and Path(value).is_absolute(),'ABSOLUTE_PATH_REQUIRED')
    p=Path(value)
    if value==R1_SOURCE:
        r1_verified_read()
        return p
    metadata=re.fullmatch(r'ROOT_DECISIONS_NGC3198_CONSTRUCTION_[A-Za-z0-9_-]+\.md',p.name) is not None
    require(not any(x.casefold().startswith('uvt_') or x.casefold()=='kmax_a2f10_c5h_run_v001' or ('ngc3198' in x.casefold() and not (metadata and x==p.name)) for x in p.parts),'PROTECTED_PATH_REFUSED')
    return p

def safe_path(value):
    # No resolve/stat/readlink precedes the lexical refusal. Resolve one component
    # at a time so a symlink's protected target is refused before probing it.
    p=lexical_path(value);todo=list(p.parts[1:]);current=Path('/');links=0
    while todo:
        part=todo.pop(0)
        if part in ('','.'):
            continue
        if part=='..':current=current.parent;continue
        candidate=lexical_path(str(current/part))
        try:info=os.lstat(candidate)
        except (FileNotFoundError,NotADirectoryError):current=candidate;continue
        if stat.S_ISLNK(info.st_mode):
            links+=1;require(links<=40,'SYMLINK_LOOP_REFUSED')
            target=os.readlink(candidate)
            target_path=Path(target) if os.path.isabs(target) else current/target
            lexical_path(str(target_path))
            if os.path.isabs(target):current=Path('/');parts=list(Path(target).parts[1:])
            else:parts=list(Path(target).parts)
            todo=parts+todo
        else:current=candidate
    require(str(current)!=R1_SOURCE or value==R1_SOURCE,'R1_EXACT_PATH_REQUIRED')
    return lexical_path(str(current))
def raw(path):
    if str(path)==R1_SOURCE:return r1_verified_read()
    return safe_path(str(path)).read_bytes()
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
def _finite_float(s):
    v=float(s);require(math.isfinite(v),'NONFINITE_JSON');return v
def decode(data):
    return json.loads(data,object_pairs_hook=_pairs,parse_float=_finite_float,parse_constant=lambda s:(_ for _ in ()).throw(Refusal('NONFINITE_JSON')))
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
def _managed_source(path):
    return str(path) in FENCE_SOURCES or ('/Research/' in str(path) and path.suffix=='.py')
def _registered_cache(path):
    if path.suffix!='.pyc':return False
    try:source=importlib.util.source_from_cache(str(path))
    except ValueError:source=str(path.with_suffix('.py'))
    return str(safe_path(source)) in FENCE_SOURCES

def _audit(event,args):
    if not FENCE:return
    if event in ('subprocess.Popen','os.system','os.fork','os.forkpty','os.posix_spawn','os.exec','socket.connect','socket.bind'):
        raise Refusal('PREFLIGHT_PROCESS_OR_NETWORK_REFUSED')
    if event in ('os.mkdir','os.remove','os.rmdir','os.rename','os.link','os.symlink','os.truncate'):
        raise Refusal('PREFLIGHT_WRITE_REFUSED')
    if event=='compile':
        source,filename=args
        require(filename!=R1_SOURCE,'R1_READ_ONLY_SOURCE')
        if isinstance(filename,str) and os.path.isabs(filename):
            resolved=safe_path(filename)
            if _managed_source(resolved):
                require(isinstance(source,(bytes,str)),'PREFLIGHT_SOURCE_BUFFER_REQUIRED')
                data=source.encode('utf-8') if isinstance(source,str) else source
                actual=hashlib.sha256(data).hexdigest();owner=FENCE_SOURCES.get(str(resolved))
                if actual!=owner:
                    require(actual in GENERATED_COMPILE_CONTRACT.get(owner,()),'PREFLIGHT_COMPILE_HASH_MISMATCH')
                    # Generated code is bound to both exact owner bytes and the
                    # exact reviewed literal buffer; repeat custody at use time.
                    verify({'path':str(resolved),'sha256':owner})
    if event=='open':
        p,mode,flags=args
        writing=(isinstance(mode,str) and any(c in mode for c in 'wax+')) or (isinstance(flags,int) and flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND))
        if writing:raise Refusal('PREFLIGHT_WRITE_REFUSED')
        if getattr(R1_CHECK,'active',False):
            require(p==R1_SOURCE and not writing,'R1_HASH_READ_ONLY')
            return
        if isinstance(p,(str,bytes,os.PathLike)):
            requested=os.path.abspath(os.fsdecode(p))
            if requested==R1_SOURCE:
                require(FENCE_SOURCES.get(R1_SOURCE)==R1_SHA,'R1_REVIEWED_SOURCE_REQUIRED')
            resolved=safe_path(requested)
            if _registered_cache(resolved):raise Refusal('UNPINNED_PREFLIGHT_SOURCE')
            if resolved.suffix in ('.py','.pyc') and '/Research/' in str(resolved):
                require(str(resolved) in FENCE_SOURCES and resolved.suffix=='.py','UNPINNED_PREFLIGHT_SOURCE')
        if (isinstance(mode,str) and any(c in mode for c in 'wax+')) or (isinstance(flags,int) and flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)):
            raise Refusal('PREFLIGHT_WRITE_REFUSED')
@contextlib.contextmanager
def fence(sources=None):
    global FENCE,FENCE_INSTALLED,FENCE_SOURCES
    if not FENCE_INSTALLED:sys.addaudithook(_audit);FENCE_INSTALLED=True
    canonical_sources={}
    for path,h in (sources or {}).items():
        canonical=str(safe_path(path))
        require(canonical not in canonical_sources or canonical_sources[canonical]==h,'ALIASED_SOURCE_HASH_CONFLICT')
        canonical_sources[canonical]=h
    before=FENCE;old_sources=FENCE_SOURCES;FENCE=True;FENCE_SOURCES=canonical_sources
    original=importlib.machinery.SourceFileLoader.get_code
    def exact_code(loader,fullname):
        resolved=safe_path(os.path.abspath(loader.path))
        if _managed_source(resolved):
            require(str(resolved) in FENCE_SOURCES,'UNPINNED_PREFLIGHT_SOURCE')
            data=verify({'path':str(resolved),'sha256':FENCE_SOURCES[str(resolved)]})
            return compile(data,str(resolved),'exec')
        return original(loader,fullname)
    importlib.machinery.SourceFileLoader.get_code=exact_code
    try:yield
    finally:
        importlib.machinery.SourceFileLoader.get_code=original
        FENCE=before;FENCE_SOURCES=old_sources
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

def spec_structure(call,spec):
    require(spec.get('galaxy')=='DDO154' and spec.get('admit')=={},'FRESH_DDO154_SPEC_REQUIRED')
    require(type(call.get('tail_on')) is bool,'TAIL_MODE_REQUIRED')
    if call['tail_on']:
        require(spec.get('numerics',{}).get('uv_tail',{}).get('enabled') is True,'TAIL_ON_SPEC_REQUIRED')
        require(call.get('driver',{}).get('sha256')==R5_SHA,'TAIL_ON_R5_REQUIRED')
    else:
        require(call.get('family')=='DECIDING_III' and 'uv_tail' not in spec.get('numerics',{}),'ONLY_REGISTERED_DIII_TAIL_OFF_OMISSION_ALLOWED')
    return True

def globals_api():return types.SimpleNamespace(**{k:globals()[k] for k in ('require','R5_SHA','admitted_source','doc','load')})

def native_preflight(cfg,call):
    """Actual native policy/certificate/sensitivity calls, not acceptance of a PASS string."""
    spec=doc(call['spec']);spec_structure(call,spec)
    with fence(cfg['sources']):
        C=load(cfg['context_module'],cfg,'_step4_context')
        config,ag=adoption(cfg,C)
        tail=spec.get('numerics',{}).get('uv_tail',{}).get('enabled')
        require(spec.get('galaxy')=='DDO154' and spec.get('admit')=={},'FRESH_DDO154_SPEC_REQUIRED')
        require(type(call['tail_on']) is bool,'TAIL_MODE_REQUIRED')
        if call['tail_on']:
            require(tail is True,'TAIL_ON_SPEC_REQUIRED')
            require(call['driver']['sha256']==R5_SHA,'TAIL_ON_R5_REQUIRED')
            readiness=config.get('tail_readiness',{})
            for key in ('certificate_registry','certificate_policy_review','custody_deriver','state_enumerator'):
                verify(readiness.get(key))
            producers=readiness.get('approved_certificate_producers')
            require(isinstance(producers,list) and len(producers)>0,'CERTIFICATE_PRODUCERS_REQUIRED')
            for ref in producers:admitted_source(ref,cfg)
            admitted_source(readiness['custody_deriver'],cfg);admitted_source(readiness['state_enumerator'],cfg)
            adapter=load(cfg['direct_context'],cfg,'_step4_direct_preflight')
            require(adapter.DIRECT_CONTEXT_API=='UNT_STEP4_DIRECT_PREFLIGHT_CX1V001','DIRECT_CONTEXT_API_REQUIRED')
            ctx=adapter.build(C,config,guard=globals_api(),admission=cfg)
            pg=ctx.certificate_policy_gate();positive_gate(pg)
            cg=ctx.certificate_check(spec,'prelaunch');positive_gate(cg,'blockers')
            sg=ctx.sensitivity_gate(spec);positive_gate(sg)
            normalized=ctx.prelaunch_check(spec)
            checks={'certificate_policy':pg,'certificate_prelaunch':cg,'sensitivity':sg,'normalized_sha256':digest(normalized)}
        else:
            require(call.get('family')=='DECIDING_III' and 'uv_tail' not in spec.get('numerics',{}),'ONLY_REGISTERED_DIII_TAIL_OFF_OMISSION_ALLOWED')
            policy=doc(cfg['tail_off_policy'])
            require(policy.get('schema')=='UNT_STEP4_DIII_POLICY_CX1V001' and policy.get('authority')==AUTHORITY and policy.get('post_adoption_only') is True,'DIII_POLICY_REQUIRED')
            require(policy.get('verdict')=='PASS' and policy.get('status')=='TESTED' and policy.get('cases',{}).get(call['case'])=={'spec':call['spec'],'driver':call['driver']},'DIII_REVIEW_BINDING')
            drv=load(call['driver'],cfg,'_step4_diii_driver')
            normalized=drv.normalize_spec(spec)
            checks={'certificate_policy':'NOT_APPLICABLE_REVIEWED_TAIL_OFF_IDENTITY','certificate_prelaunch':'NOT_APPLICABLE_REVIEWED_TAIL_OFF_IDENTITY','sensitivity':'DECIDING_III_EVIDENCE_GENERATION_ONLY','normalized_sha256':digest(normalized),'tail_off_policy':cfg['tail_off_policy']}
    return {'schema':'UNT_STEP4_PRELAUNCH_CX1V001','case':call['case'],'spec':call['spec'],'driver':call['driver'],'config':cfg['config'],'adoption_verdict':cfg['v007']['verdict'],'checks':checks,'adoption_checked':True}


# A124: one fixed, non-symlinked output volume/root. statvfs supplies the same
# filesystem available-block measure as df without creating a helper process.
OUTPUT_VOLUME=Path('/Volumes/External1')
OUTPUT_ROOT=OUTPUT_VOLUME/'Research/UNT_STEP4_RUNS/V007_STEP4_DIRECT_V001'
DISK_RESERVE_BYTES=20*1024**3

def disk_free_bytes(path):
    try:
        v=os.statvfs(path)
        n=v.f_bavail*v.f_frsize
    except OSError as e:raise Refusal('DISK_READING_UNAVAILABLE') from e
    require(type(n) is int and n>=0,'DISK_READING_UNAVAILABLE')
    return n

def disk_output_volume(plan):
    # Reject aliases before resolution; root creates this directory at T0.
    require(OUTPUT_ROOT.is_dir(),'OUTPUT_ROOT_MISSING')
    for p in (OUTPUT_ROOT,*OUTPUT_ROOT.parents):
        require(not p.is_symlink(),'OUTPUT_SYMLINK_REFUSED')
    require(os.path.ismount(OUTPUT_VOLUME),'DECLARED_OUTPUT_VOLUME_UNMOUNTED')
    device=OUTPUT_VOLUME.stat().st_dev
    require(OUTPUT_ROOT.stat().st_dev==device,'WRONG_OUTPUT_VOLUME')
    paths=[plan['launcher_log']]
    for c in plan['calls']:paths.extend([c['outdir'],c['receipt'],c['monitor_log'],c['receipt']+'.launch.json'])
    for raw_path in paths:
        p=Path(raw_path)
        require(p.is_absolute() and '..' not in p.parts and p!=OUTPUT_ROOT and p.is_relative_to(OUTPUT_ROOT),'OUTPUT_OUTSIDE_DECLARED_ROOT')
        current=p
        while current!=OUTPUT_ROOT:
            require(not current.is_symlink(),'OUTPUT_SYMLINK_REFUSED')
            if current.exists():require(current.stat().st_dev==device,'WRONG_OUTPUT_VOLUME')
            current=current.parent
    return OUTPUT_VOLUME

def disk_admission(plan,call=None):
    volume=disk_output_volume(plan)
    chosen=plan['calls'] if call is None else [call]
    caps=[c.get('output_cap_bytes') for c in chosen]
    require(bool(caps) and all(type(n) is int and n>0 for n in caps),'POSITIVE_OUTPUT_CAP_REQUIRED')
    # Sum permits heterogeneous approved caps and equals calls*cap otherwise.
    required=sum(caps)+DISK_RESERVE_BYTES
    free=disk_free_bytes(volume)
    require(free>=required,'DISK_BATCH_BOUND' if call is None else 'DISK_START_BOUND')
    return {'free_bytes':free,'required_bytes':required,'volume':str(volume)}

# c2v012 (A150 R-S1-3 (1)): the S1 overlap admission. CORE_PRIORITY_INACTIVE is guard011 L333's dict, unchanged.
CORE_PRIORITY_INACTIVE={'normal_qos_required':True,'step2_route_a_inactive':True,'campaign_inactive':True,'background_noncritical_lanes':True,'sleep_assertion_required':True}
CORE_PRIORITY_S1_OVERLAP=dict(CORE_PRIORITY_INACTIVE,campaign_inactive=False)
S1_OVERLAP_SCHEMA='UNT_S1_OVERLAP_ADMISSION_C2V001'
S1_REPLAY_API='UNT_S1_FILL_REPLAY_C2V002'
S1_OVERLAP_CASES=('S1_UA_C3T','S1_UA_C4T')
# c2v013 (V006 A166): GATE_PIN, the A133 constants, s1_overlap_started, load_gate and s1_overlap_live are removed.
# c2v014 (V006 A172): the route-A rule's memory fields. guard013 L372-373 required them; guard014 refuses them.
MEMORY_ADMISSION_FIELDS=frozenset({'minimum_free_percent','source','first_case_memory_exemption'})

def core_priority_admission(plan,cfg):
    """guard011 L333 for every admission whose core_priority is the inactive dict (returns None: unchanged path).
    Otherwise only the S1 overlap form passes: POST_S1, one S1 call, tail ON on r5, the plan's fill record equal to
    the admission's, and the call's spec equal to the replay of that fill record by the admitted replay module."""
    cp=cfg.get('core_priority')
    if cp==CORE_PRIORITY_INACTIVE:return None
    require(cp==CORE_PRIORITY_S1_OVERLAP and plan.get('batch')=='POST_S1','CORE_PRIORITY_ATTESTATION_REQUIRED')
    ov=cfg.get('s1_overlap')
    require(isinstance(ov,dict),'S1_OVERLAP_ADMISSION_REQUIRED')
    require(set(ov)=={'schema','replay_module','fill_record'} and ov.get('schema')==S1_OVERLAP_SCHEMA,'S1_OVERLAP_ADMISSION_SCHEMA')
    calls=plan.get('calls')
    require(isinstance(calls,list) and len(calls)==1 and isinstance(calls[0],dict),'S1_OVERLAP_ONE_CALL_REQUIRED')
    call=calls[0]
    require(call.get('case') in S1_OVERLAP_CASES,'S1_OVERLAP_S1_CASE_REQUIRED')
    require(call.get('tail_on') is True and isinstance(call.get('driver'),dict) and call['driver'].get('sha256')==R5_SHA,'S1_OVERLAP_TAIL_ON_R5_REQUIRED')
    require(isinstance(plan.get('s1'),dict) and plan['s1'].get('fill_record')==ov['fill_record'],'S1_OVERLAP_FILL_RECORD_BINDING')
    verify(ov['fill_record'])
    m=load(ov['replay_module'],cfg,'_step4_s1_replay')
    require(getattr(m,'S1_REPLAY_API',None)==S1_REPLAY_API,'S1_OVERLAP_REPLAY_API')
    try:rep=m.guard_replay(ov['fill_record'])
    except Exception as e:raise Refusal('S1_OVERLAP_REPLAY_REFUSED',str(getattr(e,'code',None) or type(e).__name__)) from e
    got=(rep.get('cases') or {}).get(call['case']) if isinstance(rep,dict) else None
    require(isinstance(got,dict) and got.get('spec')==call.get('spec'),'S1_OVERLAP_SPEC_NOT_FILLED_SPEC')
    require(got.get('bytes')==verify(call['spec']),'S1_OVERLAP_REPLAY_MISMATCH')
    return call

def validate(plan_ref,producer,*,check_outputs=True,execute_native=True,config_ref=None,_candidate_config=None,_plan_bytes=None,disk_batch=True):
    """No process creation; validation precedes worker, sleep assertion and every monitor."""
    if config_ref is None and _candidate_config is None:
        p=os.environ.get('UNT_STEP4_ADMISSION_PATH','');h=os.environ.get('UNT_STEP4_ADMISSION_SHA256','')
        require(bool(p) and bool(h),'PUBLISHED_STEP4_ADMISSION_PENDING');config_ref={'path':p,'sha256':h}
    cfg=doc(config_ref) if _candidate_config is None else _candidate_config
    require(cfg.get('schema')=='UNT_STEP4_ADMISSION_CX1V001' and cfg.get('authority')==AUTHORITY,'ROOT_STEP4_AUTHORITY_REQUIRED')
    require(cfg.get('status')=='ROOT_AUTHORIZED' and cfg.get('plan')==plan_ref,'ROOT_PLAN_BINDING_REQUIRED')
    if _plan_bytes is None:plan=doc(plan_ref)
    else:
        require(isinstance(_plan_bytes,bytes) and hashlib.sha256(_plan_bytes).hexdigest()==plan_ref.get('sha256'),'PLAN_SNAPSHOT_HASH_MISMATCH')
        plan=decode(_plan_bytes);require(isinstance(plan,dict),'OBJECT_REQUIRED')
    require(plan.get('schema')=='UNT_STEP4_LAUNCH_PLAN_CX1V001' and plan.get('binding_status')=='ROOT_BOUND','UNBOUND_PLAN_REFUSED')
    source_map(cfg);check_review(cfg)
    for k in ('launcher','guard','monitor'):
        admitted_source(plan[k],cfg)
    require(plan['guard']==pin(__file__) and plan['launcher']==pin(producer),'LAUNCHER_GUARD_IDENTITY')
    require(plan['monitor']['sha256']==MONITOR_SHA,'FIXED_REVIEWED_MONITOR_REQUIRED')
    rule=plan.get('route_a_admission',{})
    require(type(rule.get('max_active')) is int and 1<=rule['max_active']<=6,'ROUTE_A_CAP_REQUIRED')
    require(rule==cfg.get('route_a_admission'),'ROOT_RAMP_APPROVAL_REQUIRED')
    require(rule.get('poll_seconds')==60 and rule.get('ramp')=='previous_first_completed_route_a_iteration','RAMP_RULE_REQUIRED')
    require(not MEMORY_ADMISSION_FIELDS&set(rule),'MEMORY_ADMISSION_FIELD_REFUSED')
    core_priority_admission(plan,cfg)
    require(plan.get('batch') in ('HEADLINE','DIII','SENS_LO','SENS_HI','POST_S1'),'BATCH_REQUIRED')
    calls=plan.get('calls');require(isinstance(calls,list) and len(calls)>0,'NONEMPTY_CALLS_REQUIRED')
    require(len({c['case'] for c in calls})==len(calls),'DUPLICATE_CASE')
    require(cfg.get('case_order')==[c['case'] for c in calls],'ROOT_ORDER_BINDING')
    outputs=[]
    for call in calls:
        require(call.get('spec_status')=='ROOT_FINAL' and call.get('pending')==[],'PENDING_SPEC_REFUSED')
        require(call['driver']['sha256'] in (R5_SHA,REF_SHA),'EXACT_R5_OR_DIII_REFERENCE_DRIVER_REQUIRED')
        if call['driver']['sha256']==REF_SHA:require(call.get('family')=='DECIDING_III' and call.get('driver_role')=='REFERENCE_V009GEO' and call['tail_on'] is False,'REFERENCE_DRIVER_SCOPE')
        admitted_source(call['driver'],cfg);verify(call['spec'])
        spec=doc(call['spec']);distance=call.get('distance_Mpc')
        require(type(distance) in (int,float) and math.isfinite(distance) and distance>0 and spec.get('physical',{}).get('distance_Mpc')==distance,'DISTANCE_BINDING')
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
    if disk_batch:disk_admission(plan)
    return plan,cfg

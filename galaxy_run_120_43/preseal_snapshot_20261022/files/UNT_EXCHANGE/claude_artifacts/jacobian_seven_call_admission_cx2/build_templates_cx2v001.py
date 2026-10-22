"""Build immutable, deliberately unbound 0848 templates from static metadata only.
date -u: Wed Oct 21 14:42:42 UTC 2026. No imported project or scientific code.
"""
import ast
import copy
import hashlib
import json
from pathlib import Path, PurePosixPath
import os
import sys

HERE=Path(__file__).parent
A=HERE.parent
E=A.parent
DATE_U='Wed Oct 21 14:42:42 UTC 2026'
def protected(p):
    if not isinstance(p,(str,bytes,os.PathLike)):return False
    s=os.fsdecode(p).casefold()
    return s.startswith('/volumes/') or '/runs/' in s or '/runs_ext/' in s or 'ngc3198' in s or 'v007_postseal_records' in s
def audit(event,args):
    if event in ('subprocess.Popen','os.system','os.fork','os.forkpty','os.posix_spawn','os.exec','socket.connect','socket.bind'):raise RuntimeError('PROCESS_NETWORK_FORBIDDEN')
    if event=='open' and protected(args[0]):raise RuntimeError('PROTECTED_OPEN_FORBIDDEN')
sys.addaudithook(audit)
for name in ('stat','lstat','readlink','listdir','scandir'):
    original=getattr(os,name)
    def wrapped(p='.',*args,_f=original,**kwargs):
        if protected(p):raise RuntimeError('PROTECTED_METADATA_FORBIDDEN')
        return _f(p,*args,**kwargs)
    setattr(os,name,wrapped)

def digest(b):return hashlib.sha256(b).hexdigest()
def enc(x):return json.dumps(x,sort_keys=True,indent=2,allow_nan=False).encode()+b'\n'
inputs={}
def read(p):
    p=Path(p);b=p.read_bytes();inputs[str(p)]=b;return b
def pin(p):
    b=read(p);return {'path':str(p),'sha256':digest(b)}
def write(name,b):
    if not isinstance(b,bytes):b=enc(b)
    p=HERE/name
    with p.open('xb') as f:f.write(b)
    return {'path':str(p),'sha256':digest(b)}
guard=A/'s1_successors_c2/step4_guard_c2v014.py'
launcher=A/'s1_successors_c2/step4_launcher_c2v015.py'
binder=A/'s1_successors_c2/step4_bind_c2v011.py'
common=A/'s4rc1_c3/build_c3v005_c2/s4rc1_common_c3v005.py'
minus=A/'future_wave_points_cx1/NOMINAL_W3_MINUS_DRAFT/POINTS_LIST.json'
params=A/'h11_wall_ceiling_c3/C2V004D_FILL_20261022T093000Z/DIRECT_BATCH_PARAMS_S45_C2V004D.json'
gp,lp,bp,cp,mp,dp=[pin(p) for p in (guard,launcher,binder,common,minus,params)]
assert gp['sha256']=='6efdca016416a919b25a1e23d46a415b75fe2b5e60145ba098f864730975165d'
assert lp['sha256']=='cd987edd097323999847208d7b5fdfd93dadecb8a10beb6feaf91a0c53b68e0b'
assert mp['sha256']=='9cfa8787934f2748482e30bbc15f57dcabfbf80b77d27c115cdc9478b54074d1'
assert dp['sha256']=='5d3f4bb84c35adee296048264ed306102ae51267f7da7ba2595cce561698f7a2'
dispatch={n:pin(E/'FROM_CODEX'/n) for n in [
 '0848_2026-10-21_codex2_resume_new_items_unit3_check_and_cause_cxv003.md',
 '0841_2026-10-21_codex1_direct_call_root_layout_ruled.md',
 '0837_2026-10-21_codex1_codex2_L2_retarget_direct_route_after_H11.md',
 '0828_2026-10-21_codex2_build_direct_path_certificate_lookup_nongenesis.md',
 '0514_2026-10-18_codex_any_nice_waiver.md']}
def literal(path,name):
    for n in ast.parse(inputs[str(path)]).body:
        if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets):return ast.literal_eval(n.value)
    raise AssertionError(name)
points=literal(common,'POINTS')
identities=[{'row':r[0],'point_key':r[1],'old_metadata_label':r[2],'distance_Mpc':r[6],'identity_source':cp} for r in points if r[0] in (28,29,30,31)]
identities += [{'row':r['row'],'point_key':r['key'],'old_metadata_label':r['label'],'distance_Mpc':r['theta']['distance_Mpc'],'identity_source':mp} for r in json.loads(inputs[str(minus)])['points']]
assert [r['row'] for r in identities]==[28,29,30,31,300,301,302]
assert all(r['distance_Mpc']==4.04 for r in identities)
assert len({r['point_key'] for r in identities})==7
ROOT='/Volumes/External1/Research/UNT_STEP4_RUNS/V007_STEP4_DIRECT_V001'
NULL={'path':None,'sha256':None}
caps={'wall_cap_s':3443340,'rss_cap_bytes':137438953472,'output_cap_bytes':85899345920}
rule={'max_active':6,'poll_seconds':60,'ramp':'previous_first_completed_route_a_iteration'}
assert all(c==caps for c in json.loads(inputs[str(params)])['batches']['HEADLINE']['caps_per_case'].values())
assert json.loads(inputs[str(params)])['batches']['HEADLINE']['route_a_admission']['max_active']==3
pending_common=[
 'ROOT_AUTHORIZATION_AND_INDEPENDENT_ADMISSION_PUBLICATION',
 'CODEX3_REVIEWED_FINAL_DIRECT_LOOKUP_AND_CONTEXT_SOURCE_CLOSURE',
 'ROOT_BOUND_C1_AND_DIRECT_CERTIFICATE_LOOKUP_REQUEST_MANIFEST',
 'EXACT_V007_ROOT_ADOPTION_TUPLE_AND_SOURCE_REVIEW',
 'ACTUAL_NATIVE_PREFLIGHT_REPLAY_AND_OUTPUT_VOLUME_DISK_CHECK',
 'HEADLINE11_ENDED_CAMPAIGN_INACTIVE_AND_MACHINE_LOCK_AVAILABLE',
 'ROOT_EXCLUSIVE_D_CREATION_NO_EXISTING_CALL_OUTPUTS',
]
plan={
 'schema':'UNT_STEP4_LAUNCH_PLAN_CX1V001','binding_status':'TEMPLATE_UNBOUND',
 'template_status':'UNTESTED_PRODUCTION_DO_NOT_EXECUTE','date_u':DATE_U,
 'batch':'HEADLINE','launcher':lp,'guard':gp,
 'monitor':{'path':None,'sha256':literal(guard,'MONITOR_SHA')},
 'route_a_admission':rule,'launcher_log':ROOT+'/DDO154_JACOBIAN_BATCH_A1.launcher.log',
 'calls':[],
 'template_metadata':{'purpose':'0848 item 1: seven fresh direct calls after HEADLINE11 ends',
    'binding_authority_pending':dispatch['0848_2026-10-21_codex2_resume_new_items_unit3_check_and_cause_cxv003.md'],
    'caps_source':dp,'caps_copy_scope':'HEADLINE per-call caps only; old HEADLINE max_active=3 is NOT copied.',
    'new_max_active_root_binding':'6 is proposed within 0848 and guard014; must be independently root-bound in plan AND admission.',
    'output_layout_authority':dispatch['0841_2026-10-21_codex1_direct_call_root_layout_ruled.md'],
    'disk_reserve_bytes':21474836480,'batch_required_free_bytes':622770257920,'each_start_required_free_bytes':107374182400,
    'pending':pending_common}}
for r in identities:
    row=r['row'];key=r['point_key'];d=ROOT+'/DDO154_JACOBIAN_R'+str(row)+'_'+key[:16]+'_A1'
    case='JACOBIAN_R'+str(row)
    plan['calls'].append({'case':case,'family':'JACOBIAN','row':row,'point_key':key,
       'identity_metadata':r,'tail_on':True,'driver_role':'CANDIDATE_R5',
       'driver':{'path':None,'sha256':literal(guard,'R5_SHA')},'spec':copy.deepcopy(NULL),
       'prelaunch':copy.deepcopy(NULL),'spec_status':'PENDING_ROOT_FINAL',
       'pending':['CODEX3_FINAL_FILLED_SPEC_PIN','ROOT_FINAL_SPEC_CONFIRMATION','MATCHING_NATIVE_PRELAUNCH_PIN'],
       'distance_Mpc':4.04,'outdir':d+'/out','receipt':d+'/RECEIPT.json',
       'monitor_log':d+'/monitor.log',**caps})
admission={
 'schema':'UNT_STEP4_ADMISSION_CX1V001','status':'PENDING_ROOT_AUTHORIZATION',
 'authority':literal(guard,'AUTHORITY'),'plan':None,'date_u':DATE_U,
 'template_status':'UNTESTED_PRODUCTION_DO_NOT_EXECUTE',
 'route_a_admission':copy.deepcopy(rule),'core_priority':literal(guard,'CORE_PRIORITY_INACTIVE'),
 'case_order':[c['case'] for c in plan['calls']],
 'caps':{c['case']:copy.deepcopy(caps) for c in plan['calls']},
 'calls':{c['case']:{k:copy.deepcopy(c[k]) for k in ('spec','driver','prelaunch')} for c in plan['calls']},
 'sources':{gp['path']:gp['sha256'],lp['path']:lp['sha256']},
 'source_review':copy.deepcopy(NULL),'config':copy.deepcopy(NULL),
 'context_module':copy.deepcopy(NULL),'direct_context':copy.deepcopy(NULL),
 'adoption_policy':copy.deepcopy(NULL),
 'v007':{k:copy.deepcopy(NULL) for k in ('seal','verdict','prereg','compare','addendum','case_block')},
 'direct_certificate_lookup':None,
 'template_metadata':{'pending':pending_common,
    'authority_is_required_identity_not_authorization':True,
    'sources_are_incomplete':'Only the reviewed guard/launcher pins are populated. No native module or certificate producer is approved here.',
    'direct_certificate_lookup':'PLACEHOLDER: use Codex3 final reviewed request/manifest schema and exact cfg extension; no schema or authority asserted here.',
    'direct_context':'PLACEHOLDER: final reviewed/adopted unit2 adapter must admit all seven point keys, including non-genesis R300-R302; never substitute old genesis-only adapter.',
    'binder_input_rule':'Root-authorized candidate must still carry plan:null; binder sets the output plan path/hash. A ROOT_BOUND final-plan successor and ROOT_AUTHORIZED admission successor must be made by root.',
    'caps_source':dp,'max_active_source':dispatch['0848_2026-10-21_codex2_resume_new_items_unit3_check_and_cause_cxv003.md']}}
pp=write('PLAN_TEMPLATE_CX2V001.json',plan)
ap=write('ADMISSION_TEMPLATE_CX2V001.json',admission)

# Verify the actual generated template contents, without touching paths they name.
checks=[]
def test(name,value):
    assert value,name
    checks.append({'name':name,'pass':True})
test('seven_unique_expected_rows',[c['row'] for c in plan['calls']]==[28,29,30,31,300,301,302] and len({c['case'] for c in plan['calls']})==7)
test('failclosed_statuses',plan['binding_status']!='ROOT_BOUND' and admission['status']!='ROOT_AUTHORIZED')
test('binder_plan_still_null',admission['plan'] is None)
test('max6_exact_cfg_plan',plan['route_a_admission']==admission['route_a_admission']==rule)
test('inactive_exact',admission['core_priority']==literal(guard,'CORE_PRIORITY_INACTIVE'))
test('no_memory_policy_fields',set(rule)=={'max_active','poll_seconds','ramp'})
test('batch_permitted_HEADLINE',plan['batch']=='HEADLINE')
test('native_source_extension_pending',admission['direct_context']==NULL and admission['direct_certificate_lookup'] is None and admission['source_review']==NULL)
outputs=[PurePosixPath(plan['launcher_log'])]
for c in plan['calls']:
    row=c['row'];d=PurePosixPath(ROOT)/('DDO154_JACOBIAN_R'+str(row)+'_'+c['point_key'][:16]+'_A1')
    test('R%d_layout'%row,c['outdir']==str(d/'out') and c['receipt']==str(d/'RECEIPT.json') and c['monitor_log']==str(d/'monitor.log'))
    test('R%d_pending_spec_prelaunch'%row,c['spec']==NULL and c['prelaunch']==NULL and c['spec_status']=='PENDING_ROOT_FINAL' and bool(c['pending']))
    test('R%d_caps_binding'%row,{k:c[k] for k in caps}==admission['caps'][c['case']]==caps)
    test('R%d_call_binding'%row,admission['calls'][c['case']]=={k:c[k] for k in ('spec','driver','prelaunch')})
    test('R%d_original_spec_not_D_spec'%row,c['spec']['path'] is None and c['driver']['path'] is None)
    outputs.extend(PurePosixPath(x) for x in (c['outdir'],c['receipt'],c['monitor_log'],c['receipt']+'.launch.json'))
test('all29_output_paths_distinct_and_non_nested',len(outputs)==29 and len(set(outputs))==29 and all(not p.is_relative_to(q) and not q.is_relative_to(p) for i,p in enumerate(outputs) for q in outputs[i+1:]))
test('launcher_log_outside_every_D',all(not PurePosixPath(plan['launcher_log']).is_relative_to(PurePosixPath(c['outdir']).parent) for c in plan['calls']))
test('batch_disk_580GiB',sum(c['output_cap_bytes'] for c in plan['calls'])+20*1024**3==622770257920)
test('per_start_disk_100GiB',caps['output_cap_bytes']+20*1024**3==107374182400)
test('caps_only_not_DBPD_maxidentity',json.loads(inputs[str(params)])['batches']['HEADLINE']['route_a_admission']['max_active']==3 and rule['max_active']==6)
tp=write('TEMPLATE_CHECKS_CX2V001.json',{'date_u':DATE_U,'status':'TESTED','production':'UNTESTED',
    'priority_note':'nice unavailable (sandbox); 0514 waiver','passed':len(checks),'total':len(checks),
    'templates':[pp,ap],'checks':checks,'filesystem_effects':'new review artifact files only; all named run paths processed lexically as PurePosixPath strings'})

sites={}
for p,names in [(guard,['validate','core_priority_admission','spec_structure','native_preflight','disk_admission','disk_output_volume']),
                (launcher,['decision','worker','acquire_lock','monitor_argv','main']), (binder,['bind','check_command'])]:
    tree=ast.parse(inputs[str(p)],str(p))
    sites[str(p)]={n.name:{'line':n.lineno,'end_line':n.end_lineno,'text':ast.get_source_segment(inputs[str(p)].decode(),n)} for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names}
sp=write('SOURCE_PROOF_CX2V001.json',{'date_u':DATE_U,'classification':'FORMAL-RESULT from exact source control flow; native policy/OS state UNTESTED',
 'source_pins':[gp,lp,bp], 'sites':sites,
 'conclusions':[
  'guard.validate has no total-call ceiling: nonempty unique calls plus independently bound order; HEADLINE accepted.',
  'Inactive core-priority exact dictionary admits this batch; live campaign rejects the HEADLINE path.',
  'Tail-ON family has no special name whitelist in spec_structure; all seven still require fresh DDO154/R5 specs and actual native policy, certificate and sensitivity gates.',
  'Launcher route-A count excludes finished route-A stages even if their monitor remains active; max_active is not total live-monitor cap.',
  'Seventh admission requires active route-A below six AND immediate predecessor first completed iteration, plus fresh guard/disk checks.',
  'Machine flock is persistent and nonblocking; fd is inherited by monitor lifetime owners and retained through draining.',
  'Launcher opens monitor_log exclusively before monitor Popen; root must exclusively prepare D, leaving all four call outputs absent.',
  'Binder snapshots plan bytes, calls full validate before any write, restricts all three outputs to packet folder, writes exclusively and never self-publishes authority.',
  'No guard014/launcher015/binder011 successor is needed merely for seven calls. Complete native admission remains pending final reviewed unit2 adapter/source closure and actual root bindings.']})

testp=pin(HERE/'STATIC_ADMISSION_TESTS_CX2V001.json')
testdata=json.loads(inputs[testp['path']])
assert testdata['passed']==testdata['total']==97
binding={
 'date_u':DATE_U,'status':'PENDING_ROOT_BINDING','production':'UNTESTED','review_verdict':'PASS_WITH_FINDINGS_SCOPE_LIMITED',
 'plan_template':pp,'admission_template':ap,'binder':bp,
 'required_root_inputs':[
  'Exclusive selected output D directories and launcher-log pathname; no call output or sidecar may exist. No assumption of D/spec.json.',
  'Independent root confirmation HEADLINE11 fully ended, no campaign live, exact inactive core-priority attestation; machine lock must actually be available.',
  'Root binding max_active=6 in both plan/admission. This changes DBPD HEADLINE design3; seven-call order/names/caps are independently rebound.',
  'All seven Codex3 final filled spec pins and original external spec paths, ROOT_FINAL statuses and pending=[] only after actual finalization.',
  'Actual R5 driver and fixed monitor paths/hash verification; full transitive source closure; distinct reviewed source-map pin.',
  'Codex3 reviewed/adopted non-genesis direct_context, direct_certificate_lookup request/manifest extension, matching C1 config and every dependency source pin. No old genesis-only substitution.',
  'Actual root V007 adoption tuple (seal/verdict/prereg/compare/addendum/case_block), adoption policy, context module; this review has not opened postseal records.',
  'Actual native_preflight replay for each filled spec; prelaunch doc byte pin must match recomputation and cfg.calls exactly.',
  'Actual fixed volume/mount/device/symlink/output-exclusivity checks and >=580 GiB free at batch validation; >=100 GiB before each individual start.',
  'New ROOT_BOUND final-plan successor and ROOT_AUTHORIZED admission-candidate successor (plan:null) after review; these templates stay unchanged.',
  'Binder output paths all new, distinct, nonnested and under step4_launch_packet_cx1. Root alone executes binder and independently publishes exact returned admission path/hash.',
  'The wall duration3443340 is copied from DBPD HEADLINE, not an automatically recomputed absolute ceiling. Root binds its applicability at actual start; no retry or cleanup is added.'],
 'suggested_binder_outputs_not_created':{k:str(A/'step4_launch_packet_cx1/jacobian_seven_call_root_binding_A1'/v) for k,v in
    [('plan_out','PLAN_ROOT_BOUND.json'),('admission_out','ADMISSION_ROOT_BOUND.json'),('command_out','ROOT_ONLY_COMMAND.txt')]},
 'no_command_generated':True,
 'unavailable':['Native final source/config/spec/prelaunch approval and bytepins','Actual OS flock/disk/output state','Production scheduling/scientific outputs'],
 'tests':testp,'template_checks':tp,'source_proof':sp}
rp=write('ROOT_BIND_INPUTS_CX2V001.json',binding)

for p,b in inputs.items():assert Path(p).read_bytes()==b,'INPUT_CHANGED:'+p
ip=write('INPUT_PINS_CX2V001.json',{'date_u':DATE_U,'before_after_equal':True,
 'files':[{'path':p,'sha256':digest(b),'bytes':len(b)} for p,b in inputs.items()]})
def ref(pin):return '`'+pin['path']+'` — SHA256 `'+pin['sha256']+'`'
text='''# Seven-call static admission review — 0848 item 1

date -u: '''+DATE_U+'''

**PASS_WITH_FINDINGS, scoped to source/schema/scheduling.** No guard014, launcher015 or binder011 successor is needed merely to carry this seven-call batch. **Full native/production admission is UNTESTED and remains blocked by pending final root/Codex3 inputs.** Templates are deliberately unbound and non-executable.

TESTED: 97/97 bounded source-function controls and '''+str(len(checks))+'''/'''+str(len(checks))+''' checks of the generated templates. Only selected AST definitions ran in one isolated Python process. Source approval/native policy, path existence, volume/free-space and flock operations used explicit in-memory seams. No project module, launcher/monitor/worker, scientific routine, subprocess, run tree or NGC input was executed/read/probed. Exact source bytes were checked again at completion. `nice unavailable (sandbox); 0514 waiver`; effective priority 0, all BLAS thread variables set to1. Native policy PASS and physical run identity are not inferred from these controls.

FORMAL-RESULT from the pinned source: guard014 permits a nonempty unique-call HEADLINE list with no total-seven ceiling. Its max_active limit is integer1..6. Tail-ON has no family/case-name whitelist, while every spec remains fresh DDO154/R5 and subject to actual certificate, sensitivity and adoption gates. The inactive core-priority dictionary is mandatory for this HEADLINE path; the old live-W1 premise is superseded by0848.

The launcher starts at most one call per poll and requires its immediate predecessor's first completed route-A iteration. At six active route-A calls, call7 waits; when one leaves routeA, call7 may start only if its predecessor marker and guard/disk gates pass. Route-B monitors may still be active: max_active6 caps routeA, not total live processes. Machine flock is exclusive/nonblocking and retained through draining and inherited monitor lifetimes. Actual OS behavior and HEADLINE11 termination are UNTESTED premises for root to confirm.

Caps are wall3443340s, RSS137438953472B and output85899345920B per call, copied from DBPD HEADLINE caps. DBPD's HEADLINE max_active is3; this proposed6 requires its own0848 root data binding in both documents. Disk reserve is20GiB; batch admission requires580GiB=622770257920B, each start100GiB=107374182400B. No volume or free-space probe was made.

The seven identities are source metadata only: rows28–31 from common metadata; rows300–302 from the explicitly synthetic draft POINTS_LIST. No draft spec hash was promoted to ROOT_FINAL. Every original final spec and native prelaunch pin is null. Paths are D/out, D/RECEIPT.json, D/RECEIPT.json.launch.json and D/monitor.log; launcher log is outside everyD. Root must create each D exclusively before launching because launcher015 opens monitor.log before spawning the monitor. It must leave all four call outputs absent. No D/spec.json is presumed.

Unit2 remains a real dependency: root must adopt Codex3's reviewed non-genesis lookup/context, request/manifest cfg extension and exact source closure for R300–302. `direct_context`, `direct_certificate_lookup`, source review and native config/adoption references remain pending. The old genesis-only adapter is not an acceptable substitute. Root must populate and review the full missing-input checklist, make new authorized successor documents, and use binder011 only after full native/disk validation. Binder writes exclusively under step4_launch_packet_cx1 and does not grant or publish authority. No executable command is generated here.

Artifacts (all immutable):

'''+ '\n'.join('- '+ref(x) for x in (pp,ap,rp,testp,tp,sp,ip))+'''

Reviewed source bytes:

'''+ '\n'.join('- '+ref(x) for x in (gp,lp,bp,cp,mp,dp))+'''

Authority/waiver bytes:

'''+ '\n'.join('- '+ref(x) for x in dispatch.values())+'''

No active execution remains. Parent owns the numbered report and root coordination. This is a build/review artifact, not launch authorization.
'''
readme=write('README_CX2V001.md',text.encode())
outputs=[HERE/'check_admission_static_cx2v001.py',HERE/'build_templates_cx2v001.py',HERE/'STATIC_ADMISSION_TESTS_CX2V001.json']+[Path(x['path']) for x in (pp,ap,tp,sp,rp,ip,readme)]
all_pins={p:digest(b) for p,b in inputs.items()}
for p in outputs:all_pins[str(p)]=digest(p.read_bytes())
manifest=('# date -u: '+DATE_U+'\n# SHA256 from file bytes; no run-tree inputs.\n'+''.join(h+'  '+p+'\n' for p,h in sorted(all_pins.items()))).encode()
hp=write('HASHES_CX2V001.txt',manifest)
print(json.dumps({'verdict':'PASS_WITH_FINDINGS_SCOPE_LIMITED','static_tests':97,'template_checks':len(checks),'readme':readme,'hashes':hp,'plan':pp,'admission':ap,'binder_pin':bp}))

"""0848 item 1: own in-process structural admission controls; no project import.

Only selected AST function definitions are compiled from pinned reviewed bytes.
All validator inputs and output-existence, disk, source/native-authority and flock
dependencies below are explicitly synthetic. No production path is probed.
"""
import ast
import copy
import datetime
import hashlib
import io
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import shlex
import sys
import types

HERE = Path(__file__).parent
A = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
E = A.parent
GUARD = A/'s1_successors_c2/step4_guard_c2v014.py'
LAUNCHER = A/'s1_successors_c2/step4_launcher_c2v015.py'
BINDER = A/'s1_successors_c2/step4_bind_c2v011.py'
COMMON = A/'s4rc1_c3/build_c3v005_c2/s4rc1_common_c3v005.py'
PARAMS = A/'h11_wall_ceiling_c3/C2V004D_FILL_20261022T093000Z/DIRECT_BATCH_PARAMS_S45_C2V004D.json'
EXPECTED = {
    str(GUARD): '6efdca016416a919b25a1e23d46a415b75fe2b5e60145ba098f864730975165d',
    str(LAUNCHER): 'cd987edd097323999847208d7b5fdfd93dadecb8a10beb6feaf91a0c53b68e0b',
    str(PARAMS): '5d3f4bb84c35adee296048264ed306102ae51267f7da7ba2595cce561698f7a2',
}
DISPATCH_NAMES = [
    '0848_2026-10-21_codex2_resume_new_items_unit3_check_and_cause_cxv003.md',
    '0841_2026-10-21_codex1_direct_call_root_layout_ruled.md',
    '0837_2026-10-21_codex1_codex2_L2_retarget_direct_route_after_H11.md',
    '0828_2026-10-21_codex2_build_direct_path_certificate_lookup_nongenesis.md',
    '0514_2026-10-18_codex_any_nice_waiver.md',
]
INPUTS = [GUARD, LAUNCHER, BINDER, COMMON, PARAMS] + [E/'FROM_CODEX'/n for n in DISPATCH_NAMES]

def forbidden(value):
    if not isinstance(value, (str, bytes, os.PathLike)):
        return False
    s = os.fsdecode(value).casefold()
    return (s.startswith('/volumes/') or '/runs/' in s or '/runs_ext/' in s
            or 'ngc3198' in s or 'v007_postseal_records' in s
            or '/.codex/log' in s or '/.codex/session' in s)

def audit(event, args):
    if event in ('subprocess.Popen', 'os.system', 'os.fork', 'os.forkpty',
                 'os.posix_spawn', 'os.exec', 'socket.connect', 'socket.bind'):
        raise RuntimeError('TEST_PROCESS_NETWORK_FORBIDDEN')
    if event == 'open' and forbidden(args[0]):
        raise RuntimeError('TEST_PROTECTED_OPEN_FORBIDDEN')

sys.addaudithook(audit)
for _name in ('stat', 'lstat', 'readlink', 'listdir', 'scandir'):
    _original = getattr(os, _name)
    def _guarded(value='.', *args, _original=_original, **kwargs):
        if forbidden(value):
            raise RuntimeError('TEST_PROTECTED_METADATA_FORBIDDEN')
        return _original(value, *args, **kwargs)
    setattr(os, _name, _guarded)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()

raws = {str(p): p.read_bytes() for p in INPUTS}
pins = [{'path': p, 'sha256': sha(b), 'bytes': len(b)} for p, b in raws.items()]
for p, h in EXPECTED.items():
    assert sha(raws[p]) == h, (p, sha(raws[p]))

def definitions(path, names, namespace):
    tree = ast.parse(raws[str(path)], str(path))
    nodes = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names]
    assert {n.name for n in nodes} == set(names)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), namespace)
    return {n.name: {'line': n.lineno, 'end_line': n.end_lineno} for n in nodes}

def literal(path, name):
    tree = ast.parse(raws[str(path)])
    for n in tree.body:
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in n.targets):
            return ast.literal_eval(n.value)
    raise AssertionError(name)

G = {'__file__': str(GUARD), 'hashlib': hashlib, 'math': math, 'json': json, 're': re}
G.update({n: literal(GUARD, n) for n in ('AUTHORITY', 'R5_SHA', 'REF_SHA', 'MONITOR_SHA', 'CORE_PRIORITY_INACTIVE')})
G.update(MEMORY_ADMISSION_FIELDS=frozenset({'minimum_free_percent', 'source', 'first_case_memory_exemption'}),
         CORE_PRIORITY_S1_OVERLAP=dict(G['CORE_PRIORITY_INACTIVE'], campaign_inactive=False),
         DISK_RESERVE_BYTES=20*1024**3)
proof = {'guard': definitions(GUARD, ['Refusal', 'require', '_pairs', '_finite_float', 'decode',
    'canonical', 'digest', 'spec_structure', 'core_priority_admission', 'disk_admission', 'validate'], G)}
Refusal = G['Refusal']
bank = {}
documents = {}
native = {}

def put(name, obj):
    b = canon(obj)
    p = '/INERT_ONLY/' + name
    bank[p] = b
    documents[p] = copy.deepcopy(obj)
    return {'path': p, 'sha256': sha(b)}

declared_external = []
guard_pin = {'path': str(GUARD), 'sha256': sha(raws[str(GUARD)])}
launcher_pin = {'path': str(LAUNCHER), 'sha256': sha(raws[str(LAUNCHER)])}
monitor_pin = {'path': '/INERT_ONLY/monitor.py', 'sha256': G['MONITOR_SHA']}
driver_pin = {'path': '/INERT_ONLY/driver.py', 'sha256': G['R5_SHA']}
declared_external.extend([monitor_pin, driver_pin, guard_pin, launcher_pin])

def verify_inert(ref):
    G['require'](isinstance(ref, dict) and set(ref) == {'path','sha256'}, 'PIN_REQUIRED')
    if ref in declared_external:
        return b'EXPLICIT_DECLARED_SOURCE_VERIFICATION_SEAM'
    G['require'](ref['path'] in bank and sha(bank[ref['path']]) == ref['sha256'], 'PIN_BYTES_CHANGED')
    return bank[ref['path']]

def doc_inert(ref):
    return G['decode'](verify_inert(ref))

def source_map_inert(cfg):
    G['require'](cfg['sources'] == {r['path']:r['sha256'] for r in declared_external}, 'SOURCES_SEAM_MISMATCH')
    return cfg['sources']

def admitted_inert(ref, cfg):
    verify_inert(ref)
    G['require'](cfg['sources'].get(ref['path']) == ref['sha256'], 'SOURCE_NOT_ALLOWLISTED')

def preflight_inert(cfg, call):
    G['spec_structure'](call, doc_inert(call['spec']))
    return copy.deepcopy(native[call['case']])

disk_free = 580*1024**3
G.update(verify=verify_inert, doc=doc_inert, source_map=source_map_inert,
         check_review=lambda cfg: G['require'](cfg['synthetic_review'] is True, 'SYNTHETIC_REVIEW_REQUIRED'),
         admitted_source=admitted_inert, pin=lambda p: guard_pin if p == str(GUARD) else launcher_pin,
         native_preflight=preflight_inert, safe_path=lambda p: PurePosixPath(p),
         os=types.SimpleNamespace(path=types.SimpleNamespace(lexists=lambda p: False)),
         disk_output_volume=lambda p: PurePosixPath('/INERT_ONLY/volume'),
         disk_free_bytes=lambda p: disk_free)

caps = {'wall_cap_s':3443340, 'rss_cap_bytes':137438953472, 'output_cap_bytes':85899345920}
rule = {'max_active':6, 'poll_seconds':60, 'ramp':'previous_first_completed_route_a_iteration'}
rows = [28,29,30,31,300,301,302]
plan = {'schema':'UNT_STEP4_LAUNCH_PLAN_CX1V001', 'binding_status':'ROOT_BOUND',
        'batch':'HEADLINE', 'guard':guard_pin, 'launcher':launcher_pin, 'monitor':monitor_pin,
        'route_a_admission':copy.deepcopy(rule), 'launcher_log':'/INERT_ONLY/output/batch.launcher.log', 'calls':[]}
cfg = {'schema':'UNT_STEP4_ADMISSION_CX1V001','authority':G['AUTHORITY'], 'status':'ROOT_AUTHORIZED',
       'plan':None,'synthetic_review':True,'route_a_admission':copy.deepcopy(rule),
       'core_priority':copy.deepcopy(G['CORE_PRIORITY_INACTIVE']),
       'sources':{r['path']:r['sha256'] for r in declared_external},'calls':{},'caps':{},'case_order':[]}
for row in rows:
    case = 'JACOBIAN_R'+str(row)
    spec = put(case+'.spec', {'galaxy':'DDO154', 'admit':{}, 'physical':{'distance_Mpc':4.04}, 'numerics':{'uv_tail':{'enabled':True}}})
    native[case] = {'schema':'SYNTHETIC_NATIVE_SEAM_ONLY','case':case,'spec':spec}
    prelaunch = put(case+'.prelaunch', native[case])
    d = '/INERT_ONLY/output/'+case
    call = dict(case=case,family='JACOBIAN',tail_on=True,driver=driver_pin,spec=spec,prelaunch=prelaunch,
                spec_status='ROOT_FINAL',pending=[],distance_Mpc=4.04,outdir=d+'/out',receipt=d+'/RECEIPT.json',
                monitor_log=d+'/monitor.log',**caps)
    plan['calls'].append(call)
    cfg['case_order'].append(case)
    cfg['calls'][case] = {'spec':spec,'driver':driver_pin,'prelaunch':prelaunch}
    cfg['caps'][case] = copy.deepcopy(caps)

results = []
def check(name, fn, code=None):
    try:
        value = fn()
        ok = code is None and value is not False
        observed = 'ACCEPT' if ok else repr(value)
    except Exception as e:
        observed = str(e)
        ok = code is not None and type(e) is Refusal and observed == code
    results.append({'name':name,'pass':ok,'expected':'ACCEPT' if code is None else code,'observed':observed})

def run(p=None,c=None):
    p = copy.deepcopy(plan if p is None else p)
    c = copy.deepcopy(cfg if c is None else c)
    b = canon(p); r = {'path':'/INERT_ONLY/plan','sha256':sha(b)}; c['plan'] = r
    return G['validate'](r,str(LAUNCHER),_candidate_config=c,_plan_bytes=b)

check('actual_validate_seven_tail_on_arbitrary_cases_HEADLINE', run)
def mutation(name, pm=None, cm=None, code=None):
    p,c = copy.deepcopy(plan),copy.deepcopy(cfg)
    if pm:pm(p)
    if cm:cm(c)
    check(name, lambda:run(p,c), code)
mutation('eight_calls_also_no_total_count_cap', lambda p:p['calls'].append(dict(p['calls'][0],case='JACOBIAN_R999')), code='ROOT_ORDER_BINDING')
for v in (0,7,True,6.0):
    mutation('max_active_'+repr(v),lambda p,v=v:p['route_a_admission'].__setitem__('max_active',v),code='ROUTE_A_CAP_REQUIRED')
mutation('rule_binding',cm=lambda c:c['route_a_admission'].__setitem__('max_active',3),code='ROOT_RAMP_APPROVAL_REQUIRED')
for key,value in [('poll_seconds',59),('ramp','arbitrary')]:
    mutation('ramp_'+key, lambda p,k=key,v=value:p['route_a_admission'].__setitem__(k,v),
             lambda c,k=key,v=value:c['route_a_admission'].__setitem__(k,v), 'RAMP_RULE_REQUIRED')
for key in sorted(G['MEMORY_ADMISSION_FIELDS']):
    mutation('forbid_memory_'+key,lambda p,k=key:p['route_a_admission'].__setitem__(k,False),
             lambda c,k=key:c['route_a_admission'].__setitem__(k,False),'MEMORY_ADMISSION_FIELD_REFUSED')
mutation('campaign_live',cm=lambda c:c['core_priority'].__setitem__('campaign_inactive',False),code='CORE_PRIORITY_ATTESTATION_REQUIRED')
mutation('step2_live',cm=lambda c:c['core_priority'].__setitem__('step2_route_a_inactive',False),code='CORE_PRIORITY_ATTESTATION_REQUIRED')
mutation('new_unrecognized_batch',lambda p:p.__setitem__('batch','JACOBIAN'),code='BATCH_REQUIRED')
mutation('empty_calls',lambda p:p.__setitem__('calls',[]),code='NONEMPTY_CALLS_REQUIRED')
mutation('duplicate_case',lambda p:p['calls'][1].__setitem__('case',p['calls'][0]['case']),code='DUPLICATE_CASE')
mutation('root_order_swap',cm=lambda c:c['case_order'].reverse(),code='ROOT_ORDER_BINDING')
mutation('pending_finalspec',lambda p:p['calls'][0].__setitem__('spec_status','PENDING_ROOT_FINAL'),code='PENDING_SPEC_REFUSED')
mutation('pending_items',lambda p:p['calls'][0].__setitem__('pending',['ROOT']),code='PENDING_SPEC_REFUSED')
mutation('cap_zero',lambda p:p['calls'][0].__setitem__('wall_cap_s',0),code='POSITIVE_INTEGER_CAPS_REQUIRED')
mutation('cap_binding',cm=lambda c:c['caps']['JACOBIAN_R28'].__setitem__('wall_cap_s',100800),code='ROOT_CAPS_BINDING')
mutation('spec_ref_binding',cm=lambda c:c['calls']['JACOBIAN_R28'].__setitem__('spec',plan['calls'][1]['spec']),code='ROOT_CALL_BINDING')
mutation('distance_binding',lambda p:p['calls'][0].__setitem__('distance_Mpc',4.05),code='DISTANCE_BINDING')
mutation('output_alias',lambda p:p['calls'][1].__setitem__('outdir',p['calls'][0]['outdir']),code='ALIASED_OUTPUTS')
mutation('output_nested',lambda p:p['calls'][0].__setitem__('monitor_log',p['calls'][0]['outdir']+'/monitor.log'),code='NESTED_OUTPUTS')
mutation('unbound_template_refuses',lambda p:p.__setitem__('binding_status','TEMPLATE_UNBOUND'),code='UNBOUND_PLAN_REFUSED')
mutation('unauthorized_template_refuses',cm=lambda c:c.__setitem__('status','PENDING_ROOT_AUTHORIZATION'),code='ROOT_PLAN_BINDING_REQUIRED')
old_native=copy.deepcopy(native['JACOBIAN_R28']);native['JACOBIAN_R28']['foreign']=True
check('prelaunch_replay_mismatch',run,'PRELAUNCH_REPLAY_MISMATCH');native['JACOBIAN_R28']=old_native

check('disk_batch_equal_580GiB',lambda:G['disk_admission'](plan)['required_bytes']==622770257920)
disk_free=622770257919
check('disk_batch_one_byte_short',lambda:G['disk_admission'](plan),'DISK_BATCH_BOUND')
disk_free=107374182400
check('disk_start_equal_100GiB',lambda:G['disk_admission'](plan,plan['calls'][0])['required_bytes']==107374182400)
disk_free-=1
check('disk_start_one_byte_short',lambda:G['disk_admission'](plan,plan['calls'][0]),'DISK_START_BOUND')
disk_free=622770257920

L={'G':types.SimpleNamespace(**G)}
proof['launcher']=definitions(LAUNCHER,['decision','first_iteration','route_a_finished','acquire_lock'],L)
for active in range(8):
    for previous in (False,True):
        for first in (False,True):
            expected = active<6 and (first or previous)
            check('decision_%d_%s_%s'%(active,previous,first),lambda a=active,p=previous,f=first,e=expected:L['decision'](active_route_a=a,previous_iteration=p,first=f,max_active=6)==e)
for invalid in (True,-1,2.0,None):
    check('decision_invalid_'+repr(invalid),lambda a=invalid:L['decision'](active_route_a=a,previous_iteration=True,first=False,max_active=6) is False)
check('seventh_waits_when_six_routeA',lambda:L['decision'](active_route_a=6,previous_iteration=True,first=False,max_active=6) is False)
check('seventh_can_start_after_one_leaves_routeA',lambda:L['decision'](active_route_a=5,previous_iteration=True,first=False,max_active=6) is True)
check('seventh_still_waits_if_predecessor_no_iteration',lambda:L['decision'](active_route_a=5,previous_iteration=False,first=False,max_active=6) is False)
for record,expected in [({'stage':'iteration_completed','iteration':0},True),({'stage':'iteration_completed','iteration':-1},False),({'stage':'iteration_completed','iteration':True},False),({'stage':'iteration_started','iteration':0},False)]:
    L['read_progress']=lambda p,r=record:[r]
    check('iteration_marker_'+str(record),lambda e=expected:L['first_iteration']('IN_MEMORY') is e)
for record,expected in [({'stage':'route_a','event':'finished'},True),({'stage':'route_a','event':'started'},False),({'stage':'route_b','event':'finished'},False)]:
    L['read_progress']=lambda p,r=record:[r]
    check('routeA_marker_'+str(record),lambda e=expected:L['route_a_finished']('IN_MEMORY') is e)

class FakeLock:
    symlink=False
    def is_symlink(self):return self.symlink
lock=FakeLock(); events=[]; exists=False; conflict=False
def fake_open(p,flags,mode=None):
    events.append(['open',flags,mode])
    if exists and flags & 0x100:raise FileExistsError()
    return 17
def fake_flock(fd,flags):
    events.append(['flock',fd,flags])
    if conflict:raise BlockingIOError()
L.update(LOCK=lock,os=types.SimpleNamespace(open=fake_open,close=lambda fd:events.append(['close',fd]),
    O_CREAT=0x100,O_EXCL=0x200,O_RDONLY=0),fcntl=types.SimpleNamespace(flock=fake_flock,LOCK_EX=2,LOCK_NB=4))
check('flock_new_inode_nonblocking_exclusive',lambda:L['acquire_lock']()==17 and events==[['open',0x300,0o600],['flock',17,6]])
events.clear();exists=True
check('flock_existing_inode_readonly_no_truncation',lambda:L['acquire_lock']()==17 and events==[['open',0x300,0o600],['open',0,None],['flock',17,6]])
events.clear();conflict=True
check('flock_conflict_refuses',L['acquire_lock'],'ANOTHER_STEP4_BATCH_ACTIVE')
check('flock_conflict_closes_fd',lambda:events[-1]==['close',17])
lock.symlink=True
check('flock_symlink_refuses',L['acquire_lock'],'LOCK_SYMLINK_REFUSED')

B={'G':types.SimpleNamespace(**G),'os':os,'NICE_PROGRAMS':frozenset({'nice','renice'})}
proof['binder']=definitions(BINDER,['check_command'],B)
check('binder_plain_command_accepts',lambda:B['check_command'](['env','OMP_NUM_THREADS=1','python','-I','-B','launcher','plan','--execute-root-only']))
for exe in ('nice','/usr/bin/nice','renice'):
    check('binder_forbids_'+exe,lambda e=exe:B['check_command']([e,'-n','10','python']),'NICE_IN_COMMAND_REFUSED')

# Source statements (not executed): retain the owning AST site, not a supplied test.
trees={str(p):ast.parse(raws[str(p)],str(p)) for p in (GUARD,LAUNCHER,BINDER)}
for path,names in ((LAUNCHER,['worker','main','monitor_argv']), (BINDER,['bind'])):
    proof[str(path)]={n.name:{'line':n.lineno,'end_line':n.end_lineno} for n in trees[str(path)].body if isinstance(n,ast.FunctionDef) and n.name in names}
worker=next(n for n in trees[str(LAUNCHER)].body if isinstance(n,ast.FunctionDef) and n.name=='worker')
worker_text=ast.get_source_segment(raws[str(LAUNCHER)].decode(),worker)
check('source_active_count_excludes_routeA_finished',lambda:"count=sum(not item['route_a_finished'] for item in active)" in worker_text)
check('source_progress_ramp_uses_attempt000',lambda:"'stages/01_route_a/attempt_000/progress.jsonl'" in worker_text)
check('source_monitor_log_open_exclusive_before_spawn',lambda:worker_text.index("with open(c['monitor_log'],'xb')")<worker_text.index("proc=subprocess.Popen(['/usr/bin/caffeinate'"))
check('source_machine_lock_inherited_by_monitor_lifetime',lambda:'pass_fds=(lock,)' in worker_text)
check('source_no_auto_retry',lambda:"'retry':'NONE'" in worker_text and 'pending.clear()' in worker_text)
check('source_guard_rechecks_native_default',lambda:'G.validate(plan_ref,__file__,check_outputs=False,disk_batch=False)' in worker_text)
check('source_lock_close_after_no_active',lambda:worker_text.index("if active:raise RuntimeError('ACTIVE_MONITORS_RETAINED_LOCK_NOT_CLOSED')")<worker_text.index('os.close(lock)'))

params=json.loads(raws[str(PARAMS)])
check('DBPD_HEADLINE_uniform_caps',lambda:all(x==caps for x in params['batches']['HEADLINE']['caps_per_case'].values()))
check('DBPD_HEADLINE_old_max3_not_proposed6',lambda:params['batches']['HEADLINE']['route_a_admission']['max_active']==3 and rule['max_active']==6)
for p,b in raws.items():assert Path(p).read_bytes()==b, 'INPUT_CHANGED:'+p
report={'schema':'JACOBIAN_SEVEN_CALL_STATIC_TESTS_CX2V001','status':'TESTED',
    'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'date_u_evidence':'Wed Oct 21 14:40:43 UTC 2026',
    'priority_note':'nice unavailable (sandbox); 0514 waiver','effective_priority':os.getpriority(os.PRIO_PROCESS,0),
    'execution':'One isolated Python process; stdlib only; selected AST functions; no project imports, subprocesses or real disk/lock operations.',
    'seams':['source-map/approval/native policy are explicit synthetic dependencies',
             'all documents are in-memory; no production specs or prelaunch reports read',
             'safe_path/output existence and volume/free-space are inert adapters',
             'flock/open are recorded mocks; no real lock inode touched'],
    'scientific_launches':0,'production_admission':'UNTESTED','input_pins_before_and_after':pins,
    'source_sites':proof,'passed':sum(r['pass'] for r in results),'total':len(results),'results':results}
assert report['passed']==report['total'], json.dumps([r for r in results if not r['pass']])
with (HERE/'STATIC_ADMISSION_TESTS_CX2V001.json').open('xb') as f:f.write(json.dumps(report,sort_keys=True,indent=2).encode()+b'\n')
print(json.dumps({'passed':report['passed'],'total':report['total'],'test_result':str(HERE/'STATIC_ADMISSION_TESTS_CX2V001.json'),'sha256':sha((HERE/'STATIC_ADMISSION_TESTS_CX2V001.json').read_bytes())}))

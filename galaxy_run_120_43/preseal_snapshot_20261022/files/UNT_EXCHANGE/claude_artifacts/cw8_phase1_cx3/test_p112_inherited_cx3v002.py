"""P112 registry integration from synthetic saved records; no child is launched."""

import _strptime
import shlex
import ast
import collections
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import traceback
import textwrap
import types

HERE = Path(__file__).resolve().parent
ART = HERE.parent
BUILDER = HERE / 'roster_builder_c2v007_cx3cw8v002.py'
BUILDER_SHA = 'a2d8dc00fd80322a2ba6822648c7399d46e9a4e55bbf309cd2efbc0e33665e7e'
P112 = HERE / 'phase1_ngc_launch_cx3cw8v002.py'
P112_SHA = '6de0d06a16a5ffab7b49bc76bc9219d0bfbd67a91020129677a5f4078846f852'
P112_TEST = ART / 'phase1_ngc_launch_kit_cx2v003/test_phase1_ngc_launch_cx2v003.py'
TEST_SHA = 'a3cdbdc661b69bd8830ea0b0f68e02674b5319064c7fb8c7060928d971c73f49'
WORK = Path(sys.argv[1]).resolve()
WORK.mkdir()
READS = []


def load(path, digest, name):
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == digest
    mod = types.ModuleType(name)
    mod.__file__ = str(path)
    exec(compile(raw, str(path), 'exec'), mod.__dict__)
    return mod


source_raw = P112_TEST.read_bytes()
assert hashlib.sha256(source_raw).hexdigest() == TEST_SHA
source = source_raw.decode()
tree = ast.parse(source)
names = {'hash_bytes', 'error_text', 'exclusive', 'Suite', 'receipt_fixture'}
segments = {n.name: ast.get_source_segment(source, n) for n in tree.body
            if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names}
fixture = segments['receipt_fixture'].replace(
    'sample=None, ram=None, receipt_changes=None):',
    'sample=None, ram=None, receipt_changes=None, no_outdir=False):')
start = fixture.index('    monitor = M.load_verified')
end = fixture.index('    if receipt_changes is not None:', start)
fixture = fixture[:start] + '''
    # A saved, synthetic monitor receipt. No monitor or driver is invoked.
    result_pin = None
    if not no_outdir:
        Path(outdir).mkdir()
        result_pin = suite.raw_write(Path(outdir) / "result.json", M.encoded({
            "synthetic": True, "status": mode, "valid": mode == "COMPLETED"}))
    pins = {"driver": driver, "monitor": M.REAL["monitor"], "spec": spec}
    rec = {"schema": M.MONITOR_SCHEMA, "utc_start": "2026-01-01T00:00:02Z",
           "utc_end": "2026-01-01T00:00:04Z", "pins": pins, "caps": M.first_caps(name),
           "child_pid": 900004, "status": "FINISHED" if mode == "COMPLETED" else "CHILD_FAILED", "driver_status": mode,
           "exit_code": 0, "result": result_pin}
    rec["receipt_sha256"] = M.sha(M.canonical(rec))
    raw_receipt = str(root / "raw_monitor.receipt.json")
    suite.raw_write(Path(raw_receipt), M.encoded(rec))
    lj = {"schema": "UNT_ROOT_MONITOR_LAUNCH_C2V001", "utc": "2026-01-01T00:00:02Z",
          "child_pid": 900004, "pins": pins, "caps": M.first_caps(name),
          "outdir": outdir}
    suite.raw_write(Path(raw_receipt + ".launch.json"), M.encoded(lj))
''' + fixture[end:]
needle = '             "name": name, "spec": registered_spec, "point_key": call["point_key"], "theta_key": call["point_key"],'
assert fixture.count(needle) == 1
fixture = fixture.replace(needle, needle + '''
             "kind": call["kind"], "alternative": call["alternative"], "key": call["key"],''')
module = types.ModuleType('saved_p112_fixture')
module.__dict__.update({
    'Path': Path, 'types': types, 'hashlib': hashlib, 'json': json, 'os': os,
    'traceback': traceback, 'SYNTHETIC_DRIVER': '# inert synthetic source; never run\\n',
})
for name in ('hash_bytes', 'error_text', 'exclusive', 'Suite'):
    exec(compile(segments[name], str(P112_TEST) + ':' + name, 'exec'), module.__dict__)
fixture = fixture.replace('P112_LAUNCHER_CX2V003', 'P112_LAUNCHER_CX3CW8V002')
fixture = fixture.replace('            text = ', "            self.cfg.update(phase1_ceiling_utc=M.PHASE1_CEILING_UTC, phase2_ceiling_utc=M.PHASE2_CEILING_UTC, cause_records=[], root_stop_records=[])\n            text = " )
fixture = fixture.replace('\"exit_code\": 0, \"result\": result_pin', '\"exit_code\": 0 if mode == \"COMPLETED\" else 1, \"result\": result_pin')
fixture = fixture.replace('\"spec\": registered_spec, \"origin\": origin,', '\"spec\": registered_spec, \"spec_doc\": M.read_pin(registered_spec), \"origin\": origin,')
exec(compile(fixture, str(P112_TEST) + ':saved_fixture', 'exec'), module.__dict__)
rf = fixture.replace('def receipt_fixture(', 'def receipt_fixture_for_resume(')
rf = rf.replace('no_outdir=False):', 'no_outdir=False, saved_caps=None):')
rf = rf.replace('M.first_caps(name)', '(dict(saved_caps) if saved_caps is not None else M.first_caps(name))')
rf = rf.replace('2026-01-01T00:00:02Z', '2026-11-01T00:00:12Z').replace('2026-01-01T00:00:04Z', '2026-11-01T00:00:14Z')
rf = rf.replace('"schema": "UNT_ROOT_MONITOR_LAUNCH_C2V001",', '"schema": M.MONITOR_SCHEMA + "_LAUNCH", "command": M.driver_command(pins, spec, outdir), "retries_allowed": 0,')
exec(compile(rf, str(P112_TEST) + ':saved_resume_fixture', 'exec'), module.__dict__)

suite = module.Suite(P112, WORK / 'fixtures', P112_SHA)
M = suite.module

MUTATIONS = {'root_stop_ignored': [("if current.get('_known_nonphysics'):", 'if False:')], 'stage_identity_ignored': [("fields = ('status', 'failing_stage', 'failure_code', 'exception_class', 'raise_site')", "fields = ('status', 'failure_code', 'exception_class', 'raise_site')")], 'class_identity_ignored': [("fields = ('status', 'failing_stage', 'failure_code', 'exception_class', 'raise_site')", "fields = ('status', 'failing_stage', 'failure_code', 'raise_site')")], 'site_identity_ignored': [("fields = ('status', 'failing_stage', 'failure_code', 'exception_class', 'raise_site')", "fields = ('status', 'failing_stage', 'failure_code', 'exception_class')")], 'hold_fix_removed': [("need(not held_for_fix(actual) or root_hold_release, 'HELD_FOR_FIX')", "need(True, 'HELD_FOR_FIX')")], 'hold_cause_removed': [("need(not held_for_cause(actual, authenticated_causes), 'HELD_FOR_CAUSE')", "need(True, 'HELD_FOR_CAUSE')")], 'output_not_doubled': [("caps['output_cap_bytes'] *= 2", "caps['output_cap_bytes'] *= 1")], 'wrong_phase_wall': [('wall = remaining_wall(monitor_ceiling_utc, now_utc)', 'wall = remaining_wall(phase_ceiling_utc, now_utc)')], 'twin_wrong_rss': [("caps['rss_cap_bytes'] = RAM * (11 if name == TWIN else 1)", "caps['rss_cap_bytes'] = RAM")], 'phase1_admission_ignored': [('    remaining_wall(phase_ceiling_utc, now_utc)', '    # mutant ignores phase admission boundary')], 'late_finish_retroactive': [("eligible = [r for r in actual if timestamp(r['time_utc'], whole=True) <= cutoff]", 'eligible = list(actual)')], 'solo_ignored': [("        if any(r.get('solo_mode') is not True or type(r.get('other_ngc_processes_max')) is not int", "        if any(False or type(r.get('other_ngc_processes_max')) is not int")], 'cause_result_binding_ignored': [("need(is_pin(monitor.get('result')) and bindings['result'] == monitor['result']['sha256'],", 'need(True,')], 'closed_projection_ignored': [("need(all(obj.get(key) == value and type(obj.get(key)) is type(value)\n             for key, value in expected.items()), 'ATTEMPT_PROJECTION_MISMATCH')", "need(True, 'ATTEMPT_PROJECTION_MISMATCH')")]}
MUTATION = sys.argv[2] if len(sys.argv)>2 else None
MUTATED_SHA = None
if MUTATION:
    changed=P112.read_text()
    for before,after in MUTATIONS[MUTATION]:
        assert changed.count(before)==1,(MUTATION,before,changed.count(before))
        changed=changed.replace(before,after)
    MUTATED_SHA=hashlib.sha256(changed.encode()).hexdigest()
    exec(compile(changed,str(P112)+":mutant:"+MUTATION,"exec"),M.__dict__)


def audit(event, args):
    if event in ('os.rename', 'os.remove', 'os.rmdir'):
        raise AssertionError('IMMUTABILITY_FENCE: ' + event)
    if event == 'open' and isinstance(args[0], (str, bytes, os.PathLike)):
        flags = args[2]
        if isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR) and os.path.lexists(args[0]):
            raise AssertionError('IMMUTABILITY_FENCE: existing-file write')
    if event == 'subprocess.Popen':
        argv = args[1]
        if argv != ['/bin/date', '-u']:
            raise AssertionError('PROCESS_FENCE: ' + repr(argv))
    if event != 'open' or not isinstance(args[0], (str, bytes, os.PathLike)):
        return
    real = os.path.realpath(os.fsdecode(args[0]))
    allowed = {str(BUILDER), str(P112), str(Path(__file__).resolve())}
    if real != str(WORK) and real not in allowed and not real.startswith(str(WORK) + os.sep):
        raise AssertionError('READ_FENCE: ' + real)
    flags = args[2]
    if not isinstance(flags, int) or not flags & (os.O_WRONLY | os.O_RDWR):
        if not os.path.isdir(real):
            if Path(real).name in ("result.json", "finish.json"):
                raise AssertionError("RUN_CONTENT_FENCE: " + real)
            READS.append(real)


sys.addaudithook(audit)

CASES = []
NOW = '2026-11-01T00:00:00Z'

def case(name, fn, expected=None):
    CASES.append((name,fn,expected))

def prepared(label, **kw):
    f=module.receipt_fixture(suite,label,**kw)
    f.ctx.system.utc=lambda:NOW
    f.closed=M.close_attempt(f.ctx,f.name,1)
    return f

def actual(f):
    return M.history(f.ctx,f.call,inspect_next=False)['actual']

def honest():
    f=prepared('honest')
    start=len(READS)
    h=M.history(f.ctx,f.call,inspect_next=False)
    counts=collections.Counter(READS[start:])
    assert counts and max(counts.values())==1, counts
    assert len(h['actual'])==1 and not h['pending']
    assert M.status(f.ctx)['calls'][0]['status']=='TERMINAL'
    return True
case('saved_close_history_status_single_read',honest)

def pending(label, now, live=False):
    f=module.receipt_fixture(suite,label,no_receipt=True)
    f.ctx.system.utc=lambda:now
    if live:
        import shlex
        f.ctx.system.rows=[{'pid':900001,'ppid':1,'command':shlex.join(M.record_monitor_argv(f.record))}]
    result=M.status(f.ctx)
    assert result['stop_requested'] is False
    return result['calls'][0]
case('active_at_phase1_is_incomplete_no_stop',lambda:pending('active_ceiling',M.PHASE1_CEILING_UTC,True)['status']=='UNEVALUATED_SCHEDULE_CEILING')
case('missing_receipt_at_phase1_is_incomplete_no_stop',lambda:pending('missing_ceiling',M.PHASE1_CEILING_UTC)['status']=='UNEVALUATED_SCHEDULE_CEILING')
case('active_before_phase1_remains_active',lambda:pending('active_before',NOW,True)['status']=='ATTEMPT_ACTIVE')
case('missing_receipt_before_phase1_remains_problem',lambda:pending('missing_before',NOW)['status']=='MONITOR_ENDED_NO_RECEIPT')

def policy_row(k=1,**changes):
    monitor_pin={'path':'/synthetic/monitor_%d.json'%k,'sha256':M.sha(str(k).encode())}
    mon={'status':'CHILD_FAILED','driver_status':'ROUTE_A_NO_FIXED_POINT','exit_code':1,
         'pins':{'spec':{'path':'/synthetic/spec.json','sha256':'a'*64},'driver':{'path':'/synthetic/driver.py','sha256':'b'*64}},
         'result':{'path':'/forbidden/NGC3198_run/result.json','sha256':M.sha(('result%d'%k).encode())}}
    obj={'attempt':k,'status_class':'FAILED','raw_status':'CHILD_FAILED|ROUTE_A_NO_FIXED_POINT',
         'spec_sha256':'a'*64,'solo_mode':True,'other_ngc_processes_max':0,'host_ram_bytes':M.RAM,
         'rss_cap_bytes':M.RAM,'wall_cap_s':17,'output_cap_bytes':1000,'time_utc':'2026-10-31T00:00:%02dZ'%k,
         'pins':{'monitor_receipt':monitor_pin,'stop_record':None},'_verified_monitor':mon,'_known_nonphysics':False,
         'receipt_pin':{'path':'/synthetic/closed_%d.json'%k,'sha256':M.sha(('closed%d'%k).encode())}}
    obj.update(changes);return obj

def proof(r,**changes):
    c={'status':'ROUTE_A_NO_FIXED_POINT','failing_stage':'03_route_a','failure_code':'ROUTE_A_NO_FIXED_POINT',
       'exception_class':'CLASS_SET:["NO_EXCEPTION_OUTCOME","RouteANoFixedPoint"]',
       'raise_site':'SITE_SET:["/synthetic/driver.py:100","/synthetic/module.py:12"]',
       'bound_shas':{'receipt':r['pins']['monitor_receipt']['sha256'],
         'result':r['_verified_monitor']['result']['sha256'],'finish':M.sha(('finish%d'%r['attempt']).encode()),
         'spec':r['spec_sha256'],'driver':r['_verified_monitor']['pins']['driver']['sha256']},
       'model_outcome':True,'model_outcome_reason':'A252_NONEMPTY_ALL_MODEL_PINNED_SITE_SET_AND_BOUND_METADATA'}
    c.update(changes);return c

N=0
def mapped(rows, changes=None):
    global N
    N+=1
    root=WORK/('causes_%03d'%N);root.mkdir()
    pins=[]
    for i,r in enumerate(rows):
        c=proof(r)
        if changes: changes(c,i)
        pins.append(suite.raw_write(root/('%d.json'%i),M.encoded(c)))
    ctx=types.SimpleNamespace(cfg={'cause_records':pins})
    return ctx

@M.read_scope
def authenticate(ctx,rows):
    return M.authenticated_causes(ctx,rows)

rows=[policy_row(1),policy_row(2)]
def pair(changes=None,alter_rows=None):
    r=copy.deepcopy(rows)
    if alter_rows:alter_rows(r)
    ctx=mapped(r,changes)
    start=len(READS)
    causes=authenticate(ctx,r)
    counts=collections.Counter(READS[start:])
    assert max(counts.values(),default=0)<=1
    return M.terminal_prefix(r,'P1_M0001',causes)
case('A252_site_set_pair_counts_without_following_any_run_path',lambda:pair()['disposition']=='RULE_C_INVALID')
case('clean_exhaustion_pair_counts',lambda:pair(lambda c,i:c.update(failure_code='ITERATION_BUDGET_EXHAUSTED'))['disposition']=='RULE_C_INVALID')
for field in ['failing_stage','failure_code','exception_class','raise_site']:
    case('different_'+field+'_does_not_count',lambda field=field:pair(lambda c,i:c.update({field:('ITERATION_BUDGET_EXHAUSTED' if field=='failure_code' else c[field]+'X')}) if i else None) is None)
for field in ['receipt','result','finish','spec','driver']:
    if field=='receipt':
        # An unmatched cause stays unavailable and cannot count.
        case('unmatched_cause_receipt',lambda:pair(lambda c,i:c['bound_shas'].update(receipt='f'*64) if i else None) is None)
    else:
        code='CAUSE_SCIENCE_BINDING' if field in ('spec','driver') else 'CAUSE_RESULT_BINDING' if field=='result' else 'CAUSE_BOUND_SHA_MISSING'
        case('wrong_bound_'+field,lambda field=field:pair(lambda c,i:c['bound_shas'].update({field:None if field=='finish' else 'f'*64}) if i else None),code)
case('same_monitor_cannot_be_pair',lambda:pair(alter_rows=lambda r:r[1]['pins'].update(monitor_receipt=r[0]['pins']['monitor_receipt'])), 'CAUSE_RECEIPT_NOT_UNIQUE')
for field,value in [('solo_mode',False),('other_ngc_processes_max',1),('other_ngc_processes_max',None),('rss_cap_bytes',M.RAM-1),('_known_nonphysics',True)]:
    case('pair_evidence_'+field+'_'+str(value),lambda f=field,v=value:pair(alter_rows=lambda r:r[1].update({f:v})) is None)
case('generic_failure_code_refused',lambda:pair(lambda c,i:c.update(failure_code='ValueError')), 'CAUSE_MODEL_IDENTITY')
case('unknown_cause_is_not_counted',lambda:pair(lambda c,i:c.update(model_outcome=False,model_outcome_reason='METADATA_REFUSED')) is None)

def next_for(r,causes=None):
    records=[{'attempt':x['attempt'],'origin':'P112','outcome':'LAUNCH'} for x in r]
    return M.next_attempt('P1_M0001',records,r,set(),phase_ceiling_utc=M.PHASE1_CEILING_UTC,
        monitor_ceiling_utc=M.PHASE2_CEILING_UTC,now_utc=NOW,authenticated_causes=causes)
case('unknown_repeated_solo_is_held',lambda:next_for(rows),'HELD_FOR_CAUSE')
case('unknown_first_is_solo_retry',lambda:next_for(rows[:1])['solo_mode'] is True)
case('no_doubled_wall_check',lambda:pair()['counted_attempts']==[0,1])
for cls,raw in [('CAP','STOPPED_WALL_CAP|NONE'),('CAP','STOPPED_RSS_CAP|NONE'),('OUTPUT_CAP','STOPPED_OUTPUT_CAP|NONE'),('INFRA','CHILD_FAILED|NONE|SIGNAL')]:
    rr=[policy_row(k,status_class=cls,raw_status=raw,_known_nonphysics=True) for k in (1,2,3)]
    case('nonphysics_no_terminal_'+raw,lambda r=rr:M.terminal_prefix(r,'P1_M0001') is None)
    case('nonphysics_retry_'+raw,lambda r=rr:next_for(r)['attempt']==4)
    if cls=='OUTPUT_CAP':case('output_doubles_previous',lambda r=rr:next_for(r)['caps']['output_cap_bytes']==2000)
for raw in ['CHILD_FAILED|REFUSED','CHILD_FAILED|BLOCKED']:
    rr=[policy_row(k,status_class='INFRA',raw_status=raw,_known_nonphysics=True) for k in (1,2)]
    case('repeat_hold_'+raw,lambda r=rr:next_for(r),'HELD_FOR_FIX')


def projection(change):
    f=prepared('projection_%03d'%len(list((WORK/'fixtures').iterdir())))
    h=M.history(f.ctx,f.call,inspect_next=False)
    r=h['actual'][0];obj={k:v for k,v in r.items() if not k.startswith('_') and k!='receipt_pin'}
    obj=copy.deepcopy(obj);change(obj)
    @M.read_scope
    def check():
        rec=f.ctx.records(f.name)[0]
        return M.verify_closed_receipt(f.ctx,f.call,rec,r['pins']['monitor_receipt'],r['_verified_monitor'],r['receipt_pin'],obj)
    return check()
for key,value in [('raw_status','CHILD_FAILED|FAILED'),('status_class','FAILED'),('solo_mode',True),('counted_rerun',True),('other_ngc_processes_max',0),('wall_cap_s',1),('rss_cap_bytes',1),('host_ram_bytes',1),('time_utc','2026-01-01T00:00:05Z')]:
    case('closed_projection_'+key,lambda k=key,v=value:projection(lambda o:o.update({k:v})),'ATTEMPT_PROJECTION_MISMATCH')
for key in ['monitor_receipt','launch_json','launch_record','solo_sample','stop_record','result','status_map_sha256']:
    case('closed_source_'+key,lambda k=key:projection(lambda o:o['pins'].update({k:'tampered'})),'ATTEMPT_SOURCE_BINDING')

def root_stopped():
    f=module.receipt_fixture(suite,'root_stopped')
    f.ctx.system.utc=lambda:NOW
    reg=suite.raw_write(f.root/'stop_registration.md',b'root synthetic stop declaration')
    doc={'schema':'ROOT_NONPHYSICS_STOP_C2V001','date_u':'2026-01-01T00:00:03Z',
         'call':{k:f.call[k] for k in ('name','kind','alternative','key')},
         'launch_json':f.launch_pin,'registration':reg}
    pin=suite.raw_write(f.root/'root_stop.json',M.encoded(doc));f.ctx.cfg['root_stop_records']=[pin]
    f.closed=M.close_attempt(f.ctx,f.name,1)
    r=actual(f)[0]
    assert r['_known_nonphysics'] is True and r['_root_stop']==pin
    assert M.terminal_prefix([r],f.name) is None
    return M.status(f.ctx)['calls'][0]['status']=='READY'
case('root_stop_preempts_natural_finished',root_stopped)

for end in [-9,137,143]:
    case('monitor_signal_'+str(end),lambda end=end:pair(alter_rows=lambda r:r[1]['_verified_monitor'].update(exit_code=end)), 'CAUSE_NONPHYSICS_END')
case('monitor_stop_reason',lambda:pair(alter_rows=lambda r:r[1]['_verified_monitor'].update(stop_reason='operator')),'CAUSE_NONPHYSICS_END')

def known_false():
    ctx=mapped(rows,lambda c,i:c.update(model_outcome=False,model_outcome_reason='SIGNAL_KILLED_STAGE'))
    return next_for(rows,authenticate(ctx,rows))['attempt']==3
case('authenticated_nonphysics_generic_FAILED_is_retried',known_false)
case('unlimited_nonphysics_attempts',lambda:next_for([policy_row(59,status_class='CAP',raw_status='STOPPED_RSS_CAP|NONE',_known_nonphysics=True,attempt=1000000)])['attempt']==1000001)
case('wall_uses_phase2',lambda:next_for(rows[:1])['caps']['wall_cap_s']==int(M.timestamp(M.PHASE2_CEILING_UTC)-M.timestamp(NOW)))
case('correct_ceiling_config',lambda:M.validate_policy_config(dict(phase1_ceiling_utc=M.PHASE1_CEILING_UTC,phase2_ceiling_utc=M.PHASE2_CEILING_UTC,cause_records=[],root_stop_records=[])))
case('wrong_ceiling_config_refuses',lambda:M.validate_policy_config(dict(phase1_ceiling_utc=M.PHASE2_CEILING_UTC,phase2_ceiling_utc=M.PHASE2_CEILING_UTC,cause_records=[],root_stop_records=[])),'PHASE_CEILING_CONFIG')


def saved_sampler():
    f=module.receipt_fixture(suite,'saved_sampler')
    ctx=f.ctx
    work=Path(ctx.cfg['p112_launch_root'])/'work'/'P1_M0001_A1_saved'
    work.mkdir()
    spec=f.call['spec']
    caps=dict(M.first_caps(f.name),wall_cap_s=M.remaining_wall(M.PHASE2_CEILING_UTC,NOW))
    plan={'schema':'UNT_P112_LAUNCH_PLAN_CX2V001','name':f.name,'attempt':1,
          'config':ctx.config_pin,'work':str(work),'spec':spec,'pins':{k:ctx.pins[k] for k in ('driver','monitor')},
          'outdir':f.outdir,'caps':caps,'caps_basis':{'rule':'bootstrap'},'invocation_utc':NOW,
          'date_u':M.date_u(),'solo_mode':False,'monitor_argv':M.monitor_command(ctx.pins,spec,f.outdir,caps)}
    bootstrap_pin=ctx.write(str(work/'plan.json'),plan)
    final,final_pin=M.write_launch_commit(ctx,plan,bootstrap_pin,work,'2026-11-01T00:00:10Z')
    ctx.write(str(work/'monitor_pid.json'),{'schema':'P112_MONITOR_PID_CX2V001','monitor_pid':900001,'plan':final_pin,'date_u':M.date_u()})
    ticks=[0.0]
    ctx.system.monotonic=lambda:ticks[0]
    ctx.system.sleep=lambda seconds:ticks.__setitem__(0,ticks[0]+seconds)
    start=len(READS)
    result=M.sampler(ctx,plan,work)
    counts=collections.Counter(READS[start:])
    assert max(counts.values(),default=0)==1,counts
    data=json.loads(Path(result['path']).read_bytes())
    assert data['n_samples']==2 and data['complete'] is True
    assert str(work/'launch_plan.json') in counts and str(work/'LAUNCH_COMMIT.json') in counts
    return True
case('real_sampler_control_flow_saved_records_final_commit_single_read',saved_sampler)
case('twin_retry_rss_is_eleven_RAM',lambda:M.next_attempt(M.TWIN,[{'attempt':1,'origin':'P112','outcome':'LAUNCH'}],
    [policy_row(1,status_class='CAP',raw_status='STOPPED_RSS_CAP|NONE',_known_nonphysics=True)],set(),
    phase_ceiling_utc=M.PHASE1_CEILING_UTC,monitor_ceiling_utc=M.PHASE2_CEILING_UTC,now_utc=NOW)['caps']['rss_cap_bytes']==11*M.RAM)
case('phase1_boundary_allows_new_admission',lambda:M.next_attempt('P1_M0001',[],[],set(),phase_ceiling_utc=M.PHASE1_CEILING_UTC,monitor_ceiling_utc=M.PHASE2_CEILING_UTC,now_utc=M.PHASE1_CEILING_UTC)['attempt']==1)
case('late_finish_never_retroactive',lambda:M.phase_disposition([policy_row(1,status_class='FINISHED',raw_status='FINISHED|COMPLETED',time_utc='2026-11-07T00:00:00Z')],'P1_M0001',M.PHASE1_CEILING_UTC,'2026-11-08T00:00:00Z')['status']=='UNEVALUATED_SCHEDULE_CEILING')


def refreshed_clock():
    f=module.receipt_fixture(suite,'refreshed_clock',no_receipt=True)
    clock=[NOW];f.ctx.system.utc=lambda:clock[0]
    assert M.status(f.ctx)['calls'][0]['status']=='MONITOR_ENDED_NO_RECEIPT'
    clock[0]=M.PHASE1_CEILING_UTC
    return M.status(f.ctx)['calls'][0]['status']=='UNEVALUATED_SCHEDULE_CEILING'
case('each_public_status_refreshes_clock',refreshed_clock)
case('cap_without_private_flag_still_never_counts',lambda:M.terminal_prefix([policy_row(1,status_class='CAP',raw_status='STOPPED_RSS_CAP|NONE'),policy_row(2,status_class='CAP',raw_status='STOPPED_RSS_CAP|NONE')],'P1_M0001') is None)


def resume_saved(label, *, wrong_invocation=False, alive=False, reused=False, missing_monitor=False):
    final_caps=dict(M.first_caps('P1_M0001'),wall_cap_s=M.remaining_wall(M.PHASE2_CEILING_UTC,'2026-11-01T00:00:10Z'))
    f=module.receipt_fixture_for_resume(suite,label,record=False,saved_caps=final_caps)
    ctx=f.ctx;ctx.system.utc=lambda:NOW
    work=Path(ctx.cfg['p112_launch_root'])/'work'/(f.name+'_A1_SAVED')
    work.mkdir()
    m15={'schema':'UNT_M15_PRELAUNCH_RECORD_C2V001','date_u':M.date_u(),
         'date_u_epoch_s':int(M.timestamp('2026-11-01T00:00:00Z'))}
    m15_pin=suite.raw_write(work/'m15_fixture.json',M.encoded(m15))
    caps=dict(final_caps,wall_cap_s=final_caps['wall_cap_s']+10)
    plan={'schema':'UNT_P112_LAUNCH_PLAN_CX2V001','name':f.name,'attempt':1,
          'config':ctx.config_pin,'work':str(work),'spec':f.call['spec'],
          'pins':{k:ctx.pins[k] for k in ('driver','monitor')},
          'outdir':f.outdir,'receipt':f.outdir+'.receipt.json','launch_json':f.outdir+'.receipt.json.launch.json',
          'caps':caps,'caps_basis':{'rule':'bootstrap'},'invocation_utc':NOW,'date_u':M.date_u(),
          'solo_mode':False,'counted_rerun':False,'rule_c_basis':[],'host_ram_bytes':M.RAM,'m15_record':m15_pin,
          'monitor_argv':M.monitor_command(ctx.pins,f.call['spec'],f.outdir,caps)}
    bootstrap_pin=ctx.write(str(work/'plan.json'),plan)
    final,pin=M.write_launch_commit(ctx,plan,bootstrap_pin,work,'2026-11-01T00:00:10Z')
    command=M.PY+' -I -B '+str(P112)+' launch --name '+f.name
    invocation={'schema':'P112_INVOCATION_CX2V001','invocation_pid':900004,'invocation_command':command,
                'sampler_pid':900002,'planned_monitor_argv':final['monitor_argv'],
                'plan':bootstrap_pin if wrong_invocation else pin,'date_u':M.date_u()}
    ctx.write(str(work/'invocation.json'),invocation)
    if not missing_monitor:
        ctx.write(str(work/'monitor_pid.json'),{'schema':'P112_MONITOR_PID_CX2V001','monitor_pid':900001,'plan':pin,'date_u':M.date_u()})
    if alive or reused:
        ctx.system.rows=[{'pid':900004,'ppid':1,'pgid':900004,'command':'/bin/sleep 60' if reused else command}]
    start=len(READS)
    result=M.launch_resume(ctx,f.name,1)
    counts=collections.Counter(READS[start:]);assert max(counts.values())==1,counts
    record=M.read_pin(result)
    assert record['outcome']=='LAUNCH' and record['plan']==pin and record['caps']==final_caps
    closed=M.close_attempt(ctx,f.name,1)
    assert closed['status_class']=='FINISHED'
    return True
case('resume_uses_committed_plan_and_closes',lambda:resume_saved('resume_committed'))
case('resume_without_pid_uses_final_argv',lambda:resume_saved('resume_no_pid',missing_monitor=True))
case('resume_reused_invocation_pid_is_safe',lambda:resume_saved('resume_reused',reused=True))
case('resume_wrong_invocation_plan_refuses',lambda:resume_saved('resume_bad_inv',wrong_invocation=True),'RESUME_PLAN_BINDING')
case('resume_live_invocation_refuses',lambda:resume_saved('resume_alive',alive=True),'RESUME_INVOCATION_ALIVE')

results=[]
for name,fn,expected in CASES:
    observed='RETURNED';passed=False
    try:
        value=fn();passed=expected is None and value is not False
    except M.Refusal as e:
        observed=e.code;passed=e.code==expected
    except Exception as e:
        observed=repr(e);detail=traceback.format_exc(limit=4)
    row={'id':name,'expected':expected,'observed':observed,'verdict':'PASS' if passed else 'FAIL'}
    results.append(row)
    if not passed:print(json.dumps(row))
record={'date_u':M.date_u(),'scope':'TESTED static/saved synthetic records; no child launch or run content reads',
        'tool':{'path':str(P112),'sha256':P112_SHA},'mutation':MUTATION,'mutated_sha256':MUTATED_SHA,'n_cases':len(results),
        'n_pass':sum(r['verdict']=='PASS' for r in results),'cases':results}
with (WORK/'TEST_RECORD.json').open('xb') as f:f.write(M.encoded(record))
print('%d/%d PASS'%(record['n_pass'],record['n_cases']))
raise SystemExit(0 if record['n_pass']==record['n_cases'] else 1)

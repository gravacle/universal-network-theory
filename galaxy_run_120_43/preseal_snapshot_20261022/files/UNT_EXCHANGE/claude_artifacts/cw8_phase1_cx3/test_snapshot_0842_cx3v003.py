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
BUILDER = HERE / 'roster_builder_c2v007_cx3cw8v003.py'
BUILDER_SHA = 'f710334b6f5ec2663fbebd826c7b326ebf7ff9eb600e751584de4f518a4e0b11'
P112 = HERE / 'phase1_ngc_launch_cx3cw8v003.py'
P112_SHA = '4d5b47e75f90241460dd0b86155ddae2267117c31f6043fc57777ea94564919d'
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


rb = load(BUILDER, BUILDER_SHA, 'snapshot_builder')
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
fixture = fixture.replace('P112_LAUNCHER_CX2V003', 'P112_LAUNCHER_CX3CW8V003')
fixture = fixture.replace('            text = ', "            self.cfg.update(phase1_ceiling_utc=M.PHASE1_CEILING_UTC, phase2_ceiling_utc=M.PHASE2_CEILING_UTC, cause_records=[], root_stop_records=[])\n            text = " )
fixture = fixture.replace('\"exit_code\": 0, \"result\": result_pin', '\"exit_code\": 0 if mode == \"COMPLETED\" else 1, \"result\": result_pin')
fixture = fixture.replace('"spec": registered_spec, "origin": origin,',
    '"spec": registered_spec, "spec_doc": M.read_pin(registered_spec), "origin": origin,')
fixture = fixture.replace('    if record:\n',
    '    if sample is not None: record_doc["solo_mode"] = True\n    if record:\n')
exec(compile(fixture, str(P112_TEST) + ':saved_fixture', 'exec'), module.__dict__)
rf = fixture.replace('def receipt_fixture(', 'def receipt_fixture_for_resume(')
rf = rf.replace('no_outdir=False):', 'no_outdir=False, saved_caps=None):')
rf = rf.replace('M.first_caps(name)', '(dict(saved_caps) if saved_caps is not None else M.first_caps(name))')
rf = rf.replace('2026-01-01T00:00:02Z', '2026-11-01T00:00:12Z').replace('2026-01-01T00:00:04Z', '2026-11-01T00:00:14Z')
rf = rf.replace('"schema": "UNT_ROOT_MONITOR_LAUNCH_C2V001",', '"schema": M.MONITOR_SCHEMA + "_LAUNCH", "command": M.driver_command(pins, spec, outdir), "retries_allowed": 0,')
exec(compile(rf, str(P112_TEST) + ':saved_resume_fixture', 'exec'), module.__dict__)

suite = module.Suite(P112, WORK / 'fixtures', P112_SHA)
M = suite.module


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


CASES=[]
def case(name,fn,expected=None):CASES.append((name,fn,expected))

def fixture(label, *, state='finished', now='2026-11-06T05:59:00Z', **kwargs):
    f=module.receipt_fixture(suite,label,no_receipt=state=='pending',**kwargs)
    if state in ('finished','mixed'):M.close_attempt(f.ctx,f.name,1)
    if state=='never':
        f.ctx._fixture_calls=[dict(f.call,name='P1_M0002',key='M001',theta_sha256='d'*64)]
    if state=='mixed':
        f.ctx._fixture_calls.append(dict(f.call,name='P1_M0002',key='M001',theta_sha256='d'*64))
    p=f.root/'deadline.json'
    registration={'schema':'SCHEDULE_CEILING_REGISTRATION_C2V001','phase':'PHASE_1',
        'deadline_utc':M.PHASE1_CEILING_UTC,'date_u':'2026-01-01T00:00:00Z'}
    deadline=suite.raw_write(p,M.encoded(registration))
    policy={'schema':'INTERRUPTION_POLICY_C2V002','phase':'PHASE_1','cause_producer':None,
        'deadline_utc':M.PHASE1_CEILING_UTC,'deadline_registration':deadline,'attempts':[],'closures':[]}
    pp=suite.raw_write(f.root/'policy.json',M.encoded(policy))
    def factory(m,pin):
        assert pin==f.ctx.config_pin
        # Virtual runtime clock for synthetic snapshot dates, not the report date.
        m.date_u=lambda:m.dt.datetime.fromtimestamp(m.timestamp(now),m.dt.timezone.utc).strftime('%a %b %d %H:%M:%S UTC %Y')
        class ReadContext(m.Context):
            def __init__(self):
                self.__dict__.update(f.ctx.__dict__)
                self.v006_raw=m.read_v006(self.cfg['v006'])
                self.v006_text=self.v006_raw.decode()
                self.system=m.SyntheticSystem({'mount_points':[str(f.root/'volume'),str(f.root/'kit_volume')],
                    'free_bytes':1<<50,'host_ram_bytes':m.RAM})
                self.system.processes=lambda:[]
                self.system.utc=lambda:now
            def calls(self):return self._fixture_calls
            def kit_entries(self):return self._fixture_kit
            def get_vpin(self,kind,name):return f.ctx.get_vpin(kind,name)
        return ReadContext()
    f.factory=factory
    f.input={'schema':'PHASE1_SNAPSHOT_INPUT_C2V007','launcher':{'path':str(P112),'sha256':P112_SHA},
        'config':f.ctx.config_pin,'interruption_policy':pp}
    f.out=f.root/'snapshot'
    return f

def create(f):
    old=rb._registry_context_factory;rb._registry_context_factory=f.factory
    try:return rb.phase1_snapshot(f.input,str(f.out))
    finally:rb._registry_context_factory=old

def verify(f,result):
    old=rb._registry_context_factory;rb._registry_context_factory=f.factory
    try:
        return rb.verify_phase1_snapshot(dict(launcher=f.input['launcher'],config=f.input['config'],snapshot=result['snapshot']),result['registry'],result['policy'])
    finally:rb._registry_context_factory=old

def normal(label,state,mode,T):
    f=fixture(label,state=state)
    start=len(READS);result=create(f);counts=collections.Counter(READS[start:])
    assert max(counts.values())==1,{p:n for p,n in counts.items() if n!=1}
    assert result['mode']==mode and rb.parse_utc_ns(result['T'],'T')==rb.parse_utc_ns(T,'T')
    start=len(READS);proof=verify(f,result);counts=collections.Counter(READS[start:])
    assert max(counts.values())==1,{p:n for p,n in counts.items() if n!=1}
    assert proof['verdict']=='BYTE_EQUAL' and proof['stop_requested'] is False
    return f,result,proof
case('all_terminal_before_ceiling',lambda:normal('all_terminal','finished','ALL_TERMINAL','2026-01-01T00:00:04Z'))
case('pending_at_ceiling',lambda:normal('pending','pending','CEILING',M.PHASE1_CEILING_UTC))
case('never_launched_at_ceiling',lambda:normal('never','never','CEILING',M.PHASE1_CEILING_UTC))
case('incomplete_before_ceiling_refuses',lambda:create(fixture('early',state='pending',now='2026-11-06T05:58:59Z')),'SNAPSHOT_BEFORE_CEILING')
case('unclosed_preceiling_receipt_refuses',lambda:create(fixture('needs_close',state='unclosed')),'SNAPSHOT_NEEDS_PRECEILING_CLOSE')


def rewrite_snapshot(f,result,change):
    doc=json.loads(Path(result['snapshot']['path']).read_bytes())
    change(doc)
    new_pin=suite.raw_write(f.root/'snapshot_successor.json',M.encoded(doc))
    return dict(result,snapshot=new_pin)

def altered(label,change,state='never'):
    f=fixture(label,state=state);result=create(f)
    return verify(f,rewrite_snapshot(f,result,change))

case('mixed_terminal_and_never',lambda:normal('mixed','mixed','CEILING',M.PHASE1_CEILING_UTC))

def before_ceiling_all_terminal():
    f=fixture('all_early',now='2026-01-02T00:00:00Z')
    result=create(f);proof=verify(f,result)
    assert result['mode']=='ALL_TERMINAL' and rb.parse_utc_ns(result['T'],'T')==rb.parse_utc_ns('2026-01-01T00:00:04Z','T')
    return proof['stop_requested'] is False
case('all_terminal_ordinary_freeze_before_ceiling',before_ceiling_all_terminal)

def late_finished():
    f=fixture('late_finished',now='2026-11-07T00:00:02Z',
        receipt_changes=lambda d:d.update(utc_end='2026-11-07T00:00:00Z'))
    result=create(f);proof=verify(f,result);row=proof['call_states'][0]
    assert result['mode']=='CEILING' and row['attempts']==[] and row['terminal'] is None
    assert rb.parse_utc_ns(result['T'],'T')==rb.parse_utc_ns(M.PHASE1_CEILING_UTC,'ceiling')
    assert len(row['after_ceiling_receipts'])==1
    closure=json.loads(Path(row['ceiling_closure']['path']).read_bytes())
    return closure['last_receipt'] is None
case('late_finish_never_retroactive',late_finished)

def future_files(state):
    f=fixture('future_'+state,state=state);result=create(f);before=verify(f,result)
    if state=='pending':
        paths=[Path(f.outdir+'.receipt.json'),Path(f.outdir+'.attempt_receipt.json')]
    else:
        call=f.ctx._fixture_calls[0]
        paths=[Path(M.own_registry_path(f.ctx,call['name'])),
               Path(M.planned_outdir(f.ctx,call['name'],1,'P112')+'.receipt.json')]
    for path in paths:suite.raw_write(path,b'FUTURE_PHASE2_UNPARSEABLE_OBSERVATION\n')
    start=len(READS);after=verify(f,result)
    assert before==after
    assert not set(map(str,paths)).intersection(READS[start:])
    return True
case('future_monitor_and_close_ignored',lambda:future_files('pending'))
case('future_registry_entry_and_receipt_ignored',lambda:future_files('never'))

def live_v006_changed():
    f=fixture('v006_changed',state='never');result=create(f)
    original=rb._p112_verifier_module
    def module_with_future_gate(pin):
        m=original(pin)
        def future_gate(path,kind='v006_gate'):
            raise AssertionError('LATER_LIVE_V006_READ')
        m.read_v006=future_gate
        return m
    rb._p112_verifier_module=module_with_future_gate
    try:return verify(f,result)['verdict']=='BYTE_EQUAL'
    finally:rb._p112_verifier_module=original
case('frozen_v006_wins_over_later_live_gate',live_v006_changed)

case('T_tamper_refused',lambda:altered('T_tamper',lambda d:d.update(T='2026-11-07T00:00:00Z')),'SNAPSHOT_T_NOT_REDERIVED')
case('mode_tamper_refused',lambda:altered('mode_tamper',lambda d:d.update(mode='ALL_TERMINAL')),'SNAPSHOT_T_NOT_REDERIVED')
case('created_before_ceiling_refused',lambda:altered('created_early',lambda d:d.update(created_utc='2026-11-06T05:58:59Z')),'SNAPSHOT_BEFORE_CEILING')
case('date_before_T_refused',lambda:altered('date_early',lambda d:d.update(date_u='2026-11-06T05:58:59Z')),'SNAPSHOT_T_NOT_REDERIVED')
case('stop_request_refused',lambda:altered('stop_flag',lambda d:d.update(stop_requested=True)),'SNAPSHOT_BINDING')
case('writer_pin_refused',lambda:altered('writer_pin',lambda d:d['writer'].update(sha256='0'*64)),'SNAPSHOT_WRITER_PIN')
case('missing_call_refused',lambda:altered('missing_call',lambda d:d.update(calls=[])),'SNAPSHOT_CALL_SET')
case('wrong_call_key_refused',lambda:altered('wrong_call',lambda d:d['calls'][0]['call'].update(key='M999')),'SNAPSHOT_CALL_BINDING')
case('wrong_terminal_refused',lambda:altered('wrong_term',lambda d:d['calls'][0].update(terminal={'forged':True})),'SNAPSHOT_TERMINAL_NOT_REDERIVED')
case('unknown_pending_refused',lambda:altered('unknown_pending',lambda d:d['calls'][0].update(pending_at_capture=[{'record':None,'status':'FAKE'}])),'SNAPSHOT_PENDING_BINDING')
case('wrong_sources_refused',lambda:altered('wrong_sources',lambda d:d.update(registry_sources=[{'path':'/synthetic','sha256':'0'*64}])),'SNAPSHOT_REGISTRY_SOURCES')
case('wrong_member_mapping_refused',lambda:altered('wrong_map',lambda d:d.update(s0_member_mappings=[{'fake':True}])),'SNAPSHOT_MEMBER_MAPPING')

def source_hash_change(d):
    # Choose a source not duplicated in the explicit output pins.
    for pin in d['sources']:
        if pin['path'].endswith('launch.json'):
            pin['sha256']='0'*64;return
    raise AssertionError('source witness missing')
case('captured_source_changed_refused',lambda:altered('wrong_source_hash',source_hash_change,state='finished'),'SNAPSHOT_SOURCE_PIN')

def closure_change(f,result,change):
    saved=json.loads(Path(result['snapshot']['path']).read_bytes())
    row=saved['calls'][0]
    closure=json.loads(Path(row['ceiling_closure']['path']).read_bytes())
    change(closure)
    cp=suite.raw_write(f.root/'closure_successor.json',M.encoded(closure))
    policy=json.loads(Path(result['policy']['path']).read_bytes())
    policy['closures']=[cp]
    pp=suite.raw_write(f.root/'policy_successor.json',M.encoded(policy))
    row['ceiling_closure']=cp;saved['interruption_policy']=pp
    sp=suite.raw_write(f.root/'snapshot_successor.json',M.encoded(saved))
    return verify(f,dict(result,policy=pp,snapshot=sp))

def wrong_last():
    f=fixture('wrong_last',state='never');result=create(f)
    return closure_change(f,result,lambda d:d.update(last_receipt=f.ctx.config_pin))
case('nullable_last_receipt_bound',wrong_last,'SNAPSHOT_CLOSURE_BINDING')

def kit_missing_entry():
    f=fixture('kit_entry',origin='KIT',name='S0_J0_SERIAL')
    result=create(f)
    return verify(f,rewrite_snapshot(f,result,lambda d:d['calls'][0].update(registry_entry=None)))
case('kit_entry_required',kit_missing_entry,'SNAPSHOT_ENTRY_BINDING')

def creator_error(kind):
    f=fixture('creator_error_'+kind,state='never')
    factory=f.factory
    def fail_factory(m,pin):
        ctx=factory(m,pin)
        if kind=='gate':
            def fail():raise m.Refusal('SYNTHETIC_GATE_REFUSED')
            ctx.gate=fail
        else:ctx.system.mounted=lambda path:False
        return ctx
    f.factory=fail_factory
    try:create(f)
    except Exception as e:
        assert isinstance(e,rb.Refused),type(e)
        raise
case('gate_refusal_normalized',lambda:creator_error('gate'),'SYNTHETIC_GATE_REFUSED')
case('mount_refusal_normalized',lambda:creator_error('mount'),'RUN_VOLUME_NOT_MOUNTED')

def verify_error():
    f=fixture('verify_error',state='never');result=create(f);factory=f.factory
    def fail_factory(m,pin):
        ctx=factory(m,pin);ctx.system.mounted=lambda path:False;return ctx
    f.factory=fail_factory
    try:verify(f,result)
    except Exception as e:
        assert isinstance(e,rb.Refused),type(e)
        raise
case('verify_mount_refusal_normalized',verify_error,'RUN_VOLUME_NOT_MOUNTED')

def zero_attempt_terminal():
    f=fixture('zero_terminal',state='never');result=create(f);proof=verify(f,result)
    cfg=rb._receipt_cfg(rb.EXACT_RECEIPT_KEYS,rb.STATUS_CLASSES)
    cfg['interruption_policy']=rb.interruption_policy(result['policy'],'PHASE_1')
    row=proof['call_states'][0]
    cfg['snapshot_call_states']={rb._call_key(row['call']):row}
    t=rb._terminal([],cfg,'never',False,row['call'])
    assert t['class']=='SCHEDULE_CEILING' and t['receipt'] is None and t['run_dir'] is None
    assert t['n_attempts']==0 and t['source_facts']==[]
    assert t['time_ns']==rb.parse_utc_ns(M.PHASE1_CEILING_UTC,'ceiling')
    return True
case('zero_attempt_terminal_no_fabrication',zero_attempt_terminal)

def zero_without_snapshot():
    f=fixture('zero_no_snapshot',state='never');result=create(f)
    cfg=rb._receipt_cfg(rb.EXACT_RECEIPT_KEYS,rb.STATUS_CLASSES)
    cfg['interruption_policy']=rb.interruption_policy(result['policy'],'PHASE_1')
    return rb._terminal([],cfg,'never',False,rb._call_binding(f.ctx._fixture_calls[0]))
case('zero_attempt_requires_snapshot',zero_without_snapshot,'CALL_ATTEMPTS_REQUIRED')

def receipt_list_tamper():
    f=fixture('list_tamper');result=create(f);proof=verify(f,result);row=proof['call_states'][0]
    cfg=rb._receipt_cfg(rb.EXACT_RECEIPT_KEYS,rb.STATUS_CLASSES)
    cfg['interruption_policy']=rb.interruption_policy(result['policy'],'PHASE_1')
    cfg['snapshot_call_states']={rb._call_key(row['call']):row}
    return rb._terminal([],cfg,'tampered',False,row['call'])
case('build_attempts_exactly_snapshot',receipt_list_tamper,'SNAPSHOT_BUILD_ATTEMPTS')

case('snapshot_time_primitive_refuses_early_incomplete',lambda:rb._snapshot_t(
    [{'terminal':None}],rb.parse_utc_ns('2026-11-06T05:58:59Z','now'),
    rb.parse_utc_ns(M.PHASE1_CEILING_UTC,'ceil')),'SNAPSHOT_BEFORE_CEILING')

MUTATION=sys.argv[2] if len(sys.argv)>2 else None
MUTATED_SHA=None
if MUTATION:
    text=BUILDER.read_text()
    before="                if (item['class'] == 'FAILED' and"
    after="                if (False and item['class'] == 'FAILED' and"
    if MUTATION=='authenticated_flag_instead_of_bound_record':
        before="                        item['evidence'].get('cause_record') is None):"
        after="                        item['evidence'].get('cause_authenticated') is not True):"
    assert text.count(before)==1
    text=text.replace(before,after)
    MUTATED_SHA=hashlib.sha256(text.encode()).hexdigest()
    exec(compile(text,str(BUILDER)+':mutant:'+MUTATION,'exec'),rb.__dict__)

def a279(label, *, solo=True, bound=False, wrong=False, late=False, null=False):
    f=fixture('A279_'+label,mode='ROUTE_A_NO_FIXED_POINT',sample={} if solo else None,
        receipt_changes=(lambda d:d.update(utc_end='2026-11-07T00:00:00Z')) if late else None,
        now='2026-11-08T00:00:00Z')
    receipt=M.pin_of(f.outdir+'.attempt_receipt.json')
    policy=M.read_pin(f.input['interruption_policy'])
    if bound or null:
        cause=None
        if bound:
            producer=suite.raw_write(f.root/'inert_cause_producer.py',b'# never executed\n')
            policy['cause_producer']=producer
            cause_doc={'status':'ROUTE_A_NO_FIXED_POINT','failing_stage':'synthetic_stage',
                'failure_code':'ROUTE_A_NO_FIXED_POINT','exception_class':'SyntheticModelError',
                'raise_site':'synthetic.py:1','model_outcome':False,
                'model_outcome_reason':'UNKNOWN_BUT_EXPLICITLY_NONMODEL',
                'bound_shas':{'receipt':M.pin_of(f.outdir+'.receipt.json')['sha256'],
                    'result':f.rec['result']['sha256'],'finish':None,
                    'spec':f.call['spec']['sha256'],'driver':f.ctx.pins['driver']['sha256']}}
            if wrong:cause_doc['bound_shas']['receipt']='0'*64
            cause=suite.raw_write(f.root/'bound_cause.json',M.encoded(cause_doc))
            root=f.ctx.v006_text+'\n## A1000: synthetic producer\nTOOL_PIN SYNTHETIC_CAUSE %s %s\n'%(
                producer['sha256'],producer['path'])
            vp=suite.raw_write(f.root/'V006_WITH_CAUSE.md',root.encode())
            f.ctx.cfg=dict(f.ctx.cfg,v006=vp['path'])
            f.ctx.config_pin=suite.raw_write(f.root/'CONFIG_WITH_CAUSE.json',M.encoded(f.ctx.cfg))
            f.input['config']=f.ctx.config_pin
        policy['attempts']=[{'receipt':receipt,'cause':cause,'root_stop':None}]
        pp=suite.raw_write(f.root/'POLICY_WITH_CAUSE.json',M.encoded(policy))
        f.input['interruption_policy']=pp
    result=create(f)
    assert result['mode']=='CEILING'
    proof=verify(f,result)
    assert proof['verdict']=='BYTE_EQUAL'
    return True

case('A279_eligible_solo_failed_missing_row_refuses',lambda:a279('missing'),
     'SNAPSHOT_SOLO_FAILED_CAUSE_REQUIRED')
case('A279_eligible_solo_failed_null_cause_refuses',lambda:a279('null',null=True),
     'SNAPSHOT_SOLO_FAILED_CAUSE_REQUIRED')
case('A279_wrong_cause_monitor_binding_refuses',lambda:a279('wrong',bound=True,wrong=True),
     'CAUSE_MONITOR_BINDING')
case('A279_bound_unknown_nonmodel_cause_is_sufficient',lambda:a279('bound',bound=True))
case('A279_non_solo_failure_unchanged',lambda:a279('not_solo',solo=False))
case('A279_postcutoff_solo_failure_excluded',lambda:a279('late',late=True))

results=[]
for name,fn,expected in CASES:
    observed='RETURNED';passed=False
    try:
        value=fn();passed=expected is None and value is not False
    except Exception as e:
        observed=getattr(e,'code',repr(e));passed=observed==expected
        if not passed:print(traceback.format_exc(limit=5))
    row={'id':name,'expected':expected,'observed':observed,'verdict':'PASS' if passed else 'FAIL'}
    results.append(row)
    if not passed:print(json.dumps(row))
import subprocess
report_date=subprocess.check_output(['/bin/date','-u'],env=dict(os.environ,LC_ALL='C'),text=True).strip()
record={'date_u':report_date,'scope':'TESTED saved synthetic P112 contexts; no process launch; actual PLAN reconstruction UNTESTED',
    'builder':{'path':str(BUILDER),'sha256':BUILDER_SHA},'n_cases':len(results),'n_pass':sum(r['verdict']=='PASS' for r in results),'cases':results}
record.update(mutation=MUTATION,mutated_source_sha256=MUTATED_SHA)
with (WORK/'TEST_RECORD.json').open('xb') as f:f.write(M.encoded(record))
print('%d/%d PASS'%(record['n_pass'],record['n_cases']))
raise SystemExit(0 if record['n_pass']==record['n_cases'] else 1)

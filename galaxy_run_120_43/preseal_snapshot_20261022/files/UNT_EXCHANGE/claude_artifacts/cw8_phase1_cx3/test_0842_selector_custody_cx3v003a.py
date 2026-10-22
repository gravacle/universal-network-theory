"""0842 N1/N6/N8: synthetic metadata, real Context/CLI, no scientific execution."""
import contextlib
import io
import threading
import time
from pathlib import Path
import sys

HERE = Path(__file__).parent
fixture_path = HERE/'test_selector_cx3v003.py'
source = fixture_path.read_text().split('\ncase("missing_license_automatic_serial"')[0]
exec(compile(source, str(fixture_path)+':definitions', 'exec'), globals())
MUTANTS = {
    'restore_license_ignored': ('        cw8_authenticate(ctx, doc.get("license"))',
                               '        pass # mutant skips restore authentication'),
    'root_license_equality_ignored': (
        '    need(cw8_root_license_pin(ctx.v006_text) == license_pin, "CW8_LICENSE_NOT_ROOT_PINNED")',
        '    need(True, "CW8_LICENSE_NOT_ROOT_PINNED")'),
    'choice_producer_ignored': ('        need(doc.get("producer") == ctx.own_pin, "CW8_CHOICE_PRODUCER")',
                                '        need(True, "CW8_CHOICE_PRODUCER")'),
    'restore_prediction_ignored': (
        '        need(prediction == doc.get("prediction") and prediction["column_workers"] == 8 and',
        '        need(True and'),
    'full_spec_root_pin_ignored': ('        need(row["spec"] == chosen_pin, "CW8_FULL_SPEC_ROOT_PIN")',
                                  '        need(True, "CW8_FULL_SPEC_ROOT_PIN")'),
    'legacy_role_widened': (
        '    if saved is None and allow_legacy and call.get("worker_choice") is None:',
        '    if saved is None and allow_legacy:'),
    'history_role_check_removed': ('        cw8_check_attempt(ctx, call, rec)\n',
                                   '        pass # mutant skips history role check\n'),
    'write_watcher_guard_removed': (
        '    need(name == TWIN or watch_pid is None, "CW8_FULL_CALL_TWIN_WATCHER")',
        '    need(True, "CW8_FULL_CALL_TWIN_WATCHER")'),
    'default_choice_skipped': ('        call = cw8_ensure_default(ctx, call)',
                               '        pass # mutant skips default choice'),
    'choice_lock_removed': ('@cw8_choice_lock\ndef select_workers(',
                            'def select_workers('),
    'malformed_forecast_guard_removed': (
        '            need(type(forecast) is dict, "CW8_FORECAST_FORM")',
        '            pass # mutant removes shape guard'),
}
mutation = sys.argv[2] if len(sys.argv)>2 else None
mutated_sha = None
if mutation:
    before, after = MUTANTS[mutation]
    changed = TOOL.read_text()
    assert changed.count(before)==1, (mutation, changed.count(before))
    changed = changed.replace(before, after)
    mutated_sha = hashlib.sha256(changed.encode()).hexdigest()
    exec(compile(changed, str(TOOL)+':mutant:'+mutation, 'exec'), M.__dict__)
M.SyntheticSystem.utc = lambda self: NOW
M.SyntheticSystem.processes = lambda self: []

def cli(f, command='status', extra=()):
    args = [command, '--config', f.config['path'], '--config-sha256', f.config['sha256'],
            '--synthetic-pins', f.synthetic['path'],
            '--synthetic-pins-sha256', f.synthetic['sha256'], *extra]
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = M.cli(args)
    return rc, json.loads(buf.getvalue())

def malformed_forecast(value, reason=None):
    f = make_context()
    fp = put(f.root/'BAD_FORECAST.json', value)
    rc, result = cli(f, 'select-workers', ('--forecast',fp['path'],'--forecast-sha256',fp['sha256']))
    assert rc==0 and result['column_workers']==1, result
    record = M.read_pin(result['choice'])
    assert record['prediction']['column_workers']==1
    if reason:
        assert record['prediction']['reason']==reason, record['prediction']
    restored = f.context(f.config)
    assert all(M.cw8_workers(c)==1 for c in restored.calls() if c['origin']=='P112')
    return True

for value in (None, [], [1], 'bad', 1, False):
    case('N1_non_dict_forecast_'+repr(value), lambda value=value:
         malformed_forecast(value,'CW8_FORECAST_FORM'))
case('N1_empty_forecast', lambda:malformed_forecast({}))

def replace_license(f, comparator):
    rp = put(f.root/'MALFORMED_COMPARATOR.json', comparator)
    lic = M.read_pin(f.license)
    lic['comparator_record'] = rp
    lp = put(f.root/'LICENSE_SUCCESSOR.json',lic)
    text = f.ctx.v006_text.replace(
        'CW8_LICENSE_PIN path=%s sha256=%s'%(f.license['path'],f.license['sha256']),
        'CW8_LICENSE_PIN path=%s sha256=%s'%(lp['path'],lp['sha256']))
    vp = put(f.root/'ROOT_SUCCESSOR.md',text.encode(),raw=True)
    cp = put(f.root/'CONFIG_SUCCESSOR.json',dict(f.ctx.cfg,v006=vp['path']))
    f.config, f.ctx, f.license = cp, f.context(cp), lp
    return f

def malformed_comparator(value):
    f=replace_license(make_context(),value)
    result, record=choose(f)
    assert result['column_workers']==1 and record['prediction']['column_workers']==1
    assert len(list(M.cw8_choice_directory(f.ctx).glob('CHOICE_*.json')))==1
    return True
for value in (None, [], [1], 'bad', 1, False, {}, {'iterations_compared':False}):
    case('N1_malformed_comparator_'+repr(value),
         lambda value=value:malformed_comparator(value))

for key,value in (('host_cores',True),('cores_in_use',[]),('remaining_barrier_h',[]),
                  ('observed_utc',{}),('calls',{}),('remaining_barrier_h',{'expectation':10**400,'upper':0})):
    def wrong_type(key=key,value=value):
        f=make_context()
        result,record=choose(f,**{key:value})
        assert result['column_workers']==1 and record['prediction']['column_workers']==1
        return True
    case('N1_forecast_wrong_type_'+key+'_'+str(type(value)),wrong_type)

def forged_choice(kind, through_cli=False):
    f=make_context(missing_license=kind=='unlicensed',
                   mutate_record=(lambda d:d.update(bitwise_equal=False)) if kind=='bad_comparator' else None)
    ctx=f.ctx
    calls=[c for c in ctx.calls() if c['origin']=='P112']
    fp=forecast(f)
    rows=[dict(name=c['name'],point_key=c['point_key'],theta_sha256=c['theta_sha256'],
               serial_spec=c['spec'],spec=ctx.get_vpin('SPEC_PIN',c['name']+'_FULL_CW8'),
               column_workers=8) for c in sorted(calls,key=lambda c:c['name'])]
    doc={'schema':M.CW8_CHOICE_SCHEMA,'producer':ctx.own_pin,'scope':M.cw8_scope(ctx),
         'selected_at_utc':NOW,'date_u':DATE,'license':f.license,'forecast':fp,
         'prediction':M.cw8_predict(M.read_pin(fp),[c['name'] for c in calls],NOW),'calls':rows}
    expected={'unlicensed':'CW8_LICENSE_NOT_ROOT_PINNED','bad_comparator':'CW8_COMPARATOR_NOT_BITWISE_EQUAL',
              'root_license':'CW8_LICENSE_NOT_ROOT_PINNED','producer':'CW8_CHOICE_PRODUCER',
              'prediction':'CW8_CHOICE_NOT_DERIVED','root_full_spec':'CW8_FULL_SPEC_ROOT_PIN'}.get(kind)
    if kind=='root_license':
        doc['license']=put(f.root/'UNREGISTERED_LICENSE_COPY.json',
                           M.read_pin(f.license,decode=False),raw=True)
    elif kind=='producer':
        doc['producer']=dict(ctx.own_pin,sha256='0'*64)
    elif kind=='prediction':
        doc['prediction']['scenarios']['upper']['predicted_saving_h']+=1
    elif kind=='root_full_spec':
        rows[0]['spec']=put(f.root/'UNREGISTERED_FULL_SPEC_COPY.json',
                            M.read_pin(rows[0]['spec'],decode=False),raw=True)
    directory=M.cw8_choice_directory(ctx);directory.mkdir()
    cp=put(directory/'CHOICE_SAVED_SYNTHETIC.json',doc)
    if through_cli:
        rc,result=cli(f)
        assert rc==2 and result.get('code')==expected,(rc,result,expected)
    else:
        try:
            restored=f.context(f.config)
            restored.calls()
        except M.Refusal as exc:
            assert exc.code==expected,(exc.code,expected)
        else:
            assert expected is None,'forged choice accepted '+kind
            assert all(M.cw8_workers(c)==8 for c in restored.calls() if c['origin']=='P112')
    return True
case('N6_honest_saved_choice_restores',lambda:forged_choice('honest'))
for kind in ('unlicensed','bad_comparator','root_license','producer','prediction','root_full_spec'):
    case('N6_restore_refuses_'+kind,lambda kind=kind:forged_choice(kind))
    case('N6_CLI_restore_refuses_'+kind,lambda kind=kind:forged_choice(kind,True))

def legacy_role():
    f=make_context();choose(f)
    M.cw8_check_role(f.ctx.call('P1_M0001'),None)
case('N6_selected_cw8_cannot_use_legacy_missing_role',legacy_role,'CW8_ROLE_CUSTODY')

def history_watcher():
    f=make_context();choose(f)
    ctx=f.ctx;call=ctx.call('P1_M0001')
    rec={'name':call['name'],'attempt':1,'origin':'P112','outcome':'LAUNCH',
         'caps':M.first_caps(call['name'],8),'worker_role':M.cw8_role(call),
         'spec':call['spec'],'watch_pid':900003,
         'receipt':str(f.root/'ABSENT.receipt.json'),'outdir':str(f.root/'ABSENT'),
         'monitor':ctx.pins['monitor'],'monitor_pid':900001,
         'record_pin':{'path':str(Path(ctx.cfg['p112_launch_root'])/'launches'/
                      'P112_P1_M0001_LAUNCH_CX2V001_A1.json'),'sha256':'a'*64}}
    # Saved record enumeration seam; role guard and history state machine are real.
    rec['outdir']=M.planned_outdir(ctx,call['name'],1,'P112')
    rec['receipt']=rec['outdir']+'.receipt.json'
    ctx.records=lambda name:[rec]
    return M.history(ctx,call,inspect_next=False)
case('N6_history_checks_role_before_pending_receipt',history_watcher,'CW8_FULL_CALL_TWIN_WATCHER')

def write_watcher():
    f=make_context();choose(f)
    ctx=f.ctx;call=ctx.call('P1_M0001')
    M.create_layout(ctx)
    plan={'name':call['name'],'attempt':1,'outdir':str(f.root/'ABSENT'),
          'receipt':str(f.root/'ABSENT.receipt.json'),'launch_json':str(f.root/'ABSENT.launch.json'),
          'spec':call['spec'],'caps':M.first_caps(call['name'],8),'caps_basis':{},
          'm15_record':None,'host_ram_bytes':M.RAM,'solo_mode':False,'counted_rerun':False,
          'rule_c_basis':[],'config':ctx.config_pin,'worker_role':M.cw8_role(call)}
    return M.write_launch_record(ctx,plan,None,None,900001,900002,900003,
                                 {'synthetic_saved_metadata':True},snapshot=(None,None))
case('N6_write_time_full_watcher_refused',write_watcher,'CW8_FULL_CALL_TWIN_WATCHER')

def default_cli():
    f=make_context(missing_license=True)
    # Empty synthetic process table refuses at the watch gate, before any
    # executable stage. The audit hook independently prohibits all processes.
    rc,result=cli(f,'launch',('--name','P1_M0001'))
    assert rc==2 and result.get('code')=='MEMORY_WATCH_NOT_RUNNING',result
    choices=M.cw8_saved_choices(f.ctx)
    assert 'P1_M0001' in choices,'CLI omitted durable default serial choice'
    assert choices['P1_M0001'][0]['column_workers']==1
    return True
case('N6_CLI_preflight_refusal_still_has_default_serial_choice',default_cli)

def concurrency():
    f=make_context()
    fp=forecast(f)
    fdoc=M.read_pin(fp);fdoc['cores_in_use']=6
    other=put(f.root/'FORECAST_SERIAL.json',fdoc)
    contexts=[f.context(f.config),f.context(f.config)]
    for ctx in contexts:ctx.calls()  # deliberately stale before the first commit
    sync=threading.Barrier(2);inside=threading.Barrier(2)
    original=M.cw8_admission_clear
    seen=set();guard=threading.Lock()
    def overlap(ctx,call):
        with guard:
            first=id(ctx) not in seen;seen.add(id(ctx))
        if first:
            try:inside.wait(timeout=0.2)
            except threading.BrokenBarrierError:pass
        return original(ctx,call)
    M.cw8_admission_clear=overlap
    outcomes=[]
    def worker(i):
        sync.wait()
        try:outcomes.append(M.select_workers(contexts[i],[fp,other][i])['status'])
        except Exception as exc:outcomes.append(getattr(exc,'code',type(exc).__name__))
    threads=[threading.Thread(target=worker,args=(i,)) for i in (0,1)]
    try:
        for th in threads:th.start()
        for th in threads:th.join(timeout=10)
        assert not any(th.is_alive() for th in threads)
    finally:M.cw8_admission_clear=original
    assert sorted(outcomes)==['CW8_NO_NEW_CALLS','SELECTED'],outcomes
    assert len(list(M.cw8_choice_directory(f.ctx).glob('CHOICE_*.json')))==1
    restored=f.context(f.config)
    assert len(M.cw8_saved_choices(restored))==3
    assert len({M.cw8_workers(c) for c in restored.calls() if c['origin']=='P112'})==1
    return True
case('N8_concurrent_selectors_create_one_cohort_and_refresh_cached_calls',concurrency)

report={'date_u':DATE,'status':'TESTED','scope':__doc__,'cases':RESULTS,
        'passed':sum(r['status']=='PASS' for r in RESULTS),
        'failed':sum(r['status']!='PASS' for r in RESULTS),
        'mutation':mutation,'mutated_source_sha256':mutated_sha,
        'launcher':{'path':str(TOOL),'sha256':TOOL_SHA},
        'test':{'path':str(Path(__file__)),'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
        'seams':['inert pins/SyntheticSystem','saved record enumeration in history adverse case',
                 'two threads contend on actual filesystem flock; no processes'],
        'scientific_execution':'NONE'}
put(WORK/'EVIDENCE.json',report)
print(json.dumps({'passed':report['passed'],'failed':report['failed'],'mutation':mutation,
                  'failures':[r for r in RESULTS if r['status']!='PASS']}))
sys.exit(bool(report['failed']))

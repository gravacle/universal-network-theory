"""0835 F1-F3 controls from invented/saved metadata; no processes or run-content reads."""
import hashlib
from pathlib import Path
import sys

BASE = Path(__file__).parent/'test_p112_inherited_cx3v002.py'
base_raw = BASE.read_bytes()
base_pin = {'path': str(BASE), 'sha256': hashlib.sha256(base_raw).hexdigest()}
prefix = base_raw.decode().split('\nresults=[]\n')[0]
assert len(prefix) < len(base_raw)
original_args = list(sys.argv)
requested_mutation = original_args[2] if len(original_args)>2 else None
sys.argv = original_args[:2]
try:
    exec(compile(prefix, str(BASE)+':definitions', 'exec'), globals())
finally:
    sys.argv = original_args
CASES = []
MUTATION = requested_mutation
MUTATED_SHA = None
MUTANTS = {
    'F1_admission_stop_returned': (
        "    need(monitor_ceiling_utc is not None, 'MONITOR_PHASE2_CEILING_REQUIRED')",
        "    remaining_wall(phase_ceiling_utc, now_utc)\n"
        "    need(monitor_ceiling_utc is not None, 'MONITOR_PHASE2_CEILING_REQUIRED')"),
    'F1_fresh_plan_stop_returned': (
        "def fresh_launch_plan(ctx, bootstrap, now_utc):\n",
        "def fresh_launch_plan(ctx, bootstrap, now_utc):\n"
        "    remaining_wall(ctx.cfg['phase1_ceiling_utc'], now_utc)\n"),
    'F1_commit_stop_returned': (
        "    need(timestamp(plan['invocation_utc']) >= timestamp(bootstrap['invocation_utc']),",
        "    remaining_wall(ctx.cfg['phase1_ceiling_utc'], basis['decision_utc'])\n"
        "    need(timestamp(plan['invocation_utc']) >= timestamp(bootstrap['invocation_utc']),"),
    'F2_hold_hidden_again': (
        "    if hold is not None:\n"
        "        return {'status': hold, 'terminal': None, 'stop_requested': False}\n",
        "    if hold is not None and timestamp(now_utc) < cutoff:\n"
        "        return {'status': hold, 'terminal': None, 'stop_requested': False}\n"),
    'F3_unknown_reason_held_again': (
        "            # A270: retain the pinned record, but release an uncounted solo\n"
        "            # retry even when its reason awaits later readable classification.\n"
        "            mapped[key] = None\n",
        "            if cause['model_outcome_reason'] in KNOWN_NONPHYSICS_CAUSES:\n"
        "                mapped[key] = None\n"),
    'phase2_stop_removed': (
        "    need(remaining > 0, 'UNEVALUATED_SCHEDULE_CEILING')",
        "    need(True, 'UNEVALUATED_SCHEDULE_CEILING')"),
}
if MUTATION:
    text = P112.read_text()
    before, after = MUTANTS[MUTATION]
    assert text.count(before)==1
    text = text.replace(before, after)
    MUTATED_SHA = hashlib.sha256(text.encode()).hexdigest()
    exec(compile(text, str(P112)+':SYNTHETIC_MUTANT:'+MUTATION, 'exec'), M.__dict__)

AFTER = '2026-11-07T00:00:00Z'
LATE = '2026-11-30T00:00:00Z'


def next_at(actual, causes=None, now=AFTER, workers=1):
    records = [{'attempt': x['attempt'], 'origin': 'P112', 'outcome': 'LAUNCH'} for x in actual]
    return M.next_attempt('P1_M0001', records, actual, set(),
        phase_ceiling_utc=M.PHASE1_CEILING_UTC, monitor_ceiling_utc=M.PHASE2_CEILING_UTC,
        now_utc=now, authenticated_causes=causes, column_workers=workers)


def first_at(now, workers):
    d = next_at([], now=now, workers=workers)
    assert d['attempt']==1 and d['solo_mode'] is False and d['counted_rerun'] is False
    assert d['caps']['wall_cap_s']==M.remaining_wall(M.PHASE2_CEILING_UTC,now)
    assert d['caps']['rss_cap_bytes']==M.RAM*(11 if workers==8 else 1)
    return True


for when in (M.PHASE1_CEILING_UTC, AFTER, LATE):
    for workers in (1,8):
        case('F1_first_admission_'+when+'_cw'+str(workers),
             lambda when=when, workers=workers:first_at(when,workers))
case('F1_phase2_first_admission_stops',lambda:next_at([],now=M.PHASE2_CEILING_UTC),
     'UNEVALUATED_SCHEDULE_CEILING')


def model_rerun():
    r1 = policy_row(1, time_utc='2026-11-06T10:00:00Z')
    a = authenticate(mapped([r1]), [r1])
    decision = next_at([r1], a)
    assert decision['attempt']==2 and decision['solo_mode'] is True
    assert decision['counted_rerun'] is False and decision['model_confirmation_rerun'] is True
    r2 = policy_row(2, time_utc='2026-11-08T00:00:00Z')
    rr = [r1,r2]
    auth = authenticate(mapped(rr),rr)
    assert M.terminal_prefix(rr,'P1_M0001',auth)['disposition']=='RULE_C_INVALID'
    assert M.terminal_prefix(rr,'P1_M0001',auth)['counted_attempts']==[0,1]
    assert M.terminal_prefix(rr,'P1_M0001',{}) is None
    changed = copy.deepcopy(rr); changed[1]['other_ngc_processes_max']=1
    assert M.terminal_prefix(changed,'P1_M0001',auth) is None
    changed = copy.deepcopy(rr); changed[1]['spec_sha256']='c'*64
    assert M.terminal_prefix(changed,'P1_M0001',auth) is None
    # Post-cutoff counts never rewrite the earlier Phase-1 reporting snapshot.
    assert M.phase_disposition(rr,'P1_M0001',M.PHASE1_CEILING_UTC,LATE,auth)['status']=='UNEVALUATED_SCHEDULE_CEILING'
    return True


case('F1_post_cutoff_solo_model_rerun_counts_only_A245',model_rerun)
for cls, raw in (('CAP','STOPPED_WALL_CAP|NONE'),('OUTPUT_CAP','STOPPED_OUTPUT_CAP|NONE'),
                 ('INFRA','CHILD_FAILED|NONE|SIGNAL')):
    def uncounted(cls=cls,raw=raw):
        rr=[policy_row(1,status_class=cls,raw_status=raw,_known_nonphysics=True,time_utc=AFTER)]
        d=next_at(rr,now=LATE)
        assert d['attempt']==2 and d['solo_mode'] is True and d['counted_rerun'] is False
        assert M.terminal_prefix(rr,'P1_M0001') is None
        if cls=='OUTPUT_CAP':
            assert d['caps']['output_cap_bytes']==2000
        return True
    case('F1_post_cutoff_uncounted_retry_'+cls,uncounted)
case('F1_phase2_retry_stops',lambda:next_at(
    [policy_row(1,status_class='CAP',raw_status='STOPPED_WALL_CAP|NONE',_known_nonphysics=True)],
    now=M.PHASE2_CEILING_UTC),'UNEVALUATED_SCHEDULE_CEILING')

NC = 0
def final_commit(now):
    global NC
    NC += 1
    f=module.receipt_fixture(suite,'F1_commit_%03d'%NC,no_receipt=True)
    ctx=f.ctx
    work=Path(ctx.cfg['p112_launch_root'])/'work'/'F1_COMMIT'
    work.mkdir()
    caps=dict(M.first_caps(f.name),wall_cap_s=M.remaining_wall(M.PHASE2_CEILING_UTC,NOW))
    plan={'schema':'UNT_P112_LAUNCH_PLAN_CX2V001','name':f.name,'attempt':1,
        'config':ctx.config_pin,'work':str(work),'spec':f.call['spec'],
        'worker_role':M.cw8_role(f.call),
        'pins':{k:ctx.pins[k] for k in ('driver','monitor')},
        'outdir':f.outdir,'caps':caps,'caps_basis':{'rule':'bootstrap'},
        'invocation_utc':NOW,'date_u':M.date_u(),'solo_mode':False,
        'monitor_argv':M.monitor_command(ctx.pins,f.call['spec'],f.outdir,caps)}
    bootstrap_pin=ctx.write(str(work/'plan.json'),plan)
    start=len(READS)
    @M.read_scope
    def check():
        final, fp = M.write_launch_commit(ctx,plan,bootstrap_pin,work,now)
        assert final['caps']['wall_cap_s']==M.remaining_wall(M.PHASE2_CEILING_UTC,now)
        assert M.read_launch_commit(ctx,plan,bootstrap_pin,work)==(final,fp)
        assert final['caps_basis']['phase1_requests_stop'] is False
    check()
    counts=collections.Counter(READS[start:])
    assert counts and max(counts.values())==1
    return True


case('F1_final_commit_after_Nov6_reconstructs_single_read',lambda:final_commit(AFTER))
case('F1_final_commit_Nov30_reconstructs_single_read',lambda:final_commit(LATE))
case('F1_final_commit_at_Phase2_refuses',lambda:final_commit(M.PHASE2_CEILING_UTC),
     'UNEVALUATED_SCHEDULE_CEILING')


def held_status(kind, now):
    rr = [policy_row(k) for k in (1,2)]
    if kind=='HELD_FOR_FIX':
        for r in rr:
            r.update(raw_status='CHILD_FAILED|REFUSED',status_class='INFRA',_known_nonphysics=True)
    h={'actual':rr,'pending':[],'nonattempts':[],'consecutive_nonattempts':0}
    ctx=types.SimpleNamespace(cfg={'cause_records':[], 'phase1_ceiling_utc':M.PHASE1_CEILING_UTC,
        'phase2_ceiling_utc':M.PHASE2_CEILING_UTC},
        system=types.SimpleNamespace(utc=lambda:now), residuals=lambda:set(),
        calls=lambda:[{'name':'P1_M0001'}])
    original=M.history
    M.history=lambda *a,**kw:h  # explicit saved-history input seam, not policy override
    try:
        result=M.status(ctx)
    finally:
        M.history=original
    assert result['calls'][0]['status']==kind
    assert result['calls'][0]['phase_1']['status']==kind
    assert result['stop_requested'] is False and result['calls'][0]['next'] is None
    return True


for kind in ('HELD_FOR_CAUSE','HELD_FOR_FIX'):
    for when in (M.PHASE1_CEILING_UTC,AFTER,M.PHASE2_CEILING_UTC):
        case('F2_status_'+kind+'_'+when,lambda kind=kind,when=when:held_status(kind,when))


def unknown_release(reason):
    rr=[policy_row(k) for k in (1,2)]
    ctx=mapped(rr,lambda c,i:c.update(model_outcome=False,model_outcome_reason=reason))
    pins=copy.deepcopy(ctx.cfg['cause_records'])
    auth=authenticate(ctx,rr)
    assert len(auth)==2 and all(x is None for x in auth.values())
    assert M.held_for_cause(rr,auth) is False and M.terminal_prefix(rr,'P1_M0001',auth) is None
    d=next_at(rr,auth)
    assert d['attempt']==3 and d['solo_mode'] is True
    assert d['counted_rerun'] is False and d['model_confirmation_rerun'] is False
    # A later synthetic classification uses successor records; old bytes survive.
    classified=authenticate(mapped(rr),rr)
    assert M.terminal_prefix(rr,'P1_M0001',classified)['disposition']=='RULE_C_INVALID'
    for p in pins:
        data=Path(p['path']).read_bytes()
        assert hashlib.sha256(data).hexdigest()==p['sha256']
        assert json.loads(data)['model_outcome'] is False
    return True


for reason in ('STATUS_NOT_MODEL_FAILURE','UNAUTHENTICATED_STAGE_FAILURE',
               'NGC_POST_SEAL_ATTESTATION_REQUIRED','METADATA_REFUSED'):
    case('F3_unknown_reason_uncounted_solo_release_'+reason,
         lambda reason=reason:unknown_release(reason))


def false_bad_binding(field):
    rr=[policy_row(k) for k in (1,2)]
    def alter(c,i):
        c.update(model_outcome=False,model_outcome_reason='UNKNOWN_REASON')
        if i:
            c['bound_shas'][field]='f'*64
    return authenticate(mapped(rr,alter),rr)


for field in ('spec','driver','result'):
    case('F3_false_cause_still_authenticates_'+field,lambda field=field:false_bad_binding(field),
         'CAUSE_RESULT_BINDING' if field=='result' else 'CAUSE_SCIENCE_BINDING')

case('F3_missing_cause_still_held',lambda:next_at([policy_row(1),policy_row(2)]),'HELD_FOR_CAUSE')

results=[]
for name,fn,expected in CASES:
    observed='RETURNED';passed=False
    try:
        value=fn();passed=expected is None and value is not False
    except M.Refusal as exc:
        observed=exc.code;passed=exc.code==expected
    except Exception as exc:
        observed=repr(exc)
    row={'id':name,'expected':expected,'observed':observed,'verdict':'PASS' if passed else 'FAIL'}
    results.append(row)
record={'date_u':M.date_u(),'scope':__doc__,'base_fixture':base_pin,
    'tool':{'path':str(P112),'sha256':P112_SHA},
    'test':{'path':str(Path(__file__)),'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
    'mutation':MUTATION,'mutated_sha256':MUTATED_SHA,'n_cases':len(results),
    'n_pass':sum(r['verdict']=='PASS' for r in results),'cases':results,
    'seams':['inherited synthetic source/System fixtures','explicit saved-history input for public status only'],
    'scientific_execution':'NONE'}
with (WORK/'TEST_RECORD.json').open('xb') as f:
    f.write(M.encoded(record))
print(json.dumps({'passed':record['n_pass'],'total':record['n_cases'],
                  'mutation':MUTATION,'failures':[r for r in results if r['verdict']!='PASS']}))
raise SystemExit(0 if record['n_pass']==record['n_cases'] else 1)

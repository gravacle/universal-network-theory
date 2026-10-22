"""F2: saved synthetic kit relaunch uses a fresh fill path with identical bytes."""
import hashlib
from pathlib import Path
import sys
HERE=Path(__file__).parent
base=HERE/'test_p112_inherited_cx3v003.py'
source=base.read_text().split('\nCASES = []\n')[0]
args=list(sys.argv);mutation=args[2] if len(args)>2 else None
sys.argv=args[:2]
exec(compile(source,str(base)+':definitions','exec'),globals())
sys.argv=args
mutated_sha=None
if mutation:
    source=P112.read_text()
    before='    need(is_pin(spec) and spec["sha256"] == call["spec"]["sha256"],'
    after=('    need(spec == call["spec"],' if mutation=='whole_pin_restored'
           else '    need(True,')
    assert source.count(before)==1
    source=source.replace(before,after)
    mutated_sha=hashlib.sha256(source.encode()).hexdigest()
    exec(compile(source,str(P112)+':mutant:'+mutation,'exec'),M.__dict__)
results=[]
def case(name,fn,code=None):
    try:
        result=fn();passed=code is None and result is not False;observed='RETURNED'
    except Exception as e:
        observed=getattr(e,'code',repr(e));passed=observed==code
    results.append({'name':name,'expected':code,'observed':observed,'passed':passed})

def relaunch(label,different=False):
    f=module.receipt_fixture(suite,label,origin='KIT',name='S0_J0_SERIAL',record=False)
    fresh=f.root/'work_relaunch'/'fill'
    fresh.mkdir(parents=True)
    data=M.read_pin(f.call['spec'],decode=False)
    if different:data=data+b'\n'
    new_spec=suite.raw_write(fresh/'SPEC.json',data)
    assert new_spec['path']!=f.call['spec']['path']
    assert (new_spec['sha256']==f.call['spec']['sha256']) is (not different)
    rec=dict(f.record,spec=new_spec)
    suite.raw_write(f.record_path,M.encoded(rec))
    f.ctx.system.utc=lambda:'2026-11-01T00:00:00Z'
    return f

def accept():
    f=relaunch('same_bytes_new_fill')
    # Real history before close recognizes an honest pending close.
    h=M.history(f.ctx,f.call,inspect_next=False,allow_incomplete=True)
    assert h['pending'][0]['status']=='ATTEMPT_NEEDS_CLOSE'
    closed=M.close_attempt(f.ctx,f.name,1)
    assert closed['status_class']=='FINISHED'
    h=M.history(f.ctx,f.call,inspect_next=False)
    assert len(h['actual'])==1 and not h['pending']
    record=f.ctx.records(f.name)[0]
    verified=M.verify_closed_receipt(f.ctx,f.call,record,closed['receipt'])
    assert verified['spec_sha256']==f.call['spec']['sha256']
    return True
case('F2_fresh_kit_fill_same_sha_history_close_verify',accept)
case('F2_fresh_kit_fill_different_sha_history_refuses',
     lambda:(lambda f:M.history(f.ctx,f.call,inspect_next=False))(relaunch('diff_history',True)),
     'CW8_ATTEMPT_RAW_SPEC')
case('F2_fresh_kit_fill_different_sha_close_refuses',
     lambda:(lambda f:M.close_attempt(f.ctx,f.name,1))(relaunch('diff_close',True)),
     'CW8_ATTEMPT_RAW_SPEC')
report={'date_u':M.date_u(),'status':'TESTED','scope':__doc__,'results':results,
        'passed':sum(x['passed'] for x in results),'failed':sum(not x['passed'] for x in results),
        'mutation':mutation,'mutated_source_sha256':mutated_sha,
        'launcher':{'path':str(P112),'sha256':P112_SHA},
        'test':{'path':str(Path(__file__)),'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
        'fixture':{'path':str(base),'sha256':hashlib.sha256(base.read_bytes()).hexdigest()},
        'seams':['saved monitor metadata; no monitor run','fixture Context call list and synthetic System'],
        'scientific_execution':'NONE'}
with (WORK/'EVIDENCE.json').open('xb') as f:f.write(M.encoded(report))
print(json.dumps(report))
sys.exit(bool(report['failed']))

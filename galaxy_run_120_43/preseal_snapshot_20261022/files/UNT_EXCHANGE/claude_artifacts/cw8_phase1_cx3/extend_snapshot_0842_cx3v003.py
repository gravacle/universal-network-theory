"""Retarget snapshot regression fixture and add A279 cause binding controls."""
import hashlib
import json
from pathlib import Path
import subprocess
H=Path(__file__).parent
old=H.parent/'runbook_v002_c2v007_cx2/test_snapshot_a253_v001.py'
source=old.read_text()
source=source.replace("BUILDER = HERE / 'roster_builder_c2v007_a253_v001.py'",
                      "BUILDER = HERE / 'roster_builder_c2v007_cx3cw8v003.py'")
source=source.replace('799fb2d002ba39885326f161e1efbe3ad35dd2b66d3c84f961ddce910e9cd15b',
                      hashlib.sha256((H/'roster_builder_c2v007_cx3cw8v003.py').read_bytes()).hexdigest())
source=source.replace("P112 = ART / 'phase1_ngc_launch_kit_cx2v004/phase1_ngc_launch_cx2v004.py'",
                      "P112 = HERE / 'phase1_ngc_launch_cx3cw8v003.py'")
source=source.replace('8cec1b56fc682f638fee57329eefc9b3cddfa47959d175e7095fc0c5fe0342c9',
                      hashlib.sha256((H/'phase1_ngc_launch_cx3cw8v003.py').read_bytes()).hexdigest())
source=source.replace('P112_LAUNCHER_CX2V004','P112_LAUNCHER_CX3CW8V003')
needle="exec(compile(fixture, str(P112_TEST) + ':saved_fixture', 'exec'), module.__dict__)"
assert source.count(needle)==1
source=source.replace(needle,'''fixture = fixture.replace('"spec": registered_spec, "origin": origin,',
    '"spec": registered_spec, "spec_doc": M.read_pin(registered_spec), "origin": origin,')
fixture = fixture.replace('    if record:\\n',
    '    if sample is not None: record_doc["solo_mode"] = True\\n    if record:\\n')
'''+needle)
extra=r'''
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
'''
assert source.count('\nresults=[]\n')==1
source=source.replace('\nresults=[]\n',extra+'\nresults=[]\n')
# Include the mutation identity in each evidence record without replacing it.
needle="with (WORK/'TEST_RECORD.json').open('xb') as f:f.write(M.encoded(record))"
assert source.count(needle)==1
source=source.replace(needle,
    "record.update(mutation=MUTATION,mutated_source_sha256=MUTATED_SHA)\n"+needle)
out=H/'test_snapshot_0842_cx3v003.py'
with out.open('x') as f:f.write(source)
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
record={'date_u':subprocess.check_output(['/bin/date','-u'],text=True).strip(),
        'source':pin(old),'successor':pin(out),'scope':'synthetic fixture; original cases retained'}
with (H/'SNAPSHOT_TEST_RETARGET_0842_CX3V003.json').open('x') as f:
    json.dump(record,f,indent=2);f.write('\n')
print(json.dumps(record))

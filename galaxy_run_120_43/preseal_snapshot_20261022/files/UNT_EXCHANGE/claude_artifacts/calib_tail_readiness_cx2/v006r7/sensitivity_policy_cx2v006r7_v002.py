"""0540 F3: exact-D, paired tail-OFF A32 identity gate. No scientific launch.

The gate recomputes c2v004's saved-output comparison rather than trusting a
populated PASS document. Only a reviewed pair at the exact requested distance
can open that distance. Read-only gate; CLI writes new reports exclusively.
"""
import argparse
import contextlib
import copy
import hashlib
import io
import json
import math
import os
import sys
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLAN = {'path': str(HERE/'DECIDING_III_PAIR_PLAN_CX2V006R7_V002.json'),
        'sha256': 'cb42a5a3bf8e26d0aa2a3a4c35784c2301fde7ff6c60170da7536ba8cfd95656'}
COMPARATOR = {'path': str(HERE/'run_identity_compare_c2v004_r5_cx2v002.py'),
              'sha256': '5e79c11e4699c311ad2cc419404a1eb28e78bdf03092d5642bc145438a47fb1a'}
BASE_COMPARATOR = {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v004/run_identity_compare_c2v004.py',
                   'sha256': 'e3d153b6dd5bf07ffd74ca8eeb75087d7a1bfd5cab67039c5514fa8744f7abcf'}
MONITOR = {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/galaxy_m0_forward_c2_0466/root_monitor_c2v001.py',
           'sha256': 'ba031c2340057d88ee399138cc645012a93aa7dc3eb7c9bba56d112c94a47107'}
MASKS = ['elapsed_seconds', 'ended_unix_ns', 'pid', 'started_unix_ns', 'utc']
CHECKS = frozenset(('AUTO_CUSTODY','INVENTORY','ATTEMPT_LEDGER','RA_BLOBS',
                    'RA_RECORDS','RA_ARRAYS','RA_IDENTITY','REQUEST','STAGES',
                    'RESULT','STRAY_UV_TAIL'))
HULL = [151250000.0,317625000.0]
SCHEMA_EVIDENCE = 'DDO154_DISTANCE_PAIR_EVIDENCE_CX2V006R7'
SCHEMA_REVIEW = 'DDO154_DISTANCE_PAIR_REVIEW_CX2V006R7'
SCHEMA_REGISTRY = 'DDO154_DISTANCE_PAIR_REGISTRY_CX2V006R7'

class Refusal(ValueError):
    pass

def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def pin(path):
    p=Path(path).resolve()
    return {'path':str(p),'sha256':sha(p.read_bytes())}

def read_bytes(ref):
    if not isinstance(ref,dict) or set(ref)!={'path','sha256'}:
        raise Refusal('PIN_SHAPE')
    if not isinstance(ref['path'],str) or not Path(ref['path']).is_absolute():
        raise Refusal('PIN_ABSOLUTE_PATH_REQUIRED')
    h=ref['sha256']
    if not isinstance(h,str) or len(h)!=64 or any(c not in '0123456789abcdef' for c in h):
        raise Refusal('PIN_SHA256_SHAPE')
    raw=Path(ref['path']).read_bytes()
    if sha(raw)!=h:
        raise Refusal('BYTE_PIN_MISMATCH: '+ref['path'])
    return raw

def read_json(ref):
    def duplicate(pairs):
        d={}
        for k,v in pairs:
            if k in d:raise Refusal('DUPLICATE_JSON_KEY: '+k)
            d[k]=v
        return d
    def bad(x):raise Refusal('NONFINITE_JSON: '+x)
    return json.loads(read_bytes(ref),object_pairs_hook=duplicate,parse_constant=bad)

def load(ref,name):
    raw=read_bytes(ref)
    m=types.ModuleType(name);m.__file__=ref['path'];sys.modules[name]=m
    exec(compile(raw,ref['path'],'exec'),m.__dict__)
    return m

def expect(ok,reason):
    if not ok:raise Refusal(reason)

def distance_key(value):
    expect(type(value) in (float,int) and math.isfinite(value) and value>0,
           'DISTANCE_NOT_FINITE_POSITIVE')
    return float(value).hex()

def plan_pair(distance):
    p=read_json(PLAN)
    key=distance_key(distance)
    expect(p['schema']=='DDO154_DISTANCE_PAIR_PLAN_CX2V006R7','PLAN_SCHEMA')
    expect(p['comparator']==COMPARATOR and p['base_comparator']==BASE_COMPARATOR,'PLAN_COMPARATOR')
    expect(p['masked_keys']==MASKS and p['gate']=='Z2_OFF' and p['tail_on'] is False,'PLAN_MASKS')
    expect(key in p['pairs'],'DISTANCE_NOT_REGISTERED')
    return key,p['pairs'][key]

def validate_tail_off(spec,distance):
    expect(spec.get('galaxy')=='DDO154','GALAXY_NOT_DDO154')
    expect(distance_key(spec['physical']['distance_Mpc'])==distance_key(distance),'DISTANCE_MISMATCH')
    n=spec['numerics']
    expect('uv_tail' not in n,'TAIL_OFF_REQUIRES_OMITTED_BLOCK')
    expect(n.get('route_a')=={'column_workers':8},'TAIL_OFF_ROUTE_A_WORKERS_OR_CONTROLS')
    expect(n.get('truncation') in ({'shape':'cube'},{'shape':'cube','kmax_inverse_kpc':None}),'KEPT_CUBE_REQUIRED')
    expect(n['composite_grid_spec']['breaks_inverse_kpc'][-1]==4,'KEPT_K4_REQUIRED')
    expect(n['brackets']['mode']=='rule','HULL_RULE_REQUIRED')
    hull=n['brackets']['rule']['fs_absolute_overrides']
    expect(set(hull)=={str(i) for i in range(72)} and all(v==HULL for v in hull.values()),'A32_FULL_HULL_REQUIRED')

def validate_run(row,registered,distance,role):
    """Pin, normalize and join own result/start/finish and monitor receipt."""
    expect(set(row)=={'driver','spec','result','receipt','finish','start'},'RUN_ROW_SHAPE: '+role)
    expect(row['driver']==registered['driver'] and row['spec']==registered['spec'],'REGISTERED_DRIVER_SPEC_PAIR: '+role)
    sp=read_json(row['spec']);validate_tail_off(sp,distance)
    driver=load(row['driver'],'_sensitivity_driver_'+role)
    normalized=driver.normalize_spec(copy.deepcopy(sp));validate_tail_off(normalized,distance)
    res=read_json(row['result']);fin=read_json(row['finish']);start=read_json(row['start'])
    out=Path(row['result']['path']).resolve().parent
    expect(Path(row['result']['path']).name=='result.json','RESULT_BASENAME')
    expect(Path(row['finish']['path']).resolve()==out/'finish.json','OWN_FINISH_REQUIRED')
    expect(Path(row['start']['path']).resolve()==out/'start.json','OWN_START_REQUIRED')
    expect(res.get('status')=='COMPLETED' and res.get('valid') is True,'RESULT_NOT_COMPLETED_VALID: '+role)
    expect(res.get('driver_sha256')==row['driver']['sha256'] and res.get('call_spec_sha256')==row['spec']['sha256'],'RESULT_DRIVER_SPEC_BINDING: '+role)
    expect(canonical(res.get('normalized_spec'))==canonical(normalized),'RESULT_NORMALIZED_SPEC_MISMATCH: '+role)
    validate_tail_off(res['normalized_spec'],distance)
    expect(start.get('driver')==row['driver']['path'] and start.get('driver_sha256')==row['driver']['sha256'],'START_DRIVER_BINDING: '+role)
    expect(start.get('call_spec_sha256')==row['spec']['sha256'] and canonical(start.get('normalized_spec'))==canonical(normalized),'START_SPEC_BINDING: '+role)
    expect(fin.get('status')=='COMPLETED' and fin.get('valid') is True and fin.get('retries')==0 and fin.get('result_sha256')==row['result']['sha256'],'FINISH_STATUS_HASH: '+role)
    expect(Path(fin.get('result_path','')).resolve()==out/'result.json','FINISH_RESULT_PATH: '+role)
    read_bytes(row['receipt'])
    mon=load(MONITOR,'_sensitivity_monitor')
    v=mon.verify_receipt(row['receipt']['path'],spec_sha256=row['spec']['sha256'],driver_sha256=row['driver']['sha256'])
    expect(v.get('ok') is True and not v.get('reasons'),'RECEIPT_INVALID: '+repr(v.get('reasons')))
    rec=v['receipt']
    expect(rec.get('status')=='FINISHED' and rec.get('driver_status')=='COMPLETED' and rec.get('exit_code')==0 and rec.get('stop_reason') is None,'RECEIPT_NOT_FINISHED: '+role)
    expect(rec.get('retries')==0,'FRESH_CALL_NO_RETRY_REQUIRED')
    expect(rec.get('result')==row['result'],'RECEIPT_RESULT_BINDING: '+role)
    expect(rec.get('pins',{}).get('spec')==row['spec'] and rec.get('pins',{}).get('driver')==row['driver'],'RECEIPT_EXACT_PINS: '+role)
    expect(rec.get('pins',{}).get('monitor')==MONITOR,'RECEIPT_MONITOR_PIN')
    py=rec.get('pins',{}).get('python')
    expect(isinstance(py,str) and Path(py).is_absolute(),'RECEIPT_PYTHON_PATH')
    expect(rec.get('command')==[py,'-I','-B',row['driver']['path'],'run','--spec',row['spec']['path'],'--outdir',str(out)],'RECEIPT_FRESH_COMMAND')
    return str(out)

def compare_saved(reference,new,tokens):
    """Run the actual pinned comparator, saved states only, no report write."""
    read_bytes(BASE_COMPARATOR)
    m=load(COMPARATOR,'_sensitivity_identity_r5')
    args=['--gate','Z2_OFF','--reference',reference,'--new',new,
          '--tokens',tokens['path'],'--out','UNUSED_IN_MEMORY_REPORT']
    with contextlib.redirect_stdout(io.StringIO()):
        return m.main(args,_return_report=True)

def validate_report(report,pair,roots):
    expect(report.get('schema')=='RUN_IDENTITY_COMPARE_C2V004','COMPARATOR_REPORT_SCHEMA')
    expect(report.get('comparator')==COMPARATOR,'COMPARATOR_IDENTITY')
    adapter=report.get('r5_adapter',{})
    expect(adapter.get('schema')=='C2V004_R5_CUSTODY_ADAPTER_CX2V002' and adapter.get('base_comparator')==BASE_COMPARATOR,'COMPARATOR_BASE_CUSTODY')
    expect(report.get('driver_pin')==[pair['new']['driver']['path'],pair['new']['driver']['sha256']],'COMPARATOR_DRIVER_PIN')
    expect(report.get('reference')==roots['reference'] and report.get('new')==roots['new'],'COMPARATOR_RUN_ROOTS')
    expect(report.get('tokens')==pair['tokens'],'COMPARATOR_DECLARED_CUSTODY_PIN')
    expect(report.get('masked_keys')==MASKS,'COMPARATOR_MASK_SET')
    expect(report.get('gate')=='Z2_OFF' and report.get('tail_on') is False
           and report.get('declared_tail_off_records') is False
           and report.get('require_ro1_armed_flag') is False
           and report.get('ro1_requirement')=='OPTIONAL'
           and report.get('expected_tail_off_request_sha256') is None,'COMPARATOR_GATE_MODE')
    cs=report.get('checks',{})
    expect(isinstance(cs,dict) and set(cs)==CHECKS,'COMPARATOR_REQUIRED_CHECKS')
    expect(all(type(c)==dict and c.get('pass') is True and 'detail' in c for c in cs.values()),'COMPARATOR_CHECK_FAILED')
    expect(report.get('verdict')=='PASS_BITWISE_EQUAL' and report.get('failing')==[],'COMPARATOR_VERDICT')
    expect(cs['AUTO_CUSTODY']['detail'].get('inadmissible')==[],'COMPARATOR_INADMISSIBLE_CUSTODY')
    for k in ('RA_BLOBS','RA_RECORDS','RA_ARRAYS'):
        ns=cs[k]['detail'].get('n')
        expect(isinstance(ns,list) and len(ns)==2 and all(type(v)==int and v>0 for v in ns) and ns[0]==ns[1],k+'_NONEMPTY_REQUIRED')
    cov=report.get('coverage',{})
    expect(type(cov.get('files_both_sides'))==int and cov['files_both_sides']>0
           and type(cov.get('content_compared'))==int and cov['content_compared']>0
           and type(cov.get('not_content_compared'))==int and cov['not_content_compared']>=0
           and cov['content_compared']+cov['not_content_compared']==cov['files_both_sides'],'COMPARATOR_COVERAGE')

def compute_pair(distance,runs):
    key,pair=plan_pair(distance)
    expect(isinstance(runs,dict) and set(runs)=={'reference','new'},'EXACT_TWO_RUNS_REQUIRED')
    roots={role:validate_run(runs[role],pair[role],distance,role) for role in ('reference','new')}
    expect(roots['reference']!=roots['new'],'DISTINCT_RUN_ROOTS_REQUIRED')
    read_json(pair['tokens'])
    report=compare_saved(roots['reference'],roots['new'],pair['tokens'])
    validate_report(report,pair,roots)
    # Reverify all evidence bytes after the potentially long tree comparison.
    for role in ('reference','new'):
        for ref in runs[role].values():read_bytes(ref)
    read_bytes(pair['tokens']);read_bytes(PLAN);read_bytes(COMPARATOR);read_bytes(BASE_COMPARATOR)
    return key,pair,report

def sensitivity_gate(*,config,spec,core=None):
    """core is accepted only for caller compatibility; no injected verifier used."""
    gate={'ok':False,'reasons':[],'status':'UNAVAILABLE','evidence':None}
    try:
        expect(spec.get('galaxy')=='DDO154','GALAXY_NOT_DDO154')
        d=spec['physical']['distance_Mpc'];key=distance_key(d)
        gate['distance_mpc']=d;gate['distance_hex']=key
        if key==float(4.04).hex():
            return dict(gate,ok=True,reasons=[],status='HEADLINE_NOT_GATED')
        key,pair=plan_pair(d)
        reg=config.get('tail_readiness',{}).get('sensitivity_deciding_iii')
        expect(isinstance(reg,dict) and reg.get('schema')==SCHEMA_REGISTRY,'SENSITIVITY_DECIDING_III_REQUIRED')
        entry=reg.get('per_distance',{}).get(key)
        expect(isinstance(entry,dict) and set(entry)=={'evidence','review'},'PER_DISTANCE_EVIDENCE_REVIEW_REQUIRED')
        ev=read_json(entry['evidence']);review=read_json(entry['review'])
        expect(ev.get('schema')==SCHEMA_EVIDENCE and ev.get('status')=='TESTED' and ev.get('ok') is True,'PAIR_EVIDENCE_NOT_TESTED_PASS')
        expect(ev.get('plan')==PLAN and ev.get('distance_hex')==key and distance_key(ev['distance_mpc'])==key,'PAIR_EVIDENCE_DISTANCE_PLAN_BINDING')
        expect(ev.get('launch_owner')=='Claude2' and ev.get('tail_on') is False and ev.get('test')=='iii','PAIR_EVIDENCE_SCOPE')
        report=read_json(ev['comparator_report'])
        expect(review.get('schema')==SCHEMA_REVIEW and review.get('status')=='TESTED' and review.get('verdict')=='PASS','DISTINCT_REVIEW_NOT_TESTED_PASS')
        expect(review.get('evidence')==entry['evidence'] and review.get('comparator_report')==ev['comparator_report']
               and review.get('runs')==ev['runs'] and review.get('plan')==PLAN
               and review.get('distance_hex')==key,'DISTINCT_REVIEW_BINDING')
        expect(isinstance(review.get('reviewer'),str) and review['reviewer'].strip() and review['reviewer'] not in ('Codex2','Codex2 build','CX2'),'DISTINCT_REVIEWER_REQUIRED')
        roots={r:str(Path(ev['runs'][r]['result']['path']).resolve().parent) for r in ('reference','new')}
        validate_report(report,pair,roots)
        _,_,fresh=compute_pair(d,ev['runs'])
        expect(canonical(report)==canonical(fresh),'COMPARATOR_REPORT_NOT_REPRODUCED')
        read_bytes(entry['evidence']);read_bytes(entry['review']);read_bytes(ev['comparator_report'])
        gate.update(ok=True,status='TESTED',evidence=entry,comparator_replayed=True)
    except (Refusal,ValueError,TypeError,KeyError,AttributeError,OSError,RuntimeError,SystemExit) as exc:
        gate['reasons'].append(str(exc))
    return gate

def write_x(path,value):
    with Path(path).open('x') as f:
        json.dump(value,f,sort_keys=True,indent=1,allow_nan=False);f.write('\n')
    return pin(path)

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--pair-input',required=True,help='JSON with distance_mpc and runs (six pins per role)')
    ap.add_argument('--pair-input-sha256',required=True)
    ap.add_argument('--out-report',required=True)
    ap.add_argument('--out-evidence',required=True)
    a=ap.parse_args(argv)
    try:
        inp=read_json({'path':str(Path(a.pair_input).resolve()),'sha256':a.pair_input_sha256})
        key,pair,report=compute_pair(inp['distance_mpc'],inp['runs'])
        rp=write_x(a.out_report,report)
        ev={'schema':SCHEMA_EVIDENCE,'status':'TESTED','ok':True,'test':'iii','tail_on':False,
            'launch_owner':'Claude2','distance_mpc':pair['distance_mpc'],'distance_hex':key,
            'plan':PLAN,'runs':inp['runs'],'comparator_report':rp,'producer':pin(__file__),
            'review_status':'REQUIRED_SEPARATELY_BEFORE_GATE_ADMISSION'}
        ep=write_x(a.out_evidence,ev)
        print(json.dumps({'status':'TESTED','pair_evidence':ep,'comparator_report':rp,'gate_admitted':False}))
        return 0
    except (Refusal,ValueError,TypeError,KeyError,AttributeError,OSError,RuntimeError,SystemExit) as exc:
        print(json.dumps({'status':'UNAVAILABLE','ok':False,'reason':str(exc)}));return 3

if __name__=='__main__':
    raise SystemExit(main())

import copy
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone
import request_guard_cx1v001 as G
from snapshot_cx1v001 import Snapshot, Refusal
root=Path(__file__).resolve().parent
case=root/'inert_fixtures'/datetime.now(timezone.utc).strftime('request_%Y%m%dT%H%M%S%f')
case.mkdir(parents=True,exist_ok=False)
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def blob(p,b):
    with p.open('xb') as f:f.write(b)
    return pin(p)
def encoded(x):return json.dumps(x,sort_keys=True).encode()
def key(x):return hashlib.sha256(encoded(x)).hexdigest() # inert key function only
passed=[]
def trial(name,mutation=None,missing_plan=False):
    d=case/name;d.mkdir();work=d/'work';work.mkdir();direct=d/'direct';direct.mkdir()
    slots={field:blob(d/(field+'.json'),b'{"inert":true}') for field in ('eps_certificate','lo_certificate')}
    spec={'numerics':{'uv_tail':slots},'test':'inert'}
    raw=encoded(spec); sp=blob(direct/'spec.json',raw)
    theta={'x':1.0}; k=key(theta)
    call={'call_index':0,'key':k,'theta':theta,'spec':spec,'spec_sha256':sp['sha256']}
    plan={'config_sha256':'c'*64,'cache_id':'d'*64,'gate_digest':'e'*64,'calls':[call]}
    pp=work/'waves/wave_0001/WAVE_PLAN.json';pp.parent.mkdir(parents=True)
    args={'work_dir':work,'wave':1,'call_index':0,'config_sha256':'c'*64,'cache_id':'d'*64,'gate_digest':'e'*64,
          'candidate':{'call_dir':str(direct),'theta':copy.deepcopy(theta),'key':k,'spec':sp},
          'mapped':{'spec':copy.deepcopy(spec),'raw':raw,'sha256':sp['sha256'],'key':k},
          'theta_key':key,'cached_keys':set()}
    if mutation:mutation(args,plan)
    args['plan_pin']={'path':str(pp),'sha256':hashlib.sha256(encoded(plan)).hexdigest()}
    if not missing_plan:blob(pp,encoded(plan))
    snap=Snapshot()
    try:result=G.check_request(snap,**args)
    except Refusal:
        if name=='exact':raise
        passed.append(name);return
    assert name=='exact',name
    assert result['prerequisites_only'] and result['original_call_dir']==str(direct)
    assert max(snap.read_counts.values())==1
    passed.append(name)
trial('exact')
trial('before_plan',missing_plan=True)
trial('wrong_config',lambda a,p:a.update(config_sha256='f'*64))
trial('wrong_cache',lambda a,p:a.update(cache_id='f'*64))
trial('wrong_gates',lambda a,p:a.update(gate_digest='f'*64))
trial('unrequested',lambda a,p:a.update(call_index=1))
trial('wrong_theta',lambda a,p:a['candidate'].update(theta={'x':2.0}))
trial('wrong_key',lambda a,p:a['candidate'].update(key='f'*64))
trial('wrong_spec',lambda a,p:a['candidate']['spec'].update(sha256='f'*64))
trial('duplicate',lambda a,p:a['cached_keys'].add(a['candidate']['key']))
trial('duplicate_plan_index',lambda a,p:p['calls'].append(copy.deepcopy(p['calls'][0])))
trial('moved_dir',lambda a,p:a['candidate'].update(call_dir=str(case/'absent')))
# This tests presence/pin prerequisites, not certificate contents/semantics.
trial('uncertified_slot',lambda a,p:p['calls'][0]['spec']['numerics']['uv_tail'].pop('eps_certificate'))
report={'status':'PASS','blocking_count':0,'scope':'request prerequisites only; no admission claim',
        'tested':passed,'untested':['certificate semantic validity','monitor receipt','acceptance','lock integration','whole engine'],
        'pins':[{'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in [Path(G.__file__),Path(__file__)]]}
with (case/'TEST_REPORT.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
print(case/'TEST_REPORT.json')

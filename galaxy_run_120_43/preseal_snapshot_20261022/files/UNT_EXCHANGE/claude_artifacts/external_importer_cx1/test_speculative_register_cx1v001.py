import copy,hashlib,json,tempfile
from pathlib import Path
from snapshot_cx1v001 import Snapshot,Refusal
from speculative_register_cx1v001 import select_registered
b=Path(tempfile.mkdtemp(prefix='register_',dir=Path(__file__).parent/'inert_fixtures')).resolve()
ctx={'config_sha256':'a'*64,'cache_id':'cache','gate_digest':'b'*64}
def pin(n):return {'path':str(b/n),'sha256':'c'*64}
e={'theta_key':'theta','spec':pin('spec'),'driver':pin('driver'),'direct_plan':pin('plan'),'case':'seed','runtime_environment':pin('runtime'),'envelope_phase':'INERT'}
r={'schema':'CX1_SPECULATIVE_REGISTER_V001','context':ctx,'entries':[e]};cases=[]
def check(name,obj,reason=None,match=True,**kw):
 raw=json.dumps(obj).encode();p=b/(name+'.json');p.write_bytes(raw);snap=Snapshot()
 args=dict(register_pin={'path':str(p),'sha256':hashlib.sha256(raw).hexdigest()},context=ctx,theta_key='theta',spec_pin=e['spec'],driver_pin=e['driver']);args.update(kw)
 try:
  got=select_registered(snap,**args);assert reason is None and (got is not None)==match
  assert snap.read_counts=={str(p):1}
 except Refusal as exc:assert reason and reason==str(exc),(name,str(exc))
 cases.append(name)
check('exact',r)
check('unrequested',r,match=False,theta_key='other')
check('different_spec',r,match=False,spec_pin={**e['spec'],'sha256':'d'*64})
check('wrong_driver',r,'REGISTER_DRIVER',driver_pin={**e['driver'],'sha256':'d'*64})
x=copy.deepcopy(r);x['context']['cache_id']='foreign';check('foreign_context',x,'REGISTER_CONTEXT')
x=copy.deepcopy(r);x['entries'].append(copy.deepcopy(e));check('duplicate',x,'REGISTER_AMBIGUOUS_REQUEST')
x=copy.deepcopy(r);x['entries'][0]['status']='COMPLETED_INVALID';check('status_not_authority',x,'REGISTER_ENTRY_SHAPE')
x=copy.deepcopy(r);x['entries'][0]['spec']['sha256']='z'*64;check('bad_pin',x,'REGISTER_PIN')
x=copy.deepcopy(r);x['entries'][0]['envelope_phase']='';check('missing_phase',x,'REGISTER_PHASE')
assert all(not Path(e[k]['path']).exists() for k in ('spec','driver','direct_plan','runtime_environment'))
r={'status':'PASS','blocking_count':0,'scope':'Register metadata selection only','tested':cases,'untested':['Root register authentication','Committed natural-plan binding','Runtime/envelope facts','Terminal status and wait lifecycle']}
p=b/'TEST_REPORT.json';p.write_text(json.dumps(r,indent=2)+'\n');print(p)

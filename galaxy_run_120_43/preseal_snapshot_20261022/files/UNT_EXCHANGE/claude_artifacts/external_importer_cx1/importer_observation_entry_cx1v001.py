"""Read-only prerequisite entry, NOT a campaign installer or admission/launch command.
Root independently supplies the request SHA. A candidate must never choose it.
No files written, science executed, phase END produced, or cache entry admitted.
"""
import sys,json,hashlib,math,types,argparse
from pathlib import Path
LOADER_SHA='8be6c013c1710654c904b0d8f116dde3604cfbab76e48fb04e35ecc6438183f0'
def need(ok,why):
 if not ok:raise ValueError(why)
def read(pin):
 need(type(pin) is dict and set(pin)=={'path','sha256'},'PIN_SHAPE')
 need(type(pin['path']) is str and type(pin['sha256']) is str and len(pin['sha256'])==64 and all(c in '0123456789abcdef' for c in pin['sha256']),'PIN_FORMAT')
 p=Path(pin['path']);need(p.is_absolute() and str(p.resolve())==str(p),'PIN_PATH')
 raw=p.read_bytes();need(hashlib.sha256(raw).hexdigest()==pin['sha256'],'PIN_HASH');return raw

def strict(raw):
 def pairs(items):
  d={}
  for k,v in items:
   need(k not in d,'JSON_DUPLICATE');d[k]=v
  return d
 def bad(v):raise ValueError('JSON_NONFINITE')
 obj=json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_constant=bad)
 def finite(v):
  if isinstance(v,float):need(math.isfinite(v),'JSON_NONFINITE')
  elif isinstance(v,dict):
   for x in v.values():finite(x)
  elif isinstance(v,list):
   for x in v:finite(x)
 finite(obj);return obj

def observe(request_pin):
 need(sys.flags.isolated==1 and sys.flags.dont_write_bytecode==1,'ISOLATED_NO_BYTECODE_REQUIRED')
 request=strict(read(request_pin))
 fields={'schema','policy','entry','root_binding','context','key','spec'}
 need(type(request) is dict and set(request)==fields and request['schema']=='CX1_OBSERVATION_REQUEST_V001','REQUEST_SCHEMA')
 own=Path(__file__).resolve();need(request['entry']['path']==str(own),'ENTRY_PATH');read(request['entry'])
 policy=strict(read(request['policy']))
 need(type(policy) is dict and policy.get('schema')=='CX1_IMPORTER_POLICY_DRAFT_V001','POLICY_SCHEMA')
 loader=own.parent/'pinned_helper_loader_cx1v001.py'
 raw=read({'path':str(loader),'sha256':LOADER_SHA})
 module=types.ModuleType('_cx1_verified_loader');module.__file__=str(loader)
 exec(compile(raw,str(loader),'exec'),module.__dict__)
 load=module.prepare(policy['components'])
 snapshot=load('snapshot_cx1v001').Snapshot()
 bound=load('importer_root_binding_cx1v001').load(snapshot,binding_pin=request['root_binding'],expected_policy=request['policy'],expected_entry=request['entry'],context=request['context'])
 result=load('registered_envelope_runtime_cx1v001').check(snapshot,**bound,key=request['key'],spec_pin=request['spec'])
 return {'status':'PREREQUISITES_ONLY','registered':result['registered'],'admission_authorized':False,'launch_authorized':False,'final_END':False,'root_request':request_pin,'checks':result}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--request',required=True);p.add_argument('--request-sha256',required=True);a=p.parse_args()
 try:result=observe({'path':a.request,'sha256':a.request_sha256})
 except BaseException as exc:
  print(json.dumps({'status':'REFUSED','reason':str(exc),'admission_authorized':False}),file=sys.stderr);return 2
 print(json.dumps(result,sort_keys=True,allow_nan=False));return 0
if __name__=='__main__':sys.exit(main())

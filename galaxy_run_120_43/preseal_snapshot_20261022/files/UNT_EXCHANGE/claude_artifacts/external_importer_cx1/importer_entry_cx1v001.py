"""Root-authenticated importer bootstrap; no launch unless root passes --run.
Root supplies the invocation pin independently. Digest integrity alone does not
establish authorship. Candidates and cached records never select these anchors.
"""
import argparse,hashlib,json,math,sys,time,types
from pathlib import Path
LOADER_SHA='393263c91c67b57b2dc7ee4c5519dade06ad94c2e72fee82d21f1708555ab16a'

def need(ok,why):
 if not ok:raise ValueError(why)
def read(pin):
 need(type(pin) is dict and set(pin)=={'path','sha256'},'ENTRY_PIN_SHAPE')
 path=Path(pin['path']);need(path.is_absolute() and str(path.resolve())==str(path),'ENTRY_PIN_PATH')
 raw=path.read_bytes();need(hashlib.sha256(raw).hexdigest()==pin['sha256'],'ENTRY_PIN_HASH')
 return raw

def strict(raw):
 def pairs(items):
  out={}
  for k,v in items:need(k not in out,'ENTRY_DUPLICATE_KEY');out[k]=v
  return out
 def bad(v):raise ValueError('ENTRY_NONFINITE_JSON')
 obj=json.loads(raw,object_pairs_hook=pairs,parse_constant=bad)
 def check(v):
  if isinstance(v,float):need(math.isfinite(v),'ENTRY_NONFINITE_JSON')
  elif isinstance(v,dict):
   for x in v.values():check(x)
  elif isinstance(v,list):
   for x in v:check(x)
 check(obj);return obj

def build(request_pin):
 need(sys.flags.isolated==1 and sys.flags.dont_write_bytecode==1,'ENTRY_ISOLATED_NO_BYTECODE_REQUIRED')
 request=strict(read(request_pin))
 fields={'schema','status','actor','policy','entry','root_binding','campaign_entry','wrapper','config','acceptance_deps','acceptance_entry','scheduler','records_root','max_polls','poll_seconds','run'}
 need(type(request) is dict and set(request)==fields and request['schema']=='CX1_IMPORTER_INVOCATION_V001','ENTRY_REQUEST_SCHEMA')
 need(request['status']=='ROOT_BOUND' and request['actor']=='Claude2','ENTRY_ROOT_INVOCATION_REQUIRED')
 own=Path(__file__).resolve();need(request['entry']['path']==str(own),'ENTRY_SELF_PATH');read(request['entry'])
 policy=strict(read(request['policy']))
 need(policy.get('schema')=='CX1_IMPORTER_POLICY_V007' and policy.get('status')=='FROZEN_REVIEW_CANDIDATE','ENTRY_POLICY_SCHEMA')
 need(type(request['max_polls']) is int and request['max_polls']>0,'ENTRY_POLL_LIMIT')
 need(type(request['poll_seconds']) in (int,float) and math.isfinite(request['poll_seconds']) and request['poll_seconds']>0,'ENTRY_POLL_INTERVAL')
 run=request['run'];need(type(run) is dict and set(run)=={'max_waves','new_campaign'} and type(run['new_campaign']) is bool,'ENTRY_RUN_FIELDS')
 need(run['max_waves'] is None or type(run['max_waves']) is int and run['max_waves']>0,'ENTRY_WAVE_LIMIT')
 root=Path(request['records_root']);need(root.is_absolute() and root.resolve()==root and root.parent.is_dir(),'ENTRY_RECORDS_ROOT')
 loader_path=own.parent/'pinned_helper_loader_cx1v002.py'
 loader=types.ModuleType('_cx1_root_loader');loader.__file__=str(loader_path)
 exec(compile(read(dict(path=str(loader_path),sha256=LOADER_SHA)),str(loader_path),'exec'),loader.__dict__)
 import numpy as np
 helpers=loader.prepare(policy['components'],runtime_modules={'numpy':np})
 Snapshot=helpers('snapshot_cx1v001').Snapshot
 snapshot=Snapshot()
 for key in ('root_binding','campaign_entry','wrapper','config','acceptance_deps','acceptance_entry','scheduler'):snapshot.pin(request[key])
 entry=types.ModuleType('_cx1_root_campaign_entry');entry.__file__=request['campaign_entry']['path']
 exec(compile(snapshot.pin(request['campaign_entry']),entry.__file__,'exec'),entry.__dict__)
 need(str(entry.WRAPPER)==request['wrapper']['path'] and entry.WRAPPER_SHA==request['wrapper']['sha256'],'ENTRY_PUBLISHED_WRAPPER_BINDING')
 wrapper=entry.load_wrapper();entry.check_patch(wrapper)
 ctx=wrapper.Context(request['config']['path'])
 need(ctx.config_sha256==request['config']['sha256'],'ENTRY_CONTEXT_CONFIG')
 # Collect the private native chain after Context loads engine/monitor/campaign.
 modules=[];seen=set()
 def collect(module):
  if not isinstance(module,types.ModuleType) or id(module) in seen:return
  seen.add(id(module));path=getattr(module,'__file__',None)
  if not isinstance(path,str) or not path.startswith('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/'):return
  modules.append(module)
  for value in list(vars(module).values()):
   if isinstance(value,types.ModuleType):collect(value)
 for module in (wrapper,ctx.E,ctx.M,ctx.C):collect(module)
 installed=helpers('importer_installation_cx1v004').install(wrapper,wrapper_pin=request['wrapper'],campaign_entry_pin=request['campaign_entry'],chain_modules=modules,root_binding_pin=request['root_binding'],policy_pin=request['policy'],entry_pin=request['entry'],deps_pin=request['acceptance_deps'],accept_entry_pin=request['acceptance_entry'],scheduler_pin=request['scheduler'],records_root=request['records_root'],pause=lambda:time.sleep(request['poll_seconds']),max_polls=request['max_polls'])
 orch=installed['Orchestrator'](ctx)
 fresh=Snapshot()
 for key in ('policy','entry','root_binding','campaign_entry','wrapper','config','acceptance_deps','acceptance_entry','scheduler'):fresh.pin(request[key])
 read(request_pin)
 return orch,request

def main(argv=None):
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--request',required=True);parser.add_argument('--request-sha256',required=True)
 parser.add_argument('--run',action='store_true',help='Execute root-selected native campaign run after authenticated installation')
 args=parser.parse_args(argv)
 try:
  orch,request=build(dict(path=args.request,sha256=args.request_sha256))
  if args.run:result=orch.run(**request['run'])
  else:result=dict(status='INSTALLED_NOT_RUN',launches_performed=0,config_sha256=orch.ctx.config_sha256,cache_id=orch.ctx.cache_id,gate_digest=orch.ctx.gate_digest)
 except (KeyboardInterrupt,SystemExit):raise
 except BaseException as exc:
  print(json.dumps(dict(status='REFUSED',reason=type(exc).__name__+': '+str(exc)),sort_keys=True),file=sys.stderr);return 3
 print(json.dumps(result,sort_keys=True,allow_nan=False,default=str))
 return 0 if result.get('status') in ('OK','COMPLETE','INSTALLED_NOT_RUN') else 3
if __name__=='__main__':sys.exit(main())

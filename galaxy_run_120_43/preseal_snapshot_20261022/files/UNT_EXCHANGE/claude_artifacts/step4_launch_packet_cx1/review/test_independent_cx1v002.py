"""Independent bounded gate probes, synthetic data and stub scientific interfaces; no subprocess."""
import copy,hashlib,json,os,sys,types
from pathlib import Path
from unittest.mock import patch
R=Path(__file__).resolve().parent;I=R.parent/'impl';OUT=R/'INDEPENDENT_V002';OUT.mkdir()
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def load(p,name):
 m=types.ModuleType(name);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
G=load(I/'step4_guard_cx1v005.py','independent_guard');L=load(I/'step4_launcher_cx1v005.py','independent_launcher');rows=[]
def ck(n,v,d=None):rows.append({'id':n,'pass':v is True,'detail':d})
def reject(n,fn):
 try:fn()
 except Exception as e:ck(n,True,type(e).__name__+':'+str(e));return
 ck(n,False,'ACCEPTED')
def wj(n,d):
 p=OUT/n
 with p.open('x') as f:json.dump(d,f,allow_nan=False);f.write('\n')
 return pin(p)
for n,s in [('duplicate','{"ok":true,"ok":false}'),('nan','{"x":NaN}'),('infinity','{"x":Infinity}'),('overflow','{"x":1e999}')]:reject(n+'_json',lambda s=s:G.decode(s))
ck('positive_gate_true',G.positive_gate({'ok':True,'reasons':[]}) is None)
for n,g in [('int',{'ok':1,'reasons':[]}),('missing_reasons',{'ok':True}),('reason',{'ok':True,'reasons':['bad']}),('false',{'ok':False,'reasons':[]})]:reject('positive_gate_'+n,lambda g=g:G.positive_gate(g))
for p in ('/private/tmp/KMAX_A2F10_C5H_RUN_V001/x','/private/tmp/UVT_ANY/x','/private/tmp/NGC3198_target.json'):reject('protected_'+p,lambda p=p:G.safe_path(p))
ck('metadata_path_allowed',G.safe_path('/private/tmp/ROOT_DECISIONS_NGC3198_CONSTRUCTION_TEST.md').name=='ROOT_DECISIONS_NGC3198_CONSTRUCTION_TEST.md')
with G.fence():
 reject('fence_process',lambda:sys.audit('subprocess.Popen','x',['x'],None,None))
 reject('fence_write',lambda:(OUT/'SHOULD_NOT_EXIST').open('x'))
 reject('fence_network',lambda:sys.audit('socket.connect',None,('invalid',1)))
ck('fence_no_output',(OUT/'SHOULD_NOT_EXIST').exists() is False)
for f in (None,24,25,100,101,True):ck('first_memory_'+str(f),L.decision(active_route_a=0,free=f,previous_iteration=False,first=True,max_active=3)==(type(f)is int and 25<=f<=100))
ck('cap_at_three',L.decision(active_route_a=3,free=100,previous_iteration=True,first=False,max_active=3) is False)
ck('ramp_missing',L.decision(active_route_a=0,free=100,previous_iteration=False,first=False,max_active=3) is False)
ck('ramp_pass',L.decision(active_route_a=2,free=25,previous_iteration=True,first=False,max_active=3) is True)
for n,b in [('partial',b'{"stage":"iteration_completed","iteration":0}'),('complete',b'{"stage":"iteration_completed","iteration":0}\n'),('wrongtype',b'{"stage":"iteration_completed","iteration":true}\n')]:
 p=OUT/(n+'.jsonl')
 with p.open('xb') as f:f.write(b)
 ck('progress_'+n,L.first_iteration(p)==(n=='complete'))
reject('progress_invalid',lambda:L.G.decode('not json'))
source=OUT/'native_stub.py'
with source.open('x') as f:f.write('# synthetic fixture, never executed\n')
sref=pin(source);cert=wj('cert.json',{});state={'pg':{'ok':True,'reasons':[]},'cg':{'ok':True,'blockers':[]},'sg':{'ok':True,'reasons':[]},'seen':[]}
class Context:
 def __init__(self,c):state['seen'].append('context')
 def certificate_policy_gate(self):state['seen'].append('policy');return state['pg']
 def certificate_check(self,s,p):state['seen'].append('certificate');return state['cg']
 def sensitivity_gate(self,s):state['seen'].append('sensitivity');return state['sg']
 def prelaunch_check(self,s):state['seen'].append('prelaunch');return s
cfg={'sources':{str(source):sref['sha256']},'context_module':sref,'direct_context':sref,'config':cert,'v007':{'verdict':cert},'tail_off_policy':None}
config={'tail_readiness':{'certificate_registry':cert,'certificate_policy_review':cert,'custody_deriver':sref,'state_enumerator':sref,'approved_certificate_producers':[sref]}}
spec={'galaxy':'DDO154','admit':{},'physical':{'distance_Mpc':4.04},'numerics':{'uv_tail':{'enabled':True}}}
call={'case':'S','spec':wj('native_spec.json',spec),'driver':{'path':'/private/tmp/unused_driver.py','sha256':G.R5_SHA},'tail_on':True}
def native_load_stub(ref,cfg,name):
 if name=='_step4_direct_preflight':return types.SimpleNamespace(DIRECT_CONTEXT_API='UNT_STEP4_DIRECT_PREFLIGHT_CX1V001',build=lambda C,config,**kw:Context(config))
 return types.SimpleNamespace(Context=Context)
with patch.object(G,'load',side_effect=native_load_stub),patch.object(G,'adoption',return_value=(config,{'ok':True,'reasons':[]})):
 out=G.native_preflight(cfg,call)
 ck('tail_enabled_true_no_mode',out['adoption_checked'] is True and state['seen']==['context','policy','certificate','sensitivity','prelaunch'])
 for k,reason in [('pg','reasons'),('cg','blockers'),('sg','reasons')]:
  old=state[k];state[k]={'ok':False,reason:['FAIL']};reject('native_'+k+'_negative',lambda:G.native_preflight(cfg,call));state[k]=old
 bad=copy.deepcopy(config);bad['tail_readiness']['certificate_registry']=None
 with patch.object(G,'adoption',return_value=(bad,{'ok':True,'reasons':[]})):reject('null_registry_refused',lambda:G.native_preflight(cfg,call))
result={'schema':'STEP4_INDEPENDENT_PROBES_CX1V002','label':'TESTED_SYNTHETIC_STUBBED_INTERFACES','verdict':'PASS' if all(x['pass'] for x in rows) else 'FAIL','checks':rows,'pins':[pin(I/'step4_guard_cx1v005.py'),pin(I/'step4_launcher_cx1v005.py'),pin(Path(__file__))],'limitations':['Scientific gates are stubbed in interface tests; no native production preflight or monitor launched. Source review, adoption policy, actual certificates and exact-D evidence remain separately gated.','Process/network fence tests raise audit events directly; no process or network attempted.']}
p=OUT/'RESULTS.json'
with p.open('x') as f:json.dump(result,f,indent=1);f.write('\n')
print(json.dumps({'result':pin(p),'total':len(rows),'failed':[x for x in rows if not x['pass']]}))

import ast,types,re,json,hashlib,fcntl,os
from pathlib import Path
from direct_accept_prepare_cx1v001 import prepare,ENTRY_SHA
from snapshot_cx1v001 import Snapshot,Refusal
helper=Path(__file__).parent/'test_valid_admission_cx1v003.py'
exec(compile(helper.read_text().split('passed=[]')[0],str(helper),'exec'),globals())
f=next(n for n in ast.parse(wr).body if isinstance(n,ast.FunctionDef) and n.name=='acceptance_passes')
W.TAILSTATES_PREFIX='ACCEPTANCE_TAILSTATES_';W.TAILSTATES_RE=re.compile(r'ACCEPTANCE_TAILSTATES_C2V002_A([0-9]{3})')
exec(compile(ast.Module(body=[f],type_ignores=[]),str(wrapper),'exec'),W.__dict__)
epath=root.parent/'h3_campaign_path_c2/h3_accept_call_c2v004.py';eraw=epath.read_bytes();assert hashlib.sha256(eraw).hexdigest()==ENTRY_SHA
E=types.ModuleType('fixture_accept_helpers');exec(compile(eraw,str(epath),'exec'),E.__dict__)
epin={'path':str(epath),'sha256':ENTRY_SHA}
policy={k:{} for k in E.POLICY_KEYS};policy['approved_certificate_producers']=ctx.cfg['tail_readiness']['approved_certificate_producers']
deps={k:{'path':str(case/'unused'),'sha256':'a'*64} for k in E.DEP_KEYS}
deps['enumerator']=ctx.cfg['tail_readiness']['state_enumerator'];deps['guard']={'path':G.__file__,'sha256':hashlib.sha256(Path(G.__file__).read_bytes()).hexdigest()}
dp=put(case/'accept_deps.json',{'schema':E.DEPS_SCHEMA,'status':'ROOT_FILLED','deps':deps,'policy':policy})
first=put(case/'incomplete_first.json',{**acceptance,'reading':'INCOMPLETE'})
args=dict(lock=lock,modules=mods,wrapper=W,entry_pin=epin,call=plan_call,candidate=candidate,deps_pin=dp,first_pass=first)
checks=[]
def refuse(name,reason,**over):
 try:prepare(orch,snapshot=Snapshot(),**{**args,**over});raise AssertionError(name)
 except Refusal as exc:assert str(exc)==reason,(name,str(exc))
 checks.append(name)
try:
 got=prepare(orch,snapshot=Snapshot(),**args);assert got['passes_before']==[passdir.name] and got['spec']==spec
 assert lock.held;checks.append('second pass prepared after pinned INCOMPLETE under held lock')
 refuse('missing first record','FIRST_PASS_REQUIRED',first_pass=None)
 refuse('accepted first cannot rerun','FIRST_PASS_NOT_INCOMPLETE_HERE',first_pass=accpin)
 orch.cache.entries[key]={};refuse('already cached','ALREADY_ACCEPTED');orch.cache.entries.clear()
 bad=put(case/'bad_deps.json',{'schema':E.DEPS_SCHEMA,'status':'ROOT_FILLED','deps':{**deps,'enumerator':deps['guard']},'policy':policy})
 refuse('foreign enumerator','ACCEPT_ENUMERATOR',deps_pin=bad)
 (call/'ACCEPTANCE_TAILSTATES_C2V002_A002').mkdir();refuse('third pass prohibited','ACCEPTANCE_RERUN_LIMIT')
finally:fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)
r={'status':'PASS','blocking_count':0,'scope':'Read-only acceptance preparation with pinned helper rules and synthetic Context/dependency values','tested':checks,'untested':['Dependency loading/acceptance execution','Full Context and root auth','First-pass creation path','Concurrent mutation races and whole-engine integration']}
p=case/'ACCEPT_PREP_TEST_REPORT.json';p.write_text(json.dumps(r,indent=2)+'\n');print(p)

import ast,types,re,json,hashlib,fcntl,os
from pathlib import Path
from direct_accept_prepare_cx1v002 import prepare,ENTRY_SHA
from snapshot_cx1v001 import Snapshot,Refusal
helper=Path(__file__).parent/'test_valid_admission_cx1v003.py'
exec(compile(helper.read_text().split('passed=[]')[0].replace('passdir.mkdir()','None'),str(helper),'exec'),globals())
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
 args['first_pass']=None
 got=prepare(orch,snapshot=Snapshot(),**args)
 assert got['passes_before']==[] and got['spec']==spec and not passdir.exists() and lock.held
 checks.append('first pass prepared read-only without creating acceptance directory')
 refuse('first record without prior pass','FIRST_PASS_WITHOUT_PASS',first_pass=first)
 lock.held=False;refuse('unheld lock','WORK_LOCK_REQUIRED');lock.held=True
 refuse('foreign call spec','ACCEPT_SPEC_BINDING',call={**plan_call,'spec_sha256':'0'*64})
 orch.check_identity_now=lambda:['inert identity mismatch']
 refuse('changed work identity','WORK_IDENTITY_CHANGED');orch.check_identity_now=lambda:[]
 passdir.mkdir()
 args['first_pass']=first
 got=prepare(orch,snapshot=Snapshot(),**args);assert got['passes_before']==[passdir.name]
 checks.append('second-pass route remains available only with pinned INCOMPLETE record')
finally:fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)
r={'status':'PASS','blocking_count':0,'scope':'Read-only acceptance preparation with pinned helper rules and synthetic Context/dependency values','tested':checks,'untested':['Dependency loading/acceptance execution','Full Context and root auth','Concurrent mutation races and whole-engine integration']}
p=case/'ACCEPT_FIRST_PREP_TEST_REPORT.json';
with p.open('x') as out:out.write(json.dumps(r,indent=2)+'\n')
print(p)

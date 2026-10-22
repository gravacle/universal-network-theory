"""D021 production-loader source test; no call data or scientific producer invoked."""
import copy,hashlib,json,os,sys,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from snapshot_cx1v001 import Snapshot,Refusal
from acceptance_loader_cx1v001 import load_acceptance
root=Path(__file__).parent;art=root.parent
case=Path(tempfile.mkdtemp(prefix='accept_loader_',dir=root/'inert_fixtures'))
def fence(event,args):
 if event in ('os.remove','os.unlink','os.rename','os.rmdir','shutil.rmtree'):raise PermissionError('NO_MUTATION')
 if event=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
  p=Path(os.fsdecode(args[0]));parts=[x.lower() for x in p.parts]
  if any(x in ('runs','runs_ext','unt_internal_runs','unt_step4_runs') or 'ngc3198' in x or x.startswith('uvt_') for x in parts):raise PermissionError('FORBIDDEN_READ '+str(p))
  mode=args[1];flags=args[2]
  writing=(isinstance(mode,str) and any(c in mode for c in 'wax+')) or (isinstance(flags,int) and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT))
  if writing and (not p.is_relative_to(case) or not flags&os.O_EXCL):raise PermissionError('NONEXCLUSIVE_OR_OUTSIDE '+str(p))
sys.addaudithook(fence)
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def put(name,obj):
 p=case/name
 with p.open('x') as f:json.dump(obj,f,sort_keys=True);f.write('\n')
 return pin(p)
draft=art/'root_thu_checklist_c3/c1_successor/draft_c3v001/C1_H1_DRAFT_C2V003.json'
assert pin(draft)['sha256']=='387b1b35988e83435fc74826a744868d5ff54fbf9f52e5d5d031ef6c792ad1c1'
c1=json.loads(draft.read_bytes());inputs=c1['acceptance_policy_inputs_from_c1'];d=copy.deepcopy(inputs['deps'])
d['guard']=pin(art/'eps_rule_successor_cx2/integration/guard/certificate_guard_b1_a296_cx2v003.py')
policy=copy.deepcopy(inputs['policy']);tail=c1['tail_readiness']
for k in ['approved_certificate_producers','row_policy_reviews','trusted_source_producers']:policy[k]=copy.deepcopy(tail[k])
policy.update(packet_binding_reviews={},approved_review_sha256=[])
doc={'schema':'H3_CAMPAIGN_ACCEPTANCE_DEPS_C2V001','status':'SYNTHETIC','deps':d,'policy':policy}
rp=put('SYNTHETIC_ACCEPT_DEPS.json',doc)
args=dict(record_pin=rp,expected_enumerator=d['enumerator'],expected_guard=d['guard'],expected_producers=policy['approved_certificate_producers'],output_roots=[case/'outputs'],allow_synthetic=True)
snapshot=Snapshot();before=dict(sys.modules)
with load_acceptance(snapshot=snapshot,**args) as loaded:
 assert loaded.deps['pins']==d and callable(loaded.handoff.accept_call)
 assert callable(loaded.deps['lo_adapter']) and callable(loaded.deps['srb_adapter'])
 assert loaded.deps['guard'].__file__==d['guard']['path']
 count=len(loaded.modules)
 assert all(snapshot.read_counts[p['path']]==1 for p in d.values())
 assert max(snapshot.read_counts.values())==1
 touched=[m.__name__ for m in loaded.modules]
assert all((sys.modules.get(k) is before[k]) if k in before else k not in sys.modules for k in touched)
checks=['all eight actual selected dependencies and c2v004 handoff load','D021 A296 guard and ordered seven retained','all source/data snapshot reads counted once','private module registrations restored','no scientific function invoked']
def refusal(name,changes):
 a=dict(args);a.update(changes)
 try:
  with load_acceptance(snapshot=Snapshot(),**a):pass
 except (ValueError,Refusal):checks.append(name)
 else:raise AssertionError(name)
refusal('synthetic record refuses without explicit test flag',{'allow_synthetic':False})
refusal('foreign record pin refuses',{'record_pin':dict(rp,sha256='0'*64)})
refusal('wrong guard refuses',{'expected_guard':dict(d['guard'],sha256='0'*64)})
refusal('producer reorder refuses',{'expected_producers':list(reversed(policy['approved_certificate_producers']))})
bad=copy.deepcopy(doc);bad['deps']['srb_adapter']=None
refusal('null selected dependency refuses before execution',{'record_pin':put('SYNTHETIC_NULL_DEP.json',bad)})
bad=copy.deepcopy(doc);bad['deps']['writer']['sha256']='0'*64
refusal('dependency byte mismatch refuses before execution',{'record_pin':put('SYNTHETIC_WRONG_DEP.json',bad)})
report={'status':'PASS','tested':checks,'loaded_modules':count,'source_reads':len(snapshot.read_counts),'scope':__doc__,'record':rp,'test':pin(Path(__file__)),'loader':pin(root/'acceptance_loader_cx1v001.py'),'untested':['producer invocation on inert or real call','complete installed importer','direct os/io bypass coverage']}
print(put('LOADER_REPORT.json',report))

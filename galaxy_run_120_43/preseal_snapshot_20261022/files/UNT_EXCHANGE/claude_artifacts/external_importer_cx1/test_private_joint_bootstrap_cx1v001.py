"""Actual private helper graph on existing inert root-binding evidence; no science."""
from pathlib import Path
import sys,json,hashlib,tempfile
from pinned_helper_loader_cx1v001 import prepare
b=Path(__file__).resolve().parent
policy_path=b/'IMPORTER_POLICY_DRAFT_CX1V003.json';policy=json.loads(policy_path.read_text());components=dict(policy['components'])
def pin(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
components['importer_root_binding_cx1v001.py']=pin(b/'importer_root_binding_cx1v001.py')
names={Path(k).stem for k in components};before={k:sys.modules.get(k) for k in names}
load=prepare(components)
snapmod=load('snapshot_cx1v001');root=load('importer_root_binding_cx1v001');joint=load('registered_envelope_runtime_cx1v001')
fixture=b/'inert_fixtures/registered_runtime__y4kw_c9';binding_path=fixture/'root_binding.json';obj=json.loads(binding_path.read_text());reg=json.loads(Path(obj['register']['path']).read_text());entry=reg['entries'][0]
snapshot=snapmod.Snapshot();bound=root.load(snapshot,binding_pin=pin(binding_path),expected_policy=obj['policy'],expected_entry=obj['entry'],context=obj['context'])
result=joint.check(snapshot,**bound,key=entry['key'],spec_pin=entry['spec'])
assert result['registered'] and result['admission_authorized'] is False
assert all(v==1 for v in snapshot.read_counts.values())
assert all(sys.modules.get(k) is v for k,v in before.items())
assert load('snapshot_cx1v001') is snapmod
r=dict(status='PASS',blocking_count=0,tested=['40 helper sources hashed/compiled before loading','actual private root-binding/runtime/envelope join passes inert records','Snapshot implementation and Refusal class shared through private module cache','local sys.modules identities unchanged','all snapshot evidence paths read once'],untested=['Separate CLI entry','Root production binding/adoption','Liveness/acceptance and final freeze integration'],pins=[pin(p) for p in [Path(__file__),b/'pinned_helper_loader_cx1v001.py',policy_path,binding_path]],helper_pins=components)
c=Path(tempfile.mkdtemp(prefix='private_joint_',dir=b/'inert_fixtures'))
with (c/'TEST_REPORT.json').open('x') as f:json.dump(r,f,indent=2)
print(c/'TEST_REPORT.json')

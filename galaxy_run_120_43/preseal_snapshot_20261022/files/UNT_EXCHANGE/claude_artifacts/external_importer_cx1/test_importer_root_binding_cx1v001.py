"""Root anchor field binding joined to actual prerequisite checks on inert evidence."""
from pathlib import Path
import runpy,copy,json,hashlib
from snapshot_cx1v001 import Snapshot,Refusal
from importer_root_binding_cx1v001 import load
from registered_envelope_runtime_cx1v001 import check
b=Path(__file__).resolve().parent;g=runpy.run_path(str(b/'test_registered_envelope_runtime_cx1v001.py'));c=g['c'];write=g['write'];args=g['args'];dummy=g['dummy']
root=dict(schema='CX1_IMPORTER_ROOT_BINDING_V001',policy=dummy,entry=dummy,context=args['context'],register=args['register_pin'],binding=args['binding_pin'],runtime=args['runtime_policy'],envelope=args['envelope_policy'])
p=write('root_binding.json',root);s=Snapshot();bound=load(s,binding_pin=p,expected_policy=dummy,expected_entry=dummy,context=args['context'])
r=check(s,**bound,key=args['key'],spec_pin=args['spec_pin']);assert r['registered'] and not r['admission_authorized']
assert all(n==1 for n in s.read_counts.values());passed=['root binding plus actual joined checks use one Snapshot without candidate policy inputs']
for name,change in [('foreign_policy',lambda x:x['policy'].update(sha256='0'*64)),('foreign_entry',lambda x:x['entry'].update(sha256='0'*64)),('foreign_context',lambda x:x['context'].update(cache_id='0'*64)),('missing_envelope',lambda x:x.pop('envelope')),('extra_field',lambda x:x.update(candidate_override={})),('missing_runtime',lambda x:x['runtime'].pop('campaign_capture'))]:
 bad=copy.deepcopy(root);change(bad);bp=write(name+'.json',bad)
 try:load(Snapshot(),binding_pin=bp,expected_policy=dummy,expected_entry=dummy,context=args['context'])
 except Refusal:passed.append(name+' refuses')
 else:raise AssertionError(name)
r=dict(status='PASS',blocking_count=0,tested=passed,untested=['Actual root invocation/authorship and adoption','Separate entry installation','Whole lifecycle and acceptance','Final invalidation consumer freeze'],pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [Path(__file__),b/'importer_root_binding_cx1v001.py',b/'registered_envelope_runtime_cx1v001.py']])
with (c/'ROOT_BINDING_REPORT.json').open('x') as f:json.dump(r,f,indent=2)
print(c/'ROOT_BINDING_REPORT.json')

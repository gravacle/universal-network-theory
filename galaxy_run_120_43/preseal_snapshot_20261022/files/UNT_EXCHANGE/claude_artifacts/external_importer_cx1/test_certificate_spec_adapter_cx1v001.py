"""Actual certificate checker/guard with synthetic policy/custody/state fixture."""
from pathlib import Path
import hashlib,json
from certificate_spec_adapter_cx1v001 import build_checker
from snapshot_cx1v001 import Snapshot,Refusal
from readonly_scope_cx1v001 import ReadOnlyScope
helper=Path(__file__).parent/'test_wrapper_certificate_snapshot_cx1v001.py'
prefix=helper.read_text().split("baseline=W.certificate_check",1)[0]
exec(compile(prefix,str(helper),'exec'),globals())
fn=build_checker(wr,str(wrapper),W)
original=case/'source_spec.json'
with original.open('xb') as f:f.write(Path(sp['path']).read_bytes())
ctx._cx1_original_spec_path=lambda directory:original
snap=Snapshot()
with ReadOnlyScope(snap,[W,O,M,G,monitor]):
 good=fn(ctx,spec,'acceptance',result=result,call_dir=call)
assert good['ok'],good
assert str(original) in snap.read_counts
# Content substitution cannot pass even though the output/archived spec is unchanged.
wrong=put(case/'wrong_original.json',{'wrong':True})
ctx._cx1_original_spec_path=lambda directory:Path(wrong['path'])
with ReadOnlyScope(Snapshot(),[W,O,M,G,monitor]):
 bad=fn(ctx,spec,'acceptance',result=result,call_dir=call)
assert not bad['ok'] and any('SPEC_CONTENT_MISMATCH' in x for x in bad['blockers']),bad
# Local resolver uses the original physical local spec and preserves result.
ctx._cx1_original_spec_path=lambda directory:directory/'spec.json'
with ReadOnlyScope(Snapshot(),[W,O,M,G,monitor]):
 local=fn(ctx,spec,'acceptance',result=result,call_dir=call)
assert local==good,(local,good)
try:build_checker(wr+b'\n',str(wrapper),W);raise AssertionError('wrong source accepted')
except Refusal:pass
report={'status':'PASS','blocking_count':0,'scope':'Explicit-spec certificate method with real pinned guard/monitor and synthetic policy/custody/enumerator','tested':['actual alternate spec read','wrong source spec content refused','local path retains certificate result','wrong wrapper bytes refused'],'untested':['Authenticated resolver','Full Context and production policy','Receipt original spec association (separate custody prerequisite)','Acceptance writer and executor/cache integration']}
p=case/'SPEC_ADAPTER_TEST_REPORT.json';p.write_text(json.dumps(report,indent=2)+'\n');print(p)

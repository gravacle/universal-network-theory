from pathlib import Path
import copy,json
from certificate_spec_adapter_cx1v001 import build_checker
from original_spec_resolver_cx1v001 import OriginalSpecResolver
from snapshot_cx1v001 import Snapshot,Refusal
from readonly_scope_cx1v001 import ReadOnlyScope
helper=Path(__file__).parent/'test_wrapper_certificate_snapshot_cx1v001.py'
exec(compile(helper.read_text().split("baseline=W.certificate_check",1)[0],str(helper),'exec'),globals())
source_spec=put(case/'explicit_source.json',spec)
driver={'path':str(case/'driver.py'),'sha256':driver_sha}
plan=put(case/'direct_plan.json',{'calls':[{'case':'seed','spec':source_spec,'driver':driver,'outdir':str(call/'out'),'receipt':str(call/'RECEIPT.json'),'monitor_log':str(call/'monitor.log')}],'launcher_log':str(case/'batch.log')})
binding={'direct_plan':plan,'case':'seed','spec':source_spec,'driver':driver};work=case/'campaign'
snap=Snapshot();resolver=OriginalSpecResolver(snap,work_dir=work,bindings=[binding]);ctx._cx1_original_spec_path=resolver
checker=build_checker(wr,str(wrapper),W)
with ReadOnlyScope(snap,[W,O,M,G,monitor]):
 result_checked=checker(ctx,spec,'acceptance',result=result,call_dir=call)
assert result_checked['ok'],result_checked
assert resolver(call)==Path(source_spec['path'])
assert resolver(work/'waves/wave_0001/campaign/call_0000')==work/'waves/wave_0001/campaign/call_0000/spec.json'
checks=['bound_checker_acceptance','explicit_source_path','local_path_preserved']
def refuses(name,fn,reason):
 try:fn();raise AssertionError(name)
 except Refusal as exc:assert str(exc)==reason,(name,str(exc))
 checks.append(name)
refuses('unknown_external',lambda:resolver(case/'unknown'),'RESOLVER_UNREGISTERED_EXTERNAL')
refuses('unknown_local',lambda:resolver(work/'other'),'RESOLVER_UNKNOWN_LOCAL_LAYOUT')
refuses('duplicate_root',lambda:OriginalSpecResolver(Snapshot(),work_dir=work,bindings=[binding,binding]),'RESOLVER_DUPLICATE_ROOT')
# A registered plan pointing to the wrong physical output shape is rejected.
p2=put(case/'bad_layout_plan.json',{'calls':[{'case':'seed','spec':source_spec,'driver':driver,'outdir':str(case/'flat_output'),'receipt':str(case/'flat_receipt'),'monitor_log':str(case/'flat_log')}],'launcher_log':str(case/'batch2.log')})
refuses('wrong_layout',lambda:OriginalSpecResolver(Snapshot(),work_dir=work,bindings=[{**binding,'direct_plan':p2}]),'RESOLVER_LAYOUT_NOT_0841')
assert all(n==1 for n in snap.read_counts.values())
r={'status':'PASS','blocking_count':0,'scope':'Resolver plus actual certificate checker/guard with synthetic policy/custody/enumerator','tested':checks,'untested':['Root registration authentication','Live direct plan','Full parent Context','Acceptance writer, executor/cache/wait integration']}
p=case/'RESOLVER_TEST_REPORT.json';p.write_text(json.dumps(r,indent=2)+'\n');print(p)

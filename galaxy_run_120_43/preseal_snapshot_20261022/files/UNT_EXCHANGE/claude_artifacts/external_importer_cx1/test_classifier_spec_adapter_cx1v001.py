from pathlib import Path
import types,json,copy
from classifier_spec_adapter_cx1v001 import build_classifier
from snapshot_cx1v001 import Snapshot,Refusal
from readonly_scope_cx1v001 import ReadOnlyScope
helper=Path(__file__).parent/'test_wrapper_certificate_snapshot_cx1v001.py'
exec(compile(helper.read_text().split("baseline=W.certificate_check",1)[0],str(helper),'exec'),globals())
O.Path=Path;O.CACHED_CLASSES={'VALID','MODEL_INVALID'}
O.collect_evidence=lambda *a:{'files':{},'route_a':{}}
O.tax_record=lambda out,tax:dict(out)
O.forward_from_result=lambda *a:{'valid':True,'speeds_km_s':{}}
fn=build_classifier(parent_raw,str(parent),O)
ctx.driver={'sha256':driver_sha};ctx.row_ids=[]
ctx.taxonomy=types.SimpleNamespace(classify=lambda *a:{'class':'VALID','code':None,'rule':'INERT'})
source_spec=put(case/'classifier_source_spec.json',spec)
ctx._cx1_original_spec_path=lambda d:Path(source_spec['path'])
exe=types.SimpleNamespace(ctx=ctx);pc={'spec_sha256':sp['sha256']};rec={'call_dir':str(call),'status':'OK'}
def classify(status='OK'):
 with ReadOnlyScope(Snapshot(),[O,monitor]):
  return fn(exe,pc,rec,{'call_dir':str(call),'campaign_status':status,'spec_sha256':sp['sha256']})
good=classify();assert good[0]=='VALID',good
ctx._cx1_original_spec_path=lambda d:d/'spec.json'
assert classify()==good
wrong=put(case/'classifier_wrong_spec.json',{'wrong':True})
ctx._cx1_original_spec_path=lambda d:Path(wrong['path'])
assert classify()[:2]==('INFRA','SPEC_FILE_MISMATCH')
assert classify('RUNNING')[:2]==('INFRA','CAMPAIGN_RUNNING')
ctx._cx1_original_spec_path=lambda d:Path(source_spec['path'])
real_monitor=ctx.M
ctx.M=types.SimpleNamespace(verify_receipt=lambda *a,**kw:{'ok':True,'receipt':{**receipt,'status':'STOPPED_WALL'}})
assert classify()[:2]==('INFRA','MONITOR_STOPPED_WALL')
ctx.M=real_monitor
try:build_classifier(parent_raw+b'\n',str(parent),O);raise AssertionError('source accepted')
except Refusal:pass
r={'status':'PASS','blocking_count':0,'scope':'Actual parent _classify with real monitor/finish binding; synthetic evidence and taxonomy; stop receipt double','tested':['external spec valid path','local result unchanged','wrong source spec INFRA','running status INFRA','stopped monitor INFRA','wrong parent bytes refused'],'untested':['Production taxonomy/evidence','Outer classify exception handling','Authenticated resolver and parent integration','Whole-engine replay']}
p=case/'CLASSIFIER_SPEC_TEST_REPORT.json';p.write_text(json.dumps(r,indent=2)+'\n');print(p)

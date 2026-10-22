import copy, hashlib, json
from pathlib import Path
from snapshot_cx1v001 import Snapshot, Refusal
from envelope_guard_cx1v001 import check_envelope
# Reuse only inert manifest construction, before the earlier test execution.
prefix=(Path(__file__).parent/'test_envelope_comparator_cx1v001.py').read_text().split('sp,sh=write(')[0]
exec(compile(prefix,'inert_manifest_fixture','exec'))
tool={'path':str(source),'sha256':sha}
sp,sh=write('start',start);startpin={'path':sp,'sha256':sh}
cases=[]
def check(name,e,reason=None,**overrides):
 ep,eh=write(name,e);snap=Snapshot()
 args=dict(tool_pin=tool,start_pin=startpin,end_pin={'path':ep,'sha256':eh},phase='INERT_ONLY',pin_set=start['pin_set'],required_pins=[{'path':f,'sha256':h}]);args.update(overrides)
 try:
  got=check_envelope(snap,**args)
  assert reason is None,name
  assert got['prerequisites_only'] and snap.read_counts=={str(source):1,sp:1,ep:1}
 except Refusal as exc:
  assert reason and reason in str(exc),(name,str(exc),reason)
 cases.append(name)
check('valid',end)
check('foreign_expected_phase',end,'ENVELOPE_FOREIGN_PHASE',phase='OTHER')
check('missing_coverage',end,'ENVELOPE_REQUIRED_PIN_MISSING',required_pins=[{'path':f+'2','sha256':h}])
check('empty_coverage',end,'ENVELOPE_COVERAGE_REQUIRED',required_pins=[])
e=copy.deepcopy(end);e['files'][0]['ctime_ns']=9;check('rewrite',e,'ENVELOPE_INVALIDATED')
e=copy.deepcopy(end);e['unresolved_pins']=[{}];check('unresolved',e,'ENVELOPE_UNRESOLVED')
e=copy.deepcopy(end);e['files'][0]['sha256_from_bytes']='d'*64;check('wrong_required_hash',e,'ENVELOPE_REQUIRED_PIN_UNMATCHED')
ep,eh=write('duplicate_base',end);p=Path(ep);raw=p.read_bytes();duplicate=raw[:-1]+b', "phase":"INERT_ONLY"}'
dp=b/'duplicate.json';dp.write_bytes(duplicate)
try:
 check_envelope(Snapshot(),tool_pin=tool,start_pin=startpin,end_pin={'path':str(dp),'sha256':hashlib.sha256(duplicate).hexdigest()},phase='INERT_ONLY',pin_set=start['pin_set'],required_pins=[{'path':f,'sha256':h}])
 raise AssertionError('duplicate accepted')
except Refusal as exc:assert 'JSON_DUPLICATE_KEY' in str(exc)
cases.append('duplicate_key')
assert not Path(f).exists()
r={'status':'PASS','blocking_count':0,'scope':'Envelope prerequisite adapter on inert manifests only','tested':cases,'untested':['Root registration authentication','Full required-input coverage','Actual collection/snapshot','Importer integration']}
p=b/'GUARD_TEST_REPORT.json';p.write_text(json.dumps(r,indent=2)+'\n');print(p)

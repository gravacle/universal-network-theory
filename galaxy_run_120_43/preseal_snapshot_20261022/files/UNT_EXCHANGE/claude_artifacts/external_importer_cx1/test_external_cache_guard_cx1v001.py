from pathlib import Path
import json,hashlib,copy
root=Path(__file__).resolve().parent
fixture=root/'test_valid_admission_cx1v003.py'
exec(compile(fixture.read_text().split('passed=[]',1)[0],str(fixture),'exec'),globals())
from external_cache_guard_cx1v001 import check_external_cache
from snapshot_cx1v001 import Snapshot
passed=[]
try:
 got=V.validate_valid(orch,lock=lock,chain_modules=mods,wave_dir=wd,plan=plan,candidate=candidate)
 entry=dict(source='WAVE',classification='VALID',key=key,theta=theta,provenance=got['provenance'])
 put(wd/'WAVE_RESULT.json',{'inert_ingested':True});orch.cache.entries[key]=entry
 def check(e):return check_external_cache(Snapshot(),ctx=ctx,entry=e,theta_key=G.digest)
 assert check(entry)['prerequisites_only'];passed.append('already ingested/cached entry rechecks natural request and custody')
 def refuse(label,mutate):
  e=copy.deepcopy(entry);mutate(e)
  try:check(e)
  except Refusal:passed.append(label)
  else:raise AssertionError(label)
 refuse('foreign cache identity',lambda e:e['provenance']['external_admission'].update(cache_id='f'*64))
 refuse('unrequested cached theta',lambda e:e.update(theta={'x':2.}))
 refuse('foreign original directory',lambda e:e['provenance'].update(call_dir=str(case/'foreign')))
 bad=put(case/'negative_cache_acceptance.json',dict(acceptance,reading='NON_LAPSE_TAIL_MATERIAL'))
 refuse('negative acceptance refuses on replay',lambda e:e['provenance']['external_admission']['candidate'].update(acceptance=bad))
finally:fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)
r=dict(status='PASS',blocking_count=0,scope='External cache prerequisite guard only',tested=passed,untested=['Parent cache self-hash/taxonomy/certificate verification integrated under shared snapshot','Real cache open/put/forward','Root runtime/register/envelope authentication'],pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [Path(__file__),root/'external_cache_guard_cx1v001.py',fixture]])
p=case/'CACHE_GUARD_TEST_REPORT.json'
with p.open('x') as f:json.dump(r,f,indent=2);f.write('\n')
print(p)

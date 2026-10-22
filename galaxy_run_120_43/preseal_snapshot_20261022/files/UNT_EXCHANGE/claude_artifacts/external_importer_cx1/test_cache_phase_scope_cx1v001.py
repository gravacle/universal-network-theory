"""Inert cache wrapper boundary tests with original verifier double; not full parent replay."""
from pathlib import Path
import tempfile,types,json,hashlib,copy
from cache_verify_scope_cx1v003 import make_verifier
from snapshot_cx1v001 import Refusal
from phase_invalidation_cx1v001 import require_use
b=Path(__file__).resolve().parent;c=Path(tempfile.mkdtemp(prefix='cache_phase_',dir=b/'inert_fixtures'))
f=(c/'ORCHESTRATOR.lock').open('x')
lock=types.SimpleNamespace(held=True,_fd=f.fileno(),path=c/'ORCHESTRATOR.lock')
ctx=types.SimpleNamespace(work_dir=c);cache=types.SimpleNamespace(ctx=ctx)
entry={'source':'WAVE','provenance':{'execution_origin':'DIRECT_EXTERNAL'},'key':'inert'}
events=[dict(seq=0,phase_id='INERT',kind='ADMIT',subject='inert')];calls=[];mode='ok'
def phase(ctx,e):calls.append('phase');return require_use(events,'INERT',e['key'])
def original(self,e,stem):
 calls.append('original')
 if mode=='invalidate':events.append(dict(seq=1,phase_id='INERT',kind='FINAL_INVALIDATE',subject=''))
 if mode=='unlock':lock.held=False
 if mode=='mutate':e['key']='foreign'
 return 'VALUE'
v=make_verifier(original,chain_modules=[],phase_use=phase,held_lock=lambda ctx:lock)
assert v(cache,entry,None)=='VALUE' and calls==['phase','original','phase'];assert not hasattr(ctx,'_cx1_cache_snapshot')
passed=['fresh phase check before and after original; transaction cleaned']
def refused():
 try:v(cache,copy.deepcopy(entry),None)
 except Refusal:pass
 else:raise AssertionError('expected refusal')
 assert not hasattr(ctx,'_cx1_cache_snapshot')
for chosen in ['invalidate','unlock','mutate']:
 mode=chosen;events[:]=events[:1];lock.held=True;refused();passed.append(chosen+' during verification refuses and cleans transaction')
mode='ok';lock.held=True;events[:]=events[:1]+[dict(seq=1,phase_id='INERT',kind='FINAL_REFUSAL',subject='')];calls.clear();refused();assert 'original' not in calls
passed.append('already invalid phase refuses before original')
report=dict(status='PASS',blocking_count=0,tested=passed,untested=['Real parent cache replay with phase hook','Authenticated phase journal callback','Actual OS lock acquisition','Consumer freeze and escalation'],pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [Path(__file__),b/'cache_verify_scope_cx1v003.py',b/'phase_invalidation_cx1v001.py']])
with (c/'TEST_REPORT.json').open('x') as out:json.dump(report,out,indent=2)
f.close();print(c/'TEST_REPORT.json')

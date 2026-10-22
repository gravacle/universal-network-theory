"""Actual wrapper Cache methods with explicit parent-cache double and inert certificate evidence."""
from pathlib import Path
import copy,json,hashlib,ast
root=Path(__file__).resolve().parent
fixture=root/'test_cache_certificate_adapter_cx1v003.py'
exec(compile(fixture.read_text().split('\npassed=[]\n',1)[0],str(fixture),'exec'),globals())
ctx.check_cached_certificate=types.MethodType(checker,ctx)
parent_calls=[]
class ParentCache:
 def __init__(self):self.ctx=ctx;self.entries={}
 def forward(self,k):parent_calls.append('forward');return copy.deepcopy(self.entries[k]['forward'])
 def _verify_impl(self,e,stem):parent_calls.append('verify')
 def put(self,**kw):
  parent_calls.append('put');e=copy.deepcopy(kw);self._verify_impl(e,e['key'])
  # Exclusive fixture output proves the read-only certificate scope has ended.
  O.write_fixture(case/'INERT_CACHE_WRITE.json',e)
  self.entries[e['key']]=e;return e,True
exec("def write_fixture(p,e):\n with open(p,'x') as f:json.dump(e,f)",O.__dict__)
W.OldCache=ParentCache
nodes=[n for n in ast.parse(wr).body if isinstance(n,ast.ClassDef) and n.name in ('CertificateRefusal','Cache')]
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(wrapper),'exec'),W.__dict__)
passed=[]
try:
 got=V.validate_valid(orch,lock=lock,chain_modules=mods,wave_dir=wd,plan=plan,candidate=candidate)
 cache=W.Cache()
 e,new=cache.put(key=key,theta=theta,classification='VALID',failure_class=None,source='WAVE',provenance=got['provenance'],forward=got['forward'])
 assert new and parent_calls==['put','verify'] and (case/'INERT_CACHE_WRITE.json').is_file()
 passed.append('actual wrapper pre-put partial and verify full entry pass adapter; parent output remains writable')
 assert cache.forward(key)==got['forward'] and parent_calls[-1]=='forward'
 passed.append('actual wrapper hit validates then returns parent forward')
 old=copy.deepcopy(cache.entries[key])
 cache.entries[key]['provenance']['external_admission']['cache_id']='f'*64
 before=len(parent_calls)
 try:cache.forward(key)
 except Refusal:pass
 else:raise AssertionError('changed identity accepted')
 assert len(parent_calls)==before
 passed.append('adapter refusal escapes before cached value reaches engine')
 cache.entries[key]=old
 bad=copy.deepcopy(old);bad['provenance']['external_admission']['candidate']['case']='foreign'
 try:cache._verify_impl(bad,key)
 except Refusal:pass
 else:raise AssertionError('foreign case accepted')
 assert not hasattr(ctx,'_cx1_original_spec_path')
 passed.append('actual wrapper verify path rejects foreign direct case and leaves resolver restored')
finally:fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)
r=dict(status='PASS',blocking_count=0,scope=__doc__,tested=passed,untested=['Real parent Cache self-hash/taxonomy/custody/open/put','Full generated context and installer','Runtime/register/envelope/wait authentication'],pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [Path(__file__),fixture,wrapper,root/'cache_certificate_adapter_cx1v001.py']])
p=case/'WRAPPER_CACHE_TEST_REPORT.json'
with p.open('x') as f:json.dump(r,f,indent=2);f.write('\n')
print(p)

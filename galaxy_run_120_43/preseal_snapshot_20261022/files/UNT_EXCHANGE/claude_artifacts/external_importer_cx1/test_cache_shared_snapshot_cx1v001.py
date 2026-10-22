from pathlib import Path
import json,hashlib,types
root=Path(__file__).resolve().parent
fixture=root/'test_cache_certificate_adapter_cx1v003.py'
exec(compile(fixture.read_text().split('\npassed=[]\n',1)[0],str(fixture),'exec'),globals())
from cache_certificate_adapter_cx1v002 import make_checker
from cache_verify_scope_cx1v001 import make_verifier
checker=make_checker(W.check_cached_certificate,chain_modules=mods,theta_key=G.digest)
seen=[]
def parent_verify(self,e,k):
 s=ctx._cx1_cache_snapshot;seen.append(s)
 O.sha256_file(e['provenance']['result_path'])
 checker(ctx,e)
 assert O.sha256_file(e['provenance']['result_path'])==e['provenance']['result_sha256']
 return True
verify=make_verifier(parent_verify,chain_modules=mods)
cache=types.SimpleNamespace(ctx=ctx);passed=[]
try:
 got=V.validate_valid(orch,lock=lock,chain_modules=mods,wave_dir=wd,plan=plan,candidate=candidate)
 e=dict(source='WAVE',classification='VALID',key=key,theta=theta,provenance=got['provenance'])
 assert verify(cache,e,key)
 assert all(v==1 for v in seen[-1].read_counts.values()) and rp['path'] in seen[-1].read_counts
 assert not hasattr(ctx,'_cx1_cache_snapshot') and not hasattr(ctx,'_cx1_original_spec_path')
 passed.append('parent read and real wrapper certificate checks share one snapshot buffer per path')
 verify(cache,e,key);assert seen[0] is not seen[1]
 passed.append('separate verification transactions use fresh snapshots')
 def fail(self,e,k):checker(ctx,e);raise RuntimeError('inert')
 try:make_verifier(fail,chain_modules=mods)(cache,e,key)
 except RuntimeError:pass
 else:raise AssertionError('failure swallowed')
 assert not hasattr(ctx,'_cx1_cache_snapshot') and not hasattr(ctx,'_cx1_original_spec_path')
 passed.append('exception restores both context slots')
 ctx._cx1_cache_snapshot=object()
 try:verify(cache,e,key)
 except Refusal:pass
 else:raise AssertionError('nested accepted')
 del ctx._cx1_cache_snapshot
 passed.append('nested verification transaction refuses')
finally:fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)
p=case/'CACHE_SHARED_SNAPSHOT_TEST_REPORT.json'
r=dict(status='PASS',blocking_count=0,scope='Shared cache validation scope; parent verifier is explicit double',tested=passed,untested=['Actual parent cache verifier and dynamic loaders','Production installation and full cache lifecycle'],pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [Path(__file__),root/'cache_verify_scope_cx1v001.py',root/'cache_certificate_adapter_cx1v002.py',fixture]])
with p.open('x') as f:json.dump(r,f,indent=2);f.write('\n')
print(p)

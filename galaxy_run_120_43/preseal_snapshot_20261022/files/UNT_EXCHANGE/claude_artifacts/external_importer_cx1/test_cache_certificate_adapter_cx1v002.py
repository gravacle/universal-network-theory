from pathlib import Path
import ast,copy,json,hashlib
root=Path(__file__).resolve().parent
fixture=root/'test_valid_admission_cx1v003.py'
exec(compile(fixture.read_text().split('O.CACHED_CLASSES=('VALID','MODEL_INVALID')
W.TAIL_INVALID_SOURCE='TAIL_ACCEPTANCE_CERTIFIED'
passed=[]',1)[0],str(fixture),'exec'),globals())
from cache_certificate_adapter_cx1v001 import make_checker
# Extract unchanged original wrapper method; full wrapper globals are private fixture modules.
tree=ast.parse(wr)
cl=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='Context')
fn=next(n for n in cl.body if isinstance(n,ast.FunctionDef) and n.name=='check_cached_certificate')
exec(compile(ast.Module(body=[fn],type_ignores=[]),str(wrapper),'exec'),W.__dict__)
# The fixture defines real certificate checker as a free function, so bind it to context.
ctx.certificate_check=types.MethodType(W.certificate_check,ctx)
checker=make_checker(W.check_cached_certificate,chain_modules=mods,theta_key=G.digest)
O.CACHED_CLASSES=('VALID','MODEL_INVALID')
W.TAIL_INVALID_SOURCE='TAIL_ACCEPTANCE_CERTIFIED'
passed=[]
try:
 got=V.validate_valid(orch,lock=lock,chain_modules=mods,wave_dir=wd,plan=plan,candidate=candidate)
 entry=dict(source='WAVE',classification='VALID',key=key,theta=theta,provenance=got['provenance'])
 original=copy.deepcopy(entry)
 checker(ctx,entry);assert entry==original and not hasattr(ctx,'_cx1_original_spec_path')
 passed.append('full entry passes original wrapper certificate method plus external prerequisites')
 partial=copy.deepcopy(entry);del partial['key'];before=copy.deepcopy(partial)
 checker(ctx,partial);assert partial==before
 passed.append('pre-put partial entry derives key without mutating caller')
 bad=copy.deepcopy(entry);bad['key']='f'*64
 try:checker(ctx,bad)
 except Refusal as ex:assert 'EXTERNAL_CACHE_KEY' in str(ex)
 else:raise AssertionError('wrong key')
 passed.append('supplied wrong key refuses')
 sentinel=object();ctx._cx1_original_spec_path=sentinel
 checker(ctx,entry);assert ctx._cx1_original_spec_path is sentinel
 del ctx._cx1_original_spec_path
 passed.append('existing resolver restored')
 def fail(self,e):raise RuntimeError('INERT original checker failure')
 failing=make_checker(fail,chain_modules=mods,theta_key=G.digest)
 try:failing(ctx,entry)
 except RuntimeError:pass
 else:raise AssertionError('failure swallowed')
 assert not hasattr(ctx,'_cx1_original_spec_path')
 passed.append('original checker failure restores resolver')
 seen=[]
 normal=make_checker(lambda self,e:seen.append(e),chain_modules=mods,theta_key=G.digest)
 local={'classification':'INFRA'};normal(ctx,local);assert seen==[local]
 passed.append('nonexternal entries retain original checker')
finally:fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)
p=case/'CACHE_CERT_ADAPTER_TEST_REPORT.json'
r=dict(status='PASS',blocking_count=0,scope='Private adapter with actual wrapper method/certificate/monitor and synthetic context',tested=passed,untested=['Production Context and cache lifecycle','Parent selfhash/taxonomy verifier shared snapshot','Authenticated runtime/register/envelope integration'],pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [Path(__file__),root/'cache_certificate_adapter_cx1v001.py',fixture,wrapper]])
with p.open('x') as f:json.dump(r,f,indent=2);f.write('\n')
print(p)

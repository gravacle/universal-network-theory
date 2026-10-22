"""Combined actual parent and wrapper WAVE cache verification; synthetic mapper/taxonomy."""
from pathlib import Path
import ast,copy,json,hashlib,re
root=Path(__file__).resolve().parent
fixture=root/'test_valid_admission_cx1v003.py'
source=fixture.read_text().split('passed=[]',1)[0]
source=source.replace("exec(compile(text,str(helper),'exec'),globals())", "text=text.replace(\"result={'status':\",\"result={'speeds_km_s':{},'status':\")\nexec(compile(text,str(helper),'exec'),globals())")
exec(compile(source,str(fixture),'exec'),globals())
from cache_verify_scope_cx1v001 import make_verifier
pt=ast.parse(parent_raw)
names={'canonical','collect_evidence','tax_record','forward_from_result','receipt_and_finish_custody'}
nodes=[n for n in pt.body if isinstance(n,ast.FunctionDef) and n.name in names]
pc=next(n for n in pt.body if isinstance(n,ast.ClassDef) and n.name=='Cache')
method=next(n for n in pc.body if isinstance(n,ast.FunctionDef) and n.name=='_verify_impl')
O.re=re;O.ast=ast;O.OrchestratorError=ValueError;O.theta_key=G.digest
O.SCHEMA_CACHE_ENTRY='DDO154_CALIBRATION_CACHE_ENTRY_C2V004';O.CACHED_CLASSES=('VALID','MODEL_INVALID')
exec(compile(ast.Module(body=nodes+[method],type_ignores=[]),str(parent),'exec'),O.__dict__)
ctx.row_ids=[]
out=dict(rule='INERT',code=None,**{'class':'VALID','judgment_call':False})
ctx.taxonomy=types.SimpleNamespace(sha256='a'*64,classify=lambda result,evidence:out)
ctx.mapper=types.SimpleNamespace(build=lambda theta,recovery=None:mapped)
from cache_certificate_adapter_cx1v002 import make_checker
wt=ast.parse(wr)
wc=next(n for n in wt.body if isinstance(n,ast.ClassDef) and n.name=='Context')
cm=next(n for n in wc.body if isinstance(n,ast.FunctionDef) and n.name=='check_cached_certificate')
exec(compile(ast.Module(body=[cm],type_ignores=[]),str(wrapper),'exec'),W.__dict__)
W.TAIL_INVALID_SOURCE='TAIL_ACCEPTANCE_CERTIFIED'
ctx.certificate_check=types.MethodType(W.certificate_check,ctx)
ctx.check_cached_certificate=types.MethodType(make_checker(W.check_cached_certificate,chain_modules=mods,theta_key=G.digest),ctx)
class ParentCache:
 _verify_impl=O._verify_impl
 def forward(self,key):return copy.deepcopy(self.entries[key]['forward'])
W.OldCache=ParentCache
nodes=[n for n in wt.body if isinstance(n,ast.ClassDef) and n.name in ('Cache','CertificateRefusal')]
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(wrapper),'exec'),W.__dict__)
verify=make_verifier(W.Cache._verify_impl,chain_modules=mods)
cache=W.Cache();cache.ctx=ctx;cache.entries={}
passed=[]
try:
 ev=O.collect_evidence(call/'out',result,[],ctx.taxonomy);assert not ev['errors']
 fin,why=O.finish_binding(rp['path'],rp['sha256']);assert not why
 pv=dict(execution_origin='DIRECT_EXTERNAL',result_path=rp['path'],result_sha256=rp['sha256'],spec_sha256=sp['sha256'],receipt_path=str(receipt_path),receipt_file_sha256=hashlib.sha256(receipt_path.read_bytes()).hexdigest(),receipt_sha256_self=receipt['receipt_sha256'],finish=fin,evidence_files=ev['files'],taxonomy=O.tax_record(out,ctx.taxonomy))
 got=V.validate_valid(orch,lock=lock,chain_modules=mods,wave_dir=wd,plan=plan,candidate=candidate)
 pv.update(got['provenance'])
 e=dict(schema=O.SCHEMA_CACHE_ENTRY,cache_id=ctx.cache_id,key=key,theta=theta,source='WAVE',classification='VALID',failure_class=None,forward={'valid':True,'speeds_km_s':{},'reasons':[]},provenance=pv)
 def seal(e):e['entry_sha256']=hashlib.sha256(O.canonical({k:v for k,v in e.items() if k!='entry_sha256'})).hexdigest()
 seal(e);verify(cache,e,key);passed.append('actual parent WAVE verifier passes inert evidence and real receipt/finish binding')
 def refuses(label,mutate,reseal=True):
  bad=copy.deepcopy(e);mutate(bad)
  if reseal:seal(bad)
  try:verify(cache,bad,key)
  except (ValueError,Refusal):passed.append(label)
  else:raise AssertionError(label)
  assert not hasattr(ctx,'_cx1_cache_snapshot')
 cache.entries[key]=e
 assert cache.forward(key)==e['forward']
 passed.append('actual wrapper forward certificate path returns validated inert entry')
 refuses('entry self hash',lambda e:e.update(entry_sha256='0'*64),False)
 refuses('receipt hash',lambda e:e['provenance'].update(receipt_file_sha256='0'*64))
 refuses('evidence set',lambda e:e['provenance'].update(evidence_files={}))
 refuses('taxonomy rederivation',lambda e:e['provenance']['taxonomy'].update(rule='foreign'))
 refuses('forward rederivation',lambda e:e['forward'].update(reasons=['foreign']))
finally:fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)
p=case/'COMBINED_CACHE_TEST_REPORT.json'
r=dict(status='PASS',blocking_count=0,scope=__doc__,tested=passed,untested=['Production mapper/taxonomy','Full cache open/put lifecycle','Authenticated importer installation'],pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [Path(__file__),fixture,parent,wrapper,root/'cache_verify_scope_cx1v001.py',root/'cache_certificate_adapter_cx1v002.py']])
with p.open('x') as f:json.dump(r,f,indent=2);f.write('\n')
print(p)

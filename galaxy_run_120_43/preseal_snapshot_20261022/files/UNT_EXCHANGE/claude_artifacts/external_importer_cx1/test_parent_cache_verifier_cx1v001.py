"""Actual parent WAVE cache verifier; synthetic mapper/taxonomy, real evidence/monitor/finish functions."""
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
verify=make_verifier(O._verify_impl,chain_modules=mods)
cache=types.SimpleNamespace(ctx=ctx)
passed=[]
try:
 ev=O.collect_evidence(call/'out',result,[],ctx.taxonomy);assert not ev['errors']
 fin,why=O.finish_binding(rp['path'],rp['sha256']);assert not why
 pv=dict(execution_origin='DIRECT_EXTERNAL',result_path=rp['path'],result_sha256=rp['sha256'],spec_sha256=sp['sha256'],receipt_path=str(receipt_path),receipt_file_sha256=hashlib.sha256(receipt_path.read_bytes()).hexdigest(),receipt_sha256_self=receipt['receipt_sha256'],finish=fin,evidence_files=ev['files'],taxonomy=O.tax_record(out,ctx.taxonomy))
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
 refuses('entry self hash',lambda e:e.update(entry_sha256='0'*64),False)
 refuses('receipt hash',lambda e:e['provenance'].update(receipt_file_sha256='0'*64))
 refuses('evidence set',lambda e:e['provenance'].update(evidence_files={}))
 refuses('taxonomy rederivation',lambda e:e['provenance']['taxonomy'].update(rule='foreign'))
 refuses('forward rederivation',lambda e:e['forward'].update(reasons=['foreign']))
finally:fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)
p=case/'PARENT_CACHE_TEST_REPORT.json'
r=dict(status='PASS',blocking_count=0,scope=__doc__,tested=passed,untested=['Production mapper/taxonomy','Combined wrapper and parent full lifecycle','Authenticated importer installation'],pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [Path(__file__),fixture,parent,root/'cache_verify_scope_cx1v001.py']])
with p.open('x') as f:json.dump(r,f,indent=2);f.write('\n')
print(p)

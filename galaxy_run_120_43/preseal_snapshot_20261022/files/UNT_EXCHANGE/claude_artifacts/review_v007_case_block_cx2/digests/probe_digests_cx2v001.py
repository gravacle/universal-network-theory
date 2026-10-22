"""Owned ten-case uv_tail config digest recomputation. Pure AST normalizer only; no pipeline, cert or run traversal."""
import ast,copy,hashlib,json,math,os,sys,unicodedata
from pathlib import Path
A=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts');OUT=A/'review_v007_case_block_cx2/digests'
CB=A/'v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json';BUILD=A/'v007_final_prereg_c4/r5/out/CASE_BLOCK_BUILD_C4V001.json';CMP=A/'v007_compare_c2/r12/kmax_tail_compare_c2v007_r12_cx3v002.py';LIB=A/'tail_scheme_impl_c2/module/owned_uv_tail_lapse_v001.py'
PINS={CB:'76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71',BUILD:'bcf560de77cd42f67fedb62744df0723a052c1f2ffc4f4b2a7bed874eb5b59ad',CMP:'4bd7b262caae26f2de146cee803dd689a1f4e565cb67552f04e6d6b97188dd28',LIB:'c28d4209dc617708e1ae4d1d568ecf88d79fa926847f0ac050748642e6990b22'}
allowed=set(str(p) for p in PINS)|{__file__};blocked=[];reads=[];checks=[]
def guard(p,op):
 if isinstance(p,int):return
 s=os.path.abspath(os.fsdecode(p));n=unicodedata.normalize('NFC',s).casefold().replace('/system/volumes/data','')
 if any(t in Path(n).parts for t in ('runs','runs_ext','.codex','.vol')) or 'kmax_a2f10_c5h' in n or ('ngc3198' in n and any(t in n for t in ('observed','target','rotmod'))):blocked.append([op,s]);raise PermissionError('PROTECTED_PATH')
 if s in allowed or s.startswith(str(OUT)+'/'):return
 if op=='metadata' and any(t.startswith(s.rstrip('/')+'/') for t in allowed|{str(OUT)}):return
 blocked.append([op,s]);raise PermissionError('ALLOWLIST_ONLY')
for name in ('stat','lstat','readlink'):
 old=getattr(os,name)
 def f(p,*a,_old=old,**kw):guard(p,'metadata');return _old(p,*a,**kw)
 setattr(os,name,f)
def audit(e,a):
 if e=='open':
  guard(a[0],'open')
  if a[2]&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC):assert str(a[0]).startswith(str(OUT)+'/') and a[2]&os.O_EXCL
  else:reads.append(str(a[0]))
 elif e in ('os.listdir','os.scandir'):raise PermissionError('NO_TRAVERSAL')
 elif e.startswith(('subprocess.','socket.')) or e in ('os.system','os.exec','os.posix_spawn','os.remove','os.rename','os.rmdir','os.link','os.symlink'):raise PermissionError('NO_PROCESS_MUTATION')
sys.addaudithook(audit)
def sha(b):return hashlib.sha256(b).hexdigest()
def hook(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise ValueError('DUPLICATE_JSON_KEY')
  d[k]=v
 return d
def canon(d):return json.dumps(d,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def add(n,expected,actual):checks.append({'id':n,'status':'TESTED','expected':expected,'actual':actual,'pass':expected==actual})
raw={p:p.read_bytes() for p in list(PINS)+[Path(__file__)]};actual={str(p):{'path':str(p),'sha256':sha(b),'bytes':len(b)} for p,b in raw.items()}
for p,h in PINS.items():assert sha(raw[p])==h,(p,sha(raw[p]))
cb=json.loads(raw[CB],object_pairs_hook=hook);build=json.loads(raw[BUILD],object_pairs_hook=hook)
ct=ast.parse(raw[CMP]);pin=next(n for n in ct.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PIN_UVT_LIB' for t in n.targets))
# Only the recorded constant tuple is evaluated, with ART fixed to this permitted artifact root.
assert isinstance(pin.value,ast.Tuple) and len(pin.value.elts)==2
libpin=eval(compile(ast.Expression(pin.value),str(CMP),'eval'),{'__builtins__':{},'ART':str(A)})
add('r12_declared_library_path',str(LIB),libpin[0]);add('r12_declared_library_bytes',PINS[LIB],libpin[1]);add('builder_compare_metadata',{'path':str(CMP),'sha256':PINS[CMP]}, {k:build['compare'][k] for k in ('path','sha256')})
lt=ast.parse(raw[LIB]);names={'Refusal','_canon','_sha','_pos_float','_strict','normalize_config'};constnames={'CONFIG_SCHEMA','TEST_ONLY_CERT'}
selected=[n for n in lt.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names]
selected +=[n for n in lt.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in constnames for t in n.targets)]
assert len(selected)==8
ns={'json':json,'math':math,'hashlib':hashlib}
exec(compile(ast.Module(body=selected,type_ignores=[]),str(LIB),'exec'),ns)
labels=[s for s,c in cb['cases'].items() if c.get('tail') is True];add('ten_tail_cases',10,len(labels));rows=[]
for lab in labels:
 e=cb['cases'][lab];uv=e['normalized_spec_equal']['/numerics']['uv_tail'];before=canon(uv);nreads=len(reads);n=ns['normalize_config'](uv);add(lab+'_normalizer_no_file_reads',nreads,len(reads));add(lab+'_input_unchanged',sha(before),sha(canon(uv)))
 got=n['sha256'];body={k:v for k,v in n.items() if k!='sha256'};independent=sha(canon(body));add(lab+'_declared_digest',e['uv_tail_config_sha256'],got);add(lab+'_independent_sha256_of_canonical_bytes',got,independent)
 # Different dict insertion order must not change canonical identity.
 def reversed_keys(x):
  if isinstance(x,dict):return {k:reversed_keys(x[k]) for k in reversed(list(x))}
  if isinstance(x,list):return [reversed_keys(v) for v in x]
  return x
 add(lab+'_mapping_order_invariant',got,ns['normalize_config'](reversed_keys(uv))['sha256'])
 changed=copy.deepcopy(uv);changed['domain']['R_eval_max_kpc']=math.nextafter(changed['domain']['R_eval_max_kpc'],math.inf);add(lab+'_domain_bit_change_bound',True,ns['normalize_config'](changed)['sha256']!=got)
 changed=copy.deepcopy(uv);changed['eps_certificate']['sha256']='0'*64;add(lab+'_certificate_pin_bound_in_digest',True,ns['normalize_config'](changed)['sha256']!=got)
 rows.append({'case':lab,'declared':e['uv_tail_config_sha256'],'normalizer_sha256':got,'independent_canonical_sha256':independent,'canonical_byte_count':len(canon(body)),'outer':n['outer'],'source_rule':n['source_rule'],'lambda_scale':n['lambda_scale'],'gas_M_s':n['gas']['M_s']})
# Strict shape/type controls are scoped to normalization, not certificate validity.
u=copy.deepcopy(cb['cases'][labels[0]]['normalized_spec_equal']['/numerics']['uv_tail'])
for name,field,value in [('unknown_top','unexpected',1),('boolean_lambda','lambda_scale',True),('nan_lambda','lambda_scale',float('nan'))]:
 x=copy.deepcopy(u);x[field]=value
 try:ns['normalize_config'](x);code='ACCEPTED'
 except ns['Refusal'] as ex:code=ex.code
 add(name,'UV_TAIL_CONFIG_INVALID',code)
for p,b in raw.items():add('end_pin_'+p.name,sha(b),sha(p.read_bytes()))
add('zero_protected_access_attempts',[],blocked)
result={'date_u':os.environ['REVIEW_DATE_U'],'verdict':'PASS' if all(x['pass'] for x in checks) else 'FAIL','counts':{'checks':len(checks),'passed':sum(x['pass'] for x in checks),'failed':sum(not x['pass'] for x in checks),'tail_config_digests':len(rows)},'digests':rows,'tests':checks,'input_pins':list(actual.values()),'selected_library':{'path':libpin[0],'sha256':libpin[1]},'AST_selected_functions_classes':sorted(names),'AST_selected_constants':sorted(constnames),'external_reads':sorted(set(reads)),'blocked':blocked,'scope':'Recompute each declared tail config digest from the candidate whole-numerics uv_tail, using only exact r12-pinned pure normalizer AST plus independent canonical-byte SHA256. No compare/driver/pipeline import, no source/evaluator execution, no certificate references opened.','limitations':['Case-block structure and spec/dry joins reviewed by other lanes.','Certificate bytes, validity and admission not verified here; only their literal path/sha inclusion in config identity checked.','No scientific launch or numerical solver; no full compare or real run evidence read.']}
p=OUT/'RESULTS_CX2V001.json';b=(json.dumps(result,indent=1,allow_nan=False)+'\n').encode()
with p.open('xb') as f:f.write(b)
print(json.dumps({'path':str(p),'sha256':sha(b),'counts':result['counts'],'verdict':result['verdict'],'digests':rows,'failed':[t for t in checks if not t['pass']]}))

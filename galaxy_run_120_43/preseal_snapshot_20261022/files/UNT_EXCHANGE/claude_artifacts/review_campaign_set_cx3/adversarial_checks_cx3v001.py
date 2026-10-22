"""A205 extra boundary probes. Exact source AST functions, synthetic fixtures only.
Ledger guard/producers and receipt verification are stand-ins: tests concern orchestration/binding,
not certificate mathematics or independent receipt validation. Whole-chain suites cover integration.
"""
import ast,copy,hashlib,json,os,re,stat,subprocess,types
from pathlib import Path
H=Path(__file__).parent;A=H.parent;D=A/'h3_campaign_path_c2';S=H/'adversarial_scratch_cx3v001'
S.mkdir();rows=[];sources=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def digest(x):return sha(canonical(x))
def pin(p):return {'path':str(p),'sha256':sha(p.read_bytes())}
def put(name,obj=None,raw=None):
 p=S/name;p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(raw if raw is not None else canonical(obj))
 return pin(p)
def readpin(p,*a):
 b=Path(p['path']).read_bytes()
 if sha(b)!=p['sha256']:raise ValueError('pin mismatch')
 return b

def check(name,ok,detail=None,same_path=False):
 rows.append({'case':name,'passed':bool(ok),'detail':detail,'same_path':same_path});assert ok,name

def subset(path,functions,constants=(),classes=()):
 raw=path.read_bytes();tree=ast.parse(raw);selected=[]
 for n in tree.body:
  if isinstance(n,ast.FunctionDef) and n.name in functions or isinstance(n,ast.ClassDef) and n.name in classes:selected.append(n)
  elif isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in constants for t in n.targets):selected.append(n)
 env={'Path':Path,'json':json,'os':os,'re':re,'stat':stat,'hashlib':hashlib,'Error':ValueError,'GiB':1<<30,'__file__':str(path)}
 exec(compile(ast.Module(body=selected,type_ignores=[]),str(path),'exec'),env)
 sources.append(pin(path));return types.SimpleNamespace(**env),env,tree
F,fe,_=subset(D/'h3_accept_call_c2v004.py',{'f6_action','first_pass_problems'},{'HANDOFF','MAX_PASSES','CERTIFIABLE_INVALID','ACCEPTANCE_RECORD_SCHEMA','RERUNNABLE'})
M=types.SimpleNamespace(Error=ValueError,O=types.SimpleNamespace(read_pinned=readpin))
call=S/'call_first';call.mkdir();passname='ACCEPTANCE_TAILSTATES_C2V002_A001'
base={'schema':F.ACCEPTANCE_RECORD_SCHEMA,'handoff':F.HANDOFF,'call_dir':str(call),'tailstate_dir':str(call/passname),'reading':'INCOMPLETE'}
ref=put('first_good.json',base)
check('first-pass own pinned INCOMPLETE accepted',not F.first_pass_problems(M,call,[passname],ref))
for name,field,value in [('schema','schema','wrong'),('handoff','handoff',{'path':'/other','sha256':'0'*64}),('other call','call_dir',str(S/'foreign')),('other pass','tailstate_dir',str(call/'ACCEPTANCE_TAILSTATES_C2V002_A002')),*[('reading '+s,'reading',s) for s in ['ACCEPTED','ACCEPTED_PASS_FLAGGED','NON_LAPSE_TAIL_MATERIAL','BOUND_INSUFFICIENT','UNKNOWN',None]]]:
 d=copy.deepcopy(base);d[field]=value;p=put('first_bad_%02d.json'%len(rows),d);bad=F.first_pass_problems(M,call,[passname],p);check('first-pass refuses '+name,bool(bad),bad)
for name,p in [('missing',None),('relative',{'path':'relative','sha256':ref['sha256']}),('sha',dict(ref,sha256='0'*64)),('extra',dict(ref,extra=True))]:
 bad=F.first_pass_problems(M,call,[passname],p);check('first-pass refuses pin '+name,bool(bad),bad)
for reading in ['NON_LAPSE_TAIL_MATERIAL','BOUND_INSUFFICIENT']:
 check('F6 '+reading+' eligible',F.f6_action({'reading':reading,'rows_are_model_output':False,'step4_stop_for_root_ruling':False},False).startswith('CERTIFIED_MODEL_INVALID_ELIGIBLE'))
 check('F6 '+reading+' step4 stop halts',F.f6_action({'reading':reading,'rows_are_model_output':False,'step4_stop_for_root_ruling':True},False).startswith('HALT'))
for reading in ['ACCEPTED','ACCEPTED_PASS_FLAGGED']:
 check('F6 '+reading+' accepted maps valid',F.f6_action({'reading':reading},True)=='CACHED_VALID')
for passes in [1,2,3]:
 got=F.f6_action({'reading':'INCOMPLETE','tailstate_dir':'synthetic'},False,passes)
 check('F6 incomplete pass '+str(passes),got.startswith('RERUN' if passes==1 else 'HALT'),got)
for reading in ['LO_UNCERTIFIED_TRANSIENT','UNKNOWN',None]:check('F6 other halt '+str(reading),F.f6_action({'reading':reading},False).startswith('HALT'))

W,we,tr=subset(D/'calibration_orchestrator_q5b1_ledger_c2v004.py',{'acceptance_passes','latest_pass_problems','tail_invalid_forward'}, {'TAILSTATES_PREFIX','TAILSTATES_RE','LEDGER_SCHEMA','LEDGER_NAME','LEDGER_ENTRY_SCHEMA'})
for name,nums in [('one',[1]),('two',[1,2]),('gap',[1,3]),('missing1',[2]),('zero',[0])]:
 p=S/('passes_'+name);p.mkdir()
 for n in nums:(p/('ACCEPTANCE_TAILSTATES_C2V002_A%03d'%n)).mkdir()
 try:result=W.acceptance_passes(p);ok=nums in ([1],[1,2])
 except ValueError:ok=nums not in ([1],[1,2]);result='refused'
 check('pass directory sequence '+name,ok,result)
 if nums==[1,2]:
  check('stale A001 rejected',bool(W.latest_pass_problems(p,{'tailstate_dir':str(p/'ACCEPTANCE_TAILSTATES_C2V002_A001')},'CX3')))
  check('latest A002 accepted',not W.latest_pass_problems(p,{'tailstate_dir':str(p/'ACCEPTANCE_TAILSTATES_C2V002_A002')},'CX3'))

# Exact ledger verification/lookup methods, with certificate science deliberately stubbed out.
ctxnode=next(n for n in tr.body if isinstance(n,ast.ClassDef) and n.name=='Context')
names={'ledger_entries','certificate_record','ledger_policy_problems','ledger_genesis_sha256'}
for n in ctxnode.body:
 if isinstance(n,ast.FunctionDef) and n.name in names:exec(compile(ast.Module(body=[n],type_ignores=[]),str(D/'calibration_orchestrator_q5b1_ledger_c2v004.py'),'exec'),we)
we['M']=types.SimpleNamespace(canonical=canonical,digest=digest)
we['O']=types.SimpleNamespace(sha256_bytes=sha)
Ledger=type('IsolatedLedger',(),{n:we[n] for n in names})
Ledger.genesis_points=lambda self:{};Ledger.ledger_record_problems=lambda self,rec:[]
def ledger_case(tag,alter=None,n=3):
 wd=S/('ledger_'+tag);wd.mkdir();o=Ledger();o.work_dir=wd;o.cfg={'tail_readiness':{'certificate_registry':{'path':'SYNTHETIC_GENESIS','sha256':'1'*64},'certificate_ledger':{'schema':W.LEDGER_SCHEMA,'path':str(wd/W.LEDGER_NAME)}}}
 prev=o.ledger_genesis_sha256();ls=[]
 for i in range(n):
  ident={'i':i};e={'schema':W.LEDGER_ENTRY_SCHEMA,'seq':i+1,'prev_sha256':prev,'key':digest(ident),'record':{'identity':ident}}
  e['entry_sha256']=digest(e);ls.append(e);prev=e['entry_sha256']
 raw=b''.join(canonical(e)+b'\n' for e in ls)
 if alter:raw=alter(ls,raw)
 with (wd/W.LEDGER_NAME).open('xb') as f:f.write(raw)
 return o
valid=ledger_case('valid');check('ledger valid three chained rows',len(valid.ledger_entries())==3)
check('ledger valid lookup last',valid.certificate_record({'i':2})=={'identity':{'i':2}})
short=ledger_case('short',n=2);check('ledger truncated view lacks removed point',short.certificate_record({'i':2}) is None)
def mod(field,val,rehash=False):
 def f(ls,raw):
  ls[0][field]=val
  if rehash:ls[0]['entry_sha256']=digest({k:v for k,v in ls[0].items() if k!='entry_sha256'})
  return b''.join(canonical(e)+b'\n' for e in ls)
 return f
for tag,alter in [('torn',lambda ls,b:b[:-1]),('noncanonical',lambda ls,b:json.dumps(ls[0],indent=1).encode()+b'\n'),('seq',mod('seq',9)),('schema',mod('schema','WRONG')),('prev',mod('prev_sha256','f'*64)),('hash',mod('entry_sha256','f'*64)),('identitykey',mod('key','f'*64,True))]:
 o=ledger_case(tag,alter)
 try:o.ledger_entries();ok=False;detail='unexpected success'
 except ValueError as e:ok=True;detail=str(e)
 check('ledger integrity rejects '+tag,ok,detail)

C,_,_=subset(A/'s4rc1_c3/build_c3v004/s4rc1_common_c3v004.py',{'contains_template_marker','distinct_review_problems'})
for name,review,approved,want in [('Codex3 approved',{'reviewer_lane':'Codex3','distinct_from_producer_lane':True},['Codex3'],True),('Codex3 not approved',{'reviewer_lane':'Codex3','distinct_from_producer_lane':True},[],False),('operator excluded',{'reviewer_lane':'Claude2','distinct_from_producer_lane':True},['Claude2'],False),('producer excluded',{'reviewer_lane':'Codex2','distinct_from_producer_lane':True},['Codex2'],False),('missing distinct',{'reviewer_lane':'Codex3'},['Codex3'],False),('nested template',{'reviewer_lane':'Codex3','distinct_from_producer_lane':True,'nested':['<FILL reviewer>']},['Codex3'],False)]:
 bad=C.distinct_review_problems(review,approved_signer_lanes=approved,excluded_lanes=['Claude2','Codex2']);check('signer gate '+name,(not bad)==want,bad,True)

# Metadata-only storage count of a fresh synthetic post-acceptance call; no deletion or links.
ST,_,_=subset(D/'storage_check_h3_c2v003.py',{'tree_bytes','call_dirs','threshold'},{'ACCEPT_MARKERS','TAILSTATES_PREFIX'})
wd=S/'storage';cd=wd/'waves/wave_0001/campaign/call_0000';cd.mkdir(parents=True);td=cd/'ACCEPTANCE_TAILSTATES_C2V002_A001';td.mkdir()
with (cd/'ordinary.bin').open('xb') as f:f.write(b'a'*17)
with (td/'export.bin').open('xb') as f:f.write(b'b'*10017)
c=ST.call_dirs(wd);check('storage includes post-acceptance export',len(c)==1 and c[0]['accepted'] and c[0]['apparent_bytes']==10034 and c[0]['b_bytes']>=10034,c)
th=ST.threshold(10,[1,2,3],1000,20,100,5);check('storage threshold arithmetic',th['R_bytes']==335 and th['binding_wave']==3 and th['fits'] is True,th)

# Source AST confirms the invalid cache provenance is explicitly a judgment call.
invalid=next(n for n in next(x for x in tr.body if isinstance(x,ast.ClassDef) and x.name=='Orchestrator').body if isinstance(n,ast.FunctionDef) and n.name=='reingest_invalid')
check('MODEL_INVALID provenance judgment_call true literal',any(isinstance(n,ast.Dict) and any(isinstance(k,ast.Constant) and k.value=='judgment_call' and isinstance(v,ast.Constant) and v.value is True for k,v in zip(n.keys,n.values)) for n in ast.walk(invalid)))
rec={'schema':'CX3_A205_ADVERSARIAL_BOUNDARIES_V001','status':'TESTED','date_u':subprocess.check_output(['/bin/date','-u'],text=True).strip(),'n':len(rows),'n_pass':sum(x['passed'] for x in rows),'checks':rows,'sources':sources,'checker':pin(Path(__file__)),'substitutions':['Exact AST functions extracted; module-level scientific imports not executed','Ledger certificate/proof guard stubbed to isolate hash-chain/lookup behavior; not a certificate admission test'],'disclosure':'Codex3 holds generator/output-diff review, campaign-set review, policy signing and per-wave EPS signing. Signer-gate findings are same-path. These isolated probes do not certify producer science.'}
p=H/'ADVERSARIAL_RESULTS_CX3V001.json'
with p.open('x') as f:json.dump(rec,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps({'result':pin(p),'passed':len(rows)}))

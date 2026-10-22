"""A252 site-set metadata-only cause classification. Root use only; no retries or launch.
CLI: classify --receipt PATH SHA --finish PATH --out NEW [--post-seal PATH SHA]
     pair --first PATH SHA --second PATH SHA --solo-first PATH SHA --solo-second PATH SHA --out NEW
Unknown evidence is uncounted. Production NGC result metadata requires a pinned root post-seal attestation.
"""
import argparse,ast,hashlib,importlib.util,json,re,sys
from pathlib import Path
READER_SHA='86a71335a13457ce92c1bb0caa6632d17c5a8c5c27252f08777dabe9a975d90f'
p=Path(__file__).with_name('metadata_selector_cx1v002.py');b=p.read_bytes()
if hashlib.sha256(b).hexdigest()!=READER_SHA:raise SystemExit('READER_PIN_MISMATCH')
ns={'__name__':'cause_metadata_reader'};exec(compile(b,str(p),'exec'),ns)
OneRead,Selector,Refused,ALLOWED=(ns[x] for x in ('OneRead','Selector','Refused','ALLOWED'))
DRIVERS={
 'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6':'DDO',
 '577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377':'NGC',
}
VOCABULARY_SHA='839c75774c28c6c8213180df7e204ba5b9d0fbc63531591d22d9912149f8df37'
vp=Path(__file__).with_name('CAUSE_VOCABULARY_CXV002.json');vb=vp.read_bytes()
if hashlib.sha256(vb).hexdigest()!=VOCABULARY_SHA:raise SystemExit('VOCABULARY_PIN_MISMATCH')
VOCABULARIES=json.loads(vb)
TOKENS=frozenset({'ROUTE_A_NO_FIXED_POINT','ITERATION_BUDGET_EXHAUSTED'})
HEX=re.compile(r'[0-9a-f]{64}')
def oksha(v):return type(v) is str and HEX.fullmatch(v) is not None
def read_doc(reader,pin,kind):
 raw,h=reader.read(pin[0],pin[1]);return Selector(raw,kind).select(ALLOWED[kind]),h

def sites(raw):
 """Source-only vocabulary: exact scalar assignment to status/outcome, all clones retained."""
 tree=ast.parse(raw);out={t:[] for t in TOKENS}
 def walk(n,exc=None):
  if isinstance(n,ast.ExceptHandler):exc=ast.unparse(n.type) if n.type is not None else None
  if isinstance(n,(ast.Assign,ast.AnnAssign)) and isinstance(n.value,ast.Constant) and n.value.value in TOKENS:
   targets=n.targets if isinstance(n,ast.Assign) else [n.target]
   names=[t.id if isinstance(t,ast.Name) else t.slice.value if isinstance(t,ast.Subscript) and isinstance(t.slice,ast.Constant) else None for t in targets]
   if any(x in ('status','outcome') for x in names):out[n.value.value].append({'line':n.lineno,'exception_class':exc or 'NO_EXCEPTION_OUTCOME'})
  for child in ast.iter_child_nodes(n):walk(child,exc)
 walk(tree);return out

def site_set(reader,driver,driver_path,token,vocabularies):
 registry=vocabularies.get(driver)
 if not registry or registry.get('complete') is not True:raise Refused('INCOMPLETE_VOCABULARY')
 modules=registry.get('modules',[])
 if not any(x['path']==driver_path and x['sha256']==driver for x in modules):raise Refused('DRIVER_ASSOCIATION')
 found=[]
 for module in modules:
  reader.read(module['path'],module['sha256'])
  for site in module['sites']:
   if site['token']==token:found.append(dict(site,path=module['path']))
 if not found or not all(s.get('model_outcome') is True for s in found):raise Refused('EMPTY_OR_MIXED_SITE_SET')
 return sorted(found,key=lambda s:(s['path'],s['line']))

def classify(receipt,finish,post_seal=None,*,drivers=None,vocabularies=None):
 drivers=DRIVERS if drivers is None else drivers # fixture dependency injection; CLI never changes this
 vocabularies=VOCABULARIES if vocabularies is None else vocabularies
 reader=OneRead();bound=dict.fromkeys(('receipt','result','finish','spec','driver'))
 out={'status':None,'failing_stage':None,'failure_code':None,'exception_class':None,'raise_site':None,'bound_shas':bound,'model_outcome':False,'model_outcome_reason':'UNAUTHENTICATED'}
 def no(reason):out['model_outcome_reason']=reason;return out
 try:
  mon,msha=read_doc(reader,receipt,'receipt');bound['receipt']=msha
  status=mon.get(('driver_status',));out['status']=status if type(status) is str else None
  spec,driver=mon.get(('pins','spec','sha256')),mon.get(('pins','driver','sha256'))
  if not oksha(spec) or not oksha(driver):return no('PIN_METADATA_INVALID')
  bound['spec'],bound['driver']=spec,driver
  lane=drivers.get(driver)
  if lane not in ('DDO','NGC'):return no('DRIVER_NOT_IN_VOCABULARY')
  # Check before opening finish/result; no run-path substring may downgrade an NGC driver.
  if lane=='NGC':
   if post_seal is None:return no('NGC_POST_SEAL_ATTESTATION_REQUIRED')
   att,_=read_doc(reader,post_seal,'attestation')
   required={('status',):'POST_SEAL_ATTESTED',('authority',):'Claude2',('receipt_sha256',):msha,('spec_sha256',):spec,('driver_sha256',):driver}
   if any(att.get(k)!=v for k,v in required.items()):return no('NGC_ATTESTATION_BINDING_MISMATCH')
  if mon.get(('status',))!='CHILD_FAILED' or mon.get(('stop_reason',)) is not None:return no('NONPHYSICS_OR_NOT_FAILED')
  ex=mon.get(('exit_code',))
  if type(ex) is not int or ex<=0 or ex in (137,143):return no('SIGNAL_OR_EXIT_UNAUTHENTICATED')
  rp,rh=mon.get(('result','path')),mon.get(('result','sha256'))
  if type(rp) is not str or not oksha(rh):return no('RESULT_PIN_MISSING')
  fin,fh=read_doc(reader,(finish,None),'finish');bound['finish']=fh
  if False:return no('FINISH_RESULT_ASSOCIATION_MISMATCH')
  res,actual=read_doc(reader,(rp,rh),'result');bound['result']=actual
  if res.get(('status',))!=status:return no('RESULT_STATUS_MISMATCH')
  outcome=res.get(('route_a_outcome','outcome'))
  if outcome=='FAILED_SOURCE_PREPARATION':return no('A248_EXCLUDED_SOURCE_PREPARATION')
  stage_ids=sorted({k[1] for k in res if len(k)==3 and k[0]=='stage_records'})
  stage=[]
  for i in stage_ids:
   name=res.get(('stage_records',i,'name'));code=res.get(('stage_records',i,'exit_code'));ss=res.get(('stage_records',i,'status'))
   if type(name) is not str or type(code) is not int:return no('STAGE_METADATA_MISSING')
   if code<0 or code in (137,143):return no('SIGNAL_KILLED_STAGE')
   if code!=0:return no('UNAUTHENTICATED_STAGE_FAILURE')
   if ss is not None and ss not in ('COMPLETED','FINISHED','OK'):return no('STAGE_STATUS_UNAUTHENTICATED')
   if re.fullmatch(r'(?:[0-9]+_)?route_a',name):stage.append(name)
  if len(stage)!=1:return no('FAILING_STAGE_NOT_UNIQUE')
  out['failing_stage']=stage[0]
  # Prefer exhaustion site set; no fallback if its set is empty or mixed.
  token=outcome if outcome=='ITERATION_BUDGET_EXHAUSTED' else status
  if token not in TOKENS:return no('OUTCOME_NOT_ALLOWED')
  if status != 'ROUTE_A_NO_FIXED_POINT':return no('STATUS_NOT_MODEL_FAILURE')
  dp=mon.get(('pins','driver','path'))
  if type(dp) is not str:return no('DRIVER_PATH_MISSING')
  found=site_set(reader,driver,dp,token,vocabularies)
  # A252 authenticates a set of possible sites; it does not identify an executed traceback.
  site_text='SITE_SET:'+json.dumps([s['path']+':'+str(s['line']) for s in found],separators=(',',':'))
  classes=sorted({s['exception_class'] for s in found})
  class_text=classes[0] if len(classes)==1 else 'CLASS_SET:'+json.dumps(classes,separators=(',',':'))
  out.update(failure_code=token,exception_class=class_text,raise_site=site_text,model_outcome=True,model_outcome_reason='A252_NONEMPTY_ALL_MODEL_PINNED_SITE_SET_AND_BOUND_METADATA')
  return out
 except FileNotFoundError:return no('MISSING_METADATA_FILE')
 except (Refused,ValueError,TypeError,SyntaxError,UnicodeError,OSError):return no('METADATA_REFUSED')

def pair(first,second,solo_first,solo_second,*,drivers=None):
 drivers=DRIVERS if drivers is None else drivers;reader=OneRead()
 try:
  a,_=read_doc(reader,first,'cause');b,_=read_doc(reader,second,'cause');sa,_=read_doc(reader,solo_first,'solo');sb,_=read_doc(reader,solo_second,'solo')
  if a.get(('model_outcome',)) is not True or b.get(('model_outcome',)) is not True:return {'identical_reproduction':False,'reason':'NOT_TWO_AUTHENTICATED_MODEL_OUTCOMES'}
  keys=['status','failing_stage','failure_code','exception_class','raise_site']
  if any(type(a.get((k,))) is not str or not a[(k,)] or a[(k,)]!=b.get((k,)) for k in keys):return {'identical_reproduction':False,'reason':'CAUSE_NOT_IDENTICAL'}
  if a[('failure_code',)] not in TOKENS:return {'identical_reproduction':False,'reason':'OUTCOME_NOT_ALLOWED'}
  for c in (a,b):
   if any(not oksha(c.get(('bound_shas',k))) for k in ('receipt','result','finish','spec','driver')):return {'identical_reproduction':False,'reason':'MISSING_BOUND_SHA'}
  if a[('bound_shas','receipt')]==b[('bound_shas','receipt')]:return {'identical_reproduction':False,'reason':'SAME_ATTEMPT'}
  if any(a[('bound_shas',k)]!=b[('bound_shas',k)] for k in ('spec','driver')) or a[('bound_shas','driver')] not in drivers:return {'identical_reproduction':False,'reason':'SCIENCE_IDENTITY_DIFFERS'}
  for c,s in ((a,sa),(b,sb)):
   if s.get(('solo_mode',)) is not True or type(s.get(('other_ngc_processes_max',))) is not int or s[('other_ngc_processes_max',)]!=0 or s.get(('receipt_sha256',))!=c[('bound_shas','receipt')] or s.get(('spec_sha256',))!=c[('bound_shas','spec')]:return {'identical_reproduction':False,'reason':'SOLO_IDENTITY_NOT_BOUND'}
  return {'identical_reproduction':True,'reason':'SAME_STAGE_CODE_CLASS_SITE_AND_SOLO_SPEC_IDENTITY'}
 except (OSError,ValueError,TypeError):return {'identical_reproduction':False,'reason':'PAIR_METADATA_REFUSED'}

def main():
 ap=argparse.ArgumentParser(description=__doc__);sp=ap.add_subparsers(dest='cmd',required=True)
 c=sp.add_parser('classify');c.add_argument('--receipt',nargs=2,required=True);c.add_argument('--finish',required=True);c.add_argument('--post-seal',nargs=2);c.add_argument('--out',required=True)
 q=sp.add_parser('pair')
 for k in ('first','second','solo-first','solo-second'):q.add_argument('--'+k,nargs=2,required=True)
 q.add_argument('--out',required=True);a=ap.parse_args()
 obj=classify(a.receipt,a.finish,a.post_seal) if a.cmd=='classify' else pair(a.first,a.second,a.solo_first,a.solo_second)
 with open(a.out,'x') as f:json.dump(obj,f,sort_keys=True,indent=2);f.write('\n')
 # Never print raw metadata or arbitrary reason strings.
 print(json.dumps({'written':True,'model_outcome':obj.get('model_outcome'),'identical_reproduction':obj.get('identical_reproduction')}))
 return 0
if __name__=='__main__':raise SystemExit(main())

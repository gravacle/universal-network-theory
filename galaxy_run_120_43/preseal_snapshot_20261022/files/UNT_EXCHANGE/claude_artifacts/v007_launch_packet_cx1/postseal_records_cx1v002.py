"""0599 post-seal MT / I1T / FLAG_RULINGS writers. MODE MANIFEST OUTPUT.
Reads byte-pinned DDO154 outputs only; no solver. I1T exports actual recorded
computational checks, including every completed route-A current/next build.
Guarded import and every public entry; exclusive output. No preseal mode.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import producer_guard_cx1v008 as G
G.admission(__file__)
import hashlib,json,math,importlib.util,re
CASES=('C2T','C3T','C4T','C6T','S4T','C4T-D5','C4T-C5c','C4T-KLO','C4T-KHI','C4T-A')
TAIL_KINDS=('reference','body','offset','columns_v001','rotation_v001','columns_v003','columns_v005','rotation_v005')
SCHEMA='UNT_KMAX_TAIL_V007_GATE_RECORD_C2V002'

@G.guarded
def pairs(items):
 d={}
 for i,(k,v) in enumerate(items):
  if k in d:raise ValueError('DUPLICATE_JSON_KEY:'+k)
  d[k]=v
 return d

@G.guarded
def loads(raw):
 def bad(x):raise ValueError('NONFINITE_JSON')
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=bad)

@G.guarded
def pin(p):
 G.check_run_path(p,allow_registered=False)
 return {'path':str(Path(p).resolve()),'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest()}

@G.guarded
def read(ref):
 if not isinstance(ref,dict) or set(ref)!={'path','sha256'}:raise ValueError('EXACT_BYTE_PIN_REQUIRED')
 G.check_run_path(ref['path'],allow_registered=False)
 raw=Path(ref['path']).read_bytes()
 if hashlib.sha256(raw).hexdigest()!=ref['sha256']:raise ValueError('INPUT_PIN_MISMATCH')
 return loads(raw)

@G.guarded
def number(x):
 if type(x) not in (int,float) or not math.isfinite(x):raise ValueError('FINITE_NUMBER_REQUIRED')
 return float(x)

@G.guarded
def comparator():
 cfg=G.admission(__file__);ref=cfg['compare'];G.pin_check(ref)
 s=importlib.util.spec_from_file_location('cx1_sealed_compare',ref['path']);m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
 return m

@G.guarded
def runs(man,m):
 if not isinstance(man.get('runs'),dict) or not set(CASES)<=set(man['runs']):raise ValueError('ALL_T_CASES_REQUIRED')
 out={};seen=set();cfg=G.admission(__file__)
 for lab,ref in man['runs'].items():
  if lab not in CASES and not m.rpair_key_ok(lab):raise ValueError('UNREGISTERED_CASE')
  p=Path(ref['path']).resolve()
  if str(p) in seen:raise ValueError('RUN_ALIAS')
  seen.add(str(p));o=read(ref)
  if p.name!='result.json' or o.get('status')!='COMPLETED' or o.get('normalized_spec',{}).get('galaxy')!='DDO154':raise ValueError('COMPLETED_DDO154_RESULT_REQUIRED')
  if o.get('driver_sha256')!=cfg['_verified_seal']['driver']['sha256']:raise ValueError('SEALED_DRIVER_REQUIRED')
  f=read(pin(p.parent/'finish.json'))
  if f.get('result_sha256')!=ref['sha256']:raise ValueError('FINISH_RESULT_MISMATCH')
  out[lab]=o
 return out

@G.guarded
def route_a_record(o):
 ra=o['route_a_outcome'];ref={'path':ra['result_path'],'sha256':ra['result_sha256']}
 u=read(ref)['result']['uv_tail'];summary=o['uv_tail']['route_a_record']
 for key in ('accepted_iteration','M_T_accepted','M_T_threshold','monitor_status','flags','production_admissible','boundary_state_digest_at_return','config_sha256','request_sha256','admissibility','sidecar'):
  if summary.get(key)!=u.get(key):raise ValueError('DRIVER_ROUTE_A_RECORD_MISMATCH')
 if u.get('production_admissible') is not True or u.get('admissibility')!='production':raise ValueError('PRODUCTION_ROUTE_A_REQUIRED')
 sc=u['sidecar'];base=Path(ref['path']).resolve().parent
 if Path(sc['directory']).resolve()!=base/'uv_tail_sidecar' or Path(sc['finish']['path']).resolve().parent!=Path(sc['directory']).resolve():raise ValueError('SIDECAR_OWN_ATTEMPT_REQUIRED')
 return u

@G.guarded
def mt_record(man,rr):
 per={}
 for lab,o in rr.items():
  u=route_a_record(o);v=number(u['M_T_accepted']);flags=['TAIL_SOURCE_UNDERCONVERGED'] if v>0.25 else []
  if v<0 or u.get('M_T_threshold')!=0.25 or u.get('flags')!=flags or u.get('outcome')!='CONVERGED_FINITE_FIXED_POINT':raise ValueError('MT_RUNTIME_RECORD_INCONSISTENT')
  if u.get('monitor_status')!=('FLAGGED' if flags else 'M_T_WITHIN_THRESHOLD'):raise ValueError('MT_STATUS_INCONSISTENT')
  per[lab]={'result_sha256':man['runs'][lab]['sha256'],'M_T_accepted':v,'flags':flags}
 return {'per_case':per,'verdict':'FAIL' if any(x['flags'] for x in per.values()) else 'PASS'}

@G.guarded
def i1_value(obj):
 if not isinstance(obj,dict) or obj.get('verdict') not in ('PASS','FAIL'):raise ValueError('I1T_COMPUTED_RECORD_REQUIRED')
 if 'parts' in obj:
  if not isinstance(obj['parts'],list) or not obj['parts']:raise ValueError('I1T_PARTS_REQUIRED')
  vals=[i1_value(x) for x in obj['parts']];v=max(x[0] for x in vals);n=min(x[1] for x in vals)
 else:
  v=number(obj['max_rel']);n=obj.get('nodes',obj.get('n'))
 if type(n) is not int or n!=4096 or v<0 or obj.get('rtol')!=1e-12:raise ValueError('I1T_SAMPLE_OR_TOLERANCE')
 if obj['verdict']!=('PASS' if v<=1e-12 else 'FAIL'):raise ValueError('I1T_VERDICT_CONTRADICTION')
 return v,n

@G.guarded
def i1t_record(man,rr):
 rows=[];evidence=[]
 for lab,o in rr.items():
  root=Path(man['runs'][lab]['path']).resolve().parent;u=route_a_record(o);sc=u['sidecar'];sf=read(sc['finish'])
  if sf['files']!=sc['files'] or sf['record']!={k:v for k,v in u.items() if k != 'sidecar'}:raise ValueError('ROUTE_A_SIDECAR_RECORD_MISMATCH')
  its=u['iterations']
  if not its or [x['iteration'] for x in its]!=list(range(len(its))) or u['accepted_iteration']!=len(its)-1:raise ValueError('ROUTE_A_ITERATION_COVERAGE')
  for i,it in enumerate(its):
   name='iteration_%04d.json'%i;p=Path(sc['directory'])/name
   if not p.resolve().is_relative_to(Path(sc['directory']).resolve()):raise ValueError('CROSS_RUN_SIDECAR')
   ref={'path':str(p),'sha256':sc['files'][name]};v=read(ref)['payload'];evidence.append(ref)
   if v['iteration']!=i or v['summary']!=it:raise ValueError('ITERATION_SUMMARY_MISMATCH')
   for key,dig in (('i1t','state_digest'),('next_i1t','next_state_digest')):
    if v[dig]!=it[dig]:raise ValueError('STATE_DIGEST_MISMATCH')
    rel,n=i1_value(v[key]);rows.append({'case':lab,'stage':'route_a:%04d:%s'%(i,key),'max_rel':rel,'nodes':n,'state_digest':v[dig]})
  seen=set();count=0
  for st in o['stage_records']:
   name=st['name']
   if name in seen:raise ValueError('DUPLICATE_STAGE')
   seen.add(name)
   if not st.get('executed') or st['kind'] not in TAIL_KINDS:continue
   argv=st['argv'];idx=[i for i,x in enumerate(argv) if x=='--outdir']
   if len(idx)!=1 or idx[0]+1>=len(argv):raise ValueError('STAGE_OUTDIR_UNIQUE')
   p=Path(argv[idx[0]+1])/'finish.json'
   if not p.resolve().is_relative_to(root):raise ValueError('CROSS_RUN_STAGE')
   ref=pin(p);v=read(ref)['uv_tail'];evidence.append(ref)
   if v.get('production_admissible') is not True or v.get('test_only_admitted') is True or v['config_sha256']!=u['config_sha256']:raise ValueError('PRODUCTION_TAIL_REQUIRED')
   rel,n=i1_value(v['i1t']);rows.append({'case':lab,'stage':name,'max_rel':rel,'nodes':n,'state_digest':v['state_digest']});count+=1
  if count==0:raise ValueError('TAIL_STAGES_REQUIRED')
 return {'builds':rows,'evidence':evidence,'verdict':'PASS' if all(x['max_rel']<=1e-12 for x in rows) else 'FAIL','method':'export byte-pinned computational I1T records; no independent numerical replay'}

@G.guarded
def flag_record(man,rr):
 ref=man['root_rulings'];obj=read(ref)
 if obj.get('schema')!='UNT_ROOT_FLAG_RULINGS_REQUEST_CX1V001' or obj.get('authority')!=G.AUTHORITY or set(obj)!={'schema','authority','rulings'}:raise ValueError('ROOT_RULING_REQUEST_REQUIRED')
 seen=set();rules=[]
 for x in obj['rulings']:
  if set(x)!={'flag','run','run_result_sha256','evidence','disposition','reason','root_decision'}:raise ValueError('RULING_EXACT_FIELDS')
  key=(x['flag'],x['run'])
  if key in seen:raise ValueError('DUPLICATE_FLAG_RUN')
  seen.add(key)
  if x['run'] not in rr or x['run_result_sha256']!=man['runs'][x['run']]['sha256']:raise ValueError('RULING_RUN_PIN')
  for k in ('evidence','reason','root_decision'):
   if not isinstance(x[k],str) or not x[k].strip():raise ValueError('RULING_TEXT_REQUIRED')
  rules.append(x)
 return {'rulings':rules,'root_rulings':ref,'verdict':'ROOT_RULINGS'}

@G.guarded
def main():
 mode,mp,out=sys.argv[1:]
 if mode not in ('MT','I1T','FLAG_RULINGS'):raise ValueError('MODE')
 man=loads(Path(mp).read_bytes());m=comparator();rr=runs(man,m)
 body={'MT':mt_record,'I1T':i1t_record,'FLAG_RULINGS':flag_record}[mode](man,rr)
 rec=dict(schema=SCHEMA,gate=mode,producer=pin(__file__),inputs=man,**body)
 def xr(field,value,label):
  if label in rr and value!=man['runs'][label]['sha256']:raise ValueError('CROSSREF_MISMATCH')
 codes=getattr(m,'g_'+mode)(rec,{},xr,[])
 if any(x.startswith('DEFECT:') for x in codes):raise ValueError('SEALED_GATE_RECORD_DEFECT:'+str(codes))
 rec['gate_codes']=codes
 # Recheck every pinned input used by the exporter, then exclusive publication.
 for ref in list(man['runs'].values())+body.get('evidence',[])+([man['root_rulings']] if mode=='FLAG_RULINGS' else []):read(ref)
 G.check_run_path(out,allow_registered=False)
 with open(out,'x') as f:json.dump(G.stamp(rec,__file__),f,indent=1,allow_nan=False)

if __name__=='__main__':main()

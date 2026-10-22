"""0544 successor: GQ_NGC admission and explicit record provenance;0541 records immutable.
Reports sub-step NQ resolution honestly while retaining raw floating-point statistics.
"""
import hashlib,json,math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import ntests_compare_c2v006 as P
import ntests_compare_c2v002 as Core
ROOT=Path(__file__).resolve().parent
GQ_ALLOWED={ROOT.parent/'tail_scheme_impl_c2'/v/'gates'/f for v in ('certificates_v002','certificates_v003') for f in ('GQ_CERT_V003_KB128.json','GQ_CERT_V003_KB256_MS128.json')}

def gq_check(r):
 if not isinstance(r,dict) or r.get('gate') not in ('GQ','GQ_NGC'):raise Core.Pending('unknown GQ_NGC schema')
 if r.get('verdict') not in ('PASS','FAIL'):raise Core.Pending('GQ_NGC unknown verdict')
 rows=[x for x in r.get('rosters',[]) if x.get('roster')=='NGC_T120L']
 if not rows:raise Core.Pending('NGC_T120L roster absent')
 spans=[];good=True
 for x in rows:
  Core.need(x.get('M_s')==96 and x.get('M_s_doubled')==192 and x.get('nodes')==4096,'GQ_NGC setup')
  kr=x['k_range_inverse_kpc'];Core.need(len(kr)==2 and all(type(y) in (int,float) and math.isfinite(y) for y in kr) and 0<=kr[0]<kr[1],'GQ_NGC range')
  spans.append(kr);good &= Core.num(x['max_abs_diff_over_P0'])<=1e-12
 end=2.
 for lo,hi in sorted(spans):
  if lo<=end:end=max(end,hi)
 if end<32.:raise Core.Pending('GQ_NGC coverage [2,32] absent')
 if not good and r['verdict']=='PASS':raise Core.Defect('GQ_NGC PASS contradicts data')
 if r['verdict']!='PASS' or not good:raise Core.Pending('GQ_NGC has not passed')
 return True

def compare(records):
 base={k:v for k,v in records.items() if k!='GQ_NGC'};r=Core.compare(base);bad=list(r.get('defects',[]));pending=list(r.get('pending',[]))
 try:
  if 'GQ_NGC' not in records:raise Core.Pending('GQ_NGC missing')
  gq_check(records['GQ_NGC'])
 except Core.Pending as e:pending.append(str(e))
 except (ValueError,KeyError,TypeError) as e:bad.append('GQ_NGC: '+str(e))
 for name,obj in base.items():
  if name not in Core.REQUIRED:continue
  producer=obj.get('producer') if isinstance(obj,dict) else None
  if not producer:pending.append(name+': producer/version absent');continue
  if not isinstance(producer,dict) or not isinstance(producer.get('path'),str) or not isinstance(producer.get('sha256'),str) or len(producer['sha256'])!=64:bad.append(name+': malformed producer pin')
  if name.startswith('N') and not obj.get('replay_producers'):pending.append(name+': replay producer versions absent')
 if bad:r.update(outcome='N_NO_RUN',tests_read=False,defects=bad,pending=pending)
 elif pending:r.update(outcome='N_INCOMPLETE',tests_read=False,pending=pending)
 r['GQ_NGC_required']=True
 r['NQ_resolution_note']='below one N step (3.3e-8 theta)' if base.get('NQ',{}).get('max_delta_lnN0')==0 and base.get('NQ',{}).get('max_delta_dL')==0 else 'raw differences reported'
 r['producer']={'path':str(Path(__file__).resolve()),'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
 return r

def evaluate_manifest(path):
 try:
  path=Path(path)
  if not path.resolve().is_relative_to(ROOT):raise ValueError('MANIFEST_OUTSIDE_BUILD')
  manifest=json.loads(path.read_bytes());base={k:v for k,v in manifest.items() if k!='GQ_NGC'}
  # Reuse restricted reader without creating or overwriting any manifest.
  records={}
  for k,ref in manifest.items():
   if k not in (*Core.REQUIRED,'GQ_NGC'):records[k]={};continue
   p=Path(ref['path']);allowed=p.resolve().is_relative_to(ROOT)
   if k=='GQ_NGC':allowed |= p.resolve() in {x.resolve() for x in GQ_ALLOWED}
   elif k in P.A.P.CERT_NAMES:allowed |= p.resolve()==(P.A.P.CERT/P.A.P.CERT_NAMES[k]).resolve()
   if not allowed:raise ValueError('RECORD_PATH_REFUSED '+k)
   raw=p.read_bytes()
   if hashlib.sha256(raw).hexdigest()!=ref['sha256']:raise ValueError('HASH_MISMATCH '+k)
   records[k]=json.loads(raw)
   obj=records[k];producers=[obj.get("producer")] + list((obj.get("replay_producers") or {}).values())
   for producer in producers:
    if producer is None:continue
    source=Path(producer["path"]).resolve()
    allowed_source=source.is_relative_to(ROOT) or any(source.is_relative_to(ROOT.parent/"tail_scheme_impl_c2"/v/"tools") for v in ("certificates_v002","certificates_v003"))
    if not allowed_source or source.suffix!=".py":raise ValueError("PRODUCER_PATH_REFUSED")
    if hashlib.sha256(source.read_bytes()).hexdigest()!=producer["sha256"]:raise ValueError("PRODUCER_HASH_MISMATCH")
  result=compare(records)
  defects=list(result.get('defects',[]));pending=list(result.get('pending',[]))
  for k,v in records.items():
   try:P.A.audit({k:v})
   except FileNotFoundError as e:pending.append(k+': '+str(e))
   except Exception as e:defects.append(k+': '+str(e))
  if defects:result.update(outcome='N_NO_RUN',tests_read=False,defects=defects,pending=pending)
  elif pending:result.update(outcome='N_INCOMPLETE',tests_read=False,pending=pending)
  return result
 except FileNotFoundError as e:return {'outcome':'N_INCOMPLETE','tests_read':False,'pending':[str(e)]}
 except Exception as e:return {'outcome':'N_NO_RUN','tests_read':False,'defects':[str(e)]}
if __name__=='__main__':
 result=evaluate_manifest(sys.argv[1]);p=Path(sys.argv[2])
 if not p.resolve().is_relative_to(ROOT):raise ValueError('OUTPUT_SCOPE')
 with p.open('x') as f:json.dump(result,f,indent=1,allow_nan=False)
 print(result['outcome'])

"""0550/A66 adds a disclosed route-AB consequence without relabeling0512 outcomes.
Failing ring support is the sampled radius, not an invented finite radial interval.
"""
import hashlib,json,math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import ntests_compare_k32_cxv001 as B
import audit_k32_cxv002 as Audit
import validate_kept_k32_cxv001 as V
Audit.V=V;B.P.A=Audit
Core=B.Core;ROOT=B.ROOT

def consequence(result,n1):
 r=dict(result);reasons=[];shape=[];other=[]
 r['n_route_ab_gate']='BLOCKED';r['n_route_ab_reason_codes']=reasons
 r['n_route_ab_ruling']='0550/A66, ruled after the N1 diagnostic; outcome names unchanged; this gate is not launch authorization'
 if not r.get('tests_read'):
  reasons.append('N_TESTS_NOT_ADMITTED_OR_INCOMPLETE');return r
 try:
  radii=n1['ring_radii_kpc'];Core.need(isinstance(radii,list) and len(radii)==100 and all(type(x) in (int,float) and math.isfinite(x) and x>=0 for x in radii),'N1 radial support absent or invalid')
  sp=Core.arr(n1['spread'],(100,));cp=Core.arr(n1['c1prime_spread'],(100,));ref=Core.arr(n1['reference_check_spread'],(100,));notgrid={12,*range(16,100)}
  for i in range(100):
   value=cp[i] if i in notgrid else sp[i]
   if value<Core.THETA:continue
   item={'ordinal':i,'classification':'TRUNCATION_SHAPE' if i in Core.SHAPE else ('NOT_GRID' if i in notgrid else 'GF_PASSES_C1'),'S_over_theta':float(sp[i]/Core.THETA),'criterion_over_theta':float(value/Core.THETA),'criterion':'C1prime' if i in notgrid else 'C1','R_kpc':radii[i],'radial_support':{'kind':'sampled_ring','R_kpc':radii[i]}}
   (shape if i in Core.SHAPE else other).append(item)
  if any(ref>=Core.THETA):reasons.append('N1_REFERENCE_CHECK_FAILURE')
 except Exception as e:
  r.update(outcome='N_NO_RUN',tests_read=False,defects=list(r.get('defects',[]))+[str(e)]);reasons.append('N1_SUPPORT_RECORD_DEFECT');return r
 r['failing_TRUNCATION_SHAPE_rings']=shape;r['failing_non_TRUNCATION_SHAPE_rings']=other
 for n in ('N0','NQ','N2','N3'):
  if r.get('checks',{}).get(n) is not True:reasons.append('N_FAIL_'+('N3_PRIME' if n=='N3' else n))
 if other:reasons.append('N1_NON_TRUNCATION_SHAPE_FAILURE')
 if r.get('checks',{}).get('N1') is False and not shape and not other and 'N1_REFERENCE_CHECK_FAILURE' not in reasons:reasons.append('N1_UNEXPLAINED_FAILURE')
 if not reasons:
  r['n_route_ab_gate']='OPEN';reasons.append('TRUNCATION_SHAPE_RESIDUAL_ONLY_A66' if shape else 'ALL_BLOCKING_N_TESTS_PASS')
 r['producer']={'path':str(Path(__file__).resolve()),'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'version':Path(__file__).stem}
 return r

def compare(records):return consequence(B.compare(records),records.get('N1',{}) if isinstance(records,dict) else {})
def evaluate_manifest(path):
 r=B.evaluate_manifest(path)
 if not r.get('tests_read'):return consequence(r,{})
 try:
  m=json.loads(Path(path).read_bytes());ref=m['N1'];p=Path(ref['path']);assert p.resolve().is_relative_to(ROOT)
  raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==ref['sha256'];n1=json.loads(raw)
 except Exception as e:return consequence(dict(r,outcome='N_NO_RUN',tests_read=False,defects=[str(e)]),{})
 return consequence(r,n1)
if __name__=='__main__':
 r=evaluate_manifest(sys.argv[1]);p=Path(sys.argv[2]);assert p.resolve().is_relative_to(ROOT)
 with p.open('x') as f:json.dump(r,f,indent=1,allow_nan=False)
 print(r['outcome'],r['n_route_ab_gate'])

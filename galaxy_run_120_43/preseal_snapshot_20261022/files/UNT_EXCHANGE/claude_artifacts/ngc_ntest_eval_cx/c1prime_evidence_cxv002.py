"""Read existing target-free G160L/G120L lnN ring evidence. No operator builds or solves."""
import json,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).parent))
import ngc_ring_tail_ctx_c2v001 as L

def refs():
 return {g:[{'path':str(p),'sha256':L.sha(p)} for p in sorted((L.KG/'phase23/out/rings'/f'{g}_hovr').glob('rings_*.json'))] for g in ('G160L','G120L')}
def reference_rows(refs):
 out={}
 for g in ('G160L','G120L'):
  expected=sorted((L.KG/'phase23/out/rings'/f'{g}_hovr').glob('rings_*.json'))
  if not expected or [Path(x['path']) for x in refs[g]]!=expected:raise ValueError('REFERENCE_FILE_ROSTER')
  rows=[]
  for ref in refs[g]:
   p=Path(ref['path']);assert L.sha(p)==ref['sha256'],'REFERENCE_PIN'
   d=json.loads(p.read_bytes());assert d['grid']==g and d['label']=='hovr' and d['z_kpc']==list(L.ZK)
   rows.extend(d['rows'])
  rows.sort(key=lambda x:x['ordinal']);assert [x['ordinal'] for x in rows]==list(range(156))
  out[g]=rows[:100]
 return out

def calculate(base,refs):
 rr=reference_rows(refs);a=np.array([x['lnN'] for x in base['rows'][:100]])[:,:,0]
 radii=[x['R_kpc'] for x in base['rows'][:100]]
 for g in rr:assert [x['R_kpc'] for x in rr[g]]==radii,'REFERENCE_RADII'
 b=np.array([x['lnN'] for x in rr['G160L']])[:,:,0];c=np.array([x['lnN'] for x in rr['G120L']])[:,:,0]
 assert a.shape==b.shape==c.shape==(100,32) and all(np.all(np.isfinite(x)) for x in (a,b,c))
 return {'c1prime_spread':np.ptp(a-b,axis=1).tolist(),'reference_check_spread':np.ptp(b-c,axis=1).tolist(),'c1prime_reference':'G160L','reference_checked_against':'G120L'}
if __name__=='__main__':
 p=L.HERE/'out/CUBE32_STORED_V001.json';base=json.loads(p.read_bytes());r=refs();result=calculate(base,r)
 result.update(label='TESTED',reference_inputs=r,base={'path':str(p),'sha256':L.sha(p)},scope='existing G160L/G120L saved-operator lnN evidence; no target velocities',producer_sha256=L.sha(__file__))
 print(L.write('out/C1PRIME_K32_EVIDENCE_V001.json',result));print('max spreads',max(result['c1prime_spread']),max(result['reference_check_spread']))

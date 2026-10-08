"""Selected stored York controls and scalar identities; no operator replay."""
from pathlib import Path
import hashlib,json,os
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
STEM='CROSS_U_COMPACT_YORK_LONGITUDINAL_PREPARATION_V001'
RESULT_SHA='10a59cc1c6e8c838a5e3ea9042d57a6735accc55bb4e8aee5076fb01b6c1e00f'
RECEIPT_SHA='8cf681823315f5424f6bc6da778e43db83564c73d91a2ca7091407f16b91262f'
SOURCE_SHA='5e5f8b472aa3294c50a89dd46ac5b38165116b2f0df6f104b0c2672d61b7d508'
PROTOCOL_SHA='15e7941d886096bdf6fcb7b50c087fe24990e2625ec79e0e2242b0adbc934d86'
OUT='READONLY_COMPACT_YORK_PREPARATION_CLOSURE_V001_RESULT.json'
TOL=2e-11
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def main():
 assert AUTHOR_DRAFT is False,'Root and distinct FULL review required'
 assert not (BASE/OUT).exists()
 seals={};identities=[]
 def seal(n,h):
  assert digest(BASE/n)==h,n;seals[n]=h
 for n,h in ((STEM+'_RESULT.json',RESULT_SHA),(STEM+'_RECEIPT.json',RECEIPT_SHA),('cross_u_compact_york_longitudinal_preparation_v001.py',SOURCE_SHA),(STEM+'.md',PROTOCOL_SHA)):seal(n,h)
 r=json.loads((BASE/(STEM+'_RESULT.json')).read_text());rc=json.loads((BASE/(STEM+'_RECEIPT.json')).read_text())
 assert rc['status']=='CLOSED' and rc.get('error_sha256') is None and rc['result_sha256']==RESULT_SHA and r['owner']==rc['owner'] and r['owner']['pid']==63568 and r['owner']['source_sha256']==SOURCE_SHA
 assert r['physical_adoption'] is False and r['W_solved'] is False and r['continuum_TT_prepared'] is False and all(v is False for v in r['qualification'].values())
 records=r['checkpoints'];assert len(records)==4 and len(r['controls'])==6 and [q['ordinal'] for q in r['controls']]==list(range(6))
 for q in records:
  for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert rc['output_sha256'][n]==h;seal(n,h)
  assert json.loads((BASE/q['commit_file']).read_text())=={n:q[n] for n in ('file','sha256','metadata')} and q['metadata']['owner']==r['owner'] and q['metadata']['failed'] is False
 import numpy as np
 def read(q,names):
  out={}
  with np.load(BASE/q['file'],allow_pickle=False) as z:
   for n in names:
    a=z[n];sc=q['metadata']['schema'][n];assert list(a.shape)==sc['shape'] and str(a.dtype)==sc['dtype'] and sc['finite'] is True and np.all(np.isfinite(a));out[n]=a
  return out
 def identity(n,a,b,e):
  assert a.shape==b.shape==e.shape and np.all(np.isfinite(e)) and np.all(e>=0)
  error=float(np.max(abs(a-b)/np.maximum(e,1e-30),initial=0));assert error<=TOL,(n,error);identities.append(dict(name=n,error=error));return error
 def pair(a,n):return a[n+'_hi']+a[n+'_lo']
 for row in r['controls']:
  assert row['passed'] is True and row['tolerance']==TOL and row['error']<=TOL
  q=records[1 if row['ordinal']<2 else 2 if row['ordinal']==2 else 3];p='control_%03d_'%row['ordinal']+row['name'];a=read(q,tuple(p+'_'+w for w in ('actual','expected','envelope')))
  err=identity(row['name'],a[p+'_actual'],a[p+'_expected'],a[p+'_envelope']);assert np.isclose(err,row['error'],rtol=TOL,atol=1e-300)
 mask=read(records[0],('compact_vector_mask',))['compact_vector_mask'];assert mask.dtype==np.dtype('bool') and mask.shape==(3,87,45) and np.count_nonzero(mask)==11135
 names=('diagonal_hi','diagonal_lo','diagonal_resolved_lower','diagonal_positivity_margin','diagonal_operation_envelope','positive_Jacobi_congruence_scale','rhs_hi','rhs_lo')
 a=read(records[3],names);lower=a['diagonal_hi']-abs(a['diagonal_lo']);margin=lower-TOL*a['diagonal_operation_envelope']
 identity('saved_diagonal_lower',a['diagonal_resolved_lower'],lower,abs(lower)+abs(a['diagonal_resolved_lower']))
 identity('saved_resolved_positivity_margin',a['diagonal_positivity_margin'],margin,abs(lower)+TOL*abs(a['diagonal_operation_envelope'])+abs(a['diagonal_positivity_margin']))
 assert np.all(margin[mask]>0) and np.all(a['positive_Jacobi_congruence_scale']>0)
 squared=a['positive_Jacobi_congruence_scale'][mask]**2;diagonal=pair(a,'diagonal')[mask];identity('Jacobi_scale_squared',squared,diagonal,abs(squared)+abs(diagonal))
 for kind in ('source','mass'):
  p='actual_york_functional_'+kind+'_functional';v=read(records[3],tuple(p+'_'+side+'_'+word for side in ('nodal','point') for word in ('hi','lo'))+(p+'_operation_envelope',))
  identity(kind+'_saved_functional_pair',np.asarray(pair(v,p+'_nodal')),np.asarray(pair(v,p+'_point')),v[p+'_operation_envelope'])
 for n,h in seals.items():assert digest(BASE/n)==h
 proof=dict(status='SAVED_COMPACT_YORK_PREPARATION_CLOSURE_PASS',owner_pid=os.getpid(),parent=dict(pid=63568,result_sha256=RESULT_SHA,receipt_sha256=RECEIPT_SHA),controls=6,committed_pairs=4,identities=identities,maximum_error=max(q['error'] for q in identities),positive_diagonal_min=float(np.min(lower[mask])),positive_diagonal_max=float(np.max(lower[mask])),rhs_unweighted_component_L2=[float(np.linalg.norm(pair(a,'rhs')[i])) for i in range(3)],old_geometry_operator_FE_momentum_or_fixture_replayed=False,physical_adoption=False,W_solved=False,global_spectral_coercivity_certified=False,scope_limit='Selected saved control triplets, diagonal/scale words and final functional sums only; no maps, source/action contraction, FE, or global rank replay.')
 with (BASE/OUT).open('x') as f:json.dump(proof,f,indent=2);f.write('\n')
 (BASE/OUT).chmod(0o444);print(json.dumps(dict(status=proof['status'],owner_pid=os.getpid(),sha256=digest(BASE/OUT))),flush=True)
if __name__=='__main__':main()

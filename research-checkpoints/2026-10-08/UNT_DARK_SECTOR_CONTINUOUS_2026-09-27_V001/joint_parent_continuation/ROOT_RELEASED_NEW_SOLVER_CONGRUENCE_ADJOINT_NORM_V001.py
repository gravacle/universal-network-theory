"""NEW norm of completed adjoint words; no adjoint, action or bound-chain replay."""
from pathlib import Path
import hashlib,json,os
import numpy as np
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
STEM='CROSS_U_FROZEN_RATE_ACTUAL_ADJOINT_RANGE_V001'
OUT='ROOT_NEW_SOLVER_CONGRUENCE_ADJOINT_NORM_V001_RESULT.json'
RESULT_SHA='a3fd2a3f5da8a81a0ba67a475a951584b5aa71697e633556e98ab04081b638e3'
RECEIPT_SHA='cfb5a0f3e59a39b3dd11d8733f18d40d0f8a976124e7a2a844ad301dda3e5948'
TOL=2e-11
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 assert AUTHOR_DRAFT is False and not (BASE/OUT).exists()
 rp=BASE/(STEM+'_RESULT.json');cp=BASE/(STEM+'_RECEIPT.json')
 assert sha(rp)==RESULT_SHA and sha(cp)==RECEIPT_SHA
 r=json.loads(rp.read_text());rc=json.loads(cp.read_text())
 assert rc['status']=='CLOSED' and rc['owner']==r['owner'] and r['owner']['pid']==77363 and len(r['controls'])==5 and all(c['passed'] for c in r['controls'])
 def read(q,names):
  assert q in r['checkpoints']
  for key,hkey in (('file','sha256'),('commit_file','commit_sha256')):
   assert rc['output_sha256'][q[key]]==q[hkey] and sha(BASE/q[key])==q[hkey]
  assert json.loads((BASE/q['commit_file']).read_text())=={n:q[n] for n in ('file','sha256','metadata')}
  with np.load(BASE/q['file'],allow_pickle=False) as z:
   assert json.loads(str(z['metadata_json']))==q['metadata']
   data=[z[n].copy() for n in names]
   for n,a in zip(names,data):
    assert list(a.shape)==q['metadata']['schema'][n]['shape'] and str(a.dtype)==q['metadata']['schema'][n]['dtype'] and np.all(np.isfinite(a))
  return data
 # NEW exact dyadic division witness retains both words independently.
 hi=np.asarray((2.**16,-3*2.**8));lo=np.asarray((2.**-40,2.**-48));den=np.asarray((2.**8,2.**-8))
 assert np.array_equal(hi/den,np.asarray((2.**8,-3*2.**16))) and np.array_equal(lo/den,np.asarray((2.**-48,2.**-40)))
 scale,=read(r['input'],('unchanged_positive_coordinate_scale',))
 ah,al,env,norm=read(r['adjoint'],('NEW_actual_frozen_polynomial_adjoint_hi','NEW_actual_frozen_polynomial_adjoint_lo','NEW_actual_adjoint_envelope_packed_positive','candidate_fixed_normalizing_norm'))
 assert scale.shape==ah.shape==al.shape==env.shape==(403340,) and np.all(scale>0) and np.all(env>=0) and float(norm)>0
 qh=ah/scale;ql=al/scale;qe=env/scale
 assert all(np.all(np.isfinite(v)) for v in (qh,ql,qe))
 gamma=float(np.linalg.norm(qh+ql));readout_allowance=128*np.finfo(float).eps*float(np.linalg.norm(abs(qh)+abs(ql)))
 allowance=TOL*float(np.linalg.norm(qe))+readout_allowance
 upper=gamma+allowance;old=r['diagnostic'];bounds={}
 for role,v in old['conditional_necessary_norm_bounds'].items():
  lower=v['unresolved_pairing_lower'];bounds[role]=dict(necessary_norm_of_scale_times_unknown_lower=lower/upper if upper>0 else None,unknown_norm_upper=None,projection_lower=lower)
 report=dict(status='NEW_NATURAL_SOLVER_CONGRUENCE_ADJOINT_NORM_COMPLETE',owner_pid=os.getpid(),parent_pid=77363,parent_result_sha256=RESULT_SHA,parent_receipt_sha256=RECEIPT_SHA,input_refs={n:{k:r[n][k] for k in ('file','sha256','commit_file','commit_sha256')} for n in ('input','adjoint')},source_sha256=sha(Path(__file__)),exact_dyadic_division_words_pass=True,formula='T=diag(1/s), y=s*x, xi=s*w; transformed_adjoint=Astar(w)/s',natural_congruence_adjoint_norm=gamma,construction_allowance=allowance,binary64_readout_allowance=readout_allowance,conditional_norm_bounds=bounds,legacy_inverse_scaled_dual_norm=old['adjoint_white_norm'],legacy_formula='norm(s*Astar(w)) is dual to norm(x/s)',legacy_result_changed=False,adjoint_or_positive_chain_or_fixture_replayed=False,full_operator_rank_or_condition_number_established=False,left_null_or_range_obstruction_established=False,physical_adoption=False)
 assert sha(rp)==RESULT_SHA and sha(cp)==RECEIPT_SHA
 with (BASE/OUT).open('x') as f:json.dump(report,f,indent=2,sort_keys=True,allow_nan=False);f.write(chr(10))
 print(json.dumps(dict(status=report['status'],pid=os.getpid(),gamma=gamma,allowance=allowance,bounds=bounds,sha256=sha(BASE/OUT))),flush=True)
if __name__=='__main__':main()

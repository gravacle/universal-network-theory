"""HELD root-only actual binary64 scalar-hat injectivity bound.
Only CLOSED94049 metadata and original BASIS hats/R/dv may be read.
Exact four-by-four Fraction reference algebra; no phase/action/science replay.
All-cell Neumann bound is conditional on future same-candidate positive H.
"""
from pathlib import Path
from fractions import Fraction
from datetime import datetime,timezone
import hashlib,json,math,os,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
STEM='CLOSED_REGISTERED_SCALAR_HAT_CONDITIONING_AUDIT_V002'
PARENT_SOURCE_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
PINS={
 'CROSS_U_FINITE0_CANDIDATE_ACTION_RESIDUAL_V007_ERROR.json':'4edf894c38ee0fd2ff54996ba45dd444f7ca3ccdedfc81c8dd3cd67ccf8a7bcd',
 'CROSS_U_FINITE0_CANDIDATE_ACTION_RESIDUAL_V007_RECEIPT.json':'3e333a3023836a16c3d90701bcc49134fd022c9a990b2ce2bdf4a8551c852543',
 'CROSS_U_CANONICAL_NODAL_METRIC_RATE_SOLVE_V001_00007_BASIS.npz':'28bb1ba976b88bfa6b96a7d614524f5760faa79a111da8f75fcaacc7ca95f93f',
 'CROSS_U_CANONICAL_NODAL_METRIC_RATE_SOLVE_V001_00007_BASIS.npz.COMMIT.json':'36d13345fc78b0afbad152f3f6e03ff381eaa8915b0b84cc4e2c333e00599c11'}
INPUTS={};OUTPUTS={};EVIDENCE={};OWNER=None

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def rational(x):return dict(numerator=str(x.numerator),denominator=str(x.denominator))
def matrix_words(A):return [[rational(x) for x in row] for row in A]
def converted(x,direction='nearest'):
 value=float(x);assert math.isfinite(value)
 if direction=='lower' and Fraction.from_float(value)>x:value=math.nextafter(value,-math.inf)
 if direction=='upper' and Fraction.from_float(value)<x:value=math.nextafter(value,math.inf)
 return dict(exact=rational(x),binary64=value,direction=direction,exact_minus_binary64=rational(x-Fraction.from_float(value)))
def publish(name,obj):
 path=BASE/name;data=(json.dumps(obj,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
 with path.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
 path.chmod(0o444);OUTPUTS[name]=sha(path);return OUTPUTS[name]
def recheck():
 for n,h in INPUTS.items():assert sha(Path(n))==h,n
 assert sha(Path(__file__).resolve())==OWNER['source_sha256']
 for n,h in OUTPUTS.items():assert sha(BASE/n)==h,n

def selected_admission():
 for n,h in PINS.items():assert sha(BASE/n)==h,n;INPUTS[str((BASE/n).resolve())]=h
 e=json.loads((BASE/list(PINS)[0]).read_text());rc=json.loads((BASE/list(PINS)[1]).read_text())
 assert e['status']=='FAILED' and rc['status']=='CLOSED_ERROR' and rc['error_sha256']==PINS[list(PINS)[0]] and rc.get('result_sha256') is None
 assert e['owner']==rc['owner'] and e['owner']['pid']==94049 and e['owner']['source_sha256']==PARENT_SOURCE_SHA
 assert e['qualification']==rc['qualification'] and all(x is False for x in e['qualification'].values())
 ref=e['checkpoints'][1]['metadata']['reference'];assert ref['file']==list(PINS)[2] and ref['commit_file']==list(PINS)[3]
 assert ref['sha256']==PINS[ref['file']] and ref['commit_sha256']==PINS[ref['commit_file']]
 commit=json.loads((BASE/ref['commit_file']).read_text());assert commit=={k:ref[k] for k in ('file','sha256','metadata')}
 for n in (ref['file'],ref['commit_file']):assert rc['input_sha256'][str((BASE/n).resolve())]==PINS[n]
 md=ref['metadata'];assert md['failed'] is False and md['axis_reflection'] is True and md['scalar_dofs']==3870
 for n,shape in (('hats',[4,4,3,86,44]),('R',[4,3784]),('dv',[4,3784])):assert md['schema'][n]==dict(dtype='float64',finite=True,shape=shape)
 return ref,e['qualification']

def exact_reference_inverse(B):
 EVIDENCE.update(reference_cell=[0,0],reference_hat_matrix=matrix_words(B));A=[row[:]+[Fraction(int(i==j)) for j in range(4)] for i,row in enumerate(B)]
 for column in range(4):
  EVIDENCE.update(exact_inverse_pivot_column=column,exact_inverse_augmented_before_pivot=matrix_words(A))
  candidates=[i for i in range(column,4) if A[i][column]!=0];assert candidates,'Stored reference hat matrix singular'
  pivot=candidates[0];A[column],A[pivot]=A[pivot],A[column];v=A[column][column];A[column]=[x/v for x in A[column]]
  for i in range(4):
   if i!=column:
    factor=A[i][column];A[i]=[x-factor*y for x,y in zip(A[i],A[column])]
  EVIDENCE['exact_inverse_augmented_completed_pivot']=matrix_words(A)
 inverse=[row[4:] for row in A]
 assert all(sum(B[i][k]*inverse[k][j] for k in range(4))==int(i==j) for i in range(4) for j in range(4))
 EVIDENCE['exact_reference_inverse']=matrix_words(inverse);return inverse

def actual_basis_bound(ref):
 import numpy as np
 with np.load(BASE/ref['file'],allow_pickle=False) as f:
  assert set(f.files)==set(ref['metadata']['schema'])|{'metadata_json'} and json.loads(str(f['metadata_json']))==ref['metadata']
  hats=f['hats'].copy();R=f['R'].copy();dv=f['dv'].copy()
 for n,a in (('hats',hats),('R',R),('dv',dv)):assert a.dtype==np.float64 and list(a.shape)==ref['metadata']['schema'][n]['shape'] and np.all(np.isfinite(a)),n
 EVIDENCE.update(only_numerical_payload_fields_read=['hats','R','dv'],R_min=float(R.min()),dv_min=float(dv.min()),reference_cell_predeclared=True)
 assert np.all(R>0) and np.all(dv>0)
 F=lambda x:Fraction.from_float(float(x));B=[[F(hats[q,k,0,0,0]) for k in range(4)] for q in range(4)];inverse=exact_reference_inverse(B)
 row_sums=[sum(abs(x) for x in row) for row in inverse];b=max(row_sums);assert b>0;EVIDENCE.update(reference_inverse_row_sums=[rational(x) for x in row_sums],b=converted(b,'upper'))
 d=Fraction(-1);maximizers=[]
 for i in range(86):
  for j in range(44):
   for q in range(4):
    row=[F(hats[q,k,0,i,j]) for k in range(4)];difference=[x-y for x,y in zip(row,B[q])];value=sum(abs(x) for x in difference)
    EVIDENCE.update(current_cell=[i,j],current_quadrature_row=q,current_hat_row=[rational(x) for x in row],current_reference_difference=[rational(x) for x in difference],current_row_sum=rational(value))
    if value>d:d=value;maximizers=[[i,j,q]]
    elif value==d:maximizers.append([i,j,q])
    EVIDENCE.update(maximum_cell_reference_difference=rational(d),maximum_cell_row_indices=maximizers)
 eta=b*d;c=1/b-d;EVIDENCE.update(cells_checked=3784,rows_checked=15136,d=converted(d,'upper'),eta=converted(eta,'upper'),c=converted(c,'lower'))
 assert eta<1 and c>0,'Actual serialized hats did not earn Neumann injectivity'
 coverage=np.zeros((87,45),dtype=np.int64)
 for i in range(86):
  for j in range(44):
   for di,dj in ((0,0),(1,0),(0,1),(1,1)):coverage[max(i+di,1),j+dj]+=1
 independent=coverage[1:];assert independent.shape==(86,45) and independent.size==3870 and np.all(independent>=1) and np.all(coverage[0]==0) and int(coverage.sum())==15136
 EVIDENCE.update(independent_node_count=3870,minimum_corner_coverage=int(independent.min()),axis_row0_identified_with_row1=True,outer_and_top_scalar_nodes_free=True,local_sigma_min_lower=converted(c/2,'lower'),conditional_global_mass_coefficient=converted(c*c/4,'lower'))
 return dict(status='ACTUAL_REGISTERED_SCALAR_HAT_INJECTIVITY_BOUND_PASS',evidence=dict(EVIDENCE),phase_mass_bound='x^T Mphi x >= w_min*c^2/4 * ||independent x||_2^2',future_weight_definition='w_min=min(real_literal_H * registered_binary64(dv/R)) over all4 quadrature sections',actual_four_section_H_read_or_admitted=False,actual_phase_mass_SPD_qualified=False,binary64_coefficient_real_polynomial_bound=True,rounded_DD_operator_error_bound_earned=False,action_EOS_scalar_scatter_solver_eigen_or_old_fixture_replayed=False,physical_adoption=False)

def main():
 global OWNER
 assert AUTHOR_DRAFT is False and not AUTHORING_IN_PROGRESS,'Root release required';assert not list(BASE.glob(STEM+'_*')),'Exclusive namespace required'
 OWNER=dict(owner='root',pid=os.getpid(),started=datetime.now(timezone.utc).isoformat(),source_sha256=sha(Path(__file__).resolve()));INPUTS[str(Path(__file__).resolve())]=OWNER['source_sha256']
 try:
  publish(STEM+'_OWNER_START.json',OWNER);ref,qualifications=selected_admission();EVIDENCE['original94049_qualifications']=qualifications
  result=actual_basis_bound(ref);recheck();h=publish(STEM+'_RESULT.json',dict(result,owner=OWNER,reference=dict(file=ref['file'],sha256=ref['sha256'],commit_file=ref['commit_file'],commit_sha256=ref['commit_sha256']),input_sha256=INPUTS));recheck();publish(STEM+'_RECEIPT.json',dict(owner=OWNER,status='CLOSED',closed=datetime.now(timezone.utc).isoformat(),result_sha256=h,error_sha256=None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS)));recheck();print(result['status'],h);return 0
 except BaseException:
  failure=traceback.format_exc();h=publish(STEM+'_ERROR.json',dict(owner=OWNER,status='FAILED',traceback=failure,available_exact_basis_evidence=EVIDENCE,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),actual_phase_or_physical_adoption=False));prior=BASE/(STEM+'_RECEIPT.json');publish(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=OWNER,status='CLOSED_ERROR',closed=datetime.now(timezone.utc).isoformat(),error_sha256=h,prior_receipt_sha256=sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS)));recheck();raise
if __name__=='__main__':raise SystemExit(main())

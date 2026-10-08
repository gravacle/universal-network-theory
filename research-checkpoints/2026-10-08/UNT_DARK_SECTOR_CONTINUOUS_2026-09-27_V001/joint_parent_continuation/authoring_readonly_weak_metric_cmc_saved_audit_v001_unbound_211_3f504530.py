"""Prospective saved-only reader. Terminal pins MUST be bound by root after closure.

No producer import, M application, Gram construction, eigensystem, field reconstruction,
inverse, solve, fixture replay or evolution. Contractions use only stored operands.
"""
from pathlib import Path
import hashlib,json,math,os,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_WEAK_NODAL_METRIC_TEMPORAL_CMC_V001'
AUDIT='READONLY_'+STEM+'_SAVED_AUDIT'
TERMINAL=dict(owner_pid=None,source_sha256='e11bb7ec123971998fbdd64d1e2171627aae9202804d1c625202f412b5f85b6c',protocol_sha256='60de28cc558734f648fc3845ebf18ab47b10f0cf9d06a89142e59268951baf7a',result_sha256=None,receipt_sha256=None,error_sha256=None)
np=None;MAX_IDENTITY_ERROR=0.;IDENTITIES=0;COUNTS=dict(pairs=0,numeric_arrays=0,numeric_entries=0,negative_entries=0,nonfinite_entries=0,metadata_arrays=0)

def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p

def sha(p):
 h=hashlib.sha256()
 with path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()

def json_read(n):return json.loads(path(n).read_text())

def false_flags(v):
 assert v and all(x is False for x in v.values()),v

def identity(label,a,b,envelope=None):
 global MAX_IDENTITY_ERROR,IDENTITIES
 a=np.asarray(a);b=np.asarray(b);assert a.shape==b.shape and np.all(np.isfinite(a)) and np.all(np.isfinite(b)),label
 e=np.abs(a)+np.abs(b) if envelope is None else np.asarray(envelope)
 assert e.shape==a.shape and np.all(np.isfinite(e)) and np.all(e>=0),label
 error=float(np.max(np.abs(a-b)/np.maximum(e,1e-30),initial=0))
 assert error<=2e-11,(label,error);MAX_IDENTITY_ERROR=max(MAX_IDENTITY_ERROR,error);IDENTITIES+=1

def scalar_same(label,a,b):
 assert math.isfinite(float(a)) and math.isfinite(float(b)) and abs(float(a)-float(b))<=2e-13*max(1.,abs(float(a)),abs(float(b))),(label,a,b)

def record_read(r):
 assert sha(r['file'])==r['sha256'] and sha(r['commit_file'])==r['commit_sha256']
 assert json_read(r['commit_file'])=={k:v for k,v in r.items() if k not in ('commit_file','commit_sha256')}
 out={};md=r['metadata'];false_flags(md['qualification']);assert md['owner']['pid']==TERMINAL['owner_pid']
 with np.load(path(r['file']),allow_pickle=False) as f:
  assert set(f.files)==set(md['schema'])|{'metadata_json'} and json.loads(str(f['metadata_json']))==md
  for k,s in md['schema'].items():
   a=f[k];assert list(a.shape)==s['shape'] and str(a.dtype)==s['dtype'] and a.dtype.kind in 'fiub',k
   finite=np.isfinite(a);assert bool(np.all(finite))==s['finite'],k
   if not md['failed']:assert s['finite'],k
   COUNTS['numeric_arrays']+=1;COUNTS['numeric_entries']+=a.size;COUNTS['negative_entries']+=int(np.count_nonzero(a<0));COUNTS['nonfinite_entries']+=int(a.size-np.count_nonzero(finite))
   out[k]=a.copy()
 COUNTS['metadata_arrays']+=1;COUNTS['pairs']+=1;return out

def parent_arrays(ref,names):
 assert sha(ref['file'])==ref['sha256'] and sha(ref['commit_file'])==ref['commit_sha256']
 rec=json_read(ref['commit_file']);assert rec['file']==ref['file'] and rec['sha256']==ref['sha256']
 with np.load(path(ref['file']),allow_pickle=False) as f:
  assert json.loads(str(f['metadata_json']))==rec['metadata'] and set(f.files)==set(rec['metadata']['schema'])|{'metadata_json'}
  out={}
  for k in names:
   a=f[k].copy();s=rec['metadata']['schema'][k];assert list(a.shape)==s['shape'] and str(a.dtype)==s['dtype'] and np.all(np.isfinite(a));out[k]=a
 return out

def stored_control(row,d):
 name=row['name'];k=row['ordinal']
 if name.endswith('_original_and_congruence_CG'):
  keys=[name+'_'+x for x in ('residual_norm','rhs_norm','scaled_residual_norm','scaled_rhs_norm','actual')];assert all(x in d for x in keys)
  a,b,c,e,ratio=[d[x] for x in keys];active=b>0;fresh=np.zeros_like(ratio)
  assert np.array_equal(active,e>0) and np.all(a[~active]==0) and np.all(c[~active]==0)
  fresh[active,0]=a[active]/b[active];fresh[active,1]=c[active]/e[active];identity(name+'_ratios',ratio,fresh)
  error=float(np.max(ratio,initial=0));assert row['tolerance']==1e-10
 else:
  prefix=f'control_{k:03d}_{name}_';a,b,e=[d[prefix+x] for x in ('actual','expected','envelope')]
  assert a.shape==b.shape==e.shape and np.all(np.isfinite(a)) and np.all(np.isfinite(b)) and np.all(np.isfinite(e)) and np.all(e>=0)
  error=float(np.max(np.abs(a-b)/np.maximum(e,1e-30),initial=0));assert row['tolerance']==2e-11
 scalar_same(name+'_stored_error',error,row['error']);assert (error<=row['tolerance']) is row['passed']

def six_tensor(a):
 # Algebraic coordinate unpacking only; metric velocities carry each offdiag once.
 t=np.zeros(a.shape[:-1]+(3,3));t[...,0,0]=a[...,0];t[...,1,1]=a[...,1];t[...,2,2]=a[...,2]
 for k,(i,j) in enumerate(((0,1),(0,2),(1,2)),3):t[...,i,j]=t[...,j,i]=a[...,k]
 return t

def saved_scalar_incidence(values,basis):
 # Contraction of stored quadrature weights and stored Q1 hats only. No field evaluation.
 out=np.zeros(values.shape[:-1]+(87,45));v=values.reshape((-1,4,3784));o=out.reshape((-1,87,45))
 ci=basis['geometry_cell_i'];cj=basis['geometry_cell_j'];w=basis['geometry_dv']/basis['geometry_R']
 for iq in range(4):
  for a,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   weighted=v[:,iq]*w[iq]*basis['geometry_hats'][iq,a,0].reshape(3784)
   for group in range(len(v)):np.add.at(o[group],(ci+di,cj+dj),weighted[group])
 o[:,1,:]+=o[:,0,:];o[:,0,:]=0;return out

def main():
 global np
 # No live prefix read and no NumPy import precedes authenticated terminal bindings.
 if TERMINAL['owner_pid'] is None or TERMINAL['receipt_sha256'] is None or (TERMINAL['result_sha256'] is None and TERMINAL['error_sha256'] is None):raise SystemExit('HELD: root CLOSED notice, terminal pins and audit authorization required.')
 print('READONLY_METRIC_CMC_AUDIT_PID',os.getpid(),flush=True)
 assert sha('cross_u_weak_nodal_metric_temporal_cmc_v001.py')==TERMINAL['source_sha256'] and sha(STEM+'.md')==TERMINAL['protocol_sha256'] and sha(STEM+'_RECEIPT.json')==TERMINAL['receipt_sha256']
 rc=json_read(STEM+'_RECEIPT.json');assert rc['status'] in ('CLOSED','CLOSED_ERROR') and rc['closed'] and rc['owner']['owner']=='root' and rc['owner']['pid']==TERMINAL['owner_pid'] and rc['owner']['source_sha256']==TERMINAL['source_sha256'];false_flags(rc['qualification'])
 hashes={}
 for key in ('input_sha256','output_sha256'):
  for n,h in rc[key].items():assert n not in hashes or hashes[n]==h;hashes[n]=h;assert sha(n)==h,n
 for n in rc['output_sha256']:assert path(n).stat().st_mode&0o777==0o444,n
 assert path(STEM+'_RECEIPT.json').stat().st_mode&0o777==0o444
 success=TERMINAL['error_sha256'] is None
 if TERMINAL['result_sha256'] is not None:assert sha(STEM+'_RESULT.json')==TERMINAL['result_sha256']==rc['result_sha256']
 if success:
  assert sha(STEM+'_RESULT.json')==TERMINAL['result_sha256']==rc['result_sha256'];doc=json_read(STEM+'_RESULT.json')
  assert doc['status']=='CONDITIONAL_WEAK_METRIC_TEMPORAL_CMC_ARITHMETIC_PASS' and len(doc['cases'])==1 and doc['cases'][0]['sigma']==1.
 else:
  assert sha(STEM+'_ERROR.json')==TERMINAL['error_sha256'];doc=json_read(STEM+'_ERROR.json');assert doc['status']=='FAILED'
  if rc['status']=='CLOSED_ERROR':assert rc['error_sha256']==TERMINAL['error_sha256']
  else:assert doc['prior_receipt_sha256']==TERMINAL['receipt_sha256']
  for n,h in doc['preserved_outputs'].items():assert sha(n)==h
 assert doc['owner']==rc['owner'];false_flags(doc['qualification']);records=doc['checkpoints'];controls=doc['controls']
 if success:assert len(controls)==49 and all(x['passed'] for x in controls) and len(records)<=64
 else:assert len(controls)<=49 and len(records)<=65
 assert [x['ordinal'] for x in controls]==list(range(len(controls)))
 normal=[r for r in records if r['metadata']['kind']!='resumable_unqualified_native_iterate' and not r['metadata']['failed']]
 if success:assert len(normal)==16
 expected={r['file'] for r in records};expected_commit={r['commit_file'] for r in records}
 actual={p.name for p in BASE.glob(STEM+'_*.npz')};actual_commit={p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}
 if success:assert actual==expected and actual_commit==expected_commit
 else:
  declared=set(doc['unqualified_npz']);assert actual==expected|declared and expected_commit<=actual_commit
  for n in actual|actual_commit:assert n in doc['preserved_outputs'] and sha(n)==doc['preserved_outputs'][n]
 import numpy as _np
 np=_np;groups={};control_witness={};columns=[];solves=[]
 for r in records:
  d=record_read(r);kind=r['metadata']['kind']
  for row in r['metadata'].get('controls',[]):
   assert row==controls[row['ordinal']];stored_control(row,d);control_witness[row['ordinal']]=True
  if r['metadata']['failed']:
   for row in controls:
    key=row['name']+'_actual' if row['name'].endswith('_original_and_congruence_CG') else f"control_{row['ordinal']:03d}_{row['name']}_actual"
    if key in d:stored_control(row,d);control_witness[row['ordinal']]=True
  if kind=='six_new_metric_time_columns_and_affine_CMC_operands':
   ks=d['current_metric_time_jet'];vs=d['current_native_velocity_star'];B=d['B'];T=d['T_total']
   bk=np.einsum('pia,pa->pi',B,ks);identity('B_kstar',d['native_B_kstar'],bk,d['native_B_kstar_envelope'])
   bv=np.einsum('pia,pi->pa',B,vs);tk=np.einsum('pab,pb->pa',T,ks)
   identity('metric_affine_offset',d['metric_affine_offset'],d['current_metric_pistar']-bv-tk,d['metric_affine_offset_envelope'])
   identity('saved_native_gap',d['saved_affine_gap'],d['current_native_pstar']-d['old_native_target'])
   identity('native_plus_EH',T,d['T_native']+d['T_EH'],d['T_total_envelope'])
   identity('stored_metric_Gram',d['T_native'],d['independent_six_metric_Gram'],d['T_native_envelope']+d['independent_six_metric_Gram_envelope'])
   kt=(d['current_metric_time_tensor']-d['saved_Lie_beta_h'])/(2*d['current_N'][:,None,None]);identity('saved_K_tensor',d['independent_K_tensor'],kt,d['independent_K_envelope'])
   identity('saved_Ktrace',d['independent_Ktrace'],np.einsum('pij,pij->p',d['current_ih'],kt),d['independent_Ktrace_envelope'])
   columns.append({k:d[k] for k in ('B','T_total','T_total_envelope','current_ih','current_N','current_sqrt_h','metric_affine_offset','native_B_kstar','saved_Lie_beta_h')})
   groups.setdefault(kind,[]).append((r,columns[-1]))
  elif kind in ('resumable_unqualified_native_iterate','unqualified_available_weak_metric_operands'):groups.setdefault(kind,[]).append((r,None))
  else:groups.setdefault(kind,[]).append((r,d))
  if kind=='new_metric_column_original_weak_native_solve':solves.append((r,d))
  if kind=='resumable_unqualified_native_iterate':identity('iteration_saved_residual',d['native_original_residual'],d['native_original_residual'])
 if success:assert set(control_witness)==set(range(49)) and len(columns)==4 and len(solves)==6
 if not success:
  report=dict(status='SAVED_CLOSED_FAILURE_CUSTODY_AUDIT_PASS',terminal=TERMINAL,census=COUNTS,control_count=len(controls),witnessed_control_ordinals=sorted(control_witness),unwitnessed_control_ordinals=sorted(set(range(len(controls)))-set(control_witness)),copied_false_controls=[x for x in controls if not x['passed']],completed_normal_pairs=len(normal),unqualified_files=sorted(actual-expected),identity_count=IDENTITIES,max_identity_error=MAX_IDENTITY_ERROR,scientific_operator_or_producer_replay=False)
 else:
  inp=groups['same_sigma1_grid_modes_and_authenticated_CLOSED_weak99'][0][1];basis=groups['regular_six_metric_temporal_Q1_basis'][0][1];sample=groups['six_hat_signed_global_metric_Schur_sample'][0][1];affine=groups['full_weak_affine_offsets_and_CMC_trace_operator_data'][0][1]
  weak=json_read('CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001_RESULT.json');prep=next(x for x in weak['checkpoints'] if x['metadata']['kind']=='preconditioner_only_positive_node_block');scale=parent_arrays(prep,('kinetic_congruence_scale',))['kinetic_congruence_scale']
  for a,(r,d) in enumerate(sorted(solves,key=lambda x:x[0]['metadata']['probe'])):
   assert r['metadata']['probe']==a;rhs=d['new_metric_native_rhs'];res=d['new_metric_native_original_residual'];act=d['new_metric_native_original_action'];identity('linear_residual_'+str(a),res,rhs-act,abs(rhs)+abs(act))
   label=f'new_metric_{a}_original_and_congruence_CG'
   for suffix,value in (('residual_norm',np.linalg.norm(res)),('rhs_norm',np.linalg.norm(rhs)),('scaled_residual_norm',np.linalg.norm(res/scale)),('scaled_rhs_norm',np.linalg.norm(rhs/scale))):scalar_same(label+'_'+suffix,value,d[label+'_'+suffix][0])
   assert np.max(d[label+'_actual'])<=1e-10 and r['metadata']['iterations']<=160
   identity('solution_copy',sample['six_new_nodal_native_solutions'][a],d['new_metric_native_nodal_solution']);identity('action_copy',sample['six_new_native_original_actions'][a],act);identity('residual_copy',sample['six_new_native_original_residuals'][a],res)
  rhs=sample['six_new_native_RHS'];yy=sample['six_new_nodal_native_solutions'];rr=sample['six_new_native_original_residuals'];T=sample['sampled_full_T'];E=sample['sampled_global_elimination'];S=sample['sampled_signed_global_Schur']
  kv=sample['six_metric_unit_hat_qvalues'];wq=(basis['geometry_dv']/basis['geometry_R']).reshape(15136);total=np.concatenate([x['T_total'] for x in columns]);totalenv=np.concatenate([x['T_total_envelope'] for x in columns])
  direct=np.einsum('p,Apa,pab,Bpb->AB',wq,kv,total,kv);identity('sample_direct_T',T,direct,sample['sampled_full_T_envelope'])
  elimination=np.einsum('Agcrz,Bgcrz->AB',rhs,yy);identity('sample_elimination',E,elimination,sample['sampled_global_elimination_envelope'])
  identity('signed_Schur',S,T-E,sample['sampled_full_T_envelope']+sample['sampled_global_elimination_envelope'])
  cross=np.einsum('Agcrz,Bgcrz->AB',rr,yy);identity('Schur_residual_antisymmetry',S-S.T,T-T.T-cross+cross.T,sample['sampled_full_T_envelope']+sample['sampled_full_T_envelope'].T+sample['sampled_global_elimination_envelope']+sample['sampled_global_elimination_envelope'].T+np.einsum('Agcrz,Bgcrz->AB',abs(rr),abs(yy))+np.einsum('Bgcrz,Agcrz->AB',abs(rr),abs(yy)))
  Q=sample['sampled_positive_metric_Gram'];W=sample['sampled_metric_congruence'];eQ=sample['sampled_metric_Gram_envelope'];identity('positive_Gram_certificate',W.T@Q@W,np.eye(6),abs(W).T@eQ@abs(W)+np.eye(6))
  normalized=W.T@S@W;identity('signed_congruence',sample['sampled_metric_normalized_global_Schur'],normalized,abs(W).T@(sample['sampled_full_T_envelope']+sample['sampled_global_elimination_envelope'])@abs(W))
  eigen=sample['sampled_signed_global_Schur_eigenvalues'];assert eigen.shape==(6,) and np.all(np.diff(eigen)>=0);sym=(normalized+normalized.T)/2
  identity('eigen_trace_only',np.array(np.sum(eigen)),np.array(np.trace(sym)),np.array(np.sum(abs(eigen))+np.sum(abs(np.diag(sym)))))
  identity('eigen_square_trace_only',np.array(np.sum(eigen*eigen)),np.array(np.sum(sym*sym)),np.array(np.sum(eigen*eigen)+np.sum(sym*sym)))
  identity('affine_native_RHS',affine['new_affine_native_weak_RHS'],affine['old_fixed_kstar_native_weak_RHS']+affine['full_affine_B_kstar_weak_load'],affine['new_affine_native_weak_RHS_envelope'])
  identity('affine_incidence_copy',affine['full_affine_B_kstar_weak_load'],affine['full_affine_B_kstar_independent_load'],affine['full_affine_B_kstar_weak_envelope']+abs(affine['full_affine_B_kstar_independent_load']))
  identity('CMC_weak_gap_relation',affine['CMC_star_weak_gap'],affine['CMC_star_metric_trace_action']-affine['CMC_scalar_star_RHS'],abs(affine['CMC_star_metric_trace_action'])+abs(affine['CMC_scalar_star_RHS']))
  identity('CMC_saved_literal',affine['CMC_scalar_star_RHS'],affine['CMC_independent_scalar_star_RHS'],groups['full_weak_affine_offsets_and_CMC_trace_operator_data'][0][1]['control_048_CMC_star_load_independent_saved_shift_geometry_envelope'])
  ih=affine['current_ih'];N=affine['current_N'];mu=affine['current_sqrt_h'];ks=affine['current_metric_time_jet'];K=affine['current_Kstar'];H=groups['same_sigma1_grid_modes_and_authenticated_CLOSED_weak99'][0][0]['metadata']['Hbar']
  trace=np.einsum('pij,pij->p',ih,six_tensor(ks))/(2*N);lie=np.concatenate([x['saved_Lie_beta_h'] for x in columns]);lie_trace=np.einsum('pij,pij->p',ih,lie)/(2*N)
  ck=saved_scalar_incidence(mu*trace,basis);env=saved_scalar_incidence(mu*(abs(trace)+abs(K)+3*abs(H)+abs(lie_trace)),basis)
  identity('CMC_trace_saved_incidence',affine['CMC_star_metric_trace_action'],ck,env)
  identity('CMC_RHS_saved_incidence',affine['CMC_scalar_star_RHS'],saved_scalar_incidence(mu*(3*H-K),basis)+ck,env)
  identity('CMC_literal_saved_incidence',affine['CMC_independent_scalar_star_RHS'],saved_scalar_incidence(mu*(3*H+lie_trace),basis),env)
  hat_trace=np.einsum('pij,Apij->Ap',ih,six_tensor(kv))/(2*N[None]);hat_bound=saved_scalar_incidence(mu[None]*np.einsum('pij,Apij->Ap',abs(ih),abs(six_tensor(kv)))/(2*N[None]),basis)
  identity('CMC_six_trace_saved_incidence',affine['CMC_six_hat_trace_columns'],saved_scalar_incidence(mu[None]*hat_trace,basis),hat_bound)
  local=np.stack((ih[:,0,0],ih[:,1,1],ih[:,2,2],2*ih[:,0,1],2*ih[:,0,2],2*ih[:,1,2]),axis=1)*mu[:,None]/(2*N[:,None]);identity('CMC_local_trace',affine['CMC_local_trace_coefficients'],local)
  identity('CMC_point_gap',affine['CMC_star_point_gap'],K-3*H,abs(K)+np.full_like(K,3*abs(H)))
  identity('full_ks_column_copy',ks,np.concatenate([record_read_small(r,'current_metric_time_jet') for r,_ in groups['six_new_metric_time_columns_and_affine_CMC_operands']]))
  identity('six_hat_affine_pairing',affine['six_hat_metric_affine_pairing'],np.einsum('Aaij,aij->A',sample['six_metric_unit_hats'],affine['full_metric_affine_weak_load']))
  for k in ('native_affine_baseline_inverse','metric_momentum_target_selected','metric_rate_selected','full_CMC_lapse_force','CMC_preservation_force','phase_current_evolution','ordinary_worldline_evolution','temporal_gauge_rates','exterior_ports','physical_worldtube','activity_outside_measured_support'):assert groups['full_weak_affine_offsets_and_CMC_trace_operator_data'][0][0]['metadata'][k] is None
  report=dict(status='SAVED_PACKET_AUDIT_PASS',terminal=TERMINAL,census=COUNTS,control_count=49,normal_pair_count=16,iteration_pair_count=len(records)-16,identity_count=IDENTITIES,max_identity_error=MAX_IDENTITY_ERROR,signed_sample_eigenvalues=eigen.tolist(),native_iterations=[r['metadata']['iterations'] for r,d in solves],qualification=doc['qualification'],scientific_operator_or_producer_replay=False,scope='Stored arithmetic and certificates only; no full metric/CMC/force/history/source/inertia qualification.')
 for n,h in hashes.items():assert sha(n)==h
 report['input_bindings']=len(rc['input_sha256']);report['output_bindings']=len(rc['output_sha256']);report['audit_pid']=os.getpid()
 publish_report(AUDIT+'.json',report);print(json.dumps({k:report[k] for k in ('status','audit_pid','census','control_count','identity_count','max_identity_error')},sort_keys=True),flush=True)

def record_read_small(r,k):
 with np.load(path(r['file']),allow_pickle=False) as f:return f[k].copy()

def publish_report(n,report):
 raw=(json.dumps(report,sort_keys=True,indent=2,allow_nan=False)+'\n').encode();p=path(n)
 with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);assert p.read_bytes()==raw;print('READONLY_AUDIT_SHA256',sha(n),flush=True)

if __name__=='__main__':
 try:main()
 except BaseException:
  if TERMINAL['owner_pid'] is not None and TERMINAL['receipt_sha256'] is not None:
   publish_report(AUDIT+'_READER_REFUSAL.json',dict(status='READER_REFUSAL',terminal=TERMINAL,audit_pid=os.getpid(),traceback=traceback.format_exc(),source_sha256=sha(__file__)))
  raise

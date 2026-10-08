"""Held saved adjoint words only; no transpose, positive chain or fixture replay."""
from pathlib import Path
import hashlib,json,math,os
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_FROZEN_RATE_ACTUAL_ADJOINT_RANGE_V001'
OUT='READONLY_FROZEN_RATE_ACTUAL_ADJOINT_CLOSURE_V001_RESULT.json'
AUTHOR_DRAFT=True
SOURCE_SHA='8b840a5ccceae242d029b07820092f386a65015e661c6b8f24a19b81aaf88a4c'
PROTOCOL_SHA='a2f44c088cf83771569b117c0a3c5fc1928cfb6ed98c12e2746790c2cbc408a9'
TERMINAL=dict(pid=None,result_sha256=None,receipt_sha256=None,error_sha256=None)
PARENT=dict(pid=75215,result_sha256='4fa6fe13c1a32163cb9f867143389946eda19fc17e001834400346483417af0e',receipt_sha256='0a7a1c4b8c0d8f334b8404d41644955dd32e4305443b53c2125655d3c578e0cb',error_sha256=None)
PARENT_PROOF='READONLY_RECYCLED_TRACE_RESPONSE_CLOSURE_V001_RESULT.json'
PARENT_PROOF_SHA='dd392d8a8ea0dba45e418efa34d53f5c0e6f0ce1340f6c7e113f6a502f928055'
TOL=2e-11;ROW_TOL=1e-10

def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p
def sha(n):
 h=hashlib.sha256()
 with path(n).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def js(n,h):
 assert h is not None and sha(n)==h,n
 return json.loads(path(n).read_text())
def thin(q):return {n:q[n] for n in ('file','sha256','commit_file','commit_sha256')}

def main():
 assert AUTHOR_DRAFT is False and TERMINAL['pid'] is not None and TERMINAL['receipt_sha256'] is not None and not path(OUT).exists(),'Reviewed actual natural closure required before I/O'
 assert (TERMINAL['result_sha256'] is None)!=(TERMINAL['error_sha256'] is None)
 assert sha('cross_u_frozen_rate_actual_adjoint_range_v001.py')==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA
 receipt=STEM+('_ERROR_RECEIPT.json' if TERMINAL['error_sha256'] is not None and path(STEM+'_ERROR_RECEIPT.json').exists() else '_RECEIPT.json');rc=js(receipt,TERMINAL['receipt_sha256']);closed=rc['status']=='CLOSED';assert rc['status'] in ('CLOSED','CLOSED_ERROR')
 r=js(STEM+('_RESULT.json' if closed else '_ERROR.json'),TERMINAL['result_sha256'] if closed else TERMINAL['error_sha256']);assert rc.get('result_sha256')==TERMINAL['result_sha256'] and rc.get('error_sha256')==TERMINAL['error_sha256'] and rc['owner']==r['owner'] and r['owner']['pid']==TERMINAL['pid'] and r['owner']['source_sha256']==SOURCE_SHA
 assert r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values());records=r['checkpoints'];controls=r['controls'];assert len({q['file'] for q in records})==len(records)
 assert {p.name for p in BASE.glob(STEM+'_*.npz')}=={q['file'] for q in records} and {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={q['commit_file'] for q in records}
 for q in records:
  for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert rc['output_sha256'][n]==h and sha(n)==h,n
  assert js(q['commit_file'],q['commit_sha256'])=={k:q[k] for k in ('file','sha256','metadata')} and q['metadata']['owner']==r['owner'] and q['metadata']['qualification']==r['qualification']
  if closed:assert q['metadata']['failed'] is False and all(v['finite'] for v in q['metadata']['schema'].values())
 assert [c['ordinal'] for c in controls]==list(range(len(controls))) and len(controls)<=5 and all(c['tolerance']==TOL and math.isfinite(c['error']) and c['passed']==(c['error']<=TOL) for c in controls)
 import numpy as np
 selected=[];identities=[]
 def read(q,names):
  out={};sc=q['metadata']['schema']
  with np.load(path(q['file']),allow_pickle=False) as f:
   assert set(f.files)==set(sc)|{'metadata_json'} and json.loads(str(f['metadata_json']))==q['metadata']
   for n in names:
    a=f[n].copy();assert list(a.shape)==sc[n]['shape'] and str(a.dtype)==sc[n]['dtype'] and sc[n]['finite'] and np.all(np.isfinite(a)),n;out[n]=a
  selected.append(dict(file=q['file'],fields=len(names)));return out
 def parent(q):
  for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert rc['input_sha256'][str(path(n).resolve())]==h and sha(n)==h
  a=js(q['commit_file'],q['commit_sha256']);assert a['file']==q['file'] and a['sha256']==q['sha256'];return dict(a,commit_file=q['commit_file'],commit_sha256=q['commit_sha256'])
 def pair(a,n):return a[n+'_hi'],a[n+'_lo']
 def total(p):return p[0]+p[1]
 def identity(label,terms,envelope=None):
  words=[sign*x for sign,p in terms for x in p];gap=np.add.reduce(words);bound=np.add.reduce([abs(x) for x in words]) if envelope is None else envelope;assert gap.shape==bound.shape and np.all(bound>=0)
  error=float(np.max(abs(gap)/np.maximum(bound,1e-30),initial=0));assert error<=TOL,(label,error);identities.append(dict(name=label,error=error))
 def close(label,a,b):
  assert np.allclose(np.asarray(a),np.asarray(b),rtol=TOL,atol=1e-300),label
  identities.append(dict(name=label,error=float(np.max(abs(np.asarray(a)-np.asarray(b))/np.maximum(abs(np.asarray(a))+abs(np.asarray(b)),1e-30),initial=0))))
 for c in controls:
  prefix='control_%03d_%s_'%(c['ordinal'],c['name']);names=tuple(prefix+n for n in ('actual','expected','envelope'));hits=[q for q in records if all(n in q['metadata']['schema'] for n in names)];assert hits,c;a=read(hits[0],names)
  for q in hits[1:]:
   b=read(q,names);assert all(np.array_equal(a[n],b[n]) for n in names)
  actual,expected,envelope=(a[n] for n in names);assert np.all(envelope>=0);error=float(np.max(abs(actual-expected)/np.maximum(envelope,1e-30),initial=0));assert error==c['error'];identities.append(dict(name=c['name']+'_saved_triplet',error=error))
 if not closed:report=dict(status='SAVED_ACTUAL_ADJOINT_FAILURE_PRESERVED',controls=len(controls),committed_pairs=len(records),context=r.get('context'),obstruction_certified=False,canonical_response_admitted=False)
 else:
  inp,fixture,adj,ro=(r[n] for n in ('input','fixture','adjoint','readout'));assert records==[inp,fixture,adj,ro] and len(controls)==5 and all(c['passed'] for c in controls);im,am,lm=(q['metadata'] for q in (inp,adj,ro))
  assert r['status']=='ACTUAL_FROZEN_ADJOINT_DIAGNOSTIC_COMPLETE' and im['controls']==controls[:1] and fixture['metadata']['controls']==controls[:3] and am['controls']==controls[3:] and im['candidate_normalization_words_earned'] and im['old_action_coarse_fixture_or_solver_replayed'] is False
  assert im['parent_terminal']==r['parent_terminal']==PARENT and r['parent_original_nonadmission_preserved'] and all(r[n] is False for n in ('canonical_response_admitted','obstruction_certified','physical_adoption'))
  assert r['diagnostic']=={n:am[n] for n in r['diagnostic']}=={n:lm[n] for n in r['diagnostic']} and all(am[n] is False for n in ('candidate_left_null_admitted','obstruction_certified','literal_adjoint_evaluated','native_global_invertibility_or_coercivity_assumed','physical_adoption')) and am['near_null_is_descriptive_only'] and am['original_six_gates_unchanged'] and am['physical_ports'] is None
  assert lm['registered_literal_range_or_gauge_admission'] is False and lm['canonical_response_admitted'] is False and lm['finite_configuration_prepared'] is False and am['source_qualification']==im['source_qualification'] and all(v is False for v in am['source_qualification'].values())
  assert rc['input_sha256'][str(path(PARENT_PROOF).resolve())]==PARENT_PROOF_SHA;proof=js(PARENT_PROOF,PARENT_PROOF_SHA);assert proof['parent']==PARENT and proof['status']=='SAVED_RECYCLED_TRACE_RESPONSE_CLOSURE_PASS' and proof['frozen_original_response_admitted'] is False and proof['literal_original_response_admitted'] is False
  pi,pr,pl=(parent(im[n]) for n in ('input_ref','response_ref','readout_ref'));assert thin(adj['metadata']['input_ref'])==thin(inp) and thin(lm['input_ref'])==thin(inp) and thin(lm['adjoint_ref'])==thin(adj) and thin(lm['fixture_ref'])==thin(fixture)
  input_names=tuple(n+'_'+w for n in ('NEW_t_target_RHS','saved_final_paired_response','saved_final_frozen_action','saved_final_frozen_residual','candidate_original_saved_residual','candidate_white_residual','candidate_normalized_white_words','candidate_actual_left_test_words','candidate_scaled_words','candidate_reconstructed_residual','candidate_definition_division_and_normalization_gap') for w in ('hi','lo'))+('unchanged_positive_coordinate_scale','candidate_fixed_normalizing_norm','candidate_white_norm_only_readout','candidate_definition_positive_bound','original_basis_native_scale','original_basis_metric_scale','inherited_original_native_affine_reference','inherited_original_native_canonical_reference')
  ia=read(inp,input_names);rhs=pair(ia,'NEW_t_target_RHS');nodes=pair(ia,'saved_final_paired_response');action=pair(ia,'saved_final_frozen_action');res=pair(ia,'saved_final_frozen_residual');w=pair(ia,'candidate_actual_left_test_words');scale=ia['unchanged_positive_coordinate_scale'];norm=float(ia['candidate_fixed_normalizing_norm']);assert scale.shape==(403340,) and np.all(scale>0) and norm>0
  pa=read(pr,tuple(n+'_'+v for n in ('final_paired_response','final_frozen_action','final_frozen_residual','unchanged_original_RHS') for v in ('hi','lo')));assert all(np.array_equal(pair(pa,n)[j],p[j]) for n,p in (('final_paired_response',nodes),('final_frozen_action',action),('final_frozen_residual',res),('unchanged_original_RHS',rhs)) for j in (0,1))
  ca=read(pi,('NEW_t_target_RHS_hi','NEW_t_target_RHS_lo','original_basis_native_scale','original_basis_metric_scale','inherited_original_native_affine_reference','inherited_original_native_canonical_reference'));assert all(np.array_equal(ca[n],ia[n]) for n in ca)
  assert all(np.array_equal(pair(ia,'candidate_original_saved_residual')[j],res[j]) for j in (0,1));identity('saved_RHS_action_residual',[(1,rhs),(-1,action),(-1,res)])
  identity('candidate_saved_reconstruction_gap',[(1,res),(-1,pair(ia,'candidate_reconstructed_residual')),(-1,pair(ia,'candidate_definition_division_and_normalization_gap'))],ia['candidate_definition_positive_bound']);close('candidate_white_readout_copy',ia['candidate_white_norm_only_readout'],total(pair(ia,'candidate_white_residual')));close('candidate_fixed_norm',norm,np.linalg.norm(ia['candidate_white_norm_only_readout']))
  for label,source,out,den in (('candidate_first_scale_division',res,pair(ia,'candidate_white_residual'),scale),('candidate_norm_division',pair(ia,'candidate_white_residual'),pair(ia,'candidate_normalized_white_words'),np.asarray(norm)),('candidate_second_scale_division',pair(ia,'candidate_normalized_white_words'),w,scale)):
   da=read(inp,(label+'_denominator',label+'_quotient_hi',label+'_quotient_lo',label+'_division_defect_hi',label+'_division_defect_lo'));assert np.array_equal(da[label+'_denominator'],den) and all(np.array_equal(pair(da,label+'_quotient')[j],out[j]) for j in (0,1));identity(label+'_saved_defect',[(1,source),(-1,tuple(den*t for t in out)),(-1,pair(da,label+'_division_defect'))])
  fa=read(fixture,tuple(n+'_'+v for n in ('fresh_actual_adjoint_result','fresh_actual_adjoint_independent_dense_expected','fresh_actual_adjoint_forward_distinction','fresh_actual_adjoint_transpose_minus_forward') for v in ('hi','lo')));assert all(np.array_equal(pair(fa,'fresh_actual_adjoint_result')[j],pair(fa,'fresh_actual_adjoint_independent_dense_expected')[j]) for j in (0,1));identity('saved_fresh_transpose_forward_distinction',[(1,pair(fa,'fresh_actual_adjoint_result')),(-1,pair(fa,'fresh_actual_adjoint_forward_distinction')),(-1,pair(fa,'fresh_actual_adjoint_transpose_minus_forward'))]);assert np.linalg.norm(total(pair(fa,'fresh_actual_adjoint_transpose_minus_forward')))>0
  labels=('saved_forward_action_pairing','NEW_actual_adjoint_pairing','candidate_original_RHS_projection','candidate_latest_residual_projection','candidate_saved_forward_projection','candidate_saved_literal_minus_frozen_action_projection');values={}
  for q,names in ((fixture,('fresh_actual_adjoint_pairing_left','fresh_actual_adjoint_pairing_right')),(adj,labels)):
   for label in names:
    a=read(q,tuple(label+n for n in ('_original_product_terms_hi','_original_product_terms_lo','_value_hi','_value_lo')));p=pair(a,label+'_original_product_terms');value=pair(a,label+'_value');true=math.fsum(float(v) for z in p for v in z);bound=2*float(np.sum(abs(p[0])+abs(p[1])));err=abs(math.fsum(float(z) for z in value)-true)/max(bound,1e-30);assert err<=TOL;identities.append(dict(name=label+'_saved_product_reduction',error=err));values[label]=value
  an=tuple(n+'_'+v for n in ('candidate_actual_left_test_words','candidate_scaled_words','NEW_actual_frozen_polynomial_adjoint','NEW_scale_times_actual_adjoint','NEW_saved_forward_actual_adjoint_gap','candidate_saved_RHS_action_residual_projection_gap','saved_literal_minus_frozen_derivative') for v in ('hi','lo'))+('NEW_actual_adjoint_envelope_packed_positive','NEW_adjoint_white_norm_and_construction_allowance','unchanged_six_gate_absolute_thresholds','unchanged_six_gate_allowed_test_pairing_bound','candidate_scaled_norm_only','total_solution_projection_value_allowance_lower','new_correction_projection_value_allowance_lower','NEW_global_adjoint_pairing_positive_bound','candidate_saved_projection_identity_positive_bound');aa=read(adj,an);assert all(np.array_equal(pair(aa,'candidate_actual_left_test_words')[j],w[j]) and np.array_equal(pair(aa,'candidate_scaled_words')[j],pair(ia,'candidate_scaled_words')[j]) for j in (0,1))
  identity('saved_global_adjoint_pairing_gap',[(1,values['saved_forward_action_pairing']),(-1,values['NEW_actual_adjoint_pairing']),(-1,pair(aa,'NEW_saved_forward_actual_adjoint_gap'))],aa['NEW_global_adjoint_pairing_positive_bound']);identity('saved_projection_identity_gap',[(1,values['candidate_original_RHS_projection']),(-1,values['candidate_saved_forward_projection']),(-1,values['candidate_latest_residual_projection']),(-1,pair(aa,'candidate_saved_RHS_action_residual_projection_gap'))],aa['candidate_saved_projection_identity_positive_bound'])
  lb=read(pl,tuple('recycled_trace_literal_translation_literal_minus_frozen_derivative_'+v for v in ('hi','lo')));assert all(np.array_equal(pair(aa,'saved_literal_minus_frozen_derivative')[j],pair(lb,'recycled_trace_literal_translation_literal_minus_frozen_derivative')[j]) for j in (0,1));close('literal_frozen_saved_projection_metadata',am['literal_minus_frozen_action_projection'],total(values['candidate_saved_literal_minus_frozen_action_projection']))
  astar=pair(aa,'NEW_actual_frozen_polynomial_adjoint');scaled=pair(aa,'NEW_scale_times_actual_adjoint');identity('saved_scale_times_adjoint',[(1,scaled),(-1,tuple(scale*t for t in astar))]);eadj=aa['NEW_actual_adjoint_envelope_packed_positive'];assert np.all(eadj>=0)
  gamma=float(np.linalg.norm(total(scaled)));error=TOL*np.linalg.norm(scale*eadj)+128*np.finfo(float).eps*np.linalg.norm(abs(scaled[0])+abs(scaled[1]));close('adjoint_white_norm_allowance_interval',aa['NEW_adjoint_white_norm_and_construction_allowance'],(gamma,error,max(0.,gamma-error),gamma+error));close('adjoint_norm_metadata',(am['adjoint_white_norm'],am['adjoint_construction_allowance']),(gamma,error));assert am['stored_adjoint_words_exactly_zero']==bool(np.all(astar[0]==0) and np.all(astar[1]==0))
  nm=np.ones((33,3,87,45),bool);nm[:,:,0]=False;nm[:,1,:,0]=False;mm=np.ones((6,87,45),bool);mm[:,0]=False;mm[3:5,:,0]=False
  def fields(x):
   assert x.shape==(403340,);n=np.zeros(nm.shape);m=np.zeros(mm.shape);n[nm]=x[:380292];m[mm]=x[380292:];return n,m
  ns,ms=ia['original_basis_native_scale'],ia['original_basis_metric_scale'];assert np.array_equal(scale,np.concatenate((ns[nm],ms[mm])));nrefs=(ia['inherited_original_native_affine_reference'],ia['inherited_original_native_canonical_reference']);mr=fields(total(rhs))[1];wn,wm=fields(total(w));thresholds=np.asarray(((ROW_TOL*min(np.linalg.norm(t) for t in nrefs),ROW_TOL*min(np.linalg.norm(t/ns) for t in nrefs)),(ROW_TOL*np.linalg.norm(mr),ROW_TOL*np.linalg.norm(mr/ms))));close('unchanged_six_gate_absolute_thresholds',aa['unchanged_six_gate_absolute_thresholds'],thresholds)
  allowed=min(thresholds[0,0]*np.linalg.norm(wn),thresholds[0,1]*np.linalg.norm(ns*wn))+min(thresholds[1,0]*np.linalg.norm(wm),thresholds[1,1]*np.linalg.norm(ms*wm));close('unchanged_six_gate_test_pairing_bound',aa['unchanged_six_gate_allowed_test_pairing_bound'],allowed);close('candidate_scaled_norm',aa['candidate_scaled_norm_only'],np.linalg.norm(total(pair(aa,'candidate_scaled_words'))))
  for role,label,target in (('total_solution','candidate_original_RHS_projection',rhs),('new_correction','candidate_latest_residual_projection',res)):
   signed=float(total(values[label]));allowance=TOL*2*np.sum((abs(w[0])+abs(w[1]))*(abs(target[0])+abs(target[1])));lower=max(0.,abs(signed)-allowance-allowed);upper=gamma+error;necessary=lower/upper if upper>0 else None;close(role+'_projection_saved_scalars',aa[role+'_projection_value_allowance_lower'],(signed,allowance,lower));md=am['conditional_necessary_norm_bounds'][role];close(role+'_projection_metadata',(md['signed_pairing'],md['construction_allowance'],md['unresolved_pairing_lower']),(signed,allowance,lower));assert md['unknown_solution_norm_upper'] is None and (md['necessary_white_unknown_norm_lower'] is None)==(necessary is None)
   if necessary is not None:close(role+'_conditional_norm_lower',md['necessary_white_unknown_norm_lower'],necessary)
  ra=read(ro,tuple(ro['metadata']['schema']));comparison=read(adj,tuple(ra));assert all(np.array_equal(ra[n],comparison[n]) for n in ra)
  report=dict(status='SAVED_ACTUAL_FROZEN_ADJOINT_CLOSURE_PASS',producer_status=r['status'],controls=5,committed_pairs=4,parent75215_nonadmission_preserved=True,actual_adjoint_white_norm=gamma,displayed_adjoint_construction_allowance=float(error),conditional_necessary_norm_bounds=am['conditional_necessary_norm_bounds'],candidate_left_null_admitted=False,obstruction_certified=False,literal_adjoint_evaluated=False,native_global_invertibility_or_coercivity_assumed=False,canonical_response_admitted=False)
 report.update(owner_pid=os.getpid(),parent=TERMINAL,selected=selected,identities=identities,arithmetic_tolerance=TOL,original_row_tolerance=ROW_TOL,actual_adjoint_positive_chain_point_E_F_fixture_coarse_solver_or_producer_replayed=False,physical_adoption=False,scope_limit='Stored triplets, selected copies, saved division/reconstruction and product-word reductions, scalar norms and conditional-bound bookkeeping only. No transpose, positive-envelope chain, point polynomial, fixture, FE/scatter or solver is reconstructed. Frozen-versus-literal action remains separate; literal adjoint and exact null/rank/obstruction remain unearned.')
 for n,h in rc['output_sha256'].items():assert sha(n)==h
 assert sha(receipt)==TERMINAL['receipt_sha256'] and sha('cross_u_frozen_rate_actual_adjoint_range_v001.py')==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA
 with path(OUT).open('x') as f:json.dump(report,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
 path(OUT).chmod(0o444);print(json.dumps(dict(status=report['status'],pid=os.getpid(),sha256=sha(OUT))),flush=True)
if __name__=='__main__':main()

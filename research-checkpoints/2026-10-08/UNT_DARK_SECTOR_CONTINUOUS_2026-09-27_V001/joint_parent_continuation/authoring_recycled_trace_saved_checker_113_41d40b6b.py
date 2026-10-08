"""Guard-held saved recycled response words only; no producer or operator replay."""
from pathlib import Path
import hashlib,json,math,os
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_RECYCLED_TRACE_TARGET_RATE_RESPONSE_V001'
OUT='READONLY_RECYCLED_TRACE_RESPONSE_CLOSURE_V001_RESULT.json'
AUTHOR_DRAFT=True
SOURCE_SHA=None
PROTOCOL_SHA=None
TERMINAL=dict(pid=None,result_sha256=None,receipt_sha256=None,error_sha256=None)
ORIGINAL_TERMINAL=dict(pid=71394,result_sha256='6041c495ea6d837840d6f4bde687ba3dcf604131087c2ed7b395ae67fe284bb6',receipt_sha256='1aee74e2996755c644e242e78ecb488f2bc334dc63aa6568a5d3309f4c8235a3')
ORIGINAL_PROOF='READONLY_INITIAL_YORK_TRACE_TARGET_RESPONSE_CLOSURE_V001_RESULT.json'
ORIGINAL_PROOF_SHA='eb9c8fbe3736069d72b1be992e4637b33ff7b53408157a7f60ca510e7dcc4153'
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
 assert AUTHOR_DRAFT is False and SOURCE_SHA is not None and PROTOCOL_SHA is not None and TERMINAL['pid'] is not None and TERMINAL['receipt_sha256'] is not None and not path(OUT).exists(),'Reviewed actual natural closure required before I/O'
 assert (TERMINAL['result_sha256'] is None)!=(TERMINAL['error_sha256'] is None)
 assert sha('cross_u_recycled_trace_target_rate_response_v001.py')==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA
 receipt=STEM+('_ERROR_RECEIPT.json' if TERMINAL['error_sha256'] is not None and path(STEM+'_ERROR_RECEIPT.json').exists() else '_RECEIPT.json');rc=js(receipt,TERMINAL['receipt_sha256']);closed=rc['status']=='CLOSED';assert rc['status'] in ('CLOSED','CLOSED_ERROR')
 r=js(STEM+('_RESULT.json' if closed else '_ERROR.json'),TERMINAL['result_sha256'] if closed else TERMINAL['error_sha256']);assert rc.get('result_sha256')==TERMINAL['result_sha256'] and rc.get('error_sha256')==TERMINAL['error_sha256'] and rc['owner']==r['owner'] and r['owner']['pid']==TERMINAL['pid'] and r['owner']['source_sha256']==SOURCE_SHA
 assert r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values());records=r['checkpoints'];controls=r['controls'];assert len({q['file'] for q in records})==len(records)
 assert {p.name for p in BASE.glob(STEM+'_*.npz')}=={q['file'] for q in records} and {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={q['commit_file'] for q in records}
 for q in records:
  for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert rc['output_sha256'][n]==h and sha(n)==h,n
  assert js(q['commit_file'],q['commit_sha256'])=={k:q[k] for k in ('file','sha256','metadata')} and q['metadata']['owner']==r['owner'] and q['metadata']['qualification']==r['qualification']
  if closed:assert not q['metadata']['failed'] and all(v['finite'] for v in q['metadata']['schema'].values())
 assert [c['ordinal'] for c in controls]==list(range(len(controls))) and len(controls)<=6 and all(c['tolerance']==TOL and math.isfinite(c['error']) and c['passed']==(c['error']<=TOL) for c in controls)
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
  raw=js(q['commit_file'],q['commit_sha256']);assert raw['file']==q['file'] and raw['sha256']==q['sha256'] and (q.get('metadata') is None or raw['metadata']==q['metadata']);return dict(raw,commit_file=q['commit_file'],commit_sha256=q['commit_sha256'])
 def pair(a,n):return a[n+'_hi'],a[n+'_lo']
 def total(p):return p[0]+p[1]
 def identity(label,terms,envelope=None):
  values=[sign*x for sign,p in terms for x in p];gap=np.add.reduce(values);bound=np.add.reduce([abs(x) for x in values]) if envelope is None else envelope;assert gap.shape==bound.shape and np.all(bound>=0)
  error=float(np.max(abs(gap)/np.maximum(bound,1e-30),initial=0));assert error<=TOL,(label,error);identities.append(dict(name=label,error=error))
 for c in controls:
  prefix='control_%03d_%s_'%(c['ordinal'],c['name']);names=tuple(prefix+n for n in ('actual','expected','envelope'));hits=[q for q in records if all(n in q['metadata']['schema'] for n in names)];assert hits,c;a=read(hits[0],names)
  for q in hits[1:]:
   b=read(q,names);assert all(np.array_equal(a[n],b[n]) for n in names)
  actual,expected,envelope=(a[n] for n in names);assert np.all(envelope>=0);error=float(np.max(abs(actual-expected)/np.maximum(envelope,1e-30),initial=0));assert error==c['error'];identities.append(dict(name=c['name']+'_saved_triplet',error=error))
 if not closed:report=dict(status='SAVED_RECYCLED_TRACE_FAILURE_PRESERVED',controls=len(controls),committed_pairs=len(records),context=r.get('context'),canonical_response_qualified=False)
 else:
  inp,fixture,coarse,response,jets,ro=(r[n] for n in ('input','fixture','coarse','response','NEW_rate_jets','readout'));cols=r['NEW_columns'];roles=[inp,fixture,coarse,response,jets,ro]+cols;assert len(cols)==4 and len(roles)==10 and all(q in records for q in roles) and len(controls)==6 and all(c['passed'] for c in controls)
  snaps=[q for q in records if q not in roles];assert len(snaps)<=4 and len({q['metadata']['iteration'] for q in snaps})==len(snaps) and all(q['metadata']['kind']=='unqualified_restart_snapshot_signed_MINRES_iterate' and q['metadata']['stage']=='recycled_trace_warm' and q['metadata']['iteration'] in (40,80,120,160) for q in snaps)
  im,cm,rm,lm=inp['metadata'],coarse['metadata'],response['metadata'],ro['metadata'];assert im['kind']=='cached_trace_response_with_four_fixed_snapshot_differences' and cm['kind']=='four_predeclared_snapshot_differences_and_absolute_symmetrized_congruence_only' and rm['kind']=='one_NEW_recycled_correction_to_authenticated_nonadmitted_trace_seed' and lm['kind']=='saved_old_literal_plus_only_NEW_exact_increment'
  assert fixture['metadata']['controls']==controls[:4] and cm['controls']==controls[4:5] and rm['controls']==controls[5:6] and im['parent_terminal']==r['parent_terminal']==ORIGINAL_TERMINAL and im['parent_canonical_response_admitted'] is False and r['parent_original_nonadmission_preserved'] and r['original_six_gates_unchanged']
  assert r['cap']==im['cap']==rm['cap']==rm['solver']['cap']==160 and r['new_cycles']==im['new_cycles']==rm['new_cycles']==rm['solver']['new_cycles']==1 and lm['zero_native_RHS_relative_ratio'] is None and im['physical_ports'] is None and lm['physical_ports'] is None
  assert all(r[n] is False for n in ('physical_operator_or_RHS_changed','finite_configuration_prepared','physical_adoption')) and all(cm[n] is False for n in ('physical_action_or_RHS_changed','directions_dropped','jitter_clipping_or_tolerance_relaxation')) and all(lm[n] is False for n in ('primitive_stationarity_mismatch_resolved','configuration_changed')) and cm['H_asymmetry_preserved']
  for n,h in ((ORIGINAL_PROOF,ORIGINAL_PROOF_SHA),('CROSS_U_INITIAL_YORK_TRACE_TARGET_RATE_RESPONSE_V001_RESULT.json',ORIGINAL_TERMINAL['result_sha256']),('CROSS_U_INITIAL_YORK_TRACE_TARGET_RATE_RESPONSE_V001_RECEIPT.json',ORIGINAL_TERMINAL['receipt_sha256'])):assert rc['input_sha256'][str(path(n).resolve())]==h
  old=js('CROSS_U_INITIAL_YORK_TRACE_TARGET_RATE_RESPONSE_V001_RESULT.json',ORIGINAL_TERMINAL['result_sha256']);proof=js(ORIGINAL_PROOF,ORIGINAL_PROOF_SHA);assert old['status']=='NEW_LITERAL_TRACE_TARGET_RESPONSE_NOT_ADMITTED' and old['literal_original_response_admitted'] is False and old['old_frozen_inverse_numerically_admitted'] is False and proof['parent']==dict(ORIGINAL_TERMINAL,error_sha256=None) and proof['status']=='SAVED_INITIAL_YORK_TRACE_TARGET_RESPONSE_CLOSURE_PASS' and im['parent_controls']==old['controls']
  old_input=parent(im['parent_input']);old_approx=parent(im['parent_approximation']);old_literal=parent(im['parent_readout']);assert thin(old_input)==thin(old['input']) and thin(old_approx)==thin(old['numerical_approximation']) and thin(old_literal)==thin(old['readout'])
  ia=read(inp,('NEW_t_target_RHS_hi','NEW_t_target_RHS_lo','inherited_original_native_affine_reference','inherited_original_native_canonical_reference','original_basis_native_scale','original_basis_metric_scale'));orig=read(old_input,tuple(ia));assert all(np.array_equal(ia[n],orig[n]) for n in ia);rhs=pair(ia,'NEW_t_target_RHS')
  nm=np.ones((33,3,87,45),bool);nm[:,:,0]=False;nm[:,1,:,0]=False;mm=np.ones((6,87,45),bool);mm[:,0]=False;mm[3:5,:,0]=False;assert int(np.sum(nm))==380292 and int(np.sum(mm))==23048
  ns=ia['original_basis_native_scale'][nm];ms=ia['original_basis_metric_scale'][mm];nref=ia['inherited_original_native_affine_reference'][nm];cref=ia['inherited_original_native_canonical_reference'][nm];mref=total(rhs)[380292:];assert np.all(ns>0) and np.all(ms>0) and np.linalg.norm(mref)>0 and np.all(rhs[0][:380292]==0) and np.all(rhs[1][:380292]==0)
  def scores(label,res,stored,metadata):
   v=total(res);rows=[];absolute=[]
   for x,ref,s in ((v[:380292],nref,ns),(v[:380292],cref,ns),(v[380292:],mref,ms)):
    a=float(np.linalg.norm(x));b=float(np.linalg.norm(x/s));c=float(np.linalg.norm(ref));d=float(np.linalg.norm(ref/s));assert c>0 and d>0;rows.append((a/c,b/d));absolute.append((a,b,c,d,ROW_TOL*c,ROW_TOL*d))
   rows=np.asarray(rows);assert rows.shape==stored.shape==(3,2) and np.allclose(rows,stored,rtol=TOL,atol=1e-300) and np.array_equal(stored,np.asarray(metadata)),label
   return bool(np.all(rows<=ROW_TOL)),np.asarray(absolute)
  ca=read(coarse,tuple('recycled_trace_preconditioner_'+n for n in ('independence_eigenvalues','independence_resolved_error_budget','projected_eigenvalues','projected_resolved_error_budget')));wg=ca['recycled_trace_preconditioner_independence_eigenvalues'];wh=ca['recycled_trace_preconditioner_projected_eigenvalues'];ge=float(ca['recycled_trace_preconditioner_independence_resolved_error_budget']);he=float(ca['recycled_trace_preconditioner_projected_resolved_error_budget']);assert wg.shape==wh.shape==(4,) and ge>=0 and he>=0 and float(np.min(wg))-ge==cm['independence_margin']>0 and float(np.min(abs(wh)))-he==cm['projected_spectral_margin']>0
  for k in (40,80,120,160):
   snap=parent(im['snapshot_refs'][str(k)]);assert snap['metadata']['iteration']==k;sa=read(snap,('NEW_trace_target_frozen_approximate_inverse_original_iterate',));copy=read(inp,('saved_original_iterate_%d'%k,));assert np.array_equal(sa['NEW_trace_target_frozen_approximate_inverse_original_iterate'],copy['saved_original_iterate_%d'%k])
  bases=('final_paired_response','unchanged_original_RHS','final_frozen_action','final_frozen_residual','exact_NEW_literal_increment','recycled_trace_warm_before_nodes','recycled_trace_warm_before_action','recycled_trace_warm_before_residual','recycled_trace_warm_NEW_correction_action','recycled_trace_warm_NEW_compression_action','recycled_trace_warm_original_residual_update_gap');up='recycled_trace_warm_final_update'
  a=read(response,tuple(n+'_'+w for n in bases for w in ('hi','lo'))+tuple(up+n for n in ('_old_nodes_hi','_old_nodes_lo','_float_correction','_updated_nodes_hi','_updated_nodes_lo','_exact_update_minus_two_word_nodes'))+('final_frozen_original_six_scores','recycled_trace_warm_uncancelled_update_bound'))
  source_names=tuple(n+'_'+w for n in ('NEW_trace_target_final_update_updated_nodes','NEW_trace_target_final_frozen_action','NEW_trace_target_final_frozen_residual') for w in ('hi','lo'));oa=read(old_approx,source_names)
  for new,prior in (('recycled_trace_warm_before_nodes','NEW_trace_target_final_update_updated_nodes'),('recycled_trace_warm_before_action','NEW_trace_target_final_frozen_action'),('recycled_trace_warm_before_residual','NEW_trace_target_final_frozen_residual')):assert all(np.array_equal(pair(a,new)[w],pair(oa,prior)[w]) for w in (0,1))
  assert all(np.array_equal(pair(a,'unchanged_original_RHS')[w],rhs[w]) and np.array_equal(pair(a,'final_paired_response')[w],pair(a,up+'_updated_nodes')[w]) and np.array_equal(pair(a,'recycled_trace_warm_before_nodes')[w],pair(a,up+'_old_nodes')[w]) for w in (0,1))
  words=[a[up+n] for n in ('_old_nodes_hi','_old_nodes_lo','_float_correction','_updated_nodes_hi','_updated_nodes_lo','_exact_update_minus_two_word_nodes')];assert all(x.shape==(403340,) for x in words) and all(math.fsum((x[0],x[1],x[2],-x[3],-x[4],-x[5]))==0 for x in zip(*words));identities.append(dict(name='exact_saved_old_pair_plus_delta_equals_new_pair_plus_q',error=0.))
  inc=pair(a,'exact_NEW_literal_increment');assert all(math.fsum((x[0],x[1],-x[2],x[3]))==0 for x in zip(inc[0],inc[1],words[2],words[5]));identities.append(dict(name='exact_saved_NEW_literal_increment_equals_delta_minus_q',error=0.))
  frozen=pair(a,'final_frozen_action');fres=pair(a,'final_frozen_residual');env=a['recycled_trace_warm_uncancelled_update_bound'];identity('frozen_rhs_action_residual',[(1,rhs),(-1,frozen),(-1,fres)]);identity('original_update_stored_gap',[(1,fres),(-1,pair(a,'recycled_trace_warm_before_residual')),(1,pair(a,'recycled_trace_warm_NEW_correction_action')),(-1,pair(a,'recycled_trace_warm_NEW_compression_action')),(-1,pair(a,'recycled_trace_warm_original_residual_update_gap'))],env)
  fok,fnorm=scores('frozen',fres,a['final_frozen_original_six_scores'],rm['solver']['original_six_scores']);assert fok==r['frozen_original_response_admitted']==rm['frozen_original_rows_admitted']
  assert jets['metadata']['kind']=='only_NEW_exact_increment_paired_E_F_value_R_Z' and lm['NEW_rate_jets']==thin(jets) and lm['NEW_rate_columns']==[thin(q) for q in cols] and lm['old_literal_ref']==thin(old_literal) and lm['prior_signed_primitive_readout']==im['prior_signed_primitive_readout']
  ja=read(jets,tuple('NEW_exact_increment_'+n+'_'+w for n in ('native_value','metric_value') for w in ('hi','lo')))
  for iq,q in enumerate(cols):
   md=q['metadata'];assert md['kind']=='only_NEW_delta_minus_q_literal_rate_derivative' and md['column']==iq and md['pilot_ref']==im['pilot_columns'][iq] and md['affine_constant_derivative_zero'] and md['configuration_unchanged'] and md['old_primal_or_full_response_replayed'] is False and md['original_primitive_stationarity_mismatch_resolved'] is False
   local=read(q,tuple('NEW_exact_increment_local_'+n+'_'+w for n in ('native_value','physical_metric_value') for w in ('hi','lo')));sl=slice(iq*3784,(iq+1)*3784)
   for w in (0,1):assert np.array_equal(pair(local,'NEW_exact_increment_local_native_value')[w],pair(ja,'NEW_exact_increment_native_value')[w][:,sl].transpose(1,0,2).reshape(3784,99)) and np.array_equal(pair(local,'NEW_exact_increment_local_physical_metric_value')[w],pair(ja,'NEW_exact_increment_metric_value')[w][sl])
   for family,names in (('NEW_increment_first_jet',('du','dz','dg','Ga')),('NEW_increment_feature',('nu','nz','V','D','F','Fup','a','Pi','PiU')),('NEW_increment_momentum',('native_density','metric_total_density','K','Ktrace','metric_EH_tensor','connection_momentum'))):assert all(family+'_'+n+'_'+w in md['schema'] for n in names for w in ('hi','lo'))
  lb='recycled_trace_literal_translation';rbases=('NEW_increment_literal_full_action',lb+'_old_saved_literal_action',lb+'_NEW_increment_literal_action',lb+'_new_literal_action',lb+'_new_literal_residual',lb+'_literal_minus_frozen_derivative');ra=read(ro,tuple(n+'_'+w for n in rbases for w in ('hi','lo'))+(lb+'_literal_original_scores',lb+'_literal_addition_defect_exact_expansion'));ol=read(old_literal,tuple('complete_rate_direction_literal_full_action_'+w for w in ('hi','lo')))
  oldaction=pair(ra,lb+'_old_saved_literal_action');newaction=pair(ra,lb+'_NEW_increment_literal_action');literal=pair(ra,lb+'_new_literal_action');lres=pair(ra,lb+'_new_literal_residual');assert all(np.array_equal(oldaction[w],pair(ol,'complete_rate_direction_literal_full_action')[w]) and np.array_equal(newaction[w],pair(ra,'NEW_increment_literal_full_action')[w]) for w in (0,1))
  expansion=ra[lb+'_literal_addition_defect_exact_expansion'];assert expansion.shape==(6,403340);supplied=(oldaction[0],oldaction[1],newaction[0],newaction[1],-literal[0],-literal[1]);assert all(math.fsum(x)==math.fsum(y) for x,y in zip(zip(*supplied),zip(*expansion)));identities.append(dict(name='literal_translation_six_saved_words_equals_retained_expansion',error=0.))
  identity('literal_rhs_action_residual',[(1,rhs),(-1,literal),(-1,lres)]);identity('literal_minus_frozen_stored_bridge',[(1,literal),(-1,frozen),(-1,pair(ra,lb+'_literal_minus_frozen_derivative'))])
  lok,lnorm=scores('literal',lres,ra[lb+'_literal_original_scores'],lm['literal_original_six_scores']);assert lok==r['literal_original_response_admitted']==lm['literal_original_response_admitted'] and r['status']==('RECYCLED_LITERAL_TRACE_RESPONSE_ADMITTED' if fok and lok else 'RECYCLED_LITERAL_TRACE_RESPONSE_NOT_ADMITTED')
  report=dict(status='SAVED_RECYCLED_TRACE_RESPONSE_CLOSURE_PASS',producer_status=r['status'],controls=6,committed_pairs=len(records),iteration_snapshots=len(snaps),original71394_nonadmission_preserved=True,frozen_original_response_admitted=fok,literal_original_response_admitted=lok,zero_native_RHS_relative_ratio=None,frozen_absolute_residual_reference_thresholds=fnorm.tolist(),literal_absolute_residual_reference_thresholds=lnorm.tolist(),NEW_increment_columns_complete=4,old_literal_plus_only_NEW_delta_minus_q_verified_from_saved_words=True,original_primitive_stationarity_mismatch_resolved=False)
 report.update(owner_pid=os.getpid(),parent=TERMINAL,selected=selected,identities=identities,original_row_tolerance=ROW_TOL,arithmetic_tolerance=TOL,producer_coarse_eigen_Gram_action_operator_affine_features_momenta_FE_MINRES_or_fixtures_replayed=False,physical_adoption=False,scope_limit='Stored controls, copies, finite resolved margins, arithmetic-word identities, reshapes and norms only. No normalized directions, Gram/H contractions, spectrum/factorization, E/F evaluation, momenta or weak scatter are reconstructed. Frozen/literal qualification stays separate; original nonadmission and finite primitive/port gaps remain.')
 for n,h in rc['output_sha256'].items():assert sha(n)==h
 assert sha(receipt)==TERMINAL['receipt_sha256'] and sha('cross_u_recycled_trace_target_rate_response_v001.py')==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA
 with path(OUT).open('x') as f:json.dump(report,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
 path(OUT).chmod(0o444);print(json.dumps(dict(status=report['status'],pid=os.getpid(),sha256=sha(OUT))),flush=True)
if __name__=='__main__':main()

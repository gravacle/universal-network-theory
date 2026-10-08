"""Guard-held saved t response words/norms; no producer or scientific replay."""
from pathlib import Path
import hashlib,json,math,os
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_INITIAL_YORK_TRACE_TARGET_RATE_RESPONSE_V001'
OUT='READONLY_INITIAL_YORK_TRACE_TARGET_RESPONSE_CLOSURE_V001_RESULT.json'
AUTHOR_DRAFT=False
SOURCE_SHA='23cbba6893b934236c8fff2c8ff4dda63f6808f589a04f701dcd536fdd31de27'
PROTOCOL_SHA='793cc56c47dabc8a7baa7838b57fd95b658d655242a71e112d0d64b932ba44f7'
TERMINAL={'pid': 71394, 'result_sha256': '6041c495ea6d837840d6f4bde687ba3dcf604131087c2ed7b395ae67fe284bb6', 'receipt_sha256': '1aee74e2996755c644e242e78ecb488f2bc334dc63aa6568a5d3309f4c8235a3', 'error_sha256': None}
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
 assert AUTHOR_DRAFT is False and TERMINAL['pid'] is not None and TERMINAL['receipt_sha256'] is not None and not path(OUT).exists()
 assert (TERMINAL['result_sha256'] is None)!=(TERMINAL['error_sha256'] is None)
 assert sha('cross_u_initial_york_trace_target_rate_response_v001.py')==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA
 receipt=STEM+('_ERROR_RECEIPT.json' if TERMINAL['error_sha256'] is not None and path(STEM+'_ERROR_RECEIPT.json').exists() else '_RECEIPT.json');rc=js(receipt,TERMINAL['receipt_sha256']);closed=rc['status']=='CLOSED';assert rc['status'] in ('CLOSED','CLOSED_ERROR')
 r=js(STEM+('_RESULT.json' if closed else '_ERROR.json'),TERMINAL['result_sha256'] if closed else TERMINAL['error_sha256']);assert rc.get('result_sha256')==TERMINAL['result_sha256'] and rc.get('error_sha256')==TERMINAL['error_sha256'] and rc['owner']==r['owner'] and r['owner']['pid']==TERMINAL['pid'] and r['owner']['source_sha256']==SOURCE_SHA
 assert r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values());records=r['checkpoints'];controls=r['controls'];assert len({q['file'] for q in records})==len(records)
 assert {p.name for p in BASE.glob(STEM+'_*.npz')}=={q['file'] for q in records} and {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={q['commit_file'] for q in records}
 for q in records:
  for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert rc['output_sha256'][n]==h and sha(n)==h,n
  assert js(q['commit_file'],q['commit_sha256'])=={k:q[k] for k in ('file','sha256','metadata')} and q['metadata']['owner']==r['owner'] and q['metadata']['qualification']==r['qualification']
  if closed:assert not q['metadata']['failed'] and all(v['finite'] for v in q['metadata']['schema'].values())
 assert [c['ordinal'] for c in controls]==list(range(len(controls))) and len(controls)<=3 and all(c['tolerance']==TOL and math.isfinite(c['error']) and c['passed']==(c['error']<=TOL) for c in controls)
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
  raw=js(q['commit_file'],q['commit_sha256']);assert raw['file']==q['file'] and raw['sha256']==q['sha256'] and (q.get('metadata') is None or q['metadata']==raw['metadata']);return dict(raw,commit_file=q['commit_file'],commit_sha256=q['commit_sha256'])
 def pair(a,n):return a[n+'_hi'],a[n+'_lo']
 def total(p):return p[0]+p[1]
 def identity(label,terms,envelope=None):
  v=[sign*x for sign,p in terms for x in p];gap=np.add.reduce(v);bound=np.add.reduce([abs(x) for x in v]) if envelope is None else envelope;assert gap.shape==bound.shape and np.all(bound>=0)
  e=float(np.max(abs(gap)/np.maximum(bound,1e-30),initial=0));assert e<=TOL,(label,e);identities.append(dict(name=label,error=e))
 nm=np.ones((33,3,87,45),bool);nm[:,:,0]=False;nm[:,1,:,0]=False;mm=np.ones((6,87,45),bool);mm[:,0]=False;mm[3:5,:,0]=False;assert int(np.sum(nm))==380292 and int(np.sum(mm))==23048
 def fields(x):
  assert x.shape==(403340,);n=np.zeros(nm.shape);m=np.zeros(mm.shape);n[nm]=x[:380292];m[mm]=x[380292:];return n,m
 def norms(label,res,nref,cref,mref,ns,ms,stored,metadata):
  v=fields(total(res));rows=[];absolute=[]
  for x,ref,scale in ((v[0],nref,ns),(v[0],cref,ns),(v[1],mref,ms)):
   raw=float(np.linalg.norm(x));white=float(np.linalg.norm(x/scale));den=float(np.linalg.norm(ref));wd=float(np.linalg.norm(ref/scale));assert (den>0)==(wd>0);absolute.append((raw,white,den,wd,ROW_TOL*den,ROW_TOL*wd));rows.append((raw/den,white/wd) if den>0 else ((0.,0.) if raw==white==0 else (1.,1.)))
  rows=np.asarray(rows);assert rows.shape==stored.shape==(3,2) and np.allclose(rows,stored,rtol=TOL,atol=1e-300) and np.array_equal(stored,np.asarray(metadata['scores'])) and np.allclose(absolute,metadata['absolute'],rtol=TOL,atol=1e-300),label
  return bool(np.all(rows<=ROW_TOL)),np.asarray(absolute)
 for c in controls:
  prefix='control_%03d_%s_'%(c['ordinal'],c['name']);names=tuple(prefix+n for n in ('actual','expected','envelope'));found=[q for q in records if all(n in q['metadata']['schema'] for n in names)];assert found,c;a=read(found[0],names)
  for q in found[1:]:
   b=read(q,names);assert all(np.array_equal(a[n],b[n]) for n in names)
  x,y,e=(a[n] for n in names);assert np.all(e>=0);error=float(np.max(abs(x-y)/np.maximum(e,1e-30),initial=0));assert error==c['error'];identities.append(dict(name=c['name']+'_stored_triplet',error=error))
 if not closed:report=dict(status='SAVED_TRACE_TARGET_RESPONSE_FAILURE_PRESERVED',controls=controls,committed_pairs=len(records),context=r.get('context'))
 else:
  inp,fix,ap,jets,ro=(r[n] for n in ('input','fixture','numerical_approximation','rate_jets','readout'));cols=r['columns'];assert len(cols)==4 and all(q in records for q in [inp,fix,ap,jets,ro]+cols) and len(controls)==3 and all(c['passed'] for c in controls)
  assert [q['metadata']['kind'] for q in (inp,fix,ap,jets,ro)]==['NEW_compact_total_trace_target_RHS_and_immutable_numerical_preconditioner','fresh_signed_coupled_zero_native_RHS_control','NEW_target_frozen_signed_numerical_approximate_inverse','NEW_target_response_genuine_paired_E_F_value_R_Z','NEW_current_literal_target_response_and_frozen_preconditioner_remainder']
  assert fix['metadata']['controls']==controls[:1] and ap['metadata']['controls']==controls[1:2] and ro['metadata']['controls']==controls[2:3] and r['zero_native_RHS_relative_ratio'] is None and ro['metadata']['zero_native_RHS_relative_ratio'] is None
  assert all(r[n] is False for n in ('frozen_operator_is_physical_action','original_primitive_stationarity_mismatch_resolved','whole_grid_five_field_preparation','physical_adoption')) and ro['metadata']['uncancelled_backward_error_is_an_admission_route'] is False
  im=inp['metadata'];assert im['cap']==160 and im['cycles']==1 and im['NEW_native_target_exactly_zero'] and im['native_conservative_reference_choice_fixed_before_solve'] and im['zero_source_relative_ratio'] is None
  ti=parent(im['target_ref']);ni=parent(im['native_reference_ref']);basis=im['frozen_system_refs']['basis'];assert jets['metadata']['basis_ref']==basis and jets['metadata']['frozen_operator_ref']==im['frozen_system_refs'] and ro['metadata']['prior_signed_primitive_readout']==im['prior_signed_primitive_readout']
  ia=read(inp,('NEW_t_target_RHS_hi','NEW_t_target_RHS_lo','inherited_original_native_affine_reference','inherited_original_native_canonical_reference','original_basis_native_scale','original_basis_metric_scale'));rhs=pair(ia,'NEW_t_target_RHS');nref=ia['inherited_original_native_affine_reference'];cref=ia['inherited_original_native_canonical_reference'];ns=ia['original_basis_native_scale'];ms=ia['original_basis_metric_scale'];assert np.all(ns>0) and np.all(ms>0)
  target=read(ti,tuple(n+'_'+w for n in ('t_full_coupled_target_RHS','t_weak_metric_target') for w in ('hi','lo')));native=read(ni,('original_rhs','current_Pn'));assert np.array_equal(nref,fields(native['original_rhs'])[0]) and np.array_equal(cref,native['current_Pn'])
  for w,suffix in enumerate(('hi','lo')):assert np.array_equal(rhs[w],target['t_full_coupled_target_RHS_'+suffix]) and np.all(fields(rhs[w])[0]==0) and np.array_equal(fields(rhs[w])[1],target['t_weak_metric_target_'+suffix])
  mref=fields(total(rhs))[1];assert np.linalg.norm(mref)>0
  up='NEW_trace_target_final_update';bases=('NEW_rhs','frozen_approximation_action','frozen_original_residual','NEW_trace_target_completed_correction_action','NEW_trace_target_third_word_action','NEW_trace_target_shift_prediction','NEW_trace_target_shift_identity_gap','NEW_trace_target_recurrence_rhs_rounding_defect')
  anames=tuple(n+'_'+w for n in bases for w in ('hi','lo'))+tuple(up+n for n in ('_old_nodes_hi','_old_nodes_lo','_float_correction','_updated_nodes_hi','_updated_nodes_lo','_exact_update_minus_two_word_nodes'))+('NEW_trace_target_final_frozen_original_admission_scores','NEW_trace_target_update_envelope_through_third_word','NEW_trace_target_recurrence_rhs_rounded_value')+tuple(n+'_'+w for n in ('native_rate_response','metric_rate_response') for w in ('hi','lo'));a=read(ap,anames)
  assert all(np.array_equal(pair(a,'NEW_rhs')[w],rhs[w]) for w in (0,1));words=[a[up+n] for n in ('_old_nodes_hi','_old_nodes_lo','_float_correction','_updated_nodes_hi','_updated_nodes_lo','_exact_update_minus_two_word_nodes')];assert np.all(words[0]==0) and np.all(words[1]==0) and all(math.fsum((v[0],v[1],v[2],-v[3],-v[4],-v[5]))==0 for v in zip(*words));identities.append(dict(name='exact_zero_start_plus_delta_equals_updated_plus_q',error=0.))
  for w in (0,1):assert np.array_equal(fields(pair(a,up+'_updated_nodes')[w])[0],pair(a,'native_rate_response')[w]) and np.array_equal(fields(pair(a,up+'_updated_nodes')[w])[1],pair(a,'metric_rate_response')[w])
  frozen=pair(a,'frozen_approximation_action');fres=pair(a,'frozen_original_residual');env=a['NEW_trace_target_update_envelope_through_third_word'];identity('frozen_rhs_action_residual',[(1,rhs),(-1,frozen),(-1,fres)]);identity('frozen_prediction_words',[(1,pair(a,'NEW_trace_target_shift_prediction')),(-1,rhs),(1,pair(a,'NEW_trace_target_completed_correction_action')),(-1,pair(a,'NEW_trace_target_third_word_action'))],env);identity('stored_frozen_update_gap',[(1,fres),(-1,pair(a,'NEW_trace_target_shift_prediction')),(-1,pair(a,'NEW_trace_target_shift_identity_gap'))],env)
  identity('recurrence_rhs_readout_defect',[(1,rhs),(-1,(a['NEW_trace_target_recurrence_rhs_rounded_value'],np.zeros(403340))),(-1,pair(a,'NEW_trace_target_recurrence_rhs_rounding_defect'))])
  fm=ap['metadata']['solver'];fok,fnorm=norms('frozen',fres,nref,cref,mref,ns,ms,a['NEW_trace_target_final_frozen_original_admission_scores'],dict(scores=ap['metadata']['frozen_original_scores'],absolute=fm['absolute_residual_reference_thresholds']));assert fok==r['old_frozen_inverse_numerically_admitted'] and fm['cap']==160 and fm['cycles']==1 and fm['frozen_action_is_numerical_approximation_only'] is True
  for q in cols:assert q['metadata']['kind']=='NEW_literal_complete_and_uncancelled_block_temporal_derivatives' and q['metadata']['configuration_unchanged'] and q['metadata']['affine_constant_derivative_zero'] and q['metadata']['original_primitive_mismatch_resolved'] is False
  assert [q['metadata']['column'] for q in cols]==list(range(4)) and [q['metadata']['pilot_ref'] for q in cols]==im['pilot_columns'] and ro['metadata']['columns']==[thin(q) for q in cols] and ro['metadata']['rate_jets']==thin(jets)
  for family,shape in (('NEW_native_rate',(33,15136,3)),('NEW_metric_rate',(15136,6))):
   for jet in ('value','R','Z'):
    for w in ('hi','lo'):assert jets['metadata']['schema'][family+'_'+jet+'_'+w]==dict(shape=list(shape),dtype='float64',finite=True)
  ja=read(jets,tuple(n+'_'+w for n in ('NEW_native_rate_value','NEW_metric_rate_value') for w in ('hi','lo')))
  for iq,q in enumerate(cols):
   sl=slice(iq*3784,(iq+1)*3784);ca=read(q,tuple(n+'_'+w for n in ('NEW_local_native_rate_values','NEW_local_physical_metric_rate_values','NEW_rate_momentum_native_density','NEW_rate_momentum_metric_total_density','complete_rate_direction_native_density','complete_rate_direction_metric_total_density') for w in ('hi','lo')))
   for w in (0,1):assert np.array_equal(pair(ca,'NEW_local_native_rate_values')[w],pair(ja,'NEW_native_rate_value')[w][:,sl].transpose(1,0,2).reshape(3784,99)) and np.array_equal(pair(ca,'NEW_local_physical_metric_rate_values')[w],pair(ja,'NEW_metric_rate_value')[w][sl]) and np.array_equal(pair(ca,'NEW_rate_momentum_native_density')[w],pair(ca,'complete_rate_direction_native_density')[w]) and np.array_equal(pair(ca,'NEW_rate_momentum_metric_total_density')[w],pair(ca,'complete_rate_direction_metric_total_density')[w])
   for n in ('du','dz','dg','Ga'):assert all('NEW_rate_first_jet_'+n+'_'+w in q['metadata']['schema'] for w in ('hi','lo'))
   for n in ('nu','nz','q','V','D','F','Fup','a','V_raised','D_raised','Pi','PiU'):assert all('NEW_rate_feature_'+n+'_'+w in q['metadata']['schema'] for w in ('hi','lo'))
   for n in ('K','Ktrace','metric_EH_tensor','metric_total_density','native_density','connection_momentum'):assert all('NEW_rate_momentum_'+n+'_'+w in q['metadata']['schema'] for w in ('hi','lo'))
  rbases=('complete_rate_direction_literal_full_action','NEW_current_literal_residual','NEW_literal_minus_frozen_derivative_remainder','NEW_literal_residual_prediction','NEW_literal_residual_bookkeeping_gap');ra=read(ro,tuple(n+'_'+w for n in rbases for w in ('hi','lo'))+('NEW_current_literal_original_admission_scores',));literal=pair(ra,rbases[0]);lres=pair(ra,rbases[1]);bridge=pair(ra,rbases[2]);identity('literal_rhs_action_residual',[(1,rhs),(-1,literal),(-1,lres)]);identity('literal_minus_frozen_derivative',[(1,literal),(-1,frozen),(-1,bridge)]);identity('literal_residual_prediction',[(1,pair(ra,rbases[3])),(-1,fres),(1,bridge)]);identity('literal_bookkeeping_saved_gap',[(1,lres),(-1,pair(ra,rbases[3])),(-1,pair(ra,rbases[4]))])
  admitted,lnorm=norms('literal',lres,nref,cref,mref,ns,ms,ra['NEW_current_literal_original_admission_scores'],dict(scores=ro['metadata']['literal_original_reference_scores'],absolute=ro['metadata']['absolute_residual_reference_thresholds']));assert admitted==r['literal_original_response_admitted']==ro['metadata']['literal_original_response_admitted'] and np.array_equal(ra['NEW_current_literal_original_admission_scores'],np.asarray(r['literal_original_scores']))
  expected='NEW_LITERAL_TRACE_TARGET_RESPONSE_ADMITTED' if admitted else 'NEW_LITERAL_TRACE_TARGET_RESPONSE_NOT_ADMITTED';assert r['status']==expected;roles=[inp,fix,ap,jets,ro]+cols;snaps=[q for q in records if q not in roles];assert len(snaps)<=4 and all(q['metadata']['kind']=='unqualified_restart_snapshot_signed_MINRES_iterate' and q['metadata']['iteration'] in (40,80,120,160) for q in snaps)
  report=dict(status='SAVED_INITIAL_YORK_TRACE_TARGET_RESPONSE_CLOSURE_PASS',producer_status=r['status'],controls=3,committed_pairs=len(records),literal_original_response_admitted=admitted,frozen_numerical_inverse_admitted=fok,literal_reference_scores=r['literal_original_scores'],literal_absolute_residual_reference_thresholds=lnorm.tolist(),frozen_absolute_residual_reference_thresholds=fnorm.tolist(),zero_native_RHS_relative_ratio=None,rate_columns_complete=4,original_primitive_stationarity_mismatch_resolved=False,iteration_snapshots=len(snaps))
 report.update(owner_pid=os.getpid(),parent=TERMINAL,selected=selected,identities=identities,original_row_tolerance=ROW_TOL,arithmetic_tolerance=TOL,old_maps_inverse_MINRES_affine66_81_momenta_scatter_or_fixtures_replayed=False,physical_adoption=False,scope_limit='Saved copies, packing/reshape ties, triplets and norms only; E/F jets, point momenta and weak scatter are not reconstructed. Frozen and literal qualification remain separate; zero native RHS relative ratio is undefined.')
 for n,h in rc['output_sha256'].items():assert sha(n)==h
 assert sha(receipt)==TERMINAL['receipt_sha256'] and sha('cross_u_initial_york_trace_target_rate_response_v001.py')==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA
 with path(OUT).open('x') as f:json.dump(report,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
 path(OUT).chmod(0o444);print(json.dumps(dict(status=report['status'],pid=os.getpid(),sha256=sha(OUT))),flush=True)
if __name__=='__main__':main()

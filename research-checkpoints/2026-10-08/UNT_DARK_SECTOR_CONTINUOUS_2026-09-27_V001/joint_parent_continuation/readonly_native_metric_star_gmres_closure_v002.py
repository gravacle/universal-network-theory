"""Held saved-only coupled STAR-GMRES closure; no solver/operator/rate replay."""
from pathlib import Path
import ast,hashlib,json,math,os,struct,zipfile
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_NATIVE_METRIC_STAR_PAIRED_TRACE_GMRES_V002'
SOURCE='cross_u_native_metric_star_paired_trace_gmres_v002.py'
SOURCE_SHA='091a6d1303bf8c75160a0472af6e88688b89be4e6ba6b770310b280125350871'
PROTOCOL_SHA='976ef7b27f08731576217a89c45035322182adf3ea00bcbb44b40f5062afbe09'
OUT='READONLY_NATIVE_METRIC_STAR_GMRES_CLOSURE_V002_RESULT.json'
AUTHOR_DRAFT=True
TERMINAL=dict(pid=None,result_sha256=None,receipt_sha256=None,error_sha256=None)
TOL=2e-11;ROW_TOL=1e-10
LATEST=dict(pid=75215,result_sha256='4fa6fe13c1a32163cb9f867143389946eda19fc17e001834400346483417af0e',receipt_sha256='0a7a1c4b8c0d8f334b8404d41644955dd32e4305443b53c2125655d3c578e0cb',error_sha256=None)
FACTOR=dict(pid=81895,result_sha256='545294354b3af026eeb84422c7d2e710e57281ca29f884639a5c77f09c86f7c0',receipt_sha256='86b782cc94a3e15b88e3a126980fb9ee9f647a2a815af47b68be61111b45eddb',error_sha256=None)
FACTOR_PROOF='READONLY_SAVED_STAR_BALANCED_CLOSURE_V001_RESULT.json'
FACTOR_PROOF_SHA='d6e0196a2f04f1d7c6fa88d53de52d079565868833da68665a5cba05abcd41c3'

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
 assert AUTHOR_DRAFT is False and TERMINAL['pid'] is not None and TERMINAL['receipt_sha256'] is not None and not path(OUT).exists(),'Reviewed actual natural terminal binding required'
 assert (TERMINAL['result_sha256'] is None)!=(TERMINAL['error_sha256'] is None) and sha(SOURCE)==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA
 receipt=STEM+('_ERROR_RECEIPT.json' if TERMINAL['error_sha256'] is not None and path(STEM+'_ERROR_RECEIPT.json').exists() else '_RECEIPT.json');rc=js(receipt,TERMINAL['receipt_sha256']);closed=rc['status']=='CLOSED';assert rc['status'] in ('CLOSED','CLOSED_ERROR')
 r=js(STEM+('_RESULT.json' if closed else '_ERROR.json'),TERMINAL['result_sha256'] if closed else TERMINAL['error_sha256']);assert rc.get('result_sha256')==TERMINAL['result_sha256'] and rc.get('error_sha256')==TERMINAL['error_sha256'] and rc['owner']==r['owner'] and r['owner']['pid']==TERMINAL['pid'] and r['owner']['source_sha256']==SOURCE_SHA
 assert r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values());records=r['checkpoints'];controls=r['controls'];assert len({q['file'] for q in records})==len(records)
 assert {p.name for p in BASE.glob(STEM+'_*.npz')}=={q['file'] for q in records} and {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={q['commit_file'] for q in records}
 import numpy as np
 selected=[];identities=[];header_count=0
 def seal(q,output=True):
  for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):
   key=n if n in rc['input_sha256'] else str(path(n).resolve());assert (rc['output_sha256'][n] if output else rc['input_sha256'][key])==h and sha(n)==h,n
  cm=js(q['commit_file'],q['commit_sha256']);assert cm['file']==q['file'] and cm['sha256']==q['sha256'] and ('metadata' not in q or cm['metadata']==q['metadata']);return dict(cm,commit_file=q['commit_file'],commit_sha256=q['commit_sha256'])
 def headers(q):
  nonlocal header_count
  with zipfile.ZipFile(path(q['file'])) as z:
   assert set(z.namelist())=={n+'.npy' for n in q['metadata']['schema']}|{'metadata_json.npy'}
   for n,sc in q['metadata']['schema'].items():
    with z.open(n+'.npy') as f:
     assert f.read(6)==b'\x93NUMPY';v=f.read(2);assert v in (b'\x01\x00',b'\x02\x00',b'\x03\x00');length=struct.unpack('<H' if v[0]==1 else '<I',f.read(2 if v[0]==1 else 4))[0];h=ast.literal_eval(f.read(length).decode('utf8' if v[0]==3 else 'latin1'))
    assert list(h['shape'])==sc['shape'] and str(np.dtype(h['descr']))==sc['dtype'] and np.dtype(h['descr']).kind in 'fiub';header_count+=1
 def read(q,names):
  out={};sc=q['metadata']['schema']
  with np.load(path(q['file']),allow_pickle=False) as z:
   assert set(z.files)==set(sc)|{'metadata_json'} and json.loads(str(z['metadata_json']))==q['metadata']
   for n in names:
    x=z[n].copy();assert list(x.shape)==sc[n]['shape'] and str(x.dtype)==sc[n]['dtype'] and sc[n]['finite'] is True and np.all(np.isfinite(x)),n;out[n]=x
  selected.append(dict(file=q['file'],fields=len(names)));return out
 def pair(a,n):return a[n+'_hi'],a[n+'_lo']
 def identity(label,terms,envelope=None):
  words=[sign*x for sign,p in terms for x in p];gap=np.add.reduce(words);bound=np.add.reduce([abs(x) for x in words]) if envelope is None else envelope;assert gap.shape==bound.shape and np.all(bound>=0)
  error=float(np.max(abs(gap)/np.maximum(bound,1e-30),initial=0));assert error<=TOL,(label,error);identities.append(dict(name=label,error=error))
 def exact(label,words):
  assert all(x.shape==words[0].shape for x in words) and all(math.fsum(v)==0 for v in zip(*(x.ravel() for x in words))),label
  identities.append(dict(name=label,error=0.,exact_saved_addition=True))
 for q in records:
  seal(q);headers(q);assert q['metadata']['owner']==r['owner'] and q['metadata']['qualification']==r['qualification']
  if closed:assert q['metadata']['failed'] is False and all(v['finite'] is True for v in q['metadata']['schema'].values())
 assert [c['ordinal'] for c in controls]==list(range(len(controls))) and len(controls)<=11 and all(c['tolerance']==TOL and math.isfinite(c['error']) and c['passed']==(c['error']<=TOL) for c in controls)
 for c in controls:
  prefix='control_%03d_%s_'%(c['ordinal'],c['name']);names=tuple(prefix+n for n in ('actual','expected','envelope'));hits=[q for q in records if all(n in q['metadata']['schema'] for n in names)];assert hits,c;a=read(hits[0],names)
  for q in hits[1:]:
   b=read(q,names);assert all(np.array_equal(a[n],b[n]) for n in names)
  x,y,e=(a[n] for n in names);assert x.shape==y.shape==e.shape and np.all(e>=0);error=float(np.max(abs(x-y)/np.maximum(e,1e-30),initial=0));assert error==c['error'];identities.append(dict(name=c['name']+'_saved_triplet',error=error))
 input_records=[q for q in records if q['metadata'].get('kind')=='latest_nonadmitted_paired_trace_seed_and_earned_STAR_factor_only'];assert len(input_records)<=1
 ia=None;inp=input_records[0] if input_records else None
 if inp is not None:
  im=inp['metadata'];assert im['latest_terminal']==LATEST and im['factor_terminal']==FACTOR and im['all111_latest_INPUT_fields_bitcopied'] is True and im['shared76_fields_bitwise_equal'] is True and im['cap']==80 and im['restarts']==0 and im['checkpoints']==[20,40,80] and im['zero_native_RHS_relative_ratio'] is None and im['physical_adoption'] is False
  proof=js(FACTOR_PROOF,FACTOR_PROOF_SHA);assert rc['input_sha256'][str(path(FACTOR_PROOF).resolve())]==FACTOR_PROOF_SHA and proof['status']=='SAVED_COMPLETED_STAR_BALANCED_NORMWISE_CLOSURE_PASS' and proof['parent']==FACTOR and proof['original_componentwise_control_12_passed'] is False and proof['new_candidate_factor_certified'] is True and proof['physical_adoption'] is False
  latest_input,latest_response,latest_literal,factor_input,factor=(seal(im[n],False) for n in ('latest_input','latest_response','latest_literal_readout','factor_input','factor'));assert proof['factor_ref']==thin(factor) and im['factor_original_failed_control']['ordinal']==12 and im['factor_original_failed_control']['passed'] is False and len(im['factor_new_normwise_controls'])==2 and all(c['passed'] for c in im['factor_new_normwise_controls'])
  ia=read(inp,tuple(inp['metadata']['schema']));parents=((latest_input,''),(factor_input,'certified_STAR_input_'))
  originals={}
  for q,prefix in parents:
   a=read(q,tuple(q['metadata']['schema']));originals[prefix]=a
   for n,x in a.items():assert inp['metadata']['schema'][prefix+n]==q['metadata']['schema'][n] and np.array_equal(x,ia[prefix+n]),prefix+n
  assert len(originals[''])==111 and len(originals['certified_STAR_input_'])==88;shared=set(originals[''])&set(originals['certified_STAR_input_']);assert len(shared)==76 and all(np.array_equal(originals[''][n],originals['certified_STAR_input_'][n]) for n in shared)
  for q,prefix,names in ((latest_response,'latest_GMRES_seed_',tuple(n+'_'+w for n in ('final_paired_response','unchanged_original_RHS','final_frozen_action','final_frozen_residual') for w in ('hi','lo'))+('final_frozen_original_six_scores',)),(latest_literal,'latest_GMRES_literal_',tuple('recycled_trace_literal_translation_'+n+'_'+w for n in ('new_literal_action','new_literal_residual','literal_minus_frozen_derivative') for w in ('hi','lo'))+('recycled_trace_literal_translation_literal_addition_defect_exact_expansion','recycled_trace_literal_translation_literal_original_scores')),(factor,'certified_STAR_',tuple('NEW_star_preconditioner_'+n for n in ('L','V','D_factor','K_factor','D_symmetric','K_symmetric','C','S','basis_scale','native_mask','metric_mask')))):
   a=read(q,names)
   for n,x in a.items():assert np.array_equal(x,ia[prefix+n]),prefix+n
  assert np.all(ia['certified_STAR_NEW_star_preconditioner_basis_scale']>0);identities.append(dict(name='all_closed_latest_input_factor_seed_literal_copies',error=0.,latest_INPUT_fields=111,factor_INPUT_fields=88,shared_fields=76))
 if not closed:report=dict(status='SAVED_STAR_GMRES_FAILURE_PRESERVED',producer_terminal_status='CLOSED_ERROR',controls=len(controls),committed_pairs=len(records),context=r.get('context'),input_copies_checked=inp is not None,frozen_original_response_admitted=None,literal_original_response_admitted=None,canonical_response_qualified=False)
 else:
  assert ia is not None and inp==r['input'];fixture,cong,response,jets,ro=(r[n] for n in ('fixture','congruence','response','NEW_rate_jets','readout'));cols=r['NEW_columns'];snaps=r['iterations'];assert len(cols)==4 and len(snaps)<=3 and len(controls)>=7 and all(c['passed'] for c in controls) and all(q in records for q in (fixture,cong,response,jets,ro)+tuple(cols)+tuple(snaps))
  assert set(q['file'] for q in records)==set(q['file'] for q in (inp,fixture,cong,response,jets,ro)+tuple(cols)+tuple(snaps)) and fixture['metadata']['controls']==controls[:5] and cong['metadata']['controls']==controls[5:6] and response['metadata']['controls']==controls[6:]
  rm=response['metadata'];lm=ro['metadata'];solver=r['solver'];assert solver==rm['solver'] and solver['cap']==r['cap']==80 and solver['restarts']==r['restarts']==0 and solver['self_adjointness_assumed'] is False and 0<=solver['iterations']<=80 and solver['physical_adoption'] is False
  assert r['parent_terminal']==LATEST and r['factor_terminal']==FACTOR and r['original_six_gates_unchanged'] is True and r['finite_configuration_prepared'] is False and r['physical_adoption'] is False and lm['zero_native_RHS_relative_ratio'] is None and all(lm[n] is False for n in ('original_primitive_stationarity_mismatch_resolved','configuration_changed','physical_adoption')) and lm['literal_addition_defect_retained'] is True and lm['old_literal_addition_defect_preserved_in_INPUT'] is True
  nm=np.ones((33,3,87,45),bool);nm[:,:,0]=False;nm[:,1,:,0]=False;mm=np.ones((6,87,45),bool);mm[:,0]=False;mm[3:5,:,0]=False;assert int(np.sum(nm))==380292 and int(np.sum(mm))==23048
  def fields(x):
   assert x.shape==(403340,);n=np.zeros(nm.shape);m=np.zeros(mm.shape);n[nm]=x[:380292];m[mm]=x[380292:];return n,m
  rhs=pair(ia,'NEW_t_target_RHS');ns=ia['original_basis_native_scale'];ms=ia['original_basis_metric_scale'];nref=ia['inherited_original_native_affine_reference'];cref=ia['inherited_original_native_canonical_reference'];mref=fields(rhs[0]+rhs[1])[1];assert np.all(ns>0) and np.all(ms>0) and np.all(rhs[0][:380292]==0) and np.all(rhs[1][:380292]==0)
  def scores(label,res,stored,metadata=None):
   v=fields(res[0]+res[1]);rows=[];absolute=[]
   for x,ref,scale in ((v[0],nref,ns),(v[0],cref,ns),(v[1],mref,ms)):
    a=float(np.linalg.norm(x));b=float(np.linalg.norm(x/scale));c=float(np.linalg.norm(ref));d=float(np.linalg.norm(ref/scale));assert c>0 and d>0;rows.append((a/c,b/d));absolute.append((a,b,c,d,ROW_TOL*c,ROW_TOL*d))
   rows=np.asarray(rows);assert stored.shape==(3,2) and np.allclose(rows,stored,rtol=TOL,atol=1e-300),label
   if metadata is not None:assert np.array_equal(stored,np.asarray(metadata))
   return bool(np.all(stored<=ROW_TOL)),np.asarray(absolute)
  names=tuple(n+'_'+w for n in ('final_paired_response','unchanged_original_RHS','final_frozen_action','final_frozen_residual','exact_NEW_literal_increment') for w in ('hi','lo'))+('final_frozen_original_six_scores',)
  a=read(response,names);nodes=pair(a,'final_paired_response');action=pair(a,'final_frozen_action');res=pair(a,'final_frozen_residual');increment=pair(a,'exact_NEW_literal_increment');assert all(np.array_equal(pair(a,'unchanged_original_RHS')[w],rhs[w]) for w in (0,1));identity('frozen_saved_RHS_action_residual',[(1,rhs),(-1,action),(-1,res)])
  fok,fnorm=scores('frozen',res,a['final_frozen_original_six_scores']);assert fok==r['frozen_original_response_admitted']==rm['frozen_original_rows_admitted']==solver['original_six_rows_admitted']
  candidate_names=[]
  for q in snaps:
   md=q['metadata'];k=md['iteration'];assert md['kind']=='unrestarted_paired_GMRES_original_candidate_and_full_Arnoldi_state' and md['input_ref']==thin(inp) and md['cap']==80 and 1<=k<=80 and k<=solver['iterations'] and md['physical_adoption'] is False;label='coupled_STAR_GMRES_candidate_%03d'%k;candidate_names.append(label)
   sh=read(q,('coupled_STAR_GMRES_history',))['coupled_STAR_GMRES_history'];assert sh.shape==(k,4) and (k in (20,40,80) or (k==solver['iterations'] and sh[-1,2]==0));sc=q['metadata']['schema'];basis=sc['coupled_STAR_GMRES_all_earned_basis_hi'];assert basis==sc['coupled_STAR_GMRES_all_earned_basis_lo'] and basis['shape']==[403340,k] and sc['coupled_STAR_GMRES_H_hi']['shape']==sc['coupled_STAR_GMRES_H_lo']['shape']==sc['coupled_STAR_GMRES_R']['shape']==[81,80]
   keys=tuple(label+'_'+n+'_'+w for n in ('before_nodes','before_action','before_original_residual','delta','after_high_insert','updated_nodes','total_compression_words','exact_increment_two_word_readout','NEW_original_action','NEW_original_residual','NEW_delta_action','NEW_compression_action','residual_prediction','residual_update_gap') for w in ('hi','lo'))+(label+'_insert_high_exact_update_minus_two_word_nodes',label+'_insert_low_exact_update_minus_two_word_nodes',label+'_increment_readout_exact_expansion',label+'_residual_update_envelope',label+'_original_six_scores')
   ca=read(q,keys);old=pair(ca,label+'_before_nodes');delta=pair(ca,label+'_delta');mid=pair(ca,label+'_after_high_insert');new=pair(ca,label+'_updated_nodes');compression=pair(ca,label+'_total_compression_words');inc=pair(ca,label+'_exact_increment_two_word_readout');qh=ca[label+'_insert_high_exact_update_minus_two_word_nodes'];ql=ca[label+'_insert_low_exact_update_minus_two_word_nodes']
   assert all(np.array_equal(old[w],ia['latest_GMRES_seed_final_paired_response_'+('hi','lo')[w]]) and np.array_equal(pair(ca,label+'_before_action')[w],ia['latest_GMRES_seed_final_frozen_action_'+('hi','lo')[w]]) and np.array_equal(pair(ca,label+'_before_original_residual')[w],ia['latest_GMRES_seed_final_frozen_residual_'+('hi','lo')[w]]) for w in (0,1))
   exact(label+'_high_insertion',(old[0],old[1],delta[0],-mid[0],-mid[1],-qh));exact(label+'_low_insertion',(mid[0],mid[1],delta[1],-new[0],-new[1],-ql));exact(label+'_compression_words',(qh,ql,-compression[0],-compression[1]))
   expansion=ca[label+'_increment_readout_exact_expansion'];assert expansion.shape==(6,403340);supplied=(delta[0],delta[1],-compression[0],-compression[1],-inc[0],-inc[1]);assert all(math.fsum(x)==math.fsum(y) for x,y in zip(zip(*supplied),zip(*expansion)));identities.append(dict(name=label+'_exact_increment_readout_expansion',error=0.))
   env=ca[label+'_residual_update_envelope'];newres=pair(ca,label+'_NEW_original_residual');newaction=pair(ca,label+'_NEW_original_action');identity(label+'_stored_residual_prediction',[(1,newres),(-1,pair(ca,label+'_before_original_residual')),(1,pair(ca,label+'_NEW_delta_action')),(-1,pair(ca,label+'_NEW_compression_action')),(-1,pair(ca,label+'_residual_update_gap'))],env)
   identity(label+'_saved_prediction',[(1,pair(ca,label+'_residual_prediction')),(-1,pair(ca,label+'_before_original_residual')),(1,pair(ca,label+'_NEW_delta_action')),(-1,pair(ca,label+'_NEW_compression_action'))],env)
   identity(label+'_RHS_action_residual',[(1,rhs),(-1,newaction),(-1,newres)],env);ok,_=scores(label,newres,ca[label+'_original_six_scores']);assert ok==md['original_six_rows_admitted']
   copies=read(q,tuple('GMRES_current_'+n+'_'+w for n in ('nodes','original_action','original_residual','exact_increment') for w in ('hi','lo')))
   for name,source_name in (('nodes','updated_nodes'),('original_action','NEW_original_action'),('original_residual','NEW_original_residual'),('exact_increment','exact_increment_two_word_readout')):assert all(np.array_equal(pair(copies,'GMRES_current_'+name)[w],pair(ca,label+'_'+source_name)[w]) for w in (0,1))
  if snaps:
   last=read(snaps[-1],tuple('GMRES_current_'+n+'_'+w for n in ('nodes','original_action','original_residual','exact_increment') for w in ('hi','lo')))
   for role,p in (('nodes',nodes),('original_action',action),('original_residual',res),('exact_increment',increment)):assert all(np.array_equal(pair(last,'GMRES_current_'+role)[w],p[w]) for w in (0,1))
  else:
   assert solver['reason']=='exact_QR_pivot_breakdown'
   for w in (0,1):assert np.array_equal(nodes[w],ia['latest_GMRES_seed_final_paired_response_'+('hi','lo')[w]]) and np.all(increment[w]==0)
  bs=response['metadata']['schema'].get('coupled_STAR_GMRES_all_earned_basis_hi');assert bs is not None and bs==response['metadata']['schema']['coupled_STAR_GMRES_all_earned_basis_lo'] and bs['shape'][0]==403340 and 1<=bs['shape'][1]<=80
  if solver['iterations']:
   qr_fields=('coupled_STAR_GMRES_H_hi','coupled_STAR_GMRES_H_lo','coupled_STAR_GMRES_R','coupled_STAR_GMRES_Givens_cos','coupled_STAR_GMRES_Givens_sin','coupled_STAR_GMRES_rotated_RHS','coupled_STAR_GMRES_history');qr=read(response,qr_fields);history=qr['coupled_STAR_GMRES_history'];assert history.shape==(solver['iterations'],4) and np.array_equal(history[:,0],np.arange(1,solver['iterations']+1)) and qr['coupled_STAR_GMRES_H_hi'].shape==qr['coupled_STAR_GMRES_H_lo'].shape==qr['coupled_STAR_GMRES_R'].shape==(81,80)
  else:assert solver['reason']=='exact_QR_pivot_breakdown' and not snaps
  ja=read(jets,tuple('NEW_exact_increment_'+n+'_'+w for n in ('native_value','metric_value') for w in ('hi','lo')));assert lm['NEW_rate_jets']==thin(jets) and lm['NEW_rate_columns']==[thin(q) for q in cols] and lm['old_literal_ref']==im['latest_literal_readout']
  for iq,q in enumerate(cols):
   md=q['metadata'];assert md['kind']=='only_NEW_delta_minus_q_literal_rate_derivative' and md['column']==iq and md['configuration_unchanged'] is True and md['affine_constant_derivative_zero'] is True and md['old_primal_or_full_response_replayed'] is False and md['original_primitive_stationarity_mismatch_resolved'] is False
   local=read(q,tuple('NEW_exact_increment_local_'+n+'_'+w for n in ('native_value','physical_metric_value') for w in ('hi','lo')));sl=slice(iq*3784,(iq+1)*3784)
   for w in (0,1):assert np.array_equal(pair(local,'NEW_exact_increment_local_native_value')[w],pair(ja,'NEW_exact_increment_native_value')[w][:,sl].transpose(1,0,2).reshape(3784,99)) and np.array_equal(pair(local,'NEW_exact_increment_local_physical_metric_value')[w],pair(ja,'NEW_exact_increment_metric_value')[w][sl])
   for family,fields2 in (('NEW_increment_first_jet',('du','dz','dg','Ga')),('NEW_increment_feature',('nu','nz','V','D','F','Fup','a','Pi','PiU')),('NEW_increment_momentum',('native_density','metric_total_density','K','Ktrace','metric_EH_tensor','connection_momentum'))):assert all(family+'_'+n+'_'+w in md['schema'] for n in fields2 for w in ('hi','lo'))
  label='STAR_GMRES_literal_translation';rbases=('NEW_increment_literal_full_action',label+'_old_saved_literal_action',label+'_NEW_increment_literal_action',label+'_new_literal_action',label+'_new_literal_residual',label+'_literal_minus_frozen_derivative');ra=read(ro,tuple(n+'_'+w for n in rbases for w in ('hi','lo'))+(label+'_literal_original_scores',label+'_literal_addition_defect_exact_expansion'))
  old_literal=pair(ra,label+'_old_saved_literal_action');new_literal=pair(ra,label+'_NEW_increment_literal_action');literal=pair(ra,label+'_new_literal_action');lres=pair(ra,label+'_new_literal_residual');assert all(np.array_equal(old_literal[w],ia['latest_GMRES_literal_recycled_trace_literal_translation_new_literal_action_'+('hi','lo')[w]]) and np.array_equal(new_literal[w],pair(ra,'NEW_increment_literal_full_action')[w]) for w in (0,1))
  expansion=ra[label+'_literal_addition_defect_exact_expansion'];assert expansion.shape==(6,403340);supplied=(old_literal[0],old_literal[1],new_literal[0],new_literal[1],-literal[0],-literal[1]);assert all(math.fsum(x)==math.fsum(y) for x,y in zip(zip(*supplied),zip(*expansion)));identity('literal_saved_RHS_action_residual',[(1,rhs),(-1,literal),(-1,lres)]);identity('stored_literal_minus_frozen_remainder',[(1,literal),(-1,action),(-1,pair(ra,label+'_literal_minus_frozen_derivative'))])
  lok,lnorm=scores('literal',lres,ra[label+'_literal_original_scores'],lm['literal_original_six_scores']);assert lok==r['literal_original_response_admitted']==lm['literal_original_response_admitted'] and r['status']==('STAR_GMRES_LITERAL_TRACE_RESPONSE_ADMITTED' if fok and lok else 'STAR_GMRES_LITERAL_TRACE_RESPONSE_NOT_ADMITTED')
  report=dict(status='SAVED_STAR_GMRES_TRACE_RESPONSE_CLOSURE_PASS',producer_status=r['status'],controls=len(controls),committed_pairs=len(records),all111_latest_INPUT_fields_bitcopied=True,all88_factor_INPUT_fields_bitcopied=True,shared76_fields_bitwise_equal=True,latest_solution_literal_and_factor_wordcopies=True,original_factor_componentwise_control_12_passed=False,iterations=solver['iterations'],candidate_checkpoints=len(snaps),cap=80,restarts=0,frozen_original_response_admitted=fok,literal_original_response_admitted=lok,frozen_absolute_residual_reference_thresholds=fnorm.tolist(),literal_absolute_residual_reference_thresholds=lnorm.tolist(),zero_native_RHS_relative_ratio=None,NEW_increment_columns_complete=4,original_primitive_stationarity_mismatch_resolved=False)
 report.update(owner_pid=os.getpid(),parent=TERMINAL,selected=selected,identities=identities,numeric_header_count=header_count,arithmetic_tolerance=TOL,original_row_tolerance=ROW_TOL,A_STAR_energy_Arnoldi_QR_GMRES_rate_E_F_scatter_or_fixture_replayed=False,physical_adoption=False,scope_limit='Saved controls, immutable copies, EFT insertion/addition words, stored residual contacts and original six reference norms only. All basis/H/QR words are seal/schema checked; orthogonality, QR reproducts and operator/transpose contacts are not recontracted. Literal increment features and scatter are authenticated serialized data only. Finite normal/CMC/phase/exterior/evolution/43 readout remain unqualified.')
 for n,h in rc['output_sha256'].items():assert sha(n)==h,n
 assert sha(receipt)==TERMINAL['receipt_sha256'] and sha(SOURCE)==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA
 with path(OUT).open('x') as f:json.dump(report,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
 path(OUT).chmod(0o444);print(json.dumps(dict(status=report['status'],pid=os.getpid(),sha256=sha(OUT))),flush=True)
if __name__=='__main__':main()

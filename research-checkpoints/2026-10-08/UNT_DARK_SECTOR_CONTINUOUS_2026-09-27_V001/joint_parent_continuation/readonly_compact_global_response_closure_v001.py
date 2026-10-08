"""Guarded saved-output arithmetic only; no imported scientific definitions."""
from pathlib import Path
import hashlib,json,math,os
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_COMPACT_CONFIGURATION_GLOBAL_RATE_RESPONSE_V001'
OUT='READONLY_COMPACT_GLOBAL_RESPONSE_CLOSURE_V001_RESULT.json'
AUTHOR_DRAFT=False
SOURCE_SHA='99d78680bc628ff0b4eade105ab20e1c933064ff88f747c6ee06203bb10e5e93'
PROTOCOL_SHA='adebde2682b8ceb5dc0067d742a1cbba1fcdeed3a5dadbc2a02000f956d4f56b'
TERMINAL=dict(pid=55595,result_sha256='1f487ba1e70c90f46a4e203abe815b4fccd7756a43a932633a4c39f7e837ae08',receipt_sha256='97ff7badbcfcd50c8e5f84c28cf538dc0088e5c40a01d37d6bff565cfcdf89e3',error_sha256=None)
TOL=2e-11
def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p
def sha(n):
 h=hashlib.sha256()
 with path(n).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def load_json(n,h):
 assert h is not None and sha(n)==h,n
 return json.loads(path(n).read_text())
def main():
 assert AUTHOR_DRAFT is False and TERMINAL['pid'] is not None and TERMINAL['receipt_sha256'] is not None
 assert (TERMINAL['result_sha256'] is None)!=(TERMINAL['error_sha256'] is None)
 assert not path(OUT).exists()
 import numpy as np
 assert sha('cross_u_compact_configuration_global_rate_response_v001.py')==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA
 rc=load_json(STEM+'_RECEIPT.json',TERMINAL['receipt_sha256']);closed=rc['status']=='CLOSED'
 assert rc['status'] in ('CLOSED','CLOSED_ERROR') and rc['owner']['pid']==TERMINAL['pid'] and rc['owner']['source_sha256']==SOURCE_SHA
 name=STEM+('_RESULT.json' if closed else '_ERROR.json');h=TERMINAL['result_sha256'] if closed else TERMINAL['error_sha256'];r=load_json(name,h)
 assert r['owner']==rc['owner'] and rc.get('result_sha256')==TERMINAL['result_sha256'] and rc.get('error_sha256')==TERMINAL['error_sha256']
 assert r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values())
 for n,h in rc['output_sha256'].items():assert sha(n)==h,n
 records=r['checkpoints'];assert len({x['file'] for x in records})==len(records)
 assert {p.name for p in BASE.glob(STEM+'_*.npz')}=={x['file'] for x in records}
 assert {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={x['commit_file'] for x in records}
 for x in records:
  assert rc['output_sha256'][x['file']]==x['sha256'] and rc['output_sha256'][x['commit_file']]==x['commit_sha256']
  assert load_json(x['commit_file'],x['commit_sha256'])=={k:x[k] for k in ('file','sha256','metadata')}
  assert x['metadata']['owner']==r['owner'] and x['metadata']['qualification']==r['qualification']
 controls=r['controls'];assert [c['ordinal'] for c in controls]==list(range(len(controls)))
 assert all(c['tolerance']==TOL and math.isfinite(c['error']) and c['passed']==(c['error']<=TOL) for c in controls)
 if not closed:
  report=dict(status='SAVED_GLOBAL_RESPONSE_CLOSED_FAILURE_PRESERVED',owner_pid=os.getpid(),parent=TERMINAL,committed_pairs=len(records),controls=controls,context=r.get('context'),physical_adoption=False,operator_or_feature_or_solver_replayed=False)
 else:
  assert all(c['passed'] for c in controls) and r['configuration_updated'] is False and r['physical_adoption'] is False and r['phase_charge_preserved'] is False
  selected=[];identities=[]
  def read(x,names):
   sc=x['metadata']['schema'];out={}
   with np.load(path(x['file']),allow_pickle=False) as f:
    assert set(f.files)==set(sc)|{'metadata_json'} and json.loads(str(f['metadata_json']))==x['metadata']
    for n in names:
     a=f[n].copy();assert list(a.shape)==sc[n]['shape'] and str(a.dtype)==sc[n]['dtype'] and sc[n]['finite'] is True and np.all(np.isfinite(a)),n
     out[n]=a
   selected.append(dict(file=x['file'],fields=len(names)));return out
  def pair(a,n):return a[n+'_hi'],a[n+'_lo']
  def total(x):return x[0]+x[1]
  def identity(label,terms):
   values=[a for sign,p in terms for a in (sign*p[0],sign*p[1])];actual=np.add.reduce(values)
   bound=np.add.reduce([abs(a) for a in values]);error=float(np.max(abs(actual)/np.maximum(bound,1e-30),initial=0));assert error<=TOL,(label,error)
   identities.append(dict(name=label,error=error))
  inp=records[0];assert inp['metadata']['kind']=='one_compact_configuration_contact_global_fixed_target_response'
  q=read(inp,('new_rhs_hi','new_rhs_lo'));rhs=pair(q,'new_rhs');assert rhs[0].shape==rhs[1].shape==(403340,)
  response=[x for x in records if x['metadata'].get('kind')=='single_new_RHS_global_rate_response_diagnostic'];assert len(response)==1;response=response[0]
  a=read(response,('new_rhs_hi','new_rhs_lo','frozen_action_hi','frozen_action_lo','frozen_original_residual_hi','frozen_original_residual_lo','new_RHS_original_ratios'))
  for w in ('hi','lo'):assert np.array_equal(a['new_rhs_'+w],q['new_rhs_'+w])
  action=pair(a,'frozen_action');res=pair(a,'frozen_original_residual');identity('new_rhs_minus_action_minus_residual',[(1,rhs),(-1,action),(-1,res)])
  basis=inp['metadata']['system_refs']['basis'];im=rc['input_sha256']
  for n,h in ((basis['file'],basis['sha256']),(basis['commit_file'],basis['commit_sha256'])):assert im.get(n,im.get(str(path(n).resolve())))==h and sha(n)==h
  assert load_json(basis['commit_file'],basis['commit_sha256'])=={k:basis[k] for k in ('file','sha256','metadata')}
  bs=read(basis,('native_scale','metric_scale'));nm=np.ones((3,87,45),bool);nm[:,0]=False;nm[1,:,0]=False;mm=np.ones((6,87,45),bool);mm[:,0]=False;mm[3:5,:,0]=False
  ns=bs['native_scale'][np.broadcast_to(nm,bs['native_scale'].shape)];ms=bs['metric_scale'][mm];assert len(ns)==380292 and len(ms)==23048 and np.all(ns>0) and np.all(ms>0)
  rr=total(res);fr=total(rhs);ratios=np.array([[np.linalg.norm(rr[:380292])/np.linalg.norm(fr[:380292]),np.linalg.norm(rr[:380292]/ns)/np.linalg.norm(fr[:380292]/ns)],[np.linalg.norm(rr[380292:])/np.linalg.norm(fr[380292:]),np.linalg.norm(rr[380292:]/ms)/np.linalg.norm(fr[380292:]/ms)]])
  assert np.allclose(ratios,a['new_RHS_original_ratios'],rtol=TOL,atol=1e-30) and np.array_equal(a['new_RHS_original_ratios'],np.array(r['new_RHS_original_ratios']))
  assert r['response_rows_admitted']==bool(np.all(a['new_RHS_original_ratios']<=1e-10)) and response['metadata']['response_rows_admitted']==r['response_rows_admitted']
  cycles=[x for x in records if x['metadata'].get('kind')=='new_RHS_response_with_original_full_DD_certificate'];assert len(cycles)==len(r['cycles'])<=3 and len(controls)==len(cycles)+1
  previous=rhs
  for ordinal,x in enumerate(cycles):
   label='response_cycle_%03d'%(ordinal+1);assert x['metadata']['cycle']==ordinal+1 and x['metadata']['cap']==160 and x['metadata']['controls']==[controls[ordinal]]
   names=tuple(label+'_'+n+'_'+w for n in ('final_residual','shift_prediction','shift_identity_gap','delta_action','third_word_action') for w in ('hi','lo'))+(label+'_upstream_bound_through_third_word',)
   z=read(x,names);final=pair(z,label+'_final_residual');prediction=pair(z,label+'_shift_prediction');gap=pair(z,label+'_shift_identity_gap')
   identity(label+'_prediction',[(1,prediction),(-1,previous),(1,pair(z,label+'_delta_action')),(-1,pair(z,label+'_third_word_action'))])
   identity(label+'_stored_update_gap',[(1,final),(-1,prediction),(-1,gap)])
   e=z[label+'_upstream_bound_through_third_word'];assert np.all(e>=0)
   error=max(np.linalg.norm(total(gap)[:380292])/max(np.linalg.norm(e[:380292]),1e-30),np.linalg.norm(total(gap)[380292:])/max(np.linalg.norm(e[380292:]),1e-30));assert math.isclose(error,controls[ordinal]['error'],rel_tol=TOL,abs_tol=1e-30)
   previous=final
  assert np.array_equal(previous[0],res[0]) and np.array_equal(previous[1],res[1])
  tangents=[x for x in records if x['metadata'].get('kind')=='new_literal_primitive_temporal_tangent_at_held_configuration'];assert [x['metadata']['column'] for x in tangents]==list(range(4))
  for x in tangents:
   z=read(x,tuple(n+'_'+w for n in ('delta_native_density','delta_metric_density','delta_Gamma_trace_density') for w in ('hi','lo')))
   for n,shape in (('delta_native_density',(3784,99)),('delta_metric_density',(3784,6)),('delta_Gamma_trace_density',(3784,))):assert pair(z,n)[0].shape==pair(z,n)[1].shape==shape
  out=[x for x in records if x['metadata'].get('kind')=='conditional_literal_bridge_and_weak_trace_response'];assert len(out)==1;out=out[0];assert out['metadata']['trace_target_not_imposed'] is True and out['metadata']['phase_charge_held'] is False and out['metadata']['original_finite_stationarity_gap_retained'] is True
  prior=out['metadata']['prior_signed_primitive_readout'];assert prior==inp['metadata']['contact_refs']['prior_signed_primitive_readout'] and prior['metadata']['owner']['pid']==50104 and prior['metadata']['canonical_primitive_readout_admitted'] is False
  for n,h in ((prior['file'],prior['sha256']),(prior['commit_file'],prior['commit_sha256'])):assert im.get(n,im.get(str(path(n).resolve())))==h
  prefixes=('literal_action','frozen_to_literal_tangent_bridge','combined_literal_momentum_contact','literal_bookkeeping_gap','frozen_trace_response','literal_Gamma_trace_response','trace_rate_bridge','configuration_Gamma_trace_contact','configuration_ADM_trace_contact','combined_Gamma_trace_contact','combined_ADM_trace_contact');names=tuple(n+'_'+w for n in prefixes for w in ('hi','lo'))
  control_names=tuple(n for n in out['metadata']['schema'] if n.startswith('control_'));z=read(out,names+control_names)
  p=lambda n:pair(z,n);identity('literal_minus_frozen_bridge',[(1,p('literal_action')),(-1,action),(-1,p('frozen_to_literal_tangent_bridge'))]);identity('combined_contact',[(1,p('combined_literal_momentum_contact')),(1,rhs),(-1,p('literal_action'))]);identity('bookkeeping',[(1,p('combined_literal_momentum_contact')),(1,res),(-1,p('frozen_to_literal_tangent_bridge')),(-1,p('literal_bookkeeping_gap'))])
  identity('trace_rate_bridge',[(1,p('literal_Gamma_trace_response')),(-1,p('frozen_trace_response')),(-1,p('trace_rate_bridge'))]);identity('combined_Gamma_trace',[(1,p('configuration_Gamma_trace_contact')),(1,p('literal_Gamma_trace_response')),(-1,p('combined_Gamma_trace_contact'))]);identity('combined_ADM_trace',[(1,p('configuration_ADM_trace_contact')),(1,p('frozen_trace_response')),(-1,p('combined_ADM_trace_contact'))])
  last=controls[-1];stem='control_%03d_%s_'%(last['ordinal'],last['name']);ca,ce,cb=(z[stem+n] for n in ('actual','expected','envelope'));assert np.all(cb>=0);err=float(np.max(abs(ca-ce)/np.maximum(cb,1e-30),initial=0));assert err==last['error'] and err<=TOL
  assert len(records)==7+len(cycles)+sum(x['metadata'].get('kind')=='unqualified_restart_snapshot_signed_MINRES_iterate' for x in records)
  trace_norms={n:dict(L2=float(np.linalg.norm(total(p(n)))),Linf=float(np.max(abs(total(p(n))),initial=0))) for n in prefixes if 'trace' in n}
  report=dict(status='SAVED_GLOBAL_RESPONSE_CLOSURE_PASS',parent_status=r['status'],owner_pid=os.getpid(),parent=TERMINAL,controls=len(controls),committed_pairs=len(records),identities=identities,selected=selected,new_RHS_original_ratios=ratios.tolist(),response_rows_admitted=r['response_rows_admitted'],signed_trace_norms_descriptive=trace_norms,prior_signed_primitive_readout=out['metadata']['prior_signed_primitive_readout'],physical_adoption=False,phase_charge_preserved=False,operator_or_feature_or_solver_replayed=False)
 for n,h in rc['output_sha256'].items():assert sha(n)==h
 assert sha(STEM+'_RECEIPT.json')==TERMINAL['receipt_sha256']
 with path(OUT).open('x') as f:json.dump(report,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
 path(OUT).chmod(0o444);print(json.dumps(dict(status=report['status'],pid=os.getpid(),sha256=sha(OUT))),flush=True)
if __name__=='__main__':main()

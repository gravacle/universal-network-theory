"""Saved words and arithmetic only; no scientific definitions or old operators."""
from pathlib import Path
import hashlib,json,math,os
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_COMPACT_CONFIGURATION_GLOBAL_RATE_RESPONSE_V002'
OUT='READONLY_COMPACT_WARM_RESPONSE_CLOSURE_V002_RESULT.json'
AUTHOR_DRAFT=True
SOURCE_SHA='f2ca60901d417668f965db4d81c10c09b7513a1c9193f53e02347a6242f3c458'
PROTOCOL_SHA='ea907bc213898a261cf2c21ba84cf86ffa484aa80e019b35c5cbe2586e2c9479'
TERMINAL=dict(pid=None,result_sha256=None,receipt_sha256=None,error_sha256=None)
PRIOR_CHECKER=('READONLY_COMPACT_GLOBAL_RESPONSE_CLOSURE_V001_RESULT.json','3de4b8b9a9727d512d4cd9d73ae6929904cc6627f0d4ed15256322c77b3b3fb7')
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
 assert (TERMINAL['result_sha256'] is None)!=(TERMINAL['error_sha256'] is None) and not path(OUT).exists()
 assert sha('cross_u_compact_configuration_global_rate_response_v002.py')==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA
 rc=load_json(STEM+'_RECEIPT.json',TERMINAL['receipt_sha256']);closed=rc['status']=='CLOSED'
 assert rc['status'] in ('CLOSED','CLOSED_ERROR') and rc['owner']['pid']==TERMINAL['pid'] and rc['owner']['source_sha256']==SOURCE_SHA
 r=load_json(STEM+('_RESULT.json' if closed else '_ERROR.json'),TERMINAL['result_sha256'] if closed else TERMINAL['error_sha256'])
 assert r['owner']==rc['owner'] and rc.get('result_sha256')==TERMINAL['result_sha256'] and rc.get('error_sha256')==TERMINAL['error_sha256']
 assert r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values())
 for n,h in rc['output_sha256'].items():assert sha(n)==h,n
 records=r['checkpoints'];controls=r['controls'];assert len({q['file'] for q in records})==len(records)
 assert {p.name for p in BASE.glob(STEM+'_*.npz')}=={q['file'] for q in records} and {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={q['commit_file'] for q in records}
 for q in records:
  assert rc['output_sha256'][q['file']]==q['sha256'] and rc['output_sha256'][q['commit_file']]==q['commit_sha256']
  assert load_json(q['commit_file'],q['commit_sha256'])=={k:q[k] for k in ('file','sha256','metadata')}
  assert q['metadata']['owner']==r['owner'] and q['metadata']['qualification']==r['qualification'] and all(v['finite'] is True for v in q['metadata']['schema'].values())
 assert [c['ordinal'] for c in controls]==list(range(len(controls))) and all(c['tolerance']==TOL and math.isfinite(c['error']) and c['passed']==(c['error']<=TOL) for c in controls)
 if not closed:
  report=dict(status='SAVED_WARM_RESPONSE_FAILURE_PRESERVED',context=r.get('context'),controls=controls,committed_pairs=len(records))
 else:
  import numpy as np
  assert all(c['passed'] for c in controls) and r['original_budget_unchanged'] is True and r['old_literal_replayed'] is False and r['configuration_updated'] is False and r['phase_charge_preserved'] is False and r['physical_adoption'] is False
  assert r['additional_budget']==dict(cycles=3,cap=160)
  proof=load_json(*PRIOR_CHECKER);assert proof['status']=='SAVED_GLOBAL_RESPONSE_CLOSURE_PASS' and proof['owner_pid']==56739 and proof['response_rows_admitted'] is False
  identities=[];selected=[]
  def read(q,names):
   sc=q['metadata']['schema'];out={}
   with np.load(path(q['file']),allow_pickle=False) as f:
    assert set(f.files)==set(sc)|{'metadata_json'} and json.loads(str(f['metadata_json']))==q['metadata']
    for n in names:
     a=f[n].copy();assert list(a.shape)==sc[n]['shape'] and str(a.dtype)==sc[n]['dtype'] and sc[n]['finite'] is True and np.all(np.isfinite(a)),n;out[n]=a
   selected.append(dict(file=q['file'],fields=len(names)));return out
  def prior_record(q):
   for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert rc['input_sha256'].get(n,rc['input_sha256'].get(str(path(n).resolve())))==h and sha(n)==h
   assert load_json(q['commit_file'],q['commit_sha256'])=={k:q[k] for k in ('file','sha256','metadata')};return q
  def pair(a,n):return a[n+'_hi'],a[n+'_lo']
  def total(p):return p[0]+p[1]
  def identity(label,terms):
   a=[sign*x for sign,p in terms for x in p];gap=np.add.reduce(a);bound=np.add.reduce([abs(x) for x in a]);e=float(np.max(abs(gap)/np.maximum(bound,1e-30),initial=0));assert e<=TOL,(label,e);identities.append(dict(name=label,error=e))
  def exact_sum(label,terms):
   arrays=[np.asarray(a).ravel() for a in terms];assert all(a.shape==arrays[0].shape for a in arrays)
   # Independent correctly rounded scalar sum; no producer expansion routine.
   maximum=max((abs(math.fsum(float(a[i]) for a in arrays)) for i in range(len(arrays[0]))),default=0.0)
   assert maximum==0.0,(label,maximum);identities.append(dict(name=label,exact_saved_binary64_sum_zero=True,entries=len(arrays[0])))
  def control(q,a,c):
   prefix='control_%03d_%s_'%(c['ordinal'],c['name']);ca,ce,eb=(a[prefix+n] for n in ('actual','expected','envelope'));assert np.all(eb>=0)
   e=float(np.max(abs(ca-ce)/np.maximum(eb,1e-30),initial=0));assert e==c['error'] and e<=TOL
  base=records[0];assert base['metadata']['kind']=='exact_closed_response_and_literal_readout_recovery'
  old=base['metadata']['prior_refs'];prior=prior_record(old['response']);oldout=prior_record(old['readout']);prior_record(old['final_cycle'])
  z=read(base,tuple(base['metadata']['schema']));rhs=pair(z,'restored_rhs');previous=pair(z,'restored_residual');nodes=pair(z,'restored_nodes')
  oldr=read(prior,tuple(prior['metadata']['schema']));assert np.allclose(oldr['new_RHS_original_ratios'],np.array(proof['new_RHS_original_ratios']),rtol=TOL,atol=1e-300)
  prefixes=('literal_action','literal_Gamma_trace_response','frozen_trace_response','configuration_Gamma_trace_contact','configuration_ADM_trace_contact','frozen_to_literal_tangent_bridge','combined_literal_momentum_contact','literal_bookkeeping_gap','trace_rate_bridge','combined_Gamma_trace_contact','combined_ADM_trace_contact')
  oo=read(oldout,tuple(n+'_'+w for n in prefixes for w in ('hi','lo')))
  for n in prefixes:
   for w in ('hi','lo'):assert np.array_equal(z['restored_'+n+'_'+w],oo[n+'_'+w])
  for new,oldname in (('restored_rhs','new_rhs'),('restored_action','frozen_action'),('restored_residual','frozen_original_residual')):
   for w in ('hi','lo'):assert np.array_equal(z[new+'_'+w],oldr[oldname+'_'+w])
  nm=np.ones((3,87,45),bool);nm[:,0]=False;nm[1,:,0]=False;mm=np.ones((6,87,45),bool);mm[:,0]=False;mm[3:5,:,0]=False
  for iw,w in enumerate(('hi','lo')):assert np.array_equal(nodes[iw],np.concatenate((oldr['native_rate_response_'+w][np.broadcast_to(nm,(33,3,87,45))],oldr['metric_rate_response_'+w][mm])))
  basis=prior_record(base['metadata']['node_refs']['system']['basis']);sc=read(basis,('native_scale','metric_scale'));ns=sc['native_scale'][np.broadcast_to(nm,(33,3,87,45))];ms=sc['metric_scale'][mm];assert len(ns)==380292 and len(ms)==23048 and np.all(ns>0) and np.all(ms>0)
  cycles=[q for q in records if q['metadata'].get('kind')=='warm_same_RHS_response_with_original_full_DD_certificate'];increments=[q for q in records if q['metadata'].get('kind')=='new_increment_only_literal_response_with_retained_addition_defects']
  assert [q['metadata']['cycle'] for q in cycles]==[4+i for i in range(len(cycles))] and 1<=len(cycles)<=3 and len(increments)==len(cycles) and len(controls)==len(cycles)+1 and len(records)==3+6*len(cycles)+sum(q['metadata'].get('kind')=='unqualified_restart_snapshot_signed_MINRES_iterate' for q in records)
  literal=pair(z,'restored_literal_action')
  for ordinal,(q,inc) in enumerate(zip(cycles,increments)):
   cycle=q['metadata']['cycle'];label='response_continuation_%03d'%cycle;assert q['metadata']['cap']==160 and q['metadata']['controls']==[controls[ordinal]] and q['metadata']['new_budget_explicit'] is True and inc['metadata']['cycle']==cycle
   names=tuple(label+'_'+n+'_'+w for n in ('final_action','final_residual','shift_prediction','shift_identity_gap','delta_action','third_word_action','exact_increment','final_update_old_nodes','final_update_updated_nodes') for w in ('hi','lo'))+(label+'_completed_correction',label+'_final_update_exact_update_minus_two_word_nodes',label+'_upstream_bound_through_third_word')+tuple(n for n in q['metadata']['schema'] if n.startswith('control_'))
   a=read(q,names);control(q,a,controls[ordinal]);delta=a[label+'_completed_correction'];q3=a[label+'_final_update_exact_update_minus_two_word_nodes'];newnodes=pair(a,label+'_final_update_updated_nodes');incnodes=pair(a,label+'_exact_increment')
   for iw in (0,1):assert np.array_equal(nodes[iw],pair(a,label+'_final_update_old_nodes')[iw])
   exact_sum(label+'_node_update',(nodes[0],nodes[1],delta,-newnodes[0],-newnodes[1],-q3));exact_sum(label+'_increment',(delta,-q3,-incnodes[0],-incnodes[1]))
   final=pair(a,label+'_final_residual');prediction=pair(a,label+'_shift_prediction');gap=pair(a,label+'_shift_identity_gap');identity(label+'_original_rhs',[(1,rhs),(-1,pair(a,label+'_final_action')),(-1,final)])
   identity(label+'_prediction',[(1,prediction),(-1,previous),(1,pair(a,label+'_delta_action')),(-1,pair(a,label+'_third_word_action'))]);identity(label+'_gap',[(1,final),(-1,prediction),(-1,gap)])
   eb=a[label+'_upstream_bound_through_third_word'];assert np.all(eb>=0);cp='control_%03d_%s_'%(ordinal,controls[ordinal]['name']);gn=np.array([np.linalg.norm(total(gap)[:380292]),np.linalg.norm(total(gap)[380292:])]);en=np.array([np.linalg.norm(eb[:380292]),np.linalg.norm(eb[380292:])]);assert np.allclose(gn,a[cp+'actual'],rtol=TOL,atol=1e-300) and np.allclose(en,a[cp+'envelope'],rtol=TOL,atol=1e-300)
   v=read(inc,tuple(inc['metadata']['schema']));newliteral=pair(v,'literal_action');assert v['literal_addition_defect_words'].shape==(6,403340)
   for iw in (0,1):assert np.array_equal(pair(v,'increment_nodes')[iw],incnodes[iw])
   exact_sum(label+'_literal_addition',(literal[0],literal[1],v['increment_literal_hi'],v['increment_literal_lo'],-newliteral[0],-newliteral[1],*[-a for a in v['literal_addition_defect_words']]))
   identity(label+'_increment_bridge',[(1,pair(v,'increment_literal')),(-1,pair(a,label+'_delta_action')),(1,pair(a,label+'_third_word_action')),(-1,pair(v,'increment_literal_bridge'))])
   for n in ('literal_trace_addition_defect_words','frozen_trace_addition_defect_words'):assert v[n].shape==(6,87,45)
   literal=newliteral;previous=final;nodes=newnodes
  response=r['response'];assert response in records;rr=read(response,tuple(response['metadata']['schema']));res=pair(rr,'frozen_original_residual');action=pair(rr,'frozen_action')
  for iw,w in enumerate(('hi','lo')):
   assert np.array_equal(rr['new_rhs_'+w],rhs[iw]) and np.array_equal(res[iw],previous[iw]);assert np.array_equal(nodes[iw],np.concatenate((rr['native_rate_response_'+w][np.broadcast_to(nm,(33,3,87,45))],rr['metric_rate_response_'+w][mm])))
  f=total(rhs);y=total(res);ratios=np.array([[np.linalg.norm(y[:380292])/np.linalg.norm(f[:380292]),np.linalg.norm(y[:380292]/ns)/np.linalg.norm(f[:380292]/ns)],[np.linalg.norm(y[380292:])/np.linalg.norm(f[380292:]),np.linalg.norm(y[380292:]/ms)/np.linalg.norm(f[380292:]/ms)]])
  assert np.allclose(ratios,rr['new_RHS_original_ratios'],rtol=TOL,atol=1e-300) and np.array_equal(rr['new_RHS_original_ratios'],np.array(r['new_RHS_original_ratios'])) and r['response_rows_admitted']==bool(np.all(ratios<=1e-10))
  out=r['readout'];assert out in records and out['metadata']['trace_target_not_imposed'] is True and out['metadata']['phase_charge_held'] is False and out['metadata']['prior_signed_primitive_readout']==base['metadata']['contact_refs']['prior_signed_primitive_readout']
  a=read(out,tuple(out['metadata']['schema']));p=lambda n:pair(a,n);control(out,a,controls[-1])
  for iw in (0,1):
   assert np.array_equal(p('literal_action')[iw],literal[iw])
   for n in ('literal_Gamma_trace_response','frozen_trace_response'):assert np.array_equal(p(n)[iw],pair(v,n)[iw])
  identity('literal_frozen_bridge',[(1,p('literal_action')),(-1,action),(-1,p('frozen_to_literal_tangent_bridge'))]);identity('combined_literal',[(1,p('combined_literal_momentum_contact')),(1,rhs),(-1,p('literal_action'))]);identity('literal_bookkeeping',[(1,p('combined_literal_momentum_contact')),(1,res),(-1,p('frozen_to_literal_tangent_bridge')),(-1,p('literal_bookkeeping_gap'))])
  identity('trace_bridge',[(1,p('literal_Gamma_trace_response')),(-1,p('frozen_trace_response')),(-1,p('trace_rate_bridge'))]);identity('Gamma_sum',[(1,p('configuration_Gamma_trace_contact')),(1,p('literal_Gamma_trace_response')),(-1,p('combined_Gamma_trace_contact'))]);identity('ADM_sum',[(1,p('configuration_ADM_trace_contact')),(1,p('frozen_trace_response')),(-1,p('combined_ADM_trace_contact'))])
  for n in ('configuration_Gamma_trace_contact','configuration_ADM_trace_contact'):
   for iw in (0,1):assert np.array_equal(p(n)[iw],pair(z,'restored_'+n)[iw])
  tangents=[q for q in records if q['metadata'].get('kind')=='new_literal_primitive_temporal_tangent_at_held_configuration'];assert [q['metadata']['column'] for q in tangents]==list(range(4))*len(cycles)
  for q in tangents:
   t=read(q,tuple(q['metadata']['schema']))
   for n,shape in (('delta_native_density',(3784,99)),('delta_metric_density',(3784,6)),('delta_Gamma_trace_density',(3784,))):assert pair(t,n)[0].shape==pair(t,n)[1].shape==shape
  summary={}
  for n in ('frozen_to_literal_tangent_bridge','combined_literal_momentum_contact'):
   v=total(p(n));summary[n]=dict(native_raw=float(np.linalg.norm(v[:380292])/np.linalg.norm(f[:380292])),native_scaled=float(np.linalg.norm(v[:380292]/ns)/np.linalg.norm(f[:380292]/ns)),metric_raw=float(np.linalg.norm(v[380292:])/np.linalg.norm(f[380292:])),metric_scaled=float(np.linalg.norm(v[380292:]/ms)/np.linalg.norm(f[380292:]/ms)))
  report=dict(status='SAVED_WARM_RESPONSE_CLOSURE_PASS',controls=len(controls),committed_pairs=len(records),cycles=[q['metadata']['cycle'] for q in cycles],identities=identities,selected=selected,new_RHS_original_ratios=ratios.tolist(),response_rows_admitted=r['response_rows_admitted'],literal_bridge_and_combined_contact_over_new_RHS=summary,signed_trace_norms_descriptive={n:dict(L2=float(np.linalg.norm(total(p(n)))),Linf=float(np.max(abs(total(p(n))),initial=0))) for n in prefixes if 'trace' in n},independent_trace_increment_addition_checked=False,trace_limit='Incremental trace operands not published; finite six-word defects and final stored trace sums checked without scatter replay',original_55595_nonadmission_preserved=True,prior_signed_primitive_readout=out['metadata']['prior_signed_primitive_readout'])
 report.update(owner_pid=os.getpid(),parent=TERMINAL,physical_adoption=False,phase_charge_preserved=False,operator_or_feature_or_solver_or_scatter_replayed=False)
 for n,h in rc['output_sha256'].items():assert sha(n)==h
 assert sha(STEM+'_RECEIPT.json')==TERMINAL['receipt_sha256']
 with path(OUT).open('x') as f:json.dump(report,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
 path(OUT).chmod(0o444);print(json.dumps(dict(status=report['status'],pid=os.getpid(),sha256=sha(OUT))),flush=True)
if __name__=='__main__':main()

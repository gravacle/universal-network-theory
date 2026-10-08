"""Held one recycled numerical correction; immutable original trace response retained."""
from pathlib import Path
import importlib.util,hashlib,json,math,os,sys,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_RECYCLED_TRACE_TARGET_RATE_RESPONSE_V001'
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='1352d9e45283e6afd64e17e0d3b4458522a647984d2d91b970e6c922d45d9f7f'
PROVIDER='cross_u_initial_york_trace_target_rate_response_v001.py'
PROVIDER_SHA='23cbba6893b934236c8fff2c8ff4dda63f6808f589a04f701dcd536fdd31de27'
KERNEL='author_fragment_recycled_trace_response_preconditioner_v001.py'
KERNEL_SHA='2d5b8bd8289ba38b5b7bce5b4d13fd62d4c6020c63eaf118652b3bf5e1aa63d5'
ADMISSION='author_fragment_recycled_trace_response_admission_v001.py'
ADMISSION_SHA='9043c4eaeaa8dccd4ab74b013c93f839c4dde31af4aa3fc0fdadb5f68b7bee33'
T=R=P=N=np=None

def bind(n,h):
 p=Path(n);p=p if p.is_absolute() else BASE/p;assert h is not None and P.sha(p)==h,n
 key=str(p.resolve());assert key not in P.INPUTS or P.INPUTS[key]==h;P.INPUTS[key]=h;return p
def keep(n,x):return ORIGINAL_CAPTURE(n,np.asarray(x).copy())
def pair_keep(n,x):
 for w,suffix in enumerate(('hi','lo')):keep(n+'_'+suffix,x[w])
 return x
def arrays():return {n:np.asarray(x).copy() for n,x in {**P.RAW,**P.AVAILABLE,**P.DD_ARRAY_CURRENT.get('arrays',{})}.items()}
def thin(q):return {n:q[n] for n in ('file','sha256','commit_file','commit_sha256')}
def reset(stage,**context):
 P.RAW.clear();P.AVAILABLE.clear();P.DD_ARRAY_CURRENT.clear();P.CONTEXT.clear();P.CONTEXT.update(stage=stage,**context)
def initialize():
 global T,R,P,N,np,ORIGINAL_CAPTURE
 assert ADMISSION is not None and ADMISSION_SHA is not None
 assert hashlib.sha256((BASE/PROVIDER).read_bytes()).hexdigest()==PROVIDER_SHA
 spec=importlib.util.spec_from_file_location('sealed_trace_response_definitions_only',BASE/PROVIDER);T=importlib.util.module_from_spec(spec);spec.loader.exec_module(T);T.initialize()
 R,P,N,np=T.R,T.P,T.N,T.np;ORIGINAL_CAPTURE=P.capture;P.capture=keep
 P.STEM=STEM;P.__file__=__file__;P.PROTOCOL_SHA=PROTOCOL_SHA
 globals().update(path=P.path,sha=P.sha,INPUTS=P.INPUTS)
 for n,h in ((PROVIDER,PROVIDER_SHA),(KERNEL,KERNEL_SHA),(ADMISSION,ADMISSION_SHA),(STEM+'.md',PROTOCOL_SHA),(__file__,P.sha(__file__))):bind(n,h)
 for n in (KERNEL,ADMISSION):exec(compile((BASE/n).read_text(),str(BASE/n),'exec'),globals())

def load_cached_response(refs):
 reset('recover_exact_cached_trace_response_and_four_predeclared_snapshots')
 raw=P.read_pair(refs['input'],tuple(refs['input']['metadata']['schema']))
 assert len(raw)==38
 for n,x in raw.items():keep(n,x)
 b={n.removeprefix('frozen_native_'):x for n,x in raw.items() if n.startswith('frozen_native_')}
 d={n.removeprefix('frozen_metric_'):x for n,x in raw.items() if n.startswith('frozen_metric_')}
 g={n.removeprefix('original_basis_'):x for n,x in raw.items() if n.startswith('original_basis_')}
 scales=(g['native_scale'],g['metric_scale']);scale=P.pack_fields(*scales);keep('unchanged_positive_congruence',scale)
 rhs=(raw['NEW_t_target_RHS_hi'],raw['NEW_t_target_RHS_lo']);nref=raw['inherited_original_native_affine_reference'];cref=raw['inherited_original_native_canonical_reference']
 metric_reference=P.fields_from_pair(rhs,'cached_NEW_metric_reference')[1]
 assert np.all(P.fields_from_pair(rhs,'cached_zero_native_reference')[0]==0) and np.linalg.norm(metric_reference)>0 and np.all(scale>0)
 names=tuple(n+'_'+w for n in ('NEW_trace_target_final_update_updated_nodes','NEW_trace_target_final_frozen_action','NEW_trace_target_final_frozen_residual','NEW_rhs') for w in ('hi','lo'))+('NEW_trace_target_final_frozen_original_admission_scores',)
 old=P.read_pair(refs['approximation'],names)
 for n,x in old.items():keep('saved_approximation_'+n,x)
 nodes=(old['NEW_trace_target_final_update_updated_nodes_hi'],old['NEW_trace_target_final_update_updated_nodes_lo']);action=(old['NEW_trace_target_final_frozen_action_hi'],old['NEW_trace_target_final_frozen_action_lo']);residual=(old['NEW_trace_target_final_frozen_residual_hi'],old['NEW_trace_target_final_frozen_residual_lo'])
 assert nodes[0].shape==nodes[1].shape==rhs[0].shape==rhs[1].shape==(403340,)
 assert all(np.array_equal(rhs[w],old['NEW_rhs_'+('hi' if w==0 else 'lo')]) for w in (0,1))
 scores=old['NEW_trace_target_final_frozen_original_admission_scores'];assert scores.shape==(3,2) and not np.all(scores<=P.LINEAR_TOL)
 old_literal=P.read_pair(refs['readout'],tuple('complete_rate_direction_literal_full_action_'+w for w in ('hi','lo')))
 for n,x in old_literal.items():keep('saved_literal_'+n,x)
 literal=tuple(old_literal['complete_rate_direction_literal_full_action_'+w] for w in ('hi','lo'))
 snapshots={}
 for k in (40,80,120,160):
  q=refs['iterations'][k];a=P.read_pair(q,('NEW_trace_target_frozen_approximate_inverse_original_iterate',));snapshots[k]=a['NEW_trace_target_frozen_approximate_inverse_original_iterate'];keep('saved_original_iterate_%d'%k,snapshots[k])
 bound=[]
 for ref,s in ((nref,scales[0]),(cref,scales[0]),(metric_reference,scales[1])):
  raw_norm=float(np.linalg.norm(ref));white_norm=float(np.linalg.norm(ref/s));assert raw_norm>0 and white_norm>0;bound.extend((raw_norm/float(np.max(s)),white_norm))
 sufficient=P.LINEAR_TOL*min(bound);keep('unchanged_sufficient_absolute_white_target',np.asarray(sufficient))
 inp=P.checkpoint('INPUT',arrays(),dict(kind='cached_trace_response_with_four_fixed_snapshot_differences',parent_input=thin(refs['input']),parent_approximation=thin(refs['approximation']),parent_readout=thin(refs['readout']),snapshot_refs={str(k):thin(refs['iterations'][k]) for k in snapshots},prior_signed_primitive_readout=thin(refs['prior_signed_primitive_readout']),pilot_columns=[thin(q) for q in refs['pilot_columns']],fixed=refs['fixed'],owned_background=refs['owned_background'],parent_terminal=refs['terminal'],saved_proof=refs['proof'],parent_controls=refs['original_controls'],parent_canonical_response_admitted=False,unchanged_six_original_gate_references=True,zero_native_RHS_relative_ratio=None,physical_ports=None,cap=160,new_cycles=1,old_operator_geometry_fixture_or_response_replayed=False))
 return b,d,g,scales,scale,rhs,nref,cref,metric_reference,sufficient,nodes,dict(action=action,residual=residual,scores=scores,admitted=False),literal,snapshots,inp

def new_increment_column(refs,iq,y,k):
 reset('NEW_recycled_exact_increment_literal_column',column=iq)
 s,c=R.load_fixed_configuration(refs['pilot_columns'][iq]);sl=slice(iq*3784,(iq+1)*3784)
 yy=P.a_reshape(P.a_transpose(P.a_slice(y,(slice(None),sl,slice(None))),(1,0,2)),(3784,99));kk=P.a_slice(k,(sl,slice(None)))
 pair_keep('NEW_exact_increment_local_native_value',yy);pair_keep('NEW_exact_increment_local_physical_metric_value',kk)
 jets=N.paired_fixed_chart_velocity_increment(s,c,yy,kk,keep,'NEW_increment_first_jet');tangent_s=dict(s,Z=np.zeros_like(s['Z']))
 feature=N.paired_current_affine_features(tangent_s,c,jets,keep,'NEW_increment_feature');moments=N.paired_current_affine_momenta(tangent_s,c,feature,jets,keep,'NEW_increment_momentum')
 data={}
 for family,items in (('NEW_increment_first_jet',jets),('NEW_increment_feature',feature['paired']),('NEW_increment_momentum',moments)):
  for n,x in items.items():
   pair_keep(family+'_'+n,x)
   for w,suffix in enumerate(('hi','lo')):data[family+'_'+n+'_'+suffix]=np.asarray(x[w]).copy()
 for n,x in (('NEW_exact_increment_local_native_value',yy),('NEW_exact_increment_local_physical_metric_value',kk)):
  for w,suffix in enumerate(('hi','lo')):data[n+'_'+suffix]=np.asarray(x[w]).copy()
 rec=P.checkpoint('RATE_COLUMN',data,dict(kind='only_NEW_delta_minus_q_literal_rate_derivative',column=iq,pilot_ref=thin(refs['pilot_columns'][iq]),configuration_unchanged=True,affine_constant_derivative_zero=True,old_primal_or_full_response_replayed=False,original_primitive_stationarity_mismatch_resolved=False))
 return moments['native_density'],moments['metric_total_density'],rec

def new_increment_literal(increment,refs,g):
 reset('NEW_recycled_delta_minus_q_E_F_value_and_R_Z')
 vh,kh,_=P.unpack_fields(increment[0],False);vl,kl,_=P.unpack_fields(increment[1],False);data={}
 for n,fn,v,jet in (('native_value',P.dd_native_node_value,(vh,vl),0),('metric_value',P.dd_metric_node_value,(kh,kl),0),('native_R',P.dd_native_node_value,(vh,vl),1),('native_Z',P.dd_native_node_value,(vh,vl),2),('metric_R',P.dd_metric_node_value,(kh,kl),1),('metric_Z',P.dd_metric_node_value,(kh,kl),2)):
  x=fn(v,g,keep,jet=jet);pair_keep('NEW_exact_increment_'+n,x)
  for w,suffix in enumerate(('hi','lo')):data['NEW_exact_increment_'+n+'_'+suffix]=np.asarray(x[w]).copy()
  if n=='native_value':y=x
  if n=='metric_value':k=x
 values=P.checkpoint('RATE_JETS',data,dict(kind='only_NEW_exact_increment_paired_E_F_value_R_Z',parent_input=thin(refs['input']),baseline_response_unchanged=True,finite_configuration_adopted=False))
 rows=[];columns=[]
 for iq in range(4):
  pn,pm,rec=new_increment_column(refs,iq,y,k);rows.append((pn,pm));columns.append(rec)
 reset('NEW_recycled_increment_literal_global_scatter')
 pn=tuple(np.concatenate([a[0][w].reshape(3784,33,3).transpose(1,0,2) for a in rows],axis=1) for w in (0,1));pair_keep('NEW_increment_global_native_point_density',pn)
 pm=tuple(np.concatenate([a[1][w] for a in rows]) for w in (0,1));pair_keep('NEW_increment_global_metric_point_density',pm)
 native=P.dd_native_scatter(pn,g,keep);pair_keep('NEW_increment_weak_native',native)
 metric=P.dd_metric_scatter(pm,g,keep);pair_keep('NEW_increment_weak_metric',metric)
 action=P.pack_dd(native,metric);pair_keep('NEW_increment_literal_full_action',action)
 return action,columns,values

def recycled_packet(refs):
 b,d,g,scales,scale,rhs,nref,cref,mref,sufficient,nodes,current,old_literal,snapshots,inp=load_cached_response(refs)
 reset('NEW_indefinite_four_direction_recycle_method_control');fixture_meta=fresh_recycled_trace_response_control();fixture=P.checkpoint('FIXTURE',arrays(),dict(fixture_meta,controls=P.CHECKS.copy()))
 reset('NEW_four_predeclared_recycled_trace_directions')
 def action_dd(x):return P.dd_node_original_action(x,b,d,g,keep)
 def positive(x,label):return P.node_positive_envelope(x,b,d,g,label)
 def action64(x):
  v,k,_=P.unpack_fields(x,False);n,m=P.coupled_action(v,k,b,d,g);out=P.pack_fields(n,m);keep('latest_unchanged_frozen_recurrence_action',out);return out
 def scores(x,label):return T.trace_target_reference_scores(x,nref,cref,mref,scales,label)[0]
 pre=recycled_trace_preconditioner(snapshots,scale,action_dd,positive,'recycled_trace_preconditioner')
 coarse=P.checkpoint('COARSE',arrays(),dict(kind='four_predeclared_snapshot_differences_and_absolute_symmetrized_congruence_only',input_ref=thin(inp),independence_margin=pre['independence_margin'],projected_spectral_margin=pre['projected_spectral_margin'],H_asymmetry_preserved=True,physical_action_or_RHS_changed=False,directions_dropped=False,jitter_clipping_or_tolerance_relaxation=False,controls=P.CHECKS[-1:]))
 reset('one_NEW_recycled160_correction')
 updated,after,increment,solver=recycled_trace_warm_correction(nodes,current,rhs,pre,action64,action_dd,positive,scores,sufficient,'recycled_trace_warm',160)
 for n,x in (('final_paired_response',updated),('unchanged_original_RHS',rhs),('final_frozen_action',after['action']),('final_frozen_residual',after['residual']),('exact_NEW_literal_increment',increment)):pair_keep(n,x)
 keep('final_frozen_original_six_scores',after['scores'])
 response=P.checkpoint('RESPONSE',arrays(),dict(kind='one_NEW_recycled_correction_to_authenticated_nonadmitted_trace_seed',input_ref=thin(inp),coarse_ref=thin(coarse),solver=solver,parent_original_nonadmission_preserved=True,cap=160,new_cycles=1,frozen_original_rows_admitted=after['admitted'],controls=P.CHECKS[-1:]))
 new_action,columns,rate_jets=new_increment_literal(increment,refs,g)
 translated=recycled_trace_literal_translation(old_literal,new_action,rhs,after['action'],scores,'recycled_trace_literal_translation')
 readout=P.checkpoint('READOUT',arrays(),dict(kind='saved_old_literal_plus_only_NEW_exact_increment',input_ref=thin(inp),response_ref=thin(response),NEW_rate_columns=[thin(q) for q in columns],NEW_rate_jets=thin(rate_jets),old_literal_ref=thin(refs['readout']),prior_signed_primitive_readout=thin(refs['prior_signed_primitive_readout']),literal_original_six_scores=translated['scores'].tolist(),literal_original_response_admitted=translated['literal_original_response_admitted'],literal_addition_defect_retained=True,parent_original_nonadmission_preserved=True,zero_native_RHS_relative_ratio=None,primitive_stationarity_mismatch_resolved=False,configuration_changed=False,phase_direct_contact_zero=True,ordinary_direct_contact_zero=True,physical_ports=None))
 assert len(P.CHECKS)==6
 admitted=after['admitted'] and translated['literal_original_response_admitted']
 return dict(status='RECYCLED_LITERAL_TRACE_RESPONSE_ADMITTED' if admitted else 'RECYCLED_LITERAL_TRACE_RESPONSE_NOT_ADMITTED',input=inp,fixture=fixture,coarse=coarse,response=response,NEW_columns=columns,NEW_rate_jets=rate_jets,readout=readout,parent_terminal=refs['terminal'],parent_original_nonadmission_preserved=True,frozen_original_response_admitted=after['admitted'],literal_original_response_admitted=translated['literal_original_response_admitted'],original_six_gates_unchanged=True,cap=160,new_cycles=1,physical_operator_or_RHS_changed=False,finite_configuration_prepared=False,physical_adoption=False)

def outputs_recheck():
 assert P.sha(__file__)==P.OWNER['source_sha256']
 for n,h in P.OUTPUTS.items():assert P.sha(P.path(n))==h,n
def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and PROTOCOL_SHA is not None and ADMISSION is not None and ADMISSION_SHA is not None,'Held FULL reviews and root release required'
 assert not list(BASE.glob(STEM+'_*')),'Fresh exclusive namespace required'
 initialize();P.OWNER=dict(pid=os.getpid(),source_file=Path(__file__).name,source_sha256=P.sha(__file__),started_utc=P.now(),execution='root_owned_one_NEW_recycled_trace_correction');P.json_file(STEM+'_OWNER_START.json',P.OWNER)
 try:
  pins,refs=recycled_trace_admission();case=recycled_packet(refs);P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(case,owner=P.OWNER,controls=P.CHECKS,checkpoints=P.RECORDS,qualification=P.FLAGS));outputs_recheck();P.json_file(STEM+'_RECEIPT.json',dict(status='CLOSED',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),result_sha256=rh,error_sha256=None,closed_utc=P.now(),qualification=P.FLAGS));outputs_recheck();print(json.dumps(dict(status=case['status'],controls=len(P.CHECKS),pairs=len(P.RECORDS))),flush=True);return 0 if case['frozen_original_response_admitted'] and case['literal_original_response_admitted'] else 3
 except BaseException:
  raw=arrays()
  if raw:P.checkpoint('ERROR_RAW',raw,dict(kind='NEW_recycled_trace_partial_operands',context=P.CONTEXT,controls=P.CHECKS),failed=True)
  P.seal_actual();eh=P.json_file(STEM+'_ERROR.json',dict(status='FAILED',owner=P.OWNER,controls=P.CHECKS,checkpoints=P.RECORDS,context=P.CONTEXT,qualification=P.FLAGS,traceback=traceback.format_exc()));prior=BASE/(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(status='CLOSED_ERROR',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,closed_utc=P.now(),qualification=P.FLAGS));raise
if __name__=='__main__':sys.exit(main())

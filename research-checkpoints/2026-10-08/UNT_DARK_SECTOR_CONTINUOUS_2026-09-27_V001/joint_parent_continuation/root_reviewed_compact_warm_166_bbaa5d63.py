"""Guarded warm continuation of the same compact configuration rate response."""
from pathlib import Path
import importlib.util,hashlib,json,math,os,sys,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_COMPACT_CONFIGURATION_GLOBAL_RATE_RESPONSE_V002'
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='b86b9c0a6354a59244f758b528f3a0c963047c48b73673d1a4bb5d9143e9d7c5'
PARENT_PROVIDER='cross_u_compact_configuration_global_rate_response_v001.py'
PARENT_PROVIDER_SHA='99d78680bc628ff0b4eade105ab20e1c933064ff88f747c6ee06203bb10e5e93'
ADMISSION_FRAGMENT='author_fragment_compact_response_continuation_admission_v002.txt'
ADMISSION_SHA='30d6e01c6871e4b7497176414da2a7e8fb4d7ed1e92d5d52244abb56119f440b'
ADDITIONAL_CYCLES=3
R=None;P=None;np=None


def bind(name,h):
 p=Path(name);p=p if p.is_absolute() else BASE/p
 assert h is not None and P.sha(p)==h,name
 key=str(p.resolve());assert key not in P.INPUTS or P.INPUTS[key]==h;P.INPUTS[key]=h
 return p


def pair_keep(name,x):
 P.capture(name+'_hi',x[0]);P.capture(name+'_lo',x[1]);return x


def initialize():
 global R,P,np
 assert ADMISSION_FRAGMENT is not None and ADMISSION_SHA is not None
 assert hashlib.sha256((BASE/PARENT_PROVIDER).read_bytes()).hexdigest()==PARENT_PROVIDER_SHA
 spec=importlib.util.spec_from_file_location('closed_response_definition_provider',BASE/PARENT_PROVIDER);R=importlib.util.module_from_spec(spec);spec.loader.exec_module(R)
 R.initialize();P=R.P;np=R.np;R.STEM=STEM
 P.STEM=STEM;P.__file__=__file__;P.PROTOCOL_SHA=PROTOCOL_SHA
 bind(PARENT_PROVIDER,PARENT_PROVIDER_SHA);bind(ADMISSION_FRAGMENT,ADMISSION_SHA)
 globals().update(path=P.path,sha=P.sha,INPUTS=P.INPUTS,resolve_record=P.resolve_record)
 exec(compile((BASE/ADMISSION_FRAGMENT).read_text(),str(BASE/ADMISSION_FRAGMENT),'exec'),globals())


def six_term_exact_sum(terms,label):
 # Grow an error-free binary64 expansion; every low word is retained.
 assert len(terms)==6 and all(a.shape==terms[0].shape for a in terms)
 words=[]
 for ordinal,term in enumerate(terms):
  accumulator=term;next_words=[]
  for word in words:
   accumulator,low=P.a_sum(accumulator,word);next_words.append(low)
  words=next_words+[accumulator]
  P.capture(label+'_step_%d_words'%ordinal,np.stack(words))
 out=np.stack(words);P.capture(label+'_exact_expansion_words',out);return out


def add_literal_retaining_defect(old,increment,label):
 new=P.a_add(old,increment);pair_keep(label+'_sum',new)
 defect=six_term_exact_sum((old[0],old[1],increment[0],increment[1],-new[0],-new[1]),label+'_addition_defect')
 return new,defect


def restore_response(prior):
 names=('native_rate_response_hi','native_rate_response_lo','metric_rate_response_hi','metric_rate_response_lo','new_rhs_hi','new_rhs_lo','frozen_action_hi','frozen_action_lo','frozen_original_residual_hi','frozen_original_residual_lo','new_RHS_original_ratios')
 raw=P.read_pair(prior['response'],names)
 x=P.pack_dd((raw['native_rate_response_hi'],raw['native_rate_response_lo']),(raw['metric_rate_response_hi'],raw['metric_rate_response_lo']));pair_keep('restored_nodes',x)
 cycle=P.read_pair(prior['final_cycle'],tuple('response_cycle_003_final_update_updated_nodes_'+w for w in ('hi','lo')))
 for w,suffix in enumerate(('hi','lo')):assert np.array_equal(x[w],cycle['response_cycle_003_final_update_updated_nodes_'+suffix])
 rhs=(raw['new_rhs_hi'],raw['new_rhs_lo']);action=(raw['frozen_action_hi'],raw['frozen_action_lo']);res=(raw['frozen_original_residual_hi'],raw['frozen_original_residual_lo'])
 for n,v in (('restored_rhs',rhs),('restored_action',action),('restored_residual',res)):pair_keep(n,v)
 prefixes=('literal_action','literal_Gamma_trace_response','frozen_trace_response','configuration_Gamma_trace_contact','configuration_ADM_trace_contact','frozen_to_literal_tangent_bridge','combined_literal_momentum_contact','literal_bookkeeping_gap','trace_rate_bridge','combined_Gamma_trace_contact','combined_ADM_trace_contact')
 old=P.read_pair(prior['readout'],tuple(n+'_'+w for n in prefixes for w in ('hi','lo')))
 pairs={n:(old[n+'_hi'],old[n+'_lo']) for n in prefixes}
 for n,v in pairs.items():pair_keep('restored_'+n,v)
 return x,rhs,action,res,raw['new_RHS_original_ratios'],pairs


def continue_response(current,rhs,action,base_res,ratios,pairs,contact,b,d,g,scales):
 reference,field_bound=R.response_reference(rhs,scales);scale=P.pack_fields(scales[0],scales[1]);P.capture('unchanged_positive_congruence',scale)
 assert np.all(np.isfinite(scale)) and np.all(scale>0)
 literal=pairs['literal_action'];literal_trace=pairs['literal_Gamma_trace_response'];frozen_trace=pairs['frozen_trace_response'];cycles=[];tangent_refs=[]
 if np.all(ratios<=P.LINEAR_TOL):return current,action,base_res,ratios,True,cycles,literal,literal_trace,frozen_trace,tangent_refs
 for additional in range(1,ADDITIONAL_CYCLES+1):
  cycle=3+additional;label='response_continuation_%03d'%cycle;P.RAW.clear();P.AVAILABLE.clear();P.CONTEXT.update(stage='warm_same_RHS_response_continuation',cycle=cycle)
  start=current;rhs_c=P.collapse(base_res,label+'_recurrence_rhs');defect=P.a_sub(base_res,P.a_dd(rhs_c));pair_keep(label+'_recurrence_rhs_rounding_defect',defect)
  wn=float(np.linalg.norm(rhs_c/scale));assert math.isfinite(wn) and wn>0
  tolerance=P.LINEAR_TOL*field_bound/wn;P.capture(label+'_sufficient_white_tolerance',np.array(tolerance));assert math.isfinite(tolerance) and tolerance>0
  def A(delta):
   v,k,_=P.unpack_fields(delta,False);n,m=P.coupled_action(v,k,b,d,g);out=P.pack_fields(n,m);P.capture(label+'_latest_binary64_recurrence_action',out);assert np.all(np.isfinite(out));return out
  def certificate(delta):
   nodes,q3=P.dd_node_update(start,delta,P.capture,label+'_candidate_update');act,res,ra=R.response_certificate(nodes,rhs,reference,b,d,g,scales,label+'_candidate')
   return P.collapse(res,label+'_candidate_norm_only_residual'),ra
  delta,callback_ratios,ok,reason=P.minres_core(A,rhs_c,scale,tolerance,certificate,label,cap=P.CAP);P.capture(label+'_completed_correction',delta)
  current,q3=P.dd_node_update(start,delta,P.capture,label+'_final_update');action,residual,ratios=R.response_certificate(current,rhs,reference,b,d,g,scales,label+'_final')
  da=P.dd_node_original_action(P.a_dd(delta),b,d,g,P.capture);pair_keep(label+'_delta_action',da)
  qa=P.dd_node_original_action(P.a_dd(q3),b,d,g,P.capture);pair_keep(label+'_third_word_action',qa)
  prediction=P.shifted_residual_with_update_defect(base_res,da,qa);pair_keep(label+'_shift_prediction',prediction);gap=P.a_sub(residual,prediction);pair_keep(label+'_shift_identity_gap',gap)
  bound=2*(abs(rhs[0])+abs(rhs[1]))
  for role,nodes in (('start',start),('new',current),('delta',P.a_dd(delta)),('third_word',P.a_dd(q3))):bound+=P.node_positive_envelope(nodes,b,d,g,label+'_'+role);P.capture(label+'_upstream_bound_through_'+role,bound)
  actual=np.array([np.linalg.norm(a) for a in P.fields_from_pair(gap,label+'_norm_only_identity')[:2]]);env=np.array([np.linalg.norm(a) for a in P.unpack_fields(bound,False)[:2]])
  P.check(label+'_DD_response_update_with_retained_third_word',actual,np.zeros(2),env)
  increment=P.a_sum(delta,-q3);pair_keep(label+'_exact_increment',increment)
  row=dict(cycle=cycle,additional_cycle=additional,cap=P.CAP,solver_reason=reason,callback_admitted=bool(ok),new_RHS_original_ratios=ratios.tolist(),third_word_defect_retained=True,new_budget_explicit=True);cycles.append(row)
  P.checkpoint('RESPONSE_CYCLE',{**{n:a for n,a in P.AVAILABLE.items() if n.startswith(label+'_')},**{n:a for n,a in P.RAW.items() if n.startswith('control_')}},dict(kind='warm_same_RHS_response_with_original_full_DD_certificate',controls=P.CHECKS[-1:],**row))
  # Only this exact new increment is sent through the literal action derivative.
  increment_action=P.a_sub(da,qa);pair_keep(label+'_increment_frozen_action',increment_action)
  inc_literal,inc_bridge,inc_trace,refs=R.literal_rate_tangent(increment,contact,b,d,g,increment_action);tangent_refs.extend(refs)
  P.RAW.clear();P.AVAILABLE.clear();P.CONTEXT.update(stage='incremental_literal_response_accumulation',cycle=cycle)
  for name,v in (('old_literal',literal),('old_literal_trace',literal_trace),('old_frozen_trace',frozen_trace),('increment_literal',inc_literal),('increment_literal_bridge',inc_bridge),('increment_literal_trace',inc_trace),('exact_node_increment',increment)):pair_keep(label+'_'+name,v)
  literal,ldef=add_literal_retaining_defect(literal,inc_literal,label+'_literal')
  literal_trace,tdef=add_literal_retaining_defect(literal_trace,inc_trace,label+'_literal_trace')
  inc_frozen_trace=P.dd_node_trace(increment,d,g,P.capture,label+'_increment_trace');pair_keep(label+'_increment_frozen_trace',inc_frozen_trace)
  frozen_trace,fdef=add_literal_retaining_defect(frozen_trace,inc_frozen_trace,label+'_frozen_trace')
  data=dict(literal_action_hi=literal[0],literal_action_lo=literal[1],literal_Gamma_trace_response_hi=literal_trace[0],literal_Gamma_trace_response_lo=literal_trace[1],frozen_trace_response_hi=frozen_trace[0],frozen_trace_response_lo=frozen_trace[1],literal_addition_defect_words=ldef,literal_trace_addition_defect_words=tdef,frozen_trace_addition_defect_words=fdef,increment_literal_hi=inc_literal[0],increment_literal_lo=inc_literal[1],increment_literal_bridge_hi=inc_bridge[0],increment_literal_bridge_lo=inc_bridge[1],increment_nodes_hi=increment[0],increment_nodes_lo=increment[1])
  for name,a in data.items():P.capture('completed_'+name,a)
  P.checkpoint('INCREMENTAL_LITERAL',data,dict(kind='new_increment_only_literal_response_with_retained_addition_defects',cycle=cycle,tangent_refs=refs,old_literal_action_replayed=False,exact_node_increment='delta minus third_word',defect_sign='old plus increment equals new plus expansion_sum',inherited_DD_contraction_scope=True))
  base_res=residual
  if np.all(ratios<=P.LINEAR_TOL):break
 return current,action,base_res,ratios,bool(np.all(ratios<=P.LINEAR_TOL)),cycles,literal,literal_trace,frozen_trace,tangent_refs


def continuation_packet(prior,contact,node):
 b,d,g,affine,scales=R.load_frozen_system(node['system']);P.RAW.clear();P.AVAILABLE.clear()
 x,rhs,action,res,ratios,pairs=restore_response(prior)
 recovered={n:a for n,a in P.AVAILABLE.items()}
 P.checkpoint('RECOVERED_BASE',recovered,dict(kind='exact_closed_response_and_literal_readout_recovery',prior_refs={n:prior[n] for n in ('response','readout','input','final_cycle','cycle_refs')},contact_refs=contact,node_refs=node,original_budget={'cycles':3,'cap':160,'outcome':'nonadmitted'},additional_budget={'cycles':ADDITIONAL_CYCLES,'cap':160},controls_inherited_not_recounted=prior['original_controls'],original_cycles=prior['original_cycles'],phase_charge_preserved=False,configuration_updated=False))
 x,action,res,ratios,admitted,cycles,literal,literal_trace,frozen_trace,tangent_refs=continue_response(x,rhs,action,res,ratios,pairs,contact,b,d,g,scales)
 vh,kh,_=P.unpack_fields(x[0],False);vl,kl,_=P.unpack_fields(x[1],False)
 data=dict(native_rate_response_hi=vh,native_rate_response_lo=vl,metric_rate_response_hi=kh,metric_rate_response_lo=kl,new_rhs_hi=rhs[0],new_rhs_lo=rhs[1],frozen_action_hi=action[0],frozen_action_lo=action[1],frozen_original_residual_hi=res[0],frozen_original_residual_lo=res[1],new_RHS_original_ratios=ratios)
 for n,a in data.items():P.capture('completed_'+n,a)
 response=P.checkpoint('RESPONSE',data,dict(kind='warm_continued_same_RHS_global_rate_response_diagnostic',response_rows_admitted=admitted,cycles=cycles,prior_response=prior['response'],original_budget_unchanged=True,additional_budget={'cycles':ADDITIONAL_CYCLES,'cap':160},targets_changed=False,configuration_changed=False,phase_charge_preserved=False))
 P.RAW.clear();P.AVAILABLE.clear();bridge=P.a_sub(literal,action);pair_keep('completed_frozen_to_literal_tangent_bridge',bridge)
 q=(-rhs[0],-rhs[1]);combined=P.a_add(q,literal);pair_keep('completed_combined_literal_momentum_contact',combined)
 predicted=P.a_add((-res[0],-res[1]),bridge);pair_keep('completed_literal_prediction',predicted);gap=P.a_sub(combined,predicted);pair_keep('completed_literal_bookkeeping_gap',gap)
 eb=P.node_positive_envelope(x,b,d,g,'response_bookkeeping')+abs(q[0])+abs(q[1])+abs(literal[0])+abs(literal[1])+abs(bridge[0])+abs(bridge[1])+abs(res[0])+abs(res[1])
 P.check('continued_literal_response_frozen_residual_and_bridge_identity',np.array([np.linalg.norm(a) for a in P.fields_from_pair(gap,'bridge_identity_norm')[:2]]),np.zeros(2),np.array([np.linalg.norm(a) for a in P.unpack_fields(eb,False)[:2]]))
 trace_bridge=P.a_sub(literal_trace,frozen_trace);pair_keep('completed_trace_rate_bridge',trace_bridge)
 combined_Gamma=P.a_add(pairs['configuration_Gamma_trace_contact'],literal_trace);pair_keep('completed_combined_Gamma_trace_contact',combined_Gamma)
 combined_ADM=P.a_add(pairs['configuration_ADM_trace_contact'],frozen_trace);pair_keep('completed_combined_ADM_trace_contact',combined_ADM)
 values=dict(literal_action=literal,frozen_to_literal_tangent_bridge=bridge,combined_literal_momentum_contact=combined,literal_bookkeeping_gap=gap,frozen_trace_response=frozen_trace,literal_Gamma_trace_response=literal_trace,trace_rate_bridge=trace_bridge,configuration_Gamma_trace_contact=pairs['configuration_Gamma_trace_contact'],configuration_ADM_trace_contact=pairs['configuration_ADM_trace_contact'],combined_Gamma_trace_contact=combined_Gamma,combined_ADM_trace_contact=combined_ADM)
 out={}
 for name,pair in values.items():pair_keep('completed_'+name,pair);out[name+'_hi']=pair[0];out[name+'_lo']=pair[1]
 out.update({n:a for n,a in P.RAW.items() if n.startswith('control_')})
 readout=P.checkpoint('READOUT',out,dict(kind='continued_conditional_literal_bridge_and_weak_trace_response',response=response,new_tangent_refs=tangent_refs,prior_literal_readout=prior['readout'],prior_signed_primitive_readout=contact['prior_signed_primitive_readout'],original_finite_stationarity_gap_retained=True,incremental_addition_defects_retained=True,trace_target_not_imposed=True,phase_charge_held=False,physical_step=None))
 return dict(status='GLOBAL_RATE_RESPONSE_CONTINUATION_MEASURED' if admitted else 'GLOBAL_RATE_RESPONSE_CONTINUATION_NUMERICALLY_UNADMITTED',response_rows_admitted=admitted,response=response,readout=readout,cycles=cycles,new_RHS_original_ratios=ratios.tolist(),original_budget_unchanged=True,additional_budget={'cycles':ADDITIONAL_CYCLES,'cap':160},old_response=prior['response'],old_literal_replayed=False,literal_bridge_preserved=True,phase_charge_preserved=False,configuration_updated=False,physical_adoption=False)


def outputs_recheck():
 assert P.sha(__file__)==P.OWNER['source_sha256']
 for name,h in P.OUTPUTS.items():assert P.sha(P.path(name))==h,('output changed',name)


def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and PROTOCOL_SHA is not None,'Root full review and release required'
 assert not list(BASE.glob(STEM+'_*')),'Fresh exclusive output namespace required'
 initialize();bind(STEM+'.md',PROTOCOL_SHA);pins,prior,contact,node=response_continuation_admission()
 for name,h in pins.items():bind(name,h)
 P.OWNER=dict(pid=os.getpid(),source_file=Path(__file__).name,source_sha256=P.sha(__file__),started_utc=P.now(),execution='root_owned_bounded_same_RHS_warm_continuation');P.json_file(STEM+'_OWNER_START.json',P.OWNER)
 try:
  case=continuation_packet(prior,contact,node);P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(case,owner=P.OWNER,controls=P.CHECKS,checkpoints=P.RECORDS,qualification=P.FLAGS));outputs_recheck()
  P.json_file(STEM+'_RECEIPT.json',dict(status='CLOSED',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),result_sha256=rh,error_sha256=None,closed_utc=P.now(),qualification=P.FLAGS));outputs_recheck();print(json.dumps(dict(status=case['status'],controls=len(P.CHECKS),pairs=len(P.RECORDS))),flush=True)
  return 0 if case['response_rows_admitted'] else 3
 except BaseException:
  arrays={**P.RAW,**P.AVAILABLE};arrays.update(P.DD_ARRAY_CURRENT.get('arrays',{}))
  if arrays:P.checkpoint('ERROR_RAW',arrays,dict(kind='available_warm_response_or_incremental_literal_operands',context=P.CONTEXT),failed=True)
  P.seal_actual();eh=P.json_file(STEM+'_ERROR.json',dict(status='FAILED',owner=P.OWNER,input_sha256=P.INPUTS,controls=P.CHECKS,checkpoints=P.RECORDS,context=P.CONTEXT,qualification=P.FLAGS,traceback=traceback.format_exc()))
  prior_receipt=BASE/(STEM+'_RECEIPT.json');name=STEM+('_ERROR_RECEIPT.json' if prior_receipt.exists() else '_RECEIPT.json')
  P.json_file(name,dict(status='CLOSED_ERROR',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),error_sha256=eh,prior_receipt_sha256=P.sha(prior_receipt) if prior_receipt.exists() else None,closed_utc=P.now(),qualification=P.FLAGS));raise

if __name__=='__main__':sys.exit(main())

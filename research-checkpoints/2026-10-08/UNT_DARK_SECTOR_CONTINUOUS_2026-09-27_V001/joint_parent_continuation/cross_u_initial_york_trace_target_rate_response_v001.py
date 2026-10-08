"""Held NEW compact total-trace target response; frozen inverse is diagnostic."""
from pathlib import Path
import importlib.util,hashlib,json,math,os,sys,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_INITIAL_YORK_TRACE_TARGET_RATE_RESPONSE_V001'
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='793cc56c47dabc8a7baa7838b57fd95b658d655242a71e112d0d64b932ba44f7'
PROVIDER='cross_u_compact_configuration_global_rate_response_v001.py'
PROVIDER_SHA='99d78680bc628ff0b4eade105ab20e1c933064ff88f747c6ee06203bb10e5e93'
KERNEL='author_fragment_initial_york_trace_target_response_v001.py'
KERNEL_SHA='71fda02b76e03c5ac4fe917f0514a3f13e60ec15b9aad21610045fbe40fe71e1'
ADMISSION='author_fragment_compact_t_rate_response_admission_v001.py'
ADMISSION_SHA='4e8b3b5e87c122f2d3798bc851af276da9c4d399d0cf1c2e97cbd0f88718da3b'
R=P=N=np=None

def bind(n,h):
 p=Path(n);p=p if p.is_absolute() else BASE/p;assert h is not None and P.sha(p)==h,n
 key=str(p.resolve());assert key not in P.INPUTS or P.INPUTS[key]==h;P.INPUTS[key]=h;return p

def keep(n,x):return ORIGINAL_CAPTURE(n,np.asarray(x).copy())
def pair_keep(n,x):keep(n+'_hi',x[0]);keep(n+'_lo',x[1]);return x

def arrays():
 out={**P.RAW,**P.AVAILABLE,**P.DD_ARRAY_CURRENT.get('arrays',{})};return {n:np.asarray(x).copy() for n,x in out.items()}

def thin(q):return {n:q[n] for n in ('file','sha256','commit_file','commit_sha256')}

def reset(stage,**context):
 P.RAW.clear();P.AVAILABLE.clear();P.DD_ARRAY_CURRENT.clear();P.CONTEXT.clear();P.CONTEXT.update(stage=stage,**context)

def initialize():
 global R,P,N,np,ORIGINAL_CAPTURE
 assert ADMISSION is not None and ADMISSION_SHA is not None
 assert hashlib.sha256((BASE/PROVIDER).read_bytes()).hexdigest()==PROVIDER_SHA
 spec=importlib.util.spec_from_file_location('reviewed_response_definitions_only',BASE/PROVIDER);R=importlib.util.module_from_spec(spec);spec.loader.exec_module(R);R.initialize()
 P,N,np=R.P,R.N,R.np;ORIGINAL_CAPTURE=P.capture;P.capture=keep
 P.STEM=STEM;P.__file__=__file__;P.PROTOCOL_SHA=PROTOCOL_SHA
 P.FLAGS=dict(literal_primitive_stationarity_prepared=False,finite_configuration_prepared=False,normal_constraints_qualified=False,initial_CMC_qualified=False,TT_free_data_admitted=False,physical_exterior_adopted=False,evolution_qualified=False,galaxy_velocity_qualified=False,physical_adoption=False)
 globals().update(path=P.path,sha=P.sha,INPUTS=P.INPUTS)
 for n,h in ((PROVIDER,PROVIDER_SHA),(KERNEL,KERNEL_SHA),(ADMISSION,ADMISSION_SHA),(STEM+'.md',PROTOCOL_SHA),(__file__,P.sha(__file__))):bind(n,h)
 for n,h in (('authoring_initial_york_trace_target_response_146_bb895d8a.py','bb895d8a79044fc0a37cb8e9cf921d461e14d7ee70711e73543f7d15c657b07a'),('authoring_initial_york_trace_target_response_13_07f5d190.md','07f5d1907f67ba68472cef946d53036238a52ed1a114a101199332f8527ca177')):bind(n,h)
 for n in (KERNEL,ADMISSION):exec(compile((BASE/n).read_text(),str(BASE/n),'exec'),globals())

def load_new_target(refs):
 b,d,g,affine,scales=R.load_frozen_system(refs['node_system'])
 reset('retain_authenticated_frozen_preconditioner_operands')
 for family,items in (('frozen_native',b),('frozen_metric',d),('original_basis',g),('frozen_affine',affine)):
  for n,x in items.items():keep(family+'_'+n,x)
 old=P.read_pair(refs['node_compatibility'],('original_rhs','current_Pn'));inherited=P.unpack_fields(old['original_rhs'],False)[0]
 assert np.array_equal(old['current_Pn'],affine['Pn']) and np.all(scales[0]>0)
 keep('inherited_original_native_affine_reference',inherited);keep('inherited_original_native_canonical_reference',old['current_Pn'])
 raw=P.read_pair(refs['target_loads'],('t_full_coupled_target_RHS_hi','t_full_coupled_target_RHS_lo','t_weak_metric_target_hi','t_weak_metric_target_lo'))
 rhs=(raw['t_full_coupled_target_RHS_hi'],raw['t_full_coupled_target_RHS_lo']);pair_keep('NEW_t_target_RHS',rhs)
 for w in (0,1):
  native,metric,_=P.unpack_fields(rhs[w],False);assert np.all(native==0) and np.array_equal(metric,raw['t_weak_metric_target_'+('hi' if w==0 else 'lo')])
 assert np.linalg.norm(rhs[0]+rhs[1])>0
 rec=P.checkpoint('INPUT',arrays(),dict(kind='NEW_compact_total_trace_target_RHS_and_immutable_numerical_preconditioner',field='t',compact_node=[43,22],target_ref=thin(refs['target_loads']),target_input_ref=thin(refs['target_input']),frozen_system_refs=refs['node_system'],native_reference_ref=thin(refs['node_compatibility']),native_reference_names=['original_rhs native slice','current_Pn'],pilot_columns=[thin(q) for q in refs['pilot_columns']],prior_signed_primitive_readout=thin(refs['prior_readout']),primitive_canonical_readout_admitted=False,fixed=refs['fixed'],owned_background=refs['bg'],NEW_native_target_exactly_zero=True,NEW_metric_target_nonzero=True,zero_source_relative_ratio=None,configuration_unchanged=True,phase_direct_contact_zero=True,ordinary_direct_contact_zero=True,physical_ports=None,cap=160,cycles=1,native_conservative_reference_choice_fixed_before_solve=True))
 reset('NEW_independent_zero_native_source_control');return b,d,g,affine,scales,rhs,inherited,old['current_Pn'],rec

def new_rate_column(nodes,refs,iq,y,k,g):
 # Three genuinely new directions at the same supplied configuration. Full
 # words are saved once for the next action readout; no old primal is repeated.
 reset('NEW_literal_trace_target_rate_column',column=iq)
 s,c=R.load_fixed_configuration(refs['pilot_columns'][iq]);sl=slice(iq*3784,(iq+1)*3784)
 yy=P.a_reshape(P.a_transpose(P.a_slice(y,(slice(None),sl,slice(None))),(1,0,2)),(3784,99));kk=P.a_slice(k,(sl,slice(None)))
 zero_n=P.a_dd(np.zeros((3784,99)));zero_k=P.a_dd(np.zeros((3784,6)));tangent_s=dict(s,Z=np.zeros_like(s['Z']));completed={};blocks={}
 for role,native,metric in (('native_block_Mv',yy,zero_k),('mixed_block_Bk',zero_n,kk),('complete_rate_direction',yy,kk)):
  for n,x in completed.items():keep(n,x)
  jets=N.paired_fixed_chart_velocity_increment(s,c,native,metric,keep,role+'_first_jet')
  feature=N.paired_current_affine_features(tangent_s,c,jets,keep,role+'_feature');moments=N.paired_current_affine_momenta(tangent_s,c,feature,jets,keep,role+'_momenta')
  blocks[role]=(moments['native_density'],moments['metric_total_density'])
  for name,x in (('native_density',moments['native_density']),('metric_total_density',moments['metric_total_density'])):
   pair_keep(role+'_'+name,x)
   for w,suffix in enumerate(('hi','lo')):completed[role+'_'+name+'_'+suffix]=x[w].copy()
  if role=='complete_rate_direction':
   for family,items in (('NEW_rate_first_jet',jets),('NEW_rate_feature',feature['paired']),('NEW_rate_momentum',moments)):
    for n,x in items.items():
     pair_keep(family+'_'+n,x)
     for w,suffix in enumerate(('hi','lo')):completed[family+'_'+n+'_'+suffix]=x[w].copy()
  del jets,feature,moments
 native_gap=P.a_sub(blocks['complete_rate_direction'][0],P.a_add(blocks['native_block_Mv'][0],blocks['mixed_block_Bk'][0]));pair_keep('literal_native_block_addition_readout_gap',native_gap)
 metric_gap=P.a_sub(blocks['complete_rate_direction'][1],P.a_add(blocks['native_block_Mv'][1],blocks['mixed_block_Bk'][1]))
 for name,x in (('literal_native_block_addition_readout_gap',native_gap),('literal_metric_block_addition_readout_gap',metric_gap)):
  pair_keep(name,x)
  for w,suffix in enumerate(('hi','lo')):completed[name+'_'+suffix]=x[w].copy()
 for n,x in (('NEW_local_native_rate_values',yy),('NEW_local_physical_metric_rate_values',kk)):
  pair_keep(n,x)
  for w,suffix in enumerate(('hi','lo')):completed[n+'_'+suffix]=x[w].copy()
 rec=P.checkpoint('RATE_COLUMN',completed,dict(kind='NEW_literal_complete_and_uncancelled_block_temporal_derivatives',column=iq,pilot_ref=thin(refs['pilot_columns'][iq]),affine_constant_derivative_zero=True,configuration_unchanged=True,three_NEW_directions_only=True,linear_block_addition_gaps_descriptive=True,old_primal_or_response_replayed=False,original_primitive_mismatch_resolved=False))
 return blocks,completed,rec

def literal_target_readout(nodes,refs,b,d,g,scales,rhs,frozen_action,frozen_residual,native_reference,canonical_reference,metric_reference):
 reset('NEW_trace_target_response_value_and_R_Z_jets');vh,kh,_=P.unpack_fields(nodes[0],False);vl,kl,_=P.unpack_fields(nodes[1],False)
 value_data={}
 for n,fn,v,jet in (('NEW_native_rate_value',P.dd_native_node_value,(vh,vl),0),('NEW_metric_rate_value',P.dd_metric_node_value,(kh,kl),0),('NEW_native_rate_R',P.dd_native_node_value,(vh,vl),1),('NEW_native_rate_Z',P.dd_native_node_value,(vh,vl),2),('NEW_metric_rate_R',P.dd_metric_node_value,(kh,kl),1),('NEW_metric_rate_Z',P.dd_metric_node_value,(kh,kl),2)):
  x=fn(v,g,keep,jet=jet);pair_keep(n,x)
  for w,suffix in enumerate(('hi','lo')):value_data[n+'_'+suffix]=x[w].copy()
  if n=='NEW_native_rate_value':y=x
  if n=='NEW_metric_rate_value':k=x
 values=P.checkpoint('RATE_JETS',value_data,dict(kind='NEW_target_response_genuine_paired_E_F_value_R_Z',numerical_response_only=True,current_literal_derivative_qualification_pending=True,basis_ref=refs['node_system']['basis'],frozen_operator_ref=refs['node_system']))
 columns=[];parts={role:[] for role in ('native_block_Mv','mixed_block_Bk','complete_rate_direction')}
 for iq in range(4):
  blocks,completed,rec=new_rate_column(nodes,refs,iq,y,k,g);columns.append(rec)
  for role in parts:parts[role].append(blocks[role])
 reset('NEW_current_literal_original_action_certificate');literal={}
 for role,rows in parts.items():
  pn=tuple(np.concatenate([a[0][w].reshape(3784,33,3).transpose(1,0,2) for a in rows],axis=1) for w in (0,1));pm=tuple(np.concatenate([a[1][w] for a in rows]) for w in (0,1))
  n=P.dd_native_scatter(pn,g,keep);pair_keep(role+'_weak_native',n);m=P.dd_metric_scatter(pm,g,keep);pair_keep(role+'_weak_metric',m);literal[role]=P.pack_dd(n,m);pair_keep(role+'_literal_full_action',literal[role])
 action=literal['complete_rate_direction'];res=P.a_sub(rhs,action);pair_keep('NEW_current_literal_residual',res);scores,norms,zero=trace_target_reference_scores(res,native_reference,canonical_reference,metric_reference,scales,'NEW_current_literal')
 bridge=P.a_sub(action,frozen_action);pair_keep('NEW_literal_minus_frozen_derivative_remainder',bridge)
 predicted=P.a_sub(frozen_residual,bridge);pair_keep('NEW_literal_residual_prediction',predicted);gap=P.a_sub(res,predicted);pair_keep('NEW_literal_residual_bookkeeping_gap',gap)
 envelope=2*(abs(rhs[0])+abs(rhs[1])+abs(action[0])+abs(action[1])+abs(frozen_action[0])+abs(frozen_action[1])+abs(bridge[0])+abs(bridge[1])+abs(res[0])+abs(res[1])+abs(frozen_residual[0])+abs(frozen_residual[1]))
 P.check('NEW_literal_target_residual_frozen_remainder_bookkeeping',np.array([np.linalg.norm(a) for a in P.fields_from_pair(gap,'NEW_bookkeeping_norm')[:2]]),np.zeros(2),np.array([np.linalg.norm(a) for a in P.unpack_fields(envelope,False)[:2]]))
 blocknorm=[]
 for role in ('native_block_Mv','mixed_block_Bk'):
  a=P.fields_from_pair(literal[role],role+'_norm_only_action')[0];blocknorm.append((float(np.linalg.norm(a)),float(np.linalg.norm(a/scales[0]))))
 total=np.sum(np.asarray(blocknorm),axis=0);rn=norms[0,:2];diagnostic=[float(rn[i]/total[i]) if total[i]>0 else (0. if rn[i]==0 else None) for i in range(2)]
 keep('NEW_uncancelled_literal_native_Mv_Bk_raw_scaled_norms',np.asarray(blocknorm));keep('NEW_uncancelled_literal_native_reference_sum_raw_scaled',total)
 data=arrays();readout=P.checkpoint('READOUT',data,dict(kind='NEW_current_literal_target_response_and_frozen_preconditioner_remainder',columns=[thin(q) for q in columns],rate_jets=thin(values),literal_original_response_admitted=bool(np.all(scores<=P.LINEAR_TOL)),literal_original_reference_scores=scores.tolist(),absolute_residual_reference_thresholds=norms.tolist(),zero_native_RHS_relative_ratio=None,uncancelled_literal_native_backward_error_diagnostic=diagnostic,uncancelled_backward_error_is_an_admission_route=False,original_native_reference_choice_fixed=True,prior_signed_primitive_readout=thin(refs['prior_readout']),original_primitive_stationarity_mismatch_resolved=False,configuration_changed=False,phase_direct_contact_zero=True,physical_ports=None,controls=P.CHECKS[-1:]))
 return readout,columns,values,scores,bool(np.all(scores<=P.LINEAR_TOL))

def response_packet(refs):
 b,d,g,affine,scales,rhs,nref,cref,inp=load_new_target(refs);meta=fresh_trace_target_zero_native_control();fixture=P.checkpoint('FIXTURE',arrays(),dict(meta,controls=P.CHECKS.copy()))
 reset('NEW_t_target_one_bounded_numerical_approximate_inverse');nodes,action,res,scores,solver,mref=trace_target_frozen_approximate_inverse(rhs,b,d,g,scales,nref,cref)
 vh,kh,_=P.unpack_fields(nodes[0],False);vl,kl,_=P.unpack_fields(nodes[1],False);data=dict(native_rate_response_hi=vh,native_rate_response_lo=vl,metric_rate_response_hi=kh,metric_rate_response_lo=kl)
 for n,x in (('NEW_rhs',rhs),('frozen_approximation_action',action),('frozen_original_residual',res)):
  pair_keep(n,x)
  for w,suffix in enumerate(('hi','lo')):data[n+'_'+suffix]=x[w].copy()
 data.update(arrays());approx=P.checkpoint('APPROXIMATE_RESPONSE',data,dict(kind='NEW_target_frozen_signed_numerical_approximate_inverse',input_ref=thin(inp),solver=solver,frozen_original_scores=scores.tolist(),current_literal_derivative_admission_pending=True,physical_preparation=False,controls=P.CHECKS[-1:]))
 readout,columns,jets,lscores,admitted=literal_target_readout(nodes,refs,b,d,g,scales,rhs,action,res,nref,cref,mref)
 assert len(P.CHECKS)==3
 return dict(status='NEW_LITERAL_TRACE_TARGET_RESPONSE_ADMITTED' if admitted else 'NEW_LITERAL_TRACE_TARGET_RESPONSE_NOT_ADMITTED',field='t',compact_node=[43,22],input=inp,fixture=fixture,numerical_approximation=approx,columns=columns,rate_jets=jets,readout=readout,literal_original_response_admitted=admitted,literal_original_scores=lscores.tolist(),frozen_operator_is_physical_action=False,old_frozen_inverse_numerically_admitted=bool(np.all(scores<=P.LINEAR_TOL)),zero_native_RHS_relative_ratio=None,original_primitive_stationarity_mismatch_resolved=False,whole_grid_five_field_preparation=False,physical_adoption=False)

def outputs_recheck():
 assert P.sha(__file__)==P.OWNER['source_sha256']
 for n,h in P.OUTPUTS.items():assert P.sha(P.path(n))==h,n

def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and PROTOCOL_SHA is not None and ADMISSION is not None and ADMISSION_SHA is not None,'Held full review and root release required'
 assert not list(BASE.glob(STEM+'_*')),'Fresh exclusive namespace required'
 initialize();P.OWNER=dict(pid=os.getpid(),source_file=Path(__file__).name,source_sha256=P.sha(__file__),started_utc=P.now(),execution='root_owned_NEW_trace_target_rate_response');P.json_file(STEM+'_OWNER_START.json',P.OWNER)
 try:
  refs=t_rate_response_admission();case=response_packet(refs);P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(case,owner=P.OWNER,controls=P.CHECKS,checkpoints=P.RECORDS,qualification=P.FLAGS));outputs_recheck();P.json_file(STEM+'_RECEIPT.json',dict(status='CLOSED',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),result_sha256=rh,error_sha256=None,closed_utc=P.now(),qualification=P.FLAGS));outputs_recheck();print(json.dumps(dict(status=case['status'],controls=len(P.CHECKS),pairs=len(P.RECORDS))),flush=True);return 0 if case['literal_original_response_admitted'] else 3
 except BaseException:
  raw=arrays()
  if raw:P.checkpoint('ERROR_RAW',raw,dict(kind='NEW_target_inverse_or_current_literal_partial_operands',context=P.CONTEXT),failed=True)
  P.seal_actual();eh=P.json_file(STEM+'_ERROR.json',dict(status='FAILED',owner=P.OWNER,controls=P.CHECKS,checkpoints=P.RECORDS,context=P.CONTEXT,qualification=P.FLAGS,traceback=traceback.format_exc()));prior=BASE/(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(status='CLOSED_ERROR',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,closed_utc=P.now(),qualification=P.FLAGS));raise
if __name__=='__main__':sys.exit(main())

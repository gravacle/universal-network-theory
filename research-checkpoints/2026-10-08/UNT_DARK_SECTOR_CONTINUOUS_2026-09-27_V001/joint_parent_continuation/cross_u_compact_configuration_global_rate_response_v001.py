"""Guarded one-RHS frozen global Legendre response to the earned compact contact."""
from pathlib import Path
import importlib.util,hashlib,json,math,os,sys,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_COMPACT_CONFIGURATION_GLOBAL_RATE_RESPONSE_V001'
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='adebde2682b8ceb5dc0067d742a1cbba1fcdeed3a5dadbc2a02000f956d4f56b'
NODE_PROVIDER='cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py'
NODE_PROVIDER_SHA='5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18'
PRIMITIVE_PROVIDER='cross_u_paired_current_primitive_momentum_readout_v002.py'
PRIMITIVE_PROVIDER_SHA='b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19'
ADMISSION_FRAGMENT='author_fragment_compact_configuration_one_response_admission_v002.txt'
ADMISSION_SHA='5e374d66b207245c1e7bdafe6b72b1ac2a62b4f099d5c752fa0ce2d0dccfb5b4'
P=None;N=None;np=None


def bind(name,h):
 p=Path(name);p=p if p.is_absolute() else BASE/p
 assert h is not None and P.sha(p)==h,name
 key=str(p.resolve());assert key not in P.INPUTS or P.INPUTS[key]==h;P.INPUTS[key]=h
 return p


def pair_keep(name,x):
 P.capture(name+'_hi',x[0]);P.capture(name+'_lo',x[1]);return x


def initialize():
 global P,N,np
 assert ADMISSION_FRAGMENT is not None and ADMISSION_SHA is not None
 import numpy as numpy_module
 np=numpy_module
 for name,h in ((NODE_PROVIDER,NODE_PROVIDER_SHA),(PRIMITIVE_PROVIDER,PRIMITIVE_PROVIDER_SHA)):
  assert hashlib.sha256((BASE/name).read_bytes()).hexdigest()==h
 modules=[]
 for role,name in (('response_frozen_node_provider',NODE_PROVIDER),('response_literal_tangent_provider',PRIMITIVE_PROVIDER)):
  spec=importlib.util.spec_from_file_location(role,BASE/name);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);modules.append(module)
 P,N=modules;P.np=N.np=np;N.B=1.0059833281731022e-10*3.085677581491367e19/299792458.**2
 P.STEM=STEM;P.__file__=__file__;P.PROTOCOL_SHA=PROTOCOL_SHA
 P.FLAGS=dict(global_response_physical=False,configuration_preparation_admitted=False,full_normal_constraints_qualified=False,phase_charge_preserved=False,global_rank_qualified=False,evolution_qualified=False,physical_exterior_qualified=False,galaxy_velocity_qualified=False)
 for name in ('a_dd','a_add','a_sub','a_mul','a_mul64','a_prod','a_matvec','a_stack','a_slice','a_transpose','a_reshape','a_div64'):setattr(N,name,getattr(P,name))
 for name,h in ((NODE_PROVIDER,NODE_PROVIDER_SHA),(PRIMITIVE_PROVIDER,PRIMITIVE_PROVIDER_SHA),(ADMISSION_FRAGMENT,ADMISSION_SHA)):bind(name,h)
 globals().update(path=P.path,sha=P.sha,INPUTS=P.INPUTS,resolve_record=P.resolve_record)
 exec(compile((BASE/ADMISSION_FRAGMENT).read_text(),str(BASE/ADMISSION_FRAGMENT),'exec'),globals())


def load_frozen_system(system):
 # Load earned immutable operands; no original solve, feature, Gram or fixture call.
 columns=[P.read_pair(system[str(i)],('B','T','eB','eT','ih','N','mu')) for i in range(4)]
 d={n:np.concatenate([row[n] for row in columns]) for n in columns[0]}
 cr=P.read_pair(system['coefficient'],('mixing_L','modal_D','Maxwell_M0','operation_eL','operation_eD','operation_eM0'))
 b=dict(L=cr['mixing_L'],D=cr['modal_D'],M0=cr['Maxwell_M0'],eL=cr['operation_eL'],eD=cr['operation_eD'],eM0=cr['operation_eM0'])
 g=P.read_pair(system['basis'],('R','dv','hats','cell_i','cell_j','native_scale','metric_scale','scalar_scale','r','z'))
 affine=P.read_pair(system['affine'],('Pn','Pm','cn','cm','trace_rhs'))
 scales=(g['native_scale'],g['metric_scale'],g['scalar_scale'])
 return b,d,g,affine,scales


def embed_compact_contact(contact):
 row=P.read_pair(contact['loads'],('weak_native_hi','weak_native_lo','weak_metric_hi','weak_metric_lo','weak_trace_Gamma_hi','weak_trace_Gamma_lo','weak_trace_ADM_hi','weak_trace_ADM_lo'))
 n=[np.zeros((33,3,87,45)),np.zeros((33,3,87,45))];m=[np.zeros((6,87,45)),np.zeros((6,87,45))];tr={name:[np.zeros((87,45)),np.zeros((87,45))] for name in ('Gamma','ADM')}
 for w,suffix in enumerate(('hi','lo')):
  n[w][:,:,42:45,21:24]=row['weak_native_'+suffix];m[w][:,42:45,21:24]=row['weak_metric_'+suffix]
  for name in tr:tr[name][w][42:45,21:24]=row['weak_trace_'+name+'_'+suffix]
 q=P.pack_dd(tuple(n),tuple(m));pair_keep('new_compact_configuration_canonical_contact',q)
 rhs=(-q[0],-q[1]);pair_keep('new_response_rhs',rhs)
 assert np.all(n[0][...,~P.native_mask()]==0) and np.all(n[1][...,~P.native_mask()]==0)
 assert np.all(m[0][~P.metric_mask()]==0) and np.all(m[1][~P.metric_mask()]==0)
 return q,rhs,{name:tuple(x) for name,x in tr.items()}


def response_reference(rhs,scales):
 reference=rhs[0]+rhs[1];P.capture('new_response_rhs_norm_reference',reference)
 fields=P.unpack_fields(reference,False)
 bound=[]
 for field,scale in zip(fields[:2],scales[:2]):
  raw=float(np.linalg.norm(field));white=float(np.linalg.norm(field/scale));assert raw>0 and white>0 and math.isfinite(raw) and math.isfinite(white)
  bound.extend((raw/float(np.max(scale)),white))
 return reference,min(bound)


def response_certificate(x,rhs,reference,b,d,g,scales,label):
 action=P.dd_node_original_action(x,b,d,g,P.capture);pair_keep(label+'_action',action)
 residual=P.a_sub(rhs,action);pair_keep(label+'_residual',residual)
 fields=P.fields_from_pair(residual,label+'_norm_only_residual');right=P.unpack_fields(reference,False)
 ratios=np.stack([P.original_ratios(fields[i],right[i],scales[i]) for i in range(2)]);P.capture(label+'_new_RHS_original_ratios',ratios)
 return action,residual,ratios


def solve_one_response(rhs,b,d,g,scales):
 # One new physical derivative RHS; only inherited bounded numerical refinement.
 reference,field_bound=response_reference(rhs,scales);scale=P.pack_fields(scales[0],scales[1]);P.capture('unchanged_positive_congruence',scale)
 assert np.all(np.isfinite(scale)) and np.all(scale>0)
 current=P.a_dd(np.zeros(403340));base_res=rhs;cycles=[];action=P.a_dd(np.zeros(403340));ratios=np.ones((2,2))
 for cycle in range(1,P.MAX_CYCLES+1):
  label='response_cycle_%03d'%cycle;P.CONTEXT.update(stage='new_single_RHS_global_rate_response',cycle=cycle)
  start=current;rhs_c=P.collapse(base_res,label+'_recurrence_rhs');defect=P.a_sub(base_res,P.a_dd(rhs_c));pair_keep(label+'_recurrence_rhs_rounding_defect',defect)
  wn=float(np.linalg.norm(rhs_c/scale));assert math.isfinite(wn) and wn>0
  tolerance=P.LINEAR_TOL*field_bound/wn;P.capture(label+'_sufficient_white_tolerance',np.array(tolerance));assert math.isfinite(tolerance) and tolerance>0
  def A(delta):
   v,k,_=P.unpack_fields(delta,False);n,m=P.coupled_action(v,k,b,d,g);out=P.pack_fields(n,m);P.capture(label+'_latest_binary64_recurrence_action',out);assert np.all(np.isfinite(out));return out
  def certificate(delta):
   nodes,q3=P.dd_node_update(start,delta,P.capture,label+'_candidate_update');act,res,ra=response_certificate(nodes,rhs,reference,b,d,g,scales,label+'_candidate')
   return P.collapse(res,label+'_candidate_norm_only_residual'),ra
  delta,callback_ratios,ok,reason=P.minres_core(A,rhs_c,scale,tolerance,certificate,label,cap=P.CAP);P.capture(label+'_completed_correction',delta)
  current,q3=P.dd_node_update(start,delta,P.capture,label+'_final_update');action,residual,ratios=response_certificate(current,rhs,reference,b,d,g,scales,label+'_final')
  da=P.dd_node_original_action(P.a_dd(delta),b,d,g,P.capture);pair_keep(label+'_delta_action',da)
  qa=P.dd_node_original_action(P.a_dd(q3),b,d,g,P.capture);pair_keep(label+'_third_word_action',qa)
  prediction=P.shifted_residual_with_update_defect(base_res,da,qa);gap=P.a_sub(residual,prediction);pair_keep(label+'_shift_prediction',prediction);pair_keep(label+'_shift_identity_gap',gap)
  bound=2*(abs(rhs[0])+abs(rhs[1]))
  for role,nodes in (('start',start),('new',current),('delta',P.a_dd(delta)),('third_word',P.a_dd(q3))):bound+=P.node_positive_envelope(nodes,b,d,g,label+'_'+role);P.capture(label+'_upstream_bound_through_'+role,bound)
  actual=np.array([np.linalg.norm(a) for a in P.fields_from_pair(gap,label+'_norm_only_identity')[:2]]);env=np.array([np.linalg.norm(a) for a in P.unpack_fields(bound,False)[:2]])
  P.check(label+'_DD_response_update_with_retained_third_word',actual,np.zeros(2),env)
  row=dict(cycle=cycle,cap=P.CAP,solver_reason=reason,callback_admitted=bool(ok),new_RHS_original_ratios=ratios.tolist(),third_word_defect_retained=True);cycles.append(row)
  P.checkpoint('RESPONSE_CYCLE',{n:a for n,a in P.AVAILABLE.items() if n.startswith(label+'_')},dict(kind='new_RHS_response_with_original_full_DD_certificate',controls=P.CHECKS[-1:],**row))
  base_res=residual
  if np.all(ratios<=P.LINEAR_TOL):break
 return current,action,base_res,ratios,bool(np.all(ratios<=P.LINEAR_TOL)),cycles


def load_fixed_configuration(ref):
 rec=P.resolve_record(ref);schema=rec['metadata']['schema'];old={'K','Ktrace','pi_EH','p_native','p_metric_native','old_velocity'}
 names=tuple(n for n in schema if n.startswith('config_') or (n.startswith('chart_') and n.removeprefix('chart_') not in old))
 raw=P.read_pair(rec,names);s={n.removeprefix('config_'):a for n,a in raw.items() if n.startswith('config_')};c={n.removeprefix('chart_'):a for n,a in raw.items() if n.startswith('chart_')}
 return s,c


def literal_rate_tangent(x,contact,b,d,g,frozen_action):
 # Zero affine constants denote their derivative, not a changed physical source.
 vh,kh,_=P.unpack_fields(x[0],False);vl,kl,_=P.unpack_fields(x[1],False)
 y=P.dd_native_node_value((vh,vl),g,P.capture);k=P.dd_metric_node_value((kh,kl),g,P.capture)
 pair_keep('response_point_native_rates',y);pair_keep('response_point_metric_rates',k)
 native=[];metric=[];trace=[];refs=[]
 for iq,ref in enumerate(contact['pilot_columns']):
  P.RAW.clear();P.AVAILABLE.clear();P.CONTEXT.update(stage='new_literal_fixed_configuration_rate_tangent',column=iq)
  s,c=load_fixed_configuration(ref);sl=slice(iq*3784,(iq+1)*3784)
  yy=P.a_reshape(P.a_transpose(P.a_slice(y,(slice(None),sl,slice(None))),(1,0,2)),(3784,99));kk=P.a_slice(k,(sl,slice(None)))
  jets=N.paired_fixed_chart_velocity_increment(s,c,yy,kk,P.capture,'tangent_firstjets');tangent_s=dict(s,Z=np.zeros_like(s['Z']))
  feature=N.paired_current_affine_features(tangent_s,c,jets,P.capture,'tangent_feature');moments=N.paired_current_affine_momenta(tangent_s,c,feature,jets,P.capture,'tangent_momentum')
  pn=moments['native_density'];pm=moments['metric_total_density'];tt=P.a_mul64(d['mu'][sl],moments['Ktrace'])
  native.append(P.a_transpose(P.a_reshape(pn,(3784,33,3)),(1,0,2)));metric.append(pm);trace.append(tt)
  data={}
  for name,pair in (('delta_native_density',pn),('delta_metric_density',pm),('delta_Gamma_trace_density',tt)):
   pair_keep('completed_'+name,pair);data[name+'_hi']=pair[0];data[name+'_lo']=pair[1]
  rec=P.checkpoint('RATE_TANGENT',data,dict(kind='new_literal_primitive_temporal_tangent_at_held_configuration',column=iq,configuration_ref=ref,affine_constant_derivative_zero=True,primal_features_replayed=False,source_changed=False));refs.append(rec)
  del jets,feature,moments,s,c
 pn=tuple(np.concatenate([a[w] for a in native],axis=1) for w in (0,1));pm=tuple(np.concatenate([a[w] for a in metric]) for w in (0,1));tt=tuple(np.concatenate([a[w] for a in trace]) for w in (0,1))
 n=P.dd_native_scatter(pn,g,P.capture);pair_keep('literal_native_rate_response',n)
 m=P.dd_metric_scatter(pm,g,P.capture);pair_keep('literal_metric_rate_response',m)
 literal=P.pack_dd(n,m);pair_keep('literal_global_rate_tangent',literal)
 bridge=P.a_sub(literal,frozen_action);pair_keep('literal_minus_frozen_rate_tangent_bridge',bridge)
 literal_trace=P.dd_scalar_scatter(tt,g,P.capture,'literal_rate_trace');pair_keep('literal_rate_Gamma_trace',literal_trace)
 return literal,bridge,literal_trace,refs


def response_packet(contact,node):
 system=node['system'];b,d,g,affine,scales=load_frozen_system(system);P.RAW.clear();P.AVAILABLE.clear()
 q,rhs,trace_contacts=embed_compact_contact(contact)
 P.checkpoint('INPUT',dict(new_rhs_hi=rhs[0],new_rhs_lo=rhs[1]),dict(kind='one_compact_configuration_contact_global_fixed_target_response',system_refs=system,contact_refs=contact,node_refs=node,original_phase_jets_held=True,ordinary_labels_and_targets_held=True,original_finite_primitive_bridge_retained=contact['primitive_bridge'],physical_step=None,exterior_ports=None))
 x,action,res,ratios,admitted,cycles=solve_one_response(rhs,b,d,g,scales)
 vh,kh,_=P.unpack_fields(x[0],False);vl,kl,_=P.unpack_fields(x[1],False)
 data=dict(native_rate_response_hi=vh,native_rate_response_lo=vl,metric_rate_response_hi=kh,metric_rate_response_lo=kl,new_rhs_hi=rhs[0],new_rhs_lo=rhs[1],frozen_action_hi=action[0],frozen_action_lo=action[1],frozen_original_residual_hi=res[0],frozen_original_residual_lo=res[1],new_RHS_original_ratios=ratios)
 response=P.checkpoint('RESPONSE',data,dict(kind='single_new_RHS_global_rate_response_diagnostic',response_rows_admitted=admitted,cycles=cycles,targets_changed=False,configuration_changed=False,phase_charge_preserved=False))
 P.RAW.clear();P.AVAILABLE.clear();literal,bridge,literal_trace,tangent_refs=literal_rate_tangent(x,contact,b,d,g,action)
 frozen_trace=P.dd_node_trace(x,d,g,P.capture,'frozen_rate_trace');pair_keep('frozen_rate_weak_trace',frozen_trace)
 combined=P.a_add(q,literal);pair_keep('configuration_plus_literal_induced_momentum',combined)
 predicted=P.a_add((-res[0],-res[1]),bridge);gap=P.a_sub(combined,predicted);pair_keep('literal_response_bookkeeping_gap',gap)
 eb=P.node_positive_envelope(x,b,d,g,'response_bookkeeping')+abs(q[0])+abs(q[1])+abs(literal[0])+abs(literal[1])+abs(bridge[0])+abs(bridge[1])+abs(res[0])+abs(res[1])
 P.check('literal_response_frozen_residual_and_bridge_identity',np.array([np.linalg.norm(a) for a in P.fields_from_pair(gap,'bridge_identity_norm')[:2]]),np.zeros(2),np.array([np.linalg.norm(a) for a in P.unpack_fields(eb,False)[:2]]))
 out={}
 trace_bridge=P.a_sub(literal_trace,frozen_trace);pair_keep('completed_trace_rate_bridge',trace_bridge)
 combined_Gamma=P.a_add(trace_contacts['Gamma'],literal_trace);pair_keep('completed_combined_Gamma_trace_contact',combined_Gamma)
 combined_ADM=P.a_add(trace_contacts['ADM'],frozen_trace);pair_keep('completed_combined_ADM_trace_contact',combined_ADM)
 values=dict(literal_action=literal,frozen_to_literal_tangent_bridge=bridge,combined_literal_momentum_contact=combined,literal_bookkeeping_gap=gap,frozen_trace_response=frozen_trace,literal_Gamma_trace_response=literal_trace,trace_rate_bridge=trace_bridge,configuration_Gamma_trace_contact=trace_contacts['Gamma'],configuration_ADM_trace_contact=trace_contacts['ADM'],combined_Gamma_trace_contact=combined_Gamma,combined_ADM_trace_contact=combined_ADM)
 for name,pair in values.items():pair_keep('completed_'+name,pair);out[name+'_hi']=pair[0];out[name+'_lo']=pair[1]
 out.update({n:a for n,a in P.RAW.items() if n.startswith('control_')})
 readout=P.checkpoint('READOUT',out,dict(kind='conditional_literal_bridge_and_weak_trace_response',response=response,tangent_refs=tangent_refs,prior_signed_primitive_readout=contact['prior_signed_primitive_readout'],original_finite_stationarity_gap_retained=True,trace_target_not_imposed=True,phase_charge_held=False,physical_step=None))
 return dict(status='GLOBAL_RATE_RESPONSE_MEASURED' if admitted else 'GLOBAL_RATE_RESPONSE_NUMERICALLY_UNADMITTED',response_rows_admitted=admitted,response=response,readout=readout,cycles=cycles,new_RHS_original_ratios=ratios.tolist(),literal_bridge_preserved=True,phase_charge_preserved=False,configuration_updated=False,physical_adoption=False)


def outputs_recheck():
 assert P.sha(__file__)==P.OWNER['source_sha256']
 for name,h in P.OUTPUTS.items():assert P.sha(P.path(name))==h,('output changed',name)


def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and PROTOCOL_SHA is not None,'Root full review and release required'
 assert not list(BASE.glob(STEM+'_*')),'Fresh exclusive output namespace required'
 initialize();bind(STEM+'.md',PROTOCOL_SHA);pins,contact,node=response_admission()
 for name,h in pins.items():bind(name,h)
 P.OWNER=dict(pid=os.getpid(),source_file=Path(__file__).name,source_sha256=P.sha(__file__),started_utc=P.now(),execution='root_owned_single_new_compact_configuration_response')
 P.json_file(STEM+'_OWNER_START.json',P.OWNER)
 try:
  case=response_packet(contact,node);P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(case,owner=P.OWNER,controls=P.CHECKS,checkpoints=P.RECORDS,qualification=P.FLAGS));outputs_recheck()
  P.json_file(STEM+'_RECEIPT.json',dict(status='CLOSED',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),result_sha256=rh,error_sha256=None,closed_utc=P.now(),qualification=P.FLAGS));outputs_recheck();print(json.dumps(dict(status=case['status'],controls=len(P.CHECKS),pairs=len(P.RECORDS))),flush=True)
  return 0 if case['response_rows_admitted'] else 3
 except BaseException:
  arrays={**P.RAW,**P.AVAILABLE};arrays.update(P.DD_ARRAY_CURRENT.get('arrays',{}))
  if arrays:P.checkpoint('ERROR_RAW',arrays,dict(kind='available_new_response_or_literal_tangent_operands',context=P.CONTEXT),failed=True)
  P.seal_actual();eh=P.json_file(STEM+'_ERROR.json',dict(status='FAILED',owner=P.OWNER,input_sha256=P.INPUTS,controls=P.CHECKS,checkpoints=P.RECORDS,context=P.CONTEXT,qualification=P.FLAGS,traceback=traceback.format_exc()))
  prior=BASE/(STEM+'_RECEIPT.json');name=STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json')
  P.json_file(name,dict(status='CLOSED_ERROR',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,closed_utc=P.now(),qualification=P.FLAGS));raise

if __name__=='__main__':sys.exit(main())

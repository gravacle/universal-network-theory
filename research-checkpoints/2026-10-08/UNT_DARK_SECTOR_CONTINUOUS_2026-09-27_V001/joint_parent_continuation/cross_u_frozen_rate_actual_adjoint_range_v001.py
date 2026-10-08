"""Held one NEW actual-transpose diagnostic; no restart or physical admission."""
from pathlib import Path
import importlib.util,hashlib,json,math,os,sys,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_FROZEN_RATE_ACTUAL_ADJOINT_RANGE_V001'
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='a2f44c088cf83771569b117c0a3c5fc1928cfb6ed98c12e2746790c2cbc408a9'
PROVIDER='cross_u_recycled_trace_target_rate_response_v001.py'
PROVIDER_SHA='18fb6bc3a3e3ce7bf47769c1e586cf77e2530d95fac05023f32201252638c414'
KERNEL='author_fragment_frozen_rate_actual_adjoint_v002.py'
KERNEL_SHA='0b634f2398cb937c43477b967b7f0d0b8c2c35e42f3bd4b8f5700116a72da610'
ADMISSION='author_fragment_recycled_adjoint_range_admission_v001.py'
ADMISSION_SHA='6526b95d9e8715162a21547463cae90d07b355863710d05238e7662ad7b98e34'
Q=P=np=None

def bind(n,h):
 p=Path(n);p=p if p.is_absolute() else BASE/p;assert h is not None and P.sha(p)==h,n
 k=str(p.resolve());assert k not in P.INPUTS or P.INPUTS[k]==h;P.INPUTS[k]=h;return p
def keep(n,x):return ORIGINAL_CAPTURE(n,np.asarray(x).copy())
def arrays():return {n:np.asarray(x).copy() for n,x in {**P.RAW,**P.AVAILABLE,**P.DD_ARRAY_CURRENT.get('arrays',{})}.items()}
def thin(q):return {n:q[n] for n in ('file','sha256','commit_file','commit_sha256')}
def reset(stage):
 P.RAW.clear();P.AVAILABLE.clear();P.DD_ARRAY_CURRENT.clear();P.CONTEXT.clear();P.CONTEXT.update(stage=stage)
def initialize():
 global Q,P,np,ORIGINAL_CAPTURE
 assert hashlib.sha256((BASE/PROVIDER).read_bytes()).hexdigest()==PROVIDER_SHA
 spec=importlib.util.spec_from_file_location('sealed_recycled_definitions_only',BASE/PROVIDER);Q=importlib.util.module_from_spec(spec);spec.loader.exec_module(Q);Q.initialize();P,np=Q.P,Q.np
 ORIGINAL_CAPTURE=P.capture;P.capture=keep;P.STEM=STEM;P.__file__=__file__;P.PROTOCOL_SHA=PROTOCOL_SHA
 for n,h in ((PROVIDER,PROVIDER_SHA),(KERNEL,KERNEL_SHA),(ADMISSION,ADMISSION_SHA),(STEM+'.md',PROTOCOL_SHA),(__file__,P.sha(__file__))):bind(n,h)
 for n in (KERNEL,ADMISSION):exec(compile((BASE/n).read_text(),str(BASE/n),'exec'),globals())

def fixed_adjoint_candidate(residual,scale):
 actual_adjoint_put('candidate_original_saved_residual',residual)
 white=actual_adjoint_put('candidate_white_residual',P.a_div64(residual,scale,keep,'candidate_first_scale_division'))
 readout=white[0]+white[1];keep('candidate_white_norm_only_readout',readout);norm=float(np.linalg.norm(readout));keep('candidate_fixed_normalizing_norm',np.asarray(norm));assert math.isfinite(norm) and norm>0
 normal=actual_adjoint_put('candidate_normalized_white_words',P.a_div64(white,norm,keep,'candidate_norm_division'))
 w=actual_adjoint_put('candidate_actual_left_test_words',P.a_div64(normal,scale,keep,'candidate_second_scale_division'))
 scaled_w=actual_adjoint_put('candidate_scaled_words',P.a_mul64(scale,w));reconstructed=actual_adjoint_put('candidate_reconstructed_residual',P.a_mul64(scale,P.a_mul64(scale,P.a_mul64(norm,w))))
 definition_gap=actual_adjoint_put('candidate_definition_division_and_normalization_gap',P.a_sub(residual,reconstructed));definition_bound=2*(abs(residual[0])+abs(residual[1])+abs(reconstructed[0])+abs(reconstructed[1]));keep('candidate_definition_positive_bound',definition_bound)
 P.check('NEW_saved_residual_candidate_normalization_identity',definition_gap[0]+definition_gap[1],np.zeros(403340),definition_bound)
 return w,norm

def cached_adjoint_operands(refs):
 reset('selected_cached_frozen_coefficients_geometry_and_latest_saved_words')
 names=tuple('frozen_native_'+n for n in ('M0','D','L','eM0','eD','eL'))+tuple('frozen_metric_'+n for n in ('B','T','eB','eT'))+tuple('original_basis_'+n for n in ('R','dv','hats','native_scale','metric_scale'))+('NEW_t_target_RHS_hi','NEW_t_target_RHS_lo','inherited_original_native_affine_reference','inherited_original_native_canonical_reference')
 raw=P.read_pair(refs['input'],names)
 for n,x in raw.items():keep(n,x)
 b={n.removeprefix('frozen_native_'):x for n,x in raw.items() if n.startswith('frozen_native_')};d={n.removeprefix('frozen_metric_'):x for n,x in raw.items() if n.startswith('frozen_metric_')};g={n.removeprefix('original_basis_'):x for n,x in raw.items() if n.startswith('original_basis_')}
 for a in (b['eM0'],b['eD'],b['eL'],d['eB'],d['eT']):assert np.all(a>=0)
 assert g['R'].shape==g['dv'].shape==(4,3784) and np.all(g['R']>0) and np.all(g['dv']>0)
 for a in (g['native_scale'],g['metric_scale']):assert np.all(np.isfinite(a)) and np.all(a>0)
 rhs=(raw['NEW_t_target_RHS_hi'],raw['NEW_t_target_RHS_lo']);names=tuple(n+'_'+w for n in ('final_paired_response','unchanged_original_RHS','final_frozen_action','final_frozen_residual') for w in ('hi','lo'))+('final_frozen_original_six_scores',)
 saved=P.read_pair(refs['response'],names)
 for n,x in saved.items():keep('saved_'+n,x)
 pairs={n:tuple(saved[n+'_'+w] for w in ('hi','lo')) for n in ('final_paired_response','final_frozen_action','final_frozen_residual')}
 assert all(np.array_equal(rhs[w],saved['unchanged_original_RHS_'+('hi' if w==0 else 'lo')]) for w in (0,1))
 ln=tuple('recycled_trace_literal_translation_'+n+'_'+w for n in ('new_literal_action','new_literal_residual','literal_minus_frozen_derivative') for w in ('hi','lo'))+('recycled_trace_literal_translation_literal_original_scores',)
 literal=P.read_pair(refs['readout'],ln)
 for n,x in literal.items():keep('saved_'+n,x)
 assert all(pairs[n][w].shape==rhs[w].shape==(403340,) for n in pairs for w in (0,1))
 scale=P.pack_fields(g['native_scale'],g['metric_scale']);keep('unchanged_positive_coordinate_scale',scale)
 w,norm=fixed_adjoint_candidate(pairs['final_frozen_residual'],scale)
 record=P.checkpoint('INPUT',arrays(),dict(controls=P.CHECKS.copy(),candidate_normalization_words_earned=True,kind='selected_cached_frozen_polynomial_and_latest_nonadmitted_words',input_ref=thin(refs['input']),response_ref=thin(refs['response']),readout_ref=thin(refs['readout']),parent_terminal=refs['terminal'],saved_proof=refs['proof'],prior71394=refs['prior71394'],source_qualification=refs['source_qualification'],latest_six_original_gates=refs['latest_six_original_gates'],fixed=refs['fixed'],owned_background=refs['owned_background'],physical_ports=None,old_action_coarse_fixture_or_solver_replayed=False))
 return raw,b,d,g,scale,rhs,pairs,literal,w,norm,record

def diagnostic_readout(raw,b,d,g,scale,rhs,saved,literal,refs,w,norm):
 reset('fixed_latest_residual_candidate_and_NEW_actual_polynomial_adjoint')
 residual=saved['final_frozen_residual'];nodes=saved['final_paired_response'];action=saved['final_frozen_action']
 actual_adjoint_put('candidate_actual_left_test_words',w);keep('candidate_fixed_normalizing_norm',np.asarray(norm))
 scaled_w=actual_adjoint_put('candidate_scaled_words',P.a_mul64(scale,w))
 astar=actual_adjoint_put('NEW_actual_frozen_polynomial_adjoint',actual_frozen_adjoint(w,b,d,g,'NEW_actual_adjoint'))
 eadj=actual_adjoint_positive(w,b,d,g,'NEW_actual_adjoint_envelope');eforward=P.node_positive_envelope(nodes,b,d,g,'NEW_saved_nodes_positive_forward_bound');keep('NEW_saved_nodes_positive_forward_bound',eforward)
 left=actual_adjoint_dot(action,w,'saved_forward_action_pairing');right=actual_adjoint_dot(nodes,astar,'NEW_actual_adjoint_pairing');pairing_gap=actual_adjoint_put('NEW_saved_forward_actual_adjoint_gap',P.a_sub(left,right))
 wm=abs(w[0])+abs(w[1]);xm=abs(nodes[0])+abs(nodes[1]);bound=2*(np.sum(wm*eforward)+np.sum(xm*eadj));keep('NEW_global_adjoint_pairing_positive_bound',np.asarray(bound))
 P.check('NEW_saved_forward_polynomial_actual_adjoint_pairing',np.asarray(pairing_gap[0]+pairing_gap[1]),np.asarray(0.),np.asarray(bound))
 beta=actual_adjoint_dot(w,rhs,'candidate_original_RHS_projection');rho=actual_adjoint_dot(w,residual,'candidate_latest_residual_projection');alpha=actual_adjoint_dot(w,action,'candidate_saved_forward_projection')
 identity_gap=actual_adjoint_put('candidate_saved_RHS_action_residual_projection_gap',P.a_sub(P.a_sub(beta,alpha),rho));identity_bound=2*np.sum(wm*(abs(rhs[0])+abs(rhs[1])+eforward+abs(residual[0])+abs(residual[1])));keep('candidate_saved_projection_identity_positive_bound',np.asarray(identity_bound))
 P.check('NEW_saved_RHS_action_residual_projection_identity',np.asarray(identity_gap[0]+identity_gap[1]),np.asarray(0.),np.asarray(identity_bound))
 bridge=tuple(literal['recycled_trace_literal_translation_literal_minus_frozen_derivative_'+suffix] for suffix in ('hi','lo'));actual_adjoint_put('saved_literal_minus_frozen_derivative',bridge);bridge_projection=actual_adjoint_dot(w,bridge,'candidate_saved_literal_minus_frozen_action_projection')
 scaled_adjoint=actual_adjoint_put('NEW_scale_times_actual_adjoint',P.a_mul64(scale,astar));gamma=float(np.linalg.norm(scaled_adjoint[0]+scaled_adjoint[1]));gamma_error=P.TOL*float(np.linalg.norm(scale*eadj))+128*np.finfo(float).eps*float(np.linalg.norm(abs(scaled_adjoint[0])+abs(scaled_adjoint[1])));keep('NEW_adjoint_white_norm_and_construction_allowance',np.asarray((gamma,gamma_error,max(0.,gamma-gamma_error),gamma+gamma_error)))
 wn,wmfield,_=P.unpack_fields(w[0]+w[1],False);mref=P.fields_from_pair(rhs,'unchanged_metric_reference_norm_only')[1]
 nrefs=(raw['inherited_original_native_affine_reference'],raw['inherited_original_native_canonical_reference']);ns,ms=g['native_scale'],g['metric_scale']
 native_raw=P.LINEAR_TOL*min(float(np.linalg.norm(t)) for t in nrefs);native_white=P.LINEAR_TOL*min(float(np.linalg.norm(t/ns)) for t in nrefs);metric_raw=P.LINEAR_TOL*float(np.linalg.norm(mref));metric_white=P.LINEAR_TOL*float(np.linalg.norm(mref/ms))
 keep('unchanged_six_gate_absolute_thresholds',np.asarray(((native_raw,native_white),(metric_raw,metric_white))))
 allowed=min(native_raw*np.linalg.norm(wn),native_white*np.linalg.norm(ns*wn))+min(metric_raw*np.linalg.norm(wmfield),metric_white*np.linalg.norm(ms*wmfield));keep('unchanged_six_gate_allowed_test_pairing_bound',np.asarray(allowed))
 projections={}
 for role,value,target in (('total_solution',beta,rhs),('new_correction',rho,residual)):
  signed=float(value[0]+value[1]);error=P.TOL*2*float(np.sum(wm*(abs(target[0])+abs(target[1]))));lower=max(0.,abs(signed)-error-float(allowed));upper=gamma+gamma_error;necessary=lower/upper if upper>0 else None
  keep(role+'_projection_value_allowance_lower',np.asarray((signed,error,lower)));projections[role]=dict(signed_pairing=signed,construction_allowance=error,unresolved_pairing_lower=lower,necessary_white_unknown_norm_lower=necessary,unknown_solution_norm_upper=None)
 keep('candidate_scaled_norm_only',np.asarray(np.linalg.norm(scaled_w[0]+scaled_w[1])))
 return dict(kind='one_NEW_actual_adjoint_range_diagnostic',candidate='saved_final_frozen_residual_divided_by_scale_then_norm_then_scale',adjoint_white_norm=gamma,adjoint_construction_allowance=gamma_error,stored_adjoint_words_exactly_zero=bool(np.all(astar[0]==0) and np.all(astar[1]==0)),candidate_left_null_admitted=False,near_null_is_descriptive_only=True,obstruction_certified=False,conditional_necessary_norm_bounds=projections,literal_adjoint_evaluated=False,literal_minus_frozen_action_projection=float(bridge_projection[0]+bridge_projection[1]),native_global_invertibility_or_coercivity_assumed=False,source_qualification=refs['source_qualification'],original_six_gates_unchanged=True,physical_ports=None,physical_adoption=False)

def adjoint_packet(refs):
 raw,b,d,g,scale,rhs,saved,literal,w,norm,inp=cached_adjoint_operands(refs)
 reset('NEW_nonsymmetric_actual_point_transpose_independent_control');fm=fresh_actual_point_adjoint_control();fixture=P.checkpoint('FIXTURE',arrays(),dict(fm,controls=P.CHECKS.copy()))
 meta=diagnostic_readout(raw,b,d,g,scale,rhs,saved,literal,refs,w,norm);adjoint=P.checkpoint('ADJOINT',arrays(),dict(meta,input_ref=thin(inp),controls=P.CHECKS[3:]))
 data={n:np.asarray(x).copy() for n,x in P.AVAILABLE.items() if n.endswith('_value_hi') or n.endswith('_value_lo') or n in ('NEW_adjoint_white_norm_and_construction_allowance','unchanged_six_gate_absolute_thresholds','unchanged_six_gate_allowed_test_pairing_bound','candidate_scaled_norm_only') or n.endswith('_projection_value_allowance_lower')}
 readout=P.checkpoint('READOUT',data,dict(meta,input_ref=thin(inp),adjoint_ref=thin(adjoint),fixture_ref=thin(fixture),prior_signed_primitive_readout_ref=refs['input']['metadata']['prior_signed_primitive_readout'],registered_literal_range_or_gauge_admission=False,canonical_response_admitted=False,finite_configuration_prepared=False))
 assert len(P.CHECKS)==5 and len(P.RECORDS)==4
 return dict(status='ACTUAL_FROZEN_ADJOINT_DIAGNOSTIC_COMPLETE',input=inp,fixture=fixture,adjoint=adjoint,readout=readout,diagnostic=meta,parent_terminal=refs['terminal'],parent_original_nonadmission_preserved=True,canonical_response_admitted=False,obstruction_certified=False,physical_adoption=False)

def outputs_recheck():
 assert P.sha(__file__)==P.OWNER['source_sha256']
 for n,h in P.OUTPUTS.items():assert P.sha(P.path(n))==h,n
def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and PROTOCOL_SHA is not None,'Held FULL reviews and root release required'
 assert not list(BASE.glob(STEM+'_*')),'Fresh exclusive namespace required'
 initialize();P.OWNER=dict(pid=os.getpid(),source_file=Path(__file__).name,source_sha256=P.sha(__file__),started_utc=P.now(),execution='root_owned_one_NEW_actual_adjoint_range_diagnostic');P.json_file(STEM+'_OWNER_START.json',P.OWNER)
 try:
  pins,refs=adjoint_range_admission();case=adjoint_packet(refs);P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(case,owner=P.OWNER,controls=P.CHECKS,checkpoints=P.RECORDS,qualification=P.FLAGS));outputs_recheck();P.json_file(STEM+'_RECEIPT.json',dict(status='CLOSED',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),result_sha256=rh,error_sha256=None,closed_utc=P.now(),qualification=P.FLAGS));outputs_recheck();print(json.dumps(dict(status=case['status'],controls=len(P.CHECKS),pairs=len(P.RECORDS))),flush=True);return 0
 except BaseException:
  raw=arrays()
  if raw:P.checkpoint('ERROR_RAW',raw,dict(kind='NEW_actual_adjoint_partial_operands',context=P.CONTEXT,controls=P.CHECKS),failed=True)
  P.seal_actual();eh=P.json_file(STEM+'_ERROR.json',dict(status='FAILED',owner=P.OWNER,controls=P.CHECKS,checkpoints=P.RECORDS,context=P.CONTEXT,qualification=P.FLAGS,traceback=traceback.format_exc()));prior=BASE/(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(status='CLOSED_ERROR',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,closed_utc=P.now(),qualification=P.FLAGS));raise
if __name__=='__main__':sys.exit(main())

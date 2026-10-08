"""Held one coupled nonsymmetric paired GMRES; root alone releases numerical work."""
from pathlib import Path
import importlib.util,hashlib,json,os,sys,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_NATIVE_METRIC_STAR_PAIRED_TRACE_GMRES_V002'
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='976ef7b27f08731576217a89c45035322182adf3ea00bcbb44b40f5062afbe09'
PROVIDER='cross_u_recycled_trace_target_rate_response_v001.py'
PROVIDER_SHA='18fb6bc3a3e3ce7bf47769c1e586cf77e2530d95fac05023f32201252638c414'
METHOD='author_fragment_native_metric_star_paired_gmres_v001.py'
METHOD_SHA='3ba68a8916f94a2ffc5fb3d66e72cf66c6ab249d2941a658f3003b70f8e04770'
STAR='author_fragment_native_metric_star_preconditioner_v004.py'
STAR_SHA='076261aa0d8666182890418b7808f5149a3e59f77c0ceff4876875265700125a'
ADMISSION='author_fragment_latest_trace_response_seed_admission_v001.py'
ADMISSION_SHA='2ed47497843961a2a9182c20d68e43440296f4df6c3911dde94762866137c566'
FRESH='author_fragment_fresh_native_metric_star_gmres_control_v001.py'
FRESH_SHA='1a616e2335755dcf1796fe3166d9a89dbf0d2422ce06b69b1119fc073d029b43'
FACTOR_PROOF='READONLY_SAVED_STAR_BALANCED_CLOSURE_V001_RESULT.json'
FACTOR_PROOF_SHA='d6e0196a2f04f1d7c6fa88d53de52d079565868833da68665a5cba05abcd41c3'
C=T=R=P=N=np=None

def bind(n,h):
 p=Path(n);p=p if p.is_absolute() else BASE/p;assert h is not None and P.sha(p)==h,n
 key=str(p.resolve());assert key not in P.INPUTS or P.INPUTS[key]==h;P.INPUTS[key]=h;return p

def keep(n,x):return ORIGINAL_CAPTURE(n,np.asarray(x).copy())
def pair_keep(n,x):keep(n+'_hi',x[0]);keep(n+'_lo',x[1]);return x
def arrays():return {n:np.asarray(x).copy() for n,x in {**P.RAW,**P.AVAILABLE,**P.DD_ARRAY_CURRENT.get('arrays',{})}.items()}
def thin(q):return {n:q[n] for n in ('file','sha256','commit_file','commit_sha256')}
def reset(stage,**context):
 P.RAW.clear();P.AVAILABLE.clear();P.DD_ARRAY_CURRENT.clear();P.CONTEXT.clear();P.CONTEXT.update(stage=stage,**context)

def initialize():
 global C,T,R,P,N,np,ORIGINAL_CAPTURE
 assert hashlib.sha256((BASE/PROVIDER).read_bytes()).hexdigest()==PROVIDER_SHA
 spec=importlib.util.spec_from_file_location('latest_trace_definitions_only',BASE/PROVIDER);C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C);C.initialize()
 T,R,P,N,np=C.T,C.R,C.P,C.N,C.np;ORIGINAL_CAPTURE=C.ORIGINAL_CAPTURE;P.capture=keep;P.STEM=STEM;P.__file__=__file__;P.PROTOCOL_SHA=PROTOCOL_SHA
 assert not P.CHECKS and not P.RECORDS and not P.OUTPUTS and all(v is False for v in P.FLAGS.values())
 for n,h in ((PROVIDER,PROVIDER_SHA),(METHOD,METHOD_SHA),(STAR,STAR_SHA),(ADMISSION,ADMISSION_SHA),(FRESH,FRESH_SHA),(STEM+'.md',PROTOCOL_SHA),(__file__,P.sha(__file__))):bind(n,h)
 for n in (STAR,METHOD,ADMISSION,FRESH):exec(compile((BASE/n).read_text(),str(BASE/n),'exec'),globals())
 assert NATIVE_METRIC_GMRES_AUTHOR_DRAFT is True and NATIVE_METRIC_GMRES_AUTHORING_IN_PROGRESS is False

def factor_admission():
 stem='CROSS_U_NATIVE_METRIC_STAR_PRECONDITIONER_PREPARATION_V004';source='cross_u_native_metric_star_preconditioner_preparation_v004.py';sh='baba0601348770ee6461b4abc9fc368addb3ecba3f8c1842c3bea4781d7e26e0';ph='1b1c1586bd5989686768504aeb6ff391a989702a1938a9e3365711376a374e9b'
 terminal=dict(pid=81895,result_sha256='545294354b3af026eeb84422c7d2e710e57281ca29f884639a5c77f09c86f7c0',receipt_sha256='86b782cc94a3e15b88e3a126980fb9ee9f647a2a815af47b68be61111b45eddb',error_sha256=None)
 for n,h in ((source,sh),(stem+'.md',ph),(stem+'_RESULT.json',terminal['result_sha256']),(stem+'_RECEIPT.json',terminal['receipt_sha256']),(FACTOR_PROOF,FACTOR_PROOF_SHA)):bind(n,h)
 r=json.loads(P.path(stem+'_RESULT.json').read_text());rc=json.loads(P.path(stem+'_RECEIPT.json').read_text());proof=json.loads(P.path(FACTOR_PROOF).read_text())
 assert rc['status']=='CLOSED' and rc['result_sha256']==terminal['result_sha256'] and rc.get('error_sha256') is None and r['owner']==rc['owner'] and r['owner']['pid']==81895 and r['owner']['source_sha256']==sh
 assert r['status']=='SAVED_COMPLETED_STAR_BALANCED_NORMWISE_CONSTRUCTION_PASS' and r['new_candidate_factor_certified'] is True and r['original_failed_control_preserved'] is True and r['original_componentwise_control_12_passed'] is False and len(r['controls'])==15 and r['controls'][12]['passed'] is False and all(c['passed'] for c in r['controls'][:12]+r['controls'][13:])
 assert r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values()) and r['physical_adoption'] is False and r['fine_action_or_RHS_or_original_six_gates_changed'] is False
 assert proof['status']=='SAVED_COMPLETED_STAR_BALANCED_NORMWISE_CLOSURE_PASS' and proof['parent']==terminal and proof['owner_pid']==82970 and proof['committed_pairs']==5 and proof['total_controls']==15 and proof['original_componentwise_control_12_passed'] is False and proof['new_normwise_controls']==2 and proof['new_candidate_factor_certified'] is True and proof['source_qualification']==r['qualification'] and proof['physical_adoption'] is False
 refs={}
 for role in ('input','factor'):
  q=r[role];assert q in r['checkpoints']
  for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert rc['output_sha256'][n]==h;bind(n,h)
  cm=json.loads(P.path(q['commit_file']).read_text());assert cm=={n:q[n] for n in ('file','sha256','metadata')} and cm['metadata']['owner']==r['owner'] and cm['metadata']['qualification']==r['qualification'] and cm['metadata']['failed'] is False
  refs[role]=dict(cm,commit_file=q['commit_file'],commit_sha256=q['commit_sha256'])
 assert proof['factor_ref']==thin(refs['factor']) and len(refs['input']['metadata']['schema'])==88
 for name,shape,dtype in (('L',(32,3915,3,3),'float64'),('V',(32,3915,3,6),'float64'),('D_factor',(32,3915,3,3),'float64'),('D_symmetric',(32,3915,3,3),'float64'),('K_factor',(3915,9,9),'float64'),('K_symmetric',(3915,9,9),'float64'),('C',(3915,3,6),'float64'),('S',(3915,6,6),'float64'),('basis_scale',(3915,3),'float64'),('native_mask',(3915,3),'bool'),('metric_mask',(3915,6),'bool')):assert refs['factor']['metadata']['schema']['NEW_star_preconditioner_'+name]==dict(shape=list(shape),dtype=dtype,finite=True)
 refs.update(terminal=terminal,proof=dict(file=FACTOR_PROOF,sha256=FACTOR_PROOF_SHA,status=proof['status']),original_failed_control=r['controls'][12],new_normwise_controls=r['controls'][13:],original_parent=r['parent_terminal']);return refs

def load_warm(refs,factor):
 reset('exact_latest_trace_and_earned_factor_recovery')
 raw=P.read_pair(refs['input'],tuple(refs['input']['metadata']['schema']))
 for n,x in raw.items():keep(n,x)
 old=P.read_pair(refs['response'],tuple(n+'_'+w for n in ('final_paired_response','unchanged_original_RHS','final_frozen_action','final_frozen_residual') for w in ('hi','lo'))+('final_frozen_original_six_scores',))
 for n,x in old.items():keep('latest_GMRES_seed_'+n,x)
 literal=P.read_pair(refs['readout'],tuple('recycled_trace_literal_translation_'+n+'_'+w for n in ('new_literal_action','new_literal_residual','literal_minus_frozen_derivative') for w in ('hi','lo'))+('recycled_trace_literal_translation_literal_addition_defect_exact_expansion','recycled_trace_literal_translation_literal_original_scores'))
 for n,x in literal.items():keep('latest_GMRES_literal_'+n,x)
 fi=P.read_pair(factor['input'],tuple(factor['input']['metadata']['schema']))
 for n,x in fi.items():keep('certified_STAR_input_'+n,x)
 shared=sorted(set(raw)&set(fi));assert len(raw)==111 and len(shared)==76 and all(np.array_equal(raw[n],fi[n]) for n in shared)
 names=tuple('NEW_star_preconditioner_'+n for n in ('L','V','D_factor','K_factor','D_symmetric','K_symmetric','C','S','basis_scale','native_mask','metric_mask'));fp=P.read_pair(factor['factor'],names)
 for n,x in fp.items():keep('certified_STAR_'+n,x)
 pre={n.removeprefix('NEW_star_preconditioner_'):x for n,x in fp.items()};assert np.all(pre['basis_scale']>0)
 b={n.removeprefix('frozen_native_'):x for n,x in raw.items() if n.startswith('frozen_native_')};d={n.removeprefix('frozen_metric_'):x for n,x in raw.items() if n.startswith('frozen_metric_')};g={n.removeprefix('original_basis_'):x for n,x in raw.items() if n.startswith('original_basis_')}
 rhs=(raw['NEW_t_target_RHS_hi'],raw['NEW_t_target_RHS_lo']);nodes=tuple(old['final_paired_response_'+w] for w in ('hi','lo'));act=tuple(old['final_frozen_action_'+w] for w in ('hi','lo'));res=tuple(old['final_frozen_residual_'+w] for w in ('hi','lo'))
 assert all(np.array_equal(rhs[w],old['unchanged_original_RHS_'+('hi' if w==0 else 'lo')]) for w in (0,1)) and nodes[0].shape==nodes[1].shape==rhs[0].shape==rhs[1].shape==(403340,)
 rows=old['final_frozen_original_six_scores'];assert rows.shape==(3,2) and not np.all(rows<=P.LINEAR_TOL)
 scales=(g['native_scale'],g['metric_scale']);nref=raw['inherited_original_native_affine_reference'];cref=raw['inherited_original_native_canonical_reference'];mref=P.fields_from_pair(rhs,'unchanged_NEW_metric_reference')[1]
 assert np.all(P.fields_from_pair(rhs,'zero_native_RHS_undefined_relative_reference')[0]==0) and np.linalg.norm(mref)>0 and np.linalg.norm(nref)>0 and np.linalg.norm(cref)>0 and all(np.all(s>0) for s in scales)
 old_literal=tuple(literal['recycled_trace_literal_translation_new_literal_action_'+w] for w in ('hi','lo'))
 inp=P.checkpoint('INPUT',arrays(),dict(kind='latest_nonadmitted_paired_trace_seed_and_earned_STAR_factor_only',latest_input=thin(refs['input']),latest_response=thin(refs['response']),latest_literal_readout=thin(refs['readout']),factor_input=thin(factor['input']),factor=thin(factor['factor']),latest_terminal=refs['terminal'],latest_proof=refs['proof'],factor_terminal=factor['terminal'],factor_proof=factor['proof'],all111_latest_INPUT_fields_bitcopied=True,shared76_fields_bitwise_equal=True,latest_solution_prefix='latest_GMRES_seed_',latest_literal_prefix='latest_GMRES_literal_',factor_input_prefix='certified_STAR_input_',factor_array_prefix='certified_STAR_',factor_original_failed_control=factor['original_failed_control'],factor_new_normwise_controls=factor['new_normwise_controls'],pilot_columns=[thin(q) for q in refs['pilot_columns']],prior_signed_primitive_readout=thin(refs['prior_signed_primitive_readout']),fixed=refs['fixed'],owned_background=refs['bg'],prior_nonadmissions_preserved=True,zero_native_RHS_relative_ratio=None,cap=80,checkpoints=(20,40,80),restarts=0,physical_ports=None,physical_adoption=False))
 return b,d,g,scales,rhs,nref,cref,mref,nodes,dict(action=act,residual=res,scores=rows,admitted=False),old_literal,pre,inp

def star_positive(x,pre,adjoint=False):
 fields=P.unpack_fields(abs(x[0])+abs(x[1]),False);n=fields[0].transpose(0,2,3,1).reshape(33,3915,3)*pre['native_mask'][None];k=fields[1].transpose(1,2,0).reshape(3915,6)*pre['metric_mask'];mm=lambda a,v:np.einsum('...ij,...j->...i',abs(a),v)
 if not adjoint:
  uk=mm(pre['K_factor'],np.concatenate((n[0],k),axis=-1));u,k=uk[:,:3],uk[:,3:];z=mm(pre['D_factor'],n[1:])+mm(pre['L'],u)+mm(pre['V'],k);n=np.concatenate((u[None],z),axis=0)/pre['basis_scale'][None]
 else:
  n=n/pre['basis_scale'][None];m=n[1:];u=n[0]+np.sum(mm(pre['L'].swapaxes(-1,-2),m),axis=0);k=k+np.sum(mm(pre['V'].swapaxes(-1,-2),m),axis=0);uk=mm(pre['K_factor'].swapaxes(-1,-2),np.concatenate((u,k),axis=-1));n=np.concatenate((uk[:,:3][None],mm(pre['D_factor'].swapaxes(-1,-2),m)),axis=0);k=uk[:,3:]
 n*=pre['native_mask'][None];k*=pre['metric_mask'];out=P.pack_fields(n.reshape(33,87,45,3).transpose(0,3,1,2),k.reshape(87,45,6).transpose(2,0,1));assert np.all(np.isfinite(out)) and np.all(out>=0);return out

def actual_star_transpose_control(pre):
 label='NEW_saved_STAR_actual_transpose';indices=np.arange(403340);x=(np.ldexp(np.where(indices%2==0,1.,-1.),-(indices%4+2)),np.zeros(403340));y=(np.ldexp(np.where(indices%3==0,-1.,1.),-(indices%5+3)),np.zeros(403340));pair_keep(label+'_fixed_x',x);pair_keep(label+'_fixed_y',y)
 fx=native_metric_gmres_star_full(x,pre,label+'_forward');aty=native_metric_gmres_star_full(y,pre,label+'_transpose',True);lhs=native_metric_gmres_dot(fx,y,label+'_left');rhs=native_metric_gmres_dot(x,aty,label+'_right');gap=pair_keep(label+'_bilinear_contact',P.a_sub(lhs,rhs))
 ef=star_positive(x,pre);keep(label+'_forward_positive_envelope',ef);ea=star_positive(y,pre,True);keep(label+'_transpose_positive_envelope',ea);bound=float(np.sum(ef*(abs(y[0])+abs(y[1]))+(abs(x[0])+abs(x[1]))*ea));keep(label+'_upstream_bilinear_operation_bound',np.asarray(bound));assert bound>0
 P.check(label+'_actual_bilinear_adjoint_construction',np.asarray(gap[0]+gap[1]),np.asarray(0.),np.asarray(bound));return dict(kind='NEW_saved_STAR_forward_actual_transpose_contact',global_inverse_or_coercivity_claimed=False)

def gmres_packet(refs,factor):
 b,d,g,scales,rhs,nref,cref,mref,nodes,current,old_literal,pre,inp=load_warm(refs,factor)
 reset('NEW_nonsymmetric_anisotropic_GMRES_control');fresh=fresh_native_metric_star_gmres_control();fixture=P.checkpoint('FIXTURE',arrays(),dict(fresh,controls=P.CHECKS.copy()))
 reset('NEW_actual_saved_STAR_transpose_contact');contact=actual_star_transpose_control(pre);congruence=P.checkpoint('CONGRUENCE',arrays(),dict(contact,factor_ref=thin(factor['factor']),controls=P.CHECKS[-1:],no_old_factor_or_action_replayed=True))
 reset('one_NEW_coupled_paired_GMRES80')
 def action(x,label):
  pair_keep(label+'_trial_nodes',x);a=P.dd_node_original_action(x,b,d,g,keep);return pair_keep(label+'_completed_fine_action',a)
 def positive(x,label):return P.node_positive_envelope(x,b,d,g,label)
 def scores(x,label):return T.trace_target_reference_scores(x,nref,cref,mref,scales,label)[0]
 def forward(x,label):return native_metric_gmres_star_full(x,pre,label)
 def adjoint(x,label):return native_metric_gmres_star_full(x,pre,label,True)
 iterations=[]
 def progress(k,x,after,increment):
  for n,pair in (('GMRES_current_nodes',x),('GMRES_current_original_action',after['action']),('GMRES_current_original_residual',after['residual']),('GMRES_current_exact_increment',increment)):pair_keep(n,pair)
  keep('GMRES_current_original_six_scores',after['scores']);iterations.append(P.checkpoint('ITERATION',arrays(),dict(kind='unrestarted_paired_GMRES_original_candidate_and_full_Arnoldi_state',iteration=k,cap=80,input_ref=thin(inp),original_six_rows_admitted=after['admitted'],controls=P.CHECKS.copy(),original_gates_unchanged=True,physical_adoption=False)))
 updated,after,increment,meta=native_metric_gmres_solve(nodes,current,rhs,forward,adjoint,action,positive,scores,'coupled_STAR_GMRES',80,progress)
 for n,x in (('final_paired_response',updated),('unchanged_original_RHS',rhs),('final_frozen_action',after['action']),('final_frozen_residual',after['residual']),('exact_NEW_literal_increment',increment)):pair_keep(n,x)
 keep('final_frozen_original_six_scores',after['scores']);response=P.checkpoint('RESPONSE',arrays(),dict(kind='one_NEW_unrestarted_coupled_STAR_GMRES80',input_ref=thin(inp),factor_ref=thin(factor['factor']),solver=meta,frozen_original_rows_admitted=after['admitted'],controls=P.CHECKS[6:],old_response_primal_factor_fixture_or_solve_replayed=False))
 new_action,columns,rate_jets=C.new_increment_literal(increment,refs,g)
 translated=C.recycled_trace_literal_translation(old_literal,new_action,rhs,after['action'],scores,'STAR_GMRES_literal_translation')
 readout=P.checkpoint('READOUT',arrays(),dict(kind='cached_latest_literal_plus_only_NEW_exact_GMRES_increment',input_ref=thin(inp),response_ref=thin(response),NEW_rate_columns=[thin(q) for q in columns],NEW_rate_jets=thin(rate_jets),old_literal_ref=thin(refs['readout']),prior_signed_primitive_readout=thin(refs['prior_signed_primitive_readout']),literal_original_six_scores=translated['scores'].tolist(),literal_original_response_admitted=translated['literal_original_response_admitted'],literal_addition_defect_retained=True,old_literal_addition_defect_preserved_in_INPUT=True,original_primitive_stationarity_mismatch_resolved=False,configuration_changed=False,phase_direct_contact_zero=True,ordinary_direct_contact_zero=True,zero_native_RHS_relative_ratio=None,physical_ports=None,physical_adoption=False))
 admitted=after['admitted'] and translated['literal_original_response_admitted'];assert all(c['passed'] for c in P.CHECKS)
 return dict(status='STAR_GMRES_LITERAL_TRACE_RESPONSE_ADMITTED' if admitted else 'STAR_GMRES_LITERAL_TRACE_RESPONSE_NOT_ADMITTED',input=inp,fixture=fixture,congruence=congruence,iterations=iterations,response=response,NEW_columns=columns,NEW_rate_jets=rate_jets,readout=readout,parent_terminal=refs['terminal'],factor_terminal=factor['terminal'],factor_proof=factor['proof'],solver=meta,frozen_original_response_admitted=after['admitted'],literal_original_response_admitted=translated['literal_original_response_admitted'],original_six_gates_unchanged=True,cap=80,restarts=0,finite_configuration_prepared=False,physical_adoption=False)

def outputs_recheck():
 assert P.sha(__file__)==P.OWNER['source_sha256']
 for n,h in P.OUTPUTS.items():assert P.sha(P.path(n))==h,n

def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and PROTOCOL_SHA is not None and FACTOR_PROOF_SHA is not None,'Held FULL review and root release required'
 assert not list(BASE.glob(STEM+'_*')),'Fresh exclusive namespace required'
 initialize();P.OWNER=dict(pid=os.getpid(),source_file=Path(__file__).name,source_sha256=P.sha(__file__),started_utc=P.now(),execution='root_owned_NEW_nonsymmetric_coupled_STAR_GMRES80');P.json_file(STEM+'_OWNER_START.json',P.OWNER)
 try:
  pins,refs=latest_trace_response_admission();factor=factor_admission();case=gmres_packet(refs,factor);P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(case,owner=P.OWNER,controls=P.CHECKS,checkpoints=P.RECORDS,qualification=P.FLAGS));outputs_recheck();P.json_file(STEM+'_RECEIPT.json',dict(status='CLOSED',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),result_sha256=rh,error_sha256=None,closed_utc=P.now(),qualification=P.FLAGS));outputs_recheck();print(json.dumps(dict(status=case['status'],controls=len(P.CHECKS),pairs=len(P.RECORDS))),flush=True);return 0 if case['frozen_original_response_admitted'] and case['literal_original_response_admitted'] else 3
 except BaseException:
  raw=arrays()
  if raw:P.checkpoint('ERROR_RAW',raw,dict(kind='NEW_coupled_STAR_GMRES_partial_words',context=P.CONTEXT,controls=P.CHECKS),failed=True)
  P.seal_actual();eh=P.json_file(STEM+'_ERROR.json',dict(status='FAILED',owner=P.OWNER,controls=P.CHECKS,checkpoints=P.RECORDS,context=P.CONTEXT,qualification=P.FLAGS,traceback=traceback.format_exc()));prior=BASE/(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(status='CLOSED_ERROR',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,closed_utc=P.now(),qualification=P.FLAGS));raise
if __name__=='__main__':sys.exit(main())

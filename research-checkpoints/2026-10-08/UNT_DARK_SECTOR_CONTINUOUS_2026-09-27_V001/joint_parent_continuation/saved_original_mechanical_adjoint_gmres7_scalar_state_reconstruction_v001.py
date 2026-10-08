"""HELD lost original117 adjoint MGS/QR state reconstruction from CLOSED37897.
New scalar arithmetic only; no Kstar/action/factor/producer/old control replay.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='SAVED_ORIGINAL_MECHANICAL_ADJOINT_GMRES7_SCALAR_STATE_RECONSTRUCTION_V001'
DRIVER_PROTOCOL='SAVED_ORIGINAL_MECHANICAL_ADJOINT_GMRES7_SCALAR_STATE_RECONSTRUCTION_V001.md'
PROTOCOL_SHA='ccc1a45a1e085e000a7f8a79512d0e9d6b3940a07e3e5662debb2cadf081e42b'
OLD_STEM='CROSS_U_CANDIDATE_RIGHT_ONLY_MECHANICAL_ADJOINT_RESPONSE_V003'
OLD_SOURCE=('cross_u_candidate_right_only_mechanical_adjoint_response_v003.py','720ab9f4bad4a39a1c44e93acb22a8c4dd5ead032598503bec93774c6cab969b')
OLD_MANIFEST=(OLD_STEM+'_MANIFEST.json','2e9b4a997a381a7afcbdf23e92f50f8a2842c9562a956cd8cb857511a7d1f71a')
OLD_PROTOCOL=('CANDIDATE_RIGHT_ONLY_MECHANICAL_ADJOINT_RESPONSE_V001.md','8e2fcafa2722c0aed693c169e8a7accd3d0e07d7be13ca0b44b0cd8e0c898133')
SELECTED_OUTPUT_PROOF=('READONLY_CLOSED_ADJOINT7_SELECTED_PREFIX_BYTE_SEALS_V001.json','457d33990eb54213e087515e96b6a9bd2f0bf1f11ce17449991898bd02c572b0','READONLY_CLOSED_ADJOINT7_SELECTED_PREFIX_BYTE_SEALS_VERIFIED')
FIRST_CHUNK_OUTPUT_PROOF=(None,None,None)
MANIFEST_INPUT_COVERAGE_PROOF=(None,None,None)
IO_PARENT='cross_u_finite0_candidate_action_residual_v007.py'
IO_PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
PINS={'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18','cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19','author_fragment_native_metric_star_paired_gmres_v001.py':'3ba68a8916f94a2ffc5fb3d66e72cf66c6ab249d2941a658f3003b70f8e04770','author_fragment_candidate_right_only_mechanical_adjoint_gmres_v002.py':'25747c25adfeda383c2f862352f0066010abefb79a2c06bdd1e6e6172dedb35c','author_fragment_exact_exponent_two_product_v003.py':'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235','author_fragment_single_decode_recheck_v001.py':'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d'}
CAP=80;PREFIX=7;N=403340
np=P=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={}
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)


def definitions(file,names):
 t=ast.parse((BASE/file).read_text());d=[n for n in t.body if isinstance(n,ast.FunctionDef) and n.name in names];assert {n.name for n in d}==set(names);return ast.Module(body=d,type_ignores=[])

def initialize():
 global np
 assert hashlib.sha256((BASE/IO_PARENT).read_bytes()).hexdigest()==IO_PARENT_SHA
 for n,h in PINS.items():assert hashlib.sha256((BASE/n).read_bytes()).hexdigest()==h,n
 names={'bind','keep','arrays','thin','clear_current','initialize_io'}
 exec(compile(definitions(IO_PARENT,names),IO_PARENT,'exec'),globals());initialize_io()
 import numpy as numpy
 np=numpy;SCOPE['np']=np
 arithmetic={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64'}
 exec(compile(definitions(list(PINS)[0],arithmetic),list(PINS)[0],'exec'),SCOPE)
 for n in arithmetic:setattr(P,n,SCOPE[n])
 f='author_fragment_exact_exponent_two_product_v003.py';exec(compile(definitions(f,{'exact_exponent_two_product','install_exact_exponent_product'}),f,'exec'),globals());install_exact_exponent_product(SCOPE,P,keep,'NEW_saved_adjoint_scalar_exact_exponent_product')
 f='author_fragment_native_metric_star_paired_gmres_v001.py';exec(compile(definitions(f,{'native_metric_gmres_put','native_metric_gmres_tree','native_metric_gmres_dot','native_metric_gmres_norm'}),f,'exec'),globals())
 f='author_fragment_single_decode_recheck_v001.py';exec(compile(definitions(f,{'recheck'}),f,'exec'),SCOPE);P.recheck=SCOPE['recheck'];P.LINEAR_TOL=1e-10

def load_json(ref):
 assert all(v is not None for v in ref);bind(ref[0],ref[1]);r=json.loads(P.path(ref[0]).read_text());assert len(ref)==2 or r['status']==ref[2];return r

def role(pr,ordinal,tag,owner):
 rows=[r for r in pr['records'] if r['ordinal']==ordinal];assert len(rows)==1;r=rows[0]
 assert r['role']==tag and r['file']==OLD_STEM+'_%05d_'%ordinal+tag+'.npz' and r['commit_file']==r['file']+'.COMMIT.json'
 assert r['failed'] is False and all(r[k] is True for k in ('owner_equal','embedded_metadata_equal','member_names_headers_and_structural_lengths_equal','qualification_all_false'))
 bind(r['commit_file'],r['commit_sha256']);q=json.loads(P.path(r['commit_file']).read_text());assert set(q)=={'file','sha256','metadata'} and q['file']==r['file'] and q['sha256']==r['sha256']
 md=q['metadata'];assert md['owner']==owner and md['failed'] is False and len(md['qualification'])==9 and all(v is False for v in md['qualification'].values()) and md['physical_adoption'] is False
 assert hashlib.sha256(P.encode(md)).hexdigest()==r['metadata_sha256'] and hashlib.sha256(P.encode(md['schema'])).hexdigest()==r['schema_sha256']
 s=P.path(r['file']).stat();saved=r['data_stat'];assert s.st_size==r['data_bytes']==saved['size'] and s.st_mtime_ns==saved['mtime_ns'] and s.st_ino==saved['ino'] and s.st_mode&0o777==saved['mode']==0o444
 return dict(q,commit_file=r['commit_file'],commit_sha256=r['commit_sha256'])

def linked_commit(ref):
 bind(ref['commit_file'],ref['commit_sha256']);r=json.loads(P.path(ref['commit_file']).read_text());assert r['file']==ref['file'] and r['sha256']==ref['sha256'];return r

def admission():
 bind(OLD_SOURCE[0],OLD_SOURCE[1]);bind(OLD_PROTOCOL[0],OLD_PROTOCOL[1]);manifest=load_json(OLD_MANIFEST);owner=manifest['owner']
 assert owner==dict(owner='root',pid=37897,source_sha256=OLD_SOURCE[1],started='2026-10-07T21:51:25.564084+00:00')
 assert manifest['cap']==CAP and manifest['cycles']==1 and manifest['restarts']==0 and manifest['physical_adoption'] is False
 pr=load_json(SELECTED_OUTPUT_PROOF);extra=load_json(FIRST_CHUNK_OUTPUT_PROOF);coverage=load_json(MANIFEST_INPUT_COVERAGE_PROOF)
 assert pr['owner']==owner and pr['source']['sha256']==OLD_SOURCE[1] and pr['selected_expected_roles']==pr['selected_verified_roles']==16 and not pr['pending'] and not pr['errors']
 assert pr['selected_coverage_only'] is True and pr['all857_outputs_authenticated'] is pr['all_manifest_inputs_authenticated'] is False
 assert pr['metadata_and_schema_hash_encoding']=='sorted compact JSON plus newline, matching original encode'
 bind(pr['owner_start']['file'],pr['owner_start']['sha256']);assert json.loads(P.path(pr['owner_start']['file']).read_text())==owner
 failure=load_json((pr['natural_failure_proof']['file'],pr['natural_failure_proof']['sha256']));observed=[q for q in failure['workers'] if q['pid']==37897];assert len(observed)==1 and observed[0]['exit_code']==1 and observed[0]['committed_roles']==857
 assert extra['owner']==owner and extra['source']['sha256']==OLD_SOURCE[1] and extra['selected_expected_roles']==extra['selected_verified_roles']==7 and not extra['pending'] and not extra['errors']
 assert extra['metadata_and_schema_hash_encoding']==pr['metadata_and_schema_hash_encoding'] and extra['all857_outputs_authenticated'] is extra['all_manifest_inputs_authenticated'] is False
 assert coverage['owner']==owner and coverage['manifest']['sha256']==OLD_MANIFEST[1] and coverage['required_scalar_stage_inputs_verified'] is coverage['required_source_and_header_bytes_freshly_verified'] is True
 assert coverage['selected_output_proof']['sha256']==SELECTED_OUTPUT_PROOF[1] and coverage['first_chunk_output_proof']['sha256']==FIRST_CHUNK_OUTPUT_PROOF[1] and coverage['all_original_manifest_inputs_verified'] is False
 required={OLD_SOURCE[0],OLD_PROTOCOL[0],IO_PARENT,*PINS};covered=coverage['selected_input_sha256'];original=manifest['input_sha256']
 assert all(str((BASE/n).resolve()) in covered and covered[str((BASE/n).resolve())]==original[str((BASE/n).resolve())] for n in required)
 assert all(n in original and h==original[n] for n,h in covered.items())
 inp=role(pr,0,'INPUT',owner);md=inp['metadata'];assert md['kind']=='copied_NEW_literal_stationarity_eL_and_fixed_coordinate_scaling' and md['context']=={} and md['closed_provenance']==manifest['closed_provenance']
 assert md['RHS_sign']=='epsilon minus literal-minus-registered' and md['score_groups']==['native','metric','packed'] and md['score_columns']==['raw','divided_by_saved_coordinate_scale'] and md['original_forward_physical_six_gates_tested'] is False
 rights=[role(pr,2+122*j,'RIGHT_ADJOINT',owner) for j in range(PREFIX+1)];actions=[role(pr,123+122*j,'ADJOINT_WEAK',owner) for j in range(PREFIX)];first_chunks=[role(extra,3+122*j,'ADJOINT_CHUNK',owner) for j in range(PREFIX)]
 factor=rights[0]['metadata']['factor'];factor_md=linked_commit(factor)['metadata'];assert factor_md['owner']==owner and factor_md['failed'] is False and factor_md['controls']==manifest['closed_provenance']['application']
 for q in rights:assert q['metadata']['kind']=='NEW_nodal110_signed_factor_adjoint_application' and q['metadata']['input']==thin(inp) and q['metadata']['factor']==factor and q['metadata']['context']==dict(operation_role='RIGHT_ADJOINT')
 for q,c in zip(actions,first_chunks):
  m=q['metadata'];cm=c['metadata'];assert m['kind']=='NEW_original244_coefficient_Astar_fullweak' and m['input']==thin(inp) and len(m['chunks'])==120 and m['chunks'][0]==thin(c)
  assert cm['kind']=='NEW_directed_Kstar_application_to_NEW_GMRES_dual' and cm['column']==0 and cm['selection']==[0,128] and cm['input']==thin(inp) and cm['label']==m['label'] and cm['context']==dict(operation_role='ADJOINT_WEAK')
 selected=[inp]+rights+actions+first_chunks;assert len(selected)==23 and len({q['file'] for q in selected})==23
 return dict(owner=owner,input=inp,rights=rights,actions=actions,first_chunks=first_chunks,factor_context=dict(copy=factor,original=factor_md['source'],terminal=manifest['closed_provenance']['factor'],application=factor_md['controls']),manifest=manifest,selected=selected,selected_proof=SELECTED_OUTPUT_PROOF,first_chunk_proof=FIRST_CHUNK_OUTPUT_PROOF,coverage_proof=MANIFEST_INPUT_COVERAGE_PROOF)

def selected_read(q,names):
 # Whole archive byte seals are inherited from root proof, not rehashed/decompressed here.
 out={};md=q['metadata']
 with np.load(P.path(q['file']),allow_pickle=False) as f:
  assert set(f.files)==set(md['schema'])|{'metadata_json'} and json.loads(str(f['metadata_json']))==md
  for n in names:
   a=f[n].copy();keep('loaded_'+n,a);s=md['schema'][n];assert list(a.shape)==s['shape'] and str(a.dtype)==s['dtype'] and s['finite'] is True and np.all(np.isfinite(a)),n;out[n]=a
 return out

def pair(data,name):
 p=tuple(data[name+'_'+w] for w in ('hi','lo'));assert all(a.shape==(N,) and a.dtype==np.float64 and np.all(np.isfinite(a)) for a in p);return p

def words_equal(a,b):return all(np.array_equal(a[w].view(np.uint64),b[w].view(np.uint64)) for w in (0,1))

def compact_seal(tag,data,metadata):
 q=P.checkpoint(tag,arrays(data),dict(metadata,context=dict(CONTEXT)));clear_current();return thin(q)

def reconstruct(refs):
 label='NEW_saved_original_adjoint7';schema=refs['input']['metadata']['schema'];norm_names=['NEW_adjoint_source_reference_'+group+'_'+version+'_source_norm_normalizing_norm' for group in ('native','metric','packed') for version in ('raw','scaled')]
 reference_names=['NEW_adjoint_source_reference_original_positive_coordinate_scale']+[n for n in schema if n.startswith('copied_canonical_reference_')]+['copied_anchor_original_reference_'+n for n in ('native_scale','metric_scale')]
 prefixes=('NEW_adjoint_packed_eL_RHS','NEW_adjoint_source_reference_both_word_eL','NEW_adjoint_source_reference_packed_raw_source_words','NEW_adjoint_source_reference_scaled_source')
 data=selected_read(refs['input'],[n+'_'+w for n in prefixes for w in ('hi','lo')]+norm_names+reference_names);rhs=pair(data,'NEW_adjoint_packed_eL_RHS');scaled=pair(data,'NEW_adjoint_source_reference_scaled_source')
 assert words_equal(rhs,pair(data,'NEW_adjoint_source_reference_both_word_eL')) and words_equal(rhs,pair(data,'NEW_adjoint_source_reference_packed_raw_source_words'))
 scale=data[reference_names[0]];assert scale.shape==(N,) and scale.dtype==np.float64 and np.all(scale>0)
 norms=np.asarray([float(data[n]) for n in norm_names]).reshape(3,2);groups=(slice(0,380292),slice(380292,None),slice(None));scores=np.zeros((3,2))
 for row,selection in enumerate(groups):
  zero=all(np.all(a[selection]==0) for a in rhs);assert all(np.all(a[selection]==0) for a in scaled)==zero and np.all(norms[row]==0 if zero else norms[row]>0);scores[row]=0. if zero else 1.
 assert scores.shape==(3,2) and not np.all(scores<=P.LINEAR_TOL);beta=float(data[norm_names[4]]);assert np.isfinite(beta) and beta>0
 start=P.a_dd(np.zeros(N));zero=P.a_dd(np.zeros(N))
 context_data={n+'_'+w:p[i] for n,p in (('start',start),('rhs',rhs),('current_action',zero),('current_residual',rhs)) for i,w in enumerate(('hi','lo'))};context_data.update(current_scores=scores,cached_source_norms=norms,initial_norm=np.asarray(beta),scaled_source_hi=scaled[0],scaled_source_lo=scaled[1],**{n:data[n] for n in reference_names+norm_names})
 context_ref=compact_seal('CONTEXT',context_data,dict(kind='bitcopied_original_eL_references_and_source53_identity_left_zero_start',source=thin(refs['input']),factor_context=refs['factor_context'],initial_score_ratios_NEW_from_exact_saved_source_reference=True,old_score_body_replayed=False,original_forward_physical_six_gates_tested=False));del data,context_data,scaled
 V=[];basis_refs=[];right_solution_hashes=[];first_forward=None;rp='mechanical_adjoint_GMRES_current_forward_original_packed_'
 for j,q in enumerate(refs['rights']):
  CONTEXT.update(stage='copy_saved_basis',basis=j);d=selected_read(q,[rp+n+'_'+w for n in ('words','solution') for w in ('hi','lo')]);v=pair(d,rp+'words');solution=pair(d,rp+'solution');V.append(v)
  right_solution_hashes.append([hashlib.sha256(a.tobytes()).hexdigest() for a in solution]);basis_refs.append(compact_seal('BASIS',dict(basis_hi=v[0],basis_lo=v[1]),dict(kind='bitcopied_archived_original_adjoint_Arnoldi_basis',basis=j,source=thin(q),factor_context=refs['factor_context'])))
  if j==PREFIX:first_forward=compact_seal('EARNED_FIRST_FORWARD',dict(earned_solution_hi=solution[0],earned_solution_lo=solution[1]),dict(kind='bitcopied_ALREADY_EARNED_eighth_right_factor_ADJOINT_result',source=thin(q),exact_input_basis=basis_refs[-1],factor_context=refs['factor_context'],must_return_once_after_exact_argument_context_match=True,factor_application_replayed=False))
  del d,solution
 v0=P.a_div64(rhs,beta,keep,label+'_initial_normalization');assert words_equal(v0,V[0]),'Reconstructed initial normalization words differ';del v0
 cap=CAP;Hh=np.zeros((cap+1,cap));Hl=Hh.copy();R=Hh.copy();cs=np.zeros(cap);sn=cs.copy();g=np.zeros(cap+1);g[0]=beta;history=[];arnoldi_errors=[];arnoldi_bounds=[];steps=[];iterations=0;ap='mechanical_adjoint_GMRES_current_fine_action_'
 for j,q in enumerate(refs['actions']):
  clear_current();CONTEXT.update(stage='new_lost_scalar_MGS_QR_arithmetic',iteration=j+1);keep('reconstructed_initial_norm',np.asarray(beta))
  d=selected_read(q,[ap+'completed_Astar_'+w for w in ('hi','lo')]);av=pair(d,ap+'completed_Astar');supplied=selected_read(refs['first_chunks'][j],[ap+n+'_'+w for n in ('supplied_NEW_dual','Sstar_supplied_packed_dual') for w in ('hi','lo')]);physical=pair(supplied,ap+'supplied_NEW_dual');sstar=pair(supplied,ap+'Sstar_supplied_packed_dual')
  assert words_equal(physical,sstar) and [hashlib.sha256(a.tobytes()).hexdigest() for a in physical]==right_solution_hashes[j],'Saved Astar input differs from earned right-adjoint result';del physical,sstar,d,supplied
  original=native_metric_gmres_put(label+'_current_congruence_action',tuple(a.copy() for a in av));w=original;h=P.a_dd(np.zeros(j+1))
  for repeat in range(2):
   for i in range(j+1):
    value=native_metric_gmres_dot(V[i],w,label+'_current_MGS_dot');h[0][i],h[1][i]=P.a_add((h[0][i],h[1][i]),value)
    w=native_metric_gmres_put(label+'_current_MGS_remainder',P.a_sub(w,P.a_mul(value,V[i])))
  Hh[:j+1,j]=h[0];Hl[:j+1,j]=h[1];norm=native_metric_gmres_norm(w,label+'_current_remainder');Hh[j+1,j]=norm
  rebuilt=w;envelope=abs(w[0])+abs(w[1])+abs(original[0])+abs(original[1])
  for i in range(j+1):rebuilt=P.a_add(rebuilt,P.a_mul((h[0][i],h[1][i]),V[i]));envelope=envelope+(abs(h[0][i])+abs(h[1][i]))*(abs(V[i][0])+abs(V[i][1]))
  defect=native_metric_gmres_put(label+'_current_Arnoldi_reconstruction_gap',P.a_sub(original,rebuilt));keep(label+'_current_Arnoldi_positive_envelope',envelope.copy());arnoldi_errors.append(float(np.linalg.norm(defect[0]+defect[1])));arnoldi_bounds.append(float(np.linalg.norm(envelope)))
  column=Hh[:j+2,j]+Hl[:j+2,j];native_metric_gmres_put(label+'_current_H_readout_defect',P.a_sub((Hh[:j+2,j],Hl[:j+2,j]),P.a_dd(column)));keep(label+'_current_unrotated_H_column',column.copy());keep(label+'_H_hi',Hh.copy());keep(label+'_H_lo',Hl.copy())
  for i in range(j):a,b=column[i],column[i+1];column[i]=cs[i]*a+sn[i]*b;column[i+1]=-sn[i]*a+cs[i]*b
  den=float(np.hypot(column[j],column[j+1]));keep(label+'_current_Givens_denominator',np.asarray(den))
  assert np.isfinite(den) and den>0,'Reconstructed prefix has an exact QR breakdown'
  cs[j]=column[j]/den;sn[j]=column[j+1]/den;a,b=column[j],column[j+1];column[j]=cs[j]*a+sn[j]*b;discarded=-sn[j]*a+cs[j]*b;keep(label+'_current_QR_lower_roundoff',np.asarray(discarded));column[j+1]=0;R[:j+2,j]=column
  a,b=g[j],g[j+1];g[j]=cs[j]*a+sn[j]*b;g[j+1]=-sn[j]*a+cs[j]*b;iterations=j+1
  history.append((iterations,float(abs(g[j+1])),norm,den));keep(label+'_history',np.asarray(history));keep(label+'_H_hi',Hh.copy());keep(label+'_H_lo',Hl.copy());keep(label+'_R',R.copy());keep(label+'_Givens_cos',cs.copy());keep(label+'_Givens_sin',sn.copy());keep(label+'_rotated_RHS',g.copy())
  assert norm>0 and iterations==j+1 and iterations<20
  next_v=native_metric_gmres_put(label+'_basis_%03d'%iterations,P.a_div64(w,norm,keep,label+'_current_normalization'))
  assert words_equal(next_v,V[j+1]),('Reconstructed normalized next basis words differ',j+1)
  steps.append(compact_seal('SCALAR_STEP',dict(H_hi=Hh,H_lo=Hl,R=R,Givens_cos=cs,Givens_sin=sn,rotated_RHS=g,history=np.asarray(history),Arnoldi_contact_norms=np.asarray(arnoldi_errors),Arnoldi_operation_bounds=np.asarray(arnoldi_bounds),initial_norm=np.asarray(beta)),dict(kind='NEW_reconstructed_original117_lost_scalar_state',completed_iteration=iterations,original_action=thin(q),next_basis=basis_refs[j+1],both_next_basis_words_exact=True,old_action_or_factor_replayed=False,unrecorded_outer_state_byte_identity_claimed=False)))
  del av,original,w,h,rebuilt,defect,envelope,next_v
 ae=np.asarray(arnoldi_errors);ab=np.asarray(arnoldi_bounds);keep(label+'_all_Arnoldi_contact_norms',ae.copy());keep(label+'_all_Arnoldi_operation_bounds',ab.copy());P.check(label+'_all_Arnoldi_reconstructions',ae,np.zeros_like(ae),ab)
 Q=np.eye(iterations+1)
 for i in range(iterations):a,b=Q[i].copy(),Q[i+1].copy();Q[i]=cs[i]*a+sn[i]*b;Q[i+1]=-sn[i]*a+cs[i]*b
 HH=Hh[:iterations+1,:iterations]+Hl[:iterations+1,:iterations];RR=R[:iterations+1,:iterations];contact=Q@HH-RR;bound=abs(Q)@abs(HH)+abs(RR);keep(label+'_small_Q',Q.copy());keep(label+'_small_QR_contact',contact.copy());keep(label+'_small_QR_positive_bound',bound.copy());P.check(label+'_small_QR_operation_norm',np.asarray(np.linalg.norm(contact)),np.asarray(0.),np.asarray(np.linalg.norm(bound)))
 state=compact_seal('RESUME_STATE',dict(H_hi=Hh,H_lo=Hl,R=R,Givens_cos=cs,Givens_sin=sn,rotated_RHS=g,history=np.asarray(history),Arnoldi_contact_norms=ae,Arnoldi_operation_bounds=ab,initial_norm=np.asarray(beta)),dict(kind='NEW_scalar_state_for_HELD_original117_adjoint_saved_prefix_resume',cap=CAP,iterations=PREFIX,next_iteration=PREFIX,reason='explicit_cap',context=context_ref,basis=basis_refs,scalar_steps=steps,earned_first_forward=first_forward,column_action_scopes=['represented_coefficient_Astar']*PREFIX,updated_is_original_start=True,after_is_original_current=True,increment_is_original_zero_correction=True,prefix_state_authenticated=True,original_associations_or_committed_state_verified=True,all_available_next_basis_words_matched=True,completed_actions_and_factors_not_replayed=True,original_rhs_warm_current_and_six_references_unchanged=True,original_right_and_left_maps_unchanged=True,external_new_natural_close_prefix_proof_required=True,unrecorded_outer_state_byte_identity_claimed=False,original_forward_physical_six_gates_tested=False,physical_adoption=False))
 assert iterations==PREFIX and len(RECORDS)==18 and len(CHECKS)==2 and all(q['passed'] is True and q['tolerance']==2e-11 for q in CHECKS)
 return dict(status='ORIGINAL_MECHANICAL_ADJOINT_GMRES7_SCALAR_STATE_RECONSTRUCTED',resume_state=state,context=context_ref,basis=basis_refs,scalar_steps=steps,earned_first_forward=first_forward,original_owner=refs['owner'],original_natural_exit_code=1,selected_original_roles=23,selected_archive_byte_authentication_inherited_from_bound_proofs=True,full_original_input_or_unused_archive_audit_claimed=False,initial_and7next_basis_words_exact=True,cap=CAP,next_iteration=PREFIX,old_actions_factors_or_controls_replayed=False,source_relative_adjoint_gates_tested=False,original_forward_physical_six_gates_tested=False,physical_adoption=False)

def main():
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and all(v is not None for q in (SELECTED_OUTPUT_PROOF,FIRST_CHUNK_OUTPUT_PROOF,MANIFEST_INPUT_COVERAGE_PROOF) for v in q),'Root reviewed proof-bound release required'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive new namespace required'
 initialize();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(IO_PARENT,IO_PARENT_SHA);bind(DRIVER_PROTOCOL,PROTOCOL_SHA)
  for n,h in PINS.items():bind(n,h)
  refs=admission();P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,selected_original_roles=[thin(q) for q in refs['selected']],selected_output_proof=SELECTED_OUTPUT_PROOF,first_chunk_output_proof=FIRST_CHUNK_OUTPUT_PROOF,manifest_input_coverage_proof=MANIFEST_INPUT_COVERAGE_PROOF,original_owner=refs['owner'],cap=CAP,prefix=PREFIX,actions_or_factors_will_be_called=False,full_original_input_audit_claimed=False))
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=reconstruct(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(case['status'],rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  try:P.checkpoint('ERROR_RAW',arrays({**RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='available_NEW_scalar_reconstruction_operands',context=dict(CONTEXT)),failed=True)
  except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())

"""Guarded compact five-field canonical York target contacts; no field solve."""
from pathlib import Path
import importlib.util,hashlib,json,os,sys,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_INITIAL_YORK_FIVE_FIELD_TARGET_CONTACTS_V001'
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='9611aa7fd54466514f14d2cdf69b58d57bedab89f86d182700711390c11a776e'
PROVIDER=('cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py','5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18')
FRAGMENTS={'author_fragment_initial_york_five_field_target_contact_v002.py':'8f00c4a5bf905a6b1b338ec9444c26d7e7f4faaccd3a5189d0bb6159fb177093','author_fragment_initial_york_five_field_target_admission_v001.txt':'bfe2cb3e201dd5fb1ce23c59a269055bc91be03614a76bdc8f92946b708eb31e'}
FIELDS=('a','W_R','W_Z','W_phi','t')
P=np=None

def bind(n,h):
 assert h is not None and P.sha(P.path(n))==h,n
 key=str(P.path(n).resolve());assert key not in P.INPUTS or P.INPUTS[key]==h;P.INPUTS[key]=h

def keep(n,x):return ORIGINAL_CAPTURE(n,np.asarray(x).copy())

def put(n,x):keep(n+'_hi',x[0]);keep(n+'_lo',x[1]);return x

def thin(q):return {n:q[n] for n in ('file','sha256','commit_file','commit_sha256')}

def initialize():
 global P,np,ORIGINAL_CAPTURE
 n,h=PROVIDER;assert hashlib.sha256((BASE/n).read_bytes()).hexdigest()==h
 spec=importlib.util.spec_from_file_location('five_field_target_provider',BASE/n);P=importlib.util.module_from_spec(spec);spec.loader.exec_module(P)
 import numpy as numpy_module
 np=numpy_module;P.np=np;ORIGINAL_CAPTURE=P.capture;P.capture=keep;P.STEM=STEM;P.__file__=__file__;P.PROTOCOL_SHA=PROTOCOL_SHA
 P.FLAGS=dict(finite_configuration_prepared=False,global_rate_response_computed=False,global_constraint_rank_qualified=False,TT_free_data_admitted=False,canonical_primitive_bridge_resolved=False,exterior_qualified=False,physical_adoption=False,evolution_qualified=False)
 for n,h in {PROVIDER[0]:PROVIDER[1],**FRAGMENTS,STEM+'.md':PROTOCOL_SHA,__file__:P.sha(__file__)}.items():bind(n,h)
 for n in FRAGMENTS:exec(compile((BASE/n).read_text(),str(BASE/n),'exec'),globals())

def reset(stage,**context):
 P.RAW.clear();P.AVAILABLE.clear();P.DD_ARRAY_CURRENT.clear();P.CONTEXT.clear();P.CONTEXT.update(stage=stage,**context)

def arrays():return {n:np.asarray(x).copy() for n,x in {**P.RAW,**P.AVAILABLE,**P.DD_ARRAY_CURRENT.get('arrays',{})}.items()}

def pair_sum(x,label):
 put(label+'_operands',x);out=P.a_dd(np.array(0.))
 for h,l in zip(x[0].reshape(-1),x[1].reshape(-1)):
  out=P.a_add(out,(h,l));put(label+'_current_partial',out)
 return put(label+'_sum',out)

def fresh_five_field_target_control():
 reset('new_dyadic_five_field_target_control');eps=2.**-60;w=2.**-12
 h=np.eye(3)[None];S=np.diag([1.,-1.,0.])[None];Pi=np.diag([3.,1.,2.])[None];BW=np.diag([2*w,0.,-2*w])[None]
 inputs=dict(reference_h=h,reference_ih=h.copy(),reference_h_basis=h.copy(),reference_A=np.ones(1),reference_mu=np.ones(1),S=S,tau=np.array([6.]),owned_Pi=Pi,delta_a=np.array([4*eps]),delta_BW=BW,delta_tau=np.array([3.]))
 for n,x in inputs.items():keep('fixture_input_'+n,x)
 out=initial_york_five_field_target_contact(inputs['reference_A'],h,h,h,inputs['reference_mu'],P.a_dd(S),P.a_dd(inputs['tau']),P.a_dd(Pi),P.a_dd(inputs['delta_a']),P.a_dd(BW),P.a_dd(inputs['delta_tau']),keep,'fixture')
 target=out['delta_coordinate_target'];dm=out['delta_sqrt_h'];dt=(P.AVAILABLE['fixture_actual_canonical_trace_contact_hi'],P.AVAILABLE['fixture_actual_canonical_trace_contact_lo'])
 actual=np.concatenate((target[0].reshape(-1),target[1].reshape(-1),dm[0],dm[1],dt[0],dt[1]))
 expected=np.array([1+2*w,1.,1-2*w,0.,0.,0.,-12*eps,-4*eps,-8*eps,0.,0.,0.,6*eps,0.,3.,0.])
 envelope=np.array([32.]*6+[128*eps]*6+[32*eps,32*eps,32.,128*eps])
 P.check('fresh_dyadic_combined_five_field_target_high_and_low_words',actual,expected,envelope)
 return P.checkpoint('FIXTURE',arrays(),dict(kind='new_dyadic_combined_York_target_first_contact',epsilon=eps,longitudinal_weight=w,independent_expected_words=True,controls=P.CHECKS.copy()))

def compact_basis(geo):
 ci=geo['cell_i'];cj=geo['cell_j'];indices=np.flatnonzero(np.isin(ci,(42,43))&np.isin(cj,(21,22)))
 assert len(indices)==4 and len(set(zip(ci[indices],cj[indices])))==4
 corners=((0,0),(1,0),(0,1),(1,1));which=np.array([next(k for k,(di,dj) in enumerate(corners) if int(i)+di==43 and int(j)+dj==22) for i,j in zip(ci[indices],cj[indices])])
 hats=geo['hats'].reshape(4,4,3,3784);factors=[]
 for iq in range(4):factors.append(np.stack([hats[iq,which,j,indices] for j in range(3)],axis=-1))
 return indices,which,np.stack(factors)

def longitudinal_contact(maps,factors,R,component,label):
 jets=factors.copy()
 if component==0:jets[:,0]=R*factors[:,0];jets[:,1]=R*factors[:,1]+factors[:,0];jets[:,2]=R*factors[:,2]
 keep(label+'_registered_vector_value_R_Z_factors',jets);out=P.a_dd(np.zeros((len(R),3,3)))
 for jet in range(3):
  term=P.a_mul64(jets[:,jet,None,None],P.a_slice(maps,(slice(None),component,jet,slice(None),slice(None))))
  put(label+'_current_map_term',term);out=P.a_add(out,term);put(label+'_current_map_partial',out)
 return put(label+'_L_delta_W',out)

def compact_metric_scatter(targets,geo,indices,label):
 out=P.a_dd(np.zeros((6,87,45)));ci=geo['cell_i'][indices];cj=geo['cell_j'][indices]
 for iq,target in enumerate(targets):
  F=P.dd_metric_F(geo['R'][iq])[indices];keep(label+'_current_F',F)
  local=P.a_matvec(F.swapaxes(-1,-2),target);put(label+'_current_F_transpose_target',local)
  weight=(geo['dv'][iq]/geo['R'][iq])[indices];weighted=P.a_mul64(weight[:,None],local);put(label+'_current_weighted_target',weighted)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   hat=geo['hats'][iq,corner,0].reshape(3784)[indices];value=P.a_transpose(P.a_mul64(hat[:,None],weighted),(1,0));put(label+'_current_corner_target',value)
   key=(slice(None),ci+di,cj+dj);updated=P.a_add(P.a_slice(out,key),value);out[0][key]=updated[0];out[1][key]=updated[1];put(label+'_current_scatter_partial',out)
  # Each complete Gauss-column contribution is retained before the next one.
 update=P.a_add(P.a_slice(out,(slice(None),1,slice(None))),P.a_slice(out,(slice(None),0,slice(None))))
 out[0][:,1]=update[0];out[1][:,1]=update[1];out[0][:,0]=0;out[1][:,0]=0;out[0][3:5,:,0]=0;out[1][3:5,:,0]=0
 return put(label+'_metric_weak_target',out)

def compact_dual_test(test,geo,indices,iq,label):
 # Polynomial transpose of the original separate F64/weight64/hat64 scatter.
 lifted=P.lift_metric(test);ci=geo['cell_i'][indices];cj=geo['cell_j'][indices];local=P.a_dd(np.zeros((4,6)));positive=np.zeros((4,6))
 for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
  values=lifted[:,ci+di,cj+dj].T;hat=geo['hats'][iq,corner,0].reshape(3784)[indices]
  local=P.a_add(local,P.a_prod(hat[:,None],values));positive+=abs(hat[:,None])*abs(values);put(label+'_current_test_partial',local)
 F=P.dd_metric_F(geo['R'][iq])[indices];value=put(label+'_physical_dual_test',P.a_matvec(F,local));weight=(geo['dv'][iq]/geo['R'][iq])[indices]
 return value,weight,np.einsum('pij,pj->pi',abs(F),positive)

def target_contact_packet(refs):
 reset('select_owned_reference_geometry');geo=P.read_pair(refs['input'],('R','dv','hats','cell_i','cell_j','r','z'));indices,which,factors=compact_basis(geo)
 keep('compact_point_indices',indices);keep('compact_hat_corner',which);keep('compact_scalar_value_R_Z_factors',factors)
 inp=P.checkpoint('INPUT',{**geo,'compact_point_indices':indices.copy(),'compact_hat_corner':which.copy(),'compact_scalar_value_R_Z_factors':factors.copy()},dict(kind='same_reference_five_compact_York_target_fields',node=[43,22],fields=FIELDS,input_ref=thin(refs['input']),maps_ref=thin(refs['maps']),columns=[thin(q) for q in refs['columns']],shared_basis_ref=refs['shared_basis_ref'],pilot_refs=refs['pilot_refs'],prior_signed_primitive_readout_ref=refs['prior_readout_ref'],fixed=refs['fixed'],owned_background=refs['owned_background'],S_source='owned_literal_PiTF_test_only',tau_parameterization='fixed_reference_mu_ref_times_scalar_t',W_state_admitted=False,physical_ports=None))
 fixture=fresh_five_field_target_control();reset('load_saved_full_longitudinal_maps');full=P.read_pair(refs['maps'],('L_maps_hi','L_maps_lo','L_map_operation_envelope'))
 maps={iq:tuple(full['L_maps_'+word][iq*3784+indices].copy() for word in ('hi','lo')) for iq in range(4)};map_bounds={iq:full['L_map_operation_envelope'][iq*3784+indices].copy() for iq in range(4)};del full
 columns=[];targets={name:[] for name in FIELDS}
 for iq in range(4):
  reset('five_new_compact_target_contacts',column=iq);names=tuple('column_%d_%s_%s'%(iq,n,w) for n in ('trace_subtracted_canonical_density','total_canonical_trace_density','total_canonical_tensor_density') for w in ('hi','lo'))+('input_chart_h','input_chart_ih','input_chart_sqrt_h')
  raw=P.read_pair(refs['columns'][iq],names);selected={n:x[indices].copy() for n,x in raw.items()};del raw;P.RAW.clear()
  for n,x in selected.items():keep('owned_'+n,x)
  put('owned_longitudinal_maps',maps[iq]);keep('owned_L_map_operation_envelope',map_bounds[iq]);keep('compact_point_indices',indices);keep('compact_scalar_value_R_Z_factors',factors[iq])
  h=selected['input_chart_h'];ih=selected['input_chart_ih'];mu=selected['input_chart_sqrt_h'];R=geo['R'][iq,indices];hb=np.zeros((4,3,3));hb[:,0,0]=hb[:,1,1]=1.;hb[:,2,2]=(geo['R'][iq]**2)[indices]
  keep('compact_R',R);keep('reference_h_basis',hb);keep('reference_A',h[:,0,0])
  S=tuple(selected['column_%d_trace_subtracted_canonical_density_%s'%(iq,w)] for w in ('hi','lo'));tau=tuple(selected['column_%d_total_canonical_trace_density_%s'%(iq,w)] for w in ('hi','lo'));Pi=tuple(selected['column_%d_total_canonical_tensor_density_%s'%(iq,w)] for w in ('hi','lo'))
  for field in FIELDS:
   zero=P.a_dd(np.zeros(4));da=P.a_dd(factors[iq,:,0]) if field=='a' else zero;dt=P.a_prod(mu,factors[iq,:,0]) if field=='t' else zero;BW=P.a_dd(np.zeros((4,3,3)))
   put(field+'_delta_a',da);put(field+'_fixed_reference_delta_tau',dt)
   if field in ('W_R','W_Z','W_phi'):
    L=longitudinal_contact(maps[iq],factors[iq],R,FIELDS.index(field)-1,field);left=put(field+'_inverse_left_L_delta_W',five_field_raw_left(ih,L));raised=put(field+'_two_sided_raised_L_delta_W',five_field_raw_right(left,ih));BW=P.a_mul64(mu[:,None,None],raised)
   put(field+'_delta_BW',BW);out=initial_york_five_field_target_contact(h[:,0,0],hb,h,ih,mu,S,tau,Pi,da,BW,dt,keep,field);targets[field].append(tuple(x.copy() for x in out['delta_coordinate_target']))
  rec=P.checkpoint('COLUMN',arrays(),dict(kind='five_compact_total_canonical_metric_target_contacts',column=iq,node=[43,22],fields=FIELDS,trace_column_ref=thin(refs['columns'][iq]),saved_maps_ref=thin(refs['maps']),all_map_cross_terms_retained=True,reference_mu_held_fixed=True,S_is_owned_PiTF_test_only=True,TT_free_prior_admitted=False,physical_ports=None));columns.append(rec)
 reset('new_metric_canonical_target_RHS_assembly');test=(np.arange(6*87*45)%23-11).reshape(6,87,45)/41.;test[~P.metric_mask()]=0;keep('metric_functional_test',test);loads={};errors=[];envelopes=[]
 for field in FIELDS:
  for iq,x in enumerate(targets[field]):put(field+'_point_%d_target'%iq,x)
  weak=compact_metric_scatter(targets[field],geo,indices,field);nodal=pair_sum(P.a_mul64(test,weak),field+'_nodal_functional');direct=P.a_dd(np.array(0.));bound=0.
  for iq,target in enumerate(targets[field]):
   value,weight,positive=compact_dual_test(test,geo,indices,iq,field+'_dual_%d'%iq);integrand=P.a_mul64(weight[:,None],P.a_mul(value,target));put(field+'_current_direct_integrand',integrand);term=pair_sum(integrand,field+'_current_direct_column');direct=P.a_add(direct,term);put(field+'_direct_functional',direct)
   bound+=2*float(np.sum(abs(weight[:,None])*positive*(abs(target[0])+abs(target[1]))))
  gap=put(field+'_nodal_minus_direct_functional',P.a_sub(nodal,direct));errors.append(float(gap[0]+gap[1]));envelopes.append(bound)
  for n,x in (('weak_metric_target',weak),('nodal_functional',nodal),('direct_functional',direct),('functional_gap',gap)):
   for word,suffix in enumerate(('hi','lo')):loads[field+'_'+n+'_'+suffix]=np.asarray(x[word]).copy();keep(field+'_'+n+'_'+suffix,x[word])
  for word,suffix in enumerate(('hi','lo')):
   native=np.zeros((33,3,87,45));packed=P.pack_fields(native,weak[word]);loads[field+'_full_coupled_target_RHS_'+suffix]=packed.copy();keep(field+'_full_coupled_target_RHS_'+suffix,packed)
  # Save completed target rows before the next field's assembly can refuse.
 P.check('five_new_metric_target_nodal_direct_functionals',np.array(errors),np.zeros(5),np.array(envelopes));loads.update({n:np.asarray(x).copy() for n,x in P.RAW.items() if n.startswith('control_')});loads['metric_functional_test']=test.copy();loads['compact_point_indices']=indices.copy()
 final=P.checkpoint('LOADS',loads,dict(kind='five_new_canonical_metric_target_RHS_only',columns=[thin(q) for q in columns],fields=FIELDS,coupled_coordinates=403340,metric_coordinates=23048,ordinary_and_phase_targets_unchanged=True,global_rate_response_computed=False,canonical_primitive_bridge_resolved=False,controls=P.CHECKS.copy(),physical_ports=None))
 assert len(P.CHECKS)==2 and len(P.RECORDS)==7
 return dict(status='INITIAL_YORK_FIVE_FIELD_TARGET_CONTACTS_MEASURED',input=inp,fixture=fixture,columns=columns,loads=final,controls=P.CHECKS,checkpoints=P.RECORDS,owned_PiTF_as_current_S_test_only=True,auxiliary_W_state_admitted=False,canonical_primitive_bridge_resolved=False,physical_adoption=False)

def outputs_recheck():
 assert P.sha(__file__)==P.OWNER['source_sha256']
 for n,h in P.OUTPUTS.items():assert P.sha(P.path(n))==h,n

def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and PROTOCOL_SHA is not None,'Root and distinct FULL review required'
 assert not list(BASE.glob(STEM+'_*')),'Fresh exclusive output namespace required'
 initialize();P.OWNER=dict(pid=os.getpid(),source_file=Path(__file__).name,source_sha256=P.sha(__file__),started_utc=P.now(),execution='root_owned_new_five_field_target_contacts');P.json_file(STEM+'_OWNER_START.json',P.OWNER)
 try:
  pins,refs=five_field_target_admission();case=target_contact_packet(refs);P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(case,owner=P.OWNER,qualification=P.FLAGS));outputs_recheck();P.json_file(STEM+'_RECEIPT.json',dict(status='CLOSED',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),result_sha256=rh,error_sha256=None,closed_utc=P.now(),qualification=P.FLAGS));outputs_recheck();print(json.dumps(dict(status=case['status'],controls=2,pairs=7)),flush=True);return 0
 except BaseException:
  raw=arrays()
  if raw:P.checkpoint('ERROR_RAW',raw,dict(kind='new_five_field_target_partial_operands',context=P.CONTEXT),failed=True)
  P.seal_actual();eh=P.json_file(STEM+'_ERROR.json',dict(status='FAILED',owner=P.OWNER,controls=P.CHECKS,checkpoints=P.RECORDS,context=P.CONTEXT,qualification=P.FLAGS,traceback=traceback.format_exc()));prior=BASE/(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(status='CLOSED_ERROR',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,closed_utc=P.now(),qualification=P.FLAGS));raise

if __name__=='__main__':sys.exit(main())

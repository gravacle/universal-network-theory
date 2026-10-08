"""Guarded new literal phase Hessian and fixed weak-charge mass preparation."""
from pathlib import Path
import importlib.util,hashlib,json,math,os,sys,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_PHASE_FIXED_WEAK_CHARGE_PREPARATION_V001'
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='6a7eb68c536e5584882a7b883702768f650c271ab7704eb0e51f546df6067e03'
PROVIDER='cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py'
PROVIDER_SHA='5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18'
KERNEL='author_fragment_phase_literal_charge_hessian_v001.py'
KERNEL_SHA='26dd7ebb49baaf9fe1093e227ed6474849096d2dab88c573fe62bdc2d97b010b'
ADMISSION_FRAGMENT='author_fragment_literal_phase_preparation_admission_v001.txt'
ADMISSION_SHA='935fbdd316c4abd5f6fe35a89e40ed8b73b85d9b137f328804073efdd58ce030'
P=None;np=None


def bind(name,h):
 p=Path(name);p=p if p.is_absolute() else BASE/p
 assert h is not None and P.sha(p)==h,name
 key=str(p.resolve());assert key not in P.INPUTS or P.INPUTS[key]==h;P.INPUTS[key]=h;return p


def initialize():
 global P,np
 assert ADMISSION_FRAGMENT is not None and ADMISSION_SHA is not None
 assert hashlib.sha256((BASE/PROVIDER).read_bytes()).hexdigest()==PROVIDER_SHA
 spec=importlib.util.spec_from_file_location('phase_DD_custody_provider',BASE/PROVIDER);P=importlib.util.module_from_spec(spec);spec.loader.exec_module(P)
 import numpy as numpy_module
 np=numpy_module;P.np=np;P.STEM=STEM;P.__file__=__file__;P.PROTOCOL_SHA=PROTOCOL_SHA
 P.FLAGS=dict(finite_configuration_adopted=False,fixed_weak_phase_charge_restored=False,global_I0_profile_determined=False,joint_constraints_qualified=False,evolution_qualified=False,physical_exterior_qualified=False,galaxy_velocity_qualified=False)
 for name,h in ((PROVIDER,PROVIDER_SHA),(KERNEL,KERNEL_SHA),(ADMISSION_FRAGMENT,ADMISSION_SHA)):bind(name,h)
 globals().update(path=P.path,sha=P.sha,INPUTS=P.INPUTS,resolve_record=P.resolve_record)
 for name in (KERNEL,ADMISSION_FRAGMENT):exec(compile((BASE/name).read_text(),str(BASE/name),'exec'),globals())


def save_pairs(values,label):
 data={}
 for name,pair in values.items():
  if isinstance(pair,tuple):phase_pair_keep(label+'_'+name,pair,P.capture);data[name+'_hi']=pair[0];data[name+'_lo']=pair[1]
  else:P.capture(label+'_'+name,pair);data[name]=pair
 return data


def fresh_phase_hessian_control():
 # Independent manufactured tilted chart; it selects no physical EOS or profile.
 h=np.eye(3)[None];g=np.diag([-25/16,1,1,1])[None];hi=np.diag([-16/25,1,1,1])[None];U=np.array([[1.,3/4,0,0]]);uc=np.array([[-25/16,3/4,0,0]])
 s=dict(g=g,hi=hi,U=U,uc=uc,P=np.eye(4)[None]+uc[:,:,None]*U[:,None,:],phi=np.array([[35/32,0,0,0]]),phase_X=np.array([7/8]),phase_PX=np.array([3/8]),phase_PXX=np.array([2.]))
 c=dict(N=np.array([5/4]),dens=np.array([5/4]),sqrt_h=np.array([1.]),ih=h,u=np.array([[3/4,0,0]]))
 for family,values in (('state',s),('chart',c)):
  for name,a in values.items():P.capture('fresh_'+family+'_'+name,a)
 out=phase_literal_charge_hessian(s,c,P.capture,'fresh_phase');save_pairs(out,'fresh_complete')
 actual=np.array([out['action_current'][0][0,0]+out['action_current'][1][0,0],out['action_canonical_density'][0][0]+out['action_canonical_density'][1][0],out['literal_hessian'][0][0]+out['literal_hessian'][1][0]])
 expected=np.array([-3/32,-15/128,23/20]);env=np.array([out['current_envelope'][0,0],c['dens'][0]*out['current_envelope'][0,0],out['hessian_envelope'][0]])+abs(expected)
 P.check('fresh_tilted_literal_phase_charge_and_temporal_Hessian',actual,expected,env)
 P.checkpoint('FIXTURE',{**P.AVAILABLE,**P.RAW},dict(kind='new_independent_literal_phase_Hessian_control',controls=P.CHECKS.copy(),physical_EOS_selected=False))


def phase_column(iq,ref,domain_ref,fixed):
 P.RAW.clear();P.AVAILABLE.clear();P.CONTEXT.update(stage='new_literal_phase_Legendre_readout',column=iq)
 names=('config_P','config_hi','config_uc','config_U','config_phi','config_phase_X','config_phase_PX','config_phase_PXX','chart_N','chart_sqrt_h','chart_dens','chart_ih','chart_u','unchanged_new_phase_canonical_density')
 raw=P.read_pair(ref,names);s={n.removeprefix('config_'):a for n,a in raw.items() if n.startswith('config_')};c={n.removeprefix('chart_'):a for n,a in raw.items() if n.startswith('chart_')}
 assert s['phi'].shape==(3784,4) and np.all(s['phi'][:,1:]==0) and np.all((s['phi'][:,0]>0)&(c['N']>0)&(c['dens']>0)&(c['sqrt_h']>0))
 out=phase_literal_charge_hessian(s,c,P.capture,'phase_column_%d'%iq)
 domain=P.read_pair(domain_ref,('phase_u',));owned_u=domain['phase_u'];P.capture('owned_pressure_argument_u',owned_u);assert owned_u.shape==(3784,) and np.all((owned_u>0)&(owned_u<fixed['eps']))
 assert fixed['Q0_over_Hstar']==100;eta=fixed['Hunit']/299792458.;P.capture('registered_phase_eta',np.array(eta));Q0=fixed['Q0_over_Hstar']*eta;P.capture('registered_phase_Q0',np.array(Q0));xu=P.a_div64(P.a_div64(P.a_prod(s['phase_X'],s['phase_X']),np.array(Q0),P.capture,'clock_Q0_once'),np.array(Q0),P.capture,'clock_Q0_twice');xu=P.a_sub(xu,P.a_dd(np.ones(3784)));phase_pair_keep('clock_invariant_pressure_argument_u',xu,P.capture)
 u_gap=P.a_sub(xu,P.a_dd(owned_u));phase_pair_keep('clock_minus_owned_pressure_argument_gap',u_gap,P.capture)
 owned=P.a_dd(raw['unchanged_new_phase_canonical_density']);owned_gap=P.a_sub(out['registered_canonical_density'],owned);phase_pair_keep('owned_registered_construction_gap',owned_gap,P.capture)
 action_owned_gap=P.a_sub(out['action_canonical_density'],owned);phase_pair_keep('action_minus_owned_density_gap',action_owned_gap,P.capture)
 data=save_pairs(dict(out,owned_registered_density=owned,registered_minus_owned_density=owned_gap,action_minus_owned_density=action_owned_gap,clock_pressure_argument=xu,clock_minus_owned_pressure_argument_gap=u_gap),'completed_phase');data['owned_pressure_argument_u']=owned_u
 # A sufficient strict pair test proves positivity without collapsing its sign.
 H_lower=out['literal_hessian'][0]-abs(out['literal_hessian'][1]);P.capture('literal_Hessian_pair_lower_bound',H_lower);resolved_H=(H_lower>P.TOL*out['hessian_envelope']);P.capture('literal_Hessian_construction_margin',H_lower/np.maximum(out['hessian_envelope'],1e-30))
 clock_domain=(xu[0]>abs(xu[1]))&((fixed['eps']-xu[0])>abs(xu[1]));P.capture('clock_argument_pair_domain_test',clock_domain);positive=resolved_H&clock_domain;P.capture('literal_Hessian_resolved_positive_and_clock_domain_test',positive)
 P.check('column_%d_literal_Hessian_resolved_positive_and_clock_domain'%iq,positive.astype(float),np.ones(3784),np.ones(3784));data.update(literal_Hessian_pair_lower_bound=H_lower,literal_Hessian_construction_margin=H_lower/np.maximum(out['hessian_envelope'],1e-30),clock_argument_pair_domain_test=clock_domain)
 data.update({n:a for n,a in P.RAW.items() if n.startswith('control_')})
 data.update(owned_phi_first_jets=s['phi'],owned_X=s['phase_X'],owned_P_X=s['phase_PX'],owned_P_XX=s['phase_PXX'],owned_N=c['N'],owned_sqrt_h=c['sqrt_h'],owned_density=c['dens'])
 record=P.checkpoint('COLUMN',data,dict(kind='new_literal_phase_temporal_Hessian_and_current_charge',column=iq,configuration_parent=ref,EOS_domain_parent=domain_ref,current_phase_first_jets_held=True,strict_literal_positive=True,positive_sign_resolved_at_construction_tolerance=True,clock_X_in_bounded_EOS_domain=True,reduced_formula_is_diagnostic=True,registered_current_gap_retained=True,controls=P.CHECKS[-1:]))
 return out,owned,record


def contact_phase_points(contact_refs):
 full=P.a_dd(np.zeros((4,3784)))
 for iq,ref in enumerate(contact_refs):
  raw=P.read_pair(ref,('indices','delta_phase_delta_canonical_density_action_hi','delta_phase_delta_canonical_density_action_lo'))
  take=raw['indices'];assert take.shape==(4,) and take.dtype.kind in 'iu' and len(set(map(int,take)))==4 and np.all((take>=0)&(take<3784))
  for w,suffix in enumerate(('hi','lo')):full[w][iq,take]=raw['delta_phase_delta_canonical_density_action_'+suffix]
  phase_pair_keep('compact_phase_configuration_point_contact',full,P.capture)
 return P.a_reshape(full,(15136,))


def phase_packet(phase):
 geo=P.read_pair(phase['basis'],('R','dv','hats','cell_i','cell_j','r','z'));assert geo['R'].shape==geo['dv'].shape==(4,3784) and geo['hats'].shape==(4,4,3,86,44)
 P.checkpoint('INPUT',{n:a for n,a in geo.items()},dict(kind='fixed_current_literal_weak_phase_charge_Cauchy_prior_and_mass_preparation',phase_refs=phase,phase_velocity_space_free_dimension=3870,old_trace_scale_not_reused=True,physical_history=None,finite_physical_step=None))
 P.RAW.clear();P.AVAILABLE.clear();fresh_phase_hessian_control()
 columns=[phase_column(iq,ref,phase['domain_refs'][iq],phase['fixed']) for iq,ref in enumerate(phase['pilot_columns'])]
 H=tuple(np.concatenate([row[0]['literal_hessian'][w] for row in columns]) for w in (0,1));p=tuple(np.concatenate([row[0]['action_canonical_density'][w] for row in columns]) for w in (0,1));reg=tuple(np.concatenate([row[0]['registered_canonical_density'][w] for row in columns]) for w in (0,1));own=tuple(np.concatenate([row[1][w] for row in columns]) for w in (0,1))
 eH=np.concatenate([row[0]['hessian_envelope'] for row in columns]);P.RAW.clear();P.AVAILABLE.clear();P.CONTEXT.update(stage='new_fixed_weak_phase_charge_and_scalar_mass_preparation');P.capture('full_literal_Hessian_operation_envelope',eH)
 target=P.dd_scalar_scatter(p,geo,P.capture,'literal_phase_prior');phase_pair_keep('fixed_current_literal_weak_phase_charge',target,P.capture)
 reg_target=P.dd_scalar_scatter(reg,geo,P.capture,'registered_phase_readout');phase_pair_keep('registered_weak_phase_charge_readout',reg_target,P.capture)
 owned_target=P.dd_scalar_scatter(own,geo,P.capture,'owned_phase_readout');phase_pair_keep('owned_registered_weak_phase_charge',owned_target,P.capture)
 qpoints=contact_phase_points(phase['contact_columns']);Q=P.dd_scalar_scatter(qpoints,geo,P.capture,'compact_phase_configuration');phase_pair_keep('compact_literal_weak_phase_configuration_contact',Q,P.capture)
 rhs=(-Q[0],-Q[1]);phase_pair_keep('fixed_weak_charge_phase_velocity_rhs',rhs,P.capture)
 diagonal=phase_mass_diagonal(H,geo,P.capture,'new_phase_mass');mask=P.scalar_mask();assert np.count_nonzero(mask)==3870 and np.all(diagonal[0][mask]>abs(diagonal[1][mask]))
 test=P.a_dd(P.scalar_lift(((np.arange(87*45)%17)-8).reshape(87,45)/29));Mv=phase_mass_action(test,H,geo,P.capture,'new_phase_mass_functional');phase_pair_keep('new_phase_mass_on_registered_test',Mv,P.capture)
 value=phase_scalar_value(test,geo,P.capture,'new_phase_mass_test');weighted=P.a_mul(H,value);density_pair=P.a_mul(value,weighted);weight=(geo['dv']/geo['R']).reshape(15136)
 direct=phase_pair_sum(P.a_mul64(weight,density_pair),0,P.capture,'new_phase_mass_direct');nodal=phase_pair_sum(phase_pair_sum(P.a_mul(test,Mv),0,P.capture,'new_phase_mass_nodal_rows'),0,P.capture,'new_phase_mass_nodal')
 gap=P.a_sub(nodal,direct);phase_pair_keep('new_phase_mass_Q1_functional_gap',gap,P.capture);value_bound=abs(value[0])+abs(value[1]);nodal_bound=P.scalar_scatter(eH*value_bound,geo);bound=np.sum(abs(weight)*eH*value_bound**2)+np.sum((abs(test[0])+abs(test[1]))*nodal_bound);P.capture('new_phase_mass_functional_upstream_bound',np.array(bound))
 P.check('new_literal_phase_mass_Q1_functional',np.array(gap[0]+gap[1]),np.array(0.),np.array(bound))
 gapreg=P.a_sub(target,reg_target);phase_pair_keep('literal_minus_registered_weak_phase_charge_gap',gapreg,P.capture);gapown=P.a_sub(reg_target,owned_target);phase_pair_keep('registered_minus_owned_weak_phase_charge_gap',gapown,P.capture)
 values=dict(literal_Hessian=H,fixed_literal_weak_phase_charge=target,registered_weak_phase_charge=reg_target,owned_registered_weak_phase_charge=owned_target,literal_minus_registered_weak_gap=gapreg,registered_minus_owned_weak_gap=gapown,new_phase_mass_diagonal=diagonal,compact_literal_phase_configuration_contact=Q,fixed_weak_phase_velocity_rhs=rhs,new_phase_mass_test_response=Mv)
 data=save_pairs(values,'complete_phase_mass');data.update({n:a for n,a in P.RAW.items() if n.startswith('control_')})
 loads=P.checkpoint('LOADS',data,dict(kind='positive_literal_phase_Hessian_and_new_3870_scalar_mass_prepared',column_refs=[row[2] for row in columns],scalar_basis=phase['basis'],target_prior='prior_current_literal_action_weak_phase_density_unchanged',compact_contact_refs=phase['contact_columns'],phase_velocity_solve=None,phase_velocity_space_dimension=3870,positive_mass_from_strict_positive_H_and_independent_basis=True,global_I0_profile_determined=False,correction_mixed_jets='same scalar value/R/Z basis required at next solve; full existing phi_t spatial jets not assumed zero',joint_normal_and_initial_CMC_step=None,controls=P.CHECKS[-1:]))
 assert len(P.CHECKS)==6 and len(P.RECORDS)==7 and all(c['passed'] for c in P.CHECKS)
 return dict(status='LITERAL_PHASE_HESSIAN_POSITIVE_AND_FIXED_WEAK_CHARGE_MASS_PREPARED',literal_Hessian_positive=True,phase_velocity_space_dimension=3870,phase_mass_positive=True,loads=loads,controls=P.CHECKS,checkpoints=P.RECORDS,phase_charge_restored=False,phase_velocity_solved=False,configuration_updated=False,physical_adoption=False)


def outputs_recheck():
 assert P.sha(__file__)==P.OWNER['source_sha256']
 for name,h in P.OUTPUTS.items():assert P.sha(P.path(name))==h,('output changed',name)


def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and PROTOCOL_SHA is not None,'Root full review and release required'
 assert not list(BASE.glob(STEM+'_*')),'Fresh exclusive output namespace required'
 initialize();bind(STEM+'.md',PROTOCOL_SHA);pins,phase=phase_preparation_admission()
 for name,h in pins.items():bind(name,h)
 P.OWNER=dict(pid=os.getpid(),source_file=Path(__file__).name,source_sha256=P.sha(__file__),started_utc=P.now(),execution='root_owned_new_literal_phase_Hessian_and_mass_preparation');P.json_file(STEM+'_OWNER_START.json',P.OWNER)
 try:
  case=phase_packet(phase);P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(case,owner=P.OWNER,qualification=P.FLAGS));outputs_recheck();P.json_file(STEM+'_RECEIPT.json',dict(status='CLOSED',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),result_sha256=rh,error_sha256=None,closed_utc=P.now(),qualification=P.FLAGS));outputs_recheck();print(json.dumps(dict(status=case['status'],controls=len(P.CHECKS),pairs=len(P.RECORDS))),flush=True)
 except BaseException:
  arrays={**P.RAW,**P.AVAILABLE};arrays.update(P.DD_ARRAY_CURRENT.get('arrays',{}))
  if arrays:P.checkpoint('ERROR_RAW',arrays,dict(kind='available_literal_phase_Hessian_charge_and_mass_operands',context=P.CONTEXT),failed=True)
  P.seal_actual();eh=P.json_file(STEM+'_ERROR.json',dict(status='FAILED',owner=P.OWNER,input_sha256=P.INPUTS,controls=P.CHECKS,checkpoints=P.RECORDS,context=P.CONTEXT,qualification=P.FLAGS,traceback=traceback.format_exc()));prior=BASE/(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(status='CLOSED_ERROR',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,closed_utc=P.now(),qualification=P.FLAGS));raise

if __name__=='__main__':main()

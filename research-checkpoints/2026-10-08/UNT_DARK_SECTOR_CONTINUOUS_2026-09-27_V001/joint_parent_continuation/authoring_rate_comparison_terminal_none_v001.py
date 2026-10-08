"""Prospective bounded SAME-operand registered rate derivative comparison."""
from pathlib import Path
import importlib.util,hashlib,json,os,sys,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_REGISTERED_NORMAL_RATE_SPECIALIZATION_COMPARISON_V001'
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=True
PROTOCOL_SHA=None
RESPONSE_TERMINAL=dict(pid=None,result_sha256=None,receipt_sha256=None)
ADMISSION=None
ADMISSION_SHA=None
PROVIDER='cross_u_combined_configuration_normal_derivative_v001.py'
PROVIDER_SHA='e139a418838005d8db5498ccacca6afeed0092628a96886d61d7b5f3a86d49d0'
SPECIALIZATION='author_fragment_registered_normal_rate_specialization_v002.py'
SPECIALIZATION_SHA='4edfc21db69afbbdfaa08c365f335c664c96233480553afc32c74cbfea21103f'
COMPARISON='author_fragment_one_response_rate_comparison_v001.py'
COMPARISON_SHA=None
PATCH_NODES=((43,22),(21,11),(64,33))
R=P=N=A=np=None

def bind(n,h):
 p=Path(n);p=p if p.is_absolute() else BASE/p;assert h is not None and P.sha(p)==h,n
 key=str(p.resolve());assert key not in P.INPUTS or P.INPUTS[key]==h;P.INPUTS[key]=h;return p
def keep(n,x):return ORIGINAL_CAPTURE(n,np.asarray(x).copy())
def pair(n,x):return normal_keep_pair(n,x,keep)
def thin(q):return {n:q[n] for n in ('file','sha256','commit_file','commit_sha256')}
def arrays():return {n:np.asarray(x).copy() for n,x in {**P.RAW,**P.AVAILABLE,**P.DD_ARRAY_CURRENT.get('arrays',{})}.items()}
def reset(stage,preserved=None,**context):
 P.RAW.clear();P.AVAILABLE.clear();P.DD_ARRAY_CURRENT.clear();P.CONTEXT.clear();P.CONTEXT.update(stage=stage,**context)
 if preserved:P.AVAILABLE.update(preserved)

def retained_inputs(prefix,obj,out):
 if isinstance(obj,dict):
  for n,x in obj.items():retained_inputs(prefix+'_'+n,x,out)
 elif isinstance(obj,tuple):
  for i,x in enumerate(obj):retained_inputs(prefix+('_hi' if i==0 else '_lo' if i==1 else '_%d'%i),x,out)
 elif isinstance(obj,(np.ndarray,np.generic)):
  out[prefix]=np.asarray(obj).copy();keep(prefix,out[prefix])

def initialize():
 global R,P,N,A,np,ORIGINAL_CAPTURE,C,ALPHA,ELL,B,GC
 assert hashlib.sha256((BASE/PROVIDER).read_bytes()).hexdigest()==PROVIDER_SHA
 spec=importlib.util.spec_from_file_location('reviewed_full_rate_derivative_definitions',BASE/PROVIDER);R=importlib.util.module_from_spec(spec);spec.loader.exec_module(R);R.initialize()
 P,N,A,np=R.P,R.N,R.A,R.np;ORIGINAL_CAPTURE=R.ORIGINAL_CAPTURE;P.capture=N.capture=A.capture=keep
 P.STEM=STEM;P.__file__=__file__;P.PROTOCOL_SHA=PROTOCOL_SHA
 P.FLAGS=dict(whole_grid_arithmetic_qualified=False,canonical_target_response_qualified=False,physical_constraint_qualified=False,primitive_legendre_bridge_resolved=False,physical_exterior_adopted=False,finite_configuration_adopted=False,global_rank_admitted=False,physical_adoption=False)
 C,ALPHA,ELL,B,GC=R.C,R.ALPHA,R.ELL,R.B,R.GC
 for n in ('a_dd','a_add','a_sub','a_mul','a_mul64','a_prod','a_matvec','a_stack','a_slice','a_transpose','a_reshape','a_div64'):globals()[n]=getattr(P,n)
 for n in ('normal_keep_pair','normal_pair_sum','normal_pair_left','normal_pair_right','normal_pair_sandwich','normal_pair_connection_from_jet','normal_action_dot','normal_action_reduce','paired_normal_chart_jets','paired_normal_lift','paired_normal_metric_delta','normal_positive_features','normal_positive_direction','connection_from_jet_envelope'):globals()[n]=getattr(N,n)
 for n in ('normal_contact_connection','normal_contact_test_derivatives','combined_normal_native_contact','combined_normal_z0_contact','combined_normal_absolute_phase_contact','combined_normal_EH_contact'):globals()[n]=getattr(R,n)
 globals().update(path=P.path,INPUTS=P.INPUTS)
 for n,h in ((PROVIDER,PROVIDER_SHA),(SPECIALIZATION,SPECIALIZATION_SHA),(COMPARISON,COMPARISON_SHA),(ADMISSION,ADMISSION_SHA),(STEM+'.md',PROTOCOL_SHA),(__file__,P.sha(__file__))):bind(n,h)
 for n in (SPECIALIZATION,COMPARISON,ADMISSION):exec(compile((BASE/n).read_text(),str(BASE/n),'exec'),globals())

def patch_geometry(refs):
 raw=P.read_pair(refs['input'],tuple('original_basis_'+n for n in ('R','dv','hats','cell_i','cell_j','r','z')))
 g={n.removeprefix('original_basis_'):x for n,x in raw.items()};assert g['R'].shape==g['dv'].shape==(4,3784) and g['hats'].shape==(4,4,3,86,44)
 patches=[]
 for i,j in PATCH_NODES:
  take=np.flatnonzero(((g['cell_i']==i-1)|(g['cell_i']==i))&((g['cell_j']==j-1)|(g['cell_j']==j)))
  assert len(take)==4;patches.append(take)
 take=np.concatenate(patches);assert len(set(take.tolist()))==12
 keep('predeclared_patch_nodes',np.asarray(PATCH_NODES,dtype=np.int64));keep('predeclared_patch_point_indices',take)
 return g,take

def saved_rate_fields(ref,take):
 sc=ref['metadata']['schema'];names=tuple(n for n in sc if n.startswith(('NEW_rate_first_jet_','NEW_rate_feature_','NEW_rate_momentum_','NEW_local_native_rate_values_','NEW_local_physical_metric_rate_values_')))
 assert names and all(n[:-3]+'_lo' in sc for n in names if n.endswith('_hi'))
 raw=P.read_pair(ref,names);mode={'dz','nz','q','V','D','V_raised','D_raised','Pi'}
 def family(prefix):
  out={}
  for n in names:
   if n.startswith(prefix) and n.endswith('_hi'):
    key=n[len(prefix):-3];axis=1 if key in mode else 0;out[key]=(np.take(raw[n],take,axis=axis),np.take(raw[n[:-3]+'_lo'],take,axis=axis))
  return out
 jets=family('NEW_rate_first_jet_');feature=dict(paired=family('NEW_rate_feature_'));moments=family('NEW_rate_momentum_')
 values=[tuple(raw[n+'_'+w][take] for w in ('hi','lo')) for n in ('NEW_local_native_rate_values','NEW_local_physical_metric_rate_values')]
 del raw
 assert set(jets)=={'du','dz','dg','Ga'} and all(n in moments for n in ('K','Ktrace','metric_EH_tensor','native_density','metric_total_density'))
 return jets,feature,moments,values[0],values[1]

def comparison_column(iq,refs,take):
 reset('bounded_rate_comparison_column',column=iq)
 s,c,jets,F,moments,op,_=N.load_pilot_column(refs['pilot_columns'][iq]);s['du']=jets['du'][0];s['dz']=jets['dz'][0]
 s,c,jets,F,moments,op=R.take_point_fields(s,c,jets,F,moments,op,take)
 rj,rf,rm,y,k=saved_rate_fields(refs['rate_columns'][iq],take)
 rop=rate_comparison_positive_increment(s,c,y,k,keep,'new_response_operation_bound');rcj=paired_normal_chart_jets(s,c,rj,keep,'new_response_chart')
 column=rate_normal_column_cache(s,c,jets,moments,refs['gap_refs'],keep,'current_common_cache');data=dict(point_indices=take.copy());completed={}
 for n,x in dict(s=s,c=c,current_first_jets=jets,current_feature=F,current_moments=moments,current_bounds=op,new_first_jets=rj,new_feature=rf,new_moments=rm,new_native_values=y,new_physical_metric_values=k,new_bounds=rop,new_chart=rcj,column_cache=column).items():retained_inputs('same_operand_'+n,x,completed)
 shapes=dict(native_metric_terms=(12,4,4,7),mode_compensation_terms=(12,4,4,7),absolute_phase_terms=(12,4,4,2),EH_terms=(12,4,4,3),component_densities=(12,4,4,4),coefficient=(12,4,4))
 fast={n:a_dd(np.zeros(sh)) for n,sh in shapes.items()};full={n:a_dd(np.zeros(sh)) for n,sh in shapes.items()};env={n:np.zeros(sh) for n,sh in shapes.items()}
 for row in range(4):
  for jet in range(4):
   reset('bounded_rate_comparison_direction',completed,column=iq,row=row,test_jet=jet);f,df,b,db=R.direction_test(12,row,jet)
   a,z,delta,e=rate_comparison_direction(s,c,jets,F,moments,op,rj,rf,rm,rop,rcj,column,f,df,b,db,keep,'current_direction')
   for n in shapes:
    for w in (0,1):fast[n][w][:,row,jet]=a[n][w];full[n][w][:,row,jet]=z[n][w]
    env[n][:,row,jet]=e[n]
    for family,x in (('specialized',fast[n]),('full',full[n])):
     pair('completed_'+family+'_'+n,x)
     for w,suffix in enumerate(('hi','lo')):completed[family+'_'+n+'_'+suffix]=x[w].copy()
    completed[n+'_implementation_envelope']=env[n].copy()
   for n,x in a['construction_gaps'].items():
    for w,suffix in enumerate(('hi','lo')):completed['direction_%d_%d_%s_gap_%s'%(row,jet,n,suffix)]=x[w].copy()
 differences=[]
 for n in shapes:
  x=a_sub(fast[n],full[n]);pair('completed_'+n+'_specialized_minus_full',x);differences.append(x)
 actual=np.concatenate([(x[0]+x[1]).ravel() for x in differences]);bounds=np.concatenate([env[n].ravel() for n in shapes]);P.check('bounded_same_operand_rate_families_column_%d'%iq,actual,np.zeros_like(actual),bounds)
 cmc=rate_normal_CMC_contact(s,c,k,rm,keep,'same_response_CMC');eK=abs(c['N'])[:,None,None]*rop['Ga'][:,0,1:,1:];ec=abs(c['sqrt_h'])*np.einsum('pij,pij->p',abs(c['ih']),eK)
 ek=np.zeros((12,3,3))
 for a,(i,j) in enumerate(((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))):ek[:,i,j]=ek[:,j,i]=abs(k[0][:,a])+abs(k[1][:,a])
 ec+=abs(c['sqrt_h']*c['N']*s['hi'][:,0,0]/2)*np.einsum('pij,pij->p',abs(c['ih']),ek)
 P.check('bounded_CMC_Gamma_chain_against_same_affine81_column_%d'%iq,cmc['Gamma_chain_minus_affine81'][0]+cmc['Gamma_chain_minus_affine81'][1],np.zeros(12),ec)
 for n,x in cmc.items():
  if isinstance(x,tuple):
   pair('CMC_'+n,x)
   for w,suffix in enumerate(('hi','lo')):completed['CMC_'+n+'_'+suffix]=x[w].copy()
 actual_cmc=a_mul64(c['sqrt_h'],rm['Ktrace']);pair('CMC_actual_affine81_density',actual_cmc)
 for w,suffix in enumerate(('hi','lo')):completed['CMC_actual_affine81_density_'+suffix]=actual_cmc[w].copy()
 completed['CMC_implementation_envelope']=ec;data.update(completed);data.update({n:x for n,x in P.RAW.items() if n.startswith('control_')})
 rec=P.checkpoint('COLUMN',data,dict(kind='bounded_same_response_all_sixteen_registered_rate_test_comparison',column=iq,patch_nodes=PATCH_NODES,pilot_ref=thin(refs['pilot_columns'][iq]),rate_ref=thin(refs['rate_columns'][iq]),literal_response_qualification=refs['source_qualification'],all_primary_test_directions_retained=True,gap_refs=refs['gap_refs'],physical_ports=None,whole_grid_arithmetic_qualified=False))
 return data,rec

def paired_normal_test_values(test,g):
 t=N.extend_normal_tests(test);out=a_dd(np.zeros((15136,4,3)))
 for iq in range(4):
  sl=slice(iq*3784,(iq+1)*3784)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   for row in range(4):
    for jet,hat in enumerate(N.normal_hat_jet(g,iq,corner,row)):
     x=a_prod(t[row,di:86+di,dj:44+dj],hat);x=a_reshape(x,(3784,));value=a_add(a_slice(out,(sl,row,jet)),x)
     for w in (0,1):out[w][sl,row,jet]=value[w]
     pair('current_normal_test_polynomial_transpose',out)
 return out

def paired_scalar_test_values(test,g):
 t=P.scalar_lift(test);out=a_dd(np.zeros(15136))
 for iq in range(4):
  sl=slice(iq*3784,(iq+1)*3784)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   term=a_reshape(a_prod(t[di:86+di,dj:44+dj],g['hats'][iq,corner,0]),(3784,));value=a_add(a_slice(out,sl),term)
   for w in (0,1):out[w][sl]=value[w]
   pair('current_scalar_test_polynomial_transpose',out)
 return out

def comparison_packet(refs):
 reset('geometry_selection_before_response_values');g,take=patch_geometry(refs)
 inp=P.checkpoint('INPUT',{**g,**arrays()},dict(kind='predeclared_three_owned_geometry_patches',patch_nodes=PATCH_NODES,point_count=48,response_terminal=RESPONSE_TERMINAL,source_qualification=refs['source_qualification'],gap_refs=refs['gap_refs'],current_refs=[thin(q) for q in refs['pilot_columns']],response_refs=[thin(q) for q in refs['rate_columns']],physical_ports=None))
 cols=[];records=[]
 for iq in range(4):q,rec=comparison_column(iq,refs,take);cols.append(q);records.append(rec)
 reset('bounded_patch_new_normal_and_CMC_functionals');data={};test=(np.arange(4*87*45).reshape(4,87,45)%17-8)/31.;test*=N.normal_test_mask();tv=paired_normal_test_values(test,g);weight=(g['dv']/g['R']).reshape(15136)
 scalar_test=(np.arange(87*45).reshape(87,45)%19-9)/37.;scalar_test*=P.scalar_mask();scalar_tv=paired_scalar_test_values(scalar_test,g)
 data['normal_functional_test']=test.copy();data['scalar_functional_test']=scalar_test.copy()
 for patch in range(3):
  fields={};envelope=np.zeros((15136,4,3))
  for family in ('specialized','full'):
   value=a_dd(np.zeros((15136,4,3)))
   for iq,q in enumerate(cols):
    ids=iq*3784+take[patch*4:patch*4+4]
    for w,suffix in enumerate(('hi','lo')):value[w][ids]=-q[family+'_coefficient_'+suffix][patch*4:patch*4+4,:,:3]
    envelope[ids]=q['coefficient_implementation_envelope'][patch*4:patch*4+4,:,:3]
   weak=N.paired_scatter_normal(value,g,'patch_%d_%s_normal'%(patch,family));pair('completed_patch_%d_%s_normal'%(patch,family),weak);fields[family]=weak
   nodal=normal_action_reduce(a_mul64(test,weak),(0,1,2));pair('patch_%d_%s_normal_nodal'%(patch,family),nodal)
   direct=normal_action_reduce(a_mul64(weight,normal_action_reduce(a_mul(value,tv),(1,2))),(0,));pair('patch_%d_%s_normal_direct'%(patch,family),direct);gap=a_sub(nodal,direct);pair('patch_%d_%s_normal_gap'%(patch,family),gap)
   for n,x in (('weak_normal',weak),('functional_nodal',nodal),('functional_direct',direct),('functional_gap',gap)):
    pair('patch_%d_%s_%s'%(patch,family,n),x)
    for w,suffix in enumerate(('hi','lo')):data['patch_%d_%s_%s_%s'%(patch,family,n,suffix)]=x[w].copy()
   en=N.scatter_normal_envelope(envelope,g);bound=np.sum(abs(test)*en)+np.sum(weight[:,None,None]*(abs(tv[0])+abs(tv[1]))*envelope)
   P.check('patch_%d_%s_exact_normal_polynomial_functional'%(patch,family),np.asarray(gap[0]+gap[1]),np.asarray(0.),np.asarray(bound))
  difference=a_sub(fields['specialized'],fields['full']);pair('patch_%d_weak_normal_difference'%patch,difference);P.check('patch_%d_specialized_full_weak_normal'%patch,difference[0]+difference[1],np.zeros((4,87,45)),2*N.scatter_normal_envelope(envelope,g))
  for w,suffix in enumerate(('hi','lo')):data['patch_%d_weak_normal_difference_%s'%(patch,suffix)]=difference[w].copy()
  cmc_fields={};cmc_envelope=np.zeros(15136)
  for family,source in (('specialized','CMC_Gamma_density'),('full','CMC_actual_affine81_density')):
   density=a_dd(np.zeros(15136))
   for iq,q in enumerate(cols):
    ids=iq*3784+take[patch*4:patch*4+4]
    for w,suffix in enumerate(('hi','lo')):density[w][ids]=q[source+'_'+suffix][patch*4:patch*4+4]
    cmc_envelope[ids]=q['CMC_implementation_envelope'][patch*4:patch*4+4]
   pair('completed_patch_%d_%s_CMC_density'%(patch,family),density)
   weak=P.dd_scalar_scatter(density,g,keep,'patch_%d_%s_CMC'%(patch,family));pair('completed_patch_%d_%s_CMC_weak'%(patch,family),weak);cmc_fields[family]=weak
   nodal=normal_action_reduce(a_mul64(scalar_test,weak),(0,1));pair('patch_%d_%s_CMC_nodal'%(patch,family),nodal)
   direct=normal_action_reduce(a_mul64(weight,a_mul(density,scalar_tv)),(0,));pair('patch_%d_%s_CMC_direct'%(patch,family),direct);gap=a_sub(nodal,direct);pair('patch_%d_%s_CMC_gap'%(patch,family),gap)
   for n,x in (('density',density),('weak',weak),('functional_nodal',nodal),('functional_direct',direct),('functional_gap',gap)):
    for w,suffix in enumerate(('hi','lo')):data['patch_%d_%s_CMC_%s_%s'%(patch,family,n,suffix)]=np.asarray(x[w]).copy()
   en=P.scalar_scatter(cmc_envelope,g);bound=np.sum(abs(scalar_test)*en)+np.sum(weight*(abs(scalar_tv[0])+abs(scalar_tv[1]))*cmc_envelope)
   P.check('patch_%d_%s_exact_scalar_CMC_functional'%(patch,family),np.asarray(gap[0]+gap[1]),np.asarray(0.),np.asarray(bound))
  difference=a_sub(cmc_fields['specialized'],cmc_fields['full']);pair('patch_%d_weak_CMC_difference'%patch,difference);P.check('patch_%d_specialized_full_weak_CMC'%patch,difference[0]+difference[1],np.zeros((87,45)),2*P.scalar_scatter(cmc_envelope,g))
  for w,suffix in enumerate(('hi','lo')):data['patch_%d_weak_CMC_difference_%s'%(patch,suffix)]=difference[w].copy()
 data.update({n:x for n,x in P.RAW.items() if n.startswith('control_')});loads=P.checkpoint('LOADS',data,dict(kind='bounded_patch_rate_implementation_functionals',columns=[thin(q) for q in records],source_qualification=refs['source_qualification'],patch_nodes=PATCH_NODES,whole_grid_arithmetic_qualified=False,canonical_target_response_qualified=False,physical_constraint_qualified=False,gap_refs=refs['gap_refs'],physical_ports=None))
 assert len(P.CHECKS)==26 and len(P.RECORDS)==6
 return dict(status='BOUNDED_REGISTERED_RATE_SPECIALIZATION_COMPARED',input=inp,columns=records,loads=loads,source_qualification=refs['source_qualification'],whole_grid_arithmetic_qualified=False,canonical_target_response_qualified=False,physical_adoption=False)

def outputs_recheck():
 assert P.sha(__file__)==P.OWNER['source_sha256']
 for n,h in P.OUTPUTS.items():assert P.sha(P.path(n))==h,n

def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and all(v is not None for v in RESPONSE_TERMINAL.values()) and all(x is not None for x in (PROTOCOL_SHA,ADMISSION,ADMISSION_SHA,COMPARISON_SHA)),'Future terminal and full review required before I/O'
 assert not list(BASE.glob(STEM+'_*')),'Fresh exclusive namespace required'
 initialize();P.OWNER=dict(pid=os.getpid(),source_file=Path(__file__).name,source_sha256=P.sha(__file__),started_utc=P.now());P.json_file(STEM+'_OWNER_START.json',P.OWNER)
 try:
  pins,refs=rate_comparison_admission();case=comparison_packet(refs);P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(case,owner=P.OWNER,controls=P.CHECKS,checkpoints=P.RECORDS,qualification=P.FLAGS));outputs_recheck();P.json_file(STEM+'_RECEIPT.json',dict(status='CLOSED',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),result_sha256=rh,error_sha256=None,closed_utc=P.now(),qualification=P.FLAGS));outputs_recheck();return 0
 except BaseException:
  raw=arrays()
  if raw:P.checkpoint('ERROR_RAW',raw,dict(kind='bounded_same_response_comparison_partial_operands',context=P.CONTEXT),failed=True)
  P.seal_actual();eh=P.json_file(STEM+'_ERROR.json',dict(status='FAILED',owner=P.OWNER,controls=P.CHECKS,checkpoints=P.RECORDS,context=P.CONTEXT,qualification=P.FLAGS,traceback=traceback.format_exc()));prior=BASE/(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(status='CLOSED_ERROR',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,closed_utc=P.now(),qualification=P.FLAGS));raise
if __name__=='__main__':sys.exit(main())

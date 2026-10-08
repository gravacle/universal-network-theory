"""Definitions only: reusable whole-grid fixed-configuration Frechet assembler.
The containing NEW producer must call whole_rate_terminal_gate BEFORE any I/O,
then authenticate its completed current/increment columns and comparison proof.
No admission, loader, producer, old fixture, inverse, solve or affine66/81 call
is defined here. An increment supplies saved jets/features/momenta and genuine
native99/physical6 values; current configuration/phase/source/gauge are fixed.
Caller supplies np, reviewed208 specialization (seven unchanged definitions),
reviewed positive64 increment bound, registered98 positive chains, direction_test,
DD a_*/normal_action_*, N/P original normal/scalar Q1 assembly, keep and check.
check is the original 2e-11 operation-bound control with 1e-30 denominator floor.

One current column/chart is cached once. Each of its sixteen test caches is
used for EVERY supplied increment before moving to the next test. Rate charts
and positive features are prepared once per increment. Scratch labels are reused;
completed families and all four construction-gap families are copied immediately.
Caller retains each completed COLUMN before loading the next owned Gauss column.
All scalar publication paths use np.asarray(x).copy(), including DD words.

The four normal rows are minus the registered action variation, with original
F/hat/weight polynomial-transpose assembly and all time-primary coefficients
retained separately. Initial CMC uses saved affine81 sqrt_h*delta(Ktrace);
Gamma/ADM/affine81 gaps remain explicit. Phase and ordinary rate contacts vanish
only in this fixed-configuration derivative; their primal rows are not replaced.
Original canonical/literal qualification and all inherited gaps remain metadata.
Weak functional PASS is arithmetic qualification only. A refused inverse may
be an implementation diagnostic; it is never adopted as a canonical/Jacobian
direction. No finite increment-squared, stationarity, rank or physical claim.
"""
WHOLE_RATE_AUTHOR_DRAFT=True
WHOLE_RATE_AUTHORING_IN_PROGRESS=False
WHOLE_RATE_ARITHMETIC_TOL=2e-11

def whole_rate_terminal_gate(terminal):
 assert WHOLE_RATE_AUTHOR_DRAFT is False and WHOLE_RATE_AUTHORING_IN_PROGRESS is False
 assert all(terminal.get(n) is not None for n in ('pid','result_sha256','receipt_sha256')),'Actual natural CLOSED complete operands required before I/O'

def whole_rate_pair(keep,label,name,x,data=None):
 normal_keep_pair(label+'_'+name,x,keep)
 if data is not None:
  for w,suffix in enumerate(('hi','lo')):data[name+'_'+suffix]=np.asarray(x[w]).copy()
 return x

def whole_rate_column(terminal,current,increments,gap_refs,keep,check,label):
 whole_rate_terminal_gate(terminal)
 s,c,jets,F,moments,op=(current[n] for n in ('s','c','jets','feature','moments','operation_bounds'))
 p=len(s['U']);assert p==3784 and increments and len(set(increments))==len(increments)
 column=rate_normal_column_cache(s,c,jets,moments,gap_refs,keep,label+'_current_common')
 shapes=dict(native_metric_terms=(p,4,4,7),mode_compensation_terms=(p,4,4,7),absolute_phase_terms=(p,4,4,2),EH_terms=(p,4,4,3),component_densities=(p,4,4,4),coefficient=(p,4,4))
 prepared={};outputs={}
 for name,r in increments.items():
  assert all(n in r for n in ('jets','feature','moments','native_value','metric_value','source_qualification','reference'))
  assert r['native_value'][0].shape==r['native_value'][1].shape==(p,99) and r['metric_value'][0].shape==r['metric_value'][1].shape==(p,6)
  rop=rate_comparison_positive_increment(s,c,r['native_value'],r['metric_value'],keep,label+'_'+name+'_positive_increment')
  rcj=paired_normal_chart_jets(s,c,r['jets'],keep,label+'_'+name+'_rate_chart')
  positive={n:op[n]+rop[n] for n in ('du','dz','dg','Ga')}
  ef=normal_positive_features(s,c,positive,keep,label+'_'+name+'_positive_features')
  prepared[name]=dict(rop=rop,chart=rcj,positive=positive,feature_bound=ef)
  outputs[name]=dict(data={},families={n:a_dd(np.zeros(sh)) for n,sh in shapes.items()},envelopes={n:np.zeros(sh) for n,sh in shapes.items()},source_qualification=r['source_qualification'],reference=r['reference'],gap_refs=gap_refs)
 zero_curvature=dict(envelope_Q=np.zeros(p),envelope_V=np.zeros((p,3)))
 for row in range(4):
  for jet in range(4):
   f,dt,b,db=direction_test(p,row,jet)
   cache=rate_normal_test_cache(s,c,jets,F,column,f,dt,b,db,keep,label+'_current_test')
   for name,r in increments.items():
    ready=prepared[name];out=outputs[name];data=out['data']
    for n,x in cache['construction_gaps'].items():whole_rate_pair(keep,label+'_'+name,'direction_%d_%d_%s_gap'%(row,jet,n),x,data)
    value=rate_normal_direction(s,c,F,moments,r['jets'],r['feature'],r['moments'],ready['chart'],column,cache,keep,label+'_'+name+'_direction')
    for n,shape in shapes.items():
     assert value[n][0].shape==value[n][1].shape==shape[:1]+shape[3:]
     for w in (0,1):out['families'][n][w][:,row,jet]=value[n][w]
     whole_rate_pair(keep,label+'_'+name,'completed_'+n,out['families'][n])
    envelope=normal_positive_direction(s,c,ready['positive'],ready['feature_bound'],zero_curvature,f,dt,b,db,keep,label+'_'+name+'_positive_direction')
    for n in shapes:
     out['envelopes'][n][:,row,jet]=4*envelope[n]
     assert np.all(np.isfinite(out['envelopes'][n])) and np.all(out['envelopes'][n]>=0)
     keep(label+'_'+name+'_completed_'+n+'_envelope',np.asarray(out['envelopes'][n]).copy())
 for name,r in increments.items():
  out=outputs[name];data=out['data'];ready=prepared[name]
  for n,x in out['families'].items():
   whole_rate_pair(keep,label+'_'+name,n,x,data);data[n+'_operation_envelope']=np.asarray(out['envelopes'][n]).copy()
  cmc=rate_normal_CMC_contact(s,c,r['metric_value'],r['moments'],keep,label+'_'+name+'_CMC')
  eK=abs(c['N'])[:,None,None]*ready['rop']['Ga'][:,0,1:,1:]
  ec=abs(c['sqrt_h'])*np.einsum('pij,pij->p',abs(c['ih']),eK);ek=np.zeros((p,3,3))
  for a,(i,j) in enumerate(((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))):ek[:,i,j]=ek[:,j,i]=abs(r['metric_value'][0][:,a])+abs(r['metric_value'][1][:,a])
  ec+=abs(c['sqrt_h']*c['N']*s['hi'][:,0,0]/2)*np.einsum('pij,pij->p',abs(c['ih']),ek)
  cmc['Gamma_minus_ADM']=a_sub(cmc['Gamma_density'],cmc['ADM_density'])
  cmc['affine81_density']=a_mul64(c['sqrt_h'],r['moments']['Ktrace'])
  for n,x in cmc.items():
   if isinstance(x,tuple):whole_rate_pair(keep,label+'_'+name,'CMC_'+n,x,data)
  data['CMC_operation_envelope']=np.asarray(ec).copy();keep(label+'_'+name+'_CMC_operation_envelope',data['CMC_operation_envelope'])
  gap=cmc['Gamma_chain_minus_affine81'];check(label+'_'+name+'_CMC_Gamma_against_same81',np.asarray(gap[0]+gap[1]).copy(),np.zeros(p),ec)
  out.pop('families');out.pop('envelopes')
 return outputs

def whole_rate_test_polynomials(normal_test,scalar_test,g,keep,label):
 assert normal_test.shape==(4,87,45) and scalar_test.shape==(87,45)
 assert np.all(normal_test[~N.normal_test_mask()]==0) and np.all(scalar_test[~P.scalar_mask()]==0)
 t=N.extend_normal_tests(normal_test);u=P.scalar_lift(scalar_test)
 tv=a_dd(np.zeros((15136,4,3)));sv=a_dd(np.zeros(15136))
 for iq in range(4):
  sl=slice(iq*3784,(iq+1)*3784)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   for row in range(4):
    for jet,hat in enumerate(N.normal_hat_jet(g,iq,corner,row)):
     term=a_reshape(a_prod(t[row,di:86+di,dj:44+dj],hat),(3784,));value=a_add(a_slice(tv,(sl,row,jet)),term)
     for w in (0,1):tv[w][sl,row,jet]=value[w]
     whole_rate_pair(keep,label,'normal_polynomial_transpose',tv)
   term=a_reshape(a_prod(u[di:86+di,dj:44+dj],g['hats'][iq,corner,0]),(3784,));value=a_add(a_slice(sv,sl),term)
   for w in (0,1):sv[w][sl]=value[w]
   whole_rate_pair(keep,label,'scalar_polynomial_transpose',sv)
 return tv,sv

def whole_rate_assemble(terminal,columns,g,normal_test,scalar_test,keep,check,label):
 whole_rate_terminal_gate(terminal)
 assert len(columns)==4 and g['R'].shape==g['dv'].shape==(4,3784) and g['hats'].shape==(4,4,3,86,44)
 assert np.all(g['R']>0) and np.all(g['dv']>0) and np.all(g['hats'][:,:,0]>=0)
 names=tuple(columns[0]);assert all(tuple(q)==names for q in columns)
 tv,sv=whole_rate_test_polynomials(normal_test,scalar_test,g,keep,label+'_test');weight=(g['dv']/g['R']).reshape(15136)
 result={}
 for name in names:
  metadata=columns[0][name];assert all(q[name]['source_qualification']==metadata['source_qualification'] and q[name]['gap_refs']==metadata['gap_refs'] for q in columns)
  value=a_dd(np.zeros((15136,4,3)));primary=a_dd(np.zeros((15136,4)));density=a_dd(np.zeros(15136));envelope=np.zeros((15136,4,3));ec=np.zeros(15136);data={}
  for iq,q in enumerate(columns):
   sl=slice(iq*3784,(iq+1)*3784);d=q[name]['data']
   for w,suffix in enumerate(('hi','lo')):
    value[w][sl]=-d['coefficient_'+suffix][:,:,:3];primary[w][sl]=d['coefficient_'+suffix][:,:,3];density[w][sl]=d['CMC_affine81_density_'+suffix]
   envelope[sl]=d['coefficient_operation_envelope'][:,:,:3];ec[sl]=d['CMC_operation_envelope']
   for n,x in (('normal_action_negative_density',value),('time_primary_action_coefficients',primary),('initial_CMC_density',density)):whole_rate_pair(keep,label+'_'+name,n,x,data)
  weak=N.paired_scatter_normal(value,g,label+'_'+name+'_normal');whole_rate_pair(keep,label+'_'+name,'weak_normal',weak,data)
  nodal=normal_action_reduce(a_mul64(normal_test,weak),(0,1,2));whole_rate_pair(keep,label+'_'+name,'normal_functional_nodal',nodal,data)
  direct=normal_action_reduce(a_mul64(weight,normal_action_reduce(a_mul(value,tv),(1,2))),(0,));whole_rate_pair(keep,label+'_'+name,'normal_functional_direct',direct,data)
  gap=a_sub(nodal,direct);whole_rate_pair(keep,label+'_'+name,'normal_functional_gap',gap,data)
  en=N.scatter_normal_envelope(envelope,g);bound=np.sum(abs(normal_test)*en)+np.sum(weight[:,None,None]*(abs(tv[0])+abs(tv[1]))*envelope)
  data['normal_functional_operation_envelope']=np.asarray(bound).copy();keep(label+'_'+name+'_normal_functional_operation_envelope',data['normal_functional_operation_envelope'])
  check(label+'_'+name+'_normal_polynomial_transpose_functional',np.asarray(gap[0]+gap[1]).copy(),np.asarray(0.).copy(),np.asarray(bound).copy())
  trace=P.dd_scalar_scatter(density,g,keep,label+'_'+name+'_CMC');whole_rate_pair(keep,label+'_'+name,'weak_initial_CMC',trace,data)
  nodal=normal_action_reduce(a_mul64(scalar_test,trace),(0,1));whole_rate_pair(keep,label+'_'+name,'CMC_functional_nodal',nodal,data)
  direct=normal_action_reduce(a_mul64(weight,a_mul(density,sv)),(0,));whole_rate_pair(keep,label+'_'+name,'CMC_functional_direct',direct,data)
  gap=a_sub(nodal,direct);whole_rate_pair(keep,label+'_'+name,'CMC_functional_gap',gap,data)
  en=P.scalar_scatter(ec,g);bound=np.sum(abs(scalar_test)*en)+np.sum(weight*(abs(sv[0])+abs(sv[1]))*ec)
  data['CMC_functional_operation_envelope']=np.asarray(bound).copy();keep(label+'_'+name+'_CMC_functional_operation_envelope',data['CMC_functional_operation_envelope'])
  check(label+'_'+name+'_CMC_polynomial_transpose_functional',np.asarray(gap[0]+gap[1]).copy(),np.asarray(0.).copy(),np.asarray(bound).copy())
  for n,x in dict(normal_point_operation_envelope=envelope,CMC_point_operation_envelope=ec,normal_weak_operation_envelope=N.scatter_normal_envelope(envelope,g),CMC_weak_operation_envelope=en).items():data[n]=np.asarray(x).copy();keep(label+'_'+name+'_'+n,data[n])
  result[name]=dict(data={n:np.asarray(x).copy() for n,x in data.items()},source_qualification=metadata['source_qualification'],gap_refs=metadata['gap_refs'],column_references=[q[name]['reference'] for q in columns],whole_grid_functional_controls_passed=True,canonical_target_response_qualified=False,finite_rate_change_qualified=False,physical_adoption=False,physical_ports=None)
 return result

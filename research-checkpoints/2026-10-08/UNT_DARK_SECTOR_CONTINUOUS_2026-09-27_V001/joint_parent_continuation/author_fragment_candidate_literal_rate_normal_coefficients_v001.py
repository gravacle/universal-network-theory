"""HELD literal Rv/Tv coefficient construction and original-coordinate apply.
Globals np,P,N,fy_*,lg_six,mp_* are definitions-only selected sources.
Inputs are CLOSED same-candidate147 caches,142 literal primitive adjoints and
the VALUE words of all16 completed247 tests. No old action/test/EOS/producer
body is called. New arithmetic prepares16 physical99+6 covectors by primitive
adjoints, not105 basis actions and not registered286 Cstar or Schwarz.
Operation bounds enclose this represented-coefficient polynomial, conditional
on resolved divisions and finite arithmetic. They do not bound every rounding
association of original87. That action remains authority; later comparisons to
two saved original directions are sampled controls, not a uniform proof.
Future containing ownership/seal/proof binding and per-port/chunk publication
are mandatory. No normal/canonical/adjoint/inverse/physical acceptance follows.
"""
RATE_COEFFICIENT_AUTHOR_DRAFT=True
RATE_COEFFICIENT_AUTHORING_IN_PROGRESS=False
RATE_COEFFICIENT_SOURCE=(None,None)
RATE_COEFFICIENT_RESULT=(None,None,None)
RATE_COEFFICIENT_RECEIPT=(None,None,None)
RATE_COEFFICIENT_PROOF=(None,None,None)
RATE_COEFFICIENT_PARENT_PINS={
 'tests':{'source':(None,None),'result':(None,None,None),'receipt':(None,None,None),'proof':(None,None,None)},
 'literal':{'source':(None,None),'result':(None,None,None),'receipt':(None,None,None),'proof':(None,None,None)},
 'temporal':{'source':(None,None),'result':(None,None,None),'receipt':(None,None,None),'proof':(None,None,None)}}

def rnc_pair(label,x,keep,shape=None):
 assert isinstance(x,tuple) and len(x)==2 and x[0].shape==x[1].shape
 keep(label+'_both_words',np.stack(x).copy())
 for word,a in zip(('hi','lo'),x):
  keep(label+'_'+word,a.copy());assert a.dtype==np.float64 and np.all(np.isfinite(a))
  if shape is not None:assert a.shape==shape
 return x

def rnc_box(label,x,keep,envelope=None):
 rnc_pair(label,x,keep)
 mag=mp_add(abs(x[0]),abs(x[1]),keep,label+'_word_magnitude')
 e=mag if envelope is None else np.asarray(envelope,dtype=np.float64)
 keep(label+'_uncancelled_operation_envelope',e.copy())
 assert e.shape==x[0].shape and np.all(np.isfinite(e)) and np.all(e>=mag)
 return x,e

def rnc_view(x,key):return tuple(a[key] for a in x[0]),x[1][key]

def rnc_transpose(x):return tuple(a.swapaxes(-1,-2) for a in x[0]),x[1].swapaxes(-1,-2)

def rnc_expand(x,axis):return tuple(np.expand_dims(a,axis) for a in x[0]),np.expand_dims(x[1],axis)

def rnc_algebra(keep,label):
 # Unique operation labels retain operands/result/envelope before another call.
 count=[0]
 def op(kind,a,b=None):
  tag=label+'_operation%d_'%count[0]+kind;count[0]+=1
  rnc_pair(tag+'_left',a[0],keep);keep(tag+'_left_envelope',a[1].copy())
  if b is not None:rnc_pair(tag+'_right',b[0],keep);keep(tag+'_right_envelope',b[1].copy())
  if kind in ('add','sub'):
   x=(P.a_add if kind=='add' else P.a_sub)(a[0],b[0]);rnc_pair(tag+'_completed_result',x,keep);e=mp_add(a[1],b[1],keep,tag)
  elif kind=='mul':
   x=P.a_mul(a[0],b[0]);rnc_pair(tag+'_completed_result',x,keep);e=mp_mul(a[1],b[1],keep,tag)
  elif kind=='mm':
   x=fy_mm(a[0],b[0]);rnc_pair(tag+'_completed_result',x,keep);e=mp_mm(a[1],b[1],keep,tag)
  elif kind=='mv':
   x=fy_mv(a[0],b[0]);rnc_pair(tag+'_completed_result',x,keep);e=mp_mv(a[1],b[1],keep,tag)
  elif kind=='div':
   lower=np.nextafter(abs(b[0][0])-abs(b[0][1]),-np.inf);keep(tag+'_resolved_denominator_lower',lower.copy());assert np.all(lower>0)
   x=fy_div(a[0],b[0],keep,tag);rnc_pair(tag+'_completed_result',x,keep);e=mp_div(a[1],lower,keep,tag)
  else:raise AssertionError(kind)
  return rnc_box(tag,x,keep,e)
 def total(a,axis):
  tag=label+'_operation%d_sum'%count[0];count[0]+=1;rnc_pair(tag+'_operand',a[0],keep)
  x=fy_sum(a[0],axis);rnc_pair(tag+'_completed_result',x,keep);return rnc_box(tag,x,keep,mp_sum(a[1],axis,keep,tag))
 def stack(values,axis):
  tag=label+'_operation%d_stack'%count[0];count[0]+=1
  return rnc_box(tag,P.a_stack([a[0] for a in values],axis),keep,np.stack([a[1] for a in values],axis))
 def seed(name,x):return rnc_box(label+'_copied_'+name,x,keep)
 def raw(name,x):return seed(name,P.a_dd(np.asarray(x,dtype=np.float64)))
 def scale(a,s):return op('mul',raw('scalar_multiplier_%d'%count[0],s),a)
 return dict(op=op,total=total,stack=stack,seed=seed,raw=raw,scale=scale,count=count,label=label,keep=keep)

def rnc_outer(A,x,y):return A['op']('mul',rnc_expand(x,-1),rnc_expand(y,-2))

def rnc_gamma_time_reverse(A,X,bGa):
 rows=[];op,total,stack=A['op'],A['total'],A['stack']
 for b in range(4):
  columns=[]
  for k in range(4):
   sym=op('add',rnc_view(bGa,(slice(None),slice(None),0,b)),rnc_view(bGa,(slice(None),slice(None),b,0)))
   terms=op('sub',op('mul',rnc_view(X,(slice(None),slice(None),k)),sym),op('mul',rnc_view(X,(slice(None),slice(None),0)),rnc_view(bGa,(slice(None),slice(None),b,k))))
   columns.append(A['scale'](total(terms,-1),.5))
  rows.append(stack(columns,-1))
 return stack(rows,-2)

def rnc_DG_pullback(A,bDG,beta,b=None):
 op=A['op'];cross=op('add',rnc_view(bDG,(slice(None),0,slice(1,None))),rnc_view(bDG,(slice(None),slice(1,None),0)))
 if b is None:
  diagonal=op('mul',rnc_expand(rnc_expand(rnc_view(bDG,(slice(None),0,0)),-1),-1),rnc_outer(A,beta,beta))
  return op('add',op('add',rnc_view(bDG,(slice(None),slice(1,None),slice(1,None))),rnc_outer(A,cross,beta)),diagonal)
 diagonal=op('mul',rnc_expand(rnc_expand(rnc_view(bDG,(slice(None),0,0)),-1),-1),rnc_outer(A,beta,b))
 return op('add',rnc_outer(A,cross,b),A['scale'](diagonal,2.))

def rnc_Gamma_adjoint(A,bnu,bnz,U,z):
 rows=[]
 for l in range(4):
  row=rnc_outer(A,rnc_view(bnu,(slice(None),slice(None),l)),U)
  for j in range(32):row=A['op']('sub',row,A['op']('mul',rnc_expand(rnc_expand(rnc_view(z,(j,slice(None),l)),-1),-1),rnc_view(bnz,j)))
  rows.append(row)
 return A['stack'](rows,1)

def rnc_chart_reverse(A,cache,gwt,ggt,gzt):
 op,raw,total=A['op'],A['raw'],A['total'];c=cache['c'];I=raw('chart_I',c['ih']);IT=rnc_transpose(I);u=raw('chart_u',c['u']);up=raw('raw_chart_up',c['up'])
 gnum=op('div',ggt,raw('twice_gamma',2*c['gamma']))
 gwt=op('add',gwt,op('mul',u,rnc_expand(gnum,-1)))
 gu=op('add',op('mul',up,rnc_expand(gnum,-1)),op('mv',IT,gwt))
 gQ=A['scale'](op('mm',op('mm',IT,rnc_outer(A,gwt,u)),IT),-1.)
 native=A['stack']([rnc_view(gu,(slice(None),i)) for i in range(3)]+[rnc_view(gzt,(j,slice(None),i)) for j in range(32) for i in range(3)],-1)
 return native,gQ

def rnc_primitive_rate_reverse(A,cache,bnu,bnz):
 op,raw,seed,total=A['op'],A['raw'],A['seed'],A['total'];s,c=cache['s'],cache['c']
 U,z,beta,N,gamma=(raw(n,x) for n,x in (('U',s['U']),('z',s['z']),('beta',c['beta']),('N',c['N']),('gamma',c['gamma'])))
 bGa=rnc_Gamma_adjoint(A,bnu,bnz,U,z);bDG=rnc_gamma_time_reverse(A,raw('spacetime_hi',s['hi']),bGa)
 bu=rnc_view(bnu,(slice(None),0,slice(None)));bz=rnc_view(bnz,(slice(None),slice(None),0,slice(None)));gz0=rnc_view(bz,(slice(None),slice(None),0))
 gwt=rnc_view(bu,(slice(None),slice(1,None)))
 ggt=op('div',op('sub',rnc_view(bu,(slice(None),0)),total(op('mul',beta,gwt),-1)),N)
 second=op('div',op('mul',seed('anchored_NA',cache['NA']),gz0),rnc_expand(seed('rounded_gamma_squared',cache['gamma_squared']),0))
 ggt=op('add',ggt,total(second,0));gAt=A['scale'](op('div',op('mul',rnc_expand(N,0),gz0),rnc_expand(gamma,0)),-1.)
 gwt=op('add',gwt,total(op('mul',raw('zi',s['z'][:,:,1:]),rnc_expand(gAt,-1)),0))
 gzt=op('add',op('add',rnc_view(bz,(slice(None),slice(None),slice(1,None))),op('mul',rnc_expand(beta,0),rnc_expand(gz0,-1))),op('mul',rnc_expand(raw('up',c['up']),0),rnc_expand(gAt,-1)))
 native,Q=rnc_chart_reverse(A,cache,gwt,ggt,gzt)
 return native,op('add',Q,rnc_DG_pullback(A,bDG,beta))

def rnc_test_rate_reverse(A,cache,test,bnu,bnz):
 op,raw,seed,total=A['op'],A['raw'],A['seed'],A['total'];s,c=cache['s'],cache['c'];p=cache['p']
 U,z,beta,N,gamma=(raw(n,x) for n,x in (('U',s['U']),('z',s['z']),('beta',c['beta']),('N',c['N']),('gamma',c['gamma'])))
 eta,zeta,It=(seed(n,test[n]) for n in ('eta','zeta','It'));f,b=raw('test_f',test['f']),raw('test_b',test['b'])
 gGt=rnc_Gamma_adjoint(A,bnu,bnz,U,z);gGa=rnc_Gamma_adjoint(A,bnu,bnz,eta,zeta)
 d1=rnc_gamma_time_reverse(A,It,gGt);d2=rnc_gamma_time_reverse(A,raw('hi',s['hi']),gGa);d3=rnc_gamma_time_reverse(A,raw('hi_qtest',s['hi']),gGt)
 Q=op('add',op('add',rnc_DG_pullback(A,d1,beta),rnc_DG_pullback(A,d2,beta)),rnc_DG_pullback(A,d3,beta,b))
 fN=op('div',f,N);bUt=rnc_view(bnu,(slice(None),0,slice(None)))
 u0=A['scale'](op('mul',fN,rnc_view(bUt,(slice(None),0))),-1.)
 u0=op('add',u0,total(op('mul',rnc_view(bUt,(slice(None),slice(1,None))),op('sub',op('mul',beta,rnc_expand(fN,-1)),b)),-1))
 gz=rnc_view(bnz,(slice(None),slice(None),0,0));gAt=A['scale'](op('div',op('mul',rnc_expand(f,0),gz),rnc_expand(gamma,0)),-1.)
 #247 test-first uses paired gamma*gamma;147 JR uses its anchored raw gamma².
 test_g2=op('mul',gamma,gamma);rnc_pair(A['label']+'_paired_test_gamma_squared_minus_anchored147',P.a_sub(test_g2[0],cache['gamma_squared']),A['keep'])
 ggt=op('add',op('div',u0,N),total(op('div',op('mul',op('mul',rnc_expand(f,0),seed('anchored_A',cache['A'])),gz),rnc_expand(test_g2,0)),0))
 gwt=total(op('mul',raw('zi',s['z'][:,:,1:]),rnc_expand(gAt,-1)),0)
 gzt=op('add',op('mul',rnc_expand(b,0),rnc_expand(gz,-1)),op('mul',rnc_expand(raw('up',c['up']),0),rnc_expand(gAt,-1)))
 native,Qchart=rnc_chart_reverse(A,cache,gwt,ggt,gzt)
 return native,op('add',Q,Qchart)

def rnc_test_primitive_adjoint(A,cache,features,test,literal):
 op,raw,seed=A['op'],A['raw'],A['seed'];s=cache['s'];H=raw('hi',s['hi']);HT=rnc_transpose(H);G=raw('g',s['g']);Proj=raw('P',s['P']);PT=rnc_transpose(Proj);U=raw('U',s['U'])
 It,q,eta,zeta,Pt,Ft,Vt,Dt=(seed(n,test[n]) for n in ('It','q','eta','zeta','Pt','Ft','Vt','Dt'));ItT=rnc_transpose(It);Ft0,V0,D0=(seed(n,features[n]) for n in ('F','V','D'))
 Fut=op('add',op('add',op('mm',op('mm',It,Ft0),H),op('mm',op('mm',H,Ft),H)),op('mm',op('mm',H,Ft0),It))
 bFt=A['scale'](op('add',op('add',op('add',op('mm',op('mm',ItT,Ft0),HT),op('mm',op('mm',HT,Ft),HT)),op('mm',op('mm',HT,Ft0),ItT)),Fut),-P.ALPHA/4)
 bF=seed('literal_bF',literal['F']);Max=op('add',op('mm',op('sub',bFt,rnc_transpose(bFt)),rnc_transpose(G)),op('mm',op('sub',bF,rnc_transpose(bF)),rnc_transpose(q)))
 Z=seed('literal_paired_Z',literal['Z']);Zt=A['total'](op('mul',raw('mode_weights',s['w'][:,None,None]),zeta),0)
 bnu=op('add',Max,op('add',rnc_outer(A,eta,Z),rnc_outer(A,U,Zt)))
 Vut=op('add',op('mv',It,V0),op('mv',H,Vt));bVt=op('add',op('add',op('mv',ItT,V0),op('mv',HT,Vt)),Vut)
 bVt=op('mul',raw('mode_weights_V',s['w'][:,None,None]),op('div',bVt,raw('rounded_twice_frequency_squared',2*(s['omega']**2)[:,None,None])))
 bV=seed('literal_bV',literal['V']);left=op('add',op('mv',rnc_transpose(Pt),bV),op('mv',PT,bVt))
 bnzV=op('add',rnc_outer(A,rnc_expand(eta,0),op('mv',PT,bV)),rnc_outer(A,rnc_expand(U,0),left))
 Dut=op('add',op('add',op('mm',op('mm',It,D0),H),op('mm',op('mm',H,Dt),H)),op('mm',op('mm',H,D0),It))
 bDt=op('add',op('add',op('add',op('mm',op('mm',ItT,D0),HT),op('mm',op('mm',HT,Dt),HT)),op('mm',op('mm',HT,D0),ItT)),Dut)
 bDt=op('mul',raw('mode_weights_D',s['w'][:,None,None,None]),A['scale'](bDt,-P.ELL**2/2));bD=seed('literal_bD',literal['D'])
 bnzD=op('add',op('add',op('mm',op('mm',rnc_transpose(Pt),bD),Proj),op('mm',op('mm',PT,bDt),Proj)),op('mm',op('mm',PT,bD),Pt))
 return bnu,op('add',bnzV,bnzD)

def rnc_EH_coefficients(A,cache,momenta,test):
 op,raw,seed=A['op'],A['raw'],A['seed'];s,c=cache['s'],cache['c'];p=cache['p'];I=raw('EH_I',c['ih']);IT=rnc_transpose(I);K=seed('current_K',momenta['K']);tau=seed('current_Ktrace',momenta['Ktrace']);Kt=seed('current_Ktest',test['Kt'])
 taut=A['total'](A['total'](op('mul',I,Kt),-1),-1)
 def gradient(Q,t):return op('sub',op('add',op('mm',op('mm',I,Q),I),op('mm',op('mm',IT,Q),IT)),A['scale'](op('mul',rnc_expand(rnc_expand(t,-1),-1),I),2.))
 AK,AT=gradient(K,tau),gradient(Kt,taut);N,dens,mu,f=(raw(n,x) for n,x in (('N',c['N']),('dens',c['dens']),('mu',c['sqrt_h']),('f',test['f'])))
 expand=lambda x:rnc_expand(rnc_expand(x,-1),-1)
 direct=op('add',op('add',op('mul',expand(op('mul',op('mul',N,mu),f)),AK),op('mul',expand(op('mul',N,dens)),AT)),op('mul',expand(op('mul',dens,f)),AK))
 tested=op('mul',expand(op('mul',N,dens)),AK)
 denominator=raw('EH_twice_C',np.full((p,1,1),2*P.C));direct=op('div',direct,denominator);tested=op('div',tested,denominator)
 def gamma(x):
  pair=P.a_dd(np.zeros((p,4,4,4)));e=np.zeros((p,4,4,4))
  for w in (0,1):pair[w][:,0,1:,1:]=x[0][w]
  e[:,0,1:,1:]=x[1];tag=A['label']+'_EH_Gamma_covector_%d'%A['count'][0];A['count'][0]+=1
  return rnc_box(tag,pair,keep=A['keep'],envelope=e)
 bg,bgt=gamma(direct),gamma(tested);beta=raw('EH_beta',c['beta']);hi=raw('EH_hi',s['hi']);It=seed('EH_test_It',test['It']);b=raw('EH_test_b',test['b'])
 out=op('add',rnc_DG_pullback(A,rnc_gamma_time_reverse(A,hi,bg),beta),op('add',rnc_DG_pullback(A,rnc_gamma_time_reverse(A,It,bgt),beta),rnc_DG_pullback(A,rnc_gamma_time_reverse(A,hi,bgt),beta,b)))
 return A['scale'](out,-1.)

def prepare_candidate_literal_rate_normal_point_coefficients(candidate,cache,literal,tests,closed,keep,label,port_complete):
 assert not RATE_COEFFICIENT_AUTHOR_DRAFT and not RATE_COEFFICIENT_AUTHORING_IN_PROGRESS
 assert callable(port_complete)
 for group,pins in RATE_COEFFICIENT_PARENT_PINS.items():
  parent=closed[group];assert parent['all_selected_seals_verified'] is True and parent['naturally_closed'] is True and parent['natural_exit_code']==0
  for name,pin in pins.items():assert all(x is not None for x in pin) and tuple(parent[name])==pin
 p=cache['p'];assert 0<p<=128 and len(tests)==16 and cache['configuration_held'] is True and candidate['candidate_provenance']==cache['candidate_provenance']==closed['same_candidate_provenance']
 assert literal['same_candidate_provenance']==closed['same_candidate_provenance'] and literal['closed_literal_ref'] and literal['primitive_adjoints_are_literal142'] is True
 for family in ('s','c'):
  for n,a in cache[family].items():keep(label+'_same_candidate_'+family+'_'+n,a.copy());assert np.array_equal(a,candidate[family][n])
 assert all(cache['constants'][n]==getattr(P,n) for n in ('ALPHA','ELL','C')) and np.all(cache['c']['N']>0) and np.all(cache['c']['gamma']>0) and np.all(cache['s']['omega']>0) and np.all(cache['s']['w']>=0)
 assert literal['source_association_contacts'] and cache['source_primary_contacts'],'Retain original formal/left, raised/feature, primary and quotient bridges'
 for name,shape in (('F',(p,4,4)),('V',(32,p,4)),('D',(32,p,4,4)),('nu',(p,4,4)),('nz',(32,p,4,4)),('Z',(p,4))):rnc_pair(label+'_copied_literal_'+name,literal[name],keep,shape)
 native=P.a_dd(np.zeros((p,4,4,99)));metric=P.a_dd(np.zeros((p,4,4,6)));en=np.zeros((p,4,4,99));em=np.zeros((p,4,4,6));refs=[]
 for serial,test in enumerate(tests):
  row,jet=divmod(serial,4);tag=label+'_row%d_jet%d'%(row,jet);assert test['row']==row and test['jet']==jet and test['value_only'] is True and test['source_ref'] and test['same_candidate_provenance']==closed['same_candidate_provenance']
  f=np.zeros(p);b=np.zeros((p,3))
  if jet==0:
   if row==0:f[:]=1.
   else:b[:,row-1]=1.
  assert test['f'].dtype==test['b'].dtype==np.float64 and np.array_equal(test['f'],f) and np.array_equal(test['b'],b),'Original value,R,Z,t registration'
  assert tuple(test['jet_order'])==('value','R','Z','t')
  for name,shape in (('q',(p,4,4)),('It',(p,4,4)),('eta',(p,4)),('zeta',(32,p,4)),('Pt',(p,4,4)),('Ft',(p,4,4)),('Vt',(32,p,4)),('Dt',(32,p,4,4)),('Kt',(p,3,3)),('lm',(p,))):rnc_pair(tag+'_copied_closed_test_'+name,test[name],keep,shape)
  A=rnc_algebra(keep,tag);A['keep']=keep;op,seed=A['op'],A['seed']
  dt_nu,dt_nz=rnc_test_primitive_adjoint(A,cache,candidate['features']['paired'],test,literal)
  lm=seed('copied_source_measure_test',test['lm']);bn, bz=seed('literal_nu',literal['nu']),seed('literal_nz',literal['nz'])
  dt_nu=op('add',dt_nu,op('mul',rnc_expand(rnc_expand(lm,-1),-1),bn));dt_nz=op('add',dt_nz,op('mul',rnc_expand(rnc_expand(rnc_expand(lm,0),-1),-1),bz))
  nJ,mJ=rnc_primitive_rate_reverse(A,cache,dt_nu,dt_nz);nK,mK=rnc_test_rate_reverse(A,cache,test,bn,bz)
  dens=A['raw']('dens',cache['c']['dens']);n=A['scale'](op('mul',rnc_expand(dens,-1),op('add',nJ,nK)),-1.)
  m=A['scale'](op('mul',rnc_expand(rnc_expand(dens,-1),-1),op('add',mJ,mK)),-1.);m=op('add',m,rnc_EH_coefficients(A,cache,candidate['momenta'],test))
  six=rnc_box(tag+'_physical_metric_six',lg_six(m[0]),keep,np.stack([m[1][:,i,j] if i==j else mp_add(m[1][:,i,j],m[1][:,j,i],keep,tag+'_cross%d%d'%(i,j)) for i,j in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))],-1))
  for w in (0,1):native[w][:,row,jet]=n[0][w];metric[w][:,row,jet]=six[0][w]
  en[:,row,jet]=n[1];em[:,row,jet]=six[1];rnc_pair(tag+'_completed_native_coefficient',n[0],keep,(p,99));rnc_pair(tag+'_completed_metric_coefficient',six[0],keep,(p,6))
  ref=port_complete(row,jet,dict(native=n[0],metric=six[0],e_native=n[1],e_metric=six[1],same_candidate_provenance=closed['same_candidate_provenance'],test_ref=test['source_ref'],literal_ref=literal['closed_literal_ref'],represented_coefficient_only=True));assert isinstance(ref,dict) and all(ref.get(k) for k in ('file','sha256','commit_file','commit_sha256'));refs.append(ref)
 A=rnc_algebra(keep,label+'_CMC');op=A['op'];c,s=cache['c'],cache['s'];kappa=A['scale'](op('mul',A['raw']('N',c['N']),A['raw']('raw_hi00',s['hi'][:,0,0])),-.5)
 tensor=op('mul',rnc_expand(rnc_expand(op('mul',A['raw']('mu',c['sqrt_h']),kappa),-1),-1),A['raw']('I',c['ih']))
 theta=rnc_box(label+'_CMC_physical_six',lg_six(tensor[0]),keep,np.stack([tensor[1][:,i,j] if i==j else mp_add(tensor[1][:,i,j],tensor[1][:,j,i],keep,label+'_CMC_cross%d%d'%(i,j)) for i,j in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))],-1))
 for name,pair in (('normal_native',native),('normal_metric',metric)):rnc_pair(label+'_completed_'+name,pair,keep)
 for name,x in (('e_native',en),('e_metric',em),('e_CMC_metric',theta[1])):keep(label+'_completed_'+name,x.copy())
 return dict(normal_native=native,normal_metric=metric,CMC_metric=theta[0],e_native=en,e_metric=em,e_CMC_metric=theta[1],port_refs=refs,same_candidate_provenance=closed['same_candidate_provenance'],source_association_contacts=literal['source_association_contacts'],source_primary_contacts=cache['source_primary_contacts'],normal_jet_order=('value','R','Z','t'),direct_phase_ordinary_sheet_rate_zero=True,coefficient_scope='literal247 derivative; formal147 chart; represented paired coefficient construction',registered_Cstar_substituted=False,uniform_original87_association_bound_earned=False,original87_whole_direction_authority_required=True,physical_adoption=False)

def candidate_literal_rate_normal_point_apply(block,native,metric,keep,label):
 assert not RATE_COEFFICIENT_AUTHOR_DRAFT and not RATE_COEFFICIENT_AUTHORING_IN_PROGRESS and block['physical_adoption'] is False
 p=metric[0].shape[0];rnc_pair(label+'_native_input',native,keep,(p,99));rnc_pair(label+'_metric_input',metric,keep,(p,6))
 for name,shape in (('normal_native',(p,4,4,99)),('normal_metric',(p,4,4,6)),('CMC_metric',(p,6))):rnc_pair(label+'_saved_'+name,block[name],keep,shape)
 for name,pair,shape in (('e_native',block['normal_native'],(p,4,4,99)),('e_metric',block['normal_metric'],(p,4,4,6)),('e_CMC_metric',block['CMC_metric'],(p,6))):
  e=np.asarray(block[name]);keep(label+'_saved_'+name,e.copy());assert e.shape==shape and e.dtype==np.float64 and np.all(np.isfinite(e)) and np.all(e>=mp_add(abs(pair[0]),abs(pair[1]),keep,label+'_saved_coefficient_magnitude_'+name))
 n=P.a_mul(block['normal_native'],tuple(a[:,None,None] for a in native));rnc_pair(label+'_all_native_products',n,keep)
 m=P.a_mul(block['normal_metric'],tuple(a[:,None,None] for a in metric));rnc_pair(label+'_all_metric_products',m,keep)
 nr=fy_sum(n,-1);rnc_pair(label+'_completed_native_contraction',nr,keep);mr=fy_sum(m,-1);rnc_pair(label+'_completed_metric_contraction',mr,keep)
 normal=rnc_pair(label+'_four_normal_coefficients',P.a_add(nr,mr),keep,(p,4,4));terms=P.a_mul(block['CMC_metric'],metric);rnc_pair(label+'_all_CMC_products',terms,keep)
 theta=rnc_pair(label+'_CMC_density',fy_sum(terms,-1),keep,(p,))
 mag=lambda x:mp_add(abs(x[0]),abs(x[1]),keep,label+'_supplied_word_magnitudes')
 e=mp_add(mp_sum(mp_mul(block['e_native'],mag(native)[:,None,None],keep,label+'_native_bound'),-1,keep,label+'_native_bound'),mp_sum(mp_mul(block['e_metric'],mag(metric)[:,None,None],keep,label+'_metric_bound'),-1,keep,label+'_metric_bound'),keep,label+'_normal_bound')
 t=mp_sum(mp_mul(block['e_CMC_metric'],mag(metric),keep,label+'_CMC_bound'),-1,keep,label+'_CMC_bound')
 return dict(normal_coefficients=normal,initial_CMC_density=theta,normal_operation_envelope=e,CMC_operation_envelope=t,time_primary_action_coefficients=rnc_pair(label+'_weighted_time_primary_action',P.a_mul64(-1.,P.a_slice(normal,(slice(None),slice(None),3))),keep),represented_coefficient_enclosure_only=True,original87_whole_direction_authority_required=True,physical_adoption=False)

def prepare_candidate_literal_rate_normal_apply(chunks,basis,closed,keep,label):
 assert not RATE_COEFFICIENT_AUTHOR_DRAFT and not RATE_COEFFICIENT_AUTHORING_IN_PROGRESS
 for name,pin in (('source',RATE_COEFFICIENT_SOURCE),('result',RATE_COEFFICIENT_RESULT),('receipt',RATE_COEFFICIENT_RECEIPT),('proof',RATE_COEFFICIENT_PROOF)):
  assert all(x is not None for x in pin) and tuple(closed[name])==pin
 assert closed['naturally_closed'] is True and closed['natural_exit_code']==0 and closed['all_selected_seals_verified'] is True and closed['physical_adoption'] is False
 assert len(chunks)==120 and len(closed['same_candidate_provenance'])==4 and basis['closed_provenance']
 for n,shape in (('R',(4,3784)),('dv',(4,3784)),('hats',(4,4,3,86,44))):
  keep(label+'_original_basis_'+n,basis[n].copy());assert basis[n].shape==shape and basis[n].dtype==np.float64 and np.all(np.isfinite(basis[n]))
 assert np.all(basis['R']>0) and np.all(basis['dv']>0)
 for serial,d in enumerate(chunks):
  iq,lo=serial//30,(serial%30)*128;hi=min(lo+128,3784)
  assert (d['column'],d['lo'],d['hi'])==(iq,lo,hi) and d['point_coefficients_ref'] and d['same_candidate_provenance']==closed['same_candidate_provenance'][iq] and d['basis_provenance']==basis['closed_provenance']
 return dict(chunks=list(chunks),basis={n:basis[n].copy() for n in ('R','dv','hats')},closed=closed,physical_adoption=False)

def rnc_positive_normal_CMC_scatter(normal,theta,basis,keep,label):
 assert normal.shape==(15136,4,4) and theta.shape==(15136,) and np.all(normal>=0) and np.all(theta>=0)
 nw=np.zeros((4,87,45));cw=np.zeros((87,45))
 for iq in range(4):
  sl=slice(iq*3784,(iq+1)*3784);weight=abs((basis['dv'][iq]/basis['R'][iq]).reshape(86,44))
  ct=mp_mul(weight,theta[sl].reshape(86,44),keep,label+'_q%d_CMC_weight'%iq)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   tag=label+'_q%d_corner%d'%(iq,corner)
   for row in range(4):
    value=np.zeros((86,44));rt=tag+'_row%d'%row
    for jet,hat in enumerate(N.normal_hat_jet(basis,iq,corner,row)):
     term=mp_mul(abs(hat),normal[sl,row,jet].reshape(86,44),keep,rt+'_jet%d'%jet);keep(rt+'_jet%d_completed_term'%jet,term.copy())
     value=mp_add(value,term,keep,rt+'_jet%d_add'%jet)
    value=mp_mul(weight,value,keep,rt+'_weight');key=(row,slice(di,86+di),slice(dj,44+dj))
    nw[key]=mp_add(nw[key],value,keep,rt+'_scatter');keep(rt+'_completed_partial',nw.copy())
   term=mp_mul(abs(basis['hats'][iq,corner,0]),ct,keep,tag+'_CMC_hat');key=(slice(di,86+di),slice(dj,44+dj));cw[key]=mp_add(cw[key],term,keep,tag+'_CMC_scatter');keep(tag+'_completed_CMC_partial',cw.copy())
 nw[:,1]=mp_add(nw[:,1],nw[:,0],keep,label+'_normal_axis_fold');nw[:,0]=0;nw[:,-1]=0;nw[:,:,-1]=0;nw[2,:,0]=0
 cw[1]=mp_add(cw[1],cw[0],keep,label+'_CMC_axis_fold');cw[0]=0
 keep(label+'_restricted_normal_outward',nw.copy());keep(label+'_restricted_CMC_outward',cw.copy())
 return nw,cw

def candidate_literal_rate_normal_packed_apply(prepared,x,read_closed_chunk,keep,label,chunk_complete,column_complete):
 assert not RATE_COEFFICIENT_AUTHOR_DRAFT and not RATE_COEFFICIENT_AUTHORING_IN_PROGRESS
 assert prepared['physical_adoption'] is False and callable(read_closed_chunk) and callable(chunk_complete) and callable(column_complete)
 chunks,basis=prepared['chunks'],prepared['basis']
 rnc_pair(label+'_original_packed_direction',x,keep,(403340,));fields=[P.unpack_fields(a,False) for a in x];native=tuple(q[0] for q in fields);metric=tuple(q[1] for q in fields)
 for pair,mask in ((native,np.broadcast_to(P.native_mask(),(33,3,87,45))),(metric,P.metric_mask())):assert all(np.all(w[~mask]==0) for w in pair)
 nv=rnc_pair(label+'_NEW_original_native_E',P.dd_native_node_value(native,basis,keep,jet=0),keep,(33,15136,3));mv=rnc_pair(label+'_NEW_original_metric_E',P.dd_metric_node_value(metric,basis,keep,jet=0),keep,(15136,6))
 # Positive original124 E uses all input words independently; never factor bounds.
 nm=mp_add(abs(native[0]),abs(native[1]),keep,label+'_native_input_bound');mm=mp_add(abs(metric[0]),abs(metric[1]),keep,label+'_metric_input_bound');ev,em=candidate_mechanical_positive_lift(nm,mm,basis,keep,label+'_original124_E_bound')
 coeff=P.a_dd(np.zeros((15136,4,4)));theta=P.a_dd(np.zeros(15136));en=np.zeros((15136,4,4));et=np.zeros(15136);refs=[];columns=[]
 for serial,d in enumerate(chunks):
  iq,lo=serial//30,(serial%30)*128;hi=min(lo+128,3784);assert (d['column'],d['lo'],d['hi'])==(iq,lo,hi) and d['same_candidate_provenance']==prepared['closed']['same_candidate_provenance'][iq]
  sl=slice(iq*3784+lo,iq*3784+hi);block=read_closed_chunk(d);assert block['record']==d['point_coefficients_ref'] and block['same_candidate_provenance']==d['same_candidate_provenance'] and block['physical_adoption'] is False
  nr=tuple(a[:,sl].transpose(1,0,2).reshape(hi-lo,99) for a in nv);mr=P.a_slice(mv,sl);part=candidate_literal_rate_normal_point_apply(block,nr,mr,keep,label+'_q%d_chunk%d'%(iq,lo))
  for w in (0,1):coeff[w][sl]=part['normal_coefficients'][w];theta[w][sl]=part['initial_CMC_density'][w]
  un=ev[:,sl].transpose(1,0,2).reshape(hi-lo,99);um=em[sl]
  tag=label+'_q%d_chunk%d_outward'%(iq,lo)
  en[sl]=mp_add(mp_sum(mp_mul(block['e_native'],un[:,None,None],keep,tag+'_native_bound'),-1,keep,tag+'_native_sum'),mp_sum(mp_mul(block['e_metric'],um[:,None,None],keep,tag+'_metric_bound'),-1,keep,tag+'_metric_sum'),keep,tag+'_normal_add');keep(tag+'_completed_normal_bound',en[sl].copy())
  et[sl]=mp_sum(mp_mul(block['e_CMC_metric'],um,keep,tag+'_CMC_bound'),-1,keep,tag+'_CMC_sum');keep(tag+'_completed_CMC_bound',et[sl].copy())
  part['normal_operation_envelope']=en[sl].copy();part['CMC_operation_envelope']=et[sl].copy()
  ref=chunk_complete(d,part);assert isinstance(ref,dict) and all(ref.get(k) for k in ('file','sha256','commit_file','commit_sha256'));refs.append(ref)
  if hi==3784:
   col=slice(iq*3784,(iq+1)*3784);rnc_pair(label+'_column%d_normal'%iq,P.a_slice(coeff,col),keep);rnc_pair(label+'_column%d_CMC'%iq,P.a_slice(theta,col),keep)
   ref=column_complete(iq,dict(normal_coefficients=P.a_slice(coeff,col),initial_CMC_density=P.a_slice(theta,col),normal_operation_envelope=en[col].copy(),CMC_operation_envelope=et[col].copy(),chunk_refs=refs[-30:],same_candidate_provenance=d['same_candidate_provenance'],physical_adoption=False));assert isinstance(ref,dict) and all(ref.get(k) for k in ('file','sha256','commit_file','commit_sha256'));columns.append(ref)
 spatial=P.a_slice(coeff,(slice(None),slice(None),slice(0,3)));rnc_pair(label+'_completed_spatial_normal',spatial,keep)
 weak=rnc_pair(label+'_original_weak_normal',N.paired_scatter_normal(spatial,basis,label+'_original_normal_Tstar'),keep,(4,87,45));CMC=rnc_pair(label+'_original_weak_CMC',P.dd_scalar_scatter(theta,basis,keep,label+'_original_scalar_Tstar'),keep,(87,45))
 primary=rnc_pair(label+'_time_primary_action',P.a_mul64(-1.,P.a_slice(coeff,(slice(None),slice(None),3))),keep,(15136,4))
 keep(label+'_completed_point_uncancelled_normal_envelope',en.copy());keep(label+'_completed_point_uncancelled_CMC_envelope',et.copy())
 ew,ec=rnc_positive_normal_CMC_scatter(en,et,basis,keep,label+'_outward_original_Tstar')
 return dict(weak_normal=weak,weak_initial_CMC=CMC,time_primary_action_coefficients=primary,normal_coefficients=coeff,initial_CMC_density=theta,point_normal_operation_envelope=en,point_CMC_operation_envelope=et,weak_normal_operation_envelope=ew,weak_CMC_operation_envelope=ec,time_primary_operation_envelope=en[:,:,3].copy(),chunk_refs=refs,column_refs=columns,original_weights_and_masks_used_once=True,represented_coefficient_enclosure_only=True,original87_whole_direction_authority_required=True,old_actions_tests_or_registered_Cstar_replayed=False,uniform_source_rounding_or_global_inverse_qualified=False,physical_adoption=False)

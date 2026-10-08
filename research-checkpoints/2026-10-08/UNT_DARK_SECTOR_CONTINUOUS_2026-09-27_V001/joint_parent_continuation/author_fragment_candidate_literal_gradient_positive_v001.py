"""HELD outward bound for NEW142 literal temporal gradient, definitions only.
Globals np,P and the seven reviewed mp_* outward scalar/contraction primitives.
Completed raw/current/cache words are coefficients; no old primal is evaluated.
This bounds the represented coefficient-polynomial reverse chain, not a global
inverse, finite-law error, old-current construction or uniform EFT derivative.
"""
LITERAL_GRADIENT_POSITIVE_AUTHOR_DRAFT=True
LITERAL_GRADIENT_POSITIVE_AUTHORING_IN_PROGRESS=False

def candidate_literal_gradient_positive(candidate,cache,keep,label):
 s,c,F,M=candidate['s'],candidate['c'],candidate['features']['paired'],candidate['momenta'];p=cache['p']
 add=lambda a,b:mp_add(a,b,keep,label)
 mul=lambda a,b:mp_mul(a,b,keep,label)
 div=lambda a,b:mp_div(a,b,keep,label)
 total=lambda a,axis:mp_sum(a,axis,keep,label)
 mm=lambda a,b:mp_mm(a,b,keep,label)
 mv=lambda a,b:mp_mv(a,b,keep,label)
 mag=lambda x:add(abs(x[0]),abs(x[1]))
 transpose=lambda x:x.swapaxes(-1,-2)
 outer=lambda x,y:mul(x[..., :,None],y[...,None,:])
 put=lambda n,a:keep(label+'_'+n,np.asarray(a).copy())
 for family in ('s','c'):
  for n,a in cache[family].items():assert np.array_equal(a,candidate[family][n])
 assert cache['configuration_held'] and all(cache['constants'][n]==getattr(P,n) for n in ('ALPHA','ELL','C'))
 H,G,Proj,I,U,z,beta,up,u=(abs(x) for x in (s['hi'],s['g'],s['P'],c['ih'],s['U'],s['z'],c['beta'],c['up'],c['u']))
 HT,PT,IT=transpose(H),transpose(Proj),transpose(I);N,gamma,dens=c['N'],c['gamma'],abs(c['dens'])
 assert np.all(N>0) and np.all(gamma>0) and np.all(s['omega']>0) and np.all(s['w']>=0) and P.C>0
 # The denominator is the saved source147 rounded-square pair, not a new square.
 den=cache['gamma_squared'];lower=np.nextafter(den[0]-abs(den[1]),-np.inf)
 put('saved_gamma_squared_denominator_both_words',np.stack(den));put('saved_gamma_squared_downward_lower',lower)
 assert np.all(np.isfinite(lower)) and np.all(lower>0)
 omega2=s['omega']**2;put('source_rounded_frequency_squared',omega2);assert np.all(np.isfinite(omega2)) and np.all(omega2>0)
 bF=mul(abs(P.ALPHA)/4,add(mm(mm(HT,mag(F['F'])),HT),mag(F['Fup'])))
 bnu_Max=put('nu_Maxwell',mm(add(bF,transpose(bF)),transpose(G)))
 bV=mul(s['w'][:,None,None],div(add(mv(HT,mag(F['V'])),mag(F['V_raised'])),2*omega2[:,None,None]))
 bnz_V=put('nz_V',outer(U[None],mv(PT,bV)))
 bD=mul(s['w'][:,None,None,None],mul(P.ELL**2/2,add(mm(mm(HT,mag(F['D'])),HT),mag(F['D_raised']))))
 bnz_D=put('nz_D',mm(mm(PT,bD),Proj));bnz=put('nz',add(bnz_V,bnz_D))
 Z=np.zeros((p,4))
 for j in range(32):Z=put('acceleration_Z_partial',add(Z,mul(s['w'][j],z[j])))
 bnu_acc=put('nu_acceleration',outer(U,Z));bnu=put('nu',add(bnu_Max,bnu_acc));rows=[]
 for l in range(4):
  row=outer(bnu[:,:,l],U)
  for j in range(32):row=put('Gamma_row_partial',add(row,mul(z[j,:,l,None,None],bnz[j])))
  rows.append(row);put('Gamma_partial',np.stack(rows,1))
 bGa=put('Gamma',np.stack(rows,1));DG=[]
 for b in range(4):
  cols=[]
  for k in range(4):
   v=np.zeros(p)
   for l in range(4):v=add(v,add(mul(H[:,l,k],add(bGa[:,l,0,b],bGa[:,l,b,0])),mul(H[:,l,0],bGa[:,l,b,k])))
   cols.append(mul(.5,v))
  DG.append(np.stack(cols,-1));put('DG_partial',np.stack(DG,-2))
 bDG=put('DG',np.stack(DG,-2));bUt=bnu[:,0];bZt=bnz[:,:,0];gz0=bZt[:,:,0];gwt=bUt[:,1:]
 ggt=div(add(bUt[:,0],total(mul(beta,gwt),-1)),N)
 ggt=add(ggt,total(div(mul(mag(cache['NA']),gz0),lower[None]),0));gAt=div(mul(N[None],gz0),gamma[None])
 gwt=add(gwt,total(mul(z[:,:,1:],gAt[:,:,None]),0))
 gzt=add(add(bZt[:,:,1:],mul(beta[None],gz0[:,:,None])),mul(up[None],gAt[:,:,None]))
 gnum=div(ggt,2*gamma);gwt=add(gwt,mul(u,gnum[:,None]));gv=add(mul(up,gnum[:,None]),mv(IT,gwt))
 gIt=outer(gwt,u);gQ=mm(mm(IT,gIt),IT)
 cross=add(bDG[:,0,1:],bDG[:,1:,0]);gQDG=add(add(bDG[:,1:,1:],outer(cross,beta)),mul(bDG[:,0,0,None,None],outer(beta,beta)))
 native=put('literal_native',mul(dens[:,None],np.stack([gv[:,i] for i in range(3)]+[gzt[j,:,i] for j in range(32) for i in range(3)],-1)))
 six=lambda a:np.stack([a[:,i,j] if i==j else add(a[:,i,j],a[:,j,i]) for i,j in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))],-1)
 metric_native=put('literal_metric_native',mul(dens[:,None],six(add(gQ,gQDG))))
 K,tau=mag(M['K']),mag(M['Ktrace']);both=add(mm(mm(I,K),I),mm(mm(IT,K),IT));trace=mul(2.,mul(tau[:,None,None],I))
 bK=div(mul(dens[:,None,None],add(both,trace)),2*P.C)
 kappa=div(mul(N,abs(s['hi'][:,0,0])),2.);EH=put('literal_metric_EH',six(mul(kappa[:,None,None],bK)))
 metric=put('literal_metric_total',add(metric_native,EH))
 return dict(native=native,metric_native=metric_native,metric_EH=EH,metric_total=metric,
             scope='outward current coefficient-polynomial NEW142 reverse chain; no source-state error or inverse bound',
             normal_or_stationarity_qualified=False,physical_adoption=False)

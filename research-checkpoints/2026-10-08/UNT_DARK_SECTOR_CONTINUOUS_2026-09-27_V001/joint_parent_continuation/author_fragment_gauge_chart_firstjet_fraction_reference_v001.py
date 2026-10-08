"""HELD independent exact-Fraction gauge chart/firstjet contact oracle.
Globals Fraction only. No P/fs/fy callback, producer, EOS, action or numerical
helper is called. Fractions use original raw coefficients, both paired input
words and explicitly supplied NEW quotient/value locks; no ideal inverse,
normalization or zero-primary-gap identity is substituted. Each scalar result
is (locked coefficient value, NEW derivative, uncancelled derivative envelope).
"""
GAUGE_CHART_REFERENCE_AUTHOR_DRAFT=True
GAUGE_CHART_REFERENCE_AUTHORING_IN_PROGRESS=False

def gauge_chart_firstjet_fraction_reference(column,direction,result,locks,point):
 assert not GAUGE_CHART_REFERENCE_AUTHOR_DRAFT and not GAUGE_CHART_REFERENCE_AUTHORING_IN_PROGRESS
 s,c=column['candidate']['s'],column['candidate']['c'];state=result['mechanical']['state'];zero=Fraction(0)
 exact=lambda x:Fraction.from_float(float(x))
 def scalar(v,d=zero):return v,d,abs(d)
 def const(x):return scalar(exact(x))
 def add(a,b):return a[0]+b[0],a[1]+b[1],a[2]+b[2]
 def neg(a):return -a[0],-a[1],a[2]
 def sub(a,b):return add(a,neg(b))
 def mul(a,b):return a[0]*b[0],a[1]*b[0]+a[0]*b[1],abs(b[0])*a[2]+abs(a[0])*b[2]
 def scale(k,a):return mul(const(k),a)
 def sum_(items):
  out=const(0.)
  for a in items:out=add(out,a)
  return out
 def lock(v,a):return v[0],a[1],a[2]
 def quotient(v,den,num):
  assert den[0]!=0
  return v[0],(num[1]-v[0]*den[1])/den[0],(num[2]+abs(v[0])*den[2])/abs(den[0])
 def tensor(pair,axis=0,delta=None):
  shape=pair[0].shape;assert pair[1].shape==shape
  def descend(dim,key):
   if dim==len(shape):
    v=exact(pair[0][key])+exact(pair[1][key]);d=zero if delta is None else exact(delta[0][key])+exact(delta[1][key]);return scalar(v,d)
   if dim==axis:return descend(dim+1,key+(point,))
   return [descend(dim+1,key+(i,)) for i in range(shape[dim])]
  return descend(0,())
 def raw(a,delta=None):
  def descend(shape,key):
   if not shape:
    d=zero if delta is None else exact(delta[0][key])+exact(delta[1][key]);return scalar(exact(a[key]),d)
   return [descend(shape[1:],key+(i,)) for i in range(shape[0])]
  return descend(a.shape[1:],(point,))
 def dot(a,b):return sum_(mul(x,y) for x,y in zip(a,b))
 def mv(A,x):return [dot(row,x) for row in A]
 def transpose(A):return [list(row) for row in zip(*A)]
 def mm(A,B):return transpose([mv(A,col) for col in transpose(B)])
 def outer(a,b):return [[mul(x,y) for y in b] for x in a]
 def ta(A,B,operation=add):return [[operation(x,y) for x,y in zip(ar,br)] for ar,br in zip(A,B)]
 def ts(k,A):return [[scale(k,x) for x in row] for row in A]
 def locked(name):return tensor(locks[name],axis=1 if name.startswith('z0_') else 0)
 N=raw(c['N'],direction['N']);beta=raw(c['beta'],direction['beta']);h=raw(c['h']);I=raw(c['ih']);up=raw(c['up']);u=raw(c['u']);gamma=raw(c['gamma']);mu=raw(c['sqrt_h'])
 Na=tensor(column['gauge']['N_jets'],delta=direction['N_jets']);ba=tensor(column['gauge']['beta_jets'],delta=direction['beta_jets'])
 ua=tensor(column['covectors']['u_jets']);za=tensor(column['covectors']['z_jets'],axis=1);zi=raw(s['z'].transpose(1,0,2)[:,:,1:])
 ha=[tensor(column['mechanical']['h_dot'])]+tensor(column['geometry']['h_spatial_jets'])+[[[const(0.) for j in range(3)] for i in range(3)]]
 N2=lock(raw(c['N']**2),mul(N,N));gamma2=raw(c['gamma']**2)
 U0=quotient(raw(s['U'][:,0]),N,gamma);Ui=[lock(raw(s['U'][:,1:])[i],sub(up[i],mul(beta[i],U0))) for i in range(3)];U=[U0]+Ui
 A=tensor(state['A'][0],axis=1);z=[]
 for mode in range(32):
  zquot=quotient(locked('z0_quotient')[mode],gamma,mul(N,A[mode]));z0=lock(raw(s['z'].transpose(1,0,2))[mode][0],sub(dot(beta,zi[mode]),zquot));z.append([z0]+zi[mode])
 hb=[lock(a,b) for a,b in zip(locked('h_beta'),mv(h,beta))]
 g00=sub(dot(beta,hb),N2);g=[[g00]+hb]+[[hb[i]]+h[i] for i in range(3)]
 hi00=quotient(raw(s['hi'][:,0,0]),N2,const(-1.));hi0i=[quotient(raw(s['hi'][:,0,1:])[i],N2,beta[i]) for i in range(3)]
 shift=locked('shift_inverse');bb=outer(beta,beta);hij=[[lock(raw(s['hi'][:,1:,1:])[i][j],sub(I[i][j],quotient(shift[i][j],N2,bb[i][j]))) for j in range(3)] for i in range(3)]
 hi=[[hi00]+hi0i]+[[hi0i[i]]+hij[i] for i in range(3)]
 density=lock(raw(c['dens']),mul(N,mu));dg=[];du=[];dz=[[] for _ in range(32)]
 ga=tensor(state['gamma_first'][0]);wa=tensor(state['up_first'][0]);oldDG=tensor(locks['current_dg']);oldDU=tensor(locks['current_du'])
 for a in range(4):
  ga[a]=scalar(ga[a][0]);wa[a]=[scalar(x[0]) for x in wa[a]]
  first=quotient(locked('U0_first_'+str(a)),N,ga[a]);second=quotient(locked('U0_second_'+str(a)),N2,mul(gamma,Na[a]));U0a=sub(first,second)
  # U0a's computed primal is a lock, not an anchored old du[0] assumption.
  U0a=lock(oldDU[a][0],U0a)
  Uia=[sub(sub(wa[a][i],mul(U0,ba[a][i])),mul(beta[i],U0a)) for i in range(3)];du.append([U0a]+Uia)
  for mode in range(32):
   Aa=add(dot(wa[a],zi[mode]),dot(up,za[mode][a]));num=add(mul(Na[a],A[mode]),mul(N,Aa))
   second=quotient(locked('z0_second_'+str(a))[mode],gamma2,mul(mul(N,A[mode]),ga[a]));first=quotient(locked('z0_first_'+str(a))[mode],gamma,num)
   shift=add(dot(ba[a],zi[mode]),dot(beta,za[mode][a]));dz[mode].append([add(shift,sub(second,first))]+za[mode][a])
  hba=[lock(oldDG[a][0][i+1],x) for i,x in enumerate([add(x,y) for x,y in zip(mv(ha[a],beta),mv(h,ba[a]))])]
  g00a=sub(add(dot(ba[a],hb),dot(beta,hba)),scale(2.,mul(N,Na[a])));dg.append([[g00a]+hba]+[[hba[i]]+ha[a][i] for i in range(3)])
 # Derivative-first connection polynomial uses inherited DG/E0, without LC reset.
 DG=tensor(column['candidate']['jets']['dg']);E0=tensor(column['reference']['E0']);Ga=[]
 for l in range(4):
  rows=[]
  for a in range(4):
   cols=[]
   for b in range(4):
    terms=[]
    for m in range(4):
     base=sub(add(sub(DG[a][b][m],E0[a][b][m]),sub(DG[b][a][m],E0[b][a][m])),sub(DG[m][a][b],E0[m][a][b]))
     term=sub(add(dg[a][b][m],dg[b][a][m]),dg[m][a][b]);term=lock(base,term);terms.append(mul(hi[l][m],term))
    cols.append(scale(.5,sum_(terms)))
   rows.append(cols)
  Ga.append(rows)
 # Gamma primal is anchored independently; δNΓ+NδΓ is the full K contact.
 oldGamma=tensor(column['candidate']['jets']['Ga']);K=[[mul(N,lock(oldGamma[0][i+1][j+1],Ga[0][i+1][j+1])) for j in range(3)] for i in range(3)]
 tau=sum_(mul(I[i][j],K[i][j]) for i in range(3) for j in range(3));IK=mm(mm(I,K),I)
 # Keep C as the exact represented coefficient: division, not a fresh reciprocal.
 C=exact(column['constants']['C']);assert C>0
 EH=[[(x[0]/(2*C),x[1]/(2*C),x[2]/(2*C)) for x in row] for row in [[mul(mu,sub(IK[i][j],mul(I[i][j],tau))) for j in range(3)] for i in range(3)]]
 six=[EH[i][j] if i==j else scale(2.,EH[i][j]) for i,j in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))]
 return dict(g=g,hi=hi,U=U,z=z,dg=dg,du=du,dz=dz,Ga=Ga,dens=density,K=K,metric_EH_density=six,
             scope='NEW gauge coordinate polynomial with explicit raw/cached quotient locks; no ideal inverse or primary identity')

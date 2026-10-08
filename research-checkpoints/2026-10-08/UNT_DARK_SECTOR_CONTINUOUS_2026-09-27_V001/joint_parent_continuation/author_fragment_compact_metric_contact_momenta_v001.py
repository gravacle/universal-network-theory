"""Definitions only: paired first configuration derivative of the saved81 map.
Caller supplies np, retained a_* DD algebra, a_div64, normal_keep_pair,
normal_pair_sum, ALPHA/ELL/C/B/GC, and keep(name,array). No calls by authors.
Current configuration s,c is fixed binary64; jets/feature['paired']/moments
are the saved current two-word operands, never old target/L2 substitutes.
d holds pairs g,hi,U,z,du,dz,Ga. dc holds pairs ih,JU,JzU,Jzz,Uh,zh,
embed,dens,sqrt_h,log_dens (plus the caller's disclosed up/gamma contacts).
Mechanical native/metric rates, coordinate N/beta/gauge jets, phi first jets,
weights,omega,xi and action constants are fixed for this partial derivative.
dGa is the supplied covariant contact; its algebraic-contact difference stays
in the caller's separate witness. No normalization/chart gap is reset here.
log_dens is the fractional derivative of the SAME dens; at fixed N it also
is the fractional sqrt_h derivative. This uses stored current momenta for
measure terms and avoids recomputing a primal momentum/EH map.
Outputs preserve all words. This is no caller, force, normal solve or adoption.
"""

def compact_contact_swap(x):
 return np.swapaxes(x[0],-1,-2),np.swapaxes(x[1],-1,-2)
def compact_contact_matvec(A,x):
 assert A[0].shape==A[1].shape and x[0].shape==x[1].shape and A[0].shape[-1]==x[0].shape[-1]
 out=a_dd(np.zeros(np.broadcast_shapes(A[0].shape[:-2],x[0].shape[:-1])+(A[0].shape[-2],)))
 for k in range(A[0].shape[-1]):
  v=a_slice(x,(Ellipsis,k));out=a_add(out,a_mul(a_slice(A,(Ellipsis,slice(None),k)),(v[0][...,None],v[1][...,None])))
 return out
def compact_contact_left(A,x):
 return a_stack([compact_contact_matvec(A,a_slice(x,(Ellipsis,slice(None),k))) for k in range(x[0].shape[-1])],axis=-1)
def compact_contact_right(x,A):
 return a_stack([compact_contact_matvec(compact_contact_swap(A),a_slice(x,(Ellipsis,k,slice(None)))) for k in range(x[0].shape[-2])],axis=-2)
def compact_contact_outer(x,y):
 return a_mul((x[0][..., :,None],x[1][..., :,None]),(y[0][...,None,:],y[1][...,None,:]))
def compact_contact_reduce(x,axes):
 for axis in sorted(((a+x[0].ndim) if a<0 else a for a in axes),reverse=True):x=normal_pair_sum(x,axis)
 return x

def compact_contact_momenta(s,c,jets,feature,moments,d,dc,keep,label):
 # Product rules only; every rate-dependent primal is a saved current pair.
 F=feature['paired'];U,z,g,hi=s['U'],s['z'],s['g'],s['hi'];p=len(U);df={};dm={};dq={}
 def put(store,n,x):store[n]=x;return normal_keep_pair(label+'_'+n,x,keep)
 G,H,Up,zp,P=a_dd(g),a_dd(hi),a_dd(U),a_dd(z),a_dd(s['P'])
 for n in ('g','hi','U','z','du','dz','Ga'):assert d[n][0].shape==d[n][1].shape
 for n in ('ih','JU','JzU','Jzz','Uh','zh','embed','dens','sqrt_h','log_dens'):assert dc[n][0].shape==dc[n][1].shape
 duc=put(dq,'uc',a_add(compact_contact_matvec(d['g'],Up),compact_contact_matvec(G,d['U'])))
 dP=put(dq,'P',a_add(compact_contact_outer(duc,Up),compact_contact_outer(a_dd(s['uc']),d['U'])))
 dZ=a_dd(np.zeros((p,4)))
 for j in range(32):dZ=a_add(dZ,a_mul64(s['w'][j],a_slice(d['z'],j)));normal_keep_pair(label+'_delta_Z_partial',dZ,keep)
 put(dq,'Z',dZ);put(dq,'r',compact_contact_matvec(dP,a_dd(s['phi'])))
 dzu=a_add(compact_contact_matvec(d['hi'],zp),compact_contact_matvec(H,d['z']))
 dz2=a_add(compact_contact_reduce(a_mul(d['z'],compact_contact_matvec(H,zp)),(-1,)),compact_contact_reduce(a_mul(zp,dzu),(-1,)))
 put(dq,'z2',dz2);put(dq,'f',a_div64(dz2,(B*GC)**2*s['xi'][:,None]**4,keep,label+'_delta_f_division'))
 for n in ('du','dz','Ga'):put(df,n,d[n])
 dnu=d['du'];dnz=d['dz']
 for l in range(4):
  ga=a_transpose(a_slice(jets['Ga'],(slice(None),slice(None),slice(None),l)),(0,2,1));dga=a_transpose(a_slice(d['Ga'],(slice(None),slice(None),slice(None),l)),(0,2,1))
  du_l=a_slice(d['U'],(slice(None),l))
  dnu=a_add(dnu,a_add(a_mul64(U[:,l,None,None],dga),a_mul((du_l[0][:,None,None],du_l[1][:,None,None]),ga)))
  zz_l=a_slice(d['z'],(slice(None),slice(None),l))
  dnz=a_sub(dnz,a_add(a_mul64(z[:,:,l,None,None],a_slice(d['Ga'],(slice(None),l,slice(None),slice(None)))),a_mul((zz_l[0][:,:,None,None],zz_l[1][:,:,None,None]),a_slice(jets['Ga'],(slice(None),l,slice(None),slice(None))))))
  normal_keep_pair(label+'_delta_nu_partial',dnu,keep);normal_keep_pair(label+'_delta_nz_partial',dnz,keep)
 put(df,'nu',dnu);put(df,'nz',dnz);dqq=a_dd(np.zeros((32,p,4)));da=a_dd(np.zeros((p,4)))
 for a in range(4):
  ua=a_slice(d['U'],(slice(None),a))
  dqq=a_add(dqq,a_add(a_mul((ua[0][None,:,None],ua[1][None,:,None]),a_slice(F['nz'],(slice(None),slice(None),a,slice(None)))),a_mul64(U[None,:,a,None],a_slice(dnz,(slice(None),slice(None),a,slice(None))))))
  da=a_add(da,a_add(a_mul((ua[0][:,None],ua[1][:,None]),a_slice(F['nu'],(slice(None),a,slice(None)))),a_mul64(U[:,a,None],a_slice(dnu,(slice(None),a,slice(None))))))
  normal_keep_pair(label+'_delta_q_partial',dqq,keep);normal_keep_pair(label+'_delta_a_partial',da,keep)
 put(df,'q',dqq);put(df,'a',da)
 dV=put(df,'V',a_add(compact_contact_matvec(dP,F['q']),compact_contact_matvec(P,dqq)))
 dD=a_add(compact_contact_right(compact_contact_left(dP,F['nz']),compact_contact_swap(P)),compact_contact_right(compact_contact_left(P,dnz),compact_contact_swap(P)))
 dD=put(df,'D',a_add(dD,compact_contact_right(compact_contact_left(P,F['nz']),compact_contact_swap(dP))))
 lower=put(df,'lower_nu',a_add(compact_contact_right(dnu,G),compact_contact_right(F['nu'],d['g'])))
 dF=put(df,'F',a_sub(lower,compact_contact_swap(lower)))
 dFu=a_add(compact_contact_right(compact_contact_left(d['hi'],F['F']),H),compact_contact_right(compact_contact_left(H,dF),H))
 dFu=put(df,'Fup',a_add(dFu,compact_contact_right(compact_contact_left(H,F['F']),d['hi'])))
 dVu=put(df,'V_raised',a_add(compact_contact_matvec(d['hi'],F['V']),compact_contact_matvec(H,dV)))
 dDu=a_add(compact_contact_right(compact_contact_left(d['hi'],F['D']),H),compact_contact_right(compact_contact_left(H,dD),H))
 dDu=put(df,'D_raised',a_add(dDu,compact_contact_right(compact_contact_left(H,F['D']),d['hi'])))
 dPi=a_add(compact_contact_outer((d['U'][0][None],d['U'][1][None]),F['V_raised']),compact_contact_outer(a_dd(U[None]),dVu))
 dPi=a_div64(dPi,s['omega'][:,None,None,None]**2,keep,label+'_delta_Pi_frequency');dPi=put(df,'Pi',a_mul64(s['w'][:,None,None,None],a_sub(dPi,a_mul64(ELL**2,dDu))))
 dPiU=a_add(a_mul64(-ALPHA,a_add(compact_contact_left(d['hi'],F['F']),compact_contact_left(H,dF))),a_add(compact_contact_outer(d['U'],a_dd(s['Z'])),compact_contact_outer(Up,dZ)))
 put(df,'PiU',dPiU)
 sym=a_mul64(.5,a_add(F['Pi'],compact_contact_swap(F['Pi'])));dsym=a_mul64(.5,a_add(dPi,compact_contact_swap(dPi)));dKlo=[]
 UU=compact_contact_outer(Up,Up);dUU=a_add(compact_contact_outer(d['U'],Up),compact_contact_outer(Up,d['U']))
 for l in range(4):
  zl=a_slice(dZ,(slice(None),l));row=a_add(a_mul((zl[0][:,None,None],zl[1][:,None,None]),UU),a_mul64(s['Z'][:,l,None,None],dUU))
  for j in range(32):
   zz=a_slice(d['z'],(j,slice(None),l));row=a_sub(row,a_add(a_mul64(z[j,:,l,None,None],a_slice(dsym,j)),a_mul((zz[0][:,None,None],zz[1][:,None,None]),a_slice(sym,j))));normal_keep_pair(label+'_delta_Klo_partial_l%d'%l,row,keep)
  dKlo.append(row)
 dKlo=put(dm,'connection_Klo',a_stack(dKlo,axis=1));dKup=a_dd(np.zeros((p,4,4,4)))
 for m in range(4):
  hm=a_slice(d['hi'],(slice(None),slice(None),m));km=a_slice(moments['connection_Klo'],(slice(None),m,slice(None),slice(None)))
  dKup=a_add(dKup,a_add(a_mul((hm[0][:,:,None,None],hm[1][:,:,None,None]),(km[0][:,None],km[1][:,None])),a_mul64(hi[:,:,m,None,None],(dKlo[0][:,None,m],dKlo[1][:,None,m]))));normal_keep_pair(label+'_delta_raised_Klo_partial',dKup,keep)
 put(dm,'connection_raised_Klo',dKup);dCCn=put(dm,'connection_D',a_mul64(.5,a_sub(a_add(a_transpose(dKup,(0,2,1,3)),a_transpose(dKup,(0,2,3,1))),dKup)))
 def mx_product(f,u):return a_add(a_mul((f[0][:,:,:,None],f[1][:,:,:,None]),(u[0][:,None,None,:],u[1][:,None,None,:])),a_mul((f[0][:,:,None,:],f[1][:,:,None,:]),(u[0][:,None,:,None],u[1][:,None,:,None])))
 dMX=put(dm,'connection_Maxwell',a_mul64(-ALPHA/2,a_add(mx_product(dFu,Up),mx_product(F['Fup'],d['U']))));dCC=put(dm,'connection_momentum',a_add(dCCn,dMX))
 PU=a_slice(F['PiU'],(slice(None),0,slice(None)));dPU=a_slice(dPiU,(slice(None),0,slice(None)));P00=a_slice(F['Pi'],(slice(None),slice(None),0,0));dP00=a_slice(dPi,(slice(None),slice(None),0,0))
 dpu=a_dd(np.zeros((p,3)))
 for a in range(4):
  pu=a_slice(PU,(slice(None),a));dp=a_slice(dPU,(slice(None),a));dpu=a_add(dpu,a_add(a_mul64(c['JU'][:,a],(dp[0][:,None],dp[1][:,None])),a_mul(a_slice(dc['JU'],(slice(None),a,slice(None))),(pu[0][:,None],pu[1][:,None]))));normal_keep_pair(label+'_delta_pu_chart_partial',dpu,keep)
 for j in range(32):
  pj=a_slice(P00,j);dpj=a_slice(dP00,j);dpu=a_add(dpu,a_add(a_mul64(c['JzU'][j],(dpj[0][:,None],dpj[1][:,None])),a_mul(a_slice(dc['JzU'],j),(pj[0][:,None],pj[1][:,None]))));normal_keep_pair(label+'_delta_pu_mode_partial',dpu,keep)
 dpz=a_add(a_slice(dPi,(slice(None),slice(None),0,slice(1,None))),a_add(a_mul64(c['Jzz'][None],(dP00[0][:,:,None],dP00[1][:,:,None])),a_mul((dc['Jzz'][0][None],dc['Jzz'][1][None]),(P00[0][:,:,None],P00[1][:,:,None]))))
 delta99=a_stack([a_slice(dpu,(slice(None),i)) for i in range(3)]+[a_slice(dpz,(j,slice(None),i)) for j in range(32) for i in range(3)],axis=-1)
 log=dc['log_dens'];put(dm,'native_density',a_add(a_mul64(c['dens'][:,None],delta99),a_mul((log[0][:,None],log[1][:,None]),moments['native_density'])))
 dpm=a_dd(np.zeros((p,6)));C0=a_slice(moments['connection_momentum'],(slice(None),0,slice(None),slice(None)));dC0=a_slice(dCC,(slice(None),0,slice(None),slice(None)))
 for a in range(4):
  pu=a_slice(PU,(slice(None),a));dp=a_slice(dPU,(slice(None),a))
  dpm=a_add(dpm,a_add(a_mul64(c['Uh'][:,:,a],(dp[0][:,None],dp[1][:,None])),a_mul(a_slice(dc['Uh'],(slice(None),slice(None),a)),(pu[0][:,None],pu[1][:,None]))))
  for b in range(4):
   cv=a_slice(C0,(slice(None),a,b));dv=a_slice(dC0,(slice(None),a,b));dpm=a_add(dpm,a_add(a_mul64(c['embed'][:,:,a,b],(dv[0][:,None],dv[1][:,None])),a_mul(a_slice(dc['embed'],(slice(None),slice(None),a,b)),(cv[0][:,None],cv[1][:,None]))))
  normal_keep_pair(label+'_delta_metric_native_partial',dpm,keep)
 for j in range(32):
  pj=a_slice(P00,j);dpj=a_slice(dP00,j);dpm=a_add(dpm,a_add(a_mul64(c['zh'][j],(dpj[0][:,None],dpj[1][:,None])),a_mul(a_slice(dc['zh'],j),(pj[0][:,None],pj[1][:,None]))));normal_keep_pair(label+'_delta_metric_mode_partial',dpm,keep)
 put(dm,'metric_native_density',a_add(a_mul64(c['dens'][:,None],dpm),a_mul((log[0][:,None],log[1][:,None]),moments['metric_native_density'])))
 dK=put(dm,'K',a_mul64(c['N'][:,None,None],a_slice(d['Ga'],(slice(None),0,slice(1,None),slice(1,None)))))
 dtrace=put(dm,'Ktrace',a_add(compact_contact_reduce(a_mul(dc['ih'],moments['K']),(1,2)),compact_contact_reduce(a_mul64(c['ih'],dK),(1,2))))
 I=a_dd(c['ih']);dKu=a_add(compact_contact_right(compact_contact_left(dc['ih'],moments['K']),I),compact_contact_right(compact_contact_left(I,dK),I))
 dKu=a_add(dKu,compact_contact_right(compact_contact_left(I,moments['K']),dc['ih']))
 dpi=a_sub(dKu,a_add(a_mul64(c['ih'],(dtrace[0][:,None,None],dtrace[1][:,None,None])),a_mul((moments['Ktrace'][0][:,None,None],moments['Ktrace'][1][:,None,None]),dc['ih'])))
 dpi=a_div64(a_mul64(c['sqrt_h'][:,None,None],dpi),2*C,keep,label+'_delta_EH_momentum_division');dpi=put(dm,'metric_EH_tensor',a_add(dpi,a_mul((log[0][:,None,None],log[1][:,None,None]),moments['metric_EH_tensor'])))
 deh=put(dm,'metric_EH_density',a_stack([a_mul64(1. if a==b else 2.,a_slice(dpi,(slice(None),a,b))) for a,b in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))],axis=-1))
 put(dm,'metric_total_density',a_add(dm['metric_native_density'],deh))
 dq.update(g=d['g'],hi=d['hi'],U=d['U'],z=d['z'])
 return dict(paired=df,configuration=dq,fixed_rates_gauge_spectrum_and_phase_jets=True),dm

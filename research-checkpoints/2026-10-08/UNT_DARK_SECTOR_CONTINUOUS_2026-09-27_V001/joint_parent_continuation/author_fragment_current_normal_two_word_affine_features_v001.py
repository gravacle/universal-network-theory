"""Definitions only: fixed-configuration paired features and momenta.
The same g/hi/U/z/P/r/uc/Z and covector chart coefficients are frozen inputs.
Complete du/dz/Gamma pairs come from the admitted affine first-jet wrapper.
Every rate-dependent quantity here is affine; no old feature or kinetic replay.
Use both words in every contraction; later stress uses hh+hl+lh+ll products.
Caller supplies np, a_* DD helpers, a_div64, normal_keep_pair, C/ALPHA/ELL,
and keep(name,array). No physical state/source/gauge/history is selected.
"""

def normal_pair_left(A,x):
 # A[p,m,n], x[...,p,n,k]; preserve both words before each contracted sum.
 return a_stack([a_matvec(A,a_slice(x,(Ellipsis,slice(None),i))) for i in range(x[0].shape[-1])],axis=-1)
def normal_pair_right(x,A):
 return a_stack([a_matvec(A.swapaxes(-1,-2),a_slice(x,(Ellipsis,i,slice(None)))) for i in range(x[0].shape[-2])],axis=-2)
def normal_pair_sandwich(A,x,B):return normal_pair_right(normal_pair_left(A,x),B)
def normal_pair_sum(x,axis):
 out=a_dd(np.zeros(x[0].shape[:axis]+x[0].shape[axis+1:]))
 for i in range(x[0].shape[axis]):out=a_add(out,(np.take(x[0],i,axis=axis),np.take(x[1],i,axis=axis)))
 return out

def paired_current_affine_features(s,c,jets,keep,label):
 # Feature names match the existing action; constants keep their admitted bits.
 U,z,g,hi,P=s['U'],s['z'],s['g'],s['hi'],s['P'];p=len(U);out={}
 def put(n,x):out[n]=x;return normal_keep_pair(label+'_'+n,x,keep)
 for n in ('du','dz','Ga'):put(n,jets[n])
 nu=jets['du']
 for l in range(4):
  term=a_mul64(U[:,l,None,None],a_transpose(a_slice(jets['Ga'],(slice(None),slice(None),slice(None),l)),(0,2,1)))
  nu=a_add(nu,term);normal_keep_pair(label+'_nu_partial',nu,keep)
 put('nu',nu);nz=jets['dz']
 for l in range(4):
  term=a_mul64(z[:,:,l,None,None],a_slice(jets['Ga'],(slice(None),l,slice(None),slice(None))))
  nz=a_sub(nz,term);normal_keep_pair(label+'_nz_partial',nz,keep)
 put('nz',nz);q=a_dd(np.zeros((32,p,4)))
 for a in range(4):q=a_add(q,a_mul64(U[None,:,a,None],a_slice(nz,(slice(None),slice(None),a,slice(None)))));normal_keep_pair(label+'_q_partial',q,keep)
 put('q',q);V=put('V',a_matvec(P,q));D=put('D',normal_pair_sandwich(P,nz,P.swapaxes(-1,-2)))
 nuc=put('lower_nu',normal_pair_right(nu,g));F=put('F',a_sub(nuc,a_transpose(nuc,(0,2,1))))
 put('Fup',normal_pair_sandwich(hi,F,hi));acc=a_dd(np.zeros((p,4)))
 for a in range(4):acc=a_add(acc,a_mul64(U[:,a,None],a_slice(nu,(slice(None),a,slice(None)))));normal_keep_pair(label+'_a_partial',acc,keep)
 put('a',acc);Vu=put('V_raised',a_matvec(hi,V));Du=put('D_raised',normal_pair_sandwich(hi,D,hi))
 Pi=a_mul64(U[None,:,:,None],(Vu[0][:,:,None,:],Vu[1][:,:,None,:]))
 Pi=a_div64(Pi,s['omega'][:,None,None,None]**2,keep,label+'_Pi_frequency_division');Pi=a_sub(Pi,a_mul64(ELL**2,Du));put('Pi',a_mul64(s['w'][:,None,None,None],Pi))
 contact=a_prod(U[:,:,None],s['Z'][:,None,:]);put('PiU',a_add(a_mul64(-ALPHA,normal_pair_left(hi,F)),contact))
 # All configuration-only fields remain ordinary arrays, separately disclosed.
 return dict(constants={n:s[n] for n in ('g','hi','U','z','P','uc','Z','r','z2','f','phi','omega','xi','w')},paired=out,configuration_changed=False)

def paired_current_affine_momenta(s,c,feature,jets,keep,label):
 f=feature['paired'];Pi,PiU,Fup=f['Pi'],f['PiU'],f['Fup'];U,z,hi=s['U'],s['z'],s['hi'];p=len(U);out={}
 def put(n,x):out[n]=x;return normal_keep_pair(label+'_'+n,x,keep)
 sym=a_mul64(.5,a_add(Pi,a_transpose(Pi,(0,1,3,2))));K=[]
 for l in range(4):
  row=a_mul64(s['Z'][:,l,None,None],a_prod(U[:,:,None],U[:,None,:]))
  for j in range(32):row=a_sub(row,a_mul64(z[j,:,l,None,None],a_slice(sym,j)));normal_keep_pair(label+'_Klo_partial_l%d'%l,row,keep)
  K.append(row)
 Klo=put('connection_Klo',a_stack(K,axis=1));Kup=a_dd(np.zeros((p,4,4,4)))
 for m in range(4):Kup=a_add(Kup,a_mul64(hi[:,:,m,None,None],(Klo[0][:,None,m],Klo[1][:,None,m])));normal_keep_pair(label+'_raised_Klo_partial',Kup,keep)
 put('connection_raised_Klo',Kup)
 native=put('connection_D',a_mul64(.5,a_sub(a_add(a_transpose(Kup,(0,2,1,3)),a_transpose(Kup,(0,2,3,1))),Kup)))
 mx=a_add(a_mul64(U[:,None,None,:],(Fup[0][:,:,:,None],Fup[1][:,:,:,None])),a_mul64(U[:,None,:,None],(Fup[0][:,:,None,:],Fup[1][:,:,None,:])))
 mx=put('connection_Maxwell',a_mul64(-ALPHA/2,mx));CC=put('connection_momentum',a_add(native,mx))
 PU=a_slice(PiU,(slice(None),0,slice(None)));P00=a_slice(Pi,(slice(None),slice(None),0,0))
 pu=a_dd(np.zeros((p,3)))
 for a in range(4):pu=a_add(pu,a_mul64(c['JU'][:,a],(PU[0][:,a,None],PU[1][:,a,None])));normal_keep_pair(label+'_pu_chart_partial',pu,keep)
 for j in range(32):pu=a_add(pu,a_mul64(c['JzU'][j],(P00[0][j,:,None],P00[1][j,:,None])));normal_keep_pair(label+'_pu_mode_partial',pu,keep)
 pz=a_add(a_slice(Pi,(slice(None),slice(None),0,slice(1,None))),a_mul64(c['Jzz'][None],(P00[0][:,:,None],P00[1][:,:,None])))
 native_p=a_mul64(c['dens'][:,None],a_stack([a_slice(pu,(slice(None),i)) for i in range(3)]+[a_slice(pz,(j,slice(None),i)) for j in range(32) for i in range(3)],axis=-1));put('native_density',native_p)
 pm=a_dd(np.zeros((p,6)));C0=a_slice(CC,(slice(None),0,slice(None),slice(None)))
 for a in range(4):
  pm=a_add(pm,a_mul64(c['Uh'][:,:,a],(PU[0][:,a,None],PU[1][:,a,None])))
  for b in range(4):pm=a_add(pm,a_mul64(c['embed'][:,:,a,b],(C0[0][:,a,b,None],C0[1][:,a,b,None])))
  normal_keep_pair(label+'_metric_native_partial',pm,keep)
 for j in range(32):pm=a_add(pm,a_mul64(c['zh'][j],(P00[0][j,:,None],P00[1][j,:,None])));normal_keep_pair(label+'_metric_mode_partial',pm,keep)
 put('metric_native_density',a_mul64(c['dens'][:,None],pm))
 Kpair=put('K',a_mul64(c['N'][:,None,None],a_slice(jets['Ga'],(slice(None),0,slice(1,None),slice(1,None)))))
 Ktrace=a_dd(np.zeros(p))
 for a in range(3):
  for b in range(3):Ktrace=a_add(Ktrace,a_mul64(c['ih'][:,a,b],a_slice(Kpair,(slice(None),a,b))))
 put('Ktrace',Ktrace);Ku=normal_pair_sandwich(c['ih'],Kpair,c['ih'])
 pi=a_sub(Ku,a_mul64(c['ih'],(Ktrace[0][:,None,None],Ktrace[1][:,None,None])));pi=a_mul64(c['sqrt_h'][:,None,None],pi);pi=put('metric_EH_tensor',a_div64(pi,2*C,keep,label+'_EH_momentum_division'))
 eh=a_stack([a_mul64(1. if a==b else 2.,a_slice(pi,(slice(None),a,b))) for a,b in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))],axis=-1)
 put('metric_EH_density',eh);put('metric_total_density',a_add(out['metric_native_density'],eh));return out

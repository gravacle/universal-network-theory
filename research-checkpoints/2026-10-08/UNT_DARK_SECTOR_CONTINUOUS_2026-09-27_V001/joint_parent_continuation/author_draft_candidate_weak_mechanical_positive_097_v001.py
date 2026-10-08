"""HELD unsigned full147/E/F construction envelope, not a factor bound.
Globals np,P and sw_keep. All fixed coefficients are the same copied CLOSED147
raw values or cached paired NA/denominator. No physics/action is evaluated.
Each unsigned scalar product/add uses an outward128eps allowance and nextafter;
an active subnormal rounded to zero gets its directed rounding upper, not a
reference floor. Overflow or unresolved denominators refuse. Original1e-10
rows and2e-11 construction controls remain unchanged.
"""
MECHANICAL_POSITIVE_AUTHOR_DRAFT=True
MECHANICAL_POSITIVE_AUTHORING_IN_PROGRESS=True

def mp_out(value,active,keep,label):
 value=np.asarray(value,dtype=np.float64);active=np.broadcast_to(active,value.shape)
 keep(label+'_current_positive_raw',value.copy());assert np.all(np.isfinite(value)) and np.all(value>=0)
 out=np.where(active,np.nextafter(value*(1+128*np.finfo(np.float64).eps),np.inf),0.)
 keep(label+'_current_positive_outward',out.copy());assert np.all(np.isfinite(out)) and np.all(out>=0)
 return out

def mp_add(a,b,keep,label):return mp_out(a+b,(np.asarray(a)>0)|(np.asarray(b)>0),keep,label)

def mp_mul(a,b,keep,label):return mp_out(a*b,(np.asarray(a)>0)&(np.asarray(b)>0),keep,label)

def mp_div(a,b,keep,label):
 keep(label+'_positive_denominator',np.asarray(b).copy());assert np.all(np.isfinite(b)) and np.all(np.asarray(b)>0)
 return mp_out(a/b,np.asarray(a)>0,keep,label)

def mp_sum(a,axis,keep,label):
 axis%=a.ndim;out=np.zeros(a.shape[:axis]+a.shape[axis+1:])
 for column in range(a.shape[axis]):out=mp_add(out,np.take(a,column,axis=axis),keep,label)
 keep(label+'_completed_positive_sum',out.copy());return out

def mp_mm(a,b,keep,label):
 terms=mp_mul(a[..., :, :,None],b[...,None,:,:],keep,label)
 return mp_sum(terms,-2,keep,label)

def mp_mv(a,b,keep,label):return mp_sum(mp_mul(a,b[...,None,:],keep,label),-1,keep,label)

def candidate_mechanical_positive_point(cache,physical,keep,label):
 s,c,p=cache['s'],cache['c'],cache['p'];put=lambda n,a:keep(label+'_'+n,np.asarray(a).copy())
 add=lambda a,b:mp_add(a,b,keep,label);mul=lambda a,b:mp_mul(a,b,keep,label);div=lambda a,b:mp_div(a,b,keep,label)
 total=lambda a,axis:mp_sum(a,axis,keep,label);mm=lambda a,b:mp_mm(a,b,keep,label);mv=lambda a,b:mp_mv(a,b,keep,label)
 mag=lambda x:add(abs(x[0]),abs(x[1]))
 v=mag(physical['native']).reshape(p,33,3);ut=v[:,0];zt=v[:,1:].transpose(1,0,2);six=mag(physical['metric'])
 Q=np.zeros((p,3,3))
 for slot,(i,j) in enumerate(((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))):Q[:,i,j]=Q[:,j,i]=six[:,slot]
 I,u,up,beta=map(abs,(c['ih'],c['u'],c['up'],c['beta']));hi,U,z,proj,g=map(abs,(s['hi'],s['U'],s['z'],s['P'],s['g']))
 assert cache['configuration_held'] and np.all(c['N']>0) and np.all(c['gamma']>0) and np.all(s['omega']>0) and np.all(s['w']>=0)
 It=put('formal_inverse_time',mm(mm(I,Q),I));wt=put('formal_up_time',add(mv(It,u),mv(I,ut)))
 gt=put('gamma_time',div(add(total(mul(ut,up),-1),total(mul(u,wt),-1)),2*c['gamma']));U0t=div(gt,c['N'])
 Ut=put('formal_U_time',np.column_stack((U0t,add(wt,mul(beta,U0t[:,None])))))
 At=add(total(mul(wt[None],z[:,:,1:]),-1),total(mul(up[None],zt),-1));gamma=cache['gamma_squared'];lower=gamma[0]-abs(gamma[1]);put('literal_gamma_squared_lower',lower)
 first=div(mul(c['N'][None],At),c['gamma'][None]);second=div(mul(mag(cache['NA']),gt[None]),lower[None]);z0t=add(total(mul(beta[None],zt),-1),add(second,first))
 Zt=put('formal_z_time',np.concatenate((z0t[:,:,None],zt),2));DG=np.zeros((p,4,4,4));qb=mv(Q,beta)
 DG[:,0,1:,1:]=Q;DG[:,0,0,1:]=DG[:,0,1:,0]=qb;DG[:,0,0,0]=total(mul(beta,qb),-1);put('metric_time_jets',DG)
 Ga=np.zeros((p,4,4,4))
 for a in range(4):
  for b in range(4):Ga[:,:,a,b]=mul(.5,mv(hi,add(add(DG[:,a,b],DG[:,b,a]),DG[:,:,a,b])))
 put('connection_direction',Ga);nu=np.zeros((p,4,4));nz=np.zeros((32,p,4,4));nu[:,0]=Ut;nz[:,:,0]=Zt
 for l in range(4):
  nu=add(nu,mul(U[:,l,None,None],Ga[:,:,:,l].transpose(0,2,1)));nz=add(nz,mul(z[:,:,l,None,None],Ga[:,l][None]))
 put('nu',nu);put('nz',nz);q=np.zeros((32,p,4))
 for a in range(4):q=add(q,mul(U[None,:,a,None],nz[:,:,a]))
 V=mv(proj[None],q);DD=mm(mm(proj[None],nz),proj.swapaxes(-1,-2)[None]);lowerU=mm(nu,g)
 F=add(lowerU,lowerU.swapaxes(-1,-2));Fu=mm(mm(hi,F),hi);Vu=mv(hi[None],V);Du=mm(mm(hi[None],DD),hi[None])
 frequency=s['omega']**2;put('literal_frequency_squared_denominator',frequency)
 Pi=put('Pi',mul(s['w'][:,None,None,None],add(div(mul(U[None,:,:,None],Vu[:,:,None,:]),frequency[:,None,None,None]),mul(P.ELL**2,Du))))
 PiU=put('PiU',mul(abs(P.ALPHA),mm(hi,F)));sym=mul(.5,add(Pi,Pi.swapaxes(-1,-2)));Klo=np.zeros((p,4,4,4))
 for l in range(4):
  for mode in range(32):Klo[:,l]=add(Klo[:,l],mul(z[mode,:,l,None,None],sym[mode]))
 put('connection_Klo',Klo);Kup=np.zeros((p,4,4,4))
 for m in range(4):Kup=add(Kup,mul(hi[:,:,m,None,None],Klo[:,None,m]))
 CCn=mul(.5,add(add(Kup.transpose(0,2,1,3),Kup.transpose(0,2,3,1)),Kup));MX=add(mul(U[:,None,None,:],Fu[:,:,:,None]),mul(U[:,None,:,None],Fu[:,:,None,:]));CC=put('connection_momentum',add(CCn,mul(abs(P.ALPHA)/2,MX)))
 PU=PiU[:,0];P00=Pi[:,:,0,0];pu=np.zeros((p,3));pm=np.zeros((p,6))
 for a in range(4):pu=add(pu,mul(abs(c['JU'][:,a]),PU[:,a,None]))
 for mode in range(32):pu=add(pu,mul(abs(c['JzU'][mode]),P00[mode,:,None]))
 pz=add(Pi[:,:,0,1:],mul(abs(c['Jzz'])[None],P00[:,:,None]));native=put('native',mul(abs(c['dens'])[:,None],np.concatenate((pu,pz.transpose(1,0,2).reshape(p,96)),-1)))
 for a in range(4):
  pm=add(pm,mul(abs(c['Uh'][:,:,a]),PU[:,a,None]))
  for b in range(4):pm=add(pm,mul(abs(c['embed'][:,:,a,b]),CC[:,0,a,b,None]))
 for mode in range(32):pm=add(pm,mul(abs(c['zh'][mode]),P00[mode,:,None]))
 metric_native=put('metric_native',mul(abs(c['dens'])[:,None],pm));K=mul(c['N'][:,None,None],Ga[:,0,1:,1:]);trace=total(total(mul(I,K),-1),-1)
 EH=div(mul(c['sqrt_h'][:,None,None],add(mm(mm(I,K),I),mul(I,trace[:,None,None]))),2*P.C)
 metric_EH=put('metric_EH',np.stack([mul(1. if i==j else 2.,EH[:,i,j]) for i,j in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))],-1))
 return dict(native=native,metric_native=metric_native,metric_EH=metric_EH,metric_total=put('metric_total',add(metric_native,metric_EH)))

def candidate_weak_mechanical_positive(blocks,basis,x,keep,label):
 parts=[P.unpack_fields(a,False) for a in x];native=tuple(q[0] for q in parts);metric=tuple(q[1] for q in parts)
 for n in ('R','dv','hats'):assert np.array_equal(basis[n],blocks['basis'][n])
 nmag=mp_add(abs(native[0]),abs(native[1]),keep,label);mmag=mp_add(abs(metric[0]),abs(metric[1]),keep,label)
 n=sw_keep(label+'_unsigned_original_native_lift',P.dd_native_node_value(P.a_dd(nmag),basis,keep,jet=0),keep);m=sw_keep(label+'_unsigned_original_metric_lift',P.dd_metric_node_value(P.a_dd(mmag),basis,keep,jet=0),keep)
 n=mp_add(abs(n[0]),abs(n[1]),keep,label);m=mp_add(abs(m[0]),abs(m[1]),keep,label);npieces=[];mpieces=[]
 for iq,cache in enumerate(blocks['columns']):
  sl=slice(iq*3784,(iq+1)*3784);physical=dict(native=P.a_dd(n[:,sl].transpose(1,0,2).reshape(3784,99)),metric=P.a_dd(m[sl]))
  out=candidate_mechanical_positive_point(cache,physical,keep,label+'_column%d'%iq);npieces.append(out['native']);mpieces.append(out['metric_total'])
 nv=np.concatenate(npieces).reshape(15136,33,3).transpose(1,0,2);mv=np.concatenate(mpieces)
 nweak=sw_keep(label+'_unsigned_original_native_scatter',P.dd_native_scatter(P.a_dd(nv),basis,keep),keep);mweak=sw_keep(label+'_unsigned_original_metric_scatter',P.dd_metric_scatter(P.a_dd(mv),basis,keep),keep)
 out=P.pack_fields(mp_add(abs(nweak[0]),abs(nweak[1]),keep,label),mp_add(abs(mweak[0]),abs(mweak[1]),keep,label));keep(label+'_full_authoritative_positive_operation_envelope',out.copy());return out

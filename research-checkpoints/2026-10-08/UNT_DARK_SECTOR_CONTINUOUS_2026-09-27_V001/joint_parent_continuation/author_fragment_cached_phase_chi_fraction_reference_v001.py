"""HELD independent rational contact oracle and unsigned operation envelopes.
The four-point oracle uses exact Fractions of the original paired cache words.
No logarithm, square root, EOS value, normal value or producer is evaluated.
The full-section envelope mode carries only unsigned values and derivative bounds.
Globals np, math, Fraction; no candidate/helper arithmetic callbacks are used.
"""
CHI_FRACTION_REFERENCE_AUTHOR_DRAFT=True
CHI_FRACTION_REFERENCE_AUTHORING_IN_PROGRESS=False

def chi_reference_tensor(pair,point,bounds):
 def scalar(key):
  h,l=pair[0][key],pair[1][key]
  if not bounds:
   v=Fraction.from_float(float(h))+Fraction.from_float(float(l));return (v,Fraction(0),Fraction(0),abs(v))
  upper=np.nextafter(abs(h)+abs(l),np.inf);lower=np.maximum(0.,np.nextafter(h-abs(l),-np.inf))
  return (upper,None,np.zeros_like(upper),lower)
 def descend(shape,key):
  if not shape:return scalar(key)
  return [descend(shape[1:],key+(i,)) for i in range(shape[0])]
 return descend(pair[0].shape[1:],(slice(None) if bounds else point,))

def chi_cached_contact_reference(prepared,direction,normal_cache,f,b,point=None,bounds=False,keep=None,label=None):
 assert not CHI_FRACTION_REFERENCE_AUTHOR_DRAFT and not CHI_FRACTION_REFERENCE_AUTHORING_IN_PROGRESS
 assert bounds is (point is None) and len(normal_cache)==4
 up=lambda x:np.nextafter(x,np.inf) if bounds else x
 plus=lambda a,b:up(a+b);times=lambda a,b:up(a*b);divide=lambda a,b:up(a/b)
 def const(x):
  v=float(x) if bounds else Fraction.from_float(float(x));return (abs(v) if bounds else v,None if bounds else Fraction(0),0. if bounds else Fraction(0),abs(v))
 zero=const(0.);one=const(1.);completed_bounds=[0]
 def add(a,b):return (plus(a[0],b[0]),None if bounds else a[1]+b[1],plus(a[2],b[2]),0.)
 def neg(a):return a if bounds else (-a[0],-a[1],a[2],a[3])
 def sub(a,b):return add(a,neg(b))
 def mul(a,b):return (times(a[0],b[0]),None if bounds else a[1]*b[0]+a[0]*b[1],plus(times(abs(a[0]),b[2]),times(a[2],abs(b[0]))),0.)
 def scale(x,a):return mul(const(x),a)
 def total(items):
  out=zero
  for item in items:out=add(out,item)
  return out
 def lock(cache,expr):
  if isinstance(cache,list):return [lock(a,b) for a,b in zip(cache,expr)]
  if bounds and keep is not None:
   completed_bounds[0]+=1;keep(label+'_completed_unsigned_stage_%04d'%completed_bounds[0],np.stack(np.broadcast_arrays(cache[0],expr[2],cache[3])).copy())
  return (cache[0],expr[1],expr[2],cache[3])
 def quotient(cache,den,num):
  lower=den[3] if bounds else abs(den[0]);assert np.all(lower>0) if bounds else lower>0
  return (cache[0],None if bounds else (num[1]-cache[0]*den[1])/den[0],divide(plus(num[2],times(abs(cache[0]),den[2])),lower),cache[3])
 def dot(a,b):return total([mul(x,y) for x,y in zip(a,b)])
 def mv(A,x):return [dot(row,x) for row in A]
 def transpose(A):return [list(row) for row in zip(*A)]
 def mm(A,B):return transpose([mv(A,col) for col in transpose(B)])
 def outer(a,b):return [[mul(x,y) for y in b] for x in a]
 def tensor_add(a,b):
  if isinstance(a,list):return [tensor_add(x,y) for x,y in zip(a,b)]
  return add(a,b)
 def tensor_neg(a):return [tensor_neg(x) for x in a] if isinstance(a,list) else neg(a)
 def tensor_direction(pair,delta):
  value=chi_reference_tensor(pair,point,bounds);d=chi_reference_tensor(delta,point,bounds)
  def merge(a,b):
   if isinstance(a,list):return [merge(x,y) for x,y in zip(a,b)]
   return (a[0],None if bounds else b[0],b[0] if bounds else abs(b[0]),a[3])
  return merge(value,d)
 v={n:chi_reference_tensor(pair,point,bounds) for n,pair in prepared['values'].items()}
 s={n:tensor_direction(pair,direction[n]) for n,pair in prepared['s'].items()};c={n:tensor_direction(pair,direction[n]) for n,pair in prepared['c'].items()}
 raised=lock(v['raised'],mv(s['hi'],s['phi']));X2=lock(v['X2'],neg(dot(s['phi'],raised)))
 twoX=(2*v['X'][0],v['X'][1],2*v['X'][2],2*v['X'][3]);X=quotient(v['X'],twoX,X2)
 q=quotient(v['q'],v['X0'],X);u=lock(v['u'],sub(mul(q,q),one));d=lock(v['d'],sub(const(prepared['constants']['eps']),u))
 distance=quotient(v['s'],d,u);ones=lock(v['one_plus_s'],add(one,distance))
 logarithm=lock(v['logarithm'],quotient(zero,v['one_plus_s'],distance));fraction=quotient(v['fraction'],ones,distance)
 pressureq=quotient(v['pressure_quotient'],v['norm'],sub(logarithm,fraction));A0=prepared['constants']['A0']
 pressure=lock(v['pressure'],scale(A0,pressureq));PXdim=quotient(v['PX_dimensionless'],v['epnorm'],mul(q,distance))
 PX=quotient(v['PX'],v['X0'],scale(2*A0,PXdim));first=quotient(v['PXX_first'],v['epnorm'],scale(2.,distance))
 second_den=lock(v['PXX_second_denominator'],mul(v['norm'],mul(d,d)))
 second=quotient(v['PXX_second'],second_den,scale(4.,mul(q,q)));PXX=quotient(v['PXX'],v['X0_squared'],scale(A0,add(first,second)))
 clock=[quotient(old,X,new) for old,new in zip(v['clock'],raised)]
 pressureJ=[neg(mul(PX,x)) for x in clock];r=lock(v['r'],mv(s['P'],s['phi']));hir=lock(v['hi_r'],mv(s['hi'],r))
 relative=mv(transpose(s['P']),hir);J=lock(v['J'],[sub(x,y) for x,y in zip(pressureJ,relative)])
 registeredJ=lock(v['registered_J'],[sub(x,y) for x,y in zip(pressureJ,hir)]);density=lock(v['density'],mul(c['N'],c['mu']))
 p=lock(v['p'],mul(density,J[0]));registeredp=lock(v['registered_p'],mul(density,registeredJ[0]))
 n02=lock(v['n02'],mul(clock[0],clock[0]));PXoverX=quotient(v['PX_over_X'],X,PX)
 pressureH=lock(v['pressureH'],sub(mul(PXX,n02),mul(PXoverX,add(s['hi'][0][0],n02))))
 p0=[row[0] for row in s['P']];hp0=lock(v['hp0'],mv(s['hi'],p0));A00=lock(v['A00'],dot(p0,hp0))
 H=lock(v['H'],mul(density,sub(pressureH,A00)));registeredH=lock(v['registered_H'],mul(density,sub(pressureH,hp0[0])))
 nativeb=lock(v['b'],dot(c['u'],mv(c['ih'],c['u'])));reducedH=quotient(v['reduced_H'],c['N'],mul(c['mu'],sub(PXX,nativeb)))
 eos=dict(X2=X2,X=X,q=q,u=u,s=distance,pressure=pressure,PX=PX,PXX=PXX,J=J,registered_J=registeredJ,p=p,registered_p=registeredp,H=H,registered_H=registeredH,reduced_H=reducedH,density=density,current_gap=[sub(x,y) for x,y in zip(J,registeredJ)],density_gap=sub(p,registeredp),hessian_gap=sub(H,registeredH),reduced_gap=sub(H,reducedH))
 chain={}
 for n,actual,slope in (('P',pressure,v['PX']),('PX',PX,v['PXX']),('PXX',PXX,v['PXXX'])):
  expected=(0.,None if bounds else slope[0]*X[1],times(abs(slope[0]),X[2]),0.)
  chain[n]=dict(actual=actual,expected=expected,gap=sub(actual,expected))
 normals=[]
 for row,raw in enumerate(normal_cache):
  a={n:chi_reference_tensor(pair,point,bounds) for n,pair in raw.items()};fr=const(float(f[row]));br=[const(float(x)) for x in b[row]]
  hb=mv(c['h'],br);qtest=[[zero for j in range(4)] for i in range(4)];qtest[0][0]=add(scale(-2.,mul(c['N'],fr)),scale(2.,dot(c['beta'],hb)))
  for i in range(3):qtest[0][i+1]=qtest[i+1][0]=hb[i]
  qtest=lock(a['q'],qtest);It=lock(a['It'],tensor_neg(mm(mm(s['hi'],qtest),s['hi'])))
  eta0=neg(quotient(neg(a['eta'][0]),c['N'],mul(s['U'][0],fr)))
  eta=lock(a['eta'],[eta0]+[sub(neg(mul(s['U'][0],br[i])),mul(c['beta'][i],eta0)) for i in range(3)])
  uct=lock(a['uct'],tensor_add(mv(qtest,s['U']),mv(s['g'],eta)))
  Pt=lock(a['Pt'],tensor_add(outer(uct,s['U']),outer(s['uc'],eta)))
  rt=lock(a['rt'],mv(Pt,s['phi']));rrow=lock(a['r'],r);r2=lock(a['r2'],dot(rrow,hir))
  Xtest=quotient(a['Xtest'],X,scale(-.5,dot(s['phi'],mv(It,s['phi']))));lm=quotient(a['lm'],c['N'],fr)
  abs_terms=lock(a['absolute_terms'],[mul(PX,Xtest),mul(pressure,lm)])
  rel_terms=lock(a['relative_terms'],[scale(-.5,dot(rrow,mv(It,rrow))),neg(dot(rrow,mv(s['hi'],rt))),scale(-.5,mul(r2,lm))])
  absolute=lock(a['absolute'],mul(lock(a['density'],density),total(abs_terms)));relative_a=lock(a['relative'],mul(lock(a['density'],density),total(rel_terms)))
  action=lock(a['action'],add(absolute,relative_a));normals.append(dict(absolute=absolute,relative=relative_a,action=action,hamiltonian=neg(action)))
 return dict(eos=eos,chain=chain,normals=normals,scope='cached rational direction stages; no ideal quotient or chain equality assumed')

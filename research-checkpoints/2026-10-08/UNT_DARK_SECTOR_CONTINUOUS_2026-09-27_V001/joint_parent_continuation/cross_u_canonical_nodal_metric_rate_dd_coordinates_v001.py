"""Guarded two-word nodal coordinates for the unchanged frozen canonical system."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal,localcontext
import argparse,hashlib,json,math,os,sys,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_CANONICAL_NODAL_METRIC_RATE_DD_COORDINATES_V001'
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='1f3c5afbb26dd9f43fcea053f92bfad073fdeb75221265d6212772125445e23e'
BAND='CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001'
MAX_CYCLES=3;CAP=160;LINEAR_TOL=1e-10;TOL=2e-11
np=None;OWNER=None;INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];RAW={};AVAILABLE={};CONTEXT={};DD_ARRAY_CURRENT={}
FLAGS=dict(canonical_rate_physical=False,CMC_preservation_qualified=False,full_constraints_qualified=False,physical_metric_qualified=False,source_history_qualified=False,exterior_qualified=False,galaxy_velocity_qualified=False)
def now():return datetime.now(timezone.utc).isoformat()

def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p

def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()

def canonical(v):
 if isinstance(v,dict):return {str(k):canonical(x) for k,x in v.items()}
 if isinstance(v,(list,tuple)):return [canonical(x) for x in v]
 if np is not None and isinstance(v,np.generic):return canonical(v.item())
 if v is None or type(v) in (str,bool,int):return v
 if type(v) is float and math.isfinite(v):return v
 raise TypeError('Unsupported/nonfinite metadata '+type(v).__name__)

def encode(v):return (json.dumps(canonical(v),sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()

def publish(n,raw):
 p=path(n)
 with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);assert p.read_bytes()==raw;OUTPUTS[n]=sha(p);return OUTPUTS[n]

def json_file(n,v):return publish(n,encode(v))

def check(label,actual,expected,envelope):
 a=np.asarray(actual);b=np.asarray(expected);e=np.asarray(envelope);k=len(CHECKS)
 CONTEXT.update(control=label,ordinal=k)
 for n,v in (('actual',a),('expected',b),('envelope',e)):RAW[f'control_{k:03d}_{label}_{n}']=v.copy()
 assert a.shape==b.shape==e.shape and np.all(np.isfinite(a)) and np.all(np.isfinite(b)) and np.all(np.isfinite(e)) and np.all(e>=0)
 error=float(np.max(abs(a-b)/np.maximum(e,1e-30),initial=0));row=dict(ordinal=k,name=label,error=error,tolerance=TOL,passed=error<=TOL);CHECKS.append(row)
 assert row['passed'],(label,error)

def checkpoint(tag,arrays,meta,failed=False):
 schema={}
 for k,a in arrays.items():
  assert isinstance(a,np.ndarray) and a.dtype.kind in 'fiub'
  finite=bool(np.all(np.isfinite(a)));assert failed or finite,k
  schema[k]=dict(shape=list(a.shape),dtype=str(a.dtype),finite=finite)
 md=json.loads(encode(dict(meta,owner=OWNER,qualification=FLAGS,schema=schema,failed=failed)).decode())
 text=encode(md).decode();name=f'{STEM}_{len(RECORDS):05d}_{tag}.npz';p=path(name)
 with p.open('xb') as f:np.savez_compressed(f,metadata_json=np.array(text),**arrays);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);OUTPUTS[name]=sha(p);rec=dict(file=name,sha256=OUTPUTS[name],metadata=md);cf=name+'.COMMIT.json';ch=json_file(cf,rec)
 rec=dict(rec,commit_file=cf,commit_sha256=ch);RECORDS.append(rec)
 with np.load(p,allow_pickle=False) as f:
  assert str(f['metadata_json'])==text and set(f.files)==set(arrays)|{'metadata_json'}
  for k,a in arrays.items():assert f[k].shape==a.shape and f[k].dtype==a.dtype and np.array_equal(f[k],a,equal_nan=True),k
 return rec

def recheck(strict=True):
 for n,h in INPUTS.items():assert sha(path(n))==h,('input changed',n)
 assert sha(__file__)==OWNER['source_sha256']
 for n,h in OUTPUTS.items():assert sha(path(n))==h,('output changed',n)
 for r in RECORDS:
  assert json.loads(path(r['commit_file']).read_text())=={k:v for k,v in r.items() if k not in ('commit_file','commit_sha256')}
  with np.load(path(r['file']),allow_pickle=False) as f:
   assert json.loads(str(f['metadata_json']))==r['metadata'] and set(f.files)==set(r['metadata']['schema'])|{'metadata_json'}
   for n,s in r['metadata']['schema'].items():assert list(f[n].shape)==s['shape'] and str(f[n].dtype)==s['dtype'] and bool(np.all(np.isfinite(f[n])))==s['finite']
 if strict:
  assert path(STEM+'_OWNER_START.json').read_bytes()==encode(OWNER)
  assert {p.name for p in BASE.glob(STEM+'_*.npz')}=={r['file'] for r in RECORDS}
  assert {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={r['commit_file'] for r in RECORDS}

def seal_actual():
 for p in sorted(BASE.glob(STEM+'_*')):
  if p.is_file():p.chmod(0o444);OUTPUTS[p.name]=sha(p)

def read_pair(rec,names):
 assert sha(path(rec['file']))==rec['sha256'] and sha(path(rec['commit_file']))==rec['commit_sha256']
 assert json.loads(path(rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
 out={};metadata_key='metadata' if rec['file'].startswith(BAND+'_') else 'metadata_json'
 with np.load(path(rec['file']),allow_pickle=False) as f:
  assert set(f.files)==set(rec['metadata']['schema'])|{metadata_key}
  assert json.loads(str(f[metadata_key]))==rec['metadata']
  for n in names:
   a=f[n].copy();RAW['loaded_'+n]=a
   s=rec['metadata']['schema'][n];assert list(a.shape)==s['shape'] and str(a.dtype)==s['dtype'] and np.all(np.isfinite(a)),n
   out[n]=a
 return out

def resolve_record(ref):
 assert sha(path(ref['file']))==ref['sha256'] and sha(path(ref['commit_file']))==ref['commit_sha256']
 out=json.loads(path(ref['commit_file']).read_text())
 assert out['file']==ref['file'] and out['sha256']==ref['sha256']
 return dict(out,commit_file=ref['commit_file'],commit_sha256=ref['commit_sha256'])

def capture(name,a):
 AVAILABLE[name]=a.copy();return a

def finite_real(name,a):
 capture(name,a);assert a.dtype.kind=='f' and np.all(np.isfinite(a)),name
 return a

def native_mask():
 m=np.ones((3,87,45),dtype=bool);m[:,0]=False;m[1,:,0]=False;return m

def lift_velocity(x):
 assert x.shape[-3:]==(3,87,45)
 y=x.copy();y[...,0,0,:]=0;y[...,1,0,:]=y[...,1,1,:];y[...,1,:,0]=0;y[...,2,0,:]=y[...,2,1,:];return y

def restrict_velocity(x):
 assert x.shape[-3:]==(3,87,45)
 y=x.copy();y[...,1,1,:]+=y[...,1,0,:];y[...,2,1,:]+=y[...,2,0,:];y[..., :,0,:]=0;y[...,1,:,0]=0;return y

def evaluate_velocity(x,geo,jet=0):
 # Covector phi value R²N; radial derivative is 2RN+R²NR.
 y=lift_velocity(x);out=np.zeros(x.shape[:-3]+(4,86,44,3))
 for iq in range(4):
  R=geo['R'][iq].reshape(86,44)
  for a,(i,j) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   h=geo['hats'][iq,a,jet];factor=np.broadcast_to(h[...,None],(86,44,3)).copy();factor[...,2]=R**2*h
   if jet==1:factor[...,2]+=2*R*geo['hats'][iq,a,0]
   out[...,iq,:,:,:]+=np.moveaxis(y[..., :,i:86+i,j:44+j],-3,-1)*factor
 return out.reshape(x.shape[:-3]+(15136,3))

def scatter_velocity(field,geo):
 assert field.shape[-2:]==(15136,3)
 f=field.reshape(field.shape[:-2]+(4,86,44,3));out=np.zeros(field.shape[:-2]+(3,87,45))
 for iq in range(4):
  R=geo['R'][iq].reshape(86,44);wq=geo['dv'][iq].reshape(86,44)/R
  for a,(i,j) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   factor=np.broadcast_to(geo['hats'][iq,a,0][...,None],(86,44,3)).copy();factor[...,2]*=R**2
   out[..., :,i:86+i,j:44+j]+=np.moveaxis(f[...,iq,:,:,:]*wq[...,None]*factor,-1,-3)
 return restrict_velocity(out)

def point_action(v,b):
 mixed=v[1:]+np.einsum('jpik,pk->jpi',b['L'],v[0],optimize=True);modes=np.einsum('jpik,jpk->jpi',b['D'],mixed,optimize=True)
 U=np.einsum('pik,pk->pi',b['M0'],v[0],optimize=True)+np.einsum('jpki,jpk->pi',b['L'],modes,optimize=True)
 return np.concatenate((U[None],modes))

def point_action_envelope(v,b):
 mixed=abs(v[1:])+np.einsum('jpik,pk->jpi',b['eL'],abs(v[0]),optimize=True);modes=np.einsum('jpik,jpk->jpi',b['eD'],mixed,optimize=True)
 U=np.einsum('pik,pk->pi',b['eM0'],abs(v[0]),optimize=True)+np.einsum('jpki,jpk->pi',b['eL'],modes,optimize=True)
 return np.concatenate((U[None],modes))

def metric_mask():
 m=np.ones((6,87,45),dtype=bool);m[:,0]=False;m[3:5,:,0]=False;return m

def lift_metric(x):
 assert x.shape[-3:]==(6,87,45)
 y=x.copy();y[..., :,0,:]=y[..., :,1,:];y[...,3:5,:,0]=0;return y

def restrict_metric(x):
 assert x.shape[-3:]==(6,87,45)
 y=x.copy();y[..., :,1,:]+=y[..., :,0,:];y[..., :,0,:]=0;y[...,3:5,:,0]=0;return y

def metric_value_matrix(R):
 # Physical local order RR,ZZ,phiphi,RZ,Rphi,Zphi. Coefficient order a,b,c,d,e,f.
 F=np.zeros(R.shape+(6,6));F[...,0,0]=1;F[...,0,1]=R**2;F[...,1,5]=1;F[...,2,0]=R**2;F[...,3,3]=R;F[...,4,2]=R**3;F[...,5,4]=R**2
 return F

def metric_R_matrix(R):
 F=np.zeros(R.shape+(6,6));F[...,0,1]=2*R;F[...,2,0]=2*R;F[...,3,3]=1;F[...,4,2]=3*R**2;F[...,5,4]=2*R
 return F

def evaluate_metric(x,geo,jet=0):
 y=lift_metric(x);out=np.zeros(x.shape[:-3]+(4,86,44,6))
 for iq in range(4):
  R=geo['R'][iq].reshape(86,44);F=metric_value_matrix(R)
  for a,(i,j) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   h=geo['hats'][iq,a,jet];factor=h[...,None,None]*F
   if jet==1:factor+=geo['hats'][iq,a,0][...,None,None]*metric_R_matrix(R)
   vals=np.moveaxis(y[..., :,i:86+i,j:44+j],-3,-1)
   out[...,iq,:,:,:]+=np.einsum('...ijb,ijab->...ija',vals,factor,optimize=True)
 return out.reshape(x.shape[:-3]+(15136,6))

def scatter_metric(field,geo):
 assert field.shape[-2:]==(15136,6)
 f=field.reshape(field.shape[:-2]+(4,86,44,6));out=np.zeros(field.shape[:-2]+(6,87,45))
 for iq in range(4):
  R=geo['R'][iq].reshape(86,44);wq=(geo['dv'][iq]/geo['R'][iq]).reshape(86,44);F=metric_value_matrix(R)
  for a,(i,j) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   val=np.einsum('...ija,ijab->...ijb',f[...,iq,:,:,:],F,optimize=True)*wq[...,None]*geo['hats'][iq,a,0][...,None]
   out[..., :,i:86+i,j:44+j]+=np.moveaxis(val,-1,-3)
 return restrict_metric(out)

def scalar_lift(x):
 assert x.shape[-2:]==(87,45)
 y=x.copy();y[...,0,:]=y[...,1,:];return y

def scalar_scatter(field,geo):
 assert field.shape[-1]==15136
 f=field.reshape(field.shape[:-1]+(4,86,44));out=np.zeros(field.shape[:-1]+(87,45))
 for iq in range(4):
  wq=(geo['dv'][iq]/geo['R'][iq]).reshape(86,44)
  for a,(i,j) in enumerate(((0,0),(1,0),(0,1),(1,1))):out[...,i:86+i,j:44+j]+=wq*geo['hats'][iq,a,0]*f[...,iq,:,:]
 out[...,1,:]+=out[...,0,:];out[...,0,:]=0;return out

def point_metric_tensor(k):
 # k represents a symmetric metric VELOCITY; offdiagonal k values are actual hdot_ij.
 out=np.zeros(k.shape[:-1]+(3,3));out[...,0,0]=k[...,0];out[...,1,1]=k[...,1];out[...,2,2]=k[...,2]
 for a,(i,j) in enumerate(((0,1),(0,2),(1,2)),3):out[...,i,j]=out[...,j,i]=k[...,a]
 return out

def trace_CMC_actions(k,ih,N,mu,g):
 tensor=point_metric_tensor(k);tr=np.einsum('pij,...pij->...p',ih,tensor,optimize=True)/(2*N)
 return scalar_scatter(mu*tr,g)

def scalar_evaluate(x,g):
 y=scalar_lift(x);out=np.zeros((4,86,44))
 for iq in range(4):
  for a,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):out[iq]+=g['hats'][iq,a,0]*y[di:86+di,dj:44+dj]
 return out.reshape(15136)

def trace_forward(k,d,g):return trace_CMC_actions(evaluate_metric(k,g),d['ih'],d['N'],d['mu'],g)

def scalar_mask():
 mask=np.ones((87,45),dtype=bool);mask[0]=False;return mask

def pack_fields(v,k,lam=None):
 out=[v[np.broadcast_to(native_mask(),v.shape)],k[metric_mask()]]
 if lam is not None:out.append(lam[scalar_mask()])
 return np.concatenate(out)

def unpack_fields(x,constrained):
 nv=380292;nk=23048;assert len(x)==nv+nk+(3870 if constrained else 0)
 v=np.zeros((33,3,87,45));k=np.zeros((6,87,45));v[np.broadcast_to(native_mask(),v.shape)]=x[:nv];k[metric_mask()]=x[nv:nv+nk]
 lam=None
 if constrained:lam=np.zeros((87,45));lam[scalar_mask()]=x[nv+nk:]
 return v,k,lam

def coupled_action(v,k,b,d,g):
 vp=evaluate_velocity(v,g);kv=evaluate_metric(k,g);vf=vp.transpose(1,0,2).reshape(15136,99)
 bk=np.einsum('pia,pa->pi',d['B'],kv,optimize=True).reshape(15136,33,3).transpose(1,0,2)
 n=scatter_velocity(point_action(vp,b)+bk,g)
 m=scatter_metric(np.einsum('pia,pi->pa',d['B'],vf,optimize=True)+np.einsum('pab,pb->pa',d['T'],kv,optimize=True),g)
 return n,m

def coupled_envelope(v,k,b,d,g):
 vp=abs(evaluate_velocity(abs(v),g));kv=abs(evaluate_metric(abs(k),g))
 # Metric R powers and value hats are nonnegative; all cancellation is bounded upstream.
 vf=vp.transpose(1,0,2).reshape(15136,99);bk=np.einsum('pia,pa->pi',d['eB'],kv,optimize=True).reshape(15136,33,3).transpose(1,0,2)
 n=scatter_velocity(point_action_envelope(vp,b)+bk,g)
 m=scatter_metric(np.einsum('pia,pi->pa',d['eB'],vf,optimize=True)+np.einsum('pab,pb->pa',d['eT'],kv,optimize=True),g)
 return n,m

def original_ratios(res,rhs,scale):
 raw=float(np.linalg.norm(res));den=float(np.linalg.norm(rhs));white=float(np.linalg.norm(res/scale));wd=float(np.linalg.norm(rhs/scale))
 assert all(math.isfinite(x) for x in (raw,den,white,wd)) and (den>0)==(wd>0)
 if den==0:return np.array((0.,0.)) if raw==white==0 else np.array((math.inf,math.inf))
 return np.array((raw/den,white/wd))

def minres_core(A,rhs,scale,tolerance,certificate,label,cap=CAP):
 # The same bounded recurrence serves fresh dense witnesses and the full field.
 white_rhs=rhs/scale;wn=float(np.linalg.norm(white_rhs));capture(label+'_white_rhs',white_rhs);assert math.isfinite(wn)
 if wn==0:
  assert np.all(rhs==0);x=np.zeros_like(rhs);res,ratios=certificate(x);return x,ratios,bool(np.all(ratios<=LINEAR_TOL)),'zero_rhs'
 assert math.isfinite(tolerance) and tolerance>0
 def W(y):return A(y/scale)/scale
 y=np.zeros_like(rhs);r=white_rhs.copy();beta=float(np.linalg.norm(r));v=r/beta;pv=np.zeros_like(v);ow=np.zeros_like(v);pw=np.zeros_like(v)
 cs=-1.;sn=0.;dbar=eps=0.;phibar=beta;history=[];reason='iteration_cap'
 for it in range(1,cap+1):
  z=W(v);capture(label+'_Lanczos_action',z);assert np.all(np.isfinite(z));z=z-beta*pv;alpha=float(np.sum(v*z));z=z-alpha*v;next_beta=float(np.linalg.norm(z))
  oldeps=eps;delta=cs*dbar+sn*alpha;gbar=sn*dbar-cs*alpha;eps=sn*next_beta;dbar=-cs*next_beta;gamma=math.hypot(gbar,next_beta)
  capture(label+'_Lanczos_scalars',np.array((it,alpha,beta,next_beta,gamma,phibar)))
  if not all(math.isfinite(a) for a in (alpha,next_beta,delta,gbar,eps,dbar,gamma)) or gamma==0:reason='Lanczos_or_Givens_breakdown';break
  cs=gbar/gamma;sn=next_beta/gamma;phi=cs*phibar;phibar=sn*phibar;w=(v-oldeps*ow-delta*pw)/gamma;y=y+phi*w
  capture(label+'_white_iterate',y);capture(label+'_Lanczos_direction',v);capture(label+'_MINRES_direction',w)
  assert np.all(np.isfinite(y)) and np.all(np.isfinite(w))
  if it%20==0 or abs(phibar)/wn<=tolerance or next_beta==0 or it==cap:
   x=y/scale;res,ratios=certificate(x);white_res=float(np.linalg.norm(res/scale))/wn
   history.append((it,white_res,float(np.max(ratios))));capture(label+'_history',np.asarray(history));capture(label+'_original_iterate',x)
   if np.all(ratios<=LINEAR_TOL):reason='all_original_rows_admitted';break
   if it%40==0:checkpoint('ITERATION',{k:a for k,a in AVAILABLE.items() if k.startswith(label+'_') and k.endswith(('iterate','residual','history','scalars'))},dict(kind='unqualified_restart_snapshot_signed_MINRES_iterate',stage=label,iteration=it))
  if next_beta==0:reason='Lanczos_terminal_original_rows_failed';break
  ow=pw;pw=w;pv=v;v=z/next_beta;beta=next_beta
 x=y/scale;res,ratios=certificate(x);capture(label+'_history',np.asarray(history));capture(label+'_original_iterate',x)
 return x,ratios,bool(np.all(ratios<=LINEAR_TOL)),reason

def a_keep(name,**arrays):
 # Retain references to newly created arrays; caller snapshots on refusal.
 DD_ARRAY_CURRENT.clear();DD_ARRAY_CURRENT.update(operation=name,arrays=arrays)
 for a in arrays.values():assert a.dtype==np.float64 and np.all(np.isfinite(a)),name

def a_sum(x,y):
 x=np.asarray(x,dtype=np.float64);y=np.asarray(y,dtype=np.float64);a_keep('two_sum_inputs',x=x,y=y)
 s=x+y;a_keep('two_sum_sum',x=x,y=y,s=s)
 bb=s-x;a_keep('two_sum_split',x=x,y=y,s=s,bb=bb)
 e=(x-(s-bb))+(y-bb);a_keep('two_sum_result',s=s,e=e);return s,e

def a_split(x):
 x=np.asarray(x,dtype=np.float64);a_keep('split_input',x=x)
 assert np.all((x==0)|((abs(x)>=2.**-450)&(abs(x)<=2.**450))),'Dekker safe high/low operand domain'
 c=(2.**27+1.)*x;a_keep('split_product',x=x,c=c)
 h=c-(c-x);l=x-h;a_keep('split_result',h=h,l=l);return h,l

def a_prod(x,y):
 x=np.asarray(x,dtype=np.float64);y=np.asarray(y,dtype=np.float64);a_keep('two_prod_inputs',x=x,y=y)
 xh,xl=a_split(x);yh,yl=a_split(y);p=x*y;a_keep('two_prod_product',x=x,y=y,p=p)
 t0=xh*yh-p;a_keep('two_prod_t0',p=p,t0=t0)
 t1=t0+xh*yl;a_keep('two_prod_t1',p=p,t1=t1)
 t2=t1+xl*yh;a_keep('two_prod_t2',p=p,t2=t2)
 e=t2+xl*yl;a_keep('two_prod_result',p=p,e=e);return p,e

def a_dd(x):
 x=np.asarray(x,dtype=np.float64);return x,np.zeros_like(x)

def a_add(x,y):
 s,e=a_sum(x[0],y[0]);t,f=a_sum(x[1],y[1]);u,v=a_sum(e,t)
 h,w=a_sum(s,u);l0,l1=a_sum(w,v);l2,l3=a_sum(l0,f)
 tail0,tail1=a_sum(l1,l3);low0,low1=a_sum(l2,tail0)
 return a_sum(h,low0+(low1+tail1))

def a_sub(x,y):return a_add(x,(-y[0],-y[1]))

def a_mul(x,y):
 out=a_prod(x[0],y[0]);out=a_add(out,a_prod(x[0],y[1]))
 out=a_add(out,a_prod(x[1],y[0]));return a_add(out,a_prod(x[1],y[1]))

def a_mul64(x,y):return a_add(a_prod(x,y[0]),a_prod(x,y[1]))

def a_matvec(A,x):
 # A is a retained binary64 coefficient block; no rounded new coefficient matrix.
 assert A.shape[-1]==x[0].shape[-1] and x[0].shape==x[1].shape
 shape=np.broadcast_shapes(A.shape[:-2],x[0].shape[:-1])+(A.shape[-2],)
 out=a_dd(np.zeros(shape))
 for j in range(A.shape[-1]):out=a_add(out,a_mul64(A[...,j],(x[0][...,j,None],x[1][...,j,None])))
 return out

def a_stack(pairs,axis=0):return np.stack([x[0] for x in pairs],axis=axis),np.stack([x[1] for x in pairs],axis=axis)

def a_slice(pair,key):return pair[0][key],pair[1][key]

def a_reshape(pair,shape):return pair[0].reshape(shape),pair[1].reshape(shape)

def a_transpose(pair,axes):return pair[0].transpose(axes),pair[1].transpose(axes)

def dd_native_value(x,g,capture):
 # Only original binary64 nodal coefficients are candidates, never hidden DD nodes.
 assert x.shape==(33,3,87,45);y=x.copy();y[:,0,0,:]=0;y[:,1,0,:]=y[:,1,1,:];y[:,1,:,0]=0;y[:,2,0,:]=y[:,2,1,:]
 out=a_dd(np.zeros((33,4,86,44,3)))
 for iq in range(4):
  R=g['R'][iq].reshape(86,44)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   hat=g['hats'][iq,corner,0];factor=np.broadcast_to(hat[...,None],(86,44,3)).copy();factor[...,2]=R**2*hat
   val=np.moveaxis(y[:,:,di:86+di,dj:44+dj],1,-1)
   updated=a_add(a_slice(out,(slice(None),iq)),a_prod(val,factor))
   out[0][:,iq]=updated[0];out[1][:,iq]=updated[1]
   capture("native_evaluation_current_partial_hi",out[0]);capture("native_evaluation_current_partial_lo",out[1])
 return a_reshape(out,(33,15136,3))

def dd_metric_F(R):
 F=np.zeros(R.shape+(6,6));F[...,0,0]=1;F[...,0,1]=R**2;F[...,1,5]=1;F[...,2,0]=R**2;F[...,3,3]=R;F[...,4,2]=R**3;F[...,5,4]=R**2
 return F

def dd_metric_value(x,g,capture):
 assert x.shape==(6,87,45);y=x.copy();y[:,0,:]=y[:,1,:];y[3:5,:,0]=0
 out=a_dd(np.zeros((4,86,44,6)))
 for iq in range(4):
  R=g['R'][iq].reshape(86,44);F=dd_metric_F(R)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   hat=g['hats'][iq,corner,0];factor=F*hat[...,None,None]
   exact_factor=a_prod(F,hat[...,None,None]);geometry_defect=a_sub(a_dd(factor),exact_factor)
   capture('geometry_Fhat64_minus_exact_product_q%d_corner%d_hi'%(iq,corner),geometry_defect[0])
   capture('geometry_Fhat64_minus_exact_product_q%d_corner%d_lo'%(iq,corner),geometry_defect[1])
   val=np.moveaxis(y[:,di:86+di,dj:44+dj],0,-1)
   updated=a_add(a_slice(out,iq),a_matvec(factor,a_dd(val)))
   out[0][iq]=updated[0];out[1][iq]=updated[1]
   capture("metric_evaluation_current_partial_hi",out[0]);capture("metric_evaluation_current_partial_lo",out[1])
 return a_reshape(out,(15136,6))

def dd_point_coupled(v,k,b,d,capture):
 # Parent order: M0vU + sum L^T[D(z+LvU)] + Bu k, mode D(z+LvU)+Bz k.
 p=v[0].shape[1];assert v[0].shape==v[1].shape==(33,p,3) and k[0].shape==k[1].shape==(p,6)
 u=a_slice(v,0);modes=[];U=a_matvec(b['M0'],u)
 capture('point_Maxwell_U_hi',U[0]);capture('point_Maxwell_U_lo',U[1])
 for mode in range(32):
  mixed=a_add(a_slice(v,mode+1),a_matvec(b['L'][mode],u))
  capture('point_mode%d_mixed_hi'%mode,mixed[0]);capture('point_mode%d_mixed_lo'%mode,mixed[1])
  Dm=a_matvec(b['D'][mode],mixed)
  capture('point_mode%d_Dmixed_hi'%mode,Dm[0]);capture('point_mode%d_Dmixed_lo'%mode,Dm[1])
  modes.append(Dm);U=a_add(U,a_matvec(b['L'][mode].swapaxes(-1,-2),Dm))
  capture('point_U_through_mode%d_hi'%mode,U[0]);capture('point_U_through_mode%d_lo'%mode,U[1])
 native=a_stack([U]+modes);Bv=a_matvec(d['B'],k)
 native=a_add(native,a_transpose(a_reshape(Bv,(p,33,3)),(1,0,2)))
 vf=a_reshape(a_transpose(v,(1,0,2)),(p,99))
 metric=a_add(a_matvec(d['B'].swapaxes(-1,-2),vf),a_matvec(d['T'],k))
 capture('point_native_action_hi',native[0]);capture('point_native_action_lo',native[1])
 capture('point_metric_action_hi',metric[0]);capture('point_metric_action_lo',metric[1])
 return native,metric

def dd_native_scatter(field,g,capture):
 assert field[0].shape==field[1].shape==(33,15136,3)
 f=a_reshape(field,(33,4,86,44,3));out=a_dd(np.zeros((33,3,87,45)))
 for iq in range(4):
  R=g['R'][iq].reshape(86,44);weight=(g['dv'][iq]/g['R'][iq]).reshape(86,44)
  weighted=a_mul64(weight[...,None],a_slice(f,(slice(None),iq)))
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   hat=g['hats'][iq,corner,0];factor=np.broadcast_to(hat[...,None],(86,44,3)).copy();factor[...,2]*=R**2
   val=a_transpose(a_mul64(factor,weighted),(0,3,1,2));key=(slice(None),slice(None),slice(di,86+di),slice(dj,44+dj))
   update=a_add(a_slice(out,key),val);out[0][key]=update[0];out[1][key]=update[1]
   capture("scatter_current_partial_hi",out[0]);capture("scatter_current_partial_lo",out[1])
 for component in (1,2):
  update=a_add(a_slice(out,(slice(None),component,1,slice(None))),a_slice(out,(slice(None),component,0,slice(None))))
  out[0][:,component,1]=update[0];out[1][:,component,1]=update[1]
  capture("native_scatter_current_restricted_hi",out[0]);capture("native_scatter_current_restricted_lo",out[1])
 out[0][:,:,0]=0;out[1][:,:,0]=0;out[0][:,1,:,0]=0;out[1][:,1,:,0]=0
 return out

def dd_metric_scatter(field,g,capture):
 # Original scatter F64 contraction, then weight64 and hat64 separately.
 assert field[0].shape==field[1].shape==(15136,6)
 f=a_reshape(field,(4,86,44,6));out=a_dd(np.zeros((6,87,45)))
 for iq in range(4):
  R=g['R'][iq].reshape(86,44);F=dd_metric_F(R);weight=(g['dv'][iq]/g['R'][iq]).reshape(86,44)
  FTf=a_matvec(F.swapaxes(-1,-2),a_slice(f,iq));weighted=a_mul64(weight[...,None],FTf)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   value=a_mul64(g['hats'][iq,corner,0][...,None],weighted);val=a_transpose(value,(2,0,1));key=(slice(None),slice(di,86+di),slice(dj,44+dj))
   update=a_add(a_slice(out,key),val);out[0][key]=update[0];out[1][key]=update[1]
   capture("scatter_current_partial_hi",out[0]);capture("scatter_current_partial_lo",out[1])
 update=a_add(a_slice(out,(slice(None),1,slice(None))),a_slice(out,(slice(None),0,slice(None))))
 out[0][:,1]=update[0];out[1][:,1]=update[1];capture("metric_scatter_current_restricted_hi",out[0]);capture("metric_scatter_current_restricted_lo",out[1]);out[0][:,0]=0;out[1][:,0]=0;out[0][3:5,:,0]=0;out[1][3:5,:,0]=0
 return out

def global_coupled_action_dd(v,k,b,d,g,capture):
 vp=dd_native_value(v,g,capture);capture('native_point_rate_hi',vp[0]);capture('native_point_rate_lo',vp[1])
 kp=dd_metric_value(k,g,capture);capture('metric_point_rate_hi',kp[0]);capture('metric_point_rate_lo',kp[1])
 npnt,mpnt=dd_point_coupled(vp,kp,b,d,capture)
 n=dd_native_scatter(npnt,g,capture);capture('native_weak_action_hi',n[0]);capture('native_weak_action_lo',n[1])
 m=dd_metric_scatter(mpnt,g,capture);capture('metric_weak_action_hi',m[0]);capture('metric_weak_action_lo',m[1])
 return n,m

def original_residual_dd(rhs,action):return a_sub(a_dd(rhs),action)

def rounded_node_update(base,delta,capture,label):
 # Original binary64 candidate is the high word; the low word is a disclosed defect.
 high,low=a_sum(base,delta);capture(label+'_actual_binary64_nodes',high);capture(label+'_exact_update_minus_actual_nodes',low)
 return high,low

def shifted_residual_with_update_defect(base_residual,delta_action,node_rounding_action):
 # A(x_actual)=A(xbase)+A(delta)-A(exact_update_minus_actual_nodes).
 return a_add(a_sub(base_residual,delta_action),node_rounding_action)

def bind(n,h):
 key=str(path(n).resolve());assert key not in INPUTS or INPUTS[key]==h
 assert sha(path(n))==h,n;INPUTS[key]=h

def collapse(pair,label):
 value=pair[0]+pair[1];capture(label+'_hi',pair[0]);capture(label+'_lo',pair[1]);capture(label+'_rounded_value',value)
 assert np.all(np.isfinite(value));return value

def pack_dd(n,m):return pack_fields(n[0],m[0]),pack_fields(n[1],m[1])

def scaled_norm_ratios(pair,reference,scale,label):
 value=collapse(pair,label);return original_ratios(value,reference,scale)

def accurate_original_action(x,b,d,g,label):
 CONTEXT.update(active_action=label)
 v,k,_=unpack_fields(x,False);n,m=global_coupled_action_dd(v,k,b,d,g,capture);action=pack_dd(n,m)
 capture(label+'_action_hi',action[0]);capture(label+'_action_lo',action[1]);return action

def original_field_bound(rhs,affine,scales):
 bounds=[]
 for value,scale in zip(unpack_fields(rhs,False)[:2],scales[:2]):
  raw=float(np.linalg.norm(value));white=float(np.linalg.norm(value/scale));assert math.isfinite(raw) and math.isfinite(white) and raw>0 and white>0
  bounds.extend((raw/float(np.max(scale)),white))
 for target,scale in zip((affine['Pn'],affine['Pm']),scales[:2]):
  raw=float(np.linalg.norm(target));white=float(np.linalg.norm(target/scale));assert math.isfinite(raw) and math.isfinite(white) and raw>0 and white>0
  bounds.extend((raw/float(np.max(scale)),white))
 return min(bounds)

"""Definitions only: two-word values in the SAME native/metric Q1 coordinates.
ROOT supplies the accepted array DD primitives, point/scatter kernels and geometry.
No new physical DOF, coefficient, source, gauge, RHS or solver cap is registered.
"""
np=None

def dd_native_node_value(x,g,capture,jet=0):
 assert x[0].shape==x[1].shape==(33,3,87,45) and jet in (0,1,2)
 y=(lift_velocity(x[0]),lift_velocity(x[1]));out=a_dd(np.zeros((33,4,86,44,3)))
 capture('dd_native_input_nodes_hi',x[0]);capture('dd_native_input_nodes_lo',x[1])
 for iq in range(4):
  R=g['R'][iq].reshape(86,44)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   hat=g['hats'][iq,corner,jet];factor=np.broadcast_to(hat[...,None],(86,44,3)).copy();factor[...,2]=R**2*hat
   if jet==1:factor[...,2]+=2*R*g['hats'][iq,corner,0]
   val=(np.moveaxis(y[0][:,:,di:86+di,dj:44+dj],1,-1),np.moveaxis(y[1][:,:,di:86+di,dj:44+dj],1,-1))
   updated=a_add(a_slice(out,(slice(None),iq)),a_mul64(factor,val));out[0][:,iq]=updated[0];out[1][:,iq]=updated[1]
   capture('dd_native_current_jet%d_partial_hi'%jet,out[0]);capture('dd_native_current_jet%d_partial_lo'%jet,out[1])
 return a_reshape(out,(33,15136,3))
def dd_metric_node_value(x,g,capture,jet=0):
 assert x[0].shape==x[1].shape==(6,87,45) and jet in (0,1,2)
 y=(lift_metric(x[0]),lift_metric(x[1]));out=a_dd(np.zeros((4,86,44,6)))
 capture('dd_metric_input_nodes_hi',x[0]);capture('dd_metric_input_nodes_lo',x[1])
 for iq in range(4):
  R=g['R'][iq].reshape(86,44);F=dd_metric_F(R)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   hat=g['hats'][iq,corner,jet];factor=hat[...,None,None]*F
   if jet==1:factor+=g['hats'][iq,corner,0][...,None,None]*metric_R_matrix(R)
   val=(np.moveaxis(y[0][:,di:86+di,dj:44+dj],0,-1),np.moveaxis(y[1][:,di:86+di,dj:44+dj],0,-1))
   updated=a_add(a_slice(out,iq),a_matvec(factor,val));out[0][iq]=updated[0];out[1][iq]=updated[1]
   capture('dd_metric_current_jet%d_partial_hi'%jet,out[0]);capture('dd_metric_current_jet%d_partial_lo'%jet,out[1])
 return a_reshape(out,(15136,6))
def dd_node_original_action(x,b,d,g,capture):
 assert x[0].shape==x[1].shape==(403340,)
 vh,kh,_=unpack_fields(x[0],False);vl,kl,_=unpack_fields(x[1],False)
 vp=dd_native_node_value((vh,vl),g,capture);kp=dd_metric_node_value((kh,kl),g,capture)
 capture('dd_native_point_rate_hi',vp[0]);capture('dd_native_point_rate_lo',vp[1]);capture('dd_metric_point_rate_hi',kp[0]);capture('dd_metric_point_rate_lo',kp[1])
 n,m=dd_point_coupled(vp,kp,b,d,capture)
 nw=dd_native_scatter(n,g,capture);mw=dd_metric_scatter(m,g,capture)
 capture('dd_original_native_action_hi',nw[0]);capture('dd_original_native_action_lo',nw[1]);capture('dd_original_metric_action_hi',mw[0]);capture('dd_original_metric_action_lo',mw[1])
 return pack_dd(nw,mw)
def dd_node_update(start,delta,capture,label):
 # Exact three-word EFT sum; a disclosed third word is the compression defect.
 capture(label+'_old_nodes_hi',start[0]);capture(label+'_old_nodes_lo',start[1]);capture(label+'_float_correction',delta)
 s,e=a_sum(start[0],delta);t,f=a_sum(start[1],e);h,g=a_sum(s,t);l,q=a_sum(g,f);hi,lo=a_sum(h,l)
 capture(label+'_updated_nodes_hi',hi);capture(label+'_updated_nodes_lo',lo);capture(label+'_exact_update_minus_two_word_nodes',q)
 return (hi,lo),q

def a_div64(x,den,capture,label):
 # Division by the ORIGINAL finite denominator, no newly frozen reciprocal.
 den=np.asarray(den,dtype=np.float64);capture(label+'_denominator',den);assert np.all(np.isfinite(den)) and np.all(den!=0)
 q1=x[0]/den;capture(label+'_first_quotient',q1);r=a_sub(x,a_mul64(den,a_dd(q1)))
 capture(label+'_first_remainder_hi',r[0]);capture(label+'_first_remainder_lo',r[1])
 q2=(r[0]+r[1])/den;capture(label+'_second_quotient',q2);q=a_sum(q1,q2)
 r=a_sub(x,a_mul64(den,q));capture(label+'_second_remainder_hi',r[0]);capture(label+'_second_remainder_lo',r[1])
 q3=(r[0]+r[1])/den;capture(label+'_third_quotient',q3);q=a_add(q,a_dd(q3))
 residual=a_sub(x,a_mul64(den,q));capture(label+'_division_defect_hi',residual[0]);capture(label+'_division_defect_lo',residual[1]);capture(label+'_quotient_hi',q[0]);capture(label+'_quotient_lo',q[1])
 return q
def dd_scalar_scatter(field,g,capture,label):
 assert field[0].shape==field[1].shape==(15136,)
 f=a_reshape(field,(4,86,44));out=a_dd(np.zeros((87,45)))
 for iq in range(4):
  weighted=a_mul64((g['dv'][iq]/g['R'][iq]).reshape(86,44),a_slice(f,iq))
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   val=a_mul64(g['hats'][iq,corner,0],weighted);key=(slice(di,86+di),slice(dj,44+dj));update=a_add(a_slice(out,key),val)
   out[0][key]=update[0];out[1][key]=update[1];capture(label+'_scalar_scatter_partial_hi',out[0]);capture(label+'_scalar_scatter_partial_lo',out[1])
 update=a_add(a_slice(out,(1,slice(None))),a_slice(out,(0,slice(None))));out[0][1]=update[0];out[1][1]=update[1];out[0][0]=0;out[1][0]=0
 capture(label+'_scalar_scatter_hi',out[0]);capture(label+'_scalar_scatter_lo',out[1]);return out
def dd_node_trace(x,d,g,capture,label):
 vh,kh,_=unpack_fields(x[0],False);vl,kl,_=unpack_fields(x[1],False);kp=dd_metric_node_value((kh,kl),g,capture)
 # Both entries of each symmetric offdiagonal contraction remain explicit.
 terms=[]
 for coord,(i,j) in enumerate(((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))):
  terms.append(a_mul64(d['ih'][:,i,j],a_slice(kp,(slice(None),coord))))
  if i!=j:terms.append(a_mul64(d['ih'][:,j,i],a_slice(kp,(slice(None),coord))))
 total=a_dd(np.zeros(15136))
 for i,term in enumerate(terms):total=a_add(total,term);capture(label+'_trace_contraction_through%d_hi'%i,total[0]);capture(label+'_trace_contraction_through%d_lo'%i,total[1])
 tr=a_div64(total,2*d['N'],capture,label+'_trace_normalization');weighted=a_mul64(d['mu'],tr)
 capture(label+'_point_density_hi',weighted[0]);capture(label+'_point_density_lo',weighted[1]);return dd_scalar_scatter(weighted,g,capture,label)
def dd_node_rate_jets(x,g,capture):
 vh,kh,_=unpack_fields(x[0],False);vl,kl,_=unpack_fields(x[1],False);out={}
 for jet,axis in enumerate(('value','R','Z')):
  for name,pair,evalf in (('native',(vh,vl),dd_native_node_value),('metric',(kh,kl),dd_metric_node_value)):
   value=evalf(pair,g,capture,jet);out[name+'_jet_'+axis+'_hi']=value[0];out[name+'_jet_'+axis+'_lo']=value[1]
 return out


def node_candidate_certificate(x,rhs,b,d,g,affine,scales,label):
 CONTEXT.update(active_action=label);action=dd_node_original_action(x,b,d,g,capture)
 capture(label+'_action_hi',action[0]);capture(label+'_action_lo',action[1]);res=original_residual_dd(rhs,action);capture(label+'_residual_hi',res[0]);capture(label+'_residual_lo',res[1])
 rf=fields_from_pair(res,label+'_original_residual');right=unpack_fields(rhs,False);ah,al=unpack_fields(action[0],False),unpack_fields(action[1],False);rows=[]
 for i,name in enumerate(('native','metric')):
  ratio=original_ratios(rf[i],right[i],scales[i]);capture(label+'_'+name+'_original_ratios',ratio);rows.append(ratio)
  target=affine['Pn' if i==0 else 'Pm'];offset=affine['cn' if i==0 else 'cm'];actual=a_sub(a_dd(target),a_add(a_dd(offset),(ah[i],al[i])))
  ratio=scaled_norm_ratios(actual,target,scales[i],label+'_'+name+'_actual_target_residual');capture(label+'_'+name+'_actual_target_ratios',ratio);rows.append(ratio)
 tr=dd_node_trace(x,d,g,capture,label+'_trace');capture(label+'_weak_trace_action_hi',tr[0]);capture(label+'_weak_trace_action_lo',tr[1]);tg=a_sub(tr,a_dd(affine['trace_rhs']))
 ratio=scaled_norm_ratios(tg,affine['trace_rhs'],scales[2],label+'_weak_trace_residual');capture(label+'_weak_trace_ratios',ratio)
 return action,res,np.stack(rows),ratio

def fields_from_pair(x,label):return unpack_fields(collapse(x,label),False)
def node_positive_envelope(x,b,d,g,label):
 vh,kh,_=unpack_fields(x[0],False);vl,kl,_=unpack_fields(x[1],False)
 n,m=coupled_envelope(abs(vh)+abs(vl),abs(kh)+abs(kl),b,d,g);capture(label+'_native_positive_bound',n);capture(label+'_metric_positive_bound',m)
 assert np.all(np.isfinite(n)) and np.all(np.isfinite(m)) and np.all(n>=0) and np.all(m>=0);return pack_fields(n,m)
def load_dd_node_seed(system,parent,proof):
 # Same frozen coefficient, geometry, actual target and rounded affine operands.
 columns=[]
 for i in range(4):
  c=read_pair(system[str(i)],('B','T','eB','eT','ih','N','mu'))
  for n,a in c.items():capture('saved_column%d_'%i+n,a)
  columns.append(c)
 d={n:np.concatenate([c[n] for c in columns]) for n in columns[0]}
 for n,a in d.items():capture('original_assembled_'+n,a)
 cr=read_pair(system['coefficient'],('mixing_L','modal_D','Maxwell_M0','operation_eL','operation_eD','operation_eM0'))
 b=dict(L=cr['mixing_L'],D=cr['modal_D'],M0=cr['Maxwell_M0'],eL=cr['operation_eL'],eD=cr['operation_eD'],eM0=cr['operation_eM0'])
 gr=read_pair(system['basis'],('R','dv','hats','cell_i','cell_j','native_scale','metric_scale','scalar_scale','r','z'))
 for n,a in gr.items():capture('saved_basis_'+n,a)
 affine=read_pair(system['affine'],('Pn','Pm','cn','cm','trace_rhs'));scales=(gr['native_scale'],gr['metric_scale'],gr['scalar_scale'])
 sol=read_pair(parent['solution'],('native_nodal_rate','metric_nodal_rate','original_rhs','current_Pn','current_Pm','original_action_hi','original_action_lo','original_residual_hi','original_residual_lo'))
 last='cycle_003';high_key=last+'_final_update_actual_binary64_nodes';low_key=last+'_final_update_exact_update_minus_actual_nodes'
 correction=read_pair(parent['correction'],(high_key,low_key));high=pack_fields(sol['native_nodal_rate'],sol['metric_nodal_rate']);low=correction[low_key]
 capture('seed_final_binary64_nodes',high);capture('seed_last_discarded_update_low',low)
 assert np.array_equal(high,correction[high_key]) and high.shape==low.shape==(403340,)
 assert np.array_equal(sol['current_Pn'],affine['Pn']) and np.array_equal(sol['current_Pm'],affine['Pm'])
 rhs=sol['original_rhs'];assert np.array_equal(rhs,pack_fields(affine['Pn']-affine['cn'],affine['Pm']-affine['cm']))
 data=dict(seed_nodes_hi=high,seed_nodes_lo=low,original_rhs=rhs,current_Pn=affine['Pn'],current_Pm=affine['Pm'],rounded_global_cn=affine['cn'],rounded_global_cm=affine['cm'],weak_trace_rhs=affine['trace_rhs'],native_scale=scales[0],metric_scale=scales[1],scalar_scale=scales[2],parent_binary64_action_hi=sol['original_action_hi'],parent_binary64_action_lo=sol['original_action_lo'],parent_binary64_residual_hi=sol['original_residual_hi'],parent_binary64_residual_lo=sol['original_residual_lo'])
 rec=checkpoint('SEED',data,dict(kind='disclosed_two_word_candidate_final_high_plus_actual_last_discarded_low',system_refs=system,parent_refs=parent,proof=proof,original_nonadmission_preserved=True,state_adopted=False,original_rhs_changed=False,source_or_coefficients_changed=False,point_reference_and_restart_defects='preserved through authenticated parent INITIAL and RECOVERED_BASE references'))
 return (high,low),rhs,b,d,gr,affine,scales,rec

def measure_dd_node_candidate(seed,rhs,b,d,g,affine,scales):
 current=seed;scale=pack_fields(scales[0],scales[1]);capture('unchanged_positive_congruence',scale);assert np.all(np.isfinite(scale)) and np.all(scale>0)
 action,res,ratios,tr=node_candidate_certificate(current,rhs,b,d,g,affine,scales,'initial_dd_nodes')
 checkpoint('INITIAL',dict(AVAILABLE),dict(kind='new_full_two_word_node_candidate_original_certificate',original_affine_and_actual_target_ratios=ratios.tolist(),weak_trace_ratios=tr.tolist(),binary64_nodes_not_adopted=True,source_or_coefficient_change=False));cycles=[]
 for cycle in range(1,MAX_CYCLES+1):
  if np.all(ratios<=LINEAR_TOL) and np.all(tr<=LINEAR_TOL):break
  label='cycle_%03d'%cycle;start=current;base_res=res
  rhs_c=collapse(base_res,label+'_correction_rhs');defect=a_sub(base_res,a_dd(rhs_c));capture(label+'_rhs_rounding_defect_hi',defect[0]);capture(label+'_rhs_rounding_defect_lo',defect[1])
  wn=float(np.linalg.norm(rhs_c/scale));assert math.isfinite(wn) and wn>0;tolerance=LINEAR_TOL*original_field_bound(rhs,affine,scales)/wn;capture(label+'_sufficient_white_tolerance',np.array(tolerance));assert math.isfinite(tolerance) and tolerance>0
  def A(delta):
   v,k,_=unpack_fields(delta,False);n,m=coupled_action(v,k,b,d,g);out=pack_fields(n,m);capture(label+'_latest_float_recurrence_action',out);assert np.all(np.isfinite(out));return out
  def certificate(delta):
   nodes,q=dd_node_update(start,delta,capture,label+'_update');act,r,ra,tra=node_candidate_certificate(nodes,rhs,b,d,g,affine,scales,label)
   return collapse(r,label+'_certificate_residual'),np.concatenate((ra,tra[None]),axis=0)
  delta,callback_ratios,ok,reason=minres_core(A,rhs_c,scale,tolerance,certificate,label,cap=CAP);capture(label+'_completed_correction',delta)
  current,q=dd_node_update(start,delta,capture,label+'_final_update');action,res,ratios,tr=node_candidate_certificate(current,rhs,b,d,g,affine,scales,label+'_final')
  da=dd_node_original_action(a_dd(delta),b,d,g,capture)
  capture(label+'_delta_action_hi',da[0]);capture(label+'_delta_action_lo',da[1])
  qa=dd_node_original_action(a_dd(q),b,d,g,capture)
  capture(label+'_compression_defect_action_hi',qa[0]);capture(label+'_compression_defect_action_lo',qa[1])
  prediction=shifted_residual_with_update_defect(base_res,da,qa);gap=a_sub(res,prediction);capture(label+'_prediction_hi',prediction[0]);capture(label+'_prediction_lo',prediction[1]);capture(label+'_update_identity_gap_hi',gap[0]);capture(label+'_update_identity_gap_lo',gap[1])
  bound=2*abs(rhs)
  for name,nodes in (('start',start),('new',current),('delta',a_dd(delta)),('compression',a_dd(q))):bound=bound+node_positive_envelope(nodes,b,d,g,label+'_'+name);capture(label+'_uncancelled_bound_through_'+name,bound)
  actual=np.array([np.linalg.norm(x) for x in fields_from_pair(gap,label+'_update_gap')[:2]]);env=np.array([np.linalg.norm(x) for x in unpack_fields(bound,False)[:2]])
  capture(label+'_update_identity_norms',actual);capture(label+'_update_identity_positive_norm_bounds',env);check(label+'_two_word_update_with_explicit_third_word_defect',actual,np.zeros(2),env)
  row=dict(cycle=cycle,cap=CAP,solver_reason=reason,callback_admitted=bool(ok),original_affine_and_actual_target_ratios=ratios.tolist(),weak_trace_ratios=tr.tolist(),third_word_compression_defect_retained=True);cycles.append(row)
  checkpoint('CORRECTION',{n:a for n,a in AVAILABLE.items() if n.startswith(label+'_')},dict(kind='bounded_float_correction_with_unrounded_two_word_node_certificate',controls=CHECKS[-1:],**row))
 admitted=bool(np.all(ratios<=LINEAR_TOL) and np.all(tr<=LINEAR_TOL));return current,action,res,ratios,tr,admitted,cycles

def save_dd_node_solution(x,action,res,ratios,tr,admitted,cycles,rhs,affine,g,system,parent):
 vh,kh,_=unpack_fields(x[0],False);vl,kl,_=unpack_fields(x[1],False);ah=unpack_fields(action[0],False);al=unpack_fields(action[1],False)
 pn=a_add(a_dd(affine['cn']),(ah[0],al[0]));pm=a_add(a_dd(affine['cm']),(ah[1],al[1]));capture('new_Pn_hi',pn[0]);capture('new_Pn_lo',pn[1]);capture('new_Pm_hi',pm[0]);capture('new_Pm_lo',pm[1])
 data=dict(native_nodal_rate_hi=vh,native_nodal_rate_lo=vl,metric_nodal_rate_hi=kh,metric_nodal_rate_lo=kl,current_Pn=affine['Pn'],current_Pm=affine['Pm'],new_Pn_hi=pn[0],new_Pn_lo=pn[1],new_Pm_hi=pm[0],new_Pm_lo=pm[1],original_rhs=rhs,original_action_hi=action[0],original_action_lo=action[1],original_residual_hi=res[0],original_residual_lo=res[1],original_affine_and_actual_target_ratios=ratios,weak_trace_ratios=tr,trace_rhs=affine['trace_rhs'])
 data.update({n:a for n,a in RAW.items() if n.startswith('control_')})
 sol=checkpoint('SOLUTION',data,dict(kind='two_word_actual_canonical_compatibility_test',stage='compatibility',canonical_rows_admitted=bool(np.all(ratios<=LINEAR_TOL)),trace_row_admitted=bool(np.all(tr<=LINEAR_TOL)),canonical_and_trace_admitted=admitted,basis_ref=system['basis'],parent_refs=parent,targets_unchanged=True,metric_momentum_preparation=False,precision_scope='same real403340 coordinates represented by hi+lo',physical_adoption=False,corrections=cycles));rate=None
 if admitted:
  jets=dd_node_rate_jets(x,g,capture);rate=checkpoint('RATE_JETS',jets,dict(kind='genuine_fixed_Q1_two_word_rate_value_and_spatial_jets',stage='compatibility',canonical_rows_admitted=True,weak_trace_admitted=True,pointwise_CMC_claim=False,basis_ref=system['basis'],collapse_to_binary64_adopted=False,physical_time_history=None,consumer_requirement='retain both words through momenta and later nonlinear state reconstruction'))
 return sol,rate


# Definitions only; caller supplies path, sha, bind, INPUTS and json.
# Read only earned current terminal/selected record metadata; no operator or array calls.
DD_NODE_PARENT='CROSS_U_CANONICAL_NODAL_METRIC_RATE_DD_REFINEMENT_V001'
DD_NODE_TERMINAL=dict(pid=45073,source_sha256='7725619fd925c7fc91796b495a482d71fa24756a75537e72839d6090d7e774db',protocol_sha256='32f3abd7e056c29ab41474a3eb06ec1969f3a8de9aa1a8a160b9cf80414dd884',result_sha256='cbf7b2e4a2117ebcd3a4cd76a7189d17578371f90a715c24483a55e75a220489',receipt_sha256='2fe91fa6040b9417fd472cd6dca902d4a6353618f22c1a482f521ef4d7bc3b85')
DD_NODE_READER=('READONLY_GLOBAL_DD_REFINEMENT_SAVED_RESULT_AUDIT_V002_RESULT.json','1a3aab2739b4043e9982bf91149d6bc49716e20d9214082fb977aaae1bb95532')
def dd_node_selected_record(rec,mapping):
 assert set(rec)=={'file','sha256','commit_file','commit_sha256','metadata'}
 for name,key in (('file','sha256'),('commit_file','commit_sha256')):
  mapkey=rec[name] if rec[name] in mapping else str(path(rec[name]).resolve());assert mapping[mapkey]==rec[key];bind(rec[name],rec[key])
 assert json.loads(path(rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
 return rec

def dd_node_schema(rec,fields):
 schema=rec['metadata']['schema']
 for key,shape in fields.items():assert schema[key]==dict(shape=shape,dtype='float64',finite=True),(rec['file'],key)

def dd_node_admission():
 t=DD_NODE_TERMINAL;assert all(v is not None for v in t.values()),'Actual CLOSED parent and saved-reader PASS required'
 for n,h in ((DD_NODE_PARENT+'_RESULT.json',t['result_sha256']),(DD_NODE_PARENT+'_RECEIPT.json',t['receipt_sha256']),('cross_u_canonical_nodal_metric_rate_dd_refinement_v001.py',t['source_sha256']),(DD_NODE_PARENT+'.md',t['protocol_sha256']),DD_NODE_READER):bind(n,h)
 result=json.loads(path(DD_NODE_PARENT+'_RESULT.json').read_text());receipt=json.loads(path(DD_NODE_PARENT+'_RECEIPT.json').read_text());reader=json.loads(path(DD_NODE_READER[0]).read_text())
 assert receipt['status']=='CLOSED' and receipt['error_sha256'] is None and receipt['result_sha256']==t['result_sha256']
 assert result['owner']==receipt['owner'] and result['owner']['owner']=='root' and result['owner']['pid']==t['pid'] and result['owner']['source_sha256']==t['source_sha256'] and receipt['closed']>result['owner']['started']
 assert result['status']==result['case']['status']=='ORIGINAL_CANONICAL_ROWS_NOT_ADMITTED' and result['case']['rate_jets'] is None and result['case']['trace_preparation'] is None
 assert result['case']['parent_nonadmission_preserved'] is True and result['case']['physical_adoption'] is False and result['case']['no_extra_iteration_cap'] is True
 assert result['qualification']==receipt['qualification'] and all(x is False for x in result['qualification'].values())
 assert reader['status']=='SAVED_GLOBAL_DD_REFINEMENT_AUDIT_PASS' and reader['pid']==46047 and reader['parent_terminal']==t and reader['controls']==13 and reader['committed_pairs']==20
 assert reader['original_canonical_and_trace_admitted'] is False and reader['qualification']==result['qualification'] and reader['DD_EFT_FE_operator_or_solver_replayed'] is False and reader['new_field_or_history_adopted'] is False
 records=result['checkpoints'];assert len(records)==20 and len(result['controls'])==13 and all(c['passed'] for c in result['controls'])
 assert [c['cycle'] for c in result['case']['compatibility_corrections']]==[1,2,3]
 def one(kind,cycle=None):
  selected=[r for r in records if r['metadata']['kind']==kind and (cycle is None or r['metadata'].get('cycle')==cycle)];assert len(selected)==1;return selected[0]
 inherited=one('inherited_closed_DD_and_geometry_proofs_and_selected_frozen_system')
 parent_records=dict(solution=result['case']['compatibility'],correction=one('bounded_float_MINRES_correction_with_DD_original_certificate',3),recovered=one('exact_frozen_x1080_rhs_targets_and_rounded_affine_offsets'),initial=one('new_accurate_original_action_on_unadmitted_x1080'))
 assert parent_records['solution'] in records and parent_records['solution']['metadata']['kind']=='actual_canonical_compatibility_test_with_DD_original_certificate' and parent_records['solution']['metadata']['canonical_and_trace_admitted'] is False
 assert parent_records['correction']['metadata']['cap']==160
 system_records=inherited['metadata']['records'];assert set(system_records)=={'solution','basis','coefficient','affine','0','1','2','3'} and system_records==parent_records['recovered']['metadata']['records']
 mapping=dict(receipt['input_sha256'])
 for name,h in receipt['output_sha256'].items():assert name not in mapping or mapping[name]==h;mapping[name]=h
 assert mapping[str(path(DD_NODE_PARENT+'.md').resolve())]==t['protocol_sha256']
 for rec in parent_records.values():dd_node_selected_record(rec,receipt['output_sha256'])
 for rec in system_records.values():dd_node_selected_record(rec,mapping)
 dd_node_schema(parent_records['solution'],dict(native_nodal_rate=[33,3,87,45],metric_nodal_rate=[6,87,45],original_rhs=[403340],original_action_hi=[403340],original_action_lo=[403340],original_residual_hi=[403340],original_residual_lo=[403340]))
 dd_node_schema(parent_records['correction'],dict(cycle_003_final_update_actual_binary64_nodes=[403340],cycle_003_final_update_exact_update_minus_actual_nodes=[403340]))
 dd_node_schema(parent_records['recovered'],dict(original_rhs=[403340],rounded_global_cn=[33,3,87,45],rounded_global_cm=[6,87,45],current_Pn=[33,3,87,45],current_Pm=[6,87,45]))
 dd_node_schema(parent_records['initial'],{name:[403340] for name in ('original_rhs64_minus_exact_saved_target_offset_hi','original_rhs64_minus_exact_saved_target_offset_lo','saved_residual_minus_DD_original_residual_hi','saved_residual_minus_DD_original_residual_lo')})
 proof=dict(parent_terminal=t,parent_status=result['status'],saved_reader_ref=dict(file=DD_NODE_READER[0],sha256=DD_NODE_READER[1]),parent_result_ref=dict(file=DD_NODE_PARENT+'_RESULT.json',sha256=t['result_sha256']),parent_receipt_ref=dict(file=DD_NODE_PARENT+'_RECEIPT.json',sha256=t['receipt_sha256']),high_low_roles=dict(high='packed final SOLUTION native_nodal_rate/metric_nodal_rate',low='CORRECTION cycle_003_final_update_exact_update_minus_actual_nodes',last_actual_nodes='cycle_003_final_update_actual_binary64_nodes'),high_equals_last_actual_nodes_earned_by_saved_reader=True,original_nonadmission_preserved=True,physical_state_or_rate_adopted=False)
 return INPUTS.copy(),system_records,parent_records,proof

"""Definitions only: three new DD-node/update/division controls; no evaluation.
No original geometry, physical fields, block actions or earned fixtures are replayed.
Caller supplies np, Decimal, localcontext, CHECKS, capture, check, dd_node_update,
and a_div64. ROOT alone evaluates an admitted containing producer.
"""

def fresh_dd_node_coordinate_fixtures():
 start=len(CHECKS)
 hi=np.array([2.**60]);lo=np.array([1.]);delta=np.array([-2.**60])
 capture('fresh_dd_nodes_cancellation_input_hi',hi);capture('fresh_dd_nodes_cancellation_input_lo',lo);capture('fresh_dd_nodes_cancellation_delta',delta)
 pair,defect=dd_node_update((hi,lo),delta,capture,'fresh_dd_nodes_cancellation')
 actual=np.stack((pair[0],pair[1],defect));expected=np.array([[1.],[0.],[0.]])
 capture('fresh_dd_nodes_cancellation_actual',actual);capture('fresh_dd_nodes_cancellation_expected',expected)
 check('fresh_DD_node_high_cancellation_retains_old_low_word',actual,expected,abs(actual)+abs(expected))
 hi=np.array([2.**60]);lo=np.array([1.]);delta=np.array([2.**-60])
 capture('fresh_dd_nodes_compression_input_hi',hi);capture('fresh_dd_nodes_compression_input_lo',lo);capture('fresh_dd_nodes_compression_delta',delta)
 pair,defect=dd_node_update((hi,lo),delta,capture,'fresh_dd_nodes_compression')
 actual=np.stack((pair[0],pair[1],defect));expected=np.array([[2.**60],[1.],[2.**-60]])
 capture('fresh_dd_nodes_compression_actual',actual);capture('fresh_dd_nodes_compression_expected',expected)
 check('fresh_DD_node_exact_update_minus_new_pair_has_positive_third_word',actual,expected,abs(actual)+abs(expected))
 retained={}
 def division_capture(name,array):
  retained[name]=array;capture(name,array)
 label='fresh_dd_nodes_division'
 quotient=a_div64((np.ones(1),np.zeros(1)),np.array([3.]),division_capture,label)
 expected_words=np.array([[float.fromhex('0x1.5555555555555p-2')],[float.fromhex('0x1.5555555555555p-56')]])
 words=np.stack(quotient);remainder=np.stack((retained[label+'_division_defect_hi'],retained[label+'_division_defect_lo']))
 expected_remainder=np.array([[2.**-108],[0.]])
 capture(label+'_actual_quotient_words',words);capture(label+'_expected_quotient_words',expected_words)
 capture(label+'_actual_remainder_words',remainder);capture(label+'_expected_remainder_words',expected_remainder)
 with localcontext() as ctx:
  ctx.prec=100
  actual=Decimal.from_float(float(quotient[0][0]))+Decimal.from_float(float(quotient[1][0]))
  expected=Decimal(1)/Decimal(3);error=abs(actual-expected)/abs(expected)
 word_exact=bool(np.array_equal(words,expected_words));remainder_exact=bool(np.array_equal(remainder,expected_remainder))
 rec=dict(ordinal=len(CHECKS),name='fresh_DD_division_one_third_precision_and_disclosed_nonzero_defect',error=str(error),tolerance='1e-30',passed=bool(error<=Decimal('1e-30') and word_exact and remainder_exact),actual=str(actual),expected=str(expected),expected_quotient_words_hex=[float(v).hex() for v in expected_words[:,0]],actual_quotient_words_hex=[float(v).hex() for v in words[:,0]],expected_remainder_words_hex=[float(v).hex() for v in expected_remainder[:,0]],actual_remainder_words_hex=[float(v).hex() for v in remainder[:,0]],quotient_words_exact=word_exact,remainder_words_exact=remainder_exact,defect_normalized_by_own_tiny_magnitude=False,defect_convention='numerator minus original denominator times returned two-word quotient')
 CHECKS.append(rec);assert rec['passed'],rec
 assert len(CHECKS)-start==3
 return dict(kind='three_fresh_DD_node_update_and_non_dyadic_division_controls',controls=CHECKS[start:],exact_update_convention='old_hi+old_lo+delta=new_hi+new_lo+third_word',division_defect='1-3*q=2^-108',physical_state_evaluation=False)

PINS={'author_fragment_dd_nodal_coordinates_v001.py':'8ab3af96ab28b2f4cb6eed4039933e3def0c0ad9ceb1de643a07dea015c38eae','author_fragment_dd_node_admission_v002.txt':'a775cddd4719b8a23026e32ccaca4afe8dd6cd604c49c2151360ac9786523ec6','author_fragment_dd_nodal_coordinate_fixtures_v001.txt':'510f7242f187201f3d1178fa8447b32e0d93a2a8eebe44d4ce795ab15fc5620b'}
def main():
 global np,OWNER,RAW,AVAILABLE
 ap=argparse.ArgumentParser();ap.add_argument('--root-run',action='store_true');args=ap.parse_args()
 assert args.root_run and not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and PROTOCOL_SHA,'Guarded definitions; ROOT owns execution'
 assert sha(path(STEM+'.md'))==PROTOCOL_SHA and not list(BASE.glob(STEM+'_*'))
 OWNER=dict(owner='root',pid=os.getpid(),started=now(),source_sha256=sha(__file__),scope='same saved sigma1 frozen canonical system, explicit two-word nodal-coordinate precision test')
 try:
  json_file(STEM+'_OWNER_START.json',OWNER);bind(STEM+'.md',PROTOCOL_SHA)
  for n,h in PINS.items():bind(n,h)
  pins,system,parent,proof=dd_node_admission()
  manifest=dict(owner=OWNER,input_sha256=INPUTS.copy(),system_records=system,parent_records=parent,proof=proof,configuration=dict(sigma=1.,real_FE_coordinates=403340,precision='two explicit binary64 words per unchanged real coordinate',linear_tolerance=LINEAR_TOL,arithmetic_tolerance=TOL,correction_cycle_cap=MAX_CYCLES,correction_iteration_cap=CAP,recurrence='unchanged binary64 coupled_action with unrounded two-word original certificate',initial_candidate='final authenticated45073 high plus cycle3 last discarded update low',metric_evaluator='retained Fhat64',metric_scatter='F64 then weight64 then hat64',original_rhs_changed=False,coefficient_or_source_changed=False),qualification=FLAGS)
  json_file(STEM+'_MANIFEST.json',manifest)
  import numpy as np_local
  np=np_local
  checkpoint('INPUT',{},dict(kind='inherited_closed_float_node_nonadmission_and_saved_reader_with_frozen_system',system_records=system,parent_records=parent,proof=proof))
  fixtures=fresh_dd_node_coordinate_fixtures();checkpoint('FIXTURE',dict(RAW,**AVAILABLE),fixtures);RAW={};AVAILABLE={}
  seed,rhs,b,d,g,affine,scales,seed_record=load_dd_node_seed(system,parent,proof);RAW={};AVAILABLE={}
  current,action,residual,ratios,tr,admitted,cycles=measure_dd_node_candidate(seed,rhs,b,d,g,affine,scales)
  assert len(CHECKS)==3+len(cycles) and all(q['passed'] for q in CHECKS)
  solution,jets=save_dd_node_solution(current,action,residual,ratios,tr,admitted,cycles,rhs,affine,g,system,parent)
  status='CURRENT_CANONICAL_AND_WEAK_CMC_COMPATIBLE' if admitted else 'ORIGINAL_CANONICAL_ROWS_NOT_ADMITTED'
  case=dict(status=status,compatibility=solution,trace_preparation=None,rate_jets=jets,compatibility_corrections=cycles,seed=seed_record,parent_nonadmission_preserved=True,no_extra_iteration_cap=True,precision='two_word_nodal_coordinates',targets_unchanged=True,physical_adoption=False)
  recheck();rh=json_file(STEM+'_RESULT.json',dict(owner=OWNER,status=status,case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));recheck()
  json_file(STEM+'_RECEIPT.json',dict(owner=OWNER,status='CLOSED',closed=now(),input_sha256=INPUTS.copy(),output_sha256=OUTPUTS.copy(),result_sha256=rh,error_sha256=None,qualification=FLAGS));recheck();print(status,len(CHECKS),len(RECORDS))
  return 0 if admitted else 3
 except BaseException:
  failure=traceback.format_exc();raw_error=None;closing_error=None
  try:
   for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items():AVAILABLE['current_EFT_'+n]=a.copy()
   if RAW or AVAILABLE:checkpoint('ERROR_RAW',dict(RAW,**AVAILABLE),dict(kind='completed_original_operands_two_word_nodes_actions_and_current_iterate',context=dict(CONTEXT),controls=CHECKS,EFT_operation=DD_ARRAY_CURRENT.get('operation')),failed=True)
  except BaseException:raw_error=traceback.format_exc()
  try:seal_actual();recheck(False)
  except BaseException:closing_error=traceback.format_exc()
  prior=sha(path(STEM+'_RECEIPT.json')) if path(STEM+'_RECEIPT.json').exists() else None
  eh=json_file(STEM+'_ERROR.json',dict(owner=OWNER,status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=closing_error,prior_receipt_sha256=prior,controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS.copy(),preserved_outputs=OUTPUTS.copy(),qualification=FLAGS))
  json_file(STEM+('_ERROR_RECEIPT.json' if prior is not None else '_RECEIPT.json'),dict(owner=OWNER,status='CLOSED_ERROR',closed=now(),input_sha256=INPUTS.copy(),output_sha256=OUTPUTS.copy(),result_sha256=None,error_sha256=eh,prior_receipt_sha256=prior,qualification=FLAGS));seal_actual()
  return 1
if __name__=='__main__':raise SystemExit(main())

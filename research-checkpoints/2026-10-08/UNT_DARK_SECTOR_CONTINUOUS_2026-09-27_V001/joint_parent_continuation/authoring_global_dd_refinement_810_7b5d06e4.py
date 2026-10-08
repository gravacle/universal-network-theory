"""Guarded original frozen FE action in DD and bounded residual correction. ROOT only."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal,localcontext
import argparse,hashlib,json,math,os,sys,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_CANONICAL_NODAL_METRIC_RATE_DD_REFINEMENT_V001'
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=True
PROTOCOL_SHA=None
BAND='CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001'
MAX_CYCLES=3;CAP=160;LINEAR_TOL=1e-10;TOL=2e-11
np=None;OWNER=None;INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];RAW={};AVAILABLE={};CONTEXT={}
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


"""Definitions-only global DD adapter. ROOT injects np and admits saved operands.
No runner, input loading, recurrence, cap, state adoption or physical assumption.
The scalar selected component must PASS before any owner executes this adapter.
"""
np=None
DD_ARRAY_CURRENT={}

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


# Private definitions only. Caller supplies json, path, sha, bind and INPUTS.
# Original159 PARENTS/admitted are literal; only selected old records are hashed.
PARENTS=(('CROSS_U_CANONICAL_NODAL_METRIC_RATE_SOLVE_V002',41181,'6759a9c44574bfd75865d1867c4467df18deca79a162979b89f1546ba9e417b7','2b6603b36ef3596c419d76e2ce82ac9c50dae31d150fb850f2d4179a56e3ff70'),('CROSS_U_CANONICAL_NODAL_METRIC_RATE_SOLVE_V001',39611,'efffd53fc12abd68daf723a418de8c58b05374e5ad117c260ad2cbde73fbae82','8f306769022830cb0762e735308f493b072b58320fbdffabf46898c5a180f473'),('CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001',28469,'e5a8f065a865245a430a2b23fe1c69a20ae2dd542071e5804a216f2f604f8fe5','00478e51c5ae07c31707ca8ec548bef193d33b2f76dc4b09361efd6e281727ae'))

def admitted():
 docs=[];maps={}
 for st,pid,rh,ch in PARENTS:
  bind(st+'_RESULT.json',rh);bind(st+'_RECEIPT.json',ch)
  r=json.loads(path(st+'_RESULT.json').read_text());rc=json.loads(path(st+'_RECEIPT.json').read_text())
  assert rc['status']=='CLOSED' and rc['owner']==r['owner'] and r['owner']['pid']==pid and r['owner']['owner']=='root'
  assert rc['result_sha256']==rh and rc.get('error_sha256') is None and rc['closed']>rc['owner']['started']
  assert all(c['passed'] for c in r['controls']) and all(v is False for v in r['qualification'].values())
  for mapping in (rc['input_sha256'],rc['output_sha256']):
   for n,h in mapping.items():
    key=str(path(n).resolve());assert key not in maps or maps[key]==h;maps[key]=h
  docs.append(r)
 current,old,weak=docs
 assert current['status']==old['status']=='ORIGINAL_CANONICAL_ROWS_NOT_ADMITTED'
 assert len(current['controls'])==21 and len(current['checkpoints'])==19 and len(old['controls'])==17 and len(old['checkpoints'])==25
 assert current['case']['trace_preparation'] is None and current['case']['parent_nonadmission_preserved'] is True
 assert current['owner']['source_sha256']=='f662ade49c204ba116049fa7de6b303575ef219dc8dd6313df5c3fbd453b6ea0'
 bind('cross_u_canonical_nodal_metric_rate_solve_v002.py',current['owner']['source_sha256'])
 bind(PARENTS[0][0]+'.md','0128d1613b8f43f8dce40ed5cb2c5a72b974104da3e838deff6cfec4345b0465')
 def unique(r,kind):
  q=[x for x in r['checkpoints'] if x['metadata']['kind']==kind];assert len(q)==1;return q[0]
 records=dict(solution=current['case']['compatibility'],basis=unique(old,'unchanged_E_F_S_bases_and_positive_solver_congruences'),coefficient=unique(weak,'complete_fixed_metric_native99_mass_coefficients'))
 cols=[q for q in old['checkpoints'] if q['metadata']['kind']=='copied_signed_blocks_and_current_actual_affine_reference']
 assert len(cols)==4 and [q['metadata']['column'] for q in cols]==list(range(4));records.update({str(i):q for i,q in enumerate(cols)})
 for rec in records.values():
  for key in ('file','commit_file'):assert maps[str(path(rec[key]).resolve())]==rec['sha256' if key=='file' else 'commit_sha256'];bind(rec[key],rec['sha256' if key=='file' else 'commit_sha256'])
  assert json.loads(path(rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
 return records,dict(parent_nonadmission_preserved=True,parent_map_authority='hashed CLOSED receipts; only selected immutable files rehashed',old_controls=current['controls'],old_qualification=current['qualification'])

GLOBAL_DD_PROOF_STEM='CROSS_U_SELECTED_NATIVE_FE_DOUBLE_DOUBLE_V001'
GLOBAL_DD_PROOF_SOURCE_SHA='1a1658c897765a265a7788906588b4d41bd02ef5af1a3dc24ebe89f125b720a1'
GLOBAL_DD_PROOF_PROTOCOL_SHA='8689dc0cbd7c4ce711359d731bb7050f9959d4e960090c50269fdf2db43599c0'
GLOBAL_DD_PROOF_RESULT_SHA='0c67ed1ead3fa33832a83eabd7f5527116b33bf645335e305ff5013be5e22c30'
GLOBAL_DD_PROOF_RECEIPT_SHA='e0e3add13fa0e153a766b87e446924e83b7e18ce6a137334a6bf458489b95d6d'
GLOBAL_DD_READER_FILE='READONLY_SELECTED_NATIVE_FE_DOUBLE_DOUBLE_V001_AUDIT_RESULT.json'
GLOBAL_DD_READER_SHA='be8850340dcde4edd6fbcd1fad4f937aaff9887f5d18af6b3e7172778fe64633'

def global_dd_schema(record,shapes,integer=()):
 schema=record['metadata']['schema']
 for n,s in shapes.items():
  assert schema[n]['shape']==list(s) and schema[n]['dtype']==('int64' if n in integer else 'float64') and schema[n]['finite'] is True,(record['file'],n)

def admission():
 # Closed proof/reader gates precede original selected-file I/O; no old replay.
 st=GLOBAL_DD_PROOF_STEM
 for n,h in ((st+'_RESULT.json',GLOBAL_DD_PROOF_RESULT_SHA),(st+'_RECEIPT.json',GLOBAL_DD_PROOF_RECEIPT_SHA),('cross_u_selected_native_fe_double_double_v001.py',GLOBAL_DD_PROOF_SOURCE_SHA),(st+'.md',GLOBAL_DD_PROOF_PROTOCOL_SHA),(GLOBAL_DD_READER_FILE,GLOBAL_DD_READER_SHA)):bind(n,h)
 proof=json.loads(path(st+'_RESULT.json').read_text());receipt=json.loads(path(st+'_RECEIPT.json').read_text());reader=json.loads(path(GLOBAL_DD_READER_FILE).read_text())
 assert receipt['status']=='CLOSED' and receipt['owner']==proof['owner'] and proof['owner']['owner']=='root' and proof['owner']['pid']==43274 and proof['owner']['source_sha256']==GLOBAL_DD_PROOF_SOURCE_SHA
 assert receipt['closed']>proof['owner']['started'] and receipt['result_sha256']==GLOBAL_DD_PROOF_RESULT_SHA and receipt['error_sha256'] is None
 assert proof['status']=='BOUNDED_DOUBLE_DOUBLE_COMPONENT_COMPLETE' and len(proof['controls'])==15 and all(q['passed'] for q in proof['controls']) and len(proof['rows'])==2
 assert proof['qualification']==receipt['qualification'] and all(q is False for q in proof['qualification'].values()) and proof['full_row_admission'] is proof['new_operator_solve'] is proof['source_or_coefficient_change'] is proof['original_rhs_changed'] is False
 assert reader['status']=='SAVED_DD_COMPONENT_AUDIT_PASS' and reader['pid']==43547 and reader['controls']==15 and reader['counts']['accuracy_controls']==8 and reader['counts']['exact_fixture_controls']==7
 assert reader['parent_status']=='CLOSED' and reader['parent_terminal']==dict(pid=43274,source_sha256=GLOBAL_DD_PROOF_SOURCE_SHA,protocol_sha256=GLOBAL_DD_PROOF_PROTOCOL_SHA,result_sha256=GLOBAL_DD_PROOF_RESULT_SHA,receipt_sha256=GLOBAL_DD_PROOF_RECEIPT_SHA,error_sha256=None)
 assert reader['qualification']==proof['qualification'] and reader['full_vector_admission'] is reader['EFT_FE_operator_or_solve_replayed'] is False
 records,ancestry=admitted()
 old=json.loads(path(PARENTS[1][0]+'_RESULT.json').read_text());current=json.loads(path(PARENTS[0][0]+'_RESULT.json').read_text());rc=json.loads(path(PARENTS[1][0]+'_RECEIPT.json').read_text())
 affine=[q for q in old['checkpoints'] if q['metadata']['kind']=='actual_current_weak_targets_and_owned_H_trace_rhs'];assert len(affine)==1;affine=affine[0]
 for key in ('file','commit_file'):
  n=affine[key];h=affine['sha256' if key=='file' else 'commit_sha256']
  assert rc['output_sha256'][n]==h;bind(n,h)
 assert json.loads(path(affine['commit_file']).read_text())=={k:v for k,v in affine.items() if k not in ('commit_file','commit_sha256')};records['affine']=affine
 recovered=[q for q in current['checkpoints'] if q['metadata']['kind']=='exact_saved_600_iterate_original_targets_and_rows'];assert len(recovered)==1
 meta=recovered[0]['metadata'];mini=lambda q:{k:q[k] for k in ('file','sha256','commit_file','commit_sha256')}
 assert meta['basis_ref']==records['basis'] and meta['affine_ref']==affine and meta['native_mass_ref']==mini(records['coefficient']) and meta['column_refs']==[mini(records[str(i)]) for i in range(4)]
 global_dd_schema(records['solution'],dict(native_nodal_rate=(33,3,87,45),metric_nodal_rate=(6,87,45),compatibility_cycle_003_original_rhs=(403340,),compatibility_original_residual=(403340,),compatibility_original_action=(403340,),current_Pn=(33,3,87,45),current_Pm=(6,87,45),trace_rhs=(87,45)))
 global_dd_schema(records['basis'],dict(R=(4,3784),dv=(4,3784),hats=(4,4,3,86,44),cell_i=(3784,),cell_j=(3784,),native_scale=(33,3,87,45),metric_scale=(6,87,45),scalar_scale=(87,45),r=(87,),z=(45,)),('cell_i','cell_j'))
 global_dd_schema(records['coefficient'],dict(mixing_L=(32,15136,3,3),modal_D=(32,15136,3,3),Maxwell_M0=(15136,3,3),operation_eL=(32,15136,3,3),operation_eD=(32,15136,3,3),operation_eM0=(15136,3,3)))
 column_shapes=dict(B=(3784,99,6),T=(3784,6,6),cn=(3784,99),cm=(3784,6),pstar=(3784,99),pistar=(3784,6),vstar=(3784,99),kstar=(3784,6),ih=(3784,3,3),N=(3784,),mu=(3784,),Kstar=(3784,),lie=(3784,3,3),eB=(3784,99,6),eT=(3784,6,6))
 for i in range(4):assert records[str(i)]['metadata']['column']==i;global_dd_schema(records[str(i)],column_shapes)
 global_dd_schema(affine,dict(Pn=(33,3,87,45),Pm=(6,87,45),cn=(33,3,87,45),cm=(6,87,45),trace_rhs=(87,45)))
 assert [q['selection']['group'] for q in proof['rows']]==[10,14]
 proof=dict(result=proof,result_ref=dict(file=st+'_RESULT.json',sha256=GLOBAL_DD_PROOF_RESULT_SHA),receipt_ref=dict(file=st+'_RECEIPT.json',sha256=GLOBAL_DD_PROOF_RECEIPT_SHA),reader_ref=dict(file=GLOBAL_DD_READER_FILE,sha256=GLOBAL_DD_READER_SHA,status=reader['status']),original_ancestry=ancestry,authority='Three hashed CLOSED original receipts; eight selected immutable NPZ/COMMIT pairs rehashed. No complete ancestral map traversal, feature/kinetic-law or prior solver replay.',original_rows_admitted=False,global_precision_admission=False,physical_rate_adoption=False)
 return INPUTS.copy(),records,proof


def bind(n,h):
 key=str(path(n).resolve());assert key not in INPUTS or INPUTS[key]==h
 assert sha(path(n))==h,n;INPUTS[key]=h
def collapse(pair,label):
 value=pair[0]+pair[1];capture(label+'_hi',pair[0]);capture(label+'_lo',pair[1]);capture(label+'_rounded_value',value)
 assert np.all(np.isfinite(value));return value
def pack_dd(n,m):return pack_fields(n[0],m[0]),pack_fields(n[1],m[1])
def scaled_norm_ratios(pair,reference,scale,label):
 value=collapse(pair,label);return original_ratios(value,reference,scale)
# Private definitions only. ROOT evaluates these fresh artificial fixtures.
# Requires np, a_sum/a_prod/a_dd/a_add/a_sub/a_mul/a_matvec/a_slice,
# dd_point_coupled, capture, check(label,actual,expected,envelope), CHECKS.
# Six new gates; all32 modes, group-major99 and signed sixmetric order retained.

def fresh_global_dd_fixtures():
 start=len(CHECKS)
 # Broadcasting two signed high words across three independent low components.
 x=np.array([2.**60,-2.**60])[:,None];y=np.array([1.,-1.,2.**-60])[None,:]
 capture('fresh_array_sum_x',x);capture('fresh_array_sum_y',y)
 high,low=a_sum(x,y);capture('fresh_array_sum_hi',high);capture('fresh_array_sum_lo',low)
 expected=np.stack((np.broadcast_to(x,(2,3)),np.broadcast_to(y,(2,3))))
 actual=np.stack((high,low));capture('fresh_array_sum_expected',expected)
 check('fresh_array_two_sum_three_component_broadcast',actual,expected,abs(actual)+abs(expected))
 # Product low words survive positive/negative high-word products and broadcasting.
 x=np.array([2.**53+2.,-(2.**53+2.)])[:,None];y=np.array([1.-2.**-52,1.,1.+2.**-52])[None,:]
 capture('fresh_array_product_x',x);capture('fresh_array_product_y',y)
 high,low=a_prod(x,y);capture('fresh_array_product_hi',high);capture('fresh_array_product_lo',low)
 expected_high=np.array([[2.**53,2.**53+2.,2.**53+4.],[-2.**53,-(2.**53+2.),-(2.**53+4.)]])
 expected_low=np.array([[-2.**-51,0.,2.**-51],[2.**-51,0.,-2.**-51]])
 expected=np.stack((expected_high,expected_low));actual=np.stack((high,low));capture('fresh_array_product_expected',expected)
 check('fresh_array_Dekker_product_low_three_component_broadcast',actual,expected,abs(actual)+abs(expected))
 # All four DD products: the two cross terms cancel, leaving low-low products.
 left=(np.full(3,2.**60),np.array([1.,-1.,2.]));right=(np.ones(3),np.array([-2.**-60,2.**-60,-2.**-59]))
 capture('fresh_array_four_product_left_hi',left[0]);capture('fresh_array_four_product_left_lo',left[1]);capture('fresh_array_four_product_right_hi',right[0]);capture('fresh_array_four_product_right_lo',right[1])
 product=a_mul(left,right);capture('fresh_array_four_product_hi',product[0]);capture('fresh_array_four_product_lo',product[1])
 remainder=a_sub(product,a_dd(np.full(3,2.**60)));capture('fresh_array_four_product_remainder_hi',remainder[0]);capture('fresh_array_four_product_remainder_lo',remainder[1])
 expected=np.stack((np.array([-2.**-60,-2.**-60,-2.**-58]),np.zeros(3)));actual=np.stack(remainder);capture('fresh_array_four_product_expected',expected)
 check('fresh_array_all_four_DD_products_after_high_cancellation',actual,expected,abs(actual)+abs(expected))
 # One point, all32 modes. No actual galaxy field/state/omega is selected.
 v=np.zeros((33,1,3));v[0,0]=[2.,-4.,8.]
 for j in range(1,33):v[j,0]=[j/32.,j/16.,-j/8.]
 k=np.array([[2.,-1.,4.,-2.,1.,-1.]])
 capture('fresh_block_native_group_major99_input',v);capture('fresh_block_metric_six_input',k)
 L=np.broadcast_to(np.diag([.5,-.25,.125]),(32,1,3,3)).copy();D=np.broadcast_to(np.eye(3)/32.,(32,1,3,3)).copy();M0=np.diag([2.,3.,4.])[None]
 capture('fresh_block_L',L);capture('fresh_block_D',D);capture('fresh_block_Maxwell_M0',M0)
 B=np.zeros((1,99,6));B[0,:3,:3]=np.diag([.5,-.5,-.125]);B[0,0,3]=1.;B[0,1,4]=-2.;B[0,2,5]=3.
 for j in range(32):B[0,3+3*j:6+3*j,:3]=np.diag([1.,2.,-1.])/32.
 capture('fresh_block_supplied_Bu_and_Bz',B)
 T=np.diag([-2.,1.,2.,-1.,.5,-.25])[None];T[0,0,3]=T[0,3,0]=.5;capture('fresh_block_signed_T',T)
 n,m=dd_point_coupled(a_dd(v),a_dd(k),dict(M0=M0,L=L,D=D),dict(B=B,T=T),capture)
 capture('fresh_block_native_answer_hi',n[0]);capture('fresh_block_native_answer_lo',n[1]);capture('fresh_block_metric_answer_hi',m[0]);capture('fresh_block_metric_answer_lo',m[1])
 expected_native=np.zeros((33,1,3));expected_native[0,0]=[481./128.,-1793./128.,3631./128.]
 for j in range(1,33):expected_native[j,0]=[(j+96.)/1024.,(j-16.)/512.,-(j+24.)/256.]
 expected=np.stack((expected_native,np.zeros_like(expected_native)));actual=np.stack(n);capture('fresh_block_independent_native99_expected',expected)
 check('fresh_all32_modes_and_supplied_Bu_native99_dyadic_answer',actual,expected,abs(actual)+abs(expected))
 expected_metric=np.array([[-223./64.,49./16.,145./16.,5.,17./2.,97./4.]])
 expected=np.stack((expected_metric,np.zeros_like(expected_metric)));actual=np.stack(m);capture('fresh_block_independent_signed_metric6_expected',expected)
 check('fresh_B_transpose_native99_and_signed_T_metric6_answer',actual,expected,abs(actual)+abs(expected))
 # Completing U from the FULL mode output incorrectly substitutes sum(L^T Bz) for Bu.
 # Here C=Bu-sum(L^T Bz) has C03=1,C14=-2,C25=3, so Ck=(-2,-2,-3).
 completed=a_matvec(M0,a_dd(v[0]));capture('fresh_wrong_completion_initial_hi',completed[0]);capture('fresh_wrong_completion_initial_lo',completed[1])
 for j in range(32):
  completed=a_add(completed,a_matvec(L[j].swapaxes(-1,-2),a_slice(n,j+1)))
  capture('fresh_wrong_completion_through_mode%d_hi'%j,completed[0]);capture('fresh_wrong_completion_through_mode%d_lo'%j,completed[1])
 missing=a_sub(a_slice(n,0),completed);capture('fresh_retained_nonzero_Ck_hi',missing[0]);capture('fresh_retained_nonzero_Ck_lo',missing[1])
 expected=np.stack((np.array([[-2.,-2.,-3.]]),np.zeros((1,3))));actual=np.stack(missing);capture('fresh_retained_Ck_expected',expected)
 check('fresh_nonzero_Bu_minus_sum_L_transpose_Bz_cannot_be_completed_away',actual,expected,abs(actual)+abs(expected))
 assert len(CHECKS)-start==6
 return dict(kind='six_fresh_array_EFT_and_full32_native99_signed_metric6_controls',controls=CHECKS[start:],point_count=1,all32_modes=True,missing_completion_Ck=[-2.,-2.,-3.],actual_field_or_state_evaluation=False)


def selected_row_accuracy(action,rhs,rows,references):
 n=unpack_fields(action[0],False)[0];nl=unpack_fields(action[1],False)[0]
 for row in rows:
  group,component=row['group'],row['component'];i,j=row['node'];value=(n[group,component,i,j],nl[group,component,i,j]);res=a_sub(a_dd(np.array(row['original_rhs'])),(np.array(value[0]),np.array(value[1])))
  for name,pair,reference in (('action',value,references[str(group)]['action']),('original_residual',res,references[str(group)]['original_rhs_residual'])):
   with localcontext() as ctx:
    ctx.prec=100;actual=Decimal.from_float(float(pair[0]))+Decimal.from_float(float(pair[1]));expected=Decimal(reference);assert expected!=0
    error=abs(actual-expected)/abs(expected)
   ordinal=len(CHECKS);rec=dict(ordinal=ordinal,name='selected_row%d_array_%s_accuracy'%(group,name),error=str(error),tolerance='1e-10',passed=error<=Decimal('1e-10'),actual=str(actual),expected=str(expected))
   CHECKS.append(rec);assert rec['passed'],rec
def accurate_original_action(x,b,d,g,label):
 CONTEXT.update(active_action=label)
 v,k,_=unpack_fields(x,False);n,m=global_coupled_action_dd(v,k,b,d,g,capture);action=pack_dd(n,m)
 capture(label+'_action_hi',action[0]);capture(label+'_action_lo',action[1]);return action
def certify_current_dd(x,rhs,b,d,g,affine,scales,label):
 action=accurate_original_action(x,b,d,g,label);res=original_residual_dd(rhs,action)
 capture(label+'_residual_hi',res[0]);capture(label+'_residual_lo',res[1])
 rr=collapse(res,label+'_original_residual');fields=unpack_fields(rr,False);right=unpack_fields(rhs,False)
 actual_n,actual_m=unpack_fields(action[0],False)[:2];low_n,low_m=unpack_fields(action[1],False)[:2];ratios=[]
 for name,r,f,s,target,offset,act,low in zip(('native','metric'),fields[:2],right[:2],scales[:2],(affine['Pn'],affine['Pm']),(affine['cn'],affine['cm']),(actual_n,actual_m),(low_n,low_m)):
  ratio=original_ratios(r,f,s);capture(label+'_'+name+'_affine_ratios',ratio);ratios.append(ratio)
  actual_target_res=a_sub(a_dd(target),a_add(a_dd(offset),(act,low)))
  target_ratio=scaled_norm_ratios(actual_target_res,target,s,label+'_'+name+'_actual_target_residual')
  capture(label+'_'+name+'_actual_target_ratios',target_ratio);ratios.append(target_ratio)
 v,k,_=unpack_fields(x,False);trace=trace_forward(k,d,g);capture(label+'_weak_trace_action',trace)
 trace_res=trace-affine['trace_rhs'];capture(label+'_weak_trace_residual',trace_res)
 trace_ratios=original_ratios(trace_res,affine['trace_rhs'],scales[2]);capture(label+'_weak_trace_ratios',trace_ratios)
 return action,res,np.stack(ratios),trace_ratios
def original_field_bound(rhs,affine,scales):
 bounds=[]
 for value,scale in zip(unpack_fields(rhs,False)[:2],scales[:2]):
  raw=float(np.linalg.norm(value));white=float(np.linalg.norm(value/scale));assert math.isfinite(raw) and math.isfinite(white) and raw>0 and white>0
  bounds.extend((raw/float(np.max(scale)),white))
 for target,scale in zip((affine['Pn'],affine['Pm']),scales[:2]):
  raw=float(np.linalg.norm(target));white=float(np.linalg.norm(target/scale));assert math.isfinite(raw) and math.isfinite(white) and raw>0 and white>0
  bounds.extend((raw/float(np.max(scale)),white))
 return min(bounds)
def measure_and_correct(base,rhs,b,d,g,affine,scales,rows,references,saved):
 scale=pack_fields(scales[0],scales[1]);capture('positive_original_congruence',scale);assert np.all(scale>0) and np.all(np.isfinite(scale))
 action,res,ratios,tr=certify_current_dd(base,rhs,b,d,g,affine,scales,'initial')
 selected_row_accuracy(action,rhs,rows,references)
 epsilon=a_sub(a_dd(saved['compatibility_original_residual']),res);capture('saved_residual_minus_DD_original_residual_hi',epsilon[0]);capture('saved_residual_minus_DD_original_residual_lo',epsilon[1])
 old_action_gap=a_sub(a_dd(saved['compatibility_original_action']),action);capture('saved_action_minus_DD_original_action_hi',old_action_gap[0]);capture('saved_action_minus_DD_original_action_lo',old_action_gap[1])
 exact_rhs=a_sub(a_dd(pack_fields(affine['Pn'],affine['Pm'])),a_dd(pack_fields(affine['cn'],affine['cm'])))
 rhs_defect=a_sub(a_dd(rhs),exact_rhs);capture('original_rhs64_minus_exact_saved_target_offset_hi',rhs_defect[0]);capture('original_rhs64_minus_exact_saved_target_offset_lo',rhs_defect[1])
 checkpoint('INITIAL',dict(AVAILABLE),dict(kind='new_accurate_original_action_on_unadmitted_x1080',original_affine_ratios=ratios.tolist(),actual_weak_trace_ratios=tr.tolist(),qualification=False))
 current=base.copy();cycles=[]
 for cycle in range(1,MAX_CYCLES+1):
  if np.all(ratios<=LINEAR_TOL) and np.all(tr<=LINEAR_TOL):break
  label='cycle_%03d'%cycle;start=current.copy();base_action=action;base_res=res
  rhs_c=collapse(base_res,label+'_correction_rhs');rhs_defect=a_sub(base_res,a_dd(rhs_c));capture(label+'_correction_rhs_rounding_defect_hi',rhs_defect[0]);capture(label+'_correction_rhs_rounding_defect_lo',rhs_defect[1])
  wn=float(np.linalg.norm(rhs_c/scale));assert math.isfinite(wn) and wn>0
  tolerance=LINEAR_TOL*original_field_bound(rhs,affine,scales)/wn;capture(label+'_sufficient_white_tolerance',np.array(tolerance));assert math.isfinite(tolerance) and tolerance>0
  def float_action(delta):
   v,k,_=unpack_fields(delta,False);n,m=coupled_action(v,k,b,d,g);out=pack_fields(n,m);capture(label+'_latest_float_correction_action',out);assert np.all(np.isfinite(out));return out
  def certificate(delta):
   actual_nodes,low=rounded_node_update(start,delta,capture,label+'_update')
   a,r,ra,tra=certify_current_dd(actual_nodes,rhs,b,d,g,affine,scales,label)
   return collapse(r,label+'_certificate_residual'),np.concatenate((ra,tra[None]),axis=0)
  delta,callback_ratios,ok,reason=minres_core(float_action,rhs_c,scale,tolerance,certificate,label,cap=CAP)
  capture(label+'_completed_correction',delta);current,low=rounded_node_update(start,delta,capture,label+'_final_update')
  action,res,ratios,tr=certify_current_dd(current,rhs,b,d,g,affine,scales,label+'_final')
  delta_action=accurate_original_action(delta,b,d,g,label+'_accurate_delta')
  low_action=accurate_original_action(low,b,d,g,label+'_accurate_node_rounding')
  predicted=shifted_residual_with_update_defect(base_res,delta_action,low_action)
  gap=a_sub(res,predicted);capture(label+'_shifted_prediction_hi',predicted[0]);capture(label+'_shifted_prediction_lo',predicted[1]);capture(label+'_shifted_gap_hi',gap[0]);capture(label+'_shifted_gap_lo',gap[1])
  true=unpack_fields(collapse(res,label+'_new_true_residual'),False);old=unpack_fields(collapse(base_res,label+'_old_true_residual'),False);diff=unpack_fields(collapse(gap,label+'_update_identity_gap'),False)
  bound=2*abs(rhs);capture(label+'_update_uncancelled_rhs_bound',bound)
  for name,nodes in (('start',start),('new',current),('delta',delta),('node_low',low)):
   v,k,_=unpack_fields(nodes,False);en,em=coupled_envelope(v,k,b,d,g);capture(label+'_'+name+'_original_native_positive_bound',en);capture(label+'_'+name+'_original_metric_positive_bound',em)
   assert np.all(np.isfinite(en)) and np.all(np.isfinite(em)) and np.all(en>=0) and np.all(em>=0)
   bound=bound+pack_fields(en,em);capture(label+'_update_uncancelled_bound_through_'+name,bound)
  bound_fields=unpack_fields(bound,False)
  actual=np.array([np.linalg.norm(x) for x in diff[:2]]);env=np.array([np.linalg.norm(x) for x in bound_fields[:2]])
  capture(label+'_update_identity_actual_field_norms',actual);capture(label+'_update_identity_uncancelled_field_norm_bounds',env)
  capture(label+'_update_identity_postcancelled_residual_norms_diagnostic',np.array([[np.linalg.norm(a),np.linalg.norm(z)] for a,z in zip(true[:2],old[:2])]))
  assert np.all(np.isfinite(actual)) and np.all(np.isfinite(env)) and np.all(env>0)
  check(label+'_original_shifted_residual_with_actual_node_rounding',actual,np.zeros(2),env)
  cycles.append(dict(cycle=cycle,reason=reason,callback_admitted=bool(ok),original_affine_and_actual_target_ratios=ratios.tolist(),weak_trace_ratios=tr.tolist()))
  checkpoint('CORRECTION',{n:a for n,a in AVAILABLE.items() if n.startswith(label+'_')},dict(kind='bounded_float_MINRES_correction_with_DD_original_certificate',cycle=cycle,cap=CAP,original_rhs_changed=False,targets_changed=False,physical_adoption=False,controls=CHECKS[-1:]))
 admitted=bool(np.all(ratios<=LINEAR_TOL) and np.all(tr<=LINEAR_TOL))
 return current,action,res,ratios,tr,admitted,cycles

GEOMETRY_TERMINAL=dict(source_sha256='f2e257b3b32d78d8a908eefdd9f79456c4eb161111925338300ff59a67f51a63',protocol_sha256='c579b2ff765a4ab12ba83a3b7b242c978339949e27cce72eab421f97dbee91c7',result_sha256='49ff84580f00486f2c08d09c3944d63297d4094ca39b53e060282fb03d691896',receipt_sha256='71c06c2c094041a7295522509153d59df0d7c4f93c2459350e0a5dc6e1595769',pid=44342)
def recover_geometry_proof(records,proof):
 st='CROSS_U_SELECTED_GLOBAL_FE_GEOMETRY_BITS_V001';t=GEOMETRY_TERMINAL
 for n,h in ((st+'_RESULT.json',t['result_sha256']),(st+'_RECEIPT.json',t['receipt_sha256']),('cross_u_selected_global_fe_geometry_bits_v001.py',t['source_sha256']),(st+'.md',t['protocol_sha256'])):bind(n,h)
 result=json.loads(path(st+'_RESULT.json').read_text());receipt=json.loads(path(st+'_RECEIPT.json').read_text())
 assert receipt['status']=='CLOSED' and receipt['owner']==result['owner'] and result['owner']['owner']=='root' and result['owner']['pid']==t['pid'] and result['owner']['source_sha256']==t['source_sha256']
 assert receipt['closed']>result['owner']['started'] and receipt['result_sha256']==t['result_sha256'] and receipt['error_sha256'] is None
 assert result['status']=='GEOMETRY_BITS_MATCH' and result['controls']==[dict(compared_entries=5248,name='actual_array_geometry_matches_scalar_frozen_contacts',passed=True,tolerance='exact binary64 bits')]
 assert result['basis']==records['basis'] and result['result']['compared_binary64_entries']==result['result']['same_bits']==5248 and result['result']['different_bits']==0 and result['result']['exact_match'] is True
 assert all(q is False for q in result['qualification'].values()) and result['source_or_factor_change'] is False
 n=st+'_COMPARISONS.json';bind(n,receipt['output_sha256'][n]);comparison=json.loads(path(n).read_text())
 assert comparison['owner']==result['owner'] and comparison['result']==result['result'] and comparison['basis']==records['basis']
 # Recover the immutable 32 operand contacts and their 100-digit references.
 n=GLOBAL_DD_PROOF_STEM+'_INPUT.json';rc=json.loads(path(GLOBAL_DD_PROOF_STEM+'_RECEIPT.json').read_text());bind(n,rc['output_sha256'][n]);capsule=json.loads(path(n).read_text())
 assert capsule['owner']==proof['result']['owner'] and [r['group'] for r in capsule['rows']]==[10,14]
 for row,reference in zip(capsule['rows'],proof['result']['rows']):
  assert len(row['contacts'])==16 and {k:v for k,v in row.items() if k!='contacts'}==reference['selection'] and capsule['references'][str(row['group'])]==reference['reference100']
 assert [(q['group'],q['point']) for q in comparison['result']['points']]==[(row['group'],p['point']) for row in capsule['rows'] for p in row['contacts']]
 return capsule['rows'],capsule['references'],dict(terminal=t,comparisons=dict(file=st+'_COMPARISONS.json',sha256=receipt['output_sha256'][st+'_COMPARISONS.json']),control=result['controls'][0],replayed=False)
def load_frozen_system(records):
 # Saved current weak offsets/targets are used literally, with no point refit.
 names=('native_nodal_rate','metric_nodal_rate','compatibility_cycle_003_original_rhs','compatibility_original_residual','compatibility_original_action','current_Pn','current_Pm','trace_rhs')
 solution=read_pair(records['solution'],names)
 for n,a in solution.items():capture('saved_solution_'+n,a)
 geometry=read_pair(records['basis'],('R','dv','hats','cell_i','cell_j','native_scale','metric_scale','scalar_scale','r','z'))
 for n,a in geometry.items():capture('saved_basis_'+n,a)
 coefficients=read_pair(records['coefficient'],('mixing_L','modal_D','Maxwell_M0','operation_eL','operation_eD','operation_eM0'))
 for n,a in coefficients.items():capture('saved_coefficient_'+n,a)
 b=dict(L=coefficients['mixing_L'],D=coefficients['modal_D'],M0=coefficients['Maxwell_M0'],eL=coefficients['operation_eL'],eD=coefficients['operation_eD'],eM0=coefficients['operation_eM0'])
 columns=[]
 for iq in range(4):
  column=read_pair(records[str(iq)],('B','T','ih','N','mu','eB','eT'))
  for n,a in column.items():capture('saved_column%d_'%iq+n,a)
  columns.append(column)
 d={n:np.concatenate([c[n] for c in columns],axis=0) for n in columns[0]}
 for n,a in d.items():capture('assembled_original_'+n,a);assert np.all(np.isfinite(a))
 affine=read_pair(records['affine'],('Pn','Pm','cn','cm','trace_rhs'))
 for n,a in affine.items():capture('saved_authoritative_affine_'+n,a)
 assert np.array_equal(solution['current_Pn'],affine['Pn']) and np.array_equal(solution['current_Pm'],affine['Pm']) and np.array_equal(solution['trace_rhs'],affine['trace_rhs'])
 base=pack_fields(solution['native_nodal_rate'],solution['metric_nodal_rate']);rhs=solution['compatibility_cycle_003_original_rhs'];capture('saved_packed_x1080',base);capture('saved_original_rhs',rhs)
 assert np.array_equal(rhs,pack_fields(affine['Pn']-affine['cn'],affine['Pm']-affine['cm']))
 scales=(geometry['native_scale'],geometry['metric_scale'],geometry['scalar_scale'])
 data=dict(x1080=base,original_rhs=rhs,original_saved_action=solution['compatibility_original_action'],original_saved_residual=solution['compatibility_original_residual'],current_Pn=affine['Pn'],current_Pm=affine['Pm'],rounded_global_cn=affine['cn'],rounded_global_cm=affine['cm'],weak_trace_rhs=affine['trace_rhs'],native_scale=scales[0],metric_scale=scales[1],scalar_scale=scales[2])
 for n,a in data.items():capture('recovered_'+n,a)
 rec=checkpoint('RECOVERED_BASE',data,dict(kind='exact_frozen_x1080_rhs_targets_and_rounded_affine_offsets',parent_status='ORIGINAL_CANONICAL_ROWS_NOT_ADMITTED',parent_rate_adopted=False,records=records,point_reference_defects_retained_by_capsule=True,original_rhs_changed=False,pointstar_refit=False))
 return base,rhs,b,d,geometry,affine,scales,rec,solution
def save_precise_solution(x,action,residual,ratios,tr,admitted,cycles,rhs,affine,g,b,d,records):
 v,k,_=unpack_fields(x,False);nh,nm,_=unpack_fields(action[0],False);nl,ml,_=unpack_fields(action[1],False)
 pn=a_add(a_dd(affine['cn']),(nh,nl));pm=a_add(a_dd(affine['cm']),(nm,ml))
 capture('final_new_Pn_hi',pn[0]);capture('final_new_Pn_lo',pn[1]);capture('final_new_Pm_hi',pm[0]);capture('final_new_Pm_lo',pm[1])
 newpn=collapse(pn,'final_new_Pn');newpm=collapse(pm,'final_new_Pm')
 data=dict(native_nodal_rate=v,metric_nodal_rate=k,current_Pn=affine['Pn'],current_Pm=affine['Pm'],new_Pn=newpn,new_Pm=newpm,new_Pn_hi=pn[0],new_Pn_lo=pn[1],new_Pm_hi=pm[0],new_Pm_lo=pm[1],rounded_global_cn=affine['cn'],rounded_global_cm=affine['cm'],original_rhs=rhs,original_action_hi=action[0],original_action_lo=action[1],original_residual_hi=residual[0],original_residual_lo=residual[1],original_affine_and_actual_target_ratios=ratios,weak_trace_ratios=tr,trace_rhs=affine['trace_rhs'])
 data.update({n:a for n,a in RAW.items() if n.startswith('control_')})
 rec=checkpoint('SOLUTION',data,dict(kind='actual_canonical_compatibility_test_with_DD_original_certificate',stage='compatibility',canonical_rows_admitted=bool(np.all(ratios<=LINEAR_TOL)),trace_row_admitted=bool(np.all(tr<=LINEAR_TOL)),canonical_and_trace_admitted=admitted,targets='unchanged actual current force V003',basis_ref=records['basis'],metric_momentum_changed=False,point_reference_defects_disclosed=True,exact_global_selfadjointness_claim=False,corrections=cycles,physical_Cauchy_adoption=False))
 rate=None
 if admitted:
  jets={}
  for name,rate_field,evalf in (('native',v,evaluate_velocity),('metric',k,evaluate_metric)):
   for jet,axis in enumerate(('value','R','Z')):
    a=evalf(rate_field,g,jet);capture('admitted_'+name+'_jet_'+axis,a);assert np.all(np.isfinite(a));jets[name+'_jet_'+axis]=a
  rate=checkpoint('RATE_JETS',jets,dict(kind='genuine_fixed_Q1_rate_value_and_spatial_jets',stage='compatibility',canonical_rows_admitted=True,weak_trace_admitted=True,pointwise_CMC_claim=False,physical_time_history=None,basis_ref=records['basis']))
 return rec,rate
PINS={'author_fragment_global_native_metric_dd_admission_v001.txt':'9011f9acd997b63748f6148d38c75395010c7ceef8fa68ec449b5804119a9855','author_fragment_global_native_metric_dd_fixtures_v001.txt':'8aaa4bc094ef6239850ea4ea9045bbdb74d8033560043f0b727e6526f1c79295'}
def main():
 global np,OWNER,RAW,AVAILABLE
 ap=argparse.ArgumentParser();ap.add_argument('--root-run',action='store_true');args=ap.parse_args()
 assert args.root_run and not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and PROTOCOL_SHA,'Guarded definitions; ROOT owns execution'
 assert sha(path(STEM+'.md'))==PROTOCOL_SHA and not list(BASE.glob(STEM+'_*'))
 OWNER=dict(owner='root',pid=os.getpid(),started=now(),source_sha256=sha(__file__),scope='same saved sigma1 frozen original binary64 coefficients, new global DD arithmetic and bounded correction')
 try:
  json_file(STEM+'_OWNER_START.json',OWNER);bind(STEM+'.md',PROTOCOL_SHA)
  for n,h in PINS.items():bind(n,h)
  pins,records,proof=admission();rows,references,geometry_proof=recover_geometry_proof(records,proof)
  manifest=dict(owner=OWNER,input_sha256=INPUTS.copy(),records=records,proof=proof,geometry_proof=geometry_proof,configuration=dict(sigma=1.,linear_tolerance=LINEAR_TOL,arithmetic_tolerance=TOL,correction_cycle_cap=MAX_CYCLES,correction_iteration_cap=CAP,recurrence='unchanged binary64 coupled_action with DD original certificate',metric_evaluator='retained Fhat64',metric_scatter='F64 then weight64 then hat64',original_rhs_changed=False,coefficient_or_source_changed=False),qualification=FLAGS)
  json_file(STEM+'_MANIFEST.json',manifest)
  import numpy as np_local
  np=np_local
  checkpoint('INPUT',{},dict(kind='inherited_closed_DD_and_geometry_proofs_and_selected_frozen_system',records=records,proof=proof,geometry_proof=geometry_proof,rows=rows,references=references,qualification=False))
  fixtures=fresh_global_dd_fixtures();checkpoint('FIXTURE',dict(RAW,**AVAILABLE),fixtures);RAW={};AVAILABLE={}
  base,rhs,b,d,g,affine,scales,recovered,saved=load_frozen_system(records);RAW={};AVAILABLE={}
  current,action,residual,ratios,tr,admitted,cycles=measure_and_correct(base,rhs,b,d,g,affine,scales,rows,references,saved)
  assert len(CHECKS)==10+len(cycles) and all(q['passed'] for q in CHECKS)
  solution,jets=save_precise_solution(current,action,residual,ratios,tr,admitted,cycles,rhs,affine,g,b,d,records)
  status='CURRENT_CANONICAL_AND_WEAK_CMC_COMPATIBLE' if admitted else 'ORIGINAL_CANONICAL_ROWS_NOT_ADMITTED'
  case=dict(status=status,compatibility=solution,trace_preparation=None,rate_jets=jets,compatibility_corrections=cycles,parent_nonadmission_preserved=True,no_extra_iteration_cap=True,physical_adoption=False)
  recheck();rh=json_file(STEM+'_RESULT.json',dict(owner=OWNER,status=status,case=case,controls=CHECKS,checkpoints=RECORDS,geometry_proof=geometry_proof,qualification=FLAGS));recheck()
  json_file(STEM+'_RECEIPT.json',dict(owner=OWNER,status='CLOSED',closed=now(),input_sha256=INPUTS.copy(),output_sha256=OUTPUTS.copy(),result_sha256=rh,error_sha256=None,qualification=FLAGS));recheck();print(status,len(CHECKS),len(RECORDS))
  return 0 if admitted else 3
 except BaseException:
  failure=traceback.format_exc();raw_error=None;closing_error=None
  try:
   for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items():AVAILABLE['current_EFT_'+n]=a.copy()
   if RAW or AVAILABLE:checkpoint('ERROR_RAW',dict(RAW,**AVAILABLE),dict(kind='completed_original_operands_DD_words_and_current_iterate',context=dict(CONTEXT),controls=CHECKS,EFT_operation=DD_ARRAY_CURRENT.get('operation')),failed=True)
  except BaseException:raw_error=traceback.format_exc()
  try:seal_actual();recheck(False)
  except BaseException:closing_error=traceback.format_exc()
  prior=sha(path(STEM+'_RECEIPT.json')) if path(STEM+'_RECEIPT.json').exists() else None
  eh=json_file(STEM+'_ERROR.json',dict(owner=OWNER,status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=closing_error,prior_receipt_sha256=prior,controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS.copy(),preserved_outputs=OUTPUTS.copy(),qualification=FLAGS))
  json_file(STEM+('_ERROR_RECEIPT.json' if prior is not None else '_RECEIPT.json'),dict(owner=OWNER,status='CLOSED_ERROR',closed=now(),input_sha256=INPUTS.copy(),output_sha256=OUTPUTS.copy(),result_sha256=None,error_sha256=eh,prior_receipt_sha256=prior,qualification=FLAGS));seal_actual()
  return 1
if __name__=='__main__':raise SystemExit(main())

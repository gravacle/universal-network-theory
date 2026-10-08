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

def dd_native_value(x,g):
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

def dd_native_scatter(field,g):
 assert field[0].shape==field[1].shape==(33,15136,3)
 f=a_reshape(field,(33,4,86,44,3));out=a_dd(np.zeros((33,3,87,45)))
 for iq in range(4):
  R=g['R'][iq].reshape(86,44);weight=(g['dv'][iq]/g['R'][iq]).reshape(86,44)
  weighted=a_mul64(weight[...,None],a_slice(f,(slice(None),iq)))
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   hat=g['hats'][iq,corner,0];factor=np.broadcast_to(hat[...,None],(86,44,3)).copy();factor[...,2]*=R**2
   val=a_transpose(a_mul64(factor,weighted),(0,3,1,2));key=(slice(None),slice(None),slice(di,86+di),slice(dj,44+dj))
   update=a_add(a_slice(out,key),val);out[0][key]=update[0];out[1][key]=update[1]
 for component in (1,2):
  update=a_add(a_slice(out,(slice(None),component,1,slice(None))),a_slice(out,(slice(None),component,0,slice(None))))
  out[0][:,component,1]=update[0];out[1][:,component,1]=update[1]
 out[0][:,:,0]=0;out[1][:,:,0]=0;out[0][:,1,:,0]=0;out[1][:,1,:,0]=0
 return out
def dd_metric_scatter(field,g):
 # Original scatter F64 contraction, then weight64 and hat64 separately.
 assert field[0].shape==field[1].shape==(15136,6)
 f=a_reshape(field,(4,86,44,6));out=a_dd(np.zeros((6,87,45)))
 for iq in range(4):
  R=g['R'][iq].reshape(86,44);F=dd_metric_F(R);weight=(g['dv'][iq]/g['R'][iq]).reshape(86,44)
  FTf=a_matvec(F.swapaxes(-1,-2),a_slice(f,iq));weighted=a_mul64(weight[...,None],FTf)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   value=a_mul64(g['hats'][iq,corner,0][...,None],weighted);val=a_transpose(value,(2,0,1));key=(slice(None),slice(di,86+di),slice(dj,44+dj))
   update=a_add(a_slice(out,key),val);out[0][key]=update[0];out[1][key]=update[1]
 update=a_add(a_slice(out,(slice(None),1,slice(None))),a_slice(out,(slice(None),0,slice(None))))
 out[0][:,1]=update[0];out[1][:,1]=update[1];out[0][:,0]=0;out[1][:,0]=0;out[0][3:5,:,0]=0;out[1][3:5,:,0]=0
 return out
def global_coupled_action_dd(v,k,b,d,g,capture):
 vp=dd_native_value(v,g);capture('native_point_rate_hi',vp[0]);capture('native_point_rate_lo',vp[1])
 kp=dd_metric_value(k,g,capture);capture('metric_point_rate_hi',kp[0]);capture('metric_point_rate_lo',kp[1])
 npnt,mpnt=dd_point_coupled(vp,kp,b,d,capture)
 n=dd_native_scatter(npnt,g);capture('native_weak_action_hi',n[0]);capture('native_weak_action_lo',n[1])
 m=dd_metric_scatter(mpnt,g);capture('metric_weak_action_hi',m[0]);capture('metric_weak_action_lo',m[1])
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
def geometry_selected_bits(g,rows):
 compared=[];unequal=[]
 for row in rows:
  for p in row['contacts']:
   iq=p['iq'];ci,cj=p['cell'];local=p['local'];R=g['R'][iq].reshape(86,44);F=dd_metric_F(R)
   hats=[g['hats'][iq,a,0] for a in range(4)]
   nf=[];mf=[]
   for h in hats:
    factor=np.broadcast_to(h[...,None],(86,44,3)).copy();factor[...,2]=R**2*h;nf.append(factor[ci,cj].copy())
    mf.append((F*h[...,None,None])[ci,cj].copy())
   actual=dict(R2_64=np.asarray((R**2)[ci,cj]),R3_64=np.asarray((R**3)[ci,cj]),weight64=np.asarray((g['dv'][iq]/g['R'][iq])[local]),native_factors=np.asarray(nf),metric_factors=np.asarray(mf),hats=np.asarray([h[ci,cj] for h in hats]),scatter_factor64=np.asarray(hats[p['row_corner']][ci,cj]))
   evidence=dict(group=row['group'],point=p['point'],fields={})
   for name,a in actual.items():
    reference=np.asarray(p[name],dtype=np.float64);assert a.shape==reference.shape
    equal=a.view(np.uint64)==reference.view(np.uint64)
    evidence['fields'][name]=dict(actual=a.tolist(),reference=reference.tolist(),same_bits=bool(np.all(equal)))
    compared.append(bool(np.all(equal)));unequal.append(float(np.count_nonzero(~equal)))
   CONTEXT['latest_geometry_evidence']=evidence
   RAW['geometry_q%d_point%d_native_factors'%(iq,p['point'])]=actual['native_factors']
   RAW['geometry_q%d_point%d_metric_factors'%(iq,p['point'])]=actual['metric_factors']
 checkpoint('GEOMETRY',dict(RAW,comparison_equal=np.asarray(compared,dtype=bool),comparison_unequal_entries=np.asarray(unequal)),dict(kind='actual_array_geometry_bits_against32_scalar_frozen_contacts',selected_groups=[10,14],silent_factor_alignment=False))
 check('actual_array_geometry_matches_selected_frozen_bits',np.asarray(unequal),np.zeros(len(unequal)),np.ones(len(unequal)))
def array_fresh_controls():
 # New array interface checks; no completed scalar seven-fixture replay.
 x=np.array((2.**60,2.**60));y=np.array((1.,-2.**60));s=a_sum(x,y)
 v=a_sub(s,a_dd(np.array((2.**60,-1.))))
 check('fresh_array_two_sum_and_cancelled_high_words',collapse(v,'fresh_array_sum'),np.ones(2),np.ones(2))
 x=a_sum(np.array((2.**53+2.,2.**60)),np.array((0.,1.)))
 y=a_sum(np.array((1.-2.**-52,1.)),np.array((0.,-2.**-60)))
 v=a_sub(a_mul(x,y),a_dd(np.array((2.**53,2.**60))))
 expected=-np.array((2.**-51,2.**-60))
 check('fresh_array_product_low_and_allfour_DD_products',collapse(v,'fresh_array_product'),expected,abs(expected))
 checkpoint('FIXTURE',{n:a for n,a in AVAILABLE.items() if n.startswith('fresh_')},dict(kind='two_new_array_EFT_interface_controls',source_or_field_replay=False,controls=CHECKS[-2:]))
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
def measure_and_correct(base,rhs,b,d,g,affine,scales,rows,references):
 scale=pack_fields(scales[0],scales[1]);capture('positive_original_congruence',scale);assert np.all(scale>0) and np.all(np.isfinite(scale))
 action,res,ratios,tr=certify_current_dd(base,rhs,b,d,g,affine,scales,'initial')
 selected_row_accuracy(action,rhs,rows,references)
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
  actual=np.array([np.linalg.norm(x) for x in diff[:2]]);env=np.array([max(np.linalg.norm(a),np.linalg.norm(z)) for a,z in zip(true[:2],old[:2])])
  assert np.all(np.isfinite(actual)) and np.all(np.isfinite(env)) and np.all(env>0)
  check(label+'_original_shifted_residual_with_actual_node_rounding',actual,np.zeros(2),env)
  cycles.append(dict(cycle=cycle,reason=reason,callback_admitted=bool(ok),original_affine_and_actual_target_ratios=ratios.tolist(),weak_trace_ratios=tr.tolist()))
  checkpoint('CORRECTION',{n:a for n,a in AVAILABLE.items() if n.startswith(label+'_')},dict(kind='bounded_float_MINRES_correction_with_DD_original_certificate',cycle=cycle,cap=CAP,original_rhs_changed=False,targets_changed=False,physical_adoption=False,controls=CHECKS[-1:]))
 admitted=bool(np.all(ratios<=LINEAR_TOL) and np.all(tr<=LINEAR_TOL))
 return current,action,res,ratios,tr,admitted,cycles

def main():
 raise RuntimeError("AUTHORING: global DD final loader/caller pending; no execution")
if __name__=="__main__":main()

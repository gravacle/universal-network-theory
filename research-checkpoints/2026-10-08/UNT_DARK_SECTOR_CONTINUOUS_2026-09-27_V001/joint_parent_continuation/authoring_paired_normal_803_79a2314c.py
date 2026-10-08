"""Guarded paired same-action normal constraint diagnostic from saved pilot primitives."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,math,os,sys,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_PAIRED_CURRENT_NORMAL_CONSTRAINTS_V001'
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=True
PROTOCOL_SHA=None
BAND='CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001'
SIGMA=1.;C=1.98;KB=.02;ALPHA=KB/C;ELL=.1;GC=3*math.pi/8
B=None;TOL=2e-11;LINEAR_TOL=1e-10
np=None;OWNER=None;INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];RAW={};AVAILABLE={};CONTEXT={};DD_ARRAY_CURRENT={}
FLAGS=dict(normal_constraints_qualified=False,canonical_primitive_physical_adoption=False,CMC_preservation_qualified=False,evolution_qualified=False,physical_metric_qualified=False,source_history_qualified=False,exterior_qualified=False,galaxy_velocity_qualified=False)

PINS={'author_fragment_current_normal_two_word_action_v002.py': '710b450c125c7ec13b06cbd06b56def7527f8fd148cb103d4aee65853acb1f69', 'author_fragment_current_normal_operation_envelopes_v001.py': '71c8107533923b60681f4d66da4a47693edf9f6818c7678855dcc1620dd3ed7b', 'author_fragment_normal_pilot_pair_admission_v002.txt': '935d06abe0d41ff8f5f3d92e4d5be41d8467fb217789944d83157b8638d7b298', 'root_held_primitive_readout_700_679a97b2.py': '679a97b277196dff2f61acffd39167d130f882df5d0123adb0fc2a5e604ea1db', 'cross_u_current_canonical_nodal_normal_constraints_v001.py': '41f84a9165e8028734e07d463444eb30077bd7145df7f814440fc9ad3201968d'}

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

def connection_from_jet_envelope(hi,dg):
 # hi is the saved inverse. dg may be the actual signed metric first jet OR
 # a previously propagated nonnegative envelope for that jet's construction.
 # Bound the three Christoffel summands BEFORE their +/- cancellation.
 p=len(hi);out=np.zeros((p,4,4,4));eh=abs(hi);ed=abs(dg)
 for a in range(4):
  for b in range(4):
   terms=ed[:,a,b,:]+ed[:,b,a,:]+ed[:,:,a,b]
   out[:,:,a,b]=np.einsum('plm,pm->pl',eh,terms)/2
 RAW['operation_connection_jet_envelope']=out.copy()
 return out


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

def collapse(pair,label):
 value=pair[0]+pair[1];capture(label+'_hi',pair[0]);capture(label+'_lo',pair[1]);capture(label+'_rounded_value',value)
 assert np.all(np.isfinite(value));return value

def normal_keep_pair(name,value,keep):
 keep(name+'_hi',value[0]);keep(name+'_lo',value[1]);return value

def normal_pair_connection_from_jet(hi,dg,keep,label):
 p=len(hi);out=a_dd(np.zeros((p,4,4,4)))
 for a in range(4):
  for b in range(4):
   terms=a_sub(a_add(a_slice(dg,(slice(None),a,b,slice(None))),a_slice(dg,(slice(None),b,a,slice(None)))),a_slice(dg,(slice(None),slice(None),a,b)))
   normal_keep_pair(label+'_Gamma_summands_a%d_b%d'%(a,b),terms,keep)
   value=a_mul64(.5,a_matvec(hi,terms))
   out[0][:,:,a,b]=value[0];out[1][:,:,a,b]=value[1]
   normal_keep_pair(label+'_Gamma_partial',out,keep)
 return out

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


def current_reference_curvature(s,c,cj):
 # Q and V are COORDINATE DENSITIES, already containing cylindrical R.
 # sqrt(h)R3 = Q + partial_i V^i for the fixed flat cylindrical reference.
 R=s['R'];dh=cj['dh'][:,1:];edh=s['metric_partial_envelope'][:,1:,1:,1:];ih=c['ih'];p=len(R)
 G=np.zeros((p,3,3,3));eG=np.zeros_like(G)
 for i in range(3):
  for j in range(3):
   terms=dh[:,i,j,:]+dh[:,j,i,:]-dh[:,:,i,j]
   G[:,:,i,j]=np.einsum('plm,pm->pl',ih,terms)/2
   capture('reference_curvature_Gamma3_partial',G)
   eG[:,:,i,j]=np.einsum('plm,pm->pl',abs(ih),edh[:,i,j,:]+edh[:,j,i,:]+edh[:,:,i,j])/2
   capture('reference_curvature_Gamma3_envelope_partial',eG)
 bar=np.zeros_like(G);bar[:,0,2,2]=-R;bar[:,2,0,2]=bar[:,2,2,0]=1/R
 cc=G-bar;ec=eG+abs(bar)
 first=np.einsum('pij,pkil,pljk->p',ih,cc,cc);second=np.einsum('pij,pkij,plkl->p',ih,cc,cc)
 Q=c['sqrt_h']*(first-second);capture('reference_curvature_Q',Q)
 V=c['sqrt_h'][:,None]*(np.einsum('pij,pkij->pk',ih,cc)-np.einsum('pik,plil->pk',ih,cc));capture('reference_curvature_V',V)
 eQ=c['sqrt_h']*(np.einsum('pij,pkil,pljk->p',abs(ih),ec,ec)+np.einsum('pij,pkij,plkl->p',abs(ih),ec,ec));capture('reference_curvature_envelope_Q',eQ)
 eV=c['sqrt_h'][:,None]*(np.einsum('pij,pkij->pk',abs(ih),ec)+np.einsum('pik,plil->pk',abs(ih),ec))
 out=dict(Gamma3=G,reference_Gamma3=bar,C3=cc,envelope_C3=ec,Q_terms=c['sqrt_h'][:,None]*np.column_stack((first,-second)),Q=Q,V=V,envelope_Q=eQ,envelope_V=eV)
 for name,a in out.items():finite_real('reference_curvature_'+name,a)
 return out

def normal_test_mask():
 # All four coefficient fields are axis-even; betaR=R*coefficient is smooth.
 # betaZ is odd across the sheet. Outer test values vanish, not physical fields.
 m=np.ones((4,87,45),dtype=bool);m[:,0]=False;m[:,-1]=False;m[:,:,-1]=False;m[2,:,0]=False
 return m

def extend_normal_tests(a):
 assert a.shape==(4,87,45)
 out=a.copy();out[:,0]=out[:,1];out[:,-1]=0;out[:,:,-1]=0;out[2,:,0]=0
 return out

def restrict_normal_rows(a):
 assert a.shape==(4,87,45)
 out=a.copy();out[:,1]+=out[:,0];out[:,0]=0;out[:,-1]=0;out[:,:,-1]=0;out[2,:,0]=0
 return out

def normal_hat_jet(geo,iq,corner,row):
 N,NR,NZ=geo['hats'][iq,corner];R=geo['R'][iq].reshape(86,44)
 if row==1:return (R*N,R*NR+N,R*NZ)
 return (N,NR,NZ)

def evaluate_normal_test(a,geo):
 a=extend_normal_tests(a);out=np.zeros((15136,4,3))
 for iq in range(4):
  sl=slice(iq*3784,(iq+1)*3784)
  for corner,(i,j) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   for row in range(4):
    av=a[row,i:86+i,j:44+j]
    for jet,h in enumerate(normal_hat_jet(geo,iq,corner,row)):out[sl,row,jet]+=(av*h).reshape(3784)
 return out

def normal_hat_operation_envelope(geo,iq,corner,row):
 N,NR,NZ=geo['hats'][iq,corner];R=geo['R'][iq].reshape(86,44)
 if row==1:return (R*abs(N),R*abs(NR)+abs(N),R*abs(NZ))
 return (abs(N),abs(NR),abs(NZ))

def scatter_normal_envelope(coeff,geo):
 assert coeff.shape==(15136,4,3) and np.all(coeff>=0)
 out=np.zeros((4,87,45))
 for iq in range(4):
  sl=slice(iq*3784,(iq+1)*3784);wq=(geo['dv'][iq]/geo['R'][iq]).reshape(86,44)
  for corner,(i,j) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   for row in range(4):
    val=sum(coeff[sl,row,k].reshape(86,44)*h for k,h in enumerate(normal_hat_operation_envelope(geo,iq,corner,row)))
    out[row,i:86+i,j:44+j]+=wq*val
 return restrict_normal_rows(out)

def current_EH_isotropic_shift_diagnostic(s,c,cj,Hbar):
 # Analytical comparison tensor only. The actual full pi_EH and normal rows
 # are authoritative; no zero-incidence replacement or alias subtraction.
 iso=-c['sqrt_h'][:,None,None]*Hbar*c['ih']/C
 eiso=c['sqrt_h'][:,None,None]*abs(Hbar)*abs(c['ih'])/C
 p=len(c['N']);coeff=np.zeros((p,4,3));env=np.zeros_like(coeff)
 for i in range(3):
  coeff[:,i+1,0]=-np.einsum('pjk,pjk->p',iso,cj['dh'][:,i+1])
  env[:,i+1,0]=np.einsum('pjk,pjk->p',eiso,s['metric_partial_envelope'][:,i+1,1:,1:])
  for jet,j in ((1,0),(2,1)):
   coeff[:,i+1,jet]=-2*np.einsum('pk,pk->p',iso[:,j],c['h'][:,:,i])
   env[:,i+1,jet]=2*np.einsum('pk,pk->p',eiso[:,j],abs(c['h'][:,:,i]))
 for n,a in dict(momentum=iso,momentum_envelope=eiso,coefficient=coeff,envelope=env).items():finite_real('EH_isotropic_diagnostic_'+n,a)
 return iso,coeff,env


"""Definitions only: same normal1101 action on two-word first jets.
Configuration/test-only coefficients retain the original binary64 convention.
All rate-dependent contractions retain both words and every hh/hl/lh/ll term.
Caller supplies reviewed a_*, a_div64, normal_pair_* and affine jet helpers,
np,C,ALPHA,ELL,B,GC. ROOT alone evaluates an admitted containing producer.
Fixed curvature Q/V and ordinary annular source are each assembled once.
No source, gauge, history, pressure subtraction, physical port or law changes.
The original FE 1e-10 momentum bridge is a separate mandatory caller gate.
Preserved unexecuted v001 SHA 6ea87fd4085fed799e03ff507cdcaba06f4b1095f089b5727472025c43b77f31.
"""

def normal_action_reduce(x,axes):
 for axis in sorted(((a+x[0].ndim) if a<0 else a for a in axes),reverse=True):x=normal_pair_sum(x,axis)
 return x

def normal_action_dot(x,y,axes):return normal_action_reduce(a_mul(x,y),axes)

def paired_normal_chart_jets(s,c,j,keep,label):
 dg=j['dg'];dhi=a_transpose(normal_pair_sandwich(s['hi'],a_transpose(dg,(1,0,2,3)),s['hi']),(1,0,2,3));dhi=(-dhi[0],-dhi[1])
 dN=a_mul64(c['N'][:,None]**3/2,a_slice(dhi,(slice(None),slice(None),0,0)))
 db=a_add(a_mul64(2*c['N'][:,None,None]*s['hi'][:,None,0,1:],(dN[0][:,:,None],dN[1][:,:,None])),a_mul64(c['N'][:,None,None]**2,a_slice(dhi,(slice(None),slice(None),0,slice(1,None)))))
 out=dict(dN=dN,dbeta=db,dh=a_slice(dg,(slice(None),slice(None),slice(1,None),slice(1,None))))
 for n,x in out.items():normal_keep_pair(label+'_'+n,x,keep)
 return out

def paired_normal_lift(s,c,j,cj,f,df,b,db,keep,label):
 N,h,beta,U,z=c['N'],c['h'],c['beta'],s['U'],s['z'];p=len(U)
 q=np.zeros((p,4,4));q[:,0,0]=-2*N*f+2*np.einsum('pi,pij,pj->p',beta,h,b);q[:,0,1:]=np.einsum('pij,pj->pi',h,b);q[:,1:,0]=q[:,0,1:]
 eta=np.empty_like(U);eta[:,0]=-U[:,0]*f/N;eta[:,1:]=-U[:,0,None]*b-beta*eta[:,0,None]
 ez=np.einsum('pa,jpa->jp',eta,z);zeta=np.zeros_like(z);zeta[:,:,0]=-ez/U[None,:,0]
 for n,x in dict(q=q,eta=eta,zeta=zeta,compensation_numerator=ez).items():keep(label+'_'+n,x)
 dq=a_dd(np.zeros((p,4,4,4)));d00=a_add(a_mul64(-2*f[:,None],cj['dN']),a_dd(-2*N[:,None]*df+2*np.einsum('pi,pij,paj->pa',beta,h,db)))
 for i in range(3):
  for k in range(3):
   d00=a_add(d00,a_mul64((2*h[:,i,k]*b[:,k])[:,None],a_slice(cj['dbeta'],(slice(None),slice(None),i))))
   d00=a_add(d00,a_mul64((2*beta[:,i]*b[:,k])[:,None],a_slice(cj['dh'],(slice(None),slice(None),i,k))));normal_keep_pair(label+'_dq00_partial',d00,keep)
 dq[0][:,:,0,0]=d00[0];dq[1][:,:,0,0]=d00[1]
 for i in range(3):
  value=a_dd(np.einsum('pk,pak->pa',h[:,i],db))
  for k in range(3):value=a_add(value,a_mul64(b[:,k,None],a_slice(cj['dh'],(slice(None),slice(None),i,k))))
  dq[0][:,:,0,i+1]=dq[0][:,:,i+1,0]=value[0];dq[1][:,:,0,i+1]=dq[1][:,:,i+1,0]=value[1]
 normal_keep_pair(label+'_dq',dq,keep)
 du0=a_slice(j['du'],(slice(None),slice(None),0));de0=a_add(a_mul64((-f/N)[:,None],du0),a_dd(-U[:,0,None]*df/N[:,None]))
 de0=a_add(de0,a_mul64((U[:,0]*f/N**2)[:,None],cj['dN']));deta=a_dd(np.zeros_like(s['du']));deta[0][:,:,0]=de0[0];deta[1][:,:,0]=de0[1]
 for i in range(3):
  value=a_add(a_mul64(-b[:,i,None],du0),a_dd(-U[:,0,None]*db[:,:,i]))
  value=a_sub(value,a_mul64(eta[:,0,None],a_slice(cj['dbeta'],(slice(None),slice(None),i))));value=a_sub(value,a_mul64(beta[:,i,None],de0))
  deta[0][:,:,i+1]=value[0];deta[1][:,:,i+1]=value[1]
 normal_keep_pair(label+'_deta',deta,keep);dez=a_dd(np.zeros((32,p,4)))
 for a in range(4):
  dez=a_add(dez,a_mul64(z[:,:,a,None],a_slice(deta,(slice(None),slice(None),a))))
  dez=a_add(dez,a_mul64(eta[None,:,a,None],a_slice(j['dz'],(slice(None),slice(None),slice(None),a))));normal_keep_pair(label+'_compensation_numerator_jet_partial',dez,keep)
 dz0=a_add(a_div64((-dez[0],-dez[1]),U[None,:,0,None],keep,label+'_dzeta_division'),a_mul64(ez[:,:,None]/U[None,:,0,None]**2,(du0[0][None],du0[1][None])))
 dzeta=a_dd(np.zeros_like(s['dz']));dzeta[0][:,:,:,0]=dz0[0];dzeta[1][:,:,:,0]=dz0[1];normal_keep_pair(label+'_dzeta',dzeta,keep)
 return dict(q=q,dq=dq,eta=eta,deta=deta,zeta=zeta,dzeta=dzeta)

def paired_normal_metric_delta(s,j,feature,lift,keep,label):
 q,eta=lift['q'],lift['eta'];F=feature['paired'];U,z,g,hi,P=s['U'],s['z'],s['g'],s['hi'],s['P'];nq=[]
 for a in range(4):
  ga=a_slice(j['Ga'],(slice(None),slice(None),a,slice(None)))
  connection=a_add(normal_pair_right(a_transpose(ga,(0,2,1)),q),normal_pair_left(q,ga))
  nq.append(a_sub(a_slice(lift['dq'],(slice(None),a,slice(None),slice(None))),connection))
 deltaG=normal_pair_connection_from_jet(hi,a_stack(nq,axis=1),keep,label+'_delta_connection')
 dnu=lift['deta'];dnz=a_dd(np.zeros_like(s['dz']))
 for l in range(4):
  dnu=a_add(dnu,a_mul64(U[:,l,None,None],a_transpose(a_slice(deltaG,(slice(None),slice(None),slice(None),l)),(0,2,1))))
  dnu=a_add(dnu,a_mul64(eta[:,l,None,None],a_transpose(a_slice(j['Ga'],(slice(None),slice(None),slice(None),l)),(0,2,1))))
  dnz=a_sub(dnz,a_mul64(z[:,:,l,None,None],a_slice(deltaG,(slice(None),l,slice(None),slice(None)))));normal_keep_pair(label+'_dnu_partial',dnu,keep);normal_keep_pair(label+'_dnz_partial',dnz,keep)
 duc=np.einsum('pab,pb->pa',q,U)+np.einsum('pab,pb->pa',g,eta);dP=duc[:,:,None]*U[:,None,:]+s['uc'][:,:,None]*eta[:,None,:]
 dqq=a_dd(np.zeros_like(F['q'][0]));da=a_dd(np.zeros_like(F['a'][0]))
 for a in range(4):
  dqq=a_add(dqq,a_add(a_mul64(eta[None,:,a,None],a_slice(F['nz'],(slice(None),slice(None),a,slice(None)))),a_mul64(U[None,:,a,None],a_slice(dnz,(slice(None),slice(None),a,slice(None))))))
  da=a_add(da,a_add(a_mul64(eta[:,a,None],a_slice(F['nu'],(slice(None),a,slice(None)))),a_mul64(U[:,a,None],a_slice(dnu,(slice(None),a,slice(None))))));normal_keep_pair(label+'_delta_q_partial',dqq,keep);normal_keep_pair(label+'_delta_acceleration_partial',da,keep)
 dV=a_add(a_matvec(dP,F['q']),a_matvec(P,dqq))
 dD=a_add(normal_pair_sandwich(dP,F['nz'],P.swapaxes(-1,-2)),normal_pair_sandwich(P,F['nz'],dP.swapaxes(-1,-2)));dD=a_add(dD,normal_pair_sandwich(P,dnz,P.swapaxes(-1,-2)))
 lower=a_add(normal_pair_right(F['nu'],q),normal_pair_right(dnu,g));dF=a_sub(lower,a_transpose(lower,(0,2,1)))
 dhi=-np.einsum('pac,pcd,pdb->pab',hi,q,hi);dr=np.einsum('pab,pb->pa',dP,s['phi']);lm=np.einsum('pab,pba->p',hi,q)/2
 out=dict(deltaG=deltaG,dnu=dnu,dnz=dnz,dV=dV,dD=dD,dF=dF,da=da)
 for n,x in out.items():normal_keep_pair(label+'_'+n,x,keep)
 for n,x in dict(dhi=dhi,dr=dr,log_measure=lm).items():keep(label+'_'+n,x)
 return dict(paired=out,dhi=dhi,dr=dr,lm=lm)

def paired_normal_native_metric_terms(s,feature,delta,keep,label):
 F=feature['paired'];D=delta['paired'];hi,dhi=s['hi'],delta['dhi'];om=s['omega'][:,None]**2;kj=(B*GC)**2*s['xi'][:,None]**4
 V2=normal_action_dot(F['V_raised'],F['V'],(2,));D2=normal_action_dot(F['D_raised'],F['D'],(2,3));F2=normal_action_dot(F['Fup'],F['F'],(1,2))
 dV2=a_add(normal_action_dot(a_matvec(dhi,F['V']),F['V'],(2,)),a_mul64(2.,normal_action_dot(F['V_raised'],D['dV'],(2,))))
 dD2=a_mul64(2.,normal_action_dot(F['D_raised'],D['dD'],(2,3)))
 dF2=a_mul64(2.,normal_action_dot(F['Fup'],D['dF'],(1,2)))
 for A0,A1 in ((dhi,hi),(hi,dhi)):
  dD2=a_add(dD2,normal_action_dot(normal_pair_sandwich(A0,F['D'],A1),F['D'],(2,3)))
  dF2=a_add(dF2,normal_action_dot(normal_pair_sandwich(A0,F['F'],A1),F['F'],(1,2)));normal_keep_pair(label+'_delta_D_squared_partial',dD2,keep);normal_keep_pair(label+'_delta_F_squared_partial',dF2,keep)
 az=normal_action_reduce(a_mul64(s['z'],(F['a'][0][None],F['a'][1][None])),(2,));daz=normal_action_reduce(a_mul64(s['z'],(D['da'][0][None],D['da'][1][None])),(2,))
 dz2=np.einsum('jpa,pab,jpb->jp',s['z'],dhi,s['z']);z2=s['z2']
 primal=a_stack((a_div64(V2,2*om,keep,label+'_primal_frequency'),a_dd(-z2/2),a_dd(-z2*z2/(4*kj)),a_mul64(-ELL**2/2,D2),az),axis=-1)
 derivative=a_stack((a_div64(dV2,2*om,keep,label+'_variation_frequency'),a_dd(-dz2/2),a_dd(-z2*dz2/(2*kj)),a_mul64(-ELL**2/2,dD2),daz),axis=-1)
 modal=normal_pair_sum(a_mul64(s['w'][:,None,None],primal),0);dmodal=normal_pair_sum(a_mul64(s['w'][:,None,None],derivative),0)
 r2=np.einsum('pa,pab,pb->p',s['r'],hi,s['r']);dr2=np.einsum('pa,pab,pb->p',s['r'],dhi,s['r'])+2*np.einsum('pa,pab,pb->p',s['r'],hi,delta['dr'])
 p=a_stack([a_mul64(-ALPHA/4,F2),a_dd(-r2/2)]+[a_slice(modal,(slice(None),i)) for i in range(5)],axis=-1)
 dp=a_stack([a_mul64(-ALPHA/4,dF2),a_dd(-dr2/2)]+[a_slice(dmodal,(slice(None),i)) for i in range(5)],axis=-1)
 out=a_add(dp,a_mul64(delta['lm'][:,None],p));normal_keep_pair(label+'_primal',p,keep);normal_keep_pair(label+'_variation_without_measure',dp,keep);return normal_keep_pair(label+'_terms',out,keep)

def paired_normal_z0_terms(s,j,feature,lift,keep,label):
 F=feature['paired'];nz=lift['dzeta'];U,zeta,P=s['U'],lift['zeta'],s['P']
 for l in range(4):nz=a_sub(nz,a_mul64(zeta[:,:,l,None,None],a_slice(j['Ga'],(slice(None),l,slice(None),slice(None)))));normal_keep_pair(label+'_covariant_compensation_jet_partial',nz,keep)
 dq=a_dd(np.zeros_like(F['q'][0]))
 for a in range(4):dq=a_add(dq,a_mul64(U[None,:,a,None],a_slice(nz,(slice(None),slice(None),a,slice(None)))))
 dV=a_matvec(P,dq);dD=normal_pair_sandwich(P,nz,P.swapaxes(-1,-2))
 kinetic=a_div64(normal_action_dot(F['V_raised'],dV,(2,)),s['omega'][:,None]**2,keep,label+'_frequency')
 zeta_dot=np.einsum('jpa,pab,jpb->jp',s['z'],s['hi'],zeta);quartic=s['z2']/((B*GC)**2*s['xi'][:,None]**4)
 gradient=a_mul64(-ELL**2,normal_action_dot(F['D_raised'],dD,(2,3)));acc=normal_action_reduce(a_mul64(zeta,(F['a'][0][None],F['a'][1][None])),(2,))
 modes=a_stack((kinetic,a_dd(-zeta_dot),a_dd(-quartic*zeta_dot),gradient,acc),axis=-1);modal=normal_pair_sum(a_mul64(s['w'][:,None,None],modes),0)
 zero=a_dd(np.zeros(len(U)));out=a_stack([zero,zero]+[a_slice(modal,(slice(None),i)) for i in range(5)],axis=-1)
 normal_keep_pair(label+'_covariant_compensation_jet',nz,keep);return normal_keep_pair(label+'_terms',out,keep)

def paired_normal_EH_terms(s,c,cj,moments,curvature,f,df,b,db,keep,label):
 kinetic=a_sub(a_mul(moments['Ktrace'],moments['Ktrace']),normal_action_dot(moments['K'],normal_pair_sandwich(c['ih'],moments['K'],c['ih']),(1,2)))
 kinetic=a_div64(a_mul64(f*c['sqrt_h'],kinetic),2*C,keep,label+'_kinetic_division')
 cv=a_prod(f,curvature['Q'])
 for i in range(3):cv=a_sub(cv,a_prod(df[:,i+1],curvature['V'][:,i]))
 cv=a_div64(cv,2*C,keep,label+'_curvature_division');Lie=a_dd(np.zeros_like(c['h']))
 for i in range(3):Lie=a_add(Lie,a_mul64(b[:,i,None,None],a_slice(cj['dh'],(slice(None),i+1,slice(None),slice(None)))))
 Lie=a_add(Lie,a_dd(np.einsum('pik,pjk->pij',c['h'],db[:,1:])+np.einsum('pkj,pik->pij',c['h'],db[:,1:])))
 paired_shift=normal_action_dot(moments['metric_EH_tensor'],Lie,(1,2));normal_keep_pair(label+'_unnegated_shift',paired_shift,keep);shift=(-paired_shift[0],-paired_shift[1])
 normal_keep_pair(label+'_Lie_test_h',Lie,keep);out=a_stack((cv,kinetic,shift),axis=-1);return normal_keep_pair(label+'_terms',out,keep)

def paired_normal_direction(s,c,jets,feature,moments,curvature,f,df,b,db,keep,label):
 cj=paired_normal_chart_jets(s,c,jets,keep,label+'_chart');lift=paired_normal_lift(s,c,jets,cj,f,df,b,db,keep,label+'_lift')
 delta=paired_normal_metric_delta(s,jets,feature,lift,keep,label+'_metric_delta')
 native=paired_normal_native_metric_terms(s,feature,delta,keep,label+'_native');mode=paired_normal_z0_terms(s,jets,feature,lift,keep,label+'_z0')
 dX=-np.einsum('pa,pab,pb->p',s['phi'],delta['dhi'],s['phi'])/(2*s['phase_X']);phase=a_stack((a_prod(s['phase_PX'],dX),a_prod(s['phase_P'],delta['lm'])),axis=-1);normal_keep_pair(label+'_absolute_phase_terms',phase,keep)
 EH=paired_normal_EH_terms(s,c,cj,moments,curvature,f,df,b,db,keep,label+'_EH')
 components=a_stack((a_mul64(c['dens'],normal_pair_sum(native,1)),a_mul64(c['dens'],normal_pair_sum(mode,1)),a_mul64(c['dens'],normal_pair_sum(phase,1)),normal_pair_sum(EH,1)),axis=-1)
 coefficient=normal_pair_sum(components,1);normal_keep_pair(label+'_components',components,keep);normal_keep_pair(label+'_coefficient',coefficient,keep)
 return dict(native_metric_terms=native,mode_compensation_terms=mode,absolute_phase_terms=phase,EH_terms=EH,component_densities=components,coefficient=coefficient,configuration_or_law_changed=False,ordinary_source_added_here=False)

"""Definitions only: positive operation bounds for paired normal action134.
Signed primitives/features/momenta are consumed elsewhere, never replayed here.
Input op contains pilot's uncancelled du/dz/dg/Ga bounds. Configuration is fixed.
All projector, polarization, connection, inverse and quadratic bounds precede
their signed cancellations. Curvature envelopes and ordinary source are supplied
once by the caller. These bounds do not replace the original 1e-10 bridge test.
Caller supplies np,C,ALPHA,ELL,B,GC,connection_from_jet_envelope and keep.
No definitions, arrays, helpers, physical fields or operators evaluated by author.
"""

def normal_positive_save(label,rows,keep):
 for n,a in rows.items():keep(label+'_'+n,a);assert np.all(np.isfinite(a)) and np.all(a>=0),(label,n)
 return rows

def normal_positive_features(s,c,op,keep,label):
 U,z,g,hi=abs(s['U']),abs(s['z']),abs(s['g']),abs(s['hi']);w=abs(s['w']);om=s['omega'][:,None]**2
 uc=np.einsum('pab,pb->pa',g,U);P=np.eye(4)[None]+uc[:,:,None]*U[:,None,:];Z=np.einsum('j,jpa->pa',w,z)
 nu=op['du']+np.einsum('pbal,pl->pab',op['Ga'],U);nz=op['dz']+np.einsum('plab,jpl->jpab',op['Ga'],z)
 q=np.einsum('pa,jpab->jpb',U,nz);V=np.einsum('pab,jpb->jpa',P,q);D=np.einsum('pac,jpcd,pbd->jpab',P,nz,P)
 lower=np.einsum('pab,pcb->pca',g,nu);F=lower+lower.swapaxes(1,2);Fup=np.einsum('pac,pcd,pdb->pab',hi,F,hi)
 a=np.einsum('pa,pab->pb',U,nu);Vu=np.einsum('pab,jpb->jpa',hi,V);Du=np.einsum('pac,jpcd,pdb->jpab',hi,D,hi)
 Pi=w[:,None,None,None]*(U[None,:,:,None]*Vu[:,:,None,:]/om[:,:,None,None]+ELL**2*Du)
 PiU=abs(ALPHA)*np.einsum('pac,pcb->pab',hi,F)+U[:,:,None]*Z[:,None,:]
 sym=(Pi+Pi.swapaxes(2,3))/2;Klo=Z[:,:,None,None]*U[:,None,:,None]*U[:,None,None,:]+np.einsum('jpab,jpl->plab',sym,z)
 Kup=np.einsum('plm,pmab->plab',hi,Klo);CC=(Kup.transpose(0,2,1,3)+Kup.transpose(0,2,3,1)+Kup)/2
 CC+=abs(ALPHA)*(Fup[:,:,:,None]*U[:,None,None,:]+Fup[:,:,None,:]*U[:,None,:,None])/2
 K=abs(c['N'])[:,None,None]*op['Ga'][:,0,1:,1:];ih=abs(c['ih']);tr=np.einsum('pij,pij->p',ih,K)
 pi=abs(c['sqrt_h'])[:,None,None]*(np.einsum('pik,pkl,plj->pij',ih,K,ih)+tr[:,None,None]*ih)/(2*abs(C))
 r=np.einsum('pab,pb->pa',P,abs(s['phi']));z2=np.einsum('jpa,pab,jpb->jp',z,hi,z)
 return normal_positive_save(label,dict(uc=uc,P=P,Z=Z,nu=nu,nz=nz,q=q,V=V,D=D,F=F,Fup=Fup,a=a,V_raised=Vu,D_raised=Du,Pi=Pi,PiU=PiU,connection_momentum=CC,K=K,Ktrace=tr,metric_EH_tensor=pi,r=r,z2=z2),keep)

def normal_positive_chart_jets(s,c,op,keep,label):
 hi=abs(s['hi']);dhi=np.einsum('pij,pajk,pkl->pail',hi,op['dg'],hi);N=abs(c['N'])
 dN=N[:,None]**3*dhi[:,:,0,0]/2;dbeta=2*N[:,None,None]*dN[:,:,None]*hi[:,None,0,1:]+N[:,None,None]**2*dhi[:,:,0,1:]
 return normal_positive_save(label,dict(dhi=dhi,dN=dN,dbeta=dbeta,dh=op['dg'][:,:,1:,1:]),keep)

def normal_positive_lift(s,c,op,cj,f,df,b,db,keep,label):
 U,z,g,h,N,beta=abs(s['U']),abs(s['z']),abs(s['g']),abs(c['h']),abs(c['N']),abs(c['beta']);p=len(U)
 f,df,b,db=abs(f),abs(df),abs(b),abs(db);q=np.zeros((p,4,4))
 q[:,0,0]=2*N*f+2*np.einsum('pi,pij,pj->p',beta,h,b);q[:,0,1:]=np.einsum('pij,pj->pi',h,b);q[:,1:,0]=q[:,0,1:]
 eta=np.zeros((p,4));eta[:,0]=U[:,0]*f/N;eta[:,1:]=U[:,0,None]*b+beta*eta[:,0,None]
 ez=np.einsum('pa,jpa->jp',eta,z);zeta=np.zeros_like(z);zeta[:,:,0]=ez/U[None,:,0]
 dq=np.zeros((p,4,4,4));dq[:,:,0,0]=2*cj['dN']*f[:,None]+2*N[:,None]*df
 dq[:,:,0,0]+=2*np.einsum('pai,pij,pj->pa',cj['dbeta'],h,b)+2*np.einsum('pi,paij,pj->pa',beta,cj['dh'],b)+2*np.einsum('pi,pij,paj->pa',beta,h,db)
 dq[:,:,0,1:]=np.einsum('paij,pj->pai',cj['dh'],b)+np.einsum('pij,paj->pai',h,db);dq[:,:,1:,0]=dq[:,:,0,1:]
 deta=np.zeros((p,4,4));deta[:,:,0]=op['du'][:,:,0]*f[:,None]/N[:,None]+U[:,0,None]*df/N[:,None]+U[:,0,None]*f[:,None]*cj['dN']/N[:,None]**2
 deta[:,:,1:]=op['du'][:,:,0,None]*b[:,None,:]+U[:,0,None,None]*db+eta[:,0,None,None]*cj['dbeta']+beta[:,None,:]*deta[:,:,0,None]
 dez=np.einsum('pab,jpb->jpa',deta,z)+np.einsum('pb,jpab->jpa',eta,op['dz']);dzeta=np.zeros_like(op['dz'])
 dzeta[:,:,:,0]=dez/U[None,:,0,None]+ez[:,:,None]*op['du'][None,:,:,0]/U[None,:,0,None]**2
 return normal_positive_save(label,dict(q=q,dq=dq,eta=eta,deta=deta,zeta=zeta,dzeta=dzeta),keep)

def normal_positive_direction(s,c,op,features,curvature,f,df,b,db,keep,label):
 U,z,g,hi=abs(s['U']),abs(s['z']),abs(s['g']),abs(s['hi']);P=features['P'];w=abs(s['w']);om=s['omega'][:,None]**2;kj=(B*GC)**2*s['xi'][:,None]**4
 cj=normal_positive_chart_jets(s,c,op,keep,label+'_chart');lift=normal_positive_lift(s,c,op,cj,f,df,b,db,keep,label+'_lift')
 q,eta=lift['q'],lift['eta'];nq=lift['dq']+np.einsum('plam,pln->pamn',op['Ga'],q)+np.einsum('plan,pml->pamn',op['Ga'],q)
 dG=connection_from_jet_envelope(hi,nq);dnu=lift['deta']+np.einsum('pbal,pl->pab',dG,U)+np.einsum('pbal,pl->pab',op['Ga'],eta)
 dnz=np.einsum('plab,jpl->jpab',dG,z);duc=np.einsum('pab,pb->pa',q,U)+np.einsum('pab,pb->pa',g,eta)
 dP=duc[:,:,None]*U[:,None,:]+features['uc'][:,:,None]*eta[:,None,:];dqq=np.einsum('pa,jpab->jpb',eta,features['nz'])+np.einsum('pa,jpab->jpb',U,dnz)
 dV=np.einsum('pab,jpb->jpa',dP,features['q'])+np.einsum('pab,jpb->jpa',P,dqq)
 dD=np.einsum('pac,jpcd,pbd->jpab',dP,features['nz'],P)+np.einsum('pac,jpcd,pbd->jpab',P,dnz,P)+np.einsum('pac,jpcd,pbd->jpab',P,features['nz'],dP)
 lower=np.einsum('pab,pcb->pca',q,features['nu'])+np.einsum('pab,pcb->pca',g,dnu);dF=lower+lower.swapaxes(1,2)
 da=np.einsum('pa,pab->pb',eta,features['nu'])+np.einsum('pa,pab->pb',U,dnu);dhi=np.einsum('pac,pcd,pdb->pab',hi,q,hi)
 dr=np.einsum('pab,pb->pa',dP,abs(s['phi']));lm=np.einsum('pab,pba->p',hi,q)/2
 normal_positive_save(label+'_metric_delta',dict(deltaG=dG,dnu=dnu,dnz=dnz,dP=dP,dV=dV,dD=dD,dF=dF,da=da,dhi=dhi,dr=dr,log_measure=lm),keep)
 V,D,F=features['V'],features['D'],features['F'];Vu,Du,Fu=features['V_raised'],features['D_raised'],features['Fup'];z2=features['z2'];r=features['r']
 V2=np.sum(Vu*V,axis=2);D2=np.sum(Du*D,axis=(2,3));F2=np.sum(Fu*F,axis=(1,2));az=np.einsum('pa,jpa->jp',features['a'],z)
 dz2=np.einsum('jpa,pab,jpb->jp',z,dhi,z);dV2=np.einsum('jpa,pab,jpb->jp',V,dhi,V)+2*np.sum(Vu*dV,axis=2)
 dD2=2*np.sum(Du*dD,axis=(2,3));dF2=2*np.sum(Fu*dF,axis=(1,2))
 for A0,A1 in ((dhi,hi),(hi,dhi)):
  dD2+=np.einsum('pac,jpab,pbd,jpcd->jp',A0,D,A1,D);dF2+=np.einsum('pac,pab,pbd,pcd->p',A0,F,A1,F)
 r2=np.einsum('pa,pab,pb->p',r,hi,r);dr2=np.einsum('pa,pab,pb->p',r,dhi,r)+2*np.einsum('pa,pab,pb->p',r,hi,dr)
 modal=np.stack((V2/(2*om),z2/2,z2*z2/(4*kj),ELL**2*D2/2,az),axis=-1)
 dmodal=np.stack((dV2/(2*om),dz2/2,z2*dz2/(2*kj),ELL**2*dD2/2,np.einsum('pa,jpa->jp',da,z)),axis=-1)
 primal=np.column_stack((abs(ALPHA)*F2/4,r2/2,np.einsum('j,jpk->pk',w,modal)));variation=np.column_stack((abs(ALPHA)*dF2/4,dr2/2,np.einsum('j,jpk->pk',w,dmodal)));native=variation+lm[:,None]*primal
 zeta=lift['zeta'];nzeta=lift['dzeta']+np.einsum('plab,jpl->jpab',op['Ga'],zeta);qq=np.einsum('pa,jpab->jpb',U,nzeta)
 vv=np.einsum('pab,jpb->jpa',P,qq);dd=np.einsum('pac,jpcd,pbd->jpab',P,nzeta,P);zz=np.einsum('jpa,pab,jpb->jp',z,hi,zeta)
 zm=np.stack((np.sum(Vu*vv,axis=2)/om,zz,z2*zz/kj,ELL**2*np.sum(Du*dd,axis=(2,3)),np.einsum('pa,jpa->jp',features['a'],zeta)),axis=-1)
 mode=np.column_stack((np.zeros((len(U),2)),np.einsum('j,jpk->pk',w,zm)))
 dX=np.einsum('pa,pab,pb->p',abs(s['phi']),dhi,abs(s['phi']))/(2*abs(s['phase_X']));phase=np.column_stack((abs(s['phase_PX'])*dX,abs(s['phase_P'])*lm))
 f,df,b,db=abs(f),abs(df),abs(b),abs(db);K,kt,pi=features['K'],features['Ktrace'],features['metric_EH_tensor'];ih=abs(c['ih'])
 curvature_term=(f*curvature['envelope_Q']+np.einsum('pi,pi->p',df[:,1:],curvature['envelope_V']))/(2*abs(C))
 kinetic=f*abs(c['sqrt_h'])*(kt**2+np.einsum('pij,pik,pkl,plj->p',K,ih,K,ih))/(2*abs(C))
 Lie=np.einsum('pi,pijk->pjk',b,cj['dh'][:,1:])+np.einsum('pik,pjk->pij',abs(c['h']),db[:,1:])+np.einsum('pkj,pik->pij',abs(c['h']),db[:,1:])
 EH=np.column_stack((curvature_term,kinetic,np.einsum('pij,pij->p',pi,Lie)))
 components=np.column_stack((abs(c['dens'])*native.sum(axis=1),abs(c['dens'])*mode.sum(axis=1),abs(c['dens'])*phase.sum(axis=1),EH.sum(axis=1)))
 return normal_positive_save(label,dict(native_metric_terms=native,mode_compensation_terms=mode,absolute_phase_terms=phase,EH_terms=EH,component_densities=components,coefficient=components.sum(axis=1)),keep)

def normal_positive_primary(s,c,features,keep,label):
 U,z,h,beta,N=abs(s['U']),abs(s['z']),abs(c['h']),abs(c['beta']),abs(c['N']);p=len(U);out=np.zeros((p,4))
 for row in range(4):
  q=np.zeros((p,4,4));eta=np.zeros((p,4))
  if row==0:q[:,0,0]=2*N;eta[:,0]=U[:,0]/N;eta[:,1:]=beta*eta[:,0,None]
  else:
   i=row-1;q[:,0,0]=2*np.einsum('pi,pi->p',beta,h[:,:,i]);q[:,0,1:]=h[:,:,i];q[:,1:,0]=q[:,0,1:];eta[:,i+1]=U[:,0]
  zeta=np.einsum('pa,jpa->jp',eta,z)/U[None,:,0]
  out[:,row]=abs(c['dens'])*(np.einsum('pab,pab->p',features['connection_momentum'][:,0],q)+np.einsum('pa,pa->p',features['PiU'][:,0],eta)+np.einsum('jp,jp->p',features['Pi'][:,:,0,0],zeta))
  keep(label+'_partial',out)
 return normal_positive_save(label,dict(primary=out),keep)['primary']

# Definitions only; caller supplies path,sha,resolve_record,read_pair,json,PINS.
# Stream saved pilot primitives. This adapter does not recompute any first jet/feature.
NORMAL_PILOT_STEM='CROSS_U_PAIRED_CURRENT_PRIMITIVE_MOMENTUM_READOUT_V002'
NORMAL_PILOT_TERMINAL={'pid': 50104, 'protocol_sha256': '0ccd71e96ff40c8105256fd9cce17b68ff06ad0292a726bd1ecac458d8bff30a', 'receipt_sha256': '293295534b3c32ea152641ee4bd54b4cf224a171e3de9e14f2833759787eadaa', 'result_sha256': '7289a181e37a8f3277dfc7a587f09bf9078e1d20381eb0c0c371aac2511203be', 'source_sha256': 'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19'}
NORMAL_PILOT_READER={'file': 'READONLY_PAIRED_PRIMITIVE_CLOSURE_V002_RESULT.json', 'sha256': '5c3eba7c11f65c6c9449325f24683c8f3fde04a55dd684729d759431c7e771cf', 'pid': 50596}
def paired_pilot_admission():
 t=NORMAL_PILOT_TERMINAL;a=NORMAL_PILOT_READER;assert all(v is not None for v in t.values()) and all(v is not None for v in a.values()),'Actual CLOSED pilot and earned saved checker required before I/O'
 pins={str(path(n).resolve()):h for n,h in PINS.items()}
 def bind(n,h):
  key=str(path(n).resolve());assert key not in pins or pins[key]==h;assert sha(path(n))==h,n;pins[key]=h
 for n,h in ((NORMAL_PILOT_STEM+'_RESULT.json',t['result_sha256']),(NORMAL_PILOT_STEM+'_RECEIPT.json',t['receipt_sha256']),('cross_u_paired_current_primitive_momentum_readout_v002.py',t['source_sha256']),(NORMAL_PILOT_STEM+'.md',t['protocol_sha256']),(a['file'],a['sha256'])):bind(n,h)
 result=json.loads(path(NORMAL_PILOT_STEM+'_RESULT.json').read_text());rc=json.loads(path(NORMAL_PILOT_STEM+'_RECEIPT.json').read_text());proof=json.loads(path(a['file']).read_text())
 assert rc['status']=='CLOSED' and rc['error_sha256'] is None and rc['result_sha256']==t['result_sha256'] and rc['owner']==result['owner'] and result['owner']['pid']==t['pid'] and result['owner']['source_sha256']==t['source_sha256']
 assert proof['status']=='SAVED_PAIRED_PRIMITIVE_CLOSURE_PASS' and proof['parent_terminal']==t and proof['pid']==a['pid'] and proof['controls']==18 and proof['committed_pairs']==7
 assert len(result['controls'])==18 and len(result['checkpoints'])==7 and all(c['passed'] is True for c in result['controls']) and all(v is False for v in result['qualification'].values()) and proof['qualification']==result['qualification']
 case=result['case'];admitted=case['canonical_primitive_readout_admitted'];assert proof['canonical_primitive_readout_admitted']==admitted and proof['parent_status']==result['status']
 assert result['status']==('CURRENT_PRIMITIVE_CANONICAL_READOUT_ADMITTED' if admitted else 'CURRENT_PRIMITIVE_CANONICAL_READOUT_MISMATCH') and case['frozen_canonical_admission_preserved'] is True and case['physical_adoption'] is False
 def rec(ref,mapping):
  r=resolve_record(ref)
  for n,h in ((r['file'],r['sha256']),(r['commit_file'],r['commit_sha256'])):assert mapping[n if n in mapping else str(path(n).resolve())]==h;bind(n,h)
  return r
 refs=[rec(r,rc['output_sha256']) for r in result['checkpoints']];assert case['columns']==refs[2:6] and case['readout']==refs[-1]
 for i,r in enumerate(refs[2:6]):assert r['metadata']['column']==i and r['metadata']['source_configuration_changed'] is False and r['metadata']['rate_word_collapse_adopted'] is False
 fixed=refs[0]['metadata']['fixed'];assert fixed['eps']==1e-5 and fixed['Q0_over_Hstar']==100
 cpname='CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_EPS_1em05_CP.json';bind(cpname,rc['input_sha256'][str(path(cpname).resolve())]);cp=json.loads(path(cpname).read_text());assert cp['background']==refs[0]['metadata']['owned_background']
 force_name='CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V003_RESULT.json';bind(force_name,'981a314d7ca598c101db34d4da6f36679c752da81d8cc1325c521f4ce0c7b770');force=json.loads(path(force_name).read_text());assert force['owner']['pid']==36387 and force['cases'][0]['sigma']==1.
 ordinary=rec(force['cases'][0]['loads'],rc['input_sha256'])
 pilot=dict(result,input=refs[0],basis=refs[1],columns=refs[2:6],readout=refs[-1],ordinary_loads=ordinary,saved_reader=proof,primitive_bridge_admitted=admitted,conditional_normal_diagnostic=True,physical_adoption=False)
 return pins,pilot,fixed,cp

def load_pilot_column(ref):
 rec=resolve_record(ref);assert rec['metadata']['owner']['pid']==NORMAL_PILOT_TERMINAL['pid'] and rec['metadata']['kind']=='new_paired_current_primitives_and_affine_canonical_momenta'
 schema=rec['metadata']['schema'];skip={'feature_du_hi','feature_du_lo','feature_dz_hi','feature_dz_lo','feature_Ga_hi','feature_Ga_lo'}
 names=tuple(n for n in schema if n not in skip and (n.startswith(('config_','chart_','first_jet_','feature_','momentum_','operation_','native_rate_','metric_rate_','unchanged_new_phase_')) or n in ('seed_owned_coordinate_Ndot','seed_owned_coordinate_betadot')))
 for n in names:
  if n.endswith(('_hi','_lo')):assert n[:-3]+('_lo' if n.endswith('_hi') else '_hi') in names,'Both words mandatory'
 raw=read_pair(rec,names);s={n.removeprefix('config_'):v for n,v in raw.items() if n.startswith('config_')}
 # These copied chart time/momentum witnesses remain old; current values are paired below.
 old={'K','Ktrace','pi_EH','p_native','p_metric_native','old_velocity'};c={n.removeprefix('chart_'):v for n,v in raw.items() if n.startswith('chart_') and n.removeprefix('chart_') not in old}
 def paired(prefix):
  return {n[len(prefix):-3]:(raw[n],raw[n[:-3]+'_lo']) for n in names if n.startswith(prefix) and n.endswith('_hi')}
 jets=paired('first_jet_');feature=dict(constants=s,paired=paired('feature_'),configuration_changed=False);moments=paired('momentum_');op={n.removeprefix('operation_'):v for n,v in raw.items() if n.startswith('operation_')}
 assert set(jets)=={'du','dz','dg','Ga'} and set(op)=={'du','dz','dg','Ga'}
 return s,c,jets,feature,moments,op,raw

def normal_scratch(name,a):
 # Current direction only. Compact completed directions live under other keys.
 return capture('active_direction_'+name,a)

def clear_normal_scratch():
 for name in tuple(AVAILABLE):
  if name.startswith('active_direction_'):del AVAILABLE[name]

def normal_primary_pair(s,c,feature,moments):
 U,z,h,beta,N=s['U'],s['z'],c['h'],c['beta'],c['N'];p=len(U);rows=[]
 for row in range(4):
  q=np.zeros((p,4,4));eta=np.zeros((p,4))
  if row==0:q[:,0,0]=-2*N;eta[:,0]=-U[:,0]/N;eta[:,1:]=-beta*eta[:,0,None]
  else:
   i=row-1;q[:,0,0]=2*np.einsum('pi,pi->p',beta,h[:,:,i]);q[:,0,1:]=h[:,:,i];q[:,1:,0]=q[:,0,1:];eta[:,i+1]=-U[:,0]
  zeta=-np.einsum('pa,jpa->jp',eta,z)/U[None,:,0]
  metric=normal_action_reduce(a_mul64(q,a_slice(moments['connection_momentum'],(slice(None),0,slice(None),slice(None)))),(1,2))
  native=normal_pair_sum(a_mul64(eta,a_slice(feature['paired']['PiU'],(slice(None),0,slice(None)))),1)
  mode=normal_pair_sum(a_mul64(zeta,a_slice(feature['paired']['Pi'],(slice(None),slice(None),0,0))),0)
  value=a_mul64(c['dens'],a_add(a_add(metric,native),mode));normal_keep_pair('primary_completed_'+str(row),value,capture);rows.append(value)
 return a_stack(rows,axis=1)

def paired_normal_column(iq,ref,Hbar):
 global RAW,AVAILABLE
 RAW={};AVAILABLE={};CONTEXT.update(stage='saved_pilot_to_paired_normal_coefficients',column=iq);start=len(CHECKS)
 s,c,jets,feature,moments,op,raw=load_pilot_column(ref)
 # Shape aliases only: every derivative-dependent contraction consumes jets pairs.
 s['du']=jets['du'][0];s['dz']=jets['dz'][0]
 s['metric_partial_envelope']=op['dg'];s['connection_envelope']=op['Ga']
 assert np.all(jets['dg'][1][:,1:]==0),'Fixed spatial metric configuration must retain zero rate-induced low jet'
 cj_fixed=dict(dh=jets['dg'][0][:,:,1:,1:])
 curvature=current_reference_curvature(s,c,cj_fixed)
 RAW={};AVAILABLE={};CONTEXT.update(stage='sixteen_paired_normal_directions',column=iq)
 for n,a in curvature.items():capture('completed_curvature_'+n,a)
 positive=normal_positive_features(s,c,op,normal_scratch,'positive_features')
 p=len(s['U']);coeff=a_dd(np.zeros((p,4,4)));components=a_dd(np.zeros((p,4,4,4)));env=np.zeros((p,4,4));ce=np.zeros((p,4,4,4))
 termshapes=dict(native_metric_terms=7,mode_compensation_terms=7,absolute_phase_terms=2,EH_terms=3)
 terms={n:a_dd(np.zeros((p,4,4,m))) for n,m in termshapes.items()};te={n:np.zeros((p,4,4,m)) for n,m in termshapes.items()}
 for row in range(4):
  for jet,axis in enumerate((None,1,2,0)):
   clear_normal_scratch();CONTEXT.update(row=row,jet=jet,axis=axis)
   f=np.zeros(p);df=np.zeros((p,4));b=np.zeros((p,3));db=np.zeros((p,4,3))
   if row==0:
    if axis is None:f[:]=1
    else:df[:,axis]=1
   else:
    if axis is None:b[:,row-1]=1
    else:db[:,axis,row-1]=1
   label=f'direction_{row}_{jet}'
   result=paired_normal_direction(s,c,jets,feature,moments,curvature,f,df,b,db,normal_scratch,label)
   for wi in range(2):coeff[wi][:,row,jet]=result['coefficient'][wi];components[wi][:,row,jet]=result['component_densities'][wi]
   normal_keep_pair('completed_normal_coefficient',coeff,capture);normal_keep_pair('completed_normal_components',components,capture)
   for n in terms:
    for wi in range(2):terms[n][wi][:,row,jet]=result[n][wi]
    normal_keep_pair('completed_'+n,terms[n],capture)
   bound=normal_positive_direction(s,c,op,positive,curvature,f,df,b,db,normal_scratch,label+'_positive')
   env[:,row,jet]=bound['coefficient'];ce[:,row,jet]=bound['component_densities'];capture('completed_normal_envelope',env);capture('completed_normal_component_envelope',ce)
   for n in te:te[n][:,row,jet]=bound[n];capture('completed_'+n+'_envelope',te[n])
 clear_normal_scratch();primary=normal_primary_pair(s,c,feature,moments);normal_keep_pair('completed_primary_signed',primary,capture)
 ep=normal_positive_primary(s,c,positive,normal_scratch,'primary_positive');capture('completed_primary_envelope',ep)
 time=a_slice(coeff,(slice(None),slice(None),3));difference=a_sub(time,primary);normal_keep_pair('completed_time_primary_difference',difference,capture)
 check('four_time_coefficients_equal_canonical_primary_column_'+str(iq),collapse(difference,'time_primary_difference'),np.zeros((p,4)),env[:,:,3]+ep)
 check('four_primary_gauge_momenta_vanish_column_'+str(iq),collapse(primary,'primary_zero_readout'),np.zeros((p,4)),ep)
 iso,ic,ie=current_EH_isotropic_shift_diagnostic(s,c,cj_fixed,Hbar)
 data=dict(normal_envelope=env,normal_component_envelope=ce,primary_operation_envelope=ep,EH_isotropic_diagnostic_momentum=iso,EH_isotropic_diagnostic_coefficient=ic,EH_isotropic_diagnostic_envelope=ie)
 for n,x in dict(normal_coefficient=coeff,normal_components=components,primary_signed=primary,time_primary_difference=difference,**terms).items():
  for wi,word in enumerate(('hi','lo')):data[n+'_'+word]=x[wi].copy()
 data.update({n+'_envelope':a for n,a in te.items()});data.update({'curvature_'+n:a for n,a in curvature.items()});data.update({n:a for n,a in RAW.items() if n.startswith('control_')})
 for n,a in data.items():finite_real('column_saved_'+n,a)
 assert len(CHECKS)-start==2
 rec=checkpoint('COLUMN',data,dict(kind='paired_same_action_sixteen_normal_test_coefficients',column=iq,sigma=SIGMA,pilot_parent=ref,rows=['lapse','shift_R','shift_Z','shift_phi'],jet_order=['value','R','Z','time'],components=['native_metric','mode_z0_compensation','absolute_phase','EH_ADM_reference_curvature'],controls=CHECKS[start:],source_configuration_changed=False,primitive_momentum_replayed=False,rate_word_collapse_adopted=False,temporal_improvement_ports=None,physical_outer_GHY=None,sheet_traction=None,physical_gauge_time_jets=None,exterior=None))
 return dict(coefficient=coeff,components=components,envelope=env,component_envelope=ce,iso=ic,iso_envelope=ie),rec

def paired_restrict_normal_rows(x):
 hi,lo=x[0].copy(),x[1].copy();joined=a_add((hi[:,1],lo[:,1]),(hi[:,0],lo[:,0]));hi[:,1]=joined[0];lo[:,1]=joined[1]
 hi[:,0]=lo[:,0]=0;hi[:,-1]=lo[:,-1]=0;hi[:,:,-1]=lo[:,:,-1]=0;hi[2,:,0]=lo[2,:,0]=0
 return hi,lo

def paired_scatter_normal(coeff,geo,label):
 assert coeff[0].shape==coeff[1].shape==(15136,4,3)
 out=a_dd(np.zeros((4,87,45)));normal_keep_pair(label+'_start',out,capture)
 for iq in range(4):
  sl=slice(iq*3784,(iq+1)*3784);weight=(geo['dv'][iq]/geo['R'][iq]).reshape(86,44)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   for row in range(4):
    value=a_dd(np.zeros((86,44)))
    for jet,hat in enumerate(normal_hat_jet(geo,iq,corner,row)):
     value=a_add(value,a_mul64(hat,a_reshape(a_slice(coeff,(sl,row,jet)),(86,44))));normal_keep_pair(label+'_corner_value',value,capture)
    value=a_mul64(weight,value);normal_keep_pair(label+'_weighted_corner_value',value,capture)
    idx=(row,slice(di,86+di),slice(dj,44+dj));joined=a_add(a_slice(out,idx),value);out[0][idx]=joined[0];out[1][idx]=joined[1];normal_keep_pair(label+'_partial',out,capture)
 out=paired_restrict_normal_rows(out);return normal_keep_pair(label+'_restricted',out,capture)

def paired_ordinary_normal(source,gamma):
 R,Z,mass,p,indices,t=(source[n] for n in ('source_R','source_Z','source_mass_weight','source_specific_covariant_p','source_indices','source_right_weight'))
 assert gamma.shape==R.shape and p.shape==(len(R),3) and np.all(gamma>=1) and np.all(mass>=0)
 assert indices.dtype.kind=='i' and np.all((indices>=0)&(indices<86)) and np.all((t>=0)&(t<=1)) and np.all(Z==0)
 force=a_mul64(mass[:,None],a_dd(np.column_stack((gamma,-p))));normal_keep_pair('ordinary_point_force',force,capture)
 out=a_dd(np.zeros((4,87,45)));envelope=np.zeros((4,87,45))
 for side,hat in ((0,1-t),(1,t)):
  for row in range(4):
   scale=R if row==1 else np.ones_like(R);value=a_mul64(hat,a_mul64(scale,a_slice(force,(slice(None),row))));normal_keep_pair('ordinary_point_basis_value',value,capture)
   ev=mass*abs(np.column_stack((gamma,-p))[:,row])*abs(scale)*abs(hat)
   for node in range(87):
    take=np.flatnonzero(indices+side==node)
    if len(take):
     subtotal=normal_pair_sum((value[0][take],value[1][take]),0);joined=a_add((out[0][row,node,0],out[1][row,node,0]),subtotal);out[0][row,node,0]=joined[0];out[1][row,node,0]=joined[1];envelope[row,node,0]+=np.sum(ev[take])
     normal_keep_pair('ordinary_nodal_partial',out,capture);capture('ordinary_nodal_envelope_partial',envelope)
 out=paired_restrict_normal_rows(out);envelope=restrict_normal_rows(envelope);normal_keep_pair('ordinary_nodal_rows',out,capture);capture('ordinary_nodal_envelope',envelope)
 return out,envelope,force

def fresh_normal_pair_fixtures():
 R=np.array((3.,));one=np.ones(1);h=np.diag((1.,1.,9.))[None];ih=np.diag((1.,1.,1/9))[None]
 dh=np.zeros((1,4,3,3));dh[:,1,2,2]=2*R;bar=np.zeros((1,3,3,3));bar[:,0,2,2]=-R;bar[:,2,0,2]=bar[:,2,2,0]=1/R
 def fixture_curvature(hh,iih,sh,dhh,G3,label):
  g=np.zeros((1,4,4));g[:,0,0]=-1;g[:,1:,1:]=hh;Ga=np.zeros((1,4,4,4));Ga[:,1:,1:,1:]=G3
  product=np.einsum('plam,pln->pamn',abs(Ga),abs(g));edg=product+product.swapaxes(2,3)
  s=dict(R=R,metric_partial_envelope=edg);c=dict(h=hh,ih=iih,sqrt_h=sh)
  result=current_reference_curvature(s,c,dict(dh=dhh));data={label+'_'+n:a.copy() for n,a in result.items()};RAW.update(data);return result,data
 flat,data=fixture_curvature(h,ih,R,dh,bar,'flat')
 check('fresh_flat_cylindrical_reference_Q_V',np.column_stack((flat['Q'],flat['V'])),np.zeros((1,4)),np.column_stack((flat['envelope_Q'],flat['envelope_V'])))
 ph=5/4;l=np.array((2/7,-1/5,0.));hc=ph**4*h;ihc=ih/ph**4;dhc=ph**4*dh;G3=bar.copy()
 for a in range(3):
  dhc[:,a+1]+=4*l[a]*hc
  for i in range(3):
   for j in range(3):
    for k in range(3):G3[:,k,i,j]+=2*((1 if k==i else 0)*l[j]+(1 if k==j else 0)*l[i]-h[:,i,j]*ih[:,k,k]*l[k])
 curved,more=fixture_curvature(hc,ihc,ph**6*R,dhc,G3,'conformal');data.update(more)
 target=np.column_stack((8*R*ph**2*np.sum(l*l),-8*R[:,None]*ph**2*l[None]))
 check('fresh_conformal_cylindrical_reference_Q_V',np.column_stack((curved['Q'],curved['V'])),target,np.column_stack((curved['envelope_Q'],curved['envelope_V']))+abs(target))
 eps=2.**-30;kh=np.diag((1.,-2.,3.))[None];kl=eps*np.diag((2.,1.,-1.))[None]
 c=dict(ih=np.eye(3)[None],h=np.eye(3)[None],sqrt_h=one);cj=dict(dh=a_dd(np.zeros((1,4,3,3))));m=dict(K=(kh,kl),Ktrace=(np.array((2.,)),np.array((2*eps,))),metric_EH_tensor=a_dd(np.zeros((1,3,3))))
 eh=paired_normal_EH_terms({},c,cj,m,dict(Q=np.zeros(1),V=np.zeros((1,3))),one,np.zeros((1,4)),np.zeros((1,3)),np.zeros((1,4,3)),capture,'fresh_EH_polarization')
 restored=a_mul64(2*C,a_slice(eh,(slice(None),1)));cross=a_add(a_dd(np.array((-10.,))),a_dd(np.array((14*eps,))));low=a_sub(restored,cross);normal_keep_pair('fresh_EH_restored_numerator',restored,capture);normal_keep_pair('fresh_EH_isolated_low_low',low,capture)
 check('fresh_EH_high_low_and_low_low_polarization',collapse(low,'fresh_EH_low_low_readout'),np.array((-2*eps**2,)),np.array((2*eps**2,)))
 data.update(EH_K_hi=kh,EH_K_lo=kl,EH_terms_hi=eh[0],EH_terms_lo=eh[1],EH_restored_numerator_hi=restored[0],EH_restored_numerator_lo=restored[1],EH_low_low_hi=low[0],EH_low_low_lo=low[1]);data.update({n:a for n,a in RAW.items() if n.startswith('control_')});return data

def paired_normal_loads(columns,source,gamma,geo,readout,Hbar):
 global RAW,AVAILABLE
 RAW={};AVAILABLE={};CONTEXT.update(stage='paired_genuine_weak_normal_rows');start=len(CHECKS)
 coeff=tuple(np.concatenate([x['coefficient'][wi] for x in columns]) for wi in range(2));components=tuple(np.concatenate([x['components'][wi] for x in columns]) for wi in range(2));env=np.concatenate([x['envelope'] for x in columns]);ce=np.concatenate([x['component_envelope'] for x in columns])
 action=paired_scatter_normal(a_slice(coeff,(slice(None),slice(None),slice(0,3))),geo,'full_normal_action');action_env=scatter_normal_envelope(env[:,:,:3],geo);capture('full_normal_action_envelope',action_env)
 ordinary,ordinary_env,force=paired_ordinary_normal(source,gamma);ham=a_add((-action[0],-action[1]),ordinary);normal_keep_pair('full_Hamiltonian_normal_rows',ham,capture)
 test=(np.arange(4*87*45)%13-6).reshape(4,87,45)/37.;test*=normal_test_mask();testjet=evaluate_normal_test(test,geo);capture('functional_nodal_test',test);capture('functional_qpoint_test',testjet)
 nodal=normal_action_reduce(a_mul64(test,action),(0,1,2));weight=(geo['dv']/geo['R']).reshape(15136)
 point=a_mul64(weight[:,None,None],a_mul64(testjet,a_slice(coeff,(slice(None),slice(None),slice(0,3)))));point=a_reshape(point,(4,86,44,4,3));direct=normal_action_reduce(point,(0,1,2,3,4));normal_keep_pair('functional_nodal_pair',nodal,capture);normal_keep_pair('functional_direct_pair',direct,capture)
 difference=a_sub(nodal,direct);normal_keep_pair('functional_difference_pair',difference,capture)
 ep=float(np.sum(weight[:,None,None]*abs(testjet)*env[:,:,:3])+np.sum(abs(test)*action_env))
 check('paired_normal_Q1_functional_incidence',np.array((float(collapse(difference,'functional_difference')),)),np.zeros(1),np.array((ep,)))
 fields=[]
 for ci in range(4):
  value=paired_scatter_normal(a_slice(components,(slice(None),slice(None),slice(0,3),ci)),geo,'component_'+str(ci));fields.append((-value[0],-value[1]))
 fields.append(ordinary);component_rows=a_stack(fields,axis=-1);normal_keep_pair('full_Hamiltonian_component_rows',component_rows,capture)
 iso=np.concatenate([x['iso'] for x in columns]);isoenv=np.concatenate([x['iso_envelope'] for x in columns]);isopair=paired_scatter_normal(a_dd(iso),geo,'analytical_isotropic_raw_alias');fullEH=a_slice(component_rows,(slice(None),slice(None),slice(None),3));isoH=(-isopair[0],-isopair[1]);remainder=a_sub(fullEH,isoH)
 normal_keep_pair('EH_isotropic_Hamiltonian_alias',isoH,capture);normal_keep_pair('EH_full_minus_isotropic_remainder',remainder,capture)
 data=dict(normal_action_envelope=action_env,normal_Hamiltonian_envelope=action_env+ordinary_env,ordinary_envelope=ordinary_env,ordinary_gamma=gamma,ordinary_input_source_indices=source['source_indices'],functional_nodal_test=test,functional_qpoint_test=testjet,functional_operation_envelope=np.array((ep,)),EH_isotropic_operation_envelope=scatter_normal_envelope(isoenv,geo))
 pairs=dict(normal_action=action,normal_Hamiltonian_rows=ham,normal_Hamiltonian_components=component_rows,ordinary_Hamiltonian_rows=ordinary,ordinary_point_force=force,functional_nodal=nodal,functional_direct=direct,functional_difference=difference,EH_isotropic_Hamiltonian_alias=isoH,EH_full_minus_isotropic_remainder=remainder)
 for n,x in pairs.items():
  for wi,word in enumerate(('hi','lo')):data[n+'_'+word]=np.asarray(x[wi]).copy()
 # Original bridge/offset/RHS defects are copied, never refitted or replayed.
 for n,a in readout.items():data['pilot_saved_readout_'+n]=a.copy()
 data.update({n:a for n,a in RAW.items() if n.startswith('control_')})
 assert len(CHECKS)-start==1
 rec=checkpoint('LOADS',data,dict(kind='conditional_four_same_action_weak_normal_constraints',rows=['lapse','shift_R','shift_Z','shift_phi'],normal_dof=14875,ordinary_labels_counted_once=True,halfspace_measure='coordinate_density_times_reference_volume_over_R_once',full_EH_authoritative=True,isotropic_alias_subtracted=False,analytical_continuum_isotropic_divergence_zero_only_for_compact_continuous_tests=True,primitive_readout_recomputed=False,pointwise_CMC_admitted=False,Hbar_diagnostic=Hbar,unknown_ports=dict(temporal_improvement=None,outer_GHY=None,sheet_traction=None,physical_gauge_time_jets=None,exterior=None,activity_outside_saved_grid=None),controls=CHECKS[start:]))
 return rec

def paired_normal_packet(pilot,fixed,cp):
 global RAW,AVAILABLE,B
 B=1.0059833281731022e-10*3.085677581491367e19/299792458.**2
 inp=read_pair(pilot['input'],('r_kpc','z_kpc','xi','weights'));RAW={};AVAILABLE={}
 checkpoint('INPUT',inp,dict(kind='closed_paired_pilot_conditional_normal_inputs',fixed=fixed,owned_background=cp['background'],pilot_input=pilot['input'],pilot_columns=pilot['columns'],pilot_readout=pilot['readout'],pilot_saved_checker=NORMAL_PILOT_READER,primitive_bridge_admitted=pilot['primitive_bridge_admitted'],conditional_normal_diagnostic=True,physical_history=None))
 fixtures=fresh_normal_pair_fixtures();checkpoint('FIXTURE',fixtures,dict(kind='three_fresh_reference_curvature_and_paired_EH_controls',controls=CHECKS.copy(),physical_parameters=False))
 geo=read_pair(pilot['basis'],('R','dv','hats','cell_i','cell_j','r','z'));assert geo['R'].shape==geo['dv'].shape==(4,3784) and geo['hats'].shape==(4,4,3,86,44) and np.all(geo['R']>0) and np.all(geo['dv']>0)
 assert np.array_equal(geo['r'],inp['r_kpc']) and np.array_equal(geo['z'],inp['z_kpc'])
 checkpoint('BASIS',geo,dict(kind='unchanged_regular_normal_Q1_test_basis',parent=pilot['basis'],normal_dof=14875,outer_test_zero_is_not_physical_boundary=True,axis_even_coefficients=True,radial_shift_R_power=1,vertical_shift_sheet_odd=True))
 Hbar=cp['background']['H_over_Hstar']*fixed['Hunit']/299792458.;columns=[];refs=[]
 for iq,ref in enumerate(pilot['columns']):
  column,record=paired_normal_column(iq,ref,Hbar);columns.append(column);refs.append(record)
 RAW={};AVAILABLE={};CONTEXT.update(stage='saved_ordinary_and_bridge_load')
 oref=pilot['ordinary_loads'];names=tuple(n for n in oref['metadata']['schema'] if n.startswith('ordinary_input_source_'))+('ordinary_gamma',);loaded=read_pair(oref,names)
 source={n.removeprefix('ordinary_input_'):a for n,a in loaded.items() if n.startswith('ordinary_input_source_')};gamma=loaded['ordinary_gamma']
 rr=pilot['readout'];rnames=tuple(n for n in rr['metadata']['schema'] if not n.startswith('control_'));readout=read_pair(rr,rnames)
 loads=paired_normal_loads(columns,source,gamma,geo,readout,Hbar)
 assert len(CHECKS)==12 and len(RECORDS)==8 and all(row['passed'] for row in CHECKS)
 return dict(status='CONDITIONAL_PAIRED_NORMAL_CONSTRAINTS_MEASURED',columns=refs,loads=loads,pilot_result_sha256=NORMAL_PILOT_TERMINAL['result_sha256'],primitive_canonical_readout_admitted=pilot['primitive_bridge_admitted'],original_affine_readout_ratios=pilot['case']['original_affine_and_actual_target_ratios'],bridge_ratios=pilot['case']['bridge_rhs_and_target_ratios'],frozen_canonical_admission_preserved=True,finite_Legendre_stationarity_remainder_retained=True,physical_adoption=False,normal_constraint_solution=False)

def main():
 global np,OWNER,INPUTS,RAW,AVAILABLE
 ap=argparse.ArgumentParser();ap.add_argument('--root-run',action='store_true');args=ap.parse_args()
 if AUTHOR_DRAFT or AUTHORING_IN_PROGRESS or not args.root_run:raise SystemExit('Guarded paired normal measurement: root release after full review required.')
 assert PROTOCOL_SHA and sha(path(STEM+'.md'))==PROTOCOL_SHA;assert not list(BASE.glob(STEM+'_*')),'Unused runtime namespace required'
 INPUTS,pilot,fixed,cp=paired_pilot_admission();INPUTS[str(path(STEM+'.md').resolve())]=PROTOCOL_SHA;INPUTS[str(Path(__file__).resolve())]=sha(__file__)
 OWNER=dict(owner='root',pid=os.getpid(),started=now(),source_sha256=sha(__file__))
 try:
  json_file(STEM+'_OWNER_START.json',OWNER);json_file(STEM+'_MANIFEST.json',dict(owner=OWNER,input_sha256=INPUTS,scope='new paired same-action normal coefficients from sealed pilot, conditional finite Legendre remainder',controls=12,pairs=8,qualification=FLAGS))
  import numpy as _np
  np=_np
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=paired_normal_packet(pilot,fixed,cp)
  recheck();rh=json_file(STEM+'_RESULT.json',dict(owner=OWNER,status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));recheck()
  json_file(STEM+'_RECEIPT.json',dict(owner=OWNER,status='CLOSED',closed=now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));recheck();print(case['status'],len(CHECKS),len(RECORDS),rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None;available=dict(AVAILABLE);available.update(RAW);available.update({'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()})
  if np is not None and available:
   try:checkpoint('ERROR_RAW',available,dict(kind='available_unqualified_normal_direction_or_assembly_operands',context=dict(CONTEXT)),failed=True)
   except BaseException:raw_error=traceback.format_exc()
  try:seal_actual();recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=json_file(STEM+'_ERROR.json',dict(owner=OWNER,status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,preserved_outputs=dict(OUTPUTS),qualification=FLAGS))
  prior=path(STEM+'_RECEIPT.json');rn=STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json');json_file(rn,dict(prior_receipt_sha256=sha(prior) if prior.exists() else None,owner=OWNER,status='CLOSED_ERROR',closed=now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),error_sha256=eh,qualification=FLAGS));seal_actual();recheck(False);raise

if __name__=='__main__':raise SystemExit(main())

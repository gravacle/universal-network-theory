"""Guarded current two-word first-jet/primitive canonical momentum readout."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,math,os,sys,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_PAIRED_CURRENT_PRIMITIVE_MOMENTUM_READOUT_V002'
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='62fda77850accc5fc2057cb6c4d506d364b16e2c49c0d98c5359f0e05f83ead8'
BAND='CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001'
SIGMA=1.;C=1.98;KB=.02;ALPHA=KB/C;ELL=.1;GC=3*math.pi/8
B=None;TOL=2e-11;LINEAR_TOL=1e-10
np=None;OWNER=None;INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];RAW={};AVAILABLE={};CONTEXT={};DD_ARRAY_CURRENT={}
FLAGS=dict(primitive_canonical_physical_adoption=False,normal_constraints_qualified=False,CMC_preservation_qualified=False,evolution_qualified=False,physical_metric_qualified=False,source_history_qualified=False,exterior_qualified=False,galaxy_velocity_qualified=False)
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

def tensor_velocity_coordinates(hdot):
 return np.stack((hdot[...,0,0],hdot[...,1,1],hdot[...,2,2],hdot[...,0,1],hdot[...,0,2],hdot[...,1,2]),axis=-1)

def metric_basis():
 e=np.zeros((6,3,3))
 for k,(i,j) in enumerate(((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))):e[k,i,j]=e[k,j,i]=1
 return e

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

def velocity_operation_envelopes(s,c,y,k,chartenv):
 p=len(s['U']);y=abs(np.broadcast_to(y,(p,99)));k=abs(np.broadcast_to(k,(p,6)))
 e=abs(metric_basis());up=chartenv['up'];N,ga=c['N'],c['gamma']
 edga=np.einsum('pi,kij,pj->pk',up,e,up)/(2*ga[:,None])
 eUh=np.empty_like(c['Uh']);eUh[:,:,0]=edga/N[:,None]
 eUh[:,:,1:]=np.einsum('pij,kjl,pl->pki',abs(c['ih']),e,up)+abs(c['beta'])[:,None,:]*eUh[:,:,0,None]
 RAW['assembling_envelope_U_metric_chain']=eUh.copy()
 ezh=np.einsum('jpa,pka->jpk',abs(s['z']),eUh)/abs(s['U'][None,:,0,None])
 RAW['assembling_envelope_zt_metric_chain']=ezh.copy()
 embed=np.zeros_like(c['embed']);embed[:,:,1:,1:]=e[None]
 embed[:,:,0,1:]=np.einsum('kij,pj->pki',e,abs(c['beta']));embed[:,:,1:,0]=embed[:,:,0,1:]
 embed[:,:,0,0]=np.einsum('pi,kij,pj->pk',abs(c['beta']),e,abs(c['beta']))
 RAW['assembling_envelope_metric_embedding']=embed.copy()
 du=np.zeros((p,4,4));dz=np.zeros((32,p,4,4));dg=np.zeros((p,4,4,4))
 du[:,0]=np.einsum('pai,pi->pa',chartenv['JU'],y[:,:3])+np.einsum('pka,pk->pa',eUh,k)
 dz[:,:,0,1:]=y[:,3:].reshape(p,32,3).transpose(1,0,2)
 dz[:,:,0,0]=np.einsum('jpi,pi->jp',chartenv['JzU'],y[:,:3])+np.einsum('pi,jpi->jp',chartenv['Jzz'],dz[:,:,0,1:])+np.einsum('jpk,pk->jp',ezh,k)
 dg[:,0]=np.einsum('pk,pkab->pab',k,embed)
 RAW.update(assembling_envelope_du=du.copy(),assembling_envelope_dz=dz.copy(),assembling_envelope_dg=dg.copy())
 Ga=connection_from_jet_envelope(s['hi'],dg)
 RAW['assembling_envelope_delta_connection']=Ga.copy()
 nu=du+np.einsum('pbal,pl->pab',Ga,abs(s['U']))
 nz=dz+np.einsum('plab,jpl->jpab',Ga,abs(s['z']))
 RAW.update(assembling_envelope_nu=nu.copy(),assembling_envelope_nz=nz.copy())
 # P=I+U_cov outer U contains cancellation even when its physical00 entry is0.
 uc=np.einsum('pab,pb->pa',abs(s['g']),abs(s['U']))
 Pe=np.eye(4)[None]+np.einsum('pa,pb->pab',uc,abs(s['U']))
 RAW['assembling_envelope_projector']=Pe.copy()
 qq=np.einsum('pa,jpab->jpb',abs(s['U']),nz)
 V=np.einsum('pab,jpb->jpa',Pe,qq)
 D=np.einsum('pac,jpcd,pbd->jpab',Pe,nz,Pe)
 nuc=np.einsum('pab,pcb->pca',abs(s['g']),nu)
 F=nuc+np.swapaxes(nuc,1,2)
 RAW.update(assembling_envelope_F=F.copy(),assembling_envelope_V=V.copy(),assembling_envelope_D=D.copy())
 return dict(du=du,dz=dz,dg=dg,Gamma=Ga,nu=nu,nz=nz,projector=Pe,F=F,V=V,D=D)

def force_d0_column_shapes():
 p=3784;j=32;sh={}
 def add(prefix,rows):
  for n,a in rows.items():sh[prefix+n]=list(a)
 add('seed_',dict(g=(p,4,4),hi=(p,4,4),Ga=(p,4,4,4),U=(p,4),uc=(p,4),du=(p,4,4),z=(j,p,4),dz=(j,p,4,4),phi=(p,4),nu=(p,4,4),nz=(j,p,4,4),P=(p,4,4),q=(j,p,4),V=(j,p,4),D=(j,p,4,4),F=(p,4,4),Fup=(p,4,4),Pi=(j,p,4,4),PiU=(p,4,4),Z=(p,4),A=(p,4),mu=(j,p),a=(p,4),r=(p,4),f=(j,p),z2=(j,p),V_raised=(j,p,4),connection_Klo=(p,4,4,4),connection_momentum=(p,4,4,4),connection_D=(p,4,4,4),connection_Maxwell=(p,4,4,4),R=(p,),Z_coordinate=(p,),phase_P=(p,),phase_PX=(p,),phase_PXX=(p,),phase_X=(p,)))
 add('seed_chart_',dict(h=(p,3,3),ih=(p,3,3),N=(p,),beta=(p,3),u=(p,3),up=(p,3),gamma=(p,),JU=(p,4,3),JzU=(j,p,3),Jzz=(p,3),embed=(p,6,4,4),Uh=(p,6,4),zh=(j,p,6),dens=(p,),sqrt_h=(p,),old_velocity=(p,99),K=(p,3,3),Ktrace=(p,)))
 add('seed_chart_derivative_',dict(dg=(p,4,4,4),dhi=(p,4,4,4),dN=(p,4),dbeta=(p,4,3),dh=(p,4,3,3),dih=(p,4,3,3),du_cov=(p,4,3),dup=(p,4,3),dgamma=(p,4),dJU=(p,4,4,3),dJzU=(j,p,4,3),dJzz=(p,4,3),dUh=(p,4,6,4),dzh=(j,p,4,6),dembed=(p,4,6,4,4)))
 add('',dict(seed_nodal_native_rate=(p,99),seed_old_L2_native_rate=(p,99),seed_native_rate_delta=(p,99),seed_covariant_native_rate_R=(33,p,3),seed_covariant_native_rate_Z=(33,p,3),seed_metric_L2_rate=(p,3,3),seed_metric_L2_rate_R=(p,3,3),seed_metric_L2_rate_Z=(p,3,3),seed_owned_coordinate_Ndot=(p,),seed_owned_coordinate_betadot=(p,3),new_native_momentum=(p,99),new_metric_native_momentum=(p,6),new_metric_EH_momentum=(p,3,3),new_metric_total_momentum=(p,6),new_phase_current=(p,4),new_phase_canonical_density=(p,),native_Euler_coefficient=(p,99,3),native_Euler_envelope=(p,99,3),metric_Euler_coefficient=(p,6,3),metric_Euler_envelope=(p,6,3),metric_Euler_component_coefficients=(p,6,3,15),metric_Euler_component_envelope=(p,6,3,15)))
 return sh

def force_d0_require_schema(rec,shapes):
 for n,shape in shapes.items():
  assert rec['metadata']['schema'][n]==dict(shape=shape,dtype='float64',finite=True),(rec['file'],n)

def load_force_column(ref):
 rec=resolve_record(ref);force_d0_require_schema(rec,force_d0_column_shapes());raw=read_pair(rec,tuple(force_d0_column_shapes()))
 features=('g','hi','Ga','U','uc','du','z','dz','phi','nu','nz','P','q','V','D','F','Fup','Pi','PiU','Z','A','mu','a','r','f','z2','V_raised','connection_Klo','connection_momentum','connection_D','connection_Maxwell')
 s={k:raw['seed_'+k] for k in features};c={k.removeprefix('seed_chart_'):a for k,a in raw.items() if k.startswith('seed_chart_') and not k.startswith('seed_chart_derivative_')};cj={k.removeprefix('seed_chart_derivative_'):a for k,a in raw.items() if k.startswith('seed_chart_derivative_')}
 c.update(pi_EH=raw['new_metric_EH_momentum'],p_native=raw['new_native_momentum'],p_metric_native=raw['new_metric_native_momentum'])
 rates={k:raw[k] for k in ('seed_nodal_native_rate','seed_covariant_native_rate_R','seed_covariant_native_rate_Z','seed_metric_L2_rate','seed_metric_L2_rate_R','seed_metric_L2_rate_Z','seed_owned_coordinate_Ndot','seed_owned_coordinate_betadot')}
 momenta={k:raw[k] for k in ('new_native_momentum','new_metric_native_momentum','new_metric_EH_momentum','new_metric_total_momentum','new_phase_current','new_phase_canonical_density')}
 # Caller attaches exact INPUT xi/weights and the already registered omega conversion.
 # Gauge n,b and their gradients stay independent; this loader chooses none.
 return s,c,cj,rates,momenta,raw

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

def native_mask():
 m=np.ones((3,87,45),dtype=bool);m[:,0]=False;m[1,:,0]=False;return m

def lift_velocity(x):
 assert x.shape[-3:]==(3,87,45)
 y=x.copy();y[...,0,0,:]=0;y[...,1,0,:]=y[...,1,1,:];y[...,1,:,0]=0;y[...,2,0,:]=y[...,2,1,:];return y

def restrict_velocity(x):
 assert x.shape[-3:]==(3,87,45)
 y=x.copy();y[...,1,1,:]+=y[...,1,0,:];y[...,2,1,:]+=y[...,2,0,:];y[..., :,0,:]=0;y[...,1,:,0]=0;return y

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

def dd_metric_F(R):
 F=np.zeros(R.shape+(6,6));F[...,0,0]=1;F[...,0,1]=R**2;F[...,1,5]=1;F[...,2,0]=R**2;F[...,3,3]=R;F[...,4,2]=R**3;F[...,5,4]=R**2
 return F

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

def pack_dd(n,m):return pack_fields(n[0],m[0]),pack_fields(n[1],m[1])

def collapse(pair,label):
 value=pair[0]+pair[1];capture(label+'_hi',pair[0]);capture(label+'_lo',pair[1]);capture(label+'_rounded_value',value)
 assert np.all(np.isfinite(value));return value

def original_ratios(res,rhs,scale):
 raw=float(np.linalg.norm(res));den=float(np.linalg.norm(rhs));white=float(np.linalg.norm(res/scale));wd=float(np.linalg.norm(rhs/scale))
 assert all(math.isfinite(x) for x in (raw,den,white,wd)) and (den>0)==(wd>0)
 if den==0:return np.array((0.,0.)) if raw==white==0 else np.array((math.inf,math.inf))
 return np.array((raw/den,white/wd))

"""Definitions-only affine first-jet wrapper for the held normal1101 action.
No evaluation, new configuration, source, gauge, history, physical port or law.
Caller provides np, a_dd/a_add/a_sub/a_mul64/a_matvec/a_slice/a_reshape/
a_transpose and tensor_velocity_coordinates, plus keep(name,array).
Each pair encodes one unchanged real tensor by two explicit binary64 words.

At fixed g,U,z,phi and ADM chart coefficients, first jets are J_old+L(delta_rate).
DD subtraction retains the first high-minus-old construction remainder; both
words enter every L contraction. The metric increment has only partial_t g,
but its Christoffel increment fills every affected spacetime slot.
P,uc,z2,f,Z,r and phase/ordinary fixed-configuration terms do not change.
nu,nz,q,V,D,F,a,Pi,PiU,connection momentum,EH pi and reduced momenta are affine.
Chart first derivatives and normal-test first jets are affine in these jets.
Every rate-dependent normal coefficient is at most quadratic. Preserve each
original bilinear product by hh+hl+lh+ll; symmetric quadratics may use 2hl.
In particular Kinetic_EH=f*sqrt_h/(2C)*[th^2-Kh:Kh+2th*tl-2Kh:Kl+
 tl^2-Kl:Kl]. Indices are raised by the unchanged h inverse. The shift EH
term is linear in pi_EH. Curvature, absolute P and fixed-p ordinary terms
are unchanged. Never obtain low corrections by subtracting two large float
normal evaluations. Carry original uncollapsed momenta and their weak-row
residuals to the original canonical certificate before any float readout.
This wrapper alone does not qualify the later nonlinear source/evolution.
"""

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

def paired_fixed_chart_velocity_increment(s,c,y,k,keep,label):
 p=len(s['U']);assert y[0].shape==y[1].shape==(p,99) and k[0].shape==k[1].shape==(p,6)
 du=a_dd(np.zeros((p,4,4)));dz=a_dd(np.zeros((32,p,4,4)));dg=a_dd(np.zeros((p,4,4,4)))
 yu=a_slice(y,(slice(None),slice(0,3)))
 u0=a_add(a_matvec(c['JU'],yu),a_matvec(c['Uh'].swapaxes(-1,-2),k));normal_keep_pair(label+'_U_time_increment',u0,keep)
 du[0][:,0]=u0[0];du[1][:,0]=u0[1];normal_keep_pair(label+'_du_increment',du,keep)
 zi=a_transpose(a_reshape(a_slice(y,(slice(None),slice(3,None))),(p,32,3)),(1,0,2));normal_keep_pair(label+'_z_spatial_component_time_increment',zi,keep)
 z0=a_add(a_matvec(c['JzU'][:,:,None,:],yu),a_matvec(c['Jzz'][:,None,:],zi))
 z0=a_add(z0,a_matvec(c['zh'][:,:,None,:],k));normal_keep_pair(label+'_z0_time_increment',z0,keep)
 dz[0][:,:,0,1:]=zi[0];dz[1][:,:,0,1:]=zi[1];dz[0][:,:,0,0]=z0[0][...,0];dz[1][:,:,0,0]=z0[1][...,0];normal_keep_pair(label+'_dz_increment',dz,keep)
 embed=c['embed'].transpose(0,2,3,1).reshape(p,16,6)
 g0=a_reshape(a_matvec(embed,k),(p,4,4));normal_keep_pair(label+'_metric_time_increment',g0,keep)
 dg[0][:,0]=g0[0];dg[1][:,0]=g0[1];normal_keep_pair(label+'_dg_increment',dg,keep)
 Ga=normal_pair_connection_from_jet(s['hi'],dg,keep,label)
 return dict(du=du,dz=dz,dg=dg,Ga=Ga)

def paired_current_first_jets(old_s,old_c,old_cj,old_rates,y,k,keep,label):
 oldy=old_rates['seed_nodal_native_rate'];oldk=tensor_velocity_coordinates(old_rates['seed_metric_L2_rate'])
 normal_keep_pair(label+'_genuine_native_rate',y,keep);normal_keep_pair(label+'_genuine_metric_rate',k,keep)
 keep(label+'_old_native_rate',oldy);keep(label+'_old_metric_rate',oldk)
 dy=a_sub(y,a_dd(oldy));dk=a_sub(k,a_dd(oldk));normal_keep_pair(label+'_native_rate_difference',dy,keep);normal_keep_pair(label+'_metric_rate_difference',dk,keep)
 delta=paired_fixed_chart_velocity_increment(old_s,old_c,dy,dk,keep,label+'_increment')
 base=dict(du=old_s['du'],dz=old_s['dz'],dg=old_cj['dg'],Ga=old_s['Ga']);out={}
 for name,value in delta.items():
  keep(label+'_old_'+name,base[name]);out[name]=a_add(a_dd(base[name]),value);normal_keep_pair(label+'_current_'+name,out[name],keep)
 # Both registered base jets and their compatibility residual are retained.
 # No reconstructed spatial dg, inverse or configuration replaces the base.
 return dict(first_jets=out,rate_difference=dict(native=dy,metric=dk),jet_difference=delta,configuration_changed=False,collapse_adopted=False)

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

def primitive_chart_positive(s,c):
 uc=np.einsum('pab,pb->pa',abs(s['g']),abs(s['U']));up=np.einsum('pij,pj->pi',abs(c['ih']),uc[:,1:]);ju=np.empty_like(c['JU']);ju[:,0]=up/abs(c['N']*c['gamma'])[:,None]
 ju[:,1:]=abs(c['ih'])+abs(c['beta'])[:,:,None]*ju[:,None,0,:]
 return dict(up=up,JU=ju,JzU=np.einsum('jpa,pai->jpi',abs(s['z']),ju)/abs(s['U'][None,:,0,None]),Jzz=(up+abs(c['beta'])*abs(c['gamma']/c['N'])[:,None])/abs(s['U'][:,0,None]))
def primitive_first_jet_positive(s,c,y,k,rates):
 yabs=abs(y[0])+abs(y[1])+abs(rates['seed_nodal_native_rate']);kabs=abs(k[0])+abs(k[1])+abs(tensor_velocity_coordinates(rates['seed_metric_L2_rate']))
 ce=primitive_chart_positive(s,c);ve=velocity_operation_envelopes(s,c,yabs,kabs,ce)
 out=dict(du=abs(s['du'])+ve['du'],dz=abs(s['dz'])+ve['dz'],dg=abs(s['Ga'])*0,Ga=abs(s['Ga'])+ve['Gamma'])
 product=np.einsum('plam,pln->pamn',out['Ga'],abs(s['g']));out['dg']=product+product.swapaxes(2,3)+ve['dg']
 for n,a in out.items():finite_real('primitive_operation_bound_'+n,a);assert np.all(a>=0)
 return out

def primitive_compatibility_controls(s,c,cj,jets,y,k,op):
 p=len(s['U']);U,z,g=s['U'],s['z'],s['g'];du,dz,dg,Ga=(jets[n] for n in ('du','dz','dg','Ga'))
 # Unit metric contraction requires both metric indices, independently of du.
 unit=a_dd(np.zeros((p,4)))
 for a in range(4):
  for b in range(4):unit=a_add(unit,a_mul64((U[:,a]*U[:,b])[:,None],a_slice(dg,(slice(None),slice(None),a,b))))
  for b in range(4):unit=a_add(unit,a_mul64((2*g[:,a,b]*U[:,b])[:,None],a_slice(du,(slice(None),slice(None),a))))
 transverse=a_dd(np.zeros((32,p,4)))
 for b in range(4):
  transverse=a_add(transverse,a_mul64(z[:,:,b,None],a_slice(du,(slice(None),slice(None),b))));transverse=a_add(transverse,a_mul64(U[None,:,b,None],a_slice(dz,(slice(None),slice(None),slice(None),b))))
 normal_keep_pair('primitive_unit_first_jet',unit,capture);normal_keep_pair('primitive_transverse_first_jet',transverse,capture)
 eu=np.einsum('pamn,pm,pn->pa',op['dg'],abs(U),abs(U))+2*np.einsum('pab,pca,pb->pc',abs(g),op['du'],abs(U))
 ez=np.einsum('pab,jpb->jpa',op['du'],abs(z))+np.einsum('pb,jpab->jpa',abs(U),op['dz'])
 check('complete_current_paired_unit_first_jets',collapse(unit,'primitive_unit_readout'),np.zeros((p,4)),eu)
 check('complete_current_paired_transverse_first_jets',collapse(transverse,'primitive_transverse_readout'),np.zeros((32,p,4)),ez)
 def compatible(Gamma,label):
  product=a_dd(np.zeros((p,4,4,4)))
  for l in range(4):
   term=a_mul64(g[:,l,None,None,:],(Gamma[0][:,l,:,:,None],Gamma[1][:,l,:,:,None]));product=a_add(product,term)
  normal_keep_pair(label+'_unsymmetrized_metric_compatibility_product',product,capture)
  return a_add(product,a_transpose(product,(0,1,3,2)))
 metric=compatible(Ga,'primitive_current');gap=a_sub(dg,metric);basegap=a_sub(a_dd(cj['dg']),compatible(a_dd(s['Ga']),'primitive_base'))
 normal_keep_pair('primitive_current_metric_compatibility_gap',gap,capture);normal_keep_pair('primitive_base_metric_compatibility_gap',basegap,capture)
 eg=np.einsum('plam,pln->pamn',op['Ga'],abs(g));eg=eg+eg.swapaxes(2,3)+op['dg']
 check('paired_metric_compatibility_retains_base_gap',collapse(gap,'primitive_metric_gap'),collapse(basegap,'primitive_base_gap'),eg+abs(cj['dg']))
 uv=[]
 for i in range(1,4):
  v=a_dd(np.zeros(p))
  for m in range(4):v=a_add(v,a_add(a_mul64(g[:,i,m],a_slice(du,(slice(None),0,m))),a_mul64(U[:,m],a_slice(dg,(slice(None),0,i,m)))))
  uv.append(v)
 actual=a_stack(uv+[a_slice(dg,(slice(None),0,i,j)) for i,j in ((1,1),(2,2),(3,3),(1,2),(1,3),(2,3))],axis=-1)
 expected=a_stack([a_slice(y,(slice(None),i)) for i in range(3)]+[a_slice(k,(slice(None),i)) for i in range(6)],axis=-1)
 normal_keep_pair('primitive_mechanical_time_readout',actual,capture);normal_keep_pair('primitive_genuine_mechanical_rate',expected,capture)
 ev=np.einsum('pim,pm->pi',abs(g[:,1:]),op['du'][:,0])+np.einsum('pim,pm->pi',op['dg'][:,0,1:,:],abs(U))
 eh=np.stack([op['dg'][:,0,i,j] for i,j in ((1,1),(2,2),(3,3),(1,2),(1,3),(2,3))],axis=-1)
 check('paired_covector_and_metric_mechanical_time_readout',collapse(a_sub(actual,expected),'primitive_mechanical_gap'),np.zeros((p,9)),np.column_stack((ev,eh))+abs(expected[0])+abs(expected[1]))

def paired_primitive_column(iq,ref,jets,xi,w,omega,recovered=None):
 global RAW,AVAILABLE
 if recovered is None:
  old_s,c,cj,rates,oldmoment,raw=load_force_column(ref);old_s.update(omega=omega,xi=xi,w=w)
  for n in ('R','Z_coordinate','phase_P','phase_PX','phase_PXX','phase_X'):old_s[n]=raw['seed_'+n]
  sl=slice(iq*3784,(iq+1)*3784)
  y=tuple(jets['native_jet_value_'+word][:,sl].transpose(1,0,2).reshape(3784,99) for word in ('hi','lo'));k=tuple(jets['metric_jet_value_'+word][sl] for word in ('hi','lo'))
  lifted=paired_current_first_jets(old_s,c,cj,rates,y,k,capture,'primitive');first=lifted['first_jets'];op=primitive_first_jet_positive(old_s,c,y,k,rates)
 else:
  assert iq==0
  old_s,c,cj,rates,oldmoment,raw,first,op,y,k=recovered
  old_s.update(omega=omega,xi=xi,w=w)
 primitive_compatibility_controls(old_s,c,cj,first,y,k,op)
 feature=paired_current_affine_features(old_s,c,first,capture,'primitive_feature');moment=paired_current_affine_momenta(old_s,c,feature,first,capture,'primitive_momentum')
 data={}
 for prefix,values in (('first_jet',first),('feature',feature['paired']),('momentum',moment)):
  for n,pair in values.items():data[prefix+'_'+n+'_hi']=pair[0];data[prefix+'_'+n+'_lo']=pair[1]
 for n,a in feature['constants'].items():data['config_'+n]=a
 for n in ('R','Z_coordinate','phase_P','phase_PX','phase_PXX','phase_X'):data['config_'+n]=old_s[n]
 for n in ('new_phase_current','new_phase_canonical_density'):data['unchanged_'+n]=oldmoment[n]
 for n,a in c.items():
  if isinstance(a,np.ndarray):data['chart_'+n]=a
 for n,a in op.items():data['operation_'+n]=a
 for name,pair in (('native_rate',y),('metric_rate',k)):data[name+'_hi']=pair[0];data[name+'_lo']=pair[1]
 for n in ('seed_owned_coordinate_Ndot','seed_owned_coordinate_betadot'):data[n]=rates[n]
 data.update({n:a for n,a in AVAILABLE.items() if n.startswith(('primitive_current_metric_compatibility_gap_','primitive_base_metric_compatibility_gap_'))})
 data.update({n:a for n,a in RAW.items() if n.startswith(('control_','failed_V001_'))})
 rec=checkpoint('COLUMN',data,dict(kind='new_paired_current_primitives_and_affine_canonical_momenta',column=iq,old_force_ref=ref,controls=CHECKS[-4:],full_normal_coefficients_computed=False,source_configuration_changed=False,old_L2_rate_not_adopted=True,rate_word_collapse_adopted=False,physical_history=None,recovered_first_jets_and_bounds=bool(recovered is not None),completed_first_jet_replayed=False if recovered is not None else None))
 return dict(native=moment['native_density'],metric=moment['metric_total_density']),rec

def pair_norms(pair,reference,scale,label):return original_ratios(collapse(pair,label),reference,scale)
def primitive_FE_readout(columns,solution,seed,g):
 # Convert local99 ordering to the unchanged group,p,component scatter ordering.
 native=(np.concatenate([c['native'][0].reshape(3784,33,3).transpose(1,0,2) for c in columns],axis=1),np.concatenate([c['native'][1].reshape(3784,33,3).transpose(1,0,2) for c in columns],axis=1))
 metric=(np.concatenate([c['metric'][0] for c in columns]),np.concatenate([c['metric'][1] for c in columns]))
 pn=dd_native_scatter(native,g,capture);normal_keep_pair("completed_primitive_native",pn,capture)
 pm=dd_metric_scatter(metric,g,capture);normal_keep_pair("completed_primitive_metric",pm,capture);data={};rows=[];gaps=[]
 rhs_fields=unpack_fields(seed['original_rhs'],False)[:2]
 for i,(name,primitive,target,offset,scale) in enumerate((('native',pn,seed['current_Pn'],seed['rounded_global_cn'],seed['native_scale']),('metric',pm,seed['current_Pm'],seed['rounded_global_cm'],seed['metric_scale']))):
  achieved=(solution['new_Pn_hi' if i==0 else 'new_Pm_hi'],solution['new_Pn_lo' if i==0 else 'new_Pm_lo']);bridge=a_sub(primitive,achieved);normal_keep_pair(name+"_completed_earned_momentum",achieved,capture);normal_keep_pair(name+"_completed_bridge",bridge,capture)
  saved_res=tuple(unpack_fields(solution['original_residual_'+word],False)[i] for word in ('hi','lo'));e_f=a_sub(a_dd(rhs_fields[i]),a_sub(a_dd(target),a_dd(offset)));normal_keep_pair(name+"_completed_rhs_defect",e_f,capture)
  original=a_sub(saved_res,bridge);normal_keep_pair(name+"_completed_original_residual",original,capture)
  actual=a_sub(a_dd(target),primitive);normal_keep_pair(name+"_completed_actual_target_residual",actual,capture)
  predicted=a_sub(a_sub(saved_res,e_f),bridge);normal_keep_pair(name+"_completed_predicted_residual",predicted,capture)
  gap=a_sub(actual,predicted);normal_keep_pair(name+"_completed_identity_gap",gap,capture)
  positive=abs(target)+abs(offset)+abs(primitive[0])+abs(primitive[1])+abs(achieved[0])+abs(achieved[1])+abs(rhs_fields[i])
  check(name+'_paired_primitive_bridge_and_frozen_rhs_identity',collapse(gap,name+'_identity_gap'),np.zeros_like(target),positive)
  ratio=pair_norms(original,rhs_fields[i],scale,name+'_original_affine_residual');actualratio=pair_norms(actual,target,scale,name+'_actual_target_residual');rows.extend((ratio,actualratio))
  bridge_rhs=pair_norms(bridge,rhs_fields[i],scale,name+'_bridge_rhs_scale');bridge_target=pair_norms(bridge,target,scale,name+'_bridge_target_scale');gaps.extend((bridge_rhs,bridge_target))
  for field,pair in (('primitive_momentum',primitive),('earned_achieved_momentum',achieved),('primitive_minus_earned_bridge',bridge),('original_affine_residual',original),('actual_target_residual',actual),('frozen_rhs_defect',e_f),('identity_gap',gap)):
   data[name+'_'+field+'_hi']=pair[0];data[name+'_'+field+'_lo']=pair[1]
  data[name+'_original_target']=target;data[name+'_rounded_offset']=offset;data[name+'_positive_congruence']=scale;data[name+'_original_rhs']=rhs_fields[i]
 ratios=np.stack(rows);bridgeratios=np.stack(gaps);data['original_affine_and_actual_target_ratios']=ratios;data['bridge_rhs_and_target_ratios']=bridgeratios
 data.update({n:a for n,a in RAW.items() if n.startswith('control_')})
 admitted=bool(np.all(ratios<=LINEAR_TOL));rec=checkpoint('READOUT',data,dict(kind='new_paired_primitive_FE_canonical_readout_with_unfitted_bridge',canonical_primitive_readout_admitted=admitted,controls=CHECKS[-2:],unchanged_linear_tolerance=LINEAR_TOL,normal_coefficients_computed=False,frozen_operator_admission_preserved=True,primitive_and_frozen_operator_admission_distinct=True,offsets_targets_or_state_refitted=False,conditional_full_normal_diagnostic_allowed=True,physical_adoption=False))
 return rec,admitted,ratios,bridgeratios

PINS={'cross_u_current_canonical_nodal_normal_constraints_v001.py': '41f84a9165e8028734e07d463444eb30077bd7145df7f814440fc9ad3201968d', 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py': '5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18', 'author_fragment_current_normal_two_word_first_jets_v001.txt': 'b519899cd4ca3829e2e97e1c247cd574ba49d765f1f32f67e2dfc6b2688c6852', 'author_fragment_current_normal_two_word_affine_features_v001.py': '0625b07a62072a53488d13dd66f530f4475a558006afd48860ae4a7e11be6fe2', 'author_fragment_primitive_dd_pair_admission_v002.txt': '93d829bd060b56ddb19b4eba1bbc6bc5e34b759e846b1712949f1668285743f9', 'author_root_primitive_readout_caller_v001.txt': '050cc9c6f608e94791c33404699421da7fdd1fc41ad85efab8db5285309288b0', 'author_fragment_paired_primitive_failed_admission_v001.txt': 'ea523d63ca7f360810136e2cc068b66866c98bcf46d40606b47e0b3e973eae49'}

# Definitions only; primitive first-jet/momentum measurement, not full normal rows.
# Caller supplies PINS,path,sha,resolve_record,read_pair,json. Both words mandatory.
PRIMITIVE_DD_STEM='CROSS_U_CANONICAL_NODAL_METRIC_RATE_DD_COORDINATES_V001'
PRIMITIVE_DD_TERMINAL=dict(pid=47969,source_sha256='5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',protocol_sha256='1f3c5afbb26dd9f43fcea053f92bfad073fdeb75221265d6212772125445e23e',result_sha256='6979db89e7612ddda54e9b4cadaa565263b99d02c2eca24324a695e0fc92a2bc',receipt_sha256='a11e491baa8950d8dbedf5a0470aea1604cc0366e008fed8fc6154fd649f123d')
PRIMITIVE_DD_READER=('READONLY_DD_NODE_COORDINATE_WORDS_V001_RESULT.json','ce19e353075341a82b475f019cd3fb6ca6f630868001b479b5aee1760c9bb8fc')
PRIMITIVE_DD_KERNELS={'author_fragment_current_normal_two_word_first_jets_v001.txt':'b519899cd4ca3829e2e97e1c247cd574ba49d765f1f32f67e2dfc6b2688c6852','author_fragment_current_normal_two_word_affine_features_v001.py':'0625b07a62072a53488d13dd66f530f4475a558006afd48860ae4a7e11be6fe2'}
def primitive_constraint_admission():
 t=PRIMITIVE_DD_TERMINAL;assert all(v is not None for v in t.values());pins={str(path(n).resolve()):h for n,h in PINS.items()}
 def bind(n,h):
  key=str(path(n).resolve());assert key not in pins or pins[key]==h;assert sha(path(n))==h,n;pins[key]=h
 def record(ref,mapping):
  rec=resolve_record(ref)
  for n,h in ((rec['file'],rec['sha256']),(rec['commit_file'],rec['commit_sha256'])):assert mapping[n if n in mapping else str(path(n).resolve())]==h;bind(n,h)
  return rec
 for n,h in ((PRIMITIVE_DD_STEM+'_RESULT.json',t['result_sha256']),(PRIMITIVE_DD_STEM+'_RECEIPT.json',t['receipt_sha256']),('cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py',t['source_sha256']),(PRIMITIVE_DD_STEM+'.md',t['protocol_sha256']),PRIMITIVE_DD_READER,*PRIMITIVE_DD_KERNELS.items()):bind(n,h)
 nodal=json.loads(path(PRIMITIVE_DD_STEM+'_RESULT.json').read_text());rc=json.loads(path(PRIMITIVE_DD_STEM+'_RECEIPT.json').read_text());reader=json.loads(path(PRIMITIVE_DD_READER[0]).read_text())
 assert rc['status']=='CLOSED' and rc['result_sha256']==t['result_sha256'] and rc['error_sha256'] is None and rc['owner']==nodal['owner'] and nodal['owner']['pid']==47969 and nodal['owner']['source_sha256']==t['source_sha256']
 assert nodal['status']=='CURRENT_CANONICAL_AND_WEAK_CMC_COMPATIBLE' and reader['status']=='SAVED_DD_NODE_COORDINATE_WORDS_PASS' and reader['parent_terminal']==t and reader['pid']==48542 and reader['canonical_and_weak_trace_admitted'] is True
 assert reader['controls']==4 and reader['committed_pairs']==9 and reader['qualification']==nodal['qualification'] and all(v is False for v in nodal['qualification'].values())
 solution=record(nodal['case']['compatibility'],rc['output_sha256']);jets=record(nodal['case']['rate_jets'],rc['output_sha256']);seed=record(nodal['case']['seed'],rc['output_sha256']);system=seed['metadata']['system_refs'];basis=record(system['basis'],rc['input_sha256'])
 assert solution['metadata']['basis_ref']==jets['metadata']['basis_ref']==basis and solution['metadata']['parent_refs']==seed['metadata']['parent_refs'] and seed['metadata']['original_nonadmission_preserved'] is True
 assert solution['metadata']['canonical_and_trace_admitted'] is True and jets['metadata']['collapse_to_binary64_adopted'] is False
 for name,shape in (('native',(33,15136,3)),('metric',(15136,6))):
  for axis in ('value','R','Z'):
   for word in ('hi','lo'):assert jets['metadata']['schema'][name+'_jet_'+axis+'_'+word]==dict(shape=list(shape),dtype='float64',finite=True)
 force_stem='CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V003';bind(force_stem+'_RESULT.json','981a314d7ca598c101db34d4da6f36679c752da81d8cc1325c521f4ce0c7b770');bind(force_stem+'_RECEIPT.json','822c82d59631ebef6f87c0847829370792338a1dcb741c325843d1c8f07e3af2')
 force=json.loads(path(force_stem+'_RESULT.json').read_text());frc=json.loads(path(force_stem+'_RECEIPT.json').read_text());assert frc['status']=='CLOSED' and frc['owner']==force['owner'] and force['owner']['pid']==36387
 bind('READONLY_CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V003_SAVED_AUDIT.json','80b7fac6e83d178bc2eb706853d301bbf258e0fe9f22caa0423e28010eac66e2');fcase=force['cases'][0];assert fcase['sigma']==1. and len(fcase['columns'])==4
 for i,ref in enumerate(fcase['columns']):assert record(ref,frc['output_sha256'])['metadata']['column']==i
 ordinary=record(fcase['loads'],frc['output_sha256']);inp=record(force['checkpoints'][0],frc['output_sha256']);fixed=inp['metadata']['fixed'];assert fixed['eps']==1e-5 and fixed['Q0_over_Hstar']==100
 cpname='CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_EPS_1em05_CP.json';bind(cpname,frc['input_sha256'][str(path(cpname).resolve())]);cp=json.loads(path(cpname).read_text());assert cp['background']==inp['metadata']['owned_background']
 selected=dict(nodal,normal_selected_stage='compatibility',normal_solution=solution,normal_rate_jets=jets,normal_basis=basis,normal_original_seed=seed,normal_original_system_records=system,normal_ordinary_loads=ordinary,normal_precision='separate_hi_lo',normal_consumer_scope='primitive_first_jet_and_momentum_measurement_only',normal_actual_native_momentum=('new_Pn_hi','new_Pn_lo'),normal_actual_metric_momentum=('new_Pm_hi','new_Pm_lo'),normal_native_target='current_Pn',normal_metric_target='current_Pm',full_normal_route_admitted=False,physical_adoption=False,comparison_requirement='retain original-affine and total-target ratios separately at1e-10; measured mismatch never resets offset')
 return pins,selected,force,fixed,cp

def load_normal_rate_record(ref,names):
 rec=resolve_record(ref);assert set(names)<=set(rec['metadata']['schema'])
 if rec['metadata']['owner']['pid']!=47969:
  assert rec['metadata']['owner']['pid']==39611 and rec['file']=='CROSS_U_CANONICAL_NODAL_METRIC_RATE_SOLVE_V001_00007_BASIS.npz' and rec['sha256']=='28bb1ba976b88bfa6b96a7d614524f5760faa79a111da8f75fcaacc7ca95f93f' and rec['commit_sha256']=='36d13345fc78b0afbad152f3f6e03ff381eaa8915b0b84cc4e2c333e00599c11' and rec['metadata']['kind']=='unchanged_E_F_S_bases_and_positive_solver_congruences'
 for n in names:
  if n.endswith(('_hi','_lo')):assert n[:-3]+('_lo' if n.endswith('_hi') else '_hi') in names,'Both saved words mandatory'
 return read_pair(rec,tuple(names))

def load_normal_force_column(ref,names):
 rec=resolve_record(ref);assert rec['metadata']['owner']['pid']==36387 and rec['metadata']['column'] in range(4) and set(names)<=set(rec['metadata']['schema']);return read_pair(rec,tuple(names))


# Definitions only. Caller supplies path/sha/resolve_record/read_pair/json/hashlib.
# Restore only the completed V001 first-jet seed; all controls/features remain unearned.
PRIMITIVE_FAILED_STEM='CROSS_U_PAIRED_CURRENT_PRIMITIVE_MOMENTUM_READOUT_V001'
PRIMITIVE_FAILED_TERMINAL=dict(pid=49473,source_sha256='0f3f4e14f31e2dafe0c4fba18fb439a2af66bd41054b6147fc9a0e96a583a45b',protocol_sha256='2966ccd98523e3e683e97e033fc1e556d771e78cc0d9a1883788125f73ce1867',error_sha256='9e214858d953cfe767ea6e53fd39960f7c66a16a532fe42ff9ded8bd676789cb',receipt_sha256='d63f704c7fc372f355994fad9ee60bf8fa15b9284f69dc7248e61b74ba9e9935')
PRIMITIVE_FAILED_RAW_SCHEMA_SHA='42510ee48aa384e2da7e9d55adae472816295fcc0d241127f1d5b5c0cafa6e24'
def primitive_failed_admission(pins,fixed,cp):
 pins=dict(pins);t=PRIMITIVE_FAILED_TERMINAL;s=PRIMITIVE_FAILED_STEM
 def bind(n,h):
  key=str(path(n).resolve());assert key not in pins or pins[key]==h;assert sha(path(n))==h,n;pins[key]=h
 for n,h in ((s+'_ERROR.json',t['error_sha256']),(s+'_RECEIPT.json',t['receipt_sha256']),('cross_u_paired_current_primitive_momentum_readout_v001.py',t['source_sha256']),(s+'.md',t['protocol_sha256'])):bind(n,h)
 error=json.loads(path(s+'_ERROR.json').read_text());rc=json.loads(path(s+'_RECEIPT.json').read_text())
 assert rc['status']=='CLOSED_ERROR' and rc['error_sha256']==t['error_sha256'] and rc['owner']==error['owner'] and error['owner']['pid']==49473 and error['owner']['source_sha256']==t['source_sha256']
 assert error['status']=='FAILED' and error['controls']==[] and error['context']==dict(column=0,stage='new_paired_primitive_column')
 assert 'could not be broadcast together with shapes (3784,) (3784,4)' in error['traceback'] and error['raw_preservation_traceback'] is None and error['closing_traceback'] is None
 assert all(v is False for v in error['qualification'].values()) and rc['qualification']==error['qualification'] and len(error['checkpoints'])==3
 for mapping in (rc['input_sha256'],rc['output_sha256']):
  for n,h in mapping.items():
   key=str(path(n).resolve());assert key not in pins or pins[key]==h;pins[key]=h
 records={};kinds=('unchanged_configuration_and_earned_paired_rate_references','authenticated_unchanged_E_F_geometry_reused_without_operator_replay','available_unqualified_paired_primitive_operands')
 for label,ref,kind,count in zip(('input','basis','raw'),error['checkpoints'],kinds,(4,7,182)):
  rec=resolve_record(ref);assert rec==ref and rec['metadata']['owner']==error['owner'] and rec['metadata']['kind']==kind and len(rec['metadata']['schema'])==count
  for n,h in ((rec['file'],rec['sha256']),(rec['commit_file'],rec['commit_sha256'])):assert rc['output_sha256'][n]==h;bind(n,h)
  records[label]=rec
 assert records['input']['metadata']['fixed']==fixed and records['input']['metadata']['owned_background']==cp['background']
 assert set(records['input']['metadata']['schema'])=={'r_kpc','z_kpc','xi','weights'} and set(records['basis']['metadata']['schema'])=={'R','dv','hats','cell_i','cell_j','r','z'}
 schema=records['raw']['metadata']['schema'];assert hashlib.sha256(json.dumps(schema,sort_keys=True,separators=(',',':')).encode()).hexdigest()==PRIMITIVE_FAILED_RAW_SCHEMA_SHA
 assert all(v['dtype']=='float64' and v['finite'] is True for v in schema.values()) and not any(n.startswith('control_') for n in schema)
 for name,shape in (('du',[3784,4,4]),('dz',[32,3784,4,4]),('dg',[3784,4,4,4]),('Ga',[3784,4,4,4])):
  for word in ('hi','lo'):assert schema['primitive_current_'+name+'_'+word]==dict(shape=shape,dtype='float64',finite=True)
  assert schema['primitive_operation_bound_'+name]==dict(shape=shape,dtype='float64',finite=True)
 for name,shape in (('native',[3784,99]),('metric',[3784,6])):
  for word in ('hi','lo'):assert schema['primitive_genuine_'+name+'_rate_'+word]==dict(shape=shape,dtype='float64',finite=True)
 for n in (s+'_OWNER_START.json',s+'_MANIFEST.json'):bind(n,rc['output_sha256'][n])
 assert json.loads(path(s+'_OWNER_START.json').read_text())==error['owner'];manifest=json.loads(path(s+'_MANIFEST.json').read_text());assert manifest['owner']==error['owner'] and manifest['controls']==18 and manifest['pairs']==7
 return pins,dict(records,error=error,receipt=rc,original_controls=[],first_jets_complete=True,controls_or_features_completed=False)

def read_failed_primitive_seed(failed):
 rec=failed['raw'];raw=read_pair(rec,tuple(rec['metadata']['schema']));assert len(raw)==182
 features=('g','hi','Ga','U','uc','du','z','dz','phi','nu','nz','P','q','V','D','F','Fup','Pi','PiU','Z','A','mu','a','r','f','z2','V_raised','connection_Klo','connection_momentum','connection_D','connection_Maxwell','R','Z_coordinate','phase_P','phase_PX','phase_PXX','phase_X')
 old_s={n:raw['loaded_seed_'+n] for n in features}
 c={n.removeprefix('loaded_seed_chart_'):a for n,a in raw.items() if n.startswith('loaded_seed_chart_') and not n.startswith('loaded_seed_chart_derivative_')};cj={n.removeprefix('loaded_seed_chart_derivative_'):a for n,a in raw.items() if n.startswith('loaded_seed_chart_derivative_')}
 c.update(pi_EH=raw['loaded_new_metric_EH_momentum'],p_native=raw['loaded_new_native_momentum'],p_metric_native=raw['loaded_new_metric_native_momentum'])
 rates={n:raw['loaded_'+n] for n in ('seed_nodal_native_rate','seed_covariant_native_rate_R','seed_covariant_native_rate_Z','seed_metric_L2_rate','seed_metric_L2_rate_R','seed_metric_L2_rate_Z','seed_owned_coordinate_Ndot','seed_owned_coordinate_betadot')}
 oldmoment={n:raw['loaded_'+n] for n in ('new_native_momentum','new_metric_native_momentum','new_metric_EH_momentum','new_metric_total_momentum','new_phase_current','new_phase_canonical_density')}
 first={n:tuple(raw['primitive_current_'+n+'_'+word] for word in ('hi','lo')) for n in ('du','dz','dg','Ga')};op={n:raw['primitive_operation_bound_'+n] for n in ('du','dz','dg','Ga')}
 y=tuple(raw['primitive_genuine_native_rate_'+word] for word in ('hi','lo'));k=tuple(raw['primitive_genuine_metric_rate_'+word] for word in ('hi','lo'))
 # Caller attaches authenticated INPUT omega/xi/w, preserves all182 raw fields, then runs only unearned controls/features/momenta.
 return old_s,c,cj,rates,oldmoment,raw,first,op,y,k

def paired_primitive_packet(nodal,force,fixed,cp,failed):
 global RAW,AVAILABLE,B
 inp=failed['input'];ev=read_pair(inp,('r_kpc','z_kpc','xi','weights'))
 xi,w=ev['xi'],ev['weights'];assert np.all(xi>0) and np.all(w>0) and np.all(np.diff(xi)>0)
 B=1.0059833281731022e-10*3.085677581491367e19/299792458.**2
 omega=SIGMA*xi*fixed['Hunit']/299792458.;assert np.all(np.isfinite(omega)) and np.all(omega>0)
 checkpoint('INPUT',ev,dict(kind='unchanged_configuration_and_earned_paired_rate_references',fixed=fixed,owned_background=cp['background'],selected_solution=nodal['normal_solution'],selected_rate_jets=nodal['normal_rate_jets'],selected_original_seed=nodal['normal_original_seed'],selected_basis=nodal['normal_basis'],copied_completed_parent=failed['input'],failed_raw_parent=failed['raw'],original_failed_controls=[],full_normal_coefficients_computed=False,physical_history=None))
 g=read_pair(failed['basis'],('R','dv','hats','cell_i','cell_j','r','z'))
 assert g['R'].shape==g['dv'].shape==(4,3784) and g['hats'].shape==(4,4,3,86,44) and np.all(g['R']>0) and np.all(g['dv']>0)
 assert np.array_equal(g['r'],ev['r_kpc']) and np.array_equal(g['z'],ev['z_kpc'])
 checkpoint('BASIS',g,dict(kind='authenticated_unchanged_E_F_geometry_reused_without_operator_replay',parent=nodal['normal_basis'],copied_completed_parent=failed['basis'],native_dof=380292,metric_dof=23048))
 jets=load_normal_rate_record(nodal['normal_rate_jets'],tuple(name+'_jet_'+axis+'_'+word for name in ('native','metric') for axis in ('value','R','Z') for word in ('hi','lo')))
 solution=load_normal_rate_record(nodal['normal_solution'],tuple(name+'_'+word for name in ('new_Pn','new_Pm','original_residual') for word in ('hi','lo')))
 seed=load_normal_rate_record(nodal['normal_original_seed'],('original_rhs','current_Pn','current_Pm','rounded_global_cn','rounded_global_cm','native_scale','metric_scale'))
 columns=[];records=[]
 for iq,ref in enumerate(force['cases'][0]['columns']):
  RAW={};AVAILABLE={};CONTEXT.update(stage='new_paired_primitive_column',column=iq)
  recovered=None
  if iq==0:
   recovered=read_failed_primitive_seed(failed)
   RAW.update({'failed_V001_'+n:a.copy() for n,a in recovered[5].items()})
   for n,pair in (('native',recovered[8]),('metric',recovered[9])):
    for wi,word in enumerate(('hi','lo')):
     expected=jets[n+'_jet_value_'+word][:,:3784].transpose(1,0,2).reshape(3784,99) if n=='native' else jets[n+'_jet_value_'+word][:3784]
     assert np.array_equal(pair[wi],expected),(n,word,'cached genuine rate changed')
  col,rec=paired_primitive_column(iq,ref,jets,xi,w,omega,recovered=recovered);columns.append(col);records.append(rec)
 RAW={};AVAILABLE={};CONTEXT.update(stage='paired_primitive_to_frozen_FE_readout')
 readout,admitted,ratios,bridge=primitive_FE_readout(columns,solution,seed,g)
 assert len(CHECKS)==18 and len(RECORDS)==7 and all(c['passed'] for c in CHECKS)
 return dict(original_failed_attempt=dict(owner=failed['error']['owner'],error_sha256=PRIMITIVE_FAILED_TERMINAL['error_sha256'],receipt_sha256=PRIMITIVE_FAILED_TERMINAL['receipt_sha256'],raw_ref=failed['raw'],controls=[]),status='CURRENT_PRIMITIVE_CANONICAL_READOUT_ADMITTED' if admitted else 'CURRENT_PRIMITIVE_CANONICAL_READOUT_MISMATCH',columns=records,readout=readout,canonical_primitive_readout_admitted=admitted,original_affine_and_actual_target_ratios=ratios.tolist(),bridge_rhs_and_target_ratios=bridge.tolist(),frozen_canonical_admission_preserved=True,conditional_full_normal_diagnostic_allowed=True,normal_coefficients_computed=False,physical_adoption=False)

def main():
 global np,OWNER,INPUTS,RAW,AVAILABLE
 ap=argparse.ArgumentParser();ap.add_argument('--root-run',action='store_true');args=ap.parse_args()
 if AUTHOR_DRAFT or AUTHORING_IN_PROGRESS or not args.root_run:raise SystemExit('Guarded paired primitive readout: root release after full review required.')
 assert PROTOCOL_SHA and sha(path(STEM+'.md'))==PROTOCOL_SHA
 assert not list(BASE.glob(STEM+'_*')),'Unused namespace required; all previous attempts preserved'
 INPUTS,nodal,force,fixed,cp=primitive_constraint_admission()
 INPUTS,failed=primitive_failed_admission(INPUTS,fixed,cp)
 INPUTS[str(path(STEM+'.md').resolve())]=PROTOCOL_SHA;INPUTS[str(Path(__file__).resolve())]=sha(__file__)
 OWNER=dict(owner='root',pid=os.getpid(),started=now(),source_sha256=sha(__file__))
 try:
  json_file(STEM+'_OWNER_START.json',OWNER)
  json_file(STEM+'_MANIFEST.json',dict(owner=OWNER,input_sha256=INPUTS,scope='saved column0 first jets and bounds reused; unearned controls/affine momenta and columns1-3/bridge only',controls=18,pairs=7,normal_coefficients_computed=False,qualification=FLAGS))
  import numpy as _np
  np=_np
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=paired_primitive_packet(nodal,force,fixed,cp,failed)
  recheck();rh=json_file(STEM+'_RESULT.json',dict(owner=OWNER,status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS))
  recheck();json_file(STEM+'_RECEIPT.json',dict(owner=OWNER,status='CLOSED',closed=now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));recheck()
  print(case['status'],len(CHECKS),len(RECORDS),rh);return 0 if case['canonical_primitive_readout_admitted'] else 3
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None;available=dict(AVAILABLE);available.update(RAW)
  available.update({'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()})
  if np is not None and available:
   try:checkpoint('ERROR_RAW',available,dict(kind='available_unqualified_paired_primitive_operands',context=dict(CONTEXT)),failed=True)
   except BaseException:raw_error=traceback.format_exc()
  try:seal_actual();recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=json_file(STEM+'_ERROR.json',dict(owner=OWNER,status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,preserved_outputs=dict(OUTPUTS),qualification=FLAGS))
  prior=path(STEM+'_RECEIPT.json');receipt_name=STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json')
  json_file(receipt_name,dict(prior_receipt_sha256=sha(prior) if prior.exists() else None,owner=OWNER,status='CLOSED_ERROR',closed=now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),error_sha256=eh,qualification=FLAGS))
  seal_actual();recheck(False);raise

if __name__=='__main__':raise SystemExit(main())

"""Guarded root-only full-metric/native/source weak measures on CLOSED trial data."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,ast,hashlib,json,math,os,traceback
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_SAVED_FULL_METRIC_NATIVE_SOURCE_RESIDUAL_V001'
ODD='CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001'
BAND='CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001'
COMPACT='CROSS_U_SAVED_EVEN_SPATIAL_METRIC_COMPACT_RESIDUAL_V002'
PROTOCOL_SHA='88fbf64e1568af3f47f1346b809c6d8a35fe7b685a73817938616b9056068e24'
PINS={'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_EPS_1em05_CP.json': '3f4cbdf1c8255ae06668dc63fa6cdfc7ca4c5b70c78a2b5cbe64a303fb17973c', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RECEIPT.json': 'df514792bf703b6ce6b9e4c2a64e2ac19c407dffa0f14acf9bb9f75b6acc64e6', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RESULT.json': 'e9f7b2070e762920cb3548ccbe11c5f46efd1a262065ba594afaca6635acc35f', 'CROSS_U_EPS5_MACRO_BACKGROUND_CALLER_REGISTRATION_V001.md': '087b59df9fd2ef89b3f471fa5fc8a6b0e5a1102b8c37f6d2d6e377f8130e2523', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001.md': '030a618dc6ac06f9faa6748e3559afe074e17be4ad6feba94ae7348a935a9f2e', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_00000_INPUT.npz': 'f6d8c876eca1db21e613fda745a3c239f682789e98db581f56436804e2fe7b02', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_00000_INPUT.npz.COMMIT.json': '49e79e3a41cf1fb3466a2d79634aabf12b368e895b2594f91db09bc148bc31b6', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_00003_COEFFICIENTS.npz': '9b016352c4aa8fdd1dc9bf76bdbc20bfe3ef48c6287c41f2ffab929da37d5ea1', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_00003_COEFFICIENTS.npz.COMMIT.json': 'bc9320157d55270b5a50c7a9e87122b836cd0974dea4e3fd53ee62d582d5866a', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_00005_COEFFICIENTS.npz': 'eceb3c5dcbfe38578a6b04a9e3ef64f7a27ed06ba8df40c170ead7dc1a28781e', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_00005_COEFFICIENTS.npz.COMMIT.json': 'd07ce6a875f4204ef4b8dcebba5cdc23ab77144a17466c1e8a9d77dcbf232924', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_00007_COEFFICIENTS.npz': 'bb3f8f8640bfda483bf3cfc8d81c281a7184323252fead9dd7418608a738427d', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_00007_COEFFICIENTS.npz.COMMIT.json': 'a258e0960f18f611c3bdb0128101ca6f625cdea56be5597215b04b4e69137b4e', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_00009_COEFFICIENTS.npz': 'e5f337c07424d4b1332eb820bdc6bcbb780b01f43d89969f44bdd9f5e33a25f5', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_00009_COEFFICIENTS.npz.COMMIT.json': '3d6a51a9ede774eaec6eff223605844f63cc48cde2ce1639a3f2049608bf6f24', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_RECEIPT.json': 'afd64b4dff5f9f4151494749d3d3d54b91dc031e82a394994c6c17e8e24ebe04', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001.md': '0f7b501037a0f0e65359435825b9d48f49d1249efc6c39a4549e285bdf88423b', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_00003_ASSEMBLY.npz': '75887254f27f8352053afe167b5f9bddd0878e9d1a71f2dd5c85ca490592f32f', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_00003_ASSEMBLY.npz.COMMIT.json': 'f8d7d621c5a2e2ea3faae41660cade972c4efd0bb39d4bbc629d6fe2e77ebbfc', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_00004_FINAL.npz': 'edc24ede7539c954eff7b672e57100b80d698e5bf2b0d7f6098e695b26fe0322', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_00004_FINAL.npz.COMMIT.json': '892f1f28e508bd63c971e80448e3dbd5fb0f89d03395d14dde919319e3760b7b', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_00005_ASSEMBLY.npz': '987d28e2a6e029358083887b9ad00baebe1ec0b3db41f7f7d4577c3aca8e42b5', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_00005_ASSEMBLY.npz.COMMIT.json': 'f4a36c2c27eb24861eb9fef549691e3545df710a151038333873f3092992e213', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_00006_FINAL.npz': '0fd15943c18f728830a657fa24d60da9e09dd6877e4f0506080ff6bb52e71c2b', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_00006_FINAL.npz.COMMIT.json': 'f6c5580e0d7c1c54872e6dd5a7233e1ef2de1a21480012b7626635bd37d4c907', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_00007_ASSEMBLY.npz': 'e278b910fc7610857925fd43909eeb0b1eb0c0726adad87a5d16de7f8bfadcac', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_00007_ASSEMBLY.npz.COMMIT.json': '38898898221e62e5e65615dbef695dc10c143422dd26a17451009ecf12565324', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_00008_FINAL.npz': '03f795d1e8abc64a971861f763301d1e95be5d6e05f917c5bab9da6ea22f5a92', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_00008_FINAL.npz.COMMIT.json': '34adc747416f6b1a7da6fe1d3fbd767648df112d324867d3cad1b24718bf489f', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_00009_ASSEMBLY.npz': 'bafae248fbb0c3289fd2e9cfcb6d4650d15955fe1c16b298a774fb744d0bcc7a', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_00009_ASSEMBLY.npz.COMMIT.json': '4fd00973e05df5445b7be830b18ef28fda611d2fb8851d059b71b50fc1c725f7', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_00010_FINAL.npz': '53a28d073995fc4dbc2acc7acb9dc6e95745ca2f9f6c64a7bf5db67e8cee324a', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_00010_FINAL.npz.COMMIT.json': '6d88233b8787ea606c2a5ee1f80f277b29c50944250abbec4b6bb220cc7010cf', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_RECEIPT.json': '41a22374c9747d5b64bf4894290433af8a2cdb92f345f64f6de89f8cc175ea0f', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_RESULT.json': 'fc54d032172c901d288d7f845c077b7f4114199183190e3c0b7eb2c8a1420e85', 'CROSS_U_NONLINEAR_NATIVE_FLOW_AND_CIRCULAR_ACCELERATION_CLOSURE_V001.md': 'f7fc8138a9683a677851bdf9241c82ca942d4153db1254f513e28eca9f912a21', 'CROSS_U_STATIONARY_AZIMUTHAL_SHIFT_AND_NATIVE_RESPONSE_V001.md': '048b224899adf28c6924fa02c06a2e2d42fced7f086a139ed8a6981e0dc20fe2', 'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md': 'e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0', 'cross_u_axial_flrw_state_and_moving_port_v001.py': '96e7004d7abf2efedcff74eb2f36fb5a5a19a77ac181b58a652c5b8974c3f759', 'cross_u_ngc3198_conditional_odd_sector_v001.py': '508c379f4bd287435b406567f772fb14efdb7142ca17b18ef0d3e4e74736b394', 'cross_u_ngc3198_odd_banded_correction_v001.py': 'a22931b8f9b8a0a1cca663a459892c634b0f484791a61495567bff33f14bc913', 'reviewed_cross_u_saved_untruncated_native_flow_residual_v001_443_0467e0f8.py': '0467e0f881d9e58acfacb57bb9cbb675bba8eba18994f9202574390240f8a1c2', 'reviewed_cross_u_saved_untruncated_native_flow_residual_v001_444_ad897489.py': 'ad897489cec81a3f6a5dba22c6f5c2b9cf400c6e334f8fc84bbec0cb73471f10', 'cross_u_saved_untruncated_native_flow_residual_v001.py': 'f912774d0cc918512a4a13c4c65436138f30b04ae24a51bcf5232e6139730915', 'CROSS_U_FULL_METRIC_CONSTRAINED_WEAK_VARIATION_SCOPE_V001.md': '2b927d54354eec7f8e8018960c7920c12d8099c070c42c2577cae1af8fe4dad7', 'CROSS_U_SAVED_EVEN_SPATIAL_METRIC_COMPACT_RESIDUAL_V002_RECEIPT.json': '8beca951650f8fb498b0ce1e4b273bf9bf10f92ada1dc541327aa26cd9733407', 'CROSS_U_SAVED_EVEN_SPATIAL_METRIC_COMPACT_RESIDUAL_V002_00000_INPUT.npz': '487f71346cc001caa6177fcdb4867c8d61be1b784fdfad786eb9f8eda2df0187', 'CROSS_U_SAVED_EVEN_SPATIAL_METRIC_COMPACT_RESIDUAL_V002_00000_INPUT.npz.COMMIT.json': '3447c04a5cf43b94bba719ec1b9ca16c247dd4bdc815d356608540fa4681ed51', 'galaxy_density.py': '9819b9cb1f63baea07eb06a150dbda3113d7850d9ac24a13ee65e96f6f07bb6c', 'cross_u_saved_even_spatial_metric_compact_residual_v002.py': 'c12a1ec51c8a589d49b6a09cff0467a9a6fa63a2970bc4ffe6fcf26f64e29119', 'CROSS_U_SAVED_EVEN_SPATIAL_METRIC_COMPACT_RESIDUAL_V002.md': '4899ed0d053c052dafd5f885070b9b4eb4d71398e026edb404de287ad52a1cad'}
COEFFICIENT_FILES=['CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_00003_COEFFICIENTS.npz', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_00005_COEFFICIENTS.npz', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_00007_COEFFICIENTS.npz', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_00009_COEFFICIENTS.npz']
LIGHT=299792458.;KPC=3.085677581491367e19;A0=1.0059833281731022e-10;B=A0*KPC/LIGHT**2
G_KPC_KMS2_MSUN=4.30091e-6;A0_V=A0*KPC/1e6
KB=.02;C=1.98;ALPHA=KB/C;ELL=.1;GC=3*math.pi/8
SIGMAS=(.1,1.,10.,100.);BOXES=((2.,16.),(16.,48.));TOL=2e-11;CONTROL_COUNT=36;PAIR_COUNT=6
DYADS=tuple((a,b) for a in range(4) for b in range(a,4))
np=None;OWNER=None;INPUTS={};OUTPUTS={};RECORDS=[];RAW={};ARM_AVAILABLE={};CONTEXT={};CHECKS=[];QBAR=None
FLAGS={k:False for k in ('full_metric_Galerkin_qualified','full_Einstein_solution_qualified','full_phase_solution_qualified','full_ordinary_Euler_qualified','physical_junction_qualified','physical_temporal_spectrum_qualified','physical_Cauchy_preparation_qualified','active_source_mapping_qualified','orbital_force_qualified','observational_qualified','joint_model_adopted')}
def now():return datetime.now(timezone.utc).isoformat()

def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p

def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def canonical(v):
 if isinstance(v,dict):return {str(k):canonical(x) for k,x in v.items()}
 if isinstance(v,(list,tuple)):return [canonical(x) for x in v]
 if np is not None and isinstance(v,np.generic):return canonical(v.item())
 if v is None or type(v) in (str,bool,int):return v
 if type(v) is float and math.isfinite(v):return v
 raise TypeError('Nonfinite or unsupported metadata: '+type(v).__name__)

def encode(v):return (json.dumps(canonical(v),sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()

def publish(n,b):
 p=path(n)
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);assert p.read_bytes()==b;OUTPUTS[n]=sha(p);return OUTPUTS[n]

def json_file(n,v):return publish(n,encode(v))

def array(v,name):
 a=np.asarray(v)
 if a.dtype.kind not in 'fiu' or not np.all(np.isfinite(a)):raise ValueError(name+' must be finite real numeric data.')
 return a.astype(np.float64,copy=False)

def check(name,actual,expected,envelope=None):
 ordinal=len(CHECKS);CONTEXT.update(current_control=name,current_control_ordinal=ordinal)
 a=np.asarray(actual);b=np.asarray(expected);prefix=f'control_{ordinal:03d}_{name}'
 RAW[prefix+'_actual']=a.copy();RAW[prefix+'_expected']=b.copy()
 if envelope is not None:RAW[prefix+'_envelope']=np.asarray(envelope).copy()
 assert a.shape==b.shape and np.all(np.isfinite(a)) and np.all(np.isfinite(b))
 env=max(1e-30,float(np.max(abs(a),initial=0)),float(np.max(abs(b),initial=0))) if envelope is None else max(1e-30,float(np.max(array(envelope,'control envelope'),initial=0)))
 gap=float(np.max(abs(a-b),initial=0));err=gap/env;assert all(math.isfinite(x) for x in (env,gap,err))
 row=dict(ordinal=ordinal,name=name,absolute_gap=gap,envelope=env,error=err,tolerance=TOL,passed=err<=TOL);CHECKS.append(row)
 assert row['passed'],name
 return row

def checkpoint(tag,arrays,meta):
 md=canonical(dict(meta,owner=OWNER,qualification=FLAGS,schema={k:dict(shape=list(v.shape),dtype=str(v.dtype),finite=bool(np.all(np.isfinite(v)))) for k,v in arrays.items()}))
 text=encode(md).decode();md=json.loads(text);name=f'{STEM}_{len(RECORDS):05d}_{tag}.npz';p=path(name)
 with p.open('xb') as f:np.savez_compressed(f,metadata_json=np.array(text),**arrays);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);rec=dict(file=name,sha256=sha(p),metadata=md);cf=name+'.COMMIT.json';ch=json_file(cf,rec)
 rec=dict(rec,commit_file=cf,commit_sha256=ch);OUTPUTS[name]=rec['sha256'];RECORDS.append(rec)
 with np.load(p,allow_pickle=False) as f:
  assert set(f.files)==set(arrays)|{'metadata_json'} and str(f['metadata_json'])==text
  for k,a in arrays.items():assert f[k].dtype==a.dtype and f[k].shape==a.shape and np.array_equal(f[k],a,equal_nan=True)
 return rec

def seal_created():
 for p in sorted(BASE.glob(STEM+'_*')):
  if p.is_file():p.chmod(0o444);OUTPUTS[p.name]=sha(p)

def recheck(strict=True):
 for n,h in INPUTS.items():assert sha(path(n))==h,('Input changed',n)
 assert sha(__file__)==OWNER['source_sha256']
 if strict:assert path(STEM+'_OWNER_START.json').read_bytes()==encode(OWNER)
 for n,h in OUTPUTS.items():assert sha(path(n))==h,('Output changed',n)
 for r in RECORDS:
  assert json.loads(path(r['commit_file']).read_text())=={k:v for k,v in r.items() if k not in ('commit_file','commit_sha256')}
  with np.load(path(r['file']),allow_pickle=False) as f:
   assert json.loads(str(f['metadata_json']))==r['metadata'] and set(f.files)==set(r['metadata']['schema'])|{'metadata_json'}
   for k,s in r['metadata']['schema'].items():assert f[k].shape==tuple(s['shape']) and str(f[k].dtype)==s['dtype'] and bool(np.all(np.isfinite(f[k])))==s['finite']
 if strict:
  assert {p.name for p in BASE.glob(STEM+'_*.npz')}=={r['file'] for r in RECORDS}
  assert {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={r['commit_file'] for r in RECORDS}

def shape_quadrature(r,z):
    dr=np.diff(r)[:,None]; dz=np.diff(z)[None,:]
    nodes=(-1/math.sqrt(3),1/math.sqrt(3)); out=[]
    for u in nodes:
        for v in nodes:
            rr=(r[:-1,None]+r[1:,None])/2+u*dr/2
            volume=rr*dr*dz/4
            shapes=[]
            for i,j in ((0,0),(1,0),(0,1),(1,1)):
                si=1 if i else -1; sj=1 if j else -1
                shapes.append(((1+si*u)*(1+sj*v)/4,
                               si*(1+sj*v)/(2*dr),sj*(1+si*u)/(2*dz),i,j))
            out.append((rr,volume,shapes))
    return out

def interpolate(x,shapes):
    val=np.zeros(x.shape[:-2]+(x.shape[-2]-1,x.shape[-1]-1))
    gr=np.zeros_like(val); gz=np.zeros_like(val)
    for n,nr,nz,i,j in shapes:
        xx=x[...,i:x.shape[-2]-1+i,j:x.shape[-1]-1+j]
        val+=n*xx; gr+=nr*xx; gz+=nz*xx
    return val,gr,gz

def compact(R,Z,box):
 l,h=box;m=(l+h)/2;d=(h-l)/2;x=(R-m)/d;y=Z/16
 ok=(abs(x)<1)&(y<1)&(y>=0);f=(1-x*x)**3*(1-y*y)**3
 fr=-6*x/d*(1-x*x)**2*(1-y*y)**3;fz=-6*y/16*(1-y*y)**2*(1-x*x)**3
 return np.where(ok,f,0),np.where(ok,fr,0),np.where(ok,fz,0)

def lower(g,v):return np.einsum('pab,...pb->...pa',g,v)

def lower_last(g,v):return np.einsum('pab,pcb->pca',g,v)

def raise_cov(hi,v):return np.einsum('pab,...pb->...pa',hi,v)
def covdot(hi,a,b):return np.einsum('...pa,...pa->...p',raise_cov(hi,a),b)

def metric(R,Phi,gr,beta,br):
 n=np.exp(Phi);rho=R/n;m=np.exp(-2*Phi);p=len(R)
 g=np.zeros((p,4,4));g[:,0,0]=-n*n+rho*rho*beta*beta;g[:,0,3]=g[:,3,0]=rho*rho*beta
 g[:,1,1]=g[:,2,2]=m;g[:,3,3]=rho*rho
 hi=np.zeros_like(g);hi[:,0,0]=-1/(n*n);hi[:,0,3]=hi[:,3,0]=beta/(n*n)
 hi[:,1,1]=hi[:,2,2]=1/m;hi[:,3,3]=1/(rho*rho)-beta*beta/(n*n)
 dg=np.zeros((p,4,4,4))
 for a in (1,2):
  nr=n*gr[:,a];rr=rho*((1/R if a==1 else 0)-gr[:,a]);mr=-2*m*gr[:,a];bb=br[:,a]
  dg[:,a,0,0]=-2*n*nr+2*rho*rr*beta*beta+2*rho*rho*beta*bb
  dg[:,a,0,3]=dg[:,a,3,0]=2*rho*rr*beta+rho*rho*bb
  dg[:,a,1,1]=dg[:,a,2,2]=mr;dg[:,a,3,3]=2*rho*rr
 Ga=np.zeros_like(dg)
 for a in range(4):
  for b in range(4):
   Ga[:,:,a,b]=np.einsum('plm,pm->pl',hi,(dg[:,a,b,:]+dg[:,b,a,:]-dg[:,:,a,b]))/2
 RAW.update(current_metric=g,current_inverse=hi,current_metric_jet=dg,current_connection=Ga)
 return g,hi,dg,Ga,n,rho

def features(g,hi,Ga,U,du,z,dz,phi,omega,xi,w):
 # du/dz have derivative index first; z and dz are COVECTORS.
 nu=du+np.einsum('pbal,pl->pab',Ga,U)
 nz=dz-np.einsum('plab,jpl->jpab',Ga,z)
 uc=lower(g,U);P=np.eye(4)[None,:,:]+np.einsum('pa,pb->pab',uc,U)
 q=np.einsum('pa,jpab->jpb',U,nz);V=np.einsum('pab,jpb->jpa',P,q)
 D=np.einsum('pac,jpcd,pbd->jpab',P,nz,P)
 F=lower_last(g,nu)-np.swapaxes(lower_last(g,nu),1,2)
 # lower_last(g,nu) lowers nu's last (vector) index, leaving derivative index first.
 a=np.einsum('pa,pab->pb',U,nu);r=np.einsum('pab,pb->pa',P,phi)
 z2=covdot(hi,z,z);f=1+z2/((B*GC)**2*xi[:,None]**4)
 Vu=raise_cov(hi,V);Du=np.einsum('pac,jpcd,pdb->jpab',hi,D,hi)
 Pi=w[:,None,None,None]*(np.einsum('pa,jpb->jpab',U,Vu)/omega[:,None,None,None]**2-ELL**2*Du)
 nuc=lower_last(g,nu);mu=np.einsum('jpab,pab->jp',Pi,nuc)
 Z=np.einsum('j,jpa->pa',w,z);Fup=np.einsum('pac,pcd,pdb->pab',hi,F,hi)
 PiU=-ALPHA*np.einsum('pac,pcb->pab',hi,F)+np.einsum('pa,pb->pab',U,Z)
 Aj=(np.einsum('jpn,jprn->jpr',Vu,nz)+np.einsum('jpa,pa->jp',q,U)[:,:,None]*V)/omega[:,None,None]**2
 Aj-=ELL**2*(np.einsum('jprn,jpn->jpr',D,Vu)
        +np.einsum('jpmr,jpmn,pn->jpr',np.einsum('pmc,jpcr->jpmr',hi,D),nz,U))
 # In the second projector term raise D's FIRST index; rho stays lower.
 Q=np.einsum('pa,pa->p',U,phi);Ur=np.einsum('pa,pa->p',U,r)
 A=-(Q[:,None]*r+Ur[:,None]*phi)+np.einsum('pn,prn->pr',Z,nu)+np.einsum('j,jpr->pr',w,Aj)
 out=dict(g=g,hi=hi,Ga=Ga,U=U,du=du,z=z,dz=dz,phi=phi,omega=omega,xi=xi,w=w,nu=nu,nz=nz,uc=uc,P=P,q=q,V=V,D=D,a=a,r=r,f=f,z2=z2,Pi=Pi,mu=mu,Z=Z,F=F,Fup=Fup,PiU=PiU,A=A)
 RAW.update({f'current_{k}':v for k,v in out.items() if isinstance(v,np.ndarray)})
 return out

def variation(s,eta,deta,zeta,dzeta):
 g,hi,Ga=s['g'],s['hi'],s['Ga'];U=s['U'];z=s['z'];w=s['w'];om=s['omega'];P=s['P']
 ne=deta+np.einsum('pbal,pl->pab',Ga,eta)
 nzeta=dzeta-np.einsum('plab,jpl->jpab',Ga,zeta)
 ec=lower(g,eta);dP=np.einsum('pa,pb->pab',ec,U)+np.einsum('pa,pb->pab',s['uc'],eta)
 dq=np.einsum('pa,jpab->jpb',eta,s['nz'])+np.einsum('pa,jpab->jpb',U,nzeta)
 dV=np.einsum('pab,jpb->jpa',dP,s['q'])+np.einsum('pab,jpb->jpa',P,dq)
 dD=np.einsum('pac,jpcd,pbd->jpab',dP,s['nz'],P)+np.einsum('pac,jpcd,pbd->jpab',P,s['nz'],dP)+np.einsum('pac,jpcd,pbd->jpab',P,nzeta,P)
 dF=lower_last(g,ne)-np.swapaxes(lower_last(g,ne),1,2)
 da=np.einsum('pa,pab->pb',eta,s['nu'])+np.einsum('pa,pab->pb',U,ne)
 dr=np.einsum('pab,pb->pa',dP,s['phi'])
 # Raw terms and TERMwise absolute contraction sums, before any integration/cancellation.
 mterms=[raise_cov(hi,s['V'])*dV/om[:,None,None]**2,
  -raise_cov(hi,z)*zeta,-(s['z2']/((B*GC)**2*s['xi'][:,None]**4))[:,:,None]*raise_cov(hi,z)*zeta,
  -ELL**2*np.einsum('pac,jpcd,pdb->jpab',hi,s['D'],hi)*dD,
  da[None,:,:]*z+s['a'][None,:,:]*zeta]
 md=np.stack([np.sum(t,axis=tuple(range(2,t.ndim))) for t in mterms],axis=-1)
 me=np.stack([np.sum(abs(t),axis=tuple(range(2,t.ndim))) for t in mterms],axis=-1)
 mx=-ALPHA*s['Fup']*dF/2;ph=-raise_cov(hi,s['r'])*dr
 terms=np.column_stack((mx.sum(axis=(1,2)),ph.sum(axis=1),np.einsum('j,jpk->pk',w,md)))
 env=np.column_stack((abs(mx).sum(axis=(1,2)),abs(ph).sum(axis=1),np.einsum('j,jpk->pk',w,me)))
 weakU=np.sum(s['A']*eta,axis=1)+np.sum(s['PiU']*ne,axis=(1,2))
 potential=w[:,None]*np.sum((s['a'][None,:,:]-s['f'][:,:,None]*raise_cov(hi,z))*zeta,axis=-1)
 weakmode=potential+np.einsum('jpab,jpab->jp',s['Pi'],nzeta)
 unitjet=2*(np.einsum('pab,pb->pa',lower_last(g,s['nu']),eta)+np.einsum('pb,pab->pa',s['uc'],ne))
 constraint=np.column_stack((2*np.einsum('pa,pa->p',s['uc'],eta),unitjet))
 dc=np.einsum('pa,jpa->jp',eta,z)+np.einsum('pa,jpa->jp',U,zeta)
 ddc=np.einsum('pab,jpb->jpa',ne,z)+np.einsum('pb,jpab->jpa',eta,s['nz'])+np.einsum('pab,jpb->jpa',s['nu'],zeta)+np.einsum('pb,jpab->jpa',U,nzeta)
 RAW.update(current_eta=eta,current_eta_partial=deta,current_zeta=zeta,current_zeta_partial=dzeta,current_direct_terms=terms,current_envelope=env,current_weakU=weakU,current_weakmode=weakmode,current_mode_envelope=me,current_constraint=constraint,current_delta_transverse=dc,current_delta_transverse_jet=ddc)
 return terms,env,md,weakU,weakmode,constraint,dc,ddc

def trial_point(r,z,x,odd,xi,w,omega,shapes,R,Z,sel):
 val,dr,dz=interpolate(x,shapes);ov,orr,oz=interpolate(odd,shapes)
 Phi=B*val[0][sel];gr=np.zeros((len(R),4));gr[:,1]=B*dr[0][sel];gr[:,2]=B*dz[0][sel]
 beta=ov[0][sel];chi=ov[1][sel];br=np.zeros_like(gr);cr=np.zeros_like(gr)
 br[:,1]=orr[0][sel];br[:,2]=oz[0][sel];cr[:,1]=orr[1][sel];cr[:,2]=oz[1][sel]
 g,hi,dg,Ga,n,rho=metric(R,Phi,gr,beta,br);c=np.cosh(chi);ss=np.sinh(chi)
 U=np.zeros((len(R),4));U[:,0]=c/n;U[:,3]=ss/rho-beta*c/n;du=np.zeros((len(R),4,4))
 E=np.zeros_like(U);E[:,0]=ss/n;E[:,3]=c/rho-beta*ss/n;de=np.zeros_like(du)
 for a in (1,2):
  lr=(1/R if a==1 else 0)-gr[:,a]
  du[:,a,0]=(ss*cr[:,a]-c*gr[:,a])/n
  du[:,a,3]=(c*cr[:,a]-ss*lr)/rho-br[:,a]*c/n-beta*du[:,a,0]
  de[:,a,0]=(c*cr[:,a]-ss*gr[:,a])/n
  de[:,a,3]=(ss*cr[:,a]-c*lr)/rho-br[:,a]*ss/n-beta*de[:,a,0]
 zz=np.zeros((32,len(R),4));pz=np.zeros((32,len(R),4,4));sw=np.sqrt(w)[:,None]
 zz[:,:,1]=B*val[1::2][:,sel]/sw;zz[:,:,2]=B*val[2::2][:,sel]/sw
 for a,der in ((1,dr),(2,dz)):
  pz[:,:,a,1]=B*der[1::2][:,sel]/sw;pz[:,:,a,2]=B*der[2::2][:,sel]/sw
 phi=np.zeros_like(U);phi[:,0]=QBAR
 s=features(g,hi,Ga,U,du,zz,pz,phi,omega,xi,w);s.update(R=R,Z=Z,Phi=Phi,gr=gr,n=n,rho=rho,E=E,de=de)
 return s

def selected_arrays(file,names):
 out={}
 with np.load(path(file),allow_pickle=False) as f:
  for k in names:
   a=f[k].copy();RAW['loaded_'+k]=a
   assert a.dtype==np.dtype('float64') and np.all(np.isfinite(a));out[k]=a
 return out

def merged_inputs():
 ins={}
 def add(n,h):
  n=str(path(n).resolve());assert n not in ins or ins[n]==h;ins[n]=h
 for n,h in PINS.items():add(n,h)
 add(STEM+'.md',PROTOCOL_SHA)
 add(str(Path(__file__).resolve()),sha(__file__))
 for name in (BAND+'_RECEIPT.json',ODD+'_RECEIPT.json',COMPACT+'_RECEIPT.json'):
  r=json.loads(path(name).read_text());assert r['status']=='CLOSED' and r['closed']
  for key in ('input_sha256','output_sha256'):
   for n,h in r[key].items():add(n,h)
 for n,h in ins.items():assert sha(path(n))==h,('Input changed',n)
 return ins

def admission():
 ins=merged_inputs();r=json.loads(path(BAND+'_RECEIPT.json').read_text());b=json.loads(path(BAND+'_RESULT.json').read_text())
 assert r['owner']['pid']==88234 and b['owner']==r['owner'] and b['status']=='CONDITIONAL_LINEAR_PASS'
 assert sha(path(BAND+'_RESULT.json'))==r['result_sha256']
 assert [v['sigma'] for v in b['cases']]==list(SIGMAS) and len(b['controls'])==22 and all(v['passed'] for v in b['controls'])
 for i,c in enumerate(b['cases']):
  pc=c['assembly_checkpoint']['metadata']['parent_coefficient'];assert pc['file']==COEFFICIENT_FILES[i] and pc['sha256']==PINS[pc['file']] and pc['commit_sha256']==PINS[pc['commit_file']]
  assert c['status']=='LINEAR_PASS' and c['INFO']==0 and c['original_residual']<=1e-10
  rec=c['final_checkpoint'];assert r['output_sha256'][rec['file']]==rec['sha256'] and r['output_sha256'][rec['commit_file']]==rec['commit_sha256']
  assert json.loads(path(rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
 shared=json.loads(path('CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RESULT.json').read_text());fixed=dict(shared['manifest']['fixed_parent']);fixed['eps']=1e-5
 cp=json.loads(path('CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_EPS_1em05_CP.json').read_text());assert cp==next(v for v in shared['rows'] if v['eps']==1e-5)
 assert fixed['eps']==1e-5 and fixed['Q0_over_Hstar']==100 and abs(KB-(2-C))<1e-16
 cr=json.loads(path(COMPACT+'_RECEIPT.json').read_text());assert cr['owner']['owner']=='root' and cr['owner']['pid']==94158
 cf=COMPACT+'_00000_INPUT.npz';cm=json.loads(path(cf+'.COMMIT.json').read_text())
 assert cm['file']==cf and cm['sha256']==PINS[cf]==cr['output_sha256'][cf]
 assert cr['output_sha256'][cf+'.COMMIT.json']==PINS[cf+'.COMMIT.json'] and cm['metadata']['owner']==cr['owner']
 inherited_fixed=cm['metadata']['fixed'];assert inherited_fixed['eps']==1e-6
 assert {k:v for k,v in inherited_fixed.items() if k!='eps'}=={k:v for k,v in fixed.items() if k!='eps'}
 assert cm['metadata']['physical_changes']==[] and all(v is False for v in cm['metadata']['qualification'].values())
 assert len(cm['metadata']['copied_band_controls'])==22 and len(cm['metadata']['copied_original_controls'])==21 and len(cm['metadata']['copied_original_failures'])==4
 assert cm['metadata']['copied_band_controls']==b['controls'] and cm['metadata']['copied_original_controls']==b['copied_parent_controls']
 expected=dict(r_kpc=[87],z_kpc=[45],final_state=[65,87,45],xi=[32],weights=[32],source_samples16=[2416,9],source_samples32=[4832,9])
 assert cm['metadata']['schema']=={k:dict(shape=v,dtype='float64',finite=True) for k,v in expected.items()}
 return ins,b,fixed,cp,cm

def metric_partial(s):
 # Metric compatibility recovers the same exact first metric jet, no second derivatives.
 a=np.einsum('plam,pln->pamn',s['Ga'],s['g'])
 return a+np.swapaxes(a,2,3)

def connection_delta(s,q,dq):
 nq=dq-np.einsum('plam,pln->pamn',s['Ga'],q)-np.einsum('plan,pml->pamn',s['Ga'],q)
 dG=np.zeros_like(s['Ga'])
 for a in range(4):
  for b in range(4):dG[:,:,a,b]=np.einsum('plm,pm->pl',s['hi'],nq[:,a,b,:]+nq[:,b,a,:]-nq[:,:,a,b])/2
 return dG

def normalized_lift(s,q,dq):
 dg=metric_partial(s);U=s['U'];du=s['du'];v=np.einsum('pa,pab,pb->p',U,q,U)
 dv=np.einsum('pamn,pm,pn->pa',dq,U,U)+2*np.einsum('pmn,pm,pan->pa',q,U,du)
 eta=v[:,None]*U/2;deta=dv[:,:,None]*U[:,None,:]/2+v[:,None,None]*du/2
 ucpartial=np.einsum('pamn,pn->pam',dg,U)+lower_last(s['g'],du)
 unit=v+2*np.sum(s['uc']*eta,axis=-1)
 jet=dv+2*np.einsum('pam,pm->pa',ucpartial,eta)+2*np.einsum('pm,pam->pa',s['uc'],deta)
 transverse=np.einsum('pa,jpa->jp',eta,s['z'])
 tj=np.einsum('pab,jpb->jpa',deta,s['z'])+np.einsum('pb,jpab->jpa',eta,s['dz'])
 return eta,deta,np.concatenate((unit.ravel(),jet.ravel(),transverse.ravel(),tj.ravel()))

def metric_native(s,q,dq,eta,deta):
 hi,g,U,z,P=s['hi'],s['g'],s['U'],s['z'],s['P'];w=s['w'];om=s['omega'];kj=(B*GC)**2*s['xi'][:,None]**4
 dG=connection_delta(s,q,dq);dhi=-np.einsum('pac,pcd,pdb->pab',hi,q,hi)
 dnu=deta+np.einsum('pbal,pl->pab',dG,U)+np.einsum('pbal,pl->pab',s['Ga'],eta)
 dnz=-np.einsum('plab,jpl->jpab',dG,z)
 duc=lower(q,U)+lower(g,eta);dP=np.einsum('pa,pb->pab',duc,U)+np.einsum('pa,pb->pab',s['uc'],eta)
 dqq=np.einsum('pa,jpab->jpb',eta,s['nz'])+np.einsum('pa,jpab->jpb',U,dnz)
 dV=np.einsum('pab,jpb->jpa',dP,s['q'])+np.einsum('pab,jpb->jpa',P,dqq)
 dD=np.einsum('pac,jpcd,pbd->jpab',dP,s['nz'],P)+np.einsum('pac,jpcd,pbd->jpab',P,dnz,P)+np.einsum('pac,jpcd,pbd->jpab',P,s['nz'],dP)
 lower_nu=lower_last(q,s['nu'])+lower_last(g,dnu);dF=lower_nu-np.swapaxes(lower_nu,1,2)
 da=np.einsum('pa,pab->pb',eta,s['nu'])+np.einsum('pa,pab->pb',U,dnu);dr=np.einsum('pab,pb->pa',dP,s['phi'])
 z2=s['z2'];V2=covdot(hi,s['V'],s['V']);F2=np.sum(s['Fup']*s['F'],axis=(1,2));r2=covdot(hi,s['r'],s['r'])
 Du=np.einsum('pac,jpcd,pdb->jpab',hi,s['D'],hi);D2=np.sum(Du*s['D'],axis=(2,3));az=np.einsum('pa,jpa->jp',s['a'],z)
 dz2=covdot(dhi,z,z);dV2=covdot(dhi,s['V'],s['V'])+2*covdot(hi,s['V'],dV)
 dD2=2*np.sum(Du*dD,axis=(2,3))+np.einsum('pac,jpab,pbd,jpcd->jp',dhi,s['D'],hi,s['D'])+np.einsum('pac,jpab,pbd,jpcd->jp',hi,s['D'],dhi,s['D'])
 dF2=2*np.sum(s['Fup']*dF,axis=(1,2))+np.einsum('pac,pab,pbd,pcd->p',dhi,s['F'],hi,s['F'])+np.einsum('pac,pab,pbd,pcd->p',hi,s['F'],dhi,s['F'])
 dr2=covdot(dhi,s['r'],s['r'])+2*covdot(hi,s['r'],dr);daz=np.einsum('pa,jpa->jp',da,z)
 modal=np.stack((V2/(2*om[:,None]**2),-z2/2,-z2*z2/(4*kj),-ELL**2*D2/2,az),axis=-1)
 dm=np.stack((dV2/(2*om[:,None]**2),-dz2/2,-z2*dz2/(2*kj),-ELL**2*dD2/2,daz),axis=-1)
 primal=np.column_stack((-ALPHA*F2/4,-r2/2,np.einsum('j,jpk->pk',w,modal)))
 derivative=np.column_stack((-ALPHA*dF2/4,-dr2/2,np.einsum('j,jpk->pk',w,dm)))
 lm=np.einsum('pab,pba->p',hi,q)/2
 total=derivative+lm[:,None]*primal
 # Sum absolute tensor products BEFORE contractions or inter-term cancellation.
 def quad_env(hh,v):return np.einsum('pab,jpa,jpb->jp',abs(hh),abs(v),abs(v))
 ez=quad_env(hi,z);ev=quad_env(hi,s['V']);ed=np.einsum('pac,jpab,pbd,jpcd->jp',abs(hi),abs(s['D']),abs(hi),abs(s['D']))
 edz=quad_env(dhi,z);edv=quad_env(dhi,s['V'])+2*np.sum(abs(raise_cov(hi,s['V'])*dV),axis=-1)
 edd=2*np.sum(abs(Du*dD),axis=(2,3))+np.einsum('pac,jpab,pbd,jpcd->jp',abs(dhi),abs(s['D']),abs(hi),abs(s['D']))+np.einsum('pac,jpab,pbd,jpcd->jp',abs(hi),abs(s['D']),abs(dhi),abs(s['D']))
 ef=np.einsum('pac,pab,pbd,pcd->p',abs(hi),abs(s['F']),abs(hi),abs(s['F']))
 edf=2*np.sum(abs(s['Fup']*dF),axis=(1,2))+np.einsum('pac,pab,pbd,pcd->p',abs(dhi),abs(s['F']),abs(hi),abs(s['F']))+np.einsum('pac,pab,pbd,pcd->p',abs(hi),abs(s['F']),abs(dhi),abs(s['F']))
 er=np.einsum('pab,pa,pb->p',abs(hi),abs(s['r']),abs(s['r']));edr=np.einsum('pab,pa,pb->p',abs(dhi),abs(s['r']),abs(s['r']))+2*np.sum(abs(raise_cov(hi,s['r'])*dr),axis=-1)
 mp=np.stack((ev/(2*om[:,None]**2),ez/2,ez*ez/(4*kj),ELL**2*ed/2,np.sum(abs(s['a'][None,:,:]*z),axis=-1)),axis=-1)
 em=np.stack((edv/(2*om[:,None]**2),edz/2,ez*edz/(2*kj),ELL**2*edd/2,np.sum(abs(da[None,:,:]*z),axis=-1)),axis=-1)
 el=np.einsum('pab,pba->p',abs(hi),abs(q))/2
 penv=np.column_stack((ALPHA*ef/4,er/2,np.einsum('j,jpk->pk',w,mp)))
 denv=np.column_stack((ALPHA*edf/4,edr/2,np.einsum('j,jpk->pk',w,em)))
 env=denv+el[:,None]*penv
 per_mode=w[:,None,None]*(dm+lm[None,:,None]*modal)
 menv=w[:,None,None]*(em+el[None,:,None]*mp)
 operands=dict(delta_connection=dG,delta_inverse=dhi,delta_U=eta,delta_U_partial=deta,log_measure_tangent=lm,raw_native_primal=primal,raw_native_no_measure=derivative,per_mode_metric_terms=per_mode,per_mode_metric_envelope=menv)
 RAW.update({'current_metric_'+k:v for k,v in operands.items()})
 return total,env,operands

def pressure(s,q,fixed):
 X2=-covdot(s['hi'],s['phi'],s['phi']);eta=fixed['Hunit']/LIGHT;Q0=100*eta;ep=1e-5;norm=1/ep-math.log1p(1/ep);s0=.5*ep*norm*fixed['d0'];target=s0
 for _ in range(12):
  q0=math.sqrt(1+ep*s0/(1+s0));dq0=ep/(2*q0*(1+s0)**2);s0-=(s0*q0-target)/(q0+s0*dq0)
 u0=ep*s0/(1+s0);u=u0+(1+u0)*np.expm1(-2*s['Phi']);qq=np.sqrt(1+u)
 RAW.update(current_phase_X2=X2,current_phase_q=qq,current_phase_q2_minus1=u)
 assert np.all(np.isfinite(u)) and np.all((u>0)&(u<ep))
 ss=u/(ep-u);Abar=1.5*fixed['OA']/fixed['rG'];fac=2*eta*eta/C
 pe=(np.log1p(ss)-ss/(1+ss))/norm;dp=2*qq*ss/(ep*norm)
 P=fac*Abar*(pe-1);W=fac*Abar*qq*dp
 raised=raise_cov(s['hi'],s['phi']);dlnX=np.einsum('pa,pab,pb->p',raised,q,raised)/(2*X2);lm=np.einsum('pab,pba->p',s['hi'],q)/2
 value=W*dlnX+P*lm;env=abs(W)*np.einsum('pa,pab,pb->p',abs(raised),abs(q),abs(raised))/(2*X2)+abs(P)*np.einsum('pab,pba->p',abs(s['hi']),abs(q))/2
 return value,env,dict(Pstar=P,Wstar=W,X2=X2,delta_lnX=dlnX,phase_measure_term=P*lm,phase_clock_term=W*dlnX)

def einstein(s,q,dq):
 g,hi,Ga=s['g'],s['hi'],s['Ga'];R=s['R'];dg=metric_partial(s);dG=connection_delta(s,q,dq)
 dhi=-np.einsum('pac,pcd,pdb->pab',hi,q,hi);di=-np.einsum('pac,pdce,peb->pdab',hi,dg,hi)
 ddi=np.zeros_like(di)
 for a in range(4):ddi[:,a]=-np.einsum('pbc,pcd,pde->pbe',di[:,a],q,hi)-np.einsum('pbc,pcd,pde->pbe',hi,dq[:,a],hi)-np.einsum('pbc,pcd,pde->pbe',hi,q,di[:,a])
 ratio=np.sqrt(-np.linalg.det(g))/R;lm=np.einsum('pab,pba->p',hi,q)/2
 lr=np.einsum('pab,pdba->pd',hi,dg)/2;lr[:,1]-=1/R;dratio=ratio[:,None]*lr
 dlm=(np.einsum('pdab,pba->pd',di,q)+np.einsum('pab,pdba->pd',hi,dq))/2
 vr=ratio*lm;dvr=dratio*lm[:,None]+ratio[:,None]*dlm
 V=ratio[:,None,None]*hi;dV=vr[:,None,None]*hi+ratio[:,None,None]*dhi
 DV=dratio[:,:,None,None]*hi[:,None,:,:]+ratio[:,None,None,None]*di
 dDV=dvr[:,:,None,None]*hi[:,None,:,:]+dratio[:,:,None,None]*dhi[:,None,:,:]+vr[:,None,None,None]*di+ratio[:,None,None,None]*ddi
 bar=np.zeros_like(Ga);bar[:,1,3,3]=-R;bar[:,3,1,3]=bar[:,3,3,1]=1/R
 DV+=np.einsum('pman,pnb->pamb',bar,V)+np.einsum('pban,pmn->pamb',bar,V)
 dDV+=np.einsum('pman,pnb->pamb',bar,dV)+np.einsum('pban,pmn->pamb',bar,dV)
 cc=Ga-bar;tr=np.einsum('plml->pm',cc);dtr=np.einsum('plml->pm',dG)
 aa=np.einsum('plmn,pl->pmn',cc,tr)-np.einsum('prml,plnr->pmn',cc,cc)
 daa=np.einsum('plmn,pl->pmn',dG,tr)+np.einsum('plmn,pl->pmn',cc,dtr)-np.einsum('prml,plnr->pmn',dG,cc)-np.einsum('prml,plnr->pmn',cc,dG)
 e1=-np.einsum('plmn,plmn->p',DV,cc);e2=np.einsum('pnmn,pm->p',DV,tr);e3=np.einsum('pmn,pmn->p',V,aa)
 de1=-np.einsum('plmn,plmn->p',dDV,cc)-np.einsum('plmn,plmn->p',DV,dG)
 de2=np.einsum('pnmn,pm->p',dDV,tr)+np.einsum('pnmn,pm->p',DV,dtr)
 de3=np.einsum('pmn,pmn->p',dV,aa)+np.einsum('pmn,pmn->p',V,daa)
 terms=np.column_stack((de1,de2,de3))/(2*C);raw=dict(reference_connection=bar,connection_difference=cc,reference_V=V,reference_DV=DV,EH_delta_V=dV,EH_delta_DV=dDV,EH_delta_C=dG,EH_terms=terms,EH_primal_terms=np.column_stack((e1,e2,e3))/(2*C))
 RAW.update({'current_'+k:v for k,v in raw.items()})
 etr=np.einsum('plml->pm',abs(cc));edtr=np.einsum('plml->pm',abs(dG))
 eaa=np.einsum('plmn,pl->pmn',abs(cc),etr)+np.einsum('prml,plnr->pmn',abs(cc),abs(cc))
 edaa=np.einsum('plmn,pl->pmn',abs(dG),etr)+np.einsum('plmn,pl->pmn',abs(cc),edtr)+np.einsum('prml,plnr->pmn',abs(dG),abs(cc))+np.einsum('prml,plnr->pmn',abs(cc),abs(dG))
 e1=np.einsum('plmn,plmn->p',abs(dDV),abs(cc))+np.einsum('plmn,plmn->p',abs(DV),abs(dG))
 e2=np.einsum('pnmn,pm->p',abs(dDV),etr)+np.einsum('pnmn,pm->p',abs(DV),edtr)
 e3=np.einsum('pmn,pmn->p',abs(dV),eaa)+np.einsum('pmn,pmn->p',abs(V),edaa)
 raw['EH_component_envelopes']=np.column_stack((e1,e2,e3))/(2*C);env=raw['EH_component_envelopes'].sum(axis=1)
 raw['EH_uncancelled_envelope']=env
 return terms.sum(axis=1),env,raw

def tetrad_direction(s,box,a,b):
 R=s['R'];f,fr,fz=compact(R,s['Z'],box);df=np.zeros((len(R),4));df[:,1]=fr;df[:,2]=fz
 if (a==2)!=(b==2):
  df[:,1]=s['Z']/16*fr;df[:,2]=f/16+s['Z']/16*fz;f=s['Z']/16*f
 co=np.zeros((len(R),4,4));dco=np.zeros((len(R),4,4,4));n=s['n'];rho=s['rho'];gr=s['gr'];beta=s['g'][:,0,3]/rho**2
 co[:,0,0]=n;co[:,1,1]=co[:,2,2]=1/n;co[:,3,0]=rho*beta;co[:,3,3]=rho
 dg=metric_partial(s);br=np.zeros_like(gr)
 for k in (1,2):
  lr=(1/R if k==1 else 0)-gr[:,k];br[:,k]=(dg[:,k,0,3]-2*lr*s['g'][:,0,3])/rho**2
  dco[:,k,0,0]=n*gr[:,k];dco[:,k,1,1]=dco[:,k,2,2]=-gr[:,k]/n
  dco[:,k,3,0]=rho*(lr*beta+br[:,k]);dco[:,k,3,3]=rho*lr
 tensor=np.einsum('pm,pn->pmn',co[:,a],co[:,b]);jet=np.einsum('pam,pn->pamn',dco[:,:,a],co[:,b])+np.einsum('pm,pan->pamn',co[:,a],dco[:,:,b])
 if a!=b:tensor+=np.swapaxes(tensor,1,2);jet+=np.swapaxes(jet,2,3)
 return f[:,None,None]*tensor,df[:,:,None,None]*tensor[:,None,:,:]+f[:,None,None,None]*jet,f

def connection_from_first_metric(g,hi,dg):
 out=np.zeros_like(dg)
 for a in range(4):
  for b in range(4):out[:,:,a,b]=np.einsum('plm,pm->pl',hi,dg[:,a,b,:]+dg[:,b,a,:]-dg[:,:,a,b])/2
 return out

def independent_gravity_fixtures():
 # All constants below are arithmetic fixtures, not an actual expansion history.
 R=np.array([3.]);Phi=1/20;Psi=1/30;aa=np.array([0.,1/7,1/11,0.]);bb=np.array([0.,1/13,-1/17,0.]);nu=1/19;ps=-1/23;gn=np.array([0.,1/29,-1/31,0.]);gp=np.array([0.,1/37,1/41,0.])
 n=math.exp(Phi);m=math.exp(-2*Psi);g=np.diag([-n*n,m,m,m*9])[None,:,:];hi=np.diag([-1/n**2,1/m,1/m,1/(m*9)])[None,:,:]
 dg=np.zeros((1,4,4,4));q=np.zeros_like(g);dq=np.zeros_like(dg)
 q[:,0,0]=2*nu*g[:,0,0]
 for j in (1,2,3):q[:,j,j]=-2*ps*g[:,j,j]
 for a in range(4):
  dg[:,a,0,0]=2*aa[a]*g[:,0,0];dq[:,a,0,0]=2*gn[a]*g[:,0,0]+2*nu*dg[:,a,0,0]
  for j in (1,2,3):
   dg[:,a,j,j]=(-2*bb[a]+(2/3 if a==1 and j==3 else 0))*g[:,j,j]
   dq[:,a,j,j]=-2*gp[a]*g[:,j,j]-2*ps*dg[:,a,j,j]
 Ga=connection_from_first_metric(g,hi,dg);s=dict(g=g,hi=hi,Ga=Ga,R=R)
 val,env,raw=einstein(s,q,dq)
 expected=math.exp(Phi-Psi)/C*((nu-ps)*(np.sum(bb*bb)-2*np.sum(aa*bb))+2*np.sum(bb*gp)-2*np.sum(gn*bb)-2*np.sum(aa*gp))
 RAW.update(static_EH_g=g,static_EH_dg=dg,static_EH_q=q,static_EH_dq=dq,static_EH_a=aa,static_EH_b=bb,static_EH_delta_a=gn,static_EH_delta_b=gp)
 ARM_AVAILABLE.update({'static_fixture_'+k:v.copy() for k,v in raw.items()});check('independent_static_conformal_EH',val,np.array([expected]),env)
 a=7/6;H=1/17;g=np.diag([-1.,a*a,a*a,9*a*a])[None,:,:];hi=np.diag([-1.,1/a**2,1/a**2,1/(9*a*a)])[None,:,:];dg=np.zeros((1,4,4,4))
 for j in (1,2,3):dg[:,0,j,j]=2*H*g[:,j,j]
 dg[:,1,3,3]=2*g[:,3,3]/3;s=dict(g=g,hi=hi,Ga=connection_from_first_metric(g,hi,dg),R=R)
 for label,l,ss,sd in (('lapse',1/11,0.,0.),('spatial',0.,1/13,1/19)):
  q=np.zeros_like(g);dq=np.zeros_like(dg);q[:,0,0]=-2*l
  for j in (1,2,3):q[:,j,j]=2*ss*g[:,j,j];dq[:,0,j,j]=2*ss*dg[:,0,j,j]+2*sd*g[:,j,j]
  dq[:,1,3,3]=2*q[:,3,3]/3
  val,env,raw=einstein(s,q,dq);expected=a**3*(3*H*H*l-3*(3*H*H*ss+2*H*sd))/C
  ARM_AVAILABLE.update({f'FLRW_{label}_'+k:v.copy() for k,v in raw.items()});ARM_AVAILABLE.update({f'FLRW_{label}_'+k:v.copy() for k,v in dict(g=g,dg=dg,q=q,dq=dq).items()})
  check('independent_FLRW_EH_'+label,val,np.array([expected]),env)
 g=np.diag([-1.,1.,1.,1.])[None,:,:];hi=g.copy();Ga=np.zeros((1,4,4,4));q=np.array([[[1/7,1/11,0.,1/13],[1/11,-1/17,1/19,0.],[0.,1/19,1/23,0.],[1/13,0.,0.,-1/29]]]);dq=np.zeros((1,4,4,4));dq[:,1]=q/31;dq[:,0]=q/37
 dG=connection_delta(dict(g=g,hi=hi,Ga=Ga),q,dq);expected=np.zeros_like(dG)
 for l in range(4):
  for j in range(4):
   for k in range(4):expected[:,l,j,k]=hi[:,l,l]*(dq[:,j,l,k]+dq[:,k,l,j]-dq[:,l,j,k])/2
 RAW.update(flat_fixture_metric=g,flat_fixture_q=q,flat_fixture_dq=dq,flat_fixture_delta_Gamma=dG)
 check('independent_flat_connection_jet',dG,expected,np.ones_like(dG))
 dhi=-np.einsum('pac,pcd,pdb->pab',hi,q,hi);actual=np.einsum('pac,pcb->pab',dhi,g)+np.einsum('pac,pcb->pab',hi,q)
 check('independent_inverse_metric_jet',actual,np.zeros_like(actual),np.ones_like(actual));RAW.update(flat_fixture_metric=g,flat_fixture_q=q,flat_fixture_dq=dq,flat_fixture_delta_Gamma=dG)

def per_arm_fixtures(xi,w,om,sigma):
 g=np.diag([-1.,1.,1.,1.])[None,:,:];hi=g.copy();Ga=np.zeros((1,4,4,4));U=np.array([[1.,0.,0.,0.]]);du=np.zeros((1,4,4));z=np.zeros((32,1,4));dz=np.zeros((32,1,4,4));phi=np.array([[QBAR,0.,0.,0.]])
 z[:,:,1]=B*xi[:,None]**2/3;s=features(g,hi,Ga,U,du,z,dz,phi,om,xi,w);q=np.zeros_like(g);q[:,1,1]=1/7;dq=np.zeros((1,4,4,4))
 eta,de,_=normalized_lift(s,q,dq);val,env,raw=metric_native(s,q,dq,eta,de);zz=(B*xi[:,None]**2/3)**2;kj=(B*GC)**2*xi[:,None]**4
 expected=w[:,None]*(1/7)*(zz/4+3*zz*zz/(8*kj))
 ARM_AVAILABLE.update({'fixture_potential_'+k:v.copy() for k,v in raw.items()});check(f's{sigma}_independent_metric_potential',raw['per_mode_metric_terms'][:,:,1:3].sum(axis=-1),expected,raw['per_mode_metric_envelope'][:,:,1:3].sum(axis=-1))
 dz[:,:,0,1]=B*xi[:,None]**2/5;s=features(g,hi,Ga,U,du,z,dz,phi,om,xi,w);q=np.zeros_like(g);q[:,0,0]=1/11;eta,de,_=normalized_lift(s,q,dq);val,env,raw=metric_native(s,q,dq,eta,de)
 expected=w[:,None]*(1/11)*(B*xi[:,None]**2/5)**2/(4*om[:,None]**2)
 ARM_AVAILABLE.update({'fixture_inertia_'+k:v.copy() for k,v in raw.items()});check(f's{sigma}_independent_metric_inertia',raw['per_mode_metric_terms'][:,:,0],expected,raw['per_mode_metric_envelope'][:,:,0])

def sheet_point(even,odd,samples):
 r=even['r_kpc'];z=even['z_kpc'];R=samples[:,0];ix=np.searchsorted(r,R,side='right')-1;assert np.all((ix>=0)&(ix<len(r)-1));d=r[ix+1]-r[ix];t=(R-r[ix])/d
 def at(v):
  a=(1-t)*v[ix,0]+t*v[ix+1,0];gr=(v[ix+1,0]-v[ix,0])/d
  gz=((1-t)*(v[ix,1]-v[ix,0])+t*(v[ix+1,1]-v[ix+1,0]))/(z[1]-z[0]);return a,gr,gz
 ph,pr,pz=at(B*even['final_state'][0]);beta,br,bz=at(odd[0]);gr=np.zeros((len(R),4));bg=np.zeros_like(gr);gr[:,1]=pr;gr[:,2]=pz;bg[:,1]=br;bg[:,2]=bz
 g,hi,dg,Ga,n,rho=metric(R,ph,gr,beta,bg);Omega0=np.exp(samples[:,2])*samples[:,4]/samples[:,6];k=np.zeros((len(R),4));k[:,0]=1;k[:,3]=Omega0
 D=-np.einsum('pa,pab,pb->p',k,g,k);RAW.update(source_held_Omega0=Omega0,source_metric=g,source_metric_jet=dg,source_k=k,source_D=D)
 assert np.all(np.isfinite(D)) and np.all(D>0),'Held ordinary worldline is not timelike; no clipping.'
 speed=rho*(Omega0+beta)/n;Gamma=n/np.sqrt(D);force=-np.einsum('pamn,pm,pn->pa',dg,k,k)/(2*D[:,None])
 # Surface rest density and current use the same fixed-coordinate annulus once.
 area=np.sqrt(g[:,1,1])*rho;Dsig=samples[:,1]*R/area;Srest=Dsig/Gamma;ut=1/np.sqrt(D);mass_identity=n*area*Srest*ut/R
 mean=force.copy();mean[:,2]=0.
 out=dict(R=R,Z=np.zeros(len(R)),g=g,hi=hi,Ga=Ga,n=n,rho=rho,gr=gr,k=k,D=D,Gamma=Gamma,speed=speed,held_Omega0=Omega0,normal_rest_surface_density=Dsig,proper_rest_surface_density=Srest,rest_mass_annulus_identity=mass_identity,radial_material_Euler=force[:,1],material_Euler_reflected_mean=mean,vertical_sheet_contact_plus=force[:,2],vertical_sheet_contact_minus=-force[:,2],vertical_sheet_reflected_mean=np.zeros(len(R)))
 return out

def independent_relative_fixture(xi,w):
 g=np.diag([-1.,1.,1.,1.])[None,:,:];U=np.array([[math.sqrt(17)/4,1/4,0.,0.]]);z=np.zeros((32,1,4));du=np.zeros((1,4,4));dz=np.zeros((32,1,4,4));phi=np.array([[3/20,0.,0.,0.]])
 s=features(g,g.copy(),np.zeros((1,4,4,4)),U,du,z,dz,phi,np.ones(32),xi,w);q=np.array([[[1/7,1/11,0.,0.],[1/11,1/13,0.,0.],[0.,0.,-1/17,0.],[0.,0.,0.,1/19]]]);dq=np.zeros((1,4,4,4));eta,de,_=normalized_lift(s,q,dq)
 val,env,raw=metric_native(s,q,dq,eta,de);r=raise_cov(s['hi'],s['r']);Q=np.sum(U*phi,axis=1);rr=covdot(s['hi'],s['r'],s['r']);lm=np.einsum('pab,pba->p',s['hi'],q)/2
 expected=np.einsum('pa,pab,pb->p',r,q,r)/2-Q*np.einsum('pa,pab,pb->p',r,q,U)-rr*lm/2
 ARM_AVAILABLE.update({'tilted_relative_'+k:v.copy() for k,v in dict(g=g,U=U,phi=phi,q=q,r=s['r'],projector=s['P'],delta_U=eta).items()});check('independent_tilted_relative_metric_contact',val[:,1],expected,env[:,1])

def source_registration_controls(even,source):
 R=source[:,0];r=even['r_kpc'];ix=np.searchsorted(r,R,side='right')-1;assert np.all((ix>=0)&(ix<len(r)-1));dr=r[ix+1]-r[ix];t=(R-r[ix])/dr;psi=even['final_state'][0,:,0]
 Phi=B*((1-t)*psi[ix]+t*psi[ix+1]);pr=B*(psi[ix+1]-psi[ix])/dr;u=R*pr;v=source[:,4];N=np.exp(Phi);rho=R/N;Omega0=np.exp(source[:,2])*v/source[:,6]
 force=-2*N*N*pr+2*rho*rho*(1/R-pr)*Omega0**2;envelope=2*N*N*abs(pr)+2*rho*rho*abs((1/R-pr)*Omega0**2)
 actual=np.column_stack((source[:,2],source[:,3],v*v,source[:,5],force));expected=np.column_stack((Phi,u,u/(1-u),1/np.sqrt(1-v*v),np.zeros(len(R))))
 env=np.column_stack((np.ones(len(R)),np.ones(len(R)),np.ones(len(R)),np.ones(len(R)),envelope))
 RAW.update(parent_source_held_Omega0=Omega0,parent_source_original_Phi=Phi,parent_source_original_u=u,parent_source_geodesic_force=force,parent_source_geodesic_envelope=envelope)
 scales=np.empty_like(actual);scales[:,:4]=np.maximum(np.maximum(np.max(abs(actual[:,:4]),axis=0),np.max(abs(expected[:,:4]),axis=0)),1e-30)
 scales[:,4]=np.maximum(envelope,1e-30);env[:,:4]=scales[:,:4]
 RAW.update(parent_source_registration_actual=actual,parent_source_registration_expected=expected,parent_source_registration_envelope=env,parent_source_registration_column_scale=scales)
 check('unchanged_parent_exact_conformal_source',actual/scales,expected/scales,env/scales)

def arm(case,even,source,xi,w,fixed):
 global RAW,ARM_AVAILABLE
 RAW={};ARM_AVAILABLE={};CONTEXT.update(stage='metric_arm',sigma=case['sigma']);begin=len(CHECKS);sigma=case['sigma'];r,z,x=even['r_kpc'],even['z_kpc'],even['final_state']
 odd=selected_arrays(case['final_checkpoint']['file'],('physical_beta_chi',))['physical_beta_chi'];assert odd.shape==(2,87,45) and np.all(odd[:,-1]==0) and np.all(odd[:,:,-1]==0) and np.array_equal(odd[0,0],odd[0,1]) and np.all(odd[1,0]==0)
 om=sigma*xi*fixed['Hunit']/LIGHT;oldomega=selected_arrays(COEFFICIENT_FILES[SIGMAS.index(sigma)],('omega_star',))['omega_star'];check(f's{sigma}_inherited_frequency',om,oldomega);per_arm_fixtures(xi,w,om,sigma)
 AR=ARM_AVAILABLE;AR.update(physical_beta_chi=odd.copy(),omega_star=om.copy(),xi=xi.copy(),weights=w.copy());totals=np.zeros((2,10,10));envelopes=np.zeros_like(totals);modal=np.zeros((2,10,32,5));constraint=[];chainA=[];chainB=[];chainE=[]
 AR.update(metric_signed_components=totals,metric_uncancelled_envelopes=envelopes,per_mode_metric_components=modal)
 for iq,(rr,vol,shapes) in enumerate(shape_quadrature(r,z)):
  rr=np.broadcast_to(rr,vol.shape);zz=np.broadcast_to(sum(n*z[j:len(z)-1+j][None,:] for n,nr,nz,i,j in shapes),vol.shape);sel=(rr>2)&(rr<48)&(zz<16);R=rr[sel];Z=zz[sel];dv=vol[sel]
  s=trial_point(r,z,x,odd,xi,w,om,shapes,R,Z,sel);ratio=np.exp(-2*s['Phi']);AR[f'q{iq}_reference_volume']=dv.copy();AR[f'q{iq}_measure_ratio']=ratio.copy()
  for k in ('R','Z','Phi','gr','n','rho','g','hi','Ga','U','du','z','dz','phi','V','D','a','r','f','Pi','mu','PiU','A'):AR[f'q{iq}_{k}']=s[k].copy()
  for ib,box in enumerate(BOXES):
   for ik,(a,b) in enumerate(DYADS):
    CONTEXT.update(stage='full_metric_probe',sigma=sigma,quadrature=iq,rectangle=ib,dyad=[a,b]);q,dq,bump=tetrad_direction(s,box,a,b);eta,de,c=normalized_lift(s,q,dq);constraint.append(c)
    label=f'b{ib}_d{ik}_q{iq}_';AR.update({label+k:v.copy() for k,v in dict(metric_test=q,metric_test_partial=dq,delta_U=eta,delta_U_partial=de).items()})
    direct,env,raw=metric_native(s,q,dq,eta,de)
    AR.update({label+k:v.copy() for k,v in dict(delta_connection=raw['delta_connection'],direct_native=direct,native_envelope=env,per_mode_terms=raw['per_mode_metric_terms'],per_mode_envelope=raw['per_mode_metric_envelope']).items()})
    bare,be,braw=metric_native(s,q,dq,np.zeros_like(eta),np.zeros_like(de));AR[label+'bare_native']=bare.copy()
    u_chain,fe,_,_,_,*_=variation(s,eta,de,np.zeros_like(s['z']),np.zeros_like(s['dz']))
    AR[label+'longitudinal_U_chain']=u_chain.copy()
    chain_scale=max(1e-30,float(np.max(env+be+fe,initial=0)));AR[label+'native_chain_control_scale']=np.array(chain_scale)
    chainA.append((direct/chain_scale).ravel());chainB.append(((bare+u_chain)/chain_scale).ravel());chainE.append(((env+be+fe)/chain_scale).ravel())
    ph,pe,pr=pressure(s,q,fixed);AR[label+'phase']=ph.copy();AR[label+'phase_envelope']=pe.copy()
    for k,v in pr.items():AR[label+k]=v.copy()
    AR[label+'phase_u_chart']=RAW['current_phase_q2_minus1'].copy();AR[label+'phase_u_float']=pr['X2']/(100*fixed['Hunit']/LIGHT)**2-1
    AR[label+'phase_u_cancellation_difference']=AR[label+'phase_u_float']-AR[label+'phase_u_chart']
    eh,ee,er=einstein(s,q,dq);AR.update({label+k:v.copy() for k,v in dict(gravity=eh,gravity_envelope=ee,EH_terms=er['EH_terms'],EH_component_envelopes=er['EH_component_envelopes'],EH_delta_V=er['EH_delta_V'],EH_delta_DV=er['EH_delta_DV']).items()})
    phase_identity=(-covdot(s['hi'],s['phi'],s['phi'])/(100*fixed['Hunit']/LIGHT)**2-(1+RAW['current_phase_q2_minus1']));constraint.append(phase_identity.ravel())
    constraint.append((np.sqrt(-np.linalg.det(s['g']))/R-ratio).ravel())
    expected_trace=bump*((-1 if a==0 else 1) if a==b else 0)
    constraint.append((np.einsum('pab,pba->p',s['hi'],q)-expected_trace).ravel())
    density=np.column_stack((eh,ratio[:,None]*direct,ratio*ph));denv=np.column_stack((ee,ratio[:,None]*env,ratio*pe))
    totals[ib,ik,:9]+=np.sum(dv[:,None]*density,axis=0);envelopes[ib,ik,:9]+=np.sum(dv[:,None]*denv,axis=0);modal[ib,ik]+=np.sum((dv*ratio)[None,:,None]*raw['per_mode_metric_terms'],axis=1)
    AR[label+'density_terms']=density.copy();AR[label+'density_envelopes']=denv.copy()
  # Shared EH coefficients suffice to audit all derivatives; derived mode δjets are not duplicated.
  for k in ('reference_connection','connection_difference','reference_V','reference_DV','EH_primal_terms'):AR[f'q{iq}_{k}']=er[k].copy()
 check(f's{sigma}_full_metric_constraint_and_clock_identity',np.concatenate(constraint),np.zeros(sum(v.size for v in constraint)),np.ones(sum(v.size for v in constraint)))
 ss=sheet_point(even,odd,source);AR.update({'source_'+k:v.copy() for k,v in ss.items()});ma=[];mb=[];me=[]
 for ib,box in enumerate(BOXES):
  for ik,(a,b) in enumerate(DYADS):
   q,dq,bump=tetrad_direction(ss,box,a,b);k=ss['k'];D=ss['D'];weight=B*source[:,7]
   value=weight*np.einsum('pa,pab,pb->p',k,q,k)/(2*np.sqrt(D));env=abs(weight)*np.einsum('pa,pab,pb->p',abs(k),abs(q),abs(k))/(2*np.sqrt(D))
   vv=ss['speed'];S00=1. if a==b==0 else 0.;S0p=1. if (a,b)==(0,3) else 0.;Spp=1. if a==b==3 else 0.
   expected=weight*ss['n']*ss['Gamma']*bump*(S00+2*S0p*vv+Spp*vv*vv)/2
   scale=max(1e-30,float(np.max(env,initial=0)));ma.append(value/scale);mb.append(expected/scale);me.append(env/scale);totals[ib,ik,9]=value.sum();envelopes[ib,ik,9]=env.sum()
   AR.update({f'b{ib}_d{ik}_source_'+k:v.copy() for k,v in dict(metric_test=q,metric_test_partial=dq,worldline_derivative=value,independent_ADM_derivative=expected,envelope=env).items()})
   AR[f'b{ib}_d{ik}_source_control_scale']=np.array(scale)
 scale=max(1e-30,float(np.max(abs(source[:,1]),initial=0)));ma.append(ss['rest_mass_annulus_identity']/scale);mb.append(source[:,1]/scale);me.append(np.maximum(abs(source[:,1]),1e-30)/scale)
 check(f's{sigma}_fixed_worldline_metric_and_annulus',np.concatenate(ma),np.concatenate(mb),np.concatenate(me))
 # Independently contract the saved per-direction densities and sheet derivatives.
 again=np.zeros_like(totals)
 for ib in range(2):
  for ik in range(10):
   for iq in range(4):again[ib,ik,:9]+=np.einsum('p,pk->k',AR[f'q{iq}_reference_volume'],AR[f'b{ib}_d{ik}_q{iq}_density_terms'])
   again[ib,ik,9]=np.sum(AR[f'b{ib}_d{ik}_source_worldline_derivative'])
 scale=np.maximum(envelopes,1e-30);AR['independent_saved_density_contraction']=again.copy();AR['integral_control_scale']=scale.copy()
 chainA.append((totals/scale).ravel());chainB.append((again/scale).ravel());chainE.append(np.ones(totals.size))
 check(f's{sigma}_normalized_metric_native_chain_and_integral',np.concatenate(chainA),np.concatenate(chainB),np.concatenate(chainE))
 AR.update(metric_signed_components=totals,metric_uncancelled_envelopes=envelopes,per_mode_metric_components=modal);AR.update({k:v.copy() for k,v in RAW.items() if k.startswith('control_')})
 rec=checkpoint('ARM',AR,dict(kind='full_untruncated_constrained_metric_weak_measures',sigma=sigma,controls=CHECKS[begin:],parent_final_file=case['final_checkpoint']['file'],metric_dyads=DYADS,component_order=['EH','Maxwell','relative_phase','mode_inertia','mode_mass','mode_quartic','mode_gradient','mode_acceleration','absolute_P','ordinary_sheet'],ordinary_Euler='radial heldOmega residual; vertical reflected mean with both one-sided traction contacts retained',unknowns=dict(physical_background_subtraction=None,physical_exterior=None,finite_height_ordinary_distribution=None,activity_outside_support=None,full_junction=None)))
 ARM_AVAILABLE={};return dict(sigma=sigma,status='CONDITIONAL_FULL_METRIC_WEAK_MEASURES',checkpoint=rec,metric_signed_components=totals.tolist(),metric_envelopes=envelopes.tolist(),qualification=FLAGS)

def main():
 global np,INPUTS,OWNER,RAW,QBAR
 ap=argparse.ArgumentParser();ap.add_argument('--root-run',action='store_true');args=ap.parse_args()
 if AUTHOR_DRAFT or AUTHORING_IN_PROGRESS or not args.root_run:raise SystemExit('Guarded draft; reviewed root-only execution required.')
 assert not list(BASE.glob(STEM+'_*')), 'Own runtime namespace occupied.'
 INPUTS,binding,fixed,cp,source_record=admission()
 OWNER=dict(owner='root',pid=os.getpid(),started=now(),source_file=Path(__file__).name,source_sha256=sha(__file__),scope='full metric/source weak measures of the unchanged conditional trial; no solver or history')
 cases=[]
 try:
  json_file(STEM+'_OWNER_START.json',OWNER)
  json_file(STEM+'_MANIFEST.json',dict(owner=OWNER,input_sha256=INPUTS,parent_receipts=[BAND+'_RECEIPT.json',ODD+'_RECEIPT.json',COMPACT+'_RECEIPT.json'],parent_result=BAND+'_RESULT.json',parent_result_sha256=sha(path(BAND+'_RESULT.json')),source_pair=source_record['file'],source_pair_sha256=source_record['sha256'],configuration=dict(sigma=SIGMAS,rectangles=BOXES,metric_dyads=DYADS,controls=CONTROL_COUNT,pairs=PAIR_COUNT,tolerance=TOL),qualification=FLAGS))
  import numpy as _np
  np=_np
  even=selected_arrays(ODD+'_00000_INPUT.npz',('r_kpc','z_kpc','final_state','xi','weights'))
  loaded=selected_arrays(source_record['file'],tuple(source_record['metadata']['schema']))
  with np.load(path(source_record['file']),allow_pickle=False) as f:
   assert set(f.files)==set(source_record['metadata']['schema'])|{'metadata'}
   assert json.loads(str(f['metadata']))==source_record['metadata']
  for k,v in even.items():assert loaded[k].dtype==v.dtype and np.array_equal(loaded[k],v),('Changed closed even input',k)
  source={k:loaded[k] for k in ('source_samples16','source_samples32')}
  r,z,x,xi,w=(even[n] for n in ('r_kpc','z_kpc','final_state','xi','weights'))
  assert r.shape==(87,) and z.shape==(45,) and x.shape==(65,87,45) and xi.shape==w.shape==(32,)
  assert np.all(np.diff(r)>0) and np.all(np.diff(z)>0) and np.all((xi>0)&(xi<1)) and np.all(w>0)
  assert np.all(x[:,-1]==0) and np.all(x[:,:,-1]==0) and np.all(x[1::2,0]==0) and np.all(x[2::2,:,0]==0)
  for k,v in source.items():
   assert v.shape==((2416,9) if k.endswith('16') else (4832,9)) and np.all(v[:,0]>0) and np.all(v[:,1]>=0) and np.all(v[:,7]>=0)
   assert np.all((v[:,3]>=0)&(v[:,3]<.5)) and np.all((v[:,4]>=0)&(v[:,4]<1))
  eta=fixed['Hunit']/LIGHT;ep=1e-5;norm=1/ep-math.log1p(1/ep);target=.5*ep*norm*fixed['d0'];ss=target
  for _ in range(12):
   qq=math.sqrt(1+ep*ss/(1+ss));dqq=ep/(2*qq*(1+ss)**2);ss-=(ss*qq-target)/(qq+ss*dqq)
  qbar=math.sqrt(1+ep*ss/(1+ss));QBAR=fixed['Q0_over_Hstar']*eta*qbar
  RAW.update(even,**source,eta=np.array(eta),qbar=np.array(qbar),Qbar_star=np.array(QBAR))
  check('proper_eta_units',np.array(eta),np.array((fixed['Hunit']*1000/(1000*KPC))*KPC/LIGHT))
  check('owned_macro_Qbar',np.array(qbar),np.array(cp['background']['q']))
  check('actual_weight_sum',np.array(w.sum()),np.array(1.))
  fac=2*eta**2/C;Abar=1.5*fixed['OA']/fixed['rG'];pe=(math.log1p(ss)-ss/(1+ss))/norm;dp=2*qbar*ss/(ep*norm)
  actual=np.array([fac*Abar*(pe-1),fac*Abar*qbar*dp,Abar]);expected=np.array([fac*(cp['background']['w']-cp['background']['rho']),fac*cp['background']['w'],cp['background']['A']])
  RAW.update(pressure_reference_s=np.array(ss),pressure_reference_p_eps=np.array(pe),pressure_reference_dp_eps=np.array(dp),pressure_reference_raw_actual=actual,pressure_reference_raw_expected=expected)
  scales=np.maximum(np.maximum(abs(actual),abs(expected)),1e-30);RAW['pressure_reference_control_scale']=scales
  check('owned_absolute_pressure_and_enthalpy',actual/scales,expected/scales,np.ones(3))
  factor=2*math.pi*1e6*G_KPC_KMS2_MSUN/A0_V;unit=np.array([B*factor,C/(2*(1-KB/2))]);unit_expected=np.array([2*math.pi*1e6*G_KPC_KMS2_MSUN/(LIGHT/1000)**2,1.])
  RAW.update(source_unit_raw_actual=unit,source_unit_raw_expected=unit_expected,source_unit_factor=np.array(factor),source_G_KPC_KMS2_MSUN=np.array(G_KPC_KMS2_MSUN),source_B0=np.array(B))
  scale=np.maximum(np.maximum(abs(unit),abs(unit_expected)),1e-30);RAW['source_unit_control_scale']=scale
  check('once_only_reflected_sheet_and_Gbare_units',unit/scale,unit_expected/scale,np.ones(2))
  source_registration_controls(even,source['source_samples32'])
  checkpoint('INPUT',dict(even,**source),dict(kind='exact_closed_even_fields_and_fixed_rest_mass_annuli',parent_even_file=ODD+'_00000_INPUT.npz',parent_even_sha256=PINS[ODD+'_00000_INPUT.npz'],source_file=source_record['file'],source_sha256=source_record['sha256'],source_commit_sha256=PINS[source_record['file']+'.COMMIT.json'],owned_fixed=fixed,inherited_compact_fixed=source_record['metadata']['fixed'],phase_Qbar_star=QBAR,copied_band_controls=binding['controls'],copied_original_controls=binding['copied_parent_controls'],copied_original_failures=source_record['metadata']['copied_original_failures'],parent_band_finals=[c['final_checkpoint']['file'] for c in binding['cases']],physical_changes=[]))
  independent_gravity_fixtures();independent_relative_fixture(xi,w)
  assert len(CHECKS)==12
  available=dict(ARM_AVAILABLE);available.update(RAW)
  checkpoint('ARITHMETIC_FIXTURES',available,dict(kind='twelve_global_registration_and_independent_metric_controls',controls=list(CHECKS)))
  for c in binding['cases']:
   with np.errstate(over='raise',invalid='raise',divide='raise'):cases.append(arm(c,even,source['source_samples32'],xi,w,fixed))
  assert len(CHECKS)==CONTROL_COUNT and len(RECORDS)==PAIR_COUNT and all(c['passed'] for c in CHECKS)
  result=dict(owner=OWNER,status='CONDITIONAL_FULL_METRIC_WEAK_MEASURES_ARITHMETIC_PASS',cases=cases,controls=CHECKS,checkpoints=RECORDS,parent_file=BAND+'_RESULT.json',parent_sha256=sha(path(BAND+'_RESULT.json')),old_failed_evidence='unchanged original parent references and copied INPUT controls',qualification=FLAGS,unknowns=dict(full_metric_solution=None,physical_junction=None,physical_Cauchy_history=None,physical_constitutive_dictionary=None,ordinary_source_feedback=None,finite_height_ordinary_distribution=None,activity_outside_support=None))
  recheck();rh=json_file(STEM+'_RESULT.json',result)
  publish(STEM+'_REPORT.md',(f'# {STEM}\n\n{CONTROL_COUNT} implementation checks; four unchanged conditional full-metric trials, ten independent dyads and two compact rectangles.\n\nFull EH/native/phase/ordinary signed pieces, longitudinal unit reactions and held-worldline conservation rows are retained. No inverse, residual-smallness, full Galerkin, physical Einstein/junction or observational gate.\n').encode())
  recheck();receipt=dict(owner=OWNER,status='CLOSED',closed=now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,qualification=FLAGS)
  json_file(STEM+'_RECEIPT.json',receipt);assert json.loads(path(STEM+'_RECEIPT.json').read_text())==canonical(receipt);recheck()
  print('CONDITIONAL_FULL_METRIC_WEAK_MEASURES_ARITHMETIC_PASS',CONTROL_COUNT,len(RECORDS))
 except BaseException:
  failure_traceback=traceback.format_exc();raw_failure=None;closing_failure=None
  available=dict(ARM_AVAILABLE);available.update(RAW)
  if np is not None and available:
   try:checkpoint('ERROR_RAW',available,dict(kind='unaccepted_current_and_completed_operands',context=CONTEXT))
   except BaseException:raw_failure=traceback.format_exc()
  try:seal_created();recheck(False)
  except BaseException:closing_failure=traceback.format_exc()
  existing=STEM+'_RECEIPT.json';prior=sha(path(existing)) if path(existing).exists() else None
  if prior:OUTPUTS[existing]=prior
  unknown_npz=[p.name for p in BASE.glob(STEM+'_*.npz') if p.name not in {r['file'] for r in RECORDS}]
  unknown_commit=[p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json') if p.name not in {r['commit_file'] for r in RECORDS}]
  error=dict(owner=OWNER,status='FAILED',traceback=failure_traceback,raw_preservation_traceback=raw_failure,closing_traceback=closing_failure,context=CONTEXT,checkpoints=RECORDS,controls=CHECKS,completed_cases=cases,unqualified_npz=unknown_npz,unqualified_commits=unknown_commit,input_sha256=INPUTS,preserved_outputs=dict(OUTPUTS),prior_receipt_sha256=prior,qualification=FLAGS)
  if not path(STEM+'_ERROR.json').exists():eh=json_file(STEM+'_ERROR.json',error)
  else:eh=sha(path(STEM+'_ERROR.json'))
  if prior is None:
   receipt=dict(owner=OWNER,status='CLOSED_ERROR',closed=now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),error_sha256=eh,qualification=FLAGS)
   json_file(STEM+'_RECEIPT.json',receipt);assert json.loads(path(STEM+'_RECEIPT.json').read_text())==canonical(receipt)
  recheck(False);raise

if __name__=='__main__':main()

"""AUTHORING DRAFT: full fixed-metric native first-jet weak measures; root only."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,ast,hashlib,json,math,os,traceback
AUTHOR_DRAFT=True
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_SAVED_UNTRUNCATED_NATIVE_FLOW_RESIDUAL_V001'
ODD='CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001'
BAND='CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001'
PROTOCOL_SHA='23fa963473f5c383176c60ae8ab4a7953142883bb8e14e8b2b9ca1f287f62b96'
PINS={'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_EPS_1em05_CP.json': '3f4cbdf1c8255ae06668dc63fa6cdfc7ca4c5b70c78a2b5cbe64a303fb17973c', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RECEIPT.json': 'df514792bf703b6ce6b9e4c2a64e2ac19c407dffa0f14acf9bb9f75b6acc64e6', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RESULT.json': 'e9f7b2070e762920cb3548ccbe11c5f46efd1a262065ba594afaca6635acc35f', 'CROSS_U_EPS5_MACRO_BACKGROUND_CALLER_REGISTRATION_V001.md': '087b59df9fd2ef89b3f471fa5fc8a6b0e5a1102b8c37f6d2d6e377f8130e2523', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001.md': '030a618dc6ac06f9faa6748e3559afe074e17be4ad6feba94ae7348a935a9f2e', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_00000_INPUT.npz': 'f6d8c876eca1db21e613fda745a3c239f682789e98db581f56436804e2fe7b02', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_00000_INPUT.npz.COMMIT.json': '49e79e3a41cf1fb3466a2d79634aabf12b368e895b2594f91db09bc148bc31b6', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_00003_COEFFICIENTS.npz': '9b016352c4aa8fdd1dc9bf76bdbc20bfe3ef48c6287c41f2ffab929da37d5ea1', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_00003_COEFFICIENTS.npz.COMMIT.json': 'bc9320157d55270b5a50c7a9e87122b836cd0974dea4e3fd53ee62d582d5866a', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_00005_COEFFICIENTS.npz': 'eceb3c5dcbfe38578a6b04a9e3ef64f7a27ed06ba8df40c170ead7dc1a28781e', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_00005_COEFFICIENTS.npz.COMMIT.json': 'd07ce6a875f4204ef4b8dcebba5cdc23ab77144a17466c1e8a9d77dcbf232924', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_00007_COEFFICIENTS.npz': 'bb3f8f8640bfda483bf3cfc8d81c281a7184323252fead9dd7418608a738427d', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_00007_COEFFICIENTS.npz.COMMIT.json': 'a258e0960f18f611c3bdb0128101ca6f625cdea56be5597215b04b4e69137b4e', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_00009_COEFFICIENTS.npz': 'e5f337c07424d4b1332eb820bdc6bcbb780b01f43d89969f44bdd9f5e33a25f5', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_00009_COEFFICIENTS.npz.COMMIT.json': '3d6a51a9ede774eaec6eff223605844f63cc48cde2ce1639a3f2049608bf6f24', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_RECEIPT.json': 'afd64b4dff5f9f4151494749d3d3d54b91dc031e82a394994c6c17e8e24ebe04', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001.md': '0f7b501037a0f0e65359435825b9d48f49d1249efc6c39a4549e285bdf88423b', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_00003_ASSEMBLY.npz': '75887254f27f8352053afe167b5f9bddd0878e9d1a71f2dd5c85ca490592f32f', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_00003_ASSEMBLY.npz.COMMIT.json': 'f8d7d621c5a2e2ea3faae41660cade972c4efd0bb39d4bbc629d6fe2e77ebbfc', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_00004_FINAL.npz': 'edc24ede7539c954eff7b672e57100b80d698e5bf2b0d7f6098e695b26fe0322', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_00004_FINAL.npz.COMMIT.json': '892f1f28e508bd63c971e80448e3dbd5fb0f89d03395d14dde919319e3760b7b', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_00005_ASSEMBLY.npz': '987d28e2a6e029358083887b9ad00baebe1ec0b3db41f7f7d4577c3aca8e42b5', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_00005_ASSEMBLY.npz.COMMIT.json': 'f4a36c2c27eb24861eb9fef549691e3545df710a151038333873f3092992e213', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_00006_FINAL.npz': '0fd15943c18f728830a657fa24d60da9e09dd6877e4f0506080ff6bb52e71c2b', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_00006_FINAL.npz.COMMIT.json': 'f6c5580e0d7c1c54872e6dd5a7233e1ef2de1a21480012b7626635bd37d4c907', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_00007_ASSEMBLY.npz': 'e278b910fc7610857925fd43909eeb0b1eb0c0726adad87a5d16de7f8bfadcac', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_00007_ASSEMBLY.npz.COMMIT.json': '38898898221e62e5e65615dbef695dc10c143422dd26a17451009ecf12565324', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_00008_FINAL.npz': '03f795d1e8abc64a971861f763301d1e95be5d6e05f917c5bab9da6ea22f5a92', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_00008_FINAL.npz.COMMIT.json': '34adc747416f6b1a7da6fe1d3fbd767648df112d324867d3cad1b24718bf489f', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_00009_ASSEMBLY.npz': 'bafae248fbb0c3289fd2e9cfcb6d4650d15955fe1c16b298a774fb744d0bcc7a', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_00009_ASSEMBLY.npz.COMMIT.json': '4fd00973e05df5445b7be830b18ef28fda611d2fb8851d059b71b50fc1c725f7', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_00010_FINAL.npz': '53a28d073995fc4dbc2acc7acb9dc6e95745ca2f9f6c64a7bf5db67e8cee324a', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_00010_FINAL.npz.COMMIT.json': '6d88233b8787ea606c2a5ee1f80f277b29c50944250abbec4b6bb220cc7010cf', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_RECEIPT.json': '41a22374c9747d5b64bf4894290433af8a2cdb92f345f64f6de89f8cc175ea0f', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_RESULT.json': 'fc54d032172c901d288d7f845c077b7f4114199183190e3c0b7eb2c8a1420e85', 'CROSS_U_NONLINEAR_NATIVE_FLOW_AND_CIRCULAR_ACCELERATION_CLOSURE_V001.md': 'f7fc8138a9683a677851bdf9241c82ca942d4153db1254f513e28eca9f912a21', 'CROSS_U_STATIONARY_AZIMUTHAL_SHIFT_AND_NATIVE_RESPONSE_V001.md': '048b224899adf28c6924fa02c06a2e2d42fced7f086a139ed8a6981e0dc20fe2', 'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md': 'e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0', 'cross_u_axial_flrw_state_and_moving_port_v001.py': '96e7004d7abf2efedcff74eb2f36fb5a5a19a77ac181b58a652c5b8974c3f759', 'cross_u_ngc3198_conditional_odd_sector_v001.py': '508c379f4bd287435b406567f772fb14efdb7142ca17b18ef0d3e4e74736b394', 'cross_u_ngc3198_odd_banded_correction_v001.py': 'a22931b8f9b8a0a1cca663a459892c634b0f484791a61495567bff33f14bc913'}
COEFFICIENT_FILES=['CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_00003_COEFFICIENTS.npz', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_00005_COEFFICIENTS.npz', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_00007_COEFFICIENTS.npz', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_00009_COEFFICIENTS.npz']
LIGHT=299792458.;KPC=3.085677581491367e19;A0=1.0059833281731022e-10;B=A0*KPC/LIGHT**2
KB=.02;C=1.98;ALPHA=KB/C;ELL=.1;GC=3*math.pi/8
SIGMAS=(.1,1.,10.,100.);BOXES=((2.,16.),(16.,48.));TOL=2e-11;CONTROL_COUNT=72;PAIR_COUNT=6
np=None;OWNER=None;INPUTS={};OUTPUTS={};RECORDS=[];RAW={};ARM_AVAILABLE={};CONTEXT={};CHECKS=[];QBAR=None
FLAGS={k:False for k in ('full_native_Galerkin_qualified','full_Einstein_solution_qualified','full_phase_solution_qualified','full_ordinary_feedback_qualified','physical_junction_qualified','physical_temporal_spectrum_qualified','physical_Cauchy_preparation_qualified','active_source_mapping_qualified','orbital_force_qualified','observational_qualified','joint_model_adopted')}

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

def lower(g,v):return np.einsum('pab,...pb->...pa',g,v)
def lower_last(g,v):return np.einsum('pab,pcb->pca',g,v)
def raise_cov(hi,v):return np.einsum('pab,...pb->...pa',hi,v)
def covdot(hi,a,b):return np.einsum('...pa,...pa->...p',raise_cov(hi,a),b)
def compact(R,Z,box):
 l,h=box;m=(l+h)/2;d=(h-l)/2;x=(R-m)/d;y=Z/16
 ok=(abs(x)<1)&(y<1)&(y>=0);f=(1-x*x)**3*(1-y*y)**3
 fr=-6*x/d*(1-x*x)**2*(1-y*y)**3;fz=-6*y/16*(1-y*y)**2*(1-x*x)**3
 return np.where(ok,f,0),np.where(ok,fr,0),np.where(ok,fz,0)
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
 constraint=np.stack((2*np.einsum('pa,pa->p',s['uc'],eta),np.einsum('pa,pa->p',s['uc'],eta)),axis=-1)
 dc=np.einsum('pa,jpa->jp',eta,z)+np.einsum('pa,jpa->jp',U,zeta)
 ddc=np.einsum('pab,jpb->jpa',ne,z)+np.einsum('pb,jpab->jpa',eta,s['nz'])+np.einsum('pab,jpb->jpa',s['nu'],zeta)+np.einsum('pb,jpab->jpa',U,nzeta)
 RAW.update(current_eta=eta,current_eta_partial=deta,current_zeta=zeta,current_zeta_partial=dzeta,current_direct_terms=terms,current_envelope=env,current_weakU=weakU,current_weakmode=weakmode,current_mode_envelope=me,current_constraint=constraint,current_delta_transverse=dc,current_delta_transverse_jet=ddc)
 return terms,env,md,weakU,weakmode,constraint,dc,ddc

def compensation(s,eta,deta):
 q=np.einsum('pa,jpa->jp',eta,s['z'])
 dq=np.einsum('pab,jpb->jpa',deta,s['z'])+np.einsum('pb,jpab->jpa',eta,s['dz'])
 z=s['uc'][None,:,:]*q[:,:,None]
 # Partial of lowered U equals metric compatibility expression.
 duc=lower_last(s['g'],s['nu'])+np.einsum('plab,pl->pab',s['Ga'],s['uc'])
 dz=duc[None,:,:,:]*q[:,:,None,None]+s['uc'][None,:,None,:]*dq[:,:,:,None]
 return z,dz

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

def directions(s,box,kind):
 f,fr,fz=compact(s['R'],s['Z'],box);df=np.zeros((len(f),4));df[:,1]=fr;df[:,2]=fz
 if kind==1:
  df[:,2]=f/16+s['Z']/16*fz;df[:,1]=s['Z']/16*fr;f=s['Z']/16*f
 eta=np.zeros_like(s['U']);de=np.zeros_like(s['du'])
 if kind in (0,1):
  a=kind+1;eta[:,a]=s['n']*f;de[:,:,a]=s['n'][:,None]*(df+s['gr']*f[:,None])
 else:
  eta=s['E']*f[:,None];de=s['de']*f[:,None,None]+s['E'][:,None,:]*df[:,:,None]
 # Same boosted spatial vector determines the pure covector mode direction.
 cov=lower(s['g'],eta)
 # Use the actual metric jet from compatibility: d(g eta)=g nabla eta+Gamma*eta_flat.
 ne=de+np.einsum('pbal,pl->pab',s['Ga'],eta)
 dcov=lower_last(s['g'],ne)+np.einsum('plab,pl->pab',s['Ga'],cov)
 amplitude=B*s['xi'][:,None]**2
 zeta=amplitude[:,:,None]*cov[None,:,:];dzeta=amplitude[:,:,None,None]*dcov[None,:,:,:]
 return eta,de,zeta,dzeta

def selected_arrays(file,names):
 out={}
 with np.load(path(file),allow_pickle=False) as f:
  for k in names:
   a=f[k].copy();RAW['loaded_'+k]=a
   assert a.dtype==np.dtype('float64') and np.all(np.isfinite(a));out[k]=a
 return out

def fixture_state(xi,w,omega,noncircle=False):
 p=1;g=np.diag([-1.,1.,1.,1.])[None,:,:];hi=g.copy();Ga=np.zeros((1,4,4,4))
 U=np.array([[1.,0.,0.,0.]]);du=np.zeros((1,4,4));z=np.zeros((32,1,4));dz=np.zeros((32,1,4,4));phi=np.array([[3/20,0.,0.,0.]])
 z[:,:,1]=B*xi[:,None]**2/3;z[:,:,2]=B*xi[:,None]**2/7
 if noncircle:
  du[:,0,1]=1/5;dz[:,:,0,1]=B*xi[:,None]**2/7
  dz[:,:,:,0]=-np.einsum('pab,jpb->jpa',du,z)
 return features(g,hi,Ga,U,du,z,dz,phi,omega,xi,w)

def retain_fixture(label):
 ARM_AVAILABLE.update({label+'_'+k:v.copy() for k,v in RAW.items() if k.startswith('current_')})

def artificial_controls(xi,w,omega,sigma):
 s=fixture_state(xi,w,omega);zero=np.zeros_like(s['U']);d0=np.zeros_like(s['du']);zz=np.zeros_like(s['z']);dz=np.zeros_like(s['dz'])
 zz[:,:,1]=B*xi[:,None]**2/11
 t,e,md,wu,wm,*_=variation(s,zero,d0,zz,dz)
 expected=-w[:,None]*(B*xi[:,None]**2/3)*(B*xi[:,None]**2/11)*(1+(1/9+1/49)/GC**2)
 retain_fixture('fixture_flat_potential')
 check(f's{sigma}_flat_potential',w[:,None]*md.sum(axis=-1),expected,abs(expected))
 kin=s['dz'].copy();kin[:,:,0,1]=B*xi[:,None]**2/5;s=features(s['g'],s['hi'],s['Ga'],s['U'],s['du'],s['z'],kin,s['phi'],omega,xi,w)
 dz[:,:,0,1]=B*xi[:,None]**2/13;t,e,md,wu,wm,*_=variation(s,zero,d0,np.zeros_like(zz),dz)
 ex=w[:,None]*(B*xi[:,None]**2)**2/(65*omega[:,None]**2)
 retain_fixture('fixture_flat_kinetic')
 check(f's{sigma}_flat_kinetic',w[:,None]*md.sum(axis=-1),ex,abs(ex))
 s=fixture_state(xi,w,omega);d0[:,1,2]=1/3;d0[:,2,1]=-1/7
 s['du'][:,1,2]=1/5;s['du'][:,2,1]=-1/11;s=features(s['g'],s['hi'],s['Ga'],s['U'],s['du'],s['z'],s['dz'],s['phi'],omega,xi,w)
 t,e,*_=variation(s,zero,d0,np.zeros_like(zz),np.zeros_like(dz));ex=np.array([-ALPHA*(1/5+1/11)*(1/3+1/7)])
 retain_fixture('fixture_Maxwell')
 check(f's{sigma}_Maxwell_antisymmetry',t[:,0],ex,abs(ex))
 s=fixture_state(xi,w,omega);dt=np.zeros_like(s['du']);dt[:,0,1]=2/9
 t,e,*_=variation(s,zero,dt,np.zeros_like(zz),np.zeros_like(dz));ex=(2/9)*np.sum(w*B*xi**2/3)
 retain_fixture('fixture_acceleration')
 check(f's{sigma}_acceleration_contact',t[:,-1],np.array([ex]),np.array([abs(ex)]))
 s=fixture_state(xi,w,omega,True);eta=np.array([[0.,1/6,0.,0.]]);de=np.zeros_like(s['du']);de[:,0,0]=1/30
 comp,dc=compensation(s,eta,de);t,e,md,*_=variation(s,zero,np.zeros_like(de),comp,dc)
 exmu=w[:,None]*(B*xi[:,None]**2/35)/omega[:,None]**2
 assert np.all(exmu!=0),'Manufactured reaction must be nonzero.'
 excomp=exmu*(B*xi[:,None]**2/18)
 retain_fixture('fixture_mu_compensation')
 check(f's{sigma}_noncircular_mu_compensation',np.stack((s['mu'],w[:,None]*md.sum(axis=-1))),np.stack((exmu,excomp)),np.stack((abs(exmu),abs(excomp))))


def arm(case,even,xi,w,fixed,Qbar):
 global RAW,ARM_AVAILABLE,QBAR
 RAW={};ARM_AVAILABLE={};QBAR=Qbar;CONTEXT.update(stage='arm',sigma=case['sigma']);start=len(CHECKS)
 physical=selected_arrays(case['final_checkpoint']['file'],('physical_beta_chi',))['physical_beta_chi'];r=even['r_kpc'];z=even['z_kpc'];x=even['final_state'];sigma=case['sigma']
 assert physical.shape==(2,87,45) and np.all(physical[:,-1]==0) and np.all(physical[:,:,-1]==0)
 assert np.array_equal(physical[0,0],physical[0,1]) and np.all(physical[1,0]==0)
 om=sigma*xi*fixed['Hunit']/LIGHT
 oldomega=selected_arrays(COEFFICIENT_FILES[SIGMAS.index(sigma)],('omega_star',))['omega_star']
 check(f's{sigma}_inherited_frequency',om,oldomega)
 artificial_controls(xi,w,om,sigma)
 AR=ARM_AVAILABLE;AR.update(physical_beta_chi=physical.copy(),omega_star=om.copy(),xi=xi.copy(),weights=w.copy())
 signed=np.zeros((2,3,7));envelope=np.zeros_like(signed);mrows=np.zeros((2,3,32,5));menv=np.zeros_like(mrows);mureaction=np.zeros((2,3,32))
 zeros=[];normals=[];proj=[];pino=[];variation_constraints=[];us=[[] for _ in range(3)];ue=[[] for _ in range(3)];uw=[[] for _ in range(3)];ms=[[] for _ in range(3)];me=[[] for _ in range(3)];mw=[[] for _ in range(3)]
 for iq,(rr,vol,shapes) in enumerate(shape_quadrature(r,z)):
  rr=np.broadcast_to(rr,vol.shape)
  # Recover actual Z of this Q1 quadrature, not cell midpoint, from shape weights.
  zr=np.broadcast_to(sum(n*z[j:len(z)-1+j][None,:] for n,nr,nz,i,j in shapes),vol.shape)
  sel=(rr>2)&(rr<48)&(zr<16);R=rr[sel];Z=zr[sel];dv=vol[sel]
  s=trial_point(r,z,x,physical,xi,w,om,shapes,R,Z,sel);measure=dv*np.exp(-2*s['Phi']);AR[f'q{iq}_R']=R;AR[f'q{iq}_Z']=Z;AR[f'q{iq}_measure']=measure
  assert np.all((Qbar/(100*fixed['Hunit']/LIGHT)/s['n'])**2>1) and np.all((Qbar/(100*fixed['Hunit']/LIGHT)/s['n'])**2<1+1e-5)
  for k in ('g','hi','Ga','U','du','z','dz','phi','V','D','a','r','f','Pi','mu','PiU','A'):
   AR[f'q{iq}_{k}']=s[k].copy()
  zeros.append(np.einsum('pa,pa->p',s['uc'],s['U'])+1)
  normal=np.einsum('pa,jpa->jp',s['U'],s['z']);jet=np.einsum('pab,jpb->jpa',s['nu'],s['z'])+np.einsum('pb,jpab->jpa',s['U'],s['nz'])
  normals.append(np.concatenate((normal.ravel(),jet.ravel())))
  proj.append((np.einsum('pac,pcb->pab',s['P'],s['P'])-s['P']).ravel())
  pino.append(np.einsum('jpab,pb->jpa',s['Pi'],s['uc']).ravel())
  for ib,box in enumerate(BOXES):
   for kind in range(3):
    CONTEXT.update(stage='compact_probe',sigma=sigma,quadrature=iq,rectangle=ib,kind=kind)
    eta,de,pure,dpure=directions(s,box,kind);comp,dcomp=compensation(s,eta,de);zero=np.zeros_like(eta);d0=np.zeros_like(de);z0=np.zeros_like(pure);dz0=np.zeros_like(dpure)
    a,e,md,wu,wm,cv,ct,cjt=variation(s,eta,de,z0,dz0)
    b,be,bmd,bwu,bwm,*_=variation(s,zero,d0,comp,dcomp)
    combined=a+b;ce=e+be;reaction=s['mu']*np.einsum('pa,jpa->jp',eta,s['z']);weak=wu+reaction.sum(axis=0)
    us[kind].append(combined.sum(axis=1));ue[kind].append(ce.sum(axis=1));uw[kind].append(weak)
    signed[ib,kind]+=np.sum(measure[:,None]*combined,axis=0);envelope[ib,kind]+=np.sum(measure[:,None]*ce,axis=0);mureaction[ib,kind]+=np.sum(measure[None,:]*reaction,axis=1)
    AR.update({f'b{ib}_k{kind}_q{iq}_'+k:v.copy() for k,v in dict(eta=eta,eta_partial=de,compensation=comp,compensation_partial=dcomp,pure_mode=pure,pure_mode_partial=dpure,assembled_U=weak,assembled_rawU=wu,assembled_compensation=bwm).items()})
    AR[f'b{ib}_k{kind}_q{iq}_rawU_terms']=a;AR[f'b{ib}_k{kind}_q{iq}_compensation_terms']=b;AR[f'b{ib}_k{kind}_q{iq}_U_envelope']=ce;AR[f'b{ib}_k{kind}_q{iq}_mu_reaction']=reaction
    _,_,_,_,_,cc,tc,jc=variation(s,eta,de,comp,dcomp)
    variation_constraints.extend((cc.ravel(),tc.ravel(),jc.ravel()))
    a,e,md,wu,wm,cv,ct,cjt=variation(s,zero,d0,pure,dpure)
    actual=w[:,None]*md.sum(axis=-1);ms[kind].append(actual.ravel());mw[kind].append(wm.ravel())
    # Signed mode terms and envelope use their actual positive quadrature weights.
    # Recover per-mode absolute contractions from the direct formula saved in RAW.
    # Individual contraction envelope is supplied by variation(), not absolute sums of cancelled terms.
    men=w[:,None,None]*RAW['current_mode_envelope']
    me[kind].append(men.sum(axis=-1).ravel());mrows[ib,kind]+=np.sum(measure[None,:,None]*(w[:,None,None]*md),axis=1);menv[ib,kind]+=np.sum(measure[None,:,None]*men,axis=1)
    AR[f'b{ib}_k{kind}_q{iq}_assembled_mode']=wm;AR[f'b{ib}_k{kind}_q{iq}_mode_terms']=w[:,None,None]*md;AR[f'b{ib}_k{kind}_q{iq}_mode_envelope']=men
    variation_constraints.extend((cv.ravel(),ct.ravel(),cjt.ravel()))
 check(f's{sigma}_unit',np.concatenate(zeros),np.zeros(sum(len(v) for v in zeros)),np.ones(sum(len(v) for v in zeros)))
 for label,vectors in (('transverse_and_jet',normals),('projector',proj),('Pi_normal',pino)):
  a=np.concatenate(vectors);check(f's{sigma}_{label}',a,np.zeros_like(a),np.ones_like(a))
 for kind in range(3):
  check(f's{sigma}_U_direct_weak_{kind}',np.concatenate(us[kind]),np.concatenate(uw[kind]),np.concatenate(ue[kind]))
  check(f's{sigma}_mode_direct_weak_{kind}',np.concatenate(ms[kind]),np.concatenate(mw[kind]),np.concatenate(me[kind]))
 a=np.concatenate(variation_constraints);check(f's{sigma}_full_constraint_variation',a,np.zeros_like(a),np.ones_like(a))
 AR.update(U_signed_components=signed,U_uncancelled_envelopes=envelope,mode_signed_components=mrows,mode_uncancelled_envelopes=menv,integrated_mode_reaction=mureaction)
 AR.update({k:v for k,v in RAW.items() if k.startswith('control_')})
 record=checkpoint('ARM',AR,dict(kind='conditional_untruncated_native_U_weak_measures',sigma=sigma,controls=CHECKS[start:],full_constraint_reactions='mu=Pi:nablaU retained; lambda cancels on tangent directions',parent_final_file=case['final_checkpoint']['file'],unknowns=dict(strong_lambda=None,physical_boundary=None,full_metric_equations=None,full_ordinary_feedback=None,activity_outside_support=None)))
 rows=[dict(box=list(box),U_components=signed[i].tolist(),U_envelope=envelope[i].tolist(),mode_components=mrows[i].tolist(),mode_envelope=menv[i].tolist()) for i,box in enumerate(BOXES)]
 ARM_AVAILABLE={};return dict(sigma=sigma,status='CONDITIONAL_WEAK_MEASURES',checkpoint=record,rows=rows,qualification=FLAGS)

def merged_inputs():
 ins={}
 def add(n,h):
  n=str(path(n).resolve());assert n not in ins or ins[n]==h;ins[n]=h
 for n,h in PINS.items():add(n,h)
 add(STEM+'.md',PROTOCOL_SHA)
 for name in (BAND+'_RECEIPT.json',ODD+'_RECEIPT.json'):
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
 for c in b['cases']:
  assert c['status']=='LINEAR_PASS' and c['INFO']==0 and c['original_residual']<=1e-10
  rec=c['final_checkpoint'];assert r['output_sha256'][rec['file']]==rec['sha256'] and r['output_sha256'][rec['commit_file']]==rec['commit_sha256']
  assert json.loads(path(rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
 shared=json.loads(path('CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RESULT.json').read_text());fixed=dict(shared['manifest']['fixed_parent']);fixed['eps']=1e-5
 cp=json.loads(path('CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_EPS_1em05_CP.json').read_text());assert cp==next(v for v in shared['rows'] if v['eps']==1e-5)
 return ins,b,fixed,cp

def main():
 global np,INPUTS,OWNER,RAW,QBAR
 ap=argparse.ArgumentParser();ap.add_argument('--root-run',action='store_true');args=ap.parse_args()
 if AUTHOR_DRAFT or not args.root_run:raise SystemExit('Guarded draft; reviewed root-only execution required.')
 assert not list(BASE.glob(STEM+'_*')), 'Own runtime namespace occupied.'
 INPUTS,binding,fixed,cp=admission()
 OWNER=dict(pid=os.getpid(),started=now(),source_file=Path(__file__).name,source_sha256=sha(__file__),scope='held conditional trial; no solver or history')
 cases=[]
 try:
  json_file(STEM+'_OWNER_START.json',OWNER)
  json_file(STEM+'_MANIFEST.json',dict(owner=OWNER,input_sha256=INPUTS,parent_receipt=BAND+'_RECEIPT.json',parent_result=BAND+'_RESULT.json',parent_result_sha256=sha(path(BAND+'_RESULT.json')),configuration=dict(sigma=SIGMAS,rectangles=BOXES,controls=CONTROL_COUNT,pairs=PAIR_COUNT,tolerance=TOL),qualification=FLAGS))
  import numpy as _np
  np=_np
  even=selected_arrays(ODD+'_00000_INPUT.npz',('r_kpc','z_kpc','final_state','xi','weights'))
  r,z,x,xi,w=(even[n] for n in ('r_kpc','z_kpc','final_state','xi','weights'))
  assert r.shape==(87,) and z.shape==(45,) and x.shape==(65,87,45) and xi.shape==w.shape==(32,)
  assert np.all(np.diff(r)>0) and np.all(np.diff(z)>0) and np.all((xi>0)&(xi<1)) and np.all(w>0)
  assert np.all(x[:,-1]==0) and np.all(x[:,:,-1]==0) and np.all(x[1::2,0]==0) and np.all(x[2::2,:,0]==0)
  eta=fixed['Hunit']/LIGHT;ep=1e-5;norm=1/ep-math.log1p(1/ep);target=.5*ep*norm*fixed['d0'];s=target
  for _ in range(12):
   q=math.sqrt(1+ep*s/(1+s));dq=ep/(2*q*(1+s)**2);s-=(s*q-target)/(q+s*dq)
  qbar=math.sqrt(1+ep*s/(1+s));QBAR=fixed['Q0_over_Hstar']*eta*qbar
  RAW.update(even,eta=np.array(eta),qbar=np.array(qbar),Qbar_star=np.array(QBAR))
  check('proper_eta_units',np.array(eta),np.array((fixed['Hunit']*1000/(1000*KPC))*KPC/LIGHT))
  check('owned_macro_Qbar',np.array(qbar),np.array(cp['background']['q']))
  check('actual_weight_sum',np.array(w.sum()),np.array(1.))
  g=np.diag([-1.,1.,1.,1.])[None,:,:];U=np.array([[math.sqrt(17)/4,1/4,0.,0.]]);eta0=np.array([[1/12,math.sqrt(17)/12,0.,0.]])
  uc=lower(g,U);ec=lower(g,eta0);P=np.eye(4)[None,:,:]+np.einsum('pa,pb->pab',uc,U);dP=np.einsum('pa,pb->pab',ec,U)+np.einsum('pa,pb->pab',uc,eta0)
  actual=np.einsum('pac,pcb->pab',dP,P)+np.einsum('pac,pcb->pab',P,dP)-dP
  RAW.update(projector_fixture_metric=g,projector_fixture_U=U,projector_fixture_eta=eta0,projector_fixture_P=P,projector_fixture_deltaP=dP)
  check('independent_projector_jet',actual,np.zeros_like(actual),np.ones_like(actual))
  checkpoint('INPUT',even,dict(kind='unchanged_closed_even_fields',parent_input=ODD+'_00000_INPUT.npz',parent_band_finals=[c['final_checkpoint']['file'] for c in binding['cases']],owned_fixed=fixed,phase_Qbar_star=QBAR))
  checkpoint('ARITHMETIC_FIXTURES',dict(RAW),dict(kind='four_global_registration_controls',controls=list(CHECKS)))
  for c in binding['cases']:
   with np.errstate(over='raise',invalid='raise',divide='raise'):cases.append(arm(c,even,xi,w,fixed,QBAR))
  assert len(CHECKS)==CONTROL_COUNT and len(RECORDS)==PAIR_COUNT and all(c['passed'] for c in CHECKS)
  result=dict(owner=OWNER,status='CONDITIONAL_WEAK_MEASURES_ARITHMETIC_PASS',cases=cases,controls=CHECKS,checkpoints=RECORDS,parent_file=BAND+'_RESULT.json',parent_sha256=sha(path(BAND+'_RESULT.json')),old_failed_evidence='unchanged original parent references',qualification=FLAGS,unknowns=dict(full_metric_solution=None,physical_junction=None,physical_Cauchy_history=None,physical_constitutive_dictionary=None,ordinary_source_feedback=None,activity_outside_support=None))
  recheck();rh=json_file(STEM+'_RESULT.json',result)
  publish(STEM+'_REPORT.md',(f'# {STEM}\n\n{CONTROL_COUNT} implementation checks; four untruncated native weak measures on the unchanged conditional trial.\n\nNo residual-smallness, full Galerkin, metric solve, force or observational gate.\n').encode())
  recheck();receipt=dict(owner=OWNER,status='CLOSED',closed=now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,qualification=FLAGS)
  json_file(STEM+'_RECEIPT.json',receipt);assert json.loads(path(STEM+'_RECEIPT.json').read_text())==canonical(receipt);recheck()
  print('CONDITIONAL_WEAK_MEASURES_ARITHMETIC_PASS',CONTROL_COUNT,len(RECORDS))
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

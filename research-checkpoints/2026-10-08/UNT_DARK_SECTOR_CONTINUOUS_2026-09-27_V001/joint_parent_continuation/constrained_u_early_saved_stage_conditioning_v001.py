"""Bounded exact saved-stage numerical conditioning diagnostic; root alone executes.
No producer import, initial/trajectory replay, source modification or parent qualification.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import ast
import hashlib
import json
import math
import os
import time
for _thread_key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ.setdefault(_thread_key,'1')
import numpy as np

BASE=Path(__file__).resolve().parent
STEM='CONSTRAINED_U_EARLY_SAVED_STAGE_CONDITIONING_V001'
PARENT='CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V004'
PROTOCOL_SHA='7c8b8e46c0552785cb75dac5133c362c48e5a4f3a4ccb0a0f0f70f82e16d461e'
PINS={'constrained_u_clock_gradient_early_transfer_v004.py': 'a4e78b6467b0ba5884c8da2081ff580378b4afb839a90cec548fcf30a389fa07', 'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V004.md': '8d7f33f6b336488e92ed6b516dd196a66f7ee2929bda5a72e7a258fe34ac9cd5', 'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V004_RESULT.json': '2df066c32b5140d91e2194166940128e92611d7c1ab5d97ae8846fdc73e565c2', 'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V004_RECEIPT.json': 'b4959fb0e1c07179e34ab6a3de0e8075162f87624d7c9e2a8ecd83b16b1ab564', 'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V004_TIME_CP_000000.json': '3e7369f022aee6ade97ece62bf0cfc06fca2e5c5bb4169ee0c79ba90fdbde1fe', 'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V004_TIME_CP_000000_COMMIT.json': '477f236bb12e96660a386aaf101cbb7a3a70221ac2f2ea54c251e0c729831932', 'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V004_TIME_CP_000512.json': 'ec88831d8f3f9f9824285a6a6b390f9f26739606da95f2458c946a55b5c22229', 'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V004_TIME_CP_000512_COMMIT.json': '2c848911cba4598b7d8c95cab83177c5c42623426e1d7125fd3fdadacb87e541', 'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V004_TIME_CP_002048.json': '77d10c58804d926dbccc1e28becab5116bf1ccb5cdde85af32c775b49d440515', 'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V004_TIME_CP_002048_COMMIT.json': 'b71f9250d92185aee0a53563b3e7f7ee63f7739673f522de1a54e9b35b6483bb', 'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V004_TIME_CP_004096.json': 'b80c40c21a1b6f58b390f7974962dcf9d768f8853c5f7dbbd16bf5916b433cc7', 'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V004_TIME_CP_004096_COMMIT.json': 'd249c142d868935d4b71177fa282c3dfe190dce34ce38a6ae544557b4a1e10f0', 'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V004_TIME_CP_007680.json': '40bbbf54d5515c7220e99ef6b8d0c210616210f2636ec2a0ac20b8bc173aa616', 'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V004_TIME_CP_007680_COMMIT.json': '80612ceb6a5d68ff7aab5f828cbe18aa9c372b9476467dc3db40530218283e4c'}
HELPER_SHA={'background': 'eb224e42c6c567b0339b18cdf54a1d8c4f005810b6d6952fee9efee4983b7ec2', 'Thermal': '0d4c6a2726fd817d2cfb5ba8b90a6674a288bc0484c927da719ecdef72a7cd47', 'Layout': 'f199860c3687d2acc7817eda8a00133c1ef57abb2ffbf224ddc760a90e41d2a8', 'coefficients': 'b9e6a7edca9a67031670d32dba146c289347b9253f32bf16d0f3587597125637', 'rates': '2053ec557e765a899a9468fed8a48d701e010d2f76a0aa666ab209e8dc079354', 'stage_matrix': '0b02c3bb7a1c4d2d4a9ce6e5ddfe964965042d013ba916d50a4eeda63cb040fe', 'tridiagonal_blocks': 'aa7b86cf64ba2f4b4ccccebc676f120a57270ca5203b8ff4555c19743f2e378f', 'block_stage_solve': 'a44e8a47d27984773c73bc3c32f38e83444502417310d6e126d836daf0ae0a56'}
RADAU_SHA='78ec29a3205ec0d84d527fe7a9a6a8f7ca408ad984662fa3d7593865dced6568'
MPC=3.0856775814913673e22
CP=299792458.
KB,C,CBAR=.02,1.98,.99
K=.01
CURVATURE=1e-5
AI=1e-7
OMEGAS=(.1,1.,10.,100.)
SELECTED=(0,512,2048,4096,7680)
TIME_SPEC=['TIME',8192,32,96,128,AI,'HALF',1]
TOL=2e-11
BALANCE_PASSES=4
REFINEMENT_STEPS=3
SEALS={};CREATED={};RUN_SOURCE='';RUN_MANIFEST=''


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read(path):return json.loads(Path(path).read_text())
def now():return datetime.now(timezone.utc).isoformat()
def require(flag,name):
    if not flag:raise AssertionError(name)
def seal(path,digest):
    p=Path(path).resolve()
    allowed=p.is_relative_to(BASE.parent.parent.resolve()) or (str(p)=='/usr/bin/clang' and digest=='179301dcb41ea78accc3fa0048a7e6f6710d891945a751a34addd622020c1818')
    require(allowed and sha(p)==digest,'Input path/seal '+str(p))
    require(str(p) not in SEALS or SEALS[str(p)]==digest,'Conflicting seal')
    SEALS[str(p)]=digest

def recheck():
    for p,h in {**SEALS,**CREATED}.items():
        if sha(p)!=h:raise AssertionError('Changed sealed bytes '+p)
    require(sha(__file__)==RUN_SOURCE,'Diagnostic source unchanged')

def write(name,obj,raw=False):
    data=obj if raw else (json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
    p=BASE/name
    with p.open('xb') as f:f.write(data)
    p.chmod(0o444);CREATED[str(p.resolve())]=sha(p)
    return sha(p)

def journal(event,**data):
    line=json.dumps(dict(time=now(),event=event,owner='root',pid=os.getpid(),source_sha256=RUN_SOURCE,manifest_sha256=RUN_MANIFEST,**data),sort_keys=True,allow_nan=False)+'\n'
    with (BASE/(STEM+'_JOURNAL.jsonl')).open('a') as f:f.write(line)

def background(x, fixed):
    a = math.exp(x)
    eps, d0, OA, OB, OR, rG = (fixed[k] for k in ('eps', 'd0', 'OA', 'OB', 'OR', 'rG'))
    norm = 1/eps-math.log1p(1/eps)
    d = d0/a**3
    target = .5*eps*norm*d
    s = target
    for _ in range(5):
        qbar = math.sqrt(1+eps*s/(1+s))
        dq = eps/(2*qbar*(1+s)**2)
        s -= (s*qbar-target)/(qbar+s*dq)
    qbar = math.sqrt(1+eps*s/(1+s))
    dq = eps/(2*qbar*(1+s)**2)
    pex = (math.log1p(s)-s/(1+s))/norm
    cs = eps*s/(2+(4+3*eps)*s+2*(1+eps)*s*s)
    b, r = 1.5*OB/rG/a**3, 1.5*OR/rG/a**4
    w = 1.5*OA/rG*qbar*d
    rho = 1.5*OA/rG*(1+qbar*d-pex)
    h = math.sqrt((2/3)*(b+r+rho))
    den=2+(4+3*eps)*s+2*(1+eps)*s*s
    ds_dt=-3*h*s/(1+s*dq/qbar)
    cs_dt=eps*(2-2*(1+eps)*s*s)*ds_dt/(den*den)
    Q=fixed['Q0_over_Hstar']*qbar
    return dict(a=a, h=h, b=b, r=r, w=w, rho=rho, cs=cs, qbar=qbar,
                h_dt=-b-4*r/3-w, cs_dt=cs_dt, Q=Q,
                s=s, charge=d, charge_error=abs(2*qbar*s/(eps*norm)/d-1))

class Thermal:
    def __init__(self,arm,thin,fixed):
        name='CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V002_'+arm+'_OUTPUT.json'
        self.data=json.loads((BASE/name).read_text());self.rows=np.array([r[:3] for r in self.data['rows'][::thin]])
        if self.rows[0,0]!=0 or self.rows[-1,0]!=8000:raise AssertionError('Thermal table endpoints')
        self.nH=self.data['nH0_cm3']*1e6;self.fHe=self.data['fHe'];self.xfull=1+2*self.fHe
        self.hs=fixed['Hunit']*1000/MPC;self.T0=self.data['T0_K']
    def at(self,a):
        z=1/a-1
        if z>8000:xe,tm=self.xfull,self.T0/a
        elif z<0:raise ValueError('Thermal extrapolation below z0')
        else:xe,tm=(float(np.interp(z,self.rows[:,0],self.rows[:,i])) for i in (1,2))
        g=CP*6.6524587321e-29*self.nH*xe/a**3/self.hs
        cb2=5*1.380649e-23*tm*(1+self.fHe+xe)/(3*1.67262192369e-27*(1+4*self.fHe)*CP**2)
        return dict(g=g,xe=xe,Tm=tm,cold_pressure_diagnostic=cb2)

class Layout:
    def __init__(self,ns,lg,ln):
        self.ns,self.lg,self.ln=ns,lg,ln
        self.fg={l:9+l-2 for l in range(2,lg+1)};i=9+lg-1
        self.pol={l:i+l for l in range(lg+1)};i+=lg+1
        self.fn={l:i+l-2 for l in range(2,ln+1)};i+=ln-1
        self.z=np.arange(i,i+ns);self.zd=np.arange(i+ns,i+2*ns);self.n=i+2*ns
        self.core=list(range(9))+[self.fg[2],self.pol[0],self.pol[1],self.pol[2],self.fn[2],self.n,self.n+1]
        self.tails=[[self.fg[l] for l in range(3,lg+1)],
                    [self.pol[l] for l in range(3,lg+1)],
                    [self.fn[l] for l in range(3,ln+1)]]
    def names(self):
        names=['Psi','delta_b','Hstar_u_b','delta_gamma','Hstar_u_gamma',
               'delta_nu','Hstar_u_nu','delta_n_clock','Hstar_V_phi']
        names += ['F_gamma_'+str(l) for l in self.fg]+['G_gamma_'+str(l) for l in self.pol]+['F_nu_'+str(l) for l in self.fn]
        names += ['z_'+str(i) for i in range(self.ns)]+['zd_'+str(i) for i in range(self.ns)]
        return names

def coefficients(x,y,fixed,lay,therm,snodes,weights,omega,n_override=None):
    bg=background(x,fixed);h,b,r,w,c,Q=(bg[k] for k in ('h','b','r','w','cs','Q'))
    rg,rn=r*fixed['fgamma'],r*(1-fixed['fgamma']);q=K*CP/(1000*fixed['Hunit']*bg['a'])
    th=therm.at(bg['a']);g=th['g'];rb=3*b/(4*rg)
    psi,db,ub,dg,ug,dn,un,d,V=(y[i] for i in range(9))
    phi=psi-2*(rg*y[lay.fg[2]]+rn*y[lay.fn[2]])/q**2
    mom=b*ub+4*rg*ug/3+4*rn*un/3+w*V;psid=mom-h*phi
    Z=weights@y[lay.z];Zd=weights@y[lay.zd];R1=(weights*snodes**2)@y[lay.z]*omega**2
    alpha=omega**2*float(weights@snodes**2);L=Q*q;Ld=-h*(1+3*c)*L
    Ldd=(h*h*(1+3*c)**2-bg['h_dt']*(1+3*c)-3*h*bg['cs_dt'])*L
    v=Z/L;vd=(Zd-Ld*v)/L;Gamma=d+3*h*V;ncalc=vd-c*Gamma
    n=ncalc if n_override is None else n_override
    Vd=phi+c*Gamma;Bq=1+(fixed['ell_native']*q)**2;Delta=alpha+C*Q*Q/KB+CBAR*Q*Q*q*q*c/w
    Fv=(-h*n-C*(Zd+2*h*Z)/(KB*q)+bg['cs_dt']*Gamma
        +c*(3*psid-q*q*V+3*bg['h_dt']*V+3*h*Vd))
    sigma=(L*Fv+2*Ld*vd+Ldd*v+3*h*Zd+Bq*R1-alpha*q*n)/Delta
    return dict(bg=bg,h=h,b=b,rg=rg,rn=rn,w=w,c=c,Q=Q,q=q,thermal=th,g=g,rb=rb,
                phi=phi,psi=psi,psid=psid,mom=mom,Z=Z,Zd=Zd,L=L,Ld=Ld,Ldd=Ldd,
                v=v,vd=vd,Gamma=Gamma,n=n,ncalc=ncalc,Vd=Vd,Bq=Bq,Delta=Delta,sigma=sigma)

def rates(x,y,fixed,lay,therm,snodes,weights,omega,n_override=None,sigma_override=None):
    f=coefficients(x,y,fixed,lay,therm,snodes,weights,omega,n_override)
    h,b,rg,rn,w,c,Q,q,g,rb=(f[k] for k in ('h','b','rg','rn','w','c','Q','q','g','rb'))
    phi,psid,n=(f[k] for k in ('phi','psid','n'));sigma=f['sigma'] if sigma_override is None else sigma_override
    out=np.zeros_like(y);psi,db,ub,dg,ug,dn,un,d,V=(y[i] for i in range(9))
    out[0]=psid;out[1]=3*psid-q*q*ub;out[2]=phi+g/rb*(ug-ub)
    out[3]=4*psid-4*q*q*ug/3;out[4]=h*ug+phi+dg/4-y[lay.fg[2]]/2+g*(ub-ug)
    out[5]=4*psid-4*q*q*un/3;out[6]=h*un+phi+dn/4-y[lay.fn[2]]/2
    out[7]=3*psid-q*q*V-CBAR*Q*q*sigma/w;out[8]=f['Vd']
    Pi=y[lay.fg[2]]+y[lay.pol[0]]+y[lay.pol[2]]
    for indices,velocity,collision in [(lay.fg,ug,g),(lay.fn,un,0.)]:
        for l,i in indices.items():
            before=4*q*velocity/3 if l==2 else y[indices[l-1]]
            after=y[indices[l+1]] if l<max(indices) else 0.
            out[i]=q*(l*before-(l+1)*after)/(2*l+1)-collision*y[i]
            if l==2 and collision:out[i]+=collision*Pi/10
    for l,i in lay.pol.items():
        before=y[lay.pol[l-1]] if l else 0.;after=y[lay.pol[l+1]] if l<lay.lg else 0.
        out[i]=q*(l*before-(l+1)*after)/(2*l+1)-g*y[i]
        if l in (0,2):out[i]+=g*Pi*(.5 if l==0 else .1)
    out[lay.z]=y[lay.zd]
    if y.ndim==1:out[lay.zd]=-3*h*y[lay.zd]-omega**2*snodes**2*(f['Bq']*y[lay.z]-q*n-sigma)
    else:out[lay.zd]=-3*h*y[lay.zd]-omega**2*snodes[:,None]**2*(f['Bq']*y[lay.z]-q*n[None,:]-sigma[None,:])
    return out,f

def stage_matrix(x,fixed,lay,therm,snodes,weights,omega):
    na=lay.n+2;eye=np.eye(na);y=eye[:lay.n,:]
    out,f=rates(x,y,fixed,lay,therm,snodes,weights,omega,eye[lay.n],eye[lay.n+1])
    mat=np.zeros((na,na));mat[:lay.n]=out/f['h']
    mat[lay.n]=eye[lay.n]-f['ncalc'];mat[lay.n+1]=eye[lay.n+1]-f['sigma']
    return mat

def tridiagonal_blocks(K,B):
    n=len(K)//2;D=[K[2*i:2*i+2,2*i:2*i+2].copy() for i in range(n)];R=B.reshape(n,2,-1).copy();U=[]
    for i in range(n-1):U.append(K[2*i:2*i+2,2*i+2:2*i+4])
    for i in range(1,n):
        lower=K[2*i:2*i+2,2*i-2:2*i]
        solved=np.linalg.solve(D[i-1],np.concatenate((U[i-1],R[i-1]),axis=1))
        D[i]-=lower@solved[:,:2];R[i]-=lower@solved[:,2:]
    X=np.empty_like(R);X[-1]=np.linalg.solve(D[-1],R[-1])
    for i in range(n-2,-1,-1):X[i]=np.linalg.solve(D[i],R[i]-U[i]@X[i+1])
    return X.reshape(2*n,-1)

def block_stage_solve(Kmat,rhs,lay):
    na=lay.n+2;core=np.array(lay.core+[na+i for i in lay.core]);S=Kmat[np.ix_(core,core)].copy();R=rhs[core].copy();saved=[]
    owned=set(core.tolist())
    for tail in lay.tails:
        idx=np.array([i for t in tail for i in (t,na+t)]);owned.update(idx.tolist())
        B=np.column_stack((Kmat[np.ix_(idx,core)],rhs[idx]))
        V=tridiagonal_blocks(Kmat[np.ix_(idx,idx)],B)
        Cc=Kmat[np.ix_(core,idx)];S-=Cc@V[:,:len(core)];R-=Cc@V[:,-1];saved.append((idx,V))
    groups=np.array([[int(z),na+int(z),int(v),na+int(v)] for z,v in zip(lay.z,lay.zd)])
    owned.update(groups.ravel().tolist())
    if len(owned)!=len(rhs):raise AssertionError('Exact stage partition')
    matrices=Kmat[groups[:,:,None],groups[:,None,:]]
    B=np.concatenate((Kmat[groups[:,:,None],core[None,None,:]],rhs[groups][:,:,None]),axis=2)
    V=np.linalg.solve(matrices,B)
    for idx,res in zip(groups,V):
        Cc=Kmat[np.ix_(core,idx)];S-=Cc@res[:,:len(core)];R-=Cc@res[:,-1];saved.append((idx,res))
    solution=np.zeros(len(rhs));solution[core]=np.linalg.solve(S,R)
    for idx,V in saved:solution[idx]=V[:,-1]-V[:,:len(core)]@solution[core]
    return solution


def authenticate():
    for name,digest in {**PINS,STEM+'.md':PROTOCOL_SHA}.items():seal(BASE/name,digest)
    source=(BASE/'constrained_u_clock_gradient_early_transfer_v004.py').read_text()
    own=Path(__file__).read_text()
    defs={n.name:n for n in ast.parse(source).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
    copies={n.name:n for n in ast.parse(own).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
    for name,digest in HELPER_SHA.items():
        literal=ast.get_source_segment(source,defs[name])
        require(hashlib.sha256(literal.encode()).hexdigest()==digest and ast.get_source_segment(own,copies[name])==literal,'Exact definition-only helper '+name)
    require(hashlib.sha256(ast.get_source_segment(source,defs['radau_step']).encode()).hexdigest()==RADAU_SHA,'Original Radau reconstruction contract')
    result=read(BASE/(PARENT+'_RESULT.json'));receipt=read(BASE/(PARENT+'_RECEIPT.json'));manifest=result['manifest']
    require(receipt['lineage']==manifest and receipt['source_sha256']==manifest['source_sha256']==PINS['constrained_u_clock_gradient_early_transfer_v004.py'],'Actual failed-parent source/lineage')
    require(receipt['result_sha256']==PINS[PARENT+'_RESULT.json'] and result['status']==receipt['status']=='NEW_EARLY_TRANSFER_ARITHMETIC_FAILED','Failed original disposition retained')
    gates=result['numerical_gates']
    require(len(gates)==527 and all(type(g['passed']) is bool for g in gates) and sum(g['passed'] for g in gates)==375 and not result['all_numerical_gates_passed'],'375 PASS / 152 FAIL original gates')
    require(manifest['omegas']==list(OMEGAS) and manifest['trials'][1]==TIME_SPEC and np.__version__==manifest['numpy_version'],'Original TIME / four inertias / NumPy ABI')
    require(manifest['fixed']['curvature']==CURVATURE and manifest['fixed']['k_Mpc_inverse']==K,'Original source amplitude and wavenumber')
    for path,digest in manifest['inputs'].items():seal(path,digest)
    for suffix,key in (('_MANIFEST.json','manifest_sha256'),('_JOURNAL.jsonl','journal_sha256'),('_REPORT.md','report_sha256')):seal(BASE/(PARENT+suffix),receipt[key])
    require(read(BASE/(PARENT+'_MANIFEST.json'))==manifest,'Actual manifest bytes and content')
    for path,digest in receipt['checkpoint_seals'].items():seal(path,digest)
    events=[json.loads(line) for line in (BASE/(PARENT+'_JOURNAL.jsonl')).read_text().splitlines()]
    expected=[(spec[0],n) for spec in manifest['trials'] for n in range(0,spec[1]+1,512)]
    actual=[];owner=None;files=set()
    for index,e in enumerate(events):
        require(e['owner']=='root' and type(e['pid']) is int and e['pid']>0 and e['source_sha256']==manifest['source_sha256'] and e['manifest_sha256']==receipt['manifest_sha256'],'Original root/PID/source/manifest event')
        if e['event']=='OWNER_START':owner=e['pid'];continue
        require(e['pid']==owner,'Original owner epoch')
        if e['event']=='OWNER_COMPLETE':
            require(index==len(events)-1 and e['result_sha256']==receipt['result_sha256'] and e['gates']==527 and e['passed']==375 and e['status']==result['status'],'Failed parent natural closure')
            continue
        require(e['event']=='CHECKPOINT','Original checkpoint event')
        actual.append((e['trial'],e['n']))
        pn=PARENT+'_'+e['trial']+'_CP_'+str(e['n']).zfill(6)+'.json';cn=pn[:-5]+'_COMMIT.json'
        require(e['payload']==pn and sha(BASE/pn)==e['sha256'] and sha(BASE/cn)==e['commit_sha256'],'Actual original CP / commit bytes')
        co=read(BASE/cn)
        require(co['payload']==pn and co['sha256']==e['sha256'] and co['n']==e['n'] and co['meta']['lineage']==manifest,'Original CP complete lineage')
        files.update((pn,cn))
    require(len(actual)==111 and actual==expected and events[0]['event']=='OWNER_START' and events[-1]['event']=='OWNER_COMPLETE','Complete original 111 CP natural event sequence')
    require(set(p.name for p in BASE.glob(PARENT+'_*_CP_*.json'))==files,'No original orphan checkpoints')
    targets=manifest['targets'];x0=math.log(AI)
    expected_targets=sorted(set([x0+k*(-x0)/64 for k in range(65)]+[-math.log(1+z) for z in (8000.,1100.,800.)]))
    require(targets==expected_targets and len(targets)==68,'Exact original split targets')
    row=result['rows'][1];lay=Layout(*TIME_SPEC[2:5]);names=lay.names()
    require(lay.n==392 and row['label']=='TIME' and row['spec']==TIME_SPEC and row['state_names']==names and len(row['snodes'])==len(row['weights'])==32,'Full retained TIME axes and saved nodes')
    require([s['x'] for s in row['snapshots']]==targets,'Ordered original TIME snapshots')
    selected=[]
    for n in SELECTED:
        pn=PARENT+'_TIME_CP_'+str(n).zfill(6)+'.json';co=read(BASE/(pn[:-5]+'_COMMIT.json'));cp=read(BASE/pn)
        meta=dict(lineage=manifest,spec=TIME_SPEC,state_shape=[4,lay.n],state_names=names)
        require(set(cp)==set(('meta','n','state','snapshots','step_errors','dense_errors')) and cp['n']==n and cp['meta']==meta,'Selected exact CP schema / axes')
        require(co==dict(meta=meta,n=n,payload=pn,sha256=PINS[pn]),'Selected direct committed CP')
        require(len(cp['state'])==4 and all(len(s)==lay.n and all(type(v) in (int,float) and math.isfinite(v) for v in s) for s in cp['state']),'Selected full finite four-mode state')
        endpoint=x0+n*(-x0)/TIME_SPEC[1]
        require(cp['snapshots']==[s for s in row['snapshots'] if s['x']<=endpoint+1e-14] and cp['snapshots'][-1]['x']==endpoint and cp['state']==[s['state'] for s in cp['snapshots'][-1]['cases']],'Selected lossless TIME state prefix')
        selected.append(cp)
    return result,receipt,lay,selected


def construct_system(y,x,dx,fixed,lay,therm,snodes,weights,omega):
    # Literal Radau K/rhs construction; do not return or propagate a next state.
    na=lay.n+2;m1=stage_matrix(x+dx/3,fixed,lay,therm,snodes,weights,omega);m2=stage_matrix(x+dx,fixed,lay,therm,snodes,weights,omega)
    eye=np.eye(na);eye[lay.n:]=0.
    Kmat=np.block([[eye-dx*(5/12)*m1,dx*m2/12],[-dx*.75*m1,eye-dx*.25*m2]])
    Kmat[lay.n:na]=0.;Kmat[lay.n:na,:na]=m1[lay.n:]
    Kmat[na+lay.n:]=0.;Kmat[na+lay.n:,na:]=m2[lay.n:]
    rhs=np.tile(np.concatenate((y,[0.,0.])),2)
    require(Kmat.shape==(788,788) and rhs.shape==(788,) and np.all(np.isfinite(Kmat)) and np.all(np.isfinite(rhs)),'Finite full original Radau system')
    return Kmat,rhs


def coordinate_scales(Kmat):
    A=Kmat.copy();dr=np.ones(len(A));dc=np.ones(len(A))
    for _ in range(BALANCE_PASSES):
        rows=np.max(np.abs(A),axis=1);require(bool(np.all(rows>0)),'No zero equation row')
        rr=1/np.sqrt(rows);dr*=rr;A=rr[:,None]*A
        columns=np.max(np.abs(A),axis=0);require(bool(np.all(columns>0)),'No zero coordinate column')
        cc=1/np.sqrt(columns);dc*=cc;A=A*cc[None,:]
    require(bool(np.all(np.isfinite(dr)) and np.all(np.isfinite(dc)) and np.all(dr>0) and np.all(dc>0)),'Strictly positive reversible scales')
    A=(dr[:,None]*Kmat)*dc[None,:]
    require(bool(np.all(np.isfinite(A))) and np.array_equal(A==0,Kmat==0),'No entry or mode removed by scaling')
    return dr,dc,A


def residual(Kmat,rhs,stages):
    r=Kmat@stages-rhs;den=np.maximum(np.abs(Kmat)@np.abs(stages)+np.abs(rhs),abs(CURVATURE)*1e-16)
    require(bool(np.all(np.isfinite(r)) and np.all(np.isfinite(den)) and np.all(den>0)),'Finite original residual')
    return float(np.max(np.abs(r)/den)),r,den


def disagreement(a,b):
    return float(np.max(np.abs(a-b))/max(float(np.max(np.abs(b))),CURVATURE*1e-16))


def refine(Kmat,rhs,A,dr,dc,stages,solve):
    current=stages.copy();trace=[]
    lk=Kmat.astype(np.longdouble);lr=rhs.astype(np.longdouble)
    for iteration in range(REFINEMENT_STEPS):
        r=lr-lk@current.astype(np.longdouble)
        delta=dc*solve(A,dr*np.asarray(r,dtype=np.float64))
        current=current+delta
        require(bool(np.all(np.isfinite(current))), 'Finite fixed refinement stage')
        error,_,_=residual(Kmat,rhs,current)
        trace.append(dict(iteration=iteration+1,proper_stage_residual=error,correction_max=float(np.max(abs(delta))),stage=current.tolist()))
    return current,trace


def condition_estimate(A):
    try:
        inverse=np.linalg.solve(A,np.eye(len(A)))
        value=float(np.linalg.norm(A,ord=np.inf)*np.linalg.norm(inverse,ord=np.inf))
        return dict(value=value if math.isfinite(value) else None,refusal=None if math.isfinite(value) else 'NONFINITE_FLOAT_CONDITION_ESTIMATE',scope='Floating inverse-norm estimate; nondirected; no acceptance gate')
    except np.linalg.LinAlgError:
        return dict(value=None,refusal='SINGULAR_FLOAT_CONDITION_ESTIMATE',scope='No condition or stability certification')


def row_attribution(Kmat,rhs,stages,lay):
    error,r,den=residual(Kmat,rhs,stages);index=int(np.argmax(abs(r)/den));na=lay.n+2;j=index%na
    fields=lay.names()+['algebraic_n_U','algebraic_sigma'];products=Kmat[index]*stages
    group='core' if j in lay.core else 'kinetic_mode' if j in set(lay.z.tolist()+lay.zd.tolist()) else 'radiation_tail'
    magnitude=float(math.fsum(abs(float(v)) for v in products)+abs(float(rhs[index])))
    stable=float(math.fsum([*(float(v) for v in products),-float(rhs[index])]))
    ratio=magnitude/max(abs(stable),1e-300)
    return dict(row=index,stage=index//na+1,field=fields[j],group=group,proper_error=error,ordinary_residual=float(r[index]),compensated_residual=stable,denominator=float(den[index]),rhs=float(rhs[index]),sum_absolute_products=magnitude,product_terms=products.tolist(),cancellation_ratio=ratio if math.isfinite(ratio) else None,cancellation_ratio_refusal=None if math.isfinite(ratio) else 'NONFINITE_FLOAT_CANCELLATION_RATIO')


def array_info(array):
    require(array.dtype==np.dtype('float64') and bool(np.all(np.isfinite(array))),'Lossless finite binary64 inventory')
    return dict(shape=list(array.shape),dtype=str(array.dtype),sha256_raw_c_bytes=hashlib.sha256(array.tobytes(order='C')).hexdigest())


def main():
    global RUN_SOURCE,RUN_MANIFEST
    tick=time.monotonic();RUN_SOURCE=sha(__file__)
    parent,receipt,lay,checkpoints=authenticate();manifest=parent['manifest'];fixed=manifest['fixed'];row=parent['rows'][1]
    snodes=np.array(row['snodes']);weights=np.array(row['weights']);therm=Thermal('HALF',1,fixed)
    require(bool(np.all(snodes>0) and np.all(weights>0)),'Unchanged positive retained nodes / weights')
    run=dict(owner='root',pid=os.getpid(),source_sha256=RUN_SOURCE,inputs=dict(SEALS),parent_status=parent['status'],parent_passed=375,parent_failed=152,selected=list(SELECTED),omegas=list(OMEGAS),time_spec=TIME_SPEC,matrix_shape=[788,788],balance_passes=BALANCE_PASSES,refinement_steps=REFINEMENT_STEPS,tolerance=TOL,numpy_version=np.__version__,longdouble_mantissa_bits=int(np.finfo(np.longdouble).nmant),scope='Twenty saved-stage systems; no trajectory qualification')
    RUN_MANIFEST=write(STEM+'_MANIFEST.json',run);journal('OWNER_START')
    rows=[];gates=[];arrays={};inventory={};x0=math.log(AI);dx=-x0/TIME_SPEC[1]
    for saved in checkpoints:
        n=saved['n'];left=x0+n*dx;right=x0+(n+1)*dx
        cuts=[x for x in manifest['targets'] if left<x<=right]
        points=cuts+([right] if not cuts or cuts[-1]!=right else [])
        destination=points[0];width=destination-left
        require(width>0 and destination<=right,'First exact original target-split substep')
        for oi,omega in enumerate(OMEGAS):
            key='n'+str(n).zfill(6)+'_o'+str(oi);y=np.array(saved['state'][oi])
            Kmat,rhs=construct_system(y,left,width,fixed,lay,therm,snodes,weights,omega)
            raw=block_stage_solve(Kmat,rhs,lay);dense=np.linalg.solve(Kmat,rhs)
            dr,dc,A=coordinate_scales(Kmat);b=dr*rhs
            sb=dc*block_stage_solve(A,b,lay);sd=dc*np.linalg.solve(A,b)
            block,bt=refine(Kmat,rhs,A,dr,dc,sb,lambda mat,vec:block_stage_solve(mat,vec,lay))
            independent,dt=refine(Kmat,rhs,A,dr,dc,sd,np.linalg.solve)
            metrics=dict(raw_block_residual=residual(Kmat,rhs,raw)[0],raw_dense_residual=residual(Kmat,rhs,dense)[0],raw_block_dense_difference=disagreement(raw,dense),corrected_block_residual=residual(Kmat,rhs,block)[0],corrected_dense_residual=residual(Kmat,rhs,independent)[0],corrected_block_dense_difference=disagreement(block,independent))
            for name,value in metrics.items():gates.append(dict(case=key,name=name,error=value,tolerance=TOL,passed=bool(math.isfinite(value) and value<=TOL),role='corrected_candidate' if name.startswith('corrected') else 'preserved_raw_diagnostic'))
            casearrays=dict(K=Kmat,rhs=rhs,raw_block=raw,raw_dense=dense,row_scale=dr,column_scale=dc,scaled_K=A,scaled_rhs=b,initial_scaled_block=sb,initial_scaled_dense=sd,corrected_block=block,corrected_dense=independent,direct_raw_difference=raw-dense,direct_corrected_difference=block-independent)
            for label,stage in (('raw_block',raw),('raw_dense',dense),('corrected_block',block),('corrected_dense',independent)):
                _,rr,dd=residual(Kmat,rhs,stage);casearrays[label+'_residual']=rr;casearrays[label+'_denominator']=dd
            for label,array in casearrays.items():
                arraykey=key+'_'+label;arrays[arraykey]=array;inventory[arraykey]=array_info(array)
            rows.append(dict(case=key,checkpoint=n,omega=omega,x_left=left,x_right=destination,full_grid_right=right,width=width,target_split=bool(cuts),state_sha256_raw=hashlib.sha256(y.tobytes()).hexdigest(),metrics=metrics,raw_condition=condition_estimate(Kmat),scaled_condition=condition_estimate(A),row_scale_min=float(min(dr)),row_scale_max=float(max(dr)),column_scale_min=float(min(dc)),column_scale_max=float(max(dc)),initial_scaled_residuals=dict(block=residual(Kmat,rhs,sb)[0],dense=residual(Kmat,rhs,sd)[0]),block_refinement=bt,dense_refinement=dt,worst_raw=row_attribution(Kmat,rhs,raw,lay),worst_corrected=row_attribution(Kmat,rhs,block,lay)))
            journal('STAGE_SYSTEM_COMPLETE',case=key,checkpoint=n,omega=omega,corrected_gates_passed=bool(all(g['passed'] for g in gates[-3:])))
            print(json.dumps(dict(case=key,completed_systems=len(rows),total_systems=20)),flush=True)
    require(len(rows)==20 and len(gates)==120 and len(inventory)==440,'Fixed 20 / 120 / 440 census')
    recheck();npz=BASE/(STEM+'_SYSTEMS.npz')
    with npz.open('xb') as f:np.savez_compressed(f,**arrays)
    npz.chmod(0o444);CREATED[str(npz.resolve())]=sha(npz)
    with np.load(npz,allow_pickle=False) as saved:
        require(set(saved.files)==set(inventory),'Exact compressed array key inventory')
        for key in saved.files:require(array_info(saved[key])==inventory[key],'Lossless compressed array '+key)
    corrected=[g for g in gates if g['role']=='corrected_candidate'];require(len(corrected)==60,'Sixty exact corrected gates')
    qualified=all(g['passed'] for g in corrected);status='SAVED_STAGE_NUMERICAL_CONDITIONING_PASSED' if qualified else 'SAVED_STAGE_NUMERICAL_CONDITIONING_FAILED'
    result=dict(status=status,all_corrected_stage_gates_passed=qualified,manifest=run,rows=rows,numerical_gates=gates,array_inventory=inventory,systems_sha256=sha(npz),parent_status=parent['status'],original_numerical_gates=parent['numerical_gates'],original_endpoint_domain_heads=[s['domain_heads'] for s in parent['rows'][1]['snapshots'][-1]['cases']],elapsed_seconds=time.monotonic()-tick,scope='Algebraic stage conditioning only; original 152 numerical failures and sampled-domain refusals preserved; no trajectory recovery or physical qualification')
    recheck();rh=write(STEM+'_RESULT.json',result)
    lines=['# Saved early Radau stage conditioning V001','',status,'','Twenty systems; 120 exact threshold records; corrected candidate '+str(sum(g['passed'] for g in corrected))+'/60 PASS. Original early parent remains 375/527 PASS and 152 FAIL.','','| CP n | omega/Hstar | raw residual | raw dense disagreement | corrected residual | corrected dense disagreement |','|---|---|---|---|---|---|']
    for r in rows:
        m=r['metrics'];lines.append('| '+str(r['checkpoint'])+' | '+str(r['omega'])+' | '+str(m['raw_block_residual'])+' | '+str(m['raw_block_dense_difference'])+' | '+str(m['corrected_block_residual'])+' | '+str(m['corrected_block_dense_difference'])+' |')
    lines+=['','No state propagation, source change, accepted trajectory or physical-domain qualification. All stages, scaling, row attribution, signed differences and condition-estimate refusals remain saved.']
    write(STEM+'_REPORT.md',('\n'.join(lines)+'\n').encode(),raw=True)
    journal('OWNER_COMPLETE',status=status,result_sha256=rh,systems_sha256=sha(npz),systems=20,gate_count=120,corrected_passed=sum(g['passed'] for g in corrected))
    jp=BASE/(STEM+'_JOURNAL.jsonl');jp.chmod(0o444);CREATED[str(jp.resolve())]=sha(jp)
    events=read_journal(jp)
    require([e['event'] for e in events]==['OWNER_START']+['STAGE_SYSTEM_COMPLETE']*20+['OWNER_COMPLETE'],'Exact diagnostic journal census')
    require(all(e['owner']=='root' and e['pid']==os.getpid() and e['source_sha256']==RUN_SOURCE and e['manifest_sha256']==RUN_MANIFEST for e in events),'Diagnostic owner/source/manifest binding')
    recheck();write(STEM+'_RECEIPT.json',dict(status=status,source_sha256=RUN_SOURCE,manifest_sha256=RUN_MANIFEST,result_sha256=rh,journal_sha256=sha(jp),input_sha256=dict(SEALS),output_sha256=dict(CREATED),systems=20,gate_count=120,corrected_passed=sum(g['passed'] for g in corrected),original_parent_failed=152))
    recheck();return 0 if qualified else 3


def read_journal(path):return [json.loads(line) for line in Path(path).read_text().splitlines()]


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--execute',action='store_true')
    if not parser.parse_args().execute:raise SystemExit('Root alone launches --execute after full reviews')
    if any((BASE/(STEM+s)).exists() for s in ('_MANIFEST.json','_JOURNAL.jsonl','_SYSTEMS.npz','_RESULT.json','_REPORT.md','_RECEIPT.json')) or any(BASE.glob(STEM+'_FAILED_*.json')):raise SystemExit('Existing runtime prefix; no overwrite, resume or extra error mutation')
    try:raise SystemExit(main())
    except Exception as exc:
        stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')
        write(STEM+'_FAILED_'+stamp+'.json',dict(status='EXECUTION_ERROR_PRESERVED',error=repr(exc),owner='root',pid=os.getpid(),time=now(),source_sha256=sha(__file__)))
        raise

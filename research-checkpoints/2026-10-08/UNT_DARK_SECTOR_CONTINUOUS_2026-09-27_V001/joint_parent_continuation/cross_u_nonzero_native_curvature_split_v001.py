"""Root-owned fixed accepted-state positive native curvature split; immutable parent fields."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, importlib, json, math, os

BASE=Path(__file__).resolve().parent
STEM='CROSS_U_NONZERO_NATIVE_CURVATURE_SPLIT_V001'
PARENT='CROSS_U_NGC3198_MINRES_RECOVERY_V003'
AUTHOR_DRAFT=False
CASES=['E1em05_HI0_H20','E1em04_HI0_H20','E1em03_HI0_H20']
PINS={'CROSS_U_NONZERO_NATIVE_CURVATURE_SPLIT_V001.md': '3eb392f83607b7c6373c6d5cdae012fe7fba9984fd4ff37f74935bb1b2cebc0a',
 'cross_u_ngc3198_nonlinear_disk_v001.py': 'ae4285fc9c19cdf2d8efa176ac3d770b7eaf379a75fa3b9627bc9d3f6f3179e1',
 'CROSS_U_NGC3198_NONLINEAR_DISK_V001.md': 'a5e7f129c46af6aac63bbec179d98fe8ae9d3ac7178d0598bb23ba21eaf92b76',
 'CROSS_U_NGC3198_NONLINEAR_DISK_V001_RESULT.json': '720cbaf0902285d35dc3a50d59f81d266431c7d91b4985eb19ab822b0b14413b',
 'cross_u_q1_projection_stiffness_v001.py': '63363c94d8a96a0444ab932f360f6bf9501fc1020064b509f5faf7e37f0e42bf',
 'CROSS_U_Q1_PROJECTION_STIFFNESS_V001.md': 'c3ab70d3274feb39499c2b0eca482686085071362657a4766a93ecba071f00f9',
 'CROSS_U_Q1_PROJECTION_STIFFNESS_V001_RESULT.json': 'eb99696cfc5ff635cc56dbe3dd128f7ce7032529ff62f0c4037f0b3cfc346300',
 'CROSS_U_Q1_PROJECTION_STIFFNESS_V001_RECEIPT.json': 'fe87ff6b30ae9d3086319e70a6cf5798e6aa3b0c9aabe1a781bb2e821820b474',
 'cross_u_ngc3198_minres_recovery_v003.py': '5f807a858ac7b00e29b724a39e4d1de4d96e102442530b067bbc2ee7953a5683',
 'CROSS_U_NGC3198_MINRES_RECOVERY_V003.md': '91f8df979025c53ee96601839e1adad7eacb6436b7444ab2e488c53fc9a01dc8',
 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_RESULT.json': '9da87a64f0e37c17530d34aae0f2ffb0efdf16d610763adcddff875c0a87ec8c',
 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_RECEIPT.json': 'eee323ea063832eac8f9d731823cf9fd3e5135930e74d9a477646d60b5300eb5'}
STATE_BINDINGS={'E1em05_HI0_H20': {'case_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em05_HI0_H20_CASE.json',
                    'case_sha256': 'aacab61f915a1bc4347377da1d5b5b7bdcd515ad519cd5b1661ce8c61c71d299',
                    'terminal': {'file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em05_HI0_H20_LINEAR_FAILED_001.npz',
                                 'sha256': '2dd4897d541dc74543bc7185894a0879d5a4ff99c090bf4bf4a369eb29cdef15',
                                 'commit_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em05_HI0_H20_LINEAR_FAILED_001.npz.commit.json',
                                 'commit_sha256': '5fe0d9fe062eecbcb65997965569ab58e4f56e6a742ec4df84728691bd571b2f',
                                 'receipt_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_RECEIPT.json',
                                 'receipt_sha256': 'eee323ea063832eac8f9d731823cf9fd3e5135930e74d9a477646d60b5300eb5'},
                    'previous': {'file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em05_HI0_H20_STEP_000.npz',
                                 'sha256': '3b11acd125a560a73ff580b595984d7b8631aa7e3828a46c6ca0f61c7210c979',
                                 'commit_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em05_HI0_H20_STEP_000.npz.commit.json',
                                 'commit_sha256': '3ec353f2ee5125fe5a405789a2a1e820c60e3ab7a6f9c6250c06ec5ae3a4286f',
                                 'receipt_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_RECEIPT.json',
                                 'receipt_sha256': 'eee323ea063832eac8f9d731823cf9fd3e5135930e74d9a477646d60b5300eb5'}},
 'E1em04_HI0_H20': {'case_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em04_HI0_H20_CASE.json',
                    'case_sha256': 'e9313e8356bb58177a6b891a028d0293b1feb0a81997f32e997623a5ad0ff7be',
                    'terminal': {'file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em04_HI0_H20_LINEAR_FAILED_000.npz',
                                 'sha256': 'c0b9f237e81f8d8d4d62fb2fa5901aae16711bfc31c0cc70979f687d01ff2aa4',
                                 'commit_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em04_HI0_H20_LINEAR_FAILED_000.npz.commit.json',
                                 'commit_sha256': '14e42f5dea351040f26cd0b14d237a56e1e21a167d4c8e80453fc222bceec5b4',
                                 'receipt_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_RECEIPT.json',
                                 'receipt_sha256': 'eee323ea063832eac8f9d731823cf9fd3e5135930e74d9a477646d60b5300eb5'},
                    'previous': {'file': 'CROSS_U_NGC3198_PARTIAL_RECOVERY_V002_E1em04_HI0_H20_STEP_028.npz',
                                 'sha256': '2a06de35a04023ffa10862c63265e82c9a8e56c25092807242e147d2916551f2',
                                 'commit_file': 'CROSS_U_NGC3198_PARTIAL_RECOVERY_V002_E1em04_HI0_H20_STEP_028.npz.commit.json',
                                 'commit_sha256': '86b9ec60372acf209a4a0487b50dcef290708e93f69609f81bc3e2dfd1683ece',
                                 'receipt_file': 'CROSS_U_NGC3198_PARTIAL_RECOVERY_V002_RECEIPT.json',
                                 'receipt_sha256': 'c72830fb31defeae5443beed55eec910b08c2bf520a45f14853c9cdfe59950a1'}},
 'E1em03_HI0_H20': {'case_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em03_HI0_H20_CASE.json',
                    'case_sha256': '51c138f74b213b6fa455329c578d071eb99eeacd590efd81977ee8f1c715ffc8',
                    'terminal': {'file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em03_HI0_H20_LINEAR_FAILED_001.npz',
                                 'sha256': 'fe0b587bb8a979e260d991216451fb61adc19d3afba37ec6f100f17c0afab24d',
                                 'commit_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em03_HI0_H20_LINEAR_FAILED_001.npz.commit.json',
                                 'commit_sha256': '15da0758f2cebf87c684d225703c7327a3b9495751fd0445462b239f38aa215a',
                                 'receipt_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_RECEIPT.json',
                                 'receipt_sha256': 'eee323ea063832eac8f9d731823cf9fd3e5135930e74d9a477646d60b5300eb5'},
                    'previous': {'file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em03_HI0_H20_STEP_000.npz',
                                 'sha256': 'a0b9f7ad56886da85d057f29019abb018cef8f3491406c003f8ba48a01052208',
                                 'commit_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em03_HI0_H20_STEP_000.npz.commit.json',
                                 'commit_sha256': '993d047e5bf2805e01d1b2e4b96b5dc1fbf009f7f131728fab11caca43635d73',
                                 'receipt_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_RECEIPT.json',
                                 'receipt_sha256': 'eee323ea063832eac8f9d731823cf9fd3e5135930e74d9a477646d60b5300eb5'}}}
CORE_INPUT_PINS={'CROSS_U_NGC3198_NONLINEAR_DISK_V001.md': 'a5e7f129c46af6aac63bbec179d98fe8ae9d3ac7178d0598bb23ba21eaf92b76', 'galaxy_density.py': '9819b9cb1f63baea07eb06a150dbda3113d7850d9ac24a13ee65e96f6f07bb6c', 'NGC3198_BARYON_INPUT.json': '8895693861ee0db1b42136c6aac7f0fb9fa9e0e84c72c69e8c8e3c89ba0e78d1', 'NGC3198_FIXED_DENSITY_PROTOCOL.md': '0dd06827f2b6cddb4f158f9c21eaccf70bf44597d0bd8891d39a96eb6380d10b', 'LINEAR_SOURCE_GALAXY_REFERENCE_V001.md': '399fa90b083afe9a014bc47e2e3d70c80f1c8ef5708edb205cb348b8d6f72801', 'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md': 'e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RESULT.json': 'e9f7b2070e762920cb3548ccbe11c5f46efd1a262065ba594afaca6635acc35f', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RECEIPT.json': 'df514792bf703b6ce6b9e4c2a64e2ac19c407dffa0f14acf9bb9f75b6acc64e6', '../ngc3198_sparc_excerpt_v001.txt': '58a303f78b8dd884aeb7be9a8d98514fa5e84665265e958f3b75479c19cfa900'}
np=core=None
RECEIPTS={}

def now():return datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def finite(v):return float(v) if math.isfinite(v) else None

def native_tree(obj):
    if obj is None or type(obj) in (str,bool,int):return
    if type(obj) is float:assert math.isfinite(obj);return
    if type(obj) is list:
        for v in obj:native_tree(v)
        return
    assert type(obj) is dict and all(type(k) is str for k in obj)
    for v in obj.values():native_tree(v)

def encode(obj):
    native_tree(obj)
    return (json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()

def publish(name,obj):
    raw=encode(obj);p=BASE/name
    with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    p.chmod(0o444);assert p.read_bytes()==raw
    return sha(p)

def inputs():
    pins=dict(CORE_INPUT_PINS)
    for name,h in PINS.items():
        if name in pins:assert pins[name]==h
        pins[name]=h
    for name in CASES:
        b=STATE_BINDINGS[name];pairs=[(b['case_file'],b['case_sha256'])]
        for key in ('terminal','previous'):
            d=b[key];pairs.extend([(d['file'],d['sha256']),(d['commit_file'],d['commit_sha256']),
                                   (d['receipt_file'],d['receipt_sha256'])])
        for path,h in pairs:
            if path in pins:assert pins[path]==h
            pins[path]=h
    return pins

def auth():
    assert not AUTHOR_DRAFT,'Unexecuted author draft: parent/source/schema preflight pending'
    for name,h in inputs().items():
        assert not h.startswith('AUTHOR') and sha(BASE/name)==h,('changed or pending input',name)
    if core is not None:core.authenticate()

def closed_receipt(name,h):
    assert sha(BASE/name)==h
    if name in RECEIPTS:
        assert RECEIPTS[name][0]==h
        return RECEIPTS[name][1]
    r=json.loads((BASE/name).read_text());native_tree(r)
    assert r['owner']=='root' and type(r['pid']) is int and r['pid']>0
    assert datetime.fromisoformat(r['started'])<datetime.fromisoformat(r['closed'])
    assert type(r['output_sha256']) is dict and r['output_sha256']
    for n,k in r['output_sha256'].items():assert sha(BASE/n)==k,('changed closed output',n)
    RECEIPTS[name]=(h,r)
    return r

def load_state(binding):
    receipt=closed_receipt(binding['receipt_file'],binding['receipt_sha256'])
    name=binding['file'];cn=binding['commit_file']
    assert receipt['output_sha256'][name]==binding['sha256']==sha(BASE/name)
    assert receipt['output_sha256'][cn]==binding['commit_sha256']==sha(BASE/cn)
    commit=json.loads((BASE/cn).read_text());native_tree(commit)
    assert commit['file']==name and commit['sha256']==binding['sha256']
    with np.load(BASE/name,allow_pickle=False) as data:
        assert {'state','history','identity'}<=set(data.files)
        x=data['state'].copy();history=json.loads(str(data['history']));identity=json.loads(str(data['identity']))
    native_tree(history);native_tree(identity)
    assert commit['identity']==identity and np.all(np.isfinite(x))
    return x,history,identity

def accepted_history(filename,history,case):
    prefix=[]
    if filename.startswith(PARENT+'_'):
        prefix=case.get('ancestral_checkpoint_history',[])+case.get('parent_checkpoint_history',[])
    elif filename.startswith('CROSS_U_NGC3198_PARTIAL_RECOVERY_V002_'):
        prefix=case.get('ancestral_checkpoint_history',[])
    else:assert filename.startswith('CROSS_U_NGC3198_NONLINEAR_DISK_V001_')
    return [row for row in prefix+history if row.get('accepted') is True]

def paired_states(name,parent):
    binding=STATE_BINDINGS[name];p=BASE/binding['case_file']
    assert sha(p)==binding['case_sha256']
    case=json.loads(p.read_text());native_tree(case)
    actual=next(c for c in parent['cases'] if c['identity']['case']==name)
    assert case==actual
    x,h,i=load_state(binding['terminal']);old,oh,oi=load_state(binding['previous'])
    assert x.shape==old.shape and i==case['identity']
    keys=('case','eps','hi_tail','h2_tail','Hunit','grid_shape','r_kpc','z_kpc')
    assert all(i[k]==oi[k] for k in keys)
    a=accepted_history(binding['terminal']['file'],h,case)
    b=accepted_history(binding['previous']['file'],oh,case)
    assert a==accepted_history(binding['terminal']['file'],case['history'],case),'Not the terminal accepted prefix'
    assert len(a)==len(b)+1 and a[:-1]==b,'Not the immediately preceding accepted event'
    assert i['hi_tail'] is False and i['h2_tail'] is False
    assert i['eps'] in (1e-5,1e-4,1e-3)
    return x,old,i,case

def pcg(A,b,diagonal,tolerance=1e-10,cap=600):
    x=np.zeros_like(b);r=b.copy();norm=float(np.linalg.norm(b));reason='iteration_allowance';it=0
    if norm==0 and np.all(b==0):return x,dict(ok=True,error=0.,iterations=0,reason='zero_rhs')
    if not math.isfinite(norm) or norm<=0:return x,dict(ok=False,error=None,iterations=0,reason='nonfinite_or_underflow_rhs')
    z=r/diagonal;p=z.copy();rz=float(np.sum(r*z))
    for it in range(1,cap+1):
        if not np.all(np.isfinite(p)) or not math.isfinite(rz) or rz<=0:reason='direction_breakdown';break
        Ap=A(p);den=float(np.sum(p*Ap))
        if not math.isfinite(den) or den<=0:reason='positive_block_breakdown';break
        alpha=rz/den
        if not math.isfinite(alpha):reason='nonfinite_alpha';break
        x+=alpha*p;r-=alpha*Ap
        if not np.all(np.isfinite(x)):reason='nonfinite_state';break
        if float(np.linalg.norm(r))/norm<=tolerance:
            r=b-A(x)
            if float(np.linalg.norm(r))/norm<=tolerance:reason='true_residual';break
            z=r/diagonal;p=z.copy();rz=float(np.sum(r*z));continue
        z=r/diagonal;new=float(np.sum(r*z))
        if not math.isfinite(new) or new<=0:reason='positive_residual_breakdown';break
        beta=new/rz
        if not math.isfinite(beta):reason='nonfinite_beta';break
        p=z+beta*p;rz=new
    error=finite(float(np.linalg.norm(b-A(x))/norm)) if np.all(np.isfinite(x)) else None
    return x,dict(ok=error is not None and error<=tolerance,error=error,iterations=it,reason=reason)

class NativeForms:
    def __init__(self,x,r,z):
        nodes,weights=np.polynomial.legendre.leggauss(32)
        self.xi=(nodes+1)/2;self.w=weights*self.xi
        assert np.all(self.w>0)
        self.alpha=1/(self.w*core.GC**2*self.xi**4)
        self.shape=(32,2,len(r),len(z));self.mask=np.ones((2,len(r),len(z)),bool)
        self.mask[:,-1,:]=False;self.mask[:,:,-1]=False
        self.mask[0,0,:]=False;self.mask[1,:,0]=False
        self.mass=np.zeros((2,len(r),len(z)));self.diag0=np.zeros(self.shape);self.diage=np.zeros(self.shape)
        self.quad=[];v=np.stack([x[1::2],x[2::2]],axis=1)
        assert v.shape==self.shape and np.all(v[:,~self.mask]==0)
        for rr,vol,shapes in core.shape_quadrature(r,z):
            vv,_,_=core.interpolate(v,shapes);a=self.alpha[:,None,None]
            norm=np.sum(vv*vv,axis=1);t=1+a*norm
            self.quad.append((rr,vol,shapes,vv,a,norm,t))
            for n,nr,nz,i,j in shapes:
                sl=(slice(None),slice(None),slice(i,len(r)-1+i),slice(j,len(z)-1+j))
                ms=(slice(None),slice(i,len(r)-1+i),slice(j,len(z)-1+j))
                self.mass[ms]+=vol*n*n
                d=vol*n*n*(t[:,None]+2*a[:,None]*vv*vv)
                self.diag0[sl]+=d
                self.diage[sl]+=d+vol*core.ELL**2*(nr*nr+nz*nz)
                self.diage[sl][:,0]+=vol*core.ELL**2*n*n/rr**2
        self.mass[~self.mask]=1;self.diag0[:,~self.mask]=1;self.diage[:,~self.mask]=1
        assert np.all(np.isfinite(self.diage)) and np.all(self.diag0>0) and np.all(self.diage>0)

    def apply(self,y,ell):
        assert y.shape==self.shape and np.all(y[:,~self.mask]==0) and np.all(np.isfinite(y))
        out=np.zeros_like(y)
        for rr,vol,shapes,vv,a,norm,t in self.quad:
            val,gr,gz=core.interpolate(y,shapes);dot=np.sum(vv*val,axis=1)
            hv=t[:,None]*val+2*a[:,None]*vv*dot[:,None]
            hv[:,0]+=ell**2*val[:,0]/rr**2
            core.add(out,hv,ell**2*gr,ell**2*gz,vol,shapes)
        out[:,~self.mask]=0;return out

    def load(self,p):
        b=np.zeros(self.shape);K=0.;local=0.;quartic=0.
        for rr,vol,shapes,vv,a,norm,t in self.quad:
            _,gr,gz=core.interpolate(p,shapes);gg=gr*gr+gz*gz;g=np.stack([gr,gz])
            bg=np.sqrt(self.w)[:,None,None,None]*g[None];zero=np.zeros_like(bg)
            core.add(b,bg,zero,zero,vol,shapes);K+=float(np.sum(vol*gg))
            dot=vv[:,0]*gr+vv[:,1]*gz;cross=vv[:,0]*gz-vv[:,1]*gr;h=1+3*a*norm
            inv=gg[None]/h+2*a*cross*cross/(t*h)
            qq=a*norm*gg[None]/t+2*a*dot*dot/(t*h)
            local+=float(np.sum(vol*self.w[:,None,None]*inv))
            quartic+=float(np.sum(vol*self.w[:,None,None]*qq))
        b[:,~self.mask]=0
        return b,K,local,quartic

    def direct(self,p,y,ell):
        value=0.
        for rr,vol,shapes,vv,a,norm,t in self.quad:
            _,gr,gz=core.interpolate(p,shapes);val,dr,dz=core.interpolate(y,shapes)
            dot=np.sum(vv*val,axis=1);hy=np.sum(t[:,None]*val*val,axis=1)+2*a*dot*dot
            by=2*np.sqrt(self.w)[:,None,None]*(gr*val[:,0]+gz*val[:,1])
            extra=ell**2*(np.sum(dr*dr+dz*dz,axis=1)+val[:,0]**2/rr**2)
            value+=float(np.sum(vol*(gr*gr+gz*gz)))
            value+=float(np.sum(vol*(hy-by+extra)))
        return value

    def errors(self,b,y,ell):
        residual=b-self.apply(y,ell)
        unresolved=float(np.sum(residual*residual/self.mass[None]))/((2-math.sqrt(3))/4)
        raw=abs(float(np.sum(y*residual)))+unresolved
        rows=[]
        for j in range(32):
            den=float(np.linalg.norm(b[j]));num=float(np.linalg.norm(residual[j]))
            rows.append(0. if den==0 and num==0 else None if den==0 else finite(num/den))
        return finite(unresolved),finite(raw),rows

def pressure_coefficient(psi,ep,fixed):
    # Literal core.Model initialization and P(X) curvature, without its source assembly.
    norm=1/ep-math.log1p(1/ep);A=1.5*fixed['OA']/fixed['rG']
    target=.5*ep*norm*fixed['d0'];s=target
    for _ in range(12):
        q=math.sqrt(1+ep*s/(1+s));dq=ep/(2*q*(1+s)**2);s-=(s*q-target)/(q+s*dq)
    u0=ep*s/(1+s);u=u0+(1+u0)*np.expm1(-2*core.B*psi)
    assert np.all(np.isfinite(u)) and np.all(u>0) and np.all(u<ep),'Actual accepted clock domain failed'
    ss=u/(ep-u);q=np.sqrt(1+u);dd=2*q*ss/(ep*norm);W=A*q*dd
    cs=ep*ss/(2+(4+3*ep)*ss+2*(1+ep)*ss*ss)
    D=W/cs;kappa=2*(fixed['Hunit']/core.KPC)**2*core.KPC/(core.C*core.A0)
    return -kappa*core.B*(D+3*W)

def pressure_energy(forms,x,p,ep,fixed):
    pressure_coefficient(x[0],ep,fixed) # Same original nodal-domain requirement.
    value=0.
    for rr,vol,shapes,*_ in forms.quad:
        psi,_,_=core.interpolate(x[0],shapes);direction,_,_=core.interpolate(p,shapes)
        value+=float(np.sum(vol*pressure_coefficient(psi,ep,fixed)*direction*direction))
    return finite(value)

def ratio(n,d,u):
    if n is None or d is None or u is None:return None,'nonfinite_quantity'
    if d<=u:return None,'denominator_not_resolved'
    out=finite(n/d);return out,None if out is not None else 'nonfinite_ratio'

def save_direction(name,index,p,y0,ye,row):
    raw=encode(row);path=BASE/f'{STEM}_{name}_D{index}.npz'
    with path.open('xb') as f:
        np.savez_compressed(f,scalar_direction=p,native_response_noell=y0,native_response_ell=ye,metadata=raw.decode())
        f.flush();os.fsync(f.fileno())
    path.chmod(0o444);h=sha(path)
    cp=path.name+'.commit.json';ch=publish(cp,dict(file=path.name,sha256=h,owner='root',pid=os.getpid(),payload=row))
    assert sha(path)==h and sha(BASE/cp)==ch
    actual=json.loads((BASE/cp).read_text());assert actual['payload']==row and actual['sha256']==h
    with np.load(path,allow_pickle=False) as saved:
        assert np.array_equal(saved['scalar_direction'],p,equal_nan=True)
        assert np.array_equal(saved['native_response_noell'],y0,equal_nan=True)
        assert np.array_equal(saved['native_response_ell'],ye,equal_nan=True)
        assert json.loads(str(saved['metadata']))==row
    return dict(file=path.name,sha256=h,commit=cp,commit_sha256=ch)

def direction(forms,x,p,name,index,ep,fixed,identity):
    scale=float(np.max(abs(p)))
    if not math.isfinite(scale) or scale<=0:
        row=dict(case=name,direction=index,status='ZERO_OR_NONFINITE_DIRECTION_REFUSED',normalization=finite(scale),
                 controls=[],passed=False,identity=identity)
        seal=save_direction(name,index,p,np.zeros(forms.shape),np.zeros(forms.shape),row)
        return dict(row,output=seal)
    p=p/scale;b,K,L,Q= forms.load(p)
    if not math.isfinite(K) or K<=0:
        row=dict(case=name,direction=index,status='NONPOSITIVE_GRADIENT_DIRECTION_REFUSED',normalization=scale,
                 K=finite(K),controls=[],passed=False,identity=identity)
        seal=save_direction(name,index,p,np.zeros(forms.shape),np.zeros(forms.shape),row)
        return dict(row,output=seal)
    y0,c0=pcg(lambda y:forms.apply(y,0.),b,forms.diag0)
    ye,ce=pcg(lambda y:forms.apply(y,core.ELL),b,forms.diage)
    # Seal raw partials before any derived floating diagnostics on a failed solve.
    partial=None
    if not c0['ok'] or not ce['ok']:
        raw=dict(case=name,direction=index,status='RAW_SOLVE_FAILURE_RETAINED',identity=identity,solves=[c0,ce])
        path=BASE/f'{STEM}_{name}_D{index}_PARTIAL.npz';meta=encode(raw).decode()
        with path.open('xb') as f:
            np.savez_compressed(f,scalar_direction=p,native_response_noell=y0,native_response_ell=ye,metadata=meta)
            f.flush();os.fsync(f.fileno())
        path.chmod(0o444);partial=dict(file=path.name,sha256=sha(path))
        cp=path.name+'.commit.json'
        partial['commit']=cp
        partial['commit_sha256']=publish(cp,dict(file=path.name,sha256=partial['sha256'],
                                              owner='root',pid=os.getpid(),payload=raw))
    E0=finite(float(np.sum(b*y0)));Ee=finite(float(np.sum(b*ye)))
    d0=finite(forms.direct(p,y0,0.)) if np.all(np.isfinite(y0)) else None
    de=finite(forms.direct(p,ye,core.ELL)) if np.all(np.isfinite(ye)) else None
    u0,e0,m0=forms.errors(b,y0,0.) if np.all(np.isfinite(y0)) else (None,None,[None]*32)
    ue,ee,me=forms.errors(b,ye,core.ELL) if np.all(np.isfinite(ye)) else (None,None,[None]*32)
    space=None if E0 is None else finite(L-E0)
    ell=None if E0 is None or Ee is None else finite(E0-Ee)
    eu=None if e0 is None or ee is None else finite(e0+ee)
    weight=finite((1-float(np.sum(forms.w)))*K);allowance=1e-8*K
    pressure=pressure_energy(forms,x,p,ep,fixed)
    native=None if Ee is None else finite(K-Ee)
    total=None if native is None or pressure is None else finite(native+pressure)
    values=[space,ell,native,Q,L,weight]
    split=None if any(v is None for v in values) else finite(space+ell+Q+weight)
    errors=[finite(abs(L+Q-float(np.sum(forms.w))*K)/K),
            None if d0 is None or E0 is None else finite(abs(d0-(K-E0))/K),
            None if de is None or native is None else finite(abs(de-native)/K),
            None if split is None or native is None else finite(abs(split-native)/K)]
    controls=[dict(name='positive_noell_true_solve',passed=c0['ok']),dict(name='positive_ell_true_solve',passed=ce['ok'])]
    for label,error in zip(('local_quadratic_partition','direct_noell_schur','direct_ell_schur','full_split'),errors):
        controls.append(dict(name=label,error=error,passed=error is not None and error<=1e-8))
    controls.extend([dict(name='space_nonnegativity',passed=space is not None and e0 is not None and space>=-e0-allowance),
                     dict(name='ell_nonnegativity',passed=ell is not None and eu is not None and ell>=-eu-allowance)])
    den=None if ell is None else finite(Q+ell)
    ru=None if eu is None else finite(eu+allowance)
    relative,why=ratio(space,den,ru)
    row=dict(case=name,direction=index,status='DIAGNOSTIC_ONLY',normalization=scale,identity=identity,
             K=K,weighted_local_inverse=finite(L),Q_quartic=finite(Q),Q_space=space,Q_ell=ell,Q_weight=weight,
             pressure=pressure,native_schur=native,total_schur=total,weight_sum=float(np.sum(forms.w)),
             projection_to_quartic_plus_ell=relative,ratio_reason=why,numerical_allowance=allowance,
             direct_energies=[d0,de],unresolved_energy_bounds=[u0,ue],raw_energy_uncertainties=[e0,ee],
             space_uncertainty=e0,ell_uncertainty=eu,mode_true_residuals=[m0,me],solves=[c0,ce],
             controls=controls,passed=all(c['passed'] for c in controls),partial=partial,
             force_bias_qualified=False,continuum_qualified=False,physical_state_qualified=False)
    seal=save_direction(name,index,p,y0,ye,row)
    return dict(row,output=seal)

def main():
    global np,core
    auth()
    assert not list(BASE.glob(STEM+'_*.json')) and not list(BASE.glob(STEM+'_*.npz')),'Existing diagnostic preserved'
    np=importlib.import_module('numpy');core=importlib.import_module('cross_u_ngc3198_nonlinear_disk_v001')
    core.authenticate();assert core.PINS==CORE_INPUT_PINS and core.ELL==.1 and core.C==1.98
    source=sha(__file__);receipt=closed_receipt(PARENT+'_RECEIPT.json',PINS[PARENT+'_RECEIPT.json'])
    assert receipt['source_sha256']==PINS['cross_u_ngc3198_minres_recovery_v003.py']
    assert receipt['result_sha256']==PINS[PARENT+'_RESULT.json']
    parent=json.loads((BASE/(PARENT+'_RESULT.json')).read_text());native_tree(parent)
    assert len(parent['cases'])==16 and len({c['identity']['case'] for c in parent['cases']})==16
    original=json.loads((BASE/'CROSS_U_NGC3198_NONLINEAR_DISK_V001_RESULT.json').read_text());fixed=original['manifest']['fixed']
    assert original['manifest']['grid']==dict(refine=1,extent_kpc=128,positive_modes=32)
    manifest=dict(owner='root',pid=os.getpid(),started=now(),source_sha256=source,input_sha256=inputs(),
                  inherited_input_sha256=core.PINS,state_bindings=STATE_BINDINGS,cases=CASES,
                  directions=['terminal_psi','last_accepted_scalar_increment'],physics_changes=[],
                  no_automatic_resume=True,parent_cases_preserved=parent['cases'],physical_flags_unchanged=True)
    mh=publish(STEM+'_MANIFEST.json',manifest);cases=[]
    for name in CASES:
        x,previous,i,case=paired_states(name,parent)
        r=np.array(i['r_kpc']);z=np.array(i['z_kpc'])
        assert list(x.shape)==i['grid_shape']==[65,len(r),len(z)]
        assert np.all(np.diff(r)>0) and np.all(np.diff(z)>0)
        expected_r,expected_z=core.edges(1,128)
        assert np.array_equal(r,expected_r) and np.array_equal(z,expected_z)
        forms=NativeForms(x,r,z)
        assert np.all(x[0,-1,:]==0) and np.all(x[0,:,-1]==0)
        previous_native=np.stack([previous[1::2],previous[2::2]],axis=1)
        assert previous_native.shape==forms.shape and np.all(previous_native[:,~forms.mask]==0)
        assert np.all(previous[0,-1,:]==0) and np.all(previous[0,:,-1]==0)
        ident=dict(parent_identity=i,parent_status=case['status'],parent_numerical_residual=case['numerical_residual'],
                   manifest_sha256=mh,source_sha256=source,state_bindings=STATE_BINDINGS[name])
        rows=[direction(forms,x,x[0].copy(),name,1,i['eps'],fixed,ident),
              direction(forms,x,x[0]-previous[0],name,2,i['eps'],fixed,ident)]
        result=dict(case=name,parent_case=case,directions=rows,physical_flags_unchanged=True)
        publish(f'{STEM}_{name}_CASE.json',result);cases.append(result)
    auth();assert sha(__file__)==source
    for filename,(receipt_hash,closed) in RECEIPTS.items():
        assert sha(BASE/filename)==receipt_hash
        for output,h in closed['output_sha256'].items():assert sha(BASE/output)==h,('changed closed output at publication',output)
    for case in cases:
        for row in case['directions']:
            seal=row['output'];assert sha(BASE/seal['file'])==seal['sha256'] and sha(BASE/seal['commit'])==seal['commit_sha256']
            cp=json.loads((BASE/seal['commit']).read_text());assert cp['payload']=={k:v for k,v in row.items() if k!='output'}
            if row.get('partial') is not None:
                part=row['partial']
                assert sha(BASE/part['file'])==part['sha256'] and sha(BASE/part['commit'])==part['commit_sha256']
    controls=[t for case in cases for row in case['directions'] for t in row['controls']]
    passed=len(controls)==48 and all(t['passed'] for t in controls)
    result=dict(status='ARITHMETIC_DIAGNOSTIC_CLOSED' if passed else 'FAILURES_OR_REFUSALS_RETAINED',manifest=manifest,
                cases=cases,controls=controls,all_parent_cases=parent['cases'],all_parent_flags_unchanged=True,
                observational_prediction=False,force_bias_qualified=False,continuum_qualified=False,
                physical_state_qualified=False,joint_superiority_qualified=False)
    rh=publish(STEM+'_RESULT.json',result)
    outputs={p.name:sha(p) for p in BASE.glob(STEM+'_*') if p.is_file()}
    publish(STEM+'_RECEIPT.json',dict(owner='root',pid=os.getpid(),source_sha256=source,
            started=manifest['started'],closed=now(),manifest_sha256=mh,result_sha256=rh,output_sha256=outputs))
    print('NONZERO_NATIVE_SPLIT_CLOSED',result['status'],flush=True)
    return 0 if passed else 3

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root-owned',action='store_true');assert ap.parse_args().root_owned
    raise SystemExit(main())

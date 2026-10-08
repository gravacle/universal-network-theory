"""Guarded compact known-piece spatial metric residual; root alone evaluates."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,ast,hashlib,json,math,mmap,os,re,struct,traceback,zipfile
AUTHOR_DRAFT=True
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_SAVED_EVEN_SPATIAL_METRIC_COMPACT_RESIDUAL_V001'
PARENT='CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001'
ORIGINAL='CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001'
PROTOCOL_SHA='da3051772d5472b110f56a85539fa3251c1b047913e8777236c30879665fc81a'
PINS={'CROSS_U_EVEN_SPATIAL_METRIC_WEAK_RESIDUAL_AND_COMPATIBILITY_V001.md': '9cc67c01fd4d9227e80514fed699ef92e57d917723015fb7e51b58e3f7301451', 'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md': 'e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0', 'CROSS_U_STATIC_HILBERT_STRESS_AND_LEADING_LENSING_INTERFACE_V001.md': '6844c982d0c017350d85731f3f58bf8b4167c860ee52f8bdd238ceef1fdcd68b', 'CROSS_U_CONFORMAL_COLD_CIRCULAR_NEXT_ORDER_SOURCE_CLOSURE_V001.md': 'f8365d7bff3f420efe7d30746fd8fe3983a88e62dda1442c00ad73329e087979', 'CROSS_U_STATIONARY_AZIMUTHAL_SHIFT_AND_NATIVE_RESPONSE_V001.md': '048b224899adf28c6924fa02c06a2e2d42fced7f086a139ed8a6981e0dc20fe2', 'cross_u_ngc3198_nonlinear_disk_v001.py': 'ae4285fc9c19cdf2d8efa176ac3d770b7eaf379a75fa3b9627bc9d3f6f3179e1', 'cross_u_ngc3198_conditional_odd_sector_v001.py': '508c379f4bd287435b406567f772fb14efdb7142ca17b18ef0d3e4e74736b394', 'cross_u_ngc3198_odd_saved_orbit_readout_v001.py': '37e33628b371ce4302d6a76468803254fc24b10a503d22bcc8a9a58aa4577320', 'cross_u_ngc3198_odd_banded_correction_v001.py': 'a22931b8f9b8a0a1cca663a459892c634b0f484791a61495567bff33f14bc913', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001.md': '0f7b501037a0f0e65359435825b9d48f49d1249efc6c39a4549e285bdf88423b', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_RECEIPT.json': '41a22374c9747d5b64bf4894290433af8a2cdb92f345f64f6de89f8cc175ea0f', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_RESULT.json': 'fc54d032172c901d288d7f845c077b7f4114199183190e3c0b7eb2c8a1420e85', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_SIGMA_0.1_CASE.json': 'b8ecde6df9e4daac214bf4a4200c5dc58fe14bbc3463c89018ab5902a90d95aa', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_SIGMA_1.0_CASE.json': '52dad743a6b59ebbccde58b68d7d3a97d2fb4cb3ef530be53ab9f2d0cc0b223c', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_SIGMA_10.0_CASE.json': 'aa5b0fee3b9cb5bf7d3c7340d7039634b01d8df175bb4be75a4fe7391627b765', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_SIGMA_100.0_CASE.json': '95dd179d7107594ba22b063ee486ae76ceade3c1d689fd9cfe19986f0533346f'}
SIGMAS=(.1,1.,10.,100.);C=1.98;KB=2-C;ELL=.1;GC=3*math.pi/8
B=1.0059833281731022e-10*3.085677581491367e19/299792458.**2
ARITH_TOL=2e-11;TRUE_TOL=1e-10
BOXES=((2.,16.,16.),(16.,48.,16.))
METRICS=('meridional_difference','meridional_shear','angular_difference')
np=None;OWNER=None;INPUTS={};CREATED={};RECORDS=[];RAW={};CONTEXT={};CHECKS=[]
PARENT_FLAGS={k:False for k in ('physical_temporal_spectrum_qualified','physical_exterior_qualified',
 'full_even_metric_qualified','full_stationary_state_qualified','stability_qualified',
 'source_feedback_qualified','formation_qualified','orbital_force_qualified',
 'observational_qualified','joint_model_adopted')}
FLAGS=dict(PARENT_FLAGS,full_background_subtraction_qualified=False,spatial_inverse_qualified=False,
 physical_constitutive_normalization_qualified=False)
def now():return datetime.now(timezone.utc).isoformat()

def path(n):
    p=Path(n);return p if p.is_absolute() else BASE/p

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def finite(x):return float(x) if math.isfinite(float(x)) else None

def canonical(v):
    if isinstance(v,dict):return {str(k):canonical(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [canonical(x) for x in v]
    if np is not None and isinstance(v,np.generic):return canonical(v.item())
    if v is None or type(v) in (str,bool,int):return v
    if type(v) is float:assert math.isfinite(v);return v
    raise TypeError(type(v).__name__)

def encode(v):return (json.dumps(canonical(v),sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()

def publish(name,raw):
    p=BASE/name
    with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    p.chmod(0o444);CREATED[name]=sha(p);assert p.read_bytes()==raw
    return CREATED[name]

def json_file(name,v):return publish(name,encode(v))

def seal_created():
    for p in BASE.glob(STEM+'_*'):
        if p.is_file():p.chmod(0o555 if p.suffix=='.exe' else 0o444);CREATED[p.name]=sha(p)

def selected_json(filename,wanted):
    """Scoped mmap field selection: never DOM-parse inherited huge JSON objects."""
    wanted=set(wanted);out={};token=re.compile(rb'[{}\[\]"]');quoted=re.compile(rb'"(?:[^"\\]|\\.)*"');ws=re.compile(rb'\s*');end=re.compile(rb'[,}\]]')
    with path(filename).open('rb') as f,mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ) as data:
        def space(p):return ws.match(data,p).end()
        def skip(p):
            p=space(p);ch=data[p:p+1]
            if ch==b'"':return quoted.match(data,p).end()
            if ch not in (b'{',b'['):return end.search(data,p).start()
            depth=1;q=p+1
            while depth:
                m=token.search(data,q);assert m is not None
                q=m.end();t=m.group()
                if t==b'"':q=quoted.match(data,m.start()).end()
                elif t in (b'{',b'['):depth+=1
                else:depth-=1
            return q
        def visit(p,key):
            p=space(p)
            if key in wanted:
                q=skip(p);out[key]=json.loads(data[p:q]);return q
            if not any(k[:len(key)]==key for k in wanted):return skip(p)
            assert data[p:p+1]==b'{';p=space(p+1)
            while data[p:p+1]!=b'}':
                m=quoted.match(data,p);assert m is not None
                k=json.loads(m.group());p=space(m.end());assert data[p:p+1]==b':'
                p=space(visit(p+1,key+(k,)))
                if data[p:p+1]==b',':p=space(p+1)
                else:assert data[p:p+1]==b'}'
            return p+1
        visit(0,());assert set(out)==wanted,('Missing selected custody field',filename,wanted-set(out))
    return out

def checkpoint(tag,arrays,meta):
    md=canonical(dict(meta,owner=OWNER,qualification=FLAGS,
        schema={k:dict(shape=list(v.shape),dtype=str(v.dtype),finite=bool(np.all(np.isfinite(v)))) for k,v in arrays.items()}))
    text=encode(md).decode();md=json.loads(text);p=BASE/f'{STEM}_{len(RECORDS):05d}_{tag}.npz'
    with p.open('xb') as f:np.savez_compressed(f,metadata=text,**arrays);f.flush();os.fsync(f.fileno())
    p.chmod(0o444);CREATED[p.name]=sha(p)
    rec=dict(file=p.name,sha256=CREATED[p.name],metadata=md)
    ch=json_file(p.name+'.COMMIT.json',rec);rec=dict(rec,commit_file=p.name+'.COMMIT.json',commit_sha256=ch);RECORDS.append(rec)
    with np.load(p,allow_pickle=False) as z:
        assert str(z['metadata'])==text and set(z.files)==set(arrays)|{'metadata'}
        for k,v in arrays.items():assert np.array_equal(z[k],v,equal_nan=True)
    return rec

def load_arrays(rec,names):
    with zipfile.ZipFile(path(rec['file'])) as zz,zz.open('metadata.npy') as f:
        magic=f.read(8);assert magic[:6]==b'\x93NUMPY' and magic[6:]==b'\x01\x00'
        h=ast.literal_eval(f.read(struct.unpack('<H',f.read(2))[0]).decode())
        assert h['shape']==() and not h['fortran_order'] and h['descr'].startswith('<U')
    out={}
    with np.load(path(rec['file']),allow_pickle=False) as z:
        assert set(z.files)==set(rec['metadata']['schema'])|{'metadata'}
        for n in names:
            v=z[n].copy();RAW['loaded_'+n]=v
            assert rec['metadata']['schema'][n]==dict(shape=list(v.shape),dtype=str(v.dtype),finite=bool(np.all(np.isfinite(v)))) and np.all(np.isfinite(v))
            out[n]=v
    return out

def original_input():
    file=ORIGINAL+'_00000_INPUT.npz';commit=file+'.COMMIT.json'
    fields={('file',),('sha256',),('metadata','owner'),('metadata','kind'),('metadata','schema')}
    v=selected_json(commit,fields)
    assert v[('file',)]==file and v[('sha256',)]==INPUTS[file] and v[('metadata','owner')]['pid']==86078
    assert v[('metadata','kind')]=='unchanged_authentic_even_state'
    return dict(file=file,sha256=INPUTS[file],commit_file=commit,commit_sha256=INPUTS[commit],metadata=dict(kind=v[('metadata','kind')],owner=v[('metadata','owner')],schema=v[('metadata','schema')]))

def recheck():
    assert sha(__file__)==OWNER['source_sha256']
    for n,h in INPUTS.items():assert sha(path(n))==h,('input seal',n)
    for n,h in CREATED.items():assert sha(BASE/n)==h,('own seal',n)
    if STEM+'_OWNER_START.json' in CREATED:assert json.loads(path(STEM+'_OWNER_START.json').read_text())==OWNER
    for rec in RECORDS:
        assert json.loads(path(rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
        with np.load(path(rec['file']),allow_pickle=False) as z:
            assert json.loads(str(z['metadata']))==rec['metadata'] and set(z.files)==set(rec['metadata']['schema'])|{'metadata'}
            for n,s in rec['metadata']['schema'].items():
                a=z[n];assert s==dict(shape=list(a.shape),dtype=str(a.dtype),finite=bool(np.all(np.isfinite(a))))

def check(name,a,b,tol=ARITH_TOL):
    a=np.asarray(a);b=np.asarray(b);i=len(CHECKS);CONTEXT.update(control=name,control_ordinal=i)
    RAW[f'control_{i:03d}_{name}_actual']=a.copy();RAW[f'control_{i:03d}_{name}_expected']=b.copy();assert a.shape==b.shape
    gap=float(np.linalg.norm(a-b));env=max(1e-30,float(np.linalg.norm(a)),float(np.linalg.norm(b)));e=gap/env
    row=dict(name=name,error=finite(e),absolute_gap=finite(gap),envelope=finite(env),tolerance=tol,passed=math.isfinite(e) and e<=tol);CHECKS.append(row);return row

def inputs_and_parent():
    pins=dict(PINS,**{STEM+'.md':PROTOCOL_SHA})
    for n,h in pins.items():assert type(h) is str and len(h)==64 and sha(path(n))==h,('direct seal',n)
    rc=json.loads(path(PARENT+'_RECEIPT.json').read_text())
    assert rc['status']=='CLOSED' and rc['owner']['owner']=='root' and rc['owner']['pid']==88234
    assert rc['closed']>rc['owner']['started'] and rc['qualification']==PARENT_FLAGS
    assert rc['result_sha256']==pins[PARENT+'_RESULT.json'] and rc['owner']['source_sha256']==pins['cross_u_ngc3198_odd_banded_correction_v001.py']
    for n,h in dict(rc['input_sha256'],**rc['output_sha256']).items():assert n not in pins or pins[n]==h;pins[n]=h
    for n in list(pins):
        if n.endswith('_RECEIPT.json'):
            rr=json.loads(path(n).read_text())
            for f,h in rr.get('output_sha256',{}).items():assert f not in pins or pins[f]==h;pins[f]=h
    for n,h in pins.items():assert sha(path(n))==h,('complete inherited seal',n)
    assert path(PARENT+'_RESULT.json').stat().st_size<=16*1024*1024
    result=json.loads(path(PARENT+'_RESULT.json').read_text())
    assert result['owner']==rc['owner'] and result['qualification']==PARENT_FLAGS
    assert [c['sigma'] for c in result['cases']]==list(SIGMAS) and len(result['controls'])==22 and all(c['passed'] for c in result['controls'])
    assert len(result['copied_parent_controls'])==21 and len(result['copied_parent_cases'])==4
    for rec in result['checkpoints']:
        assert pins[rec['file']]==rec['sha256'] and pins[rec['commit_file']]==rec['commit_sha256']
        assert json.loads(path(rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
        assert rec['metadata']['owner']==rc['owner']
    for c in result['cases']:
        assert json.loads(path(PARENT+'_SIGMA_'+str(c['sigma'])+'_CASE.json').read_text())==c
        assert c['status']=='LINEAR_PASS' and c['INFO']==0 and c['original_residual']<=TRUE_TOL
        assert c['final_checkpoint'] in result['checkpoints'] and c['assembly_checkpoint'] in result['checkpoints']
    return pins,result

def old_pair(file,kind):
    fields={('file',),('sha256',),('metadata','owner'),('metadata','kind'),('metadata','schema')}
    v=selected_json(file+'.COMMIT.json',fields)
    assert v[('file',)]==file and v[('sha256',)]==INPUTS[file] and v[('metadata','owner')]['pid']==86078 and v[('metadata','kind')]==kind
    return dict(file=file,sha256=INPUTS[file],commit_file=file+'.COMMIT.json',commit_sha256=INPUTS[file+'.COMMIT.json'],metadata=dict(owner=v[('metadata','owner')],kind=kind,schema=v[('metadata','schema')]))

class D:
    """Literal first directional derivative; no finite-difference physical action."""
    def __init__(self,v,d=0.):self.v=np.asarray(v);self.d=np.asarray(d)
    def __add__(self,o):o=asD(o);return D(self.v+o.v,self.d+o.d)
    __radd__=__add__
    def __neg__(self):return D(-self.v,-self.d)
    def __sub__(self,o):return self+-asD(o)
    def __rsub__(self,o):return asD(o)+-self
    def __mul__(self,o):o=asD(o);return D(self.v*o.v,self.d*o.v+self.v*o.d)
    __rmul__=__mul__
    def __truediv__(self,o):o=asD(o);return D(self.v/o.v,(self.d*o.v-self.v*o.d)/(o.v*o.v))
    def __rtruediv__(self,o):return asD(o)/self
    def __getitem__(self,k):return D(self.v[k],np.broadcast_to(self.d,self.v.shape)[k])
def asD(x):return x if isinstance(x,D) else D(x)
def root(x):x=asD(x);v=np.sqrt(x.v);return D(v,x.d/(2*v))
def exp(x):x=asD(x);v=np.exp(x.v);return D(v,v*x.d)
def eins(s,*xs):
    xs=[asD(x) for x in xs];v=np.einsum(s,*[x.v for x in xs]);d=np.zeros_like(v)
    for i,x in enumerate(xs):
        if np.any(x.d):d+=np.einsum(s,*[np.broadcast_to(y.d,y.v.shape) if k==i else y.v for k,y in enumerate(xs)])
    return D(v,d)
def summed(x,axis=None):x=asD(x);return D(np.sum(x.v,axis=axis),np.sum(np.broadcast_to(x.d,x.v.shape),axis=axis))
def diagonal_inverse(h):
    assert np.all(h.v==np.eye(3)*np.diagonal(h.v,axis1=-2,axis2=-1)[...,None,:]) and np.all(np.diagonal(h.v,axis1=-2,axis2=-1)>0)
    hi=np.eye(3)/np.diagonal(h.v,axis1=-2,axis2=-1)[...,None,:]
    return D(hi,-np.einsum('...ia,...ab,...bj->...ij',hi,np.broadcast_to(h.d,h.v.shape),hi))
def connection(hi,dh):
    v=np.zeros(hi.v.shape[:-2]+(3,3,3));d=np.zeros_like(v)
    for k in range(3):
        for i in range(3):
            for j in range(3):
                s=sum(hi[...,k,l]*(dh[...,i,j,l]+dh[...,j,i,l]-dh[...,l,i,j])/2 for l in range(3))
                v[...,k,i,j]=s.v;d[...,k,i,j]=s.d
    return D(v,d)
def dot(hi,x,y):return eins('...ab,...a,...b->...',hi,x,y)
def mode_dot(hi,x,y):return eins('...ab,j...a,j...b->j...',hi,x,y)
def transform(hi,x):return eins('...ab,j...b->j...a',hi,x)

def clock(phi,fixed):
    ep=1e-5;norm=1/ep-math.log1p(1/ep);A=1.5*fixed['OA']/fixed['rG'];target=.5*ep*norm*fixed['d0'];s0=target
    for _ in range(12):
        q=math.sqrt(1+ep*s0/(1+s0));dq=ep/(2*q*(1+s0)**2);s0-=(s0*q-target)/(q+s0*dq)
    u0=ep*s0/(1+s0);u=u0+(1+u0)*np.expm1(-2*phi.v);RAW['current_clock_u']=u
    assert np.all(np.isfinite(u)) and np.all((u>0)&(u<ep))
    s=u/(ep-u);q=np.sqrt(1+u);pe=(np.log1p(s)-s/(1+s))/norm;dd=2*q*s/(ep*norm)
    eta=fixed['Hunit']/(1000*299792458.);fac=2*eta*eta/C
    P=fac*A*(pe-1);W=fac*A*q*dd;Q=fixed['Q0_over_Hstar']*eta*q
    return D(P,-W*phi.d),D(Q,-Q*phi.d)

def background_data(rr,zz,volume,x,odd,shapes,xi,w,fixed,omega):
    val,gr,gz=interpolate(x,shapes);ov,orr,oz=interpolate(odd,shapes)
    cells=val.shape[1:];phi=B*val[0];a=np.zeros(cells+(3,));a[...,0]=B*gr[0];a[...,1]=B*gz[0]
    h=np.exp(-2*phi)[...,None,None]*np.eye(3);dh=np.zeros(cells+(3,3,3))
    for k in (0,1):dh[...,k,:,:]=-2*a[...,k,None,None]*h
    z=np.zeros((32,)+cells+(3,));z[...,0]=B*val[1::2]/np.sqrt(w)[:,None,None];z[...,1]=B*val[2::2]/np.sqrt(w)[:,None,None]
    dz=np.zeros((32,)+cells+(3,3));dz[...,0,0]=B*gr[1::2]/np.sqrt(w)[:,None,None];dz[...,0,1]=B*gr[2::2]/np.sqrt(w)[:,None,None]
    dz[...,1,0]=B*gz[1::2]/np.sqrt(w)[:,None,None];dz[...,1,1]=B*gz[2::2]/np.sqrt(w)[:,None,None];dz[...,2,2]=z[...,0]/rr
    gb=np.zeros_like(a);gb[...,0]=orr[0];gb[...,1]=oz[0];gc=np.zeros_like(a);gc[...,0]=orr[1];gc[...,1]=oz[1]
    return dict(rr=np.broadcast_to(rr,cells),zz=np.broadcast_to(zz,cells),volume=volume,phi=phi,N=np.exp(phi),a=a,h=h,dh=dh,z=z,dz=dz,beta=ov[0],gbeta=gb,chi=ov[1],gchi=gc,xi=xi,w=w,fixed=fixed,omega=omega)

def direction(data,**kw):
    out={k:np.zeros_like(data[k]) for k in ('phi','N','a','h','dh','z','dz','beta','gbeta','chi','gchi')};out.update(kw);return out

def functional(data,di):
    for key in di:
        RAW['current_'+key+'_primal']=data[key].copy();RAW['current_'+key+'_tangent']=di[key].copy()
    d={k:D(data[k],di[k]) for k in di};phi,N,a,h,dh,z,dz,beta,gb,chi,gchi=(d[k] for k in ('phi','N','a','h','dh','z','dz','beta','gbeta','chi','gchi'))
    hi=diagonal_inverse(h);det=np.prod(np.diagonal(h.v,axis1=-2,axis2=-1),axis=-1)
    sr=D(np.sqrt(det),np.sqrt(det)*np.einsum('...ij,...ji->...',hi.v,h.d)/2);m=N*sr
    gam=connection(hi,dh);RAW['current_connection']=gam.v.copy();RAW['current_connection_tangent']=gam.d.copy();V=m[...,None,None]*hi
    dhinv=-eins('...ia,...kab,...bj->...kij',hi,dh,hi)
    lm=a+eins('...ij,...kji->...k',hi,dh)/2
    DV=m[...,None,None,None]*(lm[..., :,None,None]*hi[...,None,:,:]+dhinv)
    tr=eins('...kik->...i',gam)
    AA=eins('...l,...lij->...ij',tr,gam)-eins('...kjl,...lik->...ij',gam,gam)
    IG=-eins('...kij,...kij->...',DV,gam)+eins('...jij,...i->...',DV,tr)+eins('...ij,...ij->...',V,AA)
    rho=data['rr']*root(h[...,2,2]);b_v=np.zeros_like(data['a']);b_d=np.zeros_like(b_v)
    for k in (0,1):
        v=dh[...,k,2,2]/(2*h[...,2,2]);b_v[...,k]=v.v;b_d[...,k]=v.d
    b_v[...,0]+=1/data['rr'];b=D(b_v,b_d);rel=b-a;t=rho[...,None]/N[...,None]*gb
    G=dz-eins('...kij,p...k->p...ij',gam,z)
    zn=mode_dot(hi,z,z);an=dot(hi,a,a);az=eins('...ab,...a,j...b->j...',hi,a,z)
    gg=eins('...ac,...bd,j...ab,j...cd->j...',hi,hi,G,G)
    w=data['w'][:,None,None];kj=(B*GC)**2*data['xi'][:,None,None]**4
    P,Q=clock(phi,data['fixed']);alpha=KB/C
    terms={'gravity':IG/(2*C),'gravity_shift':m*dot(hi,t,t)/(4*C),'maxwell_even':m*alpha*an/2,'phase_even':m*P}
    native_even=m[None,...]*w*(-zn/2-zn*zn/(4*kj)-ELL**2*gg/2+az)
    terms['native_even']=summed(native_even,axis=0)
    wc=gchi+chi[...,None]*rel
    terms['odd_maxwell_magnetic']=-m*alpha*dot(hi,wc,wc)/2
    terms['odd_maxwell_chi2']=-m*alpha*chi*chi*dot(hi,a,rel)
    terms['odd_maxwell_cross']=-m*alpha*chi*dot(hi,a,t)
    terms['odd_phase']=-m*Q*Q*chi*chi/2
    dzrel=eins('...ab,...a,j...b->j...',hi,rel,z);bz=eins('...ab,...a,j...b->j...',hi,b,z);tz=eins('...ab,...a,j...b->j...',hi,t,z)
    vv=chi[None,...]*dzrel+tz/2
    modal={'native_even':native_even,
        'odd_native_chi2':-m[None,...]*w*chi[None,...]*chi[None,...]*dzrel,
        'odd_native_cross':-m[None,...]*w*chi[None,...]*tz,
        'odd_native_inertia':m[None,...]*w*vv*vv/(2*data['omega'][:,None,None]**2),
        'odd_native_gradient':-m[None,...]*w*ELL**2*bz*(chi[None,...]*chi[None,...]*dzrel+chi[None,...]*tz)}
    for k in modal:
        if k!='native_even':terms[k]=summed(modal[k],axis=0)
    assert all(np.all(np.isfinite(t.v)) and np.all(np.isfinite(t.d)) for t in terms.values()),'Nonfinite first-derivative action; raw inputs retained.'
    return terms,modal,dict(hi=hi.v,gamma=gam.v,G=G.v,m=m.v,P=P.v,Q=Q.v,zn=zn.v,gg=gg.v,az=az.v)

def compact(R,Z,box):
    lo,hi,top=box;mid=(lo+hi)/2;scale=(hi-lo)/2;x=(R-mid)/scale;y=Z/top
    inside=(abs(x)<1)&(y>=0)&(y<1);ar=1-x*x;az=1-y*y
    v=np.where(inside,ar**3*az**3,0.);dr=np.where(inside,-6*x/scale*ar**2*az**3,0.);dz=np.where(inside,-6*y/top*az**2*ar**3,0.)
    return v,dr,dz

def metric_direction(data,box,kind):
    v,vr,vz=compact(data['rr'],data['zz'],box);S=np.zeros((3,3))
    if kind==0:S[0,0]=1;S[1,1]=-1
    elif kind==1:
        vr,vz=vr*data['zz']/box[2],vz*data['zz']/box[2]+v/box[2];v=v*data['zz']/box[2];S[0,1]=S[1,0]=1
    else:S[0,0]=S[1,1]=-.5;S[2,2]=1
    f=data['h'][...,0,0];q=f[...,None,None]*v[...,None,None]*S;dq=np.zeros(data['dh'].shape)
    for k,vk in enumerate((vr,vz)):
        dq[...,k,:,:]=f[...,None,None]*(vk[...,None,None]-2*data['a'][...,k,None,None]*v[...,None,None])*S
    Om=np.zeros(data['h'].shape);Om[...,2,0]=1/data['rr'];Om[...,0,2]=-1/data['rr']
    dq[...,2,:,:]=-np.einsum('...li,...lj->...ij',Om,q)-np.einsum('...il,...lj->...ij',q,Om)
    hi=np.eye(3)/f[...,None,None];di=direction(data,h=q,dh=dq)
    eta=np.einsum('...ij,...jk,p...k->p...i',q,hi,data['z'])
    dhi=-np.einsum('...ia,...kab,...bj->...kij',hi,data['dh'],hi)
    deta=np.einsum('...aij,...jk,p...k->p...ai',dq,hi,data['z'])+np.einsum('...ij,...ajk,p...k->p...ai',q,dhi,data['z'])+np.einsum('...ij,...jk,p...ak->p...ai',q,hi,data['dz'])
    lam=.5*S[2,2]*v;gl=np.zeros(data['a'].shape);gl[...,0]=.5*S[2,2]*vr;gl[...,1]=.5*S[2,2]*vz
    uc=data['chi']*lam;guc=data['gchi']*lam[...,None]+data['chi'][...,None]*gl
    return di,direction(data,z=eta,dz=deta),direction(data,chi=uc,gchi=guc),lam

def totals(terms,volume,derivative=True):return np.array([np.sum(volume*(v.d if derivative else v.v)) for v in terms.values()])

def literal_seven(terms,volume):
    names=('gravity_shift','odd_maxwell_magnetic','odd_maxwell_chi2','odd_maxwell_cross','odd_phase','odd_native_inertia','odd_native_gradient')
    out=totals({k:terms[k] for k in names},volume,False)
    out[2]+=float(np.sum(volume*terms['odd_native_chi2'].v));out[3]+=float(np.sum(volume*terms['odd_native_cross'].v));return out

def independent_even_tensor(data,di):
    zero=direction(data);terms,modal,p=functional(data,zero);hi=p['hi'];G=p['G'];gam=p['gamma'];z=data['z'];a=data['a'];q=di['h'];dq=di['dh'];w=data['w'][:,None,None];zn=p['zn'];kj=(B*GC)**2*data['xi'][:,None,None]**4
    qr=np.einsum('...ia,...ab,...bj->...ij',hi,q,hi);dhi=-np.einsum('...ia,...kab,...bj->...kij',hi,data['dh'],hi)
    dqr=np.einsum('...kia,...ab,...bj->...kij',dhi,q,hi)+np.einsum('...ia,...kab,...bj->...kij',hi,dq,hi)+np.einsum('...ia,...ab,...kbj->...kij',hi,q,dhi)
    Dqr=dqr+np.einsum('...ikl,...lj->...kij',gam,qr)+np.einsum('...jkl,...il->...kij',gam,qr)
    m=p['m'];Ln=(KB/C)*np.einsum('...ab,...a,...b->...',hi,a,a)/2+p['P']+np.sum(w*(-zn/2-zn*zn/(4*kj)-ELL**2*p['gg']/2+p['az']),axis=0)
    T=Ln[...,None,None]*data['h']-(KB/C)*a[..., :,None]*a[...,None,:]
    T+=np.sum(w[...,None,None]*((1+zn/kj)[...,None,None]*z[..., :,None]*z[...,None,:]-a[None,...,:,None]*z[...,None,:]-z[..., :,None]*a[None,...,None,:]+ELL**2*(np.einsum('p...ik,...kl,p...jl->p...ij',G,hi,G)+np.einsum('p...ki,...kl,p...lj->p...ij',G,hi,G))),axis=0)
    sy=(G+np.swapaxes(G,-1,-2))/2;zu=np.einsum('...ab,p...b->p...a',hi,z)
    F=zu[..., :,None,None]*sy[...,None,:,:]-z[...,None,:,None]*np.einsum('p...jl,...lk->p...kj',sy,hi)[..., :,None,:]-z[...,None,None,:]*np.einsum('p...il,...lk->p...ki',sy,hi)[..., :, :,None]
    result=m*(np.einsum('...ij,...ij->...',T,qr)-ELL**2*np.sum(w*np.einsum('p...kij,...kij->p...',F,Dqr),axis=0))/2
    return result

def matter(samples,beta,box,kind,normal=False):
    R=samples[:,0];ph=samples[:,2];v0=samples[:,4];rho0=samples[:,6];weight=samples[:,7];N=np.exp(ph);Omega=N*v0/rho0;v=v0+rho0/N*beta
    RAW['current_worldline_Omega']=Omega;RAW['current_worldline_v']=v
    assert np.all(np.isfinite(v)) and np.all(v*v<1),'Held coordinate worldline became nontimelike; no repaired source.'
    gamma=1/np.sqrt(1-v*v);b,_,_=compact(R,np.zeros_like(R),box);lam=(.5*b if kind==2 and not normal else np.zeros_like(b));nu=b if normal else np.zeros_like(b)
    derivative=B*weight*N*gamma*(v*v*lam-nu)
    # Independent variation of -mN sqrt(1-v²) at fixed Omega and beta.
    dv=v*(lam-nu);rootv=np.sqrt(1-v*v);second=-B*weight*N*(nu*rootv-v*dv/rootv)
    return derivative,second,np.stack([R,Omega,beta,v,gamma,lam,nu,derivative,second],axis=1)



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

def interpolate_sheet(r,v,R):
    ix=np.searchsorted(r,R,side='right')-1;assert np.all((ix>=0)&(ix<len(r)-1));t=(R-r[ix])/(r[ix+1]-r[ix]);return (1-t)*v[ix]+t*v[ix+1]

def fixtures():
    diag=np.array([.7,1.2,1.9]);h=np.diag(diag);q=np.array([[.2,.3,0.],[.3,-.1,.4],[0.,.4,.6]])
    hd=D(h,q);iv=diagonal_inverse(hd);check('known_diagonal_inverse_tangent',iv.d,-q/(diag[:,None]*diag[None,:]))
    rootdet=math.sqrt(float(np.prod(diag)));actual=rootdet*np.trace(iv.v@q)/2
    expected=(q[0,0]*diag[1]*diag[2]+q[1,1]*diag[0]*diag[2]+q[2,2]*diag[0]*diag[1])/(2*rootdet)
    check('known_determinant_tangent',np.array(actual),np.array(expected))
    # Pure conformal EH identity at independent Phi/Psi variations, no source/state.
    phi=np.array([[.03]]);aa=np.array([[[.07,-.04,0.]]]);f=np.exp(-2*phi);hh=f[...,None,None]*np.eye(3);dh=np.zeros((1,1,3,3,3))
    for k in (0,1):dh[...,k,:,:]=-2*aa[...,k,None,None]*hh
    data=dict(rr=np.array([[3.]]),zz=np.array([[1.]]),phi=phi,N=np.exp(phi),a=aa,h=hh,dh=dh,z=np.zeros((32,1,1,3)),dz=np.zeros((32,1,1,3,3)),beta=np.zeros((1,1)),gbeta=np.zeros((1,1,3)),chi=np.zeros((1,1)),gchi=np.zeros((1,1,3)),xi=np.linspace(1/64,63/64,32),w=np.ones(32)/32,fixed=dict(OA=.7,rG=.98/.99,d0=.35857141419482286,Hunit=67.49711988577813,Q0_over_Hstar=100.),omega=np.ones(32))
    # Keep fixture phase in its owned domain: use phi=0 only for unrelated clock.
    data['phi']=np.zeros((1,1));data['N']=np.ones((1,1));data['h']=np.eye(3)[None,None];data['dh']=-2*aa[..., :,None,None]*data['h'][...,None,:,:]
    nu=np.array([[.2]]);gn=np.array([[[.1,.05,0.]]]);ps=np.array([[.3]]);gp=np.array([[[-.08,.06,0.]]]);dq=-2*ps[...,None,None]*data['h'];ddq=-2*gp[..., :,None,None]*data['h'][...,None,:,:]-2*ps[...,None,None,None]*data['dh']
    di=direction(data,phi=nu,N=nu,a=gn,h=dq,dh=ddq);t,_,_=functional(data,di)
    expected=np.array([[-np.sum(aa*aa,axis=-1)[0,0]/C,(-(nu-ps)*np.sum(aa*aa,axis=-1)-2*np.sum(aa*gn,axis=-1))[0,0]/C]])
    check('independent_conformal_EH_identity',np.array([[t['gravity'].v[0,0],t['gravity'].d[0,0]]]),expected)
    checkpoint('ARITHMETIC_FIXTURES',dict(RAW),dict(kind='fixed_inverse_determinant_conformal_gravity_controls',controls=list(CHECKS)))

def arm(case,even,source,fixed):
    RAW.clear();CONTEXT.clear();CONTEXT.update(sigma=case['sigma'],stage='closed_arm_admission');begin=len(CHECKS)
    data=load_arrays(case['final_checkpoint'],('physical_beta_chi','original_rhs','original_H_action','original_residual'));odd=data['physical_beta_chi'];assert odd.shape==(2,87,45)
    co=case['assembly_checkpoint']['metadata']['parent_coefficient'];coeff=load_arrays(co,('omega_star','xi','weights','manufactured_y','literal_action_terms'))
    r=even['r_kpc'];z=even['z_kpc'];x=even['final_state'];xi=even['xi'];w=even['weights'];eta=fixed['Hunit']/(1000*299792458.)
    assert np.array_equal(xi,coeff['xi']) and np.array_equal(w,coeff['weights']);check('sigma_'+str(case['sigma'])+'_actual_frequency',coeff['omega_star'],case['sigma']*xi*eta)
    checkpoint('ARM_INPUT',dict(physical_beta_chi=odd,omega_star=coeff['omega_star'],original_rhs=data['original_rhs'],original_H_action=data['original_H_action'],original_residual=data['original_residual'],**{k:v for k,v in RAW.items() if k.startswith('control_')}),dict(kind='unchanged_closed_odd_arm',sigma=case['sigma'],reference=dict(final=case['final_checkpoint']['file'],final_sha256=case['final_checkpoint']['sha256'],coefficient=co['file'],coefficient_sha256=co['sha256']),copied_status=case['status'],copied_original_residual=case['original_residual'],controls=CHECKS[begin:]))
    RAW.clear();quads=shape_quadrature(r,z);terms7=np.zeros(7);manufactured=coeff['manufactured_y'].copy();manufactured[0,0]=manufactured[0,1]
    for rr,vol,sh in quads:
        zz=np.zeros_like(vol)
        for n,nr,nz,i,j in sh:zz+=n*z[None,j:len(z)-1+j]
        bg=background_data(rr,zz,vol,x,manufactured,sh,xi,w,fixed,coeff['omega_star']);ts,_,_=functional(bg,direction(bg));terms7+=literal_seven(ts,vol)
    check('sigma_'+str(case['sigma'])+'_literal_odd_action',terms7,coeff['literal_action_terms'])
    rowsets=[];chain_actual=[];chain_expected=[];saved={};beta_samples=interpolate_sheet(r,odd[0,:,0],source[:,0])
    for ib,box in enumerate(BOXES):
        for kind,name in enumerate(METRICS):
            tag=f'b{ib}_{name}';rows=[];mode_rows=[];chain_rows=[];independent=0.;cov_even=0.
            for iq,(rr,vol,sh) in enumerate(quads):
                zz=np.zeros_like(vol)
                for n,nr,nz,i,j in sh:zz+=n*z[None,j:len(z)-1+j]
                bg=background_data(rr,zz,vol,x,odd,sh,xi,w,fixed,coeff['omega_star']);md,mc,uc,lam=metric_direction(bg,box,kind)
                combined={k:md[k]+mc[k]+uc[k] for k in md}
                runs=[]
                for label,di in (('covector_metric',md),('modal_chain',mc),('U_chain',uc),('held_vector_metric',combined)):
                    CONTEXT.update(stage='compact_metric_derivative',box=ib,metric=name,quadrature=iq,derivative=label)
                    RAW['current_metric_direction']=di['h'];RAW['current_metric_direction_gradient']=di['dh'];RAW['current_mode_direction']=di['z'];RAW['current_mode_direction_gradient']=di['dz'];RAW['current_chi_direction']=di['chi'];RAW['current_chi_direction_gradient']=di['gchi']
                    ts,mods,pr=functional(bg,di);runs.append(totals(ts,vol));saved[f'{tag}_q{iq}_{label}_densities']=np.stack([v.d for v in ts.values()])
                    if label=='modal_chain':mode_rows.append(np.stack([np.sum(vol[None,...]*v.d,axis=(1,2)) for v in mods.values()]))
                    if label=='covector_metric':cov_even+=sum(float(np.sum(vol*ts[k].d)) for k in ('maxwell_even','phase_even','native_even'))
                rows.append(np.stack(runs));chain_actual.append(runs[3]);chain_expected.append(runs[0]+runs[1]+runs[2])
                if case['sigma']==.1:independent+=float(np.sum(vol*independent_even_tensor(bg,md)))
            mat,_,rawmat=matter(source,beta_samples,box,kind);saved[tag+'_worldline_operands']=rawmat
            if case['sigma']==.1:check(tag+'_independent_even_tensor',np.array(cov_even),np.array(independent))
            summed_rows=np.sum(rows,axis=0);saved[tag+'_component_rows']=summed_rows;saved[tag+'_per_mode_chain']=np.sum(mode_rows,axis=0)
            rowsets.append(dict(box=box,metric=name,component_names=list(ts),covector_metric=summed_rows[0].tolist(),modal_chain=summed_rows[1].tolist(),U_chain=summed_rows[2].tolist(),held_vector_metric=summed_rows[3].tolist(),ordinary_sheet=float(np.sum(mat)),known_total=float(np.sum(summed_rows[3])+np.sum(mat)),full_background_contribution=None,exterior_contribution=None,full_metric_qualified=False))
        # Separate compact U, normal and both meridional modal compatibility tests.
        for probe in ('projected_U','normal_covector','normal_compensated','mode_R','mode_Z'):
            totals_probe=[];permode=[]
            for iq,(rr,vol,sh) in enumerate(quads):
                zz=np.zeros_like(vol)
                for n,nr,nz,i,j in sh:zz+=n*z[None,j:len(z)-1+j]
                bg=background_data(rr,zz,vol,x,odd,sh,xi,w,fixed,coeff['omega_star']);v,vr,vz=compact(bg['rr'],bg['zz'],box);grad=np.zeros_like(bg['a']);grad[...,0]=vr;grad[...,1]=vz
                if probe=='projected_U':di=direction(bg,chi=v,gchi=grad)
                elif probe.startswith('normal'):
                    chi=-bg['chi']*v if probe=='normal_compensated' else np.zeros_like(v);gchi=-bg['gchi']*v[...,None]-bg['chi'][...,None]*grad if probe=='normal_compensated' else np.zeros_like(grad)
                    di=direction(bg,phi=v,N=bg['N']*v,a=grad,chi=chi,gchi=gchi)
                else:
                    j=0 if probe=='mode_R' else 1
                    if j==1:vr,vz=vr*bg['zz']/box[2],vz*bg['zz']/box[2]+v/box[2];v=v*bg['zz']/box[2]
                    eta_z=np.zeros_like(bg['z']);eta_dz=np.zeros_like(bg['dz']);scale=B*xi[:,None,None]**2;eta_z[...,j]=scale*v;eta_dz[...,0,j]=scale*vr;eta_dz[...,1,j]=scale*vz
                    if j==0:eta_dz[...,2,2]=eta_z[...,0]/bg['rr']
                    di=direction(bg,z=eta_z,dz=eta_dz)
                CONTEXT.update(stage='separate_compatibility',box=ib,probe=probe,quadrature=iq);ts,mods,_=functional(bg,di);totals_probe.append(totals(ts,vol));saved[f'b{ib}_{probe}_q{iq}_densities']=np.stack([v.d for v in ts.values()]);permode.append(np.stack([np.sum(vol[None,...]*v.d,axis=(1,2)) for v in mods.values()]))
            saved[f'b{ib}_{probe}_components']=np.sum(totals_probe,axis=0);saved[f'b{ib}_{probe}_per_mode']=np.sum(permode,axis=0)
        for normal in (False,True):
            mat,second,rawmat=matter(source,beta_samples,box,2,normal);check(f'sigma_{case["sigma"]}_b{ib}_worldline_'+('normal' if normal else 'angular'),mat,second)
            saved[f'b{ib}_worldline_'+('normal' if normal else 'angular')]=rawmat
    check('sigma_'+str(case['sigma'])+'_off_shell_chain_linearity',np.array(chain_actual),np.array(chain_expected))
    saved.update({k:v for k,v in RAW.items() if k.startswith('control_')});cp=checkpoint('RESIDUAL',saved,dict(kind='known_compact_metric_and_separate_compatibility_residuals',sigma=case['sigma'],rows=rowsets,controls=CHECKS[begin:],unknown_terms=dict(full_background=None,exterior=None,spatial_inverse=None,physical_temporal_mapping=None),reaction_order='same accepted L0+L2, compensated normalized-U and held-vector chains',coordinate_worldlines_fixed=True,source_feedback_solved=False))
    return dict(sigma=case['sigma'],status='KNOWN_PIECES_RECORDED' if all(c['passed'] for c in CHECKS[begin:]) else 'ARITHMETIC_FAILED',checkpoint=cp,rows=rowsets,qualification=FLAGS)

def main():
    global np,OWNER,INPUTS
    ap=argparse.ArgumentParser();ap.add_argument('--root-run',action='store_true');args=ap.parse_args();assert args.root_run and not AUTHOR_DRAFT and type(PROTOCOL_SHA) is str
    assert not list(BASE.glob(STEM+'_*')),'Unused namespace; no automatic replay or resume.'
    INPUTS,parent=inputs_and_parent();OWNER=dict(owner='root',pid=os.getpid(),started=now(),source_sha256=sha(__file__));cases=[]
    try:
        json_file(STEM+'_OWNER_START.json',OWNER);json_file(STEM+'_MANIFEST.json',dict(owner=OWNER,input_sha256=INPUTS,sigmas=SIGMAS,boxes=BOXES,metric_tests=METRICS,known_piece_only=True,qualification=FLAGS))
        import numpy as _np
        np=_np
        rec=original_input();even=load_arrays(rec,('r_kpc','z_kpc','final_state','xi','weights'))
        assert even['r_kpc'].shape==(87,) and even['z_kpc'].shape==(45,) and even['final_state'].shape==(65,87,45)
        assert np.all(np.diff(even['r_kpc'])>0) and np.all(np.diff(even['z_kpc'])>0) and even['r_kpc'][0]==even['z_kpc'][0]==0 and even['r_kpc'][-1]==even['z_kpc'][-1]==128
        fixed=selected_json(rec['commit_file'],{('metadata','parent','source_identity','inherited_fixed')})[('metadata','parent','source_identity','inherited_fixed')]
        assert fixed['rG']==.98/.99 and fixed['Q0_over_Hstar']==100
        sr=old_pair(ORIGINAL+'_00001_CIRCULAR_SOURCE.npz','predicted_circular_source_entire_support');source=load_arrays(sr,('source_samples16','source_samples32'))
        assert source['source_samples16'].shape[1]==source['source_samples32'].shape[1]==9
        checkpoint('INPUT',dict(even,**source),dict(kind='unchanged_saved_even_fields_and_fixed_coordinate_worldline_quadrature',original_input=rec['file'],original_input_sha256=rec['sha256'],source_record=sr['file'],source_record_sha256=sr['sha256'],fixed=fixed,copied_original_controls=parent['copied_parent_controls'],copied_band_controls=parent['controls'],copied_original_failures=parent['copied_parent_cases']))
        RAW.clear();fixtures()
        for case in parent['cases']:cases.append(arm(case,even,source['source_samples16'],fixed))
        assert len(CHECKS)==37 and len(RECORDS)==10
        result=dict(owner=OWNER,status='KNOWN_PIECE_ARITHMETIC_PASS' if all(c['passed'] for c in CHECKS) else 'ARITHMETIC_FAILED',cases=cases,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS,unknown_full_background=None,unknown_exterior=None,spatial_inverse=None,physical_constitutive_match=None)
        recheck();rh=json_file(STEM+'_RESULT.json',result);publish(STEM+'_REPORT.md',('# '+STEM+'\n\n'+result['status']+'. Compact known-piece action derivatives only; no inverse, orbital force bound or physical closure.\n').encode());recheck()
        rc=dict(owner=OWNER,status='CLOSED',closed=now(),input_sha256=INPUTS,output_sha256=dict(CREATED),result_sha256=rh,qualification=FLAGS);json_file(STEM+'_RECEIPT.json',rc);recheck();assert json.loads(path(STEM+'_RECEIPT.json').read_text())==rc
        print(json.dumps(dict(status=result['status'],controls=len(CHECKS),cases=4,result_sha256=rh),sort_keys=True));return 0 if result['status']=='KNOWN_PIECE_ARITHMETIC_PASS' else 3
    except BaseException:
        failure=traceback.format_exc();prior=path(STEM+'_RECEIPT.json');old_sha=sha(prior) if prior.exists() else None
        if np is not None and RAW:checkpoint('ERROR_RAW',dict(RAW),dict(kind='unaccepted_latest_compact_operands',context=CONTEXT,traceback=failure))
        seal_created();recheck();eh=json_file(STEM+'_ERROR.json',dict(owner=OWNER,traceback=failure,context=CONTEXT,preserved_receipt_sha256=old_sha,output_sha256=dict(CREATED),input_sha256=INPUTS,checkpoints=RECORDS,qualification=FLAGS))
        if old_sha is None:
            rc=dict(owner=OWNER,status='CLOSED_ERROR',closed=now(),error_sha256=eh,input_sha256=INPUTS,output_sha256=dict(CREATED),qualification=FLAGS);json_file(STEM+'_RECEIPT.json',rc);recheck();assert json.loads(path(STEM+'_RECEIPT.json').read_text())==rc
        else:assert sha(prior)==old_sha;recheck()
        raise
if __name__=='__main__':raise SystemExit(main())

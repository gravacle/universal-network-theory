"""Guarded root-only SAME signed-Q1 odd correction from a fully CLOSED owner."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,ast,hashlib,json,math,mmap,os,re,struct,subprocess,traceback,zipfile

AUTHOR_DRAFT=True
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001'
PARENT='CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001'
PARENT_PID=86078
PROTOCOL_SHA='0f7b501037a0f0e65359435825b9d48f49d1249efc6c39a4549e285bdf88423b'
PINS={'cross_u_ngc3198_conditional_odd_sector_v001.py': '508c379f4bd287435b406567f772fb14efdb7142ca17b18ef0d3e4e74736b394', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001.md': '030a618dc6ac06f9faa6748e3559afe074e17be4ad6feba94ae7348a935a9f2e', 'cross_u_ngc3198_odd_banded_driver_v001.c': 'f5a5fd7f7ed663fb2cc1873ba4c063a02fdc50026f7b6ab368f062812d475fd1', '/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/clang': '15339439a6be4a9d33d281ec040a7e0092190b1c8d7de5f94d824b50ffae0769', '/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/System/Library/Frameworks/Accelerate.framework/Versions/A/Headers/Accelerate.h': '20a2be0c151e0590dbed832eef5fe9b2232fc6212f4426aaea6aaf1aa6d07c13', '/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/System/Library/Frameworks/Accelerate.framework/Versions/A/Frameworks/vecLib.framework/Versions/A/Headers/lapack.h': '0a8e9b19e98e6ea16f84aad688efebea790163786bb506aed85cb20a8a3ac431', '/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/System/Library/Frameworks/Accelerate.framework/Versions/A/Frameworks/vecLib.framework/Versions/A/Headers/lapack_types.h': '13f5883531fbf42697bff8ff5f9cc265cc0448e614ed76e3a91ecff96a23b8af', '/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/System/Library/Frameworks/Accelerate.framework/Versions/A/Frameworks/vecLib.framework/Versions/A/Headers/lapack_version.h': 'dbcd4c709a707748a97cd1d12219091eb0f79821cf58fc1992af31337ed5c253', '/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/System/Library/Frameworks/Accelerate.framework/Versions/A/Frameworks/vecLib.framework/Versions/A/libLAPACK.tbd': '38d7eece9a78fff8d9e78867184fbead9ca6c26e8d891d11cdfbf95fd7f44ce6'}
PARENT_TERMINAL_PINS={'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_RESULT.json': 'ce1486a19ec863c90e688b171e1ab9f1258205d412bb3d092d392da9c8ef8132', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_SIGMA_0.1_CASE.json': '84b4c4c323841263510dedb8208d89c2b756566eae359ffb27eb2a61ed78ad79', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_SIGMA_1.0_CASE.json': '613595aaa877ee3a599f67493c15f0833abfaed5b293d0c1f1023597d8a9d05c', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_SIGMA_10.0_CASE.json': '5ba871dc9bafe86ab23ce3f1c801720a78c63f351b28548d19b9eaf230e1ed26', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_SIGMA_100.0_CASE.json': '74f80b745e16bde243bd344d28a92b2f27df19bf134f4c7c06ff83eed5530be5', 'CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001_RECEIPT.json': 'afd64b4dff5f9f4151494749d3d3d54b91dc031e82a394994c6c17e8e24ebe04'}
CLANG='/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/clang'
SDK='/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk'
DRIVER='cross_u_ngc3198_odd_banded_driver_v001.c'
SIGMAS=(.1,1.,10.,100.)
N=7480;KL=KU=91;LDAB=274
C=1.98;KB=2-C;B=1.0059833281731022e-10*3.085677581491367e19/299792458.**2
TRUE_TOL=1e-10;ARITH_TOL=2e-11
np=None;OWNER=None;INPUTS={};CREATED={};RECORDS=[];CHECKS=[];RAW={};CONTEXT={}
FLAGS={k:False for k in ('physical_temporal_spectrum_qualified','physical_exterior_qualified',
 'full_even_metric_qualified','full_stationary_state_qualified','stability_qualified',
 'source_feedback_qualified','formation_qualified','orbital_force_qualified',
 'observational_qualified','joint_model_adopted')}

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
def selected_pair(file,pins,owner):
    commit=file+'.COMMIT.json'
    fields=(('file',),('sha256',),('metadata','kind'),('metadata','owner'),('metadata','schema'))
    v=selected_json(commit,fields);assert v[('file',)]==file and v[('sha256',)]==pins[file]
    assert v[('metadata','owner')]==owner
    return dict(file=file,sha256=pins[file],commit_file=commit,commit_sha256=pins[commit],
        metadata=dict(kind=v[('metadata','kind')],owner=owner,schema=v[('metadata','schema')]))
def inputs_and_parent():
    assert all(type(h) is str and len(h)==64 for h in PARENT_TERMINAL_PINS.values()),'Parent terminal bindings are pending; no live-owner admission.'
    pins=dict(PINS,**PARENT_TERMINAL_PINS,**{STEM+'.md':PROTOCOL_SHA})
    for k,h in pins.items():assert sha(path(k))==h,('direct seal',k)
    rc=json.loads(path(PARENT+'_RECEIPT.json').read_text())
    assert rc['status']=='CLOSED' and rc['owner']['owner']=='root' and rc['owner']['pid']==PARENT_PID
    assert rc['closed']>rc['owner']['started'] and rc['owner']['source_sha256']==PINS['cross_u_ngc3198_conditional_odd_sector_v001.py']
    assert rc['result_sha256']==PARENT_TERMINAL_PINS[PARENT+'_RESULT.json']
    for k,h in dict(rc['input_sha256'],**rc['output_sha256']).items():
        assert k not in pins or pins[k]==h; pins[k]=h
    for k,h in pins.items():assert sha(path(k))==h,('full parent seal',k)
    # Every consumed inherited receipt/output map is byte checked; no producer runs.
    for k in list(pins):
        if k.endswith('_RECEIPT.json'):
            rr=json.loads(path(k).read_text())
            for f,h in rr.get('output_sha256',{}).items():assert sha(path(f))==h,('inherited closed output',f)
    assert rc['qualification']==FLAGS
    files=sorted(k for k in rc['output_sha256'] if k.endswith('.npz'))
    tags=('INPUT','CIRCULAR_SOURCE','SOLVER_CONTROLS','COEFFICIENTS','FINAL','COEFFICIENTS','FINAL','COEFFICIENTS','FINAL','COEFFICIENTS','FINAL')
    assert files==[f'{PARENT}_{i:05d}_{t}.npz' for i,t in enumerate(tags)]
    assert set(k for k in rc['output_sha256'] if k.endswith('.npz.COMMIT.json'))=={f+'.COMMIT.json' for f in files}
    records=[selected_pair(f,pins,rc['owner']) for f in files]
    controls=selected_json(records[2]['commit_file'],{('metadata','controls')})[('metadata','controls')]
    cases=[]
    for i,sigma in enumerate(SIGMAS):
        co=records[3+2*i];fi=records[4+2*i];name=PARENT+'_SIGMA_'+str(sigma)+'_CASE.json'
        fields={('sigma',),('status',),('original_residual',),('qualification',)}
        for prefix in ('coefficient_checkpoint','final_checkpoint'):
            fields.update((prefix,k) for k in ('file','sha256','commit_file','commit_sha256'))
        v=selected_json(name,fields)
        assert v[('sigma',)]==sigma and v[('status',)] in ('LINEAR_FAILED','LINEAR_PASS') and v[('qualification',)]==FLAGS
        for prefix,rec in (('coefficient_checkpoint',co),('final_checkpoint',fi)):
            for key in ('file','sha256','commit_file','commit_sha256'):assert v[(prefix,key)]==rec[key]
        cm=selected_json(co['commit_file'],{('metadata','sigma'),('metadata','controls')})
        fm=selected_json(fi['commit_file'],{('metadata','sigma'),('metadata','status'),('metadata','original_residual'),('metadata','coefficient_checkpoint')})
        assert co['metadata']['kind']=='signed_odd_quadratic_action' and fi['metadata']['kind']=='all_signed_odd_partial_and_readouts'
        assert cm[('metadata','sigma')]==fm[('metadata','sigma')]==sigma
        assert fm[('metadata','coefficient_checkpoint')]==co['file'] and fm[('metadata','status')]==v[('status',)]
        assert fm[('metadata','original_residual')]==v[('original_residual',)]
        controls.extend(cm[('metadata','controls')])
        cases.append(dict(sigma=sigma,status=v[('status',)],original_residual=v[('original_residual',)],case_file=name,
            case_sha256=pins[name],coefficient_checkpoint=co,final_checkpoint=fi,qualification=FLAGS))
    assert len(controls)==21 and all(c['passed'] for c in controls)
    return pins,dict(owner=rc['owner'],controls=controls,cases=cases,checkpoints=records,qualification=FLAGS,
        result_file=PARENT+'_RESULT.json',result_sha256=pins[PARENT+'_RESULT.json'])
def load_pair(rec):
    # Complete parent file/commit bytes were admitted above. Read only the scalar
    # Unicode metadata header, not its 89 MB inherited JSON payload into RAM.
    with zipfile.ZipFile(path(rec['file'])) as zz,zz.open('metadata.npy') as f:
        magic=f.read(8);assert magic[:6]==b'\x93NUMPY' and magic[6:]==b'\x01\x00'
        length=struct.unpack('<H',f.read(2))[0];header=ast.literal_eval(f.read(length).decode())
        assert header['shape']==() and not header['fortran_order'] and header['descr'].startswith('<U')
    with np.load(path(rec['file']),allow_pickle=False) as z:
        assert set(z.files)==set(rec['metadata']['schema'])|{'metadata'}
        a={}
        for k,s in rec['metadata']['schema'].items():
            v=z[k].copy();RAW['loaded_'+k]=v
            assert s==dict(shape=list(v.shape),dtype=str(v.dtype),finite=bool(np.all(np.isfinite(v))))
            assert s['finite'];a[k]=v
    return a
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
def recheck():
    assert sha(__file__)==OWNER['source_sha256']
    for k,h in INPUTS.items():assert sha(path(k))==h,('input seal',k)
    for k,h in CREATED.items():assert sha(BASE/k)==h,('own seal',k)
    if STEM+'_OWNER_START.json' in CREATED:assert json.loads(path(STEM+'_OWNER_START.json').read_text())==OWNER
    for rec in RECORDS:
        assert json.loads(path(rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
        with np.load(path(rec['file']),allow_pickle=False) as z:
            assert json.loads(str(z['metadata']))==rec['metadata'] and set(z.files)==set(rec['metadata']['schema'])|{'metadata'}
            for k,s in rec['metadata']['schema'].items():
                a=z[k];assert s==dict(shape=list(a.shape),dtype=str(a.dtype),finite=bool(np.all(np.isfinite(a))))
def check(name,a,b):
    a=np.asarray(a);b=np.asarray(b);i=len(CHECKS);CONTEXT.update(control=name,control_ordinal=i)
    RAW[f'control_{i:03d}_{name}_actual']=a.copy();RAW[f'control_{i:03d}_{name}_expected']=b.copy()
    assert a.shape==b.shape
    gap=float(np.linalg.norm(a-b));env=max(1e-30,float(np.linalg.norm(a)),float(np.linalg.norm(b)))
    er=gap/env;row=dict(name=name,error=finite(er),absolute_gap=finite(gap),envelope=finite(env),tolerance=ARITH_TOL,passed=math.isfinite(er) and er<=ARITH_TOL)
    CHECKS.append(row);return row

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


def add(out,value,gr,gz,volume,shapes):
    for n,nr,nz,i,j in shapes:
        out[...,i:out.shape[-2]-1+i,j:out.shape[-1]-1+j]+=volume*(n*value+nr*gr+nz*gz)


class SavedAction:
    def __init__(self,data,r,z):
        self.shape=(2,len(r),len(z));self.mask=data['free_mask'].copy();self.alpha=KB/C
        assert self.shape==(2,87,45) and self.mask.dtype==bool
        expected=np.ones(self.shape,bool);expected[:,-1,:]=False;expected[:,:,-1]=False;expected[:,0,:]=False
        assert np.array_equal(self.mask,expected)
        self.quad=[]
        for iq,(_,_,shapes) in enumerate(shape_quadrature(r,z)):
            k=lambda n:data[f'q{iq}_'+n]
            self.quad.append((k('volume'),shapes,k('expPhi'),k('rho'),k('a'),k('b'),k('d'),k('zh'),k('T'),k('bz'),k('dz'),k('At'),k('k'),k('cchi')))
    def lift(self,y):
        assert y.shape==self.shape;v=np.where(self.mask,y,0.);v[0,0]=v[0,1];return v

    def restrict(self,y):
        y[0,1]+=y[0,0];y[~self.mask]=0;return y

    def action(self,y):
        v=self.lift(y);out=np.zeros(self.shape)
        for volume,shapes,ef,rho,a,b,d,zh,T,bz,dz,At,k,cc in self.quad:
            val,gr,gz=interpolate(v,shapes);chi=val[1];t=rho[...,None]*np.stack([gr[0],gz[0]],axis=-1)
            W=ef[...,None]*np.stack([gr[1],gz[1]],axis=-1)+chi[...,None]*d
            pt=np.einsum('...ab,...b->...a',At,t)+chi[...,None]*k
            ch=cc*chi+np.sum(k*t,axis=-1)-self.alpha*np.sum(d*W,axis=-1)
            add(out[0],np.zeros_like(chi),rho*pt[...,0],rho*pt[...,1],volume,shapes)
            add(out[1],ch,-self.alpha*ef*W[...,0],-self.alpha*ef*W[...,1],volume,shapes)
        return self.restrict(out)


def pack(x):
    assert x.shape==(2,87,45)
    return x[:,1:-1,:-1].transpose(1,2,0).reshape(N).copy()
def unpack(v):
    assert v.shape==(N,);x=np.zeros((2,87,45));x[:,1:-1,:-1]=v.reshape(85,44,2).transpose(2,0,1);return x
def band_action(ab,x,kl=KL,ku=KU):
    n=len(x);out=np.zeros(n)
    for off in range(-ku,kl+1):
        i=np.arange(max(0,off),min(n,n+off));j=i-off
        out[i]+=ab[kl+ku+off,j]*x[j]
    return out
def assemble(model):
    ab=np.zeros((LDAB,N),order='F');RAW['current_band']=ab
    ir=np.arange(86)[:,None];iz=np.arange(44)[None,:]
    def index(i,j,f):
        R=np.broadcast_to(ir+i,(86,44));Z=np.broadcast_to(iz+j,(86,44))
        if f==0:R=np.where(R==0,1,R)
        good=(R>0)&(R<86)&(Z<44)
        return ((R-1)*44+Z)*2+f,good
    for volume,shapes,ef,rho,a,b,d,zh,T,bz,dz,At,k,cc in model.quad:
        tests=[]
        for n,nr,nz,i,j in shapes:
            grad=np.stack(np.broadcast_arrays(nr,nz),axis=-1)
            tg=rho[...,None]*grad;wc=ef[...,None]*grad+n*d
            tests.append((n,tg,wc,index(i,j,0),index(i,j,1)))
        for na,ta,wa,ia,ca in tests:
            for nb,tb,wb,ib,cb in tests:
                values=((ia,ib,np.einsum('...a,...ab,...b->...',ta,At,tb)),
                        (ia,cb,np.sum(ta*k,axis=-1)*nb),
                        (ca,ib,na*np.sum(k*tb,axis=-1)),
                        (ca,cb,cc*na*nb-model.alpha*np.sum(wa*wb,axis=-1)))
                for (ii,ok_i),(jj,ok_j),v in values:
                    good=ok_i&ok_j;off=ii[good]-jj[good];RAW['current_local_entry']=v.copy()
                    assert np.all(abs(off)<=KL)
                    np.add.at(ab,(KL+KU+off,jj[good]),(volume*v)[good])
    assert np.all(np.isfinite(ab));return ab
def symmetry_vectors(ab):
    left=[];right=[]
    for off in range(1,KL+1):
        j=np.arange(N-off);left.append(ab[KL+KU+off,j]);right.append(ab[KL+KU-off,j+off])
    return np.concatenate(left),np.concatenate(right)
def build_driver():
    exe=BASE/(STEM+'_DRIVER.exe');argv=[CLANG,'-O2','-std=c11','-isysroot',SDK,str(BASE/DRIVER),'-framework','Accelerate','-o',str(exe)]
    CONTEXT.update(stage='root_only_C_build',argv=argv)
    p=subprocess.run(argv,capture_output=True,check=False)
    publish(STEM+'_BUILD.stdout',p.stdout);publish(STEM+'_BUILD.stderr',p.stderr);seal_created()
    json_file(STEM+'_BUILD.json',dict(argv=argv,returncode=p.returncode,compiler_sha256=INPUTS[CLANG],executable_sha256=CREATED.get(exe.name),no_install=True))
    assert p.returncode==0 and exe.is_file(),'C build failed; all available outputs retained.'
    exe.chmod(0o555);CREATED[exe.name]=sha(exe);return exe
def driver_solve(exe,tag,ab,rhs,kl,ku):
    n=len(rhs);assert ab.shape==(2*kl+ku+1,n) and np.all(np.isfinite(ab)) and np.all(np.isfinite(rhs))
    prefix=STEM+'_'+tag;names={k:prefix+'_'+k+'.bin' for k in ('BAND','RHS','LU','CORRECTION','PIVOTS','INFO')}
    publish(names['BAND'],np.asarray(ab,dtype='<f8').tobytes(order='F'));publish(names['RHS'],np.asarray(rhs,dtype='<f8').tobytes())
    argv=[str(exe),str(n),str(kl),str(ku)]+[str(BASE/names[k]) for k in ('BAND','RHS','LU','CORRECTION','PIVOTS','INFO')]
    CONTEXT.update(stage='root_only_dgbsv',driver_argv=argv)
    p=subprocess.run(argv,capture_output=True,check=False)
    publish(prefix+'_DRIVER.stdout',p.stdout);publish(prefix+'_DRIVER.stderr',p.stderr);seal_created()
    assert p.returncode==0,('Native driver refused',p.returncode)
    outputs={}
    for k,dtype,count in (('LU','<f8',ab.size),('CORRECTION','<f8',n),('PIVOTS','<i4',n),('INFO','<i4',1)):
        raw=(BASE/names[k]).read_bytes();assert len(raw)==np.dtype(dtype).itemsize*count
        v=np.frombuffer(raw,dtype=dtype).copy();outputs[k]=v;RAW['driver_'+k]=v.copy()
    outputs['LU']=outputs['LU'].reshape(ab.shape,order='F')
    return outputs,dict(argv=argv,returncode=p.returncode,outputs={n:CREATED[n] for n in names.values()})
def driver_controls(exe):
    ab=np.zeros((4,3));ab[2]=[0,-1,4];ab[3,:2]=[2,3];ab[1,1:]=[2,3]
    rhs=np.array([-4.,13.,6.]);out,meta=driver_solve(exe,'KNOWN_PIVOT',ab,rhs,1,1)
    assert out['INFO'][0]==0;check('known_pivoted_indefinite_solution',out['CORRECTION'],np.array([1.,-2.,3.]))
    checkpoint('KNOWN_PIVOT',dict(band=ab,rhs=rhs,**out,**RAW),dict(kind='LP64_binary_ABI_known_pivot',driver=meta,controls=list(CHECKS)))
    RAW.clear();ab=np.zeros((4,2));ab[2]=1.;ab[3,0]=1.;ab[1,1]=1.
    out,meta=driver_solve(exe,'KNOWN_SINGULAR',ab,np.array([2.,2.]),1,1)
    check('known_singular_INFO',out['INFO'],np.array([2],dtype=np.int32))
    checkpoint('KNOWN_SINGULAR',dict(band=ab,rhs=np.array([2.,2.]),**out,**RAW),dict(kind='LP64_exact_singular_INFO_refusal',driver=meta,controls=list(CHECKS)))
    assert all(c['passed'] for c in CHECKS),'Driver ABI control refusal.'
def recover(exe,case,r,z,phi):
    RAW.clear();CONTEXT.clear();CONTEXT.update(sigma=case['sigma'],stage='closed_saved_arm_admission')
    coeff=load_pair(case['coefficient_checkpoint']);final=load_pair(case['final_checkpoint'])
    model=SavedAction(coeff,r,z);partial=final['unknown_coordinates'];rhs=final['original_rhs'];res=final['original_residual']
    assert np.array_equal(rhs,coeff['rhs']) and np.all(partial[~model.mask]==0)
    assert np.array_equal(final['physical_beta_chi'],model.lift(partial))
    ab=assemble(model);RAW['assembled_band']=ab.copy();begin=len(CHECKS)
    y=coeff['manufactured_y'];q=coeff['manufactured_q']
    check('sigma_'+str(case['sigma'])+'_band_manufactured_y',band_action(ab,pack(y)),pack(coeff['manufactured_Hy']))
    check('sigma_'+str(case['sigma'])+'_band_manufactured_q',band_action(ab,pack(q)),pack(coeff['manufactured_Hq']))
    check('sigma_'+str(case['sigma'])+'_band_saved_partial',band_action(ab,pack(partial)),pack(final['original_H_action']))
    check('sigma_'+str(case['sigma'])+'_saved_residual',pack(final['original_H_action']-rhs),pack(res))
    left,right=symmetry_vectors(ab);check('sigma_'+str(case['sigma'])+'_band_symmetry',left,right)
    assembled=checkpoint('ASSEMBLY',dict(band=ab,partial=partial,original_rhs=rhs,saved_residual=res,
        manufactured_y=y,manufactured_q=q,saved_Hy=coeff['manufactured_Hy'],saved_Hq=coeff['manufactured_Hq'],saved_Hpartial=final['original_H_action'],**{k:v for k,v in RAW.items() if k.startswith('control_')}),
        dict(kind='same_signed_Q1_band_before_LAPACK',sigma=case['sigma'],parent_coefficient=case['coefficient_checkpoint'],parent_final=case['final_checkpoint'],controls=CHECKS[begin:]))
    assert all(c['passed'] for c in CHECKS[begin:]),'Signed band equivalence refusal; no factorization.'
    out,driver=driver_solve(exe,'SIGMA_'+str(case['sigma']),ab,-pack(res),KL,KU)
    info=int(out['INFO'][0]);arrays=dict(LU=out['LU'],pivots=out['PIVOTS'],INFO=out['INFO'],correction_vector=out['CORRECTION'],partial=partial)
    accepted=False;error=None;smallness=None
    if info==0 and all(np.all(np.isfinite(out[k])) for k in ('LU','CORRECTION')):
        correction=unpack(out['CORRECTION']);RAW['physical_correction']=correction
        candidate=partial+correction;RAW['physical_candidate']=candidate
        action=model.action(candidate);RAW['fresh_original_H_action']=action
        residual=action-rhs;RAW['fresh_original_residual']=residual
        norm=float(np.linalg.norm(rhs));error=finite(float(np.linalg.norm(residual)/norm)) if norm>0 and math.isfinite(norm) else None
        accepted=error is not None and error<=TRUE_TOL and np.all(np.isfinite(candidate)) and np.all(np.isfinite(action))
        physical=model.lift(candidate);RAW['physical_beta_chi']=physical
        speed=r[:,None]*np.exp(-2*phi)*physical[0];smallness=dict(max_abs_chi=finite(float(np.max(abs(physical[1])))),max_abs_shift_speed_over_c=finite(float(np.max(abs(speed)))))
        arrays.update(correction=correction,unknown_coordinates=candidate,physical_beta_chi=physical,original_H_action=action,original_residual=residual,original_rhs=rhs,coordinate_shift_speed_over_c=speed)
    status='LINEAR_PASS' if accepted else 'LINEAR_FAILED'
    final_cp=checkpoint('FINAL',arrays,dict(kind='signed_direct_correction_from_saved_partial',sigma=case['sigma'],status=status,INFO=info,original_residual=error,original_tolerance=TRUE_TOL,assembly_checkpoint=assembled['file'],driver=driver,smallness=smallness,smallness_qualified=False,original_parent_status=case['status'],original_parent_residual=case['original_residual']))
    row=dict(sigma=case['sigma'],status=status,INFO=info,original_residual=error,parent_status=case['status'],parent_residual=case['original_residual'],assembly_checkpoint=assembled,final_checkpoint=final_cp,smallness=smallness,qualification=FLAGS)
    json_file(STEM+'_SIGMA_'+str(case['sigma'])+'_CASE.json',row);return row
def main():
    global np,OWNER,INPUTS
    ap=argparse.ArgumentParser();ap.add_argument('--root-run',action='store_true');args=ap.parse_args()
    assert args.root_run and not AUTHOR_DRAFT and len(PROTOCOL_SHA)==64,'Guarded draft is unlaunchable.'
    assert not list(BASE.glob(STEM+'_*')),'Unused own namespace; no automatic resume or producer rerun.'
    INPUTS,parent=inputs_and_parent();OWNER=dict(owner='root',pid=os.getpid(),started=now(),source_sha256=sha(__file__))
    cases=[]
    try:
        json_file(STEM+'_OWNER_START.json',OWNER)
        json_file(STEM+'_MANIFEST.json',dict(owner=OWNER,input_sha256=INPUTS,parent_owner=parent['owner'],sigmas=SIGMAS,n=N,kl=KL,ku=KU,ldab=LDAB,configuration=dict(original_tolerance=TRUE_TOL,arithmetic_tolerance=ARITH_TOL,regularization=False,partial_recovery=True),qualification=FLAGS))
        import numpy as _np
        np=_np
        recs=parent['checkpoints'];input_rec=[r for r in recs if r['metadata']['kind']=='unchanged_authentic_even_state'];assert len(input_rec)==1
        data=load_pair(input_rec[0]);r=data['r_kpc'];z=data['z_kpc'];phi=B*data['final_state'][0]
        assert r.shape==(87,) and z.shape==(45,) and np.all(np.diff(r)>0) and np.all(np.diff(z)>0)
        assert r[0]==z[0]==0 and r[-1]==z[-1]==128
        checkpoint('INPUT',dict(r_kpc=r,z_kpc=z,held_Phi=phi),dict(kind='unchanged_closed_geometry_and_parent_dispositions',parent_input=input_rec[0],parent_result_file=parent['result_file'],parent_result_sha256=parent['result_sha256'],copied_parent_controls=parent['controls'],copied_parent_qualification=parent['qualification']))
        RAW.clear();exe=build_driver();driver_controls(exe)
        for case in parent['cases']:cases.append(recover(exe,case,r,z,phi))
        assert len(CHECKS)==22 and len(RECORDS)==11
        status='CONDITIONAL_LINEAR_PASS' if all(c['status']=='LINEAR_PASS' for c in cases) else 'CONDITIONAL_NUMERICAL_FAILED'
        result=dict(owner=OWNER,status=status,parent_owner=parent['owner'],cases=cases,controls=CHECKS,copied_parent_controls=parent['controls'],copied_parent_cases=[dict(sigma=c['sigma'],status=c['status'],original_residual=c['original_residual']) for c in parent['cases']],checkpoints=RECORDS,qualification=FLAGS)
        recheck();rh=json_file(STEM+'_RESULT.json',result)
        report=('# '+STEM+'\n\n'+status+'. Four fixed arms; original signed action and source retained.\n\n'+''.join(f'- sigma={c["sigma"]}: {c["status"]}, INFO={c["INFO"]}, original residual={c["original_residual"]}\n' for c in cases)+'\nNo physical inertia/exterior/stability/full-state/force qualification.\n').encode()
        publish(STEM+'_REPORT.md',report);recheck()
        rc=dict(owner=OWNER,status='CLOSED',closed=now(),input_sha256=INPUTS,output_sha256=dict(CREATED),result_sha256=rh,qualification=FLAGS)
        json_file(STEM+'_RECEIPT.json',rc);recheck();assert json.loads(path(STEM+'_RECEIPT.json').read_text())==rc
        print(json.dumps(dict(status=status,cases=len(cases),controls=len(CHECKS),result_sha256=rh),sort_keys=True));return 0 if status=='CONDITIONAL_LINEAR_PASS' else 3
    except BaseException:
        failure=traceback.format_exc();prior=path(STEM+'_RECEIPT.json');old_sha=sha(prior) if prior.exists() else None
        if np is not None and RAW:checkpoint('ERROR_RAW',dict(RAW),dict(kind='unaccepted_available_band_driver_operands',context=CONTEXT,traceback=failure))
        seal_created();recheck()
        eh=json_file(STEM+'_ERROR.json',dict(owner=OWNER,failed=now(),context=CONTEXT,traceback=failure,checkpoints=RECORDS,controls=CHECKS,preserved_outputs=dict(CREATED),existing_receipt_sha256=old_sha,qualification=FLAGS))
        if old_sha is None:
            rc=dict(owner=OWNER,status='CLOSED_ERROR',closed=now(),input_sha256=INPUTS,output_sha256=dict(CREATED),error_sha256=eh,qualification=FLAGS)
            json_file(STEM+'_RECEIPT.json',rc);recheck();assert json.loads(prior.read_text())==rc
        else:recheck();assert sha(prior)==old_sha
        raise
if __name__=='__main__':raise SystemExit(main())

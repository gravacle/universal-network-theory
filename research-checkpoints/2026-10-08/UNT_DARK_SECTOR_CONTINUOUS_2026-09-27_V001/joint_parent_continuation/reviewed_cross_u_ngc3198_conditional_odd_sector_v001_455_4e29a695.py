"""Root-only conditional four-inertia odd-sector benchmark; no even-field solve."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,importlib.util,json,math,os,traceback

AUTHOR_DRAFT=True
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_NGC3198_CONDITIONAL_ODD_SECTOR_V001'
PARENT='CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V002'
PROTOCOL_SHA='6de18bf4e98dc3c7b4d460d9f9c088ad1ae391be8501d6e0ffaf06795a37c845'
PINS={'CROSS_U_STATIONARY_AZIMUTHAL_SHIFT_AND_NATIVE_RESPONSE_V001.md': '048b224899adf28c6924fa02c06a2e2d42fced7f086a139ed8a6981e0dc20fe2', 'CROSS_U_CONFORMAL_COLD_CIRCULAR_NEXT_ORDER_SOURCE_CLOSURE_V001.md': 'f8365d7bff3f420efe7d30746fd8fe3983a88e62dda1442c00ad73329e087979', 'CROSS_U_STATIONARY_AXISYMMETRIC_ORBIT_AND_ORDINARY_MATTER_REGISTRATION_V001.md': 'b962a4e6cc2583033f66b5194b50d47e1553456feda4147624d9f246bc86ebd5', 'CROSS_U_FULL_FLRW_SOURCE_CONSTRAINT_AND_FINITE_SLICE_TEST_V001.md': 'c81fa7ed6961f5f0620bbb48dd133ef474543765131ceb738bdcf676f9b9a986', 'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md': 'e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0', 'cross_u_ngc3198_nonlinear_disk_v001.py': 'ae4285fc9c19cdf2d8efa176ac3d770b7eaf379a75fa3b9627bc9d3f6f3179e1', 'cross_u_ngc3198_minres_recovery_v003.py': '5f807a858ac7b00e29b724a39e4d1de4d96e102442530b067bbc2ee7953a5683', 'cross_u_ngc3198_sparc_stellar_footprint_v002.py': '95c86130b9a348da58f2c3442b51460bdc980998b4395114a4ba3ad69ebd4ac0', 'CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V002.md': '0e17b74071cf9bfe1b9066c24ac13dd9a969f7cf21bdf1042b2afd3c6b33ccc9', 'galaxy_density.py': '9819b9cb1f63baea07eb06a150dbda3113d7850d9ac24a13ee65e96f6f07bb6c', 'NGC3198_BARYON_INPUT.json': '8895693861ee0db1b42136c6aac7f0fb9fa9e0e84c72c69e8c8e3c89ba0e78d1', 'sparc_official_NGC3198_rotmod.dat': '17b774ad11e7dd745a067073b76f1909d4de32fa87616df12b64da3f225cf953', 'CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V002_RECEIPT.json': 'bd3f63a75dc1296ae3c6fad84bcf6b1a09c051d5a5dc8a2ee9afe9e483a775b8', 'CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V002_MANIFEST.json': '31877af20581a9c63d7df0b54488e19b804369c524a7b22fe21d4ff87201b62e', 'CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V002_EXP24_CASE.json': '2a25fb0da765a9db6490b912aab45cad415506a70b1cfc1a5cfb8d4fd93063a7', 'CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V002_RESULT.json': '9e74228d73b0df6312836dfced7b5053743561289a03b8b0f0245d469c34203a', 'CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V002_00044_FINAL.npz': 'cd4cda3a48f9d104a69a25f896d11af08bf2130d35be9c356cfbc785be1a2fa6', 'CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V002_00044_FINAL.npz.COMMIT.json': '0b5d5bc5f8217503731b5960f824839c9f572a50573474998eeaae8f89aadb39'}
RECEIPT_EXPECTATIONS={'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V006_RECEIPT.json': {'status': 'CLOSED', 'owner_kind': 'dict', 'pid': 62181}, 'CROSS_U_NONZERO_NATIVE_CURVATURE_SPLIT_V001_RECEIPT.json': {'status': None, 'owner_kind': 'str', 'pid': 50386}, 'CROSS_U_Q1_PROJECTION_STIFFNESS_V001_RECEIPT.json': {'status': None, 'owner_kind': 'str', 'pid': 47083}, 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RECEIPT.json': {'status': 'NUMERICAL_PASS', 'owner_kind': 'str', 'pid': 39330}, 'NGC3198_STATIONARY_LAPSE_SPAN_V001_RECEIPT.json': {'status': 'PASS', 'owner_kind': 'NoneType', 'pid': None}, 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_PANTHEON_PROFILE_V002_RECEIPT.json': {'status': 'NEW_FIXED_PANTHEON_PROFILE_ARITHMETIC_PASS', 'owner_kind': 'NoneType', 'pid': None}, 'CONSTRAINED_U_CLOCK_GRADIENT_RECOMBINATION_PAIR_V002_RECEIPT.json': {'status': 'NEW_ATOMIC_PAIR_ARITHMETIC_PASS', 'owner_kind': 'NoneType', 'pid': None}, 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_PAIR_V001_RECEIPT.json': {'status': 'FIXED_NEVO_NEW_ACTION_NUMERICALLY_QUALIFIED', 'owner_kind': 'NoneType', 'pid': None}, 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V002_RECEIPT.json': {'status': 'NEW_ATOMIC_PAIR_ARITHMETIC_PASS', 'owner_kind': 'NoneType', 'pid': None}, 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_ACOUSTIC_READOUT_V001_RECEIPT.json': {'status': 'NEW_BBN_ACOUSTIC_ARITHMETIC_PASS', 'owner_kind': 'NoneType', 'pid': None}, 'CROSS_U_NGC3198_PARTIAL_RECOVERY_V002_RECEIPT.json': {'status': None, 'owner_kind': 'str', 'pid': 42904}, 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_RECEIPT.json': {'status': None, 'owner_kind': 'str', 'pid': 49006}, 'CROSS_U_NGC3198_NONLINEAR_DISK_V001_RECEIPT.json': {'status': None, 'owner_kind': 'str', 'pid': 42114}, 'CROSS_U_DIRECT_SCALAR_PROXY_CONTROLS_V001_RECEIPT.json': {'status': 'CLOSED', 'owner_kind': 'dict', 'pid': 56449}, 'CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V001_RECEIPT.json': {'status': 'CLOSED', 'owner_kind': 'dict', 'pid': 76290}, 'CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V002_RECEIPT.json': {'status': 'CLOSED', 'owner_kind': 'dict', 'pid': 76996}}
C=1.98;KB=2-C;ELL=.1;A0=1.0059833281731022e-10;KPC=3.085677581491367e19
LIGHT=299792458.;B=A0*KPC/LIGHT**2;A0_V=A0*KPC/1e6
SIGMAS=(.1,1.,10.,100.)
CAP=2400;TRUE_TOL=1e-10;ARITH_TOL=2e-11
FLAGS={k:False for k in ('physical_temporal_spectrum_qualified','physical_exterior_qualified','full_even_metric_qualified','full_stationary_state_qualified','stability_qualified','source_feedback_qualified','formation_qualified','orbital_force_qualified','observational_qualified','joint_model_adopted')}
np=density=None;OWNER=None;INPUTS={};CREATED={};RECORDS=[];RAW={};CONTEXT={};CHECKS=[];PARENT_SHORT=None

def now():return datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def finite(x):return float(x) if math.isfinite(float(x)) else None
def canonical(v):
    if isinstance(v,dict):return {str(k):canonical(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [canonical(x) for x in v]
    if np is not None and isinstance(v,np.generic):return canonical(v.item())
    if v is None or type(v) in (str,bool,int):return v
    if type(v) is float:assert math.isfinite(v);return v
    raise TypeError(type(v).__name__)
def encode(v):return (json.dumps(canonical(v),sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def publish(name,data):
    raw=encode(data);p=BASE/name
    with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    p.chmod(0o444);assert p.read_bytes()==raw;CREATED[name]=sha(p);return CREATED[name]
def closed_map(name):
    r=json.loads((BASE/name).read_text());ex=RECEIPT_EXPECTATIONS[Path(name).name]
    assert r.get('status')==ex['status'] and type(r.get('owner')).__name__==ex['owner_kind']
    o=r.get('owner')
    if isinstance(o,dict):assert o.get('owner','root')=='root' and o['pid']==ex['pid'] and r.get('closed',r.get('finished_utc'))>o.get('started',o.get('started_utc'))
    elif isinstance(o,str):assert o=='root' and r['pid']==ex['pid'] and r['closed']>r['started']
    else:assert 'owner' not in r and ex['owner_kind']=='NoneType'
    ins=dict(r.get('input_sha256',r.get('pins',{})));outs=r['output_sha256'];assert outs
    for n,h in outs.items():assert sha(BASE/n)==h,('closed output changed',n)
    manifest=Path(name).name[:-len('_RECEIPT.json')]+'_MANIFEST.json'
    keys=[k for k in outs if Path(k).name==manifest]
    if keys:
        assert len(keys)==1;m=json.loads((BASE/keys[0]).read_text())
        if 'manifest' in r:assert m==r['manifest']
        if 'manifest_sha256' in r:assert outs[keys[0]]==r['manifest_sha256']
        for k,h in dict(m.get('input_sha256',{}),**m.get('inherited_input_sha256',{})).items():
            assert k not in ins or ins[k]==h;ins[k]=h
    return dict(ins,**outs)
def resolve_inputs():
    result=dict(PINS,**{STEM+'.md':PROTOCOL_SHA});todo=[PARENT+'_RECEIPT.json'];seen=set()
    while todo:
        n=todo.pop();assert sha(BASE/n)==result[n]
        if n in seen:continue
        seen.add(n)
        for k,h in closed_map(n).items():
            assert len(h)==64 and (k not in result or result[k]==h),('seal conflict',k)
            result[k]=h
            if k.endswith('_RECEIPT.json') and k not in seen:todo.append(k)
    for k,h in result.items():assert sha(BASE/k)==h,('input changed',k)
    return result
def parent_binding():
    r=json.loads((BASE/(PARENT+'_RECEIPT.json')).read_text())
    m=json.loads((BASE/(PARENT+'_MANIFEST.json')).read_text())
    c=json.loads((BASE/(PARENT+'_EXP24_CASE.json')).read_text())
    assert r['status']=='CLOSED' and r['owner']['pid']==76996 and c['status']=='CONVERGED' and c['numerical_residual']<=1e-8
    assert c['identity']['case']=='E1em05_SPARC_EXP24_HI0_H20_CONTROL_RECOVERY_V002'
    si=c['identity']['source_identity'];assert si['eps']==1e-5 and si['source_id']=='EXP24' and si['native_modes']==32
    assert si['M_to_L']==.5 and si['Rd_kpc']==3.14 and si['anchor']==[24.03,.28] and si['grid_shape']==[65,87,45]
    assert si['hi_tail'] is False and si['h2_tail'] is False and si['law_changes']==[]
    physical={k:v for k,v in m['source_identity'].items() if k not in ('control_registration','recovery_law_changes','recovery_parent_final')}
    assert physical==si and m['owner']==r['owner']
    records=c['own_checkpoints'];assert len(records)==45
    for rec in records:
        assert INPUTS[rec['file']]==r['output_sha256'][rec['file']]==rec['sha256']
        assert INPUTS[rec['commit_file']]==r['output_sha256'][rec['commit_file']]==rec['commit_sha256']
        assert json.loads((BASE/rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
    rec=c['final_checkpoint'];assert rec==records[-1] and rec['file']==PARENT+'_00044_FINAL.npz'
    md=rec['metadata'];assert md['kind']=='final_state_and_signed_readouts' and md['status']==c['status'] and md['identity']==c['identity']
    assert md['history']==c['history'] and md['rows']==c['rows'] and md['error']==c['numerical_residual']
    assert c['readout_qualified'] is False and all(v is False for v in c['physical_flags'].values())
    assert len(c['source_controls'])==20 and all(v['passed'] for v in c['source_controls'])
    assert len(c['controls'])==6 and all(v['passed'] for v in c['controls'])
    return rec,dict(file=rec['file'],sha256=rec['sha256'],commit_file=rec['commit_file'],commit_sha256=rec['commit_sha256'],
        case_file=PARENT+'_EXP24_CASE.json',case_sha256=INPUTS[PARENT+'_EXP24_CASE.json'],status=c['status'],
        error=c['numerical_residual'],source_identity=si,original_source_controls=c['source_controls'],new_native_controls=c['controls'],
        original_native_failed_controls=c['historical_native_controls'],physical_flags=c['physical_flags'],
        history_length=len(c['history']),identity_sha256=hashlib.sha256(encode(c['identity'])).hexdigest())
def checkpoint(tag,arrays,meta):
    md=canonical(dict(meta,owner=OWNER,parent=PARENT_SHORT,qualification=FLAGS,
        schema={k:dict(shape=list(v.shape),dtype=str(v.dtype),finite=bool(np.all(np.isfinite(v)))) for k,v in arrays.items()}))
    text=encode(md).decode();md=json.loads(text);p=BASE/f'{STEM}_{len(RECORDS):05d}_{tag}.npz'
    with p.open('xb') as f:np.savez_compressed(f,metadata=text,**arrays);f.flush();os.fsync(f.fileno())
    p.chmod(0o444);CREATED[p.name]=sha(p)
    rec=dict(file=p.name,sha256=CREATED[p.name],metadata=md)
    ch=publish(p.name+'.COMMIT.json',rec);rec=dict(rec,commit_file=p.name+'.COMMIT.json',commit_sha256=ch);RECORDS.append(rec)
    with np.load(p,allow_pickle=False) as z:
        assert str(z['metadata'])==text and set(z.files)==set(arrays)|{'metadata'}
        for k,v in arrays.items():assert np.array_equal(z[k],v,equal_nan=True)
    return rec
def recheck():
    assert sha(__file__)==OWNER['source_sha256'] and resolve_inputs()==INPUTS
    for n,h in CREATED.items():assert sha(BASE/n)==h,('own output changed',n)
    if STEM+'_OWNER_START.json' in CREATED:assert json.loads((BASE/(STEM+'_OWNER_START.json')).read_text())==OWNER
    for rec in RECORDS:
        assert json.loads((BASE/rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
        with np.load(BASE/rec['file'],allow_pickle=False) as z:
            assert json.loads(str(z['metadata']))==rec['metadata'] and set(z.files)==set(rec['metadata']['schema'])|{'metadata'}
            for k,s in rec['metadata']['schema'].items():
                a=z[k];assert s==dict(shape=list(a.shape),dtype=str(a.dtype),finite=bool(np.all(np.isfinite(a))))
def check(name,actual,expected,tol=ARITH_TOL,envelope=None):
    i=len(CHECKS);CONTEXT.update(control=name,control_ordinal=i)
    a=np.asarray(actual);b=np.asarray(expected);RAW[f'control_{i:03d}_{name}_actual']=a.copy();RAW[f'control_{i:03d}_{name}_expected']=b.copy()
    assert a.shape==b.shape
    gap=float(np.max(abs(a-b))) if a.size else 0.
    env=max(1e-30,float(np.max(abs(a))) if a.size else 0.,float(np.max(abs(b))) if b.size else 0.) if envelope is None else max(1e-30,float(envelope))
    er=gap/env;row=dict(name=name,error=finite(er),absolute_gap=finite(gap),envelope=finite(env),tolerance=tol,passed=math.isfinite(er) and er<=tol)
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

def surface_load(r,profiles,order):
    nodes,weights=np.polynomial.legendre.leggauss(order)
    load=np.zeros(len(r)); all_breaks=np.unique(np.concatenate([p.r for p in profiles.values()]))
    factor=2*math.pi*1e6*density.G_KPC_KMS2_MSUN/A0_V
    for i,(lo,hi) in enumerate(zip(r,r[1:])):
        breaks=np.r_[lo,all_breaks[(all_breaks>lo)&(all_breaks<hi)],hi]
        for a,b in zip(breaks,breaks[1:]):
            x=(a+b)/2+(b-a)*nodes/2
            sigma=sum(p.sigma(x) for p in profiles.values())
            q=factor*(b-a)/2*weights*x*sigma
            load[i]+=np.sum(q*(hi-x)/(hi-lo)); load[i+1]+=np.sum(q*(x-lo)/(hi-lo))
    return load

def minres(A,b,seed,tolerance,cap=600):
    """M=None, shift0; accepts only original-denominator true residual."""
    x=seed.copy();norm=float(np.linalg.norm(b));checks=[];it=0
    def close(reason):
        error=None
        if math.isfinite(norm) and norm>0 and np.all(np.isfinite(b)) and np.all(np.isfinite(x)):
            action=A(x)
            if np.all(np.isfinite(action)):error=finite(float(np.linalg.norm(b-action)/norm))
        return x,dict(ok=error is not None and error<=tolerance,error=error,
                      iterations=it,reason=reason,true_checks=checks)
    if norm==0:
        if np.all(b==0):return np.zeros_like(b),dict(ok=True,error=0.,iterations=0,reason='zero_rhs',true_checks=[])
        return close('underflowed_nonzero_rhs_norm')
    if not math.isfinite(norm) or not np.all(np.isfinite(x)):return close('nonfinite_initial_state')
    action=A(x)
    if not np.all(np.isfinite(action)):return close('nonfinite_seed_action')
    r=b-action;beta=float(np.linalg.norm(r))
    initial=finite(beta/norm);checks.append(dict(iteration=0,error=initial))
    if initial is not None and initial<=tolerance:return close('authenticated_seed_true_residual')
    if not math.isfinite(beta) or beta<=0:return close('initial_norm_breakdown')
    v=r/beta;previous_v=np.zeros_like(v)
    older_w=np.zeros_like(v);previous_w=np.zeros_like(v)
    cs=-1.;sn=0.;dbar=eps=0.;phibar=beta
    for it in range(1,cap+1):
        if not np.all(np.isfinite(v)):return close('nonfinite_lanczos_direction')
        q=A(v)
        if not np.all(np.isfinite(q)):return close('nonfinite_lanczos_action')
        q-=beta*previous_v;alpha=float(np.sum(v*q));q-=alpha*v
        next_beta=float(np.linalg.norm(q))
        oldeps=eps;delta=cs*dbar+sn*alpha;gbar=sn*dbar-cs*alpha
        eps=sn*next_beta;dbar=-cs*next_beta;gamma=math.hypot(gbar,next_beta)
        if not all(math.isfinite(t) for t in (alpha,next_beta,delta,gbar,eps,dbar,gamma)) or gamma==0:
            return close('givens_or_lanczos_breakdown')
        cs=gbar/gamma;sn=next_beta/gamma;phi=cs*phibar;phibar=sn*phibar
        w=(v-oldeps*older_w-delta*previous_w)/gamma
        x+=phi*w
        if not np.all(np.isfinite(x)) or not np.all(np.isfinite(w)):return close('nonfinite_linear_state')
        if abs(phibar)/norm<=tolerance or it%25==0 or next_beta==0:
            action=A(x)
            error=finite(float(np.linalg.norm(b-action)/norm)) if np.all(np.isfinite(action)) else None
            checks.append(dict(iteration=it,error=error))
            if error is not None and error<=tolerance:return close('true_residual')
        if next_beta==0:return close('lanczos_terminal_true_residual_failed')
        older_w=previous_w;previous_w=w;previous_v=v;v=q/next_beta;beta=next_beta
    return close('iteration_allowance')


def source_profiles():
    rows=[]
    for line in (BASE/'sparc_official_NGC3198_rotmod.dat').read_text().splitlines():
        if line.strip() and not line.startswith('#'):
            f=line.split();rows.append((float(f[0]),float(f[6])))
    photo=np.array(rows,float);RAW['source_photometry_only']=photo.copy()
    assert photo.shape==(43,2) and np.all(np.diff(photo[:,0])>0) and np.all(photo>=0)
    k=np.flatnonzero(photo[:,0]==24.03);assert len(k)==1 and photo[k[0],1]==.28
    prefix=photo[:k[0]+1];p=density.profiles(False,False)
    p['stars']=density.Profile(prefix[:,0],.5*prefix[:,1],3.14)
    return p,photo
def circular_sheet(r,psi,profiles,order):
    nodes,weights=np.polynomial.legendre.leggauss(order);load=np.zeros(len(r));scalar=np.zeros(len(r));samples=[]
    slopes=np.diff(psi)/np.diff(r);breaks_all=np.unique(np.concatenate([p.r for p in profiles.values()]))
    factor=2*math.pi*1e6*density.G_KPC_KMS2_MSUN/A0_V
    for i,(lo,hi) in enumerate(zip(r,r[1:])):
        cuts=np.r_[lo,breaks_all[(breaks_all>lo)&(breaks_all<hi)],hi]
        for l,h in zip(cuts,cuts[1:]):
            x=(l+h)/2+(h-l)*nodes/2;sig=sum(p.sigma(x) for p in profiles.values())
            ph=B*(psi[i]+(x-lo)*slopes[i]);u=x*B*slopes[i]
            assert np.all(np.isfinite(u)) and np.all((u>=0)&(u<.5))
            v=np.sqrt(u/(1-u));gamma=1/np.sqrt(1-v*v);rho=x*np.exp(-ph)
            weight=factor*(h-l)/2*weights*x*sig;odd=B*weight*rho*gamma*v
            for n,ix in (((hi-x)/(hi-lo),i),((x-lo)/(hi-lo),i+1)):
                load[ix]+=np.sum(odd*n);scalar[ix]+=np.sum(weight*n)
            samples.append(np.stack([x,sig,ph,u,v,gamma,rho,weight,odd],axis=1))
            RAW['current_source_samples']=samples[-1].copy()
    return load,scalar,np.concatenate(samples)
def load_source(r,psi,profiles,parent_rhs):
    slopes=np.diff(psi)/np.diff(r);mass=np.array([sum(float(p.integral(lo,hi)) for p in profiles.values()) for lo,hi in zip(r,r[1:])])
    ends=B*slopes[:,None]*np.stack([r[:-1],r[1:]],axis=1);support=mass>0
    RAW['source_cell_mass']=mass;RAW['source_cell_u_endpoints']=ends;RAW['source_supported_cells']=support
    admitted=np.all(np.isfinite(ends)) and np.all((ends[support]>=0)&(ends[support]<.5))
    if not admitted:return None,dict(admitted=False,reason='At least one entire supported Q1 cell has negative or nontimelike circular force; no source clipping.',negative_cells=np.flatnonzero(support&np.any(ends<0,axis=1)).tolist(),nontimelike_cells=np.flatnonzero(support&np.any(ends>=.5,axis=1)).tolist())
    lo,old16,s16=circular_sheet(r,psi,profiles,16);RAW['ordinary_load16']=lo;RAW['source_samples16']=s16;RAW['scalar_load16']=old16
    hi,old32,s32=circular_sheet(r,psi,profiles,32);RAW['ordinary_load32']=hi;RAW['source_samples32']=s32;RAW['scalar_load32']=old32
    masked16=old16.copy();masked16[-1]=0.;RAW['masked_even_load16']=masked16
    check('unchanged_even_source',masked16,parent_rhs[0,:,0],envelope=float(np.sum(abs(old16))))
    check('scalar_sheet_16_32',old16,old32,envelope=float(np.sum(abs(old32))))
    check('circular_sheet_16_32',lo,hi,envelope=float(np.sum(abs(hi))))
    factor=2*math.pi*1e6*density.G_KPC_KMS2_MSUN/A0_V
    check('one_G_unit_identity',np.array(B*factor),np.array(2*math.pi*1e6*density.G_KPC_KMS2_MSUN/(LIGHT/1000)**2))
    return lo,dict(admitted=True,reason='Entire supported cell admits the leading conformal timelike circular branch.',order=16,reference_order=32,load_nonnegative=bool(np.all(lo>=0)),source_feedback=False)

class Odd:
    def __init__(self,r,z,x,xi,w,fixed,sigma):
        self.r,self.z,self.xi,self.w,self.sigma=r,z,xi,w,sigma;self.phi=B*x[0];self.shape=(2,len(r),len(z));self.alpha=KB/C
        self.mask=np.ones(self.shape,bool);self.mask[:,-1,:]=False;self.mask[:,:,-1]=False;self.mask[:,0,:]=False
        # beta[0]=beta[1] is an axis-even Q1 trial constraint; chi[0]=0.
        eta=fixed['Hunit']/(1000*(LIGHT/1000));self.omega=sigma*xi*eta
        ep=1e-5;norm=1/ep-math.log1p(1/ep);target=.5*ep*norm*fixed['d0'];s=target
        for _ in range(12):
            q=math.sqrt(1+ep*s/(1+s));dq=ep/(2*q*(1+s)**2);s-=(s*q-target)/(q+s*dq)
        self.qbar=math.sqrt(1+ep*s/(1+s));self.Qbar=fixed['Q0_over_Hstar']*eta*self.qbar
        u0=ep*s/(1+s);u=u0+(1+u0)*np.expm1(-2*B*x[0]);RAW['held_nodal_q2_minus1']=u
        assert np.all(np.isfinite(u)) and np.all((u>0)&(u<ep))
        self.quad=[];self.raw={};diag=np.zeros(self.shape)
        for iq,(rr,vol,shapes) in enumerate(shape_quadrature(r,z)):
            val,gr,gz=interpolate(x,shapes);ph=B*val[0];ef=np.exp(ph);em=np.exp(-ph);volume=vol*em**2
            a=ef[...,None]*B*np.stack([gr[0],gz[0]],axis=-1)
            b=-a.copy();b[...,0]+=ef/rr;d=b-a
            zh=B*ef[None,...,None]*np.stack([val[1::2],val[2::2]],axis=-1)/np.sqrt(w)[:,None,None,None]
            Z=np.sum(w[:,None,None,None]*zh,axis=0);T=self.alpha*a+Z
            I=np.einsum('j,j...a,j...b->...ab',w/self.omega**2,zh,zh)
            bz=np.sum(zh*b[None,...,:],axis=-1);dz=np.sum(zh*d[None,...,:],axis=-1)
            E=ELL**2*np.sum(w[:,None,None,None]*bz[...,None]*zh,axis=0);V=T+E
            At=np.eye(2)/(2*C)+I/4;k=-V+np.einsum('...ab,...b->...a',I,d)/2
            cc=-2*np.sum(V*d,axis=-1)-self.Qbar**2*em**2+np.einsum('...a,...ab,...b->...',d,I,d)
            rho=rr*em
            data=(volume,shapes,ef,rho,a,b,d,zh,T,bz,dz,At,k,cc)
            self.quad.append(data)
            for name,v in dict(rr=rr,volume=volume,expPhi=ef,rho=rho,a=a,b=b,d=d,zh=zh,Z=Z,T=T,I=I,E=E,At=At,k=k,cchi=cc,bz=bz,dz=dz).items():
                self.raw[f'q{iq}_{name}']=v.copy();RAW[f'q{iq}_{name}']=v.copy()
            for n,nr,nz,i,j in shapes:
                br=np.broadcast_to(nr,rho.shape).copy();bztest=np.broadcast_to(nz,rho.shape).copy()
                if i==0:br[0]=0;bztest[0]=0
                else:br[0]=0;bztest[0]=(1 if j else -1)/np.diff(z)
                gb=rho[...,None]*np.stack([br,bztest],axis=-1)
                db=volume*np.einsum('...a,...ab,...b->...',gb,At,gb)
                wc=ef[...,None]*np.stack([np.broadcast_to(nr,rho.shape),np.broadcast_to(nz,rho.shape)],axis=-1)+n*d
                dc=volume*(cc*n*n-self.alpha*np.sum(wc*wc,axis=-1))
                diag[0,i:len(r)-1+i,j:len(z)-1+j]+=db
                diag[1,i:len(r)-1+i,j:len(z)-1+j]+=dc
        diag[~self.mask]=0;assert np.all(np.isfinite(diag));self.signed_diagonal=diag
        floor=max(1e-30,float(np.max(abs(diag)))*1e-14);self.pre=np.maximum(abs(diag),floor);self.pre[~self.mask]=1
        self.preconditioner_floor=floor;assert np.all(np.isfinite(self.pre)) and np.all(self.pre>0)
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
    def energies(self,y):
        v=self.lift(y);terms=np.zeros(7);folded=0.
        for volume,shapes,ef,rho,a,b,d,zh,T,bz,dz,At,k,cc in self.quad:
            val,gr,gz=interpolate(v,shapes);chi=val[1];t=rho[...,None]*np.stack([gr[0],gz[0]],axis=-1)
            W=ef[...,None]*np.stack([gr[1],gz[1]],axis=-1)+chi[...,None]*d
            tz=np.sum(zh*t[None,...,:],axis=-1);vj=chi[None,...]*dz+tz/2
            Q2=self.Qbar**2/ef**2
            literal=[np.sum(t*t,axis=-1)/(4*C),-self.alpha*np.sum(W*W,axis=-1)/2,
               -chi**2*np.sum(T*d,axis=-1),-chi*np.sum(T*t,axis=-1),-Q2*chi**2/2,
               np.sum(self.w[:,None,None]*vj*vj/(2*self.omega[:,None,None]**2),axis=0),
               -ELL**2*np.sum(self.w[:,None,None]*bz*(chi[None,...]**2*dz+chi[None,...]*tz),axis=0)]
            terms+=np.array([np.sum(volume*l) for l in literal])
            f=.5*np.einsum('...a,...ab,...b->...',t,At,t)+chi*np.sum(k*t,axis=-1)+.5*cc*chi**2-.5*self.alpha*np.sum(W*W,axis=-1)
            folded+=float(np.sum(volume*f))
        return terms,folded
    def controls(self):
        R=self.r[:,None]/self.r[-1];Z=self.z[None,:]/self.z[-1]
        y=np.stack([np.broadcast_to((1-R)*(1-Z)*(1+R*R),self.shape[1:]),np.broadcast_to(R*(1-R)*(1-Z),self.shape[1:])]);y[~self.mask]=0
        q=np.stack([np.broadcast_to((1-R)*(1-Z)*(1+Z),self.shape[1:]),np.broadcast_to(R*(1-R)*(1-Z)*(1+R+Z),self.shape[1:])]);q[~self.mask]=0
        ay=self.action(y);aq=self.action(q);terms,fold=self.energies(y);prefix='sigma_'+str(self.sigma)
        RAW.update(manufactured_y=y,manufactured_q=q,manufactured_Hy=ay,manufactured_Hq=aq,literal_action_terms=terms)
        env=float(np.sum(abs(y*aq))+np.sum(abs(q*ay)));check(prefix+'_symmetry',np.array(np.sum(y*aq)),np.array(np.sum(q*ay)),envelope=env)
        env=float(np.sum(abs(terms)));check(prefix+'_literal_folded',np.array(np.sum(terms)),np.array(fold),envelope=env)
        env=max(env,float(np.sum(abs(y*ay))));check(prefix+'_gradient_energy',np.array(np.sum(y*ay)),np.array(2*fold),envelope=env)

def solver_controls():
    cases=[('SPD',[[4.,1.],[1.,3.]],[1.,2.],[.3,-.2],[1/11,7/11]),('INDEFINITE',[[2.,3.],[3.,-1.]],[1.,2.],[0.,0.],[7/11,-1/11]),('COMPATIBLE_SINGULAR',[[1.,1.],[1.,1.]],[2.,2.],[.2,.3],[.95,1.05]),('INCOMPATIBLE_SINGULAR',[[1.,0.],[0.,0.]],[1.,1.],[0.,0.],None)]
    arrays={};info=[]
    for name,mat,b,seed,exact in cases:
        mat=np.array(mat);b=np.array(b);seed=np.array(seed);sol,lin=minres(lambda y:mat@y,b,seed,1e-12,20)
        arrays.update({name+'_matrix':mat,name+'_rhs':b,name+'_seed':seed,name+'_partial':sol})
        if exact is None:check('MINRES_'+name,np.array(int(not lin['ok'] and lin['error'] is not None and lin['error']>1e-10)),np.array(1),tol=0.)
        else:check('MINRES_'+name,sol,np.array(exact),tol=2e-12)
        info.append(dict(name=name,linear=lin))
    arrays.update({k:v.copy() for k,v in RAW.items() if k.startswith('control_')})
    return checkpoint('SOLVER_CONTROLS',arrays,dict(kind='inherited_known_MINRES_controls',rows=info,controls=list(CHECKS)))

def orbit_rows(r,psi,odd):
    obs=[]
    for line in (BASE/'sparc_official_NGC3198_rotmod.dat').read_text().splitlines():
        if line.strip() and not line.startswith('#'):obs.append([float(v) for v in line.split()[:3]])
    beta=odd[0,:,0];gs=np.diff(psi)/np.diff(r);bs=np.diff(beta)/np.diff(r);rows=[];raw=[]
    for R,V,E in obs:
        hits=np.flatnonzero(r==R)
        inds=[int(hits[0])-1,int(hits[0])] if len(hits) else [int(np.searchsorted(r,R)-1)]*2
        ph=B*float(np.interp(R,r,psi));bet=float(np.interp(R,r,beta));sides=[]
        for i in inds:
            assert 0<=i<len(gs);D=B*gs[i];A=1/R-D;Bs=R*math.exp(-2*ph)*bs[i];disc=Bs*Bs+4*A*D
            plus=minus=None
            if disc>=0 and A!=0:
                root=math.sqrt(disc);plus=(-Bs+root)/(2*A);minus=(-Bs-root)/(2*A)
                if D>0 and root+Bs>0:plus=2*D/(root+Bs)
            timelike=plus is not None and math.isfinite(plus) and 0<=plus<1
            omega=None if not timelike else LIGHT/KPC*(math.exp(2*ph)*plus/R-bet)
            lead2=R*D/(1-R*D) if 1-R*D!=0 else None
            sides.append(dict(cell=i,radial_Phi_derivative=finite(D),radial_beta_star_derivative=finite(bs[i]),discriminant=finite(disc),prograde_v_over_c=finite(plus) if plus is not None else None,retrograde_v_over_c=finite(minus) if minus is not None else None,constructed_metric_timelike=bool(timelike),Omega_rad_per_second=finite(omega) if omega is not None else None,velocity_kms=None if not timelike else plus*LIGHT/1000,leading_v2_over_c2=finite(lead2) if lead2 is not None else None))
            raw.append([R,ph,bet,A,Bs,D,disc,0. if plus is None else plus,0. if minus is None else minus,float(plus is not None),float(timelike)])
        rows.append(dict(R_kpc=R,Vobs_kms=V,error_kms=E,exact_mesh_node=bool(len(hits)),left=sides[0],right=sides[1],orbital_force_qualified=False))
    assert len(rows)==43
    return rows,np.array(raw)
def solve_arm(model,load,psi):
    begin=len(CHECKS);model.controls();rhs=np.zeros(model.shape);rhs[0,:,0]=-load;rhs=model.restrict(rhs)
    coeff=dict(RAW,omega_star=model.omega.copy(),xi=model.xi.copy(),weights=model.w.copy(),signed_diagonal=model.signed_diagonal.copy(),positive_numerical_preconditioner=model.pre.copy(),rhs=rhs.copy(),free_mask=model.mask.copy())
    cp=checkpoint('COEFFICIENTS',coeff,dict(kind='signed_odd_quadratic_action',sigma=model.sigma,controls=CHECKS[begin:],preconditioner_floor=model.preconditioner_floor,physical_regularization=False))
    if not all(c['passed'] for c in CHECKS[begin:]):
        refused=checkpoint('CONTROL_REFUSAL',dict(RAW),dict(kind='arithmetic_refusal_without_odd_solve',sigma=model.sigma,controls=CHECKS[begin:],coefficient_checkpoint=cp['file']))
        return dict(sigma=model.sigma,status='ARITHMETIC_FAILED',original_residual=None,coefficient_checkpoint=cp,final_checkpoint=refused,rows=[],smallness=None,qualification=FLAGS)
    root=np.sqrt(model.pre);white_rhs=rhs/root;seed=np.zeros(model.shape)
    def A(y):
        RAW['latest_whitened_direction']=y.copy();physical=y/root;RAW['latest_physical_direction']=physical.copy()
        if not np.all(np.isfinite(physical)):return np.full_like(y,np.nan)
        action=model.action(physical);RAW['latest_original_H_action']=action.copy();return action/root
    sol,lin=minres(A,white_rhs,seed,TRUE_TOL,CAP);physical=sol/root;RAW['linear_partial']=physical.copy()
    action=model.action(physical);res=action-rhs;RAW['original_H_action']=action;RAW['original_residual']=res
    norm=float(np.linalg.norm(rhs));er=0. if np.all(rhs==0) and np.all(res==0) else (None if not math.isfinite(norm) or norm<=0 else finite(float(np.linalg.norm(res)/norm)))
    accepted=bool(lin['ok'] and er is not None and er<=TRUE_TOL and np.all(np.isfinite(physical)))
    out=model.lift(physical);speed=model.r[:,None]*np.exp(-2*model.phi)*out[0]
    rows,orbit=orbit_rows(model.r,psi,out) if np.all(np.isfinite(out)) else ([],np.empty((0,11)))
    arrays=dict(unknown_coordinates=physical,physical_beta_chi=out,whitened_solution=sol,whitened_rhs=white_rhs,zero_seed=seed,original_rhs=rhs,original_H_action=action,original_residual=res,coordinate_shift_speed_over_c=speed,linear_phase_spatial_current_over_g_times_L0=-model.Qbar*np.exp(-model.phi)*out[1],constructed_orbit_operands=orbit)
    arrays.update({k:v.copy() for k,v in RAW.items() if k.startswith('latest_')})
    smallness=dict(max_abs_chi=finite(float(np.max(abs(out[1])))),max_abs_shift_speed_over_c=finite(float(np.max(abs(speed)))))
    final=checkpoint('FINAL',arrays,dict(kind='all_signed_odd_partial_and_readouts',sigma=model.sigma,status='LINEAR_PASS' if accepted else 'LINEAR_FAILED',linear=lin,original_residual=er,coefficient_checkpoint=cp['file'],rows=rows,smallness=smallness,smallness_qualified=False,source_feedback=False))
    return dict(sigma=model.sigma,status='LINEAR_PASS' if accepted else 'LINEAR_FAILED',linear=lin,original_residual=er,coefficient_checkpoint=cp,final_checkpoint=final,rows=rows,smallness=final['metadata']['smallness'],qualification=FLAGS)

def main():
    global np,density,INPUTS,OWNER,PARENT_SHORT,RAW
    ap=argparse.ArgumentParser();ap.add_argument('--root-run',action='store_true');args=ap.parse_args()
    assert args.root_run and not AUTHOR_DRAFT and len(PROTOCOL_SHA)==64,'Prospective guarded source is unlaunchable.'
    assert not list(BASE.glob(STEM+'_*')),'Unused namespace required; no automatic resume/retry.'
    INPUTS=resolve_inputs();binding,PARENT_SHORT=parent_binding()
    OWNER=dict(owner='root',pid=os.getpid(),started=now(),source_sha256=sha(__file__))
    cases=[];source=None;source_cp=None
    try:
        publish(STEM+'_OWNER_START.json',OWNER)
        publish(STEM+'_MANIFEST.json',dict(owner=OWNER,input_sha256=INPUTS,parent=PARENT_SHORT,sigmas=SIGMAS,configuration=dict(MINRES_cap=CAP,true_original_tolerance=TRUE_TOL,arithmetic_tolerance=ARITH_TOL,axis_beta='beta0=beta1 Q1 even trace',axis_chi=0,outer_beta_chi=0,chi_sheet='action conormal; no ordinary U load'),qualification=FLAGS))
        import numpy as _np
        np=_np
        spec=importlib.util.spec_from_file_location('owned_density_math',BASE/'galaxy_density.py');density=importlib.util.module_from_spec(spec);spec.loader.exec_module(density)
        data={}
        with np.load(BASE/binding['file'],allow_pickle=False) as z:
            assert json.loads(str(z['metadata']))==binding['metadata'] and set(z.files)==set(binding['metadata']['schema'])|{'metadata'}
            for name,s in binding['metadata']['schema'].items():
                a=z[name];assert s==dict(shape=list(a.shape),dtype=str(a.dtype),finite=bool(np.all(np.isfinite(a))))
            for name in ('final_state','final_rhs','final_residual','final_pre','final_midplane_psi','final_cell_slopes'):data[name]=z[name].copy()
        r=np.array(binding['metadata']['identity']['r_kpc']);z=np.array(binding['metadata']['identity']['z_kpc']);x=data['final_state'];psi=data['final_midplane_psi'];RAW.update(data);RAW['r_kpc']=r;RAW['z_kpc']=z
        assert x.shape==(65,87,45) and np.array_equal(psi,x[0,:,0]) and np.array_equal(data['final_cell_slopes'],np.diff(psi)/np.diff(r))
        assert np.all(x[:,-1]==0) and np.all(x[:,:,-1]==0) and np.all(x[1::2,0]==0) and np.all(x[2::2,:,0]==0)
        xi,ww=np.polynomial.legendre.leggauss(32);xi=(xi+1)/2;w=ww*xi;RAW.update(xi=xi,weights=w)
        assert np.all(w>0);check('actual_native_weight_sum',np.array(np.sum(w)),np.array(1.))
        checkpoint('INPUT',dict(RAW),dict(kind='unchanged_authentic_even_state',controls=list(CHECKS),no_even_updates=True))
        RAW={};profiles,photo=source_profiles();load,source=load_source(r,psi,profiles,data['final_rhs'])
        source_cp=checkpoint('CIRCULAR_SOURCE',dict(RAW),dict(kind='predicted_circular_source_entire_support',source=source,controls=list(CHECKS),uses_observed_velocity=False))
        solver_controls()
        if load is None:
            cases=[dict(sigma=s,status='CIRCULAR_SOURCE_REFUSED',reason=source['reason'],qualification=FLAGS) for s in SIGMAS]
        else:
            assert all(c['passed'] for c in CHECKS),'Arithmetic implementation control refused.'
            for sigma in SIGMAS:
                CONTEXT.clear();CONTEXT.update(sigma=sigma,stage='signed_odd_linear_solve');RAW={}
                model=Odd(r,z,x,xi,w,PARENT_SHORT['source_identity']['inherited_fixed'],sigma)
                cases.append(solve_arm(model,load,psi));publish(STEM+'_SIGMA_'+str(sigma)+'_CASE.json',cases[-1])
        expected=5+4+3*4
        assert len(CHECKS)==expected if load is not None else len(CHECKS)==5
        status='CONDITIONAL_LINEAR_PASS' if load is not None and all(c['passed'] for c in CHECKS) and all(c['status']=='LINEAR_PASS' for c in cases) else 'CONDITIONAL_NUMERICAL_FAILED'
        result=dict(owner=OWNER,status=status,parent=PARENT_SHORT,source=source,source_checkpoint=source_cp,cases=cases,controls=CHECKS,expected_full_arithmetic_census=expected,checkpoints=RECORDS,qualification=FLAGS)
        recheck();rh=publish(STEM+'_RESULT.json',result)
        report=(f'# {STEM}\n\n{status}. Four predeclared temporal benchmarks; unchanged even fields and predicted cold circular source.\n\n'+''.join(f'- sigma={c["sigma"]}: {c["status"]}; original residual={c.get("original_residual")}\n' for c in cases)+'\nNo physical inertia, exterior, full metric, stability, force or observational qualification.\n').encode()
        rp=BASE/(STEM+'_REPORT.md')
        with rp.open('xb') as f:f.write(report);f.flush();os.fsync(f.fileno())
        rp.chmod(0o444);assert rp.read_bytes()==report;CREATED[rp.name]=sha(rp)
        recheck();receipt=dict(owner=OWNER,status='CLOSED',closed=now(),input_sha256=INPUTS,output_sha256=dict(CREATED),result_sha256=rh,qualification=FLAGS)
        publish(STEM+'_RECEIPT.json',receipt);recheck();assert json.loads((BASE/(STEM+'_RECEIPT.json')).read_text())==receipt
        print(json.dumps(dict(status=status,cases=len(cases),controls=len(CHECKS),result_sha256=rh,receipt_sha256=sha(BASE/(STEM+'_RECEIPT.json'))),sort_keys=True))
        return 0 if status=='CONDITIONAL_LINEAR_PASS' else 3
    except BaseException:
        failure=traceback.format_exc();prior=BASE/(STEM+'_RECEIPT.json');prior_sha=sha(prior) if prior.exists() else None
        if np is not None and RAW:checkpoint('ERROR_RAW',dict(RAW),dict(kind='unaccepted_progressive_odd_operands',context=CONTEXT,traceback=failure))
        for p in BASE.glob(STEM+'_*'):
            if p.is_file():p.chmod(0o444);CREATED[p.name]=sha(p)
        recheck();eh=publish(STEM+'_ERROR.json',dict(owner=OWNER,failed=now(),context=CONTEXT,traceback=failure,checkpoints=RECORDS,controls=CHECKS,preserved_outputs=dict(CREATED),existing_receipt_sha256=prior_sha,qualification=FLAGS))
        if prior_sha is None:
            rc=dict(owner=OWNER,status='CLOSED_ERROR',closed=now(),input_sha256=INPUTS,output_sha256=dict(CREATED),error_sha256=eh,qualification=FLAGS)
            publish(STEM+'_RECEIPT.json',rc);recheck();assert json.loads(prior.read_text())==rc
        else:recheck();assert sha(prior)==prior_sha
        raise
if __name__=='__main__':raise SystemExit(main())

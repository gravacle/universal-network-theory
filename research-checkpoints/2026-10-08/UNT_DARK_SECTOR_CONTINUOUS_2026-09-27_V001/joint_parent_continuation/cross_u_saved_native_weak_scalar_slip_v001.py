"""Guarded saved-native weak scalar-slip potential only; root evaluates geometry."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,ast,hashlib,importlib,json,math,os,time,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_SAVED_NATIVE_WEAK_SCALAR_SLIP_V001'
PARENT='CROSS_U_NGC3198_SAVED_WEAK_STRESS_METER_V002'
AUTHOR_GUARD=False
PROTOCOL_SHA='f4becddcf5de1777ca847d0fd2b05aad9181d0e819dc71942213389687302b91'
PINS={'CROSS_U_STATIC_HILBERT_STRESS_AND_LEADING_LENSING_INTERFACE_V001.md': '6844c982d0c017350d85731f3f58bf8b4167c860ee52f8bdd238ceef1fdcd68b', 'CROSS_U_STATIONARY_AXISYMMETRIC_ORBIT_AND_ORDINARY_MATTER_REGISTRATION_V001.md': 'b962a4e6cc2583033f66b5194b50d47e1553456feda4147624d9f246bc86ebd5', 'cross_u_ngc3198_saved_weak_stress_meter_v002.py': 'af1c2f0826380c714220e090f755fc20773c76804f2b0952e1f6400f9cd6eee6', 'CROSS_U_NGC3198_SAVED_WEAK_STRESS_METER_V002.md': 'be14d5467450d17f0cd0d5b2b310d1a21db1cbcb2890859807d7a27ccd101202', 'CROSS_U_NGC3198_SAVED_WEAK_STRESS_METER_V002_RESULT.json': 'd8d7de0d9f2faf7545c400230d116ad1dc2fe3488471982e3c1c01d3aac582c1', 'CROSS_U_NGC3198_SAVED_WEAK_STRESS_METER_V002_RECEIPT.json': '12d150e67f3da4f36714e52480d5c7e90f7b7b0fd3dac919787e021503312018', 'CROSS_U_NGC3198_SAVED_WEAK_STRESS_METER_V002_MANIFEST.json': 'fe77e5227bac083d885804fd72fdc2c43cf440e77ef56599340241641453e0f3', 'CROSS_U_NGC3198_SAVED_WEAK_STRESS_METER_V002_000_INPUT.npz': '9ace843429b1dce8341eec4f7cbf36be3ebbca47dfedac633f71976ecffa0b16', 'CROSS_U_NGC3198_SAVED_WEAK_STRESS_METER_V002_000_INPUT.npz.COMMIT.json': 'a547ff066a0b54227a65ab0f0013c6a9c5703e10b04e82024df050c3c60cfd08', 'CROSS_U_NGC3198_SAVED_WEAK_STRESS_METER_V002_001_VOLUME_Q2.npz': '727666662662b047b046027c069e92482d70a8149fd3b53108a4cdbfafbfe525', 'CROSS_U_NGC3198_SAVED_WEAK_STRESS_METER_V002_001_VOLUME_Q2.npz.COMMIT.json': 'a9b83507eeb2907f938cb788a2c7816658a731193c81112475ea9d4bd7702487', 'CROSS_U_NGC3198_SAVED_WEAK_STRESS_METER_V002_002_FACES_Q2.npz': 'da9f2914182f63241c66ff1f94896d08a71d905db942cfaa1a4845eabd76afb2', 'CROSS_U_NGC3198_SAVED_WEAK_STRESS_METER_V002_002_FACES_Q2.npz.COMMIT.json': 'cac42094fe9be2e9a5c6718501e619cc2d519ecec41c8dde4c2b0cd0c32c89d8', 'CROSS_U_NGC3198_SAVED_WEAK_STRESS_METER_V002_003_VOLUME_Q3.npz': '419d40eff2dc55355bce96c1a2c94ed32d9f5c8a4ffd023476a13ebcfdab9ce7', 'CROSS_U_NGC3198_SAVED_WEAK_STRESS_METER_V002_003_VOLUME_Q3.npz.COMMIT.json': '528228c9c0ef61b890691f1edf8e5b280c96f6b5e107f8a387dbd91e70ddb73a', 'CROSS_U_NGC3198_SAVED_WEAK_STRESS_METER_V002_004_FACES_Q3.npz': 'a845b37193689a0e56a03956a2a2e6a2d4b49762b901f3444188894b68360c93', 'CROSS_U_NGC3198_SAVED_WEAK_STRESS_METER_V002_004_FACES_Q3.npz.COMMIT.json': 'e24769f50d93d5510ad6ebf9965f78118fca63bfaa22e25f9a113176a9a7cb91', 'CROSS_U_NGC3198_SAVED_WEAK_STRESS_METER_V002_005_COMPARISONS.npz': 'efa5747091ad81a6d492e46f51a9a020e4726809e0cb081143207693f104e387', 'CROSS_U_NGC3198_SAVED_WEAK_STRESS_METER_V002_005_COMPARISONS.npz.COMMIT.json': '14d2ed4d65e36ed134d3ae248d7ac7192104c925f499969f22dc55e48a6c2190'}
TARGETS=(.32,2.89,5.78,6.43,10.04,14.05,20.05,28.16,44.08)
ORDERS=(8,16,32)
BREAKS=(0.,1e-5,5e-5,2e-4,.001,.005,.025,.1,.4,1.,math.pi)
C,ELL,BLOCK=1.98,.1,128
ARITH_TOL,FD_TOL,ANGLE_TOL,FLOOR=2e-11,1e-7,1e-6,1e-30
FLAGS={k:False for k in ('full_metric','lensing','force_correction','continuum','refinement','stability','exterior_match','homogeneous_metric','ordinary_stress','background_Einstein','TT_metric','shift_metric','physical_stress_bound','parameter_adoption')}
np=None;OWNER=None;INPUTS={};CREATED={};RECORDS=[];RAW={};CONTEXT={};CONTROLS=[];B0=None

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
def finite(x):return float(x) if math.isfinite(float(x)) else None

def canonical(v):
    if isinstance(v,dict):return {str(k):canonical(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [canonical(x) for x in v]
    if np is not None and isinstance(v,np.generic):return canonical(v.item())
    if v is None or type(v) in (str,bool,int):return v
    if type(v) is float:
        if not math.isfinite(v):raise ValueError('Nonfinite JSON scalar')
        return v
    raise TypeError(type(v).__name__)
def encode(v):return (json.dumps(canonical(v),sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()

def publish(n,v):
    raw=encode(v);p=BASE/n
    with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    p.chmod(0o444)
    if p.read_bytes()!=raw:raise ValueError('Exact JSON bytes')
    CREATED[n]=sha(p);return CREATED[n]

def inputs():
    out=dict(PINS,**{STEM+'.md':PROTOCOL_SHA});todo=[PARENT+'_RECEIPT.json'];done=set()
    while todo:
        n=todo.pop()
        if n in done:continue
        if sha(BASE/n)!=out[n]:raise ValueError('Receipt seal')
        done.add(n);rc=json.loads((BASE/n).read_text());ins=dict(rc.get('input_sha256',rc.get('pins',{})));outs=rc['output_sha256']
        if not outs:raise ValueError('Closed output map')
        mn=Path(n).name[:-len('_RECEIPT.json')]+'_MANIFEST.json';found=[k for k in outs if Path(k).name==mn]
        if found:
            if len(found)!=1:raise ValueError('Unique manifest')
            m=json.loads((BASE/found[0]).read_text())
            if 'manifest' in rc and rc['manifest']!=m:raise ValueError('Whole parent manifest')
            if 'manifest_sha256' in rc and rc['manifest_sha256']!=outs[found[0]]:raise ValueError('Manifest hash')
            for k,h in dict(m.get('input_sha256',m.get('inputs',{})),**m.get('inherited_input_sha256',{})).items():
                if k in ins and ins[k]!=h:raise ValueError('Inherited conflict')
                ins[k]=h
        for k,h in dict(ins,**outs).items():
            if k in out and out[k]!=h:raise ValueError('Seal conflict')
            out[k]=h
            if k.endswith('_RECEIPT.json') and k not in done:todo.append(k)
    for n,h in out.items():
        if len(h)!=64 or sha(BASE/n)!=h:raise ValueError('Actual admitted byte '+n)
    out[Path(__file__).name]=sha(__file__);return out

def authenticate():
    for n,h in INPUTS.items():
        if sha(BASE/n)!=h:raise ValueError('Changed input '+n)
    if OWNER is not None and sha(__file__)!=OWNER['source_sha256']:raise ValueError('Changed own source')

def parent():
    r=json.loads((BASE/(PARENT+'_RESULT.json')).read_text());rc=json.loads((BASE/(PARENT+'_RECEIPT.json')).read_text());m=json.loads((BASE/(PARENT+'_MANIFEST.json')).read_text())
    if rc['owner']!=r['owner'] or rc['owner']!=m['owner'] or rc['owner']['pid']!=73230 or rc['owner']['owner']!='root' or not rc['closed']>rc['owner']['started']:raise ValueError('Actual natural closure')
    if rc['status']!='CLOSED' or r['status']!='ARITHMETIC_PASS' or rc['result_sha256']!=PINS[PARENT+'_RESULT.json']:raise ValueError('Actual closed result')
    if rc['records']!=r['records'] or len(r['records'])!=6 or len(r['controls'])!=24 or not all(z['passed'] for z in r['controls']):raise ValueError('Actual completed meter')
    if any(r['physical_flags'].values()) or r['parent_case_copied_exactly']['identity']['case']!='E1em05_HI0_H20':raise ValueError('Original physical scope')
    if r['parent_case_copied_exactly']['identity']['eps']!=1e-5 or r['parent_case_copied_exactly']['identity']['grid_shape']!=[65,87,45]:raise ValueError('Exactly V006 coarse state')
    for rec in r['records']:
        if json.loads((BASE/rec['commit_file']).read_text())!={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}:raise ValueError('Exact full parent COMMIT')
        if INPUTS[rec['file']]!=rec['sha256'] or INPUTS[rec['commit_file']]!=rec['commit_sha256']:raise ValueError('Actual parent pair binding')
    return r

def read_parent(rec):
    arrays={}
    with np.load(BASE/rec['file'],allow_pickle=False) as z:
        if set(z.files)!=set(rec['metadata']['schema'])|{'metadata'}:raise ValueError('Entire saved parent dictionary')
        for n in rec['metadata']['schema']:arrays[n]=z[n].copy();RAW['admitted_'+Path(rec['file']).stem+'_'+n]=arrays[n].copy()
        if json.loads(str(z['metadata']))!=rec['metadata']:raise ValueError('Exact saved parent metadata')
    for n,v in arrays.items():
        if rec['metadata']['schema'][n]!=dict(shape=list(v.shape),dtype=str(v.dtype),finite=bool(np.all(np.isfinite(v)))):raise ValueError('Actual saved schema')
        if not np.all(np.isfinite(v)):raise ArithmeticError('Nonfinite admitted operand')
    return arrays

def checkpoint(tag,arrays,meta,failed=False):
    md=canonical(dict(owner=OWNER,context=dict(CONTEXT),metadata=meta,failed=failed,physical_flags=FLAGS,schema={k:dict(shape=list(v.shape),dtype=str(v.dtype),finite=bool(np.all(np.isfinite(v)))) for k,v in arrays.items()}))
    if not failed and any(not v['finite'] for v in md['schema'].values()):raise ArithmeticError('Nonfinite successful arrays')
    text=encode(md).decode();md=json.loads(text);p=BASE/f'{STEM}_{len(RECORDS):04d}_{tag}.npz'
    with p.open('xb') as f:np.savez_compressed(f,metadata=text,**arrays);f.flush();os.fsync(f.fileno())
    p.chmod(0o444);CREATED[p.name]=sha(p);rec=dict(payload=p.name,payload_sha256=CREATED[p.name],metadata=md)
    h=publish(p.stem+'_COMMIT.json',rec);rec=dict(rec,commit_file=p.stem+'_COMMIT.json',commit_sha256=h);RECORDS.append(rec);reread(rec,arrays);return rec

def reread(rec,arrays=None):
    if sha(BASE/rec['payload'])!=rec['payload_sha256'] or sha(BASE/rec['commit_file'])!=rec['commit_sha256']:raise ValueError('Own pair seals')
    if json.loads((BASE/rec['commit_file']).read_text())!={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}:raise ValueError('Whole own COMMIT')
    with np.load(BASE/rec['payload'],allow_pickle=False) as z:
        if set(z.files)!=set(rec['metadata']['schema'])|{'metadata'} or json.loads(str(z['metadata']))!=rec['metadata']:raise ValueError('Whole own dictionary')
        for n,d in rec['metadata']['schema'].items():
            v=z[n]
            if d!=dict(shape=list(v.shape),dtype=str(v.dtype),finite=bool(np.all(np.isfinite(v)))):raise ValueError('Exact own schema')
            if arrays is not None and not np.array_equal(v,arrays[n],equal_nan=True):raise ValueError('Immediate whole raw reread')

def close():
    authenticate()
    for n,h in CREATED.items():
        if sha(BASE/n)!=h:raise ValueError('Changed owned output')
    for rec in RECORDS:reread(rec)
    if {p.name for p in BASE.glob(STEM+'_*.npz')}!={z['payload'] for z in RECORDS} or {p.name for p in BASE.glob(STEM+'_*_COMMIT.json')}!={z['commit_file'] for z in RECORDS}:raise ValueError('Unregistered/orphan own pairs')
    if STEM+'_OWNER_START.json' in CREATED and json.loads((BASE/(STEM+'_OWNER_START.json')).read_text())!=OWNER:raise ValueError('Exact original owner')

def check(name,actual,expected,envelope,tol=ARITH_TOL):
    ix=len(CONTROLS);prefix=f'control_{ix:02d}_{name}_';a=np.asarray(actual);b=np.asarray(expected);e=np.asarray(envelope);RAW.update({prefix+'actual':a.copy(),prefix+'expected':b.copy(),prefix+'envelope':e.copy()})
    if a.shape!=b.shape or a.shape!=e.shape:raise ValueError('Control shapes')
    error=float(np.max(abs(a-b)/np.maximum(e,FLOOR)))
    CONTROLS.append(dict(name=name,error=finite(error),tolerance=tol,floor=FLOOR,passed=math.isfinite(error) and error<=tol))

def kernel(displacement):
    d=np.sqrt(np.sum(displacement*displacement,axis=-1));RAW['current_kernel_displacement']=displacement.copy();RAW['current_kernel_distance']=d.copy()
    if not np.all(np.isfinite(d)) or np.any(d<=0):raise ArithmeticError('Strictly positive finite Green distance')
    n=displacement/d[...,None];eye=np.eye(3);K=(n[..., :,None]*n[...,None,:]-eye/3)/d[...,None,None];D=np.empty(K.shape[:-2]+(3,3,3))
    for k in range(3):D[...,k,:,:]=(-eye[k,:,None]*n[...,None,:]-eye[k,None,:]*n[..., :,None]+3*n[...,k,None,None]*n[..., :,None]*n[...,None,:]-eye*n[...,k,None,None]/3)/d[...,None,None]**2
    RAW.update(current_kernel_K=K.copy(),current_kernel_D=D.copy())
    if not np.all(np.isfinite(K)) or not np.all(np.isfinite(D)):raise ArithmeticError('Nonfinite Green tensor')
    return K,D,d

def source_kernel(R,Z,target,phi):
    shape=(len(R),len(phi));v=np.stack((target*np.cos(phi)[None,:]-R[:,None],np.broadcast_to(-target*np.sin(phi)[None,:],shape),np.broadcast_to(-Z[:,None],shape)),axis=-1)
    return kernel(v)

def implementation():
    r=np.asarray([[1.3,.7,.2],[-.4,1.1,.8],[.6,-.3,1.4]]);K,D,d=kernel(r);eye=np.eye(3)
    check('K_tracefree',np.trace(K,axis1=-2,axis2=-1),np.zeros(3),np.sum(abs(K),axis=(-2,-1)))
    check('DK_tracefree',np.trace(D,axis1=-2,axis2=-1),np.zeros((3,3)),np.sum(abs(D),axis=(-2,-1)))
    step=1e-6
    for k in range(3):
        direction=eye[k]*step;kp=kernel(r-direction)[0];km=kernel(r+direction)[0];fd=(kp-km)/(2*step);check('Cartesian_source_derivative_'+str(k),fd,D[:,k],abs(fd)+abs(D[:,k]),FD_TOL)
    R=np.asarray([3.1]);Z=np.asarray([.7]);target=2.4;phi=np.asarray([.8]);K,D,d=source_kernel(R,Z,target,phi);n=np.asarray([target*math.cos(.8)-3.1,-target*math.sin(.8),-.7])/d[0,0];v=np.asarray([-target*math.sin(.8),-target*math.cos(.8),0.]);dd=float(np.dot(n,v));dn=(v-n*dd)/d[0,0];partial=(dn[:,None]*n[None,:]+n[:,None]*dn[None,:])/d[0,0]-K[0,0]*dd/d[0,0];Omega=np.asarray([[0.,-1.,0.],[1.,0.,0.],[0.,0.,0.]]);coframe=(partial+Omega@K[0,0]-K[0,0]@Omega)/R[0]
    check('cylindrical_full_Dphi',coframe,D[0,0,1],abs(coframe)+abs(D[0,0,1]))
    for axis,label in ((2,'Z'),(1,'phi')):
        parity=np.eye(3);parity[axis,axis]=-1;rr=r@parity;kr,dr,_=kernel(rr);ke=np.einsum('ia,pab,jb->pij',parity,kernel(r)[0],parity);de=np.einsum('ka,ib,jc,pabc->pkij',parity,parity,parity,kernel(r)[1]);check('explicit_'+label+'_reflection',np.concatenate((kr.reshape(-1),dr.reshape(-1))),np.concatenate((ke.reshape(-1),de.reshape(-1))),np.concatenate(((abs(kr)+abs(ke)).reshape(-1),(abs(dr)+abs(de)).reshape(-1))))

def dataset(order,initial,volume,faces):
    nr,nz=len(initial['r'])-1,len(initial['z'])-1;data={};Rv=[];Zv=[];Tv=[];Fv=[];av=[];wv=[];Nv=[]
    for i in range(order):
        for j in range(order):
            tag=f'Q{order}_U{i}_V{j}_';R=np.broadcast_to(volume[tag+'rr'],(nr,nz)).copy();Z=np.broadcast_to(volume[tag+'zz'],(nr,nz)).copy();bulk=volume[tag+'bulk'];flux=volume[tag+'flux'];a=np.stack((volume[tag+'gr'][0],np.zeros((nr,nz)),volume[tag+'gz'][0]),axis=-1);measure=volume[tag+'measure'];RAW.update(current_dataset_R=R.copy(),current_dataset_Z=Z.copy(),current_dataset_bulk=bulk.copy(),current_dataset_flux=flux.copy(),current_dataset_acceleration=a.copy(),current_dataset_measure=measure.copy())
            if bulk.shape!=(nr,nz,3,3) or flux.shape!=(3,nr,nz,3,3) or np.any(R<=0) or np.any(Z<=0) or np.any(measure<=0):raise ValueError('Actual positive volume geometry/tensors')
            Rv.append(R.reshape(-1));Zv.append(Z.reshape(-1));Tv.append(bulk.reshape(-1,3,3));Fv.append(flux.reshape(3,-1,3,3));av.append(a.reshape(-1,3));wv.append(measure.reshape(-1));Nv.append(volume[tag+'N'].reshape(-1))
    data.update(R=np.asarray(Rv),Z=np.asarray(Zv),bulk=np.asarray(Tv),flux=np.asarray(Fv),a=np.asarray(av),measure=np.asarray(wv),N=np.asarray(Nv))
    parity=np.asarray([1.,-1.,1.]);bt=data['bulk']*parity[None,None,:,None]*parity[None,None,None,:];ft=data['flux']*parity[None,:,None,None,None]*parity[None,None,None,:,None]*parity[None,None,None,None,:];aa=np.concatenate(((data['bulk']-bt).reshape(-1),(data['flux']-ft).reshape(-1)));ee=np.concatenate(((abs(data['bulk'])+abs(bt)).reshape(-1),(abs(data['flux'])+abs(ft)).reshape(-1)));check('Q'+str(order)+'_source_meridional_parity',aa,np.zeros_like(aa),ee)
    ro=[];zo=[];fo=[];wo=[]
    for k in range(order):
        label=f'F{k}_';radial_z=volume[f'Q{order}_U0_V{k}_zz'][0];top_r=volume[f'Q{order}_U{k}_V0_rr'][:,0];radial_weight=faces[label+'radial_measure'][-1]*initial['r'][-1]/initial['r'][-2];top_weight=faces[label+'vertical_measure'][:,0]
        ro.extend((np.full(nz,initial['r'][-1]),top_r.copy()));zo.extend((radial_z.copy(),np.full(nr,initial['z'][-1])));fo.extend((faces[label+'radial_outer_flux'].copy(),faces[label+'vertical_outer_flux'].copy()));wo.extend((radial_weight.copy(),top_weight.copy()))
    data.update(outer_R=np.concatenate(ro),outer_Z=np.concatenate(zo),outer_flux=np.concatenate(fo),outer_measure=np.concatenate(wo));RAW.update({f'admitted_Q{order}_'+k:v.copy() for k,v in data.items()})
    if np.any(data['outer_Z']<=0) or np.any(data['outer_R']<=0) or np.any(data['outer_measure']<=0):raise ValueError('Actual outer port geometry')
    return data

def angular_rule(order):
    n,w=np.polynomial.legendre.leggauss(order);nodes=[];weights=[]
    for lo,hi in zip(BREAKS[:-1],BREAKS[1:]):nodes.append(lo+(hi-lo)*(n+1)/2);weights.append((hi-lo)*w/2)
    return np.concatenate(nodes),np.concatenate(weights)*4

def integrate(R,Z,bulk,flux,a,measure,target,phi,weight,outer=False):
    result=np.zeros((len(R),3));envelope=np.zeros_like(result)
    for start in range(0,len(R),BLOCK):
        stop=min(start+BLOCK,len(R));CONTEXT.update(chunk_start=start,chunk_end=stop,outer=outer);sl=slice(start,stop);K,D,_=source_kernel(R[sl],Z[sl],target,phi);RAW.update(current_source_bulk=bulk[sl].copy(),current_source_flux=flux[:,sl].copy(),current_source_a=a[sl].copy(),current_source_measure=measure[sl].copy(),current_angle_nodes=phi.copy(),current_angle_weights=weight.copy())
        b=bulk[sl,None]*K;g=-ELL**2*flux[:,sl].transpose(1,0,2,3)[:,None]*D;l=B0*ELL**2*a[sl,:,None,None][:,None]*flux[:,sl].transpose(1,0,2,3)[:,None]*K[:,:,None]
        signed=np.stack((np.sum(b,axis=(-2,-1)),np.sum(g,axis=(-3,-2,-1)),np.sum(l,axis=(-3,-2,-1))),axis=-1);absolute=np.stack((np.sum(abs(b),axis=(-2,-1)),np.sum(abs(g),axis=(-3,-2,-1)),np.sum(abs(l),axis=(-3,-2,-1))),axis=-1)
        if outer:signed*=ELL**2;absolute*=ELL**2
        contribution=measure[sl,None]*np.sum(weight[None,:,None]*signed,axis=1);env=measure[sl,None]*np.sum(weight[None,:,None]*absolute,axis=1);RAW.update(current_integrand_components=signed.copy(),current_integrand_component_envelopes=absolute.copy(),current_integrated_components=contribution.copy(),current_integrated_envelopes=env.copy())
        if not np.all(np.isfinite(contribution)) or not np.all(np.isfinite(env)):raise ArithmeticError('Finite weak projection operands refused')
        result[sl]=contribution;envelope[sl]=env;RAW.update(running_point_components=result.copy(),running_point_envelopes=envelope.copy())
    return result,envelope

def branch(data,spatial,order,input_record):
    phi,weight=angular_rule(order);nq,npoint=data['R'].shape;parts=np.zeros((len(TARGETS),nq,npoint,3));env=np.zeros_like(parts);outer=np.zeros((len(TARGETS),len(data['outer_R'])));outerenv=np.zeros_like(outer);rows=[];prefactor=3*C*B0**2/(16*math.pi)
    for t,target in enumerate(TARGETS):
        CONTEXT.update(spatial_order=spatial,angular_order=order,target_radius=target,target_index=t)
        for q in range(nq):
            CONTEXT.update(volume_quadrature_index=q);pp,ee=integrate(data['R'][q],data['Z'][q],data['bulk'][q],data['flux'][q],data['a'][q],data['measure'][q],target,phi,weight);parts[t,q]=pp;env[t,q]=ee;RAW.update(accepted_volume_components=parts.copy(),accepted_volume_envelopes=env.copy())
        ff=data['outer_flux'];pp,ee=integrate(data['outer_R'],data['outer_Z'],ff,np.zeros((3,len(ff),3,3)),np.zeros((len(ff),3)),data['outer_measure'],target,phi,weight,True);outer[t]=pp[:,0];outerenv[t]=ee[:,0];RAW.update(accepted_outer_components=outer.copy(),accepted_outer_envelopes=outerenv.copy())
        total=parts[t].sum(axis=(0,1));totalenv=env[t].sum(axis=(0,1));ot=float(outer[t].sum());oe=float(outerenv[t].sum());raw=float(total.sum()+ot);den=float(totalenv.sum()+oe)
        rows.append(dict(target_R_kpc=target,target_Z_kpc=0.,bulk=float(total[0]),gradient_improvement=float(total[1]),lapse_improvement=float(total[2]),outer=ot,raw_total=raw,raw_uncanceled_envelope=den,prefactor=prefactor,scalar_slip=prefactor*raw,scalar_slip_envelope=prefactor*den,unknown_exterior=None,unknown_homogeneous=None,unknown_ordinary=None,unknown_background=None,unknown_TT=None,unknown_shift=None,physical_flags=FLAGS))
    arrays=dict(volume_components=parts,volume_component_envelopes=env,outer_components=outer,outer_component_envelopes=outerenv,angular_nodes=phi,angular_weights=weight,target_radii=np.asarray(TARGETS));record=checkpoint(f'Q{spatial}_ANGLE{order}',arrays,dict(input_checkpoint=input_record,spatial_order=spatial,angular_order=order,component_order=['bulk','gradient_improvement','lapse_improvement'],rows=rows,prefactor=prefactor,geometry_fold='actual phi reflection and midplane Z mirror factor4'))
    return rows,record

def main():
    global np,INPUTS,OWNER,B0
    if AUTHOR_GUARD:raise RuntimeError('Guarded root-only saved weak projection')
    if list(BASE.glob(STEM+'_*')):raise FileExistsError('Existing runtime preserved')
    INPUTS=inputs();old=parent();OWNER=dict(owner='root',pid=os.getpid(),started=now(),source_sha256=sha(__file__));tick=time.monotonic();cases=[]
    try:
        publish(STEM+'_OWNER_START.json',OWNER);B0=old['units']['B0']
        if not math.isfinite(B0) or B0<=0:raise ValueError('Literal positive saved B0')
        manifest=dict(owner=OWNER,input_sha256=INPUTS,targets=TARGETS,spatial_orders=[2,3],angular_orders=ORDERS,phi_breaks=BREAKS,block_points=BLOCK,fold=4,implementation_tolerance=ARITH_TOL,finite_difference_tolerance=FD_TOL,angular_tolerance=ANGLE_TOL,floor=FLOOR,C=C,ell=ELL,B0=B0,implementation_count=10,angular_count=36,checkpoint_pairs=9,scope='Conditional finite-domain native scalar-slip potential only',physical_flags=FLAGS);publish(STEM+'_MANIFEST.json',manifest)
        np=importlib.import_module('numpy');authenticate();initial=read_parent(old['records'][0]);datasets={};admitted=dict(r=initial['r'].copy(),z=initial['z'].copy())
        for order in (2,3):
            volume=read_parent(old['records'][1 if order==2 else 3]);faces=read_parent(old['records'][2 if order==2 else 4]);data=dataset(order,initial,volume,faces);datasets[order]=data;admitted.update({f'Q{order}_'+k:v for k,v in data.items()})
        inp=checkpoint('INPUT',admitted,dict(parent_records=old['records'],original_parent_identity=old['parent_case_copied_exactly']['identity'],all_parent_controls_copied=old['controls'],no_stress_reevaluation=True))
        control_raw={k:v.copy() for k,v in RAW.items() if k.startswith('control_')};RAW.clear();RAW.update(control_raw);implementation()
        if len(CONTROLS)!=10:raise ValueError('Exact implementation census')
        checkpoint('IMPLEMENTATION',dict(RAW),dict(controls=CONTROLS,input_checkpoint=inp))
        if not all(c['passed'] for c in CONTROLS):raise ArithmeticError('Implementation controls refused')
        for spatial in (2,3):
            for order in ORDERS:RAW.clear();rows,rec=branch(datasets[spatial],spatial,order,inp);cases.append(dict(spatial_order=spatial,angular_order=order,rows=rows,checkpoint=rec))
        outcomes=[];differences=[];comparison_arrays={}
        for spatial in (2,3):
            ref=next(z for z in cases if z['spatial_order']==spatial and z['angular_order']==32)
            for order in (8,16):
                cur=next(z for z in cases if z['spatial_order']==spatial and z['angular_order']==order)
                for t,(a,b) in enumerate(zip(cur['rows'],ref['rows'])):
                    diff=a['scalar_slip']-b['scalar_slip'];den=a['scalar_slip_envelope']+b['scalar_slip_envelope'];er=abs(diff)/max(den,FLOOR);outcomes.append(dict(spatial_order=spatial,angular_order=order,reference_order=32,target_R_kpc=TARGETS[t],signed_difference=diff,uncanceled_envelope=den,error=finite(er),tolerance=ANGLE_TOL,floor=FLOOR,passed=math.isfinite(er) and er<=ANGLE_TOL,relative_to_slip=finite(abs(diff)/max(abs(a['scalar_slip'])+abs(b['scalar_slip']),FLOOR)),not_continuum_or_force_qualification=True))
        for order in ORDERS:
            a=next(z for z in cases if z['spatial_order']==2 and z['angular_order']==order);b=next(z for z in cases if z['spatial_order']==3 and z['angular_order']==order)
            for t,(aa,bb) in enumerate(zip(a['rows'],b['rows'])):differences.append(dict(angular_order=order,target_R_kpc=TARGETS[t],signed_Q3_minus_Q2=bb['scalar_slip']-aa['scalar_slip'],descriptive_only=True))
        comparison_arrays.update(angular_signed_differences=np.asarray([z['signed_difference'] for z in outcomes]),angular_envelopes=np.asarray([z['uncanceled_envelope'] for z in outcomes]),spatial_signed_differences=np.asarray([z['signed_Q3_minus_Q2'] for z in differences]));checkpoint('COMPARISONS',comparison_arrays,dict(angular_outcomes=outcomes,spatial_differences=differences,input_checkpoint=inp))
        if len(RECORDS)!=9 or len(outcomes)!=36:raise ValueError('Complete bounded census')
        close();status='DISCRETE_ANGULAR_ARITHMETIC_PASS' if all(z['passed'] for z in CONTROLS+outcomes) else 'DISCRETE_PROJECTION_OUTCOMES_RETAINED'
        result=dict(status=status,owner=OWNER,manifest=manifest,cases=cases,implementation_controls=CONTROLS,angular_outcomes=outcomes,spatial_differences=differences,checkpoint_pairs=RECORDS,parent_controls_copied_exactly=old['controls'],parent_case_copied_exactly=old['parent_case_copied_exactly'],parent_failure_receipt_sha256_copied_exactly=old['original_failure_receipt_sha256'],parent_flags_copied_exactly=old['physical_flags'],physical_flags=FLAGS,elapsed_seconds=time.monotonic()-tick)
        rh=publish(STEM+'_RESULT.json',result);text=('# Saved native scalar-slip potential\n\n'+status+'; native finite-domain conditional contribution only. No force, full metric, exterior or observational qualification.\n').encode();rp=BASE/(STEM+'_REPORT.md')
        with rp.open('xb') as f:f.write(text);f.flush();os.fsync(f.fileno())
        rp.chmod(0o444)
        if rp.read_bytes()!=text:raise ValueError('Exact report bytes')
        CREATED[rp.name]=sha(rp);close();rc=dict(status='CLOSED',owner=OWNER,closed=now(),input_sha256=INPUTS,output_sha256=dict(CREATED),result_sha256=rh,checkpoint_pairs=9,predicate_count=46,physical_flags=FLAGS);publish(STEM+'_RECEIPT.json',rc);close()
        if json.loads((BASE/(STEM+'_RECEIPT.json')).read_text())!=rc:raise ValueError('Exact final receipt')
        return 0 if status=='DISCRETE_ANGULAR_ARITHMETIC_PASS' else 3
    except Exception:
        trace=traceback.format_exc();p=BASE/(STEM+'_RECEIPT.json');prior=dict(file=p.name,sha256=sha(p),registered_sha256=CREATED.get(p.name)) if p.exists() else None;rawrec=None
        if np is not None and RAW:rawrec=checkpoint('ERROR_RAW',dict(RAW),dict(unaccepted=True,context=dict(CONTEXT),protected_prior_receipt=prior),True)
        h=publish(STEM+'_ERROR.json',dict(status='ERROR_PRESERVED',owner=OWNER,failed=now(),traceback=trace,error_raw=rawrec,context=CONTEXT,protected_prior_receipt=prior,preserved_outputs=dict(CREATED),physical_flags=FLAGS))
        if prior is None:publish(STEM+'_RECEIPT.json',dict(status='CLOSED',owner=OWNER,closed=now(),input_sha256=INPUTS,output_sha256=dict(CREATED),error_sha256=h,physical_flags=FLAGS))
        elif sha(p)!=prior['sha256']:raise ValueError('Protected receipt changed')
        close();raise

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root-owned',action='store_true');args=ap.parse_args()
    if not args.root_owned:raise RuntimeError('Explicit root ownership required')
    raise SystemExit(main())

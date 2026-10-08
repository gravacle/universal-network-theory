"""Guarded prospective same-H continuation from the exact saved entangled tau2 states."""
import os,sys
sys.dont_write_bytecode=True
for k in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
import argparse,hashlib,json,math,time
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
BASE=Path(__file__).resolve().parent
NAME='NATIVE_UNIFIED_PARENT_LATE_PHOTON_CONTINUATION_V001'
PARENT='NATIVE_RECORD_COPY_CANONICAL_MAXWELL_V001';REM='NATIVE_UNIFIED_PARENT_REDUCED_CORRELATION_REMAINDER_V001';SHAPE='NATIVE_UNIFIED_PARENT_SAVED_PHYSICAL_MODE_THERMAL_SHAPE_V002'
ROOT_REVIEW_PENDING=False
TOL=1e-11;RELATIVE_FLOOR=1e-14;ORDER=32;RADIUS=2.;RADIUS_ALLOWANCE=32*sys.float_info.epsilon*RADIUS;TIMES=(2.,4.,8.,16.,32.)
CASES=(('native',1.,.5),('feedback_off',1.,0.),('copy_off',0.,.5));KS=(0.,-.001,.001);MS=(8,12,16)
PINS={'native_record_copy_canonical_maxwell_v001.py': '607c84a7ac98776d3e3e34bf508808b2e8e3500088354b02205fdb6995e4e23a', 'NATIVE_RECORD_COPY_CANONICAL_MAXWELL_V001.md': '28167e16995285aaa24e7d8a1ef734cdd086a0d7aeefccb7fef33c07374ca048', 'NATIVE_RECORD_COPY_CANONICAL_MAXWELL_V001_RESULT.json': 'd2ad69ba985d5b5ef21ecd2caa687578231c621a79c0d4eb34cdefb344ad90d3', 'NATIVE_RECORD_COPY_CANONICAL_MAXWELL_V001_RECEIPT.json': '91bc8a7feafdbf6bc72ab8e072e7a1575ae0641c64d9c8b91eb1c6c7e64dd073', 'native_unified_parent_reduced_correlation_remainder_v001.py': 'f66f37ef6a8bc86ade6fcb35bc2d576031ff17370b6f23526c36c9892f64fb37', 'NATIVE_UNIFIED_PARENT_REDUCED_CORRELATION_REMAINDER_V001.md': '2bca11d70888856b4b43489068bbeb3184cdf7066f34ef4b45ccb11843d0246a', 'NATIVE_UNIFIED_PARENT_REDUCED_CORRELATION_REMAINDER_V001_RESULT.json': '6e85cf97be74cc36185e929b333a929ec3a0367982041bd2aea64b7019b3c0b0', 'NATIVE_UNIFIED_PARENT_REDUCED_CORRELATION_REMAINDER_V001_RECEIPT.json': '1bfa3a4cb52d408ba1a88949826dd7622b27fc3245946bdf79f78bfcdba8ca21', 'native_unified_parent_saved_physical_mode_thermal_shape_v002.py': '0fd348d2c0a8a27f55a4312e4c311d1f485ebfc73902d03c13f8f7572c2b76c3', 'NATIVE_UNIFIED_PARENT_SAVED_PHYSICAL_MODE_THERMAL_SHAPE_V002.md': '230122c32d646618fef1fad5207adc14c1f4efd16d34147bb23b741eaf1d85a9', 'NATIVE_UNIFIED_PARENT_SAVED_PHYSICAL_MODE_THERMAL_SHAPE_V002_RESULT.json': '1086b2f4565b51b342255567613b03ed17f43b45e9f3f6ce5049d45adfe4c385', 'NATIVE_UNIFIED_PARENT_SAVED_PHYSICAL_MODE_THERMAL_SHAPE_V002_RECEIPT.json': 'eb4890bfd6b6ce83a268f23fda7b04bad5e0402e56bc336994f2c694d0d727c8', 'NATIVE_UNIFIED_PARENT_PHYSICAL_MODE_MARGINAL_AND_THERMAL_ONSET_V001.md': 'f97636a2851631cecbe215072f61082cd890334f9b48152e9ad174c7991854f7', 'PHYSICAL_MODE_PAIR_BUNCHING_ONSET_V001.md': '416ce614bde2d7bf89b0ec06c59261ee78165a5b5983c82c1e5004f516deb111', 'native_unified_parent_late_photon_continuation_v001_AUTHOR_DRAFT.py': 'b4964bc0bdc11dc265b1394f5a880bac9ac81abef4ac856a3f4ad7462c1ede3e', 'NATIVE_UNIFIED_PARENT_LATE_PHOTON_CONTINUATION_V001_AUTHOR_DRAFT.md': 'c1266250cfed57503fc303bd6ea7bf427347f8ced04a873909663f4ac861e42f'}
PINS[NAME+'.md']='41a261b24a812c76d1195326da0a3402a8e2652d91743104ddf94376eaeb2729'
OUTS=[BASE/(NAME+s) for s in ('_RESULT.json','_REPORT.md','_RECEIPT.json')]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def finite(v):
    if isinstance(v,dict):
        if any(not isinstance(k,str) for k in v):raise TypeError('JSON key')
        for q in v.values():finite(q)
    elif isinstance(v,list):
        for q in v:finite(q)
    elif isinstance(v,float):
        if not math.isfinite(v):raise ValueError('Nonfinite JSON')
    elif not isinstance(v,(str,int,bool,type(None))):raise TypeError('Non-native JSON type')
def canonical(v):
    finite(v);return json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False).encode()+b'\n'
def read(p):
    raw=Path(p).read_bytes();z=json.loads(raw);finite(z)
    if canonical(z)!=raw:raise ValueError('Noncanonical JSON '+str(p))
    return z

def write(p,v):
    b=v if isinstance(v,bytes) else canonical(v)
    with Path(p).open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
    Path(p).chmod(0o444);return sha(p)
def verify(source):
    if sha(__file__)!=source or Path(__file__).stat().st_mode&0o222:raise RuntimeError('Source changed or mutable')
    for n,h in PINS.items():
        if h=='PENDING' or sha(BASE/n)!=h or (BASE/n).stat().st_mode&0o222:raise RuntimeError('Input changed or mutable '+n)
    return dict(PINS,**{Path(__file__).name:source})
def pack(v):return dict(real=v.real.tolist(),imag=v.imag.tolist())
def unpack(v,shape):
    if set(v)!={'real','imag'}:raise ValueError('Complex pack keys')
    a=np.asarray(v['real'],float);b=np.asarray(v['imag'],float)
    if a.shape!=shape or b.shape!=shape or not np.all(np.isfinite(a)) or not np.all(np.isfinite(b)):raise ValueError('Complex shape/finite')
    z=np.empty(shape,complex);z.real=a;z.imag=b;return z

def taylor(app,v,t,bound):
    blocks=max(1,math.ceil(abs(t)*bound/RADIUS));dt=t/blocks;r=abs(dt)*bound
    tail=math.exp(r)*r**(ORDER+1)/math.factorial(ORDER+1);u=v.copy()
    for _ in range(blocks):
        term=u.copy();out=u.copy()
        for k in range(1,ORDER+1):term=(-1j*dt/k)*app(term);out+=term
        u=out
    return u,dict(substeps=blocks,order=ORDER,radius=r,local_tail=tail,accumulated_tail=blocks*tail*math.exp(blocks*tail),tail_scope='Exact-arithmetic truncation only; no roundoff certificate')
def validate_tail(td,tau):
    if set(td)!={'substeps','order','radius','local_tail','accumulated_tail','tail_scope'} or td['order']!=ORDER or type(td['substeps']) is not int:raise ValueError('Taylor schema')
    if tau==2.:
        if td['substeps']!=0 or any(td[k]!=0. for k in ('radius','local_tail','accumulated_tail')):raise ValueError('Anchor Taylor record')
    elif td['substeps']<=0 or not (0.<td['radius']<=RADIUS+RADIUS_ALLOWANCE) or not (0.<td['local_tail']<=td['accumulated_tail']<TOL) or any(not math.isfinite(td[k]) for k in ('radius','local_tail','accumulated_tail')):raise ValueError('Taylor radius/tail precondition')
def metrics(v,hn,n,B,W,H):
    hn_v=hn@v;B_v=v@B.T;I_v=(n@v)@W.T
    energies=[np.vdot(v,a) for a in (hn_v,B_v,I_v)];EN,EB,EI=(float(a.real) for a in energies)
    direct=np.vdot(v.ravel(),H@v.ravel());norm=float(np.vdot(v,v).real);diag=np.sum(np.abs(v)**2,axis=0);M=v.shape[1]-1
    pop=[math.fsum(float(diag[j])/(j+1) for j in range(m,M+1)) for m in range(M+1)]
    number=math.fsum(2*j*float(x) for j,x in enumerate(diag));mu=number/4;factorial=math.fsum(j*(j-1)*float(x)/3 for j,x in enumerate(diag))
    r=mu/(1+mu);reference=[r**m/(1+mu) for m in range(M+1)];tail=r**(M+1);signed=[x-y for x,y in zip(pop,reference)]
    half=(math.fsum(abs(x) for x in signed)+tail)/2;defined=mu>RELATIVE_FLOOR
    scalars=dict(norm=norm,norm_defect=norm-1.,native=EN,bare_photon=EB,interaction=EI,total=math.fsum((EN,EB,EI)),total_dense=float(direct.real),native_debit=3.-EN,bare_photon_gain=EB-2.,inclusive_field_excess=math.fsum((EB,EI,-2.)),absolute_ledger=math.fsum((EN,EB,EI,-5.)),photon_number=number,mean_incidence=float(np.vdot(v,n@v).real),mu=mu,factorial=factorial,thermal_factorial_reference=2*mu*mu,signed_factorial_minus_thermal=factorial-2*mu*mu,top_pair_probability=float(diag[-1]),raw_half_L1=half,g2=factorial/(mu*mu) if defined else None,relative_raw_half_L1_over_mu=half/mu if defined else None,relative_reason=None if defined else 'raw_mean_not_above_1e-14')
    return dict(joint_amplitudes=pack(v),field_diagonal=diag.tolist(),physical_mode_populations=pop,geometric_reference=reference,infinite_reference_tail=tail,signed_population_minus_reference=signed,energy_imag=[float(a.imag) for a in energies],total_dense_imag=float(direct.imag),scalars=scalars)
def check(controls,label,a,b=0.,scale=1.):
    e=float(np.max(np.abs(np.asarray(a)-np.asarray(b))));s=max(1.,float(scale))
    controls.append(dict(label=label,error=e,scale=s,tolerance=TOL,passed=bool(math.isfinite(e) and e<=TOL*s)))
def calculate(tr,anchor,old):
    case,kappa,M=tr['case'],tr['kappa'],tr['M'];d=M+1;D=16*d;tag=f'{case}:{kappa}:{M}'
    hn=unpack(tr['HN'],(16,16));n=unpack(tr['n'],(16,16));B=unpack(tr['B'],(d,d));W=unpack(tr['W'],(d,d))
    H=np.kron(hn,np.eye(d))+np.kron(np.eye(16),B)+np.kron(n,W);bound=float(np.linalg.norm(hn,np.inf)+np.linalg.norm(B,np.inf)+np.linalg.norm(n,np.inf)*np.linalg.norm(W,np.inf))
    def app(v):return hn@v+v@B.T+(n@v)@W.T
    eig,vec=np.linalg.eigh(H);controls=[]
    for key,a in (('HN',hn),('n',n),('B',B),('W',W)):check(controls,tag+':hermitian:'+key,a,a.conj().T,scale=bound)
    check(controls,tag+':projector',n@n,n);check(controls,tag+':full_hermitian',H,H.conj().T,scale=bound)
    check(controls,tag+':eigen_equation',H@vec,vec*eig,scale=bound);check(controls,tag+':eigen_orthogonal',vec.conj().T@vec,np.eye(D))
    anchors={method:unpack(anchor['methods'][method]['joint_amplitudes'],(16,d)) for method in ('spectral','taylor')}
    initial={method:metrics(v,hn,n,B,W,H) for method,v in anchors.items()};weights=vec.conj().T@anchors['spectral'].ravel()
    for method in anchors:
        stats=anchor['methods'][method]['scalars'];a=initial[method]['scalars'];check(controls,tag+':anchor_norm:'+method,a['norm'],stats['norm']);check(controls,tag+':anchor_number:'+method,a['photon_number'],stats['photon_number'])
    for key in ('native','bare_photon','interaction'):check(controls,tag+':anchor_energy:'+key,initial['spectral']['scalars'][key],old[key],scale=bound)
    frames=[]
    if not (0.<bound<45.82 and math.isfinite(bound)):raise ValueError('Owned operator bound')
    for tau in TIMES:
        elapsed=tau-2.;sp=anchors['spectral'].copy() if elapsed==0 else (vec@(np.exp(-1j*elapsed*eig)*weights)).reshape(16,d)
        tv,td=(anchors['taylor'].copy(),dict(substeps=0,order=ORDER,radius=0.,local_tail=0.,accumulated_tail=0.,tail_scope='Exact preserved anchor')) if elapsed==0 else taylor(app,anchors['taylor'],elapsed,bound)
        validate_tail(td,tau);methods={}
        for method,v in (('spectral',sp),('taylor',tv)):
            z=metrics(v,hn,n,B,W,H);a=z['scalars'];a0=initial[method]['scalars'];ptag=tag+':'+str(tau)+':'+method
            a['total_change_from_own_anchor']=a['total']-a0['total'];a['native_change_from_own_anchor']=a['native']-a0['native'];a['bare_photon_change_from_own_anchor']=a['bare_photon']-a0['bare_photon'];a['interaction_change_from_own_anchor']=a['interaction']-a0['interaction']
            check(controls,ptag+':norm_anchor',a['norm'],a0['norm']);check(controls,ptag+':norm_one',a['norm'],1.)
            scale=abs(a['native'])+abs(a['bare_photon'])+abs(a['interaction'])+abs(a0['total'])
            check(controls,ptag+':energy_anchor',a['total'],a0['total'],scale=scale)
            check(controls,ptag+':direct_energy',[a['total_dense'],z['total_dense_imag']]+z['energy_imag'],[a['total'],0.,0.,0.,0.],scale=scale)
            check(controls,ptag+':field_lower',max(0.,2*a['norm']-a['bare_photon']-a['interaction']),scale=scale)
            check(controls,ptag+':diagonal_trace',math.fsum(z['field_diagonal']),a['norm']);check(controls,ptag+':physical_trace',math.fsum(z['physical_mode_populations']),a['norm'])
            check(controls,ptag+':physical_mean',math.fsum(m*x for m,x in enumerate(z['physical_mode_populations'])),a['mu'],scale=max(1.,a['photon_number']))
            check(controls,ptag+':factorial_identity',math.fsum(m*(m-1)*x for m,x in enumerate(z['physical_mode_populations'])),a['factorial'],scale=max(1.,a['factorial']))
            check(controls,ptag+':geometric_measure',math.fsum(z['geometric_reference'])+z['infinite_reference_tail'],1.)
            methods[method]=z
        check(controls,tag+':'+str(tau)+':spectral_taylor',np.linalg.norm(sp-tv))
        ss=methods['spectral']['scalars'];ts=methods['taylor']['scalars'];dif={k:ss[k]-ts[k] for k in ss if isinstance(ss[k],(float,int)) and not isinstance(ss[k],bool) and isinstance(ts[k],(float,int))}
        frames.append(dict(case=case,kappa=kappa,M=M,tau=tau,methods=methods,taylor=td,method_difference=dict(joint_amplitudes=pack(sp-tv),joint_frobenius=float(np.linalg.norm(sp-tv)),scalar_differences=dif,signed_physical_populations=[x-y for x,y in zip(methods['spectral']['physical_mode_populations'],methods['taylor']['physical_mode_populations'])])))
    if len(controls)!=120:raise ValueError('Trial control census')
    return dict(trial=tr,anchor=anchor,dimension=D,operator_bound=bound,eigenvalues=eig.tolist(),frames=frames,controls=controls)
def validate_trial(cp,index,expected,lineage,anchors,trials):
    if cp['index']!=index or cp['lineage']!=lineage or cp['owner']!='root' or type(cp['PID']) is not int or cp['PID']<=0:raise ValueError('Trial provenance')
    data=cp['data'];tr=data['trial'];key=(tr['case'],tr['kappa'],tr['M'])
    if key!=expected[index] or canonical(data['anchor'])!=canonical(anchors[key]) or canonical(tr)!=canonical(trials[key]) or [r['tau'] for r in data['frames']]!=list(TIMES) or len(data['controls'])!=120:raise ValueError('Trial schema')
    if data['dimension']!=16*(key[2]+1):raise ValueError('Trial dimension')
    for row in data['frames']:
        validate_tail(row['taylor'],row['tau'])
        if (row['case'],row['kappa'],row['M'])!=key or set(row['methods'])!={'spectral','taylor'}:raise ValueError('Frame descriptor')
        for method,z in row['methods'].items():
            a=z['joint_amplitudes'];d=key[2]+1
            if len(a['real'])!=16 or len(a['imag'])!=16 or any(len(v)!=d for v in a['real']+a['imag']) or any(len(z[k])!=d for k in ('field_diagonal','physical_mode_populations','geometric_reference','signed_population_minus_reference')):raise ValueError('Frame packed shape')
            if row['tau']==2. and canonical(a)!=canonical(anchors[key]['methods'][method]['joint_amplitudes']):raise ValueError('Anchor changed')
    for c in data['controls']:
        if set(c)!={'label','error','scale','tolerance','passed'} or not isinstance(c['label'],str) or type(c['passed']) is not bool or type(c['error']) not in (int,float) or type(c['scale']) not in (int,float) or not (0.<=c['error'] and math.isfinite(c['error']) and c['scale']>=1. and math.isfinite(c['scale'])) or c['tolerance']!=TOL or c['passed']!=(c['error']<=TOL*c['scale']):raise ValueError('Stored trial predicate')
def main(resume,publish_only):
    if ROOT_REVIEW_PENDING or 'AUTHOR_DRAFT' in Path(__file__).name:raise SystemExit('Guarded author draft; root review/final seals required')
    if OUTS[2].exists():raise RuntimeError('Existing accepted terminal receipt')
    if publish_only and not resume:raise ValueError('Publication recovery requires explicit --resume --publish-only')
    if not publish_only and any(p.exists() for p in OUTS):raise RuntimeError('Existing partial publication; use explicit --resume --publish-only only after complete closed prefix')
    source=sha(__file__);inputs=verify(source);started=datetime.now(timezone.utc).isoformat();tick=time.monotonic()
    parent=read(BASE/(PARENT+'_RESULT.json'));rem=read(BASE/(REM+'_RESULT.json'));shape=read(BASE/(SHAPE+'_RESULT.json'))
    for name,z,count,producer in ((PARENT,parent,3348,'native_record_copy_canonical_maxwell_v001.py'),(REM,rem,6345,'native_unified_parent_reduced_correlation_remainder_v001.py'),(SHAPE,shape,3195,'native_unified_parent_saved_physical_mode_thermal_shape_v002.py')):
        receipt=read(BASE/(name+'_RECEIPT.json'))
        if z['inputs']!=receipt['inputs'] or z['source_sha256']!=PINS[producer] or z['inputs'][producer]!=PINS[producer] or receipt['outputs'][name+'_RESULT.json']!=PINS[name+'_RESULT.json']:raise ValueError('Parent binding '+name)
        if receipt['trials']!=27 or receipt['states']!=135 or receipt['comparisons']!=90 or receipt['checks' if name==PARENT else 'controls']!=count:raise ValueError('Parent receipt census '+name)
        if z['owner']!=receipt['owner'] or z['owner']!='root' or z['PID']!=receipt['PID'] or z['status']!=receipt['status'] or z['status']!='PASS' or z['failed']!=receipt['failed'] or z['failed']!=0:raise ValueError('Parent owner/status '+name)
        if len(z['controls'])!=count or any(not c['passed'] for c in z['controls']) or len(z['rows'])!=135 or len(z['comparisons'])!=90 or len(z['trials'])!=27:raise ValueError('Parent census '+name)
    if shape['original_controls']!=parent['controls'] or shape['component_controls']!=rem['component_controls'] or shape['correlation_controls']!=rem['controls'] or rem['original_controls']!=parent['controls'] or len(rem['component_controls'])!=3528:raise ValueError('Preserved controls')
    expected=[(c,k,M) for c,g,lr in CASES for k in KS for M in MS]
    trials={(z['case'],z['kappa'],z['M']):z for z in rem['trials']};anchors={(z['case'],z['kappa'],z['M']):z for z in rem['rows'] if z['tau']==2.};old={(z['case'],z['kappa'],z['M']):z for z in parent['rows'] if z['tau']==2.}
    if set(trials)!=set(expected) or set(anchors)!=set(expected) or set(old)!=set(expected):raise ValueError('Complete anchor descriptors')
    for c,g,lr in CASES:
        for k in KS:
            for M in MS:
                tr=trials[(c,k,M)]
                if tr['g']!=g or tr['lambda_R']!=lr or set(tr)!={'case','g','lambda_R','kappa','M','HN','n','B','W'}:raise ValueError('Exact saved trial schema')
    lineage=dict(name=NAME,source_sha256=source,inputs=inputs,times=list(TIMES),expected_trials=[list(k) for k in expected],tolerance=TOL,taylor_order=ORDER,taylor_radius=RADIUS,radius_roundoff_allowance=RADIUS_ALLOWANCE,relative_floor=RELATIVE_FLOOR,numpy_version=np.__version__,anchor_source=REM+'_RESULT.json',anchor_tau=2.,actuator_work=0.,new_initial_preparation=False)
    mp=BASE/(NAME+'_MANIFEST.json');jp=BASE/(NAME+'_JOURNAL.jsonl');cp_names=[NAME+'_CP_'+str(i).zfill(3)+'.json' for i in range(27)]
    present=[n for n in cp_names if (BASE/n).exists()];commits=[n[:-5]+'_COMMIT.json' for n in present]
    reserved=list(BASE.glob(NAME+'_CP_*'))
    if not resume and (mp.exists() or jp.exists() or reserved):raise RuntimeError('Explicit --resume required')
    if not mp.exists() and (jp.exists() or reserved):raise RuntimeError('Preserved owner-prefix orphan')
    created={};events=[]
    if mp.exists():
        if read(mp)!=lineage or not jp.exists():raise ValueError('Resume manifest/owner prefix')
        raw=jp.read_bytes();events=[json.loads(b) for b in raw.splitlines()]
        if not events or any(canonical(e).rstrip(b'\n')!=b for e,b in zip(events,raw.splitlines())) or not raw.endswith(b'\n'):raise ValueError('Noncanonical owner journal')
    else:
        if publish_only:raise ValueError('No publication prefix')
        write(mp,lineage)
    created[mp.name]=sha(mp)
    if present!=cp_names[:len(present)] or sorted(p.name for p in reserved)!=sorted(present+commits):raise ValueError('Exact checkpoint prefix')
    loaded=[];validated_events=[];epoch=-1;owner_pid=None;last_index=-1;completed=None
    for e in events:
        if e.get('source_sha256')!=source or e.get('input_sha256')!=inputs or e.get('manifest_sha256')!=created[mp.name] or e.get('owner')!='root' or type(e.get('PID')) is not int or e['PID']<=0:raise ValueError('Journal ownership')
        if completed is not None:raise ValueError('Event after terminal owner closure')
        if e['event'] in ('OWNER_START','OWNER_RESUME'):
            if e['epoch']!=epoch+1 or (epoch==-1 and e['event']!='OWNER_START') or (epoch>=0 and e['event']!='OWNER_RESUME'):raise ValueError('Owner epoch')
            epoch=e['epoch'];owner_pid=e['PID']
        elif e['event']=='CHECKPOINT':
            if e['epoch']!=epoch or e['PID']!=owner_pid or e['index']!=last_index+1 or last_index+1>=len(present):raise ValueError('Checkpoint owner/prefix')
            last_index+=1;validated_events.append(e)
        elif e['event']=='OWNER_COMPLETE':
            if e['epoch']!=epoch or e['PID']!=owner_pid or last_index!=26 or (e['trials'],e['states'],e['comparisons'],e['controls'])!=(27,135,90,3600):raise ValueError('Terminal owner census')
            completed=e
        else:raise ValueError('Unexpected journal event')
    if len(validated_events)!=len(present):raise ValueError('Incomplete committed owner prefix')
    if publish_only:
        if completed is None or len(present)!=27 or jp.stat().st_mode&0o222:raise ValueError('Publication recovery requires protected complete27-pair journal')
    elif completed is not None or (jp.exists() and not jp.stat().st_mode&0o222):raise ValueError('Closed prefix requires explicit --resume --publish-only; no trajectory rerun')
    for index,nm in enumerate(present):
        cp=read(BASE/nm);cn=nm[:-5]+'_COMMIT.json';co=read(BASE/cn);h=sha(BASE/nm);validate_trial(cp,index,expected,lineage,anchors,trials)
        if co!=dict(payload=nm,sha256=h,index=index,lineage=lineage,owner='root',PID=cp['PID']) or validated_events[index]['payload_sha256']!=h or validated_events[index]['commit_sha256']!=sha(BASE/cn) or validated_events[index]['PID']!=cp['PID']:raise ValueError('Commit/event binding')
        for n in (nm,cn):
            if (BASE/n).stat().st_mode&0o222:raise ValueError('Mutable checkpoint')
            created[n]=sha(BASE/n)
        loaded.append(cp['data'])
    def event(kind,**fields):
        e=dict(event=kind,owner='root',PID=os.getpid(),epoch=epoch,utc=datetime.now(timezone.utc).isoformat(),source_sha256=source,input_sha256=inputs,manifest_sha256=created[mp.name],**fields)
        with jp.open('ab') as f:f.write(canonical(e));f.flush();os.fsync(f.fileno())
        events.append(e)
    if not publish_only:
        epoch+=1;event('OWNER_START' if not events else 'OWNER_RESUME')
    for index in range(len(loaded),27):
        verify(source);key=expected[index];data=calculate(trials[key],anchors[key],old[key]);payload=dict(index=index,lineage=lineage,owner='root',PID=os.getpid(),data=data);validate_trial(payload,index,expected,lineage,anchors,trials)
        nm=cp_names[index];h=write(BASE/nm,payload);cn=nm[:-5]+'_COMMIT.json';ch=write(BASE/cn,dict(payload=nm,sha256=h,index=index,lineage=lineage,owner='root',PID=os.getpid()))
        created[nm]=h;created[cn]=ch;event('CHECKPOINT',index=index,payload_sha256=h,commit_sha256=ch);loaded.append(data);print('LATE_PHOTON',index+1,'/27',flush=True)
    rows=[r for z in loaded for r in z['frames']];controls=[c for z in loaded for c in z['controls']];look={(r['case'],r['kappa'],r['M'],r['tau']):r for r in rows};comparisons=[]
    for case,g,lr in CASES:
        for k in KS:
            for lo,hi in ((8,12),(12,16)):
                for tau in TIMES:
                    methods={}
                    for method in ('spectral','taylor'):
                        a=look[(case,k,lo,tau)]['methods'][method];b=look[(case,k,hi,tau)]['methods'][method];av=unpack(a['joint_amplitudes'],(16,lo+1));bv=unpack(b['joint_amplitudes'],(16,hi+1));ev=np.pad(av,((0,0),(0,hi-lo)));dv=bv-ev
                        scalar={n:b['scalars'][n]-a['scalars'][n] for n in a['scalars'] if isinstance(a['scalars'][n],(float,int)) and isinstance(b['scalars'][n],(float,int))}
                        selected=('norm','native','bare_photon','interaction','total','photon_number','mu','factorial','signed_factorial_minus_thermal','raw_half_L1')
                        tag=f'cutoff:{case}:{k}:{lo}:{hi}:{tau}:{method}';check(controls,tag+':vector',np.linalg.norm(dv));check(controls,tag+':absolute_scalars',[scalar[n] for n in selected],scale=max(1.,*(abs(a['scalars'][n]) for n in selected),*(abs(b['scalars'][n]) for n in selected)))
                        methods[method]=dict(joint_difference=pack(dv),joint_frobenius=float(np.linalg.norm(dv)),signed_scalar_differences=scalar,signed_physical_population_differences=[x-y for x,y in zip(b['physical_mode_populations'],a['physical_mode_populations']+[0.]*(hi-lo))],high_field_tail=pack(bv[:,lo+1:]),high_field_tail_probability=float(np.vdot(bv[:,lo+1:],bv[:,lo+1:]).real))
                    comparisons.append(dict(case=case,kappa=k,M_low=lo,M_high=hi,tau=tau,methods=methods))
    if len(rows)!=135 or len(comparisons)!=90 or len(controls)!=3600 or len(created)!=55:raise ValueError('Locked final census')
    verify(source)
    for n,h in created.items():
        if sha(BASE/n)!=h or (BASE/n).stat().st_mode&0o222:raise RuntimeError('Checkpoint seal changed')
    failed=sum(not c['passed'] for c in controls);status='PASS' if not failed else 'FAIL'
    if publish_only:
        if completed['status']!=status or completed['failed']!=failed:raise ValueError('Publication-control identity')
    else:
        event('OWNER_COMPLETE',trials=27,states=135,comparisons=90,controls=3600,status=status,failed=failed);completed=events[-1];jp.chmod(0o444)
    created[jp.name]=sha(jp);scientific_start=events[0]['utc'];scientific_end=completed['utc'];scientific_pid=completed['PID']
    result=dict(name=NAME,owner='root',PID=scientific_pid,started_utc=scientific_start,finished_utc=scientific_end,elapsed_wall_seconds=(datetime.fromisoformat(scientific_end)-datetime.fromisoformat(scientific_start)).total_seconds(),source_sha256=source,inputs=inputs,status=status,failed=failed,controls=controls,trials=loaded,rows=rows,comparisons=comparisons,original_controls=parent['controls'],component_controls=rem['component_controls'],correlation_controls=rem['controls'],marginal_controls=shape['controls'],parent_physical_claims=parent['physical_claims'],component_physical_claims=rem['component_physical_claims'],correlation_physical_claims=rem['physical_claims'],marginal_physical_claims=shape['physical_claims'],actuator_work=0.,new_initial_preparation=False,physical_claims=dict(thermal_origin=False,temperature=False,Planck_spectrum=False,outgoing_radiation=False,fluid_decoupling=False,macroscopic_pressure_match=False,cosmology=False))
    report=f'# Same autonomous parent late continuation\n\n{status}: {3600-failed}/3600 controls;27 unchanged inherited cases,135 paired states including exact tau2 anchors,90 cutoff comparisons. No vacuum restart, state repair, phase alignment or normalization. Inclusive native/bare-field/interaction energies retain absolute vacuum2 and total5. Mode-shape and factorial ratios are descriptive; no thermality or origin criterion is applied.\n'
    for path,body in ((OUTS[0],canonical(result)),(OUTS[1],report.encode())):
        if path.exists():
            if not publish_only or path.stat().st_mode&0o222 or path.read_bytes()!=body:raise ValueError('Existing publication differs from complete saved prefix')
            created[path.name]=sha(path)
        else:created[path.name]=write(path,body)
    verify(source)
    receipt=dict(owner='root',PID=scientific_pid,publication_PID=os.getpid(),publication_recovery=publish_only,started_utc=scientific_start,closed_utc=datetime.now(timezone.utc).isoformat(),source_sha256=source,inputs=inputs,outputs=created,status=status,failed=failed,trials=27,states=135,new_late_states=108,comparisons=90,controls=3600,checkpoint_pairs=27,journal_events=len(events),original_controls=3348,component_controls=3528,correlation_controls=6345,marginal_controls=3195)
    write(OUTS[2],receipt)
    if verify(source)!=inputs or any(sha(BASE/n)!=h or (BASE/n).stat().st_mode&0o222 for n,h in created.items()):raise RuntimeError('Post-publication seal')
    print(json.dumps(dict(status=status,controls=3600,failed=failed,result_sha256=sha(OUTS[0]),receipt_sha256=sha(OUTS[2]))));return 0 if not failed else 3
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--root-owned',action='store_true',required=True);parser.add_argument('--resume',action='store_true');parser.add_argument('--publish-only',action='store_true');args=parser.parse_args();raise SystemExit(main(args.resume,args.publish_only))

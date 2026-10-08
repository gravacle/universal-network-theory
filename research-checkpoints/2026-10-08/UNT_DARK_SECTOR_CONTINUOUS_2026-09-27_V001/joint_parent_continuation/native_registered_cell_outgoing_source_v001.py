"""Complete saved native spectral/outgoing source functions; root execution only."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,ast,hashlib,json,math,os,time,traceback
BASE=Path(__file__).resolve().parent
STEM='NATIVE_REGISTERED_CELL_OUTGOING_SOURCE_V001'
PARENT='NATIVE_ENERGY_SELECTIVE_CALORIMETER_PORTS_V001'
PROTOCOL_SHA='1b4709beb5ad6c6f52979def111849290d050fec6d31cdc6c6eaf362b992752f'
PINS={'NATIVE_REGISTERED_CELL_OUTGOING_MAXWELL_PAIR_KERNEL_V001.md': 'f4debb30c540386d39179fdcfc244373ac6a2bcab9f04f27fa32c0f404c88c8c', 'NATIVE_INCIDENCE_MAXWELL_PAIR_SOURCE_V002.md': '7e5cf9d3651de4471b52c9a3769f23cdd5457726c8354ff42ecee3c2a4034c7b', 'native_energy_selective_calorimeter_ports_v001.py': '55f7c578c1ed05046c95b4107dcd147d096033c8cbe0a6d87438338ad05a6e70', 'NATIVE_ENERGY_SELECTIVE_CALORIMETER_PORTS_V001.md': '145993fbd35cb52be09169c2dbfcee4e059a3bc45a6f8f696ba6f5081e535d44', 'NATIVE_ENERGY_SELECTIVE_CALORIMETER_PORTS_V001_RESULT.json': '90ab446321a185f0ffae97d6ac6a7d9bbfc50fbc9540460ec491ce1f7c586feb', 'NATIVE_ENERGY_SELECTIVE_CALORIMETER_PORTS_V001_RECEIPT.json': '81611398329f56feb0d1b14fc8eb7cae3b7514791c27ccc617f65c370dc72d2f', 'NATIVE_ENERGY_SELECTIVE_CALORIMETER_PORTS_V001_MANIFEST.json': 'eed0247905d543b6cc658824a0711f74b1a2fab011a680b6b9648ffc4cfba98f', 'NATIVE_ENERGY_SELECTIVE_CALORIMETER_PORTS_V001_JOURNAL.jsonl': 'e80c8cee5df3edd137256b6174641859c22223eaf68e6f8103c877118050464a', 'NATIVE_ENERGY_SELECTIVE_CALORIMETER_PORTS_V001_CP0000.json': '16bc8403151a00565d61c63fda4bbefa45c98cf8bbf89e66ebef1f27173405d1', 'NATIVE_ENERGY_SELECTIVE_CALORIMETER_PORTS_V001_CP0000_COMMIT.json': '539059898279512e031d2328a007239de28d4993cf4b3a8c9291792c934f157f', 'NATIVE_ENERGY_SELECTIVE_CALORIMETER_PORTS_V001_CP0072.json': 'b93a26c777a8ab8321db518f4e75ea4337853b2274f46f138ec3df6f25d36c35', 'NATIVE_ENERGY_SELECTIVE_CALORIMETER_PORTS_V001_CP0072_COMMIT.json': '505f316ef7bde685ead62b90371fab5a503fb95e4f61407ccd7e439beab5898c', 'NATIVE_THERMAL_PACKET_V001_RESULTS.json': '8531cd6f2cf7d60e4b981428c9f80b55ee76b23f17bd4ab91c0e435894010538', 'NATIVE_THERMAL_PACKET_V001_FROZEN.json': '4a6ed3c387bc87961264806ef630f988199bfdde0b3f9d81fb53b11a2c40f0b3'}
EDGES=(0,3)
WINDOWS=(.25,1.,2.)
FREQUENCIES=(.25,.5,1.,2.,4.,8.,16.,32.)
ORDERS=(128,256)
STAGES=('AUTH','CATALOG_Q0','CATALOG_Q1','WINDOW_Q0','WINDOW_Q1','SUMMARY')
SEALS={};CREATED={};SOURCE_SHA=None;MANIFEST_SHA=None;ENTERED=False

def require(ok,msg):
    if not ok:raise AssertionError(msg)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def canonical(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def now():return datetime.now(timezone.utc).isoformat()
def finite(v):
    if type(v) in (bool,int,str) or v is None:return
    if type(v) is float:require(math.isfinite(v),'Finite serialized scalar');return
    if isinstance(v,list):
        for x in v:finite(x)
        return
    if isinstance(v,dict):
        require(all(type(k) is str for k in v),'Canonical string keys')
        for x in v.values():finite(x)
        return
    raise AssertionError('Noncanonical output type')
def write(name,obj):
    finite(obj);b=canonical(obj);p=BASE/name
    with p.open('xb') as f:f.write(b)
    p.chmod(0o444);CREATED[str(p)]=sha(p);return sha(p)
def seal(p,h):
    p=Path(p).resolve();require(p.is_relative_to(BASE.parent.parent),'Owned input path')
    require(sha(p)==h,'Input bytes '+str(p));require(str(p) not in SEALS or SEALS[str(p)]==h,'Consistent input seal');SEALS[str(p)]=h

def recheck():
    require(sha(__file__)==SOURCE_SHA,'Frozen own source')
    for p,h in dict(SEALS,**CREATED).items():require(sha(p)==h,'Frozen input/output '+p)
def event(kind,**kw):
    v=dict(event=kind,time=now(),owner='root',pid=os.getpid(),source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,**kw);finite(v)
    with (BASE/(STEM+'_JOURNAL.jsonl')).open('a') as f:f.write(canonical(v).decode())
def checkpoint(stage,data):
    recheck();pn=STEM+'_'+stage+'_CP.json';cn=STEM+'_'+stage+'_CP_COMMIT.json'
    payload=dict(stage=stage,owner='root',pid=os.getpid(),source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,data=data)
    h=write(pn,payload);ch=write(cn,dict(stage=stage,owner='root',pid=os.getpid(),source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,payload=pn,payload_sha256=h))
    event('CHECKPOINT',stage=stage,payload=pn,payload_sha256=h,commit=cn,commit_sha256=ch)

def authenticate():
    for n,h in dict(PINS,**{STEM+'.md':PROTOCOL_SHA}).items():seal(BASE/n,h)
    r=read(BASE/(PARENT+'_RESULT.json'));receipt=read(BASE/(PARENT+'_RECEIPT.json'));m=read(BASE/(PARENT+'_MANIFEST.json'))
    require(receipt['source_sha256']==PINS['native_energy_selective_calorimeter_ports_v001.py'] and receipt['result_sha256']==PINS[PARENT+'_RESULT.json'],'Completed parent source/result')
    require(receipt['manifest']==m==r['manifest'] and receipt['status']==r['status'] and not r['checks']['failures'],'Accepted whole parent envelope')
    require(receipt['checkpoint_count']==144 and r['census']['positive_pair_IDs']==2256 and len(r['checkpoint_references'])==144,'Full parent144/2256 census')
    for mapping in (m['input_sha256'],receipt['output_sha256']):
        for p,h in mapping.items():seal(p,h)
    require(sha(BASE/(PARENT+'_MANIFEST.json'))==receipt['manifest_sha256'] and sha(BASE/(PARENT+'_JOURNAL.jsonl'))==receipt['journal_sha256'],'Actual parent manifest/journal')
    events=[json.loads(v) for v in (BASE/(PARENT+'_JOURNAL.jsonl')).read_text().splitlines()];epochs={};cp=[]
    for i,e in enumerate(events):
        require(e['owner']=='root' and type(e['pid']) is int and e['pid']>0 and e['source_sha256']==receipt['source_sha256'] and e['manifest_sha256']==receipt['manifest_sha256'],'Parent complete root/source fields')
        if e['event']=='OWNER_START':require(e['epoch']==len(epochs),'Parent owner epoch');epochs[e['epoch']]=e['pid']
        elif e['event']=='CHECKPOINT':
            require(e['epoch'] in epochs and e['pid']==epochs[e['epoch']] and e['index']==len(cp),'Parent exact checkpoint epoch/index')
            seal(BASE/e['payload'],e['payload_sha256']);seal(BASE/e['commit'],e['commit_sha256']);cp.append(e)
            c=read(BASE/e['commit']);require(c==dict(source_sha256=receipt['source_sha256'],manifest_sha256=receipt['manifest_sha256'],owner='root',pid=e['pid'],epoch=e['epoch'],index=e['index'],stage=e['stage'],payload=e['payload'],payload_sha256=e['payload_sha256']),'Parent exact complete commit')
        elif e['event']=='OWNER_COMPLETE':require(i==len(events)-1 and e['epoch'] in epochs and e['pid']==epochs[e['epoch']] and e['status']==r['status'] and e['result_sha256']==receipt['result_sha256'] and e['checkpoint_count']==144,'Parent natural terminal identity')
        else:raise AssertionError('Unexpected parent owner lifecycle')
    require(events[0]['event']=='OWNER_START' and events[-1]['event']=='OWNER_COMPLETE' and len(cp)==144,'Full completed144 parent prefix')
    require([c['stage'] for c in cp]==[v['stage'] for v in r['checkpoint_references']] and len(list(BASE.glob(PARENT+'_CP*_COMMIT.json')))==144,'Parent stage/file census')
    witness=[]
    for q,index in ((0,0),(1,72)):
        p=read(BASE/(PARENT+'_CP'+str(index).zfill(4)+'.json'));w=p['witness'];require(p['stage']=='SPECTRAL_'+str(q) and w['q']==q and w['pair_count']==1128 and len(w['groups'])==48,'Selected complete spectral identity')
        require([i for g in w['groups'] for i in g['indices']]==list(range(64)) and [g['ID'] for g in w['groups']]==list(range(48)),'Complete ordered energy partition')
        require(sorted(p['ID'] for g in w['gap_groups'] for p in g['pairs'])==sorted(f'{i}:{k}' for i in range(48) for k in range(i+1,48)),'All positive pairIDs, no filtering')
        require(len(w['incidence_spectral'])==2 and w['groups'][0]['qualified'] and len(w['groups'][0]['indices'])==1 and w['uncertainty']['directed_interval'] is False,'Inherited complete incidence/ground/resolution scope');witness.append(w)
    packet=read(BASE/'NATIVE_THERMAL_PACKET_V001_RESULTS.json');require(packet['status']=='COMPLETE' and not packet['payload']['failures'] and hashlib.sha256(canonical(packet['payload'])[:-1]).hexdigest()==packet['payload_sha256'],'Complete coherent source packet')
    require(packet['freeze_sha256']==PINS['NATIVE_THERMAL_PACKET_V001_FROZEN.json'] and len(packet['payload']['sectors'])==2,'Original physical parameter/preparation ancestry')
    return witness,packet['payload'],dict(parent_status=r['status'],parent_census=r['census'],parent_check_counts=r['checks']['counts'],parent_checkpoint_count=144)

def carr(v,np):return np.asarray(v['real'],float)+1j*np.asarray(v['imag'],float)
def cjson(v):return dict(real=v.real.tolist(),imag=v.imag.tolist())
def control(checks,name,error,tol,**ids):
    error=float(error);checks.append(dict(name=name,error=error,tolerance=tol,passed=bool(math.isfinite(error) and error<=tol),**ids))

def window(nu,T,np):
    nu=np.asarray(nu,float);a=2*math.pi/T;x=nu*T/2;phase=np.exp(1j*x)
    entire=T*phase*(3*np.sinc(x/math.pi)/8+(np.sinc(x/math.pi+1)+np.sinc(x/math.pi-1))/4+(np.sinc(x/math.pi+2)+np.sinc(x/math.pi-2))/16)
    out=entire.copy();far=abs(nu)>2.5*a
    out[far]=3*a**4*phase[far]*np.sin(x[far])/(nu[far]*(nu[far]**2-a*a)*(nu[far]**2-4*a*a))
    return out

def quadrature_window(nu,T,order,np):
    x,w=np.polynomial.legendre.leggauss(order);ts=T*(x+1)/2;ws=T*w*np.sin(math.pi*ts/T)**4/2
    flat=np.asarray(nu,float).reshape(-1);out=np.zeros(flat.shape,complex)
    for t,v in zip(ts,ws):out+=v*np.exp(1j*flat*t)
    return out.reshape(np.shape(nu))

def source_sector(w,sector,np,checks):
    q=w['q'];E=np.asarray(w['eigenvalues'],float);V=carr(w['eigenvectors'],np);H=carr(w['native_H'],np)
    require(E.shape==(64,) and V.shape==H.shape==(64,64) and bool(np.all(np.diff(E)>=0)),'Entire64 native spectral axes/order')
    scale=max(float(np.linalg.norm(H,'fro')),1.);ident=np.eye(64)
    control(checks,'native_H_hermitian',np.linalg.norm(H-H.conj().T,'fro')/scale,2e-10,q=q)
    control(checks,'saved_frame_Gram',np.linalg.norm(V.conj().T@V-ident,'fro'),2e-10,q=q)
    control(checks,'saved_eigensystem',np.linalg.norm(H@V-V*E,'fro')/scale,2e-10,q=q)
    require(len(sector['holds'])==22 and sector['record_occupation']==q,'Original complete22 holds/record branch')
    states=[];labels=[]
    for d in sector['holds']:
        psi=carr(d['state_vector'],np);require(psi.shape==(64,),'Complete coherent source vector')
        norm=float(np.vdot(psi,psi).real);energy=float(np.vdot(psi,H@psi).real)
        control(checks,'incoming_norm',abs(norm-1),2e-10,q=q,preparation=d['preparation'],age=d['age'])
        control(checks,'absolute_incoming_energy',abs(energy-d['energy'])/max(1.,abs(energy)),2e-10,q=q,preparation=d['preparation'],age=d['age'])
        states.append(V.conj().T@psi);labels.append(dict(preparation=d['preparation'],age=d['age'],absolute_native_energy=energy,incoming_norm=norm,state_source='UNCHANGED_COHERENT_HOLD'))
    groundpsi=V[:,w['groups'][0]['indices'][0]];ground=V.conj().T@groundpsi;states.append(ground);labels.append(dict(preparation='complete_native_ground',age=None,absolute_native_energy=float(np.vdot(groundpsi,H@groundpsi).real),incoming_norm=float(np.vdot(groundpsi,groundpsi).real),state_source='INHERITED_QUALIFIED_RANK1_SAVED_PHYSICAL_FRAME_COLUMN_WITHOUT_RENORMALIZATION'))
    return E,V,H,np.column_stack(states),labels

def catalog(w,E,V,states,labels,np,checks):
    q=w['q'];groups=w['groups'];mapping={p['ID']:dict(gap_group_ID=g['ID'],inherited_status=g['status'],group_span=g['span']) for g in w['gap_groups'] for p in g['pairs']}
    all_edges=[]
    for edge,rawO in zip(EDGES,w['incidence_spectral']):
        O=carr(rawO,np);require(O.shape==(64,64),'Full64 incidence source')
        diagonal=np.asarray([float((word>>edge)&1) for word in range(16) for carrier in range(4)])
        control(checks,'incidence_Hermitian',np.linalg.norm(O-O.conj().T,'fro'),2e-10,q=q,edge=edge)
        control(checks,'incidence_projector',np.linalg.norm(O@O-O,'fro'),2e-10,q=q,edge=edge)
        control(checks,'literal_full_incidence',np.linalg.norm(O-V.conj().T@(diagonal[:,None]*V),'fro'),2e-10,q=q,edge=edge)
        rows=[];elastic=[];mom7=np.zeros(23);mom8=np.zeros(23);upper7=np.zeros(23);upper8=np.zeros(23);total=np.zeros(23)
        for i,g in enumerate(groups):
            high=g['indices'];c=states[high];full=O[:,high]@c;total+=np.sum(abs(full)**2,axis=0)
            z=O[np.ix_(high,high)]@c;elastic.append(dict(group_ID=i,rank=len(high),source_weight=np.sum(abs(z)**2,axis=0).tolist(),qualified=g['qualified'],width=g['width']))
            for j in range(i):
                lo=groups[j]['indices'];block=O[np.ix_(lo,high)];a=block@c;weights=np.sum(abs(a)**2,axis=0);d=g['energy']-groups[j]['energy']
                delta=w['uncertainty']['ordered_eigenvalue_error_estimate'];pad=w['uncertainty']['roundoff_pad'];lower=float(min(E[high])-max(E[lo])-2*delta-pad);upper=float(max(E[high])-min(E[lo])+2*delta+pad)
                require(d>0,'Ordered positive center gap');mom7+=d**7*weights;mom8+=d**8*weights;upper7+=max(upper,0.)**7*weights;upper8+=max(upper,0.)**8*weights
                rows.append(dict(pair_ID=f'{j}:{i}',low=j,high=i,gap_center=d,gap_estimate_lower=lower,gap_estimate_upper=upper,interval_directed=False,low_rank=len(lo),high_rank=len(high),source_Frobenius_squared=float(np.sum(abs(block)**2)),stationary_block_weights=weights.tolist(),block_qualified=bool(g['qualified'] and groups[j]['qualified']),**mapping[f'{j}:{i}']))
        require(len(rows)==1128 and len(elastic)==48,'Complete1128 downward/48 elastic source catalog')
        moments=[];factor=2/(945*math.pi)
        for k,label in enumerate(labels):
            norm=float(np.vdot(states[:,k],states[:,k]).real);pop=[float(np.vdot(states[g['indices'],k],states[g['indices'],k]).real) for g in groups]
            control(checks,'block_population_completeness',abs(sum(pop)-norm),2e-10,q=q,edge=edge,state=k)
            moments.append(dict(**label,group_population=pop,stationary_block_total_source_weight=float(total[k]),moment7_center=float(mom7[k]),moment8_center=float(mom8[k]),moment7_gap_estimate_upper=float(upper7[k]),moment8_gap_estimate_upper=float(upper8[k]),conditional_center_rate_majorant_coefficient=factor*float(mom7[k]),conditional_center_power_majorant_coefficient=factor*float(mom8[k]),scope='ENERGY_BLOCK_DEPHASED_DIAGNOSTIC_WITHIN_INHERITED_NONDIRECTED_RESOLUTION; NOT_THE_ACTUAL_COHERENT_STATE_OR_EXACT_DEGENERACY_CERTIFICATE'))
        all_edges.append(dict(q=q,edge=edge,groups=groups,uncertainty=w['uncertainty'],states=labels,downward_rows=rows,elastic_rows=elastic,stationary_moments=moments,rate_units='coefficient*kappa^2*r^6*Eunit/hbar',power_units='coefficient*kappa^2*r^6*Eunit^2/hbar',r='R_cell*Eunit/(hbar*c_p)',unresolved_rows_retained=True))
    return all_edges

def finite_windows(w,E,states,labels,np,checks):
    q=w['q'];diff=E[:,None]-E[None,:];span=float(E[-1]-E[0]);templates=[];rows=[]
    for T in WINDOWS:
        a=2*math.pi/T;limits=np.asarray((0.,a,-a,2*a,-2*a));expected=np.asarray((3*T/8,-T/4,-T/4,T/16,T/16))
        control(checks,'exact_window_removable_limits',np.max(abs(window(limits,T,np)-expected))/T,2e-11,q=q,T=T)
        for omega in FREQUENCIES:
            nu=omega+diff;S=window(nu,T,np);s128=quadrature_window(nu,T,ORDERS[0],np);s256=quadrature_window(nu,T,ORDERS[1],np)
            e128=float(np.max(abs(S-s128))/T);e256=float(np.max(abs(S-s256))/T);eref=float(np.max(abs(s128-s256))/T)
            control(checks,'closed_vs256_window',e256,2e-11,q=q,T=T,omega=omega);control(checks,'128_vs256_window',eref,2e-11,q=q,T=T,omega=omega)
            templates.append(dict(q=q,T=T,total_photon_energy_native=omega,full_frequency_argument=nu.tolist(),closed_window=cjson(S),maximum_argument_phase=float(np.max(abs(nu))*T),closed128_error=e128,closed256_error=e256,refinement_error=eref))
            for edge,rawO in zip(EDGES,w['incidence_spectral']):
                O=carr(rawO,np);C=O*S;out=C@states;norms=np.sum(abs(states)**2,axis=0);raw=np.sum(abs(out)**2,axis=0);means=np.sum(states.conj()*out,axis=0);connected=raw-abs(means)**2/norms
                P2=float(np.sum(abs(O)**2));tail_start=max(32.,2*span,6*a);tail_constant=(972*a**4/5)**2*P2
                for k,label in enumerate(labels):
                    scale=(3*T/8)**2*P2*float(norms[k]);control(checks,'coherent_function_norm_bound',max(0.,float(raw[k])-scale)/max(scale,1e-280),2e-10,q=q,edge=edge,T=T,omega=omega,state=k)
                    control(checks,'connected_Cauchy',max(0.,-float(connected[k]))/max(scale,1e-280),2e-10,q=q,edge=edge,T=T,omega=omega,state=k)
                    rows.append(dict(q=q,edge=edge,T_native=T,total_photon_energy_native=omega,**label,source_frame_norm=float(norms[k]),raw_CdaggerC=float(raw[k]),coherent_mean=[float(means[k].real),float(means[k].imag)],connected_variance=float(connected[k]),uniform_ball_pair_density_majorant=float(omega**7*raw[k]/(945*math.pi**2)),uniform_ball_energy_density_majorant=float(omega**8*raw[k]/(945*math.pi**2)),tail_start_native=tail_start,pair_tail_majorant_coefficient=tail_constant*float(norms[k])/(1890*math.pi**2*tail_start**2),energy_tail_majorant_coefficient=tail_constant*float(norms[k])/(945*math.pi**2*tail_start),probability_units='density_majorant*kappa^2*r^6*dOmega_native',energy_units='density_majorant*kappa^2*r^6*Eunit*dOmega_native',scope='ACTUAL_COHERENT_SOURCE_FUNCTION_NOT_INTEGRATED_RADIATION_OR_NATIVE_DYSON_DEBIT'))
    require(len(templates)==24 and len(rows)==1104,'Complete24 matrices/1104 coherent source rows per q')
    return dict(q=q,templates=templates,rows=rows,UV_majorant='For Omega>=max(2 spectral_span,6a): |S|<=(972/5)a^4/Omega^5. Source norm uses full O Frobenius and incoming norm; probability tail~Omega^-2, energy tail~Omega^-1.',absolute_native_H_retained=True,native_energy_change_computed=False,switching_work_computed=False,continuum_integration_computed=False)

def main():
    global SOURCE_SHA,MANIFEST_SHA,ENTERED
    require(not list(BASE.glob(STEM+'_*')),'Entire exclusive runtime prefix absent; no resume/overwrite')
    SOURCE_SHA=sha(__file__);tick=time.monotonic();witness,packet,parent=authenticate()
    for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ.setdefault(k,'1')
    import numpy as np
    manifest=dict(source_sha256=SOURCE_SHA,input_sha256=SEALS.copy(),parent=parent,edges=list(EDGES),windows=list(WINDOWS),frequencies=list(FREQUENCIES),quadrature_orders=list(ORDERS),census=dict(record_sectors=2,states_per_q=23,source_preparation_cases=92,downward_rows=4512,elastic_rows=192,source_function_rows=2208,window_templates=48,checkpoints=6),numpy_version=np.__version__,native_units='tau=Eunit*t_proper/hbar; Omega_native=hbar*(omega+omega_prime)/Eunit',physical_scale='Eunit,R_cell,kappa symbolic and globally common; no value/frequency/support fit',scope='FULL_SOURCE_CATALOG_AND_COHERENT_FREQUENCY_FUNCTION_ONLY; NO_EIGEN_OR_H_EVOLUTION_OR_CONTINUUM_INTEGRATION')
    MANIFEST_SHA=write(STEM+'_MANIFEST.json',manifest);ENTERED=True;event('OWNER_START');checkpoint('AUTH',dict(parent=parent,input_count=len(SEALS)))
    checks=[];prepared=[];catalogs=[];windows=[]
    for q,w in enumerate(witness):
        E,V,H,states,labels=source_sector(w,packet['sectors'][q],np,checks);prepared.append((E,states,labels));data=catalog(w,E,V,states,labels,np,checks);catalogs.extend(data);checkpoint('CATALOG_Q'+str(q),dict(q=q,catalog=data,checks=checks.copy()))
    for q,w in enumerate(witness):
        E,states,labels=prepared[q];data=finite_windows(w,E,states,labels,np,checks);windows.append(data);checkpoint('WINDOW_Q'+str(q),dict(window=data,checks=checks.copy()))
    require(sum(len(v['downward_rows']) for v in catalogs)==4512 and sum(len(v['elastic_rows']) for v in catalogs)==192 and sum(len(v['rows']) for v in windows)==2208,'Frozen entire source census')
    # 3 spectral +44 hold +6 incidence +46 population +3 pole +48 quadrature +2208 source controls per q.
    require(len(checks)==4716,'Frozen4716 arithmetic source/control census')
    failed=[v for v in checks if not v['passed']];status='OUTGOING_SOURCE_FUNCTION_ARITHMETIC_PASS' if not failed else 'OUTGOING_SOURCE_FUNCTION_ARITHMETIC_FAILED'
    checkpoint('SUMMARY',dict(status=status,checks=len(checks),failures=len(failed),census=manifest['census']))
    recheck();result=dict(status=status,manifest=manifest,catalogs=catalogs,coherent_windows=windows,arithmetic_controls=checks,elapsed_seconds=time.monotonic()-tick,near_degeneracy_scope='Inherited finite numerical resolution, never exact/directed certification',energy_ledger='Full absolute native H retained. Source functions and weak symbolic bounds do not compute complete coherent native energy/no-photon Dyson terms or switch work. No pair-only debit substituted.',thermal_or_history_qualified=False)
    rh=write(STEM+'_RESULT.json',result);report=('# Native registered-cell outgoing source V001\n\n'+status+'. '+str(len(checks)-len(failed))+'/'+str(len(checks))+' arithmetic controls. All4512 downward blocks,192 elastic blocks,92 preparations and2208 coherent frequency functions retained. Symbolic global support/unit/coupling; no integrated rate, escaped photon energy, native/no-photon debit, thermal origin or history qualification.\n').encode();rp=BASE/(STEM+'_REPORT.md')
    with rp.open('xb') as f:f.write(report)
    rp.chmod(0o444);CREATED[str(rp)]=sha(rp);event('OWNER_COMPLETE',status=status,result_sha256=rh,checkpoint_count=6,control_count=len(checks))
    jp=BASE/(STEM+'_JOURNAL.jsonl');jp.chmod(0o444);CREATED[str(jp)]=sha(jp);ev=[json.loads(v) for v in jp.read_text().splitlines()]
    require([v['event'] for v in ev]==['OWNER_START']+['CHECKPOINT']*6+['OWNER_COMPLETE'] and [v['stage'] for v in ev[1:7]]==list(STAGES),'Own full6-stage natural closure')
    require(all(v['owner']=='root' and v['pid']==os.getpid() and v['source_sha256']==SOURCE_SHA and v['manifest_sha256']==MANIFEST_SHA for v in ev),'Own full root/source epoch')
    recheck();write(STEM+'_RECEIPT.json',dict(status=status,source_sha256=SOURCE_SHA,input_sha256=SEALS,output_sha256=CREATED.copy(),manifest_sha256=MANIFEST_SHA,journal_sha256=sha(jp),result_sha256=rh,checkpoint_count=6,control_count=len(checks)));recheck();return 0 if not failed else 3

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--execute',action='store_true');args=ap.parse_args()
    if not args.execute:raise SystemExit('Author/static review only; root --execute after full review')
    try:raise SystemExit(main())
    except Exception:
        if ENTERED and not (BASE/(STEM+'_RESULT.json')).exists():
            write(STEM+'_FAILED.json',dict(time=now(),owner='root',pid=os.getpid(),source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,traceback=traceback.format_exc(),created=CREATED.copy()));event('FAILED')
        raise

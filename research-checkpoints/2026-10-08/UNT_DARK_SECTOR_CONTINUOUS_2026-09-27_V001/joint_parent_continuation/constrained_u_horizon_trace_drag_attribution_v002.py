"""Prospective saved-only endpoint trace/drag attribution; root execution only."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,ast,hashlib,json,math,os,time,traceback

BASE=Path(__file__).resolve().parent
STEM='CONSTRAINED_U_HORIZON_TRACE_DRAG_ATTRIBUTION_V002'
PARENT='CONSTRAINED_U_GALAXY_HORIZON_ACTUAL_OPACITY_V001'
PENDING_COMPLETED_PARENT=False
PROTOCOL_SHA='9817b4049850b64a81388d792f968c80a677ccb689232eff391abf22d258b022'
PINS={
 'constrained_u_horizon_trace_drag_attribution_v001.py':'767dad2f03b7d0d325e34ef169feda912177ed4e0610e41376c8530961dd9c2f',
 'CONSTRAINED_U_HORIZON_TRACE_DRAG_ATTRIBUTION_V001.md':'fd72552c149cd227702876ab649fa314988da54003e529e0418b22607d5c533e',
 'constrained_u_galaxy_horizon_actual_opacity_v001.py':'7b77dad9b5e7b28fad8616325139b526364016087dfa916d31cfe78dc5a18dc1',
 'CONSTRAINED_U_GALAXY_HORIZON_ACTUAL_OPACITY_V001.md':'1933878083169615d6820c791c7d017568778225dc82ada68d8771f1006e8be8',
 'constrained_u_clock_gradient_early_transfer_v004.py':'a4e78b6467b0ba5884c8da2081ff580378b4afb839a90cec548fcf30a389fa07',
 'CONSTRAINED_U_GALAXY_SCALE_REGULAR_SEED_AND_RETARDED_RADIATION_KERNEL_V002.md':'2d66ca4ec9c35bcd67c29914d29a634c1968ed1c2e7e8ab5eb7ba99cdf5b1f47',
 'CONSTRAINED_U_GALAXY_HORIZON_ACTUAL_OPACITY_V001_RESULT.json':'59897a17c245dac41a49d02d4961dbaee1a91471997b4cf64f32235fb7f9365b',
 'CONSTRAINED_U_GALAXY_HORIZON_ACTUAL_OPACITY_V001_RECEIPT.json':'1df6d6a4586b0314dae3c189f3b7f099855f402242c4ebbe74417e2cfd1ef70c'}
TRIALS=[('BASE',512,32,1,3e-8),('TIME',1024,32,1,3e-8),
 ('FINE',2048,32,1,3e-8),('MODES',2048,64,1,3e-8),
 ('SOURCE',2048,32,2,3e-8),('START',2176,32,1,2e-8)]
OMEGAS=[.1,1.,10.,100.]
SPECIES=['baryon','photon','neutrino','phase']
EPS=2.220446049250313e-16
ROUNDING_MULTIPLIER=4096.
ABSOLUTE_ARITHMETIC_FLOOR=1e-280
SCOPE='Saved coarse snapshot endpoint identities only; no trajectory, source fit, physical qualification or per-step-maximum reconstruction'
SEALS={};CREATED={};SOURCE_SHA=None;MANIFEST_SHA=None;ENTERED=False

def require(ok,message):
    if not ok:raise AssertionError(message)
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read(path):return json.loads(Path(path).read_text())
def canonical(value):return (json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def finite_tree(value):
    if value is None or type(value) in (bool,int,str):return
    if type(value) is float:require(math.isfinite(value),'Finite saved number');return
    if isinstance(value,list):
        for x in value:finite_tree(x)
        return
    if isinstance(value,dict):
        require(all(type(k) is str for k in value),'Saved string keys')
        for x in value.values():finite_tree(x)
        return
    raise AssertionError('Noncanonical saved type')
def write(name,value):
    finite_tree(value);data=canonical(value);path=BASE/name
    with path.open('xb') as f:f.write(data)
    path.chmod(0o444);CREATED[str(path)]=sha(path);return sha(path)
def now():return datetime.now(timezone.utc).isoformat()
def event(kind,**fields):
    value=dict(time=now(),event=kind,owner='root',pid=os.getpid(),source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,**fields)
    finite_tree(value)
    with (BASE/(STEM+'_JOURNAL.jsonl')).open('a') as f:f.write(canonical(value).decode())
def seal(path,digest):
    path=Path(path).resolve()
    require(path.is_relative_to(BASE.parent.parent) or path==Path('/usr/bin/clang').resolve(),'Owned inherited path/declared compiler')
    require(sha(path)==digest,'Immutable input '+str(path))
    require(str(path) not in SEALS or SEALS[str(path)]==digest,'Consistent input seal');SEALS[str(path)]=digest
def recheck():
    require(sha(__file__)==SOURCE_SHA,'Immutable own source')
    for path,digest in dict(SEALS,**CREATED).items():require(sha(path)==digest,'Immutable input/output '+path)
def arithmetic_check(checks,name,left,right,operation_terms,**labels):
    error=abs(left-right);scale=math.fsum(abs(x) for x in operation_terms)
    tolerance=ROUNDING_MULTIPLIER*EPS*scale+ABSOLUTE_ARITHMETIC_FLOOR
    checks.append(dict(name=name,left=left,right=right,error=error,operation_scale=scale,
                       tolerance=tolerance,passed=bool(math.isfinite(error) and error<=tolerance),**labels))

def authenticate():
    require(not PENDING_COMPLETED_PARENT and PROTOCOL_SHA!='PENDING','Pending completed-parent freeze refuses execution')
    for name,digest in dict(PINS,**{STEM+'.md':PROTOCOL_SHA}).items():seal(BASE/name,digest)
    result=read(BASE/(PARENT+'_RESULT.json'));receipt=read(BASE/(PARENT+'_RECEIPT.json'))
    finite_tree(result);finite_tree(receipt);lineage=result['lineage']
    require(receipt['source_sha256']==PINS['constrained_u_galaxy_horizon_actual_opacity_v001.py'] and receipt['result_sha256']==PINS[PARENT+'_RESULT.json'],'Exact completed parent source/result')
    require(receipt['status']==result['status'] and receipt['checkpoint_count']==83,'Parent status/83 checkpoints')
    qualified=all(x['passed'] for x in result['numerical_gates']+result['optical_map_controls'])
    require(len(result['numerical_gates'])==670 and len(result['optical_map_controls'])==36 and result['numerical_gate_count']==670 and result['all_numerical_gates_passed']==qualified,'Preserved670+36 parent dispositions')
    require(result['status']==('COUPLED_HORIZON_ARITHMETIC_PASS' if qualified else 'COUPLED_HORIZON_ARITHMETIC_FAILED'),'Exact parent qualification label')
    require(lineage['source_sha256']==receipt['source_sha256'] and lineage['trials']==[list(x) for x in TRIALS] and lineage['omegas']==OMEGAS,'Exact parent physical trial census')
    for path,digest in receipt['input_sha256'].items():seal(path,digest)
    for path,digest in receipt['output_sha256'].items():seal(path,digest)
    mp=BASE/(PARENT+'_MANIFEST.json');jp=BASE/(PARENT+'_JOURNAL.jsonl')
    seal(mp,receipt['manifest_sha256']);seal(jp,receipt['journal_sha256']);require(read(mp)==lineage,'Exact parent manifest')
    events=[json.loads(line) for line in jp.read_text().splitlines()];expected=[(t[0],i) for t in TRIALS for i in sorted(set(list(range(0,t[1]+1,128))+[t[1]]))]
    seen=[];epoch=None;prefix={};last_step={}
    for index,e in enumerate(events):
        require(e['owner']=='root' and type(e['pid']) is int and e['pid']>0 and e['source_sha256']==receipt['source_sha256'] and e['manifest_sha256']==receipt['manifest_sha256'],'Parent root/source/manifest event')
        if e['event'] in ('OWNER_START','OWNER_RESUME'):
            require(e['event']==('OWNER_START' if epoch is None else 'OWNER_RESUME'),'Parent owner lifecycle');epoch=e['pid']
        elif e['event']=='CHECKPOINT':
            require(epoch is not None and e['pid']==epoch,'Parent current owner epoch')
            trial,n=e['trial'],e['nstep'];seen.append((trial,n));spec=next(t for t in TRIALS if t[0]==trial)
            pn=PARENT+'_'+trial+'_CP_'+str(n).zfill(6)+'.json';cn=pn[:-5]+'_COMMIT.json'
            seal(BASE/pn,e['payload_sha256']);seal(BASE/cn,e['commit_sha256']);cp=read(BASE/pn);commit=read(BASE/cn)
            require(commit==dict(lineage=lineage,trial=trial,nstep=n,payload=pn,sha256=e['payload_sha256']),'Parent exact byte commit')
            require(cp['lineage']==lineage and (cp['trial'],cp['nstep'],cp['step_count'],cp['ns'],cp['stride'])==(trial,n,spec[1],spec[2],spec[3]),'Parent complete checkpoint labels')
            finite_tree(cp);require(len(cp['states'])==4 and all(len(y)==20+2*spec[2] for y in cp['states']),'Parent full state axes')
            require(cp['snapshots'] and cp['snapshots'][-1]['nstep']==n and [v['state'] for v in cp['snapshots'][-1]['cases']]==cp['states'],'Parent final snapshot/state closure')
            require(trial not in prefix or cp['snapshots'][:len(prefix[trial])]==prefix[trial],'Parent entire immutable snapshot prefix')
            prefix[trial]=cp['snapshots'];last_step[trial]=n
        elif e['event']=='OWNER_COMPLETE':
            require(index==len(events)-1 and e['pid']==epoch and e['status']==result['status'] and e['result_sha256']==receipt['result_sha256'] and (e['gate_count'],e['optical_control_count'],e['checkpoint_count'])==(670,36,83),'Parent exact natural terminal record')
        else:raise AssertionError('Unexpected parent lifecycle event')
    require(events and events[0]['event']=='OWNER_START' and events[-1]['event']=='OWNER_COMPLETE' and seen==expected,'Parent full83 global ordered checkpoint census')
    require([r['label'] for r in result['rows']]==[t[0] for t in TRIALS],'All six parent rows')
    for row,spec in zip(result['rows'],TRIALS):
        require(last_step[spec[0]]==spec[1] and row['snapshots']==prefix[spec[0]],'Result/full checkpoint snapshot identity')
        start=128 if spec[0]=='START' else 0;common=spec[1]-start
        expected_snaps=[0]+[i for i in range(1,spec[1]+1) if i>=start and (i-start)%(common//32)==0]
        require([s['nstep'] for s in row['snapshots']]==expected_snaps and all(len(s['cases'])==4 for s in row['snapshots']),'33common/START34 complete saved snapshots')
    require(sum(len(row['snapshots'])*4 for row in result['rows'])==796,'Full796 case-frame census')
    require(len(list(BASE.glob(PARENT+'_*_CP_*_COMMIT.json')))==83 and len(list(BASE.glob(PARENT+'_*_CP_*.json')))==166,'Parent complete checkpoint file census')
    require(lineage['fixed']['k_Mpc_inverse']==10. and lineage['fixed']['curvature']==1e-5,'Same frozen physical wavenumber/amplitude')
    return result,receipt

def endpoint(case,fixed):
    y=case['state'];bg=case['background'];h,b,r,w,c=(bg[k] for k in ('h','b','r','w','cs'))
    rg,rn=r*fixed['fgamma'],r*(1-fixed['fgamma']);q=10.*299792458./(1000*fixed['Hunit']*case['a'])
    phi,psi=case['Phi'],case['Psi'];ub,ug,un,V=(y[i] for i in (2,4,6,8));g=case['thermal']['g'];rb=3*b/(4*rg)
    Gamma=y[7]+3*h*V;drag_b=g/rb*(ug-ub);drag_g=g*(ub-ug)
    p=[b,4*rg/3,4*rn/3,w];u=[ub,ug,un,V];px=[-3*b,-4*p[1],-4*p[2],-3*(1+c)*w]
    # Exact literal proper-time parent Euler rows, converted to log-a derivatives.
    ux=[(phi+drag_b)/h,(h*ug+phi+y[3]/4-y[9]/2+drag_g)/h,
        (h*un+phi+y[5]/4-y[17]/2)/h,(phi+c*Gamma)/h]
    ux_drag=[drag_b/h,drag_g/h,0.,0.]
    ux_nondrag=[phi/h,(h*ug+phi+y[3]/4-y[9]/2)/h,
                (h*un+phi+y[5]/4-y[17]/2)/h,(phi+c*Gamma)/h]
    terms=[p[i]*ux[i]+px[i]*u[i] for i in range(4)]
    mom=math.fsum(p[i]*u[i] for i in range(4));mx=math.fsum(terms)
    pressure=c*w*y[7]+(rg*y[3]+rn*y[5])/3;shear=rg*y[9]+rn*y[17]
    force_parts=[3*mom,bg['h_dt']*phi/h,q*q*(psi-phi)/(3*h),-pressure/h]
    force=math.fsum(force_parts);drag_parts=[p[i]*ux_drag[i] for i in range(4)]
    conservative_source=case['a']**3*((b+4*(rg+rn)/3+w)*phi+pressure-2*shear/3)/h
    return dict(x=case['x'],a=case['a'],p=p,u=u,p_x=px,u_x=ux,u_x_drag=ux_drag,u_x_nondrag=ux_nondrag,
        momentum=mom,momentum_x=mx,component_momentum_x=terms,force=force,force_parts=force_parts,
        ward=mx+force,drag_parts=drag_parts,pressure=pressure,shear=shear,conservative_source=conservative_source,
        serialized_momentum=case['normal_terms'][1]/(3*h),h=h)

def interval(left,right,labels,checks):
    dx=right['x']-left['x'];require(dx>0,'Increasing coarse snapshot interval')
    components=[];all_operations=[]
    for i,name in enumerate(SPECIES):
        p0,p1=left['p'][i],right['p'][i];u0,u1=left['u'][i],right['u'][i]
        px0,px1=left['p_x'][i],right['p_x'][i];ux0,ux1=left['u_x'][i],right['u_x'][i]
        dp,du=p1-p0,u1-u0;pb,ub=(p0+p1)/2,(u0+u1)/2
        ru=du-dx*(ux0+ux1)/2;rp=dp-dx*(px0+px1)/2
        velocity=pb*ru;background=ub*rp;product=-dx*(dp*(ux1-ux0)+du*(px1-px0))/4
        direct=p1*u1-p0*u0-dx*(p0*ux0+px0*u0+p1*ux1+px1*u1)/2
        drag=-dx*pb*(left['u_x_drag'][i]+right['u_x_drag'][i])/2
        nondrag=-dx*pb*(left['u_x_nondrag'][i]+right['u_x_nondrag'][i])/2
        terms=[p1*u1,p0*u0,dx*p0*ux0/2,dx*px0*u0/2,dx*p1*ux1/2,dx*px1*u1/2,
               velocity,background,product,dx*pb*ux0/2,dx*pb*ux1/2]
        all_operations.extend(terms)
        arithmetic_check(checks,'species_product_identity',direct,math.fsum((velocity,background,product)),terms,species=name,**labels)
        components.append(dict(species=name,coarse_velocity_residual=ru,coarse_background_residual=rp,
            velocity_term=velocity,background_term=background,product_quadrature_term=product,
            direct_species_trace=direct,velocity_increment=pb*du,velocity_drag_trapezoid=drag,
            velocity_nondrag_trapezoid=nondrag))
    dm=right['momentum']-left['momentum'];force_trapezoid=dx*(left['force']+right['force'])/2
    observed=dm+force_trapezoid;ward=dx*(left['ward']+right['ward'])/2
    decomposition=math.fsum(c['velocity_term']+c['background_term']+c['product_quadrature_term'] for c in components)+ward
    scales=[right['momentum'],left['momentum'],force_trapezoid,ward]+all_operations+[v for c in components for k,v in c.items() if k.endswith('_term')]
    arithmetic_check(checks,'whole_trace_decomposition',observed,decomposition,scales,**labels)
    direct_sum=math.fsum(c['direct_species_trace'] for c in components)+ward
    arithmetic_check(checks,'whole_component_trace_sum',observed,direct_sum,scales,**labels)
    denom=abs(right['momentum'])+abs(left['momentum'])+dx*(abs(left['force'])+abs(right['force']))/2
    normalized=abs(observed)/max(denom,1e-5*1e-18)
    conservative=right['a']**3*right['momentum']-left['a']**3*left['momentum']-dx*(left['conservative_source']+right['conservative_source'])/2
    return dict(**labels,left_x=left['x'],right_x=right['x'],left_a=left['a'],right_a=right['a'],coarse_log_span=dx,
        momentum_increment=dm,force_trapezoid=force_trapezoid,coarse_trace_residual=observed,
        original_form_coarse_trace_scale=denom,coarse_normalized_trace=normalized,
        endpoint_ward_correction=ward,decomposed_trace_residual=decomposition,components=components,
        drag_weighted_velocity_sum=math.fsum(c['velocity_drag_trapezoid'] for c in components),
        conservative_a3_momentum_residual=conservative,
        scope='Stored adjacent snapshots only; neither a parent per-step error nor a new success disposition')

def checkpoint(stage,data):
    recheck();pn=STEM+'_'+stage+'_CP.json';cn=STEM+'_'+stage+'_CP_COMMIT.json'
    payload=dict(stage=stage,owner='root',pid=os.getpid(),source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,data=data)
    digest=write(pn,payload);commit=dict(stage=stage,payload=pn,payload_sha256=digest,owner='root',pid=os.getpid(),source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA)
    ch=write(cn,commit);event('CHECKPOINT',stage=stage,payload=pn,payload_sha256=digest,commit=cn,commit_sha256=ch)

def main():
    global SOURCE_SHA,MANIFEST_SHA,ENTERED
    runtime=[BASE/(STEM+s) for s in ('_MANIFEST.json','_JOURNAL.jsonl','_RESULT.json','_REPORT.md','_RECEIPT.json','_FAILED.json')]
    require(not any(p.exists() for p in runtime) and not any(BASE.glob(STEM+'_*_CP*')),'Entire new runtime prefix absent; no resume/overwrite')
    SOURCE_SHA=sha(__file__);parent,receipt=authenticate();start=time.monotonic();fixed=parent['lineage']['fixed']
    manifest=dict(source_sha256=SOURCE_SHA,input_sha256=SEALS.copy(),parent_status=parent['status'],scope=SCOPE,
        endpoint_count=796,interval_count=772,rounding_multiplier=ROUNDING_MULTIPLIER,absolute_arithmetic_floor=ABSOLUTE_ARITHMETIC_FLOOR,
        species=SPECIES,units='Parent proper tau=Hstar*t; displayed derivatives d/dlog(a); saved background/thermal data only')
    MANIFEST_SHA=write(STEM+'_MANIFEST.json',manifest);ENTERED=True;event('OWNER_START')
    inherited=dict(parent_status=parent['status'],numerical_gates=parent['numerical_gates'],optical_map_controls=parent['optical_map_controls'],gas_fixture_flags=parent['gas_fixture_flags'])
    checkpoint('AUTH',dict(parent_result_sha256=receipt['result_sha256'],parent_checkpoint_count=83,preserved_dispositions=inherited))
    checks=[];frames=[];intervals=[]
    for row,spec in zip(parent['rows'],TRIALS):
        all_cases=[]
        for snap in row['snapshots']:
            values=[]
            for arm,case in enumerate(snap['cases']):
                require(len(case['state'])==20+2*spec[2] and abs(case['x']-math.log(case['a']))<=4*EPS*max(1.,abs(case['x'])),'Finite parent snapshot chart')
                value=endpoint(case,fixed);labels=dict(trial=row['label'],omega=OMEGAS[arm],nstep=snap['nstep'])
                scale=[p*u for p,u in zip(value['p'],value['u'])]
                arithmetic_check(checks,'saved_momentum_identity',value['momentum'],value['serialized_momentum'],scale,**labels)
                ops=[p*ux for p,ux in zip(value['p'],value['u_x'])]+[px*u for px,u in zip(value['p_x'],value['u'])]+value['force_parts']
                arithmetic_check(checks,'instantaneous_whole_action_ward',value['momentum_x'],-value['force'],ops,**labels)
                arithmetic_check(checks,'instantaneous_drag_cancellation',math.fsum(value['drag_parts']),0.,value['drag_parts'],**labels)
                frames.append(dict(**labels,**value));values.append(value)
            all_cases.append(values)
        for index,(left,right) in enumerate(zip(all_cases[:-1],all_cases[1:])):
            for arm in range(4):
                labels=dict(trial=row['label'],omega=OMEGAS[arm],left_nstep=row['snapshots'][index]['nstep'],right_nstep=row['snapshots'][index+1]['nstep'],preparation_interval=bool(row['label']=='START' and index==0))
                intervals.append(interval(left[arm],right[arm],labels,checks))
    require(len(frames)==796 and len(intervals)==772 and len(checks)==7020,'Frozen796/772/7020 arithmetic census')
    endpoint_checks=[c for c in checks if c['name'] in ('saved_momentum_identity','instantaneous_whole_action_ward','instantaneous_drag_cancellation')]
    require(len(endpoint_checks)==2388,'Frozen2388 endpoint arithmetic identities')
    checkpoint('ENDPOINTS',dict(frames=frames,arithmetic_checks=endpoint_checks))
    checkpoint('INTERVALS',dict(intervals=intervals,arithmetic_checks=checks))
    failed=[c for c in checks if not c['passed']];status='SAVED_TRACE_ATTRIBUTION_ARITHMETIC_PASS' if not failed else 'SAVED_TRACE_ATTRIBUTION_ARITHMETIC_FAILED'
    summary=[dict(trial=t[0],omega=o,coarse_interval_count=sum(r['trial']==t[0] and r['omega']==o for r in intervals),
        maximum_coarse_normalized_trace=max(r['coarse_normalized_trace'] for r in intervals if r['trial']==t[0] and r['omega']==o),
        interpretation='Measured coarse-interval drift; no physical success gate') for t in TRIALS for o in OMEGAS]
    checkpoint('SUMMARY',dict(status=status,summary=summary,arithmetic_check_count=len(checks),arithmetic_failure_count=len(failed)))
    recheck();result=dict(status=status,manifest=manifest,parent_dispositions=inherited,frames=frames,intervals=intervals,
        arithmetic_checks=checks,summary=summary,physical_or_parent_qualification_changed=False,elapsed_seconds=time.monotonic()-start)
    rh=write(STEM+'_RESULT.json',result);report=('# Saved trace/drag/product attribution\n\n'+status+'\n\nAll796 endpoints and772 coarse snapshot intervals retained;7020 arithmetic identity checks. The original670 numerical and36 optical dispositions remain unchanged. No per-step maximum is reconstructed, and trace/drag/product drift is not a success gate.\n').encode()
    rp=BASE/(STEM+'_REPORT.md')
    with rp.open('xb') as f:f.write(report)
    rp.chmod(0o444);CREATED[str(rp)]=sha(rp);event('OWNER_COMPLETE',status=status,result_sha256=rh,checkpoint_count=4,arithmetic_check_count=len(checks))
    jp=BASE/(STEM+'_JOURNAL.jsonl');jp.chmod(0o444);CREATED[str(jp)]=sha(jp)
    events=[json.loads(line) for line in jp.read_text().splitlines()]
    require([e['event'] for e in events]==['OWNER_START']+['CHECKPOINT']*4+['OWNER_COMPLETE'] and [e['stage'] for e in events[1:5]]==['AUTH','ENDPOINTS','INTERVALS','SUMMARY'],'Own exact four-stage natural closure')
    require(all(e['owner']=='root' and e['pid']==os.getpid() and e['source_sha256']==SOURCE_SHA and e['manifest_sha256']==MANIFEST_SHA for e in events),'Own complete root/source/PID journal')
    recheck();write(STEM+'_RECEIPT.json',dict(status=status,source_sha256=SOURCE_SHA,input_sha256=SEALS,output_sha256=CREATED.copy(),manifest_sha256=MANIFEST_SHA,journal_sha256=sha(jp),result_sha256=rh,report_sha256=sha(rp),checkpoint_count=4));recheck()
    return 0 if not failed else 3

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--execute',action='store_true');args=ap.parse_args()
    if not args.execute:raise SystemExit('Root saved-only execution requires --execute after completed-parent freeze/review')
    try:raise SystemExit(main())
    except Exception:
        if ENTERED and not (BASE/(STEM+'_RESULT.json')).exists():
            write(STEM+'_FAILED.json',dict(time=now(),owner='root',pid=os.getpid(),source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,traceback=traceback.format_exc(),created=CREATED.copy()))
            event('FAILED')
        raise

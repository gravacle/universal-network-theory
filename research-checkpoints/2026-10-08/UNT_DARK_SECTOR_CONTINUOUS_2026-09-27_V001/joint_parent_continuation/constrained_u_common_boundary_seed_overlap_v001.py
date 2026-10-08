"""Bounded OLD versus REGULAR common-boundary discriminator; root execution only."""
from pathlib import Path
from datetime import datetime, timezone
import argparse,ast,hashlib,json,math,os,time
BASE=Path(__file__).resolve().parent
STEM='CONSTRAINED_U_COMMON_BOUNDARY_SEED_OVERLAP_V001'
PROTOCOL_SHA='9497ea73b1022274ede52315d3c01261f8766ec4c71b34ea7110d91a639dac00'
PINS={'constrained_u_clock_gradient_early_transfer_v005.py': 'bfee912d66cbfd91b9d80630c15cbe1cf32c4c905f0d736c4491113f01d84b20', 'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V005.md': '027233e02902b2905a5f172e3aaec6ab297a956e5e66a1f058ffbb36f66c93a6', 'constrained_u_galaxy_horizon_volterra_v003.py': '06823e14186e3dec4a20b13206ceb3b5fd4824e166f09c2a856083e276b5b273', 'CONSTRAINED_U_GALAXY_HORIZON_VOLTERRA_V003.md': 'f3ec83a84bee7291b73a02ba73d48a793ab0ec7a081baa34a963ab5e5f27fc7d', 'CONSTRAINED_U_GALAXY_SCALE_REGULAR_SEED_AND_RETARDED_RADIATION_KERNEL_V002.md': '2d66ca4ec9c35bcd67c29914d29a634c1968ed1c2e7e8ab5eb7ba99cdf5b1f47'}
SPANS={'sha': 'd58e56b684b01bf61e0cc835c278e755e664aa0f96019b39d4ef2fe6b80ae50b', 'seal': '3862936d749ebc1cfdf9523019b5593366adc9b48bf5f319f8ec1ea5c04b5d88', 'background': 'eb224e42c6c567b0339b18cdf54a1d8c4f005810b6d6952fee9efee4983b7ec2', 'Thermal': '0d4c6a2726fd817d2cfb5ba8b90a6674a288bc0484c927da719ecdef72a7cd47', 'Layout': 'f199860c3687d2acc7817eda8a00133c1ef57abb2ffbf224ddc760a90e41d2a8', 'coefficients': 'b9e6a7edca9a67031670d32dba146c289347b9253f32bf16d0f3587597125637', 'rates': '2053ec557e765a899a9468fed8a48d701e010d2f76a0aa666ab209e8dc079354', 'initial': 'a4c4a630fa849f83fbeb3f5128126807d571f308edecff24dc9891b7dabf51ab', 'stage_matrix': '0b02c3bb7a1c4d2d4a9ce6e5ddfe964965042d013ba916d50a4eeda63cb040fe', 'tridiagonal_blocks': 'aa7b86cf64ba2f4b4ccccebc676f120a57270ca5203b8ff4555c19743f2e378f', 'block_stage_solve': 'a44e8a47d27984773c73bc3c32f38e83444502417310d6e126d836daf0ae0a56', 'require': '404261933c28a75c12593bf939703277ec0dd231219dfafff8a8577fb8b46dd0', 'coordinate_scales': 'f0903a138a434ae053aba727d97e91e8c12385e6870a808600b1a6ba4983c01e', 'residual': '7344e575e1fc8058685dec9c678d79d42243b3783455ae37c5818cef020e65e0', 'refined_stages': 'ed7e137c739e59cd211f8b33981200e92da0096ca3d0f8eec93467327959d0b8', 'radau_step': '7cbdcca7d319312c2bbe8ffaf4fa0f22e5655867a98c54e77bbf21dd8da28eb6', 'snapshot': '842bef984f2904f4eabdb467fc1bdd6e90f83d472874507c57dbd8aea8d62b7f', 'authenticate': '19187ee4f2a19960ba605284f0dd8b2fde648bff861ce7e1f4a5e82fb608ea9c', 'regular_seed': 'fcfc6f1e6f8baf62058c99448ca332592332ce0da93f3810c1c7dfddf0b896fe'}
V5='constrained_u_clock_gradient_early_transfer_v005.py'
H3='constrained_u_galaxy_horizon_volterra_v003.py'
FAMILIES=('OLD','REGULAR')
STEPS=(512,1024)
AI=1e-7
CURVATURE=1e-5
OMEGAS=(.1,1.,10.,100.)
READOUT_NAMES=('photon_monopole_plus_Phi','photon_velocity','baryon_velocity','Weyl','photon_quadrupole','polarization_source','neutrino_quadrupole','comoving_baryon_contrast','comoving_baryon_density','comoving_radiation_density','comoving_clock_density','polarization_density','hard_density','soft_density','normal_acceleration')
SEALS={};CREATED={};SOURCE_SHA=None;MANIFEST_SHA=None;ENTERED=False

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def require(ok,msg):
    if not ok:raise AssertionError(msg)
def read(p):return json.loads(Path(p).read_text())
def now():return datetime.now(timezone.utc).isoformat()
def seal(p,h):
    p=Path(p).resolve();require(p.is_relative_to(BASE.parent.parent) or p==Path('/usr/bin/clang').resolve(),'Input path')
    require(sha(p)==h,'Input seal '+str(p));require(str(p) not in SEALS or SEALS[str(p)]==h,'Conflicting seal');SEALS[str(p)]=h

def write(name,obj):
    data=json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n'
    p=BASE/name
    with p.open('x') as f:f.write(data)
    p.chmod(0o444);CREATED[str(p)]=sha(p);return sha(p)

def event(kind,**kw):
    obj=dict(time=now(),event=kind,owner='root',pid=os.getpid(),source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,**kw)
    with (BASE/(STEM+'_JOURNAL.jsonl')).open('a') as f:f.write(json.dumps(obj,sort_keys=True,allow_nan=False)+'\n')

def recheck():
    require(sha(__file__)==SOURCE_SHA,'Source changed')
    for p,h in SEALS.items():require(sha(p)==h,'Input changed '+p)
    for p,h in CREATED.items():require(sha(p)==h,'Output changed '+p)

def load_helpers(np):
    source=(BASE/V5).read_text();tree=ast.parse(source)
    constants={}
    wanted={'STEM','PROTOCOL_SHA','PINS','BACKGROUND_SPAN_SHA','RADAU_SPAN_SHA','COMPILER_SHA','MPC','CP','K','KB','C','CBAR','CURVATURE','BALANCE_PASSES','REFINEMENT_STEPS'}
    for n in tree.body:
        if not isinstance(n,ast.Assign):continue
        for target in n.targets:
            if isinstance(target,ast.Name) and target.id in wanted:constants[target.id]=ast.literal_eval(n.value)
            if isinstance(target,ast.Tuple) and all(isinstance(t,ast.Name) and t.id in wanted for t in target.elts):
                constants.update(zip((t.id for t in target.elts),ast.literal_eval(n.value)))
    require(set(constants)==wanted,'Complete authenticated helper constants')
    require(constants['K']==.01 and constants['CURVATURE']==CURVATURE and constants['BALANCE_PASSES']==4 and constants['REFINEMENT_STEPS']==3,'Exact source/method fixtures')
    env=dict(__file__=str(BASE/V5),__name__='seed_overlap_definition_only',np=np,math=math,Path=Path,json=json,ast=ast,hashlib=hashlib,SEALS={},**constants)
    names=set(SPANS)-{'regular_seed'};definitions=[]
    for n in tree.body:
        if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names:
            require(hashlib.sha256(ast.get_source_segment(source,n).encode()).hexdigest()==SPANS[n.name],'Helper span '+n.name);definitions.append(n)
    require({n.name for n in definitions}==names,'Definition-only whitelist')
    exec(compile(ast.Module(body=definitions,type_ignores=[]),str(BASE/V5),'exec'),env)
    fixed=env['authenticate']()
    for p,h in env['SEALS'].items():seal(p,h)
    hs=(BASE/H3).read_text();node=next(n for n in ast.parse(hs).body if isinstance(n,ast.FunctionDef) and n.name=='regular_seed')
    require(hashlib.sha256(ast.get_source_segment(hs,node).encode()).hexdigest()==SPANS['regular_seed'],'Exact regular seed')
    exec(compile(ast.Module(body=[node],type_ignores=[]),str(BASE/H3),'exec'),env)
    require(fixed['k_Mpc_inverse']==.01 and fixed['curvature']==CURVATURE,'Same physical input recovery')
    return env,fixed

def seed(family,a,omega,env,fixed,lay,therm,snodes,weights):
    if family=='OLD':
        y=env['initial'](math.log(a),fixed,lay,therm,snodes,weights)
        meta=dict(finite_curvature_target=CURVATURE,scope='Inherited leading finite-start zero-mode preparation')
    else:y,eta,meta=env['regular_seed'](a,fixed,lay,therm,snodes,weights,omega,env)
    return y,meta

def contact_controls(case,family,a,omega,env,fixed,lay,snodes,weights,meta,check):
    s=case;y=env['np'].array(s['state']);q=.01*env['CP']/(1000*fixed['Hunit']*a);h=s['background']['h']
    ids=dict(family=family,a=a,omega=omega)
    for key,tol in (('normal_error',1e-10),('trace_error',1e-10),('omitted_Euler_error',1e-10)):check('direct_'+key,s[key],tol,**ids)
    check('direct_shear',abs(s['Psi']-s['Phi']-2*s['signed_sources']['shear']/q**2)/CURVATURE,1e-13,**ids)
    if family=='OLD':
        check('old_finite_curvature',abs((s['Psi']+h*y[8])/CURVATURE-1),2e-13,**ids)
        check('old_zero_modes',float(env['np'].max(abs(y[lay.z])))+float(env['np'].max(abs(y[lay.zd]))),0.,**ids)
    else:
        R=1-fixed['fgamma'];A=CURVATURE/(1.5+2*R/5);hr=math.sqrt(fixed['OR']/fixed['rG']);q0=.01*env['CP']/(1000*fixed['Hunit'])
        f=(56*R*R+10*R-525)/(630*(25+2*R));g=-(56*R*R+580*R+525)/(630*(25+2*R))
        norm=1/fixed['eps']-math.log1p(1/fixed['eps']);Qc=fixed['Q0_over_Hstar']*math.sqrt(1+fixed['eps'])
        alpha=omega**2*float(weights@snodes**2);gamma2=A*(3*g-.25+.75*f)*(q0/hr)**2
        c3=1/(math.sqrt(1+fixed['eps'])*norm*fixed['d0']);sigma2=6*hr*Qc*q0*c3*gamma2/(alpha+env['C']*Qc**2/env['KB'])
        z6=omega**2*snodes**2*sigma2/(42*hr**2)
        check('regular_asymptotic_amplitude',abs(meta['A']/A-1)+abs(meta['asymptotic_curvature']/CURVATURE-1),2e-13,**ids)
        for name,actual,expected in (('z6',y[lay.z],z6*a**6),('zd4',y[lay.zd],6*hr*z6*a**4)):
            den=max(float(env['np'].max(abs(expected))),env['np'].finfo(float).tiny)
            check('regular_'+name,float(env['np'].max(abs(actual-expected)))/den,2e-13,**ids)

def compute_run(family,steps,env,fixed,lay,therm,snodes,weights):
    np=env['np'];x0=math.log(AI/2);xf=math.log(AI);dx=(xf-x0)/steps
    states=[];seed_meta=[]
    for om in OMEGAS:
        y,meta=seed(family,AI/2,om,env,fixed,lay,therm,snodes,weights);states.append(y);seed_meta.append(meta)
    y=np.stack(states);snapshots=[];errors=[0.]*4;dense=[0.]*4;tick=time.monotonic()
    for n in range(steps+1):
        if n%(steps//16)==0:
            x=xf if n==steps else x0+n*dx
            snapshots.append(dict(n=n,x=x,cases=[env['snapshot'](x,y[i],fixed,lay,therm,snodes,weights,om) for i,om in enumerate(OMEGAS)]))
        if n==steps:break
        for i,om in enumerate(OMEGAS):
            y[i],er,de=env['radau_step'](y[i],x0+n*dx,dx,fixed,lay,therm,snodes,weights,om,n%64==0,n==0)
            errors[i]=max(errors[i],er);dense[i]=max(dense[i],de)
        require(bool(np.all(np.isfinite(y))),'Finite entire propagated state')
        if (n+1)%128==0:print(json.dumps(dict(family=family,steps=steps,completed=n+1,elapsed=time.monotonic()-tick)),flush=True)
    require(len(snapshots)==17 and [r['n'] for r in snapshots]==list(range(0,steps+1,steps//16)) and snapshots[0]['x']==x0 and snapshots[-1]['x']==xf and all(snapshots[i]['x']<snapshots[i+1]['x'] for i in range(16)),'Full ordered overlap snapshot census')
    return dict(family=family,steps=steps,snapshots=snapshots,seed_metadata=seed_meta,stage_errors=errors,dense_errors=dense,state_names=lay.names(),snodes=snodes.tolist(),weights=weights.tolist(),elapsed_seconds=time.monotonic()-tick)

def main():
    global SOURCE_SHA,MANIFEST_SHA,ENTERED
    require(not any(BASE.glob(STEM+'_*')),'Nonresumable runtime namespace already exists')
    ENTERED=True;SOURCE_SHA=sha(__file__);tick=time.monotonic()
    for p,h in dict(PINS,**{STEM+'.md':PROTOCOL_SHA}).items():seal(BASE/p,h)
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ.setdefault(key,'1')
    import numpy as np
    env,fixed=load_helpers(np);lay=env['Layout'](32,96,128);therm=env['Thermal']('HALF',1,fixed)
    nodes,raw=np.polynomial.legendre.leggauss(32);snodes=(nodes+1)/2;weights=raw*snodes
    lineage=dict(source_sha256=SOURCE_SHA,inputs=dict(SEALS),fixed=fixed,k=.01,curvature=CURVATURE,interval=[AI/2,AI],families=list(FAMILIES),steps=list(STEPS),omegas=list(OMEGAS),numpy_version=np.__version__,spans=SPANS,ns=32,lg=96,ln=128,physical_overlap_is_gate=False,resume=False)
    MANIFEST_SHA=write(STEM+'_MANIFEST.json',lineage);event('OWNER_START')
    direct=[];runs=[];gates=[]
    def check(name,error,tolerance,**ids):
        error=float(error);gates.append(dict(name=name,error=error,tolerance=tolerance,passed=bool(math.isfinite(error) and error<=tolerance),**ids))
    check('spectrum_normalization',abs(float(sum(weights))-1),1e-13)
    for family in FAMILIES:
        for a in (AI/2,AI):
            cases=[];metas=[]
            for om in OMEGAS:
                y,meta=seed(family,a,om,env,fixed,lay,therm,snodes,weights);case=env['snapshot'](math.log(a),y,fixed,lay,therm,snodes,weights,om)
                cases.append(case);metas.append(meta);contact_controls(case,family,a,om,env,fixed,lay,snodes,weights,meta,check)
            direct.append(dict(family=family,a=a,cases=cases,metadata=metas))
        for steps in STEPS:
            recheck();row=compute_run(family,steps,env,fixed,lay,therm,snodes,weights);recheck();runs.append(row)
            name=STEM+'_'+family+'_'+str(steps)+'_CP.json';h=write(name,dict(lineage=lineage,row=row));cn=name[:-5]+'_COMMIT.json'
            ch=write(cn,dict(lineage=lineage,payload=name,sha256=h));event('CHECKPOINT',family=family,steps=steps,payload=name,sha256=h,commit_sha256=ch)
            for i,om in enumerate(OMEGAS):
                check('dynamic_stage',row['stage_errors'][i],2e-11,family=family,steps=steps,omega=om)
                check('independent_dense',row['dense_errors'][i],2e-11,family=family,steps=steps,omega=om)
                for key,tol in (('normal_error',1e-5),('trace_error',1e-10),('omitted_Euler_error',1e-10)):
                    check(key,max(s['cases'][i][key] for s in row['snapshots']),tol,family=family,steps=steps,omega=om)
    allcases=[c for d in direct for c in d['cases']]+[c for r in runs for s in r['snapshots'] for c in s['cases']]
    check('maximum_charge_root',max(c['background']['charge_error'] for c in allcases),1e-13)
    require(all(c['reaction_denominator']>0 for c in allcases),'All positive reaction denominators')
    overlaps=[];refinements=[]
    for family in FAMILIES:
        coarse,fine=[r for r in runs if r['family']==family];endpoint=next(d for d in direct if d['family']==family and d['a']==AI)
        cf=np.array([[c['readouts'] for c in s['cases']] for s in coarse['snapshots']]);ff=np.array([[c['readouts'] for c in s['cases']] for s in fine['snapshots']]);den=np.maximum(np.max(abs(ff),axis=0),CURVATURE*1e-8);err=np.max(abs(cf-ff),axis=0)/den
        modal=[]
        for i,om in enumerate(OMEGAS):
            for k,name in enumerate(READOUT_NAMES):check('time_refinement',err[i,k],1e-3,family=family,omega=om,variable=name)
            for name,idx in (('z',lay.z),('zd',lay.zd)):
                ca=np.array([s['cases'][i]['state'] for s in coarse['snapshots']])[:,idx];fa=np.array([s['cases'][i]['state'] for s in fine['snapshots']])[:,idx]
                modal.append(dict(omega=om,field=name,signed_endpoint_difference=(ca[-1]-fa[-1]).tolist(),maximum_absolute_difference=float(np.max(abs(ca-fa))),normalized_with_curvature_floor=float(np.max(abs(ca-fa))/max(float(np.max(abs(fa))),CURVATURE*1e-8)),qualification='ABSOLUTE_DIAGNOSTIC_ONLY_NO_TINY_RELATIVE_PRECISION'))
        refinements.append(dict(family=family,coarse=512,fine=1024,signed_endpoint_difference=(cf[-1]-ff[-1]).tolist(),normalization=den.tolist(),normalized_errors=err.tolist(),modal_diagnostics=modal))
        for row in (coarse,fine):
            for i,om in enumerate(OMEGAS):
                actual=row['snapshots'][-1]['cases'][i];target=endpoint['cases'][i];delta=np.array(actual['state'])-np.array(target['state']);rd=np.array(actual['readouts'])-np.array(target['readouts'])
                overlaps.append(dict(family=family,steps=row['steps'],omega=om,signed_full_state_difference=delta.tolist(),signed_readout_difference=rd.tolist(),native_z_difference=delta[lay.z].tolist(),native_zd_difference=delta[lay.zd].tolist(),signed_curvature_difference=actual['Psi']+actual['background']['h']*actual['state'][8]-target['Psi']-target['background']['h']*target['state'][8],normal_errors=[actual['normal_error'],target['normal_error']],source_ratios=[actual['source_ratios'],target['source_ratios']],qualification='STATE_DEPENDENT_OVERLAP_NOT_AN_ACCEPTANCE_GATE'))
    old=next(d for d in direct if d['family']=='OLD' and d['a']==AI);reg=next(d for d in direct if d['family']=='REGULAR' and d['a']==AI)
    distinctions=[dict(omega=om,signed_full_state_difference=(np.array(old['cases'][i]['state'])-np.array(reg['cases'][i]['state'])).tolist(),signed_readout_difference=(np.array(old['cases'][i]['readouts'])-np.array(reg['cases'][i]['readouts'])).tolist()) for i,om in enumerate(OMEGAS)]
    require(len(gates)==306 and len(allcases)==288 and len(overlaps)==16,'Frozen complete census')
    events=[json.loads(line) for line in (BASE/(STEM+'_JOURNAL.jsonl')).read_text().splitlines()]
    require([e['event'] for e in events]==['OWNER_START']+['CHECKPOINT']*4,'Exact owned checkpoint prefix')
    expected_cp={STEM+'_'+r['family']+'_'+str(r['steps'])+'_CP'+suffix for r in runs for suffix in ('.json','_COMMIT.json')}
    require({p.name for p in BASE.glob(STEM+'_*_CP*.json')}==expected_cp,'Exact four CP pairs; no orphans')
    require(all(e['owner']=='root' and e['pid']==os.getpid() and e['source_sha256']==SOURCE_SHA and e['manifest_sha256']==MANIFEST_SHA for e in events),'Entire root owner epoch')
    for e,row in zip(events[1:],runs):
        p=e['payload'];co=read(BASE/(p[:-5]+'_COMMIT.json'))
        require(e['family']==row['family'] and e['steps']==row['steps'],'Exact checkpoint stage identifiers')
        require(co==dict(lineage=lineage,payload=p,sha256=sha(BASE/p)) and sha(BASE/(p[:-5]+'_COMMIT.json'))==e['commit_sha256'] and read(BASE/p)==dict(lineage=lineage,row=row),'Exact complete committed row')
    recheck();status='BOUNDED_SEED_OVERLAP_NUMERICALLY_QUALIFIED' if all(g['passed'] for g in gates) else 'BOUNDED_SEED_OVERLAP_ARITHMETIC_FAILED'
    result=dict(status=status,lineage=lineage,direct_seeds=direct,runs=runs,numerical_gates=gates,overlaps=overlaps,time_refinements=refinements,direct_old_minus_regular=distinctions,elapsed_seconds=time.monotonic()-tick,scope='Numerical seed-overlap discriminator only; physical discrepancy and sampled domain remain independent; no late-time preparation qualification')
    rh=write(STEM+'_RESULT.json',result)
    report='# Bounded common-boundary seed overlap V001\n\nStatus '+status+'. '+str(sum(g['passed'] for g in gates))+'/306 numerical controls. 16 direct seeds, 272 propagated frames, all16 signed overlap rows and4 direct preparation distinctions retained. Physical overlap has no pass threshold and gives no late-time history qualification.\n'
    rp=BASE/(STEM+'_REPORT.md')
    with rp.open('x') as f:f.write(report)
    rp.chmod(0o444);CREATED[str(rp)]=sha(rp)
    event('OWNER_COMPLETE',status=status,gate_count=306,result_sha256=rh)
    require(len((BASE/(STEM+'_JOURNAL.jsonl')).read_text().splitlines())==6,'Closed six-event journal')
    (BASE/(STEM+'_JOURNAL.jsonl')).chmod(0o444)
    CREATED[str(BASE/(STEM+'_JOURNAL.jsonl'))]=sha(BASE/(STEM+'_JOURNAL.jsonl'));recheck()
    receipt=dict(status=status,source_sha256=SOURCE_SHA,input_sha256=dict(SEALS),manifest_sha256=MANIFEST_SHA,journal_sha256=sha(BASE/(STEM+'_JOURNAL.jsonl')),result_sha256=rh,output_sha256=dict(CREATED),gate_count=306)
    write(STEM+'_RECEIPT.json',receipt);recheck();print(json.dumps(dict(status=status,passed=sum(g['passed'] for g in gates),gates=306)),flush=True)
    return 0 if all(g['passed'] for g in gates) else 3

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--execute',action='store_true');args=parser.parse_args()
    if not args.execute:raise SystemExit('Author/static review only; root explicit --execute required')
    try:raise SystemExit(main())
    except Exception as exc:
        if not ENTERED:raise
        if any((BASE/(STEM+s)).exists() for s in ('_RESULT.json','_REPORT.md','_RECEIPT.json')):raise
        name=STEM+'_FAILED_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')+'.json'
        write(name,dict(error_type=type(exc).__name__,error=str(exc),source_sha256=sha(__file__),input_sha256=dict(SEALS),outputs=dict(CREATED),scope='Preserve bounded attempt; no overwritten parent or qualified physics'))
        raise

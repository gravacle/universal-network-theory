"""Prospective bounded actual-opacity coordinate/kernel controls; root only.
No state, trajectory, calibration, historical forcing or live result is read.
"""
from pathlib import Path
from datetime import datetime,timezone
from functools import lru_cache
import argparse,ast,hashlib,json,math,os,time
import numpy as np
BASE=Path(__file__).resolve().parent
STEM='CONSTRAINED_U_ACTUAL_OPACITY_KERNEL_CONTROLS_V001'
PROTOCOL_SHA='7441534bf4335c08dd46be7b33d59a87ab7e087d0507f137265cbae0e04292a0'
K=10.;CP=299792458.;MPC=3.0856775814913673e22
PINS={'actual_opacity_retarded_radiation_kernel_v001.py':'b43b9def6b0eeaafd12f5f947b8dd77cdf02ab60838951f799fb0bc043bc9721',
 'constrained_u_galaxy_horizon_volterra_v003.py':'06823e14186e3dec4a20b13206ceb3b5fd4824e166f09c2a856083e276b5b273',
 'CONSTRAINED_U_GALAXY_HORIZON_VOLTERRA_V003.md':'f3ec83a84bee7291b73a02ba73d48a793ab0ec7a081baa34a963ab5e5f27fc7d',
 'constrained_u_clock_gradient_early_transfer_v004.py':'a4e78b6467b0ba5884c8da2081ff580378b4afb839a90cec548fcf30a389fa07',
 'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V004_MANIFEST.json':'3a62d2b2636ebc66273ac162ee333233c98ec30949d55265a17a6d79cca43ce8'}
COMPILER_SHA='179301dcb41ea78accc3fa0048a7e6f6710d891945a751a34addd622020c1818'
SEALS={};OUTPUTS={};SOURCE_SHA=None;MANIFEST_SHA=None

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def builtin(v):
    if isinstance(v,dict):return {str(k):builtin(z) for k,z in v.items()}
    if isinstance(v,(tuple,list)):return [builtin(z) for z in v]
    if isinstance(v,np.ndarray):return builtin(v.tolist())
    if isinstance(v,np.generic):return v.item()
    return v

def write(name,obj):
    data=(json.dumps(builtin(obj),sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
    p=BASE/name
    with p.open('xb') as f:f.write(data)
    p.chmod(0o444);OUTPUTS[str(p.resolve())]=sha(p);return sha(p)

def seal(p,h):
    p=Path(p).resolve()
    if not (p.is_relative_to(BASE.parent.parent.resolve()) or (p==Path('/usr/bin/clang').resolve() and h==COMPILER_SHA)) or sha(p)!=h:raise AssertionError('Exact declared input '+str(p))
    if str(p) in SEALS and SEALS[str(p)]!=h:raise AssertionError('Conflicting seal')
    SEALS[str(p)]=h

def recheck():
    if sha(__file__)!=SOURCE_SHA:raise AssertionError('Changed source')
    for p,h in dict(SEALS,**OUTPUTS).items():
        if sha(p)!=h:raise AssertionError('Changed sealed bytes '+p)

def journal(event,**fields):
    with (BASE/(STEM+'_JOURNAL.jsonl')).open('a') as f:
        f.write(json.dumps(builtin(dict(time=datetime.now(timezone.utc).isoformat(),event=event,owner='root',pid=os.getpid(),source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,**fields)),sort_keys=True,allow_nan=False)+'\n')

def definitions(path,names,namespace):
    text=path.read_text();nodes=[n for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names]
    if {n.name for n in nodes}!=set(names):raise AssertionError('Exact definition-only helper set')
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path)+'<declared-definitions>','exec'),namespace)
    return namespace

def main():
    global SOURCE_SHA,MANIFEST_SHA
    if PROTOCOL_SHA=='PENDING':raise AssertionError('Unsealed prospective source')
    SOURCE_SHA=sha(__file__);tick=time.monotonic()
    for name,h in dict(PINS,**{STEM+'.md':PROTOCOL_SHA}).items():seal(BASE/name,h)
    parent=json.loads((BASE/'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V004_MANIFEST.json').read_text())
    for p,h in parent['inputs'].items():seal(p,h)
    fixed=parent['fixed']
    env=dict(np=np,math=math,json=json,BASE=BASE,CP=CP,MPC=MPC,lru_cache=lru_cache)
    helpers=definitions(BASE/'constrained_u_clock_gradient_early_transfer_v004.py',('background','Thermal'),env)
    angular=definitions(BASE/'constrained_u_galaxy_horizon_volterra_v003.py',('gauss','bessel','panel'),dict(np=np,math=math,lru_cache=lru_cache))
    kernel=definitions(BASE/'actual_opacity_retarded_radiation_kernel_v001.py',('gauss','background_rates','integrals','backward_integrals','inverse_depth','optical_geometry','source_weights','OpticalKernel'),dict(np=np,math=math,lru_cache=lru_cache,CP=CP,MPC=MPC,SIGMA_T=6.6524587321e-29,CAP=48.))
    therm=helpers['Thermal']('HALF',1,fixed)
    manifest=dict(source_sha256=SOURCE_SHA,inputs=dict(SEALS),fixed=fixed,k=K,starts=[3e-8,2e-8],af=1e-6,orders=[16,32],cap=48.,gate_count=1275,numpy_version=np.__version__)
    MANIFEST_SHA=write(STEM+'_MANIFEST.json',manifest);journal('OWNER_START')
    gates=[];rows=[];checkpoint_records=[]
    def check(name,error,tolerance=2e-11,**ids):
        gates.append(dict(name=name,error=float(error),tolerance=tolerance,passed=bool(math.isfinite(error) and error<=tolerance),**ids))
    def checkpoint(label):
        recheck();pn=STEM+'_'+label+'_CP.json';payload=builtin(dict(manifest=manifest,stage=label,rows=rows,gates=gates));ph=write(pn,payload);cn=pn[:-5]+'_COMMIT.json'
        commit=dict(manifest=manifest,stage=label,payload=pn,sha256=ph)
        ch=write(cn,commit);checkpoint_records.append((pn,cn,payload,commit));journal('CHECKPOINT',stage=label,payload=pn,sha256=ph,commit_sha256=ch)
    xs=np.linspace(math.log(2e-8),math.log(1e-6),17)
    for i,x in enumerate(xs):
        tx,ex,ge=kernel['background_rates'](float(x),fixed,therm,K);bg=helpers['background'](float(x),fixed);a=math.exp(float(x));g=therm.at(a)['g'];q=K*CP/(1000*fixed['Hunit']*a)
        for name,v,expected in [('tau_x',tx,g/bg['h']),('eta_x',ex,q/(K*bg['h'])),('gamma_eta',ge,g*K/q)]:check('scalar_vector_'+name,abs(float(v)/expected-1),2e-12,point=i)
    checkpoint('SCALAR')
    physical=[]
    for ai in (3e-8,2e-8):
        for n in (512,1024,2048):
            dx=math.log(1e-6/ai)/n
            for stride in (1,2):
                for position in (0.,.5,1.):
                    hi=math.log(ai)+position*math.log(1e-6/ai)
                    if position==0:hi+=stride*dx
                    lo=hi-stride*dx
                    _,width=kernel['integrals'](lo,hi,fixed,therm,K,32)
                    engine=kernel['OpticalKernel'](fixed,therm,K);geo=engine.geometry(lo,hi,0.,float(width))
                    for phase in (0.,2.,4.):engine.weights(geo,phase,angular['bessel'])
                    for name,error in engine.maximum.items():check('actual_'+name,error,ai=ai,n=n,stride=stride,position=position)
                    physical.append(dict(ai=ai,n=n,stride=stride,position=position,lo=lo,hi=hi,eta_width=float(width),depth=geo['depth'],controls=engine.maximum))
    rows.append(dict(stage='PHYSICAL',geometry=physical));checkpoint('PHYSICAL')
    radiation=dict(fixed);radiation.update(OA=0.,OB=0.)
    hr=math.sqrt(radiation['OR']/radiation['rG']);g0=CP*6.6524587321e-29*therm.nH*therm.xfull/(fixed['Hunit']*1000/MPC)
    q0=K*CP/(1000*fixed['Hunit'])
    for j,r in enumerate(physical):
        lo,hi=r['lo'],r['hi'];ae=math.exp(hi);width=q0/(K*hr)*ae*(-math.expm1(lo-hi))
        depth=g0/(hr*ae)*math.expm1(hi-lo)
        geo=kernel['optical_geometry'](lo,hi,0.,width,radiation,therm,K)
        delta,_=kernel['inverse_depth'](geo['t'],lo,hi,radiation,therm,K)
        u=hr*ae/g0*geo['t'];exact_delta=np.log1p(u);exact_back=q0/(K*hr)*ae*u/(1+u)
        check('radiation_exact_depth',abs(geo['depth']/depth-1),case=j)
        check('radiation_exact_conformal',float(np.max(abs(geo['eta_back']-exact_back)))/width,case=j)
        check('radiation_exact_inverse',float(np.max(abs(delta-exact_delta)))/max(hi-lo,1e-30),case=j)
    checkpoint('RADIATION')
    for depth in (1e-8,1.,48.,1e3,1e6):
        for phase_width in (.001,.5,4.):
            cap=min(depth,48.);pieces=max(1,math.ceil(cap/8));u,w=kernel['gauss'](16);t=np.concatenate([(i+.5)*cap/pieces+cap*u/(2*pieces) for i in range(pieces)]);dt=np.concatenate([cap*w/(2*pieces) for _ in range(pieces)])
            fraction=t/depth;collision=dt*np.exp(-t);geometry=dict(eta_back=fraction,fraction=fraction,metric_weights=collision/depth,collision_weights=collision)
            mm,cc=kernel['source_weights'](geometry,0.,phase_width,angular['bessel'])
            for l in range(5):
                for r in range(3):
                    for p in range(2):
                        oracle,_=angular['panel'](l,r,p,depth,phase_width,order=32)
                        check('constant_opacity_metric',abs(mm[l,r,p]-oracle)/max(min(1.,1/depth),1e-300),depth=depth,phase_width=phase_width,l=l,r=r,p=p)
                        check('constant_opacity_collision',abs(cc[l,r,p]-depth*oracle)/max(min(depth,1.),1e-300),depth=depth,phase_width=phase_width,l=l,r=r,p=p)
    checkpoint('CONSTANT')
    if len(gates)!=1275:raise AssertionError('Frozen1275 control census')
    qualified=all(g['passed'] for g in gates);status='ACTUAL_OPACITY_KERNEL_ARITHMETIC_PASS' if qualified else 'ACTUAL_OPACITY_KERNEL_ARITHMETIC_FAILED'
    recheck();result=dict(status=status,all_numerical_gates_passed=qualified,manifest=manifest,numerical_gates=gates,rows=rows,elapsed_seconds=time.monotonic()-tick,
        scope='Actual-source positive coordinate/kernel controls, not a trajectory or propagated-error qualification')
    rh=write(STEM+'_RESULT.json',result)
    report=BASE/(STEM+'_REPORT.md');text='# Actual-opacity kernel controls V001\n\n'+status+'\n\n'+str(sum(g['passed'] for g in gates))+'/1275 prospective controls PASS. No state or trajectory advanced.\n'
    with report.open('xb') as f:f.write(text.encode())
    report.chmod(0o444);OUTPUTS[str(report.resolve())]=sha(report)
    journal('OWNER_COMPLETE',status=status,result_sha256=rh,gates=len(gates),passed=sum(g['passed'] for g in gates))
    jp=BASE/(STEM+'_JOURNAL.jsonl');jp.chmod(0o444);OUTPUTS[str(jp.resolve())]=sha(jp)
    if len(list(BASE.glob(STEM+'_*_COMMIT.json')))!=4:raise AssertionError('Four complete stage commits')
    events=[json.loads(z) for z in jp.read_text().splitlines()]
    if [e['event'] for e in events]!=['OWNER_START']+['CHECKPOINT']*4+['OWNER_COMPLETE'] or any(e['owner']!='root' or e['pid']!=os.getpid() or e['source_sha256']!=SOURCE_SHA or e['manifest_sha256']!=MANIFEST_SHA for e in events):raise AssertionError('Exact natural root closure')
    if [e['stage'] for e in events[1:5]]!=['SCALAR','PHYSICAL','RADIATION','CONSTANT']:raise AssertionError('Frozen ordered stage closure')
    for (pn,cn,payload,commit),event in zip(checkpoint_records,events[1:5]):
        if json.loads((BASE/pn).read_text())!=payload or json.loads((BASE/cn).read_text())!=commit or event['payload']!=pn or event['sha256']!=sha(BASE/pn) or event['commit_sha256']!=sha(BASE/cn):raise AssertionError('Complete checkpoint/commit/event exact schema')
    recheck();write(STEM+'_RECEIPT.json',dict(status=status,source_sha256=SOURCE_SHA,result_sha256=rh,report_sha256=sha(report),manifest_sha256=MANIFEST_SHA,journal_sha256=sha(jp),input_sha256=dict(SEALS),output_sha256=dict(OUTPUTS),checkpoint_count=4))
    recheck();return 0 if qualified else 3

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--execute',action='store_true')
    if not ap.parse_args().execute:raise SystemExit('Root only after full frozen preflight')
    if any(BASE.glob(STEM+'_*')):raise SystemExit('Exclusive nonresumable prefix already exists; preserve/refuse')
    try:raise SystemExit(main())
    except Exception:
        write(STEM+'_FAILED_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')+'.json',dict(status='ERROR_PRESERVED',source_sha256=SOURCE_SHA,time=datetime.now(timezone.utc).isoformat()))
        raise

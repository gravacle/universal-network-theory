"""Prospective universal ball-response controls. Root alone executes.

No native spectrum, source vector, physical scale, rate or history is evaluated.
The original positive two-dimensional integral and its exact positive one-
dimensional reduction are independently contracted at every fixed order.
"""
from pathlib import Path
from fractions import Fraction
from datetime import datetime, timezone
import argparse, hashlib, json, math, os, time
import numpy as np

BASE=Path(__file__).resolve().parent
STEM='NATIVE_REGISTERED_MAXWELL_BALL_RESPONSE_CONTROLS_V001'
PROTOCOL_SHA='ef29e770ef39ce84f2acf1f114f9efa9242fca6334c7775ea16a7e9f2867e5ca'
PINS={
 'NATIVE_REGISTERED_MAXWELL_STATIONARY_EMISSION_AND_DEBIT_V001.md':'595e89b2993a81530250176a636df4639aec493b9f399997500112a14d44c536',
 'NATIVE_REGISTERED_CELL_OUTGOING_MAXWELL_PAIR_KERNEL_V001.md':'f4debb30c540386d39179fdcfc244373ac6a2bcab9f04f27fa32c0f404c88c8c',
 'NATIVE_REGISTERED_MAXWELL_DYSON_ENERGY_LEDGER_V001.md':'2ab45d4575ee2c8569a5e1a59f38dbbf3b4c60854f3ef63100e82ccd6a987306',
 'NATIVE_CANONICAL_MAXWELL_DYSON_ENERGY_CONTROL_V001_RESULT.json':'b6ef391337e96998976eab6d9b99b3e90369b88e2c2f47fcfc23e59bd62f1dd4',
 'NATIVE_CANONICAL_MAXWELL_DYSON_ENERGY_CONTROL_V001_RECEIPT.json':'94c8c845c16b2f6d4978afda790f6a70f31ee33e799d5e581aae3d174913cdce',
 'NATIVE_REGISTERED_CELL_OUTGOING_SOURCE_V001_RESULT.json':'9ad2f9890d5e909c048c0353365b75a22b86570c91d45488fb6d19b5e018de1b',
 'NATIVE_REGISTERED_CELL_OUTGOING_SOURCE_V001_RECEIPT.json':'0c5bf238307def809f53b05cf37e773385542da8816952af89d7308a74832c7e'}
ORDERS=(64,128,256)
GRID=(0.,.01,.1,.25,.5,1.,2.,4.,8.,16.,32.,64.)
TAYLOR_GRID=(0.,.01,.1,.25,.5)
REP_GRID=(.01,.025,.05,.1,.25,.5)
TOL=2e-11
SEALS={};CREATED={};SOURCE_SHA=None;MANIFEST_SHA=None;ENTERED=False

def require(ok,message):
    if not ok:raise AssertionError(message)

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def canonical(value):
    def visit(x):
        if x is None or type(x) in (str,int,bool):return
        if type(x) is float:require(math.isfinite(x),'Finite literal JSON scalar');return
        if type(x) is list:
            for y in x:visit(y)
            return
        if type(x) is dict:
            require(all(type(k) is str for k in x),'Literal string keys')
            for y in x.values():visit(y)
            return
        raise AssertionError('Native JSON values only')
    visit(value)
    return (json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()

def seal(path,digest):
    path=Path(path).resolve();require(sha(path)==digest,'Actual immutable input '+path.name)
    require(path.stat().st_mode & 0o777==0o444,'Protected immutable input')
    require(str(path) not in SEALS or SEALS[str(path)]==digest,'Unique consistent seal')
    SEALS[str(path)]=digest

def recheck():
    require(sha(__file__)==SOURCE_SHA,'Own frozen source')
    for p,h in dict(SEALS,**CREATED).items():require(sha(p)==h,'Preserved input/output '+p)

def write(name,value):
    data=canonical(value);p=BASE/name
    with p.open('xb') as f:f.write(data)
    p.chmod(0o444);CREATED[str(p.resolve())]=sha(p)
    return CREATED[str(p.resolve())]

def event(kind,epoch,**extra):
    row=dict(event=kind,time=datetime.now(timezone.utc).isoformat(),owner='root',pid=os.getpid(),epoch=epoch,source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,**extra)
    with (BASE/(STEM+'_JOURNAL.jsonl')).open('a') as f:f.write(canonical(row).decode())

def authenticate():
    require(PROTOCOL_SHA!='PENDING','Frozen prospective protocol')
    for n,h in dict(PINS,**{STEM+'.md':PROTOCOL_SHA}).items():seal(BASE/n,h)
    prior={}
    for stem,count in (('NATIVE_CANONICAL_MAXWELL_DYSON_ENERGY_CONTROL_V001',6624),('NATIVE_REGISTERED_CELL_OUTGOING_SOURCE_V001',4716)):
        result=json.loads((BASE/(stem+'_RESULT.json')).read_text());receipt=json.loads((BASE/(stem+'_RECEIPT.json')).read_text())
        require(receipt['result_sha256']==PINS[stem+'_RESULT.json'],'Completed result binding')
        flags=result['arithmetic_controls'];require(len(flags)==count and all(g['passed'] is True for g in flags),'Preserve complete old disposition')
        prior[stem]=dict(result_sha256=PINS[stem+'_RESULT.json'],receipt_sha256=PINS[stem+'_RECEIPT.json'],passed=count,total=count)
    return prior

def ball_series(u):
    u=np.asarray(u,dtype=float);term=np.ones_like(u);answer=term.copy()
    for n in range(11):term=-term*u*u/((2*n+2)*(2*n+5));answer+=term
    return answer

def ball(u):
    u=np.asarray(u,dtype=float);answer=np.empty_like(u);small=np.abs(u)<=.5
    answer[small]=ball_series(u[small]);v=u[~small]
    answer[~small]=3*(np.sin(v)-v*np.cos(v))/(v*v*v)
    return answer

def flag(name,error,scale=1.,tolerance=TOL,**labels):
    error=float(error);scale=float(scale)
    require(scale>0 and math.isfinite(error) and math.isfinite(scale),'Finite positive comparison envelope')
    return dict(name=name,error=error/scale,scale=scale,tolerance=float(tolerance),passed=bool(error/scale<=tolerance),**labels)

def arm(order):
    nodes,weights=np.polynomial.legendre.leggauss(order)
    s=(nodes+1)/2;sw=weights/2;x=s;xw=sw;c=nodes;cw=weights
    raw1=105*s*s*(1-s*s)**2/8
    raw2=105*x[:,None]**3*(1-x[:,None])**3*(1-c[None,:])**2/2
    measure1=sw*raw1;measure2=xw[:,None]*cw[None,:]*raw2
    separation2=1-2*x[:,None]*(1-x[:,None])*(1-c[None,:])
    require(np.all(separation2>=0),'Literal nonnegative separation support')
    separation=np.sqrt(separation2);checks=[];rows=[];moments=[]
    checks.append(flag('positive_nodes_weights',0. if np.all(weights>0) and np.all(np.diff(nodes)>0) and np.all(abs(nodes)<1) else 1.,order=order))
    for method,measure in (('ONE_D',measure1),('TWO_D',measure2)):
        checks.append(flag('measure_normalization',abs(float(np.sum(measure))-1.),order=order,method=method))
    for n in range(9):
        exact=Fraction(105,(2*n+3)*(2*n+5)*(2*n+7));m1=float(np.sum(measure1*s**(2*n)));m2=float(np.sum(measure2*separation2**n))
        moments.append(dict(n=n,exact=[str(exact.numerator),str(exact.denominator)],ONE_D=m1,TWO_D=m2))
        for method,value in (('ONE_D',m1),('TWO_D',m2)):checks.append(flag('moment',abs(value-float(exact)),float(exact),order=order,method=method,n=n))
    for z in GRID:
        j1=float(np.sum(measure1*ball(z*s)**2));j2=float(np.sum(measure2*ball(z*separation)**2));rows.append(dict(z=z,ONE_D=j1,TWO_D=j2))
        for method,value in (('ONE_D',j1),('TWO_D',j2)):
            checks.append(flag('positive_unit_bound',max(0.,-value,value-1.) if value>0 else 1.,order=order,method=method,z=z))
        checks.append(flag('independent_dimension_comparison',abs(j1-j2),max(abs(j1)+abs(j2),1e-300),order=order,z=z))
        if z==0.:
            for method,value in (('ONE_D',j1),('TWO_D',j2)):checks.append(flag('exact_zero_shape',abs(value-1.),order=order,method=method))
        if z in TAYLOR_GRID:
            polynomial=1-z*z/15+z**4/385;bound=4*z**6/57915;allowance=TOL*(1+abs(polynomial))
            for method,value in (('ONE_D',j1),('TWO_D',j2)):
                checks.append(flag('rigorous_quartic_remainder',max(0.,abs(value-polynomial)-bound),allowance,tolerance=1.,order=order,method=method,z=z,analytic_bound=bound,roundoff_allowance=allowance))
    require(len(checks)==69,'Exact69 controls per quadrature arm')
    return dict(order=order,nodes=nodes.tolist(),weights=weights.tolist(),rows=rows,moments=moments,numerical_gates=checks)

def summary(arms):
    checks=[]
    for u in REP_GRID:
        direct=3*(math.sin(u)-u*math.cos(u))/u**3;series=float(ball_series(np.array(u)))
        checks.append(flag('series_literal_formfactor',abs(series-direct),abs(series)+abs(direct),u=u))
    checks.append(flag('formfactor_at_zero',abs(float(ball(np.array(0.)))-1.)))
    coefficients=(Fraction(-1,5)*Fraction(1,3),Fraction(3,175)*Fraction(5,33),Fraction(-4,4725)*Fraction(35,429))
    for n,(actual,expected) in enumerate(zip(coefficients,(Fraction(-1,15),Fraction(1,385),Fraction(-4,57915))),1):checks.append(flag('exact_taylor_fraction',0. if actual==expected else 1.,power=2*n))
    for a,b in zip(arms[:-1],arms[1:]):
        for old,new in zip(a['rows'],b['rows']):
            require(old['z']==new['z'],'Same whole grid')
            for method in ('ONE_D','TWO_D'):checks.append(flag('quadrature_refinement',abs(old[method]-new[method]),max(abs(old[method])+abs(new[method]),1e-300),coarse=a['order'],fine=b['order'],method=method,z=old['z']))
    require(len(checks)==58,'Exact58 summary controls')
    return dict(numerical_gates=checks,physical_rate_or_scale_selected=False)

def recover(lineage):
    jp=BASE/(STEM+'_JOURNAL.jsonl');require(jp.exists() and jp.stat().st_size,'Existing nonempty root owner prefix')
    events=[json.loads(s) for s in jp.read_text().splitlines()];labels=['AUTH','ORDER64','ORDER128','ORDER256','SUMMARY'];prefix=[];payloads={};files=set();epoch=-1;pid=None
    for i,e in enumerate(events):
        require(type(e['pid']) is int and e['pid']>0 and type(e['epoch']) is int,'Literal owner identity')
        require(e['owner']=='root' and e['source_sha256']==SOURCE_SHA and e['manifest_sha256']==MANIFEST_SHA,'Same root/source lineage')
        if e['event'] in ('OWNER_START','OWNER_RESUME'):
            require((e['event']=='OWNER_START')==(i==0) and e['epoch']==epoch+1,'Exact owner epoch');epoch=e['epoch'];pid=e['pid'];continue
        require(e['event']=='CHECKPOINT' and e['epoch']==epoch and e['pid']==pid,'Current owner checkpoint')
        label=e['label'];require(len(prefix)<len(labels) and label==labels[len(prefix)],'Contiguous exact checkpoint census')
        pn=BASE/(STEM+'_CP_'+label+'.json');cn=BASE/(STEM+'_CP_'+label+'_COMMIT.json');require(sha(pn)==e['payload_sha256'] and sha(cn)==e['commit_sha256'],'Exact committed own payload bytes');p=json.loads(pn.read_text());c=json.loads(cn.read_text())
        require(pn.read_bytes()==canonical(p) and cn.read_bytes()==canonical(c),'Canonical complete checkpoint')
        require(p['lineage']==c['lineage']==lineage and p['label']==c['label']==label and c['payload']==pn.name and c['sha256']==e['payload_sha256'] and p['pid']==c['pid']==pid and p['epoch']==c['epoch']==epoch and p['owner']==c['owner']=='root','Authenticated entire checkpoint identity')
        value=p['value']
        if label=='AUTH':require(value==lineage['prior_dispositions'],'Exact reused parent disposition')
        if label.startswith('ORDER'):
            require(value['order']==int(label[5:]) and len(value['nodes'])==len(value['weights'])==value['order'] and [r['z'] for r in value['rows']]==list(GRID) and len(value['moments'])==9 and len(value['numerical_gates'])==69,'Exact reused arm schema/census')
            require(set(value)=={'order','nodes','weights','rows','moments','numerical_gates'} and all(type(x) is float for x in value['nodes']+value['weights']) and all(value['nodes'][j]<value['nodes'][j+1] for j in range(value['order']-1)) and all(abs(x)<1 for x in value['nodes']) and all(x>0 for x in value['weights']),'Full positive ordered arm arrays')
            require(all(set(r)=={'z','ONE_D','TWO_D'} and type(r['ONE_D']) is type(r['TWO_D']) is float for r in value['rows']) and [m['n'] for m in value['moments']]==list(range(9)),'Full literal grid/moment records')
            for m in value['moments']:
                exact=Fraction(105,(2*m['n']+3)*(2*m['n']+5)*(2*m['n']+7));require(set(m)=={'n','exact','ONE_D','TWO_D'} and m['exact']==[str(exact.numerator),str(exact.denominator)],'Exact saved moment witness')
        if label=='SUMMARY':require(len(value['numerical_gates'])==58,'Exact reused summary census')
        if label!='AUTH':require(all(type(g['passed']) is bool and type(g['error']) is type(g['scale']) is type(g['tolerance']) is float and g['scale']>0 and g['passed']==(g['error']<=g['tolerance']) for g in value['numerical_gates']),'Entire reused criterion schema/status')
        payloads[label]=value;prefix.append(label);files.update((pn.name,cn.name));CREATED[str(pn.resolve())]=sha(pn);CREATED[str(cn.resolve())]=sha(cn)
    require({p.name for p in BASE.glob(STEM+'_CP_*.json')}==files,'No orphan checkpoint/payload')
    return prefix,payloads,epoch,events

def main():
    global SOURCE_SHA,MANIFEST_SHA,ENTERED
    parser=argparse.ArgumentParser();parser.add_argument('--resume',action='store_true');args=parser.parse_args();SOURCE_SHA=sha(__file__)
    closed=['_RESULT.json','_REPORT.md','_RECEIPT.json'];require(not any((BASE/(STEM+s)).exists() for s in closed) and not list(BASE.glob(STEM+'_FAILED*')),'Closed attempt immutable')
    start=time.monotonic();prior=authenticate();lineage=dict(source_sha256=SOURCE_SHA,inputs=SEALS.copy(),orders=list(ORDERS),grid=list(GRID),tolerance=TOL,prior_dispositions=prior,scope='UNIVERSAL_DIMENSIONLESS_RESPONSE_ONLY')
    mp=BASE/(STEM+'_MANIFEST.json');jp=BASE/(STEM+'_JOURNAL.jsonl')
    if mp.exists():
        require(args.resume and mp.read_bytes()==canonical(lineage),'Exact requested resume manifest');MANIFEST_SHA=sha(mp);CREATED[str(mp.resolve())]=MANIFEST_SHA;prefix,values,epoch,_=recover(lineage);epoch+=1;event('OWNER_RESUME',epoch);ENTERED=True
    else:
        require(not args.resume and not jp.exists() and not list(BASE.glob(STEM+'_CP_*.json')),'Refuse orphan runtime before manifest');MANIFEST_SHA=write(mp.name,lineage);prefix=[];values={};epoch=0;event('OWNER_START',epoch);ENTERED=True
    def checkpoint(label,value):
        recheck();pn=STEM+'_CP_'+label+'.json';cn=STEM+'_CP_'+label+'_COMMIT.json';identity=dict(lineage=lineage,label=label,owner='root',pid=os.getpid(),epoch=epoch)
        ph=write(pn,dict(identity,value=value));ch=write(cn,dict(identity,payload=pn,sha256=ph));event('CHECKPOINT',epoch,label=label,payload_sha256=ph,commit_sha256=ch);values[label]=value
    if 'AUTH' not in values:checkpoint('AUTH',prior)
    for order in ORDERS:
        label='ORDER'+str(order)
        if label not in values:checkpoint(label,arm(order))
    arms=[values['ORDER'+str(n)] for n in ORDERS]
    if 'SUMMARY' not in values:checkpoint('SUMMARY',summary(arms))
    actual,authenticated,_,_=recover(lineage);require(actual==['AUTH','ORDER64','ORDER128','ORDER256','SUMMARY'] and authenticated==values,'Final complete owned checkpoint closure')
    checks=[g for a in arms for g in a['numerical_gates']]+values['SUMMARY']['numerical_gates'];require(len(checks)==265,'Exact full265 criteria')
    result=dict(lineage=lineage,arms=arms,summary=values['SUMMARY'],numerical_gates=checks,passed=sum(g['passed'] for g in checks),total=265,status='RESPONSE_CONTROLS_PASS' if all(g['passed'] for g in checks) else 'RESPONSE_CONTROLS_NOT_QUALIFIED',elapsed_seconds=time.monotonic()-start)
    rh=write(STEM+'_RESULT.json',result);report='# Universal registered-ball response controls V001\n\n'+str(result['passed'])+'/265 fixed numerical controls pass. All positive1D/2D orders and signed comparisons are retained. No physical rate, spectrum, scale, preparation or history is selected.\n';p=BASE/(STEM+'_REPORT.md')
    with p.open('xb') as f:f.write(report.encode())
    p.chmod(0o444);CREATED[str(p.resolve())]=sha(p);event('OWNER_COMPLETE',epoch,result_sha256=rh,status=result['status'],control_count=265,checkpoint_count=5)
    terminal=json.loads(jp.read_text().splitlines()[-1]);require(terminal['event']=='OWNER_COMPLETE' and terminal['owner']=='root' and terminal['pid']==os.getpid() and terminal['epoch']==epoch and terminal['source_sha256']==SOURCE_SHA and terminal['manifest_sha256']==MANIFEST_SHA and terminal['result_sha256']==rh and terminal['status']==result['status'] and terminal['control_count']==265 and terminal['checkpoint_count']==5,'Exact natural terminal owner/census')
    jp.chmod(0o444);CREATED[str(jp.resolve())]=sha(jp);recheck()
    receipt=dict(source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,result_sha256=rh,journal_sha256=sha(jp),input_sha256=SEALS,output_sha256=CREATED.copy(),status=result['status']);write(STEM+'_RECEIPT.json',receipt);recheck();print(result['status'],result['passed'],'/',result['total'],flush=True)
    return 0 if result['passed']==265 else 3

if __name__=='__main__':
    try:raise SystemExit(main())
    except Exception as exc:
        if ENTERED and not (BASE/(STEM+'_RESULT.json')).exists():
            p=BASE/(STEM+'_FAILED_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')+'.json');data=canonical(dict(owner='root',pid=os.getpid(),source_sha256=SOURCE_SHA,error=repr(exc)))
            with p.open('xb') as f:f.write(data)
            p.chmod(0o444)
        raise

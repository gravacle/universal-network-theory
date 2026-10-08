"""Same-action predicted-ruler DESI readout, root-only; no fit/legacy imports."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import ast
import hashlib
import json
import math
import os
import time
import numpy as np
BASE=Path(__file__).resolve().parent
STEM='CONSTRAINED_U_CLOCK_GRADIENT_BBN_DESI_BAO_V001'
PROTOCOL_SHA='b6f2443c0119da770907e41891903909cbdebad025b72ad35c6ee2c942ef624a'
PINS={'constrained_u_clock_gradient_bbn_acoustic_readout_v001.py': '0440a959e2a662203b57f3da39afee973f41cc90fbe289520415f50f3da94f3b', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_ACOUSTIC_READOUT_V001.md': '74e0c0ce3be19e1cb115d47f21eefeaf122f3530b1d4bd6a3eae194c0960051f', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_ACOUSTIC_READOUT_V001_RESULT.json': '844d085f18ab85589793858d24fb4a3333741175c6a7d5b41792d83b331ee403', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_ACOUSTIC_READOUT_V001_RECEIPT.json': 'e0dab9c7d3e335001908ed10f43972b4f6b97658061490087720a3ffcb2d16d7', 'desi_dr2_bao_external_v001/desi_gaussian_bao_ALL_GCcomb_mean.txt': '9ac154ab583ce759c0f7eef3c978c7c70a6ead2d18774caceadf1a350a640585', 'desi_dr2_bao_external_v001/desi_gaussian_bao_ALL_GCcomb_cov.txt': '252a143274c8a07c78694c119617d36594f6d7965d00319ca611c6ffb886e509', 'desi_dr2_bao_external_v001/README.md': '5f21b88b1a6d6264174f7ecd2b1e0baf78a62c9feb467c5fe3865eb3ba9b70f6', 'invariant_clock_acoustic_bao_v001.py': '42f60b72673d5cb52c467ec0990c4fed0c85c2882a189d3b309d22491af00fcb'}
PARENT='CONSTRAINED_U_CLOCK_GRADIENT_BBN_ACOUSTIC_READOUT_V001'
BACKGROUND_SPAN_SHA='eb224e42c6c567b0339b18cdf54a1d8c4f005810b6d6952fee9efee4983b7ec2'
COMPILER_SHA='179301dcb41ea78accc3fa0048a7e6f6710d891945a751a34addd622020c1818'
MPC=3.0856775814913673e22
CP=299792458.
ORDER=[(.295,'DV_over_rs'),(.510,'DM_over_rs'),(.510,'DH_over_rs'),(.706,'DM_over_rs'),(.706,'DH_over_rs'),(.934,'DM_over_rs'),(.934,'DH_over_rs'),(1.321,'DM_over_rs'),(1.321,'DH_over_rs'),(1.484,'DM_over_rs'),(1.484,'DH_over_rs'),(2.33,'DH_over_rs'),(2.33,'DM_over_rs')]
SEALS={}
CREATED={}
RUN_SOURCE=''
RUN_MANIFEST=''

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def now():return datetime.now(timezone.utc).isoformat()

def write(name,obj,raw=False):
    p=BASE/name;data=obj if raw else (json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
    with p.open('xb') as f:f.write(data)
    p.chmod(0o444);h=sha(p);CREATED[str(p.resolve())]=h;return h

def seal(p,h):
    p=Path(p).resolve()
    if not (p.is_relative_to(BASE.parent.parent.resolve()) or (p==Path('/usr/bin/clang').resolve() and h==COMPILER_SHA)) or sha(p)!=h:
        raise AssertionError('Input path/seal '+str(p))
    if str(p) in SEALS and SEALS[str(p)]!=h:raise AssertionError('Conflicting seal')
    SEALS[str(p)]=h

def recheck():
    for p,h in dict(SEALS,**CREATED).items():
        if sha(p)!=h:raise AssertionError('Changed sealed input/prefix '+p)
    if sha(__file__)!=RUN_SOURCE:raise AssertionError('Changed source')

def journal(event,**data):
    with (BASE/(STEM+'_JOURNAL.jsonl')).open('a') as f:
        f.write(json.dumps(dict(event=event,owner='root',pid=os.getpid(),time=now(),source_sha256=RUN_SOURCE,manifest_sha256=RUN_MANIFEST,**data),sort_keys=True)+'\n')

def background(x, fixed):
    a = math.exp(x)
    eps, d0, OA, OB, OR, rG = (fixed[k] for k in ('eps', 'd0', 'OA', 'OB', 'OR', 'rG'))
    norm = 1/eps-math.log1p(1/eps)
    d = d0/a**3
    target = .5*eps*norm*d
    s = target
    for _ in range(5):
        qbar = math.sqrt(1+eps*s/(1+s))
        dq = eps/(2*qbar*(1+s)**2)
        s -= (s*qbar-target)/(qbar+s*dq)
    qbar = math.sqrt(1+eps*s/(1+s))
    dq = eps/(2*qbar*(1+s)**2)
    pex = (math.log1p(s)-s/(1+s))/norm
    cs = eps*s/(2+(4+3*eps)*s+2*(1+eps)*s*s)
    b, r = 1.5*OB/rG/a**3, 1.5*OR/rG/a**4
    w = 1.5*OA/rG*qbar*d
    rho = 1.5*OA/rG*(1+qbar*d-pex)
    h = math.sqrt((2/3)*(b+r+rho))
    den=2+(4+3*eps)*s+2*(1+eps)*s*s
    ds_dt=-3*h*s/(1+s*dq/qbar)
    cs_dt=eps*(2-2*(1+eps)*s*s)*ds_dt/(den*den)
    Q=fixed['Q0_over_Hstar']*qbar
    return dict(a=a, h=h, b=b, r=r, w=w, rho=rho, cs=cs, qbar=qbar,
                h_dt=-b-4*r/3-w, cs_dt=cs_dt, Q=Q,
                s=s, charge=d, charge_error=abs(2*qbar*s/(eps*norm)/d-1))

def quad(func,lo,hi,n):
    t,w=np.polynomial.legendre.leggauss(n);x=(lo+hi)/2+(hi-lo)*t/2
    return float((hi-lo)*np.dot(w,func(x))/2)

class Background:
    def __init__(self,fixed,ledger):
        self.fixed=fixed;self.Rb0=ledger['Rb0'];self.hs=fixed['Hunit']*1000/MPC;self.unit=CP/(self.hs*MPC)
    def E(self,a):
        return np.array([background(math.log(float(t)),self.fixed)['h'] for t in np.asarray(a).reshape(-1)]).reshape(np.asarray(a).shape)
    def H(self,z):return self.hs*self.E(1/(1+np.asarray(z)))


def authenticate():
    for n,h in dict(PINS,**{STEM+'.md':PROTOCOL_SHA}).items():seal(BASE/n,h)
    raw=json.loads((BASE/(PARENT+'_RESULT.json')).read_text());receipt=json.loads((BASE/(PARENT+'_RECEIPT.json')).read_text())
    if (raw['status']!='NEW_BBN_ACOUSTIC_ARITHMETIC_PASS' or receipt['status']!=raw['status'] or not raw['all_numerical_gates_passed']
        or len(raw['numerical_gates'])!=22 or not all(g['passed'] for g in raw['numerical_gates'])
        or receipt['source_sha256']!=PINS['constrained_u_clock_gradient_bbn_acoustic_readout_v001.py']
        or receipt['result_sha256']!=PINS[PARENT+'_RESULT.json'] or raw['manifest']!=receipt['manifest']):raise AssertionError('Acoustic source/parent qualification')
    for p,h in dict(receipt['manifest']['input_sha256'],**receipt['output_sha256']).items():seal(p,h)
    seal(BASE/(PARENT+'_MANIFEST.json'),receipt['manifest_sha256']);seal(BASE/(PARENT+'_JOURNAL.jsonl'),receipt['journal_sha256'])
    events=[json.loads(t) for t in (BASE/(PARENT+'_JOURNAL.jsonl')).read_text().splitlines()]
    if ([e['event'] for e in events]!=['OWNER_START']+['CHECKPOINT']*4+['OWNER_COMPLETE']
        or [e['arm'] for e in events[1:-1]]!=['DEFAULT','HALF','THIN','QUADRATURE']
        or events[-1]['status']!=raw['status'] or events[-1]['result_sha256']!=receipt['result_sha256']
        or events[-1]['gate_count']!=22 or events[-1]['passed']!=22):raise AssertionError('Acoustic natural closure')
    owner=events[0]['pid']
    for e in events:
        if (e['owner']!='root' or type(e['pid']) is not int or e['pid']!=owner or e['source_sha256']!=receipt['source_sha256']
            or e['manifest_sha256']!=receipt['manifest_sha256']):raise AssertionError('Acoustic root/source/manifest/PID')
    for e,row in zip(events[1:-1],raw['rows']):
        pn=PARENT+'_'+row['label']+'_CP.json';cn=PARENT+'_'+row['label']+'_CP_COMMIT.json';co=json.loads((BASE/cn).read_text())
        if (e['payload']!=pn or e['sha256']!=sha(BASE/pn) or e['commit_sha256']!=sha(BASE/cn)
            or co!=dict(manifest=raw['manifest'],arm=row['label'],payload=pn,sha256=e['sha256']) or json.loads((BASE/pn).read_text())!=row):raise AssertionError('Acoustic full committed arm')
    old=(BASE/'constrained_u_clock_gradient_bbn_acoustic_readout_v001.py').read_text();own=Path(__file__).read_text()
    for name in ('background','quad','Background'):
        n0=next(n for n in ast.parse(old).body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==name)
        n1=next(n for n in ast.parse(own).body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==name)
        if ast.get_source_segment(old,n0)!=ast.get_source_segment(own,n1):raise AssertionError('Copied pure geometry '+name)
        if name=='background' and hashlib.sha256(ast.get_source_segment(own,n1).encode()).hexdigest()!=BACKGROUND_SPAN_SHA:raise AssertionError('Background span')
    return raw


def distance_vector(bg,n,simpson=False):
    values=[]
    for z,kind in ORDER:
        dh=bg.unit/float(bg.E(1/(1+z)))
        if simpson:
            zz=np.linspace(0,z,2049);v=1/bg.E(1/(1+zz));dm=bg.unit*z/2048/3*(v[0]+v[-1]+4*sum(v[1:-1:2])+2*sum(v[2:-1:2]))
        else:dm=bg.unit*quad(lambda zz:1/bg.E(1/(1+zz)),0.,z,n)
        dv=(z*dm*dm*dh)**(1/3);values.append({'DM_over_rs':dm,'DH_over_rs':dh,'DV_over_rs':dv}[kind])
    return np.array(values)


def main():
    global RUN_SOURCE,RUN_MANIFEST
    tick=time.monotonic();RUN_SOURCE=sha(__file__)
    if list(BASE.glob(STEM+'_*')):raise FileExistsError('Existing runtime prefix preserved')
    parent=authenticate();lines=[s.split() for s in (BASE/'desi_dr2_bao_external_v001/desi_gaussian_bao_ALL_GCcomb_mean.txt').read_text().splitlines() if s.strip() and not s.startswith('#')]
    if [(float(r[0]),r[2]) for r in lines]!=ORDER:raise AssertionError('Exact13 data order')
    obs=np.array([float(r[1]) for r in lines]);cov=np.loadtxt(BASE/'desi_dr2_bao_external_v001/desi_gaussian_bao_ALL_GCcomb_cov.txt')
    if obs.shape!=(13,) or cov.shape!=(13,13) or not np.all(np.isfinite(cov)) or not np.all(obs>0):raise AssertionError('Data/covariance shapes/finite')
    manifest=dict(source_sha256=RUN_SOURCE,input_sha256=dict(SEALS),physical=parent['manifest']['fixed'],ordinary=parent['manifest']['ordinary'],order=ORDER,numerical_controls=5,numpy_version=np.__version__)
    RUN_MANIFEST=write(STEM+'_MANIFEST.json',manifest);journal('OWNER_START');recheck()
    bg=Background(parent['manifest']['fixed'],parent['manifest']['photon_baryon_ledger']);f=distance_vector(bg,96);co=distance_vector(bg,48);si=distance_vector(bg,96,True)
    chol=np.linalg.cholesky(cov);ci=np.linalg.solve(cov,np.eye(13));A=float(f@ci@f);B=float(f@ci@obs);C0=float(obs@ci@obs)
    lo,hi=parent['rows'][1]['observables']['drag_ruler_Mpc_interval']
    if not (parent['rows'][1]['label']=='HALF' and math.isfinite(lo) and 0<lo<hi and np.all(f>0)):raise AssertionError('Primary finite physical ruler')
    lowy,highy=1/hi,1/lo;vertex=min(highy,max(lowy,B/A));candidates=(lowy,highy,vertex,2/(lo+hi));witnesses=[];score_errors=[]
    for y in candidates:
        prediction=f*y;res=prediction-obs;white=np.linalg.solve(chol,res);score=float(white@white);polynomial=A*y*y-2*B*y+C0
        score_errors.append(abs(score-polynomial));witnesses.append(dict(ruler_Mpc=1/y,score=score,prediction=prediction.tolist(),residual=res.tolist(),whitened_residual=white.tolist(),quadratic_score=polynomial))
    gates=[]
    def check(name,error,tol):gates.append(dict(name=name,error=float(error),tolerance=tol,passed=bool(math.isfinite(error) and error<=tol)))
    check('covariance_symmetry',np.max(abs(cov-cov.T)),2e-12);check('covariance_inverse',np.max(abs(cov@ci-np.eye(13))),2e-12)
    check('gauss48_96_distance',np.max(abs(co/f-1)),2e-12);check('independent_simpson_distance',np.max(abs(si/f-1)),2e-11);check('direct_vs_quadratic_score',max(score_errors),2e-8)
    ok=all(g['passed'] for g in gates);status='NEW_BBN_PREDICTED_RULER_BAO_ARITHMETIC_PASS' if ok else 'NEW_BBN_PREDICTED_RULER_BAO_ARITHMETIC_FAILED'
    result=dict(status=status,all_numerical_gates_passed=ok,manifest=manifest,data=obs.tolist(),covariance=cov.tolist(),distance_vector_Mpc=f.tolist(),gauss48_distance_vector_Mpc=co.tolist(),simpson_distance_vector_Mpc=si.tolist(),ruler_Mpc_interval=[lo,hi],score_interval=[witnesses[2]['score'],max(w['score'] for w in witnesses[:2])],score_witnesses=witnesses,numerical_gates=gates,elapsed_seconds=time.monotonic()-tick,scope='Exposed13-point DESI development prediction, no fit/p-value/fullstandard-model comparison/superiority')
    recheck();pn=STEM+'_VECTOR_CP.json';cn=STEM+'_VECTOR_CP_COMMIT.json';h=write(pn,result);ch=write(cn,dict(manifest=manifest,payload=pn,sha256=h));journal('CHECKPOINT',payload=pn,sha256=h,commit_sha256=ch)
    rh=write(STEM+'_RESULT.json',result);report='# Same-action BBN-linked predicted-ruler DESI BAO V001\n\n'+status+'\n\n'+str(sum(g['passed'] for g in gates))+'/5 numerical controls PASS.\nPredicted ruler interval '+repr([lo,hi])+' Mpc; correlated13-point score interval '+repr(result['score_interval'])+'.\n\nNo new fit. Existing data/calibration exposure and adopted action/state freedom remain counted; this is not a superiority result or a full joint likelihood.\n'
    reph=write(STEM+'_REPORT.md',report.encode(),True);recheck()
    ev=[json.loads(s) for s in (BASE/(STEM+'_JOURNAL.jsonl')).read_text().splitlines()];commit=json.loads((BASE/cn).read_text())
    if (len(ev)!=2 or [e['event'] for e in ev]!=['OWNER_START','CHECKPOINT'] or any(e['owner']!='root' or e['pid']!=os.getpid() or e['source_sha256']!=RUN_SOURCE or e['manifest_sha256']!=RUN_MANIFEST for e in ev)
        or ev[1]['payload']!=pn or ev[1]['sha256']!=h or ev[1]['commit_sha256']!=ch or commit!=dict(manifest=manifest,payload=pn,sha256=h) or json.loads((BASE/pn).read_text())!=result):raise AssertionError('Exact complete vector custody')
    journal('OWNER_COMPLETE',status=status,result_sha256=rh,gate_count=5,passed=sum(g['passed'] for g in gates));write(STEM+'_RECEIPT.json',dict(status=status,source_sha256=RUN_SOURCE,manifest=manifest,manifest_sha256=RUN_MANIFEST,result_sha256=rh,report_sha256=reph,journal_sha256=sha(BASE/(STEM+'_JOURNAL.jsonl')),output_sha256=dict(CREATED)))
    recheck();print(json.dumps(dict(status=status,score_interval=result['score_interval'],elapsed_seconds=result['elapsed_seconds'],result_sha256=rh)),flush=True);return 0 if ok else 3


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--execute',action='store_true')
    if not ap.parse_args().execute:raise SystemExit('Root alone launches --execute')
    if list(BASE.glob(STEM+'_*')):raise SystemExit('Existing runtime prefix; no retry/failure mutation')
    try:raise SystemExit(main())
    except Exception as exc:
        stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f');write(STEM+'_FAILED_'+stamp+'.json',dict(status='EXECUTION_ERROR_PRESERVED',error=repr(exc),pid=os.getpid(),time=now(),source_sha256=sha(__file__)));raise

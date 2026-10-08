"""NEW same-action BBN-helium acoustic/drag saved arithmetic; root --execute only.
No legacy modules, binary calls, calibration or perturbation evolution.
"""
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
STEM='CONSTRAINED_U_CLOCK_GRADIENT_BBN_ACOUSTIC_READOUT_V001'
PROTOCOL_SHA='74e0c0ce3be19e1cb115d47f21eefeaf122f3530b1d4bd6a3eae194c0960051f'
PINS={'constrained_u_clock_gradient_flrw_reduced_chart_v002.py': '6d9878bb854bc7147aefcdcd358c6cecd16087a9577960f10686f5c4d17094b9', 'CONSTRAINED_U_CLOCK_GRADIENT_FLRW_REDUCED_CHART_V002.md': '5d644d9d07d6d2dbf4f44a20e329e30965ef0c558a052359bda102dc0b5aba1b', 'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md': 'e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0', 'INVARIANT_CLOCK_JOINT_CALIBRATION_V003_RESULT.json': 'c92eb0ce131a61009361f2ead3f4db7522d3eabb22f7e3d472f0e4e0c116c24f', 'invariant_clock_acoustic_v001.py': '9cd21314b29d11cedba04eb6e53799aa7847d40c1280718913d2a392bb3db396', 'constrained_u_clock_gradient_bbn_helium_recombination_pair_v002.py': '713d7ce75c43cea179f6c126424a1fe58b60739186b12089d083ded786c15601', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V002.md': '7075a9557ec141c99843c744a135c070dc1a4c90b0be4e27a52cd5b62c7a5d6d', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V002_RESULT.json': '8edf04b504f89b0e378823c2b5eda6547138361bb5ad13f6858bd0e34ce5be20', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V002_RECEIPT.json': '867911256634977adc8a50cdcc9b3b2e2e7aabaed6435de25c8be80acb6253fd', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V002_DEFAULT_OUTPUT.json': '07e8e4e7fe524fd9d1f1a19422f293f11a49573f6ee6d1bf016b17c80ec70437', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V002_HALF_OUTPUT.json': '1df474629eb706d1315f090de228059c59db3ad58c127be2b614c005dc471386', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_PAIR_V001_RESULT.json': '64e55eefc0079b75994dc749f5e8853835cd3bc72a2566e9627f8b98851fdc36', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_PAIR_V001_RECEIPT.json': 'e7a9cc7d8f3b59e3b9351a7a3253d5ad4e806a49340908b067600d71783d6685', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_PAIR_V001_REFINED_STDOUT.txt': 'd0ec0ef40b5202420b1f064bb42b5101eb6008936cfafe8ab69b2862ca44d225'}
BACKGROUND_SPAN_SHA='eb224e42c6c567b0339b18cdf54a1d8c4f005810b6d6952fee9efee4983b7ec2'
COMPILER_SHA='179301dcb41ea78accc3fa0048a7e6f6710d891945a751a34addd622020c1818'
ATOMIC='CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V002'
MPC=3.0856775814913673e22
CP=299792458.
SIGMA_T=6.6524587321e-29
FIELDS=('zstar','rs_Mpc','DM_Mpc','theta100','drag_redshift_interval','drag_ruler_Mpc_interval')
ARMS=(('DEFAULT','DEFAULT',1,512),('HALF','HALF',1,512),('THIN','HALF',2,512),('QUADRATURE','HALF',1,256))
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


def authenticate():
    for n,h in dict(PINS,**{STEM+'.md':PROTOCOL_SHA}).items():seal(BASE/n,h)
    old=(BASE/'constrained_u_clock_gradient_flrw_reduced_chart_v002.py').read_text();own=Path(__file__).read_text()
    a=next(n for n in ast.parse(old).body if isinstance(n,ast.FunctionDef) and n.name=='background')
    b=next(n for n in ast.parse(own).body if isinstance(n,ast.FunctionDef) and n.name=='background')
    span=ast.get_source_segment(old,a)
    if ast.get_source_segment(own,b)!=span or hashlib.sha256(span.encode()).hexdigest()!=BACKGROUND_SPAN_SHA:raise AssertionError('Literal background identity')
    cal=json.loads((BASE/'INVARIANT_CLOCK_JOINT_CALIBRATION_V003_RESULT.json').read_text())
    for p,h in cal['hashes'].items():seal(p,h)
    result=json.loads((BASE/(ATOMIC+'_RESULT.json')).read_text());receipt=json.loads((BASE/(ATOMIC+'_RECEIPT.json')).read_text())
    if (result['status']!=receipt['status'] or result['status']!='NEW_ATOMIC_PAIR_ARITHMETIC_PASS'
        or len(result['numerical_gates'])!=12 or not all(g['passed'] for g in result['numerical_gates'])
        or not result['all_numerical_gates_passed'] or result['lineage']!=receipt['lineage']
        or receipt['result_sha256']!=PINS[ATOMIC+'_RESULT.json']
        or receipt['lineage']['source_sha256']!=PINS['constrained_u_clock_gradient_bbn_helium_recombination_pair_v002.py']):raise AssertionError('Accepted BBN atomic identity')
    for p,h in dict(receipt['lineage']['input_sha256'],**receipt['output_sha256']).items():seal(p,h)
    seal(BASE/(ATOMIC+'_MANIFEST.json'),receipt['manifest_sha256']);seal(BASE/(ATOMIC+'_JOURNAL.jsonl'),receipt['journal_sha256'])
    ev=[json.loads(x) for x in (BASE/(ATOMIC+'_JOURNAL.jsonl')).read_text().splitlines()]
    if ([e['event'] for e in ev]!=['OWNER_START','CHECKPOINT','CHECKPOINT','OWNER_COMPLETE']
        or ev[0]['owner']!='root' or type(ev[0]['pid']) is not int or ev[0]['pid']<=0
        or ev[0]['source_sha256']!=receipt['lineage']['source_sha256']
        or [e['arm'] for e in ev[1:3]]!=['DEFAULT','HALF']
        or ev[-1]['result_sha256']!=PINS[ATOMIC+'_RESULT.json'] or ev[-1]['status']!=result['status'] or ev[-1]['gate_count']!=12):raise AssertionError('Atomic natural closure')
    for arm,event,inv in zip(('DEFAULT','HALF'),ev[1:3],result['invocations']):
        pn=ATOMIC+'_'+arm+'_CP.json';cn=ATOMIC+'_'+arm+'_CP_COMMIT.json';co=json.loads((BASE/cn).read_text())
        if (co!=dict(arm=arm,lineage=result['lineage'],checkpoint=pn,sha256=sha(BASE/pn))
            or event['commit_sha256']!=sha(BASE/cn) or event['source_sha256']!=receipt['lineage']['source_sha256']
            or json.loads((BASE/pn).read_text())!=inv):raise AssertionError('Atomic committed arm identity')
    bb='CONSTRAINED_U_CLOCK_GRADIENT_BBN_PAIR_V001';br=json.loads((BASE/(bb+'_RESULT.json')).read_text());bp=json.loads((BASE/(bb+'_RECEIPT.json')).read_text())
    raw=json.loads((BASE/(bb+'_REFINED_STDOUT.txt')).read_text())
    if (br['status']!=bp['status'] or br['status']!='FIXED_NEVO_NEW_ACTION_NUMERICALLY_QUALIFIED'
        or len(br['numerical_gates'])!=39 or not all(g['passed'] for g in br['numerical_gates'])
        or bp['result_sha256']!=PINS[bb+'_RESULT.json'] or raw['profile']!='refined' or raw['final']!=br['finals']['REFINED']['final']
        or raw['final']['YPCMB']!=result['lineage']['ordinary']['YHe']):raise AssertionError('Same-action BBN helium parent')
    sel=cal['selected'];ctx=cal['trials'][-1]['atomic_invocation']['context'];oldfix=cal['fixed']
    fixed=dict(Hunit=sel['Hunit'],OA=oldfix['omega_A'],OB=sel['OB'],OR=ctx['OR'],d0=oldfix['d0'],eps=oldfix['eps'],rG=.98/.99,Q0_over_Hstar=oldfix['Q0_over_H0'])
    ordinary=dict(Hstar=sel['Hunit'],Neff=sel['Neff'],T0=ctx['T0'],YHe=raw['final']['YPCMB'],YHe_old_fixture=sel['YHe'],omega_b=sel['physical_omega_b'],helium_source='Accepted same-action BBN refined YPCMB; no fit')
    if result['lineage']['fixed']!=fixed or result['lineage']['ordinary']!=ordinary:raise AssertionError('Physical ledger match')
    tables={}
    for arm,count,dlna in (('DEFAULT',8001,8.49e-5),('HALF',16001,4.245e-5)):
        d=json.loads((BASE/(ATOMIC+'_'+arm+'_OUTPUT.json')).read_text());rows=d['rows']
        if (d['status']!='COMPLETE_ATOMIC_HISTORY_ONLY' or d['mode']!='external' or not d['zero_injection']
            or d['output_count']!=count or len(rows)!=count or d['dlna']!=dlna
            or d['columns']!=['z','xe_per_H','Tm_K','external_grid_H_s_inverse_or_null']
            or any(d[k]!=ordinary[v] for k,v in [('omega_b','omega_b'),('T0_K','T0'),('YHe_atomic','YHe'),('Hcal_km_s_Mpc','Hstar')])
            or d['nH0_cm3']<=0 or d['fHe']<=0):raise AssertionError('Atomic header identity')
        if any(len(row)!=4 or row[0]!=8000*j/(count-1) or not all(math.isfinite(t) and t>0 for t in row[1:3]) for j,row in enumerate(rows)):
            raise AssertionError('Complete uniform atomic table')
        tables[arm]=d
    if any(c[0]!=f[0] for c,f in zip(tables['DEFAULT']['rows'],tables['HALF']['rows'][::2])):raise AssertionError('Paired atomic z grid')
    ledger=dict(Rb0=3*sel['OB']/(4*ctx['og']),og_old_units=ctx['og'],OR_old_units=ctx['OR'],og_new_units=ctx['og']/fixed['rG'],OB_new_units=sel['OB']/fixed['rG'],Gbare_over_GN=.99)
    return fixed,ordinary,ledger,tables


def quad(func,lo,hi,n):
    t,w=np.polynomial.legendre.leggauss(n);x=(lo+hi)/2+(hi-lo)*t/2
    return float((hi-lo)*np.dot(w,func(x))/2)


class Background:
    def __init__(self,fixed,ledger):
        self.fixed=fixed;self.Rb0=ledger['Rb0'];self.hs=fixed['Hunit']*1000/MPC;self.unit=CP/(self.hs*MPC)
    def E(self,a):
        return np.array([background(math.log(float(t)),self.fixed)['h'] for t in np.asarray(a).reshape(-1)]).reshape(np.asarray(a).shape)
    def H(self,z):return self.hs*self.E(1/(1+np.asarray(z)))


def distances(bg,z,n):
    a=1/(1+z)
    rs=bg.unit*quad(lambda t:1/(t*t*bg.E(t)*np.sqrt(3*(1+bg.Rb0*t))),0.,a,n)
    dm=bg.unit*quad(lambda x:np.exp(-x)/bg.E(np.exp(x)),math.log(a),0.,n)
    return dict(rs_Mpc=rs,DM_Mpc=dm,theta100=100*rs/dm,ell_A=math.pi*dm/rs)


def observables(bg,data,thin,n):
    arr=np.array([r[:3] for r in data['rows'][::thin]],dtype=float);arr=arr[arr[:,0]>=10]
    z,xe=arr[:,0],arr[:,1];aa=1+z;dz=np.diff(z)
    if not np.all(dz>0) or not np.allclose(dz,dz[0],rtol=0,atol=1e-12):raise AssertionError('Uniform thinned z grid')
    nh=data['nH0_cm3']*1e6;rate=CP*SIGMA_T*nh*xe*aa**3;td=rate/(aa*bg.H(z))
    tau=np.concatenate(([0.],np.cumsum(dz*(td[1:]+td[:-1])/2)))
    lv=np.log(rate/aa)-tau;i=int(np.argmax(lv))
    if not 0<i<len(z)-1:raise AssertionError('Interior visibility peak')
    v=lv[i-1:i+2];curv=v[0]-2*v[1]+v[2]
    if curv>=0:raise AssertionError('Negative visibility curvature')
    off=float(dz[0]*(v[0]-v[2])/(2*curv))
    if not math.isfinite(off) or abs(off)>dz[0]:raise AssertionError('Parabolic visibility vertex')
    zs=float(z[i]+off);dragder=td*aa/bg.Rb0;drag=np.concatenate(([0.],np.cumsum(dz*(dragder[1:]+dragder[:-1])/2)))
    low=quad(lambda zz:CP*SIGMA_T*nh*(1+2*data['fHe'])*(1+zz)**3/(bg.H(zz)*bg.Rb0),0.,10.,n)
    if not 0<1-low<1<drag[-1] or not np.all(np.diff(drag)>0):raise AssertionError('Drag interval bracket')
    zd=[float(np.interp(target,drag,z)) for target in (1-low,1.)];rd=[distances(bg,zz,n)['rs_Mpc'] for zz in reversed(zd)]
    ds=distances(bg,zs,n);tail=bg.unit*quad(lambda a:1/(a*a*bg.E(a)*np.sqrt(3*(1+bg.Rb0*a))),0.,1e-8,n)
    bound=bg.unit*1e-8/math.sqrt(3*bg.fixed['OR']/bg.fixed['rG'])
    out=dict(zstar=zs,**ds,drag_redshift_interval=zd,drag_ruler_Mpc_interval=rd,unknown_low_z_drag_depth_max=low,
        Rb_at_visibility_peak=bg.Rb0/(1+zs),early_a_below_1e_minus8_sound_Mpc=tail,early_tail_model_upper_bound_Mpc=bound,
        early_tail_fraction_of_rs=tail/ds['rs_Mpc'],visibility_peak_index=i,visibility_parabola_offset=off,
        visibility_convention='per conformal time; unknown low-z normalization constant omitted',
        descriptor_theta100=1.0411,descriptor_summary_error=.0003,fractional_theta_descriptor_offset=ds['theta100']/1.0411-1,
        descriptor_scope='Ancestor calibration exposed; not holdout, likelihood or superiority evidence')
    if not all(math.isfinite(t) and t>0 for key in FIELDS for t in np.atleast_1d(out[key])) or not 0<tail<=bound*(1+1e-13):raise AssertionError('Positive finite rulers/within-model early-tail bound')
    return out


def main():
    global RUN_SOURCE,RUN_MANIFEST
    tick=time.monotonic();RUN_SOURCE=sha(__file__)
    if list(BASE.glob(STEM+'_*')):raise FileExistsError('Existing runtime prefix; no resume, overwrite or orphan reuse')
    fixed,ordinary,ledger,tables=authenticate();bg=Background(fixed,ledger)
    manifest=dict(source_sha256=RUN_SOURCE,input_sha256=dict(SEALS),fixed=fixed,ordinary=ordinary,photon_baryon_ledger=ledger,arms=[list(t) for t in ARMS],numpy_version=np.__version__,gate_count=22)
    RUN_MANIFEST=write(STEM+'_MANIFEST.json',manifest);journal('OWNER_START')
    rows=[];gates=[]
    for label,atomic,thin,n in ARMS:
        recheck();obs=observables(bg,tables[atomic],thin,n);row=dict(label=label,atomic=atomic,thinning=thin,gauss_order=n,observables=obs)
        pn=STEM+'_'+label+'_CP.json';cn=STEM+'_'+label+'_CP_COMMIT.json';h=write(pn,row);ch=write(cn,dict(manifest=manifest,arm=label,payload=pn,sha256=h))
        journal('CHECKPOINT',arm=label,payload=pn,sha256=h,commit_sha256=ch);rows.append(row)
        print(json.dumps(dict(arm=label,status='SAVED_ARITHMETIC_CHECKPOINT')),flush=True)
    ref=rows[1]['observables'];comparisons=[]
    for index,tol in ((0,2e-4),(2,1e-4),(3,2e-8)):
        signed={}
        for key in FIELDS:
            delta=np.array(rows[index]['observables'][key])/np.array(ref[key])-1;err=float(np.max(abs(delta)))
            signed[key]=delta.tolist();gates.append(dict(name=rows[index]['label']+'_'+key,error=err,tolerance=tol,passed=err<=tol))
        comparisons.append(dict(label=rows[index]['label'],signed_fractional_differences=signed))
    for row in rows:
        o=row['observables'];err=abs(o['theta100']*o['ell_A']/(100*math.pi)-1)
        gates.append(dict(name=row['label']+'_angular_identity',error=err,tolerance=1e-13,passed=err<=1e-13))
    if len(gates)!=22:raise AssertionError('Frozen22 gate census')
    ok=all(g['passed'] for g in gates);status='NEW_BBN_ACOUSTIC_ARITHMETIC_PASS' if ok else 'NEW_BBN_ACOUSTIC_ARITHMETIC_FAILED'
    result=dict(status=status,all_numerical_gates_passed=ok,manifest=manifest,rows=rows,comparisons=comparisons,numerical_gates=gates,
        H_today_km_s_Mpc=fixed['Hunit']*background(0.,fixed)['h'],elapsed_seconds=time.monotonic()-tick,
        scope='Same-action BBN-helium saved atomic acoustic/drag geometry only; early plasma/reionization/primordial/anisotropy/data fit not qualified')
    recheck();rh=write(STEM+'_RESULT.json',result)
    report=['# NEW same-action BBN-helium acoustic/drag readout V001','',status,f'{sum(g["passed"] for g in gates)}/22 frozen numerical controls PASS.','',
      'Fixed .99-GN source and accepted BBN helium; no new atomic/BBN call or parameter adjustment.',
      '100theta was exposed to ancestor calibration. This comparison is development evidence, not a holdout or likelihood.','',
      '| Arm | zstar | rs Mpc | DM Mpc | 100theta | drag z interval | drag rs Mpc interval |','|---|---:|---:|---:|---:|---|---|']
    for row in rows:
        o=row['observables'];report.append(f"| {row['label']} | {o['zstar']:.12g} | {o['rs_Mpc']:.12g} | {o['DM_Mpc']:.12g} | {o['theta100']:.12g} | {o['drag_redshift_interval']} | {o['drag_ruler_Mpc_interval']} |")
    report+=['','Unknown low-z drag depth and the adopted high-temperature radiation extrapolation remain explicitly scoped in JSON. All signed refinements and failures retained.']
    recheck();reph=write(STEM+'_REPORT.md',('\n'.join(report)+'\n').encode(),True)
    events=[json.loads(x) for x in (BASE/(STEM+'_JOURNAL.jsonl')).read_text().splitlines()]
    if [e['event'] for e in events]!=['OWNER_START']+['CHECKPOINT']*4 or [e['arm'] for e in events[1:]]!=[a[0] for a in ARMS]:raise AssertionError('Ordered four-arm journal')
    for e,row in zip(events[1:],rows):
        co=json.loads((BASE/(STEM+'_'+row['label']+'_CP_COMMIT.json')).read_text());cp=json.loads((BASE/e['payload']).read_text())
        if (e['owner']!='root' or e['pid']!=os.getpid() or e['source_sha256']!=RUN_SOURCE or e['manifest_sha256']!=RUN_MANIFEST
            or e['commit_sha256']!=sha(BASE/(STEM+'_'+row['label']+'_CP_COMMIT.json'))
            or co!=dict(manifest=manifest,arm=row['label'],payload=e['payload'],sha256=e['sha256']) or sha(BASE/e['payload'])!=e['sha256'] or cp!=row):raise AssertionError('Full committed arm custody')
    recheck();journal('OWNER_COMPLETE',status=status,result_sha256=rh,gate_count=22,passed=sum(g['passed'] for g in gates))
    write(STEM+'_RECEIPT.json',dict(status=status,source_sha256=RUN_SOURCE,manifest=manifest,result_sha256=rh,report_sha256=reph,manifest_sha256=RUN_MANIFEST,journal_sha256=sha(BASE/(STEM+'_JOURNAL.jsonl')),output_sha256=dict(CREATED)))
    recheck();print(json.dumps(dict(status=status,result_sha256=rh,elapsed_seconds=result['elapsed_seconds'])),flush=True)
    return 0 if ok else 3


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--execute',action='store_true')
    if not ap.parse_args().execute:raise SystemExit('Root alone launches --execute')
    if list(BASE.glob(STEM+'_*')):raise SystemExit('Existing runtime prefix preserved; no retry or failure mutation')
    try:raise SystemExit(main())
    except Exception as exc:
        stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')
        write(STEM+'_FAILED_'+stamp+'.json',dict(status='EXECUTION_ERROR_PRESERVED',error=repr(exc),pid=os.getpid(),time=now(),source_sha256=sha(__file__)))
        raise

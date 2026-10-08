"""Root-owned saved-parameter source-loading screen; no scientific replay."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import math
import os
import time

BASE=Path(__file__).resolve().parent
STEM='CONSTRAINED_U_FIXED_CLOCK_STATIC_LOADING_V001'
PINS={
    STEM+'.md':'e280863de0287d0ae274f88059ad7f8fe169d0e3c6ef8631a9be617d26dc0153',
    'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md':'e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0',
    'SAME_T_CLOCK_GRADIENT_GEOMETRIC_EPOCHS_V002_RESULT.json':'b4fe2f337ceb598182db936328ea49ee5272105b573789dd908ebebef7b4929c',
    'INVARIANT_CLOCK_GRADIENT_SAME_T_STATIONARY_CURRENT_AND_CENTER_V001.md':'c868cf604996b853dff433e999dfe870db4c14398d9b032b0602acdad55d8713',
    'INVARIANT_CLOCK_JOINT_CALIBRATION_V003_RESULT.json':'c92eb0ce131a61009361f2ead3f4db7522d3eabb22f7e3d472f0e4e0c116c24f',
}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def save(suffix,obj):
    p=BASE/(STEM+suffix)
    with p.open('x') as f:
        json.dump(obj,f,sort_keys=True,separators=(',',':'),allow_nan=False)
        f.write('\n')
    p.chmod(0o444)
    return sha(p)


def execute():
    started=time.monotonic()
    for name,h in PINS.items():
        if sha(BASE/name)!=h: raise ValueError('Direct seal changed: '+name)
    lineage=dict(source_sha256=sha(__file__),inputs=PINS)
    rawp,recp=(BASE/(STEM+s) for s in ('_RESULT.json','_RECEIPT.json'))
    if rawp.exists() or recp.exists():
        if not (rawp.exists() and recp.exists()): raise ValueError('Partial preserved; no replay')
        raw,rec=(json.loads(p.read_text()) for p in (rawp,recp))
        if (raw['lineage']!=lineage or rec['lineage']!=lineage or rec['raw_sha256']!=sha(rawp)
                or rec['gates']!=raw['gate_summary']): raise ValueError('Completed checkpoint changed')
        print(json.dumps(dict(status='authenticated saved checkpoint; no recalculation',gates=raw['gate_summary'])))
        return
    saved=json.loads((BASE/'SAME_T_CLOCK_GRADIENT_GEOMETRIC_EPOCHS_V002_RESULT.json').read_text())
    fixed,bg=saved['fixed'],saved['epochs'][-1]
    if bg['a']!=1.: raise ValueError('Actual saved today required')
    KB,C,Gbare,ell_Mpc,Phi=.02,1.98,.99,1e-4,-1e-8
    RH=299792.458/fixed['Hunit']
    L=ell_Mpc/RH
    Dgn=bg['w']/bg['cs']
    Db=Gbare*Dgn
    Q=100*bg['qbar']
    xcrit=(Db+math.sqrt(Db*Db+2*C*Db/(L*L)))/C
    rcrit=RH/math.sqrt(xcrit)
    ar=2*C*RH*RH*ell_Mpc*ell_Mpc/Db
    rcrit2=math.sqrt(ar/(2*(math.sqrt(ell_Mpc**4+ar)+ell_Mpc**2)))
    s,qp,eps=bg['s'],bg['qbar'],fixed['eps']
    lower=eps*s/((1+s)*qp*(qp+1))
    upper=eps/((1+s)*qp*(math.sqrt(1+eps)+qp))
    gates=[]

    def gate(name,value,limit,sense='le'):
        passed=value<=limit if sense=='le' else value>limit
        gates.append(dict(name=name,value=float(value),limit=float(limit),sense=sense,passed=bool(passed)))

    for label,v in [('Dgn',Dgn),('Dbare',Db),('cs2',bg['cs']),('critical_x',xcrit),('clock_lower',lower),('clock_upper',upper),('Q',Q),('ell',ell_Mpc)]:
        gate(label+'_positive',v,0.,'gt')
    rootcontact=(C/2)*L*L*xcrit*xcrit/(1+L*L*xcrit)
    gate('critical_equation',abs(rootcontact/Db-1),1e-13)
    gate('independent_inverse_critical',abs(rcrit/rcrit2-1),1e-13)
    rows=[]
    for rkpc in (.1,1.,10.,100.):
        r=rkpc/1000
        x=(RH/r)**2
        l2x=L*L*x
        F0=1/(1+l2x)
        one_minus=l2x/(1+l2x)
        gradient=(C/2)*x*one_minus
        full=gradient-Db
        gn_contact=x*one_minus-Dgn
        gate(str(rkpc)+'_kernel_two_forms',abs((1-F0)-one_minus),1e-13)
        gate(str(rkpc)+'_GN_contact',abs(full/Gbare-gn_contact)/(x*one_minus+Dgn),1e-13)
        gate(str(rkpc)+'_inverse_units',abs((math.sqrt(x)*r)/RH-1),1e-13)
        rows.append(dict(inverse_wavenumber_kpc=rkpc,x=x,L2x=l2x,F0=F0,one_minus_F0=one_minus,
                         bare_gradient_contact=gradient,clock_load=Db,full_bare_contact=full,
                         load_over_gradient=Db/gradient,full_over_gradient=full/gradient,
                         full_GN_mu=gn_contact/x,static_source_sign='attractive' if full>0 else 'sign_reversed',
                         illustrative_normal_velocity=abs(math.sqrt(x)*F0*Phi/Q)))
    gate('positive_discriminant',Db*Db+2*C*Db/(L*L),0.,'gt')
    result=dict(lineage=lineage,fixed=dict(KB=KB,C=C,Gbare_over_GN=Gbare,ell_Mpc=ell_Mpc,Hstar_km_s_Mpc=fixed['Hunit'],
                Phi=Phi,physical_budget_conversion='Dstar_bare=.99*saved_GN_W/cs2'),
                present=dict(W_GN=bg['w'],cs2=bg['cs'],D_GN=Dgn,D_bare=Db,Q_over_Hstar=Q),
                critical=dict(x=xcrit,inverse_wavenumber_kpc=rcrit*1000,independent_inverse_kpc=rcrit2*1000,
                              root_gradient_contact=rootcontact),rows=rows,
                physical_diagnostics=dict(lower_fraction=lower,upper_fraction=upper,delta_Q_over_Q=-Phi,
                    branch_domain_passed=(-lower<-Phi<upper),density_contrast=-Phi/bg['cs'],
                    density_contrast_below_1percent=abs(Phi/bg['cs'])<.01,
                    interpretation='illustrative linear coefficients only; branch membership does not certify nonlinear or linear-state control'),
                gates=gates,gate_summary=dict(total=len(gates),passed=sum(g['passed'] for g in gates),failed=[g['name'] for g in gates if not g['passed']]),
                scope='unadopted cTheta0 constrained action; frozen local static operator, not observed galaxy/ghost/global stationary proof')
    if sha(__file__)!=lineage['source_sha256'] or any(sha(BASE/n)!=h for n,h in PINS.items()):
        raise ValueError('Input/source changed before publication')
    rawsha=save('_RESULT.json',result)
    save('_RECEIPT.json',dict(lineage=lineage,raw_sha256=rawsha,gates=result['gate_summary'],pid=os.getpid(),
                              finished=datetime.now(timezone.utc).isoformat(),wall_seconds=time.monotonic()-started))
    if sha(__file__)!=lineage['source_sha256'] or any(sha(BASE/n)!=h for n,h in PINS.items()):
        raise ValueError('Input/source changed after publication; preserve for root review')
    print(json.dumps(dict(raw_sha256=rawsha,gates=result['gate_summary'],critical=result['critical'],rows=rows,physical_diagnostics=result['physical_diagnostics'])))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--execute',action='store_true')
    if not parser.parse_args().execute: parser.error('Root-owned --execute required')
    execute()

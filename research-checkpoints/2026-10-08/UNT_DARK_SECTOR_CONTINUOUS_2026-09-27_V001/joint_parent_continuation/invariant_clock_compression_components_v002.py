"""Technical repair of six failed component-oracle checks; unchanged gates.

V001 saved six failures. The radial pressure oracle incorrectly used -c*tauN
instead of -tauN/c; the multiplier itself had the correct factor. Three
near-center pointwise coupled-RHS checks lost digits by subtracting O(H)
terms to recover O(H^3 R^2). V002 evaluates that algebra with50-digit
Decimal and reconstitutes on-shell FLRW inputs at that precision; merely
promoting rounded A and chi would not repair input conditioning.

All39 passing V001 controls are reused. This does NOT retroactively qualify
the binary outward coupled helper: its failed1e-9 gate remains preserved.
The planned physical solver instead uses inward chi plus integrated mass.
No source evolution, new parameter, calibration or scientific claim here.
"""
from pathlib import Path
from decimal import Decimal, localcontext
import json
import time
import numpy as np
import invariant_clock_compression_components_v001 as prev
import invariant_clock_compression_radial_v002 as repaired

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'INVARIANT_CLOCK_COMPRESSION_COMPONENTS_V002_RESULT.json'
OLD=ROOT/'INVARIANT_CLOCK_COMPRESSION_COMPONENTS_V001_RESULT.json'
OLDSHA='01888050c639f6d0a9e6999661342277bb7cb5270761b34aa1875d646a0ec3f0'

def exact_coupled(r,m,X,K,rb):
    with localcontext() as context:
        context.prec=60
        R,mm,XX,KK,rho=map(lambda v:Decimal(str(float(v))),(r,m,X,K,rb))
        cT=Decimal('.01'); F=1+3*cT/2
        H=((XX*mm-KK+rho)/(3*F)).sqrt();Hd=-(XX*mm+rho)/(2*F)
        B=1-H*H*R*R;A=1/B.sqrt();tr=-H*R/B;Hr=Hd*tr
        Br=-2*H*H*R-2*H*Hr*R*R;Ar=-Br*A/(2*B)
        u=H*R/B;ur=(Hr*R+H)/B-H*R*Br/(B*B)
        chi=-3*cT*H;chir=-3*cT*Hd*tr
        rho0=(XX*mm+rho)/B-KK;j0=(XX*mm+rho)*u
        out=repaired.coupledradial_rhs(R,A,chi,rho0,j0,u,ur,Decimal(0),cT)
        return float(Ar),float(chir),out['A_R'],out['chi_R']

def main():
    if OUT.exists():raise FileExistsError(OUT)
    started=time.monotonic()
    if prev.sha(OLD)!=OLDSHA:raise ValueError('changed failed receipt')
    old=json.loads(OLD.read_text());checks=[dict(c) for c in old['controls'] if c['passed']]
    cal=json.loads(prev.CAL.read_text());saved=json.loads(prev.base.SOURCE.read_text())
    if prev.sha(prev.CAL)!=prev.CALSHA:raise ValueError('changed calibration')
    saved['inherited']=cal['fixed'];model=prev.base.Model(saved,1);rows=[]
    for n in (64,128,256):
        r=(np.arange(n)+.5)*.02/n
        g=prev.oracle(model,r,prev.polar_slice(model,r,2048))
        correct_Prchi=g['sig']*g['chir']/g['A']+g['chi']**2/(2*prev.CT)-g['tauN']/g['c']
        err=prev.maximum(g['Pr0']+correct_Prchi-g['Prtotal'])/prev.maximum(g['Prtotal'])
        checks.append(dict(name=f'{n}_FLRW_pressure_corrected_oracle',error=err,gate=1e-9,passed=err<=1e-9))
        values=np.array([exact_coupled(rr,mm,xx,kk,bb) for rr,mm,xx,kk,bb
                         in zip(r,g['m'],g['X'],g['K'],g['rb'])]).T
        ae=prev.maximum(values[2]-values[0])/prev.maximum(values[0])
        ce=prev.maximum(values[3]-values[1])/prev.maximum(values[1])
        for label,error in (('A_R',ae),('chi_R',ce)):
            checks.append(dict(name=f'{n}_FLRW_{label}_decimal_inputs_arithmetic',error=error,gate=1e-9,passed=error<=1e-9))
        rows.append(dict(nodes=n,pressure_error=err,A_R_error=ae,chi_R_error=ce))
    result=dict(protocol=__doc__,parent_sha256=OLDSHA,reused_passing_controls=39,
        preserved_binary_helper_failures=[c for c in old['controls'] if not c['passed'] and 'chi_R' in c['name']],
        rows=rows,controls=checks,all_controls_passed=all(c['passed'] for c in checks),
        elapsed_seconds=time.monotonic()-started,
        hashes={str(p):prev.sha(p) for p in (Path(__file__),Path(prev.__file__),Path(repaired.__file__),
                                          Path(prev.radial.__file__),OLD,prev.CAL)})
    with OUT.open('x') as file:json.dump(result,file,indent=2,allow_nan=False)
    print(json.dumps(dict(rows=rows,checks=len(checks),all_controls_passed=result['all_controls_passed'],
        elapsed_seconds=result['elapsed_seconds'],result_sha256=prev.sha(OUT)),indent=2))
    if not result['all_controls_passed']:raise SystemExit(1)

if __name__=='__main__':main()

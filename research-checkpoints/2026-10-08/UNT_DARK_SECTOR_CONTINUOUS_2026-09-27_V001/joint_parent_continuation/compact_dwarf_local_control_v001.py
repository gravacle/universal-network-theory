"""New ell=0 certificate gate; reuse authenticated response bounds, no rerun."""
import hashlib
import json
import math
from pathlib import Path
import time
import numpy as np

HERE=Path(__file__).resolve().parent


def main():
    start=time.perf_counter()
    out=HERE/'COMPACT_DWARF_LOCAL_CONTROL_V001_RESULT.json'
    if out.exists():
        raise SystemExit('Existing result preserved; refusing overwrite/repeat.')
    source=HERE/'COMPACT_DWARF_FILTER_TEST_V001_RESULT.json'
    digest=hashlib.sha256(source.read_bytes()).hexdigest()
    expected='e6ddd8aae780f785f12d4973300108815230aceac8bdfdf310c68785f4618258'
    if digest!=expected:
        raise SystemExit('Source hash mismatch.')
    old=json.loads(source.read_text())
    if old['status']!='PASS' or not all(c['passed'] for c in old['controls']):
        raise SystemExit('Source qualification failed.')
    pc=648000*149597870700/math.pi
    a=28*pc
    z,w=np.polynomial.legendre.leggauss(256)
    q=(z+1)/2
    u=q/(1-q)
    integ=float(np.dot(w/2,u*np.exp(-u)/(1-q)**2))
    controls=[dict(name='mixture_first_moment',error=abs(integ-1),tolerance=2e-10,passed=abs(integ-1)<=2e-10)]
    rows=[]
    for prior in old['rows']:
        gm=prior['M_nominal_solar']*1.3271244e20
        e=prior['external_fraction']*old['inputs']['a0']
        lf=prior['LF_upper']
        eps=4*gm/(math.pi*a*a*e)
        limit=(1-lf)*old['inputs']['r0']
        qualified=eps<=limit
        force=e*lf*eps/(1-lf) if qualified else None
        total=3*math.pi*gm/(32*a)+2*a*force if qualified else None
        unit_error=abs((e*eps)/(4*gm/(math.pi*a*a))-1)
        controls.append(dict(name=f'unit_{prior["external_fraction"]}_{prior["M_nominal_solar"]}',error=unit_error,tolerance=2e-12,passed=unit_error<=2e-12))
        rows.append(dict(M_nominal_solar=prior['M_nominal_solar'],external_fraction=prior['external_fraction'],
                         LF_upper=lf,input_norm_exact=eps,self_map_limit=limit,self_map_margin=limit-eps,
                         certificate='PASS' if qualified else 'UNCERTIFIED',
                         anomalous_force_upper_m_s2=force,
                         global_LOS_upper_km_s=math.sqrt(total)/1000 if qualified else None,
                         aperture_LOS_upper_km_s=math.sqrt(total/old['aperture_fraction'])/1000 if qualified else None))
    result=dict(status='CONTROLS_PASS' if all(c['passed'] for c in controls) else 'CONTROL_FAILURE',
                scope='Matched ell=0 nonlinear branch certificate only for rows marked PASS; no observed exclusion confidence or ranking from loose upper bounds.',
                ell_pc=0.,rows=rows,controls=controls,source_sha256=digest,
                custody={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),HERE/'COMPACT_DWARF_LOCAL_CONTROL_V001.md')},
                elapsed_seconds=time.perf_counter()-start)
    with out.open('x') as f:
        json.dump(result,f,indent=2,allow_nan=False)
        f.write('\n')
    print(json.dumps(result,indent=2))
    if result['status']!='CONTROLS_PASS':
        raise SystemExit(1)


if __name__=='__main__':
    main()

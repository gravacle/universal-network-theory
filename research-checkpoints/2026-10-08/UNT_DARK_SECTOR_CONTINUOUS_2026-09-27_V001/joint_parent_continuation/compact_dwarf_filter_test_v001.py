"""Prospectively fixed Plummer force/velocity upper bounds; no halo inference."""
import hashlib
import json
import math
from pathlib import Path
import time

import numpy as np

HERE = Path(__file__).resolve().parent
A0 = 1.0059833281731022e-10
GC = 3*math.pi*A0/8
GS = 25.51664211557329*A0
PC = 648000*149597870700/math.pi
ELL, A, AP = 100*PC, 28*PC, 67*PC
GM_SUN = 1.3271244e20
R0, S0 = .01, .02


def root_t(s, h):
    return 2/math.sqrt(3)*np.sinh(np.arcsinh(3*math.sqrt(3)/2*h/(GC*s*s))/3)


def enclosure(h, n):
    s = np.linspace(0,1,n+1)
    values = np.zeros(n+1)
    t = root_t(s[1:],h)
    values[1:] = 1/(1+t*t)
    weights = np.diff(s*s)
    return float(np.dot(weights, values[:-1])), float(np.dot(weights, values[1:]))


def main():
    start = time.perf_counter()
    output = HERE/'COMPACT_DWARF_FILTER_TEST_V001_RESULT.json'
    if output.exists():
        raise SystemExit('Existing result preserved; refusing repeat/overwrite.')
    controls = []

    def gate(name, value, limit, strict=False):
        controls.append(dict(name=name,value=float(value),limit=float(limit),
                             margin=float(limit-value),passed=bool(math.isfinite(value) and (value<limit if strict else value<=limit))))

    z, w = np.polynomial.legendre.leggauss(256)
    q, weights = (z+1)/2,w/2
    t = q/(1-q)
    jac = 1/(1-q)**2
    gate('gaussian_mixture_normalization', abs(float(np.dot(weights,np.exp(-t)*jac))-1),2e-10)
    meanr = float(np.dot(weights,3*t**3/(1+t*t)**2.5*jac))
    virial = float(np.dot(weights,3*t**4/(1+t*t)**4*jac))
    gate('Plummer_mean_radius',abs(meanr/2-1),2e-9)
    gate('Plummer_virial',abs(virial/(3*math.pi/32)-1),2e-9)
    upper = AP/A
    rr = upper*q
    projected = float(np.dot(weights,2*rr/(1+rr*rr)**2))*upper
    fraction = AP*AP/(AP*AP+A*A)
    gate('Plummer_aperture',abs(projected/fraction-1),2e-10)
    rows = []
    for external_fraction in (.5,1.):
        e = external_fraction*A0
        zz = (e/GS)**2
        f0 = 1/math.sqrt(1+zz)
        gamma = zz/(1+zz)
        tt = gamma*(2*R0+R0**2)
        jmax = (1-tt)**(-.5)+gamma*(1+R0)**2*(1-tt)**(-1.5)
        djmax = 3*gamma*(1+R0)*(1-tt)**(-1.5)+3*gamma**2*(1+R0)**3*(1-tt)**(-2.5)
        modal_lip = 6*S0+3*S0*S0
        modal_map = jmax*R0+3*S0*S0+S0**3
        lw = jmax/(1-modal_lip)
        hlo, hhi = enclosure(e*f0,64)
        _, refined_hi = enclosure(e*f0,128)
        ts = root_t(q,e*f0)
        exact_quad = float(np.dot(weights,2*q/(1+ts*ts)))
        LF = f0*f0*hhi*(jmax*lw+djmax*(1+S0))
        gate(f'enclosure_{external_fraction}',max(hlo-exact_quad,exact_quad-hhi,0.),2e-10)
        gate(f'monotone_enclosure_{external_fraction}',max(refined_hi-hhi,0.),2e-12)
        cubic_error = float(np.max(np.abs((ts+ts**3)/(e*f0/(GC*q*q))-1)))
        gate(f'modal_root_{external_fraction}',cubic_error,2e-12)
        for mass in (340.,1020.,3400.):
            tag = f'{external_fraction}_{mass}'
            gm = GM_SUN*mass
            eps = gm/(math.pi*ELL*ELL*e)*(math.log1p(4*ELL*ELL/(A*A))+math.exp(-1))
            first = len(controls)
            gate(tag+'_binomial',tt,1.,True)
            gate(tag+'_modal_map',modal_map,S0)
            gate(tag+'_modal_contraction',modal_lip,1.,True)
            gate(tag+'_outer_contraction',LF,1.,True)
            gate(tag+'_outer_map',eps,(1-LF)*R0)
            certified = all(c['passed'] for c in controls[first:])
            force = e*LF*eps/(1-LF) if certified else None
            total = 3*math.pi*gm/(32*A)+2*A*force if certified else None
            rows.append(dict(external_fraction=external_fraction,M_nominal_solar=mass,
                             a_pc=28.,stellar_M_to_L=mass/340.,LF_upper=LF,
                             polarization_lower=hlo,polarization_upper=hhi,
                             input_norm_upper=eps,solution_norm_upper=eps/(1-LF) if certified else None,
                             certified=certified,anomalous_force_upper_m_s2=force,
                             total_velocity_second_moment_upper_m2_s2=total,
                             global_LOS_upper_km_s=math.sqrt(total)/1000 if certified else None,
                             aperture_LOS_upper_km_s=math.sqrt(total/fraction)/1000 if certified else None))
    result = dict(status='PASS' if all(c['passed'] for c in controls) else 'PARTIAL_OR_FAILED_CERTIFICATE',
                  scope='Conditional stationary same-source/tracer Plummer kinetic-budget bound; not a velocity fit, membership likelihood or observed confidence-level exclusion.',
                  inputs=dict(a0=A0,ratio=25.51664211557329,ell_pc=100.,a_pc=28.,
                              aperture_pc=67.,nominal_luminosity_solar=340.,r0=R0,s0=S0,
                              source_dark_mass_used=False,external_tides_omitted=True),
                  aperture_fraction=fraction,rows=rows,controls=controls,control_count=len(controls),
                  custody={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (Path(__file__), HERE/'COMPACT_DWARF_FILTER_TEST_V001.md',
                            HERE/'FILTERED_SOURCE_NONLINEAR_BOUND_V001.md')},
                  elapsed_seconds=time.perf_counter()-start)
    with output.open('x') as out:
        json.dump(result,out,indent=2,allow_nan=False)
        out.write('\n')
    print(json.dumps(dict(status=result['status'],control_count=len(controls),
                         failed_controls=[c for c in controls if not c['passed']],
                         rows=rows,elapsed_seconds=result['elapsed_seconds']),indent=2))
    if result['status'] != 'PASS':
        raise SystemExit(1)


if __name__ == '__main__':
    main()

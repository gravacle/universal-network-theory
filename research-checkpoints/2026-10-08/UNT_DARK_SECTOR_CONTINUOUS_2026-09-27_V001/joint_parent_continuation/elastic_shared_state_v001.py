"""One bounded elastic-state comparison, with prospective controls and no fit."""
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import time

import numpy as np

HERE = Path(__file__).resolve().parent
R = 25.51664211557329
GC = 3 * math.pi / 8
OB, OG, OL = .05, .25, .70
OM = OB + OG
H0, C_LIGHT, K_COM = 70., 299792.458, .1
K = C_LIGHT * K_COM / H0
AI, PSI_I = .01, -1e-9
F_LOCAL, DELTA_MAX = OG / (OG + OL), .1
LEVELS = (2048, 4096, 8192)


@lru_cache(None)
def gauss(n):
    z, w = np.polynomial.legendre.leggauss(n)
    return (z + 1) / 2, w / 2


def modes(h, n):
    s, w = gauss(n)
    t = 2 / math.sqrt(3) * np.sinh(np.arcsinh(3 * math.sqrt(3) / 2 * h / (GC * s * s)) / 3)
    weights = 2 * s * w
    energy = GC**2 * np.dot(weights, s**4 * (.5 * t*t + .75 * t**4))
    pol = GC * np.dot(weights, s*s*t)
    polprime = np.dot(weights, 1 / (1 + 3 * t*t))
    return float(energy), float(pol), float(polprime)


def response(x, n):
    fac = 1 / math.sqrt(1 + (x / R)**2)
    h, hp = x * fac, fac**3
    hpp = -3 * x / R**2 * fac**5
    energy, pol, pp = modes(h, n)
    mu = 1 - hp * pol / x
    mup = hp * pol / x**2 - (hpp * pol + hp*hp*pp) / x
    return energy, mu, mup, hp * pol


def material(x, n):
    q = modes(R, n)[0]
    t, w = gauss(n)
    # B(x)-B(0)=-integral_0^x t^2 mu'(t)dt avoids subtracting two Q-sized terms.
    eta = -x**3 * float(np.dot(w, t*t*np.array([response(x*z, n)[2] for z in t]))) / (2*q)
    energy, mu, mup, force = response(x, n)
    eta_direct = (-2*energy + x*force) / (2*q)
    kb = F_LOCAL * x**3 * mup / (4*q)
    return dict(x=x, Q=q, eta=eta, eta_direct=eta_direct, mu=mu,
                muprime=mup, kb=kb,
                kappa_local=.75*max(0., abs(eta)/DELTA_MAX-kb))


def expansion(a):
    e = math.sqrt(OM/a**3 + OL)
    return e, -1.5*OM/a**3/e


def growth(a):
    t, w = gauss(256)
    aa = a*t
    ee = np.sqrt(OM/aa**3 + OL)
    integ = a*float(np.dot(w, 1/(aa**3*ee**3)))
    e, ex = expansion(a)
    d = 2.5*OM*e*integ
    f = ex/e + 1/(a*a*e**3*integ)
    return d, f


def dust_state(a):
    d, f = growth(a)
    di, _ = growth(AI)
    psi = PSI_I * (d/a)/(di/AI)
    e, _ = expansion(a)
    v = 2*a**3*e*f*psi/(3*OM)
    delta = -2*a*K*K*psi/(3*OM)-3*e*v
    return np.array([delta, v, delta, v])


def rhs(loga, y, kappa, inspect=False):
    a = math.exp(loga)
    e, ex = expansion(a)
    db, vb, dg, vg = y
    weighted_v = OB*vb+OG*vg
    psi = -1.5/(a*K*K)*(OB*(db+3*e*vb)+OG*(dg+3*e*vg))
    phi = psi+6*kappa*OG/(a*K*K)*(dg-3*psi)
    psix = 1.5*weighted_v/(a**3*e)-phi
    dx = np.array([-K*K*vb/(a*a*e)+3*psix, phi/e,
                   -K*K*vg/(a*a*e)+3*psix,
                   (phi+4*kappa/3*(dg-3*psi))/e])
    if not inspect:
        return dx
    sx = OB*dx[0]+OG*dx[2]+3*ex*weighted_v+3*e*(OB*dx[1]+OG*dx[3])
    psix_alg = -psi-1.5/(a*K*K)*sx
    residual = abs(psix_alg-psix)/max(abs(PSI_I), abs(psix), abs(psix_alg))
    return dx, dict(a=a, delta_b=float(db), delta_g=float(dg), v_b=float(vb),
                    v_g=float(vg), Psi=float(psi), Phi=float(phi),
                    Weyl_sum=float(phi+psi), constraint_residual=float(residual))


def evolve(kappa, steps):
    logai = math.log(AI)
    step = -logai/steps
    y = dust_state(AI)
    max_residual = 0.
    trajectory = []
    for i in range(steps+1):
        x = logai+i*step
        if i % (steps//32) == 0 or i == steps:
            _, row = rhs(x, y, kappa, True)
            max_residual = max(max_residual, row['constraint_residual'])
            trajectory.append(row)
        if i == steps:
            break
        k1 = rhs(x, y, kappa)
        k2 = rhs(x+step/2, y+step*k1/2, kappa)
        k3 = rhs(x+step/2, y+step*k2/2, kappa)
        k4 = rhs(x+step, y+step*k3, kappa)
        y += step*(k1+2*k2+2*k3+k4)/6
    return dict(steps=steps, final=trajectory[-1],
                max_constraint_residual=max_residual, trajectory=trajectory)


def main():
    start = time.perf_counter()
    destination = HERE/'ELASTIC_SHARED_STATE_V001_RESULT.json'
    if destination.exists():
        raise SystemExit('Existing result preserved: refusing repeat/overwrite.')
    controls = []

    def check(name, error, tolerance):
        controls.append(dict(name=name, error=float(error), tolerance=tolerance,
                             passed=bool(math.isfinite(error) and error <= tolerance)))

    source_rows = []
    for x in (.1, 1.):
        low, high = material(x,128), material(x,256)
        for key in ('Q','eta','mu','muprime','kb','kappa_local'):
            check(f'quadrature_{x}_{key}', abs(low[key]/high[key]-1), 2e-6)
        check(f'eta_energy_identity_{x}', abs(high['eta_direct']/high['eta']-1), 2e-6)
        eps = x*1e-4
        left, right = material(x-eps,256), material(x+eps,256)
        bprime = high['Q']*(right['eta']-left['eta'])/eps
        check(f'chemical_derivative_{x}', abs(bprime/(-x*x*high['muprime'])-1), 2e-5)
        eprime = (response(x+eps,256)[0]-response(x-eps,256)[0])/(2*eps)
        check(f'source_energy_derivative_{x}', abs(eprime/response(x,256)[3]-1), 2e-6)
        check(f'positive_response_{x}', 0. if high['kb']>0 and high['muprime']>0 and high['mu']>0 and high['eta']<0 else 1., 0.)
        source_rows.append(high)
    small = material(.001,256)
    check('small_source_eta', abs(small['eta']/(-.001**3/(6*small['Q']))-1), .01)
    cases = []
    for label, kappa in [('dust_reference',0.)]+[(f'local_x_{r["x"]}', r['kappa_local']) for r in source_rows]:
        levels = [evolve(kappa,steps) for steps in LEVELS]
        check(f'{label}_material_causal', 0. if 0 <= kappa <= .75 else 1., 0.)
        for level in levels:
            check(f'{label}_constraint_{level["steps"]}', level['max_constraint_residual'], 2e-8)
        cases.append(dict(label=label,kappa=kappa,cL_over_c=math.sqrt(4*kappa/3),levels=levels))
    ref = cases[0]['levels'][-1]['final']
    exact_dust = dust_state(1.)
    check('dust_growth_integral', abs(ref['delta_b']/exact_dust[0]-1), 2e-6)
    check('dust_components_equal', abs(ref['delta_b']/ref['delta_g']-1), 2e-12)
    for case in cases:
        fine = case['levels'][-1]['final']
        for coarse in case['levels'][:-1]:
            for key in ('delta_b','delta_g','Phi','Psi'):
                check(f'{case["label"]}_refinement_{coarse["steps"]}_{key}',
                      abs((coarse['final'][key]-fine[key])/ref[key]), 2e-4)
        case['final_relative_to_dust'] = {key:fine[key]/ref[key] for key in ('delta_b','delta_g','Phi','Psi','Weyl_sum')}
    files = [Path(__file__), HERE/'ELASTIC_SHARED_STATE_V001.md']
    result = dict(status='PASS' if all(c['passed'] for c in controls) else 'FAIL',
                  scope='Conditional finite-epoch elastic candidate; not an observed likelihood, primordial mode or endpoint normalization fit.',
                  inputs=dict(r=R,Omega_b=OB,Omega_g=OG,Omega_Lambda=OL,H0_km_s_Mpc=H0,
                              k_comoving_per_Mpc=K_COM,a_initial=AI,Psi_initial=PSI_I,
                              local_fraction=F_LOCAL,local_density_strain_limit=DELTA_MAX,
                              no_initial_clock_charge=True,background_is_exposed_reference=True),
                  source_rows=source_rows,cases=cases,controls=controls,control_count=len(controls),
                  hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
                  elapsed_seconds=time.perf_counter()-start)
    with destination.open('x') as out:
        json.dump(result,out,indent=2,allow_nan=False)
        out.write('\n')
    print(json.dumps(dict(status=result['status'],controls=len(controls),
                         failed_controls=[c for c in controls if not c['passed']],
                         source_rows=source_rows,
                         growth=[{key:case[key] for key in ('label','kappa','cL_over_c','final_relative_to_dust')} for case in cases],
                         elapsed_seconds=result['elapsed_seconds']),indent=2))
    if result['status'] != 'PASS':
        raise SystemExit(1)


if __name__ == '__main__':
    main()

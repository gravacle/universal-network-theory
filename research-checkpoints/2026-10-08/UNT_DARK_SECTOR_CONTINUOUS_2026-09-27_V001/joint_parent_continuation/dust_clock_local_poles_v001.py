"""Frozen local dust/clock poles; no parameter fit or time integration."""
import cmath
import hashlib
import itertools
import json
import math
from pathlib import Path
import time

import numpy as np

HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / 'DUST_CLOCK_LOCAL_POLES_V001.md'
OUTPUT = HERE / 'DUST_CLOCK_LOCAL_POLES_V001_RESULT.json'
BETA, ELL_MPC, A0 = .5, .0001, 1.0059833281731022e-10
OB, HVAC, HREF = .02235, 50.3528974592, 100.
C_KMS, C_SI = 299792.458, 299792458.
MPC = 648000 * 149597870700 / math.pi * 1e6


def poles(h, r, p, q, beta):
    ff = 1 + 1.5 * beta
    aa = 3 + 2 / beta
    eps = q*q*(2+q*q)
    u = 1+eps
    bb = 3*u*r/aa-r/ff+eps*p*p/aa
    cc = u*r/aa*(p*p+3*r/ff)
    disc = math.hypot(bb, 2*math.sqrt(cc))
    if cc == 0:
        xp, xm = max(0., -bb), min(0., -bb)
    elif bb >= 0:
        xp = 2*cc/(bb+disc)
        xm = -.5*(bb+disc)
    else:
        xp = .5*(disc-bb)
        xm = -cc/xp
    grow = 2*xp/(h+math.sqrt(h*h+4*xp)) if xp else 0.
    roots = [complex(grow), complex(-h-grow)]
    z = cmath.sqrt(h*h/4+xm)
    roots += [-h/2+z, -h/2-z]
    return dict(F=ff, A=aa, eps=eps, u=u, B=bb, C=cc,
                xplus=xp, xminus=xm, growth=grow, roots=roots)


def matrix(h, r, p, q, beta):
    fbg, aa = 1+1.5*beta, 3+2/beta
    eps = q*q*(2+q*q)
    return np.array([[-h, r/fbg, -p*p/aa, 0.],
                     [1., 0., 0., 0.],
                     [eps, 0., 0., 1+eps],
                     [0., -r, -3*r/aa, -h]])


def mode(h, r, p, q, beta):
    z = poles(h, r, p, q, beta)
    ss, aa = z['growth'], z['A']
    psi = -1.
    theta = psi/ss
    sigma = aa*(-z['xplus']+r/z['F'])*psi/(p*p*ss)
    dd = (ss*sigma-z['eps']*psi)/z['u']
    # n=Psi+sigma_dot avoids subtracting D and -Psi at large q.
    nn = psi+ss*sigma
    yy = np.array([psi, theta, sigma, dd])
    mm = matrix(h, r, p, q, beta)
    terms = np.abs(mm)*np.abs(yy)[None, :]
    denom = np.maximum(terms.sum(axis=1)+abs(ss)*np.abs(yy), 1e-30)
    residual = float(np.max(np.abs(mm@yy-ss*yy)/denom))
    return z, dict(Psi=psi, theta=theta, sigma=sigma, D=dd, n=nn,
                   Delta=p*p*dd/r, delta_N=p*p*dd/r-3*h*theta,
                   potential_ratio=-psi/dd,
                   equation_residual=residual,
                   lapse_constraint_residual=abs(nn/z['u']-psi-dd)
                       /max(abs(nn/z['u'])+abs(psi)+abs(dd), 1e-30))


def row(a, k):
    h = math.sqrt((OB/a**3+(HVAC/HREF)**2)/(1+1.5*BETA))
    r = 1.5*OB/a**3
    p, q = C_KMS*k/(a*HREF), ELL_MPC*k/a
    z, m = mode(h, r, p, q, BETA)
    f = 1/(1+q*q)
    one_minus = q*q*(2+q*q)/(1+q*q)**2
    accel_factor = C_SI**2*(k/a/MPC)/A0
    nscreen = .01*one_minus/(2*f**3*accel_factor)
    psiscreen = nscreen/abs(m['n']) if m['n'] else None
    dscreen = psiscreen*abs(m['Delta']) if psiscreen is not None else None
    return dict(a=a, k_Mpc_inverse=k, physical_inverse_k_Mpc=a/k,
                physical_wavelength_Mpc=2*math.pi*a/k,
                H_over_Href=h, r_over_Href_squared=r, p_over_Href=p,
                q=q, growth_over_H=z['growth']/h,
                growth_inverse_Gyr=MPC/(HREF*1000*z['growth'])/(365.25*86400*1e9),
                xplus_over_r=z['xplus']/r,
                growing_mode=m,
                asymptotic_spatial_1percent_n_screen=nscreen,
                asymptotic_spatial_1percent_Psi_screen=psiscreen,
                asymptotic_spatial_1percent_Delta_screen=dscreen)


def main():
    if OUTPUT.exists():
        raise SystemExit('Refusing to overwrite an existing result')
    started = time.perf_counter()
    controls = []

    def check(name, error, tolerance):
        controls.append(dict(name=name, error=float(error), tolerance=tolerance,
                             passed=math.isfinite(error) and error <= tolerance))

    for beta, q, p in itertools.product((.1,.5,2.), (.001,.1,1.,10.), (1.,3.,10.)):
        h, r = .4, .23
        z, mm = mode(h, r, p, q, beta)
        direct = np.linalg.eigvals(matrix(h, r, p, q, beta))
        roots = z['roots']
        error = min(max(abs(roots[i]-perm[i])/max(1.,abs(roots[i]),abs(perm[i]))
                        for i in range(4)) for perm in itertools.permutations(direct))
        label = f'beta={beta}:q={q}:p={p}'
        check('matrix_poles:'+label, error, 2e-9)
        check('eigenvector:'+label, mm['equation_residual'], 2e-10)
        check('lapse:'+label, mm['lapse_constraint_residual'], 2e-10)
        for sign in ('xplus', 'xminus'):
            x = z[sign]
            error = abs(x*x+z['B']*x-z['C'])/max(abs(x*x)+abs(z['B']*x)+z['C'],1e-30)
            check(sign+':'+label, error, 2e-10)
    for q in (.001,.1,1.,10.):
        z = poles(0.,0.,3.,q,.5)
        vacuum = .5/(2+3*.5)*9*q*q*(2+q*q)
        check(f'vacuum:q={q}', abs(-z['xminus']/vacuum-1), 2e-12)
        check(f'zero_matter_growth:q={q}', z['growth'], 2e-12)
    z = poles(.4,.23,1e6,1e-6,.5)
    check('intermediate_growth', abs(z['xplus']/(math.sqrt(.23/7)*1e6)-1), 2e-5)
    z = poles(.4,.23,1e6,1e4,.5)
    check('UV_finite_Jeans', abs(z['xplus']/.23-1), 2e-5)

    ks = np.logspace(-5,6,221)
    grids, summaries = [], []
    for a in (.1,.3,1.):
        rows = [row(a,float(k)) for k in ks]
        imax = max(range(len(rows)), key=lambda i: rows[i]['growth_over_H'])
        summaries.append(dict(a=a, maximum_grid_row=rows[imax],
                              neighboring_rows=rows[max(0,imax-1):imax+2],
                              declared_readouts=[row(a,k) for k in (.01,.1,1.)]))
        for rr in rows:
            check(f'grid_eigenvector:a={a}:k={rr["k_Mpc_inverse"]}',
                  rr['growing_mode']['equation_residual'], 2e-10)
        grids.append(dict(a=a, rows=rows))
    result = dict(status='QUALIFIED' if all(c['passed'] for c in controls) else 'FAILED',
                  scope='Frozen local poles only; no time evolution or observational success',
                  assumptions=dict(beta=BETA, ell_Mpc=ELL_MPC, a0_SI=A0,
                                   omega_b=OB,H_vac_km_s_Mpc=HVAC,H_ref_km_s_Mpc=HREF,
                                   radiation='omitted in this late-time diagnostic'),
                  protocol_sha256=hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  controls=controls,summaries=summaries,grids=grids,
                  elapsed_seconds=time.perf_counter()-started)
    with OUTPUT.open('x') as handle:
        json.dump(result,handle,indent=2,allow_nan=False)
        handle.write('\n')
    print(json.dumps(dict(status=result['status'], controls=len(controls),
                          failed=[c for c in controls if not c['passed']],
                          summaries=[dict(a=s['a'],
                              k_peak=s['maximum_grid_row']['k_Mpc_inverse'],
                              growth_over_H=s['maximum_grid_row']['growth_over_H'],
                              inverse_k_kpc=1000*s['maximum_grid_row']['physical_inverse_k_Mpc'],
                              growth_inverse_Gyr=s['maximum_grid_row']['growth_inverse_Gyr'],
                              potential_ratio=s['maximum_grid_row']['growing_mode']['potential_ratio'],
                              delta_spatial_screen=s['maximum_grid_row']['asymptotic_spatial_1percent_Delta_screen'])
                                     for s in summaries],
                          elapsed_seconds=result['elapsed_seconds']),indent=2))


if __name__ == '__main__':
    main()

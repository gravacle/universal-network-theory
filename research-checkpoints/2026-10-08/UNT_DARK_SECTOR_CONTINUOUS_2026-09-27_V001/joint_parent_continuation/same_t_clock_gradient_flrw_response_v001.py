"""NEW same-T effective FLRW basis response; prospective no-fit census.

No old scientific producer is imported. Root alone launches --execute after
full scientific reviews and fresh execution ownership verification.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import math
import os
import time
import numpy as np

BASE = Path(__file__).resolve().parent
STEM = 'SAME_T_CLOCK_GRADIENT_FLRW_RESPONSE_V001'
PROTOCOL_SHA = '61ee3ff72207a8e25d7a9b4eb736e438ccc409d6d897402dafd58a231e214e9a'
PINS = {
    'INVARIANT_CLOCK_JOINT_CALIBRATION_V003_RESULT.json': 'c92eb0ce131a61009361f2ead3f4db7522d3eabb22f7e3d472f0e4e0c116c24f',
    'bounded_clock_shared_prediction_v001.py': 'dd3d22e143e10b977fb7c0d6a2ce0a7cd260e0ddb077e3a9cf56e9e471f0b896',
    'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V001.md': '8359678351bc69f6e58abc6e0355e9b1f7d450138645c8939b944b0769c16e08',
    'GRADIENT_PARENT_LONGITUDINAL_RESPONSE_AND_NORMAL_CONSTRAINT_V001.md': '633d604e5b655d1df096c4bba01c340f25f91460364bf7080df7d1604368560c',
    'LOCAL_RECORD_FEEDBACK_NATIVE_MATERIAL_NORMAL_CURRENT_SOURCE_V001.md': '4ddf27182ec7f24ea60c2a72b24ff3b04ead5929bd30878a1a2c8a97a67b52dd',
    'INVARIANT_CLOCK_GRADIENT_SAME_T_FLRW_INTERFACE_V002.md': '6f25d82ac4b2b6c6c27052d7464dade327b7be527e5c9ee22844c73cce8cf604',
}
AI, SEED = .01, 1e-8
X0 = math.log(AI)
CP_KMS, MPC_M = 299792.458, 3.085677581491367e22
CASES = [(k, om) for k in (.01, .1) for om in (0., .1, 1., 10., 100.)]
TRIALS = [('COARSE', 16384, 48), ('FINE', 32768, 48), ('MODES', 32768, 96)]
FLUID_NAMES = ['Phi', 'delta_b', 'Hunit_v_b', 'delta_rad', 'Hunit_v_rad',
               'Hunit_pi', 'delta_rho_clock_over_rho_star', 'Z', 'Z_prime']


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def write_json(name, obj):
    path = BASE / name
    with path.open('x') as f:
        json.dump(obj, f, sort_keys=True, separators=(',', ':'), allow_nan=False)
        f.write('\n')
    path.chmod(0o444)
    return sha(path)


def journal(event, **kwargs):
    with (BASE / (STEM + '_JOURNAL.jsonl')).open('a') as f:
        f.write(json.dumps(dict(time=now(), event=event, **kwargs), sort_keys=True)+'\n')


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
    pex = (math.log1p(s)-s/(1+s))/norm
    cs = eps*s/(2+(4+3*eps)*s+2*(1+eps)*s*s)
    b, r = 1.5*OB/rG/a**3, 1.5*OR/rG/a**4
    w = 1.5*OA/rG*qbar*d
    rho = 1.5*OA/rG*(1+qbar*d-pex)
    h = math.sqrt((2/3)*(b+r+rho))
    return dict(a=a, h=h, b=b, r=r, w=w, rho=rho, cs=cs, qbar=qbar,
                s=s, charge=d, charge_error=abs(2*qbar*s/(eps*norm)/d-1))


def rates(x, y, fixed, snodes, weights):
    bg = background(x, fixed)
    h, b, r, w, cs = (bg[n] for n in ('h', 'b', 'r', 'w', 'cs'))
    q = np.array([k*CP_KMS/fixed['Hunit']/bg['a'] for k, _ in CASES])[:, None]
    om2 = np.array([om*om for _, om in CASES])[:, None, None]
    ns = len(snodes)
    z, v = y[:, :, 7:7+ns], y[:, :, 7+ns:]
    Z, Zp = z@weights, v@weights
    phi, db, ub, dr, ur, u, E = (y[:, :, i] for i in range(7))
    phip = b*ub+4*r*ur/3+w*u-h*phi
    acc = -cs*(E/w+3*h*u)
    out = np.empty_like(y)
    out[:, :, 0] = phip
    out[:, :, 1] = 3*phip-q*q*ub
    out[:, :, 2] = phi
    out[:, :, 3] = 4*phip-4*q*q*ur/3
    out[:, :, 4] = phi+dr/4+h*ur
    out[:, :, 5] = phi-acc
    out[:, :, 6] = -3*h*(1+cs)*E+3*w*phip-w*q*q*u+q*(Zp+2*h*Z)
    out[:, :, 7:7+ns] = v
    out[:, :, 7+ns:] = (-3*h*v-om2*snodes[None, None, :]**2
                         *((1+(fixed['L']*q)**2)[:, :, None]*z-q[:, :, None]*acc[:, :, None]))
    return out/h


def initial_state(fixed, ns):
    bg = background(X0, fixed)
    y = np.zeros((len(CASES), 2, 7+2*ns))
    B = bg['b']+4*bg['r']/3+bg['w']
    for c, (k, _) in enumerate(CASES):
        q = k*CP_KMS/fixed['Hunit']/AI
        for seed in range(2):
            phi, U = (SEED, 0.) if seed == 0 else (0., SEED/bg['h'])
            ds = -q*q*phi/B-3*bg['h']*U
            y[c, seed, :7] = [phi, ds, U, 4*ds/3, U, U, bg['w']*ds]
    return y


def readouts(x, y, fixed, weights):
    bg = background(x, fixed)
    h, b, r, w, cs = (bg[n] for n in ('h', 'b', 'r', 'w', 'cs'))
    q = np.array([k*CP_KMS/fixed['Hunit']/bg['a'] for k, _ in CASES])[:, None]
    ns = len(weights)
    Z, Zp = y[:, :, 7:7+ns]@weights, y[:, :, 7+ns:]@weights
    phi, db, ub, dr, ur, u, E = (y[:, :, i] for i in range(7))
    mom = b*ub+4*r*ur/3+w*u
    terms = np.stack((q*q*phi, 3*h*mom, b*db, r*dr, E, -q*Z), axis=-1)
    residual = np.sum(terms, axis=-1)
    den = np.maximum(np.sum(np.abs(terms), axis=-1), q*q*SEED*1e-10)
    comov_b = db+3*h*ub
    comov_rad = r*(dr+4*h*ur)
    comov_clock = E+3*h*w*u
    pol = -q*Z
    acc = -q*cs*(E/w+3*h*u)
    fluids = np.concatenate((y[:, :, :7], Z[:, :, None], Zp[:, :, None]), axis=-1)
    physical = np.stack((comov_b, comov_rad, comov_clock, pol, 2*phi, acc), axis=-1)
    amplitudes = np.stack((abs(phi), abs(db), abs(dr), abs(E/w),
                           abs(q*ub), abs(q*ur), abs(q*u), abs(acc)), axis=-1)
    eps, s, qp = fixed['eps'], bg['s'], bg['qbar']
    lower = eps*s/((1+s)*qp*(qp+1))
    upper = eps/((1+s)*qp*(math.sqrt(1+eps)+qp))
    rate_fraction = cs*E/w
    clock_domain = np.stack((rate_fraction, np.full_like(rate_fraction, lower),
                             np.full_like(rate_fraction, upper),
                             abs(rate_fraction)/min(lower, upper)), axis=-1)
    return dict(background=bg, fluids=fluids, physical=physical, normal_terms=terms,
                normal_error=abs(residual)/den, amplitudes=amplitudes, clock_domain=clock_domain)


def trial(label, steps, ns, fixed, lineage):
    xn, wn = np.polynomial.legendre.leggauss(ns)
    snodes, weights = (xn+1)/2, wn*(xn+1)/2
    dx = -X0/steps
    y, n0, snapshots = initial_state(fixed, ns), 0, []
    commits = sorted(BASE.glob(STEM+'_'+label+'_CP_*_COMMIT.json'))
    payloads = set(p.name for p in BASE.glob(STEM+'_'+label+'_CP_*.json')
                   if not p.name.endswith('_COMMIT.json'))
    committed = set(p.name.replace('_COMMIT.json', '.json') for p in commits)
    if payloads != committed:
        raise RuntimeError('Orphan checkpoint preserved for root inspection; no overwrite/rerun')
    if commits:
        events = [json.loads(line) for line in (BASE/(STEM+'_JOURNAL.jsonl')).read_text().splitlines()]
        for cp in commits:
            row = json.loads(cp.read_text())
            entries = [e for e in events if e.get('event') == 'CHECKPOINT'
                       and e.get('trial') == label and e.get('payload') == row['payload']]
            if len(entries) != 1 or entries[0]['commit_sha256'] != sha(cp):
                raise RuntimeError('Checkpoint commit journal authentication failed')
            if entries[0]['sha256'] != row['sha256'] or sha(BASE/row['payload']) != row['sha256']:
                raise RuntimeError('Checkpoint payload journal authentication failed')
        commit = json.loads(commits[-1].read_text())
        if commit['lineage'] != lineage or commit['steps'] != steps or commit['ns'] != ns:
            raise RuntimeError('Checkpoint lineage/census mismatch; preserved without overwrite')
        payload = BASE / commit['payload']
        if sha(payload) != commit['sha256']:
            raise RuntimeError('Checkpoint payload seal mismatch')
        saved = json.loads(payload.read_text())
        if any(saved[k] != commit[k] for k in ('lineage', 'steps', 'ns')):
            raise RuntimeError('Saved checkpoint metadata mismatch')
        y, n0, snapshots = np.array(saved['state']), saved['n'], saved['snapshots']
        if type(n0) is not int or not 0 < n0 <= steps or n0 % 2048:
            raise RuntimeError('Invalid saved step')
        if y.shape != (len(CASES), 2, 7+2*ns) or not np.all(np.isfinite(y)):
            raise RuntimeError('Saved full state schema failure')
        if [s['n'] for s in snapshots] != list(range(0, n0+1, steps//64)):
            raise RuntimeError('Saved ordered snapshot prefix mismatch')
        for s in snapshots:
            if s['x'] != X0+s['n']*dx or np.array(s['state']).shape != y.shape:
                raise RuntimeError('Saved snapshot coordinate/shape mismatch')
            if not np.all(np.isfinite(np.array(s['state']))):
                raise RuntimeError('Saved snapshot nonfinite state')
        if n0 != int(payload.stem.rsplit('_', 1)[-1]) or snapshots[-1]['state'] != saved['state']:
            raise RuntimeError('Saved checkpoint end-state mismatch')
        journal('RESUME', trial=label, n=n0, commit=commits[-1].name)
    if n0 == 0:
        rr = readouts(X0, y, fixed, weights)
        snapshots.append(dict(n=0, x=X0, state=y.tolist(),
                              **{k: v.tolist() if isinstance(v, np.ndarray) else v for k, v in rr.items()}))
    for n in range(n0+1, steps+1):
        x = X0+(n-1)*dx
        k1 = rates(x, y, fixed, snodes, weights)
        k2 = rates(x+dx/2, y+dx*k1/2, fixed, snodes, weights)
        k3 = rates(x+dx/2, y+dx*k2/2, fixed, snodes, weights)
        k4 = rates(x+dx, y+dx*k3, fixed, snodes, weights)
        y += dx*(k1+2*k2+2*k3+k4)/6
        if not np.all(np.isfinite(y)):
            raise FloatingPointError('Nonfinite state at '+label+' step '+str(n))
        if n % (steps//64) == 0:
            xx = X0+n*dx
            rr = readouts(xx, y, fixed, weights)
            snapshots.append(dict(n=n, x=xx, state=y.tolist(),
                                  **{k: v.tolist() if isinstance(v, np.ndarray) else v for k, v in rr.items()}))
        if n % 2048 == 0 or n == steps:
            stem = STEM+'_'+label+'_CP_'+str(n).zfill(6)
            payload = stem+'.json'
            seal = write_json(payload, dict(lineage=lineage, steps=steps, ns=ns, n=n,
                                            state=y.tolist(), snapshots=snapshots))
            commit_sha = write_json(stem+'_COMMIT.json', dict(lineage=lineage, steps=steps, ns=ns,
                                                             payload=payload, sha256=seal))
            journal('CHECKPOINT', trial=label, n=n, payload=payload, sha256=seal, commit_sha256=commit_sha)
            print(json.dumps(dict(trial=label, completed_steps=n, total_steps=steps)), flush=True)
    return dict(label=label, steps=steps, ns=ns, snodes=snodes.tolist(),
                weights=weights.tolist(), snapshots=snapshots)


def main():
    start = time.monotonic()
    pins = dict(PINS, **{STEM+'.md': PROTOCOL_SHA})
    for name, expected in pins.items():
        if sha(BASE/name) != expected:
            raise RuntimeError('Input seal mismatch '+name)
    source_sha = sha(__file__)
    lineage = dict(inputs=pins, source_sha256=source_sha)
    cal = json.loads((BASE/'INVARIANT_CLOCK_JOINT_CALIBRATION_V003_RESULT.json').read_text())
    sel, owned = cal['selected'], cal['fixed']
    context = cal['trials'][-1]['atomic_invocation']['context']
    if context['fixed']['H0_km_s_Mpc'] != sel['Hunit'] or context['fixed']['omega_b_cos'] != sel['OB']:
        raise RuntimeError('Selected radiation inventory mismatch')
    fixed = dict(Hunit=sel['Hunit'], OA=owned['omega_A'], OB=sel['OB'], OR=context['OR'],
                 d0=owned['d0'], eps=owned['eps'], rG=owned['rG'],
                 Q0_over_old_Hunit=owned['Q0_over_H0'], ell_pc=100.,
                 L=100e-6*sel['Hunit']/CP_KMS, seed=SEED, initial_a=AI)
    manifest = dict(lineage=lineage, fixed=fixed, cases=CASES, trials=TRIALS,
                    seeds=['fixed_Phi_zero_velocity', 'zero_Phi_fixed_velocity'],
                    minimal_new_same_T_action=True, extra_native_remainder='absent',
                    radiation='conserved perfect fluid, no anisotropic stress')
    mp = BASE/(STEM+'_MANIFEST.json')
    if mp.exists():
        if json.loads(mp.read_text()) != json.loads(json.dumps(manifest)):
            raise RuntimeError('Existing manifest mismatch')
    else:
        write_json(mp.name, manifest)
    if (BASE/(STEM+'_RESULT.json')).exists():
        raise RuntimeError('Completed result already exists; no duplicate execution')
    journal('OWNER_START', pid=os.getpid(), owner='root', source_sha256=source_sha)
    rows = [trial(*tr, fixed, lineage) for tr in TRIALS]
    gates = []

    def check(name, error, tolerance, **ident):
        gates.append(dict(name=name, error=float(error), tolerance=tolerance,
                          passed=bool(math.isfinite(error) and error <= tolerance), **ident))

    for tr in rows:
        check('spectral_normalization', abs(sum(tr['weights'])-1), 1e-13, trial=tr['label'])
        check('charge_root', max(s['background']['charge_error'] for s in tr['snapshots']),
              1e-13, trial=tr['label'])
        for c, (k, om) in enumerate(CASES):
            for seed in range(2):
                check('normal_constraint', max(s['normal_error'][c][seed] for s in tr['snapshots']),
                      1e-6, trial=tr['label'], case=c, seed=seed)
                if om == 0:
                    check('mode_off_zero', max(abs(v) for s in tr['snapshots']
                          for v in s['state'][c][seed][7:]), 1e-13,
                          trial=tr['label'], case=c, seed=seed)
    fine = np.array([s['fluids'] for s in rows[1]['snapshots']])
    for index, name in [(0, 'time'), (2, 'spectral')]:
        comp = np.array([s['fluids'] for s in rows[index]['snapshots']])
        err = np.max(abs(comp-fine), axis=0)/np.maximum(np.max(abs(fine), axis=0), SEED*1e-8)
        for c, (k, om) in enumerate(CASES):
            for seed in range(2):
                for v, label in enumerate(FLUID_NAMES):
                    check(name+'_refinement', err[c, seed, v], 1e-4, case=c, seed=seed, variable=label)
    for c in (0, 5):
        check('mode_off_spectral_identity', float(np.max(abs(np.array(rows[1]['snapshots'][-1]['state'])[c,:,:7]
                       -np.array(rows[2]['snapshots'][-1]['state'])[c,:,:7])))/SEED, 1e-12, case=c)
    bg1 = background(0., fixed)
    check('fixed_inventory_H_identity', abs(bg1['h']**2*fixed['rG']-
          (fixed['OA']*(1+bg1['qbar']*bg1['charge']-
           (math.log1p(bg1['s'])-bg1['s']/(1+bg1['s']))/(1/fixed['eps']-math.log1p(1/fixed['eps'])))
           +fixed['OB']+fixed['OR'])), 1e-13)
    endpoints, physical_flags, effect_refinements = [], [], []
    for c, (k, om) in enumerate(CASES):
        ref = 0 if c < 5 else 5
        for seed in range(2):
            p = np.array(rows[1]['snapshots'][-1]['physical'])[c, seed]
            pr = np.array(rows[1]['snapshots'][-1]['physical'])[ref, seed]
            endpoints.append(dict(case=c, k_Mpc_inverse=k, omega_over_old_Hunit=om, seed=seed,
                                  physical=p.tolist(), difference_from_mode_off=(p-pr).tolist()))
            paired = []
            for tr in rows:
                phys = np.array(tr['snapshots'][-1]['physical'])
                paired.append(phys[c, seed]-phys[ref, seed])
            time_change, spectrum_change = paired[0]-paired[1], paired[2]-paired[1]
            margin = 3*np.maximum(abs(time_change), abs(spectrum_change))
            effect_refinements.append(dict(case=c, seed=seed,
                coarse_effect=paired[0].tolist(), fine_effect=paired[1].tolist(),
                spectral_effect=paired[2].tolist(), time_change=time_change.tolist(),
                spectral_change=spectrum_change.tolist(), three_change_margin=margin.tolist(),
                resolution=['control_zero' if om == 0 else ('resolved' if abs(v) > m else 'unresolved')
                            for v, m in zip(paired[1], margin)]))
            amp = max(max(s['amplitudes'][c][seed]) for s in rows[1]['snapshots'])
            domain = max(s['clock_domain'][c][seed][3] for s in rows[1]['snapshots'])
            physical_flags.append(dict(case=c, seed=seed, maximum_amplitude=amp,
                                       small_perturbation=bool(amp < .01),
                                       maximum_clock_domain_fraction=domain,
                                       inside_clock_domain=bool(domain < 1),
                                       sampled_maximum_basis_amplitude=(SEED/domain if domain > 0 else None),
                                       scope='sampled at65 stored times, not an all-times certificate'))
    result = dict(manifest=manifest, trials=rows, numerical_gates=gates,
                  all_numerical_gates_passed=all(g['passed'] for g in gates),
                  physical_fixture_flags=physical_flags, endpoints=endpoints,
                  endpoint_effect_refinements=effect_refinements,
                  physical_names=['comoving_delta_b', 'comoving_rad_density', 'comoving_clock_density',
                                  'polarization_density', 'Weyl', 'normal_acceleration'],
                  elapsed_seconds=time.monotonic()-start, status='COMPLETED',
                  scope='NEW minimal effective action basis propagator; no primordial/data/growth fit')
    for name, expected in pins.items():
        if sha(BASE/name) != expected:
            raise RuntimeError('Input changed during worker; unpublished result preserved in checkpoints')
    if sha(__file__) != source_sha:
        raise RuntimeError('Worker source changed; refusing result publication')
    result_sha = write_json(STEM+'_RESULT.json', result)
    lines = ['# Same-T coupled FLRW response V001', '',
             'NEW effective hypothesis; fixed physical inventory, ONE GN, no extra native remainder.',
             'No observational agreement or primordial growing state inferred.', '',
             f'Numerical gates: {sum(g["passed"] for g in gates)}/{len(gates)} PASS.',
             f'Present H / old Hunit: {bg1["h"]:.12g}.', '',
             '| k/Mpc | omega/Hunit | basis | comoving db | db minus mode-off | Weyl |',
             '|---|---|---|---|---|---|']
    for row in endpoints:
        lines.append('| '+f'{row["k_Mpc_inverse"]} | {row["omega_over_old_Hunit"]} | {row["seed"]} | '
                     f'{row["physical"][0]:.12g} | {row["difference_from_mode_off"][0]:.12g} | '
                     f'{row["physical"][4]:.12g}'+' |')
    lines += ['', 'Physical small-perturbation flags are separate from numerical qualification.',
              'Any numerical failures are retained; unqualified forecasts must not be promoted.']
    rp = BASE/(STEM+'_REPORT.md')
    with rp.open('x') as f:
        f.write('\n'.join(lines)+'\n')
    rp.chmod(0o444)
    journal('OWNER_COMPLETE', result_sha256=result_sha, gates=len(gates),
            passed=sum(g['passed'] for g in gates))
    write_json(STEM+'_RECEIPT.json', dict(lineage=lineage, manifest_sha256=sha(mp),
               result_sha256=result_sha, report_sha256=sha(rp),
               journal_sha256=sha(BASE/(STEM+'_JOURNAL.jsonl')), status='COMPLETED'))
    print(json.dumps(dict(status='COMPLETED', passed=sum(g['passed'] for g in gates),
                          total=len(gates), result_sha256=result_sha,
                          elapsed_seconds=result['elapsed_seconds'])), flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--execute', action='store_true')
    if not ap.parse_args().execute:
        raise SystemExit('Refusing numerical work without explicit --execute')
    try:
        main()
    except Exception as exc:
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')
        write_json(STEM+'_FAILED_'+stamp+'.json', dict(error=repr(exc), pid=os.getpid(), time=now()))
        raise

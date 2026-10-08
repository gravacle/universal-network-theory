"""Small coherent-controller diagnostic; stdout only, no scientific file writes."""
import os
import sys
sys.dont_write_bytecode = True
for key in ('OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'OMP_NUM_THREADS',
            'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import resource
import time
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CONFIG = dict(ages=[0., .5, 2.], durations=[.25, .75], g=.4, dv=.3,
              pairs=[[0., 0.], [.8, 0.], [0., .6], [-.8, -.6]],
              tol=1e-10, decoded_tol=1e-8, global_shift=.31)
PARENT_RESULT = '2b9b19954f137aaf0b60173481fdb9059cda3892ee3c71bd9a6884cbb4b6350a'
PARENT_FREEZE = '4d22da45549f2de78fc0477be6b5f23bc0f58b3598a312e2aa76d8f729ac9ff3'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def inputs():
    rp, fp = HERE/'RECORD_ADDITION_RESULTS.json', HERE/'RECORD_ADDITION_FROZEN.json'
    if sha(rp) != PARENT_RESULT or sha(fp) != PARENT_FREEZE:
        raise RuntimeError('Parent identity changed')
    parent, frozen = json.loads(rp.read_text()), json.loads(fp.read_text())
    if parent['status'] != 'COMPLETE' or not all(c['passed'] for c in parent['payload']['checks']):
        raise RuntimeError('Parent did not qualify')
    if parent['freeze_sha256'] != PARENT_FREEZE or parent['payload_sha256'] != hashlib.sha256(encoded(parent['payload'])).hexdigest():
        raise RuntimeError('Parent payload authentication failed')
    files = {}
    for relative, expected in frozen['files'].items():
        p = (ROOT/relative).resolve()
        if not p.is_relative_to(ROOT) or sha(p) != expected:
            raise RuntimeError('Parent source mismatch: '+relative)
        files[relative] = expected
    for p in (rp, fp, Path(__file__).resolve(), HERE/'COHERENT_SOURCE_VOLUME_PROTOCOL_V001.md'):
        files[str(p.relative_to(ROOT))] = sha(p)
    return parent, dict(config=CONFIG, files=files)


def spectral(h, t):
    e, v = np.linalg.eigh(h)
    return (v*np.exp(-1j*t*e)) @ v.conj().T


def taylor(h, t):
    a = -1j*t*h
    n = float(np.linalg.norm(a, ord=np.inf))
    s = max(0, math.ceil(math.log2(n/.5))) if n else 0
    a /= 2**s
    n = float(np.linalg.norm(a, ord=np.inf))
    u = np.eye(len(h), dtype=complex)
    term, mag = u.copy(), 1.
    for k in range(1, 201):
        term = term @ a / k
        u += term
        mag *= n/k
        tail = math.exp(n)*mag*n/(k+1)
        if tail <= 1e-18:
            break
    else:
        raise ArithmeticError('Taylor criterion failed')
    for _ in range(s):
        u = u @ u
    return u


def reductions(state):
    arms = state.reshape(4, 16)
    # rho_controller[a,b]=<psi_b|psi_a>/4; rho_native=sum_a |arm_a><arm_a|.
    return arms @ arms.conj().T, arms.T @ arms.conj()


def run():
    started = time.perf_counter()
    parent, snapshot = inputs()
    freeze = HERE/'COHERENT_SOURCE_VOLUME_V002_FROZEN.json'
    if json.loads(freeze.read_text()) != snapshot:
        raise RuntimeError('Prospective freeze differs')
    spec = importlib.util.spec_from_file_location('native_controller_parent', HERE/'record_addition_compute.py')
    native = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(native)
    op = native.operators()
    ident = np.eye(16)
    records = op['QL']+op['QR']
    names = [x['name'] for x in parent['payload']['cases']]
    if names != ['native', 'feedback_off', 'copying_off']:
        raise RuntimeError('Parent census changed')
    maxima, counts, failures, cases = {}, {}, [], []

    def check(metric, a, b=0., tol=None, case=''):
        tolerance = CONFIG['tol'] if tol is None else tol
        err = float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
        maxima[metric] = max(maxima.get(metric, 0.), err)
        counts[metric] = counts.get(metric, 0)+1
        if not math.isfinite(err) or err > tolerance:
            failures.append(dict(metric=metric, case=case, error=err, tolerance=tolerance))
        return err

    for saved in parent['payload']['cases']:
        params = saved['parameters']
        psi0 = np.asarray(saved['formed_vector']['real'])+1j*np.asarray(saved['formed_vector']['imag'])
        h, _ = native.hamiltonian(dict(params, g=0.), op)
        compact = 3*ident+records-op['Xa']+(2.25*ident-params['lambda_R']*records-.5*op['XC']) @ op['n']
        check('native_compact_H', h, compact)
        for age in CONFIG['ages']:
            psi = spectral(h, age) @ psi0
            for duration in CONFIG['durations']:
                gs = [0., 0., CONFIG['g'], CONFIG['g']]
                vs = [0., CONFIG['dv'], 0., CONFIG['dv']]
                base_states = np.array([spectral(h-g*op['n'], duration) @ psi for g in gs])
                base_c, base_n = reductions((base_states/2).reshape(-1))
                baseline = 4*base_c[2, 0]
                check('contrast_lower_bound', max(0., 1.-abs(CONFIG['g'])*duration-abs(baseline)))
                for c, alpha in CONFIG['pairs']:
                    tag = f"{saved['name']}:age{age}:t{duration}:c{c}:alpha{alpha}"
                    shifts = np.array([.5*c*g*g+alpha*v for g, v in zip(gs, vs)])
                    ht = np.zeros((64, 64), dtype=complex)
                    for a, g in enumerate(gs):
                        ht[a*16:(a+1)*16, a*16:(a+1)*16] = h-g*op['n']+shifts[a]*ident
                    initial = np.tile(psi/2, 4)
                    ut = taylor(ht, duration)
                    final = ut @ initial
                    block_final = (np.exp(-1j*duration*shifts)[:, None]*base_states/2).reshape(-1)
                    cross = check('full_taylor_vs_block_eigh', final, block_final, case=tag)
                    check('unitarity', ut.conj().T @ ut, np.eye(64), case=tag)
                    check('normalization', np.vdot(final, final), 1., case=tag)
                    check('total_energy', np.vdot(final, ht @ final), np.vdot(initial, ht @ initial), case=tag)
                    rc, rn = reductions(final)
                    native_err = check('native_reduced_identity', rn, base_n, case=tag)
                    expected_rc = base_c*np.exp(-1j*duration*(shifts[:, None]-shifts[None, :]))
                    check('controller_phase_identity', rc, expected_rc, case=tag)
                    for a in range(4):
                        check('conditional_native_identity', 4*np.outer(final[a*16:(a+1)*16], final[a*16:(a+1)*16].conj()),
                              np.outer(base_states[a], base_states[a].conj()), case=tag)
                    check('record_clock_identity', np.trace(rn @ (op['AL']+op['AR'])), np.trace(base_n @ (op['AL']+op['AR'])), case=tag)
                    ratio = (4*rc[2, 0])/baseline
                    volume_contrast = 4*rc[1, 0]
                    c_hat = -2*np.angle(ratio)/(CONFIG['g']**2*duration)
                    alpha_hat = -np.angle(volume_contrast)/(CONFIG['dv']*duration)
                    check('decoded_c', c_hat, c, CONFIG['decoded_tol'], tag)
                    check('decoded_alpha', alpha_hat, alpha, CONFIG['decoded_tol'], tag)
                    check('volume_two_source_agreement', volume_contrast, 4*rc[3, 2], case=tag)
                    # Direct propagation of the initial controller-dephased density matrix.
                    rho_in = np.zeros((64, 64), complex)
                    for a in range(4):
                        rho_in[a*16:(a+1)*16, a*16:(a+1)*16] = np.outer(psi, psi.conj())/4
                    rho_final = ut @ rho_in @ ut.conj().T
                    dephased_c = np.trace(rho_final.reshape(4, 16, 4, 16), axis1=1, axis2=3)
                    check('dephased_controller_null', dephased_c, np.eye(4)/4, case=tag)
                    # A global energy shift remains invisible in the full density matrix.
                    shifted = taylor(ht+CONFIG['global_shift']*np.eye(64), duration) @ initial
                    check('global_identity_gauge', np.outer(shifted, shifted.conj()), np.outer(final, final.conj()), case=tag)
                    check('phase_alias_margin', max(0., abs(.5*c*CONFIG['g']**2*duration)-math.pi,
                                                     abs(alpha*CONFIG['dv']*duration)-math.pi), case=tag)
                    cases.append(dict(preparation=saved['name'], age=age, duration=duration, c=c, alpha=alpha,
                                      source_reference_visibility=float(abs(baseline)), volume_visibility=float(abs(volume_contrast)),
                                      source_phase=float(np.angle(ratio)), volume_phase=float(np.angle(volume_contrast)),
                                      c_decoded=float(c_hat), alpha_decoded=float(alpha_hat),
                                      native_density_max_error=native_err, propagation_max_error=cross))
    check('case_count', len(cases), 72, 0.)
    payload = dict(scope='Adopted coherent-controller discrimination only; no physical coefficient selection or volume derivation.',
                   config=CONFIG, cases=cases, check_counts=counts, maximum_errors=maxima, failures=failures)
    result = dict(status='COMPLETE' if not failures else 'FAILED', payload=payload,
                  payload_sha256=hashlib.sha256(encoded(payload)).hexdigest(), freeze_sha256=sha(freeze),
                  seconds=time.perf_counter()-started, peak_self_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    print(json.dumps(result, allow_nan=False))
    return 1 if failures else 0


if __name__ == '__main__':
    if sys.argv[1:] == ['freeze']:
        print(json.dumps(inputs()[1], indent=2))
    elif sys.argv[1:]:
        raise SystemExit('Use freeze or no arguments')
    else:
        raise SystemExit(run())

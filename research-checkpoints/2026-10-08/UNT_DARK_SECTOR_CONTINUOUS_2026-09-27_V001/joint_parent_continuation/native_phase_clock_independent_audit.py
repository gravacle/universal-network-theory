"""Post-result original-matrix / Taylor audit, with no new preparation."""
import os
import sys
sys.dont_write_bytecode = True
for _key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
             'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[_key] = '1'
import hashlib
import json
import math
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent.parent
OUTPUT = ROOT / 'NATIVE_PHASE_CLOCK_INDEPENDENT_REVIEW_DATA.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encode(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def cx(x):
    return x['real'] + 1j*x['imag']


def main():
    assert not OUTPUT.exists()
    authenticated = {}

    def load(result_name, freeze_name):
        rp, fp = ROOT/result_name, ROOT/freeze_name
        result, frozen = json.loads(rp.read_text()), json.loads(fp.read_text())
        assert result['status'] == 'COMPLETE'
        assert result['freeze_sha256'] == sha(fp)
        assert result['payload_sha256'] == hashlib.sha256(encode(result['payload'])).hexdigest()
        assert all(x['passed'] for x in result['payload']['checks'])
        for rel, digest in frozen['files'].items():
            path = WORKSPACE/rel
            assert sha(path) == digest, rel
            authenticated[str(path)] = digest
        authenticated[str(rp)] = sha(rp); authenticated[str(fp)] = sha(fp)
        return result

    result = load('native_phase_clock_v001_results.json', 'native_phase_clock_v001_frozen.json')
    old = load('RECORD_ADDITION_RESULTS.json', 'RECORD_ADDITION_FROZEN.json')
    pulse = load('native_writer_pulse_results.json', 'native_writer_pulse_frozen.json')
    expected_names = ['native', 'feedback_off', 'copying_off']
    assert [x['name'] for x in result['payload']['cases']] == expected_names
    assert len(result['payload']['checks']) == 518
    ident = np.eye(16, dtype=complex)
    tiny = np.eye(2, dtype=complex)
    n2 = np.diag([0., 1.]); x2 = np.array([[0., 1.], [1., 0.]])
    raising = np.array([[0., 0.], [1., 0.]])
    def at(a, factor):
        z = np.ones((1, 1), complex)
        for i in range(4):
            z = np.kron(z, a if i == factor else tiny)
        return z
    ql, qr, n, xl, xc = at(n2, 0), at(n2, 1), at(n2, 2), at(x2, 2), at(x2, 3)
    raising_op = at(raising, 0) + at(raising, 1)
    count = ql + qr
    records = []
    errors = []
    def check(label, a, b=0., tolerance=1e-11):
        value = float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
        assert math.isfinite(value) and value <= tolerance, (label, value)
        errors.append({'name': label, 'residual': value})
    for case, initial, old_pulse in zip(result['payload']['cases'], old['payload']['cases'], pulse['payload']['cases']):
        assert case['name'] == initial['name'] == old_pulse['name']
        label = case['name']; lam = case['parameters']['lambda_R']
        psi = np.asarray(initial['formed_vector']['real']) + 1j*np.asarray(initial['formed_vector']['imag'])
        h = 3*ident + count - xl + (2.25*ident-lam*count-.5*xc) @ n
        check(label+':count_commutes', h @ count - count @ h)
        comm = h @ raising_op - raising_op @ h
        adot = 1j*comm
        addot = -(h @ comm - comm @ h)
        check(label+':source_identity', comm, (ident-lam*n) @ raising_op)
        energies, vectors = np.linalg.eigh(h)
        sectors = {}
        for rr in (0, 1, 2):
            pr = ((ident-ql) @ (ident-qr) if rr == 0 else
                  ql @ qr if rr == 2 else ql @ (ident-qr)+(ident-ql) @ qr)
            for s in (-1, 1):
                ps = (ident+s*xc)/2
                for beta in (-1, 1):
                    x = 2.25-lam*rr-.5*s
                    e = 3+rr+(x+beta*math.sqrt(x*x+4))/2
                    # Aggregate the entire possibly degenerate numerical energy eigenspace,
                    # then enforce the two exact commuting labels (no eigenvector selection).
                    v = vectors[:, abs(energies-e) < 1e-10]
                    proj = pr @ ps @ (v @ v.conj().T) @ ps @ pr
                    sectors[(rr, s, beta)] = proj
                    check(label+':numerical_sector_rank', np.trace(proj), [1, 2, 1][rr])
        lines = case['spectral_lines']
        assert len(lines) == 16
        omega = np.asarray([r['omega'] for r in lines])
        c = np.asarray([cx(r['coefficient']) for r in lines])
        nc = np.asarray([cx(r['n_coefficient']) for r in lines])
        for row, coeff, ncoeff in zip(lines, c, nc):
            pi = sectors[(row['R'], row['s'], row['beta'])]
            pf = sectors[(row['R']+1, row['s'], row['gamma'])]
            check(label+':independent_coefficient', np.vdot(psi, pf @ raising_op @ pi @ psi), coeff)
            check(label+':independent_n_coefficient', np.vdot(psi, pf @ n @ raising_op @ pi @ psi), ncoeff)
        moments = np.array([sum(abs(c)*abs(omega)**k) for k in range(3)])
        check(label+':moments', moments, case['moments_M0_M1_M2'])
        age_values = []
        for row, prior in zip(case['ages'], old_pulse['ages']):
            t = row['age']
            assert t == prior['age']
            # Independent fixed-degree centered-H scaled Taylor, no imported propagator.
            centered = h - np.trace(h).real/16*ident
            arg = -1j*t*centered
            squarings = max(0, math.ceil(math.log2(max(1., np.linalg.norm(arg, ord=np.inf)/.25))))
            arg /= 2**squarings
            u = ident.copy(); term = ident.copy()
            for order in range(1, 41):
                term = term @ arg/order
                u += term
            for _ in range(squarings):
                u = u @ u
            state = u @ psi
            check(label+':taylor_unitarity', u.conj().T @ u, ident)
            a = np.vdot(state, raising_op @ state)
            a1 = np.vdot(state, adot @ state)
            a2 = np.vdot(state, addot @ state)
            z = np.vdot(state, n @ raising_op @ state)
            check(label+':age_A', a, cx(row['A']))
            check(label+':age_Adot', a1, cx(row['Adot']))
            check(label+':age_nA', z, cx(row['nA']))
            check(label+':saved_K', 2*a.real, prior['initial_K'])
            check(label+':saved_Y', 2*a.imag, prior['initial_Ysum'])
            check(label+':second_derivative_spectral', a2, np.sum(-omega*omega*c*np.exp(1j*omega*t)))
            numerator = float((a.conjugate()*a1).imag)
            rate = numerator/abs(a)**2 if label != 'copying_off' else None
            if rate is not None:
                check(label+':age_phase_rate', rate, row['phase_rate'])
            else:
                check(label+':blank_amplitude', a)
                assert row['phase_rate'] is None
            age_values.append({'age': t, 'amplitude': float(abs(a)), 'phase_rate': rate})
        computed_bounds = []
        for bound in case['continuous_bounds']:
            intervals = bound['intervals']; assert intervals in (512, 1024)
            grid = np.arange(intervals+1) * (2/intervals)
            phase = np.exp(1j*grid[:, None]*omega)
            aa, av = phase @ c, phase @ (1j*omega*c)
            az = phase @ (-omega*omega*c)
            amp = abs(aa); numerator = (aa.conj()*av).imag
            allowance = result['payload']['numerical_allowance']
            lo_a = float(min(amp)-moments[1]/intervals-allowance)
            lo_n = float(min(numerator)-moments[0]*moments[2]/intervals-allowance)
            hi_n = float(max(numerator)+moments[0]*moments[2]/intervals+allowance)
            check(label+':amplitude_bound', lo_a, bound['amplitude_lower_bound'])
            check(label+':numerator_lower_bound', lo_n, bound['numerator_lower_bound'])
            check(label+':numerator_upper_bound', hi_n, bound['numerator_upper_bound'])
            assert np.max(abs((aa.conj()*az).imag)) <= moments[0]*moments[2]+1e-12
            decision = ('undefined_exact_blank' if label == 'copying_off' else
                        'positive_whole_window' if lo_a > 0 and lo_n > 0 else
                        'negative_whole_window' if lo_a > 0 and hi_n < 0 else 'inconclusive')
            assert bound['orientation'] == decision
            computed_bounds.append({'intervals': intervals, 'orientation': decision,
                'amplitude_lower_bound': lo_a, 'numerator_lower_bound': lo_n,
                'numerator_upper_bound': hi_n})
        records.append({'name': label, 'ages': age_values, 'bounds': computed_bounds})
    output = {'status': 'INDEPENDENT_CHECKS_PASS', 'scope': 'Saved-state native phase-window audit; no new preparation or spacetime calibration.',
        'script_sha256': sha(Path(__file__)), 'input_sha256': authenticated,
        'independent_check_count': len(errors), 'max_absolute_residual': max(x['residual'] for x in errors),
        'cases': records, 'checks': errors}
    with OUTPUT.open('x') as stream:
        json.dump(output, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write('\n')
    print(json.dumps({k:v for k,v in output.items() if k not in ('input_sha256','checks','cases')}, indent=2))


if __name__ == '__main__':
    main()

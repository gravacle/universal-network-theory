"""Saved-matrix fast-inertia matching; stdlib only, stdout, no ODE or fits."""
from pathlib import Path
import hashlib
import json
import math

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CASE = HERE / 'COSMOLOGICAL_CLOCK_EVOLUTION_V001_CASE_00.json'
CASE_SHA = '526fb8bb4b0cc00e220bb800f361fa86e6f87bfbecaf458b5dd236031bd7443d'
FREEZE = HERE / 'COSMOLOGICAL_CLOCK_EVOLUTION_V001_FROZEN.json'
HISTORY = HERE / 'COMMON_HISTORY_MECHANISM_V001_RESULTS.json'


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    assert sha(CASE) == CASE_SHA
    wrapper = json.loads(CASE.read_text())
    p = wrapper['payload']
    frozen = json.loads(FREEZE.read_text())
    assert sha(FREEZE) == wrapper['freeze_sha256']
    assert hashlib.sha256(encode(p)).hexdigest() == wrapper['payload_sha256']
    assert p['status'] == 'COMPLETE' and not p['checks']['failures']
    assert p['selected_case'] == 0 and len(p['rows']) == 1
    assert p['configuration'] == frozen['configuration']
    for name, expected in frozen['files'].items():
        path = (ROOT / name).resolve()
        path.relative_to(ROOT.resolve())
        assert sha(path) == expected, name
    history = json.loads(HISTORY.read_text())['payload']
    spectra = {}
    for case in history['cases']:
        key = case['gap'], case['order']
        data = dict(delta=case['delta'], weights=case['weights'])
        if key in spectra:
            assert data == spectra[key]
        spectra[key] = data
    assert set(spectra) == {(.001, 64), (.001, 128), (.002, 64), (.002, 128)}
    beta = p['configuration']['beta']
    slow = p['slow_reference']['rows']
    ref = p['reference']
    ai = p['configuration']['a_start']
    Hi = math.sqrt((ref['Omega_b'] + ref['Omega_exc']) / ai**3 + ref['Omega_Lambda'])
    rows = []
    for (cutoff, order), spectrum in sorted(spectra.items()):
        identity = hashlib.sha256(encode(spectrum)).hexdigest()
        assert identity == frozen['spectrum_identities'][f'{cutoff}:{order}']
        kb = math.fsum(spectrum['weights']) + beta
        f = beta / kb
        matched = []
        for row in slow:
            s = row['state']
            assert len(s) == 2 and all(len(v) == 2 for v in s)
            result = [[s[i][0] + (f-1)*s[i][1], f*s[i][1]] for i in range(2)]
            assert all(math.isfinite(v) for pair in result for v in pair)
            matched.append(dict(a=row['a'], state=result))
        assert matched[0]['state'] == [[1., 0.], [f-1, f]]
        peaks = [max(matched, key=lambda row: abs(row['state'][0][c])) for c in range(2)]
        gamma = math.sqrt(1.5*kb*ref['Omega_exc']/(beta*ai**3))
        rows.append(dict(cutoff=cutoff, order=order, spectrum_sha256=identity,
            Kb=kb, f=f, matching_matrix=[[1., 0.], [f-1, f]],
            matched_slow_rows=matched, endpoint=matched[-1],
            sampled_peak=[dict(a=peaks[c]['a'], absolute_tilt=abs(peaks[c]['state'][0][c])) for c in range(2)],
            initial_rate_screens=dict(H_over_H0=Hi, gravitational_rate_over_H0=gamma,
                cutoff_over_H=cutoff/Hi, cutoff_over_gravitational_rate=cutoff/gamma,
                minimum_quadrature_node_over_H=min(spectrum['delta'])/Hi,
                scope='Rate screens only, not finite-eta error bounds; true cutoff distinct from minimum quadrature node')))
    result = dict(status='SAVED_MATRIX_ARITHMETIC_COMPLETE',
        scope='Leading fixed-positive-cutoff eta-to-zero matching, not a new ODE, preparation, fit or claim that existing eta values are in this regime',
        script_sha256=sha(Path(__file__)),
        input_sha256={CASE.name:sha(CASE), FREEZE.name:sha(FREEZE), HISTORY.name:sha(HISTORY)},
        authenticated_frozen_member_count=len(frozen['files']),
        reference=ref, slow_reference_rows=slow,
        clock_controls_years=[dict(eta=eta, tau_star_Julian_years=eta/ref['H0_s_inverse']/31557600.) for eta in p['configuration']['etas']],
        spectrum_count=len(rows), sample_count_per_spectrum=len(slow), rows=rows)
    print(encode(dict(payload_sha256=hashlib.sha256(encode(result)).hexdigest(), payload=result)).decode())


if __name__ == '__main__':
    main()

"""Small authenticated background-budget arithmetic; no fit or cosmological evolution.

All nine inherited reference cases and both BBN nuclear-rate determinations are
retained. Radiation and curvature are zero ONLY for this late-time illustrative
flat branch. The reference vacuum was previously calibrated using a model-dependent
Pantheon+ result; this is a closure diagnostic, not independent validation.
"""
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent / 'joint_parent_dynamics'
FROZEN = PARENT / 'SHAPE_REFERENCE_FROZEN.json'
REFERENCE = PARENT / 'SHAPE_REFERENCE_RESULTS.json'
OUTPUT = ROOT / 'COSMOLOGY_CLOSURE_ARITHMETIC.json'
MPC_KM = 3.085677581491367e19
GYR_S = 365.25 * 86400 * 1e9
C_M_S = 299792458.
BBN = (
    {'name': 'Cooke2018_Marcucci_rate_eq12', 'omega_b': .02166,
     'measurement_error': .00015, 'nuclear_error': .00011},
    {'name': 'Cooke2018_empirical_rate_eq14', 'omega_b': .02235,
     'measurement_error': .00016, 'nuclear_error': .00033},
)
Z = (0., .5, 1., 2.)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def main():
    assert not OUTPUT.exists(), 'Preserve the earlier result.'
    inputs, seen = {}, set()

    def authenticate(path):
        path = path.resolve()
        if path in seen:
            return
        seen.add(path)
        inputs[str(path.relative_to(ROOT.parent))] = sha(path)
        data = json.loads(path.read_text())
        for name, digest in data['files'].items():
            child = path.parent / name
            assert sha(child) == digest, child
            inputs[str(child.resolve().relative_to(ROOT.parent))] = digest
            if child.name.endswith('_FROZEN.json'):
                authenticate(child)

    authenticate(FROZEN)
    reference = json.loads(REFERENCE.read_text())
    assert reference['freeze_sha256'] == sha(FROZEN)
    assert reference['payload_sha256'] == hashlib.sha256(encoded(reference['payload'])).hexdigest()
    inputs[str(REFERENCE.relative_to(ROOT.parent))] = sha(REFERENCE)
    cases = reference['payload']['cases']
    assert len(cases) == 9
    rows = []
    for i, case in enumerate(cases):
        h0 = case['input']['H0_km_s_Mpc']
        ol = case['input']['Omega_Lambda_ref']
        lv = h0*h0*ol
        hv = case['H_vac_reference_s_inverse'] * MPC_KM
        assert abs(hv*hv/lv-1) < 1e-13
        for baryon in BBN:
            b = 10000*baryon['omega_b']
            hzero = math.sqrt(lv+b)
            closure = h0*h0-lv-b
            history = []
            for z in Z:
                x = 1+z
                hz2 = lv+b*x**3
                href2 = lv+(h0*h0-lv)*x**3
                hk2 = hz2+closure*x**2
                assert abs((href2-hz2)-closure*x**3) < 1e-10*max(1., href2)
                assert abs((href2-hk2)-closure*x*x*z) < 1e-10*max(1., href2)
                history.append({'z': z, 'zero_excitation_flat_H_kmsMpc': math.sqrt(hz2),
                    'inherited_flat_reference_H_kmsMpc': math.sqrt(href2),
                    'curvature_closed_at_z0_H_kmsMpc': math.sqrt(hk2),
                    'invariant_B_kmsMpc_squared': (hz2-lv)/x**3})
            age = 2/(3*math.sqrt(lv))*math.asinh(math.sqrt(lv/b))*MPC_KM/GYR_S
            rows.append({'reference_case': i, 'reference_input': case['input'],
                'reference_r': case['r'], 'bbn': baryon,
                'Hvac_kmsMpc': hv, 'vacuum_coefficient_kmsMpc_squared': lv,
                'baryon_coefficient_kmsMpc_squared': b,
                'zero_excitation_flat_H0_kmsMpc': hzero,
                'zero_excitation_flat_Omega_b0': b/(lv+b),
                'zero_excitation_flat_Omega_vac0': lv/(lv+b),
                'zero_excitation_flat_q0': (.5*b-lv)/(lv+b),
                'zero_excitation_flat_transition_z': (2*lv/b)**(1/3)-1,
                'ideal_dust_vacuum_age_Gyr': age,
                'reference_H0_missing_coefficient_kmsMpc_squared': closure,
                'reference_H0_missing_omega': closure/10000,
                'reference_H0_missing_Omega': closure/(h0*h0),
                'missing_coefficient_over_baryon': closure/b,
                'H_history': history})
    result = {'status': 'AUTHENTICATED_REFERENCE_CLOSURE_DIAGNOSTIC',
        'script_sha256': sha(Path(__file__)), 'input_sha256': inputs,
        'external_primary': {
            'BBN': 'https://arxiv.org/pdf/1710.11129; equations12 and14',
            'inherited_reference': 'https://arxiv.org/html/2202.04077v2; Table3 flat-Lambda-CDM'},
        'scope': 'No new fit; vacuum already cosmologically calibrated; standard-BBN benchmark conditional.',
        'assumptions': 'Late-time flat zero-excitation baryon+dust/vacuum diagnostic; radiation omitted here only.',
        'rows': rows}
    with OUTPUT.open('x') as stream:
        json.dump(result, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write('\n')
    print(json.dumps({'rows': len(rows), 'central_cases': rows[:2]}, indent=2))


if __name__ == '__main__':
    main()

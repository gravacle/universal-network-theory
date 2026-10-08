"""Dimension-only photon comparison of all saved radiation mappings; no fit."""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'SAME_ACTION_RADIATION_V001_RESULTS.json'
NOTE = HERE / 'RADIATION_PHOTON_REFERENCE_V001.md'

def encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()

def main():
    expected, = sys.argv[1:]
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == expected
    saved = json.loads(raw)
    assert saved['status'] == 'COMPLETE'
    p = saved['payload']
    assert saved['payload_sha256'] == hashlib.sha256(encode(p)).hexdigest()
    assert not p['failures']
    constants = dict(T_K=2.72548, sigma_T_K=.00057, G_SI=6.67430e-11,
        sigma_G_SI=.00015e-11, k_B_J_K=1.380649e-23,
        h_P_J_s=6.62607015e-34, c_m_s=299792458.)
    T, G, k, h, c = (constants[v] for v in
        ('T_K', 'G_SI', 'k_B_J_K', 'h_P_J_s', 'c_m_s'))
    energy = 8*math.pi**5*k**4*T**4/(15*h**3*c**3)
    hbar = h/(2*math.pi)
    other = math.pi**2*(k*T)**4/(15*hbar**3*c**3)
    assert abs(energy/other-1) < 2e-12
    refs = {}
    for r in p['references']:
        H = r['H0_s_inverse']
        omega = 8*math.pi*G*energy/(3*H*H*c*c)
        direct = (energy/(c*c))/(3*H*H/(8*math.pi*G))
        assert abs(omega/direct-1) < 2e-12
        refs[r['reference']] = dict(reference=r['reference'], H0_s_inverse=H,
            Omega_gamma=omega, inherited_reference=r)
    rows = []
    for r in p['original_calibration_mappings'] + p['conditional_extended_mappings']:
        omega = refs[r['reference']]['Omega_gamma']
        index = r['inverse_scale_factors'].index(1101.)
        finite = r['finite_A_Omega_coefficient'][index]
        upper = r['finite_A_upper_errors'][index]
        asympt = r['Omega_extra_rad_asympt']
        assert asympt is not None
        assert r['inverse_scale_factors'] == [1., 2., 4., 11., 101., 1101.]
        for value, error in zip(r['finite_A_Omega_coefficient'], r['finite_A_upper_errors']):
            assert asympt <= value*(1+2e-8)
            assert value <= (asympt+error)*(1+2e-8)
        rows.append(dict(template_index=r['template_index'], reference=r['reference'],
            status=r['status'], asymptote_over_photons=asympt/omega,
            inverse_scale_factors=r['inverse_scale_factors'],
            finite_A_over_photons=[v/omega for v in r['finite_A_Omega_coefficient']],
            finite_A_asymptote_upper_error_over_photons=[v/omega for v in r['finite_A_upper_errors']],
            at_A1101_over_photons=finite/omega, asymptote_upper_error_A1101_over_photons=upper/omega))
    assert len(rows) == 756 and len(refs) == 18
    result = dict(status='COMPLETE', constants=constants, photon_energy_J_m3=energy,
        photon_mass_kg_m3=energy/c**2,
        independent_T_G_linearized_relative_uncertainty=math.hypot(
            4*constants['sigma_T_K']/T, constants['sigma_G_SI']/G),
        input_sha256=expected, input_payload_sha256=saved['payload_sha256'],
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        note_sha256=hashlib.sha256(NOTE.read_bytes()).hexdigest(),
        references=list(refs.values()), rows=rows,
        scope='Conditional density-scale comparison only; no neutrinos, N_eff likelihood, photon creation or CMB fit; physical action/redshift/clock domain and inherited calibration assumptions remain.')
    print(encode(result).decode())

if __name__ == '__main__':
    main()

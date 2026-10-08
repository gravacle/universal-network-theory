#!/usr/bin/env python3
"""Guarded present band-intensity adapter; no physical field/source producer."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, math, os, sys, traceback
AUTHOR_DRAFT = True
J = Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation')
SOURCE = 'cross_u_ngc3198_observed_photon_band_adapter_v001.py'
STEM = 'CROSS_U_NGC3198_OBSERVED_PHOTON_BAND_ADAPTER_V001'
PROTOCOL = STEM + '.md'
PROTOCOL_SHA = 'cd710599c7ea94fef19f28be882ea3a89ad74e16d99a4e2137c9d048e3ddc7fa'
PINS = {'CROSS_U_NGC3198_OBSERVED_PHOTON_BAND_ADAPTER_V001_CALIBRATION.json': '65a9fd28878ab1d17802b2091a975d856f0d2e40ab0eeffbd3c97ba86f6bb686', 'CROSS_U_NGC3198_OBSERVED_ACTIVITY_ADAPTER_V001_CATALOGUE.json': '5a1f0e186767aea83524945b74d01a112e72b7f48f85bc3fc947f4a323ee86ac', 'CROSS_U_NGC3198_OBSERVED_ACTIVITY_ADAPTER_V001_RESULT.json': '21ba529a4e06ba2a5b6ec778ac70811750d75d5d948c534c9d0fec79bcb32a23', 'CROSS_U_NGC3198_OBSERVED_ACTIVITY_ADAPTER_V001_RECEIPT.json': '3dd3b20c9dfa3a42993742a53d5e956e804d39f7a3f8d4740f1207942ae54961', 'leroy2008_table4.dat': '938104d0289f93f9fed0843028555e92f63a61889d623ee5b5f132e9d6ea1f44', 'leroy2008_table7.dat': '43165045c50d534ff7789dda05627328c23ba71c708ded9cf87cf0773fe02d99', 'leroy2008_ReadMe.html': 'cbd9a431c5ef4d9ae1bcda8bc141210bd03360a4d2b0ea5d8dd40e9079763c48', 'NATIVE_INCIDENCE_MAXWELL_PAIR_SOURCE_V002.md': '7e5cf9d3651de4471b52c9a3769f23cdd5457726c8354ff42ecee3c2a4034c7b', 'reviewed_photon_band_adapter_140_a69ea630.py': 'a69ea6305c3c98b648652688b6c63d99748b4e9e106c329451cee957702932ee', 'REVIEWED_PHOTON_BAND_ADAPTER_15_34621ae9.md': '34621ae978ddbb4903029b90901fe39a6f67161662c0577eb639faf0171a9047', 'reviewed_photon_band_calibration_404dba7f.json': '404dba7f855a296e5e9f5344c3db366c3bddcd93b3a1384608e2c77c78aee78e'}
FLAGS = {k: False for k in ('native_writer_source_registered', 'radiation_energy_source_registered',
    'source_history_registered', 'three_dimensional_source_registered', 'Hilbert_stress_qualified',
    'full_metric_qualified', 'velocity_prediction_qualified', 'observational_success_qualified')}
CREATED, ROWS, CHECKS = {}, [], []
EPS = sys.float_info.epsilon

class PhysicalSourceUnavailable(RuntimeError):
    pass

def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1048576), b''): h.update(b)
    return h.hexdigest()

def read(name):
    return json.loads((J / name).read_text())

def publish(suffix, obj):
    p = J / (STEM + '_' + suffix + '.json')
    data = (json.dumps(obj, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()
    with p.open('xb') as f: f.write(data); f.flush(); os.fsync(f.fileno())
    if p.read_bytes() != data: raise RuntimeError('Exact publication reread: ' + p.name)
    p.chmod(0o444); CREATED[p.name] = sha(p)
    return CREATED[p.name]

def actual_outputs():
    out = {}
    for p in sorted(J.glob(STEM + '_*.json')):
        if p.name == STEM + '_CALIBRATION.json': continue
        if not p.is_file(): raise RuntimeError('Unexpected output: ' + p.name)
        p.chmod(0o444); out[p.name] = sha(p)
    return out

def verify(source_hash):
    for name, expected in {**PINS, PROTOCOL: PROTOCOL_SHA, SOURCE: source_hash}.items():
        if sha(J / name) != expected: raise RuntimeError('Byte mismatch: ' + name)

def check(name, passed, raw):
    CHECKS.append(dict(name=name, passed=bool(passed), raw=raw))
    if not passed: raise ArithmeticError('Arithmetic/input refusal: ' + name)

def relative(a, b):
    return abs(a - b) / max(abs(a), abs(b), 1e-30)

def physical_source_gate():
    raise PhysicalSourceUnavailable('Band intensity does not register F^2/joint native-field correlations, '
        'operator/material/support/clock/units/history or conserved full Hilbert source. No velocity is produced.')

def main():
    ap = argparse.ArgumentParser(description=__doc__); ap.add_argument('--root-execute', action='store_true'); args = ap.parse_args()
    if AUTHOR_DRAFT or not args.root_execute: raise RuntimeError('Guarded draft/root flag')
    if sys.platform != 'darwin' or Path(__file__).resolve() != J / SOURCE: raise RuntimeError('Root Mac/source context')
    allowed = {PROTOCOL, STEM + '_CALIBRATION.json'}
    if any(p.name not in allowed for p in J.glob(STEM + '*')): raise FileExistsError('Preserved namespace')
    owner = dict(owner='root', pid=os.getpid(), started=datetime.now(timezone.utc).isoformat(), source_sha256=sha(J / SOURCE))
    verify(owner['source_sha256'])
    try:
        cat = read('CROSS_U_NGC3198_OBSERVED_ACTIVITY_ADAPTER_V001_CATALOGUE.json')
        parent = read('CROSS_U_NGC3198_OBSERVED_ACTIVITY_ADAPTER_V001_RESULT.json')
        rc = read('CROSS_U_NGC3198_OBSERVED_ACTIVITY_ADAPTER_V001_RECEIPT.json')
        if rc['status'] != 'CLOSED' or parent['status'] != 'OBSERVED_INPUT_ADAPTER_CLOSED': raise RuntimeError('Parent not closed')
        for n in ('CROSS_U_NGC3198_OBSERVED_ACTIVITY_ADAPTER_V001_CATALOGUE.json', 'CROSS_U_NGC3198_OBSERVED_ACTIVITY_ADAPTER_V001_RESULT.json'):
            if rc['output_sha256'][n] != PINS[n]: raise RuntimeError('Accessed closed parent map')
        if rc['result_sha256'] != PINS['CROSS_U_NGC3198_OBSERVED_ACTIVITY_ADAPTER_V001_RESULT.json']: raise RuntimeError('Parent result seal')
        if rc['input_sha256'] != parent['inputs'] or rc['owner'] != parent['owner'] or cat['owner'] != parent['owner']: raise RuntimeError('Parent owner/input map')
        if parent['counts']['controls'] != 176 or not all(x['passed'] is True for x in parent['controls']): raise RuntimeError('Parent numerical controls')
        if parent['physical_flags'] != FLAGS or cat['physical_flags'] != FLAGS: raise RuntimeError('Parent physical disposition')
        rows = cat['rows']; check('closed_parent_23_rows', len(rows) == 23 and rows[0]['R_kpc'] == .3 and rows[-1]['R_kpc'] == 15.1,
            dict(count=len(rows), radii=[x['R_kpc'] for x in rows]))
        cal = read(STEM + '_CALIBRATION.json')
        constants = [cal['FUV_SFR_coefficient'], cal['IR24_SFR_coefficient_nominal'], cal['IR24_SFR_coefficient_published_range'], cal['IR24_frequency_Hz'],
            cal['MJy_SI_W_m2_Hz'], cal['MJy_CGS_erg_s_cm2_Hz'], cal['original_Leroy_NGC3198_inclination_deg']]
        check('literal_primary_calibration', constants == [.081, .0032, [.0025, .0044], 1.25e13, 1e-20, 1e-17, 72.], constants)
        cosine = math.cos(math.radians(cal['original_Leroy_NGC3198_inclination_deg']))
        forward, unit, los, bracket = [], [], [], []
        for old in rows:
            row = dict(R_kpc=old['R_kpc'], original_catalogue_row=old, bands={})
            ROWS.append(row)
            for band, field, coefficient in [('FUV', 'FUV_component_Msun_yr_kpc2', .081), ('IR24', 'IR24_component_Msun_yr_kpc2', .0032)]:
                sf = old[field]; face = sf / coefficient
                val = dict(original_SFR_component=sf, nominal_SFR_coefficient=coefficient, face_on_I_nu_cos_i_MJy_sr=face,
                    catalogue_line_of_sight_I_nu_MJy_sr=face / cosine, face_on_I_nu_cos_i_W_m2_Hz_sr=face * 1e-20,
                    face_on_I_nu_cos_i_erg_s_cm2_Hz_sr=face * 1e-17, component_measurement_rms=None)
                row['bands'][band] = val
                forward.append(relative(face * coefficient, sf))
                unit.append(relative(val['face_on_I_nu_cos_i_W_m2_Hz_sr'] * 1000., val['face_on_I_nu_cos_i_erg_s_cm2_Hz_sr']))
                los.append(relative(val['catalogue_line_of_sight_I_nu_MJy_sr'] * cosine, face))
                if band == 'IR24':
                    lo, hi = cal['IR24_SFR_coefficient_published_range']
                    val['counterfactual_fixed_SFR_component_conversion_MJy_sr'] = [sf / hi, sf / lo]
                    val['face_on_nu_I_nu_cos_i_W_m2_sr'] = face * 1e-20 * cal['IR24_frequency_Hz']
                    bracket.append(sf / hi <= face <= sf / lo)
            if not all(math.isfinite(x) and x >= 0 for b in row['bands'].values() for k, x in b.items() if isinstance(x, (int, float))):
                raise ArithmeticError('Nonfinite/nonpositive band input')
        check('nominal_inverse_forward_and_IR_calibration_bracket', max(forward) <= 32 * EPS and all(bracket), dict(errors=forward, brackets=bracket, tolerance=32 * EPS))
        check('SI_CGS_spectral_conversion', max(unit) <= 32 * EPS, dict(errors=unit, factor=1000., tolerance=32 * EPS))
        check('original_inclination_back_projection', max(los) <= 32 * EPS, dict(errors=los, inclination_deg=72., cosine=cosine, tolerance=32 * EPS))
        refused = False
        try: physical_source_gate()
        except PhysicalSourceUnavailable: refused = True
        check('physical_source_promotion_refused', refused, dict(refused=refused))
        if len(CHECKS) != 6: raise RuntimeError('Fixed six-control census')
        result = dict(status='PRESENT_BAND_INPUT_ADAPTER_CLOSED', owner=owner, input_sha256={**PINS, PROTOCOL: PROTOCOL_SHA, SOURCE: owner['source_sha256']},
            rows=ROWS, controls=CHECKS, calibration=cal, original_support_kpc=[.3, 15.1], original_SFR_rms_scope='Quoted total only; not assigned to either band',
            same_EPS5_parent_source_identity=parent['inherited_source_identity'], parent_result_sha256=PINS['CROSS_U_NGC3198_OBSERVED_ACTIVITY_ADAPTER_V001_RESULT.json'],
            observation_constraint='Admitted radiation transfer predicts directional I_nu in the measured bands; these values constrain it without assigning local field energy or writer rate.',
            source_vertex='-kappa F_munu F^munu delta O/(4 mu0); null-beam intensity alone does not fix this joint source',
            unknown={k:None for k in ('bolometric_flux','band_integrated_power','three_dimensional_radiation_stress','F_squared','native_field_joint_state','writer_rate','source_history','velocity')}, physical_flags=FLAGS)
        result_hash = publish('RESULT', result); verify(owner['source_sha256'])
        if actual_outputs() != CREATED or read(STEM + '_RESULT.json') != result: raise RuntimeError('Result schema/census')
        publish('RECEIPT', dict(status='CLOSED', owner=owner, closed=datetime.now(timezone.utc).isoformat(), input_sha256=result['input_sha256'],
            output_sha256=dict(CREATED), result_sha256=result_hash, physical_flags=FLAGS))
        verify(owner['source_sha256'])
        if actual_outputs() != CREATED: raise RuntimeError('Final actual output census')
        print(json.dumps(dict(status=result['status'], rows=len(ROWS), controls=len(CHECKS), result_sha256=result_hash)))
    except BaseException as exc:
        prior = J / (STEM + '_RECEIPT.json')
        prior_ref = dict(file=prior.name, sha256=sha(prior)) if prior.exists() else None
        outputs = actual_outputs()
        eh = publish('ERROR', dict(status='CLOSED_ERROR', owner=owner, exception=repr(exc), traceback=traceback.format_exc(),
            available_rows=ROWS, controls=CHECKS, preserved_output_sha256=outputs, prior_receipt=prior_ref, physical_flags=FLAGS))
        if prior_ref is None: publish('RECEIPT', dict(status='CLOSED_ERROR', owner=owner, closed=datetime.now(timezone.utc).isoformat(),
            input_sha256={**PINS, PROTOCOL:PROTOCOL_SHA, SOURCE:owner['source_sha256']}, output_sha256=actual_outputs(), error_sha256=eh, physical_flags=FLAGS))
        actual_outputs()
        raise

if __name__ == '__main__': main()

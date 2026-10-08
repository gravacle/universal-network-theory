"""Stdlib saved-data audit only; no propagation, eigensolver or producer import."""
import base64
import hashlib
import json
import math
from pathlib import Path
import zlib

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
RESULT = HERE / 'NATIVE_TRANSPORT_TWIST_V001_RESULTS.json'
FREEZE = HERE / 'NATIVE_TRANSPORT_TWIST_V001_FROZEN.json'
TRANSPORT = HERE / 'NATIVE_TRANSPORT_TWIST_V001_TRANSPORT.json'
OLD = HERE / 'RECORD_ADDITION_RESULTS.json'
EXPECTED_RESULT = '9f29e3d5083d5a03b2e02dca62c2dd90041fa1303a573c55e5a73ed5545775d3'


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    result = json.loads(RESULT.read_text())
    freeze = json.loads(FREEZE.read_text())
    transport = json.loads(TRANSPORT.read_text())
    old = json.loads(OLD.read_text())
    assert sha(RESULT) == EXPECTED_RESULT
    assert result['freeze_sha256'] == sha(FREEZE)
    assert result['payload_sha256'] == hashlib.sha256(encode(result['payload'])).hexdigest()
    assert old['payload_sha256'] == hashlib.sha256(encode(old['payload'])).hexdigest()
    assert result['status'] == old['status'] == 'COMPLETE'
    for name, digest in freeze['files'].items():
        path = (PROJECT / name).resolve(strict=True)
        assert path.is_relative_to(PROJECT) and sha(path) == digest, name
    old_freeze = HERE / 'RECORD_ADDITION_FROZEN.json'
    assert old['freeze_sha256'] == sha(old_freeze)
    for name, digest in json.loads(old_freeze.read_text())['files'].items():
        assert freeze['files'][name] == digest
    raw = zlib.decompress(base64.b64decode(transport['data']))
    assert transport['codec'] == 'zlib/base64' and transport['producer_exit_code'] == 0
    assert len(raw) == transport['raw_bytes']
    assert hashlib.sha256(raw).hexdigest() == transport['raw_sha256'] == sha(RESULT)
    assert raw == RESULT.read_bytes()
    p = result['payload']
    assert p['configuration'] == freeze['configuration']
    assert len(p['checks']) == p['check_count'] == 3110
    assert p['failure_count'] == 0 and p['output_target_exceeded'] is False
    for c in p['checks']:
        assert c['passed'] is True
        assert math.isfinite(c['residual']) and 0 <= c['residual'] <= c['tolerance']
    for c in old['payload']['checks']:
        assert c['passed'] is True
    assertions = []

    def compare(tag, got, expected, tolerance=2e-11):
        residual = abs(got-expected)
        assertions.append(dict(tag=tag, absolute_error=residual, tolerance=tolerance))
        assert math.isfinite(residual) and residual <= tolerance, (tag, got, expected)

    ages = [0., .25, .5, 1., 2.]
    names = ['native', 'feedback_off', 'copying_off']
    assert [(r['preparation'], r['age']) for r in p['rows']] == [(n, a) for n in names for a in ages]
    assert len(p['synthetic_controls']) == 6
    old_cases = {c['name']: c for c in old['payload']['cases']}
    hbar = p['configuration']['hbar']

    def readout_checks(q, t, tag):
        D, j = q['contact_t_nT'], q['current_t_nJ']
        compare(tag+':factorized_D', q['factorized_contact'], t*q['incidence_mean']*q['transfer_mean'])
        compare(tag+':factorized_j', q['factorized_current'], t*q['incidence_mean']*q['current_operator_mean'])
        compare(tag+':D_correlation', q['contact_factorization_error'], D-q['factorized_contact'])
        compare(tag+':j_correlation', q['current_factorization_error'], j-q['factorized_current'])
        compare(tag+':rate', q['carrier_right_rate'], j/hbar)
        compare(tag+':moment', q['contact_frequency_moment'], D/hbar**2)
        assert [a['phi'] for a in q['angles']] == p['configuration']['angles']
        by_angle = {a['phi']: a for a in q['angles']}
        for a in q['angles']:
            phi = a['phi']
            sn, one_minus_cos = math.sin(phi), 2*math.sin(phi/2)**2
            work = D*one_minus_cos-j*sn
            compare(tag+':work', a['interaction_work'], work)
            compare(tag+':full_E', a['complete_fixed_state_energy'], q['complete_held_energy']+work)
            compare(tag+':derivative', a['energy_derivative'], D*sn-j*math.cos(phi))
            compare(tag+':second_derivative', a['energy_second_derivative'], D*math.cos(phi)+j*sn)
            compare(tag+':state_work', a['fixed_H_state_twist_work'], D*one_minus_cos+j*sn)
        eps = p['configuration']['small_angle']
        fp, fm = by_angle[eps]['interaction_work'], by_angle[-eps]['interaction_work']
        compare(tag+':centered_first_published', q['small_angle_first'], (fp-fm)/(2*math.sin(eps)))
        compare(tag+':centered_second_published', q['small_angle_second'], (fp+fm)/(4*math.sin(eps/2)**2))
        compare(tag+':centered_first_exact', q['small_angle_first'], -j, 2e-9)
        compare(tag+':centered_second_exact', q['small_angle_second'], D, 2e-9)

    def formed_readout(psi, t, lam):
        # Bit-index contractions of an already saved vector, not time evolution.
        prob = [abs(a)**2 for a in psi]
        nmean = math.fsum(prob[i] for i in range(16) if i & 2)
        pairs = [(i, psi[i].conjugate()*psi[i+1]) for i in range(0, 16, 2)]
        T = 2*math.fsum(z.real for _, z in pairs)
        J = 2*math.fsum(z.imag for _, z in pairs)
        D = 2*t*math.fsum(z.real for i, z in pairs if i & 2)
        j = 2*t*math.fsum(z.imag for i, z in pairs if i & 2)
        diagonal = math.fsum(prob[i]*(3+int(bool(i & 4))+int(bool(i & 8))
            +(2.25-lam*(int(bool(i & 4))+int(bool(i & 8))))*int(bool(i & 2)))
            for i in range(16))
        xa = 2*math.fsum((psi[i].conjugate()*psi[i+2]).real for i in range(16) if not i & 2)
        return dict(incidence_mean=nmean, transfer_mean=T, current_operator_mean=J,
                    contact_t_nT=D, current_t_nJ=j, complete_held_energy=diagonal-xa-D)

    summaries = []
    for r in p['rows']:
        case = old_cases[r['preparation']]
        assert r['parameters'] == case['parameters']
        prior = next(a for a in case['hold'] if a['time'] == r['age'])
        q = r['readout']
        tag = r['preparation']+':'+str(r['age'])
        t, lam = r['parameters']['t_hop'], r['parameters']['lambda_R']
        readout_checks(q, t, tag)
        compare(tag+':old_energy', q['complete_held_energy'], case['held_energy'])
        compare(tag+':old_component_sum', q['complete_held_energy'], math.fsum(prior['energy_terms'].values()))
        compare(tag+':old_hopping_contact', q['contact_t_nT'], -prior['energy_terms']['carrier_hopping'])
        compare(tag+':old_incidence', q['incidence_mean'], prior['link_occupation'])
        if r['age'] == 0.:
            v = case['formed_vector']
            psi = [complex(a, b) for a, b in zip(v['real'], v['imag'])]
            for key, value in formed_readout(psi, t, lam).items():
                compare(tag+':independent_saved_vector_'+key, q[key], value)
        summaries.append(dict(preparation=r['preparation'], age=r['age'], contact=q['contact_t_nT'],
            current=q['current_t_nJ'], factorized_contact=q['factorized_contact'],
            factorized_current=q['factorized_current'], held_energy=q['complete_held_energy']))

    synthetic = [('Xplus','on', [.5**.5,.5**.5]), ('Xminus','on',[.5**.5,-.5**.5]),
        ('Yplus','on',[.5**.5,1j*.5**.5]), ('Yminus','on',[.5**.5,-1j*.5**.5]),
        ('left','on',[1.,0.]), ('Xplus','off',[.5**.5,.5**.5])]
    for r, (label, incidence, pair) in zip(p['synthetic_controls'], synthetic):
        assert (r['label'], r['incidence']) == (label, incidence)
        tag = 'synthetic:'+label+':'+incidence
        readout_checks(r['readout'], .5, tag)
        psi = [0j]*16
        i = 2 if incidence == 'on' else 0
        psi[i:i+2] = pair
        for key, value in formed_readout(psi, .5, .5).items():
            compare(tag+':independent_vector_'+key, r['readout'][key], value)

    fb = [r['readout'] for r in p['rows'] if r['preparation'] == 'feedback_off']
    co = [r['readout'] for r in p['rows'] if r['preparation'] == 'copying_off']
    control_diffs = {key: max(abs(a[key]-b[key]) for a, b in zip(fb, co))
        for key in ['contact_t_nT','current_t_nJ','incidence_mean','transfer_mean','current_operator_mean']}
    for key, diff in control_diffs.items():
        compare('controls_actual_transport_match:'+key, diff, 0.)
    payload = dict(scope='Saved-data arithmetic and original age-zero vector contractions only; no propagation, eigensolve, formation, or producer import.',
        source_sha256=sha(Path(__file__)), result_sha256=sha(RESULT), freeze_sha256=sha(FREEZE),
        producer_payload_sha256=result['payload_sha256'], transport_sha256=sha(TRANSPORT),
        original_result_sha256=sha(OLD), frozen_member_count=len(freeze['files']),
        authenticated_transport_bytes=len(raw), original_check_count=p['check_count'],
        original_max_residual=max(c['residual'] for c in p['checks']),
        original_seconds=p['seconds'], original_peak_self_rss_bytes=p['peak_rss_bytes'],
        actual_rows=len(p['rows']), synthetic_rows=len(synthetic), angle_readouts=6*(len(p['rows'])+len(synthetic)),
        arithmetic_comparison_count=len(assertions), max_absolute_error=max(a['absolute_error'] for a in assertions),
        max_error_over_tolerance=max(a['absolute_error']/a['tolerance'] for a in assertions),
        worst_absolute_comparison=max(assertions, key=lambda a:a['absolute_error']),
        feedback_off_copying_off_transport_max_differences=control_diffs,
        actual_row_summary=summaries,
        independently_reconstructed='All angle work/derivatives, factorization arithmetic and old energy/contact/incidence controls; all readout operators for the three saved formed vectors at age zero and six synthetic controls. Later-age currents/matrix reconstruction are producer controls, not a second propagation here.')
    out = dict(status='COMPLETE', payload_sha256=hashlib.sha256(encode(payload)).hexdigest(), payload=payload)
    print(json.dumps(out, sort_keys=True, indent=2, allow_nan=False))


if __name__ == '__main__':
    main()

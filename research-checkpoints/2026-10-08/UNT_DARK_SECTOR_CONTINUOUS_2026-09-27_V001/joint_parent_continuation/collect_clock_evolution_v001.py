"""Read-only census/contrasts of all frozen clock cases; no evolution."""
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha(path):
    path = path.resolve(strict=True)
    path.relative_to(ROOT)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    freeze_path = HERE / 'COSMOLOGICAL_CLOCK_EVOLUTION_V001_FROZEN.json'
    freeze = json.loads(freeze_path.read_text())
    frozen_sha = sha(freeze_path)
    for name, expected in freeze['files'].items():
        assert sha(ROOT / name) == expected, name
    assert len(freeze['cases']) == 12
    files = {freeze_path.name: frozen_sha, Path(__file__).name: sha(Path(__file__))}
    rows, counts, maxima, timings = [], {}, {}, []
    slow = None
    config = freeze['configuration']
    fields = ['u', 'u_log_a', 'clock_source_Q', 'acceleration_over_H0',
              'unitary_lapse_times_k_over_H0', 'H0_clock_pi_times_k_over_H0',
              'hard_density_contrast_per_k_over_H0',
              'polarization_contrast_per_k_over_H0']
    for expected in freeze['cases']:
        index = expected['case']
        path = HERE / f'COSMOLOGICAL_CLOCK_EVOLUTION_V001_CASE_{index:02d}.json'
        wrapper = json.loads(path.read_text())
        files[path.name] = sha(path)
        data = wrapper['payload']
        assert wrapper['freeze_sha256'] == frozen_sha
        assert wrapper['payload_sha256'] == hashlib.sha256(encode(data)).hexdigest()
        assert data['selected_case'] == index
        assert encode(data['configuration']) == encode(config)
        assert encode(data['reference']) == encode(freeze['reference'])
        assert data['status'] == 'COMPLETE' and not data['checks']['failures']
        assert len(data['rows']) == 1
        row = data['rows'][0]
        assert all(row[key] == value for key, value in expected.items())
        assert len(row['full_states']) == 5
        assert [v['a'] for v in row['full_states']] == config['full_state_scale_factors']
        if slow is None:
            slow = data['slow_reference']['rows']
        else:
            assert encode(slow) == encode(data['slow_reference']['rows'])
        assert [v['a'] for v in row['sample_rows']] == [v['a'] for v in slow]
        assert len(slow) == 64
        for field in fields:
            assert all(len(v[field]) == 2 and all(math.isfinite(x) for x in v[field])
                       for v in row['sample_rows'])
        actual_peak = [max(abs(v['u'][col]) for v in row['sample_rows']) for col in (0, 1)]
        assert actual_peak == row['sampled_maximum_absolute_tilt_transfer']
        for key, value in data['checks']['counts'].items():
            counts[key] = counts.get(key, 0) + value
        for key, value in data['checks']['maximum_errors'].items():
            maxima[key] = max(maxima.get(key, 0), value)
        timings.append(dict(case=index, seconds=data['seconds'], peak_self_rss_bytes=data['peak_self_rss_bytes']))
        rows.append(row)
    contrasts = []
    for gap in (.001, .002):
        for eta in config['etas']:
            pair = [next(r for r in rows if r['gap'] == gap and r['eta'] == eta and r['order'] == order)
                    for order in (64, 128)]
            channels = {}
            for field in fields:
                a, b = [[v[field] for v in r['sample_rows']] for r in pair]
                scale = [max(1, max(abs(v[col]) for v in a), max(abs(v[col]) for v in b)) for col in (0, 1)]
                difference = [[vb[col] - va[col] for col in (0, 1)] for va, vb in zip(a, b)]
                channels[field] = dict(fine_minus_coarse=difference,
                    peak_normalized_difference=[max(abs(v[col])/scale[col] for v in difference) for col in (0, 1)])
            contrasts.append(dict(gap=gap, eta=eta, channels=channels))
    summary = []
    for row in rows:
        item = {key: row[key] for key in ('case', 'gap', 'eta', 'order', 'tau_star_seconds',
                  'sampled_maximum_absolute_tilt_transfer',
                  'initial_amplitude_for_sampled_tilt_below_display_threshold')}
        item['a_at_sampled_peak'] = [max(row['sample_rows'], key=lambda v: abs(v['u'][col]))['a'] for col in (0, 1)]
        item['at_present'] = next(v for v in row['sample_rows'] if v['a'] == 1.)
        item['at_final'] = row['sample_rows'][-1]
        item['numerical_comparisons'] = {key: value['maximum_scaled_error'] for key, value in row['comparisons'].items()}
        summary.append(item)
    payload = dict(status='COMPLETE_SAVED_CASE_CENSUS', files=files,
        original_frozen_member_count=len(freeze['files']), case_count=len(rows),
        sample_count_per_case=len(slow), full_state_count_per_case=5,
        producer_check_counts=counts, producer_check_maximum_errors=maxima,
        producer_check_total=sum(counts.values()), cases=summary,
        quadrature_contrasts=contrasts, slow_reference=slow, timing=timings,
        scope='Read-only aggregation, all12 cases and all six64/128 contrasts; no ODE rerun. All channel contrasts are descriptive, not outcome-selected convergence gates. Each original normalized basis has zero initial soft coordinates. Eta is illustrative, not a measured network clock. Radiation is omitted from this synthetic background. Large internal transfer is not an observed cosmic amplitude or an all-sector stability conclusion.',
        amplitude_scope='Quoted initial-amplitude ceilings control only sampled physical tilt, not lapse, density, unsampled extrema or nonlinear validity.')
    print(encode(dict(payload=payload, payload_sha256=hashlib.sha256(encode(payload)).hexdigest())).decode())


if __name__ == '__main__':
    main()

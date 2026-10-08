#!/usr/bin/env python3
"""Post-hoc scalar reconstruction from sealed moments; no physics/RNG replay."""
from pathlib import Path
import hashlib
import json
import math
import os
import sys
import traceback
import numpy as np

J = Path(__file__).resolve().parent
NAME = 'LOCAL_RECORD_FEEDBACK_3D_SCALAR_PAIR_COORDINATION_RECOVERY_V001'
SOURCE = Path(__file__).resolve()
SEALS = {
    'WORLDLINE_PILOT': ('LOCAL_RECORD_FEEDBACK_3D_WORLDLINE_PILOT_V001',
                       'local_record_feedback_3d_worldline_pilot_v001_checkpoints',
                       '2fb94e9b5c9f22eb9161013024d542b03bf5822eed1736e1ba883aa1e1cf730c'),
    'COLLECTIVE_CYCLE': ('LOCAL_RECORD_FEEDBACK_3D_COLLECTIVE_CYCLE_CONTINUATION_V001',
                       'local_record_feedback_3d_collective_cycle_continuation_v001_checkpoints',
                       '7c3567741d689da4d339aceb7373d6ae70bb43d71729d1574d0d4bec5a5e1c83'),
}
COMPLETED = []


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def save(path, value):
    with path.open('xb') as stream:
        stream.write(canonical(value) + b'\n')
        stream.flush()
        os.fsync(stream.fileno())
    return sha(path)


def estimate(raw, beta):
    mean = raw[:2]
    second = np.array(((raw[2], raw[3]), (raw[3], raw[4])))
    return beta * 54 * (second - np.outer(mean, mean))


def summary(blocks, beta):
    b = len(blocks)
    mean = blocks.mean(axis=0)
    central = estimate(mean, beta)
    replicas = np.array([estimate((b * mean - blocks[i]) / (b - 1), beta) for i in range(b)])
    error = np.sqrt((b - 1) / b * ((replicas - replicas.mean(axis=0)) ** 2).sum(axis=0))
    assert np.isfinite(central).all() and np.isfinite(error).all()
    assert float(np.linalg.eigvalsh(central).min()) >= -3e-11 * max(1, float(np.linalg.norm(central)))
    return {'mean_density_T_Q': mean[:2].tolist(), 'chi_density_T_Q': central.tolist(),
            'component_block_SE': error.tolist(), 'blocks': b, 'block_size': 16,
            'scalar_abs_cross_exceeds_three_SE': bool(abs(central[0, 1]) > 3 * error[0, 1])}


def ess(values):
    x = values - values.mean()
    c0 = float(x @ x / len(x))
    if c0 == 0:
        return {'ESS': None, 'tau': None, 'status': 'UNDEFINED_CONSTANT'}
    cov = [float(x[:-lag] @ x[lag:] / (len(x) - lag)) for lag in range(1, 127)]
    total = 0.0
    for i in range(0, 126, 2):
        pair = cov[i] + cov[i + 1]
        if pair <= 0:
            break
        total += pair
    tau = max(1.0, 1 + 2 * total / c0)
    return {'ESS': len(x) / tau, 'tau': tau, 'status': 'SHORT_CHAIN_IPP_ESTIMATE'}


def recover(label, name, cpname, receipt_pin):
    cp = J / cpname
    receipt_path = J / (name + '_RECEIPT.json')
    assert sha(receipt_path) == receipt_pin
    receipt = json.loads(receipt_path.read_bytes())
    parent_path = J / (name + '_RESULT.json')
    parent = json.loads(parent_path.read_bytes())
    assert sha(parent_path) == receipt['result_sha256']
    assert hashlib.sha256(canonical(parent)).hexdigest() == receipt['result_canonical_sha256']
    assert parent['failed'] == 0 and len(parent['chains']) == 16 and len(parent['conditions']) == 4
    rows, condition_blocks = [], {i: [] for i in range(4)}
    for chain in parent['chains']:
        cid = chain['id']
        ref = chain['checkpoints'][-1]
        meta_path, bundle = cp / ref['metadata'], cp / ref['bundle']
        assert sha(meta_path) == ref['metadata_sha256'] == receipt['checkpoint_sha256'][ref['metadata']]
        assert sha(bundle) == ref['bundle_sha256'] == receipt['checkpoint_sha256'][ref['bundle']]
        meta = json.loads(meta_path.read_bytes())
        assert meta['id'] == cid and meta['completed_production_sweeps'] == 256
        with np.load(bundle, allow_pickle=False) as arrays:
            scalars = arrays['scalar']
            mean_d = arrays['mean_d']
        assert scalars.shape == (256, 15) and mean_d.shape == (256, 7, 2)
        assert np.max(np.abs(mean_d[:, 0].imag)) <= 3e-11
        td = 2 * scalars[:, 3] - 2
        qd = mean_d[:, 0].real.sum(axis=1) / (2 * math.sqrt(27))
        assert np.max(np.abs(qd - (4 * scalars[:, 4] - 2))) <= 3e-11
        assert np.max(np.abs(scalars[:, 1] - (scalars[:, 3] - qd / 2))) <= 3e-11
        primitives = np.column_stack((td, qd, td * td, td * qd, qd * qd))
        blocks = primitives.reshape(16, 16, 5).mean(axis=1)
        row = {'parent_segment': label, 'id': cid, 'condition': chain['condition'],
               'beta': chain['beta'], 'epsilon': chain['epsilon'],
               'parent_chain_status': chain['status'], **summary(blocks, chain['beta']),
               'scalar_ESS': {key: ess(value) for key, value in
                              (('T_density', td), ('Q_density', qd), ('TQ_over_V', 54 * td * qd))},
               'raw_block_moments': blocks.tolist(), 'source_terminal_reference': ref}
        assert abs(row['chi_density_T_Q'][1][1] - chain['estimates']['chi_evenodd']['real'][0][0][0]) <= 3e-11
        rows.append(row)
        COMPLETED.append(row)
        condition_blocks[chain['condition']].append(blocks)
        assert sha(meta_path) == ref['metadata_sha256'] and sha(bundle) == ref['bundle_sha256']
    conditions = []
    for condition in parent['conditions']:
        i = condition['condition']
        conditions.append({'parent_segment': label, 'condition': i, 'beta': condition['beta'],
                           'epsilon': condition['epsilon'], 'parent_condition_status': condition['status'],
                           **summary(np.concatenate(condition_blocks[i]), condition['beta'])})
    assert sha(receipt_path) == receipt_pin and sha(parent_path) == receipt['result_sha256']
    return {'receipt_sha256': receipt_pin, 'result_sha256': receipt['result_sha256'],
            'chains': rows, 'conditions': conditions}


def main():
    assert sys.argv[1:] == ['--execute']
    result_path, report_path, receipt_path, error_path = [J / (NAME + suffix) for suffix in
                                                         ('_RESULT.json', '_RESULT.md', '_RECEIPT.json', '_ERROR.json')]
    assert not any(p.exists() for p in (result_path, report_path, receipt_path, error_path))
    segments = {label: recover(label, *spec) for label, spec in SEALS.items()}
    contrasts = []
    for i in range(4):
        old, new = (segments[label]['conditions'][i] for label in ('WORLDLINE_PILOT', 'COLLECTIVE_CYCLE'))
        contrasts.append({'condition': i, 'new_minus_old': (np.array(new['chi_density_T_Q']) - np.array(old['chi_density_T_Q'])).tolist(),
                          'old_component_SE': old['component_block_SE'], 'new_component_SE': new['component_block_SE'],
                          'status': 'CORRELATED_SEGMENTS_SEPARATE_ERRORS_NO_INDEPENDENT_COMBINATION'})
    result = {'name': NAME, 'source_sha256': sha(SOURCE), 'segments': segments, 'contrasts': contrasts,
              'status': 'POST_HOC_EXACT_SCALAR_RECONSTRUCTION_ONLY',
              'method': 'T/V=2 scalar_delta2_density-2; Q/V=Re(sum_AB mean_d(k0))/(2sqrt27); chi_density=beta V covariance; V=54',
              'limitations': ['PARENT_MIXING_STATUSES_RETAINED', 'NO_NEW_153_TENSOR_DIAGNOSTICS',
                              'NO_FULL_PAIR_MATRIX_OR_PHYSICAL_MEMORY_METRIC', 'BLOCK_ERRORS_MAY_MISS_SLOW_MODES',
                              'POST_HOC_RECOVERY_NOT_BLIND_VALIDATION', 'FINITE_BETA_M_L_NO_PHYSICAL_CLOCK_RULER_OR_GRAVITY'],
              'formal_fixed_ice_h2_comparator': (0.2 ** 2 / 27 * np.array(((896, 416), (416, 224)))).tolist()}
    raw_sha = save(result_path, result)
    lines = ['# Recovered scalar pair–coordination response V001', '',
             'Post-hoc reconstruction from complete sealed production moments; no Hamiltonian, sampler, RNG or producer replay.',
             'The primary scalar channel is recoverable; the directional pair matrix still requires the new measurement.', '',
             '| Segment | Condition | beta | dt | chi_TT/V | chi_TQ/V | chi_QQ/V | Parent condition status |',
             '|---|---:|---:|---:|---|---|---|---|']
    for segment in segments.values():
        for row in segment['conditions']:
            values, errors = row['chi_density_T_Q'], row['component_block_SE']
            entries = [f'{values[a][b]:.8g} +/- {errors[a][b]:.3g}' for a, b in ((0, 0), (0, 1), (1, 1))]
            lines.append(f"| {row['parent_segment']} | {row['condition']} | {row['beta']} | {row['epsilon']} | {' | '.join(entries)} | {row['parent_condition_status']} |")
    lines += ['', 'The three-SE scalar flags are raw block diagnostics; parent mixing and the absent new tensor diagnostics are not waived.',
              'Old/new segments are correlated; each component error is separate. All32 chain estimates, raw block moments and scalar ESS remain in JSON.',
              'Formal h² comparison is not a controlled finite-h accuracy gate. No qualified retained memory, physical metric, gravity or superiority follows.', '']
    with report_path.open('x') as stream:
        stream.write('\n'.join(lines))
        stream.flush()
        os.fsync(stream.fileno())
    receipt_sha = save(receipt_path, {'result_sha256': raw_sha, 'result_canonical_sha256': hashlib.sha256(canonical(result)).hexdigest(),
                                      'report_sha256': sha(report_path), 'source_sha256': sha(SOURCE),
                                      'parent_receipt_sha256': {label: spec[2] for label, spec in SEALS.items()},
                                      'status': result['status'], 'chains': 32, 'conditions': 8})
    print(json.dumps({'status': result['status'], 'result_sha256': raw_sha, 'receipt_sha256': receipt_sha}))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        path = J / (NAME + '_ERROR.json')
        if not path.exists():
            save(path, {'error': str(error), 'traceback': traceback.format_exc(), 'completed_rows': COMPLETED})
        raise

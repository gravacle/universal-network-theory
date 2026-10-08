#!/usr/bin/env python3
"""NEW saved-only affine query response, no producer or Hamiltonian replay."""
from pathlib import Path
import hashlib
import itertools
import json
import math
import os
import sys
import time
import traceback
import numpy as np

J = Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation')
NAME = 'LOCAL_RECORD_FEEDBACK_3D_QUERY_RESPONSE_RECOVERY_V001'
PARENT = 'LOCAL_RECORD_FEEDBACK_3D_PAIR_COORDINATION_RESPONSE_V001'
SOURCE = Path(__file__).resolve()
PROTOCOL = J / (NAME + '.md')
PROTOCOL_SHA = '784888d9d6ab11d462e40c402fecf86bdda4894b2e23202d021ffa852707abf1'
CP = J / 'local_record_feedback_3d_query_response_recovery_v001_checkpoints'
PCP = J / 'local_record_feedback_3d_pair_coordination_response_v001_checkpoints'
RESULT, REPORT, RECEIPT = (J / (NAME + suffix) for suffix in ('_RESULT.json', '_RESULT.md', '_RECEIPT.json'))
PINS = {'local_record_feedback_3d_pair_coordination_response_v001.py': '0fdfd2ad3d20cd7e72a2b4e5055bfd3e422a706f85100ddfb6204f1f0f0212fb',
 'LOCAL_RECORD_FEEDBACK_3D_PAIR_COORDINATION_RESPONSE_V001.md': 'e862125ece9b312e51802a4f6fe46128088a27f4077d62ba3f311db4cc8be6c7',
 'LOCAL_RECORD_FEEDBACK_3D_PAIR_COORDINATION_RESPONSE_V001_RESULT.json': '74042b5f40401085c151b10b4e32cda5257ca09c86a831f1ef98965abf4649a8',
 'LOCAL_RECORD_FEEDBACK_3D_PAIR_COORDINATION_RESPONSE_V001_RESULT.md': '687e4643a8268b103f7e3e6a49b831deae0d5191c82050299386c0e159d3a513',
 'LOCAL_RECORD_FEEDBACK_3D_PAIR_COORDINATION_RESPONSE_V001_RECEIPT.json': '36de22839fba41a440f78d14ef24bb1930e2c1cebe0e9a9f8e1220bbc47a81c8'}
TERMINAL_PINS = {'c0_I01': ('4421209194cf90f1b92a13945cdb8488208e91aa018de8f961db54e079154648', 'f70eb09ba52fd57c1599a1ba93ff1ccdb7d07411db468210aa0ea9bc99777325'),
 'c0_I02': ('825df333285331d9b4825356e4e2425bc945fccfd88a55f94f2242fa306d9ca3', '74d436ac39bfab0a7a6208014802573532fc20d13d5709ea77544e5dfd8b29c8'),
 'c0_B': ('86b6eff0512a7ed6bd0bb95d179d9e461eb189095afdcff57818ac81dc5b55da', '706ef6af14a8daa6df7d9d480fe7869bfbf370f82f9536ffdc45fd885bf514de'),
 'c0_R': ('29d820bd7b83344968e2a18dcff6ada950487e357cf256669578afd52d2187b6', '39aee8c936602dfe551fe55b35b4fb21acc96a245447fbcf671c4c79311c18a6'),
 'c1_I01': ('ac2a9b65a0b2cc231fd2f63ea37c2557a27d5a3729dffe714fe869c0a53ee345', 'bdacf17295448b1af0bc330c93c45f166e64a5150503bd15d979658033728f5a'),
 'c1_I02': ('21eb7c64adf0f3842ef89594f447aaed57c63ae136eaa0179bd64326049d3f52', '51dabf0d85d1c4fd3a2e7853e6bbbf0113e0eb6f72127586e96b7c50ce977ee1'),
 'c1_B': ('e47d0776495aa5839ae5093efee65b5707a64fc8ba5bad16090dd654b8a9f67f', '2d4da962e297ce202a85f8ec3265e582c056e4643e59ea9fb0063c5eaae8ee28'),
 'c1_R': ('51717ac6ea151b9b9edb3953c9381d65c5f4281030fccfb273525a0eb545a620', 'f7993d9b6ca955d624a8cf14ad2065c5695306350eb11692c9eda8218bd442fb'),
 'c2_I01': ('65e24ff2ca6ebc3ba1cf8877c27c6138d685e742a721ba30d6f9ff93cc550c2e', '24f48f3e851040a335d7d22b95ac51f7408006e2d13ee91ad44c405ee0208aaf'),
 'c2_I02': ('83610997182a48b508646dc409e63d6cf8c4a95c968fd66ebabc30f4a79889a0', '18ec6c39a72733299f0c5919f25295bd3ccccb0fa0e90d4dffe260336dd9f94b'),
 'c2_B': ('19861c33f80458a1d0e927c4dec659537972d5d6f18cca3d65e959dd525fd1e4', '4623936c1078bcacc67b5c7c1c85b7a8c4e13d5264306ec5f6cef0a13b950d71'),
 'c2_R': ('17962a3902fa87a9c89c4f429630c77bddab6fb1ed74799fea059a1ad7abbf74', 'f1e1e2afb659aab1a5706fad6e5591da86b32299473773e43efe98a4cb84ab7a'),
 'c3_I01': ('d81d3f5de594d670b56b73b1a8d24b35bc0094b30f64f9f6bcafb53f11191798', '56fa0eac1b5688d7a316651b520d66682fd81ae5e53fe4ab8658bee4675f1107'),
 'c3_I02': ('49f9b0ea6a0ba85a7d5858c31f2f89d720b831ed4e89b4171a5cafa0806c2a22', '130db74f0b0b66d83a4cb937aa180322fd116eea4be383f907c7c4cf87d562f6'),
 'c3_B': ('f830d3bfff7fe57bc39d05e5631ab502803e08afc92d0642b4601e6cae5a5513', '9d98cfd16816ad34dada3d36a559cccee0b7a77a3c97d1455c81f73fa00aad26'),
 'c3_R': ('114d1ef38fc8e46e4eaf507ca280ebfc2bc241ed0929e97874ca4be82c06fc6f', '686cc6f5b7bfd9f2dd592a848168bd51057445db1ee5acf0c15afee44d1d20b8')}
PARENT_CHECK_COUNT = 180914
P = np.eye(4) - np.ones((4, 4)) / 4
PAIRS = tuple(itertools.combinations(range(4), 2))
B = np.array([np.outer(P[:, a], P[:, b]) + np.outer(P[:, b], P[:, a]) for a, b in PAIRS])
T = np.r_[np.ones(12), 0, 0]
Q = np.r_[np.zeros(12), 1, 1]
SOURCES = np.stack((T, Q), axis=1)
CHECKS, STAGES = [], {}
CREATED = False
ACTIVE = None


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def safe(value):
    if isinstance(value, dict): return {key: safe(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)): return [safe(item) for item in value]
    if isinstance(value, (float, np.floating)) and not math.isfinite(float(value)): return {'nonfinite': repr(float(value))}
    return value


def pack(value):
    a = np.asarray(value)
    return {'real': a.real.tolist(), 'imag': a.imag.tolist()} if np.iscomplexobj(a) else a.tolist()


def unpack(value):
    return np.asarray(value['real']) + 1j * np.asarray(value['imag']) if isinstance(value, dict) else np.asarray(value)


def require(passed, label):
    if not passed: raise RuntimeError('Custody: ' + label)


def close(label, first, second):
    a, b = np.asarray(first), np.asarray(second)
    residual = float(np.linalg.norm(a - b))
    tolerance = 3e-11 * max(1, float(np.linalg.norm(b)))
    row = {'label': label, 'passed': math.isfinite(residual) and residual <= tolerance,
           'residual': residual, 'tolerance': tolerance}
    CHECKS.append(safe(row))
    if not row['passed']: raise ArithmeticError(label)


def exclusive(path, value):
    with path.open('xb') as stream:
        stream.write(canonical(value) + b'\n'); stream.flush(); os.fsync(stream.fileno())
    return sha(path)


def event(kind, **fields):
    with (CP / 'journal.jsonl').open('ab') as stream:
        stream.write(canonical({'event': kind, 'pid': os.getpid(), **fields}) + b'\n')
        stream.flush(); os.fsync(stream.fileno())


def save(name, value):
    STAGES[name] = exclusive(CP / name, value)
    event('stage_complete', filename=name, sha256=STAGES[name])


def read(path):
    return json.loads(path.read_bytes())


def authenticate():
    require(len(PINS) == 5 and len(TERMINAL_PINS) == 16 and PARENT_CHECK_COUNT is not None, 'final pins frozen')
    actual = {name: sha(J / name) for name in PINS}
    require(actual == PINS, 'parent direct pins')
    actual['source'], actual['protocol'] = sha(SOURCE), sha(PROTOCOL)
    require(actual['protocol'] == PROTOCOL_SHA, 'new protocol')
    parent, receipt = read(J / (PARENT + '_RESULT.json')), read(J / (PARENT + '_RECEIPT.json'))
    require(receipt['result_sha256'] == actual[PARENT + '_RESULT.json'] and
            receipt['report_sha256'] == actual[PARENT + '_RESULT.md'], 'parent raw/report')
    require(receipt['result_canonical_sha256'] == hashlib.sha256(canonical(parent)).hexdigest(), 'parent canonical')
    require(receipt['input_sha256'] == parent['input_sha256'], 'parent input identity')
    require(receipt['failed'] == parent['failed'] == 0 and receipt['passed'] == parent['passed'] ==
            receipt['check_count'] == parent['check_count'] == len(parent['checks']) == PARENT_CHECK_COUNT and
            all(row['passed'] for row in parent['checks']), 'all parent arithmetic passed')
    require(receipt['status'] == parent['status'] and len(parent['chains']) == 16 and len(parent['conditions']) == 4, 'full census/status')
    lines = (PCP / 'journal.jsonl').read_bytes().splitlines(keepends=True)
    journal = [json.loads(line) for line in lines]
    require(hashlib.sha256(b''.join(lines[:-1])).hexdigest() == receipt['journal_prefix_sha256'] and
            journal[-1]['event'] == 'receipt_complete' and journal[-1]['sha256'] == actual[PARENT + '_RECEIPT.json'], 'journal receipt/prefix')
    actual[PCP.name + '/journal.jsonl'] = sha(PCP / 'journal.jsonl')
    commits = {(row.get('filename'), row.get('sha256')) for row in journal}
    for name, wanted in receipt['checkpoint_sha256'].items():
        digest = sha(PCP / name)
        require(digest == wanted and (name, digest) in commits, 'parent checkpoint ' + name)
        actual[PCP.name + '/' + name] = digest
    manifest = read(PCP / 'manifest.json')
    require(manifest['input_sha256'] == receipt['input_sha256'] and any(row['event'] == 'started' and
            row['input_sha256'] == receipt['input_sha256'] and row['manifest_sha256'] == receipt['checkpoint_sha256']['manifest.json'] for row in journal), 'manifest/start')
    for name, wanted in receipt['input_sha256'].items():
        if name == 'source': path = J / 'local_record_feedback_3d_pair_coordination_response_v001.py'
        elif name == 'protocol': path = J / (PARENT + '.md')
        elif name == 'core_identity_canonical_sha256':
            require(hashlib.sha256(canonical(manifest['preserved_core_identity'])).hexdigest() == wanted, 'core identity seal'); continue
        else: path = J / name
        require(sha(path) == wanted, 'inherited input ' + name)
        actual[str(path.relative_to(J))] = wanted
    for row in parent['chains']:
        cid, ref = row['id'], row['checkpoints'][-1]
        require(cid in TERMINAL_PINS and (ref['metadata_sha256'], ref['bundle_sha256']) == tuple(TERMINAL_PINS[cid]), 'terminal pin ' + cid)
        require(ref['metadata'] == cid + '_production1024.json' and ref['bundle'] == cid + '_production1024.npz', 'terminal names')
        meta = read(PCP / ref['metadata'])
        require(meta['completed_production_sweeps'] == row['production_sweeps'] == 1024 and meta['completed_burn_sweeps'] == 64 and
                meta['input_sha256'] == receipt['input_sha256'] and meta['configuration'] == {key: row[key] for key in ('seed', 'beta', 'epsilon', 'M', 'start')}, 'terminal counters/configuration')
        require(meta['bundle_sha256'] == ref['bundle_sha256'] == receipt['checkpoint_sha256'][ref['bundle']] and
                ref['metadata_sha256'] == receipt['checkpoint_sha256'][ref['metadata']], 'terminal receipt')
    return actual, parent


def chain_blocks(row):
    ref = row['checkpoints'][-1]
    with np.load(PCP / ref['bundle'], allow_pickle=False) as arrays:
        n, q = arrays['mean_z'][:, 0].copy(), arrays['bar_Q_every_production_measurement'][:, 0].copy()
    require(n.shape == (1024, 4) and q.shape == (1024, 14) and np.isfinite(n).all() and np.isfinite(q).all(), 'paired saved trace census')
    values = {'n': n, 'q': q, 'nn': n[:, :, None] * n[:, None, :].conj(),
              'qq': q[:, :, None] * q[:, None, :].conj(), 'nq': n[:, :, None] * q[:, None, :].conj()}
    blocks = {key: value.reshape(32, 32, *value.shape[1:]).mean(axis=1) for key, value in values.items()}
    old, joint = row['block_raw_moments'], row['joint_block_raw_moments']
    close(row['id'] + '_n_saved_block', blocks['n'], unpack(old['mean_z'])[:, 0])
    close(row['id'] + '_nn_saved_block', blocks['nn'], unpack(old['second_z_zero'])[:, 0])
    close(row['id'] + '_q_saved_block', blocks['q'], unpack(joint['mean_Q'])[:, 0])
    close(row['id'] + '_qq_saved_block', blocks['qq'], unpack(joint['second_Q'])[:, 0])
    for key in ('local_X_mean', 'local_pair_mean', 'local_XX_second', 'local_c2_mean'):
        blocks[key] = unpack(joint[key])
    return blocks


def calculate(raw, beta):
    n, q = raw['n'], raw['q']
    sn = raw['nn'] - n[:, None] * n[None, :].conj()
    chi = beta * (raw['qq'] - q[:, None] * q[None, :].conj())
    cross = beta * (raw['nq'] - n[:, None] * q[None, :].conj())
    mu = raw['local_X_mean']
    mu_b = -2 * P @ n / math.sqrt(27)
    mu_prime = -2 * P @ cross @ SOURCES
    gamma = (chi[:12] @ SOURCES).reshape(2, 6, 2)
    pair_term = np.einsum('spa,pij->saij', gamma, B, optimize=True)
    dyad_term = np.einsum('ia,sj->saij', mu_prime, mu) + np.einsum('si,ja->saij', mu, mu_prime)
    response = pair_term - dyad_term
    pair_mean = q[:12].reshape(2, 6) / math.sqrt(27)
    mean_dyad = mu[:, :, None] * mu[:, None, :]
    cov = raw['local_XX_second'] - mean_dyad
    scalar_chi = SOURCES.T @ chi @ SOURCES / 2
    sector = 2 * raw['local_c2_mean'].mean() - scalar_chi[0, 0] / 4
    return {'mu': mu, 'mu_from_centered_occupation': mu_b, 'mean_dyad': mean_dyad,
            'mu_prime_u_f': mu_prime, 'gamma_u_f': gamma, 'pair_term_u_f': pair_term,
            'dyad_term_u_f': dyad_term, 'response_u_f': response,
            'all_vertex_response_u_f': response.mean(axis=0),
            'all_vertex_response_trace_u_f': np.trace(response.mean(axis=0), axis1=-2, axis2=-1), 'ET_covariance': cov,
            'pair_mean': pair_mean, 'S_zero': sn, 'chi_joint_k0': chi, 'chi_nQ': cross,
            'scalar_chi_density_TQ': scalar_chi, 'fixed_V_conditional_sector_contact_minus_response': sector}


def summarize(blocks, beta, label, parent_row):
    count = len(blocks['q'])
    raw = {key: value.mean(axis=0) for key, value in blocks.items()}
    result = calculate(raw, beta)
    replicas = [calculate({key: (count * value.mean(axis=0) - value[i]) / (count - 1)
                           for key, value in blocks.items()}, beta) for i in range(count)]
    errors = {}
    for key in result:
        a = np.asarray([replica[key] for replica in replicas])
        errors[key] = {part + '_se': np.sqrt((count - 1) / count * ((getattr(a, part) - getattr(a, part).mean(axis=0)) ** 2).sum(axis=0))
                       for part in (('real', 'imag') if np.iscomplexobj(a) else ('real',))}
    mu, response, gamma = result['mu'], result['response_u_f'], result['gamma_u_f']
    close(label + '_mean_query_crosswalk', mu, np.repeat(result['mu_from_centered_occupation'][None], 2, axis=0))
    close(label + '_pair_mean', raw['local_pair_mean'], result['pair_mean'])
    close(label + '_ET_identity_with_mean_dyad', result['ET_covariance'], P[None] + np.einsum('sp,pij->sij', result['pair_mean'], B) - result['mean_dyad'])
    close(label + '_parent_ET_covariance', result['ET_covariance'], unpack(parent_row['joint_estimates']['local_X_ET_covariance']))
    close(label + '_parent_chi_k0', result['chi_joint_k0'], unpack(parent_row['joint_estimates']['chi_joint'])[0])
    close(label + '_parent_S_zero_k0', result['S_zero'], unpack(parent_row['estimates']['S_zero'])[0])
    close(label + '_f_mean_response_crosswalk', result['mu_prime_u_f'][:, 1], -4 * beta * P @ result['S_zero'] @ np.ones(4))
    close(label + '_response_transpose', response, response.swapaxes(-1, -2))
    close(label + '_P_projected_response', np.einsum('ij,sajk,kl->sail', P, response, P), response)
    close(label + '_zero_response_rows', response.sum(axis=-1), np.zeros((2, 2, 4)))
    trace = np.trace(response, axis1=-2, axis2=-1)
    close(label + '_response_trace', trace, -gamma.sum(axis=1) / 2 - 2 * mu @ result['mu_prime_u_f'])
    dc = unpack(parent_row['joint_estimates']['chi_Dc_independent'])[0]
    cc = unpack(parent_row['joint_estimates']['chi_cc'])[0]
    close(label + '_f_degree_square_response', gamma[:, :, 1].sum(axis=1) / 2, (dc + cc / 2) @ np.ones(2))
    close(label + '_primary_TQ_response', gamma[:, :, 1].sum() / 2, result['scalar_chi_density_TQ'][0, 1])
    close(label + '_degree_square_mean', raw['local_c2_mean'].mean(), 1 + q_scalar(raw['q']) / 2)
    close(label + '_k0_response_imaginary', response.imag, np.zeros_like(response.imag))
    return {'id': label, 'beta': beta, 'block_count': count, 'block_measurements': 32,
            'parent_status': parent_row['status'], 'posthoc_scope': 'SAVED_FINITE_GRID_RESPONSE_WITH_UNCHANGED_PARENT_QUALIFICATION',
            'values': {key: pack(value) for key, value in result.items()},
            'component_errors': {key: {part: pack(value) for part, value in error.items()} for key, error in errors.items()},
            'raw_block_sufficient_sums': {key: pack(32 * value) for key, value in blocks.items()},
            'new_significance_or_inverse_qualification': False}


def q_scalar(q):
    return T @ q / (2 * math.sqrt(27))


def report(rows):
    lines = ['# Saved affine ET query covariance response V001', '',
             'Both uT and fQtotal derivatives retain the complete changing mean dyad. Parent mixing statuses are unchanged; this posthoc response is not a Fisher/SLD or physical metric.', '',
             '| Dataset/source | tr(pair term) | tr(dyad term) | tr(total) Re +/- SE | Parent status |', '|---|---|---|---|---|']
    for row in rows:
        for j, source in enumerate(('uT', 'fQ')):
            pair = np.trace(unpack(row['values']['pair_term_u_f']).mean(axis=0)[j])
            dyad = np.trace(unpack(row['values']['dyad_term_u_f']).mean(axis=0)[j])
            # Trace SE is recomputed as a complete derived statistic below, not summed entrywise.
            trace = unpack(row['values']['all_vertex_response_trace_u_f'])[j]
            se = unpack(row['component_errors']['all_vertex_response_trace_u_f']['real_se'])[j]
            lines.append(f"| {row['id']} {source} | {pair.real:.9g} | {dyad.real:.9g} | {trace.real:.9g} +/- {se:.3g} | {row['parent_status']} |")
    lines.extend(('', '| Dataset | Conditional fixed-V S/a sector Re +/- SE | Parent status |', '|---|---|---|'))
    for row in rows:
        value = unpack(row['values']['fixed_V_conditional_sector_contact_minus_response'])
        error = unpack(row['component_errors']['fixed_V_conditional_sector_contact_minus_response']['real_se'])
        lines.append(f"| sector {row['id']} | {value.real:.9g} +/- {error:.3g} | {row['parent_status']} |")
    require(sum(line.startswith('| c') for line in lines) == 40 and sum(line.startswith('| sector ') for line in lines) == 20, 'report row census')
    lines.extend(('', 'All signed A/B matrices, average, pair/dyad terms, means, derivative means, raw cross moments and component errors are retained in JSON.',
                  'The fixed-V sector is conditional canonical contact-minus-response only. Rest/source terms and R double-prime are unknown; no complete stiffness, pressure, volume law or expansion is earned.',
                  'No H, RNG, sampler, eigenproblem, selected threshold, rerun or physical trajectory is used.', ''))
    return '\n'.join(lines)


def main():
    global CREATED, ACTIVE
    require(sys.argv[1:] == ['--execute'], 'exact --execute')
    require(not any(path.exists() for path in (CP, RESULT, REPORT, RECEIPT)), 'reserved outputs absent')
    inputs, parent = authenticate()
    CP.mkdir(); CREATED = True
    save('manifest.json', {'input_sha256': inputs, 'pid': os.getpid(), 'source_scope': 'SAVED_ONLY_ALL16_PLUS4', 'sources': ['uT', 'fQtotal']})
    event('started', input_sha256=inputs, manifest_sha256=STAGES['manifest.json'])
    rows, cache = [], {}
    for old in parent['chains']:
        ACTIVE = {'dataset': old['id'], 'phase': 'READ_PAIRED_SAVED_TRACES'}
        blocks = chain_blocks(old); cache[old['id']] = blocks
        row = summarize(blocks, old['beta'], old['id'], old)
        save(old['id'] + '.json', row); rows.append(row)
    for old in parent['conditions']:
        ACTIVE = {'dataset': 'condition' + str(old['condition']), 'phase': 'POOL_RAW_BLOCKS_BEFORE_CENTERING'}
        blocks = {key: np.concatenate([cache[cid][key] for cid in old['chain_ids']]) for key in cache[old['chain_ids'][0]]}
        row = summarize(blocks, old['beta'], 'condition' + str(old['condition']), old)
        save(row['id'] + '.json', row); rows.append(row)
    require(len(rows) == 20 and [row['block_count'] for row in rows] == [32] * 16 + [128] * 4, 'fixed dataset/block census')
    require(authenticate()[0] == inputs, 'unchanged inputs')
    ACTIVE = None
    result = {'name': NAME, 'input_sha256': inputs, 'rows': rows, 'source_order': ['uT', 'fQtotal'],
              'checks': CHECKS.copy(), 'passed': len(CHECKS), 'failed': 0,
              'status': 'SAVED_ONLY_ANALYSIS_COMPLETE_PARENT_QUALIFICATIONS_UNCHANGED', 'elapsed_seconds': time.perf_counter() - T0}
    output = report(rows)
    raw_sha = exclusive(RESULT, result); event('result_complete', filename=RESULT.name, sha256=raw_sha)
    with REPORT.open('x') as stream:
        stream.write(output); stream.flush(); os.fsync(stream.fileno())
    event('report_complete', filename=REPORT.name, sha256=sha(REPORT))
    receipt = {'result_sha256': raw_sha, 'result_canonical_sha256': hashlib.sha256(canonical(result)).hexdigest(),
               'report_sha256': sha(REPORT), 'input_sha256': inputs, 'checkpoint_sha256': STAGES.copy(),
               'journal_prefix_sha256': sha(CP / 'journal.jsonl'), 'pid': os.getpid(), 'passed': len(CHECKS), 'failed': 0,
               'status': result['status'], 'elapsed_seconds': time.perf_counter() - T0}
    digest = exclusive(RECEIPT, receipt); event('receipt_complete', filename=RECEIPT.name, sha256=digest)
    print(json.dumps({'passed': len(CHECKS), 'failed': 0, 'result_sha256': raw_sha, 'receipt_sha256': digest}), flush=True)


if __name__ == '__main__':
    T0 = time.perf_counter()
    try: main()
    except Exception as error:
        if CREATED:
            save('ERROR.json', safe({'status': 'ARITHMETIC_FAILED' if isinstance(error, ArithmeticError) else 'EXECUTION_FAILED',
                                     'error_type': type(error).__name__, 'error': str(error), 'traceback': traceback.format_exc(),
                                     'active': ACTIVE, 'checks': CHECKS.copy()}))
        print(traceback.format_exc(), file=sys.stderr); sys.exit(3)

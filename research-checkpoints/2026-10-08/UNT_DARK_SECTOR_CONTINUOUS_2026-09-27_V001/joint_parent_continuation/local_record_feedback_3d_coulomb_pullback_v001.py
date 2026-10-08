#!/usr/bin/env python3
"""NEW saved-only clamped Coulomb-sector pullback; no producer/H/RNG imports."""
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
NAME = 'LOCAL_RECORD_FEEDBACK_3D_COULOMB_PULLBACK_V001'
PARENT = 'LOCAL_RECORD_FEEDBACK_3D_QUERY_RESPONSE_RECOVERY_V001'
SOURCE = Path(__file__).resolve()
PROTOCOL = J / (NAME + '.md')
PROTOCOL_SHA = '6bf9dd0fcf1fcc865aed06581c93220ec6fd9682b3ae2f8b25db5f9f9818a7ee'
CP = J / 'local_record_feedback_3d_coulomb_pullback_v001_checkpoints'
PCP = J / 'local_record_feedback_3d_query_response_recovery_v001_checkpoints'
RESULT, REPORT, RECEIPT = (J / (NAME + suffix) for suffix in ('_RESULT.json', '_RESULT.md', '_RECEIPT.json'))
PINS = {'local_record_feedback_3d_query_response_recovery_v001.py': '618a557ca85d7bcd9d4eb9d0a1d3090cfc935e85899548383aa85c1c9b6ee358',
 PARENT + '.md': '784888d9d6ab11d462e40c402fecf86bdda4894b2e23202d021ffa852707abf1',
 PARENT + '_RESULT.json': '679c40e69cca152498af8af9763467467ad48315286bf150a45f813dce614b0a',
 PARENT + '_RESULT.md': '64860630cf647f2abb069ff5982ec01d0fb7d184d46e8edb48148054c68e0266',
 PARENT + '_RECEIPT.json': '22207c521d03eb59b1edc1d3a3505c186279729568da1ff3de9ae48aaa5d8217',
 'LOCAL_RECORD_FEEDBACK_OFFSET_ELASTANCE_COMPLETION_V001.md': 'e8233446d3de84ae2832f4f41f63aba3b09c0d6bd60f48a1c8e9842af0551c7b'}
P = np.eye(4) - np.ones((4, 4)) / 4
B = np.array([np.outer(P[:, a], P[:, b]) + np.outer(P[:, b], P[:, a]) for a, b in itertools.combinations(range(4), 2)])
T, Q = np.r_[np.ones(12), 0, 0], np.r_[np.zeros(12), 1, 1]
V_A = (T - Q) / 2
CHECKS, STAGES = [], {}
CREATED, ACTIVE = False, None


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path): return json.loads(path.read_bytes())
def canonical(value): return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
def require(passed, label):
    if not passed: raise RuntimeError('Custody: ' + label)
def unpack(value): return np.asarray(value['real']) + 1j * np.asarray(value['imag']) if isinstance(value, dict) else np.asarray(value)
def pack(value):
    a = np.asarray(value)
    return {'real': a.real.tolist(), 'imag': a.imag.tolist()} if np.iscomplexobj(a) else a.tolist()
def safe(value):
    if isinstance(value, dict): return {key: safe(v) for key, v in value.items()}
    if isinstance(value, (tuple, list)): return [safe(v) for v in value]
    if isinstance(value, (float, np.floating)) and not math.isfinite(float(value)): return {'nonfinite': repr(float(value))}
    return value


def close(label, first, second):
    residual = float(np.linalg.norm(np.asarray(first) - np.asarray(second)))
    tolerance = 3e-11 * max(1, float(np.linalg.norm(np.asarray(second))))
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
        stream.write(canonical({'event': kind, 'pid': os.getpid(), **fields}) + b'\n'); stream.flush(); os.fsync(stream.fileno())
def save(name, value):
    STAGES[name] = exclusive(CP / name, value)
    event('stage_complete', filename=name, sha256=STAGES[name])


def authenticate():
    actual = {name: sha(J / name) for name in PINS}
    require(actual == PINS, 'six direct pins')
    actual['source'], actual['protocol'] = sha(SOURCE), sha(PROTOCOL)
    require(actual['protocol'] == PROTOCOL_SHA, 'new protocol')
    parent, receipt = read(J / (PARENT + '_RESULT.json')), read(J / (PARENT + '_RECEIPT.json'))
    require(receipt['result_sha256'] == actual[PARENT + '_RESULT.json'] and receipt['report_sha256'] == actual[PARENT + '_RESULT.md'], 'query raw/report')
    require(receipt['result_canonical_sha256'] == hashlib.sha256(canonical(parent)).hexdigest(), 'query canonical')
    require(receipt['input_sha256'] == parent['input_sha256'] and receipt['failed'] == parent['failed'] == 0 and
            receipt['passed'] == parent['passed'] == len(parent['checks']) == 364 and all(c['passed'] for c in parent['checks']), '364 query controls')
    require(receipt['status'] == parent['status'] == 'SAVED_ONLY_ANALYSIS_COMPLETE_PARENT_QUALIFICATIONS_UNCHANGED', 'query status')
    expected = [f'c{i}_{start}' for i in range(4) for start in ('I01', 'I02', 'B', 'R')] + [f'condition{i}' for i in range(4)]
    require([row['id'] for row in parent['rows']] == expected and [row['block_count'] for row in parent['rows']] == [32]*16+[128]*4 and
            all(row['block_measurements'] == 32 for row in parent['rows']), 'all20 fixed blocks')
    lines = (PCP / 'journal.jsonl').read_bytes().splitlines(keepends=True)
    journal = [json.loads(line) for line in lines]
    require(hashlib.sha256(b''.join(lines[:-1])).hexdigest() == receipt['journal_prefix_sha256'] and journal[-1]['event'] == 'receipt_complete' and
            journal[-1]['sha256'] == actual[PARENT + '_RECEIPT.json'], 'query journal/prefix/receipt')
    actual[PCP.name + '/journal.jsonl'] = sha(PCP / 'journal.jsonl')
    commits = {(row.get('filename'), row.get('sha256')) for row in journal}
    for name, wanted in receipt['checkpoint_sha256'].items():
        digest = sha(PCP / name); require(digest == wanted and (name, digest) in commits, 'query checkpoint ' + name)
        actual[PCP.name + '/' + name] = digest
    manifest = read(PCP / 'manifest.json')
    require(manifest['input_sha256'] == receipt['input_sha256'] and any(row['event'] == 'started' and row['input_sha256'] == receipt['input_sha256'] and
            row['manifest_sha256'] == receipt['checkpoint_sha256']['manifest.json'] for row in journal), 'query manifest/start')
    for name, wanted in receipt['input_sha256'].items():
        path = J / ('local_record_feedback_3d_query_response_recovery_v001.py' if name == 'source' else PARENT + '.md' if name == 'protocol' else name)
        require(sha(path) == wanted, 'query inherited input ' + name)
        actual[str(path.relative_to(J))] = wanted
    joint_name = 'LOCAL_RECORD_FEEDBACK_3D_PAIR_COORDINATION_RESPONSE_V001_RESULT.json'
    require(joint_name in actual, 'joint result already authenticated by query receipt')
    joint = read(J / joint_name)
    old_rows = {row['id']: row for row in joint['chains']}
    old_rows.update({f"condition{row['condition']}": row for row in joint['conditions']})
    require(all(row['parent_status'] == old_rows[row['id']]['status'] for row in parent['rows']), 'inherited joint statuses')
    return actual, parent, old_rows


def calculate(raw, beta):
    n, q = raw['n'], raw['q']
    chi = beta * (raw['qq'] - q[:, None] * q[None, :].conj())
    cross = beta * (raw['nq'] - n[:, None] * q[None, :].conj())
    mu, mu_prime = raw['local_X_mean'], -2 * P @ cross @ V_A
    gamma = (chi[:12] @ V_A).reshape(2, 6)
    pair = np.einsum('sp,pij->sij', gamma, B)
    dyad = mu_prime[None, :, None] * mu[:, None, :] + mu[:, :, None] * mu_prime[None, None, :]
    response = pair - dyad
    mean_D = raw['local_c2_mean'].mean() - Q @ q / (4 * math.sqrt(27))
    scalar = np.stack((T, Q)) @ chi @ np.stack((T, Q)).T / 2
    chi_DD = V_A @ chi @ V_A / 2
    return {'mu': mu, 'mu_prime_a': mu_prime, 'gamma_a': gamma, 'pair_term_a': pair, 'dyad_term_a': dyad,
            'response_a_AB': response, 'response_a_average': response.mean(axis=0),
            'trace_a_AB': np.trace(response, axis1=-2, axis2=-1), 'trace_a_average': np.trace(response.mean(axis=0)),
            'mean_D_density': mean_D, 'chi_DD_density': chi_DD, 'scalar_chi_density_TQ': scalar,
            'K_D_clamped_nonidentity_canonical': 2 * mean_D - chi_DD}


def summarize(row, old):
    blocks = {key: unpack(value) / 32 for key, value in row['raw_block_sufficient_sums'].items()}
    count, beta, label = row['block_count'], row['beta'], row['id']
    require(all(len(value) == count and np.isfinite(value).all() for value in blocks.values()), 'finite raw blocks ' + label)
    raw = {key: value.mean(axis=0) for key, value in blocks.items()}
    central = calculate(raw, beta)
    replicas = [calculate({key: (count * value.mean(axis=0) - value[i]) / (count - 1) for key, value in blocks.items()}, beta) for i in range(count)]
    errors = {}
    for key in central:
        a = np.asarray([rep[key] for rep in replicas])
        errors[key] = {part + '_se': np.sqrt((count - 1) / count * ((getattr(a, part) - getattr(a, part).mean(axis=0))**2).sum(axis=0))
                       for part in (('real', 'imag') if np.iscomplexobj(a) else ('real',))}
    prior, response = row['values'], central['response_a_AB']
    close(label + '_saved_u_f_response_pullback', response, (unpack(prior['response_u_f'])[:, 0] - unpack(prior['response_u_f'])[:, 1]) / 2)
    close(label + '_saved_mean_pullback', central['mu_prime_a'], (unpack(prior['mu_prime_u_f'])[:, 0] - unpack(prior['mu_prime_u_f'])[:, 1]) / 2)
    close(label + '_saved_pair_pullback', central['gamma_a'], (unpack(prior['gamma_u_f'])[:, :, 0] - unpack(prior['gamma_u_f'])[:, :, 1]) / 2)
    close(label + '_mean_D_independent_old', central['mean_D_density'], old['estimates']['scalars'][1])
    sc = central['scalar_chi_density_TQ']
    close(label + '_chi_DD_scalar_contraction', central['chi_DD_density'], (sc[0, 0] - 2 * sc[0, 1] + sc[1, 1]) / 4)
    close(label + '_response_symmetry', response, response.swapaxes(-1, -2))
    close(label + '_response_P_projection', P @ response @ P, response)
    close(label + '_response_zero_rows', response.sum(axis=-1), np.zeros((2, 4)))
    close(label + '_response_trace', central['trace_a_AB'], -central['gamma_a'].sum(axis=1) / 2 - 2 * central['mu'] @ central['mu_prime_a'])
    close(label + '_k0_imaginary_residual', response.imag, np.zeros_like(response.imag))
    return {'id': label, 'beta': beta, 'parent_status': row['parent_status'], 'block_count': count, 'block_measurements': 32,
            'values': {key: pack(value) for key, value in central.items()},
            'component_errors': {key: {part: pack(value) for part, value in err.items()} for key, err in errors.items()},
            'raw_block_sufficient_sums': row['raw_block_sufficient_sums'],
            'clamping': 'ONLY_OFFSET_COULOMB_BLOCK_DEFORMS_OTHER_OPERATOR_STRAIN_TANGENTS_ABSENT',
            'full_circuit_sector_curvature': 'K_D+2*(alpha+1/[4*(alpha+4)])+Rraw_second/V',
            'unknowns': ['alpha>0', 'Rraw_second', 'other_rest_h_hop_source_contacts_and_mixed_responses'],
            'new_significance_threshold_or_full_stiffness_claim': False}


def report(rows):
    lines = ['# Clamped Coulomb offset-sector pullback V001', '',
             'One declared fixedq1 candidate tangent, with du/da=.5 and df/da=−.5. Full nonlinear derivatives and their block SE are recomputed together, with unchanged inherited mixing statuses.', '',
             '| Dataset | Average ET trace derivative Re +/- SE | K_D Re +/- SE | Parent status |', '|---|---|---|---|']
    for row in rows:
        v, e = row['values'], row['component_errors']
        tr, kd = unpack(v['trace_a_average']), unpack(v['K_D_clamped_nonidentity_canonical'])
        tse, kse = e['trace_a_average']['real_se'], e['K_D_clamped_nonidentity_canonical']['real_se']
        lines.append(f"| {row['id']} | {tr.real:.10g} +/- {tse:.3g} | {kd.real:.10g} +/- {kse:.3g} | {row['parent_status']} |")
    require(sum(line.startswith('| c') for line in lines) == 20, 'report all20 rows')
    lines.extend(('', 'All signed A/B and average matrices, pair/dyad terms, derivative means, raw sufficient sums and Re/Im errors are retained.',
                  'Full clamped circuit-sector expression: K_D+2[alpha+1/(4(alpha+4))]+Rraw double-prime/V. Neither alpha nor the reference derivative is selected.',
                  'Other strain contacts and mixed operator responses remain unknown. This fixed-beta canonical sector is not complete mechanical stiffness, stability, pressure, volume or expansion evidence.',
                  'No physical metric/Fisher/SLD, inverse, selected significance, sampler/RNG/H replay or automatic continuation is inferred.', ''))
    return '\n'.join(lines)


def main():
    global CREATED, ACTIVE
    require(sys.argv[1:] == ['--execute'], 'exact --execute argument')
    require(not any(path.exists() for path in (CP, RESULT, REPORT, RECEIPT)), 'reserved outputs absent')
    inputs, parent, old = authenticate(); CP.mkdir(); CREATED = True
    save('manifest.json', {'input_sha256': inputs, 'pid': os.getpid(), 'source_direction': V_A.tolist(), 'all20_saved_datasets': True})
    event('started', input_sha256=inputs, manifest_sha256=STAGES['manifest.json'])
    rows = []
    for prior in parent['rows']:
        ACTIVE = {'dataset': prior['id'], 'phase': 'SAVED_RAW_BLOCK_PULLBACK'}
        row = summarize(prior, old[prior['id']]); save(row['id'] + '.json', row); rows.append(row)
    require(authenticate()[0] == inputs, 'unchanged inputs before seal'); ACTIVE = None
    result = {'name': NAME, 'input_sha256': inputs, 'rows': rows, 'checks': CHECKS.copy(), 'passed': len(CHECKS), 'failed': 0,
              'status': 'CLAMPED_SAVED_ONLY_PULLBACK_PARENT_QUALIFICATIONS_UNCHANGED', 'elapsed_seconds': time.perf_counter() - T0}
    output = report(rows); raw_sha = exclusive(RESULT, result); event('result_complete', filename=RESULT.name, sha256=raw_sha)
    with REPORT.open('x') as stream: stream.write(output); stream.flush(); os.fsync(stream.fileno())
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
        if CREATED: save('ERROR.json', safe({'error': str(error), 'error_type': type(error).__name__, 'traceback': traceback.format_exc(),
                                           'active': ACTIVE, 'checks': CHECKS.copy(), 'status': 'ARITHMETIC_FAILED' if isinstance(error, ArithmeticError) else 'EXECUTION_FAILED'}))
        print(traceback.format_exc(), file=sys.stderr); sys.exit(3)

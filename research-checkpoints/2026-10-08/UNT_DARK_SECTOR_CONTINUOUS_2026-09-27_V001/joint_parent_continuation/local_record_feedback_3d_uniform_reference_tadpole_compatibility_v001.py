#!/usr/bin/env python3
"""NEW saved-only two-tadpole compatibility; no H, RNG or producer replay."""
import os
for _name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS'):
    os.environ[_name] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
from pathlib import Path
import hashlib
import json
import math
import sys
import time
import traceback
import numpy as np

J = Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation')
NAME = 'LOCAL_RECORD_FEEDBACK_3D_UNIFORM_REFERENCE_TADPOLE_COMPATIBILITY_V001'
PARENT = 'LOCAL_RECORD_FEEDBACK_3D_LOCAL_ENERGY_SOURCE_RESPONSE_V001'
ACCEPT = PARENT + '_AUTHORED_ACCEPTANCE_V002'
SOURCE = Path(__file__).resolve()
PROTOCOL = J / (NAME + '.md')
PROTOCOL_SHA = '2d393f1a8e728ec216c3cd4f32a8efa4dd5d96f7dce247779bba57551cdfbe86'
CP = J / 'local_record_feedback_3d_uniform_reference_tadpole_compatibility_v001_checkpoints'
PCP = J / 'local_record_feedback_3d_local_energy_source_response_v001_checkpoints'
RESULT, REPORT, RECEIPT, ERROR = (J / (NAME + s) for s in ('_RESULT.json', '_RESULT.md', '_RECEIPT.json', '_ERROR.json'))
PINS = {
 'LOCAL_RECORD_FEEDBACK_COMPLETE_STRAIN_SOURCE_CONTRACT_V001.md': 'cc363bf1885917a9beededadb8d49b5d898c951bd54a1e2d2ad6ce5003ebaf63',
 'LOCAL_RECORD_FEEDBACK_COMMON_COFRAME_OPTICAL_BINDING_V001.md': '585d9a20fb0c2bec5dccd3f8dac726a5b57b8b0c9cdad90744f4ce7d5f22c9c4',
 'LOCAL_RECORD_FEEDBACK_COMMON_FIELD_TWO_POTENTIAL_CLOSURE_V001.md': '0e4c9a8e47d8570c53761ba5d605764f145ffdc398c52d047b5f39f63c143459',
 'LOCAL_RECORD_FEEDBACK_WEAK_FIELD_CONSTRAINT_AND_BULK_SOURCE_JOIN_V001.md': '0ae61eb4f616133ad07fbca38d33b6a6193b404f00dcd9e76cbf09fcf5d635ab',
 'local_record_feedback_3d_local_energy_source_response_v001.py': 'cc10b0836b9105192e210a5e17d877044fa2a64fa0ba826863bebcb521924167',
 PARENT + '.md': 'ed426216edd6788537c3149d0a85c5d26d670ac1d7279a085bdf387435059f58',
 PARENT + '_RESULT.json': '389df141d19e496c5989d114b67025605f248c4b1aad80f145400e2395a5cfca',
 PARENT + '_RESULT.md': 'be19640343895de1624c1c7963abe9987fb6da978a7feb33366854762661bb2e',
 PARENT + '_RECEIPT.json': '7e67d3ce3c2f9f4cb8f76d6f3f69dfad1427dd550a2e99339067051292148e33',
 'local_record_feedback_3d_local_energy_source_response_v001_saved_authored_acceptance_v002.py': 'fb81052f8c9ead0f1deccc432986cf185968329df3c09f44e9670063a3d90c73',
 ACCEPT + '.json': '77d307619ebdff976dc6e1c47b25af129f641df83e12a81bf6a37aedd0b84399',
 ACCEPT + '.md': '18cece480c9445f5c2004332d6e68b504f09b6c7c83b204bf5a3c2332fc156dc',
 PARENT + '_AUTHORED_ACCEPTANCE_RECEIPT_V002.json': '85d067a77e22bb14a2890db9e76218ba7c482bc68bc5ded2d5df086c1ec1af2a',
 'LOCAL_RECORD_FEEDBACK_3D_CHARGING_TWO_POTENTIAL_SOURCE_V001.md': '5a9ed4a929f4076eaa48edf4a6240b0eb1edae0de7ae9b983a710f27887541eb',
 'local_record_feedback_3d_charging_two_potential_source_v001.py': '0a7e4d915c2556e7f7b92e51cf10a0cb315af6cb4097f1f4ddd959b181f6211b',
 'LOCAL_RECORD_FEEDBACK_TOLMAN_AND_SPATIAL_STRESS_IDENTIFIABILITY_V001.md': '699bef32d88cedde18d7ca1157b210dce14f8a55859235bc88eb28141125cfd3'}
IDS = [f'c{i}_{s}' for i in range(2) for s in ('I01', 'I02', 'B', 'R')] + ['condition0', 'condition1']
MODES = np.array(((0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)))
L_D = np.zeros((2, 14)); L_D[0, :6] = .5; L_D[1, 6:12] = .5; L_D[0, 12] = L_D[1, 13] = -.5
RAW_SHAPES = {'mean_Q': (7, 14), 'mean_E_dynamic': (7, 2), 'mean_D': (7, 2)}
COEFFICIENTS = ('e', 'd', 'R=3e+d', 'ell_req=(d-e)/4')
COMPONENT_ORDER = [key + '_' + sub for key in COEFFICIENTS for sub in ('A', 'B')]
CHECKS, INPUTS, STAGES = [], {}, {}
ACTIVE, CREATED = None, False


def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read(path): return json.loads(Path(path).read_bytes())
def canonical(obj): return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
def unpack(value): return np.asarray(value['real']) + 1j * np.asarray(value['imag']) if isinstance(value, dict) else np.asarray(value)
def pack(value):
    a = np.asarray(value)
    return {'real': a.real.tolist(), 'imag': a.imag.tolist()} if np.iscomplexobj(a) else a.tolist()
def safe(value):
    if isinstance(value, dict): return {k: safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)): return [safe(v) for v in value]
    if isinstance(value, (np.integer,)): return int(value)
    if isinstance(value, (float, np.floating)): return float(value) if math.isfinite(float(value)) else {'nonfinite': repr(float(value))}
    return value

def require(passed, label):
    CHECKS.append({'label': label, 'passed': bool(passed)})
    if not passed: raise RuntimeError(label)

def close(label, actual, expected):
    a, b = np.asarray(actual), np.asarray(expected)
    error = float(np.linalg.norm(a - b)); tolerance = 3e-11 * max(1, float(np.linalg.norm(b)))
    passed = bool(np.isfinite(a).all() and np.isfinite(b).all() and math.isfinite(error) and error <= tolerance)
    CHECKS.append(safe({'label': label, 'passed': passed, 'residual': error, 'tolerance': tolerance}))
    if not passed: raise ArithmeticError(label)

def register(path, wanted):
    path = Path(path).resolve(); key = str(path)
    require(sha(path) == wanted, 'input seal ' + key)
    require(key not in INPUTS or INPUTS[key] == wanted, 'input alias ' + key)
    INPUTS[key] = wanted

def recheck(counting=True):
    for path, wanted in INPUTS.items():
        if counting: require(sha(path) == wanted, 'unchanged input ' + path)
        elif sha(path) != wanted: raise RuntimeError('post-output input changed ' + path)

def exclusive(path, obj):
    with Path(path).open('xb') as f:
        f.write(canonical(safe(obj)) + b'\n'); f.flush(); os.fsync(f.fileno())
    return sha(path)

def event(kind, **fields):
    with (CP / 'journal.jsonl').open('ab') as f:
        f.write(canonical({'event': kind, 'pid': os.getpid(), 'elapsed_seconds': time.perf_counter() - T0, **fields}) + b'\n')
        f.flush(); os.fsync(f.fileno())

def save(name, obj):
    digest = exclusive(CP / name, obj); STAGES[name] = digest
    event('stage_complete', filename=name, sha256=digest)

def bundle(name, arrays):
    with (CP / name).open('xb') as f:
        np.savez_compressed(f, **arrays); f.flush(); os.fsync(f.fileno())
    STAGES[name] = sha(CP / name); event('stage_complete', filename=name, sha256=STAGES[name])


def authenticate():
    for name, wanted in PINS.items(): register(J / name, wanted)
    register(PROTOCOL, PROTOCOL_SHA); register(SOURCE, sha(SOURCE))
    a, ar = read(J / (ACCEPT + '.json')), read(J / (PARENT + '_AUTHORED_ACCEPTANCE_RECEIPT_V002.json'))
    require(a['audit_status'] == ar['audit_status'] == 'PASS' and a['failed_assertions'] == 0, 'accepted V002 PASS')
    require(a['assertions'] == ar['assertions'] == 5070671 and a['check_count'] == len(a['checks']) == 18697 and all(c['passed'] for c in a['checks']), 'accepted full arithmetic census')
    require(ar['audit_sha256'] == PINS[ACCEPT + '.json'] and ar['report_sha256'] == PINS[ACCEPT + '.md'], 'acceptance raw/report seals')
    require(a['source_sha256'] == ar['source_sha256'] == PINS['local_record_feedback_3d_local_energy_source_response_v001_saved_authored_acceptance_v002.py'], 'acceptance source')
    require(a['input_sha256'] == ar['input_sha256'] and len(a['input_sha256']) == 1206, 'all accepted custody inputs')
    require(a['preserved_failed_attempt_sha256'] == ar['preserved_failed_attempt_sha256'], 'preserved V001 failure ancestry')
    for path, wanted in a['input_sha256'].items(): register(path, wanted)
    p, r = read(J / (PARENT + '_RESULT.json')), read(J / (PARENT + '_RECEIPT.json'))
    require(r['result_sha256'] == a['result_sha256'] == ar['result_sha256'] == PINS[PARENT + '_RESULT.json'] and a['parent_receipt_sha256'] == PINS[PARENT + '_RECEIPT.json'], 'producer and accepted result identity')
    require(r['report_sha256'] == PINS[PARENT + '_RESULT.md'] and r['result_canonical_sha256'] == hashlib.sha256(canonical(p)).hexdigest(), 'producer report/canonical')
    require(p['input_sha256'] == r['input_sha256'], 'producer inputs')
    for path, wanted in p['input_sha256'].items(): register(path, wanted)
    require(p['failed'] == r['failed'] == 0 and p['passed'] == r['passed'] == p['check_count'] == r['check_count'] == len(p['checks']) == 197470 and all(c['passed'] for c in p['checks']), 'producer complete checks')
    require(p['status'] == r['status'] == 'FINITE_GRID_LOCAL_ENERGY_SOURCE_DIAGNOSTICS_PASSED', 'producer status retained')
    require(p['mode_order'] == MODES.tolist() and [c['id'] for c in p['chains']] == IDS[:8] and [c['condition'] for c in p['conditions']] == [0, 1], 'ordered ten/seven census')
    require((r['chain_count'], r['condition_count'], r['mode_count'], r['checkpoint_bundle_count']) == (8, 2, 7, 80), 'producer receipt census')
    lines = (PCP / 'journal.jsonl').read_bytes().splitlines(keepends=True); es = [json.loads(x) for x in lines]
    require(len(es) == 191 and hashlib.sha256(b''.join(lines[:-1])).hexdigest() == r['journal_prefix_sha256'], 'producer journal/prefix')
    require(es[-1]['event'] == 'receipt_complete' and es[-1]['sha256'] == PINS[PARENT + '_RECEIPT.json'] and [e['event'] for e in es[-3:]] == ['result_complete', 'report_complete', 'receipt_complete'], 'producer complete final commits')
    require(es[-3]['sha256'] == r['result_sha256'] and es[-2]['sha256'] == r['report_sha256'], 'producer result/report commits')
    register(PCP / 'journal.jsonl', sha(PCP / 'journal.jsonl'))
    require(len(r['checkpoint_sha256']) == 172 and set(r['checkpoint_sha256']) == {x.name for x in PCP.iterdir() if x.name != 'journal.jsonl'}, 'all172 producer checkpoint files')
    commits = {(e.get('filename'), e.get('sha256')) for e in es}
    for name, wanted in r['checkpoint_sha256'].items():
        register(PCP / name, wanted)
        if name != 'manifest.json': require((name, wanted) in commits, 'producer checkpoint commit ' + name)
    m = read(PCP / 'manifest.json'); starts = [e for e in es if e['event'] == 'started']
    require(len(starts) == 1 and starts[0] == es[0] and starts[0]['manifest_sha256'] == r['checkpoint_sha256']['manifest.json'], 'producer exact start/manifest')
    require(m['input_sha256'] == p['input_sha256'] == starts[0]['input_sha256'] and m['pid'] == p['pid'] == r['pid'] == 73342 and all(e['pid'] == 73342 for e in es), 'producer PID/full inputs')
    rows = p['chains'] + p['conditions']
    for label, row in zip(IDS, rows): require(read(PCP / (label + '_complete.json')) == row, 'named checkpoint duplicate ' + label)
    return p, rows, a['authorship_scope']


def calculate(raw, label):
    q, e, d = raw['mean_Q'], raw['mean_E_dynamic'], raw['mean_D']
    expected_d = q @ L_D.T; expected_d[0] += math.sqrt(27)
    close(label + '_D_Q_mean_all7', d, expected_d)
    primitive = np.stack((e[0], d[0])) / math.sqrt(27)
    close(label + '_Hermitian_k0_mean_imaginary', primitive.imag, np.zeros((2, 2)))
    er, dr = primitive[0].real, primitive[1].real
    coefficients = np.stack((er, dr, 3 * er + dr, (dr - er) / 4))
    out = {'mean_E_dynamic': e, 'mean_D': d, 'primitive_k0_complex': primitive,
           'coefficients': coefficients, 'common_mean': coefficients.mean(axis=1),
           'A_minus_B': coefficients[:, 0] - coefficients[:, 1]}
    close(label + '_compatibility_identity', coefficients[2], 3 * coefficients[0] + coefficients[1])
    close(label + '_single_reference_identity', 4 * coefficients[3], coefficients[1] - coefficients[0])
    require(all(np.isfinite(v).all() for v in out.values()), label + '_all_finite')
    return out


def errors_from(replicas):
    count = len(next(iter(replicas.values()))); factor = (count - 1) / count
    return {key: {'real_se': np.sqrt(factor * ((v.real - v.real.mean(axis=0)) ** 2).sum(axis=0)),
                  'imag_se': np.sqrt(factor * ((v.imag - v.imag.mean(axis=0)) ** 2).sum(axis=0))}
            for key, v in replicas.items()}


def covariance(replicas):
    values = replicas.reshape(len(replicas), -1).real
    centered = values - values.mean(axis=0)
    return (len(values) - 1) / len(values) * centered.T @ centered


def summarize(prior, label, count):
    is_chain = not label.startswith('condition')
    raw_parent = prior['block_raw_moments'] if is_chain else prior['pooled_block_raw_moments']
    counts = prior['block_counts'] if is_chain else prior['pooled_block_counts']
    require(prior['beta'] == 4 and prior['M'] == (64 if label in IDS[:4] + ['condition0'] else 128), 'fixed beta/M ' + label)
    require(counts == [32] * count, 'fixed block census ' + label)
    blocks = {key: unpack(raw_parent[key]) for key in RAW_SHAPES}
    require(all(v.shape == (count,) + RAW_SHAPES[k] and np.isfinite(v).all() for k, v in blocks.items()), 'raw finite shapes ' + label)
    raw = {k: v.mean(axis=0) for k, v in blocks.items()}; central = calculate(raw, label + '_central')
    collected = {key: [] for key in central}
    for index in range(count):
        global ACTIVE
        ACTIVE = {'dataset': label, 'phase': 'DELETE_BLOCK', 'block_index': index}
        leave = {key: (count * raw[key] - value[index]) / (count - 1) for key, value in blocks.items()}
        for key, value in calculate(leave, label + '_delete' + str(index)).items(): collected[key].append(value)
    replicas = {key: np.asarray(values) for key, values in collected.items()}; errors = errors_from(replicas)
    for key in ('mean_E_dynamic', 'mean_D'):
        close(label + '_parent_central_' + key, central[key], unpack(prior['estimates'][key]))
        for part in ('real_se', 'imag_se'):
            close(label + '_parent_error_' + key + '_' + part, errors[key][part], unpack(prior['component_errors'][key][part]))
    joint = covariance(replicas['coefficients'])
    common_cov, optical_cov = covariance(replicas['common_mean']), covariance(replicas['A_minus_B'])
    common_map, optical_map = np.zeros((4, 8)), np.zeros((4, 8))
    for index in range(4):
        common_map[index, 2 * index:2 * index + 2] = .5
        optical_map[index, 2 * index:2 * index + 2] = (1, -1)
    close(label + '_paired_common_covariance', common_cov, common_map @ joint @ common_map.T)
    close(label + '_paired_optical_covariance', optical_cov, optical_map @ joint @ optical_map.T)
    close(label + '_joint_component_error', np.diag(joint).reshape(4, 2), errors['coefficients']['real_se'] ** 2)
    require(all(np.isfinite(v).all() for entry in errors.values() for v in entry.values()), 'all errors finite ' + label)
    arrays = {'mode_order': MODES, 'D_from_Q_matrix': L_D, 'joint_covariance': joint,
              'common_covariance': common_cov, 'A_minus_B_covariance': optical_cov}
    arrays.update({'raw_' + key: value for key, value in blocks.items()})
    arrays.update({'central_' + key: value for key, value in central.items()})
    arrays.update({'replica_' + key: value for key, value in replicas.items()})
    row = {'id': label, 'beta': 4, 'M': prior['M'], 'parent_status': prior['status'], 'block_count': count,
           'block_measurements': 32, 'coefficient_order': list(COEFFICIENTS), 'joint_component_order': COMPONENT_ORDER,
           'central_intercepts': {key: pack(v) for key, v in central.items()},
           'component_errors': {key: {part: pack(v) for part, v in entry.items()} for key, entry in errors.items()},
           'joint_covariance': pack(joint), 'common_covariance': pack(common_cov), 'A_minus_B_covariance': pack(optical_cov),
           'symbolic_c0_slopes': {'eta_tadpole': [1, 1], 'psi_tadpole': [1, 1], 'compatibility': [4, 4], 'ell_req': [0, 0]},
           'symbolic_ell_slopes': {'eta_tadpole': [1, 1], 'psi_tadpole': [-3, -3],
                                  'direct_Npsi': [-3, -3], 'direct_psipsi_metric': [3, 3], 'direct_psipsi_affine': [6, 6]},
           'replicas': count, 'dataset_bundle': label + '.npz', 'physical_compatibility_or_sign_gate': False}
    return row, arrays


def format_value(value, se): return f'{float(value):.12g} +/- {float(se):.4g}'


def report(rows):
    lines = ['# Single uniform reference: two-tadpole compatibility V001', '',
      'All numbers are c0=0 intercepts of the declared charging-only/clamped-flip source. One global c0 and one uniform ell remain symbolic; no value or physical compatibility is selected.', '',
      '| Dataset | A/B/common/A-minus-B | e | d | 3e+d | (d-e)/4 |', '|---|---|---|---|---|---|']
    table_rows = 0
    for row in rows:
        central, errors = row['central_intercepts'], row['component_errors']
        for key, index, text in (('coefficients', 0, 'A'), ('coefficients', 1, 'B'), ('common_mean', None, 'common'), ('A_minus_B', None, 'A-B')):
            values, se = unpack(central[key]), unpack(errors[key]['real_se'])
            if index is not None: values, se = values[:, index], se[:, index]
            lines.append('| ' + row['id'] + ' | ' + text + ' | ' + ' | '.join(format_value(v, s) for v, s in zip(values, se)) + ' |'); table_rows += 1
    require(len(rows) == 10 and table_rows == 40 and sum(r['replicas'] for r in rows) == 512, 'report10/40/512 census')
    lines.extend(('', 'Both local balances would require 3e_s+d_s+4c0=0 and a COMMON ell=(d_s-e_s)/4 for A/B; averaging does not supply that condition. The table is a diagnostic, not a flatness/sign test or fitted reference.',
      'Lossless NPZ/JSON pairs retain all raw means, 512 paired replicas, joint 8x8 covariance, common/optical covariance and full complex k0 controls/errors. Each table error is a correlated delete-block component SE.',
      'Reference source ell N(1-2psi)^(3/2) owns Npsi=-3ell and psipsi=3ell, compared with 6ell in the affine coframe. If all flat balances hold, direct total Npsi=0 and metric/affine spatial contacts agree at 4J; connected covariances and other action terms remain.',
      'Parent finite-grid dispositions and old beta8/inverse refusals remain. No c0, ell, physical self/vacuum/volume, stable background, total-G matching or dark-energy action is adopted. The fixed-coordinate bath is distinct from the whole-action proper-bath guard.', ''))
    return '\n'.join(lines)


def main():
    global CREATED, ACTIVE
    require(sys.argv[1:] == ['--execute'], 'exact --execute argument')
    require(not any(path.exists() for path in (CP, RESULT, REPORT, RECEIPT, ERROR)), 'exclusive outputs absent')
    parent, priors, authorship = authenticate(); CP.mkdir(); CREATED = True
    manifest = {'name': NAME, 'pid': os.getpid(), 'input_sha256': INPUTS.copy(), 'source_sha256': sha(SOURCE),
                'protocol_sha256': PROTOCOL_SHA, 'dataset_order': IDS, 'coefficient_order': list(COEFFICIENTS),
                'source_chart': 'N=1+eta,a=sqrt(1-2psi); charging plus psi-clamped flips; symbolic ell N a^3',
                'c0_and_ell': 'GLOBAL_SYMBOLIC_UNSELECTED', 'replica_count': 512}
    STAGES['manifest.json'] = exclusive(CP / 'manifest.json', manifest)
    event('started', input_sha256=INPUTS.copy(), manifest_sha256=STAGES['manifest.json'])
    rows = []
    for index, (label, prior) in enumerate(zip(IDS, priors)):
        ACTIVE = {'dataset': label, 'phase': 'PAIRED_RAW_MEAN_RECOVERY'}
        row, arrays = summarize(prior, label, 32 if index < 8 else 128)
        bundle(label + '.npz', arrays); row['bundle_sha256'] = STAGES[label + '.npz']
        save(label + '.json', row); rows.append(row)
    ACTIVE = {'phase': 'FINAL_INPUT_AND_REPORT_GUARDS'}; recheck(); output = report(rows)
    require(len(STAGES) == 21 and len((CP / 'journal.jsonl').read_bytes().splitlines()) == 21, 'checkpoint/journal prefix census')
    result = {'name': NAME, 'pid': os.getpid(), 'status': 'SYMBOLIC_REFERENCE_TADPOLE_SAVED_DIAGNOSTICS_PASSED',
              'input_sha256': INPUTS.copy(), 'source_sha256': sha(SOURCE), 'protocol_sha256': PROTOCOL_SHA,
              'parent_status': parent['status'], 'parent_beta8_refusals': parent['parent_condition_statuses'],
              'parent_covariance_inverse': parent['covariance_inverse'], 'parent_authorship_scope': authorship,
              'rows': rows, 'checks': CHECKS.copy(), 'passed': len(CHECKS), 'failed': 0, 'replica_count': 512,
              'dataset_order': IDS, 'coefficient_order': list(COEFFICIENTS), 'c0_and_ell': 'GLOBAL_SYMBOLIC_UNSELECTED',
              'physical_compatibility_or_sign_gate': False, 'elapsed_seconds': time.perf_counter() - T0}
    ACTIVE = {'phase': 'OUTPUT_SEAL'}
    raw_sha = exclusive(RESULT, result); event('result_complete', filename=RESULT.name, sha256=raw_sha)
    with REPORT.open('x') as f: f.write(output); f.flush(); os.fsync(f.fileno())
    event('report_complete', filename=REPORT.name, sha256=sha(REPORT)); recheck(counting=False)
    receipt = {'status': result['status'], 'pid': os.getpid(), 'result_sha256': raw_sha,
               'result_canonical_sha256': hashlib.sha256(canonical(result)).hexdigest(), 'report_sha256': sha(REPORT),
               'source_sha256': sha(SOURCE), 'protocol_sha256': PROTOCOL_SHA, 'input_sha256': INPUTS.copy(),
               'checkpoint_sha256': STAGES.copy(), 'journal_prefix_sha256': sha(CP / 'journal.jsonl'),
               'passed': result['passed'], 'failed': 0, 'check_count': len(CHECKS), 'dataset_count': 10,
               'replica_count': 512, 'table_row_count': 40, 'checkpoint_file_count': 21, 'journal_event_count_after_receipt': 24,
               'elapsed_seconds': time.perf_counter() - T0}
    digest = exclusive(RECEIPT, receipt); event('receipt_complete', filename=RECEIPT.name, sha256=digest); ACTIVE = None
    print(json.dumps({'status': result['status'], 'passed': result['passed'], 'failed': 0, 'result_sha256': raw_sha, 'receipt_sha256': digest}), flush=True)


if __name__ == '__main__':
    T0 = time.perf_counter()
    try: main()
    except Exception as exc:
        failure = {'status': 'EXECUTION_ERROR_PRESERVED', 'pid': os.getpid(), 'exception': repr(exc), 'traceback': traceback.format_exc(),
                   'active': ACTIVE, 'checkpoint_directory_created': CREATED, 'checkpoint_sha256': STAGES.copy(),
                   'input_sha256': INPUTS.copy(), 'checks': CHECKS.copy(), 'passed': sum(c['passed'] for c in CHECKS),
                   'failed': sum(not c['passed'] for c in CHECKS), 'source_sha256': sha(SOURCE), 'protocol_sha256': PROTOCOL_SHA}
        if not ERROR.exists(): exclusive(ERROR, failure)
        print(json.dumps({'status': 'EXECUTION_ERROR_PRESERVED', 'exception': repr(exc)}), flush=True); sys.exit(3)

#!/usr/bin/env python3
"""NEW saved-only conditional charging spatial source; no H, RNG or producer replay."""
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
NAME = 'LOCAL_RECORD_FEEDBACK_3D_CHARGING_TWO_POTENTIAL_SOURCE_V001'
PARENT = 'LOCAL_RECORD_FEEDBACK_3D_LOCAL_ENERGY_SOURCE_RESPONSE_V001'
ACCEPT = PARENT + '_AUTHORED_ACCEPTANCE_V002'
SOURCE = Path(__file__).resolve()
PROTOCOL = J / (NAME + '.md')
PROTOCOL_SHA = '5a9ed4a929f4076eaa48edf4a6240b0eb1edae0de7ae9b983a710f27887541eb'
CP = J / 'local_record_feedback_3d_charging_two_potential_source_v001_checkpoints'
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
 PARENT + '_AUTHORED_ACCEPTANCE_RECEIPT_V002.json': '85d067a77e22bb14a2890db9e76218ba7c482bc68bc5ded2d5df086c1ec1af2a'}
IDS = [f'c{i}_{s}' for i in range(2) for s in ('I01', 'I02', 'B', 'R')] + ['condition0', 'condition1']
MODES = np.array(((0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)))
L_D = np.zeros((2, 14)); L_D[0, :6] = .5; L_D[1, 6:12] = .5; L_D[0, 12] = L_D[1, 13] = -.5
PLANE = np.stack((np.ones(7), np.exp(-1j * math.pi * MODES.sum(axis=1) / 6)), axis=1) / math.sqrt(2)
RAW_SHAPES = {'mean_Q': (7, 14), 'second_Q': (7, 14, 14), 'mean_E_dynamic': (7, 2),
              'second_E_dynamic': (7, 2, 2), 'second_QE_dynamic': (7, 14, 2),
              'mean_D': (7, 2), 'second_D': (7, 2, 2), 'score_contact_C2': (7, 2, 2)}
ANCHORS = ('mean_D', 'chi_QQ', 'chi_QE', 'chi_EQ', 'R_NN')
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


def plane(matrix): return np.einsum('ki,kij,kj->k', PLANE.conj(), matrix, PLANE)

def calculate(raw, beta, label):
    q, e, d = raw['mean_Q'], raw['mean_E_dynamic'], raw['mean_D']
    chiqq = beta * (raw['second_Q'] - q[:, :, None] * q[:, None, :].conj())
    chiee = beta * (raw['second_E_dynamic'] - e[:, :, None] * e[:, None, :].conj())
    chiqe = beta * (raw['second_QE_dynamic'] - q[:, :, None] * e[:, None, :].conj())
    chieq = chiqe.conj().transpose(0, 2, 1)
    chied, chide = chieq @ L_D.T, L_D @ chiqe
    chidd = L_D @ chiqq @ L_D.T
    directdd = beta * (raw['second_D'] - d[:, :, None] * d[:, None, :].conj())
    expected_d = q @ L_D.T; expected_d[0] += math.sqrt(27)
    close(label + '_D_Q_mean', d, expected_d); close(label + '_DD_direct_Q', chidd, directdd)
    close(label + '_zero_mean_D_imaginary', d[0].imag, np.zeros(2))
    close(label + '_zero_mean_E_imaginary', e[0].imag, np.zeros(2))
    jd = np.diag(d[0].real / math.sqrt(27)); contact = np.broadcast_to(jd, (7, 2, 2)).copy()
    nn = -chiee - raw['score_contact_C2'] / beta
    b, br, dm, da = contact - chied, contact - chide, 3 * contact - chidd, 2 * contact - chidd
    source = np.concatenate((np.concatenate((nn, b), axis=2), np.concatenate((br, dm), axis=2)), axis=1)
    out = {'mean_Q': q, 'mean_E_dynamic': e, 'mean_D': d, 'chi_QQ': chiqq, 'chi_QE': chiqe,
           'chi_EQ': chieq, 'chi_EE': chiee, 'chi_ED': chied, 'chi_DE': chide,
           'chi_DD': chidd, 'chi_DD_direct': directdd, 'score_contact_C2': raw['score_contact_C2'],
           'J_contact_intercept': contact, 'R_NN': nn, 'b_intercept': b, 'b_reverse_intercept': br,
           'd_metric_intercept': dm, 'd_affine_intercept': da, 'source4_intercept': source,
           'eta_local_mean_intercept': e[0].real / math.sqrt(27), 'psi_local_mean_intercept': d[0].real / math.sqrt(27)}
    for key in ('R_NN', 'chi_DD', 'd_metric_intercept', 'd_affine_intercept', 'source4_intercept'):
        close(label + '_Hermitian_' + key, out[key], out[key].conj().transpose(0, 2, 1))
    close(label + '_b_reverse', br, b.conj().transpose(0, 2, 1)); close(label + '_chart_contact_difference', dm - da, contact)
    for key, value in tuple(out.items()):
        if value.shape[0] == 7:
            close(label + '_negative_character_' + key, value[[2, 4, 6]], value[[1, 3, 5]].conj())
    for key in ('R_NN', 'b_intercept', 'b_reverse_intercept', 'd_metric_intercept', 'd_affine_intercept', 'chi_ED', 'chi_DE', 'chi_DD'):
        out['plane_' + key] = plane(out[key])
    close(label + '_plane_reverse', out['plane_b_reverse_intercept'], out['plane_b_intercept'].conj())
    require(all(np.isfinite(v).all() for v in out.values()), label + '_all_finite')
    return out


def errors_from(replicas):
    count = len(next(iter(replicas.values()))); factor = (count - 1) / count
    return {key: {'real_se': np.sqrt(factor * ((v.real - v.real.mean(axis=0)) ** 2).sum(axis=0)),
                  'imag_se': np.sqrt(factor * ((v.imag - v.imag.mean(axis=0)) ** 2).sum(axis=0))}
            for key, v in replicas.items()}


def summarize(prior, label, block_count):
    raw_parent = prior['block_raw_moments'] if label.startswith('c') and not label.startswith('condition') else prior['pooled_block_raw_moments']
    counts = prior['block_counts'] if label.startswith('c') and not label.startswith('condition') else prior['pooled_block_counts']
    beta = prior['beta']; require(beta == 4 and prior['M'] == (64 if label in IDS[:4] + ['condition0'] else 128), 'fixed beta/M ' + label)
    require(counts == [32] * block_count, 'all fixed 32-measurement blocks ' + label)
    blocks = {key: unpack(raw_parent[key]) for key in RAW_SHAPES}
    require(all(v.shape == (block_count,) + RAW_SHAPES[k] and np.isfinite(v).all() for k, v in blocks.items()), 'finite raw shapes ' + label)
    raw = {k: v.mean(axis=0) for k, v in blocks.items()}; central = calculate(raw, beta, label + '_central')
    reps = {key: [] for key in central}
    for index in range(block_count):
        global ACTIVE
        ACTIVE = {'dataset': label, 'phase': 'DELETE_BLOCK', 'block_index': index}
        leave = {key: (block_count * raw[key] - value[index]) / (block_count - 1) for key, value in blocks.items()}
        for key, value in calculate(leave, beta, label + '_delete' + str(index)).items(): reps[key].append(value)
    replicas = {key: np.asarray(value) for key, value in reps.items()}; errors = errors_from(replicas)
    require(all(np.isfinite(v).all() for value in errors.values() for v in value.values()), 'all finite component errors ' + label)
    for key in ANCHORS:
        close(label + '_parent_central_' + key, central[key], unpack(prior['estimates'][key]))
        for part in ('real_se', 'imag_se'):
            close(label + '_parent_error_' + key + '_' + part, errors[key][part], unpack(prior['component_errors'][key][part]))
    slope = np.broadcast_to(np.eye(2), (7, 2, 2)).copy(); slopes = {'b': slope, 'b_reverse': slope, 'd_metric': 3 * slope, 'd_affine': 2 * slope,
              'R_NN': np.zeros_like(slope), 'eta_local_mean': np.ones(2), 'psi_local_mean': np.ones(2), 'homogeneous_mode_mean': np.full(2, math.sqrt(27))}
    mean_slope = np.zeros((7, 2)); mean_slope[0] = math.sqrt(27)
    slopes.update({'mean_E_dynamic': mean_slope, 'mean_D': mean_slope, 'J_contact': slope,
                   'source4': np.concatenate((np.concatenate((np.zeros_like(slope), slope), axis=2),
                                              np.concatenate((slope, 3 * slope), axis=2)), axis=1)})
    close(label + '_homogeneous_scalar_mean_slope', PLANE[0].conj() @ mean_slope[0], math.sqrt(54))
    for key, value in (('b', 1), ('b_reverse', 1), ('d_metric', 3), ('d_affine', 2)):
        close(label + '_proper_plane_slope_' + key, plane(slopes[key]), np.full(7, value))
    arrays = {'mode_order': MODES, 'proper_plane_source_column': PLANE, 'D_from_Q_matrix': L_D}
    arrays.update({'raw_' + key: value for key, value in blocks.items()})
    arrays.update({'central_' + key: value for key, value in central.items()})
    arrays.update({'replica_' + key: value for key, value in replicas.items()})
    arrays.update({'c0_slope_' + key: value for key, value in slopes.items()})
    row = {'id': label, 'beta': beta, 'M': prior['M'], 'parent_status': prior['status'], 'block_count': block_count, 'block_measurements': 32,
           'central_intercepts': {key: pack(v) for key, v in central.items()},
           'component_errors': {key: {part: pack(v) for part, v in value.items()} for key, value in errors.items()},
           'c0_slopes': {key: pack(v) for key, v in slopes.items()},
           'plane_c0_slopes': {'b': 1, 'b_reverse': 1, 'd_metric': 3, 'd_affine': 2, 'R_NN': 0},
           'replicas': block_count, 'dataset_bundle': label + '.npz', 'inverse_or_sign_selection': False}
    return row, arrays


def text_value(value, errors, index):
    a, er, ei = unpack(value)[index], unpack(errors['real_se'])[index], unpack(errors['imag_se'])[index]
    return f'{float(a.real):.10g} +/- {float(er):.3g}; Im {float(a.imag):.10g} +/- {float(ei):.3g}'


def report(rows):
    lines = ['# Conditional charging two-potential source V001', '',
      'Metric-linear spatial source a=sqrt(1-2psi), affine N, charging J/a and psi-clamped flips. All entries below are c0=0 intercepts; c0=AR+Sself stays symbolic and unselected.', '',
      '| Dataset | Parent disposition | Paired replicas | Lossless full matrices/raw blocks |', '|---|---|---:|---|']
    for row in rows: lines.append(f"| {row['id']} | {row['parent_status']} | {row['replicas']} | {CP.name}/{row['dataset_bundle']} |")
    lines.extend(('', '| Dataset | k | A plane Re/Im +/- component SE | b plane Re/Im +/- component SE | reverse b plane Re/Im +/- component SE | d_metric plane Re/Im +/- component SE | d_affine plane Re/Im +/- component SE |', '|---|---|---|---|---|---|---|'))
    mode_rows = 0
    for row in rows:
        for index, k in enumerate(MODES.tolist()):
            keys = ('plane_R_NN', 'plane_b_intercept', 'plane_b_reverse_intercept', 'plane_d_metric_intercept', 'plane_d_affine_intercept')
            values = [text_value(row['central_intercepts'][key], row['component_errors'][key], index) for key in keys]
            lines.append('| ' + row['id'] + ' | ' + str(k) + ' | ' + ' | '.join(values) + ' |'); mode_rows += 1
    require(len(rows) == 10 and mode_rows == 70 and sum(r['replicas'] for r in rows) == 512, 'report ten/seventy/512 census')
    lines.extend(('', 'Add c0 times slopes 1 to b/reverse, 3 to d_metric and 2 to d_affine on every proper-plane mode; A/connected covariances have slope zero. Local first eta/psi means have slope1. Homogeneous source means gain sqrt27 per sublattice, sqrt54 in the scalar plane.',
      'The NN finite-M transfer second contact is retained; the mixed and spatial direct contacts are J and 3J. Covariance/contact errors use the same paired replicas. Both complex orders and +/- modes remain.',
      'The affine-coframe 2J comparison differs by background charging stress and cannot replace the specified metric chart.',
      'Parent fixed-coordinate diagnostics, old beta8/inverse refusals and distinct-method authored acceptance are unchanged. The whole-action proper-bath uniform rescaling guard is separate and does not delete coordinate energy covariance.',
      'This is a charging contribution, not complete material/Maxwell/support spatial stress, a stable-background selection, a physical body source, an inverse, a total-G calibration or a gravity prediction. No h strain law, field solve, favorable function, sampler/H/RNG replay or physical source value is selected.', ''))
    return '\n'.join(lines)


def main():
    global CREATED, ACTIVE
    require(sys.argv[1:] == ['--execute'], 'exact --execute argument')
    require(not any(path.exists() for path in (CP, RESULT, REPORT, RECEIPT, ERROR)), 'exclusive outputs absent')
    parent, priors, authorship = authenticate(); CP.mkdir(); CREATED = True
    require(np.isfinite(PLANE).all(), 'finite declared proper plane')
    close('proper_plane_norm', np.sum(abs(PLANE) ** 2, axis=1), np.ones(7))
    close('proper_plane_negative_modes', PLANE[[2, 4, 6]], PLANE[[1, 3, 5]].conj())
    manifest = {'name': NAME, 'pid': os.getpid(), 'input_sha256': INPUTS.copy(), 'protocol_sha256': PROTOCOL_SHA, 'source_sha256': sha(SOURCE),
                'source_chart': 'N=1+eta,a=sqrt(1-2psi); J/a and psi-clamped midpoint flips', 'dataset_order': IDS, 'mode_order': MODES.tolist(), 'c0': 'AR+Sself_SYMBOLIC_UNSELECTED', 'replica_count': 512}
    STAGES['manifest.json'] = exclusive(CP / 'manifest.json', manifest)
    event('started', input_sha256=INPUTS.copy(), manifest_sha256=STAGES['manifest.json'])
    rows = []
    for index, (label, prior) in enumerate(zip(IDS, priors)):
        ACTIVE = {'dataset': label, 'phase': 'RAW_MOMENT_SOURCE_RECOVERY'}
        row, arrays = summarize(prior, label, 32 if index < 8 else 128)
        bundle(label + '.npz', arrays); row['bundle_sha256'] = STAGES[label + '.npz']
        save(label + '.json', row); rows.append(row)
    ACTIVE = {'phase': 'FINAL_INPUT_AND_REPORT_GUARDS'}; recheck(); output = report(rows)
    require(len(STAGES) == 21 and len((CP / 'journal.jsonl').read_bytes().splitlines()) == 21, 'checkpoint/journal prefix census')
    result = {'name': NAME, 'pid': os.getpid(), 'status': 'CONDITIONAL_CHARGING_SOURCE_SAVED_RECOVERY_PASSED',
              'input_sha256': INPUTS.copy(), 'source_sha256': sha(SOURCE), 'protocol_sha256': PROTOCOL_SHA,
              'parent_status': parent['status'], 'parent_beta8_refusals': parent['parent_condition_statuses'],
              'parent_covariance_inverse': parent['covariance_inverse'], 'parent_authorship_scope': authorship,
              'rows': rows, 'checks': CHECKS.copy(), 'passed': len(CHECKS), 'failed': 0, 'replica_count': 512, 'mode_count': 7,
              'c0': 'SYMBOLIC_AR_PLUS_SSELF_NO_VALUE_SELECTED', 'mode_order': MODES.tolist(), 'dataset_order': IDS,
              'full_material_or_gravity_closure': False, 'elapsed_seconds': time.perf_counter() - T0}
    ACTIVE = {'phase': 'OUTPUT_SEAL'}
    raw_sha = exclusive(RESULT, result); event('result_complete', filename=RESULT.name, sha256=raw_sha)
    with REPORT.open('x') as f: f.write(output); f.flush(); os.fsync(f.fileno())
    event('report_complete', filename=REPORT.name, sha256=sha(REPORT))
    recheck(counting=False)
    receipt = {'status': result['status'], 'pid': os.getpid(), 'result_sha256': raw_sha,
               'result_canonical_sha256': hashlib.sha256(canonical(result)).hexdigest(), 'report_sha256': sha(REPORT),
               'source_sha256': sha(SOURCE), 'protocol_sha256': PROTOCOL_SHA, 'input_sha256': INPUTS.copy(),
               'checkpoint_sha256': STAGES.copy(), 'journal_prefix_sha256': sha(CP / 'journal.jsonl'),
               'passed': result['passed'], 'failed': 0, 'check_count': len(CHECKS), 'dataset_count': 10, 'replica_count': 512,
               'mode_count': 7, 'checkpoint_file_count': 21, 'journal_event_count_after_receipt': 24,
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

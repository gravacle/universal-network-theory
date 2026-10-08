#!/usr/bin/env python3
"""Exploratory saved scalar source response; root alone executes, no old imports."""
import os
for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[key] = '1'
import sys, json, hashlib, math, re, time, traceback
from pathlib import Path
import numpy as np

J = Path(__file__).resolve().parent
ROOT = J.parent.parent
NAME = 'LOCAL_RECORD_FEEDBACK_TRACE_COORDINATION_RESPONSE_V001'
STEM = 'local_record_feedback_trace_coordination_response_v001'
PROTOCOL = J / (NAME + '.md')
PROTOCOL_SHA = '15803e409afbdcbf5081be1d942479e28ad21f2bb3e28be05077849300a0fae2'
CP = J / (STEM + '_checkpoints')
RESULT, REPORT, RECEIPT, ERROR = [J / (NAME + suffix) for suffix in
                                ('_RESULT.json', '_RESULT.md', '_RECEIPT.json', '_ERROR.json')]
PARENT = 'LOCAL_RECORD_FEEDBACK_3D_PAIR_COORDINATION_RESPONSE_V001'
QUERY = 'LOCAL_RECORD_FEEDBACK_3D_QUERY_RESPONSE_RECOVERY_V001'
PACKETS = ((PARENT, 'local_record_feedback_3d_pair_coordination_response_v001', 180914, 342),
           (QUERY, 'local_record_feedback_3d_query_response_recovery_v001', 364, 21))
L = np.zeros((2, 14)); L[0, :12] = 1 / math.sqrt(2); L[1, 12:] = 1 / math.sqrt(2)
CONDITIONS = ((4, 1 / 16), (4, 1 / 32), (8, 1 / 16), (8, 1 / 32))
STARTS = ('I01', 'I02', 'B', 'R')
FIELDS = ('A', 'B', 'C', 'determinant', 'S_T_fixed_Q', 'S_Q_fixed_T',
          'T_response_relaxed', 'response_reduction', 'coupling_fraction', 'df_du_fixed_Q',
          'Gamma_TT_candidate', 'Gamma_TQ_candidate', 'Gamma_QQ_candidate',
          'Gamma_TT_relaxed_candidate', 'candidate_stiffness_reduction')
CHECKS, INPUTS, COMMITS = [], {}, {}
ACTIVE, CREATED = None, False

def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for data in iter(lambda: stream.read(1 << 20), b''): digest.update(data)
    return digest.hexdigest()

def read(path): return json.loads(Path(path).read_bytes())

def safe(value):
    if isinstance(value, np.ndarray): return safe(value.tolist())
    if isinstance(value, np.generic): return safe(value.item())
    if isinstance(value, dict): return {str(k): safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)): return [safe(v) for v in value]
    if isinstance(value, float) and not math.isfinite(value): return {'nonfinite': repr(value)}
    return value

def canonical(value): return json.dumps(safe(value), sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
def unpack(value): return np.asarray(value['real']) + 1j * np.asarray(value['imag']) if isinstance(value, dict) else np.asarray(value)
def require(ok, label):
    if not ok: raise RuntimeError(label)

def close(label, actual, expected):
    a, b = np.asarray(actual), np.asarray(expected)
    residual = float(np.linalg.norm(a - b)); tolerance = 3e-11 * max(1., float(np.linalg.norm(b)))
    ok = bool(np.isfinite(a).all() and np.isfinite(b).all() and residual <= tolerance)
    CHECKS.append(safe({'label': label, 'passed': ok, 'residual': residual, 'tolerance': tolerance}))
    if not ok: raise ArithmeticError(label)

def register(path, wanted):
    path = Path(path).resolve(); require(sha(path) == wanted, 'input seal: ' + str(path))
    name = str(path.relative_to(ROOT)); require(name not in INPUTS or INPUTS[name] == wanted, 'contradictory seal')
    INPUTS[name] = wanted

def recheck():
    for name, wanted in INPUTS.items(): require(sha(ROOT / name) == wanted, 'changed input: ' + name)

def write(path, value):
    with Path(path).open('xb') as stream:
        stream.write(canonical(value) + b'\n'); stream.flush(); os.fsync(stream.fileno())
    return sha(path)

def event(kind, **values):
    with (CP / 'journal.jsonl').open('ab') as stream:
        stream.write(canonical({'event': kind, **values}) + b'\n'); stream.flush(); os.fsync(stream.fileno())

def save(name, value):
    digest = write(CP / name, value); COMMITS[name] = digest
    event('row_complete', filename=name, sha256=digest)

def authenticate_packet(name, stem, count, cpcount):
    result, receipt = read(J / (name + '_RESULT.json')), read(J / (name + '_RECEIPT.json'))
    require(receipt['result_sha256'] == sha(J / (name + '_RESULT.json')) and
            receipt['result_canonical_sha256'] == hashlib.sha256(canonical(result)).hexdigest() and
            receipt['report_sha256'] == sha(J / (name + '_RESULT.md')), name + ' result/report/canonical')
    require(result['failed'] == receipt['failed'] == 0 and result['passed'] == receipt['passed'] ==
            len(result['checks']) == count and all(c['passed'] for c in result['checks']), name + ' arithmetic')
    require(result['status'] == receipt['status'] and result['input_sha256'] == receipt['input_sha256'], name + ' status/inputs')
    cp = J / (stem + '_checkpoints'); manifest = read(cp / 'manifest.json')
    lines = (cp / 'journal.jsonl').read_bytes().splitlines(keepends=True); journal = [json.loads(x) for x in lines]
    require(hashlib.sha256(b''.join(lines[:-1])).hexdigest() == receipt['journal_prefix_sha256'] and
            journal[-1]['event'] == 'receipt_complete' and journal[-1]['sha256'] == sha(J / (name + '_RECEIPT.json')), name + ' journal prefix')
    require(manifest['input_sha256'] == receipt['input_sha256'] and any(e['event'] == 'started' and
            e['manifest_sha256'] == receipt['checkpoint_sha256']['manifest.json'] and
            e['input_sha256'] == receipt['input_sha256'] for e in journal), name + ' manifest/start')
    require(len(receipt['checkpoint_sha256']) == cpcount, name + ' checkpoint census')
    for filename, wanted in receipt['checkpoint_sha256'].items():
        register(cp / filename, wanted)
        commits = [e for e in journal if e.get('filename') == filename and e.get('sha256') == wanted]
        require(len(commits) == 1, name + ' unique checkpoint commit: ' + filename)
    register(cp / 'journal.jsonl', sha(cp / 'journal.jsonl'))
    for filename, wanted in receipt['input_sha256'].items():
        if filename == 'core_identity_canonical_sha256':
            require(hashlib.sha256(canonical(manifest['preserved_core_identity'])).hexdigest() == wanted, 'core identity seal')
        else:
            path = J / (stem + '.py') if filename == 'source' else J / (name + '.md') if filename == 'protocol' else J / filename
            register(path, wanted)
    return result

def authenticate():
    require(sha(PROTOCOL) == PROTOCOL_SHA, 'frozen new protocol')
    pins = re.findall(r'^\| (.+?) \| ([0-9a-f]{64}) \|$', PROTOCOL.read_text(), re.M)
    require(len(pins) == 12, 'direct pin census')
    for name, wanted in pins: register(ROOT / name, wanted)
    register(PROTOCOL, PROTOCOL_SHA); register(Path(__file__).resolve(), sha(__file__))
    return [authenticate_packet(*spec) for spec in PACKETS]

def covariance(raw, beta): return beta * (raw['second'] - np.outer(raw['mean'], raw['mean']))

def derive(matrix):
    a, b, c = float(matrix[0, 0]), float((matrix[0, 1] + matrix[1, 0]) / 2), float(matrix[1, 1])
    det = a * c - b * b
    quotient = lambda num, den: num / den if den != 0 and math.isfinite(num) and math.isfinite(den) and math.isfinite(num / den) else None
    reduce = quotient(b * b, c)
    reverse_reduce = quotient(b * b, a)
    values = [a, b, c, det, a - reduce if reduce is not None else None,
              c - reverse_reduce if reverse_reduce is not None else None, a, reduce, quotient(b * b, a * c),
              quotient(-b, c), quotient(c, det), quotient(-b, det), quotient(a, det),
              quotient(1., a), quotient(b * b, a * det)]
    distance = math.hypot(a - c, 2 * b); lo, hi = (a + c - distance) / 2, (a + c + distance) / 2
    flags = []
    if not np.isfinite(matrix).all() or not all(math.isfinite(x) for x in (lo, hi)): flags.append('NONFINITE')
    if lo <= 0: flags.append('NONPOSITIVE')
    condition = quotient(hi, lo) if lo > 0 else None
    if condition is None or condition > 1e8: flags.append('CONDITIONING')
    gamma = np.array([[c, -b], [-b, a]]) / det if det != 0 and all(math.isfinite(v) for v in (a, b, c, det)) else None
    residual = float(np.linalg.norm(matrix @ gamma - np.eye(2))) if gamma is not None else None
    if residual is None or not math.isfinite(residual) or residual > 3e-11 * max(1., condition or 1.): flags.append('INVERSE_RESIDUAL')
    return dict(zip(FIELDS, values)), {'eigenvalues': [lo, hi], 'condition_number': condition,
                                      'inverse_residual': residual, 'refusal_flags': flags}, gamma

def jackknife(values):
    x = np.asarray(values); b = len(x); delta = x - x.mean(axis=0)
    return (b - 1) / b * delta.T @ delta

def summarize(label, blocks, beta, parent_row, query_row, condition_status):
    begin = len(CHECKS); b = len(blocks['mean'])
    require(b in (32, 128) and query_row['block_count'] == b and query_row['block_measurements'] == 32, 'row block census')
    raw = {key: value.mean(axis=0) for key, value in blocks.items()}; chi = covariance(raw, beta)
    close(label + ' symmetry', chi, chi.T)
    close(label + ' parent chi', chi, parent_row['joint_estimates']['chi_TQ_density_independent'])
    close(label + ' query chi', chi, unpack(query_row['values']['scalar_chi_density_TQ']))
    replicas = [covariance({k: (b * value.mean(axis=0) - value[i]) / (b - 1)
                            for k, value in blocks.items()}, beta) for i in range(b)]
    central, diagnostic, gamma = derive(chi); derived = [derive(value) for value in replicas]
    chi_cov = jackknife(np.asarray(replicas).reshape(b, 4)); chi_se = np.sqrt(np.diag(chi_cov)).reshape(2, 2)
    close(label + ' parent chi SE', chi_se, parent_row['joint_component_errors']['chi_TQ_density_independent']['se'])
    close(label + ' query chi SE', chi_se, unpack(query_row['component_errors']['scalar_chi_density_TQ']['real_se']))
    available = [k for k in FIELDS if central[k] is not None and math.isfinite(central[k]) and
                 all(row[0][k] is not None and math.isfinite(row[0][k]) for row in derived)]
    cov = jackknife([[row[0][k] for k in available] for row in derived])
    se = dict(zip(available, np.sqrt(np.diag(cov))))
    for label2, values, spectrum in [('central', central, diagnostic)] + [(str(i), row[0], row[1]) for i, row in enumerate(derived)]:
        a, c, det = values['A'], values['C'], values['determinant']
        close(label + label2 + ' eigenvalue trace', sum(spectrum['eigenvalues']), a + c)
        close(label + label2 + ' eigenvalue determinant', math.prod(spectrum['eigenvalues']), det)
        if values['S_T_fixed_Q'] is not None: close(label + label2 + ' constrained response', values['S_T_fixed_Q'] * c, det)
        if values['S_Q_fixed_T'] is not None: close(label + label2 + ' reverse constrained response', values['S_Q_fixed_T'] * a, det)
        if all(values[k] is not None for k in ('Gamma_TT_candidate', 'Gamma_TQ_candidate', 'Gamma_QQ_candidate',
                                               'Gamma_TT_relaxed_candidate', 'candidate_stiffness_reduction')) and values['Gamma_QQ_candidate'] != 0:
            close(label + label2 + ' relaxed Legendre', values['Gamma_TT_candidate'] -
                  values['Gamma_TQ_candidate'] ** 2 / values['Gamma_QQ_candidate'], values['Gamma_TT_relaxed_candidate'])
            close(label + label2 + ' stiffness difference', values['Gamma_TT_candidate'] -
                  values['Gamma_TT_relaxed_candidate'], values['candidate_stiffness_reduction'])
    close(label + ' D identity', 1 + (raw['mean'][0] - raw['mean'][1]) / (2 * math.sqrt(54)), parent_row['estimates']['scalars'][1])
    flags = diagnostic['refusal_flags'].copy(); error_scale = 3 * float(np.linalg.norm(chi_se))
    if diagnostic['eigenvalues'][0] <= error_scale: flags.append('BLOCK_ERROR_DOMINATED')
    if any(row[1]['refusal_flags'] for row in derived): flags.append('REPLICA_REFUSAL')
    mixing = condition_status == 'FINITE_GRID_PILOT_DIAGNOSTICS_PASSED' and 'MIXING_UNQUALIFIED' not in query_row['parent_status']
    if not mixing: flags.append('MIXING_UNQUALIFIED')
    qualified = gamma is not None and not flags
    return {'id': label, 'condition': parent_row['condition'], 'beta': beta, 'epsilon': parent_row['epsilon'],
            'block_count': b, 'block_measurements': 32,
            'parent_status': query_row['parent_status'], 'parent_condition_status': condition_status,
            'mean_density_TQ': raw['mean'] / math.sqrt(54), 'raw_paired_block_means': blocks,
            'chi': chi, 'chi_SE': chi_se, 'chi_component_jackknife_covariance': chi_cov, 'chi_replicas': replicas,
            'central': central, 'derived_replicas': [row[0] for row in derived], 'derived_SE': se,
            'paired_derived_covariance_labels': available, 'paired_derived_jackknife_covariance': cov,
            'central_diagnostics': diagnostic, 'replica_diagnostics': [row[1] for row in derived],
            'three_SE_Frobenius_scale': error_scale, 'inverse_refusal_flags': flags,
            'Gamma_candidate': gamma, 'qualified_Gamma': gamma if qualified else None,
            'inverse_status': 'SCALAR_STATIC_INVERSE_DIAGNOSTICS_PASSED_ONLY' if qualified else 'INVERSE_UNQUALIFIED_' + '_'.join(flags),
            'mechanical_or_metric_stiffness_qualification': False, 'source_contacts_uu_uf_ff': [0, 0, 0],
            'scope': 'EXPLORATORY_SAVED_LINEAR_SOURCE_RESPONSE', 'checks': CHECKS[begin:].copy()}

def main():
    global ACTIVE, CREATED
    start = time.perf_counter(); require(sys.argv[1:] == ['--execute'], 'exact root-only --execute required')
    require(not any(p.exists() for p in (CP, RESULT, REPORT, RECEIPT, ERROR)), 'exclusive reserved outputs')
    parent, query = authenticate(); CP.mkdir(); CREATED = True
    save('manifest.json', {'pid': os.getpid(), 'input_sha256': INPUTS, 'post_result_exploratory_design': True})
    event('started', input_sha256=INPUTS, manifest_sha256=COMMITS['manifest.json'])
    qrows = {r['id']: r for r in query['rows']}; require(len(qrows) == len(query['rows']) == 20, 'unique query rows')
    require(len(parent['chains']) == 16 and len(parent['conditions']) == 4, 'full parent census')
    expected_ids = ['c%d_%s' % (ci, start) for ci in range(4) for start in STARTS]
    require([r['id'] for r in parent['chains']] == expected_ids and
            [r['condition'] for r in parent['conditions']] == list(range(4)) and
            list(qrows) == expected_ids + ['condition%d' % ci for ci in range(4)], 'ordered unique full census')
    statuses = {r['condition']: r['status'] for r in parent['conditions']}; cache, rows = {}, []
    for old in parent['chains'] + parent['conditions']:
        label = old.get('id', 'condition' + str(old['condition'])); ACTIVE = {'row': label}
        qr = qrows[label]; require(qr['beta'] == old['beta'] and qr['parent_status'] == old['status'], 'row beta/status')
        require((old['beta'], old['epsilon']) == CONDITIONS[old['condition']], 'frozen beta/step')
        sums = qr['raw_block_sufficient_sums']; q = unpack(sums['q']) / 32; qq = unpack(sums['qq']) / 32
        close(label + ' k0 imaginary means', q.imag, np.zeros_like(q.imag))
        close(label + ' k0 imaginary seconds', qq.imag, np.zeros_like(qq.imag))
        blocks = {'mean': q.real @ L.T, 'second': np.einsum('ai,bij,cj->bac', L, qq.real, L)}
        require(blocks['mean'].shape == (qr['block_count'], 2) and blocks['second'].shape == (qr['block_count'], 2, 2), 'scalar block shapes')
        if 'id' in old:
            cache[label] = blocks; independent = old['joint_block_raw_moments']
        else:
            require(old['chain_ids'] == ['c%d_%s' % (old['condition'], start) for start in STARTS], 'pooled chain order')
            independent = {k: np.concatenate([np.asarray(next(r for r in parent['chains'] if r['id'] == cid)['joint_block_raw_moments'][k]) for cid in old['chain_ids']])
                           for k in ('mean_TQ_density_scaled', 'second_TQ_density')}
            for key in blocks: close(label + ' pooled raw ' + key, blocks[key], np.concatenate([cache[cid][key] for cid in old['chain_ids']]))
        close(label + ' independent scalar means', blocks['mean'], independent['mean_TQ_density_scaled'])
        close(label + ' independent scalar seconds', blocks['second'], independent['second_TQ_density'])
        row = summarize(label, blocks, old['beta'], old, qr, statuses[old['condition']]); save(label + '.json', row); rows.append(row)
    require(len(rows) == 20 and sum(r['block_count'] for r in rows) == 1024, 'all20/1024 replicas')
    recheck(); result = {'name': NAME, 'rows': rows, 'input_sha256': INPUTS, 'passed': len(CHECKS), 'failed': 0,
                        'checks': CHECKS.copy(), 'status': 'EXPLORATORY_SAVED_RESPONSE_PARENT_QUALIFICATIONS_UNCHANGED',
                        'elapsed_seconds': time.perf_counter() - start}
    raw = write(RESULT, result); event('result_complete', filename=RESULT.name, sha256=raw)
    lines = ['# Exploratory trace–coordination response V001', '',
             'Post-result source design; the original inverse-error criterion and parent beta8 failures are unchanged.', '',
             '| Dataset (beta, step) | A +/- SE | B +/- SE | C +/- SE | fixed-Q trace response +/- SE | relaxed trace response +/- SE | Parent row | Parent condition |', '|---|---|---|---|---|---|---|---|']
    def fmt(row, key):
        value = row['central'][key]
        if value is None or not math.isfinite(value): return 'undefined'
        return '%+.10g +/- %.3g' % (value, row['derived_SE'][key]) if key in row['derived_SE'] else '%+.10g (SE undefined)' % value
    for r in rows: lines.append('| response %s (%g, %g) | %s | %s | %s | %s | %s | %s | %s |' % (r['id'], r['beta'], r['epsilon'], *(fmt(r, k) for k in ('A', 'B', 'C', 'S_T_fixed_Q', 'T_response_relaxed')), r['parent_status'], r['parent_condition_status']))
    lines += ['', '| Dataset | candidate Gamma_TT +/- SE | candidate Gamma_TQ +/- SE | candidate relaxed Gamma_TT +/- SE | inverse status |', '|---|---|---|---|---|']
    for r in rows: lines.append('| candidate %s | %s | %s | %s | %s |' % (r['id'], *(fmt(r, k) for k in ('Gamma_TT_candidate', 'Gamma_TQ_candidate', 'Gamma_TT_relaxed_candidate')), r['inverse_status']))
    require(sum(x.startswith('| response ') for x in lines) == sum(x.startswith('| candidate ') for x in lines) == 20, 'report20/20 rows')
    lines += ['', 'All raw paired blocks, means, chi and nonlinear replicas, complete scalar covariance and refusal flags are in JSON. Affine source contacts are zero; identity2uV remains work/count energy.',
              'These are fixed-source-coordinate responses and algebraic candidate Legendre quantities, not complete mechanical/metric stiffness, pressure or a new volume/expansion law.']
    with REPORT.open('x') as stream: stream.write('\n'.join(lines) + '\n'); stream.flush(); os.fsync(stream.fileno())
    event('report_complete', filename=REPORT.name, sha256=sha(REPORT)); recheck()
    receipt = {'result_sha256': raw, 'result_canonical_sha256': hashlib.sha256(canonical(result)).hexdigest(),
               'report_sha256': sha(REPORT), 'input_sha256': INPUTS, 'checkpoint_sha256': COMMITS.copy(),
               'journal_prefix_sha256': sha(CP / 'journal.jsonl'), 'passed': len(CHECKS), 'failed': 0,
               'pid': os.getpid(), 'status': result['status'], 'elapsed_seconds': time.perf_counter() - start}
    digest = write(RECEIPT, receipt); event('receipt_complete', filename=RECEIPT.name, sha256=digest)
    print(json.dumps({'passed': len(CHECKS), 'failed': 0, 'raw_sha256': raw, 'receipt_sha256': digest}), flush=True)

if __name__ == '__main__':
    try: main()
    except Exception as error:
        if not ERROR.exists():
            digest = write(ERROR, {'status': 'ARITHMETIC_FAILED' if isinstance(error, ArithmeticError) else 'EXECUTION_ERROR_PRESERVED',
                                   'type': type(error).__name__, 'error': str(error), 'traceback': traceback.format_exc(),
                                   'active': ACTIVE, 'input_sha256': INPUTS, 'committed_sha256': COMMITS, 'checks': CHECKS.copy()})
            if CREATED: event('error_preserved', sha256=digest)
        print(traceback.format_exc(), file=sys.stderr); sys.exit(3)

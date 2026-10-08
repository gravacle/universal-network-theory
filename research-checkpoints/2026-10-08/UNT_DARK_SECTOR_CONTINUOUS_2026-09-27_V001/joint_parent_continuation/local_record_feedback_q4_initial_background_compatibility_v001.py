"""Prospective diagonal census only; root launches after frozen full reviews."""
import argparse
from fractions import Fraction
import hashlib
import itertools
import json
import os
from pathlib import Path
import time
import traceback

J = Path(__file__).resolve().parent
ROOT = J.parent.parent
STEM = 'LOCAL_RECORD_FEEDBACK_Q4_INITIAL_BACKGROUND_COMPATIBILITY_V001'
PROTOCOL = STEM + '.md'
PROTOCOL_SHA = '395ecb1b4fb6679d71db347a7d2607f73e516b57f3fc1fd8669196dabac8630f'
PARENT = 'LOCAL_RECORD_FEEDBACK_Q4_SPARSE_INSERTION_VERIFICATION_V001'
DIRECT = {
    'LOCAL_RECORD_FEEDBACK_CONSTRAINED_COUNT_BACKGROUND_ACTION_V001.md': 'fcfe8fd7513ff7a495ddebf7a857c98b8d5ca1a3760bb8519f2e5a05e13ad18d',
    'LOCAL_RECORD_FEEDBACK_Q4_CONSERVING_FORMATION_CANDIDATE_V001.md': '07323053b75b947b35712f0ac8fc4ce04c2766131cd4e684fd64167321b51f3c',
    PARENT + '.md': '92f7f9c4cf26befb1eed9d85c2232271629f3088fcdb0342692a74342f589813',
    'local_record_feedback_q4_sparse_insertion_verification_v001.py': '774c81de75458fb430009655f83f00dcc24bac423385ac1b72409dc6f160134e',
    PARENT + '_RESULT.json': '8bc5f32488c6bfdeb0312dbb68c681eb4ce88cf1a63a62fef9177013e0a8fd60',
    PARENT + '_RECEIPT.json': '932c46279b44d856e1bdedf2a9a3e2c267ba3e3c59edfe9d64e64f4cebf6d5b8',
}
COLUMNS = ['cut_word', 'carrier', 'record_index', 'E4', 'degree_carrier',
           'Q', 'Q_A', 'Q_B', 'staggered_K', 'occupied_links',
           'degree_square_sum', 'feedback_dot', 'Qcut', 'Rcut']
CHECKS = 0
ACTIVE = {}


def check(test, label):
    global CHECKS
    CHECKS += 1
    if not test:
        raise AssertionError(label)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def write_new(path, value):
    data = canonical(value)
    with path.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    path.chmod(0o444)
    return hashlib.sha256(data).hexdigest()


def resolve(name):
    return ROOT / name if name.startswith('program-worktree/') else J / name


def seal(pins, name, expected):
    check(name not in pins or pins[name] == expected, ('pin_collision', name))
    check(sha(resolve(name)) == expected, ('input_seal', name))
    pins[name] = expected


def note_pins(pins, name):
    for line in resolve(name).read_text().splitlines():
        if line.startswith('| '):
            cells = [x.strip() for x in line.strip('|').split('|')]
            if len(cells) == 2 and len(cells[1]) == 64:
                seal(pins, cells[0], cells[1])


def authenticate():
    pins = {}
    for name, expected in DIRECT.items():
        seal(pins, name, expected)
    seal(pins, PROTOCOL, PROTOCOL_SHA)
    seal(pins, Path(__file__).name, sha(Path(__file__)))
    note_pins(pins, 'LOCAL_RECORD_FEEDBACK_CONSTRAINED_COUNT_BACKGROUND_ACTION_V001.md')
    note_pins(pins, 'LOCAL_RECORD_FEEDBACK_Q4_CONSERVING_FORMATION_CANDIDATE_V001.md')
    parent = json.loads((J / (PARENT + '_RESULT.json')).read_text())
    receipt = json.loads((J / (PARENT + '_RECEIPT.json')).read_text())
    check(parent['status'] == 'EXACT_SPARSE_Q4_OPERATOR_IDENTITIES_PASSED', 'parent_status')
    check((parent['base_vertices'], parent['base_edges'], parent['columns'], parent['Gram_entries_checked'])
          == (54, 108, 207360, 1492992), 'parent_census')
    check(parent['native_coefficients'] == {'U': 1, 'EP': 1, 'lambda': '1/2', 'j': '1/4',
                                          't': '1/10', 'h': '1/5', 'Delta': 0}, 'parent_coefficients')
    check(receipt['pins'] == parent['pins'], 'parent_receipt_pins')
    check(receipt['raw_sha256'] == DIRECT[PARENT + '_RESULT.json'], 'parent_receipt_raw')
    seal(pins, PARENT + '_RESULT.md', receipt['report_sha256'])
    for name, expected in parent['pins'].items():
        seal(pins, name, expected)
    cp = J / 'q4_sparse_insertion_verification_v001_checkpoints'
    expected_files = {'OWNER_START.json'} | {f'F{length}_{suffix}.json{commit}'
        for length in (2, 3) for suffix in ('background0', 'background1', 'background2', 'GRAM')
        for commit in ('', '.COMMIT.json')}
    check(set(receipt['checkpoint_sha256']) == expected_files, 'parent_checkpoint_census')
    check(set(p.name for p in cp.iterdir()) == expected_files, 'parent_checkpoint_directory')
    for name, expected in receipt['checkpoint_sha256'].items():
        seal(pins, str(Path(cp.name) / name), expected)
    owner = json.loads((cp / 'OWNER_START.json').read_text())
    check(owner['pins'] == parent['pins'] and owner['pid'] == receipt['pid'], 'parent_owner')
    check([(r['length'], r['background'], r['columns'], r['record_patterns']) for r in parent['rows']]
          == [(length, bg, 34560, 20) for length in (2, 3) for bg in range(3)], 'parent_ordered_rows')
    check([(r['length'], r['entries_checked']) for r in parent['grams']]
          == [(2, 746496), (3, 746496)], 'parent_ordered_grams')
    for row in parent['rows'] + parent['grams']:
        suffix = 'GRAM' if 'entries_checked' in row else 'background' + str(row['background'])
        name = f"F{row['length']}_{suffix}.json"
        check(json.loads((cp / name).read_text()) == row, ('parent_row', name))
        commit = json.loads((cp / (name + '.COMMIT.json')).read_text())
        check(commit == {'checkpoint_name': name, 'checkpoint_sha256': sha(cp / name),
                         'pins': parent['pins'], 'status': 'COMPLETE_EXACT_CHECKS_PASSED'},
              ('parent_commit', name))
    check(not (J / (PARENT + '_ERROR.json')).exists(), 'parent_no_error')
    return pins, parent


def graph_and_census(parent):
    coords = list(itertools.product(range(3), repeat=3))
    index = {r: i for i, r in enumerate(coords)}
    edges = [(i, 27 + index[tuple((r[k] + s[k]) % 3 for k in range(3))])
             for i, r in enumerate(coords)
             for s in ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))]
    cuts = [4 * index[r] for r in ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))]
    endpoints = [v for e in cuts for v in edges[e]]
    check(len(set(edges)) == 108 and len(set(endpoints)) == 8, 'native_graph')
    check(parent['cuts'] == [list(edges[e]) for e in cuts], 'saved_native_cuts')
    cutmask = sum(1 << e for e in cuts)
    backgrounds = [0, ((1 << 108) - 1) ^ cutmask,
                   sum(1 << e for e in range(108) if e not in cuts and e % 2)]
    allq = (1 << 54) - 1
    records = [0, allq, sum(1 << v for v in range(0, 54, 2)),
               sum(1 << v for v in range(1, 54, 2))] + [1 << v for v in endpoints] + [allq ^ (1 << v) for v in endpoints]
    labels = ['blank', 'all', 'even_index', 'odd_index'] + ['singleton_' + str(v) for v in endpoints] + ['hole_' + str(v) for v in endpoints]
    check(len(set(records)) == 20 and set(allq ^ q for q in records) == set(records), 'record_complements')
    qr = [(q.bit_count(), (q & ((1 << 27) - 1)).bit_count(), (q >> 27).bit_count()) for q in records]
    check(sum(q for q, a, b in qr) == 540 and sum(q * q for q, a, b in qr) == 26854,
          'record_Q_oracle')
    check(sum(a - b for q, a, b in qr) == 0 and sum((a - b) ** 2 for q, a, b in qr) == 18
          and sum(q * (a - b) for q, a, b in qr) == 0, 'record_K_oracle')
    return edges, cuts, endpoints, backgrounds, records, labels, qr


def frac(value):
    f = Fraction(value)
    return [f.numerator, f.denominator]


def group(bi, background, edges, cuts, endpoints, records, qr):
    rows, word_data = [], []
    for n in range(16):
        bits = [(n >> i) & 1 for i in range(4)]
        word = background | sum(bit << e for bit, e in zip(bits, cuts))
        degree = [0] * 54
        for e, (a, b) in enumerate(edges):
            if (word >> e) & 1:
                degree[a] += 1
                degree[b] += 1
        S, occ = sum(bits), word.bit_count()
        charge = [d - 2 for d in degree]
        square = sum(c * c for c in charge)
        check(sum(degree) == 2 * occ and all(0 <= d <= 4 for d in degree), 'degree_incidence')
        check(sum(charge) == 2 * occ - 108, 'charge_sum')
        base, other = ((0, 0), (3, 4), (2, 2))[bi]
        endpoint_bit = {v: bits[i] for i, e in enumerate(cuts) for v in edges[e]}
        check(degree == [base + endpoint_bit[v] if v in endpoint_bit else other for v in range(54)],
              'background_degrees')
        word_data.append({'cut_word': n, 'incidence_word': str(word), 'degrees': degree,
                          'charge_sum': sum(charge), 'S': S})
        for ri, (q, (Q, QA, QB)) in enumerate(zip(records, qr)):
            qbits = [(q >> v) & 1 for v in range(54)]
            dot = sum(qv * cv for qv, cv in zip(qbits, charge))
            qcut = sum(qbits[v] for v in endpoints)
            rcut = sum(bits[i] * (qbits[a] + qbits[b]) for i, e in enumerate(cuts) for a, b in [edges[e]])
            for carrier in range(54):
                row = [n, carrier, ri, 4 * square - 2 * dot + 4 + degree[carrier],
                       degree[carrier], Q, QA, QB, QA - QB, occ, square, dot, qcut, rcut]
                ACTIVE.clear()
                ACTIVE.update(background=bi, cut_word=n, carrier=carrier, record_index=ri, partial_row=row)
                oracle = ((868 - 24 * S + 4 * Q - 2 * rcut + degree[carrier]),
                          (772 + 24 * S - 4 * Q + 2 * qcut - 2 * rcut + degree[carrier]),
                          (4 + 8 * S - 2 * rcut + degree[carrier]))[bi]
                check(row[3] == oracle, 'independent_diagonal_polynomial')
                rows.append(row)
    check(len(rows) == 17280 and len({tuple(r[:3]) for r in rows}) == 17280, 'unique_group_census')
    lo, hi = min(r[3] for r in rows), max(r[3] for r in rows)
    total = sum(r[3] for r in rows)
    check((lo, hi) == ((772, 1084), (575, 872), (6, 39))[bi], 'predeclared_range')
    check(total == (15968000, 12440320, 312320)[bi], 'predeclared_sum')
    summary = {'background': bi, 'rows': len(rows), 'native_energy_range': [frac(Fraction(lo, 4)), frac(Fraction(hi, 4))],
               'native_energy_sum': frac(Fraction(total, 4)), 'native_census_centroid': frac(Fraction(total, 4 * len(rows))),
               'energy_min_ids': [r[:3] for r in rows if r[3] == lo], 'energy_max_ids': [r[:3] for r in rows if r[3] == hi],
               'field_ranges': {COLUMNS[k]: [min(r[k] for r in rows), max(r[k] for r in rows)] for k in range(4, len(COLUMNS))}}
    return {'columns': COLUMNS, 'background': bi, 'word_data': word_data, 'rows': rows}, summary


def execute(args):
    start = time.time()
    check(args.protocol_sha == PROTOCOL_SHA, 'launch_protocol_seal')
    pins, parent = authenticate()
    edges, cuts, endpoints, backgrounds, records, labels, qr = graph_and_census(parent)
    cp = J / 'q4_initial_background_compatibility_v001_checkpoints'
    cp.mkdir()
    write_new(cp / 'OWNER_START.json', {'pid': os.getpid(), 'pins': pins, 'time': start})
    summaries, bundles = [], []
    for bi, background in enumerate(backgrounds):
        data, summary = group(bi, background, edges, cuts, endpoints, records, qr)
        data['pins'] = pins
        name = f'background{bi}.json'
        bundle_sha = write_new(cp / name, data)
        write_new(cp / (name + '.COMMIT.json'), {'name': name, 'sha256': bundle_sha, 'rows': 17280,
                  'pins': pins, 'status': 'COMPLETE_EXACT_DIAGONAL_CHECKS_PASSED'})
        bundles.append({'file': str(Path(cp.name) / name), 'sha256': bundle_sha, 'rows': 17280})
        summaries.append(summary)
    check(sum(r['rows'] for r in summaries) == 51840, 'full_unique_census')
    for name, expected in pins.items():
        check(sha(resolve(name)) == expected, ('pre_output_seal', name))
    formulas = {
        'E0(b;m,g)': 'Eunit*(E4/4+AR*Q+54*Sself)+E_donor(b;m,g)+E_precursor(b;m,g)+E_support(b;m,g)+E_additional_field(b;m,g)+E_other(b;m,g)',
        'rho0': 'E0/(27*nu)', 'k_req': '8*pi*G_total*E0/(81*nu*c_p^4)+Lambda/3',
        'P_req': '-E0/(81*nu)-p_b0+c_p^4*Lambda/(12*pi*G_total)-c_p^2*m*epsilon_phys^2/(162*pi*G_total*hbar^2)',
        'a_acceleration0': '2*m*epsilon_phys^2/(81*hbar^2)',
        'DAE_denominator': '324*pi*G_total/c_p^2',
        'fixed_proper_conditional_source': 'p_b0=0 only if complete admitted bare inventory is held independent of a',
        'epsilon_units': 'epsilon_phys=Eunit*epsilon_native',
        'flat_Lambda0_old_only_condition': 'FULL E0=0, not native intercept alone',
    }
    result = {'status': 'EXACT_DIAGONAL_INITIAL_DATA_AND_SYMBOLIC_COMPATIBILITY_REPORTED',
              'pins': pins, 'checks': CHECKS, 'unique_basis_count': 51840, 'basis_groups': summaries,
              'bundles': bundles, 'edges': [list(e) for e in edges], 'cuts': cuts,
              'record_patterns': [{'label': label, 'word': str(q), 'Q': Q, 'QA': a, 'QB': b, 'K': a - b}
                                  for label, q, (Q, a, b) in zip(labels, records, qr)],
              'symbolic_formulas': formulas, 'initial_counts': {'n0': 27, 'a0': 1, 'V0': '27*nu', 'count_current_K0': 0, 'count_load_B0': 0},
              'event_coefficients': [{'m': m, 'A0_coefficient': 2 * m, 'a_acceleration_coefficient': frac(Fraction(2 * m, 81)),
                  'P_port_coefficient': frac(Fraction(-m, 162)), 'unit_donor_assumption':
                  'one occupied unit donor' if m == 1 else 'two independent occupied unit donors; product lowering'} for m in (1, 2)],
              'census_is_physical_state': False, 'physical_compatibility_selected': False,
              'unknown_absolute_inventories_retained': True, 'per_basis_quantum_VarQ_and_VarK': [0, 0],
              'elapsed_seconds': time.time() - start}
    raw_path, report_path, receipt_path = [J / (STEM + suffix) for suffix in ('_RESULT.json', '_RESULT.md', '_RECEIPT.json')]
    raw_sha = write_new(raw_path, result)
    report = '# q4 diagonal initial-data compatibility V001\n\n' + result['status'] + '\n\n'
    report += 'All 51,840 representative incoming bases retained; integer diagonal checks only. Full rows are in three sealed checkpoint bundles. No physical background, pressure, state or unknown energy is selected.\n\n'
    report += '| Background | Bases | Native energy range | Exact native sum | Census centroid |\n|---|---:|---|---|---|\n'
    for r in summaries:
        report += f"| {r['background']} | {r['rows']} | {r['native_energy_range']} | {r['native_energy_sum']} | {r['native_census_centroid']} |\n"
    report += '\nFull energy retains AR Q + 54 Sself and unresolved donor/precursor/support/additional-field/other inventories. Census centroids are bookkeeping, not an adopted mixed or thermal state.\n\n'
    report += '\n'.join(f'- {k}: {v}' for k, v in formulas.items()) + '\n\n'
    report += f'Exact check count: {CHECKS}. Raw SHA256: {raw_sha}. Both m=1 and m=2 unit-donor conditions are reported; physical q4 placement/ruler/covariant stress remains open.\n'
    with report_path.open('x') as stream:
        stream.write(report)
        stream.flush()
        os.fsync(stream.fileno())
    report_path.chmod(0o444)
    for name, expected in pins.items():
        if sha(resolve(name)) != expected:
            raise AssertionError(('post_output_input_changed', name))
    receipt = {'pins': pins, 'pid': os.getpid(), 'raw_sha256': raw_sha, 'report_sha256': sha(report_path),
               'checks': CHECKS, 'unique_basis_count': 51840, 'elapsed_seconds': result['elapsed_seconds'],
               'checkpoint_sha256': {p.name: sha(p) for p in sorted(cp.iterdir())}}
    receipt_sha = write_new(receipt_path, receipt)
    print(json.dumps({'status': result['status'], 'checks': CHECKS, 'unique_basis_count': 51840,
                      'raw_sha256': raw_sha, 'receipt_sha256': receipt_sha, 'seconds': result['elapsed_seconds']}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--protocol-sha', required=True)
    args = parser.parse_args()
    if not args.execute:
        raise SystemExit('No calculation: frozen full review and root-only launch required.')
    reserved = [J / (STEM + suffix) for suffix in ('_RESULT.json', '_RESULT.md', '_RECEIPT.json', '_ERROR.json')]
    reserved.append(J / 'q4_initial_background_compatibility_v001_checkpoints')
    if any(path.exists() for path in reserved):
        raise SystemExit('Reserved path exists; preserve it and use a distinct reviewed recovery.')
    try:
        execute(args)
    except BaseException as error:
        path = J / (STEM + '_ERROR.json')
        if not path.exists():
            write_new(path, {'status': 'EXECUTION_ERROR_PRESERVED', 'pid': os.getpid(), 'checks_completed': CHECKS,
                            'active_context': ACTIVE, 'error_type': type(error).__name__, 'message': str(error),
                            'traceback': traceback.format_exc()})
        raise

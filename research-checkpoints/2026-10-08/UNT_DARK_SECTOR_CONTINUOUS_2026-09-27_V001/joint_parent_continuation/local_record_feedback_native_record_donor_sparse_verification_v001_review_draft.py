"""New F2 b_w operator/source verification; root-only launch after full review."""
import argparse
from functools import lru_cache
import hashlib
import itertools
import json
import os
from pathlib import Path
import time
import traceback

J = Path(__file__).resolve().parent
ROOT = J.parent.parent
STEM = 'LOCAL_RECORD_FEEDBACK_NATIVE_RECORD_DONOR_SPARSE_VERIFICATION_V001'
PROTOCOL = STEM + '.md'
PROTOCOL_SHA = 'PENDING_PROTOCOL_FREEZE'
NOTE = 'LOCAL_RECORD_FEEDBACK_NATIVE_RECORD_DONOR_FORMATION_V001.md'
PARENT = 'LOCAL_RECORD_FEEDBACK_Q4_SPARSE_INSERTION_VERIFICATION_V001'
DIRECT = {
    NOTE: '45b99f9642d9cf757460cb8a65ea1d27f1bbb9eac9b23674b1cf879adeabed4f',
    PARENT + '.md': '92f7f9c4cf26befb1eed9d85c2232271629f3088fcdb0342692a74342f589813',
    'local_record_feedback_q4_sparse_insertion_verification_v001.py': '774c81de75458fb430009655f83f00dcc24bac423385ac1b72409dc6f160134e',
    PARENT + '_RESULT.json': '8bc5f32488c6bfdeb0312dbb68c681eb4ce88cf1a63a62fef9177013e0a8fd60',
    PARENT + '_RECEIPT.json': '932c46279b44d856e1bdedf2a9a3e2c267ba3e3c59edfe9d64e64f4cebf6d5b8',
}
ZERO = (0,) * 12
COEFFICIENTS = ['cap_native_x0', 'cap_AR_x0', 'cap_Sself_x0', 'cap_native_x1', 'cap_AR_x1', 'cap_Sself_x1',
                'mid_native_x0', 'mid_AR_x0', 'mid_Sself_x0', 'mid_native_x1', 'mid_AR_x1', 'mid_Sself_x1']
W = 0
CHECKS = 0
ACTIVE = {}


def check(test, label):
    global CHECKS
    CHECKS += 1
    if not test:
        raise AssertionError(label)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve(name):
    return ROOT / name if name.startswith('program-worktree/') else J / name


def write_new(path, value):
    data = json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
    with path.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    path.chmod(0o444)
    return hashlib.sha256(data).hexdigest()


def seal(pins, name, expected):
    check(name not in pins or pins[name] == expected, ('pin_collision', name))
    check(sha(resolve(name)) == expected, ('input_seal', name))
    pins[name] = expected


def note_pins(pins, name):
    for line in resolve(name).read_text().splitlines():
        if line.startswith('| '):
            cells = [s.strip() for s in line.strip('|').split('|')]
            if len(cells) == 2 and len(cells[1]) == 64:
                seal(pins, cells[0], cells[1])


def authenticate():
    pins = {}
    for name, expected in DIRECT.items():
        seal(pins, name, expected)
    seal(pins, PROTOCOL, PROTOCOL_SHA)
    seal(pins, Path(__file__).name, sha(Path(__file__)))
    for note in (NOTE, 'LOCAL_RECORD_FEEDBACK_Q4_CONSERVING_FORMATION_CANDIDATE_V001.md',
                 'LOCAL_RECORD_FEEDBACK_CONSTRAINED_COUNT_BACKGROUND_ACTION_V001.md'):
        note_pins(pins, note)
    parent = json.loads((J / (PARENT + '_RESULT.json')).read_text())
    receipt = json.loads((J / (PARENT + '_RECEIPT.json')).read_text())
    check(parent['status'] == 'EXACT_SPARSE_Q4_OPERATOR_IDENTITIES_PASSED', 'parent_status')
    check((parent['base_vertices'], parent['base_edges'], parent['columns'], parent['Gram_entries_checked'])
          == (54, 108, 207360, 1492992), 'parent_census')
    check(parent['native_coefficients'] == {'U': 1, 'EP': 1, 'lambda': '1/2', 'j': '1/4',
                                          't': '1/10', 'h': '1/5', 'Delta': 0}, 'native_tuple')
    check(parent['pins'] == receipt['pins'] and receipt['raw_sha256'] == DIRECT[PARENT + '_RESULT.json'],
          'parent_receipt')
    seal(pins, PARENT + '_RESULT.md', receipt['report_sha256'])
    for name, expected in parent['pins'].items():
        seal(pins, name, expected)
    cp = J / 'q4_sparse_insertion_verification_v001_checkpoints'
    expected_names = {'OWNER_START.json'} | {f'F{length}_{suffix}.json{commit}'
        for length in (2, 3) for suffix in ('background0', 'background1', 'background2', 'GRAM')
        for commit in ('', '.COMMIT.json')}
    check(set(receipt['checkpoint_sha256']) == expected_names == set(p.name for p in cp.iterdir()),
          'parent_checkpoint_census')
    for name, expected in receipt['checkpoint_sha256'].items():
        seal(pins, str(Path(cp.name) / name), expected)
    owner = json.loads((cp / 'OWNER_START.json').read_text())
    check(owner['pins'] == parent['pins'] and owner['pid'] == receipt['pid'], 'parent_owner')
    for row in parent['rows'] + parent['grams']:
        suffix = 'GRAM' if 'entries_checked' in row else 'background' + str(row['background'])
        name = f"F{row['length']}_{suffix}.json"
        check(json.loads((cp / name).read_text()) == row, ('parent_row', name))
        check(json.loads((cp / (name + '.COMMIT.json')).read_text()) == {
            'checkpoint_name': name, 'checkpoint_sha256': sha(cp / name), 'pins': parent['pins'],
            'status': 'COMPLETE_EXACT_CHECKS_PASSED'}, ('parent_commit', name))
    check(not (J / (PARENT + '_ERROR.json')).exists(), 'parent_no_error')
    return pins, parent


def add(out, state, value):
    total = tuple(a + b for a, b in zip(out.get(state, ZERO), value))
    if total != ZERO:
        out[state] = total
    else:
        out.pop(state, None)


def offdiag(a0, a1):
    return (a0, 0, 0, a1, 0, 0) * 2


def compare(actual, expected, label):
    if actual != expected:
        def serial(mapping):
            return [[str(w), c, str(q), list(v)] for (w, c, q), v in sorted(mapping.items())]
        ACTIVE['failed_actual'] = serial(actual)
        ACTIVE['failed_expected'] = serial(expected)
    check(actual == expected, label)


@lru_cache(maxsize=256)
def degrees(edges, vertices, word):
    d = [0] * vertices
    for e, (a, b) in enumerate(edges):
        if (word >> e) & 1:
            d[a] += 1
            d[b] += 1
    return tuple(d)


def native_graph():
    cells = tuple(itertools.product(range(3), repeat=3))
    index = {r: i for i, r in enumerate(cells)}
    edges = tuple((i, 27 + index[tuple((r[k] + s[k]) % 3 for k in range(3))])
        for i, r in enumerate(cells) for s in ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)))
    cuts = tuple(4 * index[r] for r in ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)))
    return edges, cuts


class DonorF2:
    def __init__(self, edges, cuts):
        self.old, self.cuts = edges, cuts
        self.keep = tuple(e for e in range(108) if e not in cuts)
        target = [edges[e] for e in self.keep]
        paths = []
        for e in cuts:
            a, b = edges[e]
            paths.append((len(target), len(target) + 1))
            target.extend(((a, 55), (54, b)))
        self.new, self.paths = tuple(target), tuple(paths)
        self.ell_old = tuple(1 if v == W else 0 for v in range(54))
        self.ell_new = self.ell_old + (1, 2)

    @lru_cache(maxsize=256)
    def encode_word(self, word):
        value = sum(((word >> e) & 1) << i for i, e in enumerate(self.keep))
        for e, path in zip(self.cuts, self.paths):
            for k in path:
                value |= ((word >> e) & 1) << k
        return value

    def forward(self, state):
        word, carrier, q = state
        return None if not (q >> W) & 1 else (self.encode_word(word), carrier, q ^ (1 << W))

    @lru_cache(maxsize=32768)
    def decode_word(self, word):
        pairs = [tuple((word >> k) & 1 for k in path) for path in self.paths]
        if any(a != b for a, b in pairs):
            return None
        value = sum(((word >> i) & 1) << e for i, e in enumerate(self.keep))
        for e, bits in zip(self.cuts, pairs):
            value |= bits[0] << e
        return value

    def reverse(self, state):
        word, carrier, q = state
        old = self.decode_word(word)
        if old is None or carrier >= 54 or q >> 54 or (q >> W) & 1:
            return None
        return old, carrier, q | (1 << W)


def action(edges, vertices, ell, state):
    """Complete g=0 Nc1 operator; independent cap and midpoint source coefficients."""
    word, carrier, q = state
    d = degrees(edges, vertices, word)
    qb = [(q >> v) & 1 for v in range(vertices)]
    c = [dv - 2 for dv in d]
    cap0 = sum(80 * cv * cv - 40 * qv * cv for cv, qv in zip(c, qb)) + 80
    cap1 = sum(ell[v] * (80 * c[v] ** 2 - 40 * qb[v] * c[v]) for v in range(vertices)) + 80 * ell[carrier]
    mid0 = sum(80 * cv * cv for cv in c) + 80 * sum(qb) + 80
    mid1 = sum(ell[v] * (80 * c[v] ** 2 + 80 * qb[v]) for v in range(vertices)) + 80 * ell[carrier]
    current0 = current1 = 0
    out = {}
    for e, (a, b) in enumerate(edges):
        es = ell[a] + ell[b]
        add(out, (word ^ (1 << e), carrier, q), offdiag(-16, -8 * es))
        if (word >> e) & 1:
            mid0 -= 40 * (qb[a] + qb[b])
            mid1 -= 20 * es * (qb[a] + qb[b])
            if carrier in (a, b):
                current0 += 20
                current1 += 10 * es
                add(out, (word, b if carrier == a else a, q), offdiag(-8, -4 * es))
    ar0, ar1 = 80 * sum(qb), 80 * sum(e * qv for e, qv in zip(ell, qb))
    self0, self1 = 80 * vertices, 80 * sum(ell)
    add(out, state, (cap0 + current0, ar0, self0, cap1 + current1, ar1, self1,
                     mid0 + current0, ar0, self0, mid1 + current1, ar1, self1))
    return out


def independent_d(inc, state):
    word, carrier, q = state
    if not (q >> W) & 1:
        return {}
    bits = [(word >> e) & 1 for e in inc.cuts]
    cw = degrees(inc.old, 54, word)[W] - 2
    qp = q ^ (1 << W)
    ea, eb = inc.ell_new[54], inc.ell_new[55]
    newcost = (sum(bits) - 2) ** 2
    current1 = redirect1 = 0
    out = {}
    for e, n in zip(inc.cuts, bits):
        a, b = inc.old[e]
        es = inc.ell_old[a] + inc.ell_old[b]
        add(out, (word ^ (1 << e), carrier, q), offdiag(16, 8 * es))
        if n and carrier in (a, b):
            add(out, (word, b if carrier == a else a, q), offdiag(8, 4 * es))
        current1 += 10 * n * ((eb - inc.ell_old[b]) * (carrier == a) + (ea - inc.ell_old[a]) * (carrier == b))
        redirect1 -= 20 * n * ((eb - inc.ell_old[b]) * ((qp >> a) & 1)
                               + (ea - inc.ell_old[a]) * ((qp >> b) & 1))
    ew = inc.ell_old[W]
    donor_mid1 = -80 * ew + 20 * sum((inc.ell_old[a] + inc.ell_old[b])
        for e, (a, b) in enumerate(inc.old) if W in (a, b) and (word >> e) & 1)
    native0 = 160 * newcost + 40 * cw
    cap1 = 80 * (ea + eb) * newcost + current1 + 40 * ew * cw
    mid1 = 80 * (ea + eb) * newcost + current1 + redirect1 + donor_mid1
    add(out, state, (native0, -80, 160, cap1, -80 * ew, 80 * (ea + eb),
                     native0, -80, 160, mid1, -80 * ew, 80 * (ea + eb)))
    return out


def independent_leak(inc, state):
    target = inc.forward(state)
    if target is None:
        return {}
    word, carrier, q = target
    out = {}
    for path in inc.paths:
        for e in path:
            a, b = inc.new[e]
            es = inc.ell_new[a] + inc.ell_new[b]
            add(out, (word ^ (1 << e), carrier, q), offdiag(-16, -8 * es))
            if (word >> e) & 1 and carrier in (a, b):
                add(out, (word, b if carrier == a else a, q), offdiag(-8, -4 * es))
    return out


def residual(inc, state):
    target = inc.forward(state)
    out = {} if target is None else action(inc.new, 56, inc.ell_new, target)
    for old, value in action(inc.old, 54, inc.ell_old, state).items():
        mapped = inc.forward(old)
        if mapped is not None:
            add(out, mapped, tuple(-v for v in value))
    image, outside = {}, {}
    for target, value in out.items():
        old = inc.reverse(target)
        add(outside if old is None else image, target if old is None else old, value)
    return image, outside


def staggered(q, vertices):
    return sum(((q >> v) & 1) * (1 if v < 27 or v == 54 else -1) for v in range(vertices))


def group(inc, bg, background, records):
    rows, eligible = [], 0
    for n, carrier, ri in itertools.product(range(16), range(54), range(20)):
        q = records[ri]
        word = background | sum(((n >> i) & 1) << e for i, e in enumerate(inc.cuts))
        state = (word, carrier, q)
        ACTIVE.clear()
        ACTIVE.update(background=bg, cut_word=n, carrier=carrier, record_index=ri,
                      incidence_word=str(word), record_word=str(q))
        target = inc.forward(state)
        gate = (q >> W) & 1
        check((target is not None) == bool(gate), 'T_gate_TdaggerT')
        if target is not None:
            eligible += 1
            check(inc.reverse(target) == state and inc.forward(inc.reverse(target)) == target, 'partial_isometry')
            check(target[1] == carrier and target[2].bit_count() == q.bit_count() - 1, 'carrier_Q_map')
            oldK, newK = staggered(q, 54), staggered(target[2], 56)
            check(newK == oldK - 1 and -newK == -oldK + 1, 'staggered_return_map')
            check(27 + gate == 28 + ((target[2] >> W) & 1), 'count_donor_resource')
            check(-27 <= -oldK <= 26 and -28 <= -newK <= 28, 'nonwrapping_occupied_return_shift')
            check(degrees(inc.old, 54, word) == degrees(inc.new, 56, target[0])[:54], 'old_degrees')
            for edges, vertices, w in ((inc.old, 54, word), (inc.new, 56, target[0])):
                check(sum((1 if v < 27 or v == 54 else -1) * (4 - 2 * d)
                          for v, d in enumerate(degrees(edges, vertices, w))) == 0, 'paired_port_charge')
        image, outside = residual(inc, state)
        expected_d, expected_l = independent_d(inc, state), independent_leak(inc, state)
        compare(image, expected_d, 'complete_H1T_TH0_image')
        compare(outside, expected_l, 'complete_H1T_TH0_leakage')
        if not gate:
            check(not image and not outside, 'ineligible_zero_operator')
        diagonal = list(image.get(state, ZERO)) if gate else None
        rows.append([n, carrier, ri, bool(gate), q.bit_count(), staggered(q, 54),
                     degrees(inc.old, 54, word)[W] - 2, diagonal])
    check(len(rows) == 17280 and len({tuple(r[:3]) for r in rows}) == 17280, 'unique_group_columns')
    check(eligible == 8640, 'eligible_group_census')
    return {'background': bg, 'old_columns': 17280, 'eligible': eligible, 'ineligible': 17280 - eligible,
            'row_columns': ['cut_word', 'carrier', 'record_index', 'eligible', 'old_Q', 'old_K', 'c_w', 'diagonal_coefficients'],
            'coefficient_order': COEFFICIENTS, 'rows': rows}


def execute(args):
    start = time.time()
    check(args.protocol_sha == PROTOCOL_SHA, 'launch_protocol')
    pins, parent = authenticate()
    edges, cuts = native_graph()
    check(parent['cuts'] == [list(edges[e]) for e in cuts], 'parent_cuts')
    inc = DonorF2(edges, cuts)
    check(len(set(edges)) == 108 and len(set(inc.new)) == 112, 'graph_edge_census')
    check(degrees(edges, 54, (1 << 108) - 1) == (4,) * 54
          and degrees(inc.new, 56, (1 << 112) - 1) == (4,) * 56, 'q4_eligibility_graphs')
    check(edges[cuts[0]][0] == W, 'fixed_donor_A000')
    endpoints = [v for e in cuts for v in edges[e]]
    check(len(set(endpoints)) == 8, 'disjoint_cut_endpoints')
    allq = (1 << 54) - 1
    records = [0, allq, sum(1 << v for v in range(0, 54, 2)), sum(1 << v for v in range(1, 54, 2))]
    records += [1 << v for v in endpoints] + [allq ^ (1 << v) for v in endpoints]
    check(len(set(records)) == 20 and sum((q >> W) & 1 for q in records) == 10, 'record_pattern_gate')
    cutmask = sum(1 << e for e in cuts)
    backgrounds = [0, ((1 << 108) - 1) ^ cutmask,
                   sum(1 << e for e in range(108) if e not in cuts and e % 2)]
    cp = J / 'native_record_donor_sparse_verification_v001_checkpoints'
    cp.mkdir()
    write_new(cp / 'OWNER_START.json', {'pid': os.getpid(), 'pins': pins, 'time': start})
    groups = []
    for bg, background in enumerate(backgrounds):
        data = group(inc, bg, background, records)
        data['pins'] = pins
        name = f'background{bg}.json'
        h = write_new(cp / name, data)
        write_new(cp / (name + '.COMMIT.json'), {'name': name, 'sha256': h, 'pins': pins,
                  'old_columns': 17280, 'status': 'COMPLETE_EXACT_DONOR_OPERATOR_CHECKS_PASSED'})
        groups.append({'background': bg, 'old_columns': data['old_columns'], 'eligible': data['eligible'],
                       'ineligible': data['ineligible'], 'file': str(Path(cp.name) / name), 'sha256': h})
    check(sum(g['old_columns'] for g in groups) == 51840 and sum(g['eligible'] for g in groups) == 25920
          and sum(g['ineligible'] for g in groups) == 25920, 'full_census')
    for name, expected in pins.items():
        check(sha(resolve(name)) == expected, ('pre_output_seal', name))
    result = {'status': 'EXACT_NATIVE_RECORD_DONOR_OPERATOR_AND_SOURCE_IDENTITIES_PASSED',
              'pins': pins, 'checks': CHECKS, 'unique_old_columns': 51840, 'eligible': 25920, 'ineligible': 25920,
              'groups': groups, 'native_integer_scale': 80, 'coefficient_order': COEFFICIENTS,
              'donor_vertex': W, 'copy_native': 0, 'count_increment': 1,
              'old_edges': [list(e) for e in edges], 'new_edges': [list(e) for e in inc.new], 'cuts': list(cuts),
              'old_record_words': [str(q) for q in records], 'old_background_words': [str(w) for w in backgrounds],
              'affine_direction_old': list(inc.ell_old), 'affine_direction_new': list(inc.ell_new),
              'AR_Sself': 'literal independent symbolic coefficient columns; no value selected',
              'source_scope': 'uniform plus one affine direction in both allocations; not every nodal or physical strain jet',
              'donor_and_precursor_physical_completion': False, 'field_or_background_solved': False,
              'elapsed_seconds': time.time() - start}
    raw, report, receipt = [J / (STEM + suffix) for suffix in ('_RESULT.json', '_RESULT.md', '_RECEIPT.json')]
    raw_sha = write_new(raw, result)
    text = '# F2 native-record donor verification V001\n\n' + result['status'] + '\n\n'
    text += 'All 51,840 distinct old bases retained: 25,920 occupied-donor isometries and 25,920 blank-donor zero maps. '
    text += 'Complete old/new H1T−TH0, image/leakage, resource, Q/K/return and symbolic AR/self identities agree exactly. '
    text += 'Both cap and midpoint sources retain uniform and one frozen affine-direction coefficient. No Gram or old trajectory was rerun.\n\n'
    text += 'Three sealed bundles retain every basis eligibility and signed diagonal coefficient. Active copy, physical donor preparation/gauge/precursor/collar/support and complete absolute work remain open; no physical parameter, pressure or cosmological state is chosen.\n\n'
    text += f'Exact checks: {CHECKS}; raw SHA256: {raw_sha}.\n'
    with report.open('x') as stream:
        stream.write(text)
        stream.flush()
        os.fsync(stream.fileno())
    report.chmod(0o444)
    for name, expected in pins.items():
        if sha(resolve(name)) != expected:
            raise AssertionError(('post_output_input_changed', name))
    receipt_sha = write_new(receipt, {'pins': pins, 'pid': os.getpid(), 'checks': CHECKS,
        'unique_old_columns': 51840, 'eligible': 25920, 'ineligible': 25920, 'raw_sha256': raw_sha,
        'report_sha256': sha(report), 'checkpoint_sha256': {p.name: sha(p) for p in sorted(cp.iterdir())},
        'elapsed_seconds': result['elapsed_seconds']})
    print(json.dumps({'status': result['status'], 'checks': CHECKS, 'columns': 51840,
                      'raw_sha256': raw_sha, 'receipt_sha256': receipt_sha, 'seconds': result['elapsed_seconds']}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--protocol-sha', required=True)
    args = parser.parse_args()
    if not args.execute:
        raise SystemExit('No action: full frozen reviews and root-only launch required.')
    reserved = [J / (STEM + s) for s in ('_RESULT.json', '_RESULT.md', '_RECEIPT.json', '_ERROR.json')]
    reserved.append(J / 'native_record_donor_sparse_verification_v001_checkpoints')
    if any(p.exists() for p in reserved):
        raise SystemExit('Reserved output exists; preserve it and use a distinct reviewed recovery.')
    try:
        execute(args)
    except BaseException as error:
        path = J / (STEM + '_ERROR.json')
        if not path.exists():
            write_new(path, {'status': 'EXECUTION_ERROR_PRESERVED', 'pid': os.getpid(), 'checks': CHECKS,
                'active_context': ACTIVE, 'error_type': type(error).__name__, 'message': str(error),
                'traceback': traceback.format_exc()})
        raise

"""New exact coherent-cut functionals from proved D/K expressions; no network H replay."""
import argparse
from fractions import Fraction
import hashlib
import itertools
import json
import math
import os
from pathlib import Path
import time
import traceback

J = Path(__file__).resolve().parent
ROOT = J.parent.parent
STEM = 'LOCAL_RECORD_FEEDBACK_NATIVE_DONOR_COHERENT_CUT_FUNCTIONALS_V001'
PARENT = 'LOCAL_RECORD_FEEDBACK_NATIVE_RECORD_DONOR_SPARSE_VERIFICATION_V001'
PROTOCOL_SHA = 'a29a5e645035de88e3d70f9b301ac90895eccc96cc34a5e9b555c0eea3fe433a'
DIRECT = {
    'LOCAL_RECORD_FEEDBACK_NATIVE_RECORD_DONOR_FORMATION_V001.md': '45b99f9642d9cf757460cb8a65ea1d27f1bbb9eac9b23674b1cf879adeabed4f',
    'LOCAL_RECORD_FEEDBACK_Q4_CONSERVING_FORMATION_CANDIDATE_V001.md': '07323053b75b947b35712f0ac8fc4ce04c2766131cd4e684fd64167321b51f3c',
    'LOCAL_RECORD_FEEDBACK_Q4_CONDITIONAL_NEWSTAR_QUERY_V001.md': '34eb3374dfeb849fb24d85dd305e1a1e791c3b15392bfccd097456626fe92ff3',
    PARENT + '.md': '9706c0e14a348c701882ff408e94abe2bc452773ef66fbfdd30d135dc92da11d',
    'local_record_feedback_native_record_donor_sparse_verification_v001.py': '85dbd31c4f76d493df2394f44a18320ccdb83f170d67efea0109e15c6d69da55',
    PARENT + '_RESULT.json': 'f465ccc297862549327a77477ce8853cf06d3962b77d691902c9ad7183eeb137',
    PARENT + '_RECEIPT.json': '97ef886df76a0b64afa849b58ef121a42e91661a80d9b3f402698d58f215a93e',
}
PREPS = ['product_plus_X', 'product_minus_X', 'product_plus_Y', 'product_minus_Y',
         'uniform16_mixed', 'ice6_mixed', 'ice6_coherent_plus', 'fixed_ice_word3',
         'ice_pair_mixed', 'ice_pair_coherent_plus', 'ice_pair_coherent_minus']
ICE = [3, 5, 6, 9, 10, 12]
PORTS = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
PAIRS = list(itertools.combinations(range(4), 2))
CONTROL_PAIRS = list(itertools.combinations(range(5), 2)) + [(5, 6), (8, 9), (8, 10), (9, 10)]
CHECKS = 0
ACTIVE = {}


def check(test, label):
    global CHECKS
    CHECKS += 1
    if not test:
        ACTIVE['failed_control'] = label
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


def authenticate(pins):
    for name, expected in DIRECT.items():
        seal(pins, name, expected)
    for note in list(DIRECT)[:3]:
        for line in (J / note).read_text().splitlines():
            if line.startswith('| '):
                cells = [x.strip() for x in line.strip('|').split('|')]
                if len(cells) == 2 and len(cells[1]) == 64:
                    seal(pins, cells[0], cells[1])
    seal(pins, STEM + '.md', PROTOCOL_SHA)
    seal(pins, Path(__file__).name, sha(Path(__file__)))
    parent = json.loads((J / (PARENT + '_RESULT.json')).read_text())
    receipt = json.loads((J / (PARENT + '_RECEIPT.json')).read_text())
    check(parent['status'] == 'EXACT_NATIVE_RECORD_DONOR_OPERATOR_AND_SOURCE_IDENTITIES_PASSED', 'parent_status')
    check((parent['unique_old_columns'], parent['eligible'], parent['ineligible']) == (51840, 25920, 25920), 'parent_census')
    check(parent['pins'] == receipt['pins'] and receipt['raw_sha256'] == DIRECT[PARENT + '_RESULT.json'], 'parent_receipt')
    for name, expected in parent['pins'].items():
        seal(pins, name, expected)
    seal(pins, PARENT + '_RESULT.md', receipt['report_sha256'])
    cp = J / 'native_record_donor_sparse_verification_v001_checkpoints'
    expected_names = {'OWNER_START.json'} | {f'background{k}.json{s}' for k in range(3) for s in ('', '.COMMIT.json')}
    check(set(receipt['checkpoint_sha256']) == expected_names == {p.name for p in cp.iterdir()}, 'parent_cp_census')
    for name, expected in receipt['checkpoint_sha256'].items():
        seal(pins, str(Path(cp.name) / name), expected)
    owner = json.loads((cp / 'OWNER_START.json').read_text())
    check(owner['pins'] == parent['pins'] and owner['pid'] == receipt['pid'], 'parent_owner')
    for group in parent['groups']:
        path = J / group['file']
        commit = json.loads(Path(str(path) + '.COMMIT.json').read_text())
        check(commit == {'name': path.name, 'sha256': group['sha256'], 'old_columns': group['old_columns'],
                         'pins': parent['pins'], 'status': 'COMPLETE_EXACT_DONOR_OPERATOR_CHECKS_PASSED'}, 'parent_commit')
        check(sha(path) == group['sha256'], 'parent_group_digest')
    check(not (J / (PARENT + '_ERROR.json')).exists(), 'parent_no_error')
    check(parent['affine_direction_old'] == [1] + [0] * 53 and
          parent['affine_direction_new'] == [1] + [0] * 53 + [1, 2], 'source_profile')
    check((len(parent['old_edges']), len(parent['new_edges']), len(parent['cuts'])) == (108, 112, 4), 'graph_sizes')
    check(parent['donor_vertex'] == 0 and parent['copy_native'] == 0 and parent['count_increment'] == 1, 'held_donor_tuple')
    return pins, parent


def gauss(a, b=0, den=1):
    check(den > 0, 'positive_rational_denominator')
    divisor = math.gcd(math.gcd(abs(a), abs(b)), den)
    return {'numerator': [a // divisor, b // divisor], 'denominator': den // divisor}


def real(x):
    x = Fraction(x)
    return [x.numerator, x.denominator]


def multiply(a, b):
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def densities():
    out = []
    for p, label in enumerate(PREPS):
        matrix = [[(0, 0) for _ in range(16)] for _ in range(16)]
        pure = p in (0, 1, 2, 3, 6, 7, 9, 10)
        if p < 4:
            den = 16
            powers = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            phase = powers[p]
            amplitudes = []
            for word in range(16):
                value = (1, 0)
                for _ in range(word.bit_count()):
                    value = multiply(value, phase)
                amplitudes.append(value)
        else:
            words = list(range(16)) if p == 4 else ICE if p in (5, 6) else [3] if p == 7 else [3, 12]
            den = len(words)
            amplitudes = [(0, 0)] * 16
            for word in words:
                amplitudes[word] = (-1, 0) if p == 10 and word == 12 else (1, 0)
        if pure:
            for a in range(16):
                for b in range(16):
                    matrix[a][b] = multiply(amplitudes[a], (amplitudes[b][0], -amplitudes[b][1]))
        else:
            for word in words:
                matrix[word][word] = (1, 0)
        check(sum(matrix[w][w][0] for w in range(16)) == den, ('density_trace', label))
        check(all(matrix[a][b] == (matrix[b][a][0], -matrix[b][a][1])
                  for a in range(16) for b in range(16)), ('density_hermitian', label))
        if pure:
            for a in range(16):
                for b in range(16):
                    terms = [multiply(matrix[a][k], matrix[k][b]) for k in range(16)]
                    check((sum(x[0] for x in terms), sum(x[1] for x in terms)) ==
                          (den * matrix[a][b][0], den * matrix[a][b][1]), ('pure_density_idempotent', label))
        out.append((matrix, den))
    return out


def trace_kernel(rho, kernel):
    a = b = 0
    for i in range(16):
        for j, value in kernel[i].items():
            z = rho[j][i]
            a += value * z[0]
            b += value * z[1]
    return a, b


def query(rho, den, prep):
    weights = [rho[w][w][0] for w in range(16)]
    z = [[1 - 2 * ((w >> i) & 1) for i in range(4)] for w in range(16)]
    x = [[sum(PORTS[i][a] * z[w][i] for i in range(4)) // 2 for a in range(3)] for w in range(16)]
    mz = [Fraction(sum(weights[w] * z[w][i] for w in range(16)), den) for i in range(4)]
    pairs = [Fraction(sum(weights[w] * z[w][i] * z[w][j] for w in range(16)), den) for i, j in PAIRS]
    mx = [Fraction(sum(weights[w] * x[w][a] for w in range(16)), den) for a in range(3)]
    g = [[Fraction(sum(weights[w] * x[w][a] * x[w][b] for w in range(16)), den) - mx[a] * mx[b]
          for b in range(3)] for a in range(3)]
    for a in range(3):
        for b in range(3):
            via_pair = Fraction(int(a == b)) + sum(Fraction(PORTS[i][a] * PORTS[j][b] + PORTS[j][a] * PORTS[i][b], 4) * pairs[k]
                                                     for k, (i, j) in enumerate(PAIRS)) - mx[a] * mx[b]
            check(g[a][b] == via_pair, 'query_pair_mean_dyad_identity')
    determinant = g[0][0] * (g[1][1] * g[2][2] - g[1][2] * g[2][1]) - g[0][1] * (g[1][0] * g[2][2] - g[1][2] * g[2][0]) + g[0][2] * (g[1][0] * g[2][1] - g[1][1] * g[2][0])
    minors = [g[a][a] * g[b][b] - g[a][b] * g[b][a] for a, b in itertools.combinations(range(3), 2)]
    check(determinant >= 0 and min(minors) >= 0 and min(g[a][a] for a in range(3)) >= 0, 'query_psd')
    rank = 3 if determinant else 2 if any(minors) else 1 if any(g[a][a] for a in range(3)) else 0
    sx = []
    xx = []
    for i in range(4):
        sx.append(sum(rho[w ^ (1 << i)][w][0] for w in range(16)))
    for i, j in PAIRS:
        xx.append(sum(rho[w ^ (1 << i) ^ (1 << j)][w][0] for w in range(16)))
    degree = [sum(weights[w] for w in range(16) if w.bit_count() == s) for s in range(5)]
    check(sum(g[a][a] for a in range(3)) == 4 - Fraction(sum(weights[w] * (w.bit_count() - 2) ** 2 for w in range(16)), den) - sum(y * y for y in mx), 'query_trace')
    expected = [Fraction(1)] * 5 + [Fraction(4, 3)] * 2 + [Fraction(0)] + [Fraction(4)] * 3
    check(rank == ([3] * 7 + [0, 1, 1, 1])[prep], 'query_frozen_rank')
    target = [[expected[prep] * int(a == b) if prep < 7 else Fraction(4 * int(a == b == 0)) if prep >= 8 else Fraction(0) for b in range(3)] for a in range(3)]
    check(g == target, 'query_frozen_table')
    check(mx == ([Fraction(-2), Fraction(0), Fraction(0)] if prep == 7 else [Fraction(0)] * 3), 'query_frozen_mean')
    result = {'Z_mean': list(map(real, mz)), 'pair_mean': list(map(real, pairs)), 'm': list(map(real, mx)),
              'G': [[real(v) for v in row] for row in g], 'rank_G': rank, 'rank_joint': rank,
              'joint_covariance': [[real(g[a % 3][b % 3] * (1 if (a < 3) == (b < 3) else -1)) for b in range(6)] for a in range(6)],
              'X_mean': [real(Fraction(v, den)) for v in sx], 'XX_mean': [real(Fraction(v, den)) for v in xx],
              'degree_probabilities': [real(Fraction(v, den)) for v in degree], 'density_numerator': rho, 'density_denominator': den}
    return result


def cut_operators(background, carrier_class, q, anchors):
    pa = [int(carrier_class == 2 * i) for i in range(4)]
    pb = [int(carrier_class == 2 * i + 1) for i in range(4)]
    diagonals = [[], [], []]
    for word in range(16):
        ns = [(word >> i) & 1 for i in range(4)]
        s = sum(ns)
        dw = [0, 3, 2][background] + ns[0]
        f0 = 160 * (s - 2) ** 2 + 40 * (dw - 2)
        fc = 240 * (s - 2) ** 2 + 40 * (dw - 2) + 20 * sum(ns[i] * pa[i] for i in range(4)) + 10 * sum(ns[i] * pb[i] for i in range(1, 4))
        fm = fc - 40 * sum(ns[i] * ((q >> anchors[i][0]) & 1) for i in range(1, 4)) - 20 * sum(ns[i] * ((q >> anchors[i][1]) & 1) for i in range(1, 4)) - 20 * dw
        for values, f in zip(diagonals, (f0, fc, fm)):
            values.append(f)
    flip = [[16] * 4, [8, 0, 0, 0], [8, 0, 0, 0]]
    hop = [[8] * 4, [4, 0, 0, 0], [4, 0, 0, 0]]
    ops = []
    for f, a in zip(diagonals, flip):
        ops.append([{w: f[w], **{w ^ (1 << i): a[i] for i in range(4) if a[i]}} for w in range(16)])
    products = []
    for j in range(3):
        for l in range(3):
            kernel = []
            for a in range(16):
                row = {}
                for k, av in ops[j][a].items():
                    for b, bv in ops[l][k].items():
                        row[b] = row.get(b, 0) + av * bv
                returned = sum(hop[j][i] * hop[l][i] * ((a >> i) & 1) * (pa[i] + pb[i]) for i in range(4))
                row[a] = row.get(a, 0) + returned
                for b in range(16):
                    oracle = int(a == b) * (diagonals[j][a] * diagonals[l][a] + returned)
                    oracle += sum((diagonals[j][a] * flip[l][i] + flip[j][i] * diagonals[l][b]) * int(b == a ^ (1 << i)) for i in range(4))
                    oracle += sum(flip[j][i] * flip[l][k] * int(b == a ^ (1 << i) ^ (1 << k)) for i in range(4) for k in range(4))
                    check(row.get(b, 0) == oracle, 'independent_ordered_D_second_entry')
                kernel.append(row)
            products.append(kernel)
    return ops, products, pa, pb


def functional(rho, den, ops, products, pa, pb, prep):
    means = [trace_kernel(rho, a) for a in ops]
    second = [trace_kernel(rho, a) for a in products]
    check(all(y == 0 for _, y in means), 'real_D_means')
    cov = [(second[3 * j + l][0] * den - means[j][0] * means[l][0], second[3 * j + l][1] * den)
           for j in range(3) for l in range(3)]
    for j in range(3):
        check(cov[3 * j + j][1] == 0 and cov[3 * j + j][0] >= 0, 'D_variance_nonnegative')
        for l in range(3):
            check(cov[3 * j + l] == (cov[3 * l + j][0], -cov[3 * l + j][1]), 'ordered_D_covariance_conjugation')
    weights = [rho[w][w][0] for w in range(16)]
    ni = [sum(weights[w] * ((w >> i) & 1) for w in range(16)) for i in range(4)]
    xi = [sum(rho[w ^ (1 << i)][w][0] for w in range(16)) for i in range(4)]
    ls, rs = [3, 2, 2, 2], [1] * 4
    flip_k = [512 * sum(den + v for v in xi), 256 * sum((ls[i] + rs[i]) * (den + xi[i]) for i in range(4)),
              sum(64 * (ls[i] ** 2 + rs[i] ** 2) * den + 128 * ls[i] * rs[i] * xi[i] for i in range(4))]
    hop_k = [64 * sum(ni[i] * (pa[i] + pb[i]) for i in range(4)),
             64 * sum(ni[i] * (ls[i] * pa[i] + rs[i] * pb[i]) for i in range(4)),
             16 * sum(ni[i] * (ls[i] ** 2 * pa[i] + rs[i] ** 2 * pb[i]) for i in range(4))]
    oracle = [4096, 6656, 2752] if prep == 0 else [0, 0, 448] if prep == 1 else [2048, 3328, 1600]
    check(flip_k == [den * v for v in oracle], 'prospective_flip_kappa_polynomial')
    kappa = [flip_k[i] + hop_k[i] for i in range(3)]
    variance_polynomials = [{
        'constant': gauss(*cov[0], den * den * 6400),
        'linear': gauss(cov[l][0] + cov[3 * l][0], cov[l][1] + cov[3 * l][1], den * den * 6400),
        'quadratic': gauss(*cov[3 * l + l], den * den * 6400)} for l in (1, 2)]
    return {'D_native_means': [gauss(a, b, den * 80) for a, b in means],
            'D_native_ordered_second': [gauss(a, b, den * 6400) for a, b in second],
            'D_ordered_covariance': [gauss(a, b, den * den * 6400) for a, b in cov],
            'kappa_polynomial': [gauss(v, den=den * 6400) for v in kappa],
            'kappa_flip_polynomial': [gauss(v, den=den * 6400) for v in flip_k],
            'kappa_hop_polynomial': [gauss(v, den=den * 6400) for v in hop_k],
            'kappa_xx': gauss(2 * kappa[2], den=den * 6400), 'conditional_query_id': prep,
            'source_variance_polynomials_cap_mid': variance_polynomials,
            'symbolic_offsets': ['2*Sself-AR', '3*Sself-AR', '3*Sself-AR'],
            'complete_ordered_second_rule': 'native_second[j,l]+offset[j]*native_mean[l]+offset[l]*native_mean[j]+offset[j]*offset[l]',
            'direct_D_xx': 0, 'physical_energy_unit_selected': False}


def subtract(a, b):
    den = a['denominator'] * b['denominator']
    return gauss(a['numerator'][0] * b['denominator'] - b['numerator'][0] * a['denominator'],
                 a['numerator'][1] * b['denominator'] - b['numerator'][1] * a['denominator'], den)


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    if not args.execute:
        raise SystemExit('requires exact --execute; no calculation performed')
    targets = [J / (STEM + suffix) for suffix in ('_RESULT.json', '_RESULT.md', '_RECEIPT.json', '_ERROR.json')]
    cp = J / 'native_donor_coherent_cut_functionals_v001_checkpoints'
    if any(p.exists() for p in targets + [cp]):
        raise SystemExit('reserved path exists; preserve partials and use a distinct reviewed recovery')
    started = time.monotonic()
    pins = {}
    try:
        pins, parent = authenticate(pins)
        cp.mkdir()
        checkpoint_hashes = {}
        owner = {'pid': os.getpid(), 'started_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'pins': pins}
        checkpoint_hashes['OWNER_START.json'] = write_new(cp / 'OWNER_START.json', owner)
        density = densities()
        catalogue = []
        for p, (rho, den) in enumerate(density):
            ACTIVE.update(preparation=p)
            catalogue.append({'preparation': PREPS[p], **query(rho, den, p)})
        for a, b in CONTROL_PAIRS:
            check([density[a][0][w][w] for w in range(16)] == [density[b][0][w][w] for w in range(16)] and density[a][1] == density[b][1], 'equal_Z_statistics')
            check(catalogue[a]['G'] == catalogue[b]['G'] and catalogue[a]['m'] == catalogue[b]['m'], 'equal_Z_query')
        edges = [tuple(e) for e in parent['old_edges']]
        anchors = [edges[e] for e in parent['cuts']]
        check(parent['cuts'] == [0, 36, 12, 4] and anchors == [(0, 27), (9, 36), (3, 30), (1, 28)], 'cut_bit_registration')
        cut_set = set(parent['cuts'])
        backgrounds = [0, sum(1 << e for e in range(108) if e not in cut_set),
                       sum(1 << e for e in range(108) if e not in cut_set and e % 2)]
        check(parent['old_background_words'] == list(map(str, backgrounds)), 'uncut_background_words')
        check([sum((word >> e) & 1 for e, edge in enumerate(edges) if 0 in edge) for word in backgrounds] == [0, 3, 2], 'donor_uncut_degrees')
        record_words = [int(v) for v in parent['old_record_words']]
        check(len(set(record_words)) == 20 and sum(q & 1 for q in record_words) == 10, 'record_eligibility_census')
        endpoint_list = [v for edge in anchors for v in edge]
        check(len(set(endpoint_list)) == 8, 'disjoint_anchors')
        full_q = (1 << 54) - 1
        expected_q = [0, full_q, sum(1 << v for v in range(0, 54, 2)), sum(1 << v for v in range(1, 54, 2))]
        expected_q += [1 << v for v in endpoint_list] + [full_q ^ (1 << v) for v in endpoint_list]
        check(record_words == expected_q, 'record_pattern_registration')
        carrier_class = [endpoint_list.index(c) if c in endpoint_list else 8 for c in range(54)]
        groups = []
        eligible = ineligible = total_comparisons = actual_case_comparisons = 0
        for background in range(3):
            templates, rows, comparisons = {}, [], []
            for cls in range(9):
                for qindex, q in enumerate(record_words):
                    if not q & 1:
                        continue
                    ACTIVE.update(background=background, carrier_class=cls, record=qindex)
                    ops, products, pa, pb = cut_operators(background, cls, q, anchors)
                    functions = []
                    for p, (rho, den) in enumerate(density):
                        ACTIVE.update(preparation=p)
                        key = f'{cls}:{qindex}:{p}'
                        value = functional(rho, den, ops, products, pa, pb, p)
                        templates[key] = value
                        functions.append(value)
                    for a, b in CONTROL_PAIRS:
                        differences = {k: [subtract(v, w) for v, w in zip(functions[b][k], functions[a][k])]
                            for k in ('D_native_means', 'D_ordered_covariance', 'kappa_polynomial')}
                        comparisons.append({'carrier_class': cls, 'record_index': qindex, 'preparations': [a, b],
                                            'direction': 'second-minus-first', 'differences': differences})
                    check(subtract(functions[0]['D_native_means'][0], functions[1]['D_native_means'][0]) == gauss(8, den=5), 'product_X_D_mean_difference')
            for carrier in range(54):
                for qindex, q in enumerate(record_words):
                    if q & 1:
                        actual_case_comparisons += len(CONTROL_PAIRS)
                    qtotal = q.bit_count()
                    ktotal = sum((1 if v < 27 else -1) * ((q >> v) & 1) for v in range(54))
                    for p in range(11):
                        yes = bool(q & 1)
                        key = f'{carrier_class[carrier]}:{qindex}:{p}' if yes else None
                        check(key is None or key in templates, 'functional_template_reference')
                        rows.append({'carrier': carrier, 'record_index': qindex, 'record_word': str(q), 'preparation': p,
                                     'success_probability': int(yes), 'conditional_template': key,
                                     'status': 'ELIGIBLE_CONDITIONAL_FUNCTIONALS' if yes else 'ZERO_MAP_CONDITIONAL_QUERY_UNDEFINED',
                                     'Q_old': qtotal, 'K_old': ktotal, 'Q_new': qtotal - 1 if yes else None,
                                     'record_word_new': str(q ^ 1) if yes else None,
                                     'new_record_bits': [0, 0] if yes else None,
                                     'K_new': ktotal - 1 if yes else None, 'return_new': -ktotal + 1 if yes else None})
                        eligible += yes
                        ineligible += not yes
            check(len(rows) == 11880 and len(templates) == 990 and len(comparisons) == 1260, 'background_census')
            total_comparisons += len(comparisons)
            bundle = {'background': background, 'rows': rows, 'functional_templates': templates, 'equal_Z_comparisons': comparisons,
                      'pins': pins, 'status': 'EXACT_COHERENT_FUNCTIONALS_PASSED'}
            name = f'background{background}.json'
            digest = write_new(cp / name, bundle)
            checkpoint_hashes[name] = digest
            commit_name = name + '.COMMIT.json'
            checkpoint_hashes[commit_name] = write_new(cp / commit_name, {'checkpoint_name': name, 'checkpoint_sha256': digest,
                'pins': pins, 'status': 'COMPLETE_EXACT_CHECKS_PASSED'})
            groups.append({'background': background, 'rows': len(rows), 'templates': len(templates), 'comparisons': len(comparisons),
                           'file': str(Path(cp.name) / name), 'sha256': digest})
        check((eligible, ineligible, total_comparisons, actual_case_comparisons) == (17820, 17820, 3780, 22680), 'final_census')
        for name, expected in pins.items():
            check(sha(resolve(name)) == expected, ('final_input_seal', name))
        result = {'status': 'EXACT_NATIVE_DONOR_COHERENT_CUT_FUNCTIONALS_PASSED', 'checks': CHECKS, 'pins': pins,
                  'preparation_catalogue': catalogue, 'groups': groups, 'functional_rows': eligible + ineligible,
                  'eligible': eligible, 'ineligible': ineligible, 'equal_Z_template_comparisons': total_comparisons,
                  'equal_Z_actual_carrier_case_comparisons': actual_case_comparisons,
                  'equal_Z_preparation_pair_census': CONTROL_PAIRS, 'carrier_class_by_site': carrier_class,
                  'carrier_sites_by_class': [[c for c in range(54) if carrier_class[c] == cls] for cls in range(9)],
                  'D_order': ['uniform', 'cap_source_derivative', 'mid_source_derivative'],
                  'ordered_D_covariance_layout': 'row-major[j,l]; cap variance uses00,01+10,11; mid uses00,02+20,22',
                  'native_scales': {'D': 80, 'D_second_covariance_kappa': 6400},
                  'same_preparation_all_carriers_and_records': True, 'physical_metric_or_preparation_qualified': False,
                  'closed_two_level_orbit_claimed': False, 'physical_source_units': 'D times Eunit; covariance/kappa times Eunit^2',
                  'elapsed_seconds': time.monotonic() - started}
        raw = write_new(targets[0], result)
        lines = ['# Exact native-donor coherent-cut functionals V001', '',
                 f'All {result["functional_rows"]} rows retained: {eligible} eligible and {ineligible} zero-map refusals.',
                 'This is a mathematical preparation/control packet, not physical metric, preparation, cosmological state or a closed two-level orbit.',
                 'Full rational moments, covariance order and symbolic AR/self rules are losslessly saved in all three referenced bundles.', '',
                 '| Preparation | rank G | m | G |', '|---|---:|---|---|']
        for row in catalogue:
            lines.append(f'| {row["preparation"]} | {row["rank_G"]} | {row["m"]} | {row["G"]} |')
        lines += ['', 'All 3,780 equal-Z functional-template comparisons retain signed differences and exact redundancies; census rows retain all actual carriers.',
                  'Ordered D covariance is retained as complex data; affine Dxx=0 does not remove leakage second contacts or physical source/history contacts.',
                  'Native self/AR identity offsets survive means and complete second moments. No AR, Sself, Eunit, x or preparation work is selected.',
                  f'Exact checks: {CHECKS}. Input seals: {len(pins)}. Result SHA256: {raw}.']
        report = ('\n'.join(lines) + '\n').encode()
        with targets[1].open('xb') as stream:
            stream.write(report)
            stream.flush()
            os.fsync(stream.fileno())
        targets[1].chmod(0o444)
        write_new(targets[2], {'raw_sha256': raw, 'report_sha256': hashlib.sha256(report).hexdigest(), 'pins': pins,
            'checkpoint_sha256': checkpoint_hashes, 'pid': os.getpid(), 'checks': CHECKS,
            'functional_rows': eligible + ineligible, 'eligible': eligible, 'ineligible': ineligible,
            'elapsed_seconds': result['elapsed_seconds']})
        for name, expected in pins.items():
            if sha(resolve(name)) != expected:
                raise AssertionError('post-output input changed ' + name)
        print(json.dumps({'status': result['status'], 'checks': CHECKS, 'rows': eligible + ineligible, 'raw_sha256': raw}))
    except Exception as exc:
        if not targets[3].exists():
            write_new(targets[3], {'status': 'EXECUTION_ERROR_PRESERVED', 'error': repr(exc), 'traceback': traceback.format_exc(),
                                  'active': ACTIVE, 'checks': CHECKS, 'pins': pins, 'pid': os.getpid()})
        raise


if __name__ == '__main__':
    run()

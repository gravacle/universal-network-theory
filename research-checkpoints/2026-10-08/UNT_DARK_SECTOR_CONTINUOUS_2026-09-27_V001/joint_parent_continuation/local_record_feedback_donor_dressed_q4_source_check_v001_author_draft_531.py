"""Guarded prospective exact native donor/source check; root execution only."""
import argparse
import ast
from functools import lru_cache
import hashlib
import itertools
import json
import os
from pathlib import Path
import time
import traceback
from datetime import datetime, timezone

AUTHOR_DRAFT = True
J = Path(__file__).resolve().parent
STEM = 'LOCAL_RECORD_FEEDBACK_DONOR_DRESSED_Q4_SOURCE_CHECK_V001'
PROTOCOL = STEM + '.md'
PINS = {'LOCAL_RECORD_FEEDBACK_NATIVE_RECORD_DONOR_FORMATION_V001.md': '45b99f9642d9cf757460cb8a65ea1d27f1bbb9eac9b23674b1cf879adeabed4f', 'LOCAL_RECORD_FEEDBACK_Q4_CONSERVING_FORMATION_CANDIDATE_V001.md': '07323053b75b947b35712f0ac8fc4ce04c2766131cd4e684fd64167321b51f3c', 'LOCAL_RECORD_FEEDBACK_Q4_SPARSE_INSERTION_VERIFICATION_V001.md': '92f7f9c4cf26befb1eed9d85c2232271629f3088fcdb0342692a74342f589813', 'local_record_feedback_q4_sparse_insertion_verification_v001.py': '774c81de75458fb430009655f83f00dcc24bac423385ac1b72409dc6f160134e', 'LOCAL_RECORD_FEEDBACK_Q4_SPARSE_INSERTION_VERIFICATION_V001_RESULT.json': '8bc5f32488c6bfdeb0312dbb68c681eb4ce88cf1a63a62fef9177013e0a8fd60', 'LOCAL_RECORD_FEEDBACK_Q4_SPARSE_INSERTION_VERIFICATION_V001_RECEIPT.json': '932c46279b44d856e1bdedf2a9a3e2c267ba3e3c59edfe9d64e64f4cebf6d5b8', 'LOCAL_RECORD_FEEDBACK_FLOATING_RETURN_COMPLETION_V001.md': '255ea0ca5f86cc711cae2ff5e746d8e9b005c2156b934818ded7789f9461f2a4', 'LOCAL_PROPER_BOND_NORMALIZATION_V001.md': '9b4cc5e1942ac7373e210efa46bfa74e03bbcfb8130c01232373b02e8a622a5b', 'LOCAL_PROPER_BOND_CONSERVING_CREATION_SOURCE_CONTACT_V001.md': 'e28eb807a3df201d46981898f4f85189cca4d54f7723a7946e13dd3cae8f9d43', 'UNIFIED_REPEATED_COUNT_VOLUME_DEPENDENT_NORMAL_ACTION_V001.md': '4fb8381caae88420093ab43fdb1abaf31451bbe2ff51e77b7d27ff606efd282a', 'LOCAL_RECORD_FEEDBACK_NATIVE_MATERIAL_NORMAL_CURRENT_SOURCE_V001.md': '4ddf27182ec7f24ea60c2a72b24ff3b04ead5929bd30878a1a2c8a97a67b52dd', 'LOCAL_RECORD_FEEDBACK_DONOR_DRESSED_Q4_SOURCE_CHECK_V001.md': '949fa80ba59b95258fc755508b6114d1ea755a40f2dce0396771f191fa13a6af'}
OLD = 'local_record_feedback_q4_sparse_insertion_verification_v001.py'
PARENT = 'LOCAL_RECORD_FEEDBACK_Q4_SPARSE_INSERTION_VERIFICATION_V001'
CP = J / 'local_record_feedback_donor_dressed_q4_source_check_v001_checkpoints'
SCALE, W = 40, 0
CARRIERS = (0, 27, 9, 26)
RECORDS = (0, 1, (1 << 27) - 1, ((1 << 27) - 1) << 27)
ZERO = (0, 0, 0)
CASE_KEYS = ('partial_isometry', 'count_resource', 'record_return', 'full_mismatch',
             'compressed_eligibility', 'outside_leakage', 'donor_commutator',
             'full_action_neutrality', 'absolute_inventory')
PHYSICAL = {k: False for k in ('physical_embedding_selected', 'physical_dilation_checked',
    'Maxwell_birth_interface_checked', 'donor_preparation_solved', 'cosmology_solved',
    'sustained_growth_qualified', 'temperature_or_EOS_derived')}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def utc():
    return datetime.now(timezone.utc).isoformat()


def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def exclusive(p, data):
    with Path(p).open('xb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    Path(p).chmod(0o444)
    return hashlib.sha256(data).hexdigest()


def verify(pins):
    for n, h in pins.items():
        assert isinstance(n, str) and len(h) == 64 and sha(J / n) == h, ('byte_seal', n)


def parent_closed():
    r = json.loads((J / (PARENT + '_RECEIPT.json')).read_text())
    verify(r['pins'])
    paths = {PARENT + '_RESULT.json': r['raw_sha256'],
             PARENT + '_RESULT.md': r['report_sha256']}
    paths.update({'q4_sparse_insertion_verification_v001_checkpoints/' + n: h
                  for n, h in r['checkpoint_sha256'].items()})
    verify(paths)
    p = json.loads((J / (PARENT + '_RESULT.json')).read_text())
    assert p['pins'] == r['pins'] and p['status'] == 'EXACT_SPARSE_Q4_OPERATOR_IDENTITIES_PASSED'
    assert p['physical_embedding_selected'] is False and p['field_or_cosmology_solved'] is False
    assert isinstance(r['pid'], int) and r['pid'] > 0
    return r, {**r['pins'], **paths}


def load_geometry():
    tree = ast.parse((J / OLD).read_text())
    names = ('old_graph', 'Inclusion', 'degrees')
    nodes = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names]
    assert tuple(n.name for n in nodes) == names
    env = {'itertools': itertools, 'lru_cache': lru_cache}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(J / OLD), 'exec'), env)
    edges, cuts = env['old_graph']()
    inc = env['Inclusion'](2, edges, cuts)
    assert len(edges) == 108 and inc.vertices == 56 and len(inc.edges) == 112
    assert cuts == (0, 36, 12, 4) and len(set(sum(inc.endpoints, ()))) == 8
    return inc, env['degrees']


def add(out, key, value):
    value = tuple(value)
    total = tuple(a + b for a, b in zip(out.get(key, ZERO), value))
    if any(total):
        out[key] = total
    else:
        out.pop(key, None)


def combine(*terms):
    out = {}
    for factor, column in terms:
        for key, value in column.items():
            add(out, key, tuple(factor * x for x in value))
    return out


def packed(column):
    return [[list(k), list(v)] for k, v in sorted(column.items())]


def eta(v):
    return 1 if v < 27 or v == 54 else -1


def record_k(q, vertices):
    return sum(eta(v) * ((q >> v) & 1) for v in range(vertices))


def neutral(state, vertices):
    return state[3] == -record_k(state[2], vertices)


def lower(state, vertices=54):
    word, c, q, r = state
    if not (q & 1):
        return None
    rr = r + 1
    assert -vertices // 2 <= rr <= vertices // 2, 'nonwrapping_lower'
    return word, c, q ^ 1, rr


def F(inc, state):
    return inc.encode(state[:3]) + (state[3],)


def T(inc, state):
    s = lower(state)
    return None if s is None else F(inc, s)


def Tad(inc, state):
    s = inc.decode(state[:3])
    if s is None or s[2] & 1:
        return None
    rr = state[3] - 1
    if not -27 <= rr <= 27:
        return None
    return s[0], s[1], s[2] | 1, rr


def mapped(column, fn):
    out = {}
    for s, value in column.items():
        k = fn(s)
        if k is not None:
            add(out, k, value)
    return out


def eligible(column, wanted=True):
    return {s: v for s, v in column.items() if bool(s[2] & 1) == wanted}


def profile(index):
    if index == 0:
        return (1,) * 54, (1,) * 56
    if index == 1:
        old = tuple(1 + v % 3 for v in range(54))
        return old, old + (2, 3)
    old = tuple(2 + v % 2 for v in range(54))
    return old, old + (3, 1)


def source_shift(old, new, direction):
    oo, nn = list(old), list(new)
    if direction < 54:
        oo[direction] += 1
    nn[direction] += 1
    return tuple(oo), tuple(nn)


def action(edges, vertices, state, copy, L, allocation, degrees):
    """Complete SCALE40 affine cap/all-midpoint action, AR and Sself symbolic."""
    word, c, q, r = state
    assert neutral(state, vertices) and len(L) == vertices
    d = degrees(edges, vertices, word)
    bare = sum(L[v] * (40 * (d[v] - 2) ** 2 - 20 * ((q >> v) & 1) * (d[v] - 2))
               for v in range(vertices)) + 40 * L[c]
    ar = 40 * sum(L[v] * ((q >> v) & 1) for v in range(vertices))
    out = {}
    for e, (a, b) in enumerate(edges):
        m2, bit = L[a] + L[b], (word >> e) & 1
        if bit:
            bare += 5 * m2 * (int(c == a) + int(c == b))
            if allocation == 'allmid':
                bare += 10 * (L[a] - L[b]) * (((q >> a) & 1) - ((q >> b) & 1))
            if c in (a, b):
                add(out, (word, b if c == a else a, q, r), (-2 * m2, 0, 0))
        add(out, (word ^ (1 << e), c, q, r), (-4 * m2, 0, 0))
    add(out, state, (bare, ar, 40 * sum(L)))
    if copy:
        occupied = (q >> c) & 1
        rr = r + (eta(c) if occupied else -eta(c))
        assert -vertices // 2 <= rr <= vertices // 2, 'nonwrapping_copy'
        add(out, (word, c, q ^ (1 << c), rr), (copy * L[c], 0, 0))
    return out


def d2(inc, state, old, new, allocation):
    word, c, q, r = state
    bits = tuple((word >> e) & 1 for e in inc.cuts)
    aa, bb = new[54:]
    bare = 40 * (aa + bb) * (sum(bits) - 2) ** 2
    out = {}
    for e, bit, (a, b) in zip(inc.cuts, bits, inc.endpoints):
        bare += 5 * bit * ((bb - old[b]) * int(c == a) + (aa - old[a]) * int(c == b))
        if allocation == 'allmid':
            bare -= 10 * bit * ((bb - old[b]) * ((q >> a) & 1) + (aa - old[a]) * ((q >> b) & 1))
        add(out, (word ^ (1 << e), c, q, r), (4 * (old[a] + old[b]), 0, 0))
        if bit and c in (a, b):
            add(out, (word, b if c == a else a, q, r), (2 * (old[a] + old[b]), 0, 0))
    add(out, state, (bare, 0, 40 * (aa + bb)))
    return out


def rw(inc, state, old, allocation, degrees):
    d = degrees(inc.old, 54, state[0])
    bare = -20 * old[W] * (d[W] - 2)
    if allocation == 'allmid':
        bare += 10 * sum(((state[0] >> e) & 1) * (old[W] - old[b if a == W else a])
                         for e, (a, b) in enumerate(inc.old) if W in (a, b))
    return bare, 40 * old[W], 0


def leak2(inc, lowered, new):
    word, c, q, r = F(inc, lowered)
    out = {}
    for e in itertools.chain.from_iterable(inc.paths):
        a, b = inc.edges[e]
        add(out, (word ^ (1 << e), c, q, r), (-4 * (new[a] + new[b]), 0, 0))
        if (word >> e) & 1 and c in (a, b):
            add(out, (word, b if c == a else a, q, r), (-2 * (new[a] + new[b]), 0, 0))
    return out


def mismatch(inc, state, copy, old, new, allocation, degrees):
    target = T(inc, state)
    left = {} if target is None else action(inc.edges, 56, target, copy, new, allocation, degrees)
    h0 = action(inc.old, 54, state, copy, old, allocation, degrees)
    return combine((1, left), (-1, mapped(h0, lambda s: T(inc, s)))), left, h0


def expected(inc, state, copy, old, new, allocation, degrees):
    s = lower(state)
    out, leakage = {}, {}
    if s is not None:
        out = mapped(d2(inc, s, old, new, allocation), lambda k: F(inc, k))
        add(out, F(inc, s), tuple(-x for x in rw(inc, s, old, allocation, degrees)))
        leakage = leak2(inc, s, new)
        out = combine((1, out), (1, leakage))
    if state[1] == W and copy:
        value = (copy * old[W] * (2 * (state[2] & 1) - 1), 0, 0)
        add(out, F(inc, state), value)
        if state[2] & 1:
            add(leakage, F(inc, state), value)
    return out, leakage


def check(flags, key, left, right):
    ok = left == right
    flags[key] = ok
    if not ok:
        def display(v):
            return packed(v) if isinstance(v, dict) and all(isinstance(k, tuple) for k in v) else v
        raise AssertionError({'control': key, 'left': display(left), 'right': display(right)})


def column_check(inc, state, copy, old, new, allocation, degrees):
    flags = {}
    ts = T(inc, state)
    check(flags, 'partial_isometry', None if ts is None else Tad(inc, ts), state if state[2] & 1 else None)
    check(flags, 'count_resource', (28 - 27, 28 + ((ts[2] >> W) & 1)) if ts else None,
          (1, 27 + ((state[2] >> W) & 1)) if ts else None)
    check(flags, 'record_return', (ts[2].bit_count() - state[2].bit_count(), record_k(ts[2], 56) - record_k(state[2], 54), ts[3] - state[3], neutral(ts, 56)) if ts else None,
          (-1, -1, 1, True) if ts else None)
    actual, left, h0 = mismatch(inc, state, copy, old, new, allocation, degrees)
    exp, leak = expected(inc, state, copy, old, new, allocation, degrees)
    check(flags, 'full_mismatch', actual, exp)
    c = combine((1, mapped(left, lambda s: Tad(inc, s))), (-1, eligible(h0)))
    dt = combine((1, mapped(left, lambda s: Tad(inc, s))), (-1, eligible(h0) if state[2] & 1 else {}))
    off = eligible(h0) if not state[2] & 1 else {}
    check(flags, 'compressed_eligibility', c, combine((1, dt), (-1, off)))
    actual_leak = {s: value for s, value in actual.items() if Tad(inc, s) is None}
    check(flags, 'outside_leakage', actual_leak, leak)
    bs = lower(state)
    hb = {} if bs is None else action(inc.old, 54, bs, copy, old, allocation, degrees)
    comm = combine((1, hb), (-1, mapped(h0, lower)))
    ecomm = {}
    if bs is not None:
        add(ecomm, bs, tuple(-x for x in rw(inc, bs, old, allocation, degrees)))
    if state[1] == W and copy:
        add(ecomm, state, (copy * old[W] * (2 * (state[2] & 1) - 1), 0, 0))
    check(flags, 'donor_commutator', comm, ecomm)
    check(flags, 'full_action_neutrality', all(neutral(s, 54) for s in h0) and all(neutral(s, 56) for s in left), True)
    check(flags, 'absolute_inventory', h0[state][1:],
          (40 * sum(old[v] * ((state[2] >> v) & 1) for v in range(54)), 40 * sum(old)))
    assert tuple(flags) == CASE_KEYS
    midpoint_ordering_difference = {}
    if allocation == 'allmid' and bs is not None:
        correct = d2(inc, bs, old, new, allocation)
        premature = mapped(d2(inc, state, old, new, allocation), lower)
        midpoint_ordering_difference = combine((1, correct), (-1, premature))
    return {'state': list(state), 'copy_scaled': copy, 'donor_occupied': bool(state[2] & 1),
            'incoming_absolute_diagonal': list(h0[state]),
            'actual_mismatch': packed(actual), 'compressed': packed(c), 'eligible_Hermitian_part': packed(dt),
            'eligibility_off_term': packed(off), 'outside': packed(actual_leak),
            'midpoint_ordering_difference': packed(midpoint_ordering_difference), 'controls': flags}


def states(inc, backgrounds=(0, 1, 2), records=RECORDS):
    for bg in backgrounds:
        base = sum(1 << e for e in inc.keep if bg == 1 or bg == 2 and e % 2 == 0)
        for cut in range(16):
            word = base | sum(((cut >> i) & 1) << e for i, e in enumerate(inc.cuts))
            for carrier in CARRIERS:
                for record in records:
                    s = word, carrier, record, -record_k(record, 54)
                    yield bg, cut, s


def source_checks(inc, degrees):
    old, new = profile(0)
    directions = (0, 27, 54, 55)
    rows = []
    for allocation in ('cap', 'allmid'):
        for copy in (0, 4):
            for bg, cut, state in states(inc, backgrounds=(0,)):
                base = mismatch(inc, state, copy, old, new, allocation, degrees)[0]
                first, flags = {}, {}
                for direction in directions:
                    oo, nn = source_shift(old, new, direction)
                    shifted = mismatch(inc, state, copy, oo, nn, allocation, degrees)[0]
                    xi_old = tuple(int(v == direction) for v in range(54))
                    xi_new = tuple(int(v == direction) for v in range(56))
                    derived = expected(inc, state, copy, xi_old, xi_new, allocation, degrees)[0]
                    first[direction] = combine((1, shifted), (-1, base))
                    check(flags, 'first_' + str(direction), first[direction], derived)
                for xi, ze in itertools.combinations(directions, 2):
                    oo, nn = source_shift(*source_shift(old, new, xi), ze)
                    mixed = combine((1, mismatch(inc, state, copy, oo, nn, allocation, degrees)[0]),
                                    (-1, base), (-1, first[xi]), (-1, first[ze]))
                    check(flags, 'mixed_' + str(xi) + '_' + str(ze), mixed, {})
                rows.append({'allocation': allocation, 'copy_scaled': copy, 'cut_word': cut,
                             'state': list(state), 'first_mismatch': {str(k): packed(v) for k, v in first.items()},
                             'mixed_mismatch': [], 'controls': flags})
    assert len(rows) == 1024
    return {'rows': rows, 'fixed_logical_T_derivatives_zero': True,
            'uniform_normal_first_is_full_H': True, 'uniform_normal_mixed_L_is_H_L': True,
            'normal_second_zero_only_affine_coordinate': True}


def gram(columns):
    assert all(all(v[1:] == (0, 0) for v in col.values()) for col in columns)
    return [[sum(v[0] * columns[j].get(k, ZERO)[0] for k, v in col.items())
             for j in range(len(columns))] for col in columns]


def expected_gram(inc, basis, new, copy):
    result = [[0] * len(basis) for _ in basis]
    for i, si in enumerate(basis):
        for j, sj in enumerate(basis):
            wi, ci, _, _ = si
            wj, cj, _, _ = sj
            if ci == cj:
                for e, (a, b) in zip(inc.cuts, inc.endpoints):
                    aa, bb = 4 * (new[a] + new[55]), 4 * (new[54] + new[b])
                    if wi == wj:
                        result[i][j] += aa * aa + bb * bb
                    elif wi ^ wj == 1 << e:
                        result[i][j] += 2 * aa * bb
            if wi == wj:
                for side in (0, 1):
                    ai = aj = 0
                    for e, endpoints in zip(inc.cuts, inc.endpoints):
                        a, b = endpoints
                        endpoint = endpoints[side]
                        amp = 2 * (new[a] + new[55]) if side == 0 else 2 * (new[54] + new[b])
                        if ci == endpoint:
                            ai += amp * ((wi >> e) & 1)
                        if cj == endpoint:
                            aj += amp * ((wj >> e) & 1)
                    result[i][j] += ai * aj
                if ci == cj == W:
                    result[i][j] += copy * copy * new[W] ** 2
    return result


def gram_checks(inc, degrees):
    basis = [s for _, _, s in states(inc, backgrounds=(0,), records=(1,))]
    assert len(basis) == 64
    rows = []
    for pi in range(3):
        old, new = profile(pi)
        for copy in (0, 4):
            actual_cols = []
            for s in basis:
                full = mismatch(inc, s, copy, old, new, 'cap', degrees)[0]
                actual_cols.append({k: value for k, value in full.items() if Tad(inc, k) is None})
            actual = gram(actual_cols)
            exp = expected_gram(inc, basis, new, copy)
            flags = {}
            check(flags, 'full_Gram', actual, exp)
            rows.append({'profile': pi, 'copy_scaled': copy, 'actual': actual, 'expected': exp,
                         'signed_difference': [[a - b for a, b in zip(x, y)] for x, y in zip(actual, exp)], 'controls': flags})
    contacts = []
    old, new = profile(0)
    for copy in (0, 4):
        base = expected_gram(inc, basis, new, copy)
        for xi, ze in itertools.combinations_with_replacement((0, 27, 54, 55), 2):
            xo, xn = source_shift(old, new, xi)
            zo, zn = source_shift(old, new, ze)
            xzo, xzn = source_shift(xo, xn, ze)
            def outside(oo, nn):
                return [expected(inc, s, copy, oo, nn, 'cap', degrees)[1] for s in basis]
            l0, lx, lz, lxz = outside(old, new), outside(xo, xn), outside(zo, zn), outside(xzo, xzn)
            gxz, gx, gz, g0 = gram(lxz), gram(lx), gram(lz), gram(l0)
            mixed = [[gxz[i][j] - gx[i][j] - gz[i][j] + g0[i][j] for j in range(64)] for i in range(64)]
            kxz, kx, kz = expected_gram(inc, basis, xzn, copy), expected_gram(inc, basis, xn, copy), expected_gram(inc, basis, zn, copy)
            exact = [[kxz[i][j] - kx[i][j] - kz[i][j] + base[i][j] for j in range(64)] for i in range(64)]
            flags = {}
            check(flags, 'mixed_Gram', mixed, exact)
            contacts.append({'copy_scaled': copy, 'xi': xi, 'eta': ze, 'actual': mixed,
                             'expected': exact, 'controls': flags})
    return {'basis': [list(s) for s in basis], 'scaled_Gram_denominator': SCALE ** 2,
            'rows': rows, 'mixed_contacts': contacts}


def checkpoint(name, payload, pins, owner):
    p = CP / (name + '.json')
    data = {'name': name, 'pins': pins, 'owner': owner, 'payload': payload, 'status': 'EXACT_CHECKS_PASSED'}
    digest = exclusive(p, canonical(data))
    commit = {'checkpoint': p.name, 'sha256': digest, 'pins': pins, 'owner': owner, 'status': data['status']}
    exclusive(p.with_name(p.name + '.COMMIT.json'), canonical(commit))
    assert json.loads(p.read_text()) == data and json.loads(p.with_name(p.name + '.COMMIT.json').read_text()) == commit
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root-owned', action='store_true')
    ap.add_argument('--execute', action='store_true')
    args = ap.parse_args()
    assert args.root_owned and args.execute, 'root_owned_explicit_execution_required'
    assert not AUTHOR_DRAFT, 'AUTHOR_DRAFT_UNLAUNCHABLE'
    verify(PINS)
    prior, inherited = parent_closed()
    pins = dict(PINS)
    for n, h in inherited.items():
        assert n not in pins or pins[n] == h
        pins[n] = h
    pins[Path(__file__).name] = sha(__file__)
    verify(pins)
    outputs = [J / (STEM + suffix) for suffix in ('_RESULT.json', '_REPORT.md', '_RECEIPT.json', '_ERROR.json')]
    assert all(not p.exists() for p in outputs) and not CP.exists(), 'unused_runtime_namespace'
    owner = {'pid': os.getpid(), 'started_utc': utc(), 'source_sha256': sha(__file__)}
    assert isinstance(owner['pid'], int) and owner['pid'] > 0
    start = time.monotonic()
    CP.mkdir()
    exclusive(CP / 'OWNER_START.json', canonical({'owner': owner, 'pins': pins}))
    try:
        inc, degrees = load_geometry()
        groups = []
        for allocation in ('cap', 'allmid'):
            for pi in range(3):
                old, new = profile(pi)
                assert all(x > 0 for x in old + new)
                rows = [dict(column_check(inc, s, copy, old, new, allocation, degrees),
                             background=bg, cut_word=cut)
                        for copy in (0, 4) for bg, cut, s in states(inc)]
                assert len(rows) == 1536 and all(set(r['controls']) == set(CASE_KEYS) for r in rows)
                groups.append(checkpoint(allocation + '_L' + str(pi),
                              {'allocation': allocation, 'L_old': list(old), 'L_new': list(new), 'rows': rows}, pins, owner))
        source = checkpoint('SOURCE_CONTACTS', source_checks(inc, degrees), pins, owner)
        grams = checkpoint('LEAKAGE_GRAMS', gram_checks(inc, degrees), pins, owner)
        verify(pins)
        parent_closed()
        cp_map = {p.relative_to(J).as_posix(): sha(p) for p in sorted(CP.iterdir())}
        assert len(cp_map) == 17
        for group in groups + [source, grams]:
            p = CP / (group['name'] + '.json')
            assert json.loads(p.read_text()) == group
            commit = json.loads(p.with_name(p.name + '.COMMIT.json').read_text())
            assert commit['sha256'] == sha(p) and commit['pins'] == pins and commit['owner'] == owner
        result = {'status': 'EXACT_DONOR_DRESSED_SOURCE_CHECKS_PASSED', 'pins': pins,
                  'scale': SCALE, 'coefficient_order': ['bare', 'AR', 'Sself'], 'fixed_donor': 'A000',
                  'groups': groups, 'source_contacts': source, 'leakage_grams': grams,
                  'census': {'native_columns': 9216, 'native_predicates': 82944,
                             'source_columns': 1024, 'source_predicates': 10240,
                             'Gram_matrices': 6, 'mixed_Gram_matrices': 20, 'Gram_predicates': 26,
                             'checkpoint_pairs': 8, 'total_predicates': 93210},
                  'prior_dispositions': {'status': prior.get('status', 'legacy_receipt'), 'raw_sha256': prior['raw_sha256'],
                                         'old_result_byte_bound': True, 'no_old_operator_replay': True},
                  'qualification': PHYSICAL, 'operator_scope': 'Nc1/one-content exact affine native cap and allmid only',
                  'unavailable_contacts': ['physical coframe/metric/dilation', 'Wilson/Maxwell birth interface',
                                           'precursor/material/support', 'source-dependent encoder and readout']}
        raw = canonical(result)
        report = ('# Donor-dressed q4 exact native source check V001\n\n'
                  'All prospective exact integer identities passed. Native columns 9216; source columns 1024; '
                  'six 64-column leakage Grams and twenty mixed Gram contacts. Copy OFF and ON, blank and occupied donors, '
                  'both source allocations and every fixed branch were retained.\n\n'
                  'This checks the literal logical native action and affine source. It does not supply physical deformation, '
                  'Maxwell/return transfer path, preparation, volume, EOS or cosmological evolution.\n').encode()
        rh, th = exclusive(outputs[0], raw), exclusive(outputs[1], report)
        assert json.loads(outputs[0].read_text()) == result
        receipt = {'status': 'CLOSED', 'owner': owner, 'finished_utc': utc(), 'elapsed_seconds': time.monotonic() - start,
                   'pins': pins, 'outputs': {outputs[0].name: rh, outputs[1].name: th},
                   'checkpoint_outputs': cp_map, 'qualification': PHYSICAL}
        exclusive(outputs[2], canonical(receipt))
        verify(pins)
        parent_closed()
        print(json.dumps({'status': result['status'], 'result_sha256': rh, 'receipt_sha256': sha(outputs[2])}))
    except Exception:
        data = canonical({'status': 'FAILED', 'owner': owner, 'failed_utc': utc(), 'pins': pins,
                          'traceback': traceback.format_exc(), 'qualification': PHYSICAL,
                          'checkpoint_outputs': {p.relative_to(J).as_posix(): sha(p) for p in CP.iterdir()}})
        if not outputs[3].exists():
            exclusive(outputs[3], data)
        raise


if __name__ == '__main__':
    main()

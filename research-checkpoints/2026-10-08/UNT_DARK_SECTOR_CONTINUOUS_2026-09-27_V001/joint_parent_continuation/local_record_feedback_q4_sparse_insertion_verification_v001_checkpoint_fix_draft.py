"""Prospective exact sparse-action verification; execute only after full review."""
import argparse
import hashlib
import itertools
import json
import os
from pathlib import Path
import time
import traceback

import numpy as np

J = Path(__file__).resolve().parent
STEM = 'LOCAL_RECORD_FEEDBACK_Q4_SPARSE_INSERTION_VERIFICATION_V001'
NOTE = 'LOCAL_RECORD_FEEDBACK_Q4_CONSERVING_FORMATION_CANDIDATE_V001.md'
NOTE_SHA = '07323053b75b947b35712f0ac8fc4ce04c2766131cd4e684fd64167321b51f3c'
PROTOCOL = STEM + '.md'
SCALE = 40


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def write_new(path, value):
    data = canonical(value)
    with path.open('xb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    return hashlib.sha256(data).hexdigest()


def checkpoint_write(path, row, pins):
    row_sha = write_new(path, row)
    write_new(path.with_name(path.name + '.COMMIT.json'),
              {'checkpoint_name': path.name, 'checkpoint_sha256': row_sha,
               'pins': pins, 'status': 'COMPLETE_EXACT_CHECKS_PASSED'})
    path.chmod(0o444)
    path.with_name(path.name + '.COMMIT.json').chmod(0o444)


def checkpoint_read(path, pins, expected):
    commit_path = path.with_name(path.name + '.COMMIT.json')
    commit = json.loads(commit_path.read_text())
    assert commit == {'checkpoint_name': path.name, 'checkpoint_sha256': digest(path),
                      'pins': pins, 'status': 'COMPLETE_EXACT_CHECKS_PASSED'}, 'checkpoint_commit'
    row = json.loads(path.read_text())
    assert isinstance(row, dict) and row['pins'] == pins
    for key, value in expected.items():
        assert row[key] == value, ('checkpoint_census', path.name, key)
    assert set(row) == set(expected), ('checkpoint_schema', path.name)
    return row


def add(out, key, value):
    total = out.get(key, 0) + value
    if total:
        out[key] = total
    else:
        out.pop(key, None)


def old_graph():
    coords = tuple(itertools.product(range(3), repeat=3))
    index = {r: i for i, r in enumerate(coords)}
    shifts = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
    edges = tuple((i, 27 + index[tuple((r[k] + s[k]) % 3 for k in range(3))])
                  for i, r in enumerate(coords) for s in shifts)
    anchors = tuple(index[r] for r in ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)))
    return edges, tuple(4 * a for a in anchors)


class Inclusion:
    def __init__(self, length, edges, cuts):
        self.length, self.old, self.cuts = length, edges, cuts
        self.endpoints = tuple(edges[e] for e in cuts)
        self.keep = tuple(e for e in range(len(edges)) if e not in cuts)
        new_edges = [edges[e] for e in self.keep]
        paths = []
        if length == 2:
            self.vertices, self.m = 56, 1
            self.groups = ((54, tuple(b for a, b in self.endpoints)),
                           (55, tuple(a for a, b in self.endpoints)))
        else:
            self.vertices, self.m = 58, 2
            self.groups = ((54, tuple(self.endpoints[i][1] for i in (0, 2))),
                           (55, tuple(self.endpoints[i][1] for i in (1, 3))),
                           (56, tuple(self.endpoints[i][0] for i in (0, 1))),
                           (57, tuple(self.endpoints[i][0] for i in (2, 3))))
        for i, (a, b) in enumerate(self.endpoints):
            path = ((a, 55), (54, b)) if length == 2 else (
                (a, 56 + i // 2), (54 + i % 2, 56 + i // 2), (54 + i % 2, b))
            paths.append(tuple(range(len(new_edges), len(new_edges) + length)))
            new_edges.extend(path)
        self.edges, self.paths = tuple(new_edges), tuple(paths)

    def encode_word(self, word):
        target = sum(((word >> e) & 1) << k for k, e in enumerate(self.keep))
        for old_e, path in zip(self.cuts, self.paths):
            for k in path:
                target |= ((word >> old_e) & 1) << k
        return target

    def encode(self, state):
        word, carrier, records = state
        return self.encode_word(word), carrier, records

    def decode(self, state):
        word, carrier, records = state
        if carrier >= 54 or records >> 54:
            return None
        old = sum(((word >> k) & 1) << e for k, e in enumerate(self.keep))
        for old_e, path in zip(self.cuts, self.paths):
            bits = tuple((word >> k) & 1 for k in path)
            if len(set(bits)) != 1:
                return None
            old |= bits[0] << old_e
        return old, carrier, records


def degrees(edges, vertices, word):
    result = [0] * vertices
    for e, (a, b) in enumerate(edges):
        if (word >> e) & 1:
            result[a] += 1
            result[b] += 1
    return result


def action(edges, vertices, state, copy):
    """Full uniform Nc1 node-cap native action, coefficientwise AR/self retained."""
    word, carrier, records = state
    d = degrees(edges, vertices, word)
    diagonal = sum(40 * (x - 2) ** 2 - 20 * ((records >> v) & 1) * (x - 2)
                   for v, x in enumerate(d)) + 40 + 10 * d[carrier]
    out = {state: diagonal} if diagonal else {}
    for e, (a, b) in enumerate(edges):
        add(out, (word ^ (1 << e), carrier, records), -8)
        if (word >> e) & 1:
            if carrier == a:
                add(out, (word, b, records), -4)
            elif carrier == b:
                add(out, (word, a, records), -4)
    add(out, (word, carrier, records ^ (1 << carrier)), copy)
    return out


def expected_d(inc, state):
    word, carrier, records = state
    bits = tuple((word >> e) & 1 for e in inc.cuts)
    if inc.length == 2:
        diagonal = 80 * (sum(bits) - 2) ** 2
    else:
        sums = (bits[0] + bits[1], bits[2] + bits[3],
                bits[0] + bits[2], bits[1] + bits[3])
        diagonal = 40 * sum((2 * s - 2) ** 2 for s in sums)
    out = {state: diagonal} if diagonal else {}
    for e, n, (a, b) in zip(inc.cuts, bits, inc.endpoints):
        add(out, (word ^ (1 << e), carrier, records), 8)
        if n and carrier in (a, b):
            add(out, (word, b if carrier == a else a, records), 4)
    return out


def expected_leak(inc, state):
    word, carrier, records = inc.encode(state)
    out = {}
    for path in inc.paths:
        for e in path:
            add(out, (word ^ (1 << e), carrier, records), -8)
    for e in itertools.chain.from_iterable(inc.paths):
        a, b = inc.edges[e]
        if (word >> e) & 1 and carrier in (a, b):
            add(out, (word, b if carrier == a else a, records), -4)
    return out


def decomposition(inc, state, copy):
    residual = action(inc.edges, inc.vertices, inc.encode(state), copy)
    for key, value in action(inc.old, 54, state, copy).items():
        add(residual, inc.encode(key), -value)
    compressed, leaked = {}, {}
    for key, value in residual.items():
        old = inc.decode(key)
        add(leaked if old is None else compressed, key if old is None else old, value)
    return compressed, leaked


def gram_test(inc, background):
    states = tuple((background | sum(((n >> i) & 1) << e for i, e in enumerate(inc.cuts)), c, 0)
                   for n in range(16) for c in range(54))
    lookup = {s: i for i, s in enumerate(states)}
    by_target = {}
    for i, state in enumerate(states):
        compressed, leaked = decomposition(inc, state, 4)
        assert compressed == expected_d(inc, state)
        assert leaked == expected_leak(inc, state)
        for target, value in leaked.items():
            by_target.setdefault(target, []).append((i, value))
    actual = np.zeros((864, 864), dtype=np.int64)
    for contributors in by_target.values():
        for i, x in contributors:
            for j, y in contributors:
                actual[i, j] += x * y
    expected = np.zeros_like(actual)
    for col, state in enumerate(states):
        word, carrier, records = state
        expected[col, col] += 8 * 8 * (8 if inc.length == 2 else 12)
        if inc.length == 2:
            for e in inc.cuts:
                expected[lookup[(word ^ (1 << e), carrier, records)], col] += 2 * 8 * 8
        for destination, endpoints in inc.groups:
            occupied = [v for v in endpoints
                        if (word >> inc.cuts[next(i for i, pair in enumerate(inc.endpoints) if v in pair)]) & 1]
            if carrier in occupied:
                for v in occupied:
                    expected[lookup[(word, v, records)], col] += 4 * 4
    assert np.array_equal(actual, expected), 'independent_full_Gram'
    return {'matrix_shape': list(actual.shape), 'entries_checked': int(actual.size),
            'integer_scale_squared': 1600, 'Gram_sha256': hashlib.sha256(actual.tobytes()).hexdigest(),
            'max_integer_entry': int(actual.max()), 'target_syndromes': len(by_target)}


def execute(args):
    start = time.time()
    protocol_path = J / PROTOCOL
    assert digest(J / NOTE) == NOTE_SHA
    assert digest(protocol_path) == args.protocol_sha
    pins = {NOTE: NOTE_SHA, PROTOCOL: args.protocol_sha, Path(__file__).name: digest(Path(__file__))}
    for line in (J / NOTE).read_text().splitlines():
        if line.startswith('| ') and ' | ' in line:
            cells = [x.strip() for x in line.strip('|').split('|')]
            if len(cells) == 2 and len(cells[1]) == 64:
                assert digest(J / cells[0]) == cells[1], cells[0]
                pins[cells[0]] = cells[1]
    outputs = [J / (STEM + suffix) for suffix in ('_RESULT.json', '_RESULT.md', '_RECEIPT.json', '_ERROR.json')]
    assert not any(p.exists() for p in outputs), 'reserved_output_exists'
    cp = J / 'q4_sparse_insertion_verification_v001_checkpoints'
    if not args.resume:
        cp.mkdir()
        write_new(cp / 'OWNER_START.json', {'pid': os.getpid(), 'pins': pins, 'time': start})
    else:
        saved = json.loads((cp / 'OWNER_START.json').read_text())
        assert set(saved) == {'pid', 'pins', 'time'} and saved['pins'] == pins, 'resume_pins'
        assert isinstance(saved['pid'], int) and saved['pid'] > 0 and isinstance(saved['time'], (float, int))
        assert not any(p.name.endswith('.json') and p.name.startswith('F') and
                       not p.name.endswith('.COMMIT.json') and
                       not p.with_name(p.name + '.COMMIT.json').exists() for p in cp.iterdir()), 'orphan_checkpoint'
    edges, cuts = old_graph()
    assert len(set(edges)) == 108 and all(x == 4 for x in degrees(edges, 54, (1 << 108) - 1))
    assert len(set(v for e in cuts for v in edges[e])) == 8
    cutmask = sum(1 << e for e in cuts)
    backgrounds = (0, ((1 << 108) - 1) ^ cutmask,
                   sum(1 << e for e in range(108) if e not in cuts and e % 2))
    endpoints = tuple(v for e in cuts for v in edges[e])
    all_records = (1 << 54) - 1
    records = tuple(dict.fromkeys((0, all_records,
                                  sum(1 << v for v in range(0, 54, 2)),
                                  sum(1 << v for v in range(1, 54, 2)))
                                 + tuple(1 << v for v in endpoints)
                                 + tuple(all_records ^ (1 << v) for v in endpoints)))
    rows, grams = [], []
    for length in (2, 3):
        inc = Inclusion(length, edges, cuts)
        assert len(set(inc.edges)) == 108 + 4 * inc.m
        assert all(x == 4 for x in degrees(inc.edges, inc.vertices, (1 << len(inc.edges)) - 1))
        for bi, background in enumerate(backgrounds):
            path = cp / f'F{length}_background{bi}.json'
            expected_row = {'length': length, 'background': bi, 'columns': 16 * 54 * len(records) * 2,
                            'pins': pins, 'record_patterns': len(records), 'copy_native_controls': [0, '1/10'],
                            'AR_Q_intertwiner': True, 'Sself_coefficient_increment': 2 * inc.m,
                            'count_pair_increment': inc.m, 'donor_resource_decrement_required': inc.m}
            if path.exists():
                assert args.resume
                row = checkpoint_read(path, pins, expected_row)
            else:
                count = 0
                for n, carrier, q, copy in itertools.product(range(16), range(54), records, (0, 4)):
                    word = background | sum(((n >> i) & 1) << e for i, e in enumerate(cuts))
                    state = (word, carrier, q)
                    encoded = inc.encode(state)
                    assert inc.decode(encoded) == state
                    assert q.bit_count() == encoded[2].bit_count()
                    assert sum(((q >> v) & 1) * (1 if v < 27 else -1) for v in range(54)) == sum(
                        ((encoded[2] >> v) & 1) * (1 if v < 27 else -1) for v in range(54))
                    assert degrees(edges, 54, word) == degrees(inc.edges, inc.vertices, encoded[0])[:54]
                    compressed, leaked = decomposition(inc, state, copy)
                    assert compressed == expected_d(inc, state), (length, bi, n, carrier, q, copy, 'D')
                    assert leaked == expected_leak(inc, state), (length, bi, n, carrier, q, copy, 'Lambda')
                    count += 1
                row = {'length': length, 'background': bi, 'columns': count, 'pins': pins,
                       'record_patterns': len(records), 'copy_native_controls': [0, '1/10'],
                       'AR_Q_intertwiner': True, 'Sself_coefficient_increment': 2 * inc.m,
                       'count_pair_increment': inc.m, 'donor_resource_decrement_required': inc.m}
                assert row == expected_row, 'fresh_census'
                checkpoint_write(path, row, pins)
            rows.append(row)
        path = cp / f'F{length}_GRAM.json'
        if path.exists():
            assert args.resume
            metadata = json.loads(path.read_text())
            expected_gram = {'length': length, 'pins': pins, 'matrix_shape': [864, 864],
                             'entries_checked': 864 * 864, 'integer_scale_squared': 1600,
                             'Gram_sha256': metadata['Gram_sha256'],
                             'max_integer_entry': 528 if length == 2 else 784,
                             'target_syndromes': 3486 if length == 2 else 10416}
            assert isinstance(metadata['Gram_sha256'], str) and len(metadata['Gram_sha256']) == 64
            assert all(c in '0123456789abcdef' for c in metadata['Gram_sha256'])
            row = checkpoint_read(path, pins, expected_gram)
        else:
            row = {'length': length, 'pins': pins, **gram_test(inc, backgrounds[1])}
            checkpoint_write(path, row, pins)
        grams.append(row)
    for name, expected in pins.items():
        assert digest(J / name) == expected, ('input_changed', name)
    result = {'status': 'EXACT_SPARSE_Q4_OPERATOR_IDENTITIES_PASSED', 'pins': pins,
              'native_coefficients': {'U': 1, 'EP': 1, 'lambda': '1/2', 'j': '1/4',
                                      't': '1/10', 'h': '1/5', 'Delta': 0},
              'AR_Sself': 'symbolic coefficient intertwiners; no physical value selected',
              'base_vertices': 54, 'base_edges': 108, 'cuts': [list(edges[e]) for e in cuts],
              'rows': rows, 'grams': grams, 'columns': sum(r['columns'] for r in rows),
              'Gram_entries_checked': sum(r['entries_checked'] for r in grams),
              'physical_embedding_selected': False, 'field_or_cosmology_solved': False,
              'elapsed_seconds': time.time() - start}
    raw_sha = write_new(outputs[0], result)
    report = ('# Exact sparse q4 insertion verification V001\n\n' + result['status'] + '\n\n'
              + f"Both same-native-action compression/leakage identities PASS on {result['columns']} columns; "
              + f"{result['Gram_entries_checked']} independent integer Gram entries agree exactly.\n\n"
              + 'All16 cut words, all54 old carrier sites,20 declared record patterns,three background words, '
              + 'both existing copy controls and both rewrites are retained. AR/self remain symbolic. '
              + 'This verifies the stated graph operators, not complete Hilbert-space enumeration or physical embedding. '
              + 'No parameter/state/rate is fitted, no trajectory or field is solved, and no cosmic growth is inferred.\n\n'
              + f'Raw SHA256: {raw_sha}\n')
    with outputs[1].open('x') as f:
        f.write(report)
    receipt = {'pins': pins, 'raw_sha256': raw_sha, 'report_sha256': digest(outputs[1]),
               'checkpoint_sha256': {p.name: digest(p) for p in sorted(cp.glob('*.json'))},
               'pid': os.getpid(), 'elapsed_seconds': result['elapsed_seconds']}
    receipt_sha = write_new(outputs[2], receipt)
    print(json.dumps({'status': result['status'], 'columns': result['columns'],
                      'Gram_entries': result['Gram_entries_checked'], 'seconds': result['elapsed_seconds'],
                      'raw_sha256': raw_sha, 'receipt_sha256': receipt_sha}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--resume', action='store_true')
    parser.add_argument('--protocol-sha', required=True)
    arguments = parser.parse_args()
    if not arguments.execute:
        raise SystemExit('No action executed: full source/protocol review and root launch required.')
    if any((J / (STEM + suffix)).exists() for suffix in ('_RESULT.json', '_RESULT.md', '_RECEIPT.json', '_ERROR.json')):
        raise SystemExit('Reserved outputs already exist; preserve them and use a distinct reviewed recovery.')
    try:
        execute(arguments)
    except BaseException as error:
        error_path = J / (STEM + '_ERROR.json')
        if not error_path.exists():
            write_new(error_path, {'error_type': type(error).__name__, 'message': str(error),
                                   'traceback': traceback.format_exc(), 'pid': os.getpid()})
        raise

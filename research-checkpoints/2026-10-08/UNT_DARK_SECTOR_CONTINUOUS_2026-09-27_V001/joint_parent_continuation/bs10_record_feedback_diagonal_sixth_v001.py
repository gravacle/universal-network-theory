#!/usr/bin/env python3
"""Prospectively frozen exact linked diagonal coefficient; stdlib only."""
from decimal import Decimal, ROUND_FLOOR, ROUND_CEILING, localcontext
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib
import json
import os
import resource
import sys
import time
import traceback

ROOT = Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J = ROOT / 'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
NAME = 'BS10_RECORD_FEEDBACK_DIAGONAL_SIXTH_V001'
PROTOCOL = J / (NAME + '.md')
RESULT = J / (NAME + '_RESULT.json')
REPORT = J / (NAME + '_RESULT.md')
RECEIPT = J / (NAME + '_RECEIPT.json')
CP = J / 'bs10_record_feedback_diagonal_sixth_v001_checkpoints'
SOURCE = Path(__file__).resolve()
ATTEMPT_CREATED = False
H = Fraction(1, 5)
ORDERS = (2, 4, 6)
CLASSES = (
    ('single_add', ((0, 1),), (1,), 2),
    ('single_remove', ((0, 1),), (-1,), 2),
    ('pair_add_add', ((0, 1), (1, 2)), (1, 1), 2),
    ('pair_remove_remove', ((0, 1), (1, 2)), (-1, -1), 2),
    ('pair_add_remove', ((0, 1), (1, 2)), (1, -1), 8),
    ('star_add_add_remove', ((0, 1), (0, 2), (0, 3)), (1, 1, -1), 4),
    ('star_add_remove_remove', ((0, 1), (0, 2), (0, 3)), (1, -1, -1), 4),
    ('path_add_add_add', ((0, 1), (1, 2), (2, 3)), (1, 1, 1), 2),
    ('path_remove_remove_remove', ((0, 1), (1, 2), (2, 3)), (-1, -1, -1), 2),
    ('path_add_add_remove', ((0, 1), (1, 2), (2, 3)), (1, 1, -1), 8),
    ('path_add_remove_remove', ((0, 1), (1, 2), (2, 3)), (1, -1, -1), 8),
    ('path_add_remove_add', ((0, 1), (1, 2), (2, 3)), (1, -1, 1), 8),
    ('path_remove_add_remove', ((0, 1), (1, 2), (2, 3)), (-1, 1, -1), 8),
)
INPUTS = {
    'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/LOCAL_PROPER_BOND_NORMALIZATION_V001.md': '9b4cc5e1942ac7373e210efa46bfa74e03bbcfb8130c01232373b02e8a622a5b',
    'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/DEGREE_TWO_JOINT_MATTER_REFERENCE_GATE_V001.md': '84e889f6148b43c91c2ef1a0e3194a8723e190bcf5f9a16407013e85b6a02a83',
    'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/recovered_sources/BS_MICRO_ACTION.md': '00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec',
    'program-worktree/LANE_CROSS_RFT_GRA_GL6AO_COMPLETE_SIXTH_ORDER_LOCKED_HAMILTONIAN_V001/THEOREM.md': 'f75edcb115c3f7c86c6598f4597366b36e363df2d03ad919cc607b57dfb6b20c',
    'program-worktree/LANE_CROSS_RFT_GRA_GL6AO_COMPLETE_SIXTH_ORDER_LOCKED_HAMILTONIAN_V001/verify_sixth_order_hamiltonian.py': '6cd1c8533821012e3281310ec0dadc95f8788ecf74729ba912f56d46f5a9b271',
    'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/RECORD_FEEDBACK_LOOP_BACKGROUND_ORDERS_V001.md': '7800587a83941d3c3380af211ba16be584c29f36f26e4c78c5b362c347e1abc9',
    'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/BS10_RECORD_FEEDBACK_HEX_RING_V001.md': '14a5b2d44887920b7bab1bd32cbc98d1d2395b3f7110a6faed0036037b16fd78',
    'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_record_feedback_hex_ring_v001.py': 'd9f406d945e8e5350c7d397191d7a26bef1aafabeaaab0f50cf06db87c0b2d62',
    'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/BS10_RECORD_FEEDBACK_HEX_RING_V001_RESULT.json': '986554b4c2315f214fef98436f285997d6c37a0884ffa1647a5a513b261fbd8f',
    'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/BS10_RECORD_FEEDBACK_HEX_RING_V001_RECEIPT.json': '265692857646e2e271b16ed3e91be60baaab818b6a890e3d3ca41832ffd90fa1',
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def exclusive(path, obj):
    with path.open('xb') as stream:
        stream.write(canonical(obj) + b'\n')
        stream.flush()
        os.fsync(stream.fileno())
    return sha(path)


def event(kind, **fields):
    row = {'event': kind, 'pid': os.getpid(), 'elapsed_seconds': time.perf_counter() - T0, **fields}
    with (CP / 'journal.jsonl').open('ab') as stream:
        stream.write(canonical(row) + b'\n')
        stream.flush()
        os.fsync(stream.fileno())


def exact(value):
    value = Fraction(value)
    out = {'numerator': value.numerator, 'denominator': value.denominator}
    values = []
    for rounding in (ROUND_FLOOR, ROUND_CEILING):
        with localcontext() as ctx:
            ctx.prec, ctx.rounding = 20, rounding
            values.append(str(Decimal(value.numerator) / Decimal(value.denominator)))
    out['decimal20_lower'], out['decimal20_upper'] = values
    return out


def checks_add(checks, label, condition):
    checks.append({'label': label, 'passed': bool(condition)})


def authenticate():
    observed = {}
    for rel, wanted in INPUTS.items():
        got = sha(ROOT / rel)
        if got != wanted:
            raise RuntimeError('Frozen input mismatch: ' + rel)
        observed[rel] = got
    old = json.loads((J / 'BS10_RECORD_FEEDBACK_HEX_RING_V001_RESULT.json').read_text())
    receipt = json.loads((J / 'BS10_RECORD_FEEDBACK_HEX_RING_V001_RECEIPT.json').read_text())
    for stem, key in (('bs10_record_feedback_hex_ring_v001.py', 'source_sha256'),
                      ('BS10_RECORD_FEEDBACK_HEX_RING_V001.md', 'protocol_sha256')):
        wanted = sha(J / stem)
        if old[key] != wanted or receipt[key] != wanted:
            raise RuntimeError('Old hex source/protocol seal mismatch: ' + key)
    if receipt['result_raw_sha256'] != sha(J / 'BS10_RECORD_FEEDBACK_HEX_RING_V001_RESULT.json'):
        raise RuntimeError('Old hex raw receipt mismatch')
    if receipt['result_canonical_sha256'] != hashlib.sha256(canonical(old)).hexdigest():
        raise RuntimeError('Old hex canonical receipt mismatch')
    if old['input_sha256'] != receipt['input_sha256']:
        raise RuntimeError('Old hex input seal mismatch')
    for rel, digest in old['input_sha256'].items():
        if observed.get(rel) != digest:
            raise RuntimeError('Old hex ancestor mismatch: ' + rel)
    return observed


def submasks(mask):
    out, value = [], mask
    while True:
        out.append(value)
        if value == 0:
            return out
        value = (value - 1) & mask


def gap_forms(edges, signs, q, lapse=Fraction(1)):
    nv = 1 + max(v for edge in edges for v in edge)
    direct, expanded = [], []
    for mask in range(1 << len(edges)):
        charge = [0] * nv
        selected = [i for i in range(len(edges)) if mask & (1 << i)]
        for i in selected:
            for v in edges[i]:
                charge[v] += signs[i]
        direct.append(lapse * sum((Fraction(d*d) - Fraction(q*d, 2) for d in charge), Fraction(0)))
        cross = sum(signs[i] * signs[j] for n, i in enumerate(selected) for j in selected[n+1:]
                    if set(edges[i]) & set(edges[j]))
        expanded.append(lapse * Fraction(2*len(selected) + 2*cross - q*sum(signs[i] for i in selected)))
    return direct, expanded


def recurrence(gaps, edges_count, lapse=Fraction(1)):
    amplitudes = [[Fraction(0)] * (1 << edges_count) for _ in range(7)]
    energies = [Fraction(0)] * 7
    amplitudes[0][0] = Fraction(1)
    for r in range(1, 7):
        energies[r] = -lapse * sum((amplitudes[r-1][1 << e] for e in range(edges_count)), Fraction(0))
        for mask in range(1, 1 << edges_count):
            neighbors = lapse * sum((amplitudes[r-1][mask ^ (1 << e)] for e in range(edges_count)), Fraction(0))
            folded = sum((energies[k] * amplitudes[r-k][mask] for k in range(1, r+1)), Fraction(0))
            amplitudes[r][mask] = (neighbors + folded) / gaps[mask]
    return energies, amplitudes


def q_words(gaps, edges_count, length, lapse=Fraction(1)):
    total, derivative, retained = Fraction(0), Fraction(0), 0
    for word in product(range(edges_count), repeat=length):
        mask, intermediates = 0, []
        for e in word[:-1]:
            mask ^= 1 << e
            if mask == 0:
                break
            intermediates.append(mask)
        if len(intermediates) != length - 1 or (mask ^ (1 << word[-1])) != 0:
            continue
        weight = lapse**length
        for value in intermediates:
            weight /= gaps[value]
        total -= weight
        if length == 4:
            derivative += weight * sum((1 / gaps[value] for value in intermediates), Fraction(0))
        retained += 1
    return total, derivative, retained


def canonical_folds(gaps, edges_count, lapse=Fraction(1)):
    b = -lapse**2 * sum((1 / gaps[1 << e] for e in range(edges_count)), Fraction(0))
    a2 = lapse**2 * sum((1 / gaps[1 << e]**2 for e in range(edges_count)), Fraction(0))
    a3 = -lapse**2 * sum((1 / gaps[1 << e]**3 for e in range(edges_count)), Fraction(0))
    t4, x4, n4 = q_words(gaps, edges_count, 4, lapse)
    t6, unused, n6 = q_words(gaps, edges_count, 6, lapse)
    d = t4 - b * a2
    c = t6 - b * x4 + b*b*a3 - d*a2
    return {2: b, 4: d, 6: c}, {'b': b, 'A2': a2, 'A3': a3, 'T4': t4, 'X4': x4,
                               'T6': t6, 'E4': d, 'E6': c}, {'four': n4, 'six': n6}


def component_masks(edges):
    remaining, out = set(range(len(edges))), []
    while remaining:
        component = {remaining.pop()}
        vertices = set(edges[next(iter(component))])
        changed = True
        while changed:
            changed = False
            for e in sorted(remaining):
                if vertices & set(edges[e]):
                    remaining.remove(e)
                    component.add(e)
                    vertices.update(edges[e])
                    changed = True
        out.append(sum(1 << e for e in component))
    return out


def polynomial_mul(left, right):
    out = [Fraction(0)] * 7
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            if i+j <= 6:
                out[i+j] += a*b
    return out


def pair_polynomial(energies, single_a, single_b, double):
    factors = []
    for shift in (0, double, single_a, single_b):
        factor = list(energies)
        factor[0] -= shift
        factors.append(factor)
    first = [Fraction(1)] + [Fraction(0)] * 6
    for factor in factors:
        first = polynomial_mul(first, factor)
    second_a = [2 * x for x in energies]
    second_b = list(second_a)
    second_a[0] -= double
    second_b[0] -= single_a + single_b
    second = polynomial_mul(second_a, second_b)
    return [first[r] - (second[r-2] if r >= 2 else 0) for r in range(7)]


def analyze_cluster(edges, signs, q):
    checks, data, coefficients = [], {}, {0: [Fraction(0)] * 7}
    weights = {0: [Fraction(0)] * 7}
    m = len(edges)
    for mask in range(1, 1 << m):
        chosen = [e for e in range(m) if mask & (1 << e)]
        subedges, subsigns = tuple(edges[e] for e in chosen), tuple(signs[e] for e in chosen)
        direct, expanded = gap_forms(subedges, subsigns, q)
        for s in range(1 << len(chosen)):
            checks_add(checks, f'mask{mask}_gap_forms{s}', direct[s] == expanded[s])
            if s:
                checks_add(checks, f'mask{mask}_positive_gap{s}', direct[s] > 0)
        energy, amplitudes = recurrence(direct, len(chosen))
        folds, terms, words = canonical_folds(expanded, len(chosen))
        coefficients[mask] = energy
        for r in ORDERS:
            checks_add(checks, f'mask{mask}_method_order{r}', energy[r] == folds[r])
        for r in (1, 3, 5):
            checks_add(checks, f'mask{mask}_odd_order{r}', energy[r] == 0)
        weight = [Fraction(0)] * 7
        for r in ORDERS:
            weight[r] = energy[r] - sum((weights[t][r] for t in submasks(mask) if t not in (0, mask)), Fraction(0))
            mobius = sum(((-1)**(mask.bit_count()-t.bit_count()) * coefficients[t][r]
                          for t in submasks(mask)), Fraction(0))
            checks_add(checks, f'mask{mask}_mobius_order{r}', weight[r] == mobius)
            if r < 2*len(chosen):
                checks_add(checks, f'mask{mask}_below_min_order{r}', weight[r] == 0)
        weights[mask] = weight
        components = component_masks(subedges)
        if len(components) > 1:
            parent_components = [sum(1 << chosen[e] for e in range(len(chosen)) if cm & (1 << e))
                                 for cm in components]
            for r in ORDERS:
                checks_add(checks, f'mask{mask}_disconnected_zero_order{r}', weight[r] == 0)
                checks_add(checks, f'mask{mask}_factorized_order{r}',
                           energy[r] == sum((coefficients[c][r] for c in parent_components), Fraction(0)))
        if len(chosen) == 1:
            delta = direct[1]
            for r, expected in ((2, -1/delta), (4, 1/delta**3), (6, -2/delta**5)):
                checks_add(checks, f'mask{mask}_single_exact_order{r}', energy[r] == expected)
        pair_residual = None
        if len(chosen) == 2:
            pair_residual = pair_polynomial(energy, direct[1], direct[2], direct[3])
            for r, value in enumerate(pair_residual):
                checks_add(checks, f'mask{mask}_pair_polynomial_order{r}', value == 0)
            if len(components) == 1:
                if q == 1:
                    control = {(1, 1): (Fraction(-10), Fraction(-6)),
                               (-1, -1): (Fraction(-7, 243), Fraction(-1, 81)),
                               (-1, 1): (Fraction(-128, 243), Fraction(40, 27))}[tuple(sorted(subsigns))]
                else:
                    control = (Fraction(-1, 4), Fraction(-1, 8)) if subsigns[0] == subsigns[1] else (Fraction(1, 4), Fraction(3, 8))
                checks_add(checks, f'mask{mask}_pair_raw_c6_control', energy[6] == control[0])
                checks_add(checks, f'mask{mask}_pair_linked_c6_control', weight[6] == control[1])
        source = {}
        for lapse in (Fraction(1, 2), Fraction(2)):
            scaled_gaps, unused = gap_forms(subedges, subsigns, q, lapse)
            scaled_energy, unused = recurrence(scaled_gaps, len(chosen), lapse)
            for r in range(1, 7):
                checks_add(checks, f'mask{mask}_source_L{lapse}_order{r}', scaled_energy[r] == lapse*energy[r])
            source[str(lapse)] = [exact(value) for value in scaled_energy]
        data[str(mask)] = {'original_edge_indices': chosen, 'edges': list(subedges), 'signs': list(subsigns),
                           'gaps': [exact(x) for x in direct],
                           'energy_coefficients_r0_to_r6': [exact(x) for x in energy],
                           'amplitude_coefficients_order_then_mask': [[exact(x) for x in values] for values in amplitudes],
                           'canonical_terms': {key: exact(value) for key, value in terms.items()},
                           'Q_only_word_counts': words,
                           'connected_weight_r0_to_r6': [exact(x) for x in weight],
                           'component_masks_within_subset': components,
                           'pair_polynomial_residual': None if pair_residual is None else [exact(x) for x in pair_residual],
                           'uniform_source_coefficients': source}
    return data, coefficients[(1 << m)-1], weights[(1 << m)-1], checks


def derive_embeddings():
    counts = {'single_add': 2, 'single_remove': 2}
    counts.update({'pair_add_add': 2, 'pair_remove_remove': 2, 'pair_add_remove': 2*2*2})
    counts.update({'star_add_add_remove': 2*2, 'star_add_remove_remove': 2*2})
    mapping = {min(signs, signs[::-1]): label for label, edges, signs, wanted in CLASSES if label.startswith('path_')}
    for label in mapping.values():
        counts[label] = 0
    for middle in (-1, 1):
        available = {1: 2-int(middle == 1), -1: 2-int(middle == -1)}
        for left in (-1, 1):
            for right in (-1, 1):
                key = min((left, middle, right), (right, middle, left))
                counts[mapping[key]] += 2*available[left]*available[right]
    return counts


def disconnected_specs():
    out = []
    for length in (2, 3):
        edges = tuple((2*i, 2*i+1) for i in range(length))
        for signs in product((-1, 1), repeat=length):
            out.append((f'matching{length}_' + ''.join('A' if x == 1 else 'R' for x in signs), edges, signs))
    for signs in product((-1, 1), repeat=3):
        out.append(('pair_plus_single_' + ''.join('A' if x == 1 else 'R' for x in signs),
                    ((0, 1), (1, 2), (3, 4)), signs))
    return out


def format_report(result):
    def rat(value):
        return str(value['numerator']) + '/' + str(value['denominator'])
    lines = ['# Native homogeneous record-feedback diagonal through sixth order V001', '',
             f"Arithmetic controls: {result['checks_passed']}/{result['checks_total']}; failed {result['checks_failed']}.", '',
             'Exact formal diagonal coefficients only. No full finite-h remainder, converged phase, matter pole, clock, ruler, gravity or expansion claim.', '',
             '| q | colored class | embeddings/N | raw E2 | raw E4 | raw E6 | linked W2 | linked W4 | linked W6 |',
             '|---:|---|---:|---:|---:|---:|---:|---:|---:|']
    for row in result['rows']:
        vals = [rat(row[key][str(r)]) for key in ('energy_coefficients', 'connected_weights') for r in ORDERS]
        lines.append(f"| {row['q']} | {row['class']} | {row['embeddings_per_N']} | " + ' | '.join(vals) + ' |')
    lines += ['', '| uniform q | homogeneous c2 | homogeneous c4 | homogeneous c6 | formal polynomial at h=1/5 |',
              '|---:|---:|---:|---:|---:|']
    for q in (0, 1):
        data = result['homogeneous_per_N'][str(q)]
        lines.append(f'| {q} | ' + ' | '.join(rat(data['coefficients'][str(r)]) for r in ORDERS)
                     + ' | ' + rat(data['formal_truncated_at_h_one_fifth']) + ' |')
    lines += ['', 'The qblank complete GL6AO diagonal is a recovered control; occupied q1 sixth order is an unselected new output. Every canonical normalization fold and all disconnected cancellations are retained.', '',
              'This homogeneous diagonal does not select a ring phase: the separate sealed offdiagonal hex matrix enters the complete order-six effective Hamiltonian. No older symmetric remainder or phase result is imported into q1.', '',
              'All26 connected rows,40 disconnected controls, subcluster amplitudes, independent Q words/folds, source controls and exact rationals are preserved in JSON/checkpoints. Directed Decimal20 displays are diagnostic; exact Fractions are authoritative. Ancestors were authenticated as bytes only.', '']
    return '\n'.join(lines)


def main():
    global ATTEMPT_CREATED
    for path in (RESULT, REPORT, RECEIPT, CP):
        if path.exists():
            raise FileExistsError('Exclusive reserved output exists: ' + str(path))
    inputs = authenticate()
    source_hash, protocol_hash = sha(SOURCE), sha(PROTOCOL)
    CP.mkdir()
    ATTEMPT_CREATED = True
    manifest = {'schema': NAME + '_INPUT_MANIFEST', 'pid': os.getpid(),
                'source_sha256': source_hash, 'protocol_sha256': protocol_hash, 'input_sha256': inputs,
                'class_specs': [{'class': label, 'edges': list(edges), 'signs': list(signs), 'embeddings_per_N': count}
                                for label, edges, signs, count in CLASSES],
                'q_values': [0, 1], 'h': exact(H), 'maximum_scalar_basis_masks': 8,
                'forbidden': ['H_action', 'import_ancestor', 'evolution', 'eigensolver', 'NPZ', 'finite_h_phase']}
    manifest_hash = exclusive(CP / 'input_manifest.json', manifest)
    event('started', manifest_sha256=manifest_hash, source_sha256=source_hash, protocol_sha256=protocol_hash)
    rows, weights, row_hashes = [], {}, {}
    global_checks, embeddings = [], derive_embeddings()
    checks_add(global_checks, 'exact_thirteen_classes', len(CLASSES) == len(embeddings) == 13)
    for label, edges, signs, count in CLASSES:
        checks_add(global_checks, label + '_derived_embedding', embeddings[label] == count)
    for q in (0, 1):
        for label, edges, signs, count in CLASSES:
            started = time.perf_counter()
            data, energy, weight, checks = analyze_cluster(edges, signs, q)
            for v in set(x for edge in edges for x in edge):
                incident = [signs[e] for e, edge in enumerate(edges) if v in edge]
                checks_add(checks, f'collar_vertex{v}', incident.count(1) <= 2 and incident.count(-1) <= 2)
            checks_add(checks, 'representative_connected', len(component_masks(edges)) == 1)
            row = {'q': q, 'class': label, 'edges': list(edges), 'signs': list(signs), 'embeddings_per_N': count,
                   'subclusters': data, 'energy_coefficients': {str(r): exact(energy[r]) for r in ORDERS},
                   'connected_weights': {str(r): exact(weight[r]) for r in ORDERS}, 'checks': checks,
                   'row_elapsed_seconds': time.perf_counter() - started}
            path = CP / f'q{q}_{label}.json'
            digest = exclusive(path, row)
            row_hashes[path.name] = digest
            event('row_complete', q=q, class_name=label, filename=path.name, sha256=digest,
                  checks_failed=sum(not x['passed'] for x in checks))
            rows.append(row)
            weights[(q, label)] = weight
    disconnected, control_hashes = [], {}
    for q in (0, 1):
        controls = []
        for label, edges, signs in disconnected_specs():
            data, energy, weight, checks = analyze_cluster(edges, signs, q)
            checks_add(checks, 'disconnected_control_components', len(component_masks(edges)) > 1)
            for r in ORDERS:
                checks_add(checks, f'whole_connected_zero_order{r}', weight[r] == 0)
            controls.append({'q': q, 'control': label, 'edges': list(edges), 'signs': list(signs),
                             'subclusters': data, 'energy_coefficients': {str(r): exact(energy[r]) for r in ORDERS},
                             'connected_weights': {str(r): exact(weight[r]) for r in ORDERS}, 'checks': checks})
        path = CP / f'q{q}_disconnected_controls.json'
        digest = exclusive(path, {'q': q, 'controls': controls})
        control_hashes[path.name] = digest
        event('disconnected_controls_complete', q=q, filename=path.name, sha256=digest, control_count=len(controls))
        disconnected.extend(controls)
    homogeneous = {}
    for q in (0, 1):
        coeff = {r: sum((count * weights[(q, label)][r] for label, edges, signs, count in CLASSES), Fraction(0))
                 for r in ORDERS}
        anchors = {2: Fraction(-2), 4: Fraction(-7, 6), 6: Fraction(-893, 270)} if q == 0 else {2: Fraction(-8, 3), 4: Fraction(5, 9)}
        for r, target in anchors.items():
            checks_add(global_checks, f'q{q}_homogeneous_order{r}_known_control', coeff[r] == target)
        homogeneous[str(q)] = {'coefficients': {str(r): exact(coeff[r]) for r in ORDERS},
                               'formal_truncated_at_h_one_fifth': exact(sum((coeff[r]*H**r for r in ORDERS), Fraction(0))),
                               'q1_c6_expected_target': None, 'finite_h_control': False}
    checks_add(global_checks, 'all26_connected_rows', len(rows) == 26)
    checks_add(global_checks, 'all40_disconnected_controls', len(disconnected) == 40)
    checks_add(global_checks, 'final_input_bytes_unchanged', authenticate() == inputs)
    checks_add(global_checks, 'source_protocol_unchanged', sha(SOURCE) == source_hash and sha(PROTOCOL) == protocol_hash)
    allchecks = global_checks + [c for row in rows + disconnected for c in row['checks']]
    failed = sum(not x['passed'] for x in allchecks)
    result = {'schema': NAME + '_RESULT', 'status': 'EXACT_COEFFICIENT_ARITHMETIC_PASS' if not failed else 'ARITHMETIC_FAILED_PRESERVED',
              'pid': os.getpid(), 'source_sha256': source_hash, 'protocol_sha256': protocol_hash,
              'input_sha256': inputs, 'manifest_sha256': manifest_hash, 'row_sha256': row_hashes,
              'control_sha256': control_hashes, 'rows': rows, 'disconnected_controls': disconnected,
              'derived_embeddings_per_N': embeddings, 'homogeneous_per_N': homogeneous,
              'global_checks': global_checks, 'checks_total': len(allchecks),
              'checks_passed': len(allchecks)-failed, 'checks_failed': failed,
              'finite_h_control': False, 'phase_selected_ground_energy': False,
              'matter_clock_ruler_gravity_expansion_claim': False,
              'elapsed_seconds': time.perf_counter()-T0,
              'ru_maxrss_native': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    report = format_report(result)
    class_table = report.split('| q | colored class |', 1)[1].split('| uniform q |', 1)[0]
    assembly_table = report.split('| uniform q |', 1)[1]
    if class_table.count('\n| ') != 26 or assembly_table.count('\n| ') != 2:
        raise RuntimeError('Report must contain26 class DATA rows and2 assembly DATA rows')
    result_hash = exclusive(RESULT, result)
    with REPORT.open('x', encoding='utf-8') as stream:
        stream.write(report)
        stream.flush()
        os.fsync(stream.fileno())
    report_hash = sha(REPORT)
    event('result_complete', raw_sha256=result_hash, report_sha256=report_hash,
          checks_passed=result['checks_passed'], checks_total=result['checks_total'])
    receipt = {'schema': NAME + '_RECEIPT', 'pid': os.getpid(), 'status': result['status'],
               'result_raw_sha256': result_hash, 'result_canonical_sha256': hashlib.sha256(canonical(result)).hexdigest(),
               'report_sha256': report_hash, 'manifest_sha256': manifest_hash,
               'journal_prefix_sha256': sha(CP / 'journal.jsonl'), 'row_sha256': row_hashes,
               'control_sha256': control_hashes, 'source_sha256': source_hash, 'protocol_sha256': protocol_hash,
               'input_sha256': inputs, 'checks_passed': result['checks_passed'], 'checks_total': result['checks_total'],
               'checks_failed': failed, 'elapsed_seconds': result['elapsed_seconds']}
    receipt_hash = exclusive(RECEIPT, receipt)
    event('receipt_complete', receipt_sha256=receipt_hash)
    print(json.dumps({'pid': os.getpid(), 'status': result['status'], 'checks_passed': result['checks_passed'],
                      'checks_total': result['checks_total'], 'checks_failed': failed,
                      'result_raw_sha256': result_hash, 'receipt_sha256': receipt_hash,
                      'elapsed_seconds': result['elapsed_seconds']}))
    return 0 if not failed else 2


if __name__ == '__main__':
    T0 = time.perf_counter()
    try:
        sys.exit(main())
    except Exception as error:
        if ATTEMPT_CREATED:
            payload = {'pid': os.getpid(), 'exception_type': type(error).__name__, 'error': str(error),
                       'traceback': traceback.format_exc(), 'elapsed_seconds': time.perf_counter()-T0}
            path = CP / 'ERROR.json'
            if not path.exists():
                digest = exclusive(path, payload)
                event('error', filename=path.name, sha256=digest)
        traceback.print_exc()
        sys.exit(3)

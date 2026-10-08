#!/usr/bin/env python3
"""Frozen tiny exact coefficient gate; imports only the Python standard library."""
from decimal import Decimal, ROUND_FLOOR, ROUND_CEILING, localcontext
from fractions import Fraction
from itertools import permutations
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
NAME = 'BS10_RECORD_FEEDBACK_HEX_RING_V001'
PROTOCOL = J / (NAME + '.md')
RESULT = J / (NAME + '_RESULT.json')
REPORT = J / (NAME + '_RESULT.md')
RECEIPT = J / (NAME + '_RECEIPT.json')
CP = J / 'bs10_record_feedback_hex_ring_v001_checkpoints'
SOURCE = Path(__file__).resolve()
ATTEMPT_CREATED = False
H = Fraction(1, 5)
EPS = tuple(1 if i % 2 == 0 else -1 for i in range(6))
ORDERS = tuple(permutations(range(6)))
INPUTS = {
    'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/LOCAL_PROPER_BOND_NORMALIZATION_V001.md': '9b4cc5e1942ac7373e210efa46bfa74e03bbcfb8130c01232373b02e8a622a5b',
    'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/DEGREE_TWO_JOINT_MATTER_REFERENCE_GATE_V001.md': '84e889f6148b43c91c2ef1a0e3194a8723e190bcf5f9a16407013e85b6a02a83',
    'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/recovered_sources/BS_MICRO_ACTION.md': '00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec',
    'program-worktree/LANE_CROSS_RFT_GRA_GL6AO_COMPLETE_SIXTH_ORDER_LOCKED_HAMILTONIAN_V001/THEOREM.md': 'f75edcb115c3f7c86c6598f4597366b36e363df2d03ad919cc607b57dfb6b20c',
    'program-worktree/LANE_CROSS_RFT_GRA_GL6AO_COMPLETE_SIXTH_ORDER_LOCKED_HAMILTONIAN_V001/verify_sixth_order_hamiltonian.py': '6cd1c8533821012e3281310ec0dadc95f8788ecf74729ba912f56d46f5a9b271',
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


def event(kind, **kw):
    row = {'event': kind, 'pid': os.getpid(), 'elapsed_seconds': time.perf_counter() - T0, **kw}
    with (CP / 'journal.jsonl').open('ab') as stream:
        stream.write(canonical(row) + b'\n')
        stream.flush()
        os.fsync(stream.fileno())


def exact(value):
    value = Fraction(value)
    out = {'numerator': value.numerator, 'denominator': value.denominator}
    displays = []
    for rounding in (ROUND_FLOOR, ROUND_CEILING):
        with localcontext() as ctx:
            ctx.prec = 20
            ctx.rounding = rounding
            displays.append(str(Decimal(value.numerator) / Decimal(value.denominator)))
    out['decimal20_lower'], out['decimal20_upper'] = displays
    return out


def check(log, label, condition):
    log.append({'label': label, 'passed': bool(condition)})


def authenticate():
    observed = {}
    for rel, wanted in INPUTS.items():
        got = sha(ROOT / rel)
        if got != wanted:
            raise RuntimeError('Frozen input mismatch: ' + rel)
        observed[rel] = got
    return observed


def gaps_direct(q, eps=EPS):
    values = []
    for mask in range(64):
        charges = [eps[(v-1) % 6] * bool(mask & (1 << ((v-1) % 6)))
                   + eps[v] * bool(mask & (1 << v)) for v in range(6)]
        values.append(sum((Fraction(d*d) - Fraction(q[v]*d, 2)
                           for v, d in enumerate(charges)), Fraction(0)))
    return values


def gaps_boundary(q, eps=EPS):
    values = []
    for mask in range(64):
        twice_energy = 0
        for v in range(6):
            left = bool(mask & (1 << ((v-1) % 6)))
            right = bool(mask & (1 << v))
            if left != right:
                sign = eps[(v-1) % 6] if left else eps[v]
                twice_energy += 2 - q[v] * sign
        values.append(Fraction(twice_energy, 2))
    return values


def subset_dp(gaps):
    weights = [Fraction(0) for _ in range(64)]
    weights[0] = Fraction(1)
    for size in range(1, 6):
        for mask in range(1, 63):
            if mask.bit_count() == size:
                weights[mask] = sum((weights[mask ^ (1 << e)] for e in range(6)
                                     if mask & (1 << e)), Fraction(0)) / gaps[mask]
    return sum((weights[63 ^ (1 << e)] for e in range(6)), Fraction(0))


def path_sum(gaps):
    total = Fraction(0)
    for order in ORDERS:
        mask, weight = 0, Fraction(1)
        for e in order[:5]:
            mask |= 1 << e
            weight /= gaps[mask]
        total += weight
    return total


def row(qmask):
    started = time.perf_counter()
    q = tuple((qmask >> v) & 1 for v in range(6))
    direct, boundary = gaps_direct(q), gaps_boundary(q)
    checks = []
    check(checks, 'empty_full_gap_zero', direct[0] == direct[63] == 0)
    for mask in range(64):
        check(checks, 'denominator_forms_' + str(mask), direct[mask] == boundary[mask])
        if 0 < mask < 63:
            check(checks, 'proper_gap_positive_' + str(mask), direct[mask] >= 1)
    dp, paths = subset_dp(direct), path_sum(boundary)
    reversed_paths = path_sum(gaps_boundary(q, tuple(-e for e in EPS)))
    check(checks, '720_orders', len(ORDERS) == 720)
    check(checks, 'independent_dp_path_equal', dp == paths)
    check(checks, 'orientation_reversal_equal', dp == reversed_paths)
    check(checks, 'positive_coefficient', dp > 0)
    check(checks, 'exact_h6_scaling', dp * H**6 / H**6 == dp)
    if qmask == 0:
        check(checks, 'sealed_blank_control_63_over_8', dp == Fraction(63, 8))
    if qmask == 63:
        check(checks, 'new_q1_hand_control_2504_over_81', dp == Fraction(2504, 81))
        check(checks, 'new_q1_J6_control', dp * H**6 == Fraction(2504, 1265625))
    return {
        'qmask': qmask, 'q_v0_to_v5': list(q), 'record_count': sum(q),
        'proper_gap_min': exact(min(direct[1:63])),
        'proper_gap_max': exact(max(direct[1:63])),
        'c6_dp': exact(dp), 'c6_720_paths': exact(paths),
        'c6_orientation_reversed': exact(reversed_paths), 'J6': exact(dp * H**6),
        'effective_offdiagonal_sign': 'NEGATIVE',
        'checks': checks, 'row_elapsed_seconds': time.perf_counter() - started,
    }, dp


def transform(qmask, shift, reflected):
    q = [(qmask >> v) & 1 for v in range(6)]
    return sum(q[((-v if reflected else v) + shift) % 6] << v for v in range(6))


def format_report(result):
    def rational(value):
        return str(value['numerator']) + '/' + str(value['denominator'])
    lines = ['# Native record-feedback hexagon exact coefficient V001', '',
             f"Arithmetic controls: {result['checks_passed']}/{result['checks_total']}; failed {result['checks_failed']}.", '',
             'All64 fixed record words; no full finite-h remainder, diagonal-order6, matter-pole, phase or physical-clock claim.', '',
             'Global c6 extrema: [' + rational(result['c6_global_min']) + ', '
             + rational(result['c6_global_max']) + '].', '',
             '| qmask | q(v0..v5) | occupied | c6 exact | J6 at h=1/5 exact |',
             '|---:|---|---:|---:|---:|']
    for data in result['rows']:
        c, j = data['c6_dp'], data['J6']
        lines.append(f"| {data['qmask']} | {''.join(map(str, data['q_v0_to_v5']))} | {data['record_count']} | {c['numerator']}/{c['denominator']} | {j['numerator']}/{j['denominator']} |")
    lines += ['', '| occupied record count | words | distinct c6 | minimum c6 exact | maximum c6 exact |',
              '|---:|---:|---:|---:|---:|']
    for count in range(7):
        group = result['range_by_record_count'][str(count)]
        lines.append(f"| {count} | {group['word_count']} | {group['distinct_coefficients']} | "
                     + rational(group['c6_min']) + ' | ' + rational(group['c6_max']) + ' |')
    lines += ['', 'Uniform blank recovers the sealed symmetric63/8. Uniform occupied tests the NEW actual add1/remove3 coefficient2504/81, with independent DP/path controls. The actual matrix element is minus J6. Complete record storage/feedback is retained.', '',
              'All inputs, partial rows and exact rationals are sealed in the companion JSON/checkpoints. Decimal20 interval displays are diagnostic; exact Fractions are authoritative. No ancestor was imported or executed.', '',
              'The old symmetric scalar-diagonal theorem and phase evidence are not imported into the detuned local family. A finite-h local/linked-cluster or complementary-defect bound remains required.', '']
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
                'source_sha256': source_hash, 'protocol_sha256': protocol_hash,
                'input_sha256': inputs, 'h': exact(H), 'Ud': exact(1),
                'lambda_R': exact(Fraction(1, 2)), 'record_words': 64,
                'orders_per_word': 720, 'allowed_old_source_use': 'BYTES_ONLY',
                'forbidden': ['H_action', 'import_ancestor', 'evolution', 'eigensolver', 'NPZ']}
    manifest_hash = exclusive(CP / 'input_manifest.json', manifest)
    event('started', manifest_sha256=manifest_hash, source_sha256=source_hash,
          protocol_sha256=protocol_hash)
    rows, coeffs, row_hashes = [], {}, {}
    for qmask in range(64):
        data, coeff = row(qmask)
        path = CP / f'q_{qmask:02d}.json'
        digest = exclusive(path, data)
        event('row_complete', qmask=qmask, filename=path.name, sha256=digest,
              checks_failed=sum(not c['passed'] for c in data['checks']))
        rows.append(data)
        coeffs[qmask] = coeff
        row_hashes[path.name] = digest
    checks = []
    check(checks, 'all64_words_retained', len(rows) == len(coeffs) == 64)
    for qmask in range(64):
        for shift in range(6):
            for reflected in (False, True):
                target = transform(qmask, shift, reflected)
                check(checks, f'dihedral_{qmask}_{shift}_{int(reflected)}',
                      coeffs[qmask] == coeffs[target])
    check(checks, 'final_input_bytes_unchanged', authenticate() == inputs)
    check(checks, 'source_protocol_unchanged', sha(SOURCE) == source_hash and sha(PROTOCOL) == protocol_hash)
    grouped = {}
    for count in range(7):
        values = [coeffs[qmask] for qmask in range(64) if qmask.bit_count() == count]
        grouped[str(count)] = {'word_count': len(values), 'c6_min': exact(min(values)),
                               'c6_max': exact(max(values)),
                               'distinct_coefficients': len(set(values))}
    allchecks = checks + [c for data in rows for c in data['checks']]
    failed = sum(not c['passed'] for c in allchecks)
    result = {'schema': NAME + '_RESULT', 'status': 'EXACT_COEFFICIENT_ARITHMETIC_PASS' if not failed else 'ARITHMETIC_FAILED_PRESERVED',
              'pid': os.getpid(), 'source_sha256': source_hash, 'protocol_sha256': protocol_hash,
              'input_sha256': inputs, 'manifest_sha256': manifest_hash, 'row_sha256': row_hashes,
              'rows': rows, 'global_checks': checks, 'checks_total': len(allchecks),
              'checks_passed': len(allchecks) - failed, 'checks_failed': failed,
              'c6_global_min': exact(min(coeffs.values())), 'c6_global_max': exact(max(coeffs.values())),
              'range_by_record_count': grouped,
              'finite_h_control': False, 'diagonal_order6_computed': False,
              'phase_clock_matter_gravity_claim': False,
              'elapsed_seconds': time.perf_counter() - T0,
              'ru_maxrss_native': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    report = format_report(result)
    word_table = report.split('| qmask |', 1)[1].split('| occupied record count |', 1)[0]
    range_table = report.split('| occupied record count |', 1)[1]
    if word_table.count('\n| ') != 64 or range_table.count('\n| ') != 7:
        raise RuntimeError('Report must contain exactly64 word data rows and7 record-count data rows')
    raw_hash = exclusive(RESULT, result)
    with REPORT.open('x', encoding='utf-8') as stream:
        stream.write(report)
        stream.flush()
        os.fsync(stream.fileno())
    report_hash = sha(REPORT)
    event('result_complete', raw_sha256=raw_hash, report_sha256=report_hash,
          checks_passed=result['checks_passed'], checks_total=result['checks_total'])
    receipt = {'schema': NAME + '_RECEIPT', 'pid': os.getpid(),
               'result_raw_sha256': raw_hash, 'result_canonical_sha256': hashlib.sha256(canonical(result)).hexdigest(),
               'report_sha256': report_hash, 'manifest_sha256': manifest_hash,
               'journal_prefix_sha256': sha(CP / 'journal.jsonl'), 'row_sha256': row_hashes,
               'source_sha256': source_hash, 'protocol_sha256': protocol_hash,
               'input_sha256': inputs, 'checks_passed': result['checks_passed'],
               'checks_total': result['checks_total'], 'checks_failed': failed,
               'elapsed_seconds': result['elapsed_seconds'], 'status': result['status']}
    receipt_hash = exclusive(RECEIPT, receipt)
    event('receipt_complete', receipt_sha256=receipt_hash)
    print(json.dumps({'pid': os.getpid(), 'status': result['status'],
                      'checks_passed': result['checks_passed'], 'checks_total': result['checks_total'],
                      'checks_failed': failed, 'elapsed_seconds': result['elapsed_seconds'],
                      'result_raw_sha256': raw_hash, 'receipt_sha256': receipt_hash}, sort_keys=True), flush=True)
    return 0 if not failed else 3


T0 = time.perf_counter()
if __name__ == '__main__':
    try:
        sys.exit(main())
    except BaseException as exc:
        if not isinstance(exc, SystemExit) and ATTEMPT_CREATED:
            error = {'schema': NAME + '_ERROR', 'pid': os.getpid(), 'error': repr(exc),
                     'traceback': traceback.format_exc(), 'elapsed_seconds': time.perf_counter() - T0}
            path = CP / 'error.json'
            if not path.exists():
                digest = exclusive(path, error)
                event('error_preserved', sha256=digest)
        raise

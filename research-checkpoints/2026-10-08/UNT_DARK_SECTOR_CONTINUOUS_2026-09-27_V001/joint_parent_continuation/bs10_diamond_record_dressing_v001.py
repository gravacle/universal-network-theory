#!/usr/bin/env python3
"""New exact held-diamond return-moment arithmetic; execute only after preflight.

No old module is imported. No Hamiltonian, propagation or eigensolver is run.
The complete g^2 curvature is perturbative; full energy uses separate theorems.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from fractions import Fraction as F
import hashlib
import json
from math import factorial
import os
from pathlib import Path
import resource
import sys
import time
import traceback

ROOT = Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
JREL = 'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/'
J = ROOT / JREL
PROTOCOL = J / 'BS10_DIAMOND_RECORD_DRESSING_V001.md'
SOURCE = J / 'bs10_diamond_record_dressing_v001.py'
RESULT = J / 'BS10_DIAMOND_RECORD_DRESSING_V001_RESULT.json'
REPORT = J / 'BS10_DIAMOND_RECORD_DRESSING_V001_RESULT.md'
RECEIPT = J / 'BS10_DIAMOND_RECORD_DRESSING_V001_RECEIPT.json'
CP = J / 'bs10_diamond_record_dressing_v001_checkpoints'
MAX_N = 12
CONV_N = 6
DISPLAY_PRECISION = 20
SQRT_SCALE = 10**40
E0, G, C0 = F(8, 5), F(1, 10), F(2, 15)
R = F(4, 49)
ANCHORS = {
    'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/recovered_sources/BS_MICRO_ACTION.md':
        '00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec',
    'program-worktree/LANE_GRA_FF_F3_Q4_CARRIER_LIFT_DERIVABILITY_NO_GO_V001/THEOREM.md':
        '4c5d476e007f36b20f3e34964607c013ab28ae16bf884c063b7f4ac954178e5a',
    'program-worktree/LANE_GRA_FE_F3_Q4_DIAMOND_ICE_CARRIER_JOIN_V001/THEOREM.md':
        '4cc63e3e5853b4250a2a5b78256d41b83b195cf527901819a62a04ef53f8d932',
    JREL + 'BS10_K33_UNCLAMPED_FORMATION_V001.md':
        '8391edb0b3ac88268605f30d6e9589c05871fd570f48bee18ae845fcaec060c6',
    JREL + 'bs10_k33_unclamped_formation_v001.py':
        '2a6d6326592dee5fb04ba47776ea495df68c0acdf7dce22f26f4be0eae0a1b6c',
    JREL + 'BS10_K33_UNCLAMPED_FORMATION_V001_RESULT.json':
        '21bf1c0abaf548364665aee7d5e4559f3a0457899fcb25f3f7e35cc52d7c317b',
    JREL + 'KINETIC_RULER_AND_PHYSICAL_CENSUS_HYPOTHESIS_V001.md':
        'f5b2986719281523ba348822292ee20d8bb3062c082c42eb0192dbf3ddb50af1',
    JREL + 'DIAMOND_KINETIC_CENSUS_PREFIT_SCREEN_V001.md':
        '3b54496315835853fd5e29df90db51a01e8378ed8029e0f0b4e03367ed4fc9a5',
}
SCOPE = (
    'Held supplied infinite/deep-bulk diamond, saturated incidence/flip OFF, '
    'one chosen conserved carrier content x, record alphabet B/x and occupied-x '
    'background, fixed tetrahedral chart ell. Exact integer/Fraction moment '
    'arithmetic only. All-order positive addition-energy bounds are separate '
    'from formal g^2 energy/curvature coefficients; omitted g^4 curvature is '
    'not bounded. No physical 3D phase, metric, clock, gravity, census growth, '
    'observational fit or Stage3 closure is claimed.'
)


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'),
                      allow_nan=False).encode('utf-8')


def write_json(path, obj):
    data = (json.dumps(obj, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()
    with path.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    return sha(path)


def event(kind, **fields):
    line = json.dumps({'event': kind, 'utc': now(), **fields},
                      sort_keys=True, allow_nan=False) + '\n'
    with (CP / 'events.jsonl').open('a', encoding='utf-8') as stream:
        stream.write(line)
        stream.flush()
        os.fsync(stream.fileno())


def directed(q, rounding):
    q = F(q)
    with localcontext() as ctx:
        ctx.prec = DISPLAY_PRECISION
        ctx.rounding = rounding
        return str(Decimal(q.numerator) / Decimal(q.denominator))


def rational(q):
    q = F(q)
    return {'numerator': str(q.numerator), 'denominator': str(q.denominator),
            'decimal20_floor': directed(q, ROUND_FLOOR),
            'decimal20_ceiling': directed(q, ROUND_CEILING)}


def interval(lo, hi):
    lo, hi = F(lo), F(hi)
    return {'lower': rational(lo), 'upper': rational(hi),
            'display_lower': directed(lo, ROUND_FLOOR),
            'display_upper': directed(hi, ROUND_CEILING)}


def check(checks, name, passed, **evidence):
    checks.append({'name': name, 'passed': bool(passed), 'evidence': evidence})


def authenticate():
    found = {name: sha(ROOT / name) for name in ANCHORS}
    if found != ANCHORS:
        raise RuntimeError('Frozen ancestor bytes do not match: ' +
                           repr({k: v for k, v in found.items() if v != ANCHORS[k]}))
    return found


def moment(n):
    total = 0
    fact = factorial(n)
    for a in range(n + 1):
        for b in range(n - a + 1):
            for c in range(n - a - b + 1):
                d = n - a - b - c
                m = fact // (factorial(a) * factorial(b) * factorial(c) * factorial(d))
                total += m * m
    return total


def convolved_moments():
    # Independent Laurent-polynomial multiplication of all16 |f|^2 monomials.
    axes = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
    step = Counter(tuple(a[k] - b[k] for k in range(3))
                   for a in axes for b in axes)
    state = {(0, 0, 0): 1}
    out = [1]
    for _ in range(CONV_N):
        nxt = Counter()
        for a, multiplicity in state.items():
            for b, weight in step.items():
                nxt[tuple(a[k] + b[k] for k in range(3))] += multiplicity * weight
        state = dict(nxt)
        out.append(state.get((0, 0, 0), 0))
    return out, dict(step)


def sqrt_bracket(radicand):
    # Integer bisection gives exact rational square bounds, no Decimal.sqrt.
    target = radicand * SQRT_SCALE**2
    low, high = 0, radicand * SQRT_SCALE + 1
    while high - low > 1:
        mid = (low + high) // 2
        if mid * mid <= target:
            low = mid
        else:
            high = mid
    return F(low, SQRT_SCALE), F(high, SQRT_SCALE)


def tuple_checks(checks):
    # Metadata only, no old executable module imported or scientific replay.
    parent = json.loads((J / 'BS10_K33_UNCLAMPED_FORMATION_V001_RESULT.json').read_text())
    p = parent['inputs']
    expected = {'epsilon_psi': 1.0, 'epsilon_r': 1.0, 'U_d': 1.0,
                'd_star': 2, 'lambda_J': 0.25, 'lambda_R': 0.5, 't': 0.1,
                'Nc': 1, 'other_copy_ports': 0, 'g': [0.0, 0.1]}
    for k, v in expected.items():
        check(checks, 'saved_native_tuple_' + k, p[k] == v, actual=p[k], expected=v)
    check(checks, 'saved_formation_qualified', parent['status'] == 'QUALIFIED_ARITHMETIC'
          and parent['passed_count'] == 1194, status=parent['status'],
          passed_count=parent['passed_count'])
    # Record preparation differs prospectively; it is NOT the old blank history.
    return {'saved_formation_metadata': expected, 'new_prepared_hold':
            {'incidence': 'saturated diamond; held OFF flips',
             'records': 'all occupied x; invariant alphabet B/x',
             'carrier': 'Nc1 fixed content x', 'g': rational(G)}}


def make_report(result):
    b = result['bands']
    lines = [
        '# Held-diamond active-record dressing V001 result', '',
        f"Status: {result['status']}; {result['passed_count']}/{result['check_count']} checks.", '',
        'This is a new exact arithmetic gate on the disclosed saturated diamond hold.',
        'All-order addition-energy bounds and perturbative curvature have different scope.', '',
        '| Quantity | Outward lower | Outward upper | Qualification |',
        '|---|---:|---:|---|',
    ]
    labels = [
        ('G1', 'one-hole resolvent G1', 'exact positive moment-tail interval'),
        ('G2', 'one-hole derivative G2', 'exact positive moment-tail interval'),
        ('full_energy_sharp', 'Full copy-on addition energy', 'all-order parity/trial bounds'),
        ('full_energy_wide', 'Wide full-energy control', 'all-order local/2x2 trial'),
        ('energy_g2', 'Energy through g^2 at g=.1', 'formal truncation; no g^4 bound'),
        ('curvature_g2_unit_ell', 'Curvature through g^2, ell=1', 'formal truncation; no full-g C claim'),
        ('curvature_ratio_g2', 'C/C0 through g^2', 'formal truncation only'),
    ]
    for key, label, qualification in labels:
        item = b[key]
        lines.append(f"| {label} | {item['display_lower']} | {item['display_upper']} | {qualification} |")
    lines += ['', 'The mu0,mu2,mu4,mu6 anchors are1,4,28,256; all13 exact moments',
              'and independent convolution through n=6 are retained in JSON/checkpoint.',
              'The positive full addition pole is earned in the fixed B/x record sector.',
              'The >=.7 separation is Gamma-fiber only, not an all-k or selected phase gap.', '',
              'Its selected Gamma B/x no-hole projection weight is >=81/82;',
              'this reference-sector projection weight is not a physical spectral residue.', '',
              'The complete matched background/source/work remains owned. Uniform lapse',
              'scales E and C together and does not change C/E; nonuniform source, support,',
              'physical clock/ruler/census, second probe and all Stage3 evidence remain open.', '',
              f"Runtime seconds: {result['runtime_seconds']:.9f}; PID: {result['pid']}.",
              f"Source SHA256: {result['source_sha256']}",
              f"Protocol SHA256: {result['protocol_sha256']}",
              f"Canonical result payload SHA256: {result['canonical_payload_sha256']}", '',
              'Failed checks:']
    failed = [c for c in result['checks'] if not c['passed']]
    lines.extend(['- ' + c['name'] for c in failed] if failed else ['None.'])
    return '\n'.join(lines) + '\n'


def run():
    if Path(__file__).resolve() != SOURCE:
        raise RuntimeError('Source must run from its exclusively owned sole-root path')
    reserved = (RESULT, REPORT, RECEIPT, CP)
    if any(p.exists() for p in reserved):
        raise FileExistsError('Refusing existing result/report/receipt/checkpoint; no rerun/resume')
    started, start = now(), time.perf_counter()
    CP.mkdir()
    (CP / 'events.jsonl').open('x').close()
    checks = []
    try:
        inputs_before = authenticate()
        source_hash, protocol_hash = sha(SOURCE), sha(PROTOCOL)
        manifest = {'started_utc': started, 'pid': os.getpid(),
                    'source_sha256': source_hash, 'protocol_sha256': protocol_hash,
                    'input_sha256': inputs_before, 'scope': SCOPE,
                    'frozen': {'max_n': MAX_N, 'convolution_n': CONV_N,
                               'sqrt_scale': str(SQRT_SCALE),
                               'display_precision': DISPLAY_PRECISION,
                               'e0': rational(E0), 'g': rational(G),
                               'C0_unit_ell': rational(C0), 'r': rational(R)},
                    'execution': 'stdlib only; no imported old code/H/propagation/eigensolver'}
        manifest_hash = write_json(CP / 'manifest.json', manifest)
        event('started', pid=os.getpid(), manifest_sha256=manifest_hash)
        ancestry = tuple_checks(checks)
        moments = [moment(n) for n in range(MAX_N + 1)]
        conv, step = convolved_moments()
        check(checks, 'independent_convolution_step_total16', sum(step.values()) == 16)
        check(checks, 'independent_convolution_zero_weight4', step[(0, 0, 0)] == 4)
        for n, mu in enumerate(moments):
            check(checks, f'moment_positive_n{n}', mu > 0, value=str(mu))
            check(checks, f'moment_spectral_bound_n{n}', mu <= 16**n,
                  value=str(mu), upper=str(16**n))
        for n, expected in enumerate((1, 4, 28, 256)):
            check(checks, f'exact_anchor_mu{2*n}', moments[n] == expected,
                  actual=str(moments[n]), expected=str(expected))
        for n, actual in enumerate(conv):
            check(checks, f'independent_convolution_n{n}', actual == moments[n],
                  actual=str(actual), composition=str(moments[n]))
        checkpoint = {'moments': [{'n': n, 'order': 2*n, 'value': str(mu)}
                                  for n, mu in enumerate(moments)],
                      'independent_convolution': [str(x) for x in conv],
                      'step': [{'exponent': list(k), 'multiplicity': v}
                               for k, v in sorted(step.items())],
                      'checks': checks, 'elapsed_seconds': time.perf_counter()-start}
        moment_hash = write_json(CP / 'moments.json', checkpoint)
        event('moments_completed', moments_sha256=moment_hash, failed_count=
              sum(not c['passed'] for c in checks))
        s1 = sum((F(mu, 14**(2*n)) for n, mu in enumerate(moments)), F(0))
        s2 = sum((F((2*n+1)*mu, 14**(2*n)) for n, mu in enumerate(moments)), F(0))
        t1 = R**13/(1-R)
        t2 = R**13*(F(27)/(1-R)+2*R/(1-R)**2)
        check(checks, 'r_equals_norm_ratio', R == F(16, 14**2))
        check(checks, 'positive_tails', t1 > 0 and t2 > 0)
        check(checks, 'tail2_independent_closed_form',
              t2 == R**13*(27-25*R)/(1-R)**2)
        check(checks, 'S1_spectral_series_bound', s1+t1 <= 1/(1-R))
        check(checks, 'S2_spectral_series_bound', s2+t2 <= (1+R)/(1-R)**2)
        g1lo, g1hi = F(5, 7)*s1, F(5, 7)*(s1+t1)
        g2lo, g2hi = F(25, 49)*s2, F(25, 49)*(s2+t2)
        roots = {}
        for radicand in (2, 26):
            lo, hi = sqrt_bracket(radicand)
            check(checks, f'sqrt{radicand}_rational_square_lower', lo*lo <= radicand)
            check(checks, f'sqrt{radicand}_rational_square_upper', hi*hi >= radicand)
            check(checks, f'sqrt{radicand}_frozen_width', hi-lo == F(1, SQRT_SCALE))
            roots[radicand] = (lo, hi)
        basic_l_lo, basic_l_hi = (21-roots[26][1])/10, (21-roots[26][0])/10
        basic_u_lo, basic_u_hi = (23-5*roots[2][1])/10, (23-5*roots[2][0])/10
        sharp_lo = E0-G*G*g1hi-F(1, 19900)
        sharp_hi = E0-G*G*g1lo/(1+G*G*g2hi)
        e2lo, e2hi = E0-G*G*g1hi, E0-G*G*g1lo
        z2lo, z2hi = 1-G*G*g2hi, 1-G*G*g2lo
        c2lo, c2hi = C0*z2lo, C0*z2hi
        check(checks, 'full_energy_positive_lower', sharp_lo > 0)
        check(checks, 'full_energy_sharp_ordering', sharp_lo <= sharp_hi)
        check(checks, 'sharp_improves_wide_lower', sharp_lo >= basic_l_hi)
        check(checks, 'sharp_improves_wide_upper', sharp_hi <= basic_u_lo)
        check(checks, 'formal_g2_curvature_positive_not_full_bound', z2lo > 0)
        check(checks, 'formal_energy_inside_full_energy_band',
              sharp_lo <= e2lo <= e2hi <= sharp_hi)
        check(checks, 'parity_remainder_exact',
              G**4/(F(1)*(F(2)-G*G)) == F(1, 19900))
        check(checks, 'Gamma_next_fiber_norm_gap', F(12, 5)-G-E0 == F(7, 10))
        check(checks, 'wide_gap_to_Qfull', F(13, 5)-G-E0 == F(9, 10))
        check(checks, 'Gamma_nohole_projection_weight_control',
              1/(1+(G/F(9, 10))**2) == F(81, 82))
        raw_bands = {
            'S1': (s1, s1+t1), 'S2': (s2, s2+t2),
            'G1': (g1lo, g1hi), 'G2': (g2lo, g2hi),
            'sqrt2': roots[2], 'sqrt26': roots[26],
            'basic_lower_bound': (basic_l_lo, basic_l_hi),
            'basic_upper_bound': (basic_u_lo, basic_u_hi),
            'full_energy_wide': (basic_l_lo, basic_u_hi),
            'full_energy_sharp': (sharp_lo, sharp_hi),
            'energy_g2_coefficient': (-g1hi, -g1lo),
            'curvature_g2_coefficient_unit_ell': (-C0*g2hi, -C0*g2lo),
            'energy_g2': (e2lo, e2hi),
            'curvature_ratio_g2': (z2lo, z2hi),
            'curvature_g2_unit_ell': (c2lo, c2hi),
        }
        for name, (lo, hi) in raw_bands.items():
            check(checks, name+'_ordered', lo <= hi)
            check(checks, name+'_display_outward',
                  F(Decimal(directed(lo, ROUND_FLOOR))) <= lo and
                  F(Decimal(directed(hi, ROUND_CEILING))) >= hi)
        inputs_after = authenticate()
        check(checks, 'input_seals_unchanged', inputs_before == inputs_after)
        check(checks, 'source_protocol_unchanged',
              sha(SOURCE) == source_hash and sha(PROTOCOL) == protocol_hash)
        failed = sum(not c['passed'] for c in checks)
        result = {'status': 'QUALIFIED_ARITHMETIC' if failed == 0 else 'FAILED_ARITHMETIC',
                  'scope': SCOPE, 'started_utc': started, 'finished_utc': now(),
                  'pid': os.getpid(), 'runtime_seconds': time.perf_counter()-start,
                  'peak_RSS_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  'source_sha256': source_hash, 'protocol_sha256': protocol_hash,
                  'input_sha256': inputs_after, 'manifest_sha256': manifest_hash,
                  'moments_checkpoint_sha256': moment_hash, 'ancestry': ancestry,
                  'moments': checkpoint['moments'], 'tails': {'S1': rational(t1),
                  'S2': rational(t2), 'r': rational(R)},
                  'bands': {name: interval(*bounds) for name, bounds in raw_bands.items()},
                  'full_energy_remainder_bound': rational(F(1, 19900)),
                  'Gamma_fiber_gap_lower': rational(F(7, 10)),
                  'Gamma_nohole_projection_weight_lower': rational(F(81, 82)),
                  'check_count': len(checks), 'passed_count': len(checks)-failed,
                  'failed_count': failed, 'checks': checks, 'rerun_resume': False}
        result['canonical_payload_sha256'] = hashlib.sha256(canonical(result)).hexdigest()
        result_hash = write_json(RESULT, result)
        event('result_completed', result_sha256=result_hash,
              canonical_payload_sha256=result['canonical_payload_sha256'])
        with REPORT.open('x', encoding='utf-8') as stream:
            stream.write(make_report(result))
            stream.flush()
            os.fsync(stream.fileno())
        report_hash = sha(REPORT)
        event('report_completed', report_sha256=report_hash)
        receipt = {'status': result['status'], 'pid': os.getpid(),
                   'check_count': result['check_count'], 'passed_count': result['passed_count'],
                   'failed_count': failed, 'runtime_seconds': result['runtime_seconds'],
                   'source_sha256': source_hash, 'protocol_sha256': protocol_hash,
                   'input_sha256': inputs_after, 'result_sha256': result_hash,
                   'report_sha256': report_hash, 'manifest_sha256': manifest_hash,
                   'moments_sha256': moment_hash,
                   'journal_sha256': sha(CP / 'events.jsonl'),
                   'canonical_payload_sha256': result['canonical_payload_sha256'],
                   'scope': SCOPE, 'rerun_resume': False}
        receipt_hash = write_json(RECEIPT, receipt)
        print(json.dumps({'status': result['status'], 'pid': os.getpid(),
                          'checks': len(checks), 'failed': failed,
                          'runtime_seconds': result['runtime_seconds'],
                          'result_sha256': result_hash, 'receipt_sha256': receipt_hash}))
        return 0 if failed == 0 else 3
    except Exception as exc:
        error = {'status': 'ERROR_PRESERVED', 'utc': now(), 'pid': os.getpid(),
                 'exception': repr(exc), 'traceback': traceback.format_exc(),
                 'checks_completed': checks, 'elapsed_seconds': time.perf_counter()-start,
                 'partial_outputs': {p.name: sha(p) for p in
                                     (RESULT, REPORT, CP/'manifest.json', CP/'moments.json')
                                     if p.is_file()}, 'rerun_resume': False}
        error_hash = write_json(CP / 'error.json', error)
        event('error_preserved', error_sha256=error_hash, exception=repr(exc))
        print(json.dumps({'status': 'ERROR_PRESERVED', 'pid': os.getpid(),
                          'exception': repr(exc), 'error_sha256': error_hash}))
        return 2


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true', help='single root-approved new arithmetic launch')
    args = parser.parse_args()
    if not args.execute:
        parser.error('No calculation without explicit --execute and root preflight/ownership approval')
    sys.exit(run())

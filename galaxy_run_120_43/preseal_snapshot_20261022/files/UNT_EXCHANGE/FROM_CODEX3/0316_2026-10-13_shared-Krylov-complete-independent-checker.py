"""SOURCE ONLY, root executes. Complete independent eight-control saved review.
Analytic two-state powers, direct scalar Taylor polynomials, integer bisection
square roots. Never imports/executes the producer scientific or caller sources.
CLI --archive literal absolute original twenty-file scientific directory.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import json
from math import factorial
from pathlib import Path
import resource
import sys
import time

BASE = Path('/Users/bgm/Research/UNT_EXCHANGE')
LANE = BASE/'lanes/P49_CODEX2'
PINS = {
    'math': {'path': str(LANE/'certified_krylov_reference_v001.py'),
             'sha256': 'adb77d50bae4d1e230b36e5b97cf7b0d5bbc427a02f8a3bbe135b88393fe9e7d'},
    'controls': {'path': str(LANE/'certified_krylov_controls_v001.py'),
                 'sha256': 'f74de621ba3848bc3651dc7da9d227031a9aa95047f7bb2bdc99b80d0f1d518f'},
    'caller': {'path': str(BASE/'KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001/SHARED_KRYLOV_CONTROLS_ROOT_PRODUCER_V001.py'),
               'sha256': '2b501f5830557e293724ecc6bc9c80724bb555ab50e0c0b58925331fa6a243f5'}}
THEORY = LANE/'CERTIFIED_KRYLOV_REFERENCE_PROSPECT_V001.txt'
THEORY_SHA = 'c152a10fe74ed66903fa19523ac4959ee2a6ab920e09cd6d6ec1e0fe6cf19b33'
NAMES = ['full_subspace_polynomial', 'insufficient_subspace_wide_bound',
         'untrusted_decimal_candidate', 'excited_inclusion_not_ground',
         'ground_exact_inertia', 'refuse_nonhermitian', 'refuse_missing_basis_entry',
         'refuse_forged_inertia']
FILES = {'START.json', 'SOURCE_SNAPSHOTS.json', 'RESULTS.json', 'FINISH.json'} | {
    'CALL_%02d_%s.json' % (i, event) for i in range(8) for event in ('PRE', 'RETURN')}
S = 2**80


def need(ok, why):
    if not ok:
        raise ValueError(why)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def raw_file(p, cap):
    need(p.is_absolute() and p.resolve() == p and not p.is_symlink()
         and p.is_file() and p.stat().st_size <= cap, 'bounded plain input '+str(p))
    with p.open('rb') as stream:
        raw = stream.read(cap+1)
    need(len(raw) <= cap, 'actual bytes cap')
    return raw


def pairs(items):
    result = {}
    for k, v in items:
        need(k not in result, 'duplicate JSON key')
        result[k] = v
    return result


def decode(raw):
    def bad(v):
        raise ValueError('nonfinite '+v)
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=bad)


def exact(a, b, label):
    need(type(a) is type(b), 'typed '+label)
    if isinstance(b, dict):
        need(a.keys() == b.keys(), 'complete keys '+label)
        for k in b:
            exact(a[k], b[k], label+'/'+k)
    elif isinstance(b, list):
        need(len(a) == len(b), 'complete length '+label)
        for i in range(len(b)):
            exact(a[i], b[i], label+'/'+str(i))
    else:
        need(a == b, 'exact '+label)


def upward_root(q):
    """Smallest integer r with r^2 >= q*2^256; no producer isqrt algorithm."""
    q = Q(q)
    need(q >= 0, 'nonnegative norm square')
    p, d = q.numerator*2**256, q.denominator
    low, high = 0, 1
    while high*high*d < p:
        high *= 2
    while low < high:
        mid = (low+high)//2
        if mid*mid*d >= p:
            high = mid
        else:
            low = mid+1
    need(low*low*d >= p and (low == 0 or (low-1)**2*d < p), 'outward root minimality')
    return Q(low, 2**128)


def proposal(scope, narrow=False):
    return {'basis_I80': [[[S, 0], [0, 0]]] if narrow else [[[S, 0], [0, 0]], [[0, 0], [S, 0]]],
            'projected_H_I80': [[[0, 0]]] if narrow else [[[0, 0], [S, 0]], [[S, 0], [0, 0]]],
            'initial_coeff_I80': [[S, 0]] if narrow else [[S, 0], [0, 0]],
            'candidate_scope': scope}


def expected_inputs():
    H = [[[1, 1, 0]], [[0, 1, 0]]]
    seed = [[S, 0], [0, 0]]
    full = proposal('MANUFACTURED_EXACT_FULL_BASIS')
    narrow = proposal('MANUFACTURED_INSUFFICIENT_SUBSPACE', True)
    def propagation(p):
        return {'rows': H, 'denominator': 1, 'center': seed, 'input_L2_error': '0',
                'proposal': p, 'tau': '1/8', 'degree': 24}
    d = [[[0, -1, 0]], [[1, 2, 0]]]
    proof = {'permutation': [0, 1], 'unit_lower': [[['1', '0'], ['0', '0']], [['0', '0'], ['1', '0']]],
             'real_diagonal': ['-1', '2']}
    ground = {'rows': d, 'denominator': 1, 'vector_I80': seed,
              'reference_lambda': '-1', 'beta': '0', 'inertia_proof': proof}
    malformed = dict(narrow, basis_I80=[[[S, 0]]])
    return [propagation(full), propagation(narrow),
            {'rows': H, 'denominator': 1, 'center': seed, 'max_columns': 4, 'tau': '1/8', 'degree': 24},
            {'rows': d, 'denominator': 1, 'vector_I80': [[0, 0], [S, 0]], 'reference_lambda': '2'},
            ground,
            dict(propagation(full), rows=[[[1, 1, 0]], [[0, 2, 0]]]),
            propagation(malformed),
            dict(ground, inertia_proof=dict(proof, real_diagonal=['-1', '3']))]


def expected_propagation(narrow):
    # X^k e0 alternates e0/e1. For the one-dimensional zero projection,
    # only k=0 survives and H e0=e1 gives a constant-path defect of norm1.
    degree, tau = 24, Q(1, 8)
    powers = []
    terms = []
    integral = Q(0)
    for k in range(degree+1):
        if narrow:
            powers.append([['1' if k == 0 else '0', '0']])
            norm_squared = Q(int(k == 0))
        else:
            powers.append([['1' if k%2 == 0 else '0', '0'], ['1' if k%2 else '0', '0']])
            norm_squared = Q(int(k == degree))
        factor = tau**(k+1)/factorial(k+1)
        upper = upward_root(norm_squared)
        integral += factor*upper
        terms.append({'power': k, 'complete_defect_norm_squared': str(norm_squared),
                      'norm_upper': str(upper), 'integral_factor': str(factor)})
    if narrow:
        real, imag = Q(1), Q(0)
    else:
        real = sum(((-1)**j*tau**(2*j)/factorial(2*j) for j in range(13)), Q(0))
        imag = -sum(((-1)**j*tau**(2*j+1)/factorial(2*j+1) for j in range(12)), Q(0))
    # Only coordinate0.real and coordinate1.imag are nonzero.
    # Explicit signed numerator quotient independently expresses truncation.
    def trunc(q):
        n, d = q.numerator*S, q.denominator
        return (1 if n >= 0 else -1)*(abs(n)//d)
    a, b = trunc(real), trunc(imag)
    round2 = (real-Q(a, S))**2+(imag-Q(b, S))**2
    rounding = upward_root(round2)
    added = integral+rounding
    need((narrow and integral == tau) or (not narrow and integral == tau**25/factorial(25)),
         'independent analytic integrated defect')
    return {'schema': 'CERTIFIED_KRYLOV_POLYNOMIAL_DEFECT_V001', 'dimension': 2,
            'basis_columns': 1 if narrow else 2, 'degree': degree, 'tau': str(tau),
            'input_L2_error': '0', 'initial_projection_defect_squared': '0',
            'initial_projection_error_upper': '0',
            'all_basis_residual_norm_squared': ['1'] if narrow else ['0', '0'],
            'all_projected_powers': powers, 'all_polynomial_defect_terms': terms,
            'integrated_defect_upper': str(integral), 'endpoint_quantization_norm_squared': str(round2),
            'endpoint_quantization_error_upper': str(rounding), 'step_added_L2_error': str(added),
            'accumulated_L2_error': str(added), 'endpoint_I80': [[a, 0], [0, b]],
            'step_target_2_minus_64_met': added <= Q(1, 2**64),
            'original_cumulative_cap_2_minus_51_met': added < Q(1, 2**51),
            'arithmetic': 'FULL_EXACT_RATIONAL_WITH_INTEGER_OUTWARD_SQRT',
            'orthogonality_or_backend_flags_trusted': False,
            'exact_input_error_and_H_ancestry_authenticated_here': False,
            'native_N2_validation_completed': False, 'physical_release': False}


def expected_spectral(ground):
    # Complete diagonal spectrum {-1,2}; I diag(-1,2) I* is the supplied
    # whole beta0 proof, exactly one negative entry. Excited e1 is not ground.
    mu = '-1' if ground else '2'
    return {'schema': 'CERTIFIED_KRYLOV_SPECTRAL_BOUND_V001', 'Rayleigh_quotient': mu,
            'normalized_variance': '0', 'some_eigenvalue_interval': [mu, mu],
            'reference_residual_squared_over_norm': '0', 'ground_energy_interval': ['-1', mu],
            'ground_bracket_method': ('EXACT_INERTIA_AND_TEMPLE_GROUND_BRACKET' if ground
                                      else 'GERSHGORIN_TO_RAYLEIGH_GROUND_BRACKET'),
            'verified_negative_inertia': 1 if ground else None,
            'ground_halfwidth_1_over_4096_met': ground,
            'small_residual_identifies_ground_by_itself': False,
            'full_sector_authentication_required': True,
            'effective_H_remainder_or_leakage_included': False, 'physical_release': False}


def expected_outcomes():
    full = expected_propagation(False)
    narrow = expected_propagation(True)
    # The manufactured candidate starts with exact e0. First H action is e1;
    # two orthogonalization passes do nothing. Next H action is e0, removed
    # exactly. All decimal operations are0/1/sqrt1; basis has exactly2columns.
    candidate = proposal('UNTRUSTED_DECIMAL80_TWO_PASS_KRYLOV; ONLY_FULL_EXACT_DEFECT_CAN_CERTIFY')
    values = [full, narrow, {'candidate': candidate, 'certificate': full},
              expected_spectral(False), expected_spectral(True)]
    result = [{'exception': None, 'value': v} for v in values]
    for message in ('complete Hermitian H', 'complete I80 vector', 'every exact congruence matrix entry'):
        result.append({'exception': 'ValueError', 'message': message})
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--archive', type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    def guard():
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if sys.platform != 'darwin':
            rss *= 1024
        need(rss <= 256*2**20 and time.monotonic()-started <= 60, 'checker256MiB60s cap')
    root = args.archive
    need(root.is_absolute() and root.resolve() == root and not root.is_symlink()
         and root.is_dir(), 'literal original archive')
    need({p.name for p in root.iterdir()} == FILES, 'whole twenty-file success census')
    sources = {name: raw_file(Path(rec['path']), 32768) for name, rec in PINS.items()}
    for name, rec in PINS.items():
        need(digest(sources[name]) == rec['sha256'], 'source pin '+name)
    theory = raw_file(THEORY, 32768)
    need(digest(theory) == THEORY_SHA, 'theory pin')
    raw = {name: raw_file(root/name, 8*2**20) for name in FILES}
    need(sum(map(len, raw.values())) <= 8*2**20, 'whole scientific reserve')
    decoded = {name: decode(data) for name, data in raw.items()}
    start = decoded['START.json']
    pid = start.get('pid')
    need(type(pid) is int and pid > 0, 'recorded PID syntax only')
    exact(start, {'schema': 'SHARED_KRYLOV_EIGHT_CONTROLS_ROOT_START_V001', 'pid': pid,
          'source_pins': PINS, 'caps': {'cpu': 1, 'rss_bytes': 268435456, 'seconds': 60, 'output_bytes': 16777216},
          'external_supervisor_required': True, 'scientific_acceptance': False}, 'START')
    exact(decoded['SOURCE_SNAPSHOTS.json'], {k: v.decode() for k, v in sources.items()}, 'SNAPSHOTS')
    inputs, outcomes = expected_inputs(), expected_outcomes()
    for i, name in enumerate(NAMES):
        guard()
        exact(decoded['CALL_%02d_PRE.json' % i], {'name': name, 'arguments': inputs[i]}, 'PRE/'+name)
        exact(decoded['CALL_%02d_RETURN.json' % i], {'name': name, 'outcome': outcomes[i]}, 'RETURN/'+name)
        print(json.dumps({'independent_progress': 'COMPLETE_CONTROL', 'index': i, 'name': name}), flush=True)
    flags = {'full_basis_precision': True, 'bad_subspace_wide': True, 'candidate_certified': True,
             'excited_not_ground_precision': True, 'ground_exact': True, 'three_refusals': True}
    need(outcomes[0]['value']['step_target_2_minus_64_met']
         and not outcomes[1]['value']['step_target_2_minus_64_met'], 'independent precision control answers')
    result = {'schema': 'CERTIFIED_KRYLOV_FIXED_EIGHT_CONTROLS_V001',
              'calls': dict(zip(NAMES, outcomes)), 'checks': flags, 'all_controls': True,
              'native_N2_validation': False, 'physical_release': False}
    exact(decoded['RESULTS.json'], result, 'RESULTS')
    inventory = {k: {'bytes': len(v), 'sha256': digest(v)} for k, v in raw.items() if k != 'FINISH.json'}
    exact(decoded['FINISH.json'], {'schema': 'SHARED_KRYLOV_EIGHT_CONTROLS_ROOT_FINISH_V001',
          'pid': pid, 'all16_audit_events_saved': True, 'source_closing_bytes_match': True,
          'files_before_finish': inventory, 'status': 'RAW_CONTROL_RESULTS_PENDING_DISTINCT_SAVED_COMPARISON',
          'native_N2_validation': False, 'physical_release': False}, 'FINISH')
    need({p.name for p in root.iterdir()} == FILES, 'closing twenty files')
    for name, rec in PINS.items():
        need(raw_file(Path(rec['path']), 32768) == sources[name], 'closing source bytes')
    need(raw_file(THEORY, 32768) == theory, 'closing theory bytes')
    for name, data in raw.items():
        need(raw_file(root/name, 8*2**20) == data, 'closing all archive bytes')
    guard()
    print(json.dumps({'schema': 'SHARED_KRYLOV_COMPLETE_INDEPENDENT_SAVED_REVIEW_V001',
          'status': 'PASS_COMPLETE_PAYLOAD_PENDING_ROOT_RUNTIME_CUSTODY', 'archive': str(root),
          'reviewer': 'Codex3', 'source_author': 'Codex2', 'caller_author': 'Codex ROOT', 'self_review': False,
          'all20_files': {k: {'bytes': len(v), 'sha256': digest(v)} for k, v in sorted(raw.items())},
          'all8_complete_pre_return_pairs_exact': True, 'every_polynomial_term_and_endpoint_exact': True,
          'all3_refusal_messages_exact': True, 'candidate_wire_independently_derived': True,
          'shared_math': 'Exact polynomial-defect identity; analytic two-state powers and scalar Taylor sums; independent bisection square roots',
          'original_runtime_verified_by_this_checker': False, 'native_N2_validation': False,
          'native_feasibility_released': False, 'physical_release': False}, sort_keys=True, allow_nan=False), flush=True)


if __name__ == '__main__':
    main()

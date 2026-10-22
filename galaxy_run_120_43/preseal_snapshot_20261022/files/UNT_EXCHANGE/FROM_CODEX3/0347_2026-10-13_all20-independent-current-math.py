"""SOURCE ONLY. Full Hx continuity read, distinct from upper-pair producer.
Root supplies independently reconstructed full native packet and actual
accepted checkpoint objects. No Code2 mathematical module is called.
"""
from fractions import Fraction as Q
from itertools import combinations

WORDS = ('00', '01', '10', '11')
TYPES = ('OLD_CARRIER_SITE0', 'OLD_CARRIER_SITE1', 'OLD_READY_SITE0',
         'OLD_COHERENT_PLUS_I', 'OLD_COHERENT_MINUS_I')
TIMES = (Q(1, 8), Q(1, 4), Q(1, 2), Q(1))
S = 1 << 80


def need(ok, why):
    if not ok:
        raise ValueError(why)


def wire(x):
    if isinstance(x, Q):
        return str(x)
    if isinstance(x, dict):
        return {k: wire(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [wire(v) for v in x]
    return x


def current_table(packet, guard):
    states, h = packet['active_states'], packet['rows']
    need(len(states) == len(h) == 10432, 'whole independently rebuilt active parent')
    occupation = [[((s[2] >> v) & 1)+((s[4] >> v) & 1) for s in states] for v in range(4)]
    need(all(sum(row[i] for row in occupation) == 1 for i in range(10432)), 'exact whole Q1')
    currents = [[[] for _ in states] for _ in range(4)]
    for i, row in enumerate(h):
        for j, a, b in row:
            totals = [0, 0]
            for v in range(4):
                d = occupation[v][j]-occupation[v][i]
                if d:
                    need(states[i][0] == states[j][0] and states[i][3] == states[j][3], 'current preserves q and sector')
                    currents[v][i].append([j, -b*d, a*d])
                    totals[0] -= b*d
                    totals[1] += a*d
            need(totals == [0, 0], 'every entry total-current zero')
        if i % 256 == 0:
            guard()
    for matrix in currents:
        need(max(sum(abs(a)+abs(b) for j, a, b in row) for row in matrix) <= 2240, 'entire exact current norm4')
        # Full directed entries constructed separately, not by mirroring.
        maps = [{j: (a, b) for j, a, b in row} for row in matrix]
        for i, row in enumerate(matrix):
            for j, a, b in row:
                need(maps[j].get(i) == (a, -b), 'independently full Hermitian current')
    return wire({'schema': 'P64_ALL20_NATIVE_CURRENT_TABLE_V001', 'active_dimension': 10432,
          'active_states': states, 'active_to_native': packet['active_to_native'],
          'eta_diagonals': occupation, 'all_four_complete_current_rows_numerator_over_560': currents,
          'current_reference_inverse_benchmark_time': 4, 'dimensionless_comparison_tolerance': Q(1, 64),
          'required_individual_halfwidth': Q(1, 1024),
          'current_definition': 'J_v=i[H,eta_v]; eta_v=p_v+Ready_v',
          'dimensionless_endpoint_read': 'j_v=J_v/4',
          'dimensionless_integrated_read': 'F_v=(eta_v(T)-eta_v(0))/(4T)',
          'physical_motion_release': False})


def preparation(packet, word, kind, checkpoints, guard):
    need(word in WORDS and kind in TYPES and set(checkpoints) == {'0', '1', '2', '3'}, 'complete state/four horizons')
    states, h = packet['active_states'], packet['rows']
    occupancy = [[((s[2] >> v) & 1)+((s[4] >> v) & 1) for s in states] for v in range(4)]
    q = int(word[0])+2*int(word[1])
    a, b, r = (0, 3, 1, q, 0, 1), (0, 3, 2, q, 0, 1), (0, 3, 0, q, 1, 0)
    kets = {TYPES[0]: [(a, 5, 0)], TYPES[1]: [(b, 5, 0)], TYPES[2]: [(r, 5, 0)],
            TYPES[3]: [(a, 3, 0), (b, 0, 4)], TYPES[4]: [(a, 3, 0), (b, 0, -4)]}
    location = {tuple(s): i for i, s in enumerate(states)}
    initial = [sum(Q((x*x+y*y)*occupancy[v][location[s]], 25) for s, x, y in kets[kind]) for v in range(4)]
    need(sum(initial) == 1, 'independently normalized exact initial eta')
    seed = kind if word == '11' else 'Q'+word+'_'+kind
    def bracket(value, error, low, high):
        left, right = max(Q(low), value-error), min(Q(high), value+error)
        need(left <= right and right-left <= Q(1, 512), 'whole read precision')
        return [left, right]
    endpoints = []
    for stage, t in enumerate(TIMES):
        cp = checkpoints[str(stage)]
        need(cp['schema'] == 'P49_STAGE_CHECKPOINT_V001' and cp['seed'] == seed
             and type(cp['stage']) is int and cp['stage'] == stage and Q(cp['time']) == t
             and cp['all_component_weights'] == [1, 0, 0, 0, 0]
             and cp['phase'] == 'exp(-i(H-(2121/80)I)t), hbar=1', 'complete accepted checkpoint identity')
        z, error = cp['center'], Q(cp['L2_error'])
        need(len(z) == 10432 and all(type(pair) is list and len(pair) == 2
             and all(type(x) is int for x in pair) for pair in z)
             and 0 <= error < Q(1, 1 << 51), 'every Gaussian integer and inherited L2 error')
        # Full Hx action independently on every row, including diagonal.
        action = []
        for i, row in enumerate(h):
            real = imag = 0
            for j, a0, b0 in row:
                x, y = z[j]
                real += a0*x-b0*y
                imag += b0*x+a0*y
            action.append((real, imag))
            if i % 256 == 0:
                guard()
        norms = [x*x+y*y for x, y in z]
        imaginary = [x*b0-y*a0 for (x, y), (a0, b0) in zip(z, action)]
        need(sum(imaginary) == 0, 'exact full H expectation reality')
        allowance = 2*error+error*error
        vertices = []
        for v in range(4):
            eta = Q(sum(n*m for n, m in zip(occupancy[v], norms)), S*S)
            # d<eta>/dt = 2 Im<x|eta H|x>; j=J/4, H numerator/560.
            j = Q(sum(n*m for n, m in zip(occupancy[v], imaginary)), 1120*S*S)
            f = (eta-initial[v])/(4*t)
            ferr = allowance/(4*t)
            vertices.append({'vertex': v, 'eta_initial_exact': initial[v],
                'eta_endpoint_center': eta, 'eta_endpoint_interval': bracket(eta, allowance, 0, 1),
                'j_endpoint_center': j, 'j_endpoint_interval': bracket(j, allowance, -1, 1),
                'F_time_average_center': f, 'F_time_average_interval': bracket(f, ferr, -1, 1),
                'endpoint_vector_error_allowance': allowance, 'F_vector_error_allowance': ferr})
        need(sum(v['j_endpoint_center'] for v in vertices) == 0, 'all vertex currents sum exactly0')
        endpoints.append({'stage': stage, 'T': t, 'center_norm_squared': Q(sum(norms), S*S),
                          'L2_error': error, 'vertices': vertices})
    return wire({'schema': 'P64_ALL20_COMPLETE_PREPARATION_CURRENT_V001', 'seed': seed,
        'word': word, 'preparation_type': kind, 'initial_word_only': True, 'fixed_background_claim': False,
        'all_endpoints': endpoints, 'current_reference_inverse_benchmark_time': 4,
        'dimensionless_comparison_tolerance': Q(1, 64), 'required_individual_halfwidth': Q(1, 1024),
        'integrated_identity': 'F=(eta(T)-eta(0))/(4T); exact continuity, no quadrature',
        'readout_arithmetic': 'EXACT_INTEGER_GAUSSIAN_AND_RATIONAL_WITH_CERTIFIED_INPUT_L2_ERROR',
        'center_renormalized': False, 'history_D_M_status': 'NOT_AVAILABLE_REQUIRES_NEW_BRANCH_PROPAGATION',
        'locality': 'NOT_TESTABLE_AT_THIS_RUNG', 'species_universality': 'NOT_TESTABLE',
        'physical_motion_release': False, 'root_complete_archive_authentication_required': True})


def contrast(left, right):
    need(len(left) == len(right) == 4, 'all four vertex intervals')
    components = []
    for v in range(4):
        need(len(left[v]) == len(right[v]) == 2, 'closed read intervals')
        a, b = map(Q, left[v]); c, d = map(Q, right[v])
        need(-1 <= a <= b <= 1 and -1 <= c <= d <= 1
             and b-a <= Q(1, 512) and d-c <= Q(1, 512), 'all individual read precision/ranges')
        lo, hi = c-b, d-a
        # Distance of interval from zero, and its farthest endpoint.
        components.append({'vertex': v, 'right_minus_left_interval': [lo, hi],
                           'absolute_difference_interval': [max(Q(0), lo, -hi), max(-lo, hi)]})
    low = max(c['absolute_difference_interval'][0] for c in components)
    high = max(c['absolute_difference_interval'][1] for c in components)
    decision = ('WITHIN_DECLARED_CURRENT_TOLERANCE' if high <= Q(1, 64)
                else 'RESOLVED_RECORD_CONTENT_DIFFERENCE' if low > Q(1, 64) else 'UNRESOLVED')
    return wire({'components': components, 'max_vertex_absolute_difference_interval': [low, high],
                 'threshold': Q(1, 64), 'decision': decision, 'sign_or_focusing_inferred': False})


def compare(reads, guard):
    need(set(reads) == {w+':'+k for w in WORDS for k in TYPES}, 'all twenty distinctly accepted complete preparation reads')
    def get(word, kind, stage, name):
        return [v[name] for v in reads[word+':'+kind]['all_endpoints'][stage]['vertices']]
    pairs, temporal = [], []
    for stage, t in enumerate(TIMES):
        for kind in TYPES:
            for a, b in combinations(WORDS, 2):
                row = {'stage': stage, 'T': t, 'preparation_type': kind,
                       'left_initial_word': a, 'right_initial_word': b,
                       'left_initial_written_count': a.count('1'), 'right_initial_written_count': b.count('1')}
                for label, field in [('j', 'j_endpoint_interval'), ('F', 'F_time_average_interval')]:
                    row[label] = contrast(get(a, kind, stage, field), get(b, kind, stage, field))
                pairs.append(row)
                guard()
    translation = {'RESOLVED_RECORD_CONTENT_DIFFERENCE': 'RESOLVED_ADJACENT_HORIZON_CHANGE',
                   'WITHIN_DECLARED_CURRENT_TOLERANCE': 'WITHIN_DECLARED_ADJACENT_HORIZON_TOLERANCE',
                   'UNRESOLVED': 'UNRESOLVED'}
    for word in WORDS:
        for kind in TYPES:
            for earlier in range(3):
                row = {'word': word, 'preparation_type': kind,
                       'earlier_T': TIMES[earlier], 'later_T': TIMES[earlier+1]}
                for label, field in [('j', 'j_endpoint_interval'), ('F', 'F_time_average_interval')]:
                    result = contrast(get(word, kind, earlier, field), get(word, kind, earlier+1, field))
                    result['decision'] = translation[result['decision']]
                    row[label] = result
                temporal.append(row)
                guard()
    need(len(pairs) == 120 and len(temporal) == 60, 'complete two pair censuses')
    return wire({'schema': 'P64_ALL20_CURRENT_WORD_PAIR_DECISIONS_V001',
        'dimensionless_comparison_tolerance': Q(1, 64), 'required_individual_halfwidth': Q(1, 1024),
        'all120_same_type_crossword_pairs': pairs, 'all60_adjacent_horizon_pairs': temporal,
        'crossword_decisions_per_read_family': 120, 'adjacent_horizon_decisions_per_read_family': 60,
        'j_and_F_are_separate_instruments': True, 'word_TV_not_substituted_for_current': True,
        'ordered_by_written_count': 'UNDETERMINED_NO_ORDERING_FUNCTIONAL_IN_0322',
        'signed_or_focusing_law': 'NOT_INFERRED_FROM_MAX_NORM',
        'energy_controlled_causality': 'NOT_ESTABLISHED_C157185_UNEQUAL_PAIRS',
        'history_D_M_status': 'NOT_AVAILABLE_REQUIRES_NEW_BRANCH_PROPAGATION',
        'locality': 'NOT_TESTABLE_AT_THIS_RUNG', 'species_universality': 'NOT_TESTABLE',
        'finite_window_only': True, 'stationarity': False, 'physical_motion_release': False})

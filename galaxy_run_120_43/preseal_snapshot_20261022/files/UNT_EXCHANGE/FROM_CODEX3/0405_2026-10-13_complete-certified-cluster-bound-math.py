"""SOURCE ONLY. Complete fixed-partition exact infinite-time outer bounds.
Kernel, exact reference conversion, native H/state census and original grouping
custody are caller obligations. No floating arithmetic, eigenvalue gap fitting,
internal exact-degeneracy assertion or native physical prediction.
"""
from fractions import Fraction as Q
from math import isqrt
WORDS = ('00', '01', '10', '11')
READS = WORDS + ('old_presence', 'born_presence', 'carriers', 'Ready', 'Nq_old', 'Nq_all')
CAPS = (1, 1, 1, 1, 1, 1, 1, 1, 2, 4)
SEEDS = ('OLD_CARRIER_SITE0', 'OLD_CARRIER_SITE1', 'COHERENT_PLUS', 'COHERENT_MINUS', 'OLD_READY_BLANK')


def need(ok, why):
    if not ok:
        raise ValueError(why)


def normroot(integer_square, denominator):
    need(type(integer_square) is int and integer_square >= 0 and
         type(denominator) is int and denominator > 0, 'integer norm domain')
    scaled = integer_square << 256
    lower = isqrt(scaled)
    upper = lower + int(lower*lower < scaled)
    need(lower*lower <= scaled <= upper*upper, 'outward integer square-root inequalities')
    return Q(upper, denominator*(1 << 128))


def complete_reads_and_seeds(states):
    need(type(states) is list and len(states) == 10432, 'full native active basis')
    index = {}
    diagonals = {name: [] for name in READS}
    for i, state in enumerate(states):
        need(type(state) is list and len(state) == 6 and all(type(x) is int for x in state), 'whole exact state')
        t = tuple(state)
        need(t not in index, 'basis uniqueness')
        index[t] = i
        sector, inc, p, q, ready, spent = state
        need(sector in (0, 1) and p >= 0 and q >= 0 and ready in (0, 1), 'native state domain')
        word = str(q & 1)+str((q >> 1) & 1)
        values = tuple(int(word == name) for name in WORDS) + (
            int(sector == 0), int(sector == 1), bin(p).count('1'), ready,
            (q & 1)+((q >> 1) & 1), bin(q).count('1'))
        need(sum(values[:4]) == values[4]+values[5] == values[6]+values[7] == 1, 'full diagonal identities')
        for name, value, cap in zip(READS, values, CAPS):
            need(0 <= value <= cap, 'declared read range')
            diagonals[name].append(value)
    need(tuple(max(diagonals[name]) for name in READS) == CAPS, 'full read maximum census')
    a = index[(0, 3, 1, 3, 0, 1)]
    b = index[(0, 3, 2, 3, 0, 1)]
    r = index[(0, 3, 0, 3, 1, 0)]
    # All amplitudes below have common denominator five.
    seeds = {SEEDS[0]: [[a, 5, 0]], SEEDS[1]: [[b, 5, 0]],
             SEEDS[2]: [[a, 3, 0], [b, 0, 4]],
             SEEDS[3]: [[a, 3, 0], [b, 0, -4]], SEEDS[4]: [[r, 5, 0]]}
    need(all(sum(re*re+im*im for i, re, im in terms) == 25 for terms in seeds.values()), 'exact normalized seeds')
    return diagonals, seeds


def seed_products(w, n, seeds, guard):
    need(len(w) == 2*n*n and tuple(seeds) == SEEDS, 'complete reference and seed ordering')
    output = {}
    for name in SEEDS:
        products, squares = [], []
        for j in range(n):
            re, im = 0, 0
            for i, a, b in seeds[name]:
                u, v = w[2*(j*n+i)], w[2*(j*n+i)+1]
                re += u*a+v*b
                im += u*b-v*a
            products.append([re, im])
            squares.append(re*re+im*im)
            if j % 256 == 0:
                guard()
        output[name] = {'all_column_overlap_numerators': products,
                        'overlap_denominator': 5*(1 << 55),
                        'all_column_squared_mass_numerators': squares,
                        'squared_mass_denominator': 25*(1 << 110)}
    return output


def partitions(original, n):
    value = original['value']
    groups = value['coherent_group_comparators']
    need(len(groups) == 2, 'two original diagnostic partitions')
    # Original tau values are documentary JSON floats. We neither recompute
    # float gaps nor infer eigenvalue multiplicity from the original grouping.
    need(str(groups[0]['tau']) == '1e-10' and str(groups[1]['tau']) == '1e-08', 'frozen original grouping labels')
    sets = {'singleton': value['singleton_basis_diagonal_comparator']['groups_half_open'],
            'original_tau_1e-10': groups[0]['groups_half_open'],
            'original_tau_1e-8': groups[1]['groups_half_open'], 'all_spectrum': [[0, n]]}
    need(sets['singleton'] == [[j, j+1] for j in range(n)], 'complete original singleton partition')
    for name, ranges in sets.items():
        need(type(ranges) is list and ranges, 'nonempty complete partition')
        cursor = 0
        for pair in ranges:
            need(type(pair) is list and len(pair) == 2 and all(type(x) is int for x in pair), 'half-open exact index pair')
            a, b = pair
            need(a == cursor and a < b <= n, 'consecutive exhaustive partition')
            cursor = b
        need(cursor == n, 'no omitted reference column')
    return sets


def extremize(masses, costs, maximum):
    need(len(masses) == len(costs) > 0 and all(0 <= a <= b <= 1 for a, b in masses), 'whole LP domains')
    need(sum(a for a, b in masses) <= 1 <= sum(b for a, b in masses), 'box-simplex feasibility')
    allocation = [a for a, b in masses]
    remaining = 1-sum(allocation)
    # Stable original index tie-break is frozen and retained in full.
    order = sorted(range(len(costs)), key=lambda j: ((-costs[j]) if maximum else costs[j], j))
    for j in order:
        take = min(remaining, masses[j][1]-allocation[j])
        allocation[j] += take
        remaining -= take
    need(remaining == 0 and sum(allocation) == 1, 'complete feasible extremizing allocation')
    return {'value': sum(x*y for x, y in zip(allocation, costs)),
            'allocation': allocation, 'cost_order': order}


def certify(n, lambdas, gram, residual, partition_sets, mass_products,
            diagonals, diagonal_reference, kernel, save, guard):
    """save(name,value) exclusively writes complete exact wire and returns its pin.
    Whole small-cluster matrices are retained by kernel PRE/RETURN. Results here
    reference those records through cluster ranges and deterministic call serials.
    """
    need(n == 10432 and len(lambdas) == n and all(lambdas[j] <= lambdas[j+1] for j in range(n-1)), 'full ordered native references')
    gs, rs = gram['squared_column_numerators'], residual['squared_column_numerators']
    need(len(gs) == len(rs) == n and all(type(x) is int and x >= 0 for x in gs+rs), 'all exact norm columns')
    need(sum(gs) == gram['squared_total_numerator'] and gram['squared_denominator'] == 1 << 220, 'whole Gram sum/scale')
    need(sum(rs) == residual['squared_total_numerator'] and residual['squared_denominator'] == 560**2*(1 << 206), 'whole residual sum/scale')
    delta = normroot(sum(gs), 1 << 110)
    r = normroot(sum(rs), 560*(1 << 103))
    ell = Q(max(abs(x) for x in lambdas), 1 << 48)
    eta = r+(Q(10207, 560)+ell)*delta
    beta = delta*(2+delta)
    norm_pin = save('FULL_NORM_BOUNDS', {'delta': delta, 'residual': r, 'lambda_norm': ell,
        'H_norm': Q(10207, 560), 'eta': eta, 'beta': beta, 'polar_condition': delta < 1,
        'outward_sqrt_fractional_bits': 128})
    cache, outcomes = {}, {}
    valid_intervals = {s: {name: [] for name in READS} for s in SEEDS}
    for partition_name, ranges in partition_sets.items():
        budgets, refused = [], []
        for first, stop in ranges:
            rank = stop-first
            if rank == n:
                budgets.append({'first': first, 'stop': stop, 'exact_projector_identity': True})
                continue
            gap_candidates = []
            if first:
                gap_candidates.append(lambdas[first]-lambdas[first-1])
            if stop < n:
                gap_candidates.append(lambdas[stop]-lambdas[stop-1])
            gap = Q(min(gap_candidates), 1 << 48)
            rg = normroot(sum(rs[first:stop]), 560*(1 << 103))
            etag = rg+(Q(10207, 560)+ell)*delta
            item = {'first': first, 'stop': stop, 'gap': gap, 'residual_group': rg,
                    'eta_group': etag, 'separated': delta < 1 and gap > 2*eta}
            if not item['separated']:
                refused.append([first, stop])
            else:
                item['projector_error'] = min(Q(1), etag/(gap-eta))
                item['mass_error'] = item['projector_error']+beta
            budgets.append(item)
            guard()
        budget_pin = save('PARTITION_'+partition_name+'_BUDGETS', {'partition': ranges, 'groups': budgets,
                           'full_norm_bounds': norm_pin, 'unseparated_groups': refused})
        if refused:
            outcomes[partition_name] = {'status': 'UNCERTIFIED', 'reason': 'polar condition or strict external gap failed',
                                        'budgets': budget_pin, 'all_groups_retained': True}
            continue
        group_records = []
        for budget in budgets:
            first, stop = budget['first'], budget['stop']
            rank, key = stop-first, (first, stop)
            if key not in cache:
                if rank == n:
                    masses = {s: [Q(1), Q(1)] for s in SEEDS}
                    reads = {name: [Q(0), Q(cap)] for name, cap in zip(READS, CAPS)}
                    record = {'first': first, 'stop': stop, 'mode': 'EXACT_IDENTITY_GLOBAL_RANGE',
                              'masses': masses, 'reads': reads, 'compression': {}}
                else:
                    masses, reads, compressed = {}, {}, {}
                    for s in SEEDS:
                        source = mass_products[s]
                        b = Q(sum(source['all_column_squared_mass_numerators'][first:stop]), source['squared_mass_denominator'])
                        masses[s] = [max(Q(0), b-budget['mass_error']), min(Q(1), b+budget['mass_error'])]
                        need(masses[s][0] <= masses[s][1], 'nonempty cluster mass intersection')
                    if rank > 16:
                        reads = {name: [Q(0), Q(cap)] for name, cap in zip(READS, CAPS)}
                    else:
                        identity_ref = {'file': diagonal_reference, 'field': ['identity']}
                        call0 = kernel.serial
                        g = kernel.compression([1]*n, first, rank, 'identity', identity_ref)['complete_gaussian_integer_matrix']
                        trace_g = sum(g[j][j][0] for j in range(rank))
                        need(trace_g > 0, 'nonzero cluster norm under polar condition')
                        for name, cap in zip(READS, CAPS):
                            call = kernel.serial
                            weighted = kernel.compression(diagonals[name], first, rank, name,
                                {'file': diagonal_reference, 'field': ['reads', name]})['complete_gaussian_integer_matrix']
                            c = Q(sum(weighted[j][j][0] for j in range(rank)), trace_g)
                            need(0 <= c <= cap, 'read center in exact global range')
                            squares = 0
                            for j in range(rank):
                                for k in range(rank):
                                    for z in (0, 1):
                                        val = c.denominator*weighted[j][k][z]-c.numerator*g[j][k][z]
                                        squares += val*val
                            knorm = normroot(squares, c.denominator*(1 << 110))
                            radius = knorm+max(c, cap-c)*(beta+2*budget['projector_error'])
                            reads[name] = [max(Q(0), c-radius), min(Q(cap), c+radius)]
                            compressed[name] = {'kernel_call': call, 'gram_kernel_call': call0,
                                'center': c, 'centered_square_numerator': squares,
                                'centered_entry_denominator': c.denominator*(1 << 110),
                                'compressed_norm_upper': knorm, 'radius': radius}
                    record = {'first': first, 'stop': stop,
                              'mode': 'COMPLETE_COMPRESSION' if rank <= 16 else 'GLOBAL_RANGE_RANK_OVER_16',
                              'masses': masses, 'reads': reads, 'compression': compressed, 'budget': budget}
                pin = save('GROUP_%05d_%05d' % key, record)
                cache[key] = (record, pin)
            group_records.append(cache[key])
            guard()
        result = {}
        for s in SEEDS:
            result[s] = {}
            for name in READS:
                masses = [item['masses'][s] for item, pin in group_records]
                lower = extremize(masses, [item['reads'][name][0] for item, pin in group_records], False)
                upper = extremize(masses, [item['reads'][name][1] for item, pin in group_records], True)
                interval = [lower['value'], upper['value']]
                need(interval[0] <= interval[1], 'ordered certified read interval')
                lp_pin = save('LP_'+partition_name+'_'+s+'_'+name,
                              {'group_references': [pin for item, pin in group_records],
                               'lower': lower, 'upper': upper, 'seed': s, 'read': name,
                               'interval': interval, 'budgets': budget_pin})
                result[s][name] = {'interval': interval, 'extremizing_witnesses': lp_pin}
                valid_intervals[s][name].append(interval)
                guard()
        outcomes[partition_name] = {'status': 'CERTIFIED_OUTER_BOUND', 'budgets': budget_pin, 'reads': result}
    final = {}
    for s in SEEDS:
        final[s] = {}
        for name in READS:
            intervals = valid_intervals[s][name]
            need(intervals, 'at least all-spectrum global bound')
            lo, hi = max(x[0] for x in intervals), min(x[1] for x in intervals)
            need(lo <= hi, 'nonempty intersection of same-target certified bounds')
            final[s][name] = [lo, hi]
    target = all(final[s][name][1]-final[s][name][0] <= Q(1, 512) for s in SEEDS for name in WORDS)
    return {'schema': 'COMPLETE_EXACT_INFINITE_TIME_OUTER_BOUNDS_V001',
            'status': 'WORD_HALFWIDTH_CERTIFIED' if target else 'CERTIFICATE_INCONCLUSIVE',
            'full_norm_bounds': norm_pin, 'partitions': outcomes, 'intersections': final,
            'all_five_seeds_all_ten_reads': True, 'word_halfwidth_target': Q(1, 1024),
            'exact_internal_degeneracy_claimed': False, 'finite_Q1_benchmark_only': True,
            'physical_state_or_S1_prediction': False, 'distinct_whole_comparison_required': True}

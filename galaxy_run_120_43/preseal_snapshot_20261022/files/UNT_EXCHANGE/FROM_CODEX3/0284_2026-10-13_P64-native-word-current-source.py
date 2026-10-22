"""SOURCE ONLY. Prospective P64 exact word census and accepted-endpoint reads.

No file access, solver, root release, historical acceptance or caller launch.
Root must authenticate full packet/archives under prospect0283 first. A new
distinct reviewer and complete saved checker are required before invocation.
"""
from fractions import Fraction as F

SCALE = 1 << 80
DENOMINATOR = 560
SHIFT_NUMERATOR = 14847
CURRENT_REFERENCE = 4
TIMES = (F(1, 8), F(1, 4), F(1, 2), F(1))
TYPES = ('OLD_CARRIER_SITE0', 'OLD_CARRIER_SITE1', 'OLD_READY_SITE0',
         'OLD_COHERENT_PLUS_I', 'OLD_COHERENT_MINUS_I')
WORDS = ('00', '01', '10', '11')


def require(ok, why):
    if not ok:
        raise ValueError(why)


def pop(value):
    return bin(value).count('1')


def wire(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): wire(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [wire(v) for v in value]
    return value


def exact_kets():
    """Integer Gaussian numerators over FIVE, including basis amplitudes5/5."""
    family = {}
    for word in WORDS:
        q = int(word[0]) + 2 * int(word[1])
        a = (0, 3, 1, q, 0, 1)
        b = (0, 3, 2, q, 0, 1)
        ready = (0, 3, 0, q, 1, 0)
        entries = [[(a, 5, 0)], [(b, 5, 0)], [(ready, 5, 0)],
                   [(a, 3, 0), (b, 0, 4)], [(a, 3, 0), (b, 0, -4)]]
        for name, ket in zip(TYPES, entries):
            family[word + ':' + name] = ket
    return family


def validate_packet(packet, guard):
    """Checks supplied binding structurally; does NOT authenticate its origin.
    Full coefficient-source/native census authentication is an external gate.
    """
    states = [tuple(s) for s in packet['full_states']]
    require(len(states) == 20672 and len(set(states)) == 20672, 'full native census')
    index = {s: i for i, s in enumerate(states)}
    for state in states:
        require(len(state) == 6 and all(type(x) is int and x >= 0 for x in state), 'six registers')
        sector, incidence, carrier, q, ready, spent = state
        require(sector in (0, 1), 'old/Born sector')
        vertices, edges = ((2, 4), (4, 8))[sector]
        require(incidence < 1 << edges and all(x < 1 << vertices for x in (carrier, q, ready, spent)), 'literal register widths')
        require(ready & spent == 0 and ready | spent == 1, 'every Av active only site0')
        require(pop(carrier) + pop(ready) == 1, 'sharp Q1')
    groups = packet['components']
    require(sorted(map(len, groups)) == [2048, 2048, 3072, 3072, 10432], 'all five components')
    owner = {}
    for label, group in enumerate(groups):
        for i in group:
            require(type(i) is int and 0 <= i < len(states) and i not in owner, 'full component partition')
            owner[i] = label
    require(len(owner) == len(states), 'no missing component states')
    active = packet['active_to_native']
    require(len(active) == 10432 and active == sorted(active) and len(set(active)) == len(active), 'full ordered active component')
    label = owner[index[(0, 3, 1, 3, 0, 1)]]
    require(active == sorted(groups[label]), 'active component identity')
    require(all(owner[i] == label for i, s in enumerate(states) if s[0] == 0), 'every old state belongs to active component')
    active_states = [states[i] for i in active]
    require(active_states == [tuple(s) for s in packet['active_states']], 'full active state map')
    require(packet['coefficient_denominator'] == 560 and F(packet['shift']) == F(2121, 80), 'original exact coefficient/reference')
    require(packet['exact_all_component_invariance'] is True, 'upstream full invariance statement')
    rows = []
    for row in packet['rows']:
        result = {}
        for j, real, imag in row:
            require(all(type(x) is int for x in (j, real, imag)), 'integer Gaussian row')
            require(0 <= j < len(active) and j not in result and (real or imag), 'unique nonzero native row')
            result[j] = (real, imag)
        rows.append(result)
    require(len(rows) == len(active), 'all active rows')
    for i, row in enumerate(rows):
        for j, (a, b) in row.items():
            require(rows[j].get(i) == (a, -b), 'all Hermitian mates')
        if i % 256 == 0:
            guard()
    bound = F(max(sum(abs(a) + abs(b) for a, b in row.values()) for row in rows), 560)
    require(bound == F(10207, 560) == F(packet['shifted_row_norm']), 'original shifted row bound')
    return states, index, owner, active, active_states, rows


def census(packet, guard=lambda: None):
    states, index, owner, active, active_states, rows = validate_packet(packet, guard)
    local = {j: i for i, j in enumerate(active)}
    preparations = {}
    for name, ket in exact_kets().items():
        entries = []
        vector = {}
        weights = [F(0) for group in packet['components']]
        for state, re, im in ket:
            require(state in index and index[state] in local, 'new word exact native support')
            require(state[0] == 0 and state[1] == 3, 'literal initial incidence/old support')
            global_index = index[state]
            i = local[global_index]
            vector[i] = (re, im)
            weight = F(re * re + im * im, 25)
            weights[owner[global_index]] += weight
            entries.append({'native_index': global_index, 'active_index': i,
                            'state': list(state), 'amplitude': [F(re, 5), F(im, 5)]})
        require(sum(weights) == 1, 'exact normalized new preparation')
        acted = []
        for i, row in enumerate(rows):
            xr = xi = 0
            for j, (a, b) in row.items():
                if j in vector:
                    r, s = vector[j]
                    xr += a * r - b * s
                    xi += a * s + b * r
            r, s = vector.get(i, (0, 0))
            acted.append((xr + SHIFT_NUMERATOR * r, xi + SHIFT_NUMERATOR * s))
            if i % 256 == 0:
                guard()
        er = ei = 0
        for i, (r, s) in vector.items():
            a, b = acted[i]
            er += r * a + s * b
            ei += r * b - s * a
        require(ei == 0, 'real exact energy')
        mean = F(er, 25 * 560)
        second = F(sum(a * a + b * b for a, b in acted), 25 * 560 * 560)
        variance = second - mean * mean
        require(variance >= 0, 'nonnegative exact variance')
        preparations[name] = {'entries': entries, 'initial_old_q_word': name[:2],
            'sharp_Q': 1, 'active_mask': 1, 'old_sector_weight': F(1),
            'all_component_weights': weights, 'exact_norm_squared': F(1),
            'mean_absolute_energy': mean, 'second_absolute_energy_moment': second,
            'energy_variance': variance,
            'full_energy_measure_definition': 'Spectral measure of SAME authenticated full H and this exact ket',
            'full_spectral_projectors_computed': False, 'physical_S1_admissibility': 'NOT_ESTABLISHED',
            'energy_conserving_writer_admissibility': 'NOT_ESTABLISHED'}
    pairs = []
    names = list(preparations)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            fields = ('mean_absolute_energy', 'second_absolute_energy_moment')
            unequal = [k for k in fields if preparations[a][k] != preparations[b][k]]
            pairs.append({'a': a, 'b': b, 'witness_moments': unequal,
                          'full_measure_equality': 'UNEQUAL_PROVED' if unequal else 'NOT_ESTABLISHED'})
    return wire({'schema': 'P64_NATIVE_INITIAL_WORD_CENSUS_V001', 'preparations': preparations,
        'all_190_energy_pairs': pairs, 'original_q11_names': ['11:' + n for n in TYPES],
        'existing_seed_authorizations_extended': False, 'new_trajectories_executed': False,
        'source_owner': 'Original accepted coefficientwise native Q1/A1 parent; root must authenticate full bytes',
        'physical_motion_release': False})


def current_rows(active_states, rows):
    eta = [[((s[2] >> v) & 1) + ((s[4] >> v) & 1) for s in active_states]
           for v in range(4)]
    require(all(sum(eta[v][i] for v in range(4)) == 1 for i in range(len(rows))), 'complete Q1 eta sum')
    currents = []
    for v in range(4):
        full = []
        for i, row in enumerate(rows):
            values = {}
            for j, (a, b) in row.items():
                delta = eta[v][j] - eta[v][i]
                if delta:
                    values[j] = (-b * delta, a * delta)
            full.append(values)
        for i, row in enumerate(full):
            for j, (a, b) in row.items():
                require(full[j].get(i) == (a, -b), 'complete current Hermiticity')
                require(active_states[i][3] == active_states[j][3], 'current commutes all q reads')
                require(active_states[i][0] == active_states[j][0], 'actual join current vanishes')
        bound = F(max(sum(abs(a) + abs(b) for a, b in row.values()) for row in full), 560)
        require(bound <= CURRENT_REFERENCE, 'frozen current reference covers all rows')
        currents.append(full)
    for i, row in enumerate(rows):
        for j in row:
            require(sum(currents[v][i].get(j, (0, 0))[0] for v in range(4)) == 0
                    and sum(currents[v][i].get(j, (0, 0))[1] for v in range(4)) == 0,
                    'exact complete current conservation')
    return eta, currents


def quadratic(rows, center, guard):
    real = imag = 0
    for i, row in enumerate(rows):
        r, s = center[i]
        for j, (a, b) in row.items():
            x, y = center[j]
            u, v = a * x - b * y, a * y + b * x
            real += r * u + s * v
            imag += r * v - s * u
        if i % 256 == 0:
            guard()
    require(imag == 0, 'exact Hermitian quadratic form')
    return F(real, 560 * SCALE * SCALE * CURRENT_REFERENCE)


def enclose(center, error, lower, upper):
    interval = [max(F(lower), center - error), min(F(upper), center + error)]
    require(interval[0] <= interval[1], 'certified interval nonempty')
    require((interval[1] - interval[0]) / 2 <= F(1, 1024), 'frozen read precision')
    return interval


def baseline(packet, seed, checkpoints, guard=lambda: None):
    require(seed in TYPES, 'original q11 seed only; new words need new gate')
    require(set(checkpoints) == {'0', '1', '2', '3'}, 'all frozen endpoints')
    states, index, owner, active, ss, rows = validate_packet(packet, guard)
    eta, currents = current_rows(ss, rows)
    ket = exact_kets()['11:' + seed]
    initial_eta = [sum(F((r*r + s*s) * (((state[2] >> v) & 1) + ((state[4] >> v) & 1)), 25)
                       for state, r, s in ket) for v in range(4)]
    results = []
    for stage, T in enumerate(TIMES):
        checkpoint = checkpoints[str(stage)]
        require(checkpoint['seed'] == seed and checkpoint['stage'] == stage
                and F(checkpoint['time']) == T, 'exact seed/stage/time checkpoint')
        require(checkpoint['phase'] == 'exp(-i(H-(2121/80)I)t), hbar=1', 'same global phase convention')
        require(checkpoint['all_component_weights'] == [1, 0, 0, 0, 0], 'original seed component weights')
        center = checkpoint['center']
        require(len(center) == len(ss) and all(len(z) == 2 and all(type(x) is int for x in z) for z in center), 'complete integer center')
        error = F(checkpoint['L2_error'])
        require(0 <= error < F(1, 1 << 51), 'original cumulative L2 cap')
        delta = 2 * error + error * error
        vertices = []
        for v in range(4):
            a = F(sum(weight * (r*r + s*s) for weight, (r, s) in zip(eta[v], center)), SCALE*SCALE)
            eta_interval = enclose(a, delta, 0, 1)
            current = quadratic(currents[v], center, guard)
            current_interval = enclose(current, delta, -1, 1)
            integrated = (a - initial_eta[v]) / (CURRENT_REFERENCE * T)
            integrated_error = delta / (CURRENT_REFERENCE * T)
            integrated_interval = enclose(integrated, integrated_error, -1, 1)
            vertices.append({'vertex': v, 'eta_initial_exact': initial_eta[v],
                'eta_endpoint_center': a, 'eta_endpoint_interval': eta_interval,
                'j_endpoint_center': current, 'j_endpoint_interval': current_interval,
                'F_time_average_center': integrated, 'F_time_average_interval': integrated_interval,
                'endpoint_vector_error_allowance': delta,
                'F_vector_error_allowance': integrated_error})
        results.append({'stage': stage, 'T': T, 'center_norm_squared':
                        F(sum(r*r+s*s for r, s in center), SCALE*SCALE),
                        'L2_error': error, 'vertices': vertices})
    row_records = [[[[j, a, b] for j, (a, b) in sorted(row.items())]
                    for row in current] for current in currents]
    return wire({'schema': 'P64_ACCEPTED_Q11_BASELINE_CURRENT_V001', 'seed': seed,
        'initial_word_only': '11', 'fixed_background_claim': False,
        'current_reference_inverse_benchmark_time': CURRENT_REFERENCE,
        'dimensionless_comparison_tolerance': F(1, 64), 'required_individual_halfwidth': F(1, 1024),
        'all_four_complete_current_rows_numerator_over_560': row_records,
        'all_endpoints': results,
        'integrated_identity': 'F=(eta(T)-eta(0))/(4T); exact continuity, no quadrature',
        'readout_arithmetic': 'EXACT_INTEGER_GAUSSIAN_AND_RATIONAL_WITH_CERTIFIED_INPUT_L2_ERROR',
        'history_D_M_status': 'NOT_AVAILABLE_REQUIRES_NEW_BRANCH_PROPAGATION',
        'locality': 'NOT_TESTABLE_AT_THIS_RUNG', 'species_universality': 'NOT_TESTABLE',
        'physical_motion_release': False, 'root_complete_archive_authentication_required': True})

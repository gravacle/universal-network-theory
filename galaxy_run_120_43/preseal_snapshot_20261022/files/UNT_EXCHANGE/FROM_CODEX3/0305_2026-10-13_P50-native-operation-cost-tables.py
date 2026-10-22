"""SOURCE ONLY. Full-target instantaneous cost comparators; prospect0302.
Root injects distinctly reviewed pinned P64 math module0284 only to validate
the original native packet. No file I/O, backend, propagation or author call.
"""
from fractions import Fraction as F


def need(ok, why):
    if not ok:
        raise ValueError(why)


def pop(value):
    return bin(value).count('1')


def checked(state):
    need(len(state) == 6 and all(type(x) is int and x >= 0 for x in state), 'six exact registers')
    sector, inc, p, q, r, s = state
    need(sector in (0, 1), 'complete old/Born sector')
    nv, ne = ((2, 4), (4, 8))[sector]
    need(inc < 1 << ne and all(x < 1 << nv for x in (p, q, r, s)), 'full target register width')
    need(r & s == 0, 'orthogonal target cell register')
    return tuple(state)


def cost_numerators(state):
    sector, inc, p, q, r, s = checked(state)
    if sector == 0:
        degree = [pop(inc), pop(inc)]
    else:
        degree = [sum((inc >> k) & 1 for k in (0, 2, 4, 6)),
                  sum((inc >> k) & 1 for k in (1, 3, 5, 7))]
    return [(7-degree[v])*(1-2*((q >> v) & 1)) for v in (0, 1)]


def unitary_registry():
    entries = [{'name': 'identity', 'kind': 'identity'}]
    entries += [{'name': 'carrier_flip_v%d' % v, 'kind': 'carrier_flip', 'site': v} for v in (0, 1)]
    entries += [{'name': 'cell_RS_swap_v0', 'kind': 'cell_swap', 'site': 0},
                {'name': 'admission_swap_v0', 'kind': 'admission_swap', 'site': 0}]
    entries += [{'name': 'record_flip_v%d' % v, 'kind': 'record_flip', 'site': v} for v in (0, 1)]
    entries += [{'name': 'old_edge_flip_e%d' % e, 'kind': 'incidence_flip', 'sector': 0, 'edge': e} for e in range(4)]
    entries += [{'name': 'born_edge_flip_e%d' % e, 'kind': 'incidence_flip', 'sector': 1, 'edge': e} for e in range(8)]
    entries += [{'name': 'old_parallel_swap_e0_e1', 'kind': 'incidence_swap', 'sector': 0, 'edges': [0, 1]},
                {'name': 'born_parallel_swap_e0_e2', 'kind': 'incidence_swap', 'sector': 1, 'edges': [0, 2]},
                {'name': 'born_parallel_swap_e1_e3', 'kind': 'incidence_swap', 'sector': 1, 'edges': [1, 3]}]
    entries += [{'name': 'carrier_phase_v%d' % v, 'kind': 'carrier_phase', 'site': v} for v in (0, 1)]
    need(len(entries) == 24, 'all frozen unitaries')
    return entries


def apply_unitary(state, operation):
    state = checked(state)
    sector, inc, p, q, r, s = state
    kind = operation['kind']
    phase = 1
    if kind == 'identity':
        pass
    elif kind == 'carrier_flip':
        p ^= 1 << operation['site']
    elif kind == 'carrier_phase':
        phase = 1-2*((p >> operation['site']) & 1)
    elif kind == 'record_flip':
        q ^= 1 << operation['site']
    elif kind == 'cell_swap':
        bit = 1 << operation['site']
        if (r | s) & bit:
            r ^= bit
            s ^= bit
    elif kind == 'admission_swap':
        bit = 1 << operation['site']
        if ((r & bit) and not (p & bit)) or ((s & bit) and (p & bit)):
            p ^= bit
            r ^= bit
            s ^= bit
    elif kind == 'incidence_flip':
        if sector == operation['sector']:
            inc ^= 1 << operation['edge']
    elif kind == 'incidence_swap':
        if sector == operation['sector']:
            a, b = operation['edges']
            if ((inc >> a) & 1) != ((inc >> b) & 1):
                inc ^= (1 << a) | (1 << b)
    else:
        raise ValueError('unknown frozen unitary')
    return checked((sector, inc, p, q, r, s)), phase


def bias_norm(operation, probe):
    if operation['kind'] == 'record_flip':
        return F(1) if operation['site'] == probe else F(0)
    if operation['kind'] == 'incidence_flip':
        touches = operation['sector'] == 0 or operation['edge'] % 2 == probe
        return F(1, 14) if touches else F(0)
    return F(0)


def expected_bias_numerator(state, operation, probe):
    c = cost_numerators(state)[probe]
    if operation['kind'] == 'record_flip' and operation['site'] == probe:
        return -2*c
    if operation['kind'] == 'incidence_flip' and state[0] == operation['sector']:
        if state[0] == 0 or operation['edge'] % 2 == probe:
            return -(1-2*((state[1] >> operation['edge']) & 1))*(1-2*((state[3] >> probe) & 1))
    return 0


def partial_registry():
    return [{'name': 'Birth_partial', 'kind': 'Birth'},
            {'name': 'carrier_creation_v0', 'kind': 'carrier_creation', 'site': 0},
            {'name': 'carrier_creation_v1', 'kind': 'carrier_creation', 'site': 1}]


def apply_partial(state, operation):
    sector, inc, p, q, r, s = checked(state)
    if operation['kind'] == 'Birth':
        if sector != 0 or pop(inc) != 2:
            return None
        lifted = sum(3 << (2*k) for k in range(4) if (inc >> k) & 1)
        return checked((1, lifted, p, q, r, s))
    need(operation['kind'] == 'carrier_creation', 'fixed partial operation')
    bit = 1 << operation['site']
    if p & bit:
        return None
    return checked((sector, inc, p | bit, q, r, s))


def prepare(M, packet, guard=lambda: None):
    states, index, owner, active, active_states, rows = M.validate_packet(packet, guard)
    local = {j: i for i, j in enumerate(active)}
    base = [cost_numerators(s) for s in states]
    reads = {}
    def add_read(name, full_weights, norm, kind, lower=None, upper=None):
        need(len(full_weights) == len(states), 'complete full-sector read table')
        need(all(type(w) is int and abs(F(w, 14)) <= norm for w in full_weights), 'proved full read norm covers every input')
        weights = [full_weights[i] for i in active]
        maximum = 0
        for i, row in enumerate(rows):
            amount = sum((abs(a)+abs(b))*abs(weights[j]-weights[i]) for j, (a, b) in row.items())
            maximum = max(maximum, amount)
            if i % 256 == 0:
                guard()
        reads[name] = {'weights_numerator_over_14': weights,
                       'operator_norm_upper': norm, 'kind': kind,
                       'global_range': [-norm if lower is None else lower, norm if upper is None else upper],
                       'commutator_norm_upper': F(maximum, 560*14),
                       'exact_operator_null': norm == 0}
    for v in (0, 1):
        add_read('baseline_cost_v%d' % v, [c[v] for c in base], F(1, 2), 'ABSOLUTE_COST_OVER_EBIAS')
    unitary_results = []
    for operation in unitary_registry():
        images = []
        seen = set()
        target_costs = []
        Q_counts = {}
        A_counts = {}
        inside_full = inside_active = 0
        for i, state in enumerate(states):
            target, phase = apply_unitary(state, operation)
            back, back_phase = apply_unitary(target, operation)
            need(back == state and phase*back_phase == 1 and target not in seen, 'full-target involution and injection')
            seen.add(target)
            target_index = index.get(target)
            active_index = local.get(target_index)
            inside_full += target_index is not None
            inside_active += active_index is not None
            C = cost_numerators(target)
            target_costs.append(C)
            Q = pop(target[2])+pop(target[4])
            A = target[4] | target[5]
            Q_counts[str(Q)] = Q_counts.get(str(Q), 0)+1
            A_counts[str(A)] = A_counts.get(str(A), 0)+1
            images.append(list(target)+[phase, target_index, active_index, C[0], C[1]])
            for v in (0, 1):
                need(C[v]-base[i][v] == expected_bias_numerator(state, operation, v), 'full-domain C140 identity')
            if i % 256 == 0:
                guard()
        for v in (0, 1):
            add_read(operation['name']+':after_cost_v%d' % v, [c[v] for c in target_costs], F(1, 2), 'UNITARY_ABSOLUTE_TARGET_COST')
            add_read(operation['name']+':bias_v%d' % v,
                     [c[v]-b[v] for c, b in zip(target_costs, base)], bias_norm(operation, v), 'UNITARY_SIGNED_COST_BIAS')
        unitary_results.append({'operation': operation, 'full_image_rows': images,
             'image_columns': ['sector', 'incidence', 'carrier', 'q', 'ready', 'spent', 'phase', 'original_full_index_or_null', 'active_index_or_null', 'C0_numerator_over8', 'C1_numerator_over8'],
             'target_Q_census': Q_counts, 'target_Av_mask_census': A_counts,
             'targets_inside_original_20672': inside_full, 'targets_inside_active10432': inside_active,
             'full_target_cost_evaluated': True, 'target_full_H_energy_computed': False,
             'outgoing_targets_projected_back': False, 'qualified_writer': False})
    partial_results = []
    for operation in partial_registry():
        images = []
        seen = set()
        success = []
        after = []
        for i, state in enumerate(states):
            target = apply_partial(state, operation)
            exists = target is not None
            success.append(int(exists))
            C = cost_numerators(target) if exists else [0, 0]
            after.append(C)
            if exists:
                need(target not in seen and C == base[i], 'partial isometry injection and eligible pullback identity')
                seen.add(target)
                target_index = index.get(target)
                images.append(list(target)+[target_index, local.get(target_index), C[0], C[1]])
            else:
                images.append(None)
            if i % 256 == 0:
                guard()
        add_read(operation['name']+':success', [14*s for s in success], F(1), 'PARTIAL_SUCCESS_PROBABILITY', F(0), F(1))
        for v in (0, 1):
            before = [s*c[v] for s, c in zip(success, base)]
            target = [c[v] for c in after]
            raw = [c[v]-b[v] for c, b in zip(after, base)]
            event = [a-b for a, b in zip(target, before)]
            add_read(operation['name']+':event_before_v%d' % v, before, F(1, 2), 'UNNORMALIZED_EVENT_COST')
            add_read(operation['name']+':event_after_v%d' % v, target, F(1, 2), 'UNNORMALIZED_EVENT_COST')
            add_read(operation['name']+':raw_functional_v%d' % v, raw, F(1, 2), 'NONUNITARY_RAW_FUNCTIONAL_NOT_NORMALIZED_BIAS')
            add_read(operation['name']+':event_difference_v%d' % v, event, F(0), 'EXACT_ELIGIBLE_PULLBACK_NULL')
        partial_results.append({'operation': operation, 'full_success_image_rows': images,
            'image_columns': ['sector', 'incidence', 'carrier', 'q', 'ready', 'spent', 'original_full_index_or_null', 'active_index_or_null', 'C0_numerator_over8', 'C1_numerator_over8'],
            'success_domain_size': sum(success), 'normalized_postselected_cost_computed': False,
            'partial_not_unitary': True, 'qualified_writer': False})
    need(len(reads) == 125, 'all declared absolute/unitary/partial reads')
    return M.wire({'schema': 'P50_NATIVE_COMPLETE_OPERATION_COST_TABLES_V001',
        'full_input_dimension': 20672, 'active_dimension': 10432,
        'active_to_native': active, 'native_input_authentication': 'EXTERNAL_ROOT_COMPLETE_ORIGINAL_GATE_REQUIRED',
        'unitary_operations': unitary_results, 'partial_operations': partial_results, 'reads': reads,
        'E_bias': F(7, 4), 'signed_bias_threshold': F(1, 128), 'required_halfwidth': F(1, 4096),
        'full_target_cost_formula': 'C_v=(7-d_v)*(1-2q_v)/8 on entire unrestricted old/Born parent',
        'new_propagation': False, 'physical_mass_claim': False,
        'cross_sector_H_energies_available': False,
        'normalization_debt': 'H+alphaQ leaves probe costs unchanged but shifts cross-sector addition energy',
        'unprovided_candidates': ['dressed carrier/cloud operator', 'general loop writer', 'qualified physical species']})

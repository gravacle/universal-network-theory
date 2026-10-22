"""SOURCE ONLY. Root-only invocation after distinct review.

Primary count: trace of a periodic row matching transfer, at most 32 states.
Telemetry audit: binary-order inclusion/exclusion, grouping by inverse Gray
prefix. No producer import, Gray walk, or mutable nonzero product is reused.
"""
from fractions import Fraction
from itertools import product
import hashlib
import json


def require(ok, why):
    if not ok:
        raise ValueError(why)


def transfer_count(L):
    require(type(L) is int and L in (2, 4, 5), 'fixed complete sizes')
    width = 1 << L
    full = width - 1
    matrix = [[0] * width for _ in range(width)]
    # Each A(x,y) chooses B(x,y), B(x,y+1), or B(x+1,y).
    # Internal destinations must be distinct. Their complement is exactly the
    # incoming occupied boundary; outward choices form the outgoing boundary.
    for choice in product((0, 1, 2), repeat=L):
        internal = outgoing = 0
        valid = True
        for y, option in enumerate(choice):
            if option == 2:
                outgoing |= 1 << y
            else:
                target = 1 << ((y + option) % L)
                if internal & target:
                    valid = False
                    break
                internal |= target
        if valid:
            matrix[full ^ internal][outgoing] += 1
    # Trace(T^L): fix the boundary before row zero, propagate all L rows,
    # and close to that same boundary. Every labelled matching appears once.
    total = 0
    for initial in range(width):
        state = [0] * width
        state[initial] = 1
        for unused in range(L):
            following = [0] * width
            for incoming, multiplicity in enumerate(state):
                if multiplicity:
                    for outgoing, ways in enumerate(matrix[incoming]):
                        if ways:
                            following[outgoing] += multiplicity * ways
            state = following
        total += state[initial]
    return total, matrix


def inverse_gray(value):
    answer = 0
    while value:
        answer ^= value
        value >>= 1
    return answer


def complete_layer(L, progress):
    n = L * L
    rows = []
    for row in range(n):
        x, y = divmod(row, L)
        rows.append([row, ((x + 1) % L) * L + y, x * L + (y + 1) % L])
    columns = [[] for unused in range(n)]
    for r, neighbors in enumerate(rows):
        for c in neighbors:
            columns[c].append(r)
    term_count = 1 << n
    block_size = 1 << 18
    block_count = (term_count + block_size - 1) // block_size
    contributions = [0] * block_count
    values = [0] * n
    histogram = [n, 0, 0, 0]
    powers2 = [1 << k for k in range(n + 1)]
    powers3 = [3 ** k for k in range(n + 1)]
    cardinality = 0
    # Binary order is deliberately distinct from producer Gray order. A binary
    # carry removes trailing selected columns and adds the next column. The
    # histogram gives the entire product; no exact-divide product recurrence.
    for mask in range(1, term_count):
        changed = mask ^ (mask - 1)
        column = 0
        while changed:
            delta = 1 if mask & (1 << column) else -1
            cardinality += delta
            for row in columns[column]:
                old = values[row]
                new = old + delta
                histogram[old] -= 1
                histogram[new] += 1
                values[row] = new
            changed >>= 1
            column += 1
        if histogram[0] == 0:
            term = powers2[histogram[2]] * powers3[histogram[3]]
            if (n - cardinality) % 2:
                term = -term
            # Inverting Gray commutes with removing low bits: each fixed high
            # Gray prefix corresponds to one complete 2^18-index block.
            contributions[inverse_gray(mask >> 18)] += term
        if mask % block_size == 0 or mask == term_count - 1:
            progress('BINARY_SUBSET_AUDIT', mask, term_count - 1)
    matching, matrix = transfer_count(L)
    require(sum(contributions) == matching, 'independent transfer versus full subset identity')
    blocks = []
    accumulator = 0
    digest = hashlib.sha256()
    for block, contribution in enumerate(contributions):
        accumulator += contribution
        # Producer emits after index 2^18, rather than 2^18-1. The partition
        # above consists of complete index blocks; adjust by the next boundary
        # term and subtract it at the following boundary through a prefix sum.
        endpoint = min((block + 1) * block_size, term_count - 1)
        gray = endpoint ^ (endpoint >> 1)
        sums = [sum((gray >> j) & 1 for j in row) for row in rows]
        size = bin(gray).count('1')
        product_nonzero = 1
        for value in sums:
            if value:
                product_nonzero *= value
        boundary_term = 0
        if endpoint != term_count - 1 and all(sums):
            boundary_term = product_nonzero * (-1 if (n - size) % 2 else 1)
        record = {'last_subset_index': endpoint, 'gray_mask': gray,
                  'subset_size': size, 'row_sums': sums,
                  'zero_rows': sums.count(0), 'nonzero_product': product_nonzero,
                  'signed_accumulator': accumulator + boundary_term}
        raw = json.dumps(record, sort_keys=True, separators=(',', ':')).encode()
        digest.update(raw + b'\n')
        blocks.append(record)
    return {'L': L, 'rows': rows, 'permanent': matching,
            'complete_subset_terms': term_count, 'empty_subset_term': 0,
            'nonempty_terms': term_count - 1, 'row_updates': 3 * (term_count - 1),
            'block_records': blocks, 'block_sha256': digest.hexdigest(),
            'formula': 'sum_S (-1)^(n-|S|) product_i |neighbors(i) intersect S|',
            'algorithm': 'GRAY_RYSER_EXACT_INTEGERS_NO_FLOAT'}, {
                'primary_algorithm': 'PERIODIC_ROW_MATCHING_TRANSFER_TRACE',
                'boundary_states': 1 << L, 'transfer_matrix': matrix,
                'telemetry_algorithm': 'BINARY_SUBSET_HISTOGRAM_INVERSE_GRAY_BLOCKS',
                'complete_audited_nonempty_subsets': term_count - 1}


def literal_graph(L):
    volume = L ** 3
    edges = []
    sections = [[], [], []]
    for a in range(volume):
        x, rem = divmod(a, L * L)
        y, z = divmod(rem, L)
        neighbors = [a, ((x + 1) % L) * L * L + rem,
                     x * L * L + ((y + 1) % L) * L + z,
                     x * L * L + y * L + (z + 1) % L]
        for shift, b in enumerate(neighbors):
            edges.append([4 * a + shift, a, volume + b])
        for axis, coordinate in enumerate((x, y, z)):
            if coordinate == L - 1:
                sections[axis].append(4 * a + axis + 1)
    cuts = [0, 4 * L * L, 4 * L, 4]
    born = [edge[:] for edge in edges if edge[0] not in cuts]
    children = []
    for index, edge_id in enumerate(cuts):
        a, b = edges[edge_id][1:]
        first = 4 * volume + 2 * index
        born += [[first, a, 2 * volume + 1], [first + 1, 2 * volume, b]]
        children.append({'old_edge': edge_id, 'children': [first, first + 1]})
    return {'L': L, 'old_vertices': 2 * volume, 'old_edges': edges,
            'Born_vertices': 2 * volume + 2, 'Born_edges': born,
            'cut_order': cuts, 'children': children, 'crosssections': sections,
            'edge_id_convention': 'STABLE_OLD_IDS_RETAINED_CHILD_IDS_APPEND_AFTER_OLD_RANGE',
            'physical_geometry_qualified': False}


def expected(case, progress):
    require(case in ('control2', 'L4', 'L5'), 'frozen cases')
    L = {'control2': 2, 'L4': 4, 'L5': 5}[case]
    count, audit = complete_layer(L, progress)
    if case == 'control2':
        return {'schema': 'P60_LAYER_PERMANENT_CONTROL_V001', 'actual': count,
                'independent_analytic_expectation': 9,
                'actual_matches': count['permanent'] == 9, 'native_spectrum': False,
                'requires_distinct_saved_checker': True}, audit
    vertices = 2 * L ** 3
    edges = 2 * vertices
    lower = count['permanent'] ** L
    mu = []
    for p in (0, 1):
        for q in (0, 1):
            value = Fraction(2 * p - q, 8)
            mu.append({'p': p, 'q': q, 'mu': str(value),
                       'Ud_minus_abs_mu': str(1 - abs(value))})
    return {'schema': 'P60_NATIVE_G1_SIZE_PREFLIGHT_V001',
            'graph': literal_graph(L), 'layer_count': count,
            'complete_full_domain_dimension': 2 ** edges * 12 ** vertices + 2 ** (edges + 4) * 12 ** (vertices + 2),
            'fixed_Q0_persistent_q_newq0_cellsI_joined_dimension': 17 * 2 ** edges,
            'old_incidence_dimension': 2 ** edges,
            'old_incidence_complex128_vector_bytes': 2 ** (edges + 4),
            'joined_Q0_complex128_vector_bytes': 17 * 2 ** (edges + 4),
            'ice_dimension_lower_bound': lower,
            'ice_lower_bound_reason': 'Independent layer perfectmatchings complemented in shift0/1/2 graph; shift3 empty',
            'ice_complex128_vector_bytes_lower_bound': 16 * lower,
            'ice_complex128_dense_matrix_bytes_lower_bound': 16 * lower ** 2,
            'complete_ice_dimension_known': False, 'layer_subset_only': True,
            'word_uniform_mu_table': mu,
            'diagonal_all_word_off_ice_lower_bound': '3/2',
            'diagonal_Q0_word_uniform_off_ice_lower_bound': '7/4',
            'old_Q0_written_Weyl_lower_bound': str(Fraction(7, 4) - Fraction(2 * edges, 5)),
            'Weyl_gap_status': 'NONCOVERING_NOT_A_GAP_REFUTATION',
            'spectral_execution': False, 'full_h_gap_certified': False,
            'R3_qualified': False, 'Gamma_qualified': False, 'physical_release': False}, audit

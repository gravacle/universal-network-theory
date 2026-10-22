"""SOURCE ONLY. Independent whole fixed N-ladder count reconstruction.
Union-find components, Pascal coefficient arrays, attachment convolution.
No producer import or call. Root executes after distinct review only.
"""
from itertools import product


def need(ok, why):
    if not ok:
        raise ValueError(why)


def binomial_row(slots):
    row = [1]
    for unused in range(slots):
        row = [1] + [row[i-1] + row[i] for i in range(1, len(row))] + [1]
    return row


def coefficient(row, k):
    return row[k] if 0 <= k < len(row) else 0


def convolution(a, b, degree):
    out = [0] * (min(degree, len(a)+len(b)-2)+1)
    for i, x in enumerate(a):
        for j, y in enumerate(b[:max(0, degree-i+1)]):
            out[i+j] += x*y
    return out


def partition(vertices, edges):
    root = list(range(vertices))
    def find(x):
        while root[x] != x:
            root[x] = root[root[x]]
            x = root[x]
        return x
    for a, b in edges:
        x, y = find(a), find(b)
        if x != y:
            root[max(x, y)] = min(x, y)
    groups = {}
    for v in range(vertices):
        groups.setdefault(find(v), []).append(v)
    return sorted(groups.values(), key=lambda row: row[0])


def graph(kind, size):
    edges = []
    if kind == 'METHOD_STRIP':
        n = 2*size
        for a in range(0, n, 2):
            local_b = a + 1
            next_b = ((a + 2) % n) + 1
            edges += [[a, local_b], [a, next_b], [a, local_b], [a, local_b]]
        cuts = [0, 1, 2, 3]
    else:
        need(kind == 'PERIODIC_Q4', 'fixed graph kind')
        L = size
        cells = L**3
        n = 2*cells
        for a in range(cells):
            x, rest = divmod(a, L*L)
            y, z = divmod(rest, L)
            destinations = [a, ((x+1) % L)*L*L+rest,
                            x*L*L+((y+1) % L)*L+z,
                            x*L*L+y*L+(z+1) % L]
            edges += [[a, cells+b] for b in destinations]
        cuts = [0, 4*L*L, 4*L, 4]
    old_degrees = [0]*n
    for a, b in edges:
        old_degrees[a] += 1
        old_degrees[b] += 1
    need(old_degrees == [4]*n, 'complete old degrees')
    born = [[i, a, b] for i, (a, b) in enumerate(edges) if i not in cuts]
    for i, edge in enumerate(cuts):
        a, b = edges[edge]
        born += [[len(edges)+2*i, a, n+1], [len(edges)+2*i+1, n, b]]
    born_degrees = [0]*(n+2)
    for key, a, b in born:
        born_degrees[a] += 1
        born_degrees[b] += 1
    need(born_degrees == [4]*(n+2), 'complete Born degrees')
    return {'kind': kind, 'size': size, 'old_vertices': n, 'old_edges': edges,
            'ordered_cuts': cuts, 'born_edges_with_persistent_ids': born,
            'stars': [n, n+1]}


def counts(g, active, Q):
    n = g['old_vertices']
    E = len(g['old_edges'])
    need(partition(n, g['old_edges']) == [list(range(n))], 'old connected')
    parts = partition(n+2, [[a, b] for key, a, b in g['born_edges_with_persistent_ids']])
    slots_old = binomial_row(n+len(active))
    slots_new = binomial_row(n+2+len(active))
    old_dimension = (1 << (E+n))*coefficient(slots_old, Q)
    born_dimension = (1 << (E+4+n+2))*coefficient(slots_new, Q)
    full = old_dimension + born_dimension
    local = []
    for part in parts:
        c = len(part)
        o = sum(v < n for v in part)
        a = sum(v in active for v in part)
        local.append((c, o, a, binomial_row(c+a)))
    # Independent generating coefficient of all states in Born components
    # admitting inverse Birth: empty components fix insertedq0, occupied ones
    # have allq mobile; resources must fit old slots. Compare to per-allocation
    # attachment sum below, not only to the author's final histogram.
    attachment_polynomial = [1]
    resource_polynomial = [1]
    for c, o, a, choices in local:
        factor = [1 << o] + [(1 << c)*choices[k]
                              for k in range(1, min(o+a, Q)+1)]
        attachment_polynomial = convolution(attachment_polynomial, factor, Q)
        resource_polynomial = convolution(resource_polynomial, choices[:Q+1], Q)
    need(coefficient(resource_polynomial, Q) == coefficient(slots_new, Q), 'whole slot polynomial identity')
    histogram = {}
    def add(dimension, multiplicity):
        if multiplicity:
            histogram[dimension] = histogram.get(dimension, 0) + multiplicity
    details = []
    if Q == 0:
        connected_dimension = (1 << E) + (1 << (E+4))
        old_components = 1 << n
        add(connected_dimension, old_components)
        add(1 << (E+4), 3*old_components)
        details.append({'Q0_fixed_old_word_dimension': connected_dimension,
                        'old_word_component_multiplicity': old_components,
                        'dark_new_q_nonzero_multiplicity': 3*old_components})
    else:
        old_components = int(old_dimension > 0)
        connected_dimension = old_dimension
        attached_total = 0
        options = [range(min(c+a, Q)+1) for c, o, a, choices in local]
        for allocation in product(*options):
            if sum(allocation) != Q:
                continue
            dimension = 1 << (E+4)
            multiplicity = 1
            attached = 1 if old_dimension else 0
            for (c, o, a, choices), tokens in zip(local, allocation):
                dimension *= choices[tokens]
                if tokens:
                    dimension *= 1 << c
                else:
                    multiplicity *= 1 << c
                    attached *= 1 << o
                if tokens > o+a:
                    attached = 0
            remaining = multiplicity-attached
            need(remaining >= 0, 'nonnegative full complement multiplicity')
            add(dimension, remaining)
            attached_total += attached*dimension
            details.append({'resource_allocation': list(allocation), 'dimension_each': dimension,
                            'total_multiplicity': multiplicity, 'attached_to_old': attached,
                            'remaining_born_only': remaining})
        polynomial_attached = (1 << (E+4))*coefficient(attachment_polynomial, Q) if old_dimension else 0
        need(attached_total == polynomial_attached, 'independent complete Birth attachment convolution')
        connected_dimension += polynomial_attached
        if old_dimension:
            add(connected_dimension, 1)
    need(sum(d*m for d, m in histogram.items()) == full, 'complete dimensions including complements')
    original = g['kind'] == 'METHOD_STRIP' and g['size'] == 1 and active == [0] and Q == 1
    storage = 16*connected_dimension*connected_dimension + 8*connected_dimension
    return {'graph_kind': g['kind'], 'size': g['size'], 'N_old': n, 'E_old': E,
            'A_old_vertices': active, 'Q': Q, 'born_graph_components': parts,
            'full_unrestricted_parent_dimension': (1 << E)*12**n + (1 << (E+4))*12**(n+2),
            'full_fixed_Q_A_dimension': full,
            'component_dimension_histogram': {str(d): histogram[d] for d in sorted(histogram)},
            'old_containing_component_multiplicity': old_components,
            'dimension_per_old_containing_component': connected_dimension,
            'allocation_census': details,
            'one_complex_vector_bytes': 16*connected_dimension,
            'complete_eigenvectors_and_eigenvalues_minimum_bytes': storage,
            'full_dense_minimum_fits_96GiB': storage <= 96*(1 << 30),
            'full_dense_minimum_fits_native_16GiB': storage <= 16*(1 << 30),
            'five_original_preparations_literal': original,
            'preparation_scope': 'ORIGINAL_FIVE' if original else 'NO_UNIQUELY_SPECIFIED_ANALOGUE',
            'exact_component_count_hypotheses': 'NONZERO_h_g_t_kappa_Birth; inserted_Av0; full_incidence_domain',
            'exact_DE_certified': False, 'physical_S1_family_selected': False}


def reconstruct():
    rows = []
    progress = []
    for kind, size in [('METHOD_STRIP', k) for k in range(1, 5)] + [('PERIODIC_Q4', k) for k in (2, 3, 4)]:
        g = graph(kind, size)
        progress.append({'kind': 'FULL_LITERAL_GRAPH', 'graph': g})
        n = g['old_vertices']
        for active in ([0], list(range(n))):
            for Q in sorted({0, 1, 2, n}):
                row = counts(g, active, Q)
                rows.append(row)
                progress.append({'kind': 'EXACT_FULL_COMPONENT_COUNT', 'row': row})
    need(len(rows) == 54 and len(progress) == 61, 'whole frozen call census')
    return {'schema': 'P49_EXACT_N_LADDER_COUNTS_V001', 'rows': rows,
            'scope': 'EXACT_CONNECTIVITY_COUNTS_NOT_SPECTRA_OR_NEW_PREPARATIONS',
            'all_rungs_preserved': True, 'root_numerical_launch_only': True}, progress

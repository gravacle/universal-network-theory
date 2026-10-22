"""SOURCE ONLY. Independent full N2 H built by undirected Hermitian pairs.
Arithmetic state indexing, common280 units, then full emitted columns and
active560 rows checked. No Code2 scientific module imported or called.
"""
from fractions import Fraction as Q


def need(ok, why):
    if not ok:
        raise ValueError(why)


def state_at(index):
    need(type(index) is int and 0 <= index < 20672, 'whole native index')
    sector, nv, local = (0, 2, index) if index < 192 else (1, 4, index-192)
    slot, q = divmod(local, 1 << nv)
    inc, carrier_slot = divmod(slot, nv+1)
    return (sector, inc, 0 if carrier_slot == nv else 1 << carrier_slot, q,
            int(carrier_slot == nv), int(carrier_slot != nv))


def index_of(state):
    sector, inc, p, q, r, s = state
    need(sector in (0, 1), 'literal two sectors')
    nv = 2+2*sector
    need(0 <= inc < 1 << (4+4*sector) and 0 <= q < 1 << nv, 'native incidence/register bounds')
    if p == 0:
        need((r, s) == (1, 0), 'Q1 Ready state')
        slot = nv
    else:
        need(p > 0 and p & (p-1) == 0 and p < 1 << nv and (r, s) == (0, 1), 'Q1 carrier state')
        slot = p.bit_length()-1
    index = 192*sector+(inc*(nv+1)+slot)*(1 << nv)+q
    need(state_at(index) == tuple(state), 'complete arithmetic state bijection')
    return index


def reconstruct(packet, selected, emitted, guard):
    states = [state_at(i) for i in range(20672)]
    need(packet['full_states'] == [list(s) for s in states], 'all20672 native states in literal order')
    rows = [{} for _ in states]
    def put(i, j, a, b):
        x, y = rows[i].get(j, (0, 0))
        z = x+a, y+b
        if z == (0, 0):
            rows[i].pop(j, None)
        else:
            rows[i][j] = z
    def pair(j, target, re, im=0):
        i = index_of(target)
        need(i != j, 'offdiagonal owner pair')
        put(i, j, re, im)
        put(j, i, re, -im)
    phase = ((1, 0), (0, -1), (-1, 0), (0, 1))
    for j, state in enumerate(states):
        sector, inc, p, q, ready, spent = state
        nv = 2+2*sector
        edges = [(0, 1, e) for e in range(4)] if not sector else [
            (0, 3, e) if e%2 == 0 else (2, 1, e) for e in range(8)]
        degrees = [0]*nv
        count = 0
        for a, b, e in edges:
            if inc & (1 << e):
                degrees[a] += 1; degrees[b] += 1; count += 1
        # Every diagonal owner separately in exact1/280 units.
        diagonal = 1120*count
        for v, d in enumerate(degrees):
            diagonal += 280*(d-3)**2
            diagonal += (280+70*d)*int(bool(p & (1 << v)))
            diagonal += (245-35*d)*int(bool(q & (1 << v)))
            diagonal += 196 if ready & (1 << v) else 308 if spent & (1 << v) else 112
        put(j, j, diagonal, 0)
        for a, b, e in edges:
            bit = 1 << e
            if not inc & bit:
                pair(j, (sector, inc | bit, p, q, ready, spent), -56)
            elif p & (1 << a):
                # Only A->B owner direction; add Hermitian reverse once.
                re, im = phase[e if not sector else e//2]
                pair(j, (sector, inc, p ^ (1 << a) ^ (1 << b), q, ready, spent), -280*re, 280*im)
        for v in range(nv):
            bit = 1 << v
            if p & bit and not q & bit:
                pair(j, (sector, inc, p, q | bit, ready, spent), 140)
        if ready == 1:
            pair(j, (sector, inc, 1, q, 0, 1), 80, 120)
        if sector == 0 and count == 2:
            target_inc = 0
            for e in range(4):
                if inc & (1 << e):
                    target_inc |= (1 << (2*e)) | (1 << (2*e+1))
            pair(j, (1, target_inc, p, q, ready, spent), 35, -70)
        if j%256 == 0:
            guard()
    need(sum(map(len, rows)) == 222640, 'all222640 complete parent directed entries')
    stream = iter(emitted)
    first = next(stream)
    need(first['kind'] == 'basis' and first['index'] == 0
         and first['payload']['states'] == [list(s) for s in states], 'original complete emitted basis')
    params = {'real': {'h': '1/5', 'Delta': '4', 'Ud': '1', 'epsilon_c': '1', 't': '1',
              'epsilon_r': '7/8', 'g': '1/2', 'lambda_R': '1/8', 'lambda_J': '1/4',
              'E_I': '2/5', 'E_R': '7/10', 'E_S': '11/10', 'identity_offset': '0'},
              'dstar': '3', 'epsilon_B': ['1/8', '-1/4'], 'kappa': [['2/7', '3/7'] for _ in range(4)],
              'old_hop_phases': [[str(a), str(b)] for a, b in phase],
              'born_hop_phases': [[str(a), str(b)] for a, b in phase for _ in range(2)]}
    need(first['payload']['parameters'] == params and first['payload']['cuts'] == [0, 1, 2, 3]
         and first['payload']['graph_edges'] == [[[0, 1]]*4, [[0, 3], [2, 1]]*4], 'whole actual canonical tuple/graph')
    parent = list(range(20672))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    for j, state in enumerate(states):
        record = next(stream)
        need(record['kind'] == 'column' and record['index'] == j and record['payload']['state'] == list(state), 'all original emitted columns')
        expected = {i: (a, -b) for i, (a, b) in rows[j].items()}
        given = {}
        for entry in record['payload']['entries']:
            i = entry['target']
            a, b = (Q(v)*280 for v in entry['value'])
            need(type(i) is int and i not in given and a.denominator == b.denominator == 1 and (a or b), 'exact complete emitted coefficients')
            given[i] = int(a), int(b)
        need(given == expected, 'every independently reconstructed emitted column')
        need(list(map(Q, record['payload']['diagonal'])) == [Q(rows[j][j][0], 280), Q(0)]
             and Q(record['payload']['H2_diagonal']) == Q(sum(a*a+b*b for a, b in expected.values()), 280**2), 'full emitted diagonal/norm metadata')
        for i, (a, b) in expected.items():
            need(rows[i].get(j) == (a, b), 'all parent Hermitian pairs')
            x, y = find(i), find(j)
            if x != y:
                parent[max(x, y)] = min(x, y)
        if j%256 == 0:
            guard()
    need(next(stream)['kind'] == 'summary' and next(stream, None) is None, 'complete original emit EOF')
    groups = {}
    for i in range(20672):
        groups.setdefault(find(i), []).append(i)
    components = sorted(groups.values(), key=lambda g: g[0])
    need(components == packet['components'] and sorted(map(len, components)) == [2048, 2048, 3072, 3072, 10432], 'all five independent union-find components')
    active = next(g for g in components if 39 in g)
    local = {i: j for j, i in enumerate(active)}
    need(len(active) == 10432 and sum(len(rows[i]) for i in active) == 112048, 'full10432 active component and all112048 entries')
    shifted = []
    for gj in active:
        row = {}
        for gi, (a, b) in rows[gj].items():
            need(gi in local, 'whole active invariance')
            a, b = 2*a-(14847 if gi == gj else 0), 2*b
            if a or b:
                row[local[gi]] = (a, b)
        shifted.append([[i, a, b] for i, (a, b) in sorted(row.items())])
    other = [tuple(s) for s in selected['states']]
    need(selected['Q'] == 1 and selected['active_mask'] == 1 and len(other) == len(set(other)) == 20672
         and set(other) == set(states), 'whole original selected-census bijection')
    selected_index = {s: i for i, s in enumerate(other)}
    rebuilt = {'shifted_row_norm': '10207/560', 'full_states': [list(s) for s in states],
        'native_to_selected_census': [selected_index[s] for s in states],
        'selected_census_to_native': [index_of(s) for s in other], 'components': components,
        'all_component_weights': [1, 0, 0, 0, 0], 'active_to_native': active,
        'active_states': [list(states[i]) for i in active], 'seed_index': local[39], 'rows': shifted,
        'shift': '2121/80', 'coefficient_denominator': 560, 'exact_all_component_invariance': True,
        'native_input_authentication': 'EXTERNAL_ROOT_RECEIPTS_REQUIRED'}
    need(rebuilt == packet and Q(max(sum(abs(a)+abs(b) for i, a, b in row) for row in shifted), 560) == Q(10207, 560), 'entire exact native packet and norm independently reconstructed')
    return rebuilt

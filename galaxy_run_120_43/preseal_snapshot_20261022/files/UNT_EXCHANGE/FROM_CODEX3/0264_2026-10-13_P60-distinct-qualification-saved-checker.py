"""Codex3 SOURCE ONLY. Independent complete P60 qualification saved checker.
Root executes after distinct source/runtime review. Never imports producer/source.
Literal cubical boundary construction, coefficient DP for subset syndromes, BFS,
and exact row-operation verification. No carrier-class or physical acceptance.
"""
import argparse
from collections import Counter, deque
from fractions import Fraction as F
import hashlib
import json
from math import comb
from pathlib import Path

SOURCE = Path('/Users/bgm/Research/UNT_EXCHANGE/lanes/P60_CODEX2/p60_toric_d3_qualification_v002.py')
SOURCE_HASH = 'fc72f42ca3209e7df631d43ec0595c9406bf40da994cb1d86719fdf863e5bd99'
RUNNER = Path('/Users/bgm/Research/UNT_EXCHANGE/lanes/P60_CODEX2/p60_qualification_root_producer_v001.py')
RUNNER_HASH = '375cfc31e9bab77afeed79147ac6ad9fbcacfd3d2fd8ffba5cb756c029677db4'
LIMIT = 16*2**20
FILES = {'START.json', 'SOURCE_SNAPSHOT.py', 'ACTUAL_PRE.json', 'ACTUAL_RETURN.json', 'FINISH.json'}
CASES = {'small333': ('small_qualification', [[3, 3, 3]]),
         'small334': ('small_qualification', [[3, 3, 4]]),
         'growth17': ('growth_qualification', [])}


def require(ok, label):
    if not ok:
        raise ValueError(label)


def bounded(path, limit=LIMIT):
    require(path.is_file() and not path.is_symlink() and path.stat().st_size <= limit,
            'bounded plain file '+str(path))
    with path.open('rb') as stream:
        raw = stream.read(limit+1)
    require(len(raw) <= limit, 'bounded actual read')
    return raw


def decode(raw):
    def pairs(items):
        value = {}
        for k, v in items:
            require(k not in value, 'duplicate JSON key')
            value[k] = v
        return value
    return json.loads(raw, object_pairs_hook=pairs,
                      parse_constant=lambda s: (_ for _ in ()).throw(ValueError(s)))


def literal(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): literal(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [literal(v) for v in value]
    return value


def equal(actual, expected, location='root'):
    require(type(actual) is type(expected), 'type '+location)
    if isinstance(expected, dict):
        require(set(actual) == set(expected), 'keys '+location)
        for k in expected:
            equal(actual[k], expected[k], location+'/'+k)
    elif isinstance(expected, list):
        require(len(actual) == len(expected), 'length '+location)
        for i, (a, e) in enumerate(zip(actual, expected)):
            equal(a, e, location+'/'+str(i))
    else:
        require(actual == expected, 'value '+location)


def cell_complex(shape, include_faces):
    nx, ny, nz = shape
    vertices = [[x, y, z] for x in range(nx) for y in range(ny) for z in range(nz)]
    def index(x):
        return (x[0] % nx)*ny*nz + (x[1] % ny)*nz + x[2] % nz
    def moved(x, a):
        out = list(x); out[a] += 1
        return out
    # Qu bit labels are three per lexicographic vertex. Build boundary first;
    # stars are then recovered as transposed boundary incidence.
    edges = [[i, index(moved(v, a))] for i, v in enumerate(vertices) for a in range(3)]
    incident = [set() for _ in vertices]
    for e, ends in enumerate(edges):
        for v in ends:
            incident[v].add(e)
    stars = [sum(1 << e for e in es) for es in incident]
    faces = []; labels = []
    if include_faces:
        for v in vertices:
            for a, b in [(0, 1), (0, 2), (1, 2)]:
                boundary = {3*index(v)+a, 3*index(moved(v, a))+b,
                            3*index(moved(v, b))+a, 3*index(v)+b}
                require(len(boundary) == 4, 'reference square boundary')
                faces.append(sum(1 << e for e in boundary)); labels.append([v, a, b])
    loops = []
    for a, length in enumerate(shape):
        ids = []
        for x in range(length):
            v = [0, 0, 0]; v[a] = x; ids.append(3*index(v)+a)
        loops.append(sum(1 << e for e in ids))
    graph = [Counter() for _ in vertices]
    for u, v in edges:
        graph[u][v] += 1; graph[v][u] += 1
    return {'shape': shape, 'vertices': vertices, 'edges': edges, 'X_stars': stars,
            'Z_faces': faces, 'face_labels': labels, 'Z_winding_loops': loops}, graph


def binary_rank(values):
    # Least-significant pivots, independent of producer's highest-bit basis.
    basis = {}
    for word in values:
        while word:
            pivot = word & -word
            if pivot in basis:
                word ^= basis[pivot]
            else:
                basis[pivot] = word
                break
    return len(basis)


def graph_layers(graph, origin):
    distances = [-1]*len(graph); ways = [0]*len(graph)
    distances[origin] = 0; ways[origin] = 1; pending = deque([origin])
    while pending:
        u = pending.popleft()
        for v, multiplicity in graph[u].items():
            if distances[v] == -1:
                distances[v] = distances[u]+1; pending.append(v)
            if distances[v] == distances[u]+1:
                ways[v] += multiplicity*ways[u]
    require(-1 not in distances, 'whole graph connected')
    return distances, ways


def echelon(graph, mu):
    # Reconstruct full original rational matrix and every first-pivot row
    # operation; retain the exact canonical echelon and pivot history.
    n = len(graph)
    matrix = [[F(int(i == j))-mu*graph[i].get(j, 0) for j in range(n)] for i in range(n)]
    next_row = 0; steps = []
    for column in range(n):
        candidates = [r for r in range(next_row, n) if matrix[r][column] != 0]
        if not candidates:
            continue
        chosen = candidates[0]
        matrix[next_row], matrix[chosen] = matrix[chosen], matrix[next_row]
        pivot = matrix[next_row][column]; steps.append([column, pivot])
        matrix[next_row] = [x/pivot for x in matrix[next_row]]
        for r in range(next_row+1, n):
            coefficient = matrix[r][column]
            if coefficient:
                matrix[r] = [matrix[r][j]-coefficient*matrix[next_row][j] for j in range(n)]
        next_row += 1
    return {'mu': mu, 'rank': next_row, 'pivots': steps, 'row_echelon': matrix}


def small_expected(shape):
    carrier, graph = cell_complex(shape, True)
    stars = carrier['X_stars']; faces = carrier['Z_faces']; edges = carrier['edges']
    nv = len(stars); ne = len(edges)
    symplectic = [[bin(s & f).count('1') % 2 for f in faces] for s in stars]
    supports = stars+faces
    overlap = [dict() for _ in supports]
    for a, sa in enumerate(supports):
        for b in range(a):
            if sa & supports[b]:
                overlap[a][b] = 1; overlap[b][a] = 1
    star_distances = []; all_generator_distances = []
    for u in range(nv):
        star_distances.append(graph_layers(graph, u)[0])
        all_generator_distances.append(graph_layers(overlap, u)[0][:nv])
    ranks = {'stars': binary_rank(stars), 'faces': binary_rank(faces),
             'cycle_generators': binary_rank(faces+carrier['Z_winding_loops'])}
    degree = [sum(row.values()) for row in graph]; mu = F(1, degree[0])
    poles = [echelon(graph, x) for x in [mu/2, mu, F(6, 5)*mu]]
    # Coefficients of product_e (1 + t X^{boundary(e)}) in the binary
    # boundary group algebra. Descending degree ensures every edge is used
    # at most once. This is not the producer's combinations enumeration.
    layers = [Counter({0: 1}), Counter(), Counter(), Counter()]
    endpoints = [(1 << u) ^ (1 << v) for u, v in edges]
    for boundary in endpoints:
        for weight in [3, 2, 1]:
            for syndrome, multiplicity in list(layers[weight-1].items()):
                layers[weight][syndrome ^ boundary] += multiplicity
    totals = [sum(row.values()) for row in layers]
    require(totals == [comb(ne, w) for w in range(4)], 'reference complete coefficient census')
    distances, counts = graph_layers(graph, 0)
    minimum = [{'target': v, 'distance': distances[v],
                'all_weight0_to3_counts': [row.get(1 ^ (1 << v), 0) for row in layers],
                'independent_graph_geodesic_count': counts[v]}
               for v in range(1, nv) if distances[v] <= 3]
    # Independent sparse endpoint expansion, then full finite quotient rows.
    layer = {(0, 0, 0): 1}; free_rows = []
    coordinate_index = {tuple(v): i for i, v in enumerate(carrier['vertices'])}
    for depth in range(9):
        wrapped = [0]*nv
        for v, count in layer.items():
            wrapped[coordinate_index[tuple(v[i] % shape[i] for i in range(3))]] += count
        free_rows.append(wrapped)
        nxt = Counter()
        if depth < 8:
            for v, count in layer.items():
                for axis in range(3):
                    for sign in [-1, 1]:
                        target = list(v); target[axis] += sign; nxt[tuple(target)] += count
        layer = nxt
    finite = [[1]+[0]*(nv-1)]
    for depth in range(8):
        finite.append([sum(graph[j].get(i, 0)*finite[-1][j] for j in range(nv)) for i in range(nv)])
    require(finite == free_rows, 'reference complete wrap identity')
    far = distances.index(2)
    first_edge = next(e for e, ends in enumerate(edges) if 0 in ends)
    boundary = endpoints[first_edge]
    controls = {'identity': {'support': 0, 'record_flip': False, 'retained_star_violations': []},
                'one_qubit_at_distance2': {'holes': [0, far], 'support': 1 << first_edge,
                    'record_flip': bool(boundary & 1),
                    'retained_star_violations': [v for v in range(nv) if v not in [0, far] and (boundary >> v) & 1]},
                'bare_counting_row_sums': degree, 'uniform_conserving_row_sums': [mu*d for d in degree]}
    return {'scope': 'SECOND_CARRIER_TORIC_QUALIFICATION_NOT_YET_CRITICAL_CLASS',
            'carrier': carrier, 'adjacency': [dict(r) for r in graph],
            'star_face_symplectic_matrix': symplectic, 'ranks': ranks,
            'all_pair_star_distances': star_distances,
            'all_pair_full_generator_distances': all_generator_distances,
            'measured_degree': degree, 'candidate_mu_c': mu, 'resolvents': poles,
            'complete_weight0_to3_syndrome_counts': [dict(r) for r in layers],
            'enumerated_subset_totals': totals, 'minimum_rows': minimum,
            'all_depth0_to8_torus_walk_counts': finite, 'all_wrap_counts': free_rows,
            'controls': controls, 'critical_class_tested': False, 'TWO_CARRIER_adopted': False,
            'native_V005_release': False, 'history_vs_unique_operator_ensemble': 'DISTINCT_BEYOND_MINIMUM'}


def growth_expected():
    carrier, graph = cell_complex([17, 17, 17], False)
    distances, _ = graph_layers(graph, 0)
    balls = []
    for r in range(9):
        # Expanded all-r polynomial instead of producer's binomial expression.
        reference = (4*r**3+6*r*r+8*r+3)//3
        balls.append({'radius': r, 'measured_vertices': sum(d <= r for d in distances),
                      'combinatorial_reference': reference})
    return {'scope': 'OPERATOR_GRAPH_D3_FAMILY_GATE_WITH_ALL_R_THEORY_REQUIRED',
            'shape': [17, 17, 17], 'vertices': carrier['vertices'],
            'edges_from_star_ownership': [sorted(ends) for ends in carrier['edges']],
            'vertex_distances_from_origin': distances, 'balls': balls,
            'finite_torus_is_not_infinite_space': True, 'TWO_CARRIER_adopted': False}


def check(directory, case):
    require(case in CASES, 'fixed case')
    require(directory.is_dir() and not directory.is_symlink(), 'plain directory')
    entries = list(directory.iterdir())
    require({p.name for p in entries} == FILES and len(entries) == 5, 'whole five-file census')
    require(all(p.is_file() and not p.is_symlink() for p in entries), 'plain output files')
    require(sum(p.stat().st_size for p in entries) <= LIMIT, 'whole16MiB output cap')
    source = bounded(SOURCE, 2**20); runner = bounded(RUNNER, 2**20)
    require(hashlib.sha256(source).hexdigest() == SOURCE_HASH, 'original source pin')
    require(hashlib.sha256(runner).hexdigest() == RUNNER_HASH, 'original runner pin')
    raw = {p.name: bounded(p) for p in entries}
    require(sum(map(len, raw.values())) <= LIMIT, 'consumed whole16MiB cap')
    require(raw['SOURCE_SNAPSHOT.py'] == source, 'complete source snapshot')
    start = {'schema': 'P60_QUALIFICATION_FIXED_CALL_V001', 'case': case,
             'source': {'path': str(SOURCE), 'sha256': SOURCE_HASH}, 'runner_sha256': RUNNER_HASH,
             'caps': {'cpu': 1, 'rss_bytes': 268435456, 'seconds': 120, 'output_bytes': LIMIT},
             'external_supervisor_required': True, 'TWO_CARRIER_adopted': False}
    equal(decode(raw['START.json']), start)
    function, arguments = CASES[case]
    equal(decode(raw['ACTUAL_PRE.json']), {'case': case, 'function': function, 'arguments': arguments})
    expected = growth_expected() if case == 'growth17' else small_expected(arguments[0])
    equal(decode(raw['ACTUAL_RETURN.json']), literal({'case': case, 'arguments_after': arguments,
                                                     'exception': None, 'value': expected}))
    equal(decode(raw['FINISH.json']), {'status': 'RAW_RETURN_PENDING_DISTINCT_SAVED_REVIEW',
          'case': case, 'scientific_source_closing_hash_match': True, 'TWO_CARRIER_adopted': False,
          'critical_class_tested': False})
    require({p.name for p in directory.iterdir()} == FILES, 'closing census')
    return {'status': 'PASS_COMPLETE_EXACT_QUALIFICATION_OUTPUT_ONLY', 'case': case,
            'files': {k: {'bytes': len(v), 'sha256': hashlib.sha256(v).hexdigest()} for k, v in raw.items()},
            'comparison': 'EVERY_LITERAL_TYPED_FIELD_EXACT_NO_PRODUCER_IMPORT',
            'checker_author': 'Codex3', 'source_author': 'Codex2',
            'runtime_acceptance': 'ROOT_SEPARATE_GATE', 'TWO_CARRIER_adopted': False,
            'critical_class_tested': False, 'physical_prediction_released': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--case', choices=sorted(CASES), required=True)
    args = parser.parse_args()
    print(json.dumps(check(args.input, args.case), indent=2, allow_nan=False))

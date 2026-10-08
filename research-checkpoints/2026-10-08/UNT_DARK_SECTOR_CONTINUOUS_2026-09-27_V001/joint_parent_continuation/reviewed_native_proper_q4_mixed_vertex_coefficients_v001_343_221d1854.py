#!/usr/bin/env python3
"""Guarded state-free proper-q4 operator/source-jet arithmetic; root only."""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime, timezone
import argparse, ast, hashlib, itertools, json, os, sys, traceback

AUTHOR_DRAFT = True
J = Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation')
SOURCE = 'native_proper_q4_mixed_vertex_coefficients_v001.py'
STEM = 'NATIVE_PROPER_Q4_MIXED_VERTEX_COEFFICIENTS_V001'
PROTOCOL = STEM + '.md'
PROTOCOL_SHA = 'b34b8e276034a9648dbdf5a23fb8fadc28341fdc6f8001019c5cfa4cb1b6750e'
PINS = {
    'NATIVE_PROPER_BOND_COVARIANT_ACCELERATION_MATERIAL_LIFT_CANDIDATE_V001.md': 'af1fab1ab22cc9cac29582348a7eaeb89309ba09a230ff0ed7067d1e778b7cd2',
    'NATIVE_ROTATING_MATERIAL_CLOCK_SOURCE_EXTENSION_V001.md': 'e8911d59ae25f9d397a57a6dcd6d0ca5c450df82566935c00f8436568f7484ff',
    'LOCAL_RECORD_FEEDBACK_Q4_CONSERVING_FORMATION_CANDIDATE_V001.md': '07323053b75b947b35712f0ac8fc4ce04c2766131cd4e684fd64167321b51f3c',
    'LOCAL_RECORD_FEEDBACK_PROPER_METRIC_MEMORY_JOIN_AND_BODY_LOAD_V001.md': 'e7f89d032b72946c08a2e9e26a9bd30e6242b97bbef211e773e1e5dae4c84cf8',
    'LOCAL_RECORD_FEEDBACK_COMPLETE_STRAIN_SOURCE_CONTRACT_V001.md': 'cc363bf1885917a9beededadb8d49b5d898c951bd54a1e2d2ad6ce5003ebaf63',
    'local_record_feedback_q4_sparse_insertion_verification_v001.py': '774c81de75458fb430009655f83f00dcc24bac423385ac1b72409dc6f160134e',
}
CONTROL_COUNT = 15
RAW, CHECKS, RECORDS, OUTPUTS = {}, [], [], {}
FLAGS = {k: False for k in ('physical_material_member_adopted', 'proper_preparation_selected',
    'physical_units_registered', 'full_Hilbert_stress_qualified', 'normal_reactions_solved',
    'S_cross_reduction_qualified', 'source_history_registered', 'galaxy_force_qualified')}

def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(1048576), b''): h.update(b)
    return h.hexdigest()

def packed(x):
    if isinstance(x, F): return {'numerator': x.numerator, 'denominator': x.denominator}
    if isinstance(x, dict):
        if all(isinstance(k, str) for k in x): return {k: packed(v) for k, v in x.items()}
        return [{'key': packed(k), 'value': packed(v)} for k, v in sorted(x.items())]
    if isinstance(x, (list, tuple)): return [packed(v) for v in x]
    return x

def encoded(x): return (json.dumps(packed(x), sort_keys=True, indent=2, allow_nan=False) + '\n').encode()

def publish(name, x):
    p = J / name; b = encoded(x)
    with p.open('xb') as f: f.write(b); f.flush(); os.fsync(f.fileno())
    if p.read_bytes() != b: raise RuntimeError('Publication reread: ' + name)
    p.chmod(0o444); OUTPUTS[name] = sha(p)
    return {'file': name, 'sha256': OUTPUTS[name]}

def checkpoint(kind, x, owner, pins):
    payload = {'owner': owner, 'pins': pins, 'kind': kind, 'payload': x}
    ref = publish(STEM + '_' + kind + '.json', payload)
    commit = {'file': ref['file'], 'sha256': ref['sha256'], 'owner': owner, 'pins': pins, 'status': 'SEALED_ARITHMETIC_OPERANDS'}
    cr = publish(ref['file'] + '.COMMIT.json', commit)
    rec = {**ref, 'commit_file': cr['file'], 'commit_sha256': cr['sha256']}
    RECORDS.append((rec, json.loads(encoded(payload)), json.loads(encoded(commit))))
    return rec

def verify():
    for n, h in {**PINS, PROTOCOL: PROTOCOL_SHA}.items():
        if sha(J / n) != h: raise RuntimeError('Input bytes: ' + n)

def recheck(owner, strict=True):
    verify()
    if sha(J / SOURCE) != owner['source_sha256']: raise RuntimeError('Executing source changed')
    for n, h in OUTPUTS.items():
        if sha(J / n) != h: raise RuntimeError('Own output changed: ' + n)
    for rec, payload, commit in RECORDS:
        if json.loads((J / rec['file']).read_text()) != payload or json.loads((J / rec['commit_file']).read_text()) != commit:
            raise RuntimeError('Complete pair payload/commit schema')
    if strict and {p.name for p in J.glob(STEM + '_*.json')} != set(OUTPUTS):
        raise RuntimeError('Own file census')

def check(name, actual, expected):
    RAW['current_control'] = {'ordinal': len(CHECKS), 'name': name, 'actual': actual, 'expected': expected}
    record = {'ordinal': len(CHECKS), 'name': name, 'passed': actual == expected,
              'actual': actual, 'expected': expected}
    CHECKS.append(record)
    if not record['passed']: raise ArithmeticError('Exact coefficient/jet control: ' + name)

def add(d, k, v):
    z = d.get(k, F(0)) + v
    if z: d[k] = z
    else: d.pop(k, None)

def diag_add(a, b, scale=F(1)):
    out = dict(a)
    for k, v in b.items(): add(out, k, scale * v)
    return out

def diag_product(a, b):
    out = {}
    for (zi, zr, pa), va in a.items():
        for (zj, zs, pb), vb in b.items():
            if pa != '1' or pb != '1': raise RuntimeError('Unowned parameter product')
            add(out, (zi ^ zj, zr ^ zs, '1'), va * vb)
    return out

def cap_occupation(v, incident):
    c = {(0, 0, '1'): F(-2)}
    for e in incident: c = diag_add(c, {(0, 0, '1'): F(1, 2), (1 << e, 0, '1'): F(-1, 2)})
    q = {(0, 0, '1'): F(1, 2), (0, 1 << v, '1'): F(-1, 2)}
    out = diag_add(diag_product(c, c), diag_product(q, c), F(-1, 2))
    return diag_add(out, {(0, 0, 'AR'): F(1, 2), (0, 1 << v, 'AR'): F(-1, 2), (0, 0, 'Sself'): F(1)})

def cap_closed(v, incident):
    out = {(0, 0, '1'): F(1), (0, 0, 'AR'): F(1, 2), (0, 1 << v, 'AR'): F(-1, 2), (0, 0, 'Sself'): F(1)}
    for e, f in itertools.combinations(incident, 2): add(out, ((1 << e) ^ (1 << f), 0, '1'), F(1, 2))
    for e in incident:
        add(out, (1 << e, 0, '1'), F(1, 8)); add(out, (1 << e, 1 << v, '1'), F(-1, 8))
    return out

def edge_operator(e, a, b, scale):
    out = {}
    for k in (a, b):
        add(out, (0, 0, 0, 0, k, k, '1'), scale * F(1, 8))
        add(out, (1 << e, 0, 0, 0, k, k, '1'), -scale * F(1, 8))
    for k, l in ((a, b), (b, a)):
        add(out, (0, 0, 0, 0, k, l, '1'), -scale * F(1, 20))
        add(out, (1 << e, 0, 0, 0, k, l, '1'), scale * F(1, 20))
    for k in range(54): add(out, (0, 1 << e, 0, 0, k, k, '1'), -scale * F(1, 5))
    return out

def node_operator(v, cap, edges, incident):
    out = {}
    for (zi, zr, parameter), value in cap.items():
        for k in range(54): add(out, (zi, 0, zr, 0, k, k, parameter), value)
    add(out, (0, 0, 0, 0, v, v, '1'), F(1))
    add(out, (0, 0, 0, 1 << v, v, v, 'g'), F(1))
    for e in incident:
        for k, value in edge_operator(e, *edges[e], F(1, 2)).items(): add(out, k, value)
    return out

def old_graph():
    coords = tuple(itertools.product(range(3), repeat=3))
    index = {r: i for i, r in enumerate(coords)}
    shifts = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
    edges = tuple((i, 27 + index[tuple((r[k] + s[k]) % 3 for k in range(3))])
                  for i, r in enumerate(coords) for s in shifts)
    anchors = tuple(index[r] for r in ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)))
    return edges, tuple(4 * a for a in anchors)

# Exact Taylor polynomials in p,q through TOTAL degree two; coefficients are not derivatives.
def poly(x): return {(0, 0): F(x)} if x else {}
def padd(a, b, scale=F(1)):
    o = dict(a)
    for k, v in b.items(): add(o, k, scale * v)
    return o
def pmul(a, b):
    o = {}
    for (i, j), x in a.items():
        for (k, l), y in b.items():
            if i + j + k + l <= 2: add(o, (i + k, j + l), x * y)
    return o
def pscale(a, s): return {k: v * s for k, v in a.items() if v * s}
def mm(a, b):
    return [[sum_poly(pmul(a[i][k], b[k][l]) for k in range(len(b))) for l in range(len(b[0]))] for i in range(len(a))]
def mv(a, v): return [sum_poly(pmul(x, y) for x, y in zip(row, v)) for row in a]
def sum_poly(seq):
    o = {}
    for x in seq: o = padd(o, x)
    return o
def pdot(a, b, signs=None):
    return sum_poly(pscale(pmul(x, y), s) for x, y, s in zip(a, b, signs or [1] * len(a)))
def jet(sigma):
    delta = dict(sigma); delta.pop((0, 0), None)
    expjet = padd(padd(poly(1), delta), pmul(delta, delta), F(1, 2))
    return [expjet.get((1, 0), F(0)), expjet.get((0, 1), F(0)),
            2 * expjet.get((2, 0), F(0)), expjet.get((1, 1), F(0)), 2 * expjet.get((0, 2), F(0))]

def geometry(positions):
    p, q = {(1, 0): F(1)}, {(0, 1): F(1)}; p2 = pmul(p, p)
    signs = [-1, 1, 1, 1]; eye = [[poly(i == k) for k in range(4)] for i in range(4)]
    boost = [[dict(x) for x in row] for row in eye]
    boost[0][0] = boost[1][1] = padd(poly(1), p2, F(1, 2)); boost[0][1] = boost[1][0] = p
    frame = [mv(boost, [poly(i == k) for i in range(4)]) for k in range(4)]
    unit_actual = [[pdot(a, b, signs) for b in frame] for a in frame]
    unit_expected = [[poly(signs[i] if i == k else 0) for k in range(4)] for i in range(4)]
    check('boost_unit_and_triad_first_second_jets', unit_actual, unit_expected)
    a0 = [F(1), F(2), F(3)]
    boost_rows, coframe_rows, metric_rows, proper_rows, pi_rows, gamma_rows = [], [], [], [], [], []
    acceleration_actual, acceleration_expected = [], []
    RAW['geometry'] = {'boost': boost, 'positions_scaled_sqrt3': positions, 'boost_rows': boost_rows,
        'coframe_rows': coframe_rows, 'metric_rows': metric_rows, 'proper_rows': proper_rows,
        'acceleration_actual': acceleration_actual, 'acceleration_expected': acceleration_expected,
        'unit_actual': unit_actual, 'unit_expected': unit_expected, 'Pi_U_rows': pi_rows, 'connection_rows': gamma_rows}
    strain = []
    for i in range(3):
        for k in range(i, 3): strain.append([[F(int((a == i and b == k) or (a == k and b == i))) for b in range(3)] for a in range(3)])
    for r in positions:
        R = mv(boost, [poly(0)] + [poly(x) for x in r])
        for direction in range(3):
            av = [padd(poly(a0[i]), q if i == direction else {}) for i in range(3)]
            # Independent time-generator route: U(p,t)=L(p) exp[t K(a0+q e_direction)] U0.
            K = [[{} for _ in range(4)] for _ in range(4)]
            for i in range(3): K[0][i + 1] = K[i + 1][0] = av[i]
            acc = mv(boost, mv(K, [poly(1), {}, {}, {}]))
            expected_acc = [pscale(p, a0[0]) if direction != 0 else padd(pscale(p, a0[0]), pmul(p, q)),
                padd(padd(poly(a0[0]), q if direction == 0 else {}), p2, a0[0] / 2), av[1], av[2]]
            acceleration_actual.append(acc); acceleration_expected.append(expected_acc)
            js = jet(pdot(acc, R, signs))
            boost_rows.append({'r': r, 'direction': direction, 'sigma': pdot(acc, R, signs), 'actual_jet': js,
                'expected_jet': [F(0), F(r[direction]), F(0), F(0), F(r[direction] ** 2)]})
            for i in range(3):
                for k in range(3):
                    Rc = [poly(x) for x in r]; Rc[i] = padd(Rc[i], p, r[k])
                    sc = pdot(av, Rc)
                    actual = jet(sc)[3]
                    expected = F(int(direction == i) * r[k]) + F(r[direction]) * a0[i] * r[k]
                    coframe_rows.append([r, direction, i, k, actual, expected])
            for S in strain:
                S2 = [[sum(S[i][k] * S[k][l] for k in range(3)) for l in range(3)] for i in range(3)]
                metric = [[padd(poly(i == k), p, S[i][k]) for k in range(3)] for i in range(3)]
                e = [[padd(padd(poly(i == k), p, -S[i][k] / 2), p2, 3 * S2[i][k] / 8) for k in range(3)] for i in range(3)]
                Rc = mv(e, [poly(x) for x in r]); sc = pdot(av, mv(metric, Rc))
                sr = [sum(S[i][k] * r[k] for k in range(3)) for i in range(3)]
                expected = sr[direction] / 2 + F(r[direction]) * sum(a0[i] * sr[i] for i in range(3)) / 2
                metric_rows.append([r, direction, S, jet(sc)[3], expected])
                sp = pdot(mv(e, av), mv(metric, Rc))
                proper_rows.append([r, direction, S, jet(sp), [F(0), F(r[direction]), F(0), F(0), F(r[direction] ** 2)]])
        # Off-shell held-field derivative, evaluated at one exact rational Lorentz frame; not a physical seed.
        U = [F(5, 3), F(4, 3), F(0), F(0)]
        R = [F(4, 3) * r[0], F(5, 3) * r[0], F(r[1]), F(r[2])]
        Rlow = [s * x for s, x in zip(signs, R)]
        pi_first = {}
        for nu in range(4):
            for mu in range(4):
                A = [[{} for _ in range(4)] for _ in range(4)]; A[nu][mu] = p
                acc = [sum_poly(pscale(A[k][i], U[k]) for k in range(4)) for i in range(4)]
                values = jet(pdot([poly(x) for x in Rlow], acc)); actual = [values[0], values[2]]
                coefficient = U[nu] * Rlow[mu]; pi_first[nu, mu] = actual[0]
                pi_rows.append([r, nu, mu, actual, [coefficient, coefficient ** 2]])
        for mu in range(4):
            for nu in range(4):
                for rho in range(nu, 4):
                    Gamma = [[[{} for _ in range(4)] for _ in range(4)] for _ in range(4)]
                    Gamma[mu][nu][rho] = p; Gamma[mu][rho][nu] = p
                    acc = [sum_poly(pscale(Gamma[i][k][l], U[k] * U[l]) for k in range(4) for l in range(4)) for i in range(4)]
                    values = jet(pdot([poly(x) for x in Rlow], acc)); direct = [values[0], values[2]]
                    pulled = pi_first[nu, mu] * U[rho] + (pi_first[rho, mu] * U[nu] if nu != rho else 0)
                    gamma_rows.append([r, mu, nu, rho, direct, [pulled, pulled ** 2]])
    check('time_generator_acceleration_jets', acceleration_actual, acceleration_expected)
    check('coframe_acceleration_mixed_Born_chain', [x[-2] for x in coframe_rows], [x[-1] for x in coframe_rows])
    check('orthonormal_metric_fixed_contravariant_acceleration_chain', [x[-2] for x in metric_rows], [x[-1] for x in metric_rows])
    check('orthonormal_metric_fixed_proper_acceleration_chain', [x[-2] for x in proper_rows], [x[-1] for x in proper_rows])
    check('boost_first_source_Ward', [x['actual_jet'][0] for x in boost_rows], [F(0)] * len(boost_rows))
    check('boost_second_source_Ward', [x['actual_jet'][2] for x in boost_rows], [F(0)] * len(boost_rows))
    check('boost_time_source_mixed_Ward', [x['actual_jet'][3] for x in boost_rows], [F(0)] * len(boost_rows))
    check('unchanged_proper_acceleration_contact_under_boost', [[x['actual_jet'][1], x['actual_jet'][4]] for x in boost_rows],
        [[x['expected_jet'][1], x['expected_jet'][4]] for x in boost_rows])
    check('independent_U_derivative_momentum', [x[-2] for x in pi_rows], [x[-1] for x in pi_rows])
    check('metric_connection_pullback_from_Pi_U', [x[-2] for x in gamma_rows], [x[-1] for x in gamma_rows])
    return RAW['geometry']

def execute(owner, pins):
    old = ast.parse((J / 'local_record_feedback_q4_sparse_insertion_verification_v001.py').read_text())
    this = ast.parse((J / SOURCE).read_text())
    od = next(x for x in old.body if isinstance(x, ast.FunctionDef) and x.name == 'old_graph')
    nd = next(x for x in this.body if isinstance(x, ast.FunctionDef) and x.name == 'old_graph')
    if ast.dump(od, include_attributes=False) != ast.dump(nd, include_attributes=False): raise RuntimeError('Literal old graph AST')
    edges, cuts = old_graph(); incidents = [[e for e, pair in enumerate(edges) if v in pair] for v in range(54)]
    RAW['graph'] = {'edges': edges, 'incidents': incidents, 'cuts': cuts}
    check('actual_54_108_degree4_graph', [len(edges), len(set(edges)), len(incidents), [len(x) for x in incidents]], [108, 108, 54, [4] * 54])
    caps, closed, nodes, global_from_nodes, global_direct = [], [], [], {}, {}
    RAW['operators'] = {'occupation_caps': caps, 'closed_caps': closed, 'nodes': nodes,
                        'sum_owned_nodes': global_from_nodes, 'direct_whole_H': global_direct}
    for v, incident in enumerate(incidents):
        ca = cap_occupation(v, incident); caps.append(ca); closed.append(cap_closed(v, incident))
        node = node_operator(v, ca, edges, incident); nodes.append(node)
        for k, value in node.items(): add(global_from_nodes, k, value)
        for (zi, zr, parameter), value in cap_closed(v, incident).items():
            for k in range(54): add(global_direct, (zi, 0, zr, 0, k, k, parameter), value)
        add(global_direct, (0, 0, 0, 0, v, v, '1'), F(1)); add(global_direct, (0, 0, 0, 1 << v, v, v, 'g'), F(1))
    for e, (a, b) in enumerate(edges):
        for k, value in edge_operator(e, a, b, F(1)).items(): add(global_direct, k, value)
    check('full_cap_operator_occupation_vs_Pauli', caps, closed)
    check('every_endpoint_once_full_H', global_from_nodes, global_direct)
    terms_ref = checkpoint('TERMS', RAW['operators'], owner, pins)
    n = ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))
    cells = tuple(itertools.product(range(3), repeat=3))
    A = [tuple(sum(r[i] * (n[i + 1][k] - n[0][k]) for i in range(3)) for k in range(3)) for r in cells]
    positions = A + [tuple(a[k] + n[0][k] for k in range(3)) for a in A]
    mean_rows = []
    for a, b in edges:
        for i in range(3):
            for k in range(3):
                direct = F(positions[a][i] * positions[a][k] + positions[b][i] * positions[b][k], 2)
                mean = F(positions[a][i] + positions[b][i], 2) * F(positions[a][k] + positions[b][k], 2)
                spread = F((positions[a][i] - positions[b][i]) * (positions[a][k] - positions[b][k]), 4)
                mean_rows.append([a, b, i, k, direct, mean + spread, mean, spread])
    RAW['endpoint_product_rows'] = mean_rows
    check('endpoint_second_contact_mean_plus_spread', [x[4] for x in mean_rows], [x[5] for x in mean_rows])
    geo = geometry(positions)
    geometry_ref = checkpoint('GEOMETRY', {'graph': RAW['graph'], 'endpoint_product_rows': mean_rows, **geo}, owner, pins)
    if len(CHECKS) != CONTROL_COUNT: raise RuntimeError('Fixed exact control census')
    controls_ref = checkpoint('CONTROLS', CHECKS, owner, pins)
    return [terms_ref, geometry_ref, controls_ref], {'nodes': 54, 'links': 108, 'source_axes': 3,
        'node_operator_entries': sum(len(x) for x in nodes), 'whole_operator_entries': len(global_direct), 'controls': len(CHECKS)}

def main():
    ap = argparse.ArgumentParser(description=__doc__); ap.add_argument('--root-execute', action='store_true'); args = ap.parse_args()
    if AUTHOR_DRAFT or not args.root_execute or sys.platform != 'darwin' or Path(__file__).resolve() != J / SOURCE:
        raise RuntimeError('Held draft or actual root Mac/source context refused')
    if any(p.name != PROTOCOL for p in J.glob(STEM + '*')): raise FileExistsError('Unused own namespace required')
    verify(); owner = {'owner': 'root', 'pid': os.getpid(), 'started': datetime.now(timezone.utc).isoformat(), 'source_sha256': sha(J / SOURCE)}
    pins = {**PINS, PROTOCOL: PROTOCOL_SHA, SOURCE: owner['source_sha256']}
    try:
        publish(STEM + '_OWNER_START.json', owner)
        publish(STEM + '_MANIFEST.json', {'owner': owner, 'inputs': pins, 'control_count': CONTROL_COUNT,
            'preparation': None, 'history': None, 'material_flow': None,
            'downstream_material_scope': 'independent normalized rotation-capable flow of extension110; no scalar-normal material clock instantiated',
            'Eunit': 'symbolic', 'ell': 'symbolic', 'V': 'symbolic', 'physical_flags': FLAGS})
        refs, census = execute(owner, pins)
        result = {'status': 'CONDITIONAL_OPERATOR_JET_PASS', 'owner': owner, 'inputs': pins, 'pairs': refs,
            'census': census, 'controls': [{'ordinal': x['ordinal'], 'name': x['name'], 'passed': x['passed']} for x in CHECKS],
            'units': {'positions': 'sqrt(3)*R/ell', 'operator': 'H/Eunit', 'first_acceleration': 'restore ell/sqrt(3)',
                      'second_acceleration': 'restore ell^2/3', 'density': 'divide by supplied V only'},
            'scope': 'exact coefficient/source chains only; no prepared state, stress solution, force, kernel or physical normalization', 'physical_flags': FLAGS}
        rr = publish(STEM + '_RESULT.json', result); recheck(owner)
        receipt = {'status': 'CLOSED', 'owner': owner, 'closed': datetime.now(timezone.utc).isoformat(), 'input_sha256': pins,
                   'output_sha256': dict(OUTPUTS), 'result_sha256': rr['sha256'], 'physical_flags': FLAGS}
        publish(STEM + '_RECEIPT.json', receipt); recheck(owner)
        print(json.dumps({'status': result['status'], 'controls': len(CHECKS), 'result_sha256': rr['sha256']}))
    except BaseException:
        trace = traceback.format_exc(); preservation = None
        try: checkpoint('ERROR_RAW', {'available_raw': RAW, 'all_available_controls': CHECKS}, owner, pins)
        except BaseException: preservation = traceback.format_exc()
        actual = {}
        for p in sorted(J.glob(STEM + '_*.json')):
            p.chmod(0o444); actual[p.name] = sha(p)
        prior = J / (STEM + '_RECEIPT.json')
        error = {'status': 'CLOSED_ERROR', 'owner': owner, 'traceback': trace, 'raw_preservation_traceback': preservation,
            'preserved_outputs': actual, 'unqualified_files': sorted(set(actual) - set(OUTPUTS)),
            'prior_receipt': {'file': prior.name, 'sha256': sha(prior)} if prior.exists() else None,
            'completed_controls': [{'ordinal': x['ordinal'], 'name': x['name'], 'passed': x['passed']} for x in CHECKS], 'physical_flags': FLAGS}
        er = publish(STEM + '_ERROR.json', error)
        if not prior.exists(): publish(STEM + '_RECEIPT.json', {'status': 'CLOSED_ERROR', 'owner': owner,
            'closed': datetime.now(timezone.utc).isoformat(), 'input_sha256': pins, 'output_sha256': {**actual, **OUTPUTS},
            'error_sha256': er['sha256'], 'physical_flags': FLAGS})
        raise

if __name__ == '__main__': main()

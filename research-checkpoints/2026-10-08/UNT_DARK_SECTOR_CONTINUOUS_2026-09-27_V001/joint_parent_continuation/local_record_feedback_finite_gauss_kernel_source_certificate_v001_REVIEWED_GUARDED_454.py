"""Prospective finite circuit/Gauss implementation certificate; root execution only."""
import argparse
import ast
from datetime import datetime, timezone
from functools import lru_cache
import hashlib
import io
import itertools
import json
import os
from pathlib import Path
import time
import traceback

AUTHOR_DRAFT = True
J = Path(__file__).resolve().parent
STEM = 'LOCAL_RECORD_FEEDBACK_FINITE_GAUSS_KERNEL_SOURCE_CERTIFICATE_V001'
PROTOCOL = STEM + '.md'
CP = J / 'local_record_feedback_finite_gauss_kernel_source_certificate_v001_checkpoints'
DONOR = 'LOCAL_RECORD_FEEDBACK_DONOR_DRESSED_Q4_SOURCE_CHECK_V001'
OLD = 'local_record_feedback_q4_sparse_insertion_verification_v001.py'
DONOR_SOURCE = 'local_record_feedback_donor_dressed_q4_source_check_v001.py'
C8 = 'FLOATING_RETURN_C8_FORMATION_CLOCK_V001_RESULT.json'
PINS = {'LOCAL_RECORD_FEEDBACK_IDEAL_PLATE_TEM_GAUSS_CONSTRUCTOR_V001.md': '1fbfcea0364eafeabe386da930784099aeab85a00e25b460e32e6b217705cec7', 'LOCAL_RECORD_FEEDBACK_FIVE_ISLAND_PASSIVE_COMPLETION_V001.md': '124f68b600130afcb3935e11c43c1f939a804892b2794c25f89c29a0892f8693', 'LOCAL_RECORD_FEEDBACK_FLOATING_RETURN_COMPLETION_V001.md': '255ea0ca5f86cc711cae2ff5e746d8e9b005c2156b934818ded7789f9461f2a4', 'LOCAL_RECORD_FEEDBACK_Z_DEPENDENT_DONOR_CAPACITANCE_CONTACTS_V001.md': '004d3ed8e392fda31bdd0481b4ed5f5fed571566398e6671d6fdb41ffbe8c8a1', 'local_record_feedback_q4_sparse_insertion_verification_v001.py': '774c81de75458fb430009655f83f00dcc24bac423385ac1b72409dc6f160134e', 'local_record_feedback_donor_dressed_q4_source_check_v001.py': '15da2a9749633a12269eb278fda98efa718bdb90cedf95fcf94793faf3c609c3', 'LOCAL_RECORD_FEEDBACK_DONOR_DRESSED_Q4_SOURCE_CHECK_V001.md': 'd33ca57880e3e07eead44bcc9211cbd84a6733490dbf0fb0d62334b40af9e95b', 'LOCAL_RECORD_FEEDBACK_DONOR_DRESSED_Q4_SOURCE_CHECK_V001_RESULT.json': 'f457c9a558bf9816ec29054da41c6a353148decee37041ba2c58f55ff5af25a7', 'LOCAL_RECORD_FEEDBACK_DONOR_DRESSED_Q4_SOURCE_CHECK_V001_RECEIPT.json': '54cd3eb595cfcf3f1988e0660eb6143a111b357afda035e3f37b305b3e33fe14', 'FLOATING_RETURN_C8_RETAINED_RECORD_GEOMETRY_V001.md': '8f3dc32381e76a4e6badfe23fff6c8bdd4830cb32ed0aff99b1aef57eba5ce5b', 'FLOATING_RETURN_C8_FORMATION_CLOCK_V001_RESULT.json': '08ec6908d430536cf64fa5d1445e8ae95831515a5dfbdb9c318c029ab6409a43', 'UNIFIED_RECORD_BIRTH_MAXWELL_DEBIT_AND_SOURCE_CONTACTS_V001.md': '9c65b7a1b7e3b1b32de7d8691e4612312a6a401c15ede9005a4966a0e6e72a1f', 'LOCAL_RECORD_FEEDBACK_FINITE_GAUSS_KERNEL_SOURCE_CERTIFICATE_V001.md': '84147e757d65253726667fa425c1b4bdd782cadd2206e6693b5e7e3428ea6b58'}
AR = (1 / 8, 7 / 40, 1 / 4)
KAPPA = (0., -.001, .001)
TOL = 1e-11
PHYSICAL = {k: False for k in ('physical_charge_or_unit_selected', 'physical_geometry_selected',
    'physical_chi_or_Wilson_path_selected', 'Maxwell_frequency_projection_certified',
    'auxiliary_state_or_preparation_selected', 'full_quantum_birth_intertwiner_certified',
    'physical_dilation_or_Hilbert_source_certified', 'thermal_or_inflation_result',
    'macroscopic_phase_or_galaxy_match')}
KERNEL_KEYS = ('passive', 'zero_branches', 'C5_inverse', 'Cfull_null', 'relative_direct_sum', 'cycle_null',
    'cycle_count', 'canonical', 'longitudinal_orthogonality', 'TEM_reciprocity', 'positive_forms')
MAP_KEYS = ('literal_port_map', 'retained_branch_chain', 'new_star_count')
ROW_KEYS = ('old_neutral', 'new_neutral', 'old_Gauss', 'new_Gauss', 'old_polynomial',
    'new_polynomial', 'uniform_dlong', 'uniform_dlong_new', 'source_intertwining', 'first_inverse', 'mixed_inverse',
    'cycle_source', 'cycle_mixed', 'magnetic_inverse_source', 'magnetic_inverse_mixed', 'canonical_source',
    'tree_charge_chain', 'arbitrary_cycle_family',
    'donor_signed_debit', 'donor_Gauss', 'donor_chain', 'donor_first_source', 'donor_mixed_source',
    'record_return', 'partial_isometry', 'saved_copy_channels')
CONTEXT, RAW, PARTIAL = {}, {}, []


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def utc():
    return datetime.now(timezone.utc).isoformat()


def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def exclusive(p, b):
    with Path(p).open('xb') as f:
        f.write(b)
        f.flush()
        os.fsync(f.fileno())
    Path(p).chmod(0o444)
    return hashlib.sha256(b).hexdigest()


def verify(pins):
    for n, h in pins.items():
        assert isinstance(n, str) and len(h) == 64 and sha(J / n) == h, ('input_seal', n)


def donor_closed():
    receipt = json.loads((J / (DONOR + '_RECEIPT.json')).read_text())
    assert receipt['status'] == 'CLOSED' and receipt['owner']['pid'] > 0
    verify(receipt['pins'])
    verify(receipt['outputs'])
    verify(receipt['checkpoint_outputs'])
    result = json.loads((J / (DONOR + '_RESULT.json')).read_text())
    assert result['pins'] == receipt['pins'] and result['status'] == 'EXACT_DONOR_DRESSED_SOURCE_CHECKS_PASSED'
    assert result['census']['total_predicates'] == 93210 and len(result['groups']) == 6
    for group in result['groups']:
        assert len(group['payload']['rows']) == 1536
        assert all(len(r['controls']) == 9 and all(v is True for v in r['controls'].values())
                   for r in group['payload']['rows'])
    assert all(v is False for v in result['qualification'].values())
    owner_path = CP.parent / 'local_record_feedback_donor_dressed_q4_source_check_v001_checkpoints' / 'OWNER_START.json'
    assert json.loads(owner_path.read_text()) == {'owner': receipt['owner'], 'pins': receipt['pins']}
    for group in result['groups'] + [result['source_contacts'], result['leakage_grams']]:
        path = owner_path.parent / (group['name'] + '.json')
        assert json.loads(path.read_text()) == group
        assert json.loads(path.with_name(path.name + '.COMMIT.json').read_text()) == {
            'checkpoint': path.name, 'sha256': sha(path), 'pins': receipt['pins'],
            'owner': receipt['owner'], 'status': 'EXACT_CHECKS_PASSED'}
    return result, {**receipt['pins'], **receipt['outputs'], **receipt['checkpoint_outputs']}


def geometry():
    """Only pinned literal graph/isometry definitions; no producer main/import."""
    tree = ast.parse((J / OLD).read_text())
    names = ('old_graph', 'Inclusion', 'degrees')
    nodes = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names]
    assert tuple(n.name for n in nodes) == names
    env = {'itertools': itertools, 'lru_cache': lru_cache}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(J / OLD), 'exec'), env)
    source = ast.parse((J / DONOR_SOURCE).read_text())
    required = ('eta', 'record_k', 'neutral', 'lower', 'F', 'T', 'Tad')
    chosen = [n for n in source.body if isinstance(n, ast.FunctionDef) and n.name in required]
    assert tuple(n.name for n in chosen) == required
    exec(compile(ast.Module(body=chosen, type_ignores=[]), str(J / DONOR_SOURCE), 'exec'), env)
    edges, cuts = env['old_graph']()
    inc = env['Inclusion'](2, edges, cuts)
    assert cuts == (0, 36, 12, 4) and (len(edges), len(inc.edges), inc.vertices) == (108, 112, 56)
    return inc, env


def error(a, b):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    assert np.all(np.isfinite(a)) and np.all(np.isfinite(b)), 'nonfinite_arithmetic'
    return float(np.max(np.abs(a - b), initial=0.)), float(max(1., np.max(np.abs(a), initial=0.),
                                                            np.max(np.abs(b), initial=0.)))


def check(flags, name, a, b):
    e, scale = error(a, b)
    flags[name] = {'pass': bool(e <= TOL * scale), 'absolute_error': e, 'scale': scale}
    assert flags[name]['pass'], (name, e, scale)


def star(ar):
    """Dimensionless arithmetic member: q*=qR=1, ed=em=.5, g=.25."""
    ed, em, g, er = .5, .5, .25, 2 * ar
    r, sr = ed + 4 * em, er - 4 * g * g / (ed + 4 * em)
    weights = ((em * er - g * g) / (ed * r * sr), g / (r * sr),
               (er - g) / (r * sr), (r - 4 * g) / (r * sr))
    assert sr > 0 and all(v >= 0 for v in weights)
    E = np.zeros((5, 5)); E[:4, :4] = ed * np.eye(4) + em
    E[:4, 4] = g; E[4, :4] = g; E[4, 4] = er
    pairs = [(a, b, 'port_port', weights[0]) for a in range(4) for b in range(a + 1, 4)]
    pairs += [(a, 4, 'port_record', weights[1]) for a in range(4)]
    pairs += [(a, 5, 'port_return', weights[2]) for a in range(4)]
    pairs += [(4, 5, 'record_return', weights[3])]
    zero = [(a, b, label) for a, b, label, value in pairs if value == 0.]
    pairs = [(a, b, label, value) for a, b, label, value in pairs if value > 0.]
    D = np.zeros((6, len(pairs))); c = np.array([p[3] for p in pairs])
    for e, (a, b, _, _) in enumerate(pairs): D[a, e], D[b, e] = -1., 1.
    tree = [e for e, p in enumerate(pairs) if p[2] in ('port_record', 'record_return')]
    chords = [e for e in range(len(pairs)) if e not in tree]
    assert len(tree) == 5
    R = np.zeros((len(pairs), len(chords))); R[chords, np.arange(len(chords))] = 1.
    R[tree] = -np.linalg.solve(D[:5, tree], D[:5, chords])
    Crel = (D[:5] * c) @ D[:5].T
    Ec = (R.T / c) @ R
    Lc = (R.T / c) @ R  # ell_b=c_p=1 arithmetic fixture, not physical adoption.
    Nc = (R / c[:, None]) @ np.linalg.solve(Ec, np.eye(len(chords)))
    RAW.update(E=E, D_local=D, c_local=c, R_local=R, Ec=Ec, Lc=Lc, Nc=Nc)
    chol = [np.linalg.cholesky(a) for a in (Crel, Ec, Lc)]
    return {'E': E, 'D': D, 'c': c, 'R': R, 'Crel': Crel, 'Ec': Ec, 'Lc': Lc, 'Nc': Nc,
            'pairs': pairs, 'zero': zero, 'tree': tree, 'chords': chords, 'chol': chol}


def network(edges, vertices, local):
    ports = [tuple(e for e, ab in enumerate(edges) if v in ab) for v in range(vertices)]
    assert all(len(p) == 4 for p in ports)
    ne = len(local['pairs']); D = np.zeros((5 * vertices + 1, ne * vertices))
    for v in range(vertices):
        indices = list(range(5 * v, 5 * v + 5)) + [5 * vertices]
        D[np.ix_(indices, range(ne * v, ne * (v + 1)))] = local['D']
    return {'ports': ports, 'D': D, 'c': np.tile(local['c'], vertices), 'vertices': vertices,
            'edges': edges, 'local': local}


def kernel_checks(net):
    a, V, D, c = net['local'], net['vertices'], net['D'], net['c']
    flags = {}; full = (D * c) @ D.T
    RAW.update(E=a['E'], D= D, c=c, Cfull=full, R_local=a['R'], Ec=a['Ec'], Lc=a['Lc'], Nc=a['Nc'])
    check(flags, 'passive', np.minimum(c, 0.), np.zeros_like(c))
    check(flags, 'zero_branches', len(a['zero']), 4 if AR_CURRENT == AR[0] else 0)
    check(flags, 'C5_inverse', a['Crel'] @ a['E'], np.eye(5))
    check(flags, 'Cfull_null', full @ np.ones(5 * V + 1), np.zeros(5 * V + 1))
    check(flags, 'relative_direct_sum', full[:-1, :-1], np.kron(np.eye(V), a['Crel']))
    check(flags, 'cycle_null', a['D'] @ a['R'], np.zeros((6, len(a['chords']))))
    check(flags, 'cycle_count', len(a['chords']), len(a['pairs']) - 6 + 1)
    check(flags, 'canonical', a['R'].T @ a['Nc'], np.eye(len(a['chords'])))
    check(flags, 'longitudinal_orthogonality', a['D'] @ (a['c'][:, None] * a['Nc']),
          np.zeros((6, len(a['chords']))))
    check(flags, 'TEM_reciprocity', a['c'] / a['c'], np.ones(len(a['c'])))
    check(flags, 'positive_forms', [float(np.min(np.diag(q))) > 0. for q in a['chol']], [True] * 3)
    assert set(flags) == set(KERNEL_KEYS)
    return flags


def port_map(inc, old, new):
    node = np.empty(5 * 54 + 1, dtype=np.int64)
    for v in range(54):
        for a, e in enumerate(old['ports'][v]):
            if e in inc.cuts:
                i = inc.cuts.index(e); child = inc.paths[i][0 if v == inc.endpoints[i][0] else 1]
            else: child = inc.keep.index(e)
            node[5 * v + a] = 5 * v + new['ports'][v].index(child)
        node[5 * v + 4] = 5 * v + 4
    node[-1] = 5 * 56
    lookup = {}
    for e in range(new['D'].shape[1]):
        a, b = np.flatnonzero(new['D'][:, e]); lookup[(int(a), int(b))] = e
    rows, signs = [], []
    mapped = np.zeros((len(node) + 10, old['D'].shape[1]))
    for e in range(old['D'].shape[1]):
        ab = np.flatnonzero(old['D'][:, e]); aa, bb = (int(node[v]) for v in ab)
        k = lookup[tuple(sorted((aa, bb)))]; source = int(np.flatnonzero(old['D'][:, e] < 0)[0])
        sign = -float(new['D'][node[source], k]); rows.append(k); signs.append(sign)
        mapped[:, e] = sign * new['D'][:, k]
    target = np.zeros_like(mapped); target[node] = old['D']
    flags = {}; check(flags, 'literal_port_map', len(set(node)), len(node))
    check(flags, 'retained_branch_chain', mapped, target)
    check(flags, 'new_star_count', new['vertices'] - old['vertices'], 2)
    return node, np.array(rows), np.array(signs), flags


def charge(net, state, env, Z):
    word, _, record, ret = state; V = net['vertices']; x = np.zeros((V, 5))
    for v in range(V):
        x[v, :4] = [env['eta'](v) * (1 - 2 * ((word >> e) & 1)) for e in net['ports'][v]]
        x[v, 4] = env['eta'](v) * ((record >> v) & 1)
    Q = np.r_[x.ravel(), float(ret)]
    potential = np.r_[(x @ net['local']['E'].T / Z).ravel(), 0.]
    d = Z * net['c'] * (net['D'].T @ potential)
    energy = float(Q @ potential / 2)
    degrees = env['degrees'](net['edges'], V, word)
    polynomial = sum((degrees[v] - 2) ** 2 - .5 * ((record >> v) & 1) * (degrees[v] - 2)
                     + AR_CURRENT * ((record >> v) & 1) + 1. for v in range(V)) / Z
    return Q, potential, d, energy, float(polynomial)


def cycle_vector(net, coefficients):
    V, a = net['vertices'], net['local']
    assert coefficients.shape == (V, len(a['chords']))
    return (coefficients @ a['R'].T).ravel()


def tree_chain(net, delta):
    V, a = net['vertices'], net['local']; w = np.zeros((V, len(a['pairs'])))
    w[:, a['tree']] = np.linalg.solve(a['D'][:5, a['tree']], delta[:-1].reshape(V, 5).T).T
    return w.ravel()


def charge_rows(inc, env, old, new, node, ar, kappa, native_rows):
    records = []; RAW.clear(); PARTIAL.clear(); arrays = RAW
    a = old['local']; E, R, c = a['E'], a['R'], a['c']
    for bg in range(3):
        base = sum(1 << e for e in inc.keep if bg == 1 or bg == 2 and e % 2 == 0)
        for cut in range(16):
            word = base | sum(((cut >> i) & 1) << e for i, e in enumerate(inc.cuts))
            for occupied in (0, 1):
                s = (word, 0, occupied, -occupied); f = env['F'](inc, s); t = env['T'](inc, s)
                O, Ox, Oy = float(cut & 1), float(cut & 1), float((cut >> 1) & 1)
                Z = 1. + kappa * O; assert Z > 0
                newO = sum((f[0] >> e) & 1 for e in inc.paths[0]) / 2
                before = charge(old, s, env, Z); plain = charge(new, f, env, Z)
                after = charge(new, t, env, Z) if t is not None else None
                Q0, phi0, d0, en0, p0 = before
                Q1, phi1, d1, en1, p1 = plain
                qmap = np.zeros_like(Q1); qmap[node] = Q0
                delta = Q1 - qmap; w = tree_chain(new, delta)
                zeta = ((np.arange(56 * len(new['local']['chords'])) % 3) - 1).reshape(56, -1)
                wz = w + cycle_vector(new, zeta)
                prefix = 'r' + str(len(records)) + '_'
                vals = {'Q_before': Q0, 'phi_before': phi0, 'd_before': d0, 'Q_F2': Q1,
                        'phi_F2': phi1, 'd_F2': d1, 'charge_map': qmap, 'delta_Q': delta,
                        'w_tree': w, 'zeta_fixture': zeta, 'w_cycle_fixture': wz}
                if after is not None:
                    wt = tree_chain(new, after[0] - qmap)
                    vals.update(Q_after=after[0], phi_after=after[1], d_after=after[2], w_donor=wt)
                arrays.update({prefix + n: value for n, value in vals.items()})
                CONTEXT.update(background=bg, cut_word=cut, donor_occupied=occupied)
                flags = {}; CONTEXT['current_controls'] = flags
                check(flags, 'old_neutral', np.sum(Q0), 0.)
                check(flags, 'new_neutral', np.sum(Q1), 0.)
                check(flags, 'old_Gauss', old['D'] @ d0, Q0)
                check(flags, 'new_Gauss', new['D'] @ d1, Q1)
                check(flags, 'old_polynomial', en0, p0); check(flags, 'new_polynomial', en1, p1)
                check(flags, 'uniform_dlong', d0, charge(old, s, env, 1.)[2])
                check(flags, 'uniform_dlong_new', d1, charge(new, f, env, 1.)[2])
                check(flags, 'source_intertwining', newO, O)
                Crel = a['Crel'] * Z; K = E / Z; Cx, Cy = a['Crel'] * Ox, a['Crel'] * Oy
                first = -K @ Cx @ K; mixed = K @ Cy @ K @ Cx @ K + K @ Cx @ K @ Cy @ K
                check(flags, 'first_inverse', first, -Ox * E / Z ** 2)
                check(flags, 'mixed_inverse', mixed, 2 * Ox * Oy * E / Z ** 3)
                Ec = a['Ec'] / Z; Ecx = -(R.T / c) @ R * Ox / Z ** 2
                check(flags, 'cycle_source', Ecx, -Ox * Ec / Z)
                Ecxy = 2 * Ox * Oy * (R.T / c) @ R / Z ** 3
                check(flags, 'cycle_mixed', Ecxy, 2 * Ox * Oy * Ec / Z ** 2)
                Li = np.linalg.solve(a['Lc'] / Z, np.eye(len(a['chords'])))
                Lx = -Ox * a['Lc'] / Z ** 2
                check(flags, 'magnetic_inverse_source', -Li @ Lx @ Li,
                      Ox * np.linalg.solve(a['Lc'], np.eye(len(a['chords']))))
                Ly = -Oy * a['Lc'] / Z ** 2; Lxy = 2 * Ox * Oy * a['Lc'] / Z ** 3
                check(flags, 'magnetic_inverse_mixed', Li @ Ly @ Li @ Lx @ Li + Li @ Lx @ Li @ Ly @ Li
                      - Li @ Lxy @ Li, np.zeros_like(Li))
                Eci = np.linalg.solve(Ec, np.eye(len(a['chords'])))
                Nc = (R / (Z * c[:, None])) @ Eci
                Ncx = (-Ox * R / (Z ** 2 * c[:, None])) @ Eci - (R / (Z * c[:, None])) @ Eci @ Ecx @ Eci
                check(flags, 'canonical_source', np.stack((Nc - a['Nc'], Ncx)), np.zeros((2,) + Nc.shape))
                arrays.update({prefix + 'first_inverse': first, prefix + 'mixed_inverse': mixed,
                               prefix + 'Ec_first': Ecx, prefix + 'Ec_mixed': Ecxy,
                               prefix + 'Linv_first': -Li @ Lx @ Li, prefix + 'Linv_mixed':
                               Li @ Ly @ Li @ Lx @ Li + Li @ Lx @ Li @ Ly @ Li - Li @ Lxy @ Li,
                               prefix + 'Nc': Nc, prefix + 'Nc_first': Ncx})
                check(flags, 'tree_charge_chain', new['D'] @ w, delta)
                check(flags, 'arbitrary_cycle_family', new['D'] @ wz, delta)
                rw = ar - .5 * (env['degrees'](inc.old, 54, word)[0] - 2)
                expected_delta = 2 * (sum((cut >> i) & 1 for i in range(4)) - 2) ** 2 + 2. - rw
                release = None if after is None else en0 - after[3]
                check(flags, 'donor_signed_debit', 0. if after is None else -release,
                      0. if after is None else expected_delta / Z)
                check(flags, 'donor_Gauss', np.zeros_like(Q1) if after is None else new['D'] @ after[2] - after[0],
                      np.zeros_like(Q1))
                check(flags, 'donor_chain', np.zeros_like(Q1) if after is None else new['D'] @ wt - (after[0] - qmap),
                      np.zeros_like(Q1))
                rx = None if after is None else float(-Ox * (Q0 @ phi0 - after[0] @ after[1]) / (2 * Z))
                rxy = None if after is None else float(Ox * Oy * (Q0 @ phi0 - after[0] @ after[1]) / Z ** 2)
                check(flags, 'donor_first_source', 0. if rx is None else rx, 0. if release is None else -Ox * release / Z)
                check(flags, 'donor_mixed_source', 0. if rxy is None else rxy,
                      0. if release is None else 2 * Ox * Oy * release / Z ** 2)
                check(flags, 'record_return', [t is None, 0 if t is None else t[3] - s[3]],
                      [not bool(occupied), occupied])
                check(flags, 'partial_isometry', t is None or env['Tad'](inc, t) == s, True)
                selected = [native_rows[(bg, cut, occupied, copy)] for copy in (0, 4)]
                check(flags, 'saved_copy_channels', [r['donor_occupied'] for r in selected], [bool(occupied)] * 2)
                assert set(flags) == set(ROW_KEYS)
                records.append({'background': bg, 'cut_word': cut, 'state': list(s), 'F2_state': list(f),
                    'T_state': None if t is None else list(t), 'kappa': kappa, 'O': O, 'Z': Z,
                    'source_x': Ox, 'source_y': Oy, 'energy_before': en0, 'energy_F2': en1,
                    'energy_after': None if after is None else after[3], 'released_storage': release,
                    'r_w': rw, 'source_release_x': rx, 'source_release_xy': rxy,
                    'blank_T_reason': 'ineligible_donor' if after is None else None,
                    'saved_copy_OFF_ON': selected, 'controls': flags})
                PARTIAL.append(records[-1])
    assert len(records) == 96
    return records, arrays


def checkpoint(name, records, arrays, pins, owner):
    assert all(isinstance(v, np.ndarray) and np.all(np.isfinite(v)) for v in arrays.values())
    meta = {'name': name, 'records': records, 'pins': pins, 'owner': owner, 'status': 'ARITHMETIC_PASS'}
    data = canonical(meta); meta = json.loads(data)
    arrays = dict(arrays); arrays['_metadata'] = np.frombuffer(data, dtype=np.uint8)
    buffer = io.BytesIO(); np.savez_compressed(buffer, **arrays)
    path = CP / (name + '.npz'); digest = exclusive(path, buffer.getvalue())
    commit = {'checkpoint': path.name, 'sha256': digest, 'pins': pins, 'owner': owner, 'status': meta['status']}
    exclusive(path.with_name(path.name + '.COMMIT.json'), canonical(commit))
    with np.load(path, allow_pickle=False) as reread:
        assert set(reread.files) == set(arrays)
        assert all(np.array_equal(reread[k], v) for k, v in arrays.items())
        assert json.loads(reread['_metadata'].tobytes()) == meta
    assert json.loads(path.with_name(path.name + '.COMMIT.json').read_text()) == commit
    return {'checkpoint': path.name, 'sha256': digest, 'commit': path.name + '.COMMIT.json',
            'records': meta['records'], 'array_shapes': {k: list(v.shape) for k, v in arrays.items()}}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--root-owned', action='store_true'); ap.add_argument('--execute', action='store_true')
    args = ap.parse_args(); assert args.root_owned and args.execute and not AUTHOR_DRAFT, 'root_only_guarded_execution'
    assert PINS and PROTOCOL in PINS
    verify(PINS); donor, inherited = donor_closed(); pins = dict(PINS)
    c8 = json.loads((J / C8).read_text())
    assert c8['failed'] == 0 and c8['status'] == 'QUALIFIED_ARITHMETIC_NO_PHASE_OR_CLOCK_ADOPTION'
    c8_descriptors = [{k: c[k] for k in ('case', 'AR_rational', 'gamma_rational', 'branch')} for c in c8['cases']]
    assert [c['AR_rational'] for c in c8_descriptors] == ['0', '0', '1/8', '1/8', '7/40', '7/40', '1/4', '1/4']
    for n, h in inherited.items(): assert n not in pins or pins[n] == h; pins[n] = h
    pins[Path(__file__).name] = sha(__file__); verify(pins)
    paths = [J / (STEM + s) for s in ('_RESULT.json', '_REPORT.md', '_RECEIPT.json', '_ERROR.json')]
    assert all(not p.exists() for p in paths) and not CP.exists(), 'unused_namespace'
    global np, AR_CURRENT
    import numpy as np
    owner = {'pid': os.getpid(), 'started_utc': utc(), 'source_sha256': sha(__file__)}
    start = time.monotonic(); CP.mkdir(); owner_record = {'owner': owner, 'pins': pins}
    owner_sha = exclusive(CP / 'OWNER_START.json', canonical(owner_record)); checkpoints = []
    try:
        inc, env = geometry()
        cap0 = next(g for g in donor['groups'] if g['name'] == 'cap_L0')['payload']['rows']
        selected = {(r['background'], r['cut_word'], r['state'][2], r['copy_scaled']): r for r in cap0
                    if r['state'][1] == 0 and r['state'][2] in (0, 1)}
        assert len(selected) == 192
        for i, ar in enumerate(AR):
            AR_CURRENT = ar; CONTEXT.clear(); RAW.clear(); PARTIAL.clear(); CONTEXT.update(stage='kernel', AR=ar)
            local = star(ar); old, new = network(inc.old, 54, local), network(inc.edges, 56, local)
            fk = [kernel_checks(old), kernel_checks(new)]
            node, edge, sign, fm = port_map(inc, old, new)
            kernel_arrays = {n: v for n, v in local.items() if isinstance(v, np.ndarray)}
            kernel_arrays.update(D_old=old['D'], D_new=new['D'], c_old=old['c'], c_new=new['c'],
                                 node_map=node, retained_edge_map=edge, retained_edge_sign=sign,
                                 Cfull_old=(old['D'] * old['c']) @ old['D'].T,
                                 Cfull_new=(new['D'] * new['c']) @ new['D'].T)
            kernel_arrays.update({'chol_' + str(k): v for k, v in enumerate(local['chol'])})
            kernel_records = {'AR': ar, 'zero_branches': local['zero'], 'positive_branches': local['pairs'],
                'tree': local['tree'], 'chords': local['chords'], 'old_ports': old['ports'], 'new_ports': new['ports'],
                'kernel_controls': fk, 'map_controls': fm, 'chol_diagonals': [np.diag(v).tolist() for v in local['chol']]}
            checkpoints.append(checkpoint('KERNEL_AR' + str(i), kernel_records, kernel_arrays, pins, owner))
            for k, kappa in enumerate(KAPPA):
                CONTEXT.clear(); CONTEXT.update(stage='charge_source', AR=ar, kappa=kappa)
                rows, arrays = charge_rows(inc, env, old, new, node, ar, kappa, selected)
                checkpoints.append(checkpoint('CHARGE_AR' + str(i) + '_K' + str(k), rows, arrays, pins, owner))
        predicates = sum(len(c) for cp in checkpoints if cp['checkpoint'].startswith('KERNEL')
                         for c in cp['records']['kernel_controls'])
        predicates += sum(len(cp['records']['map_controls']) for cp in checkpoints if cp['checkpoint'].startswith('KERNEL'))
        predicates += sum(len(r['controls']) for cp in checkpoints if cp['checkpoint'].startswith('CHARGE') for r in cp['records'])
        assert len(checkpoints) == 12 and predicates == 6 * len(KERNEL_KEYS) + 3 * len(MAP_KEYS) + 864 * len(ROW_KEYS)
        assert sha(CP / 'OWNER_START.json') == owner_sha and json.loads((CP / 'OWNER_START.json').read_text()) == owner_record
        cpmap = {p.relative_to(J).as_posix(): sha(p) for p in sorted(CP.iterdir())}; assert len(cpmap) == 25
        for cp in checkpoints:
            p = CP / cp['checkpoint']; assert sha(p) == cp['sha256']
            assert json.loads((CP / cp['commit']).read_text()) == {'checkpoint': p.name, 'sha256': sha(p),
                'pins': pins, 'owner': owner, 'status': 'ARITHMETIC_PASS'}
        verify(pins); donor_closed()
        result = {'status': 'ARITHMETIC_PASS', 'pins': pins, 'owner': owner, 'checkpoints': checkpoints,
            'census': {'AR_members': 3, 'kappa_members': 3, 'charge_rows': 864, 'checkpoint_pairs': 12,
                       'predicates': predicates}, 'inherited_census': donor['census'],
            'inherited_qualification': donor['qualification'], 'qualification': PHYSICAL,
            'C8_fixture_descriptors_only': c8_descriptors,
            'implementation_fixture': {'qstar': 1, 'qR': 1, 'ed': .5, 'em': .5, 'gc': .25, 'U': 1,
                'lambdaR': .5, 'self_per_star': 1, 'cp': 1, 'branch_lengths': 1, 'AR': list(AR), 'kappa': list(KAPPA)},
            'unresolved': ['physical units/charge ratio/geometry/coframe', 'physical chi and Wilson cycle path',
                'new auxiliary-mode isometry and preparation', 'full quantum transfer and noncommuting dynamics',
                'distributed Maxwell frequency/domain projection', 'physical source/Hilbert and support inventory']}
        report = ('# Finite Gauss/kernel/source implementation certificate V001\n\n'
            'Three inherited passive AR fixtures; old/new actual q4 stars; 864 fixed word/donor/source rows. '
            'All baseline zero branches, absolute self/record charging, signed donor debit and stored native '
            'copy/image/complement channels are retained. Twelve array/commit pairs contain the complete arithmetic.\n\n'
            'This uniform whole-domain circuit test selects no physical charge, geometry, field support, Wilson path, '
            'auxiliary state, clock, volume, EOS or cosmological preparation. It evolves no photons or network.\n').encode()
        encoded = canonical(result); rh, th = exclusive(paths[0], encoded), exclusive(paths[1], report)
        assert json.loads(paths[0].read_text()) == result
        receipt = {'status': 'CLOSED', 'owner': owner, 'finished_utc': utc(), 'elapsed_seconds': time.monotonic() - start,
            'pins': pins, 'outputs': {paths[0].name: rh, paths[1].name: th}, 'checkpoint_outputs': cpmap,
            'qualification': PHYSICAL}
        exclusive(paths[2], canonical(receipt)); verify(pins); donor_closed()
        print(json.dumps({'status': result['status'], 'predicates': predicates, 'result_sha256': rh, 'receipt_sha256': sha(paths[2])}))
    except Exception:
        # Raw nonfinite scientific arrays are preserved on refusal, never accepted or JSON-sanitized into results.
        failed = CP / 'FAILED_RAW.npz'; buffer = io.BytesIO()
        np.savez_compressed(buffer, **{k: np.asarray(v) for k, v in RAW.items()})
        if not failed.exists():
            fh = exclusive(failed, buffer.getvalue())
            exclusive(failed.with_name(failed.name + '.COMMIT.json'), canonical({'checkpoint': failed.name,
                'sha256': fh, 'pins': pins, 'owner': owner, 'status': 'FAILED_RAW_UNACCEPTED'}))
        failure = {'status': 'FAILED', 'owner': owner, 'failed_utc': utc(), 'pins': pins, 'context': CONTEXT,
            'raw_failure_arrays': failed.relative_to(J).as_posix(), 'completed_current_group_records': PARTIAL,
            'traceback': traceback.format_exc(),
            'checkpoint_outputs': {p.relative_to(J).as_posix(): sha(p) for p in CP.iterdir()}, 'qualification': PHYSICAL}
        if not paths[3].exists(): exclusive(paths[3], canonical(failure))
        raise


if __name__ == '__main__':
    main()

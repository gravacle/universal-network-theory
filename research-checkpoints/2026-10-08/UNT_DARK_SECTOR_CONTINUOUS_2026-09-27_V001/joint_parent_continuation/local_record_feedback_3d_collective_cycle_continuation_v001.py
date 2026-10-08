#!/usr/bin/env python3
"""NEW bounded SAME-parent Gibbs plus collective-cycle segment; no ancestor execution."""
from pathlib import Path
import ast
import hashlib
import itertools
import json
import math
import os
import resource
import sys
import time
import traceback
import numpy as np

J = Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation')
NAME = 'LOCAL_RECORD_FEEDBACK_3D_COLLECTIVE_CYCLE_CONTINUATION_V001'
SOURCE = Path(__file__).resolve()
PROTOCOL = J / (NAME + '.md')
RESULT = J / (NAME + '_RESULT.json')
REPORT = J / (NAME + '_RESULT.md')
RECEIPT = J / (NAME + '_RECEIPT.json')
CP = J / 'local_record_feedback_3d_collective_cycle_continuation_v001_checkpoints'
PROTOCOL_SHA = '8d15c44df9e66706fa91a35d6e9d5b430f05e65bb55c50526b19b9a2aea57b17'
PARENT_NAME = 'LOCAL_RECORD_FEEDBACK_3D_WORLDLINE_PILOT_V001'
PARENT_CP = J / 'local_record_feedback_3d_worldline_pilot_v001_checkpoints'
PARENT_SOURCE = J / 'local_record_feedback_3d_worldline_pilot_v001.py'
PARENT_PINS = {
    'local_record_feedback_3d_worldline_pilot_v001.py': '48030f615a9a54a2235fd4619e3084a2f5bfd6c9674a13029b6836081f96c6ef',
    PARENT_NAME + '.md': 'f8f06d205be72bec8ca51e17162814a2caa9b0799ffa5dc0678b0e4c38ec0591',
    PARENT_NAME + '_RESULT.json': 'dde8be234ce35ede08fa3fb9efe2b0e06b02ef9406f3996d5df703598e6c8827',
    PARENT_NAME + '_RESULT.md': '7ae9c39e89320818b267a4488f9cb74bfa94bb4a34ed884025c055329ce44b42',
    PARENT_NAME + '_RECEIPT.json': '2fb94e9b5c9f22eb9161013024d542b03bf5822eed1736e1ba883aa1e1cf730c',
}
PARENT_CANONICAL = 'c54e61975c230464ebf1a3bad90168195e6fd9fafd1504ef8efa7cf71a31f0b7'
PARENT_CONTROL_SHA = '581e5886c8e912258c2ac65e6e1a331bfea8a9bfd256b072e7ca15770f933657'
PARENT_MANIFEST_SHA = '2b50e6c7d044380630ee45400d03447f106572fe6e6e5b243f2fce913da7c3ce'
PARENT_JOURNAL_PREFIX = '0b7cda8c9de8e11cb174149487be0c588930f1b418e1ef99c5f5fde3477c1a20'
PRESERVED_FUNCTIONS = ('degrees', 'diagonal', 'transfer', 'suffixes', 'probability',
                       'next_probability', 'inverse_cdf', 'sample_lines', 'sweep',
                       'measure', 'estimates', 'summarize', 'ess', 'rhat')
PRESERVED_CONSTANTS = ('H', 'CONDITIONS', 'STARTS', 'KS', 'COORDS', 'PORTS', 'INDEX',
                       'TARGET', 'PREVIOUS', 'PHASE', 'BPHASE', 'AFOURIER', 'EVENODD',
                       'CUTS', 'SCALAR_NAMES', 'DIAG_NAMES', 'STRUCTURAL_DIAG')
PAIR_NAMES = tuple(itertools.combinations(range(4), 2))
DIFFERENCE_TABLE = np.array(((-5, 0, 5), (-1, 0, 1), (3, 0, -3)), dtype=np.int64)
TERMINAL_PINS = {'c0_I01': ('ea8c8290a3097b4d5b6dafe33d94f8efb3fb2954ae22af4eac16c9bc861efb6c',
            'b48f6782bb39922efc4118e92d4fa357e48508cc539759dd156660f9ffb5f7a1'),
 'c0_I02': ('0a2e428c0d3e77a73e3b9f0f63e9391708a7a8c3fb8130a7155edd5a3c79bc04',
            '48dcc4f15f19bff6f7ac8f76e33446abf6b9224e2139c1c613b1a58d7637f9ac'),
 'c0_B': ('ca24bb1e44c5230dbb33567362fc51b7f81de306d2ab55a7b21d0e233b432957',
          '3777c8716caf865661a7677bc09d6de4ea0a324272ddf5a495c6da856dd3b1c7'),
 'c0_R': ('4069712095fb8750bc84a9d075c267e03ac767c56f5160e03a28be2608907d3a',
          'e92f4a3d8d7472d313eb6a4f8318df5fb53a6495d1201da5c8e9f82898874c58'),
 'c1_I01': ('b035c753eaf4b9d09f49d1851196895ac511fc90ad9109daf1abb30384e73b80',
            '8eb21af64f4911cb48140a3470d40e8a27330cdeb0b66df43e83d2f3ae3f2a52'),
 'c1_I02': ('4b19c992f2c64f3a6b0d6389a9dc75c8394b4618db5708a5b464603e5d462893',
            '6178d6dd7a57d4cacf83f79912031f524ebe1abc046a7ef53a6d88fdc345be51'),
 'c1_B': ('a592eea4d0768f5ff6244c6f810dc24e4f277cd61fb21a16caa2884bbcd670e7',
          '0c16928eb79188b7aae791814de1539f83cb10f517e8758b21dfa8413a7e9441'),
 'c1_R': ('1a2d024a5052936593a34276028b74e89790363288303c3f32686b90f47ddac0',
          'ab1aa359187284ab90db923c265b4504431b1045ba1ffaea97bbd9d5c70af944'),
 'c2_I01': ('c5de9d592f2a9c58caa24efbb2e86ff2ee45126573782c86b76e49773e240b55',
            'feb6d5d8d40dbdcba148fd35e0e6f8462edbe6a9266f37a2e65576674cf77f7a'),
 'c2_I02': ('b245d5d3a796469d53bd99ca8a5072a3eec7c301f6b783d39fcb99f28c9754d1',
            '94c031d691c856b171ef08819bef8d89bc1353b624a8e125bcb9f71f2d5cbd5d'),
 'c2_B': ('7cf33a6fd4b7531ef4314acfd5a78fd183d6ec03eaa05231c64eff8688ac4330',
          '2ce8c91cf09f0e7e217a2b60ecfebbd0b498c619fddad86e393b9d6d26282bcc'),
 'c2_R': ('5e4810aa9d3c07dbcf37109bc89b85793b0f84f12544a1f205de1386e467fdd9',
          '7eb0772e0e9eb60ac6880d90557d464eb0e9baf7b812a93dd0e3d00257372bd6'),
 'c3_I01': ('5561452b540a5ee733187572577174b62719afd5ee328443013f87f01f0e50f0',
            'd9a3bd8015be9955fd3d51918e77f77e880a5871efc0c885d06f91d85c26df4e'),
 'c3_I02': ('566712b072a43080adbd1d3c3e69d104b28baea444014b1b1d508c60d9e249a5',
            'b4c466612dc1c0dde6e8426e12ee0a3f089cd16dab5c3802561e05bb1c9f69c1'),
 'c3_B': ('86eeb2dc94c3672b68df9967657070986d6539788a28cf55834e46f42e63a71f',
          '3b92d56c5c3e85b99ffc2a3393e7fc85e5fa499f87c21f060935a2487e8f7017'),
 'c3_R': ('a1422f26d8ef6cc5413a6b37defec686acad8e94e484e43ecd5091790f29f73e',
          '7b9189386cefb0c8cf906ce87bd2165fad08d4475e003eb2d8c50178f3d8d2b6')}
INPUTS = {
    'LOCAL_RECORD_FEEDBACK_3D_ICE_OPERATOR_CROSSWALK_V001.md': '7f755bbae58c40583f784d469376792cece209193113504136f20e86259b3371',
    'LOCAL_PROPER_BOND_NORMALIZATION_V001.md': '9b4cc5e1942ac7373e210efa46bfa74e03bbcfb8130c01232373b02e8a622a5b',
    'LOCAL_RECORD_FEEDBACK_INTEGER_DEFECT_BRIDGE_V001.md': '2aae1e1585ef42459ccabc13c8e0f388c8598dd9270f5ed953c7e36073119d83',
}
H = 0.2
CONDITIONS = ((4, 16, 64, 202610050400), (4, 32, 128, 202610050410),
              (8, 16, 128, 202610050800), (8, 32, 256, 202610050810))
STARTS = ('I01', 'I02', 'B', 'R')
KS = ((0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 1, 0),
      (0, -1, 0), (0, 0, 1), (0, 0, -1))
COORDS = np.array(list(itertools.product(range(3), repeat=3)), dtype=np.int64)
PORTS = np.array(((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)), dtype=np.int64)
INDEX = {tuple(r): i for i, r in enumerate(COORDS)}
TARGET = np.array([[INDEX[tuple((r + s) % 3)] for r in COORDS] for s in PORTS])
PREVIOUS = np.array([[INDEX[tuple((r - s) % 3)] for r in COORDS] for s in PORTS])
PHASE = np.exp(-2j * np.pi * np.array(KS) @ COORDS.T / 3)
BPHASE = np.exp(-2j * np.pi * np.array(KS) @ PORTS.T / 3)
AFOURIER = np.stack((np.ones((7, 4)), BPHASE), axis=1)
EVENODD = np.array(((1, 1), (1, -1)), dtype=float) / math.sqrt(2)
CUTS = tuple(np.flatnonzero(COORDS[:, i] == 2) for i in range(3))
SCALAR_NAMES = ('energy_density', 'D_density', 'nonice_fraction', 'delta2_density',
                'occupied_fraction', 'energy_diagonal_density', 'energy_transverse_density',
                'kink_count', 'phi_time1', 'phi_time2', 'phi_time3',
                'phi_base1', 'phi_base2', 'phi_base3', 'base_slice_ice')
DIAG_NAMES = ('energy_density', 'D_density', 'nonice_fraction',
              'phi_time1', 'phi_time2', 'phi_time3') + tuple(
    f'k{k}_{p}' for k in range(7) for p in ('ET_trace', 'zero_trace', 'coord_even2', 'coord_odd2'))
STRUCTURAL_DIAG = DIAG_NAMES.index('k0_coord_odd2')
CHECKS = []
STAGES = {}
ACTIVE = None
CREATED = False
CONTROL_ROWS = []
CURRENT_CONTROL = None


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def pack(value):
    a = np.asarray(value)
    if np.iscomplexobj(a):
        return {'real': a.real.tolist(), 'imag': a.imag.tolist()}
    return a.tolist()


def error_safe(value):
    """Preserve malformed numerical evidence without weakening result JSON."""
    if isinstance(value, dict):
        return {key: error_safe(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [error_safe(item) for item in value]
    if isinstance(value, (float, np.floating)) and not math.isfinite(float(value)):
        return {'nonfinite_float': repr(float(value))}
    return value


def exclusive(path, obj):
    with path.open('xb') as stream:
        stream.write(canonical(obj) + b'\n')
        stream.flush()
        os.fsync(stream.fileno())
    return sha(path)


def event(kind, **fields):
    entry = {'event': kind, 'pid': os.getpid(), 'elapsed_seconds': time.perf_counter() - T0, **fields}
    with (CP / 'journal.jsonl').open('ab') as stream:
        stream.write(canonical(entry) + b'\n')
        stream.flush()
        os.fsync(stream.fileno())


def save(name, obj, **fields):
    digest = exclusive(CP / name, obj)
    STAGES[name] = digest
    event('stage_complete', filename=name, sha256=digest, **fields)
    return digest


def check(label, passed, **evidence):
    row = {'label': label, 'passed': bool(passed), **error_safe(evidence)}
    CHECKS.append(row)
    if not passed:
        raise ArithmeticError(label)


def close(label, first, second, tol=3e-13):
    error = float(np.max(np.abs(np.asarray(first) - np.asarray(second))))
    check(label, math.isfinite(error) and error <= tol, maximum_absolute_error=error, tolerance=tol)


def require(passed, label):
    if not passed:
        raise RuntimeError('Custody mismatch: ' + label)


def read_json(path):
    return json.loads(path.read_bytes())


def core_identity():
    """Inspect syntax/source spans only; never import or execute the ancestor."""
    sources = (PARENT_SOURCE.read_bytes(), SOURCE.read_bytes())
    nodes, spans = [], []
    for raw in sources:
        tree, lines = ast.parse(raw), raw.splitlines(keepends=True)
        chosen = {}
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name in PRESERVED_FUNCTIONS:
                chosen[node.name] = node
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id in PRESERVED_CONSTANTS:
                        chosen[target.id] = node
        require(set(chosen) == set(PRESERVED_FUNCTIONS + PRESERVED_CONSTANTS), 'all core spans')
        nodes.append(chosen)
        spans.append({name: b''.join(lines[node.lineno - 1:node.end_lineno])
                      for name, node in chosen.items()})
    hashes = {}
    for name in PRESERVED_FUNCTIONS + PRESERVED_CONSTANTS:
        dumps = [ast.dump(ns[name], include_attributes=False) for ns in nodes]
        require(spans[0][name] == spans[1][name] and dumps[0] == dumps[1], 'core identity ' + name)
        hashes[name] = {'source_span_sha256': hashlib.sha256(spans[0][name]).hexdigest(),
                        'AST_sha256': hashlib.sha256(dumps[0].encode()).hexdigest()}
    return hashes


def authenticate():
    actual = {name: sha(J / name) for name in INPUTS}
    for name, wanted in INPUTS.items():
        require(actual[name] == wanted, name)
    for name, wanted in PARENT_PINS.items():
        actual[name] = sha(J / name)
        require(actual[name] == wanted, name)
    actual['protocol'], actual['source'] = sha(PROTOCOL), sha(SOURCE)
    require(actual['protocol'] == PROTOCOL_SHA, 'new protocol')
    identity = core_identity()
    actual['core_identity_canonical_sha256'] = hashlib.sha256(canonical(identity)).hexdigest()
    parent, receipt = read_json(J / (PARENT_NAME + '_RESULT.json')), read_json(J / (PARENT_NAME + '_RECEIPT.json'))
    parent_inputs = {**INPUTS, 'protocol': PARENT_PINS[PARENT_NAME + '.md'],
                     'source': PARENT_PINS[PARENT_SOURCE.name]}
    require(receipt['input_sha256'] == parent_inputs == parent['input_sha256'], 'parent inputs')
    require(receipt['result_sha256'] == actual[PARENT_NAME + '_RESULT.json'] and
            receipt['report_sha256'] == actual[PARENT_NAME + '_RESULT.md'], 'parent raw/report')
    require(receipt['result_canonical_sha256'] == PARENT_CANONICAL ==
            hashlib.sha256(canonical(parent)).hexdigest(), 'parent canonical result')
    require(all(receipt[key] == parent[key] == value for key, value in
                (('failed', 0), ('passed', 22393), ('check_count', 22393))), 'parent counts')
    require(len(parent['checks']) == 22393 and all(row['passed'] for row in parent['checks']), 'parent checks')
    require(receipt['status'] == parent['status'] == 'MIXING_UNQUALIFIED', 'parent status retained')
    wanted_ids = [f'c{i}_{start}' for i in range(4) for start in STARTS]
    require([row['id'] for row in parent['chains']] == wanted_ids and len(parent['conditions']) == 4,
            'parent complete census')
    lines = (PARENT_CP / 'journal.jsonl').read_bytes().splitlines(keepends=True)
    require(hashlib.sha256(b''.join(lines[:-1])).hexdigest() == PARENT_JOURNAL_PREFIX ==
            receipt['journal_prefix_sha256'], 'parent journal prefix')
    journal = [json.loads(line) for line in lines]
    require(journal[-1]['event'] == 'receipt_complete' and
            journal[-1]['sha256'] == actual[PARENT_NAME + '_RECEIPT.json'], 'parent receipt commit')
    actual[PARENT_CP.name + '/journal.jsonl'] = sha(PARENT_CP / 'journal.jsonl')
    commits = {(row.get('filename'), row.get('sha256')) for row in journal}
    for name, wanted in receipt['checkpoint_sha256'].items():
        digest = sha(PARENT_CP / name)
        require(digest == wanted and (name, digest) in commits, 'parent checkpoint ' + name)
        actual[PARENT_CP.name + '/' + name] = digest
    require(receipt['checkpoint_sha256']['manifest.json'] == PARENT_MANIFEST_SHA and
            receipt['checkpoint_sha256']['controls.json'] == PARENT_CONTROL_SHA, 'parent manifest/control pins')
    manifest, controls = read_json(PARENT_CP / 'manifest.json'), read_json(PARENT_CP / 'controls.json')
    require(manifest['input_sha256'] == parent_inputs and
            manifest['conditions'] == [list(c) for c in CONDITIONS] and manifest['starts'] == list(STARTS),
            'parent manifest configuration')
    require(any(row['event'] == 'started' and row['input_sha256'] == parent_inputs and
                row['manifest_sha256'] == PARENT_MANIFEST_SHA for row in journal), 'parent start commit')
    require(len(controls['cases']) == 48 and controls['checks'] and
            all(row['passed'] for row in controls['checks']), 'prior 48 certified controls')
    for row in parent['chains']:
        cid, index, start = row['id'], row['condition'], row['start']
        beta, denom, m, seed_base = CONDITIONS[index]
        configuration = {'beta': beta, 'epsilon': 1 / denom, 'M': m,
                         'start': start, 'seed': seed_base + STARTS.index(start) + 1}
        ref = row['checkpoints'][-1]
        wanted_meta, wanted_bundle = TERMINAL_PINS[cid]
        require(ref == {'metadata': cid + '_production256.json', 'bundle': cid + '_production256.npz',
                        'metadata_sha256': wanted_meta, 'bundle_sha256': wanted_bundle}, 'terminal reference ' + cid)
        require(receipt['checkpoint_sha256'][ref['metadata']] == wanted_meta and
                receipt['checkpoint_sha256'][ref['bundle']] == wanted_bundle, 'terminal receipt ' + cid)
        meta = read_json(PARENT_CP / ref['metadata'])
        require(meta['id'] == cid and meta['phase'] == 'production256' and
                meta['completed_burn_sweeps'] == 64 and meta['completed_production_sweeps'] == 256 and
                meta['configuration'] == configuration and meta['input_sha256'] == parent_inputs and
                meta['bundle'] == ref['bundle'] and meta['bundle_sha256'] == wanted_bundle and
                meta['array_shapes']['bits'] == [m, 27, 4], 'terminal metadata ' + cid)
        require(meta['rng_state']['bit_generator'] == 'PCG64' and
                set(meta['rng_state']) == {'bit_generator', 'state', 'has_uint32', 'uinteger'}, 'full PCG metadata ' + cid)
    return actual


def degrees(bits):
    da = bits.sum(axis=2, dtype=np.int64)
    db = sum(bits[:, PREVIOUS[a], a].astype(np.int64) for a in range(4))
    return da, db


def diagonal(bits):
    da, db = degrees(bits)
    delta = np.stack((da - 2, db - 2), axis=-1)
    return (delta * delta - delta / 2).sum(axis=(1, 2)), delta


def transfer(v, eps):
    c, s = math.cosh(eps * H), math.sinh(eps * H)
    t = np.empty(v.shape + (2, 2), dtype=float)
    t[..., 0, 0], t[..., 0, 1] = c, s
    weight = np.exp(-eps * v)
    t[..., 1, 0], t[..., 1, 1] = weight * s, weight * c
    return t


def suffixes(t):
    m, batch = t.shape[:2]
    suffix = np.empty((m + 1, batch, 2, 2), dtype=float)
    suffix[m] = np.eye(2)
    logs = np.zeros(batch)
    for tau in range(m - 1, -1, -1):
        if ACTIVE is not None:
            ACTIVE['sampler_phase'], ACTIVE['active_slice'] = 'SUFFIX_MESSAGE', tau
        product = np.matmul(t[tau], suffix[tau + 1])
        scale = product.max(axis=(1, 2))
        if not np.isfinite(product).all() or (product < 0).any() or (scale <= 0).any():
            raise ArithmeticError('Invalid positive transfer message')
        suffix[tau] = product / scale[:, None, None]
        logs += np.log(scale)
    return suffix, logs


def probability(w0, w1):
    total = w0 + w1
    if not np.isfinite(total).all() or (w0 < 0).any() or (w1 < 0).any() or (total <= 0).any():
        raise ArithmeticError('Invalid choice weights')
    p = w1 / total
    if not np.isfinite(p).all() or (p < 0).any() or (p > 1).any():
        raise ArithmeticError('Probability outside [0,1]: ' + repr(p))
    return p


def next_probability(t, suffix, tau, current, first):
    batch = np.arange(t.shape[1])
    w0 = t[tau, batch, current, 0] * suffix[tau + 1, batch, 0, first]
    w1 = t[tau, batch, current, 1] * suffix[tau + 1, batch, 1, first]
    return probability(w0, w1)


def inverse_cdf(p, uniform):
    return np.less(uniform, p).astype(np.uint8)


def sample_lines(v, eps, rng):
    t = transfer(v, eps)
    suffix, _ = suffixes(t)
    m, batch = v.shape
    lines = np.full((m, batch), 255, dtype=np.uint8)
    if ACTIVE is not None:
        ACTIVE['working_lines'] = lines
    p = probability(suffix[0, :, 0, 0], suffix[0, :, 1, 1])
    if ACTIVE is not None:
        ACTIVE['sampler_phase'], ACTIVE['active_slice'] = 'FIRST_BIT', 0
    lines[0] = inverse_cdf(p, rng.random(batch))
    for tau in range(m - 1):
        if ACTIVE is not None:
            ACTIVE['sampler_phase'], ACTIVE['active_slice'] = 'CONDITIONAL_NEXT_BIT', tau + 1
        p = next_probability(t, suffix, tau, lines[tau], lines[0])
        lines[tau + 1] = inverse_cdf(p, rng.random(batch))
    return lines


def sweep(bits, eps, rng):
    for a in range(4):
        if ACTIVE is not None:
            ACTIVE['active_color'] = a
        da, db = degrees(bits)
        line = bits[:, :, a]
        cu, cv = da - line, db[:, TARGET[a]] - line
        v = 2 * (cu + cv) - 7
        bits[:, :, a] = sample_lines(v, eps, rng)
        if ACTIVE is not None:
            ACTIVE['working_lines'] = None
    if ACTIVE is not None:
        ACTIVE['active_color'], ACTIVE['active_slice'], ACTIVE['sampler_phase'] = None, None, None






def build_cycles():
    cycles = []
    for pair_index, (a, b) in enumerate(PAIR_NAMES):
        direction = (PORTS[a] - PORTS[b]) % 3
        representatives = sorted({min(tuple((r + j * direction) % 3) for j in range(3)) for r in COORDS})
        for orbit, representative in enumerate(representatives):
            representative = tuple(int(value) for value in representative)
            cells = [INDEX[tuple((np.array(representative) + j * direction) % 3)] for j in range(3)]
            edge_cells = np.array([cell for j in range(3) for cell in (cells[j], cells[(j + 1) % 3])])
            edge_ports = np.array([a, b] * 3)
            bcells = TARGET[a, cells]
            vertices = [v for j in range(3) for v in (cells[j], 27 + int(bcells[j]))]
            cycles.append({'id': len(cycles), 'pair_index': pair_index, 'pair': (a, b),
                           'orbit': orbit, 'representative': representative, 'direction': direction,
                           'edge_cells': edge_cells, 'edge_ports': edge_ports, 'A_cells': np.array(cells),
                           'B_cells': bcells, 'vertices': vertices})
    return cycles


def cycle_description(cycle):
    return {key: pack(value) if isinstance(value, np.ndarray) else value for key, value in cycle.items()}


def cycle_delta(bits, cycle):
    """Only six affected vertices and six selected columns; signed counts."""
    selected = bits[:, cycle['edge_cells'], cycle['edge_ports']].astype(np.int64)
    ra = selected[:, ((0, 5), (2, 1), (4, 3))].sum(axis=2)
    rb = selected[:, ((0, 1), (2, 3), (4, 5))].sum(axis=2)
    da = bits[:, cycle['A_cells'], :].sum(axis=2, dtype=np.int64)
    db = sum(bits[:, PREVIOUS[p, cycle['B_cells']], p].astype(np.int64) for p in range(4))
    r, c = np.concatenate((ra, rb), axis=1), np.concatenate((da - ra, db - rb), axis=1)
    if (r < 0).any() or (r > 2).any() or (c < 0).any() or (c > 2).any():
        raise ArithmeticError('Cycle local occupation count outside 0..2')
    return int(DIFFERENCE_TABLE[c, r].sum()), selected.astype(np.uint8)


def accept_cycle(ell, uniform):
    if not math.isfinite(ell) or not math.isfinite(uniform) or not 0 <= uniform < 1:
        raise ArithmeticError('Nonfinite/invalid cycle MH arithmetic')
    return uniform == 0 or math.log(uniform) < min(0.0, ell)


def cycle_sweep(state, phase_index):
    accepted = np.zeros(54, dtype=np.int64)
    for cycle in CYCLES:
        cid = cycle['id']
        state['active_cycle'], state['sampler_phase'] = cid, 'CYCLE_LOCAL_DIFFERENCE'
        state['working_cycle_proposal'] = None
        for key in ('cycle_delta_D', 'cycle_log_ratio', 'cycle_uniform', 'cycle_accepted'):
            state[key] = None
        difference, selected = cycle_delta(state['bits'], cycle)
        state['working_cycle_proposal'] = 1 - selected
        state['cycle_delta_D'] = difference
        ell = -state['epsilon'] * difference
        state['cycle_log_ratio'], state['cycle_uniform'] = ell, None
        state['cycle_attempts'][phase_index, cid] += 1
        state['sampler_phase'] = 'CYCLE_ACCEPTANCE_DRAW'
        uniform = float(state['rng'].random())  # Exactly one draw, including ell >= 0.
        state['cycle_uniform'] = uniform
        decision = accept_cycle(ell, uniform)
        state['cycle_accepted'], state['sampler_phase'] = decision, 'CYCLE_COMMIT'
        if decision:
            state['bits'][:, cycle['edge_cells'], cycle['edge_ports']] = state['working_cycle_proposal']
            state['cycle_acceptances'][phase_index, cid] += 1
            accepted[cid] = 1
    state['working_cycle_proposal'] = None
    for key in ('active_cycle', 'cycle_delta_D', 'cycle_log_ratio', 'cycle_uniform', 'cycle_accepted', 'sampler_phase'):
        state[key] = None
    return accepted


def complement_for_control(bits, cycle):
    out = bits.copy()
    out[:, cycle['edge_cells'], cycle['edge_ports']] = 1 - out[:, cycle['edge_cells'], cycle['edge_ports']]
    return out


def deterministic_word(word):
    bit_index = (COORDS[:, 0, None] + 3 * COORDS[:, 1, None] +
                 9 * COORDS[:, 2, None] + 27 * np.arange(4)[None, :]) % 8
    return ((word >> bit_index) & 1).astype(np.uint8)


def cycle_controls():
    global CYCLES, CURRENT_CONTROL
    start = len(CHECKS)
    CYCLES = build_cycles()
    check('exactly_54_cycles', len(CYCLES) == 54)
    seen, incidence = set(), np.zeros((27, 4), dtype=np.int64)
    for cycle in CYCLES:
        cid, a, b = cycle['id'], *cycle['pair']
        CURRENT_CONTROL = {'stage': 'CYCLE_GEOMETRY', 'cycle': cid}
        edges = list(zip(cycle['edge_cells'].tolist(), cycle['edge_ports'].tolist()))
        edge_set = frozenset(edges)
        check(f'cycle{cid}_six_edges_vertices', len(edge_set) == len(set(cycle['vertices'])) == 6)
        check(f'cycle{cid}_unique', edge_set not in seen)
        seen.add(edge_set)
        counts = {v: 0 for v in cycle['vertices']}
        for cell, port in edges:
            u, v = cell, 27 + int(TARGET[port, cell])
            check(f'cycle{cid}_edge{cell}_{port}_on_path', u in counts and v in counts)
            counts[u] += 1
            counts[v] += 1
            incidence[cell, port] += 1
        check(f'cycle{cid}_two_incidences', set(counts.values()) == {2})
        d = cycle['direction']
        check(f'cycle{cid}_order_three', np.any(d != 0) and np.all((3 * d) % 3 == 0))
        for j in range(3):
            check(f'cycle{cid}_ordered_endpoint{j}',
                  TARGET[a, cycle['edge_cells'][2 * j]] == TARGET[b, cycle['edge_cells'][2 * j + 1]])
    check('nine_cycles_per_pair', [sum(c['pair_index'] == p for c in CYCLES) for p in range(6)] == [9] * 6)
    check('three_cycles_per_link', np.all(incidence == 3))
    for c in range(3):
        for r in range(3):
            direct = (c - r) ** 2 - (c - r) / 2 - ((c + r - 2) ** 2 - (c + r - 2) / 2)
            check(f'endpoint_c{c}_r{r}', DIFFERENCE_TABLE[c, r] == direct)
            check(f'endpoint_reverse_c{c}_r{r}', DIFFERENCE_TABLE[c, 2 - r] == -direct)
            for denom in (16, 32):
                ell = -direct / denom
                close(f'endpoint_mh_dt{denom}_c{c}_r{r}', min(0, ell) - min(0, -ell), ell)
    ice01, ice02 = np.zeros((27, 4), dtype=np.uint8), np.zeros((27, 4), dtype=np.uint8)
    ice01[:, (0, 1)], ice02[:, (0, 2)] = 1, 1
    graph_words = [ice01, ice02, np.zeros((27, 4), dtype=np.uint8),
                   np.ones((27, 4), dtype=np.uint8)] + [deterministic_word(w) for w in range(16)]
    for wi, word in enumerate(graph_words):
        bits = word[None]
        for cycle in CYCLES:
            cid = cycle['id']
            CURRENT_CONTROL = {'stage': 'FULL_GRAPH_DIFFERENCE', 'word': wi, 'cycle': cid}
            difference, _ = cycle_delta(bits, cycle)
            changed = complement_for_control(bits, cycle)
            close(f'word{wi}_cycle{cid}_full_delta', difference, (diagonal(changed)[0] - diagonal(bits)[0]).sum(), 0)
            reverse, _ = cycle_delta(changed, cycle)
            check(f'word{wi}_cycle{cid}_reverse', reverse == -difference)
            check(f'word{wi}_cycle{cid}_involution', np.array_equal(complement_for_control(changed, cycle), bits))
    for m in (2, 3, 4):
        for word in range(16):
            bits = np.stack([deterministic_word((word + 3 * tau) % 16) for tau in range(m)])
            for cycle in CYCLES:
                cid = cycle['id']
                CURRENT_CONTROL = {'stage': 'PERIODIC_TOY_PATH', 'M': m, 'word': word, 'cycle': cid}
                difference, _ = cycle_delta(bits, cycle)
                changed = complement_for_control(bits, cycle)
                close(f'toy_m{m}_w{word}_c{cid}_full_delta', difference,
                      (diagonal(changed)[0] - diagonal(bits)[0]).sum(), 0)
                reverse, _ = cycle_delta(changed, cycle)
                check(f'toy_m{m}_w{word}_c{cid}_reverse', reverse == -difference)
                before, after = bits != np.roll(bits, -1, axis=0), changed != np.roll(changed, -1, axis=0)
                check(f'toy_m{m}_w{word}_c{cid}_kink_identity', np.array_equal(before, after) and
                      np.all(before.sum(axis=0) % 2 == 0))
                check(f'toy_m{m}_w{word}_c{cid}_involution', np.array_equal(complement_for_control(changed, cycle), bits))
                for denom in (16, 32):
                    eps, ell = 1 / denom, -difference / denom
                    c, s = math.cosh(eps * H), math.sinh(eps * H)
                    close(f'toy_m{m}_w{word}_c{cid}_C_dt{denom}', np.where(before, s, c), np.where(after, s, c))
                    close(f'toy_m{m}_w{word}_c{cid}_mh_dt{denom}', min(0, ell) - min(0, -ell), ell)
    for ell in (-1, 0, 1):
        check(f'accept_u0_ell{ell}', accept_cycle(ell, 0.0))
        check(f'accept_half_ell{ell}', accept_cycle(ell, 0.5) == (ell >= 0))
    path = ice01[None].copy()
    for cycle in CYCLES:
        if cycle['pair'] == (1, 2):
            difference, _ = cycle_delta(path, cycle)
            check(f'ice01_neutral_cycle{cycle["id"]}', difference == 0)
            path = complement_for_control(path, cycle)
    check('nine_12_cycles_map_I01_to_I02', np.array_equal(path[0], ice02))
    CURRENT_CONTROL = None
    return {'checks': CHECKS[start:].copy(), 'cycles': [cycle_description(c) for c in CYCLES],
            'endpoint_difference_table': DIFFERENCE_TABLE.tolist(), 'old_controls_reused_as_sealed_bytes': True,
            'old_controls_sha256': PARENT_CONTROL_SHA}


def measure(bits, eps, label):
    m = len(bits)
    dtime, delta = diagonal(bits)
    da, db = degrees(bits)
    occupied = bits.sum(axis=(1, 2), dtype=np.int64)
    check(label + '_charge_totals', np.all(delta[:, :, 0].sum(axis=1) == occupied - 54) and
          np.all(delta[:, :, 1].sum(axis=1) == occupied - 54))
    e = bits.astype(float) - 0.5
    z = np.einsum('kr,mra->mka', PHASE, e, optimize=True) / math.sqrt(27)
    dc = np.einsum('kr,mrs->mks', PHASE, delta, optimize=True) / math.sqrt(27)
    derived = np.einsum('ksa,mka->mks', AFOURIER, z, optimize=True)
    close(label + '_fourier_coordination', dc, derived, 3e-11)
    mz, md = z.mean(axis=0), dc.mean(axis=0)
    et = np.einsum('mka,mkb->kab', z, z.conj(), optimize=True) / m
    zero = mz[:, :, None] * mz[:, None, :].conj()
    dsecond = md[:, :, None] * md[:, None, :].conj()
    plusminus = md @ EVENODD
    close(label + '_structural_odd_zero', plusminus[0, 1], 0, 3e-12 * max(1, float(np.linalg.norm(md[0]))))
    flips = bits != np.roll(bits, -1, axis=0)
    check(label + '_even_temporal_kinks', np.all(flips.sum(axis=0) % 2 == 0))
    kinks = int(flips.sum())
    fsame, fflip = math.tanh(eps * H), 1 / math.tanh(eps * H)
    diagonal_energy = float(dtime.mean()) / 54
    transverse_energy = -H / m * (m * 108 * fsame + kinks * (fflip - fsame)) / 54
    phi = np.stack([e[:, CUTS[i], i + 1].sum(axis=1) for i in range(3)], axis=1)
    hist = np.stack((np.bincount(da.ravel(), minlength=5), np.bincount(db.ravel(), minlength=5))) / (m * 27)
    close(label + '_histogram_normalization', hist.sum(axis=1), np.ones(2), 3e-14)
    scalar = np.array((diagonal_energy + transverse_energy, diagonal_energy,
                       np.count_nonzero(delta) / (m * 54), float((delta * delta).mean()),
                       float(bits.mean()), diagonal_energy, transverse_energy, kinks,
                       *phi.mean(axis=0), *phi[0], int(np.all(delta[0] == 0))))
    primitives = []
    for k in range(7):
        primitives.extend((float((np.abs(z[:, k]) ** 2).sum(axis=1).mean()),
                           float((np.abs(mz[k]) ** 2).sum()),
                           float(abs(plusminus[k, 0]) ** 2), float(abs(plusminus[k, 1]) ** 2)))
    diagnostic = np.array((*scalar[:3], *phi.mean(axis=0), *primitives))
    fluxhist = np.stack([np.bincount((phi[:, i] + 4.5).astype(int), minlength=10) for i in range(3)]) / m
    moments = {'mean_z': mz, 'second_z_ET': et, 'second_z_zero': zero,
               'mean_d': md, 'second_d_zero': dsecond, 'hist_degree': hist,
               'hist_oriented_charge': np.stack((hist[0], hist[1, ::-1])),
               'hist_flux': fluxhist, 'scalar': scalar}
    if not all(np.isfinite(v).all() for v in moments.values()) or not np.isfinite(diagnostic).all():
        raise ArithmeticError(label + '_nonfinite_measurement')
    return moments, diagnostic


def estimates(raw):
    zmean, dmean = raw['mean_z'], raw['mean_d']
    zero = raw['second_z_zero'] - zmean[:, :, None] * zmean[:, None, :].conj()
    et = raw['second_z_ET'] - zmean[:, :, None] * zmean[:, None, :].conj()
    coord = raw['second_d_zero'] - dmean[:, :, None] * dmean[:, None, :].conj()
    chi = raw['_beta'] * coord
    evenodd = np.einsum('as,kab,bt->kst', EVENODD, chi, EVENODD, optimize=True)
    return {'S_ET': et, 'S_zero': zero, 'chi_coord': chi, 'chi_evenodd': evenodd,
            'mean_z': zmean, 'mean_d': dmean, 'degree_histogram': raw['hist_degree'],
            'all_vertex_degree_histogram': raw['hist_degree'].mean(axis=0),
            'coordination_delta_histogram': raw['hist_degree'],
            'all_vertex_delta_histogram': raw['hist_degree'].mean(axis=0),
            'oriented_charge_histogram': raw['hist_oriented_charge'],
            'all_vertex_oriented_charge_histogram': raw['hist_oriented_charge'].mean(axis=0),
            'cut_flux_histogram': raw['hist_flux'], 'scalars': raw['scalar'],
            'S_ET_trace': np.trace(et, axis1=1, axis2=2),
            'S_zero_trace': np.trace(zero, axis1=1, axis2=2)}


def summarize(blocks, beta, label):
    b = len(blocks['scalar'])
    raw = {key: value.mean(axis=0) for key, value in blocks.items()}
    raw['_beta'] = beta
    central = estimates(raw)
    replicas = {key: [] for key in central}
    for i in range(b):
        leave = {key: (b * value.mean(axis=0) - value[i]) / (b - 1) for key, value in blocks.items()}
        leave['_beta'] = beta
        for key, value in estimates(leave).items():
            replicas[key].append(value)
    errors = {}
    for key, values in replicas.items():
        a = np.asarray(values)
        re = np.sqrt((b - 1) / b * ((a.real - a.real.mean(axis=0)) ** 2).sum(axis=0))
        if np.iscomplexobj(a):
            im = np.sqrt((b - 1) / b * ((a.imag - a.imag.mean(axis=0)) ** 2).sum(axis=0))
            errors[key] = {'real_se': re, 'imag_se': im}
        else:
            errors[key] = {'se': re}
    derived = beta * np.einsum('ksa,kab,ktb->kst', AFOURIER, central['S_zero'], AFOURIER.conj(), optimize=True)
    close(label + '_static_covariance_crosswalk', central['chi_coord'], derived, 3e-11 * max(1, float(np.linalg.norm(derived))))
    for k in range(7):
        difference = central['S_ET'][k] - central['S_zero'][k]
        hermitian = (difference + difference.conj().T) / 2
        tolerance = 3e-11 * max(1, float(np.linalg.norm(hermitian, ord=2)))
        check(label + f'_time_variance_psd_k{k}', float(np.linalg.eigvalsh(hermitian).min()) >= -tolerance,
              tolerance=tolerance)
    return central, errors


def ess(x):
    x = np.asarray(x, dtype=float)
    centered = x - x.mean()
    c0 = float(centered @ centered / len(x))
    if c0 == 0:
        return {'status': 'UNDEFINED_CONSTANT', 'tau': None, 'ESS': None}
    cov = [float(centered[:-lag] @ centered[lag:] / (len(x) - lag)) for lag in range(1, 127)]
    total, pairs = 0.0, 0
    for i in range(0, 126, 2):
        pair = cov[i] + cov[i + 1]
        if pair <= 0:
            break
        total += pair
        pairs += 1
    tau = max(1.0, 1 + 2 * total / c0)
    return {'status': 'SHORT_CHAIN_IPP_ESTIMATE', 'tau': tau, 'ESS': len(x) / tau, 'positive_pairs': pairs}


def rhat(chains):
    halves = np.asarray(chains).reshape(8, 128)
    means = halves.mean(axis=1)
    w = float(halves.var(axis=1, ddof=1).mean())
    b = float(128 / 7 * ((means - means.mean()) ** 2).sum())
    if w == 0:
        return {'status': 'UNDEFINED_ZERO_WITHIN_VARIANCE', 'Rhat': None, 'W': w, 'B': b}
    return {'status': 'UNRANKED_SHORT_SPLIT_ESTIMATE', 'Rhat': math.sqrt((127 * w / 128 + b / 128) / w), 'W': w, 'B': b}


def checkpoint(state, phase):
    stem = state['id'] + '_' + phase
    arrays = {'bits': state['bits']}
    if state.get('working_lines') is not None:
        arrays['active_partial_line_bits_255_unsampled'] = state['working_lines']
    if state.get('working_cycle_proposal') is not None:
        arrays['active_six_column_cycle_proposal'] = state['working_cycle_proposal']
    arrays.update({key: np.asarray(values) for key, values in state['moments'].items()})
    arrays['diagnostic_traces'] = np.asarray(state['diagnostics']).reshape(-1, len(DIAG_NAMES))
    arrays['cycle_attempts_burn_production'] = state['cycle_attempts']
    arrays['cycle_acceptances_burn_production'] = state['cycle_acceptances']
    arrays['production_cycle_acceptance_traces'] = np.asarray(state['cycle_traces'], dtype=np.int64).reshape(-1, 54)
    complete_blocks = state['production'] // 16
    arrays['complete_block_counts'] = np.full(complete_blocks, 16, dtype=np.int64)
    if complete_blocks:
        for key, values in state['moments'].items():
            value = np.asarray(values)[:16 * complete_blocks]
            arrays['block_sufficient_sums_' + key] = value.reshape(complete_blocks, 16, *value.shape[1:]).sum(axis=1)
    bundle = CP / (stem + '.npz')
    with bundle.open('xb') as stream:
        np.savez(stream, **arrays)
        stream.flush()
        os.fsync(stream.fileno())
    digest = sha(bundle)
    metadata = {'id': state['id'], 'phase': phase, 'completed_burn_sweeps': state['burn'],
                'completed_production_sweeps': state['production'], 'input_sha256': MANIFEST_INPUTS,
                'bundle': bundle.name, 'bundle_sha256': digest, 'array_shapes': {key: list(a.shape) for key, a in arrays.items()},
                'rng_state': state['rng'].bit_generator.state, 'elapsed_seconds': time.perf_counter() - T0}
    metadata['source_terminal_reference'] = state['source_terminal_reference']
    metadata['original_completed_counters'] = {'burn_sweeps': 64, 'production_sweeps': 256}
    metadata['active_context'] = {key: state.get(key) for key in
                                  ('phase', 'attempted_sweep', 'active_color', 'active_slice', 'sampler_phase',
                                   'active_cycle', 'cycle_delta_D', 'cycle_log_ratio', 'cycle_uniform', 'cycle_accepted')}
    metadata['configuration'] = {key: state[key] for key in ('seed', 'beta', 'epsilon', 'M', 'start')}
    save(stem + '.json', error_safe(metadata))
    STAGES[bundle.name] = digest
    event('checkpoint_bundle', id=state['id'], phase=phase, filename=bundle.name, sha256=digest,
          completed_burn_sweeps=state['burn'], completed_production_sweeps=state['production'])
    state['checkpoint_refs'].append({'metadata': stem + '.json', 'bundle': bundle.name,
                                    'metadata_sha256': STAGES[stem + '.json'], 'bundle_sha256': digest})


def recover_chain(index, beta, denom, m, seed, start):
    cid = f'c{index}_{start}'
    meta_path, bundle = PARENT_CP / (cid + '_production256.json'), PARENT_CP / (cid + '_production256.npz')
    require((sha(meta_path), sha(bundle)) == TERMINAL_PINS[cid], 'terminal before load ' + cid)
    meta = read_json(meta_path)
    with np.load(bundle, allow_pickle=False) as saved:
        saved_bits = saved['bits']  # No old measurements or other saved arrays are loaded.
        bits = saved_bits.copy()
        check(cid + '_recovered_array_identity', np.array_equal(bits, saved_bits) and
              hashlib.sha256(bits.tobytes()).hexdigest() == hashlib.sha256(saved_bits.tobytes()).hexdigest())
    check(cid + '_recovered_binary_shape_dtype', bits.dtype == np.uint8 and
          bits.shape == (m, 27, 4) and np.all((bits == 0) | (bits == 1)))
    rng = np.random.Generator(np.random.PCG64(0))
    rng.bit_generator.state = meta['rng_state']  # Entire state, including cached uint32 fields.
    check(cid + '_restored_full_PCG64_state', rng.bit_generator.state == meta['rng_state'])
    require(sha(meta_path) == TERMINAL_PINS[cid][0] and sha(bundle) == TERMINAL_PINS[cid][1],
            'terminal after load ' + cid)
    return bits, rng, {'metadata': str(meta_path.relative_to(J)), 'bundle': str(bundle.relative_to(J)),
                       'metadata_sha256': TERMINAL_PINS[cid][0], 'bundle_sha256': TERMINAL_PINS[cid][1]}


def recovered_summary(bits):
    da, db = degrees(bits)
    _, delta = diagonal(bits)
    phi = np.stack([(bits[:, CUTS[i], i + 1].astype(float) - 0.5).sum(axis=1) for i in range(3)], axis=1)
    hist = np.stack((np.bincount(da.ravel(), minlength=5), np.bincount(db.ravel(), minlength=5))) / (len(bits) * 27)
    return {'degree_bins': [0, 1, 2, 3, 4], 'degree_histogram_AB': hist.tolist(),
            'all_vertex_degree_histogram': hist.mean(axis=0).tolist(),
            'nonice_fraction': float(np.count_nonzero(delta) / (len(bits) * 54)),
            'mean_cut_components': phi.mean(axis=0).tolist(), 'tau0_cut_components': phi[0].tolist()}


def correlated_segment_difference(old, new):
    quantities = {}
    for key, value in new['estimates'].items():
        if isinstance(value, dict) and set(value) == {'real', 'imag'}:
            delta = {part: (np.asarray(value[part]) - np.asarray(old['estimates'][key][part])).tolist()
                     for part in ('real', 'imag')}
        else:
            delta = (np.asarray(value) - np.asarray(old['estimates'][key])).tolist()
        quantities[key] = {'signed_new_minus_old': delta,
                           'old_component_se': old['component_errors'][key],
                           'new_component_se': new['component_errors'][key]}
    return {'quantities': quantities, 'old_status': old['status'], 'new_status': new['status'],
            'interpretation': 'CORRELATED_SUCCESSIVE_SEGMENTS_SEPARATE_COMPONENT_ERRORS_NO_INDEPENDENT_COMBINATION'}


def acceptance_summary(state):
    rows = []
    for cycle in CYCLES:
        cid = cycle['id']
        phases = {}
        for pi, name in enumerate(('burn', 'production')):
            attempts, accepted = int(state['cycle_attempts'][pi, cid]), int(state['cycle_acceptances'][pi, cid])
            phases[name] = {'attempts': attempts, 'accepted': accepted, 'rate': accepted / attempts}
        rows.append({'cycle': cid, 'pair': cycle['pair'], 'orbit': cycle['orbit'], **phases})
    pairs = []
    for pi, pair in enumerate(PAIR_NAMES):
        phases = {}
        for phase, name in enumerate(('burn', 'production')):
            attempts = int(state['cycle_attempts'][phase, 9 * pi:9 * (pi + 1)].sum())
            accepted = int(state['cycle_acceptances'][phase, 9 * pi:9 * (pi + 1)].sum())
            phases[name] = {'attempts': attempts, 'accepted': accepted, 'rate': accepted / attempts}
        pairs.append({'pair': pair, **phases})
    return rows, pairs


def run_chain(index, beta, denom, m, seed, start):
    global ACTIVE
    bits, rng, terminal = recover_chain(index, beta, denom, m, seed, start)
    state = {'id': f'c{index}_{start}', 'bits': bits, 'rng': rng, 'burn': 0, 'production': 0,
             'moments': {}, 'diagnostics': [], 'checkpoint_refs': [], 'phase': 'START',
             'attempted_sweep': None, 'active_color': None, 'active_slice': None, 'sampler_phase': None,
             'seed': seed, 'beta': beta, 'epsilon': 1 / denom, 'M': m, 'start': start, 'working_lines': None,
             'source_terminal_reference': terminal, 'working_cycle_proposal': None, 'active_cycle': None,
             'cycle_attempts': np.zeros((2, 54), dtype=np.int64), 'cycle_acceptances': np.zeros((2, 54), dtype=np.int64),
             'cycle_traces': [], 'cycle_delta_D': None, 'cycle_log_ratio': None, 'cycle_uniform': None,
             'cycle_accepted': None}
    ACTIVE = state
    initial = recovered_summary(bits)
    event('chain_started', id=state['id'], beta=beta, epsilon_denominator=denom, M=m, seed=seed, start=start,
          source_terminal_reference=terminal, initial_rng_state=rng.bit_generator.state,
          original_completed_counters={'burn_sweeps': 64, 'production_sweeps': 256},
          recovered_bits_sha256=hashlib.sha256(bits.tobytes()).hexdigest(), initial_summary=initial)
    chain_time = time.perf_counter()
    checkpoint(state, 'segment_initial')
    for burn in range(1, 65):
        state['phase'], state['attempted_sweep'] = 'BURN_SWEEP', burn
        sweep(bits, 1 / denom, rng)
        cycle_sweep(state, 0)
        state['burn'] = burn
    state['phase'] = 'BURN_COMPLETE'
    checkpoint(state, 'burn64')
    for production in range(1, 257):
        state['phase'], state['attempted_sweep'] = 'PRODUCTION_SWEEP', production
        sweep(bits, 1 / denom, rng)
        accepted = cycle_sweep(state, 1)
        state['phase'] = 'PRODUCTION_MEASUREMENT'
        values, diagnostic = measure(bits, 1 / denom, state['id'] + f'_p{production}')
        for key, value in values.items():
            state['moments'].setdefault(key, []).append(value)
        state['diagnostics'].append(diagnostic)
        state['cycle_traces'].append(accepted)
        state['production'] = production
        state['phase'] = 'PRODUCTION_MEASUREMENT_COMPLETE'
        if production % 32 == 0:
            checkpoint(state, f'production{production:03d}')
            print(json.dumps({'id': state['id'], 'production': production,
                              'elapsed_seconds': time.perf_counter() - T0}), flush=True)
    moments = {key: np.asarray(value) for key, value in state['moments'].items()}
    blocks = {key: value.reshape(16, 16, *value.shape[1:]).mean(axis=1) for key, value in moments.items()}
    central, errors = summarize(blocks, beta, state['id'])
    traces = np.asarray(state['diagnostics'])
    diagnostics = []
    for i, name in enumerate(DIAG_NAMES):
        diagnostic = {'name': name, **({'status': 'STRUCTURAL_NULL', 'ESS': None, 'tau': None}
                                      if i == STRUCTURAL_DIAG else ess(traces[:, i]))}
        diagnostics.append(diagnostic)
    phi = moments['scalar'][:, 11:14]
    phi_time = moments['scalar'][:, 8:11]
    changes = np.count_nonzero(np.diff(phi, axis=0), axis=0).tolist()
    time_changes = np.count_nonzero(np.diff(phi_time, axis=0), axis=0).tolist()
    ice = moments['scalar'][:, 14].astype(bool)
    winding_changes = sum(bool(np.any(phi[i] != phi[i - 1])) for i in range(1, 256) if ice[i] and ice[i - 1])
    def histograms(values):
        out = []
        for component in range(3):
            values_unique, counts = np.unique(values[:, component], return_counts=True)
            out.append({'values': values_unique.tolist(), 'counts': counts.tolist()})
        return out
    ice_words, ice_counts = np.unique(phi[ice], axis=0, return_counts=True)
    check(state['id'] + '_cycle_attempts_exact', np.array_equal(state['cycle_attempts'],
          np.repeat(np.array((64, 256))[:, None], 54, axis=1)))
    check(state['id'] + '_cycle_acceptance_bounds', np.all(state['cycle_acceptances'] >= 0) and
          np.all(state['cycle_acceptances'] <= state['cycle_attempts']))
    check(state['id'] + '_production_acceptance_trace_matches', np.array_equal(
          np.asarray(state['cycle_traces']).sum(axis=0), state['cycle_acceptances'][1]))
    cycle_rows, pair_rows = acceptance_summary(state)
    row = {'id': state['id'], 'condition': index, 'start': start, 'seed': seed, 'beta': beta,
           'epsilon': 1 / denom, 'M': m, 'burn_sweeps': 64, 'production_sweeps': 256,
           'estimates': {key: pack(value) for key, value in central.items()},
           'component_errors': {key: {part: pack(value) for part, value in error.items()} for key, error in errors.items()},
           'block_raw_moments': {key: pack(value) for key, value in blocks.items()},
           'block_counts': [16] * 16,
           'block_sufficient_sums': {key: pack(16 * value) for key, value in blocks.items()},
           'diagnostic_names': DIAG_NAMES, 'diagnostic_traces': traces.tolist(), 'ESS_diagnostics': diagnostics,
           'scalar_names': SCALAR_NAMES, 'scalar_traces': moments['scalar'].tolist(),
           'base_cut_change_counts': changes, 'time_averaged_cut_change_counts': time_changes,
           'base_cut_histograms': histograms(phi), 'time_averaged_cut_histograms': histograms(phi_time),
           'ice_labeled_base_cut_histogram': {'vectors': ice_words.tolist(), 'counts': ice_counts.tolist()},
           'ice_slice_count': int(ice.sum()),
           'undefined_winding_slice_count': int((~ice).sum()), 'consecutive_ice_winding_changes': winding_changes,
           'source_terminal_reference': terminal, 'original_completed_counters': {'burn_sweeps': 64, 'production_sweeps': 256},
           'initial_recovered_summary': initial, 'cycle_acceptance_rows': cycle_rows,
           'pair_acceptance_rows': pair_rows, 'production_cycle_acceptance_traces': np.asarray(state['cycle_traces']).tolist(),
           'production_pair_acceptance_traces': np.asarray(state['cycle_traces']).reshape(256, 6, 9).sum(axis=2).tolist(),
           'production_total_cycle_acceptance_trace': np.asarray(state['cycle_traces']).sum(axis=1).tolist(),
           'checkpoints': state['checkpoint_refs'], 'elapsed_seconds': time.perf_counter() - chain_time,
           'status': 'MIXING_UNQUALIFIED' if any(d['ESS'] is None or d['ESS'] < 16 for i, d in enumerate(diagnostics) if i != STRUCTURAL_DIAG)
                     or any(v == 0 for v in changes + time_changes) else 'CHAIN_DIAGNOSTICS_PASSED_ONLY'}
    old = next(r for r in PARENT_RESULT['chains'] if r['id'] == state['id'])
    row['old_new_segment_comparison'] = correlated_segment_difference(old, row)
    save(state['id'] + '_complete.json', row, id=state['id'])
    event('chain_complete', id=state['id'], status=row['status'], production_sweeps=256)
    ACTIVE = None
    return row, blocks, central, errors, traces


def condition_summary(index, beta, denom, m, records):
    blocks = {key: np.concatenate([r[1][key] for r in records], axis=0) for key in records[0][1]}
    central, errors = summarize(blocks, beta, f'condition{index}')
    split = []
    for i, name in enumerate(DIAG_NAMES):
        split.append({'name': name, **({'status': 'STRUCTURAL_NULL', 'Rhat': None} if i == STRUCTURAL_DIAG
                                      else rhat(np.array([r[4][:, i] for r in records])))})
    passed = all(r[0]['status'] == 'CHAIN_DIAGNOSTICS_PASSED_ONLY' for r in records) and all(
        d['Rhat'] is not None and d['Rhat'] <= 1.10 for i, d in enumerate(split) if i != STRUCTURAL_DIAG)
    differences = []
    for a in range(4):
        for b in range(a + 1, 4):
            differences.append({'first': records[a][0]['id'], 'second': records[b][0]['id'],
                                'signed_estimate_differences': {key: pack(records[a][2][key] - records[b][2][key]) for key in central},
                                'combined_component_se': {key: {part: pack(np.sqrt(records[a][3][key][part] ** 2 + records[b][3][key][part] ** 2))
                                                               for part in records[a][3][key]} for key in central}})
    row = {'condition': index, 'beta': beta, 'epsilon': 1 / denom, 'M': m,
           'chain_ids': [r[0]['id'] for r in records], 'estimates': {key: pack(value) for key, value in central.items()},
           'component_errors': {key: {part: pack(value) for part, value in error.items()} for key, error in errors.items()},
           'split_Rhat': split, 'between_chain_differences': differences,
           'status': 'FINITE_GRID_PILOT_DIAGNOSTICS_PASSED' if passed else 'MIXING_UNQUALIFIED'}
    old = next(r for r in PARENT_RESULT['conditions'] if r['condition'] == index)
    row['old_new_segment_comparison'] = correlated_segment_difference(old, row)
    save(f'condition{index}_complete.json', row)
    return row, central, errors


def comparison(first, second, label):
    out = {}
    for key in first[1]:
        a, b = first[1][key], second[1][key]
        delta = a - b
        error = {part: np.sqrt(first[2][key][part] ** 2 + second[2][key][part] ** 2) for part in first[2][key]}
        flags = {'real': (np.abs(delta.real) > 3 * error.get('real_se', error.get('se'))).tolist()}
        if np.iscomplexobj(delta):
            flags['imag'] = (np.abs(delta.imag) > 3 * error['imag_se']).tolist()
        out[key] = {'signed_difference': pack(delta), 'combined_component_se': {part: pack(value) for part, value in error.items()},
                    'raw_three_SE_flags': flags, 'within_arithmetic_scale': (np.abs(delta) <= 3e-11 * np.maximum(1, np.maximum(np.abs(a), np.abs(b)))).tolist()}
    return {'label': label, 'first_condition': first[0]['condition'], 'second_condition': second[0]['condition'],
            'quantities': out, 'interpretation': 'SIGNED_FINITE_GRID_DIAGNOSTIC_ONLY_NO_ZERO_STEP_OR_GROUND_LIMIT'}


def number(value, error):
    return f'{float(value):.8g} +/- {float(error):.3g}'


def complex_number(value, error, index):
    re, im = np.asarray(value['real'])[index], np.asarray(value['imag'])[index]
    se_re, se_im = np.asarray(error['real_se'])[index], np.asarray(error['imag_se'])[index]
    return number(re, se_re) + '; Im ' + number(im, se_im)


def format_report(result):
    lines = ['# Same-parent collective-cycle continuation V001', '',
             'One new fixed segment from all sixteen authenticated terminal paths and full PCG states. Gibbs helpers and measurements are byte/AST-identical; 54 cycle MH moves preserve the same finite-M law.',
             'The original pilot and its unqualified outcomes remain sealed separately. No new independent preparation or equilibrium guarantee is inferred.', '',
             '## Complete 16-chain census', '',
             '| Chain | beta | dt | Energy/54 | D/54 | Nonice | Mean cuts1–3 | Cut changes time/base | Status |',
             '|---|---:|---:|---|---|---|---|---|---|']
    for row in result['chains']:
        values, errors = row['estimates']['scalars'], row['component_errors']['scalars']['se']
        flux = ', '.join(number(values[i], errors[i]) for i in (8, 9, 10))
        lines.append(f"| {row['id']} | {row['beta']} | {row['epsilon']} | {number(values[0], errors[0])} | {number(values[1], errors[1])} | {number(values[2], errors[2])} | {flux} | {row['time_averaged_cut_change_counts']}/{row['base_cut_change_counts']} | {row['status']} |")
    lines.extend(('', '## Pooled finite-grid spatial and static diagnostics', '',
                  'Complex entries list separate Re/Im estimates and block errors. Coordination susceptibility uses beta times zero-Matsubara covariance.', '',
                  '| Condition | k | S_ET trace | S_zero trace | chi_even | chi_odd | Status |',
                  '|---|---|---|---|---|---|---|'))
    for row in result['conditions']:
        for k, char in enumerate(KS):
            values, errors = row['estimates'], row['component_errors']
            lines.append(f"| {row['condition']} | {char} | {complex_number(values['S_ET_trace'], errors['S_ET_trace'], k)} | {complex_number(values['S_zero_trace'], errors['S_zero_trace'], k)} | {complex_number(values['chi_evenodd'], errors['chi_evenodd'], (k, 0, 0))} | {complex_number(values['chi_evenodd'], errors['chi_evenodd'], (k, 1, 1))} | {row['status']} |")
    lines.extend(('', '## Signed grid comparisons', '',
                  '| Comparison | Energy/54 difference | S_zero trace k0 difference |', '|---|---|---|'))
    for row in result['comparisons']:
        quantities = row['quantities']
        energy = quantities['scalars']
        z = quantities['S_zero_trace']
        lines.append(f"| {row['label']} | {number(energy['signed_difference'][0], energy['combined_component_se']['se'][0])} | {complex_number(z['signed_difference'], z['combined_component_se'], 0)} |")
    lines.extend(('', '## Complete per-pair acceptance census', '',
                  'The attached JSON retains all 54 cycle rows and all 256 per-sweep counts for every chain. Each pair has nine cycles.', '',
                  '| Chain/pair | Burn accepted/attempted | Burn rate | Production accepted/attempted | Production rate |',
                  '|---|---|---:|---|---:|'))
    for row in result['chains']:
        for pair in row['pair_acceptance_rows']:
            burn, prod = pair['burn'], pair['production']
            lines.append(f"| pair {row['id']} {pair['pair']} | {burn['accepted']}/{burn['attempts']} | {burn['rate']:.8g} | {prod['accepted']}/{prod['attempts']} | {prod['rate']:.8g} |")
    lines.extend(('', '## Correlated old/new segment contrasts', '',
                  'Signed new minus old; errors belong to each segment separately and are not combined. Full complex component contrasts are retained in JSON.', '',
                  '| Segment | Energy difference | Old energy SE | New energy SE | Cut1–3 differences | Old cut1–3 SE | New cut1–3 SE | Old/new status |',
                  '|---|---:|---:|---:|---|---|---|---|'))
    for row in result['chains'] + result['conditions']:
        label = row['id'] if 'id' in row else f"pooled{row['condition']}"
        contrast = row['old_new_segment_comparison']
        scalar = contrast['quantities']['scalars']
        delta = scalar['signed_new_minus_old']
        oldse, newse = scalar['old_component_se']['se'], scalar['new_component_se']['se']
        cuts = lambda values: ', '.join(f'{values[i]:.8g}' for i in (8, 9, 10))
        lines.append(f"| old {label} | {delta[0]:.8g} | {oldse[0]:.3g} | {newse[0]:.3g} | {cuts(delta)} | {cuts(oldse)} | {cuts(newse)} | {contrast['old_status']}/{contrast['new_status']} |")
    lines.extend(('', '__ARITHMETIC_CHECK_SUMMARY__',
                  '', 'ESS, unranked split Rhat, between-chain differences, flux histories, degree/charge histograms and all full complex matrices are in the sealed JSON/checkpoints.',
                  'Block errors can miss slow modes. Diagnostic passage does not certify equilibrium. Two time steps give sensitivity, not a rigorous Trotter bound; two beta values and one size do not establish a ground phase.',
                  'Old/new segments are correlated; no independent-SE combination, discarded start, new budget, or automatic continuation is implied.',
                  'Cut-component equality follows supplied graph symmetry in equilibrium; differences are relaxation diagnostics, with no additional pass threshold.',
                  'No native preparation, physical ruler/range, matter vertex, gravity, galaxy or expansion inference is earned.', ''))
    check('report_16_chain_rows', sum(line.startswith('| c') for line in lines) == 16)
    check('report_28_spatial_rows', sum(line.startswith(tuple(f'| {i} | (' for i in range(4))) for line in lines) == 28)
    check('report_four_comparison_rows', sum(line.startswith('| dt_') or line.startswith('| beta_') for line in lines) == 4)
    check('report_96_pair_acceptance_rows', sum(line.startswith('| pair c') for line in lines) == 96)
    check('report_20_correlated_segment_rows', sum(line.startswith('| old ') for line in lines) == 20)
    summary = f"Arithmetic checks: {sum(c['passed'] for c in CHECKS)}/{len(CHECKS)}; runtime {result['elapsed_seconds']:.6f} seconds."
    return '\n'.join(lines).replace('__ARITHMETIC_CHECK_SUMMARY__', summary)


def main():
    global CREATED, MANIFEST_INPUTS, PARENT_RESULT
    if sys.argv[1:] != ['--execute']:
        raise ValueError('Exact --execute argument required; no outputs created')
    for path in (RESULT, REPORT, RECEIPT, CP):
        if path.exists():
            raise FileExistsError('Reserved output exists: ' + str(path))
    MANIFEST_INPUTS = authenticate()
    PARENT_RESULT = read_json(J / (PARENT_NAME + '_RESULT.json'))
    CP.mkdir()
    CREATED = True
    manifest = {'input_sha256': MANIFEST_INPUTS, 'pid': os.getpid(), 'python': sys.version,
                'numpy': np.__version__, 'generator': 'PCG64_FULL_TERMINAL_STATE_RECOVERY',
                'conditions': CONDITIONS, 'starts_as_lineage_labels': STARTS,
                'preserved_core_identity': core_identity(), 'terminal_pins': TERMINAL_PINS,
                'old_completed_counters': {'burn': 64, 'production': 256},
                'new_segment_sweeps': {'burn': 64, 'production': 256},
                'environment': {name: os.environ.get(name) for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'PYTHONDONTWRITEBYTECODE')}}
    save('manifest.json', manifest)
    event('started', input_sha256=MANIFEST_INPUTS, manifest_sha256=STAGES['manifest.json'])
    save('controls.json', cycle_controls())
    chains, conditions = [], []
    for index, (beta, denom, m, seed_base) in enumerate(CONDITIONS):
        records = []
        for offset, start in enumerate(STARTS, 1):
            record = run_chain(index, beta, denom, m, seed_base + offset, start)
            records.append(record)
            chains.append(record[0])
        conditions.append(condition_summary(index, beta, denom, m, records))
    check('complete_16_chains', len(chains) == 16 and all(r['production_sweeps'] == 256 for r in chains))
    check('complete_four_conditions', len(conditions) == 4)
    check('unchanged_all_inputs', authenticate() == MANIFEST_INPUTS)
    comparisons = [comparison(conditions[0], conditions[1], 'dt_beta4_coarse_minus_fine'),
                   comparison(conditions[2], conditions[3], 'dt_beta8_coarse_minus_fine'),
                   comparison(conditions[2], conditions[0], 'beta_dt16_8_minus_4'),
                   comparison(conditions[3], conditions[1], 'beta_dt32_8_minus_4')]
    result = {'name': NAME, 'input_sha256': MANIFEST_INPUTS, 'chains': chains,
              'conditions': [r[0] for r in conditions], 'comparisons': comparisons,
              'cycles': [cycle_description(cycle) for cycle in CYCLES],
              'preserved_core_identity': core_identity(), 'terminal_pins': TERMINAL_PINS,
              'old_segment_status': PARENT_RESULT['status'], 'old_controls_sha256': PARENT_CONTROL_SHA,
              'segment_scope': 'NEW_FIXED_64_BURN_256_PRODUCTION_RECOVERED_PCG_SAME_HAMILTONIAN',
              'characters': KS, 'scalar_names': SCALAR_NAMES, 'diagnostic_names': DIAG_NAMES,
              'histogram_bins': {'degree': [0, 1, 2, 3, 4], 'coordination_delta': [-2, -1, 0, 1, 2],
                                 'oriented_charge': [-2, -1, 0, 1, 2],
                                 'all_slice_cut_flux': [-4.5 + i for i in range(10)]},
              'status': 'FINITE_GRID_PILOT_DIAGNOSTICS_PASSED' if all(r[0]['status'] == 'FINITE_GRID_PILOT_DIAGNOSTICS_PASSED' for r in conditions) else 'MIXING_UNQUALIFIED',
              'checks': CHECKS.copy(), 'check_count': len(CHECKS), 'passed': sum(c['passed'] for c in CHECKS),
              'failed': sum(not c['passed'] for c in CHECKS), 'elapsed_seconds': time.perf_counter() - T0,
              'maxrss_native': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'limitations': ['FLOAT64_AND_PCG64_IMPLEMENTATION_NOT_DIRECTED_PROBABILITY_CERTIFICATE',
                              'EXACT_GIBBS_REFERS_TO_IDEAL_FINITE_M_LAW', 'SHORT_CHAINS_MAY_FREEZE',
                              'CYCLE_MH_IS_MONTE_CARLO_NOT_A_PHYSICAL_HAMILTONIAN_EVENT',
                              'OLD_NEW_SEGMENTS_CORRELATED_COMPONENT_ERRORS_SEPARATE',
                              'BLOCK_ERRORS_AND_ESS_CAN_MISS_SLOW_MODES', 'NO_TROTTER_OR_GROUND_OR_PHASE_CERTIFICATE',
                              'FIXED_RECORD_NC0_SUPPLIED_GRAPH_NOT_FORMATION_OR_PHYSICAL_METRIC']}
    report = format_report(result)
    result['checks'] = CHECKS.copy()
    result['check_count'], result['passed'] = len(CHECKS), sum(c['passed'] for c in CHECKS)
    result['failed'] = sum(not c['passed'] for c in CHECKS)
    raw_sha = exclusive(RESULT, result)
    event('result_complete', filename=RESULT.name, sha256=raw_sha)
    with REPORT.open('x') as stream:
        stream.write(report)
        stream.flush()
        os.fsync(stream.fileno())
    report_sha = sha(REPORT)
    event('report_complete', filename=REPORT.name, sha256=report_sha)
    receipt = {'result_sha256': raw_sha, 'result_canonical_sha256': hashlib.sha256(canonical(result)).hexdigest(),
               'report_sha256': report_sha, 'input_sha256': MANIFEST_INPUTS, 'checkpoint_sha256': STAGES,
               'journal_prefix_sha256': sha(CP / 'journal.jsonl'), 'pid': os.getpid(),
               'check_count': result['check_count'], 'passed': result['passed'], 'failed': result['failed'],
               'status': result['status'], 'elapsed_seconds': time.perf_counter() - T0}
    receipt_sha = exclusive(RECEIPT, receipt)
    event('receipt_complete', filename=RECEIPT.name, sha256=receipt_sha)
    print(json.dumps({'status': result['status'], 'passed': result['passed'], 'failed': result['failed'],
                      'elapsed_seconds': receipt['elapsed_seconds'], 'result_sha256': raw_sha,
                      'receipt_sha256': receipt_sha}), flush=True)


if __name__ == '__main__':
    T0 = time.perf_counter()
    try:
        main()
    except Exception as error:
        if CREATED:
            evidence = {'error_type': type(error).__name__, 'error': str(error), 'traceback': traceback.format_exc(),
                        'checks': CHECKS.copy(), 'elapsed_seconds': time.perf_counter() - T0,
                        'completed_control_cases': CONTROL_ROWS.copy(), 'active_control': CURRENT_CONTROL,
                        'status': 'ARITHMETIC_FAILED' if isinstance(error, ArithmeticError) else 'EXECUTION_FAILED'}
            try:
                if ACTIVE is not None:
                    checkpoint(ACTIVE, 'ERROR_partial')
                save('ERROR.json', error_safe(evidence))
                event('error', error_type=type(error).__name__, error=str(error))
            except Exception as custody_error:
                print('Error checkpoint failure: ' + repr(custody_error), file=sys.stderr, flush=True)
        print(traceback.format_exc(), file=sys.stderr, flush=True)
        sys.exit(3)

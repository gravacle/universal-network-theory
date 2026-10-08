#!/usr/bin/env python3
"""NEW fixed SAME-parent joint pair/coordination segment; ancestor bytes only."""
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
NAME = 'LOCAL_RECORD_FEEDBACK_3D_PAIR_COORDINATION_RESPONSE_V001'
SOURCE = Path(__file__).resolve()
PROTOCOL = J / (NAME + '.md')
RESULT = J / (NAME + '_RESULT.json')
REPORT = J / (NAME + '_RESULT.md')
RECEIPT = J / (NAME + '_RECEIPT.json')
CP = J / 'local_record_feedback_3d_pair_coordination_response_v001_checkpoints'
PROTOCOL_SHA = 'e862125ece9b312e51802a4f6fe46128088a27f4077d62ba3f311db4cc8be6c7'
PARENT_NAME = 'LOCAL_RECORD_FEEDBACK_3D_COLLECTIVE_CYCLE_CONTINUATION_V001'
PARENT_CP = J / 'local_record_feedback_3d_collective_cycle_continuation_v001_checkpoints'
PARENT_SOURCE = J / 'local_record_feedback_3d_collective_cycle_continuation_v001.py'
PARENT_PINS = {'local_record_feedback_3d_collective_cycle_continuation_v001.py': '1a78a4984b1cc9bca473e71e8ce7255a8ebf5f0e9977eb6e94ddf65aa2d7d89e',
 'LOCAL_RECORD_FEEDBACK_3D_COLLECTIVE_CYCLE_CONTINUATION_V001.md': '8d15c44df9e66706fa91a35d6e9d5b430f05e65bb55c50526b19b9a2aea57b17',
 'LOCAL_RECORD_FEEDBACK_3D_COLLECTIVE_CYCLE_CONTINUATION_V001_RESULT.json': 'd9ad0664073f0af71421603facecf3f54284ad967790eff5989ff169a7a871af',
 'LOCAL_RECORD_FEEDBACK_3D_COLLECTIVE_CYCLE_CONTINUATION_V001_RESULT.md': 'f1d045538ef7ff00f9a369cf1815d41915495b6655fd201880e80eec88cda8b7',
 'LOCAL_RECORD_FEEDBACK_3D_COLLECTIVE_CYCLE_CONTINUATION_V001_RECEIPT.json': '7c3567741d689da4d339aceb7373d6ae70bb43d71729d1574d0d4bec5a5e1c83'}
PARENT_CANONICAL = '2b6b9faa320605c30c262df07702c87c978d3eb7942a46d6b9404bb80bae06b5'
PARENT_CONTROL_SHA = 'cdcd9dc4f50f2c96d197fd9ae766af354ff698d6c1d569cdeda3448b1a6dd97f'
PARENT_MANIFEST_SHA = '75a9d47f9875692ff22e8f9de19aefaf44b731614fb9508a64069534b73de267'
PARENT_JOURNAL_PREFIX = 'a639a1d95823f6ef6f579114049c0864ade05f6352ce02a610ea7df5e58183d0'
PRESERVED_FUNCTIONS = ('degrees', 'diagonal', 'transfer', 'suffixes', 'probability',
                       'next_probability', 'inverse_cdf', 'sample_lines', 'sweep',
                       'build_cycles', 'cycle_description', 'cycle_delta', 'accept_cycle', 'cycle_sweep',
                       'deterministic_word', 'measure', 'estimates', 'summarize')
PRESERVED_CONSTANTS = ('H', 'CONDITIONS', 'STARTS', 'KS', 'COORDS', 'PORTS', 'INDEX',
                       'TARGET', 'PREVIOUS', 'PHASE', 'BPHASE', 'AFOURIER', 'EVENODD',
                       'CUTS', 'SCALAR_NAMES', 'DIAG_NAMES', 'STRUCTURAL_DIAG')
PAIR_NAMES = tuple(itertools.combinations(range(4), 2))
DIFFERENCE_TABLE = np.array(((-5, 0, 5), (-1, 0, 1), (3, 0, -3)), dtype=np.int64)
TERMINAL_PINS = {'c0_I01': ('012fdbda8190cfb4082a7ae1495f4abf1c33f5fcc30a17b0dc25ab8092010482',
            '2be12c29ceaca863cbc145f38cc282dc0764aaa673cee0262af3b85907aa1dab'),
 'c0_I02': ('0598d4c74903979a5e88e80beb084c5f4ba57fe19beafb4ce8813b18a76ab381',
            '95d31ce1c7473824bb39fba89ab65b8605d92bc3a1455e7cbd8fe1efaadfe292'),
 'c0_B': ('ddea4eb611e556152d094140053f7d186ad88e20181b6a087e20cb30a11330a5',
          'beff0c2236cad098993d496866db92088c8788e0056c8a00777f1e16748a55fc'),
 'c0_R': ('04518ecc899968e2cb0e65bc1c331629fa2ae3f7243291e86b1be89864b090cf',
          '02424490e3552e0badb234b696476c9ca9c2cc33f108dd4c52b3dec64a1cbdf3'),
 'c1_I01': ('80554ffb04743e008683cfb62454ed3f51166e44466344e98ff2b7071fa22f5c',
            '162e804ebba367b1317fa769282a2a9adabbb9ddbd17251123333e53612617cf'),
 'c1_I02': ('2cad928ca85c54071eb87321beffdab302b18b6ebc60175c6b9019c3044d6361',
            '024d2748de98a9d88a3d98ee0da259a2f92bdb1e5f3b0f018e2567fc4d2f4e35'),
 'c1_B': ('09497c775d27bef4f0ee2e80d7d9748316094e78c8dc719f292975839f17ffc2',
          '7c725992c249089a3a406149d51dfe3c73926e8e0fdb7246af755483226dd475'),
 'c1_R': ('b78601386567d405153331685450669d736cfc259edb8f1efa102780ee7d85ea',
          '25478445698f15850468fd02a7c38a97713ee62f70763a4a28ae2d530678392a'),
 'c2_I01': ('8dea493b573f000e462adf84d535b43c3c6157270191de9123701a9562eba239',
            'd55c9c82ed069bc89f096924cb27a858723270b5ea1bee61b388ca4ec393b0f1'),
 'c2_I02': ('53caa270b95963941c219d029cc26a383bedd3f6b58ee3bc6c3d53f2d1a3f16d',
            'fed85c997c59212fa88a7eb33ab6342b53985e98cd53fb8d3c081835f5bb9fda'),
 'c2_B': ('71e07f91869c57e99ae08f273e874513a55b503aed85138107cf1d9946701532',
          '8898239ed221d09ed0bc0a46dae9874c0e7fb69f430e192466f5039300f47506'),
 'c2_R': ('9c6d0ead69f3e93ace7f8719cebaa4eb608bd66a621aa6c011a47b274300f2fe',
          '4b21d2518e3528aa11e6ca2b754eb0dd553c6f4c2d1d84cf2149adc5cac78390'),
 'c3_I01': ('890b802c3bbdc58bce5914733a4c943ed014c1f941c794229ca84744c30700cc',
            'e0d7c1ae9337bafcb48e6e28c5b12a8a9ecdaabbc4e1a0dee36351dc171256fc'),
 'c3_I02': ('cf1970e2ccc6b536d9fccc4c52680b4b6b165869786a073d8f08ebd3ca4e2137',
            '12fd2edb366fc2754c60acdab0989116daa73061a9c16466354ac62ef7cb7429'),
 'c3_B': ('58e102b678537998690fec0d5b7054c586b650933e1bf6d9a2969767ff0b8eec',
          'e83f905f28d1463c82f761c053594fcdbc016d1bbe389682f2a9b77967cacf50'),
 'c3_R': ('ac29ac662316b7d74d57003e7d4b6130079c381d6e314ae103593e18e3a4330b',
          '652f17f6f3a579a2f9a451d883d7c21eac44ae7aea6299789deb7d84f6d00a71')}
INPUTS = {
    'LOCAL_RECORD_FEEDBACK_3D_ICE_OPERATOR_CROSSWALK_V001.md': '7f755bbae58c40583f784d469376792cece209193113504136f20e86259b3371',
    'LOCAL_PROPER_BOND_NORMALIZATION_V001.md': '9b4cc5e1942ac7373e210efa46bfa74e03bbcfb8130c01232373b02e8a622a5b',
    'LOCAL_RECORD_FEEDBACK_INTEGER_DEFECT_BRIDGE_V001.md': '2aae1e1585ef42459ccabc13c8e0f388c8598dd9270f5ed953c7e36073119d83',
}
ADDITIONAL_INPUTS = {'../../program-worktree/MODEL.md': '3d7c360a38b09fed8f4051c049e838ca561c32ba5dd105dddd80c6aeb7f65607',
 '../../program-worktree/LANE_GRA_FJ_F3_Q4_AUTHENTICATED_LINK_PAIR_RESPONSE_V001/THEOREM.md': '05f4a619a6f80aa40c48570ab4035ab874426502a31468a08f435e66610bd769',
 '../../program-worktree/LANE_CROSS_RFT_GRA_EW_Q4_PAIR_MEMORY_METRIC_DEFORMATION_CLOSURE_V001/THEOREM.md': '495e4e99171f4e3e5809f24e5a9a5b68116e996f4f29115bd22f780127d4714e',
 '../../program-worktree/LANE_CROSS_RFT_GRA_GK_Q4_PAIR_MEMORY_SOURCE_RECIPROCITY_V001/THEOREM.md': '9d79e42d128dd3bae72adc12c26aa27d4e4102bfec917a43d1d6c6688ea49ec7',
 '../../program-worktree/LANE_CROSS_RFT_GRA_GJ_Q4_PAIR_MEMORY_INTRINSIC_CURVATURE_SYMBOL_V001/THEOREM.md': '47f155990137f7467be00e9f7d2cd80633ad35df0639583b72b3262ec44f54a5'}
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
PAIR_LABELS = ('01', '02', '03', '12', '13', '23')
PAIR_I = np.array([a for a, b in PAIR_NAMES])
PAIR_J = np.array([b for a, b in PAIR_NAMES])
Q_NAMES = tuple(f'Y{s}{p}' for s in ('A', 'B') for p in PAIR_LABELS) + ('cA', 'cB')
Q0_NAMES = Q_NAMES[:12] + ('c_even',)
INDEPENDENT_K = (0, 1, 3, 5)
JOINT_DIAG_NAMES = tuple(f'k{k}_{name}_{part}' for k in INDEPENDENT_K
                        for part in (('real', 'power') if k == 0 else ('real', 'imag', 'power'))
                        for name in (Q0_NAMES if k == 0 else Q_NAMES)) + ('primary_TQ_product_density',)
Q0_T = np.zeros((13, 14))
Q0_T[:12, :12] = np.eye(12)
Q0_T[12, 12:] = 1 / math.sqrt(2)
P_CONTRAST = np.eye(4) - np.ones((4, 4)) / 4
B_PAIRS = np.array([np.outer(P_CONTRAST[:, a], P_CONTRAST[:, b]) +
                    np.outer(P_CONTRAST[:, b], P_CONTRAST[:, a]) for a, b in PAIR_NAMES])
D_MAP = np.zeros((2, 14))
D_MAP[0, :6], D_MAP[1, 6:12] = 0.5, 0.5
D_MAP[0, 12], D_MAP[1, 13] = -0.5, -0.5
TQ_MAP = np.zeros((2, 14))
TQ_MAP[0, :12], TQ_MAP[1, 12:] = 1 / math.sqrt(2), 1 / math.sqrt(2)
FOURIER_ONE = PHASE.sum(axis=1) / math.sqrt(27)
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
    actual = {}
    for name, wanted in {**INPUTS, **ADDITIONAL_INPUTS, **PARENT_PINS}.items():
        actual[name] = sha(J / name)
        require(actual[name] == wanted, name)
    actual['protocol'], actual['source'] = sha(PROTOCOL), sha(SOURCE)
    require(actual['protocol'] == PROTOCOL_SHA, 'new protocol')
    actual['core_identity_canonical_sha256'] = hashlib.sha256(canonical(core_identity())).hexdigest()
    parent, receipt = read_json(J / (PARENT_NAME + '_RESULT.json')), read_json(J / (PARENT_NAME + '_RECEIPT.json'))
    require(receipt['input_sha256'] == parent['input_sha256'], 'parent input identity')
    require(receipt['result_sha256'] == actual[PARENT_NAME + '_RESULT.json'] and
            receipt['report_sha256'] == actual[PARENT_NAME + '_RESULT.md'], 'parent raw/report')
    require(receipt['result_canonical_sha256'] == PARENT_CANONICAL ==
            hashlib.sha256(canonical(parent)).hexdigest(), 'parent canonical result')
    require(all(receipt[key] == parent[key] == value for key, value in
                (('failed', 0), ('passed', 45477), ('check_count', 45477))), 'parent counts')
    require(len(parent['checks']) == 45477 and all(row['passed'] for row in parent['checks']), 'parent checks')
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
    require(manifest['input_sha256'] == receipt['input_sha256'] and
            manifest['conditions'] == [list(c) for c in CONDITIONS], 'parent manifest configuration')
    for name, wanted in receipt['input_sha256'].items():
        if name == 'source':
            digest, output_name = sha(PARENT_SOURCE), PARENT_SOURCE.name
        elif name == 'protocol':
            digest, output_name = sha(J / (PARENT_NAME + '.md')), PARENT_NAME + '.md'
        elif name == 'core_identity_canonical_sha256':
            digest = hashlib.sha256(canonical(manifest['preserved_core_identity'])).hexdigest()
            require(digest == wanted, 'parent inherited core identity')
            continue
        else:
            digest, output_name = sha(J / name), name
        require(digest == wanted, 'parent inherited input ' + name)
        actual[output_name] = digest
    require(any(row['event'] == 'started' and row['input_sha256'] == receipt['input_sha256'] and
                row['manifest_sha256'] == PARENT_MANIFEST_SHA for row in journal), 'parent start commit')
    require(len(controls['cycles']) == 54 and controls['checks'] and
            all(row['passed'] for row in controls['checks']) and controls['old_controls_reused_as_sealed_bytes'],
            'prior cycle/Gibbs controls authenticated without rerun')
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
                meta['configuration'] == configuration and meta['input_sha256'] == receipt['input_sha256'] and
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


def quotient_vector(q, k):
    return Q0_T @ q if k == 0 else q


def quotient_matrix(matrix, k):
    return Q0_T @ matrix @ Q0_T.T if k == 0 else matrix


def joint_measure(bits, label):
    za = 1 - 2 * bits.astype(np.int64)
    zb = np.stack([za[:, PREVIOUS[p], p] for p in range(4)], axis=2)
    ya, yb = za[:, :, PAIR_I] * za[:, :, PAIR_J], zb[:, :, PAIR_I] * zb[:, :, PAIR_J]
    da, db = degrees(bits)
    ca, cb = da - 2, db - 2
    check(label + '_pair_sum_exact', np.array_equal(ya.sum(axis=2), 2 * ca * ca - 2) and
          np.array_equal(yb.sum(axis=2), 2 * cb * cb - 2))
    check(label + '_coordination_spin_exact', np.array_equal(-za.sum(axis=2), 2 * ca) and
          np.array_equal(-zb.sum(axis=2), 2 * cb))
    fields = np.concatenate((ya, yb, ca[:, :, None], cb[:, :, None]), axis=2)
    qtime = np.einsum('kr,mrj->mkj', PHASE, fields, optimize=True) / math.sqrt(27)
    qbar = qtime.mean(axis=0)
    df = np.stack((ca * ca - ca / 2, cb * cb - cb / 2), axis=2)
    dbar = (np.einsum('kr,mrs->mks', PHASE, df, optimize=True) / math.sqrt(27)).mean(axis=0)
    scale = 3e-11 * max(1, float(np.linalg.norm(dbar)))
    close(label + '_D_affine_fourier', dbar, qbar @ D_MAP.T + FOURIER_ONE[:, None], scale)
    close(label + '_charge_odd_k0', qbar[0, 12] - qbar[0, 13], 0, 3e-11 * max(1, float(np.linalg.norm(qbar))))
    close(label + '_conjugate_modes', qbar[[2, 4, 6]], qbar[[1, 3, 5]].conj(),
          3e-11 * max(1, float(np.linalg.norm(qbar))))
    zs = np.stack((za, zb), axis=2)
    ys = np.stack((ya, yb), axis=2)
    x = zs @ P_CONTRAST
    spin_mean, pair_mean, x_mean = zs.mean(axis=(0, 1)), ys.mean(axis=(0, 1)), x.mean(axis=(0, 1))
    xx = np.einsum('mrsa,mrsb->sab', x, x, optimize=True) / (len(bits) * 27)
    expected_xx = P_CONTRAST[None] + np.einsum('sp,pab->sab', pair_mean, B_PAIRS, optimize=True)
    close(label + '_local_XX_identity', xx, expected_xx, 3e-11 * max(1, float(np.linalg.norm(xx))))
    tq = (TQ_MAP @ qbar[0]).real
    values = {'mean_Q': qbar, 'second_Q': qbar[:, :, None] * qbar[:, None, :].conj(),
              'mean_D': dbar, 'second_D': dbar[:, :, None] * dbar[:, None, :].conj(),
              'second_Dc': dbar[:, :, None] * qbar[:, None, 12:].conj(),
              'local_spin_mean': spin_mean, 'local_pair_mean': pair_mean,
              'local_X_mean': x_mean, 'local_XX_second': xx,
              'local_c2_mean': np.stack((ca * ca, cb * cb), axis=2).mean(axis=(0, 1)),
              'mean_TQ_density_scaled': tq, 'second_TQ_density': tq[:, None] * tq[None, :]}
    diagnostics = []
    for k in INDEPENDENT_K:
        vector = quotient_vector(qbar[k], k)
        diagnostics.extend(vector.real)
        if k:
            diagnostics.extend(vector.imag)
        diagnostics.extend(np.abs(vector) ** 2)
    diagnostics.append(float(tq[0] * tq[1]))
    diagnostic = np.asarray(diagnostics, dtype=float)
    if diagnostic.shape != (153,) or not np.isfinite(diagnostic).all() or not all(np.isfinite(v).all() for v in values.values()):
        raise ArithmeticError(label + '_joint_nonfinite_or_wrong_diagnostic_shape')
    return values, diagnostic


def pair_controls():
    global CYCLES, CURRENT_CONTROL
    begin = len(CHECKS)
    CYCLES = build_cycles()
    sealed = read_json(PARENT_CP / 'controls.json')
    require(json.loads(canonical([cycle_description(c) for c in CYCLES])) == sealed['cycles'],
            'same canonical cycles as sealed parent controls')
    check('fixed_153_joint_diagnostics', len(JOINT_DIAG_NAMES) == 153)
    check('fixed_orthonormal_null_quotient', np.array_equal(Q0_T[:12, :12], np.eye(12)))
    close('quotient_orthonormality', Q0_T @ Q0_T.T, np.eye(13))
    for word in range(16):
        CURRENT_CONTROL = {'stage': 'LOCAL_PAIR_WORD', 'word': word}
        z = np.array([1 - 2 * ((word >> a) & 1) for a in range(4)], dtype=np.int64)
        y, c = z[PAIR_I] * z[PAIR_J], -int(z.sum()) / 2
        check(f'local_word{word}_sumY', y.sum() == 2 * c * c - 2)
        check(f'local_word{word}_D', c * c - c / 2 == y.sum() / 2 + 1 - c / 2)
        x = P_CONTRAST @ z
        close(f'local_word{word}_XX', np.outer(x, x), P_CONTRAST + np.einsum('p,pab->ab', y, B_PAIRS), 0)
    ice01, ice02 = np.zeros((27, 4), dtype=np.uint8), np.zeros((27, 4), dtype=np.uint8)
    ice01[:, (0, 1)], ice02[:, (0, 2)] = 1, 1
    words = [ice01, ice02, np.zeros((27, 4), dtype=np.uint8), np.ones((27, 4), dtype=np.uint8)] + [deterministic_word(w) for w in range(16)]
    for i, word in enumerate(words):
        CURRENT_CONTROL = {'stage': 'NATIVE_PAIR_FOURIER_WORD', 'word': i}
        values, _ = joint_measure(word[None], f'control_word{i}')
        q = values['mean_Q']
        independent = np.zeros((7, 14), dtype=complex)
        for cell in range(27):
            za = 1 - 2 * word[cell].astype(np.int64)
            zb = np.array([1 - 2 * int(word[PREVIOUS[p, cell], p]) for p in range(4)])
            local = np.array((*[za[a] * za[b] for a, b in PAIR_NAMES],
                              *[zb[a] * zb[b] for a, b in PAIR_NAMES], -za.sum() / 2, -zb.sum() / 2))
            for k, char in enumerate(KS):
                phase = complex(math.cos(-2 * math.pi * sum(char[a] * int(COORDS[cell, a]) for a in range(3)) / 3),
                                math.sin(-2 * math.pi * sum(char[a] * int(COORDS[cell, a]) for a in range(3)) / 3))
                independent[k] += phase * local / math.sqrt(27)
        close(f'control_word{i}_direct_owned_Fourier', q, independent, 3e-11 * max(1, float(np.linalg.norm(q))))
        centered_n = word.astype(float) - 0.5
        port = np.einsum('kr,ra->ka', PHASE, centered_n) / math.sqrt(27)
        derived_c = np.einsum('ksa,ka->ks', AFOURIER, port)
        close(f'control_word{i}_port_charge', q[:, 12:], derived_c, 3e-11 * max(1, float(np.linalg.norm(q))))
    CURRENT_CONTROL = None
    return {'checks': CHECKS[begin:].copy(), 'sampler_control_bytes_reused': PARENT_CONTROL_SHA,
            'cycle_descriptions': sealed['cycles'], 'characters': KS, 'Q_order': Q_NAMES,
            'joint_diagnostic_names': JOINT_DIAG_NAMES, 'all_sampler_functions_byte_AST_identical': True}


def joint_estimates(raw):
    q, d = raw['mean_Q'], raw['mean_D']
    beta = raw['_beta']
    chi = beta * (raw['second_Q'] - q[:, :, None] * q[:, None, :].conj())
    dd = beta * (raw['second_D'] - d[:, :, None] * d[:, None, :].conj())
    dc = beta * (raw['second_Dc'] - d[:, :, None] * q[:, None, 12:].conj())
    x = raw['local_X_mean']
    etx = raw['local_XX_second'] - x[:, :, None] * x[:, None, :]
    tq = raw['mean_TQ_density_scaled']
    scalar = beta * (raw['second_TQ_density'] - tq[:, None] * tq[None, :])
    return {'chi_joint': chi, 'chi_YY': chi[:, :12, :12], 'chi_Yc': chi[:, :12, 12:],
            'chi_cY': chi[:, 12:, :12], 'chi_cc': chi[:, 12:, 12:],
            'chi_DD_independent': dd, 'chi_Dc_independent': dc,
            'chi_TQ_density_independent': scalar, 'mean_Q': q, 'mean_D': d,
            'local_spin_mean': raw['local_spin_mean'], 'local_pair_mean': raw['local_pair_mean'],
            'local_X_mean': x, 'local_XX_second': raw['local_XX_second'],
            'local_X_mean_dyad': x[:, :, None] * x[:, None, :], 'local_X_ET_covariance': etx,
            'local_c2_mean': raw['local_c2_mean']}


def component_jackknife(values):
    values = np.asarray(values)
    b = len(values)
    real = np.sqrt((b - 1) / b * ((values.real - values.real.mean(axis=0)) ** 2).sum(axis=0))
    if np.iscomplexobj(values):
        imag = np.sqrt((b - 1) / b * ((values.imag - values.imag.mean(axis=0)) ** 2).sum(axis=0))
        return {'real_se': real, 'imag_se': imag}
    return {'se': real}


def inverse_diagnostics(matrix):
    residual = float(np.linalg.norm(matrix - matrix.conj().T))
    hermitian = (matrix + matrix.conj().T) / 2
    spectrum = np.linalg.eigvalsh(hermitian)
    minimum, maximum = float(spectrum[0]), float(spectrum[-1])
    condition = maximum / minimum if minimum > 0 else None
    flags = []
    if not np.isfinite(matrix).all() or not np.isfinite(spectrum).all():
        flags.append('NONFINITE')
    if minimum <= 0:
        flags.append('NONPOSITIVE')
    if condition is None or condition > 1e8:
        flags.append('CONDITIONING')
    inverse, product_error = None, None
    if not flags:
        inverse = np.linalg.inv(matrix)  # No ridge, eigenvalue edits, or pseudoinverse.
        product_error = float(np.linalg.norm(matrix @ inverse - np.eye(len(matrix))))
        if not np.isfinite(inverse).all() or product_error > 3e-11 * max(1, condition):
            flags.append('INVERSE_RESIDUAL')
    evidence = {'eigenvalues': spectrum.tolist(), 'minimum': minimum, 'maximum': maximum,
                'trace': pack(np.trace(matrix)), 'condition_number': condition,
                'Hermitian_residual': residual, 'inverse_product_residual': product_error, 'refusal_flags': flags}
    return evidence, inverse if not flags else None


def joint_summary(blocks, beta, label):
    b = len(blocks['mean_Q'])
    raw = {key: value.mean(axis=0) for key, value in blocks.items()}
    raw['_beta'] = beta
    central = joint_estimates(raw)
    replicas = []
    for i in range(b):
        leave = {key: (b * value.mean(axis=0) - value[i]) / (b - 1) for key, value in blocks.items()}
        leave['_beta'] = beta
        replicas.append(joint_estimates(leave))
    errors = {key: component_jackknife([row[key] for row in replicas]) for key in central}
    chi = central['chi_joint']
    tolerance = 3e-11 * max(1, float(np.linalg.norm(chi)))
    close(label + '_joint_Hermitian', chi, chi.conj().swapaxes(1, 2), tolerance)
    close(label + '_joint_conjugacy', chi[[2, 4, 6]], chi[[1, 3, 5]].conj(), tolerance)
    close(label + '_D_D_contraction', central['chi_DD_independent'],
          np.einsum('ai,kij,bj->kab', D_MAP, chi, D_MAP, optimize=True), tolerance)
    close(label + '_D_c_contraction', central['chi_Dc_independent'],
          np.einsum('ai,kij->kaj', D_MAP, chi[:, :, 12:], optimize=True), tolerance)
    close(label + '_scalar_TQ_density', central['chi_TQ_density_independent'], TQ_MAP @ chi[0] @ TQ_MAP.T, tolerance)
    close(label + '_local_X_mean', central['local_X_mean'], central['local_spin_mean'] @ P_CONTRAST, tolerance)
    close(label + '_local_covariance_mean_dyad', central['local_X_ET_covariance'],
          P_CONTRAST[None] + np.einsum('sp,pab->sab', central['local_pair_mean'], B_PAIRS) - central['local_X_mean_dyad'], tolerance)
    null = np.zeros(14)
    null[12], null[13] = 1 / math.sqrt(2), -1 / math.sqrt(2)
    close(label + '_sole_raw_k0_null', chi[0] @ null, np.zeros(14), tolerance)
    inverse_rows = []
    for k in range(7):
        matrix = quotient_matrix(chi[k], k)
        diagnostic, inverse = inverse_diagnostics(matrix)
        rep_matrices = [quotient_matrix(row['chi_joint'][k], k) for row in replicas]
        quotient_error = component_jackknife(rep_matrices)
        three_se = 3 * math.sqrt(float(np.sum(quotient_error['real_se'] ** 2 + quotient_error['imag_se'] ** 2)))
        replica_diagnostics, replica_inverses = [], []
        for replica in rep_matrices:
            evidence, rinv = inverse_diagnostics(replica)
            replica_diagnostics.append(evidence)
            replica_inverses.append(rinv)
        flags = diagnostic['refusal_flags'].copy()
        if diagnostic['minimum'] <= three_se:
            flags.append('BLOCK_ERROR_DOMINATED')
        if any(value is None for value in replica_inverses):
            flags.append('REPLICA_REFUSAL')
        earned = inverse is not None and not flags
        row = {'k': KS[k], 'quotient_dimension': len(matrix), 'raw_quotient_matrix': pack(matrix),
               'quotient_component_errors': {part: pack(v) for part, v in quotient_error.items()},
               'diagnostics': diagnostic, 'three_SE_Frobenius_scale': three_se,
               'replica_diagnostics': replica_diagnostics, 'refusal_flags': flags,
               'status': 'INVERSE_BLOCK_DIAGNOSTICS_PASSED_ONLY' if earned else 'INVERSE_UNQUALIFIED_' + '_'.join(flags),
               'Gamma': None, 'Gamma_Yc': None, 'Gamma_component_errors': None, 'Gamma_Yc_component_errors': None}
        if earned:
            ie = component_jackknife(replica_inverses)
            row.update({'Gamma': pack(inverse), 'Gamma_Yc': pack(inverse[:12, 12:]),
                        'Gamma_component_errors': {part: pack(v) for part, v in ie.items()},
                        'Gamma_Yc_component_errors': {part: pack(v[:12, 12:]) for part, v in ie.items()}})
        inverse_rows.append(row)
    return central, errors, inverse_rows


def qualify_inverses(rows, mixing_passed):
    for row in rows:
        row['mixing_diagnostics_passed'] = mixing_passed
        row['qualified_static_interpretation'] = mixing_passed and row['Gamma'] is not None
        if not mixing_passed:
            row['refusal_flags'].append('MIXING_UNQUALIFIED')
            row['status'] = 'INVERSE_UNQUALIFIED_' + '_'.join(row['refusal_flags'])
            for key in ('Gamma', 'Gamma_Yc', 'Gamma_component_errors', 'Gamma_Yc_component_errors'):
                row['raw_algebraic_candidate_' + key] = row[key]
                row[key] = None
    return rows


def append_joint(state, values, diagnostic):
    state['joint_vectors'].append(values['mean_Q'].copy())
    state['joint_diagnostics'].append(diagnostic)
    for key, value in values.items():
        state['joint_partial_sums'].setdefault(key, np.zeros_like(value))
        state['joint_partial_sums'][key] += value
    state['joint_partial_count'] += 1
    if state['joint_partial_count'] == 32:
        for key, value in state['joint_partial_sums'].items():
            state['joint_block_sums'].setdefault(key, []).append(value.copy())
        state['joint_partial_sums'] = {}
        state['joint_partial_count'] = 0


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
    cov = [float(centered[:-lag] @ centered[lag:] / (len(x) - lag)) for lag in range(1, 511)]
    total, pairs = 0.0, 0
    for i in range(0, 510, 2):
        pair = cov[i] + cov[i + 1]
        if pair <= 0:
            break
        total += pair
        pairs += 1
    tau = max(1.0, 1 + 2 * total / c0)
    return {'status': 'SHORT_CHAIN_IPP_ESTIMATE', 'tau': tau, 'ESS': len(x) / tau, 'positive_pairs': pairs}


def rhat(chains):
    halves = np.asarray(chains).reshape(8, 512)
    means = halves.mean(axis=1)
    w = float(halves.var(axis=1, ddof=1).mean())
    b = float(512 / 7 * ((means - means.mean()) ** 2).sum())
    if w == 0:
        return {'status': 'UNDEFINED_ZERO_WITHIN_VARIANCE', 'Rhat': None, 'W': w, 'B': b}
    return {'status': 'UNRANKED_SHORT_SPLIT_ESTIMATE', 'Rhat': math.sqrt((511 * w / 512 + b / 512) / w), 'W': w, 'B': b}


def checkpoint(state, phase):
    stem = state['id'] + '_' + phase
    arrays = {'bits': state['bits']}
    if state.get('working_lines') is not None:
        arrays['active_partial_line_bits_255_unsampled'] = state['working_lines']
    if state.get('working_cycle_proposal') is not None:
        arrays['active_six_column_cycle_proposal'] = state['working_cycle_proposal']
    arrays.update({key: np.asarray(values) for key, values in state['moments'].items()})
    arrays['diagnostic_traces'] = np.asarray(state['diagnostics']).reshape(-1, len(DIAG_NAMES))
    arrays['bar_Q_every_production_measurement'] = np.asarray(state['joint_vectors'], dtype=complex).reshape(-1, 7, 14)
    arrays['joint_diagnostic_traces'] = np.asarray(state['joint_diagnostics']).reshape(-1, len(JOINT_DIAG_NAMES))
    arrays['cycle_attempts_burn_production'] = state['cycle_attempts']
    arrays['cycle_acceptances_burn_production'] = state['cycle_acceptances']
    arrays['production_cycle_acceptance_traces'] = np.asarray(state['cycle_traces'], dtype=np.int64).reshape(-1, 54)
    complete_blocks = state['production'] // 32
    arrays['complete_block_counts'] = np.full(complete_blocks, 32, dtype=np.int64)
    if complete_blocks:
        for key, values in state['moments'].items():
            value = np.asarray(values)[:32 * complete_blocks]
            arrays['block_sufficient_sums_' + key] = value.reshape(complete_blocks, 32, *value.shape[1:]).sum(axis=1)
        for key, values in state['joint_block_sums'].items():
            arrays['joint_block_sufficient_sums_' + key] = np.asarray(values)
    for key, value in state['joint_partial_sums'].items():
        arrays['joint_partial_block_sufficient_sum_' + key] = value
    bundle = CP / (stem + '.npz')
    with bundle.open('xb') as stream:
        np.savez(stream, **arrays)
        stream.flush()
        os.fsync(stream.fileno())
    digest = sha(bundle)
    metadata = {'id': state['id'], 'phase': phase, 'completed_burn_sweeps': state['burn'],
                'completed_production_sweeps': state['production'], 'input_sha256': MANIFEST_INPUTS,
                'bundle': bundle.name, 'bundle_sha256': digest, 'array_shapes': {key: list(a.shape) for key, a in arrays.items()},
                'rng_state': state['rng'].bit_generator.state, 'elapsed_seconds': time.perf_counter() - T0,
                'source_terminal_reference': state['source_terminal_reference'],
                'original_completed_counters': {'burn_sweeps': 64, 'production_sweeps': 256},
                'joint_complete_block_count': len(state['joint_block_sums'].get('mean_Q', [])),
                'joint_partial_block_count': state['joint_partial_count'],
                'joint_raw_second_moment_retention': '32_SWEEP_COMPLETE_AND_PARTIAL_SUFFICIENT_SUMS_BEFORE_CONNECTED_SUBTRACTION',
                'configuration': {key: state[key] for key in ('seed', 'beta', 'epsilon', 'M', 'start')},
                'active_context': {key: state.get(key) for key in
                                  ('phase', 'attempted_sweep', 'active_color', 'active_slice', 'sampler_phase',
                                   'active_cycle', 'cycle_delta_D', 'cycle_log_ratio', 'cycle_uniform', 'cycle_accepted')}}
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
             'joint_vectors': [], 'joint_diagnostics': [], 'joint_block_sums': {},
             'joint_partial_sums': {}, 'joint_partial_count': 0,
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
    for production in range(1, 1025):
        state['phase'], state['attempted_sweep'] = 'PRODUCTION_SWEEP', production
        sweep(bits, 1 / denom, rng)
        accepted = cycle_sweep(state, 1)
        state['phase'] = 'PRODUCTION_MEASUREMENT_OLD'
        values, diagnostic = measure(bits, 1 / denom, state['id'] + f'_p{production}')
        state['phase'] = 'PRODUCTION_MEASUREMENT_JOINT'
        joint_values, joint_diagnostic = joint_measure(bits, state['id'] + f'_j{production}')
        for key, value in values.items():
            state['moments'].setdefault(key, []).append(value)
        state['diagnostics'].append(diagnostic)
        append_joint(state, joint_values, joint_diagnostic)
        state['cycle_traces'].append(accepted)
        state['production'] = production
        state['phase'] = 'PRODUCTION_MEASUREMENT_COMPLETE'
        if production % 128 == 0:
            checkpoint(state, f'production{production:03d}')
            print(json.dumps({'id': state['id'], 'production': production,
                              'elapsed_seconds': time.perf_counter() - T0}), flush=True)
    moments = {key: np.asarray(value) for key, value in state['moments'].items()}
    blocks = {key: value.reshape(32, 32, *value.shape[1:]).mean(axis=1) for key, value in moments.items()}
    jblocks = {key: np.asarray(value) / 32 for key, value in state['joint_block_sums'].items()}
    check(state['id'] + '_complete_32_joint_blocks', state['joint_partial_count'] == 0 and
          len(state['joint_vectors']) == 1024 and all(len(value) == 32 for value in jblocks.values()))
    central, errors = summarize(blocks, beta, state['id'])
    jcentral, jerrors, inverses = joint_summary(jblocks, beta, state['id'])
    close(state['id'] + '_joint_cc_old_crosswalk', jcentral['chi_cc'], central['chi_coord'],
          3e-11 * max(1, float(np.linalg.norm(central['chi_coord']))))
    traces, jtraces = np.asarray(state['diagnostics']), np.asarray(state['joint_diagnostics'])
    diagnostics = [{'name': name, **({'status': 'STRUCTURAL_NULL', 'ESS': None, 'tau': None}
                    if i == STRUCTURAL_DIAG else ess(traces[:, i]))} for i, name in enumerate(DIAG_NAMES)]
    jdiagnostics = [{'name': name, **ess(jtraces[:, i])} for i, name in enumerate(JOINT_DIAG_NAMES)]
    phi, phi_time = moments['scalar'][:, 11:14], moments['scalar'][:, 8:11]
    changes = np.count_nonzero(np.diff(phi, axis=0), axis=0).tolist()
    time_changes = np.count_nonzero(np.diff(phi_time, axis=0), axis=0).tolist()
    ice = moments['scalar'][:, 14].astype(bool)
    winding_changes = sum(bool(np.any(phi[i] != phi[i - 1])) for i in range(1, 1024) if ice[i] and ice[i - 1])
    def histograms(values):
        out = []
        for component in range(3):
            values_unique, counts = np.unique(values[:, component], return_counts=True)
            out.append({'values': values_unique.tolist(), 'counts': counts.tolist()})
        return out
    ice_words, ice_counts = np.unique(phi[ice], axis=0, return_counts=True)
    check(state['id'] + '_cycle_attempts_exact', np.array_equal(state['cycle_attempts'],
          np.repeat(np.array((64, 1024))[:, None], 54, axis=1)))
    check(state['id'] + '_cycle_acceptance_bounds', np.all(state['cycle_acceptances'] >= 0) and
          np.all(state['cycle_acceptances'] <= state['cycle_attempts']))
    check(state['id'] + '_production_acceptance_trace_matches', np.array_equal(
          np.asarray(state['cycle_traces']).sum(axis=0), state['cycle_acceptances'][1]))
    check(state['id'] + '_ten_fixed_checkpoints', len(state['checkpoint_refs']) == 10)
    passed = all(d['ESS'] is not None and d['ESS'] >= 32 for i, d in enumerate(diagnostics) if i != STRUCTURAL_DIAG)
    passed = passed and all(d['ESS'] is not None and d['ESS'] >= 32 for d in jdiagnostics) and all(v > 0 for v in changes + time_changes)
    qualify_inverses(inverses, passed)
    cycle_rows, pair_rows = acceptance_summary(state)
    row = {'id': state['id'], 'condition': index, 'start': start, 'seed': seed, 'beta': beta,
           'epsilon': 1 / denom, 'M': m, 'burn_sweeps': 64, 'production_sweeps': 1024,
           'estimates': {key: pack(value) for key, value in central.items()},
           'component_errors': {key: {part: pack(value) for part, value in error.items()} for key, error in errors.items()},
           'block_raw_moments': {key: pack(value) for key, value in blocks.items()},
           'block_counts': [32] * 32,
           'block_sufficient_sums': {key: pack(32 * value) for key, value in blocks.items()},
           'joint_estimates': {key: pack(value) for key, value in jcentral.items()},
           'joint_component_errors': {key: {part: pack(value) for part, value in error.items()} for key, error in jerrors.items()},
           'joint_block_raw_moments': {key: pack(value) for key, value in jblocks.items()},
           'joint_block_sufficient_sums': {key: pack(32 * value) for key, value in jblocks.items()},
           'joint_block_counts': [32] * 32, 'joint_inverse_diagnostics': inverses,
           'joint_bar_Q_traces': pack(np.asarray(state['joint_vectors'])),
           'joint_diagnostic_names': JOINT_DIAG_NAMES, 'joint_diagnostic_traces': jtraces.tolist(),
           'joint_ESS_diagnostics': jdiagnostics,
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
           'production_pair_acceptance_traces': np.asarray(state['cycle_traces']).reshape(1024, 6, 9).sum(axis=2).tolist(),
           'production_total_cycle_acceptance_trace': np.asarray(state['cycle_traces']).sum(axis=1).tolist(),
           'checkpoints': state['checkpoint_refs'], 'elapsed_seconds': time.perf_counter() - chain_time,
           'status': 'CHAIN_DIAGNOSTICS_PASSED_ONLY' if passed else 'MIXING_UNQUALIFIED'}
    old = next(r for r in PARENT_RESULT['chains'] if r['id'] == state['id'])
    row['old_new_segment_comparison'] = correlated_segment_difference(old, row)
    row['old_full_joint_segment_comparison'] = {'status': 'UNAVAILABLE_OLD_TWELVE_PAIR_TENSOR_NOT_MEASURED',
                                               'new_moments_not_backfilled_into_old_history': True}
    save(state['id'] + '_complete.json', row, id=state['id'])
    event('chain_complete', id=state['id'], status=row['status'], production_sweeps=1024)
    ACTIVE = None
    return row, blocks, central, errors, traces, jblocks, jcentral, jerrors, jtraces


def component_differences(records, central_index, error_index, central):
    differences = []
    for a in range(4):
        for b in range(a + 1, 4):
            differences.append({'first': records[a][0]['id'], 'second': records[b][0]['id'],
                                'signed_estimate_differences': {key: pack(records[a][central_index][key] - records[b][central_index][key]) for key in central},
                                'combined_component_se': {key: {part: pack(np.sqrt(records[a][error_index][key][part] ** 2 + records[b][error_index][key][part] ** 2))
                                                               for part in records[a][error_index][key]} for key in central}})
    return differences


def condition_summary(index, beta, denom, m, records):
    blocks = {key: np.concatenate([r[1][key] for r in records], axis=0) for key in records[0][1]}
    jblocks = {key: np.concatenate([r[5][key] for r in records], axis=0) for key in records[0][5]}
    central, errors = summarize(blocks, beta, f'condition{index}')
    jcentral, jerrors, inverses = joint_summary(jblocks, beta, f'condition{index}')
    close(f'condition{index}_joint_cc_old_crosswalk', jcentral['chi_cc'], central['chi_coord'],
          3e-11 * max(1, float(np.linalg.norm(central['chi_coord']))))
    split = [{'name': name, **({'status': 'STRUCTURAL_NULL', 'Rhat': None} if i == STRUCTURAL_DIAG
              else rhat(np.array([r[4][:, i] for r in records])))} for i, name in enumerate(DIAG_NAMES)]
    jsplit = [{'name': name, **rhat(np.array([r[8][:, i] for r in records]))} for i, name in enumerate(JOINT_DIAG_NAMES)]
    passed = all(r[0]['status'] == 'CHAIN_DIAGNOSTICS_PASSED_ONLY' for r in records) and all(
        d['Rhat'] is not None and d['Rhat'] <= 1.10 for i, d in enumerate(split) if i != STRUCTURAL_DIAG) and all(
        d['Rhat'] is not None and d['Rhat'] <= 1.10 for d in jsplit)
    qualify_inverses(inverses, passed)
    cross = float(jcentral['chi_TQ_density_independent'][0, 1])
    cross_se = float(jerrors['chi_TQ_density_independent']['se'][0, 1])
    primary = {'value': cross, 'component_block_SE': cross_se, 'sign': 'POSITIVE' if cross > 0 else 'NEGATIVE' if cross < 0 else 'ZERO',
               'raw_three_SE_flag': abs(cross) > 3 * cross_se, 'mixing_diagnostics_passed': passed,
               'status': 'RESOLVED_BLOCK_DIAGNOSTIC_ONLY' if passed and abs(cross) > 3 * cross_se else
                         'MIXING_UNQUALIFIED' if not passed else 'NOT_RESOLVED_BLOCK_DIAGNOSTIC_ONLY'}
    row = {'condition': index, 'beta': beta, 'epsilon': 1 / denom, 'M': m,
           'chain_ids': [r[0]['id'] for r in records], 'estimates': {key: pack(value) for key, value in central.items()},
           'component_errors': {key: {part: pack(value) for part, value in error.items()} for key, error in errors.items()},
           'joint_estimates': {key: pack(value) for key, value in jcentral.items()},
           'joint_component_errors': {key: {part: pack(value) for part, value in error.items()} for key, error in jerrors.items()},
           'joint_inverse_diagnostics': inverses, 'primary_scalar_TQ_density': primary,
           'joint_pooled_block_counts': [32] * 128,
           'joint_pooled_block_sufficient_sums': {key: pack(32 * value) for key, value in jblocks.items()},
           'split_Rhat': split, 'joint_split_Rhat': jsplit,
           'between_chain_differences': component_differences(records, 2, 3, central),
           'joint_between_chain_differences': component_differences(records, 6, 7, jcentral),
           'status': 'FINITE_GRID_PILOT_DIAGNOSTICS_PASSED' if passed else 'MIXING_UNQUALIFIED'}
    old = next(r for r in PARENT_RESULT['conditions'] if r['condition'] == index)
    row['old_new_segment_comparison'] = correlated_segment_difference(old, row)
    row['old_full_joint_segment_comparison'] = {'status': 'UNAVAILABLE_OLD_TWELVE_PAIR_TENSOR_NOT_MEASURED',
                                               'new_moments_not_backfilled_into_old_history': True}
    save(f'condition{index}_complete.json', row)
    return row, central, errors, jcentral, jerrors


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
    lines = ['# Same-parent pair and coordination static response V001', '',
             'A new fixed64-burn/1024-production segment from all16 authenticated cycle-terminal paths and full PCG states. The Gibbs and54-cycle kernels are unchanged.',
             'Static beta covariance of imaginary-time mean pair/charge primitives is measured on the SAME unprojected record-feedback parent. Direct mixed covariance and mixed inverse are distinct.', '',
             '## Complete chain census', '',
             '| Chain | beta | dt | Energy/54 | D/54 | Nonice | Mean cuts1–3 | Changes time/base | Status |',
             '|---|---:|---:|---|---|---|---|---|---|']
    for row in result['chains']:
        values, errors = row['estimates']['scalars'], row['component_errors']['scalars']['se']
        flux = ', '.join(number(values[i], errors[i]) for i in (8, 9, 10))
        lines.append(f"| chain {row['id']} | {row['beta']} | {row['epsilon']} | {number(values[0], errors[0])} | {number(values[1], errors[1])} | {number(values[2], errors[2])} | {flux} | {row['time_averaged_cut_change_counts']}/{row['base_cut_change_counts']} | {row['status']} |")
    lines.extend(('', '## Primary uniform scalar response density', '',
                  'T=sum_nodes sum_6Y and Q=sum_nodes c; native vertex count54. Real block SE is retained. Resolution requires the complete declared mixing passage as well as abs(cross)>3SE.', '',
                  '| Condition | chi_TT | chi_TQ | chi_QQ | Primary cross status | Mixing |', '|---|---|---|---|---|---|'))
    for row in result['conditions']:
        values = row['joint_estimates']['chi_TQ_density_independent']
        errors = row['joint_component_errors']['chi_TQ_density_independent']['se']
        lines.append(f"| scalar {row['condition']} | {number(values[0][0], errors[0][0])} | {number(values[0][1], errors[0][1])} | {number(values[1][1], errors[1][1])} | {row['primary_scalar_TQ_density']['status']} | {row['status']} |")
    lines.extend(('', '## All native modes: direct mixed response and inverse refusal', '',
                  'chi_Yc is12x2 in the raw basis. The k0 inverse quotient has one even-coordination column. All component matrices, Re/Im errors, spectra, replicas and refused candidates are retained in JSON; no empirical mode is removed.', '',
                  '| Condition/mode | Selected chi_YA01,cA (Re; Im) | Quotient min/max | Condition number | Inverse status | Mixing |',
                  '|---|---|---|---|---|---|'))
    for row in result['conditions']:
        values, errors = row['joint_estimates'], row['joint_component_errors']
        for k, inv in enumerate(row['joint_inverse_diagnostics']):
            diag = inv['diagnostics']
            cond = 'undefined' if diag['condition_number'] is None else f"{diag['condition_number']:.8g}"
            lines.append(f"| joint {row['condition']} {KS[k]} | {complex_number(values['chi_Yc'], errors['chi_Yc'], (k, 0, 0))} | {diag['minimum']:.8g}/{diag['maximum']:.8g} | {cond} | {inv['status']} | {row['status']} |")
    lines.extend(('', '## Retained mean dyads and local spin means', '',
                  'The complete XX moment, mean dyad and covariance are saved separately. Local spin means are retained with signed values and block SE; none is set to zero.', '',
                  '| Condition/sublattice | Local X mean0–3 |', '|---|---|'))
    for row in result['conditions']:
        values = row['joint_estimates']['local_X_mean']
        errors = row['joint_component_errors']['local_X_mean']['se']
        for sub in range(2):
            entries = ', '.join(number(values[sub][i], errors[sub][i]) for i in range(4))
            lines.append(f"| dyad {row['condition']} {'AB'[sub]} | {entries} |")
    lines.extend(('', '## Signed grid comparisons', '',
                  'Full14-dimensional component differences and separate real/imag errors are retained. These compare finite grids, without a zero-step or ground extrapolation.', '',
                  '| Comparison | Energy/54 difference | Scalar chi_TQ difference |', '|---|---|---|'))
    for old, joint in zip(result['comparisons'], result['joint_comparisons']):
        energy = old['quantities']['scalars']
        cross = joint['quantities']['chi_TQ_density_independent']
        lines.append(f"| grid {old['label']} | {number(energy['signed_difference'][0], energy['combined_component_se']['se'][0])} | {number(cross['signed_difference'][0][1], cross['combined_component_se']['se'][0][1])} |")
    lines.extend(('', '## Original old/new segment contrasts', '',
                  'Signed new-minus-cycle values; each segment retains its own component SE because the segments are correlated. The old12-pair tensor was not measured and is not reconstructed from a new history.', '',
                  '| Segment | Energy difference | Old/new energy SE | Cut1–3 differences | Old/new mixing |', '|---|---|---|---|---|'))
    for row in result['chains'] + result['conditions']:
        label = row['id'] if 'id' in row else f"pooled{row['condition']}"
        contrast = row['old_new_segment_comparison']
        scalar = contrast['quantities']['scalars']
        delta = scalar['signed_new_minus_old']
        oldse, newse = scalar['old_component_se']['se'], scalar['new_component_se']['se']
        cuts = ', '.join(f'{delta[i]:.8g}' for i in (8, 9, 10))
        lines.append(f"| old {label} | {delta[0]:.8g} | {oldse[0]:.3g}/{newse[0]:.3g} | {cuts} | {contrast['old_status']}/{contrast['new_status']} |")
    lines.extend(('', '## Complete cycle acceptance census', '',
                  'All54 cycles and1024 per-sweep accepted counts per lineage remain saved; each port pair owns nine cycles.', '',
                  '| Chain/pair | Burn accepted/attempted | Burn rate | Production accepted/attempted | Production rate |', '|---|---|---:|---|---:|'))
    for row in result['chains']:
        for pair in row['pair_acceptance_rows']:
            burn, prod = pair['burn'], pair['production']
            lines.append(f"| accept {row['id']} {pair['pair']} | {burn['accepted']}/{burn['attempts']} | {burn['rate']:.8g} | {prod['accepted']}/{prod['attempts']} | {prod['rate']:.8g} |")
    lines.extend(('', '## Formal scalar comparator', '',
                  'Cold leading h2 density [[896,416],[416,224]]h2/27; its T-given-Q Schur is32h2/7 and Q-given-T is8h2/7. The raw signed measured-minus-formal matrix is retained; it is not an h=.2 accuracy gate.', '',
                  '__ARITHMETIC_CHECK_SUMMARY__', '',
                  'All153 new and34 old diagnostic traces, ESS, split Rhat, independent D/c contractions, between-chain differences, conditional inverse errors, null residuals and flux/symmetry histories are retained.',
                  'Short block/ESS/Rhat passage does not certify equilibrium. Finite beta, finite M and one supplied graph do not establish a ground phase or a controlled Trotter limit.',
                  'Same-slice active pair data do not establish qualified retained memory, physical metric/ruler, matter/source completion, galaxy response, expansion, superiority or Stage3 completion.',
                  'No automatic continuation or background work is implied.', ''))
    for prefix, count in (('| chain ', 16), ('| scalar ', 4), ('| joint ', 28), ('| dyad ', 8),
                          ('| grid ', 4), ('| old ', 20), ('| accept ', 96)):
        check('report_rows_' + prefix.strip('| ').replace(' ', '_'), sum(line.startswith(prefix) for line in lines) == count)
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
                'new_segment_sweeps': {'burn': 64, 'production': 1024},
                'environment': {name: os.environ.get(name) for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'PYTHONDONTWRITEBYTECODE')}}
    save('manifest.json', manifest)
    event('started', input_sha256=MANIFEST_INPUTS, manifest_sha256=STAGES['manifest.json'])
    save('controls.json', pair_controls())
    chains, conditions = [], []
    for index, (beta, denom, m, seed_base) in enumerate(CONDITIONS):
        records = []
        for offset, start in enumerate(STARTS, 1):
            record = run_chain(index, beta, denom, m, seed_base + offset, start)
            records.append(record)
            chains.append(record[0])
        conditions.append(condition_summary(index, beta, denom, m, records))
    check('complete_16_chains', len(chains) == 16 and all(r['production_sweeps'] == 1024 for r in chains))
    check('complete_four_conditions', len(conditions) == 4)
    check('unchanged_all_inputs', authenticate() == MANIFEST_INPUTS)
    comparisons = [comparison(conditions[0], conditions[1], 'dt_beta4_coarse_minus_fine'),
                   comparison(conditions[2], conditions[3], 'dt_beta8_coarse_minus_fine'),
                   comparison(conditions[2], conditions[0], 'beta_dt16_8_minus_4'),
                   comparison(conditions[3], conditions[1], 'beta_dt32_8_minus_4')]
    joint_comparisons = [comparison((conditions[a][0], conditions[a][3], conditions[a][4]),
                                    (conditions[b][0], conditions[b][3], conditions[b][4]), label)
                         for a, b, label in ((0, 1, 'dt_beta4_coarse_minus_fine'),
                                             (2, 3, 'dt_beta8_coarse_minus_fine'),
                                             (2, 0, 'beta_dt16_8_minus_4'),
                                             (3, 1, 'beta_dt32_8_minus_4'))]
    formal_scalar = H * H / 27 * np.array(((896, 416), (416, 224)))
    formal_comparisons = [{'condition': row[0]['condition'], 'formal_leading_h2_density': formal_scalar.tolist(),
                          'signed_measured_minus_formal': (row[3]['chi_TQ_density_independent'] - formal_scalar).tolist(),
                          'measured_component_SE': pack(row[4]['chi_TQ_density_independent']['se']),
                          'interpretation': 'FORMAL_COLD_ORDER_H2_COMPARATOR_NOT_FINITE_H_GATE'} for row in conditions]
    check('complete_160_fixed_checkpoints', all(len(row['checkpoints']) == 10 for row in chains))
    result = {'name': NAME, 'input_sha256': MANIFEST_INPUTS, 'chains': chains,
              'conditions': [r[0] for r in conditions], 'comparisons': comparisons,
              'joint_comparisons': joint_comparisons, 'formal_scalar_comparisons': formal_comparisons,
              'cycles': [cycle_description(cycle) for cycle in CYCLES],
              'preserved_core_identity': core_identity(), 'terminal_pins': TERMINAL_PINS,
              'old_segment_status': PARENT_RESULT['status'], 'old_controls_sha256': PARENT_CONTROL_SHA,
              'segment_scope': 'NEW_FIXED_64_BURN_1024_PRODUCTION_JOINT_MEASUREMENT_RECOVERED_PCG_SAME_HAMILTONIAN',
              'characters': KS, 'scalar_names': SCALAR_NAMES, 'diagnostic_names': DIAG_NAMES,
              'joint_Q_order': Q_NAMES, 'joint_diagnostic_names': JOINT_DIAG_NAMES,
              'sole_k0_null_quotient_matrix': Q0_T.tolist(), 'independent_diagnostic_characters': INDEPENDENT_K,
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
                              'FIXED_RECORD_NC0_SUPPLIED_GRAPH_NOT_FORMATION_OR_PHYSICAL_METRIC',
                              'ACTIVE_PAIR_NOT_QUALIFIED_RETAINED_MEMORY', 'STATIC_KUBO_RESPONSE_NOT_SLD_OR_CAUSAL_KERNEL',
                              'DIRECT_CHI_YC_DISTINCT_CONDITIONAL_GAMMA_YC', 'INVERSE_REFUSED_IF_BLOCK_OR_MIXING_UNSUPPORTED']}
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

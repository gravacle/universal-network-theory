#!/usr/bin/env python3
"""NEW fixed finite-M Gibbs pilot; sealed ancestor notes are bytes only."""
from pathlib import Path
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
NAME = 'LOCAL_RECORD_FEEDBACK_3D_WORLDLINE_PILOT_V001'
SOURCE = Path(__file__).resolve()
PROTOCOL = J / (NAME + '.md')
RESULT = J / (NAME + '_RESULT.json')
REPORT = J / (NAME + '_RESULT.md')
RECEIPT = J / (NAME + '_RECEIPT.json')
CP = J / 'local_record_feedback_3d_worldline_pilot_v001_checkpoints'
PROTOCOL_SHA = 'f8f06d205be72bec8ca51e17162814a2caa9b0799ffa5dc0678b0e4c38ec0591'
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


def authenticate():
    actual = {name: sha(J / name) for name in INPUTS}
    for name, wanted in INPUTS.items():
        if actual[name] != wanted:
            raise RuntimeError('Frozen input changed: ' + name)
    actual['protocol'] = sha(PROTOCOL)
    if actual['protocol'] != PROTOCOL_SHA:
        raise RuntimeError('Protocol bytes changed')
    actual['source'] = sha(SOURCE)
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


def enumeration_case(v, eps, label):
    global CURRENT_CONTROL
    CURRENT_CONTROL = {'label': label, 'v': list(v), 'epsilon': eps}
    m = len(v)
    words = np.array(list(itertools.product((0, 1), repeat=m)), dtype=np.uint8)
    c = math.cosh(eps * H)
    s = math.sinh(eps * H)
    weights = np.array([math.exp(-eps * sum(v[t] * int(w[t]) for t in range(m))) *
                       math.prod(c if w[t] == w[(t + 1) % m] else s for t in range(m))
                       for w in words])
    probs = weights / weights.sum()
    t = transfer(np.asarray(v, dtype=float)[:, None], eps)
    suffix, logs = suffixes(t)
    logz = logs[0] + math.log(float(np.trace(suffix[0, 0])))
    relative = abs(math.exp(logz) / weights.sum() - 1)
    check(label + '_partition', relative <= 3e-13, relative_error=relative)
    reconstructed = np.empty(len(words))
    for j, word in enumerate(words):
        p = float(probability(suffix[0, :, 0, 0], suffix[0, :, 1, 1])[0])
        reconstructed[j] = p if word[0] else 1 - p
        for tau in range(m - 1):
            p = float(next_probability(t, suffix, tau, np.array([word[tau]]), np.array([word[0]]))[0])
            reconstructed[j] *= p if word[tau + 1] else 1 - p
    close(label + '_all_words', reconstructed, probs)
    for tau in range(m):
        close(label + f'_marginal{tau}', reconstructed @ words[:, tau], probs @ words[:, tau])
        for other in range(m):
            close(label + f'_pair{tau}_{other}', reconstructed @ (words[:, tau] * words[:, other]),
                  probs @ (words[:, tau] * words[:, other]))
    for length in range(m):
        for prefix in itertools.product((0, 1), repeat=length):
            CURRENT_CONTROL['prefix'] = list(prefix)
            eligible = np.all(words[:, :length] == prefix, axis=1) if length else np.ones(len(words), dtype=bool)
            p_enum = float(probs[eligible & (words[:, length] == 1)].sum() / probs[eligible].sum())
            if length == 0:
                p = float(probability(suffix[0, :, 0, 0], suffix[0, :, 1, 1])[0])
            else:
                p = float(next_probability(t, suffix, length - 1, np.array([prefix[-1]]), np.array([prefix[0]]))[0])
            CURRENT_CONTROL.update(transfer_probability=p, enumeration_probability=p_enum)
            close(label + '_prefix_' + str(prefix), p, p_enum)
            if 1e-8 < p < 1 - 1e-8:
                check(label + '_cdf_' + str(prefix),
                      int(inverse_cdf(np.asarray(p), np.asarray(p_enum - 1e-8))) == 1 and
                      int(inverse_cdf(np.asarray(p), np.asarray(p_enum + 1e-8))) == 0)
            else:
                check(label + '_cdf_endpoint_' + str(prefix),
                      int(inverse_cdf(np.asarray(p), np.asarray(0.0))) == int(p_enum > 0) and
                      int(inverse_cdf(np.asarray(p), np.asarray(1.0))) == 0)
    shifted = t * math.exp(-37 * eps)
    rs, ls = suffixes(shifted)
    close(label + '_constant_probabilities', rs, suffix)
    close(label + '_constant_logz', ls[0] + math.log(float(np.trace(rs[0, 0]))) - logz, -37 * m * eps)
    check(label + '_even_kinks', np.all(np.count_nonzero(words != np.roll(words, -1, axis=1), axis=1) % 2 == 0))
    return {'label': label, 'v': list(v), 'epsilon': eps, 'words': words.tolist(),
            'direct_weights': weights.tolist(), 'transfer_probabilities': reconstructed.tolist(),
            'direct_probabilities': probs.tolist(), 'transfer_log_partition': logz}


def controls():
    global CURRENT_CONTROL
    CURRENT_CONTROL = {'phase': 'GRAPH_AND_NATIVE_ENDPOINT_CONTROLS'}
    start = len(CHECKS)
    for p, u, wanted in ((0.0, 0.0, 0), (0.0, 0.5, 0), (1.0, 0.0, 1), (1.0, 0.5, 1)):
        check(f'inverse_CDF_exact_endpoint_{p}_{u}',
              int(inverse_cdf(np.asarray(p), np.asarray(u))) == wanted)
    edges = [(i, 27 + int(TARGET[a, i])) for i in range(27) for a in range(4)]
    check('graph_108_unique', len(set(edges)) == 108)
    degree = np.bincount(np.array(edges).reshape(-1), minlength=54)
    check('graph_degree_four', np.all(degree == 4))
    for a in range(4):
        check(f'color{a}_matching', len(set(TARGET[a].tolist())) == 27)
    for external in itertools.product((0, 1), repeat=6):
        cu, cv = sum(external[:3]), sum(external[3:])
        f = lambda d: (d - 2) ** 2 - (d - 2) / 2
        check('endpoint_difference_' + ''.join(map(str, external)),
              f(cu + 1) + f(cv + 1) - f(cu) - f(cv) == 2 * (cu + cv) - 7)
    for occupied in ((0, 1), (0, 2), (), (0, 1, 2, 3)):
        bits = np.zeros((1, 27, 4), dtype=np.uint8)
        bits[:, :, occupied] = 1
        d, delta = diagonal(bits)
        z = 1 - 2 * bits.astype(np.int64)
        owned_pairs = 0
        for vertex in range(27):
            incident_a = z[0, vertex]
            incident_b = np.array([z[0, PREVIOUS[a, vertex], a] for a in range(4)])
            owned_pairs += sum(incident_a[a] * incident_a[b] + incident_b[a] * incident_b[b]
                               for a in range(4) for b in range(a + 1, 4))
        close('pauli_start_' + str(occupied), d[0], 54 + owned_pairs / 2 + z.sum() / 2, 0)
        if len(occupied) == 2:
            check('ice_' + str(occupied), np.all(delta == 0))
            phi = [float((bits[0, CUTS[i], i + 1] - 0.5).sum()) for i in range(3)]
            close('initial_flux_' + str(occupied), phi,
                  (4.5, -4.5, -4.5) if occupied == (0, 1) else (-4.5, 4.5, -4.5), 0)
    for word in range(16):
        bit_index = (COORDS[:, 0, None] + 3 * COORDS[:, 1, None] +
                     9 * COORDS[:, 2, None] + 27 * np.arange(4)[None, :]) % 8
        bits = ((word >> bit_index) & 1).astype(np.uint8)[None]
        d, _ = diagonal(bits)
        z = 1 - 2 * bits.astype(np.int64)
        pairs = 0
        for a in range(4):
            for b in range(a + 1, 4):
                pairs += (z[0, :, a] * z[0, :, b]).sum()
                pairs += (z[0, PREVIOUS[a], a] * z[0, PREVIOUS[b], b]).sum()
        close(f'pauli_word{word}', d[0], 54 + pairs / 2 + z.sum() / 2, 0)
    for denom in (16, 32):
        for m in (2, 3, 4):
            for v in (-7, -5, -3, -1, 1, 3, 5):
                CONTROL_ROWS.append(enumeration_case([v] * m, 1 / denom, f'dt{denom}_m{m}_v{v}'))
        for v in ((-7, 5), (-3, 1, 5), (-7, -1, 3, 5)):
            CONTROL_ROWS.append(enumeration_case(v, 1 / denom, f'dt{denom}_vary{len(v)}'))
    check('48_enumeration_cases', len(CONTROL_ROWS) == 48)
    CURRENT_CONTROL = None
    return {'checks': CHECKS[start:].copy(), 'cases': CONTROL_ROWS.copy(), 'graph_edges': edges,
            'target': TARGET.tolist(), 'previous': PREVIOUS.tolist(), 'characters': KS}


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
    arrays.update({key: np.asarray(values) for key, values in state['moments'].items()})
    arrays['diagnostic_traces'] = np.asarray(state['diagnostics']).reshape(-1, len(DIAG_NAMES))
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
    metadata['active_context'] = {key: state.get(key) for key in
                                  ('phase', 'attempted_sweep', 'active_color', 'active_slice', 'sampler_phase')}
    metadata['configuration'] = {key: state[key] for key in ('seed', 'beta', 'epsilon', 'M', 'start')}
    save(stem + '.json', metadata)
    STAGES[bundle.name] = digest
    event('checkpoint_bundle', id=state['id'], phase=phase, filename=bundle.name, sha256=digest,
          completed_burn_sweeps=state['burn'], completed_production_sweeps=state['production'])
    state['checkpoint_refs'].append({'metadata': stem + '.json', 'bundle': bundle.name,
                                    'metadata_sha256': STAGES[stem + '.json'], 'bundle_sha256': digest})


def run_chain(index, beta, denom, m, seed, start):
    global ACTIVE
    rng = np.random.Generator(np.random.PCG64(seed))
    base = np.zeros((27, 4), dtype=np.uint8)
    if start in ('I01', 'I02'):
        base[:, (0, 1) if start == 'I01' else (0, 2)] = 1
    elif start == 'R':
        base[:] = rng.integers(0, 2, size=(27, 4), dtype=np.uint8)
    bits = np.repeat(base[None], m, axis=0)
    state = {'id': f'c{index}_{start}', 'bits': bits, 'rng': rng, 'burn': 0, 'production': 0,
             'moments': {}, 'diagnostics': [], 'checkpoint_refs': [], 'phase': 'START',
             'attempted_sweep': None, 'active_color': None, 'active_slice': None, 'sampler_phase': None,
             'seed': seed, 'beta': beta, 'epsilon': 1 / denom, 'M': m, 'start': start, 'working_lines': None}
    ACTIVE = state
    event('chain_started', id=state['id'], beta=beta, epsilon_denominator=denom, M=m, seed=seed, start=start,
          initial_word=base.tolist(), initial_rng_state=rng.bit_generator.state)
    chain_time = time.perf_counter()
    for burn in range(1, 65):
        state['phase'], state['attempted_sweep'] = 'BURN_SWEEP', burn
        sweep(bits, 1 / denom, rng)
        state['burn'] = burn
    state['phase'] = 'BURN_COMPLETE'
    checkpoint(state, 'burn64')
    for production in range(1, 257):
        state['phase'], state['attempted_sweep'] = 'PRODUCTION_SWEEP', production
        sweep(bits, 1 / denom, rng)
        state['phase'] = 'PRODUCTION_MEASUREMENT'
        values, diagnostic = measure(bits, 1 / denom, state['id'] + f'_p{production}')
        for key, value in values.items():
            state['moments'].setdefault(key, []).append(value)
        state['diagnostics'].append(diagnostic)
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
           'checkpoints': state['checkpoint_refs'], 'elapsed_seconds': time.perf_counter() - chain_time,
           'status': 'MIXING_UNQUALIFIED' if any(d['ESS'] is None or d['ESS'] < 16 for i, d in enumerate(diagnostics) if i != STRUCTURAL_DIAG)
                     or any(v == 0 for v in changes + time_changes) else 'CHAIN_DIAGNOSTICS_PASSED_ONLY'}
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
    lines = ['# Fixed current-parent 3D worldline pilot V001', '',
             'Finite beta, finite time step and one supplied L3 graph. Raw per-chain data, all starts and limitations are retained.', '',
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
    lines.extend(('', '__ARITHMETIC_CHECK_SUMMARY__',
                  '', 'ESS, unranked split Rhat, between-chain differences, flux histories, degree/charge histograms and all full complex matrices are in the sealed JSON/checkpoints.',
                  'Block errors can miss slow modes. Diagnostic passage does not certify equilibrium. Two time steps give sensitivity, not a rigorous Trotter bound; two beta values and one size do not establish a ground phase.',
                  'No native preparation, physical ruler/range, matter vertex, gravity, galaxy or expansion inference is earned.', ''))
    check('report_16_chain_rows', sum(line.startswith('| c') for line in lines) == 16)
    check('report_28_spatial_rows', sum(line.startswith(tuple(f'| {i} | (' for i in range(4))) for line in lines) == 28)
    check('report_four_comparison_rows', sum(line.startswith('| dt_') or line.startswith('| beta_') for line in lines) == 4)
    summary = f"Arithmetic checks: {sum(c['passed'] for c in CHECKS)}/{len(CHECKS)}; runtime {result['elapsed_seconds']:.6f} seconds."
    return '\n'.join(lines).replace('__ARITHMETIC_CHECK_SUMMARY__', summary)


def main():
    global CREATED, MANIFEST_INPUTS
    if sys.argv[1:] != ['--execute']:
        raise ValueError('Exact --execute argument required; no outputs created')
    for path in (RESULT, REPORT, RECEIPT, CP):
        if path.exists():
            raise FileExistsError('Reserved output exists: ' + str(path))
    MANIFEST_INPUTS = authenticate()
    CP.mkdir()
    CREATED = True
    manifest = {'input_sha256': MANIFEST_INPUTS, 'pid': os.getpid(), 'python': sys.version,
                'numpy': np.__version__, 'generator': 'PCG64', 'conditions': CONDITIONS, 'starts': STARTS,
                'environment': {name: os.environ.get(name) for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'PYTHONDONTWRITEBYTECODE')}}
    save('manifest.json', manifest)
    event('started', input_sha256=MANIFEST_INPUTS, manifest_sha256=STAGES['manifest.json'])
    save('controls.json', controls())
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

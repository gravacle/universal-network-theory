#!/usr/bin/env python3
"""NEW fixed beta4 continuation: local energy scores, contacts and Q response.
Root alone executes. Ancestor sampler spans are copied as bytes, never imported.
"""
import os
for _key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS'):os.environ[_key]='1'
from pathlib import Path
import ast,hashlib,itertools,json,math,sys,time,traceback,resource
import numpy as np
J=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation')
NAME='LOCAL_RECORD_FEEDBACK_3D_LOCAL_ENERGY_SOURCE_RESPONSE_V001'
SOURCE=Path(__file__).resolve();PROTOCOL=J/(NAME+'.md')
RESULT=J/(NAME+'_RESULT.json');REPORT=J/(NAME+'_RESULT.md');RECEIPT=J/(NAME+'_RECEIPT.json');ERROR=J/(NAME+'_ERROR.json')
CP=J/'local_record_feedback_3d_local_energy_source_response_v001_checkpoints'
PROTOCOL_SHA='ed426216edd6788537c3149d0a85c5d26d670ac1d7279a085bdf387435059f58'
PARENT_NAME='LOCAL_RECORD_FEEDBACK_3D_PAIR_COORDINATION_RESPONSE_V001'
PARENT_SOURCE=J/'local_record_feedback_3d_pair_coordination_response_v001.py'
PARENT_CP=J/'local_record_feedback_3d_pair_coordination_response_v001_checkpoints'
PARENT_CANONICAL='7269a6710508136d418b5c5bfa85c85691b2dcee6643bbfeeb608efc14fdee33'
PARENT_MANIFEST_SHA='26da439163fb11f25e78933706a0f993a58fac4a8cb6fbc45e3233e0eba09b77'
PARENT_CONTROL_SHA='a0758926561a56d6136cb42cd9508e4fee7035719e9490b70a17ef736d01c544'
PARENT_JOURNAL_PREFIX='78a18d159c0f82a38a4efe9e4662d9558eadde5837a00d9283bf952aaa8a26f8'
PINS={'local_record_feedback_3d_pair_coordination_response_v001.py': '0fdfd2ad3d20cd7e72a2b4e5055bfd3e422a706f85100ddfb6204f1f0f0212fb', 'LOCAL_RECORD_FEEDBACK_3D_PAIR_COORDINATION_RESPONSE_V001.md': 'e862125ece9b312e51802a4f6fe46128088a27f4077d62ba3f311db4cc8be6c7', 'LOCAL_RECORD_FEEDBACK_3D_PAIR_COORDINATION_RESPONSE_V001_RESULT.json': '74042b5f40401085c151b10b4e32cda5257ca09c86a831f1ef98965abf4649a8', 'LOCAL_RECORD_FEEDBACK_3D_PAIR_COORDINATION_RESPONSE_V001_RESULT.md': '687e4643a8268b103f7e3e6a49b831deae0d5191c82050299386c0e159d3a513', 'LOCAL_RECORD_FEEDBACK_3D_PAIR_COORDINATION_RESPONSE_V001_RECEIPT.json': '36de22839fba41a440f78d14ef24bb1930e2c1cebe0e9a9f8e1220bbc47a81c8', 'LOCAL_RECORD_FEEDBACK_WEAK_FIELD_CONSTRAINT_AND_BULK_SOURCE_JOIN_V001.md': '0ae61eb4f616133ad07fbca38d33b6a6193b404f00dcd9e76cbf09fcf5d635ab', 'LOCAL_PROPER_BOND_NORMALIZATION_V001.md': '9b4cc5e1942ac7373e210efa46bfa74e03bbcfb8130c01232373b02e8a622a5b', 'LOCAL_RECORD_FEEDBACK_FLOATING_RETURN_COMPLETION_V001.md': '255ea0ca5f86cc711cae2ff5e746d8e9b005c2156b934818ded7789f9461f2a4', 'LOCAL_RECORD_FEEDBACK_FIVE_ISLAND_PASSIVE_COMPLETION_V001.md': '124f68b600130afcb3935e11c43c1f939a804892b2794c25f89c29a0892f8693', '../FRONTIER_UPDATE_V162.md': '2330d65ce4acba10d65fc8f4702acaf159c6db66648e7e38cd863afba5ba2b13', '../../program-worktree/GRAVITY_RECORD_FIRST_WORKING_THEORY_CLOSURE_V001.md': 'cf9229586268f054b473b1641085ebafc3bca01fa0691a191cbda923ae1fa7f2'}
TERMINAL_PINS={'c0_I01': ('4421209194cf90f1b92a13945cdb8488208e91aa018de8f961db54e079154648', 'f70eb09ba52fd57c1599a1ba93ff1ccdb7d07411db468210aa0ea9bc99777325'), 'c0_I02': ('825df333285331d9b4825356e4e2425bc945fccfd88a55f94f2242fa306d9ca3', '74d436ac39bfab0a7a6208014802573532fc20d13d5709ea77544e5dfd8b29c8'), 'c0_B': ('86b6eff0512a7ed6bd0bb95d179d9e461eb189095afdcff57818ac81dc5b55da', '706ef6af14a8daa6df7d9d480fe7869bfbf370f82f9536ffdc45fd885bf514de'), 'c0_R': ('29d820bd7b83344968e2a18dcff6ada950487e357cf256669578afd52d2187b6', '39aee8c936602dfe551fe55b35b4fb21acc96a245447fbcf671c4c79311c18a6'), 'c1_I01': ('ac2a9b65a0b2cc231fd2f63ea37c2557a27d5a3729dffe714fe869c0a53ee345', 'bdacf17295448b1af0bc330c93c45f166e64a5150503bd15d979658033728f5a'), 'c1_I02': ('21eb7c64adf0f3842ef89594f447aaed57c63ae136eaa0179bd64326049d3f52', '51dabf0d85d1c4fd3a2e7853e6bbbf0113e0eb6f72127586e96b7c50ce977ee1'), 'c1_B': ('e47d0776495aa5839ae5093efee65b5707a64fc8ba5bad16090dd654b8a9f67f', '2d4da962e297ce202a85f8ec3265e582c056e4643e59ea9fb0063c5eaae8ee28'), 'c1_R': ('51717ac6ea151b9b9edb3953c9381d65c5f4281030fccfb273525a0eb545a620', 'f7993d9b6ca955d624a8cf14ad2065c5695306350eb11692c9eda8218bd442fb')}
PRESERVED_FUNCTIONS = ('degrees', 'diagonal', 'transfer', 'suffixes', 'probability',
                       'next_probability', 'inverse_cdf', 'sample_lines', 'sweep',
                       'build_cycles', 'cycle_description', 'cycle_delta', 'accept_cycle', 'cycle_sweep',
                       'deterministic_word', 'measure', 'estimates', 'summarize')


PRESERVED_CONSTANTS = ('H', 'CONDITIONS', 'STARTS', 'KS', 'COORDS', 'PORTS', 'INDEX',
                       'TARGET', 'PREVIOUS', 'PHASE', 'BPHASE', 'AFOURIER', 'EVENODD',
                       'CUTS', 'SCALAR_NAMES', 'DIAG_NAMES', 'STRUCTURAL_DIAG')


PAIR_NAMES = tuple(itertools.combinations(range(4), 2))


DIFFERENCE_TABLE = np.array(((-5, 0, 5), (-1, 0, 1), (3, 0, -3)), dtype=np.int64)


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


P_CONTRAST = np.eye(4) - np.ones((4, 4)) / 4


B_PAIRS = np.array([np.outer(P_CONTRAST[:, a], P_CONTRAST[:, b]) +
                    np.outer(P_CONTRAST[:, b], P_CONTRAST[:, a]) for a, b in PAIR_NAMES])


D_MAP = np.zeros((2, 14))


TQ_MAP = np.zeros((2, 14))


FOURIER_ONE = PHASE.sum(axis=1) / math.sqrt(27)

Q0_T[:12,:12]=np.eye(12)
Q0_T[12,12:]=1/math.sqrt(2)
D_MAP[0,:6],D_MAP[1,6:12]=.5,.5
D_MAP[0,12],D_MAP[1,13]=-.5,-.5
TQ_MAP[0,:12],TQ_MAP[1,12:]=1/math.sqrt(2),1/math.sqrt(2)
ENERGY_DIAG_NAMES=tuple(f'energy_k{k}_{s}_{part}' for k in INDEPENDENT_K for s in ('A','B') for part in (('real','power') if k==0 else ('real','imag','power')))
ALL_DIAG_NAMES=DIAG_NAMES+JOINT_DIAG_NAMES+ENERGY_DIAG_NAMES
CHECKS=[];STAGES={};ACTIVE=None;CREATED=False;CURRENT_CONTROL=None;CONTROL_ROWS=[];INPUT_FILES={};T0=0.
C0_SCOPE={'symbol':'c0=AR+Sself','sampled_constant':0,'absolute_network_energy_density':'dynamic_energy_density+c0','local_mean_E_k':'dynamic_E_k+sqrt27*c0*delta_k0*(1,1)','uniform_source_work':'54*c0*delta_N','connected_covariance_identity':'exact additive constant omitted before covariance; retained in means/work','numerical_AR_or_self_choice':None}
PHYSICAL_SCOPE={'native_hbar':1,'native_curvature_conversion':'Eunit*R_NN/c_p^4','global_coupling':'alpha_g=4pi*Gobs*Eunit/(c_p^4*ell0), counted once','Eunit_selected':False,'cp_selected':False,'inverse_computed':False,'missing_blocks':['complete B,D,J_y metric/shift blocks','qualified memory sources','matter/EM/support/controller source contacts','physical gauge/boundary quotient','absolute apparatus/body stress'],'finite_grid_scope':'beta4, two finite M, L3; conditional NN network contribution only'}

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


def recovered_summary(bits):
    da, db = degrees(bits)
    _, delta = diagonal(bits)
    phi = np.stack([(bits[:, CUTS[i], i + 1].astype(float) - 0.5).sum(axis=1) for i in range(3)], axis=1)
    hist = np.stack((np.bincount(da.ravel(), minlength=5), np.bincount(db.ravel(), minlength=5))) / (len(bits) * 27)
    return {'degree_bins': [0, 1, 2, 3, 4], 'degree_histogram_AB': hist.tolist(),
            'all_vertex_degree_histogram': hist.mean(axis=0).tolist(),
            'nonice_fraction': float(np.count_nonzero(delta) / (len(bits) * 54)),
            'mean_cut_components': phi.mean(axis=0).tolist(), 'tau0_cut_components': phi[0].tolist()}


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


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def canonical(obj):return json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def pack(value):
 a=np.asarray(value)
 return {'real':a.real.tolist(),'imag':a.imag.tolist()} if np.iscomplexobj(a) else a.tolist()
def error_safe(x):
 if isinstance(x,dict):return {k:error_safe(v) for k,v in x.items()}
 if isinstance(x,(tuple,list)):return [error_safe(v) for v in x]
 if isinstance(x,np.ndarray):return error_safe(pack(x))
 if isinstance(x,np.generic):return error_safe(x.item())
 if isinstance(x,float) and not math.isfinite(x):return {'nonfinite_float':repr(x)}
 return x
def read_json(p):return json.loads(Path(p).read_bytes())
def require(ok,label):
 if not ok:raise RuntimeError('Custody mismatch: '+label)
def check(label,passed,**evidence):
 CHECKS.append({'label':label,'passed':bool(passed),**error_safe(evidence)})
 if not passed:raise ArithmeticError(label)
def close(label,a,b,tol=3e-13):
 a,b=np.asarray(a),np.asarray(b);err=float(np.max(abs(a-b)))
 check(label,bool(np.all(np.isfinite(a)) and np.all(np.isfinite(b)) and math.isfinite(err) and err<=tol),maximum_absolute_error=err,tolerance=tol)
def norm_close(label,a,b):close(label,a,b,3e-11*max(1,float(np.linalg.norm(b))))
def exclusive(p,obj):
 with Path(p).open('xb') as f:f.write(canonical(error_safe(obj))+b'\n');f.flush();os.fsync(f.fileno())
 return sha(p)
def event(kind,**fields):
 with (CP/'journal.jsonl').open('ab') as f:f.write(canonical({'event':kind,'pid':os.getpid(),'elapsed_seconds':time.perf_counter()-T0,**fields})+b'\n');f.flush();os.fsync(f.fileno())
def save(name,obj,**fields):
 h=exclusive(CP/name,obj);STAGES[name]=h;event('stage_complete',filename=name,sha256=h,**fields);return h
def recheck():
 for p,h in INPUT_FILES.items():require(sha(Path(p))==h,'current input '+p)
def register(p,h):
 p=Path(p).resolve();require(sha(p)==h,'input seal '+str(p));require(str(p) not in INPUT_FILES or INPUT_FILES[str(p)]==h,'input alias');INPUT_FILES[str(p)]=h

def core_identity():
 sources=[PARENT_SOURCE.read_bytes(),SOURCE.read_bytes()];tables=[]
 names=PRESERVED_FUNCTIONS+PRESERVED_CONSTANTS+('joint_measure','quotient_vector','ess','rhat')
 for raw in sources:
  lines=raw.splitlines(keepends=True);nodes={}
  for n in ast.parse(raw).body:
   if isinstance(n,ast.FunctionDef) and n.name in names:nodes[n.name]=n
   elif isinstance(n,ast.Assign):
    for q in n.targets:
     if isinstance(q,ast.Name) and q.id in names:nodes[q.id]=n
  require(set(nodes)==set(names),'complete literal core spans')
  tables.append({k:(''.join([]).encode()+b''.join(lines[n.lineno-1:n.end_lineno]),ast.dump(n,include_attributes=False)) for k,n in nodes.items()})
 hashes={}
 for name in names:
  require(tables[0][name]==tables[1][name],'byte/AST identity '+name)
  hashes[name]={'source_span_sha256':hashlib.sha256(tables[0][name][0]).hexdigest(),'AST_sha256':hashlib.sha256(tables[0][name][1].encode()).hexdigest()}
 return hashes

def authenticate():
 global PARENT_RESULT
 for f,h in PINS.items():register(J/f,h)
 register(PROTOCOL,PROTOCOL_SHA);register(SOURCE,sha(SOURCE));ident=core_identity()
 p=read_json(J/(PARENT_NAME+'_RESULT.json'));r=read_json(J/(PARENT_NAME+'_RECEIPT.json'))
 require(r['input_sha256']==p['input_sha256'],'parent input identity')
 require(r['result_sha256']==sha(J/(PARENT_NAME+'_RESULT.json')) and r['report_sha256']==sha(J/(PARENT_NAME+'_RESULT.md')),'parent raw/report')
 require(r['result_canonical_sha256']==PARENT_CANONICAL==hashlib.sha256(canonical(p)).hexdigest(),'parent canonical')
 require(all(p[k]==r[k]==v for k,v in [('failed',0),('passed',180914),('check_count',180914)]),'parent arithmetic census')
 require(len(p['checks'])==180914 and all(q['passed'] for q in p['checks']),'parent checks')
 require(p['status']==r['status']=='MIXING_UNQUALIFIED','preserve parent status')
 require([q['id'] for q in p['chains']]==[f'c{i}_{s}' for i in range(4) for s in STARTS] and len(p['conditions'])==4,'all parent lineages')
 require(all(q['status']=='FINITE_GRID_PILOT_DIAGNOSTICS_PASSED' for q in p['conditions'][:2]) and all(q['status']=='MIXING_UNQUALIFIED' for q in p['conditions'][2:]),'parent beta4/beta8 dispositions')
 journal_path=PARENT_CP/'journal.jsonl';lines=journal_path.read_bytes().splitlines(keepends=True);es=[json.loads(x) for x in lines]
 require(hashlib.sha256(b''.join(lines[:-1])).hexdigest()==PARENT_JOURNAL_PREFIX==r['journal_prefix_sha256'],'parent prefix')
 require(es[-1]['event']=='receipt_complete' and es[-1]['sha256']==sha(J/(PARENT_NAME+'_RECEIPT.json')),'parent final receipt commit')
 require(len(r['checkpoint_sha256'])==342 and set(r['checkpoint_sha256'])=={x.name for x in PARENT_CP.iterdir() if x.name!='journal.jsonl'},'parent checkpoint census')
 commits=[(e.get('filename'),e.get('sha256')) for e in es]
 for f,h in r['checkpoint_sha256'].items():register(PARENT_CP/f,h);require((f,h) in commits,'parent checkpoint journal '+f)
 register(journal_path,sha(journal_path))
 require(r['checkpoint_sha256']['manifest.json']==PARENT_MANIFEST_SHA and r['checkpoint_sha256']['controls.json']==PARENT_CONTROL_SHA,'manifest/controls pin')
 manifest=read_json(PARENT_CP/'manifest.json');control=read_json(PARENT_CP/'controls.json')
 require(manifest['input_sha256']==r['input_sha256'] and manifest['conditions']==[list(c) for c in CONDITIONS],'parent manifest')
 require(any(e['event']=='started' and e['input_sha256']==r['input_sha256'] and e['manifest_sha256']==PARENT_MANIFEST_SHA for e in es),'parent start')
 for f,h in r['input_sha256'].items():
  if f=='core_identity_canonical_sha256':require(h==hashlib.sha256(canonical(manifest['preserved_core_identity'])).hexdigest(),'inherited core identity');continue
  path=PARENT_SOURCE if f=='source' else J/(PARENT_NAME+'.md') if f=='protocol' else J/f
  register(path,h)
 require(control['checks'] and all(q['passed'] for q in control['checks']) and control['all_sampler_functions_byte_AST_identical'],'sealed controls reused, not executed')
 for cid,(mh,bh) in TERMINAL_PINS.items():
  meta_path=PARENT_CP/(cid+'_production1024.json');bundle=PARENT_CP/(cid+'_production1024.npz');register(meta_path,mh);register(bundle,bh);m=read_json(meta_path)
  index=int(cid[1]);start=cid.split('_')[1];beta,denom,nt,seed=CONDITIONS[index];old=next(q for q in p['chains'] if q['id']==cid)
  ref={'metadata':meta_path.name,'bundle':bundle.name,'metadata_sha256':mh,'bundle_sha256':bh}
  require(old['checkpoints'][-1]==ref and m['id']==cid and m['phase']=='production1024','terminal ref '+cid)
  require(m['completed_burn_sweeps']==64 and m['completed_production_sweeps']==1024 and m['joint_complete_block_count']==32 and m['joint_partial_block_count']==0,'terminal counters '+cid)
  require(m['configuration']=={'beta':beta,'epsilon':1/denom,'M':nt,'start':start,'seed':seed+STARTS.index(start)+1} and m['array_shapes']['bits']==[nt,27,4],'terminal configuration '+cid)
  require(m['input_sha256']==r['input_sha256'] and m['bundle']==bundle.name and m['bundle_sha256']==bh,'terminal provenance '+cid)
  require(m['rng_state']['bit_generator']=='PCG64' and set(m['rng_state'])=={'bit_generator','state','has_uint32','uinteger'},'full RNG '+cid)
 PARENT_RESULT=p;return ident,control

def energy_measure(bits,eps,beta,old,joint,label):
 m=len(bits);da,db=degrees(bits);ca,cb=da-2,db-2
 dnode=np.stack((ca*ca-ca/2,cb*cb-cb/2),axis=2).mean(axis=0)
 kink=(bits!=np.roll(bits,-1,axis=0)).sum(axis=0,dtype=np.int64)
 if ACTIVE is not None:ACTIVE['current_measurement']['local_energy_partial']={'K_e':kink,'D_node_mean':dnode}
 check(label+'_K_integer_periodic',kink.shape==(27,4) and np.all(kink%2==0) and np.all((kink>=0)&(kink<=m)))
 check(label+'_K_global',int(kink.sum())==int(old['scalar'][7]))
 z=eps*H;th=math.tanh(z);sech2=1/math.cosh(z)**2;csch2=1/math.sinh(z)**2
 fe=m*th+kink*(1/th-th);ge=m*sech2-kink*(csch2+sech2)
 if ACTIVE is not None:ACTIVE['current_measurement']['local_energy_partial'].update(F_e=fe,G_e=ge)
 incA=fe.sum(axis=1);incB=sum(fe[PREVIOUS[a],a] for a in range(4))
 enode=dnode-H/(2*m)*np.stack((incA,incB),axis=1)
 ebar=np.einsum('kr,rs->ks',PHASE,enode,optimize=True)/math.sqrt(27)
 if ACTIVE is not None:ACTIVE['current_measurement']['local_energy_partial'].update(E_node_dynamic=enode,E_dynamic_modes=ebar)
 dbar=np.einsum('kr,rs->ks',PHASE,dnode,optimize=True)/math.sqrt(27)
 norm_close(label+'_direct_D_Q',dbar,joint['mean_Q']@D_MAP.T+FOURIER_ONE[:,None])
 norm_close(label+'_D_parent',dbar,joint['mean_D'])
 norm_close(label+'_uniform_dynamic_energy',enode.mean(),old['scalar'][0])
 norm_close(label+'_Fourier_uniform_energy',ebar[0].sum()/(2*math.sqrt(27)),old['scalar'][0])
 score=-beta*dnode+(eps*H/2)*np.stack((incA,incB),axis=1)
 norm_close(label+'_first_score_local',score,-beta*enode)
 factor=eps*eps*H*H/4;c2=np.zeros((7,2,2),complex)
 c2[:,0,0]=c2[:,1,1]=factor*ge.sum()/27
 for a in range(4):c2[:,0,1]+=factor*np.einsum('kr,kr,r->k',PHASE,PHASE[:,TARGET[a]].conj(),ge[:,a],optimize=True)/27
 c2[:,1,0]=c2[:,0,1].conj()
 global_second=eps*eps*(m*108*sech2-int(kink.sum())*(csch2+sech2))
 norm_close(label+'_uniform_second_score',27*c2[0].sum(),H*H*global_second)
 norm_close(label+'_contact_Hermitian',c2,c2.conj().transpose(0,2,1))
 norm_close(label+'_contact_conjugacy',c2[[2,4,6]],c2[[1,3,5]].conj())
 norm_close(label+'_energy_conjugacy',ebar[[2,4,6]],ebar[[1,3,5]].conj())
 norm_close(label+'_k0_real_energy',ebar[0].imag,np.zeros(2))
 q=joint['mean_Q'];values={**joint,'mean_E_dynamic':ebar,'second_E_dynamic':ebar[:,:,None]*ebar[:,None,:].conj(),
  'second_QE_dynamic':q[:,:,None]*ebar[:,None,:].conj(),'score_contact_C2':c2,
  'mean_K_edges':kink.astype(float),'mean_F_edges':fe,'mean_G_edges':ge}
 diag=[]
 for k in INDEPENDENT_K:
  for s in range(2):
   diag.append(float(ebar[k,s].real))
   if k:diag.append(float(ebar[k,s].imag))
   diag.append(float(abs(ebar[k,s])**2))
 check(label+'_fixed22_energy_diagnostics',len(diag)==22 and all(np.isfinite(v).all() for v in values.values()))
 return values,np.asarray(diag),kink,ebar

def controls(sealed):
 global CYCLES,CURRENT_CONTROL
 begin=len(CHECKS);CYCLES=build_cycles()
 require(json.loads(canonical([cycle_description(c) for c in CYCLES]))==sealed['cycle_descriptions'],'same54 sealed cycles')
 check('fixed209_diagnostics',len(ALL_DIAG_NAMES)==209 and len(ENERGY_DIAG_NAMES)==22 and len(JOINT_DIAG_NAMES)==153)
 for word in range(16):
  CURRENT_CONTROL={'stage':'NEW_LOCAL_ENERGY_WORD','word':word}
  n=np.array([(word>>a)&1 for a in range(4)],dtype=np.int64);zs=1-2*n;c=int(n.sum())-2;y=zs[PAIR_I]*zs[PAIR_J]
  check('new_local_D_'+str(word),c*c-c/2==y.sum()/2+1-c/2)
  check('new_local_c_'+str(word),2*c==-int(zs.sum()))
 first=np.zeros((27,4),np.uint8);second=first.copy();first[:,(0,1)]=1;second[:,(0,2)]=1
 words=[first,second,np.zeros((27,4),np.uint8),np.ones((27,4),np.uint8)]+[deterministic_word(w) for w in range(16)]
 for i,word in enumerate(words):
  CURRENT_CONTROL={'stage':'NEW_GRAPH_ENERGY_FOURIER','word':i}
  old,_=measure(word[None],1/16,'energy_word_old'+str(i));joint,_=joint_measure(word[None],'energy_word_joint'+str(i))
  energy_measure(word[None],1/16,1/16,old,joint,'energy_word'+str(i))
  da,db=degrees(word[None]);local=np.stack(((da-2)**2-(da-2)/2,(db-2)**2-(db-2)/2),axis=2)[0]
  direct=np.zeros((7,2),complex)
  for k,char in enumerate(KS):
   for r,coord in enumerate(COORDS):direct[k]+=complex(math.cos(-2*math.pi*np.dot(char,coord)/3),math.sin(-2*math.pi*np.dot(char,coord)/3))*local[r]/math.sqrt(27)
  norm_close('direct_owned_D_Fourier_'+str(i),direct,joint['mean_D'])
 toy=('0000','1111','0101','0011','0001','0111','0010','0110')
 bath=[]
 for denom,m in ((16,64),(32,128)):
  eps=1/denom;z=eps*H;t=math.tanh(z);sech2=1/math.cosh(z)**2;csch2=1/math.sinh(z)**2
  matrix=np.array([[math.cosh(z),math.sinh(z)],[math.sinh(z),math.cosh(z)]])
  x=np.array([[0,1],[1,0]]);d1=(eps*H/2)*(x@matrix);d2=(eps*H/2)**2*matrix
  for i in range(2):
   for k in range(2):
    first=d1[i,k]/matrix[i,k];second=d2[i,k]/matrix[i,k]-first*first
    norm_close(f'transfer_first_{denom}_{i}{k}',first,(eps*H/2)*(t if i==k else 1/t))
    norm_close(f'transfer_second_{denom}_{i}{k}',second,(eps*H/2)**2*(sech2 if i==k else -csch2))
  for w in toy:
   CURRENT_CONTROL={'stage':'NEW_PERIODIC_SCORE_CONTROL','grid':denom,'word':w}
   ns=np.tile(np.array([int(a) for a in w]),m//4);diff=ns!=np.roll(ns,-1);kk=int(diff.sum())
   check('toy_periodic_even_'+str((denom,w)),kk%2==0)
   literal_first=sum(d1[i,k]/matrix[i,k] for i,k in zip(ns,np.roll(ns,-1)))
   literal_second=sum(d2[i,k]/matrix[i,k]-(d1[i,k]/matrix[i,k])**2 for i,k in zip(ns,np.roll(ns,-1)))
   norm_close('toy_F_'+str((denom,w)),literal_first,(eps*H/2)*(m*t+kk*(1/t-t)))
   norm_close('toy_G_'+str((denom,w)),literal_second,(eps*H/2)**2*(m*sech2-kk*(csch2+sech2)))
  for numerator,denominator in ((4,5),(1,1),(6,5)):
   scale=numerator/denominator;epsc=eps/scale;tp=np.array([[math.cosh(epsc*H*scale),math.sinh(epsc*H*scale)],[math.sinh(epsc*H*scale),math.cosh(epsc*H*scale)]])
   norm_close('proper_bath_transfer_'+str((denom,numerator,denominator)),tp,matrix)
   norm_close('proper_bath_diagonal_coefficient_'+str((denom,numerator,denominator)),epsc*scale,eps)
   norm_close('proper_bath_identity_coefficient_'+str((denom,numerator,denominator)),(4/scale)*scale,4)
   bath.append({'epsilon_denominator':denom,'L_rational':str(numerator)+'/'+str(denominator),'beta_coordinate':4/scale,'beta_proper':4,'weight_invariant':True,'F_coordinate':'L*F_proper','complete_second_uniform_curvature':0,'scope':'whole specified action, symbolic constant and bath scaled together; distinct from fixed-coordinate NN response'})
 CURRENT_CONTROL=None
 return {'checks':CHECKS[begin:].copy(),'cycles':[cycle_description(c) for c in CYCLES],
  'sampler_control_reused_sha256':PARENT_CONTROL_SHA,'sampler_enumerations_replayed':False,
  'new_controls':'local16words, named20graphwords, two transfer grids, eight fixed periodic words, three proper-bath scales',
  'proper_bath_controls':bath,'diagnostic_count':209,'qualified_nonstructural_count':208,'C0_scope':C0_SCOPE}

def energy_estimates(raw,beta):
 e,q=raw['mean_E_dynamic'],raw['mean_Q'];ec=raw['second_E_dynamic']-e[:,:,None]*e[:,None,:].conj()
 qq=raw['second_Q']-q[:,:,None]*q[:,None,:].conj()
 qe=raw['second_QE_dynamic']-q[:,:,None]*e[:,None,:].conj()
 c2=raw['score_contact_C2'];r=-beta*ec-c2/beta
 return {'mean_E_dynamic':e,'mean_Q':q,'mean_D':raw['mean_D'],'mean_K_edges':raw['mean_K_edges'],
  'mean_F_edges':raw['mean_F_edges'],'mean_G_edges':raw['mean_G_edges'],
  'energy_covariance':ec,'chi_EE':beta*ec,'chi_QQ':beta*qq,'chi_QE':beta*qe,
  'chi_EQ':beta*qe.conj().transpose(0,2,1),'score_contact_C2':c2,'R_NN':r,
  'R_NN_eigenvalues':np.linalg.eigvalsh((r+r.conj().transpose(0,2,1))/2),
  'uniform_R_density':r[0].sum().real/2,'uniform_contact_density':c2[0].sum().real/2,
  'uniform_energy_susceptibility_density':beta*ec[0].sum().real/2,
  'mean_dynamic_energy_density':e[0].sum().real/(2*math.sqrt(27))}

def component_summary(blocks,beta,label):
 b=len(blocks['mean_E_dynamic']);raw={k:v.mean(axis=0) for k,v in blocks.items()};central=energy_estimates(raw,beta)
 replicas={k:[] for k in central}
 for i in range(b):
  leave={k:(b*v.mean(axis=0)-v[i])/(b-1) for k,v in blocks.items()}
  for k,v in energy_estimates(leave,beta).items():replicas[k].append(v)
 errors={};arrays={}
 for k,vs in replicas.items():
  a=np.asarray(vs);arrays[k]=a;re=np.sqrt((b-1)/b*np.sum((a.real-a.real.mean(axis=0))**2,axis=0))
  errors[k]={'real_se':re,'imag_se':np.sqrt((b-1)/b*np.sum((a.imag-a.imag.mean(axis=0))**2,axis=0))} if np.iscomplexobj(a) else {'se':re}
 norm_close(label+'_R_Hermitian',central['R_NN'],central['R_NN'].conj().transpose(0,2,1))
 for k in ('R_NN','score_contact_C2','chi_QE','chi_EQ'):
  norm_close(label+'_negative_character_'+k,central[k][[2,4,6]],central[k][[1,3,5]].conj())
 norm_close(label+'_reverse_cross',central['chi_EQ'],central['chi_QE'].conj().transpose(0,2,1))
 norm_close(label+'_uniform_contact_curvature',central['uniform_R_density'],-central['uniform_energy_susceptibility_density']-central['uniform_contact_density']/beta)
 return central,errors,arrays

def serialize_estimates(central,errors):
 return {'estimates':{k:pack(v) for k,v in central.items()},'component_errors':{k:{part:pack(v) for part,v in error.items()} for k,error in errors.items()}}

def append_measurement(state,old,diag,joint,jdiag,energy,ediag,kink,ebar):
 for k,v in old.items():state['moments'].setdefault(k,[]).append(v)
 state['diagnostics'].append(np.r_[diag,jdiag,ediag]);state['joint_vectors'].append(joint['mean_Q']);state['energy_vectors'].append(ebar);state['kink_vectors'].append(kink)
 for k,v in energy.items():state['partial_sums'][k]=state['partial_sums'].get(k,np.zeros_like(v))+v
 state['partial_count']+=1
 if state['partial_count']==32:
  for k,v in state['partial_sums'].items():state['block_sums'].setdefault(k,[]).append(v)
  state['partial_sums']={};state['partial_count']=0
def checkpoint(state,phase):
 stem=state['id']+'_'+phase;arrays={'bits':state['bits']}
 for key,name in (('working_lines','active_partial_line_bits_255_unsampled'),('working_cycle_proposal','active_six_column_cycle_proposal')):
  if state.get(key) is not None:arrays[name]=state[key]
 arrays.update({k:np.asarray(v) for k,v in state['moments'].items()})
 arrays['diagnostic_traces']=np.asarray(state['diagnostics']).reshape(-1,209)
 arrays['bar_Q_every_production_measurement']=np.asarray(state['joint_vectors'],complex).reshape(-1,7,14)
 arrays['E_dynamic_every_production_measurement']=np.asarray(state['energy_vectors'],complex).reshape(-1,7,2)
 arrays['K_e_every_production_measurement']=np.asarray(state['kink_vectors'],np.int64).reshape(-1,27,4)
 arrays['cycle_attempts_burn_production']=state['cycle_attempts'];arrays['cycle_acceptances_burn_production']=state['cycle_acceptances']
 arrays['production_cycle_acceptance_traces']=np.asarray(state['cycle_traces'],np.int64).reshape(-1,54)
 count=state['production']//32;arrays['complete_block_counts']=np.full(count,32,np.int64)
 for k,vs in state['moments'].items():
  if count:
   a=np.asarray(vs)[:count*32];arrays['old_block_sufficient_sums_'+k]=a.reshape(count,32,*a.shape[1:]).sum(axis=1)
 for k,vs in state['block_sums'].items():arrays['source_block_sufficient_sums_'+k]=np.asarray(vs)
 for k,v in state['partial_sums'].items():arrays['source_partial_block_sufficient_sum_'+k]=v
 bundle=CP/(stem+'.npz')
 with bundle.open('xb') as f:np.savez(f,**arrays);f.flush();os.fsync(f.fileno())
 h=sha(bundle);STAGES[bundle.name]=h
 event('checkpoint_bundle',id=state['id'],phase=phase,filename=bundle.name,sha256=h,completed_burn_sweeps=state['burn'],completed_production_sweeps=state['production'])
 meta={'id':state['id'],'phase':phase,'completed_burn_sweeps':state['burn'],'completed_production_sweeps':state['production'],
  'configuration':{k:state[k] for k in ('seed','beta','epsilon','M','start')},'rng_state':state['rng'].bit_generator.state,
  'input_sha256':MANIFEST_INPUTS,'bundle':bundle.name,'bundle_sha256':h,'array_shapes':{k:list(v.shape) for k,v in arrays.items()},
  'source_terminal_reference':state['source_terminal_reference'],'original_completed_counters':{'burn_sweeps':64,'production_sweeps':1024},
  'complete_block_count':len(state['block_sums'].get('mean_Q',[])),'partial_block_count':state['partial_count'],'symbolic_identity_source':C0_SCOPE,
  'active_context':{k:state.get(k) for k in ('phase','attempted_sweep','active_color','active_slice','sampler_phase','active_cycle','cycle_delta_D','cycle_log_ratio','cycle_uniform','cycle_accepted')},
  'raw_moment_scope':'complete32 and active partial sufficient sums before all covariance/mean subtraction; all Ke/Q/E production traces paired'}
 mh=save(stem+'.json',meta);state['checkpoint_refs'].append({'metadata':stem+'.json','bundle':bundle.name,'metadata_sha256':mh,'bundle_sha256':h})

def recover_chain(index,beta,denom,m,seed,start):
 cid=f'c{index}_{start}';mp=PARENT_CP/(cid+'_production1024.json');bp=PARENT_CP/(cid+'_production1024.npz')
 require((sha(mp),sha(bp))==TERMINAL_PINS[cid],'terminal before load '+cid);meta=read_json(mp)
 with np.load(bp,allow_pickle=False) as z:
  saved=z['bits'];bits=saved.copy();check(cid+'_copied_terminal_bits',np.array_equal(bits,saved) and hashlib.sha256(bits.tobytes()).hexdigest()==hashlib.sha256(saved.tobytes()).hexdigest())
 check(cid+'_binary_shape_dtype',bits.dtype==np.uint8 and bits.shape==(m,27,4) and np.all((bits==0)|(bits==1)))
 rng=np.random.Generator(np.random.PCG64(0));rng.bit_generator.state=meta['rng_state']
 check(cid+'_restored_full_rng',rng.bit_generator.state==meta['rng_state'])
 require((sha(mp),sha(bp))==TERMINAL_PINS[cid],'terminal after load '+cid)
 return bits,rng,{'metadata':str(mp.relative_to(J)),'bundle':str(bp.relative_to(J)),'metadata_sha256':TERMINAL_PINS[cid][0],'bundle_sha256':TERMINAL_PINS[cid][1]}

def histograms(values):
 return [{'values':v.tolist(),'counts':n.tolist()} for v,n in (np.unique(values[:,i],return_counts=True) for i in range(3))]

def segment_comparison(old,central,errors,newstatus):
 out={}
 for k,v in central.items():
  ov=old['estimates'][k];ov=np.asarray(ov['real'])+1j*np.asarray(ov['imag']) if isinstance(ov,dict) else np.asarray(ov)
  out[k]={'signed_new_minus_old':pack(v-ov),'old_component_se':old['component_errors'][k],'new_component_se':{part:pack(x) for part,x in errors[k].items()}}
 return {'quantities':out,'old_status':old['status'],'new_status':newstatus,'interpretation':'CORRELATED_SUCCESSIVE_SEGMENTS_SEPARATE_ERRORS_NO_INDEPENDENT_COMBINATION'}

def parent_joint_comparison(old,central,errors,newstatus):
 out={}
 for k,oldkey in (('mean_Q','mean_Q'),('mean_D','mean_D'),('chi_QQ','chi_joint')):
  ov=old['joint_estimates'][oldkey];ov=np.asarray(ov['real'])+1j*np.asarray(ov['imag']) if isinstance(ov,dict) else np.asarray(ov)
  out[k]={'signed_new_minus_old':pack(central[k]-ov),'old_component_se':old['joint_component_errors'][oldkey],'new_component_se':{part:pack(x) for part,x in errors[k].items()}}
 return {'quantities':out,'old_status':old['status'],'new_status':newstatus,'old_spatial_energy_response':'UNAVAILABLE_NOT_BACKFILLED','interpretation':'CORRELATED_SUCCESSIVE_SEGMENTS_SEPARATE_ERRORS_NO_INDEPENDENT_COMBINATION'}

def run_chain(index,beta,denom,m,seed,start):
 global ACTIVE
 bits,rng,terminal=recover_chain(index,beta,denom,m,seed,start)
 state={'id':f'c{index}_{start}','bits':bits,'rng':rng,'burn':0,'production':0,'moments':{},'diagnostics':[],
  'joint_vectors':[],'energy_vectors':[],'kink_vectors':[],'block_sums':{},'partial_sums':{},'partial_count':0,'checkpoint_refs':[],
  'seed':seed,'beta':beta,'epsilon':1/denom,'M':m,'start':start,'source_terminal_reference':terminal,
  'phase':'SEGMENT_INITIAL','attempted_sweep':None,'active_color':None,'active_slice':None,'sampler_phase':None,'working_lines':None,
  'working_cycle_proposal':None,'active_cycle':None,'cycle_delta_D':None,'cycle_log_ratio':None,'cycle_uniform':None,'cycle_accepted':None,
  'cycle_attempts':np.zeros((2,54),np.int64),'cycle_acceptances':np.zeros((2,54),np.int64),'cycle_traces':[],'current_measurement':{}}
 ACTIVE=state;initial=recovered_summary(bits);began=time.perf_counter()
 event('chain_started',id=state['id'],configuration={k:state[k] for k in ('seed','beta','epsilon','M','start')},source_terminal_reference=terminal,initial_rng_state=rng.bit_generator.state,recovered_bits_sha256=hashlib.sha256(bits.tobytes()).hexdigest(),original_completed_counters={'burn_sweeps':64,'production_sweeps':1024},initial_summary=initial)
 checkpoint(state,'segment_initial')
 for burn in range(1,65):
  state['phase']='BURN_SWEEP';state['attempted_sweep']=burn;sweep(bits,1/denom,rng);cycle_sweep(state,0);state['burn']=burn
 state['phase']='BURN_COMPLETE';checkpoint(state,'burn64')
 for prod in range(1,1025):
  state['phase']='PRODUCTION_SWEEP';state['attempted_sweep']=prod;sweep(bits,1/denom,rng);accepted=cycle_sweep(state,1)
  state['current_accepted_cycle_vector']=accepted
  state['current_measurement']={};state['phase']='PRODUCTION_MEASUREMENT_OLD';old,diag=measure(bits,1/denom,state['id']+f'_old{prod}')
  state['current_measurement']['old_values']=old;state['current_measurement']['old_diagnostic']=diag
  state['phase']='PRODUCTION_MEASUREMENT_JOINT';joint,jdiag=joint_measure(bits,state['id']+f'_joint{prod}')
  state['current_measurement']['joint_values']=joint;state['current_measurement']['joint_diagnostic']=jdiag
  state['phase']='PRODUCTION_MEASUREMENT_ENERGY';energy,ediag,kink,ebar=energy_measure(bits,1/denom,beta,old,joint,state['id']+f'_energy{prod}')
  state['current_measurement']['energy_values']=energy;state['current_measurement']['energy_diagnostic']=ediag
  append_measurement(state,old,diag,joint,jdiag,energy,ediag,kink,ebar);state['cycle_traces'].append(accepted)
  state['production']=prod;state['phase']='PRODUCTION_MEASUREMENT_COMPLETE';state['current_measurement']={}
  state['current_accepted_cycle_vector']=None
  if prod%128==0:
   checkpoint(state,'production'+str(prod));print(json.dumps({'id':state['id'],'production':prod,'elapsed_seconds':time.perf_counter()-T0}),flush=True)
 moments={k:np.asarray(v) for k,v in state['moments'].items()};oldblocks={k:v.reshape(32,32,*v.shape[1:]).mean(axis=1) for k,v in moments.items()}
 blocks={k:np.asarray(v)/32 for k,v in state['block_sums'].items()}
 check(state['id']+'_full32_source_blocks',state['partial_count']==0 and len(state['joint_vectors'])==1024 and all(len(v)==32 for v in blocks.values()))
 oldcentral,olderrors=summarize(oldblocks,beta,state['id']);central,errors,replicas=component_summary(blocks,beta,state['id'])
 norm_close(state['id']+'_old_coord_QQ',central['chi_QQ'][:,12:,12:],oldcentral['chi_coord'])
 norm_close(state['id']+'_old_energy_central',central['mean_dynamic_energy_density'],oldcentral['scalars'][0])
 traces=np.asarray(state['diagnostics']);check(state['id']+'_209_trace_shape',traces.shape==(1024,209))
 diagnostics=[{'name':name,**({'status':'STRUCTURAL_NULL','ESS':None,'tau':None} if i==STRUCTURAL_DIAG else ess(traces[:,i]))} for i,name in enumerate(ALL_DIAG_NAMES)]
 phi=moments['scalar'][:,11:14];pt=moments['scalar'][:,8:11];ice=moments['scalar'][:,14].astype(bool)
 changes=np.count_nonzero(np.diff(phi,axis=0),axis=0).tolist();tchanges=np.count_nonzero(np.diff(pt,axis=0),axis=0).tolist();words,counts=np.unique(phi[ice],axis=0,return_counts=True)
 check(state['id']+'_exact_cycle_attempts',np.array_equal(state['cycle_attempts'],np.repeat(np.array((64,1024))[:,None],54,axis=1)))
 check(state['id']+'_acceptance_bounds',np.all(state['cycle_acceptances']>=0) and np.all(state['cycle_acceptances']<=state['cycle_attempts']))
 check(state['id']+'_acceptance_trace_sum',np.array_equal(np.asarray(state['cycle_traces']).sum(axis=0),state['cycle_acceptances'][1]))
 check(state['id']+'_ten_checkpoints',len(state['checkpoint_refs'])==10)
 passed=all(d['ESS'] is not None and d['ESS']>=32 for i,d in enumerate(diagnostics) if i!=STRUCTURAL_DIAG) and all(x>0 for x in changes+tchanges)
 status='CHAIN_DIAGNOSTICS_PASSED_ONLY' if passed else 'MIXING_UNQUALIFIED';cycle_rows,pair_rows=acceptance_summary(state)
 row={'id':state['id'],'condition':index,'start':start,'seed':seed,'beta':beta,'epsilon':1/denom,'M':m,'burn_sweeps':64,'production_sweeps':1024,'status':status,
  **serialize_estimates(central,errors),'old_estimates':{k:pack(v) for k,v in oldcentral.items()},'old_component_errors':{k:{part:pack(v) for part,v in er.items()} for k,er in olderrors.items()},
  'block_counts':[32]*32,'block_raw_moments':{k:pack(v) for k,v in blocks.items()},'block_sufficient_sums':{k:pack(32*v) for k,v in blocks.items()},
  'old_block_raw_moments':{k:pack(v) for k,v in oldblocks.items()},'old_block_sufficient_sums':{k:pack(32*v) for k,v in oldblocks.items()},
  'diagnostic_names':ALL_DIAG_NAMES,'ESS_diagnostics':diagnostics,'diagnostic_traces':traces.tolist(),
  'scalar_names':SCALAR_NAMES,'scalar_traces':moments['scalar'].tolist(),'base_cut_change_counts':changes,'time_averaged_cut_change_counts':tchanges,
  'base_cut_histograms':histograms(phi),'time_averaged_cut_histograms':histograms(pt),'ice_labeled_base_cut_histogram':{'vectors':words.tolist(),'counts':counts.tolist()},
  'ice_slice_count':int(ice.sum()),'undefined_winding_slice_count':int((~ice).sum()),
  'consecutive_ice_winding_changes':sum(bool(np.any(phi[i]!=phi[i-1])) for i in range(1,1024) if ice[i] and ice[i-1]),
  'cycle_acceptance_rows':cycle_rows,'pair_acceptance_rows':pair_rows,'production_cycle_acceptance_traces':np.asarray(state['cycle_traces']).tolist(),
  'checkpoints':state['checkpoint_refs'],'source_terminal_reference':terminal,'initial_recovered_summary':initial,
  'elapsed_seconds':time.perf_counter()-began,'C0_scope':C0_SCOPE,'physical_scope':PHYSICAL_SCOPE,
  'new_Ke_Q_E_traces':'lossless in every prefix/terminal NPZ; exact paired measurement order','replicas':'all32 nonlinear covariance/contact/eigen replicas computed jointly, component errors retained',
  'histogram_bins':{'degree':[0,1,2,3,4],'delta':[-2,-1,0,1,2],'oriented':[-2,-1,0,1,2]}}
 oldrow=next(r for r in PARENT_RESULT['chains'] if r['id']==state['id'])
 row['old_new_segment_comparison']=segment_comparison(oldrow,oldcentral,olderrors,status)
 row['old_new_pair_coordination_comparison']=parent_joint_comparison(oldrow,central,errors,status)
 save(state['id']+'_complete.json',row,id=state['id']);event('chain_complete',id=state['id'],status=status,production_sweeps=1024);ACTIVE=None
 return {'row':row,'blocks':blocks,'oldblocks':oldblocks,'central':central,'errors':errors,'oldcentral':oldcentral,'olderrors':olderrors,'traces':traces}

def signed_difference(a,ae,b,be,independent):
 result={}
 for k,v in a.items():
  error={part:pack(np.sqrt(ae[k][part]**2+be[k][part]**2)) for part in ae[k]} if independent else {'first':{part:pack(x) for part,x in ae[k].items()},'second':{part:pack(x) for part,x in be[k].items()}}
  result[k]={'signed_first_minus_second':pack(v-b[k]),'component_errors':error}
 return {'quantities':result,'interpretation':'SEPARATE_CHAIN_STREAMS_COMPONENT_ERRORS_COMBINED' if independent else 'CORRELATED_SEGMENTS_SEPARATE_ERRORS'}

def condition_summary(index,beta,denom,m,records):
 blocks={k:np.concatenate([r['blocks'][k] for r in records]) for k in records[0]['blocks']}
 oldblocks={k:np.concatenate([r['oldblocks'][k] for r in records]) for k in records[0]['oldblocks']}
 central,errors,_=component_summary(blocks,beta,'condition'+str(index));oldcentral,olderrors=summarize(oldblocks,beta,'condition'+str(index))
 norm_close('condition'+str(index)+'_old_QQ_cc',central['chi_QQ'][:,12:,12:],oldcentral['chi_coord'])
 norm_close('condition'+str(index)+'_old_energy',central['mean_dynamic_energy_density'],oldcentral['scalars'][0])
 split=[{'name':name,**({'status':'STRUCTURAL_NULL','Rhat':None} if i==STRUCTURAL_DIAG else rhat(np.array([r['traces'][:,i] for r in records])))} for i,name in enumerate(ALL_DIAG_NAMES)]
 passed=all(r['row']['status']=='CHAIN_DIAGNOSTICS_PASSED_ONLY' for r in records) and all(x['Rhat'] is not None and x['Rhat']<=1.10 for i,x in enumerate(split) if i!=STRUCTURAL_DIAG)
 status='FINITE_GRID_LOCAL_ENERGY_SOURCE_DIAGNOSTICS_PASSED' if passed else 'MIXING_UNQUALIFIED'
 between=[]
 for a in range(4):
  for b in range(a+1,4):between.append({'first':records[a]['row']['id'],'second':records[b]['row']['id'],**signed_difference(records[a]['central'],records[a]['errors'],records[b]['central'],records[b]['errors'],True)})
 row={'condition':index,'beta':beta,'epsilon':1/denom,'M':m,'chain_ids':[r['row']['id'] for r in records],'status':status,
  **serialize_estimates(central,errors),'old_estimates':{k:pack(v) for k,v in oldcentral.items()},'old_component_errors':{k:{part:pack(v) for part,v in er.items()} for k,er in olderrors.items()},
  'pooled_block_counts':[32]*128,'pooled_block_raw_moments':{k:pack(v) for k,v in blocks.items()},'pooled_block_sufficient_sums':{k:pack(32*v) for k,v in blocks.items()},
  'old_pooled_block_raw_moments':{k:pack(v) for k,v in oldblocks.items()},'split_Rhat':split,'between_chain_differences':between,'C0_scope':C0_SCOPE,'physical_scope':PHYSICAL_SCOPE}
 oldrow=next(r for r in PARENT_RESULT['conditions'] if r['condition']==index)
 row['old_new_segment_comparison']=segment_comparison(oldrow,oldcentral,olderrors,status)
 row['old_new_pair_coordination_comparison']=parent_joint_comparison(oldrow,central,errors,status)
 save('condition'+str(index)+'_complete.json',row);return {'row':row,'central':central,'errors':errors,'oldcentral':oldcentral,'olderrors':olderrors}

def format_report(result):
 out=['# Same-parent local energy source response V001','',f"Status: {result['status']}. All eight beta4 lineages, seven modes and 209 primitive traces retained; one structural charge-odd null excluded. All numbers are fixed-coordinate finite-M network contributions. Symbolic c0=AR+Sself is retained in first means/work; no AR/self value is selected.",'',
  '| Dataset | Status | Minimum nonstructural ESS | Maximum defined Rhat | Dynamic energy density | Uniform R_NN density |','|---|---|---:|---:|---:|---:|']
 for row in result['chains']+result['conditions']:
  name=row.get('id','condition'+str(row.get('condition')));ds=row.get('ESS_diagnostics',[]);rs=row.get('split_Rhat',[])
  es=[x['ESS'] for x in ds if x.get('ESS') is not None];rh=[x['Rhat'] for x in rs if x.get('Rhat') is not None]
  v=row['estimates'];se=row['component_errors'];out.append('|%s|%s|%s|%s|%.12g ± %.3g|%.12g ± %.3g|'%(name,row['status'],min(es) if es else '',max(rh) if rh else '',v['mean_dynamic_energy_density'],se['mean_dynamic_energy_density']['se'],v['uniform_R_density'],se['uniform_R_density']['se']))
 out+=['','Absolute network energy density = displayed dynamic density + c0; normalized k0 E_A/B means each acquire sqrt27*c0. Uniform identity source work=54*c0*delta_N. Complete proper-bath uniform curvature=0 when the whole action/bath is scaled, distinct from displayed fixed-coordinate R_NN. Physical additive H_NN contact=0; transfer C2 is mandatory.','',
  'The complete signed matrices/errors below are per A/B normalized cell mode. Uniform per-vertex contraction is sum(R_NN[k0])/2. Pair/coordination cross responds with minus chi_QE to a plus energy source. All negative characters are retained.']
 for row in result['chains']+result['conditions']:
  name=row.get('id','condition'+str(row.get('condition')));out+=['','## '+name,'',row['status']+'. Full matrix Re/Im estimates and separate component SE follow.']
  for k,char in enumerate(KS):
   display={'character':char}
   for key in ('mean_E_dynamic','mean_Q','mean_D','R_NN','score_contact_C2','chi_QE','chi_EQ','R_NN_eigenvalues'):
    v=row['estimates'][key];display[key]={'estimate':{p:v[p][k] for p in ('real','imag')} if isinstance(v,dict) else v[k],
      'component_se':{p:se[k] for p,se in row['component_errors'][key].items()}}
   out+=['','```json',json.dumps(display,sort_keys=True,separators=(',',':'),allow_nan=False),'```']
  if 'ESS_diagnostics' in row:
   refusals=[x for i,x in enumerate(row['ESS_diagnostics']) if i!=STRUCTURAL_DIAG and (x['ESS'] is None or x['ESS']<32)]
   out+=['','ESS refusals: '+json.dumps(refusals,separators=(',',':')),'Base/time cut changes: '+json.dumps([row['base_cut_change_counts'],row['time_averaged_cut_change_counts']])+'. Both unconditional cut histograms, ice labels/undefined counts and all 209 traces are in the sealed row/bundles.']
  else:out+=['','Rhat refusals: '+json.dumps([x for i,x in enumerate(row['split_Rhat']) if i!=STRUCTURAL_DIAG and (x['Rhat'] is None or x['Rhat']>1.10)],separators=(',',':'))]
  out+=['','Old/new means retain the old and new component errors separately in JSON; they are correlated successive segments. All signed between-start differences and time-grid component errors are retained.']
 out+=['','## Signed time-grid comparison','',json.dumps(result['grid_comparison'],sort_keys=True,separators=(',',':')),'',
  'Missing retained blocks: '+', '.join(PHYSICAL_SCOPE['missing_blocks'])+'. No inverse, empirical eigenmode quotient, thermal continuum/ground phase, complete polarization or gravity success is inferred. Historical beta8 refusals are retained from the parent and are not rerun.',
  '']
 check('report_ten_dataset_rows',sum(x.startswith('|c') for x in out)==10)
 check('report_seventy_mode_blocks',sum(x.startswith('```json') for x in out)==70)
 out.append(f"Arithmetic: {len(CHECKS)}/{len(CHECKS)} passed. Checkpoint census: 80 bundles and metadata, eight complete chains, two pooled conditions; all literal sampler controls authenticated as sealed bytes.")
 return '\n'.join(out)+'\n'

def main():
 global T0,CREATED,MANIFEST_INPUTS
 if sys.argv[1:]!=['--execute']:raise SystemExit('Requires exact root --execute.')
 require(not any(p.exists() for p in (RESULT,REPORT,RECEIPT,ERROR,CP)),'exclusive new output paths')
 T0=time.perf_counter();ident,sealed=authenticate();recheck();CP.mkdir();CREATED=True;MANIFEST_INPUTS=INPUT_FILES.copy()
 mh=exclusive(CP/'manifest.json',{'pid':os.getpid(),'input_sha256':MANIFEST_INPUTS,'preserved_core_identity':ident,'conditions':[list(c) for c in CONDITIONS],'executed_condition_indices':[0,1],
  'segment_budget':{'burn':64,'production':1024,'block':32,'checkpoints_per_chain':10,'chains':8,'diagnostics':209,'qualified_nonstructural':208},
  'starts_as_lineage_labels':STARTS,'terminal_pins':TERMINAL_PINS,'C0_scope':C0_SCOPE,'physical_scope':PHYSICAL_SCOPE,
  'environment':{'python':sys.version,'numpy':np.__version__,'thread_policy':'one numeric thread'}})
 STAGES['manifest.json']=mh;event('started',input_sha256=MANIFEST_INPUTS,manifest_sha256=mh)
 ctrl=controls(sealed);save('controls.json',ctrl);chains=[];pooled=[];records=[]
 for index in (0,1):
  beta,denom,m,base=CONDITIONS[index];group=[]
  for i,start in enumerate(STARTS):
   r=run_chain(index,beta,denom,m,base+i+1,start);group.append(r);chains.append(r['row'])
  pr=condition_summary(index,beta,denom,m,group);pooled.append(pr['row']);records.append(pr)
 check('fixed8_chain2_condition_census',len(chains)==8 and len(pooled)==2)
 check('fixed80_checkpoint_bundles',sum(p.endswith('.npz') for p in STAGES)==80)
 check('fixed172_checkpoint_files',len(STAGES)==172);recheck()
 grid=signed_difference(records[0]['central'],records[0]['errors'],records[1]['central'],records[1]['errors'],True)
 status='FINITE_GRID_LOCAL_ENERGY_SOURCE_DIAGNOSTICS_PASSED' if all(r['status']=='FINITE_GRID_LOCAL_ENERGY_SOURCE_DIAGNOSTICS_PASSED' for r in pooled) else 'MIXING_UNQUALIFIED'
 result={'status':status,'failed':0,'passed':len(CHECKS),'check_count':len(CHECKS),'checks':CHECKS.copy(),'chains':chains,'conditions':pooled,'grid_comparison':grid,
  'parent_status':PARENT_RESULT['status'],'parent_condition_statuses':[{'condition':r['condition'],'status':r['status']} for r in PARENT_RESULT['conditions']],
  'C0_scope':C0_SCOPE,'physical_scope':PHYSICAL_SCOPE,'mode_order':KS,'Q_order':Q_NAMES,'diagnostic_names':ALL_DIAG_NAMES,
  'input_sha256':MANIFEST_INPUTS,'pid':os.getpid(),'elapsed_seconds':time.perf_counter()-T0,'complete_kernel_quotient':'only inherited k0 charge-odd null; no energy null deleted','covariance_inverse':None}
 report=format_report(result);result['passed']=result['check_count']=len(CHECKS);result['checks']=CHECKS.copy()
 raw=exclusive(RESULT,result);ch=hashlib.sha256(canonical(result)).hexdigest();event('result_complete',sha256=raw,canonical_sha256=ch)
 with REPORT.open('x') as f:f.write(report);f.flush();os.fsync(f.fileno())
 rh=sha(REPORT);event('report_complete',sha256=rh,data_rows=10,mode_blocks=70)
 recheck();cm={p.name:sha(p) for p in CP.iterdir() if p.name!='journal.jsonl'};require(cm==STAGES,'final checkpoint seals')
 receipt={'status':status,'failed':0,'passed':len(CHECKS),'check_count':len(CHECKS),'input_sha256':MANIFEST_INPUTS,'checkpoint_sha256':cm,
  'result_sha256':raw,'result_canonical_sha256':ch,'report_sha256':rh,'journal_prefix_sha256':sha(CP/'journal.jsonl'),'pid':os.getpid(),
  'elapsed_seconds':time.perf_counter()-T0,'chain_count':8,'condition_count':2,'checkpoint_bundle_count':80,'mode_count':7}
 rr=exclusive(RECEIPT,receipt);event('receipt_complete',sha256=rr)
 print(json.dumps({'status':status,'passed':len(CHECKS),'failed':0,'result_sha256':raw,'receipt_sha256':rr}),flush=True)

if __name__=='__main__':
 try:main()
 except Exception as e:
  if CREATED and not ERROR.exists():
   prefix=None
   if ACTIVE is not None:
    try:checkpoint(ACTIVE,'error_prefix');prefix=ACTIVE['checkpoint_refs'][-1]
    except Exception as ce:prefix={'checkpoint_error':repr(ce)}
   evidence={'status':'ARITHMETIC_FAILED' if isinstance(e,ArithmeticError) else 'EXECUTION_ERROR_PRESERVED','error':repr(e),'traceback':traceback.format_exc(),
    'input_sha256':INPUT_FILES,'source_sha256':sha(SOURCE),'checks':CHECKS,'completed_sha256':STAGES,'active_control':CURRENT_CONTROL,'failed_prefix':prefix,
    'active_context':None if ACTIVE is None else {k:v for k,v in ACTIVE.items() if k not in ('bits','rng','moments','joint_vectors','energy_vectors','kink_vectors','block_sums','partial_sums','diagnostics','working_lines','working_cycle_proposal')},
    'full_rng_state':None if ACTIVE is None else ACTIVE['rng'].bit_generator.state,
    'current_partial_sums':None if ACTIVE is None else ACTIVE['partial_sums'],'current_measurement':None if ACTIVE is None else ACTIVE['current_measurement']}
   h=exclusive(ERROR,error_safe(evidence));event('error',sha256=h,status=evidence['status'])
  print(traceback.format_exc(),file=sys.stderr);sys.exit(3)

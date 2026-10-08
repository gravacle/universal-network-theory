"""Prospective 528-state blank-register subdivision test; stdout only."""
import os
import sys
sys.dont_write_bytecode = True
for key in ('OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'OMP_NUM_THREADS',
            'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
import hashlib
import json
import math
from pathlib import Path
import resource
import time
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.resolve()
BS_SHA = '00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec'
CONFIG = dict(N=[2, 3], Omega=1., Ud=1., dstar=1., Delta=4., hbar=1.,
              anchor=[0, 0], gamma=.2, g=.5, V=4., vcell=1., Kg=2., Kv=1., C=.2,
              supply_gap=11.6, strengths=[0., 1., 8.], times=[0., .25, 1., 2.],
              inputs=['cycle15', 'tree7', 'real_plus_15_7', 'empty0'],
              operator_tolerance=2e-11, state_tolerance=2e-9,
              taylor_substep_norm=.5, taylor_tail=1e-18, taylor_max_terms=200,
              row_major_bit_order='edge(i,j) has bit i*N+j; bit1 occupied')


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inputs():
    bs = HERE.parent/'recovered_sources/BS_MICRO_ACTION.md'
    if sha(bs) != BS_SHA:
        raise RuntimeError('Native BS action identity differs')
    names = ['CONNECTED_SUBDIVISION_PROTOCOL_V001.md',
             'CONNECTED_SUBDIVISION_GROWTH_CANDIDATE_V001.md',
             'CONNECTED_SUBDIVISION_CANDIDATE_REVIEW_V001.md',
             'CONNECTED_SUBDIVISION_GROWTH_REVIEW_V001.md',
             'NATIVE_AUTONOMOUS_CONTROLLER_CANDIDATE_V001.md',
             'NATIVE_VOLUME_INCREMENT_PATHWAY.md',
             'NATIVE_RECORD_CONNECTIVITY_PATHWAY_V001.md',
             'NATIVE_RECORD_CONNECTIVITY_REVIEW_V001.md']
    files = {}
    for path in [Path(__file__), bs] + [HERE/name for name in names]:
        path = path.resolve()
        if not path.is_relative_to(ROOT):
            raise RuntimeError('Input outside project root')
        files[str(path.relative_to(ROOT))] = sha(path)
    return dict(config=CONFIG, files=files)


def incidence(n):
    """BS06, without executing the source document or any inherited code."""
    states = np.arange(1 << (n*n))
    bits = (states[:, None] >> np.arange(n*n)) & 1
    grid = bits.reshape(-1, n, n)
    degrees = np.concatenate((grid.sum(axis=2), grid.sum(axis=1)), axis=1)
    mass = bits.sum(axis=1).astype(float)
    diagonal = CONFIG['Delta']*mass + CONFIG['Ud']*((degrees-CONFIG['dstar'])**2).sum(axis=1)
    xsum = np.zeros((len(states), len(states)))
    neighbors = states[:, None] ^ (1 << np.arange(n*n))
    xsum[states[:, None], neighbors] = 1.
    h = np.diag(diagonal) - (CONFIG['Omega']/n)*xsum
    # Independent polynomial expansion of each degree square, including pairs.
    pairs = np.zeros(len(states))
    for incident in ([i*n+j for j in range(n)] for i in range(n)):
        for a in range(n):
            for b in range(a+1, n):
                pairs += bits[:, incident[a]]*bits[:, incident[b]]
    for incident in ([i*n+j for i in range(n)] for j in range(n)):
        for a in range(n):
            for b in range(a+1, n):
                pairs += bits[:, incident[a]]*bits[:, incident[b]]
    expanded = (2*n*CONFIG['Ud']*CONFIG['dstar']**2
                + (CONFIG['Delta']+2*CONFIG['Ud']*(1-2*CONFIG['dstar']))*mass
                + 2*CONFIG['Ud']*pairs)
    return dict(n=n, states=states, bits=bits, mass=mass, diagonal=diagonal,
                neighbors=neighbors, xsum=xsum, h=h, expanded=expanded)


def subdivision(anchor=(0, 0)):
    jmat = np.zeros((512, 16))
    u, v = anchor
    for state in range(16):
        if not (state >> (2*u+v)) & 1:
            continue
        target = 0
        for i in range(2):
            for j in range(2):
                if (i, j) != anchor and (state >> (2*i+j)) & 1:
                    target |= 1 << (3*i+j)
        for i, j in ((u, 2), (2, 2), (2, v)):
            target |= 1 << (3*i+j)
        jmat[target, state] = 1.
    return jmat


def graph_census(n, state):
    parent = list(range(2*n))
    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x
    edges = 0
    for i in range(n):
        for j in range(n):
            if (state >> (n*i+j)) & 1:
                parent[find(i)] = find(n+j)
                edges += 1
    components = len({find(i) for i in range(2*n)})
    return dict(edges=edges, components=components, cycle_rank=edges-2*n+components)


def permute(n, left, right):
    p = np.zeros((1 << (n*n), 1 << (n*n)))
    for state in range(len(p)):
        target = 0
        for i in range(n):
            for j in range(n):
                if (state >> (n*i+j)) & 1:
                    target |= 1 << (n*left[i]+right[j])
        p[target, state] = 1.
    return p


def elastic(n):
    z = CONFIG['V']-2*n*CONFIG['vcell']
    return CONFIG['Kg']*CONFIG['g']**2/2 + CONFIG['C']*CONFIG['g']*z + CONFIG['Kv']*z*z/2


def sparse_action(vectors, eps, old, new, mapped_old, mapped_new, diagonal):
    out = diagonal[:, None]*vectors
    out[:16] -= .5*vectors[:16][old['neighbors']].sum(axis=1)
    out[16:] -= (1/3)*vectors[16:][new['neighbors']].sum(axis=1)
    out[16+mapped_new] += eps*vectors[mapped_old]
    out[mapped_old] += eps*vectors[16+mapped_new]
    return out


def taylor_action(initial, duration, action, norm_inf):
    norm = abs(duration)*norm_inf
    scale = max(0, math.ceil(math.log2(norm/CONFIG['taylor_substep_norm']))) if norm else 0
    steps = 2**scale
    small_norm = norm/steps
    dt = duration/steps
    state = initial.astype(complex).copy()
    max_terms, log_error_amplification = 0, 0.
    if duration == 0:
        return state, dict(substeps=0, max_terms=0, accumulated_operator_truncation_bound=0.)
    for unused in range(steps):
        total, term, magnitude = state.copy(), state.copy(), 1.
        for k in range(1, CONFIG['taylor_max_terms']+1):
            term = (-1j*dt/k)*action(term)
            total += term
            magnitude *= small_norm/k
            tail = math.exp(small_norm)*magnitude*small_norm/(k+1)
            if tail <= CONFIG['taylor_tail']:
                break
        else:
            raise ArithmeticError('Scaled vector Taylor series did not converge')
        state = total
        max_terms = max(max_terms, k)
        log_error_amplification += math.log1p(tail)
    return state, dict(substeps=steps, max_terms=max_terms,
                       accumulated_operator_truncation_bound=math.expm1(log_error_amplification))


def run():
    started = time.perf_counter()
    snapshot = inputs()
    frozen_path = HERE/'CONNECTED_SUBDIVISION_V001_FROZEN.json'
    if json.loads(frozen_path.read_text()) != snapshot:
        raise RuntimeError('Prospective source/configuration freeze differs')
    checks, rows = [], []
    def check(label, error, tolerance=None):
        error = float(error)
        tolerance = CONFIG['operator_tolerance'] if tolerance is None else float(tolerance)
        checks.append(dict(label=label, error=error, tolerance=tolerance,
                           passed=bool(math.isfinite(error) and error <= tolerance)))
    def equal(label, actual, expected, tolerance=None):
        check(label, np.max(np.abs(np.asarray(actual)-np.asarray(expected))), tolerance)
    def variance(h, state):
        hv = h @ state
        return float(np.vdot(hv, hv).real - np.vdot(state, hv).real**2)
    old, new = incidence(2), incidence(3)
    for model in (old, new):
        equal('BS06_expanded_diagonal_N'+str(model['n']), model['diagonal'], model['expanded'])
    jmat = subdivision()
    pdiag = old['bits'][:, 0].astype(float)
    mapped_new, mapped_old = np.nonzero(jmat)
    qdiag = jmat.sum(axis=1)
    p, q = np.diag(pdiag), np.diag(qdiag)
    equal('JdagJ_P', jmat.T @ jmat, p)
    equal('JJdag_Q', jmat @ jmat.T, q)
    equal('eligible_image_census', [pdiag.sum(), qdiag.sum(), len(mapped_old)], [8, 8, 8])
    xa_old = np.eye(16)[old['states'] ^ 1]
    xa_new = np.eye(512)[new['states'] ^ 1]
    srest = old['xsum']-xa_old
    db = 10*np.eye(16)+srest/6
    equal('compression', jmat.T @ new['h'] @ jmat - p @ old['h'] @ p, p @ db @ p)
    source_leak = (1-pdiag)[:, None]*old['h']*pdiag[None, :]
    equal('source_leak', source_leak, -.5*xa_old @ p)
    equal('source_leak_gram', source_leak.T @ source_leak, .25*p)
    leak = (1-qdiag)[:, None]*(new['h'] @ jmat)
    new_edge_indices = [2, 5, 6, 7, 8]
    leakage_sum = xa_new @ jmat
    for edge in new_edge_indices:
        leakage_sum += jmat[new['states'] ^ (1 << edge)]
    equal('target_leak_explicit', leak, -leakage_sum/3)
    equal('target_leak_orthogonal', jmat.T @ leak, np.zeros((16, 16)))
    equal('target_leak_gram', leak.T @ leak, (2/3)*p)
    equal('full_intertwiner', new['h'] @ jmat-jmat @ old['h'],
          jmat @ db+leak+.5*jmat @ xa_old @ (np.eye(16)-p))
    equal('source_jump', new['mass'][:, None]*jmat-jmat*old['mass'][None, :], 2*jmat)
    census = []
    for before, after in zip(mapped_old.tolist(), mapped_new.tolist()):
        cb, ca = graph_census(2, before), graph_census(3, after)
        equal('component_count_'+str(before), ca['components'], cb['components'])
        equal('cycle_rank_'+str(before), ca['cycle_rank'], cb['cycle_rank'])
        equal('edge_increment_'+str(before), ca['edges']-cb['edges'], 2)
        equal('reverse_basis_'+str(before), jmat.T[:, after], np.eye(16)[:, before])
        census.append(dict(source=before, target=after, source_graph=cb, target_graph=ca))
    for left in ([0, 1], [1, 0]):
        for right in ([0, 1], [1, 0]):
            u2 = permute(2, left, right)
            u3 = permute(3, left+[2], right+[2])
            equal('anchor_covariance_'+str(left)+str(right), u3 @ jmat @ u2.T,
                  subdivision((left[0], right[0])))
    equal('cycle_energies', [old['diagonal'][15], new['diagonal'][np.argmax(jmat[:, 15])]], [20, 30])
    equal('elastic_jump', elastic(3)-elastic(2), 1.8)
    equal('pressure_work', 2*(-.1)+.5*1*2**2, 1.8)
    equal('supply_calibration', 10-.2+elastic(3)-elastic(2), CONFIG['supply_gap'])
    native = np.zeros((528, 528))
    native[:16, :16], native[16:, 16:] = old['h'], new['h']
    bdiag = np.concatenate((old['mass'], new['mass']))
    source_diag = -.1*bdiag
    elastic_diag = np.concatenate((np.full(16, elastic(2)), np.full(512, elastic(3))))
    supply_diag = np.concatenate((np.full(16, CONFIG['supply_gap']), np.zeros(512)))
    diagonal = np.concatenate((old['diagonal'], new['diagonal']))+source_diag+elastic_diag+supply_diag
    size_diag = np.concatenate((np.full(16, 2.), np.full(512, 3.)))
    supply_number = np.concatenate((np.ones(16), np.zeros(512)))
    equal('charge_exact', size_diag+supply_number, np.full(528, 3.))
    tmat = np.zeros((528, 528)); tmat[16:, :16] = jmat
    connection = np.array([graph_census(2, s)['components'] == 1 for s in range(16)]
                          + [graph_census(3, s)['components'] == 1 for s in range(512)])
    equal('port_connectivity_commutator', (connection[:, None]-connection[None, :].astype(int))*tmat, 0.)
    initial = np.zeros((528, 4), dtype=complex)
    initial[15, 0] = initial[7, 1] = initial[0, 3] = 1.
    initial[[15, 7], 2] = 1/math.sqrt(2)
    backbones = {}
    for mask in (15, 7):
        target_mask = int(np.argmax(jmat[:, mask]))
        back = np.concatenate(((old['states'] & mask) == mask,
                               (new['states'] & target_mask) == target_mask)).astype(float)
        equal('port_backbone_commutator_'+str(mask), (back[:, None]-back[None, :])*tmat, 0.)
        # Independent off-block Gram test of the backbone norm used by Eq14.
        for mod, req in ((old, mask), (new, target_mask)):
            inside = (mod['states'] & req) == req
            a = mod['h'][np.ix_(~inside, inside)]
            edge_count = int(req.bit_count())
            equal('backbone_gram_'+str(mask)+'_'+str(mod['n']), a.T @ a,
                  (edge_count/mod['n']**2)*np.eye(int(inside.sum())))
        backbones[mask] = back
    initial_ledger = []
    for i, name in enumerate(CONFIG['inputs']):
        state = initial[:, i]
        if i < 3:
            short = state[:16]
            equal('variance_target_'+name, variance(new['h'], jmat @ short),
                  variance(p @ old['h'] @ p+db, short)+2/3)
            equal('variance_source_'+name, variance(old['h'], short),
                  variance(p @ old['h'] @ p, short)+.25)
        initial_ledger.append(dict(native=float(np.vdot(state, native @ state).real),
            source=float(np.sum(abs(state)**2*source_diag)),
            elastic=float(np.sum(abs(state)**2*elastic_diag)),
            supply=float(np.sum(abs(state)**2*supply_diag)), interaction=0.))
    propagation_stats = []
    for eps in CONFIG['strengths']:
        interaction = eps*(tmat+tmat.T)
        h = native+np.diag(source_diag+elastic_diag+supply_diag)+interaction
        equal('Hermitian_'+str(eps), h, h.T)
        equal('matched_detuning_'+str(eps), jmat.T @ h[16:, 16:] @ jmat-p @ h[:16, :16] @ p,
              p @ (srest/6) @ p)
        bdiff = bdiag[:, None]-bdiag[None, :]
        response = -(bdiff**2)*h
        expected_response = np.zeros_like(h)
        expected_response[:16, :16] = .5*old['xsum']
        expected_response[16:, 16:] = new['xsum']/3
        expected_response -= 4*interaction
        equal('complete_incidence_response_'+str(eps), response, expected_response)
        size_current = 1j*h*(size_diag[None, :]-size_diag[:, None])
        equal('creation_current_operator_'+str(eps), size_current, 1j*eps*(tmat.T-tmat))
        equal('creation_source_current_'+str(eps), -1j*bdiff*interaction, 2*size_current)
        action = lambda vectors: sparse_action(vectors, eps, old, new, mapped_old, mapped_new, diagonal)
        probe = (np.arange(528)[:, None]+1)*(1+1j*np.array([1., -.5])[None, :])/528
        equal('independent_sparse_action_'+str(eps), action(probe), h @ probe)
        h_initial = action(initial)
        h2_initial = action(h_initial)
        for i, name in enumerate(CONFIG['inputs']):
            equal('initial_transfer_quadratic_'+str(eps)+'_'+name,
                  np.linalg.norm(h_initial[16:, i])**2,
                  eps**2*float(np.sum(abs(initial[:16, i])**2*pdiag)))
            if i < 3:
                equal('initial_transfer_cubic_'+str(eps)+'_'+name,
                      2*np.vdot(-1j*h_initial[16:, i], -.5*h2_initial[16:, i]).real, 0.)
        eigenvalues, eigenvectors = np.linalg.eigh(h)
        equal('eigenpair_residual_'+str(eps), h @ eigenvectors,
              eigenvectors*eigenvalues[None, :], CONFIG['state_tolerance'])
        spectral_initial = eigenvectors.T @ initial
        times = sorted(set(CONFIG['times']+([math.pi/(2*eps)] if eps > 0 else [])))
        norm_inf = float(np.max(np.sum(np.abs(h), axis=1)))
        for duration in times:
            evolved = eigenvectors @ (np.exp(-1j*duration*eigenvalues)[:, None]*spectral_initial)
            alternate, stats = taylor_action(initial, duration, action, norm_inf)
            propagation_stats.append(dict(epsilon=eps, time=duration, **stats))
            for i, name in enumerate(CONFIG['inputs']):
                state = evolved[:, i]; prob = abs(state)**2
                label = str(eps)+'_'+str(duration)+'_'+name
                error = float(np.linalg.norm(state-alternate[:, i]))
                check('eigen_Taylor_'+label, error, CONFIG['state_tolerance'])
                equal('norm_'+label, prob.sum(), 1., CONFIG['state_tolerance'])
                ledger = dict(native=float(np.vdot(state, native @ state).real),
                    source=float(prob @ source_diag), elastic=float(prob @ elastic_diag),
                    supply=float(prob @ supply_diag),
                    interaction=float(np.vdot(state, interaction @ state).real))
                total, baseline = sum(ledger.values()), sum(initial_ledger[i].values())
                equal('total_energy_'+label, total, baseline, CONFIG['state_tolerance'])
                equal('ledger_sum_'+label, total, np.vdot(state, h @ state).real, CONFIG['state_tolerance'])
                equal('charge_'+label, prob @ (size_diag+supply_number), 3., CONFIG['state_tolerance'])
                current = float(np.vdot(state, size_current @ state).real)
                equal('creation_current_state_'+label, current,
                      2*eps*np.vdot(state, tmat @ state).imag, CONFIG['state_tolerance'])
                target = float(prob[16:].sum()); in_q = float(prob[16:] @ qdiag)
                connected = float(prob @ connection)
                back_probability, back_bound, swap_bound = None, None, None
                if i < 3:
                    mask = 15 if i == 0 else 7
                    m0 = mask.bit_count()
                    back_probability = float(prob @ backbones[mask])
                    back_bound = min(1., duration**2*max(m0/4, (m0+2)/9))
                    check('Eq14_backbone_'+label, max(0., 1-back_probability-back_bound), CONFIG['state_tolerance'])
                    check('backbone_implies_connected_'+label, max(0., back_probability-connected), CONFIG['state_tolerance'])
                    if eps > 0 and duration == math.pi/(2*eps):
                        swap_bound = max(0., 1-(math.pi*(.5+math.sqrt(2/3))/(2*eps))**2)
                        check('Eq15_swap_'+label, max(0., swap_bound-in_q), CONFIG['state_tolerance'])
                if eps == 0:
                    equal('ports_off_no_growth_'+label, target, 0., CONFIG['state_tolerance'])
                check('Q_subset_target_'+label, max(0., in_q-target), CONFIG['state_tolerance'])
                rows.append(dict(epsilon=eps, time=duration, input=name,
                    source_sector_probability=float(prob[:16].sum()), target_sector_probability=target,
                    source_eligible_probability=float(prob[:16] @ pdiag),
                    target_exact_Q_reverse_eligible_probability=in_q,
                    target_outside_Q_probability=target-in_q,
                    connected_probability=connected,
                    source_connected_probability=float(prob[:16] @ connection[:16]),
                    target_connected_probability=float(prob[16:] @ connection[16:]),
                    backbone_probability=back_probability, Eq14_max_leakage=back_bound,
                    Eq15_min_Q_at_swap=swap_bound, creation_count_current=current,
                    incidence_response_moment=float(np.vdot(state, response @ state).real),
                    energy=ledger, energy_changes={key: ledger[key]-initial_ledger[i][key] for key in ledger},
                    total_energy=total, total_energy_error=total-baseline,
                    eigen_Taylor_vector_error=error))
    equal('complete_row_census', len(rows), 56)
    failures = [item for item in checks if not item['passed']]
    payload = dict(config=CONFIG, interpretation='Added clamped connected-inclusion port; not native spontaneous growth or physical expansion',
                   basis_graph_census=census, initial_energy_ledger=initial_ledger,
                   propagation=propagation_stats, rows=rows, checks=checks, failures=failures)
    result = dict(status='COMPLETE' if not failures else 'FAILED_NUMERICAL_CONTROLS',
                  payload=payload, payload_sha256=hashlib.sha256(encoded(payload)).hexdigest(),
                  freeze_sha256=sha(frozen_path), seconds=time.perf_counter()-started,
                  peak_self_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    print(json.dumps(result, allow_nan=False))
    return int(bool(failures))


if __name__ == '__main__':
    if sys.argv[1:] == ['freeze']:
        print(json.dumps(inputs(), indent=2, allow_nan=False))
    elif sys.argv[1:]:
        raise SystemExit('Use freeze or no arguments')
    else:
        raise SystemExit(run())

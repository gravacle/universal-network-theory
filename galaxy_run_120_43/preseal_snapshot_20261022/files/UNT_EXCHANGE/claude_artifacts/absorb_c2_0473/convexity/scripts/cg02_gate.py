"""CG02: estimator-convexity gate on the galaxy response coefficients (read-only, numpy only).

Exact constraint (CONVEXITY_GATE_V001.md section 1): for the pinned target, H(n, j) is a real
symmetric (after the diagonal zero-holonomy gauge) matrix affine in the lapse perturbation n and
the read sources j, so ln Z = ln Tr exp(-beta H) is jointly convex. Hence for every momentum
block d2logZ_deta2 = Cov(S) + <T> is PSD, F_total_hessian = -d2logZ/beta is NSD, and every
per-cell source Hessian grid node h(k) (cardinal extraction) is Hermitian NSD.

Estimator algebra transcribed from pairallk_v004 _measure_allk (L3643-3685), _sums (L3688-3696),
_sums_combine (L3699-3704), _estimate (L3707-3715); block projection and Mandel factor from
sampler_eval/load_capture.py (verified there to reproduce result F_total_hessian); grid extraction
from owned_positive_cardinal_source_hessian_v001 extract_real_pair / extract_self_conjugate
(L39-73). No PSD/sign repair, clipping, ridge or pseudoinverse of any estimate.
"""
import glob, hashlib, json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'results')
UPC = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13'
SE = UPC + '/CLAUDE2/CRITICAL_PATH_EVALUATION_2026-10-17_V001/sampler_eval'
CX = UPC + '/CODEX1'
RUNS = {'admission': CX + '/OWNED_L4_ADMISSION_RESIDENCE_RUN_V001',
        'cycle': CX + '/OWNED_L4_CURRENT_GRAPH_CYCLE_RUN_V001',
        'worm': CX + '/OWNED_L4_WORM_LOOP_RUN_V001'}
A2_NPZ = SE + '/CANDIDATE_4CHAIN_POOLED_GRID_V001.npz'
V004_NPZ = CX + '/PROVISIONAL_L4_COEFFICIENT_FREEZE_V001/coefficients.npz'
FAM = ['flip', 'hop', 'bind', 'admit', 'birth']  # amplitude_names h,t,g,kappa,epsilon (raw_metadata)
L, CELLS, BETA = 4, 64, 1.0
TOL = 1e-10  # roundoff classification only: |lambda| <= TOL*max(1,||M||) is "zero", not a repair


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


META = json.load(open(SE + '/cycle_meta.json'))
MAND = np.ones(10); MAND[7:10] = np.sqrt(2.0)
BLK = []
for b in META['blocks']:
    pv = np.asarray(b['profile_values'], float)
    d = 10 * pv.shape[0]
    nn = [0] if d == 10 else [0, 10]
    BLK.append({'k': tuple(b['k']), 'pv': pv, 'd': d, 'nn': nn, 'off': b['contact_offset'],
                'ent': [tuple(e) for e in b['contact_entries']]})


def load_capture(d):
    files = sorted(glob.glob(os.path.join(d, 'committed_capture', 'block_*.npz')))
    parts = {k: [] for k in ('chain_id', 'measurement_id', 'score_cells', 'allk_contacts', 'events', 'counts')}
    for f in files:
        z = np.load(f)
        for k in ('chain_id', 'measurement_id', 'score_cells', 'allk_contacts', 'events'):
            parts[k].append(np.array(z[k]))
        parts['counts'].append(np.array(z['features'][:, -5:]))
    a = {k: np.concatenate(v) for k, v in parts.items()}
    out = {}
    for c in (0, 1):
        s = a['chain_id'] == c
        o = np.argsort(a['measurement_id'][s])
        out[c] = {k: v[s][o] for k, v in a.items()}
        assert np.array_equal(out[c]['measurement_id'], np.arange(len(o)))
    return out, len(files)


def load_v004():
    z = np.load(os.path.join(OUT, 'v004_series.npz'))
    out = {}
    for c in (0, 1):
        out[c] = {'measurement_id': z['c%d_measurement_ids' % c], 'score_cells': z['c%d_score_cells' % c],
                  'allk_contacts': z['c%d_contacts' % c], 'events': z['c%d_events' % c], 'counts': None}
        assert np.array_equal(out[c]['measurement_id'], np.arange(len(out[c]['measurement_id'])))
    return out


def batch_sums(chain, partition, cid):
    """Per (chain, batch) sufficient sums for every block: n, sum S, sum S S^T, sum T (NN entries)."""
    sc = chain['score_cells'].reshape(-1, CELLS, 10)
    res = []
    for p in partition:
        if p['chain'] != cid:
            continue
        lo, hi = p['measurement_id_range_half_open']
        blocks = []
        for b in BLK:
            X = (np.einsum('pc,mcf->mpf', b['pv'], sc[lo:hi], optimize=False) * MAND).reshape(hi - lo, -1)
            T = np.zeros((b['d'], b['d']))
            for col, (pa, pb) in enumerate(b['ent']):
                v = float(chain['allk_contacts'][lo:hi, b['off'] + col].sum())
                T[b['nn'][pa], b['nn'][pb]] = v; T[b['nn'][pb], b['nn'][pa]] = v
            blocks.append({'n': hi - lo, 'S': X.sum(0), 'SS': np.einsum('ia,ib->ab', X, X, optimize=False), 'T': T})
        res.append({'chain': cid, 'batch': p['batch'], 'blocks': blocks})
    return res


def estimate(batches):
    """v004 _estimate on combined sums: cov = SS/n - g g^T (plug-in), H = cov + T/n."""
    out = []
    for bi in range(len(BLK)):
        n = sum(b['blocks'][bi]['n'] for b in batches)
        S = sum(b['blocks'][bi]['S'] for b in batches)
        SS = sum(b['blocks'][bi]['SS'] for b in batches)
        T = sum(b['blocks'][bi]['T'] for b in batches)
        g = S / n
        cov = SS / n - np.outer(g, g)
        out.append({'cov': cov, 'T': T / n, 'H': cov + T / n})
    return out


def grid_from_F(Fs):
    g = np.empty((L, L, L, 10, 10), dtype=complex); seen = set()
    for b, F in zip(BLK, Fs):
        k = b['k']; partner = tuple((-v) % L for v in k); sc = k == partner
        if sc:
            h = (F / CELLS).astype(complex)
        else:
            S = CELLS / 2
            cc, cs, scb, ss = F[:10, :10] / S, F[:10, 10:] / S, F[10:, :10] / S, F[10:, 10:] / S
            h = (cc + ss) / 2 + 1j * (cs - scb) / 2
        g[k] = h; seen.add(k)
        if not sc:
            g[partner] = h.conj(); seen.add(partner)
    assert len(seen) == CELLS
    return g


def block_gate(est):
    """Per block: eigenvalues of d2logZ (must be >= 0), N-weight of the lowest eigenvector,
    lapse diagonal (Var S_N + <T_NN>, must be >= 0), and the automatic signs of the parts."""
    rows = []
    for b, e in zip(BLK, est):
        H = (e['H'] + e['H'].T) / 2  # estimator is exactly symmetric; symmetrization is a no-op check
        asym = float(np.max(np.abs(e['H'] - e['H'].T)))
        w, V = np.linalg.eigh(H)
        scale = max(1.0, float(np.max(np.abs(w))))
        nw = float(np.sum(V[b['nn'], 0] ** 2))
        jj = [i for i in range(b['d']) if i not in b['nn']]
        wc = np.linalg.eigvalsh(e['cov']); wt = np.linalg.eigvalsh(e['T'])
        wjj = np.linalg.eigvalsh(H[np.ix_(jj, jj)])
        lapse_diag = [float(H[i, i]) for i in b['nn']]
        rows.append({'k': list(b['k']), 'd': b['d'], 'lambda_min_d2logZ': float(w[0]), 'lambda_max_d2logZ': float(w[-1]),
                     'n_negative_raw': int(np.sum(w < 0)), 'n_negative_beyond_roundoff': int(np.sum(w < -TOL * scale)),
                     'violation': bool(w[0] < -TOL * scale),
                     'lowest_eigvec_lapse_weight': nw, 'lapse_diag_d2logZ': lapse_diag,
                     'lapse_diag_violation': bool(min(lapse_diag) < -TOL * scale),
                     'lambda_min_cov': float(wc[0]), 'lambda_max_contact_mean': float(wt[-1]),
                     'lambda_min_jj_subblock': float(wjj[0]), 'asymmetry': asym})
    return rows


def grid_gate(g):
    """Per node: lambda_max of the Hermitian part of h(k) (must be <= 0); consumer-side Legendre
    signs where F_jj is invertible: lambda_max(F_jj) (< 0 required for Gamma_QQ = F_jj^-1 <= 0)
    and Gamma_nn = -(a - b F_jj^-1 c) (>= 0 implied by F <= 0)."""
    nodes = []
    for idx in np.ndindex(L, L, L):
        h = g[idx]; herm = (h + h.conj().T) / 2
        w = np.linalg.eigvalsh(herm)
        scale = max(1.0, float(np.max(np.abs(w))))
        D = herm[1:, 1:]; wD = np.linalg.eigvalsh(D)
        sv = np.linalg.svd(D, compute_uv=False)
        gnn = None
        if sv[-1] > 1e-12 * sv[0]:
            gnn = float(np.real(-(herm[0, 0] - herm[0, 1:] @ np.linalg.solve(D, herm[1:, 0]))))
        nodes.append({'k': list(idx), 'lambda_max_h': float(w[-1]), 'lambda_min_h': float(w[0]),
                      'violation': bool(w[-1] > TOL * scale), 'n_positive_beyond_roundoff': int(np.sum(w > TOL * scale)),
                      'lambda_max_Fjj': float(wD[-1]), 'Fjj_rel_smallest_sv': float(sv[-1] / sv[0]),
                      'Gamma_nn': gnn, 'hermiticity_residual': float(np.linalg.norm(h - h.conj().T))})
    return nodes


def summarize_blocks(rows):
    v = [r for r in rows if r['violation']]
    return {'n_blocks': len(rows), 'n_blocks_violating': len(v),
            'min_lambda_min_d2logZ': min(r['lambda_min_d2logZ'] for r in rows),
            'max_lambda_max_d2logZ': max(r['lambda_max_d2logZ'] for r in rows),
            'max_lambda_max_F': -min(r['lambda_min_d2logZ'] for r in rows) / BETA,
            'n_negative_eigenvalues_beyond_roundoff': sum(r['n_negative_beyond_roundoff'] for r in rows),
            'violating_k': [r['k'] for r in v],
            'n_lapse_diag_violations': sum(1 for r in rows if r['lapse_diag_violation']),
            'min_lambda_min_cov_auto_psd': min(r['lambda_min_cov'] for r in rows),
            'max_lambda_max_contact_auto_nsd': max(r['lambda_max_contact_mean'] for r in rows),
            'min_lambda_min_jj_subblock_auto_psd': min(r['lambda_min_jj_subblock'] for r in rows),
            'lowest_eigvec_lapse_weight_of_violators': [round(r['lowest_eigvec_lapse_weight'], 4) for r in v]}


def summarize_grid(nodes):
    v = [n for n in nodes if n['violation']]
    inv = [n for n in nodes if n['Gamma_nn'] is not None]
    return {'n_nodes': len(nodes), 'n_nodes_violating': len(v), 'max_lambda_max_h': max(n['lambda_max_h'] for n in nodes),
            'min_lambda_min_h': min(n['lambda_min_h'] for n in nodes),
            'violating_k': [n['k'] for n in v],
            'n_positive_eigenvalues_beyond_roundoff': sum(n['n_positive_beyond_roundoff'] for n in nodes),
            'max_lambda_max_Fjj': max(n['lambda_max_Fjj'] for n in nodes),
            'n_nodes_Fjj_invertible': len(inv),
            'min_Gamma_nn_where_invertible': min(n['Gamma_nn'] for n in inv) if inv else None,
            'n_Gamma_nn_negative': sum(1 for n in inv if n['Gamma_nn'] < 0),
            'max_hermiticity_residual': max(n['hermiticity_residual'] for n in nodes)}


def full_eval(name, batches, with_per_batch=True, keep_detail=False):
    """Pooled, per chain, leave-one-batch-out jackknife, and (optional) each batch alone."""
    res = {}
    pooled = estimate(batches)
    rows = block_gate(pooled)
    g = grid_from_F([-e['H'] / BETA for e in pooled])
    nodes = grid_gate(g)
    res['pooled'] = {'blocks': summarize_blocks(rows), 'grid': summarize_grid(nodes)}
    if keep_detail:
        res['pooled']['block_rows'] = rows
        res['pooled']['grid_nodes'] = nodes
    chains = sorted(set((b.get('run', ''), b['chain']) for b in batches))
    res['per_chain'] = {}
    for (rn, c) in chains:
        sub = [b for b in batches if b.get('run', '') == rn and b['chain'] == c]
        e = estimate(sub)
        res['per_chain'][(rn + '_' if rn else '') + 'c%d' % c] = {
            'blocks': summarize_blocks(block_gate(e)),
            'grid': summarize_grid(grid_gate(grid_from_F([-x['H'] / BETA for x in e])))}
    # jackknife
    jk_blocks, jk_grid, lam = [], [], []
    for i in range(len(batches)):
        sub = batches[:i] + batches[i + 1:]
        e = estimate(sub)
        rb = block_gate(e)
        jk_blocks.append(summarize_blocks(rb)); lam.append([r['lambda_min_d2logZ'] for r in rb])
        jk_grid.append(summarize_grid(grid_gate(grid_from_F([-x['H'] / BETA for x in e]))))
    lam = np.asarray(lam); J = lam.shape[0]
    se = np.sqrt((J - 1) / J * np.sum((lam - lam.mean(0)) ** 2, axis=0))
    pl = np.array([r['lambda_min_d2logZ'] for r in rows])
    res['jackknife'] = {'J': J,
                        'n_replicates_with_block_violation': sum(1 for s in jk_blocks if s['n_blocks_violating'] > 0),
                        'n_replicates_with_grid_violation': sum(1 for s in jk_grid if s['n_nodes_violating'] > 0),
                        'block_violations_per_replicate': [s['n_blocks_violating'] for s in jk_blocks],
                        'grid_violations_per_replicate': [s['n_nodes_violating'] for s in jk_grid],
                        'min_lambda_min_d2logZ_over_replicates': float(lam.min()),
                        'max_lambda_max_h_over_replicates': max(s['max_lambda_max_h'] for s in jk_grid),
                        'per_block_lambda_min_pooled': pl.tolist(),
                        'per_block_lambda_min_jackknife_se': se.tolist(),
                        'per_block_z_lambda_min': (pl / np.where(se > 0, se, np.nan)).tolist(),
                        'min_z_lambda_min': float(np.nanmin(pl / np.where(se > 0, se, np.nan))),
                        'jackknife_bias_lambda_min': ((J - 1) * (lam.mean(0) - pl)).tolist()}
    if with_per_batch:
        pb = []
        for b in batches:
            e = estimate([b])
            sb = summarize_blocks(block_gate(e)); sg = summarize_grid(grid_gate(grid_from_F([-x['H'] / BETA for x in e])))
            pb.append({'run': b.get('run', name), 'chain': b['chain'], 'batch': b['batch'], 'rows': b['blocks'][0]['n'],
                       'n_blocks_violating': sb['n_blocks_violating'], 'min_lambda_min_d2logZ': sb['min_lambda_min_d2logZ'],
                       'n_nodes_violating': sg['n_nodes_violating'], 'max_lambda_max_h': sg['max_lambda_max_h']})
        res['per_batch'] = {'n_batches': len(pb), 'n_batches_with_block_violation': sum(1 for x in pb if x['n_blocks_violating']),
                            'n_batches_with_grid_violation': sum(1 for x in pb if x['n_nodes_violating']), 'rows': pb}
    return res, pooled, g


def event_counts(chains, total_only=False):
    out = {}
    for c, ch in chains.items():
        ev = ch['events']
        d = {'paths': int(len(ev)), 'events_total': int(ev.sum()), 'events_per_path_mean': float(ev.mean()),
             'events_per_path_max': int(ev.max()), 'zero_event_paths': int(np.sum(ev == 0))}
        if ch['counts'] is not None:
            cnt = ch['counts']
            d['by_family_total'] = dict(zip(FAM, [int(round(x)) for x in cnt.sum(0)]))
            d['by_family_paths_with_any'] = dict(zip(FAM, [int(x) for x in (cnt > 0).sum(0)]))
            d['family_sum_equals_events'] = bool(np.array_equal(cnt.sum(1).round().astype(int), ev.astype(int)))
        else:
            d['by_family_total'] = 'NOT_SAVED (V004 series has total events only)'
        out['c%d' % c] = d
    if all(chains[c]['counts'] is not None for c in chains):
        out['both_chains_by_family_total'] = {f: sum(out['c%d' % c]['by_family_total'][f] for c in chains) for f in FAM}
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    report = {'inputs': {}, 'reproduction': {}, 'captures': {}, 'combined': {}, 'grids_saved': {}}
    report['inputs']['A2_npz'] = {'path': A2_NPZ, 'sha256': sha(A2_NPZ)}
    report['inputs']['V004_npz'] = {'path': V004_NPZ, 'sha256': sha(V004_NPZ)}
    report['inputs']['cycle_meta'] = {'path': SE + '/cycle_meta.json', 'sha256': sha(SE + '/cycle_meta.json')}
    data, batches_by_run, pooled_by_run, grid_by_run = {}, {}, {}, {}
    # V004 from its saved series
    ref = json.load(open(os.path.join(OUT, 'v004_blocks.json')))
    data['v004'] = load_v004()
    parts = {'v004': ref['partition']}
    for run, d in RUNS.items():
        data[run], nfiles = load_capture(d)
        report['inputs'][run] = {'dir': d, 'n_block_files': nfiles,
                                 'receipt_sha256': sha(d + '/receipt.json'), 'result_sha256': sha(d + '/result.json')}
        parts[run] = json.load(open(os.path.join(OUT, run + '_blocks.json')))['partition']
    for run in ('v004', 'admission', 'cycle', 'worm'):
        bl = []
        for c in (0, 1):
            for b in batch_sums(data[run][c], parts[run], c):
                b['run'] = run; bl.append(b)
        batches_by_run[run] = bl
        # reproduction against result.json point and per-chain estimates
        refb = json.load(open(os.path.join(OUT, run + '_blocks.json')))['blocks']
        e = estimate(bl)
        dp = max(float(np.max(np.abs(-x['H'] / BETA - np.asarray(r['F_total_hessian'])))) for x, r in zip(e, refb))
        dc = 0.0
        for c in (0, 1):
            ec = estimate([b for b in bl if b['chain'] == c])
            dc = max(dc, max(float(np.max(np.abs(x['H'] - np.asarray(r['per_chain_d2logZ'][c])))) for x, r in zip(ec, refb)))
        report['reproduction'][run] = {'max_abs_dev_F_total_hessian_pooled': dp, 'max_abs_dev_d2logZ_per_chain': dc}
        res, pooled, g = full_eval(run, bl, keep_detail=True)
        res['event_counts'] = event_counts(data[run])
        report['captures'][run] = res
        pooled_by_run[run] = pooled; grid_by_run[run] = g
    # V004 frozen grid reproduction
    zv = np.load(V004_NPZ)
    report['reproduction']['v004_grid_vs_frozen_npz_max_abs'] = float(np.max(np.abs(grid_by_run['v004'] - zv['source_hessian_grid'])))
    report['grids_saved']['V004_frozen_npz'] = summarize_grid(grid_gate(zv['source_hessian_grid']))
    # A2 pooled = admission + cycle (4 chains)
    combos = {'A2_pooled4_admission_cycle': ['admission', 'cycle'],
              'pooled4_cycle_worm': ['cycle', 'worm'],
              'pooled4_admission_worm': ['admission', 'worm'],
              'pooled6_admission_cycle_worm': ['admission', 'cycle', 'worm']}
    za = np.load(A2_NPZ)
    for name, rr in combos.items():
        bl = [b for r in rr for b in batches_by_run[r]]
        res, pooled, g = full_eval(name, bl, with_per_batch=False, keep_detail=(name == 'A2_pooled4_admission_cycle'))
        report['combined'][name] = res
        if name == 'A2_pooled4_admission_cycle':
            report['reproduction']['A2_grid_vs_saved_npz_max_abs'] = float(np.max(np.abs(g - za['source_hessian_grid'])))
            report['reproduction']['A2_grid_saved_max_abs_entry'] = float(np.max(np.abs(za['source_hessian_grid'])))
    report['grids_saved']['A2_npz_source_hessian_grid'] = summarize_grid(grid_gate(za['source_hessian_grid']))
    for k in za.files:
        if k.startswith('single_chain_grid_'):
            report['grids_saved']['A2_npz_' + k] = summarize_grid(grid_gate(za[k]))
    # background central covariance C (consumer requires SPD Cbar; observed only)
    report['background_C_eigenvalues'] = {
        'A2_npz': np.linalg.eigvalsh(za['background_C']).tolist(),
        'V004_npz': np.linalg.eigvalsh(zv['background_C']).tolist()}
    report['tolerance_roundoff_classification'] = TOL
    json.dump(report, open(os.path.join(OUT, 'cg02_gate_v001.json'), 'w'), indent=1, default=float)
    # compact console summary
    def line(tag, r):
        p = r['pooled']; j = r['jackknife']
        pc = {k: (v['blocks']['n_blocks_violating'], v['grid']['n_nodes_violating'], round(v['blocks']['min_lambda_min_d2logZ'], 5), round(v['grid']['max_lambda_max_h'], 6)) for k, v in r['per_chain'].items()}
        print(tag, 'pooled blocks viol', p['blocks']['n_blocks_violating'], 'minlam', p['blocks']['min_lambda_min_d2logZ'],
              'grid viol', p['grid']['n_nodes_violating'], 'maxh', p['grid']['max_lambda_max_h'],
              '| jk rep viol blocks/grid', j['n_replicates_with_block_violation'], j['n_replicates_with_grid_violation'], '/', j['J'],
              'min z', round(j['min_z_lambda_min'], 2), '| chains', pc,
              ('| batches viol %d/%d' % (r['per_batch']['n_batches_with_block_violation'], r['per_batch']['n_batches']) if 'per_batch' in r else ''))
    for k, v in report['captures'].items(): line(k, v)
    for k, v in report['combined'].items(): line(k, v)
    print('repro', json.dumps(report['reproduction']))
    print('saved grids', {k: (v['n_nodes_violating'], v['max_lambda_max_h']) for k, v in report['grids_saved'].items()})
    for k in report['captures']:
        print(k, json.dumps(report['captures'][k]['event_counts'].get('both_chains_by_family_total'))), print(json.dumps({c: report['captures'][k]['event_counts'][c].get('events_total') for c in ('c0', 'c1')}))


if __name__ == '__main__':
    main()

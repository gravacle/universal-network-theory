"""G01: registered estimator-convexity gate (CONVEXITY_GATE_V001, cg02_gate.py fcb796a9 -- the code that admitted the
A2 grid 2e3a36d8) applied to the SAVED stage-0 grids of STAGE0_ANALYSIS_V003 (pooled 8-process grid, its 8 per-process
grids and its 8 leave-one-process-out jackknife members). Read-only on every input. numpy only. No launch, no repair.
Never opens any NGC file or runs_ext/KMAX_A2F10_C5H_RUN_V001.

Writes (only under stage0_grid_gate_c2/):
  GATE_V001.json                                     (all numbers)
  candidate/STAGE0_POOLED8_CANDIDATE_GRID_V001.npz   (A2-schema coefficient file, target-free; NOT registered, NOT used)
Background moments for the candidate come from the 8 committed captures' `background` rows (read-only), with the A2
builder's own moments() (sampler_eval/coeff_grids_lib.py), cross-checked against the analysis JSON's C-bar.
"""
import hashlib, importlib.util, json, math, os, sys
from pathlib import Path
import numpy as np

OUTDIR = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/stage0_grid_gate_c2')
UPC = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13')
EXT = Path('/Volumes/External1/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs_ext')
AN = EXT / 'STAGE0_ANALYSIS_V003'
PIN = {
    'analysis_json': (AN / 'STAGE0_ANALYSIS_V003.json', '8e7717b1a987e352fa3f61c6367d4d51372e39dfbec16ae175b97302b8c2e7c8'),
    'analysis_grids_npz': (AN / 'STAGE0_ANALYSIS_V003_grids.npz', '4acad3fec253fb886709e50e1089715a7fd67b1c1407051e5c16468cb24f228a'),
    'A2_npz': (UPC / 'CLAUDE2/CRITICAL_PATH_EVALUATION_2026-10-17_V001/sampler_eval/CANDIDATE_4CHAIN_POOLED_GRID_V001.npz',
               '2e3a36d888ef8a89c9a2b6073ca6123656c31317c995962c11f34d434eca6ff7'),
    'cg02_gate_py': (Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/absorb_c2_0473/convexity/scripts/cg02_gate.py'),
                     'fcb796a9e8364862885884e9cbe16f6e18b71d5306799a30ea04b95ed854308b'),
    'cg02_gate_result_json': (Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/absorb_c2_0473/convexity/results/cg02_gate_v001.json'),
                              '7da1f1f69c2d08826bdcac601086e2697ea755064ebfb0dab64bb1e0f53ceea6'),
    'convexity_gate_json': (Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/absorb_c2_0473/convexity/CONVEXITY_GATE_V001.json'),
                            '66b93373a258c9feec3a46b450c9f8c3e0bad84a936b43a156b13d1dfe75d17d'),
    'stage0_lib_v001': (Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/sampler_stage0_c2/analysis/stage0_lib_v001.py'),
                        '79554c5f1dbc5ef3c8a95b1eb41e0c0b085d60aa973c0f73c3c1487c6f3e34b2'),
    'stage0_analysis_v003_py': (Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/sampler_stage0_c2/prelaunch_fix_v002/analysis/stage0_analysis_v003.py'),
                                '629cd1d9ed067a5f6c212bf4931855be15a9bf20b0a9f77b0b6f107e79a37c61'),
    'prereg': (Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/sampler_stage0_c2/PREREG_STAGE0_V001.md'),
               'aee48b022bccc29196a3dddb632be4a2132d1ff8942fb4217938d6b70355ea1f'),
    'addendum_v001': (Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/sampler_stage0_c2/PREREG_STAGE0_ADDENDUM_V001.md'),
                      '34e5dd29b1a0cd2abc048b869968f35a3f993e729a423ce20abcbadfa2931d69'),
    'addendum_v002': (Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/sampler_stage0_c2/prelaunch_fix_v001/PREREG_STAGE0_ADDENDUM_V002.md'),
                      'b3a4d23f9130dc2c1bf810883eea59eb4000522d192ba830e2b226a3091f7ae1'),
    'addendum_v003': (Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/sampler_stage0_c2/prelaunch_fix_v002/PREREG_STAGE0_ADDENDUM_V003.md'),
                      'f72bc001d7e345d760befb5492cc96e7ff8c0a3b39ba65c09aa3a7e1233d8a3b'),
}
COEFF_LIB = UPC / 'CLAUDE2/CRITICAL_PATH_EVALUATION_2026-10-17_V001/sampler_eval/coeff_grids_lib.py'
CONSUMER = UPC / 'helpers/coefficient_method/ddo_body_source_offset_root_v003.py'   # key list read from source text only
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
L = 4; C = 64


def load_mod(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path)); m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m; spec.loader.exec_module(m); return m


def jsonable(x):
    if isinstance(x, dict): return {str(k): jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [jsonable(v) for v in x]
    if isinstance(x, np.ndarray): return jsonable(x.tolist())
    if isinstance(x, np.generic): return jsonable(x.item())
    if isinstance(x, complex): return [x.real, x.imag]
    if isinstance(x, float) and not math.isfinite(x): return repr(x)
    return x


def main():
    rep = {'inputs': {}, 'notes': []}
    for k, (p, want) in PIN.items():
        got = sha(p)
        if got != want: raise SystemExit('PIN MISMATCH %s %s != %s' % (k, got, want))
        rep['inputs'][k] = {'path': str(p), 'sha256': got}
    rep['inputs']['coeff_grids_lib'] = {'path': str(COEFF_LIB), 'sha256': sha(COEFF_LIB)}
    cg = load_mod('cg02_gate_pinned', PIN['cg02_gate_py'][0])   # top level only defines + reads sampler_eval/cycle_meta.json
    rep['inputs']['cg02_cycle_meta'] = {'path': cg.SE + '/cycle_meta.json', 'sha256': sha(cg.SE + '/cycle_meta.json')}
    S = load_mod('stage0_lib_pinned', PIN['stage0_lib_v001'][0])
    CL = load_mod('coeff_grids_lib_a2', COEFF_LIB)
    TOL = cg.TOL

    gate = lambda g: cg.summarize_grid(cg.grid_gate(g))

    # ---- anchor: cg02 grid gate on the A2 npz must reproduce the A2 admission's saved-grid numbers exactly ----
    za = np.load(PIN['A2_npz'][0], allow_pickle=False)
    A2 = za['source_hessian_grid']
    ref = json.load(open(PIN['cg02_gate_result_json'][0]))['grids_saved']
    anc = {}
    anc['A2_npz_source_hessian_grid'] = gate(A2)
    for k in za.files:
        if k.startswith('single_chain_grid_'): anc['A2_npz_' + k] = gate(za[k])
    anc_eq = {k: (json.loads(json.dumps(v, default=float)) == ref[k]) for k, v in anc.items()}
    rep['anchor_A2_reproduction'] = {'equal_to_cg02_gate_v001_grids_saved': anc_eq, 'all_equal': all(anc_eq.values()),
                                     'A2_pooled': anc['A2_npz_source_hessian_grid']}
    if not all(anc_eq.values()): raise SystemExit('ANCHOR FAILED: ' + json.dumps(anc_eq))

    # ---- the registered stage-0 grid objects (saved by analysis v003 estimator(), PREREG section 3) ----
    zs = np.load(PIN['analysis_grids_npz'][0], allow_pickle=False)
    G, Gu, Glu, se_u, se_b = (zs[k] for k in ('stage0_pooled_grid', 'per_process_grids', 'loo_process_grids',
                                               'process_jackknife_se', 'batch_jackknife_se'))
    J = Gu.shape[0]
    se_re = np.sqrt((J - 1) / J * (np.abs(Glu - Glu.mean(0)) ** 2).sum(0))
    rep['grid_objects'] = {'stage0_pooled_grid': list(G.shape), 'per_process_grids': list(Gu.shape), 'loo_process_grids': list(Glu.shape),
                           'process_jackknife_se_recomputed_from_loo_max_abs_dev': float(np.abs(se_re - se_u).max()),
                           'process_jackknife_se_max': float(se_u.max()),
                           'loo_batch_grids_saved': False,
                           'definition': 'pooled over 8x16384 rows (mean within-process H + between-process covariance of process means), '
                                         'h = F/64 (self-conjugate) or [(cc+ss)/2 + i(cs-sc)/2]/32 (pairs); band = leave-one-process-out '
                                         'jackknife SE = sqrt(7/8 sum |g_-i - gbar|^2) per entry (PREREG section 3; analysis v003 L150-194)'}

    # ---- gate on the saved grids ----
    gp = gate(G); gu = [gate(g) for g in Gu]; gl = [gate(g) for g in Glu]
    viol = lambda s: s['n_nodes_violating'] > 0
    def compact(s):
        return {k: s[k] for k in ('n_nodes_violating', 'violating_k', 'max_lambda_max_h', 'min_lambda_min_h', 'max_lambda_max_Fjj',
                                  'n_nodes_Fjj_invertible', 'min_Gamma_nn_where_invertible', 'n_Gamma_nn_negative', 'max_hermiticity_residual',
                                  'n_positive_eigenvalues_beyond_roundoff')}
    rep['gate_saved_grids'] = {
        'code': 'cg02_gate.grid_gate + summarize_grid (sha fcb796a9), imported unmodified; violation = lambda_max(herm h) > 1e-10*max(1,|lambda|max)',
        'pooled': compact(gp),
        'per_process': [compact(s) for s in gu],
        'loo_process': [compact(s) for s in gl],
        'n_members_evaluated': 1 + 2 * J,
        'n_members_violating': int(viol(gp)) + sum(map(viol, gu)) + sum(map(viol, gl)),
        'total_violating_nodes': gp['n_nodes_violating'] + sum(s['n_nodes_violating'] for s in gu + gl),
        'max_lambda_max_h_over_all_members': max(s['max_lambda_max_h'] for s in [gp] + gu + gl),
        'min_Gamma_nn_over_all_members': min(s['min_Gamma_nn_where_invertible'] for s in [gp] + gu + gl),
        'n_Gamma_nn_negative_over_all_members': sum(s['n_Gamma_nn_negative'] for s in [gp] + gu + gl),
        'min_nodes_Fjj_invertible_over_members': min(s['n_nodes_Fjj_invertible'] for s in [gp] + gu + gl)}

    # ---- block-level part reconstructable from the grid: self-conjugate k (h = F/64 exactly, so H = -64 h) ----
    def sc_blocks(g):
        out = []
        for b in cg.BLK:
            if b['d'] != 10: continue
            h = g[b['k']]; imag = float(np.abs(h.imag).max()); H = -C * h.real
            w = np.linalg.eigvalsh(0.5 * (H + H.T)); sc = max(1.0, float(np.abs(w).max()))
            jj = list(range(1, 10)); Sch = H[0, 0] - H[0, jj] @ np.linalg.solve(H[np.ix_(jj, jj)], H[jj, 0])
            out.append({'k': list(b['k']), 'lambda_min_d2logZ': float(w[0]), 'violation': bool(w[0] < -TOL * sc), 'lapse_schur': float(Sch), 'max_abs_imag_h': imag})
        return out
    scp = sc_blocks(G); scu = [sc_blocks(g) for g in Gu]; scl = [sc_blocks(g) for g in Glu]
    allsc = scp + [r for x in scu + scl for r in x]
    rep['self_conjugate_blocks_from_grid'] = {
        'n_self_conjugate_blocks': len(scp), 'pooled': scp,
        'violations_pooled': sum(r['violation'] for r in scp), 'violations_all_members': sum(r['violation'] for r in allsc),
        'min_lambda_min_d2logZ_all_members': min(r['lambda_min_d2logZ'] for r in allsc),
        'min_lapse_schur_all_members': min(r['lapse_schur'] for r in allsc),
        'pooled_min_lambda_min_d2logZ': min(r['lambda_min_d2logZ'] for r in scp), 'pooled_min_lapse_schur': min(r['lapse_schur'] for r in scp),
        'note': 'The 28 pair blocks (d=20) are not recoverable from h, which keeps only (cc+ss)/2 and (cs-sc)/2; their block-level gate '
                'is available only as computed by analysis v003 from the captures (quoted under analysis_v003_block_gate).'}

    # ---- the analysis's own gate (stage0_lib_v001.gate = b7 transcription), quoted, plus agreement with this re-run ----
    aj = json.load(open(PIN['analysis_json'][0]))
    eg = aj['estimator']['gate']
    rep['analysis_v003_block_gate'] = {'quoted_from': 'STAGE0_ANALYSIS_V003.json estimator.gate', 'pooled': eg['pooled'],
                                       'per_process_blocks_violating': [g['blocks_violating'] for g in eg['per_process']],
                                       'per_process_grid_nodes_violating': [g['grid_nodes_violating'] for g in eg['per_process']],
                                       'per_process_min_lapse_schur': [g['min_lapse_schur'] for g in eg['per_process']],
                                       'per_process_min_lambda_min_d2logZ': [g['min_lambda_min_d2logZ'] for g in eg['per_process']],
                                       'loo_process_violating': eg['loo_process_violating'], 'loo_batch_violating': eg['loo_batch_violating'],
                                       'loo_batch_replicates': 64, 'admissible_under_gate': eg['admissible_under_gate']}
    rep['agreement_with_analysis_v003'] = {
        'pooled_max_lambda_max_h_abs_dev': abs(gp['max_lambda_max_h'] - eg['pooled']['max_lambda_max_h']),
        'pooled_min_Gamma_nn_abs_dev': abs(gp['min_Gamma_nn_where_invertible'] - eg['pooled']['min_Gamma_nn']),
        'per_process_max_lambda_max_h_max_abs_dev': max(abs(a['max_lambda_max_h'] - b['max_lambda_max_h']) for a, b in zip(gu, eg['per_process'])),
        'per_process_min_Gamma_nn_max_abs_dev': max(abs(a['min_Gamma_nn_where_invertible'] - b['min_Gamma_nn']) for a, b in zip(gu, eg['per_process']))}

    # ---- k = 0 lapse entry and band vs A2 ----
    h0 = float(G[0, 0, 0][0, 0].real); h0u = [float(g[0, 0, 0][0, 0].real) for g in Gu]; h0l = [float(g[0, 0, 0][0, 0].real) for g in Glu]
    se0 = math.sqrt((J - 1) / J * sum((v - np.mean(h0l)) ** 2 for v in h0l))
    a0 = float(A2[0, 0, 0][0, 0].real)
    a0c = {k.replace('single_chain_grid_', ''): float(za[k][0, 0, 0][0, 0].real) for k in za.files if k.startswith('single_chain_grid_')}
    k0 = aj['estimator']['k0_lapse']
    cen = aj['census_U']
    fq = {nm: [i for i, f in enumerate(cen[nm]['addendum_FQ_WC']) if not f['flat']] for nm in ('time_mean_active_slots', 'time_mean_U')}
    rep['k0'] = {
        'h_NN0_stage0_pooled': h0, 'process_jackknife_se': se0, 'saved_band_entry': float(se_u[0, 0, 0][0, 0]),
        'h_NN0_per_process': h0u, 'h_NN0_loo_process': h0l,
        'per_process_min_max': [min(h0u), max(h0u)],
        'analysis_json_h_NN0_pooled': k0['h_NN0_pooled'], 'analysis_json_se': k0['h_NN0_process_jackknife_se'],
        'abs_dev_grid_vs_analysis_scalar': abs(h0 - k0['h_NN0_pooled']), 'abs_dev_se_vs_analysis': abs(se0 - k0['h_NN0_process_jackknife_se']),
        'h_NN0_A2': a0, 'h_NN0_A2_single_chains': a0c,
        'difference_abs_A2_minus_abs_stage0': abs(a0) - abs(h0), 'difference_in_stage0_se_units': (abs(a0) - abs(h0)) / se0,
        'ratio_stage0_over_A2': h0 / a0,
        'prereg_reading_rule': '|h_S0| < 3.551 - 2 SE -> SUPPORTED (drift inflated A2 magnitude); > 3.551 + 2 SE contradicted; else INCONCLUSIVE',
        'prereg_reading': 'SUPPORTED' if abs(h0) < 3.551 - 2 * se0 else ('CONTRADICTED' if abs(h0) > 3.551 + 2 * se0 else 'INCONCLUSIVE'),
        'census_U_sealed_pass': cen['pass'], 'FQ_WC_all_flat': cen['addendum_FQ_WC_all_flat'], 'DRIFT_FLAG': cen['addendum_drift_flag'],
        'FQ_WC_failing_processes': fq,
        'drift_checked_label': bool(cen['addendum_FQ_WC_all_flat']),
        'k0_node_diag_stage0': np.real(np.diag(G[0, 0, 0])).tolist(), 'k0_node_diag_A2': np.real(np.diag(A2[0, 0, 0])).tolist(),
        'k0_node_diag_band': np.diag(se_u[0, 0, 0]).tolist(),
        'k0_node_rel_frobenius_vs_A2': float(np.linalg.norm(G[0, 0, 0] - A2[0, 0, 0]) / np.linalg.norm(A2[0, 0, 0])),
        'k0_node_diag_fields': ['N', 'R0', 'R1', 'R2', 'S00', 'S11', 'S22', 'sqrt2_S12', 'sqrt2_S02', 'sqrt2_S01']}
    # whole-grid band vs A2 difference
    d = np.abs(G - A2); m = se_u > 0
    rep['grid_vs_A2'] = {'analysis_distances': aj['estimator']['distances']['stage0_vs_A2'],
                         'entries_with_band': int(m.sum()),
                         'frac_entries_abs_diff_gt_2se': float((d[m] > 2 * se_u[m]).mean()),
                         'median_abs_diff_over_se': float(np.median(d[m] / se_u[m]))}

    # ---- background moments for the coefficient file (A2 builder's moments(), labels = pinned BG order) ----
    dirs = [Path(x['dir']) for x in (aj['inputs'][str(i)] for i in range(8))]
    for p in dirs:
        if 'KMAX' in str(p) or 'NGC' in str(p).upper(): raise SystemExit('refused path ' + str(p))
    means = []
    for i, p in enumerate(dirs):
        cap, files = S.load_capture(str(p / 'committed_capture'), ['background'])
        assert sorted(cap) == [0] and cap[0]['background'].shape == (16384, 9), (i, sorted(cap), cap[0]['background'].shape)
        means.append(cap[0]['background'].mean(0))
    pooled_row = np.mean(means, axis=0)
    mu, M, Cb = CL.moments(pooled_row, S.BG_LABELS)
    aniso = aj['anisotropy']
    rep['background'] = {'mu': mu, 'M': M, 'C': Cb, 'C_eigenvalues': np.linalg.eigvalsh(Cb), 'C_SPD': bool(np.linalg.eigvalsh(Cb)[0] > 0),
                         'C_vs_analysis_pooled_C_max_abs': float(np.abs(Cb - np.asarray(aniso['pooled']['C'])).max()),
                         'per_process_C_vs_analysis_max_abs': max(float(np.abs(CL.moments(mr, S.BG_LABELS)[2] - np.asarray(pp['C'])).max())
                                                                  for mr, pp in zip(means, aniso['per_process'])),
                         'A2_C_eigenvalues': np.linalg.eigvalsh(za['background_C']),
                         'rows_per_process': 16384, 'processes': 8}

    # ---- candidate coefficient file in the A2 schema ----
    a2_schema = {k: (list(za[k].shape), str(za[k].dtype)) for k in za.files}
    consumer_src = CONSUMER.read_text()
    consumer_keys = [k for k in ('source_hessian_grid', 'background_mu', 'background_C', 'background_M') if "f['%s']" % k in consumer_src]
    cand = OUTDIR / 'candidate' / 'STAGE0_POOLED8_CANDIDATE_GRID_V001.npz'
    if cand.exists(): raise SystemExit('candidate exists; refusing to overwrite')
    arrays = {'source_hessian_grid': np.array(G, dtype=np.complex128), 'background_mu': np.array(mu, dtype=np.float64),
              'background_M': np.array(M, dtype=np.float64), 'background_C': np.array(Cb, dtype=np.float64)}
    for i in range(J): arrays['single_chain_grid_stage0_p%d' % i] = np.array(Gu[i], dtype=np.complex128)
    np.savez(cand, **arrays)
    zc = np.load(cand, allow_pickle=False)
    roundtrip = all(np.array_equal(zc[k], v) for k, v in arrays.items())
    conj_res = max(float(np.abs(zc['source_hessian_grid'][tuple((-v) % L for v in k)] - zc['source_hessian_grid'][k].conj()).max()) for k in np.ndindex(L, L, L))
    core = ('source_hessian_grid', 'background_mu', 'background_M', 'background_C')
    rep['candidate_file'] = {
        'path': str(cand), 'sha256': sha(cand), 'bytes': cand.stat().st_size, 'keys': {k: (list(zc[k].shape), str(zc[k].dtype)) for k in zc.files},
        'A2_schema': a2_schema, 'core_keys_match_A2_shape_dtype': all(a2_schema[k] == (list(zc[k].shape), str(zc[k].dtype)) for k in core),
        'extra_keys_follow_A2_pattern': 'single_chain_grid_<name> (A2: single_chain_grid_<run>_c<chain>; here single_chain_grid_stage0_p<k>)',
        'consumer_keys_read_by_ddo_body_source_offset_root_v003_source_text': consumer_keys,
        'consumer_sha256': sha(CONSUMER),
        'roundtrip_equal': roundtrip, 'source_hessian_grid_equals_saved_stage0_pooled_grid': bool(np.array_equal(zc['source_hessian_grid'], G)),
        'partner_conjugacy_max_residual': conj_res, 'all_finite': all(bool(np.isfinite(zc[k]).all()) for k in zc.files),
        'target_free': 'built from STAGE0_ANALYSIS_V003 grids + the 8 stage-0 committed-capture background rows only; no galaxy/target file read',
        'status': 'CANDIDATE, NOT REGISTERED, NOT USED. Per sealed S0-FAIL-RHAT row: start-balanced graph-ensemble sensitivity grid only '
                  '(process-jackknife band), never a replacement for A2.'}
    zc.close()

    # ---- verdict ----
    sat_saved = rep['gate_saved_grids']['n_members_violating'] == 0
    sat_analysis = bool(eg['admissible_under_gate'])
    rep['verdict'] = {
        'CONVEXITY_ADMISSIBLE': bool(sat_saved and sat_analysis),
        'grid_node_test_rerun_here': {'members': 1 + 2 * J, 'members_violating': rep['gate_saved_grids']['n_members_violating'],
                                      'violating_nodes': rep['gate_saved_grids']['total_violating_nodes'], 'nodes_per_member': 64},
        'block_test_quoted_from_analysis': {'pooled_blocks_violating': eg['pooled']['blocks_violating'], 'processes_violating': sum(S.violates(g) for g in eg['per_process']),
                                            'loo_process_violating': eg['loo_process_violating'], 'loo_batch_violating': eg['loo_batch_violating']},
        'outcome_registered': aj['outcome'], 'wiring': aj['wiring']['class']}
    out = OUTDIR / 'GATE_V001.json'
    if out.exists(): raise SystemExit('GATE_V001.json exists; refusing to overwrite')
    rep['script'] = {'path': os.path.abspath(__file__), 'sha256': sha(__file__)}
    with open(out, 'x') as f: json.dump(jsonable(rep), f, indent=1)
    print(json.dumps(jsonable({k: rep[k] for k in ('verdict', 'anchor_A2_reproduction', 'agreement_with_analysis_v003', 'grid_objects')}), indent=1))
    print(json.dumps(jsonable({k: v for k, v in rep['gate_saved_grids'].items() if k not in ('per_process', 'loo_process')}), indent=1))
    print(json.dumps(jsonable({k: v for k, v in rep['self_conjugate_blocks_from_grid'].items() if k != 'pooled'}), indent=1))
    print(json.dumps(jsonable(rep['k0']), indent=1)); print(json.dumps(jsonable(rep['grid_vs_A2']), indent=1))
    print(json.dumps(jsonable(rep['background']), indent=1)); print(json.dumps(jsonable(rep['candidate_file']), indent=1))


if __name__ == '__main__':
    main()

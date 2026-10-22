"""P-96 stage-0 analysis V003 (successor of prelaunch_fix_v001/analysis/stage0_analysis_v002.py 7f6a1090...; applies
PREREG_STAGE0_V001 aee48b02..., PREREG_STAGE0_ADDENDUM_V001 34e5dd29..., PREREG_STAGE0_ADDENDUM_V002 b3a4d23f... and
PREREG_STAGE0_ADDENDUM_V003 f72bc001... to the 8 single-chain processes). Read-only on every input; writes only
OUT_PREFIX.json and OUT_PREFIX_grids.npz (both checked absent before anything is read; json exclusive create).
numpy only; the pinned operator/adapter/family recipe are imported (byte-checked) only to decode reference keys for the
addendum's tie-averaged C-bar. Never opens any NGC3198 file.

Deltas vs v002 (prelaunch_fix_v001/check/CHECK_V001 812671b4 F-1/F-2/F-3; ADDENDUM_V003 C0-C3), nothing else:
  * outcome(): ADDENDUM_V003 C1 precedence -- sealed rows 1-6 (INCOMPLETE, PASS-LIT, PASS-MA, FAIL-RHAT, FAIL-TAU,
    FAIL-CENSUS) always before the addendum classes S0-FAIL-STUCK and S0-UNASSESSABLE; unreachable residual ->
    ANALYSIS_ERROR_UNMAPPED (F-1);
  * read_process(): status=complete with a missing / empty / unloadable committed capture -> NOT COMPLETE with reason (F-2);
  * run_stage0(): refuses unless exactly 8 distinct existing run dirs whose self-declared chain index (monitor dir name,
    receipt.json / launch.json 'chain') equals their position, and the output files are absent (F-3);
  * outcome_mapping_inputs also lists stuck_processes.

Deltas of v002 vs v001 (CHECK_V001 bb7aae1b C-3, C-2 G-1/G-2; ADDENDUM_V002 B1-B6), nothing else:
  * a missing / 0-byte / partial / unparseable result.json, a result without sampler_result or stage0_binding, a
    non-complete status, a short or unloadable capture -> that process is NOT COMPLETE with a recorded reason (plus the
    monitor receipt's stop_reason when present); the n complete processes are analysed descriptively; outcome
    INCOMPLETE_n/8; sections that cannot be computed at that n are recorded as not_computed (the 8/8 path runs
    unguarded, exactly as v001);
  * outcome(): ADDENDUM_V002 B4 precedence (Rhat=inf counts as Rhat>1.1; S0-FAIL-STUCK; S0-UNASSESSABLE);
  * outcome_quoted: every S0-PASS carries DRIFT_FLAG (B5), with the flagged FQ-WC units and the calibrated sizes.
  The library (stage0_lib_v001.py) and tie-average module (tieavg_cbar_v001.py) are the v001 files, unchanged.

Modes:
  stage0  RUN_DIR_0 ... RUN_DIR_7 OUT_PREFIX     (each RUN_DIR holds result.json + committed_capture of one process)
  birthk  OUT_PREFIX                              (check A0: 2-chain BIRTHK capture vs the sampler's own reported analysis)
"""
import hashlib, importlib.util, json, math, os, re, sys, time
from pathlib import Path
import numpy as np
S0DIR = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/sampler_stage0_c2')
HERE = S0DIR / 'analysis'; ROOT = S0DIR          # v001 library location and package root (read-only)
sys.path.insert(0, str(HERE))
import stage0_lib_v001 as S
import tieavg_cbar_v001 as TA

UPC = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13')
X = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
A2_NPZ = (UPC / 'CLAUDE2/CRITICAL_PATH_EVALUATION_2026-10-17_V001/sampler_eval/CANDIDATE_4CHAIN_POOLED_GRID_V001.npz', '2e3a36d888ef8a89c9a2b6073ca6123656c31317c995962c11f34d434eca6ff7')
BK_EVAL = UPC / 'CLAUDE2/BIRTHK_PILOT_EVALUATION_2026-10-17_V001/out'
BK_CAP = UPC / 'CODEX1/OWNED_L4_WORM_BIRTHK_RUN_V001/committed_capture'
PREREG_SHA = 'aee48b022bccc29196a3dddb632be4a2132d1ff8942fb4217938d6b70355ea1f'
ADDENDUM_V001_SHA = '34e5dd29b1a0cd2abc048b869968f35a3f993e729a423ce20abcbadfa2931d69'
ADDENDUM_V002 = (S0DIR / 'prelaunch_fix_v001' / 'PREREG_STAGE0_ADDENDUM_V002.md', 'b3a4d23f9130dc2c1bf810883eea59eb4000522d192ba830e2b226a3091f7ae1')
ADDENDUM_V003 = (S0DIR / 'prelaunch_fix_v002' / 'PREREG_STAGE0_ADDENDUM_V003.md', 'f72bc001d7e345d760befb5492cc96e7ff8c0a3b39ba65c09aa3a7e1233d8a3b')
RUN_DIR_NAME = re.compile(r'^STAGE0_L4_BIRTHK_C(\d+)_RUN_V\d+$')     # ADDENDUM_V003 C3: monitor output dir form
CALIB_WC = (S0DIR / 'calib' / 'CALIB_FLAT_V003.json', '01a4a10dddba204e05cbd384e34db9933f5cc41f212265cf7e61b47762aab2ee')
MANIFEST = ROOT / 'starts' / 'STAGE0_STARTS_V001.json'
PINS = {'operator': (X / 'owned_retained_response_0405/owned_parent_operator_v003.py', 'a04f87954b68bb2dcc5a1af42a465b1d554ed1fc14d9b22d43e05e3e664f7f07'),
        'adapter': (UPC / 'helpers/coefficient_method/owned_diamond_registration_input_adapter_v001.py', '0705be7ca500a3b8329566ba014b80645231be2178ad5b8ef089dbca163b3f77'),
        'family_recipe': (UPC / 'helpers/coefficient_method/owned_L4_admission_family_recipe_DRAFT_v001.py', '86c2ee5319dd1277c630e15ca7ab9f224027bf638a281753e68dddecf1ca6bd7')}
L = 4; NC = 64; NA = NB = 192; NBIT = NA * NB; NS = 128; TIE_STRIDE = 16
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()


def jsonable(x):
    if isinstance(x, dict): return {str(k): jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [jsonable(v) for v in x]
    if isinstance(x, np.ndarray): return jsonable(x.tolist())
    if isinstance(x, np.generic): return jsonable(x.item())
    if isinstance(x, float) and not math.isfinite(x): return repr(x)
    return x


def load_pinned(name):
    p, want = PINS[name]
    if sha(p) != want: raise SystemExit('PIN MISMATCH ' + name)
    spec = importlib.util.spec_from_file_location('s0an_' + name, p); m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m; spec.loader.exec_module(m); return m


# ---------------- mixing over chains (PREREG section 2) ----------------
def mixing(units, BLK):
    """units: list of dicts with 'cap' (row arrays) and 'changed_in_measurement'. Returns per-block/background verdicts."""
    n = min(u['cap']['score_cells'].shape[0] for u in units)
    if any(u['cap']['score_cells'].shape[0] != n for u in units): raise ValueError('unequal measured rows across processes')
    ev = np.stack([u['cap']['events'].astype(np.float64) for u in units])
    stuck = [i for i, u in enumerate(units) if u['changed_in_measurement'] == 0]
    blocks = []; tally = {'lit': {}, 'ma': {}}
    def add(col, name, where):
        for rule, key in (('lit', 'status_lit'), ('ma', 'status_ma')):
            tally[rule][col[key]] = tally[rule].get(col[key], 0) + 1
        return dict(primary=name, where=where, **col)
    for b in BLK:
        Xs = np.stack([S.block_scores(u['cap']['score_cells'], NC, b) for u in units])      # (C, n, d)
        Ts = np.stack([S.block_contacts(u['cap']['allk_contacts'], b) for u in units])       # (C, n, entries)
        cols = []
        for a in range(b['d']): cols.append(add(S.column_verdict(Xs[:, :, a]), ['score', a], b['k']))
        for e, (pa, pb) in enumerate(b['ent']):
            ia, ib = sorted((b['nn'][pa], b['nn'][pb]))
            cols.append(add(S.column_verdict(Ts[:, :, e], exact_invariant_if_constant=False), ['contact', [ia, ib]], b['k']))
        cols.append(add(S.column_verdict(ev), ['events_per_path', None], b['k']))
        n_struct = b['d'] * (b['d'] + 1) // 2 - len(b['ent'])      # non-NN contacts: identically zero by LK3 -> exact_invariant
        st = [c['status_lit'] for c in cols]; sm = [c['status_ma'] for c in cols]
        blocks.append({'k': b['k'], 'structural_exact_invariant_contacts': n_struct, 'columns': cols,
                       'lit': 'failed' if (stuck or 'failed' in st) else ('unassessable' if 'unassessable' in st else 'passed'),
                       'ma': 'failed' if (stuck or 'failed' in sm) else ('unassessable' if 'unassessable' in sm else 'passed')})
    BGX = np.stack([u['cap']['background'] for u in units])
    bcols = [add(S.column_verdict(BGX[:, :, j]), ['read', S.BG_LABELS[j]], 'background') for j in range(9)]
    bcols.append(add(S.column_verdict(ev), ['events_per_path', None], 'background'))
    st = [c['status_lit'] for c in bcols]; sm = [c['status_ma'] for c in bcols]
    bg = {'columns': bcols, 'lit': 'failed' if (stuck or 'failed' in st) else ('unassessable' if 'unassessable' in st else 'passed'),
          'ma': 'failed' if (stuck or 'failed' in sm) else ('unassessable' if 'unassessable' in sm else 'passed')}
    allcols = [c for b in blocks for c in b['columns']] + bcols
    def joint(rule):
        s = [b[rule] for b in blocks] + [bg[rule]]
        return 'passed' if all(x == 'passed' for x in s) else ('failed' if 'failed' in s else 'unassessable')
    def num(v): return v is not None and math.isfinite(v)
    summ = {'rows_per_chain': n, 'chains': len(units), 'batch_length': n // S.N_BATCH, 'stuck_chains': stuck,
            'assessed_columns': len(allcols), 'status_counts': tally, 'R_LIT': joint('lit'), 'R_MA': joint('ma'),
            'blocks_passing_lit': sum(b['lit'] == 'passed' for b in blocks), 'blocks_passing_ma': sum(b['ma'] == 'passed' for b in blocks),
            'background_lit': bg['lit'], 'background_ma': bg['ma'],
            'columns_rhat_gt_1.1': sum(1 for c in allcols if num(c['rhat']) and c['rhat'] > S.RHAT_MAX),
            'max_rhat': max((c['rhat'] for c in allcols if num(c['rhat'])), default=None),
            'max_tau_per_chain': max((t for c in allcols for t in c['tau'] if num(t)), default=None),
            'max_tau_pooled': max((c['tau_pooled'] for c in allcols if num(c['tau_pooled'])), default=None),
            'lit_tau_failing_entries': sum(1 for c in allcols for t in c['tau'] if num(t) and (n // S.N_BATCH) < S.RATIO_MIN * t),
            'median_tau_pooled': float(np.median([c['tau_pooled'] for c in allcols if num(c['tau_pooled'])])) if any(num(c['tau_pooled']) for c in allcols) else None}
    return summ, blocks, bg


def census(units):
    out = {}
    for name in ('time_mean_active_slots', 'time_mean_U'):
        Xs = np.stack([u['cap'][name].astype(np.float64) for u in units]); v = S.column_verdict(Xs)
        fq = [S.flat_quarters(x) for x in Xs]
        out[name] = {'rhat': v['rhat'], 'tau': v['tau'], 'tau_pooled': v['tau_pooled'], 'two_part_lit': v['status_lit'],
                     'flat_quarters': fq, 'all_flat': all(f['flat'] for f in fq),
                     'pass': v['status_lit'] == 'passed' and all(f['flat'] for f in fq),
                     'addendum_FQ_WC': [S.flat_quarters_wc(x) for x in Xs], 'addendum_split_rhat_4': S.split_rhat(Xs),
                     'rd2_proposal_2_batch_se_flat': [rd2_flat(x) for x in Xs]}
    for j, nm in ((1, 'degree_1_count'), (3, 'degree_3_count')):
        Xs = np.stack([u['cap']['reference_degree_histogram'][:, j].astype(np.float64) for u in units]); v = S.column_verdict(Xs)
        out[nm] = {'descriptive_only': True, 'rhat': v['rhat'], 'tau': v['tau'], 'quarter_means': [S.flat_quarters(x)['quarter_means'] for x in Xs]}
    out['pass'] = out['time_mean_active_slots']['pass'] and out['time_mean_U']['pass']
    out['addendum_FQ_WC_all_flat'] = all(f['flat'] for nm in ('time_mean_active_slots', 'time_mean_U') for f in out[nm]['addendum_FQ_WC'])
    out['addendum_drift_flag'] = not out['addendum_FQ_WC_all_flat']
    return out


def rd2_flat(x):
    bm = np.asarray(x, float)[:8 * (len(x) // 8)].reshape(8, -1).mean(1); se = float(bm.std(ddof=1)) / math.sqrt(2)
    Q = bm.reshape(4, 2).mean(1); return bool(np.all(np.abs(Q - bm.mean()) <= 2 * se))


# ---------------- estimator (PREREG section 3) ----------------
def estimator(units, BLK, out_npz):
    n = units[0]['cap']['score_cells'].shape[0]; blen = n // S.N_BATCH
    sums = []                       # sums[unit][batch] = list over blocks
    for u in units:
        per_b = []
        Xb = [S.block_scores(u['cap']['score_cells'], NC, b) for b in BLK]; Tb = [S.block_contacts(u['cap']['allk_contacts'], b) for b in BLK]
        for bt in range(S.N_BATCH):
            sl = slice(bt * blen, (bt + 1) * blen)
            per_b.append([S.sums_for(Xb[i][sl], Tb[i][sl], b) for i, b in enumerate(BLK)])
        sums.append(per_b)
    flat = lambda sel: [s for (ui, bt), s in sel]
    allsel = [((ui, bt), sums[ui][bt]) for ui in range(len(units)) for bt in range(S.N_BATCH)]
    est = lambda sel: S.estimate(flat(sel), len(BLK))
    pooled = est(allsel); G = S.grid_arr(BLK, pooled, L)
    per_unit = [est([x for x in allsel if x[0][0] == ui]) for ui in range(len(units))]
    loo_u = [est([x for x in allsel if x[0][0] != ui]) for ui in range(len(units))]
    loo_b = [est([x for j, x in enumerate(allsel) if j != i]) for i in range(len(allsel))]
    Gu = np.array([S.grid_arr(BLK, e, L) for e in per_unit]); Glu = np.array([S.grid_arr(BLK, e, L) for e in loo_u]); Glb = np.array([S.grid_arr(BLK, e, L) for e in loo_b])
    J = len(units); se_u = np.sqrt((J - 1) / J * (np.abs(Glu - Glu.mean(0)) ** 2).sum(0))
    K = len(allsel); se_b = np.sqrt((K - 1) / K * (np.abs(Glb - Glb.mean(0)) ** 2).sum(0))
    gate_pooled = S.gate(BLK, pooled, L); gate_units = [S.gate(BLK, e, L) for e in per_unit]
    gate_lu = [S.gate(BLK, e, L) for e in loo_u]; gate_lb = [S.gate(BLK, e, L) for e in loo_b]
    admissible = (not S.violates(gate_pooled)) and not any(S.violates(g) for g in gate_units + gate_lu + gate_lb)
    # k = 0 lapse (block k=(0,0,0), field N, contact entry (0,0))
    b0 = [i for i, b in enumerate(BLK) if b['k'] == (0, 0, 0)][0]
    xs = [S.block_scores(u['cap']['score_cells'], NC, BLK[b0])[:, 0] for u in units]
    ts = [S.block_contacts(u['cap']['allk_contacts'], BLK[b0])[:, BLK[b0]['ent'].index((0, 0))] for u in units]
    def h0(xl, tl):
        x = np.concatenate(xl); t = np.concatenate(tl); return -(float(np.var(x)) + float(t.mean())) / NC, float(np.var(x)) / abs(float(t.mean()))
    hp, rp = h0(xs, ts); hl = [h0([x for j, x in enumerate(xs) if j != i], [t for j, t in enumerate(ts) if j != i])[0] for i in range(J)]
    h_se = math.sqrt((J - 1) / J * sum((v - np.mean(hl)) ** 2 for v in hl))
    k0 = {'h_NN0_pooled': hp, 'rho_pooled': rp, 'h_NN0_per_process': [h0([x], [t])[0] for x, t in zip(xs, ts)],
          'rho_per_process': [h0([x], [t])[1] for x, t in zip(xs, ts)], 'h_NN0_process_jackknife_se': h_se,
          'grid_entry_equals': float(np.real(G[0, 0, 0][0, 0]))}
    z = np.load(A2_NPZ[0]); assert sha(A2_NPZ[0]) == A2_NPZ[1]; A2 = z['source_hessian_grid']
    bkg = np.load(BK_EVAL / 'gate_coeff_grids.npz')['birthk_pooled_grid']
    dist = {'stage0_vs_A2': S.rel(G, A2, L), 'stage0_vs_birthk': S.rel(G, bkg, L),
            'leave_one_process_out_vs_pooled': [S.rel(g, G, L) for g in Glu], 'process_vs_pooled': [S.rel(g, G, L) for g in Gu]}
    np.savez(out_npz, stage0_pooled_grid=G, per_process_grids=Gu, loo_process_grids=Glu, process_jackknife_se=se_u, batch_jackknife_se=se_b)
    return {'rows_total': J * n, 'gate': {'pooled': gate_pooled, 'per_process': gate_units, 'loo_process_violating': sum(S.violates(g) for g in gate_lu),
                                          'loo_batch_violating': sum(S.violates(g) for g in gate_lb), 'admissible_under_gate': admissible},
            'k0_lapse': k0, 'distances': dist, 'grid_npz': str(out_npz),
            'max_rel_process_jackknife_se': float(np.max(se_u / np.maximum(np.abs(G), 1e-300)[...])) if False else None,
            'process_jackknife_se_frobenius_over_grid': float(np.linalg.norm(se_u) / np.linalg.norm(G)),
            'batch_jackknife_se_frobenius_over_grid': float(np.linalg.norm(se_b) / np.linalg.norm(G))}, pooled, per_unit


# ---------------- anisotropy (PREREG section 4, addendum A1/A2) ----------------
def anisotropy(units, axes, A2_stats):
    Cs = [S.cbar_from_mean_row(u['cap']['background'].mean(0), NC) for u in units]
    Cp = S.cbar_from_mean_row(np.mean([u['cap']['background'].mean(0) for u in units], axis=0), NC)
    J = len(units); sl = [S.s_vec(S.cbar_from_mean_row(np.mean([u['cap']['background'].mean(0) for j, u in enumerate(units) if j != i], axis=0), NC)) for i in range(J)]
    se = np.sqrt((J - 1) / J * ((np.array(sl) - np.mean(sl, 0)) ** 2).sum(0)); sp = S.s_vec(Cp); q = float(np.linalg.norm(sp))
    z = float(abs(sp[0]) / se[0]) if se[0] > 0 else None
    mt = S.memory_test(Cs, axes)
    D = float(np.mean([S.s_vec(C)[0] for C, a in zip(Cs, axes) if a == 'x']) - np.mean([S.s_vec(C)[0] for C, a in zip(Cs, axes) if a == 'y']))
    out = {'per_process': [{'axis': a, 'C': C, 's': S.s_vec(C), 'q': float(np.linalg.norm(S.s_vec(C))), 'major_axis_deg': S.axis_deg(C)} for C, a in zip(Cs, axes)],
           'pooled': {'C': Cp, 's': sp, 'q': q, 'major_axis_deg': S.axis_deg(Cp), 'process_jackknife_se_s': se, 'z_s1': z,
                      'class': 'WITHIN_REFERENCE' if q <= 0.016 else 'EXCEEDS_REFERENCE',
                      'locate_before_stage1': bool(q > 0.016 and z is not None and z >= 3)},
           'memory_background_declared_axis': mt, 'memory_class_background': 'START_MEMORY_DETECTED' if (mt['p_randomization'] <= 0.05 or mt['m_largest_diag_equals_start_axis'] >= 6) else 'NO_MEMORY_DETECTED',
           'inplane_contrast_D': D}
    out.update(A2_stats)
    return out


def tieavg_reference(units, files_of, start_keys, axes):
    """ADDENDUM A1/A2: actual and tie-averaged C-bar of reference-dwell states at stride 16; start C-bar (tie-averaged)."""
    op, ad, fr = load_pinned('operator'), load_pinned('adapter'), load_pinned('family_recipe')
    binding = ad.build_inputs(L=4, coefficients=dict(fr.TRIAL), port_cache_entries=4096); reg = binding['registration']
    frame = tuple(tuple(v / 2. for v in p) for p in ad.PROTOTYPES4)
    reg['port_vectors'] = {'A': frame, 'B': tuple(tuple(-v for v in r) for r in frame)}
    reg['whitening'] = tuple(tuple(ad.W if i == j else 0. for j in range(3)) for i in range(3)); reg['max_cached_graphs'] = 4
    ctx = ad.bind_context(operator_module=op, binding=binding); po = reg['port_order']
    Ca, Ct, Cst = [], [], []
    for ui, u in enumerate(units):
        sa = np.zeros((3, 3)); st = np.zeros((3, 3)); cnt = 0
        for mid, key in S.iter_keys(files_of[ui], u['chain_id']):
            if mid % TIE_STRIDE: continue
            a, t, _ = TA.cbar_pair(dict(op.state_labels(context=ctx, state=key)), ad, po, L); sa += a; st += t; cnt += 1
        Ca.append(sa / cnt); Ct.append(st / cnt)
        Cst.append(TA.cbar_pair(dict(op.state_labels(context=ctx, state=start_keys[ui])), ad, po, L)[1])
    res = {'stride': TIE_STRIDE, 'states_per_process': cnt,
           'per_process': [{'axis': a, 'C_actual_ref': A, 'C_tieavg_ref': T, 's_actual_ref': S.s_vec(A), 's_tieavg_ref': S.s_vec(T),
                            'C_tieavg_start': C0, 's_tieavg_start': S.s_vec(C0)} for A, T, C0, a in zip(Ca, Ct, Cst, axes)],
           'pooled_tieavg_ref': {'C': np.mean(Ct, 0), 's': S.s_vec(np.mean(Ct, 0)), 'q': float(np.linalg.norm(S.s_vec(np.mean(Ct, 0))))},
           'pooled_actual_ref': {'C': np.mean(Ca, 0), 's': S.s_vec(np.mean(Ca, 0)), 'q': float(np.linalg.norm(S.s_vec(np.mean(Ca, 0))))}}
    m1 = S.memory_test(Ct, axes); res['A1_memory_tieavg_declared_axis'] = m1
    res['A1_class'] = 'START_MEMORY_DETECTED' if (m1['p_randomization'] <= 0.05 or m1['m_largest_diag_equals_start_axis'] >= 6) else 'NO_MEMORY_DETECTED'
    m2 = S.overlap_memory_test(Ct, Cst); res['A2_start_graph_overlap'] = m2
    res['A2_class'] = 'START_GRAPH_MEMORY' if m2['p_permutation'] <= 0.05 else 'NO_START_GRAPH_MEMORY_DETECTED'
    return {'addendum_tieavg': res}


# ---------------- wiring (PREREG section 5) ----------------
def wiring(units, files_of):
    n = units[0]['cap']['score_cells'].shape[0]; q = n // 4; P = []; Ph = []; S16 = []; own = []
    for ui, u in enumerate(units):
        pq = np.zeros((4, NBIT)); ph = np.zeros((2, NBIT)); prev_sl = None; tog = np.zeros(NS, int); cum = []
        always = np.ones(NBIT, bool); ever_sl_inactive = np.zeros(NS, bool); stride = []
        for mid, key in S.iter_keys(files_of[ui], u['chain_id']):
            e = S.int_bits(key[1], NBIT); sl = S.int_bits(key[0], NS)
            pq[min(mid // q, 3)] += e; ph[min(mid // (n // 2), 1)] += e; always &= e; ever_sl_inactive |= ~sl
            if prev_sl is not None: tog += (sl != prev_sl)
            prev_sl = sl
            if (mid + 1) % q == 0: cum.append(int((tog > 0).sum()))
            if mid % 16 == 0: stride.append(np.packbits(e))
        P.append(pq / q); Ph.append(ph / (n // 2)); S16.append(np.array(stride))
        own.append({'owners_ever_toggled_cumulative_by_quarter': cum, 'owner_toggles_total': int(tog.sum()), 'owners_ever_inactive': int(ever_sl_inactive.sum()),
                    'edges_always_present': int(always.sum()), 'present_edges_mean': float(pq.sum(1).sum() / n)})
    cosv = lambda a, b: float(a @ b / math.sqrt((a @ a) * (b @ b)))
    J = len(units); pairs = [(i, j) for i in range(J) for j in range(i + 1, J)]
    om_q = [[cosv(P[i][qq], P[j][qq]) for (i, j) in pairs] for qq in range(4)]
    om_self = [cosv(Ph[i][0], Ph[i][1]) for i in range(J)]
    rho_w = float(np.mean(om_q[3]) / np.mean(om_self))
    shared = [[float(np.mean([np.unpackbits(S16[i][r] & S16[j][r]).sum() for r in range(len(S16[i]))]))] for (i, j) in pairs]
    pool = np.mean([P[i].mean(0) for i in range(J)], 0)
    return {'omega_between_mean_by_quarter': [float(np.mean(v)) for v in om_q], 'omega_self_per_process': om_self, 'rho_w': rho_w,
            'class': 'WIRING_MIXED' if rho_w >= 0.9 else ('WIRING_CHAIN_SPECIFIC' if rho_w <= 0.5 else 'WIRING_PARTIAL'),
            'trend_Q4_minus_Q1': float(np.mean(om_q[3]) - np.mean(om_q[0])),
            'shared_present_edges_same_index_stride16_mean_over_pairs': float(np.mean(shared)),
            'mixed_reference_sum_p_pool_sq': float((pool ** 2).sum()),
            'independent_reference_mean_sum_pi_pj': float(np.mean([(P[i].mean(0) * P[j].mean(0)).sum() for (i, j) in pairs])),
            'owners': own}


# ---------------- outcome (PREREG section 6) ----------------
def tau_leg_inputs(blocks, bg, n):
    """ADDENDUM_V002 B0: per assessed column, Rhat=inf, assessed tau-leg failure, tau unassessable (with processes)."""
    blen = n // S.N_BATCH; cols = [c for b in blocks for c in b['columns']] + bg['columns']
    rinf = 0; fail = 0; unass = []
    for c in cols:
        if c['status_ma'] == 'exact_invariant': continue
        if c['rhat'] is not None and c['rhat'] == math.inf: rinf += 1
        tp = c['tau_pooled']; taus = c['tau']
        if (tp is not None and blen < S.RATIO_MIN * tp) or any(t is not None and blen < S.RATIO_MIN * t / S.MA_GUARD for t in taus): fail += 1
        if tp is None or any(t is None for t in taus):
            unass.append({'where': c['where'], 'primary': c['primary'], 'pooled_tau_missing': tp is None,
                          'processes_tau_missing': [i for i, t in enumerate(taus) if t is None],
                          'rhat_constant_all_processes': c['rhat'] is None})
    return {'blen': blen, 'columns_rhat_inf': rinf, 'columns_tau_leg_failed_assessed': fail,
            'columns_tau_unassessable': len(unass), 'tau_unassessable_columns': unass}


def outcome(mx, cen, wire, n_complete, est, ani, tl=None):
    """ADDENDUM_V003 C1 precedence (replaces ADDENDUM_V002 B4): sealed section-6 rows 1-6 in v001 order always first;
    the addendum classes (rows 7, 8) only where no sealed row's condition holds; row 9 is the unreachable residual."""
    if n_complete < 8: return 'INCOMPLETE_%d/8' % n_complete                                          # 1 sealed
    rh_fail = mx['columns_rhat_gt_1.1'] > 0 or tl['columns_rhat_inf'] > 0
    if mx['R_LIT'] == 'passed' and cen['pass']: return 'S0-PASS-LIT'                                 # 2 sealed
    if not rh_fail and mx['R_MA'] == 'passed' and cen['pass']: return 'S0-PASS-MA'                   # 3 sealed
    if rh_fail: return 'S0-FAIL-RHAT'                                                                # 4 sealed (B3)
    if mx['R_MA'] != 'passed' and tl['columns_tau_leg_failed_assessed'] > 0: return 'S0-FAIL-TAU'    # 5 sealed (B0 reading)
    if (mx['R_LIT'] == 'passed' or mx['R_MA'] == 'passed') and not cen['pass']: return 'S0-FAIL-CENSUS'  # 6 sealed
    if mx['stuck_chains']: return 'S0-FAIL-STUCK'                                                    # 7 addendum (B2)
    if mx['R_MA'] != 'passed' and tl['columns_tau_unassessable'] > 0: return 'S0-UNASSESSABLE'       # 8 addendum (B1)
    return 'ANALYSIS_ERROR_UNMAPPED'                                                                 # 9 integrity case


def drift_quote(oc, cen):
    """ADDENDUM_V002 B5: every S0-PASS is quoted with DRIFT_FLAG; flagged FQ-WC units carry the calibrated sizes at the
    bracketing calibrated tau (CALIB_FLAT_V003, no interpolation)."""
    if not oc.startswith('S0-PASS'): return {'outcome_quoted': oc, 'drift_flag': cen.get('addendum_drift_flag') if isinstance(cen, dict) else None}
    if sha(CALIB_WC[0]) != CALIB_WC[1]: raise SystemExit('PIN MISMATCH calib')
    cal = json.loads(CALIB_WC[0].read_text()); grid = sorted(int(k.split('_')[1]) for k in cal)
    flagged = []
    for nm in ('time_mean_active_slots', 'time_mean_U'):
        for p, f in enumerate(cen[nm]['addendum_FQ_WC']):
            if f['flat']: continue
            t = f.get('tau_c', f.get('tau_w'))
            lo = max([g for g in grid if t is not None and g <= t], default=None); hi = min([g for g in grid if t is not None and g >= t], default=None)
            sz = lambda g: None if g is None else {'tau': g, 'WC_unit_false_failure': cal['tau_%d' % g]['WC_unit_false_failure'], 'WC_family_false_failure': cal['tau_%d' % g]['WC_family_false_failure']}
            flagged.append({'series': nm, 'process_position': p, 'tau': t, 'max_dev_over_se': f['max_dev_over_se'], 'calibrated_size_below': sz(lo), 'calibrated_size_above': sz(hi)})
    df = bool(cen['addendum_drift_flag'])
    return {'outcome_quoted': '%s [DRIFT_FLAG=%s]' % (oc, 'true' if df else 'false'), 'drift_flag': df, 'drift_flag_units': flagged}


def k0_drift_reading(cen, est):
    if not cen['pass']: return {'reading': 'NOT_MADE (census/U did not pass in every process)', 'addendum_drift_checked': False}
    h = est['k0_lapse']['h_NN0_pooled']; se = est['k0_lapse']['h_NN0_process_jackknife_se']; a2 = 3.551
    r = 'SUPPORTED' if abs(h) < a2 - 2 * se else ('CONTRADICTED' if abs(h) > a2 + 2 * se else 'INCONCLUSIVE')
    return {'reading': r, 'abs_h_stage0': abs(h), 'se': se, 'abs_h_A2': a2, 'addendum_drift_checked': cen['addendum_FQ_WC_all_flat']}


CAP_KEYS = ['score_cells', 'allk_contacts', 'background', 'events', 'time_mean_active_slots', 'time_mean_U', 'reference_degree_histogram']


def read_process(k, d, man):
    """ADDENDUM_V002 B6. Returns (input record, loaded unit or None). A process is complete only if every check passes;
    otherwise the record carries incomplete_reason. A present-but-mismatched binding is a provenance error (raises, as v001)."""
    d = Path(d); rec = {'dir': str(d), 'complete': False}
    rp = d / 'receipt.json'
    if rp.is_file():
        try:
            rc = json.loads(rp.read_text())
            rec['monitor_receipt'] = {'sha256': sha(rp), 'status': rc.get('status'), 'stop_reason': rc.get('stop_reason'), 'exit_code': rc.get('exit_code'),
                                      'scientific_status': rc.get('scientific_status')}
        except Exception as exc:
            rec['monitor_receipt'] = {'sha256': sha(rp), 'unparseable': repr(exc)}
    f = d / 'result.json'
    def stop(reason, unit=None):
        rec['incomplete_reason'] = reason; return rec, unit
    if not f.is_file(): return stop('result.json missing')
    raw = f.read_bytes(); rec['result_sha256'] = hashlib.sha256(raw).hexdigest(); rec['result_bytes'] = len(raw)
    if len(raw) == 0: return stop('result.json empty (0 bytes): the worker never wrote its result (killed: monitor MEMORY_CAP/WALL_CAP/OUTPUT_CAP or external termination)')
    try: r = json.loads(raw.decode('utf-8'))
    except (ValueError, UnicodeDecodeError) as exc: return stop('result.json not parseable (partial write?): ' + repr(exc)[:300])
    if not isinstance(r, dict): return stop('result.json is not a JSON object')
    rec['status'] = r.get('status')
    exc = r.get('exception') if isinstance(r.get('exception'), dict) else None
    exc_txt = '' if exc is None else '; exception %s: %s' % (exc.get('type'), str(exc.get('message'))[:300])
    b = r.get('stage0_binding')
    if not isinstance(b, dict): return stop('no stage0_binding (status=%s%s)' % (rec['status'], exc_txt))
    if b['chain'] != k or b['start']['key_text_sha256'] != man['starts'][k]['start_key_text_sha256'] or b['prereg_sha256'] != PREREG_SHA:
        raise ValueError('process %d binding does not match the manifest/prereg' % k)
    rec['spec_sha256'] = b['spec_sha256']; rec['start'] = b['start']
    sr = r.get('sampler_result')
    if not isinstance(sr, dict): return stop('no sampler_result (status=%s%s)' % (rec['status'], exc_txt))
    if r['status'] != 'complete':
        try:      # descriptive: how many rows were committed (never used in any statistic)
            cap, files = S.load_capture(str(d / 'committed_capture'), CAP_KEYS); rec['rows'] = int(cap[0]['score_cells'].shape[0]) if 0 in cap else 0; rec['blocks'] = len(files)
        except Exception as e: rec['capture_unloadable'] = repr(e)[:300]
        return stop('status=%s%s' % (r['status'], exc_txt))
    # status complete: v001's integrity checks raise; a missing / empty / unloadable capture is NOT COMPLETE (ADDENDUM_V003 C2)
    if sr['all_momentum']['background']['labels'] != S.BG_LABELS: raise ValueError('background label order')
    cd = d / 'committed_capture'
    try: cap, files = S.load_capture(str(cd), CAP_KEYS)
    except Exception as e:
        rec['capture_unloadable'] = repr(e)[:300]
        return stop('status=complete but committed capture unloadable (%s): %s' % ('directory missing' if not cd.is_dir() else 'load failed', repr(e)[:300]))
    if not cap:
        rec['rows'] = 0; rec['blocks'] = len(files)
        return stop('status=complete but committed capture holds no rows (%d block files)' % len(files))
    if list(cap) != [0]: raise ValueError('process %d committed capture holds chain ids %s, not [0]' % (k, list(cap)))
    complete = r['status'] == 'complete' and cap[0]['score_cells'].shape[0] == r['schedule_binding']['measurement_sweeps']
    rec['rows'] = int(cap[0]['score_cells'].shape[0]); rec['blocks'] = len(files); rec['complete'] = bool(complete)
    if not complete: return stop('rows %d != measurement_sweeps %d' % (rec['rows'], r['schedule_binding']['measurement_sweeps']))
    return rec, {'cap': cap[0], 'chain_id': 0, 'changed_in_measurement': sr['diagnostics']['chains'][0]['changed_path_accepts_in_measurement'],
                 'complete': True, 'files': files, 'metadata': sr['all_momentum']['metadata']}


def refuse_unless_eight_in_order(run_dirs, out_prefix):
    """ADDENDUM_V003 C3: refuse (SystemExit, nothing read beyond the declared chain indices, nothing written) unless exactly
    8 distinct existing run dirs, each self-declared chain index equal to its position, and absent output files."""
    if len(run_dirs) != 8: raise SystemExit('REFUSED (ADDENDUM_V003 C3): %d run dirs given, exactly 8 required' % len(run_dirs))
    ds = [Path(d) for d in run_dirs]
    for k, d in enumerate(ds):
        if not d.is_dir(): raise SystemExit('REFUSED (ADDENDUM_V003 C3): position %d is not an existing directory: %s' % (k, d))
    res = [d.resolve() for d in ds]
    if len(set(res)) != 8: raise SystemExit('REFUSED (ADDENDUM_V003 C3): run dirs are not pairwise distinct')
    for k, d in enumerate(ds):
        m = RUN_DIR_NAME.match(d.resolve().name)
        if m and int(m.group(1)) != k: raise SystemExit('REFUSED (ADDENDUM_V003 C3): position %d holds %s (chain %s)' % (k, d.name, m.group(1)))
        for fn in ('receipt.json', 'launch.json'):
            p = d / fn
            if not p.is_file(): continue
            try: c = json.loads(p.read_text()).get('chain')
            except Exception: continue
            if isinstance(c, int) and not isinstance(c, bool) and c != k:
                raise SystemExit('REFUSED (ADDENDUM_V003 C3): position %d %s declares chain %d' % (k, fn, c))
    op = Path(str(out_prefix))
    if not op.parent.is_dir(): raise SystemExit('REFUSED (ADDENDUM_V003 C3): output parent directory missing: %s' % op.parent)
    for suf in ('.json', '_grids.npz'):
        if Path(str(out_prefix) + suf).exists(): raise SystemExit('REFUSED (ADDENDUM_V003 C3): output exists: %s%s' % (out_prefix, suf))


def run_stage0(run_dirs, out_prefix):
    t0 = time.time()
    if sha(ADDENDUM_V002[0]) != ADDENDUM_V002[1]: raise SystemExit('PIN MISMATCH ADDENDUM_V002')
    if sha(ADDENDUM_V003[0]) != ADDENDUM_V003[1]: raise SystemExit('PIN MISMATCH ADDENDUM_V003')
    refuse_unless_eight_in_order(run_dirs, out_prefix)
    man = json.loads(MANIFEST.read_text()); units = []; files_of = []; keep = []
    rec = {'inputs': {}, 'prereg_sha256': PREREG_SHA, 'addendum_v001_sha256': ADDENDUM_V001_SHA, 'addendum_v002_sha256': ADDENDUM_V002[1],
           'addendum_v003_sha256': ADDENDUM_V003[1]}
    md = None
    for k, d in enumerate(run_dirs):
        ri, u = read_process(k, d, man); rec['inputs'][k] = ri
        if u is None: continue
        if md is None: md = u['metadata']
        elif u['metadata']['blocks'] != md['blocks']: raise ValueError('block metadata differ across processes')
        files_of.append(u.pop('files')); u.pop('metadata'); units.append(u); keep.append(k)
    n_complete = len(units); guarded = n_complete < 8
    rec['n_complete'] = n_complete; rec['complete_processes'] = keep
    rec['incomplete_processes'] = {k: rec['inputs'][k]['incomplete_reason'] for k in range(len(run_dirs)) if not rec['inputs'][k]['complete']}
    if guarded:
        rec['descriptive_only'] = ('INCOMPLETE_%d/8: no rule verdict (PREREG section 6); the %d complete processes are analysed '
                                   'descriptively; class labels inside sections are descriptive only (ADDENDUM_V002 B6)' % (n_complete, n_complete))
    def section(name, fn):
        if not guarded: return fn()
        if n_complete == 0: return {'not_computed': 'no complete process'}
        try: return fn()
        except Exception as exc: return {'not_computed': '%s at n=%d: %s' % (name, n_complete, repr(exc)[:400])}
    ok = lambda x: isinstance(x, dict) and 'not_computed' not in x
    axes = [man['starts'][k]['axis'] for k in keep]; start_keys = [tuple(int(h, 16) for h in man['starts'][k]['start_key_hex']) for k in keep]
    BLK = S.blocks_meta(md) if md is not None else None
    M = section('mixing', lambda: dict(zip(('mx', 'blocks', 'bg'), mixing(units, BLK))))
    mx, blocks, bg = (M['mx'], M['blocks'], M['bg']) if ok(M) else (M, [], M)
    cen = section('census', lambda: census(units))
    E = section('estimator', lambda: dict(zip(('est', 'pooled', 'per_unit'), estimator(units, BLK, Path(str(out_prefix) + '_grids.npz')))))
    est = E['est'] if ok(E) else E
    A12 = section('tieavg_reference', lambda: tieavg_reference(units, files_of, start_keys, axes))
    ani = section('anisotropy', lambda: anisotropy(units, axes, A12 if ok(A12) else {'addendum_tieavg': A12}))
    wire = section('wiring', lambda: wiring(units, files_of))
    tl = section('tau_leg_inputs', lambda: tau_leg_inputs(blocks, bg, mx['rows_per_chain'])) if ok(M) else {'not_computed': 'mixing not computed'}
    oc = outcome(mx, cen, wire, n_complete, est, ani, tl)
    if guarded: k0r = {'reading': 'NOT_MADE (%s: descriptive only)' % oc, 'addendum_drift_checked': False}
    else: k0r = k0_drift_reading(cen, est)
    rec.update({'mixing_summary': mx, 'census_U': cen, 'estimator': est, 'anisotropy': ani, 'wiring': wire,
                'outcome': oc, 'k0_drift_reading': k0r,
                'block_verdicts': [{'k': b['k'], 'lit': b['lit'], 'ma': b['ma'], 'worst_rhat': max((c['rhat'] for c in b['columns'] if c['rhat'] is not None and math.isfinite(c['rhat'])), default=None),
                                    'max_tau_pooled': max((c['tau_pooled'] for c in b['columns'] if c['tau_pooled'] is not None), default=None)} for b in blocks],
                'background_verdict': bg, 'columns': [c for b in blocks for c in b['columns']]})
    if ok(tl): tl = dict(tl, stuck_processes=[keep[i] for i in mx['stuck_chains']])     # ADDENDUM_V003 C1b: listed next to the class
    rec['outcome_mapping_inputs'] = tl
    rec.update(drift_quote(oc, cen) if ok(cen) else {'outcome_quoted': oc, 'drift_flag': None})
    rec['seconds'] = round(time.time() - t0, 1)
    with open(str(out_prefix) + '.json', 'x') as f: json.dump(jsonable(rec), f, indent=1); f.write('\n')
    g = lambda x, *ks: (x if not ks else (g(x.get(ks[0]), *ks[1:]) if isinstance(x, dict) else None))
    print(json.dumps(jsonable({'outcome': oc, 'outcome_quoted': rec['outcome_quoted'], 'n_complete': n_complete, 'incomplete': rec['incomplete_processes'],
                               'mixing': mx, 'census_pass': g(cen, 'pass'), 'gate_admissible': g(est, 'gate', 'admissible_under_gate'),
                               'k0': g(est, 'k0_lapse'), 'aniso_pooled': g(ani, 'pooled'), 'memory': g(ani, 'memory_class_background'), 'A1': g(ani, 'addendum_tieavg', 'A1_class'),
                               'A2': g(ani, 'addendum_tieavg', 'A2_class'), 'wiring': g(wire, 'class'), 'rho_w': g(wire, 'rho_w'), 'seconds': rec['seconds']}), indent=1))


def run_birthk(out_prefix):
    """Check A0: rebuild the BIRTHK 2-chain analysis from its committed capture and compare with the sampler's own numbers
    (b1 extract out/birthk_blocks.json, CONFIRMED by its review) and the b7 grid."""
    meta = json.load(open(BK_EVAL / 'birthk_meta.json')); bj = json.load(open(BK_EVAL / 'birthk_blocks.json'))
    cap, files = S.load_capture(str(BK_CAP), ['score_cells', 'allk_contacts', 'background', 'events'])
    units = [{'cap': cap[c], 'chain_id': c, 'changed_in_measurement': bj['diagnostics_chains'][c]['changed_path_accepts_in_measurement']} for c in (0, 1)]
    BLK = S.blocks_meta(meta); mx, blocks, bg = mixing(units, BLK)
    dr = dt = 0.0; ds = 0; nc = 0
    for mine, ref in zip(blocks, bj['blocks']):
        assert tuple(mine['k']) == tuple(ref['k'])
        refc = {json.dumps(c['primary']): c for c in ref['columns']}
        for c in mine['columns']:
            rc = refc[json.dumps(c['primary'])]; nc += 1
            if c['rhat'] is not None and rc['rhat'] is not None: dr = max(dr, abs(c['rhat'] - rc['rhat']))
            for a, b in zip(c['tau'], rc['tau']):
                if a is not None and b is not None: dt = max(dt, abs(a - b))
            ds += c['status_lit'] != rc['status']
        for rc in ref['columns']:
            if rc['primary'][0] == 'contact' and rc['status'] != 'exact_invariant':
                i, j = rc['primary'][1]
                if not (i in BLK[0]['nn'] or True): pass
    refbg = {json.dumps(c['primary']): c for c in bj['background']['columns']}
    for c in bg['columns']:
        rc = refbg[json.dumps(c['primary'])]; nc += 1
        if c['rhat'] is not None and rc['rhat'] is not None: dr = max(dr, abs(c['rhat'] - rc['rhat']))
        for a, b in zip(c['tau'], rc['tau']):
            if a is not None and b is not None: dt = max(dt, abs(a - b))
        ds += c['status_lit'] != rc['status']
    struct_ref = sum(1 for b in bj['blocks'] for c in b['columns'] if c['status'] == 'exact_invariant')
    struct_mine = sum(b['structural_exact_invariant_contacts'] for b in blocks)
    est, pooled, per_unit = estimator(units, BLK, Path(str(out_prefix) + '_grids.npz'))
    dH = max(float(np.abs(e['H'] - np.asarray(b['d2logZ_deta2_pooled'], float)).max()) for e, b in zip(pooled, bj['blocks']))
    dHc = max(float(np.abs(per_unit[c][i]['H'] - np.asarray(bj['blocks'][i]['d2logZ_deta2_per_chain'][c], float)).max()) for c in (0, 1) for i in range(len(BLK)))
    G = np.load(str(out_prefix) + '_grids.npz')['stage0_pooled_grid']; dG = float(np.abs(G - np.load(BK_EVAL / 'gate_coeff_grids.npz')['birthk_pooled_grid']).max())
    res = {'columns_compared': nc, 'max_abs_rhat_diff': dr, 'max_abs_tau_diff': dt, 'status_mismatches': ds,
           'exact_invariant_columns_reference': struct_ref, 'structural_exact_invariant_mine': struct_mine,
           'reference_joint_status': bj['all_momentum_mixing']['status'], 'mine_R_LIT': mx['R_LIT'],
           'max_abs_pooled_d2logZ_diff': dH, 'max_abs_per_chain_d2logZ_diff': dHc, 'max_abs_grid_diff_vs_b7': dG,
           'k0_lapse': est['k0_lapse'], 'gate_admissible': est['gate']['admissible_under_gate'],
           'A0_pass': dr <= 1e-10 and dt <= 1e-10 and ds == 0 and struct_ref == struct_mine and dH <= 1e-9 and dG <= 1e-9}
    with open(str(out_prefix) + '.json', 'x') as f: json.dump(jsonable(res), f, indent=1); f.write('\n')
    print(json.dumps(jsonable(res), indent=1))


if __name__ == '__main__':
    if sys.argv[1] == 'stage0': run_stage0(sys.argv[2:-1], sys.argv[-1])
    elif sys.argv[1] == 'birthk': run_birthk(sys.argv[2])
    else: raise SystemExit(__doc__)

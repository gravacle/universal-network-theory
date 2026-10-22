"""Lens R2-B runner. Installs a fence, loads the v003g module (48a1e48a...) and this lens's tools by path,
recomputes the TSR flag set from pinned target-free records, runs the synthetic edge cases and writes
CASES_R2B.json and TSR_RECOMPUTE_R2B.json with exclusive create. Synthetic data only; nothing launched."""
import sys, os, hashlib, json, importlib.util, bisect

HERE = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/miss_reading_prereg_c4/r2/checks_round2/newdefects'
MOD = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/prediction_freeze_c2v003g_cx3v001.py'
SLOTS = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json'
NODES = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/REGISTERED_ROUTE_B_GL_NODES_CX3V001.json'
N1 = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/out/K32_RECORDS_COMPLETE_V001_N1.json'
CMP = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/out/K32_COMPARE_COMPLETE_V001.json'
PINS = {MOD: '48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405',
        SLOTS: 'd3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969',
        NODES: 'ec1dcca572f295dab24e343650a519b6c96e3557e6ccc603f453dea490cb717d',
        N1: '8867c3766cc08585286ca969d4aa3fdec47fd9b15a8fe815d466346119c95c70',
        CMP: '6f095f64a1f1acc2ad2910af12f645e18acdf16fb62bfd936386a61c47ef30e9'}
FORBIDDEN_NAMES = ('rotmod', 'vobs', 'massmodel', 'sparc', 'uvt_', 'kmax_a2f10_c5h')
READ_OK = [HERE + '/', MOD, os.path.dirname(MOD) + '/__pycache__/', SLOTS, NODES, N1, CMP, sys.base_prefix, sys.prefix,
           '/dev/', '/System/', '/usr/lib/', '/private/var/db/timezone/', '/usr/share/']
BLOCK_EVENTS = ('subprocess.Popen', 'os.system', 'os.exec', 'os.posix_spawn', 'os.spawn', 'socket.connect',
                'socket.bind', 'socket.getaddrinfo', 'urllib.Request', 'os.remove', 'os.rename', 'os.rmdir',
                'shutil.rmtree', 'os.unlink', 'os.truncate', 'shutil.move', 'os.chmod')
AUDIT = []


def hook(event, args):
    if event in BLOCK_EVENTS:
        AUDIT.append((event, str(args)[:200]))
        raise RuntimeError('FENCE: %s refused' % event)
    if event == 'open':
        path = args[0]
        if isinstance(path, int) or path is None:
            return
        p = os.path.abspath(os.fsdecode(path))
        low = p.lower()
        if any(f in low for f in FORBIDDEN_NAMES):
            AUDIT.append(('open-forbidden', p))
            raise RuntimeError('FENCE: forbidden name %s' % p)
        mode = args[1] if len(args) > 1 and isinstance(args[1], str) else 'r'
        flags = args[2] if len(args) > 2 and isinstance(args[2], int) else 0
        writing = any(c in mode for c in 'wax+') or (flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT))
        if writing:
            if not p.startswith(HERE + '/'):
                AUDIT.append(('write-outside', p))
                raise RuntimeError('FENCE: write outside lens folder %s' % p)
            return
        if not any(p.startswith(a) or p == a for a in READ_OK):
            AUDIT.append(('read-outside', p))
            raise RuntimeError('FENCE: read outside allowlist %s' % p)


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    sys.addaudithook(hook)
    for p, h in PINS.items():
        got = sha(p)
        if got != h:
            raise SystemExit('PIN MISMATCH %s %s' % (p, got))
    mod = load(MOD, 'v003g_mod')
    C = load(HERE + '/tools/classify_r2b.py', 'classify_r2b')
    S = load(HERE + '/tools/synth_r2b.py', 'synth_r2b')
    slots = json.load(open(SLOTS))
    radii = {r['query_id']: float(r['Rad_text']) for r in slots['query_block']['rows']}
    assert [r['Rad_unit'] for r in slots['query_block']['rows']] == ['kpc'] * 43
    obs_rule = slots['projection_pins']['entries']['observation_rule']['entry']

    # ---------------- TSR recompute (C-1.4) ----------------
    nodes = json.load(open(NODES)); n1 = json.load(open(N1)); cmpd = json.load(open(CMP))
    rk = nodes['orders']['4']['radii_kpc']; rm = nodes['orders']['4']['radii_m']; kpc = nodes['kpc_m']
    rings = n1['ring_radii_kpc']
    failing = [r['ordinal'] for r in cmpd['failing_TRUNCATION_SHAPE_rings']]
    tsr = {'bitwise_rings_eq_radii_kpc': sum(a == b for a, b in zip(rings, rk)),
           'bitwise_rings_eq_radii_m_over_kpc_m': sum(a == b / kpc for a, b in zip(rings, rm)),
           'n_rings': len(rings), 'failing_ordinals': failing,
           'observation_rule_contains_piecewise_linear': 'piecewise-linear interpolation of mean' in obs_rule,
           'observation_rule_contains_azimuthal': 'azimuthal' in obs_rule,
           'observation_rule_text': obs_rule}
    flagged_rule_i, flagged_adapter, flagged_metre = [], [], []
    for q in C.IDS:
        R = radii[q]
        for k in failing:
            lo = rings[k - 1] if k - 1 >= 0 else None
            hi = rings[k + 1] if k + 1 < len(rings) else None
            if lo is not None and hi is not None and lo < R < hi:
                flagged_rule_i.append(q)
            if lo is not None and hi is not None and lo * kpc < R * kpc < hi * kpc:
                flagged_metre.append(q)
        # adapter logic (owned_column_mean_streaming_observation_v002: bisect_left, weights on j-1, j)
        if rk[0] <= R <= rk[-1]:
            j = bisect.bisect_left(rk, R)
            inds = [j] if (j < len(rk) and rk[j] == R) else [j - 1, j]
            if any(k in inds for k in failing):
                flagged_adapter.append(q)
    tsr.update(flagged_rule_i=flagged_rule_i, flagged_metre_form=flagged_metre, flagged_adapter_dependence=flagged_adapter,
               r14=rings[14], r15=rings[15], r16=rings[16], r17=rings[17],
               Q24=radii['NGC3198-Q24'], Q25=radii['NGC3198-Q25'], Q26=radii['NGC3198-Q26'],
               weight_on_ring15_for_Q25=(radii['NGC3198-Q25'] - rings[14]) / (rings[15] - rings[14]),
               edge_rule_defined_for_ordinal_0=False, edge_rule_defined_for_ordinal_99=False)

    # ---------------- synthetic cases ----------------
    IDS = C.IDS
    O = IDS[35:]; T = IDS[24:35]; I = IDS[:24]
    base_inv = {'NGC3198-Q01': ('INV', 'QUERY_INSIDE_INNERMOST_NODE'), 'NGC3198-Q02': ('INV', 'QUERY_INSIDE_INNERMOST_NODE')}

    def rm_of(over):
        d = dict(base_inv)
        d.update(over)
        return d

    def prim(ref_over, others=None, null_ids=(), ref_eval=True, other_eval=True):
        b = S.bound_rows(null_ids)
        ref = S.member_from_r('M000', 10, rm_of(ref_over), b, role='centroid_nearest')
        oth = others if others is not None else [{}, {}, {}]
        lis = [3, 7, 12]
        ms = [ref] + [S.member_from_r('M%03d' % (i + 1), lis[i], rm_of(o), b, evaluated=other_eval) for i, o in enumerate(oth)]
        return ms, b

    def twin_set(ref_over, others=None, b=None, ref_valid=True):
        oth = others if others is not None else [{}, {}, {}]
        lis = [3, 7, 12]
        t = S.member_from_r('M000', 10, rm_of(ref_over), b, role='centroid_nearest', forward_valid=ref_valid)
        return [t] + [S.member_from_r('M%03d' % (i + 1), lis[i], rm_of(o), b) for i, o in enumerate(oth)]

    cases = []
    ctx_base = {'radii': radii, 'tsr_flagged': ('NGC3198-Q25',), 'late_gate_rows': set(), 'c3_record_pinned': False}

    def run(name, desc, ref_over, others=None, null_ids=(), ctx_over=None, freeze_status='FREEZE_COMPLETE',
            other_eval=True, ok_twin=None, s0_twin=None, s0_twin_valid=True, ok_valid=True, mutate=None, sens_valid=False):
        ms, b = prim(ref_over, others, null_ids, other_eval=other_eval)
        ok = twin_set(ok_twin, None, b, ref_valid=ok_valid) if ok_twin is not None else None
        s0 = twin_set(s0_twin, None, b, ref_valid=s0_twin_valid) if s0_twin is not None else None
        score, mism = S.build_score(mod, ms, 'M000', b, freeze_status=freeze_status,
                                    incomplete_reasons=(['BUDGET_EXHAUSTED: synthetic'] if freeze_status != 'FREEZE_COMPLETE' else []),
                                    original_k=ok, stage0=s0, sens_valid=sens_valid)
        if mutate:
            mutate(score)
        ctx = dict(ctx_base)
        if ctx_over:
            ctx.update(ctx_over)
        res = C.classify(score, ctx)
        slim = {'name': name, 'desc': desc, 'replica_mismatches': mism, 'status': res['status']}
        if res['status'] != 'CLASSIFIED':
            slim['stop_reasons'] = res['stop_reasons']
        else:
            pr = res['primary']
            slim.update(patterns=pr['patterns_holding'], e3=res['e3'],
                        outer_failure=[pr['outer_failure_def_miss_dominated'], pr['outer_failure_def_P1_P2_P11']],
                        zones={Z: {k: pr['zones'][Z][k] for k in ('N_v', 'H', 'M', 'N', 'I', 'm', 'S', 'miss_dominated', 'hit_dominated')}
                               for Z in C.ZONES},
                        delta_out=pr['delta_out'], growing=pr['growing'],
                        readings=[(x['row'], x['reading'], x['part1'], x['part2']) for x in pr['readings']],
                        flagged_rows=[(r['id'], r['tier'], r['counts_as']) for r in pr['rows'] if r['tsr_flag']],
                        near_rows=[r['id'] for r in pr['rows'] if r['near'] is True],
                        near_na_rows=[r['id'] for r in pr['rows'] if r['near'] == 'NOT_AVAILABLE'],
                        sensitivity_col=sorted(set(r.get('sensitivity_overlap') for r in pr['rows'])),
                        alternatives={k: {kk: vv for kk, vv in v.items() if kk in ('status', 'reading', 'twin')} for k, v in res['alternatives'].items()},
                        dt_s0g=res['dt_s0g'], p8_report=res['p8_report'], provisional=res['provisional'],
                        onset=[pr['onset_radius_all_MISS'], pr['onset_radius_excluding_LATE']])
            for k in list(slim['alternatives']):
                tw = slim['alternatives'][k].get('twin')
                if tw:
                    slim['alternatives'][k]['twin'] = {'patterns_holding': tw['patterns_holding'], 'outer_failure_defs': tw['outer_failure_defs'],
                                                       'OUTER': {kk: tw['zones']['OUTER'][kk] for kk in ('N_v', 'H', 'M', 'm', 'S')}}
        slim['events'] = res['events']
        cases.append(slim)
        return res

    # C01 baseline all hit
    run('C01_all_hit', 'all valid rows HIT (r=0); Q01/Q02 built-in INVALID', {})
    # C02 OUTER deficit, growing
    run('C02_outer_deficit_growing', 'OUTER 8 misses r from -1.5 (near) to -5 (far); TRANSITION m=0',
        {q: -1.5 - 0.5 * i for i, q in enumerate(O)})
    # C03 OUTER excess
    run('C03_outer_excess', 'OUTER 8 misses r=+3', {q: 3.0 for q in O})
    # C04 OUTER mixed (CENTERED)
    run('C04_outer_mixed', 'OUTER misses of both signs, m=0', {q: (3.0 if i % 2 else -3.0) for i, q in enumerate(O)})
    # C05 tie at N_v/2 in OUTER
    run('C05_outer_tie', 'OUTER 4 HIT (r=0) and 4 MISS (r=-3): M=N_v/2', {q: (-3.0 if i < 4 else 0.0) for i, q in enumerate(O)})
    # C06 N_v(OUTER)=0 all INVALID by the built-in cut
    run('C06_outer_all_invalid', 'every OUTER row QUERY_BEYOND_OUTER_GAS_CUT', {q: ('INV', 'QUERY_BEYOND_OUTER_GAS_CUT') for q in O})
    # C07 INNER all invalid via non-late gate + TRANSITION misses
    run('C07_inner_all_invalid_gate', 'INNER Q03-Q24 INVALID through a pre-step-5 gate (not LATE); TRANSITION all misses r=-2',
        dict([(q, ('INV', 'SYNTH_GATE_EARLY')) for q in I[2:]] + [(q, -2.0) for q in T]))
    # C08 INNER mixed (P12)
    run('C08_inner_mixed', 'INNER 12 misses of both signs and 10 hits, m within 1', dict([(q, (3.0 if i % 2 else -3.0) if i < 12 else 0.0) for i, q in enumerate(I[2:])]))
    # C09 TRANSITION only failure (P13), Q25 flagged MISS -> P10
    run('C09_transition_only', 'TRANSITION 11 misses r=+2.5 (Q25 included)', {q: 2.5 for q in T})
    # C10 TRANSITION failure with Q25 a HIT -> P13 without P10
    run('C10_transition_Q25_hit', 'TRANSITION 10 misses, Q25 HIT', dict([(q, 2.5) for q in T[1:]] + [('NGC3198-Q25', 0.2)]))
    # C11 scattered (P7) with OUTER valid -> R-MF against question
    run('C11_scattered', 'one MISS per zone, no zone miss-dominated', {I[5]: 3.0, T[3]: -3.0, O[2]: 2.0})
    # C12 global offset deficit (P6)
    run('C12_global_deficit', 'every valid row r=-2', dict((q, -2.0) for q in IDS[2:]))
    # C13 P5 with OUTER EXCESS (as P1 question)
    run('C13_P5_outer_excess', 'INNER hit-dominated, TRANSITION miss-dominated, OUTER excess misses',
        dict([(q, 2.0) for q in T] + [(q, 3.0) for q in O]))
    # C14 null ratio rows: all OUTER valid rows null ratio -> S UNDEFINED
    run('C14_outer_all_null_ratio', 'OUTER rows VALID with NON_FINITE_SIGMA_RATIO (sigma 5e-324)',
        dict((q, ('NULL',)) for q in O), null_ids=tuple(O))
    # C15 LATE gate on all OUTER rows (were deficits) -> S UNDEFINED
    late_all = set((q, 'SYNTH_GATE_LATE') for q in O)
    run('C15_outer_all_late', 'all 8 OUTER rows INVALID through a LATE root gate',
        dict((q, ('INV', 'SYNTH_GATE_LATE')) for q in O), ctx_over={'late_gate_rows': late_all})
    # C16 partial LATE gating flips P1 -> P11
    run('C16a_before_late', 'OUTER 4 misses r=-3 and 4 hits r=0 (no gate)', {q: (-3.0 if i < 4 else 0.0) for i, q in enumerate(O)})
    run('C16b_after_late', 'same, with the 4 miss rows LATE-gated (their predictions become null)',
        {q: (('INV', 'SYNTH_GATE_LATE') if i < 4 else 0.0) for i, q in enumerate(O)},
        ctx_over={'late_gate_rows': set((q, 'SYNTH_GATE_LATE') for q in O[:4])})
    # C17 partial LATE gating flips GROWING
    run('C17a_growing', 'OUTER deficit, near -1.5..-2.5 far -4..-5', {q: [-1.5, -2.0, -2.5, -3.0, -4.0, -4.5, -5.0, -5.5][i] for i, q in enumerate(O)})
    run('C17b_growing_after_late', 'same, far rows Q41-Q43 LATE-gated',
        {q: ([-1.5, -2.0, -2.5, -3.0, -4.0] + [('INV', 'SYNTH_GATE_LATE')] * 3)[i] for i, q in enumerate(O)},
        ctx_over={'late_gate_rows': set((q, 'SYNTH_GATE_LATE') for q in O[5:])})
    # C18 Q25 LATE-gated -> P10 on a prediction-less row
    run('C18_Q25_late', 'Q25 INVALID through a LATE gate; rest HIT', {'NGC3198-Q25': ('INV', 'SYNTH_GATE_LATE')},
        ctx_over={'late_gate_rows': {('NGC3198-Q25', 'SYNTH_GATE_LATE')}})
    # C19 Q25 INVALID (non-late gate) -> listed, no P10
    run('C19_Q25_invalid_early_gate', 'Q25 INVALID through a pre-step-5 gate', {'NGC3198-Q25': ('INV', 'SYNTH_GATE_EARLY')})
    # C20 gate present, LATE status unknown
    run('C20_gate_late_unknown', 'Q40 gate-INVALID, late status not supplied', {'NGC3198-Q40': ('INV', 'SYNTH_GATE_X')},
        ctx_over={'late_gate_rows': None})
    # C21 NEAR straddle (no member within error)
    run('C21_near_straddle', 'Q40 ref r=-2.0; others -2.3, +2.0, +2.4 -> envelope overlaps, no member within error',
        {'NGC3198-Q40': -2.0}, others=[{'NGC3198-Q40': -2.3}, {'NGC3198-Q40': 2.0}, {'NGC3198-Q40': 2.4}])
    # C22 FREEZE_INCOMPLETE: one PRIMARY member unevaluated -> envelope invalid, NEAR NOT_AVAILABLE
    run('C22_freeze_incomplete', 'one PRIMARY member unevaluated; OUTER deficits', {q: -3.0 for q in O},
        others=[{}, {}, {}], other_eval=False, freeze_status='FREEZE_INCOMPLETE')
    # C23 pre-score stop: envelope label prefix differs
    def bad_label(s):
        s['pointwise_envelope']['label'] = 'SOMETHING_ELSE'
    run('C23_stop_label', 'envelope label prefix differs', {}, mutate=bad_label)
    # C24 pre-score stop: missing field
    def drop_field(s):
        del next(m for m in s['members'] if m['member_id'] == 'M000')['rows'][30]['sigma_ratio']
    run('C24_stop_missing_field', 'a named field missing', {}, mutate=drop_field)
    # C25 pre-score stop: reference row UNEVALUATED_OR_REFUSED
    def unevaluated_row(s):
        r = next(m for m in s['members'] if m['member_id'] == 'M000')['rows'][20]
        r['status'] = 'UNEVALUATED_OR_REFUSED'
    run('C25_stop_unevaluated_row', 'reference row status UNEVALUATED_OR_REFUSED', {}, mutate=unevaluated_row)
    # C26 pre-score stop: order
    def swap(s):
        rows = next(m for m in s['members'] if m['member_id'] == 'M000')['rows']
        rows[3], rows[4] = rows[4], rows[3]
    run('C26_stop_order', 'reference ids out of order', {}, mutate=swap)
    # DT-S0G boundaries (OUTER rows of the PRIMARY reference: 8 misses r=-3)
    o_def = {q: -3.0 for q in O}
    run('C27_s0g_consistent', 'twin gains one hit (Q36 r=-0.5), others r=-6 (M-9 consequence)', o_def,
        s0_twin=dict([(O[0], -0.5)] + [(q, -6.0) for q in O[1:]]))
    run('C28_s0g_against_tie', 'twin identical to the reference: H_S=H_P, A_S=A_P', o_def, s0_twin=dict(o_def))
    run('C29_s0g_not_decided', 'twin shrinks every residual to r=-1.5, no hit', o_def, s0_twin={q: -1.5 for q in O})
    run('C30_s0g_fewer_hits_smaller', 'ref 2 hits; twin 1 hit and smaller median |r|',
        {q: [0.5, 0.5, -3, -3, -3, -3, -3, -3][i] for i, q in enumerate(O)},
        s0_twin={q: [0.5, -1.2, -1.2, -1.2, -1.2, -1.2, -1.2, -1.2][i] for i, q in enumerate(O)})
    run('C31_s0g_no_qualifying_rows', 'twin: every OUTER row INVALID (its own cut)', o_def,
        s0_twin={q: ('INV', 'QUERY_BEYOND_OUTER_GAS_CUT') for q in O})
    run('C32_s0g_twin_invalid', 'STAGE0 twin member_valid false', o_def, s0_twin={}, s0_twin_valid=False)
    run('C33_s0g_not_evaluated', 'STAGE0 NOT_EVALUATED_BEFORE_FREEZE', o_def)
    # ORIGINAL_K valid twin with P8; TWIN_INVALID
    run('C34_P8_origk_valid', 'P8 with an ORIGINAL_K valid twin', {}, ok_twin={q: -3.0 for q in O})
    run('C35_P8_origk_invalid', 'P8 with ORIGINAL_K TWIN_INVALID', {}, ok_twin={}, ok_valid=False)
    # P8 + P0 + P9 coexistence
    run('C36_P8_P0_P9', 'all OUTER INVALID (cut), rest HIT', {q: ('INV', 'QUERY_BEYOND_OUTER_GAS_CUT') for q in O})
    # one valid OUTER row that misses (M-3 consequence) and Delta_out undefined
    run('C37_single_outer_valid_miss', '7 OUTER rows cut, Q36 valid MISS r=-1.2',
        dict([(O[0], -1.2)] + [(q, ('INV', 'QUERY_BEYOND_OUTER_GAS_CUT')) for q in O[1:]]))
    # boundary values: |r|=1 exactly HIT; r=0 sign 0; m exactly -1
    run('C38_boundaries', 'OUTER rows r=-1 exactly (HIT) and r=-1.0000001 (MISS); m(OUTER) = -1 (CENTERED)',
        {q: (-1.0 if i < 4 else -1.0000001) for i, q in enumerate(O)})
    # sensitivity rows valid (column yes/no)
    run('C39_sensitivity_valid', 'sensitivity rows valid (not the production refusal case)', {q: -3.0 for q in O}, sens_valid=True)
    # INNER miss-dominated with all INNER valid rows LATE-gated -> INNER coverage hole
    run('C40_inner_all_late', 'all INNER valid rows LATE-gated',
        dict((q, ('INV', 'SYNTH_GATE_LATE')) for q in I[2:]), ctx_over={'late_gate_rows': set((q, 'SYNTH_GATE_LATE') for q in I[2:])})

    # V2 additions: LATE gate creates P1 from P11; LATE gate removes P1g; STAGE0 with LATE rows; FREEZE_INCOMPLETE P8
    run('C16c_mixed_before_late', 'OUTER 4 misses r=+3 and 4 misses r=-3: CENTERED, P11', {q: (3.0 if i < 4 else -3.0) for i, q in enumerate(O)})
    run('C16d_mixed_after_late', 'same, the 4 excess rows LATE-gated: the remaining defined r are deficits',
        {q: (('INV', 'SYNTH_GATE_LATE') if i < 4 else -3.0) for i, q in enumerate(O)},
        ctx_over={'late_gate_rows': set((q, 'SYNTH_GATE_LATE') for q in O[:4])})
    run('C17c_growing2', 'OUTER r=[-3,-3,-3,-3,-2,-2,-6,-6]: GROWING', {q: [-3, -3, -3, -3, -2, -2, -6, -6][i] for i, q in enumerate(O)})
    run('C17d_growing2_after_late', 'same, Q42 and Q43 LATE-gated: Delta_out turns positive',
        {q: ([-3, -3, -3, -3, -2, -2] + [('INV', 'SYNTH_GATE_LATE')] * 2)[i] for i, q in enumerate(O)},
        ctx_over={'late_gate_rows': set((q, 'SYNTH_GATE_LATE') for q in O[6:])})
    run('C41_s0g_with_primary_late_rows', 'PRIMARY Q36-Q39 LATE-gated, Q40-Q43 r=-3; twin all r=-0.5 on Q36-Q39 and -3 elsewhere',
        {q: (('INV', 'SYNTH_GATE_LATE') if i < 4 else -3.0) for i, q in enumerate(O)},
        ctx_over={'late_gate_rows': set((q, 'SYNTH_GATE_LATE') for q in O[:4])},
        s0_twin={q: (-0.5 if i < 4 else -3.0) for i, q in enumerate(O)})
    run('C42_incomplete_P8', 'FREEZE_INCOMPLETE and every valid row HIT', {}, others=[{}, {}, {}], other_eval=False,
        freeze_status='FREEZE_INCOMPLETE')

    out = {'schema': 'LENS_R2B_CASES_V002', 'module_sha256': PINS[MOD], 'slots_sha256': PINS[SLOTS],
           'n_cases': len(cases), 'total_replica_mismatches': sum(c['replica_mismatches'] for c in cases),
           'audit_events': AUDIT, 'cases': cases}
    with open(HERE + '/CASES_R2B_V2.json', 'x') as f:
        json.dump(out, f, indent=1, sort_keys=True, default=str)
    with open(HERE + '/TSR_RECOMPUTE_R2B_V2.json', 'x') as f:
        json.dump(tsr, f, indent=1, sort_keys=True)
    print('cases', len(cases), 'replica mismatches', out['total_replica_mismatches'], 'audit', AUDIT)
    print('TSR flagged rule(i)', flagged_rule_i, 'metre', flagged_metre, 'adapter', flagged_adapter,
          'bitwise', tsr['bitwise_rings_eq_radii_kpc'], tsr['bitwise_rings_eq_radii_m_over_kpc_m'])
    for c in cases:
        ev = [(e['kind'], e['clause']) for e in c['events'] if e['kind'] != 'NOTE']
        print(c['name'], c['status'], c.get('patterns'), c.get('e3'), c.get('dt_s0g') if not isinstance(c.get('dt_s0g'), dict) else c['dt_s0g'].get('outcome'), ev)


if __name__ == '__main__':
    main()

# Claude4 (dispatch 0526), revision r2: assemble KMAX_TAIL_PREREG_V007_FINAL_DRAFT (UNSEALED) from R1 (c691cab6) and the binding root
# amendments: V004 A46 (RA1-RA13, frozen 487d4449) and V005 A47-A57 (open; cited by name, PENDING freeze sha). Successor of c4v001 (r1 output kept).
# Every clause carries the ruling(s) it comes from. Every pin is computed from bytes here; a missing file is refused.
# Writes: KMAX_TAIL_PREREG_V007_FINAL_DRAFT.json/.md, CLAUSE_SOURCE_MAP.md, SEAL_CHECKLIST.md, ROOT_ITEMS.md (no overwrite).
# Usage: TS=$(date -u +%Y-%m-%dT%H:%M:%SZ) python3 -I -B make_v007_final_draft_c4v001.py
import hashlib, json, os
from pathlib import Path

EX = Path('/Users/bgm/Research/UNT_EXCHANGE'); CA = EX / 'claude_artifacts'
C2 = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2')
OUT = CA / 'v007_final_prereg_c4' / 'r2'
R1 = CA / 'tail_scheme_design_c2/v002/r1/KMAX_TAIL_PREREG_V007_DRAFT_R1.json'
R1_SHA = 'c691cab6dd9752a7bd98025cf7357a5c729b3fef90a78a6277195c5520671e33'
V004 = C2 / 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V004_ADDENDUM.md'
V004_SHA = '487d44498205e563c752e692b48bbb7288055591c72cfdcf5a75d849fef3d82b'
V005 = C2 / 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def pin(p, prefix=None):
    p = Path(p)
    if not p.is_file():
        raise SystemExit('missing ' + str(p))
    h = sha(p)
    if prefix and not h.startswith(prefix):
        raise SystemExit('pin prefix %s != %s for %s' % (prefix, h[:8], p))
    return {'path': str(p), 'sha256': h}


def cl(text, *sources):
    return {'text': text, 'sources': list(sources)}


def main():
    ts = os.environ['TS']
    if sha(R1) != R1_SHA or sha(V004) != V004_SHA:
        raise SystemExit('R1 or V004 pin')
    r1 = json.loads(R1.read_text())
    v005_observed = sha(V005)
    v005_text = V005.read_text()
    for a in ('## A47', '## A48', '## A49', '## A50', '## A51', '## A52', '## A53', '## A54', '## A55', '## A56', '## A57'):
        if a not in v005_text:
            raise SystemExit('V005 addendum lacks ' + a)
    disp = {n: pin(EX / 'FROM_CODEX' / f) for n, f in (
        ('0526', '0526_2026-10-18_claude4_reprioritize_v007_final_prereg_assembly.md'),
        ('0530', '0530_2026-10-18_codex_all_A55_P128_r5_and_B0_ruling.md'),
        ('0512', '0512_2026-10-18_codex1_ruling_N3_and_N_outcomes.md'),
        ('0518', '0518_2026-10-18_codex3_ruling_invalid_as_miss_freeze_contract.md'),
        ('0532', '0532_2026-10-18_codex1_codex3_A57_gas_Ms128.md'))}
    R3 = pin(CA / 'tail_scheme_design_c2/v002/r2/KMAX_TAIL_PREREG_V007_DRAFT_R3.json', '92092f24')
    R2 = pin(CA / 'tail_scheme_design_c2/v002/r2/KMAX_TAIL_PREREG_V007_DRAFT_R2.json', 'a0f855db')
    T = CA / 'tail_scheme_impl_c2'
    bind = {
        'driver': cl('galaxy_m0_forward_c2v010 **r5** (A55.2: r4 with only the TAIL_MEMORY_CAP_BYTES module successor and the pin-only re-pin cascade; '
                     '"the sealed driver is the one the gates ran on", A55.3). sha PENDING_FROM_BYTES at seal (tail_scheme_impl_c2/driver_r5/, not yet on disk at assembly). '
                     'Base = v010 r4 below (0526 lists r4; see ROOT_ITEMS RI-01).', 'A55.2', 'A55.3', '0530 item 2', '0526'),
        'driver_r4_base': pin(T / 'driver_r4/galaxy_m0_forward_c2v010.py', 'b9ae92d5'),
        'driver_r4_build_record': pin(T / 'driver_r4/BUILD_DRIVER_C2V010_R4.json', 'c081d3b2'),
        'driver_r4_hashes': pin(T / 'driver_r4/HASHES.txt'),
        'successors': cl('Every route-A and route-B successor, worker, facade, controller, binding and the reference successor exactly as pinned by the sealed '
                         "driver's build record (r5, PENDING; the r4 set is pinned by BUILD_DRIVER_C2V010_R4 above). Reference successor under r4: "
                         'driver_r4/route_b/…_uvt_c2v003.py (4778fc73).', 'A52', 'A55.2', '0526'),
        'reference_successor_r4': pin(T / 'driver_r4/route_b/ddo_homotopy_reference_root_worker_v001_gal_c2v005_uvt_c2v003.py', '4778fc73'),
        'tail_module': {'lapse': pin(T / 'module/owned_uv_tail_lapse_v001.py', 'c28d4209'), 'roster': pin(T / 'module/uv_tail_source_roster_c2v001.py', '4366e3d6'),
                        'jn': pin(T / 'module/posix_libm_bessel_jn_provider_c2v001.py', 'd6c55b55'),
                        'successor_note': 'A55.2: a module successor changing only TAIL_MEMORY_CAP_BYTES (to 8 GiB), AST-identical otherwise, replaces lapse c28d4209 in r5 (PENDING).'},
        'ro1_c2v002': {n: pin(CA / 'ro1_readout_c2' / n) for n in (
            'ddo_composite_stable_cached_binding_v002_uvtail_ro1_c2v002.py', 'ddo_composite_stable_cached_root_worker_v002_uvtail_ro1_c2v002.py',
            'ddo_composite_stable_cached_root_worker_v002_parallel_uvtail_ro1_c2v002.py', 'ngc_composite_full_coupled_binding_v002_uvtail_ro1_c2v002.py',
            'ngc43_composite_coupled_root_worker_v002_uvtail_ro1_c2v002.py', 'ngc43_composite_coupled_root_worker_v002_parallel_uvtail_ro1_c2v002.py')},
        'nodes_v001': {'lib': pin(T / 'nodes_v001/lib/owned_uv_tail_nodes_v001.py', 'c8a04fb5'),
                       'ro1_worker_serial': pin(T / 'nodes_v001/route_a/ddo_composite_stable_cached_root_worker_v002_uvtail_ro1_nodes_c2v001.py', 'dbb331db'),
                       'ro1_worker_parallel': pin(T / 'nodes_v001/route_a/ddo_composite_stable_cached_root_worker_v002_parallel_uvtail_ro1_nodes_c2v001.py', '5a4c7d41'),
                       'scope': 'nodes RO1 workers and binding 86af6198 on the custody list only for cases whose registered source_rule is nodes_v001 (A53 NEW-13)'},
        'spec_registry': cl('The P128 spec set (0530 item 1; A55.1), PENDING: the r4-era registry SPECS_V007_C2V002_R1 (9bfe9674, pinned below) predates P = 128 and is '
                            'not the sealed registry. The sealed registry is retargeted to r5 (0530 item 2).', 'A55.1', '0530', '0526'),
        'spec_registry_r4_era': pin(T / 'driver_r4/specs/SPECS_V007_C2V002_R1.json', '9bfe9674'),
        'certificates_v002': {'index': pin(T / 'certificates_v002/CERTIFICATES_V002.json'), 'hashes': pin(T / 'certificates_v002/HASHES.txt'),
                              'eps': pin(T / 'certificates_v002/gates/EPS_CERT_V006.json', '598c8fa3'), 'lo': pin(T / 'certificates_v002/gates/LO_CERT_V002.json', 'fd4fa52b'),
                              'lo_ngc': pin(T / 'certificates_v002/gates/LO_NGC_CERT_V002.json', '33bc2190'), 'i1t_ngc': pin(T / 'certificates_v002/gates/I1T_NGC_T120L_V001.json', '3ae7981a'),
                              'gq_kb128_ms64': pin(T / 'certificates_v002/gates/GQ_CERT_V003_KB128.json', '24984fd5'),
                              'gq_full_ms64_FAIL': pin(T / 'certificates_v002/gates/GQ_CERT_V002.json', 'fac4aca7'),
                              'gq_kb256_ms128_not_registered': pin(T / 'certificates_v002/gates/GQ_CERT_V003_KB256_MS128.json', 'b3a5390f'),
                              'note': 'EPS (EPS_CERT_V006) does not depend on the gas rule and stays. GQ and LO for the DDO cases move to certificates_v003 (GQ and LO at '
                                      'M_s 128; PENDING, A57.1): GQ over the full DDO reach on all nodes; LO recomputed with the M_s 128 source (the M_s 64 transfer is UNTESTED and '
                                      'not relied on). The v002 GQ/LO records above are evidence only.'},
        'certificates_v003': cl('tail_scheme_impl_c2/certificates_v003/ (GQ + LO at M_s 128): PENDING_FROM_BYTES at seal.', 'A57.1', '0532'),
        'identity_comparator': cl('c2v004 (gates_v004, PENDING_FROM_BYTES): closes the c2v003 holes (extra files fail; .npy compared; request argv compared; '
                                  'script-custody tokens limited to the declared driver map; strict JSON type and signed zero). The r5 identity comparisons use c2v004.',
                                  'A57.3', 'A52.2'),
        'identity_comparator_c2v003_predecessor': pin(T / 'gates_v003/run_identity_compare_c2v003.py', '8f14f466'),
        'c5h_spec': pin(CA / 'c5h_hull_c2/CALL_KMAX_C5H_A2F10_HULL_N8_M32_C2V009.json', '60b46130'),
        'review_v009_orig': pin(CA / 'kmax_prereg_v005_c2/extension_c5c6/check/REVIEW_V009_PREP_V009_V001_ORIG_3bce7c02.json', '3bce7c02'),
        'identity_specs': {'Z2': pin(T / 'driver/specs/CALL_UVT_Z2_A2F10_EMPTY_DOMAIN_N8_C2V010.json', '2d5e79d0'),
                           'Z2_OFF_RO1': pin(T / 'driver_r4/specs/CALL_UVT_Z2_OFF_RO1_A2F10_N8_C2V010R4.json', '894e5b3a'),
                           'B0prime_RERUN': pin(CA / 'ngc_route_impl_c2/binding/specs/CALL_REPRO_PINNED_ADMIT_PREFIX_C2V005.json', '4ac5527a')},
        'qinf_evaluator': pin(CA / 'qinf_dependence_c2/tools/qinf_eval_v001.py', 'f58de0dc'),
        'v006_r1_sealed': pin(CA / 'kmax_prereg_v005_c2/extension_c5c6/v006_r1/prereg/KMAX_MATRIX_PREREG_V006_R1.json', '807fc5bf'),
        'compare': cl('kmax_tail_compare_c2v007 at the round sealed by root: PENDING r5-final sha, filled at seal (r5 78ac63b7 is FAIL as a seal candidate per A54 '
                      'continued (CX2-R5-B1); S9 goes into the next round).', '0526', 'A54 S9'),
        'compare_r5_current': pin(CA / 'v007_compare_c2/r5/kmax_tail_compare_c2v007_r5.py', '78ac63b7'),
        'gate_b3_final': pin(CA / 'gate_b3_c4/GATE_B3_C4_V002.md', '465cb3c3'),
    }
    fixed = {
        'anchor': cl(r1['fixed_across_all_cases']['anchor'], 'R1'),
        'grids': cl('G2/G3/G4 as V005; G5 (C5H, 108 nodes/axis, kmax 5) for the T2/T2I extension G5\\G4; G6 as V006 R1 (120 nodes/axis, prep v009) for C6T.',
                    'R1', 'A46 RA1', 'A46 RA3', 'A46 RA11'),
        'tau_km_s': cl(json.dumps(r1['fixed_across_all_cases']['tau_km_s']), 'R1'),
        'statistic': cl(r1['fixed_across_all_cases']['statistic'], 'R1'),
        'validity_gates': cl('V005 per_case_validity_gates V1-V6. V3 against the registered V007 case block, including the uv_tail config sha and the declared key-equivalence '
                             'map (any key v010 adds must appear in the map with its absent/default value shown to reproduce v009 behaviour, B0 identity; otherwise V3 fails). '
                             'The case block asserts each case\'s registered tail content: source_rule, grid (kept K), outer shape and K_out/K_big, lapse_only, enabled, '
                             'lambda_scale and the uv_tail config sha; a swapped tail, wrong grid, wrong K_out or wrong K_big is refused (S8). Every pass row-set and the final '
                             'row-set carry exactly the 12 registered row IDs (no duplicate, no unknown ID), checked before any dictionary is built; a violation is a '
                             'RECORD_DEFECT and the case reads INCOMPLETE (S9). A pass recorded without rows is a record gap: pass_rows equal passes in number with consecutive '
                             'indices, otherwise E is unavailable and the case reads INCOMPLETE if no R-PAIR resolves it (B4).',
                             'R1', 'A48 AMB-13', 'A54 S8', 'A54 S9', 'A54 B4'),
        'picard_validity_gate_km_s': cl(str(r1['fixed_across_all_cases']['picard_validity_gate_km_s']), 'R1'),
        'brackets': cl('Every V007 tail-corrected case uses C5H\'s bracket block byte for byte: fs_absolute_overrides [1.5125e8, 3.17625e8] on all 72 columns, le_first '
                       '[0.4, 0.9], le_next [0.8, 1.1], rfs [0.8, 1.2], rfs override 71: [0.8, 1.01]. Cases: C2T, C3T, C4T, C6T, S4T, C4T-D5, C4T-C5c, C4T-KLO, '
                       'C4T-KHI, C4T-A (RA4 list with the A56 T3 labels in place of C4T-K16/C4T-K64; RI-05). No W1 widening clause. A miss under the hull makes the case '
                       'invalid, reading BRACKET_HULL_MISS; next step: its own registration. The identity gates (Z2, Z2_OFF_RO1, B0prime_RERUN) keep their reference '
                       'specs\' brackets, which bitwise identity requires.', 'A46 RA4', 'A48 AMB-16', 'A55.1', 'A56 (labels)'),
        'route_a': cl('Route A is computed in every T-run (PICARD R-PAIR members instead admit their base run\'s route A) with column_workers 8 (parallel), uniformly across T-cases; route_a.max_iterations = 32 for every T-case, matching '
                      'C5H and C4T-D5; each case\'s accepted iteration is reported. Every V007 tail-corrected case uses the RO1 workers from its first launch (RO1 '
                      'changes checkpoint identity); C5H (v009-EXT, no RO1) is the declared exception admitted under A48 AMB-20 / A50. Admission of a route A or prefix '
                      'with a different uv_tail digest is refused (UVT_ADMISSION_MISMATCH). The I4 condition (V8c-F1 fix; tail-ON serial == parallel bitwise) was met '
                      'by the final implementation check (A51), so no column_workers exemption is declared.',
                      'R1', 'A47 I4', 'A47 I5', 'A49.4', 'A51'),
        'production_tail': {
            'P': cl('Production K_big P = 128 /kpc (cylinder). Production C4T and every tail-corrected case not otherwise specified use cylinder K_big = 128 '
                    '(C4T-C5c: cube K_out 5, RA2; T3 cases C4T-KLO K_big 64 and C4T-KHI K_big 256; S4T: its registered sphere tail; RI-05).', 'A55.1', 'A54 (generic T3)', 'A46 RA2', 'A56 (labels)'),
            'source_rule': cl(r1['fixed_across_all_cases']['production_tail']['source_rule'] + ' (C4T-D5: nodes_v001 on G5\\G4, RA1)', 'R1', 'A46 RA1'),
            'gas': cl('interp lagrange3_s_gl4 with **M_s = 128 for every DDO tail-corrected case** (registered change, made openly before any T result: at M_s 64 the GQ '
                      'gate fails at the reach P = 128 needs); NGC keeps M_s 96 (its GQ passes to 32).', 'R1', 'A46 RA7', 'A57.1', '0532'),
            'quadrature': cl('order 8; w_perp_max 0.05 /kpc; w_z_max 0.02 /kpc; phases 1.415 / 1.34 rad; corner_zone_rule as R1 (IA1). Node counts (N_perp per K from '
                             'the module grid; N_z_plus) and the eval/source extents at K_big 128 and 256 are those of the registered P128 uv_tail configs whose shas the case '
                             'block carries (S8). R1\'s N_z_plus 12800 and extents were set for K_big 32 (RI-03).', 'R1', 'A54 S8', 'A55.1'),
            'asymptote': cl(r1['fixed_across_all_cases']['production_tail']['asymptote'], 'R1'),
            'lapse_only': cl('true (non-lapse components bounded by LO / LO_NGC)', 'R1'),
            'jet_order': cl(json.dumps(r1['fixed_across_all_cases']['production_tail']['jet_order']), 'R1'),
            'stars': cl(json.dumps(r1['fixed_across_all_cases']['production_tail']['stars']), 'R1'),
            'memory_guard': cl('TAIL_MEMORY_CAP_BYTES is a resource guard, not numerics (design K15); r5 raises it to 8 GiB through a module successor that is AST-identical '
                               'otherwise.', 'A55.2', '0513'),
        },
        'kept_region_rule': cl(r1['fixed_across_all_cases']['kept_region_rule'], 'R1'),
    }
    pair = {
        'noise_allowance': cl('Norm in which contraction is measured: ||d_k||_tau = max_i |d_k,i|/tau_i. q = min(0.9, the larger of the last two observed ratios '
                              '||d_k||_tau/||d_k-1||_tau); with only one ratio, that ratio. Norm-level bound E_i^norm = tau_i * ||d_last||_tau * q/(1-q); with exactly one '
                              'increment, E_i = tau_i * ||d_last||_tau. Per-row bound for rows whose last two increments have the same sign (d_last,i * d_prev,i > 0): '
                              '|d_last,i| * q_i/(1-q_i), q_i = min(0.9, |d_last,i|/|d_prev,i|) (S7). Alternating bound for rows whose last two increments change sign: the tail of a '
                              'geometric series with ratio -q_i, |d_last,i| * q_i/(1+q_i), q_i = |d_last,i|/|d_prev,i| (A56 N1). E_i = max(E_i^norm, same-sign bound, '
                              'alternating bound). E is UNAVAILABLE for the run (its tests undecidable; to R-PAIR) when: no increment is observed; a tau-norm ratio >= 1 on '
                              'either of the last two ratios (NEW-7); any row has q_i >= 1, same-sign or alternating (A56 N1); or a pass-row gap / row-ID defect exists (B4, S9). '
                              '(The 0.9 cap on same-sign q_i: RI-18.) E_i(pair) = E_i(a) + E_i(b). The geometric bound assumes the observed ratio is the '
                              'map\'s contraction factor: DECLARED, checked against each run\'s own increments.',
                              'A51 F2', 'A54 S7', 'A56 N1', 'A53 NEW-7', 'A48 AMB-05', 'A54 B4', 'A54 S9'),
        'decidable_iff': cl(r1['pairing_and_decidability_rule']['decidable_iff'], 'R1'),
        'decidability_scope': cl('Decidability applies to T1_H, T2 and T3 (pass texts say "decidable"); not to T1, T2c, T1_S or RB_FP.', 'A48 AMB-06'),
        'if_not_decidable_R_PAIR': cl(
            'R-PAIR once, branch chosen on the worst undecidable row (largest (E + E^A)/tau): if E is unavailable, branch PICARD; else if E^A_i(pair) > E_i(pair) on that '
            'row, branch ROUTE_A, otherwise PICARD. ROUTE_A members recompute route A with route_a.seed_source_rtol_factor 0.1 (absent = 1.0, byte-identical; B0 covers '
            'absence); their route-A identity must differ from the base\'s (NEW-16); the C5H ROUTE_A member carries ro1_workers true. PICARD members admit their base '
            'run\'s route A (route_a.column_workers = 1 is a registered PICARD leaf, byte-equal between members), with picard.passes 12 and speed_change_bound_km_s '
            '0.0025 (byte-equal between members); V6 requires route_a_outcome.result_sha256 equal to the base\'s; a T-case PICARD member\'s RO1 record equals its '
            'base\'s canonically and its worker-kind check uses the admitted attempt\'s worker (R3-4); the C5H PICARD member carries no ro1_workers and reads '
            'ro1 armed false, fired false. Each member is validated against its partner and against its base, with only the registered R-PAIR leaves allowed to '
            'differ; a member\'s V2 uses its registered speed bound. C5H members run under v010 tail OFF with the RO1 workers where their branch computes route A, '
            'admitted through B0 identity, with worker/binding pins on the declared custody list. A manifest naming R-PAIR members for a test whose R-PAIR was not '
            'triggered is refused at load, before any test is read (NEW-17). PICARD members inherit their base run\'s flag and a cleared base clears them; ROUTE_A '
            'members carry their own flags. Still not decidable -> UNDECIDABLE_AT_ITERATION_FLOOR (reported; the test neither passes nor fails).',
            'R1', 'A48 AMB-07', 'A48 AMB-14', 'A50 B1', 'A50 N4', 'A50 item 1', 'A50 item 10', 'A50 item 11', 'A52.3', 'A53 (R-PAIR, NEW-16, NEW-17)', 'A53 R3-4'),
        'thresholds_unchanged': cl(r1['pairing_and_decidability_rule']['thresholds_unchanged'], 'R1', 'A51'),
        'T2_numerics': cl('C4T-D5 numerics are byte-equal (canonical JSON) to the numerics of the C5H spec 60b46130 after removing composite_grid_spec and uv_tail, and '
                          'apart from the keys of the declared key-equivalence map in the seal record. The C5H run\'s normalized numerics must equal the spec\'s, '
                          'normalized by its dry run. No column_workers difference is declared (A47 I4; both register route_a.column_workers 8).',
                          'A46 RA1', 'A47 I4', 'A48 AMB-13', 'A50 S1', 'A47 I2'),
        'route_a_noise': cl(r1['pairing_and_decidability_rule']['route_a_noise'] + '. C5H\'s E^A comes from a required EA replay record computed after the seal from '
                            'C5H\'s route-A outputs by this formula; the EA record carries the row radii so the row order is verified (or v010 copies probe_R_m into the '
                            'tail record); the EA record covers C4T, C6T, C4T-D5, C4T-KLO, C4T-KHI and C5H.', 'R1', 'A48 AMB-08', 'A48 AMB-22', 'A50 item 13'),
        'diagnostics_recorded': cl('Route-A accepted iteration and Picard pass count of each member and case: recorded, not compared.', 'R1', 'A48 AMB-21', 'A47 I5'),
        'T1_status': cl('T1 is not subject to the decidability rule: its Dhat pairs follow V005 exactly as sealed; RA6 adds the per-row clause.', 'R1', 'A48 AMB-06', 'A46 RA6'),
    }
    g = r1['gates_before_any_T_result']
    gates = {
        'B0': cl(g['B0'] + '. Counting rule: B0 counts only comparisons whose expected reports are non-empty and whose planning completes; equal early failures are '
                 'listed separately as no evidence (B0-EMPTY). The six historical positive R3 specs (C2R3, C3R3, C4R3, S4R3, RR3, Y3R3) refuse identically in both '
                 'drivers (seed/admission custody) and are listed as no evidence, neither a blocker nor a pass; B0 coverage = the completed non-empty comparisons '
                 'plus separately labelled computed-plan derivatives. The successor B0 tool and a B0 record rerun are required before the seal. Under A55, B0 also '
                 'shows r5 plan-identical to r4 on every spec (with the B0-EMPTY rule). Each A52.3 C5H R-PAIR member\'s own spec sha is listed in spec_sets/EXT '
                 'with its projection to v009-EXT form and its declared differences as evidence.',
                 'R1', 'A54 (B0-EMPTY)', '0530 item 3', 'A55.2', 'A53 (r4 validity F1)'),
        'B0prime_DRY': cl(g['B0prime_DRY'], 'R1'),
        'B0prime_RERUN': cl(g['B0prime_RERUN'] + '. Its route A is admitted from a saved run, so RO1 cannot be armed: it requires ro1 armed false and fired false '
                            '(exempt from A50 item 12). Rerun on v010 r5.', 'R1', 'A52.1', 'A55.3'),
        'B0_FA': cl(g['B0_FA'], 'R1'),
        'B0_RO1': cl('(a) RO1 fires in no identity-gate run; if it fires, that identity gate fails (RO1_FIRED_IN_IDENTITY_RUN). (b) A replay on the C6 iteration-8 '
                     'checkpoint records ROUTE_A_READOUT_NO_CIRCULAR_BRANCH at query 03 and hands the checkpoint to route B. (c) Every other exception, and a refusal '
                     'before convergence, still fails the call. RO1 set = {NO_SUBLUMINAL_CIRCULAR_PRESSURE_BRANCH, DEGENERATE_RADIAL_EULER, NON_TIMELIKE_COLUMN}, '
                     'exact messages (incl. the full L205 string "DEGENERATE_RADIAL_EULER: zero exact denominator; no unique speed"), type(exc) is ValueError, only after '
                     'a converged solve. A case that requires RO1 requires route_a_outcome.ro1.armed true. RO1 firing in a T-run is recorded, not an invalidity; '
                     'route-A circular-trial rows are diagnostics only; route B decides.', 'A46 RA5', 'A49.1', 'A49.2', 'A50 (A49 in the compare)', 'A53 r4 validity F3'),
        'B0_N3': cl('In tail-OFF mode v010 constructs no TailBoundary; the final checker verifies statically that every TailBoundary construction is guarded by an '
                    'enabled uv_tail block; B0prime_RERUN and Z2_OFF_RO1 bitwise identity are the runtime check.', 'A46 RA8', 'A47 I6', 'A52.1'),
        'B1_Z2': cl('Z2 = spec 2d5e79d0 (A2F10 C2, v010 tail ON, cylinder K_big = K = 2, every stage domain empty), route A as registered in that spec '
                    '(route_a.column_workers 8), RO1 workers armed (ro1.armed true, fired false), against DDO154_A2F10_ROUTE_A_PARALLEL_N8_C2V008_DECIDING_RUN_V001 '
                    '(883b37a0; COMPARE_DECIDING_II e1d3c072): all route-A blobs/records/arrays, every stage npz, rows and speeds equal; only the declared custody list '
                    'differs. The base -> successor token map is derived from the sealed driver\'s pin tables only (UVT stage table and STAGE_SUCCESSOR base map), '
                    'never from the observed diff (the token fix: 16 exact additions for 8 driver-declared successor relations, PASS by Codex3, A57); Z2 is rerun on v010 r5 '
                    'with independent verification and compared with c2v004. Precondition L as R1.',
                    'R1', 'A50 item 12', 'A52.1', 'A55.3', 'A54 pre-seal status (Z2 ruling)', 'A57', 'A57.3'),
        'Z2_OFF_RO1': cl('Mandatory (no longer a fallback): spec 894e5b3a = the 883b37a0 reference spec under v010 tail OFF with the RO1 workers armed; comparator c2v003 '
                         'gate (c2v004 for the r5 runs, A57.3) with tail-OFF semantics: admits only the declared enabled:false records, fails any other uv_tail record, requires ro1 armed true and '
                         'fired false. Rerun on v010 r5.', 'A47 I6', 'A52.1', 'A52.2', 'A55.3', 'A57.3'),
        'B2': cl(g['B2'], 'R1'),
        'B3': cl(g['B3'], 'R1'),
        'EPS': cl('Numerical sup searches are estimates, not proofs; envelope consumers read the full-envelope fields (A57.4). q(k) sampled via QINF evaluator f58de0dc (cache 7b9816ae cross-check), 13+13 directions x 64/decade per unit shell of [K, K_big]; refined 26+26 x '
                  '128/decade; eps_s(refined) <= 1.1 eps_s(base) else refine; 2 refinement failures -> EPS_UNCERTIFIED. Coverage: DDO from 2 to at least sqrt2 * 2P '
                  '(= 362.04 at P = 128; the module\'s unit shells end at ceil(sqrt2 * K_big), so the DDO record covers [2, 363]); NGC [2, 46] (ceil(sqrt2 * 32) for the '
                  'N3 case K_big 32; RI-17). The record carries envelope_bound {rule A52_5_SUP_OVER_DIRECTION_TIMES_CARDINAL_TORUS, coverage_max_inverse_kpc} with '
                  'coverage >= sqrt2 * 2P (A52.5 as raised by A54). Until such a record is slotted, per-shell values above 15 /kpc are lower bounds and SRB_ROT is not '
                  'read. An estimate, not a proven sup.', 'R1', 'A52.5', 'A53 NEW-19', 'A54 (coverage)', 'A55.4', 'A50 item 9', 'A57.4', 'certificates_v002 (coverage note)'),
        'LO': cl(g['LO'] + '; shells extended so that coverage reaches >= sqrt2 * 2P (= 362.04 at P = 128), every extended shell <= 0.005 tau (shell partition: '
                 'RI-06). The DDO LO certificate is computed with the M_s 128 source (A57.1).', 'R1', 'A54 (coverage)', 'A55.4', 'A57.1'),
        'GQ': cl('For every gas roster used, the gas transform at M_s and at 2M_s agrees to <= 1e-12 * P0 at the 4096 I1T seeded nodes over [K, K_big]; certified per '
                 'source geometry over the union of all T-case tail node domains: DDO (C2T-C4T, C4T-KLO, C4T-KHI, incl. the corner zones) and NGC T120L [2, 32]. A '
                 'replay. With production M_s 128 (A57.1) the DDO certificate is computed at M_s 128 against 256 over the full DDO reach (to sqrt2 * 2P = 362.04, the module '
                 'node reach at K_big 256) on all nodes, not only sampled ones. A failure or a coverage shortfall reads UV_TAIL_GAS_QUADRATURE_UNCERTIFIED, which is '
                 'NUMERICS_UNCERTIFIED.', 'A46 RA7', 'A48 AMB-12', 'A50 item 8', 'A55.1', 'A57.1'),
        'DOUBLING': cl(g['DOUBLING'], 'R1'),
        'I1T': cl(g['I1T'] + '; the I1T record covers every T-case.', 'R1', 'A48 AMB-11'),
        'T2I': cl('Before T2 is read: nodes_v001 transform replicas applied to the C5H rosters equal the C5H stored packet sources on G5\\G4 to <= 1e-12 (route-A updated '
                  'per iteration; offset new_body_fourier_J; feedback gas_source_feedback). A T2I failure reads IMPLEMENTATION_DEFECT (T2I).',
                  'A46 RA3', 'A48 AMB-10', 'R1'),
        'SRB_ROT': cl(g['SRB_ROT'] + '. Computed on C4T: when C4T is flagged, a pass carries the flag and a failure is undecidable. Not read until the EPS envelope record '
                      '(A52.5) is slotted.', 'R1', 'A50 item 7', 'A52.5'),
        'RB_FP': cl(g['RB_FP'] + '. E is the Picard allowance only. If C4T\'s E is unavailable (NEW-7, A56 N1) or C4T has a B4 gap, RB_FP reads E from C4T\'s Picard R-PAIR member '
                    '(the 12-pass rerun admitting C4T\'s route A); C4T-A gets the same Picard path; both are on the resolvable list; an unresolved one, or RB_FP with '
                    'undefined kappa, reads INCOMPLETE. Shell labels are read by index and never emitted verbatim in blinded modes (S6).',
                    'R1', 'A48 AMB-09', 'A50 item 9', 'A56 N2', 'A54 S6'),
        'MT_monitor': cl(g['MT_monitor'] + '. An MT verdict FAIL for a run is the TAIL_SOURCE_UNDERCONVERGED flag on that run; a defective MT record reads NO_RUN; an MT '
                         'record, when supplied, covers every T-case.', 'R1', 'A50 S2', 'A48 AMB-25'),
        'result_assembly_identity': cl('Gated ONLY by B0prime_RERUN, B1 (Z2) and Z2_OFF_RO1, on DDO154; NGC result assembly is UNTESTED (deciding test: the first NGC '
                                       'route-B result under the NGC driver successor compared with a v009 parent).', 'R1', 'A47 I6', 'A52.1', '0517'),
        'LO_NGC': cl('LO_NGC is the readout-coupled share, the quantity the N-tests read (lnN only, metric v002 L76); the field-level indicator is carried as an auxiliary '
                     'field; the record carries an honest i1t field. NGC I1-T of stars + H2 against the T120L fixed source must pass before any NGC N-test is read. '
                     'LO_NGC is reported only in this compare; the NGC N-tests get their own small compare before any N-test is read; N-tests are not read as passed '
                     'before LO_NGC passes.', 'A52.4', 'A48 AMB-23', 'R1 (L8)'),
        'HARMONIC': cl('Reported, not deciding: a0/a4/a8 of dlnN/dR at route-A query 03 (R = 1.48 kpc), at the four diagonal azimuths, for C4T, C4T-D5 and C6T, and for '
                       'C4R3, C5H and C6 direct (C6 from its checkpoint replay).', 'A46 RA10'),
        'RECEIPTS': cl('A receipt is required for every run case; a missing receipt reads INCOMPLETE.', 'A48 AMB-26'),
        'record_verdicts': cl('A gate record whose verdict contradicts its own data is a RECORD_DEFECT (NO_RUN group), not a decided failure; a defective or malformed gate '
                              'record reads NO_RUN with next step "fix the record or gate and re-review", never a physics reading.', 'A54 S5', 'A48 AMB-02'),
    }
    t = r1['tests']
    tests = {
        'T1': cl('Pass iff cases C2T, C3T, C4T are valid AND V005 criterion.shape_pass literally (Dhat_T(3,4) <= 1 AND Dhat_T(3,4) <= 0.5 * Dhat_T(2,3)) AND RA6: for '
                 'every row i, d23_i * d34_i >= 0 and |d34_i| <= 1/2 |d23_i|, where d23_i = v_i(C3T) - v_i(C2T), d34_i = v_i(C4T) - v_i(C3T); if d23_i = 0 the row passes '
                 'only if d34_i = 0. TINY (DECLARED; applies to the RA6 clause only): a row is TINY iff |d23_i| <= tau_i/8 and |d34_i| <= tau_i/8; TINY rows are exempt '
                 'from the per-row clause and stay in Dhat. No floor clause; FLOOR_LIKE pre-named (D14). Known blind spot (G5): a growing row whose increments both '
                 'stay <= tau/8 is exempt; the backstop is T1_H.', 'R1', 'A46 RA6', 'A47 I2', 'A47 (G5)'),
        'T1_H': cl('C6T against C4T: per row |v_i(C6T) - v_i(C4T)|/tau_i <= 1/2 every row, decidable; no TINY exemption. C6T is consistent through RO1.',
                   'R1', 'A47 (G5 backstop)', 'A47 I7'),
        'T1_S': cl(json.dumps(t['T1_S'], ensure_ascii=False), 'R1'),
        'T2': cl('C4T-D5 against C5H (spec 60b46130): per row |dv_i|/tau_i <= 1/4, decidable, T2I passed. C4T-D5 = K = 4 cube with the nodes_v001 tail on G5\\G4 (lapse-only; '
                 'the LO certificate on shell (4,5] makes a T2 difference read as tail-implementation error).', 'A46 RA1', 'A52.6', 'A46 RA11'),
        'T2c': cl('C4T-C5c (continuum_v001, E1, outer cube K_out = 5) against C4T-D5: per row |dv_i|/tau_i <= 1/2 (PASS/FAIL); a failure reads SOURCE_RULE_MATERIAL.',
                  'A46 RA2', 'A46 RA11'),
        'T3': cl('With production K_big P = 128: T3 = {C4T-KLO (K_big 64 = P/2), C4T-KHI (K_big 256 = 2P)}, each against C4T at P per row <= tau/4, decidable. '
                 'Producers emit the labels C4T-KLO and C4T-KHI; A55\'s "C4T-K64/K256" is descriptive only. The compare reads P, P/2 and 2P from the registered '
                 'case block and refuses any other values; the R1 labels C4T-K16/C4T-K64 are retired.', 'A54 (generic T3)', 'A55.1', 'A56 (labels)'),
        'RB_FP_run': cl(json.dumps(t['RB_FP_run'], ensure_ascii=False), 'R1'),
        'SR_K': cl(json.dumps(t['SR_K'], ensure_ascii=False), 'R1'),
        'D_m4': cl(json.dumps(t['D_m4'], ensure_ascii=False), 'R1'),
    }
    decision = {
        'ADOPT_TAIL_cube_K4_C4T': cl('All of B0, B0prime_DRY, B0prime_RERUN, B0_FA, B0_RO1, B0_N3, B1 (Z2), Z2_OFF_RO1, B2, B3 (incl. cylinder-O), EPS, LO, GQ, LO_NGC (for '
                                     'NGC readings), DOUBLING, I1T, T2I, SRB_ROT, RB_FP pass; T1, T1_H, T1_S, T2, T2c, T3 pass; a receipt for every case; no flag unruled; every '
                                     'step resolved (otherwise INCOMPLETE with the pending steps named).', 'R1', 'A46 RA5/RA7/RA8', 'A47 I6', 'A48 AMB-17', 'A48 AMB-26'),
        'carried_uncertainty_u_i': cl(r1['decision_rule']['carried_uncertainty_u_i'], 'R1'),
    }
    r1o = {o.split(':')[0].split(' ')[0]: o for o in r1['outcomes_first_applicable']}
    dec = []
    for name in ('IMPLEMENTATION_DEFECT', 'SOURCE_RULE_MATERIAL', 'KBIG_NOT_CONVERGED', 'BOUND_INSUFFICIENT', 'FLOOR_LIKE', 'NOT_UV_RESIDUAL',
                 'SOURCE_REPRESENTATION_K_DEPENDENT', 'HIGHER_K_DISAGREEMENT', 'SHAPE_DISAGREEMENT'):
        txt = r1o[name]
        if name == 'IMPLEMENTATION_DEFECT':
            txt += ' (also a T2I failure: IMPLEMENTATION_DEFECT (T2I), A48 AMB-10)'
        elif name == 'KBIG_NOT_CONVERGED':
            old = 'production K_big 64 under T3prime (32/64/128), EPS and LO to 128'
            assert old in txt
            txt = txt.replace(old, 'T3prime: production 2P with {P, 4P} (= 256 with {128, 512} at P = 128); EPS/LO coverage >= sqrt2 * 4P (A56 N4; R1\'s "' + old + '" is superseded)')
        elif name == 'FLOOR_LIKE':
            old = 'T1 fails only by the contraction clause'
            assert old in txt
            txt = txt.replace(old, 'T1 fails only by a contraction clause (max-based or per-row, RA6)')
        dec.append(txt)
    decided_text = ('Read in this order: ' + ' | '.join(dec) + '. A decided failure is read when its own condition is fully decided even if another step is '
                    'unresolved; the pending steps are listed.')
    outcomes = [
        {'position': '1a', 'outcome': 'NO_RUN', 'text': 'Any identity or implementation gate fails (B0, B0prime_DRY, B0prime_RERUN, B0_FA, B0_RO1, B0_N3, B1/Z2, Z2_OFF_RO1, B2, '
         'B3; a B2/B3 failure is IMPLEMENTATION_DEFECT of the gate), or a gate record is defective, malformed or contradicts its data (RECORD_DEFECT). Next: fix and '
         're-review. Every reading names every missing or invalid case and gate.', 'sources': ['R1', 'A48 AMB-01', 'A48 AMB-02', 'A54 S4', 'A54 S5']},
        {'position': '1b', 'outcome': 'INCOMPLETE', 'text': 'Placed directly after NO_RUN. Any registered V007 case (T-runs, C5H, identity-gate runs) invalid or missing, '
         'including BRACKET_HULL_MISS, a missing receipt, a pass-row gap or row-ID defect, RB_FP with undefined kappa -> name each case and gate with its next step; no '
         'T-test is read. Subtypes: CASES_OR_RECORDS (tests unread) and UNRESOLVED (tests read: ADOPT_TAIL or FLAG_PENDING_RULING with a pending step; a NOT_UV/SRKD '
         'split that turns on a flag).', 'sources': ['A47 I1', 'A50 item 4', 'A50 item 5', 'A48 AMB-17', 'A48 AMB-26', 'A54 B4', 'A54 S9', 'A50 item 9']},
        {'position': '1c', 'outcome': 'NUMERICS_UNCERTIFIED / NON_LAPSE_TAIL_MATERIAL', 'text': 'Same position. NUMERICS_UNCERTIFIED: EPS uncertified, DOUBLING fails, GQ '
         'fails or a GQ/EPS coverage shortfall. NON_LAPSE_TAIL_MATERIAL: LO fails (LO_NGC for NGC readings). Next: named successor. No T-test is read.',
         'sources': ['R1', 'A48 AMB-03', 'A48 AMB-18', 'A50 item 8', 'A46 RA7']},
        {'position': '2', 'outcome': 'decided failure outcomes, in R1 order', 'text': decided_text,
         'sources': ['R1', 'A50 (final order)', 'A48 AMB-10', 'A48 AMB-17', 'A46 RA6', 'A55.1', 'A56 N4']},
        {'position': '3', 'outcome': 'UNDECIDABLE_ROUTE_A_TAIL', 'text': 'Only if no decided failure outcome applies and some test with a TAIL_SOURCE_UNDERCONVERGED run '
         'failed (flags are evaluated per test: a flagged test that passes, passes with the flag carried; one that fails is undecidable and cannot trigger '
         'IMPLEMENTATION_DEFECT, NOT_UV_RESIDUAL, SOURCE_REPRESENTATION_K_DEPENDENT or FLOOR_LIKE). Next: rerun that case with seed source_rtol/10.',
         'sources': ['R1', 'A48 AMB-04', 'A50 (final order)']},
        {'position': '4', 'outcome': 'UNDECIDABLE_AT_ITERATION_FLOOR', 'text': 'A paired test still undecidable after R-PAIR: neither pass nor fail; no adoption. Both '
         'undecidable readings are listed when both apply.', 'sources': ['R1', 'A50 (final order)']},
        {'position': '5', 'outcome': 'FLAG_PENDING_RULING', 'text': 'Every gate and test passes but a flag stays unruled (SOURCE_QUADRATURE_MATERIAL, or '
         'TAIL_SOURCE_UNDERCONVERGED on an adoption run); no adoption; needs every step resolved; root rules on the flag (a flag ruling is a root addendum entry naming the flag, '
         'run and evidence, registered before any adoption reads the flagged test).', 'sources': ['R1', 'A48 AMB-04', 'A48 AMB-17', 'A48 AMB-19']},
        {'position': '6', 'outcome': 'ADOPT_TAIL', 'text': 'The decision rule holds and every step is resolved.', 'sources': ['R1', 'A48 AMB-17']},
    ]
    reading_rules = [
        cl('Any reading made while a step at an earlier position is pending is marked PROVISIONAL, with the pending steps listed. A decided T3, T1-split or SHAPE reading '
           'stands while T2/T2I is pending, marked PROVISIONAL.', 'A50 (final order)', 'A50 item 3'),
        cl('"No T-test is read" applies to NO_RUN, INCOMPLETE and NUMERICS_UNCERTIFIED/NON_LAPSE_TAIL_MATERIAL; T values may be reported descriptively, labelled '
           '"not read".', 'A48 AMB-18'),
        cl('Governing principle: no ruling may make adoption easier than the text; where the text is silent the stricter-on-adoption reading is chosen.', 'A48', 'A53'),
        cl('A V1-V6 failure other than BRACKET_HULL_MISS -> named defect, fix and rerun that case under V007 with thresholds unchanged.', 'A48 AMB-16'),
    ]
    RESOLVED_BY_A56 = {'RI-07': 'A56 N4: "T3prime: production 2P with {P, 4P}; EPS/LO coverage >= sqrt2 * 4P" (integrated)',
                       'RI-14': 'A56 N1: alternating bound |d_last,i| q_i/(1 + q_i) and any per-row q_i >= 1 makes E unavailable (integrated)',
                       'RI-15': 'A56 N2: RB_FP reads E from C4T\'s Picard R-PAIR member; C4T-A the same; both resolvable (integrated)',
                       'RI-16': 'A56 follow-up 2: producers emit C4T-KLO (K_big 64) and C4T-KHI (K_big 256) (integrated)',
                       'RI-02': 'A57.1: production gas M_s = 128 for every DDO tail-corrected case; GQ at M_s 128 over the full DDO reach on all nodes and LO recomputed '
                                'at M_s 128 required before the seal (integrated; certificates_v003 PENDING)',
                       'RI-04': 'A57.1: GQ over the full DDO reach (K_big up to 256/362) on all nodes; the draft takes the stricter edge sqrt2 * 2P = 362.04 (integrated)',
                       'RI-08': 'A57.2: PICARD member successor specs per A53 with B0 evidence (gates_v004) (integrated; specs PENDING)'}
    n = r1['ngc3198_N_tests']
    ngc = dict(n)
    ngc['tests'] = dict(n['tests'])
    ngc['tests']['N3'] = 'K_big 8 and 32 against 16, at every ring and azimuth: |Delta S| <= theta/4 and |Delta dL| <= theta/4, S = max_phi lnN0 - min_phi lnN0; "S/theta" is a reporting unit only (0512; A54 lanes)'
    ngc['outcomes'] = 'N_NO_RUN (a record is defective or contradicts its data; name it), N_INCOMPLETE (a record missing, NGC I1-T not passed, or LO_NGC absent; name each), N_FAIL_<test>, N_PASS; N_PASS is only an input to NGC route A/B (0512; A54)'
    ngc['LO_NGC'] = 'required before N-test readings (R1 L8; A52.4: readout-coupled share; NGC I1-T of stars + H2 against the T120L fixed source passes first)'
    ngc['own_compare'] = 'the N-tests get their own small compare before any N-test is read (A48 AMB-23); NGC tail route support is the driver successor v011 (0517), plan-identical to the sealed DDO driver'
    ngc['sources'] = ['R1', '0512', 'A54 (lanes)', 'A52.4', 'A48 AMB-23', '0517']
    run_list = {
        'DDO_gates': cl('Z2 (2d5e79d0; rerun on r5 with driver-derived tokens), Z2_OFF_RO1 (894e5b3a; rerun on r5), B0prime_RERUN (4ac5527a; rerun on r5).',
                        'A52.1', 'A55.3', 'A47 I6'),
        'DDO_tests': cl('C2T, C3T, C4T, C6T, S4T, C4T-D5, C4T-C5c, C4T-KLO (K_big 64), C4T-KHI (K_big 256), C4T-A (P128 specs with gas M_s 128, re-registered and '
                        'dry-run again; registry PENDING).', 'A46 RA11', 'A55.1', '0530 item 1', 'A56 (labels)', 'A57.1'),
        'external': cl('C5H (spec 60b46130; driver 999331af; REVIEW_V009 original 3bce7c02; admitted on the three A50 grounds: REVIEW_V009 PASS for driver 999331af and '
                       'spec 09ff5a96, a byte diff of 60b46130 against 09ff5a96 limited to the label and fs_absolute_overrides, and the clean dry run). Read before the '
                       'seal only as validity/admissibility booleans and reason codes, no row value printed or written.', 'A46 RA11', 'A48 AMB-20', 'A50 (AMB-20 restated)',
                       'A53 (REVIEW_V009)', 'A47 I3'),
        'contingent': cl('R-PAIR members (<= 4 pairs), with specs registered before any T result (A52.3); the PICARD member specs are successors per A53, with B0 '
                         'evidence (gates_v004, PENDING): admit the base route A, column_workers 1, V6 result_sha equality, an RO1 record equal to the base\'s, and for '
                         'the C5H PICARD member no ro1_workers.', 'R1', 'A52.3', 'A53', 'A57.2', 'compare r5 NEW-20'),
        'replays': cl('B2, B3, EPS, LO, GQ, SR_K, shell_split, DOUBLING, T2I, B0_RO1 replay (RA5 b), EA replay record (AMB-08/22), MT record.', 'R1', 'A46 RA11', 'A48 AMB-08'),
        'NGC': cl('NQ, N0, N1, N2, N3, N4, LO_NGC, NGC I1-T.', 'R1', 'A52.4'),
        'limits': cl('Resources are root\'s launch decision; the module memory cap is a resource guard (8 GiB in r5). R1\'s "<= 4 processes; serial route A; tail memory '
                     '<= 0.6 GiB/process" is superseded (route A parallel 8, A47 I4; guard A55.2).', 'A47 I4', 'A55.2', '0527'),
        'cpu_hours_estimate_UNTESTED': cl('R1\'s 77/93 CPU-hours were estimated for K_big 32 and are STALE at P = 128 (route-A tail build 15.1 min per call at K_big 128, '
                                          'Codex2 0418). No new estimate here (RI-09).', 'R1', 'A54 (Codex2 Lane A)', 'A55'),
    }
    seal_record = [
        cl('Before the seal the compare\'s gate and admissibility functions run on the real input records (the C5H receipt and result if present, the identity-gate '
           'records and the RO1 replay); their output goes into the seal record (E-SEAL1).', 'A46 RA13'),
        cl('Blinding: on C5H the gate functions run only as validity/admissibility booleans and reason codes, with no row value printed or written; the seal record '
           'states that no row value was shown. Record-controlled labels are redacted in blinded modes.', 'A47 I3', 'A54 S6'),
        cl('The compare pins at seal: V007_PREREG_SHA256 (this text once sealed), PIN_ADDENDUM_V005 (frozen V005 sha), PIN_REVIEW_V009 = the preserved original '
           '3bce7c02, PRODUCTION_K_BIG_A55 = 128.0; its custody pins (PIN_RO1_CUSTODY, PIN_RO1_NODES_CUSTODY, the drivers_allowed I4 set) move to r5\'s re-pinned '
           'shas read from r5\'s BUILD record, verified from bytes.', '0526', 'A53 (REVIEW_V009)', 'A55', 'A56 (A55 follow-ups 1, 3)', 'compare r5 NEW-26'),
        cl('Key-equivalence map: every key v010 adds that differs from v009 numerics appears with its absent/default value and B0 evidence.', 'A48 AMB-13'),
    ]
    scope_untested = list(r1['scope_untested']) + [
        'GQ for C4T-K256 at the registered M_s 64 (TESTED-NEGATIVE; RI-02)',
        'P128 cost and memory (route-A tail build 15.1 min/call at 128; K_big 256 build ~0.877 GiB)',
        'driver v010 r5 (not built at assembly)']
    root_items = [
        {'id': 'RI-01', 'kind': 'CONFLICT (input table)', 'clause': 'binding_inputs.driver', 'issue': '0526 lists driver v010 r4 b9ae92d5; A55.2-3 make the sealed driver '
         'v010 r5 ("the sealed driver is the one the gates ran on"), not yet on disk.', 'draft': 'binds r5 PENDING_FROM_BYTES with r4 b9ae92d5 and its build record as base.',
         'sources': ['0526', 'A55.2', 'A55.3', '0530']},
        {'id': 'RI-02', 'kind': 'CONFLICT (BLOCKING for adoption)', 'clause': 'GQ / production_tail.gas / T3', 'issue': 'A55.1 puts C4T-K256 (K_big 256) in T3. RA7 '
         'requires GQ at M_s vs 2M_s <= 1e-12 P0 over [K, K_big] for every roster used. certificates_v002 (TESTED): at the registered M_s 64, DDO_C4T [4,256] reaches '
         '5.9e-10 P0; the bound first exceeds 1e-12 at k_perp = 227.6 /kpc; certified only for K_big <= 128 (GQ_CERT_V003_KB128 24984fd5). M_s 128 passes to [K,362] '
         '(GQ_CERT_V003_KB256_MS128 b3a5390f, not registered). Compare r5 implements S8 strictly (NEW-26): every T-case uv_tail equals C4T\'s outside {outer, '
         'lambda_scale, source_rule}, so under that implementation M_s cannot differ for C4T-K256 alone. As written, C4T-K256 reads NUMERICS_UNCERTIFIED.', 'draft': 'keeps M_s 64 and records the conflict; options for root: '
         '(a) M_s 128 for every tail-corrected case (then GQ_CERT_V003_KB256_MS128 applies, plus an LO rebuild at M_s 128: B1 insensitive <= 1.1e-7, certificates_v002 '
         'sec 2); (b) add gas.M_s to the S8 exception set for C4T-K256 only; (c) another K_big pair.', 'sources': ['A46 RA7', 'A55.1', 'A54 S8', 'certificates_v002 sec 4-5']},
        {'id': 'RI-03', 'kind': 'UNDEFINED', 'clause': 'production_tail.quadrature', 'issue': 'R1\'s quadrature block (N_z_plus 12800, R/z eval and source extents) was set '
         'for K_big 32; no ruling restates it for K_big 128/256.', 'draft': 'defers node counts and extents to the registered P128 uv_tail configs (sha in each case block, S8).',
         'sources': ['R1', 'A55.1', 'A54 S8']},
        {'id': 'RI-04', 'kind': 'UNDEFINED', 'clause': 'GQ coverage edge', 'issue': 'Compare r5 NEW-23: GQ DDO edge max(64, 2P) vs sqrt2*2P (A54 names only EPS and LO). '
         'DERIVED (not TESTED): for a cylinder outer region the gas factor P_i depends on k_perp <= K_big, so 2P = 256 covers C4T-K256, and the kept-cube corner zone '
         'reaches only sqrt2*K; certificates_v002 profiles GQ per k_perp.', 'draft': 'states the RA7/AMB-12 rule; edge for root.', 'sources': ['A46 RA7', 'A48 AMB-12', 'A54', 'compare r5 NEW-23']},
        {'id': 'RI-05', 'kind': 'CONFLICT (wording)', 'clause': 'brackets; production_tail.P', 'issue': 'RA4 enumerates C4T-K16 and C4T-K64 (retired R1 labels); A55.1 says '
         '"every tail-corrected case uses cylinder K_big = 128", which cannot hold for C4T-C5c (cube K_out 5), the T3 cases (64, 256) or S4T (sphere tail).',
         'draft': 'RA4 list with C4T-K64/C4T-K256; K_big 128 for every case not otherwise specified.', 'sources': ['A46 RA4', 'A55.1', 'A46 RA2']},
        {'id': 'RI-06', 'kind': 'UNDEFINED', 'clause': 'LO shells above 64 /kpc', 'issue': 'R1 registers LO shells to (32,64]; A54/A55 require coverage >= sqrt2*2P '
         '(362.04) with every extended shell <= 0.005 tau (compare r5 NEW-22), but no ruling names the partition. LO_CERT_V002 (fd4fa52b) has 10 shells to 363 '
         '(per-shell max 3.95e-4 tau at (128,256]).', 'draft': 'requires coverage and per-shell bound; partition for root (proposal: LO_CERT_V002\'s 10 shells).',
         'sources': ['R1', 'A54', 'A55.4', 'compare r5 NEW-22']},
        {'id': 'RI-07', 'kind': 'UNDEFINED (stale)', 'clause': 'KBIG_NOT_CONVERGED next step', 'issue': 'R1: "production K_big 64 under T3prime (32/64/128), EPS and LO to '
         '128" is superseded by P = 128. Compare r5 NEW-24 derives "production K_big 2P under T3prime (P/2P/4P), EPS and LO to 4P" (= 256 under 128/256/512, EPS/LO to '
         'sqrt2*512); K_big 512 is outside every current certificate and the memory evidence (Codex1 0011 measured 256).', 'draft': '"next step: RI-07".',
         'sources': ['R1', 'A55', 'compare r5 NEW-24', 'FROM_CLAUDE3/0055 N4']},
        {'id': 'RI-08', 'kind': 'PENDING INPUT', 'clause': 'run_list.contingent', 'issue': 'Compare r5 NEW-20 (real bytes): the registered A52.3 PICARD member specs (C5H '
         '08d350ad: admit {}, column_workers 8, ro1_workers true; D5 template 84621760) predate A53 and read invalid; their B0 EXT entries lack projection_sha256 and '
         'declared_differences.', 'draft': 'requires re-registration to the A53 shape before the seal.', 'sources': ['A52.3', 'A53', 'compare r5 NEW-20']},
        {'id': 'RI-09', 'kind': 'STALE', 'clause': 'run_list.cpu_hours_estimate', 'issue': 'R1 estimate is for K_big 32.', 'draft': 'labelled STALE; root may supply.',
         'sources': ['R1', 'A55']},
        {'id': 'RI-10', 'kind': 'PENDING RULINGS', 'clause': 'compare-lane NEW items', 'issue': 'Compare r5 NEW-21 (S5 reading details), NEW-22 (coverage edges), '
         'NEW-25 (B4/NEW-17 scope), NEW-26 (S8 strictness), NEW-27 (label re-emission), NEW-28 (B0 record field), NEW-29 (carried notes) are lane proposals, not root '
         'text. Where a proposal is stricter and fills a gap it should become text before the seal.', 'draft': 'not integrated (only root rulings are integrated).',
         'sources': ['compare r5 COMPARE_V007_IMPL_R5.md']},
        {'id': 'RI-11', 'kind': 'CONFLICT (wording)', 'clause': 'B1 (Z2)', 'issue': 'R1 says "serial route A"; the registered Z2 spec 2d5e79d0 sets route_a.column_workers 8 '
         'and compares against the PARALLEL_N8 deciding run.', 'draft': 'route A as registered in the spec.', 'sources': ['R1', 'A47 I4', 'spec 2d5e79d0 bytes']},
        {'id': 'RI-12', 'kind': 'UNDEFINED', 'clause': 'B1 (Z2) token map', 'issue': 'The pre-seal Z2 ruling derives the token map "from the driver v010 r4 pin tables only"; '
         'A55.3 reruns Z2 on r5.', 'draft': 'derives the map from the sealed driver\'s (r5) pin tables; root confirm.', 'sources': ['A54 pre-seal status', 'A55.3']},
        {'id': 'RI-13', 'kind': 'NOTE (base choice)', 'clause': 'status', 'issue': 'Claude2\'s R2 (a0f855db) and R3 (92092f24) drafts integrate A40-A48; 0526 names R1 as '
         'the base, so this draft starts from R1 and integrates A46-A55 independently. R3 was not used as text.', 'draft': 'R3 cited for comparison only.',
         'sources': ['0526']},
        {'id': 'RI-14', 'kind': 'SHOULD_FIX for root (TESTED by Claude3)', 'clause': 'pairing_and_decidability_rule.noise_allowance', 'issue': 'A54 S7 sets the per-row '
         'bound to 0 for sign-changing rows. Claude3 0055 N1 built a world inside V2 on the tau = 0.05 row (alternating per-row ratio 0.95 under q = 0.083) that reads '
         'E/tau 0.023, decidable, and ADOPT_TAIL, while the row\'s own alternating tail is 0.12 tau; the same-sign history goes to R-PAIR. Proposal there: '
         'P_i = |d_last,i| q_i/(1 + q_i) for sign-changing rows.', 'draft': 'transcribes A54 S7 as ruled; the stricter alternative is for root.',
         'sources': ['A54 S7', 'FROM_CLAUDE3/0055 N1']},
        {'id': 'RI-15', 'kind': 'SHOULD_FIX for root', 'clause': 'gates_before_any_T_result.RB_FP', 'issue': 'Claude3 0055 N2: RB_FP has no R-PAIR path; NEW-7 or a B4 gap '
         'on C4T leaves the reading INCOMPLETE even after all three C4T R-PAIRs pass (6 runs that cannot resolve it). Root rules either a C4T rerun or RB_FP reading E '
         'from the C4T Picard member.', 'draft': 'RB_FP with unavailable E reads INCOMPLETE (A50 item 9 by analogy, fail-closed); next step for root.',
         'sources': ['A48 AMB-09', 'A50 item 9', 'FROM_CLAUDE3/0055 N2']},
        {'id': 'RI-17', 'kind': 'CONFLICT (coverage edge)', 'clause': 'gates_before_any_T_result.EPS (NGC)', 'issue': 'R1 states NGC EPS coverage [2, 32]; the NGC N3 '
         'case uses cylinder K_big 32, whose node |k| reaches sqrt2 * 32 = 45.25, and the module\'s unit shells end at ceil(sqrt2 * K_big) = 46 (certificates_v002 '
         'coverage note; its EPS record covers NGC [2, 46]).', 'draft': 'NGC [2, 46].', 'sources': ['R1', 'A52.5', 'certificates_v002']},
        {'id': 'RI-16', 'kind': 'CONFLICT (labels)', 'clause': 'tests.T3; run_list', 'issue': 'A55 names the T3 cases C4T-K64 and C4T-K256; compare r5 registers the generic '
         'labels C4T-KLO/C4T-KHI (case-block schema C2V003) and refuses retired labels (Claude3 0055 A55 follow-up 2).', 'draft': 'uses A55\'s names; root names the '
         'labels producers emit (e.g. KLO = C4T-K64, KHI = C4T-K256).', 'sources': ['A54 (generic T3)', 'A55.1', 'FROM_CLAUDE3/0055']},
    ]
    root_items.append({'id': 'RI-18', 'kind': 'LENIENCY (DERIVED, for root)', 'clause': 'pairing_and_decidability_rule.noise_allowance', 'issue': 'The q cap 0.9 '
        '(A51 norm level; S7 same-sign rows) understates a geometric tail for 0.9 < q < 1: the factor q/(1-q) is held at 9 while the series it bounds has factor '
        'up to 99 at q = 0.99. NEW-7 and A56 N1 make q >= 1 unavailable but leave the band 0.9 <= q < 1 capped, which is easier on adoption than the uncapped '
        'bound. Stricter readings: no cap below 1 (use q/(1-q)), or E unavailable for q >= 0.9.', 'draft': 'transcribes A51/S7 with the cap; stricter reading for root.',
        'sources': ['A51 F2', 'A54 S7', 'A53 NEW-7', 'A56 N1']})
    for r in root_items:
        if r['id'] in RESOLVED_BY_A56:
            r['status'] = 'RESOLVED: ' + RESOLVED_BY_A56[r['id']]
        else:
            r.setdefault('status', 'OPEN')
    root_items.sort(key=lambda r: (r['status'] != 'OPEN', r['id']))
    checklist = [
        ('Freeze the V005 addendum; pin its sha in this text (decision_pins) and in the compare (PIN_ADDENDUM_V005).', 'PENDING', '0526; A47-A57'),
        ('Root rulings on the OPEN root items (%s).' % ', '.join(r['id'] for r in root_items if r['status'] == 'OPEN'), 'PENDING', 'this draft'),
        ('Driver v010 r5 built; its gates: B0 plan identity r5 vs r4 on every spec (B0-EMPTY rule; 0530 no-evidence list), dry runs of every P = 128 spec at 0 blockers apart '
         'from certificates, an independent check.', 'PENDING', 'A55.2'),
        ('Successor B0 tool and B0 record rerun (B0-EMPTY).', 'PENDING', 'A54; 0530'),
        ('Identity runs on r5 compared by c2v004 (Z2 with the driver-derived tokens and independent verification, Z2_OFF_RO1, B0P_RERUN); record each comparison '
         '(earlier r4 results under c2v003: Z2_OFF_RO1 PASS_BITWISE_EQUAL, B0P_RERUN PASS_BITWISE_EQUAL, Z2 FAIL on stage custody only).', 'PENDING', 'A55.3; A57.3; A54 pre-seal status'),
        ('B3 final: PASS (Claude4 0060, GATE_B3_C4_V002 465cb3c3).', 'DONE', 'R1 B3; 0509'),
        ('Compare: the next round after r5 implements A54 S9 and A56 (N1 alternating bound and q_i >= 1 unavailable, N2 RB_FP Picard path, N4 KBIG text, '
         'labels, pins) and root\'s RI rulings; independent recheck; set V007_PREREG_SHA256, PIN_ADDENDUM_V005, PIN_REVIEW_V009 (3bce7c02), PRODUCTION_K_BIG_A55 = 128.0.',
         'PENDING', 'A54 S9; A56; 0526'),
        ('Run `--gates-only` and `--validity-only --case C5H` on the real records with the sealed compare; paste their output into the seal record; state that no row '
         'value was shown (E-SEAL1).', 'PENDING', 'A46 RA13; A47 I3; 0526'),
        ('Slot the A53-shape PICARD member successor specs with their B0 EXT evidence (gates_v004).', 'PENDING', 'A53; A57.2'),
        ('Slot certificates: EPS_CERT_V006 (598c8fa3; coverage 363; envelope; gas-independent), certificates_v003 GQ at M_s 128 over the full DDO reach on all '
         'nodes and LO recomputed with the M_s 128 source (A57.1), LO_NGC_CERT_V002 (33bc2190), I1T_NGC_T120L_V001 (3ae7981a).', 'PENDING (certificates_v003)', 'A52.4/5; A55.4; RA7; A57.1'),
        ('Register the P128 spec set with gas M_s 128 (case block schema C2V003; producers emit C4T-KLO (K_big 64) and C4T-KHI (K_big 256)), dry-run it again, and '
         'put its registry sha in binding_inputs.', 'PENDING', 'A55.1; A56; A57.1; 0530; 0532'),
        ('Key-equivalence map in the seal record.', 'PENDING', 'A48 AMB-13'),
        ('When driver_r5 lands: move the compare\'s custody pins (PIN_RO1_CUSTODY, PIN_RO1_NODES_CUSTODY, drivers_allowed I4 set) to r5\'s re-pinned shas read from '
         'r5\'s BUILD record, verified from bytes.', 'PENDING', 'A55.2; A56 (A55 follow-up 3)'),
    ]
    status = ('FINAL DRAFT r2 (NOT SEALED). Assembled by Claude4 (dispatch 0526) from R1 c691cab6, integrating V004 A46 RA1-RA13 (frozen 487d4449) and V005 A47-A57 (open; '
              'observed sha %s at assembly; PENDING freeze sha). Written before any V007 (tail-corrected) result exists; nothing was launched; C5H, UVT_* and targets '
              'were not read. Root seals; the open items are in root_items. Revision r2 integrates A56 and A57 (r1 = c4v001 output, kept).' % v005_observed)
    doc = {
        'schema': 'KMAX_TAIL_PREREG_V007_FINAL_DRAFT',
        'status': status,
        'assembly': {'by': 'Claude4 main session, single author (helpers unavailable until 2026-10-23T19:00Z)', 'utc': ts, 'dispatch': disp['0526'],
                     'rulings_read': {'V004_addendum_frozen': {'path': str(V004), 'sha256': V004_SHA}, 'V005_addendum_open_observed': {'path': str(V005), 'sha256': v005_observed},
                                      'dispatches': {k: v for k, v in disp.items() if k != '0526'}},
                     'base': {'path': str(R1), 'sha256': R1_SHA}, 'not_used_as_base_compared_only': {'R2': R2, 'R3': R3}},
        'design': r1['design'], 'extends': r1['extends'],
        'decision_pins_frozen': dict(r1['decision_pins_frozen'], V004_addendum={'path': str(V004), 'sha256': V004_SHA}),
        'decision_pins_pending_at_seal': {'V005_addendum': {'path': str(V005), 'sha256': 'PENDING_FREEZE_SHA', 'entries': 'A47-A55 (cited by name until frozen)'}},
        'cites_by_name': ['ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM: A47-A55 (open; pinned once frozen, PENDING_FREEZE_SHA)',
                          'KMAX_MATRIX_PREREG_V006_R1, sealed 807fc5bf, outcome X1 INCOMPLETE (A44; RA12): T2 uses C5H (A44, RA1), not a V006 C6 result'],
        'binding_inputs': bind,
        'fixed_across_all_cases': fixed,
        'pairing_and_decidability_rule': pair,
        'gates_before_any_T_result': gates,
        'tests': tests,
        'decision_rule': decision,
        'outcomes_first_applicable': outcomes,
        'outcome_reading_rules': reading_rules,
        'ngc3198_N_tests': ngc,
        'run_list': run_list,
        'seal_record_requirements': seal_record,
        'scope_untested': scope_untested,
        'error_decomposition': r1['error_decomposition'].replace('o_K = -int_{R^3 \\ O} T S_T e^{ik.x}: T3 (DDO)', 'o_K = -int_{R^3 \\ O} T S_T e^{ik.x}: T3 (DDO; K_big 64/256 against 128)'),
        'outcome_branch_tests_required': 'one synthetic branch test per outcome above in the sealed compare\'s suite (r5: 389/389 incl. FLOOR_LIKE before the T1-fail split, '
                                         'the flagged-run route to UNDECIDABLE_ROUTE_A_TAIL, UNDECIDABLE_AT_ITERATION_FLOOR neither passing nor failing, FLAG_PENDING_RULING; '
                                         'the round implementing S9 adds its tests)',
        'supersedes_draft': {'path': str(R1), 'sha256': R1_SHA},
        'root_items': root_items,
    }
    out = Path(os.environ['DRY_DIR']) if os.environ.get('DRY_DIR') else OUT      # dry run: review copy elsewhere
    out.mkdir(parents=True, exist_ok=True)

    def write(name, text):
        p = out / name
        with p.open('x') as f:
            f.write(text)
        return p
    write('KMAX_TAIL_PREREG_V007_FINAL_DRAFT.json', json.dumps(doc, indent=1, ensure_ascii=False) + '\n')
    # clause -> source map
    rows = []
    def walk(prefix, obj):
        if isinstance(obj, dict) and 'text' in obj and 'sources' in obj:
            rows.append((prefix, obj['sources'])); return
        if isinstance(obj, dict):
            for k, v in obj.items():
                walk(prefix + '.' + k if prefix else k, v)
    for sec in ('binding_inputs', 'fixed_across_all_cases', 'pairing_and_decidability_rule', 'gates_before_any_T_result', 'tests', 'decision_rule', 'run_list'):
        walk(sec, doc[sec])
    for o in outcomes:
        rows.append(('outcomes_first_applicable.%s' % o['outcome'], o['sources']))
    for i, r in enumerate(reading_rules):
        rows.append(('outcome_reading_rules[%d]' % i, r['sources']))
    for i, r in enumerate(seal_record):
        rows.append(('seal_record_requirements[%d]' % i, r['sources']))
    rows.append(('ngc3198_N_tests', ngc['sources']))
    M = ['# Clause → source ruling map — KMAX_TAIL_PREREG_V007_FINAL_DRAFT (unsealed)', '',
         'Every clause in the draft JSON carries its sources. This table lists them. "R1" means the clause text is R1\'s, unchanged or extended.', '',
         '| clause | sources |', '|---|---|']
    M += ['| `%s` | %s |' % (k, '; '.join(s)) for k, s in rows]
    write('CLAUSE_SOURCE_MAP.md', '\n'.join(M) + '\n')
    # root items
    Rr = ['# Root items — KMAX_TAIL_PREREG_V007_FINAL_DRAFT (unsealed)', '',
          'Places where the rulings conflict, leave a clause undefined, or depend on an input not yet built. Each one gives what the draft currently does.', '']
    for r in root_items:
        Rr += ['## %s — %s — %s' % (r['id'], r['kind'], 'OPEN' if r['status'] == 'OPEN' else 'RESOLVED (%s)' % r['status'].split(':')[1].strip().split(' ')[0]), '', '- **Status:** %s' % r['status'],
               '- **Clause:** `%s`' % r['clause'], '- **Issue:** %s' % r['issue'], '- **Draft:** %s' % r['draft'], '- **Sources:** %s' % '; '.join(r['sources']), '']
    write('ROOT_ITEMS.md', '\n'.join(Rr))
    # seal checklist
    S = ['# SEAL_CHECKLIST — V007 (for root; the draft is unsealed)', '', '| # | step | status at assembly | source |', '|---|---|---|---|']
    S += ['| %d | %s | %s | %s |' % (i + 1, a, b, c) for i, (a, b, c) in enumerate(checklist)]
    write('SEAL_CHECKLIST.md', '\n'.join(S) + '\n')
    # human-readable rendering
    H = ['# KMAX_TAIL_PREREG_V007 — final draft (UNSEALED)', '', status, '',
         '**Assembly:** Claude4, single author, UTC %s. Base: R1 `%s`. Dispatch 0526 `%s`. V005 addendum observed `%s` (open).' % (ts, R1_SHA, disp['0526']['sha256'], v005_observed), '']

    def render(title, d):
        H.extend(['## ' + title, ''])
        for k, v in d.items():
            if isinstance(v, dict) and 'text' in v:
                H.append('- **%s** — %s  \n  *Sources: %s*' % (k, v['text'], '; '.join(v['sources'])))
            elif isinstance(v, dict) and 'sha256' in v:
                H.append('- **%s** — `%s` (`%s`)' % (k, v['path'], v['sha256']))
            elif isinstance(v, dict):
                H.append('- **%s:**' % k)
                for k2, v2 in v.items():
                    if isinstance(v2, dict) and 'text' in v2:
                        H.append('  - **%s** — %s  \n    *Sources: %s*' % (k2, v2['text'], '; '.join(v2['sources'])))
                    elif isinstance(v2, dict) and 'sha256' in v2:
                        H.append('  - **%s** — `%s` (`%s`)' % (k2, Path(v2['path']).name, v2['sha256']))
                    else:
                        H.append('  - **%s** — %s' % (k2, v2))
            else:
                H.append('- **%s** — %s' % (k, v))
        H.append('')
    render('Binding inputs (sha256 from bytes at assembly)', bind)
    render('Fixed across all cases', fixed)
    render('Pairing and decidability', pair)
    render('Gates before any T result', gates)
    render('Tests', tests)
    render('Decision rule', decision)
    H.extend(['## Outcomes, first applicable', ''])
    for o in outcomes:
        H.append('- **[%s] %s** — %s  \n  *Sources: %s*' % (o['position'], o['outcome'], o['text'], '; '.join(o['sources'])))
    H.extend(['', '**Reading rules:**', ''])
    for r in reading_rules:
        H.append('- %s *(%s)*' % (r['text'], '; '.join(r['sources'])))
    H.extend(['', '## NGC3198 N-tests', ''])
    for k, v in ngc.items():
        H.append('- **%s** — %s' % (k, json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v))
    render('Run list', run_list)
    H.extend(['## Seal record requirements', ''])
    for r in seal_record:
        H.append('- %s *(%s)*' % (r['text'], '; '.join(r['sources'])))
    H.extend(['', '## Scope UNTESTED', ''] + ['- ' + s for s in scope_untested])
    H.extend(['', '## Root items', '', 'See `ROOT_ITEMS.md`. OPEN: %s. RESOLVED by A56/A57 and integrated: %s.' % (', '.join(r['id'] for r in root_items if r['status'] == 'OPEN'), ', '.join(r['id'] for r in root_items if r['status'] != 'OPEN')), ''])
    write('KMAX_TAIL_PREREG_V007_FINAL_DRAFT.md', '\n'.join(H) + '\n')
    rows = ['%s  ./%s' % (sha(p), p.relative_to(out)) for p in sorted(out.rglob('*')) if p.is_file() and p.name != 'HASHES.txt']
    write('HASHES.txt', '\n'.join(rows) + '\n')
    print('written', out, len(rows), 'files; V005 observed', v005_observed)


if __name__ == '__main__':
    main()

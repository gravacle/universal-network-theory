# Claude4 (dispatch 0580), revision r3: successor of c4v002. Reads the r2 draft (58a0b87d) from bytes and applies every root ruling
# since r2 (V005 A58-A80, open; observed sha recorded) plus dispatches 0561/0576/0577/0580/0582 as recorded clause edits. Each edit
# names its source ruling(s); CLAUSE_SOURCE_MAP_R3 and DELTA_R2_R3 list them. Every pin is computed from bytes here; a missing file
# or a sha prefix that differs is refused. Root-at-seal values are named SLOTS left PENDING (never guessed); a value a ruling or the packet
# names is shown as `named_candidates_verified_from_bytes` beside the slot, and is not the slot's value.
# Usage: TS=$(date -u +%Y-%m-%dT%H:%M:%SZ) [DRY_DIR=...] python3 -I -B make_v007_final_draft_c4v003.py
import copy, hashlib, json, os, re
from pathlib import Path

EX = Path('/Users/bgm/Research/UNT_EXCHANGE'); CA = EX / 'claude_artifacts'
C2 = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2')
OUT = CA / 'v007_final_prereg_c4' / 'r3'
R2 = CA / 'v007_final_prereg_c4/r2/KMAX_TAIL_PREREG_V007_FINAL_DRAFT.json'
R2_SHA = '58a0b87d995ce06e13706c127e3783dc352a292f0ec1614cf9b9b877b6140bfa'
V005 = C2 / 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md'
V005_FROZEN = C2 / 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md'
PKT = CA / 'v007_launch_packet_cx1'
T = CA / 'tail_scheme_impl_c2'
ENTRIES = ['A%d' % i for i in range(58, 81)]
PENDING = 'PENDING_ROOT_AT_SEAL_ASSEMBLY'
V005_FIRST_READ = '03120f0a6cb4d9d2610ff2e3129dd56b3e849131e8e885d6548bb1bc3a06b4c9'   # pasted from shasum at 17:31Z
V005_SECOND_READ = '4b937ec11192e3b54cfc114832be2b035c82a91753769c76316afb6bb08dcf5b'  # pasted from shasum at 17:43Z


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
    if sha(R2) != R2_SHA:
        raise SystemExit('r2 pin')
    doc = json.loads(R2.read_text())
    v005_observed = sha(V005)
    v005_text = V005.read_text()
    missing = [a for a in ENTRIES if ('## %s:' % a) not in v005_text]
    if missing:
        raise SystemExit('V005 addendum lacks ' + ', '.join(missing))
    has_a80 = '## A80' in v005_text
    disp = {n: pin(EX / 'FROM_CODEX' / f) for n, f in (
        ('0580', '0580_2026-10-18_claude4_final_prereg_r3_assembly.md'),
        ('0561', '0561_2026-10-18_codex1_seal_publication_order_ruling.md'),
        ('0576', '0576_2026-10-18_codex1_addendum_pin_at_seal.md'),
        ('0577', '0577_2026-10-18_claude4_0575_object_BUILD_V005.md'),
        ('0582', '0582_2026-10-18_claude3_codex2_successor_is_r11.md'),
        ('0559', '0559_2026-10-18_codex1_launcher_ramp_gate_and_admission_pins.md'),
        ('0544', '0544_2026-10-18_codex1_ntest_fixes_and_claude4_queue.md'))}
    r5check = pin(T / 'driver_r5/check/CHECK.md', '89a6de88')
    lane = {'Codex1 0047': pin(EX / 'FROM_CODEX1/0047_2026-10-18_finished_0574_seal_output_aggregate_fixes.md', '03f4686b'), 'driver_r5_check': r5check,
            'Codex1 0049': pin(EX / 'FROM_CODEX1/0049_2026-10-18_k32_replays_complete_lo91_blocker.md', 'ce37c472'),
            'Claude4 0079': pin(EX / 'FROM_CLAUDE4/0079_2026-10-18_done-0575-delta-build-v005-PASS.md', '07060e9c')}
    changes = []

    def node(path):
        d = doc
        for k in path:
            d = d[k]
        return d

    def upd(path, text=None, add=(), append=None, why=''):
        c = node(path)
        before = c['text']
        if text is not None:
            c['text'] = text
        if append:
            c['text'] = c['text'].rstrip() + ' ' + append
        for s in add:
            if s not in c['sources']:
                c['sources'].append(s)
        changes.append({'clause': '.'.join(path), 'kind': 'rewritten' if text is not None else ('extended' if append else 'sources'), 'added_sources': list(add),
                        'why': why, 'chars_before': len(before), 'chars_after': len(c['text'])})

    def new(path, text, *sources, why=''):
        parent = node(path[:-1])
        if path[-1] in parent:
            raise SystemExit('clause exists ' + '.'.join(path))
        parent[path[-1]] = cl(text, *sources)
        changes.append({'clause': '.'.join(path), 'kind': 'new', 'added_sources': list(sources), 'why': why, 'chars_before': 0, 'chars_after': len(text)})

    # ------------------------------------------------------------------ seal slots (0580 item 2), named, PENDING
    bound_named = {'build': pin(PKT / 'BUILD_V005.md', '46bc5b5d'), 'runbook': pin(PKT / 'RUNBOOK_V005.md', 'c1f574a0'),
                   'admission_format': pin(PKT / 'ROOT_SEAL_ADMISSION_FORMAT_V004.md', '6908ee88'), 'r5_template_plan_PENDING_ADDENDUM': pin(PKT / 'P128/LAUNCH_PLAN_V010.json', '26f1ebf9'),
                   'r5_template_command': pin(PKT / 'P128/LAUNCH_COMMAND_V010.txt', '7d649ac5'), 'binder': pin(PKT / 'bind_sealed_launch_plan_cx1v001.py', 'f3e4e2be'),
                   'guard': pin(PKT / 'producer_guard_cx1v008.py', '294cb776'), 'launcher': pin(PKT / 'route_a_token_launcher_cx1v007.py', '861bba68'),
                   'spec_registry': pin(PKT / 'SPEC_REGISTRY_R5_MS128_CX1V004.json', 'c7023846'), 'delta_review': pin(CA / 'review_launch_packet_0559_c4/REVIEW_LAUNCH_PACKET_0574_DELTA_C4V002.md', '2b483267')}
    slots = {
        'frozen_addendum': {'value': PENDING, 'path_to_be': str(V005_FROZEN), 'exists_at_assembly': V005_FROZEN.exists(),
                            'rule': 'Root exclusively creates the immutable copy at seal assembly, after the last pre-seal entry; it must contain every entry this text cites; its path and sha go to the binder and into the SEAL_RECORD.',
                            'sources': ['0576', '0574', 'RUNBOOK_V005 step 3', 'A78']},
        'driver': {'value': PENDING, 'branch': 'A72: r6 if conditions (a)-(c) all hold, otherwise r5',
                   'named_candidates_verified_from_bytes': {'r5': pin(T / 'driver_r5/galaxy_m0_forward_c2v010.py', 'b5cc62af'),
                                       'r6': 'NOT_A_CANDIDATE_AT_ASSEMBLY: no r6 BUILD published (driver_r6/ has no BUILD.md); A72 conditions (a)-(c) not yet reported'},
                   'rule': 'Path and full sha from bytes at seal; the SEAL_RECORD names it; the launcher refuses a plan whose driver differs (C4-S1, guard v008 / launcher v007); every identity run carries driver_sha256 equal to it (A67 N1). For T-runs see ROOT_ITEMS_R3 RI-24 (recommendation).',
                   'sources': ['A58 RI-01', 'A72', 'A67 N1', 'A78', '0574']},
        'compare': {'value': PENDING, 'rule': 'The final compare round: r11 (wf_9baf53cd, built from r10), or the fix round r12 if r11\'s rechecks force one (A80, 0582). It closes A79.1-6, A75 in full, A77.2 per family, A73 F2, every r10 recheck item (including binding gas_M_s_NGC to the registered value or refusing) and every Claude3 and Codex2 r10 finding, plus A71, A68 CHK-1, A69 and the RI-10 dispositions. Checks: three independent refute-by-default recheck lenses (A71; paths and blinding; regression). The distinct reviews of record (Claude3, Codex2) are of the final round.',
                    'named_candidates_verified_from_bytes': {'r10_frozen_not_for_seal': pin(CA / 'v007_compare_c2/r10/kmax_tail_compare_c2v007_r10.py', 'e801adc4')},
                    'sources': ['A79', 'A80', '0582', 'A75', 'A71', 'A58 RI-10']},
        'identity_comparator': {'value': PENDING, 'rule': 'c2v007 (equal bytes first; strict parse; A59-derived tokens only; injective labels) or its fix round if its own check or Codex2\'s review requires one; c2v004-c2v006 are superseded and not used at the seal.',
                                'named_candidates_verified_from_bytes': {'c2v007_source_observed_still_changing_at_assembly': pin(T / 'gates_v007/run_identity_compare_c2v007.py')},
                                'sources': ['A68', 'A70', 'A74', 'A76']},
        'identity_gate_records': {'value': PENDING, 'rule': 'Z2 (replace-mode tokens, A59), Z2_OFF_RO1 and B0prime_RERUN records produced by the identity-comparator slot on runs of the driver slot (r5 runs launched 14:56Z; r6 reruns if A72 adopts r6); each carries driver_sha256 = the driver slot; records carrying another driver sha are not seal records.',
                                  'observed_at_assembly': 'tail_scheme_impl_c2/gates_v007/records/ is empty', 'sources': ['A59', 'A67 N1', 'A72.3', 'A74', 'A76']},
        'launch_packet': {'value': PENDING, 'rule': 'BUILD_V005 (46bc5b5d) with the bound plan and command that the build-only binder writes from the selected template, the chosen driver and the frozen addendum (exclusive create); the pending r5 template V010 refuses validation by design.',
                          'named_candidates_verified_from_bytes': bound_named, 'pending_parts': ['bound_plan', 'bound_command', 'r6_template (if A72 adopts r6)'],
                          'sources': ['A78', '0576', '0577', '0574', 'Claude4 0079']},
        'certificates': {'value': PENDING, 'rule': 'Root confirms each record of record at seal assembly; every record states source_gas_M_s where it depends on M_s, equal to the case block\'s gas.M_s, which must be 128 for DDO.',
                         'named_candidates_verified_from_bytes': {'EPS': pin(T / 'certificates_v002/gates/EPS_CERT_V006.json', '598c8fa3'),
                                             'LO': pin(T / 'certificates_v004/gates/LO_CERT_V004_MS128.json', '1c384f76'),
                                             'GQ': pin(T / 'certificates_v003/gates/GQ_CERT_V005_MS128.json', 'fbceefe6'),
                                             'GQ_FAIL_control': pin(T / 'certificates_v003/gates/GQ_CERT_V004_MS128.json', '7ebb1d48'),
                                             'EPS_NGC_91': pin(T / 'certificates_ngc_k32/gates/EPS_CERT_NGC91_V001.json', '1d5eef1b'),
                                             'LO_NGC_91': 'NOT_ON_DISK_AT_ASSEMBLY (Codex1 0049: the sole blocker of the NGC N-test compare)',
                                             'GQ_NGC_91': 'NOT_REGISTERED_AT_ASSEMBLY (A64.2: with Codex1)',
                                             'I1T_NGC': pin(T / 'certificates_v002/gates/I1T_NGC_T120L_V001.json', '3ae7981a'),
                                             'DOUBLING_merged': 'NOT_ASSEMBLED (A73: format pending; assembled in the seal-assembly step)',
                                             'DOUBLING_DDO_half_evidence': {'K128': pin(T / 'doubling_v001/DOUBLING_K128_V001.json', 'ec169d43'),
                                                                            'K256': pin(T / 'doubling_v001/DOUBLING_K256_V001.json', '1ba4773d')}},
                         'sources': ['A70', 'A67 SF2', 'A68', 'A73', 'A64.2', 'A58 RI-03', 'A79 NEW-67']},
        'producer_registry': {'value': PENDING, 'rule': 'Root-registered producer paths and shas and the gate-record shas of record (A67 N2); the compare hashes the producer bytes, not only the claimed sha (A69.1); SR_K and every replay gate record bound to it (A62.2). Pinned in the compare as PIN_PRODUCER_REGISTRY (A67).',
                              'sources': ['A62.2', 'A67 N2', 'A67 (seal-time pins)', 'A69.1']},
    }
    # ------------------------------------------------------------------ binding_inputs: r2 pins kept / superseded
    bi = doc['binding_inputs']
    superseded = {}
    for k in ('driver', 'driver_r4_base', 'driver_r4_build_record', 'driver_r4_hashes', 'reference_successor_r4', 'tail_module', 'ro1_c2v002', 'nodes_v001',
              'spec_registry', 'spec_registry_r4_era', 'certificates_v002', 'certificates_v003', 'identity_comparator', 'identity_comparator_c2v003_predecessor',
              'compare', 'compare_r5_current'):
        superseded[k] = bi.pop(k)
    upd(('binding_inputs', 'successors'), text='Every route-A and route-B successor, worker, facade, controller, binding and the reference successor exactly as pinned by the '
        'build record of the driver in the driver slot (r5: tail_scheme_impl_c2/driver_r5/ BUILD and CASCADE_MAP_R5 plus the immutable CASCADE_MAP_R5_ADDENDUM required by '
        'A69 before the seal; r6, if adopted under A72: its own BUILD and cascade map, a pin-only cascade from tail-module v003). The tail module is the one that driver pins '
        '(r5: the TAIL_MEMORY_CAP_BYTES successor of A55.2; r6: v003 with the content-addressed cache, cache-disabled path byte-identical to v002, A72.1).',
        add=('A69', 'A72.1', 'A72.3', 'A58 RI-01'), why='r4 pins superseded by r5 (A58 RI-01) and the A72 r5/r6 branch')
    bi['ro1_role_table'] = cl(
        'RO1 custody is per case family (A77.2), verified from the driver slot\'s own tables: DDO cases fbe9ae79 (serial) / 869ce387 (parallel) with binding 86af6198; '
        'C4T-D5 and its R-PAIR member (the registered nodes_v001 source) 0ae245d8 (serial) / a5277172 (parallel) with binding 86af6198. The NGC RO1 workers (b6c4586d / ee0510df, '
        'binding 52dc4065; A73, A74) are not V007 custody. These are the r5 values; under r6 the table is re-read from r6\'s cascade map (pin-only) before the seal.',
        'A62.3', 'A73 (correction)', 'A74 (binding precision)', 'A77 N7', 'A77.2')
    bi['ro1_role_table_r5_pins'] = {k: pin(p, h) for k, p, h in (
        ('ddo_worker_serial', T / 'driver_r5/cascade/ro1_readout_c2/ddo_composite_stable_cached_root_worker_v002_uvtail_ro1_c2v002_r5.py', 'fbe9ae79'),
        ('ddo_worker_parallel', T / 'driver_r5/cascade/ro1_readout_c2/ddo_composite_stable_cached_root_worker_v002_parallel_uvtail_ro1_c2v002_r5.py', '869ce387'),
        ('nodes_worker_serial', T / 'driver_r5/cascade/tail_scheme_impl_c2/nodes_v001/route_a/ddo_composite_stable_cached_root_worker_v002_uvtail_ro1_nodes_c2v001_r5.py', '0ae245d8'),
        ('nodes_worker_parallel', T / 'driver_r5/cascade/tail_scheme_impl_c2/nodes_v001/route_a/ddo_composite_stable_cached_root_worker_v002_parallel_uvtail_ro1_nodes_c2v001_r5.py', 'a5277172'),
        ('binding', CA / 'ro1_readout_c2/ddo_composite_stable_cached_binding_v002_uvtail_ro1_c2v002.py', '86af6198'))}
    bi['spec_set'] = cl('The ten filled P128/M_s 128 V007 specs of SPEC_REGISTRY_R5_MS128_CX1V004 (c7023846; launch-packet slot), each with the A70 certificate slots; '
                        'their case block is accepted by the compare\'s own validate_case_block (Claude3 0065). Specs, caps and order are byte-identical from the reviewed '
                        'packet to BUILD_V005 apart from the declared changes (Claude4 0076/0079).', 'A70', 'A72 (packet final)', 'A78', 'Claude4 0079')
    for k in ('c5h_spec', 'review_v009_orig', 'qinf_evaluator', 'v006_r1_sealed', 'gate_b3_final'):
        if sha(bi[k]['path']) != bi[k]['sha256']:
            raise SystemExit('r2 pin moved ' + k)
    for k, v in bi['identity_specs'].items():
        if sha(v['path']) != v['sha256']:
            raise SystemExit('r2 identity spec moved ' + k)
    changes.append({'clause': 'binding_inputs', 'kind': 'restructured', 'added_sources': ['0580 item 2'],
                    'why': 'r2 r4-era and pre-slot pins moved to binding_inputs_superseded_r2; root-at-seal values moved to seal_slots', 'chars_before': 0, 'chars_after': 0})
    # ------------------------------------------------------------------ fixed_across_all_cases
    upd(('fixed_across_all_cases', 'production_tail', 'P'), text=
        'Production K_big P = 128 /kpc. Outer domains by case (A58 RI-05): C2T, C3T, C4T, C6T, C4T-A and S4T use cylinder K_big 128; S4T keeps its R1 sphere/cube '
        'kept-region rule ("sphere tail" = sphere truncation of the kept region with the cylinder tail; A62 note). The exceptions are by design: C4T-KLO (K_big 64) and '
        'C4T-KHI (K_big 256) (T3); C4T-C5c (continuum_v001, outer cube K_out 5, RA2); C4T-D5 (nodes_v001 on G5\\G4, no continuum outer, RA1). RA4\'s case list reads '
        'C4T-KLO/KHI.', add=('A58 RI-05', 'A62 (S4T note)'), why='RI-05 ruled')
    upd(('fixed_across_all_cases', 'production_tail', 'quadrature'), text=
        'Defined by the registered rules: order 8; w_perp_max 0.05 /kpc; w_z_max 0.02 /kpc; phases 1.415 / 1.34 rad; corner_zone_rule as R1 (IA1). The module derives N_perp '
        'and N_z from K_big. R1\'s numeric N values (N_z_plus 12800) are the K_big 32 instance and informational. The R/z eval and source extents depend on geometry and '
        'are unchanged. Each case block carries the sha of its registered P128 uv_tail config (S8).', add=('A58 RI-03',), why='RI-03 ruled')
    upd(('fixed_across_all_cases', 'production_tail', 'gas'), append=
        'NGC: production K_big 32 (A64.2) with M_s 96 unless GQ_NGC at M_s 96 fails on its required coverage (>= sqrt2 * 64 = 90.5, i.e. to 91 /kpc), in which case root '
        'rules on M_s 128 (A64.2; ROOT_ITEMS_R3). The certificate M_s must equal the case block\'s registered gas.M_s, and for DDO that value must be 128 (A68 CHK-1, A75.8, '
        'A79 NEW-67). The compare binds the NGC gas M_s to the registered value (96) or refuses (A80, r10 validity recheck note).', add=('A60', 'A64.2', 'A68 CHK-1', 'A75.8', 'A79 NEW-67', 'A80'), why='NGC K_big/M_s and the M_s binding')
    upd(('fixed_across_all_cases', 'production_tail', 'memory_guard'), text=
        'TAIL_MEMORY_CAP_BYTES is a resource guard, not numerics (design K15); r5 raises it to 8 GiB through a module successor that is AST-identical otherwise (A55.2). '
        'Under r6 the module is v003 (A72.1).', add=('A72.1',), why='driver-slot branch')
    new(('fixed_across_all_cases', 'production_tail', 'tail_table_cache'),
        'A72: adopted only if (a) the independent check passes, including stale-cache attacks, (b) bitwise equality is TESTED at K_big 32, 128 and 256, and (c) the measured '
        'timings (kbig_timing_v003/) show a net saving after the cost of the cascade, its review and an identity rerun. If adopted, the sealed driver is r6; the identity '
        'runs are rerun on r6 with caching enabled where the tail is ON; every V007 T-case runs with the cache, so all are compared on equal footing; the r5 identity runs '
        'are superseded and kept. If any condition fails, V007 seals on r5 and no case uses the cache. The cache is bitwise exact (hit, miss and cold builds identical). '
        'At launch the plan\'s driver must equal the SEAL_RECORD\'s driver (C4-S1; A78), so the ten T-cases of one bound plan share the sealed driver.', 'A72', 'A72.3', 'A78', why='new ruling A72')
    upd(('fixed_across_all_cases', 'brackets'), add=('A58 RI-05',), why='RA4 case list C4T-KLO/KHI ruled')
    upd(('fixed_across_all_cases', 'route_a'), append=
        'RO1 records are checked against the case family\'s role table (binding_inputs.ro1_role_table): serial/parallel against the admitted attempt\'s column_workers '
        '(for T-case PICARD members the base\'s admitted attempt, per A53), parsed strictly (A71); a cross-family worker or binding is a RECORD_DEFECT.',
        add=('A77 N7', 'A77.2'), why='A77.2 role table')
    # ------------------------------------------------------------------ pairing and decidability
    upd(('pairing_and_decidability_rule', 'noise_allowance'), text=
        'Norm in which contraction is measured: ||d_k||_tau = max_i |d_k,i|/tau_i. q = the larger of the last two observed ratios ||d_k||_tau/||d_k-1||_tau (with only one '
        'ratio, that ratio); there is no cap (A58 RI-18). For q < 1 the norm-level bound is E_i^norm = tau_i * ||d_last||_tau * q/(1-q), exactly; with exactly one increment, '
        'E_i = tau_i * ||d_last||_tau. Per-row bound for rows whose last two increments have the same sign (d_last,i * d_prev,i > 0): |d_last,i| * q_i/(1-q_i), '
        'q_i = |d_last,i|/|d_prev,i|, exactly (S7 without the 0.9 cap). Alternating bound for rows whose last two increments change sign: the tail of a geometric series '
        'with ratio -q_i, |d_last,i| * q_i/(1+q_i), q_i = |d_last,i|/|d_prev,i| (A56 N1). E_i = max(E_i^norm, same-sign bound, alternating bound). E is UNAVAILABLE for the '
        'run (its tests undecidable; to R-PAIR) when: no increment is observed; a tau-norm ratio >= 1 on either of the last two ratios (NEW-7); any row has q_i >= 1, '
        'same-sign or alternating (A56 N1); or a pass-row gap / row-ID defect exists (B4, S9). A slowly contracting run (q near 1) therefore gets a large E and goes to '
        'R-PAIR. E_i(pair) = E_i(a) + E_i(b). The geometric bound assumes the observed ratio is the map\'s contraction factor: DECLARED, checked against each run\'s own '
        'increments.', add=('A58 RI-18',), why='RI-18 ruled: the q cap of 0.9 is removed (stricter)')
    upd(('pairing_and_decidability_rule', 'if_not_decidable_R_PAIR'), append=
        'On an exact tie in (E + E^A)/tau the branch row is the lowest row index (deterministic; A69 AMB-07). Member RO1 records follow the case family\'s role table '
        '(A77.2; for T-case PICARD members serial/parallel is checked against the base\'s admitted attempt).', add=('A69 (AMB-07)', 'A77.2'), why='tie-break and role table')
    # ------------------------------------------------------------------ gates
    G = ('gates_before_any_T_result',)
    upd(G + ('B1_Z2',), text=
        'Z2 = spec 2d5e79d0 (A2F10 C2, v010 tail ON, cylinder K_big = K = 2, every stage domain empty), route A at N8 as registered in that spec (route_a.column_workers 8; '
        'R1\'s "serial" is superseded, A58 RI-11), RO1 workers armed (ro1.armed true, fired false), against DDO154_A2F10_ROUTE_A_PARALLEL_N8_C2V008_DECIDING_RUN_V001 '
        '(883b37a0; COMPARE_DECIDING_II e1d3c072 shows it bitwise equal to serial): all route-A blobs/records/arrays, every stage npz, rows and speeds equal; only the declared '
        'custody list differs. The token map is derived by rule from the sealed driver\'s pin tables only (A58 RI-12), never from the observed diff, and for the 8 '
        'successor kinds it REPLACES the base->token mapping on the new side (A59: the new side must carry the successor, so a base script on the new side fails the gate). '
        'Tokens follow the identity comparator\'s closed grammar: only A59-derived [ref, new, token] triples, each exactly once, injective labels (A73 SF2, A74). Compared '
        'with the identity-comparator slot (c2v007 lineage); the raw successor-custody check is recorded in the seal record (A59). The run carries driver_sha256 = the '
        'driver slot (A67 N1). Precondition L as R1.', add=('A58 RI-11', 'A58 RI-12', 'A59', 'A67 N1', 'A73 SF2', 'A74', 'A76'), why='Z2 rulings A58-A76')
    upd(G + ('Z2_OFF_RO1',), text=
        'Mandatory: spec 894e5b3a = the 883b37a0 reference spec under v010 tail OFF with the RO1 workers armed; compared by the identity-comparator slot with tail-OFF '
        'semantics: admits only the declared enabled:false records, fails any other uv_tail record, requires ro1 armed true and fired false. Rerun on the driver slot '
        '(r5 runs launched 14:56Z; r6 if adopted); carries driver_sha256 = the driver slot.', add=('A67', 'A67 N1', 'A72.3', 'A74', 'A76'), why='comparator and driver slot')
    upd(G + ('B0prime_RERUN',), append='Compared by the identity-comparator slot; carries driver_sha256 = the driver slot (A67 N1); rerun on r6 if A72 adopts r6.',
        add=('A67 N1', 'A72.3', 'A74'), why='comparator and driver slot')
    upd(G + ('B0_RO1',), append='A repeated B0_RO1 case kind is a RECORD_DEFECT (guards keyed on the semantic kind, not the whole object; A79.1).', add=('A79.1',), why='A79 blocking item 1')
    upd(G + ('B0_N3',), append='A repeated constructions entry is a RECORD_DEFECT (A79.1).', add=('A79.1',), why='A79 blocking item 1')
    upd(G + ('EPS',), text=
        'Numerical sup searches are estimates, not proofs; envelope consumers read the full-envelope fields (A57.4). q(k) sampled via QINF evaluator f58de0dc (cache 7b9816ae '
        'cross-check), 13+13 directions x 64/decade per unit shell of [K, K_big]; refined 26+26 x 128/decade; eps_s(refined) <= 1.1 eps_s(base) else refine; 2 refinement '
        'failures -> EPS_UNCERTIFIED. Coverage: DDO from 2 to at least sqrt2 * 2P (= 362.04 at P = 128; the DDO record covers [2, 363]); NGC at production K_big 32 '
        'with N3\' to 64: >= sqrt2 * 64 = 90.5, i.e. [2, 91] (A64.2; supersedes RI-17\'s [2, 46], which was the K_big 32 N3-case edge of A58). The record carries '
        'envelope_bound {rule A52_5_SUP_OVER_DIRECTION_TIMES_CARDINAL_TORUS, coverage_max_inverse_kpc} with coverage >= sqrt2 * 2P (A52.5 as raised by A54). The top-level '
        'and nested "dominates" flags must agree; a disagreement is a RECORD_DEFECT (A67 N4). EPS does not depend on M_s (A68); the record of record is the EPS slot '
        '(A70: EPS_CERT_V006 598c8fa3 for DDO; EPS_CERT_NGC91 for NGC). Until such a record is slotted, per-shell values above 15 /kpc are lower bounds and SRB_ROT is not '
        'read. An estimate, not a proven sup.', add=('A58 RI-17', 'A64.2', 'A67 N4', 'A68', 'A70'), why='coverage and record rulings')
    upd(G + ('LO',), text=
        'LO (V001 sec 1.6) on the DDO shells, at the M_s 128 source (A57.1), with the partition ruled by A58 RI-06: (4,5], (5,6], (6,8], (8,12], (12,16], (16,32], (32,64], '
        '(64,128], (128,256], (256,363]. Each shell <= 0.005 tau, summed <= 0.05 tau; coverage starts at lo >= K = 4 and reaches >= sqrt2 * 2P (A69.2, A54, A55.4). A '
        'duplicate shell is a RECORD_DEFECT naming both entries (A71, A75 A01), keyed on the shell range. The record states source_gas_M_s, which must equal its own gas_M_s '
        'and tail_config gas.M_s (A73 F2) and the case block\'s registered gas.M_s, which is 128 (A68 CHK-1, A75.8, A79 NEW-67); a superseded M_s 64 record refuses. Record '
        'of record: the LO slot (A70: LO_CERT_V004_MS128 1c384f76).', add=('A58 RI-06', 'A68 CHK-1', 'A69.2', 'A70', 'A71', 'A73 F2', 'A75 A01', 'A75.8', 'A79 NEW-67'),
        why='RI-06 partition and record rulings')
    upd(G + ('GQ',), text=
        'For every gas roster used, the gas transform at M_s and at 2M_s agrees to <= 1e-12 * P0, certified per source geometry over the union of all T-case tail node domains '
        '(DDO C2T-C4T, C4T-KLO, C4T-KHI, incl. the corner zones). At production M_s 128 the DDO certificate is computed at M_s 128 against 256 over the full DDO reach on all '
        'nodes (A57.1); the all-nodes check uses the root-registered per-geometry production node counts from the gq_full part records, and a record whose all_nodes count '
        'equals the 4096 sample refuses (A67 SF1). Roster names map to geometries by the fixed map DDO_C2T -> C2T_KB<P>, DDO_C3T -> C3T_KB<P>, DDO_C4T -> C4T_KB<2P>; a '
        'mismatch, a duplicate roster name, or a roster name repeated with a different valid geometry is a RECORD_DEFECT (A75.6 P-SF1, A75 A05, A79.1). The certificate M_s '
        'is bound as in LO (A68 CHK-1). Record of record: GQ_CERT_V005_MS128 (fbceefe6), with V004 (7ebb1d48) as the FAIL control (A67 SF2, A70). NGC: GQ_NGC is a required '
        'input over [2, 91] at the NGC M_s (A62 via 0544, A64.2). A failure or a coverage shortfall reads UV_TAIL_GAS_QUADRATURE_UNCERTIFIED, which is NUMERICS_UNCERTIFIED.',
        add=('A64.2', 'A67 SF1', 'A67 SF2', 'A68 CHK-1', 'A70', 'A75 A05', 'A75.6', 'A79.1', '0544'), why='GQ record rulings')
    upd(G + ('DOUBLING',), text=
        '(w/2, o+4) is required at K_big 128 and 256 with gas M_s 128: DDO static rows on saved C4R3 le3 change <= tau_i/20 (A58 RI-03); NGC lnN reads on the saved operator '
        'change <= theta/20 at the NGC production K_big. One merged record (FIELDS_R7/R8 shape) carries ddo_K_big_inverse_kpc {128, 256}, ddo_gas_M_s 128 and the NGC half '
        '(ngc_operator_sha256 e6453d52, ngc_max_change_over_theta from NQ at K_big 32); it is assembled at seal assembly and must exist before the seal (A73, A58 RI-03; '
        'the DDO half PASSed at 128 and 256, max 4.7e-13 tau, independently recomputed). Its sha is registered before the seal (A79 NEW-61) and it keeps RI-03\'s production-128 '
        'rule (A79 NEW-67).', add=('A58 RI-03', 'A73', 'A79 NEW-61', 'A79 NEW-67'), why='DOUBLING rulings')
    upd(G + ('RB_FP',), append='The shell split covers the domain exactly [K, sqrt2 * P]; excess, shortfall or a partial-domain record refuses and never PASSes '
        '(A62.1, A67 N3, A69.2).', add=('A62.1', 'A67 N3', 'A69.2'), why='shell coverage')
    upd(G + ('HARMONIC',), append='A repeated HARMONICS row is a RECORD_DEFECT (A79.1).', add=('A79.1',), why='A79 blocking item 1')
    upd(G + ('LO_NGC',), append='At NGC production K_big 32 its shell coverage reaches >= 91 /kpc (A64.2); shells keyed on range, a duplicate is a RECORD_DEFECT (A75 A01); an '
        'NGC roster with a different range refuses (A79.1). Lane state at assembly: LO_NGC to 91 is absent and is the sole blocker of the NGC N-test compare (Codex1 0049).',
        add=('A64.2', 'A75 A01', 'A79.1', 'Codex1 0049 (state only)'), why='NGC coverage')
    upd(G + ('record_verdicts',), append='An unregistered record reads NO_RUN (A67 order N1). Seal-time record states: GQ_CERT_V003 (no all_nodes), LO_CERT_V003_MS128 (no '
        'source_gas_M_s), the c2v004 identity records and unregistered gate records read RECORD_DEFECT until re-emitted (A73).', add=('A67 (order N1)', 'A73'), why='record states')
    new(G + ('no_last_wins',), 'Any list-to-mapping conversion, and any JSON object, rejects duplicate keys before the mapping is built: shells, rows, cases, gates, members, '
        'tokens, registry entries, NPY/NPZ headers and the JSON parse itself (object_pairs_hook). A duplicate is a RECORD_DEFECT naming both entries by index or JSON path, '
        'never by a record label (blinding), even when the values are equal. Guards key on the semantic identity (case kind, roster name, shell range), not the whole '
        'object. NPZ archives: collisions are rejected both in raw member names and in the logical names NumPy uses; an extensionless NPY member is refused. No tool may be '
        'last-wins anywhere; the final compare round lists every dict-from-list site with its guard and a MUST_FAIL test. Every refusal site names both entries, '
        'including the fifteen sites listed in A79.6 (T01/T02; C02-C04 and S01; the registry duplicate-key forms; the S9/D2 row codes, C10, A06/A07/B09).',
        'A71', 'A74', 'A75.1', 'A75.2', 'A75.3', 'A79.1', 'A79.4', 'A79.6', why='new ruling A71 (systematic)')
    new(G + ('after_seal_marker_policy',), 'PRODUCED_AFTER_THE_SEAL is accepted only for the eight gates computed from V007 run outputs: SRB_ROT, RB_FP, T2I, EA, MT, I1T, '
        'FLAG_RULINGS and HARMONICS; at compare time those records are verified by producer pin against the producer registry (A62.2, A69). It is refused for SR_K, EPS, GQ, '
        'LO, LO_NGC, DOUBLING and the identity gates, whose records of record exist (and SR_K\'s gate-record sha is registered) before the seal.',
        'A79 NEW-61 (as corrected 17:16Z)', 'A75.7 (corrected by A79)', 'A67 N2', 'A62.2', 'A69', why='A79 NEW-61 corrected')
    new(G + ('c5h_interlock',), 'c5h_path_hit and read_run catch /.vol/<dev>/<ino> aliases of the C5H run directory and its files, and hard links, by (st_dev, st_ino) '
        'against every file of the C5H run (H-07); rejecting any multiply-linked file on the protected device is the accepted conservative substitute for a per-file inode '
        'inventory (NEW-64); a failed os.stat of the registered C5H root is a refusal, never a silent drop (A79.3). The name test and the identity walk run on the resolved '
        'path as well as the lexical one; every prefix of realpath(s) is stat-walked against the registered (st_dev, st_ino); strings are NFC-normalized before every '
        'comparison, so firmlink (/System/Volumes/Data), NFD and symlink-then-/../ spellings are caught (A79.5). A refusal can delay the verdict but never changes a reading.',
        'A72 (H-07)', 'A75.4', 'A79.3', 'A79.5', 'A79 NEW-64', why='H-07 rulings')
    new(G + ('blinded_output',), 'Blinded modes print codes only: the 13 early-refusal sites (A75.5) and the CLI parser, whose error() raises a typed refusal and prints a '
        'code only, with allow_abbrev=False and repeated flags refused (A79.2, A76 SF-ARGV).', 'A75.5', 'A79.2', 'A76 (SF-ARGV)', why='blinding rulings')
    new(G + ('certificate_ms_binding',), 'Every certificate whose content depends on M_s states source_gas_M_s; it must equal the record\'s own gas_M_s, its tail_config '
        'gas.M_s and the case block\'s registered gas.M_s, and for DDO that value must be 128 (both bindings hold together). A superseded M_s 64 certificate refuses in an '
        'M_s 128 context; a matched-64 control refusing is correct.', 'A68 CHK-1', 'A68 (records)', 'A73 F2', 'A75.8', 'A79 NEW-67', why='M_s binding')
    # ------------------------------------------------------------------ tests
    upd(('tests', 'T1_S'), append='("sphere tail" for S4T = sphere truncation of the kept region with the cylinder K_big 128 outer tail; A62 note, A58 RI-05.)',
        add=('A62 (S4T note)', 'A58 RI-05'), why='S4T wording')
    upd(('tests', 'SR_K'), append='SR_K and its gate record are bound to root-registered producer shas (A62.2); its gate-record sha of record is registered in the producer '
        'registry before the seal (A67 N2), so PRODUCED_AFTER_THE_SEAL is refused for SR_K (A79 NEW-61); a synthetic or fixture record refuses; a bitwise-identical Delta '
        'across K is an SR_K RECORD_DEFECT (A67 N2).', add=('A62.2', 'A67 N2', 'A79 NEW-61'), why='SR_K record rulings')
    # ------------------------------------------------------------------ decision rule and outcomes
    upd(('decision_rule', 'ADOPT_TAIL_cube_K4_C4T'), append='No RECORD_DEFECT anywhere (A71); every seal slot filled and verified from bytes (0580).', add=('A71', '0580'),
        why='slots and no-last-wins')
    oc = {o['outcome']: o for o in doc['outcomes_first_applicable']}
    o = oc['NO_RUN']
    o['text'] += ' An unregistered record reads NO_RUN (A67 order N1); a duplicate anywhere is a RECORD_DEFECT (A71).'
    o['sources'] += ['A67 (order N1)', 'A71']
    changes.append({'clause': 'outcomes_first_applicable.NO_RUN', 'kind': 'extended', 'added_sources': ['A67 (order N1)', 'A71'], 'why': 'record rulings', 'chars_before': 0, 'chars_after': len(o['text'])})
    o = oc['UNDECIDABLE_AT_ITERATION_FLOOR']
    o['text'] += ' A C4T-KHI B4 gap whose Picard members reach the floor reads UNDECIDABLE_AT_ITERATION_FLOOR, PROVISIONAL; it is undecidable and adopts nothing (A67 NEW-31).'
    o['sources'] += ['A67 NEW-31']
    changes.append({'clause': 'outcomes_first_applicable.UNDECIDABLE_AT_ITERATION_FLOOR', 'kind': 'extended', 'added_sources': ['A67 NEW-31'], 'why': 'NEW-31 accepted', 'chars_before': 0, 'chars_after': len(o['text'])})
    # ------------------------------------------------------------------ NGC N-tests
    n = doc['ngc3198_N_tests']
    n['production_K_big_A64'] = ('NGC production K_big = 32, in force after the formal N3 at 16 failed (8-vs-16 dL 0.749 theta; A64.2). N3\' = {16, 64} against 32; N1, N2, '
                                 'N4 and NQ are evaluated at 32; N1 is read only on the production-K_big records (A64.3). The R1 tail block above is the K_big 16 instance; '
                                 'its node counts are re-derived by the module rules at 32. EPS, LO_NGC and GQ_NGC coverage >= sqrt2 * 64 = 90.5 (to 91 /kpc).')
    n['tests'] = dict(n['tests'])
    n['tests']['N3'] = 'N3\' = K_big 16 and 64 against production 32, at every ring and azimuth: |Delta S| <= theta/4 and |Delta dL| <= theta/4 (A64.2; the R1 form 8/32 against 16 is superseded)'
    n['C1_scope_A64'] = 'C1\' applies only on NOT_GRID rings (A17); C1 is kept on TRUNCATION_SHAPE and QUADRATURE_LIMITED rings (A64.1).'
    n['N1_consequence_A66'] = ('Ruled after the N1 diagnostic was seen and labelled so (A66): the N-test reading is decided by the compare as registered; N_FAIL_N1 is never '
                               'relabelled a pass. N_FAIL_N1 confined to TRUNCATION_SHAPE rings does not block NGC route A/B; every NGC row within the radial support of a '
                               'failing TRUNCATION_SHAPE ring is flagged TRUNCATION_SHAPE_RESIDUAL in the freeze manifest (disclosure, not INVALID, with the measured S/theta). '
                               'A failure of N0, NQ, N2 or N3\', or an N1 failure on a ring that is not TRUNCATION_SHAPE, blocks NGC route A/B.')
    n['NQ_note_A62'] = 'NQ\'s exact zero is genuine: the lnN resolution is one N step, about 3.3e-8 theta (A62, Claude4 0065).'
    n['sources'] = list(n['sources']) + ['A62', 'A64.1', 'A64.2', 'A64.3', 'A66']
    changes.append({'clause': 'ngc3198_N_tests', 'kind': 'extended', 'added_sources': ['A62', 'A64.1', 'A64.2', 'A64.3', 'A66'], 'why': 'NGC K_big 32 and N1 consequence', 'chars_before': 0, 'chars_after': 0})
    # ------------------------------------------------------------------ run list
    rl = ('run_list',)
    upd(rl + ('DDO_gates',), text='Z2 (2d5e79d0), Z2_OFF_RO1 (894e5b3a), B0prime_RERUN (4ac5527a): the r5 identity reruns launched at 14:56Z (monitor ba031c23; wall 43,200 s, '
        'RSS 16 GiB, output 32 GiB; no retries; detached), compared by the identity-comparator slot; if A72 adopts r6 they are rerun on r6 with caching enabled where the '
        'tail is ON and the r5 runs are superseded and kept.', add=('A67', 'A72.3', 'A74'), why='identity reruns')
    upd(rl + ('DDO_tests',), text='C2T, C3T, C4T, C6T, S4T, C4T-D5, C4T-C5c, C4T-KLO (K_big 64), C4T-KHI (K_big 256), C4T-A: the ten filled P128/M_s 128 specs '
        '(binding_inputs.spec_set), launched by root from the bound plan (launch-packet slot), all on the driver slot and, under r6, all with the cache.',
        add=('A70', 'A72.3', 'A78', '0576'), why='spec set and launch')
    upd(rl + ('contingent',), append='gates_v004: the R-PAIR member specs PASS (18/18 leaves; the C5H ROUTE_A B0 holds; 10/10 negative controls); PICARD members are '
        'fillable only after their bases run (A68).', add=('A68',), why='gates_v004 result')
    upd(rl + ('replays',), append='DOUBLING merged record (A73); EA, MT, I1T, T2I, SRB_ROT, RB_FP, FLAG_RULINGS and HARMONICS records are produced after the seal from run '
        'outputs and verified by producer pin (A79 NEW-61).', add=('A73', 'A79 NEW-61'), why='record timing')
    upd(rl + ('NGC',), text='NQ, N0, N1, N2, N3\' (16, 64 vs 32), N4 at NGC production K_big 32; LO_NGC, EPS and GQ_NGC to 91; NGC I1-T.', add=('A64.2',), why='K_big 32')
    upd(rl + ('limits',), text='Resources are root\'s launch decision. Route-A admission is ramp-gated: KHI starts immediately; each later case starts only after the '
        'previous case logs its first completed route-A iteration and free memory is >= 25% with fewer than 6 cases in route A; route B overlaps freely; every decision is '
        'logged (A72, 0559). RSS caps >= 1.5x the modelled peak; monitors and the launcher run detached (A61). One case failing does not cancel the others; new starts halt '
        'only on systemic failures (RSS cap or memory kill, disk guard, a refusal that would repeat for every case) or a predecessor that ends without a completed iteration '
        '(A62, 0559). The root admission config names the BUILD_V005 launcher and guard sources exactly (A78 N2). The module memory cap is a resource guard (8 GiB in r5).',
        add=('A61', 'A62', 'A72 (ITEM3-R1)', '0559', 'A78 N2'), why='launch rulings')
    total = sum(c['solo_hours_UNTESTED'] for c in json.loads((PKT / 'P128/LAUNCH_PLAN_V010.json').read_bytes())['calls'])
    upd(rl + ('cpu_hours_estimate_UNTESTED',), text='Restated from the measured-timing cost model in Codex1\'s launch packet (plan V010, UNTESTED): solo route-A+B '
        'hours per case from %.1f (C4T-KLO, C4T-C5c) to 27.8 (C4T-KHI), %.1f solo hours in total; wall caps about 2x solo (KHI 56 h). Co-load may lengthen execution; '
        'elapsed time is unbounded under the memory gate. UNTESTED.' % (4.99089, total), add=('A58 RI-09', 'A61'), why='RI-09 ruled')
    # ------------------------------------------------------------------ seal record requirements (append)
    sr = doc['seal_record_requirements']
    add_sr = [
        cl('Publication order (0561, FORMAT_V004, RUNBOOK_V005): root first freezes the V005 addendum (exclusive create) and binds the plan with the build-only binder; then '
           'exclusively creates the SEAL_RECORD, which names the prereg sha (this text, the first pin), the compare, the driver and the frozen-addendum pins; then the '
           'ROOT_SEAL_ADMISSION config pinning the SEAL_RECORD\'s full sha; then a separate SEAL_ADMISSION_RECEIPT naming both, posted in a numbered root packet. No file is '
           'edited after it is created; the config sha is therefore not inside the SEAL_RECORD (see ROOT_ITEMS_R3 RI-19 on A72 H-01\'s wording).',
           '0561', '0576', 'A72 (H-01)', 'A78', '0580'),
        cl('The seal record quotes the final compare IMPL\'s list of every compare-lane NEW item with its disposition: adopted as text if stricter on adoption and gap-filling, '
           'rejected if looser (A58 RI-10).', 'A58 RI-10'),
        cl('The raw successor-custody check of the Z2 run is recorded (A59).', 'A59'),
        cl('Disclosure E5-08: C5R3 ran the C5H driver and spec except for the label and fs overrides, so the C5R3 route-A fixtures the producers were tested on are very '
           'likely equal to C5H\'s route-A values, E^A included; they are not row values, and A47 I3 holds.', 'A62 (E5-08)'),
        cl('Seal-time pins in the compare: PIN_ADDENDUM_V005 (the frozen copy), PIN_V010_R5_CHECK (or the r6 equivalent under A72), PIN_PRODUCER_REGISTRY; the custody pins '
           'follow the A77.2 role table read from the driver slot.', 'A67 (seal-time pins)', 'A72', 'A77.2'),
        cl('CASCADE_MAP_R5_ADDENDUM (the immutable inventory addendum naming the unreachable pin-only successor) exists before the seal if the driver slot is r5.', 'A69'),
        cl('The root admission config names the BUILD_V005 launcher and guard sources exactly (the build check is a substring match).', 'A78 N2'),
    ]
    sr.extend(add_sr)
    changes.append({'clause': 'seal_record_requirements', 'kind': 'extended', 'added_sources': ['0561', '0576', 'A58 RI-10', 'A59', 'A62', 'A67', 'A69', 'A78 N2'],
                    'why': '%d requirements added' % len(add_sr), 'chars_before': 0, 'chars_after': 0})
    # ------------------------------------------------------------------ scope, decomposition, branch tests
    doc['scope_untested'] = [s for s in doc['scope_untested'] if not s.startswith('driver v010 r5') and not s.startswith('GQ for C4T-K256 at the registered M_s 64')] + [
        'GQ for C4T-KHI at M_s 64 (TESTED-NEGATIVE in certificates_v002; superseded by production M_s 128, A57/A68)',
        'cost figures restated from the launch packet cost model (A58 RI-09): UNTESTED',
        'float-floor note (A67): deciding test the late-pass increments of the first real 12-pass member',
        'the A72 cache saving, until kbig_timing_v003 reports (condition (c))']
    doc['error_decomposition'] = doc['error_decomposition'].replace('N3 (NGC)', "N3' at NGC production K_big 32 (A64)")
    doc['outcome_branch_tests_required'] = ('one synthetic branch test per outcome above in the sealed compare\'s suite (the final round: r11, or r12; A80), plus every A75 '
                                            'reproduction as a MUST_FAIL case and every dict-from-list guard of A71 with its own test.')
    # ------------------------------------------------------------------ header
    doc['schema'] = 'KMAX_TAIL_PREREG_V007_FINAL_DRAFT'
    doc['revision'] = 'r3'
    doc['status'] = ('FINAL DRAFT r3 (NOT SEALED). Assembled by Claude4 (dispatch 0580) from r2 58a0b87d, integrating V005 A58-A79%s (open; observed sha %s at assembly) '
                     'and dispatches 0561, 0576, 0577, 0582. Written before any V007 (tail-corrected) result exists; nothing was launched; C5H, UVT_* and targets were not read. '
                     'Root fills the named seal slots and seals; the open items are in ROOT_ITEMS_R3.' % (' and A80' if has_a80 else ' (A80 announced in 0582)', v005_observed))
    doc['assembly'] = {'by': 'Claude4 main session, single author (helpers unavailable until 2026-10-23T19:00Z)', 'utc': ts, 'dispatch': disp['0580'],
                       'rulings_read': {'V004_addendum_frozen': doc['decision_pins_frozen']['V004_addendum'], 'V005_addendum_open_observed': {'path': str(V005), 'sha256': v005_observed},
                                        'V005_addendum_reads': [{'read': 'first read, 17:31Z (ACK 0080)', 'sha256': V005_FIRST_READ},
                                                                {'read': 'second read, 17:43Z: adds A80, A79.5 and A79.6, all integrated', 'sha256': V005_SECOND_READ},
                                                                {'read': 'at generation (this run)', 'sha256': v005_observed}],
                                        'dispatches': {k: v for k, v in disp.items() if k != '0580'}, 'lane_state_cited': lane},
                       'base': {'path': str(R2), 'sha256': R2_SHA}}
    doc['decision_pins_pending_at_seal'] = {'V005_addendum_frozen_copy': {'path': str(V005_FROZEN), 'sha256': PENDING,
                                                                          'entries': 'A47-A79%s; cited by name until frozen' % (', A80' if has_a80 else '')}}
    doc['cites_by_name'] = ['ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM: A47-A79%s (open; pinned by its frozen copy, PENDING)' % (', A80' if has_a80 else ''),
                            'KMAX_MATRIX_PREREG_V006_R1, sealed 807fc5bf, outcome X1 INCOMPLETE (A44; RA12): T2 uses C5H (A44, RA1), not a V006 C6 result']
    doc['not_v007_text_scope'] = cl('A60 (NGC gap rows, cut binding, fe5a2f06, miss-reading prereg), A61 calibration F1-F4, A63 and A65 (stage-0 grid; STAGE0_GRID_OUTER), '
                                    'A66 freeze-manifest flag, the NGC launch-path wrappers and registries (A74 cx3r005, A77 cx3r006, A80 cx3r007; launch registry cx3r006 '
                                    '3c42ca07, retired 47023c27 and c5abc2d5) and the calibration orchestrator items are registered in the NGC freeze, the miss-reading '
                                    'prereg or the calibration lane, not in this text; only their V007-facing parts (A64 coverage, A66 N-test consequence, A80\'s compare '
                                    'items) are integrated here.', 'A60', 'A61', 'A63', 'A65', 'A66', 'A74', 'A77', 'A80', '0580')
    doc['seal_slots'] = slots
    doc['binding_inputs_superseded_r2'] = superseded
    doc['supersedes_draft'] = {'path': str(R2), 'sha256': R2_SHA}
    # ------------------------------------------------------------------ root items
    RES = {'RI-01': 'A58 RI-01 (r5) with the A72 branch: driver slot PENDING', 'RI-03': 'A58 RI-03 (rules; DOUBLING at 128/256 required)', 'RI-05': 'A58 RI-05',
           'RI-06': 'A58 RI-06 (partition)', 'RI-09': 'A58 RI-09 (restated UNTESTED)', 'RI-10': 'A58 RI-10 (adoption rule; IMPL list quoted in the seal record)',
           'RI-11': 'A58 RI-11', 'RI-12': 'A58 RI-12 and A59 (replace mode)', 'RI-13': 'A58 (Claude2 R2/R3 superseded)', 'RI-17': 'A58 RI-17, then superseded by A64.2 (NGC [2, 91])',
           'RI-18': 'A58 RI-18 (cap removed)'}
    ri = []
    for r in doc['root_items']:
        r = dict(r)
        if r['status'] == 'OPEN' and r['id'] in RES:
            r['status'] = 'RESOLVED: ' + RES[r['id']]
        ri.append(r)
    def item(i, kind, clause, issue, draft, rec, *sources):
        ri.append({'id': i, 'kind': kind, 'clause': clause, 'issue': issue, 'draft': draft, 'recommendation': 'RECOMMENDATION ONLY: ' + rec, 'sources': list(sources), 'status': 'OPEN'})
    item('RI-19', 'CONFLICT (log vs dispatch)', 'seal_record_requirements[publication order]', 'A72 records H-01 as "its sha goes in the seal record". Dispatch 0561 '
         '(15:55Z) adopted the acyclic form instead (SEAL_RECORD, then the config pinning it, then a separate receipt naming both), and FORMAT_V004 / RUNBOOK_V005 '
         'implement 0561. No A-entry logs 0561.', 'follows 0561 / FORMAT_V004 / RUNBOOK_V005.', 'log 0561 as the A-entry of record (an erratum to A72 H-01), so the '
         'frozen addendum states the order the seal uses.', 'A72 (H-01)', '0561', 'FORMAT_V004')
    item('RI-20', 'PENDING INPUT', 'seal_slots.compare', 'A79/A80: r10 is frozen and superseded for the seal; r11 (or r12) is the final round. RI-10\'s rule covers NEW-21 to '
         'NEW-29 by name; later NEW items (31, 45, 47, 61, 64, 67) were ruled one by one.', 'compare slot PENDING with the round named by A80.', 'apply RI-10\'s '
         'adoption rule to every NEW item the final IMPL declares, have that IMPL list each with its disposition and its MUST_FAIL tests (A75), and quote the list in the '
         'seal record; seal on the round whose three recheck lenses and the distinct reviews of record (Claude3, Codex2) report 0 blocking.', 'A58 RI-10', 'A75', 'A79', 'A80', '0582')
    item('RI-21', 'PENDING INPUT', 'seal_slots.identity_comparator, seal_slots.identity_gate_records', 'c2v004-c2v006 are superseded (A68, A70, A76); c2v007 carries B-ID, '
         'SF-ARGV, SF-NN and the A73/A74 items; its records directory is empty at assembly. The r4 records (A76) are not seal records (A67 N1).',
         'slots PENDING.', 'slot the c2v007-lineage round whose own check and Codex2\'s review report 0 blocking, and take as records of record only its outputs on the '
         'driver slot\'s identity runs, with the A59 replace-mode tokens and the raw successor-custody check.', 'A67 N1', 'A68', 'A70', 'A74', 'A76')
    item('RI-22', 'UNDEFINED (format)', 'gates.DOUBLING', 'A73 leaves the merged DOUBLING record format pending (FIELDS_R7/R8 shape with both halves).',
         'requires one merged record with the A73 fields, registered before the seal.', 'one merged record: DDO half (K_big {128, 256}, gas M_s 128, max change over '
         'tau per static row of saved C4R3 le3, <= tau/20) and NGC half (operator e6453d52, K_big 32, NQ max change over theta, <= theta/20); both halves must pass; the '
         'compare reads it as one gate; its sha is registered before the seal.', 'A58 RI-03', 'A73', 'A79 NEW-61')
    item('RI-23', 'CONDITIONAL RULING NEEDED', 'fixed_across_all_cases.production_tail.gas (NGC)', 'A64.2: if GQ_NGC at M_s 96 does not hold to 91 /kpc, root rules on M_s '
         '128. No GQ_NGC record to 91 is registered at assembly, and LO_NGC to 91 is absent (Codex1 0049).', 'names both branches.', 'if GQ_NGC at M_s 96 fails anywhere '
         'on [2, 91], set NGC gas M_s 128 (as A57 did for DDO) and recompute LO_NGC and DOUBLING\'s NGC half at that M_s; read no NGC N-test until LO_NGC, EPS_NGC and GQ_NGC '
         'to 91 are all slotted.', 'A64.2', 'A57', 'Codex1 0049')
    item('RI-24', 'UNDEFINED (r6 branch details)', 'fixed_across_all_cases.production_tail.tail_table_cache', 'A72.3 says the T-cases run "with the cache" if r6 is adopted, '
         'but no rule says where the cache lives, whether it may be pre-warmed before launch, or how a T-run proves it used it. Codex1 waits for the r6 BUILD and cache policy.',
         'states A72 as ruled; equal footing; no mixed drivers.', 'the r6 BUILD names the cache directory policy; the seal record names it; every T-run records its cache '
         'mode and the compare refuses a T-run whose mode differs from the registered one; no T-run starts before the seal names the driver, and every T-run\'s '
         'driver_sha256 equals the driver slot (extending A67 N1 to T-runs).', 'A72', 'A67 N1', 'Codex1 0047')
    item('RI-25', 'GAP (binding)', 'seal_slots.launch_packet', 'Launcher v007 checks the plan\'s internal pins against bytes and binds the plan\'s driver and frozen-addendum '
         'pins to the seal (C4-S1). Nothing in code compares the bound plan with the template it came from (its template_pin is recorded, not checked) or with a sealed '
         'sha, so which specs and caps are launched is bound to the seal only by procedure.', 'launch-packet slot names the bound plan and command as PENDING parts.',
         'name the bound plan and command shas in the SEAL_RECORD (or the receipt) and have root verify them from bytes immediately before running the command; '
         'optionally, have validate() require that the bound plan equals its pinned template outside the three binding fields.', 'A78', '0576', 'Claude4 0079')
    item('RI-26', 'PROCEDURE', 'decision_pins_pending_at_seal', 'This text cites A47-A80 by name; the frozen copy is made at seal assembly (0576), possibly after further '
         'entries, and the open addendum changed twice while r3 was assembled (reads 03120f0a, 4b937ec1).', 'cites by name; frozen copy PENDING.', 'freeze after the last '
         'pre-seal entry, and have the seal check verify that every entry this text cites is present in the frozen bytes; any entry after A80 that touches this text needs '
         'an r4 or an explicit no-change note.', '0576', 'A47-A80')
    ri.sort(key=lambda r: (r['status'] != 'OPEN', r['id']))
    doc['root_items'] = ri
    # ------------------------------------------------------------------ checklist
    check = [
        ('Freeze the V005 addendum (exclusive-create ..._V005_ADDENDUM_FROZEN.md) at seal assembly and pin it here and in the compare (PIN_ADDENDUM_V005).', 'PENDING', '0576; A67'),
        ('Root rulings on the OPEN root items (%s).' % ', '.join(r['id'] for r in ri if r['status'] == 'OPEN'), 'PENDING', 'ROOT_ITEMS_R3'),
        ('A72 branch: decide r5 or r6 on conditions (a)-(c); if r6: r6 BUILD and cascade map published, r6 template and bound plan, identity reruns on r6 with the cache.', 'PENDING', 'A72'),
        ('Driver r5 built (b5cc62af); dry runs 25/25 with 0 blockers; Codex3 cross-lineage review PASS_WITH_FINDINGS (A69). A Claude-lineage independent check, '
         'driver_r5/check/CHECK.md (%s), reads PASS_WITH_FINDINGS (on disk at assembly, not yet logged in an A-entry).' % r5check['sha256'][:8], 'DONE', 'A67; A69; driver_r5/check'),
        ('CASCADE_MAP_R5_ADDENDUM (immutable inventory addendum) written, if the driver slot is r5.', 'PENDING', 'A69'),
        ('Identity runs on the driver slot compared by the c2v007-lineage comparator (Z2 with A59 replace-mode tokens, Z2_OFF_RO1, B0P_RERUN); records of record emitted.', 'PENDING', 'A67; A74; A76'),
        ('B3 final: PASS (Claude4 0060, GATE_B3_C4_V002 465cb3c3).', 'DONE', 'R1 B3; 0509'),
        ('Final compare round r11 (or r12): A79.1-6, A75 in full, A77.2, A73 F2, the r10 recheck items, A71, A68 CHK-1, A69, RI-10 dispositions; three recheck lenses; distinct reviews of record by Claude3 and Codex2.', 'PENDING (r11 building)', 'A79; A80; 0582; A75'),
        ('Compare r8 and r10: superseded for the seal (r10 frozen e801adc4; both r10 rechecks FAIL: order 4 blocking, validity 2 blocking).', 'SUPERSEDED', 'A79; A80'),
        ('Run `--gates-only` and `--validity-only --case C5H` on the real records with the sealed compare; paste their output; state that no row value was shown.', 'PENDING', 'A46 RA13; A47 I3'),
        ('PICARD member successor specs (A53 shape) with B0 EXT evidence: gates_v004 PASS (18/18 leaves; 10/10 negative controls).', 'DONE', 'A68'),
        ('Certificates DDO: EPS_CERT_V006 598c8fa3 (retained), LO_CERT_V004_MS128 1c384f76 (PASS_WITH_FINDINGS), GQ_CERT_V005_MS128 fbceefe6 (PASS; V004 FAIL control).', 'DONE (root confirms slots)', 'A67 SF2; A68; A70; A73'),
        ('Certificates NGC at K_big 32: EPS_NGC91 (admission test passed), LO_NGC to 91 (absent; sole N-test blocker), GQ_NGC to 91 (with Codex1).', 'PENDING', 'A64.2; A70; Codex1 0049'),
        ('DOUBLING merged record (DDO half PASS at 128/256, max 4.7e-13 tau; NGC half from NQ at 32).', 'PENDING (format)', 'A58 RI-03; A73'),
        ('P128/M_s 128 spec set registered (SPEC_REGISTRY_R5_MS128_CX1V004 c7023846), dry-run 10/10, case block accepted.', 'DONE', 'A72 (packet final); A78'),
        ('Launch packet BUILD_V005 (46bc5b5d): ramp gate, admission, outputs and aggregate fixes reviewed PASS (Claude4 0079).', 'DONE', 'A78; Claude4 0079'),
        ('Bound plan and command written by the binder from the selected template, the driver slot and the frozen addendum (exclusive create).', 'PENDING', '0576; A78'),
        ('Root admission config names the BUILD_V005 launcher and guard sources exactly.', 'PENDING', 'A78 N2'),
        ('Publication order: freeze, bind, SEAL_RECORD, config, receipt; numbered root packet; UNT_ROOT_ADMISSION_SHA256 exported from the published value.', 'PENDING', '0561; 0576; RUNBOOK_V005'),
        ('Producer registry with producer paths, producer shas and gate-record shas of record (PIN_PRODUCER_REGISTRY).', 'PENDING', 'A62.2; A67 N2; A69.1'),
        ('Key-equivalence map in the seal record.', 'PENDING', 'A48 AMB-13'),
        ('Seal-record disclosures and quotes: E5-08, raw successor custody, the NEW-item disposition list.', 'PENDING', 'A62; A59; A58 RI-10'),
        ('Successor B0 tool and B0 record rerun (B0-EMPTY rule) on the driver slot.', 'PENDING (no A-entry records completion)', 'A54; 0530'),
        ('r2 checklist item "identity runs compared by c2v004": superseded by the c2v007 lineage.', 'SUPERSEDED', 'A68; A70; A76'),
    ]
    # ------------------------------------------------------------------ write
    out = Path(os.environ['DRY_DIR']) if os.environ.get('DRY_DIR') else OUT
    out.mkdir(parents=True, exist_ok=True)

    def write(name, text):
        p = out / name
        with p.open('x') as f:
            f.write(text)
        return p
    write('KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R3.json', json.dumps(doc, indent=1, ensure_ascii=False) + '\n')
    rows = []

    def walk(prefix, obj):
        if isinstance(obj, dict) and 'text' in obj and 'sources' in obj:
            rows.append((prefix, obj['sources']))
            return
        if isinstance(obj, dict):
            for k, v in obj.items():
                walk(prefix + '.' + k if prefix else k, v)
    for sec in ('binding_inputs', 'fixed_across_all_cases', 'pairing_and_decidability_rule', 'gates_before_any_T_result', 'tests', 'decision_rule', 'run_list'):
        walk(sec, doc[sec])
    for o in doc['outcomes_first_applicable']:
        rows.append(('outcomes_first_applicable.%s' % o['outcome'], o['sources']))
    for i, r in enumerate(doc['outcome_reading_rules']):
        rows.append(('outcome_reading_rules[%d]' % i, r['sources']))
    for i, r in enumerate(doc['seal_record_requirements']):
        rows.append(('seal_record_requirements[%d]' % i, r['sources']))
    rows.append(('ngc3198_N_tests', doc['ngc3198_N_tests']['sources']))
    for k, s in slots.items():
        rows.append(('seal_slots.%s' % k, s['sources']))
    rows.append(('not_v007_text_scope', doc['not_v007_text_scope']['sources']))
    cited = sorted({s for _, ss in rows for s in ss})
    entries_cited = sorted({m for s in cited for m in re.findall(r'A\d{2}', s)}, key=lambda a: int(a[1:]))
    M = ['# Clause → source map, r3: KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R3 (unsealed)', '',
         'Every clause in the r3 JSON carries its sources. "R1" means the clause text is R1\'s, unchanged or extended.', '',
         'A-entries since r2 cited by at least one clause: %s.' % ', '.join(a for a in entries_cited if int(a[1:]) >= 58), '',
         '| clause | sources |', '|---|---|']
    M += ['| `%s` | %s |' % (k, '; '.join(s)) for k, s in rows]
    write('CLAUSE_SOURCE_MAP_R3.md', '\n'.join(M) + '\n')
    D = ['# Delta r2 → r3 (KMAX_TAIL_PREREG_V007_FINAL_DRAFT)', '', 'Each line is one recorded edit applied to r2 (58a0b87d) by the r3 generator.', '',
         '| # | clause | kind | added sources | why |', '|---|---|---|---|---|']
    D += ['| %d | `%s` | %s | %s | %s |' % (i + 1, c['clause'], c['kind'], '; '.join(c['added_sources']), c['why']) for i, c in enumerate(changes)]
    write('DELTA_R2_R3.md', '\n'.join(D) + '\n')
    Rr = ['# Root items r3: KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R3 (unsealed)', '',
          'Every r2 item with its status after A58-A80, then the items still open. For each open item the draft\'s current handling and a recommended ruling are given; '
          'the recommendations are recommendations only, not root text.', '']
    for r in ri:
        Rr += ['## %s: %s (%s)' % (r['id'], r['kind'], 'OPEN' if r['status'] == 'OPEN' else 'RESOLVED'), '', '- **Status:** %s' % r['status'], '- **Clause:** `%s`' % r['clause'],
               '- **Issue:** %s' % r['issue'], '- **Draft:** %s' % r['draft']]
        if 'recommendation' in r:
            Rr.append('- **Recommendation:** %s' % r['recommendation'])
        Rr += ['- **Sources:** %s' % '; '.join(r['sources']), '']
    write('ROOT_ITEMS_R3.md', '\n'.join(Rr))
    S = ['# SEAL_CHECKLIST r3: V007 (for root; the draft is unsealed)', '', 'State at assembly (%s). DONE, PENDING or SUPERSEDED, each with its source.' % ts, '',
         '| # | step | state | source |', '|---|---|---|---|']
    S += ['| %d | %s | %s | %s |' % (i + 1, a, b, c) for i, (a, b, c) in enumerate(check)]
    write('SEAL_CHECKLIST_R3.md', '\n'.join(S) + '\n')
    H = ['# KMAX_TAIL_PREREG_V007: final draft r3 (UNSEALED)', '', doc['status'], '',
         '**Assembly:** Claude4, single author, UTC %s. Base: r2 `%s`. Dispatch 0580 `%s`. V005 addendum observed `%s` (open).' % (ts, R2_SHA, disp['0580']['sha256'], v005_observed), '']

    def render(title, d):
        H.extend(['## ' + title, ''])
        for k, v in d.items():
            if isinstance(v, dict) and 'text' in v:
                H.append('- **%s**: %s  \n  *Sources: %s*' % (k, v['text'], '; '.join(v['sources'])))
            elif isinstance(v, dict) and 'sha256' in v:
                H.append('- **%s**: `%s` (`%s`)' % (k, v['path'], v['sha256']))
            elif isinstance(v, dict):
                H.append('- **%s:**' % k)
                for k2, v2 in v.items():
                    if isinstance(v2, dict) and 'text' in v2:
                        H.append('  - **%s**: %s  \n    *Sources: %s*' % (k2, v2['text'], '; '.join(v2['sources'])))
                    elif isinstance(v2, dict) and 'sha256' in v2:
                        H.append('  - **%s**: `%s` (`%s`)' % (k2, Path(v2['path']).name, v2['sha256']))
                    else:
                        H.append('  - **%s**: %s' % (k2, json.dumps(v2, ensure_ascii=False) if not isinstance(v2, str) else v2))
            else:
                H.append('- **%s**: %s' % (k, v))
        H.append('')
    H.extend(['## Seal slots (root fills at seal assembly; never guessed)', ''])
    for k, s in slots.items():
        H.append('- **%s**: value `%s`. %s  \n  *Sources: %s*' % (k, s['value'], s['rule'], '; '.join(s['sources'])))
        if 'named_candidates_verified_from_bytes' in s:
            for k2, v2 in s['named_candidates_verified_from_bytes'].items():
                if isinstance(v2, dict) and 'sha256' in v2:
                    H.append('  - named candidate %s (verified from bytes, not the slot value): `%s` (`%s`)' % (k2, Path(v2['path']).name, v2['sha256']))
                elif isinstance(v2, dict):
                    for k3, v3 in v2.items():
                        H.append('  - named candidate %s %s (verified from bytes, not the slot value): `%s` (`%s`)' % (k2, k3, Path(v3['path']).name, v3['sha256']))
                else:
                    H.append('  - %s: %s' % (k2, v2))
    H.append('')
    render('Binding inputs (sha256 from bytes at assembly)', doc['binding_inputs'])
    render('Fixed across all cases', doc['fixed_across_all_cases'])
    render('Pairing and decidability', doc['pairing_and_decidability_rule'])
    render('Gates before any T result', doc['gates_before_any_T_result'])
    render('Tests', doc['tests'])
    render('Decision rule', doc['decision_rule'])
    H.extend(['## Outcomes, first applicable', ''])
    for o in doc['outcomes_first_applicable']:
        H.append('- **[%s] %s**: %s  \n  *Sources: %s*' % (o['position'], o['outcome'], o['text'], '; '.join(o['sources'])))
    H.extend(['', '**Reading rules:**', ''])
    for r in doc['outcome_reading_rules']:
        H.append('- %s *(%s)*' % (r['text'], '; '.join(r['sources'])))
    H.extend(['', '## NGC3198 N-tests', ''])
    for k, v in doc['ngc3198_N_tests'].items():
        H.append('- **%s**: %s' % (k, json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v))
    render('Run list', doc['run_list'])
    H.extend(['## Seal record requirements', ''])
    for r in doc['seal_record_requirements']:
        H.append('- %s *(%s)*' % (r['text'], '; '.join(r['sources'])))
    H.extend(['', '## Scope UNTESTED', ''] + ['- ' + s for s in doc['scope_untested']])
    H.extend(['', '## Not V007 text', '', '- %s *(%s)*' % (doc['not_v007_text_scope']['text'], '; '.join(doc['not_v007_text_scope']['sources']))])
    H.extend(['', '## Root items', '', 'See `ROOT_ITEMS_R3.md`. OPEN: %s.' % ', '.join(r['id'] for r in ri if r['status'] == 'OPEN'), ''])
    write('KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R3.md', '\n'.join(H) + '\n')
    hrows = ['%s  ./%s' % (sha(p), p.relative_to(out)) for p in sorted(out.rglob('*')) if p.is_file() and p.name != 'HASHES_R3.txt']
    write('HASHES_R3.txt', '\n'.join(hrows) + '\n')
    print('written', out, len(hrows), 'files; V005 observed', v005_observed, 'A80 present:', has_a80, '; edits', len(changes), '; open RIs',
          [r['id'] for r in ri if r['status'] == 'OPEN'])


if __name__ == '__main__':
    main()

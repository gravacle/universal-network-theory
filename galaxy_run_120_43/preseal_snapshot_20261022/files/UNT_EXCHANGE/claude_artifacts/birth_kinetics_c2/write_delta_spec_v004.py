"""Write WORM_BIRTHK_PILOT_DELTA_SPEC_V004.json (exclusive 'x'); every pin is computed from bytes.

Usage: python3 -I -B write_delta_spec_v004.py
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

H = Path(__file__).resolve().parent
UPC = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13')
W3 = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/worm_move_c2_0467')
E = UPC / 'CLAUDE2/WORM_PILOT_EVALUATION_2026-10-17_V001'
RUN = UPC / 'CODEX1/OWNED_L4_WORM_BIRTHK_RUN_V001'
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'


def pin(p):
    p = Path(p)
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}


def main():
    assert not RUN.exists()
    fx = json.loads((H / 'BIRTH_RESIDENCE_FIXTURE_RESULTS_C2V002.json').read_text())
    nx = json.loads((H / 'BIRTH_RESIDENCE_NATIVE_EXPLICIT_CHECK_C2V002.json').read_text())
    F = fx['F1_F2_exact_kernel_and_forward_reverse']
    summary = {
        'F1_cases': len(F), 'F1_paths': sum(c['paths_in_closed_set'] for c in F),
        'F1_offdiagonal_transitions': sum(c['offdiagonal_transitions'] for c in F),
        'F1_max_relative_detailed_balance_error': max(c['max_relative_detailed_balance_error'] for c in F),
        'F1_max_oracle_difference': max(c['max_abs_oracle_kernel_difference'] for c in F),
        'F1_legal_proposals_with_changed_channel_bearing_count': sum(c['legal_proposals_with_changed_channel_bearing_count'] for c in F),
        'F1_reference_states_with_empty_channel_bearing_set': sum(c['reference_states_without_any_channel_bearing_owner'] for c in F),
        'F2_forward_plus_reverse_log_mh_all_exactly_zero': all(c['forward_reverse']['all_exactly_zero'] for c in F),
        'F2_reversed_proposals': sum(c['forward_reverse']['legal_proposals_reversed'] for c in F),
        'F5_interruption_checkpoints': fx['F3_F4_F5_guards_replay_interruption']['F5_interruption']['checkpoints_in_accepted_eventful_move'],
        'F6_caught': {k: v['caught'] for k, v in fx['F6_mutants_and_controls'].items()},
        'F7_no_owner_self_loop_probability': fx['F7_no_owner_self_loop_probability'],
        'native_C1': [{k: c[k] for k in ('state', 'active_slots', 'owners_with_birth_mark_S', 'v001_empty_owner_fraction',
                                          'birth_marks_by_kind', 'owners_whose_union_partition_differs_from_per_owner_or_full',
                                          'seconds_union_call')}
                      for c in nx['C1_union_partition_equals_per_owner_rosters']],
        'native_C2_changed_reversed_exactly': sum(c['changed_reversed_exactly_with_zero_log_mh_sum']
                                                  for c in nx['C2_module_on_native_explicit_paths_via_shim'])}
    spec = {
        'utc': datetime.now(timezone.utc).isoformat(),
        'status': 'IMPLEMENTED_AWAITING_DISTINCT_REVIEW_ROOT_LAUNCH_ONLY',
        'author': 'Claude2 lane birth_kinetics_c2',
        'authority': {
            'evaluation': pin(E / 'WORM_PILOT_EVALUATION_V001.md'), 'evaluation_json': pin(E / 'WORM_PILOT_EVALUATION_V001.json'),
            'binding_review': pin(E / 'review/REVIEW_V001.md'),
            'section': '7 Recommendation: next remedy, Birth kinetics and run length',
            'binding_corrections_applied': [
                'that census/U slowness causes the residual R/S failure is UNTESTED (review, section 7 row): no such claim is made; the deciding tests decide',
                'Birth wastes 81.7%/80.0% of attempts on empty_reference_owner (1284/1572, 1248/1560) and accepts 213/223: counts CONFIRMED, used as motivation only',
                'the 6-chain-pool and gate-margin reasons were dropped by the review; nothing here relies on them']},
        'one_correction': ('Replace ONLY the Birth-residence transport in the .20 Birth slot (u in [2/15,6/15) of the .75 base '
                           'wrapper) by c2v002: owner uniform among owners WITH a Birth/reverse mark at the reference dwell, '
                           'exact owner-count Hastings factor; warmup doubled to 1024 (1024 measurements); fresh seed '
                           '2026101702; time-proportional caps scaled x2 with the hard wall 9000 s. Same native target, '
                           'weights, reads, criteria, worm slot and durability V002.'),
        'predecessor_packet': {
            'recipe_v003': pin(W3 / 'owned_L4_worm_loop_recipe_v003.py'),
            'worker_v003': pin(W3 / 'owned_L4_worm_loop_root_worker_v003.py'),
            'monitor_v003': pin(W3 / 'owned_L4_worm_loop_monitor_v003.py'),
            'durability_v002_unchanged': pin(W3 / 'owned_worm_committed_capture_durability_v002.py'),
            'worm_module_unchanged': pin(W3 / 'owned_worm_loop_whole_path_c2v001.py'),
            'spec_v003': pin(W3 / 'WORM_LOOP_PILOT_DELTA_SPEC_V003.json'),
            'birth_transport_replaced': pin(UPC / 'helpers/coefficient_method/owned_worldline_birth_residence_transport_v001.py'),
            'predecessor_run': str(UPC / 'CODEX1/OWNED_L4_WORM_LOOP_RUN_V001')},
        'unchanged_pins': {
            'sampler_v006': '896cadbbe4059a77b33f370d643cfa7657c0e031d61d1aa46886e88eb4f576b7',
            'operator_v003': 'a04f87954b68bb2dcc5a1af42a465b1d554ed1fc14d9b22d43e05e3e664f7f07',
            'family_recipe': '86c2ee5319dd1277c630e15ca7ab9f224027bf638a281753e68dddecf1ca6bd7',
            'admission_transport': '5b19e90ee4fcf86a0b8fe570abb607ae23c8047771abc4ab317c167f1837d653',
            'occupancy_transport': 'dedc932832ed41fbbb4661a2cfb97f127aee399f859f8ad3742f66645a8d4837',
            'adapter': '0705be7ca500a3b8329566ba014b80645231be2178ad5b8ef089dbca163b3f77',
            'statistics': '85f4c638eb28361f806421048d9adbebff3ea0f1e02237029d7e0b947342638a',
            'worm_module': '9fef6042eb1e13157d19a4d4381b4c73ef6e26d779f49ad7c477f1d44b9f470d',
            'durability_v002': 'c0646a9380ef59d1f95732faf732243f91e850ec3b94f8d3510ccdd5602b40f9'},
        'packet': [pin(H / n) for n in ('owned_worldline_birth_residence_transport_c2v002.py', 'owned_L4_worm_birthk_recipe_v004.py',
                                        'owned_L4_worm_birthk_root_worker_v004.py', 'owned_L4_worm_birthk_monitor_v004.py')],
        'delta_diffs': [pin(H / n) for n in ('DELTA_owned_worldline_birth_residence_transport_c2v002.diff',
                                             'DELTA_owned_L4_worm_birthk_recipe_v004.diff',
                                             'DELTA_owned_L4_worm_birthk_root_worker_v004.diff',
                                             'DELTA_owned_L4_worm_birthk_monitor_v004.diff')],
        'build': {'script': pin(H / 'build_worm_birthk_packet_v004.py'), 'report': pin(H / 'PACKET_BUILD_REPORT_V004.json'),
                  'edits': 'exact unique-anchor replacements listed in the build script; recipe 4, worker 7, monitor 6'},
        'fixed_proposal': {
            'reference_dwell': 'x = segments[0] (as V001)',
            'rosters': ("ONE palette enumeration at x over the union of the permanent owner groups of the fixed original A+B "
                        "roster; R(x,o) = marks with kind birth|birth_rev, owner_id[0]=='birth', owner_id[1]==o (V001's "
                        "per-owner roster); S(x) = roster-order owners with R(x,o) nonempty"),
            'selection': 'o uniform in S(x) (empty S: self loop, no draw); mark uniform in R(x,o); two integer draws as V001',
            'transform': 'V001 unchanged: the (kind, owner) mark applied in every dwell, inverse mark verified per dwell, closure checked',
            'reverse': 'from the transformed path Y: o from S(y) and the unique inverse mark of o in R(y,o), which must target x',
            'hastings': ('log MH = [log|S(x)| - log|S(y)|] + [log|R(x,o)| - log|R(y,o)|] - sum dt (D_new - D_old) '
                         '+ sum log(W_new/W_old); both counts recomputed on every proposal'),
            'contract_failures_new': ('union mark differs from the per-owner mark at x (kind, owner, W, target); union reverse mark '
                                      'differs from the per-owner inverse at y; Birth mark owner outside the fixed roster'),
            'self_loops': 'no_channel_bearing_owner, dwell_guard, inverse_guard, inverse_canonical_target, event_replay_guard_or_target, metropolis',
            'atomicity': ('read-integral sums, donor diagnostic and accepted counters written only after the before-atomic-commit '
                          'checkpoint (V001 wrote its read sums before it)')},
        'choice_ledger': [
            {'choice': 'owner drawn among channel-bearing owners at the reference dwell with the exact owner-count factor',
             'status': 'DECLARED as the reviewed recommendation (evaluation section 7)'},
            {'choice': 'one union palette enumeration gives S and every R instead of 128 per-owner enumerations',
             'status': ('DECLARED; equivalence checked natively (C1: 0 of 128 owners differ on 4 explicit states) and enforced per '
                        'proposal by the contract checks; 2 enumerations per legal attempt, as V001 (roster + reverse roster)')},
            {'choice': 'Birth mark owner outside the fixed roster = contract failure (V001 ignored such marks)',
             'status': 'DECLARED; none exists under the bound full original A+B roster (C1: 0 records)'},
            {'choice': 'union/per-owner disagreement at the reverse = contract failure (V001: reverse_selection self loop)',
             'status': 'DECLARED; under the operator palette contract the two coincide'},
            {'choice': ('time-proportional caps x2 with the hard wall: soft wall 8800 s, soft calls and max_channel_enumerations '
                        '3.2M, max_total_events 4.8M'),
             'status': ('DECLARED reading of "same caps scaled for time"; RSS 4 GiB hard / 3.5 GiB soft, output 2 GiB, '
                        'max_events_per_path 10000 unchanged')},
            {'choice': 'max_sweeps 3072 -> 4096',
             'status': 'COMPUTED: the sampler caps the total over both chains, 2 x (1024 + 1024)'},
            {'choice': ('the pinned family recipe hard-codes the soft budget (4400 s / 1.6M); worker V004 replaces the budget hook '
                        'after preparation and before sampling'),
             'status': "DECLARED; same prepared clock and guarded call counter; recorded in result['schedule_binding']"}],
        'bounds': {'wall_hard_seconds': 9000, 'wall_soft_seconds': 8800, 'combined_rss_hard_bytes': 4294967296,
                   'soft_rss_bytes': 3758096384, 'output_hard_bytes': 2147483648, 'native_channel_call_cap': 3200000,
                   'event_cap': 4800000, 'max_sweeps': 4096, 'max_events_per_path': 10000},
        'pilot': {'chains': 2, 'warmup_per_chain': 1024, 'measurements_per_chain': 1024, 'moves_per_sweep': 5,
                  'fresh_seed': 2026101702,
                  'mixture': {'current_graph_occupancy': .25, 'worm_loop': .10, 'Birth_residence_c2v002': .20,
                              'admission_residence': .20, 'prior_base': .25},
                  'output_directory': str(RUN), 'output_directory_absent_at_spec': True, 'root_launch_only': True,
                  'scientific_run_launched_by_helper': False,
                  'launch_argv': [PY, '-I', '-B', str(H / 'owned_L4_worm_birthk_monitor_v004.py')],
                  'threads': 'monitor sets OMP/OPENBLAS/MKL/NUMEXPR/VECLIB/BLIS_NUM_THREADS=1 (unchanged)'},
        'capture': {'unchanged': 'durability V002: 16-row committed blocks plus reference key, Birth census and U per row'},
        'deciding_tests': {
            'mixing': 'unchanged: every one of the 36 all-k blocks and the background with Rhat<=1.1 AND 128/tau>=5',
            'census_and_U': 'the census/U two-part rule (Rhat<=1.1 and 128/tau>=5 on time_mean_active_slots and time_mean_U) with flat quarter means',
            'topology': 'born edges shared between the chains rising toward the within-chain lag-512 overlap (evaluation section 5 measures)',
            'transport_counters': ('birth_residence_attempts, _channel_bearing_owner_count_sum, _no_channel_bearing_owner, '
                                   '_legal_transport, _owner_count_ratio_nonunit, _log_mh_negative, _metropolis, _accepted_changed, '
                                   'birth/birth_rev selected and accepted, guard counters, read-integral changes; full-chain and '
                                   'measurement_ scope')},
        'verification': {
            'fixture': pin(H / 'birth_residence_fixture_c2v002.py'), 'toy_library': pin(H / 'birth_fixture_toy_c2v002.py'),
            'fixture_results': pin(H / 'BIRTH_RESIDENCE_FIXTURE_RESULTS_C2V002.json'),
            'native_check': pin(H / 'birth_residence_native_explicit_check_c2v002.py'),
            'native_results': pin(H / 'BIRTH_RESIDENCE_NATIVE_EXPLICIT_CHECK_C2V002.json'),
            'packet_check': pin(H / 'packet_delta_check_v004.py'),
            'packet_check_results': pin(H / 'PACKET_DELTA_CHECK_V004.json'),
            'summary': summary},
        'cost_estimate': ('per Birth attempt 1 union enumeration (0.015-0.03 s on saturated explicit states, 0.17-0.18 s near the '
                          'seed) plus the V001 transform; per legal transform 1 more union enumeration. V003 measured 1765 s for '
                          '3072 sweeps; V004 runs 4096 sweeps and turns about 80% of Birth attempts from cheap self loops into '
                          'transforms. Explicit-state estimate, not a measurement of the pilot; expected well inside the 8800 s soft wall.'),
        'interpretation_limits': [
            'No physical rate, new Hamiltonian term, altered worldline measure or modified owned labels.',
            'No claim that census/U slowness causes the residual R/S failure (UNTESTED per the review); the deciding tests decide.',
            'On saturated explicit native states only reverse Birth marks exist (C1); the move lowers the census there and births re-raise it.',
            'No ergodicity or mixing claim; accepted-move counts alone are insufficient.',
            'Fresh seed: an independent bounded pilot, not a paired comparison with OWNED_L4_WORM_LOOP_RUN_V001.']}
    with (H / 'WORM_BIRTHK_PILOT_DELTA_SPEC_V004.json').open('x') as f:
        json.dump(spec, f, indent=1)
        f.write('\n')
    print(json.dumps({'ok': True, 'F6_caught': summary['F6_caught']}))


if __name__ == '__main__':
    main()

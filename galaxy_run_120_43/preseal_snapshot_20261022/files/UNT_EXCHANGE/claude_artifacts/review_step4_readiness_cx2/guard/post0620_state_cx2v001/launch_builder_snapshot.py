# Claude4 helper, dispatch 0587 parts (a)-(e): assemble LAUNCH_ORDER_C4V001.json from the work records in this folder.
# Every number is read from a pinned work record (reconcile v002, schedule sim v002, registry probe v002); every source
# sha256 is read from work/SOURCE_PINS_C4V001.txt (written by shasum) or recomputed here from bytes.
# Usage: python3 -I -B build_launch_order_c4v001.py <new output json>
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fence_c4v001 as F
import hashlib, json, datetime

LO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S4 = os.path.dirname(LO)


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def pin(p):
    return {'path': p, 'sha256': sha_file(p)}


def load(p):
    with open(p, 'rb') as f:
        return json.loads(f.read())


def main(out):
    utc = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    rec_p = LO + '/work/RECONCILE_C4V002.json'
    sim_p = LO + '/work/SCHEDULE_SIM_C4V002.json'
    prb_p = LO + '/work/registry_probe_v002/REGISTRY_GROWTH_PROBE_C4V002.json'
    pins_p = LO + '/work/SOURCE_PINS_C4V001.txt'
    R = load(rec_p)
    S = load(sim_p)
    P = load(prb_p)
    src = {}
    with open(pins_p) as f:
        lines = f.read().splitlines()
    pins_utc = lines[0]
    for ln in lines[1:]:
        h, p = ln.split('  ', 1)
        src[p] = h
    add_p = LO + '/work/SOURCE_PINS_C4V002_ADDITIONS.txt'
    with open(add_p) as f:
        add = f.read().splitlines()
    for ln in add[1:]:
        h, p = ln.split('  ', 1)
        src[p] = h
    B = S['batches']
    C = S['campaign']
    MX = S['mixed_queue']

    def b(k):
        v = B[k]
        return {'makespan_h': v['makespan_h'], 'per_call_wall_h_min_max': v['per_call_wall_h_min_max'],
                'max_route_a': v['max_route_a'], 'max_busy_processes': v['max_demand'], 'min_free_percent_modelled': round(v['min_free_percent'], 1)}

    def c(k):
        v = C[k]
        return {'makespan_h': v['makespan_h'], 'makespan_days': v['makespan_days'], 'max_wave_span_h': v['max_wave_span_h'],
                'calls_starting_after_48h_wave_cap': v.get('calls_starting_after_48h_wave_cap'),
                'max_route_a': v['max_route_a'], 'min_free_percent_modelled': round(v['min_free_percent'], 1)}

    pc = S['per_call']
    wall = {
        'label': 'UNTESTED projections from measured inputs (TIMING_V003 build rows and tail-OFF stage receipts; projection_c2v001 route-A '
                 'iterations at N=8). Arithmetic TESTED (work/SCHEDULE_SIM_C4V002.json, deterministic).',
        'per_run_solo_h': {
            'TAIL_ON_C4T_LIKE': {'runs': 'S4-RA, S4-W8, S4-CAP-TRIAL, S4-CAP-C000..C111, S4-SENS-* (18), every campaign call, S4-POST-S1',
                                 'E_I7_P3': pc['TIMING_V003_as_is']['C4T_E_solo_h'], 'U_I32_P6_TIMING_V003_as_is': pc['TIMING_V003_as_is']['C4T_U_solo_h'],
                                 'U_I32_P6_route_A_baseline_scaled': pc['TAIL_ON_U_ADJ']['solo_h'],
                                 'route_A_phase_h': {'E': pc['TAIL_ON_E']['route_a_phase_h'], 'U': pc['TAIL_ON_U_ADJ']['route_a_phase_h']},
                                 'first_iteration_completed_after_start_min': pc['TAIL_ON_E']['first_iteration_solo_min'],
                                 'if_r6_cache_UNTESTED_and_moot_A96': {'E': pc['TIMING_V003_as_is']['cached_r6_C4T_E_solo_h_UNTESTED'],
                                                                      'U': pc['TIMING_V003_as_is']['cached_r6_C4T_U_solo_h_UNTESTED']}},
            'TAIL_OFF_DIII': {'runs': 'S4-DIII-LO-REF/NEW, S4-DIII-HI-REF/NEW', 'E_I7_P3': pc['TIMING_V003_as_is']['tail_off_E_solo_h'],
                              'U_I32_P6_TIMING_V003_as_is': pc['TIMING_V003_as_is']['tail_off_U_solo_h'],
                              'U_I32_P6_route_A_baseline_scaled': pc['TAIL_OFF_U_ADJ']['solo_h'],
                              'route_A_phase_h': {'E': pc['TAIL_OFF_E']['route_a_phase_h'], 'U': pc['TAIL_OFF_U_ADJ']['route_a_phase_h']},
                              'first_iteration_completed_after_start_min': pc['TAIL_OFF_E']['first_iteration_solo_min']},
            'under_today_load_factor': {'rows': pc['TIMING_V003_as_is']['wall_ratio_under_load_rows'], 'mean': pc['TIMING_V003_as_is']['mean_wall_ratio'],
                                        'note': 'TIMING_V003 load calibration: same build, wall/solo, at load average 20-60 on 18 cores'},
            'arithmetic': [
                'tail-OFF E = 10702.18 (C4R3 receipt, offset..le3) + 2786.09 (C4_V005 reference) + 600.19 (C4_V005 body) + [1014.9, 1040.8] '
                '(route A, 8 workers = 375.1 prep + 7 x [91.4, 95.1] s/iteration, projection_c2v001) = [15103.4, 15129.3] s = 4.20 h',
                'tail-ON E = tail-OFF E + 3581.0 s tail (route-A side 2 x 285 cold + 7 x 111 warm = 1347; route-B side 2234.0) = [18684.4, 18710.3] s = 5.19-5.20 h',
                'tail-ON U (TIMING_V003 as-is) = 17052.9 (le3 + 3 x 2116.9 extra passes) + 2786.09 + 600.19 + [1014.9, 1040.8] + 7709.6 '
                '(route-A side 2 x 285 + 32 x 111 = 4122; route-B side 3587.6) = [29163.7, 29189.6] s = 8.10-8.11 h',
                'TIMING_V003 keeps the I=7 route-A baseline in its I=32 total; scaling it adds 25 x [91.4, 95.1] = [2285, 2377.5] s: '
                'tail-ON U = [31449, 31567] s = 8.74-8.77 h (used: 8.75 h, mean iteration 93.25 s); tail-OFF U = 6.59-6.63 h (used 6.61 h)',
                'route-A tail build per call at 6 iterations (COST_MODEL_CX2V001, M_s 64 rows): K64 271.1 s = 4.5 min, K128 905.4 s = 15.1 min '
                '(A55 text); at M_s 128 TIMING_V003 measured the same K128 cold cost (285 s solo), so the M_s 64 row stands for M_s 128'],
        },
        'measured_completed_runs_cited': {
            'label': 'cited from root text, not re-measured; receipts not opened (runs_ext and UVT_* names are out of bounds for this part)',
            'rows': [
                {'run': 'r5 identity rerun B0P_RERUN (admitted route-A prefix)', 'start': '14:56Z (A67)', 'end': '17:49Z (A92)', 'wall_h': 2.88},
                {'run': 'r5 identity rerun Z2_OFF_RO1 (tail-OFF, N8, at the anchor)', 'start': '14:56Z (A67)', 'end': '18:25Z (A92)', 'wall_h': 3.48},
                {'run': 'r5 identity rerun Z2 (tail-ON code path, empty tail domain, N8)', 'start': '14:56Z (A67)', 'end': '18:26Z (A92)', 'wall_h': 3.50}],
            'reading': 'Three calls ran concurrently with other lane load; their walls sit below the 4.20 h tail-OFF projection, so the '
                       'projection is not optimistic for tail-OFF calls on this grid (comparability of numerics UNTESTED).'},
        'batches_ramp_RA3_18_cores': {
            'DIII_4': {'E': b('DIII_4|E|RAMP_RA3|cores18'), 'U': b('DIII_4|U_ADJ|RAMP_RA3|cores18')},
            'HEADLINE_10_default': {'E': b('HEADLINE_10|E|RAMP_RA3|cores18'), 'U': b('HEADLINE_10|U_ADJ|RAMP_RA3|cores18')},
            'HEADLINE_9_if_DU1': {'E': b('HEADLINE_9|E|RAMP_RA3|cores18'), 'U': b('HEADLINE_9|U_ADJ|RAMP_RA3|cores18')},
            'HEADLINE_11_no_dual_use': {'E': b('HEADLINE_11|E|RAMP_RA3|cores18'), 'U': b('HEADLINE_11|U_ADJ|RAMP_RA3|cores18')},
            'SENS_18_both_D': {'E': b('SENS_18_BOTH_D|E|RAMP_RA3|cores18'), 'U': b('SENS_18_BOTH_D|U_ADJ|RAMP_RA3|cores18')},
            'SENS_9_one_D': {'E': b('SENS_9_ONE_D|E|RAMP_RA3|cores18'), 'U': b('SENS_9_ONE_D|U_ADJ|RAMP_RA3|cores18')},
            'POST_S1_2': {'E': b('POST_S1_2|E|RAMP_RA3|cores18'), 'U': b('POST_S1_2|U_ADJ|RAMP_RA3|cores18')},
        },
        'batch_policy_comparison_HEADLINE_10': {pn: {'E': b('HEADLINE_10|E|%s|cores18' % pn), 'U': b('HEADLINE_10|U_ADJ|%s|cores18' % pn),
                                                     'E_12_cores': b('HEADLINE_10|E|%s|cores12' % pn)}
                                                for pn in ('V005_AS_IS', 'RAMP_RA3', 'RAMP_RA2', 'RAMP_BUDGET16')},
        'mixed_queue_headline_then_sens': {k: {kk: MX[k][kk] for kk in ('makespan_h', 'headline_subset_done_h', 'max_route_a')}
                                           for k in ('MIXED_9H_18S|E|RAMP_RA3|cores18', 'MIXED_9H_18S|U_ADJ|RAMP_RA3|cores18')},
        'campaign_120_calls_21_waves': {
            'waves': '[1] + 19 x [6] + [5]: the seed wave of 1 is TESTED (orchestrator plan, dry plans); "120 = 20 batches of 6" and '
                     '"the budget, not the rounds, is expected to bind" are the coordinate spec rationale (FORMAL); real wave sizes UNTESTED',
            'config_as_shipped_m1': {'E': c('E|max_concurrent1|budget17|cores18'), 'U': c('U_ADJ|max_concurrent1|budget17|cores18')},
            'm2': {'E': c('E|max_concurrent2|budget17|cores18'), 'U': c('U_ADJ|max_concurrent2|budget17|cores18')},
            'm3': {'E': c('E|max_concurrent3|budget17|cores18'), 'U': c('U_ADJ|max_concurrent3|budget17|cores18')},
            'm6_recommended': {'E': c('E|max_concurrent6|budget17|cores18'), 'U': c('U_ADJ|max_concurrent6|budget17|cores18'),
                               'E_12_cores': c('E|max_concurrent6|budget17|cores12'), 'U_12_cores': c('U_ADJ|max_concurrent6|budget17|cores12')},
            'successor_budget24_option': {'E': c('E|max_concurrent6|budget24|cores18|SUCCESSOR_ONLY'), 'U': c('U_ADJ|max_concurrent6|budget24|cores18|SUCCESSOR_ONLY')},
            'successor_budget48_option': {'E': c('E|max_concurrent6|budget48|cores18|SUCCESSOR_ONLY'), 'U': c('U_ADJ|max_concurrent6|budget48|cores18|SUCCESSOR_ONLY')},
            'wave_cap_note': 'campaign_c2v005 starts no call after campaign_wall_cap_s (L200) and lets running calls finish. At m=1 the 6th call of a '
                             '6-call wave starts at 5 x the per-call wall: 43.8 h in U (no cut solo-equivalent); any slowdown above 48/43.8 = 1.10x '
                             'leaves that call NOT_STARTED.'},
    }
    E10, U10 = B['HEADLINE_10|E|RAMP_RA3|cores18']['makespan_h'], B['HEADLINE_10|U_ADJ|RAMP_RA3|cores18']['makespan_h']
    Ec, Uc = C['E|max_concurrent6|budget17|cores18']['makespan_h'], C['U_ADJ|max_concurrent6|budget17|cores18']['makespan_h']
    Ep, Up = B['POST_S1_2|E|RAMP_RA3|cores18']['makespan_h'], B['POST_S1_2|U_ADJ|RAMP_RA3|cores18']['makespan_h']
    Es, Us = B['SENS_18_BOTH_D|E|RAMP_RA3|cores18']['makespan_h'], B['SENS_18_BOTH_D|U_ADJ|RAMP_RA3|cores18']['makespan_h']
    Ed, Ud = B['DIII_4|E|RAMP_RA3|cores18']['makespan_h'], B['DIII_4|U_ADJ|RAMP_RA3|cores18']['makespan_h']
    Ec1, Uc1 = C['E|max_concurrent1|budget17|cores18']['makespan_h'], C['U_ADJ|max_concurrent1|budget17|cores18']['makespan_h']
    wall['critical_path'] = {
        'label': 'UNTESTED; compute only; root steps between batches are not estimated (no measured data)',
        'path': ['T0 = sealed V007 compare verdict reads ADOPT_TAIL', 'root: config C1, seal tuple line, launch bytes, step-4 admission',
                 'HEADLINE batch (10 runs)', 'root: deciding/capability documents, C4-6 derivation, caps, config C2, gates_ok in plan mode',
                 'CAMPAIGN (120 calls, m=6, budget 17)', 'FINAL_SUMMARY', 'S4-POST-S1 (2 runs, once registered)'],
        'E_h': round(E10 + Ec + Ep, 1), 'U_h': round(U10 + Uc + Up, 1),
        'E_days': round((E10 + Ec + Ep) / 24.0, 1), 'U_days': round((U10 + Uc + Up) / 24.0, 1),
        'arithmetic': 'E: %.2f + %.2f + %.2f h; U: %.2f + %.2f + %.2f h' % (E10, Ec, Ep, U10, Uc, Up),
        'with_config_as_shipped_m1': {'E_days': round((E10 + Ec1 + Ep) / 24.0, 1), 'U_days': round((U10 + Uc1 + Up) / 24.0, 1)},
        'off_path': {'DIII_4_before_T0': {'E_h': Ed, 'U_h': Ud}, 'SENS_18_after_campaign_default': {'E_h': Es, 'U_h': Us}},
        'total_step4_from_T0_sequential': {'E_h': round(E10 + Ec + Ep + Es, 1), 'U_h': round(U10 + Uc + Up + Us, 1),
                                           'E_days': round((E10 + Ec + Ep + Es) / 24.0, 1), 'U_days': round((U10 + Uc + Up + Us) / 24.0, 1)},
    }
    # compute volume (busy process-hours), from the same segment model (route-B busy 1.5 assumed)
    def ph(kind, scen):
        w = 93.25
        I = 7 if scen == 'E' else 32
        prep = 375.1
        if kind == 'ON':
            ra = prep + 285.0 + I * (8 * w + 111.0) + 285.0
            rb = (16322.5 if scen == 'E' else 24026.8) * 1.5
        else:
            ra = prep + I * 8 * w
            rb = (14088.5 if scen == 'E' else 20439.2) * 1.5
        return (ra + rb) / 3600.0
    n_on = 10 + 18 + 120 + 2
    vol = {sc: round(n_on * ph('ON', sc) + 4 * ph('OFF', sc), 0) for sc in ('E', 'U')}
    wall['compute_volume_process_hours'] = {'tail_on_calls': n_on, 'tail_off_calls': 4, 'E': vol['E'], 'U': vol['U'],
                                            'machine_hours_at_18_cores': {'E': round(vol['E'] / 18.0, 0), 'U': round(vol['U'] / 18.0, 0)},
                                            'reading': 'the campaign is latency-bound (21 sequential waves of 5-9 h calls), not throughput-bound'}

    rec = {
        'schema': 'STEP4_LAUNCH_ORDER_C4V001', 'utc': utc, 'lane': 'Claude4 helper, dispatch 0587 (coordinator Claude2); parts (a), (3) and (4)',
        'authority': 'Root (Claude2) alone launches. Nothing here launches, schedules or authorizes a run; every order and setting is a RECOMMENDATION.',
        'labels': {'TESTED': 'recomputed here from bytes or by a fenced plan-only probe', 'FORMAL': 'read from code or rulings (file:line cited)',
                   'UNTESTED': 'projections, wall times, future behaviour'},
        'inputs': {'reconcile_record': pin(rec_p), 'schedule_sim_record': pin(sim_p), 'registry_probe_record': pin(prb_p),
                   'source_pins_file': pin(pins_p), 'source_pins_utc': pins_utc,
                   'source_pins_additions_file': pin(LO + '/work/SOURCE_PINS_C4V002_ADDITIONS.txt'),
                   'inventory_json': {'path': S4 + '/inventory/INVENTORY_C4V001.json', 'sha256': R['inputs'][S4 + '/inventory/INVENTORY_C4V001.json']['sha256']},
                   'root_items_json': {'path': S4 + '/inventory/ROOT_ITEMS_C4V001.json', 'sha256': R['inputs'][S4 + '/inventory/ROOT_ITEMS_C4V001.json']['sha256']},
                   'dryplans_json': {'path': S4 + '/dryplans/DRYPLANS_C4V002.json', 'sha256': R['inputs'][S4 + '/dryplans/DRYPLANS_C4V002.json']['sha256']}},
        'addendum_v005_reads': [
            {'utc': '2026-10-18T19:21:09Z', 'sha256': sha_file(LO + '/source_snapshots/V005_ADDENDUM_snapshot_1921Z.md'), 'snapshot': LO + '/source_snapshots/V005_ADDENDUM_snapshot_1921Z.md', 'adds_vs_inventory_read': 'A92'},
            {'utc': '2026-10-18T19:52Z', 'sha256': sha_file(LO + '/source_snapshots/V005_ADDENDUM_snapshot_1952Z.md'), 'snapshot': LO + '/source_snapshots/V005_ADDENDUM_snapshot_1952Z.md', 'adds': 'A93-A96 (A96: V007 seals on r5; r6 unfinished and unused; compare r12 frozen 4bd7b262)'}],
        'sources': src,
    }

    # ---------------- (a) reconcile
    rec['reconcile'] = {
        'record': pin(rec_p),
        'result': {'pairs_checked': len([x for x in R['pairs'] if x['dryplan_records']]), 'pair_checks': R['n_pair_checks'],
                   'all_pair_checks_true': R['all_pair_checks_true'], 'unmatched_dryplan_records': R['unmatched_dryplan_records'],
                   'unmatched_inventory_runs': R['unmatched_inventory_runs'], 'unexplained_blocker_differences': R['blocker_differences_unexplained'],
                   'counts': {k: R['counts'][k] for k in ('inventory_records', 'inventory_direct_root_runs_listed', 'dryplan_records', 'dryplan_distinct_spec_files', 'dryplan_tail_on_records', 'dryplan_distinct_certificate_point_keys')},
                   'label': 'TESTED'},
        'explained_disagreements': [
            {'id': 'D1', 'topic': 'record counts 37 vs 34', 'explanation': R['counts']['explanation'], 'label': 'TESTED (counts) / FORMAL'},
            {'id': 'D2', 'topic': 'registry points 27 (inventory R-C1) vs 28 distinct dry-plan keys',
             'explanation': 'The 28th key is the campaign seed point 6944e210d071c17b502fd5188ea8967503dbf9bb1d5530b67d0b151da02b13cd (log/exp seed about 1e-15 off the anchor, R-D10). Wave 1 needs its prelaunch bundle too. R-C1 count corrected to 28.', 'label': 'TESTED'},
            {'id': 'D3', 'topic': 'HEADLINE specs "exact launch bytes" (dry plans) vs "generated at launch" (inventory)',
             'explanation': 'The dry-plan HEADLINE specs are the exact Mapper.build bytes under today\'s r9 config (PENDING slots, no registry). Both lists agree that launch bytes change after adoption (dry-plan post_adoption_probe: TAIL_REANCHOR 924851c4..., HEADLINE_TRIAL 7d9a8d47..., seed 854e1291...) and again under a registry. The registry probe here reproduced the seed sha 854e1291... with the A70 slots (TESTED).', 'label': 'TESTED'},
            {'id': 'D4', 'topic': 'deciding (iii) tail-ON (0533 B4-1, A57) vs tail-OFF (0540 F3, A61 F3)',
             'explanation': 'Both lists use tail-OFF. 0540 F3 (root specification, 13:50Z) and A61 F3 (13:40Z, later than A57 13:03Z) define the rerun as tail-OFF v010 r5 against v009-GEO; 0533/A57 wording "tail-ON" is superseded by the later root specification.', 'label': 'FORMAL'},
            {'id': 'D5', 'topic': 'R-B2 as a blocker of the DIII runs (inventory summary) vs launch-ready (dry plans)',
             'explanation': 'compute_pair refuses at its first statement while COMPARATOR_A68_REVIEWED is False, before any run read; the runs themselves plan with 0 blockers. R-B2 gates the evidence step, not the launch.', 'label': 'FORMAL + TESTED (dry plans)'},
            {'id': 'D6', 'topic': 'distance plans: "trial theta at D" (inventory) vs "anchor template at D" (dry plans)',
             'explanation': 'Same bytes apart from the label: physical equal bitwise and template-vs-spec leaf diff == [/label] (reconcile pairs S4-SENS-DIST-LO/HI).', 'label': 'TESTED'},
            {'id': 'D7', 'topic': 'per-run blocker sets',
             'explanation': 'After mapping both vocabularies to root-item ids, every difference is a layer difference (resource caps, readings, launch entries and scheduling are root items a plan-only dry run cannot see; post-run registrations sit under `unlocks` in the inventory). 0 unexplained (reconcile v002; v001 kept with 13 mapping gaps).', 'label': 'TESTED (mapping) / FORMAL (explanations)'},
            {'id': 'D8', 'topic': 'rulings newer than both lists',
             'explanation': 'Both lists read the open V005 addendum up to 0753f2d8 (19:06-19:11Z). Since then: A92 (c2v007r2 052da0fe is the identity-comparator slot; 0611), A96 (V007 seals on r5; r6 unfinished, unused; caching for steps 4-5 decided later), compare r12 frozen 4bd7b262 (still refuses CASE_BLOCK_ABSENT in sealed mode, L5705-5714). R-B1, R-B2 and R-A3 are updated in ROOT_ITEMS_FINAL.', 'label': 'TESTED (bytes) / FORMAL'},
            {'id': 'D9', 'topic': 'workers_8 candidate',
             'explanation': 'Dry plans built an anchor-point repeat (686ad07f..., the PC-7 option); the inventory recommends DU-2 (designate one headline corner). Both satisfy check_deciding (core L128-197, FORMAL). Root designates (R-D2).', 'label': 'FORMAL'},
        ],
        'open_problems': [
            {'id': 'OP1', 'what': 'DU-1 (TAIL_REANCHOR := the mapper-built trial spec) against 0557 N-1, whose text says the reanchor launches "from the template\'s physical values, not a mapper-built theta". Inventory: root must confirm. Dry plans: N-1 respected (physical bitwise equal). Not decidable from bytes.', 'owner': 'Claude2', 'item': 'R-D1'},
            {'id': 'OP2', 'what': 'Campaign points proposed by the engine after the pre-registered ones cannot pass prelaunch_check, and growing the registry changes the cache id (C4-2). Neither list raised it. TESTED on look-alikes here.', 'owner': 'Claude2 + Codex2', 'item': 'R-C8'},
            {'id': 'OP3', 'what': 'Prereg r4 has no binding_inputs.case_block; frozen compare r12 (4bd7b262) still refuses CASE_BLOCK_ABSENT in sealed mode. Seal-blocking unless a prereg successor or seal note binds a registered case block.', 'owner': 'Claude2 at seal assembly; prereg author Claude4; compare owner Codex3', 'item': 'R-A3'},
            {'id': 'OP4', 'what': 'Whether c2v007r2 (identity comparator for same-driver identity runs) can carry the two-driver (v009-GEO vs v010 r5) deciding-(iii) comparison through an adapter with declared custody tokens.', 'owner': 'Codex2 (policy) + Codex1 (c2v007r2)', 'item': 'R-B2'},
        ],
    }

    # ---------------- (b) DAG and order
    E = []
    def e(a, z, why, label='FORMAL'):
        E.append({'from': a, 'to': z, 'why': why, 'label': label})
    e('ROOT:R-A3 case block bound by the sealed prereg', 'G:V007_SEAL', 'compare r11 L5689-5697 / r12 L5705-5714: sealed mode refuses CASE_BLOCK_ABSENT')
    e('G:V007_SEAL', 'G:V007_ADOPT_TAIL (T0)', 'step 2 T-runs then the sealed compare (A57: calibration consumes only a sealed ADOPT_TAIL)')
    e('ROOT:R-D5 caps + launch window', 'RUN:DIII x4', '0540 F3 / A61 F3: tail-OFF, root launches during calibration prep; no V007 input')
    e('RUN:DIII-LO-REF + RUN:DIII-LO-NEW + ROOT:R-B2 comparator successor', 'EV:DIII-LO pair evidence', 'sensitivity policy compute_pair (refuses while COMPARATOR_A68_REVIEWED False)')
    e('RUN:DIII-HI-REF + RUN:DIII-HI-NEW + ROOT:R-B2 comparator successor', 'EV:DIII-HI pair evidence', 'as LO')
    e('EV:DIII-LO pair evidence + ROOT:R-C5 distinct review (LO)', 'REG:per_distance[D_lo]', 'review sha registered in a policy successor; config tail_readiness.sensitivity_deciding_iii (A61 F3: a pass unlocks only that D)')
    e('EV:DIII-HI pair evidence + ROOT:R-C5 distinct review (HI)', 'REG:per_distance[D_hi]', 'as LO')
    e('ROOT:R-C1 registry (28 points) + policy review + producers', 'CFG:C1', 'capability evidence binds the post-registry Mapper.build bytes (core L240-264); freeze the registry before the CAP runs', 'FORMAL + TESTED (probe)')
    e('G:V007_ADOPT_TAIL (T0)', 'CFG:C1', 'R-A1: numerics pins and block := sealed C4T numerics (adoption policy L90-91)')
    e('ROOT:R-B3 v006r10 cascade (+R-A2 tuple line after T0)', 'G:gates_ok', 'APPROVED_V007_SEALS empty in the shipped policy (adoption policy L9-12); successor pins: core L200-203, wrapper L27')
    e('CFG:C1 + ROOT:R-B6 step-4 launcher and admission + ROOT:R-D8 caps + ROOT:R-D1/R-D2 designations', 'RUN:HEADLINE batch (RA, W8, CAP x9)', 'launch bytes regenerated under C1; ramp-gated root launch')
    e('RUN:S4-RA + RUN:S4-W8', 'DOC:deciding_test + config.anchor (R-D4)', 'core check_deciding L114-197')
    e('RUN:S4-CAP-TRIAL + RUN:S4-CAP-C000..C111', 'DOC:capability_evidence (R-D3)', 'core capability_probe L313-340')
    e('DOC:deciding_test', 'G:numerics_verdict', 'v005 fresh_gates L1943-1947: check_numerics takes route_a_column_workers_verified from check_deciding (adoption_world S5)', 'FORMAL + TESTED (dry plans)')
    e('DOC:capability_evidence + V007:C4T receipt + post-adoption base/seed spec shas', 'DOC:C4-6 adoption derivation (R-A4, R-A5)', 'wrapper check_adoption L183-197 requires driver_capability ok; v005 C4-6 L1828-1926')
    e('DOC:deciding_test + DOC:capability_evidence + DOC:C4-6 + ROOT:R-C2 + ROOT:R-A5 caps (+ REG:per_distance only if final before T_campaign, R-D16)', 'CFG:C2', 'one config for the whole campaign: tail_readiness is in the cache id (wrapper L52-55), C4-2 forbids a change mid-campaign', 'FORMAL + TESTED (probe)')
    e('CFG:C2 + G:gates_ok + ROOT:R-B4 run entry + ROOT:R-C8 registry growth mechanism + ROOT:R-D7 settings + ROOT:R-D11 work dir', 'RUN:CAMPAIGN', 'v005 run() L3436-3444: refuses unless gates_ok and a session leader')
    e('RUN:CAMPAIGN', 'DOC:FINAL_SUMMARY', 'engine v003b PROBE-WAVE-INGEST loop, R-B5 per-call acceptance')
    e('DOC:FINAL_SUMMARY + ROOT:R-C6 registration', 'RUN:S4-POST-S1', 'compare r11 L489-490 ADOPT_TAIL next step')
    e('REG:per_distance[D_lo] + CFG:C1 (adopted block, registry) + ROOT:R-C7 reading', 'RUN:SENS-*-LO (9)', 'sensitivity_gate via prelaunch_check (B4-1); recommended after the campaign')
    e('REG:per_distance[D_hi] + CFG:C1 (adopted block, registry) + ROOT:R-C7 reading', 'RUN:SENS-*-HI (9)', 'as LO')
    e('RUN:HEADLINE batch done', 'RUN:CAMPAIGN start', 'one machine-wide schedule (R-D15): the campaign launcher and a direct-run launcher do not share a budget', 'RECOMMENDATION')
    rec['dag'] = {'edges': E, 'note': 'Headline D = 4.04 runs are ungated by deciding (iii) (0533 B4-1; A57). Per-D (iii) evidence unlocks only its own D (A61 F3).'}

    rec['launch_order'] = [
        {'phase': 'P (now, before the V007 seal)', 'steps': [
            {'step': 'P1', 'who': 'root + lanes', 'what': 'Close the pre-seal root items (ROOT_ITEMS_FINAL group "before the seal"): R-A3 (seal-blocking), R-A6, R-C1 (28 bundles), R-C8, R-B2/R-B3/R-B4 (v006r10 with the tuple placeholder), R-B6 (launcher successor + review), R-D1/R-D2, R-D5/R-D8 caps, R-C2..R-C7 and R-D9 rulings.'},
            {'step': 'P2', 'who': 'root launch', 'what': 'DIII batch, 4 tail-OFF runs, ramp-gated, in this order: S4-DIII-LO-REF (v009-GEO 237ef3d4), S4-DIII-LO-NEW (r5 b5cc62af), S4-DIII-HI-REF, S4-DIII-HI-NEW. Window: before the seal while load permits (19:32Z: loadavg 13.1/17.6/22.0 on 18 cores, 87% memory free, TESTED once); never at normal QoS inside the step-2 route-A ramp (A85.2 core priority). Pairs adjacent so each D\'s evidence can start as soon as its two runs finish.',
             'wall': {'E_h': wall['batches_ramp_RA3_18_cores']['DIII_4']['E']['makespan_h'], 'U_h': wall['batches_ramp_RA3_18_cores']['DIII_4']['U']['makespan_h']}},
            {'step': 'P3', 'who': 'root + reviewers', 'what': 'Per D: compute_pair under the R-B2 successor, distinct review (R-C5), registration (R-D16 placement).'}]},
        {'phase': 'S (seal to verdict)', 'steps': [
            {'step': 'S1', 'who': 'root', 'what': 'No step-4 tail-ON launch before the sealed ADOPT_TAIL (A57). DIII only if not yet run, at background priority.'}]},
        {'phase': 'H (T0 = sealed ADOPT_TAIL)', 'steps': [
            {'step': 'H1', 'who': 'root', 'what': 'Write C1 (R-A1 pins, block := sealed C4T numerics, registry/policy/producers R-C1, direct-run caps R-D8); insert the seal tuple line (R-A2) and verify it by line diff; regenerate the launch bytes plan-only; where the registry gives a point the A70 slot records, its bytes must equal the dry-plan PROVISIONAL sha; write and publish the step-4 admission record (R-B6).'},
            {'step': 'H2', 'who': 'root launch', 'what': 'HEADLINE batch, one ramp-gated plan, order: S4-RA (fresh template, default per R-D1), S4-CAP-TRIAL, S4-CAP-C000 (= S4-W8 under DU-2), C100, C010, C110, C001, C101, C011, C111 (the orchestrator probe_points order). S4-RA first: the known registered point validates the whole launch path before the corners start.',
             'wall': {'E_h': E10, 'U_h': U10}},
            {'step': 'H3', 'who': 'root', 'what': 'From monitor-verified receipts: capability evidence (R-D3), deciding_test and config.anchor (R-D4), C4-6 derivation and caps (R-A4, R-A5), u_i carrier (R-C2); write C2; run the orchestrator plan mode on C2 and require gates_ok true and the next wave = the seed call; create the fresh campaign work dir on External1 (VolumeUUID 7752BF6F-EFA9-418D-AD80-29078B663078, R-D11).'}]},
        {'phase': 'C (campaign)', 'steps': [
            {'step': 'C1', 'who': 'root launch', 'what': 'Orchestrator run under launch_setsid_c2v005 (session leader) through the R-B4 entry, max_concurrent 6, process_budget 17, stage_aware true; per completed call write_acceptance + reingest (R-B5); registry growth per R-C8; no direct batch overlaps the campaign (R-D15).',
             'wall': {'E_h': Ec, 'U_h': Uc}}]},
        {'phase': 'Z (after FINAL_SUMMARY)', 'steps': [
            {'step': 'Z1', 'who': 'root launch', 'what': 'S4-POST-S1 (2 runs, K=3 and K=4 at the calibrated point) once registered (R-C6).', 'wall': {'E_h': Ep, 'U_h': Up}},
            {'step': 'Z2', 'who': 'root launch', 'what': 'SENS batch(es): 18 runs (or 9 per registered D) under the same ramp, after their per-D registration and reading (R-C7). Default placement after the campaign keeps them off the calibration critical path; they precede the freeze if A23 reads them.', 'wall': {'E_h': Es, 'U_h': Us}}]},
    ]

    # ---------------- (c) ramp
    rec['ramp'] = {
        'decision': {
            'campaign': 'The orchestrator launches its own calls (Orchestrator.run -> CampaignExecutor -> campaign_c2v005 d35d5d4a, v005 C4-4 session leader). Keep it; no V005 launcher in front of it. Its FIFO process budget (17, stage-aware, peak 8 in route A, 2 after) bounds CPU; its memory is not binding at <= 2 route-A calls (modelled).',
            'direct_runs': 'The 33 direct runs (RA, W8, CAP x9, SENS x18, DIII x4) and S4-POST-S1 are root-direct monitor launches that the orchestrator does not launch (it only reads their receipts). The V005 pattern fits them; the V005 bytes do not.',
            'label': 'FORMAL (code) / RECOMMENDATION'},
        'v005_bytes_do_not_fit': [
            'launcher v007 validate() requires exactly 10 distinct cases with C4T-KHI first and route_a_admission.first_case_exception == "C4T-KHI" (L72-83)',
            'launcher v007 validate() calls G.admission(): the V007 ROOT_SEAL_ADMISSION config with this launcher on its producer allowlist and on BUILD_V005\'s allowlist text (guard L19-43); a step-4 launcher is on neither',
            'binder f3e4e2be writes only under v007_launch_packet_cx1 (L18 NEW_BUILD_OUTPUT_REQUIRED) and binds the frozen addendum and driver only',
            'launcher v007 caps route A at 6 (available() L47-48), sized for the 10 V007 cases'],
        'reuse_as_is_pattern': [
            'root_monitor_c2v001 (ba031c23) per call, caps as argv, and the monitor_argv binding check (L63-64, L88-89)',
            'nohup + start_new_session + DEVNULL + BLAS=1 env; exclusive monitor and launcher logs; detached worker (L161-176, L193-199)',
            'the ramp signal readers: outdir/progress.jsonl route_a finished; stages/01_route_a/attempt_000/progress.jsonl iteration_completed int >= 0 (L15-44). TESTED for the step-4 specs: route A is stage 01 at stages/01_route_a/attempt_000 in every dry plan (tail-ON solver 7667025b, tail-OFF r5 and v009-GEO solver aed4dd59); both solvers emit stage iteration_completed (7667025b L348, aed4dd59 L304; FORMAL)',
            'memory_pressure parse failing closed (L50-60)',
            'systemic-failure halts, ordinary failure continues, no retry/resume/reuse, root decides relaunch (L102-180)',
            'check_run_path for outputs (C5H/UVT refusal, guard L107-115)'],
        'adapt': [
            'plan schema: one plan per batch (DIII, HEADLINE, SENS_LO, SENS_HI, POST_S1), N >= 1 calls, the first-case exception = the first call of the plan',
            'admission: a STEP4 root admission record (root-written, exclusive create, published sha in an env var as guard v008 does) pinning the V007 SEAL_RECORD, the sealed verdict report (ADOPT_TAIL), config C1, the registry, the batch plan and the launcher/guard sources; the DIII plan has a pre-seal admission pinning only the pair plan, both drivers, the two spec files and caps',
            'per tail-ON call, a root-produced PRELAUNCH record (orchestrator prelaunch_check PASS for that spec under C1, including the sensitivity gate for SENS) whose sha the plan pins and the launcher verifies',
            'route_a_admission block {max_active 3, minimum_free_percent 25, poll_seconds 60, source /usr/bin/memory_pressure, ramp previous_first_completed_route_a_iteration, first_case_exception <first call>}',
            'caps per class (R-D8 direct tail-ON; R-D5 tail-OFF), output dirs chosen by root (R-D11)',
            'binder successor: writes under the step-4 packet folder and binds C1 and the admission instead of the frozen addendum',
            'caffeinate -i -w <launcher pid> and normal QoS for root runs (A85.2/A85.4 pattern, extended to step 4 by root ruling)'],
        'proposed_parameters': {
            'start_conditions': [
                'published step-4 admission verified from bytes (tail-ON batches: sealed ADOPT_TAIL bound; DIII: pre-seal admission)',
                'batch gate met: tail-ON -> C1 written and a PRELAUNCH PASS record per spec; SENS -> per-D registration present',
                'first call of a batch starts immediately; each later call only after its predecessor\'s first route-A iteration_completed',
                'fewer than 3 calls of step 4 in route A', 'memory_pressure free >= 25% (unavailable reading = no start)',
                'at most one start per 60 s poll', 'no start after a systemic failure or after a predecessor ended without a completed iteration',
                'one direct batch at a time; no direct batch while the campaign runs (R-D15)'],
            'memory_threshold_free_percent': 25, 'route_a_concurrency_cap': 3, 'poll_seconds': 60,
            'campaign_settings': {'max_concurrent': 6, 'process_budget': 17, 'stage_aware_budget': True,
                                  'campaign_wall_cap_s': '172800 suffices at m=6 (max wave span %.1f h E / %.1f h U)' % (C['E|max_concurrent6|budget17|cores18']['max_wave_span_h'], C['U_ADJ|max_concurrent6|budget17|cores18']['max_wave_span_h']),
                                  'min_free_percent_modelled': round(min(C['E|max_concurrent6|budget17|cores18']['min_free_percent'], C['U_ADJ|max_concurrent6|budget17|cores18']['min_free_percent']), 1)},
            'label': 'RECOMMENDATION; projections UNTESTED'},
        'why': [
            'Route-A cap 3 is A61\'s original token, sized from measured RSS (about 10.5 GB route-A baseline plus 0.40 GiB per worker at K_big 128). For the 10-run headline batch it gives %.2f h E / %.2f h U against %.2f / %.2f h for V005 cap 6 and %.2f / %.2f h for the orchestrator-style budget 16 (fluid model, 18 cores).' % (
                E10, U10, B['HEADLINE_10|E|V005_AS_IS|cores18']['makespan_h'], B['HEADLINE_10|U_ADJ|V005_AS_IS|cores18']['makespan_h'],
                B['HEADLINE_10|E|RAMP_BUDGET16|cores18']['makespan_h'], B['HEADLINE_10|U_ADJ|RAMP_BUDGET16|cores18']['makespan_h']),
            'Cap 6 buys %.0f%% in the upper case but lets modelled free memory fall to %.1f%% (below the gate, after admission) with %.1f busy processes on 18 cores; cap 3 keeps it at or above %.1f%% for the headline batch.' % (
                100.0 * (1 - B['HEADLINE_10|U_ADJ|V005_AS_IS|cores18']['makespan_h'] / U10), B['HEADLINE_10|U_ADJ|V005_AS_IS|cores18']['min_free_percent'],
                B['HEADLINE_10|U_ADJ|V005_AS_IS|cores18']['max_demand'], B['HEADLINE_10|U_ADJ|RAMP_RA3|cores18']['min_free_percent']),
            'The budget-16 accounting counts 2 busy processes for every call in route B, so it caps a batch at about 5 concurrent calls and adds %.1f-%.1f h to the critical path; it suits the campaign (where it is the reviewed rule) but not the short direct batches.' % (
                B['HEADLINE_10|E|RAMP_BUDGET16|cores18']['makespan_h'] - E10, B['HEADLINE_10|U_ADJ|RAMP_BUDGET16|cores18']['makespan_h'] - U10),
            'Memory gate 25%%, 60 s poll, one start per poll and the first-iteration ramp are the reviewed V005 rules (A72 ITEM3-R1; Claude4 0076 ramp 14/14). The first iteration completes about %.1f min (tail-ON) / %.1f min (tail-OFF) after start, solo.' % (pc['TAIL_ON_E']['first_iteration_solo_min'], pc['TAIL_OFF_E']['first_iteration_solo_min']),
            'Campaign m=6 (the nominal wave size) under the existing budget 17 gives %.1f d E / %.1f d U against %.1f / %.1f d at the shipped max_concurrent 1; no code change.' % (
                C['E|max_concurrent6|budget17|cores18']['makespan_days'], C['U_ADJ|max_concurrent6|budget17|cores18']['makespan_days'],
                C['E|max_concurrent1|budget17|cores18']['makespan_days'], C['U_ADJ|max_concurrent1|budget17|cores18']['makespan_days'])],
        'fallback_zero_build': 'campaign_c2v005 CLI (--campaign FILE --campaign-dir DIR) can run a direct batch with the same monitor and receipt checks under its FIFO budget, but has no ramp, no memory gate and no C5H output guard; at budget 16-17 the headline batch takes about %.1f h E (budget-16 row). Use only if the launcher successor is not reviewed in time.' % B['HEADLINE_10|E|RAMP_BUDGET16|cores18']['makespan_h'],
    }
    rec['wall_times'] = wall

    # ---------------- probe summary
    rec['registry_growth_probe'] = {'record': pin(prb_p), 'results': P['results'], 'reading': P['reading'],
                                    'cache_ids': {k: v['cache_id'] for k, v in P['scenarios'].items()},
                                    'label': 'TESTED on synthetic look-alikes (plan-only, fence v002 blocked 0)'}
    rec['errata'] = ['The registry probe record\'s reading cites v005 L3300-3308 for make_plan; from bytes, make_plan starts at L3293 and calls prelaunch_check at L3309 (grep at 20:06Z). The probe record is kept unchanged.']
    rec['fence'] = {'fence_c4v001': pin(LO + '/tools/fence_c4v001.py'), 'fence_c4v002': pin(LO + '/tools/fence_c4v002.py'),
                    'blocked_in_this_builder': F.BLOCKED,
                    'note': 'fence_c4v002 is the dry-plan lane\'s documented variant (admits only a lowercase uvt_*.py code file outside runs_ext; stricter on runs_ext listing); copied byte-equal; no runs_ext open is relaxed. No runs_ext, UVT_*, C5H or target path was opened by any process of this part.'}
    rif = LO + '/work/ROOT_ITEMS_FINAL_C4V001.json'
    RI = load(rif)
    rec['root_items_final'] = {'record': pin(rif), 'markdown': pin(LO + '/ROOT_ITEMS_FINAL_C4V001.md'), 'n_items': RI['n_items'],
                               'items': [{k: x[k] for k in ('id', 'group', 'title', 'close_by', 'owner', 'v007')} for x in RI['items']],
                               'most_likely_to_delay_step4_RECOMMENDATION': RI['most_likely_to_delay_step4_RECOMMENDATION'],
                               'new_items_this_part': RI['traceability']['new_items_this_part']}
    rec['producer'] = pin(os.path.abspath(__file__))
    if os.path.exists(out):
        want = os.environ.get('REPLACE_SHA_' + os.path.basename(out).replace('.', '_'))
        if not want or sha_file(out) != want:
            raise SystemExit('OUTPUT_EXISTS_WITHOUT_MATCHING_REPLACE_SHA ' + out)
        fh = open(out, 'w')
    else:
        fh = open(out, 'x')
    with fh as f:
        json.dump(rec, f, indent=1, sort_keys=False, allow_nan=False)
        f.write('\n')
    print(json.dumps({'out': out, 'sha256': sha_file(out), 'critical_path': wall['critical_path'], 'blocked': F.BLOCKED,
                      'vol': wall['compute_volume_process_hours']}, indent=1))


if __name__ == '__main__':
    main(sys.argv[1])

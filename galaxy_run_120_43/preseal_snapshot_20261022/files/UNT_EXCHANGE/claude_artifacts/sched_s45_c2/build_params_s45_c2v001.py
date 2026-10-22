"""Builder for the sched_s45 parameter successors (Claude2 sched_s45_c2, c2v001).  Writes, by exclusive create:
  * SCHED_DELTA_S45_C2V001.json            the scheduling delta (apply_sched_delta_s45_c2v001 applies it to R9, and at H3
                                           to C2);
  * RUN_CONFIG_DDO154_CX2V006R9_S45_C2V001.json  R9 (721c7230) + that delta, and its DELTA_REPORT;
  * DIRECT_BATCH_PARAMS_S45_C2V001.json    route_a_admission.max_active and per-case caps for the four Codex1 templates
                                           (templates_v004) and S4-POST-S1, parameters only (guard v010 L329-333, L346-348).
Every number carries its basis.  Reads the templates' case lists and R9; nothing else.
usage: python3 -I -B build_params_s45_c2v001.py
"""
import hashlib
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ART = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
R9 = ART / 'calib_tail_readiness_cx2/v006r9/RUN_CONFIG_DDO154_CX2V006R9_P128_MS128.json'
R9_SHA = '721c7230f3f3efde6f8406f13a52995ae321248829ab1ee64a2f522ad5582b8e'
TPL = ART / 'step4_launch_packet_cx1/templates_v004'
GiB = 1 << 30

TAIL_ON_CAPS = {'wall_cap_s': 100800,           # 28 h: >= 1.5 x 1.25 x the worst DERIVED solo call (sim 'high' row) and
                                                #   4.7 x the expected; R9 had 8 h, below the 'high' solo call
                'rss_cap_bytes': 64 * GiB,      # R9's value, unchanged: 2.1 x the MEASURED ps-RSS transfer peak (32.6 GB,
                                                #   C4T_A, 15 s sampling) and 3.4 x the 18.79 GiB model (A61 >= 1.5)
                'output_cap_bytes': 56 * GiB}   # >= 32 iterations x the MEASURED 1.575 GiB per route-A iteration (C4T,
                                                #   S4T, C4T_A, C4T_D5) + manifest/route B (MEASURED <= 0.4 GiB): 51.4 GiB;
                                                #   2.27 x the MEASURED largest full tail-ON call (26.5 GB, root); R9 12 GiB
TAIL_OFF_CAPS = {'wall_cap_s': 46800,           # 13 h >= 1.5 x 1.25 x 6.61 h (DERIVED U tail-OFF) = 12.4 h; 2.75 x the
                                                #   MEASURED 4.72 h tail-OFF call (C5H, root); R-D5 proposed 12 h
                 'rss_cap_bytes': 16 * GiB,     # R-D5 as proposed: 1.64 x the 10.47 GB tail-OFF fit (no TailState spikes)
                 'output_cap_bytes': 96 * GiB}  # R-D5 as proposed (modelled worst case 57.7 GiB)


def sha_b(b):
    return hashlib.sha256(b).hexdigest()


def xwrite(path, obj=None, raw=None):
    data = raw if raw is not None else (json.dumps(obj, indent=1, sort_keys=True) + '\n').encode()
    with open(path, 'xb') as f:
        f.write(data)
    return sha_b(data)


SIM = HERE / 'SIM_S45_C2V001_R3.json'            # max_active per batch: the simulation's memory-criterion choice
SIM_NAME = {'HEADLINE': 'HEADLINE11', 'DIII': 'DIII4', 'SENS_LO': 'SENS9', 'SENS_HI': 'SENS9', 'POST_S1': 'POST_S1_2'}


def main():
    r9b = R9.read_bytes()
    if sha_b(r9b) != R9_SHA:
        raise SystemExit('R9 pin mismatch')
    r9 = json.loads(r9b)
    camp = HERE / 'campaign_s45_c2v001.py'
    pc = r9['per_call']
    delta = {'schema': 'SCHED_DELTA_S45_C2V001',
             'predecessor': {'path': str(R9), 'sha256': R9_SHA},
             'set': {'campaign': {'path': str(camp), 'sha256': sha_b(camp.read_bytes())},
                     'max_concurrent': 12,
                     'per_call.wall_cap_s': float(TAIL_ON_CAPS['wall_cap_s']),
                     'per_call.output_cap_bytes': TAIL_ON_CAPS['output_cap_bytes'],
                     'disk_guard.per_call_bytes': TAIL_ON_CAPS['output_cap_bytes'],
                     'orphan_wait.cap_s': float(TAIL_ON_CAPS['wall_cap_s'] + 600),
                     'notes': r9['notes'] + ' s45 (sched_s45_c2, Claude2 2026-10-19): scheduling successor only -- campaign_s45_c2v001 '
                              '(shared machine gate machine_gate_s45_c2v001, set from MEASURED step-2 R2 resources), max_concurrent '
                              '12, per-call wall 28 h and output 56 GiB, disk guard 56 GiB per call, orphan wait 28 h + 600 s; every '
                              'physics input byte-identical to R9 721c7230.'},
             'unchanged_on_purpose': {
                 'per_call.rss_cap_bytes': '64 GiB (R9) already >= 1.5 x the MEASURED ps-RSS transfer peak',
                 'process_budget': '17: validated by the parent (L1727) and by campaign_s45 (no longer admits)',
                 'stage_aware_budget': 'true (reported; the gate reads phase itself)',
                 'campaign_wall_cap_s': '172800: the new rule starts every call of a 24-call wave within 12 h E / 35 h U (sim)',
                 'disk_guard.reserve_bytes': '20 GiB', 'disk_guard.measured_per_call_bytes': 'root replaces it at H3 with the '
                 'exact output bytes of the largest measured tail-ON receipt (C4-6 regenerates the adoption derivation caps)'},
             'labels': {'max_concurrent': 'DERIVED: core limit 24 / after-route-A weight 2 = 12 (the gate binds first)',
                        'per_call.wall_cap_s': 'DERIVED from MEASURED phase times (see TAIL_ON_CAPS)',
                        'per_call.output_cap_bytes': 'DERIVED from MEASURED per-iteration output x the spec max 32 iterations',
                        'orphan_wait.cap_s': 'R9 relation kept: wall cap + 600 s'},
             'parent_entry_patch': {'module_attribute': 'CAMPAIGN_MODULE_NAME', 'value': 'campaign_s45_c2v001',
                                    'where': 'the S4-R-B4b campaign entry, on the loaded parent module (O), before Context(config); '
                                             'record it in the launch record. PROCESS_BUDGET_MAX is not touched.'}}
    dsha = xwrite(HERE / 'SCHED_DELTA_S45_C2V001.json', delta)
    sys.path.insert(0, str(HERE))
    import importlib.util
    sp = importlib.util.spec_from_file_location('apply_s45', str(HERE / 'apply_sched_delta_s45_c2v001.py'))
    A = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(A)
    out, rep = A.apply(r9b, delta)
    if out is None:
        raise SystemExit('delta refused: %s' % rep)
    ssha = xwrite(HERE / 'RUN_CONFIG_DDO154_CX2V006R9_S45_C2V001.json', raw=out)
    rep['delta_sha256'] = dsha
    xwrite(HERE / 'DELTA_REPORT_R9_TO_S45_C2V001.json', rep)
    # direct batches
    simb = SIM.read_bytes()
    sim_pin = {'path': str(SIM), 'sha256': sha_b(simb)}
    chosen = json.loads(simb)['direct_batches_chosen_max_active']
    batches = {}
    for name, fname, kind in (('HEADLINE', 'HEADLINE_PLAN_TEMPLATE_CX1V004.json', 'ON'), ('DIII', 'DIII_PLAN_TEMPLATE_CX1V004.json', 'OFF'),
                              ('SENS_LO', 'SENS_LO_PLAN_TEMPLATE_CX1V004.json', 'ON'), ('SENS_HI', 'SENS_HI_PLAN_TEMPLATE_CX1V004.json', 'ON')):
        tb = (TPL / fname).read_bytes()
        t = json.loads(tb)
        cases = [c['case'] for c in t['calls']]
        tail = {c['case']: c.get('tail_on') for c in t['calls']}
        n = len(cases)
        k = chosen['chosen'][SIM_NAME[name]]
        rule = dict(t['route_a_admission'], max_active=k)
        batches[name] = {'template': {'path': str(TPL / fname), 'sha256': sha_b(tb)}, 'n_calls': n, 'case_order': cases,
                         'route_a_admission': rule, 'template_max_active': t['route_a_admission']['max_active'],
                         'caps_per_case': {c: dict(TAIL_ON_CAPS if tail[c] else TAIL_OFF_CAPS) for c in cases},
                         'max_active_basis': {'sim_row': SIM_NAME[name], 'rule': chosen['rule'], 'sim': sim_pin}}
    rule2 = dict(batches['HEADLINE']['route_a_admission'], max_active=chosen['chosen']['POST_S1_2'])
    batches['POST_S1'] = {'template': None, 'n_calls': 2, 'case_order': ['ROOT_NAMES_AT_REGISTRATION_K3', 'ROOT_NAMES_AT_REGISTRATION_K4'],
                          'route_a_admission': rule2, 'template_max_active': None,
                          'caps_per_case': {'ROOT_NAMES_AT_REGISTRATION_K3': dict(TAIL_ON_CAPS), 'ROOT_NAMES_AT_REGISTRATION_K4': dict(TAIL_ON_CAPS)},
                          'max_active_basis': {'sim_row': 'POST_S1_2', 'rule': chosen['rule'], 'sim': sim_pin}}
    impl = ART / 'step4_launch_packet_cx1/impl'
    packet = {k: {'path': str(impl / f), 'sha256': sha_b((impl / f).read_bytes())}
              for k, f in (('guard', 'step4_guard_cx1v010.py'), ('launcher', 'step4_launcher_cx1v011.py'), ('binder', 'step4_bind_cx1v009.py'))}
    doc = {'schema': 'DIRECT_BATCH_PARAMS_S45_C2V001', 'packet_read': packet,
           'scope': 'Parameters only for Codex1\'s guarded step-4 packet (the guard, launcher and binder in packet_read, unchanged): '
                    'root copies route_a_admission into C1 cfg.route_a_admission and caps_per_case into cfg.caps '
                    '(ROOT_CAPS_BINDING). No packet code changes. The packet\'s memory check stays memory_pressure >= 25 % '
                    '(MEASURED blind: 85-86 % free at 83 GB of run footprint), so max_active is the only memory lever: the '
                    'largest value whose simulated peak total footprint stays <= 120 GB in the expected and 32-iteration rows.',
           'basis': {'max_active': 'SIM_S45_C2V001_R3.json direct_batches_chosen_max_active (MEASURED footprints and transfer '
                                   'spikes, 32-iteration growth DERIVED)', 'caps': 'see build_params_s45_c2v001.py TAIL_ON_CAPS / TAIL_OFF_CAPS'},
           'batches': batches,
           'still_root_rulings': ['R-D8 (tail-ON caps: this file replaces its 29 GiB RSS proposal, which is below the MEASURED '
                                  '32.6 GB ps-RSS transfer peak)', 'R-D5 (DIII caps: wall 13 h instead of 12 h)',
                                  'R-D18 / S4-R-D8 route-A cap: max_active per batch as above (HEADLINE and SENS keep Codex1\'s 3: '
                                  '4 would reach a simulated 157 GB in the 32-iteration rows without a live memory gate; the '
                                  'shared-gate packet successors, item 6 of the README, remove that limit)']}
    xwrite(HERE / 'DIRECT_BATCH_PARAMS_S45_C2V001.json', doc)
    print(json.dumps({'delta_sha256': dsha, 'successor_sha256': ssha, 'changed': sorted(rep['changed_paths']),
                      'max_active': {b: v['route_a_admission']['max_active'] for b, v in batches.items()}}, indent=1))


if __name__ == '__main__':
    main()

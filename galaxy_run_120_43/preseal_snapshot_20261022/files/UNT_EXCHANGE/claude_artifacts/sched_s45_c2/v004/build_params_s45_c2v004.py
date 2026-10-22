"""Builder for the sched_s45 v004 parameter successors (Claude2 sched_s45_c2, c2v004; V006 addendum A166).
build_params_s45_c2v003 (fb87a1f3) with the A166 deltas only.  Writes, by exclusive create, in v004/:
  * SCHED_DELTA_S45_C2V004.json            the scheduling delta (apply_sched_delta_s45_c2v002, unchanged, applies it to R9,
                                           and at H3 to C2); notes are APPENDED, never set;
  * RUN_CONFIG_DDO154_CX2V006R9_S45_C2V004.json  R9 (721c7230) + that delta, and DELTA_REPORT_R9_TO_S45_C2V004.json;
  * DIRECT_BATCH_PARAMS_S45_C2V004.json    the successor of DIRECT_BATCH_PARAMS_S45_C2V003A.json (4adc296b; A143 note 12):
                                           the hold predicate and the memory-sim max_active are removed; max_active is the
                                           packet's own design; RSS caps = RAM; packet_read, case lists and templates kept;
  * CAPS_S45_C2V004.json                   every DDO per-call cap with its basis.
A166 against v003: the campaign is the ORIGINAL campaign_c2v005 (d35d5d4a, R9's own pin: no machine gate, no entry patch);
max_concurrent stays R9's; RSS caps rise to RAM; the wall cap (A140 N4 constant), the output cap (80 GiB), the disk guard
(= the output cap, parent L1748) and the orphan wait (wall + 600 s, R9 relation) are kept.  Every DDO per-call cap comes
from the caps module (default caps_s45_c2v004.py in this folder; its sha256 is recorded in each output).  Reads R9, the
four templates_v004 plans, 4adc296b, CAPS_S45_C2V003.json and the campaign v005 bytes (for their pins); nothing else.
usage: python3 -I -B build_params_s45_c2v004.py
A140 N4 (root, after the step-2 receipts): copy caps_s45_c2v004.py to a NEW folder with DDO_TAIL_ON_WALL_CAP_S set, then
       python3 -I -B build_params_s45_c2v004.py --caps NEW/caps_X.py --caps-sha256 H --out-dir NEW --tag S45_C2V005
writes SCHED_DELTA_<tag>.json, RUN_CONFIG_DDO154_CX2V006R9_<tag>.json, DELTA_REPORT_R9_TO_<tag>.json,
DIRECT_BATCH_PARAMS_<tag>.json and CAPS_<tag>.json there (only the wall-derived leaves move).
"""
import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent                    # sched_s45_c2/v004
ART = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
R9 = ART / 'calib_tail_readiness_cx2/v006r9/RUN_CONFIG_DDO154_CX2V006R9_P128_MS128.json'
R9_SHA = '721c7230f3f3efde6f8406f13a52995ae321248829ab1ee64a2f522ad5582b8e'
APPLY = ART / 'sched_s45_c2/v002/apply_sched_delta_s45_c2v002.py'                # unchanged tool (v002)
APPLY_SHA = '2a18b280cb3a20ec5fb2668ff9798fe41fa02121f8003dc4e3164d7c2a9277f8'
CAMP_V005 = ART / 'calibration_orchestrator_c2/v005/campaign_c2v005.py'           # A166: the original campaign (R9's pin)
CAMP_V005_SHA = 'd35d5d4a62e6e5b632eb10c59bf4c82c2b1d744f6ceba609399c02baa5ecfeb2'
DIRECT_PREV = ART / 'sched_s45_c2/v003/DIRECT_BATCH_PARAMS_S45_C2V003A.json'     # A143 note 12: the N4 rebuild's predecessor
DIRECT_PREV_SHA = '4adc296bcb0ddcd154ec0dcea820908ac525d1d39ce00d633eecc4d0c95f87e7'
CAPS_PREV = ART / 'sched_s45_c2/v003/CAPS_S45_C2V003.json'
CAPS_PREV_SHA = '35f66b6a3152f985fe6edcbaeda2950e5b17e9f9f6026e5f6201052db1508f64'
TPL = ART / 'step4_launch_packet_cx1/templates_v004'
TEMPLATES = (('HEADLINE', 'HEADLINE_PLAN_TEMPLATE_CX1V004.json'), ('DIII', 'DIII_PLAN_TEMPLATE_CX1V004.json'),
             ('SENS_LO', 'SENS_LO_PLAN_TEMPLATE_CX1V004.json'), ('SENS_HI', 'SENS_HI_PLAN_TEMPLATE_CX1V004.json'))
PACKET = ART / 'step4_launch_packet_cx1'
PACKET_DESIGN = ('the launch packet\'s own route-A cap: Claude4\'s proposal 3 for every batch (impl/IMPLEMENTATION_INTERFACE_'
                 'CX1V003.md L36 "Root-approved max_active must be integer 1..6; Claude4\'s proposal is 3"; RUNBOOK_CX1V003.md '
                 'L9 and L13; each templates_v004 plan carries route_a_admission.max_active 3); guard c2v011 L329 accepts 1..6')
PACKET_MEMORY_CHECK = {
    'where': 'step4_guard_c2v011.py L331 (minimum_free_percent 25, poll 60, source /usr/bin/memory_pressure, ramp; '
             'RAMP_RULE_REQUIRED) and L332 (first_case_memory_exemption false; FIRST_MEMORY_BYPASS_REFUSED); '
             'step4_launcher_c2v012.py L36 (decision: 25 <= free) and L121 (memory_free probe)',
    'status': 'packet code, not a parameter: route_a_admission must carry these values exactly or the pinned guard refuses '
              'the batch; MEASURED non-binding (memory_pressure read 85-86 % free at 83 GB of run footprint, C2V003A scope)',
    'removal': 'needs a guard / launcher successor (code); A166 names no packet successor, so it is not built here'}


def sha_b(b):
    return hashlib.sha256(b).hexdigest()


def xwrite(path, obj=None, raw=None):
    data = raw if raw is not None else (json.dumps(obj, indent=1, sort_keys=True) + '\n').encode()
    with open(path, 'xb') as f:
        f.write(data)
    return sha_b(data)


def load_module(path, name, want_sha=None):
    raw = Path(path).read_bytes()
    if want_sha is not None and sha_b(raw) != want_sha:
        raise SystemExit('PIN_MISMATCH %s' % path)
    sp = importlib.util.spec_from_file_location(name, str(path))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m, sha_b(raw)


def pin(p):
    return {'path': str(p), 'sha256': sha_b(Path(p).read_bytes())}


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--caps', default=str(HERE / 'caps_s45_c2v004.py'))
    ap.add_argument('--caps-sha256', default=None, help='required with a non-default --caps')
    ap.add_argument('--out-dir', default=str(HERE))
    ap.add_argument('--tag', default='S45_C2V004')
    a = ap.parse_args(argv)
    out_dir, tag = Path(a.out_dir), a.tag
    if not out_dir.is_absolute() or not out_dir.is_dir():
        raise SystemExit('--out-dir must be an existing absolute directory')
    if not tag.replace('_', '').isalnum():
        raise SystemExit('--tag must be [A-Za-z0-9_]')
    if Path(a.caps) != HERE / 'caps_s45_c2v004.py' and not a.caps_sha256:
        raise SystemExit('--caps-sha256 is required with a non-default --caps')
    direct_name = 'DIRECT_BATCH_PARAMS_%s.json' % tag
    r9b = R9.read_bytes()
    if sha_b(r9b) != R9_SHA:
        raise SystemExit('R9 pin mismatch')
    prevb = DIRECT_PREV.read_bytes()
    if sha_b(prevb) != DIRECT_PREV_SHA:
        raise SystemExit('DIRECT_BATCH_PARAMS_S45_C2V003A (4adc296b) pin mismatch')
    if sha_b(CAPS_PREV.read_bytes()) != CAPS_PREV_SHA:
        raise SystemExit('CAPS_S45_C2V003 (35f66b6a) pin mismatch')
    camp = pin(CAMP_V005)
    if camp['sha256'] != CAMP_V005_SHA or json.loads(r9b)['campaign'] != camp:
        raise SystemExit('campaign_c2v005 pin differs from its bytes or from R9\'s campaign pin')
    K, ksha = load_module(a.caps, 'caps_module', a.caps_sha256)
    caps_pin = {'path': str(a.caps), 'sha256': ksha}
    A, _ = load_module(APPLY, 'apply_s45_c2v002', APPLY_SHA)
    on = K.tail_on_caps()
    wall = on['wall_cap_s']
    # ---- 1. delta + config successor
    delta = {'schema': 'SCHED_DELTA_%s' % tag,
             'predecessor': {'path': str(R9), 'sha256': R9_SHA},
             'caps_source': dict(caps_pin, constants={'DDO_TAIL_ON_WALL_CAP_S': K.DDO_TAIL_ON_WALL_CAP_S,
                                                      'DDO_TAIL_ON_OUTPUT_CAP_BYTES': K.DDO_TAIL_ON_OUTPUT_CAP_BYTES,
                                                      'DDO_TAIL_ON_RSS_CAP_BYTES': K.DDO_TAIL_ON_RSS_CAP_BYTES,
                                                      'RAM_BYTES': K.RAM_BYTES,
                                                      'DDO_ORPHAN_WAIT_MARGIN_S': K.DDO_ORPHAN_WAIT_MARGIN_S}),
             'set': {'campaign': camp,
                     'per_call.wall_cap_s': float(wall),
                     'per_call.rss_cap_bytes': on['rss_cap_bytes'],
                     'per_call.output_cap_bytes': on['output_cap_bytes'],
                     'disk_guard.per_call_bytes': on['output_cap_bytes'],
                     'orphan_wait.cap_s': K.orphan_wait_cap_s()},
             'append': {'notes': ' s45 c2v004 (sched_s45_c2, Claude2 2026-10-19, A166): scheduling successor only -- the '
                                 'original campaign_c2v005 (no machine gate; no memory admission), max_concurrent as R9, '
                                 'per-call wall %d s (DDO_TAIL_ON_WALL_CAP_S of %s %s), RSS %d B (physical RAM, A166) and '
                                 'output %d GiB, disk guard %d GiB per call, orphan wait wall + %d s; every physics input '
                                 'byte-identical to the predecessor.' % (
                                     wall, Path(a.caps).name, ksha[:8], on['rss_cap_bytes'], on['output_cap_bytes'] >> 30,
                                     on['output_cap_bytes'] >> 30, K.DDO_ORPHAN_WAIT_MARGIN_S)},
             'unchanged_on_purpose': {
                 'campaign': 'R9\'s own pin, campaign_c2v005 (d35d5d4a, sha from bytes): admits by max_concurrent, the '
                             'process budget and the campaign wall cap only; it imports no gate. It is the parent\'s own '
                             'CAMPAIGN_MODULE_NAME, so no entry patch is needed',
                 'max_concurrent': 'R9 value (A166 leaf list). campaign_c2v005 runs at most max_concurrent calls and only '
                                   'while the process budget fits (route-A weight 8, after-route-A 2, budget 17), so any '
                                   'value >= 5 leaves the process budget alone binding. At 1 the campaign is serial '
                                   '(README_SCHED_S45_C2V002 section 5, 120-call campaign, expected: 699.0 h as shipped at 1 '
                                   'against 235.3 / 219.0 h at 6); '
                                   'a wave whose serial time passes campaign_wall_cap_s leaves calls NOT_STARTED, which the '
                                   'parent classes INFRA (c75a889f L2731-2732). ROOT ITEM',
                 'process_budget': '17 (R9): campaign_c2v005 CPU-process accounting, validated by the parent L1727-1733',
                 'stage_aware_budget': 'true (R9)',
                 'campaign_wall_cap_s': '172800 (R9)',
                 'disk_guard.reserve_bytes': '20 GiB (R9)',
                 'disk_guard.measured_per_call_bytes': 'R9 value; root replaces it at H3 with the exact output bytes of the '
                                                       'largest measured tail-ON receipt (C4-6)'},
             'labels': {'per_call.rss_cap_bytes': 'A166: physical RAM (RAM_BYTES of %s): a cap stop is value-relevant '
                                                  '(A133 (f)), so a memory cap must never kill an honest run' % Path(a.caps).name,
                        'per_call.wall_cap_s': '%s DDO_TAIL_ON_WALL_CAP_S: %s' % (Path(a.caps).name, K.DDO_TAIL_ON_WALL_CAP_STATUS),
                        'per_call.output_cap_bytes': 'A140 N5, kept by A166 (a full disk fails runs): 80 GiB',
                        'disk_guard.per_call_bytes': '= per_call.output_cap_bytes (parent c75a889f L1748 requires >=; A147 L3-01)',
                        'orphan_wait.cap_s': 'R9 relation kept: wall cap + 600 s (derived from the wall constant; below the '
                                             'wall a resume returns ORPHANS_STILL_RUNNING, c75a889f L2694-2707, while a call '
                                             'may still run legitimately)'},
             'parent_entry_patch': None,
             'removed_vs_s45_c2v003': [
                 'campaign_s45_c2v003 (011a2677) and machine_gate_s45_c2v003 (736a3438): memory limits d1 / d2 (hard 83, '
                 'knee 72, vm_stat pool), reservations, spikes, growth, NGC / twin classes, TWIN_HOLD, route-A cap 2, core '
                 'limit, swap rule, spacing, warm-up and probe (A166)',
                 'max_concurrent 12 (DERIVED from the gate\'s core limit) -> R9\'s value',
                 'parent_entry_patch CAMPAIGN_MODULE_NAME = campaign_s45_c2v003 (not needed with campaign_c2v005)']}
    dsha = xwrite(out_dir / ('SCHED_DELTA_%s.json' % tag), delta)
    out, rep = A.apply(r9b, delta)
    if out is None:
        raise SystemExit('delta refused: %s' % rep)
    ssha = xwrite(out_dir / ('RUN_CONFIG_DDO154_CX2V006R9_%s.json' % tag), raw=out)
    rep['delta_sha256'] = dsha
    rep['apply_tool'] = {'path': str(APPLY), 'sha256': APPLY_SHA}
    xwrite(out_dir / ('DELTA_REPORT_R9_TO_%s.json' % tag), rep)
    # ---- 2. direct-batch params: successor of 4adc296b
    prev = json.loads(prevb)
    doc = copy.deepcopy(prev)
    for name, fname in TEMPLATES:
        tb = (TPL / fname).read_bytes()
        if sha_b(tb) != prev['batches'][name]['template']['sha256']:
            raise SystemExit('template pin mismatch: %s' % fname)
        t = json.loads(tb)
        tail = {c['case']: c.get('tail_on') for c in t['calls']}
        if sorted(tail) != sorted(prev['batches'][name]['caps_per_case']):
            raise SystemExit('case list differs from 4adc296b: %s' % name)
        doc['batches'][name]['caps_per_case'] = {c: (K.tail_on_caps() if tail[c] else K.tail_off_caps()) for c in tail}
        tra, ra = t['route_a_admission'], dict(prev['batches'][name]['route_a_admission'])
        if {k: v for k, v in ra.items() if k != 'max_active'} != {k: v for k, v in tra.items() if k != 'max_active'}:
            raise SystemExit('route_a_admission fields differ from the template: %s' % name)
        ra['max_active'] = tra['max_active']
        doc['batches'][name]['route_a_admission'] = ra
        doc['batches'][name]['max_active_basis'] = {'rule': PACKET_DESIGN, 'template': prev['batches'][name]['template']}
    doc['batches']['POST_S1']['caps_per_case'] = {c: K.tail_on_caps() for c in prev['batches']['POST_S1']['case_order']}
    doc['batches']['POST_S1']['max_active_basis'] = {
        'rule': 'no template; max_active %d = n_calls %d <= the packet design 3, so the cap does not bind (%s)' % (
            prev['batches']['POST_S1']['route_a_admission']['max_active'], prev['batches']['POST_S1']['n_calls'],
            PACKET_DESIGN), 'template': None}
    del doc['hold_predicate']
    doc['schema'] = direct_name[:-5]
    doc['supersedes'] = {'path': str(DIRECT_PREV), 'sha256': DIRECT_PREV_SHA,
                         'what_changes': 'A166: hold_predicate removed; route_a_admission.max_active = the packet design '
                                         '(the memory-sim values are removed) and max_active_basis; every rss_cap_bytes = '
                                         'RAM; tail-ON wall = DDO_TAIL_ON_WALL_CAP_S; scope, basis, still_root_rulings, '
                                         'packet_memory_check; nothing else'}
    doc['basis'] = {'caps': '%s (%s): tail-ON wall DDO_TAIL_ON_WALL_CAP_S %d s (%s), RSS %d B (physical RAM, A166), output '
                            '%d GiB (A140 N5); DIII tail-OFF wall %d s and output %d GiB unchanged (R-D5), RSS %d B (A166)' % (
                                Path(a.caps).name, ksha[:8], wall, K.DDO_TAIL_ON_WALL_CAP_STATUS, on['rss_cap_bytes'],
                                on['output_cap_bytes'] >> 30, K.tail_off_caps()['wall_cap_s'],
                                K.tail_off_caps()['output_cap_bytes'] >> 30, K.tail_off_caps()['rss_cap_bytes']),
                    'max_active': PACKET_DESIGN}
    doc['packet_memory_check'] = PACKET_MEMORY_CHECK
    doc['scope'] = ('Parameters only for Codex1\'s guarded step-4 packet (the guard, launcher and binder in packet_read, '
                    'unchanged): root copies route_a_admission into C1 cfg.route_a_admission and caps_per_case into cfg.caps '
                    '(ROOT_CAPS_BINDING). No packet code changes. c2v004 (A166): no memory lever is set here. max_active is '
                    'the packet\'s own design, there is no hold predicate, and every RSS cap is physical RAM. The packet\'s '
                    'own start rule is unchanged packet code (packet_memory_check): free memory >= 25 % by memory_pressure, '
                    'the predecessor\'s first completed route-A iteration, the disk start bound and root\'s core-priority '
                    'attestation (guard c2v011 L333: no campaign or step-2 route A running).')
    rulings = ['R-D8 (tail-ON caps): RSS = physical RAM (A166) replaces both the 29 GiB proposal and the 64 GiB cap',
               'R-D5 (DIII caps: wall 13 h instead of 12 h; RSS = RAM, A166)',
               'R-D18 / S4-R-D8 route-A cap: max_active = the packet design 3 (HEADLINE, SENS_LO, SENS_HI, DIII); POST_S1 2 '
               '(n_calls). The memory-sim values (HEADLINE and SENS 1, DIII 4) are removed (A166)',
               'A166 residual: the packet\'s memory_pressure >= 25 % start check is packet code (packet_memory_check); '
               'removing it needs a guard / launcher successor']
    if str(K.DDO_TAIL_ON_WALL_CAP_STATUS).startswith('PROVISIONAL'):
        rulings.append('A140 N4: DDO tail-ON wall cap re-derived from the step-2 receipts before W1 (one constant, '
                       'DDO_TAIL_ON_WALL_CAP_S in a caps successor; rebuild with build_params_s45_c2v004.py --caps '
                       '--caps-sha256 --out-dir --tag)')
    doc['still_root_rulings'] = rulings
    psha = xwrite(out_dir / direct_name, doc)
    # ---- 3. caps record (DDO only; A166 build 2, the S0 kit C2V003, owns the NGC commands)
    rec = {'schema': 'CAPS_%s' % tag, 'caps_module': caps_pin, 'ram_bytes': K.RAM_BYTES,
           'ddo_tail_on': dict(K.tail_on_caps(), wall_status=K.DDO_TAIL_ON_WALL_CAP_STATUS,
                               rss_basis='A166: physical RAM (was 64 GiB)',
                               output_basis='A140 N5 (0706): 80 GiB; kept by A166'),
           'ddo_tail_off_diii': dict(K.tail_off_caps(), rss_basis='A166: physical RAM (was 16 GiB)'),
           'orphan_wait_cap_s': K.orphan_wait_cap_s(),
           'predecessor': {'path': str(CAPS_PREV), 'sha256': CAPS_PREV_SHA},
           'ngc': 'not carried: A166 build 2 (S0 kit C2V003) owns the NGC S0 and twin commands, with RSS = RAM there'}
    csha = xwrite(out_dir / ('CAPS_%s.json' % tag), rec)
    print(json.dumps({'out_dir': str(out_dir), 'tag': tag, 'delta_sha256': dsha, 'successor_sha256': ssha, 'direct_sha256': psha,
                      'caps_record_sha256': csha, 'caps_module_sha256': ksha, 'changed': sorted(rep['changed_paths'])}, indent=1))


if __name__ == '__main__':
    main()

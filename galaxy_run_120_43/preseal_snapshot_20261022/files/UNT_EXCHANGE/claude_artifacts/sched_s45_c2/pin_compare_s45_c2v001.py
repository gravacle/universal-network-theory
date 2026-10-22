"""Byte comparison of every physics input the sched_s45 successors touch or sit next to (Claude2 sched_s45_c2, c2v001).
For each pinned file: the sha256 its pin records and the sha256 of its bytes now.  For the RUN_CONFIG successor: the
canonical sha256 of every top-level key against R9, and of numerics in particular.  For the four direct-batch templates:
every call's spec and driver pin against its bytes.  Reads bytes only (no result, array or diagnostic file).
usage: python3 -I -B pin_compare_s45_c2v001.py OUT.json
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ART = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
R9 = ART / 'calib_tail_readiness_cx2/v006r9/RUN_CONFIG_DDO154_CX2V006R9_P128_MS128.json'
SUCC = HERE / 'RUN_CONFIG_DDO154_CX2V006R9_S45_C2V001.json'
TPL = ART / 'step4_launch_packet_cx1/templates_v004'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def canon(o):
    return hashlib.sha256(json.dumps(o, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def main(out):
    r9, su = json.loads(R9.read_text()), json.loads(SUCC.read_text())
    rows = []

    def pin(label, p, want):
        got = sha(p)
        rows.append({'label': label, 'path': str(p), 'pinned': want, 'bytes': got, 'equal': got == want})
    for k in ('driver', 'monitor', 'coordinate_spec', 'coordinate_spec_addendum', 'taxonomy', 'observation_region'):
        pin('successor.%s' % k, su[k]['path'], su[k]['sha256'])
    pin('successor.anchor.registered_point', su['anchor']['registered_point']['path'], su['anchor']['registered_point']['sha256'])
    for k in ('custody_deriver', 'state_enumerator'):
        pin('successor.tail_readiness.%s' % k, su['tail_readiness'][k]['path'], su['tail_readiness'][k]['sha256'])
    pin('successor.python', su['python']['path'], su['python']['sha256'])
    pin('R9 config (predecessor, unchanged)', R9, '721c7230f3f3efde6f8406f13a52995ae321248829ab1ee64a2f522ad5582b8e')
    pin('NGC driver cx3r008 (step 5; not touched)',
        ART / 'ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py',
        '577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377')
    for f in sorted(TPL.glob('*_PLAN_TEMPLATE_CX1V004.json')):
        t = json.loads(f.read_text())
        for c in t['calls']:
            pin('%s.%s.spec' % (t['batch'], c['case']), c['spec']['path'], c['spec']['sha256'])
            pin('%s.%s.driver' % (t['batch'], c['case']), c['driver']['path'], c['driver']['sha256'])
    keys = sorted(set(r9) | set(su))
    top = {k: {'R9': canon(r9.get(k)), 'successor': canon(su.get(k)), 'equal': canon(r9.get(k)) == canon(su.get(k))} for k in keys}
    changed = sorted(k for k, v in top.items() if not v['equal'])
    doc = {'schema': 'SCHED_S45_PHYSICS_PIN_COMPARE_C2V001', 'n_pins': len(rows), 'all_pins_equal': all(r['equal'] for r in rows),
           'numerics_canonical_sha256': {'R9': canon(r9['numerics']), 'successor': canon(su['numerics']),
                                         'equal': canon(r9['numerics']) == canon(su['numerics'])},
           'top_level_keys_changed': changed,
           'top_level_keys_changed_are_scheduling_only': set(changed) <= {'campaign', 'max_concurrent', 'per_call', 'disk_guard',
                                                                         'orphan_wait', 'notes'},
           'pins': rows, 'top_level': top}
    with open(out, 'x') as f:
        json.dump(doc, f, indent=1)
        f.write('\n')
    print(json.dumps({k: doc[k] for k in ('n_pins', 'all_pins_equal', 'numerics_canonical_sha256', 'top_level_keys_changed',
                                          'top_level_keys_changed_are_scheduling_only')}, indent=1))


if __name__ == '__main__':
    main(sys.argv[1])

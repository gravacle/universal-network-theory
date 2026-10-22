"""certificates_v004 (root A68 "Records"): LO_CERT_V004_MS128 = LO_CERT_V003_MS128 (9fdb897a) with the explicit field
source_gas_M_s = 128 that compare r7 g_LO / FIELDS_R7 LO require (A57 ruling 1, A58 RI-06; Codex1 0023, Codex3 0601, r7 NEW-48).
No number is recomputed.  Every V003 key is carried byte-for-byte in canonical JSON except `producer` (now this tool; the
computing tool is kept as `numbers_producer`).  Added keys: source_gas_M_s, numbers_producer, successor_of, successor_change,
source_gas_M_s_evidence, decisions_v004.  source_gas_M_s is not asserted: it is read from the three places V003 records the
source M_s (gas_M_s, tail_config_gas.M_s, build.roster_gas.M_s) and the tool refuses unless all three are the integer 128.
Outputs (exclusive create): gates/LO_CERT_V004_MS128.json, out/LO_V004_SUCCESSOR_DIFF_V001.json.
Usage: python3 -I -B build_lo_v004_c2v001.py"""
import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
ART = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
V003 = (ART / 'tail_scheme_impl_c2/certificates_v003/gates/LO_CERT_V003_MS128.json',
        '9fdb897ae3b80dd6a3d2cf9ff273619dbf5fa419405cc8dacd1fa77ee2539268')
ADD_V005 = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/'
                'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md')
CHANGED = {'producer'}
ADDED = ('source_gas_M_s', 'numbers_producer', 'successor_of', 'successor_change', 'source_gas_M_s_evidence', 'decisions_v004')


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def canon(o):
    return json.dumps(o, sort_keys=True, separators=(',', ':'), allow_nan=False)


def strict_load(raw):
    def hook(pairs):
        d = {}
        for k, v in pairs:
            if k in d:
                raise SystemExit('REFUSED: duplicate key %r' % k)
            d[k] = v
        return d
    return json.loads(raw, object_pairs_hook=hook)


def write_new(p, obj):
    data = (json.dumps(obj, indent=1, allow_nan=False) + '\n').encode()
    fd = os.open(str(p), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(fd, 'wb') as f:
        f.write(data)
    return hashlib.sha256(data).hexdigest()


def main():
    raw = V003[0].read_bytes()
    if hashlib.sha256(raw).hexdigest() != V003[1]:
        raise SystemExit('REFUSED: LO_CERT_V003_MS128 pin')
    v3 = strict_load(raw)
    if 'source_gas_M_s' in v3:
        raise SystemExit('REFUSED: V003 already carries source_gas_M_s')
    ev = {'gas_M_s': v3.get('gas_M_s'), 'tail_config_gas/M_s': (v3.get('tail_config_gas') or {}).get('M_s'),
          'build/roster_gas/M_s': ((v3.get('build') or {}).get('roster_gas') or {}).get('M_s')}
    if not all(type(x) is int and x == 128 for x in ev.values()):
        raise SystemExit('REFUSED: V003 source M_s fields are not all the integer 128: %r' % ev)
    me = {'path': str(Path(__file__).resolve()), 'sha256': sha(__file__)}
    v4 = {}
    for k, v in v3.items():                                          # V003 key order kept; the new field follows gas_M_s
        v4[k] = me if k == 'producer' else v
        if k == 'gas_M_s':
            v4['source_gas_M_s'] = 128
    v4['numbers_producer'] = v3['producer']
    v4['successor_of'] = {'LO_CERT_V003_MS128': {'path': str(V003[0]), 'sha256': V003[1]}}
    v4['successor_change'] = ('root A68 Records: LO_CERT_V004_MS128 = LO_CERT_V003_MS128 + the explicit field source_gas_M_s (the gas M_s '
                              'of the source the certificate was computed with; FIELDS_R7 LO, A57 ruling 1, A58 RI-06), numbers '
                              'unchanged.  No number recomputed; every V003 key is canonical-JSON equal here except producer (this '
                              'successor tool; the computing tool is numbers_producer).  V003 stays unedited.')
    v4['source_gas_M_s_evidence'] = {'read_from_V003': ev, 'rule': 'all three V003 source-M_s fields equal the integer 128, else refused'}
    v4['decisions_v004'] = {'path': str(ADD_V005), 'sha256_at_read': sha(ADD_V005), 'cited': 'A57 ruling 1, A58 RI-06, A68 Records'}
    # ---- diff check: numbers unchanged
    same = sorted(k for k in v3 if k not in CHANGED and canon(v3[k]) == canon(v4[k]))
    differ = sorted(k for k in v3 if canon(v3[k]) != canon(v4.get(k)))
    added = sorted(set(v4) - set(v3))
    if differ != sorted(CHANGED) or added != sorted(ADDED) or len(same) != len(v3) - len(CHANGED):
        raise SystemExit('REFUSED: diff not as declared: differ=%r added=%r' % (differ, added))
    h = write_new(OUT / 'gates/LO_CERT_V004_MS128.json', v4)
    rb = (OUT / 'gates/LO_CERT_V004_MS128.json').read_bytes()
    back = strict_load(rb)
    assert canon(back) == canon(v4) and hashlib.sha256(rb).hexdigest() == h
    diff = {'schema': 'UVT_LO_SUCCESSOR_DIFF_C2V001', 'producer': me,
            'old': {'path': str(V003[0]), 'sha256': V003[1]}, 'new': {'path': str(OUT / 'gates/LO_CERT_V004_MS128.json'), 'sha256': h},
            'v003_keys': len(v3), 'keys_canonically_equal': len(same), 'keys_changed': differ, 'keys_added': added,
            'numbers_unchanged': True, 'source_gas_M_s': 128, 'source_gas_M_s_evidence': ev,
            'shells_max_over_tau': [[s['range_inverse_kpc'], s['max_over_tau']] for s in back['shells']],
            'summed_max_over_tau': back['summed_max_over_tau']}
    hd = write_new(OUT / 'out/LO_V004_SUCCESSOR_DIFF_V001.json', diff)
    print('LO_CERT_V004_MS128', h)
    print('LO_V004_SUCCESSOR_DIFF_V001', hd, 'equal', len(same), 'changed', differ, 'added', added)


if __name__ == '__main__':
    main()

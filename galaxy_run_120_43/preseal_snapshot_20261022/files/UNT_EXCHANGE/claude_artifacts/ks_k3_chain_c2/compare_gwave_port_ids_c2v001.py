"""Port differential at case level (ks_k3_chain_c2 G-wave c2v001): every ported suite's G-wave run against its run of
record (the wave-1 port run, the offset_b1 run of record, or the r5 closure record).

  python3 -I -B compare_gwave_port_ids_c2v001.py INPUT.json OUT.json      (OUT must not exist)

INPUT: {"pairs": [{"suite", "record": path, "new": path, "added_ok": [id prefix, ...], "removed_ok": {id: reason}}]}.
For each pair: the case ids of each run, the ids only in one run, and every common id whose pass flag differs. A pair
AGREES iff every common id has the same pass flag, every id only in the new run starts with an allowed prefix (cases
the G-wave adds) and every id only in the record is listed with its reason (cases a port replaces). Hashes from bytes.
"""
import hashlib
import json
import sys


def flags(doc):
    for key, idk, okf in (('cases', 'id', lambda r: r['passed']), ('tests', 'name', lambda r: r['passed']),
                          ('checks', 'name', lambda r: r['passed'])):
        if isinstance(doc.get(key), list):
            return {r[idk]: bool(okf(r)) for r in doc[key]}
    rows = doc.get('results')
    if isinstance(rows, list) and rows and 'result' in rows[0]:
        return {r['id']: r['result'] == 'PASS' for r in rows}
    if isinstance(rows, list):
        return {r['id']: bool(r['passed']) for r in rows}
    raise ValueError('unknown results layout')


def pin(p):
    with open(p, 'rb') as f:
        raw = f.read()
    return {'path': p, 'sha256': hashlib.sha256(raw).hexdigest()}, json.loads(raw)


def main():
    if not (sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1):
        raise SystemExit('REFUSED: python3 -I -B required')
    inp_pin, inp = pin(sys.argv[1])
    out = {'schema': 'KS_GWAVE_PORT_CASE_DIFFERENTIAL_C2V001', 'input': inp_pin, 'pairs': []}
    for p in inp['pairs']:
        rp, rd = pin(p['record'])
        np_, nd = pin(p['new'])
        a, b = flags(rd), flags(nd)
        only_rec, only_new = sorted(set(a) - set(b)), sorted(set(b) - set(a))
        diff = sorted(k for k in set(a) & set(b) if a[k] != b[k])
        bad_new = [k for k in only_new if not any(k.startswith(x) for x in p.get('added_ok', []))]
        bad_rec = [k for k in only_rec if k not in p.get('removed_ok', {})]
        out['pairs'].append({'suite': p['suite'], 'record': rp, 'new': np_, 'n_record': len(a), 'n_new': len(b),
                             'record_all_pass': all(a.values()), 'new_all_pass': all(b.values()),
                             'common': len(set(a) & set(b)), 'pass_flag_differs': diff, 'only_in_new': only_new,
                             'only_in_record': only_rec, 'only_in_record_reasons': {k: p.get('removed_ok', {}).get(k) for k in only_rec},
                             'verdict': 'AGREE' if not diff and not bad_new and not bad_rec else 'DISAGREE'})
    out['verdict'] = 'AGREE' if all(x['verdict'] == 'AGREE' for x in out['pairs']) else 'DISAGREE'
    with open(sys.argv[2], 'xb') as f:
        f.write(json.dumps(out, indent=1, sort_keys=True).encode() + b'\n')
    print(json.dumps({'verdict': out['verdict'], 'pairs': [{k: x[k] for k in ('suite', 'n_record', 'n_new', 'verdict', 'pass_flag_differs',
                                                                               'only_in_new', 'only_in_record')} for x in out['pairs']]}, indent=1))
    return 0 if out['verdict'] == 'AGREE' else 1


if __name__ == '__main__':
    sys.exit(main())

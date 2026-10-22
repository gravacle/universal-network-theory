"""Case-by-case differential of each ported predecessor suite run (successor under test) against the predecessor
suite's own run of record (ks_k3_chain_c2 c2v001). Read-only on the runs of record; writes one JSON by exclusive create.

  python3 -I -B compare_port_runs_c2v001.py --ks-dir DIR --out DIR/synthetic/<new>.json PORTS_JSON

PORTS_JSON maps suite -> {"record": path, "port": path}. Per suite: the case ids, the pass flag of every case, and the
case text (observed/detail) after normalization (absolute paths under the two run roots -> <ROOT>, 64/16/12-hex
strings -> <HEX>, timestamps -> <T>, durations -> <S>). A case whose normalized text differs is listed with both texts.
"""
import argparse
import hashlib
import json
import os
import re

ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'


def cases(doc):
    if isinstance(doc.get('cases'), list):
        return [(c['id'], c['passed'], c.get('observed')) for c in doc['cases']]
    if isinstance(doc.get('results'), list) and doc['results'] and 'result' in doc['results'][0]:
        return [(c['id'], c['result'] == 'PASS', c.get('detail')) for c in doc['results']]
    if isinstance(doc.get('results'), list):
        return [(c['id'], c['passed'], c.get('observed')) for c in doc['results']]
    if isinstance(doc.get('tests'), list):
        return [(c['name'], c['passed'], c.get('detail')) for c in doc['tests']]
    if isinstance(doc.get('checks'), list):
        return [(c['name'], c['passed'], c.get('detail')) for c in doc['checks']]
    raise SystemExit('unknown results format')


TRUNC = 550       # the cp1 / proof-side suites cut a case text at 600 characters, before any normalization


def norm(text, roots):
    t = text if isinstance(text, str) else json.dumps(text, sort_keys=True, default=str)
    for r in sorted(roots, key=len, reverse=True):
        t = t.replace(r, '<ROOT>')
    t = re.sub(r'_PORT_ks[0-9a-z_]*?c2v00[0-9]', '', t)
    t = re.sub(r'_ks[0-9][a-z0-9]*_c2v00[0-9]', '', t)
    t = t.replace('s1k3_c2v002', 's1k3_c2v001')
    t = re.sub(r'/(Users|private|tmp)/[^\s\'",)\]]*', '<PATH>', t)
    t = re.sub(r'\d{8}T\d{6}Z', '<T>', t)
    t = re.sub(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(\+00:00|Z)?', '<T>', t)
    t = re.sub(r'(?<![0-9a-f])\d+\.\d+(e[+-]?\d+)?', '<F>', t)
    t = re.sub(r'[0-9a-f]{6,}', '<HEX>', t)
    t = re.sub(r'\d{4,}', '<N>', t)
    t = re.sub(r'("pid"|\'pid\'|"polls"|\'polls\'): \d+', r'\1: <N>', t)
    return t


def same_text_fn(a_raw, b_raw, roots):
    a, b = norm(a_raw, roots), norm(b_raw, roots)
    la = len(a_raw if isinstance(a_raw, str) else json.dumps(a_raw, sort_keys=True, default=str))
    lb = len(b_raw if isinstance(b_raw, str) else json.dumps(b_raw, sort_keys=True, default=str))
    if la >= TRUNC or lb >= TRUNC:              # a truncated text: compare the normalized common prefix
        n = max(0, min(len(a), len(b)) - 40)
        return a[:n] == b[:n], a, b, True
    return a == b, a, b, False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ks-dir', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('ports')
    a = ap.parse_args()
    ks = os.path.realpath(a.ks_dir)
    if not os.path.abspath(a.out).startswith(ks + '/synthetic/'):
        raise SystemExit('REFUSED: --out must be under <ks-dir>/synthetic/')
    with open(a.ports) as f:
        ports = json.load(f)
    report = {'schema': 'KS_K3_CHAIN_PORT_DIFFERENTIAL_C2V001', 'suites': {}}
    for name, p in ports.items():
        with open(p['record'], 'rb') as f:
            rraw = f.read()
        with open(p['port'], 'rb') as f:
            praw = f.read()
        rec, port = json.loads(rraw), json.loads(praw)
        roots = [os.path.dirname(os.path.dirname(p['record'])), os.path.dirname(p['record']), os.path.dirname(os.path.dirname(p['port'])),
                 os.path.dirname(p['port'])] + p.get('extra_roots', [])
        rc, pc = cases(rec), cases(port)
        rmap, pmap = {i: (ok, t) for i, ok, t in rc}, {i: (ok, t) for i, ok, t in pc}
        diffs = {}
        same_text, truncated = 0, 0
        for i in rmap:
            if i in pmap:
                eq, a_, b_, tr = same_text_fn(rmap[i][1], pmap[i][1], roots)
                truncated += tr
                if eq:
                    same_text += 1
                else:
                    diffs[i] = {'record': a_[:600], 'port': b_[:600], 'pass_flags': [rmap[i][0], pmap[i][0]]}
        expected_text_diffs = p.get('expected_text_diffs', {})
        unexplained = sorted(set(diffs) - set(expected_text_diffs))
        report['suites'][name] = {
            'record': {'path': p['record'], 'sha256': hashlib.sha256(rraw).hexdigest()},
            'port': {'path': p['port'], 'sha256': hashlib.sha256(praw).hexdigest()},
            'n_record': len(rc), 'n_port': len(pc), 'ids_only_in_record': sorted(set(rmap) - set(pmap)),
            'ids_only_in_port': sorted(set(pmap) - set(rmap)),
            'all_pass_record': all(ok for _, ok, _ in rc), 'all_pass_port': all(ok for _, ok, _ in pc),
            'pass_flags_equal_on_common_ids': all(rmap[i][0] == pmap[i][0] for i in rmap if i in pmap),
            'normalized_text_equal': same_text, 'compared_as_truncated_prefix': truncated, 'text_differences': diffs,
            'expected_text_diffs': expected_text_diffs, 'unexplained_text_differences': unexplained}
    report['verdict'] = 'AGREE' if all(s['pass_flags_equal_on_common_ids'] and s['all_pass_port'] and not s['unexplained_text_differences']
                                       and set(s['ids_only_in_record']) <= set(ports[n].get('expected_missing', []))
                                       and set(s['ids_only_in_port']) <= set(ports[n].get('expected_new', []))
                                       for n, s in report['suites'].items()) else 'DIFFER'
    raw = (json.dumps(report, sort_keys=True, indent=1) + '\n').encode()
    with open(a.out, 'xb') as f:
        f.write(raw)
    print(json.dumps({'verdict': report['verdict'], 'out': a.out, 'sha256': hashlib.sha256(raw).hexdigest(),
                      'suites': {n: {k: s[k] for k in ('n_record', 'n_port', 'pass_flags_equal_on_common_ids', 'normalized_text_equal',
                                                       'unexplained_text_differences', 'ids_only_in_record', 'ids_only_in_port')}
                                 for n, s in report['suites'].items()}}, indent=1))


if __name__ == '__main__':
    main()

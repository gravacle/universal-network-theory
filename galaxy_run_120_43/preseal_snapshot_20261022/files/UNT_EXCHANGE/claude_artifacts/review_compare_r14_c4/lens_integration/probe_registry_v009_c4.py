# Claude4 lens_integration: the real registry of record V009 (32ddadcb) through r13's and r14's own loaders, and a V010-like
# in-memory variant (V009 with gate_records.I4 = PRODUCED_AFTER_THE_SEAL, as A114.2 registers it). Read-only; run ONLY through
# tools/run_fenced_c4st2.py. Writes one JSON into out/<run>/ in this review folder.
# usage: python3 -I -B tools/run_fenced_c4st2.py probe_registry_v009_c4.py OUTDIR_NAME
import copy, hashlib, importlib.util, json, sys, time
from pathlib import Path

REVIEW = Path(__file__).resolve().parent
OUT = REVIEW / 'out' / sys.argv[1]
OUT.mkdir(parents=True, exist_ok=False)
V009 = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/producer_registry_c3/out/PRODUCER_REGISTRY_C3V009.json',
        '32ddadcb7567213f42288004f19def122da1d8c4db1a426f0f888bc3242484e8')
SRC = {'r14': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r14/kmax_tail_compare_c2v007_r14_cx1v001.py',
               'f3f9ba7ec4439933ab88c7623a6ede5b04763b83f0610b1917393362f33c67d7'),
       'r13': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/kmax_tail_compare_c2v007_r13_cx3v001.py',
               'f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157')}
RES = {'utc_start': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'checks': []}


def rec(name, ok, **info):
    RES['checks'].append(dict({'check': name, 'ok': bool(ok)}, **info))
    print('%-4s %s %s' % ('OK' if ok else 'FAIL', name, json.dumps(info, default=str)[:500]))


raw = Path(V009[0]).read_bytes()
rec('V009_sha_from_bytes', hashlib.sha256(raw).hexdigest() == V009[1], got=hashlib.sha256(raw).hexdigest())
M = {}
for k, (p, h) in SRC.items():
    b = Path(p).read_bytes()
    assert hashlib.sha256(b).hexdigest() == h, k
    s = importlib.util.spec_from_file_location('c4reg_cmp_' + k, p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    M[k] = m
norm = {}
for k, m in M.items():
    try:
        r = m.load_producer_registry(V009[0], V009[1])
        norm[k] = {kk: (sorted(map(list, v)) if isinstance(v, frozenset) else
                        ({g: (sorted(map(list, x)) if isinstance(x, frozenset) and x and isinstance(next(iter(x)), tuple) else
                              (sorted(x) if isinstance(x, frozenset) else x)) for g, x in v.items()} if isinstance(v, dict) else v))
                   for kk, v in r.items()}
        rec(k + '_loads_V009', True, gate_records_I4=norm[k]['gate_records'].get('I4'))
    except SystemExit as e:
        rec(k + '_loads_V009', False, code=getattr(e, 'refusal_code', None), msg=str(e)[:300])
if len(norm) == 2:
    rec('V009_normalized_identically_by_r13_and_r14', json.dumps(norm['r13'], sort_keys=True, default=str) == json.dumps(norm['r14'], sort_keys=True, default=str))
obj = json.loads(raw)
for gate, want14, want13 in (('I4', True, False), ('EPS', False, False), ('B0_N3', False, False), ('B0_RO1', False, False), ('GQ', False, False)):
    o = copy.deepcopy(obj)
    o['gate_records'][gate] = M['r14'].GATE_RECORD_AFTER_SEAL
    got = {}
    for k, m in M.items():
        try:
            m.producer_registry_from_obj(o, sha=None, path=None)
            got[k] = (True, None)
        except SystemExit as e:
            got[k] = (False, getattr(e, 'refusal_code', None))
    rec('V009_with_token_on_%s: r14 %s, r13 %s' % (gate, 'accepts' if want14 else 'refuses', 'accepts' if want13 else 'refuses'),
        got['r14'][0] is want14 and got['r13'][0] is want13, r14=got['r14'], r13=got['r13'])
RES['utc_end'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
RES['n_ok'] = sum(1 for c in RES['checks'] if c['ok'])
RES['n'] = len(RES['checks'])
(OUT / 'REGISTRY_V009_PROBE_C4.json').write_text(json.dumps(RES, indent=1, sort_keys=True, default=str) + '\n')
print('REGISTRY PROBE %d/%d ok' % (RES['n_ok'], RES['n']))
raise SystemExit(0 if RES['n_ok'] == RES['n'] else 1)

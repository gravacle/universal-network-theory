# verify_pins_r5chk.py -- hash every {path, sha256} pin in a JSON document from bytes (r5_check helper).
# usage: python3 -I -B verify_pins_r5chk.py DOC.json OUT.json
# Never opens a path in a forbidden class (runs_ext, UVT_*, C5H run, target-data names); those are listed as SKIPPED.
import sys, json, hashlib, os
docp, outp = sys.argv[1:3]
doc = json.load(open(docp))
FORBID = ('runs_ext', '/UVT_', 'C5H_RUN', 'KMAX_A2F10_C5H', 'rotmod', 'SPARC', 'MassModels', 'Vobs', 'sparc')
def walk(x, p=''):
    if isinstance(x, dict):
        if isinstance(x.get('path'), str) and isinstance(x.get('sha256'), str):
            yield p, x['path'], x['sha256']
        for k, v in x.items():
            yield from walk(v, p + '/' + k)
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from walk(v, p + '[%d]' % i)
base = os.path.dirname(os.path.abspath(docp))
rows = []
for p, path, sha in walk(doc):
    r = {'at': p, 'path': path, 'pinned': sha}
    full = path if os.path.isabs(path) else os.path.join(base, path)
    if any(f in path for f in FORBID):
        r['state'] = 'SKIPPED_FORBIDDEN_CLASS'
    elif not (len(sha) == 64 and all(c in '0123456789abcdef' for c in sha)):
        r['state'] = 'NOT_A_SHA (' + sha[:40] + ')'
    elif not os.path.isfile(full):
        r['state'] = 'MISSING'
    else:
        h = hashlib.sha256(open(full, 'rb').read()).hexdigest()
        r['actual'] = h
        r['state'] = 'OK' if h == sha else 'MISMATCH'
    rows.append(r)
cnt = {}
for r in rows:
    k = r['state'].split(' ')[0]
    cnt[k] = cnt.get(k, 0) + 1
res = {'schema': 'R5CHK_PIN_VERIFY_V001', 'doc': docp,
       'doc_sha256': hashlib.sha256(open(docp, 'rb').read()).hexdigest(), 'counts': cnt, 'rows': rows}
with open(outp, 'x') as f:
    json.dump(res, f, indent=1)
print(json.dumps(cnt))
for r in rows:
    if r['state'] != 'OK':
        print(r['state'], r['at'], r['path'])

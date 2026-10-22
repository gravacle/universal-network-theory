# Claude4 lens_integration: every {path, sha256[, bytes]} entry of the r14 HASHES manifests (V001 8b92153a, V002 46b811c1) and of
# VALIDATION_R14_CX1V001 (930ca7bc) evidence, re-hashed from bytes. Read-only; run ONLY through tools/run_fenced_c4st2.py (a protected
# path would be refused by the fence and reported, never read).
# usage: python3 -I -B tools/run_fenced_c4st2.py probe_hashes_c4.py OUTDIR_NAME
import hashlib, json, sys, time
from pathlib import Path

REVIEW = Path(__file__).resolve().parent
OUT = REVIEW / 'out' / sys.argv[1]
OUT.mkdir(parents=True, exist_ok=False)
R14 = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r14'
MANIFESTS = ((R14 + '/HASHES_R14_CX1V001.json', '8b92153a0200953df2e4df8e1993cfcade58ddc4b6b5536439359a9119be5a8f'),
             (R14 + '/HASHES_R14_CX1V002.json', '46b811c188834d8a72293d60d6ed792c8130dc31a565d40ac8884713e8b4d317'),
             (R14 + '/VALIDATION_R14_CX1V001.json', '930ca7bc78e74134aeac46851a6bbf9481e78f9ce3862b77d370b716dd8380ec'),
             (R14 + '/SELECTED_R14_CX1V001.json', 'dc74949d1d4f19336661f8ce85e9a85de0176837adad61c7a9585a147f933533'),
             (R14 + '/SELECTED_R14_CX1V002.json', '6b650ececefee673ec3e04849574f9a4b75b977288afd3c9949a4b8d2d3cd49a'),
             (R14 + '/SOURCE_DELTA_CX1V001.json', '56a95b7ef983608b89b5f4c30799fa9ea578eb69c7e01ccb31de96b8bf92ec51'),
             (R14 + '/BUILD_PROGRESS_CX1V001.json', 'd246fa90dd5032ae6f6801056d1763b498fa6aba5534346b0d379a7e0ace0d01'))


def pins(o, where='$', out=None):
    out = [] if out is None else out
    if isinstance(o, dict):
        if isinstance(o.get('path'), str) and isinstance(o.get('sha256'), str):
            out.append((where, o['path'], o['sha256'], o.get('bytes')))
        for k, v in o.items():
            pins(v, '%s.%s' % (where, k), out)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            pins(v, '%s[%d]' % (where, i), out)
    return out


res = {'utc_start': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'manifests': {}}
bad_total = 0
for mp, mh in MANIFESTS:
    raw = Path(mp).read_bytes()
    ok_m = hashlib.sha256(raw).hexdigest() == mh
    rows = []
    for where, p, h, n in pins(json.loads(raw)):
        try:
            b = Path(p).read_bytes()
            got, gn, err = hashlib.sha256(b).hexdigest(), len(b), None
        except Exception as e:
            got, gn, err = None, None, '%s: %s' % (type(e).__name__, str(e)[:200])
        ok = got == h and (n is None or n == gn)
        rows.append({'where': where, 'path': p, 'sha256': h, 'got': got, 'bytes': n, 'got_bytes': gn, 'ok': ok, 'error': err})
    nbad = sum(1 for r in rows if not r['ok'])
    bad_total += nbad + (0 if ok_m else 1)
    res['manifests'][Path(mp).name] = {'manifest_sha_ok': ok_m, 'n': len(rows), 'n_bad': nbad, 'bad': [r for r in rows if not r['ok']]}
    print('%s manifest_sha_ok=%s pins=%d bad=%d' % (Path(mp).name, ok_m, len(rows), nbad))
    for r in rows:
        if not r['ok']:
            print('   BAD', json.dumps(r)[:400])
res['utc_end'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
res['bad_total'] = bad_total
(OUT / 'HASH_MANIFEST_PROBE_C4.json').write_text(json.dumps(res, indent=1, sort_keys=True) + '\n')
raise SystemExit(0 if bad_total == 0 else 1)

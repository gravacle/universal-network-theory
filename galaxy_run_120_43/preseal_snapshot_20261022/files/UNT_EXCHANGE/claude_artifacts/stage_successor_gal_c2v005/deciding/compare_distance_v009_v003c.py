"""Deciding-test comparator: one real DDO154 call at a per-call distance under driver c2v009 (gal_c2v005 stages) against a
real call at the SAME call spec under driver c2v003c (absorb_c2_0473/driver_f, ed326130; reviewed base stages with the
per-call geometry patched in as module globals).  Claude2 lane stage_successor_gal_c2v005.  INERT on import; reads two run
directories, writes ONE report (exclusive create).  numpy only.

  python3 -I -B compare_distance_v009_v003c.py --reference V003C_RUN --new V009_RUN --spec-sha256 SHA --out REPORT.json
         [--reference-driver-sha256 ed326130...] [--new-driver-sha256 237ef3d4...] [--allow-no-geometry]
  (--allow-no-geometry is ONLY for the comparator self-test on a registered-geometry run; the report records it and the
   verdict is then SELFTEST_ONLY, never a deciding PASS.)

Lineage differences that are expected and are NOT compared: every 64-hex digest string (stage worker shas, seed sha: the
c2v003c seed annotation literal is c2v003, the c2v009 one c2v006; route-A identity, file digests), run-directory prefixes,
attempt tokens, and timing / process fields.  What IS compared (verdict PASS_BITWISE_EQUAL_PER_CALL_OUTPUTS needs all):
  SPEC            both start.json call_spec_sha256 == --spec-sha256; normalized_spec equal after the outdir substitution;
                  physical.distance_Mpc != 4.04 (a per-call geometry call); driver shas as given.
  GEOMETRY_INPUTS the four per-call geometry files under inputs/ (profile, source-binding V003 copy, monotone source,
                  column-mean binding) byte-identical after each run's outdir -> <OUT>.
  STATUS          both result.json status COMPLETED and valid True.
  SPEEDS          speeds_km_s (same ids) equal as JSON floats; rows equal; final_pass equal; every pass's rows and
                  max_abs_change_km_s equal.
  STAGES          stage_records names equal, in order.
  ARRAYS          per stage: the same set of .npz/.npy relative paths (attempt tokens -> <TOKEN>; content-addressed blob
                  names kept: equal content gives equal names); every array (every npz member) equal in dtype, shape, bytes.
  NUMERIC_JSON    per stage: the same set of .json/.jsonl relative paths (tokens as above); every numeric leaf (int/float,
                  not bool) equal at the same JSON path, except leaves under a key naming time/process/memory
                  (TIMING_KEYS); string leaves are not compared (they carry paths and digests).
DIAGNOSTIC (never decides): per stage, the count of string leaves that differ after outdir/hex/token normalization."""
import argparse
import hashlib
import io
import json
import re
import sys
import zipfile
from pathlib import Path

import numpy as np

V003C_SHA = 'ed326130e89654a377615e46a077764cf3ad39e0bf07bc9d0606225bc69fbdf2'
V009_SHA = '237ef3d41daf4d99b0aafed3e90b27b095a741a9f66ea06ea34f3e44876d47bb'
GEO_FILES = ('geometry_C/GALAXY_RADIAL_SOURCE_REFERENCE_V001.json', 'geometry_C/GALAXY_PHYSICAL_SOURCE_STATE_BINDING_V003.json',
             'geometry_monotone_source.json', 'geometry_column_mean_binding.json')
TIMING_KEYS = ('time', 'second', 'elapsed', 'utc', 'pid', 'rss', 'memory', 'wall', 'clock', 'started', 'finished', 'duration', 'cpu')
TOKEN = re.compile(r'\d{17,22}-\d+-[0-9a-f]{8}')
HEX = re.compile(r'[0-9a-f]{64}')


def rj(p):
    return json.loads(Path(p).read_text())


def rel_token(p):
    return TOKEN.sub('<TOKEN>', str(p))


def files_by_kind(d, exts):
    out = {}
    for p in sorted(Path(d).rglob('*')):
        if p.is_file() and p.suffix in exts:
            k = rel_token(p.relative_to(d))
            out.setdefault(k, []).append(p)
    return out


def arrays_of(p):
    if p.suffix == '.npy':
        a = np.load(p, allow_pickle=False)
        return {'': (a.dtype.str, a.shape, hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest())}
    out = {}
    with zipfile.ZipFile(p) as z:
        for n in sorted(z.namelist()):
            a = np.load(io.BytesIO(z.read(n)), allow_pickle=False)
            out[n] = (a.dtype.str, a.shape, hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest())
    return out


def numeric_leaves(o, path='', out=None, skip=False):
    out = {} if out is None else out
    if isinstance(o, dict):
        for k in sorted(o):
            sk = skip or any(t in str(k).lower() for t in TIMING_KEYS)
            numeric_leaves(o[k], path + '.' + str(k), out, sk)
    elif isinstance(o, list):
        for i, x in enumerate(o):
            numeric_leaves(x, '%s[%d]' % (path, i), out, skip)
    elif isinstance(o, (int, float)) and not isinstance(o, bool) and not skip:
        out[path] = repr(o)
    return out


def string_leaves(o, root, path='', out=None):
    out = {} if out is None else out
    if isinstance(o, dict):
        for k in sorted(o):
            string_leaves(o[k], root, path + '.' + str(k), out)
    elif isinstance(o, list):
        for i, x in enumerate(o):
            string_leaves(x, root, '%s[%d]' % (path, i), out)
    elif isinstance(o, str):
        out[path] = HEX.sub('<HEX>', TOKEN.sub('<TOKEN>', o.replace(root, '<OUT>')))
    return out


def load_json_any(p):
    if p.suffix == '.jsonl':
        return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
    return rj(p)


def compare(ref, new, spec_sha, ref_drv, new_drv, allow_no_geometry):
    ref, new = Path(ref).resolve(), Path(new).resolve()
    checks = {}

    def put(name, ok, detail):
        checks[name] = {'pass': bool(ok), 'detail': detail}
    sr, sn = rj(ref / 'start.json'), rj(new / 'start.json')
    nsr = json.loads(json.dumps(sr['normalized_spec']).replace(str(ref), '<OUT>'))
    nsn = json.loads(json.dumps(sn['normalized_spec']).replace(str(new), '<OUT>'))
    D = (nsn.get('physical') or {}).get('distance_Mpc')
    put('SPEC', sr['call_spec_sha256'] == spec_sha == sn['call_spec_sha256'] and nsr == nsn and (allow_no_geometry or D != 4.04)
        and sr['driver_sha256'] == ref_drv and sn['driver_sha256'] == new_drv,
        {'call_spec_sha256': [sr['call_spec_sha256'], sn['call_spec_sha256']], 'normalized_spec_equal': nsr == nsn, 'distance_Mpc': D,
         'driver_sha256': [sr['driver_sha256'], sn['driver_sha256']]})
    geo = {}
    for n in GEO_FILES:
        a, b = ref / 'inputs' / n, new / 'inputs' / n
        if not a.is_file() or not b.is_file():
            geo[n] = 'MISSING' + ('_REF' if not a.is_file() else '') + ('_NEW' if not b.is_file() else '')
        else:
            geo[n] = 'EQUAL' if a.read_bytes().replace(str(ref).encode(), b'<OUT>') == b.read_bytes().replace(str(new).encode(), b'<OUT>') else 'DIFFERS'
    put('GEOMETRY_INPUTS', all(v == 'EQUAL' for v in geo.values()) or (allow_no_geometry and all(v.startswith('MISSING') for v in geo.values())), geo)
    rr, rn = rj(ref / 'result.json'), rj(new / 'result.json')
    put('STATUS', rr.get('status') == rn.get('status') == 'COMPLETED' and rr.get('valid') is True and rn.get('valid') is True,
        {'status': [rr.get('status'), rn.get('status')], 'valid': [rr.get('valid'), rn.get('valid')]})

    def passes(r):
        return [{'pass': p.get('pass'), 'rows': p.get('rows'), 'max_abs_change_km_s': p.get('max_abs_change_km_s')} for p in (r.get('passes') or [])]
    sp_ok = (rr.get('speeds_km_s') == rn.get('speeds_km_s') and rr.get('speeds_km_s') is not None and rr.get('rows') == rn.get('rows')
             and rr.get('final_pass') == rn.get('final_pass') and passes(rr) == passes(rn))
    put('SPEEDS', sp_ok, {'speeds_ref': rr.get('speeds_km_s'), 'speeds_new': rn.get('speeds_km_s'),
                          'differing_ids': sorted(k for k in set(rr.get('speeds_km_s') or {}) | set(rn.get('speeds_km_s') or {})
                                                  if (rr.get('speeds_km_s') or {}).get(k) != (rn.get('speeds_km_s') or {}).get(k)),
                          'final_pass': [rr.get('final_pass'), rn.get('final_pass')], 'passes_equal': passes(rr) == passes(rn)})
    names_r = [x.get('name') for x in rr.get('stage_records') or []]
    names_n = [x.get('name') for x in rn.get('stage_records') or []]
    put('STAGES', names_r == names_n and bool(names_r), {'ref': names_r, 'new': names_n})
    dirs_r = {x.get('name'): Path(x['stage_dir']) for x in rr.get('stage_records') or [] if x.get('stage_dir')}
    dirs_n = {x.get('name'): Path(x['stage_dir']) for x in rn.get('stage_records') or [] if x.get('stage_dir')}
    arr, num, strd = {}, {}, {}
    for name in names_r:
        if name not in dirs_r or name not in dirs_n:
            arr[name] = num[name] = 'STAGE_DIR_MISSING'
            continue
        A, B = files_by_kind(dirs_r[name], ('.npz', '.npy')), files_by_kind(dirs_n[name], ('.npz', '.npy'))
        bad = sorted(set(A) ^ set(B))
        n_arrays = 0
        for k in sorted(set(A) & set(B)):
            if len(A[k]) != len(B[k]):
                bad.append(k + ' (count)')
                continue
            for pa, pb in zip(A[k], B[k]):
                xa, xb = arrays_of(pa), arrays_of(pb)
                n_arrays += len(xa)
                if xa != xb:
                    bad.append(k + ' ' + str(sorted(m for m in set(xa) | set(xb) if xa.get(m) != xb.get(m))[:5]))
        arr[name] = {'files': len(A), 'arrays': n_arrays, 'differing': bad[:20], 'equal': not bad}
        A, B = files_by_kind(dirs_r[name], ('.json', '.jsonl')), files_by_kind(dirs_n[name], ('.json', '.jsonl'))
        badj = sorted(set(A) ^ set(B))
        n_leaves, sdiff = 0, 0
        for k in sorted(set(A) & set(B)):
            if len(A[k]) != len(B[k]):
                badj.append(k + ' (count)')
                continue
            for pa, pb in zip(A[k], B[k]):
                oa, ob = load_json_any(pa), load_json_any(pb)
                la, lb = numeric_leaves(oa), numeric_leaves(ob)
                n_leaves += len(la)
                if la != lb:
                    badj.append(k + ' ' + str(sorted(p for p in set(la) | set(lb) if la.get(p) != lb.get(p))[:5]))
                sa, sb = string_leaves(oa, str(ref)), string_leaves(ob, str(new))
                sdiff += sum(1 for p in set(sa) | set(sb) if sa.get(p) != sb.get(p))
        num[name] = {'files': len(A), 'numeric_leaves': n_leaves, 'differing': badj[:20], 'equal': not badj}
        strd[name] = sdiff
    put('ARRAYS', bool(arr) and all(isinstance(v, dict) and v['equal'] for v in arr.values()), arr)
    put('NUMERIC_JSON', bool(num) and all(isinstance(v, dict) and v['equal'] for v in num.values()), num)
    ok = all(c['pass'] for c in checks.values())
    verdict = ('SELFTEST_ONLY_' + ('EQUAL' if ok else 'NOT_EQUAL')) if allow_no_geometry else ('PASS_BITWISE_EQUAL_PER_CALL_OUTPUTS' if ok else 'FAIL')
    return {'format': 'COMPARE_DISTANCE_V009_V003C_V001', 'reference': str(ref), 'new': str(new), 'verdict': verdict,
            'allow_no_geometry': allow_no_geometry, 'checks': checks, 'diagnostic_string_leaf_differences_by_stage': strd,
            'failed': [k for k, c in checks.items() if not c['pass']],
            'comparator': {'path': str(Path(__file__).resolve()), 'sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--reference', required=True)
    ap.add_argument('--new', required=True)
    ap.add_argument('--spec-sha256', required=True)
    ap.add_argument('--reference-driver-sha256', default=V003C_SHA)
    ap.add_argument('--new-driver-sha256', default=V009_SHA)
    ap.add_argument('--allow-no-geometry', action='store_true')
    ap.add_argument('--out', required=True)
    a = ap.parse_args(argv)
    rep = compare(a.reference, a.new, a.spec_sha256, a.reference_driver_sha256, a.new_driver_sha256, a.allow_no_geometry)
    raw = (json.dumps(rep, indent=1, allow_nan=False) + '\n').encode()
    with open(a.out, 'xb') as f:
        f.write(raw)
    print(json.dumps({'verdict': rep['verdict'], 'failed': rep['failed']}))
    return 0 if rep['verdict'] in ('PASS_BITWISE_EQUAL_PER_CALL_OUTPUTS', 'SELFTEST_ONLY_EQUAL') else 1


if __name__ == '__main__':
    sys.exit(main())

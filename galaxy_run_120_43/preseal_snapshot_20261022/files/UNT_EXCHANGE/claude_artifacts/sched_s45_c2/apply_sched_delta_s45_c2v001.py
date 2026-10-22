"""Apply the sched_s45 scheduling delta to a DDO154 calibration RUN_CONFIG (Claude2 sched_s45_c2, c2v001).

Root uses it twice: once here on R9 (721c7230) to publish RUN_CONFIG_DDO154_CX2V006R9_S45_C2V001.json, and at H3 on
C2 (R9's H3 successor), so the C2 successor carries exactly the same scheduling change and nothing else.
  * Only the paths in ALLOWED may change; any other path in the delta refuses.  Physics inputs (numerics, driver,
    coordinate spec and addendum, taxonomy, anchor, observation region, deciding test, tail_readiness, u_i carrier,
    work dir, python, monitor, process_budget, stage_aware_budget, n_cores, campaign_wall_cap_s, ...) cannot change.
  * The campaign pin's sha256 is recomputed from the file's bytes and must equal the delta's.
  * The output keeps the predecessor's serialization (json, indent 1, sorted keys, trailing newline) and is written by
    exclusive create.  The report lists every changed path and the canonical sha256 of every unchanged top-level key.
usage: python3 -I -B apply_sched_delta_s45_c2v001.py PREDECESSOR.json DELTA.json OUT.json [REPORT.json]
"""
import copy
import hashlib
import json
import sys
from pathlib import Path

ALLOWED = ('campaign', 'max_concurrent', 'per_call.wall_cap_s', 'per_call.rss_cap_bytes', 'per_call.output_cap_bytes',
           'disk_guard.per_call_bytes', 'disk_guard.reserve_bytes', 'orphan_wait.cap_s', 'notes')


def canon(o):
    return json.dumps(o, sort_keys=True, separators=(',', ':'), allow_nan=False)


def sha_b(b):
    return hashlib.sha256(b).hexdigest()


def get(d, path):
    for k in path.split('.'):
        d = d[k]
    return d


def put(d, path, v):
    ks = path.split('.')
    for k in ks[:-1]:
        d = d[k]
    if ks[-1] not in d:
        raise KeyError('path absent in predecessor: %s' % path)
    d[ks[-1]] = v


def flat(o, pre=''):
    if isinstance(o, dict):
        out = {}
        for k, v in o.items():
            out.update(flat(v, pre + k + '.') if isinstance(v, dict) and v else {pre + k: v})
        return out
    return {pre[:-1]: o}


def apply(pred_bytes, delta):
    pred = json.loads(pred_bytes)
    reasons = []
    sets = delta.get('set') or {}
    for p in sets:
        if p not in ALLOWED:
            reasons.append('path not allowed (scheduling only): %s' % p)
    camp = sets.get('campaign')
    if camp is not None:
        try:
            if sha_b(Path(camp['path']).read_bytes()) != camp['sha256']:
                reasons.append('campaign sha256 differs from the file bytes')
        except (OSError, KeyError, TypeError) as exc:
            reasons.append('campaign pin unreadable: %s' % exc)
    if reasons:
        return None, {'ok': False, 'reasons': reasons}
    new = copy.deepcopy(pred)
    for p, v in sets.items():
        put(new, p, v)
    if 'disk_guard.per_call_bytes' in sets or 'per_call.output_cap_bytes' in sets:
        if new['disk_guard']['per_call_bytes'] < int(new['per_call']['output_cap_bytes']):
            return None, {'ok': False, 'reasons': ['disk_guard.per_call_bytes < per_call.output_cap_bytes (parent L1748)']}
    out_bytes = (json.dumps(new, indent=1, sort_keys=True, allow_nan=False) + '\n').encode()
    fp, fn = flat(pred), flat(new)
    changed = sorted(k for k in set(fp) | set(fn) if fp.get(k, '<absent>') != fn.get(k, '<absent>'))
    illegal = [k for k in changed if not any(k == a or k.startswith(a + '.') for a in ALLOWED)]
    if illegal:
        return None, {'ok': False, 'reasons': ['changed outside ALLOWED: %s' % illegal]}
    top_same = {k: sha_b(canon(pred[k]).encode()) for k in sorted(pred) if canon(pred[k]) == canon(new[k])}
    rep = {'ok': True, 'predecessor_sha256': sha_b(pred_bytes), 'successor_sha256': sha_b(out_bytes),
           'predecessor_serialization_roundtrips': (json.dumps(pred, indent=1, sort_keys=True) + '\n').encode() == pred_bytes,
           'changed_paths': {k: {'from': fp.get(k), 'to': fn.get(k)} for k in changed},
           'unchanged_top_level_canonical_sha256': top_same}
    return out_bytes, rep


def main(argv):
    pred_p, delta_p, out_p = argv[:3]
    out_bytes, rep = apply(Path(pred_p).read_bytes(), json.loads(Path(delta_p).read_text()))
    if out_bytes is None:
        print(json.dumps(rep, indent=1))
        return 2
    with open(out_p, 'xb') as f:
        f.write(out_bytes)
    if len(argv) > 3:
        with open(argv[3], 'x') as f:
            json.dump(rep, f, indent=1)
            f.write('\n')
    print(json.dumps({k: rep[k] for k in ('ok', 'predecessor_sha256', 'successor_sha256', 'changed_paths')}, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

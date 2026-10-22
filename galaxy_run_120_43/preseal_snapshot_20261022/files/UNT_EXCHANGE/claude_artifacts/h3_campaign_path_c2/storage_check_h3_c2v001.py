"""Storage checks for the DDO154 calibration campaign (Claude2 h3_campaign_path_c2, c2v001; V006 A147 L3-01, A188).  READ-ONLY.

Two subcommands; neither moves, deletes or writes anything except --out (exclusive create).

wave  -- the per-wave disk check root runs before every `run` that plans a new wave.
  The parent's rule (c75a889f disk_forecast L2163-2182, applied before every new wave L3503-3506 and on a resume L3476-3479):
  a wave of n calls starts only if free >= n x disk_guard.per_call_bytes + disk_guard.reserve_bytes (guard = the 80 GiB cap,
  A147 L3-01), else HALTED_DISK.  This check reads the campaign's OWN receipts (waves/wave_*/campaign/call_*/RECEIPT.json of
  --work-dir; FINISHED ones), takes the largest final/peak output as the measured per-call bytes, reads free space by
  statvfs at the work dir, and forecasts the listed future waves (default: the rest of the ENGINE_SHAPED list of
  w1_disk_forecast_v001, sim_s45_c2v003 L460, an ASSUMED shape) with --other-bytes K:B for other outputs root expects on the
  same volume before wave K (HEADLINE11, S0, NGC).  Exit 0 if the next wave fits, 5 if it would halt HALTED_DISK.

move  -- may DIR leave the campaign volume by a verified move?
  Collects every {path, sha256} pin of the given JSON files (--pins-from: the H3 config, the seal tuple record, the V007
  report, the certificate registry, ...; with --follow, pinned .json files up to 8 MiB are read for their own pins, depth 3,
  except files under run trees or volumes and NGC3198 / C5H / UVT_ / .codex paths (NO_FOLLOW): those pins are checked by
  path only, never opened)
  and refuses (exit 3, NOT_MOVABLE) when a pinned path resolves under DIR, when DIR holds or lies inside the campaign work dir
  (the cache re-hashes entries by path, parent L2302-2341; SF1 pins the work dir identity), or when DIR is not a directory.
  Exit 0 MOVABLE.  The move itself is root's (README section 6): ditto, then a sha256 manifest of both trees compared equal,
  then the source removed; never a plain mv across volumes.

usage: python3 -I -B storage_check_h3_c2v001.py wave --work-dir WD [--next-calls N] [--waves 8,2,...] [--other-bytes K:B ...]
                                                     [--guard-bytes G] [--reserve-bytes R] [--out OUT.json]
       python3 -I -B storage_check_h3_c2v001.py move --candidate DIR --work-dir WD --pins-from F.json [...] [--follow]
"""
import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

GiB = 1 << 30
ENGINE_SHAPED = [1, 8, 2, 1, 1, 1, 10, 10, 24, 8, 2, 1, 10, 10, 24, 7]      # w1_disk_forecast_v001 / sim_s45_c2v003 L460
NO_FOLLOW = ('/runs/', '/runs_ext/', 'unt_internal_runs', '/volumes/', 'ngc3198', 'c5h', '/.codex/', '/uvt_')


def no_follow(*paths):
    return any(m in str(p).lower() for p in paths for m in NO_FOLLOW)


def campaign_receipts(work_dir):
    out = []
    for rp in sorted(Path(work_dir).glob('waves/wave_*/campaign/call_*/RECEIPT.json')):
        try:
            r = json.loads(rp.read_text())
        except (OSError, ValueError):
            continue
        if r.get('status') == 'FINISHED':
            out.append({'receipt': str(rp), 'final_output_bytes': r.get('final_output_bytes'),
                        'peak_output_bytes': r.get('peak_output_bytes'), 'elapsed_seconds': r.get('elapsed_seconds')})
    return out


def wave_check(a):
    wd = Path(a.work_dir)
    anc = Path(os.path.realpath(str(wd)))
    while not anc.exists() and anc != anc.parent:
        anc = anc.parent
    st = os.statvfs(str(anc))
    free = st.f_bavail * st.f_frsize
    recs = campaign_receipts(wd) if wd.is_dir() else []
    sizes = [max(int(r['final_output_bytes'] or 0), int(r['peak_output_bytes'] or 0)) for r in recs]
    measured = max(sizes) if sizes else None
    per_call = a.per_call_output_bytes if a.per_call_output_bytes is not None else measured
    n_done = len({str(Path(r['receipt']).parent) for r in recs})
    waves = [int(x) for x in a.waves.split(',')] if a.waves else ENGINE_SHAPED[1:]
    other = {}
    for s in a.other_bytes:
        k, b = s.split(':')
        other[int(k)] = other.get(int(k), 0) + int(b)
    nxt = a.next_calls if a.next_calls is not None else waves[0]
    need = nxt * a.guard_bytes + a.reserve_bytes
    rows, used = [], 0
    for k, n in enumerate(waves, 1):
        f = free - used - sum(b for kk, b in other.items() if kk <= k)
        nd = n * a.guard_bytes + a.reserve_bytes
        rows.append({'future_wave': k, 'n_calls': n, 'free_GiB': round(f / GiB, 1), 'need_GiB': round(nd / GiB, 1),
                     'fits': f >= nd, 'shortfall_GiB': 0.0 if f >= nd else round((nd - f) / GiB, 1)})
        used += n * (per_call or 0)
    first = next((r for r in rows if not r['fits']), None)
    doc = {'schema': 'H3_STORAGE_WAVE_CHECK_C2V001', 'work_dir': str(wd), 'free_bytes': free, 'free_read_at': str(anc),
           'finished_campaign_calls': n_done, 'measured_per_call_output_bytes': measured,
           'forecast_per_call_output_bytes': per_call, 'guard_bytes': a.guard_bytes, 'reserve_bytes': a.reserve_bytes,
           'next_wave': {'n_calls': nxt, 'need_bytes': need, 'fits': free >= need}, 'forecast': rows,
           'first_halting_future_wave': first, 'other_bytes_before_wave': other,
           'rule': 'parent L3503-3506: free >= n x guard + reserve, else HALTED_DISK (nothing deleted)'}
    if a.out:
        with open(a.out, 'x') as fh:
            json.dump(doc, fh, indent=1, sort_keys=True)
            fh.write('\n')
    print(json.dumps(doc, indent=1, sort_keys=True))
    return 0 if doc['next_wave']['fits'] else 5


def pins_in(obj, out):
    if isinstance(obj, dict):
        if isinstance(obj.get('path'), str) and isinstance(obj.get('sha256'), str) and len(obj['sha256']) == 64:
            out.append(obj['path'])
        for v in obj.values():
            pins_in(v, out)
    elif isinstance(obj, list):
        for v in obj:
            pins_in(v, out)
    return out


def move_check(a):
    cand = os.path.realpath(a.candidate)
    if not os.path.isdir(cand):
        print(json.dumps({'status': 'NOT_MOVABLE', 'reasons': ['candidate is not a directory: %s' % cand]}, indent=1))
        return 3
    wd = os.path.realpath(a.work_dir)
    reasons, seen, todo = [], set(), [(os.path.abspath(p), 0) for p in a.pins_from]
    pinned = []
    while todo:
        p, depth = todo.pop()
        if p in seen:
            continue
        seen.add(p)
        try:
            doc = json.loads(Path(p).read_bytes())
        except (OSError, ValueError) as exc:
            reasons.append('pin source unreadable: %s (%s)' % (p, type(exc).__name__))
            continue
        for q in pins_in(doc, []):
            pinned.append((p, q))
            rq = os.path.realpath(q)
            if a.follow and depth < 3 and rq.endswith('.json') and not no_follow(q, rq) and os.path.isfile(rq) \
                    and os.path.getsize(rq) <= 8 * 1024 * 1024:
                todo.append((rq, depth + 1))
    hits = sorted({(src, q) for src, q in pinned if os.path.realpath(q) == cand or os.path.realpath(q).startswith(cand + '/')})
    reasons += ['pinned by %s: %s' % (src, q) for src, q in hits]
    if wd == cand or wd.startswith(cand + '/') or cand.startswith(wd + '/'):
        reasons.append('the campaign work dir %s is or contains or is inside the candidate' % wd)
    doc = {'schema': 'H3_STORAGE_MOVE_CHECK_C2V001', 'candidate': cand, 'work_dir': wd, 'pin_sources_read': sorted(seen),
           'n_pins': len(pinned), 'status': 'NOT_MOVABLE' if reasons else 'MOVABLE', 'reasons': reasons}
    print(json.dumps(doc, indent=1, sort_keys=True))
    return 3 if reasons else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    w = sub.add_parser('wave')
    w.add_argument('--work-dir', required=True)
    w.add_argument('--next-calls', type=int)
    w.add_argument('--waves')
    w.add_argument('--other-bytes', action='append', default=[])
    w.add_argument('--per-call-output-bytes', type=int)
    w.add_argument('--guard-bytes', type=int, default=80 * GiB)
    w.add_argument('--reserve-bytes', type=int, default=20 * GiB)
    w.add_argument('--out')
    m = sub.add_parser('move')
    m.add_argument('--candidate', required=True)
    m.add_argument('--work-dir', required=True)
    m.add_argument('--pins-from', action='append', required=True)
    m.add_argument('--follow', action='store_true')
    a = ap.parse_args(argv)
    return wave_check(a) if a.cmd == 'wave' else move_check(a)


if __name__ == '__main__':
    sys.exit(main())

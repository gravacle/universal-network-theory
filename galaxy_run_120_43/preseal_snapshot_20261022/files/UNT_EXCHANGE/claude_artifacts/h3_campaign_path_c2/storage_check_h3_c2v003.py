"""Storage checks for the DDO154 calibration campaign (Claude2 h3_campaign_path_c2, c2v003; V006 A192 item 5).  READ-ONLY.

Successor of storage_check_h3_c2v001 (e0b3a89a), loaded by path and sha.  `move` is c2v001's, unchanged.  `wave` changes in
one thing only (A192 item 5, the verifier's blocking item): b, the per-call bytes the forecast uses, is measured as the CALL
DIR's TOTAL BYTES AFTER ACCEPTANCE, including the handoff's ACCEPTANCE_TAILSTATES_* exports and TAIL_CERTIFICATE_ACCEPTANCE.json
-- not the receipt's output bytes.

  b per call dir  = max(apparent bytes, allocated bytes) over every regular file under waves/wave_*/campaign/call_*/ (no
                    symlink followed; a hard-linked inode counted once; metadata only, no file is opened).
  accepted        = the call dir holds TAIL_CERTIFICATE_ACCEPTANCE.json (reingest VALID) or at least one
                    ACCEPTANCE_TAILSTATES_* directory (a handoff pass ran: ACCEPTED, MODEL_INVALID or a halt).
  measured b      = the largest b over ACCEPTED call dirs (None before any acceptance).  The receipt-based value of c2v001 is
                    reported beside it for comparison, never used.
The forecast and the next-wave rule are c2v001's (parent L3503-3506: free >= n x guard + reserve, else HALTED_DISK).

Threshold (STORAGE_PLAN_ERRATUM_C2V001 section 3-4, recomputed from the measured b; FORMAL arithmetic):
  need_k(b) = (sum_{j<k} n_j) * b + n_k * guard + reserve;  R(b) = max_k need_k(b);
  the program fits iff R(b) + other_program <= total_free (both volumes, root's df at plan time);
  b* = min over k with sum_{j<k} n_j > 0 of (total_free - other_program - n_k * guard - reserve) / sum_{j<k} n_j.
  With --threshold-total-free-bytes F and --threshold-other-program-bytes H (both required for it), the document carries
  R(b), the binding wave, b* and whether b <= b*.  Nothing here moves, deletes or writes anything except --out.

usage: python3 -I -B storage_check_h3_c2v003.py wave --work-dir WD [--next-calls N] [--waves 8,2,...] [--other-bytes K:B ...]
                    [--per-call-output-bytes B] [--guard-bytes G] [--reserve-bytes R] [--out OUT.json]
                    [--threshold-total-free-bytes F --threshold-other-program-bytes H [--threshold-waves 1,8,2,...]]
       python3 -I -B storage_check_h3_c2v003.py move ...   (c2v001's)
exit: wave 0 the next wave fits, 5 it would halt HALTED_DISK; move 0 MOVABLE, 3 NOT_MOVABLE.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import stat
import sys
from pathlib import Path

PRED = (os.path.join(os.path.dirname(os.path.abspath(__file__)), 'storage_check_h3_c2v001.py'),
        'e0b3a89a4a2930311c393cd62d2f51b0b343fe705736d8083a45628c8a75706d')
ACCEPT_MARKERS = ('TAIL_CERTIFICATE_ACCEPTANCE.json',)
TAILSTATES_PREFIX = 'ACCEPTANCE_TAILSTATES_'


def load_pred():
    raw = Path(PRED[0]).read_bytes()
    if hashlib.sha256(raw).hexdigest() != PRED[1]:
        raise SystemExit('PIN_MISMATCH %s' % PRED[0])
    sp = importlib.util.spec_from_file_location('_h3_storage_c2v001', PRED[0])
    m = importlib.util.module_from_spec(sp)
    exec(compile(raw, PRED[0], 'exec'), m.__dict__)
    return m


S1 = load_pred()
GiB = S1.GiB
ENGINE_SHAPED = S1.ENGINE_SHAPED


def tree_bytes(d):
    """(apparent, allocated, n_files, tailstate dirs) of every regular file under d; lstat only, symlinks not followed."""
    seen, app, alloc, n, ts = set(), 0, 0, 0, []
    for root, dirs, files in os.walk(d, followlinks=False):
        if root == str(d):
            ts = sorted(x for x in dirs if x.startswith(TAILSTATES_PREFIX))
        for f in files:
            st = os.lstat(os.path.join(root, f))
            if not stat.S_ISREG(st.st_mode) or (st.st_dev, st.st_ino) in seen:
                continue
            seen.add((st.st_dev, st.st_ino))
            app += st.st_size
            alloc += getattr(st, 'st_blocks', 0) * 512
            n += 1
    return app, alloc, n, ts


def call_dirs(work_dir):
    out = []
    for cd in sorted(Path(work_dir).glob('waves/wave_*/campaign/call_*')):
        if not cd.is_dir() or cd.is_symlink():
            continue
        app, alloc, n, ts = tree_bytes(cd)
        accepted = any((cd / m).is_file() for m in ACCEPT_MARKERS) or bool(ts)
        out.append({'call_dir': str(cd), 'apparent_bytes': app, 'allocated_bytes': alloc, 'b_bytes': max(app, alloc),
                    'n_files': n, 'acceptance_tailstate_dirs': ts, 'accepted': accepted})
    return out


def threshold(b, waves, total_free, other, guard, reserve):
    rows, before = [], 0
    for k, n in enumerate(waves, 1):
        rows.append({'wave': k, 'n_calls': n, 'calls_before': before,
                     'need_bytes': before * (b or 0) + n * guard + reserve})
        before += n
    binding = max(rows, key=lambda r: r['need_bytes'])
    cands = [((total_free - other - r['n_calls'] * guard - reserve) / r['calls_before'], r['wave'])
             for r in rows if r['calls_before'] > 0]
    bstar, bw = min(cands) if cands else (None, None)
    first_ok = all(r['n_calls'] * guard + reserve <= total_free - other for r in rows if r['calls_before'] == 0)
    return {'R_bytes': binding['need_bytes'], 'R_GiB': round(binding['need_bytes'] / GiB, 1), 'binding_wave': binding['wave'],
            'b_star_bytes': bstar, 'b_star_GiB': None if bstar is None else round(bstar / GiB, 2), 'b_star_binding_wave': bw,
            'total_free_bytes': total_free, 'other_program_bytes': other, 'b_bytes': b,
            'b_GiB': None if b is None else round(b / GiB, 2),
            'fits': None if b is None else (bool(first_ok) and binding['need_bytes'] + other <= total_free),
            'rule': 'STORAGE_PLAN_ERRATUM_C2V001 sections 3-4: R(b) = max_k (sum_{j<k} n_j) b + n_k guard + reserve; '
                    'fits iff R(b) + other <= total free; b* solves equality at the binding wave',
            'waves': waves}


def wave_check(a):
    wd = Path(a.work_dir)
    anc = Path(os.path.realpath(str(wd)))
    while not anc.exists() and anc != anc.parent:
        anc = anc.parent
    st = os.statvfs(str(anc))
    free = st.f_bavail * st.f_frsize
    calls = call_dirs(wd) if wd.is_dir() else []
    acc = [c['b_bytes'] for c in calls if c['accepted']]
    measured = max(acc) if acc else None
    recs = S1.campaign_receipts(wd) if wd.is_dir() else []
    rsz = [max(int(r['final_output_bytes'] or 0), int(r['peak_output_bytes'] or 0)) for r in recs]
    per_call = a.per_call_output_bytes if a.per_call_output_bytes is not None else measured
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
    doc = {'schema': 'H3_STORAGE_WAVE_CHECK_C2V003', 'work_dir': str(wd), 'free_bytes': free, 'free_read_at': str(anc),
           'b_rule': 'A192 item 5: the call dir total bytes after acceptance (incl. ACCEPTANCE_TAILSTATES exports)',
           'call_dirs': calls, 'n_call_dirs': len(calls), 'n_accepted_call_dirs': len(acc),
           'measured_per_call_bytes_after_acceptance': measured,
           'receipt_output_bytes_max_for_comparison': max(rsz) if rsz else None,
           'forecast_per_call_bytes': per_call, 'guard_bytes': a.guard_bytes, 'reserve_bytes': a.reserve_bytes,
           'next_wave': {'n_calls': nxt, 'need_bytes': need, 'fits': free >= need}, 'forecast': rows,
           'first_halting_future_wave': next((r for r in rows if not r['fits']), None), 'other_bytes_before_wave': other,
           'rule': 'parent L3503-3506: free >= n x guard + reserve, else HALTED_DISK (nothing deleted)',
           'predecessor': {'path': PRED[0], 'sha256': PRED[1]}}
    if a.threshold_total_free_bytes is not None or a.threshold_other_program_bytes is not None:
        if a.threshold_total_free_bytes is None or a.threshold_other_program_bytes is None:
            raise SystemExit('--threshold-total-free-bytes and --threshold-other-program-bytes go together')
        tw = [int(x) for x in a.threshold_waves.split(',')] if a.threshold_waves else list(ENGINE_SHAPED)
        doc['threshold'] = threshold(per_call, tw, a.threshold_total_free_bytes, a.threshold_other_program_bytes,
                                     a.guard_bytes, a.reserve_bytes)
    if a.out:
        with open(a.out, 'x') as fh:
            json.dump(doc, fh, indent=1, sort_keys=True)
            fh.write('\n')
    print(json.dumps(doc, indent=1, sort_keys=True))
    return 0 if doc['next_wave']['fits'] else 5


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
    w.add_argument('--threshold-total-free-bytes', type=int)
    w.add_argument('--threshold-other-program-bytes', type=int)
    w.add_argument('--threshold-waves')
    m = sub.add_parser('move')
    m.add_argument('--candidate', required=True)
    m.add_argument('--work-dir', required=True)
    m.add_argument('--pins-from', action='append', required=True)
    m.add_argument('--follow', action='store_true')
    a = ap.parse_args(argv)
    return wave_check(a) if a.cmd == 'wave' else S1.move_check(a)


if __name__ == '__main__':
    sys.exit(main())

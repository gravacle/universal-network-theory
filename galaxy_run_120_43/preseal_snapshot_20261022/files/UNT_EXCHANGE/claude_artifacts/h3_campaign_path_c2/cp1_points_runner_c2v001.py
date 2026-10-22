"""CP-1 list-of-points runner (Claude2 h3_campaign_path_c2, c2v001; V006 A192 item 2): successor of cp1_runner_c3v004 (3f5e5c18).

Table mode (no --points-list): this CLI IS the c3v004 runner's main(argv), loaded from its pinned bytes; rows 1-31 behave
byte-identically (same code, same records, same runner pin in every record).
List mode (--points-list L --points-list-sha256 H; cp1_points_common_c2v001 for the list rules):
  plan       c3v004 plan() over the list rows (spec pin and key per row; nothing computed);
  run        the c3v004 Scheduler over the list rows, unchanged except that a worker is spawned as THIS file's `worker` with
             the same list pin (c3v004 `worker` knows only its table).  Every gate is c3v004's: taskpolicy -b, python3 -I -B,
             single-thread BLAS, the memory gate and the physical floor, at most one start per poll, and list points wait for
             the anchor's EPS cross-check AGREE in this out-root (the anchor is never a list point, so the out-root must be
             CP-1's own, where the anchor already ran: design map 3.3 "continuing on the same out-root");
  worker     c3v004 run_point on one list row (CONTEXT, GQ, EPS, RHO attempt a; the RHO gate is c3v004's), then
             POINT_LIST_BINDING_<key16>.json (exclusive create) in the point folder: the list pin, the row and this file's pin;
  adapt-eps  c3v004 adapt_point on one list row (the distinct-lane EPS review first; A134 Q8: the one policy review,
             instantiated per point by root's script).
rho-repeat and compare-anchor are anchor-only (table mode).  No producer, review, proof, threshold or format is added.
The LO slot proof (proof side c3v003, cd10cd59) is root's post-run registration step, as for rows 1-31 (S L98).
Exit codes are c3v004's: 0 ok, 2 setup refusal, 3 stopped or blocked.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
SELF = os.path.realpath(__file__)
COMMON2 = (HERE + '/cp1_points_common_c2v001.py', '302abdad6b076190f7bc8e79cc71cf4de91402a1a216eb94c254acf2be22c27e')     # P2


def _load_common2():
    p = COMMON2[0]
    with open(p, 'rb') as f:
        raw = f.read()
    if hashlib.sha256(raw).hexdigest() != COMMON2[1]:
        raise SystemExit('REFUSED: cp1_points_common pin mismatch')
    sp = importlib.util.spec_from_file_location('cp1_points_common_c2v001', p)
    m = importlib.util.module_from_spec(sp)
    sys.modules[sp.name] = m
    exec(compile(raw, p, 'exec'), m.__dict__)
    m.SELF_PIN = {'path': p, 'sha256': hashlib.sha256(raw).hexdigest()}
    return m


P = _load_common2()
R = P.load_module(P.RUNNER[0], P.RUNNER[1], 'cp1_runner_c3v004')
C = R.C
Refusal = C.Refusal


def self_pin():
    return P.pin_of_self(SELF)


def worker_cmd(scheduler, row):
    """The c3v004 Scheduler._spawn command, with THIS file's `worker` and the same list pin."""
    lr = scheduler.list_ref
    return ([C.TASKPOLICY, '-b', sys.executable, '-I', '-B', SELF, 'worker', '--points-list', lr['path'],
             '--points-list-sha256', lr['sha256'], '--out-root', scheduler.out_root, '--point', row['key'],
             '--operator-lane', scheduler.lane, '--attempt', str(scheduler.attempt), '--run-id', scheduler.run_id]
            + R.gate_argv(scheduler.rho_gate_args))


class ListScheduler(R.Scheduler):
    """c3v004 Scheduler; only _spawn differs (the worker is this file's list-mode worker)."""

    def __init__(self, rows, out_root, *, list_ref, **kw):
        if any(r['key'] == C.ANCHOR_KEY for r in rows):
            raise Refusal('ANCHOR_IS_NEVER_A_LIST_POINT')
        super().__init__(rows, out_root, **kw)
        self.list_ref = dict(list_ref)

    def _spawn(self, row):
        cmd = worker_cmd(self, row)
        env = dict(os.environ)
        env.update({k: '1' for k in C.THREAD_ENV})
        logdir = os.path.join(self.out_root, 'worker_logs')
        os.makedirs(logdir, exist_ok=True)
        base = os.path.join(logdir, R.point_dir_name(row, self.attempt) + '_' + (self.run_id or 'run'))
        so = open(base + '.stdout.txt', 'x')
        se = open(base + '.stderr.txt', 'x')
        return subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=so, stderr=se, env=env, close_fds=True)


def run_list_point(row, out_root, *, list_ref, **kw):
    """c3v004 run_point, then the list binding record in the point folder (exclusive create)."""
    rc, summary = R.run_point(row, out_root, **kw)
    pdir = os.path.join(out_root, R.point_dir_name(row, kw.get('attempt', 1)))
    if os.path.isdir(pdir):
        C.write_new(os.path.join(pdir, 'POINT_LIST_BINDING_%s.json' % row['key'][:16]),
                    {'schema': 'CP1_POINT_LIST_BINDING_C2V001', 'utc': C.utc(), 'points_list': dict(list_ref),
                     'row': {k: row[k] for k in ('row', 'key', 'label', 'spec_path', 'spec_sha256', 'wave',
                                                 'pending_spec_sha256')},
                     'exit': rc, 'list_runner': self_pin(), 'c3v004_runner': R.runner_pin()}, out_root)
    return rc, summary


def list_rows(ns):
    ref = {'path': ns.points_list, 'sha256': ns.points_list_sha256}
    doc, rows = P.load_points_list(C, ref)
    return ref, doc, rows


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if '--points-list' not in argv:
        return R.main(argv)                           # table mode: the c3v004 CLI itself
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('plan')
    r = sub.add_parser('run')
    r.add_argument('--out-root', required=True)
    r.add_argument('--operator-lane', required=True)
    r.add_argument('--points')
    r.add_argument('--max-concurrent', type=int, default=4)
    r.add_argument('--margin-pct', type=float, default=5.0)
    r.add_argument('--attempt', type=int, default=1)
    r.add_argument('--hold-file')
    r.add_argument('--swap-hold-mib', type=float, default=512.0)
    r.add_argument('--poll-seconds', type=float, default=60.0)
    r.add_argument('--anchor-tol', type=float, default=R.DEFAULT_TOL)
    r.add_argument('--r2-spike-allowance-gib', type=float, default=R.DEFAULT_R2_SPIKE_ALLOWANCE_GIB)
    r.add_argument('--per-worker-peak-gib', type=float, default=R.DEFAULT_PER_WORKER_PEAK_GIB)
    r.add_argument('--floor-margin-gib', type=float, default=R.DEFAULT_FLOOR_MARGIN_GIB)
    w = sub.add_parser('worker')
    w.add_argument('--out-root', required=True)
    w.add_argument('--point', required=True)
    w.add_argument('--operator-lane', required=True)
    w.add_argument('--attempt', type=int, default=1)
    w.add_argument('--run-id', default='')
    for sp_ in (r, w):
        sp_.add_argument('--allow-rho', action='store_true')
        sp_.add_argument('--proof-side-review-pin')
        sp_.add_argument('--proof-side-review-sha256')
    a = sub.add_parser('adapt-eps')
    a.add_argument('--out-root', required=True)
    a.add_argument('--point', required=True)
    a.add_argument('--attempt', type=int, default=1)
    a.add_argument('--review')
    a.add_argument('--approved-review-sha256')
    a.add_argument('--approved-signer-lane', action='append', default=[])
    for sp_ in (p, r, w, a):
        sp_.add_argument('--points-list', required=True)
        sp_.add_argument('--points-list-sha256', required=True)
    ns = ap.parse_args(argv)
    try:
        if ns.cmd in ('run', 'worker', 'adapt-eps'):
            R.require_compute_environment()           # before any path is created or any input read (as c3v004)
        ref, doc, rows = list_rows(ns)
        if ns.cmd == 'plan':
            out = R.plan(rows)
            out.update(points_list=ref, list_runner=self_pin(), wave=doc['wave'])
            print(json.dumps(out, indent=1, sort_keys=True))
            return 0
        if getattr(ns, 'attempt', 1) < 1:
            raise Refusal('ATTEMPT_MUST_BE_POSITIVE')
        if ns.cmd == 'run':
            R.require_anchor_tol(ns.anchor_tol)
            R.require_nonnegative('SWAP_HOLD_MIB', ns.swap_hold_mib)
            for name in ('r2_spike_allowance_gib', 'per_worker_peak_gib', 'floor_margin_gib'):
                R.require_nonnegative(name.upper(), getattr(ns, name))
        out_root = R.validate_out_root(ns.out_root)
        if ns.cmd == 'run':
            if ns.poll_seconds < 10:
                raise Refusal('POLL_SECONDS_MIN_10')
            sel = P.select_list_rows(C, rows, ns.points)
            os.makedirs(out_root, exist_ok=True)
            if os.path.realpath(out_root) != out_root:
                raise Refusal('OUT_ROOT_NOT_CANONICAL')
            run_id = C.utc_compact() + '_%d' % os.getpid()
            log = C.LineLog(os.path.join(out_root, 'SCHEDULER_%s.jsonl' % run_id), out_root)
            log.write({'event': 'POINTS_LIST', 'utc': C.utc(), 'points_list': ref, 'list_runner': self_pin(),
                       'wave': doc['wave'], 'points': [x['key'] for x in sel]})
            s = ListScheduler(sel, out_root, list_ref=ref, operator_lane=ns.operator_lane, max_concurrent=ns.max_concurrent,
                              margin_pct=ns.margin_pct, attempt=ns.attempt, hold_file=ns.hold_file,
                              swap_hold_mib=ns.swap_hold_mib, poll_seconds=ns.poll_seconds, log=log, tol=ns.anchor_tol,
                              run_id=run_id, r2_spike_allowance_gib=ns.r2_spike_allowance_gib,
                              per_worker_peak_gib=ns.per_worker_peak_gib, floor_margin_gib=ns.floor_margin_gib,
                              rho_gate_args=R.gate_args_from_cli(ns))
            rc = s.run()
            log.close()
            print(json.dumps({'status': 'DONE' if rc == 0 else 'STOPPED', 'results': s.results, 'stopped': s.stopped,
                              'log': log.path}))
            return rc
        if ns.cmd == 'worker':
            hit = [x for x in rows if x['key'] == ns.point]
            if len(hit) != 1:
                raise Refusal('WORKER_POINT_KEY_NOT_IN_LIST')
            if not os.path.isdir(out_root):
                raise Refusal('OUT_ROOT_MISSING')
            rc, summary = run_list_point(hit[0], out_root, list_ref=ref, operator_lane=ns.operator_lane,
                                         attempt=ns.attempt, run_id=ns.run_id, rho_gate_args=R.gate_args_from_cli(ns))
            print(json.dumps(summary, default=str))
            return rc
        sel = P.select_list_rows(C, rows, ns.point)
        if len(sel) != 1:
            raise Refusal('ONE_POINT_REQUIRED')
        rc, res = R.adapt_point(sel[0], out_root, review_path=ns.review, approved_review_sha256=ns.approved_review_sha256,
                                approved_signer_lanes=ns.approved_signer_lane, attempt=ns.attempt)
        print(json.dumps(res, default=str))
        return rc
    except Refusal as exc:
        print(json.dumps({'status': 'REFUSED', 'reason': str(exc)}))
        return 2


if __name__ == '__main__':
    sys.exit(main())

"""Phase-2 schedule-ceiling record writer (Claude3; backlog #8, V006 A272 open item, A253 interface). Root runs it.
No launch, no run-content read: a closure binds a call by its registered identity and, optionally, its last receipt
by pin (the receipt bytes are hashed, never parsed).

  register  writes SCHEDULE_CEILING_REGISTRATION_C2V001 for a phase, dated no later than the adopted ceiling.
  close     writes one SCHEDULE_CEILING_CLOSURE_C2V002 for one registered call, dated at or after the ceiling.

Every record is checked by the UNCHANGED consumer, roster_builder_c2v007_cx3cw8v003.interruption_policy (pinned by
sha), on a private validation copy BEFORE the exclusive write; the copy is removed. Exit 0 written; 2 refused.

usage:
  python3 -I -B schedule_ceiling_writer_c3v001.py register --phase PHASE_2 --out NEW
  python3 -I -B schedule_ceiling_writer_c3v001.py close --phase PHASE_2 --registration P --registration-sha256 H
         --call P --call-sha256 H (--last-receipt P --last-receipt-sha256 H | --no-last-receipt) --out NEW
  where --call is a JSON file holding exactly {alternative, kind, key, theta_sha256, spec_sha256}: the call's launch
  registry binding, as the roster builder's _ceiling_or_hold compares it.
"""
import argparse, hashlib, json, os, shutil, stat, sys, types
from datetime import datetime, timezone

RB = {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/roster_builder_c2v007_cx3cw8v003.py',
      'sha256': 'f710334b6f5ec2663fbebd826c7b326ebf7ff9eb600e751584de4f518a4e0b11'}
CEILINGS = {'PHASE_1': '2026-11-06T05:59:00Z', 'PHASE_2': '2026-12-01T05:59:00Z'}   # roster builder L4598, A246/A249
CALL_KEYS = ('alternative', 'kind', 'key', 'theta_sha256', 'spec_sha256')


class Refused(Exception):
    pass


def need(ok, why):
    if not ok:
        raise Refused(why)


def now_utc():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def read_pin(path, sha256, label, cap=64 * 2**20):
    need(isinstance(path, str) and os.path.isabs(path) and os.path.normpath(path) == path, 'PATH_ABSOLUTE_NORMALIZED:' + label)
    need(isinstance(sha256, str) and len(sha256) == 64 and all(c in '0123456789abcdef' for c in sha256), 'SHA_FORM:' + label)
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        before = os.fstat(fd); need(stat.S_ISREG(before.st_mode), 'NOT_REGULAR:' + label)
        chunks, total = [], 0
        while True:
            b = os.read(fd, 1 << 20)
            if not b:
                break
            chunks.append(b); total += len(b); need(total <= cap, 'TOO_LARGE:' + label)
        after = os.fstat(fd)
        need(all(getattr(before, k) == getattr(after, k) for k in ('st_dev', 'st_ino', 'st_size', 'st_mtime_ns')), 'INPUT_CHANGED:' + label)
    finally:
        os.close(fd)
    raw = b''.join(chunks); need(hashlib.sha256(raw).hexdigest() == sha256, 'SHA_MISMATCH:' + label)
    return raw


RB_SHA = RB['sha256']


def load_rb():
    raw = read_pin(RB['path'], RB_SHA, 'roster builder')
    m = types.ModuleType('roster_builder_c2v007_cx3cw8v003_consumer'); m.__file__ = RB['path']
    exec(compile(raw, RB['path'], 'exec'), m.__dict__)
    return m


def encode(obj):
    return (json.dumps(obj, sort_keys=True, indent=2, allow_nan=False) + '\n').encode('ascii')


def check_out(out):
    need(isinstance(out, str) and os.path.isabs(out) and os.path.normpath(out) == out, 'OUT_ABSOLUTE_NORMALIZED')
    need(os.path.isdir(os.path.dirname(out)) and not os.path.lexists(out), 'OUT_MUST_BE_NEW')


def write_new(out, raw):
    check_out(out)
    with open(out, 'xb') as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    return {'path': out, 'sha256': hashlib.sha256(raw).hexdigest()}


def validate_with_consumer(rb, phase, registration_pin, closure_raw=None):
    """Run the unchanged interruption_policy on a private copy: a minimal INTERRUPTION_POLICY_C2V002 that names the
    registration and (for close) the candidate closure. Nothing here becomes a root record; the folder is removed."""
    work = os.path.join(os.path.dirname(registration_pin['path']), '.schedule_ceiling_validation_%d' % os.getpid())
    need(not os.path.lexists(work), 'VALIDATION_DIR_EXISTS')
    os.mkdir(work)
    try:
        closures = []
        if closure_raw is not None:
            cp = os.path.join(work, 'CLOSURE_CANDIDATE.json')
            with open(cp, 'xb') as f: f.write(closure_raw)
            closures.append({'path': cp, 'sha256': hashlib.sha256(closure_raw).hexdigest()})
        pol = {'schema': rb.INTERRUPTION_POLICY_SCHEMA, 'phase': phase, 'cause_producer': None, 'deadline_utc': CEILINGS[phase],
               'deadline_registration': registration_pin, 'attempts': [], 'closures': closures}
        pp = os.path.join(work, 'POLICY_CANDIDATE.json'); praw = encode(pol)
        with open(pp, 'xb') as f: f.write(praw)
        try:
            res = rb.interruption_policy({'path': pp, 'sha256': hashlib.sha256(praw).hexdigest()}, phase)
        except rb.Refused as e:
            raise Refused('CONSUMER_REFUSED:%s' % (e,))
        return res
    finally:
        shutil.rmtree(work)


def cmd_register(rb, a):
    check_out(a.out)
    need(a.phase in CEILINGS, 'PHASE')
    stamp = now_utc()
    need(rb.parse_utc_ns(stamp, 'now') <= rb.parse_utc_ns(CEILINGS[a.phase], 'ceiling'), 'REGISTRATION_AFTER_CEILING')
    raw = encode({'schema': 'SCHEDULE_CEILING_REGISTRATION_C2V001', 'phase': a.phase, 'deadline_utc': CEILINGS[a.phase], 'date_u': stamp})
    # validate: the consumer reads the registration by pin, so validate the exact bytes at a private path first
    work = os.path.join(os.path.dirname(a.out), '.schedule_ceiling_registration_%d' % os.getpid())
    need(not os.path.lexists(work), 'VALIDATION_DIR_EXISTS'); os.mkdir(work)
    try:
        rp = os.path.join(work, 'REGISTRATION_CANDIDATE.json')
        with open(rp, 'xb') as f: f.write(raw)
        validate_with_consumer(rb, a.phase, {'path': rp, 'sha256': hashlib.sha256(raw).hexdigest()})
    finally:
        shutil.rmtree(work)
    return write_new(a.out, raw)


def cmd_close(rb, a):
    check_out(a.out)
    need(a.phase in CEILINGS, 'PHASE')
    reg_pin = {'path': a.registration, 'sha256': a.registration_sha256}
    reg = json.loads(read_pin(a.registration, a.registration_sha256, 'registration'))
    need(isinstance(reg, dict) and reg.get('schema') == 'SCHEDULE_CEILING_REGISTRATION_C2V001' and reg.get('phase') == a.phase, 'REGISTRATION_SCHEMA')
    call = json.loads(read_pin(a.call, a.call_sha256, 'call binding'))
    need(isinstance(call, dict) and set(call) == set(CALL_KEYS), 'CALL_KEYS')
    last = None
    if a.last_receipt is not None:
        read_pin(a.last_receipt, a.last_receipt_sha256, 'last receipt')       # hashed, never parsed
        last = {'path': os.path.realpath(a.last_receipt), 'sha256': a.last_receipt_sha256}
    stamp = now_utc()
    need(rb.parse_utc_ns(stamp, 'now') >= rb.parse_utc_ns(CEILINGS[a.phase], 'ceiling'), 'CLOSURE_BEFORE_CEILING')
    raw = encode({'schema': rb.CEILING_SCHEMA, 'phase': a.phase, 'date_u': stamp, 'deadline_utc': CEILINGS[a.phase],
                  'deadline_registration': {'path': os.path.realpath(a.registration), 'sha256': a.registration_sha256},
                  'call': call, 'last_receipt': last})
    res = validate_with_consumer(rb, a.phase, reg_pin, raw)
    need(len(res['closures']) == 1, 'CONSUMER_CLOSURE_COUNT')
    return write_new(a.out, raw)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, allow_abbrev=False)
    sub = ap.add_subparsers(dest='cmd', required=True)
    r = sub.add_parser('register', allow_abbrev=False); r.add_argument('--phase', required=True); r.add_argument('--out', required=True)
    c = sub.add_parser('close', allow_abbrev=False)
    for x in ('phase', 'registration', 'registration-sha256', 'call', 'call-sha256', 'out'):
        c.add_argument('--' + x, required=True)
    g = c.add_mutually_exclusive_group(required=True)
    g.add_argument('--last-receipt'); g.add_argument('--no-last-receipt', action='store_true')
    c.add_argument('--last-receipt-sha256')
    a = ap.parse_args(argv)
    try:
        need(sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1, 'RUN_WITH_-I_-B')
        if a.cmd == 'close':
            need((a.last_receipt is None) == (a.last_receipt_sha256 is None), 'LAST_RECEIPT_PIN_PAIR')
        rb = load_rb()
        out = cmd_register(rb, a) if a.cmd == 'register' else cmd_close(rb, a)
        print(json.dumps({'written': out, 'command': a.cmd}, sort_keys=True)); return 0
    except (Refused, ValueError, OSError, KeyError, TypeError, AttributeError) as e:
        print(json.dumps({'refused': '%s: %s' % (type(e).__name__, e)})); return 2


if __name__ == '__main__':
    sys.exit(main())

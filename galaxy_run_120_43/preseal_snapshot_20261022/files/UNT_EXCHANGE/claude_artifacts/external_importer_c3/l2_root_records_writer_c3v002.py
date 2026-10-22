"""L2 root-record writer, successor c3v002 (Claude3; root 0867, deputy D030/D031; fixes Codex1 0275 B1, N1, N2). Root runs it. It never launches, admits or reads science.

  direct-launch  writes SPECULATIVE_LAUNCH_L2_V001 at the direct 7-call launch, after the P2 direct-batch capture and
                 after the operational importer freeze (A283 item 1, D005 item 5).
  binding        writes SPECULATIVE_REGISTER_BINDING_L2_V001 (stage b) at campaign init, after the P2 campaign capture
                 (A283 item 1(b), D005 items 2-3).

Every input is read once by pin into a verified byte cache (O_NOFOLLOW|O_NONBLOCK, regular file, running size cap,
fstat stable across the read, sha256 from bytes, strict JSON); the consumers read the same cached bytes. BOTH
subcommands then check the new record with the UNCHANGED pinned consumers of external_importer_cx1 BEFORE the exclusive
write: direct-launch runs select_two_stage on all 7 register entries (through an internal validation-only binding
object that is never written) and the full check_launches on the new launch record; binding runs select_two_stage and
check_launches on the real binding. Exit 0 written; 2 refused (nothing written).

usage:
  python3 -I -B l2_root_records_writer_c3v001.py direct-launch --register P --register-sha256 H --freeze P --freeze-sha256 H
         --direct-capture P --direct-capture-sha256 H --out NEW
  python3 -I -B l2_root_records_writer_c3v001.py binding --register P --register-sha256 H --freeze P --freeze-sha256 H
         --direct-launch P --direct-launch-sha256 H --campaign-capture P --campaign-capture-sha256 H
         --config-sha256 X --cache-id X --gate-digest X --out NEW
"""
import argparse, hashlib, json, os, stat, sys, types
from datetime import datetime, timezone
from pathlib import Path

CX1 = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/external_importer_cx1')
# Load order matters: each module's imports resolve from those loaded before it.
DEPS = (('snapshot_cx1v001', '036cf99ec6f6d2710f36134ece719e064bbb4a4abca550e752fde3e28c2a1279'),
        ('direct_layout_cx1v001', 'f9f51eda9289edc8ccf8d4d2842d468ce042c06bb22edbb703ceb4638c110b61'),
        ('request_guard_cx1v002', '914ccc0d3b8fe256922603662952fad6704f8d3f9a3ccdb5e8ad5afe068b4e79'),
        ('register_two_stage_cx1v002', '0b4fa008dd75324d9b362767b1bddd28ad6be4974767d613b29fd84254fdab44'),
        ('register_two_stage_cx1v003', '0d5aae44b6afefcd889ffc99ca4288a371722085f21e7469c7d1a0d16ff4e87c'),
        ('runtime_launch_binding_cx1v001', '8d90d1e6da4f9ea96c66bba69797820621e7a5ef6edfb90335bd125cbb1c7d04'),
        ('runtime_policy_cx1v001', 'a20d03fe9a7bc3c4ec0cb9fafa0bbbd8c91b41a43cfbec7f087c4b9468672269'),
        ('runtime_fingerprints_cx1v002', '5ec4f8c652917321c449d84b3272ed6f97504b002312ba8d89da583c1b00fc31'),
        ('runtime_distribution_record_cx1v004', '13fb69482de279bf758da158763c30d3951d3003bb3958da6ccbe500e317b522'))
P2_PRODUCER = {'path': str(CX1 / 'runtime_distribution_capture_cx1v004.py'),
               'sha256': 'f9c508a63be61303fa9cc3030fe5a547b468e100450eb7072802b749becac64c'}   # policy V007_F2 runtime_capture.producer
ROWS = {28, 29, 30, 31, 300, 301, 302}


class Refused(Exception):
    pass


def need(ok, why):
    if not ok:
        raise Refused(why)


def sha_hex(x):
    return isinstance(x, str) and len(x) == 64 and all(c in '0123456789abcdef' for c in x)


def load_deps():
    mods = {}
    for name, prefix in DEPS:
        need(name not in sys.modules, 'DEPENDENCY_ALREADY_LOADED:' + name)
        p = CX1 / (name + '.py')
        st = os.lstat(p); need(stat.S_ISREG(st.st_mode), 'DEPENDENCY_NOT_REGULAR:' + name)
        raw = p.read_bytes(); need(hashlib.sha256(raw).hexdigest() == prefix, 'DEPENDENCY_PIN:' + name)
        m = types.ModuleType(name); m.__file__ = str(p); sys.modules[name] = m
        exec(compile(raw, str(p), 'exec'), m.__dict__); mods[name] = m
    return mods


CAP = 8 * 2**20
CACHE = {}                                   # (path, sha256) -> verified bytes; every pin is read from disk once


def read_pin(path, sha256, label):
    need(isinstance(path, str) and os.path.isabs(path) and os.path.normpath(path) == path, 'PATH_ABSOLUTE_NORMALIZED:' + label)
    need(sha_hex(sha256), 'SHA_FORM:' + label)
    if (path, sha256) in CACHE:
        return CACHE[(path, sha256)]
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)      # N1: a FIFO cannot block before the check
    try:
        before = os.fstat(fd); need(stat.S_ISREG(before.st_mode), 'NOT_REGULAR:' + label); need(before.st_size <= CAP, 'TOO_LARGE:' + label)
        chunks, total = [], 0
        while True:
            b = os.read(fd, 1 << 20)
            if not b:
                break
            chunks.append(b); total += len(b); need(total <= CAP, 'TOO_LARGE:' + label)     # N1: running cap
        after = os.fstat(fd)
        need(all(getattr(before, k) == getattr(after, k) for k in ('st_dev', 'st_ino', 'st_size', 'st_mtime_ns', 'st_ctime_ns')), 'INPUT_CHANGED:' + label)
    finally:
        os.close(fd)
    raw = b''.join(chunks); need(hashlib.sha256(raw).hexdigest() == sha256, 'SHA_MISMATCH:' + label)
    CACHE[(path, sha256)] = raw
    return raw


class MemSnapshot:
    """The consumers' snapshot interface (document) over pinned disk reads plus records held in memory."""
    def __init__(self, strict_json, mem):
        self.strict_json = strict_json; self.mem = dict(mem)

    def document(self, pin):
        need(isinstance(pin, dict) and set(pin) == {'path', 'sha256'}, 'PIN_SHAPE')
        key = (pin['path'], pin['sha256'])
        raw = self.mem[key] if key in self.mem else read_pin(pin['path'], pin['sha256'], 'consumer read')   # cached: read once
        return self.strict_json(raw)


def iso_now():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')


def parse_utc(s, label):
    try:
        t = datetime.fromisoformat(str(s).replace('Z', '+00:00'))
    except ValueError:
        raise Refused('UTC_FORMAT:' + label)
    need(t.tzinfo is not None, 'UTC_TIMEZONE:' + label); return t


def encode(obj):
    return (json.dumps(obj, sort_keys=True, indent=2, allow_nan=False) + '\n').encode('ascii')


def common(M, a):
    sj = M['snapshot_cx1v001'].strict_json; R = M['runtime_distribution_record_cx1v004']
    reg_pin = {'path': a.register, 'sha256': a.register_sha256}; frz_pin = {'path': a.freeze, 'sha256': a.freeze_sha256}
    reg = sj(read_pin(a.register, a.register_sha256, 'register')); frz = sj(read_pin(a.freeze, a.freeze_sha256, 'freeze'))
    need(isinstance(reg, dict) and set(reg) == {'schema', 'entries'} and reg['schema'] == 'SPECULATIVE_REGISTER_L2_V001', 'REGISTER_SCHEMA')
    need(isinstance(reg['entries'], list) and len(reg['entries']) == 7 and {e.get('row') for e in reg['entries']} == ROWS, 'REGISTER_SEVEN_ROWS')
    need(isinstance(frz, dict) and set(frz) == {'schema', 'utc', 'policy', 'entry'} and frz['schema'] == 'CX1_IMPORTER_FREEZE_V001', 'FREEZE_SCHEMA')
    caps = {json.dumps(e.get('runtime_capture'), sort_keys=True) for e in reg['entries']}
    need(len(caps) == 1, 'REGISTER_ONE_DIRECT_CAPTURE')          # D005: one direct-batch capture before the 7-call launch
    direct_pin = reg['entries'][0]['runtime_capture']
    return sj, R, reg_pin, frz_pin, reg, frz, direct_pin


def check_capture(R, sj, pin, frz, label):
    rec = sj(read_pin(pin['path'], pin['sha256'], label + ' capture'))
    try:
        R.validate(rec)
    except ValueError as e:
        raise Refused('CAPTURE_INVALID:%s:%s' % (label, e))
    need(rec.get('producer') == P2_PRODUCER, 'CAPTURE_PRODUCER_NOT_P2:' + label)   # D028 F2: P2 is the only producer
    ident = rec.get('interpreter') or {}
    need(isinstance(ident, dict) and isinstance(ident.get('realpath'), str) and sha_hex(ident.get('sha256')), 'CAPTURE_INTERPRETER:' + label)
    need(parse_utc(frz['utc'], 'freeze') < parse_utc(rec.get('captured_utc'), label), 'CAPTURE_BEFORE_FREEZE:' + label)
    return rec, {'realpath': ident['realpath'], 'sha256': ident['sha256']}


def check_out(out):
    need(isinstance(out, str) and os.path.isabs(out) and os.path.normpath(out) == out, 'OUT_ABSOLUTE_NORMALIZED')
    need(os.path.isdir(os.path.dirname(out)) and not os.path.lexists(out), 'OUT_MUST_BE_NEW')


def write_new(out, raw):
    check_out(out)
    with open(out, 'xb') as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    return {'path': out, 'sha256': hashlib.sha256(raw).hexdigest()}


def direct_launch(M, a):
    check_out(a.out)                                                  # first: before any read or consumer run
    sj, R, reg_pin, frz_pin, reg, frz, direct_pin = common(M, a)
    need(direct_pin == {'path': a.direct_capture, 'sha256': a.direct_capture_sha256}, 'DIRECT_CAPTURE_NOT_THE_REGISTERED_ONE')
    rec, ident = check_capture(R, sj, direct_pin, frz, 'direct')
    utc = iso_now(); need(parse_utc(rec['captured_utc'], 'direct') < parse_utc(utc, 'now'), 'CAPTURE_NOT_BEFORE_LAUNCH')
    launch = {'schema': 'SPECULATIVE_LAUNCH_L2_V001', 'utc': utc, 'register': reg_pin, 'runtime_capture': direct_pin, 'interpreter': ident, 'freeze': frz_pin}
    raw = encode(launch); lpin = {'path': a.out, 'sha256': hashlib.sha256(raw).hexdigest()}
    # B1 (Codex1 0275): run the UNCHANGED consumer contracts before publication. The binding object below is an
    # internal, validation-only stand-in (context all zeros, never written, never a root record): select_two_stage
    # needs one to reach its register-entry checks, and check_launches is run with the direct side mirrored as the
    # campaign side so that every launch-record clause (schema, association, freeze code pins, interpreter, window) runs.
    vbind_raw = encode({'schema': 'SPECULATIVE_REGISTER_BINDING_L2_V001', 'register': reg_pin,
                        'context': {'config_sha256': '0' * 64, 'cache_id': '0' * 64, 'gate_digest': '0' * 64},
                        'campaign_capture': direct_pin, 'utc': utc, 'interpreter': ident, 'freeze': frz_pin})
    vpin = {'path': a.out + '.INTERNAL_VALIDATION_ONLY', 'sha256': hashlib.sha256(vbind_raw).hexdigest()}
    snap = MemSnapshot(sj, {(lpin['path'], lpin['sha256']): raw, (vpin['path'], vpin['sha256']): vbind_raw})
    Refusal = M['snapshot_cx1v001'].Refusal
    try:
        for e in reg['entries']:
            sel = M['register_two_stage_cx1v003'].select_two_stage(snap, register_pin=reg_pin, binding_pin=vpin,
                                                                   context={'config_sha256': '0' * 64, 'cache_id': '0' * 64, 'gate_digest': '0' * 64},
                                                                   key=e.get('key'), spec_pin=e.get('spec'))
            need(sel['entry'] == e, 'CONSUMER_ENTRY_MISMATCH')
        vb = sj(vbind_raw)
        M['runtime_launch_binding_cx1v001'].check_launches(snap, freeze_pin=frz_pin, launch_pin=lpin, register_pin=reg_pin, binding=vb,
                                                          direct_pin=direct_pin, campaign_pin=direct_pin, direct=rec, campaign=rec)
    except Refusal as e:
        raise Refused('CONSUMER_REFUSED:%s' % e)
    return write_new(a.out, raw)


def binding(M, a):
    check_out(a.out)                                                  # first: before any read or consumer run
    sj, R, reg_pin, frz_pin, reg, frz, direct_pin = common(M, a)
    ctx = {'config_sha256': a.config_sha256, 'cache_id': a.cache_id, 'gate_digest': a.gate_digest}
    need(all(sha_hex(v) for v in ctx.values()), 'CONTEXT_FORM')
    launch_pin = {'path': a.direct_launch, 'sha256': a.direct_launch_sha256}
    camp_pin = {'path': a.campaign_capture, 'sha256': a.campaign_capture_sha256}
    direct, _ = check_capture(R, sj, direct_pin, frz, 'direct')
    campaign, ident = check_capture(R, sj, camp_pin, frz, 'campaign')
    try:
        R.compare(direct, campaign)                                 # D005 item 3, refused here rather than at admission
    except ValueError as e:
        raise Refused('RUNTIME_DIRECT_CAMPAIGN_DIFFER:%s' % e)
    utc = iso_now(); need(parse_utc(campaign['captured_utc'], 'campaign') < parse_utc(utc, 'now'), 'CAPTURE_NOT_BEFORE_BINDING')
    b = {'schema': 'SPECULATIVE_REGISTER_BINDING_L2_V001', 'register': reg_pin, 'context': ctx, 'campaign_capture': camp_pin,
         'utc': utc, 'interpreter': ident, 'freeze': frz_pin}
    raw = encode(b); bpin = {'path': a.out, 'sha256': hashlib.sha256(raw).hexdigest()}
    snap = MemSnapshot(sj, {(bpin['path'], bpin['sha256']): raw})
    Refusal = M['snapshot_cx1v001'].Refusal
    try:
        for e in reg['entries']:                                     # the unchanged stage-b consumer, for every key
            sel = M['register_two_stage_cx1v003'].select_two_stage(snap, register_pin=reg_pin, binding_pin=bpin, context=ctx,
                                                                   key=e['key'], spec_pin=e['spec'])
            need(sel['entry'] == e, 'CONSUMER_ENTRY_MISMATCH')
        M['runtime_launch_binding_cx1v001'].check_launches(snap, freeze_pin=frz_pin, launch_pin=launch_pin, register_pin=reg_pin,
                                                          binding=b, direct_pin=direct_pin, campaign_pin=camp_pin, direct=direct, campaign=campaign)
    except Refusal as e:
        raise Refused('CONSUMER_REFUSED:%s' % e)
    return write_new(a.out, raw)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, allow_abbrev=False)
    sub = ap.add_subparsers(dest='cmd', required=True)
    for name in ('direct-launch', 'binding'):
        p = sub.add_parser(name, allow_abbrev=False)
        for x in ('register', 'freeze'):
            p.add_argument('--' + x, required=True); p.add_argument('--' + x + '-sha256', required=True)
        if name == 'direct-launch':
            p.add_argument('--direct-capture', required=True); p.add_argument('--direct-capture-sha256', required=True)
        else:
            for x in ('direct-launch', 'campaign-capture'):
                p.add_argument('--' + x, required=True); p.add_argument('--' + x + '-sha256', required=True)
            for x in ('config-sha256', 'cache-id', 'gate-digest'):
                p.add_argument('--' + x, required=True)
        p.add_argument('--out', required=True)
    a = ap.parse_args(argv)
    try:
        need(sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1, 'RUN_WITH_-I_-B')
        M = load_deps()
        out = direct_launch(M, a) if a.cmd == 'direct-launch' else binding(M, a)
        print(json.dumps({'written': out, 'schema': 'SPECULATIVE_LAUNCH_L2_V001' if a.cmd == 'direct-launch' else 'SPECULATIVE_REGISTER_BINDING_L2_V001'}, sort_keys=True))
        return 0
    except (Refused, ValueError, OSError, KeyError, TypeError, AttributeError) as e:
        print(json.dumps({'refused': '%s: %s' % (type(e).__name__, e)})); return 2
    except BaseException as e:                       # the cx1 snapshot Refusal derives from BaseException
        if type(e).__name__ != 'Refusal':
            raise
        print(json.dumps({'refused': 'Refusal: %s' % e})); return 2


if __name__ == '__main__':
    sys.exit(main())

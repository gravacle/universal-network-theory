# Claude4 (dispatch 0584): shared helpers for the V007 root-side seal checks. Read-only: nothing here writes a file or starts a process.
# Strict JSON (a duplicate key anywhere refuses, A71), pins verified from bytes, a typed refusal list, and a CLI parser that refuses
# abbreviations and repeated flags (A76 SF-ARGV, A79.2).
import argparse, hashlib, json, os, re, sys
from pathlib import Path

HEX64 = re.compile(r'[0-9a-f]{64}')
PENDING_RX = re.compile(r'PENDING', re.I)
AUTHORITY = {'identity': 'Claude2', 'role': 'coordinator_and_single_scientific_launch_owner'}   # FORMAT_V004; guard v008 AUTHORITY
PYTHON = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
PIN_NAMES = ('V007_PREREG_SHA256', 'PIN_ADDENDUM_V005', 'PIN_DRIVER_BUILD_RECORD', 'PIN_V010_R5_CHECK', 'PIN_PRODUCER_REGISTRY')   # A82


class DuplicateKey(ValueError):
    pass


def _pairs(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise DuplicateKey('DUPLICATE_JSON_KEY %r' % k)
        out[k] = v
    return out


def _no_constant(c):
    raise ValueError('NON_FINITE_JSON_CONSTANT ' + c)


def strict_json_bytes(raw):
    return json.loads(raw, object_pairs_hook=_pairs, parse_constant=_no_constant)


def strict_json(path):
    return strict_json_bytes(Path(path).read_bytes())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class Checker:
    def __init__(self, name):
        self.name = name
        self.failures = []
        self.notes = []
        self.pins = {}

    def fail(self, code, detail=''):
        self.failures.append({'code': code, 'detail': detail})

    def note(self, code, detail=''):
        self.notes.append({'code': code, 'detail': detail})

    def pin(self, label, ref, must_exist=True):
        """ref must be exactly {path, sha256}; the path a regular file (symlink allowed only if it resolves to a regular file) whose bytes hash to sha256."""
        if not isinstance(ref, dict) or set(ref) != {'path', 'sha256'}:
            self.fail('PIN_SHAPE', '%s: %r' % (label, ref))
            return False
        p, h = ref['path'], ref['sha256']
        if not isinstance(p, str) or not isinstance(h, str) or not Path(p).is_absolute():
            self.fail('PIN_TYPES', label)
            return False
        if PENDING_RX.search(p) or PENDING_RX.search(h):
            self.fail('PIN_PENDING', label)
            return False
        if not HEX64.fullmatch(h):
            self.fail('PIN_SHA_FORMAT', '%s: %s' % (label, h))
            return False
        if not Path(p).is_file():
            self.fail('PIN_FILE_MISSING', '%s: %s' % (label, p))
            return False
        got = sha(p)
        if got != h:
            self.fail('PIN_BYTES_MISMATCH', '%s: %s has %s, pinned %s' % (label, p, got, h))
            return False
        self.pins[label] = {'path': p, 'sha256': h}
        return True

    def result(self):
        return {'check': self.name, 'verdict': 'PASS' if not self.failures else 'REFUSE', 'failures': self.failures, 'notes': self.notes, 'pins_verified': self.pins}


def no_pending_anywhere(chk, label, obj, path='$'):
    if isinstance(obj, str):
        if PENDING_RX.search(obj):
            chk.fail('PENDING_VALUE', '%s at %s' % (label, path))
    elif isinstance(obj, dict):
        for k, v in obj.items():
            no_pending_anywhere(chk, label, v, '%s.%s' % (path, k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            no_pending_anywhere(chk, label, v, '%s[%d]' % (path, i))
    elif obj is None:
        chk.fail('NULL_VALUE', '%s at %s' % (label, path))


def find_key(obj, key, path='$'):
    """every (path, value) for dict key `key`, recursively"""
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key:
                out.append((path + '.' + k, v))
            out += find_key(v, key, path + '.' + k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out += find_key(v, key, '%s[%d]' % (path, i))
    return out


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        print(json.dumps({'verdict': 'REFUSE', 'failures': [{'code': 'CLI_ARGUMENTS', 'detail': 'usage error'}]}))
        raise SystemExit(2)


def parser(desc):
    return _Parser(description=desc, allow_abbrev=False)


def parse_args(p, argv=None):
    argv = sys.argv[1:] if argv is None else argv
    flags = [a.split('=', 1)[0] for a in argv if a.startswith('--')]
    if len(flags) != len(set(flags)):
        print(json.dumps({'verdict': 'REFUSE', 'failures': [{'code': 'CLI_REPEATED_FLAG', 'detail': 'a flag is repeated'}]}))
        raise SystemExit(2)
    return p.parse_args(argv)


def emit(res):
    print(json.dumps(res, indent=1, sort_keys=True))
    return 0 if res['verdict'] == 'PASS' else 2

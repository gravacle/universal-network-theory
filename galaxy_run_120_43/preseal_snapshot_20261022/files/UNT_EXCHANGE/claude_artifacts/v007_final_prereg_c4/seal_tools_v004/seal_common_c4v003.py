# Claude4 seal tools v003 (dispatches 0633/0634; v002: A99 item 4, dispatch 0621): shared helpers for the V007 root-side seal checks. Read-only: nothing here
# writes a file or starts a process. Successor of seal_common_c4v001.py (43d8f8eb): the same strict JSON (a duplicate key anywhere
# refuses, A71), pins verified from bytes, typed refusal list and CLI parser (no abbreviations, no repeated flag; A76 SF-ARGV,
# A79.2). New in v002: a pin-shape predicate, the BUILD allowlist parser shared by tool 3 and the builder, a guard that turns any
# unexpected exception into a coded refusal (D-07: a code, never a traceback), and the in-process loader of the reviewed compare
# (bytes read once, hashed, then compiled from those bytes). r2 (A102, A-B1 class): json_or_text, a JSON-or-text probe whose only
# text fallback is a JSON syntax error.
# v003 (successor of r2 seal_common_c4v002.py f41b0fca; D-05, dispatch 0633): strict_json_typed, the parse of root's later-entry
# dispositions file (r2's strict JSON with native integers, on the file's UTF-8 text, no text fallback) with one typed code per defect
# class; covered_later_flag / covered_later_refusal, the typed refusal of the removed bare --covered-later list.
import argparse, hashlib, json, os, re, sys, types
from pathlib import Path

HEX64 = re.compile(r'[0-9a-f]{64}')
PENDING_RX = re.compile(r'PENDING', re.I)
AUTHORITY = {'identity': 'Claude2', 'role': 'coordinator_and_single_scientific_launch_owner'}   # FORMAT_V004; guard v008 AUTHORITY
PYTHON = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
PIN_NAMES = ('V007_PREREG_SHA256', 'PIN_ADDENDUM_V005', 'PIN_DRIVER_BUILD_RECORD', 'PIN_V010_R5_CHECK', 'PIN_PRODUCER_REGISTRY')   # A82
PENDING_BUILD_V007 = 'PENDING_BUILD_V007'          # A99.1: the literal pin of BUILD_V007 until it lands (never a guessed sha)
BUILD_V007_NAME = 'BUILD_V007.md'                  # A99.1: the launch-packet BUILD of record
BUILD_ALLOWLIST_COUNT = 15                         # A99.1 V6-S3
BUILD_HEADER = '## Supported runtime entry allowlist'
ADMISSION_SCHEMA = 'UNT_ROOT_SEAL_ADMISSION_CX1V001'   # ROOT_SEAL_ADMISSION_FORMAT_V004; guard v008 L27
DISPOSITIONS_SCHEMA = 'UNT_V007_LATER_ENTRY_DISPOSITIONS_C4V001'   # v003 D-05 (0633): root's byte-pinned later-entry dispositions
COVERED_LATER_REMOVED = ('the bare covered-later list is removed in v003 (D-05, 0633): root supplies the byte-pinned dispositions file instead '
                         '(--dispositions D.json --dispositions-sha H; API dispositions=(path, sha256))')


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


def json_or_text(raw):
    """A102 (A-B1 class): (True, obj) for strict JSON, (False, None) for text that is not JSON at all. Only a JSON syntax error means
    "text"; integers are parsed as strings so a 4,300+ digit literal cannot raise before the duplicate hook; a duplicate key or any
    other ValueError (a non-finite constant, undecodable bytes) propagates and the caller refuses."""
    try:
        return True, json.loads(raw, object_pairs_hook=_pairs, parse_constant=_no_constant, parse_int=str)
    except json.JSONDecodeError:
        return False, None


def strict_json_typed(raw, prefix):
    """v003 D-05: (obj, text, None) when raw is UTF-8 text that parses by r2's strict JSON (native integers); otherwise (None, None,
    (code, detail)) with a typed code per defect class: <prefix>_JSON_ENCODING (not UTF-8), _JSON_DUPLICATE_KEY, _JSON_NON_FINITE_CONSTANT,
    _JSON_INTEGER_TOO_LONG (Python's 4,300-digit int limit), _JSON_SYNTAX (a JSON syntax error: there is no text fallback),
    _JSON_VALUE_ERROR (any other ValueError) or _JSON_DEFECT (any other exception)."""
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError as e:
        return None, None, ('%s_JSON_ENCODING' % prefix, 'not UTF-8 text: %s' % str(e)[:200])
    try:
        return strict_json_bytes(text), text, None
    except DuplicateKey as e:
        return None, None, ('%s_JSON_DUPLICATE_KEY' % prefix, str(e)[:200])
    except json.JSONDecodeError as e:
        return None, None, ('%s_JSON_SYNTAX' % prefix, str(e)[:200])
    except ValueError as e:
        m = str(e)
        if m.startswith('NON_FINITE_JSON_CONSTANT'):
            return None, None, ('%s_JSON_NON_FINITE_CONSTANT' % prefix, m[:200])
        if 'integer string conversion' in m:
            return None, None, ('%s_JSON_INTEGER_TOO_LONG' % prefix, m[:200])
        return None, None, ('%s_JSON_VALUE_ERROR' % prefix, m[:200])
    except Exception as e:
        return None, None, ('%s_JSON_DEFECT' % prefix, '%s: %s' % (type(e).__name__, str(e)[:200]))


def covered_later_flag(argv):
    """v003 D-05: True when argv gives the removed --covered-later flag (any value, the '=' form included)."""
    return any(isinstance(a, str) and a.split('=', 1)[0] == '--covered-later' for a in argv)


def covered_later_refusal(name):
    return {'check': name, 'verdict': 'REFUSE', 'failures': [{'code': 'COVERED_LATER_BARE_NAMES_REFUSED', 'detail': COVERED_LATER_REMOVED}],
            'notes': [], 'pins_verified': {}}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def is_pin(ref):
    """{path, sha256} exactly, an absolute path string and a 64-hex sha (no file access)"""
    return (isinstance(ref, dict) and set(ref) == {'path', 'sha256'} and isinstance(ref['path'], str) and isinstance(ref['sha256'], str)
            and Path(ref['path']).is_absolute() and bool(HEX64.fullmatch(ref['sha256'])))


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


def guarded_run(name, fn, *a, **k):
    """D-07: run a check; any unexpected exception becomes a REFUSE with code INTERNAL_EXCEPTION:<type> (fail closed, exit 2, never a
    traceback). A check's own refusals are returned normally."""
    try:
        return fn(*a, **k)
    except (Exception, SystemExit) as e:          # a SystemExit raised by a library call (e.g. a compare Refused) is a code too
        return {'check': name, 'verdict': 'REFUSE', 'failures': [{'code': 'INTERNAL_EXCEPTION:%s' % type(e).__name__, 'detail': str(e)[:300]}],
                'notes': [], 'pins_verified': {}}


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


def pending_paths(obj, path='$'):
    """every JSON path whose string value carries PENDING (D-09 reporting)"""
    out = []
    if isinstance(obj, str):
        if PENDING_RX.search(obj):
            out.append(path)
    elif isinstance(obj, dict):
        for k, v in obj.items():
            out += pending_paths(v, '%s.%s' % (path, k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out += pending_paths(v, '%s[%d]' % (path, i))
    return out


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


def build_allowlist(text):
    """The '## Supported runtime entry allowlist' section of a BUILD record: [(sha, path)] in file order (a repeated path is kept, so
    the caller can refuse it, A71), or None when the section is absent."""
    if BUILD_HEADER + '\n' not in text:
        return None
    sec = text.split(BUILD_HEADER + '\n', 1)[1].split('\n## ', 1)[0]
    return re.findall(r'^([0-9a-f]{64})  (/\S+\.py)$', sec, re.M)


def build_allowlist_codes(chk, text, tag='BUILD'):
    """A99.1 / V6-S3: exactly 15 supported entries, each path once, each a .py whose bytes hash to its listed sha; returns {path: sha}
    (only when every rule holds) or None."""
    entries = build_allowlist(text)
    if entries is None:
        chk.fail('%s_ALLOWLIST_SECTION' % tag, BUILD_HEADER)
        return None
    ok = True
    seen = {}
    for i, (h, p) in enumerate(entries):
        if p in seen:
            chk.fail('%s_ALLOWLIST_DUPLICATE_PATH' % tag, 'entries[%d] and entries[%d] name one path (A71)' % (seen[p], i))
            ok = False
        else:
            seen[p] = i
    if len(entries) != BUILD_ALLOWLIST_COUNT:
        chk.fail('%s_ALLOWLIST_COUNT_NOT_15' % tag, '%d entries; the launch-packet BUILD of record has %d (A99.1 V6-S3)' % (len(entries), BUILD_ALLOWLIST_COUNT))
        ok = False
    for h, p in entries:
        if not Path(p).is_file():
            chk.fail('%s_ALLOWLIST_SOURCE_MISSING' % tag, p)
            ok = False
        elif sha(p) != h:
            chk.fail('%s_ALLOWLIST_SOURCE_BYTES' % tag, '%s does not hash to its listed sha' % p)
            ok = False
    return {p: h for h, p in entries} if ok else None


_COMPARE_CACHE = {}


def load_reviewed_compare(path, sha256):
    """The reviewed compare as a module, compiled from the very bytes whose sha256 was verified (no second read); cached per sha.
    Import has no side effect beyond definitions (r12: constant assignments, defs and `import numpy`, read by AST)."""
    key = (str(path), sha256)
    if key in _COMPARE_CACHE:
        return _COMPARE_CACHE[key]
    raw = Path(path).read_bytes()
    if sha_bytes(raw) != sha256:
        raise ValueError('REVIEWED_COMPARE_BYTES_NOT_THE_SLOT')
    name = 'seal_tools_c4v003_reviewed_compare_%s' % sha256[:16]
    mod = types.ModuleType(name)
    mod.__file__ = str(path)
    exec(compile(raw, str(path), 'exec'), mod.__dict__)
    _COMPARE_CACHE[key] = mod
    return mod


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

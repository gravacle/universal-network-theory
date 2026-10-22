"""pinned_input_envelope_c2v001.py -- the root integrity envelope (V006 A226 item 3), single-read (A226 item 1, E_A220_1).

At the start and at the end of each launch phase (the S0 seed, HEADLINE11, W1, each wave, the Phase-1 NGC set, S1 and the
Phase-1 freeze) root hashes every pinned input that the phase's configs, plans, C1, registry and V006 pins name, and compares
the two manifests.  Any changed byte invalidates that phase's runs (A226 item 3, pre-registered).  This tool is mechanical and
read-only toward every pinned input: it opens inputs read-only, writes only its own outputs (exclusive create), uses no
network and launches nothing.

SINGLE READ.  Every file is opened at most ONCE per subcommand (read_once): one os.open, one pass of os.read to EOF on that
descriptor, fstat on the same descriptor before and after.  The sha256 recorded, the byte count recorded and (for the
documents collect parses) the object parsed all come from the chunks that one pass returned; no path is stat'ed for its size
or hashed or parsed through a second open.  Within one subcommand a file reached through several pins or several spellings is
read once (keyed by realpath) and its one result is reused.

  collect   Sources (root-supplied):
              --doc PATH            a JSON document (run config, plan, admission, C1, registry, launch registry entry, spec);
                                    walked for pins, and itself entered in the pin set at the sha of the bytes read now;
              --doc-pin SHA PATH    the same, but its bytes must hash to SHA (else refused, exit 2);
              --walk-only PATH      walked for pins, not itself entered (e.g. a document that is still being appended to);
              --pin-list PATH       an explicit pin list: a JSON list of {path, sha256} pins or {"pins": [...]}; every item
                                    must be a pin (else refused);
              --v006 PATH           V006: its whole-line pin lines in the kit's PIN_RE form (s0_prelaunch_record_c2v001 L43,
                                    a10965b7) plus TOOL_PIN (V006 A223, P-112 launch (D8), L3587-3588):
                                      ^(GATE_PIN|HANDOFF_PIN|SPEC_PIN|WATCH_PIN|TOOL_PIN|ROOT_LISTED_ROW_GATE) NAME SHA /PATH$
                                    Lines are split on '\\n' and trailing '\\r' removed (as the kit).  A line that starts
                                    with one of those keywords (or ROOT_LISTED_ROW_GATES) and is not a pin line or exactly
                                    'ROOT_LISTED_ROW_GATES NONE' refuses (the kit refuses the same file).  Text that mentions
                                    a keyword inside a line, or an indented line, is not a pin line.  V006 itself is not
                                    entered in the pin set (it grows during every phase).
            A PIN is any JSON object that has (at least) the keys 'path' and 'sha256' where path is a string and sha256 is a
            64-hex string (upper case is accepted and recorded lower case, with sha256_as_written in the source).  Pin
            objects are walked inside too.  An object with both keys that fails the test is a NEAR PIN: reported, never
            hashed.  A pin whose path is not absolute (or holds NUL) is UNRESOLVED: collect refuses unless
            --allow-unresolved, which records it (never hashed; compare reports the count).
            FOLLOWING: every pinned file whose name ends .json or .jsonl (case-insensitive) is read once, hashed, and only if
            that buffer's sha256 equals the pin is the SAME buffer parsed and walked; breadth-first, root documents are depth
            0, a pin found in a depth-d document has depth d+1, and a pinned document is followed when its depth is at most
            --max-depth (default 8).  Each (realpath, sha256) is parsed at most once (cycles end).  Not followed (recorded in
            the pin's 'follow'): hash_only (content guard, below), not_json_suffix, depth_limited, too_large (over
            --max-follow-bytes, default 64 MiB, by fstat before any read), parse_failed, pin_mismatch_not_parsed, missing,
            unreadable, not_regular, symlink_at_open, changed_during_read.  Every pin is in the set whether or not it was
            followed.  Output: the PIN SET (deduplicated on (path, sha256), every source kept), exclusive create.
  snapshot  Reads the pin set once (embedded body_sha256 checked; --pins-sha256 checks the file bytes), resolves every pin
            path (lstat/readlink only: realpath, final_symlink, readlink), then reads every distinct realpath ONCE and records
            per file: status, sha256_from_bytes, bytes_read, size, mtime_ns, ctime_ns, ino, dev, mode, nlink, content_guard,
            hash_only; and per pin: status (match / mismatch / the file's status), match, the resolution and hash_only.
            Output: the MANIFEST (exclusive create) with its own body_sha256, plus <out>.sha256 (the file's sha256), and the
            file sha on stdout.  Exit 0 when every pin matches, 3 when any pin is missing, mismatched or unreadable (the
            manifest is still written: it is the evidence).
  compare   Reads a start and an end manifest once each (embedded body_sha256 checked; --start-sha256/--end-sha256 check the
            file bytes); refuses unless they are labelled start and end, have the same phase and the same pin set, and end
            was taken no earlier than start.  INVALIDATE (exit 3) with a list when any pin is not matched at start or at end,
            any file's sha256 changed, any file's size, mtime_ns or ino changed (the file was rewritten or replaced, even
            with the same bytes now), any pin's resolution changed (realpath, final_symlink, readlink), or the file set
            differs.  mode, nlink, ctime_ns and dev changes are NOTES (they cannot change bytes; dev changes on a remount).
            Otherwise OK (exit 0).  --out writes the report by exclusive create.

CONTENT GUARD (hash_only).  The content of a file whose path or realpath has a component containing 'ngc3198' (any case; the
house rule, P-112 path_rules), a component containing 'v007_postseal_records', or whose basename is result.json, finish.json
or progress.jsonl is NEVER parsed or followed by any subcommand.  Pinned guarded files ARE hashed by snapshot (bytes only:
'hash_only': true).  collect never opens them.  A root document (--doc, --doc-pin, --walk-only, --pin-list), a pin set, a
manifest or an output path that is guarded is refused (exit 2) without being opened.  Named exception, as P-112 read_v006:
the --v006 file's BASENAME may contain NGC3198 (its directories may not, and it must end .md); it is parsed only for pin lines.
NEVER OPENED: any path (as written or resolved) with a '.codex' component -- not even to hash it; a pin there refuses.

SYMLINKS (recorded).  A pinned path may be or pass through a symlink: snapshot records realpath, final_symlink and readlink
and reads the realpath with O_NOFOLLOW (a final-component symlink swapped in after resolution is 'symlink_at_open', never
followed); compare INVALIDATEs when any of the three changes (a retargeted symlink), even when the bytes are the same.
Non-regular files (directory, FIFO, device) are opened O_NONBLOCK, recorded 'not_regular' and never read.

Exit codes: 0 OK; 3 INVALIDATE (collect: written, but a followed pin was missing or mismatched; snapshot: written, some pin
not matched; compare: INVALIDATE); 2 refused input (nothing written).  Any other code is a tool error.
usage:
  PY -I -B pinned_input_envelope_c2v001.py collect --phase W1 --doc CFG.json --doc-pin SHA C1.json --v006 V006.md \\
      [--walk-only REG.jsonl] [--pin-list PINS.json] [--max-depth 8] [--max-follow-bytes N] [--allow-unresolved] \\
      --out ENVELOPE_W1_PINSET.json
  PY -I -B pinned_input_envelope_c2v001.py snapshot --pins ENVELOPE_W1_PINSET.json [--pins-sha256 H] --label start \\
      --out ENVELOPE_W1_START.json
  PY -I -B pinned_input_envelope_c2v001.py compare --start ENVELOPE_W1_START.json --end ENVELOPE_W1_END.json \\
      [--start-sha256 H] [--end-sha256 H] [--out ENVELOPE_W1_COMPARE.json]
"""
import argparse
import errno
import hashlib
import json
import os
import re
import stat
import sys
import time

TOOL = 'pinned_input_envelope_c2v001'
SCHEMA_PINSET = 'UNT_PINNED_INPUT_ENVELOPE_PINSET_C2V001'
SCHEMA_MANIFEST = 'UNT_PINNED_INPUT_ENVELOPE_MANIFEST_C2V001'
SCHEMA_COMPARE = 'UNT_PINNED_INPUT_ENVELOPE_COMPARE_C2V001'
EXIT_OK, EXIT_REFUSED, EXIT_INVALIDATE = 0, 2, 3

V006_KINDS = ('GATE_PIN', 'HANDOFF_PIN', 'SPEC_PIN', 'WATCH_PIN', 'TOOL_PIN', 'ROOT_LISTED_ROW_GATE')
KEYWORD_RE = re.compile(r'^(GATE_PIN|HANDOFF_PIN|SPEC_PIN|WATCH_PIN|TOOL_PIN|ROOT_LISTED_ROW_GATES|ROOT_LISTED_ROW_GATE)(?=\s|$)')
PIN_RE = re.compile(r'^(GATE_PIN|HANDOFF_PIN|SPEC_PIN|WATCH_PIN|TOOL_PIN|ROOT_LISTED_ROW_GATE) ([A-Z0-9][A-Z0-9_]*) ([0-9a-f]{64}) (/.*\S)$')
NONE_LINE = 'ROOT_LISTED_ROW_GATES NONE'
ENTRY_RE = re.compile(r'^## (A[0-9]+)(?=[\s:.(]|$)')
HEX64 = re.compile(r'[0-9a-f]{64}')
HEX64_ANYCASE = re.compile(r'[0-9a-fA-F]{64}')
PHASE_RE = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,63}')
LABELS = ('start', 'end')
CHUNK = 8 << 20
DEFAULT_MAX_DEPTH = 8
DEFAULT_MAX_FOLLOW_BYTES = 64 << 20
SIGNED_MAX_BYTES = 1 << 30
FOLLOW_SUFFIXES = ('.json', '.jsonl')
RUN_OUTPUT_BASENAMES = ('result.json', 'finish.json', 'progress.jsonl')
INVALIDATING_FILE_FIELDS = ('size', 'mtime_ns', 'ino')
NOTE_FILE_FIELDS = ('mode', 'nlink', 'ctime_ns', 'dev')
RESOLUTION_FIELDS = ('realpath', 'final_symlink', 'readlink')
OPEN_FLAGS = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | getattr(os, 'O_CLOEXEC', 0)
NOT_OK_PROBLEM = ('missing', 'unreadable', 'not_regular', 'symlink_at_open', 'changed_during_read')


class Refusal(Exception):
    pass


def need(ok, why):
    if not ok:
        raise Refusal(why)


def canon(o):
    return json.dumps(o, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False)


def sha_b(b):
    return hashlib.sha256(b).hexdigest()


def utc_now():
    ns = time.time_ns()
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(ns // 1_000_000_000)), ns


# ------------------------------------------------------------------------------------------------ guards
def _components(path):
    return [c for c in path.split('/') if c]


def never_open_reason(path):
    """'CODEX_TREE' when the path as written or resolved has a '.codex' component (never opened, not even to hash)."""
    if '.codex' in _components(path):
        return 'CODEX_TREE'
    if '.codex' in _components(os.path.realpath(path)):
        return 'CODEX_TREE'
    return None


def content_guard(path):
    """Why this file's CONTENT is never parsed or followed (it may still be hashed: hash_only), or None."""
    for p in (path, os.path.realpath(path)):
        comps = [c.lower() for c in _components(p)]
        if any('ngc3198' in c for c in comps):
            return 'NGC3198_PATH'
        if any('v007_postseal_records' in c for c in comps):
            return 'V007_POSTSEAL_RECORDS'
        if comps and comps[-1] in RUN_OUTPUT_BASENAMES:
            return 'RUN_OUTPUT_FILE'
    return None


def pin_path_problem(p):
    if not isinstance(p, str) or not p:
        return 'PATH_NOT_A_STRING'
    if '\x00' in p:
        return 'PATH_HAS_NUL'
    if not p.startswith('/'):
        return 'PATH_NOT_ABSOLUTE'
    return None


# ------------------------------------------------------------------------------------------------ the one read
def _meta(st):
    return {'size': st.st_size, 'mtime_ns': st.st_mtime_ns, 'ctime_ns': st.st_ctime_ns, 'ino': st.st_ino,
            'dev': st.st_dev, 'mode': st.st_mode, 'nlink': st.st_nlink}


def read_once(path, keep, max_bytes=None):
    """Open `path` ONCE and read it to EOF from that one descriptor -> (rec, buf).
    rec['sha256_from_bytes'] and rec['bytes_read'] are computed from exactly the chunks os.read returned, and buf (keep=True)
    is those same chunks joined: the sha a caller records, the length it records and the buffer it parses are one read.
    fstat on the same descriptor before and after: any difference, or a byte count other than the size, is
    'changed_during_read'.  O_NOFOLLOW: a final-component symlink is never followed ('symlink_at_open').  O_NONBLOCK: a FIFO
    cannot block the open.  A non-regular file is 'not_regular' and is not read; max_bytes: a larger file is 'too_large' and
    is not read."""
    try:
        fd = os.open(path, OPEN_FLAGS)
    except (OSError, ValueError) as e:
        en = getattr(e, 'errno', None)
        st = {errno.ENOENT: 'missing', errno.ENOTDIR: 'missing', errno.ELOOP: 'symlink_at_open'}.get(en, 'unreadable')
        return {'status': st, 'errno': errno.errorcode.get(en, str(en))}, None
    try:
        st0 = os.fstat(fd)
        meta = _meta(st0)
        if not stat.S_ISREG(st0.st_mode):
            return dict(meta, status='not_regular'), None
        if max_bytes is not None and st0.st_size > max_bytes:
            return dict(meta, status='too_large'), None
        h = hashlib.sha256()
        n = 0
        chunks = []
        while True:
            b = os.read(fd, CHUNK)
            if not b:
                break
            h.update(b)
            n += len(b)
            if keep:
                chunks.append(b)
        st1 = os.fstat(fd)
    except OSError as e:
        return {'status': 'unreadable', 'errno': errno.errorcode.get(e.errno, str(e.errno))}, None
    finally:
        os.close(fd)
    stable = n == st0.st_size == st1.st_size and _meta(st1) == meta
    rec = dict(meta, status='ok' if stable else 'changed_during_read', sha256_from_bytes=h.hexdigest(), bytes_read=n)
    return rec, (b''.join(chunks) if keep else None)


class OneRead:
    """At most one open per file per subcommand: results are kept by realpath and reused.  The guards are applied again
    to the realpath that is about to be opened (guard=False only for the --v006 named exception)."""

    def __init__(self, max_bytes):
        self.max_bytes = max_bytes
        self.seen = {}

    def get(self, path, guard=True):
        rp = os.path.realpath(path)
        need(never_open_reason(rp) is None, 'NEVER_OPEN %s' % rp)
        if guard and content_guard(rp) is not None:
            return rp, {'status': 'hash_only'}, None
        if rp not in self.seen:
            self.seen[rp] = read_once(rp, keep=True, max_bytes=self.max_bytes)
        rec, buf = self.seen[rp]
        return rp, rec, buf


def resolution(path):
    """How a pinned path resolves now: lstat/readlink only, no open."""
    rp = os.path.realpath(path)
    link = None
    try:
        if os.path.islink(path):
            link = os.readlink(path)
    except OSError:
        link = None
    return {'realpath': rp, 'final_symlink': link is not None, 'readlink': link, 'resolved_differs': rp != path}


# ------------------------------------------------------------------------------------------------ parsing (same buffer)
def _esc(k):
    return str(k).replace('~', '~0').replace('/', '~1')


def walk_pins(obj):
    """Every {path, sha256} pin in a parsed JSON value -> (pins [(pointer, path, sha_lower, sha_as_written)], near [..])."""
    pins, near = [], []
    stack = [('', obj)]
    while stack:
        ptr, o = stack.pop()
        if isinstance(o, dict):
            if 'path' in o and 'sha256' in o:
                p, s = o['path'], o['sha256']
                if isinstance(p, str) and isinstance(s, str) and HEX64_ANYCASE.fullmatch(s):
                    pins.append((ptr, p, s.lower(), s))
                else:
                    near.append({'pointer': ptr, 'why': 'path_not_a_string' if not isinstance(p, str) else 'sha256_not_64_hex'})
            for k in sorted(o, reverse=True):
                stack.append((ptr + '/' + _esc(k), o[k]))
        elif isinstance(o, list):
            for i in range(len(o) - 1, -1, -1):
                stack.append(('%s/%d' % (ptr, i), o[i]))
    return pins, near


def parse_json_buffer(path, buf):
    """Parse the buffer that was hashed (never a second read).  .jsonl: one JSON value per non-blank line -> list."""
    text = buf.decode('utf-8')
    if path.lower().endswith('.jsonl'):
        return [json.loads(line) for line in text.split('\n') if line.strip()]
    return json.loads(text)


def parse_v006_lines(raw):
    """V006 bytes -> (pins [{kind, name, sha256, path, entry, line}], malformed line numbers)."""
    text = raw.decode('utf-8')
    pins, malformed, entry = [], [], None
    for i, line in enumerate(text.split('\n'), 1):
        line = line.rstrip('\r')
        m = ENTRY_RE.match(line)
        if m:
            entry = m.group(1)
            continue
        if not KEYWORD_RE.match(line):
            continue
        if line == NONE_LINE:
            continue
        p = PIN_RE.match(line)
        if p is None:
            malformed.append(i)
            continue
        kind, name, sha, path = p.groups()
        pins.append({'kind': kind, 'name': name, 'sha256': sha, 'path': path, 'entry': entry, 'line': i})
    return pins, malformed


# ------------------------------------------------------------------------------------------------ outputs
def check_out(out):
    need(isinstance(out, str) and out and '\x00' not in out, 'BAD_OUT_PATH')
    out = os.path.abspath(out)
    need(never_open_reason(out) is None, 'OUT_IN_FORBIDDEN_TREE %s' % out)
    need(content_guard(out) is None, 'OUT_PATH_CONTENT_GUARDED %s' % out)
    need(not os.path.lexists(out), 'OUTPUT_EXISTS %s' % out)
    need(not os.path.lexists(out + '.sha256'), 'OUTPUT_EXISTS %s.sha256' % out)
    need(os.path.isdir(os.path.dirname(out)), 'OUT_DIR_MISSING %s' % os.path.dirname(out))
    return out


def _fsync_dir(d):
    fd = os.open(d, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def write_signed(out, obj):
    """Exclusive create of obj with its own body_sha256 (sha256 of the canonical JSON of everything else), then
    <out>.sha256 = the file's sha256.  -> (file_sha256, body_sha256)."""
    body = {k: v for k, v in obj.items() if k != 'body_sha256'}
    signed = dict(body, body_sha256=sha_b(canon(body).encode('ascii')))
    data = (json.dumps(signed, indent=1, sort_keys=True, ensure_ascii=True, allow_nan=False) + '\n').encode('ascii')
    try:
        f = open(out, 'xb')
    except FileExistsError:
        raise Refusal('OUTPUT_EXISTS %s' % out) from None
    with f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    fsha = sha_b(data)
    with open(out + '.sha256', 'x', encoding='ascii') as f:
        f.write('%s  %s\n' % (fsha, os.path.basename(out)))
        f.flush()
        os.fsync(f.fileno())
    _fsync_dir(os.path.dirname(out))
    return fsha, signed['body_sha256']


def load_signed(path, schema, expected_sha=None):
    """Read a pin set or manifest ONCE; hash that buffer; parse that buffer; check the embedded body_sha256."""
    need(isinstance(path, str) and path and '\x00' not in path, 'BAD_INPUT_PATH')
    path = os.path.abspath(path)
    need(never_open_reason(path) is None, 'INPUT_IN_FORBIDDEN_TREE %s' % path)
    need(content_guard(path) is None, 'INPUT_CONTENT_GUARDED %s %s' % (content_guard(path), path))
    rec, buf = read_once(os.path.realpath(path), keep=True, max_bytes=SIGNED_MAX_BYTES)
    need(rec['status'] == 'ok', 'INPUT_UNREADABLE %s (%s)' % (path, rec['status']))
    if expected_sha is not None:
        need(isinstance(expected_sha, str) and HEX64.fullmatch(expected_sha) is not None, 'BAD_EXPECTED_SHA256')
        need(rec['sha256_from_bytes'] == expected_sha, 'INPUT_FILE_SHA_MISMATCH %s: expected %s, bytes %s'
             % (path, expected_sha, rec['sha256_from_bytes']))
    try:
        obj = json.loads(buf.decode('utf-8'))
    except (UnicodeDecodeError, ValueError, RecursionError):
        raise Refusal('INPUT_NOT_JSON %s' % path) from None
    need(isinstance(obj, dict) and obj.get('schema') == schema, 'INPUT_WRONG_SCHEMA %s (want %s)' % (path, schema))
    body = {k: v for k, v in obj.items() if k != 'body_sha256'}
    need(obj.get('body_sha256') == sha_b(canon(body).encode('ascii')), 'INPUT_BODY_SHA_MISMATCH %s' % path)
    return obj, rec['sha256_from_bytes'], path


def _summary(d):
    print(json.dumps(d, sort_keys=True))


# ------------------------------------------------------------------------------------------------ collect
def collect(phase, docs, doc_pins, walk_only, pin_lists, v006, max_depth, max_follow_bytes, allow_unresolved, out):
    need(isinstance(phase, str) and PHASE_RE.fullmatch(phase) is not None, 'BAD_PHASE %r' % (phase,))
    need(isinstance(max_depth, int) and max_depth >= 0, 'BAD_MAX_DEPTH')
    need(isinstance(max_follow_bytes, int) and max_follow_bytes > 0, 'BAD_MAX_FOLLOW_BYTES')
    need(bool(docs or doc_pins or walk_only or pin_lists or v006), 'NO_SOURCES')
    out = check_out(out)
    reader = OneRead(max_follow_bytes)
    pins, queue, unresolved, near, roots, problems, warnings = {}, [], [], [], [], [], []
    followed = set()

    def add_pin(path, sha, depth, source, sha_written=None):
        prob = pin_path_problem(path)
        if prob:
            unresolved.append({'path': path, 'sha256': sha, 'why': prob, 'source': source})
            return
        nr = never_open_reason(path)
        need(nr is None, 'PIN_IN_FORBIDDEN_TREE %s %s (source %s)' % (nr, path, canon(source)))
        key = (path, sha)
        if key not in pins:
            pins[key] = {'path': path, 'sha256': sha, 'depth': depth, 'sources': [], 'follow': None,
                         'content_guard': content_guard(path)}
            queue.append(key)
        elif depth < pins[key]['depth']:
            pins[key]['depth'] = depth
        if sha_written is not None and sha_written != sha:
            source = dict(source, sha256_as_written=sha_written)
        pins[key]['sources'].append(source)

    def open_root(path, role):
        need(isinstance(path, str) and path.startswith('/') and '\x00' not in path, 'ROOT_PATH_NOT_ABSOLUTE %r' % (path,))
        nr = never_open_reason(path)
        need(nr is None, 'ROOT_IN_FORBIDDEN_TREE %s %s' % (nr, path))
        if role == 'v006':   # named exception (as P-112 read_v006): only the basename may name NGC3198
            need(path.lower().endswith('.md') and os.path.realpath(path).lower().endswith('.md'), 'V006_NOT_MD %s' % path)
            need(content_guard(os.path.dirname(path)) is None and
                 content_guard(os.path.dirname(os.path.realpath(path))) is None, 'V006_DIRECTORY_CONTENT_GUARDED %s' % path)
            need(os.path.basename(path).lower() not in RUN_OUTPUT_BASENAMES, 'V006_PATH_REFUSED %s' % path)
        else:
            g = content_guard(path)
            need(g is None, 'ROOT_DOC_CONTENT_GUARDED %s %s' % (g, path))
        rp, rec, buf = reader.get(path, guard=role != 'v006')
        need(rec['status'] == 'ok', 'ROOT_DOC_UNREADABLE %s (%s)' % (path, rec['status']))
        return rp, rec, buf

    def walk_root(path, role, rec, rp, buf):
        try:
            obj = parse_json_buffer(path, buf)
        except (UnicodeDecodeError, ValueError, RecursionError):
            raise Refusal('ROOT_DOC_NOT_JSON %s' % path) from None
        found, nr = walk_pins(obj)
        if role in ('doc', 'doc_pin'):
            add_pin(path, rec['sha256_from_bytes'], 0, {'root': role})
            pins[(path, rec['sha256_from_bytes'])]['follow'] = 'root_document'
            followed.add((rp, rec['sha256_from_bytes']))
        for ptr, p, s, sw in found:
            add_pin(p, s, 1, {'doc': path, 'pointer': ptr}, sw)
        for x in nr:
            near.append(dict(x, doc=path))
        roots.append({'role': role, 'path': path, 'realpath': rp, 'sha256_from_bytes': rec['sha256_from_bytes'],
                      'bytes': rec['bytes_read'], 'entered_in_pin_set': role in ('doc', 'doc_pin'), 'n_pins_found': len(found)})

    for path in docs:
        rp, rec, buf = open_root(path, 'doc')
        walk_root(path, 'doc', rec, rp, buf)
    for sha, path in doc_pins:
        need(isinstance(sha, str) and HEX64.fullmatch(sha) is not None, 'DOC_PIN_BAD_SHA256 %r' % (sha,))
        rp, rec, buf = open_root(path, 'doc_pin')
        need(rec['sha256_from_bytes'] == sha, 'DOC_PIN_MISMATCH %s: pin %s, bytes %s' % (path, sha, rec['sha256_from_bytes']))
        walk_root(path, 'doc_pin', rec, rp, buf)
    for path in walk_only:
        rp, rec, buf = open_root(path, 'walk_only')
        walk_root(path, 'walk_only', rec, rp, buf)
    for path in pin_lists:
        rp, rec, buf = open_root(path, 'pin_list')
        try:
            obj = parse_json_buffer(path, buf)
        except (UnicodeDecodeError, ValueError, RecursionError):
            raise Refusal('PIN_LIST_NOT_JSON %s' % path) from None
        items = obj if isinstance(obj, list) else (obj.get('pins') if isinstance(obj, dict) else None)
        need(isinstance(items, list), 'PIN_LIST_SHAPE %s (a list of pins or {"pins": [...]})' % path)
        for i, it in enumerate(items):
            need(isinstance(it, dict) and isinstance(it.get('path'), str) and isinstance(it.get('sha256'), str)
                 and HEX64_ANYCASE.fullmatch(it['sha256']) is not None, 'PIN_LIST_ITEM_NOT_A_PIN %s [%d]' % (path, i))
            add_pin(it['path'], it['sha256'].lower(), 1, {'pin_list': path, 'index': i}, it['sha256'])
        roots.append({'role': 'pin_list', 'path': path, 'realpath': rp, 'sha256_from_bytes': rec['sha256_from_bytes'],
                      'bytes': rec['bytes_read'], 'entered_in_pin_set': False, 'n_pins_found': len(items)})
    v006_rec = None
    if v006:
        rp, rec, buf = open_root(v006, 'v006')
        try:
            vp, malformed = parse_v006_lines(buf)
        except UnicodeDecodeError:
            raise Refusal('V006_NOT_UTF8 %s' % v006) from None
        need(not malformed, 'V006_MALFORMED_PIN_LINES %s lines %s' % (v006, malformed[:20]))
        for x in vp:
            add_pin(x['path'], x['sha256'], 1, {'v006': v006, 'kind': x['kind'], 'name': x['name'], 'line': x['line'],
                                                'entry': x['entry']})
        kinds = {}
        for x in vp:
            kinds[x['kind']] = kinds.get(x['kind'], 0) + 1
        v006_rec = {'path': v006, 'realpath': rp, 'sha256_from_bytes': rec['sha256_from_bytes'], 'bytes': rec['bytes_read'],
                    'n_pin_lines': len(vp), 'by_kind': kinds}
        roots.append({'role': 'v006', 'path': v006, 'realpath': rp, 'sha256_from_bytes': rec['sha256_from_bytes'],
                      'bytes': rec['bytes_read'], 'entered_in_pin_set': False, 'n_pins_found': len(vp)})

    # breadth-first following (depths are final when popped: the initial queue is ordered by depth)
    queue.sort(key=lambda k: pins[k]['depth'])
    i = 0
    while i < len(queue):
        key = queue[i]
        i += 1
        pin = pins[key]
        if pin['follow'] is not None:
            continue
        path, sha, depth = pin['path'], pin['sha256'], pin['depth']
        if pin['content_guard'] is not None:
            pin['follow'] = 'hash_only'
            continue
        if not path.lower().endswith(FOLLOW_SUFFIXES):
            pin['follow'] = 'not_json_suffix'
            continue
        if depth > max_depth:
            pin['follow'] = 'depth_limited'
            continue
        rp, rec, buf = reader.get(path)
        if rec['status'] != 'ok':
            pin['follow'] = rec['status']
            if rec['status'] in NOT_OK_PROBLEM:
                problems.append({'path': path, 'sha256': sha, 'status': rec['status']})
            continue
        if rec['sha256_from_bytes'] != sha:
            pin['follow'] = 'pin_mismatch_not_parsed'
            problems.append({'path': path, 'sha256': sha, 'status': 'pin_mismatch', 'sha256_from_bytes': rec['sha256_from_bytes']})
            continue
        if (rp, sha) in followed:
            pin['follow'] = 'followed'
            continue
        try:
            obj = parse_json_buffer(path, buf)
        except (UnicodeDecodeError, ValueError, RecursionError):
            pin['follow'] = 'parse_failed'
            warnings.append({'path': path, 'sha256': sha, 'warning': 'parse_failed'})
            continue
        followed.add((rp, sha))
        pin['follow'] = 'followed'
        found, nr = walk_pins(obj)
        for ptr, p, s, sw in found:
            add_pin(p, s, depth + 1, {'doc': path, 'pointer': ptr}, sw)
        for x in nr:
            near.append(dict(x, doc=path))

    need(len(pins) > 0, 'NO_PINS_FOUND')
    need(allow_unresolved or not unresolved, 'UNRESOLVED_PINS %d (first: %s); --allow-unresolved records them'
         % (len(unresolved), canon(unresolved[:3])))
    plist = [pins[k] for k in sorted(pins)]
    tally = {}
    for p in plist:
        tally[p['follow']] = tally.get(p['follow'], 0) + 1
    when, ns = utc_now()
    obj = {'schema': SCHEMA_PINSET, 'tool': TOOL, 'rule': 'V006 A226 item 3 (single-read: A226 item 1, E_A220_1)',
           'phase': phase, 'created_utc': when, 'created_epoch_ns': ns, 'max_depth': max_depth,
           'max_follow_bytes': max_follow_bytes, 'allow_unresolved': bool(allow_unresolved), 'roots': roots, 'v006': v006_rec,
           'pins': plist, 'unresolved_pins': unresolved, 'near_pins': near, 'collect_problems': problems,
           'warnings': warnings,
           'counts': {'n_pins': len(plist), 'n_paths': len({p['path'] for p in plist}), 'n_roots': len(roots),
                      'by_follow': tally, 'n_hash_only': sum(1 for p in plist if p['content_guard']),
                      'n_unresolved': len(unresolved), 'n_near_pins': len(near), 'n_problems': len(problems),
                      'n_files_read': len(reader.seen)}}
    fsha, bsha = write_signed(out, obj)
    rc = EXIT_INVALIDATE if problems else EXIT_OK
    _summary({'tool': TOOL, 'cmd': 'collect', 'phase': phase, 'out': out, 'file_sha256': fsha, 'body_sha256': bsha,
              'counts': obj['counts'], 'exit': rc})
    return rc


# ------------------------------------------------------------------------------------------------ snapshot
def snapshot(pins_path, pins_sha, label, out):
    need(label in LABELS, 'BAD_LABEL %r' % (label,))
    out = check_out(out)
    ps, ps_fsha, pins_path = load_signed(pins_path, SCHEMA_PINSET, pins_sha)
    plist = ps.get('pins')
    need(isinstance(plist, list), 'PIN_SET_SHAPE')
    keys = []
    for p in plist:
        need(isinstance(p, dict) and pin_path_problem(p.get('path')) is None and isinstance(p.get('sha256'), str)
             and HEX64.fullmatch(p['sha256']) is not None, 'PIN_SET_BAD_PIN %s' % canon(p)[:200])
        nr = never_open_reason(p['path'])
        need(nr is None, 'PIN_IN_FORBIDDEN_TREE %s %s' % (nr, p['path']))
        keys.append((p['path'], p['sha256']))
    need(len(keys) > 0, 'PIN_SET_EMPTY')
    need(len(set(keys)) == len(keys), 'PIN_SET_DUPLICATE_PIN')
    res = {k: resolution(k[0]) for k in keys}
    guards = {k: content_guard(k[0]) for k in keys}
    by_file = {}
    for k in keys:
        by_file.setdefault(res[k]['realpath'], []).append(k)
    files = {}
    for rp in sorted(by_file):
        need(never_open_reason(rp) is None, 'NEVER_OPEN %s' % rp)
        rec, _ = read_once(rp, keep=False)          # the one read of this file in this snapshot (bytes only)
        g = content_guard(rp) or next((guards[k] for k in by_file[rp] if guards[k]), None)
        files[rp] = dict(rec, file_key=rp, content_guard=g, hash_only=g is not None)
    entries = []
    for k in sorted(keys):
        f = files[res[k]['realpath']]
        if f['status'] == 'ok':
            status = 'match' if f['sha256_from_bytes'] == k[1] else 'mismatch'
        else:
            status = f['status']
        entries.append(dict(res[k], path=k[0], sha256=k[1], status=status, match=status == 'match',
                            sha256_from_bytes=f.get('sha256_from_bytes'), content_guard=guards[k],
                            hash_only=guards[k] is not None or f['hash_only']))
    tally = {}
    for e in entries:
        tally[e['status']] = tally.get(e['status'], 0) + 1
    n_match = tally.get('match', 0)
    when, ns = utc_now()
    unresolved = ps.get('unresolved_pins', [])
    man = {'schema': SCHEMA_MANIFEST, 'tool': TOOL, 'rule': 'V006 A226 item 3', 'phase': ps.get('phase'), 'label': label,
           'created_utc': when, 'created_epoch_ns': ns,
           'pin_set': {'path': pins_path, 'file_sha256': ps_fsha, 'body_sha256': ps.get('body_sha256')},
           'files': [files[rp] for rp in sorted(files)], 'pins': entries, 'unresolved_pins': unresolved,
           'all_match': n_match == len(entries),
           'counts': {'n_pins': len(entries), 'n_files': len(files), 'by_status': tally, 'n_match': n_match,
                      'n_not_matched': len(entries) - n_match,
                      'n_hash_only_pins': sum(1 for e in entries if e['hash_only']),
                      'n_final_symlink_pins': sum(1 for e in entries if e['final_symlink']),
                      'n_resolved_differs': sum(1 for e in entries if e['resolved_differs']),
                      'n_unresolved_not_checked': len(unresolved)}}
    fsha, bsha = write_signed(out, man)
    rc = EXIT_OK if man['all_match'] else EXIT_INVALIDATE
    _summary({'tool': TOOL, 'cmd': 'snapshot', 'phase': man['phase'], 'label': label, 'out': out, 'file_sha256': fsha,
              'body_sha256': bsha, 'all_match': man['all_match'], 'counts': man['counts'], 'exit': rc})
    return rc


# ------------------------------------------------------------------------------------------------ compare
def _index(man, what):
    pins = man.get('pins')
    files = man.get('files')
    need(isinstance(pins, list) and isinstance(files, list), 'MANIFEST_SHAPE %s' % what)
    pi, fi = {}, {}
    for p in pins:
        need(isinstance(p, dict) and isinstance(p.get('path'), str) and isinstance(p.get('sha256'), str), 'MANIFEST_PIN %s' % what)
        k = (p['path'], p['sha256'])
        need(k not in pi, 'MANIFEST_DUPLICATE_PIN %s' % what)
        pi[k] = p
    for f in files:
        need(isinstance(f, dict) and isinstance(f.get('file_key'), str), 'MANIFEST_FILE %s' % what)
        need(f['file_key'] not in fi, 'MANIFEST_DUPLICATE_FILE %s' % what)
        fi[f['file_key']] = f
    for p in pins:
        need(p.get('realpath') in fi, 'MANIFEST_INCONSISTENT %s: pin %s has no file entry' % (what, p['path']))
    return pi, fi


def compare(start, end, start_sha, end_sha, out):
    if out is not None:
        out = check_out(out)
    s, s_fsha, start = load_signed(start, SCHEMA_MANIFEST, start_sha)
    e, e_fsha, end = load_signed(end, SCHEMA_MANIFEST, end_sha)
    need(s.get('label') == 'start', 'START_NOT_LABELLED_START (%r)' % (s.get('label'),))
    need(e.get('label') == 'end', 'END_NOT_LABELLED_END (%r)' % (e.get('label'),))
    need(s.get('phase') == e.get('phase'), 'PHASE_DIFFERS %r %r' % (s.get('phase'), e.get('phase')))
    need(isinstance(s.get('pin_set'), dict) and isinstance(e.get('pin_set'), dict)
         and s['pin_set'].get('body_sha256') == e['pin_set'].get('body_sha256')
         and s['pin_set'].get('file_sha256') == e['pin_set'].get('file_sha256'), 'PIN_SET_DIFFERS')
    need(isinstance(s.get('created_epoch_ns'), int) and isinstance(e.get('created_epoch_ns'), int)
         and e['created_epoch_ns'] >= s['created_epoch_ns'], 'END_TAKEN_BEFORE_START')
    need(s.get('unresolved_pins') == e.get('unresolved_pins'), 'UNRESOLVED_LISTS_DIFFER')
    sp, sf = _index(s, 'start')
    ep, ef = _index(e, 'end')
    need(set(sp) == set(ep), 'PIN_LISTS_DIFFER')
    problems, notes = [], []
    for k in sorted(sp):
        a, b = sp[k], ep[k]
        for lab, x in (('START', a), ('END', b)):
            if x.get('status') != 'match' or x.get('match') is not True:
                problems.append({'kind': 'PIN_NOT_MATCHED_AT_' + lab, 'path': k[0], 'sha256': k[1], 'status': x.get('status'),
                                 'sha256_from_bytes': x.get('sha256_from_bytes')})
        for fld in RESOLUTION_FIELDS:
            if a.get(fld) != b.get(fld):
                problems.append({'kind': 'RESOLUTION_CHANGED', 'path': k[0], 'sha256': k[1], 'field': fld,
                                 'start': a.get(fld), 'end': b.get(fld)})
    for fk in sorted(set(sf) | set(ef)):
        a, b = sf.get(fk), ef.get(fk)
        if a is None or b is None:
            problems.append({'kind': 'FILE_SET_CHANGED', 'file_key': fk, 'in_start': a is not None, 'in_end': b is not None})
            continue
        if a.get('status') != b.get('status'):
            problems.append({'kind': 'FILE_STATUS_CHANGED', 'file_key': fk, 'start': a.get('status'), 'end': b.get('status')})
        if a.get('sha256_from_bytes') != b.get('sha256_from_bytes'):
            problems.append({'kind': 'SHA_CHANGED', 'file_key': fk, 'start': a.get('sha256_from_bytes'),
                             'end': b.get('sha256_from_bytes')})
        changed = {f: [a.get(f), b.get(f)] for f in INVALIDATING_FILE_FIELDS if a.get(f) != b.get(f)}
        if changed:
            problems.append({'kind': 'FILE_REWRITTEN', 'file_key': fk, 'fields': changed})
        noted = {f: [a.get(f), b.get(f)] for f in NOTE_FILE_FIELDS if a.get(f) != b.get(f)}
        if noted:
            notes.append({'kind': 'METADATA_CHANGED', 'file_key': fk, 'fields': noted})
    verdict = 'INVALIDATE' if problems else 'OK'
    when, ns = utc_now()
    rep = {'schema': SCHEMA_COMPARE, 'tool': TOOL, 'rule': 'V006 A226 item 3: any changed byte invalidates the phase',
           'phase': s.get('phase'), 'verdict': verdict, 'created_utc': when, 'created_epoch_ns': ns,
           'start': {'path': start, 'file_sha256': s_fsha, 'body_sha256': s.get('body_sha256'), 'created_utc': s.get('created_utc')},
           'end': {'path': end, 'file_sha256': e_fsha, 'body_sha256': e.get('body_sha256'), 'created_utc': e.get('created_utc')},
           'pin_set': s.get('pin_set'), 'n_pins': len(sp), 'n_files': len(set(sf) | set(ef)),
           'problems': problems, 'notes': notes, 'unresolved_pins_not_checked': len(s.get('unresolved_pins') or [])}
    summ = {'tool': TOOL, 'cmd': 'compare', 'phase': rep['phase'], 'verdict': verdict, 'n_problems': len(problems),
            'n_notes': len(notes), 'problem_kinds': sorted({p['kind'] for p in problems}),
            'unresolved_pins_not_checked': rep['unresolved_pins_not_checked']}
    if out is not None:
        fsha, bsha = write_signed(out, rep)
        summ.update(out=out, file_sha256=fsha, body_sha256=bsha)
    rc = EXIT_INVALIDATE if problems else EXIT_OK
    summ['exit'] = rc
    _summary(summ)
    return rc


# ------------------------------------------------------------------------------------------------ CLI
def build_parser():
    ap = argparse.ArgumentParser(prog=TOOL, description='Root integrity envelope (V006 A226 item 3); single-read.')
    sub = ap.add_subparsers(dest='cmd', required=True)
    c = sub.add_parser('collect')
    c.add_argument('--phase', required=True)
    c.add_argument('--doc', action='append', default=[])
    c.add_argument('--doc-pin', nargs=2, action='append', default=[], metavar=('SHA256', 'PATH'))
    c.add_argument('--walk-only', action='append', default=[])
    c.add_argument('--pin-list', action='append', default=[])
    c.add_argument('--v006')
    c.add_argument('--max-depth', type=int, default=DEFAULT_MAX_DEPTH)
    c.add_argument('--max-follow-bytes', type=int, default=DEFAULT_MAX_FOLLOW_BYTES)
    c.add_argument('--allow-unresolved', action='store_true')
    c.add_argument('--out', required=True)
    s = sub.add_parser('snapshot')
    s.add_argument('--pins', required=True)
    s.add_argument('--pins-sha256')
    s.add_argument('--label', required=True, choices=LABELS)
    s.add_argument('--out', required=True)
    m = sub.add_parser('compare')
    m.add_argument('--start', required=True)
    m.add_argument('--end', required=True)
    m.add_argument('--start-sha256')
    m.add_argument('--end-sha256')
    m.add_argument('--out')
    return ap


def main(argv=None):
    ap = build_parser()
    try:
        a = ap.parse_args(argv)
    except SystemExit as exc:
        return EXIT_OK if exc.code in (0, None) else EXIT_REFUSED
    try:
        if a.cmd == 'collect':
            return collect(a.phase, a.doc, [tuple(x) for x in a.doc_pin], a.walk_only, a.pin_list, a.v006, a.max_depth,
                           a.max_follow_bytes, a.allow_unresolved, a.out)
        if a.cmd == 'snapshot':
            return snapshot(a.pins, a.pins_sha256, a.label, a.out)
        return compare(a.start, a.end, a.start_sha256, a.end_sha256, a.out)
    except Refusal as r:
        print(json.dumps({'tool': TOOL, 'cmd': a.cmd, 'refused': str(r), 'exit': EXIT_REFUSED}, sort_keys=True), file=sys.stderr)
        return EXIT_REFUSED


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

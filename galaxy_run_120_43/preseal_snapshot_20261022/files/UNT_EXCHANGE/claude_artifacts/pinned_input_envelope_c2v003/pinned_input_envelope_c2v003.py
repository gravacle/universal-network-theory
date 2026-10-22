"""pinned_input_envelope_c2v003.py -- the root integrity envelope (V006 A226 item 3), single-read (A226 item 1, E_A220_1).
Successor of pinned_input_envelope_c2v002 (0fac239a), which was built on the A228 rulings D1-D7 (successor of c2v001,
ecfce024).  c2v003 changes only the read/caching path, for Codex1 0164 CX1-ENV-01 (below, IDENTITY); every other behaviour,
D1-D7 and errata E1 included, is c2v002's.

IDENTITY (c2v003, CX1-ENV-01; root choice: share one read keyed by (dev, ino)).  c2v002 kept the one-read cache by realpath,
so two hard-link paths to one regular file (two realpaths, one inode) were each opened and read: the same inode read twice
in one subcommand.  c2v003 keys the one read by the file's identity, the (dev, ino) that fstat reports on the O_NOFOLLOW
descriptor that was read.  Before a realpath is opened its own identity is taken with os.lstat (no open, no symlink
followed); when that is an inode already read in this subcommand, the realpath takes that read's result and is never opened.
Otherwise it is opened O_NOFOLLOW and fstat'ed; when the descriptor is an inode already read (the path changed between the
lstat and the open) it is closed before any os.read and takes that result too.  So each inode is content-read at most once
per subcommand.  A name takes the shared result only while its own stat (that lstat, or fstat on its descriptor) still
equals the read's size, mtime_ns, ctime_ns, ino, dev, mode and nlink; otherwise the inode changed after its one read (or
its number was reused) and the name is 'changed_during_read' (never a match), not read again.  Each alias keeps its own
path: snapshot writes one file entry per realpath (its own file_key, resolution and pins), and the entry of a realpath that
shares another's read carries alias_of (the realpath that was read; None on every other entry); collect lists such
realpaths in the pin set's 'read_aliases'.  A symlink spelling is unchanged from c2v002: it resolves to the same realpath,
so it is that file, not an alias.  Not changed: compare, the guards, D1-D7.

At the start and at the end of each launch phase (the S0 seed, HEADLINE11, W1, each wave, the Phase-1 NGC set, S1 and the
Phase-1 freeze) root hashes every pinned input that the phase's configs, plans, C1, registry and V006 pins name, and compares
the two manifests.  Any changed byte invalidates that phase's runs (A226 item 3, pre-registered).  This tool is mechanical and
read-only toward every pinned input: it opens inputs read-only, writes only its own outputs (exclusive create), uses no
network and launches nothing.

SINGLE READ.  Every file is opened at most ONCE per subcommand (read_once; the one exception is IDENTITY's race, where a
second name is opened and fstat'ed and closed before any os.read): one os.open, one pass of os.read to EOF on that
descriptor, fstat on the same descriptor before and after (and, in snapshot, the extended-attribute NAMES from the same
descriptor).  The sha256 recorded, the byte count recorded and (for the documents collect parses) the object parsed all come
from the chunks that one pass returned; no path is stat'ed for its size or hashed or parsed through a second open.  Within one
subcommand a file reached through several pins or several spellings is read once (keyed by its identity (dev, inode), so hard
links share the read: IDENTITY above) and its result reused.  os.stat (no open) is used only to learn the identity (dev,
inode) of an excluded file and of a pin path, for D1; os.lstat (no open) only to learn a realpath's identity before it is
opened, for IDENTITY.

c2v002 changes (V006 A228):
  D1  any pin whose realpath equals the --v006 file (or that is the same inode: a hard link) is an EXCLUDED GROWING FILE,
      however it is reached (a root document, a followed document, a pin list, V006's own pin lines): it is listed in the
      pin set's 'excluded' block with its sources and the reason, and is never snapshotted.
  D2  the default --max-depth is 0 (only the root documents are walked).  A depth above 0 needs --depth-reason TEXT, which
      is recorded.
  D3  --scope PATH POINTER: walk only the RFC 6901 JSON-pointer subtree of the root document given as PATH (exactly as
      spelled in --doc / --doc-pin / --walk-only), e.g. --scope C1.json /tail_readiness; pins outside it are not in the
      envelope.  --exclude PATH --reason TEXT (repeatable; each --reason belongs to the --exclude just before it): a pin
      whose realpath (or inode) is PATH is listed in 'excluded' with the reason, never snapshotted; recorded in the pin set,
      in every manifest and in the compare report.
  D4  snapshot records each file's extended-attribute names; compare: a ctime-only change (bytes, size, mtime and inode
      all equal) is a NOTE when the xattr-name set changed (explained metadata), otherwise INVALIDATE
      (CTIME_CHANGED_UNEXPLAINED).  A ctime change that comes with a byte or rewrite change is a note beside that
      change's own INVALIDATE.  mode and nlink changes are listed as notes but do not explain a ctime change.
  D5  a root document (--doc, --doc-pin, --walk-only, --pin-list, --v006) that fails to parse or is over --max-follow-bytes
      refuses; a followed document that fails to parse refuses too (and, a choice beyond the ruling, one over the cap).
  D6  compare requires --start-sha256 and --end-sha256.
  D7  a pin path (or a root, exclude, scope, output or input path) that does not encode as UTF-8 refuses (exit 2), even
      with --allow-unresolved.

  collect   Sources (root-supplied):
              --doc PATH            a JSON document (run config, plan, admission, C1, registry, launch registry entry, spec);
                                    walked for pins, and itself entered in the pin set at the sha of the bytes read now;
              --doc-pin SHA PATH    the same, but its bytes must hash to SHA (else refused, exit 2);
              --walk-only PATH      walked for pins, not itself entered (e.g. a document that is still being appended to);
              --pin-list PATH       an explicit pin list: a JSON list of {path, sha256} pins or {"pins": [...]}; every item
                                    must be a pin (else refused);
              --v006 PATH           V006: its whole-line pin lines in the kit's PIN_RE form (s0_prelaunch_record_c2v001 L43,
                                    a10965b7) plus TOOL_PIN (V006 A223):
                                      ^(GATE_PIN|HANDOFF_PIN|SPEC_PIN|WATCH_PIN|TOOL_PIN|ROOT_LISTED_ROW_GATE) NAME SHA /PATH$
                                    Lines are split on '\\n' and trailing '\\r' removed (as the kit).  A line that starts
                                    with one of those keywords (or ROOT_LISTED_ROW_GATES) and is not a pin line or exactly
                                    'ROOT_LISTED_ROW_GATES NONE' refuses.  Text that mentions a keyword inside a line, or an
                                    indented line, is not a pin line.  V006 itself is the D1 excluded growing file.
              --scope PATH POINTER, --exclude PATH --reason TEXT, --max-depth N (default 0), --depth-reason TEXT (D2, D3).
            A PIN is any JSON object that has (at least) the keys 'path' and 'sha256' where path is a string and sha256 is a
            64-hex string (upper case is accepted and recorded lower case, with sha256_as_written in the source).  Pin
            objects are walked inside too.  An object with both keys that fails the test is a NEAR PIN: reported, never
            hashed.  A pin whose path is not absolute (or holds NUL) is UNRESOLVED: collect refuses unless
            --allow-unresolved, which records it (never hashed; compare reports the count).
            FOLLOWING (only with --max-depth above 0): every pinned file whose name ends .json or .jsonl (case-insensitive)
            is read once, hashed, and only if that buffer's sha256 equals the pin is the SAME buffer parsed and walked;
            breadth-first, root documents are depth 0, a pin found in a depth-d document has depth d+1, and a pinned
            document is followed when its depth is at most --max-depth.  Each (realpath, sha256) is parsed at most once.
            Not followed (recorded in the pin's 'follow'): hash_only (content guard, below), not_json_suffix,
            depth_limited, pin_mismatch_not_parsed, missing, unreadable, not_regular, symlink_at_open, changed_during_read.
            Every pin is in the set whether or not it was followed.  Output: the PIN SET (deduplicated on (path, sha256),
            every source kept; 'read_aliases' lists each document realpath that shared another's read), exclusive create.
  snapshot  Reads the pin set once (embedded body_sha256 checked; --pins-sha256 checks the file bytes), resolves every pin
            path (lstat/readlink only: realpath, final_symlink, readlink), then reads every distinct file ONCE (by identity:
            hard links share one read) and records per realpath: status, sha256_from_bytes, bytes_read, size, mtime_ns,
            ctime_ns, ino, dev, mode, nlink, xattr_names, alias_of, content_guard, hash_only; and per pin: status (match /
            mismatch / the file's status), match, the resolution and hash_only.  A file that is (by realpath, or by the
            inode fstat reports on the one descriptor) an excluded file is not read: 'excluded_not_read', never a match.
            Output: the MANIFEST (exclusive create) with its own body_sha256, plus <out>.sha256 (the file's sha256), and the
            file sha on stdout.  Exit 0 when every pin matches, 3 when any pin is not matched (the manifest is still written:
            it is the evidence).
  compare   Reads a start and an end manifest once each (embedded body_sha256 checked; --start-sha256 and --end-sha256,
            REQUIRED, check the file bytes); refuses unless they are labelled start and end, have the same phase, the same
            pin set and the same excluded list, and end was taken no earlier than start.  INVALIDATE (exit 3) with a list
            when any pin is not matched at start or at end, any file's sha256 changed, any file's size, mtime_ns or ino
            changed (the file was rewritten or replaced, even with the same bytes now), any file's ctime_ns changed while
            its bytes, size, mtime_ns, ino and xattr-name set did not (D4), any pin's resolution changed (realpath,
            final_symlink, readlink), or the file set differs.  mode, nlink and dev changes are NOTES (they are listed; they do not explain a ctime change), as are
            xattr-name changes and an explained ctime change.  Otherwise OK (exit 0).  --out writes the report.

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
Non-regular files (directory, FIFO, device) are opened O_NONBLOCK, recorded 'not_regular' and never read.  Disclosed race
(N6): O_NOFOLLOW protects the last path component only, not a parent directory swapped after realpath.

Exit codes: 0 OK; 3 INVALIDATE (collect: written, but a followed pin was missing or mismatched; snapshot: written, some pin
not matched; compare: INVALIDATE); 2 refused input (nothing written).  Any other code is a tool error.
usage:
  PY -I -B pinned_input_envelope_c2v003.py collect --phase W1 --doc CFG.json --doc-pin SHA C1.json --scope C1.json \\
      /tail_readiness --v006 V006.md [--walk-only REG.jsonl] [--pin-list PINS.json] [--exclude PATH --reason TEXT ...] \\
      [--max-depth 0] [--depth-reason TEXT] [--max-follow-bytes N] [--allow-unresolved] --out ENVELOPE_W1_PINSET.json
  PY -I -B pinned_input_envelope_c2v003.py snapshot --pins ENVELOPE_W1_PINSET.json [--pins-sha256 H] --label start \\
      --out ENVELOPE_W1_START.json
  PY -I -B pinned_input_envelope_c2v003.py compare --start ENVELOPE_W1_START.json --start-sha256 S \\
      --end ENVELOPE_W1_END.json --end-sha256 N [--out ENVELOPE_W1_COMPARE.json]
"""
import argparse
import ctypes
import errno
import hashlib
import json
import os
import re
import stat
import sys
import time

TOOL = 'pinned_input_envelope_c2v003'
SCHEMA_PINSET = 'UNT_PINNED_INPUT_ENVELOPE_PINSET_C2V003'
SCHEMA_MANIFEST = 'UNT_PINNED_INPUT_ENVELOPE_MANIFEST_C2V003'
SCHEMA_COMPARE = 'UNT_PINNED_INPUT_ENVELOPE_COMPARE_C2V003'
EXIT_OK, EXIT_REFUSED, EXIT_INVALIDATE = 0, 2, 3

V006_KINDS = ('GATE_PIN', 'HANDOFF_PIN', 'SPEC_PIN', 'WATCH_PIN', 'TOOL_PIN', 'ROOT_LISTED_ROW_GATE')
KEYWORD_RE = re.compile(r'^(GATE_PIN|HANDOFF_PIN|SPEC_PIN|WATCH_PIN|TOOL_PIN|ROOT_LISTED_ROW_GATES|ROOT_LISTED_ROW_GATE)(?=\s|$)')
PIN_RE = re.compile(r'^(GATE_PIN|HANDOFF_PIN|SPEC_PIN|WATCH_PIN|TOOL_PIN|ROOT_LISTED_ROW_GATE) ([A-Z0-9][A-Z0-9_]*) ([0-9a-f]{64}) (/.*\S)$')
NONE_LINE = 'ROOT_LISTED_ROW_GATES NONE'
ENTRY_RE = re.compile(r'^## (A[0-9]+)(?=[\s:.(]|$)')
HEX64 = re.compile(r'[0-9a-f]{64}')
HEX64_ANYCASE = re.compile(r'[0-9a-fA-F]{64}')
PHASE_RE = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,63}')
POINTER_TOKEN_RE = re.compile(r'(?:[^~]|~[01])*', re.S)
POINTER_INDEX_RE = re.compile(r'0|[1-9][0-9]*')
LABELS = ('start', 'end')
CHUNK = 8 << 20
DEFAULT_MAX_DEPTH = 0
DEFAULT_MAX_FOLLOW_BYTES = 64 << 20
SIGNED_MAX_BYTES = 1 << 30
FOLLOW_SUFFIXES = ('.json', '.jsonl')
RUN_OUTPUT_BASENAMES = ('result.json', 'finish.json', 'progress.jsonl')
INVALIDATING_FILE_FIELDS = ('size', 'mtime_ns', 'ino')
NOTE_FILE_FIELDS = ('mode', 'nlink', 'dev')
RESOLUTION_FIELDS = ('realpath', 'final_symlink', 'readlink')
OPEN_FLAGS = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | getattr(os, 'O_CLOEXEC', 0)
NOT_OK_PROBLEM = ('missing', 'unreadable', 'not_regular', 'symlink_at_open', 'changed_during_read')
V006_EXCLUDE_REASON = ('V006 grows during every phase (V006 A228 D1): any pin whose realpath, or inode, is the --v006 file is '
                       'an excluded growing file, listed here and never snapshotted')
ALIAS_READ = 'inode_already_read'       # c2v003: read_once's answer for a descriptor whose inode was already read; never recorded
FILE_ENTRY_OWN = ('file_key', 'alias_of', 'content_guard', 'hash_only')   # c2v003: what an alias's file entry keeps as its own


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


def encodes(s):
    """True when s is a str that encodes as UTF-8 (no lone surrogates) -- D7."""
    if not isinstance(s, str):
        return False
    try:
        s.encode('utf-8')
    except UnicodeEncodeError:
        return False
    return True


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
    if not encodes(p):
        return 'PATH_NOT_ENCODABLE'
    if '\x00' in p:
        return 'PATH_HAS_NUL'
    if not p.startswith('/'):
        return 'PATH_NOT_ABSOLUTE'
    return None


def _dev_ino(path):
    """(dev, ino) of what path names now (os.stat, follows symlinks; no open), or None."""
    try:
        st = os.stat(path)
    except (OSError, ValueError):
        return None
    return (st.st_dev, st.st_ino)


# ------------------------------------------------------------------------------------------------ xattr names (D4)
_XATTR = {}


def _errname(en):
    return errno.errorcode.get(en, str(en))


def xattr_names(fd):
    """The extended-attribute NAMES on the open descriptor fd (sorted) -> (names, None), or (None, error).  Names only; no
    attribute value and no file content is read.  macOS: flistxattr(2) through ctypes; elsewhere os.listxattr(fd)."""
    if hasattr(os, 'listxattr'):
        try:
            return sorted(os.listxattr(fd)), None
        except OSError as e:
            return None, _errname(e.errno)
    f = _XATTR.get('flistxattr')
    if f is None:
        try:
            f = ctypes.CDLL(None, use_errno=True).flistxattr
        except (OSError, AttributeError):
            return None, 'XATTR_UNAVAILABLE'
        f.restype = ctypes.c_ssize_t
        f.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_size_t, ctypes.c_int]
        _XATTR['flistxattr'] = f
    for _ in range(4):
        n = f(fd, None, 0, 0)
        if n < 0:
            return None, _errname(ctypes.get_errno())
        if n == 0:
            return [], None
        buf = ctypes.create_string_buffer(n)
        m = f(fd, buf, n, 0)
        if m >= 0:
            return sorted(x.decode('utf-8', 'backslashreplace') for x in buf.raw[:m].split(b'\0') if x), None
        if ctypes.get_errno() != errno.ERANGE:
            return None, _errname(ctypes.get_errno())
    return None, 'ERANGE'


# ------------------------------------------------------------------------------------------------ the one read
def _meta(st):
    return {'size': st.st_size, 'mtime_ns': st.st_mtime_ns, 'ctime_ns': st.st_ctime_ns, 'ino': st.st_ino,
            'dev': st.st_dev, 'mode': st.st_mode, 'nlink': st.st_nlink}


def _lstat_id(path):
    """((dev, ino), metadata) of path itself (os.lstat: no open, a final symlink not followed), or (None, None) -- c2v003."""
    try:
        st = os.lstat(path)
    except (OSError, ValueError):
        return None, None
    return (st.st_dev, st.st_ino), _meta(st)


def _rec_id(rec):
    """(dev, ino) that fstat reported on the descriptor read_once opened, or None when nothing was opened -- c2v003."""
    if 'dev' in rec and 'ino' in rec:
        return (rec['dev'], rec['ino'])
    return None


def _share(shared, now):
    """c2v003: the one read's result `shared`, for another name of that inode whose own stat now (lstat, or fstat on its
    descriptor) is `now`.  `shared` itself when the inode is as it was when read (size, mtime_ns, ctime_ns, ino, dev, mode
    and nlink all equal); otherwise 'changed_during_read' with that name's own metadata -- the inode changed between its one
    read and this name (or the inode number was reused), and it is not read again."""
    m = {k: now.get(k) for k in ('size', 'mtime_ns', 'ctime_ns', 'ino', 'dev', 'mode', 'nlink')}
    if all(shared.get(k) == v for k, v in m.items()):
        return shared
    return dict(m, status='changed_during_read')


def read_once(path, keep, max_bytes=None, xattrs=False, exclude_ids=None, read_ids=None):
    """Open `path` ONCE and read it to EOF from that one descriptor -> (rec, buf).
    rec['sha256_from_bytes'] and rec['bytes_read'] are computed from exactly the chunks os.read returned, and buf (keep=True)
    is those same chunks joined: the sha a caller records, the length it records and the buffer it parses are one read.
    fstat on the same descriptor before and after: any difference, or a byte count other than the size, is
    'changed_during_read'.  O_NOFOLLOW: a final-component symlink is never followed ('symlink_at_open').  O_NONBLOCK: a FIFO
    cannot block the open.  A non-regular file is 'not_regular' and is not read; max_bytes: a larger file is 'too_large' and
    is not read; exclude_ids: a file whose (dev, ino) on this descriptor is excluded is 'excluded_not_read' and is not read.
    read_ids (c2v003): a file whose (dev, ino) on this descriptor is an inode already read in this subcommand is closed
    before any os.read, status ALIAS_READ; the caller takes the earlier read's result.
    xattrs=True: the xattr NAMES are taken from the same descriptor, before the second fstat (D4)."""
    try:
        fd = os.open(path, OPEN_FLAGS)
    except (OSError, ValueError) as e:
        en = getattr(e, 'errno', None)
        st = {errno.ENOENT: 'missing', errno.ENOTDIR: 'missing', errno.ELOOP: 'symlink_at_open'}.get(en, 'unreadable')
        return {'status': st, 'errno': _errname(en)}, None
    try:
        st0 = os.fstat(fd)
        meta = _meta(st0)
        if exclude_ids and (st0.st_dev, st0.st_ino) in exclude_ids:
            return dict(meta, status='excluded_not_read'), None
        if read_ids and (st0.st_dev, st0.st_ino) in read_ids:
            return dict(meta, status=ALIAS_READ), None
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
        xa = xattr_names(fd) if xattrs else None
        st1 = os.fstat(fd)
    except OSError as e:
        return {'status': 'unreadable', 'errno': _errname(e.errno)}, None
    finally:
        os.close(fd)
    stable = n == st0.st_size == st1.st_size and _meta(st1) == meta
    rec = dict(meta, status='ok' if stable else 'changed_during_read', sha256_from_bytes=h.hexdigest(), bytes_read=n)
    if xattrs:
        rec['xattr_names'], rec['xattr_error'] = xa
    return rec, (b''.join(chunks) if keep else None)


class OneRead:
    """At most one read per file per subcommand, a file being its identity (dev, ino) -- c2v003, CX1-ENV-01.  Results are
    kept by realpath and reused.  A realpath not seen yet whose lstat identity (no open) is an inode already read takes
    that read's result unopened; otherwise read_once opens it (O_NOFOLLOW) and, when fstat on the descriptor shows an inode
    already read, closes it unread and it takes that result (through _share: only while its own stat equals the read's).
    by_id: the descriptor identity of each read -> its realpath; alias_of: realpath -> the realpath whose read it shares.
    The guards are applied again to the realpath that is about to be opened (guard=False only for the --v006 named
    exception)."""

    def __init__(self, max_bytes):
        self.max_bytes = max_bytes
        self.seen = {}
        self.by_id = {}
        self.alias_of = {}

    def get(self, path, guard=True):
        rp = os.path.realpath(path)
        need(never_open_reason(rp) is None, 'NEVER_OPEN %s' % rp)
        if guard and content_guard(rp) is not None:
            return rp, {'status': 'hash_only'}, None
        if rp not in self.seen:
            ident, now = _lstat_id(rp)
            prim = self.by_id.get(ident)
            if prim is None:
                rec, buf = read_once(rp, keep=True, max_bytes=self.max_bytes, read_ids=self.by_id)
                if rec['status'] == ALIAS_READ:
                    prim, now = self.by_id[_rec_id(rec)], rec
                else:
                    self.seen[rp] = (rec, buf)
                    if _rec_id(rec) is not None:
                        self.by_id[_rec_id(rec)] = rp
            if prim is not None:
                prec, pbuf = self.seen[prim]
                srec = _share(prec, now)
                self.seen[rp] = (srec, pbuf if srec is prec else None)
                self.alias_of[rp] = prim
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


def pointer_tokens(ptr):
    """An RFC 6901 JSON pointer (non-empty, starting with '/') -> its unescaped reference tokens; else refused."""
    need(isinstance(ptr, str) and ptr.startswith('/') and encodes(ptr),
         'SCOPE_POINTER_SYNTAX %s (an RFC 6901 pointer starting with /)' % ascii(ptr))
    toks = ptr[1:].split('/')
    for t in toks:
        need(POINTER_TOKEN_RE.fullmatch(t) is not None, 'SCOPE_POINTER_SYNTAX %s (~ must be ~0 or ~1)' % ascii(ptr))
    return [t.replace('~1', '/').replace('~0', '~') for t in toks]


def resolve_pointer(obj, ptr, where):
    """The value at JSON pointer ptr in obj (a container), else refused."""
    cur = obj
    for t in pointer_tokens(ptr):
        if isinstance(cur, dict) and t in cur:
            cur = cur[t]
        elif isinstance(cur, list) and POINTER_INDEX_RE.fullmatch(t) is not None and int(t) < len(cur):
            cur = cur[int(t)]
        else:
            raise Refusal('SCOPE_POINTER_NOT_FOUND %s in %s' % (ascii(ptr), where))
    need(isinstance(cur, (dict, list)), 'SCOPE_NOT_A_CONTAINER %s in %s' % (ascii(ptr), where))
    return cur


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
    need(isinstance(out, str) and out and encodes(out) and '\x00' not in out, 'BAD_OUT_PATH')
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
    need(isinstance(path, str) and path and encodes(path) and '\x00' not in path, 'BAD_INPUT_PATH')
    path = os.path.abspath(path)
    need(never_open_reason(path) is None, 'INPUT_IN_FORBIDDEN_TREE %s' % path)
    need(content_guard(path) is None, 'INPUT_CONTENT_GUARDED %s %s' % (content_guard(path), path))
    if expected_sha is not None:
        need(isinstance(expected_sha, str) and HEX64.fullmatch(expected_sha) is not None, 'BAD_EXPECTED_SHA256')
    rec, buf = read_once(os.path.realpath(path), keep=True, max_bytes=SIGNED_MAX_BYTES)
    need(rec['status'] == 'ok', 'INPUT_UNREADABLE %s (%s)' % (path, rec['status']))
    if expected_sha is not None:
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
def collect(phase, docs, doc_pins, walk_only, pin_lists, v006, max_depth, max_follow_bytes, allow_unresolved, out,
            scopes=(), excludes=(), depth_reason=None):
    need(isinstance(phase, str) and PHASE_RE.fullmatch(phase) is not None, 'BAD_PHASE %s' % ascii(phase))
    need(isinstance(max_depth, int) and max_depth >= 0, 'BAD_MAX_DEPTH')
    need(max_depth == 0 or (isinstance(depth_reason, str) and encodes(depth_reason) and depth_reason.strip() != ''),
         'DEPTH_REASON_REQUIRED (--max-depth %s > 0 needs --depth-reason TEXT; V006 A228 D2)' % (max_depth,))
    need(isinstance(max_follow_bytes, int) and max_follow_bytes > 0, 'BAD_MAX_FOLLOW_BYTES')
    need(bool(docs or doc_pins or walk_only or pin_lists or v006), 'NO_SOURCES')
    out = check_out(out)

    # D3 scopes: one RFC 6901 pointer per JSON root document, keyed by the root path exactly as given
    scope_map = {}
    for sp in scopes:
        need(isinstance(sp, (list, tuple)) and len(sp) == 2, 'SCOPE_SHAPE')
        path, ptr = sp
        need(isinstance(path, str) and encodes(path), 'SCOPE_PATH_NOT_ENCODABLE %s' % ascii(path))
        need(path not in scope_map, 'SCOPE_GIVEN_TWICE %s' % path)
        pointer_tokens(ptr)
        scope_map[path] = ptr
    json_roots = set(docs) | {p for _, p in doc_pins} | set(walk_only)
    for path in scope_map:
        need(path in json_roots, 'SCOPE_NOT_A_ROOT_DOCUMENT %s (a --doc, --doc-pin or --walk-only path, as spelled)' % path)

    # D3 excludes (and, below, the D1 V006 entry): matched by realpath, or by inode
    excl = []
    for x in excludes:
        need(isinstance(x, dict), 'EXCLUDE_SHAPE')
        p, why = x.get('path'), x.get('reason')
        need(p is not None, 'REASON_WITHOUT_EXCLUDE %s (each --reason follows its own --exclude)' % ascii(why))
        need(encodes(p), 'EXCLUDE_NOT_ENCODABLE %s' % ascii(p))
        need(isinstance(why, str) and encodes(why) and why.strip() != '', 'EXCLUDE_WITHOUT_REASON %s' % p)
        need(p.startswith('/') and '\x00' not in p, 'EXCLUDE_PATH_NOT_ABSOLUTE %s' % ascii(p))
        di = _dev_ino(p)
        excl.append({'kind': 'exclude', 'rule': 'D3 (V006 A228)', 'path': p, 'realpath': os.path.realpath(p),
                     'dev_ino': list(di) if di else None, 'reason': why, '_pins': {}})

    reader = OneRead(max_follow_bytes)
    pins, queue, unresolved, near, roots, problems = {}, [], [], [], [], []
    followed = set()

    def excluded_match(path):
        rp = os.path.realpath(path)
        for e in excl:
            if path == e['path'] or rp == e['realpath']:
                return e, 'realpath'
        ids = [e for e in excl if e['dev_ino'] is not None]
        if ids:
            di = _dev_ino(path)
            if di is not None:
                for e in ids:
                    if list(di) == e['dev_ino']:
                        return e, 'inode'
        return None, None

    def add_pin(path, sha, depth, source, sha_written=None):
        prob = pin_path_problem(path)
        need(prob != 'PATH_NOT_ENCODABLE', 'PIN_PATH_NOT_ENCODABLE %s (source %s)' % (ascii(path), canon(source)))
        if prob:
            unresolved.append({'path': path, 'sha256': sha, 'why': prob, 'source': source})
            return
        nr = never_open_reason(path)
        need(nr is None, 'PIN_IN_FORBIDDEN_TREE %s %s (source %s)' % (nr, path, canon(source)))
        if sha_written is not None and sha_written != sha:
            source = dict(source, sha256_as_written=sha_written)
        e, how = excluded_match(path)
        if e is not None:
            ep = e['_pins'].setdefault((path, sha), {'path': path, 'sha256': sha, 'matched_by': how, 'sources': []})
            ep['sources'].append(source)
            return
        key = (path, sha)
        if key not in pins:
            pins[key] = {'path': path, 'sha256': sha, 'depth': depth, 'sources': [], 'follow': None,
                         'content_guard': content_guard(path)}
            queue.append(key)
        elif depth < pins[key]['depth']:
            pins[key]['depth'] = depth
        pins[key]['sources'].append(source)

    def open_root(path, role):
        need(isinstance(path, str) and path and encodes(path), 'ROOT_PATH_NOT_ENCODABLE %s' % ascii(path))
        need(path.startswith('/') and '\x00' not in path, 'ROOT_PATH_NOT_ABSOLUTE %s' % ascii(path))
        nr = never_open_reason(path)
        need(nr is None, 'ROOT_IN_FORBIDDEN_TREE %s %s' % (nr, path))
        if role in ('doc', 'doc_pin'):
            e, _how = excluded_match(path)
            need(e is None, 'ROOT_DOC_EXCLUDED %s (excluded as %s; a --doc is entered in the set)' % (path, e and e['path']))
        if role == 'v006':   # named exception (as P-112 read_v006): only the basename may name NGC3198
            need(path.lower().endswith('.md') and os.path.realpath(path).lower().endswith('.md'), 'V006_NOT_MD %s' % path)
            need(content_guard(os.path.dirname(path)) is None and
                 content_guard(os.path.dirname(os.path.realpath(path))) is None, 'V006_DIRECTORY_CONTENT_GUARDED %s' % path)
            need(os.path.basename(path).lower() not in RUN_OUTPUT_BASENAMES, 'V006_PATH_REFUSED %s' % path)
        else:
            g = content_guard(path)
            need(g is None, 'ROOT_DOC_CONTENT_GUARDED %s %s' % (g, path))
        rp, rec, buf = reader.get(path, guard=role != 'v006')
        need(rec['status'] != 'too_large', 'ROOT_DOC_TOO_LARGE %s (%s bytes > --max-follow-bytes %d)'
             % (path, rec.get('size'), max_follow_bytes))
        need(rec['status'] == 'ok', 'ROOT_DOC_UNREADABLE %s (%s)' % (path, rec['status']))
        return rp, rec, buf

    def walk_root(path, role, rec, rp, buf):
        try:
            obj = parse_json_buffer(path, buf)
        except (UnicodeDecodeError, ValueError, RecursionError):
            raise Refusal('ROOT_DOC_NOT_JSON %s' % path) from None
        scope = scope_map.get(path)
        target = obj if scope is None else resolve_pointer(obj, scope, path)
        found, nr = walk_pins(target)
        prefix = scope or ''
        if role in ('doc', 'doc_pin'):
            add_pin(path, rec['sha256_from_bytes'], 0, {'root': role})
            pins[(path, rec['sha256_from_bytes'])]['follow'] = 'root_document'
            followed.add((rp, rec['sha256_from_bytes']))
        for ptr, p, s, sw in found:
            add_pin(p, s, 1, {'doc': path, 'pointer': prefix + ptr}, sw)
        for x in nr:
            near.append(dict(x, doc=path, pointer=prefix + x['pointer']))
        roots.append({'role': role, 'path': path, 'realpath': rp, 'sha256_from_bytes': rec['sha256_from_bytes'],
                      'bytes': rec['bytes_read'], 'entered_in_pin_set': role in ('doc', 'doc_pin'), 'scope': scope,
                      'n_pins_found': len(found)})

    # V006 first: its identity is the D1 exclusion every other pin is checked against
    v006_rec, v006_pins = None, []
    if v006:
        rp6, rec6, buf6 = open_root(v006, 'v006')
        try:
            v006_pins, malformed = parse_v006_lines(buf6)
        except UnicodeDecodeError:
            raise Refusal('V006_NOT_UTF8 %s' % v006) from None
        need(not malformed, 'V006_MALFORMED_PIN_LINES %s lines %s' % (v006, malformed[:20]))
        excl.insert(0, {'kind': 'v006_growing_file', 'rule': 'D1 (V006 A228)', 'path': v006, 'realpath': rp6,
                        'dev_ino': [rec6['dev'], rec6['ino']], 'reason': V006_EXCLUDE_REASON, '_pins': {}})
        kinds = {}
        for x in v006_pins:
            kinds[x['kind']] = kinds.get(x['kind'], 0) + 1
        v006_rec = {'path': v006, 'realpath': rp6, 'sha256_from_bytes': rec6['sha256_from_bytes'], 'bytes': rec6['bytes_read'],
                    'n_pin_lines': len(v006_pins), 'by_kind': kinds}
    seen_ex = set()
    for e in excl:
        need(e['realpath'] not in seen_ex, 'EXCLUDE_DUPLICATE %s' % e['path'])
        seen_ex.add(e['realpath'])

    for path in docs:
        rp, rec, buf = open_root(path, 'doc')
        walk_root(path, 'doc', rec, rp, buf)
    for sha, path in doc_pins:
        need(isinstance(sha, str) and HEX64.fullmatch(sha) is not None, 'DOC_PIN_BAD_SHA256 %s' % ascii(sha))
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
                      'bytes': rec['bytes_read'], 'entered_in_pin_set': False, 'scope': None, 'n_pins_found': len(items)})
    if v006:
        for x in v006_pins:
            add_pin(x['path'], x['sha256'], 1, {'v006': v006, 'kind': x['kind'], 'name': x['name'], 'line': x['line'],
                                                'entry': x['entry']})
        roots.append({'role': 'v006', 'path': v006, 'realpath': v006_rec['realpath'],
                      'sha256_from_bytes': v006_rec['sha256_from_bytes'], 'bytes': v006_rec['bytes'],
                      'entered_in_pin_set': False, 'scope': None, 'n_pins_found': len(v006_pins)})

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
        need(rec['status'] != 'too_large', 'FOLLOWED_DOC_TOO_LARGE %s (depth %d; %s bytes > --max-follow-bytes %d; sources %s)'
             % (path, depth, rec.get('size'), max_follow_bytes, canon(pin['sources'][:3])))
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
            raise Refusal('FOLLOWED_DOC_NOT_JSON %s (depth %d; sources %s)' % (path, depth, canon(pin['sources'][:3]))) from None
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
    excluded = []
    for e in excl:
        eps = [e['_pins'][k] for k in sorted(e['_pins'])]
        excluded.append(dict({k: v for k, v in e.items() if k != '_pins'}, pins=eps, n_pins=len(eps)))
    tally = {}
    for p in plist:
        tally[p['follow']] = tally.get(p['follow'], 0) + 1
    when, ns = utc_now()
    obj = {'schema': SCHEMA_PINSET, 'tool': TOOL, 'rule': 'V006 A226 item 3 (single-read: A226 item 1, E_A220_1); A228 D1-D7',
           'phase': phase, 'created_utc': when, 'created_epoch_ns': ns, 'max_depth': max_depth,
           'depth_reason': depth_reason, 'max_follow_bytes': max_follow_bytes, 'allow_unresolved': bool(allow_unresolved),
           'scopes': [{'path': k, 'pointer': v} for k, v in sorted(scope_map.items())], 'roots': roots, 'v006': v006_rec,
           'excluded': excluded, 'pins': plist, 'unresolved_pins': unresolved, 'near_pins': near,
           'collect_problems': problems,
           'read_aliases': [{'realpath': rp, 'alias_of': reader.alias_of[rp]} for rp in sorted(reader.alias_of)],
           'counts': {'n_pins': len(plist), 'n_paths': len({p['path'] for p in plist}), 'n_roots': len(roots),
                      'by_follow': tally, 'n_hash_only': sum(1 for p in plist if p['content_guard']),
                      'n_excluded_entries': len(excluded), 'n_excluded_pins': sum(e['n_pins'] for e in excluded),
                      'n_unresolved': len(unresolved), 'n_near_pins': len(near), 'n_problems': len(problems),
                      'n_files_read': len(reader.seen) - len(reader.alias_of), 'n_read_aliases': len(reader.alias_of)}}
    fsha, bsha = write_signed(out, obj)
    rc = EXIT_INVALIDATE if problems else EXIT_OK
    _summary({'tool': TOOL, 'cmd': 'collect', 'phase': phase, 'out': out, 'file_sha256': fsha, 'body_sha256': bsha,
              'counts': obj['counts'], 'exit': rc})
    return rc


# ------------------------------------------------------------------------------------------------ snapshot
def snapshot(pins_path, pins_sha, label, out):
    need(label in LABELS, 'BAD_LABEL %s' % ascii(label))
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
    excluded = ps.get('excluded')
    need(isinstance(excluded, list), 'PIN_SET_SHAPE (excluded)')
    ex_rps, ex_ids = set(), set()
    for e in excluded:
        need(isinstance(e, dict) and pin_path_problem(e.get('path')) is None and isinstance(e.get('realpath'), str)
             and encodes(e['realpath']), 'PIN_SET_BAD_EXCLUDED %s' % canon(e)[:200])
        ex_rps.update((e['realpath'], os.path.realpath(e['path'])))
        di = e.get('dev_ino')
        if isinstance(di, list) and len(di) == 2 and all(isinstance(v, int) for v in di):
            ex_ids.add(tuple(di))
        now = _dev_ino(e['path'])
        if now is not None:
            ex_ids.add(now)
    res = {k: resolution(k[0]) for k in keys}
    guards = {k: content_guard(k[0]) for k in keys}
    by_file = {}
    for k in keys:
        by_file.setdefault(res[k]['realpath'], []).append(k)
    files = {}
    read_by_id = {}                                  # c2v003: (dev, ino) fstat'ed on a descriptor read -> its realpath
    for rp in sorted(by_file):
        need(never_open_reason(rp) is None, 'NEVER_OPEN %s' % rp)
        g = content_guard(rp) or next((guards[k] for k in by_file[rp] if guards[k]), None)
        prim = None
        if rp in ex_rps:                             # an excluded (growing) file is never snapshotted (D1, D3)
            rec = {'status': 'excluded_not_read'}
        else:
            ident, now = _lstat_id(rp)
            prim = read_by_id.get(ident)             # a hard link to an inode already read: not opened (CX1-ENV-01)
            if prim is None:
                rec, _ = read_once(rp, keep=False, xattrs=True, exclude_ids=ex_ids, read_ids=read_by_id)   # the one read (bytes only)
                if rec['status'] == ALIAS_READ:      # the descriptor is an inode already read: closed unread
                    prim, now = read_by_id[_rec_id(rec)], rec
                elif _rec_id(rec) is not None:
                    read_by_id[_rec_id(rec)] = rp
            if prim is not None:                     # that inode's one read, shared; this realpath keeps its own entry
                rec = _share({k: v for k, v in files[prim].items() if k not in FILE_ENTRY_OWN}, now)
        files[rp] = dict(rec, file_key=rp, alias_of=prim, content_guard=g, hash_only=g is not None)
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
    man = {'schema': SCHEMA_MANIFEST, 'tool': TOOL, 'rule': 'V006 A226 item 3; A228 D1-D7', 'phase': ps.get('phase'),
           'label': label, 'created_utc': when, 'created_epoch_ns': ns,
           'pin_set': {'path': pins_path, 'file_sha256': ps_fsha, 'body_sha256': ps.get('body_sha256')},
           'collect': {'max_depth': ps.get('max_depth'), 'depth_reason': ps.get('depth_reason'), 'scopes': ps.get('scopes'),
                       'roots': ps.get('roots')},
           'excluded': excluded, 'files': [files[rp] for rp in sorted(files)], 'pins': entries, 'unresolved_pins': unresolved,
           'all_match': n_match == len(entries),
           'counts': {'n_pins': len(entries), 'n_files': len(files), 'n_alias_files': sum(1 for f in files.values() if f['alias_of']),
                      'by_status': tally, 'n_match': n_match,
                      'n_not_matched': len(entries) - n_match,
                      'n_hash_only_pins': sum(1 for e in entries if e['hash_only']),
                      'n_final_symlink_pins': sum(1 for e in entries if e['final_symlink']),
                      'n_resolved_differs': sum(1 for e in entries if e['resolved_differs']),
                      'n_excluded_pins_not_snapshotted': sum(len(e.get('pins') or []) for e in excluded),
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
    need(start_sha is not None and end_sha is not None,
         'MANIFEST_SHA256_REQUIRED (--start-sha256 and --end-sha256 are both required; V006 A228 D6)')
    if out is not None:
        out = check_out(out)
    s, s_fsha, start = load_signed(start, SCHEMA_MANIFEST, start_sha)
    e, e_fsha, end = load_signed(end, SCHEMA_MANIFEST, end_sha)
    need(s.get('label') == 'start', 'START_NOT_LABELLED_START (%s)' % ascii(s.get('label')))
    need(e.get('label') == 'end', 'END_NOT_LABELLED_END (%s)' % ascii(e.get('label')))
    need(s.get('phase') == e.get('phase'), 'PHASE_DIFFERS %s %s' % (ascii(s.get('phase')), ascii(e.get('phase'))))
    need(isinstance(s.get('pin_set'), dict) and isinstance(e.get('pin_set'), dict)
         and s['pin_set'].get('body_sha256') == e['pin_set'].get('body_sha256')
         and s['pin_set'].get('file_sha256') == e['pin_set'].get('file_sha256'), 'PIN_SET_DIFFERS')
    need(isinstance(s.get('created_epoch_ns'), int) and isinstance(e.get('created_epoch_ns'), int)
         and e['created_epoch_ns'] >= s['created_epoch_ns'], 'END_TAKEN_BEFORE_START')
    need(s.get('unresolved_pins') == e.get('unresolved_pins'), 'UNRESOLVED_LISTS_DIFFER')
    need(isinstance(s.get('excluded'), list) and s.get('excluded') == e.get('excluded'), 'EXCLUDED_LISTS_DIFFER')
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
        xa, xb = a.get('xattr_names'), b.get('xattr_names')
        xattr_changed = isinstance(xa, list) and isinstance(xb, list) and xa != xb
        if xattr_changed:
            notes.append({'kind': 'XATTR_NAMES_CHANGED', 'file_key': fk, 'added': sorted(set(xb) - set(xa)),
                          'removed': sorted(set(xa) - set(xb))})
        ca, cb = a.get('ctime_ns'), b.get('ctime_ns')
        rewritten = bool(changed) or a.get('sha256_from_bytes') != b.get('sha256_from_bytes') or a.get('status') != b.get('status')
        if ca is not None and cb is not None and ca != cb:          # D4
            if xattr_changed:
                notes.append({'kind': 'CTIME_CHANGED_EXPLAINED', 'file_key': fk, 'ctime_ns': [ca, cb],
                              'explained_by': 'xattr_names'})
            elif rewritten:                                         # already INVALIDATE above (SHA_CHANGED / FILE_REWRITTEN)
                notes.append({'kind': 'CTIME_CHANGED_EXPLAINED', 'file_key': fk, 'ctime_ns': [ca, cb],
                              'explained_by': 'the file change already invalidating'})
            else:                                                   # ctime-only: bytes, size, mtime and inode equal
                problems.append({'kind': 'CTIME_CHANGED_UNEXPLAINED', 'file_key': fk, 'ctime_ns': [ca, cb],
                                 'xattr_names': [xa, xb], 'xattr_error': [a.get('xattr_error'), b.get('xattr_error')]})
    verdict = 'INVALIDATE' if problems else 'OK'
    when, ns = utc_now()
    ex_summary = [{'kind': x.get('kind'), 'path': x.get('path'), 'reason': x.get('reason'), 'n_pins': x.get('n_pins')}
                  for x in s.get('excluded') or []]
    rep = {'schema': SCHEMA_COMPARE, 'tool': TOOL, 'rule': 'V006 A226 item 3: any changed byte invalidates the phase; A228 D4',
           'phase': s.get('phase'), 'verdict': verdict, 'created_utc': when, 'created_epoch_ns': ns,
           'start': {'path': start, 'file_sha256': s_fsha, 'body_sha256': s.get('body_sha256'), 'created_utc': s.get('created_utc')},
           'end': {'path': end, 'file_sha256': e_fsha, 'body_sha256': e.get('body_sha256'), 'created_utc': e.get('created_utc')},
           'pin_set': s.get('pin_set'), 'n_pins': len(sp), 'n_files': len(set(sf) | set(ef)),
           'excluded': ex_summary, 'n_excluded_pins_not_checked': sum((x.get('n_pins') or 0) for x in ex_summary),
           'problems': problems, 'notes': notes, 'unresolved_pins_not_checked': len(s.get('unresolved_pins') or [])}
    summ = {'tool': TOOL, 'cmd': 'compare', 'phase': rep['phase'], 'verdict': verdict, 'n_problems': len(problems),
            'n_notes': len(notes), 'problem_kinds': sorted({p['kind'] for p in problems}),
            'n_excluded_pins_not_checked': rep['n_excluded_pins_not_checked'],
            'unresolved_pins_not_checked': rep['unresolved_pins_not_checked']}
    if out is not None:
        fsha, bsha = write_signed(out, rep)
        summ.update(out=out, file_sha256=fsha, body_sha256=bsha)
    rc = EXIT_INVALIDATE if problems else EXIT_OK
    summ['exit'] = rc
    _summary(summ)
    return rc


# ------------------------------------------------------------------------------------------------ CLI
class _ExcludeAction(argparse.Action):
    """--exclude PATH: a new exclusion; its reason is the --reason that follows it."""

    def __call__(self, parser, namespace, values, option_string=None):
        lst = list(getattr(namespace, self.dest, None) or [])
        lst.append({'path': values, 'reason': None})
        setattr(namespace, self.dest, lst)


class _ReasonAction(argparse.Action):
    """--reason TEXT: the reason of the --exclude just before it (a --reason with no open --exclude is kept as an orphan,
    which collect refuses)."""

    def __call__(self, parser, namespace, values, option_string=None):
        lst = list(getattr(namespace, self.dest, None) or [])
        if lst and lst[-1]['path'] is not None and lst[-1]['reason'] is None:
            lst[-1] = dict(lst[-1], reason=values)
        else:
            lst.append({'path': None, 'reason': values})
        setattr(namespace, self.dest, lst)


def build_parser():
    ap = argparse.ArgumentParser(prog=TOOL, description='Root integrity envelope (V006 A226 item 3, A228); single-read.')
    sub = ap.add_subparsers(dest='cmd', required=True)
    c = sub.add_parser('collect')
    c.add_argument('--phase', required=True)
    c.add_argument('--doc', action='append', default=[])
    c.add_argument('--doc-pin', nargs=2, action='append', default=[], metavar=('SHA256', 'PATH'))
    c.add_argument('--walk-only', action='append', default=[])
    c.add_argument('--pin-list', action='append', default=[])
    c.add_argument('--v006')
    c.add_argument('--scope', nargs=2, action='append', default=[], metavar=('PATH', 'POINTER'))
    c.add_argument('--exclude', action=_ExcludeAction, dest='excludes', metavar='PATH')
    c.add_argument('--reason', action=_ReasonAction, dest='excludes', metavar='TEXT')
    c.set_defaults(excludes=[])
    c.add_argument('--max-depth', type=int, default=DEFAULT_MAX_DEPTH)
    c.add_argument('--depth-reason')
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
    m.add_argument('--start-sha256', required=True)
    m.add_argument('--end-sha256', required=True)
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
                           a.max_follow_bytes, a.allow_unresolved, a.out, scopes=[tuple(x) for x in a.scope],
                           excludes=a.excludes, depth_reason=a.depth_reason)
        if a.cmd == 'snapshot':
            return snapshot(a.pins, a.pins_sha256, a.label, a.out)
        return compare(a.start, a.end, a.start_sha256, a.end_sha256, a.out)
    except Refusal as r:
        print(json.dumps({'tool': TOOL, 'cmd': a.cmd, 'refused': str(r), 'exit': EXIT_REFUSED}, sort_keys=True), file=sys.stderr)
        return EXIT_REFUSED


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

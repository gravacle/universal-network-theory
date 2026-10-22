# Claude3 seal-assembly builder (dispatch 0626): the per-step helper ROOT_SEAL_STEPS.sh calls. One subcommand per step.
# c3v002: supersedes seal_steps_c3sa.py (f7c14729, never used): no-follow identity-tree scan (os.scandir, follow_symlinks=False)
# with the fence armed first; per-mode fence self-test expectations.
# c3v003: supersedes c3v002 (never used): numpy is imported BEFORE the fence is armed (its import-time ctypes probing is not a
# seal action), and the fence module is c3v003 (no ctypes.dlopen rule).
# c3v004 (dispatch 0633, seal tools v003 interface): covered-later comes ONLY from a root-supplied, byte-pinned dispositions JSON
# ({entry, disposition: revised|no_change, reason: non-empty} per entry after the prereg's entry table, plus any table row whose
# section bytes changed); subcommand 'dispositions' validates it and derives the bare-name list the v001 placeholders still take.
# c3v005: supersedes c3v004 (never used): rehash-entries reports the rows checked and unchanged (c3v004 printed a null).
# c3v006: supersedes c3v005 (dry run 2 pass B false positive): manifest scans read the path VALUES only, never the free 'note' text.
# c3v007: supersedes c3v006: the dispositions pre-check accepts the v003 row format announced in Claude4 0105 (2089d3e6): rows
# {entry, disposition, reason, section_sha256 [, change {from_section_sha256, to_section_sha256, what_changed}]} and a top-level
# frozen_addendum_sha256; each present sha is verified against the frozen bytes. The exact key set is v003 tool 1's to enforce.
# c3v008 (FROM_CODEX/0639; Codex1 SA-CX1-B1, SA-CX1-B2): (B1) no realpath / resolve anywhere: every path is checked by a no-follow
# component walk from '/' (os.lstat of each prefix, never following); a symlink component is refused AT the link (its text is read
# with readlink and vetted for protected names and /.vol; the target's metadata is never read); files are read through
# O_NOFOLLOW with an inode match against the walk. (B2) every module this helper loads (fence, compare, guard) is read ONCE,
# digest-checked, compiled from that buffer and exec'd into a fresh module: no importlib loader, no bytecode cache, no second read.
# c3v009 (FROM_CODEX/0640, SA-CX1-B3 + PV-D05-1): the dispositions input is ONLY the v003 object {schema, frozen_addendum_sha256,
# entries} (schema UNT_V007_LATER_ENTRY_DISPOSITIONS_C4V001: v003 dev seal_common_c4v003.py L24, a work copy, 101a3aeb at
# 22:10Z; PENDING v003 final); the bare-list, 'dispositions' and 'rows' forms refuse. Changed cited entries are found byte for
# byte against the bytes the prereg's table was read from (r5 entries_after_A81.addendum_read). PV-D05-1: on a changed cited
# entry plain no_change refuses; revised needs a prereg-revision pointer (key 'prereg_revision': name PENDING v003);
# no_change_after_change needs changed_text (a substring of the new section bytes and NOT of the old) and why_no_prereg_effect.
# c3v008 is superseded unused.
# c3v010 (FROM_CODEX/0642, A105; Claude4 0108 RP-S1, W7-S1): subcommand 'output-root' (check / create / verify): the step-2 output
# root is created as a NEW, EMPTY, real directory, EXCLUSIVELY (refused if it exists in any form: a directory, a file or a symlink,
# dangling or not); every parent component passes the no-follow walk; the one missing parent level (UNT_INTERNAL_RUNS) may be
# created; after the mkdir it is opened O_NOFOLLOW_ANY|O_DIRECTORY, its (st_dev, st_ino) must equal the walk, its realpath (fcntl
# F_GETPATH of that fd: the kernel's own path, no link can be followed; os.path.realpath is still never called) must equal the
# literal, its st_dev must equal /System/Volumes/Data's, it must be empty; device, realpath and free space are returned for the run
# log. W7-S1 (A105.1, A78 N2): make-config's producer_allowlist is BUILD_V007's 15-row table EXACTLY, in table order (strict parse of
# the '## Supported runtime entry allowlist' section; any other count, any row not byte-equal in path and sha, a reordered or a
# duplicated row refuses); the serialized bytes are checked BEFORE the exclusive write and the written file again after it; the
# new subcommand 'check-config-allowlist' re-checks a written config from its bytes. --n-sources is gone (15 is fixed, W7_ROWS).
# Directories this helper creates (output-root only) are created with os.mkdir, which never reuses an existing entry.
# c3v012 (FROM_CODEX/0643, ruling A106): (A) freeze takes --open-bytes: BEFORE copying, the open V005 must hash to the pinned FINAL
# sha AND have the pinned length; the exclusive copy is re-read (no-follow) and re-hashed. (C-02) check-tor: the text of record is
# exactly the prereg its SELECTED file stores (path and sha), it is UNSEALED (every seal slot but cache_directory_r6_only still a
# PENDING marker), and a given sealed prereg is not it and is byte-equal to it with only seal_slots.<k>.value filled. (C-04)
# slot-registry: every slot record is checked through the reviewed compare r13's OWN load_producer_registry, gate_record_sha_codes,
# file_pin_codes and identity_comparator_codes (r13 read once, compiled from that buffer, inside the fence) against the slotted
# registry. (C-05 + C-06) bound-check: the launcher and guard are BUILD_V007 rows by EXACT file name and sha, the bound plan names
# exactly them, and the WHOLE bound command is byte-equal to the binder's output form (its comment line and its command line, from
# the pinned binder source). (C-03) gates-provenance: GATES_ONLY.json (sealed mode) evaluated the slotted gate records (record
# sha equal, status PASS). selected-names: a SELECTED file (from bytes) names each given path and sha, and names no other sha for
# the same path. Nothing else changes.
# c3v013 (FROM_CODEX/0644, ruling A107 in the V006 addendum; Codex1 0101 7152346 findings): (C02-SEL-STRICT) a SELECTED file is parsed
# STRICTLY from the one buffer pin() read: invalid UTF-8, a BOM, nesting deeper than 64, a duplicate key, NaN / Infinity / a float
# overflowing to inf, an integer longer than 4300 digits, trailing or invalid JSON text and a non-object top level each REFUSE with
# a typed SELECTED_* code; there is no substring fallback anywhere. (C02-SEL-ASSOCIATION) each requested (path, sha) must be stored
# as ONE object of that parse whose 'path' equals the absolute path exactly and whose 'sha256' equals the sha exactly (Claude4 0112:
# exact {path, sha256} pairs; role keys PENDING Claude4's real SELECTED files); unrelated strings and suffixed paths never count,
# and any object giving the same path another value refuses. Both check-tor and the v003 selected-names use it. (A106-C03-S1)
# gates-provenance validates the slot sha and the body record_sha256 as 64-hex lowercase BEFORE comparing. (A107, P12 option (b))
# slot-registry takes the explicit two-entry exclusion list (--exclude certificates.EPS_NGC=PATH=SHA, certificates.I1T_NGC=PATH=SHA)
# and refuses any other list (a third slot, a missing one, another path or sha) and an excluded slot whose pin differs; excluded
# slots are still pinned from bytes and reported. (Codex1 0101 C04 boundary note, closed) every non-excluded slotted gate record must
# also carry its gate's pass verdict from r13's own GATE_PASS_VERDICTS (a registered FAIL, an absent or an unknown verdict refuses).
# c3v014 (0644 follow-up; Claude4 SELECTED_R6_C4V001.json 7200acd9, schema UNT_V007_SELECTED_PREREG_C4V001): C02-SEL-ASSOCIATION is now
# ROLE-QUALIFIED with the real schema's keys: the SELECTED file (strict parse as c3v013) must carry the given schema string and a
# 'files' object whose EVERY entry is exactly {path: <absolute>, sha256: <64 lowercase hex>} with no path given two shas; each
# requested pin must be EXACTLY files[<role>] (check-tor: --selected-schema and --tor-role, e.g. text_of_record; the new
# selected-roles subcommand checks any --role-pin ROLE=PATH=SHA and pins each from bytes). The generic exact-pair search remains
# only for v003's selected-names until Claude4's v003 SELECTED file (and its role keys) exists.
# c3v015 (WIRE v003; Claude4 SELECTED_SEAL_TOOLS_V003_C4V001.json cf7e5b2f): the generic exact-pair search (_selected_pairs,
# _selected_names, the selected-names subcommand) is REMOVED: the v003 SELECTED file is checked role-qualified by selected-roles
# like r6's. New subcommand check-driver-build-record (step 2a): the record v003 tool 5 printed and the script wrote exclusively
# must be byte-equal to the reviewed compare's builtin_r5_build() plus check_record (tool 5's own form: indent 1, sorted keys) and
# pass the compare's driver_build_codes and r5_custody_codes (fenced; the compare read once).
# c3v016: SLOT_KEYS is v003's slot schema UNT_V007_SEAL_SLOTS_C4V002 (adds cascade_map_r5_addendum and admission_entry); nothing else.
# c3v017 (A110/A111; 0646, 0647): new subcommand check-disclosures, the strict read-once pre-check of root's SEAL_MANUAL_DISCLOSURES_V001
# file (the c3v013 SELECTED-strictness rules; its e_r6_1_text byte-equal to r6's SELECTED erratum). Nothing else changes.
# c3v011 supersedes c3v010 (823c8aca; used only by dry run 20261018T225153Z): output-root refuses an empty, '.' or '..' component
# LEXICALLY, before any walk or mkdir (c3v010 walked the root's own last component only when its parent existed, so a path
# ending in '..' under an absent parent could have created that parent before refusing). Nothing else changes.
# Rules (every subcommand): each input is a (path, sha256) pin verified from bytes BEFORE it is used; every path argument is an
# absolute /Users/... literal whose realpath is itself (no firmlink /System/Volumes/Data spelling, no /private, no /.vol, no '..');
# every file this helper creates is created with open(path, 'x'/'xb') and nothing is ever overwritten, edited or deleted; strict
# JSON everywhere (a duplicate key or a non-finite constant refuses, A71); no process start, no network. The verdict JSON goes to
# STDERR (stdout stays free for the compare's own output in the gates-only step); exit 0 = PASS, 2 = REFUSE.
# Nothing here opens, stats or lists the registered C5H run, any runs_ext/UVT_* tree (except gates-only in ROOT mode, which reads the
# three identity-run trees named by the identity records of record, exactly as root's seal step B6 requires), /.vol or NGC targets.
import argparse, ast, fcntl, hashlib, json, os, re, shlex, stat as stat_mod, sys, time, types
from pathlib import Path

PIN_NAMES = ('V007_PREREG_SHA256', 'PIN_ADDENDUM_V005', 'PIN_DRIVER_BUILD_RECORD', 'PIN_V010_R5_CHECK', 'PIN_PRODUCER_REGISTRY')  # A82
SHA_PINS = ('V007_PREREG_SHA256', 'PIN_ADDENDUM_V005')
PREREG_SLOT_OF = {'frozen_addendum': 'frozen_addendum', 'driver': 'driver', 'compare': 'compare_reviewed_source',
                  'identity_comparator': 'identity_comparator', 'identity_gate_records': 'identity_gate_records',
                  'launch_packet': 'launch_packet', 'certificates': 'certificates', 'producer_registry': 'producer_registry',
                  'cache_directory_r6_only': 'cache_directory_r6_only'}       # seal tools README (1e04bd2a) "Mapping from slot to prereg"
SLOT_KEYS = ('schema', 'driver_branch', 'ngc_gas_M_s', 'frozen_addendum', 'driver', 'driver_build_record', 'driver_check_record',
             'compare_reviewed_source', 'identity_comparator', 'identity_gate_records', 'launch_packet', 'certificates',
             'producer_registry', 'cache_directory_r6_only', 'cascade_map_r5_addendum', 'admission_entry')   # v003 check_slot_fill_c4v003 SLOT_KEYS (C4V002)
AUTHORITY = {'identity': 'Claude2', 'role': 'coordinator_and_single_scientific_launch_owner'}   # guard v008 AUTHORITY
CONFIG_SCHEMA = 'UNT_ROOT_SEAL_ADMISSION_CX1V001'                                                # guard v008 / FORMAT_V005 item 2
RECEIPT_SCHEMA = 'UNT_ROOT_SEAL_ADMISSION_RECEIPT_V001'        # PROPOSED by Claude3 (no text of record fixes a receipt schema name)
BUILD_HEADER = '## Supported runtime entry allowlist'
W7_ROWS = 15                                      # A105.1 / A78 N2: the admission allowlist is exactly BUILD_V007's 15 rows
W7_ROW_RX = re.compile(r'([0-9a-f]{64})  (/Users/\S+)')   # one table row (fullmatch): sha, two spaces, an absolute path, no whitespace
VOLUME_ROOT = '/System/Volumes/Data'              # RP-S1 / RUNBOOK_V008 L37: the internal startup Data volume (st_dev compare)
SEL_MAX_DEPTH = 64                                # C02-SEL-STRICT: nesting deeper than this refuses (typed), never a RecursionError
SEL_MAX_INT_DIGITS = 4300                         # C02-SEL-STRICT: an integer literal longer than this refuses (typed)
C04_A107_EXCLUSIONS = {                           # A107 (V006 addendum), P12 option (b): exactly these two slots, by name, path and sha
    'certificates.EPS_NGC': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_ngc_k32/gates/EPS_CERT_NGC91_V001.json',
                             '1d5eef1b602d2489ba8c0e652156555bbd2bfddf083931c7c4c82fa0a1e0c13d'),
    'certificates.I1T_NGC': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v002/gates/I1T_NGC_T120L_V001.json',
                             '3ae7981a0c022d50a153a0857b10660661fedfd5adedcba3b805802b4a1809b6')}
C05_LAUNCHER_NAME = 'route_a_token_launcher_cx1v007.py'   # 0643 B / A106.2 C-05: exact file name (and the sha from BUILD_V007)
C05_GUARD_NAME = 'producer_guard_cx1v008.py'
BINDER_PYTHON_LINE = "PYTHON='/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'"
BINDER_COMMENT = ('# Claude2 only after root seal/config/receipt publication, independently verified UNT_ROOT_ADMISSION_SHA256 and all '
                  'root gates. This generator launches nothing.')
BINDER_CMD_FORM = "cmd=shlex.join([PYTHON,'-I','-B',plan['launcher']['path'],str(outs[0].resolve()),'--execute-root-only'])"
BINDER_WRITE_FORM = "f.write('" + BINDER_COMMENT + "\\n'+cmd+'\\n')"
CERT_SLOT_GATES = {'EPS': ('EPS',), 'LO': ('LO',), 'GQ': ('GQ',), 'DOUBLING': ('DOUBLING',), 'LO_NGC': ('LO_NGC',),
                   'EPS_NGC': ('EPS_NGC', 'EPS'), 'I1T_NGC': ('I1T_NGC', 'I1T')}   # C-04: the gate each certificate slot's record may name
IDENT_SLOT_GATE = {'Z2': 'B1', 'Z2_OFF_RO1': 'B1_OFF', 'B0prime_RERUN': 'B0prime_RERUN'}     # r13 IDENTITY_GATES
C03_SLOT_GATES = (('certificates', 'EPS', 'EPS'), ('certificates', 'LO', 'LO'), ('certificates', 'GQ', 'GQ'),
                  ('certificates', 'DOUBLING', 'DOUBLING'), ('certificates', 'LO_NGC', 'LO_NGC'), ('identity_gate_records', 'Z2', 'B1'),
                  ('identity_gate_records', 'Z2_OFF_RO1', 'B1_OFF'), ('identity_gate_records', 'B0prime_RERUN', 'B0prime_RERUN'))
HEX64 = re.compile(r'[0-9a-f]{64}')
ROW_VALUE_RX = re.compile(r'(?<![\w.])\d+\.\d{3,}(?![\w.])|(?<![\w.])\d(?:\.\d+)?[eE][-+]?\d+(?![\w.])')   # build_seal_record_c4v001
C5H_NAME_CF = 'kmax_a2f10_c5h_run_v001'
MARK_ROOT = 'PENDING_ROOT_AT_SEAL_ASSEMBLY:'
MARK_RULING = 'PENDING_ROOT_RULING:'


class Refuse(Exception):
    pass


class DuplicateKey(ValueError):
    pass


def _pairs(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise DuplicateKey('DUPLICATE_JSON_KEY %r' % k)
        out[k] = v
    return out


def _nonfinite(c):
    raise ValueError('NON_FINITE_JSON_CONSTANT ' + c)


def sjson(raw):
    return json.loads(raw, object_pairs_hook=_pairs, parse_constant=_nonfinite, parse_int=str_int)


def str_int(s):           # A102 lesson (A-B1): never let the int-digit limit turn a strict parse into a plain ValueError
    if len(s) > 4000:
        raise Refuse('JSON_INTEGER_TOO_LONG')
    return int(s)


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


_PROTECTED_CF = (C5H_NAME_CF, '/runs_ext', 'runs_ext/', '/uvt_', '/.vol', 'sparc', 'ngc3198_target', 'ngc_target', 'rotmod')
_PROTECTED_LINK_CF = (C5H_NAME_CF, 'runs_ext', 'uvt_', '/.vol', '.vol/', 'sparc', 'ngc3198_target', 'ngc_target', 'rotmod')


def _lexical_veto(s, label, allow_run_trees=False):
    sc = s.casefold()
    bad = [x for x in _PROTECTED_CF if x in sc and not (allow_run_trees and x in ('/runs_ext', 'runs_ext/', '/uvt_'))]
    if bad or sc.startswith('/.vol') or sc.startswith('//'):
        raise Refuse('PATH_PROTECTED_REFUSED %s: %r' % (label, s))


def nofollow_walk(p, label, final_may_be_absent=False, allow_run_trees=False):
    """SA-CX1-B1: lstat every prefix of the absolute path p from '/', never following a link. Each prefix is lexically vetted before
    its own lstat. A symlink component is refused at the link: its text (readlink: the link's own bytes) is vetted for protected names
    and /.vol and reported, and its target is never stat'ed, resolved or opened. Every component but the last must be a directory.
    Returns the final component's lstat (None when it is absent and that is allowed)."""
    parts = p.split('/')[1:]
    cur, st = '', None
    for i, comp in enumerate(parts):
        if comp in ('', '.', '..'):
            raise Refuse('PATH_COMPONENT_REFUSED %s: %r' % (label, p))
        cur = cur + '/' + comp
        _lexical_veto(cur, label, allow_run_trees)
        try:
            st = os.lstat(cur)
        except FileNotFoundError:
            if final_may_be_absent and i == len(parts) - 1:
                return None
            raise Refuse('PATH_COMPONENT_MISSING %s: %s' % (label, cur))
        if stat_mod.S_ISLNK(st.st_mode):
            txt = os.readlink(cur)
            tc = txt.casefold()
            if any(x in tc for x in _PROTECTED_LINK_CF) or tc.startswith('/.vol') or tc.startswith('.vol'):
                raise Refuse('PATH_LINK_TEXT_PROTECTED %s: %s -> %r (refused at the link; the target was never read)' % (label, cur, txt))
            raise Refuse('PATH_HAS_SYMLINK_COMPONENT %s: %s -> %r (never followed: the seal uses canonical spellings only)' % (label, cur, txt))
        if i < len(parts) - 1 and not stat_mod.S_ISDIR(st.st_mode):
            raise Refuse('PATH_COMPONENT_NOT_A_DIRECTORY %s: %s' % (label, cur))
    return st


def path_policy(p, must_exist=None, label='path'):
    """an absolute /Users/... literal with no protected name, no firmlink or /private spelling, no '..', '.' or '//', every component
    checked by nofollow_walk (no realpath, no resolve). must_exist True: the final component exists (and is not a link);
    False: it is absent and its parent is a real directory chain. Returns the final lstat (or None)."""
    if not isinstance(p, str) or not p.startswith('/Users/') or '\n' in p or '\x00' in p:
        raise Refuse('PATH_NOT_ABSOLUTE_USERS_SPELLING %s: %r' % (label, p))
    if p.startswith('/System/Volumes/Data') or '//' in p or p.endswith('/'):
        raise Refuse('PATH_SPELLING_REFUSED %s: %r' % (label, p))
    _lexical_veto(p, label)
    if must_exist is True:
        return nofollow_walk(p, label)
    if must_exist is False:
        st = nofollow_walk(p, label, final_may_be_absent=True)
        if st is not None:
            raise Refuse('OUTPUT_EXISTS %s: %s' % (label, p))
        return None
    return None


def read_nofollow(path, label):
    """bytes of a regular file whose every component nofollow_walk accepted, read through O_NOFOLLOW; the opened inode must be the
    walked inode (a swap between the walk and the open refuses)."""
    st = path_policy(path, must_exist=True, label=label)
    if not stat_mod.S_ISREG(st.st_mode):
        raise Refuse('PIN_NOT_A_REGULAR_FILE %s: %s' % (label, path))
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        fs = os.fstat(fd)
        if (fs.st_dev, fs.st_ino) != (st.st_dev, st.st_ino):
            raise Refuse('PATH_CHANGED_DURING_READ %s: %s' % (label, path))
        chunks = []
        while True:
            b = os.read(fd, 1 << 20)
            if not b:
                break
            chunks.append(b)
    finally:
        os.close(fd)
    return b''.join(chunks)


def pin(path, sha, label='pin'):
    """(path, sha) from bytes (read once, no-follow); returns the bytes."""
    if not (isinstance(sha, str) and HEX64.fullmatch(sha)):
        raise Refuse('PIN_SHA_FORMAT %s: %r' % (label, sha))
    b = read_nofollow(path, label)
    got = sha_bytes(b)
    if got != sha:
        raise Refuse('PIN_BYTES_MISMATCH %s: %s has %s, pinned %s' % (label, path, got, sha))
    return b


def pinref(s, label):
    """'PATH=SHA' -> (path, sha); the sha is the last 64 chars after '='."""
    if not isinstance(s, str) or '=' not in s:
        raise Refuse('PIN_ARG_FORMAT %s' % label)
    p, h = s.rsplit('=', 1)
    return p, h


def write_x(path, data, label='output'):
    path_policy(path, must_exist=False, label=label)
    b = data.encode('utf-8') if isinstance(data, str) else data
    with open(path, 'xb') as f:
        f.write(b)
    got = sha_bytes(read_nofollow(path, label))
    if got != sha_bytes(b):
        raise Refuse('WRITE_VERIFY_FAILED %s' % path)
    return {'path': path, 'sha256': got}


def dumps(obj):
    return json.dumps(obj, indent=1, ensure_ascii=False, allow_nan=False) + '\n'


def no_pending(obj, where='$'):
    out = []
    if isinstance(obj, str):
        if 'PENDING' in obj.upper():
            out.append(where)
    elif isinstance(obj, dict):
        for k, v in obj.items():
            out += no_pending(v, '%s.%s' % (where, k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out += no_pending(v, '%s[%d]' % (where, i))
    elif obj is None:
        out.append(where + ' (null)')
    return out


# ------------------------------------------------------------------------------------------------ subcommands
def c_pin(a):
    for s in a.pin:
        p, h = pinref(s, 'pin')
        pin(p, h, 'pin')
    return {'pins_verified': len(a.pin)}


def c_absent(a):
    for p in a.path:
        path_policy(p, must_exist=False, label='absent')
    return {'absent_verified': len(a.path)}


def c_freeze(a):
    """B1 / step 1 (A106; 0643 A): exclusive byte copy of the FINAL V005 addendum. BEFORE copying, the open bytes must hash to exactly
    the pinned final sha and have exactly the pinned length; the copy is created exclusively and re-read (no-follow) and re-hashed."""
    if not a.out.endswith('_V005_ADDENDUM_FROZEN.md'):
        raise Refuse('FROZEN_NAME (0576: ..._V005_ADDENDUM_FROZEN.md)')
    n = _digits(a.open_bytes, 'open-bytes')
    b = pin(a.open, a.open_sha, 'open_v005')
    if len(b) != n:
        raise Refuse('OPEN_V005_LENGTH %d != %d (A106: the FINAL V005 bytes; nothing was copied)' % (len(b), n))
    ref = write_x(a.out, b, 'frozen')
    copy = read_nofollow(a.out, 'frozen (re-hash)')
    if sha_bytes(copy) != a.open_sha or len(copy) != n or ref['sha256'] != a.open_sha:
        raise Refuse('FROZEN_COPY_REHASH_DIFFERS')
    if sha_bytes(read_nofollow(a.open, 'open_v005 (after the copy)')) != a.open_sha:
        raise Refuse('OPEN_V005_CHANGED_DURING_FREEZE')
    return {'frozen': ref, 'bytes': len(b), 'final_v005': {'sha256': a.open_sha, 'bytes': n}}


def c_same(a):
    """the open V005 file still has the frozen bytes (A82: root writes nothing to it after the freeze)."""
    fb = pin(a.frozen, a.frozen_sha, 'frozen')
    ob = read_nofollow(a.open, 'open_v005')
    if sha_bytes(ob) != sha_bytes(fb):
        raise Refuse('OPEN_V005_DIFFERS_FROM_FROZEN (A82/A99.6: a write to the open V005 after the freeze breaks the sealed compare)')
    return {'open_equals_frozen': True}


def _sections(b):
    starts = [0] + [m.end() for m in re.finditer(b'\n', b)]
    heads = [s for s in starts if s < len(b) and b.startswith(b'## ', s)]
    return heads


def _table_state(prereg_bytes, fb):
    """(rows, changed_rows, newest_row_number, entries_after_table, heading_counts) from the prereg's entries_after_A81 table and the
    frozen bytes (r5 entries_after_A81.section_rule)."""
    doc = sjson(prereg_bytes)
    rows = (doc.get('entries_after_A81') or {}).get('rows') or []
    if not rows:
        raise Refuse('NO_ENTRY_TABLE')
    heads = _sections(fb)
    changed, bad = [], []
    for r in rows:
        tag = ('## %s:' % r['entry']).encode()
        hs = [s for s in heads if fb.startswith(tag, s)]
        if len(hs) != 1:
            bad.append('%s heading count %d' % (r['entry'], len(hs)))
            continue
        nxt = [h for h in heads if h > hs[0]]
        sec = fb[hs[0]:(nxt[0] if nxt else len(fb))]
        if sha_bytes(sec) != r['section_sha256'] or len(sec) != r['section_bytes']:
            changed.append({'entry': r['entry'], 'row_sha256': r['section_sha256'], 'frozen_section_sha256': sha_bytes(sec)})
    newest = max(int(r['entry'][1:]) for r in rows)
    allh = [int(m.group(1)) for m in re.finditer(rb'^## A(\d{1,3}):', fb, re.M)]
    dup = sorted({n for n in allh if allh.count(n) > 1})
    if dup:
        bad.append('duplicate headings %s' % ['A%d' % n for n in dup])
    later = sorted(n for n in set(allh) if n > newest)
    if bad:
        raise Refuse('ENTRY_TABLE: ' + '; '.join(bad))
    return rows, changed, newest, later


def _section(fb, entry):
    heads = _sections(fb)
    tag = ('## %s:' % entry).encode()
    hs = [s for s in heads if fb.startswith(tag, s)]
    if len(hs) != 1:
        return None
    nxt = [x for x in heads if x > hs[0]]
    return fb[hs[0]:(nxt[0] if nxt else len(fb))]


DISPOSITIONS_SCHEMA = 'UNT_V007_LATER_ENTRY_DISPOSITIONS_C4V001'   # v003 dev seal_common_c4v003.py L24 (work copy); PENDING v003 final
DISPOSITIONS_KEYS = {'schema', 'frozen_addendum_sha256', 'entries'}    # v003 dev check_frozen_addendum_c4v003.py L43; 0640
LATER_VALUES = ('revised', 'no_change')                                 # an entry after the prereg's table (no old bytes)
CHANGED_VALUES = ('revised', 'no_change_after_change')                  # PV-D05-1 (0640): a cited entry whose bytes changed
ROW_KEYS_LATER = {'entry', 'disposition', 'section_sha256', 'reason'}
ROW_KEYS_CHANGED = {'entry', 'disposition', 'section_sha256', 'reason', 'change', 'prereg_revision', 'changed_text', 'why_no_prereg_effect'}
SRC_RX = re.compile(r'^A(\d{1,3})(?![\d])')
RANGE_RX = re.compile(r'\bA(\d{1,3})-A(\d{1,3})\b')


def _cited(doc):
    """the A-entries the prereg cites: its structured 'sources' lists and its cites_by_name ranges (tool 1's rule, v001 L18-L40)."""
    out = set()

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == 'sources' and isinstance(v, list):
                    for s in v:
                        if isinstance(s, str):
                            m = SRC_RX.match(s)
                            if m:
                                out.add(int(m.group(1)))
                            for x, y in RANGE_RX.findall(s):
                                out.update(range(int(x), int(y) + 1))
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(doc)
    for s in doc.get('cites_by_name', []) or []:
        for x, y in RANGE_RX.findall(s):
            out.update(range(int(x), int(y) + 1))
    return out


def _dispositions(a):
    """SA-CX1-B3 / PV-D05-1 pre-check of root's dispositions file (the v003 object only). Required rows: every frozen entry after the
    prereg's last cited entry ('later'), and every cited V005 entry (>= A47) whose section bytes differ from the bytes the prereg's
    table was read from ('changed'); no other row. A changed table row must also re-hash, in those table bytes, to its section_sha256."""
    raw = pin(a.dispositions, a.dispositions_sha, 'dispositions')
    d = sjson(raw)
    if isinstance(d, list):
        raise Refuse('DISPOSITIONS_LEGACY_BARE_LIST_REFUSED (0640: only the v003 object {schema, frozen_addendum_sha256, entries})')
    if not isinstance(d, dict):
        raise Refuse('DISPOSITIONS_SHAPE')
    for legacy in ('dispositions', 'rows'):
        if legacy in d:
            raise Refuse('DISPOSITIONS_LEGACY_KEY_REFUSED %r (0640)' % legacy)
    if set(d) != DISPOSITIONS_KEYS:
        raise Refuse('DISPOSITIONS_KEYS %r (exactly %s)' % (sorted(d), sorted(DISPOSITIONS_KEYS)))
    if d['schema'] != DISPOSITIONS_SCHEMA:
        raise Refuse('DISPOSITIONS_SCHEMA %r' % (d['schema'],))
    if d['frozen_addendum_sha256'] != a.frozen_sha:
        raise Refuse('DISPOSITIONS_FROZEN_SHA (the file names another frozen copy)')
    lst = d['entries']
    if not isinstance(lst, list):
        raise Refuse('DISPOSITIONS_ENTRIES_SHAPE')
    doc = sjson(pin(a.prereg, a.prereg_sha, 'prereg_text_of_record'))
    fb = pin(a.frozen, a.frozen_sha, 'frozen')
    tb = pin(a.table_bytes, a.table_bytes_sha, 'table_bytes')
    ar = (doc.get('entries_after_A81') or {}).get('addendum_read') or {}
    if ar.get('sha256_at_generation') != a.table_bytes_sha:
        raise Refuse('TABLE_BYTES_NOT_THE_PREREG_TABLE_SOURCE (entries_after_A81.addendum_read.sha256_at_generation)')
    rows, changed_rows, newest, later = _table_state(json.dumps(doc).encode('utf-8'), tb)   # every table row re-hashes in its own bytes
    if changed_rows:
        raise Refuse('TABLE_BYTES_DO_NOT_REHASH %r' % changed_rows)
    cited = _cited(doc)
    last = max(cited)
    changed = {}
    for n in sorted(x for x in cited if x >= 47):
        new_s, old_s = _section(fb, 'A%d' % n), _section(tb, 'A%d' % n)
        if new_s is None:
            raise Refuse('CITED_ENTRY_ABSENT_FROM_FROZEN A%d' % n)
        if old_s is None:
            raise Refuse('CITED_ENTRY_ABSENT_FROM_TABLE_BYTES A%d' % n)
        if new_s != old_s:
            changed['A%d' % n] = (old_s, new_s)
    heads = [int(m.group(1)) for m in re.finditer(rb'^## A(\d{1,3}):', fb, re.M)]
    later_e = ['A%d' % n for n in sorted(set(heads)) if n > last]
    seen = {}
    for i, e in enumerate(lst):
        w = 'entries[%d]' % i
        if not isinstance(e, dict):
            raise Refuse('DISPOSITION_ROW_NOT_AN_OBJECT %s: %r' % (w, e))
        ent = e.get('entry')
        if not (isinstance(ent, str) and re.fullmatch(r'A[1-9]\d{0,2}', ent)):
            raise Refuse('DISPOSITION_ENTRY %s: %r' % (w, ent))
        if ent in seen:
            raise Refuse('DISPOSITION_DUPLICATE %s' % ent)
        sec = _section(fb, ent)
        if sec is None:
            raise Refuse('DISPOSITION_ENTRY_NOT_IN_FROZEN %s' % ent)
        if e.get('section_sha256') != sha_bytes(sec):
            raise Refuse('DISPOSITION_WRONG_SECTION_SHA %s' % ent)
        disp = e.get('disposition')
        if ent in changed:
            if not set(e) <= ROW_KEYS_CHANGED:
                raise Refuse('DISPOSITION_ROW_KEYS %s %r' % (ent, sorted(set(e) - ROW_KEYS_CHANGED)))
            if disp == 'no_change':
                raise Refuse('DISPOSITION_NO_CHANGE_ON_CHANGED_ENTRY %s (PV-D05-1: revised, or no_change_after_change)' % ent)
            if disp not in CHANGED_VALUES:
                raise Refuse('DISPOSITION_VALUE %s: %r' % (ent, disp))
            old_s, new_s = changed[ent]
            if disp == 'revised':
                if not (isinstance(e.get('prereg_revision'), str) and e['prereg_revision'].strip()):
                    raise Refuse('DISPOSITION_REVISED_NEEDS_PREREG_REVISION_POINTER %s' % ent)
            else:
                ct, why = e.get('changed_text'), e.get('why_no_prereg_effect')
                if not (isinstance(ct, str) and ct.strip()):
                    raise Refuse('DISPOSITION_CHANGED_TEXT_EMPTY %s' % ent)
                cb = ct.encode('utf-8')
                if cb not in new_s:
                    raise Refuse('DISPOSITION_CHANGED_TEXT_NOT_IN_NEW_BYTES %s' % ent)
                if cb in old_s:
                    raise Refuse('DISPOSITION_CHANGED_TEXT_IN_OLD_BYTES %s (generic or unchanged text does not name the change)' % ent)
                if not (isinstance(why, str) and why.strip()):
                    raise Refuse('DISPOSITION_WHY_NO_PREREG_EFFECT_EMPTY %s' % ent)
            ch = e.get('change')
            if ch is not None:
                tr = next((r for r in rows if r['entry'] == ent), None)
                if not (isinstance(ch, dict) and str(ch.get('what_changed', '')).strip() and ch.get('to_section_sha256') == sha_bytes(new_s)
                        and ch.get('from_section_sha256') == (tr['section_sha256'] if tr else sha_bytes(old_s))):
                    raise Refuse('DISPOSITION_CHANGE_OBJECT %s' % ent)
        elif ent in later_e:
            if set(e) != ROW_KEYS_LATER:
                raise Refuse('DISPOSITION_ROW_KEYS %s %r (exactly %s for an entry after the table)' % (ent, sorted(e), sorted(ROW_KEYS_LATER)))
            if disp not in LATER_VALUES:
                raise Refuse('DISPOSITION_VALUE %s: %r' % (ent, disp))
            if not (isinstance(e.get('reason'), str) and e['reason'].strip()):
                raise Refuse('DISPOSITION_EMPTY_REASON %s' % ent)
        else:
            raise Refuse('DISPOSITION_FOR_UNCHANGED_CITED_OR_TABLED_ENTRY %s (one decision per entry, A99.3)' % ent)
        seen[ent] = e
    want = sorted(set(later_e) | set(changed), key=lambda x: int(x[1:]))
    have = sorted(seen, key=lambda x: int(x[1:]))
    if have != want:
        raise Refuse('DISPOSITION_ENTRIES %s must be exactly the entries after A%d %s plus the changed cited entries %s'
                     % (have, last, later_e, sorted(changed, key=lambda x: int(x[1:]))))
    return {'dispositions': {'path': a.dispositions, 'sha256': a.dispositions_sha}, 'schema': d['schema'], 'entries': have,
            'later_entries': later_e, 'changed_cited_entries': sorted(changed, key=lambda x: int(x[1:])),
            'covered_later_names_for_v001_placeholders_only': ','.join(later_e), 'table_rows_rehashed_in_table_bytes': len(rows),
            'v003_key_names': 'schema / frozen_addendum_sha256 / entries / entry / disposition / reason / section_sha256 from v003 dev; '
                              'prereg_revision, changed_text, why_no_prereg_effect, no_change_after_change from 0640 (PENDING v003 final)'}


def c_dispositions(a):
    return _dispositions(a)


def c_rehash(a):
    """r5 seal_record_requirements[11] / entries_after_A81.section_rule: every table row re-hashes from the FROZEN bytes, or the
    dispositions file carries its changed-entry row (PV-D05-1); every entry after the table carries a row."""
    res = _dispositions(a)
    rows, changed, newest, later = _table_state(pin(a.prereg, a.prereg_sha, 'prereg_text_of_record'), pin(a.frozen, a.frozen_sha, 'frozen'))
    missing = [c['entry'] for c in changed if c['entry'] not in res['changed_cited_entries']]
    if missing:
        raise Refuse('CHANGED_TABLE_ROW_WITHOUT_DISPOSITION %r' % missing)
    return {'table_rows_checked': len(rows), 'table_rows_unchanged_in_frozen': len(rows) - len(changed), 'changed_table_rows': changed,
            'entries_after_table': ['A%d' % n for n in later], 'dispositions': res}


def load_pinned(path, sha, name):
    """SA-CX1-B2: read the source ONCE (no-follow), check its sha256, compile EXACTLY that buffer and exec it into a fresh module.
    No importlib loader and no bytecode cache are involved, so a stale or planted .pyc beside the source can never run."""
    buf = pin(path, sha, name)
    code = compile(buf, path, 'exec', dont_inherit=True)
    m = types.ModuleType(name)
    m.__file__ = path
    sys.modules[name] = m
    exec(code, m.__dict__)
    return m


def _exec_module(path, sha, name):
    return load_pinned(path, sha, name)


def _fence(a, write_roots, forbid_runs_ext=True):
    import numpy                 # imported unfenced, before arming: the compare's own 'import numpy' then reuses this module
    F = load_pinned(a.fence, a.fence_sha, 'fence_c3sa_loaded')       # SA-CX1-B2: the verified buffer itself, never a loader
    if not forbid_runs_ext:      # ROOT gates-only: the identity-run trees under runs_ext are read by root's B6; C5H stays refused
        F._FORBID_SUBSTR = tuple(x for x in F._FORBID_SUBSTR if x not in ('/runs_ext', 'runs_ext/', '/uvt_'))
    F.arm(write_roots=write_roots)
    nr, n = F.selftest()
    # posixpath.realpath (non-strict) swallows the fence's PermissionError (an OSError): the syscall is still never made and the
    # refusal is counted, so 'realpath_c5h' returns normally in both modes. In ROOT mode the runs_ext/UVT_* probes are allowed by
    # design (fake nonexistent paths: FileNotFoundError, or False / None for access and the audit-only probes).
    expect = ['realpath_c5h'] if forbid_runs_ext else ['access_uvt', 'listdir_audit', 'lstat_uvt:FileNotFoundError',
                                                       'readlink_runs_ext:FileNotFoundError', 'realpath_c5h', 'scandir_audit']
    expect = sorted(expect)
    if sorted(nr) != expect:
        raise Refuse('FENCE_SELFTEST %r (expected not-refused %r)' % (nr, expect))
    return F


def c_driver_build(a):
    """B2a / step 2a: the r5 driver BUILD record = the reviewed compare's builtin_r5_build() with check_record = the ruled check
    record; validated by the compare's own driver_build_codes + r5_custody_codes before and after the exclusive write."""
    path_policy(a.out, must_exist=False, label='driver_build_record')
    pin(a.check_record, a.check_sha, 'check_record')
    F = _fence(a, write_roots=(os.path.dirname(a.out),))
    M = _exec_module(a.compare, a.compare_sha, 'reviewed_compare_c3sa')
    rec = M.builtin_r5_build()
    rec['check_record'] = {'path': a.check_record, 'sha256': a.check_sha}
    rec['note'] = ('r5 driver BUILD record (SEAL_CHECKLIST_R5 B2a; A72; A82; seal_record_requirements[8]): %s builtin_r5_build() '
                   'with check_record = the driver check record of record; written at seal assembly by ROOT_SEAL_STEPS.sh step 2a.'
                   % os.path.basename(a.compare))
    why = list(M.driver_build_codes(rec)) + list(M.r5_custody_codes())
    if why:
        raise Refuse('DRIVER_BUILD_CODES %r' % why)
    ref = write_x(a.out, dumps(rec), 'driver_build_record')
    obj, s2 = M.load_driver_build_record(ref['path'], ref['sha256'])
    M.activate_driver_build(obj)
    if F.FENCE['refused']:
        raise Refuse('FENCE_REFUSED %r' % F.FENCE['events'])
    return {'driver_build_record': ref, 'driver': rec['driver'], 'check_record': rec['check_record'], 'fence_refused': 0}


def c_check_driver_build(a):
    """B2a / step 2a (v003): v003 tool 5 printed the driver BUILD record and the script wrote it exclusively; these exact bytes must be
    the reviewed compare's builtin_r5_build() with check_record = the ruled check record, byte-equal to tool 5's own form (json indent 1,
    sorted keys, trailing newline), and pass the compare's own driver_build_codes and r5_custody_codes (fenced; the compare read once)."""
    b = pin(a.record, a.record_sha, 'driver_build_record')
    pin(a.check_record, a.check_sha, 'check_record')
    F = _fence(a, write_roots=())
    M = load_pinned(a.compare, a.compare_sha, 'reviewed_compare_c3sa')
    want = M.builtin_r5_build()
    want['check_record'] = {'path': a.check_record, 'sha256': a.check_sha}
    if b != (json.dumps(want, indent=1, sort_keys=True) + '\n').encode('utf-8'):
        raise Refuse('DRIVER_BUILD_RECORD_NOT_THE_TOOL5_FORM (not byte-equal to builtin_r5_build() + check_record, indent 1, sorted keys)')
    rec = sjson(b)
    why = list(M.driver_build_codes(rec)) + list(M.r5_custody_codes())
    if why:
        raise Refuse('DRIVER_BUILD_CODES %r' % why)
    obj, _ = M.load_driver_build_record(a.record, a.record_sha)
    M.activate_driver_build(obj)
    if F.FENCE['refused']:
        raise Refuse('FENCE_REFUSED %r' % F.FENCE['events'])
    return {'driver_build_record': {'path': a.record, 'sha256': a.record_sha}, 'driver': rec['driver'], 'check_record': rec['check_record'],
            'byte_equal_to_the_tool5_form': True, 'fence_refused': 0}


def c_check_disclosures(a):
    """A110/A111 (0646, 0647): root's SEAL_MANUAL_DISCLOSURES_V001 file, read ONCE by pin() and parsed strictly from that buffer with the
    c3v013 SELECTED-strictness rules (typed DISCLOSURES_* codes: invalid UTF-8, BOM, depth, duplicate key, NaN / Infinity / overflow, an
    integer over 4300 digits, trailing text, a non-object top level). Its form: exactly {schema, e_r6_1_text, c08_table, c08_confirmation,
    root_disclosures}; e_r6_1_text non-empty and byte-equal to r6's SELECTED basis.erratum_E_R6_1 (r6's SELECTED read the same way);
    c08_table rows exactly {new_item_id NEW-<n>, file, line (int > 0), declared_in_r13 (bool)}, ids unique; c08_confirmation non-empty;
    root_disclosures entries exactly {id, source, text}, all non-empty, ids unique. The CONTENT is not checked against the A-entries here
    (the coordinator does that); tool 4 v004 carries the file verbatim into the SEAL_RECORD."""
    def strict(b, label):
        try:
            return _selected_strict(b)
        except Refuse as e:
            raise Refuse(str(e).replace('SELECTED_', 'DISCLOSURES_' if label == 'disclosures' else 'R6_SELECTED_', 1))
    d = strict(pin(a.disclosures, a.disclosures_sha, 'manual_disclosures'), 'disclosures')
    want = {'schema', 'e_r6_1_text', 'c08_table', 'c08_confirmation', 'root_disclosures'}
    if set(d) != want:
        raise Refuse('DISCLOSURES_KEYS %r (want exactly %r)' % (sorted(d), sorted(want)))
    if d['schema'] != 'SEAL_MANUAL_DISCLOSURES_V001':
        raise Refuse('DISCLOSURES_SCHEMA %r' % d['schema'])
    e = d['e_r6_1_text']
    if not (isinstance(e, str) and e.strip()):
        raise Refuse('DISCLOSURES_E_R6_1_TEXT_EMPTY')
    r6 = strict(pin(a.r6_selected, a.r6_selected_sha, 'r6_selected'), 'r6')
    if r6.get('schema') != a.r6_schema:
        raise Refuse('R6_SELECTED_SCHEMA_MISMATCH %r' % r6.get('schema'))
    ref = (r6.get('basis') or {}).get('erratum_E_R6_1') if isinstance(r6.get('basis'), dict) else None
    if not isinstance(ref, str) or e.encode('utf-8') != ref.encode('utf-8'):
        raise Refuse('DISCLOSURES_E_R6_1_TEXT_NOT_BYTE_EQUAL_TO_R6_SELECTED (A110: exactly basis.erratum_E_R6_1)')
    rows = d['c08_table']
    if not (isinstance(rows, list) and rows):
        raise Refuse('DISCLOSURES_C08_TABLE_EMPTY_OR_NOT_A_LIST')
    seen = set()
    for j, r in enumerate(rows):
        if not (isinstance(r, dict) and set(r) == {'new_item_id', 'file', 'line', 'declared_in_r13'} and isinstance(r['new_item_id'], str)
                and re.fullmatch(r'NEW-\d{1,3}', r['new_item_id']) and isinstance(r['file'], str) and r['file'].strip()
                and type(r['line']) is int and r['line'] > 0 and type(r['declared_in_r13']) is bool):
            raise Refuse('DISCLOSURES_C08_ROW_FORM c08_table[%d]' % j)
        if r['new_item_id'] in seen:
            raise Refuse('DISCLOSURES_C08_DUPLICATE_ID %s' % r['new_item_id'])
        seen.add(r['new_item_id'])
    if not (isinstance(d['c08_confirmation'], str) and d['c08_confirmation'].strip()):
        raise Refuse('DISCLOSURES_C08_CONFIRMATION_EMPTY')
    rd = d['root_disclosures']
    if not (isinstance(rd, list) and rd):
        raise Refuse('DISCLOSURES_ROOT_DISCLOSURES_EMPTY_OR_NOT_A_LIST')
    ids = set()
    for j, x in enumerate(rd):
        if not (isinstance(x, dict) and set(x) == {'id', 'source', 'text'} and all(isinstance(x[k], str) and x[k].strip() for k in ('id', 'source', 'text'))):
            raise Refuse('DISCLOSURES_ROOT_DISCLOSURE_FORM root_disclosures[%d]' % j)
        if x['id'] in ids:
            raise Refuse('DISCLOSURES_ROOT_DISCLOSURE_DUPLICATE_ID %s' % x['id'])
        ids.add(x['id'])
    return {'manual_disclosures': {'path': a.disclosures, 'sha256': a.disclosures_sha, 'schema': d['schema'], 'c08_rows': len(rows),
            'root_disclosure_ids': sorted(ids), 'e_r6_1_text_byte_equal_to_r6_selected': True},
            'scope': 'form and the E_R6_1 byte equality only; the content is not cross-checked against the A-entries here'}


def c_fill(a):
    """step 3a: SLOT_VALUES_FINAL = the draft with every PENDING marker replaced: run-time pins (KEY=PATH=SHA, each path equal to
    the expected path the script gives) and root rulings (ITEM=SHA, each equal to the draft's single named candidate)."""
    draft = sjson(pin(a.draft, a.draft_sha, 'draft'))
    if tuple(draft) != SLOT_KEYS and set(draft) != set(SLOT_KEYS):
        raise Refuse('DRAFT_SLOT_KEYS %r' % list(draft))
    rt = {}
    for s in a.runtime:
        k, rest = s.split('=', 1)
        p, h = rest.rsplit('=', 1)
        rt[k] = (p, h)
    exp = dict(x.split('=', 1) for x in a.expect)
    rul = dict(x.split('=', 1) for x in a.ruling)
    used_rt, used_rul, notes = set(), set(), []

    def fill(v, where):
        if isinstance(v, dict) and set(v) == {'path', 'sha256'} and isinstance(v['sha256'], str):
            h = v['sha256']
            if h.startswith(MARK_ROOT):
                key = h[len(MARK_ROOT):].split(':', 1)[0]
                if key not in rt or key not in exp:
                    raise Refuse('RUNTIME_PIN_MISSING %s (%s)' % (key, where))
                p, s = rt[key]
                if p != exp[key]:
                    raise Refuse('RUNTIME_PATH_NOT_EXPECTED %s: %s vs %s' % (key, p, exp[key]))
                if v['path'] != p:
                    notes.append('%s: draft documents %s; this run uses %s' % (where, v['path'], p))
                pin(p, s, where)
                used_rt.add(key)
                return {'path': p, 'sha256': s}
            if h.startswith(MARK_RULING):
                parts = h[len(MARK_RULING):].split(':')
                item = parts[0]
                cand = parts[2] if len(parts) >= 3 and parts[1] == 'CANDIDATE' else None
                if item in rt:                         # a root-supplied input (the compare: path and sha given at invocation)
                    p, s = rt[item]
                    pin(p, s, where)
                    if cand and s != cand:
                        raise Refuse('RULING_INPUT_NOT_THE_NAMED_CANDIDATE %s' % item)
                    used_rt.add(item)
                    return {'path': p, 'sha256': s}
                if item not in rul:
                    raise Refuse('ROOT_RULING_MISSING %s (%s): set UNT_SEAL_RULING_%s=<full sha of the ruled record>' % (item, where, item))
                if cand is None or rul[item] != cand:
                    raise Refuse('ROOT_RULING_NOT_THE_DRAFT_CANDIDATE %s: %s (draft candidate %s); a different record needs a '
                                 'successor SLOT_VALUES_DRAFT' % (item, rul[item], cand))
                pin(v['path'], cand, where)
                used_rul.add(item)
                return {'path': v['path'], 'sha256': cand}
            pin(v['path'], h, where)
            return dict(v)
        if isinstance(v, dict):
            return {k: fill(x, '%s.%s' % (where, k)) for k, x in v.items()}
        return v
    out = {k: (fill(v, k) if k not in ('schema', 'driver_branch', 'ngc_gas_M_s', 'cache_directory_r6_only') else v) for k, v in draft.items()}
    left = no_pending({k: v for k, v in out.items() if k != 'cache_directory_r6_only'})
    if left:
        raise Refuse('PENDING_LEFT %r' % left)
    if set(rt) - used_rt or set(rul) - used_rul:
        raise Refuse('UNUSED_INPUTS runtime %r rulings %r' % (sorted(set(rt) - used_rt), sorted(set(rul) - used_rul)))
    if out['driver_branch'] != 'r5' or out['cache_directory_r6_only'] != 'NOT_APPLICABLE_R5' or out['ngc_gas_M_s'] != 96:
        raise Refuse('BRANCH_CACHE_MS (A96: r5, NOT_APPLICABLE_R5; ngc_gas_M_s 96 per production_tail.ngc_gas_M_s)')
    ref = write_x(a.out, dumps(out), 'slots_final')
    return {'slots_final': ref, 'runtime_filled': sorted(used_rt), 'rulings_applied': sorted(used_rul), 'notes': notes}


def c_sealed_prereg(a):
    """B4 / step 4: the text of record with each seal_slots.<k>.value replaced by the slot value; nothing else changes."""
    tb = pin(a.text_of_record, a.tor_sha, 'text_of_record')
    doc = sjson(tb)
    slots = sjson(pin(a.slots, a.slots_sha, 'slots_final'))
    ss = doc.get('seal_slots')
    if not isinstance(ss, dict) or set(ss) != set(PREREG_SLOT_OF):
        raise Refuse('PREREG_SEAL_SLOTS_KEYS %r' % (list(ss) if isinstance(ss, dict) else ss))
    for pk, sk in PREREG_SLOT_OF.items():
        if 'value' not in ss[pk]:
            raise Refuse('PREREG_SLOT_HAS_NO_VALUE %s' % pk)
        ss[pk]['value'] = slots[sk]
    ref = write_x(a.out, dumps(doc), 'sealed_prereg')
    back, orig = sjson(Path(ref['path']).read_bytes()), sjson(tb)
    for pk, sk in PREREG_SLOT_OF.items():
        if back['seal_slots'][pk]['value'] != slots[sk]:
            raise Refuse('SEALED_SLOT_READBACK %s' % pk)
        back['seal_slots'][pk]['value'] = orig['seal_slots'][pk]['value'] = '<SLOT>'
    if back != orig:
        raise Refuse('SEALED_PREREG_DIFFERS_OUTSIDE_SLOT_VALUES')
    return {'sealed_prereg': ref}


def _pin_lines(src_lines):
    found = {}
    for i, ln in enumerate(src_lines):
        for n in PIN_NAMES:
            if ln.startswith(n + ' = ') or ln.startswith(n + '='):
                found.setdefault(n, []).append(i)
    return found


def c_sealed_compare(a):
    """B5 / step 5: the reviewed compare with exactly the five seal-time pin lines set (A82); every other byte identical."""
    rb = pin(a.reviewed, a.reviewed_sha, 'compare_reviewed_source')
    slots = sjson(pin(a.slots, a.slots_sha, 'slots_final'))
    pin(a.sealed_prereg, a.sealed_prereg_sha, 'sealed_prereg')
    if slots['compare_reviewed_source'] != {'path': a.reviewed, 'sha256': a.reviewed_sha}:
        raise Refuse('REVIEWED_SOURCE_NOT_THE_SLOT')
    text = rb.decode('utf-8')
    lines = text.splitlines(keepends=True)
    found = _pin_lines(lines)
    tree = ast.parse(text)
    want = {'V007_PREREG_SHA256': a.sealed_prereg_sha, 'PIN_ADDENDUM_V005': slots['frozen_addendum']['sha256'],
            'PIN_DRIVER_BUILD_RECORD': (slots['driver_build_record']['path'], slots['driver_build_record']['sha256']),
            'PIN_V010_R5_CHECK': (slots['driver_check_record']['path'], slots['driver_check_record']['sha256']),
            'PIN_PRODUCER_REGISTRY': (slots['producer_registry']['path'], slots['producer_registry']['sha256'])}
    cnt = {n: 0 for n in PIN_NAMES}
    for node in ast.walk(tree):
        tg = node.targets if isinstance(node, ast.Assign) else ([node.target] if isinstance(node, (ast.AnnAssign, ast.AugAssign)) else [])
        for t in tg:
            for sub in ast.walk(t):
                if isinstance(sub, ast.Name) and sub.id in cnt:
                    cnt[sub.id] += 1
        if isinstance(node, ast.Global) and any(n in cnt for n in node.names):
            raise Refuse('GLOBAL_PIN_REBIND')
    new = list(lines)
    for n in PIN_NAMES:
        if len(found.get(n, [])) != 1 or cnt[n] != 1:
            raise Refuse('PIN_LINE_NOT_UNIQUE %s lines %r assignments %d' % (n, found.get(n), cnt[n]))
        i = found[n][0]
        m = re.match(r'^%s = None(?=\s|$)' % n, lines[i])
        if not m:
            raise Refuse('REVIEWED_PIN_NOT_UNSET %s: %r' % (n, lines[i][:80]))
        lit = repr(want[n])
        if n in SHA_PINS and not HEX64.fullmatch(want[n]):
            raise Refuse('PIN_SHA_FORMAT %s' % n)
        new[i] = '%s = %s%s' % (n, lit, lines[i][m.end():])
        if ast.literal_eval(lit) != want[n]:
            raise Refuse('PIN_LITERAL %s' % n)
    out = ''.join(new)
    ast.parse(out)
    diff = [i for i, (x, y) in enumerate(zip(lines, new)) if x != y]
    if len(new) != len(lines) or sorted(diff) != sorted(found[n][0] for n in PIN_NAMES):
        raise Refuse('DIFF_NOT_EXACTLY_THE_FIVE_PIN_LINES')
    ref = write_x(a.out, out, 'sealed_compare')
    return {'sealed_compare': ref, 'pin_lines_changed': [found[n][0] + 1 for n in PIN_NAMES]}


def _module_strings(text):
    tree = ast.parse(text)
    env = {}

    def ev(v):
        if isinstance(v, ast.Constant) and isinstance(v.value, str):
            return v.value
        if isinstance(v, ast.Name) and v.id in env and isinstance(env[v.id], str):
            return env[v.id]
        if isinstance(v, ast.BinOp) and isinstance(v.op, ast.Add):
            return ev(v.left) + ev(v.right)
        if isinstance(v, ast.Tuple):
            return tuple(ev(e) for e in v.elts)
        raise ValueError('not a string expression')
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            try:
                env[node.targets[0].id] = ev(node.value)
            except ValueError:
                pass
    return env


def _manifest_values(m):
    """every run-directory / record path string a manifest names (cases, identity_runs, gates, rpair members); the note is excluded."""
    out = []
    for key in ('cases', 'identity_runs', 'gates'):
        out += [v for v in (m.get(key) or {}).values() if v is not None]
    for rp in (m.get('rpair') or {}).values():
        out += [v for v in ((rp or {}).get('members') or {}).values() if v is not None]
    return out


def c_check_manifest(a):
    """the step-8 (gates) or step-9 (C5H) manifest: schema of the sealed compare; gates-only names NO case (so step 8 never reads
    the C5H run) and, in ROOT mode, exactly the identity-run directories the identity records of record name."""
    cmp_text = pin(a.sealed_compare, a.sealed_compare_sha, 'sealed_compare').decode('utf-8')
    env = _module_strings(cmp_text)
    m = sjson(pin(a.manifest, a.manifest_sha, 'manifest'))
    vals = _manifest_values(m)
    if m.get('schema') != env.get('MANIFEST_SCHEMA'):
        raise Refuse('MANIFEST_SCHEMA %r vs compare %r' % (m.get('schema'), env.get('MANIFEST_SCHEMA')))
    flat = json.dumps(vals).casefold()            # path values only (cases, identity_runs, gates, rpair): never the note
    if a.mode in ('gates-root', 'gates-dryrun'):
        if m.get('cases') or m.get('rpair'):
            raise Refuse('GATES_MANIFEST_NAMES_A_CASE_OR_RPAIR (step 8 must not read C5H or any T-run)')
        if C5H_NAME_CF in flat:
            raise Refuse('GATES_MANIFEST_MENTIONS_C5H')
        for g, p in (m.get('gates') or {}).items():
            if p is not None:
                path_policy(p, must_exist=True, label='gate ' + g)
        ids = m.get('identity_runs') or {}
        if a.mode == 'gates-dryrun':
            if ids or '/runs_ext' in flat or '/uvt_' in flat:
                raise Refuse('DRYRUN_MANIFEST_NAMES_A_RUN_TREE')
        else:
            want = {}
            for s in a.identity_record:
                run, rest = s.split('=', 1)
                p, h = rest.rsplit('=', 1)
                want[run] = sjson(pin(p, h, 'identity record ' + run))['run']['path']
            if ids != want:
                raise Refuse('IDENTITY_RUNS_NOT_THE_RECORDS_RUN_PATHS %r vs %r' % (ids, want))
    elif a.mode == 'c5h':
        reg = env.get('C5H_REGISTERED_RUN_DIRS')
        if set(m) - {'schema', 'cases', 'identity_runs', 'gates', 'rpair', 'note'} or m.get('identity_runs') or m.get('rpair'):
            raise Refuse('C5H_MANIFEST_SHAPE')
        if list((m.get('cases') or {}).keys()) != ['C5H'] or not isinstance(reg, tuple) or m['cases']['C5H'] not in reg:
            raise Refuse('C5H_MANIFEST_CASE_NOT_A_REGISTERED_SPELLING')
        if set((m.get('gates') or {})) - {'B0', 'I1T'}:
            raise Refuse('C5H_MANIFEST_GATES (validity-only reads I1T and B0 only)')
    else:
        raise Refuse('MODE')
    return {'manifest': {'path': a.manifest, 'sha256': a.manifest_sha}, 'mode': a.mode}


def c_make_c5h_manifest(a):
    """step 9 input: {cases: {C5H: <root-supplied spelling, which must be one of the sealed compare's C5H_REGISTERED_RUN_DIRS>},
    gates: {B0}}; the C5H path is a string here: nothing stats or opens it."""
    cmp_text = pin(a.sealed_compare, a.sealed_compare_sha, 'sealed_compare').decode('utf-8')
    env = _module_strings(cmp_text)
    reg = env.get('C5H_REGISTERED_RUN_DIRS')
    if not isinstance(reg, tuple) or a.c5h_dir not in reg:
        raise Refuse('C5H_DIR_NOT_A_REGISTERED_SPELLING (string compare against the sealed compare C5H_REGISTERED_RUN_DIRS)')
    bp, bh = pinref(a.b0_record, 'b0')
    pin(bp, bh, 'B0 record')
    m = {'schema': env['MANIFEST_SCHEMA'], 'cases': {'C5H': a.c5h_dir}, 'identity_runs': {}, 'gates': {'B0': bp, 'I1T': None},
         'rpair': {}, 'note': 'ROOT step 9 manifest (ROOT_SEAL_STEPS.sh): --validity-only --case C5H reads the registered C5H run and '
                             'the B0 record only; I1T is produced after the seal.'}
    return {'manifest_c5h': write_x(a.out, dumps(m), 'manifest_c5h')}


def c_gates_only(a):
    """B6a / step 8: the SEALED compare --gates-only, in-process, behind a fence armed before the compare's bytes execute.
    ROOT mode: refuses only the registered C5H run, /.vol and NGC-target spellings (the identity-run trees are root's B6 input),
    and first scans the identity-run trees for symlinks (find -P semantics) so no read can be redirected into the C5H run.
    DRYRUN mode: also refuses every runs_ext/UVT_* path and redirects C5H_REGISTERED_RUN_DIRS to a stand-in."""
    pin(a.sealed_compare, a.sealed_compare_sha, 'sealed_compare')
    pin(a.sealed_prereg, a.sealed_prereg_sha, 'sealed_prereg')
    m = sjson(pin(a.manifest, a.manifest_sha, 'manifest'))
    path_policy(a.outdir, must_exist=False, label='outdir')
    if m.get('cases') or m.get('rpair') or C5H_NAME_CF in json.dumps(_manifest_values(m)).casefold():
        raise Refuse('GATES_MANIFEST_NAMES_A_CASE')
    scanned = 0
    if a.mode not in ('root', 'dryrun'):
        raise Refuse('MODE')
    if a.mode == 'dryrun':
        if m.get('identity_runs'):
            raise Refuse('DRYRUN_MANIFEST_NAMES_IDENTITY_RUNS')
        sst = path_policy(a.standin, must_exist=True, label='standin')
        if not stat_mod.S_ISDIR(sst.st_mode):
            raise Refuse('STANDIN_NOT_A_DIRECTORY')
    F = _fence(a, write_roots=(a.outdir,), forbid_runs_ext=(a.mode == 'dryrun'))     # armed before the scan and the compare
    if a.mode == 'root':
        for run, d in sorted((m.get('identity_runs') or {}).items()):
            if not (isinstance(d, str) and d.startswith('/') and C5H_NAME_CF not in d.casefold()):
                raise Refuse('IDENTITY_RUN_DIR %s spelling' % run)
            st = nofollow_walk(d, 'identity run ' + run, allow_run_trees=True)      # SA-CX1-B1: no component is followed
            if not stat_mod.S_ISDIR(st.st_mode):
                raise Refuse('IDENTITY_RUN_DIR %s not a real directory' % run)
            for side in (d + '.receipt.json', d + '.receipt.json.launch.json'):
                sst = nofollow_walk(side, 'identity run side file', final_may_be_absent=True, allow_run_trees=True)
                if sst is not None and not stat_mod.S_ISREG(sst.st_mode):
                    raise Refuse('IDENTITY_RUN_SIDE_FILE_NOT_A_REGULAR_FILE %s' % side)
            stack = [d]
            while stack:                                   # find -P semantics: nothing is followed, no symlink target is stat'ed
                cur = stack.pop()
                with os.scandir(cur) as it:
                    for e in it:
                        scanned += 1
                        if e.is_symlink():
                            raise Refuse('SYMLINK_INSIDE_IDENTITY_RUN %s' % e.path)
                        if e.is_dir(follow_symlinks=False):
                            stack.append(e.path)
    M = _exec_module(a.sealed_compare, a.sealed_compare_sha, 'sealed_compare_c3sa')
    if a.mode == 'dryrun':
        M.C5H_REGISTERED_RUN_DIRS = (a.standin,)          # redirected BEFORE main() runs; nothing ran yet except definitions
    rc = M.main(['--prereg', a.sealed_prereg, '--manifest', a.manifest, '--outdir', a.outdir, '--gates-only'])
    sys.stdout.flush()
    out = {'compare_rc': rc, 'fence_refused': F.FENCE['refused'], 'fence_events': F.FENCE['events'][:10], 'mode': a.mode,
           'identity_tree_entries_scanned': scanned, 'gates_only_json': None}
    gj = os.path.join(a.outdir, 'GATES_ONLY.json')
    gst = nofollow_walk(gj, 'GATES_ONLY.json', final_may_be_absent=True)
    if gst is not None and stat_mod.S_ISREG(gst.st_mode):
        out['gates_only_json'] = {'path': gj, 'sha256': sha_bytes(read_nofollow(gj, 'GATES_ONLY.json'))}
    if F.FENCE['refused'] or rc != 0 or out['gates_only_json'] is None:
        raise Refuse('GATES_ONLY_FAILED %r' % out)
    return out


def c_row_scan(a):
    t = read_nofollow(a.path, 'e_seal1').decode('utf-8')
    hit = ROW_VALUE_RX.search(t)
    if hit or not t.strip():
        raise Refuse('E_SEAL1_OUTPUT_EMPTY_OR_SHOWS_A_ROW_LIKE_VALUE (A47 I3)')
    return {'e_seal1': {'path': a.path, 'sha256': sha_bytes(t.encode('utf-8'))}, 'row_like_values': 0}


def c_check_tool4(a):
    st = read_nofollow(a.stderr, 'tool4_stderr').decode('utf-8')
    v = sjson(st.encode('utf-8'))
    ob = read_nofollow(a.stdout, 'tool4_stdout')
    if v.get('verdict') != 'PASS' or not ob or v.get('seal_record_sha256') != sha_bytes(ob):
        raise Refuse('TOOL4_NOT_PASS_OR_SHA_MISMATCH verdict %r stderr sha %r stdout sha %s' % (v.get('verdict'), v.get('seal_record_sha256'), sha_bytes(ob)))
    rec = sjson(ob)
    if rec.get('sealed_by') != AUTHORITY:
        raise Refuse('SEAL_RECORD_AUTHORITY')
    return {'candidate': {'path': a.stdout, 'sha256': sha_bytes(ob)}, 'tool4_seal_record_sha256': v['seal_record_sha256']}


def c_copy_x(a):
    b = pin(a.src, a.src_sha, 'src')
    return {'created': write_x(a.dst, b, 'dst')}


def _build_table(text):
    """W7-S1 (A105.1; A78 N2): BUILD_V007's '## Supported runtime entry allowlist' section, parsed strictly. The heading line occurs
    exactly once; the section runs to the next '## ' line; it holds exactly one ```text fence and only blank lines outside it; every
    line inside the fence is one row '<64 lowercase hex>  <absolute /Users path without whitespace>' (fullmatch); exactly 15 rows; no
    duplicate path and no duplicate sha. Returns the rows in table order as [(path, sha)]. Lines of the same form elsewhere in BUILD
    (the V006 writers 9fbdb0ca and 500f8b6a at L45-L46, the binder f3e4e2be at L54) are not rows of this table."""
    L = text.split('\n')
    at = [i for i, ln in enumerate(L) if ln == BUILD_HEADER]
    if len(at) != 1:
        raise Refuse('W7_BUILD_SECTION_HEADING_COUNT %d' % len(at))
    sec = []
    for ln in L[at[0] + 1:]:
        if ln.startswith('## '):
            break
        sec.append(ln)
    fences = [i for i, ln in enumerate(sec) if ln.startswith('```')]
    if len(fences) != 2 or sec[fences[0]] != '```text' or sec[fences[1]] != '```':
        raise Refuse('W7_BUILD_SECTION_FENCE_FORM')
    if any(ln.strip() for i, ln in enumerate(sec) if i < fences[0] or i > fences[1]):
        raise Refuse('W7_BUILD_SECTION_TEXT_OUTSIDE_THE_TABLE')
    rows = []
    for ln in sec[fences[0] + 1:fences[1]]:
        m = W7_ROW_RX.fullmatch(ln)
        if not m:
            raise Refuse('W7_BUILD_TABLE_LINE_NOT_A_ROW %r' % ln[:200])
        rows.append((m.group(2), m.group(1)))
    if len(rows) != W7_ROWS:
        raise Refuse('W7_BUILD_TABLE_COUNT %d (want exactly %d)' % (len(rows), W7_ROWS))
    if len({p for p, _ in rows}) != W7_ROWS or len({h for _, h in rows}) != W7_ROWS:
        raise Refuse('W7_BUILD_TABLE_DUPLICATE')
    return rows


def _check_allowlist(cfg, rows):
    """W7-S1: cfg['producer_allowlist'] is a JSON object of exactly 15 entries whose (path, sha) items are byte-equal to the BUILD_V007
    table rows, in table order. A duplicated row is a duplicate JSON key, which the strict parser (sjson) refuses before this check."""
    pa = cfg.get('producer_allowlist') if isinstance(cfg, dict) else None
    if not isinstance(pa, dict):
        raise Refuse('W7_ALLOWLIST_NOT_AN_OBJECT')
    items = list(pa.items())
    if len(items) != W7_ROWS:
        raise Refuse('W7_ALLOWLIST_COUNT %d (want exactly %d, the BUILD_V007 table)' % (len(items), W7_ROWS))
    table = dict(rows)
    for p, h in items:
        if p not in table:
            raise Refuse('W7_ALLOWLIST_ROW_NOT_IN_TABLE %r' % p)
        if h != table[p]:
            raise Refuse('W7_ALLOWLIST_ROW_SHA_NOT_BYTE_EQUAL %r' % p)
    if items != rows:
        raise Refuse('W7_ALLOWLIST_ORDER_DIFFERS_FROM_TABLE')
    return len(items)


def _check_config_bytes(b, build_text, build_pin):
    """W7-S1 on config BYTES: strict JSON (a duplicated row = a duplicate key refuses), the config pins this BUILD, the allowlist is
    exactly its table."""
    cfg = sjson(b)
    if not isinstance(cfg, dict) or cfg.get('build') != build_pin:
        raise Refuse('W7_CONFIG_BUILD_PIN_DIFFERS')
    return _check_allowlist(cfg, _build_table(build_text))


def c_make_config(a):
    """B8 / step 12: ROOT_SEAL_ADMISSION config (FORMAT_V005 item 2; guard v008 admission): schema, authority, seal, prereg and compare
    (exactly the SEAL_RECORD's), build (BUILD_V007), producer_allowlist = BUILD_V007's 15-row table EXACTLY, in table order (W7-S1,
    A105.1, A78 N2), which must also equal ALLOWLIST_DRAFT_V006_CX3V001.txt and PRODUCER_INDEX_V009_CX3V001.json as sets. The
    serialized bytes pass the W7-S1 check BEFORE the exclusive write and the written file passes it again; then the real guard v008
    admission() self-check."""
    seal = sjson(pin(a.seal, a.seal_sha, 'seal_record'))
    bt = pin(a.build, a.build_sha, 'build').decode('utf-8')
    build_pin = {'path': a.build, 'sha256': a.build_sha}
    rows = _build_table(bt)
    allow = dict(rows)
    al = {}
    for ln in pin(a.allowlist, a.allowlist_sha, 'allowlist_file').decode('utf-8').splitlines():
        if ln.strip():
            h, p = ln.split('  ', 1)
            if p in al:
                raise Refuse('ALLOWLIST_FILE_DUPLICATE')
            al[p] = h
    pi = sjson(pin(a.producer_index, a.producer_index_sha, 'producer_index'))
    pid = {}
    for e in pi['supported_entries']:
        if e['path'] in pid:
            raise Refuse('PRODUCER_INDEX_DUPLICATE')
        pid[e['path']] = e['sha256']
    if not (allow == al == pid) or len(allow) != W7_ROWS:
        raise Refuse('ALLOWLIST_SETS_DIFFER build %d file %d index %d (want %d)' % (len(allow), len(al), len(pid), W7_ROWS))
    for p, h in rows:
        pin(p, h, 'allowlisted source')
    if allow.get(a.launcher) != a.launcher_sha or allow.get(a.guard) != a.guard_sha:
        raise Refuse('LAUNCHER_OR_GUARD_NOT_ALLOWLISTED_BY_EXACT_PATH (A78 N2)')
    for k in ('prereg', 'compare', 'driver', 'frozen_addendum'):
        r = seal.get(k)
        if not (isinstance(r, dict) and set(r) == {'path', 'sha256'}):
            raise Refuse('SEAL_PIN_SHAPE %s' % k)
        pin(r['path'], r['sha256'], 'seal.' + k)
    if seal.get('sealed_by') != AUTHORITY:
        raise Refuse('SEAL_AUTHORITY')
    cfg = {'schema': CONFIG_SCHEMA, 'authority': dict(AUTHORITY), 'seal': {'path': a.seal, 'sha256': a.seal_sha},
           'prereg': dict(seal['prereg']), 'compare': dict(seal['compare']), 'build': dict(build_pin),
           'producer_allowlist': {p: h for p, h in rows}}
    data = dumps(cfg).encode('utf-8')
    n_rows = _check_config_bytes(data, bt, build_pin)            # W7-S1 on the exact bytes, BEFORE the exclusive write
    ref = write_x(a.out, data, 'config')
    _check_config_bytes(pin(ref['path'], ref['sha256'], 'config (written)'), bt, build_pin)   # and on the written file
    # self-check with the real guard v008 (read-only): its admission() reads CONFIG, the seal, prereg, compare, build and the 15
    # sources; it never touches REGISTERED (only check_run_path does, which is not called here).
    G = _exec_module(a.guard, a.guard_sha, 'producer_guard_c3sa')
    real_config = str(G.CONFIG)
    G.CONFIG = Path(ref['path'])
    if G.AUTHORITY != AUTHORITY or G.__file__ != a.guard:
        raise Refuse('GUARD_AUTHORITY_OR_PATH')
    os.environ['UNT_ROOT_ADMISSION_SHA256'] = ref['sha256']   # in-process self-check only; never exported to the shell
    cfg2 = G.admission(a.launcher)
    del os.environ['UNT_ROOT_ADMISSION_SHA256']
    if cfg2.get('_verified_seal') != seal or cfg2.get('_verified_config_sha256') != ref['sha256']:
        raise Refuse('GUARD_SELF_CHECK')
    return {'config': ref, 'config_is_guard_CONFIG': ref['path'] == real_config, 'guard_CONFIG': real_config,
            'guard_admission_self_check': 'PASS (in-process, UNT_ROOT_ADMISSION_SHA256 = this config sha; not the published-trust check)',
            'allowlist_sources': n_rows,
            'w7_s1': 'producer_allowlist = BUILD_V007 table rows 1-15 exactly, in table order; checked on the serialized bytes before '
                     'the exclusive write and on the written file after it'}


def c_check_config_allowlist(a):
    """W7-S1 re-check of a WRITTEN admission config, from its bytes, against BUILD_V007's table (step 12; the MUST_FAIL controls)."""
    b = pin(a.config, a.config_sha, 'config')
    bt = pin(a.build, a.build_sha, 'build').decode('utf-8')
    n = _check_config_bytes(b, bt, {'path': a.build, 'sha256': a.build_sha})
    return {'w7_s1_allowlist': {'rows': n, 'byte_equal_to_the_build_table_in_table_order': True,
                                'config': {'path': a.config, 'sha256': a.config_sha}, 'build': {'path': a.build, 'sha256': a.build_sha}}}


def _volume_dev():
    st = os.lstat(VOLUME_ROOT)
    if not stat_mod.S_ISDIR(st.st_mode):
        raise Refuse('VOLUME_ROOT_NOT_A_DIRECTORY %s' % VOLUME_ROOT)
    return st.st_dev


def _kind(st):
    m = st.st_mode
    return ('symlink' if stat_mod.S_ISLNK(m) else 'directory' if stat_mod.S_ISDIR(m) else 'regular file' if stat_mod.S_ISREG(m)
            else 'other')


def _dir_fd(p):
    """the directory p opened with O_NOFOLLOW_ANY: the kernel refuses a symlink in ANY component (macOS 11+)."""
    return os.open(p, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW_ANY)


def _free(fd):
    v = os.fstatvfs(fd)
    b = v.f_bavail * v.f_frsize
    return {'free_bytes': b, 'free_gib': round(b / 2 ** 30, 2), 'free_gb': round(b / 1e9, 2)}


def _digits(s, label):
    if not (isinstance(s, str) and re.fullmatch(r'[0-9]{1,20}', s)):
        raise Refuse('OUTPUT_ROOT_ARG_NOT_AN_INTEGER %s: %r' % (label, s))
    return int(s)


def _verify_root(p, st, vdev, expect=None):
    if not stat_mod.S_ISDIR(st.st_mode):
        raise Refuse('OUTPUT_ROOT_NOT_A_DIRECTORY (%s): %s' % (_kind(st), p))
    fd = _dir_fd(p)
    try:
        fs = os.fstat(fd)
        if (fs.st_dev, fs.st_ino) != (st.st_dev, st.st_ino):
            raise Refuse('PATH_CHANGED_DURING_VERIFY %s' % p)
        rp = fcntl.fcntl(fd, fcntl.F_GETPATH, bytes(1024)).split(b'\0', 1)[0].decode('utf-8')
        entries = os.listdir(fd)
        free = _free(fd)
    finally:
        os.close(fd)
    if rp != p:
        raise Refuse('OUTPUT_ROOT_REALPATH_DIFFERS %r (literal %r)' % (rp, p))
    if fs.st_dev != vdev:
        raise Refuse('OUTPUT_ROOT_NOT_ON_THE_DATA_VOLUME st_dev %d != %s %d' % (fs.st_dev, VOLUME_ROOT, vdev))
    if entries:
        raise Refuse('OUTPUT_ROOT_NOT_EMPTY (%d entries) %s' % (len(entries), p))
    if expect is not None and (fs.st_dev, fs.st_ino) != expect:
        raise Refuse('OUTPUT_ROOT_IS_NOT_THE_RECORDED_DIRECTORY (st_dev, st_ino) %r != %r' % ((fs.st_dev, fs.st_ino), expect))
    return {'realpath': rp, 'realpath_equals_literal': True,
            'realpath_method': 'fcntl F_GETPATH of the directory opened O_NOFOLLOW_ANY|O_DIRECTORY (the kernel path of that vnode; no '
                               'symlink in any component can be followed); os.path.realpath is not called (SA-CX1-B1)',
            'st_dev': fs.st_dev, 'st_ino': fs.st_ino, 'volume_root': VOLUME_ROOT, 'volume_st_dev': vdev, 'on_data_volume': True,
            'empty': True, 'mode': oct(stat_mod.S_IMODE(fs.st_mode)), 'free': free}


def c_output_root(a):
    """RP-S1 (A105.2; FROM_CODEX/0642): the step-2 output root.
    check  (step 0): the root is ABSENT in every form (lstat: a directory, a file or a symlink, even a dangling one, refuses); its
           parent chain passes the no-follow walk (one missing level, the parent itself, is allowed); the existing ancestor is on
           /System/Volumes/Data; free space there is recorded and must be >= the root floor P10 (0 = record only). Writes nothing.
    create (step 3, before the binder): the same checks; then the missing parent level (if any) is created, and the root with
           os.mkdir, EXCLUSIVELY (an entry of any kind appearing meanwhile raises FileExistsError: refused); then verified: a real
           directory (no-follow walk), realpath equal to the literal, on the Data volume, empty. Device, realpath and free space are
           returned for the run log.
    verify (summary): the root is still the recorded (st_dev, st_ino), a real directory, realpath = literal, on the volume, empty."""
    p = a.path
    path_policy(p, must_exist=None, label='output_root')
    if any(c in ('', '.', '..') for c in p.split('/')[1:]):
        raise Refuse('PATH_COMPONENT_REFUSED output_root: %r (lexical, before any walk or mkdir)' % p)
    parent = os.path.dirname(p)
    gp = os.path.dirname(parent)
    if not gp.startswith('/Users/'):
        raise Refuse('OUTPUT_ROOT_TOO_SHALLOW %r' % p)
    vdev = _volume_dev()
    if a.mode == 'verify':
        st = nofollow_walk(p, 'output_root')
        exp = (_digits(a.expect_dev, 'expect-dev'), _digits(a.expect_ino, 'expect-ino'))
        return {'output_root': dict(_verify_root(p, st, vdev, exp), path=p, mode='verify')}
    if a.mode not in ('check', 'create'):
        raise Refuse('OUTPUT_ROOT_MODE %r' % a.mode)
    floor = _digits(a.min_free_gib, 'min-free-gib')
    gst = nofollow_walk(gp, 'output_root grandparent')
    if not stat_mod.S_ISDIR(gst.st_mode):
        raise Refuse('OUTPUT_ROOT_GRANDPARENT_NOT_A_DIRECTORY %s' % gp)
    pst = nofollow_walk(parent, 'output_root parent', final_may_be_absent=True)
    if pst is not None:
        if not stat_mod.S_ISDIR(pst.st_mode):
            raise Refuse('OUTPUT_ROOT_PARENT_NOT_A_DIRECTORY (%s) %s' % (_kind(pst), parent))
        rst = nofollow_walk(p, 'output_root', final_may_be_absent=True)
        if rst is not None:
            raise Refuse('OUTPUT_ROOT_EXISTS (%s): %s; RP-S1 needs a NEW directory; nothing was created' % (_kind(rst), p))
    anc, anc_st = (parent, pst) if pst is not None else (gp, gst)
    if anc_st.st_dev != vdev:
        raise Refuse('OUTPUT_ROOT_NOT_ON_THE_DATA_VOLUME %s' % anc)
    fd = _dir_fd(anc)
    try:
        fs = os.fstat(fd)
        if (fs.st_dev, fs.st_ino) != (anc_st.st_dev, anc_st.st_ino):
            raise Refuse('PATH_CHANGED_DURING_CHECK %s' % anc)
        free = _free(fd)
    finally:
        os.close(fd)
    if free['free_bytes'] < floor * 2 ** 30:
        raise Refuse('FREE_BELOW_THE_ROOT_FLOOR %.2f GiB < %d GiB (P10; nothing was created)' % (free['free_gib'], floor))
    out = {'path': p, 'mode': a.mode, 'parent': parent, 'parent_existed': pst is not None, 'existing_ancestor': anc,
           'volume_root': VOLUME_ROOT, 'volume_st_dev': vdev, 'free_at_existing_ancestor': free, 'min_free_gib_P10': floor,
           'absent_in_every_form': True}
    if a.mode == 'check':
        out['created'] = False
        return {'output_root': out}
    out['parent_created'] = False
    if pst is None:
        try:
            os.mkdir(parent, 0o755)
            out['parent_created'] = True
        except FileExistsError:
            pass                                    # it appeared meanwhile: accepted only if the walk below finds a real directory
        pst = nofollow_walk(parent, 'output_root parent')
        if not stat_mod.S_ISDIR(pst.st_mode) or pst.st_dev != vdev:
            raise Refuse('OUTPUT_ROOT_PARENT_AFTER_MKDIR (%s) %s' % (_kind(pst), parent))
    try:
        os.mkdir(p, 0o755)                          # EXCLUSIVE: FileExistsError for any existing entry, a dangling symlink included
    except FileExistsError:
        raise Refuse('OUTPUT_ROOT_EXISTS (appeared between the check and the mkdir): %s' % p)
    out['created'] = True
    st = nofollow_walk(p, 'output_root')
    out.update(_verify_root(p, st, vdev))
    return {'output_root': out}


def _sel_pairs_hook(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise Refuse('SELECTED_DUPLICATE_KEY %r' % k)
        out[k] = v
    return out


def _sel_const(c):
    raise Refuse('SELECTED_NON_FINITE %s' % c)


def _sel_int(t):
    n = len(t.lstrip('-'))
    if n > SEL_MAX_INT_DIGITS:
        raise Refuse('SELECTED_INTEGER_TOO_LONG %d digits (limit %d)' % (n, SEL_MAX_INT_DIGITS))
    return int(t)


def _sel_float(t):
    f = float(t)
    if f != f or f in (float('inf'), float('-inf')):
        raise Refuse('SELECTED_NON_FINITE %s' % t[:40])
    return f


def _sel_depth(t):
    depth, ins, esc = 0, False, False
    for ch in t:
        if ins:
            if esc:
                esc = False
            elif ch == '\\':
                esc = True
            elif ch == '"':
                ins = False
        elif ch == '"':
            ins = True
        elif ch in '[{':
            depth += 1
            if depth > SEL_MAX_DEPTH:
                raise Refuse('SELECTED_JSON_TOO_DEEP (more than %d levels)' % SEL_MAX_DEPTH)
        elif ch in ']}':
            depth -= 1


def _selected_strict(b):
    """C02-SEL-STRICT (Codex1 0101): the SELECTED bytes, read ONCE by pin(), parsed strictly from that exact buffer. Every failure is
    a typed refusal; there is no fallback of any kind."""
    try:
        t = b.decode('utf-8', 'strict')
    except UnicodeDecodeError as e:
        raise Refuse('SELECTED_INVALID_UTF8 at byte %d' % e.start)
    if t.startswith('﻿'):
        raise Refuse('SELECTED_BOM')
    _sel_depth(t)
    try:
        obj = json.loads(t, object_pairs_hook=_sel_pairs_hook, parse_constant=_sel_const, parse_int=_sel_int, parse_float=_sel_float)
    except Refuse:
        raise
    except RecursionError:
        raise Refuse('SELECTED_JSON_TOO_DEEP (recursion)')
    except ValueError as e:                   # json.JSONDecodeError: trailing data, syntax errors
        raise Refuse('SELECTED_NOT_STRICT_JSON %s' % str(e)[:200])
    if not isinstance(obj, dict):
        raise Refuse('SELECTED_TOP_LEVEL_NOT_AN_OBJECT')
    return obj


def _selected_roles(sel_bytes, schema, role_pins):
    """C02-SEL-ASSOCIATION, role-qualified (the real SELECTED schema, Claude4 SELECTED_R6_C4V001): strict parse (c3v013); the schema
    string must match; 'files' is an object whose every entry is exactly {path: absolute str, sha256: 64 lowercase hex}, no path with
    two shas; each requested (role, path, sha) must be EXACTLY files[role]."""
    obj = _selected_strict(sel_bytes)
    if obj.get('schema') != schema:
        raise Refuse('SELECTED_SCHEMA_MISMATCH %r (want %r)' % (obj.get('schema'), schema))
    files = obj.get('files')
    if not isinstance(files, dict) or not files:
        raise Refuse('SELECTED_FILES_NOT_A_NONEMPTY_OBJECT')
    seen = {}
    for role, e in files.items():
        if not (isinstance(e, dict) and set(e) == {'path', 'sha256'} and isinstance(e['path'], str) and e['path'].startswith('/')
                and isinstance(e['sha256'], str) and HEX64.fullmatch(e['sha256'])):
            raise Refuse('SELECTED_FILES_ENTRY_FORM %r (each entry exactly {path: absolute, sha256: 64 lowercase hex})' % role)
        if e['path'] in seen and seen[e['path']] != e['sha256']:
            raise Refuse('SELECTED_CONFLICTING_PAIR_FOR_PATH %s' % e['path'])
        seen[e['path']] = e['sha256']
    for role, p, h in role_pins:
        if not (isinstance(p, str) and p.startswith('/') and isinstance(h, str) and HEX64.fullmatch(h)):
            raise Refuse('SELECTED_REQUEST_FORM %r %r %r' % (role, p, h))
        if role not in files:
            raise Refuse('SELECTED_ROLE_MISSING %r' % role)
        if files[role] != {'path': p, 'sha256': h}:
            raise Refuse('SELECTED_ROLE_PAIR_MISMATCH %r: stored %r, requested %r' % (role, files[role], {'path': p, 'sha256': h}))
    return len(role_pins)


def c_selected_roles(a):
    """r6 wiring (0644 follow-up): every --role-pin ROLE=PATH=SHA is exactly the SELECTED file's files[ROLE]; each pin is verified from bytes."""
    sel = pin(a.selected, a.selected_sha, 'selected')
    rp = []
    for x in a.role_pin:
        if x.count('=') < 2:
            raise Refuse('ROLE_PIN_FORM %r (ROLE=PATH=SHA)' % x)
        role, rest = x.split('=', 1)
        p, h = rest.rsplit('=', 1)
        rp.append((role, p, h))
    if not rp:
        raise Refuse('SELECTED_ROLES_NO_PINS')
    n = _selected_roles(sel, a.schema, rp)
    for role, p, h in rp:
        pin(p, h, 'selected role ' + role)
    return {'selected': {'path': a.selected, 'sha256': a.selected_sha, 'schema': a.schema}, 'roles_verified': {r: {'path': p, 'sha256': h} for r, p, h in rp},
            'n': n}


def _tor_unsealed(doc):
    ss = doc.get('seal_slots') if isinstance(doc, dict) else None
    if not isinstance(ss, dict) or set(ss) != set(PREREG_SLOT_OF):
        raise Refuse('C02_TEXT_OF_RECORD_SEAL_SLOTS_KEYS %r' % (sorted(ss) if isinstance(ss, dict) else ss))
    filled = sorted(k for k, v in ss.items() if k != 'cache_directory_r6_only'
                    and not (isinstance(v, dict) and isinstance(v.get('value'), str) and 'PENDING' in v['value']))
    if filled:
        raise Refuse('C02_TEXT_OF_RECORD_HAS_FILLED_SLOTS %r (a sealed or edited prereg named as its own text of record)' % filled)


def _sealed_bytes(tor_bytes, slots):
    doc = sjson(tor_bytes)
    for pk, sk in PREREG_SLOT_OF.items():
        doc['seal_slots'][pk]['value'] = slots[sk]
    return dumps(doc).encode('utf-8')


def c_check_tor(a):
    """C-02 (A106.2; 0643 B): the text of record is exactly the prereg its SELECTED file stores (path and sha, from bytes); it is an
    UNSEALED text; and a given sealed prereg is a different file, byte-equal to the text of record with only seal_slots.<k>.value
    filled from the final slots (so an edited sealed prereg can pass neither as the text of record nor as the sealed prereg)."""
    sel = pin(a.selected, a.selected_sha, 'r6_selected')
    _selected_roles(sel, a.selected_schema, [(a.tor_role, a.text_of_record, a.tor_sha)])     # role-qualified (c3v014)
    tb = pin(a.text_of_record, a.tor_sha, 'text_of_record')
    _tor_unsealed(sjson(tb))
    out = {'text_of_record': {'path': a.text_of_record, 'sha256': a.tor_sha}, 'named_by_selected': {'path': a.selected, 'sha256': a.selected_sha,
           'schema': a.selected_schema, 'role': a.tor_role},
           'unsealed': True}
    if a.sealed_prereg or a.sealed_prereg_sha or a.slots or a.slots_sha:
        if not (a.sealed_prereg and a.sealed_prereg_sha and a.slots and a.slots_sha):
            raise Refuse('C02_ARGS (give --sealed-prereg, --sealed-prereg-sha, --slots and --slots-sha together)')
        if a.sealed_prereg == a.text_of_record or a.sealed_prereg_sha == a.tor_sha:
            raise Refuse('C02_SEALED_PREREG_IS_THE_TEXT_OF_RECORD')
        sp = pin(a.sealed_prereg, a.sealed_prereg_sha, 'sealed_prereg')
        slots = sjson(pin(a.slots, a.slots_sha, 'slots_final'))
        if sp != _sealed_bytes(tb, slots):
            raise Refuse('C02_SEALED_PREREG_NOT_THE_TEXT_OF_RECORD_PLUS_SLOT_VALUES')
        out['sealed_prereg'] = {'path': a.sealed_prereg, 'sha256': a.sealed_prereg_sha, 'rederived_byte_equal': True}
    return {'c02': out}


def _gate_record_codes(M, reg, gate, rec, sha, where):
    """C-04: one slotted gate record through r13's own registry functions (record sha of record; producer path, sha and bytes)."""
    codes = []
    if rec.get('schema') != M.GATE_SCHEMA:
        codes.append('C04_NOT_A_GATE_RECORD_SCHEMA:%s' % where)
    if gate not in M.ALL_GATES:
        return codes + ['C04_NOT_A_REGISTRY_GATE:%s:%s' % (where, gate)]
    codes += list(M.gate_record_sha_codes(gate, sha, reg))
    v, want = rec.get('verdict'), M.GATE_PASS_VERDICTS.get(gate)     # Codex1 0101 C04 boundary note (closed): the gate's PASS verdict
    if not (isinstance(v, str) and v == want):
        codes.append('C04_VERDICT_NOT_THE_GATE_PASS_VERDICT:%s:%s (want %s)' % (where, v if isinstance(v, str) else type(v).__name__, want))
    p = rec.get('producer') if isinstance(rec.get('producer'), dict) else {}
    codes += list(M.file_pin_codes(p.get('path'), p.get('sha256'), reg['producers'].get(gate, frozenset()),
                                   (M.PRODUCER_SHA_CODE, gate, M.PRODUCER_PATH_CODE, M.PRODUCER_BYTES_CODE)))
    return codes


def c_slot_registry(a):
    """C-04 (A106.2; 0643 B): every slot record, loaded through the reviewed compare r13's OWN load_producer_registry against the
    slotted registry (V009), must PASS: each certificate, each identity record (gate, record sha, producer, comparator and token
    set), the identity comparator, and any other slotted gate record (B2 / B3 where slotted). r13 is read once and exec'd from that
    buffer inside the fence."""
    excl = {}
    for x in a.exclude:                          # A107 (P12 option (b)): the explicit two-entry exclusion list, by name, path and sha
        if x.count('=') < 2:
            raise Refuse('C04_EXCLUSION_FORM %r (WHERE=PATH=SHA)' % x)
        w, rest = x.split('=', 1)
        p, h = rest.rsplit('=', 1)
        if w in excl:
            raise Refuse('C04_EXCLUSION_REPEATED %s' % w)
        excl[w] = (p, h)
    if excl != C04_A107_EXCLUSIONS:
        raise Refuse('C04_EXCLUSIONS_NOT_EXACTLY_THE_A107_LIST %r (A107: exactly certificates.EPS_NGC and certificates.I1T_NGC, each by its '
                     'path and sha; no third slot)' % sorted(excl))
    slots = sjson(pin(a.slots, a.slots_sha, 'slots_final'))
    if slots.get('producer_registry') != {'path': a.registry, 'sha256': a.registry_sha}:
        raise Refuse('C04_SLOT_REGISTRY_IS_NOT_THE_GIVEN_REGISTRY %r' % slots.get('producer_registry'))
    pin(a.registry, a.registry_sha, 'producer_registry')
    F = _fence(a, write_roots=())
    M = load_pinned(a.compare, a.compare_sha, 'reviewed_compare_r13_c04')
    reg = M.load_producer_registry(a.registry, a.registry_sha)
    res, bad, excluded = {}, {}, {}

    def record(where, ref):
        if not (isinstance(ref, dict) and set(ref) == {'path', 'sha256'}):
            bad[where] = ['C04_SLOT_NOT_A_PIN']
            return None
        return sjson(pin(ref['path'], ref['sha256'], where))
    for k, ref in sorted((slots.get('certificates') or {}).items()):
        where = 'certificates.' + k
        if where in excl and ref != {'path': excl[where][0], 'sha256': excl[where][1]}:
            raise Refuse('C04_EXCLUDED_SLOT_PIN_DIFFERS %s: the slot holds %r, A107 excludes %r' % (where, ref, excl[where]))
        rec = record(where, ref)
        if rec is None:
            continue
        gate = rec.get('gate')
        codes = [] if gate in CERT_SLOT_GATES.get(k, (k,)) else ['C04_CERT_GATE_NOT_THE_SLOT:%s:%s' % (where, gate)]
        codes += _gate_record_codes(M, reg, gate, rec, ref['sha256'], where)
        if where in excl:                         # pinned from bytes and reported; not a C-04 failure (A107)
            excluded[where] = {'gate': gate, 'sha256': ref['sha256'], 'registry_codes_reported_only': codes}
            continue
        res[where] = {'gate': gate, 'sha256': ref['sha256'], 'codes': codes}
    comp = slots.get('identity_comparator')
    ccodes = list(M.file_pin_codes((comp or {}).get('path'), (comp or {}).get('sha256'), reg['identity_comparators'],
                                   ('C04_IDENTITY_COMPARATOR_NOT_ROOT_REGISTERED_A57_3', 'identity_comparator',
                                    'C04_IDENTITY_COMPARATOR_PATH_NOT_ROOT_REGISTERED_A69_1',
                                    'C04_IDENTITY_COMPARATOR_BYTES_NOT_THE_REGISTERED_SHA_A69_1')))
    res['identity_comparator'] = {'sha256': (comp or {}).get('sha256'), 'codes': ccodes}
    for k, ref in sorted((slots.get('identity_gate_records') or {}).items()):
        where = 'identity_gate_records.' + k
        rec = record(where, ref)
        if rec is None:
            continue
        gate = rec.get('gate')
        codes = [] if gate == IDENT_SLOT_GATE.get(k) else ['C04_IDENTITY_GATE_NOT_THE_SLOT:%s:%s' % (where, gate)]
        codes += _gate_record_codes(M, reg, gate, rec, ref['sha256'], where)
        if gate in M.IDENTITY_GATES:
            codes += [c for c in M.identity_comparator_codes(rec, gate, {'producer_registry': reg}, [])]
        if rec.get('comparator') != comp:
            codes.append('C04_IDENTITY_RECORD_COMPARATOR_IS_NOT_THE_SLOT_COMPARATOR:%s' % where)
        res[where] = {'gate': gate, 'sha256': ref['sha256'], 'codes': codes}
    other = []                                   # B2 / B3 (or any other gate record) where slotted elsewhere
    for grp, v in sorted(slots.items()):
        if grp in ('certificates', 'identity_gate_records', 'identity_comparator', 'producer_registry') or not isinstance(v, dict):
            continue
        for k, ref in sorted(v.items()) if not set(v) >= {'path', 'sha256'} else [('', v)]:
            if isinstance(ref, dict) and set(ref) == {'path', 'sha256'} and str(ref['path']).endswith('.json'):
                try:
                    rec = sjson(pin(ref['path'], ref['sha256'], grp))
                except Refuse:
                    raise
                except Exception:
                    continue
                if isinstance(rec, dict) and rec.get('schema') == M.GATE_SCHEMA:
                    where = grp + ('.' + k if k else '')
                    res[where] = {'gate': rec.get('gate'), 'sha256': ref['sha256'],
                                  'codes': _gate_record_codes(M, reg, rec.get('gate'), rec, ref['sha256'], where)}
                    other.append(where)
    if F.FENCE['refused']:
        raise Refuse('FENCE_REFUSED %r' % F.FENCE['events'])
    missing = sorted(set(excl) - set(excluded))
    if missing:
        raise Refuse('C04_EXCLUDED_SLOT_ABSENT %r (A107 names slots this slot file does not hold)' % missing)
    bad.update({w: r['codes'] for w, r in res.items() if r['codes']})
    if bad:
        raise Refuse('C04_SLOT_RECORDS_FAIL_THE_REGISTRY %s' % json.dumps(bad, sort_keys=True))
    return {'c04': {'registry': {'path': a.registry, 'sha256': a.registry_sha}, 'compare': {'path': a.compare, 'sha256': a.compare_sha},
                    'records_registry_admitted_with_the_gate_pass_verdict': sorted(res), 'excluded_by_A107': excluded,
                    'other_gate_records_slotted': other, 'fence_refused': 0,
                    'scope': 'registry admission (record sha, producer, comparator, tokens) plus the gate PASS verdict; not evaluate_gate'}}


def c_bound_check(a):
    """C-05 + C-06 (A106.2; 0643 B), after the binder: the launcher and the guard are BUILD_V007 rows by EXACT file name and sha, and
    the bound plan names exactly them ('any allowlisted source' does not pass); the WHOLE bound command file is byte-equal to the
    binder's output: its fixed comment line and its shlex command line, both taken from the pinned binder source."""
    rows = _build_table(pin(a.build, a.build_sha, 'build').decode('utf-8'))
    for label, name, p, h in (('LAUNCHER', C05_LAUNCHER_NAME, a.launcher, a.launcher_sha), ('GUARD', C05_GUARD_NAME, a.guard, a.guard_sha)):
        if os.path.basename(p) != name:
            raise Refuse('C05_%s_NAME %r (want %s)' % (label, os.path.basename(p), name))
        hits = [r for r in rows if os.path.basename(r[0]) == name]
        if len(hits) != 1:
            raise Refuse('C05_%s_BUILD_ROWS_NAMED_%s %d (want exactly one)' % (label, name, len(hits)))
        if hits[0] != (p, h):
            raise Refuse('C05_%s_NOT_THE_BUILD_ROW %r (BUILD_V007 row %r)' % (label, (p, h), hits[0]))
        pin(p, h, label.lower())
    plan = sjson(pin(a.plan, a.plan_sha, 'bound_plan'))
    if plan.get('launcher') != {'path': a.launcher, 'sha256': a.launcher_sha}:
        raise Refuse('C05_PLAN_LAUNCHER_NOT_EXACT %r' % (plan.get('launcher'),))
    if plan.get('guard') != {'path': a.guard, 'sha256': a.guard_sha}:
        raise Refuse('C05_PLAN_GUARD_NOT_EXACT %r' % (plan.get('guard'),))
    bsrc = pin(a.binder, a.binder_sha, 'binder').decode('utf-8')
    for frag in (BINDER_PYTHON_LINE, BINDER_CMD_FORM, BINDER_WRITE_FORM):
        if bsrc.count(frag) != 1:
            raise Refuse('C06_BINDER_SOURCE_FORM %r' % frag[:70])
    py = BINDER_PYTHON_LINE.split("'")[1]
    want = (BINDER_COMMENT + '\n' + shlex.join([py, '-I', '-B', plan['launcher']['path'], a.plan, '--execute-root-only']) + '\n').encode('utf-8')
    got = pin(a.command, a.command_sha, 'bound_command')
    if got != want:
        gl, wl = got.split(b'\n'), want.split(b'\n')
        i = next((j for j in range(max(len(gl), len(wl))) if (gl[j] if j < len(gl) else None) != (wl[j] if j < len(wl) else None)), 0)
        raise Refuse('C06_BOUND_COMMAND_NOT_BYTE_EQUAL_TO_THE_BINDER_OUTPUT (first differing line %d; %d bytes, want %d)' % (i + 1, len(got), len(want)))
    return {'c05': {'launcher': {'path': a.launcher, 'sha256': a.launcher_sha}, 'guard': {'path': a.guard, 'sha256': a.guard_sha},
                    'exact_build_rows': True, 'plan_names_exactly_them': True},
            'c06': {'bound_command': {'path': a.command, 'sha256': a.command_sha}, 'byte_equal_to_the_binder_output': True,
                    'lines': len(want.split(b'\n')) - 1}}


def c_gates_provenance(a):
    """C-03 (B6 provenance; A106.2, taken in because it fits 10 minutes): the sealed-mode GATES_ONLY body evaluated the SLOTTED gate
    records: for each certificate and identity slot that is a gates-only gate record, the body's record_sha256 for that gate equals
    the slot's sha and its status is PASS. The NGC certificates EPS_NGC and I1T_NGC are not gates-only gate records (C-04 covers them)."""
    g = sjson(pin(a.gates_json, a.gates_json_sha, 'gates_only_json'))
    slots = sjson(pin(a.slots, a.slots_sha, 'slots_final'))
    if not isinstance(g, dict) or g.get('test_mode') is not False or not isinstance(g.get('gates'), dict):
        raise Refuse('C03_GATES_ONLY_BODY_NOT_SEALED_MODE')
    out, bad = {}, []
    for grp, k, gate in C03_SLOT_GATES:
        ref = (slots.get(grp) or {}).get(k)
        e = g['gates'].get(gate)
        if not (isinstance(ref, dict) and isinstance(e, dict)):
            bad.append('C03_SLOT_GATE_NOT_IN_THE_BODY:%s.%s:%s' % (grp, k, gate))
            continue
        if not (isinstance(ref.get('sha256'), str) and HEX64.fullmatch(ref['sha256'])):
            bad.append('C03_MALFORMED_SLOT_SHA:%s.%s' % (grp, k))         # A106-C03-S1: validated BEFORE any comparison
            continue
        if not (isinstance(e.get('record_sha256'), str) and HEX64.fullmatch(e['record_sha256'])):
            bad.append('C03_MALFORMED_BODY_RECORD_SHA:%s.%s:%s' % (grp, k, gate))
            continue
        if e.get('record_sha256') != ref.get('sha256'):
            bad.append('C03_BODY_EVALUATED_ANOTHER_RECORD:%s.%s:%s' % (grp, k, gate))
        elif e.get('status') != 'PASS':
            bad.append('C03_SLOT_GATE_STATUS_%s:%s.%s:%s' % (e.get('status'), grp, k, gate))
        else:
            out['%s.%s' % (grp, k)] = {'gate': gate, 'record_sha256': ref['sha256'], 'status': 'PASS'}
    if bad:
        raise Refuse('C03 %s' % ' '.join(bad))
    return {'c03': {'gates_only_json': {'path': a.gates_json, 'sha256': a.gates_json_sha}, 'slotted_records_evaluated': out,
                    'not_gates_only_records': ['certificates.EPS_NGC', 'certificates.I1T_NGC']}}


def c_make_receipt(a):
    """B9 / step 13: the separate SEAL_ADMISSION_RECEIPT naming the config and seal full shas (FORMAT_V005 item 3; 0561)."""
    cfg = sjson(pin(a.config, a.config_sha, 'config'))
    pin(a.seal, a.seal_sha, 'seal_record')
    if cfg.get('seal') != {'path': a.seal, 'sha256': a.seal_sha}:
        raise Refuse('CONFIG_DOES_NOT_PIN_THIS_SEAL')
    rec = {'schema': RECEIPT_SCHEMA, 'authority': dict(AUTHORITY), 'config': {'path': a.config, 'sha256': a.config_sha},
           'seal': {'path': a.seal, 'sha256': a.seal_sha},
           'statement': 'Root publishes this receipt, the config sha and the SEAL_RECORD sha in a numbered root packet; producers export '
                        'UNT_ROOT_ADMISSION_SHA256 from that published value, never from the local config (FORMAT_V005).'}
    return {'receipt': write_x(a.out, dumps(rec), 'receipt')}


def main(argv=None):
    p = argparse.ArgumentParser(allow_abbrev=False)
    sp = p.add_subparsers(dest='cmd', required=True)
    def sub(name, *flags, multi=(), opt=(), ints=()):
        q = sp.add_parser(name, allow_abbrev=False)
        for f in flags:
            q.add_argument('--' + f, required=True)
        for f in multi:
            q.add_argument('--' + f, action='append', default=[])
        for f in opt:
            q.add_argument('--' + f, default='')
        for f in ints:
            q.add_argument('--' + f, type=int, required=True)
        return q
    sub('pin', multi=('pin',))
    sub('absent', multi=('path',))
    sub('freeze', 'open', 'open-sha', 'open-bytes', 'out')
    sub('same-bytes', 'open', 'frozen', 'frozen-sha')
    sub('rehash-entries', 'prereg', 'prereg-sha', 'frozen', 'frozen-sha', 'dispositions', 'dispositions-sha', 'table-bytes', 'table-bytes-sha')
    sub('dispositions', 'prereg', 'prereg-sha', 'frozen', 'frozen-sha', 'dispositions', 'dispositions-sha', 'table-bytes', 'table-bytes-sha')
    sub('driver-build-record', 'compare', 'compare-sha', 'check-record', 'check-sha', 'fence', 'fence-sha', 'out')
    sub('fill-slots', 'draft', 'draft-sha', 'out', multi=('runtime', 'expect', 'ruling'))
    sub('sealed-prereg', 'text-of-record', 'tor-sha', 'slots', 'slots-sha', 'out')
    sub('sealed-compare', 'reviewed', 'reviewed-sha', 'slots', 'slots-sha', 'sealed-prereg', 'sealed-prereg-sha', 'out')
    sub('check-manifest', 'sealed-compare', 'sealed-compare-sha', 'manifest', 'manifest-sha', 'mode', multi=('identity-record',))
    sub('make-c5h-manifest', 'sealed-compare', 'sealed-compare-sha', 'c5h-dir', 'b0-record', 'out')
    sub('gates-only', 'fence', 'fence-sha', 'sealed-compare', 'sealed-compare-sha', 'sealed-prereg', 'sealed-prereg-sha', 'manifest',
        'manifest-sha', 'outdir', 'mode', opt=('standin',))
    sub('row-value-scan', 'path')
    sub('check-tool4', 'stdout', 'stderr')
    sub('copy-exclusive', 'src', 'src-sha', 'dst')
    sub('make-config', 'seal', 'seal-sha', 'build', 'build-sha', 'allowlist', 'allowlist-sha', 'producer-index', 'producer-index-sha',
        'guard', 'guard-sha', 'launcher', 'launcher-sha', 'out')
    sub('check-config-allowlist', 'config', 'config-sha', 'build', 'build-sha')
    sub('output-root', 'path', 'mode', opt=('min-free-gib', 'expect-dev', 'expect-ino'))
    sub('check-driver-build-record', 'compare', 'compare-sha', 'record', 'record-sha', 'check-record', 'check-sha', 'fence', 'fence-sha')
    sub('check-tor', 'text-of-record', 'tor-sha', 'selected', 'selected-sha', 'selected-schema', 'tor-role', opt=('sealed-prereg', 'sealed-prereg-sha', 'slots', 'slots-sha'))
    sub('selected-roles', 'selected', 'selected-sha', 'schema', multi=('role-pin',))
    sub('slot-registry', 'compare', 'compare-sha', 'registry', 'registry-sha', 'slots', 'slots-sha', 'fence', 'fence-sha', multi=('exclude',))
    sub('bound-check', 'build', 'build-sha', 'plan', 'plan-sha', 'command', 'command-sha', 'binder', 'binder-sha', 'launcher', 'launcher-sha', 'guard', 'guard-sha')
    sub('gates-provenance', 'gates-json', 'gates-json-sha', 'slots', 'slots-sha')
    sub('check-disclosures', 'disclosures', 'disclosures-sha', 'r6-selected', 'r6-selected-sha', 'r6-schema')
    sub('make-receipt', 'config', 'config-sha', 'seal', 'seal-sha', 'out')
    argv = sys.argv[1:] if argv is None else argv
    flags = [x.split('=', 1)[0] for x in argv if x.startswith('--')]
    multi_ok = {'--pin', '--path', '--runtime', '--expect', '--ruling', '--identity-record', '--exclude', '--role-pin'}
    if any(flags.count(f) > 1 for f in set(flags) - multi_ok):
        print(json.dumps({'verdict': 'REFUSE', 'code': 'CLI_REPEATED_FLAG'}), file=sys.stderr)
        return 2
    a = p.parse_args(argv)
    fn = {'pin': c_pin, 'absent': c_absent, 'freeze': c_freeze, 'same-bytes': c_same, 'rehash-entries': c_rehash, 'dispositions': c_dispositions,
          'driver-build-record': c_driver_build, 'fill-slots': c_fill, 'sealed-prereg': c_sealed_prereg,
          'sealed-compare': c_sealed_compare, 'check-manifest': c_check_manifest, 'make-c5h-manifest': c_make_c5h_manifest,
          'gates-only': c_gates_only, 'row-value-scan': c_row_scan, 'check-tool4': c_check_tool4, 'copy-exclusive': c_copy_x,
          'make-config': c_make_config, 'make-receipt': c_make_receipt, 'check-config-allowlist': c_check_config_allowlist,
          'output-root': c_output_root, 'check-driver-build-record': c_check_driver_build, 'check-tor': c_check_tor, 'slot-registry': c_slot_registry,
          'bound-check': c_bound_check, 'gates-provenance': c_gates_provenance, 'selected-roles': c_selected_roles,
          'check-disclosures': c_check_disclosures}[a.cmd]
    t0 = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    try:
        res = fn(a)
        print(json.dumps({'step': a.cmd, 'verdict': 'PASS', 'utc': t0, **res}, sort_keys=True), file=sys.stderr)
        return 0
    except Refuse as e:
        print(json.dumps({'step': a.cmd, 'verdict': 'REFUSE', 'utc': t0, 'code': str(e)[:2000]}), file=sys.stderr)
        return 2
    except Exception as e:      # any other failure refuses too (fail closed); the type and text are reported
        print(json.dumps({'step': a.cmd, 'verdict': 'REFUSE', 'utc': t0, 'code': 'EXCEPTION %s: %s' % (type(e).__name__, str(e)[:1500])}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())

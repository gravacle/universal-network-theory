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
# Rules (every subcommand): each input is a (path, sha256) pin verified from bytes BEFORE it is used; every path argument is an
# absolute /Users/... literal whose realpath is itself (no firmlink /System/Volumes/Data spelling, no /private, no /.vol, no '..');
# every file this helper creates is created with open(path, 'x'/'xb') and nothing is ever overwritten, edited or deleted; strict
# JSON everywhere (a duplicate key or a non-finite constant refuses, A71); no process start, no network. The verdict JSON goes to
# STDERR (stdout stays free for the compare's own output in the gates-only step); exit 0 = PASS, 2 = REFUSE.
# Nothing here opens, stats or lists the registered C5H run, any runs_ext/UVT_* tree (except gates-only in ROOT mode, which reads the
# three identity-run trees named by the identity records of record, exactly as root's seal step B6 requires), /.vol or NGC targets.
import argparse, ast, hashlib, json, os, re, sys, time
from pathlib import Path

PIN_NAMES = ('V007_PREREG_SHA256', 'PIN_ADDENDUM_V005', 'PIN_DRIVER_BUILD_RECORD', 'PIN_V010_R5_CHECK', 'PIN_PRODUCER_REGISTRY')  # A82
SHA_PINS = ('V007_PREREG_SHA256', 'PIN_ADDENDUM_V005')
PREREG_SLOT_OF = {'frozen_addendum': 'frozen_addendum', 'driver': 'driver', 'compare': 'compare_reviewed_source',
                  'identity_comparator': 'identity_comparator', 'identity_gate_records': 'identity_gate_records',
                  'launch_packet': 'launch_packet', 'certificates': 'certificates', 'producer_registry': 'producer_registry',
                  'cache_directory_r6_only': 'cache_directory_r6_only'}       # seal tools README (1e04bd2a) "Mapping from slot to prereg"
SLOT_KEYS = ('schema', 'driver_branch', 'ngc_gas_M_s', 'frozen_addendum', 'driver', 'driver_build_record', 'driver_check_record',
             'compare_reviewed_source', 'identity_comparator', 'identity_gate_records', 'launch_packet', 'certificates',
             'producer_registry', 'cache_directory_r6_only')                  # check_slot_fill_c4v001 SLOT_KEYS
AUTHORITY = {'identity': 'Claude2', 'role': 'coordinator_and_single_scientific_launch_owner'}   # guard v008 AUTHORITY
CONFIG_SCHEMA = 'UNT_ROOT_SEAL_ADMISSION_CX1V001'                                                # guard v008 / FORMAT_V005 item 2
RECEIPT_SCHEMA = 'UNT_ROOT_SEAL_ADMISSION_RECEIPT_V001'        # PROPOSED by Claude3 (no text of record fixes a receipt schema name)
BUILD_HEADER = '## Supported runtime entry allowlist'
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


def path_policy(p, must_exist=None, label='path'):
    if not isinstance(p, str) or not p.startswith('/Users/') or '\n' in p:
        raise Refuse('PATH_NOT_ABSOLUTE_USERS_SPELLING %s: %r' % (label, p))
    if p.startswith('/System/Volumes/Data') or '/../' in p or '/./' in p or p.endswith('/..') or '//' in p:
        raise Refuse('PATH_SPELLING_REFUSED %s: %r' % (label, p))
    pc = p.casefold()
    if C5H_NAME_CF in pc or '/runs_ext' in pc or '/uvt_' in pc or '/.vol' in pc:
        raise Refuse('PATH_PROTECTED_REFUSED %s: %r' % (label, p))
    if must_exist is True:
        if os.path.realpath(p) != p:
            raise Refuse('PATH_NOT_CANONICAL %s: realpath %r != %r' % (label, os.path.realpath(p), p))
    if must_exist is False:
        if os.path.lexists(p):
            raise Refuse('OUTPUT_EXISTS %s: %s' % (label, p))
        d = os.path.dirname(p)
        if os.path.realpath(d) != d or not os.path.isdir(d):
            raise Refuse('OUTPUT_PARENT_NOT_CANONICAL_DIR %s: %s' % (label, d))
    return p


def pin(path, sha, label='pin'):
    """(path, sha) from bytes; returns the bytes."""
    path_policy(path, must_exist=True, label=label)
    if not (isinstance(sha, str) and HEX64.fullmatch(sha)):
        raise Refuse('PIN_SHA_FORMAT %s: %r' % (label, sha))
    if not os.path.isfile(path):
        raise Refuse('PIN_FILE_MISSING %s: %s' % (label, path))
    b = Path(path).read_bytes()
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
    got = sha_bytes(Path(path).read_bytes())
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
    """B1 / step 1: exclusive byte copy of the open V005 addendum; the open bytes must be exactly the ones root states."""
    if not a.out.endswith('_V005_ADDENDUM_FROZEN.md'):
        raise Refuse('FROZEN_NAME (0576: ..._V005_ADDENDUM_FROZEN.md)')
    b = pin(a.open, a.open_sha, 'open_v005')
    ref = write_x(a.out, b, 'frozen')
    again = sha_bytes(Path(a.open).read_bytes())
    if again != a.open_sha or ref['sha256'] != a.open_sha:
        raise Refuse('OPEN_V005_CHANGED_DURING_FREEZE')
    return {'frozen': ref, 'bytes': len(b)}


def c_same(a):
    """the open V005 file still has the frozen bytes (A82: root writes nothing to it after the freeze)."""
    fb = pin(a.frozen, a.frozen_sha, 'frozen')
    ob = Path(path_policy(a.open, True, 'open_v005')).read_bytes()
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


def _dispositions(a):
    """the root-supplied dispositions JSON (0633; seal tools v003 interface): a list (bare, or under the key 'dispositions') of
    {entry: 'A<n>', disposition: 'revised' | 'no_change', reason: non-empty string}; the entries are EXACTLY the entries after the
    prereg's table in the frozen bytes plus every table row whose section bytes changed. A bare name, an unknown disposition, an empty
    reason, a duplicate, an extra key or a missing entry refuses."""
    raw = pin(a.dispositions, a.dispositions_sha, 'dispositions')
    d = sjson(raw)
    lst = (d.get('dispositions', d.get('rows')) if isinstance(d, dict) else d)
    if not isinstance(lst, list):
        raise Refuse('DISPOSITIONS_NOT_A_LIST')
    fb = pin(a.frozen, a.frozen_sha, 'frozen')
    rows, changed, newest, later = _table_state(pin(a.prereg, a.prereg_sha, 'prereg_text_of_record'), fb)
    if isinstance(d, dict) and 'frozen_addendum_sha256' in d and d['frozen_addendum_sha256'] != a.frozen_sha:
        raise Refuse('DISPOSITIONS_FROZEN_SHA (the file names another frozen copy)')
    seen = {}
    for i, e in enumerate(lst):
        if not isinstance(e, dict):
            raise Refuse('DISPOSITION_BARE_NAME_OR_NOT_AN_OBJECT at [%d]: %r' % (i, e))
        if not ({'entry', 'disposition', 'reason'} <= set(e) <= {'entry', 'disposition', 'reason', 'section_sha256', 'change'}):
            raise Refuse('DISPOSITION_KEYS at [%d]: %r' % (i, sorted(e)))
        if not (isinstance(e['entry'], str) and re.fullmatch(r'A\d{1,3}', e['entry'])):
            raise Refuse('DISPOSITION_ENTRY at [%d]: %r' % (i, e['entry']))
        if e['disposition'] not in ('revised', 'no_change'):
            raise Refuse('DISPOSITION_VALUE at [%d]: %r' % (i, e['disposition']))
        if not (isinstance(e['reason'], str) and e['reason'].strip()):
            raise Refuse('DISPOSITION_EMPTY_REASON at [%d] (%s)' % (i, e['entry']))
        if e['entry'] in seen:
            raise Refuse('DISPOSITION_DUPLICATE %s' % e['entry'])
        sec = _section(fb, e['entry'])
        if 'section_sha256' in e and (sec is None or e['section_sha256'] != sha_bytes(sec)):
            raise Refuse('DISPOSITION_WRONG_SECTION_SHA %s' % e['entry'])
        seen[e['entry']] = e
    for c in changed:                    # a changed table row: if a change object is given it must name both section shas
        ch = (seen.get(c['entry']) or {}).get('change')
        if ch is not None and not (isinstance(ch, dict) and ch.get('from_section_sha256') == c['row_sha256']
                                   and ch.get('to_section_sha256') == c['frozen_section_sha256'] and str(ch.get('what_changed', '')).strip()):
            raise Refuse('DISPOSITION_CHANGE_OBJECT %s' % c['entry'])
    want = sorted(set(['A%d' % n for n in later] + [c['entry'] for c in changed]), key=lambda x: int(x[1:]))
    have = sorted(seen, key=lambda x: int(x[1:]))
    if have != want:
        raise Refuse('DISPOSITION_ENTRIES %s must be exactly the entries after A%d plus the changed table rows %s'
                     % (have, newest, want))
    return {'dispositions': {'path': a.dispositions, 'sha256': a.dispositions_sha}, 'entries': have,
            'covered_later_names_for_v001': ','.join('A%d' % n for n in later), 'changed_table_rows': changed,
            'newest_table_row': 'A%d' % newest, 'container': 'object.dispositions' if isinstance(d, dict) else 'list'}


def c_dispositions(a):
    return _dispositions(a)


def c_rehash(a):
    """r5 seal_record_requirements[11] / entries_after_A81.section_rule: every row re-hashes from the frozen bytes, or carries a
    root disposition; every entry after the newest row carries a root disposition (dispositions JSON, validated by _dispositions)."""
    res = _dispositions(a)
    rows, changed, newest, later = _table_state(pin(a.prereg, a.prereg_sha, 'prereg_text_of_record'), pin(a.frozen, a.frozen_sha, 'frozen'))
    return {'table_rows_checked': len(rows), 'table_rows_unchanged': len(rows) - len(changed), 'changed_table_rows': changed,
            'entries_after_table': ['A%d' % n for n in later], 'dispositions': res}


def _exec_module(path, sha, name):
    import types
    src = pin(path, sha, name).decode('utf-8')
    m = types.ModuleType(name)
    m.__file__ = path
    sys.modules[name] = m
    exec(compile(src, path, 'exec'), m.__dict__)
    return m


def _fence(a, write_roots, forbid_runs_ext=True):
    import importlib.util
    import numpy                 # imported unfenced, before arming: the compare's own 'import numpy' then reuses this module
    pin(a.fence, a.fence_sha, 'fence')
    spec = importlib.util.spec_from_file_location('fence_c3sa_loaded', a.fence)
    F = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(F)
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
        path_policy(a.standin, must_exist=True, label='standin')
    F = _fence(a, write_roots=(a.outdir,), forbid_runs_ext=(a.mode == 'dryrun'))     # armed before the scan and the compare
    if a.mode == 'root':
        for run, d in sorted((m.get('identity_runs') or {}).items()):
            if C5H_NAME_CF in d.casefold() or os.path.islink(d) or not os.path.isdir(d):
                raise Refuse('IDENTITY_RUN_DIR %s not a real directory' % run)
            for side in (d + '.receipt.json', d + '.receipt.json.launch.json'):
                if os.path.islink(side):
                    raise Refuse('IDENTITY_RUN_SIDE_FILE_IS_A_SYMLINK %s' % side)
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
    if os.path.isfile(gj):
        out['gates_only_json'] = {'path': gj, 'sha256': sha_bytes(Path(gj).read_bytes())}
    if F.FENCE['refused'] or rc != 0 or out['gates_only_json'] is None:
        raise Refuse('GATES_ONLY_FAILED %r' % out)
    return out


def c_row_scan(a):
    t = Path(path_policy(a.path, True, 'e_seal1')).read_bytes().decode('utf-8')
    hit = ROW_VALUE_RX.search(t)
    if hit or not t.strip():
        raise Refuse('E_SEAL1_OUTPUT_EMPTY_OR_SHOWS_A_ROW_LIKE_VALUE (A47 I3)')
    return {'e_seal1': {'path': a.path, 'sha256': sha_bytes(t.encode('utf-8'))}, 'row_like_values': 0}


def c_check_tool4(a):
    st = Path(path_policy(a.stderr, True, 'tool4_stderr')).read_bytes().decode('utf-8')
    v = sjson(st.encode('utf-8'))
    ob = Path(path_policy(a.stdout, True, 'tool4_stdout')).read_bytes()
    if v.get('verdict') != 'PASS' or not ob or v.get('seal_record_sha256') != sha_bytes(ob):
        raise Refuse('TOOL4_NOT_PASS_OR_SHA_MISMATCH verdict %r stderr sha %r stdout sha %s' % (v.get('verdict'), v.get('seal_record_sha256'), sha_bytes(ob)))
    rec = sjson(ob)
    if rec.get('sealed_by') != AUTHORITY:
        raise Refuse('SEAL_RECORD_AUTHORITY')
    return {'candidate': {'path': a.stdout, 'sha256': sha_bytes(ob)}, 'tool4_seal_record_sha256': v['seal_record_sha256']}


def c_copy_x(a):
    b = pin(a.src, a.src_sha, 'src')
    return {'created': write_x(a.dst, b, 'dst')}


def _allow_from_build(text):
    sec = text.split(BUILD_HEADER + '\n', 1)[1].split('\n## ', 1)[0]
    pairs = re.findall(r'^([0-9a-f]{64})  (/\S+\.py)$', sec, re.M)
    d = {}
    for h, p in pairs:
        if p in d:
            raise Refuse('BUILD_ALLOWLIST_DUPLICATE %s' % p)
        d[p] = h
    return d


def c_make_config(a):
    """B8 / step 12: ROOT_SEAL_ADMISSION config (FORMAT_V005 item 2; guard v008 admission): schema, authority, seal, prereg and compare
    (exactly the SEAL_RECORD's), build (BUILD_V007), producer_allowlist = exactly BUILD_V007's 15 supported sources, which must equal
    ALLOWLIST_DRAFT_V006_CX3V001.txt and PRODUCER_INDEX_V009_CX3V001.json; then the real guard v008 admission() self-check."""
    seal = sjson(pin(a.seal, a.seal_sha, 'seal_record'))
    bt = pin(a.build, a.build_sha, 'build').decode('utf-8')
    allow = _allow_from_build(bt)
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
    if not (allow == al == pid) or len(allow) != a.n_sources:
        raise Refuse('ALLOWLIST_SETS_DIFFER build %d file %d index %d (want %d)' % (len(allow), len(al), len(pid), a.n_sources))
    for p, h in allow.items():
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
           'prereg': dict(seal['prereg']), 'compare': dict(seal['compare']), 'build': {'path': a.build, 'sha256': a.build_sha},
           'producer_allowlist': dict(allow)}
    ref = write_x(a.out, dumps(cfg), 'config')
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
            'allowlist_sources': len(allow)}


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
    sub('freeze', 'open', 'open-sha', 'out')
    sub('same-bytes', 'open', 'frozen', 'frozen-sha')
    sub('rehash-entries', 'prereg', 'prereg-sha', 'frozen', 'frozen-sha', 'dispositions', 'dispositions-sha')
    sub('dispositions', 'prereg', 'prereg-sha', 'frozen', 'frozen-sha', 'dispositions', 'dispositions-sha')
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
        'guard', 'guard-sha', 'launcher', 'launcher-sha', 'out', ints=('n-sources',))
    sub('make-receipt', 'config', 'config-sha', 'seal', 'seal-sha', 'out')
    argv = sys.argv[1:] if argv is None else argv
    flags = [x.split('=', 1)[0] for x in argv if x.startswith('--')]
    multi_ok = {'--pin', '--path', '--runtime', '--expect', '--ruling', '--identity-record'}
    if any(flags.count(f) > 1 for f in set(flags) - multi_ok):
        print(json.dumps({'verdict': 'REFUSE', 'code': 'CLI_REPEATED_FLAG'}), file=sys.stderr)
        return 2
    a = p.parse_args(argv)
    fn = {'pin': c_pin, 'absent': c_absent, 'freeze': c_freeze, 'same-bytes': c_same, 'rehash-entries': c_rehash, 'dispositions': c_dispositions,
          'driver-build-record': c_driver_build, 'fill-slots': c_fill, 'sealed-prereg': c_sealed_prereg,
          'sealed-compare': c_sealed_compare, 'check-manifest': c_check_manifest, 'make-c5h-manifest': c_make_c5h_manifest,
          'gates-only': c_gates_only, 'row-value-scan': c_row_scan, 'check-tool4': c_check_tool4, 'copy-exclusive': c_copy_x,
          'make-config': c_make_config, 'make-receipt': c_make_receipt}[a.cmd]
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

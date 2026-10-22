# make_helper_c3v010.py: Claude3 (FROM_CODEX/0642, A105). Derives tools/seal_steps_c3sa_c3v010.py from c3v009 (00079814) by exact
# replacements (each old string must occur exactly once; the make-config region is replaced whole); writes it exclusively.
import hashlib, sys
C3 = sys.argv[1]
src = open(C3 + '/tools/seal_steps_c3sa_c3v009.py', 'rb').read()
assert hashlib.sha256(src).hexdigest() == '000798141398d27308d95e7a25fc64d17abe9831c47a2b27457439b7bc7922a3'
s = src.decode('utf-8')
HDR = '''# c3v010 (FROM_CODEX/0642, A105; Claude4 0108 RP-S1, W7-S1): subcommand 'output-root' (check / create / verify): the step-2 output
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
'''
CONSTS = '''W7_ROWS = 15                                      # A105.1 / A78 N2: the admission allowlist is exactly BUILD_V007's 15 rows
W7_ROW_RX = re.compile(r'([0-9a-f]{64})  (/Users/\\S+)')   # one table row (fullmatch): sha, two spaces, an absolute path, no whitespace
VOLUME_ROOT = '/System/Volumes/Data'              # RP-S1 / RUNBOOK_V008 L37: the internal startup Data volume (st_dev compare)
'''
NEW_REGION = r'''def _build_table(text):
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


'''
R = [
 ('# c3v008 is superseded unused.\n', '# c3v008 is superseded unused.\n' + HDR),
 ('import argparse, ast, hashlib, json, os, re, stat as stat_mod, sys, time, types\n',
  'import argparse, ast, fcntl, hashlib, json, os, re, stat as stat_mod, sys, time, types\n'),
 ("BUILD_HEADER = '## Supported runtime entry allowlist'\n", "BUILD_HEADER = '## Supported runtime entry allowlist'\n" + CONSTS),
 (s[s.index('def _allow_from_build(text):'):s.index('def c_make_receipt(a):')], NEW_REGION),
 ("        'guard', 'guard-sha', 'launcher', 'launcher-sha', 'out', ints=('n-sources',))\n",
  "        'guard', 'guard-sha', 'launcher', 'launcher-sha', 'out')\n    sub('check-config-allowlist', 'config', 'config-sha', 'build', 'build-sha')\n"
  "    sub('output-root', 'path', 'mode', opt=('min-free-gib', 'expect-dev', 'expect-ino'))\n"),
 ("          'make-config': c_make_config, 'make-receipt': c_make_receipt}[a.cmd]\n",
  "          'make-config': c_make_config, 'make-receipt': c_make_receipt, 'check-config-allowlist': c_check_config_allowlist,\n"
  "          'output-root': c_output_root}[a.cmd]\n"),
]
for o, n in R:
    assert s.count(o) == 1, (o[:80], s.count(o))
    s = s.replace(o, n)
assert '_allow_from_build' not in s and 'n_sources' not in s
compile(s, 'seal_steps_c3sa_c3v010.py', 'exec', dont_inherit=True)
out = s.encode('utf-8')
with open(C3 + '/tools/seal_steps_c3sa_c3v010.py', 'xb') as f:
    f.write(out)
print('seal_steps_c3sa_c3v010.py', hashlib.sha256(out).hexdigest(), len(out))

# DRY RUN ONLY (Claude3 0639/0641 fix round, pass B). NOT A SEAL TOOL: the pinned runner run_pinned_c3sa_c3v003.py plus two in-process
# constant patches on the pinned check_slot_fill_c4v001 module, emulating fixes announced for v002/v003 so the dry run can exercise
# steps 4a-13: TEXT_OF_RECORD_SHA -> prereg r5 3245899f (v001 hard-pins r4), MS_KEYS += ('ddo_gas_M_s',) (D-01). Nothing else.
# Base description (unchanged runner semantics):
# Claude3 seal-assembly builder (FROM_CODEX/0639, SA-CX1-B2): run a pinned Python program from VERIFIED BYTES. Every pinned file (the main
# program and each sibling module it imports) is read ONCE (no-follow component walk, O_NOFOLLOW open, inode match), its sha256 checked,
# then compiled from exactly that buffer and exec'd into a fresh module. Sibling modules are pre-loaded into sys.modules in the order
# given, so the program's own 'import X' never reaches a finder or a loader; an import of an UNPINNED module that lives beside a pinned
# file is refused. No importlib loader runs pinned code and no bytecode cache is consulted (ROOT_SEAL_STEPS also passes
# -X pycache_prefix=<empty dir>, so even third-party loads inside the program, such as the compare's own importlib load of its pinned
# V005 compare, read source). The main program is exec'd under a non-__main__ name and its main() is called explicitly.
# usage: python3 -I -B -X pycache_prefix=P run_pinned_c3sa.py [--module NAME=PATH=SHA ...] --main PATH=SHA --call main|argv -- ARGS...
#   --call main: rc = main(ARGS)            --call argv: sys.argv = [PATH] + ARGS; rc = main()
# Exit: the program's return code (0 PASS); 2 on any refusal here (a JSON verdict on stderr).
import hashlib, importlib.machinery, json, os, stat as stat_mod, sys, types
# c3v002: importlib.machinery is imported here, before the guard is installed, and the guard is not re-entrant (c3v001 imported it
# inside find_spec, which re-entered the guard: a RecursionError instead of the typed refusal).
# c3v003 (SA-CX1-N1, 0641): the guard refuses any unpinned spec whose origin OR any submodule search location lies AT or UNDER a
# guarded folder, so a sibling package (regular or namespace) or a module inside one is refused too (c3v002 compared dirname only).

PROTECTED = ('kmax_a2f10_c5h_run_v001', '/runs_ext', 'runs_ext/', '/uvt_', '/.vol', 'sparc', 'ngc3198_target', 'ngc_target', 'rotmod')


class Refuse(Exception):
    pass


def read_pinned(path, sha, label):
    if not (isinstance(path, str) and path.startswith('/Users/') and '//' not in path and not path.endswith('/')):
        raise Refuse('PATH_SPELLING %s: %r' % (label, path))
    if any(x in path.casefold() for x in PROTECTED):
        raise Refuse('PATH_PROTECTED %s' % label)
    cur, st = '', None
    parts = path.split('/')[1:]
    for i, comp in enumerate(parts):
        if comp in ('', '.', '..'):
            raise Refuse('PATH_COMPONENT %s' % label)
        cur += '/' + comp
        st = os.lstat(cur)
        if stat_mod.S_ISLNK(st.st_mode):
            raise Refuse('PATH_HAS_SYMLINK_COMPONENT %s: %s (never followed)' % (label, cur))
        if i < len(parts) - 1 and not stat_mod.S_ISDIR(st.st_mode):
            raise Refuse('PATH_COMPONENT_NOT_A_DIRECTORY %s: %s' % (label, cur))
    if not stat_mod.S_ISREG(st.st_mode):
        raise Refuse('NOT_A_REGULAR_FILE %s' % label)
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        fs = os.fstat(fd)
        if (fs.st_dev, fs.st_ino) != (st.st_dev, st.st_ino):
            raise Refuse('PATH_CHANGED_DURING_READ %s' % label)
        chunks = []
        while True:
            b = os.read(fd, 1 << 20)
            if not b:
                break
            chunks.append(b)
    finally:
        os.close(fd)
    buf = b''.join(chunks)
    if hashlib.sha256(buf).hexdigest() != sha:
        raise Refuse('PIN_BYTES_MISMATCH %s: %s' % (label, path))
    return buf


def exec_buffer(buf, path, name):
    m = types.ModuleType(name)
    m.__file__ = path
    exec(compile(buf, path, 'exec', dont_inherit=True), m.__dict__)
    return m


class UnpinnedSiblingGuard:
    """meta-path guard: an import of a module that is NOT pinned but would be found beside a pinned file is refused."""
    def __init__(self, dirs):
        self.dirs = tuple(dirs)
        self.busy = False

    def find_spec(self, name, path=None, target=None):
        if self.busy:
            return None
        self.busy = True
        try:
            spec = importlib.machinery.PathFinder.find_spec(name, path)
        finally:
            self.busy = False
        if spec is None:
            return None
        locs = [getattr(spec, 'origin', None)] + list(getattr(spec, 'submodule_search_locations', None) or [])
        for loc in locs:
            if isinstance(loc, str) and any(loc == d or loc.startswith(d.rstrip('/') + '/') for d in self.dirs):
                raise ImportError('UNPINNED_SIBLING_IMPORT_REFUSED %s (%s)' % (name, loc))
        return None


def parse(argv):
    if '--' not in argv:
        raise Refuse('CLI: -- before the program arguments')
    k = argv.index('--')
    own, prog = argv[:k], argv[k + 1:]
    mods, main, call = [], None, None
    i = 0
    while i < len(own):
        f = own[i]
        if f == '--module' and i + 1 < len(own):
            n, rest = own[i + 1].split('=', 1)
            p, h = rest.rsplit('=', 1)
            mods.append((n, p, h))
        elif f == '--main' and i + 1 < len(own) and main is None:
            p, h = own[i + 1].rsplit('=', 1)
            main = (p, h)
        elif f == '--call' and i + 1 < len(own) and call is None and own[i + 1] in ('main', 'argv'):
            call = own[i + 1]
        else:
            raise Refuse('CLI: %r' % f)
        i += 2
    if main is None or call is None or len({m[0] for m in mods}) != len(mods):
        raise Refuse('CLI: --main and --call once each; module names unique')
    return mods, main, call, prog


def _shim_patch(m):                                   # DRY RUN ONLY
    m.TEXT_OF_RECORD_SHA = '3245899f68081a48928a7242a1d9f1ee3694bb13b3f04913dcb2825104a93393'
    m.MS_KEYS = tuple(m.MS_KEYS) + ('ddo_gas_M_s',)


def run(argv):
    mods, (mp, mh), call, prog = parse(argv)
    bufs = [(n, p, read_pinned(p, h, n)) for n, p, h in mods]       # every pinned file read once, before anything executes
    mbuf = read_pinned(mp, mh, 'main')
    sys.meta_path.insert(0, UnpinnedSiblingGuard({os.path.dirname(p) for _, p, _ in bufs} | {os.path.dirname(mp)}))
    for n, p, b in bufs:
        if n in sys.modules:
            raise Refuse('MODULE_ALREADY_LOADED %s' % n)
        sys.modules[n] = exec_buffer(b, p, n)
        if n == 'check_slot_fill_c4v001':
            _shim_patch(sys.modules[n])
    sys.argv = [mp] + list(prog)
    main = exec_buffer(mbuf, mp, '__c3sa_main__')
    if os.path.basename(mp) == 'check_slot_fill_c4v001.py':
        _shim_patch(main)
    sys.modules['__c3sa_main__'] = main
    rc = main.main(list(prog)) if call == 'main' else main.main()
    return 0 if rc is None else rc


if __name__ == '__main__':
    try:
        rc = run(sys.argv[1:])
    except Refuse as e:
        print(json.dumps({'runner': 'run_pinned_c3sa', 'verdict': 'REFUSE', 'code': str(e)}), file=sys.stderr)
        rc = 2
    sys.exit(rc if isinstance(rc, int) else 1)

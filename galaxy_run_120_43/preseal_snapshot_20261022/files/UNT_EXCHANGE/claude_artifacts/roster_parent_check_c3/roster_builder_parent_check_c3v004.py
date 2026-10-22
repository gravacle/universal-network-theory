"""Backlog #7 (A272 hardening; Claude3, D038) c3v004: --out-dir checks BEFORE the step-7 ledger commit.

The roster builder's step7 and custody commands write the ledger entry STEP7_<seq>.json ("the commit point":
roster builder L2039, L3466) and only THEN create --out-dir (L2347, L4506). So if --out-dir already exists (step7
has no pre-check), or its parent is missing, is not a directory or is not writable, the command fails AFTER the
commit: the ledger has advanced, but STEP7_RESULT.json / CUSTODY_RESULT.json and REPLAY_PLAN.json were never
written (a mid-ledger refusal). This entry refuses exactly those conditions first, before any input is read or any
ledger entry is written. Otherwise it runs the UNCHANGED base main, loaded from its pinned bytes with the base's own
__file__, so own_pin() and every byte the base writes are the same as in a direct run. Every other command, and any
argv that is not a well-formed step7/custody call, goes to the base main untouched.

c3v002 (Codex1 review B7-1): the parent is checked by the kernel's resolution of the RAW prefix of --out-dir, exactly
as os.mkdir resolves it. c3v001 used os.path.abspath, which collapses '..' lexically BEFORE symlink traversal and so
could name a different parent: it refused a valid call and admitted one whose real parent was missing.
c3v003 (Codex1 delta review B7-2): with a trailing slash, mkdir follows a symlink at the name and creates its final
target, so a dangling link whose target parent exists is valid. c3v002 refused it as OUT_DIR_EXISTS. The target is
now resolved with os.path.realpath (kernel-order symlink and '..' resolution) and its own parent is checked; a link
that resolves to an existing entry, or a chain that does not resolve (a loop), stays OUT_DIR_EXISTS.
c3v004 (Codex1 delta review B7-3): non-strict realpath drops a missing or non-directory component before '..', so
c3v003 passed a link to 'component/../made' that mkdir then fails. The link is now followed by its RAW readlink
target joined to the link's raw directory, and the same rules are applied again (at most 32 links, the macOS
MAXSYMLINKS; more is ELOOP), so the kernel's own stat walks every raw component.

usage (root): python3 -I -B roster_builder_parent_check_c3v004.py <exactly the argv of the base roster builder>
"""
import hashlib
import json
import os
import stat
import sys
import types

BASE = {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/roster_builder_c2v007_cx3cw8v003.py',
        'sha256': 'f710334b6f5ec2663fbebd826c7b326ebf7ff9eb600e751584de4f518a4e0b11'}
LEDGER_COMMANDS = ('step7', 'custody')
LEDGER_USAGE = {'--input', '--input-sha256', '--out-dir'}


def read_base():
    fd = os.open(BASE['path'], os.O_RDONLY | os.O_NOFOLLOW)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise ValueError('BASE_NOT_REGULAR')
        chunks = []
        while True:
            b = os.read(fd, 1 << 20)
            if not b:
                break
            chunks.append(b)
    finally:
        os.close(fd)
    raw = b''.join(chunks)
    if hashlib.sha256(raw).hexdigest() != BASE['sha256']:
        raise ValueError('BASE_PIN_MISMATCH')
    return raw


def load_base():
    raw = read_base()
    module = types.ModuleType('roster_builder_c2v007_cx3cw8v003')
    module.__file__ = BASE['path']
    exec(compile(raw, BASE['path'], 'exec'), module.__dict__)
    return module


MAX_LINKS = 32


def preflight(out_dir, _links=0):
    """The conditions under which the base's post-commit os.mkdir(--out-dir) fails; None if clear. No abspath,
    normpath or realpath of any path: the kernel's stat resolves symlinks and '..' in the raw strings as mkdir does.
    An existing entry at the name (lstat, trailing slashes removed) is OUT_DIR_EXISTS, except a symlink named WITH a
    trailing slash: mkdir then follows it, so its raw target (joined to the link's raw directory) is checked by the
    same rules, keeping the trailing slash."""
    name = out_dir.rstrip('/') or '/'
    if os.path.lexists(name):
        if name != out_dir and os.path.islink(name):
            if _links >= MAX_LINKS:
                return 'OUT_DIR_EXISTS'                 # ELOOP
            target = os.path.join(os.path.dirname(name), os.readlink(name))
            return preflight(target.rstrip('/') + '/', _links + 1)
        return 'OUT_DIR_EXISTS'
    return _parent_problem(os.path.dirname(name) or '.')


def _parent_problem(parent):
    if not os.path.isdir(parent):
        return 'OUT_DIR_PARENT_MISSING'
    if not os.access(parent, os.W_OK | os.X_OK):
        return 'OUT_DIR_PARENT_NOT_WRITABLE'
    return None


def main(argv):
    try:
        base = load_base()
    except (OSError, ValueError) as exc:
        print(json.dumps({'refused': 'BASE_PIN', 'detail': '%s: %s' % (type(exc).__name__, exc)}), file=sys.stderr)
        return 2
    if argv and argv[0] in LEDGER_COMMANDS:
        try:
            cmd, args = base._parse_args(argv)
        except base.Refused:
            cmd, args = None, {}
        if cmd in LEDGER_COMMANDS and set(args) == LEDGER_USAGE:
            code = preflight(args['--out-dir'])
            if code is not None:
                print(json.dumps({'refused': code, 'detail': args['--out-dir']}), file=sys.stderr)
                return 2
    return base.main(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

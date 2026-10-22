"""Backlog #7 (A272 hardening; Claude3, D038): --out-dir checks BEFORE the step-7 ledger commit.

The roster builder's step7 and custody commands write the ledger entry STEP7_<seq>.json ("the commit point":
roster builder L2039, L3466) and only THEN create --out-dir (L2347, L4506). So if --out-dir already exists (step7
has no pre-check), or its parent is missing, is not a directory or is not writable, the command fails AFTER the
commit: the ledger has advanced, but STEP7_RESULT.json / CUSTODY_RESULT.json and REPLAY_PLAN.json were never
written (a mid-ledger refusal). This entry refuses exactly those conditions first, before any input is read or any
ledger entry is written. Otherwise it runs the UNCHANGED base main, loaded from its pinned bytes with the base's own
__file__, so own_pin() and every byte the base writes are the same as in a direct run. Every other command, and any
argv that is not a well-formed step7/custody call, goes to the base main untouched.

usage (root): python3 -I -B roster_builder_parent_check_c3v001.py <exactly the argv of the base roster builder>
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


def preflight(out_dir):
    """Exactly the conditions under which the base's post-commit os.mkdir(--out-dir) must fail; None if clear."""
    if os.path.lexists(out_dir):
        return 'OUT_DIR_EXISTS'
    parent = os.path.dirname(os.path.abspath(out_dir))
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

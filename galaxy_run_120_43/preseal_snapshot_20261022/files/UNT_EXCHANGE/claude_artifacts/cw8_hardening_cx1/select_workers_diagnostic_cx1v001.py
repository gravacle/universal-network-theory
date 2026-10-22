"""D034 root-invoked select-workers entry. Diagnostics grant no launch authority.

This entry loads byte-pinned, unchanged cw8 v003, accepts only select-workers,
and delegates its CLI and choice contracts. --refusal-record is explicit and
optional. ROOT/FILE/IDENTITY lock refusals can produce diagnostic evidence only.
No launch command is exposed.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import types

TOOL = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/phase1_ngc_launch_cx3cw8v003.py')
TOOL_SHA = '4d5b47e75f90241460dd0b86155ddae2267117c31f6043fc57777ea94564919d'
LOCK_CODES = frozenset({'CW8_CHOICE_LOCK_ROOT', 'CW8_CHOICE_LOCK_FILE', 'CW8_CHOICE_LOCK_IDENTITY'})


def load_tool():
    raw = TOOL.read_bytes()
    if hashlib.sha256(raw).hexdigest() != TOOL_SHA:
        raise ValueError('CW8_DIAGNOSTIC_TOOL_PIN')
    module = types.ModuleType('cw8_diagnostic_pinned_tool')
    module.__file__ = str(TOOL)
    exec(compile(raw, str(TOOL), 'exec'), module.__dict__)
    return module


def destination_check(M, ctx, destination):
    M.need(type(destination) is str and destination.startswith('/') and
           os.path.normpath(destination) == destination,
           'CW8_REFUSAL_RECORD_PATH')
    path = Path(destination)
    M.need('worker_choices' not in path.parts, 'CW8_REFUSAL_RECORD_CHOICE_DIRECTORY')
    M.need(path.parent.is_dir() and os.path.realpath(path.parent) == str(path.parent),
           'CW8_REFUSAL_RECORD_PARENT')
    root = Path(ctx.cfg['p112_launch_root'])
    M.need(root.is_dir() or (path != root and root not in path.parents),
           'CW8_REFUSAL_RECORD_MISSING_ROOT')
    M.need(not os.path.lexists(path), 'CW8_REFUSAL_RECORD_EXISTS')
    return path


def select_with_refusal(M, selector, ctx, forecast_pin=None, *, refusal_record=None):
    path = destination_check(M, ctx, refusal_record) if refusal_record is not None else None
    try:
        return selector(ctx, forecast_pin)
    except M.Refusal as exc:
        if path is None or exc.code not in LOCK_CODES:
            raise
        own_path = Path(__file__).resolve()
        record = {'schema': 'CW8_LOCK_REFUSAL_RECORD_V001',
                  'utc': ctx.system.utc(), 'refusal_code': exc.code,
                  'refusal_text': str(exc), 'launch_root': ctx.cfg['p112_launch_root'],
                  'lock_path': str(Path(ctx.cfg['p112_launch_root']) / '.worker_choices.lock'),
                  'config_pin': ctx.config_pin,
                  'tool_pin': {'path': str(own_path), 'sha256': hashlib.sha256(own_path.read_bytes()).hexdigest()},
                  'worker_choices_written': False}
        # Recheck immediately before exclusive publication. Never replace a file.
        destination_check(M, ctx, str(path))
        data = (json.dumps(record, sort_keys=True, allow_nan=False, indent=2) + '\n').encode()
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o444)
        with os.fdopen(fd, 'wb') as out:
            out.write(data)
            out.flush()
            os.fsync(out.fileno())
        parent_fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            os.fsync(parent_fd)
        finally:
            os.close(parent_fd)
        raise  # Preserve the original lock refusal; diagnostic is not selection.


def cli(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['select-workers'])
    parser.add_argument('--refusal-record')
    args, rest = parser.parse_known_args(argv)
    M = load_tool()
    original = M.select_workers
    def guarded(ctx, forecast_pin=None):
        return select_with_refusal(M, original, ctx, forecast_pin, refusal_record=args.refusal_record)
    M.select_workers = guarded
    return M.cli([args.command] + rest)


if __name__ == '__main__':
    sys.exit(cli())

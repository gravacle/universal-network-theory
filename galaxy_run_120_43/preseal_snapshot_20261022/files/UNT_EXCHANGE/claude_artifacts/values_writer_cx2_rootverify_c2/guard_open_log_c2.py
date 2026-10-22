"""Root-verify (Claude2) open guard for values writer v004 checks. Synthetic only.

Runs one script (runpy, __main__) under a parent-process audit hook that LOGS every file open, directory listing and
subprocess, and REFUSES:
  - any path with 'ngc3198' in any component (case-folded), any path under ~/.codex, any V007_POSTSEAL_RECORDS path;
  - any write outside --work (and the --log file itself);
  - any non-.py read under /Users/bgm/Research outside --work and the --allow files/dirs.
Writes one log (exclusive create) at --log. Child processes are not hooked; their argv is logged.
"""
import argparse
import hashlib
import json
import os
import runpy
import subprocess
import sys
from pathlib import Path

RESEARCH = '/Users/bgm/Research/'
CODEX = os.path.expanduser('~/.codex')
WRITE_FLAGS = os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--script', required=True)
    ap.add_argument('--work', required=True)
    ap.add_argument('--log', required=True)
    ap.add_argument('--allow', action='append', default=[])
    ap.add_argument('rest', nargs=argparse.REMAINDER)
    a = ap.parse_args()
    work = Path(a.work).resolve()
    log = Path(a.log).resolve()
    allow = [Path(x).resolve() for x in a.allow]
    runtime = [Path(sys.prefix).resolve(), Path(sys.base_prefix).resolve()]
    py_reads, data_reads, other_reads, writes, refused, listings, subprocs = set(), set(), set(), set(), [], set(), []

    def deny(kind, p):
        refused.append({'kind': kind, 'path': str(p)})
        raise PermissionError('ROOTVERIFY_GUARD_' + kind + ': ' + str(p))

    def hook(event, args):
        if event == 'open':
            path, mode, flags = args
            if not isinstance(path, (str, bytes, os.PathLike)):
                return
            p = Path(os.fsdecode(path)).resolve()
            s = str(p)
            if any('ngc3198' in part.casefold() for part in p.parts):
                deny('NGC3198_NAMED_PATH', s)
            if s == CODEX or s.startswith(CODEX + os.sep):
                deny('CODEX_CACHE', s)
            if 'V007_POSTSEAL_RECORDS' in s:
                deny('V007_POSTSEAL_RECORDS', s)
            is_write = (isinstance(mode, str) and any(c in mode for c in 'wax+')) or \
                       (isinstance(flags, int) and bool(flags & WRITE_FLAGS))
            if is_write:
                if p == log or p.is_relative_to(work):
                    writes.add(s)
                    return
                deny('WRITE_OUTSIDE_WORK', s)
            if p.is_relative_to(work):
                return
            if s.startswith(RESEARCH):
                if any(p == x or p.is_relative_to(x) for x in allow):
                    data_reads.add(s)
                    return
                if p.suffix == '.py':
                    py_reads.add(s)
                    return
                deny('RESEARCH_NON_PY_READ', s)
            if not any(p.is_relative_to(r) for r in runtime) and not s.startswith('/dev/'):
                other_reads.add(s)
        elif event in ('os.listdir', 'os.scandir'):
            pth = args[0] if args else None
            if isinstance(pth, (str, bytes, os.PathLike)):
                s = str(Path(os.fsdecode(pth)).resolve())
                if s.startswith(RESEARCH) and not Path(s).is_relative_to(work):
                    listings.add(s)
        elif event == 'subprocess.Popen':
            subprocs.append([os.fsdecode(x) if isinstance(x, (str, bytes, os.PathLike)) else repr(x)
                             for x in (args[1] if isinstance(args[1], (list, tuple)) else [args[1]])])

    sys.addaudithook(hook)
    rest = a.rest[1:] if a.rest[:1] == ['--'] else a.rest
    sys.argv = [a.script] + rest
    code = 0
    try:
        runpy.run_path(a.script, run_name='__main__')
    except SystemExit as e:
        code = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
    pins = [{'path': p, 'sha256': hashlib.sha256(Path(p).read_bytes()).hexdigest()} for p in sorted(py_reads)
            if Path(p).is_file()]
    d = {'schema': 'C2_ROOTVERIFY_OPEN_LOG_V001',
         'date_u': subprocess.check_output(['/bin/date', '-u'], text=True).strip(),
         'script': {'path': str(Path(a.script).resolve()),
                    'sha256': hashlib.sha256(Path(a.script).read_bytes()).hexdigest()},
         'argv': rest, 'work': str(work), 'allow': [str(x) for x in allow], 'exit_code': code,
         'py_code_reads_under_research': pins, 'allowed_data_reads': sorted(data_reads),
         'other_reads_outside_runtime': sorted(other_reads), 'writes_count': len(writes),
         'writes_outside_work': sorted(w for w in writes if not Path(w).is_relative_to(work)),
         'refused': refused, 'research_listings_outside_work': sorted(listings), 'subprocesses': subprocs,
         'guard_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'flags': {'isolated': sys.flags.isolated, 'dont_write_bytecode': sys.flags.dont_write_bytecode}}
    with open(log, 'x') as f:
        json.dump(d, f, indent=1)
        f.write('\n')
    print('GUARD exit %s; refused %d; py reads %d; data reads %d' % (code, len(refused), len(pins), len(data_reads)))
    return code


if __name__ == '__main__':
    sys.exit(main())

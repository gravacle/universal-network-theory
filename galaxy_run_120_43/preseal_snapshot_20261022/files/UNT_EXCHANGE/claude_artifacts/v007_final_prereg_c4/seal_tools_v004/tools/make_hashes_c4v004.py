# Claude4 seal tools v004 (BUILD helper; A110, dispatch 0646): write HASHES_SEAL_TOOLS_C4V004.txt (exclusive create, written last): the sha256
# and size, from bytes, of every file in this folder except itself, in four blocks: the files of record (the six sources, the tests, the README
# and the DELTA), every file of the final run folder tests/<RUN>/, the tools/ files (the fence and runner copies and the build helpers), and
# dev/ (work copies, not of record). os.walk does not follow links (this folder holds none). Writes nothing else.
# usage: python3 -I -B run_fenced_c4st2.py make_hashes_c4v004.py RUN_NAME
import hashlib, os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent.parent
OUT = 'HASHES_SEAL_TOOLS_C4V004.txt'
TOP = ['build_seal_record_c4v004.py', 'seal_common_c4v003.py', 'check_frozen_addendum_c4v003.py', 'check_sealed_compare_c4v003.py',
       'check_slot_fill_c4v003.py', 'print_driver_build_record_c4v003.py', 'tests/test_seal_tools_c4v004.py', 'README_SEAL_TOOLS_V004_DELTA.md',
       'DELTA_V003_TO_V004.md']


def line(rel):
    raw = (HERE / rel).read_bytes()
    return '%s  %10d  %s\n' % (hashlib.sha256(raw).hexdigest(), len(raw), rel)


def files_under(rel):
    out = []
    for dirpath, dirnames, filenames in os.walk(HERE / rel):
        dirnames.sort()
        for fn in sorted(filenames):
            out.append(str(Path(dirpath, fn).relative_to(HERE)))
    return out


def main():
    run = sys.argv[1]
    rd = HERE / 'tests' / run
    assert rd.is_dir() and (rd / 'TEST_RESULTS_C4V004.json').is_file(), rd
    assert not (HERE / OUT).exists()
    every = set(files_under('.'))
    runfiles = files_under('tests/' + run)
    toolfiles = files_under('tools')
    devfiles = files_under('dev')
    listed = TOP + runfiles + toolfiles + devfiles
    assert len(set(listed)) == len(listed) and set(listed) == every, sorted(every ^ set(listed))[:10]
    out = ['# sha256  bytes  path (relative to %s); every file of seal tools v004 from bytes, written last\n' % HERE,
           '# the files of record\n'] + [line(r) for r in TOP]
    out.append('# the final suite run folder tests/%s (%d files)\n' % (run, len(runfiles)))
    out += [line(r) for r in runfiles]
    out.append('# tools/: the fence and runner (byte copies of v003) and the build helpers (%d files)\n' % len(toolfiles))
    out += [line(r) for r in toolfiles]
    out.append('# dev/: work copies, NOT of record (%d files)\n' % len(devfiles))
    out += [line(r) for r in devfiles]
    with open(HERE / OUT, 'x') as f:
        f.write(''.join(out))
    print(len(TOP), 'of record;', len(runfiles), 'run files;', len(toolfiles), 'tools;', len(devfiles), 'dev')


if __name__ == '__main__':
    main()

# Claude4 seal tools v003 (BUILD helper, continuation run 3): write HASHES_SEAL_TOOLS_C4V003.txt (exclusive create, written last): the sha256
# and size, from bytes, of every published file at the top level of this folder (the six sources, tests/test_seal_tools_c4v003.py, every file
# of the final run folder tests/<RUN>/, README_SEAL_TOOLS_V003.md, DELTA_V002R2_TO_V003.md, MUTATION_C4V003.json), then, in a separate block,
# the supporting tools/ files the README cites (not of record). dev/, mutants/, fixtures/, out/ and PARTIAL.md are work files and are not listed.
# usage: python3 -I -B run_fenced_c4st2.py make_hashes_c4v003.py RUN_NAME
import hashlib, os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent.parent
TOP = ['seal_common_c4v003.py', 'check_frozen_addendum_c4v003.py', 'check_sealed_compare_c4v003.py', 'check_slot_fill_c4v003.py',
       'build_seal_record_c4v003.py', 'print_driver_build_record_c4v003.py', 'tests/test_seal_tools_c4v003.py', 'README_SEAL_TOOLS_V003.md',
       'DELTA_V002R2_TO_V003.md', 'MUTATION_C4V003.json']
TOOLS = ['tools/fence_c4v002.py', 'tools/run_fenced_c4st2.py', 'tools/make_mutants_final_c4v003.py', 'tools/run_one_mutant_c4v003.sh',
         'tools/analyze_mutants_final_c4v003.py', 'tools/make_delta_c4v003.py', 'tools/delta_reasons_c4v003.py', 'tools/publish_c4v003.py',
         'tools/make_hashes_c4v003.py']


def line(rel):
    p = HERE / rel
    raw = p.read_bytes()
    return '%s  %10d  %s\n' % (hashlib.sha256(raw).hexdigest(), len(raw), rel)


def main():
    run = sys.argv[1]
    rd = HERE / 'tests' / run
    assert rd.is_dir() and (rd / 'TEST_RESULTS_C4V003.json').is_file(), rd
    runfiles = []
    for dirpath, dirnames, filenames in os.walk(rd):
        dirnames.sort()
        for fn in sorted(filenames):
            runfiles.append(str(Path(dirpath, fn).relative_to(HERE)))
    out = ['# sha256  bytes  path (relative to %s); every published file of seal tools v003, from bytes, written last\n' % HERE]
    out += [line(r) for r in TOP]
    out.append('# the final suite run folder tests/%s (%d files)\n' % (run, len(runfiles)))
    out += [line(r) for r in runfiles]
    out.append('# supporting tools cited by the README (not of record)\n')
    out += [line(r) for r in TOOLS]
    with open(HERE / 'HASHES_SEAL_TOOLS_C4V003.txt', 'x') as f:
        f.write(''.join(out))
    print(len(TOP) + len(runfiles), 'published files;', len(TOOLS), 'supporting tools')


if __name__ == '__main__':
    main()

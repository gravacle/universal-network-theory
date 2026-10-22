# Claude4 seal tools v003 (BUILD helper, continuation run 3): publish dev/ work copies at the top level of this folder by exclusive create.
# Each published file's bytes are the dev file's bytes, read once, written once with open(..., 'xb'), then re-read and compared by sha256.
# Phase 'code': the six sources and tests/test_seal_tools_c4v003.py. Phase 'docs': README_SEAL_TOOLS_V003.md (from the filled dev copy
# dev/README_SEAL_TOOLS_V003.filled.md), DELTA_V002R2_TO_V003.md (dev/delta/) and MUTATION_C4V003.json (from dev/MUTATION_C4V003_ROUND2.json).
# Refuses (exit 2) if any target exists.
# Writes nothing else. No process, no network, no delete.
# usage: python3 -I -B run_fenced_c4st2.py publish_c4v003.py code|docs
import hashlib, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent.parent
DEV = HERE / 'dev'
PHASES = {
    'code': [('seal_common_c4v003.py', 'seal_common_c4v003.py'), ('check_frozen_addendum_c4v003.py', 'check_frozen_addendum_c4v003.py'),
             ('check_sealed_compare_c4v003.py', 'check_sealed_compare_c4v003.py'), ('check_slot_fill_c4v003.py', 'check_slot_fill_c4v003.py'),
             ('build_seal_record_c4v003.py', 'build_seal_record_c4v003.py'), ('print_driver_build_record_c4v003.py', 'print_driver_build_record_c4v003.py'),
             ('tests/test_seal_tools_c4v003.py', 'tests/test_seal_tools_c4v003.py')],
    'docs': [('README_SEAL_TOOLS_V003.filled.md', 'README_SEAL_TOOLS_V003.md'), ('delta/DELTA_V002R2_TO_V003.md', 'DELTA_V002R2_TO_V003.md'),
             ('MUTATION_C4V003_ROUND2.json', 'MUTATION_C4V003.json')],
}


def main():
    phase = sys.argv[1]
    pairs = PHASES[phase]
    for _, dst in pairs:
        if (HERE / dst).exists():
            print('REFUSED: %s exists' % dst)
            raise SystemExit(2)
    for src, dst in pairs:
        raw = (DEV / src).read_bytes()
        h = hashlib.sha256(raw).hexdigest()
        with open(HERE / dst, 'xb') as f:
            f.write(raw)
        back = hashlib.sha256((HERE / dst).read_bytes()).hexdigest()
        if back != h:
            print('REFUSED: %s re-reads as %s, dev %s' % (dst, back, h))
            raise SystemExit(2)
        print('%s  %s  (= dev/%s)' % (h, dst, src))


if __name__ == '__main__':
    main()

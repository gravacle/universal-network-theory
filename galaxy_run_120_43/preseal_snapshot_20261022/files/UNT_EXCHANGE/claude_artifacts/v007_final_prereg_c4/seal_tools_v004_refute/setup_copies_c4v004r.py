# Claude4 seal tools v004 REFUTE stage (helper of lane Claude4; A110, dispatch 0646): byte copies, by exclusive create, of
#  - the v004 fence and fenced runner into tools/ (so the fence's review root is THIS refute folder: every write of a fenced run lands here),
#  - the six v004 tool files and the v004 suite into v004/ (the suite tests the tools beside it: TOOLS = parent of tests/).
# Every source sha is checked from bytes before the copy and every copy after it. Reads only; writes only under this folder.
# usage: python3 -I -B setup_copies_c4v004r.py
import hashlib, os, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
V4 = HERE.parent / 'seal_tools_v004'
V3 = HERE.parent / 'seal_tools_v003'
PLAN = [  # (source, destination relative to HERE, expected sha256)
    (V4 / 'tools/fence_c4v002.py', 'tools/fence_c4v002.py', 'c993d34c185d785d77c443a00033e8efeea10cd02f1a547a99af458c0f698eb5'),
    (V4 / 'tools/run_fenced_c4st2.py', 'tools/run_fenced_c4st2.py', 'fe904509c7d2d6300042589aaa02d839e82b436680d293b65c5c7d4cf69f6d25'),
    (V4 / 'seal_common_c4v003.py', 'v004/seal_common_c4v003.py', '101a3aeb9846a21c35993e8e7e4b50a8f1206ed4202b131afd12d7e496c5ab21'),
    (V4 / 'check_frozen_addendum_c4v003.py', 'v004/check_frozen_addendum_c4v003.py', 'a56f8d793750151920b1b47e77b46aebbfadea71fe77730f360beb02af788fb4'),
    (V4 / 'check_sealed_compare_c4v003.py', 'v004/check_sealed_compare_c4v003.py', 'c2c5dfc5ddba1e44ff82811a38d4c05b0a669f2294b229efe3437623d596f9f1'),
    (V4 / 'check_slot_fill_c4v003.py', 'v004/check_slot_fill_c4v003.py', '316973a1abf5aa2151dc1a517733d970ce1004313395d05fe590f82ed439b0af'),
    (V4 / 'print_driver_build_record_c4v003.py', 'v004/print_driver_build_record_c4v003.py', 'e5bedffe3c91650d5dba7fbd1ed5476e228158679d8959dfea0e2eff436ebdea'),
    (V4 / 'build_seal_record_c4v004.py', 'v004/build_seal_record_c4v004.py', '9787cf587ca3e9a92c24587a9c5ea56568b808f53c48acf739eea71b997ceb41'),
    (V4 / 'tests/test_seal_tools_c4v004.py', 'v004/tests/test_seal_tools_c4v004.py', 'ee237685e24d6efd799f441a4e7340009e1bc65064f86b62d5be6071dfa417e8'),
]
# the five unchanged files must also be v003's bytes (v003 SELECTED cf7e5b2f pins)
V3_SAME = {'seal_common_c4v003.py', 'check_frozen_addendum_c4v003.py', 'check_sealed_compare_c4v003.py', 'check_slot_fill_c4v003.py',
           'print_driver_build_record_c4v003.py'}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    out = []
    for src, rel, h in PLAN:
        raw = src.read_bytes()
        if sha(raw) != h:
            sys.stderr.write('REFUSED: %s hashes to %s, expected %s\n' % (src, sha(raw), h))
            return 2
        if src.name in V3_SAME and sha((V3 / src.name).read_bytes()) != h:
            sys.stderr.write('REFUSED: v003 %s is not %s\n' % (src.name, h))
            return 2
        dst = (HERE / rel)
        assert str(dst.resolve().parent).startswith(str(HERE)), dst
        dst.parent.mkdir(parents=True, exist_ok=True)
        with open(dst, 'xb') as f:
            f.write(raw)
        got = sha(dst.read_bytes())
        if got != h:
            sys.stderr.write('REFUSED: copy %s hashes to %s\n' % (dst, got))
            return 2
        out.append('%s  %s  (copy of %s)' % (got, rel, src))
    print('\n'.join(out))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

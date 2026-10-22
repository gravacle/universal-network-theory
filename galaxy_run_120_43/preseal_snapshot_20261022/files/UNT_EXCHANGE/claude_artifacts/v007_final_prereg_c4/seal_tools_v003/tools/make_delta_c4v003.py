# Claude4 seal tools v003 (BUILD helper): DELTA_V002R2_TO_V003.md, every changed line of the six v003 sources against the r2 bytes, each
# hunk with its reason. The diff is difflib.unified_diff(n=0) over lines; a hunk whose '+' lines are exactly its '-' lines with c4v002 ->
# c4v003 is classed 'rename' mechanically; every other hunk takes its reason from REASONS below, keyed by (file, the hunk's first changed
# line), and the run fails if any hunk has no reason or any REASONS key is unused. The r2 inputs are verified from bytes first.
# usage: python3 -I -B make_delta_c4v003.py SRC_DIR OUT.md   (SRC_DIR holds the six *_c4v003.py files; OUT.md is created exclusively)
import difflib, hashlib, sys
from pathlib import Path
R2 = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2')
R2_PINS = {'seal_common_c4v002.py': 'f41b0fca51a95387577839e52308a2dc6ccb79b1e6b9283f389b54c7f348dc10',
           'check_frozen_addendum_c4v002.py': '06a98bc6b56e71bff450b749b12a7e8978824baeda41458e4319506a0cfd1891',
           'check_sealed_compare_c4v002.py': 'aebb7b731a800e558b13a5f290c7fac062183cb9ba092af45df4e6bda1f390cf',
           'check_slot_fill_c4v002.py': '806733fb18e167275a1de62ebc9433fecf632cc16393933801fd4c9e53cddffb',
           'build_seal_record_c4v002.py': '4192983d262e2a27a3d9c90681b6ee66a90c901bfe2f99a7dce2349bc8c5de52',
           'print_driver_build_record_c4v002.py': 'fde0b26e7ea26d4ad15213cc9c3115a807179616e0e155037c97d2179db7a673'}
REASONS = {}          # (v003 file, first changed line, stripped) -> (tag, why); filled from REASON_ROWS
REASON_ROWS = []      # set by the caller module REASONS_C4V003 (tools/delta_reasons_c4v003.py)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def hunks(a, b):
    """[(a_start, a_lines, b_start, b_lines)] from SequenceMatcher opcodes (n=0 context)"""
    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag != 'equal':
            out.append((i1, a[i1:i2], j1, b[j1:j2]))
    return out


def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import delta_reasons_c4v003 as RR
    for f, first, tag, why in RR.ROWS:
        REASONS[(f, first.strip())] = (tag, why)
    used = set()
    lines_out = []
    totals = {}
    for r2name, h in R2_PINS.items():
        ra = (R2 / r2name).read_bytes()
        assert sha(ra) == h, r2name
        v3name = r2name.replace('c4v002', 'c4v003')
        rb = (src / v3name).read_bytes()
        a = ra.decode('utf-8').splitlines()
        b = rb.decode('utf-8').splitlines()
        hs = hunks(a, b)
        lines_out.append('\n## `%s`\n\nr2 `%s` (%d lines) -> v003 `%s` (%d lines), %d hunks.\n' % (v3name, h[:8], len(a), sha(rb)[:8], len(b), len(hs)))
        for k, (i1, al, j1, bl) in enumerate(hs, 1):
            if len(al) == len(bl) and al and all(x.replace('c4v002', 'c4v003') == y for x, y in zip(al, bl)):
                tag, why = 'rename', 'v002 -> v003 module, check-name or usage rename only'
            else:
                first = (bl[0] if bl else al[0]).strip()
                key = (v3name, first)
                if key not in REASONS:
                    raise SystemExit('NO REASON for %s hunk %d, first changed line: %r' % (v3name, k, first))
                used.add(key)
                tag, why = REASONS[key]
            totals[tag] = totals.get(tag, 0) + 1
            span_a = 'r2 L%d-%d' % (i1 + 1, i1 + len(al)) if al else 'r2 after L%d' % i1
            span_b = 'v003 L%d-%d' % (j1 + 1, j1 + len(bl)) if bl else 'v003 after L%d' % j1
            lines_out.append('### %s hunk %d: %s, %s -- **%s**\n\n%s\n\n```diff\n%s\n```\n' % (
                v3name, k, span_a, span_b, tag, why, '\n'.join(['-' + x for x in al] + ['+' + x for x in bl])))
    unused = sorted(set(REASONS) - used)
    if unused:
        raise SystemExit('UNUSED REASONS %r' % unused)
    head = RR.HEAD + '\nHunks by reason: %s.\n' % ', '.join('%s %d' % (t, n) for t, n in sorted(totals.items()))
    with open(out, 'x') as f:
        f.write(head + '\n'.join(lines_out))
    print('hunks', totals)


if __name__ == '__main__':
    main()

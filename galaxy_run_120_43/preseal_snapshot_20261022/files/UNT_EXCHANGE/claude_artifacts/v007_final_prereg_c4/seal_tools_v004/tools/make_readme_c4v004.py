# Claude4 seal tools v004 (BUILD helper; A110, dispatch 0646): README_SEAL_TOOLS_V004_DELTA.md from dev/README_SEAL_TOOLS_V004_DELTA.template.md.
# Every {{sha:REL}} becomes the sha256 of this folder's REL from bytes; {{utc}} becomes the UTC argument (date -u); FIXED holds the values and
# disclosures written in by hand (each old text must occur exactly once). Refuses if any {{ is left. The output is created exclusively.
# usage: python3 -I -B make_readme_c4v004.py UTC
import hashlib, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
FIXED = [
    ('{{sha_abs:/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/'
     'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md}}',
     '43d4562b4fce53cf7bc0ea101af2792b8669689cbbddf882882e1ac4a14cbb0c'),          # shasum of the bytes Claude4 read for this build
    ("no runs_ext, C5H or UVT path was read, listed or stat'ed (beyond the fence probes above);",
     "no runs_ext, C5H or UVT path was read, listed or stat'ed (beyond the fence probes above; one listing of the CLAUDE2 control folder, made to "
     "find the V006 addendum, showed the runs_ext symlink entry itself, and nothing under it was touched);"),
    ('no target or observed-velocity data was opened;',
     'no target or observed-velocity data was opened (the CLAUDE2 V006 root-decision addendum, a decision record as fence exception (b) classes it, '
     'was read as authority);'),
]


def main():
    utc = sys.argv[1]
    assert re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ', utc), utc
    text = (HERE / 'dev/README_SEAL_TOOLS_V004_DELTA.template.md').read_text()
    for old, new in FIXED:
        if text.count(old) != 1:
            raise SystemExit('REFUSED: %d occurrences of %r' % (text.count(old), old[:80]))
        text = text.replace(old, new, 1)
    text = text.replace('{{utc}}', utc)
    text = re.sub(r'\{\{sha:([^}]+)\}\}', lambda m: hashlib.sha256((HERE / m.group(1)).read_bytes()).hexdigest(), text)
    if '{{' in text:
        raise SystemExit('REFUSED: an unfilled placeholder is left')
    out = HERE / 'README_SEAL_TOOLS_V004_DELTA.md'
    with open(out, 'x') as f:
        f.write(text)
    print(hashlib.sha256(out.read_bytes()).hexdigest(), out)


if __name__ == '__main__':
    main()

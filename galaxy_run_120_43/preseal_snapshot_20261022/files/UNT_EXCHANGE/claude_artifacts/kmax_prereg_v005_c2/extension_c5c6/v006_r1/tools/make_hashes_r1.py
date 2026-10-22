"""Write v006_r1/HASHES.txt: sha256 from bytes of every file under v006_r1/ (except HASHES.txt itself), paths relative to v006_r1.
usage: python3 -I -B make_hashes_r1.py"""
import hashlib
import os
import time
from pathlib import Path

OUT = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/extension_c5c6/v006_r1')
HEAD = [
    '# HASHES v006_r1 (sha256 from bytes, %s); paths relative to %s' % (time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), OUT),
    '# KEY: prereg/KMAX_MATRIX_PREREG_V006_R1.json (DRAFT R1, unsealed) | prereg/kmax_compare_ext_c2v006_r1.py (pins R1) | specs/*_M32_C2V009.json (launchable after seal) | LAUNCH_EXT_V002.json/.commands.txt | SEAL_READY_V006_R1.json',
    '# SUPERSEDED (kept): dryrun/DRYRUN_R1_SUMMARY.json (summary fields read at the wrong level; replaced by dryrun/DRYRUN_R1_SUMMARY_V002.json)',
]


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def main():
    rows = []
    for r, ds, fs in os.walk(OUT):
        ds.sort()
        for f in sorted(fs):
            p = Path(r) / f
            if p == OUT / 'HASHES.txt':
                continue
            rows.append('%s  ./%s' % (sha(p), p.relative_to(OUT)))
    with open(OUT / 'HASHES.txt', 'x') as fh:
        fh.write('\n'.join(HEAD + sorted(rows, key=lambda x: x.split('  ', 1)[1])) + '\n')
    print(len(rows), 'files')


if __name__ == '__main__':
    main()

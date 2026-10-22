"""Write v006_r1/HASHES_V002.txt (successor of HASHES.txt): sha256 from bytes of every file under v006_r1/ except HASHES_V002.txt
itself, paths relative to v006_r1.  usage: python3 -I -B make_hashes_r1_v002.py"""
import hashlib
import os
import time
from pathlib import Path

OUT = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/extension_c5c6/v006_r1')
HEAD = [
    '# HASHES_V002 v006_r1 (sha256 from bytes, %s); paths relative to %s' % (time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), OUT),
    '# KEY: prereg/KMAX_MATRIX_PREREG_V006_R1.json (DRAFT R1, unsealed) | prereg/kmax_compare_ext_c2v006_r1.py (pins R1) | specs/*_M32_C2V009.json (launchable after seal) | LAUNCH_EXT_V002.json/.commands.txt | SEAL_READY_V006_R1_V002.json',
    '# SUPERSEDED (kept, not evidence of R1): HASHES.txt (index before the seal-ready successor); SEAL_READY_V006_R1.json (tests field named the V006 draft rerun; replaced by SEAL_READY_V006_R1_V002.json); dryrun/DRYRUN_R1_SUMMARY.json (summary fields read at the wrong level; replaced by DRYRUN_R1_SUMMARY_V002.json); prereg/test_runs_V001 (crash: registered_outdir read the outdirs note string; compare fixed before V002) and test_runs_V002 (29/30: T28 test-design error, note key; fixed) -> current: prereg/test_runs_V003 30/30; tools/make_seal_ready_r1.py, tools/make_hashes_r1.py (replaced by the _v002 tools)',
    '# REFERENCE: prereg/test_runs_V006_DRAFT_RERUN = the V006 draft suite (87506f45) rerun against the V006 draft, 18/18',
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
            if p == OUT / 'HASHES_V002.txt':
                continue
            rows.append('%s  ./%s' % (sha(p), p.relative_to(OUT)))
    with open(OUT / 'HASHES_V002.txt', 'x') as fh:
        fh.write('\n'.join(HEAD + sorted(rows, key=lambda x: x.split('  ', 1)[1])) + '\n')
    print(len(rows), 'files')


if __name__ == '__main__':
    main()

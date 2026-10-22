"""Fill a PENDING R2 template (C4R2 / S4R2 / Y4R2) from its cube outdir once the C4 V005 prefix exists (Claude2 lane, c2v005).

Same checks as make_kmax_v005_c2.fill() (which is bound to R1 and refuses R2 templates) and as the RR2 fill in
make_d7r2_c2.py build: template pinned by the build record, brackets == R2, cube physical/coefficients/grid equal,
cube truncation cube, cube brackets anchor/R1/R2, admit PENDING; admission from bytes with the reviewed generator.
Writes only specs_d7r2/filled/CALL_KMAX_<NAME>_A2F10_D7R2_C2V005.json (exclusive create).  Launches nothing.
Dry-run the result under v005 (dry-run --spec --report-dir) before launch.

usage: python3 -I -B fill_r2_c2.py C4R2|S4R2|Y4R2
"""
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/d7_recovery_r2')
MK = HERE / 'make_d7r2_c2.py'
MK_SHA = '53314f550cbc166375c64e635264e13dbdfdbff6c4a522a452aa4c6471a96b86'


def main(name):
    import hashlib
    if hashlib.sha256(MK.read_bytes()).hexdigest() != MK_SHA:
        raise SystemExit('REFUSED: make_d7r2_c2.py pin mismatch')
    s = importlib.util.spec_from_file_location('make_d7r2_c2', str(MK))
    M = importlib.util.module_from_spec(s)
    s.loader.exec_module(M)
    rec = json.loads((HERE / 'BUILD_R2_RECORD.json').read_text())
    if name not in ('C4R2', 'S4R2', 'Y4R2'):
        raise SystemExit('REFUSED: %s is not a pending R2 template' % name)
    sp = rec['specs'][name]
    t = json.loads(M.pinned(sp['path'], sp['sha256'], name + ' template'))
    r2 = json.loads(M.pinned(rec['R2_file']['path'], rec['R2_file']['sha256'], 'R2'))['brackets']
    pre = json.loads(M.pinned(*M.PREREG, 'prereg'))
    r1 = json.loads(M.pinned(*M.R1F, 'R1'))['brackets']
    canon = M.canon
    if canon(t['numerics']['brackets']) != canon(r2):
        raise SystemExit('REFUSED: template brackets are not R2')
    if 'PENDING' not in json.dumps(t['admit']):
        raise SystemExit('REFUSED: template admit is not PENDING')
    admit, cube = M.B.load_gen().admission_from_cube_out(sp['cube_outdir'])
    for k in ('physical', 'coefficients'):
        if cube[k] != t[k]:
            raise SystemExit('REFUSED: cube %s differs from template' % k)
    if cube['numerics']['composite_grid_spec'] != t['numerics']['composite_grid_spec'] or cube['numerics']['truncation'] != {'shape': 'cube'}:
        raise SystemExit('REFUSED: cube grid/truncation differ from template')
    if canon(cube['numerics']['brackets']) not in (canon(pre['anchor']['brackets']), canon(r1), canon(r2)):
        raise SystemExit('REFUSED: cube brackets are neither the anchor block, R1 nor R2')
    t['admit'] = admit
    t['label'] = t['label'].replace(' TEMPLATE', '') + '; admits %s' % sp['cube_outdir']
    if M.lint_override_keys(t):
        raise SystemExit('REFUSED: override key lint')
    out = HERE / 'specs_d7r2/filled' / ('CALL_KMAX_%s_A2F10_D7R2_C2V005.json' % name)
    print(json.dumps({'spec': str(out), 'sha256': M.write_x(out, M.spec_bytes(t)), 'admit': admit}, indent=1))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1])

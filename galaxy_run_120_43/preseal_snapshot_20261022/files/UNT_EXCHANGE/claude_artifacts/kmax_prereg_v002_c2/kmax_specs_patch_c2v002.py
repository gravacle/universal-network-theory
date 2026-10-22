"""Minimal hand-patch of make_kmax_specs_c2v001.py output for KMAX_MATRIX_PREREG_V002 (Claude2 lane, c2v002).

Why it exists: the read-only generator (6c74318e...) hard-codes PICARD passes 4 (line 36) and has no option
for it; PREREG_V002 (CHECK D6) registers passes 6.  Its wave1 also emits C2, which V002 binds to the running
call A2_ANCHOR_F3_RUN_V001 instead.  Its wave2 command will REFUSE every cube whose picard block is not
passes-4 ("cube call brackets/picard differ from the common block", line 235-236), i.e. C3 and C4, and for
C2 = F3 it would emit passes-4 S2/Y2.  So:

  patch  RAW_WAVE1 RAW_TEMPLATES OUT : copy generator output with exactly one change, numerics.picard.passes
                                       4 -> 6 (same serializer: indent=1 + newline); drop C2 from wave1; bind the
                                       S2/Y2 template placeholders to the F3 outdir.  Writes unified diffs.
  fill   TEMPLATE CUBE_OUT CUBE_SPEC_SHA OUT_SPEC
                                     : wave-2 spec = TEMPLATE with admit replaced by the generator's own
                                       admission_from_cube_out(CUBE_OUT) (loaded from verified bytes); refuses
                                       unless CUBE_OUT/inputs/call_spec.json has sha CUBE_SPEC_SHA and its
                                       physical/coefficients/brackets/grid equal the template's.
Launches nothing.  Every hash from bytes.  usage: python3 -I -B kmax_specs_patch_c2v002.py patch|fill ...
"""
import difflib
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

GEN = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calibration_prep_c2_0470/kmax_convergence/make_kmax_specs_c2v001.py',
       '6c74318e602e7589a5eb5e540c463e2e9101d5b80d508167818a933a9f3096c0')
F3 = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/A2_ANCHOR_F3_RUN_V001'
PASSES = 6


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def spec_bytes(obj):
    return (json.dumps(obj, indent=1, allow_nan=False) + '\n').encode()


def write_x(p, raw):
    with open(p, 'xb') as f:
        f.write(raw)
    return sha_bytes(raw)


def load_gen():
    raw = Path(GEN[0]).read_bytes()
    if sha_bytes(raw) != GEN[1]:
        raise SystemExit('REFUSED: generator sha mismatch')
    spec = importlib.util.spec_from_file_location('kmax_gen_v001', GEN[0])
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def patch(raw_wave1, raw_templates, out):
    out = Path(out)
    out.mkdir(parents=True)
    (out / 'wave1').mkdir()
    (out / 'templates').mkdir()
    man = {'schema': 'UNT_KMAX_SPECS_PATCH_MANIFEST_C2_V002', 'generator': {'path': GEN[0], 'sha256': GEN[1]},
           'patch_script_sha256': sha_bytes(Path(__file__).read_bytes()), 'change': 'numerics.picard.passes 4 -> 6 only'
           ' (templates S2/Y2: PENDING placeholders "<C2 out>" bound to the F3 outdir); C2 omitted from wave1 (bound to A2_ANCHOR_F3_RUN_V001)',
           'wave1': {}, 'templates': {}}
    diffs = []
    jobs = [('wave1', Path(raw_wave1) / ('CALL_KMAX_%s_C2V001.json' % c), out / 'wave1' / ('CALL_KMAX_%s_A2F3_C2V002.json' % c), c) for c in ('C3', 'C4', 'R')]
    jobs += [('templates', Path(raw_templates) / ('CALL_KMAX_%s_C2V001.TEMPLATE.json' % c), out / 'templates' / ('CALL_KMAX_%s_A2F3_C2V002.TEMPLATE.json' % c), c)
             for c in ('S2', 'Y2', 'C3', 'S3', 'Y3', 'C4', 'S4', 'Y4', 'R')]
    for kind, src, dst, cid in jobs:
        raw = src.read_bytes()
        s = json.loads(raw)
        if spec_bytes(s) != raw:
            raise SystemExit('REFUSED: generator output does not round-trip through the serializer: %s' % src)
        if s['numerics']['picard'] != {'passes': 4, 'speed_change_bound_km_s': 0.01, 'observe_every_pass': True}:
            raise SystemExit('REFUSED: unexpected picard block in %s' % src)
        s['numerics']['picard']['passes'] = PASSES
        if kind == 'templates' and cid in ('S2', 'Y2'):
            s = json.loads(json.dumps(s).replace('<C2 out>', F3))
        new = spec_bytes(s)
        h = write_x(dst, new)
        man[kind][cid] = {'path': str(dst), 'sha256': h, 'generator_output': str(src), 'generator_output_sha256': sha_bytes(raw)}
        diffs += list(difflib.unified_diff(raw.decode().splitlines(True), new.decode().splitlines(True), str(src), str(dst)))
    dsha = write_x(out / 'DIFF_GENERATOR_VS_PATCHED.txt', ''.join(diffs).encode())
    man['diff'] = {'path': str(out / 'DIFF_GENERATOR_VS_PATCHED.txt'), 'sha256': dsha}
    write_x(out / 'PATCH_MANIFEST.json', spec_bytes(man))
    print(json.dumps({k: {c: v['sha256'] for c, v in man[k].items()} for k in ('wave1', 'templates')}, indent=1))


def fill(template, cube_out, cube_spec_sha, out_spec):
    gen = load_gen()
    t = json.loads(Path(template).read_text())
    cs_raw = (Path(cube_out) / 'inputs' / 'call_spec.json').read_bytes()
    if sha_bytes(cs_raw) != cube_spec_sha:
        raise SystemExit('REFUSED: cube call spec sha %s != %s' % (sha_bytes(cs_raw), cube_spec_sha))
    admit, cube = gen.admission_from_cube_out(cube_out)
    for k in ('physical', 'coefficients'):
        if cube[k] != t[k]:
            raise SystemExit('REFUSED: cube %s differs from template' % k)
    tg = t['numerics']['composite_grid_spec']
    if cube['numerics']['composite_grid_spec'] != tg or cube['numerics']['truncation'] != {'shape': 'cube'} \
            or cube['numerics']['brackets'] != t['numerics']['brackets']:
        raise SystemExit('REFUSED: cube grid/truncation/brackets differ from template')
    if cube['numerics']['picard']['speed_change_bound_km_s'] != t['numerics']['picard']['speed_change_bound_km_s']:
        raise SystemExit('REFUSED: cube Picard bound differs')
    t['admit'] = admit
    t['label'] = t['label'].replace(' TEMPLATE', '') + '; admits %s (spec %s)' % (cube_out, cube_spec_sha[:16])
    print(json.dumps({'spec': out_spec, 'sha256': write_x(out_spec, spec_bytes(t)), 'admit': admit}, indent=1))


if __name__ == '__main__':
    if len(sys.argv) == 5 and sys.argv[1] == 'patch':
        patch(*sys.argv[2:])
    elif len(sys.argv) == 6 and sys.argv[1] == 'fill':
        fill(*sys.argv[2:])
    else:
        print(__doc__)
        sys.exit(2)

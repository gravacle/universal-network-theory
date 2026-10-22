"""c2v002 (Claude2 driver_r4): b0_plan_identity_c2v001.py (24108a34) with at most 3 concurrent dry runs; nothing else changes.
Gate B0 / B0prime_DRY (TAIL_SCHEME_DESIGN_V002 sec 4.1, R1 L3) and B0_FA, for driver c2v010 tail OFF (Claude2 driver lane).

Runs `dry-run` (simulate; no stage is executed) of v010 and of each parent on the standard spec sets, then compares every
file of the two report directories (DRYRUN_REPORT.json, DRYRUN_PLAN.txt, every planned input/config/seed) after a declared
substitution map T, the method of stage_successor_gal_c2v005/check/tools/cmp_dry_check_v001.py (af853189): T is built from
the driver texts, derived file hashes are added only where T(parent bytes) == v010 bytes (fixpoint), DRYRUN_PLAN.txt hash
prefixes (12/16 chars) are substituted for every full-hash pair found.  Exit codes must match; for a failing dry run the
terminal exception line must match after T.
  T_GEO (parent v009-GEO 237ef3d4 -> v010): driver path + sha, report dir.
  T_EXT (parent v009-EXT 999331af -> v010): the v008 -> GEO stage-binding pin pairs (11 stage paths + shas, schema V004 ->
        V005 path/sha/name, 3 galaxy-config paths/shas; cmp_dry_check sub_pairs), driver path + sha, report dir.
Spec sets: GEO (gal_c2v005 CHECK_V001 sec 2: the nine 4.04 specs, plus the D-test specs, compared with GEO only), EXT
(extension_c5c6 DRY_JOBS: KMAX R3, C5/C6, negatives; V006 R1 M32; C5H; compared with EXT only when GEO refuses G5/G6 or
max_iterations, else with both), and B0_FA (R-A F-A cases A1/A2/A4: v010 must end REFUSED ROUTE_A_CHECKPOINT_MISSING).
Usage: python3 -I -B b0_plan_identity_c2v001.py V010_PATH V010_SHA OUTDIR"""
import concurrent.futures as cf
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
EX = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
C2 = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2')
DRIVERS = {
    'EXT': (EX / 'kmax_prereg_v005_c2/extension_c5c6/driver_v009/galaxy_m0_forward_c2v009.py', '999331afd604dd9829aa8f389f43cdb87603d03412d52ba09712226787f18db6'),
    'GEO': (EX / 'stage_successor_gal_c2v005/driver/galaxy_m0_forward_c2v009.py', '237ef3d41daf4d99b0aafed3e90b27b095a741a9f66ea06ea34f3e44876d47bb'),
}
V008 = EX / 'driver_v008_c2/galaxy_m0_forward_c2v008.py'
K = EX / 'kmax_prereg_v005_c2'
FA = EX / 'review_driver_v008_c4/verify/V8f_delta_lines_F-A_contract/specs'
SPECS = [  # (name, path, parents compared)
    ('A2F10', C2 / 'specs/CALL_A2_ANCHOR_F10_C2V001.json', ('EXT', 'GEO')),
    ('A2F10_RA8', EX / 'driver_v007_c2/tests/specs/CALL_TEST_A2F10_RA8_C2V007.json', ('EXT', 'GEO')),
    ('ADMIT_PREFIX_C2V005', EX / 'ngc_route_impl_c2/binding/specs/CALL_REPRO_PINNED_ADMIT_PREFIX_C2V005.json', ('EXT', 'GEO')),
    ('ADMIT_ROUTE_A_C2V005', EX / 'ngc_route_impl_c2/binding/specs/CALL_REPRO_PINNED_ADMIT_ROUTE_A_C2V005.json', ('EXT', 'GEO')),
    ('PINNED_FULL_C2V001', EX / 'galaxy_m0_forward_c2_0466/specs/CALL_REPRO_PINNED_FULL_C2V001.json', ('EXT', 'GEO')),
    ('RULE_FULL_C2V001', EX / 'galaxy_m0_forward_c2_0466/specs/CALL_REPRO_RULE_FULL_C2V001.json', ('EXT', 'GEO')),
    ('DEC_II_N8', EX / 'driver_v008_c2/deciding/CALL_A2_ANCHOR_F10_ROUTE_A_PARALLEL_N8_C2V008.json', ('EXT', 'GEO')),
    ('NGC_A2F10_TEMPLATE', EX / 'ngc_f10_c2/route_b_v006/specs/CALL_NGC3198_ROUTE_B_A2F10_TEMPLATE_C2V006.json', ('EXT', 'GEO')),
    ('NGC_GL10_TEMPLATE', EX / 'ngc_f10_c2/route_b_v006/specs/CALL_NGC3198_ROUTE_B_A2F10_GL10_ALTERNATIVE_TEMPLATE_C2V006.json', ('EXT', 'GEO')),
    ('NGC_SEED_ROUTE_A_CONFIG', EX / 'galaxy_m0_forward_c2_0466/specs/CALL_NGC3198_SEED_C2V002.json', ('EXT', 'GEO')),
    ('D3p98107', EX / 'driver_v008_c2/tests/specs/c2v008/CALL_TEST_A2F10_D3p98107_C2V008.json', ('GEO',)),
    ('D4p07', EX / 'driver_v008_c2/tests/specs/c2v008/CALL_TEST_A2F10_D4p07_C2V008.json', ('GEO',)),
    ('D4p11150', EX / 'driver_v008_c2/tests/specs/c2v008/CALL_TEST_A2F10_D4p11150_C2V008.json', ('GEO',)),
    ('C2R3', K / 'd7_recovery_r3/specs_d7r3/CALL_KMAX_C2R3_A2F10_D7R3_C2V005.json', ('EXT', 'GEO')),
    ('C3R3', K / 'd7_recovery_r3/specs_d7r3/CALL_KMAX_C3R3_A2F10_D7R3_C2V005.json', ('EXT', 'GEO')),
    ('C4R3', K / 'd7_recovery_r3/specs_d7r3/CALL_KMAX_C4R3_A2F10_D7R3_C2V005.json', ('EXT', 'GEO')),
    ('S4R3', K / 'd7_recovery_r3/specs_d7r3/CALL_KMAX_S4R3_A2F10_D7R3_C2V005.json', ('EXT', 'GEO')),
    ('RR3', K / 'd7_recovery_r3/specs_d7r3/CALL_KMAX_RR3_A2F10_D7R3_C2V005.json', ('EXT', 'GEO')),
    ('Y3R3', K / 'd7_recovery_r3/specs_d7r3/CALL_KMAX_Y3R3_A2F10_D7R3_C2V005.json', ('EXT', 'GEO')),
    ('C5_N8', K / 'extension_c5c6/specs/CALL_KMAX_C5R3_A2F10_EXT_N8_C2V009.json', ('EXT',)),
    ('C5_N1', K / 'extension_c5c6/specs/CALL_KMAX_C5R3_A2F10_EXT_N1_C2V009.json', ('EXT',)),
    ('C6_N8', K / 'extension_c5c6/specs/CALL_KMAX_C6R3_A2F10_EXT_N8_C2V009.json', ('EXT',)),
    ('C6_N1', K / 'extension_c5c6/specs/CALL_KMAX_C6R3_A2F10_EXT_N1_C2V009.json', ('EXT',)),
    ('C5_N8_M32', K / 'extension_c5c6/v006_r1/specs/CALL_KMAX_C5R3_A2F10_EXT_N8_M32_C2V009.json', ('EXT',)),
    ('C6_N8_M32', K / 'extension_c5c6/v006_r1/specs/CALL_KMAX_C6R3_A2F10_EXT_N8_M32_C2V009.json', ('EXT',)),
    ('C5_N1_M32', K / 'extension_c5c6/v006_r1/specs/CALL_KMAX_C5R3_A2F10_EXT_N1_M32_C2V009.json', ('EXT',)),
    ('C6_N1_M32', K / 'extension_c5c6/v006_r1/specs/CALL_KMAX_C6R3_A2F10_EXT_N1_M32_C2V009.json', ('EXT',)),
    ('C5H', EX / 'c5h_hull_c2/CALL_KMAX_C5H_A2F10_HULL_N8_M32_C2V009.json', ('EXT',)),
    ('NEG_G5_ORDERS', K / 'extension_c5c6/specs/negative/NEG_G5_ORDERS_NOT_DECLARED.json', ('EXT',)),
    ('NEG_G7_132', K / 'extension_c5c6/specs/negative/NEG_G7_132_NODES.json', ('EXT',)),
    ('NEG_MAXIT_0', K / 'extension_c5c6/specs/negative/NEG_MAXIT_0.json', ('EXT',)),
    ('NEG_MAXIT_33', K / 'extension_c5c6/specs/negative/NEG_MAXIT_33.json', ('EXT',)),
    ('NEG_MAXIT_BOOL', K / 'extension_c5c6/specs/negative/NEG_MAXIT_BOOL.json', ('EXT',)),
    ('NEG_MAXIT_ADMIT', K / 'extension_c5c6/specs/negative/NEG_MAXIT_WITH_ADMITTED_ROUTE_A.json', ('EXT',)),
]
FA_SPECS = [('FA_A1_NFP_EMPTY', FA / 'SPEC_A1_NFP_EMPTY.json'), ('FA_A2_NFP_ABSENT', FA / 'SPEC_A2_NFP_ABSENT.json'),
            ('FA_A4_CONV_EMPTY', FA / 'SPEC_A4_CONV_EMPTY.json')]
ENV = {k: v for k, v in os.environ.items() if not k.startswith('PYTHON')}
for _k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
    ENV[_k] = '1'


def sha_b(b):
    return hashlib.sha256(b).hexdigest()


def sha_f(p):
    return sha_b(Path(p).read_bytes())


def geo_pin_pairs():
    """cmp_dry_check_v001.sub_pairs(): v008 (= v009-EXT stage binding) -> v009-GEO stage binding, from the driver texts."""
    t8, t9 = V008.read_text(), DRIVERS['GEO'][0].read_text()
    b6 = str(EX / 'ngc_f10_c2/route_b_v006') + '/'
    b7 = str(EX / 'stage_successor_gal_c2v005') + '/'
    p8 = dict((m[0], (m[1], m[2])) for m in re.findall(r"'(\w+)': \(BIND6 / '(stages/[^']+)', '([0-9a-f]{64})'\)", t8))
    p9 = dict((m[0], (m[1], m[2])) for m in re.findall(r"'(\w+)': \(BIND7 / '(stages/[^']+)', '([0-9a-f]{64})'\)", t9))
    assert set(p8) == set(p9) and len(p8) == 11
    pairs = []
    for k in sorted(p8):
        pairs += [(b6 + p8[k][0], b7 + p9[k][0]), (p8[k][1], p9[k][1])]
    pairs += [(b6 + 'schema/GALAXY_CONFIG_SCHEMA_V004.json', b7 + 'schema/GALAXY_CONFIG_SCHEMA_V005.json'),
              ('8fc7ef48ed91f9cd00e356296b9524adcfd65a1933d3332e9d1ad176c17364bb', 'f9b8d48eca10e5c8f2299c23dc1ac69c60c9f87bc24486024e675f7927bc042a'),
              ('UNT_ROUTE_B_GALAXY_CONFIG_SCHEMA_V004', 'UNT_ROUTE_B_GALAXY_CONFIG_SCHEMA_V005'),
              (b6 + 'configs/GALAXY_CONFIG_DDO154_C2V006.json', b7 + 'configs/GALAXY_CONFIG_DDO154_GAL_C2V005.json'),
              ('24d07f800e3c3c31bc5123f359603d336f095482bf5c1c83802c3192fadebdd0', 'c21f1272f94026dcd4d38b5a8d89e8af2c76e85fbdff2d28f517c366c80f7c45'),
              (b6 + 'configs/GALAXY_CONFIG_NGC3198_C2V006.json', b7 + 'configs/GALAXY_CONFIG_NGC3198_GAL_C2V005.json'),
              ('64b6f1fadb432b1d5e2ee5b54620fb0c4d2cdb59e425e8034458e0dcd58ee441', '299ce971fab0ad6557754066d39ec5a0a664d09dfddcff7650f91b059cd82559'),
              (b6 + 'configs/GALAXY_CONFIG_NGC3198_GL10_ALTERNATIVE_C2V006.json', b7 + 'configs/GALAXY_CONFIG_NGC3198_GL10_ALTERNATIVE_GAL_C2V005.json'),
              ('4a1aa7ebc1a913c3e09b320f6dfacda7670af819acb4f37c2ef1c0eb5b1784ae', '0873b6a4ffde696243f842c656fdc64c519d40aaad7a04f4beda5d47b0f1335a')]
    # DRYRUN_PLAN.txt prints stage file basenames: their pairs follow the full-path pairs (declared, same pin map)
    pairs += [(Path(a).name, Path(b).name) for a, b in list(pairs) if a.startswith('/') and Path(a).name != Path(b).name]
    gt = DRIVERS['GEO'][0].read_text()
    for _, b in pairs:
        assert (b in gt) if re.fullmatch('[0-9a-f]{64}', b) or b.startswith('UNT_') or '/' not in b else Path(b).is_file(), b
    return pairs


def dry(driver_path, spec, rd):
    t0 = time.monotonic()
    p = subprocess.run(['nice', '-n', '10', PY, '-I', '-B', str(driver_path), 'dry-run', '--spec', str(spec), '--report-dir', str(rd)],
                       capture_output=True, text=True, env=ENV, cwd=str(Path(rd).parent))
    return {'exit': p.returncode, 'seconds': round(time.monotonic() - t0, 2), 'stderr_tail': p.stderr.strip().splitlines()[-1:] if p.stderr.strip() else [],
            'stdout_bytes': len(p.stdout)}


def files(d):
    d = Path(d)
    return {str(p.relative_to(d)): p.read_bytes() for p in sorted(d.rglob('*')) if p.is_file()} if d.is_dir() else {}


def apply(pairs, b):
    for a, c in pairs:
        b = b.replace(a.encode(), c.encode())
    return b


PREP_V009 = (EX / 'kmax_prereg_v005_c2/extension_c5c6/prep_successor/ddo_actual_initial_source_preparation_v009.py',
             'b4b27a1deb68a2ec24e9bd3700de3a23537fd14b7029e124aab0f7b50bcac8bc')


def ext_feature_map(raw):
    """Declared EXT map (design sec 4.1, against GEO): v010 carries v009-EXT's AUX['prep_v009'], so its DRYRUN_REPORT.json has
    exactly one more static pin and one more transitively verified file (prep v009 b4b27a1d) than v009-GEO's.  Removed here
    (and verified_files decremented) before the byte comparison; anything else must be equal.  Returns (bytes, applied)."""
    rep = json.loads(raw)
    key = str(PREP_V009[0])
    applied = []
    if rep.get('static_pins', {}).get(key) == PREP_V009[1]:
        del rep['static_pins'][key]
        applied.append('static_pins[prep_v009]')
    tp = rep.get('transitive_pins') or {}
    if (tp.get('files') or {}).get(key) == PREP_V009[1]:
        del tp['files'][key]
        tp['verified_files'] -= 1
        applied.append('transitive_pins.files[prep_v009], verified_files-1')
    return (json.dumps(rep, indent=1, allow_nan=False) + '\n').encode(), applied


def driver_needle_map(raw):
    """Declared map (NGC route-A configuration report only): route_b_hardcoding rows whose needles are located in the DRIVER'S
    OWN text (key_is_driver) carry driver line numbers, which necessarily move with any driver edit; they are blanked on both
    sides.  Rows located in stage files are compared unchanged.  Returns (bytes, n_rows_blanked)."""
    rep = json.loads(raw)
    n = 0
    for r in rep.get('route_b_hardcoding') or []:
        if r.get('key_is_driver'):
            r['needle_lines'] = 'DRIVER_LINE_NUMBERS_BLANKED'
            r['file'] = 'DRIVER'
            n += 1
    return (json.dumps(rep, indent=1, allow_nan=False) + '\n').encode(), n


RO1_NON_ARMED = {'rule': 'RO1', 'fired': False, 'events': [], 'armed': False, 'worker_sha256': None, 'binding_sha256': None}


def ro1_key_map(raw):
    """Declared RO1 map (V005 addendum A48 AMB-15; RO1 lane final patch 1f363113 / RO1_IMPL_V001): v010 adds key 'ro1' to
    EVERY route-A outcome record.  For an attempt of a non-RO1 worker (every tail-OFF call) its value is exactly
    RO1_NON_ARMED; exactly those occurrences (in dicts that carry 'classification') are removed before the byte comparison.
    An armed, fired or differently-valued ro1 block is NOT removed (it would then show as a difference)."""
    rep = json.loads(raw)
    n = [0]

    def walk(o):
        if isinstance(o, dict):
            if 'classification' in o and o.get('ro1') == RO1_NON_ARMED:
                del o['ro1']
                n[0] += 1
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(rep)
    return (json.dumps(rep, indent=1, allow_nan=False) + '\n').encode(), n[0]


def compare(dp, dv, base, parent=None):
    fp, fv = files(dp), files(dv)
    ext_map = []
    if 'DRYRUN_REPORT.json' in fv:
        fv['DRYRUN_REPORT.json'], n_ro1 = ro1_key_map(fv['DRYRUN_REPORT.json'])
        if n_ro1:
            ext_map.append('route_a_outcome.ro1 == RO1_NON_ARMED removed (%d occurrences)' % n_ro1)
    if 'DRYRUN_REPORT.json' in fp and 'DRYRUN_REPORT.json' in fv and b'"route_b_hardcoding"' in fv['DRYRUN_REPORT.json']:
        fp['DRYRUN_REPORT.json'], n1 = driver_needle_map(fp['DRYRUN_REPORT.json'])
        fv['DRYRUN_REPORT.json'], n2 = driver_needle_map(fv['DRYRUN_REPORT.json'])
        ext_map.append('driver needle line numbers blanked (%d/%d rows)' % (n1, n2))
        rows = [(r['stage'], r['status']) for r in json.loads(fv['DRYRUN_REPORT.json']).get('route_b_hardcoding') or [] if r.get('key_is_driver')]
        for side in (fp, fv):
            if 'DRYRUN_PLAN.txt' in side:
                out_lines = []
                for ln in side['DRYRUN_PLAN.txt'].decode().splitlines(True):
                    for st, status in rows:
                        head = '      %-18s %-40s ' % (st, status)
                        if ln.startswith(head):
                            ln = head + 'DRIVER_LINE_NUMBERS_BLANKED\n'
                    out_lines.append(ln)
                side['DRYRUN_PLAN.txt'] = ''.join(out_lines).encode()
    if parent == 'GEO' and 'DRYRUN_REPORT.json' in fv:
        fv['DRYRUN_REPORT.json'], applied = ext_feature_map(fv['DRYRUN_REPORT.json'])
        ext_map += applied
    pairs = list(base) + [(str(dp), str(dv))]
    for _ in range(8):
        added = False
        known = {a for a, _ in pairs}
        for n in fp:
            if n in fv:
                hp, hv = sha_b(fp[n]), sha_b(fv[n])
                if hp != hv and hp not in known and apply(pairs, fp[n]) == fv[n]:
                    pairs.append((hp, hv))
                    added = True
        if not added:
            break
    hp_pairs = [(a, b) for a, b in pairs if re.fullmatch('[0-9a-f]{64}', a)]
    prefix = pairs + [(a[:16], b[:16]) for a, b in hp_pairs] + [(a[:12], b[:12]) for a, b in hp_pairs]
    res = {'files_parent': len(fp), 'files_v010': len(fv), 'only_parent': sorted(set(fp) - set(fv)), 'only_v010': sorted(set(fv) - set(fp)),
           'raw_equal': 0, 'equal_after_T': 0, 'differ': {}, 'derived_hash_pairs': len(pairs) - len(base) - 1}
    for n in sorted(set(fp) & set(fv)):
        if fp[n] == fv[n]:
            res['raw_equal'] += 1
            continue
        a = apply(prefix if n.endswith('DRYRUN_PLAN.txt') else pairs, fp[n])
        if a == fv[n]:
            res['equal_after_T'] += 1
            continue
        al, bl = a.decode(errors='replace').splitlines(), fv[n].decode(errors='replace').splitlines()
        dl = [(i, x[:300], y[:300]) for i, (x, y) in enumerate(zip(al, bl)) if x != y]
        res['differ'][n] = {'n_lines': [len(al), len(bl)], 'first_diff_lines': dl[:8], 'n_diff_lines': len(dl)}
    res['declared_ext_map_applied'] = ext_map
    res['identical'] = not res['only_parent'] and not res['only_v010'] and not res['differ']
    return res


def main():
    v010, v010_sha, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
    if sha_f(v010) != v010_sha:
        raise SystemExit('v010 pin')
    for k, (p, s) in DRIVERS.items():
        if sha_f(p) != s:
            raise SystemExit('parent pin ' + k)
    out.mkdir(parents=True, exist_ok=False)
    (out / 'dry').mkdir()
    gp = geo_pin_pairs()
    maps = {'GEO': [(str(DRIVERS['GEO'][0]), str(v010)), (DRIVERS['GEO'][1], v010_sha)],
            'EXT': gp + [(str(DRIVERS['EXT'][0]), str(v010)), (DRIVERS['EXT'][1], v010_sha)]}
    jobs = []
    for name, spec, parents in SPECS:
        jobs.append(('V010', name, spec))
        for par in parents:
            jobs.append((par, name, spec))
    for name, spec in FA_SPECS:
        jobs.append(('V010', name, spec))
    paths = {'V010': v010, 'EXT': DRIVERS['EXT'][0], 'GEO': DRIVERS['GEO'][0]}
    runs = {}
    with cf.ThreadPoolExecutor(max_workers=3) as ex:  # c2v002: <= 3 dry-run processes at a time (machine busy; the only change)
        fut = {ex.submit(dry, paths[d], s, out / 'dry' / ('%s_%s' % (d, n))): (d, n) for d, n, s in jobs}
        for f in cf.as_completed(fut):
            runs[fut[f]] = f.result()
    rep = {'schema': 'B0_PLAN_IDENTITY_C2V001', 'v010': [str(v010), v010_sha],
           'parents': {k: [str(p), s] for k, (p, s) in DRIVERS.items()}, 'T_maps': {k: len(v) for k, v in maps.items()},
           'method': 'cmp_dry_check_v001 (af853189) generalized: T + derived-hash fixpoint; DRYRUN_PLAN prefixes', 'specs': {}, 'fa': {}}
    for name, spec, parents in SPECS:
        r = {'spec': str(spec), 'spec_sha256': sha_f(spec), 'v010': runs[('V010', name)], 'vs': {}}
        for par in parents:
            pr = runs[(par, name)]
            cmpd = compare(out / 'dry' / ('%s_%s' % (par, name)), out / 'dry' / ('V010_%s' % name), maps[par], par)
            st_p = apply(maps[par] + [(str(out / 'dry' / ('%s_%s' % (par, name))), str(out / 'dry' / ('V010_%s' % name)))],
                         '\n'.join(pr['stderr_tail']).encode()).decode()
            same_err = pr['exit'] == 0 or st_p == '\n'.join(runs[('V010', name)]['stderr_tail'])
            r['vs'][par] = {'parent_run': pr, 'exit_equal': pr['exit'] == runs[('V010', name)]['exit'],
                            'terminal_line_equal_after_T': same_err, 'files': cmpd,
                            'verdict': 'PASS_PLAN_IDENTICAL' if (pr['exit'] == runs[('V010', name)]['exit'] and same_err and cmpd['identical']) else 'FAIL'}
        rep['specs'][name] = r
    for name, spec in FA_SPECS:
        r = runs[('V010', name)]
        ok = r['exit'] != 0 and any('ROUTE_A_CHECKPOINT_MISSING' in x and x.startswith('Refusal') for x in r['stderr_tail'])
        rep['fa'][name] = {'spec': str(spec), 'spec_sha256': sha_f(spec), 'v010': r, 'verdict': 'PASS_REFUSED_ROUTE_A_CHECKPOINT_MISSING' if ok else 'FAIL'}
    n_cmp = sum(len(r['vs']) for r in rep['specs'].values())
    n_pass = sum(1 for r in rep['specs'].values() for v in r['vs'].values() if v['verdict'] == 'PASS_PLAN_IDENTICAL')
    rep['summary'] = {'comparisons': n_cmp, 'pass': n_pass, 'fail': [('%s vs %s' % (n, p)) for n, r in rep['specs'].items()
                                                                       for p, v in r['vs'].items() if v['verdict'] != 'PASS_PLAN_IDENTICAL'],
                      'fa_pass': sum(1 for r in rep['fa'].values() if r['verdict'].startswith('PASS')), 'fa_total': len(rep['fa']),
                      'verdict_B0': 'PASS_PLAN_IDENTICAL' if n_pass == n_cmp else 'FAIL',
                      'verdict_B0_FA': 'PASS' if all(r['verdict'].startswith('PASS') for r in rep['fa'].values()) else 'FAIL'}
    with open(out / 'B0_PLAN_IDENTITY_C2V001.json', 'x') as f:
        json.dump(rep, f, indent=1)
    print(json.dumps(rep['summary'], indent=1))


if __name__ == '__main__':
    main()

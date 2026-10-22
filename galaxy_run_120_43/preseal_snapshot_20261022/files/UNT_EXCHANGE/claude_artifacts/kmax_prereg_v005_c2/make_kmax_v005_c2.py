"""Build KMAX pre-registration V005, its D7 recovery R1 block and the recovery call specs (Claude2 lane, c2v005).

Answers Claude3 review 0020 (REVIEW_PREREG_V004_C3_V001, FAIL): F1 (driver amendment executable), F2/check 5
(no single-shape adoption; the pre-named V1(ii) -> D7 recovery is invoked for S2/Y2), F3 (stopped runs recorded),
F4 (status text), F5 (v005 CHECK cited by sha).  Every threshold, tau_i, gate, next step and the decision order
are copied from V004 bytes unchanged (asserted below).

Reads only (all hashes from bytes): prereg V004, the failed S2/Y2 calls' fs column failure/iteration files,
start/finish/launch files and route-A progress logs of the stopped v003 runs, the F10 anchor outdir (admission),
the V003 specs.  It never opens any result.json or finish.json of a *_V005_* run or of the DDO v005 deciding run
(existence checks only).  Writes only into OUT (exclusive create).  Launches nothing.

usage: python3 -I -B make_kmax_v005_c2.py            (OUT must not contain the products yet)
       python3 -I -B make_kmax_v005_c2.py fill TEMPLATE CUBE_OUTDIR OUT_SPEC
                     (after seal: fill a PENDING admit block of a V005 template from the cube outdir, from bytes)
"""
import copy
import hashlib
import importlib.util
import json
import os
import sys
import time
from pathlib import Path

OUT = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2')
EX = Path('/Users/bgm/Research/UNT_EXCHANGE')
CA = EX / 'claude_artifacts'
RUNS = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs')
V004 = (CA / 'kmax_prereg_v004_c2/KMAX_MATRIX_PREREG_V004.json', '51c9aa6cd997c5cc58b7b814601b27d153952a6cd87368035c985ebab4232136')
SEAL_V004 = CA / 'kmax_prereg_v004_c2/SEAL_RECORD_V004.json'
REVIEW = CA / 'review_prereg_v004_c3/REVIEW_PREREG_V004_C3_V001.md'
REVIEW_MSG = EX / 'FROM_CLAUDE3/0020_2026-10-17_done-0477-prereg-v004-review.md'
DRV5 = (CA / 'ngc_route_impl_c2/binding/galaxy_m0_forward_c2v005.py', '2aef51c4a4cf0ee192594ab366e9b37e54881977df2e4d1b2f259a759818a42f')
CHECK5 = CA / 'ngc_route_impl_c2/binding/CHECK_V001.md'
DECIDING_SPEC = (CA / 'ngc_route_impl_c2/binding/specs/CALL_REPRO_PINNED_ADMIT_PREFIX_C2V005.json',
                 '4ac5527ad1731353d798c2648adc1033335a12102ec071b3ae6a619334313cb7')
DECIDING_RUN = RUNS / 'DDO154_ROUTE_B_C2V005_DECIDING_ADMIT_PREFIX_RUN_V001'
GEN = (CA / 'calibration_prep_c2_0470/kmax_convergence/make_kmax_specs_c2v001.py',
       '6c74318e602e7589a5eb5e540c463e2e9101d5b80d508167818a933a9f3096c0')
F10 = RUNS / 'A2_ANCHOR_F10_RUN_V001'
V003S = CA / 'kmax_prereg_v003_c2/specs_anchor_f10'
FAILED = {'S2': (RUNS / 'KMAX_A2F10_S2_RUN_V001', V003S / 'filled/CALL_KMAX_S2_A2F10_FILLED_C2V003.json',
                 '4d3e695566d3976d793421727622e96e516a19477f80e66148ea2d2c9d740212'),
          'Y2': (RUNS / 'KMAX_A2F10_Y2_RUN_V001', V003S / 'filled/CALL_KMAX_Y2_A2F10_FILLED_C2V003.json',
                 '799fea4f7074804ce892bea7c9e66398f857f11a206de1915871abf90b5cd93b')}
EXPECTED_MISSES = {'S2': [5, 6, 7, 8, 9, 50], 'Y2': [45]}
FS_TEMPLATE = [151250000.0, 302500000.0]   # DDO154_REMAINING_FREE_SURFACE_CONTROLS_V001 solver.enthalpy_bracket (driver v001 template)
FS_TEMPLATE_SRC = ('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/DDO154_REMAINING_FREE_SURFACE_CONTROLS_V001.json',
                   '5d69360f24fc1c943bdec1b24b2a1dd6e22670375118f344c4e66231df002d16')
V005_CASES = ('C3', 'C4', 'R', 'S3', 'Y3', 'S4', 'Y4')


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    return sha_bytes(Path(p).read_bytes())


def spec_bytes(obj):
    return (json.dumps(obj, indent=1, allow_nan=False) + '\n').encode()


def canon(o):
    return json.dumps(o, sort_keys=True, separators=(',', ':'), allow_nan=False)


def write_x(p, raw):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'xb') as f:
        f.write(raw)
    return sha_bytes(raw)


def pinned(path, sha, label):
    raw = Path(path).read_bytes()
    if sha_bytes(raw) != sha:
        raise SystemExit('REFUSED: %s pin mismatch (%s)' % (label, path))
    return raw


def utc_of(p):
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(os.stat(p).st_mtime))


def load_gen():
    pinned(GEN[0], GEN[1], 'generator')
    s = importlib.util.spec_from_file_location('kmax_gen_v001', str(GEN[0]))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


# --------------------------------------------------------------------------- D7 widening rule W1
def widen_W1(entry, template, r_lo, r_hi):
    """Pre-declared D7 step (1) widening of ONE missed column entry from the failed call's own evidence
    (mass residual at the two bracket ends; the column solver requires r(lo) <= 0 <= r(hi)).
    Step A: if the missed side lies inside the hull H = [template_lo, 1.05*template_hi] move that end to H's end.
    Step B: otherwise halve lo / double hi.  Only the side the evidence names moves; the other end is kept."""
    lo, hi = entry
    h_lo, h_hi = template[0], 1.05 * template[1]
    if r_lo > 0 and r_hi > 0:         # root below lo
        return [h_lo if lo > h_lo else lo / 2.0, hi], 'root_below_lo: lo %s -> %s' % (lo, h_lo if lo > h_lo else lo / 2.0)
    if r_lo < 0 and r_hi < 0:         # root above hi
        return [lo, h_hi if hi < h_hi else hi * 2.0], 'root_above_hi: hi %s -> %s' % (hi, h_hi if hi < h_hi else hi * 2.0)
    raise SystemExit('REFUSED: evidence does not show a one-sided miss (r_lo=%r, r_hi=%r)' % (r_lo, r_hi))


def miss_evidence(cid):
    outdir, spec_path, spec_sha = FAILED[cid]
    spec = json.loads(pinned(spec_path, spec_sha, cid + ' spec'))
    if sha_file(outdir / 'inputs' / 'call_spec.json') != spec_sha:
        raise SystemExit('REFUSED: %s outdir call_spec differs from the filled spec' % cid)
    fin_raw = (outdir / 'finish.json').read_bytes()
    fin = json.loads(fin_raw)
    res_sha = sha_file(outdir / 'result.json')
    if fin['status'] != 'FAILED_AT_STAGE' or fin['result_sha256'] != res_sha:
        raise SystemExit('REFUSED: %s finish not FAILED_AT_STAGE or result sha mismatch' % cid)
    rule = spec['numerics']['brackets']['rule']['fs_absolute_overrides']
    cols = []
    for f in sorted(outdir.glob('stages/*_fs_columns_*/columns/column_*_failure.json')):
        fail = json.loads(f.read_text())
        it = f.with_name(f.name.replace('_failure.json', '_iterations.jsonl'))
        hist = [json.loads(x) for x in it.read_text().splitlines() if x.strip()]
        idx = int(fail['index'])
        entry = list(rule.get(str(idx), FS_TEMPLATE))
        if not fail['message'].startswith('MASS_ENTHALPY_NOT_BRACKETED') or len(hist) != 2 \
                or [h['Hc_m2_s2'] for h in hist] != entry:
            raise SystemExit('REFUSED: unexpected failure record %s' % f)
        new, why = widen_W1(entry, FS_TEMPLATE, hist[0]['mass_relative_residual'], hist[1]['mass_relative_residual'])
        cols.append({'index': idx, 'stage_dir': f.parent.parent.name, 'message': fail['message'],
                     'failure_file': {'path': str(f), 'sha256': sha_file(f)}, 'iterations_file': {'path': str(it), 'sha256': sha_file(it)},
                     'entry_in_failed_call': entry,
                     'evidence': [{'Hc_m2_s2': h['Hc_m2_s2'], 'mass_relative_residual': h['mass_relative_residual']} for h in hist],
                     'W1': {'new_entry': new, 'step': why}})
    if sorted(c['index'] for c in cols) != EXPECTED_MISSES[cid]:
        raise SystemExit('REFUSED: %s missed columns %s != expected %s' % (cid, [c['index'] for c in cols], EXPECTED_MISSES[cid]))
    rot_err = (outdir / 'stages/06_fs_rotation/stderr.txt').read_text().strip().splitlines()[-1]
    return spec, {'case': cid, 'run': str(outdir), 'driver_sha256': '75b0c08a44eac92caedd46564eaaefe08b88a6c536e95cb46f54a9d8da962f22',
                  'call_spec': {'path': str(spec_path), 'sha256': spec_sha},
                  'finish': {'path': str(outdir / 'finish.json'), 'sha256': sha_bytes(fin_raw), 'status': fin['status'], 'reasons': fin['reasons'],
                             'utc_mtime': utc_of(outdir / 'finish.json')},
                  'result_sha256': res_sha, 'fs_rotation_last_stderr_line': rot_err,
                  'gate': 'V1 (ii) FAILED_AT_STAGE with a bracket miss in a column pass -> D7 recovery (invoked)',
                  'missed_columns': cols}


# --------------------------------------------------------------------------- stopped runs (F3)
def route_a_events(run):
    p = run / 'stages/01_route_a/attempt_000/progress.jsonl'
    its, last = [], None
    with open(p) as f:
        for line in f:
            last = line
            if '"iteration_completed"' in line:
                e = json.loads(line)
                its.append({'iteration': e['iteration'], 'gas_fourier_residual_J': e['gas_fourier_residual_J'], 'bound_J': e['bound_J'],
                            'met_bound': e['gas_fourier_residual_J'] < e['bound_J']})
    le = json.loads(last)
    return p, its, {k: le.get(k) for k in ('stage', 'iteration', 'column_index', 'column_count', 'elapsed_seconds')}


def stop_record(name, reason, extra=None):
    run = RUNS / name
    launch = json.loads((Path(str(run) + '.receipt.json.launch.json')).read_text())
    p, its, last = route_a_events(run)
    newest = max((x for x in run.rglob('*') if x.is_file()), key=lambda x: os.stat(x).st_mtime)
    cp_end = sorted((run / 'stages/01_route_a/checkpoint/attempts').glob('*.end.json'))
    rec = {'run': str(run), 'launch_utc': launch['utc'], 'driver_sha256': launch['pins']['driver']['sha256'],
           'spec': launch['pins']['spec'], 'finish_json_exists': (run / 'finish.json').exists(),
           'result_json_exists': (run / 'result.json').exists(), 'receipt_exists': Path(str(run) + '.receipt.json').exists(),
           'monitor_log_bytes': os.stat(str(run) + '.monitor.log').st_size,
           'route_a_progress': {'path': str(p), 'sha256': sha_file(p), 'iterations_completed': its, 'last_event': last},
           'route_a_checkpoint_end_records': [json.loads(x.read_text()) for x in cp_end],
           'last_byte_written': {'path': str(newest), 'utc_mtime': utc_of(newest)},
           'stop_utc': 'NOT_RECORDED_BY_COORDINATOR; bounded from bytes: not before last_byte_written.utc_mtime; no process of this run alive at build time',
           'stopped_by': 'coordinator (Claude2 lane orchestration); no monitor receipt was written because the monitor was stopped with the child',
           'reason': reason}
    if extra:
        rec.update(extra)
    return rec


def alive(name):
    """Driver/monitor/stage processes whose command line names this run's outdir (exact path segment)."""
    import subprocess
    out = subprocess.run(['ps', '-axo', 'pid=,command='], capture_output=True, text=True).stdout
    seg = str(RUNS / name)
    hits = []
    for line in out.splitlines():
        if ('galaxy_m0_forward' in line or 'root_monitor' in line) and (seg + '/' in line or seg + ' ' in line or line.endswith(seg)
                                                                      or seg + '.receipt' in line):
            hits.append(line.strip()[:300])
    return hits


# --------------------------------------------------------------------------- build
def main():
    products = ['KMAX_MATRIX_PREREG_V005.json', 'd7_recovery/KMAX_D7_RECOVERY_R1.json']
    for p in products:
        if (OUT / p).exists():
            raise SystemExit('REFUSED: %s exists' % p)
    v4raw = pinned(V004[0], V004[1], 'prereg V004')
    v4 = json.loads(v4raw)
    pinned(DRV5[0], DRV5[1], 'driver v005')
    pinned(FS_TEMPLATE_SRC[0], FS_TEMPLATE_SRC[1], 'fs solver template')
    if json.loads(Path(FS_TEMPLATE_SRC[0]).read_text())['solver']['enthalpy_bracket'] != FS_TEMPLATE:
        raise SystemExit('REFUSED: template bracket differs')
    gen = load_gen()
    anchor_br = v4['anchor']['brackets']

    # ---- D7 evidence and R1 block
    specs, evid = {}, {}
    for cid in ('S2', 'Y2'):
        specs[cid], evid[cid] = miss_evidence(cid)
        if canon(specs[cid]['numerics']['brackets']) != canon(anchor_br):
            raise SystemExit('REFUSED: %s ran with a brackets block other than the registered anchor block' % cid)
    r1 = copy.deepcopy(anchor_br)
    widened = {}
    for cid in ('S2', 'Y2'):
        for c in evid[cid]['missed_columns']:
            k = str(c['index'])
            if k in widened and widened[k] != c['W1']['new_entry']:
                raise SystemExit('REFUSED: conflicting W1 results for column %s' % k)
            widened[k] = c['W1']['new_entry']
    for k, v in widened.items():
        r1['rule']['fs_absolute_overrides'][k] = v
    r1_rec = {'brackets': r1,
              'reason': 'D7 recovery R1 (prereg V005 amendment_v005.d7_recovery): FS column passes of S2 (KMAX_A2F10_S2_RUN_V001: columns 5,6,7,8,9,50) '
                        'and Y2 (KMAX_A2F10_Y2_RUN_V001: column 45) failed MASS_ENTHALPY_NOT_BRACKETED with mass residual > 0 at both ends of '
                        '[3.025e8, 3.17625e8]; rule W1 moves only lo of those 7 entries to the template lo 1.5125e8. No other key changes.',
              'invocation': 'R1',
              'widened_entries': {k: {'from': anchor_br['rule']['fs_absolute_overrides'].get(k, FS_TEMPLATE), 'to': v} for k, v in sorted(widened.items(), key=lambda kv: int(kv[0]))},
              'evidence': {cid: [{'index': c['index'], 'failure_file': c['failure_file'], 'iterations_file': c['iterations_file'],
                                  'evidence': c['evidence']} for c in evid[cid]['missed_columns']] for cid in ('S2', 'Y2')}}
    r1_sha = write_x(OUT / 'd7_recovery/KMAX_D7_RECOVERY_R1.json', spec_bytes(r1_rec))
    ev_sha = write_x(OUT / 'd7_recovery/D7_EVIDENCE_S2_Y2_V001.json', spec_bytes(evid))

    # ---- corrected base spec (D7 step 2): anchor base spec with only the brackets block changed
    base_path = v4['anchor']['base_spec']['path']
    base = json.loads(pinned(base_path, v4['anchor']['base_spec']['sha256'], 'anchor base spec'))
    if canon(base['numerics']['brackets']) != canon(anchor_br):
        raise SystemExit('REFUSED: anchor base spec brackets differ from anchor.brackets')
    cbase = copy.deepcopy(base)
    cbase['numerics']['brackets'] = copy.deepcopy(r1)
    cbase_path = OUT / 'd7_recovery/CALL_A2_ANCHOR_F10_D7R1_BASE_C2V005.json'
    cbase_sha = write_x(cbase_path, spec_bytes(cbase))

    # ---- admission of the F10 prefix, from bytes, with the reviewed generator
    adm_f10, f10_spec = gen.admission_from_cube_out(str(F10))
    if sha_file(F10 / 'inputs/call_spec.json') != v4['anchor']['base_spec']['sha256']:
        raise SystemExit('REFUSED: F10 call_spec is not the anchor base spec')
    calls = {}
    # S2R / Y2R: failed spec with only the 7 widened override entries (and the label) changed
    for cid in ('S2', 'Y2'):
        s = copy.deepcopy(specs[cid])
        if canon(s['admit']) != canon(adm_f10):
            raise SystemExit('REFUSED: %s admit block is not the F10 prefix re-derived from bytes' % cid)
        s['numerics']['brackets'] = copy.deepcopy(r1)
        s['label'] = s['label'] + ' | D7 recovery R1 rerun of %s (prereg V005; only fs_absolute_overrides %s widened)' % (
            FAILED[cid][0].name, ','.join(sorted(widened, key=int)))
        p = OUT / ('specs_d7r1/CALL_KMAX_%sR_A2F10_D7R1_C2V005.json' % cid)
        calls[cid + 'R'] = {'case': cid, 'path': str(p), 'sha256': write_x(p, spec_bytes(s)), 'driver': 'v001',
                            'outdir': str(RUNS / ('KMAX_A2F10_%sR_D7R1_RUN_V001' % cid)), 'derived_from': {'path': str(FAILED[cid][1]), 'sha256': FAILED[cid][2]}}
    # C2R: D7 step (4) for the completed cube C2 = F10 bound call: corrected base spec, passes 6 (CHECK D6), admits F10's own prefix
    c2 = copy.deepcopy(cbase)
    c2['numerics']['picard']['passes'] = v4['anchor']['picard']['passes']
    c2['admit'] = adm_f10
    c2['label'] = 'P-88 kmax matrix case C2 (grid G2, cube) | D7 recovery R1 step (4) rerun of the completed bound call A2_ANCHOR_F10_RUN_V001 ' \
                  '(prereg V005): corrected base spec %s, picard.passes 6, admits its own route-A/reference/body' % cbase_sha[:16]
    p = OUT / 'specs_d7r1/CALL_KMAX_C2R_A2F10_D7R1_C2V005.json'
    calls['C2R'] = {'case': 'C2', 'path': str(p), 'sha256': write_x(p, spec_bytes(c2)), 'driver': 'v001',
                    'outdir': str(RUNS / 'KMAX_A2F10_C2R_D7R1_RUN_V001'), 'derived_from': {'path': base_path, 'sha256': v4['anchor']['base_spec']['sha256']}}
    # Templates (fill after the cube prefix exists): cube reruns admitting their own v005 prefix, and wave-2 cases with R1
    templates = {}
    for cid in ('C3', 'C4', 'R'):
        w = json.loads((V003S / 'wave1' / ('CALL_KMAX_%s_A2F10_C2V003.json' % cid)).read_text())
        if canon(w['numerics']['brackets']) != canon(anchor_br) or w['admit'] != {}:
            raise SystemExit('REFUSED: unexpected wave1 spec %s' % cid)
        w['numerics']['brackets'] = copy.deepcopy(r1)
        own = RUNS / ('KMAX_A2F10_%s_V005_RUN_V001' % cid)
        w['admit'] = {'route_a': {'attempt_directory': 'PENDING(%s/stages/01_route_a/attempt_000)' % own, 'checkpoint_directory': 'PENDING(%s/stages/01_route_a/checkpoint)' % own,
                                  'identity_sha256': 'PENDING', 'result_sha256': 'PENDING'},
                      'reference': {'directory': 'PENDING(%s/stages/02_reference/reference)' % own, 'start_sha256': 'PENDING', 'finish_sha256': 'PENDING'},
                      'body': {'directory': 'PENDING(%s/stages/03_body/body)' % own, 'finish_sha256': 'PENDING'}}
        w['label'] = w['label'] + ' TEMPLATE | D7 recovery R1 step (4) rerun admitting its own v005 prefix (prereg V005)'
        p = OUT / ('specs_d7r1/templates/CALL_KMAX_%sR_A2F10_D7R1_C2V005.TEMPLATE.json' % cid)
        templates[cid + 'R'] = {'case': cid, 'path': str(p), 'sha256': write_x(p, spec_bytes(w)), 'driver': 'v005', 'cube_outdir': str(own),
                                'outdir': str(RUNS / ('KMAX_A2F10_%sR_D7R1_V005_RUN_V001' % cid))}
    for cid, cube in (('S3', 'C3'), ('Y3', 'C3'), ('S4', 'C4'), ('Y4', 'C4')):
        t = json.loads((V003S / 'templates' / ('CALL_KMAX_%s_A2F10_C2V003.TEMPLATE.json' % cid)).read_text())
        if canon(t['numerics']['brackets']) != canon(anchor_br):
            raise SystemExit('REFUSED: unexpected template %s' % cid)
        t['numerics']['brackets'] = copy.deepcopy(r1)
        own = RUNS / ('KMAX_A2F10_%s_V005_RUN_V001' % cube)
        t = json.loads(json.dumps(t).replace('<%s out>' % cube, str(own)))
        t['label'] = t['label'] + ' | brackets = D7 recovery R1 block (prereg V005); admits the v005 prefix of %s' % cube
        p = OUT / ('specs_d7r1/templates/CALL_KMAX_%s_A2F10_D7R1_C2V005.TEMPLATE.json' % cid)
        templates[cid] = {'case': cid, 'path': str(p), 'sha256': write_x(p, spec_bytes(t)), 'driver': 'v005', 'cube_outdir': str(own),
                          'outdir': str(RUNS / ('KMAX_A2F10_%s_D7R1_V005_RUN_V001' % cid))}

    # ---- stopped runs (F3)
    stopped = {
        'KMAX_A2F10_C4_RUN_V001': stop_record('KMAX_A2F10_C4_RUN_V001',
            'Coordinator choice: all cases on grids > 80 nodes/axis (C3 84, C4 96, R 92) run under ONE driver, v005, after C3 under v003 was BLOCKED '
            'ROUTE_A_NOT_CONVERGED_AT_ITERATION_4. For C4 the v003 limit would also have applied: its route A had NOT met the bound at iteration 4 '
            '(see iterations_completed) and was inside iteration 5. Rerun: KMAX_A2F10_C4_V005_RUN_V001 (v005, launched 16:39:59Z).'),
        'KMAX_A2F10_R_RUN_V001': stop_record('KMAX_A2F10_R_RUN_V001',
            'Coordinator choice to run all > 80-node cases under one driver (v005). NOT the iteration-4 limit: R\'s v003 route A MET its bound at '
            'iteration 4 (3.2273e56 < 4.1295e56; checkpoint attempt_end CONVERGED_FINITE_FIXED_POINT), so under v003 R would have proceeded to '
            'route B. The stop was not required by any gate; it discarded a converged v003 route A. Rerun: KMAX_A2F10_R_V005_RUN_V001 (v005, 16:39:59Z), '
            'route A recomputed from the seed.'),
        'KMAX_A2F3_C3_RUN_V001': stop_record('KMAX_A2F3_C3_RUN_V001',
            'Factor-3 matrix abandoned: anchor A2_ANCHOR_F3_RUN_V001 FAILED (rfs_columns_01 column 70 NO_TWO_SAMPLED_FREE_SURFACES); prereg V003 '
            '(sealed 15:44:15Z) moved the anchor to factor 10. These cases belong to no live registration.'),
        'KMAX_A2F3_C4_RUN_V001': stop_record('KMAX_A2F3_C4_RUN_V001', 'Factor-3 matrix abandoned (as KMAX_A2F3_C3_RUN_V001).'),
        'KMAX_A2F3_R_RUN_V001': stop_record('KMAX_A2F3_R_RUN_V001', 'Factor-3 matrix abandoned (as KMAX_A2F3_C3_RUN_V001).'),
    }
    for name in stopped:
        hits = alive(name)
        stopped[name]['process_alive_at_build'] = bool(hits)
        stopped[name]['process_check'] = {'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'matching_driver_or_monitor_processes': hits}
    f3_done = {}
    for name in ('KMAX_A2F3_S2_RUN_V001', 'KMAX_A2F3_Y2_RUN_V001'):
        run = RUNS / name
        fin = json.loads((run / 'finish.json').read_text())
        f3_done[name] = {'finish': {'path': str(run / 'finish.json'), 'sha256': sha_file(run / 'finish.json'), 'status': fin['status'], 'reasons': fin['reasons']},
                         'fs_failure_columns': sorted(int(x.name[7:11]) for x in run.glob('stages/*_fs_columns_*/columns/column_*_failure.json')),
                         'note': 'finished (not stopped) under the superseded factor-3 matrix; no recovery: no live registration.'}
    stop_sha = write_x(OUT / 'evidence/STOPPED_RUNS_V001.json', spec_bytes({'stopped': stopped, 'factor3_finished': f3_done}))

    # ---- v005 deciding test and v005 run dirs: EXISTENCE ONLY
    exist = {}
    for name in ['DDO154_ROUTE_B_C2V005_DECIDING_ADMIT_PREFIX_RUN_V001'] + ['KMAX_A2F10_%s_V005_RUN_V001' % c for c in ('C3', 'C4', 'R')]:
        d = RUNS / name
        exist[name] = {'dir_exists': d.is_dir(), 'result_json_exists': (d / 'result.json').exists(), 'finish_json_exists': (d / 'finish.json').exists()}

    # ---- prereg V005 (from V004 bytes)
    v5 = copy.deepcopy(v4)
    v5['schema'] = 'KMAX_MATRIX_PREREG_V005'
    v5['status'] = ('PREREGISTERED. V005 is sealed (SEAL_RECORD_V005.json) after: C2 = A2_ANCHOR_F10_RUN_V001 COMPLETED (v001); S2 and Y2 first attempts '
                    'FAILED_AT_STAGE under v001 (registered V1 (ii) failures, D7 recovery R1 invoked); C3 under v003 BLOCKED; C4 and R under v003 stopped '
                    '(amendment_v005.stopped_runs); and while the v005 runs of C3, C4, R and the v005 DDO deciding reproduction are running, before any of '
                    'their result.json or finish.json exists and before any D7 recovery call (S2R, Y2R, C2R, cube reruns) is launched. Thresholds, gates '
                    'and the decision rule are those of V002-V004 unchanged; a change is a new version with its reason recorded.')
    v5['supersedes'] = {'path': str(V004[0]), 'sha256': V004[1], 'seal': {'path': str(SEAL_V004), 'sha256': sha_file(SEAL_V004)},
                        'review': {'path': str(REVIEW), 'sha256': sha_file(REVIEW), 'message': str(REVIEW_MSG), 'message_sha256': sha_file(REVIEW_MSG),
                                   'verdict': 'FAIL (checks 1-4 hold; check 5 fails; F1 blocking; F3-F5)'},
                        'withdrawn_from_v004': 'driver_amendment_v004 is withdrawn as a whole: its gate-V3 sentence was prose the compare script never read (F1), '
                                               'and its sentences "Shapes sphere/cylinder are recorded BRACKET_PRECONDITION_FAILED at G2; the matrix proceeds '
                                               'with the cube shape; the prereg already allows a single passing shape" were not a pre-named outcome (check 5). '
                                               'No single-shape adoption is registered; decision rules 1-6 apply unchanged to all three shapes.'}
    del v5['driver_amendment_v004']
    v5['binding_inputs']['drivers']['v005'] = {'path': str(DRV5[0]), 'sha256': DRV5[1]}
    v5['binding_inputs']['v005_independent_check'] = {
        'path': str(CHECK5), 'sha256': sha_file(CHECK5), 'verdict': 'PASS_WITH_DEFECTS (1 MAJOR, 1 MEDIUM, 5 LOW, 1 INFO)', 'pins_driver_sha256': DRV5[1],
        'scope_used_here': 'DDO154 / deciding test: clean (pure binding change for DDO154; simulate-equivalent to c2v004 on ADMIT_PREFIX 19, PINNED_FULL 22, '
                           'RULE_FULL 20, ADMIT_ROUTE_A 21 stages). The MAJOR defect D1 is on the NGC3198 route-B binding, not on any DDO154 path.'}
    v5['binding_inputs']['v005_deciding_test'] = {
        'run_outdir': str(DECIDING_RUN), 'result_path': str(DECIDING_RUN / 'result.json'), 'finish_path': str(DECIDING_RUN / 'finish.json'),
        'launch_file': {'path': str(DECIDING_RUN) + '.receipt.json.launch.json', 'sha256': sha_file(str(DECIDING_RUN) + '.receipt.json.launch.json')},
        'call_spec': {'path': str(DECIDING_SPEC[0]), 'sha256': DECIDING_SPEC[1]}, 'driver_sha256': DRV5[1],
        'required': {'deciding_test.verdict': 'PASS_BITWISE_EQUAL', 'driver_sha256': DRV5[1], 'call_spec_sha256': DECIDING_SPEC[1],
                     'finish.result_sha256': 'equals sha256 of result.json bytes'},
        'state_at_build': exist['DDO154_ROUTE_B_C2V005_DECIDING_ADMIT_PREFIX_RUN_V001']}
    for c in v5['cases']:
        if c['id'] in V005_CASES:
            c['drivers_allowed'] = c['drivers_allowed'] + ['v005']
    v5['amendment_v005'] = {
        'driver': {
            'rule': 'v005 (2aef51c4) is added to binding_inputs.drivers and to drivers_allowed of C3, C4, R and of the cases admitting their cubes '
                    '(S3, Y3 admit C3; S4, Y4 admit C4; gate V6 requires the admitted case to run under its cube\'s driver). v003 stays allowed. '
                    'C2, S2, Y2 stay v001/v003 (C2 = F10 prefix is v001; V6 makes S2/Y2 v001).',
            'admissibility_condition': 'A case whose driver_sha256 is v005 is admissible (gate V3 driver term) only if binding_inputs.v005_deciding_test.result_path '
                                       'exists at comparison time, its finish.json result_sha256 equals the sha256 of its bytes, its driver_sha256 and call_spec_sha256 '
                                       'equal the pinned values, and its deciding_test.verdict is PASS_BITWISE_EQUAL. Otherwise every v005 case fails V3 with reason '
                                       'V005_INADMISSIBLE:<reason> and the matrix is INCOMPLETE (rule 1). Executed by kmax_compare_c2v005.py, which reads that file '
                                       'only at comparison time.',
            'inadmissible_next_step': 'V005_INADMISSIBLE: the >80-node cases have no admissible driver; gate V1 (iii) applies (matrix stops as BLOCKED_ROUTE_A at '
                                      'those grids; next step is a reviewed route-B successor that accepts the converged route-A iteration and passes the DDO '
                                      'deciding reproduction, under separate review). No v005 case result is used.',
            'admission_constraint_note': 'admission_constraint (inherited text) names v003 for S3/Y3/S4/Y4; the rule it states (same driver as the cube) is '
                                         'unchanged, so with v005 cubes S3/Y3/S4/Y4 run under v005.'},
        'd7_recovery': {
            'invoked': True,
            'registered_first_attempts': {cid: {k: evid[cid][k] for k in ('run', 'call_spec', 'finish', 'result_sha256', 'fs_rotation_last_stderr_line', 'gate')}
                                          | {'missed_columns': [c['index'] for c in evid[cid]['missed_columns']]} for cid in ('S2', 'Y2')},
            'p6_outcome': 'Bracket precondition P6 TESTED-NEGATIVE for the inherited fs override entries at S2 (6 columns) and Y2 (1 column); TESTED-POSITIVE at '
                          'C2 (all fs/rfs/le passes completed). Each miss: mass residual > 0 at both ends of [3.025e8, 3.17625e8] (root below lo).',
            'W1_widening_rule': 'D7 step (1), for each missed column entry [lo, hi] with the failed call\'s mass residuals r(lo), r(hi) as evidence: if r(lo) > 0 and '
                                'r(hi) > 0 (root below lo): lo -> template_lo if lo > template_lo else lo/2; if r(lo) < 0 and r(hi) < 0 (root above hi): '
                                'hi -> 1.05*template_hi if hi < 1.05*template_hi else 2*hi; the other end is kept. fs template = [1.5125e8, 3.025e8] '
                                '(driver v001 solver template DDO154_REMAINING_FREE_SURFACE_CONTROLS_V001 5d69360f); for rfs/le factor entries the template is '
                                'the rule factor pair of that pass (rfs_factors; le_first_factors for pass 1, le_next_factors after). The hull '
                                '[template_lo, 1.05*template_hi] = [1.5125e8, 3.17625e8] contains the template and every inherited override and equals the '
                                'reviewed NGC fs bracket [h0/2, 1.05 h0] (v005 CHECK_V001, N4).',
            'fs_template_bracket': FS_TEMPLATE,
            'R1': {'recovery_file': {'path': str(OUT / 'd7_recovery/KMAX_D7_RECOVERY_R1.json'), 'sha256': r1_sha},
                   'evidence_file': {'path': str(OUT / 'd7_recovery/D7_EVIDENCE_S2_Y2_V001.json'), 'sha256': ev_sha},
                   'brackets': r1,
                   'widened_entries': r1_rec['widened_entries'],
                   'corrected_base_spec': {'path': str(cbase_path), 'sha256': cbase_sha, 'differs_from_anchor_base_spec_in': 'numerics.brackets.rule.fs_absolute_overrides entries 5,6,7,8,9,45,50 only'}},
            'step4_every_case': 'D7 step (4) is applied as written: EVERY case is compared with the R1 block (gate V3, "the D7 recovery block, as a whole, for every '
                                'case"). Completed or running cases are rerun admitting their own prefixes: C2 -> C2R (v001, admits F10 route-A/reference/body, '
                                'passes 6); C3, C4, R (v005, running with the anchor block) -> C3R, C4R, RR admitting their own v005 prefixes once those exist; '
                                'S3, Y3, S4, Y4 are generated with R1 from the start. The first attempts stay on record.',
            'calls': calls, 'templates': templates,
            'case_binding_for_comparison': {'C2': 'C2R', 'S2': 'S2R', 'Y2': 'Y2R', 'C3': 'C3R', 'C4': 'C4R', 'R': 'RR',
                                            'S3': 'S3', 'Y3': 'Y3', 'S4': 'S4', 'Y4': 'Y4'},
            'later_invocations': 'The same rule applies to any later column-pass bracket miss in any case (S3, Y3, S4, Y4 included): R(n) = R(n-1) with only the '
                                 'newly missed entries widened by W1 from that failed call\'s evidence; every case is regenerated with R(n) (completed cases rerun '
                                 'admitting their own prefixes); the comparison takes --bracket-recovery R(n). The compare script refuses a recovery block that '
                                 'changes anything but override entries, narrows or removes any anchor entry, or does not contain every R1 entry. A column that '
                                 'misses again after a W1 step B widening is reported BRACKET_RECOVERY_EXHAUSTED for review (matrix INCOMPLETE). A miss of type '
                                 '"no bracket source" is outside W1 and is reported for review.'},
        'stopped_runs': {'record': {'path': str(OUT / 'evidence/STOPPED_RUNS_V001.json'), 'sha256': stop_sha},
                         'summary': {
                             'KMAX_A2F10_C4_RUN_V001': 'v003, launched 15:45:33Z, stopped by the coordinator at or after %s (last byte); route A not converged at iteration 4, '
                                                       'in iteration 5 (column 575/576); no finish/receipt; reason: all >80-node cases under one driver (v005).' % stopped['KMAX_A2F10_C4_RUN_V001']['last_byte_written']['utc_mtime'],
                             'KMAX_A2F10_R_RUN_V001': 'v003, launched 15:45:33Z, stopped by the coordinator at or after %s (last byte: route-A attempt_end CONVERGED); route A MET its '
                                                      'bound at iteration 4 (3.2273e56 < 4.1295e56), so the iteration-4 limit did not apply; reason: coordinator choice to '
                                                      'run all >80-node cases under one driver; R reruns under v005.' % stopped['KMAX_A2F10_R_RUN_V001']['last_byte_written']['utc_mtime'],
                             'KMAX_A2F3_{C3,C4,R}_RUN_V001': 'v003, launched 15:27:18Z, stopped (last bytes 15:44Z) when the factor-3 anchor failed and V003 moved to factor 10.'}},
        'status_correction': 'V004 status text ("before any other case is launched") was inherited and false at the V004 seal; the V005 status states what was sealed before what.',
        'unchanged': 'anchor, row_ids, quoted_sigma_km_s, tau_km_s, grids, grids_note, cases (except drivers_allowed of C3, C4, R, S3, Y3, S4, Y4), admission_constraint, '
                     'fixed_across_all_cases, criterion (thresholds, gates V1-V6, gate_next_steps, P6, decision_rule 1-6, picard_equivalence, statistics) are '
                     'byte-identical to V004 (canonical JSON).'}
    # ---- guard: unchanged blocks
    for k in ('anchor', 'row_ids', 'quoted_sigma_km_s', 'tau_km_s', 'grids', 'grids_note', 'admission_constraint', 'fixed_across_all_cases', 'criterion',
              'plan_item', 'change_log_v003'):
        if canon(v5[k]) != canon(v4[k]):
            raise SystemExit('REFUSED: %s changed' % k)
    for a, b in zip(v4['cases'], v5['cases']):
        if canon({k: v for k, v in a.items() if k != 'drivers_allowed'}) != canon({k: v for k, v in b.items() if k != 'drivers_allowed'}):
            raise SystemExit('REFUSED: case %s changed beyond drivers_allowed' % a['id'])
    for k in ('a2_coefficients', 'anchor_base_spec', 'base_seed', 'driver_equivalence_evidence', 'independent_check', 'root_decisions', 'row_binding', 'sigma_source'):
        if canon(v5['binding_inputs'][k]) != canon(v4['binding_inputs'][k]):
            raise SystemExit('REFUSED: binding_inputs.%s changed' % k)
    v5 = {k: v5[k] for k in sorted(v5)}
    psha = write_x(OUT / 'KMAX_MATRIX_PREREG_V005.json', spec_bytes(v5))
    print(json.dumps({'prereg_v005_sha256': psha, 'r1_sha256': r1_sha, 'corrected_base_sha256': cbase_sha,
                      'calls': {k: v['sha256'] for k, v in calls.items()}, 'templates': {k: v['sha256'] for k, v in templates.items()},
                      'widened': widened, 'existence': exist}, indent=1))


# --------------------------------------------------------------------------- fill (after seal)
def fill(template, cube_out, out_spec):
    gen = load_gen()
    t = json.loads(Path(template).read_text())
    pre = json.loads((OUT / 'KMAX_MATRIX_PREREG_V005.json').read_text())
    r1 = pre['amendment_v005']['d7_recovery']['R1']['brackets']
    if canon(t['numerics']['brackets']) != canon(r1):
        raise SystemExit('REFUSED: template brackets are not R1')
    admit, cube = gen.admission_from_cube_out(cube_out)
    for k in ('physical', 'coefficients'):
        if cube[k] != t[k]:
            raise SystemExit('REFUSED: cube %s differs from template' % k)
    if cube['numerics']['composite_grid_spec'] != t['numerics']['composite_grid_spec'] or cube['numerics']['truncation'] != {'shape': 'cube'}:
        raise SystemExit('REFUSED: cube grid/truncation differ from template')
    if canon(cube['numerics']['brackets']) not in (canon(pre['anchor']['brackets']), canon(r1)):
        raise SystemExit('REFUSED: cube brackets are neither the anchor block nor R1')
    if 'PENDING' not in json.dumps(t['admit']):
        raise SystemExit('REFUSED: template admit is not PENDING')
    t['admit'] = admit
    t['label'] = t['label'].replace(' TEMPLATE', '') + '; admits %s' % cube_out
    print(json.dumps({'spec': out_spec, 'sha256': write_x(out_spec, spec_bytes(t)), 'admit': admit}, indent=1))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
    elif len(sys.argv) == 5 and sys.argv[1] == 'fill':
        fill(*sys.argv[2:])
    else:
        print(__doc__)
        sys.exit(2)

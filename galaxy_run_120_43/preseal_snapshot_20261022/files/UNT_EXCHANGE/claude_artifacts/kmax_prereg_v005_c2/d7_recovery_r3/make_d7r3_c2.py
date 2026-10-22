"""D7 recovery R3 under sealed prereg V005 (Claude2 lane, c2v005): evidence, R3 block, R3 specs, dry-runs, launch file.

Method of d7_recovery_r2/make_d7r2_c2.py (pinned 53314f55), one invocation later.  Applies
amendment_v005.d7_recovery.later_invocations: R3 = R2 with only the newly missed fs entries widened by the declared W1
rule (make_kmax_v005_c2.widen_W1, imported from the pinned builder bytes) from the failed calls' own evidence
(C4R2 / S4R2 / Y4R2 D7R2 runs, FAILED_AT_STAGE at fs_rotation).  W1 step A moves a missed end to the hull
[template_lo, 1.05*template_hi]; a miss on an entry already widened by R1/R2 is step B (halve lo / double hi); a column
that misses again after a step B widening is BRACKET_RECOVERY_EXHAUSTED -> STOP (BLOCKED, nothing written past evidence).
Read scope on the failed D7R2 runs: launch.json, monitor log, finish.json (status/reasons; bytes hashed), stage directory
listings, column *_failure.json / *_iterations.jsonl, *_fs_rotation/stderr.txt.  It never opens result.json, inputs/ or
any rotation/speed array of those runs.  Admission blocks are re-derived with the reviewed generator
(admission_from_cube_out), which reads only the admitted prefix of the cube outdir.
All 10 cases are regenerated from their R2 counterparts (C4R2/S4R2/Y4R2: the filled R2 specs the failed runs launched).
Writes only under this directory (exclusive create; never check/ nor STOPPED_R2_RUNS_V001.json).  Launches nothing.

usage: python3 -I -B make_d7r3_c2.py build | dryrun | launch
"""
import copy
import glob
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/d7_recovery_r3')
V5 = HERE.parent
R2D = V5 / 'd7_recovery_r2'
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
RUNS = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs')
BUILDER = (V5 / 'make_kmax_v005_c2.py', 'e2cddb1ed345709d795125655535ff69a24eb98959c67218e0eda8de3bdb49c6')
COMPARE = (V5 / 'kmax_compare_c2v005.py', '49404bc4b0d558c93113ed650802d9009f03be64c364f0d862213783389786f5')
PREREG = (V5 / 'KMAX_MATRIX_PREREG_V005.json', 'dbddc02c4d793b44a12136fc4fc88b20c001865ddd4c89b1b70c57bc406bb174')
R1F = (V5 / 'd7_recovery/KMAX_D7_RECOVERY_R1.json', 'b3938db22cc7758a40fe3559c5213873807646f1b01771c4b9fb685e71bec365')
R2F = (R2D / 'KMAX_D7_RECOVERY_R2.json', 'ff7cf806cc3e297201cc151d05ce46b1c43e911d3a9dda15f1a07734532e93fd')
R2EV = (R2D / 'D7_EVIDENCE_C3R_S3_Y3_V001.json', 'f0d5180e701083c48fb3ec7b95380c88cd9d04e9944019e32ba0252270730da1')
R2BUILD = (R2D / 'BUILD_R2_RECORD.json', 'd59c74464ec3ae144cf3afae39ec0f35fe19359af3099a7ec2e4fd3b8abd18a5')
R2MAKE = (R2D / 'make_d7r2_c2.py', '53314f550cbc166375c64e635264e13dbdfdbff6c4a522a452aa4c6471a96b86')
R2LAUNCH = (R2D / 'LAUNCH_R2.json', '47e79e17087f4b014cb5b237554b6f351410f070f352af99052efa0bfb6fb945')
STOPPED = HERE / 'STOPPED_R2_RUNS_V001.json'
DRV = {'v001': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/galaxy_m0_forward_c2_0466/galaxy_m0_forward_c2v001.py',
                '75b0c08a44eac92caedd46564eaaefe08b88a6c536e95cb46f54a9d8da962f22'),
       'v005': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_impl_c2/binding/galaxy_m0_forward_c2v005.py',
                '2aef51c4a4cf0ee192594ab366e9b37e54881977df2e4d1b2f259a759818a42f')}
MONITOR = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/galaxy_m0_forward_c2_0466/root_monitor_c2v001.py',
           'ba031c2340057d88ee399138cc645012a93aa7dc3eb7c9bba56d112c94a47107')
CAPS = {'v001': {'wall_cap_s': 21600, 'rss_cap_bytes': 3221225472, 'output_cap_bytes': 17179869184, 'poll_s': 2.0},
        'v005': {'wall_cap_s': 28800, 'rss_cap_bytes': 3221225472, 'output_cap_bytes': 17179869184, 'poll_s': 2.0}}
F10 = RUNS / 'A2_ANCHOR_F10_RUN_V001'
C3V5 = RUNS / 'KMAX_A2F10_C3_V005_RUN_V001'
RV5 = RUNS / 'KMAX_A2F10_R_V005_RUN_V001'
C4V5 = RUNS / 'KMAX_A2F10_C4_V005_RUN_V001'
S2 = R2D / 'specs_d7r2'
# failed D7R2 calls (driver v005): run, spec launched (sha = launch.json pin), expected missed columns (from the task)
FAILED = {'C4R2': (RUNS / 'KMAX_A2F10_C4R2_D7R2_RUN_V001', S2 / 'filled/CALL_KMAX_C4R2_A2F10_D7R2_C2V005.json',
                   '12e29f3bf6728ba44368df6f44d2a8b2eeb499b5a41eeafc209b428550cc22d9', [2, 66, 67, 68]),
          'S4R2': (RUNS / 'KMAX_A2F10_S4R2_D7R2_RUN_V001', S2 / 'filled/CALL_KMAX_S4R2_A2F10_D7R2_C2V005.json',
                   '093508fde0b8a7d19d9597349a636f13c4a9c3289ae55d14c0d8b94d8983ca89', [66, 67, 68]),
          'Y4R2': (RUNS / 'KMAX_A2F10_Y4R2_D7R2_RUN_V001', S2 / 'filled/CALL_KMAX_Y4R2_A2F10_D7R2_C2V005.json',
                   '80db47bd14a7f12d591eea7ce1d7ba9999c11c55843c307bd8a2c2b7f6d68c67', [2, 71])}
# R3 specs: name -> (R2 counterpart, its sha, driver, admitted prefix, R2 dry-run dir)
SPECS = {
    'C2R3': (S2 / 'CALL_KMAX_C2R2_A2F10_D7R2_C2V005.json', '8f4a32471051de1fd427c0cf6242fea07c268f631a379d90988bb6c0ea6b6866', 'v001', F10, R2D / 'dryrun_r2/C2R2'),
    'S2R3': (S2 / 'CALL_KMAX_S2R2_A2F10_D7R2_C2V005.json', '23b8793df5edc22b009cbb6b3c6134e0e8a123742f5f1513e7e6be6bc3941ded', 'v001', F10, R2D / 'dryrun_r2/S2R2'),
    'Y2R3': (S2 / 'CALL_KMAX_Y2R2_A2F10_D7R2_C2V005.json', '73e3709fe5ed82fa5dc0da21c226ad9f260c269b7b57abc4dd3adb801e246df6', 'v001', F10, R2D / 'dryrun_r2/Y2R2'),
    'C3R3': (S2 / 'CALL_KMAX_C3R2_A2F10_D7R2_C2V005.json', '001395fa03334019debe4c0996aa35d08fa322b7634be014744ef11829c7d2ff', 'v005', C3V5, R2D / 'dryrun_r2/C3R2'),
    'S3R3': (S2 / 'CALL_KMAX_S3R2_A2F10_D7R2_C2V005.json', 'aa636d162a3ddc45155e615064c57faf131e99c02a975794ebb76780724c2f51', 'v005', C3V5, R2D / 'dryrun_r2/S3R2'),
    'Y3R3': (S2 / 'CALL_KMAX_Y3R2_A2F10_D7R2_C2V005.json', 'aea097d74bfd43459f15b3dae3fa08bb244c3985e4ef55810feaab667aec51a8', 'v005', C3V5, R2D / 'dryrun_r2/Y3R2'),
    'RR3': (S2 / 'CALL_KMAX_RR2_A2F10_D7R2_C2V005.json', '9f74dbad7310119a1108ff05524f3df941c5a68b4b48dfdc762a5208f7d46308', 'v005', RV5, R2D / 'dryrun_r2/RR2'),
    'C4R3': (S2 / 'filled/CALL_KMAX_C4R2_A2F10_D7R2_C2V005.json', '12e29f3bf6728ba44368df6f44d2a8b2eeb499b5a41eeafc209b428550cc22d9', 'v005', C4V5, R2D / 'dryrun_r2_c4/C4R2'),
    'S4R3': (S2 / 'filled/CALL_KMAX_S4R2_A2F10_D7R2_C2V005.json', '093508fde0b8a7d19d9597349a636f13c4a9c3289ae55d14c0d8b94d8983ca89', 'v005', C4V5, R2D / 'dryrun_r2_c4/S4R2'),
    'Y4R3': (S2 / 'filled/CALL_KMAX_Y4R2_A2F10_D7R2_C2V005.json', '80db47bd14a7f12d591eea7ce1d7ba9999c11c55843c307bd8a2c2b7f6d68c67', 'v005', C4V5, R2D / 'dryrun_r2_c4/Y4R2')}
C4_FILL = ('C4R3', 'S4R3', 'Y4R3')   # R2 counterparts were filled from templates after the R2 build; re-check the fill
ORDER = tuple(SPECS)
KEY_RE = re.compile(r'0|[1-9][0-9]*')


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    return sha_bytes(Path(p).read_bytes())


def pinned(path, sha, label):
    raw = Path(path).read_bytes()
    if sha_bytes(raw) != sha:
        raise SystemExit('REFUSED: %s pin mismatch (%s)' % (label, path))
    return raw


def load_mod(path, sha, name):
    pinned(path, sha, name)
    s = importlib.util.spec_from_file_location(name, str(path))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


B = load_mod(*BUILDER, 'make_kmax_v005_c2')
canon, spec_bytes, write_x, utc_of = B.canon, B.spec_bytes, B.write_x, B.utc_of
HULL = [B.FS_TEMPLATE[0], 1.05 * B.FS_TEMPLATE[1]]


def leaves(o, p=''):
    if isinstance(o, dict):
        out = {}
        for k, v in o.items():
            out.update(leaves(v, p + '/' + str(k)))
        return out
    if isinstance(o, list) and o and any(isinstance(x, (dict, list)) for x in o):
        out = {}
        for i, v in enumerate(o):
            out.update(leaves(v, p + '/' + str(i)))
        return out
    return {p: o}


def leaf_diff(a, b):
    la, lb = leaves(a), leaves(b)
    return sorted(k for k in set(la) | set(lb) if la.get(k, '<absent>') != lb.get(k, '<absent>'))


def lint_override_keys(o, path='', bad=None):
    bad = [] if bad is None else bad
    if isinstance(o, dict):
        for k, v in o.items():
            if k.endswith('_overrides') and isinstance(v, dict):
                for k2, v2 in v.items():
                    if not KEY_RE.fullmatch(k2):
                        bad.append('%s/%s/%s' % (path, k, k2))
                    if isinstance(v2, dict):
                        for k3 in v2:
                            if not KEY_RE.fullmatch(k3):
                                bad.append('%s/%s/%s/%s' % (path, k, k2, k3))
            lint_override_keys(v, path + '/' + k, bad)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            lint_override_keys(v, path + '/%d' % i, bad)
    return bad


def w1_step(entry, r_lo, r_hi):
    """Which declared W1 step widen_W1 takes (A: hull end; B: halve/double)."""
    h_lo, h_hi = HULL
    if r_lo > 0 and r_hi > 0:
        return 'A' if entry[0] > h_lo else 'B'
    if r_lo < 0 and r_hi < 0:
        return 'A' if entry[1] < h_hi else 'B'
    return None


def prior_step(we):
    """Declared step of an earlier (R1/R2) widening, from its own record."""
    if 'W1_step' in we:
        return sorted(set(we['W1_step']))
    f, t = we['from'], we['to']   # R1 records carry from/to only
    steps = set()
    if t[0] != f[0]:
        steps.add('A' if t[0] == HULL[0] and f[0] > HULL[0] else 'B')
    if t[1] != f[1]:
        steps.add('A' if t[1] == HULL[1] and f[1] < HULL[1] else 'B')
    return sorted(steps)


def contains(outer, inner):
    return outer is not None and outer[0] <= inner[0] and inner[1] <= outer[1]


# --------------------------------------------------------------------------- evidence (read scope above)
def miss_evidence(cid, r2):
    outdir, spec_path, spec_sha, expected = FAILED[cid]
    spec = json.loads(pinned(spec_path, spec_sha, cid + ' spec'))
    launch_p = Path(str(outdir) + '.receipt.json.launch.json')
    launch_raw = launch_p.read_bytes()
    launch = json.loads(launch_raw)
    if launch['pins']['spec'] != {'path': str(spec_path), 'sha256': spec_sha} or launch['pins']['driver']['sha256'] != DRV['v005'][1]:
        raise SystemExit('REFUSED: %s launch pins differ from the R2 spec / driver v005' % cid)
    if canon(spec['numerics']['brackets']) != canon(r2):
        raise SystemExit('REFUSED: %s ran with a brackets block other than R2' % cid)
    fin_raw = (outdir / 'finish.json').read_bytes()
    fin = json.loads(fin_raw)
    fin_sr = {'status': fin['status'], 'reasons': fin['reasons']}
    del fin
    if fin_sr['status'] != 'FAILED_AT_STAGE':
        raise SystemExit('REFUSED: %s finish not FAILED_AT_STAGE' % cid)
    mon_p = Path(str(outdir) + '.monitor.log')
    mon_last = json.loads(mon_p.read_text().strip().splitlines()[-1])
    if mon_last.get('driver_status') != 'FAILED_AT_STAGE':
        raise SystemExit('REFUSED: %s monitor log last record not driver_status FAILED_AT_STAGE' % cid)
    rule = spec['numerics']['brackets']['rule']['fs_absolute_overrides']
    cols = []
    for f in sorted(outdir.glob('stages/*_fs_columns_*/columns/column_*_failure.json')):
        fail = json.loads(f.read_text())
        it = f.with_name(f.name.replace('_failure.json', '_iterations.jsonl'))
        hist = [json.loads(x) for x in it.read_text().splitlines() if x.strip()]
        idx = int(fail['index'])
        entry = list(rule.get(str(idx), B.FS_TEMPLATE))
        if not fail['message'].startswith('MASS_ENTHALPY_NOT_BRACKETED') or len(hist) != 2 \
                or [h['Hc_m2_s2'] for h in hist] != entry:
            raise SystemExit('REFUSED: unexpected failure record %s' % f)
        r_lo, r_hi = hist[0]['mass_relative_residual'], hist[1]['mass_relative_residual']
        new, why = B.widen_W1(entry, B.FS_TEMPLATE, r_lo, r_hi)
        cols.append({'index': idx, 'stage_dir': f.parent.parent.name, 'message': fail['message'],
                     'failure_file': {'path': str(f), 'sha256': sha_file(f)}, 'iterations_file': {'path': str(it), 'sha256': sha_file(it)},
                     'entry_in_failed_call': entry,
                     'entry_source': 'R2 fs_absolute_overrides[%d]' % idx if str(idx) in rule else 'fs template (no override key)',
                     'evidence': [{'Hc_m2_s2': h['Hc_m2_s2'], 'mass_relative_residual': h['mass_relative_residual']} for h in hist],
                     'W1': {'new_entry': new, 'step': why, 'declared_step': w1_step(entry, r_lo, r_hi)}})
    if sorted(c['index'] for c in cols) != expected:
        raise SystemExit('REFUSED: %s missed columns %s != expected %s' % (cid, [c['index'] for c in cols], expected))
    rot = sorted(outdir.glob('stages/*_fs_rotation/stderr.txt'))
    if len(rot) != 1:
        raise SystemExit('REFUSED: %s expected one fs_rotation stderr' % cid)
    rot_err = rot[0].read_text().strip().splitlines()[-1]
    return spec, {'case': cid, 'run': str(outdir), 'driver_sha256': launch['pins']['driver']['sha256'],
                  'call_spec': {'path': str(spec_path), 'sha256': spec_sha},
                  'launch_file': {'path': str(launch_p), 'sha256': sha_bytes(launch_raw), 'utc': launch['utc'], 'caps': launch['caps']},
                  'finish': {'path': str(outdir / 'finish.json'), 'sha256': sha_bytes(fin_raw), 'status': fin_sr['status'], 'reasons': fin_sr['reasons'],
                             'utc_mtime': utc_of(outdir / 'finish.json')},
                  'result_sha256': mon_last['result']['sha256'],
                  'result_sha256_source': 'monitor log last record (%s); result.json not opened (lane read scope)' % mon_p,
                  'monitor_last_record': {k: mon_last.get(k) for k in ('status', 'exit_code', 'stop_reason', 'driver_status', 'elapsed_seconds', 'peak_rss_bytes')},
                  'fs_rotation_stderr': {'path': str(rot[0]), 'sha256': sha_file(rot[0])},
                  'fs_rotation_last_stderr_line': rot_err,
                  'gate': 'V1 (ii) FAILED_AT_STAGE with a bracket miss in a column pass -> D7 recovery (later invocation R3)',
                  'missed_columns': cols}


# --------------------------------------------------------------------------- build
def build():
    for p in ('D7_EVIDENCE_C4R2_S4R2_Y4R2_V001.json', 'KMAX_D7_RECOVERY_R3.json', 'specs_d7r3', 'BUILD_R3_RECORD.json'):
        if (HERE / p).exists():
            raise SystemExit('REFUSED: %s exists' % p)
    pre = json.loads(pinned(*PREREG, 'prereg V005'))
    C = load_mod(*COMPARE, 'kmax_compare_c2v005')
    gen = B.load_gen()
    r1rec = json.loads(pinned(*R1F, 'R1'))
    r2rec = json.loads(pinned(*R2F, 'R2'))
    pinned(*R2EV, 'R2 evidence')
    pinned(*R2BUILD, 'R2 build record')
    pinned(*R2MAKE, 'R2 maker')
    pinned(*R2LAUNCH, 'R2 launch')
    r1, r2 = r1rec['brackets'], r2rec['brackets']
    d7 = pre['amendment_v005']['d7_recovery']
    if canon(r1) != canon(d7['R1']['brackets']) or d7['fs_template_bracket'] != B.FS_TEMPLATE:
        raise SystemExit('REFUSED: R1 file differs from prereg R1 or template differs')
    if C.validate_recovery(pre, r2):
        raise SystemExit('REFUSED: R2 itself not accepted by the sealed validator')
    anc = pre['anchor']['brackets']

    # ---- 1. evidence
    evid = {}
    for cid in FAILED:
        _, evid[cid] = miss_evidence(cid, r2)
    ev_path = HERE / 'D7_EVIDENCE_C4R2_S4R2_Y4R2_V001.json'
    ev_sha = write_x(ev_path, spec_bytes(evid))

    # ---- 2. W1 -> R3
    r2_fs = r2['rule']['fs_absolute_overrides']
    prior = r2rec['widened_entries']                     # R1 + R2 widenings
    proposals = {}
    for cid in FAILED:
        for c in evid[cid]['missed_columns']:
            proposals.setdefault(str(c['index']), []).append({'case': cid, 'from': c['entry_in_failed_call'], 'to': c['W1']['new_entry'],
                                                              'step': c['W1']['declared_step'], 'why': c['W1']['step']})
    # exhaustion / step-B classification before anything else is written
    exhausted, rewiden = [], {}
    for k, props in proposals.items():
        if k in prior:
            ps = prior_step(prior[k])
            rewiden[k] = {'prior_invocation': prior[k].get('invocation'), 'prior_step': ps, 'W1_step_now': sorted({p['step'] for p in props})}
            if 'B' in ps:
                exhausted.append(k)
            elif any(p['step'] != 'B' for p in props):
                raise SystemExit('REFUSED: column %s was widened before (step A, to the hull) but W1 now reports step %s' % (k, props))
    if exhausted:
        raise SystemExit('BLOCKED: BRACKET_RECOVERY_EXHAUSTED for columns %s (missed again after a W1 step B widening; matrix INCOMPLETE); '
                         'evidence %s sha256 %s' % (sorted(exhausted, key=int), ev_path, ev_sha))
    widened, conflicts = {}, []
    for k, props in proposals.items():
        if len({canon(p['from']) for p in props}) != 1:
            raise SystemExit('BLOCKED: column %s entry differs across the failed calls (all ran R2)' % k)
        tos = {canon(p['to']): p['to'] for p in props}
        if len(tos) == 1:
            widened[k] = list(tos.values())[0]
            continue
        cand = [t for t in tos.values() if all(contains(t, u) for u in tos.values())]
        if len(cand) != 1:
            raise SystemExit('BLOCKED: conflicting W1 results for column %s %s: no single result contains the others; '
                             'the declared rule does not define this case' % (k, list(tos.values())))
        widened[k] = cand[0]
        conflicts.append({'column': k, 'results': props, 'taken': cand[0], 'rule': 'took the W1 result that contains all others'})
    if widened != {k: HULL for k in ('2', '66', '67', '68', '71')} or rewiden:   # the reason text below states these values
        raise SystemExit('REFUSED: W1 results %s / re-widenings %s differ from the stated R3 reason; rewrite the reason' % (widened, rewiden))
    cross = {k: {'cases': [p['case'] for p in proposals[k]], 'from': proposals[k][0]['from'], 'to_all_equal': len({canon(p['to']) for p in proposals[k]}) == 1,
                 'steps': sorted({p['step'] for p in proposals[k]}), 'branches': sorted({p['why'].split(':')[0] for p in proposals[k]})}
             for k in sorted(proposals, key=int)}
    r3 = copy.deepcopy(r2)
    fs = dict(r3['rule']['fs_absolute_overrides'])
    for k, v in widened.items():
        fs[k] = v
    r3['rule']['fs_absolute_overrides'] = {k: fs[k] for k in sorted(fs)}
    new_keys = sorted(widened, key=int)
    we = {}
    for k in sorted(set(prior) | set(widened), key=int):
        if k in widened:
            p0 = proposals[k][0]
            we[k] = {'invocation': 'R3', 'from_R2': r2_fs.get(k, B.FS_TEMPLATE),
                     'from_source': 'R2 entry' if k in r2_fs else 'fs template (no override key in R2)', 'to': widened[k],
                     'W1_step': sorted({p['step'] for p in proposals[k]}), 'W1_branch': p0['why'].split(':')[0],
                     'evidenced_by': [p['case'] for p in proposals[k]]}
        else:
            we[k] = prior[k]
    r3_rec = {'brackets': r3,
              'reason': 'D7 recovery R3 (prereg V005 amendment_v005.d7_recovery.later_invocations): R3 = R2 with only the newly missed fs entries '
                        'widened by W1 from the failed D7R2 calls\' own evidence. C4R2 (KMAX_A2F10_C4R2_D7R2_RUN_V001: columns 2,66,67,68), '
                        'S4R2 (KMAX_A2F10_S4R2_D7R2_RUN_V001: 66,67,68), Y4R2 (KMAX_A2F10_Y4R2_D7R2_RUN_V001: 2,71) failed '
                        'MASS_ENTHALPY_NOT_BRACKETED at fs. Columns 2,66,67,68,71 (template [1.5125e8, 3.025e8], no fs override in R2, never widened '
                        'by R1/R2): r < 0 at both ends (root above hi), W1 step A moves hi to 1.05*template_hi = 3.17625e8; lo kept. Columns 2 '
                        '(C4R2, Y4R2) and 66,67,68 (C4R2, S4R2) agree across cases (no conflict). No re-miss of an R1/R2-widened entry (no step B, '
                        'no BRACKET_RECOVERY_EXHAUSTED). R2 entries 3,4,5,6,7,8,9,45,46,47,48,49,50 and rfs_factor_overrides[71] unchanged. '
                        'No other key changes.',
              'invocation': 'R3',
              'widened_entries': we,
              'evidence': {'R1_recovery_file': {'path': str(R1F[0]), 'sha256': R1F[1]}, 'R2_recovery_file': {'path': str(R2F[0]), 'sha256': R2F[1]},
                           'R2_evidence_file': {'path': str(R2EV[0]), 'sha256': R2EV[1]},
                           'R3_evidence_file': {'path': str(ev_path), 'sha256': ev_sha},
                           **{cid: [{'index': c['index'], 'failure_file': c['failure_file'], 'iterations_file': c['iterations_file'],
                                     'evidence': c['evidence']} for c in evid[cid]['missed_columns']] for cid in FAILED}}}
    # sealed compare script: file-schema check of its main() and its validator, unchanged
    if not ({'brackets', 'reason'} <= set(r3_rec) <= {'brackets', 'reason', 'invocation', 'widened_entries', 'evidence'}) \
            or not isinstance(r3_rec.get('brackets'), dict) or r3_rec['brackets'].get('mode') != 'rule':
        raise SystemExit('REFUSED: R3 file schema')
    why = C.validate_recovery(pre, r3_rec['brackets'])
    if why:
        raise SystemExit('REFUSED: sealed validator rejects R3: %s' % why)
    # liveness of the validator: two tampered copies must be refused
    t1 = copy.deepcopy(r3)
    t1['rule']['fs_absolute_overrides']['5'] = anc['rule']['fs_absolute_overrides']['5']
    t2 = copy.deepcopy(r3)
    t2['rule']['fs_absolute_overrides']['66'] = [1.6e8, 3.17625e8]
    live = {'R1_entry_5_undone': C.validate_recovery(pre, t1), 'new_entry_66_not_containing_template': C.validate_recovery(pre, t2)}
    if not all(live.values()):
        raise SystemExit('REFUSED: validator liveness')
    # explicit checks
    r3_fs = r3['rule']['fs_absolute_overrides']
    own = {'contains_R1': all(contains(r3['rule'][key].get(i), e) for key in ('fs_absolute_overrides', 'rfs_factor_overrides') for i, e in r1['rule'][key].items()),
           'contains_R2': all(contains(r3['rule'][key].get(i), e) for key in ('fs_absolute_overrides', 'rfs_factor_overrides') for i, e in r2['rule'][key].items()),
           'only_override_entries_change': sorted(k for k in set(r2['rule']) | set(r3['rule']) if canon(r2['rule'].get(k)) != canon(r3['rule'].get(k))) == ['fs_absolute_overrides'],
           'changed_fs_entries_vs_R2': sorted((k for k in r3_fs if r3_fs[k] != r2_fs.get(k)), key=int),
           'new_keys_vs_R2': sorted((k for k in r3_fs if k not in r2_fs), key=int),
           'removed_keys_vs_R2': sorted((k for k in r2_fs if k not in r3_fs), key=int),
           'new_entries_contain_template': all(contains(r3_fs[k], B.FS_TEMPLATE) for k in r3_fs if k not in anc['rule']['fs_absolute_overrides']),
           'nothing_narrowed_vs_R2': all(contains(r3_fs.get(k), v) for k, v in r2_fs.items()),
           'nothing_narrowed_vs_anchor': all(contains(r3_fs.get(k), v) for k, v in anc['rule']['fs_absolute_overrides'].items()),
           'other_rule_keys_equal_R2': all(canon(r2['rule'][k]) == canon(r3['rule'][k]) for k in r2['rule'] if k != 'fs_absolute_overrides'),
           'only_evidenced_side_moved': all(widened[k][0] == proposals[k][0]['from'][0] for k in widened),
           'override_key_lint': lint_override_keys(r3)}
    if not (own['contains_R1'] and own['contains_R2'] and own['only_override_entries_change'] and own['changed_fs_entries_vs_R2'] == new_keys
            and own['new_keys_vs_R2'] == new_keys and not own['removed_keys_vs_R2'] and own['new_entries_contain_template']
            and own['nothing_narrowed_vs_R2'] and own['nothing_narrowed_vs_anchor'] and own['other_rule_keys_equal_R2']
            and own['only_evidenced_side_moved'] and not own['override_key_lint']):
        raise SystemExit('REFUSED: own R3 checks %s' % own)
    r3_sha = write_x(HERE / 'KMAX_D7_RECOVERY_R3.json', spec_bytes(r3_rec))

    # ---- 3. specs on R3
    adm = {F10: gen.admission_from_cube_out(str(F10)), C3V5: gen.admission_from_cube_out(str(C3V5)),
           RV5: gen.admission_from_cube_out(str(RV5)), C4V5: gen.admission_from_cube_out(str(C4V5))}
    note = (' | brackets = D7 recovery R3 block %s (prereg V005 d7_recovery.later_invocations; fs_absolute_overrides %s widened by W1 '
            'from the C4R2/S4R2/Y4R2 D7R2 failures)' % (r3_sha[:16], ','.join(new_keys)))
    r2build = json.loads(pinned(*R2BUILD, 'R2 build record'))
    out = {}
    expect_br = sorted('/numerics/brackets/rule/fs_absolute_overrides/%s' % k for k in new_keys)
    for name, (src, ssha, drv, cube, _dr) in SPECS.items():
        s2 = json.loads(pinned(src, ssha, name + ' R2 counterpart'))
        if canon(s2['numerics']['brackets']) != canon(r2):
            raise SystemExit('REFUSED: %s R2 counterpart brackets are not R2' % name)
        if 'PENDING' in json.dumps(s2['admit']):
            raise SystemExit('REFUSED: %s R2 counterpart admit is PENDING' % name)
        rec = {'r2_counterpart': {'path': str(src), 'sha256': ssha}, 'driver': drv, 'cube_outdir': str(cube), 'kind': 'filled'}
        if canon(s2['admit']) != canon(adm[cube][0]):
            raise SystemExit('REFUSED: %s admit is not the %s prefix re-derived from bytes' % (name, cube.name))
        rec['admit_rederived_equal'] = True
        if name in C4_FILL:   # = fill_r2_c2.py checks, against the C4 V005 prefix, now with R3 admissible
            r2n = name.replace('R3', 'R2')
            tsp = r2build['specs'][r2n]
            tmpl = json.loads(pinned(tsp['path'], tsp['sha256'], r2n + ' R2 template'))
            dt = leaf_diff(tmpl, s2)
            if [x for x in dt if not x.startswith('/admit/')] != ['/label'] or s2['label'] != tmpl['label'].replace(' TEMPLATE', '') + '; admits %s' % cube:
                raise SystemExit('REFUSED: %s filled R2 spec differs from its R2 template beyond admit + label: %s' % (r2n, dt))
            cspec = adm[cube][1]
            for k in ('physical', 'coefficients'):
                if cspec[k] != s2[k]:
                    raise SystemExit('REFUSED: cube %s differs from %s' % (k, name))
            if cspec['numerics']['composite_grid_spec'] != s2['numerics']['composite_grid_spec'] or cspec['numerics']['truncation'] != {'shape': 'cube'}:
                raise SystemExit('REFUSED: cube grid/truncation differ from %s' % name)
            if canon(cspec['numerics']['brackets']) not in (canon(anc), canon(r1), canon(r2), canon(r3)):
                raise SystemExit('REFUSED: cube brackets are neither the anchor block, R1, R2 nor R3')
            rec['fill_checks'] = {'r2_template': {'path': tsp['path'], 'sha256': tsp['sha256']}, 'filled_r2_vs_template_leaf_diff': dt,
                                  'cube_physical_coefficients_grid_truncation_equal': True,
                                  'cube_call_spec_brackets': 'anchor' if canon(cspec['numerics']['brackets']) == canon(anc) else 'R1/R2/R3'}
        s = copy.deepcopy(s2)
        s['numerics']['brackets'] = copy.deepcopy(r3)
        s['label'] = s2['label'] + note
        d = leaf_diff(s2, s)
        if d != sorted(['/label'] + expect_br):
            raise SystemExit('REFUSED: %s differs from its R2 counterpart beyond label + R3 entries: %s' % (name, d))
        lint = lint_override_keys(s)
        if lint:
            raise SystemExit('REFUSED: %s override key lint %s' % (name, lint))
        p = HERE / 'specs_d7r3' / ('CALL_KMAX_%s_A2F10_D7R3_C2V005.json' % name)
        rec.update({'path': str(p), 'sha256': write_x(p, spec_bytes(s)), 'leaf_diff_vs_R2_counterpart': d, 'override_key_lint': 'PASS',
                    'picard_passes': s['numerics']['picard']['passes'], 'admit_pending': 'PENDING' in json.dumps(s['admit'])})
        out[name] = rec
    record = {'schema': 'KMAX_D7_R3_BUILD_RECORD_C2V005', 'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
              'inputs': {'prereg': {'path': str(PREREG[0]), 'sha256': PREREG[1]}, 'compare': {'path': str(COMPARE[0]), 'sha256': COMPARE[1]},
                         'builder': {'path': str(BUILDER[0]), 'sha256': BUILDER[1]}, 'R1': {'path': str(R1F[0]), 'sha256': R1F[1]},
                         'R2': {'path': str(R2F[0]), 'sha256': R2F[1]}, 'R2_build_record': {'path': str(R2BUILD[0]), 'sha256': R2BUILD[1]},
                         'R2_maker_method': {'path': str(R2MAKE[0]), 'sha256': R2MAKE[1]}, 'R2_launch': {'path': str(R2LAUNCH[0]), 'sha256': R2LAUNCH[1]},
                         'root_stop_record_not_touched': {'path': str(STOPPED), 'sha256': sha_file(STOPPED)}},
              'evidence_file': {'path': str(ev_path), 'sha256': ev_sha},
              'R3_file': {'path': str(HERE / 'KMAX_D7_RECOVERY_R3.json'), 'sha256': r3_sha},
              'W1_proposals': proposals, 'cross_case_consistency': cross, 'conflicts': conflicts,
              'prior_widened_entries_missed_again': rewiden, 'bracket_recovery_exhausted': exhausted,
              'validator': {'function': 'kmax_compare_c2v005.validate_recovery (sealed 49404bc4) + main() file-schema check', 'reasons': why,
                            'accepted': not why, 'liveness_tampered_copies_refused': live}, 'own_checks': own,
              'admissions_rederived': {str(k): v[0] for k, v in adm.items()}, 'specs': out}
    write_x(HERE / 'BUILD_R3_RECORD.json', spec_bytes(record))
    print(json.dumps({'evidence_sha256': ev_sha, 'r3_sha256': r3_sha, 'new_or_changed': {k: widened[k] for k in new_keys}, 'cross_case': cross,
                      'conflicts': conflicts, 'validator_reasons': why, 'liveness': live, 'specs': {k: v['sha256'] for k, v in out.items()}}, indent=1))


# --------------------------------------------------------------------------- dry-runs
def fs_table(d):
    tab = {}
    for f in sorted(glob.glob(str(Path(d) / 'simulated_call/inputs/fs_controls_*.json'))):
        c = json.loads(Path(f).read_text())
        for i in c['radial_indices']:
            if str(i) in tab:
                raise SystemExit('column %s twice in %s' % (i, d))
            tab[str(i)] = c['solver']['enthalpy_bracket']
    return tab


def norm(s, d):
    return re.sub(r'/stages/[0-9][0-9]_', '/stages/NN_', s.replace(str(d), '$DRY'))


def stage_rows(d):
    """Non-fs-column stage rows (= d7_recovery_r2/stage_rows_r1_r2_c2.py masking)."""
    rep = json.loads((Path(d) / 'DRYRUN_REPORT.json').read_text())
    out = []
    for s in rep['stages']:
        if s['name'].startswith('fs_columns_'):
            continue
        argv = [norm(x, d) for x in (s.get('argv') or [])]
        argv = ['<sha>' if i > 0 and argv[i - 1] in ('--controls-sha256', '--column-manifest-sha256') else a for i, a in enumerate(argv)]
        nd = lambda o: json.loads(norm(json.dumps(o, sort_keys=True), d))
        out.append({'name': s['name'], 'kind': s.get('kind'), 'script_sha256': s.get('script_sha256'), 'argv': argv,
                    'stage_globals': nd(s.get('stage_globals')), 'module_patches': nd(s.get('module_patches')), 'mask': nd(s.get('mask'))})
    return out


def dryrun():
    rec = json.loads((HERE / 'BUILD_R3_RECORD.json').read_text())
    r3 = json.loads(pinned(rec['R3_file']['path'], rec['R3_file']['sha256'], 'R3'))['brackets']
    r3fs = r3['rule']['fs_absolute_overrides']
    new_keys = rec['own_checks']['changed_fs_entries_vs_R2']
    if (HERE / 'DRYRUN_R3_CHECKS.json').exists():
        raise SystemExit('REFUSED: DRYRUN_R3_CHECKS.json exists')
    res = {}
    for name in ORDER:
        sp = rec['specs'][name]
        pinned(sp['path'], sp['sha256'], name)
        drv = DRV[sp['driver']]
        pinned(drv[0], drv[1], 'driver ' + sp['driver'])
        rd = HERE / 'dryrun_r3' / name
        if rd.exists():
            raise SystemExit('REFUSED: %s exists' % rd)
        rd.parent.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        pr = subprocess.run(['nice', '-n', '10', PY, '-I', '-B', drv[0], 'dry-run', '--spec', sp['path'], '--report-dir', str(rd)],
                            capture_output=True, text=True)
        write_x(HERE / 'dryrun_r3' / (name + '.stdout.txt'), pr.stdout.encode())
        write_x(HERE / 'dryrun_r3' / (name + '.stderr.txt'), pr.stderr.encode())
        r = {'exit_code': pr.returncode, 'seconds': round(time.time() - t0, 2)}
        if pr.returncode == 0:
            rep = json.loads((rd / 'DRYRUN_REPORT.json').read_text())
            sm = rep['summary']
            tab = fs_table(rd)
            n = sm['bracket_rule_checks']['fs']['n']
            r.update({'report_sha256': sha_file(rd / 'DRYRUN_REPORT.json'),
                      'call_spec_sha256_ok': rep['call_spec_sha256'] == sp['sha256'], 'driver_sha256_ok': rep['driver_sha256'] == drv[1],
                      'stages_planned': sm['stages_planned'], 'pin_problems': sm['pin_problems'], 'scipy_imports': sm['scipy_imports'],
                      'binding_blockers': sm.get('binding_blockers', 'n/a (v001 report has no field)'),
                      'unexplained_refusals': sm.get('unexplained_refusals', 'n/a (v001 report has no field)'),
                      'refusals_beyond_pending_inputs': sm.get('refusals_beyond_pending_inputs', 'n/a (v001 report has no field)'),
                      'stage_admission_refused': sm.get('stage_admission_refused', 'n/a'),
                      'remaining_refusals_by_class': sm.get('remaining_refusals_by_class', 'n/a'),
                      'fs_columns_covered': sorted(map(int, tab)) == list(range(n)), 'fs_n': n,
                      'fs_table_matches_R3': all(tab[k] == (r3fs[k] if k in r3fs else B.FS_TEMPLATE) for k in tab)})
            r2d = SPECS[name][4]
            t2 = fs_table(r2d)
            diffc = sorted((k for k in set(t2) | set(tab) if t2.get(k) != tab.get(k)), key=int)
            r['fs_table_diff_vs_R2_dryrun'] = {'r2_dryrun': str(r2d), 'columns': diffc, 'equals_R3_changed_entries': diffc == new_keys}
            a, b = stage_rows(r2d), stage_rows(rd)
            r['non_fs_stage_rows_vs_R2_dryrun'] = {'names': [x['name'] for x in b], 'identical': a == b,
                                                   'differing_rows': [x['name'] for x, y in zip(a, b) if x != y] + (['<count>'] if len(a) != len(b) else [])}
            ok = (r['call_spec_sha256_ok'] and r['driver_sha256_ok'] and not r['pin_problems'] and not r['scipy_imports']
                  and r['fs_columns_covered'] and r['fs_table_matches_R3'] and r['fs_table_diff_vs_R2_dryrun']['equals_R3_changed_entries']
                  and r['non_fs_stage_rows_vs_R2_dryrun']['identical'])
            if sp['driver'] == 'v005':
                ok = ok and r['binding_blockers'] == [] and r['unexplained_refusals'] == [] and r['refusals_beyond_pending_inputs'] == [] \
                     and r['stage_admission_refused'] == [] and (rep.get('binding_blockers') in ([], None))
            r['verdict'] = 'PASS' if ok else 'FAIL'
        else:
            r['verdict'] = 'FAIL'
        res[name] = r
    write_x(HERE / 'DRYRUN_R3_CHECKS.json', spec_bytes(res))
    print(json.dumps({k: {x: v.get(x) for x in ('verdict', 'exit_code', 'fs_table_matches_R3', 'binding_blockers', 'unexplained_refusals',
                                                 'refusals_beyond_pending_inputs')} | {'diff_vs_R2': v.get('fs_table_diff_vs_R2_dryrun', {}).get('columns')}
                      for k, v in res.items()}, indent=1))


# --------------------------------------------------------------------------- launch file
def launch():
    import shlex
    rec = json.loads((HERE / 'BUILD_R3_RECORD.json').read_text())
    dr = json.loads((HERE / 'DRYRUN_R3_CHECKS.json').read_text())
    pinned(MONITOR[0], MONITOR[1], 'monitor')
    for p in ('LAUNCH_R3.json', 'LAUNCH_R3.md', 'HASHES.txt'):
        if (HERE / p).exists():
            raise SystemExit('REFUSED: %s exists' % p)
    calls = []
    for name in ORDER:
        sp = rec['specs'][name]
        if dr[name]['verdict'] != 'PASS':
            raise SystemExit('REFUSED: dry-run of %s not PASS' % name)
        pinned(sp['path'], sp['sha256'], name)
        drv = DRV[sp['driver']]
        cap = CAPS[sp['driver']]
        od = RUNS / ('KMAX_A2F10_%s_D7R3_RUN_V001' % name)
        rc = Path(str(od) + '.receipt.json')
        argv = [PY, '-I', '-B', MONITOR[0], '--driver', drv[0], '--driver-sha256', drv[1], '--spec', sp['path'], '--outdir', str(od),
                '--receipt', str(rc), '--wall-cap-s', str(cap['wall_cap_s']), '--rss-cap-bytes', str(cap['rss_cap_bytes']),
                '--output-cap-bytes', str(cap['output_cap_bytes']), '--poll-s', str(cap['poll_s'])]
        calls.append({'case': name, 'driver': sp['driver'], 'driver_sha256': drv[1], 'spec': {'path': sp['path'], 'sha256': sp['sha256']},
                      'admits': sp['cube_outdir'], 'outdir': str(od), 'receipt': str(rc), 'caps': cap, 'argv': argv,
                      'shell': ' '.join(shlex.quote(a) for a in argv),
                      'outdir_state_now': {'dir_exists': od.exists(), 'receipt_exists': rc.exists(),
                                           'launch_file_exists': Path(str(rc) + '.launch.json').exists()}})
    if any(any(c['outdir_state_now'].values()) for c in calls):
        raise SystemExit('REFUSED: an R3 outdir/receipt already exists')
    L = {'schema': 'KMAX_D7_R3_LAUNCH_C2V005', 'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
         'R3': rec['R3_file'], 'prereg': {'path': str(PREREG[0]), 'sha256': PREREG[1]},
         'monitor': {'path': MONITOR[0], 'sha256': MONITOR[1]}, 'launched_by': 'root (this file launches nothing)',
         'calls': calls, 'templates_pending': {},
         'superseded_R2_runs': 'all R2 runs are superseded by R3 (C3R2/S3R2/Y3R2/RR2 stopped by root, %s; C2R2/S2R2/Y2R2 probes); '
                               'no R2 result enters the comparison' % STOPPED,
         'comparison_binding': {'C2': 'C2R3', 'S2': 'S2R3', 'Y2': 'Y2R3', 'C3': 'C3R3', 'S3': 'S3R3', 'Y3': 'Y3R3', 'R': 'RR3',
                                'C4': 'C4R3', 'S4': 'S4R3', 'Y4': 'Y4R3'},
         'comparison_flag': '--bracket-recovery %s' % rec['R3_file']['path']}
    lsha = write_x(HERE / 'LAUNCH_R3.json', spec_bytes(L))
    md = ['# KMAX D7 recovery R3 launch (prereg V005, Claude2 lane c2v005)', '',
          'R3 block: `%s` (sha256 %s). Launched by root; nothing here launches. Each outdir is absent now.' % (rec['R3_file']['path'], rec['R3_file']['sha256']), '',
          'Monitor `%s` (%s). Caps: v001 wall 21600 s, v005 wall 28800 s; rss 3221225472; output 17179869184; poll 2.0.' % MONITOR, '']
    for c in calls:
        md += ['## %s (driver %s, admits %s)' % (c['case'], c['driver'], Path(c['admits']).name), '',
               'spec `%s` sha256 %s' % (c['spec']['path'], c['spec']['sha256']), '', '```', c['shell'], '```', '']
    md += ['No pending templates (C4R3/S4R3/Y4R3 admit the C4 V005 prefix, re-derived from bytes).', '',
           'Comparison: kmax_compare_c2v005.py ... %s; case binding %s.' % (L['comparison_flag'], json.dumps(L['comparison_binding'])),
           '', 'LAUNCH_R3.json sha256 %s' % lsha, '']
    write_x(HERE / 'LAUNCH_R3.md', '\n'.join(md).encode())
    files = sorted(p for p in HERE.rglob('*') if p.is_file() and p.name != 'HASHES.txt' and 'check' not in p.relative_to(HERE).parts[:1])
    write_x(HERE / 'HASHES.txt', ''.join('%s  %s\n' % (sha_file(p), p.relative_to(HERE)) for p in files).encode())
    print(json.dumps({'launch_json_sha256': lsha, 'launch_md_sha256': sha_file(HERE / 'LAUNCH_R3.md'), 'hashes_txt_sha256': sha_file(HERE / 'HASHES.txt'),
                      'calls': [c['shell'] for c in calls]}, indent=1))


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) == 2 else None
    if cmd == 'build':
        build()
    elif cmd == 'dryrun':
        dryrun()
    elif cmd == 'launch':
        launch()
    else:
        print(__doc__)
        sys.exit(2)

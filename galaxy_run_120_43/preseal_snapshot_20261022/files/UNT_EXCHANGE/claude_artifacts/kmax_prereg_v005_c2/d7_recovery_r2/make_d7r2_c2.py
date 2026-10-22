"""D7 recovery R2 under sealed prereg V005 (Claude2 lane, c2v005): evidence, R2 block, R2 specs, dry-runs, launch file.

Applies amendment_v005.d7_recovery.later_invocations: R2 = R1 with only the newly missed fs entries widened by the
declared W1 rule (make_kmax_v005_c2.widen_W1, imported from the pinned builder bytes) from the failed calls' own
evidence (C3R / S3 / Y3 D7R1 runs, FAILED_AT_STAGE at fs_rotation).  Read scope on the failed D7R1 runs: launch.json,
monitor log, finish.json (status/reasons; bytes hashed), stage directory listings, column *_failure.json /
*_iterations.jsonl, *_fs_rotation/stderr.txt.  It never opens result.json, inputs/ or any rotation/speed array of
those runs.  Admission blocks are derived with the reviewed generator (admission_from_cube_out), which reads only the
admitted prefix (stages *_route_a/*_reference/*_body custody files and inputs/call_spec.json) of the cube outdir.
Writes only under this directory (exclusive create).  Launches nothing.

usage: python3 -I -B make_d7r2_c2.py build | dryrun | launch
"""
import copy
import glob
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/d7_recovery_r2')
V5 = HERE.parent
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
RUNS = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs')
BUILDER = (V5 / 'make_kmax_v005_c2.py', 'e2cddb1ed345709d795125655535ff69a24eb98959c67218e0eda8de3bdb49c6')
COMPARE = (V5 / 'kmax_compare_c2v005.py', '49404bc4b0d558c93113ed650802d9009f03be64c364f0d862213783389786f5')
PREREG = (V5 / 'KMAX_MATRIX_PREREG_V005.json', 'dbddc02c4d793b44a12136fc4fc88b20c001865ddd4c89b1b70c57bc406bb174')
R1F = (V5 / 'd7_recovery/KMAX_D7_RECOVERY_R1.json', 'b3938db22cc7758a40fe3559c5213873807646f1b01771c4b9fb685e71bec365')
R1EV = (V5 / 'd7_recovery/D7_EVIDENCE_S2_Y2_V001.json', 'f8f63d6b2bfde5c4c0457373bef57423135266941c9e1a1290bcd2fc5baed6fa')
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
S1 = V5 / 'specs_d7r1'
# failed D7R1 calls (driver v005): run, spec launched (sha = launch.json pin), expected missed columns (from the task)
FAILED = {'C3R': (RUNS / 'KMAX_A2F10_C3R_D7R1_V005_RUN_V001', S1 / 'filled/CALL_KMAX_C3R_A2F10_D7R1_C2V005.json',
                  'fa320e1a114e6e1ba3f94e07df6d633c995dfa40a101a6039e62fd38ba87802d', [3, 4, 46, 47, 48, 49]),
          'S3': (RUNS / 'KMAX_A2F10_S3_D7R1_V005_RUN_V001', S1 / 'filled/CALL_KMAX_S3_A2F10_D7R1_C2V005.json',
                 '74fdab5d49602fd0db3a610d94a9c1f3b9ab1f200f70a6479b0afb424dce9f79', [46, 47, 48, 49]),
          'Y3': (RUNS / 'KMAX_A2F10_Y3_D7R1_V005_RUN_V001', S1 / 'filled/CALL_KMAX_Y3_A2F10_D7R1_C2V005.json',
                 '47b196af8d9e7aaa257382a453195fee9d8712900338b1cf0f6531deb0b29a3b', [3, 4, 46, 47, 48, 49])}
# R2 specs: name -> (R1 counterpart, its sha, driver, admitted prefix, kind, R1 dry-run dir or None)
SPECS = {
    'C2R2': (S1 / 'CALL_KMAX_C2R_A2F10_D7R1_C2V005.json', '06743b2faf7094f9b09b8152ed91695f3fec21851e07f3c625e3ad72aa6cc485', 'v001', F10, 'filled', V5 / 'dryrun/C2R'),
    'S2R2': (S1 / 'CALL_KMAX_S2R_A2F10_D7R1_C2V005.json', '0b06ea067001e7744d80298a04a9cc9f14b9b63d0ce45d498450f506b7f68cc6', 'v001', F10, 'filled', V5 / 'dryrun/S2R'),
    'Y2R2': (S1 / 'CALL_KMAX_Y2R_A2F10_D7R1_C2V005.json', '37af4454e90a9a144f85b930be50b7e06113033694474a63ffaad13897c6256f', 'v001', F10, 'filled', V5 / 'dryrun/Y2R'),
    'C3R2': (S1 / 'filled/CALL_KMAX_C3R_A2F10_D7R1_C2V005.json', 'fa320e1a114e6e1ba3f94e07df6d633c995dfa40a101a6039e62fd38ba87802d', 'v005', C3V5, 'filled', V5 / 'dryrun_filled/C3R'),
    'S3R2': (S1 / 'filled/CALL_KMAX_S3_A2F10_D7R1_C2V005.json', '74fdab5d49602fd0db3a610d94a9c1f3b9ab1f200f70a6479b0afb424dce9f79', 'v005', C3V5, 'filled', V5 / 'dryrun_filled/S3'),
    'Y3R2': (S1 / 'filled/CALL_KMAX_Y3_A2F10_D7R1_C2V005.json', '47b196af8d9e7aaa257382a453195fee9d8712900338b1cf0f6531deb0b29a3b', 'v005', C3V5, 'filled', V5 / 'dryrun_filled/Y3'),
    'RR2': (S1 / 'templates/CALL_KMAX_RR_A2F10_D7R1_C2V005.TEMPLATE.json', '7b984554bf142436280d00df1a83fe005a63ddf62bfc2844bf4bbf268cf77c0f', 'v005', RV5, 'fill_from_template', None),
    'C4R2': (S1 / 'templates/CALL_KMAX_C4R_A2F10_D7R1_C2V005.TEMPLATE.json', '08ad05e2e8635bf801f8d18fb9bd23f7aef99f6db919f81df3adb8c5f13796f8', 'v005', C4V5, 'template', None),
    'S4R2': (S1 / 'templates/CALL_KMAX_S4_A2F10_D7R1_C2V005.TEMPLATE.json', 'e7759fce10a7d711ea2e436e121a14c834ae10dcce6269404929c987b1286214', 'v005', C4V5, 'template', None),
    'Y4R2': (S1 / 'templates/CALL_KMAX_Y4_A2F10_D7R1_C2V005.TEMPLATE.json', 'd079ed54e875fae038d7b2a759bd56622f262b72cf09e8a1dc067b600d375f88', 'v005', C4V5, 'template', None)}
FILLED = ('C2R2', 'S2R2', 'Y2R2', 'C3R2', 'S3R2', 'Y3R2', 'RR2')
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
    h_lo, h_hi = B.FS_TEMPLATE[0], 1.05 * B.FS_TEMPLATE[1]
    if r_lo > 0 and r_hi > 0:
        return 'A' if entry[0] > h_lo else 'B'
    if r_lo < 0 and r_hi < 0:
        return 'A' if entry[1] < h_hi else 'B'
    return None


# --------------------------------------------------------------------------- evidence (miss_evidence logic, read scope above)
def miss_evidence(cid, r1):
    outdir, spec_path, spec_sha, expected = FAILED[cid]
    spec = json.loads(pinned(spec_path, spec_sha, cid + ' spec'))
    launch_p = Path(str(outdir) + '.receipt.json.launch.json')
    launch_raw = launch_p.read_bytes()
    launch = json.loads(launch_raw)
    if launch['pins']['spec'] != {'path': str(spec_path), 'sha256': spec_sha} or launch['pins']['driver']['sha256'] != DRV['v005'][1]:
        raise SystemExit('REFUSED: %s launch pins differ from the R1 spec / driver v005' % cid)
    if canon(spec['numerics']['brackets']) != canon(r1):
        raise SystemExit('REFUSED: %s ran with a brackets block other than R1' % cid)
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
                     'entry_source': 'R1 fs_absolute_overrides[%d]' % idx if str(idx) in rule else 'fs template (no override key)',
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
                  'gate': 'V1 (ii) FAILED_AT_STAGE with a bracket miss in a column pass -> D7 recovery (later invocation R2)',
                  'missed_columns': cols}


def contains(outer, inner):
    return outer[0] <= inner[0] and inner[1] <= outer[1]


# --------------------------------------------------------------------------- build
def build():
    for p in ('D7_EVIDENCE_C3R_S3_Y3_V001.json', 'KMAX_D7_RECOVERY_R2.json', 'specs_d7r2', 'BUILD_R2_RECORD.json'):
        if (HERE / p).exists():
            raise SystemExit('REFUSED: %s exists' % p)
    pre = json.loads(pinned(*PREREG, 'prereg V005'))
    C = load_mod(*COMPARE, 'kmax_compare_c2v005')
    gen = B.load_gen()
    r1rec = json.loads(pinned(*R1F, 'R1'))
    pinned(*R1EV, 'R1 evidence')
    r1 = r1rec['brackets']
    d7 = pre['amendment_v005']['d7_recovery']
    if canon(r1) != canon(d7['R1']['brackets']) or d7['fs_template_bracket'] != B.FS_TEMPLATE:
        raise SystemExit('REFUSED: R1 file differs from prereg R1 or template differs')
    anc = pre['anchor']['brackets']

    # ---- 1. evidence
    specs, evid = {}, {}
    for cid in ('C3R', 'S3', 'Y3'):
        specs[cid], evid[cid] = miss_evidence(cid, r1)
    ev_sha = write_x(HERE / 'D7_EVIDENCE_C3R_S3_Y3_V001.json', spec_bytes(evid))

    # ---- 2. W1 -> R2
    r1_fs = r1['rule']['fs_absolute_overrides']
    r1_widened = set(r1rec['widened_entries'])
    proposals = {}
    for cid in ('C3R', 'S3', 'Y3'):
        for c in evid[cid]['missed_columns']:
            proposals.setdefault(str(c['index']), []).append({'case': cid, 'from': c['entry_in_failed_call'], 'to': c['W1']['new_entry'],
                                                              'step': c['W1']['declared_step'], 'why': c['W1']['step']})
    widened, conflicts = {}, []
    for k, props in proposals.items():
        if len({canon(p['from']) for p in props}) != 1:
            raise SystemExit('BLOCKED: column %s entry differs across the failed calls (all ran R1)' % k)
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
    r1_widened_remissed = sorted((k for k in widened if k in r1_widened), key=int)
    if r1_widened_remissed:   # all R1 widenings were step A; a re-miss would take W1 step B -- not built here, reported for root
        raise SystemExit('BLOCKED: R1-widened entries %s missed again; report for root' % r1_widened_remissed)
    hull = [B.FS_TEMPLATE[0], 1.05 * B.FS_TEMPLATE[1]]
    if widened != {k: hull for k in ('3', '4', '46', '47', '48', '49')}:   # the reason text below states these values
        raise SystemExit('REFUSED: W1 results %s differ from the stated R2 reason; rewrite the reason' % widened)
    r2 = copy.deepcopy(r1)
    fs = dict(r2['rule']['fs_absolute_overrides'])
    for k, v in widened.items():
        fs[k] = v
    r2['rule']['fs_absolute_overrides'] = {k: fs[k] for k in sorted(fs)}
    new_keys = sorted(widened, key=int)
    we = {}
    for k in sorted(set(r1rec['widened_entries']) | set(widened), key=int):
        if k in widened:
            p0 = proposals[k][0]
            we[k] = {'invocation': 'R2', 'from_R1': r1_fs.get(k, B.FS_TEMPLATE),
                     'from_source': 'R1 entry' if k in r1_fs else 'fs template (no override key in R1)', 'to': widened[k],
                     'W1_step': sorted({p['step'] for p in proposals[k]}), 'W1_branch': p0['why'].split(':')[0],
                     'evidenced_by': [p['case'] for p in proposals[k]]}
        else:
            we[k] = dict(r1rec['widened_entries'][k], invocation='R1')
    r2_rec = {'brackets': r2,
              'reason': 'D7 recovery R2 (prereg V005 amendment_v005.d7_recovery.later_invocations): R2 = R1 with only the newly missed fs entries '
                        'widened by W1 from the failed D7R1 calls\' own evidence. C3R (KMAX_A2F10_C3R_D7R1_V005_RUN_V001: columns 3,4,46,47,48,49), '
                        'S3 (KMAX_A2F10_S3_D7R1_V005_RUN_V001: 46,47,48,49), Y3 (KMAX_A2F10_Y3_D7R1_V005_RUN_V001: 3,4,46,47,48,49) failed '
                        'MASS_ENTHALPY_NOT_BRACKETED. Columns 3,4 (template [1.5125e8, 3.025e8], no override): r < 0 at both ends (root above hi), '
                        'W1 step A moves hi to 1.05*template_hi = 3.17625e8. Columns 46-49 (R1 entry [3.025e8, 3.17625e8], inherited from the anchor, '
                        'not widened in R1): r > 0 at both ends (root below lo), W1 step A moves lo to template_lo = 1.5125e8. All cases agree per column '
                        '(no conflict). R1 entries 5,6,7,8,9,45,50 unchanged. No other key changes.',
              'invocation': 'R2',
              'widened_entries': we,
              'evidence': {'R1_recovery_file': {'path': str(R1F[0]), 'sha256': R1F[1]}, 'R1_evidence_file': {'path': str(R1EV[0]), 'sha256': R1EV[1]},
                           'R2_evidence_file': {'path': str(HERE / 'D7_EVIDENCE_C3R_S3_Y3_V001.json'), 'sha256': ev_sha},
                           **{cid: [{'index': c['index'], 'failure_file': c['failure_file'], 'iterations_file': c['iterations_file'],
                                     'evidence': c['evidence']} for c in evid[cid]['missed_columns']] for cid in ('C3R', 'S3', 'Y3')}}}
    # sealed compare script: file-schema check of its main() and its validator, unchanged
    if not ({'brackets', 'reason'} <= set(r2_rec) <= {'brackets', 'reason', 'invocation', 'widened_entries', 'evidence'}) \
            or not isinstance(r2_rec.get('brackets'), dict) or r2_rec['brackets'].get('mode') != 'rule':
        raise SystemExit('REFUSED: R2 file schema')
    why = C.validate_recovery(pre, r2_rec['brackets'])
    if why:
        raise SystemExit('REFUSED: sealed validator rejects R2: %s' % why)
    # liveness of the validator: two tampered copies must be refused
    t1 = copy.deepcopy(r2)
    t1['rule']['fs_absolute_overrides']['5'] = anc['rule']['fs_absolute_overrides']['5']
    t2 = copy.deepcopy(r2)
    t2['rule']['fs_absolute_overrides']['3'] = [1.6e8, 3.17625e8]
    live = {'R1_entry_5_undone': C.validate_recovery(pre, t1), 'new_entry_3_not_containing_template': C.validate_recovery(pre, t2)}
    if not all(live.values()):
        raise SystemExit('REFUSED: validator liveness')
    # explicit checks
    own = {'contains_R1': all(contains(r2['rule'][key][i], e) for key in ('fs_absolute_overrides', 'rfs_factor_overrides') for i, e in r1['rule'][key].items()),
           'only_override_entries_change': sorted(k for k in set(r1['rule']) | set(r2['rule']) if canon(r1['rule'].get(k)) != canon(r2['rule'].get(k))) == ['fs_absolute_overrides'],
           'changed_fs_entries_vs_R1': sorted((k for k in r2['rule']['fs_absolute_overrides'] if r2['rule']['fs_absolute_overrides'][k] != r1_fs.get(k)), key=int),
           'new_keys_vs_R1': sorted((k for k in r2['rule']['fs_absolute_overrides'] if k not in r1_fs), key=int),
           'new_entries_contain_template': all(contains(r2['rule']['fs_absolute_overrides'][k], B.FS_TEMPLATE) for k in r2['rule']['fs_absolute_overrides'] if k not in anc['rule']['fs_absolute_overrides']),
           'nothing_narrowed_vs_R1': all(contains(r2['rule']['fs_absolute_overrides'][k], v) for k, v in r1_fs.items()),
           'nothing_narrowed_vs_anchor': all(contains(r2['rule']['fs_absolute_overrides'][k], v) for k, v in anc['rule']['fs_absolute_overrides'].items()),
           'other_rule_keys_equal_R1': all(canon(r1['rule'][k]) == canon(r2['rule'][k]) for k in r1['rule'] if k != 'fs_absolute_overrides'),
           'override_key_lint': lint_override_keys(r2)}
    if not (own['contains_R1'] and own['only_override_entries_change'] and own['changed_fs_entries_vs_R1'] == new_keys
            and own['new_entries_contain_template'] and own['nothing_narrowed_vs_R1'] and own['nothing_narrowed_vs_anchor']
            and own['other_rule_keys_equal_R1'] and not own['override_key_lint']):
        raise SystemExit('REFUSED: own R2 checks %s' % own)
    r2_sha = write_x(HERE / 'KMAX_D7_RECOVERY_R2.json', spec_bytes(r2_rec))

    # ---- 3. specs on R2
    adm = {F10: gen.admission_from_cube_out(str(F10)), C3V5: gen.admission_from_cube_out(str(C3V5)), RV5: gen.admission_from_cube_out(str(RV5))}
    note = (' | brackets = D7 recovery R2 block %s (prereg V005 d7_recovery.later_invocations; fs_absolute_overrides %s widened by W1 '
            'from the C3R/S3/Y3 D7R1 failures)' % (r2_sha[:16], ','.join(new_keys)))
    out = {}
    expect_br = sorted('/numerics/brackets/rule/fs_absolute_overrides/%s' % k for k in new_keys)
    for name, (src, ssha, drv, cube, kind, _dr) in SPECS.items():
        s1 = json.loads(pinned(src, ssha, name + ' R1 counterpart'))
        if canon(s1['numerics']['brackets']) != canon(r1):
            raise SystemExit('REFUSED: %s R1 counterpart brackets are not R1' % name)
        s = copy.deepcopy(s1)
        s['numerics']['brackets'] = copy.deepcopy(r2)
        s['label'] = s1['label'] + note
        rec = {'r1_counterpart': {'path': str(src), 'sha256': ssha}, 'driver': drv, 'cube_outdir': str(cube), 'kind': kind}
        if kind == 'filled':
            if canon(s['admit']) != canon(adm[cube][0]):
                raise SystemExit('REFUSED: %s admit is not the %s prefix re-derived from bytes' % (name, cube.name))
            rec['admit_rederived_equal'] = True
        elif kind == 'fill_from_template':   # = make_kmax_v005_c2.fill() with R2 in place of R1
            admit, cspec = adm[cube]
            for k in ('physical', 'coefficients'):
                if cspec[k] != s[k]:
                    raise SystemExit('REFUSED: cube %s differs from template' % k)
            if cspec['numerics']['composite_grid_spec'] != s['numerics']['composite_grid_spec'] or cspec['numerics']['truncation'] != {'shape': 'cube'}:
                raise SystemExit('REFUSED: cube grid/truncation differ from template')
            if canon(cspec['numerics']['brackets']) not in (canon(anc), canon(r1), canon(r2)):
                raise SystemExit('REFUSED: cube brackets are neither the anchor block, R1 nor R2')
            if 'PENDING' not in json.dumps(s['admit']):
                raise SystemExit('REFUSED: template admit is not PENDING')
            s['admit'] = admit
            s['label'] = s['label'].replace(' TEMPLATE', '') + '; admits %s' % cube
            rec['cube_call_spec_brackets'] = 'anchor' if canon(cspec['numerics']['brackets']) == canon(anc) else 'R1/R2'
        else:
            if 'PENDING' not in json.dumps(s['admit']) or canon(s['admit']) != canon(s1['admit']):
                raise SystemExit('REFUSED: %s template admit not PENDING/unchanged' % name)
        d = leaf_diff(s1, s)
        exp = sorted(['/label'] + expect_br)
        dd = [x for x in d if not x.startswith('/admit/')] if kind == 'fill_from_template' else d
        if dd != exp:
            raise SystemExit('REFUSED: %s differs from its R1 counterpart beyond label + R2 entries: %s' % (name, d))
        lint = lint_override_keys(s)
        if lint:
            raise SystemExit('REFUSED: %s override key lint %s' % (name, lint))
        fn = 'CALL_KMAX_%s_A2F10_D7R2_C2V005%s.json' % (name, '.TEMPLATE' if kind == 'template' else '')
        p = HERE / 'specs_d7r2' / ('templates' if kind == 'template' else '') / fn
        rec.update({'path': str(p), 'sha256': write_x(p, spec_bytes(s)), 'leaf_diff_vs_R1_counterpart': d, 'override_key_lint': 'PASS',
                    'picard_passes': s['numerics']['picard']['passes'], 'admit_pending': 'PENDING' in json.dumps(s['admit'])})
        out[name] = rec
    record = {'schema': 'KMAX_D7_R2_BUILD_RECORD_C2V005', 'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
              'inputs': {'prereg': {'path': str(PREREG[0]), 'sha256': PREREG[1]}, 'compare': {'path': str(COMPARE[0]), 'sha256': COMPARE[1]},
                         'builder': {'path': str(BUILDER[0]), 'sha256': BUILDER[1]}, 'R1': {'path': str(R1F[0]), 'sha256': R1F[1]}},
              'evidence_file': {'path': str(HERE / 'D7_EVIDENCE_C3R_S3_Y3_V001.json'), 'sha256': ev_sha},
              'R2_file': {'path': str(HERE / 'KMAX_D7_RECOVERY_R2.json'), 'sha256': r2_sha},
              'W1_proposals': proposals, 'conflicts': conflicts, 'R1_widened_entries_missed_again': r1_widened_remissed,
              'validator': {'function': 'kmax_compare_c2v005.validate_recovery (sealed 49404bc4) + main() file-schema check', 'reasons': why,
                            'accepted': not why, 'liveness_tampered_copies_refused': live}, 'own_checks': own,
              'admissions_rederived': {str(k): v[0] for k, v in adm.items()}, 'specs': out}
    write_x(HERE / 'BUILD_R2_RECORD.json', spec_bytes(record))
    print(json.dumps({'evidence_sha256': ev_sha, 'r2_sha256': r2_sha, 'new_or_changed': {k: widened[k] for k in new_keys}, 'conflicts': conflicts,
                      'validator_reasons': why, 'specs': {k: v['sha256'] for k, v in out.items()}}, indent=1))


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


def dryrun():
    rec = json.loads((HERE / 'BUILD_R2_RECORD.json').read_text())
    r2 = json.loads(pinned(rec['R2_file']['path'], rec['R2_file']['sha256'], 'R2'))['brackets']
    r2fs = r2['rule']['fs_absolute_overrides']
    new_keys = rec['own_checks']['changed_fs_entries_vs_R1']
    res = {}
    for name in FILLED:
        sp = rec['specs'][name]
        pinned(sp['path'], sp['sha256'], name)
        drv = DRV[sp['driver']]
        pinned(drv[0], drv[1], 'driver ' + sp['driver'])
        rd = HERE / 'dryrun_r2' / name
        if rd.exists():
            raise SystemExit('REFUSED: %s exists' % rd)
        rd.parent.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        pr = subprocess.run(['nice', '-n', '10', PY, '-I', '-B', drv[0], 'dry-run', '--spec', sp['path'], '--report-dir', str(rd)],
                            capture_output=True, text=True)
        write_x(HERE / 'dryrun_r2' / (name + '.stdout.txt'), pr.stdout.encode())
        write_x(HERE / 'dryrun_r2' / (name + '.stderr.txt'), pr.stderr.encode())
        r = {'exit_code': pr.returncode, 'seconds': round(time.time() - t0, 2)}
        if pr.returncode == 0:
            rep = json.loads((rd / 'DRYRUN_REPORT.json').read_text())
            sm = rep['summary']
            tab = fs_table(rd)
            n = sm['bracket_rule_checks']['fs']['n']
            r.update({'call_spec_sha256_ok': rep['call_spec_sha256'] == sp['sha256'], 'driver_sha256_ok': rep['driver_sha256'] == drv[1],
                      'stages_planned': sm['stages_planned'], 'pin_problems': sm['pin_problems'], 'scipy_imports': sm['scipy_imports'],
                      'binding_blockers': sm.get('binding_blockers', 'n/a (v001 report has no field)'),
                      'unexplained_refusals': sm.get('unexplained_refusals', 'n/a (v001 report has no field)'),
                      'refusals_beyond_pending_inputs': sm.get('refusals_beyond_pending_inputs', 'n/a (v001 report has no field)'),
                      'stage_admission_refused': sm.get('stage_admission_refused', 'n/a'),
                      'remaining_refusals_by_class': sm.get('remaining_refusals_by_class', 'n/a'),
                      'fs_columns_covered': sorted(map(int, tab)) == list(range(n)), 'fs_n': n,
                      'fs_table_matches_R2': all(tab[k] == (r2fs[k] if k in r2fs else B.FS_TEMPLATE) for k in tab)})
            r1d = SPECS[name][5]
            if r1d is not None:
                t1 = fs_table(r1d)
                diffc = sorted((k for k in set(t1) | set(tab) if t1.get(k) != tab.get(k)), key=int)
                r['fs_table_diff_vs_R1_dryrun'] = {'r1_dryrun': str(r1d), 'columns': diffc, 'equals_R2_changed_entries': diffc == new_keys}
            ok = (r['call_spec_sha256_ok'] and r['driver_sha256_ok'] and not r['pin_problems'] and not r['scipy_imports']
                  and r['fs_columns_covered'] and r['fs_table_matches_R2']
                  and (r1d is None or r['fs_table_diff_vs_R1_dryrun']['equals_R2_changed_entries']))
            if sp['driver'] == 'v005':
                ok = ok and r['binding_blockers'] == [] and r['unexplained_refusals'] == [] and r['refusals_beyond_pending_inputs'] == [] \
                     and r['stage_admission_refused'] == [] and (rep.get('binding_blockers') in ([], None))
            r['verdict'] = 'PASS' if ok else 'FAIL'
        else:
            r['verdict'] = 'FAIL'
        res[name] = r
    write_x(HERE / 'DRYRUN_R2_CHECKS.json', spec_bytes(res))
    print(json.dumps(res, indent=1))


# --------------------------------------------------------------------------- launch file
def launch():
    import shlex
    rec = json.loads((HERE / 'BUILD_R2_RECORD.json').read_text())
    dr = json.loads((HERE / 'DRYRUN_R2_CHECKS.json').read_text())
    pinned(MONITOR[0], MONITOR[1], 'monitor')
    calls = []
    for name in FILLED:
        sp = rec['specs'][name]
        if dr[name]['verdict'] != 'PASS':
            raise SystemExit('REFUSED: dry-run of %s not PASS' % name)
        pinned(sp['path'], sp['sha256'], name)
        drv = DRV[sp['driver']]
        cap = CAPS[sp['driver']]
        od = RUNS / ('KMAX_A2F10_%s_D7R2_RUN_V001' % name)
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
        raise SystemExit('REFUSED: an R2 outdir/receipt already exists')
    pend = {n: {'path': rec['specs'][n]['path'], 'sha256': rec['specs'][n]['sha256'], 'cube_outdir': rec['specs'][n]['cube_outdir'],
                'status': 'PENDING: fill admit from the C4 V005 prefix once stages 01-03 exist, then dry-run under v005 before launch'}
            for n in ('C4R2', 'S4R2', 'Y4R2')}
    L = {'schema': 'KMAX_D7_R2_LAUNCH_C2V005', 'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
         'R2': rec['R2_file'], 'prereg': {'path': str(PREREG[0]), 'sha256': PREREG[1]},
         'monitor': {'path': MONITOR[0], 'sha256': MONITOR[1]}, 'launched_by': 'root (this file launches nothing)',
         'calls': calls, 'templates_pending': pend,
         'comparison_binding': {'C2': 'C2R2', 'S2': 'S2R2', 'Y2': 'Y2R2', 'C3': 'C3R2', 'S3': 'S3R2', 'Y3': 'Y3R2', 'R': 'RR2',
                                'C4': 'C4R2', 'S4': 'S4R2', 'Y4': 'Y4R2'},
         'comparison_flag': '--bracket-recovery %s' % rec['R2_file']['path']}
    lsha = write_x(HERE / 'LAUNCH_R2.json', spec_bytes(L))
    md = ['# KMAX D7 recovery R2 launch (prereg V005, Claude2 lane c2v005)', '',
          'R2 block: `%s` (sha256 %s). Launched by root; nothing here launches. Each outdir is absent now.' % (rec['R2_file']['path'], rec['R2_file']['sha256']), '',
          'Monitor `%s` (%s). Caps: v001 wall 21600 s, v005 wall 28800 s; rss 3221225472; output 17179869184; poll 2.0.' % MONITOR, '']
    for c in calls:
        md += ['## %s (driver %s, admits %s)' % (c['case'], c['driver'], Path(c['admits']).name), '',
               'spec `%s` sha256 %s' % (c['spec']['path'], c['spec']['sha256']), '', '```', c['shell'], '```', '']
    md += ['## Pending templates (not launchable yet)', '']
    for n, p in pend.items():
        md += ['- %s: `%s` sha256 %s; %s' % (n, p['path'], p['sha256'], p['status'])]
    md += ['', 'Comparison: kmax_compare_c2v005.py ... %s; case binding %s.' % (L['comparison_flag'], json.dumps(L['comparison_binding'])),
           '', 'LAUNCH_R2.json sha256 %s' % lsha, '']
    write_x(HERE / 'LAUNCH_R2.md', '\n'.join(md).encode())
    files = sorted(p for p in HERE.rglob('*') if p.is_file() and p.name != 'HASHES.txt')
    write_x(HERE / 'HASHES.txt', ''.join('%s  %s\n' % (sha_file(p), p.relative_to(HERE)) for p in files).encode())
    print(json.dumps({'launch_json_sha256': lsha, 'calls': [c['shell'] for c in calls]}, indent=1))


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

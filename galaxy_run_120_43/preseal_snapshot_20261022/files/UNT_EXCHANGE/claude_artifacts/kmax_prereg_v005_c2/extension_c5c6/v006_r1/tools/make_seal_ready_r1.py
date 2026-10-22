"""Write v006_r1/SEAL_READY_V006_R1.json: what a SEAL_RECORD_V006_R1 would pin, and the seal preconditions evaluated from bytes
and the filesystem at write time:
  (i)  no C5/C6 outdir (or receipt) exists: every registered C5/C6 outdir and receipt (N8 and N1, External1 real path and the
       CLAUDE2/runs_ext symlink) is absent, and no entry naming C5/C6 is under CLAUDE2/runs or runs_ext;
  (ii) the separate review record extension_c5c6/check/REVIEW_V009_PREP_V009_V001.json is present, by a reviewer distinct from
       this lane (Claude4), with an accepted verdict and the pinned driver/prep shas (V006 R1 binding_inputs.v009_admissibility).
Writes nothing else.  usage: python3 -I -B make_seal_ready_r1.py"""
import hashlib
import json
import os
import time
from pathlib import Path

LANE = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/extension_c5c6')
OUT = LANE / 'v006_r1'
CL2 = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2')
EXT1 = '/Volumes/External1/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs_ext'
LINK = str(CL2 / 'runs_ext')


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def pin(p):
    return {'path': str(p), 'sha256': sha(p)}


def main():
    pre_p = OUT / 'prereg/KMAX_MATRIX_PREREG_V006_R1.json'
    cmp_p = OUT / 'prereg/kmax_compare_ext_c2v006_r1.py'
    pre = json.loads(pre_p.read_text())
    psha = sha(pre_p)
    pinned = "PREREG_SHA256 = '%s'" % psha in cmp_p.read_text()
    tests = sorted((OUT / 'prereg').glob('test_runs_V*/TESTS_RESULT.json'))[-1]
    tj = json.loads(tests.read_text())
    dry = OUT / 'dryrun/DRYRUN_R1_SUMMARY_V002.json'
    dj = json.loads(dry.read_text())
    launch = OUT / 'LAUNCH_EXT_V002.json'
    lj = json.loads(launch.read_text())
    # (i)
    paths = []
    for c in pre['cases']:
        for v in (c.get('outdirs') or {}).values():
            if isinstance(v, dict):
                for k in ('outdir', 'receipt'):
                    paths += [v[k], v[k].replace(EXT1, LINK), v[k] + '.launch.json' if k == 'receipt' else v[k]]
    paths = sorted(set(paths))
    exist = [p for p in paths if os.path.lexists(p)]
    named = []
    for root in (CL2 / 'runs', Path(LINK), Path(EXT1)):
        if root.is_dir():
            named += ['%s/%s' % (root, n) for n in os.listdir(root) if 'C5' in n or 'C6' in n]
    pre_i = {'holds': not exist and not named, 'registered_paths_checked': paths, 'existing': exist, 'entries_naming_C5_or_C6': sorted(named)}
    # (ii)
    adm = pre['binding_inputs']['v009_admissibility']
    rp = Path(adm['review']['path'])
    pre_ii = {'path': str(rp), 'required': {'distinct_reviewer': 'Claude4 (not this lane)', 'verdict_in': adm['review']['accepted_verdicts'],
                                             'driver_sha256': adm['driver_sha256'], 'prep_sha256': adm['prep_sha256']}}
    if rp.is_file():
        try:
            r = json.loads(rp.read_text())
        except Exception as exc:
            r = None
            pre_ii['error'] = 'unreadable: %s' % exc
        pre_ii['present'] = True
        pre_ii['sha256'] = sha(rp)
        if r is not None:
            pre_ii['fields'] = {k: r.get(k) for k in ('verdict', 'driver_sha256', 'prep_sha256', 'reviewer', 'reviewed_by', 'author')}
            pre_ii['holds'] = bool(r.get('verdict') in adm['review']['accepted_verdicts'] and r.get('driver_sha256') == adm['driver_sha256']
                                   and r.get('prep_sha256') == adm['prep_sha256'])
            pre_ii['distinct_reviewer_note'] = 'reviewer identity is read from the record fields above; the sealing root confirms it is Claude4'
        else:
            pre_ii['holds'] = False
    else:
        pre_ii['present'] = False
        pre_ii['holds'] = False
        pre_ii['state'] = 'PENDING: the record does not exist yet (written by the separate review, Claude4)'
    rec = {'schema': 'KMAX_PREREG_V006_R1_SEAL_READY', 'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
           'prereg': {'path': str(pre_p), 'sha256': psha, 'status': pre['status'][:40]},
           'compare': {'path': str(cmp_p), 'sha256': sha(cmp_p), 'pins_prereg_sha256': psha if pinned else None},
           'tests': {'path': str(tests), 'sha256': sha(tests), 'n': tj['n'], 'n_pass': tj['n_pass']},
           'test_script': pin(OUT / 'prereg/tests_kmax_compare_ext_c2v006_r1.py'),
           'specs': {k: {'path': c['specs'][v]['path'], 'sha256': c['specs'][v]['sha256']} for c in pre['cases'] if c['id'] in ('C5', 'C6')
                     for k, v in (('%s_N8' % c['id'], 'primary_N8'), ('%s_N1' % c['id'], 'alternate_N1'))},
           'dryrun': {'path': str(dry), 'sha256': sha(dry), 'n_jobs': dj['n_jobs'], 'n_as_expected': dj['n_as_expected'],
                      'driver_sha256': '999331afd604dd9829aa8f389f43cdb87603d03412d52ba09712226787f18db6'},
           'launch': {'path': str(launch), 'sha256': sha(launch), 'json_pins_prereg': lj['pins']['prereg_v006_r1']['sha256'] == psha,
                      'json_pins_compare': lj['pins']['compare_v006_r1']['sha256'] == sha(cmp_p),
                      'commands': pin(OUT / 'LAUNCH_EXT_V002.commands.txt')},
           'check_applied': pre['revision_r1']['check'],
           'supersedes_draft': pre['supersedes_draft'],
           'decision_file_pins': ('none: V006 R1 pins no root decision addendum (the open V004 addendum is not pinned and is cited by '
                                  'name only; the frozen V002 17c26616 / V003 5bef6552 addenda are not inputs of this prereg)'),
           'seal_preconditions': {'i_no_C5_C6_outdir_exists': pre_i, 'ii_review_v009_present': pre_ii},
           'ready_to_seal': bool(pre_i['holds'] and pre_ii['holds'] and pinned and tj['n'] == tj['n_pass'] and dj['all_as_expected']),
           'seal_act': ('root writes SEAL_RECORD_V006_R1.json (prereg + compare path/sha, the 4 spec shas, LAUNCH_EXT_V002 sha, the review '
                        'record sha) after re-evaluating (i) and (ii) at seal time; launches follow LAUNCH_EXT_V002 only after the seal')}
    with open(OUT / 'SEAL_READY_V006_R1.json', 'x') as f:
        json.dump(rec, f, indent=1)
        f.write('\n')
    print(json.dumps({'ready_to_seal': rec['ready_to_seal'], 'i': pre_i['holds'], 'ii': pre_ii['holds'], 'ii_present': pre_ii['present'],
                      'tests': '%d/%d' % (tj['n_pass'], tj['n']), 'dry': '%d/%d' % (dj['n_as_expected'], dj['n_jobs']), 'compare_pins': pinned}))


if __name__ == '__main__':
    main()

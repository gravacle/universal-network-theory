"""Checker K4: D7 recovery against the V002 D7 text, from bytes.
 (1) missed columns and evidence re-derived from every *_failure.json / *_iterations.jsonl of the failed S2/Y2 calls;
     W1 applied independently; R1 block, recovery file and prereg R1 compared.
 (2) corrected base spec vs anchor base spec (leaf diff).
 (3)/(4) every author spec/template vs the reviewed generator's templates regenerated with --base-spec <corrected base>
     (check/regen_templates_d7r1), excluding label and admit; admits checked separately.
 F3: stopped-run facts from route-A progress logs / mtimes; process table (read-only ps).
 Seal precondition: existence only of result.json/finish.json under every V005/D7R1 outdir (never opened).
"""
import glob
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANE = HERE.parent
RUNS = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs')
V002 = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v002_c2/KMAX_MATRIX_PREREG_V002.json')
PRE = json.loads((LANE / 'KMAX_MATRIX_PREREG_V005.json').read_text())
D7 = PRE['amendment_v005']['d7_recovery']
canon = lambda o: json.dumps(o, sort_keys=True, separators=(',', ':'))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def leaves(o, p=''):
    if isinstance(o, dict):
        r = {}
        for k, v in o.items():
            r.update(leaves(v, p + '/' + str(k)))
        return r or {p: {}}
    if isinstance(o, list):
        r = {}
        for i, v in enumerate(o):
            r.update(leaves(v, p + '[%d]' % i))
        return r or {p: []}
    return {p: o}


def ldiff(a, b):
    la, lb = leaves(a), leaves(b)
    return sorted(k for k in set(la) | set(lb) if la.get(k, '<absent>') != lb.get(k, '<absent>'))


out = {}
# ---- V002 D7 text equals V005 P6 declared_recovery
v2 = json.loads(V002.read_text())
out['d7_text_V002_equals_V005'] = v2['criterion']['bracket_precondition_P6']['declared_recovery'] == PRE['criterion']['bracket_precondition_P6']['declared_recovery']

# ---- (1) evidence from bytes
anchor_fs = PRE['anchor']['brackets']['rule']['fs_absolute_overrides']
tmpl = D7['fs_template_bracket']
ctrl = json.loads(Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/DDO154_REMAINING_FREE_SURFACE_CONTROLS_V001.json').read_text())
out['fs_template_equals_solver_template'] = ctrl['solver']['enthalpy_bracket'] == tmpl
miss = {}
for cid, run in (('S2', 'KMAX_A2F10_S2_RUN_V001'), ('Y2', 'KMAX_A2F10_Y2_RUN_V001')):
    rd = RUNS / run
    allfail = sorted(str(Path(f).relative_to(rd)) for f in glob.glob(str(rd / 'stages/**/*failure*.json'), recursive=True))
    cols = []
    for f in sorted(glob.glob(str(rd / 'stages/*_columns_*/columns/column_*_failure.json'))):
        fl = json.loads(Path(f).read_text())
        it = [json.loads(x) for x in Path(f.replace('_failure.json', '_iterations.jsonl')).read_text().splitlines() if x.strip()]
        i = str(fl['index'])
        entry = anchor_fs.get(i, tmpl)
        r_lo, r_hi = it[0]['mass_relative_residual'], it[-1]['mass_relative_residual']
        # my own W1 reading
        if r_lo > 0 and r_hi > 0:
            new = [tmpl[0] if entry[0] > tmpl[0] else entry[0] / 2, entry[1]]
        elif r_lo < 0 and r_hi < 0:
            new = [entry[0], 1.05 * tmpl[1] if entry[1] < 1.05 * tmpl[1] else 2 * entry[1]]
        else:
            new = None
        cols.append({'index': i, 'stage': Path(f).parts[-3], 'message': fl['message'], 'n_evals': len(it),
                     'evaluated_Hc': [x['Hc_m2_s2'] for x in it], 'entry': entry, 'evaluated_at_entry_ends': [x['Hc_m2_s2'] for x in it] == entry,
                     'r_lo': r_lo, 'r_hi': r_hi, 'W1_new': new, 'failure_sha256': sha(f)})
    spec = json.loads((rd / 'inputs/call_spec.json').read_text())
    miss[cid] = {'all_failure_files': allfail, 'columns': cols,
                 'ran_with_anchor_block': canon(spec['numerics']['brackets']) == canon(PRE['anchor']['brackets']),
                 'stderr_last': (rd / 'stages/06_fs_rotation/stderr.txt').read_text().strip().splitlines()[-1]}
out['missed'] = miss
mine = json.loads(json.dumps(PRE['anchor']['brackets']))
for cid in miss:
    for c in miss[cid]['columns']:
        mine['rule']['fs_absolute_overrides'][c['index']] = c['W1_new']
rec = json.loads((LANE / 'd7_recovery/KMAX_D7_RECOVERY_R1.json').read_text())
ev = json.loads((LANE / 'd7_recovery/D7_EVIDENCE_S2_Y2_V001.json').read_text())
out['R1_equals_my_W1_block'] = canon(mine) == canon(rec['brackets']) == canon(D7['R1']['brackets'])
out['R1_changed_entries_vs_anchor'] = sorted((k for k in rec['brackets']['rule']['fs_absolute_overrides'] if rec['brackets']['rule']['fs_absolute_overrides'][k] != anchor_fs.get(k)), key=int)
out['R1_other_keys_equal_anchor'] = all(canon(rec['brackets']['rule'][k]) == canon(PRE['anchor']['brackets']['rule'][k]) for k in rec['brackets']['rule'] if k != 'fs_absolute_overrides')
out['evidence_file_hashes_match_bytes'] = all(sha(c['failure_file']['path']) == c['failure_file']['sha256'] and sha(c['iterations_file']['path']) == c['iterations_file']['sha256']
                                              for cid in ev for c in ev[cid]['missed_columns'])
out['missed_union'] = sorted({c['index'] for cid in miss for c in miss[cid]['columns']}, key=int)
out['prereg_missed_lists'] = {cid: D7['registered_first_attempts'][cid]['missed_columns'] for cid in ('S2', 'Y2')}

# ---- (2) corrected base vs anchor base
base = json.loads(Path(PRE['anchor']['base_spec']['path']).read_text())
cb = json.loads((LANE / 'd7_recovery/CALL_A2_ANCHOR_F10_D7R1_BASE_C2V005.json').read_text())
out['anchor_base_sha_ok'] = sha(PRE['anchor']['base_spec']['path']) == PRE['anchor']['base_spec']['sha256']
out['corrected_base_leaf_diff'] = ldiff(base, cb)

# ---- (3)/(4) specs/templates vs regenerated-from-corrected-base templates
RG = HERE / 'regen_templates_d7r1'
author = {'S2': LANE / 'specs_d7r1/CALL_KMAX_S2R_A2F10_D7R1_C2V005.json', 'Y2': LANE / 'specs_d7r1/CALL_KMAX_Y2R_A2F10_D7R1_C2V005.json',
          'C2': LANE / 'specs_d7r1/CALL_KMAX_C2R_A2F10_D7R1_C2V005.json'}
for cid in ('C3', 'C4', 'R'):
    author[cid] = LANE / ('specs_d7r1/templates/CALL_KMAX_%sR_A2F10_D7R1_C2V005.TEMPLATE.json' % cid)
for cid in ('S3', 'Y3', 'S4', 'Y4'):
    author[cid] = LANE / ('specs_d7r1/templates/CALL_KMAX_%s_A2F10_D7R1_C2V005.TEMPLATE.json' % cid)
regen = {}
for cid, p in author.items():
    a = json.loads(p.read_text())
    g = json.loads((RG / ('CALL_KMAX_%s_C2V001.TEMPLATE.json' % cid)).read_text())
    strip = lambda s: {k: v for k, v in s.items() if k not in ('label', 'admit')}
    regen[cid] = {'spec': str(p), 'diff_excl_label_admit': ldiff(strip(g), strip(a)),
                  'brackets_equal_R1': canon(a['numerics']['brackets']) == canon(D7['R1']['brackets']),
                  'picard_passes': a['numerics']['picard']['passes'], 'admit_kind': ('PENDING' if 'PENDING' in json.dumps(a['admit']) else ('filled' if a['admit'] else 'compute'))}
f10_admit = json.loads(author['S2'].read_text())['admit']
regen['_admit_S2R_eq_Y2R_eq_C2R'] = (canon(f10_admit) == canon(json.loads(author['Y2'].read_text())['admit']) == canon(json.loads(author['C2'].read_text())['admit']))
regen['_admit_S2R_eq_first_attempt_S2'] = canon(f10_admit) == canon(json.loads(Path(D7['registered_first_attempts']['S2']['call_spec']['path']).read_text())['admit'])
regen['_admit_points_to_F10'] = all(str(RUNS / 'A2_ANCHOR_F10_RUN_V001') in v for blk in f10_admit.values() for k, v in blk.items() if 'directory' in k)
regen['_pending_admit_paths'] = {cid: sorted({v.split('(')[1].split('/stages')[0] for blk in json.loads(author[cid].read_text())['admit'].values()
                                             for k, v in blk.items() if 'directory' in k}) for cid in ('C3', 'C4', 'R', 'S3', 'Y3', 'S4', 'Y4')}
out['regen'] = regen

# ---- F3 stopped runs
stopped = json.loads((LANE / 'evidence/STOPPED_RUNS_V001.json').read_text())
f3 = {}
for name in ('KMAX_A2F10_C4_RUN_V001', 'KMAX_A2F10_R_RUN_V001'):
    rd = RUNS / name
    its, last = [], None
    for line in open(rd / 'stages/01_route_a/attempt_000/progress.jsonl'):
        last = line
        if '"iteration_completed"' in line:
            e = json.loads(line)
            its.append((e['iteration'], e['gas_fourier_residual_J'] < e['bound_J']))
    newest = max((x for x in rd.rglob('*') if x.is_file()), key=lambda x: os.stat(x).st_mtime)
    rec = stopped['stopped'][name]
    f3[name] = {'iterations_met_bound': its, 'last_event': json.loads(last).get('stage'),
                'newest_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(os.stat(newest).st_mtime)),
                'record_last_byte_utc': rec['last_byte_written']['utc_mtime'], 'record_reason': rec['reason'][:160],
                'record_stop_utc': rec['stop_utc'], 'record_stopped_by': rec['stopped_by'],
                'finish_exists': (rd / 'finish.json').exists(), 'receipt_exists': Path(str(rd) + '.receipt.json').exists()}
ps = subprocess.run(['ps', '-axo', 'command='], capture_output=True, text=True).stdout.splitlines()
f3['alive_now'] = {n: [l[:160] for l in ps if str(RUNS / n) + '/' in l or l.rstrip().endswith(str(RUNS / n))] for n in ('KMAX_A2F10_C4_RUN_V001', 'KMAX_A2F10_R_RUN_V001')}
out['F3'] = f3

# ---- F4: status claims checkable without forbidden opens
f10fin = json.loads((RUNS / 'A2_ANCHOR_F10_RUN_V001/finish.json').read_text())
c3fin = json.loads((RUNS / 'KMAX_A2F10_C3_RUN_V001/finish.json').read_text())
out['F4'] = {'F10_status': f10fin.get('status'), 'C3_v003_status': c3fin.get('status'), 'C3_v003_reasons': c3fin.get('reasons')}

# ---- seal precondition now (existence only)
now = {}
for p in sorted(RUNS.iterdir()):
    n = p.name
    if p.is_dir() and (('_V005_RUN_V001' in n) or n.startswith('DDO154_ROUTE_B_C2V005_') or 'D7R1' in n):
        now[n] = {'result_json_exists': (p / 'result.json').exists(), 'finish_json_exists': (p / 'finish.json').exists()}
for n in ('KMAX_A2F10_S2R_D7R1_RUN_V001', 'KMAX_A2F10_Y2R_D7R1_RUN_V001', 'KMAX_A2F10_C2R_D7R1_RUN_V001'):
    now.setdefault(n, {'dir_exists': (RUNS / n).exists()})
out['existence_now'] = {'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'dirs': now,
                        'seal_record_v005_exists': (LANE / 'SEAL_RECORD_V005.json').exists()}
json.dump(out, sys.stdout, indent=1, default=str)

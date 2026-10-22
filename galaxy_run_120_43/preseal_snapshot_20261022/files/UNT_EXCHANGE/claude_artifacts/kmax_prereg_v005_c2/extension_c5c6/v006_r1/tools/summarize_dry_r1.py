"""Summary V002 of the V006 R1 dry runs (v006_r1/dryrun/, produced by run_dry_r1.py).  Supersedes the summary block of
run_dry_r1.py (DRYRUN_R1_SUMMARY.json), which read stages_planned / unexplained_refusals / pin_problems from the report top
level instead of DRYRUN_REPORT.json['summary'] and compared the PENDING_PROBE configs without substituting the per-call seed
sha.  Read-only on the dry-run outputs.  Writes v006_r1/dryrun/DRYRUN_R1_SUMMARY_V002.json (must not exist).
For every expect_ok job: exit 0, guard denied nothing, summary.binding_blockers == [], summary.unexplained_refusals == [],
summary.refusals_beyond_pending_inputs == [], summary.pin_problems == [], the only remaining refusal class is
PRODUCED_BY_THIS_CALL; the per-call seed differs from the superseded _M16 dry-run seed (dryrun_b2, same driver build) only in
numerical_inputs.max_iterations (16 -> 32) and its mirror in c2_changed_fields.changed; every other simulated input is
byte-equal to the M16 one after substituting the report dir and the seed sha.
usage: python3 -I -B summarize_dry_r1.py"""
import hashlib
import json
from pathlib import Path

LANE = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/extension_c5c6')
D = LANE / 'v006_r1/dryrun'
B2 = LANE / 'dryrun_b2/dry'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def leaves(o, p=''):
    if isinstance(o, dict):
        out = {}
        for k, v in o.items():
            out.update(leaves(v, p + '/' + k))
        return out or {p: '{}'}
    return {p: json.dumps(o)}


def main():
    jobs = json.loads((D / 'DRYRUN_R1_SUMMARY.json').read_text())['jobs']
    out = {'schema': 'UNT_KMAX_EXT_DRYRUN_V006_R1_SUMMARY_V002', 'supersedes': {'path': str(D / 'DRYRUN_R1_SUMMARY.json'), 'sha256': sha(D / 'DRYRUN_R1_SUMMARY.json'),
                                                                                'defect': 'summary fields read from the wrong level; seed sha not substituted'},
           'jobs': {}}
    for name, j in sorted(jobs.items()):
        e = {k: j[k] for k in ('name', 'driver', 'driver_sha256', 'spec', 'spec_sha256', 'expect', 'exit', 'seconds', 'guard_denied', 'guard_velocity_like_opened')}
        rp = D / 'dry' / name / 'DRYRUN_REPORT.json'
        if j['expect'] == 'expect_refused':
            e['refusal_text'] = j.get('refusal_text')
            e['report_exists'] = rp.is_file()
            e['as_expected'] = j['exit'] != 0 and not rp.is_file() and not j['guard_denied']
            out['jobs'][name] = e
            continue
        r = json.loads(rp.read_text())
        s = r['summary']
        e['report_sha256'] = sha(rp)
        for k in ('stages_planned', 'binding_blockers', 'unexplained_refusals', 'refusals_beyond_pending_inputs', 'pin_problems',
                  'remaining_refusals_by_class', 'route_a_prep', 'overrides_wording'):
            e[k] = s.get(k)
        e['top_level_binding_blockers'] = r.get('binding_blockers')
        key = name[len('v009_'):-len('_M32')]
        inp = D / 'dry' / name / 'simulated_call/inputs'
        b2 = B2 / ('v009_' + key) / 'simulated_call/inputs'
        sn, so = inp / 'seed_c2v001.json', b2 / 'seed_c2v001.json'
        jn, jo = json.loads(sn.read_text()), json.loads(so.read_text())
        ln, lo = leaves(jn), leaves(jo)
        ch_n = [c for c in jn['c2_changed_fields']['changed'] if c['field'] != 'numerical_inputs.max_iterations']
        ch_o = [c for c in jo['c2_changed_fields']['changed'] if c['field'] != 'numerical_inputs.max_iterations']
        e['seed'] = {'path': str(sn), 'sha256': sha(sn), 'max_iterations': jn['numerical_inputs']['max_iterations'],
                     'fourier_points_per_axis': jn['numerical_inputs']['fourier_points_per_axis'],
                     'M16_seed': {'path': str(so), 'sha256': sha(so), 'max_iterations': jo['numerical_inputs']['max_iterations']},
                     'leaf_diff_vs_M16_seed': sorted(k for k in set(ln) | set(lo) if ln.get(k) != lo.get(k)),
                     'changed_fields_equal_except_max_iterations': ch_n == ch_o,
                     'numerical_inputs_equal_except_max_iterations': {k: v for k, v in jn['numerical_inputs'].items() if k != 'max_iterations'}
                     == {k: v for k, v in jo['numerical_inputs'].items() if k != 'max_iterations'}}
        rd_n, rd_o = str(D / 'dry' / name), str(B2 / ('v009_' + key))
        files = {}
        for f in sorted(inp.iterdir()):
            if f.name == 'seed_c2v001.json':
                continue
            a = f.read_text().replace(rd_n, '<REPORT_DIR>').replace(e['seed']['sha256'], '<SEED_SHA>')
            b = (b2 / f.name).read_text().replace(rd_o, '<REPORT_DIR>').replace(e['seed']['M16_seed']['sha256'], '<SEED_SHA>') if (b2 / f.name).is_file() else None
            files[f.name] = a == b
        e['other_simulated_inputs_equal_M16_after_report_dir_and_seed_sha_substitution'] = files
        e['as_expected'] = bool(j['exit'] == 0 and not j['guard_denied'] and e['binding_blockers'] == [] and e['top_level_binding_blockers'] == []
                                and e['unexplained_refusals'] == [] and e['refusals_beyond_pending_inputs'] == [] and e['pin_problems'] == []
                                and set(e['remaining_refusals_by_class'] or {}) == {'PRODUCED_BY_THIS_CALL'}
                                and e['seed']['max_iterations'] == 32 and e['seed']['M16_seed']['max_iterations'] == 16
                                and e['seed']['leaf_diff_vs_M16_seed'] == ['/c2_changed_fields/changed', '/numerical_inputs/max_iterations']
                                and e['seed']['changed_fields_equal_except_max_iterations'] and e['seed']['numerical_inputs_equal_except_max_iterations']
                                and all(files.values()))
        out['jobs'][name] = e
    out['n_jobs'] = len(out['jobs'])
    out['n_as_expected'] = sum(e['as_expected'] for e in out['jobs'].values())
    out['all_as_expected'] = out['n_jobs'] == out['n_as_expected']
    with open(D / 'DRYRUN_R1_SUMMARY_V002.json', 'x') as f:
        json.dump(out, f, indent=1)
        f.write('\n')
    for k, e in out['jobs'].items():
        print(k, 'exit', e['exit'], 'ok', e['as_expected'], 'stages', e.get('stages_planned'), 'blockers', e.get('binding_blockers'),
              'unexpl', e.get('unexplained_refusals'), 'classes', sorted(e.get('remaining_refusals_by_class') or {}),
              'seed', (e.get('seed') or {}).get('sha256', '')[:16], (e.get('seed') or {}).get('max_iterations'))
    print('%d/%d as expected' % (out['n_as_expected'], out['n_jobs']))


if __name__ == '__main__':
    main()

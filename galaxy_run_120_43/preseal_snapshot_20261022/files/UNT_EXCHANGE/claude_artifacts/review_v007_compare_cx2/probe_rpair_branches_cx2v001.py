"""Additional A53 R-PAIR branch and flag controls, manufactured records only.
nice unavailable (sandbox); 0514 waiver
"""
import ast
import copy
import hashlib
import json
from pathlib import Path
import resource
import time
HERE = Path(__file__).resolve().parent
setup_raw = (HERE / 'probe_compare_r5_cx2v001.py').read_bytes()
setup_tree = ast.parse(setup_raw)
prefix = []
for node in setup_tree.body:
    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'CHECKS' for t in node.targets):
        break
    prefix.append(node)
exec(compile(ast.Module(body=prefix, type_ignores=[]), str(HERE / 'probe_compare_r5_cx2v001.py') + ':setup_only', 'exec'))
checks = []
def check(name, cond, **data):
    checks.append(dict(name=name, passed=bool(cond), **data))
base = f['base_runs']()
for branch in ('PICARD', 'ROUTE_A'):
    for lab in ('C4T', 'C5H'):
        key = lab + '@RPAIR:' + ('T2' if lab == 'C5H' else 'T1_H')
        num = copy.deepcopy(base[lab]['result']['normalized_spec']['numerics'])
        if branch == 'PICARD':
            num['picard'] = dict(M.RPAIR_PICARD)
        else:
            num['route_a']['seed_source_rtol_factor'] = .1
            if lab == 'C5H':
                num['route_a']['ro1_workers'] = True
        run = f['make_run'](key, base[lab]['adapted']['rows'], numerics=num)
        if branch == 'PICARD':
            f['a53_picard_shape'](run, base[lab])
        else:
            run['adapted']['route_a_identity_sha256'] = '1' * 64
        csha = run['result']['call_spec_sha256']
        ex = {'b0_spec_shas': {M.PIN_C5H_SPEC[1], csha}, 'b0_ext_spec_shas': {csha},
              'b0_ext_entries': {csha: f['b0_ext_entry'](key, run)}}
        def validity(r):
            return M.case_validity(key, r, ctx, {'V4': True, 'V5': True}, {'status': 'PASS', 'per': {key: 'PASS'}},
                                   None, {'base': lab, 'branch': branch, 'base_run': base[lab]}, ex)
        v = validity(run)
        check(branch + '_' + lab + '_valid', v['valid_all'], v3=v.get('V3_mismatch'), v6=v.get('V6_codes'))
        attack = copy.deepcopy(run)
        if branch == 'ROUTE_A':
            attack['adapted']['route_a_identity_sha256'] = base[lab]['adapted']['route_a_identity_sha256']
        else:
            attack['route_a_outcome']['result_sha256'] = '2' * 64
        v = validity(attack)
        check(branch + '_' + lab + '_bad_custody_rejected', not v['valid_all'], v3=v.get('V3_mismatch'), v6=v.get('V6_codes'))
        if lab == 'C5H':
            attack = copy.deepcopy(run)
            attack['route_a_outcome']['ro1'] = f['ro1b'](armed=(branch == 'PICARD'))
            v = validity(attack)
            check(branch + '_C5H_wrong_armed_rejected', not v['valid_all'], v3=v.get('V3_mismatch'))

# The noisy base forces PICARD. Clean members have zero route-A noise and small Picard increments.
R = f['base_runs']()
pid = 'T1_H'
pair = M.PAIRS[pid]
for lab in pair:
    final = R[lab]['adapted']['rows']
    R[lab]['pass_rows'] = [dict(final)]  # unavailable E -> PICARD
V = {lab: {'_uvt_info': {'E_A_rows_km_s': [0.]*12}} for lab in pair}
RPV = {lab + '@RPAIR:' + pid: {'valid_all': True, '_uvt_info': {'E_A_rows_km_s': [0.]*12}} for lab in pair}
members = {lab: f['make_run'](lab + '@RPAIR:' + pid, R[lab]['adapted']['rows']) for lab in pair}
for flagged in (False, True):
    rp = {pid: {'branch': 'PICARD', '_runs': members}}
    got = M.evaluate_pair_test(pid, R, V, rp, RPV, lambda key: flagged, {}, ctx, .5, True)
    check('PICARD_base_flag_' + str(flagged), got['status'] == ('PASS_FLAGGED' if flagged else 'PASS'), status=got['status'])
bad = M.evaluate_pair_test(pid, R, V, {pid: {'branch': 'ROUTE_A', '_runs': members}}, RPV, lambda key: False, {}, ctx, .5, True)
check('RPAIR_branch_mismatch_incomplete', bad['status'] == 'INCOMPLETE', status=bad['status'])
report = {'schema': 'UNT_CX2_RPAIR_BRANCH_PROBES_V001', 'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
          'priority_note': 'nice unavailable (sandbox); 0514 waiver', 'source_pins': PINS,
          'setup_sha256': hashlib.sha256(setup_raw).hexdigest(), 'checks': checks,
          'counts': {'total': len(checks), 'passed': sum(x['passed'] for x in checks)},
          'max_rss_bytes_macos': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
          'source_stable_end': {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() == s for p,s in PINS.items()}}
with (HERE / 'RPAIR_RESULTS_CX2V001.json').open('x') as out:
    json.dump(report, out, sort_keys=True, indent=2)
    out.write('\n')
print(json.dumps({'counts': report['counts'], 'failed': [x for x in checks if not x['passed']]}))

"""Independent checker K1: V004 -> V005 leaf diff, hashes from bytes, supersedes/review pins."""
import hashlib, json, sys

A = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/'
V4 = A + 'kmax_prereg_v004_c2/KMAX_MATRIX_PREREG_V004.json'
V5 = A + 'kmax_prereg_v005_c2/KMAX_MATRIX_PREREG_V005.json'


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def leaves(o, p=''):
    if isinstance(o, dict):
        out = {}
        for k, v in o.items():
            out.update(leaves(v, p + '/' + str(k)))
        if not o:
            out[p] = {}
        return out
    if isinstance(o, list):
        out = {}
        for i, v in enumerate(o):
            out.update(leaves(v, p + '[%d]' % i))
        if not o:
            out[p] = []
        return out
    return {p: o}


d4 = json.load(open(V4)); d5 = json.load(open(V5))
l4 = leaves(d4); l5 = leaves(d5)
diff = []
for k in sorted(set(l4) | set(l5)):
    if k not in l4:
        diff.append(('ADDED', k))
    elif k not in l5:
        diff.append(('REMOVED', k))
    elif l4[k] != l5[k] or type(l4[k]) != type(l5[k]):
        diff.append(('CHANGED', k, l4[k], l5[k]))

# collapse to top-level groups
groups = {}
for t in diff:
    top = t[1].split('/')[1].split('[')[0]
    groups.setdefault(top, []).append(t)

canon = lambda o: json.dumps(o, sort_keys=True, separators=(',', ':'))
unchanged_claim = ['anchor', 'row_ids', 'quoted_sigma_km_s', 'tau_km_s', 'grids', 'grids_note',
                   'admission_constraint', 'fixed_across_all_cases', 'criterion', 'plan_item', 'change_log_v003']
uc = {k: (canon(d4.get(k)) == canon(d5.get(k))) for k in unchanged_claim}

cases4 = {c['id']: c for c in d4['cases']}; cases5 = {c['id']: c for c in d5['cases']}
case_diffs = {}
for cid in sorted(set(cases4) | set(cases5)):
    a = dict(cases4.get(cid, {})); b = dict(cases5.get(cid, {}))
    da = {k for k in set(a) | set(b) if canon(a.get(k)) != canon(b.get(k))}
    if da:
        case_diffs[cid] = {k: [a.get(k), b.get(k)] for k in da}
case_order_same = [c['id'] for c in d4['cases']] == [c['id'] for c in d5['cases']]

bi4 = d4['binding_inputs']; bi5 = d5['binding_inputs']
bi_diff = {k: ('ADDED' if k not in bi4 else 'REMOVED' if k not in bi5 else 'CHANGED')
           for k in set(bi4) | set(bi5) if canon(bi4.get(k)) != canon(bi5.get(k))}
drv_diff = {k: [bi4['drivers'].get(k), bi5['drivers'].get(k)] for k in set(bi4['drivers']) | set(bi5['drivers'])
            if canon(bi4['drivers'].get(k)) != canon(bi5['drivers'].get(k))}

pins = {
    'V004_sha': sha(V4),
    'V005_sha': sha(V5),
    'supersedes_sha_eq_V004_bytes': d5['supersedes']['sha256'] == sha(V4),
    'supersedes_seal_sha_eq': d5['supersedes']['seal']['sha256'] == sha(d5['supersedes']['seal']['path']),
    'review_sha_eq': d5['supersedes']['review']['sha256'] == sha(d5['supersedes']['review']['path']),
    'review_msg_sha_eq': d5['supersedes']['review']['message_sha256'] == sha(d5['supersedes']['review']['message']),
    'v005_driver_sha_eq_bytes': bi5['drivers']['v005']['sha256'] == sha(bi5['drivers']['v005']['path']),
    'v005_check_sha_eq_bytes': bi5['v005_independent_check']['sha256'] == sha(bi5['v005_independent_check']['path']),
    'v005_check_pins_driver': bi5['v005_independent_check']['pins_driver_sha256'] in open(bi5['v005_independent_check']['path']).read(),
    'v005_check_verdict_line_present': bi5['v005_independent_check']['verdict'] in open(bi5['v005_independent_check']['path']).read(),
    'deciding_call_spec_sha_eq_bytes': bi5['v005_deciding_test']['call_spec']['sha256'] == sha(bi5['v005_deciding_test']['call_spec']['path']),
    'deciding_launch_file_sha_eq_bytes': bi5['v005_deciding_test']['launch_file']['sha256'] == sha(bi5['v005_deciding_test']['launch_file']['path']),
    'stopped_runs_record_sha_eq': d5['amendment_v005']['stopped_runs']['record']['sha256'] == sha(d5['amendment_v005']['stopped_runs']['record']['path']),
    'R1_recovery_sha_eq': d5['amendment_v005']['d7_recovery']['R1']['recovery_file']['sha256'] == sha(d5['amendment_v005']['d7_recovery']['R1']['recovery_file']['path']),
    'R1_evidence_sha_eq': d5['amendment_v005']['d7_recovery']['R1']['evidence_file']['sha256'] == sha(d5['amendment_v005']['d7_recovery']['R1']['evidence_file']['path']),
    'corrected_base_sha_eq': d5['amendment_v005']['d7_recovery']['R1']['corrected_base_spec']['sha256'] == sha(d5['amendment_v005']['d7_recovery']['R1']['corrected_base_spec']['path']),
}
for k, c in d5['amendment_v005']['d7_recovery']['calls'].items():
    pins['call_%s_sha_eq' % k] = c['sha256'] == sha(c['path'])
    pins['call_%s_derived_sha_eq' % k] = c['derived_from']['sha256'] == sha(c['derived_from']['path'])
for k, c in d5['amendment_v005']['d7_recovery']['templates'].items():
    pins['tmpl_%s_sha_eq' % k] = c['sha256'] == sha(c['path'])
for k, c in d5['amendment_v005']['d7_recovery']['registered_first_attempts'].items():
    pins['first_%s_spec_sha_eq' % k] = c['call_spec']['sha256'] == sha(c['call_spec']['path'])
    # finish.json of v001 first attempts (not V005 runs) may be read: S2/Y2 RUN_V001
    pins['first_%s_finish_sha_eq' % k] = c['finish']['sha256'] == sha(c['finish']['path'])
    f = json.load(open(c['finish']['path']))
    pins['first_%s_finish_status_eq' % k] = (f.get('status') == c['finish']['status'] and f.get('reasons') == c['finish']['reasons'])
    pins['first_%s_result_sha_eq' % k] = f.get('result_sha256') == c['result_sha256']

out = {
    'top_level_groups_changed': {k: len(v) for k, v in groups.items()},
    'top_level_keys_added': sorted(set(d5) - set(d4)),
    'top_level_keys_removed': sorted(set(d4) - set(d5)),
    'unchanged_claim_canonical_equal': uc,
    'case_diffs': case_diffs,
    'case_order_same': case_order_same,
    'binding_inputs_diff': bi_diff,
    'drivers_diff': drv_diff,
    'supersedes_diff': [t for t in groups.get('supersedes', [])][:40],
    'status_v4': d4['status'], 'status_v5': d5['status'],
    'pins': pins,
}
json.dump(out, sys.stdout, indent=1, default=str)

# Claude4 refute helper (dispatch 0650, refute_p6): SYNTHETIC test of the builder's converter
#   /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_b7_inputs_c4/tools/make_custody_record_c4v001.py (1b097cba)
# on a report whose stage set is the one driver r5 (b5cc62af) plans for a DDO154 tail-ON run (FORMAL, driver L3131-3147,
# L3226-3241, L3268-3277): route_a, route_a_tail_manifest, reference, body, offset, fs_columns_00..03, fs_rotation, fs_feedback
# (feedback_v002), rfs_columns_00..01, then per LE pass columns, rotation, [column_mean], and feedback (feedback_v004) on every
# pass but the last, which ends with its column_mean (column_mean_v004). Every row is what comparator c2v007r2's SCRIPT_CUSTODY
# writes for an honest run (L2336-2345): planned = SCRIPTS_UVT[kind] for the 8 UVT kinds, the RO1 parallel worker for route_a,
# the AUX_UVT manifest writer, and SCRIPTS[kind] for the kinds the driver gives no successor; script_sha256 = planned; ok true.
# No real report, record, run or run listing is read: every fixture is written here (exclusive create) with fictitious run paths.
# The converter is loaded from its file and called in-process with --dry-run (it writes nothing). Run under run_fenced_c4st2.py.
import contextlib, copy, hashlib, importlib.util, io, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FIX = ROOT / 'fixtures' / 'real_stage_set_v001'
CONV = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_b7_inputs_c4/tools/make_custody_record_c4v001.py')
CONV_SHA = '1b097cbaf75d4bc1931218d943c6f247f99291a233ca46c2c0a6933d061ca841'
R5 = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py',
      'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6')
NEW_RUN = '/Volumes/SYNTHETIC_NOT_A_RUN/Z2_NEW_RUN_SYNTHETIC_REFUTE'
REF_RUN = '/Volumes/SYNTHETIC_NOT_A_RUN/Z2_REFERENCE_RUN_SYNTHETIC_REFUTE'
HEAD = [('route_a', 'route_a'), ('route_a_tail_manifest', 'route_a_tail_manifest'), ('reference', 'reference'), ('body', 'body'),
        ('offset', 'offset'), ('fs_columns_00', 'columns_v001'), ('fs_columns_01', 'columns_v001'), ('fs_columns_02', 'columns_v001'),
        ('fs_columns_03', 'columns_v001'), ('fs_rotation', 'rotation_v001')]
FS_FB = [('fs_feedback', 'feedback_v002')]
RFS = [('rfs_columns_00', 'columns_v003'), ('rfs_columns_01', 'columns_v003')]


def le(p, column_mean, feedback):
    out = [('le%d_columns_00' % p, 'columns_v005'), ('le%d_rotation' % p, 'rotation_v005')]
    if column_mean:
        out.append(('le%d_column_mean' % p, 'column_mean_v004'))
    if feedback:
        out.append(('le%d_feedback' % p, 'feedback_v004'))
    return out


SETS = {
    # the builder's PASS fixture set (18 stages: 16 UVT-kind stages, route_a, manifest); no stage of a no-successor kind
    'CONTROL_BUILDER_18_STAGES': HEAD + RFS + le(1, False, False) + le(2, False, False) + le(3, False, False),
    # driver plan, observe only on the last pass (22 stages)
    'DRIVER_PLAN_OBSERVE_LAST_PASS_22': HEAD + FS_FB + RFS + le(1, False, True) + le(2, False, True) + le(3, True, False),
    # driver plan, observe every pass or a speed bound (24 stages; VERIFY.md L57 names le1_column_mean in the r4 Z2 run)
    'DRIVER_PLAN_OBSERVE_EVERY_PASS_24': HEAD + FS_FB + RFS + le(1, True, True) + le(2, True, True) + le(3, True, False),
}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def write_x(path, obj):
    data = (json.dumps(obj, indent=1) + '\n').encode('utf-8')
    with open(path, 'xb') as f:
        f.write(data)
    return sha(data)


def planned(kind, tabs):
    if kind in tabs['UVT_TAIL_KINDS']:
        return tabs['SCRIPTS_UVT'][kind]
    if kind == 'route_a':
        return tabs['RO1_ROUTE_A']['worker_parallel']
    if kind == 'route_a_tail_manifest':
        return tabs['AUX_UVT']['manifest_writer']
    return tabs['SCRIPTS'][kind]          # comparator L1595: drv.SCRIPTS.get(kind) for every other kind


def report(stages, tabs, cmp_pin, tok_pin):
    rows = {n: {'kind': k, 'script_sha256': planned(k, tabs), 'planned_sha256': planned(k, tabs), 'ok': True} for n, k in stages}
    order = [n for n, _ in stages]
    pin = [R5[0], R5[1]]
    checks = {k: {'pass': True, 'detail': {'synthetic': True}} for k in ('BYTES_EQUAL', 'TOKENS_POLICY', 'AUTO_CUSTODY', 'INVENTORY', 'REQUEST')}
    checks['STAGE_SET'] = {'pass': True, 'detail': {'reference_problems': [], 'new_problems': [],
                                                    'order_reference': [x for x in order if x != 'route_a_tail_manifest'], 'order_new': order,
                                                    'order_equal_after_declared_extras': True,
                                                    'declared_extra_stages': {'route_a_tail_manifest': {'count': 1, 'immediately_after_route_a': True}}}}
    checks['NEW_DRIVER_PIN'] = {'pass': True, 'detail': {'selected': 'r5', 'pin': pin, 'start_json': pin, 'result_json_driver_sha256': R5[1]}}
    checks['SCRIPT_CUSTODY'] = {'pass': True, 'detail': {'rule': 'A59: every new stage runs the driver-planned script for gate Z2, hashed from bytes',
                                                         'stages': rows, 'violations': []}}
    return {'schema': 'RUN_IDENTITY_COMPARE_C2V007', 'gate': 'Z2', 'driver_selected': 'r5', 'driver_pin': pin, 'tail_on': True,
            'ro1_requirement': 'ARMED', 'declared_tail_off_records': False, 'require_ro1_armed_flag': False, 'masked_keys': ['pid', 'utc'],
            'array_policy': 'SYNTHETIC', 'declared_differ': [], 'comparator': dict(cmp_pin), 'reference': REF_RUN, 'new': NEW_RUN,
            'tokens': dict(tok_pin), 'checks': checks, 'verdict': 'PASS_BITWISE_EQUAL', 'failing': [], 'comparator_sha256_at_end': cmp_pin['sha256']}


def record(cmp_pin, tok_pin, ror_pin):
    return {'schema': 'UNT_KMAX_TAIL_V007_GATE_RECORD_C2V002', 'gate': 'B1', 'tail': 'ON', 'comparator': dict(cmp_pin), 'tokens': dict(tok_pin),
            'identity_comparison': {'gate': 'Z2', 'driver_selected': 'r5', 'report': dict(ror_pin), 'verdict': 'PASS_BITWISE_EQUAL', 'failing': [],
                                    'checks': {'SCRIPT_CUSTODY': True, 'NEW_DRIVER_PIN': True, 'STAGE_SET': True}},
            'run': {'path': NEW_RUN, 'driver_sha256': R5[1]}, 'reference_run': {'path': REF_RUN},
            'a67_n1': {'identity_run_driver_sha256': R5[1], 'is_v010_r5': True}, 'verdict': 'PASS_BITWISE_EQUAL_EXCEPT_DECLARED'}


def main():
    craw = CONV.read_bytes()
    assert sha(craw) == CONV_SHA, 'converter bytes are not 1b097cba'
    spec = importlib.util.spec_from_file_location('make_custody_record_c4v001', str(CONV))
    conv = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(conv)
    draw = Path(R5[0]).read_bytes()
    assert sha(draw) == R5[1]
    tabs = conv.driver_tables(draw)
    no_succ = sorted(k for k in tabs['SCRIPTS'] if k not in tabs['UVT_TAIL_KINDS'] and k != 'route_a')
    cmp_pin = {'path': conv.COMPARATOR[0], 'sha256': conv.COMPARATOR[1]}
    assert sha(Path(cmp_pin['path']).read_bytes()) == cmp_pin['sha256']
    FIX.mkdir(parents=True, exist_ok=False)
    tok_path = FIX / 'SYNTH_TOKENS_Z2.json'
    tok_pin = {'path': str(tok_path), 'sha256': write_x(tok_path, {'declared': [], 'note': 'SYNTHETIC tokens file (refute_p6)'})}
    res = {'converter': {'path': str(CONV), 'sha256': CONV_SHA}, 'driver': {'path': R5[0], 'sha256': R5[1]},
           'driver_kinds_without_a_successor': no_succ, 'synthetic_only': True, 'cases': []}
    for name, stages in SETS.items():
        d = FIX / name
        d.mkdir()
        rp = d / 'Z2_REPORT_SYNTHETIC.json'
        rep = report(stages, tabs, cmp_pin, tok_pin)
        rsha = write_x(rp, rep)
        recp = d / 'B1_RECORD_SYNTHETIC.json'
        recsha = write_x(recp, record(cmp_pin, tok_pin, {'path': str(rp), 'sha256': rsha}))
        argv = ['--report', str(rp), '--report-sha256', rsha, '--identity-record', str(recp), '--identity-record-sha256', recsha,
                '--driver-sha256', R5[1], '--out', str(d / 'CUSTODY_WOULD_BE.json'), '--dry-run']
        err, out = io.StringIO(), io.StringIO()
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(out):
            rc = conv.main(argv)
        last = json.loads(err.getvalue().strip().splitlines()[-1])
        rec_obj = json.loads(out.getvalue()) if rc == 0 else None
        res['cases'].append({'case': name, 'n_stages': len(stages),
                             'stages_of_no_successor_kinds': [n for n, k in stages if k in no_succ],
                             'rc': rc, 'verdict': last.get('verdict'), 'code': last.get('code'), 'detail': last.get('detail'),
                             'dry_run_record_counts': None if rec_obj is None else [rec_obj['stages_total'], rec_obj['stages_successor']],
                             'wrote_output': (d / 'CUSTODY_WOULD_BE.json').exists()})
    res['expected'] = {'CONTROL_BUILDER_18_STAGES': 'DRY_RUN_PASS', 'DRIVER_PLAN_OBSERVE_LAST_PASS_22': 'REFUSE STAGE_KIND_HAS_NO_SUCCESSOR',
                       'DRIVER_PLAN_OBSERVE_EVERY_PASS_24': 'REFUSE STAGE_KIND_HAS_NO_SUCCESSOR'}
    outp = ROOT / 'TEST_CONVERTER_REAL_STAGE_SET_R6V001.json'
    with open(outp, 'x', encoding='utf-8') as f:
        f.write(json.dumps(res, indent=1, sort_keys=True) + '\n')
    print(json.dumps(res, indent=1, sort_keys=True))
    print('WROTE', outp, sha(outp.read_bytes()))


if __name__ == '__main__':
    main()

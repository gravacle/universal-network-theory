# Claude4 helper (dispatch 0650, A113 P6): SYNTHETIC tests of tools/make_custody_record_c4v001.py. No real run output is read:
# every report, record and tokens file is a synthetic look-alike written here (exclusive create) under fixtures/custody_synth_v001/;
# their run paths are fictitious strings that are never opened. The real comparator source (c2v007r2 052da0fe) and the real driver
# slot source (r5 b5cc62af) are read as bytes (the driver as AST and by an independent regex, never executed): the synthetic stage
# rows use the driver's own successor shas. The converter is loaded from its file and called in-process (main(argv)), one case at a
# time, with stderr captured. A passing case must write exactly one record; a must-fail case must return 2, name its code, and write
# nothing. Results are written once, by exclusive create. Run under tools/run_fenced_c4st2.py.
import contextlib, copy, hashlib, importlib.util, io, json, os, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FIX = ROOT / 'fixtures' / 'custody_synth_v001'
CONV = HERE / 'make_custody_record_c4v001.py'
R5 = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py',
      'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6')
R4 = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r4/galaxy_m0_forward_c2v010.py',
      'b9ae92d5857951511437cf7632eb732c97b63592ed700e6810941c5f2d8d762b')
NEW_RUN = '/Volumes/SYNTHETIC_NOT_A_RUN/Z2_NEW_RUN_SYNTHETIC'
REF_RUN = '/Volumes/SYNTHETIC_NOT_A_RUN/Z2_REFERENCE_RUN_SYNTHETIC'
STAGES = [('reference', 'reference'), ('body', 'body'), ('offset', 'offset'), ('fs_columns_00', 'columns_v001'), ('fs_columns_01', 'columns_v001'),
          ('fs_columns_02', 'columns_v001'), ('fs_columns_03', 'columns_v001'), ('fs_rotation', 'rotation_v001'), ('rfs_columns_00', 'columns_v003'),
          ('rfs_columns_01', 'columns_v003'), ('le1_columns_00', 'columns_v005'), ('le1_rotation', 'rotation_v005'), ('le2_columns_00', 'columns_v005'),
          ('le2_rotation', 'rotation_v005'), ('le3_columns_00', 'columns_v005'), ('le3_rotation', 'rotation_v005'), ('route_a', 'route_a'),
          ('route_a_tail_manifest', 'route_a_tail_manifest')]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def load_conv():
    spec = importlib.util.spec_from_file_location('make_custody_record_c4v001', str(CONV))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def regex_tables(text):
    """an independent extraction (regex over the source lines) to cross-check the converter's AST reader"""
    out = {}
    for name in ('SCRIPTS', 'SCRIPTS_UVT', 'RO1_ROUTE_A', 'AUX_UVT', 'PARALLEL_ROUTE_A'):
        m = re.search(r'^%s = \{\n(.*?)^\}' % name, text, re.S | re.M)
        out[name] = dict(re.findall(r"^    '([A-Za-z0-9_]+)': \(.*?, '([0-9a-f]{64})'\),?[ \t]*$", m.group(1), re.M))
    m = re.search(r"^UVT_TAIL_KINDS = \((.*?)\)[ \t]*$", text, re.M)
    out['UVT_TAIL_KINDS'] = tuple(re.findall(r"'([a-z0-9_]+)'", m.group(1)))
    return out


def write_x(path, obj=None, raw=None):
    data = raw if raw is not None else (json.dumps(obj, indent=1) + '\n').encode('utf-8')
    with open(path, 'xb') as f:
        f.write(data)
    return sha(data)


def base_report(tabs, cmp_pin, tok_pin):
    rows = {}
    for name, kind in STAGES:
        if kind in tabs['UVT_TAIL_KINDS']:
            s = tabs['SCRIPTS_UVT'][kind]
        elif kind == 'route_a':
            s = tabs['RO1_ROUTE_A']['worker_parallel']
        else:
            s = tabs['AUX_UVT']['manifest_writer']
        rows[name] = {'kind': kind, 'script_sha256': s, 'planned_sha256': s, 'ok': True}
    order = [n for n, _ in STAGES]
    pin = [R5[0], R5[1]]
    checks = {k: {'pass': True, 'detail': {'synthetic': True}} for k in ('BYTES_EQUAL', 'TOKENS_POLICY', 'AUTO_CUSTODY', 'INVENTORY', 'REQUEST',
                                                                           'RO1', 'RO1_CUSTODY', 'STRICT_PARSE', 'TREE_STABLE')}
    checks['STAGE_SET'] = {'pass': True, 'detail': {'reference_problems': [], 'new_problems': [], 'order_reference': order[:-1], 'order_new': order,
                                                    'order_equal_after_declared_extras': True,
                                                    'declared_extra_stages': {'route_a_tail_manifest': {'count': 1, 'immediately_after_route_a': True}}}}
    checks['NEW_DRIVER_PIN'] = {'pass': True, 'detail': {'selected': 'r5', 'pin': pin, 'start_json': pin, 'result_json_driver_sha256': R5[1]}}
    checks['SCRIPT_CUSTODY'] = {'pass': True, 'detail': {'rule': 'A59: every new stage runs the driver-planned script for gate Z2, hashed from bytes',
                                                         'stages': rows, 'violations': []}}
    return {'schema': 'RUN_IDENTITY_COMPARE_C2V007', 'gate': 'Z2', 'driver_selected': 'r5', 'driver_pin': pin, 'tail_on': True,
            'ro1_requirement': 'ARMED', 'declared_tail_off_records': False, 'require_ro1_armed_flag': False, 'masked_keys': ['pid', 'utc'],
            'array_policy': 'SYNTHETIC', 'declared_differ': [], 'comparator': dict(cmp_pin), 'reference': REF_RUN, 'new': NEW_RUN,
            'tokens': dict(tok_pin), 'checks': checks, 'verdict': 'PASS_BITWISE_EQUAL', 'failing': [], 'comparator_sha256_at_end': cmp_pin['sha256']}


def base_record(cmp_pin, tok_pin, ror_pin):
    names = ['BYTES_EQUAL', 'STAGE_SET', 'TOKENS_POLICY', 'AUTO_CUSTODY', 'NEW_DRIVER_PIN', 'SCRIPT_CUSTODY', 'RO1', 'RO1_CUSTODY']
    return {'schema': 'UNT_KMAX_TAIL_V007_GATE_RECORD_C2V002', 'gate': 'B1', 'producer': {'path': '/SYNTHETIC/producer.py', 'sha256': '0' * 64},
            'tail': 'ON', 'comparator': dict(cmp_pin), 'tokens': dict(tok_pin),
            'identity_comparison': {'gate': 'Z2', 'driver_selected': 'r5', 'report': dict(ror_pin), 'verdict': 'PASS_BITWISE_EQUAL', 'failing': [],
                                    'checks': {k: True for k in names}},
            'run': {'path': NEW_RUN, 'driver_sha256': R5[1]}, 'reference_run': {'path': REF_RUN},
            'a67_n1': {'identity_run_driver_sha256': R5[1], 'is_v010_r5': True}, 'verdict': 'PASS_BITWISE_EQUAL_EXCEPT_DECLARED'}


def main():
    conv = load_conv()
    results = {'converter': {'path': str(CONV), 'sha256': sha(CONV.read_bytes())}, 'synthetic_only': True, 'cases': []}
    drv_raw = Path(R5[0]).read_bytes()
    assert sha(drv_raw) == R5[1]
    tabs = conv.driver_tables(drv_raw)
    rx = regex_tables(drv_raw.decode('utf-8'))
    agree = {k: (tabs[k] == rx[k]) for k in rx}
    results['driver_tables_ast_equals_regex'] = agree
    results['driver_tables'] = {k: (list(v) if isinstance(v, tuple) else v) for k, v in tabs.items()}
    cmp_raw = Path(conv.COMPARATOR[0]).read_bytes()
    assert sha(cmp_raw) == conv.COMPARATOR[1]
    cmp_pin = {'path': conv.COMPARATOR[0], 'sha256': conv.COMPARATOR[1]}
    FIX.mkdir(parents=False, exist_ok=False)
    tok_path = FIX / 'SYNTH_TOKENS_Z2.json'
    tok_pin = {'path': str(tok_path), 'sha256': write_x(tok_path, {'declared': [], 'note': 'SYNTHETIC tokens file for converter tests only'})}
    ror_path = FIX / 'SYNTH_Z2_REPORT_OF_RECORD.json'
    rep0 = base_report(tabs, cmp_pin, tok_pin)
    ror_pin = {'path': str(ror_path), 'sha256': write_x(ror_path, rep0)}
    rec_path = FIX / 'SYNTH_B1_RECORD.json'
    rec0 = base_record(cmp_pin, tok_pin, ror_pin)
    rec_pin = {'path': str(rec_path), 'sha256': write_x(rec_path, rec0)}

    def run_case(name, expect, mutate_report=None, raw_report=None, record=None, args=None, use_record_report=False, pre_out=False):
        d = FIX / name
        d.mkdir()
        if use_record_report:
            rp, rs = str(ror_path), ror_pin['sha256']
        else:
            rp = str(d / 'REPORT.json')
            if raw_report is not None:
                rs = write_x(rp, raw=raw_report)
            else:
                r = copy.deepcopy(rep0)
                if mutate_report:
                    mutate_report(r)
                rs = write_x(rp, r)
        if record is not None:
            recp = str(d / 'RECORD.json')
            recs = write_x(recp, record)
        else:
            recp, recs = rec_pin['path'], rec_pin['sha256']
        out = str(d / 'CUSTODY.json')
        if pre_out:
            write_x(out, raw=b'pre-existing\n')
        argv = ['--report', rp, '--report-sha256', rs, '--identity-record', recp, '--identity-record-sha256', recs, '--driver-sha256', R5[1],
                '--out', out]
        if args:
            argv = args(argv, d)
        err = io.StringIO()
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
            rc = conv.main(argv)
        msg = err.getvalue().strip().splitlines()
        last = json.loads(msg[-1]) if msg else {}
        wrote = os.path.exists(out) and not pre_out
        pre_intact = (Path(out).read_bytes() == b'pre-existing\n') if pre_out else None
        if expect == 'PASS':
            ok = rc == 0 and wrote and last.get('verdict') == 'PASS'
        else:
            ok = rc == 2 and not wrote and last.get('code') == expect and (pre_intact is not False)
        row = {'case': name, 'expect': expect, 'rc': rc, 'code': last.get('code', last.get('verdict')), 'wrote_output': wrote, 'ok': ok}
        if pre_out:
            row['pre_existing_out_unchanged'] = pre_intact
        if wrote:
            row['output'] = {'path': out, 'sha256': sha(Path(out).read_bytes())}
        results['cases'].append(row)
        return row

    def setp(path, value):
        def f(r):
            cur = r
            for k in path[:-1]:
                cur = cur[k]
            cur[path[-1]] = value
        return f

    def delp(path):
        def f(r):
            cur = r
            for k in path[:-1]:
                cur = cur[k]
            del cur[path[-1]]
        return f

    rows_path = ('checks', 'SCRIPT_CUSTODY', 'detail', 'stages')
    base_le1 = tabs['SCRIPTS']['columns_v005']
    # passing cases
    run_case('P01_RERUN_REPORT_EQUAL_TO_THE_REPORT_OF_RECORD', 'PASS')
    run_case('P02_THE_REPORT_OF_RECORD_ITSELF', 'PASS', use_record_report=True)
    # must-fail cases
    run_case('F01_A_STAGE_WITHOUT_ITS_CUSTODY_ROW', 'STAGE_WITHOUT_CUSTODY_ROW', delp(rows_path + ('le2_rotation',)))
    run_case('F02_A_UVT_STAGE_ON_ITS_BASE_SCRIPT', 'STAGE_NOT_ON_ITS_SUCCESSOR',
             setp(rows_path + ('le1_columns_00',), {'kind': 'columns_v005', 'script_sha256': base_le1, 'planned_sha256': base_le1, 'ok': True}))
    run_case('F03_A_STAGE_NOT_ON_ITS_PLANNED_SCRIPT', 'STAGE_NOT_ON_ITS_PLANNED_SCRIPT',
             setp(rows_path + ('body',), {'kind': 'body', 'script_sha256': tabs['SCRIPTS']['body'], 'planned_sha256': tabs['SCRIPTS_UVT']['body'], 'ok': False}))
    run_case('F04_GATE_Z2_OFF_RO1_NOT_Z2', 'RUN_NOT_Z2', setp(('gate',), 'Z2_OFF_RO1'))
    run_case('F05_REPORT_ON_DRIVER_R4', 'DRIVER_NOT_THE_SLOT', setp(('driver_pin',), [R4[0], R4[1]]))
    run_case('F06_DRIVER_SHA_ARGUMENT_NOT_THE_REPORT_DRIVER', 'DRIVER_NOT_THE_SLOT',
             args=lambda a, d: a[:a.index('--driver-sha256') + 1] + [R4[1]] + a[a.index('--driver-sha256') + 2:])
    run_case('F07_COMPARISON_VERDICT_FAIL', 'COMPARISON_NOT_PASS', lambda r: (r.update(verdict='FAIL', failing=['BYTES_EQUAL'])))
    run_case('F08_SCRIPT_CUSTODY_CHECK_FALSE', 'COMPARISON_NOT_PASS', setp(('checks', 'SCRIPT_CUSTODY', 'pass'), False))
    dup = (json.dumps(rep0, indent=1)[:-2] + ',\n "gate": "Z2"\n}\n').encode('utf-8')
    run_case('F09_MALFORMED_DUPLICATE_JSON_KEY', 'REPORT_JSON', raw_report=dup)
    nan = json.dumps(rep0, indent=1).replace('"array_policy": "SYNTHETIC"', '"array_policy": NaN').encode('utf-8')
    run_case('F10_MALFORMED_NON_FINITE_CONSTANT', 'REPORT_JSON', raw_report=nan)
    run_case('F11_MALFORMED_NOT_AN_OBJECT', 'REPORT_SHAPE', raw_report=b'[1, 2, 3]\n')
    run_case('F12_MALFORMED_SCRIPT_CUSTODY_ABSENT', 'CHECK_MISSING_OR_MALFORMED', delp(('checks', 'SCRIPT_CUSTODY')))
    run_case('F13_MALFORMED_STAGE_ROW_EXTRA_KEY', 'STAGE_ROW_MALFORMED',
             lambda r: r['checks']['SCRIPT_CUSTODY']['detail']['stages']['offset'].update(extra=1))
    fb = tabs['SCRIPTS']['feedback_v002']
    run_case('F14_A_STAGE_KIND_WITH_NO_SUCCESSOR', 'STAGE_KIND_HAS_NO_SUCCESSOR',
             lambda r: (r['checks']['STAGE_SET']['detail']['order_new'].append('le1_feedback'),
                        r['checks']['SCRIPT_CUSTODY']['detail']['stages'].update(
                            le1_feedback={'kind': 'feedback_v002', 'script_sha256': fb, 'planned_sha256': fb, 'ok': True})))
    run_case('F15_COMPARATOR_NOT_C2V007R2', 'COMPARATOR_NOT_C2V007R2', setp(('comparator', 'sha256'), '1' * 64))
    run_case('F16_REPORT_SHA_ARGUMENT_WRONG', 'REPORT_PIN_MISMATCH',
             args=lambda a, d: a[:a.index('--report-sha256') + 1] + ['2' * 64] + a[a.index('--report-sha256') + 2:])
    rec_other = copy.deepcopy(rec0)
    rec_other['run']['path'] = '/Volumes/SYNTHETIC_NOT_A_RUN/A_DIFFERENT_Z2_RUN'
    run_case('F17_RECORD_NAMES_ANOTHER_RUN', 'NOT_THE_RECORDED_Z2_RUN', record=rec_other)
    run_case('F18_RERUN_CUSTODY_DIFFERS_FROM_THE_REPORT_OF_RECORD', 'RERUN_DIFFERS_FROM_THE_REPORT_OF_RECORD',
             lambda r: r['checks']['STAGE_SET']['detail'].update(order_reference=['reference']))
    run_case('F19_OUT_EXISTS_NO_OVERWRITE', 'OUT_EXISTS', pre_out=True)
    run_case('F20a_CLI_REPEATED_FLAG', 'CLI_REPEATED_FLAG', args=lambda a, d: a + ['--driver-sha256', R5[1]])
    run_case('F20b_CLI_FLAG_EQUALS_VALUE', 'CLI_ARGUMENT', args=lambda a, d: ['--report=' + a[1]] + a[2:])
    run_case('F20c_CLI_ABBREVIATED_FLAG', 'CLI_ARGUMENT', args=lambda a, d: ['--rep'] + a[1:])
    run_case('F21_NEW_DRIVER_PIN_RESULT_ON_ANOTHER_DRIVER', 'NEW_DRIVER_PIN_NOT_THE_SLOT',
             setp(('checks', 'NEW_DRIVER_PIN', 'detail', 'result_json_driver_sha256'), R4[1]))
    run_case('F22_NO_STAGES', 'STAGE_SET_MALFORMED',
             lambda r: (r['checks']['STAGE_SET']['detail'].update(order_new=[]), r['checks']['SCRIPT_CUSTODY']['detail'].update(stages={})))
    run_case('F23_OUT_INSIDE_THE_COMPARED_RUN', 'OUT_INSIDE_A_COMPARED_RUN', lambda r: r.update(new=str(FIX / 'F23_OUT_INSIDE_THE_COMPARED_RUN')))
    run_case('F24_RECORD_SHA_ARGUMENT_WRONG', 'RECORD_PIN_MISMATCH',
             args=lambda a, d: a[:a.index('--identity-record-sha256') + 1] + ['3' * 64] + a[a.index('--identity-record-sha256') + 2:])
    run_case('F25_SCRIPT_CUSTODY_RULE_OF_ANOTHER_GATE', 'SCRIPT_CUSTODY_RULE',
             setp(('checks', 'SCRIPT_CUSTODY', 'detail', 'rule'), 'A59: every new stage runs the driver-planned script for gate Z2_OFF_RO1, hashed from bytes'))
    run_case('F26_ROUTE_A_ON_THE_BASE_PARALLEL_WORKER', 'STAGE_NOT_ON_ITS_SUCCESSOR',
             setp(rows_path + ('route_a',), {'kind': 'route_a', 'script_sha256': tabs['PARALLEL_ROUTE_A']['worker'],
                                            'planned_sha256': tabs['PARALLEL_ROUTE_A']['worker'], 'ok': True}))
    run_case('F27_RECORD_ON_ANOTHER_DRIVER', 'RECORD_DRIVER_NOT_THE_SLOT',
             record=dict(copy.deepcopy(rec0), a67_n1={'identity_run_driver_sha256': R4[1]}))
    results['n_cases'] = len(results['cases'])
    results['n_ok'] = sum(1 for c in results['cases'] if c['ok'])
    results['all_ok'] = results['n_ok'] == results['n_cases'] and all(agree.values())
    results['fixture_pins'] = {'tokens': tok_pin, 'report_of_record': ror_pin, 'record': rec_pin}
    outp = ROOT / 'TEST_CUSTODY_CONVERTER_SYNTHETIC_C4V001.json'
    with open(outp, 'x', encoding='utf-8') as f:
        f.write(json.dumps(results, indent=1, sort_keys=True) + '\n')
    print(json.dumps({'all_ok': results['all_ok'], 'n_ok': results['n_ok'], 'n_cases': results['n_cases'], 'ast_equals_regex': agree,
                      'results': str(outp), 'results_sha256': sha(outp.read_bytes())}, sort_keys=True))
    for c in results['cases']:
        print('%-55s expect %-40s got rc=%s %-40s wrote=%s ok=%s' % (c['case'], c['expect'], c['rc'], c['code'], c['wrote_output'], c['ok']))
    return 0 if results['all_ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())

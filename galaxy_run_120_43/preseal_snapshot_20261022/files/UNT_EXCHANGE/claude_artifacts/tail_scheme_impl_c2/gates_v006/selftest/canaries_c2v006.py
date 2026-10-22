"""c2v006 selftest canaries (Claude2 gates_v006), synthetic trees only.
Group C = the c2v004 CHECK canary set (gates_v004/check/scripts/canaries_c2v004_cl001.py 9ff721e0: F01-F30, P00-P08, Q01-Q05; the
  B1/B2/S1-S3 classes of gates_v004/check/CHECK.md), PORTED onto c2v005/c2v006-valid baseline trees.  The c2v004 base trees
  (SELFTEST_C2V004_V002/C/C2) do not satisfy the c2v005 gates (no result driver_sha256, no driver-planned scripts, no Z2 tail
  argv), so every case is rebuilt on the independent Codex2 invocation fixture (ported_cx2/invocation_canaries_cx2v003_port_c2v006
  Tree: B0P_RERUN and Z2 trees).  The Q (probe) cases of c2v004 were declared-uncompared classes; c2v005 S3 compares them, so they
  are MUST_FAIL here.
Group D = own c2v006 canaries (O01-O29): normalization collisions at every level, raw normalizer text, duplicate JSON / JSONL /
  NPZ members, structured dtype, ARRAY_POLICY storage order, trailing bytes, A71 duplicates (argv, stage_records, tokens),
  hexmap many-to-one, TREE_STABLE fault injection, comparator exception path, run-root boundary.
Each case: MUST_PASS (verdict PASS_BITWISE_EQUAL) or MUST_FAIL (verdict FAIL and every named check failing) or MUST_REFUSE.
  python3 -I -B canaries_c2v006.py --comparator C --sha256 S --driver r4|r5 --out DIR
"""
import argparse
import contextlib
import copy
import datetime
import hashlib
import importlib.util
import io
import json
import sys
import types
import warnings
import zipfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
INV = HERE / 'ported_cx2' / 'invocation_canaries_cx2v003_port_c2v006.py'
EXT = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/extension_c5c6/driver_v009/galaxy_m0_forward_c2v009.py',
       '999331afd604dd9829aa8f389f43cdb87603d03412d52ba09712226787f18db6')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def load(p, name, expected=None):
    raw = Path(p).read_bytes()
    if expected is not None and sha(raw) != expected:
        raise SystemExit('pin %s' % p)
    m = types.ModuleType(name)
    m.__file__ = str(p)
    sys.modules[name] = m
    exec(compile(raw, str(p), 'exec'), m.__dict__)
    return m


def npy_bytes(a):
    b = io.BytesIO()
    np.save(b, a, allow_pickle=False)
    return b.getvalue()


def npz_bytes(compressed=False, members=None, raw_members=None):
    b = io.BytesIO()
    if raw_members is not None:
        with zipfile.ZipFile(b, 'w') as z:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', UserWarning)
                for n, payload in raw_members:
                    z.writestr(n, payload)
    elif compressed:
        np.savez_compressed(b, **members)
    else:
        np.savez(b, **members)
    return b.getvalue()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--comparator', required=True)
    ap.add_argument('--sha256', required=True)
    ap.add_argument('--driver', required=True, choices=('r4', 'r5'))
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=False)
    I = load(INV, '_inv_port_c2v006')
    m = load(a.comparator, '_cmp_c2v006_canaries', a.sha256)
    m.DRIVER[:] = list(m.DRIVERS[a.driver])
    drv = m.load_driver()
    cm = m.load_cm()
    rows = []
    ref_req = 'stages/11_reference/request.json'
    ref_fin = 'stages/11_reference/reference/finish.json'
    ra_req = 'stages/07_route_a/request.json'

    def refinish(t):
        t.obj('finish.json')['result_sha256'] = I.sha(I.raw_json(t.obj('result.json')))

    def case(name, gate, expect, mut=None, must_fail=(), note='', tokens_override=None, patch=None):
        d = out / name
        d.mkdir()
        r = I.Tree(d / 'REF', 'REF', gate, m, drv, cm)
        n = I.Tree(d / 'NEW', 'NEW', gate, m, drv, cm)
        tokens = []
        if gate == 'Z2':
            for old, new, label in ((I.REF_BIND, drv.RO1_ROUTE_A['binding'], 'BINDING'), (I.REF_FAC, drv.AUX_UVT['facade'], 'FACADE')):
                tokens.extend([[old[0], str(new[0]), '<' + label + '_PATH>'], [old[1], new[1], '<' + label + '_SHA>']])
            for kind in sorted(drv.UVT_TAIL_KINDS):
                old, new = drv.SCRIPTS[kind], drv.SCRIPTS_UVT[kind]
                tokens.extend([[str(old[0]), str(new[0]), '<UVT_' + kind + '_PATH>'], [old[1], new[1], '<UVT_' + kind + '_SHA>']])
        res = mut(r, n, d) if mut else None
        r.publish()
        n.publish()
        if isinstance(res, dict) and 'post' in res:
            res['post'](r, n, d)
        tp = d / 'TOKENS.json'
        if isinstance(res, dict) and 'tokens_raw' in res:
            with open(tp, 'xb') as f:
                f.write(res['tokens_raw'])
        else:
            with open(tp, 'xb') as f:
                f.write(I.raw_json({'declared': res['tokens'] if isinstance(res, dict) and 'tokens' in res else tokens}))
        op = d / 'REPORT.json'
        argv = ['--driver', a.driver, '--gate', gate, '--reference', str(r.root), '--new', str(n.root), '--tokens', str(tp), '--out', str(op)]
        exc = None
        saved = {}
        if patch:
            saved = patch(m, r, n)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                m.main(argv)
        except SystemExit as e:
            exc = 'SystemExit: %s' % e
        except Exception as e:
            exc = '%s: %s' % (type(e).__name__, e)
        finally:
            for k, v in saved.items():
                setattr(m, k, v)
        rep = json.loads(op.read_bytes()) if op.exists() else {}
        verdict = rep.get('verdict', 'REFUSED' if exc and exc.startswith('SystemExit') else 'CRASH')
        failing = rep.get('failing') or []
        if expect == 'MUST_PASS':
            ok = verdict == 'PASS_BITWISE_EQUAL'
        elif expect == 'MUST_FAIL':
            ok = verdict == 'FAIL' and set(must_fail) <= set(failing)
        else:  # MUST_REFUSE
            ok = verdict == 'REFUSED'
        rows.append({'case': name, 'gate': gate, 'expect': expect, 'must_fail': list(must_fail), 'verdict': verdict, 'failing': failing,
                     'ok': ok, 'exception': exc, 'note': note,
                     'report': {'path': str(op), 'sha256': sha(op.read_bytes())} if op.exists() else None})
        print('%-6s %-58s %-10s %-18s %s' % ('ok' if ok else 'BREACH', name, expect, verdict, failing), flush=True)

    B, Z = 'B0P_RERUN', 'Z2'

    def copy_stage(t, src, dst, tamper=None):
        for rel in list(t.files):
            if rel.startswith('stages/%s/' % src):
                t.files['stages/%s/' % dst + rel[len('stages/%s/' % src):]] = copy.deepcopy(t.files[rel])
        if tamper:
            tamper(t)

    # ================= group C: the c2v004 CHECK canaries, ported =================
    case('C_P00_baseline_B0P', B, 'MUST_PASS')
    case('C_P00_baseline_Z2', Z, 'MUST_PASS')
    case('C_F01_extra_toplevel_txt', B, 'MUST_FAIL', lambda r, n, d: n.files.__setitem__('notes.txt', ('raw', b'x\n')), ('INVENTORY',))
    case('C_F02_extra_route_a_attempt_json', Z, 'MUST_FAIL', lambda r, n, d: n.add('stages/07_route_a/attempt_000/extra.json', {'x': 1}), ('INVENTORY',))
    case('C_F03_extra_inputs_file', B, 'MUST_FAIL', lambda r, n, d: n.add('inputs/extra_config.json', {'x': 1}), ('INVENTORY',))

    def f04(r, n, d):
        copy_stage(n, '11_reference', '19_reference')
        n.obj(ref_fin)['matrix'][0][0] = 999.0
    case('C_F04_duplicate_stage_tampered_plus_faithful_copy', B, 'MUST_FAIL', f04, ('STAGE_SET',), 'B1 of CHECK.md')
    case('C_F05_duplicate_stage_extra_identical_copy', B, 'MUST_FAIL', lambda r, n, d: copy_stage(n, '11_reference', '19_reference'), ('STAGE_SET',))

    def f06(r, n, d):
        b = bytearray(n.files['stages/07_route_a/checkpoint/blobs/independent_blob.npy'][1])
        b[-1] ^= 1
        n.files['stages/07_route_a/checkpoint/blobs/independent_blob.npy'] = ('raw', bytes(b))
    case('C_F06_route_a_blob_last_bit', Z, 'MUST_FAIL', f06, ('RA_BLOBS',))

    def f07(r, n, d):
        r.files['stages/11_reference/reference/field.npy'] = ('raw', npy_bytes(np.array([1.0, 2.0])))
        n.files['stages/11_reference/reference/field.npy'] = ('raw', npy_bytes(np.array([1.0, np.nextafter(2.0, 3.0)])))
    case('C_F07_stage_npy_1ulp', B, 'MUST_FAIL', f07, ('STAGES',))

    def f08(r, n, d):
        r.files['stages/07_route_a/attempt_000/arrays/000001_extra.npy'] = ('raw', npy_bytes(np.array([1.0])))
        n.files['stages/07_route_a/attempt_000/arrays/000001_extra.npy'] = ('raw', npy_bytes(np.array([2.0])))
    case('C_F08_route_a_attempt_npy_changed', Z, 'MUST_FAIL', f08, ('FILES_ROUTE_A',), 'c2v004 PROBE; compared since c2v005')
    case('C_F09_stage_argv_value', B, 'MUST_FAIL', lambda r, n, d: n.obj(ref_req).update(argv=['--columns', '0,2,5', '--tolerance', '0.000250']), ('REQUEST',))

    def f10(r, n, d):
        av = n.obj(ra_req)['argv']
        av[av.index('--column-workers') + 1] = '4'
    case('C_F10_route_a_argv_column_workers', Z, 'MUST_FAIL', f10, ('REQUEST',))

    def f11(r, n, d):
        n.obj(ra_req)['argv'][:0] = ['--uv-tail-sidecar-directory', '/elsewhere/uv_tail_sidecar']
    case('C_F11_route_a_tail_flag_twice_first_outside_run', Z, 'MUST_FAIL', f11, ('REQUEST',), 'S1 of CHECK.md')
    case('C_F12_rotation_dir_flag_on_reference_stage', Z, 'MUST_FAIL',
         lambda r, n, d: n.obj(ref_req)['argv'].extend(['--uv-tail-source-rotation-directory', str(n.root / 'stages/11_reference/x')]), ('REQUEST',), 'S2')

    def f13(r, n, d):
        for t in (r, n):
            copy_stage(t, '11_reference', '12_fs_feedback')
            q = t.obj('stages/12_fs_feedback/request.json')
            q['kind'], q['name'] = 'feedback_v002', 'fs_feedback'
            q['argv'] = ['--columns', '0,2,5', '--tolerance', '0.00025']
            if 'feedback_v002' in drv.SCRIPTS:
                q['script'], q['script_sha256'] = str(drv.SCRIPTS['feedback_v002'][0]), drv.SCRIPTS['feedback_v002'][1]
        n.obj('stages/12_fs_feedback/request.json')['argv'].append('--uv-tail-admit-test-only')
    case('C_F13_tail_flag_on_non_uvt_kind_stage', Z, 'MUST_FAIL', f13, ('REQUEST',), 'S2')

    def f14(r, n, d):
        r.obj(ref_fin)['probe'] = 0.0
        n.obj(ref_fin)['probe'] = -0.0
    case('C_F14_stage_json_signed_zero', B, 'MUST_FAIL', f14, ('STAGES',))

    def res_mut(fn_):
        def f(r, n, d):
            fn_(r, n)
            refinish(r)
            refinish(n)
        return f
    case('C_F15_result_rows_signed_zero', B, 'MUST_FAIL',
         res_mut(lambda r, n: [r.obj('result.json')['rows'][0].update(speed_km_s=0.0), n.obj('result.json')['rows'][0].update(speed_km_s=-0.0)]), ('RESULT',))
    case('C_F16_result_unlisted_key_signed_zero', B, 'MUST_FAIL',
         res_mut(lambda r, n: [r.obj('result.json').update(residual_diagnostics={'max_abs_residual': 0.0}),
                               n.obj('result.json').update(residual_diagnostics={'max_abs_residual': -0.0})]), ('RESULT',), 'B2')

    def f17(r, n, d):
        r.obj('stages/07_route_a/checkpoint/iteration_0000/COMPLETED.json')['residual'] = 0.0
        n.obj('stages/07_route_a/checkpoint/iteration_0000/COMPLETED.json')['residual'] = -0.0
    case('C_F17_checkpoint_record_signed_zero', Z, 'MUST_FAIL', f17, ('RA_RECORDS',))

    def f18(r, n, d):
        r.obj(ref_fin)['metric'] = 2.0
        n.obj(ref_fin)['metric'] = 2
    case('C_F18_stage_json_float_to_int', B, 'MUST_FAIL', f18, ('STAGES',))
    case('C_F19_result_rows_float_to_int', B, 'MUST_FAIL', res_mut(lambda r, n: n.obj('result.json')['rows'][0].update(speed_km_s=3)), ('RESULT',))
    case('C_F20_result_unlisted_float_to_int', B, 'MUST_FAIL',
         res_mut(lambda r, n: [r.obj('result.json').update(residual_diagnostics={'n_rows': 1.0}), n.obj('result.json').update(residual_diagnostics={'n_rows': 1})]), ('RESULT',))
    case('C_F21_result_verdict_keys_flipped', B, 'MUST_FAIL',
         res_mut(lambda r, n: [r.obj('result.json').update(accepted_for_calibration=True, picard_bound_met=True),
                               n.obj('result.json').update(accepted_for_calibration=False, picard_bound_met=False)]), ('RESULT',), 'B2')
    case('C_F22_result_pass_key_bool_to_int', B, 'MUST_FAIL',
         res_mut(lambda r, n: [r.obj('result.json')['passes'][0].update(rotation_positive=True), n.obj('result.json')['passes'][0].update(rotation_positive=1)]), ('RESULT',))
    case('C_F23_result_route_a_outcome_changed', Z, 'MUST_FAIL',
         res_mut(lambda r, n: n.obj('result.json')['route_a_outcome'].update(classification='NOT_CONVERGED', result_sha256='e' * 64)), ('RESULT',), 'B2')

    def f24(r, n, d):
        a_, b_ = r.obj(ref_req), n.obj(ref_req)
        b_['script'], b_['script_sha256'] = '/x/evil_reference.py', 'c' * 64
        return {'tokens': [[a_['script'], b_['script'], '<S_PATH>'], [a_['script_sha256'], b_['script_sha256'], '<S_SHA>']]}
    case('C_F24_script_swap_hidden_by_declared_token', B, 'MUST_FAIL', f24, ('AUTO_CUSTODY',))

    def f25(r, n, d):
        q = n.obj(ref_req)
        q['script'], q['script_sha256'] = str(drv.SCRIPTS_UVT['body'][0]), drv.SCRIPTS_UVT['body'][1]
    case('C_F25_swap_to_real_entry_of_other_kind', Z, 'MUST_FAIL', f25, ('AUTO_CUSTODY',))

    def f26(r, n, d):
        q = n.obj(ref_req)
        q['script'], q['script_sha256'] = str(drv.SCRIPTS['reference'][0]), drv.SCRIPTS['reference'][1]
    case('C_F26_Z2_reference_runs_plain_base_not_uvt', Z, 'MUST_FAIL', f26, ('SCRIPT_CUSTODY',))

    def f27(r, n, d):
        q = n.obj(ra_req)
        q['script'], q['script_sha256'] = str(drv.NODES_ROUTE_A['worker_parallel'][0]), drv.NODES_ROUTE_A['worker_parallel'][1]
    case('C_F27_route_a_swap_to_nodes_worker', Z, 'MUST_FAIL', f27, ('AUTO_CUSTODY',))
    case('C_F28_new_driver_is_ext_not_selected', B, 'MUST_FAIL',
         lambda r, n, d: n.obj('start.json').update(driver=EXT[0], driver_sha256=EXT[1]), ('AUTO_CUSTODY', 'NEW_DRIVER_PIN'))

    def f29(r, n, d):
        r.obj('start.json').update(driver='/x/galaxy_m0_forward_c2v008.py', driver_sha256='a' * 64)
        return {'tokens': [['/x/galaxy_m0_forward_c2v008.py', m.DRIVER[0], '<D>'], ['a' * 64, m.DRIVER[1], '<DS>']]}
    case('C_F29_undeclared_ref_driver_hidden_by_token', B, 'MUST_FAIL', f29, ('AUTO_CUSTODY',))

    def f30(r, n, d):
        av = n.obj(ra_req)['argv']
        i = av.index('--solver')
        av[i + 1], av[i + 3] = 'X' + av[i + 1], 'f' * 64
    case('C_F30_route_a_solver_not_in_driver_map', Z, 'MUST_FAIL', f30, ('AUTO_CUSTODY',))
    case('C_Q01_inputs_json_content_changed', B, 'MUST_FAIL',
         lambda r, n, d: n.obj('inputs/seed_c2v001.json')['numerical_inputs'].update(source_rtol=0.5), ('FILES_INPUTS',), 'c2v004 PROBE (S3)')

    def q02(r, n, d):
        n.obj('inputs/seed_c2v001.json')['numerical_inputs']['source_rtol'] = 0.5
        for t in (r, n):
            t.obj(ref_req)['argv'] += ['--seed', str(t.root / 'inputs/seed_c2v001.json'), '--seed-sha256', I.sha(I.raw_json(t.obj('inputs/seed_c2v001.json')))]
    case('C_Q02_input_change_cited_by_sha_in_request', B, 'MUST_FAIL', q02, ('FILES_INPUTS',), 'c2v004 PROBE (S3)')
    case('C_Q03_toplevel_finish_changed', B, 'MUST_FAIL', lambda r, n, d: n.obj('finish.json').update(status='FAILED'), ('FILES_TOP',), 'c2v004 PROBE (S3)')

    def q04(r, n, d):
        r.add('stages/07_route_a/attempt_000/result.json', {'outcome': 'CONVERGED_FINITE_FIXED_POINT', 'speeds': [1.0]})
        n.add('stages/07_route_a/attempt_000/result.json', {'outcome': 'NOT_CONVERGED', 'speeds': [9.0]})
    case('C_Q04_route_a_attempt_result_changed', Z, 'MUST_FAIL', q04, ('FILES_ROUTE_A',), 'c2v004 PROBE (S3)')

    def q05(r, n, d):
        av = n.obj(ref_req)['argv']
        n.obj(ref_req)['argv'] = av[:av.index('--uv-tail-config')]
    case('C_Q05_Z2_uvt_stage_without_tail_argv', Z, 'MUST_FAIL', q05, ('REQUEST',), 'c2v004 PROBE (S2)')

    def p01(r, n, d):
        o = n.obj(ref_fin)
        n.files[ref_fin] = ('raw', json.dumps(dict(reversed(list(o.items()))), indent=None).encode())
    case('C_P01_stage_json_key_order_and_format', B, 'MUST_PASS', p01)

    def p02(r, n, d):
        n.files['stages/11_reference/reference/response.npz'] = ('raw', npz_bytes(True, {'matrix': np.arange(12, dtype=np.float64).reshape(3, 4)}))
    case('C_P02_npz_recompressed_same_arrays', B, 'MUST_PASS', p02)

    def p03(r, n, d):
        for rel in list(n.files):
            if rel.startswith('stages/11_reference/'):
                n.files['stages/15_reference/' + rel[len('stages/11_reference/'):]] = n.files.pop(rel)
    case('C_P03_stage_renumbered', B, 'MUST_PASS', p03)

    def p04(r, n, d):
        for t, v in ((r, 1.0), (n, 2.0)):
            t.obj(ref_fin).update(elapsed_seconds=v, utc='T%s' % v)
    case('C_P04_masked_keys_differ', B, 'MUST_PASS', p04)

    def p05(r, n, d):
        for t in (r, n):
            o = dict(t.obj(ref_fin), nan_probe=float('nan'))
            t.files[ref_fin] = ('raw', json.dumps(o, sort_keys=True).encode())
    case('C_P05_nan_equal_both_sides', B, 'MUST_PASS', p05)
    case('C_P06_Z2_declared_successor_swap', Z, 'MUST_PASS', None, (), 'the Z2 baseline is the declared base->SCRIPTS_UVT swap (replace-mode tokens)')

    def p07(r, n, d):
        r.obj('start.json').update(driver=m.DRIVER[0], driver_sha256=m.DRIVER[1])
        r.obj('result.json')['driver_sha256'] = m.DRIVER[1]
        refinish(r)
    case('C_P07_Z2_reference_run_on_selected_driver', Z, 'MUST_PASS', p07)
    case('C_P08_Z2_declared_sidecar_file', Z, 'MUST_PASS', lambda r, n, d: n.add('stages/07_route_a/uv_tail_sidecar/iteration_0000.json', {'x': 1}))

    # ================= group D: own c2v006 canaries =================
    def o01(r, n, d):
        r.obj('result.json')['extra'] = {str(r.root) + '/stages/01_a': 'v'}
        n.obj('result.json')['extra'] = {str(n.root) + '/stages/01_a': 'v', str(n.root) + '/stages/02_a': 'tampered'}
        refinish(r)
        refinish(n)
    case('D_O01_key_collision_stage_number_new_side', B, 'MUST_FAIL', o01, ('NORM_INJECTIVE',), 'CX2-V5-B1 class without marker text')

    def o02(r, n, d):
        for t in (r, n):
            t.obj(ref_fin)['deep'] = [{'x': [{str(t.root) + '/stages/01_a': 1, str(t.root) + '/stages/02_a': 1}]}]
    case('D_O02_symmetric_nested_collision_in_list', B, 'MUST_FAIL', o02, ('NORM_INJECTIVE',), 'equal on both sides yet ambiguous')

    def o03(r, n, d):
        arr = {'q': np.arange(6.0)}
        ua, ub = npz_bytes(False, arr), npz_bytes(True, arr)
        for t in (r, n):
            t.files['stages/11_reference/reference/a.npz'] = ('raw', ua)
            t.files['stages/11_reference/reference/b.npz'] = ('raw', ub)
            t.obj(ref_fin)['by_sha'] = {sha(ua): 1, sha(ub): 2}
    case('D_O03_collision_via_npz_content_equal_hex_keys', B, 'MUST_FAIL', o03, ('NORM_INJECTIVE',))

    def o04(r, n, d):
        r.obj(ref_fin)['where'] = '<RUN>/x'
        n.obj(ref_fin)['where'] = str(n.root) + '/x'
    case('D_O04_raw_normalizer_text_value', B, 'MUST_FAIL', o04, ('NORM_INJECTIVE',), 'value-level form of CX2-V5-B1')

    def o05(r, n, d):
        for t in (r, n):
            t.obj(ref_fin)['<DRIVER_DRIVER>'] = 1
    case('D_O05_raw_key_contains_token_label', B, 'MUST_FAIL', o05, ('NORM_INJECTIVE',))

    def o06(r, n, d):
        o = n.obj(ref_fin)
        txt = json.dumps(dict(o, nest={'k': {'v': 1}}), sort_keys=True).replace('"v": 1', '"v": 2, "v": 1')
        n.files[ref_fin] = ('raw', txt.encode())
        r.obj(ref_fin)['nest'] = {'k': {'v': 1}}
    case('D_O06_duplicate_key_nested_stage_json', B, 'MUST_FAIL', o06, ('STRICT_PARSE',))

    def o07(r, n, d):
        line = json.dumps({'stage': 'reference', 'event': 'start', 'v': 1})
        r.files['progress.jsonl'] = ('raw', (line + '\n').encode())
        n.files['progress.jsonl'] = ('raw', (line.replace('"v": 1', '"v": 9, "v": 1') + '\n').encode())
    case('D_O07_duplicate_key_in_jsonl_line', B, 'MUST_FAIL', o07, ('STRICT_PARSE',))

    def o08(r, n, d):
        txt = I.raw_json(n.obj('inputs/uv_tail_config.json')).decode().replace('"fixture": "CX2"', '"fixture": "X", "fixture": "CX2"')
        n.files['inputs/uv_tail_config.json'] = ('raw', txt.encode())
    case('D_O08_duplicate_key_in_new_only_input', Z, 'MUST_FAIL', o08, ('STRICT_PARSE',), 'a new-only declared file is still strictly parsed')

    def o09(r, n, d):
        raw = n.files['stages/07_route_a/checkpoint/IDENTITY.json'][1]
        n.files['stages/07_route_a/checkpoint/IDENTITY.json'] = ('raw', raw.replace(b'"kind":"identity"', b'"kind":"x","kind":"identity"', 1))
    case('D_O09_duplicate_key_in_checkpoint_identity', Z, 'MUST_FAIL', o09, ('STRICT_PARSE',))

    def o10(r, n, d):
        good = npy_bytes(np.arange(12, dtype=np.float64).reshape(3, 4))
        r.files['stages/11_reference/reference/response.npz'] = ('raw', npz_bytes(raw_members=[('matrix.npy', good)]))
        n.files['stages/11_reference/reference/response.npz'] = ('raw', npz_bytes(raw_members=[('matrix', npy_bytes(np.zeros(2))), ('matrix.npy', good)]))
    case('D_O10_npz_member_without_npy_suffix_same_key', B, 'MUST_FAIL', o10, ('STRICT_PARSE',))

    def o11(r, n, d):
        good = npy_bytes(np.arange(12, dtype=np.float64).reshape(3, 4))
        for t in (r, n):
            t.files['stages/11_reference/reference/response.npz'] = ('raw', npz_bytes(raw_members=[('matrix.npy', good), ('notes.txt', b'hi')]))
    case('D_O11_npz_non_array_member_both_sides', B, 'MUST_FAIL', o11, ('STRICT_PARSE',))

    def o12(r, n, d):
        r.files['stages/11_reference/reference/s.npy'] = ('raw', npy_bytes(np.zeros(2, dtype=[('a', '<f8'), ('b', '<f8')])))
        n.files['stages/11_reference/reference/s.npy'] = ('raw', npy_bytes(np.zeros(2, dtype=[('b', '<f8'), ('a', '<f8')])))
    case('D_O12_structured_field_order_swapped', B, 'MUST_FAIL', o12, ('STAGES',), 'CX2-V5-S1 (names equal as a set, order differs)')

    def o13(r, n, d):
        r.files['stages/11_reference/reference/s.npz'] = ('raw', npz_bytes(False, {'s': np.zeros(2, dtype=np.dtype([('a', 'u1'), ('b', '<f8')], align=False))}))
        n.files['stages/11_reference/reference/s.npz'] = ('raw', npz_bytes(False, {'s': np.zeros(2, dtype=np.dtype([('a', 'u1'), ('b', '<f8')], align=True))}))
    case('D_O13_structured_aligned_vs_packed_npz', B, 'MUST_FAIL', o13, ('STAGES',))

    def o14(r, n, d):
        b = npy_bytes(np.arange(3.0))
        r.files['stages/11_reference/reference/t.npy'] = ('raw', b)
        n.files['stages/11_reference/reference/t.npy'] = ('raw', b + b'\x00')
    case('D_O14_npy_trailing_bytes', B, 'MUST_FAIL', o14, ('STAGES',))

    def o15(r, n, d):
        r.files['stages/11_reference/reference/v.npy'] = ('raw', npy_bytes(np.arange(4.0)))
        n.files['stages/11_reference/reference/v.npy'] = ('raw', npy_bytes(np.asfortranarray(np.arange(4.0))))
    case('D_O15_1d_array_order_flag_irrelevant', B, 'MUST_PASS', o15, (), '1-D arrays are written fortran_order False either way')

    def o16(r, n, d):
        z = np.arange(6.0).reshape(2, 3)
        r.files['stages/11_reference/reference/v.npy'] = ('raw', npy_bytes(np.array(z, order='C')))
        n.files['stages/11_reference/reference/v.npy'] = ('raw', npy_bytes(np.array(z, order='F')))
    case('D_O16_npy_2d_C_vs_F', B, 'MUST_FAIL', o16, ('STAGES',), 'ARRAY_POLICY: storage order is part of identity')

    def o17(r, n, d):
        for t in (r, n):
            t.obj(ra_req)['argv'][:0] = ['--column-workers', '8']
    case('D_O17_duplicate_argv_flag_read_by_name', Z, 'MUST_FAIL', o17, ('NO_LAST_WINS',), 'A71')

    def o18(r, n, d):
        for t in (r, n):
            rq = dict(t.obj(ref_req), exit_code=0)
            t.obj('result.json')['stage_records'] = [rq, copy.deepcopy(rq)]
            refinish(t)
    case('D_O18_duplicate_stage_records_name', B, 'MUST_FAIL', o18, ('STAGE_RECORDS', 'NO_LAST_WINS'), 'A71')

    def o19_patch(mod, r, n):
        orig = mod.stray_uv_tail
        target = n.root / ref_fin

        def wrapped(tree, S):
            if S.tag == 'new' and target.is_file():
                with open(target, 'r+b') as f:  # in-place change after the comparator read it (fault injection)
                    b = f.read()
                    f.seek(0)
                    f.write(b.replace(b'0.25', b'0.75', 1))
            return orig(tree, S)
        mod.stray_uv_tail = wrapped
        return {'stray_uv_tail': orig}
    case('D_O19_tree_stable_fault_injection', B, 'MUST_FAIL', None, ('TREE_STABLE',), 'file changed after its single read', patch=o19_patch)
    case('D_O20_token_reference_raw_paired_twice', B, 'MUST_FAIL',
         lambda r, n, d: {'tokens': [['alpha_raw', 'beta_raw', '<T1>'], ['alpha_raw', 'gamma_raw', '<T2>']]}, ('NORM_INJECTIVE',), 'A71 tokens')
    case('D_O21_token_label_used_for_two_pairs', B, 'MUST_FAIL',
         lambda r, n, d: {'tokens': [['alpha_raw', 'beta_raw', '<T1>'], ['delta_raw', 'eps_raw', '<T1>']]}, ('NORM_INJECTIVE',), 'A71 tokens')
    case('D_O22_tokens_file_duplicate_json_key', B, 'MUST_REFUSE',
         lambda r, n, d: {'tokens_raw': b'{"declared": [], "declared": [["a", "b", "<T>"]]}'}, (), 'A71: the tokens file parse refuses')

    def o23(r, n, d):
        for t in (r, n):
            t.obj('stages/07_route_a/checkpoint/iteration_0000/COMPLETED.json')['identity_sha256'] = 'a' * 64
    case('D_O23_hexmap_two_identity_shas_one_token', Z, 'MUST_FAIL', o23, ('NORM_INJECTIVE',))

    def o24(r, n, d):
        r.obj('result.json')['extra'] = {str(r.root) + '/stages/01_a': 1, str(r.root) + '/stages/02_a': 1}
        n.obj('result.json')['extra'] = {str(n.root) + '/stages/01_a': 1}
        refinish(r)
        refinish(n)
    case('D_O24_reference_side_only_collision', B, 'MUST_FAIL', o24, ('NORM_INJECTIVE',))
    case('D_O25_request_not_an_object_exception_path', B, 'MUST_FAIL',
         lambda r, n, d: n.files.__setitem__(ref_req, ('raw', b'[1, 2]')), ('COMPARATOR_EXCEPTION',), 'own hardening: a FAIL report, not a crash')

    def o26(r, n, d):
        txt = json.dumps(r.obj(ref_fin), sort_keys=True).replace('"status": "SYNTHETIC_REFERENCE"', '"status": "SYNTHETIC_REFERENCE", "status": "SYNTHETIC_REFERENCE"')
        n.files[ref_fin] = ('raw', txt.encode())
    case('D_O26_duplicate_key_equal_values', B, 'MUST_FAIL', o26, ('STRICT_PARSE',), 'no last-wins even when values agree')

    def o27(r, n, d):
        good = npy_bytes(np.arange(12, dtype=np.float64).reshape(3, 4))
        n.files['stages/11_reference/reference/response.npz'] = ('raw', npz_bytes(raw_members=[('matrix.npy', good), ('matrix.npy', good)]))
    case('D_O27_duplicate_npz_member_identical_payloads', B, 'MUST_FAIL', o27, ('STRICT_PARSE',))

    def o28(r, n, d):
        for t in (r, n):
            t.obj(ref_fin)['sibling'] = str(t.root) + 'X/y'
    case('D_O28_run_root_prefix_not_a_boundary', B, 'MUST_FAIL', o28, ('STAGES',), 'a longer sibling path is not the run root')

    def o29(r, n, d):
        blob = {'same': True}
        for t in (r, n):
            t.add('stages/11_reference/reference/c1.json', blob)
            t.add('stages/11_reference/reference/c2.json', blob)
            t.obj(ref_fin)['cites'] = I.sha(I.raw_json(blob))
    case('D_O29_identical_json_files_cited_by_sha', B, 'MUST_PASS', o29, (), 'a sha naming two files maps to the joined token on both sides')

    def o30(r, n, d):
        for t in (r, n):
            t.obj('result.json')['extra'] = {'plain/x': 'same'}
            refinish(t)
    case('D_O30_cx2_source_audit_control_plain_key', B, 'MUST_PASS', o30, (), 'the CX2 whole-gate positive control without raw normalizer text')

    summ = {'must_pass': [sum(1 for r in rows if r['expect'] == 'MUST_PASS' and r['ok']), sum(1 for r in rows if r['expect'] == 'MUST_PASS')],
            'must_fail': [sum(1 for r in rows if r['expect'] == 'MUST_FAIL' and r['ok']), sum(1 for r in rows if r['expect'] == 'MUST_FAIL')],
            'must_refuse': [sum(1 for r in rows if r['expect'] == 'MUST_REFUSE' and r['ok']), sum(1 for r in rows if r['expect'] == 'MUST_REFUSE')],
            'breaches': [r['case'] for r in rows if not r['ok']]}
    rep = {'schema': 'CANARIES_C2V006_V001', 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'driver': a.driver,
           'comparator': {'path': str(Path(a.comparator).resolve()), 'sha256': a.sha256,
                          'sha256_at_end': sha(Path(a.comparator).read_bytes())},
           'harness': {'path': str(Path(__file__).resolve()), 'sha256': sha(Path(__file__).read_bytes())},
           'fixture': {'path': str(INV), 'sha256': sha(INV.read_bytes())}, 'rows': rows, 'summary': summ}
    with open(out / 'CANARIES_C2V006.json', 'x') as f:
        json.dump(rep, f, indent=1)
    print(json.dumps(summ))


if __name__ == '__main__':
    main()

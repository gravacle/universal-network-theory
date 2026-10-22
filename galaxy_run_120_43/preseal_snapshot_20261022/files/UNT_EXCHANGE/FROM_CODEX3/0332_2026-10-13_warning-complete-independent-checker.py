"""SOURCE ONLY. Root executes complete37-file/11-call diagnostic saved review.
No NumPy import, matmul or eigh. Both helpers are distinct Code3 checker source.
CLI --archive ABS --producer-spec ABS --producer-spec-sha256 SHA
    --producer-job ABS --output FRESH_ABS_DIRECTORY.
"""
import argparse
import ast
import hashlib
import json
import math
from pathlib import Path
import resource
import struct
import sys
import time
from types import SimpleNamespace

EX = Path('/Users/bgm/Research/UNT_EXCHANGE')
ROOT = EX/'KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001'
OUT = EX/'FROM_CODEX3'
WORKER = EX/'lanes/P49_CODEX2/p49_backend_warning_diagnostic_worker_v002.py'
WORKER_SHA = '88f11c52dbacd727d8679799f00c9a2343c7264c88eb1a42cf1201e0e320d347'
HELPERS = {
    'math': (OUT/'0330_2026-10-13_warning-independent-binary-math.py', '605d6476f7a53d5f91b1bf99d7bbcb428b99c433c1745c35dcf822b308b1caba'),
    'custody': (OUT/'0331_2026-10-13_warning-independent-custody.py', '6fab6cd9636fca18463fe158f0da7b1641e51ff9fe3276e4a52c4220edfb5f47')}
EXTRAS = {
    'survey': {'path': str(EX/'lanes/P49_SPECTRAL_CODEX3/owned_runtime_inventory_v001.py'), 'bytes': 5114, 'sha256': 'f6ada63431a5cde326532307068e15a453c299dd8500e18f64c4596dc59625d0'},
    'prospect': {'path': str(EX/'lanes/P49_CODEX2/P49_BACKEND_WARNING_PROSPECT_V002.txt'), 'bytes': 6073, 'sha256': '52f0b5a5d037e4edc9aead622590c7e4f789a6db9f43d7376b3da61a258e89fb'},
    'c153': {'path': str(ROOT/'P49_SPECTRAL_NATIVE_FLOAT_COMPARISON_ACCEPTANCE_V001.json'), 'bytes': 2486, 'sha256': '48405948dd46eef4253146dc08f97017e3c6759f452d2548bbcabf150626a522'},
    'producer_stderr': {'path': str(ROOT/'P49_SPECTRAL_NATIVE_RUN_V001/P49spectralnative/stderr.log'), 'bytes': 2767, 'sha256': 'be435742be49a4aa143da75f476fbd6f308394db0f7319f4ff8ee1fc63410086'},
    'checker_stderr': {'path': str(ROOT/'ROOT_NATIVE_SPECTRAL_CHECKER_G1_PRODUCERS_RUN_V001/P49spectralnativecheck/stderr.log'), 'bytes': 3974, 'sha256': '6f349da39ea0618651555c1b7ee0b115c4a51ec4d404b3468d944857ffaaf950'}}
V_PIN = {'path': str(ROOT/'P49_SPECTRAL_NATIVE_OUTPUT_V001/ALL_EIGENVECTORS.npy'), 'sha256': '690ee75633a58e7f76f4b29462f6a502bd8d1d207e3f00f2e0e763e8236bb301', 'bytes': 1741226112}
E_PIN = {'path': str(ROOT/'P49_SPECTRAL_NATIVE_OUTPUT_V001/SHIFTED_EIGENVALUES.npy'), 'sha256': '5ae2b69e3ddf16e41b663e269e532def903f80d42b9bdf06eab203ece04dcf32', 'bytes': 83584}
ROLE = 'P49_BACKEND_WARNING_DIAGNOSTIC_V001'
CAPS = {'cpu': 1, 'rss_bytes': 8*2**30, 'seconds': 300, 'output_bytes': 128*2**20, 'scientific_reserve_bytes': 112*2**20}
POLICY = {'divide': 'warn', 'over': 'warn', 'under': 'ignore', 'invalid': 'warn'}
FILES = {'START.json', 'ROOT_CONFIG.json', 'SOURCE_SNAPSHOTS.json', 'GATE_SNAPSHOT.json',
         'INPUT_PINS.json', 'ORIGINAL_WARNINGS.json', 'RUNTIME_INITIAL.json', 'EXACT_SIX_CELLS.json',
         'RESULTS.json', 'RUNTIME_FINAL.json', 'FINISH.json'} | {
         'CONTROL_%02d_%s.json' % (i, e) for i in range(9) for e in ('PRE', 'RETURN')} | {
         'GRAM_%02d_%s' % (i, e) for i in (9, 10) for e in ('LEFT.npy', 'PRE.json', 'RESULT.npy', 'RETURN.json')}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--producer-spec', type=Path, required=True)
    parser.add_argument('--producer-spec-sha256', required=True)
    parser.add_argument('--producer-job', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    def guard():
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024)
        if time.monotonic()-started > 300 or rss > 8*2**30:
            raise ValueError('complete independent checker300s8GiB cap')
    modules, helper_raw = {}, {}
    for label, (p, sha) in HELPERS.items():
        if p.resolve() != p or p.is_symlink() or p.stat().st_size > 65536:
            raise ValueError('literal bounded independent helper')
        raw = p.read_bytes()
        if hashlib.sha256(raw).hexdigest() != sha:
            raise ValueError('independent helper source pin')
        helper_raw[label] = raw
        ns = {'__name__': 'root_warning_distinct_'+label, '__file__': str(p)}
        exec(compile(raw, str(p), 'exec'), ns)
        modules[label] = SimpleNamespace(**ns)
    H, C = modules['math'], modules['custody']
    need, exact, decode = C.need, C.exact, C.decode
    I = C.Inputs(guard)
    for label, (p, sha) in HELPERS.items():
        I.read(p, sha, 65536)
    I.read(Path(__file__).resolve(), cap=65536)
    root = args.archive
    need(root.is_absolute() and root.resolve() == root and not root.is_symlink()
         and ROOT in root.parents and root.is_dir(), 'literal original scientific archive')
    need({p.name for p in root.iterdir()} == FILES, 'complete37-file diagnostic success census')
    output = args.output
    need(output.is_absolute() and output.resolve() == output and not output.exists()
         and ROOT in output.parents, 'fresh root-owned checker output')
    data, filemeta = {}, {}
    for name in sorted(FILES):
        raw = I.read(root/name, cap=112*2**20, retain=name.endswith('.json'))
        pin = I.pins[str(root/name)]
        filemeta[name] = {'bytes': pin['bytes'], 'sha256': pin['sha256']}
        if name.endswith('.json'):
            data[name] = decode(raw)
    totalbytes = sum(v['bytes'] for v in filemeta.values())
    need(totalbytes <= 112*2**20, 'whole112MiB scientific cap')
    workerraw = I.read(WORKER, WORKER_SHA, 65536)
    workerpin = I.pins[str(WORKER)]
    small = {k: I.pin(p, cap=2*2**20) for k, p in EXTRAS.items()}
    I.pin(V_PIN, False)
    I.pin(E_PIN, False, 1 << 20)
    cfg = data['ROOT_CONFIG.json']
    need(set(cfg) == {'schema', 'role', 'released_by', 'execute', 'output', 'caps', 'source_gate', 'original_namespace_custody'}, 'closed root config')
    need(cfg['schema'] == 'P49_BACKEND_WARNING_RELEASE_V001' and cfg['role'] == ROLE and cfg['released_by'] == '/root'
         and cfg['execute'] is True and cfg['output'] == str(root), 'literal root release')
    exact(cfg['caps'], CAPS, 'frozen caps')
    inputlist = data['INPUT_PINS.json']['all_original_full_files']
    need(type(inputlist) is list and len(inputlist) == 11, 'entire worker opening11 input files')
    configpin = inputlist[0]
    need(Path(configpin['path']).parent == ROOT, 'original root-owned config')
    exact(decode(I.pin(configpin, cap=2*2**20)), cfg, 'original config bytes')
    sourcegate = decode(I.pin(cfg['source_gate'], cap=2*2**20))
    custody = decode(I.pin(cfg['original_namespace_custody'], cap=2*2**20))
    for k in ('source_gate', 'original_namespace_custody'):
        need(Path(cfg[k]['path']).parent == ROOT, 'root-owned original gate')
    need(sourcegate['acceptor'] == '/root' and sourcegate['reviewer_id'] != 'Codex2'
         and str(sourcegate['status']).startswith('PASS') and sourcegate['role'] == ROLE
         and sourcegate['worker_sha256'] == WORKER_SHA, 'distinct actual worker source acceptance')
    need(custody['acceptor'] == '/root' and str(custody['status']).startswith('PASS')
         and custody['c153'] == EXTRAS['c153'] and custody['complete_original_opening_checked'] is True
         and custody['complete_original_closing_root_obligation'] is True, 'root whole original namespace gate')
    opening_paths = [configpin['path'], cfg['source_gate']['path'], cfg['original_namespace_custody']['path'], str(WORKER)]
    opening_paths += [p['path'] for p in EXTRAS.values()]+[V_PIN['path'], E_PIN['path']]
    exact(data['INPUT_PINS.json'], {'all_original_full_files': [I.pins[p] for p in opening_paths],
                                  'original_closing_namespace_root_required': True}, 'complete worker opening pin census')
    exact(data['SOURCE_SNAPSHOTS.json'], {'worker': workerraw.decode(), 'survey': small['survey'].decode(),
                                        'prospect': small['prospect'].decode()}, 'whole raw source snapshots')
    exact(data['GATE_SNAPSHOT.json'], {'source': sourcegate, 'original_custody': custody}, 'whole original gate snapshots')
    exact(data['ORIGINAL_WARNINGS.json'], {'producer_stderr': small['producer_stderr'].decode(),
          'checker_stderr': small['checker_stderr'].decode(), 'disposition': 'UNRESOLVED_ORIGINAL_LOGS_PRESERVED'}, 'original full warning logs')
    pid = data['START.json']['pid']
    need(type(pid) is int and pid > 0, 'original PID syntax')
    exact(data['START.json'], {'schema': ROLE, 'pid': pid, 'caps': CAPS, 'executor': '/root',
          'scientific_acceptance': False, 'external_supervisor_required': True}, 'START')
    original, child_end, stderr, runtime_receipt = C.runtime(I,
          {'path': str(args.producer_spec), 'sha256': args.producer_spec_sha256}, args.producer_job,
          root, {'path': configpin['path'], 'sha256': configpin['sha256']}, WORKER, WORKER_SHA, pid, totalbytes)
    C.inventory_checks(data['RUNTIME_INITIAL.json'], data['RUNTIME_FINAL.json'], original, pid, child_end)
    warning_lines = [n.lineno for n in ast.walk(ast.parse(workerraw)) if isinstance(n, ast.Call)
                     and isinstance(n.func, ast.Attribute) and n.func.attr == 'matmul']
    need(len(warning_lines) == 1, 'unique pinned actual matmul callsite')
    warning_line = warning_lines[0]
    allwarnings, cases = [], []
    stderr_position = 0
    def warnings_for(name, values):
        nonlocal stderr_position
        need(type(values) is list and len(values) <= 100, 'bounded complete actual warning events')
        for row in values:
            need(set(row) == {'category', 'message', 'filename', 'lineno'}
                 and type(row['message']) is str and row['category'] == 'RuntimeWarning'
                 and row['filename'] == str(WORKER) and row['lineno'] == warning_line,
                 'actual warning category/location bound to pinned caller')
            text = '%s:%d: %s: %s\n  %s\n' % (row['filename'], row['lineno'], row['category'],
                    row['message'], workerraw.decode().splitlines()[warning_line-1].strip())
            found = stderr.find(text.encode(), stderr_position)
            need(found >= 0, 'every captured warning retained in actual original stderr order')
            stderr_position = found+len(text.encode())
            allwarnings.append({'call': name, **row})
        cases.append({'name': name, 'return_file': name+'_RETURN.json', 'warning_count': len(values)})
    tiny_meta = {'shape': [2, 2], 'dtype': '<c16', 'strides': [32, 16], 'C_contiguous': True, 'F_contiguous': False, 'nbytes': 64}
    matrices = [('identity', [1+0j, 0j, 0j, 1+0j]), ('zero', [0j]*4), ('Hermitian_rank1', [1+0j, 1j, -1j, 1+0j])]
    for i in range(9):
        label, matrix = matrices[i//3]
        name = 'CONTROL_%02d' % i
        operand = struct.pack('<8d', *[v for z in matrix for v in (z.real, z.imag)])
        pre, ret = data[name+'_PRE.json'], data[name+'_RETURN.json']
        exact(pre, {'case': label, 'repeat': i%3, 'operation': 'A@A', 'left': tiny_meta, 'right': tiny_meta,
                    'left_complete_C_bytes_hex': operand.hex(), 'right_complete_C_bytes_hex': operand.hex(),
                    'numpy_error_policy': POLICY}, name+'/wholePRE')
        result_bytes = bytes.fromhex(ret['output_complete_C_bytes_hex'])
        need(result_bytes.hex() == ret['output_complete_C_bytes_hex'], 'canonical full actual result hex')
        H.tiny(operand, result_bytes, i//3)
        warnings_for(name, ret['warnings'])
        exact(ret, {'exception': None, 'case': label, 'repeat': i%3, 'output': tiny_meta,
                    'output_complete_C_bytes_hex': result_bytes.hex(), 'all_output_finite': True,
                    'warnings': ret['warnings'], 'numpy_error_policy_after': POLICY}, name+'/wholeRETURN')
    print(json.dumps({'independent_progress': 'NINE_FULL_EXACT_TINY_PRODUCTS_COMPLETE'}), flush=True)
    opened_arrays = []
    try:
        V = H.Npy(V_PIN['path'], (10432, 10432), '<c16'); opened_arrays.append(V)
        E = H.Npy(E_PIN['path'], (10432,), '<f8'); opened_arrays.append(E)
        need(not V.fortran, 'original complete C-order V')
        vhash = V.scan(guard, bound=2)
        E.scan(guard)
        ev = [z[0] for z in struct.iter_unpack('<d', E.data[E.offset:])]
        need(ev == sorted(ev), 'all original eigenvalues ordered')
        products = []
        for i, label in ((9, 'MAPPED_ORIGINAL'), (10, 'FULL_C_COPY')):
            name = 'GRAM_%02d' % i
            left = H.Npy(root/(name+'_LEFT.npy'), (128, 10432), '<c16'); opened_arrays.append(left)
            result = H.Npy(root/(name+'_RESULT.npy'), (128, 10432), '<c16'); opened_arrays.append(result)
            H.verify_left(V, left, guard)
            result.scan(guard)
            lpin = {'file': name+'_LEFT.npy', 'shape': [128, 10432], 'dtype': '<c16', **filemeta[name+'_LEFT.npy']}
            rpin = {'file': name+'_RESULT.npy', 'shape': [128, 10432], 'dtype': '<c16', **filemeta[name+'_RESULT.npy']}
            exact(data[name+'_PRE.json'], {'case': label, 'operation': 'conj(V[:,:128]).T @ V',
                  'left': left.meta(), 'actual_complete_left_array': lpin, 'right': V.meta(),
                  'complete_right_original_pin': V_PIN, 'complete_right_data_sha256': vhash,
                  'all_copy_bytes_equal_original': True, 'numpy_error_policy': POLICY,
                  'buffer_comparison_not_distinct_stride_class': True}, name+'/wholePRE')
            ret = data[name+'_RETURN.json']
            warnings_for(name, ret['warnings'])
            exact(ret, {'exception': None, 'case': label, 'output': result.meta(), 'actual_complete_result_array': rpin,
                        'all_output_finite': True, 'warnings': ret['warnings'], 'numpy_error_policy_after': POLICY}, name+'/wholeRETURN')
            products.append(result)
            print(json.dumps({'independent_progress': 'COMPLETE_LEFT_BITS_AND_RESULT_CENSUS', 'call': name}), flush=True)
        six = H.six_cells(V, products, guard)
        exact(data['EXACT_SIX_CELLS.json'], six, 'every exact full-summand dot/model/discrepancy field')
    finally:
        for a in reversed(opened_arrays):
            a.close()
    compatible = all(c['within_stated_scalar_model_envelope'] for r in six['cells'] for c in r['all_two_actual_products'])
    disposition = ('SELECTED_CELL_SCALAR_MODEL_ENVELOPE_EXCEEDED' if not compatible else
                   'WARNINGS_REPRODUCED_SELECTED_CELL_COMPARISONS_ONLY' if allwarnings else
                   'MATMUL_WARNINGS_NOT_REPRODUCED_THIS_FROZEN_CALL_SEQUENCE')
    exact(data['RESULTS.json'], {'schema': 'P49_BACKEND_WARNING_DIAGNOSTIC_RESULT_V001', 'cases': cases,
          'all_captured_matmul_warning_events': allwarnings, 'all_eleven_matmul_calls_complete': True,
          'six_exact_cell_comparisons_complete': True, 'selected_cells_scalar_model_compatible': compatible,
          'disposition': disposition, 'original_warning_disposition_resolved': False,
          'whole_Gram_arithmetic_certified': False, 'eigh_rerun': False, 'exact_DE_certified': False,
          'physical_release': False}, 'wholeRESULTS')
    exact(data['FINISH.json'], {'schema': 'P49_BACKEND_WARNING_DIAGNOSTIC_FINISH_V001', 'pid': pid,
          'all_opened_full_input_closing_pins_match': True,
          'files_before_finish': {k: v for k, v in filemeta.items() if k != 'FINISH.json'},
          'status': 'RAW_DIAGNOSTIC_REQUIRES_DISTINCT_COMPLETE_SAVED_REVIEW',
          'whole_original_namespace_closing_by_root_required': True,
          'original_warning_disposition_resolved': False, 'physical_release': False}, 'wholeFINISH')
    need({p.name for p in root.iterdir()} == FILES, 'closing whole scientific file census')
    I.close()
    guard()
    report = {'schema': 'P49_WARNING_COMPLETE_INDEPENDENT_SAVED_REVIEW_V001',
              'status': 'PASS_COMPLETE_DIAGNOSTIC_PENDING_ROOT_ORIGINAL_NAMESPACE_ADJUDICATION',
              'source_author': 'Codex2', 'checker_author': 'Codex3', 'self_review': False,
              'archive': str(root), 'all37_scientific_files': filemeta, 'all11_calls_compared': True,
              'all9_exact_tiny_products_compared': True, 'all_actual_left_operand_bits_compared': True,
              'full_Gram_arrays_preserved_finite_and_custody_checked': True, 'six_complete_exact_dots': six,
              'complete_new_runtime': runtime_receipt, 'all_captured_warnings': allwarnings,
              'selected_cells_scalar_model_compatible': compatible, 'disposition': disposition,
              'all_opened_complete_input_closing_pins_match': True, 'complete_checker_input_pins': I.pins,
              'independent_math': 'Raw IEEE754 integer units2^-1074, exact integer dot accumulation, rational scalar-envelope algebra; no NumPy oracle',
              'full_right_copy_identity_basis': 'Complete originalV retained; producer source checks every copied byte, full PRE datahash independently verified',
              'dynamic_owned_inventory_scope': 'Recorded full producer telemetry bound to actual PID/runtime; no host-global inventory claim',
              'original_warning_disposition_resolved': False, 'whole_Gram_arithmetic_certified': False,
              'eigh_rerun': False, 'exact_DE_certified': False, 'physical_release': False}
    raw = (json.dumps(report, sort_keys=True, separators=(',', ':'), allow_nan=False)+'\n').encode()
    need(len(raw) <= 16*2**20, 'complete checker report reserve')
    output.mkdir(exist_ok=False)
    import os
    with (output/'INDEPENDENT_REPORT.json').open('xb') as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    print(json.dumps({'status': report['status'], 'report_bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
                      'warning_events': len(allwarnings), 'disposition': disposition}), flush=True)


if __name__ == '__main__':
    main()

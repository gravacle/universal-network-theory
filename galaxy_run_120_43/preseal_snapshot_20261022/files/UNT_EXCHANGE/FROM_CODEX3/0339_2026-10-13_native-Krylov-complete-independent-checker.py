"""SOURCE ONLY. Root-only complete13-file saved native feasibility checker.
CLI --archive ORIGINAL_ABS --output FRESH_ABS_DIRECTORY.
Candidate Decimal values are untrusted saved operands, not regenerated here.
Every exact certificate/H/state field independently reconstructed; root binds
actual caller/PID/runtime and complete historical namespaces separately.
"""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import struct
import sys
import time
from types import SimpleNamespace

EX = Path('/Users/bgm/Research/UNT_EXCHANGE')
B = EX/'KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001'
O = EX/'FROM_CODEX3'
CALLER = EX/'lanes/P49_CODEX2/shared_krylov_native_one_step_caller_v001.py'
CALLER_SHA = 'f0a3595da2a45ccf1569ec947a3c82591c0bc9a6da124ddf0b3afc7c40c566a7'
CONTRACT = EX/'lanes/P49_CODEX2/SHARED_KRYLOV_NATIVE_ONE_STEP_CONTRACT_V001.txt'
CONTRACT_SHA = '425ca1118596b209416cc4b9d7fd87e9e09d0e54b2a67e6cef0eefd85655fba6'
HELPERS = {
    'custody': (O/'0331_2026-10-13_warning-independent-custody.py', '6fab6cd9636fca18463fe158f0da7b1641e51ff9fe3276e4a52c4220edfb5f47'),
    'native': (O/'0336_2026-10-13_native-Krylov-independent-H.py', 'c65b7c6ad4b4cd41a9ef31c45eeae3c282600b3f4207f9173e80a017f8ad9985'),
    'certificate': (O/'0337_2026-10-13_native-Krylov-independent-integer-certificate.py', 'c7096f7bcea6a75e726fa82ea2e78859228bc7f0346393aeddc05b2f242f623f'),
    'pins': (O/'0338_2026-10-13_native-Krylov-frozen-checker-pins.py', '54c9d635a82703beffdc1e571fa3a361ff8f0f009b16f4f7745720116ca623a0')}
ROLE = 'SHARED_KRYLOV_NATIVE_FEASIBILITY_V001'
CAPS = {'cpu': 1, 'rss_bytes': 8*2**30, 'seconds': 600, 'output_bytes': 128*2**20, 'scientific_reserve_bytes': 120*2**20}
FILES = {'START.json', 'ROOT_CONFIG.json', 'SOURCE_SNAPSHOTS.json', 'GATE_SNAPSHOTS.json', 'INPUT_PINS.json',
         'NATIVE_BINDING.json', 'CANDIDATE_PRE.json', 'CANDIDATE_RETURN.json', 'CERTIFICATE_PRE.json',
         'CERTIFICATE_RETURN.json', 'RESULTS.json', 'INPUT_MANIFEST.json', 'FINISH.json'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    def guard():
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024)
        if time.monotonic()-started > 600 or rss > 8*2**30:
            raise ValueError('whole independent600s8GiB feasibility checker cap')
    modules = {}
    for label, (path, sha) in HELPERS.items():
        if path.resolve() != path or path.is_symlink() or path.stat().st_size > 65536:
            raise ValueError('plain bounded independent checker helper')
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != sha:
            raise ValueError('literal checker helper pin')
        ns = {'__name__': 'root_native_distinct_'+label, '__file__': str(path)}
        exec(compile(raw, str(path), 'exec'), ns)
        modules[label] = SimpleNamespace(**ns)
    C, N, M, P = (modules[k] for k in ('custody', 'native', 'certificate', 'pins'))
    need, exact, decode = C.need, C.exact, C.decode
    I = C.Inputs(guard)
    for path, sha in HELPERS.values():
        I.read(path, sha, 65536)
    I.read(Path(__file__).resolve(), cap=65536)
    I.read(CONTRACT, CONTRACT_SHA, 65536)
    root, output = args.archive, args.output
    need(root.is_absolute() and root.resolve() == root and not root.is_symlink()
         and root.is_dir() and B in root.parents, 'literal original root scientific archive')
    need({p.name for p in root.iterdir()} == FILES, 'all13 successful scientific files, no partial-prefix acceptance')
    need(output.is_absolute() and output.resolve() == output and not output.exists()
         and B in output.parents, 'fresh root-owned checker output')
    data, filemeta = {}, {}
    for name in sorted(FILES):
        raw = I.read(root/name, cap=120*2**20)
        data[name] = decode(raw)
        rec = I.pins[str(root/name)]
        filemeta[name] = {'bytes': rec['bytes'], 'sha256': rec['sha256']}
    need(sum(v['bytes'] for v in filemeta.values()) <= 120*2**20, 'entire scientific output reserve')
    producer_paths = []
    def producer_pin(pin, cap=32*2**20):
        raw = I.pin(pin, cap=cap)
        if pin['path'] not in producer_paths:
            producer_paths.append(pin['path'])
        return raw
    configpin = data['START.json']['config']
    need(Path(configpin['path']).parent == B, 'literal root-owned original config')
    cfg = decode(producer_pin(configpin, 2*2**20))
    exact(data['ROOT_CONFIG.json'], cfg, 'entire original config snapshot')
    need(set(cfg) == {'schema', 'role', 'released_by', 'execute', 'output', 'caps', 'source_gate', 'original_namespace_custody'}, 'closed one-step root config')
    need(cfg['schema'] == 'SHARED_KRYLOV_ONE_STEP_RELEASE_V001' and cfg['role'] == ROLE
         and cfg['released_by'] == '/root' and cfg['execute'] is True and cfg['output'] == str(root), 'actual frozen one-step release')
    exact(cfg['caps'], CAPS, 'same declared wholecaps')
    callerraw = producer_pin({'path': str(CALLER), 'sha256': CALLER_SHA}, 65536)
    gates = {}
    for key in ('source_gate', 'original_namespace_custody'):
        need(Path(cfg[key]['path']).parent == B, 'root-owned exact gate')
        gates[key] = decode(producer_pin(cfg[key], 2*2**20))
    exact(data['GATE_SNAPSHOTS.json'], gates, 'complete gate snapshots')
    sg, cg = gates['source_gate'], gates['original_namespace_custody']
    need(sg['acceptor'] == '/root' and str(sg['status']).startswith('PASS') and sg['role'] == ROLE, 'actual distinct source gate')
    exact(sg['source_pins'], P.SOURCES, 'every caller helper source pin')
    matched = [r for r in sg['allowed_runners'] if r['path'] == str(CALLER) and r['sha256'] == CALLER_SHA and r['role'] == 'feasibility']
    need(len(matched) == 1 and matched[0]['source_author'] == 'Codex2'
         and matched[0]['reviewer_id'] != 'Codex2', 'distinct actual complete caller review')
    need(cg['acceptor'] == '/root' and str(cg['status']).startswith('PASS') and cg['role'] == ROLE
         and cg['complete_original_opening_checked'] is True and cg['complete_original_closing_root_obligation'] is True,
         'whole original namespace custody gate')
    exact(cg['input_pins'], P.INPUTS, 'frozen entire original input scope')
    exact(data['INPUT_PINS.json'], P.INPUTS, 'all initial literal input pins')
    rawinputs = {k: producer_pin(pin) for k, pin in P.INPUTS.items()}
    controls = decode(rawinputs['controls'])
    need(controls['acceptor'] == '/root' and controls['status'] == 'PASS_COMPLETE_EXACT_CONTROLS'
         and controls['all8_calls_all16_events_exactly_compared'] is True
         and controls['all20_scientific_files_compared'] is True and controls['complete_original_runtime_custody'] is True,
         'actual accepted C161 complete controls')
    ig = decode(rawinputs['original_input_gate'])
    need(ig['acceptor'] == '/root' and str(ig['status']).startswith('PASS')
         and ig['all_original_namespaces_authenticated'] is True
         and ig['all_original_closing_pins_root_obligation'] is True, 'C150/C153 whole root input qualification')
    for name in ('c150', 'c153', 'packet'):
        need(ig[name]['path'] == P.INPUTS[name]['path'] and ig[name]['sha256'] == P.INPUTS[name]['sha256'], 'unchanged accepted native ancestry')
    c150 = decode(rawinputs['c150'])
    oldaudit = decode(producer_pin(c150['audit']))
    closures = ig['original_archive_closures']
    bypath = {v['path']: v for v in closures}
    need(len(closures) == len(bypath) == 39 and set(bypath) == set(oldaudit['complete_archives']), 'all39 original archives')
    for rec in c150['records']:
        for field in ('producer_closure', 'reader_closure'):
            need(bypath[rec[field]['path']]['sha256'] == rec[field]['sha256'], 'literal original final-stage closures')
    for pin in closures:
        value = decode(producer_pin(pin))
        need(value['returncode'] == 0 and value['cap_stop'] is None and value['all_opening_pins_checked'] is True
             and value['all_closing_pins_match'] is True, 'whole successful original closure')
    exact(ig['journals']['OLD_CARRIER_SITE0:0'], {'journal': P.INPUTS['initial_journal'],
          'closure': P.INPUTS['initial_closure']}, 'original pilot namespace binding')
    closure = decode(rawinputs['initial_closure'])
    for key, basename in (('initial_journal', 'OPERANDS.jsonl'), ('initial_vector', 'STEP_000_left.bin')):
        pin = P.INPUTS[key]
        exact(closure['outputs']['NATIVE_PAYLOAD/'+basename], {'bytes': pin['bytes'], 'sha256': pin['sha256']}, 'whole original pilot file entry')
    journal = [decode(line) for line in rawinputs['initial_journal'].splitlines()]
    pres = [r for r in journal if r.get('kind') == 'microstep_pre' and r['index'] == 0]
    ledgers = [r for r in journal if r.get('kind') == 'microstep_ledger' and r['index'] == 0]
    need(len(pres) == len(ledgers) == 1 and M.Q(pres[0]['time']) == 0
         and M.Q(ledgers[0]['value']['previous_L2_error']) == 0, 'unique initial0 exact-error point')
    exact(ledgers[0]['value']['vector_files']['left'], {'file': 'STEP_000_left.bin', 'bytes': 500752,
          'sha256': P.INPUTS['initial_vector']['sha256'], 'dimension': 10432, 'fractional_bits': 80,
          'fields': ['real_lower', 'real_upper', 'imag_lower', 'imag_upper'], 'endpoint_signed_bits': 96}, 'complete original initial vector binding')
    snapshots = {'caller': callerraw.decode()}
    for name, pin in P.SOURCES.items():
        snapshots[name] = producer_pin(pin, 65536).decode()
    exact(data['SOURCE_SNAPSHOTS.json'], snapshots, 'every full original caller/helper source byte')
    pid = data['START.json']['pid']
    need(type(pid) is int and pid > 0, 'original PID syntax; original owned runtime separatelyroot')
    exact(data['START.json'], {'schema': 'SHARED_KRYLOV_ONE_STEP_START_V001', 'executor': '/root', 'pid': pid,
          'config': configpin, 'caps': CAPS, 'external_supervisor_required': True, 'scientific_acceptance': False}, 'wholeSTART')
    native = decode(rawinputs['packet'])
    need(native['phase'] == 'native', 'exact original native packet container')
    selected = decode(I.pin(P.PARENT_SELECTED))
    I.pin(P.PARENT_EMITS, False)
    with Path(P.PARENT_EMITS['path']).open('rb') as stream:
        rebuilt = N.reconstruct(native['complete_native_packet'], selected, (decode(line) for line in stream), guard)
    print(json.dumps({'independent_progress': 'ALL20672_LITERAL_COLUMNS_AND10432_SHIFTED_ROWS_COMPLETE'}), flush=True)
    index = rebuilt['seed_index']
    center = [[0, 0] for _ in range(10432)]
    center[index] = [1 << 80, 0]
    raw = rawinputs['initial_vector']
    need(len(raw) == 500752 and raw[:8] == b'UNTI80V1' and struct.unpack('<II', raw[8:16]) == (10432, 4), 'entire original I80 binarypoint')
    for i, (re, im) in enumerate(center):
        endpoints = [int.from_bytes(raw[16+48*i+12*k:16+48*i+12*(k+1)], 'little', signed=True) for k in range(4)]
        exact(endpoints, [re, re, im, im], 'every initial coordinate/'+str(i))
    exact(data['NATIVE_BINDING.json'], {'schema': 'SHARED_KRYLOV_EXACT_NATIVE_BINDING_V001', 'full_dimension': 20672,
          'active_dimension': 10432, 'all20672_native_columns_reconstructed': True, 'all_component_rows_exactly_matched': True,
          'active_to_native': rebuilt['active_to_native'], 'active_states': rebuilt['active_states'], 'seed': 'OLD_CARRIER_SITE0',
          'seed_index': index, 'exact_initial_L2_error': '0', 'original_initial_vector': P.INPUTS['initial_vector'],
          'tau': '1/512', 'max_columns': 16, 'degree': 32, 'fractional_bits': 80, 'coefficient_denominator': 560,
          'shift': '2121/80', 'shifted_row_norm': '10207/560'}, 'whole native binding')
    args1 = {'rows': rebuilt['rows'], 'denominator': 560, 'center': center, 'max_columns': 16}
    exact(data['CANDIDATE_PRE.json'], {'function': 'candidate_lanczos', 'arguments': args1,
          'phase': 'BEFORE_ACTUAL_CALL'}, 'complete candidate PRE')
    cr = data['CANDIDATE_RETURN.json']
    need(type(cr) is dict and set(cr) == {'exception', 'value'} and cr['exception'] is None, 'whole successful saved candidate')
    proposal = cr['value']
    args2 = {'rows': rebuilt['rows'], 'denominator': 560, 'center': center, 'input_L2_error': '0',
             'proposal': proposal, 'tau': '1/512', 'degree': 32}
    exact(data['CERTIFICATE_PRE.json'], {'function': 'certificate', 'arguments': args2,
          'phase': 'BEFORE_ACTUAL_CALL'}, 'every actual candidate byte/value consumed by certificate')
    certificate = M.reconstruct(rebuilt['rows'], center, proposal, guard)
    exact(data['CERTIFICATE_RETURN.json'], {'exception': None, 'value': certificate}, 'every full independent exact certificate field')
    result = {'schema': 'SHARED_KRYLOV_ONE_STEP_RAW_RESULTS_V001', 'candidate_columns': len(proposal['basis_I80']),
              'step_target_2_minus_64_met': certificate['step_target_2_minus_64_met'],
              'original_cumulative_cap_2_minus_51_met': certificate['original_cumulative_cap_2_minus_51_met'],
              'step_added_L2_error': certificate['step_added_L2_error'], 'accumulated_L2_error': certificate['accumulated_L2_error'],
              'candidate_is_untrusted': True, 'distinct_complete_comparison_required': True,
              'native_N2_validation_completed': False, 'full_native_validation_released': False,
              'N4_released': False, 'original_backend_warnings_resolved': False, 'physical_release': False}
    exact(data['RESULTS.json'], result, 'wholeRESULTS including any precision miss')
    exact(data['INPUT_MANIFEST.json'], {'complete_consumed_input_files': [I.pins[p] for p in producer_paths],
          'whole_original_namespace_closing_root_obligation': True, 'selected_inputs_are_original_process_closure': False}, 'whole ordered original consumed-input manifest')
    exact(data['FINISH.json'], {'schema': 'SHARED_KRYLOV_ONE_STEP_FINISH_V001', 'pid': pid,
          'files_before_finish': {k: v for k, v in filemeta.items() if k != 'FINISH.json'},
          'all_consumed_input_closing_bytes_match': True,
          'status': 'RAW_COMPLETE_FEASIBILITY_REQUIRES_DISTINCT_COMPARISON_AND_ROOT_CUSTODY',
          'native_N2_validation_completed': False, 'physical_release': False}, 'wholeFINISH')
    need({p.name for p in root.iterdir()} == FILES, 'closing entire13-file census')
    I.close()
    guard()
    report = {'schema': 'SHARED_KRYLOV_COMPLETE_NATIVE_ONE_STEP_INDEPENDENT_REVIEW_V001',
              'status': 'PASS_COMPLETE_EXACT_FEASIBILITY_COMPARISON_PENDING_ROOT_RUNTIME_CUSTODY',
              'producer_author': 'Codex2', 'checker_author': 'Codex3', 'self_review': False, 'archive': str(root),
              'all13_scientific_files': filemeta, 'all20672_native_columns_independently_reconstructed': True,
              'all10432_active_rows_and_initial_coordinates_exact': True, 'all_saved_candidate_entries_consumed': True,
              'candidate_decimal_regenerated': False,
              'candidate_contract': 'UNTRUSTED_COMPLETE_I80_INPUT_WITH_ROOT_ACTUAL_SOURCE_CALL_PROVENANCE; INDEPENDENT_FULL_DEFECT_PROOF',
              'every_exact_certificate_field_independently_compared': True,
              'independent_arithmetic': 'Hermitian-pair fullH in280units; Gaussian integer T powers and common-factor full polynomial; bisection outward roots',
              'result': result, 'complete_checker_input_pins': I.pins, 'all_opened_input_closing_pins_match': True,
              'original_runtime_and_whole_historical_namespaces_verified_here': False,
              'full_native_validation_released': False, 'N4_released': False, 'physical_release': False}
    raw = (json.dumps(report, sort_keys=True, separators=(',', ':'), allow_nan=False)+'\n').encode()
    need(len(raw) <= 16*2**20, 'complete bounded checker report')
    output.mkdir(exist_ok=False)
    import os
    with (output/'INDEPENDENT_REPORT.json').open('xb') as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    print(json.dumps({'status': report['status'], 'report_bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
          'step_target_2_minus_64_met': result['step_target_2_minus_64_met'],
          'candidate_decimal_regenerated': False}), flush=True)


if __name__ == '__main__':
    main()

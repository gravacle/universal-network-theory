"""SOURCE ONLY. Complete original13/profile14 native archive audit.
Derived from accepted independent0339, retaining every full native H/certificate
and provenance comparison. No producer scientific source execution.
Root supplies one whole-job guard and input tracker, never resets runtime caps.
"""
from pathlib import Path
import json
import struct
B=Path('/Users/bgm/Research/UNT_EXCHANGE/KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001')
LANE=Path('/Users/bgm/Research/UNT_EXCHANGE/lanes/P49_CODEX2')
CAPS={'cpu':1,'rss_bytes':8*2**30,'seconds':600,'output_bytes':128*2**20,'scientific_reserve_bytes':120*2**20}
BASE_FILES={'START.json','ROOT_CONFIG.json','SOURCE_SNAPSHOTS.json','GATE_SNAPSHOTS.json','INPUT_PINS.json',
    'NATIVE_BINDING.json','CANDIDATE_PRE.json','CANDIDATE_RETURN.json','CERTIFICATE_PRE.json',
    'CERTIFICATE_RETURN.json','RESULTS.json','INPUT_MANIFEST.json','FINISH.json'}


def audit(root,I,guard,modules,profile=False):
    C,N,M,P,U=(modules[k] for k in ('custody','native','certificate','pins','support'))
    need,exact,decode=C.need,C.exact,C.decode
    CALLER=LANE/('krylov_integer_native_profile_root_caller_v001.py' if profile else 'shared_krylov_native_one_step_caller_v001.py')
    CALLER_SHA=('3a4fba047e5ec38963822df7d69c2a45ca5295e6029db30c64e201c8bacdca99' if profile else 'f0a3595da2a45ccf1569ec947a3c82591c0bc9a6da124ddf0b3afc7c40c566a7')
    ROLE='SHARED_KRYLOV_INTEGER_NATIVE_PROFILE_V001' if profile else 'SHARED_KRYLOV_NATIVE_FEASIBILITY_V001'
    sourcepins=dict(P.SOURCES)
    if profile:sourcepins['integer']=U.SOURCES['integer']
    FILES=BASE_FILES|({'PROFILE.json'} if profile else set())
    need(root.is_absolute() and root.resolve()==root and not root.is_symlink() and root.is_dir() and B in root.parents,'literal whole native archive')
    need({p.name for p in root.iterdir()}==FILES,'entire13 or14 file census')
    data,filemeta={},{}
    for name in sorted(FILES):
        data[name]=decode(I.read(root/name,cap=120*2**20))
        rec=I.pins[str(root/name)];filemeta[name]={'sha256':rec['sha256'],'bytes':rec['bytes']}
    need(sum(v['bytes'] for v in filemeta.values())<=120*2**20,'whole science reserve')
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
    need(set(cfg) == {'schema', 'role', 'released_by', 'execute', 'output', 'caps', 'source_gate', 'original_namespace_custody'} | ({'qualification_acceptance'} if profile else set()), 'closed one-step root config')
    need(cfg['schema'] == ('SHARED_KRYLOV_INTEGER_PROFILE_RELEASE_V001' if profile else 'SHARED_KRYLOV_ONE_STEP_RELEASE_V001') and cfg['role'] == ROLE
         and cfg['released_by'] == '/root' and cfg['execute'] is True and cfg['output'] == str(root), 'actual frozen one-step release')
    exact(cfg['caps'], CAPS, 'same declared wholecaps')
    callerraw = producer_pin({'path': str(CALLER), 'sha256': CALLER_SHA}, 65536)
    gates = {}
    for key in (('source_gate', 'original_namespace_custody', 'qualification_acceptance') if profile else ('source_gate', 'original_namespace_custody')):
        need(Path(cfg[key]['path']).parent == B, 'root-owned exact gate')
        gates[key] = decode(producer_pin(cfg[key], 2*2**20))
    exact(data['GATE_SNAPSHOTS.json'], gates, 'complete gate snapshots')
    sg, cg = gates['source_gate'], gates['original_namespace_custody']
    need(sg['acceptor'] == '/root' and str(sg['status']).startswith('PASS') and sg['role'] == ROLE, 'actual distinct source gate')
    exact(sg['source_pins'], sourcepins, 'every caller helper source pin')
    matched = [r for r in sg['allowed_runners'] if r['path'] == str(CALLER) and r['sha256'] == CALLER_SHA and r['role'] == ('producer' if profile else 'feasibility')]
    need(len(matched) == 1 and matched[0]['source_author'] == 'Codex2'
         and matched[0]['reviewer_id'] not in (None, 'Codex2'), 'distinct actual complete caller review')
    need(cg['acceptor'] == '/root' and str(cg['status']).startswith('PASS') and cg['role'] == ROLE
         and cg['complete_original_opening_checked'] is True and cg['complete_original_closing_root_obligation'] is True,
         'whole original namespace custody gate')
    exact(cg['input_pins'], P.INPUTS, 'frozen entire original input scope')
    if profile:
        qa = gates['qualification_acceptance']
        need(qa['schema'] == 'KRYLOV_INTEGER_QUALIFICATION_ACCEPTANCE_V001' and qa['acceptor'] == '/root'
             and str(qa['status']).startswith('PASS') and qa['integer_sha256'] == U.SOURCES['integer']['sha256']
             and qa['all10_controls_all20_events_complete'] is True
             and qa['full_C170_saved_candidate_certificate_equal'] is True
             and qa['distinct_complete_comparison'] is True and qa['complete_original_runtime_custody'] is True,
             'actual accepted complete controls and saved replay before fresh profile')
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
    for name, pin in sourcepins.items():
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
    if profile:
        U.profile(data['PROFILE.json'], pid, 'profile', exact, need, 600)
    exact(data['FINISH.json'], {'schema': 'SHARED_KRYLOV_ONE_STEP_FINISH_V001', 'pid': pid,
          'files_before_finish': {k: v for k, v in filemeta.items() if k != 'FINISH.json'},
          'all_consumed_input_closing_bytes_match': True,
          'status': 'RAW_COMPLETE_FEASIBILITY_REQUIRES_DISTINCT_COMPARISON_AND_ROOT_CUSTODY',
          'native_N2_validation_completed': False, 'physical_release': False}, 'wholeFINISH')
    need({p.name for p in root.iterdir()} == FILES, 'closing entire13-file census')
    return {'all_scientific_files':filemeta,'certificate':certificate,'certificate_pre':data['CERTIFICATE_PRE.json'],
        'result':result,'profile':data.get('PROFILE.json'),'archive':str(root),
        'all20672_native_columns_independently_reconstructed':True,
        'all10432_active_rows_and_initial_coordinates_exact':True,
        'every_exact_certificate_field_independently_compared':True,
        'candidate_decimal_regenerated':False,'original_runtime_verified_here':False}

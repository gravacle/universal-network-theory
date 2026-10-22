"""SOURCE ONLY. Root-only complete51-file all20 current/pair comparison.
CLI --archive ORIGINAL_ABS --output FRESH_ABS_DIRECTORY.
Full independent parent/current/80checkpoint reads/360vector decisions.
Actual all120 historical process namespaces and current runtime remain
root's separate custody obligation, never inferred from selected inputs.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import sys
import time
from types import SimpleNamespace

EX = Path('/Users/bgm/Research/UNT_EXCHANGE')
B = EX/'KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001'
O = EX/'FROM_CODEX3'
CALLER = EX/'lanes/P49_CODEX2/p64_all20_current_pair_root_caller_v002.py'
CALLER_SHA = 'b1d782d0d96091b370af47debd919c5aee76be6beaffe26529a26179708ba6c3'
CONTRACT = EX/'lanes/P49_CODEX2/P64_ALL20_CURRENT_PAIR_CONTRACT_V001.txt'
CONTRACT_SHA = '1ee9111892369aaf1d612200cb8b4f70819e53a6492ef67543366cbe4830c3e9'
HELPERS = {
    'custody': (O/'0331_2026-10-13_warning-independent-custody.py', '6fab6cd9636fca18463fe158f0da7b1641e51ff9fe3276e4a52c4220edfb5f47'),
    'native': (O/'0336_2026-10-13_native-Krylov-independent-H.py', 'c65b7c6ad4b4cd41a9ef31c45eeae3c282600b3f4207f9173e80a017f8ad9985'),
    'math': (O/'0347_2026-10-13_all20-independent-current-math.py', '9068d0d09c0e28dd481125dc0c4d26f4f0076676fe00408bfc8dcdb89fc552bd'),
    'pins': (O/'0348_2026-10-13_all20-independent-frozen-pins.py', '46e3f5a7e55aa07e843a7887132e5853e74b0d104155411d3bf87a9e1849932e')}
PARENT_EMITS = {'path': str(EX/'lanes/P49_CODEX2/ROOT_NATIVE_TRACE_Q1_A1_V001/FULL_INTERFACE_EMITS.jsonl'),
                'sha256': '0b236c5a4b17ce48f5877b14eb427319d57a9fc98eea7af50c0574df4ad5ecd2'}
PARENT_SELECTED = {'path': str(EX/'lanes/P49_CODEX2/ROOT_NATIVE_TRACE_Q1_A1_V001/ACCEPTED_PARENT_SELECTED_CENSUS.json'),
                   'sha256': '39436da4bbc696e9a790b129f4501e94e4cb6cbae700e0419bf012e586068ab8'}
ROLE = 'P64_ALL20_CURRENT_PAIR_READ_V001'
CAPS = {'cpu': 1, 'rss_bytes': 3*2**30, 'seconds': 900,
        'output_bytes': 128*2**20, 'scientific_reserve_bytes': 120*2**20}
FILES = {'START.json', 'ROOT_CONFIG.json', 'SOURCE_SNAPSHOTS.json', 'GATE_SNAPSHOTS.json',
         'RESULTS.json', 'INPUT_MANIFEST.json', 'FINISH.json'} | {
         'CALL_%02d_%s.json' % (i, event) for i in range(22) for event in ('PRE', 'RETURN')}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    def guard():
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024)
        if rss > 3*2**30 or time.monotonic()-started > 900:
            raise ValueError('whole independent900s3GiB role cap')
    modules = {}
    for name, (path, digest) in HELPERS.items():
        if path.resolve() != path or path.is_symlink() or path.stat().st_size > 65536:
            raise ValueError('plain checker helper')
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != digest:
            raise ValueError('exact independent helper source')
        ns = {'__name__': 'root_distinct_all20_'+name, '__file__': str(path)}
        exec(compile(raw, str(path), 'exec'), ns)
        modules[name] = SimpleNamespace(**ns)
    C, N, M, P = (modules[name] for name in ('custody', 'native', 'math', 'pins'))
    need, exact, decode = C.need, C.exact, C.decode
    I = C.Inputs(guard)
    for path, digest in HELPERS.values():
        I.read(path, digest, 65536)
    I.read(Path(__file__).resolve(), cap=65536)
    I.read(CONTRACT, CONTRACT_SHA, 65536)
    root, out = args.archive, args.output
    need(root.is_absolute() and root.resolve() == root and root.is_dir()
         and not root.is_symlink() and B in root.parents, 'literal root-owned original archive')
    need(out.is_absolute() and out.resolve() == out and not out.exists()
         and B in out.parents, 'literal fresh root-owned report folder')
    need({p.name for p in root.iterdir()} == FILES, 'whole51file successful census')
    data, meta = {}, {}
    for name in sorted(FILES):
        data[name] = decode(I.read(root/name, cap=120*2**20))
        pin = I.pins[str(root/name)]
        meta[name] = {'bytes': pin['bytes'], 'sha256': pin['sha256']}
    need(sum(v['bytes'] for v in meta.values()) <= 120*2**20, 'complete native science reserve')
    # Track producer read-order independently of this checker's extra inputs.
    producer_paths = []
    def producer_pin(pin, cap=32*2**20):
        raw = I.pin(pin, cap=cap)
        if pin['path'] not in producer_paths:
            producer_paths.append(pin['path'])
        return raw
    configpin = data['START.json']['config']
    need(Path(configpin['path']).parent == B, 'literal root release path')
    cfg = decode(producer_pin(configpin, 2*2**20))
    exact(data['ROOT_CONFIG.json'], cfg, 'whole original config')
    need(set(cfg) == {'schema', 'role', 'released_by', 'execute', 'output', 'caps',
                     'source_gate', 'controls_acceptance', 'input_gate'}, 'closed release')
    need(cfg['schema'] == 'P64_ALL20_CURRENT_PAIR_RELEASE_V001' and cfg['role'] == ROLE
         and cfg['released_by'] == '/root' and cfg['execute'] is True and cfg['output'] == str(root), 'actual full release identity')
    exact(cfg['caps'], CAPS, 'original role caps')
    rawcaller = producer_pin({'path': str(CALLER), 'sha256': CALLER_SHA}, 65536)
    gates = {}
    for name in ('source_gate', 'controls_acceptance', 'input_gate'):
        need(Path(cfg[name]['path']).parent == B, 'root gate ownership')
        gates[name] = decode(producer_pin(cfg[name]))
    exact(data['GATE_SNAPSHOTS.json'], gates, 'every complete gate snapshot')
    sg, cg, ig = (gates[k] for k in ('source_gate', 'controls_acceptance', 'input_gate'))
    need(sg['acceptor'] == '/root' and str(sg['status']).startswith('PASS') and sg['role'] == ROLE, 'distinct source authority')
    exact(sg['source_pins'], P.SOURCES, 'all source pins')
    hits = [r for r in sg['allowed_runners'] if r['path'] == str(CALLER)
            and r['sha256'] == CALLER_SHA and r['role'] == 'producer']
    need(len(hits) == 1 and hits[0]['source_author'] == 'Codex2'
         and hits[0]['reviewer_id'] not in (None, 'Codex2'), 'reviewer distinct from caller author')
    need(cg['acceptor'] == '/root' and str(cg['status']).startswith('PASS')
         and cg['math_sha256'] == P.SOURCES['math']['sha256']
         and cg['controls_sha256'] == P.SOURCES['controls']['sha256']
         and cg['all9_calls_all18_events_independently_compared'] is True
         and cg['complete_original_runtime_custody'] is True, 'actual nine-control acceptance')
    need(ig['schema'] == 'P64_ALL20_COMPLETE_TRAJECTORY_INPUT_GATE_V001'
         and ig['acceptor'] == '/root' and str(ig['status']).startswith('PASS')
         and ig['all60_newword_stages_distinctly_accepted'] is True
         and ig['all5_original_q11_histories_accepted'] is True
         and ig['complete_all20_original_opening_checked'] is True
         and ig['complete_all20_original_closing_root_obligation'] is True, 'actual full trajectory acceptance gate')
    exact(ig['fixed_inputs'], P.INPUTS, 'frozen exact native input pins')
    inputs = {name: decode(producer_pin(pin)) for name, pin in P.INPUTS.items()}
    old, c150 = inputs['old_endpoint_gate'], inputs['c150']
    audit = decode(producer_pin(c150['audit']))
    need(old['acceptor'] == '/root' and str(old['status']).startswith('PASS')
         and old['all_original_namespaces_authenticated'] is True, 'original q11 actual endpoint authority')
    need(inputs['c157']['claim'] == 'C-157' and inputs['c157']['complete_original_runtime_custody'] is True, 'accepted current baseline/census')
    oldpins = old['original_archive_closures']
    bypath = {pin['path']: pin for pin in oldpins}
    need(len(oldpins) == len(bypath) == 39 and set(bypath) == set(audit['complete_archives']), 'all39 original historical closures')
    for row in c150['records']:
        for field in ('producer_closure', 'reader_closure'):
            need(bypath[row[field]['path']]['sha256'] == row[field]['sha256'], 'C150 final producer/reader closure binding')
    oldclosures = {}
    for pin in oldpins:
        value = decode(producer_pin(pin))
        need(value['returncode'] == 0 and value['cap_stop'] is None
             and value['all_opening_pins_checked'] is True and value['all_closing_pins_match'] is True, 'original successful closed process')
        oldclosures[pin['path']] = value
    descriptors = ig['endpoints']
    need(set(descriptors) == {w+':'+kind+':'+str(stage) for w in M.WORDS
         for kind in M.TYPES for stage in range(4)}, 'all80 endpoint descriptors')
    selected = {}
    for word in M.WORDS:
        for kind in M.TYPES:
            key = word+':'+kind
            seed = kind if word == '11' else 'Q'+word+'_'+kind
            selected[key] = {}
            for stage in range(4):
                item = descriptors[key+':'+str(stage)]
                need(set(item) == {'family', 'seed', 'stage', 'pin', 'selector', 'source_closure', 'acceptance'}, 'closed endpoint descriptor')
                need(item['seed'] == seed and type(item['stage']) is int and item['stage'] == stage, 'every descriptor identity')
                pin, closurepin = item['pin'], item['source_closure']
                path = Path(pin['path'])
                if word == '11':
                    need(item['family'] == 'P49_ORIGINAL_Q11_FIVE', 'original q11 family only')
                    exact(item['acceptance'], P.INPUTS['c150'], 'exact original acceptance pin')
                    exact({'pin': pin, 'selector': item['selector']}, old['endpoints'][kind+':'+str(stage)], 'unchanged original endpoint binding')
                    need(closurepin['path'] in bypath, 'one of actual39 closures')
                    exact(closurepin, bypath[closurepin['path']], 'original closure pin')
                    closure = oldclosures[closurepin['path']]
                    need(path.parent.name == 'PAYLOAD' and str(path.parent) == closure['payload_root'], 'original selected file namespace')
                    exact(closure['outputs'][path.name], {'bytes': pin['bytes'], 'sha256': pin['sha256']}, 'whole original selected-file digest')
                else:
                    need(item['family'] == 'P64_NEW15_INITIAL_WORDS_V001'
                         and item['selector'] == 'WHOLE_CHECKPOINT_JSON', 'literal newword family selector')
                    need(Path(item['acceptance']['path']).parent == B, 'root-issued actual newword acceptance')
                    auth = decode(producer_pin(item['acceptance']))
                    closure = decode(producer_pin(closurepin))
                    need(auth['schema'] == 'P64_NEW_WORD_STAGE_REUSE_AUTHORIZATION_V001'
                         and auth['status'] == 'ROOT_ACCEPTED_FOR_NEW_WORD_STAGE_REUSE' and auth['issued_by'] == '/root'
                         and auth['reviewer_id'] not in (None, 'Codex3') and auth['seed'] == seed
                         and type(auth['stage']) is int and auth['stage'] == stage
                         and auth['complete_original_output_review'] is True and auth['whole_ancestry_review'] is True, 'actual complete stage acceptance')
                    exact(auth['process_closure'], closurepin, 'accepted stage closure pin')
                    report = decode(producer_pin(auth['independent_report']))
                    need(report['complete_saved_reconstruction'] is True and report['seed'] == seed
                         and type(report['stage']) is int and report['stage'] == stage
                         and report['whole_original_output_checked'] is True
                         and report['whole_same_seed_ancestry_checked'] is True, 'actual full distinct trajectory arithmetic')
                    need(closure['schema'] == 'P49_ORIGINAL_TWO_NAMESPACE_PROCESS_CLOSURE_V001'
                         and closure['complete_success'] is True and closure['returncode'] == 0
                         and closure['cap_stop'] is None and closure['all_opening_pins_checked'] is True
                         and closure['all_closing_pins_match'] is True, 'successful original newword process')
                    folder = Path(auth['archive_root'])
                    need(folder.is_absolute() and folder.resolve() == folder and B in folder.parents
                         and folder.name == 'PAYLOAD' and closure['payload_root'] == str(folder)
                         and closure['runtime_root'] == str(folder.parent/'RUNTIME')
                         and path == folder/'CHECKPOINT.json', 'exact newword two-namespace provenance')
                    exact(closure['outputs']['CHECKPOINT.json'], {'bytes': pin['bytes'], 'sha256': pin['sha256']}, 'entire newword checkpoint binding')
                selected[key][str(stage)] = item
    # Original producer source-read order is after dependency authentication.
    snapshots = {'caller': rawcaller.decode()}
    for name, pin in P.SOURCES.items():
        snapshots[name] = producer_pin(pin, 65536).decode()
    exact(data['SOURCE_SNAPSHOTS.json'], snapshots, 'all complete original source snapshots')
    pid = data['START.json']['pid']
    need(type(pid) is int and pid > 0, 'actual original PID field')
    exact(data['START.json'], {'schema': 'P64_ALL20_CURRENT_PAIR_START_V001', 'executor': '/root',
          'pid': pid, 'config': configpin, 'caps': CAPS,
          'external_supervisor_required': True, 'scientific_acceptance': False}, 'entireSTART')
    need(inputs['packet']['phase'] == 'native', 'native exact packet input')
    census = decode(I.pin(PARENT_SELECTED))
    I.pin(PARENT_EMITS, retain=False)
    with Path(PARENT_EMITS['path']).open('rb') as stream:
        packet = N.reconstruct(inputs['packet']['complete_native_packet'], census,
                               (decode(line) for line in stream), guard)
    table = M.current_table(packet, guard)
    def compare_call(index, name, arguments, result):
        exact(data['CALL_%02d_PRE.json' % index], {'name': name, 'arguments': arguments,
              'phase': 'BEFORE_ACTUAL_CALL'}, 'complete call PRE'+str(index))
        exact(data['CALL_%02d_RETURN.json' % index], {'name': name, 'exception': None,
              'value': result}, 'complete call RETURN'+str(index))
    compare_call(0, 'rebuild_complete_native_and_prepare_currents',
                 {'packet': P.INPUTS['packet'], 'selector': 'complete_native_packet'}, table)
    print(json.dumps({'independent_progress': 'ALL20672_PARENT_COLUMNS_AND_ALL_FOUR_COMPLETE_CURRENT_MATRICES'}), flush=True)
    tablepin = {'path': str(root/'CALL_00_RETURN.json'), **meta['CALL_00_RETURN.json']}
    reads, readpins = {}, {}
    index = 1
    for word in M.WORDS:
        for kind in M.TYPES:
            key = word+':'+kind
            checkpoints = {}
            for stage in range(4):
                item = selected[key][str(stage)]
                raw = producer_pin(item['pin'])
                if item['selector'] == 'WHOLE_CHECKPOINT_JSON':
                    cp = decode(raw)
                else:
                    need(word == '11' and kind == M.TYPES[0] and stage == 0
                         and item['selector'] == 'UNIQUE_ANCESTOR_CHECKPOINT_OBJECT', 'only actual pilot endpoint ancestry exception')
                    candidates = []
                    for line in raw.splitlines():
                        record = decode(line)
                        if record.get('kind') == 'ancestor_checkpoint':
                            candidates.append(record['checkpoint'])
                    need(len(candidates) == 1, 'one complete actual ancestor checkpoint')
                    cp = candidates[0]
                checkpoints[str(stage)] = cp
            value = M.preparation(packet, word, kind, checkpoints, guard)
            arguments = {'word': word, 'kind': kind, 'table': tablepin, 'table_selector': 'value',
                         'checkpoints': selected[key]}
            compare_call(index, 'read_preparation', arguments, value)
            reads[key] = value
            name = 'CALL_%02d_RETURN.json' % index
            readpins[key] = {'path': str(root/name), **meta[name]}
            index += 1
            print(json.dumps({'independent_complete_preparation': key, 'all_coordinates_per_endpoint': 10432}), flush=True)
    decisions = M.compare(reads, guard)
    compare_call(21, 'compare_all20_currents', {'accepted_original_read_sources': readpins,
                 'read_selector': 'value', 'these_intermediate_reads_require_same_complete_job_comparison': True}, decisions)
    exact(data['RESULTS.json'], {'schema': 'P64_ALL20_CURRENT_PAIR_RAW_COMPLETION_V001',
          'calls': 22, 'events': 44, 'preparations': 20, 'horizons_per_preparation': 4,
          'vertices_per_horizon': 4, 'crossword_pairs': 120, 'adjacent_horizon_pairs': 60,
          'each_pair_has_separate_j_and_F': True, 'distinct_complete_comparison_required': True,
          'physical_motion_release': False}, 'completeRESULTS')
    exact(data['INPUT_MANIFEST.json'], {'complete_consumed_input_files': [I.pins[path] for path in producer_paths],
          'complete_all20_original_closing_root_obligation': True,
          'selected_inputs_are_original_process_closure': False}, 'whole original ordered input manifest')
    exact(data['FINISH.json'], {'schema': 'P64_ALL20_CURRENT_PAIR_FINISH_V001', 'pid': pid,
          'files_before_finish': {name: rec for name, rec in meta.items() if name != 'FINISH.json'},
          'all_consumed_input_closing_bytes_match': True,
          'status': 'RAW_COMPLETE_ALL20_READ_REQUIRES_DISTINCT_COMPARISON_AND_ROOT_CUSTODY',
          'new_propagation': False, 'physical_motion_release': False}, 'wholeFINISH')
    I.close()
    need({p.name for p in root.iterdir()} == FILES, 'closing whole51file census')
    result = {'schema': 'CODEX3_ALL20_NATIVE_COMPLETE_INDEPENDENT_COMPARISON_V001',
              'status': 'PASS_COMPLETE_SAVED_COMPARISON',
              'all51_scientific_files_compared': True, 'all22_calls_all44_events_compared': True,
              'all20672_parent_columns_independently_reconstructed': True,
              'all_four_complete_current_matrices_compared': True,
              'all80_checkpoints_all10432_coordinates_compared': True,
              'all320_vertex_read_sets_compared': True,
              'all240_crossword_j_and_F_decisions_compared': True,
              'all120_temporal_j_and_F_decisions_compared': True,
              'complete_pair_decisions': decisions,
              'all51_scientific_file_hashes': meta,
              'all_opened_input_closing_pins': list(I.pins.values()),
              'complete_historical_runtime_namespaces_checked_here': False,
              'original_current_runtime_checked_here': False,
              'root_complete_historical_and_current_runtime_custody_required': True,
              'no_code2_scientific_module_executed': True,
              'finite_window_only': True, 'physical_motion_release': False}
    raw = (json.dumps(result, indent=2, allow_nan=False)+'\n').encode()
    need(len(raw) <= 120*2**20, 'whole report science reserve')
    guard()
    out.mkdir(exist_ok=False)
    with (out/'INDEPENDENT_REPORT.json').open('xb') as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    print(json.dumps({'status': result['status'], 'report_sha256': hashlib.sha256(raw).hexdigest()}))


if __name__ == '__main__':
    main()

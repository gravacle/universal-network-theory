"""SOURCE ONLY. Root-only native table/stage/aggregate durable caller.
CLI --config ABS --config-sha256 SHA --output FRESH_ABS.
Original complete runtime/namespace custody is root-owned, not replaced here.
"""
import argparse
from fractions import Fraction as F
import hashlib
import os
from pathlib import Path
from types import SimpleNamespace

EX = Path('/Users/bgm/Research/UNT_EXCHANGE')
B = EX/'KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001'
O = EX/'FROM_CODEX3'
PINS = {
    'io': {'path': str(O/'0319_2026-10-13_P50-native-durable-io.py'), 'sha256': 'c2bd0c3ee98e6dfd1f7e81d095e7701be87728a28d56d1bd28a3d49d77a247d4'},
    'p64': {'path': str(O/'0284_2026-10-13_P64-native-word-current-source.py'), 'sha256': '3e8405f3056f72646c9f5b1aa6402e3dcb101fe204294e9e1dc30eecdcf05fb6'},
    'table': {'path': str(O/'0305_2026-10-13_P50-native-operation-cost-tables.py'), 'sha256': '4ace341388a22eb59d1a3d3cf2bbc3cbb500d53d44c2731d40db29c4c5de2ab6'},
    'read': {'path': str(O/'0306_2026-10-13_P50-exact-saved-vector-reads.py'), 'sha256': 'a059fe12f1e1d1eedead91e0ff06a04e189e2103ad7e428eade97ea08b3d68e3'},
    'binding': {'path': str(O/'0307_2026-10-13_P50-complete-stage-vector-binding.py'), 'sha256': '4763d15704428b592c3be2c650c625337e4c15aad2a4423fa2be1f575889d8d2'},
    'prospect': {'path': str(O/'0302_2026-10-13_P50-native-bias-prospect.md'), 'sha256': '53f526bdfc03c4511546e5e56cbfa12214fc656d4edd016d7c8cade88a407ea3'}}
C150 = {'path': str(B/'P49_STAGE3_SCIENTIFIC_ACCEPTANCE_V001.json'), 'sha256': '347a12a04970199ad58edf938ec2be43473361590406a2daaf567bd10ab8e91b'}
C153 = {'path': str(B/'P49_SPECTRAL_NATIVE_FLOAT_COMPARISON_ACCEPTANCE_V001.json'), 'sha256': '48405948dd46eef4253146dc08f97017e3c6759f452d2548bbcabf150626a522'}
PACKET = {'path': str(B/'P49_SPECTRAL_NATIVE_OUTPUT_V001/ACTUAL_PRE.json'), 'sha256': '42b9c9106beaa841ed98892caa0cf115d24bee71eca57af3b60d9e0a82a1f272', 'bytes': 10998891}
PILOT = Path('/Users/bgm/Research/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/ROOT_UNT_LOCAL_RESIDENCY_MANIFEST_V002/exploratory_physics/PHASE12_PARALLEL_SCREEN_V001/H_record_front_provisional_V001/NATIVE_COEFFICIENT_DEPENDENCE_AUDIT_V001/P49_HISTORY_INTERVAL_ROOT_EXECUTION_V001')
SEEDS = ('OLD_CARRIER_SITE0', 'OLD_CARRIER_SITE1', 'OLD_READY_SITE0', 'OLD_COHERENT_PLUS_I', 'OLD_COHERENT_MINUS_I')
PANELS = (64, 64, 128, 256)
CAPS = {'cpu': 1, 'rss_bytes': 3*2**30, 'seconds': 900, 'output_bytes': 256*2**20,
        'scientific_reserve_bytes': 240*2**20}
COMMON = {'START.json', 'ROOT_CONFIG.json', 'SOURCE_SNAPSHOTS.json', 'GATE_SNAPSHOTS.json',
          'ACTUAL_PRE.json', 'ACTUAL_RETURN.json', 'INPUT_MANIFEST.json', 'FINISH.json'}


def io_module():
    p = Path(PINS['io']['path'])
    if p.resolve() != p or p.is_symlink() or p.stat().st_size > 65536:
        raise ValueError('plain bounded I/O source')
    raw = p.read_bytes()
    if hashlib.sha256(raw).hexdigest() != PINS['io']['sha256']:
        raise ValueError('literal I/O source hash')
    ns = {'__name__': 'root_p50_native_io', '__file__': str(p)}
    exec(compile(raw, str(p), 'exec'), ns)
    return SimpleNamespace(**ns)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--config-sha256', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    I = io_module()
    I.need(args.config.parent == B, 'root-owned release config')
    config_raw = I.plain(args.config, 2*2**20)
    I.need(I.sha(config_raw) == args.config_sha256, 'literal release hash')
    cfg = I.decode(config_raw)
    I.need(set(cfg) == {'schema', 'case', 'seed', 'stage', 'released_by', 'execute', 'output',
                       'caps', 'source_gate', 'control_acceptance', 'input_gate', 'dependency_gate'}, 'closed config')
    I.need(cfg['schema'] == 'P50_NATIVE_COMPLETE_READ_RELEASE_V001' and cfg['released_by'] == '/root'
           and cfg['execute'] is True and cfg['caps'] == CAPS and cfg['output'] == str(args.output), 'frozen root release')
    case, seed, stage = cfg['case'], cfg['seed'], cfg['stage']
    I.need(case in ('table', 'stage', 'aggregate'), 'three native roles only')
    I.need((case == 'table' and seed is None and stage is None)
           or (case == 'stage' and seed in SEEDS and type(stage) is int and 0 <= stage < 4)
           or (case == 'aggregate' and seed in SEEDS and stage is None), 'closed case seed stage')
    I.need((cfg['dependency_gate'] is None) == (case == 'table'), 'dependencies for every consuming role')
    for key in ('source_gate', 'control_acceptance', 'input_gate', 'dependency_gate'):
        if cfg[key] is not None:
            I.need(Path(cfg[key]['path']).parent == B, 'root-owned gate namespace')
    sink = I.Sink(args.output)
    try:
        config_pin = {'path': str(args.config), 'sha256': args.config_sha256}
        sink.pinned(config_pin, 2*2**20)
        own = Path(__file__).resolve()
        own_raw = I.plain(own, 65536)
        own_pin = {'path': str(own), 'sha256': I.sha(own_raw)}
        sink.pinned(own_pin, 65536)
        source_raw = {k: sink.pinned(v, 65536) for k, v in PINS.items()}
        source_raw['caller'] = own_raw
        gates = {k: I.decode(sink.pinned(cfg[k], 32*2**20)) for k in
                 ('source_gate', 'control_acceptance', 'input_gate', 'dependency_gate') if cfg[k] is not None}
        sg, cg, ig = (gates[k] for k in ('source_gate', 'control_acceptance', 'input_gate'))
        I.need(sg['acceptor'] == '/root' and str(sg['status']).startswith('PASS')
               and sg['role'] == 'P50_NATIVE_COMPLETE_READ_V001' and sg['source_pins'] == PINS,
               'distinct full source gate')
        allowed = [r for r in sg['allowed_runners'] if r['path'] == str(own) and r['sha256'] == own_pin['sha256'] and r['role'] == case]
        I.need(len(allowed) == 1 and allowed[0]['source_author'] == 'Codex3'
               and allowed[0]['reviewer_id'] != 'Codex3', 'exact distinct caller role review')
        I.need(cg['acceptor'] == '/root' and str(cg['status']).startswith('PASS')
               and cg['table_source_sha256'] == PINS['table']['sha256']
               and cg['read_source_sha256'] == PINS['read']['sha256']
               and cg['controls_source_sha256'] == '1f92ee09f2d025b581eb3dd2194e2bbb59adb8920ecac16262792803b3f6b41d'
               and cg['all_fifteen_calls_independently_compared'] is True
               and cg['complete_original_runtime_custody'] is True, 'actual complete control acceptance')
        I.need(ig['schema'] == 'P50_COMPLETE_ORIGINAL_INPUT_GATE_V001' and ig['acceptor'] == '/root'
               and str(ig['status']).startswith('PASS') and ig['all_original_namespaces_authenticated'] is True
               and ig['all_original_closing_pins_root_obligation'] is True
               and ig['c150'] == C150 and ig['c153'] == C153 and ig['packet'] == PACKET,
               'complete original input gate, never selected-input closure')
        c150 = I.decode(sink.pinned(C150))
        sink.pinned(C153)
        audit = I.decode(sink.pinned(c150['audit']))
        closure_pins = ig['original_archive_closures']
        I.need(len(closure_pins) == 39 and len({p['path'] for p in closure_pins}) == 39
               and {p['path'] for p in closure_pins} == set(audit['complete_archives']), 'all39 original archive census')
        by_path = {p['path']: p for p in closure_pins}
        for rec in c150['records']:
            for key in ('producer_closure', 'reader_closure'):
                I.need(by_path[rec[key]['path']]['sha256'] == rec[key]['sha256'], 'unchanged final original closure')
        closures = {}
        for pin in closure_pins:
            v = I.decode(sink.pinned(pin))
            I.need(v['returncode'] == 0 and v['cap_stop'] is None and v['all_opening_pins_checked'] is True
                   and v['all_closing_pins_match'] is True, 'successful original closure')
            closures[pin['path']] = v
        bindings = ig['journals']
        I.need(set(bindings) == {s+':'+str(k) for s in SEEDS for k in range(4)}, 'all20 original journal bindings')
        for s in SEEDS:
            for k in range(4):
                item = bindings[s+':'+str(k)]
                I.need(set(item) == {'journal', 'closure'}, 'closed journal binding')
                pilot = s == SEEDS[0] and k == 0
                folder = PILOT/'ROOT_NATIVE_HISTORY_INTERVAL_A_OUTPUT_V001/NATIVE_PAYLOAD' if pilot else B/('P49_STAGE%d_%s_RUN_V001/PAYLOAD' % (k, s))
                cp = PILOT/'ROOT_NATIVE_HISTORY_INTERVAL_A_CLOSURE_V001.json' if pilot else folder.parent/'PROCESS_CLOSURE.json'
                I.need(item['journal']['path'] == str(folder/'OPERANDS.jsonl')
                       and item['closure'] == by_path[str(cp)], 'literal original stage namespace')
                cname = 'NATIVE_PAYLOAD/OPERANDS.jsonl' if pilot else 'OPERANDS.jsonl'
                meta = closures[str(cp)]['outputs'][cname]
                I.need(item['journal']['sha256'] == meta['sha256'] and item['journal']['bytes'] == meta['bytes'],
                       'original journal closure entry')
        native = I.decode(sink.pinned(PACKET))
        I.need(native['phase'] == 'native', 'accepted exact native packet container')
        packet = native['complete_native_packet']
        modules = {}
        for k in ('p64', 'table', 'read', 'binding'):
            ns = {'__name__': 'root_p50_'+k, '__file__': PINS[k]['path']}
            exec(compile(source_raw[k], PINS[k]['path'], 'exec'), ns)
            modules[k] = SimpleNamespace(**ns)
        M, C, R, D = (modules[k] for k in ('p64', 'table', 'read', 'binding'))
        sink.save('START.json', {'schema': 'P50_NATIVE_COMPLETE_READ_START_V001', 'executor': '/root',
                  'pid': os.getpid(), 'config': config_pin, 'caps': CAPS,
                  'external_supervisor_required': True, 'scientific_acceptance': False})
        sink.save('ROOT_CONFIG.json', cfg)
        sink.save('SOURCE_SNAPSHOTS.json', {k: v.decode() for k, v in source_raw.items()})
        sink.save('GATE_SNAPSHOTS.json', gates)
        dependencies = {}

        def dependency(name, expected_case, expected_stage=None):
            dg = gates['dependency_gate']
            I.need(dg['schema'] == 'P50_DISTINCT_ACCEPTED_DEPENDENCIES_V001' and dg['acceptor'] == '/root'
                   and str(dg['status']).startswith('PASS') and dg['complete_original_runtime_custody'] is True,
                   'actual distinct accepted dependencies')
            item = dg['artifacts'][name]
            I.need(item['case'] == expected_case and item['seed'] == (None if expected_case == 'table' else seed)
                   and item['stage'] == expected_stage and item['accepted_by'] == '/root'
                   and str(item['status']).startswith('PASS') and item['reviewer_id'] != 'Codex3'
                   and item['all_scientific_fields_independently_compared'] is True,
                   'complete distinct prior scientific acceptance')
            sink.pinned(item['saved_checker_report'])
            folder = Path(item['archive'])
            I.need(folder.is_absolute() and folder.resolve() == folder and not folder.is_symlink()
                   and B in folder.parents and folder.is_dir(), 'root-owned accepted artifact directory')
            wanted = COMMON | ({'EXACT_INITIAL.json'} if expected_case == 'table' else {
                'FRAME_%03d_%s.json' % (i, e) for i in range(PANELS[expected_stage]+2) for e in ('PRE', 'RETURN')})
            I.need(set(item['files']) == wanted and {p.name for p in folder.iterdir()} == wanted, 'whole dependency file census')
            loaded = {}
            for filename in sorted(wanted):
                meta = item['files'][filename]
                loaded[filename] = I.decode(sink.pinned({'path': str(folder/filename), **meta}))
            fin = loaded['FINISH.json']
            I.need(fin['files_before_finish'] == {k: v for k, v in item['files'].items() if k != 'FINISH.json'}
                   and fin['all_consumed_input_closing_bytes_match'] is True, 'full prior finish manifest')
            rc = loaded['ROOT_CONFIG.json']
            I.need(rc['case'] == expected_case and rc['seed'] == item['seed'] and rc['stage'] == expected_stage
                   and rc['caps'] == CAPS, 'prior exact role and caps')
            I.need(loaded['SOURCE_SNAPSHOTS.json'] == {k: v.decode() for k, v in source_raw.items()}, 'identical accepted native source bytes')
            out = loaded['ACTUAL_RETURN.json']
            I.need(out['case'] == expected_case and out['seed'] == item['seed'] and out['stage'] == expected_stage
                   and out['exception'] is None, 'whole successful accepted return')
            dependencies[name] = item
            return loaded

        if case != 'table':
            want = {'table'} | ({'stage'+str(k) for k in range(4)} if case == 'aggregate' else set())
            I.need(set(gates['dependency_gate']['artifacts']) == want, 'exact full dependency role census')
            accepted_table = dependency('table', 'table')
            table = accepted_table['ACTUAL_RETURN.json']['value']
            I.need(table['schema'] == 'P50_NATIVE_COMPLETE_OPERATION_COST_TABLES_V001'
                   and table['active_dimension'] == 10432 and len(table['reads']) == 125, 'complete accepted operation table')
        frames = 0
        pending = None
        selected = None
        stage_frames = {}
        if case == 'stage':
            selected = bindings[seed+':'+str(stage)]
            journal_raw = sink.pinned(selected['journal'])
            I.need(journal_raw.endswith(b'\n'), 'complete original journal newline')
            folder = Path(selected['journal']['path']).parent
            closure = closures[selected['closure']['path']]
            prefix = 'NATIVE_PAYLOAD/' if seed == SEEDS[0] and stage == 0 else ''
            def load_vector(binding):
                filename = binding['file']
                I.need(Path(filename).name == filename, 'literal original vector basename')
                meta = closure['outputs'][prefix+filename]
                I.need(meta == {'bytes': binding['bytes'], 'sha256': binding['sha256']}, 'vector exact original closure entry')
                return sink.pinned({'path': str(folder/filename), **meta}, 500752)
            def audit_frame(event, label, payload):
                nonlocal frames, pending
                expected_label = 'START' if frames == 0 else 'STEP_%03d' % (frames-1)
                I.need(frames < PANELS[stage]+2 and label == expected_label, 'complete original frame sequence')
                if event == 'PRE':
                    I.need(pending is None, 'one durable PRE before each read')
                    pending = payload
                else:
                    I.need(event == 'RETURN' and pending is not None, 'one actual return after PRE')
                    if stage == 0 and frames == 0:
                        exact_reads = accepted_table['EXACT_INITIAL.json'][seed]['all_reads']
                        for name, row in payload['all_reads'].items():
                            lo, hi = map(F, row['interval'])
                            I.need(lo <= F(exact_reads[name]['exact_expectation']) <= hi, 'original exact initial read enclosed')
                sink.save('FRAME_%03d_%s.json' % (frames, event), {'label': label, 'payload': payload})
                if event == 'RETURN':
                    frames += 1
                    pending = None
        elif case == 'aggregate':
            for k in range(4):
                data = dependency('stage'+str(k), 'stage', k)
                values = []
                for i in range(PANELS[k]+2):
                    pre = data['FRAME_%03d_PRE.json' % i]
                    ret = data['FRAME_%03d_RETURN.json' % i]
                    label = 'START' if i == 0 else 'STEP_%03d' % (i-1)
                    I.need(pre['label'] == ret['label'] == label
                           and pre['payload']['seed'] == seed and pre['payload']['stage'] == k,
                           'all prior actual frames belong to exact seed/stage')
                    values.append({'time': pre['payload']['time'], 'result': ret['payload']})
                stage_frames[str(k)] = values
                del data
        sink.save('ACTUAL_PRE.json', {'case': case, 'seed': seed, 'stage': stage,
                  'function': {'table': 'prepare+all_five_exact_initial', 'stage': 'stage_reads', 'aggregate': 'aggregate'}[case],
                  'packet': PACKET, 'packet_selector': 'complete_native_packet', 'source_pins': PINS,
                  'selected_original_journal': selected, 'accepted_dependencies': dependencies,
                  'phase': 'BEFORE_ACTUAL_ARITHMETIC_CALL'})
        try:
            if case == 'table':
                result = C.prepare(M, packet, sink.guard)
                sink.save('ACTUAL_RETURN.json', {'case': case, 'seed': seed, 'stage': stage, 'exception': None, 'value': result})
                exacts = {s: R.exact_initial(M, result, packet, s) for s in SEEDS}
                sink.save('EXACT_INITIAL.json', exacts)
            elif case == 'stage':
                records = (I.decode(line) for line in journal_raw.splitlines())
                result = D.stage_reads(R, table, seed, stage, records, load_vector, audit_frame, sink.guard)
                I.need(frames == PANELS[stage]+2 and pending is None, 'all complete frame calls retained')
            else:
                result = D.aggregate(R, table, seed, stage_frames)
            if case != 'table':
                sink.save('ACTUAL_RETURN.json', {'case': case, 'seed': seed, 'stage': stage, 'exception': None, 'value': result})
        except BaseException as error:
            if 'ACTUAL_RETURN.json' not in sink.files:
                sink.save('ACTUAL_RETURN.json', {'case': case, 'seed': seed, 'stage': stage,
                          'exception': type(error).__name__, 'message': str(error)})
            raise
        sink.save('INPUT_MANIFEST.json', {'complete_consumed_input_files': list(sink.inputs.values()),
                  'selected_original_journal': selected, 'accepted_dependency_archives': dependencies,
                  'manifest_is_original_process_closure': False, 'root_whole_original_closing_required': True,
                  'original_Taylor_recomputed': False, 'floating_eigensolve_used': False})
        sink.close_inputs()
        sink.save('FINISH.json', {'schema': 'P50_NATIVE_COMPLETE_READ_FINISH_V001', 'pid': os.getpid(),
                  'case': case, 'seed': seed, 'stage': stage, 'frames': frames,
                  'files_before_finish': sink.files.copy(), 'all_consumed_input_closing_bytes_match': True,
                  'status': 'RAW_COMPLETE_READ_REQUIRES_DISTINCT_SAVED_COMPARISON_AND_ROOT_CUSTODY',
                  'whole_original_namespace_closing_by_root_still_required': True,
                  'new_propagation': False, 'physical_mass_claim': False})
        expected = COMMON | ({'EXACT_INITIAL.json'} if case == 'table' else set())
        if case == 'stage':
            expected |= {'FRAME_%03d_%s.json' % (i, e) for i in range(PANELS[stage]+2) for e in ('PRE', 'RETURN')}
        I.need(set(sink.files) == expected, 'complete scientific success census')
    except BaseException as error:
        sink.failure(error)
        raise


if __name__ == '__main__':
    main()

"""SOURCE ONLY. Root --config ABS --config-sha256 SHA --output FRESH_ABS.
Selected-input gate is NOT an original process closure or arithmetic checker.
Root must authenticate/close every complete original namespace separately.
"""
import argparse
import hashlib
import os
from pathlib import Path
from types import SimpleNamespace

EX = Path('/Users/bgm/Research/UNT_EXCHANGE')
B = EX/'KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001'
O = EX/'FROM_CODEX3'
IO_PIN = {'path': str(O/'0289_2026-10-13_P64-durable-io.py'),
          'sha256': '523cbda8be5e8d993f0d08d5f4c1400a4b325698caf1e804eff598598e908d7b'}
MATH_PIN = {'path': str(O/'0284_2026-10-13_P64-native-word-current-source.py'),
            'sha256': '3e8405f3056f72646c9f5b1aa6402e3dcb101fe204294e9e1dc30eecdcf05fb6'}
PROSPECT_PIN = {'path': str(O/'0283_2026-10-13_P64-native-word-current-prospect.md'),
                'sha256': '0ee9e806e513861c0c5b099fc6c48551e0c50b334e37eeb7642f07713e784610'}
C150_PIN = {'path': str(B/'P49_STAGE3_SCIENTIFIC_ACCEPTANCE_V001.json'),
            'sha256': '347a12a04970199ad58edf938ec2be43473361590406a2daaf567bd10ab8e91b'}
C153_PIN = {'path': str(B/'P49_SPECTRAL_NATIVE_FLOAT_COMPARISON_ACCEPTANCE_V001.json'),
            'sha256': '48405948dd46eef4253146dc08f97017e3c6759f452d2548bbcabf150626a522'}
PACKET_PIN = {'path': str(B/'P49_SPECTRAL_NATIVE_OUTPUT_V001/ACTUAL_PRE.json'),
              'sha256': '42b9c9106beaa841ed98892caa0cf115d24bee71eca57af3b60d9e0a82a1f272',
              'bytes': 10998891}
CONTROL_SHA = '285104c46f4af1277968d710fb0988efee66091ccb9826dac87e347f9fc24bd1'
CAPS = {'cpu': 1, 'rss_bytes': 2*2**30, 'seconds': 600, 'output_bytes': 16*2**20,
        'scientific_reserve_bytes': 8*2**20}


def load_io():
    path = Path(IO_PIN['path'])
    if path.resolve() != path or path.is_symlink() or path.stat().st_size > 65536:
        raise ValueError('plain bounded I/O source')
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != IO_PIN['sha256']:
        raise ValueError('I/O source hash')
    ns = {'__name__': 'root_p64_native_io', '__file__': str(path)}
    exec(compile(raw, str(path), 'exec'), ns)
    return SimpleNamespace(**ns)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--config-sha256', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    I = load_io()
    raw_config = I.plain(args.config, 2*2**20)
    I.require(I.digest(raw_config) == args.config_sha256, 'root release literal hash')
    cfg = I.decode(raw_config)
    I.require(set(cfg) == {'schema', 'case', 'seed', 'released_by', 'execute', 'output',
                          'caps', 'source_gate', 'control_acceptance', 'input_gate'}, 'closed config fields')
    I.require(cfg['schema'] == 'P64_NATIVE_SAVED_READ_RELEASE_V001'
              and cfg['released_by'] == '/root' and cfg['execute'] is True, 'actual root release')
    I.require(cfg['caps'] == CAPS and cfg['output'] == str(args.output), 'literal caps/output')
    I.require(cfg['case'] in ('census', 'baseline'), 'fixed read-only cases')
    I.require((cfg['case'] == 'census' and cfg['seed'] is None)
              or (cfg['case'] == 'baseline' and type(cfg['seed']) is str), 'case seed contract')
    for field in ('source_gate', 'control_acceptance', 'input_gate'):
        I.require(Path(cfg[field]['path']).parent == B, 'root-owned gate namespace')
    sink = I.Sink(args.output, 600, 2*2**30)
    try:
        config_pin = {'path': str(args.config), 'sha256': args.config_sha256}
        sink.pinned(config_pin, 2*2**20)
        self_raw = I.plain(Path(__file__).resolve(), 65536)
        self_pin = {'path': str(Path(__file__).resolve()), 'sha256': I.digest(self_raw)}
        sink.pinned(self_pin, 65536)
        io_raw = sink.pinned(IO_PIN, 65536)
        prospect_raw = sink.pinned(PROSPECT_PIN, 65536)
        M, math_raw = sink.module(MATH_PIN)
        I.require(cfg['case'] != 'baseline' or cfg['seed'] in M.TYPES, 'original five baseline seeds')
        gates = {key: I.decode(sink.pinned(cfg[key]))
                 for key in ('source_gate', 'control_acceptance', 'input_gate')}
        sg, cg, ig = (gates[key] for key in ('source_gate', 'control_acceptance', 'input_gate'))
        I.require(sg['acceptor'] == '/root' and sg['reviewer_id'] != 'Codex3'
                  and str(sg['status']).startswith('PASS')
                  and sg['math_source_sha256'] == MATH_PIN['sha256']
                  and sg['caller_sha256'] == self_pin['sha256'], 'distinct exact source gate')
        I.require(cg['acceptor'] == '/root' and str(cg['status']).startswith('PASS')
                  and cg['math_source_sha256'] == MATH_PIN['sha256']
                  and cg['controls_source_sha256'] == CONTROL_SHA
                  and cg['all_six_calls_independently_compared'] is True
                  and cg['complete_original_runtime_custody'] is True, 'actual controls acceptance gate')
        I.require(ig['schema'] == 'P64_COMPLETE_ORIGINAL_INPUT_GATE_V001'
                  and ig['acceptor'] == '/root' and str(ig['status']).startswith('PASS')
                  and ig['all_original_namespaces_authenticated'] is True
                  and ig['all_original_closing_pins_root_obligation'] is True,
                  'whole original custody gate, not subset closure')
        I.require(ig['c150'] == C150_PIN and ig['c153'] == C153_PIN
                  and ig['packet'] == PACKET_PIN, 'unchanged accepted parent input')
        c150 = I.decode(sink.pinned(C150_PIN))
        c153 = I.decode(sink.pinned(C153_PIN))
        old_audit = I.decode(sink.pinned(c150['audit']))
        archive_pins = ig['original_archive_closures']
        I.require(len(archive_pins) == 39 and len({p['path'] for p in archive_pins}) == 39,
                  'all 39 original history archives')
        I.require({p['path'] for p in archive_pins} == set(old_audit['complete_archives']),
                  'exact C150 original archive path census')
        archive_by_path = {p['path']: p for p in archive_pins}
        for record in c150['records']:
            for key in ('producer_closure', 'reader_closure'):
                pin = record[key]
                I.require(archive_by_path[pin['path']]['sha256'] == pin['sha256'],
                          'C150 literal final closures unchanged')
        for pin in archive_pins:
            closure = I.decode(sink.pinned(pin))
            I.require(closure['returncode'] == 0 and closure['cap_stop'] is None
                      and closure['all_opening_pins_checked'] is True
                      and closure['all_closing_pins_match'] is True, 'original success closure')
        endpoints = ig['endpoints']
        I.require(set(endpoints) == {name + ':' + str(stage) for name in M.TYPES for stage in range(4)},
                  'all20 selected endpoint bindings')
        for name in M.TYPES:
            for stage in range(4):
                binding = endpoints[name + ':' + str(stage)]
                I.require(set(binding) == {'pin', 'selector'}, 'closed endpoint binding')
                special = name == 'OLD_CARRIER_SITE0' and stage == 0
                expected_path = B/('P49_STAGE1_OLD_CARRIER_SITE0_RUN_V001/PAYLOAD/OPERANDS.jsonl'
                    if special else 'P49_STAGE%d_%s_RUN_V001/PAYLOAD/CHECKPOINT.json' % (stage, name))
                selector = 'UNIQUE_ANCESTOR_CHECKPOINT_OBJECT' if special else 'WHOLE_CHECKPOINT_JSON'
                I.require(binding['pin']['path'] == str(expected_path) and binding['selector'] == selector,
                          'literal accepted endpoint selector')
        # Closing whole archives belongs to root's new wave seal. This worker
        # rehashes every consumed complete input file and original closure.
        native_pre = I.decode(sink.pinned(PACKET_PIN))
        I.require(native_pre['phase'] == 'native', 'native exact packet container')
        packet = native_pre['complete_native_packet']
        checkpoints = {}
        used_bindings = {}
        if cfg['case'] == 'baseline':
            for stage in range(4):
                key = cfg['seed'] + ':' + str(stage)
                binding = endpoints[key]
                raw = sink.pinned(binding['pin'])
                if binding['selector'] == 'WHOLE_CHECKPOINT_JSON':
                    checkpoint = I.decode(raw)
                else:
                    matches = []
                    for line in raw.splitlines():
                        item = I.decode(line)
                        if item.get('kind') == 'ancestor_checkpoint':
                            matches.append(item['checkpoint'])
                    I.require(len(matches) == 1, 'exact one original ancestor checkpoint')
                    checkpoint = matches[0]
                checkpoints[str(stage)] = checkpoint
                used_bindings[str(stage)] = binding
        sink.save('START.json', {'schema': 'P64_NATIVE_SAVED_READ_START_V001', 'executor': '/root',
                  'pid': os.getpid(), 'config': config_pin, 'caps': CAPS,
                  'external_supervisor_required': True, 'scientific_acceptance': False})
        sink.save('ROOT_CONFIG.json', cfg)
        sink.save('SOURCE_SNAPSHOTS.json', {'caller': self_raw.decode(), 'io': io_raw.decode(),
                  'math': math_raw.decode(), 'prospect': prospect_raw.decode()})
        sink.save('GATE_SNAPSHOTS.json', gates)
        sink.save('INPUT_MANIFEST.json', {'complete_input_files': list(sink.inputs.values()),
                  'packet_selector': 'complete_native_packet', 'endpoint_selectors': used_bindings,
                  'manifest_is_original_process_closure': False,
                  'original_namespace_full_verification_by_worker': False,
                  'root_whole_original_closing_required': True,
                  'floating_eigensolve_used': False, 'backend_warning_disposition_changed': False})
        sink.save('ACTUAL_PRE.json', {'case': cfg['case'], 'seed': cfg['seed'],
                  'function': cfg['case'], 'packet': PACKET_PIN,
                  'packet_selector': 'complete_native_packet', 'endpoints': used_bindings,
                  'math_source': MATH_PIN, 'phase': 'BEFORE_ACTUAL_ARITHMETIC_CALL'})
        try:
            result = M.census(packet, sink.guard) if cfg['case'] == 'census' else M.baseline(packet, cfg['seed'], checkpoints, sink.guard)
        except BaseException as error:
            sink.save('ACTUAL_RETURN.json', {'case': cfg['case'], 'seed': cfg['seed'],
                      'exception': type(error).__name__, 'message': str(error)})
            raise
        sink.save('ACTUAL_RETURN.json', {'case': cfg['case'], 'seed': cfg['seed'],
                  'exception': None, 'value': result})
        sink.close_inputs()
        sink.save('FINISH.json', {'schema': 'P64_NATIVE_SAVED_READ_FINISH_V001',
                  'pid': os.getpid(), 'case': cfg['case'], 'seed': cfg['seed'],
                  'all_consumed_input_closing_bytes_match': True,
                  'files_before_finish': sink.files.copy(),
                  'status': 'RAW_EXACT_READ_REQUIRES_DISTINCT_SAVED_COMPARISON_AND_ROOT_CUSTODY',
                  'whole_original_namespace_closing_by_root_still_required': True,
                  'new_propagation': False, 'physical_release': False})
    except BaseException as error:
        sink.failure(error)
        raise


if __name__ == '__main__':
    main()

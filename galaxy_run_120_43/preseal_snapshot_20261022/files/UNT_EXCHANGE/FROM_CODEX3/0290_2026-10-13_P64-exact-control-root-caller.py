"""SOURCE ONLY. Root CLI --output FRESH_ABSOLUTE_DIRECTORY; fixed six calls."""
import argparse
import hashlib
import os
from pathlib import Path
from types import SimpleNamespace

BASE = Path('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3')
IO_PIN = {'path': str(BASE/'0289_2026-10-13_P64-durable-io.py'),
          'sha256': '523cbda8be5e8d993f0d08d5f4c1400a4b325698caf1e804eff598598e908d7b'}
MATH_PIN = {'path': str(BASE/'0284_2026-10-13_P64-native-word-current-source.py'),
            'sha256': '3e8405f3056f72646c9f5b1aa6402e3dcb101fe204294e9e1dc30eecdcf05fb6'}
CONTROL_PIN = {'path': str(BASE/'0285_2026-10-13_P64-native-current-exact-controls.py'),
               'sha256': '285104c46f4af1277968d710fb0988efee66091ccb9826dac87e347f9fc24bd1'}
NAMES = ('plus_i', 'minus_i', 'bind_no_transport', 'current_scale_not_covering',
         'inconsistent_normalized_range', 'insufficient_precision')


def load_io():
    path = Path(IO_PIN['path'])
    if path.resolve() != path or path.is_symlink() or path.stat().st_size > 65536:
        raise ValueError('fixed bounded plain I/O source')
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != IO_PIN['sha256']:
        raise ValueError('fixed I/O hash')
    module = {'__name__': 'root_p64_io', '__file__': str(path)}
    exec(compile(raw, str(path), 'exec'), module)
    return SimpleNamespace(**module)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    I = load_io()
    sink = I.Sink(args.output, 60, 256*2**20)
    try:
        self_raw = I.plain(Path(__file__).resolve(), 65536)
        self_pin = {'path': str(Path(__file__).resolve()), 'sha256': I.digest(self_raw)}
        sink.pinned(self_pin, 65536)
        io_raw = sink.pinned(IO_PIN, 65536)
        M, math_raw = sink.module(MATH_PIN)
        C, control_raw = sink.module(CONTROL_PIN)
        sink.save('START.json', {'schema': 'P64_EXACT_CONTROL_ROOT_CALL_V001',
                  'executor': '/root', 'pid': os.getpid(),
                  'caps': {'cpu': 1, 'rss_bytes': 256*2**20, 'seconds': 60,
                           'output_bytes': 16*2**20, 'scientific_reserve_bytes': 8*2**20},
                  'external_supervisor_required': True,
                  'sources': [self_pin, IO_PIN, MATH_PIN, CONTROL_PIN],
                  'scientific_acceptance': False})
        sink.save('SOURCE_SNAPSHOTS.json', {'caller': self_raw.decode(), 'io': io_raw.decode(),
                  'math': math_raw.decode(), 'controls': control_raw.decode()})
        position = 0
        def audit(event, name, value):
            nonlocal position
            expected_name = NAMES[position//2] if position < 12 else None
            expected_event = 'PRE' if position % 2 == 0 else 'RETURN'
            I.require(name == expected_name and event == expected_event, 'complete frozen audit order')
            sink.save('CALL_%02d_%s.json' % (position//2, event),
                      {'event': event, 'name': name, 'value': value})
            position += 1
        result = C.controls(M, audit)
        I.require(position == 12, 'all six actual calls complete')
        sink.save('RESULTS.json', result)
        sink.close_inputs()
        sink.save('FINISH.json', {'schema': 'P64_EXACT_CONTROL_RAW_FINISH_V001',
                  'pid': os.getpid(), 'complete_calls': 6, 'all_closing_source_bytes_match': True,
                  'status': 'RAW_RESULTS_REQUIRE_DISTINCT_SAVED_REVIEW',
                  'all_method_checks_returned': result['all_controls'],
                  'files_before_finish': sink.files.copy(), 'physical_release': False})
    except BaseException as error:
        sink.failure(error)
        raise


if __name__ == '__main__':
    main()

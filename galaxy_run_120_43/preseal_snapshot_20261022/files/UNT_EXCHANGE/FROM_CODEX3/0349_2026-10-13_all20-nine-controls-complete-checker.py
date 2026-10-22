"""SOURCE ONLY. Root executes full22-file tiny control comparison.
Independent exact expected intervals, all18 actual events, all metadata.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import json
import os
from pathlib import Path
import resource
import sys
import time
from types import SimpleNamespace

EX = Path('/Users/bgm/Research/UNT_EXCHANGE')
O = EX/'FROM_CODEX3'
L = EX/'lanes/P49_CODEX2'
HELPERS = {'custody': (O/'0331_2026-10-13_warning-independent-custody.py', '6fab6cd9636fca18463fe158f0da7b1641e51ff9fe3276e4a52c4220edfb5f47'),
           'math': (O/'0347_2026-10-13_all20-independent-current-math.py', '9068d0d09c0e28dd481125dc0c4d26f4f0076676fe00408bfc8dcdb89fc552bd')}
PINS = {'math': {'path': str(L/'p64_all20_current_pair_math_v001.py'), 'sha256': 'a42d1c4b5c3c6fe043f9ba168e6eb814dba1aa58f3fabf039fbaca34eb24c3c2'},
        'controls': {'path': str(L/'p64_all20_current_pair_controls_v001.py'), 'sha256': 'b722dcb0a321221cdca953c292d4d69eb1a4abd6612367a4787e77c8f839f341'},
        'caller': {'path': str(L/'p64_all20_nine_controls_root_caller_v001.py'), 'sha256': '9817f3d76c7a2d4f6a42e5ec530417686c2ac384d94003f09a173ef2431e0ff9'}}
NAMES = ('positive_difference', 'exact_null', 'threshold_equality', 'straddling_threshold',
         'negative_signed_difference', 'different_vertex_maximum', 'refuse_incomplete_vertices',
         'refuse_excess_halfwidth', 'refuse_missing_state_family')
FILES = {'START.json', 'SOURCE_SNAPSHOTS.json', 'RESULTS.json', 'FINISH.json'} | {
         'CALL_%02d_%s.json' % (i, event) for i in range(9) for event in ('PRE', 'RETURN')}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    began = time.monotonic()
    def guard():
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024)
        if rss > 256*2**20 or time.monotonic()-began > 60:
            raise ValueError('whole checker60s256MiB')
    modules = {}
    for name, (path, digest) in HELPERS.items():
        if path.resolve() != path or path.is_symlink() or path.stat().st_size > 65536:
            raise ValueError('plain checker helper')
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != digest:
            raise ValueError('whole independent helper pin')
        ns = {'__name__': 'root_distinct_controls_'+name, '__file__': str(path)}
        exec(compile(raw, str(path), 'exec'), ns)
        modules[name] = SimpleNamespace(**ns)
    C, M = modules['custody'], modules['math']
    need, exact = C.need, C.exact
    I = C.Inputs(guard)
    for path, digest in HELPERS.values():
        I.read(path, digest, 65536)
    I.read(Path(__file__).resolve(), cap=65536)
    need(args.archive.is_absolute() and args.archive.resolve() == args.archive
         and args.archive.is_dir() and not args.archive.is_symlink(), 'literal archive')
    need(args.output.is_absolute() and args.output.resolve() == args.output
         and not args.output.exists(), 'fresh literal output')
    need({p.name for p in args.archive.iterdir()} == FILES, 'whole22file census')
    data = {name: C.decode(I.read(args.archive/name, cap=8*2**20)) for name in FILES}
    meta = {name: {k: I.pins[str(args.archive/name)][k] for k in ('bytes', 'sha256')} for name in FILES}
    need(sum(r['bytes'] for r in meta.values()) <= 8*2**20, 'whole science reserve')
    sources = {name: I.pin(pin, cap=32768).decode() for name, pin in PINS.items()}
    exact(data['SOURCE_SNAPSHOTS.json'], sources, 'all original source bytes')
    pid = data['START.json'].get('pid')
    need(type(pid) is int and pid > 0, 'original PID field')
    exact(data['START.json'], {'schema': 'P64_ALL20_NINE_CONTROLS_START_V001',
          'executor': '/root', 'pid': pid, 'source_pins': PINS,
          'caps': {'cpu': 1, 'rss_bytes': 256*2**20, 'seconds': 60, 'output_bytes': 16*2**20},
          'scientific_reserve_bytes': 8*2**20, 'external_supervisor_required': True,
          'scientific_acceptance': False}, 'START')
    zero = [[Q(0), Q(0)] for _ in range(4)]
    def points(value):
        return [[Q(value), Q(value)] for _ in range(4)]
    args_list = [[zero, points(Q(1, 32))], [zero, zero], [zero, points(Q(1, 64))],
        [zero, [[Q(31, 2048), Q(33, 2048)] for _ in range(4)]], [zero, points(Q(-1, 32))],
        [zero, [[Q(0), Q(0)], [Q(0), Q(0)], [Q(1, 32), Q(1, 32)], [Q(-1, 16), Q(-1, 16)]]],
        [zero[:3], zero], [zero, [[Q(-1, 512), Q(1, 512)] for _ in range(4)]], [{}]]
    messages = ('all four vertex intervals', 'all individual read precision/ranges',
                'all twenty distinctly accepted complete preparation reads')
    decisions = ('RESOLVED_RECORD_CONTENT_DIFFERENCE', 'WITHIN_DECLARED_CURRENT_TOLERANCE',
                 'WITHIN_DECLARED_CURRENT_TOLERANCE', 'UNRESOLVED',
                 'RESOLVED_RECORD_CONTENT_DIFFERENCE', 'RESOLVED_RECORD_CONTENT_DIFFERENCE')
    calls = {}
    for i, (name, arguments) in enumerate(zip(NAMES, args_list)):
        function = 'compare' if i == 8 else 'vector_contrast'
        exact(data['CALL_%02d_PRE.json' % i], {'name': name,
              'arguments': {'function': function, 'arguments': M.wire(arguments)}}, 'whole control PRE'+str(i))
        if i < 6:
            outcome = {'exception': None, 'value': M.contrast(*arguments)}
            need(outcome['value']['decision'] == decisions[i], 'fixed known-answer decision')
        else:
            # Expected producer errors are literal refusal evidence; the
            # independent rule is also invoked and must reject the input.
            rejected = False
            try:
                if i == 8:
                    M.compare({}, guard)
                else:
                    M.contrast(*arguments)
            except ValueError:
                rejected = True
            need(rejected, 'independent malformed-input rejection')
            outcome = {'exception': 'ValueError', 'message': messages[i-6]}
        exact(data['CALL_%02d_RETURN.json' % i], {'name': name, 'outcome': outcome}, 'whole control RETURN'+str(i))
        calls[name] = outcome
    exact(data['RESULTS.json'], {'schema': 'P64_ALL20_CURRENT_PAIR_NINE_CONTROLS_V001',
          'calls': calls, 'checks': {name: True for name in NAMES}, 'all_controls': True,
          'native_current_arithmetic_control_ancestry': 'C155', 'new_trajectories_or_physical_motion': False}, 'RESULTS')
    exact(data['FINISH.json'], {'schema': 'P64_ALL20_NINE_CONTROLS_FINISH_V001', 'pid': pid,
          'all18_audit_events_saved': True, 'source_closing_bytes_match': True,
          'files_before_finish': {name: row for name, row in meta.items() if name != 'FINISH.json'},
          'status': 'RAW_CONTROL_RESULTS_PENDING_DISTINCT_SAVED_COMPARISON',
          'new_trajectories_executed': False, 'physical_motion_release': False}, 'FINISH')
    I.close()
    need({p.name for p in args.archive.iterdir()} == FILES, 'closing complete22census')
    report = {'schema': 'CODEX3_ALL20_NINE_CONTROLS_COMPLETE_COMPARISON_V001',
              'status': 'PASS_COMPLETE_SAVED_COMPARISON', 'all9_calls_all18_events_independently_compared': True,
              'all22_scientific_files_compared': True, 'all_full_calls': calls,
              'source_pins': PINS, 'all_opened_inputs_closing_checked': list(I.pins.values()),
              'complete_original_runtime_custody_checked_here': False,
              'root_runtime_and_final_acceptance_required': True, 'physical_motion_release': False}
    raw = (json.dumps(report, indent=2, allow_nan=False)+'\n').encode()
    need(len(raw) <= 8*2**20, 'checker scientific reserve')
    guard()
    args.output.mkdir(exist_ok=False)
    with (args.output/'INDEPENDENT_REPORT.json').open('xb') as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    print(json.dumps({'status': report['status'], 'report_sha256': hashlib.sha256(raw).hexdigest()}))


if __name__ == '__main__':
    main()

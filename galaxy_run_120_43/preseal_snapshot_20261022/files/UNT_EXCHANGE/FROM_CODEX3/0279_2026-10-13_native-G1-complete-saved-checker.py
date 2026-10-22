"""SOURCE ONLY. Root executes; author has not imported or called this checker.

CLI --case control2|L4|L5 --archive ABSOLUTE_ROOT_SCIENTIFIC_DIRECTORY.
Prints complete comparison receipt to owned stdout. Original process-runtime
custody is a separate root obligation, never inferred from six payload files.
"""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import sys
import time

BASE = Path('/Users/bgm/Research/UNT_EXCHANGE')
SOURCE = BASE / 'lanes/P60_CODEX2/p60_native_g1_size_preflight_v001.py'
SOURCE_SHA = '291deaa298227cfe531f9ccfaf4e098e700ceb89abc40d769a135bb6571ad5a3'
PRODUCER = BASE / 'KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001/P60_NATIVE_G1_ROOT_PRODUCER_V001.py'
PRODUCER_SHA = '56e410e945031dc916055a8439f488f601b68a703cd695ffdf4070794a993703'
ENGINE = BASE / 'FROM_CODEX3/0278_2026-10-13_native-G1-independent-count-math.py'
ENGINE_SHA = '5a5896331e5e3ce470f941f4488db31f216e87a95f0369be0460c754a9b19ce4'
THEORY = BASE / 'lanes/P60_CODEX2/P60_NATIVE_G1_FRAMING_SIZE_PROSPECT_V001.txt'
THEORY_SHA = '3273cce49753cb1f5832d62d2e78458c142e2f08b8bd49aad2a8247581099d84'
FILES = {'START.json', 'SOURCE_SNAPSHOT.py', 'ACTUAL_PRE.json', 'PROGRESS.jsonl',
         'ACTUAL_RETURN.json', 'FINISH.json'}
CASES = {'control2': ('method_control', [], 120, 120),
         'L4': ('preflight', [4], 120, 600),
         'L5': ('preflight', [5], 900, 3600)}


def require(ok, label):
    if not ok:
        raise ValueError(label)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read_plain(path, cap):
    path = Path(path)
    require(path.is_absolute() and path.resolve() == path and not path.is_symlink(),
            'literal plain absolute file ' + str(path))
    require(path.is_file() and path.stat().st_size <= cap, 'bounded regular file')
    with path.open('rb') as stream:
        raw = stream.read(cap + 1)
    require(len(raw) <= cap, 'bounded actual bytes')
    return raw


def no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def decode(raw):
    def invalid(value):
        raise ValueError('nonfinite JSON ' + value)
    return json.loads(raw, object_pairs_hook=no_duplicates, parse_constant=invalid)


def exact(actual, expected, path='root'):
    require(type(actual) is type(expected), 'typed equality ' + path)
    if isinstance(expected, dict):
        require(actual.keys() == expected.keys(), 'complete keys ' + path)
        for key in expected:
            exact(actual[key], expected[key], path + '/' + key)
    elif isinstance(expected, list):
        require(len(actual) == len(expected), 'complete length ' + path)
        for i, (a, b) in enumerate(zip(actual, expected)):
            exact(a, b, path + '/' + str(i))
    else:
        require(actual == expected, 'exact value ' + path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', choices=sorted(CASES), required=True)
    parser.add_argument('--archive', type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    function, arguments, producer_seconds, checker_seconds = CASES[args.case]

    def guard():
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if sys.platform != 'darwin':
            rss *= 1024
        require(time.monotonic() - started <= checker_seconds, 'checker time cap')
        require(rss <= 256 * 2**20, 'checker 256MiB RSS cap')

    def progress(event, current, total):
        guard()
        print(json.dumps({'independent_progress': event, 'current': current,
                          'total': total}, allow_nan=False), flush=True)

    root = args.archive
    require(root.is_absolute() and root.resolve() == root and not root.is_symlink()
            and root.is_dir(), 'literal existing archive')
    require({p.name for p in root.iterdir()} == FILES, 'exact six-file census')
    source_bytes = {}
    for path, digest in ((SOURCE, SOURCE_SHA), (PRODUCER, PRODUCER_SHA),
                         (ENGINE, ENGINE_SHA), (THEORY, THEORY_SHA)):
        raw = read_plain(path, 32768)
        require(sha(raw) == digest, 'fixed source/theory pin ' + str(path))
        source_bytes[path] = raw
    payload = {name: read_plain(root / name, 8 * 2**20) for name in FILES}
    require(sum(map(len, payload.values())) <= 8 * 2**20, 'whole scientific byte cap')
    require(payload['SOURCE_SNAPSHOT.py'] == source_bytes[SOURCE], 'whole source snapshot')
    exact(decode(payload['START.json']), {
        'schema': 'P60_NATIVE_G1_FIXED_ROOT_CALL_V001', 'case': args.case,
        'source': {'path': str(SOURCE), 'sha256': SOURCE_SHA},
        'runner_sha256': PRODUCER_SHA,
        'caps': {'cpu': 1, 'rss_bytes': 268435456, 'seconds': producer_seconds,
                 'output_bytes': 16777216},
        'external_supervisor_required': True, 'scientific_acceptance': False}, 'START')
    exact(decode(payload['ACTUAL_PRE.json']), {
        'case': args.case, 'function': function, 'arguments': arguments,
        'callback': 'complete COUNT_PROGRESS records retained'}, 'ACTUAL_PRE')
    journal_bytes = payload['PROGRESS.jsonl']
    require(journal_bytes.endswith(b'\n'), 'terminated progress journal')
    lines = journal_bytes.splitlines()
    require(len(lines) <= 128 and all(0 < len(line) < 65536 for line in lines),
            'bounded complete progress records')
    journal = [decode(line) for line in lines]
    actual = decode(payload['ACTUAL_RETURN.json'])
    require(set(actual) == {'case', 'arguments_after', 'exception', 'value'},
            'successful actual return shape')
    exact(actual['case'], args.case, 'return/case')
    exact(actual['arguments_after'], arguments, 'return/arguments_after')
    require(actual['exception'] is None, 'actual success only')
    # Only this distinct-author engine is executed. Author producer/scientific
    # sources are byte comparisons, never imported or used as the oracle.
    module = {'__name__': 'root_independent_g1_math', '__file__': str(ENGINE)}
    exec(compile(source_bytes[ENGINE], str(ENGINE), 'exec'), module)
    expected, independent = module['expected'](args.case, progress)
    exact(actual['value'], expected, 'complete_return')
    count = expected['actual'] if args.case == 'control2' else expected['layer_count']
    exact(journal, [{'event': 'COUNT_PROGRESS', 'record': row}
                    for row in count['block_records']], 'whole_journal')
    exact(decode(payload['FINISH.json']), {
        'case': args.case, 'status': 'RAW_SIZE_RETURN_PENDING_DISTINCT_SAVED_REVIEW',
        'progress_records': len(journal), 'source_closing_bytes_match': True,
        'spectral_execution': False, 'Gamma_qualified': False,
        'physical_release': False}, 'FINISH')
    require({p.name for p in root.iterdir()} == FILES, 'closing exact file census')
    for path, raw in source_bytes.items():
        require(read_plain(path, 32768) == raw, 'closing source bytes')
    for name, raw in payload.items():
        require(read_plain(root / name, 8 * 2**20) == raw, 'closing archive bytes')
    guard()
    report = {'schema': 'P60_NATIVE_G1_COMPLETE_DISTINCT_SAVED_REVIEW_V001',
              'status': 'PASS_COMPLETE_PAYLOAD_PENDING_ROOT_RUNTIME_CUSTODY',
              'author': 'Codex3', 'producer_author': '/root', 'source_author': 'Codex2',
              'self_review': False, 'case': args.case, 'archive': str(root),
              'files': {name: {'bytes': len(raw), 'sha256': sha(raw)}
                        for name, raw in sorted(payload.items())},
              'complete_typed_return_exact': True, 'all_checkpoint_fields_exact': True,
              'independent_count_and_trace': independent,
              'permanent': count['permanent'], 'block_sha256': count['block_sha256'],
              'complete_nonempty_subset_terms': count['nonempty_terms'],
              'original_runtime_verified_by_this_checker': False,
              'shared_math': 'Perfect matching identity; same literal graph and Ryser identity for telemetry only',
              'spectral_execution': False, 'Gamma_qualified': False,
              'physical_release': False}
    print(json.dumps(report, sort_keys=True, allow_nan=False), flush=True)


if __name__ == '__main__':
    main()

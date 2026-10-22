"""SOURCE ONLY. Root --archive ABSOLUTE_SIX_FILE_PAYLOAD; report to stdout.
Distinct complete count comparison; original process custody remains root's.
"""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import sys
import time

EX = Path('/Users/bgm/Research/UNT_EXCHANGE')
SOURCE = EX/'lanes/P49_CODEX2/p49_exact_n_ladder_counts_v001.py'
SOURCE_SHA = '3daa0c4f45672253bdeb68e2d65ab85916927d36be37dab0e809df9ea7d2d30d'
PRODUCER = EX/'KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001/P49_N_LADDER_ROOT_PRODUCER_V001.py'
PRODUCER_SHA = '7118a685c1e1f68f2e20227be22ab878a9c2b145749d361712322c42d105d2ab'
ENGINE = EX/'FROM_CODEX3/0299_2026-10-13_N-ladder-independent-math.py'
ENGINE_SHA = '4894554d6c36796451849cf97faf81cab81c4411840abb3bae4017cbb7591561'
THEORY = EX/'lanes/P49_CODEX2/P49_EXACT_N_LADDER_THEORY_V001.txt'
THEORY_SHA = '82390e88671d78a9599a6a2198772a4773869d885fddac81683f26740845434b'
FILES = {'START.json', 'SOURCE_SNAPSHOT.py', 'ACTUAL_PRE.json', 'PROGRESS.jsonl',
         'ACTUAL_RETURN.json', 'FINISH.json'}


def need(ok, why):
    if not ok:
        raise ValueError(why)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path, cap):
    p = Path(path)
    need(p.is_absolute() and p.resolve() == p and not p.is_symlink()
         and p.is_file() and p.stat().st_size <= cap, 'plain bounded input ' + str(p))
    with p.open('rb') as stream:
        raw = stream.read(cap+1)
    need(len(raw) <= cap, 'bounded read')
    return raw


def decode(raw):
    def pairs(items):
        out = {}
        for k, v in items:
            need(k not in out, 'duplicate JSON field')
            out[k] = v
        return out
    def bad(value):
        raise ValueError('nonfinite JSON ' + value)
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=bad)


def exact(actual, expected, path='root'):
    need(type(actual) is type(expected), 'typed equality ' + path)
    if isinstance(expected, dict):
        need(actual.keys() == expected.keys(), 'whole field census ' + path)
        for key in expected:
            exact(actual[key], expected[key], path+'/'+key)
    elif isinstance(expected, list):
        need(len(actual) == len(expected), 'whole length ' + path)
        for index, (a, b) in enumerate(zip(actual, expected)):
            exact(a, b, path+'/'+str(index))
    else:
        need(actual == expected, 'exact scalar ' + path)


def main():
    started = time.monotonic()
    parser = argparse.ArgumentParser()
    parser.add_argument('--archive', type=Path, required=True)
    args = parser.parse_args()
    def guard():
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if sys.platform != 'darwin':
            rss *= 1024
        need(time.monotonic()-started <= 60 and rss <= 256*2**20, '60s/256MiB checker cap')
    root = args.archive
    need(root.is_absolute() and root.resolve() == root and root.is_dir()
         and not root.is_symlink(), 'literal complete payload directory')
    need({p.name for p in root.iterdir()} == FILES, 'exact six-file payload census')
    sources = {}
    for path, digest in ((SOURCE, SOURCE_SHA), (PRODUCER, PRODUCER_SHA),
                         (ENGINE, ENGINE_SHA), (THEORY, THEORY_SHA)):
        raw = read(path, 32768)
        need(sha(raw) == digest, 'exact source/theory pin ' + str(path))
        sources[path] = raw
    data = {name: read(root/name, 8*2**20) for name in FILES}
    need(sum(map(len, data.values())) <= 8*2**20, 'complete scientific bytes')
    need(data['SOURCE_SNAPSHOT.py'] == sources[SOURCE], 'entire scientific source snapshot')
    start = decode(data['START.json'])
    need(type(start.get('pid')) is int and start['pid'] > 0, 'actual producer PID field')
    exact(start, {'schema': 'P49_N_LADDER_FIXED_ROOT_CALL_V001', 'pid': start['pid'],
                 'source': {'path': str(SOURCE), 'sha256': SOURCE_SHA},
                 'runner_sha256': PRODUCER_SHA,
                 'caps': {'cpu': 1, 'rss_bytes': 268435456, 'seconds': 60, 'output_bytes': 16777216},
                 'external_supervisor_required': True, 'scientific_acceptance': False}, 'START')
    exact(decode(data['ACTUAL_PRE.json']), {'function': 'preflight', 'arguments': [],
          'callback': 'complete61progressrecords:7graphs54rows'}, 'ACTUAL_PRE')
    need(data['PROGRESS.jsonl'].endswith(b'\n'), 'terminated complete progress')
    lines = data['PROGRESS.jsonl'].splitlines()
    need(len(lines) == 61 and all(0 < len(line)+1 <= 65536 for line in lines), '61 bounded complete records')
    journal = [decode(line) for line in lines]
    guard()
    module = {'__name__': 'root_independent_n_ladder', '__file__': str(ENGINE)}
    exec(compile(sources[ENGINE], str(ENGINE), 'exec'), module)
    expected, expected_journal = module['reconstruct']()
    guard()
    exact(journal, expected_journal, 'complete_progress')
    exact(decode(data['ACTUAL_RETURN.json']), {'exception': None, 'value': expected}, 'complete_return')
    exact(decode(data['FINISH.json']), {
        'status': 'RAW_EXACT_COUNTS_PENDING_DISTINCT_SAVED_COMPARISON', 'pid': start['pid'],
        'progress_records': 61, 'source_closing_bytes_match': True,
        'spectral_execution': False, 'physical_release': False}, 'FINISH')
    need({p.name for p in root.iterdir()} == FILES, 'closing exact payload census')
    for path, raw in sources.items():
        need(read(path, 32768) == raw, 'closing source bytes')
    for name, raw in data.items():
        need(read(root/name, 8*2**20) == raw, 'closing whole payload bytes')
    guard()
    report = {'schema': 'P49_N_LADDER_COMPLETE_DISTINCT_SAVED_REVIEW_V001',
              'status': 'PASS_COMPLETE_COUNTS_PENDING_ROOT_ORIGINAL_RUNTIME_CUSTODY',
              'author': 'Codex3', 'source_author': 'Codex2', 'caller_author': '/root',
              'self_review': False, 'archive': str(root), 'producer_pid': start['pid'],
              'all_seven_graphs': True, 'all_54_rows': True, 'all_61_progress_records': True,
              'complete_typed_return_equal': True, 'all_allocations_and_complements_checked': True,
              'independent_methods': ['union-find connected components', 'Pascal slot coefficients',
                                      'complete Birth-attachment polynomial convolution',
                                      'full allocation and dimension histogram comparison'],
              'shared_math': 'Same proved token/Bind/Birth connectivity theorem; independent count reconstruction',
              'files': {name: {'bytes': len(raw), 'sha256': sha(raw)}
                        for name, raw in sorted(data.items())},
              'source_pins': {str(path): sha(raw) for path, raw in sources.items()},
              'original_owned_PID_argv_runtime_checked_here': False,
              'new_preparation_selected': False, 'spectral_execution': False,
              'exact_DE_certified': False, 'physical_release': False}
    print(json.dumps(report, sort_keys=True, allow_nan=False), flush=True)


if __name__ == '__main__':
    main()

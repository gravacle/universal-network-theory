"""SOURCE ONLY: Codex3 complete ten-file P60 critical/noncritical saved checker.
Root executes after distinct review; own independent math engine is pinned.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

ROOT = Path('/Users/bgm/Research/UNT_EXCHANGE/KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001')
ENGINE = Path('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0269_2026-10-13_P60-critical-independent-math-source.py')
ENGINE_HASH = 'e6fe0a7227cdc0468ec5641df455db3a5a30b8cf2b6635820ec69fddfc14e24d'
PRODUCER = Path('/Users/bgm/Research/UNT_EXCHANGE/lanes/P60_CODEX2/p60_critical_root_producer_v001.py')
PRODUCER_HASH = '9eedd51af08cde64379b7477f2b5e6cd682e67c0d2df746a9b66a1b242665740'
ACCEPTANCE = {'path': str(ROOT/'P60_TORIC_QUALIFICATION_ACCEPTANCE_V001.json'),
              'sha256': '01c5d570bb2529ce711120ffdd8e5e000db7a20afec6d0a1edd1bbbfa0392947'}
LINEAGE = {
    'SOURCE_SNAPSHOT.py': {'path': '/Users/bgm/Research/UNT_EXCHANGE/lanes/P60_CODEX2/p60_c90_exact_critical_instrument_v002.py',
                           'sha256': 'dc8b4d9108dbf67f31e5a4038ee921f6478f2285402ddb9c32bcba5ac551fb2a'},
    'ORIGINAL_C90_LIBRARY.py': {'path': '/Users/bgm/Research/Universal Network Theory/program-worktree/LANE_T44_B_WORLD/t44b_lib.py',
                               'sha256': 'fb799b4421184e81a747baa6f33ba3fa0ef13340f60105ef002c3fd612d26f1b'},
    'ORIGINAL_C90_DRIVER.py': {'path': '/Users/bgm/Research/Universal Network Theory/program-worktree/LANE_T44_B_WORLD/t44b_world.py',
                              'sha256': 'b8ee598bf9fdebbd478d51f99fd24a0f81b5516bc56b3fcda948f9bef3f4a465'},
    'ORIGINAL_CORNER_LIBRARY.py': {'path': '/Users/bgm/Research/Universal Network Theory/program-worktree/LANE_T44_A_CORNER/t44a_lib.py',
                                  'sha256': '34bdf9af938d61160ab47e26d0941e8e06ec08655b6e795080e6499f98213ae7'}}
FILES = set(LINEAGE) | {'START.json', 'ROOT_CONFIG.json', 'QUALIFICATION_ACCEPTANCE.json',
                        'ACTUAL_PRE.json', 'ACTUAL_RETURN.json', 'FINISH.json'}
LIMIT = 16*2**20


def require(ok, text):
    if not ok:
        raise ValueError(text)


def raw(path, limit=LIMIT):
    require(path.is_absolute() and path.resolve() == path and path.is_file() and not path.is_symlink(),
            'plain absolute file '+str(path))
    require(path.stat().st_size <= limit, 'prospective bounded file')
    with path.open('rb') as stream:
        value = stream.read(limit+1)
    require(len(value) <= limit, 'bounded actual file')
    return value


def pin(value, limit=2**20):
    require(type(value) is dict and set(value) == {'path', 'sha256'}, 'pin schema')
    value_bytes = raw(Path(value['path']), limit)
    require(hashlib.sha256(value_bytes).hexdigest() == value['sha256'], 'pin digest')
    return value_bytes


def parse(value):
    def unique(items):
        result = {}
        for key, child in items:
            require(key not in result, 'duplicate JSON key')
            result[key] = child
        return result
    return json.loads(value, object_pairs_hook=unique,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))


def literal(value):
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, dict):
        require(len({str(k) for k in value}) == len(value), 'reference key collision')
        return {str(k): literal(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [literal(v) for v in value]
    return value


def same(actual, expected, where='root'):
    require(type(actual) is type(expected), 'type '+where)
    if isinstance(expected, dict):
        require(set(actual) == set(expected), 'keys '+where)
        for k in expected:
            same(actual[k], expected[k], where+'/'+k)
    elif isinstance(expected, list):
        require(len(actual) == len(expected), 'length '+where)
        for i, (a, e) in enumerate(zip(actual, expected)):
            same(a, e, where+'/'+str(i))
    else:
        require(actual == expected, 'value '+where)


def check(directory, config_pin):
    require(directory.is_absolute() and directory.resolve() == directory and directory.is_dir(),
            'plain absolute saved directory')
    entries = list(directory.iterdir())
    require({p.name for p in entries} == FILES and len(entries) == 10, 'complete ten-file census')
    require(all(p.is_file() and not p.is_symlink() for p in entries), 'plain saved files')
    require(sum(p.stat().st_size for p in entries) <= LIMIT, 'whole16MiB saved bound')
    content = {p.name: raw(p) for p in entries}
    require(sum(map(len, content.values())) <= LIMIT, 'consumed16MiB bound')
    require(Path(config_pin['path']).parent == ROOT, 'root-owned config')
    config_raw = pin(config_pin); config = parse(config_raw)
    require(set(config) == {'schema', 'case', 'qualification_acceptance',
                           'root_confirms_actual_qualification_accepted'}, 'config fields')
    case = config['case']; require(case in ['critical', 'noncritical'], 'fixed case')
    require(config['schema'] == 'P60_CRITICAL_FIXED_CALL_CONFIG_V001' and
            config['root_confirms_actual_qualification_accepted'] is True, 'actual qualification gate')
    same(config['qualification_acceptance'], ACCEPTANCE)
    acceptance_raw = pin(ACCEPTANCE); acceptance = parse(acceptance_raw)
    require(acceptance['claim'] == 'C-146' and acceptance['acceptor'] == '/root' and
            acceptance['status'] == 'ROOT_ACCEPTED_DECLARED_TORIC_OPERATOR_GEOMETRY_MINIMUM_STRATUM_GATES',
            'actual root qualification receipt')
    require({r['case'] for r in acceptance['records']} == {'small333', 'small334', 'growth17'},
            'all three accepted qualification cases')
    require(content['ROOT_CONFIG.json'] == config_raw and
            content['QUALIFICATION_ACCEPTANCE.json'] == acceptance_raw, 'complete root input bytes')
    producer_raw = pin({'path': str(PRODUCER), 'sha256': PRODUCER_HASH})
    engine_raw = pin({'path': str(ENGINE), 'sha256': ENGINE_HASH})
    originals = {name: pin(p) for name, p in LINEAGE.items()}
    for name, value in originals.items():
        require(content[name] == value, 'complete lineage snapshot '+name)
    same(parse(content['START.json']), {
        'schema': 'P60_CRITICAL_FIXED_CALL_V001', 'case': case, 'config_pin': config_pin,
        'qualification_acceptance': ACCEPTANCE, 'lineage': LINEAGE, 'runner_sha256': PRODUCER_HASH,
        'caps_prospective_external': {'cpu': 1, 'rss_bytes': 536870912, 'seconds': 900, 'output_bytes': LIMIT},
        'external_supervisor_required': True, 'TWO_CARRIER_adopted': False, 'physical_release': False})
    same(parse(content['ACTUAL_PRE.json']), {'case': case, 'function': case+'_controls',
         'arguments': [], 'keyword_arguments': {}, 'source_pin': LINEAGE['SOURCE_SNAPSHOT.py'],
         'root_config_pin': config_pin})
    engine = {'__name__': 'codex3_independent_count_checker', '__file__': str(ENGINE)}
    exec(compile(engine_raw, str(ENGINE), 'exec'), engine)
    count_hash = hashlib.sha256(); domains = {}
    def count_record(kind, index, values):
        count_hash.update((json.dumps([kind, index, values], separators=(',', ':'))+'\n').encode())
        item = domains.setdefault(kind, {'rows': 0, 'first': index, 'last': index, 'counts': 0})
        require(index == item['first']+item['rows'], 'complete sequential independent count domain')
        item['rows'] += 1; item['last'] = index; item['counts'] += len(values)
    expected = engine[case+'_expected'](count_record)
    same(parse(content['ACTUAL_RETURN.json']), literal({'case': case, 'exception': None,
                                                       'arguments_after': [], 'value': expected}))
    same(parse(content['FINISH.json']), {'status': 'RAW_RETURN_PENDING_DISTINCT_SAVED_REVIEW',
         'case': case, 'all_pinned_input_closing_bytes_match': True, 'TWO_CARRIER_adopted': False,
         'physical_release': False, 'full_exact_return_retained': True})
    require({p.name for p in directory.iterdir()} == FILES, 'closing whole census')
    for name, value in content.items():
        require(raw(directory/name) == value, 'closing saved bytes '+name)
    require(pin(config_pin) == config_raw and pin(ACCEPTANCE) == acceptance_raw, 'closing root pins')
    require(pin({'path': str(PRODUCER), 'sha256': PRODUCER_HASH}) == producer_raw and
            pin({'path': str(ENGINE), 'sha256': ENGINE_HASH}) == engine_raw, 'closing method pins')
    for name, p in LINEAGE.items():
        require(pin(p) == originals[name], 'closing original lineage '+name)
    return {'status': 'PASS_COMPLETE_EXACT_CRITICAL_INSTRUMENT_OUTPUT_ONLY', 'case': case,
            'files': {k: {'bytes': len(v), 'sha256': hashlib.sha256(v).hexdigest()} for k, v in content.items()},
            'independent_math_source_sha256': ENGINE_HASH, 'complete_count_domains': domains,
            'independent_count_stream_sha256': count_hash.hexdigest(),
            'comparison': 'ALL_TYPED_RATIONAL_RETURN_FIELDS_EXACT',
            'shared_math_dependency': 'AXIS_SPLIT_IDENTITY_AND_C90_TAIL_PROOF',
            'different_count_algorithm': 'DIRECT_BINOMIAL_PRODUCTS_NOT_INCREMENTAL_SUMMAND_RATIO',
            'runtime_acceptance': 'ROOT_SEPARATE_GATE', 'TWO_CARRIER_adopted': False,
            'physical_prediction_released': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--config', required=True)
    parser.add_argument('--config-sha256', required=True)
    a = parser.parse_args()
    print(json.dumps(check(a.input, {'path': a.config, 'sha256': a.config_sha256}),
                     indent=2, allow_nan=False))

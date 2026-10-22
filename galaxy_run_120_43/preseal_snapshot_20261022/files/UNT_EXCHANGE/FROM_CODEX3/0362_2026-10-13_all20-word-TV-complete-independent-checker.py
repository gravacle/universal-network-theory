"""SOURCE ONLY. Root-only whole nine-file accepted-law TV comparison.
No producer or history engine science executes. Full180 exact bounds and
decisions, all80original laws and all190accepted energy records retained.
CLI --archive ORIGINAL_ABS --output FRESH_ABS_DIRECTORY.
"""
import argparse
from fractions import Fraction as Q
import hashlib
from itertools import combinations
import json
import os
from pathlib import Path
import resource
import sys
import time
from types import SimpleNamespace

EX = Path('/Users/bgm/Research/UNT_EXCHANGE')
B = EX/'KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001'
CALLER = EX/'lanes/P49_CODEX2/p64_all20_word_tv_root_caller_v001.py'
CALLER_SHA = '09ad6cec74ac6c9841cf5ade8c18d26b8199ec1d033de49ef5126602dbdf5159'
CUSTODY = EX/'FROM_CODEX3/0331_2026-10-13_warning-independent-custody.py'
CUSTODY_SHA = '6fab6cd9636fca18463fe158f0da7b1641e51ff9fe3276e4a52c4220edfb5f47'
ENGINE = {'path': str(EX/'lanes/P49_CODEX2/history_next_stage_prospect_v001.py'),
          'sha256': '4a8940a2bed28ed1a5cdf47382498f066aade9b1de75ef1dccbed0ce094803f9'}
OLD = (
    ('P49_STAGE0_DECISION_WHOLE_REUSE_GATE_V002.json', 'd61a4efd14fc4754aa1b2540a76efd4c53447d35a1b5d70390788261f10c7a0d'),
    ('P49_STAGE1_DECISION_WHOLE_REUSE_GATE_V001.json', '6cf0885de5ff7d5adccd9256e9c2829a382f7c70c9a3e3fdbdfa980c3dca5374'),
    ('P49_STAGE2_DECISION_WHOLE_REUSE_GATE_V001.json', '9ba6f8d667874d2b7f883c6ad6966aae2fb911540cf6a5fa6cf64f49c2854d97'),
    ('P49_STAGE3_DECISION_WHOLE_REUSE_GATE_V001.json', '11239bb6ba95312ba297157658f3a6c814a94587917c1d96167e5ec52cf4e88b'))
C157 = {'path': str(B/'P64_NATIVE_EXACT_READ_ACCEPTANCE_V001.json'),
        'sha256': '2574982b6064be5a802453d34faf4f60f00c99b9de022e5f9c6886ac1c199444'}
CENSUS = {'path': str(B/'P64_NATIVE_CENSUS_OUTPUT_V001/ACTUAL_RETURN.json'),
          'sha256': 'c190b863f63c8c93077b5b31742f6edd1b8c32e970d1f19621798a00ed1692cd'}
WORDS = ('00', '01', '10', '11')
TYPES = ('OLD_CARRIER_SITE0', 'OLD_CARRIER_SITE1', 'OLD_READY_SITE0',
         'OLD_COHERENT_PLUS_I', 'OLD_COHERENT_MINUS_I')
TIMES = ('1/8', '1/4', '1/2', '1')
ROLE = 'P64_ALL20_WORD_TV_V001'
CAPS = {'cpu': 1, 'rss_bytes': 512*2**20, 'seconds': 120,
        'output_bytes': 64*2**20, 'scientific_reserve_bytes': 56*2**20}
FILES = {'START.json', 'ROOT_CONFIG.json', 'SOURCE_SNAPSHOTS.json', 'GATE_SNAPSHOTS.json',
         'INPUT_LAWS.json', 'ACTUAL_PRE.json', 'ACTUAL_RETURN.json', 'INPUT_MANIFEST.json', 'FINISH.json'}


def need(ok, why):
    if not ok:
        raise ValueError(why)


def wire(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, dict):
        return {k: wire(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [wire(v) for v in value]
    return value


def rational_law(law):
    need(set(law) == set(WORDS), 'every word, no marginal substitution')
    out = []
    for word in WORDS:
        pair = law[word]
        need(type(pair) is list and len(pair) == 2, 'complete original closed probability interval')
        lo, hi = map(Q, pair)
        need(0 <= lo <= hi <= 1 and hi-lo <= Q(1, 512), 'probability range and frozen halfwidth')
        out.append((lo, hi))
    need(sum(p[0] for p in out) <= 1 <= sum(p[1] for p in out), 'normalizable interval box')
    return out


def tv(a, b):
    """Half L1 box distance; no producer engine calls or normalizing edits."""
    a, b = rational_law(a), rational_law(b)
    lower, upper = Q(0), Q(0)
    for (al, ah), (bl, bh) in zip(a, b):
        # Distance between intervals, and farthest opposite-endpoint distance.
        lower += max(Q(0), al-bh, bl-ah)
        upper += max(abs(al-bh), abs(ah-bl))
    return lower/2, min(Q(1), upper/2)


def decisions(laws, energy, guard):
    expected = {w+':'+kind for w in WORDS for kind in TYPES}
    need(set(laws) == expected and set(energy['preparations']) == expected, 'all20 complete initial preparations')
    for value in laws.values():
        need(set(value) == {'0', '1', '2', '3'}, 'allfour continuous windows')
        for law in value.values():
            rational_law(law)
    rows = energy['all_190_energy_pairs']
    need(len(rows) == 190, 'whole190 energy pair census')
    lookup = {}
    for row in rows:
        key = tuple(sorted((row['a'], row['b'])))
        need(key[0] != key[1] and set(key) <= expected and key not in lookup, 'unique exact energy pair')
        aa, bb = (energy['preparations'][name] for name in (row['a'], row['b']))
        witnesses = [field for field in ('mean_absolute_energy', 'second_absolute_energy_moment')
                     if Q(aa[field]) != Q(bb[field])]
        need(row['witness_moments'] == witnesses and row['full_measure_equality'] ==
             ('UNEQUAL_PROVED' if witnesses else 'NOT_ESTABLISHED'), 'accepted moment witness interpretation')
        lookup[key] = row
    need(set(lookup) == set(combinations(sorted(expected), 2)), 'all unordered preparation pairs')
    counts = {label: sum(row['full_measure_equality'] == label for row in rows)
              for label in ('UNEQUAL_PROVED', 'NOT_ESTABLISHED')}
    need(counts == {'UNEQUAL_PROVED': 185, 'NOT_ESTABLISHED': 5}, 'actual full accepted energy classification')
    cross, temporal = [], []
    def verdict(bounds, within, resolved):
        lo, hi = bounds
        return within if hi <= Q(1, 64) else resolved if lo > Q(1, 64) else 'UNRESOLVED'
    for stage in range(4):
        for kind in TYPES:
            for left, right in combinations(WORDS, 2):
                a, b = left+':'+kind, right+':'+kind
                bounds = tv(laws[a][str(stage)], laws[b][str(stage)])
                cross.append({'a': a, 'b': b, 'stage': stage, 'T': TIMES[stage], 'TV': bounds,
                    'verdict': verdict(bounds, 'WITHIN_DECLARED_TV_TOLERANCE', 'RESOLVED_INITIAL_WORD_SEPARATION'),
                    'accepted_energy_pair': lookup[tuple(sorted((a, b)))],
                    'energy_controlled_causality': 'NOT_ESTABLISHED'})
                guard()
    for word in WORDS:
        for kind in TYPES:
            key = word+':'+kind
            for stage in range(1, 4):
                bounds = tv(laws[key][str(stage-1)], laws[key][str(stage)])
                temporal.append({'preparation': key, 'previous_stage': stage-1, 'stage': stage,
                    'previous_T': TIMES[stage-1], 'T': TIMES[stage], 'TV': bounds,
                    'verdict': verdict(bounds, 'FINITE_WINDOW_STABILITY_AT_TOLERANCE', 'RESOLVED_WINDOW_CHANGE'),
                    'same_preparation_energy_measure': 'SAME_UNDER_SAME_TIME_INDEPENDENT_H'})
                guard()
    need(len(cross) == 120 and len(temporal) == 60, 'whole180 comparison census')
    return wire({'schema': 'P64_ALL20_WORD_TV_RESULTS_V001', 'threshold': Q(1, 64),
        'all120_cross_initial_word_pairs': cross, 'all60_adjacent_window_pairs': temporal,
        'all190_accepted_energy_pairs': rows, 'global_energy_status_counts': counts,
        'instrument': 'TV_OF_FOUR_AVERAGED_WORD_PROBABILITIES', 'current_j_F_instrument_combined': False,
        'locality': 'NOT_TESTABLE', 'species': 'NOT_TESTABLE', 'D_M': 'NOT_AVAILABLE',
        'ordering': 'UNDETERMINED_NO_ORDERING_FUNCTIONAL', 'finite_window_only': True,
        'DE': False, 'ETH': False, 'stationarity': False, 'physical_motion_release': False})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    def guard():
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024)
        need(rss <= 512*2**20 and time.monotonic()-started <= 120, 'whole independent120s512MiB')
    need(CUSTODY.resolve() == CUSTODY and not CUSTODY.is_symlink()
         and CUSTODY.stat().st_size <= 65536, 'plain independent metadata helper')
    rawhelper = CUSTODY.read_bytes()
    need(hashlib.sha256(rawhelper).hexdigest() == CUSTODY_SHA, 'literal metadata helper hash')
    ns = {'__name__': 'root_tv_distinct_custody', '__file__': str(CUSTODY)}
    exec(compile(rawhelper, str(CUSTODY), 'exec'), ns)
    C = SimpleNamespace(**ns)
    exact, decode = C.exact, C.decode
    I = C.Inputs(guard)
    I.read(CUSTODY, CUSTODY_SHA, 65536)
    I.read(Path(__file__).resolve(), cap=65536)
    root, output = args.archive, args.output
    need(root.is_absolute() and root.resolve() == root and root.is_dir()
         and not root.is_symlink() and B in root.parents, 'literal root original scientific archive')
    need(output.is_absolute() and output.resolve() == output and not output.exists()
         and B in output.parents, 'fresh root-owned output')
    need({p.name for p in root.iterdir()} == FILES, 'allnine original scientific artifacts')
    data, meta = {}, {}
    for name in sorted(FILES):
        data[name] = decode(I.read(root/name, cap=56*2**20))
        pin = I.pins[str(root/name)]
        meta[name] = {'bytes': pin['bytes'], 'sha256': pin['sha256']}
    need(sum(v['bytes'] for v in meta.values()) <= 56*2**20, 'whole original science reserve')
    original_order = []
    def read(pin, cap=16*2**20):
        raw = I.pin(pin, cap=cap)
        if pin['path'] not in original_order:
            original_order.append(pin['path'])
        return raw
    def doc(pin):
        return decode(read(pin))
    def rootdoc(pin):
        need(Path(pin['path']).parent == B, 'actual root-owned gate/authority')
        return doc(pin)
    def closure(pin):
        value = doc(pin)
        need(value['returncode'] == 0 and value['cap_stop'] is None
             and value['all_closing_pins_match'] is True, 'closed original successful process')
        return value
    def member(pin, closed, base):
        path, folder = Path(pin['path']), Path(base)
        need(path.is_absolute() and folder.is_absolute() and path.resolve() == path
             and folder.resolve() == folder, 'whole original literal file namespace')
        record = closed['outputs'][str(path.relative_to(folder))]
        need(record['sha256'] == pin['sha256'], 'original member digest')
        raw = read(pin)
        need(len(raw) == record['bytes'], 'original whole member bytecount')
        return decode(raw)
    configpin = data['START.json']['config']
    cfg = rootdoc(configpin)
    exact(data['ROOT_CONFIG.json'], cfg, 'whole config snapshot')
    need(set(cfg) == {'schema', 'role', 'released_by', 'execute', 'caps', 'output', 'source_gate', 'input_gate'}, 'closed release fields')
    need(cfg['schema'] == 'P64_ALL20_WORD_TV_RELEASE_V001' and cfg['role'] == ROLE
         and cfg['released_by'] == '/root' and cfg['execute'] is True and cfg['output'] == str(root), 'actual root release')
    exact(cfg['caps'], CAPS, 'whole role caps')
    sg, ig = rootdoc(cfg['source_gate']), rootdoc(cfg['input_gate'])
    callerpin = {'path': str(CALLER), 'sha256': CALLER_SHA}
    rawcaller = read(callerpin, 65536)
    need(sg['acceptor'] == '/root' and str(sg['status']).startswith('PASS') and sg['role'] == ROLE
         and sg['reviewer_id'] not in (None, 'Codex2'), 'actual distinct producer source review')
    exact(sg['caller'], callerpin, 'complete caller pin')
    exact(sg['engine'], ENGINE, 'unchanged qualified engine pin')
    need(ig['schema'] == 'P64_ALL20_WORD_TV_WHOLE_INPUT_GATE_V001' and ig['acceptor'] == '/root'
         and ig['status'] == 'ROOT_ACCEPTED_ALL80_WORD_LAWS', 'actual accepted full input gate')
    for field in ('all60_newword_stages_distinctly_accepted', 'all20_original_q11_results_accepted',
                  'complete_original_opening_checked', 'complete_original_closing_root_obligation'):
        need(ig[field] is True, 'whole input obligation '+field)
    need(set(ig['newword_bindings']) == {w+':'+kind+':'+str(stage) for w in WORDS[:3]
         for kind in TYPES for stage in range(4)}, 'all60 new bindings')
    accepted, energy_return = doc(C157), doc(CENSUS)
    need(accepted['claim'] == 'C-157' and accepted['complete_original_runtime_custody'] is True, 'accepted exact energy provenance')
    need(energy_return['case'] == 'census' and energy_return['seed'] is None
         and energy_return['exception'] is None, 'complete actual census return')
    energy = energy_return['value']
    laws = {w+':'+kind: {} for w in WORDS for kind in TYPES}
    bindings = {}
    def result_law(result, seed, stage, pilot=False):
        if not pilot:
            need(result['schema'] == 'P49_NATIVE_HISTORY_STAGE_RESULT_V001' and result['seed'] == seed
                 and type(result['stage']) is int and result['stage'] == stage, 'whole stage result identity')
        need(Q(result['T']) == Q(TIMES[stage]) and type(result['panels']) is int
             and result['panels'] == (64, 128, 256, 512)[stage], 'complete continuous window/panels')
        need(result['finite_window_only'] is True and result['DE'] is False
             and result['physical_preparation'] is False and set(result['averaged_words']) == set(WORDS), 'original scope and allfour words')
        law = {w: result['averaged_words'][w]['interval'] for w in WORDS}
        rational_law(law)
        return law
    for stage, (name, digest) in enumerate(OLD):
        old = doc({'path': str(B/name), 'sha256': digest})
        need(old['status'] == 'ROOT_ACCEPTED_FOR_DECISIONS' and old['issued_by'] == '/root', 'original old reuse authority')
        entries = [r for r in old['bindings'] if r['side'] == 'current']
        need(len(entries) == 5 and {r['seed'] for r in entries} == set(TYPES), 'allfive old preparations')
        for entry in entries:
            kind = entry['seed']
            binding = entry['binding']
            need(binding['seed'] == kind and type(binding['stage']) is int and binding['stage'] == stage, 'literal old binding identity')
            auth = doc(binding['root_reuse_authorization'])
            closed = closure(binding['process_closure'])
            exact(auth['process_closure'], binding['process_closure'], 'old closure authority')
            exact(auth['independent_report'], binding['independent_report'], 'old report authority')
            need(auth['issued_by'] == '/root' and auth['complete_original_output_review'] is True
                 and auth['whole_ancestry_review'] is True, 'old complete root acceptance')
            result = member(binding['result'], closed, binding['archive_root'])
            report = doc(binding['independent_report'])
            exact(result, report['finite_window_result'], 'entire independently reconstructed old result')
            for pin in entry['whole_envelope_receipts']:
                doc(pin)
            if 'original_reader_closure' in entry:
                rc = closure(entry['original_reader_closure'])
                member(binding['independent_report'], rc, entry['reader_payload_root'])
            pilot = binding['kind'] == 'PILOT_A'
            need((kind == TYPES[0] and stage == 0) if pilot else binding['kind'] == 'STAGE_V001', 'unique actual original pilot')
            key = '11:'+kind
            laws[key][str(stage)] = result_law(result, kind, stage, pilot)
            bindings[key+':'+str(stage)] = binding
    for word in WORDS[:3]:
        for kind in TYPES:
            key = word+':'+kind
            seed = 'Q'+word+'_'+kind
            for stage in range(4):
                binding = ig['newword_bindings'][key+':'+str(stage)]
                need(set(binding) == {'seed', 'stage', 'archive_root', 'root_reuse_authorization', 'process_closure',
                     'independent_report', 'reader_process_closure', 'result'}, 'closed complete new binding')
                need(binding['seed'] == seed and type(binding['stage']) is int and binding['stage'] == stage, 'new family identity')
                auth = rootdoc(binding['root_reuse_authorization'])
                need(auth['schema'] == 'P64_NEW_WORD_STAGE_REUSE_AUTHORIZATION_V001'
                     and auth['status'] == 'ROOT_ACCEPTED_FOR_NEW_WORD_STAGE_REUSE' and auth['issued_by'] == '/root'
                     and auth['reviewer_id'] not in (None, 'Codex3') and auth['complete_original_output_review'] is True
                     and auth['whole_ancestry_review'] is True, 'actual distinct accepted new history')
                for field in ('seed', 'stage', 'archive_root', 'process_closure', 'independent_report', 'reader_process_closure'):
                    exact(auth[field], binding[field], 'full newword authority '+field)
                acceptance = rootdoc(auth['root_acceptance'])
                need(acceptance['acceptor'] == '/root' and acceptance['all15_distinct_complete_comparisons'] is True
                     and acceptance['complete_original_producer_reader_runtime_custody'] is True
                     and type(acceptance['stage']) is int and acceptance['stage'] == stage, 'whole stage root acceptance')
                hits = [row for row in acceptance['records'] if row['seed'] == seed and row['stage'] == stage]
                need(len(hits) == 1, 'one actual accepted preparation row')
                for field in ('archive_root', 'process_closure', 'independent_report', 'reader_process_closure'):
                    exact(hits[0][field], binding[field], 'actual accepted row '+field)
                closed, rc = closure(binding['process_closure']), closure(binding['reader_process_closure'])
                need(closed['complete_success'] is True and rc['complete_success'] is True
                     and closed['payload_root'] == binding['archive_root']
                     and 'runtime_outputs' in closed and 'runtime_outputs' in rc, 'two original processes/two namespaces each')
                need(binding['result']['path'] == str(Path(binding['archive_root'])/'RESULT.json'), 'literal full new result member')
                result = member(binding['result'], closed, binding['archive_root'])
                report = member(binding['independent_report'], rc, rc['payload_root'])
                need(report['complete_saved_reconstruction'] is True and report['whole_original_output_checked'] is True
                     and report['whole_same_seed_ancestry_checked'] is True and report['seed'] == seed
                     and type(report['stage']) is int and report['stage'] == stage, 'full new independent arithmetic/ancestry')
                exact(result, report['finite_window_result'], 'entire new result independent reconstruction')
                laws[key][str(stage)] = result_law(result, seed, stage)
                bindings[key+':'+str(stage)] = binding
    rawengine = read(ENGINE, 65536)
    pid = data['START.json']['pid']
    need(type(pid) is int and pid > 0, 'original actual PID field')
    exact(data['START.json'], {'schema': 'P64_ALL20_WORD_TV_START_V001', 'executor': '/root',
          'pid': pid, 'config': configpin, 'caps': CAPS, 'external_supervisor_required': True,
          'scientific_acceptance': False}, 'wholeSTART')
    exact(data['SOURCE_SNAPSHOTS.json'], {'caller': rawcaller.decode(), 'engine': rawengine.decode()}, 'all source snapshot bytes')
    exact(data['GATE_SNAPSHOTS.json'], {'source_gate': sg, 'input_gate': ig}, 'whole gate snapshots')
    exact(data['INPUT_LAWS.json'], {'all80_laws': laws, 'all80_original_bindings': bindings,
          'accepted_census': CENSUS, 'acceptance': C157}, 'all80 original laws/bindings')
    exact(data['ACTUAL_PRE.json'], {'function': 'compare_all180_word_TV', 'laws': laws,
          'accepted_energy_census': energy, 'engine': ENGINE, 'phase': 'BEFORE_ACTUAL_CALL'}, 'complete actual PRE')
    value = decisions(laws, energy, guard)
    exact(data['ACTUAL_RETURN.json'], {'exception': None, 'value': value}, 'all180 exact bounds/decisions and190energyrows')
    exact(data['INPUT_MANIFEST.json'], {'complete_consumed_input_files': [I.pins[path] for path in original_order],
          'whole_historical_runtime_custody_checked_here': False,
          'root_complete_original_closing_required': True}, 'complete ordered original consumed inputs')
    exact(data['FINISH.json'], {'schema': 'P64_ALL20_WORD_TV_FINISH_V001', 'pid': pid,
          'files_before_finish': {name: rec for name, rec in meta.items() if name != 'FINISH.json'},
          'all_consumed_input_closing_bytes_match': True,
          'status': 'RAW_COMPLETE_REQUIRES_DISTINCT_COMPARISON_AND_ROOT_CUSTODY',
          'crossword_pairs': 120, 'adjacent_window_pairs': 60,
          'new_propagation': False, 'physical_motion_release': False}, 'wholeFINISH')
    I.close()
    need({p.name for p in root.iterdir()} == FILES, 'whole closing nine-file census')
    report = {'schema': 'CODEX3_ALL20_WORD_TV_COMPLETE_INDEPENDENT_COMPARISON_V001',
              'status': 'PASS_COMPLETE_SAVED_COMPARISON', 'all9_scientific_files_compared': True,
              'all80_full_original_laws_bound': True, 'all120_crossword_and60_window_bounds_compared': True,
              'all190_energy_rows_and_actual_pair_witnesses_checked': True,
              'full_independent_decisions': value, 'complete_scientific_census': meta,
              'all_opened_input_closing_pins': list(I.pins.values()),
              'producer_engine_scientific_functions_executed': False,
              'whole_historical_runtime_custody_checked_here': False,
              'actual_current_runtime_custody_checked_here': False,
              'root_full_historical_current_runtime_custody_required': True,
              'physical_motion_release': False}
    raw = (json.dumps(report, indent=2, allow_nan=False)+'\n').encode()
    need(len(raw) <= 56*2**20, 'complete independent report reserve')
    guard()
    output.mkdir(exist_ok=False)
    with (output/'INDEPENDENT_REPORT.json').open('xb') as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    print(json.dumps({'status': report['status'], 'report_sha256': hashlib.sha256(raw).hexdigest()}))


if __name__ == '__main__':
    main()

"""Codex3 independent A296 R3 arithmetic review and review-object writer.

Only explicitly dispatched source/record bytes and two allowed original stage
records per point are read. No producer, prepare, adapt, solver or CLI executes.
"""
from pathlib import Path
import ast
import copy
import datetime
import hashlib
import json
import math
import os
import re
import resource
import subprocess

BASE = Path('/Users/bgm/Research/UNT_EXCHANGE')
ART = BASE / 'claude_artifacts'
OUT = ART / 'a296_r3_signer_reviews_cx3'
DISPATCH = BASE / 'FROM_CLAUDE3/0324_2026-10-21_deputy-D016-Codex3-A296-R3-signer-reviews-rows-302-501-504-exact-sources-and-review-contract.md'
DISPATCH_SHA = '429100b0df22fb364402c30b06d2f8b87076e181110fd0bf6091088db7d1d0f1'
ROOT = BASE / 'FROM_CODEX/0857_2026-10-21_claude3_deputy_prepare_root_Thu1pm_adoption_checklist_A296_chain.md'
ROOT_SHA = '101787e0a351edc957d9f41602ee58bb33835812609cd5430990283758684116'
V006 = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md')
NEW_VERDICT = 'NUMERICAL_RULE_PASSED_NEGLIGIBLE_SHELLS_NOTED_REVIEW_REQUIRED'
ROWS = {302: 46, 501: 76, 504: 73}
CACHE = {}
INPUTS = {}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def serialized(obj):
    return (json.dumps(obj, indent=2, sort_keys=True, allow_nan=False) + '\n').encode()


def strict(raw):
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise ValueError('duplicate JSON key')
            out[key] = value
        return out
    def nonfinite(value):
        raise ValueError('nonfinite JSON token: ' + value)
    obj = json.loads(raw, object_pairs_hook=pairs, parse_constant=nonfinite)
    def walk(value):
        if isinstance(value, float):
            assert math.isfinite(value)
        elif isinstance(value, dict):
            for item in value.values():
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)
    walk(obj)
    return obj


def read_exact(path, expected=None):
    path = Path(path)
    if path not in CACHE:
        raw = path.read_bytes()
        CACHE[path] = raw
        INPUTS[str(path)] = {'path': str(path), 'sha256': sha(raw), 'bytes': len(raw)}
    raw = CACHE[path]
    if expected is not None:
        assert sha(raw) == expected, 'byte pin mismatch: ' + str(path)
    return raw


def pin(path):
    path = Path(path)
    return {'path': str(path), 'sha256': sha(read_exact(path))}


def write_new(path, raw):
    with Path(path).open('xb') as handle:
        handle.write(raw)


def named(pins, name):
    matches = [Path(p) for p in pins if Path(p).name == name]
    assert len(matches) == 1, (name, matches)
    return matches[0]


def extract(raw, names, namespace, filename):
    nodes = [n for n in ast.parse(raw).body if isinstance(n, ast.FunctionDef) and n.name in names]
    assert {n.name for n in nodes} == set(names)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), filename, 'exec'), namespace)
    return namespace


def independent_row(row, shell_lo, pins, common_checks):
    paths = {
        'request': named(pins, f'REQUEST_ROW{row}_CX2V003.json'),
        'stage': named(pins, f'STAGE_ONLY_ROW{row}_CX2V003.json'),
        'successor': named(pins, f'EPS_ROW{row}_CX2V001.json'),
        'audit': named(pins, f'DENSE_ROW{row}_S{shell_lo}_CX2V001.json'),
    }
    docs = {k: strict(read_exact(p)) for k, p in paths.items()}
    req, stage, new, audit = [docs[k] for k in ('request', 'stage', 'successor', 'audit')]
    oldref = new['predecessor']['record']
    assert oldref['path'] in pins and oldref['sha256'] == pins[oldref['path']]
    paths['predecessor'] = Path(oldref['path'])
    old = strict(read_exact(paths['predecessor']))
    docs['predecessor'] = old
    # A205 four-file per-point scope: only EPS_NUMERIC, STAGE_EPS and
    # STAGE_CONTEXT are read here. No spec, POINT_START or dependency is opened.
    for role, stem in [('original_stage', 'STAGE_EPS'), ('context', 'STAGE_CONTEXT')]:
        ref = req['eps_stage' if role == 'original_stage' else role]
        p = Path(ref['path'])
        assert p.parent == paths['predecessor'].parent
        assert p.name == paths['predecessor'].name.replace('EPS_NUMERIC', stem)
        paths[role] = p
        docs[role] = strict(read_exact(p, ref['sha256']))
    oldstage, ctx = docs['original_stage'], docs['context']
    checks = dict(common_checks)
    def ck(label, condition):
        checks[label] = bool(condition)
    rp = pin(named(pins, 'eps_negligible_rule_cx2v003.py'))
    ap = pin(named(pins, 'dense_eps_audit_cx2v002.py'))
    op = pin(named(pins, 'point_response_producer_cx2v002.py'))
    au = pin(named(pins, 'A296_AUTHORITY_CX2V001.json'))
    sp = pin(named(pins, 'cp1_saved_eps_stage_cx2v002.py'))
    failures = [i for i, s in enumerate(old['shells']) if s['certified'] is False]
    ck('exactly_one_failed_shell', failures == [shell_lo - 4])
    ck('registered_full_coverage', len(old['shells']) == 178 and old['required_coverage_inverse_kpc'] == [4, 182]
       and old['status'] == 'TESTED' and old['settings'] == 'registered'
       and old['coverage_complete'] is True and old['full_registered_search_executed'] is True)
    ck('point_and_identity_binding', stage['key'] == old['point_sha256'] == new['point_sha256'] == audit['point_sha256'] == ctx['key'] == ctx['point_sha256']
       and sha(canonical(old['identity'])) == stage['key']
       and old['identity'] == new['identity'] == audit['identity'])
    ck('custody_binding', old['custody'] == new['custody'] == ctx['custody']
       and sha(canonical(old['custody'])) == stage['custody_sha256'] == ctx['custody_sha256'])
    ck('context_checks_and_dependencies', all(v is True for v in ctx['checks'].values())
       and old['dependencies'] == ctx['source_pins'])
    ck('request_stage_binding', req['successor'] == stage['record'] == pin(paths['successor'])
       and stage['request'] == pin(paths['request']) and stage['generator'] == sp)
    ck('old_stage_binding', stage['original_stage'] == req['eps_stage'] == pin(paths['original_stage'])
       and oldstage['record'] == oldref and oldstage['key'] == stage['key'] and oldstage['ok'] is False)
    ck('R4_original_failures_only', oldstage['checks'] == stage['original_checks']
       and {k for k, v in stage['original_checks'].items() if v is not True}
       == {'registered_discrete_CERTIFIED', 'verdict_review_required'})
    ck('stage_status', stage['ok'] is True and stage['status'] == 'TESTED'
       and all(v is True for v in stage['checks'].values())
       and stage['numerical_only'] is True and stage['production_admissible'] is False
       and stage['approved_signer_review_required'] is True)
    for i, s in enumerate(old['shells'], 4):
        nf, levels = s['refinements'], s['levels']
        ck(f'shell_{i}_range', s['range_inverse_kpc'] == [i, i + 1] and s['lo_inverse_kpc'] == i and s['hi_inverse_kpc'] == i + 1)
        ck(f'shell_{i}_discrete_history', type(nf) is int and nf in (0, 1, 2)
           and type(s['certified']) is bool and s['certified'] == (nf != 2)
           and set(levels) == ({'0', '1'} if nf == 0 else {'0', '1', '2'})
           and s['eps_base'] == levels['0' if nf == 0 else '1']['eps']
           and s['eps_refined'] == levels['1' if nf == 0 else '2']['eps']
           and (nf == 0 or levels['1']['eps'] > 1.1 * levels['0']['eps'])
           and (s['eps_refined'] <= 1.1 * s['eps_base']) == (nf != 2))
        ck(f'shell_{i}_component_dominance', s['eps'] >= max(s['eps_base'], s['eps_refined'], s['eps_envelope'], s['actual']['estimate']) >= 0
           and s['eps_envelope'] >= s['envelope']['estimate'] >= 0)
        ck(f'shell_{i}_unaffected_or_target', i == shell_lo or canonical(s) == canonical(new['shells'][i - 4]))
    s = old['shells'][shell_lo - 4]
    n = new['shells'][shell_lo - 4]
    measured = s['eps']
    growth = abs(s['levels']['2']['eps'] - s['levels']['1']['eps'])
    ratio = audit['dense'] / audit['production']
    ck('R1a', 10 * measured <= 0.1 * old['eps_max'])
    ck('R1b', growth <= 1e-6)
    ck('R1c', ratio <= 1.05 and audit['dense_over_production'] == ratio)
    ck('R1d', s['refinements'] == 2 and all(v['certified'] is True for j, v in enumerate(old['shells']) if j != shell_lo - 4))
    ck('audit_scope', audit['row'] == row and audit['range_inverse_kpc'] == s['range_inverse_kpc']
       and audit['status'] == 'TESTED' and audit['settings'] == 'registered'
       and audit['source_record'] == oldref and audit['production'] == s['envelope']['estimate']
       and audit['original_producer'] == op and audit['audit_producer'] == ap
       and audit['spec'] == req['spec'])
    ds = audit['dense_search']
    ck('audit_search_settings', all(ds[k] == v for k, v in {
        'estimate': audit['dense'], 'torus_m': 20, 'direction_count': 400,
        'starts': 16, 'n_grid': 16000000, 'radial_fractions': [0, .25, .5, .75, 1]}.items())
       and audit['dense'] >= ds['grid_max'] >= 0)
    expected_shell = copy.deepcopy(s)
    expected_shell.update(eps=10 * measured, eps_measured_before_negligible_substitution=measured,
        accepted_negligible=True, acceptance='ACCEPTED_NEGLIGIBLE',
        negligible_acceptance_evidence={'M': 10, 'f': .1, 'absolute_floor': 1e-6,
            'absolute_level2_minus_level1': growth, 'dense_over_production': ratio,
            'dense_audit': pin(paths['audit'])})
    ck('R2_exact_shell_delta', canonical(n) == canonical(expected_shell))
    ck('R2_maximum_unchanged', new['eps_max'] == old['eps_max'] == max(x['eps'] for x in new['shells'])
       and new['eps_max_shell'] == old['eps_max_shell']
       and any(x['eps'] == old['eps_max'] and x['range_inverse_kpc'] == old['eps_max_shell'] for x in old['shells']))
    ck('R3_verdict', new['verdict'] == NEW_VERDICT and new['successor_rule_verdict'] == 'ACCEPTED_NEGLIGIBLE'
       and new['accepted_shells'] == [s['range_inverse_kpc']] and new['approved_signer_review_required'] is True)
    expected = copy.deepcopy(old)
    expected['shells'][shell_lo - 4] = expected_shell
    expected.update(verdict=NEW_VERDICT, successor_rule_verdict='ACCEPTED_NEGLIGIBLE',
        accepted_shells=[copy.deepcopy(s['range_inverse_kpc'])], approved_signer_review_required=True,
        predecessor={'record': oldref, 'producer': op, 'verdict': old['verdict'],
                     'registered_discrete_verdict': old['registered_discrete_verdict']},
        producer=rp, rule_authority={**au, 'heading': 'A296'},
        successor_date_u=new['successor_date_u'],
        successor_limitations='Saved numerical-rule re-evaluation only. No new supremum guarantee or scientific admission. Approved-signer review and root adoption required.')
    ck('independent_complete_successor_byte_reconstruction', serialized(expected) == read_exact(paths['successor']))
    trace = {'accepted_shells': copy.deepcopy(new['accepted_shells']), 'audit_producer_sha256': ap['sha256'],
        'audit_ref': pin(paths['audit']), 'authority_sha256': au['sha256'], 'predecessor_ref': oldref,
        'reevaluator_sha256': rp['sha256'], 'retains_discrete_failure': True}
    ck('trace_exact_and_all_pins_authenticated', canonical(trace) == canonical(stage['a296_acceptance']))
    lineage = stage['numeric_lineage']
    ck('lineage_pins', all(lineage[k] == v for k, v in {
        'numeric_record': pin(paths['successor']), 'predecessor_record': oldref,
        'original_producer': op, 'rule': rp, 'authority': au, 'dense_audit': pin(paths['audit']),
        'audit_producer': ap, 'accepted_shells': new['accepted_shells']}.items()))
    ck('R4_failure_retained', old['registered_discrete_verdict'] == old['verdict'] == new['registered_discrete_verdict'] == 'EPS_UNCERTIFIED'
       and n['certified'] is False and n['refinements'] == 2 and n['levels'] == s['levels'])
    ck('A297_numerical_convention', all(new[k] is False for k in ('rigorous_supremum', 'production_admissible', 'covers_all_consumed_states')))
    return {'row': row, 'checks': checks, 'failed': [k for k, v in checks.items() if not v],
        'metrics': {'accepted_shells': new['accepted_shells'], 'measured_eps': measured,
                    'substituted_eps': n['eps'], 'eps_max': new['eps_max'],
                    'R1a_margin': .1 * old['eps_max'] / (10 * measured),
                    'R1b_absolute_step': growth, 'R1c_ratio': ratio},
        'inputs': [pin(p) for p in paths.values()]}, stage, new


def make_review(result, stage, bridge, date_u):
    assert not result['failed']
    return {'schema': 'UNT_POINT_EPS_REVIEW_CX2V001', 'verdict': 'APPROVED',
        'reviewer_lane': 'Codex3', 'distinct_from_producer_lane': True,
        'numeric_ref': copy.deepcopy(stage['record']), 'point_sha256': stage['key'],
        'custody_sha256': stage['custody_sha256'], 'adapter_sha256': bridge['sha256'],
        'accepts_registered_numerical_estimate_not_rigorous_sup': True,
        'accepts_a296_negligible_shells': True,
        'a296_acceptance': copy.deepcopy(stage['a296_acceptance']),
        'date_u': date_u, 'reviewed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'signature': 'Codex3, ' + date_u, 'row': result['row'], 'metrics': result['metrics'],
        'scope': 'A296 R3 numerical-convention review of these exact saved bytes. No rigorous supremum, future-state coverage, scientific admission or root source/review approval is asserted.',
        'lineage': 'Distinct from original/successor producer author Codex2 and operator Claude2. Operator identity relies on deputy D016 byte review; POINT_START was not reopened.',
        'reliance': 'A297 blinding-clean audit-path replay and whole-campaign/genesis invariance rely on the pinned Claude3 PASS. This signer independently checks saved arithmetic and byte bindings without executing producers.',
        'untested': ['Search or producer execution', 'Actual adapt call and downstream acceptance',
                     'Root approval of these review/source hashes', 'Full scientific dependency provenance beyond the explicit review pins']}


def gate_controls(review, stage, new, pins):
    stage_path = named(pins, 'cp1_saved_eps_stage_cx2v002.py')
    common_path = named(pins, 's4rc1_common_c3v005.py')
    bridge = pin(named(pins, 'point_response_admission_a296_bridge_cx2v002.py'))
    def cached_read(ref):
        assert ref == pin(common_path)
        return read_exact(common_path)
    ns = {'Path': Path, 'os': os, 'json': json, 'ast': ast, 'ART': ART,
          'COMMON': pin(common_path), 'BRIDGE': bridge, 'read': cached_read}
    extract(read_exact(stage_path), ['need', 'canonical', 'lexical', 'safe_existing', '_functions', 'review_gate'], ns, str(stage_path))
    selected = [bridge['sha256'], new['producer']['sha256'],
                stage['numeric_lineage']['audit_producer']['sha256'], stage['numeric_lineage']['original_producer']['sha256']]
    dest = OUT / f"REVIEW_ROW{review['row']}_CX3V001.json"
    results = []
    def call(obj, label, expected, signers=None, producers=None, output=None):
        raw = serialized(obj)
        ref = {'path': str(dest), 'sha256': sha(raw)}
        class MemorySnapshot:
            def doc(self, supplied):
                assert supplied == ref
                return strict(raw)
        context = {'snapshot': MemorySnapshot(), 'start': {'operator_lane': 'Claude2'}, 'successor': new}
        try:
            rv = ns['review_gate'](ref, stage, context, approved_review_sha256=ref['sha256'],
                approved_signer_lanes=['Codex3'] if signers is None else signers,
                approved_producer_sha256=selected if producers is None else producers,
                output_root=OUT / 'DRY_ROOT_OUTPUT_DOES_NOT_EXIST' if output is None else output)
            ok = rv == obj
            reason = None
        except (ValueError, AssertionError) as exc:
            ok = False
            reason = str(exc)
        results.append({'case': label, 'expected_accept': expected, 'observed_accept': ok,
                        'pass': ok == expected, 'reason': reason})
    call(review, 'exact_review', True)
    for field, value in [('reviewer_lane', 'Codex2'), ('distinct_from_producer_lane', False),
                         ('adapter_sha256', '0' * 64), ('point_sha256', '0' * 64),
                         ('custody_sha256', '0' * 64), ('verdict', 'REJECTED'),
                         ('accepts_a296_negligible_shells', False),
                         ('accepts_registered_numerical_estimate_not_rigorous_sup', False)]:
        mutant = copy.deepcopy(review)
        mutant[field] = value
        call(mutant, field, False)
    mutant = copy.deepcopy(review)
    mutant['numeric_ref']['sha256'] = '0' * 64
    call(mutant, 'numeric_pin_mutation', False)
    mutant = copy.deepcopy(review)
    mutant['a296_acceptance']['accepted_shells'][0][0] = int(mutant['a296_acceptance']['accepted_shells'][0][0])
    call(mutant, 'canonical_trace_float_to_int', False)
    mutant = copy.deepcopy(review)
    mutant['note'] = '<FILL'
    call(mutant, 'unfilled_template', False)
    call(review, 'missing_signer_approval', False, signers=[])
    call(review, 'missing_source_approval', False, producers=selected[:-1])
    call(review, 'review_inside_output_root', False, output=OUT)
    return results


def main():
    date_u = subprocess.check_output(['/bin/date', '-u'], text=True).strip()
    dispatch = read_exact(DISPATCH, DISPATCH_SHA).decode()
    read_exact(ROOT, ROOT_SHA)
    pairs = re.findall(r'`(/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/[^`\n]+)` — `([0-9a-f]{64})`', dispatch)
    assert len(pairs) == 24 and len(dict(pairs)) == 24, len(pairs)
    pins = dict(pairs)
    for path, expected in pins.items():
        read_exact(path, expected)
    authority = strict(read_exact(named(pins, 'A296_AUTHORITY_CX2V001.json')))
    current = read_exact(V006).decode()
    a296 = current.split('## A296:', 1)[1].split('\n## A297:', 1)[0]
    prior_review = strict(read_exact(named(pins, 'RESULT_C3V001.json')))
    common_checks = {
        'all_24_dispatch_pins_from_bytes': True,
        'A296_authority_text': sha(authority['text'].encode()) == authority['section_sha256']
            and ('## A296:' + a296).rstrip() == authority['text'].rstrip(),
        'A297_reviewer_PASS_present': prior_review['verdict'] == 'PASS' and prior_review['blocking'] == 0
            and prior_review['checks']['blinding_clean_audit_path_A297'].startswith('PASS'),
    }
    bridge = pin(named(pins, 'point_response_admission_a296_bridge_cx2v002.py'))
    candidates, checks = [], []
    for row, shell_lo in ROWS.items():
        result, stage, new = independent_row(row, shell_lo, pins, common_checks)
        if result['failed']:
            checks.append(result)
            continue
        review = make_review(result, stage, bridge, date_u)
        result['gate_controls'] = gate_controls(review, stage, new, pins)
        result['failed_gate_controls'] = [x['case'] for x in result['gate_controls'] if not x['pass']]
        candidates.append((row, review))
        checks.append(result)
    # Re-hash all actually read inputs before publishing signatures.
    changed = [str(p) for p, raw in CACHE.items() if p.read_bytes() != raw]
    record = {'schema': 'CX3_A296_R3_INDEPENDENT_CHECKS_V001', 'date_u': date_u,
        'rows': checks, 'changed_inputs': changed, 'inputs': list(INPUTS.values()),
        'script': {'path': str(Path(__file__)), 'sha256': sha(Path(__file__).read_bytes())},
        'gate_scope': 'TESTED extracted unchanged review_gate and its path/distinct-review helpers with actual stage/successor and in-memory review bytes. Local test approval arguments are fixtures, not root approvals. No prepare/adapt call. No producer execution.',
        'core_scope': 'FORMAL source inspection of core review predicates; core adapt_saved_eps was not executed.',
        'reliance': 'Pinned Claude3 A297 PASS for actual audit execution/blinding graph and global R4 invariance; not replayed by Codex3.',
        'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    record['verdict'] = 'PASS' if len(candidates) == 3 and not changed and all(not x['failed'] and not x.get('failed_gate_controls') for x in checks) else 'FAIL'
    cp = OUT / 'CHECKS_CX3V001.json'
    write_new(cp, serialized(record))
    print(json.dumps({'verdict': record['verdict'], 'checks': sum(len(x['checks']) for x in checks),
                      'gate_controls': sum(len(x.get('gate_controls', [])) for x in checks),
                      'failures': {x['row']: x['failed'] + x.get('failed_gate_controls', []) for x in checks},
                      'check_record_sha256': sha(cp.read_bytes())}))
    assert record['verdict'] == 'PASS', 'No reviews written on failed checks.'
    handoff = {'schema': 'CX3_A296_R3_HANDOFF_V001', 'date_u': date_u,
               'checks': {'path': str(cp), 'sha256': sha(cp.read_bytes())}, 'reviews': []}
    for row, rv in candidates:
        rv['evidence'] = {'checks': handoff['checks'], 'root_dispatch': pin(ROOT),
                          'deputy_dispatch': pin(DISPATCH), 'signer_tool': record['script']}
        path = OUT / f'REVIEW_ROW{row}_CX3V001.json'
        write_new(path, serialized(rv))
        handoff['reviews'].append({'row': row, 'path': str(path), 'sha256': sha(path.read_bytes()), 'verdict': rv['verdict']})
    hp = OUT / 'HANDOFF_CX3V001.json'
    write_new(hp, serialized(handoff))
    print(json.dumps(handoff, sort_keys=True))


if __name__ == '__main__':
    main()

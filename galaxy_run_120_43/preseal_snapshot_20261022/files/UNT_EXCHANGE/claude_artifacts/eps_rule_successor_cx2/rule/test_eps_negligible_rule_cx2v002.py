#!/usr/bin/env python3
"""In-process saved-record and SYNTHETIC audit-contract tests. No dense search."""
from pathlib import Path
import argparse
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import math
import os
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--rule', required=True)
p.add_argument('--report', required=True)
a = p.parse_args()
source = Path(a.rule)
spec = importlib.util.spec_from_file_location('tested_saved_record_rule', source)
rule = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rule)
base = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3')
registry_path = base/'registry_c2v001/REGISTRY_31pts_20261020T140004Z.json'
registry_raw = registry_path.read_bytes()
registry = json.loads(registry_raw)
source_pin = {'path': str(source), 'sha256': rule.digest(source.read_bytes())}
inputs = [{'path': str(registry_path), 'sha256': rule.digest(registry_raw)}]
tests = []


def check(name, operation, refuse=False):
    try:
        operation()
        ok = not refuse
        error = None
    except rule.Refusal as e:
        ok = refuse
        error = str(e)
    except Exception as e:
        ok = False
        error = type(e).__name__ + ': ' + str(e)
    tests.append({'name': name, 'passed': ok, 'expected_refusal': refuse, 'detail': error})


def demand(v, why):
    if not v:
        raise AssertionError(why)


for point in registry['points'].values():
    pin = point['eps_certificate']
    raw = Path(pin['path']).read_bytes()
    demand(rule.digest(raw) == pin['sha256'], 'genesis input pin mismatch')
    inputs.append(pin)
    record = json.loads(raw)
    snapshot = copy.deepcopy(record)
    def genesis_case(record=record, snapshot=snapshot, pin=pin, raw=raw):
        output = source.parent / ('UNUSED_GENESIS_' + record['point_sha256'][:16] + '.json')
        capture = io.StringIO()
        with contextlib.redirect_stdout(capture), contextlib.redirect_stderr(capture):
            rc = rule.main(['--record', pin['path'], '--record-sha256', pin['sha256'], '--output', str(output)])
        demand(rc == 0 and json.loads(capture.getvalue())['status'] == 'UNCHANGED', 'CLI did not report UNCHANGED')
        demand(not output.exists(), 'genesis output was rewritten')
        demand(Path(pin['path']).read_bytes() == raw and record == snapshot, 'genesis input mutation')
    check('genesis_cli_unchanged_' + record['point_sha256'][:16], genesis_case)

target_paths = {r: next((base/'cp1_run_c3v004b').glob(f'P{r}_*/EPS_NUMERIC_*.json')) for r in (302, 501, 504)}
records = {}
pins = {}
for row, path in target_paths.items():
    raw = path.read_bytes()
    pins[row] = {'path': str(path), 'sha256': rule.digest(raw)}
    records[row] = json.loads(raw)
    inputs.append(pins[row])

synthetic_producer = {'path': '/SYNTHETIC_TEST_ONLY/NOT_A_REAL_AUDIT_PRODUCER.py', 'sha256': 'e'*64}
synthetic_audit_pin = {'path': '/SYNTHETIC_TEST_ONLY/NOT_AN_AUDIT.json', 'sha256': 'd'*64}


def audit_for(rec, row=302):
    shell = next(s for s in rec['shells'] if s['refinements'] == 2)
    production = shell['envelope']['estimate']
    return {'schema': rule.AUDIT_SCHEMA, 'status': 'TESTED', 'settings': 'registered',
            'test_fixture_only': True, 'source_record': pins[row], 'point_sha256': rec['point_sha256'],
            'original_producer': rec['producer'], 'audit_producer': synthetic_producer,
            'range_inverse_kpc': shell['range_inverse_kpc'], 'production': production,
            'dense': production, 'dense_over_production': 1.0,
            'dense_search': {'estimate': production, 'torus_m': 20, 'direction_count': 400,
                             'starts': 16, 'n_grid': 16000000, 'radial_fractions': [0, .25, .5, .75, 1]}}


def run(rec, audit=None, row=302):
    return rule.reevaluate(rec, audit, record_pin=pins[row], audit_pin=synthetic_audit_pin if audit is not None else None,
                           audit_producer_pin=synthetic_producer if audit is not None else None,
                           successor_producer=source_pin, date_u='SYNTHETIC TEST ONLY; NOT AN AUDIT OR ADOPTION')


for row in (302, 501, 504):
    check(f'row{row}_without_real_dense_audit_refused', lambda row=row: run(records[row], None, row), True)
    def positive(row=row):
        original = copy.deepcopy(records[row])
        result, successor = run(original, audit_for(original, row), row)
        demand(original == records[row], 'in-memory source mutated')
        demand(result['status'] == rule.NEW_VERDICT, 'wrong overall verdict')
        demand(successor['registered_discrete_verdict'] == 'EPS_UNCERTIFIED', 'discrete result changed')
        demand(successor['eps_max'] == original['eps_max'] and successor['eps_max_shell'] == original['eps_max_shell'], 'maximum changed')
        for before, after in zip(original['shells'], successor['shells']):
            if before['certified']:
                demand(before == after, 'unaccepted shell changed')
            else:
                demand(after['certified'] is False and after['refinements'] == 2, 'discrete shell history changed')
                demand(after['eps'] == 10*before['eps'] and after['eps_measured_before_negligible_substitution'] == before['eps'], 'wrong substitution')
                demand(after['accepted_negligible'] is True, 'accepted shell undisclosed')
        demand(successor['approved_signer_review_required'] is True and successor['production_admissible'] is False, 'self-admission')
    check(f'row{row}_synthetic_contract_only_conservative_substitution', positive)


def mutated(mutator, audit_mutator=None):
    rec = copy.deepcopy(records[302])
    if mutator:
        mutator(rec)
    audit = audit_for(rec)
    if audit_mutator:
        audit_mutator(audit)
    return run(rec, audit)


def target(rec):
    return next(s for s in rec['shells'] if s['refinements'] == 2)


def floor(rec, above=False):
    sh = target(rec)
    sh['levels']['0']['eps'] = 8e-7
    sh['levels']['1']['eps'] = sh['eps_base'] = 1e-6
    sh['levels']['2']['eps'] = sh['eps_refined'] = math.nextafter(2e-6, math.inf) if above else 2e-6
    sh['eps'] = sh['eps_refined']


def scale_boundary(rec, above=False):
    rec['eps_max'] = rec['shells'][0]['eps'] = 0.001
    sh = target(rec)
    measured = math.nextafter(1e-5, math.inf) if above else 1e-5
    sh['eps'] = sh['eps_envelope'] = sh['envelope']['estimate'] = measured


check('R1a_exact_one_percent_boundary_passes_synthetic_contract', lambda: mutated(scale_boundary))
check('R1a_next_float_above_one_percent_MUST_FAIL', lambda: mutated(lambda r: scale_boundary(r, True)), True)
check('R1b_exact_1e_minus6_growth_boundary_passes_synthetic_contract', lambda: mutated(floor))
check('R1b_next_float_above_growth_floor_MUST_FAIL', lambda: mutated(lambda r: floor(r, True)), True)


def audit_boundary(audit, above=False):
    prod = audit['production']
    dense = prod * 1.05
    while dense / prod > 1.05:
        dense = math.nextafter(dense, -math.inf)
    if above:
        while dense / prod <= 1.05:
            dense = math.nextafter(dense, math.inf)
    audit['dense'] = audit['dense_search']['estimate'] = dense
    audit['dense_over_production'] = dense/prod


check('R1c_dense_ratio_last_float_at_or_below1_05_passes_synthetic_contract', lambda: mutated(None, audit_boundary))
check('R1c_dense_ratio_next_float_above1_05_MUST_FAIL', lambda: mutated(None, lambda a: audit_boundary(a, True)), True)


def second_failure(rec):
    sh = rec['shells'][1]
    sh['levels']['0']['eps'] = 1e-7
    sh['levels']['1']['eps'] = sh['eps_base'] = 2e-7
    sh['levels']['2'] = {'eps': 3e-7}
    sh['eps_refined'] = 3e-7
    sh['certified'] = False
    sh['refinements'] = 2


bad_record_cases = {
    'multiple_failing_shells': second_failure,
    'wrong_settings': lambda r:r.update(settings='smoke'),
    'wrong_status': lambda r:r.update(status='UNTESTED'),
    'coverage_incomplete': lambda r:r.update(coverage_complete=False),
    'full_search_false': lambda r:r.update(full_registered_search_executed=False),
    'wrong_coverage_range': lambda r:r.update(required_coverage_inverse_kpc=[4,181]),
    'shell_gap': lambda r:r['shells'][10].update(range_inverse_kpc=[14,16]),
    'wrong_point_hash': lambda r:r.update(point_sha256='invalid'),
    'wrong_original_producer': lambda r:r['producer'].update(sha256='f'*64),
    'mismatched_eps_max': lambda r:r.update(eps_max=1),
    'bool_measured_eps': lambda r:target(r).update(eps=True),
    'nonfinite_measured_eps': lambda r:target(r).update(eps=float('nan')),
    'infinite_other_field': lambda r:r.update(malformed_extra=float('inf')),
    'unrepresentable_numeric_eps': lambda r:target(r).update(eps=10**500),
    'negative_epsilon': lambda r:target(r).update(eps=-1),
    'missing_level2': lambda r:target(r)['levels'].pop('2'),
    'inconsistent_refinement_pair': lambda r:target(r).update(eps_base=1e-8),
    'false_original_certification': lambda r:target(r).update(certified=True),
    'bool_refinements': lambda r:r['shells'][0].update(refinements=True),
    'bool_coverage_endpoint': lambda r:r.update(required_coverage_inverse_kpc=[False,182]),
    'already_substituted': lambda r:target(r).update(accepted_negligible=True),
}
for name, mutation in bad_record_cases.items():
    check('MUST_FAIL_record_' + name, lambda mutation=mutation: mutated(mutation), True)

bad_audit_cases = {
    'wrong_schema': lambda a:a.update(schema='wrong'),
    'unregistered': lambda a:a.update(settings='smoke'),
    'untested': lambda a:a.update(status='UNTESTED'),
    'wrong_point': lambda a:a.update(point_sha256='0'*64),
    'wrong_source_record': lambda a:a.update(source_record={'path':'wrong','sha256':'0'*64}),
    'wrong_shell': lambda a:a.update(range_inverse_kpc=[47,48]),
    'wrong_original_producer': lambda a:a.update(original_producer={'path':'wrong','sha256':'0'*64}),
    'wrong_audit_producer': lambda a:a.update(audit_producer={'path':'wrong','sha256':'0'*64}),
    'wrong_production': lambda a:a.update(production=1),
    'inconsistent_dense_estimate': lambda a:a.update(dense=1),
    'inconsistent_ratio': lambda a:a.update(dense_over_production=.9),
    'bool_ratio': lambda a:a.update(dense_over_production=True),
    'nan_ratio': lambda a:a.update(dense_over_production=float('nan')),
    'wrong_dense_grid': lambda a:a['dense_search'].update(n_grid=8000000),
    'missing_dense_metadata': lambda a:a.pop('dense_search'),
    'bool_dense_grid': lambda a:a['dense_search'].update(torus_m=True),
    'wrong_radial_grid': lambda a:a['dense_search'].update(radial_fractions=[0,.5,1]),
    'bool_radial_entry': lambda a:a['dense_search'].update(radial_fractions=[False,.25,.5,.75,1]),
}
for name, mutation in bad_audit_cases.items():
    check('MUST_FAIL_audit_' + name, lambda mutation=mutation: mutated(None, mutation), True)

for label, raw in (('duplicate_keys',b'{"eps":1,"eps":2}'), ('NaN_token',b'{"eps":NaN}'), ('malformed',b'{bad')):
    check('MUST_FAIL_JSON_' + label, lambda raw=raw:rule.strict_json(raw), True)


def cli_refusal(args, output=None):
    capture = io.StringIO()
    with contextlib.redirect_stdout(capture), contextlib.redirect_stderr(capture):
        rc = rule.main(args)
    demand(rc == 2 and json.loads(capture.getvalue())['status'] == 'REFUSED', 'CLI not cleanly refused')
    if output:
        demand(not Path(output).exists(), 'refused CLI wrote output')


unused = str(source.parent/'UNUSED_FAILED_CLI_OUTPUT.json')
args = ['--record', pins[302]['path'], '--record-sha256', pins[302]['sha256'], '--output', unused]
check('CLI_no_audit_refused_no_output', lambda:cli_refusal(args, unused))
check('CLI_record_pin_mismatch_refused', lambda:cli_refusal(['--record',pins[302]['path'],'--record-sha256','0'*64,'--output',unused],unused))
check('CLI_existing_output_refused_without_modification', lambda:cli_refusal(['--record',pins[302]['path'],'--record-sha256',pins[302]['sha256'],'--output',str(source)]))
check('CLI_partial_audit_arguments_refused', lambda:cli_refusal(args+['--audit','SYNTHETIC_MISSING_FILE'],unused))

report = {'schema':'EPS_NEGLIGIBLE_RULE_TESTS_CX2V001','date_u':subprocess.check_output(['/bin/date','-u'],env={**os.environ,'LC_ALL':'C'},text=True).strip(),
          'status':'PASS' if all(t['passed'] for t in tests) else 'FAIL',
          'test_count':len(tests),'passed':sum(t['passed'] for t in tests),'tests':tests,
          'rule_source':source_pin,'test_source':{'path':str(Path(__file__)),'sha256':rule.digest(Path(__file__).read_bytes())},
          'inputs':inputs,'scope':'Saved-record arithmetic and in-process CLI only. Positive audit fixtures are SYNTHETIC in memory and are not real dense audits, approvals, or scientific claims. No successor record written for real CP1 points. No project-module import or dense execution.',
          'runtime':'Specified Python -I -B; six single-thread variables; nice -n10 attempted; nice unavailable (sandbox), 0514 waiver.'}
raw=(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
with Path(a.report).open('xb') as f:f.write(raw)
print(json.dumps({'status':report['status'],'passed':report['passed'],'total':report['test_count'],'report':{'path':a.report,'sha256':rule.digest(raw)},'failures':[t for t in tests if not t['passed']]}))
raise SystemExit(0 if report['status']=='PASS' else 1)

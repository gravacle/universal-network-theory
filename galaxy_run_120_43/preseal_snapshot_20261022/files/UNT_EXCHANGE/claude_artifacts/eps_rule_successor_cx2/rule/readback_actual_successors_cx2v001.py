#!/usr/bin/env python3
"""Independent three-point saved-artifact readback; does not import the rule."""
from pathlib import Path
import copy
import hashlib
import json
import math
import os
import subprocess

B = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2')
CP = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/cp1_run_c3v004b')
TABLE = {
    302: ('P302_6f4604efe6d7fe34_W0003_P02_a1/EPS_NUMERIC_6f4604efe6d7fe34.json',
          '3babf8f45719220ac161b5e784cb86e2684129e94be5715848088ae61910dc72', 46,
          '1ca790a6e6240021ef2ea09a810dff69316d35cc9d84a06ba5116a1b01dbbb3c',
          '62e05e7dfae804127260c9300376aed937009fc638b889b1edfd80e8ca693075'),
    501: ('P501_421cb796874019be_W0005_P01_a1/EPS_NUMERIC_421cb796874019be.json',
          '52cc2502b60b53ad14a55fbb94f900e0a7d06e4f256233a9decbb5c48c33ab06', 76,
          'ebf7e745a726061a68b866c194ea0b2e920b058099dff32a31adcbf35f09f795',
          '3f599be03e59efbea98c5434bf68741c140fa6c6020c4de13cd42cde3ca2c821'),
    504: ('P504_cdc5592d149fa9ef_W0005_P04_a1/EPS_NUMERIC_cdc5592d149fa9ef.json',
          '0005d1615277d4c48ab1c1541e9f7c059bb18d11fc13bb13a9da860202d4a3dd', 73,
          'e32834939956e52ea38f2f461d3e89d03b5570f7ab15ef76d31e3476e1904b1a',
          '9cfb4f6d138d3c7101cf9b88d7b2b1067ba84b648d45c1f694f43233152e2d34'),
}
inputs = []


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load(path, expected, parse=True):
    raw = path.read_bytes()
    assert sha(raw) == expected, str(path)
    ref = {'path': str(path), 'sha256': expected}
    inputs.append(ref)
    return (json.loads(raw) if parse else raw), ref, raw


def canonical(obj):
    return json.dumps(obj, sort_keys=True, allow_nan=False, separators=(',', ':'))


def finite_tree(obj):
    if type(obj) is float:
        assert math.isfinite(obj)
    elif isinstance(obj, dict):
        for value in obj.values():
            finite_tree(value)
    elif isinstance(obj, list):
        for value in obj:
            finite_tree(value)


_, authority_ref, _ = load(B/'A296_AUTHORITY_CX2V001.json', 'd1656a16e386b5bb1d0c6dd566706cd3d06ed47ec83ae1d6bf69b9d10238ea92')
_, audit_producer_ref, _ = load(B/'audit_path/dense_eps_audit_cx2v002.py', '618ba8fa9db2e7d7747c007d00f0ec64fd30083a164b01ad8ff60195e1b0d341', False)
_, rule_ref, _ = load(B/'rule/eps_negligible_rule_cx2v003.py', '669f0640b4a9e2a005e91245c27223499dc96a35189c6b4852a11a1e99190e3b', False)
results = []
verdict = 'NUMERICAL_RULE_PASSED_NEGLIGIBLE_SHELLS_NOTED_REVIEW_REQUIRED'

for row, (relative, original_hash, low, successor_hash, audit_hash) in TABLE.items():
    original_path = CP/relative
    original, original_ref, original_bytes = load(original_path, original_hash)
    successor, successor_ref, successor_bytes = load(B/f'EPS_ROW{row}_CX2V001.json', successor_hash)
    audit, audit_ref, _ = load(B/f'audit_path/DENSE_ROW{row}_S{low}_CX2V001.json', audit_hash)
    for obj in (original, successor, audit):
        finite_tree(obj)
    assert original['status'] == 'TESTED' and original['settings'] == 'registered'
    assert original['full_registered_search_executed'] is True and original['coverage_complete'] is True
    assert original['required_coverage_inverse_kpc'] == [4,182]
    assert len(original['shells']) == len(successor['shells']) == 178
    assert [s['range_inverse_kpc'] for s in original['shells']] == [[k,k+1] for k in range(4,182)]
    failed = []
    for i, sh in enumerate(original['shells']):
        assert type(sh['refinements']) is int and type(sh['certified']) is bool
        level0, level1 = sh['levels']['0']['eps'], sh['levels']['1']['eps']
        assert type(level0) in (int,float) and type(level1) in (int,float)
        if level1 <= 1.1*level0:
            assert sh['refinements'] == 0 and sh['certified'] is True
            assert sh['eps_base'] == level0 and sh['eps_refined'] == level1
        else:
            level2 = sh['levels']['2']['eps']
            passed = level2 <= 1.1*level1
            assert sh['refinements'] == (1 if passed else 2) and sh['certified'] is passed
            assert sh['eps_base'] == level1 and sh['eps_refined'] == level2
        if not sh['certified']:
            failed.append(i)
    assert failed == [low-4]
    old_shell = original['shells'][low-4]
    new_shell = successor['shells'][low-4]
    measured = old_shell['eps']
    substituted = 10*measured
    fraction_limit = 0.1*original['eps_max']
    difference = abs(old_shell['levels']['2']['eps']-old_shell['levels']['1']['eps'])
    production = old_shell['envelope']['estimate']
    dense = audit['dense_search']['estimate']
    ratio = dense/production
    assert substituted <= fraction_limit and difference <= 1e-6 and ratio <= 1.05
    assert audit['source_record'] == original_ref and audit['point_sha256'] == original['point_sha256']
    assert audit['original_producer'] == original['producer'] and audit['audit_producer'] == audit_producer_ref
    assert audit['schema'] == 'UNT_EPS_NEGLIGIBLE_DENSE_AUDIT_CX2V001'
    assert audit['status'] == 'TESTED' and audit['settings'] == 'registered'
    assert audit['range_inverse_kpc'] == [low,low+1]
    assert audit['production'] == production and audit['dense'] == dense and audit['dense_over_production'] == ratio
    dense_search = audit['dense_search']
    for field, val in (('torus_m',20),('direction_count',400),('starts',16),('n_grid',16000000)):
        assert type(dense_search[field]) is int and dense_search[field] == val
    assert dense_search['radial_fractions'] == [0,.25,.5,.75,1]
    assert audit['checks']['discrete_saved_record_exact'] is True
    assert audit['checks']['envelope_actual_bitwise'] is True
    assert audit['checks']['grid_background_custody_rederived'] is True
    assert audit['production_admissible'] is False and audit['rigorous_supremum'] is False
    evidence = {'M':10, 'f':0.1, 'absolute_floor':1e-6,
                'absolute_level2_minus_level1':difference, 'dense_over_production':ratio,
                'dense_audit':audit_ref}
    expected_shell = copy.deepcopy(old_shell)
    expected_shell.update(eps=substituted, eps_measured_before_negligible_substitution=measured,
                          accepted_negligible=True, acceptance='ACCEPTED_NEGLIGIBLE',
                          negligible_acceptance_evidence=evidence)
    assert canonical(new_shell) == canonical(expected_shell)
    unchanged_count = sum(canonical(before)==canonical(after) for i,(before,after) in enumerate(zip(original['shells'],successor['shells'])) if i != low-4)
    assert unchanged_count == 177
    additions = {'successor_rule_verdict':'ACCEPTED_NEGLIGIBLE', 'accepted_shells':[[float(low),float(low+1)]],
                 'approved_signer_review_required':True,
                 'predecessor':{'record':original_ref,'producer':original['producer'],'verdict':'EPS_UNCERTIFIED','registered_discrete_verdict':'EPS_UNCERTIFIED'},
                 'rule_authority':dict(authority_ref,heading='A296'),
                 'successor_date_u':successor['successor_date_u'],
                 'successor_limitations':'Saved numerical-rule re-evaluation only. No new supremum guarantee or scientific admission. Approved-signer review and root adoption required.'}
    assert isinstance(additions['successor_date_u'],str) and ' UTC ' in additions['successor_date_u']
    assert set(successor) == set(original)|set(additions)
    expected = copy.deepcopy(original)
    expected.update(additions)
    expected['producer'] = rule_ref
    expected['verdict'] = verdict
    expected['shells'][low-4] = expected_shell
    assert canonical(successor) == canonical(expected)
    assert successor_bytes == (json.dumps(expected,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
    assert successor['eps_max'] == original['eps_max'] == max(s['eps'] for s in successor['shells'])
    assert canonical(successor['eps_max_shell']) == canonical(original['eps_max_shell'])
    assert successor['registered_discrete_verdict'] == 'EPS_UNCERTIFIED'
    assert new_shell['certified'] is False and new_shell['refinements'] == 2
    assert successor['production_admissible'] is False and successor['rigorous_supremum'] is False
    assert original_path.read_bytes() == original_bytes
    results.append({'row':row,'status':'PASS','range_inverse_kpc':[low,low+1],
                    'source_record':original_ref,'successor_record':successor_ref,'audit_record':audit_ref,
                    'all_allowed_differences_only':True,'whole_successor_bytes_reconstructed_independently':True,
                    'unaffected_shells_canonical_json_identical':unchanged_count,
                    'original_bytes_stable':True,'eps_max_unchanged':original['eps_max'],
                    'eps_max_shell_unchanged':original['eps_max_shell'],
                    'original_discrete_failure_preserved':True,'admission_not_granted':True,
                    'thresholds':{'measured_epsilon':measured,'substituted_epsilon':substituted,
                                  'fraction_limit':fraction_limit,'fraction_utilization':substituted/fraction_limit,
                                  'absolute_level2_minus_level1':difference,'absolute_limit':1e-6,
                                  'audit_production':production,'audit_dense':dense,'audit_ratio':ratio,'audit_ratio_limit':1.05},
                    'registered_audit_checks_recorded':audit['checks'],
                    'note':'The audit artifact records a numerical search, not a rigorous supremum; this readback did not rerun that search.'})

report = {'schema':'ACTUAL_EPS_SUCCESSOR_READBACK_CX2V001',
          'date_u':subprocess.check_output(['/bin/date','-u'],env={**os.environ,'LC_ALL':'C'},text=True).strip(),
          'status':'TESTED_PASS','rows':results,'input_pins':inputs,
          'readback_source':{'path':str(Path(__file__)),'sha256':sha(Path(__file__).read_bytes())},
          'independence':'Does not import/call the rule or audit producer. Independently calculates thresholds and reconstructs every output byte from originals and pinned evidence.',
          'limits':'Saved-artifact readback only. No dense-search rerun, scientific launch, signer admission or root adoption. No forward/run/state/NGC input opened.',
          'runtime':'Specified isolated Python; six single-thread environment variables; nice unavailable (sandbox),0514 waiver.'}
p=B/'rule/READBACK_ACTUAL_ROWS302_501_504_CX2V001.json'
raw=(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
with p.open('xb') as f:
    f.write(raw)
print(json.dumps({'status':report['status'],'report':{'path':str(p),'sha256':sha(raw)},
                  'readback_source':report['readback_source'],'rows':[{'row':r['row'],'thresholds':r['thresholds']} for r in results]},indent=2))

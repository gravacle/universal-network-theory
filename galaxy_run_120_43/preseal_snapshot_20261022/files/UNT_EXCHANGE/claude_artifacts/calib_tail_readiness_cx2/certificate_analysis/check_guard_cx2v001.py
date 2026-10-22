"""Synthetic verifier refutation tests only; creates immutable small fixtures."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('guard', HERE / 'certificate_guard_cx2v001.py')
G = importlib.util.module_from_spec(spec)
spec.loader.exec_module(G)
OUT = HERE / 'synthetic_checks_v001'
OUT.mkdir(exist_ok=False)
serial = 0
def pin(obj):
    global serial
    serial += 1
    p = OUT / ('synthetic_%03d.json' % serial)
    raw = G.canonical(obj) + b'\n'
    with p.open('xb') as f:
        f.write(raw)
    return {'path': str(p), 'sha256': hashlib.sha256(raw).hexdigest()}
producer = {'path': str(Path(__file__)), 'sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
identity = {'driver_sha256': 'a' * 64, 'physical': {'common_scale_s': 1.0},
            'coefficients': {'synthetic': True}, 'numerics': {'uv_tail': {
                'enabled': True, 'source_rule': 'continuum_v001',
                'outer': {'shape': 'cylinder', 'K_big_inverse_kpc': 64.0}, 'gas': {'M_s': 64}}}}
custody = {k: 'b' * 64 for k in G.CUSTODY_KEYS}
state = {'state_sha256': 'c' * 64, 'source_sha256': 'd' * 64,
         'stage_kind': 'SYNTHETIC_NOT_A_SCIENTIFIC_STATE', 'nonnegative_masses': True}
common = {'schema': G.PROOF_SCHEMA, 'status': 'TESTED', 'verdict': 'PASS',
          'point_sha256': G.digest(identity), 'custody_sha256': G.digest(custody), 'producer': producer,
          'fixture': 'SYNTHETIC_NOT_A_CERTIFICATE'}
eps = dict(common, gate='EPS', envelope_rule=G.ENVELOPE,
           shells=[{'range_inverse_kpc': [4, 91], 'eps': 0.01, 'eps_envelope': 0.01, 'refinement_failures': 0}])
gq = dict(common, gate='GQ', method='GEOMETRY_UNIFORM_COLUMN_BOUND',
          all_columns_included=True, all_production_kperp_nodes=True, nonnegative_masses_required=True,
          M_s=64, M_s_doubled=128, K_big_inverse_kpc=64.0,
          max_column_difference_over_analytic_Pi0=1e-14, max_zero_mode_relative_error=1e-15)
ep, gp = pin(eps), pin(gq)
lo = dict(common, gate='LO', state=state, row_contract_sha256=custody['row_contract_sha256'],
          i1t_verdict='PASS', GQ_uniform_proof_sha256=gp['sha256'],
          shells=[{'range_inverse_kpc': [4, 91], 'max_over_tau': 0.001}], summed_max_over_tau=0.001)
doc = {'schema': G.SCHEMA, 'identity': identity, 'custody': custody,
       'domain': {'K_inverse_kpc': 4.0, 'K_big_inverse_kpc': 64.0},
       'prelaunch': {'EPS': ep, 'GQ': gp},
       'acceptance_rule': 'ALL_CONSUMED_STATES_LO_AND_GQ_FAIL_CLOSED',
       'states': [{'state': state, 'LO': pin(lo)}]}
checks = []
def run(name, d, expect, **kw):
    result = G.verify_bundle(pin(d), kw.pop('identity', identity),
                            expected_custody=kw.pop('custody', custody),
                            approved_producer_sha256=kw.pop('approved', [producer['sha256']]), **kw)
    checks.append({'name': name, 'expected_ok': expect, 'actual_ok': result['ok'], 'blockers': result['blockers']})
    assert result['ok'] is expect, name
run('synthetic_prelaunch_valid', doc, True)
run('synthetic_acceptance_valid', doc, True, phase='acceptance', required_states=[state])
run('missing_trusted_custody', doc, False, custody=None)
run('unapproved_producer', doc, False, approved=[])
changed = copy.deepcopy(identity); changed['physical']['common_scale_s'] = 2.0
run('point_change', doc, False, identity=changed)
run('empty_state_inventory', doc, False, phase='acceptance')
changed = copy.deepcopy(state); changed['source_sha256'] = 'e' * 64
run('source_change', doc, False, phase='acceptance', required_states=[changed])
run('duplicate_required_state', doc, False, phase='acceptance', required_states=[state, state])
def bad_proof(name, gate, obj, change):
    mutated = copy.deepcopy(obj); change(mutated)
    d = copy.deepcopy(doc)
    if gate == 'LO':
        d['states'][0]['LO'] = pin(mutated)
        run(name, d, False, phase='acceptance', required_states=[state])
    else:
        d['prelaunch'][gate] = pin(mutated)
        run(name, d, False)
bad_proof('eps_coverage_shortfall', 'EPS', eps, lambda x: x['shells'][0].update(range_inverse_kpc=[4, 90]))
bad_proof('eps_refinement_failure', 'EPS', eps, lambda x: x['shells'][0].update(refinement_failures=2))
bad_proof('eps_false_envelope', 'EPS', eps, lambda x: x['shells'][0].update(eps=0.001))
bad_proof('eps_missing_envelope', 'EPS', eps, lambda x: x.update(envelope_rule=None))
bad_proof('gq_mass_weighted_anchor', 'GQ', gq, lambda x: x.update(method='SAVED_STATE_WEIGHTED_BOUND'))
bad_proof('gq_fails', 'GQ', gq, lambda x: x.update(max_column_difference_over_analytic_Pi0=1e-9))
bad_proof('gq_missing_columns', 'GQ', gq, lambda x: x.update(all_columns_included=False))
bad_proof('gq_wrong_order', 'GQ', gq, lambda x: x.update(M_s=8))
bad_proof('lo_threshold', 'LO', lo, lambda x: x['shells'][0].update(max_over_tau=0.006))
bad_proof('lo_fabricated_sum', 'LO', lo, lambda x: x.update(summed_max_over_tau=0.0))
bad_proof('lo_wrong_roster', 'LO', lo, lambda x: x.update(state=changed))
bad_proof('lo_missing_i1t', 'LO', lo, lambda x: x.update(i1t_verdict='NOT_RUN'))
d = copy.deepcopy(doc); d['prelaunch']['EPS']['sha256'] = '0' * 64
run('tampered_file_hash', d, False)
d = copy.deepcopy(doc); d['prelaunch']['EPS'] = ep | {'path': '/Volumes/External1/CLAUDE2/runs_ext/UVT_BLINDED/result.json'}
run('forbidden_path_refused', d, False)
summary = {'status': 'TESTED', 'kind': 'SYNTHETIC_GUARD_TESTS_NOT_SCIENTIFIC_CERTIFICATION',
           'checks': checks, 'count': len(checks), 'all_passed': True,
           'waiver': 'nice unavailable (sandbox); 0514 waiver',
           'env': {k: os.environ.get(k) for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS')},
           'maxrss_native': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
with (OUT / 'RESULT.json').open('xb') as f:
    f.write(G.canonical(summary) + b'\n')
print(json.dumps({'count': len(checks), 'all_passed': True, 'maxrss_native': summary['maxrss_native']}))

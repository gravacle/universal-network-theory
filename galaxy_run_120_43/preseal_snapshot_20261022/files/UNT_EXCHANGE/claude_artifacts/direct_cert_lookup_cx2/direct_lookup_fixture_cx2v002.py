"""0831 narrow in-process repin tests. Synthetic certificates only; never launches."""
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import sys
import types

ART = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
HERE = Path(__file__).resolve().parent
ROOT = HERE / 'DIRECT_LOOKUP_TESTS_CX2V002'
ROOT.mkdir()
READS = {}
def audit(event, args):
    if event.startswith(('subprocess.', 'socket.')) or event in (
            'os.system', 'os.fork', 'os.posix_spawn', 'os.rename', 'os.remove', 'os.rmdir'):
        raise RuntimeError('TEST_FENCE: ' + event)
    if event == 'open' and isinstance(args[0], (str, bytes)):
        p = Path(os.fsdecode(args[0]))
        low = str(p).lower()
        if any(x in low for x in ('ngc3198', '/runs_ext/', '/runs/', '/.codex/',
                                  'v007_postseal_records', 'kmax_a2f10_c5h_run_v001')):
            raise RuntimeError('TEST_PROTECTED_PATH: ' + str(p))
        flags = args[2]
        writing = flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC)
        if writing:
            if not p.is_relative_to(ROOT) or p.exists() or not flags & os.O_EXCL:
                raise RuntimeError('TEST_EXCLUSIVE_OUTPUT_REQUIRED: ' + str(p))
        elif p.is_relative_to(ART):
            if not p.is_relative_to(ROOT) and p.suffix != '.py' and p != ART/'c1_h1_c2/C1_H1_C2V001.json':
                raise RuntimeError('TEST_SOURCE_OR_C1_ONLY: ' + str(p))
            READS[str(p)] = READS.get(str(p), 0) + 1
sys.addaudithook(audit)

def rawpin(p):
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
def write(name, obj):
    p = ROOT / name
    with p.open('x') as f:
        json.dump(obj, f, indent=1, sort_keys=True, allow_nan=False)
        f.write('\n')
    return rawpin(p)
def load(p, name):
    m = types.ModuleType(name)
    m.__file__ = str(p)
    sys.modules[name] = m
    exec(compile(p.read_bytes(), str(p), 'exec'), m.__dict__)
    return m
N = load(HERE/'cp1_points_assembler_cx2v002.py', 'list_repin_new')
O = load(ART/'h3_campaign_path_c2/cp1_points_assembler_c2v001.py', 'list_repin_old')
A, C = N.A, N.C
G = A.real_guard()
RESULTS = []
def check(name, condition, detail=None):
    RESULTS.append({'name': name, 'passed': bool(condition), 'detail': detail})
def gate(c1, gen, module=A):
    return module.c1_policy_gate(c1, gen)

# The C1 metadata is the real frozen file; no registry, point, rho, EPS or run input
# is read. Only the registry and policy-review references are replaced in fixtures.
c1path = ART/'c1_h1_c2/C1_H1_C2V001.json'
c1pin = rawpin(c1path)
assert c1pin['sha256'] == '4015932226dcfbf9783b96de1daa512ef5c7a397ac4ca093d701ead362ed92c1'
frozen = json.loads(c1path.read_bytes())
six = frozen['tail_readiness']['approved_certificate_producers']
assert len(six) == 6
assert six == [C.canonical_pin(n) for n in C.CANONICAL_APPROVED_PRODUCERS]
gen = write('SYNTHETIC_GENESIS.json', {'points': {}, 'eps_source_pins_digest': C.digest(
    {'dependencies': {'synthetic': True}, 'producer': six[0]})})
def policy_fixture(tag, producers, **rv_changes):
    tr = copy.deepcopy(frozen['tail_readiness'])
    tr['certificate_registry'] = gen
    tr['approved_certificate_producers'] = copy.deepcopy(producers)
    rv = {'schema': A.POLICY_SCHEMA, 'status': 'TESTED', 'ok': True,
          'driver_sha256': C.DRIVER_SHA, 'custody_deriver': tr['custody_deriver'],
          'state_enumerator': tr['state_enumerator'], 'approved_certificate_producers': producers,
          'guard_sha256': A.wrapper_l30_guard_pin()['sha256'], 'driver_slot_rule': A.SLOT_RULE,
          'post_state_handoff': 'TAIL_CERTIFICATE_ACCEPTANCE_CX2V001',
          'synthetic_fixture': True}
    rv.update(rv_changes)
    tr['certificate_policy_review'] = write(tag+'_REVIEW.json', rv)
    return write(tag+'_C1.json', {'tail_readiness': tr, 'synthetic_fixture': True})
c1six = policy_fixture('SIX', six)
_, errors = gate(c1six, gen)
check('new_six_producer_C1_policy_accepts', errors == [], errors)
_, errors = gate(c1six, gen, O.A)
check('old_three_canonical_path_refuses_six', len(errors) == 3 and
      all(x.startswith('C1_APPROVED_PRODUCER_NOT_CANONICAL:') for x in errors), errors)
c1three = policy_fixture('THREE', six[:3])
check('old_three_producer_compatibility', gate(c1three, gen, O.A)[1] == [])
check('new_three_producer_compatibility', gate(c1three, gen)[1] == [])
seventh = dict(six[0], sha256='0'*64)
check('seventh_producer_refused', bool(gate(policy_fixture('SEVEN', six+[seventh]), gen)[1]))
check('nonboolean_policy_ok_refused', bool(gate(policy_fixture('BOOL', six, ok=1), gen)[1]))
check('reordered_review_refused', bool(gate(policy_fixture(
    'ORDER', six, approved_certificate_producers=list(reversed(six))), gen)[1]))
other_gen = write('OTHER_SYNTHETIC_GENESIS.json', {'points': {}})
check('different_genesis_refused', bool(gate(c1six, other_gen)[1]))

# Actual list/common -> c3v005 -> unchanged wrapper block -> b1 guard, on three
# synthetic points. Custody is an explicit synthetic fixture function; no actual
# geometry, registered numeric search or physical producer is executed.
custody = {k: hashlib.sha256(k.encode()).hexdigest() for k in G.CUSTODY_KEYS}
points, bundles = [], []
for i in range(3):
    block = {'uv_tail': {'enabled': True, 'source_rule': 'continuum_v001',
              'outer': {'shape': 'cylinder', 'K_big_inverse_kpc': 128.0},
              'gas': {'M_s': 128, 'interp': 'lagrange3_s_gl4'},
              'lambda_scale': 1.0, 'lapse_only': True,
              'eps_certificate': 'PENDING_UV_TAIL_CERTIFICATE',
              'lo_certificate': 'PENDING_UV_TAIL_CERTIFICATE'},
             'truncation': {'shape': 'cube'},
             'composite_grid_spec': {'breaks_inverse_kpc': [0, 4]},
             'route_a': {'column_workers': 8},
             'brackets': {'rule': {'fs_absolute_overrides': {str(j): A.HULL for j in range(72)}}}}
    spec = {'galaxy': 'DDO154', 'admit': {}, 'physical': {'distance_Mpc': 4.04, 'common_scale_s': 1.0+i/4, 'gamma': 6.0, 'Eref_J': 3.0, 'entropy_K_factor': 1.0, 'ell_F_m': 2.0, 'inclination_deg': 66.0},
            'coefficients': {}, 'numerics': block, 'label': 'synthetic fixture'}
    ident = C.point_identity(spec)
    key = C.digest(ident)
    theta = {'common_scale_s': 1.0+i/4, 'gamma_over_Eref': 2.0, 'Eref_base_J': 3.0, 'entropy_K_factor': 1.0, 'ell_F_m': 2.0, 'distance_Mpc': 4.04}
    call_key = C.digest({'schema': 'DDO154_CALIBRATION_THETA_KEY_C2V001', 'theta': {k:float(v) for k,v in theta.items()}})
    spec['label'] = 'DDO154 cx2v006 theta %s; point %s' % (call_key[:16], key[:16])
    spin = write('SPEC_%d.json'%i, spec)
    eps = write('EPS_NUMERIC_%d.json'%i, {'synthetic_fixture': True,
        'dependencies': {'synthetic': True}, 'producer': six[0]})
    rho = write('RHO_NUMERIC_%d.json'%i, {'schema': 'UNT_POINT_RHO_NUMERICAL_CX2V001',
        'gate': 'RHO_G', 'identity': ident, 'point_sha256': key, 'custody': custody,
        'settings': 'registered', 'full_registered_search_executed': True,
        'coverage_complete': True, 'synthetic_fixture': True})
    common = {'schema': G.PROOF_SCHEMA, 'status': 'TESTED', 'verdict': 'PASS',
              'point_sha256': key, 'custody_sha256': C.digest(custody), 'synthetic_fixture': True}
    ep = write('EPS_PROOF_%d.json'%i, dict(common, gate='EPS', producer=six[0],
        driver_certificate=eps, envelope_rule=G.ENVELOPE,
        shells=[{'range_inverse_kpc': [4, 182], 'refinement_failures': 0, 'eps': 1, 'eps_envelope': 1}]))
    gp = write('GQ_PROOF_%d.json'%i, dict(common, gate='GQ', producer=six[1],
        method='GEOMETRY_UNIFORM_COLUMN_BOUND', all_columns_included=True,
        all_production_kperp_nodes=True, nonnegative_masses_required=True,
        M_s=128, M_s_doubled=256, K_big_inverse_kpc=128.0,
        max_column_difference_over_analytic_Pi0=1e-14, max_zero_mode_relative_error=0.0))
    lp = write('LO_RHO_SLOT_PROOF_%d.json'%i, dict(common, gate='LO_RHO_SLOT',
        producer=six[2], driver_certificate=rho))
    bp = write('BUNDLE_%d.json'%i, {'schema': G.SCHEMA, 'identity': ident, 'custody': custody,
        'domain': {'K_inverse_kpc': 4.0, 'K_big_inverse_kpc': 128.0},
        'driver_certificate_bindings': {'eps_certificate': eps, 'lo_certificate': rho},
        'prelaunch': {'EPS': ep, 'GQ': gp, 'LO_RHO_SLOT': lp},
        'acceptance_rule': 'ALL_CONSUMED_STATES_LO_AND_GQ_FAIL_CLOSED', 'synthetic_fixture': True})
    bundles.append(bp['path'])
    points.append({'row': 300+i, 'label': 'SYNTHETIC_W3_P%02d'%i, 'key': key,
                   'theta': theta, 'call_key': call_key, 'spec': spin, 'pending_spec_sha256': spin['sha256']})
listpin = write('POINTS_LIST.json', {'schema': N.P.LIST_SCHEMA, 'wave': 3, 'points': points})
doc, rows = N.P.load_points_list(C, listpin)
records = N.assemble_records(listpin, doc, rows, bundles, approved=six,
    out_root=str(ROOT), genesis_ref=gen)
rep = N.verify_list(records, rows, c1_ref=c1six, genesis_ref=gen,
                    custody_loader=lambda pin: lambda spec: custody, guard=G)
check('new_list_verify_three_points_six_producer_C1', rep['ok'] is True and rep['n_ok'] == 3, rep)
oldrep = O.verify_list(records, rows, c1_ref=c1six, genesis_ref=gen,
                      custody_loader=lambda pin: lambda spec: custody, guard=G)
check('old_list_verify_three_points_refuses_six', oldrep['ok'] is False and oldrep['n_ok'] == 0 and
      len(oldrep['c1_policy_gate']['blockers']) == 3, oldrep)
rec = json.loads(Path(records['path']).read_bytes())
bad = copy.deepcopy(rec)
bad['records'][0]['record']['lo_certificate'] = bad['records'][1]['record']['lo_certificate']
badref = write('BAD_RECORD_SLOT.json', bad)
br = N.verify_list(badref, rows, c1_ref=c1six, genesis_ref=gen,
                  custody_loader=lambda pin: lambda spec: custody, guard=G)
check('wrong_point_slot_refused', br['ok'] is False and br['n_ok'] == 2, br['points'][0])


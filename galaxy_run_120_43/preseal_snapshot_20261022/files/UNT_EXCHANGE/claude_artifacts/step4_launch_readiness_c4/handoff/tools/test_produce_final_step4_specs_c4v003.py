# Claude4 v003 BUILD: tests of produce_final_step4_specs_c4v003.py (Claude3 0105 PR-SF1, PR-SF2, PR-SF3, PR-SF5).
# FIX stage (SF-R1): this file = the BUILD test file ff38c1812a55551c4dc08b7a74cc299df96af2028a5ae2321cd3b638d7a14a55 plus one
# section, "SF-R1" (write failures AFTER a file exists, injected at the OS layer: the REFUTE stage's runs W00-W17, ported),
# and one AST check (SFR1_STATIC_*). Every BUILD case is unchanged. Run against the BUILD producer 28921808 the SF-R1 cases
# fail (the defect, confirmed from bytes); run against the fix-stage producer they must all pass.
# Usage: python3 -I -B test_produce_final_step4_specs_c4v003.py <TAG> "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
#
# Phase A (fence REVIEW = the folder above tools/: v003_work in the BUILD, v003_work/fix_sfr1 in the FIX stage): the producer
# of record (tools/produce_final_step4_specs_c4v003.py) is loaded FIRST,
#   which installs its fence (fence_c4v003) before anything else reads a project file. Its World computes the 27 point
#   identities; synthetic fixtures are written to v003_work/tests_<TAG>/fixtures/ (every synthetic file and folder says
#   SYNTHETIC); byte copies of the producer and fence go to tests_<TAG>/run/tools/ (the T0 layout: final_specs_v00x/tools).
# Phase B (fence REVIEW = tests_<TAG>/run): the byte copy is loaded and every case runs through it; writes stay in run/.
# No case can produce a FINAL-labelled file from synthetic inputs: final mode is only ever refused here, and the in-memory
# FINAL construction (S4) is compared without being written. Nothing is launched; no process is started.
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import math
import os
import sys
import time

TOOLS = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(TOOLS)
PROD_NAME = 'produce_final_step4_specs_c4v003.py'
FENCE_NAME = 'fence_c4v003.py'


def _load(path, name):
    with open(path, 'rb') as f:
        raw = f.read()
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp)
    sys.modules[name] = m
    exec(compile(raw, path, 'exec'), m.__dict__)
    return m, hashlib.sha256(raw).hexdigest()


P1, PROD_SHA = _load(os.path.join(TOOLS, PROD_NAME), 'c4v003_producer_phaseA')     # installs fence_c4v003 first
FENCE_A = P1.FENCE
TAG, UTC = sys.argv[1], sys.argv[2]
T0 = time.time()
BASE = os.path.join(V3, 'tests_' + TAG)
FIX = os.path.join(BASE, 'fixtures')
RUN = os.path.join(BASE, 'run')
H = lambda b: hashlib.sha256(b).hexdigest()
J = P1.json_bytes


def xwrite(path, data):
    if not os.path.isdir(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    raw = data if isinstance(data, bytes) else J(data)
    with open(path, 'xb') as f:
        f.write(raw)
    return {'path': path, 'sha256': H(raw)}


def rjson(path):
    with open(path, 'rb') as f:
        return json.loads(f.read())


R9 = P1.CONFIG_R9
C4T = P1.C4T_FILLED
CB = {'path': P1.CASE_BLOCK[0], 'sha256': P1.CASE_BLOCK[1]}
R5PIN = {'path': P1.R5[0], 'sha256': P1.R5[1]}
GEOPIN = {'path': P1.V009GEO[0], 'sha256': P1.V009GEO[1]}
AUTH = dict(P1.AUTHORITY)
DRYRUN = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3/dry_run_20261019T010953Z/passB/scratch_ctrl'
POLICY_R7 = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r7/adoption_policy_cx2v006r7.py',
             '7c726fa2ad3f3e0fbcfcf36353901f970cde1eff3f76321327e5a8a5fbc29b1d')
V002_LOOKALIKE = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/v002_work/handoff/producer_test_v002/sandbox/SYNTHETIC_C1_LOOKALIKE.json',
                  '1757f2ce6f8c8b829f6bb106faab1ed21aaf7205f32af2f4e0feb43be10b15fa')

# ================================================================================================ Phase A: fixtures
os.mkdir(BASE)
os.mkdir(FIX)
os.mkdir(RUN)
os.mkdir(os.path.join(RUN, 'tools'))
for nm in (PROD_NAME, FENCE_NAME):
    with open(os.path.join(TOOLS, nm), 'rb') as f:
        raw = f.read()
    xwrite(os.path.join(RUN, 'tools', nm), raw)
    with open(os.path.join(RUN, 'tools', nm), 'rb') as f:
        assert f.read() == raw
r9 = rjson(R9[0])
assert H(open(R9[0], 'rb').read()) == R9[1]
c4t = rjson(C4T[0])
A70 = {k: copy.deepcopy(c4t['numerics']['uv_tail'][k]) for k in ('eps_certificate', 'lo_certificate')}

# point identities under the C4T block (the C1 block of an ADOPT_TAIL), computed by the producer's own construction
cfg_c4t = copy.deepcopy(r9)
cfg_c4t['numerics']['block'] = copy.deepcopy(c4t['numerics'])
w_ids = P1.World(cfg_c4t, {'path': 'in-memory', 'sha256': None}, P1.NOTE_DRY)
rows_ids = w_ids.build_all()
IDENT = {}
for r in rows_ids:
    s = json.loads(r['raw'])
    IDENT[r['point_key']] = P1.point_identity(s)
KEYS = sorted(IDENT)
ANCHOR = P1.ANCHOR_POINT_KEY
assert ANCHOR in IDENT and len(KEYS) == 27, (len(KEYS), ANCHOR in IDENT)
NONANCHOR = [k for k in KEYS if k != ANCHOR]
FIRST = NONANCHOR[0]

COMMON = os.path.join(FIX, 'SYNTHETIC_COMMON')
ADD = xwrite(os.path.join(COMMON, 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_S_WORLD_FROZEN.md'),
             b'SYNTHETIC S-WORLD FROZEN ADDENDUM STAND-IN; not the V005 addendum; no ruling.\n')
RESULT = xwrite(os.path.join(COMMON, 'SYNTHETIC_C4T_RESULT_NEVER_READ.json'),
                {'synthetic': True, 'note': 'stand-in pinned as numerics.adopted_result; the producer never reads it'})
PROD_EPS = xwrite(os.path.join(COMMON, 'SYNTHETIC_EPS_PRODUCER.py'), b'# SYNTHETIC S-world certificate producer stand-in; never executed\nSYNTHETIC = True\n')
PROD_LO = xwrite(os.path.join(COMMON, 'SYNTHETIC_LO_PRODUCER.py'), b'# SYNTHETIC S-world LO producer stand-in; never executed\nSYNTHETIC = True\n')
PRODUCERS = [PROD_EPS, PROD_LO]
REVIEW_DOC = {'schema': P1.POLICY_REVIEW_SCHEMA, 'synthetic': True, 'status': 'TESTED', 'ok': True, 'driver_sha256': P1.R5[1],
              'custody_deriver': r9['tail_readiness']['custody_deriver'], 'state_enumerator': r9['tail_readiness']['state_enumerator'],
              'approved_certificate_producers': PRODUCERS, 'guard_sha256': P1.CERT_GUARD_SHA,
              'driver_slot_rule': 'POINT_EPS_AND_REVIEWED_PRELAUNCH_LO_ENVELOPE', 'post_state_handoff': 'TAIL_CERTIFICATE_ACCEPTANCE_CX2V001'}
REVIEW = xwrite(os.path.join(COMMON, 'SYNTHETIC_CERTIFICATE_POLICY_REVIEW.json'), REVIEW_DOC)


def make_point(d, key, eps=None, lo=None, bundle_mut=None, eps_mut=None, lo_mut=None):
    """Write one point's slot certs (unless given), proofs and bundle under folder d; return the registry record."""
    k16 = key[:16]
    if eps is None:
        eps = A70['eps_certificate'] if key == ANCHOR else xwrite(os.path.join(d, 'SYNTHETIC_EPS_CERT_%s.json' % k16),
                                                                  {'schema': 'SYNTHETIC_S_WORLD_SLOT_CERT', 'synthetic': True, 'point': key, 'gate': 'EPS'})
    if lo is None:
        lo = A70['lo_certificate'] if key == ANCHOR else xwrite(os.path.join(d, 'SYNTHETIC_LO_CERT_%s.json' % k16),
                                                                {'schema': 'SYNTHETIC_S_WORLD_SLOT_CERT', 'synthetic': True, 'point': key, 'gate': 'LO'})
    pe = {'schema': P1.PROOF_SCHEMA, 'synthetic': True, 'gate': 'EPS', 'status': 'TESTED', 'verdict': 'PASS', 'point_sha256': key,
          'custody_sha256': '1' * 64, 'driver_certificate': eps, 'producer': PROD_EPS}
    pl = {'schema': P1.PROOF_SCHEMA, 'synthetic': True, 'gate': 'LO_ENVELOPE', 'status': 'TESTED', 'verdict': 'PASS', 'point_sha256': key,
          'custody_sha256': '1' * 64, 'driver_certificate': lo, 'producer': PROD_LO, 'covers_all_consumed_states': True}
    if eps_mut:
        eps_mut(pe)
    if lo_mut:
        lo_mut(pl)
    pep = xwrite(os.path.join(d, 'SYNTHETIC_EPS_PROOF_%s.json' % k16), pe)
    plp = xwrite(os.path.join(d, 'SYNTHETIC_LO_PROOF_%s.json' % k16), pl)
    b = {'schema': P1.BUNDLE_SCHEMA, 'synthetic': True, 'identity': IDENT[key], 'custody': {'synthetic': True},
         'driver_certificate_bindings': {'eps_certificate': eps, 'lo_certificate': lo}, 'prelaunch': {'EPS': pep, 'LO_ENVELOPE': plp}}
    if bundle_mut:
        bundle_mut(b)
    bp = xwrite(os.path.join(d, 'SYNTHETIC_BUNDLE_%s.json' % k16), b)
    return {'identity': IDENT[key], 'eps_certificate': eps, 'lo_certificate': lo, 'bundle': bp}


CHAIN = os.path.join(FIX, 'SYNTHETIC_CHAIN')
BASE_POINTS = {k: make_point(CHAIN, k) for k in KEYS}
REG_DOC = {'schema': 'SYNTHETIC_S_WORLD_CERTIFICATE_REGISTRY', 'synthetic': True, 'points': BASE_POINTS}
REG = xwrite(os.path.join(CHAIN, 'SYNTHETIC_REGISTRY_S_WORLD.json'), REG_DOC)
# the v002 W3 world: A70 slots on every point, no bundle (slot-fill path only; provisional semantics)
W3_REG = xwrite(os.path.join(FIX, 'SYNTHETIC_W3', 'SYNTHETIC_REGISTRY_A70_ALL_27_POINTS.json'),
                {'schema': 'SYNTHETIC_LOOKALIKE_REGISTRY_NOT_A_CERTIFICATE_REGISTRY', 'points': {
                    k: {'identity': IDENT[k], **copy.deepcopy(A70), 'bundle': {'path': 'SYNTHETIC_NO_BUNDLE', 'sha256': '0' * 64}} for k in KEYS}})
# W3 must use the r9-block identities (PENDING slots): they equal the C4T ones because identities exclude the slots
SCHEMA_REPORT = 'UNT_KMAX_TAIL_COMPARISON_C2V007_SYNTHETIC_S_WORLD'
WORLDS = {}


def make_world(name, prereg=None, compare=None, verdict=None, seal=None, policy=None, registry=None, c1=None, c1_raw=None,
               pair_form=False):
    d = os.path.join(FIX, 'SYNTHETIC_WORLD_' + name)
    pre = {'schema': 'SYNTHETIC_S_WORLD_PREREG', 'synthetic': True, 'binding_inputs': {'case_block': dict(CB)}}
    if prereg:
        prereg(pre)
    P = xwrite(os.path.join(d, 'SYNTHETIC_PREREG.json'), pre)
    add_val = repr([ADD['path'], ADD['sha256']]) if pair_form else repr(ADD['sha256'])
    src = ('# SYNTHETIC S-WORLD COMPARE STAND-IN; not a compare of record; never executed\n'
           'V007_PREREG_SHA256 = %r\nPIN_ADDENDUM_V005 = %s\nSCHEMA_REPORT = %r\nPRODUCTION_K_BIG_A55 = 128.0\n' %
           (P['sha256'], add_val, SCHEMA_REPORT))
    if compare:
        src = compare(src, P)
    K = xwrite(os.path.join(d, 'SYNTHETIC_COMPARE.py'), src.encode())
    rep = {'schema': SCHEMA_REPORT, 'synthetic': True, 'test_mode': False,
           'decision': {'tests_read': True, 'outcome': 'ADOPT_TAIL', 'carried_numerical_uncertainty_km_s': {'r1': 0.01, 'r2': 0.02}},
           'prereg': P, 'case_block': dict(CB), 'script_sha256': K['sha256'],
           'pins_verified': {'V005_addendum': [ADD['path'], ADD['sha256']] if pair_form else ADD['sha256']},
           'inputs': {'C4T': {'result_sha256': RESULT['sha256']}}, 'validity': {'C4T': {'valid_all': True}}}
    if verdict:
        verdict(rep)
    V = xwrite(os.path.join(d, 'SYNTHETIC_VERDICT.json'), rep)
    sl = {'schema': 'UNT_V007_SEAL_RECORD_SYNTHETIC_S_WORLD', 'synthetic': True, 'sealed_by': dict(AUTH), 'prereg': P, 'compare': K,
          'driver': dict(R5PIN), 'frozen_addendum': ADD, 'case_block': dict(CB)}
    if seal:
        seal(sl)
    S = xwrite(os.path.join(d, 'SYNTHETIC_SEAL_RECORD.json'), sl)
    tup = (K['sha256'], P['sha256'], ADD['sha256'], rep['schema'], V['sha256'])
    psrc = ('# SYNTHETIC S-WORLD ADOPTION POLICY STAND-IN; never executed\nSYNTHETIC_NOT_SCIENTIFIC = True\n'
            'APPROVED_V007_SEALS = frozenset({%r})\n\n\ndef check_numerics(*a, **k):\n    raise RuntimeError("synthetic")\n' % (tup,))
    if policy:
        psrc = policy(psrc, tup)
    Q = xwrite(os.path.join(d, 'SYNTHETIC_ADOPTION_POLICY.py'), psrc.encode())
    REGP = registry(d) if registry else REG
    c = copy.deepcopy(r9)
    c['synthetic'] = True
    c['notes'] = 'SYNTHETIC S-WORLD C1 for the Claude4 v003 producer tests; not a config of record. ' + str(r9.get('notes'))
    c['numerics']['block'] = copy.deepcopy(c4t['numerics'])
    c['numerics'].update(verdict_artifact=V, block_source={'path': C4T[0], 'sha256': C4T[1]}, compare=K, sealed_prereg=P,
                         adopted_result=RESULT, source_results=[])
    c['tail_readiness'].update(certificate_registry=REGP, certificate_policy_review=REVIEW, approved_certificate_producers=PRODUCERS)
    if c1:
        c1(c, d)
    raw = J(c)
    if c1_raw:
        raw = c1_raw(raw)
    C = xwrite(os.path.join(d, 'SYNTHETIC_C1.json'), raw)
    WORLDS[name] = {'c1': C, 'seal': S, 'policy': Q, 'verdict': V, 'prereg': P, 'compare': K, 'registry': REGP, 'dir': d}
    return WORLDS[name]


def reg_variant(name, fn):
    def build(d):
        doc = copy.deepcopy(REG_DOC)
        fn(doc, d)
        return xwrite(os.path.join(d, 'SYNTHETIC_REGISTRY_VARIANT.json'), doc)
    return build


def reg_raw_variant(name, fn):
    def build(d):
        return xwrite(os.path.join(d, 'SYNTHETIC_REGISTRY_VARIANT.json'), fn(J(REG_DOC)))
    return build


def setp(doc, path, val):
    node = doc
    for k in path[:-1]:
        node = node[k]
    node[path[-1]] = val


# ---- the consistent synthetic seal world (two addendum-pin forms) and the mutations (PR-SF1)
make_world('S_STRING')
make_world('S_PAIR', pair_form=True)
F1_CASES = []   # (id, c3_ref, world name, expected code, extra argv/kind)


def F1(cid, c3, expect, **mut):
    make_world(cid, **mut)
    F1_CASES.append((cid, c3, cid, expect))


F1('F1_A04_ADOPTION_FIELDS_EMPTY_DICTS', 'A04', 'PIN_MALFORMED',
   c1=lambda c, d: [c['numerics'].__setitem__(k, {}) for k in ('verdict_artifact', 'compare', 'sealed_prereg', 'adopted_result')])
F1('F1_A04b_BLOCK_SOURCE_EMPTY', 'A04b', 'PIN_MALFORMED', c1=lambda c, d: c['numerics'].__setitem__('block_source', {}))
F1('F1_A05_PIN_WITH_TARGET_ROWS', 'A05', 'PIN_MALFORMED',
   c1=lambda c, d: c['numerics']['verdict_artifact'].update(rows=[[0.5, 10.1, 1.2]], columns=['R_kpc', 'V_obs_km_s', 'err']))
F1('F1_ZERO_SHA_ADOPTED_RESULT', 'X01 (zero-sha pins)', 'PIN_SHA_ZERO',
   c1=lambda c, d: c['numerics'].__setitem__('adopted_result', {'path': RESULT['path'], 'sha256': '0' * 64}))
F1('F1_S01_SYNTHETIC_TEST_TRUE', 'S01', 'C1_SYNTHETIC_TEST_MUST_BE_FALSE', c1=lambda c, d: c.__setitem__('synthetic_test', True))
F1('F1_DRIVER_NOT_R5', 'v002 neg driver_not_r5', 'CONFIG_DRIVER_NOT_R5', c1=lambda c, d: c.__setitem__('driver', dict(GEOPIN)))
F1('F1_SEAL_SCHEMA', 'PR-SF1 seal', 'SEAL_RECORD_SCHEMA', seal=lambda s: s.__setitem__('schema', 'NOT_A_SEAL_RECORD'))
F1('F1_SEAL_SEALED_BY_NOT_ROOT', 'PR-SF1 seal', 'SEALED_ROOT_BINDING',
   seal=lambda s: s.__setitem__('sealed_by', {'identity': 'Claude4', 'role': 'coordinator_and_single_scientific_launch_owner'}))
F1('F1_SEAL_PREREG_NOT_C1', 'PR-SF1 seal', 'SEALED_ROOT_BINDING', seal=lambda s: s.__setitem__('prereg', dict(CB)))
F1('F1_SEAL_DRIVER_NOT_R5', 'PR-SF1 seal', 'SEALED_R5_BINDING', seal=lambda s: s.__setitem__('driver', dict(GEOPIN)))
F1('F1_SEAL_CASE_BLOCK_OTHER', 'PR-SF1 block_source tie', 'SEAL_CASE_BLOCK_NOT_76309ae3',
   seal=lambda s: s.__setitem__('case_block', {'path': CB['path'], 'sha256': 'a' * 64}))
F1('F1_VERDICT_TEST_MODE_TRUE', 'PR-SF1 verdict', 'SEALED_ADOPT_TAIL_REQUIRED', verdict=lambda v: v.__setitem__('test_mode', True))
F1('F1_VERDICT_TESTS_NOT_READ', 'PR-SF1 verdict', 'SEALED_ADOPT_TAIL_REQUIRED', verdict=lambda v: v['decision'].__setitem__('tests_read', False))
F1('F1_VERDICT_OUTCOME_NOT_ADOPT', 'PR-SF1 verdict', 'SEALED_ADOPT_TAIL_REQUIRED',
   verdict=lambda v: v['decision'].__setitem__('outcome', 'FLAG_PENDING_RULING'))
F1('F1_VERDICT_SCRIPT_SHA_OTHER', 'PR-SF1 verdict', 'VERDICT_BYTE_BINDING', verdict=lambda v: v.__setitem__('script_sha256', 'b' * 64))
F1('F1_VERDICT_CASE_BLOCK_OTHER', 'PR-SF1 block_source tie', 'VERDICT_BYTE_BINDING',
   verdict=lambda v: v.__setitem__('case_block', {'path': CB['path'], 'sha256': 'c' * 64}))
F1('F1_VERDICT_C4T_RESULT_NOT_INPUT', 'policy L84', 'V007_C4T_RESULT_NOT_VERDICT_INPUT',
   verdict=lambda v: v['inputs']['C4T'].__setitem__('result_sha256', 'd' * 64))
F1('F1_VERDICT_C4T_NOT_VALID', 'policy L81', 'V007_C4T_NOT_VALID', verdict=lambda v: v['validity']['C4T'].__setitem__('valid_all', False))
F1('F1_VERDICT_UNCERTAINTY_NONE', 'policy L121 (R-A6)', 'V007_CARRIED_UNCERTAINTY_REQUIRED',
   verdict=lambda v: v['decision'].__setitem__('carried_numerical_uncertainty_km_s', {'r1': None}))
F1('F1_VERDICT_SCHEMA_NOT_V007', 'policy L67', 'V007_REPORT_SCHEMA_MISMATCH', verdict=lambda v: v.__setitem__('schema', 'UNT_OTHER_REPORT'))
F1('F1_PREREG_NO_CASE_BLOCK', 'guard007 L162', 'PREREG_CASE_BLOCK_REQUIRED', prereg=lambda p: p.__setitem__('binding_inputs', {}))
F1('F1_COMPARE_NOT_SEALED', 'policy L52', 'V007_COMPARE_NOT_SEALED',
   compare=lambda s, P: s.replace("V007_PREREG_SHA256 = %r" % P['sha256'], 'V007_PREREG_SHA256 = None'))
F1('F1_COMPARE_PREREG_OTHER', 'policy L54', 'V007_SEALED_PREREG_MISMATCH',
   compare=lambda s, P: s.replace("V007_PREREG_SHA256 = %r" % P['sha256'], "V007_PREREG_SHA256 = %r" % ('e' * 64)))
F1('F1_COMPARE_ADDENDUM_OTHER', 'guard007 L159', 'SEAL_FROZEN_ADDENDUM_NOT_COMPARE_PIN',
   compare=lambda s, P: s.replace("PIN_ADDENDUM_V005 = %r" % ADD['sha256'], "PIN_ADDENDUM_V005 = %r" % ('f' * 64)))
F1('F1_COMPARE_K64', 'policy L65', 'V007_COMPARE_NOT_P128', compare=lambda s, P: s.replace('PRODUCTION_K_BIG_A55 = 128.0', 'PRODUCTION_K_BIG_A55 = 64.0'))
F1('F1_COMPARE_SCHEMA_TWICE', 'parser differential (AST)', 'COMPARE_CONSTANT_NOT_SINGLE_LITERAL',
   compare=lambda s, P: s + 'SCHEMA_REPORT = %r\n' % SCHEMA_REPORT)
F1('F1_POLICY_EMPTY_ALLOWLIST', 'R-A2 today', 'REVIEWED_SEAL_TUPLE_PENDING',
   policy=lambda s, t: s.replace('frozenset({%r})' % (t,), 'frozenset()'))
F1('F1_POLICY_OTHER_TUPLE', 'guard007 L165', 'REVIEWED_SEAL_TUPLE_PENDING',
   policy=lambda s, t: s.replace('frozenset({%r})' % (t,), 'frozenset({%r})' % (t[:4] + ('9' * 64,),)))
F1('F1_POLICY_NOT_LITERAL', 'AST only, never executed', 'ADOPTION_POLICY_SEALS_NOT_A_SINGLE_LITERAL_FROZENSET',
   policy=lambda s, t: s.replace('frozenset({%r})' % (t,), 'make_seals()'))
F1('F1_POLICY_NO_CHECK_NUMERICS', 'AST only', 'ADOPTION_POLICY_HAS_NO_CHECK_NUMERICS',
   policy=lambda s, t: s.replace('def check_numerics(', 'def other_function('))


def forged_source(d, numerics):
    src = copy.deepcopy(c4t)
    src['numerics'] = numerics
    return xwrite(os.path.join(d, 'SYNTHETIC_FORGED_BLOCK_SOURCE.json'), src)


def y01(c, d):
    c['numerics']['block']['picard']['passes'] = 5
    c['numerics']['block_source'] = forged_source(d, copy.deepcopy(c['numerics']['block']))


F1('F1_Y01_FORGED_BLOCK_AND_SOURCE', 'Y01', 'BLOCK_SOURCE_NOT_CASE_BLOCK_C4T', c1=y01)


def forged(mutate):
    def c1m(c, d):
        mutate(c['numerics']['block'])
        c['numerics']['block_source'] = forged_source(d, copy.deepcopy(c['numerics']['block']))
    return c1m


F1('F1_A02_FORGED_SOURCE_EXTRA_KEY', 'A02', 'BLOCK_SOURCE_NOT_CASE_BLOCK_C4T', c1=forged(lambda b: b.__setitem__('free_override_c3', 1.0)))
F1('F1_A03_FORGED_SOURCE_PHYSICAL_OVERRIDE', 'A03 / Y_A03', 'BLOCK_SOURCE_NOT_CASE_BLOCK_C4T',
   c1=forged(lambda b: b.__setitem__('physical_override_c3', {'distance_Mpc': 9.9, 'inclination_deg': 71.5})))
F1('F1_B04_FORGED_SOURCE_OTHER_GALAXY_GEOMETRY', 'B04 / Y_B04', 'BLOCK_SOURCE_NOT_CASE_BLOCK_C4T',
   c1=forged(lambda b: b.__setitem__('galaxy_geometry', {'galaxy': 'OTHER', 'inclination_deg': 71.5, 'distance_Mpc': 13.8})))
F1('F1_E02_FORGED_SOURCE_TARGET_KEY_IN_UV_TAIL', 'E02 / Y_E02', 'BLOCK_SOURCE_NOT_CASE_BLOCK_C4T',
   c1=forged(lambda b: b['uv_tail'].__setitem__('vobs_rows', [[0.5, 10.1, 1.2]])))
F1('F1_B01_COORDINATE_SPEC_SHA_SWAPPED', 'B01', 'COORDINATE_SPEC_NOT_50e7288e', c1=lambda c, d: c['coordinate_spec'].__setitem__('sha256', '1' * 64))
F1('F1_B03_ANCHOR_OTHER_INCLINATION', 'B03', 'CONFIG_ANCHOR_NOT_TEMPLATE_POINT', c1=lambda c, d: c['anchor']['physical'].__setitem__('inclination_deg', 71.5))
F1('F1_Y02_FORGED_BLOCK_REAL_SOURCE', 'Y02', 'C1_BLOCK_DIFFERS_FROM_ADOPTED_C4T',
   c1=lambda c, d: c['numerics']['block']['picard'].__setitem__('passes', 5))
F1('F1_A01_BLOCK_EXTRA_KEY', 'A01', 'C1_BLOCK_DIFFERS_FROM_ADOPTED_C4T', c1=lambda c, d: c['numerics']['block'].__setitem__('free_override_c3', 1.0))
F1('F1_D10a_LAMBDA_TRUE', 'D10a (True == 1.0)', 'C1_BLOCK_DIFFERS_FROM_ADOPTED_C4T',
   c1=lambda c, d: c['numerics']['block']['uv_tail'].__setitem__('lambda_scale', True))
F1('F1_D11a_MS_FLOAT', 'D11a (128.0 == 128)', 'C1_BLOCK_DIFFERS_FROM_ADOPTED_C4T',
   c1=lambda c, d: c['numerics']['block']['uv_tail']['gas'].__setitem__('M_s', 128.0))
F1('F1_D12a_WORKERS_FLOAT', 'D12a (8.0 == 8)', 'C1_BLOCK_DIFFERS_FROM_ADOPTED_C4T',
   c1=lambda c, d: c['numerics']['block']['route_a'].__setitem__('column_workers', 8.0))
F1('F1_REGISTRY_NULL', 'v002 neg final_null_registry', 'PIN_REQUIRED',
   c1=lambda c, d: c['tail_readiness'].__setitem__('certificate_registry', None))
F1('F1_PRODUCERS_EMPTY', 'guard007 L202-203', 'CERTIFICATE_PRODUCERS_REQUIRED',
   c1=lambda c, d: c['tail_readiness'].__setitem__('approved_certificate_producers', []))


def bad_review(fn):
    def c1m(c, d):
        doc = copy.deepcopy(REVIEW_DOC)
        fn(doc)
        c['tail_readiness']['certificate_policy_review'] = xwrite(os.path.join(d, 'SYNTHETIC_POLICY_REVIEW_VARIANT.json'), doc)
    return c1m


F1('F1_POLICY_REVIEW_SCHEMA', 'wrapper certificate_policy_gate', 'CERTIFICATE_POLICY_REVIEW_SCHEMA', c1=bad_review(lambda r: r.__setitem__('schema', 'X')))
F1('F1_POLICY_REVIEW_NOT_OK', 'wrapper certificate_policy_gate', 'CERTIFICATE_POLICY_REVIEW_NOT_TESTED_OK', c1=bad_review(lambda r: r.__setitem__('ok', False)))
F1('F1_POLICY_REVIEW_BINDING', 'wrapper certificate_policy_gate', 'CERTIFICATE_POLICY_REVIEW_BINDING',
   c1=bad_review(lambda r: r.__setitem__('approved_certificate_producers', [PROD_EPS])))
F1('F1_A08_NO_SCHEMA_NO_BUNDLE', 'A08', 'PIN_REQUIRED',
   registry=reg_variant('A08', lambda doc, d: (doc.__setitem__('schema', 'NOT_A_CERTIFICATE_REGISTRY'),
                                               [p.pop('bundle') for p in doc['points'].values()])))
F1('F1_BUNDLE_SCHEMA', 'certificate_check bundle', 'BUNDLE_SCHEMA_OR_IDENTITY_MISMATCH',
   registry=reg_variant('BS', lambda doc, d: doc['points'].__setitem__(FIRST, make_point(d, FIRST, bundle_mut=lambda b: b.__setitem__('schema', 'X')))))
F1('F1_BUNDLE_NOT_BINDING_SLOTS', 'wrapper L145-147', 'BUNDLE_DOES_NOT_BIND_THE_SLOTS',
   registry=reg_variant('BB', lambda doc, d: doc['points'].__setitem__(FIRST, make_point(
       d, FIRST, bundle_mut=lambda b: b['driver_certificate_bindings'].__setitem__('eps_certificate', A70['eps_certificate'])))))
F1('F1_PROOF_NOT_PASS', 'wrapper L155-156', 'PROOF_NOT_TESTED_PASS',
   registry=reg_variant('PP', lambda doc, d: doc['points'].__setitem__(FIRST, make_point(d, FIRST, eps_mut=lambda p: p.__setitem__('verdict', 'FAIL')))))
F1('F1_Y04_PROOF_PRODUCER_NOT_APPROVED', 'Y04', 'PROOF_PRODUCER_NOT_APPROVED',
   registry=reg_variant('PU', lambda doc, d: doc['points'].__setitem__(FIRST, make_point(
       d, FIRST, eps_mut=lambda p: p.__setitem__('producer', xwrite(os.path.join(d, 'SYNTHETIC_UNAPPROVED_PRODUCER.py'), b'# synthetic\n'))))))
F1('F1_LO_NOT_COVERING_ALL_STATES', 'wrapper L160-161 (no anchor substitution)', 'LO_ENVELOPE_NOT_COVERING_ALL_CONSUMED_STATES',
   registry=reg_variant('LO', lambda doc, d: doc['points'].__setitem__(FIRST, make_point(
       d, FIRST, lo_mut=lambda p: p.__setitem__('covers_all_consumed_states', False)))))
F1('F1_PROOF_POINT_OTHER', 'verify_bundle scope', 'PROOF_POINT_MISMATCH',
   registry=reg_variant('PO', lambda doc, d: doc['points'].__setitem__(FIRST, make_point(d, FIRST, eps_mut=lambda p: p.__setitem__('point_sha256', ANCHOR)))))
F1('F1_X01_A70_ON_ALL_POINTS', 'X01 (no anchor promotion)', 'A70_SLOT_OUTSIDE_ANCHOR_POINT',
   registry=reg_variant('A70', lambda doc, d: [doc['points'].__setitem__(k, make_point(d, k, eps=A70['eps_certificate'], lo=A70['lo_certificate']))
                                               for k in NONANCHOR]))
F1('F1_REGISTRY_POINT_MISSING', 'v002 neg registry_point_missing', 'REGISTRY_POINT_MISSING',
   registry=reg_variant('PM', lambda doc, d: doc['points'].pop(FIRST)))
F1('F1_C06_POINT_UNDER_WRONG_KEY', 'C06', 'REGISTRY_POINT_MISSING',
   registry=reg_variant('WK', lambda doc, d: doc['points'].__setitem__('f' * 64, doc['points'].pop(FIRST))))
F1('F1_REGISTRY_IDENTITY_MISMATCH', 'v002 neg / A09', 'REGISTRY_IDENTITY_MISMATCH',
   registry=reg_variant('IM', lambda doc, d: doc['points'][FIRST]['identity'].__setitem__('extra', 1)))
F1('F1_SLOT_SHA_WRONG', 'v002 neg registry_slot_ref_sha_wrong', 'PIN_MISMATCH',
   registry=reg_variant('SW', lambda doc, d: doc['points'][FIRST]['eps_certificate'].__setitem__('sha256', '1' * 64)))
F1('F1_C03_SLOT_SHA_UPPERCASE', 'C03', 'PIN_MALFORMED',
   registry=reg_variant('SU', lambda doc, d: doc['points'][FIRST]['eps_certificate'].__setitem__(
       'sha256', BASE_POINTS[FIRST]['eps_certificate']['sha256'].upper())))
F1('F1_C04_SLOT_SENTINEL', 'C04/C05', 'PIN_REQUIRED', registry=reg_variant('SS', lambda doc, d: doc['points'][FIRST].__setitem__('eps_certificate', 'NONE_TEST_ONLY')))
F1('F1_A06_SLOT_REF_EXTRA_KEY', 'A06/A07', 'PIN_MALFORMED',
   registry=reg_variant('SX', lambda doc, d: doc['points'][FIRST]['eps_certificate'].__setitem__('vobs_rows', [[0.5, 10.1, 1.2]])))
F1('F1_C01_SLOT_IS_PAIR_PLAN', 'C01', 'BUNDLE_DOES_NOT_BIND_THE_SLOTS',
   registry=reg_variant('PL', lambda doc, d: doc['points'][FIRST].__setitem__('eps_certificate', {'path': P1.PAIR_PLAN[0], 'sha256': P1.PAIR_PLAN[1]})))
TEMPLATE_PIN = {'path': w_ids.inputs['template']['path'], 'sha256': w_ids.inputs['template']['sha256']}
F1('F1_CERT_OUTSIDE_ALLOWED_ROOT', 'certificate guard _read roots', 'INPUT_OUTSIDE_ALLOWED_ROOT',
   registry=reg_variant('OR', lambda doc, d: doc['points'].__setitem__(FIRST, make_point(d, FIRST, eps=dict(TEMPLATE_PIN)))))
# PR-SF5 cases that need a world (strict JSON, final mode)
F5W = []


def F5(cid, c3, expect, **mut):
    make_world(cid, **mut)
    F5W.append((cid, c3, cid, expect))


F5('F5_D01_DUPLICATE_KEY_C1', 'D01', 'JSON_DUPLICATE_KEY', c1_raw=lambda raw: b'{"synthetic_test": true, ' + raw[1:].lstrip())
F5('F5_D01R_DUPLICATE_KEY_C1_REVERSED', 'D01R', 'JSON_DUPLICATE_KEY', c1_raw=lambda raw: raw.rstrip()[:-1].rstrip() + b', "synthetic_test": true}\n')
F5('F5_D02_DUPLICATE_KEY_REGISTRY', 'D02', 'JSON_DUPLICATE_KEY',
   registry=reg_raw_variant('D02', lambda raw: b'{"points": {}, ' + raw[1:].lstrip()))
F5('F5_D03a_NAN_IN_BLOCK', 'D03a', 'JSON_NONFINITE',
   c1=lambda c, d: c['numerics']['block']['picard'].__setitem__('nan_c3', 'NANMARK'), c1_raw=lambda raw: raw.replace(b'"NANMARK"', b'NaN'))
F5('F5_INFINITY', 'D03 Infinity', 'JSON_NONFINITE', c1=lambda c, d: c.__setitem__('x', 'INFMARK'), c1_raw=lambda raw: raw.replace(b'"INFMARK"', b'Infinity'))
F5('F5_NEG_INFINITY', 'D03 -Infinity', 'JSON_NONFINITE', c1=lambda c, d: c.__setitem__('x', 'INFMARK'), c1_raw=lambda raw: raw.replace(b'"INFMARK"', b'-Infinity'))
F5('F5_D06_INT_5001_DIGITS', 'D06', 'JSON_INTEGER_TOO_LONG', c1_raw=lambda raw: b'{"big_c3": 1' + b'0' * 5000 + b', ' + raw[1:].lstrip())
F5('F5_INT_65_DIGITS', 'D06 boundary', 'JSON_INTEGER_TOO_LONG', c1_raw=lambda raw: b'{"big_c3": 1' + b'0' * 64 + b', ' + raw[1:].lstrip())
F5('F5_D07_DEEP_200000', 'D07', 'JSON_TOO_DEEP', c1_raw=lambda raw: b'{"deep_c3": ' + b'[' * 200000 + b']' * 200000 + b', ' + raw[1:].lstrip())
F5('F5_DEEP_65', 'D07 boundary', 'JSON_TOO_DEEP', c1_raw=lambda raw: b'{"deep_c3": ' + b'[' * 64 + b']' * 64 + b', ' + raw[1:].lstrip())
F5('F5_D08_INVALID_UTF8', 'D08', 'JSON_NOT_UTF8', c1_raw=lambda raw: b'{"bad_utf8_c3": "\xff\xfe", ' + raw[1:].lstrip())
F5('F5_D09_UTF8_BOM', 'D09', 'JSON_BOM', c1_raw=lambda raw: b'\xef\xbb\xbf' + raw)
F5('F5_UTF16_BOM', 'PR-SF5 encodings', 'JSON_BOM', c1_raw=lambda raw: raw.decode().encode('utf-16'))
F5('F5_UTF32_BOM', 'PR-SF5 encodings', 'JSON_BOM', c1_raw=lambda raw: raw.decode().encode('utf-32'))
F5('F5_UTF16LE_NO_BOM', 'PR-SF5 encodings', 'JSON_NUL', c1_raw=lambda raw: raw.decode().encode('utf-16-le'))
F5('F5_SYNTAX_TRUNCATED', 'PR-SF5', 'JSON_SYNTAX', c1_raw=lambda raw: raw[:len(raw) // 2])
# PR-SF2 decode-time forced failures (final mode, before any write)
F2W = []


def F2(cid, c3, expect, **mut):
    make_world(cid, **mut)
    F2W.append((cid, c3, cid, expect))


F2('F2_D04_1E999_IN_ADOPTION_PIN', 'D04', 'JSON_NONFINITE',
   c1=lambda c, d: c['numerics']['verdict_artifact'].__setitem__('x', 'INFMARK'), c1_raw=lambda raw: raw.replace(b'"INFMARK"', b'1e999'))
F2('F2_D05_NAN_IN_INPUT_PIN', 'D05', 'JSON_NONFINITE',
   c1=lambda c, d: c['coordinate_spec'].__setitem__('x', 'NANMARK'), c1_raw=lambda raw: raw.replace(b'"NANMARK"', b'NaN'))
# PR-SF3 fixtures: protected names (never created), an innocent link to a protected target, a big file, a hard-link source
LOOK = os.path.join(FIX, 'SYNTHETIC_PROTECTED_NAME_PROBES')
os.mkdir(LOOK)
os.symlink(os.path.join(LOOK, 'runs_ext', 'UVT_FAKE', 'cert.json'), os.path.join(LOOK, 'innocent_link.json'))
os.symlink(os.path.join(LOOK, 'x_rotmod_target.json'), os.path.join(LOOK, 'innocent_link_two.json'))
BIG = xwrite(os.path.join(LOOK, 'innocent_big_9MiB.json'), b'{"pad": "' + b'x' * (9 * 1024 * 1024) + b'"}\n')
SMALL = xwrite(os.path.join(LOOK, 'innocent_small_4KiB.json'), b'{"pad": "' + b'y' * 4096 + b'"}\n')
HLSRC = xwrite(os.path.join(LOOK, 'innocent_hardlink_source.json'), {'synthetic': True, 'note': 'hard-link source'})
PROT = {'B06_UGC5572_N3198': 'UGC5572_N3198_lookalike_cert.json', 'B07_NGC_SPACE': 'NGC 3198 lookalike cert.json',
        'B08_DDO154_VROT': 'DDO154_vrot_lookalike_cert.json', 'B09_ROTMOD': 'x_rotmod_lookalike.json',
        'N3198': 'N3198_cert.json', 'NGC_DASH': 'NGC-3198_rc.json', 'NGC_PY': 'ngc3198_rc.py', 'VEL_OBS': 'DDO154/vel_obs/x.json',
        'TARGET_VELOCITIES': 'target_velocities.json', 'OBSERVED_ROTATION': 'observed_rotation_velocities.json',
        'ROTATION_CURVE': 'DDO154_rotation_curve.json', 'OBS_REGION': 'DDO154_CALIBRATION_OBSERVATION_REGION_V001.json',
        'NPZ': 'grid.npz', 'DOTDOT_HIDDEN': 'rotmod/../innocent.json', 'B10_INNOCENT_LINK': 'innocent_link.json',
        'G03_LINK_TO_ROTMOD': 'innocent_link_two.json'}
PROT_DIR = {nm: 'F3_P%02d' % i for i, nm in enumerate(sorted(PROT))}   # neutral folder names (a protected word may not name a folder)
for nm, rel in sorted(PROT.items()):
    def slot_to(rel=rel):
        return lambda doc, d: doc['points'][FIRST].__setitem__('eps_certificate', {'path': os.path.join(LOOK, rel), 'sha256': '2' * 64})
    make_world(PROT_DIR[nm], registry=reg_variant(nm, slot_to()))
make_world('F3_VOL_VERDICT', c1=lambda c, d: c['numerics'].__setitem__('verdict_artifact', {'path': '/.vol/16777220/2', 'sha256': '3' * 64}))
make_world('F3_VOL_DOTDOT_VERDICT', c1=lambda c, d: c['numerics'].__setitem__('verdict_artifact', {'path': '/private/../.vol/1/2', 'sha256': '3' * 64}))
make_world('F3_BIG_SLOT_CERT', registry=reg_variant('BIG', lambda doc, d: doc['points'].__setitem__(FIRST, make_point(d, FIRST, eps=BIG))))
PHASE_A = {'utc_arg': UTC, 'seconds': round(time.time() - T0, 2), 'worlds': len(WORLDS), 'keys': len(KEYS), 'anchor_present': True,
           'fence_blocked_phase_a': list(FENCE_A.BLOCKED)}
assert not FENCE_A.BLOCKED, FENCE_A.BLOCKED

# ================================================================================================ Phase B: the copy
P2, P2SHA = _load(os.path.join(RUN, 'tools', PROD_NAME), 'c4v003_producer_phaseB')
assert P2SHA == PROD_SHA and P2.FENCE.REVIEW == RUN, (P2SHA, PROD_SHA, P2.FENCE.REVIEW)
F2_ = P2.FENCE
FENCES = (FENCE_A, F2_)      # two loaded copies of the same fence bytes: the Phase A one runs first and refuses first
CERT_ROOT_OVERRIDE = None
if not V3.startswith(P2.CERT_ROOT + os.sep):          # development runs outside claude_artifacts only; recorded, never in the record run
    CERT_ROOT_OVERRIDE = P2.CERT_ROOT = '/'      # dev only: then F1_CERT_OUTSIDE_ALLOWED_ROOT cannot refuse
RESULTS = []


def reset():
    P2.READER = P2.Reader()
    P2.OPENS = []


def run_main(argv):
    reset()
    out, err = io.StringIO(), io.StringIO()
    b0 = [len(f.BLOCKED) for f in FENCES]
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = P2.main(argv)
    lines = [ln for ln in out.getvalue().splitlines() if ln.strip()]
    try:
        js = json.loads(lines[-1]) if lines else {}
    except ValueError:
        js = {'unparsed': lines[-1][:200]}
    return rc, js, err.getvalue(), [b for f, n in zip(FENCES, b0) for b in f.BLOCKED[n:]]


def final_argv(w, outname, extra=()):
    return ['final', '--config', w['c1']['path'], '--config-sha', w['c1']['sha256'], '--seal', w['seal']['path'], '--seal-sha',
            w['seal']['sha256'], '--adoption-policy', w['policy']['path'], '--adoption-policy-sha', w['policy']['sha256'],
            '--outdir', os.path.join(RUN, outname), '--utc', UTC] + list(extra)


def record(cid, fix, c3, expect, rc, js, err, blocked, outname, extra=None, ok_override=None):
    od = os.path.join(RUN, outname) if outname else None
    created = bool(od and os.path.lexists(od))
    code = js.get('code')
    if ok_override is not None:
        ok = ok_override
    else:
        ok = (rc == 3 and js.get('status') == 'REFUSED' and code == expect and not created and err == '')
    rec = {'id': cid, 'fix': fix, 'c3_ref': c3, 'expected': expect, 'exit': rc, 'status': js.get('status'), 'code': code,
           'reason': (js.get('reason') or '')[:300], 'outdir_created': created, 'stderr_empty': err == '',
           'fence_blocked_new': [list(b) for b in blocked], 'passed': bool(ok)}
    if extra:
        rec.update(extra)
    RESULTS.append(rec)
    return rec


def cases_final(lst, fix):
    for cid, c3, wname, expect in lst:
        rc, js, err, bl = run_main(final_argv(WORLDS[wname], 'out_' + cid))
        record(cid, fix, c3, expect, rc, js, err, bl, 'out_' + cid)


# ---------------------------------------------------------------- R: v002 reproduction (29/29 dry, 29/29 PROVISIONAL)
reset()
inv = P2.READER.doc({'path': P2.SPEC_INV[0], 'sha256': P2.SPEC_INV[1]}, 'V001 spec inventory')
prov = P2.READER.doc({'path': P2.PROBE_REC[0], 'sha256': P2.PROBE_REC[1]}, 'V001 post-adoption probe')
dry = {r['name']: r for r in inv['specs']}
pv = prov['specs']


def compare_rows(rows, expect):
    res = {}
    for r in rows:
        e = expect[r['case']]
        raw = P2.READER.raw({'path': e['path'], 'sha256': e['sha256']}, 'expected ' + r['case'])
        res[r['case']] = raw == r['raw']
    return res


cfg_r9 = P2.READER.doc({'path': R9[0], 'sha256': R9[1]}, 'r9 config')
pin_r9 = {'path': R9[0], 'sha256': R9[1]}
w1 = P2.World(cfg_r9, pin_r9, P2.NOTE_DRY)
rows1 = w1.build_all()
c1r = compare_rows(rows1, {k: {'path': v['path'], 'sha256': v['sha256']} for k, v in dry.items()})
keys_native = all(r['theta_key'] == dry[r['case']].get('theta_key') and r['point_key'] == dry[r['case']].get('certificate_point_key') and
                  all(r['theta'][k] == dry[r['case']]['theta'][k] for k in dry[r['case']]['theta'])
                  for r in rows1 if r['construction'] == 'MAPPER_BUILD')
record('R1_W1_DRY_R9_BITWISE', 'v002 reproduction', 'T-REPRO W1', '29/29', 0, {'status': 'REPRODUCED'}, '', [], None,
       extra={'bitwise_equal': sum(c1r.values()), 'n': len(rows1), 'mapper_keys_equal_native_records': keys_native},
       ok_override=(sum(c1r.values()) == 29 and len(rows1) == 29 and keys_native))
filled = P2.READER.doc({'path': C4T[0], 'sha256': C4T[1]}, 'C4T FILLED')
cfg2 = copy.deepcopy(cfg_r9)
for k in ('eps_certificate', 'lo_certificate'):
    cfg2['numerics']['block']['uv_tail'][k] = copy.deepcopy(filled['numerics']['uv_tail'][k])
w2 = P2.World(cfg2, {'path': R9[0] + ' [in-memory: block slots := C4T FILLED slots]', 'sha256': None}, P2.NOTE_PROV)
rows2 = w2.build_all()
exp2 = {k: {'path': v['path'], 'sha256': v['sha256']} for k, v in pv.items()}
c2r = compare_rows(rows2, exp2)
record('R2_W2_PROVISIONAL_BLOCK_BITWISE', 'v002 reproduction', 'T-REPRO W2', '29/29', 0, {'status': 'REPRODUCED'}, '', [], None,
       extra={'bitwise_equal': sum(c2r.values()), 'c4t_numerics_equal_r9_block_plus_a70': P2.same(filled['numerics'], cfg2['numerics']['block'])},
       ok_override=(sum(c2r.values()) == 29 and P2.same(filled['numerics'], cfg2['numerics']['block'])))
w3 = P2.World(cfg_r9, pin_r9, P2.NOTE_PROV, registry_pin=W3_REG)
rows3 = w3.build_all()
c3r = compare_rows(rows3, exp2)
record('R3_W3_SYNTHETIC_REGISTRY_BITWISE', 'v002 reproduction', 'T-REPRO W3', '29/29', 0, {'status': 'REPRODUCED'}, '', [], None,
       extra={'bitwise_equal': sum(c3r.values()), 'distinct_points': len({r['point_key'] for r in rows3})},
       ok_override=(sum(c3r.values()) == 29))
cbd = P2.READER.doc(CB, 'case block')
note = cbd['cases']['C4T'].get('note', '')
record('R4_ADOPTED_BLOCK_PROVENANCE', 'PR-SF1 block_source tie', 'v002 adopted_block_provenance', 'names C4T FILLED', 0,
       {'status': 'TESTED'}, '', [], None,
       extra={'note_names_path': C4T[0] in note, 'note_names_sha': C4T[1] in note, 'drivers_allowed_r5': P2.R5[1] in cbd['cases']['C4T']['drivers_allowed'],
              'tail': cbd['cases']['C4T']['tail'], 'anchor_key_three_cases': sorted(r['case'] for r in rows1 if r['point_key'] == ANCHOR)},
       ok_override=(C4T[0] in note and C4T[1] in note and cbd['cases']['C4T']['tail'] is True))
read_once_r = all(rec['physical_reads'] == 1 for rec in P2.READER.log())
record('R5_READ_ONCE_DURING_REPRODUCTION', 'PR-SF3 read once', 'G01 / slot certs read 29x', 'every input read once', 0, {'status': 'TESTED'},
       '', [], None, extra={'files': len(P2.READER.log()), 'a70_eps_references': next(
           (x['references'] for x in P2.READER.log() if x['path'] == A70['eps_certificate']['path']), None)}, ok_override=read_once_r)

# ---------------------------------------------------------------- K: compatibility with the real seal-artifact forms (dry run)
reset()
try:
    seal_dr = P2.READER.doc({'path': DRYRUN + '/V007_SEAL_ASSEMBLY/SEAL_RECORD_V007.json',
                             'sha256': H(open(DRYRUN + '/V007_SEAL_ASSEMBLY/SEAL_RECORD_V007.json', 'rb').read())}, 'dry-run SEAL_RECORD')
    k1 = {'schema_prefix': seal_dr['schema'].startswith(P2.SEAL_SCHEMA_PREFIX), 'sealed_by_root': P2.same(seal_dr['sealed_by'], AUTH),
          'driver_r5': seal_dr['driver']['sha256'] == P2.R5[1], 'case_block_76309ae3': P2.same(seal_dr['case_block'], CB),
          'exact_pins': all(set(seal_dr[k]) == {'path', 'sha256'} for k in ('prereg', 'compare', 'driver', 'frozen_addendum', 'case_block'))}
    csrc = P2.READER.raw(seal_dr['compare'], 'dry-run sealed compare')
    consts, seen, _ = P2._literal_constants(csrc, 'dry-run sealed compare')
    add_raw = P2.READER.raw(seal_dr['frozen_addendum'], 'dry-run frozen addendum')
    pre_dr = P2.READER.doc(seal_dr['prereg'], 'dry-run sealed prereg')
    k2 = {'prereg_sha_constant': consts.get('V007_PREREG_SHA256') == seal_dr['prereg']['sha256'],
          'addendum_constant_form': type(consts.get('PIN_ADDENDUM_V005')).__name__,
          'addendum_constant_equals_frozen': consts.get('PIN_ADDENDUM_V005') == seal_dr['frozen_addendum']['sha256'],
          'frozen_addendum_is_v005_final_c01b3c51': seal_dr['frozen_addendum']['sha256'] == 'c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1',
          'schema_report': consts.get('SCHEMA_REPORT'), 'k_big': consts.get('PRODUCTION_K_BIG_A55'),
          'single_assignments': all(seen.get(k) == 1 for k in ('V007_PREREG_SHA256', 'PIN_ADDENDUM_V005', 'SCHEMA_REPORT', 'PRODUCTION_K_BIG_A55')),
          'prereg_binds_case_block': P2.same((pre_dr.get('binding_inputs') or {}).get('case_block'), CB)}
    pol_src = P2.READER.raw({'path': POLICY_R7[0], 'sha256': POLICY_R7[1]}, 'adoption policy r7')
    pc, ps, pt = P2._literal_constants(pol_src, 'adoption policy r7')
    k3 = {'r7_allowlist_empty_frozenset': pc.get('APPROVED_V007_SEALS') == frozenset() and ps.get('APPROVED_V007_SEALS') == 1,
          'r7_requires_pair_form_L56_58': b"isinstance(add,(list,tuple)) or len(add)!=2" in pol_src}
    kok = all(k1.values()) and k2['prereg_sha_constant'] and k2['addendum_constant_equals_frozen'] and k2['single_assignments'] and \
        k2['prereg_binds_case_block'] and str(k2['schema_report']).startswith(P2.REPORT_SCHEMA_PREFIX) and k2['k_big'] == 128.0
    record('K1_REAL_SEAL_ARTIFACT_FORMS_PARSE', 'PR-SF1 compatibility', 'seal assembly dry run 20261019T010953Z', 'forms accepted',
           0, {'status': 'TESTED'}, '', [], None, extra={'seal_record': k1, 'sealed_compare': k2, 'policy_r7': k3,
                                                         'frozen_addendum_bytes': len(add_raw)}, ok_override=kok)
    record('K2_POLICY_R7_VS_SEALED_COMPARE_ADDENDUM_FORM', 'build finding (R-A2)', 'policy r7 L56-58 vs compare r13 L172', 'finding recorded',
           0, {'status': 'TESTED'}, '', [], None,
           extra={'sealed_compare_PIN_ADDENDUM_V005_form': k2['addendum_constant_form'], 'policy_r7_requires_pair': k3['r7_requires_pair_form_L56_58'],
                  'reading': 'policy r7 check_numerics raises V007_ADDENDUM_EXACT_BYTE_PIN_REQUIRED on a str PIN_ADDENDUM_V005 (L56-58) and '
                             'compares pins_verified.V005_addendum to list(add) (L63); the policy successor (R-A2/R-B3) must read the sha-string '
                             'form; the producer accepts both forms and ties either to the SEAL_RECORD frozen_addendum sha'},
           ok_override=(k2['addendum_constant_form'] == 'str' and k3['r7_requires_pair_form_L56_58']))
except Exception as exc:                  # recorded, never hidden
    record('K1_REAL_SEAL_ARTIFACT_FORMS_PARSE', 'PR-SF1 compatibility', 'dry run', 'forms accepted', 4, {'status': 'ERROR', 'code': type(exc).__name__,
           'reason': str(exc)[:300]}, '', [], None, ok_override=False)

# ---------------------------------------------------------------- S: the consistent synthetic world
for nm in ('S_STRING', 'S_PAIR'):
    rc, js, err, bl = run_main(final_argv(WORLDS[nm], 'out_S1_' + nm))
    reason = js.get('reason') or ''
    record('S1_FINAL_REACHES_LAST_GATE_' + nm, 'PR-SF1 (all checks satisfiable; synthetic refused last)', 'X01/W4 successor',
           'SYNTHETIC_INPUT_REFUSED_IN_FINAL_MODE', rc, js, err, bl, 'out_S1_' + nm,
           extra={'reason_names_path_marker': 'input paths carry a synthetic' in reason,
                  'reason_names_document_marker': 'documents declare synthetic' in reason,
                  'files_read': len(P2.READER.log()), 'all_read_once': all(x['physical_reads'] == 1 for x in P2.READER.log())})
s_read_once = all(x['physical_reads'] == 1 for x in P2.READER.log())
bundle_refs = sum(1 for x in P2.READER.log() if 'SYNTHETIC_BUNDLE_' in x['path'])
w = WORLDS['S_STRING']
rc, js, err, bl = run_main(['provisional', '--config', w['c1']['path'], '--config-sha', w['c1']['sha256'], '--registry', w['registry']['path'],
                            '--registry-sha', w['registry']['sha256'], '--outdir', os.path.join(RUN, 'out_S3_PROVISIONAL_SWORLD'), '--utc', UTC])
mp = os.path.join(RUN, 'out_S3_PROVISIONAL_SWORLD', P2.MANIFEST_PROV)
man3 = rjson(mp) if os.path.exists(mp) else {}
specdir = os.path.join(RUN, 'out_S3_PROVISIONAL_SWORLD', 'specs')
names3 = sorted(os.listdir(specdir)) if os.path.isdir(specdir) else []
spec3 = {n[:-5]: open(os.path.join(specdir, n), 'rb').read() for n in names3}
no_final_word = all(b'FINAL' not in v for v in spec3.values()) and 'FINAL' not in json.dumps(man3.get('label_note', '')) and \
    not os.path.exists(os.path.join(RUN, 'out_S3_PROVISIONAL_SWORLD', P2.MANIFEST_FINAL))
ok3 = (rc == 0 and man3.get('status') == 'PROVISIONAL_NOT_LAUNCH_SPECS' and 'binder_pins' not in man3 and len(spec3) == 29 and no_final_word and
       all(x['physical_reads'] == 1 for x in man3.get('reads', [])))
record('S3_PROVISIONAL_MODE_SWORLD_WRITES_PROVISIONAL_ONLY', 'PR-SF1 (synthetic only in the named provisional mode)', 'X02/X03 successor',
       'PROVISIONAL, never FINAL', rc, js, err, bl, None,
       extra={'manifest_status': man3.get('status'), 'binder_pins_key_present': 'binder_pins' in man3, 'n_specs': len(spec3),
              'no_FINAL_in_labels_or_names': no_final_word, 'reads_all_once': all(x['physical_reads'] == 1 for x in man3.get('reads', [])),
              'a70_eps_refs': next((x['references'] for x in man3.get('reads', []) if x['path'] == A70['eps_certificate']['path']), None)},
       ok_override=ok3)
# S4: the FINAL construction in memory on the same world, never written
reset()
cS = P2.READER.doc(w['c1'], 'S-world C1')
wS = P2.World(cS, w['c1'], P2.NOTE_FINAL, registry_pin=w['registry'])
rowsS = wS.build_all()
mapper_eq = sum(1 for r in rowsS if r['construction'] == 'MAPPER_BUILD' and spec3.get(r['case']) == r['raw'])
hand_eq = 0
for r in rowsS:
    if r['construction'] != 'MAPPER_BUILD' and r['case'] in spec3:
        a, b = json.loads(r['raw']), json.loads(spec3[r['case']])
        a.pop('label')
        b.pop('label')
        hand_eq += P2.same(a, b)
record('S4_INMEMORY_FINAL_EQUALS_PROVISIONAL_EXCEPT_LABEL', 'PR-SF1/PR-SF2 (FINAL bytes never written from synthetic inputs)', 'W4 successor',
       '9/9 mapper bytes, 20/20 except label', 0, {'status': 'TESTED'}, '', [], None,
       extra={'mapper_equal': mapper_eq, 'hand_equal_except_label': hand_eq, 'final_rows_written': 0},
       ok_override=(mapper_eq == 9 and hand_eq == 20))
# S5: provisional mode on the r9 config (pre-adoption, no registry)
rc, js, err, bl = run_main(['provisional', '--config', R9[0], '--config-sha', R9[1], '--outdir', os.path.join(RUN, 'out_S5_PROVISIONAL_R9'), '--utc', UTC])
sd5 = os.path.join(RUN, 'out_S5_PROVISIONAL_R9', 'specs')
spec5 = {n[:-5]: open(os.path.join(sd5, n), 'rb').read() for n in sorted(os.listdir(sd5))} if os.path.isdir(sd5) else {}
m_eq = sum(1 for r in rows1 if r['construction'] == 'MAPPER_BUILD' and spec5.get(r['case']) == r['raw'])
h_eq = 0
for r in rows1:
    if r['construction'] != 'MAPPER_BUILD' and r['case'] in spec5:
        a, b = json.loads(r['raw']), json.loads(spec5[r['case']])
        a.pop('label')
        b.pop('label')
        h_eq += P2.same(a, b)
record('S5_PROVISIONAL_MODE_R9_EQUALS_DRY', 'v002 reproduction through the CLI path', 'T-REPRO', '9/9 mapper, 20/20 except label', rc, js, err, bl, None,
       extra={'mapper_equal_dry': m_eq, 'hand_equal_dry_except_label': h_eq}, ok_override=(rc == 0 and m_eq == 9 and h_eq == 20))

# ---------------------------------------------------------------- F1: PR-SF1 MUST_FAIL (final mode)
rc, js, err, bl = run_main(['final', '--config', V002_LOOKALIKE[0], '--config-sha', V002_LOOKALIKE[1], '--seal', w['seal']['path'],
                            '--seal-sha', w['seal']['sha256'], '--adoption-policy', w['policy']['path'], '--adoption-policy-sha',
                            w['policy']['sha256'], '--outdir', os.path.join(RUN, 'out_F1_X01'), '--utc', UTC])
record('F1_X01_V002_OWN_SYNTHETIC_C1_LOOKALIKE', 'PR-SF1', 'X01 (1757f2ce in final mode)', 'PIN_MALFORMED', rc, js, err, bl, 'out_F1_X01')
with open(w['c1']['path'], 'rb') as f:
    c1raw = f.read()
INSIDE = xwrite(os.path.join(RUN, 'SYNTHETIC_C1_INSIDE_PRODUCER_FOLDER.json'), c1raw)
rc, js, err, bl = run_main(['final', '--config', INSIDE['path'], '--config-sha', INSIDE['sha256'], '--seal', w['seal']['path'], '--seal-sha',
                            w['seal']['sha256'], '--adoption-policy', w['policy']['path'], '--adoption-policy-sha', w['policy']['sha256'],
                            '--outdir', os.path.join(RUN, 'out_F1_X03'), '--utc', UTC])
record('F1_X03_CONFIG_INSIDE_PRODUCER_FOLDER', 'PR-SF1', 'X02/X03', 'SYNTHETIC_INPUT_REFUSED_IN_FINAL_MODE', rc, js, err, bl, 'out_F1_X03',
       extra={'reason_names_inside': 'inputs inside the producer folder' in (js.get('reason') or '')})
cases_final(F1_CASES, 'PR-SF1')
rc, js, err, bl = run_main(['final', '--config', w['c1']['path'], '--config-sha', w['c1']['sha256'], '--seal', w['seal']['path'], '--seal-sha',
                            w['seal']['sha256'], '--adoption-policy', POLICY_R7[0], '--adoption-policy-sha', POLICY_R7[1],
                            '--outdir', os.path.join(RUN, 'out_F1_POLICY_R7'), '--utc', UTC])
record('F1_POLICY_R7_OF_RECORD_EMPTY_ALLOWLIST', 'PR-SF1', 'R-A2 (real policy r7 7c726fa2)', 'REVIEWED_SEAL_TUPLE_PENDING', rc, js, err, bl, 'out_F1_POLICY_R7')
for cid, extra_args, expect, c3 in (
        ('F1_F10_UNKNOWN_CASE', ['--cases', 'TAIL_REANCHOR,NOT_A_CASE'], 'UNKNOWN_CASE', 'F10'),
        ('F1_REGISTRY_OVERRIDE_IN_FINAL', ['--registry', W3_REG['path'], '--registry-sha', W3_REG['sha256']], 'FINAL_REGISTRY_OVERRIDE_REFUSED', 'final registry override')):
    rc, js, err, bl = run_main(final_argv(w, 'out_' + cid, extra_args))
    record(cid, 'PR-SF1', c3, expect, rc, js, err, bl, 'out_' + cid)
for cid, utc, expect, c3 in (('F1_A10_UTC_ARBITRARY', 'NOT A DATE; arbitrary operator text', 'UTC_FORMAT', 'A10'),
                             ('F1_UTC_STALE', '2026-10-01T00:00:00Z', 'UTC_NOT_CURRENT', 'A10')):
    argv = final_argv(w, 'out_' + cid)
    argv[argv.index('--utc') + 1] = utc
    rc, js, err, bl = run_main(argv)
    record(cid, 'PR-SF1', c3, expect, rc, js, err, bl, 'out_' + cid)
rc, js, err, bl = run_main(['provisional', '--config', R9[0], '--config-sha', R9[1], '--seal', w['seal']['path'], '--seal-sha', w['seal']['sha256'],
                            '--outdir', os.path.join(RUN, 'out_F1_PROV_WITH_SEAL'), '--utc', UTC])
record('F1_PROVISIONAL_TAKES_NO_SEAL', 'PR-SF1 (named modes)', 'X02', 'PROVISIONAL_TAKES_NO_SEAL', rc, js, err, bl, 'out_F1_PROV_WITH_SEAL')

# B05: config fields the construction never reads (ngc3198_slots, observation_region) change no spec byte (provisional mode)
cfg_b05 = copy.deepcopy(r9)
cfg_b05['ngc3198_slots'] = {'inclination_deg': 71.5, 'distance_Mpc': 13.8}
cfg_b05['observation_region'] = {'rows': [[0.5, 10.1, 1.2]], 'synthetic': True}
B05 = xwrite(os.path.join(RUN, 'SYNTHETIC_CONFIG_B05.json'), cfg_b05)
rc, js, err, bl = run_main(['provisional', '--config', B05['path'], '--config-sha', B05['sha256'], '--outdir', os.path.join(RUN, 'out_F1_B05'), '--utc', UTC])
sd = os.path.join(RUN, 'out_F1_B05', 'specs')
same5 = os.path.isdir(sd) and sorted(os.listdir(sd)) == sorted(n + '.json' for n in spec5) and all(
    open(os.path.join(sd, n + '.json'), 'rb').read() == v for n, v in spec5.items())
no_obs = not any('observation' in x['path'].casefold() for x in P2.READER.log())
record('F1_B05_UNREAD_CONFIG_FIELDS_CHANGE_NO_SPEC_BYTE', 'PR-SF1', 'B05', 'specs equal S5; observation region never read', rc, js, err, bl, None,
       extra={'specs_equal_S5': same5, 'observation_region_never_read': no_obs}, ok_override=(rc == 0 and same5 and no_obs))
# ---------------------------------------------------------------- F2: PR-SF2 MUST_FAIL (no refusal after the first write)
cases_final(F2W, 'PR-SF2')
orig_probe = P2.PROBE_REC
for cid, val, expect, c3 in (('F2_S_PROBE_PIN_MISMATCH_BEFORE_WRITE', (orig_probe[0], '4' * 64), 'PIN_MISMATCH', 'S_PROBE / T2 / T3'),
                             ('F2_T4_PROBE_FILE_ABSENT_TYPED', (orig_probe[0] + '.absent', orig_probe[1]), 'PIN_UNREADABLE', 'T4')):
    P2.PROBE_REC = val
    try:
        rc, js, err, bl = run_main(['provisional', '--config', R9[0], '--config-sha', R9[1], '--outdir', os.path.join(RUN, 'out_' + cid), '--utc', UTC])
    finally:
        P2.PROBE_REC = orig_probe
    record(cid, 'PR-SF2', c3, expect, rc, js, err, bl, 'out_' + cid)
orig_strip, orig_xwrite, orig_readback, orig_statvfs = P2.strip, P2._xwrite, P2._readback, os.statvfs
prov_argv = lambda name: ['provisional', '--config', R9[0], '--config-sha', R9[1], '--outdir', os.path.join(RUN, name), '--utc', UTC]
for cid, val in (('F2_FORCED_INF_IN_MANIFEST', float('inf')), ('F2_FORCED_NAN_IN_MANIFEST', float('nan'))):
    P2.strip = lambda r, v=val: dict(orig_strip(r), forced_nonfinite=v)
    try:
        rc, js, err, bl = run_main(prov_argv('out_' + cid))
    finally:
        P2.strip = orig_strip
    record(cid, 'PR-SF2', 'D04/D05 (forced in memory)', 'MANIFEST_NOT_SERIALIZABLE', rc, js, err, bl, 'out_' + cid)
calls = []


def failing_writer(k):
    def wr(path, data):
        calls.append(path)
        if len(calls) == k:
            raise OSError(28, 'No space left on device (injected by the test)')
        return orig_xwrite(path, data)
    return wr


for cid, k in (('F2_WRITE_ERROR_FIRST_SPEC', 1), ('F2_WRITE_ERROR_MIDDLE_SPEC', 15), ('F2_WRITE_ERROR_AT_MANIFEST', 30)):
    calls.clear()
    P2._xwrite = failing_writer(k)
    try:
        rc, js, err, bl = run_main(prov_argv('out_' + cid))
    finally:
        P2._xwrite = orig_xwrite
    od = os.path.join(RUN, 'out_' + cid)
    fm = os.path.join(od, P2.MANIFEST_FAILED)
    fdoc = rjson(fm) if os.path.exists(fm) else {}
    listed = fdoc.get('written_before_failure', [])
    on_disk = sorted(os.listdir(os.path.join(od, 'specs'))) if os.path.isdir(os.path.join(od, 'specs')) else []
    listed_ok = sorted(os.path.basename(x['path']) for x in listed if '/specs/' in x['path']) == on_disk and all(
        H(open(x['path'], 'rb').read()) == x['sha256'] for x in listed)
    no_manifest = not os.path.exists(os.path.join(od, P2.MANIFEST_PROV)) and not os.path.exists(os.path.join(od, P2.MANIFEST_FINAL))
    ok = (rc == 5 and js.get('status') == 'WRITE_FAILED' and no_manifest and fdoc.get('status') == 'WRITE_FAILED_NOT_FOR_BINDING' and
          fdoc.get('binder_pins') == {} and listed_ok and len(on_disk) == min(k - 1, 29) and err == '')
    record(cid, 'PR-SF2', 'write error (task)', 'WRITE_FAILED + failure manifest listing every written spec', rc, js, err, bl, None,
           extra={'specs_on_disk': len(on_disk), 'failure_manifest_lists_them_with_shas': listed_ok, 'no_final_or_provisional_manifest': no_manifest},
           ok_override=ok)
cnt = [0]


def bad_readback(path):
    cnt[0] += 1
    raw = orig_readback(path)
    return raw + b' ' if cnt[0] == 5 else raw


P2._readback = bad_readback
try:
    rc, js, err, bl = run_main(prov_argv('out_F2_READBACK_MISMATCH'))
finally:
    P2._readback = orig_readback
od = os.path.join(RUN, 'out_F2_READBACK_MISMATCH')
fdoc = rjson(os.path.join(od, P2.MANIFEST_FAILED)) if os.path.exists(os.path.join(od, P2.MANIFEST_FAILED)) else {}
record('F2_S_READBACK_MISMATCH', 'PR-SF2', 'S_READBACK', 'WRITE_FAILED', rc, js, err, bl, None,
       extra={'failure_manifest_listed': len(fdoc.get('written_before_failure', []))},
       ok_override=(rc == 5 and len(fdoc.get('written_before_failure', [])) == 5 and not os.path.exists(os.path.join(od, P2.MANIFEST_PROV))))
os.mkdir(os.path.join(RUN, 'out_F2_PREEXISTING_DIR'))
xwrite(os.path.join(RUN, 'out_F2_PREEXISTING_FILE'), b'pre-existing\n')
os.symlink(os.path.join(RUN, 'nonexistent_target_dir'), os.path.join(RUN, 'out_F2_DANGLING_LINK'))
os.mkdir(os.path.join(RUN, 'real_inside'))
os.symlink(os.path.join(RUN, 'real_inside'), os.path.join(RUN, 'linkparent'))
for cid, outdir, expect, c3 in (
        ('F2_F01_OUTDIR_EXISTS_DIR', os.path.join(RUN, 'out_F2_PREEXISTING_DIR'), 'OUTDIR_EXISTS', 'F01/T5'),
        ('F2_F02_OUTDIR_EXISTS_FILE', os.path.join(RUN, 'out_F2_PREEXISTING_FILE'), 'OUTDIR_EXISTS', 'F02'),
        ('F2_F03_OUTDIR_DANGLING_LINK', os.path.join(RUN, 'out_F2_DANGLING_LINK'), 'OUTDIR_EXISTS', 'F03'),
        ('F2_F07_OUTDIR_IN_TOOLS', os.path.join(RUN, 'tools', 'out_F07'), 'OUTDIR_NOT_A_DIRECT_CHILD_OF_THE_PRODUCER_FOLDER', 'F07'),
        ('F2_F06_OUTDIR_OUTSIDE', os.path.join(BASE, 'escape_F06'), 'OUTDIR_NOT_A_DIRECT_CHILD_OF_THE_PRODUCER_FOLDER', 'F06'),
        ('F2_F04_OUTDIR_SYMLINK_PARENT', os.path.join(RUN, 'linkparent', 'out_F04'), 'OUTDIR_NOT_A_DIRECT_CHILD_OF_THE_PRODUCER_FOLDER', 'F04/F05')):
    before = sorted(os.listdir(RUN))
    rc, js, err, bl = run_main(['provisional', '--config', R9[0], '--config-sha', R9[1], '--outdir', outdir, '--utc', UTC])
    after = sorted(os.listdir(RUN))
    unchanged = before == after and (not os.path.isdir(outdir) or os.path.islink(outdir) or os.listdir(outdir) == []) and \
        not os.path.exists(os.path.join(RUN, 'nonexistent_target_dir')) and os.listdir(os.path.join(RUN, 'real_inside')) == [] and \
        not os.path.lexists(os.path.join(BASE, 'escape_F06'))
    record(cid, 'PR-SF2', c3, expect, rc, js, err, bl, None, extra={'nothing_created_or_changed': unchanged},
           ok_override=(rc == 3 and js.get('code') == expect and unchanged))


class _FakeStat:
    f_bavail = 1
    f_frsize = 4096


os.statvfs = lambda p: _FakeStat()
try:
    rc, js, err, bl = run_main(prov_argv('out_F2_NO_FREE_SPACE'))
finally:
    os.statvfs = orig_statvfs
record('F2_NO_FREE_SPACE_REFUSED_BEFORE_WRITE', 'PR-SF2', 'disk (R-D17 class)', 'INSUFFICIENT_FREE_SPACE', rc, js, err, bl, 'out_F2_NO_FREE_SPACE')
order, reads_at_first_write = [], []


def logging_writer(path, data):
    if not order:
        reads_at_first_write.append(len(P2.READER.log()))
    order.append(os.path.basename(path))
    return orig_xwrite(path, data)


P2._xwrite = logging_writer
try:
    rc, js, err, bl = run_main(prov_argv('out_F2_ORDER'))
finally:
    P2._xwrite = orig_xwrite
reads_end = len(P2.READER.log())
record('F2_WRITE_ORDER_MANIFEST_LAST_NO_READ_AFTER_FIRST_WRITE', 'PR-SF2', 'S0_CONTROL opens order', 'manifest last; 0 reads after the first write',
       rc, js, err, bl, None, extra={'writes': len(order), 'last_write': order[-1] if order else None,
                                     'reads_at_first_write': reads_at_first_write[:1], 'reads_at_end': reads_end},
       ok_override=(rc == 0 and len(order) == 30 and order[-1] == P2.MANIFEST_PROV and reads_at_first_write == [reads_end]))
import ast as _ast  # noqa: E402
src_tree = _ast.parse(open(os.path.join(RUN, 'tools', PROD_NAME), 'rb').read())
fn = {n.name: n for n in src_tree.body if isinstance(n, _ast.FunctionDef)}


def call_lines(f, name):
    return [n.lineno for n in _ast.walk(f) if isinstance(n, _ast.Call) and getattr(n.func, 'id', getattr(n.func, 'attr', None)) == name]


pw = fn['_plan_and_write']
static = {'json_bytes_before_write': max(call_lines(pw, 'json_bytes')) < min(call_lines(pw, 'write_outputs')),
          'preflight_before_write': max(call_lines(pw, '_outdir_preflight')) < min(call_lines(pw, 'write_outputs')),
          'final_and_provisional_share_writer': bool(call_lines(fn['cmd_final'], '_plan_and_write')) and bool(call_lines(fn['cmd_provisional'], '_plan_and_write')),
          'no_write_call_elsewhere': sorted(k for k, f in fn.items() if call_lines(f, '_xwrite')) == ['write_outputs']}
record('F2_STATIC_ONE_WRITER_AFTER_SERIALIZATION', 'PR-SF2 (FORMAL, AST of the copy)', 'final mode uses the same writer', 'all true', 0,
       {'status': 'TESTED'}, '', [], None, extra=static, ok_override=all(static.values()))

# ---------------------------------------------------------------- SF-R1: MUST_FAIL, write failures after a file exists (FIX stage)
# The REFUTE stage's OS-layer injections, ported from refute_s2_write_positions_c4r.py (91a61d81) and
# refute_s2b_corrupt_write_c4r.py (97dda3f6): os.mkdir, os.open(O_CREAT), os.write, os.fsync and os.close are replaced for one
# run at a time, in provisional mode on the r9 config. Provisional and final mode share the one writer
# (F2_STATIC_ONE_WRITER_AFTER_SERIALIZATION), so final mode is covered FORMALLY; no FINAL-labelled byte is ever written here.
# The claims tested are the corrected ones (SPEC_HANDOFF_C4V003 section 5 step 5, DELTA row 2 and SF-R1 row):
#   exit 5 and status WRITE_FAILED, nothing escapes main (KeyboardInterrupt included), stderr empty, no fence block;
#   the failure record is on stdout, and it lists exactly the files on disk with the sha and size of their bytes ON DISK;
#   a spec whose bytes differ from the intended bytes (independently rebuilt here) is DIFFERS_FROM_INTENDED, an equal one
#   COMPLETE_EQUALS_INTENDED; every manifest on disk is named in manifests_present_not_for_binding; every file on disk was
#   recorded in attempted_in_order before it was created; the WRITE_FAILED manifest on disk equals the stdout record wherever
#   the disk allowed that last write, and is absent only where its creation was refused (W14) or no folder exists (W12).
SF_REAL = {'open': os.open, 'write': os.write, 'fsync': os.fsync, 'close': os.close, 'mkdir': os.mkdir}
reset()
SF_EXP = {r['case']: r['raw'] for r in P2.World(cfg_r9, pin_r9, P2.NOTE_PROVMODE).build_all()}     # intended spec bytes
assert len(SF_EXP) == 29


class SFInj:
    def __init__(self, outdir, kind=None, k=None, fail_failed_manifest=False):
        self.outdir, self.kind, self.k, self.fffm = outdir, kind, k, fail_failed_manifest
        self.created, self.cur, self.mk, self.events = 0, {}, 0, []

    def _under(self, path):
        try:
            p = os.fsdecode(path)
        except TypeError:
            return None
        return p if (p == self.outdir or p.startswith(self.outdir + os.sep)) else None

    def open(self, path, flags, mode=0o777, *, dir_fd=None):
        p = self._under(path) if not isinstance(path, int) else None
        if p is not None and flags & os.O_CREAT:
            if self.fffm and os.path.basename(p) == P2.MANIFEST_FAILED:
                self.events.append('failure-manifest create refused (injected)')
                raise OSError(5, 'Input/output error (injected: failure manifest)')
            self.created += 1
            idx = self.created
            if self.kind == 'create' and idx == self.k:
                self.events.append('create %d refused before creation' % idx)
                raise OSError(28, 'No space left on device (injected before creation)')
            fd = SF_REAL['open'](path, flags, mode)
            self.cur[fd] = (idx, os.path.basename(p))
            return fd
        if dir_fd is None:
            return SF_REAL['open'](path, flags, mode)
        return SF_REAL['open'](path, flags, mode, dir_fd=dir_fd)

    def write(self, fd, data):
        idx = self.cur.get(fd, (None,))[0]
        if idx is not None and idx == self.k and self.kind == 'write_corrupt':
            b = bytearray(bytes(data))
            b[0] ^= 0x01
            SF_REAL['write'](fd, bytes(b))
            self.events.append('write_corrupt at file %d: first byte flipped on disk, full length reported' % idx)
            return len(b)
        if idx is not None and idx == self.k and self.kind in ('write_partial', 'write_interrupt'):
            b = bytes(data)
            SF_REAL['write'](fd, b[:max(1, len(b) // 2)])
            self.events.append('%s at file %d after %d of %d bytes' % (self.kind, idx, max(1, len(b) // 2), len(b)))
            if self.kind == 'write_interrupt':
                raise KeyboardInterrupt('injected')
            raise OSError(28, 'No space left on device (injected mid-write)')
        return SF_REAL['write'](fd, data)

    def fsync(self, fd):
        idx = self.cur.get(fd, (None,))[0]
        if idx is not None and idx == self.k and self.kind == 'fsync':
            self.events.append('fsync %d failed after a complete write' % idx)
            raise OSError(5, 'Input/output error (injected at fsync)')
        return SF_REAL['fsync'](fd)

    def close(self, fd):
        idx = self.cur.pop(fd, (None,))[0]
        SF_REAL['close'](fd)
        if idx is not None and idx == self.k and self.kind == 'close':
            self.events.append('close %d failed after write and fsync' % idx)
            raise OSError(5, 'Input/output error (injected at close)')

    def mkdir(self, path, mode=0o777, *, dir_fd=None):
        p = self._under(path)
        if p is not None:
            self.mk += 1
            if self.kind == 'mkdir' and self.mk == self.k:
                self.events.append('mkdir %d refused' % self.mk)
                raise OSError(28, 'No space left on device (injected at mkdir)')
        return SF_REAL['mkdir'](path, mode) if dir_fd is None else SF_REAL['mkdir'](path, mode, dir_fd=dir_fd)


def sf_disk(od):                          # the test's own view of the disk: every file under the staging folder, read here
    out = {}
    for dp, dn, fs in os.walk(od):
        for f in fs:
            p = os.path.join(dp, f)
            with open(p, 'rb') as fh:
                out[p] = fh.read()
    return out


def sf_run(wid, what, kind=None, k=None, fffm=False, readback_bad_at=None, manifest_state=None):
    name = 'out_SFR1_' + wid
    od = os.path.join(RUN, name)
    inj = SFInj(od, kind, k, fffm)
    cnt = [0]

    def rb(path):
        cnt[0] += 1
        raw = orig_readback(path)
        return raw + b' ' if readback_bad_at is not None and cnt[0] == readback_bad_at else raw
    rc, js, err, bl, exc_name = None, {}, '', [], None
    b0 = [len(f.BLOCKED) for f in FENCES]
    os.open, os.write, os.fsync, os.close, os.mkdir = inj.open, inj.write, inj.fsync, inj.close, inj.mkdir
    P2._readback = rb
    try:
        rc, js, err, bl = run_main(prov_argv(name))
    except BaseException as exc:          # an escape from main breaks the claim (W15 on the BUILD bytes); recorded, never hidden
        exc_name = type(exc).__name__
        bl = [b for f, n in zip(FENCES, b0) for b in f.BLOCKED[n:]]
    finally:
        os.open, os.write, os.fsync, os.close, os.mkdir = SF_REAL['open'], SF_REAL['write'], SF_REAL['fsync'], SF_REAL['close'], SF_REAL['mkdir']
        P2._readback = orig_readback
    disk = sf_disk(od) if os.path.isdir(od) else {}
    fm_raw = disk.pop(os.path.join(od, P2.MANIFEST_FAILED), None)
    try:
        fdoc = P2.strict_json(fm_raw, 'failure manifest') if fm_raw is not None else None
    except P2.Refuse as exc:
        fdoc = 'UNPARSABLE ' + exc.code
    srec = js.get('failure_record') if isinstance(js, dict) else None
    rec_ = srec if isinstance(srec, dict) else {}
    listed = {x.get('path'): x for x in rec_.get('written_before_failure', []) if isinstance(x, dict)}
    spec_dir = os.path.join(od, 'specs') + os.sep
    manifests_on_disk = sorted(p for p in disk if os.path.dirname(p) == od and os.path.basename(p) in (P2.MANIFEST_PROV, P2.MANIFEST_FINAL))
    c = {}
    if kind is None:                      # the control: a clean run
        c['exit_0_provisional'] = rc == 0 and js.get('status') == 'PROVISIONAL_NOT_LAUNCH_SPECS'
        c['29_specs_equal_intended'] = sorted(p for p in disk if p.startswith(spec_dir)) == sorted(spec_dir + n + '.json' for n in SF_EXP) and all(
            disk[spec_dir + n + '.json'] == b for n, b in SF_EXP.items())
        c['provisional_manifest_and_no_failure_manifest'] = manifests_on_disk == [os.path.join(od, P2.MANIFEST_PROV)] and fm_raw is None
    else:
        c['exit_5_write_failed'] = rc == 5 and js.get('status') == 'WRITE_FAILED' and js.get('code') == 'WRITE_FAILED'
        c['nothing_escapes_main_stderr_empty'] = exc_name is None and err == ''
        c['failure_record_on_stdout'] = rec_.get('status') == 'WRITE_FAILED_NOT_FOR_BINDING' and rec_.get('binder_pins') == {}
        c['stdout_record_lists_exactly_the_files_on_disk_with_on_disk_shas'] = bool(srec) and set(listed) == set(disk) and all(
            listed[p].get('sha256') == H(b) and listed[p].get('bytes') == len(b) for p, b in disk.items())
        if not (kind == 'mkdir' and k == 1) and not fffm:      # the REFUTE stage's own claim, read from the file on disk
            flisted = {x.get('path'): x for x in (fdoc.get('written_before_failure', []) if isinstance(fdoc, dict) else [])
                       if isinstance(x, dict)}
            c['failure_manifest_file_lists_exactly_the_files_on_disk_with_on_disk_shas'] = isinstance(fdoc, dict) and set(flisted) == set(disk) and all(
                flisted[p].get('sha256') == H(b) for p, b in disk.items())
        c['spec_states_against_independent_intended_bytes'] = all(
            listed[p].get('state') == ('COMPLETE_EQUALS_INTENDED' if b == SF_EXP.get(os.path.basename(p)[:-5]) else 'DIFFERS_FROM_INTENDED')
            for p, b in disk.items() if p.startswith(spec_dir) and p in listed)
        c['manifests_on_disk_named_not_for_binding'] = sorted(x.get('path') for x in rec_.get('manifests_present_not_for_binding', [])) == manifests_on_disk
        if manifest_state is not None:
            m = listed.get(os.path.join(od, P2.MANIFEST_PROV), {})
            c['manifest_state_' + manifest_state] = m.get('state') == manifest_state and (
                (m.get('sha256') == m.get('intended_sha256')) == (manifest_state == 'COMPLETE_EQUALS_INTENDED'))
        c['every_file_on_disk_recorded_before_creation'] = all(p in rec_.get('attempted_in_order', []) for p in disk)
        if kind == 'mkdir' and k == 1:
            c['no_folder_created'] = not os.path.lexists(od)
            c['stdout_record_says_no_folder'] = rec_.get('staging_folder_created') is False
        elif fffm:
            c['failure_manifest_absent_record_on_stdout_only'] = fm_raw is None and 'stdout only' in (js.get('reason') or '')
            c['no_final_or_provisional_manifest_so_not_bindable'] = manifests_on_disk == []
        else:
            c['failure_manifest_on_disk_equals_stdout_record'] = fdoc is not None and fdoc == srec
        if kind == 'write_interrupt':
            c['interrupt_recorded'] = rec_.get('interrupted') is True
    ok = all(c.values()) and not bl
    record('SFR1_' + wid, 'SF-R1', 'REFUTE ' + wid.split('_')[0], 'corrected write-failure claims', rc if rc is not None else -1,
           js if isinstance(js, dict) else {}, err, bl, None,
           extra={'what': what, 'injection': {'kind': kind, 'k': k, 'fail_failed_manifest': fffm, 'readback_bad_at': readback_bad_at},
                  'events': inj.events, 'exception_escaped_main': exc_name, 'files_on_disk': len(disk),
                  'failure_manifest_on_disk': fm_raw is not None, 'claims': c,
                  'states': {os.path.relpath(p, od): v.get('state') for p, v in sorted(listed.items())} if len(listed) <= 6 else
                  {'n': len(listed), 'not_complete': sorted(os.path.relpath(p, od) for p, v in listed.items() if v.get('state') != 'COMPLETE_EQUALS_INTENDED')}},
           ok_override=ok)


sf_run('W00_CONTROL', 'no injection: 29 specs + PROVISIONAL manifest, exit 0')
sf_run('W01_CREATE_1', 'first spec refused before creation (the BUILD class)', 'create', 1)
sf_run('W02_CREATE_15', '15th spec refused before creation (the BUILD class)', 'create', 15)
sf_run('W03_CREATE_30', 'manifest refused before creation (the BUILD class)', 'create', 30)
sf_run('W04_WRITE_PARTIAL_1', 'first spec created, half written, then ENOSPC', 'write_partial', 1)
sf_run('W05_WRITE_PARTIAL_15', '15th spec created, half written, then ENOSPC', 'write_partial', 15)
sf_run('W06_WRITE_PARTIAL_30', 'manifest created, half written, then ENOSPC', 'write_partial', 30, manifest_state='DIFFERS_FROM_INTENDED')
sf_run('W07_FSYNC_1', 'first spec fully written, fsync EIO', 'fsync', 1)
sf_run('W08_FSYNC_15', '15th spec fully written, fsync EIO', 'fsync', 15)
sf_run('W09_FSYNC_30', 'manifest fully written, fsync EIO', 'fsync', 30, manifest_state='COMPLETE_EQUALS_INTENDED')
sf_run('W10_CLOSE_30', 'manifest fully written and fsynced, close EIO', 'close', 30, manifest_state='COMPLETE_EQUALS_INTENDED')
sf_run('W11_READBACK_MANIFEST', 'manifest written; its read-back differs', 'readback', None, readback_bad_at=30,
       manifest_state='COMPLETE_EQUALS_INTENDED')
sf_run('W12_MKDIR_OUTDIR', 'mkdir of the staging folder fails', 'mkdir', 1)
sf_run('W13_MKDIR_SPECS', 'mkdir of specs/ fails after the staging folder exists', 'mkdir', 2)
sf_run('W14_PARTIAL_15_AND_FAILURE_MANIFEST_FAILS', '15th spec half written, and the failure manifest cannot be created', 'write_partial', 15,
       fffm=True)
sf_run('W15_INTERRUPT_15', 'KeyboardInterrupt (a BaseException) mid-write of the 15th spec', 'write_interrupt', 15)
sf_run('W16_WRITE_CORRUPT_5', '5th spec written with one flipped byte (full length reported); its read-back differs', 'write_corrupt', 5)
sf_run('W17_WRITE_CORRUPT_30', 'manifest written with one flipped byte; its read-back differs', 'write_corrupt', 30,
       manifest_state='DIFFERS_FROM_INTENDED')
wo = fn.get('write_outputs')
handlers = [h for h in _ast.walk(wo) if isinstance(h, _ast.ExceptHandler)] if wo is not None else []
mh = [h for h in _ast.walk(fn['main']) if isinstance(h, _ast.ExceptHandler)]
sf_static = {'write_outputs_catches_BaseException': any(isinstance(h.type, _ast.Name) and h.type.id == 'BaseException' for h in handlers),
             'scan_by_listdir': '_scan_staging' in fn and bool(call_lines(fn['_scan_staging'], 'listdir')),
             'write_outputs_scans_on_failure': bool(call_lines(wo, '_scan_staging')) if wo is not None else False,
             'main_types_KeyboardInterrupt': any(isinstance(h.type, _ast.Name) and h.type.id == 'KeyboardInterrupt' for h in mh),
             'still_one_writer': sorted(k for k, f in fn.items() if call_lines(f, '_xwrite')) == ['write_outputs']}
record('SFR1_STATIC_BASEEXCEPTION_SCAN_ONE_WRITER', 'SF-R1 (FORMAL, AST of the copy)', 'REFUTE SF-R1 fix list', 'all true', 0,
       {'status': 'TESTED'}, '', [], None, extra=sf_static, ok_override=all(sf_static.values()))

# ---------------------------------------------------------------- F3: PR-SF3 MUST_FAIL (literal-first fence, read once, caps)
SELFTEST_BLOCKS = 0
for label, fe in (('phase_A_copy', FENCE_A), ('phase_B_copy', F2_)):
    b_sel0 = sum(len(f.BLOCKED) for f in FENCES)
    st = fe.selftest()
    SELFTEST_BLOCKS += sum(len(f.BLOCKED) for f in FENCES) - b_sel0
    record('F3_FENCE_SELFTEST_' + label, 'PR-SF3', '/.vol, N3198, UGC5572, DDO154 aliases, ..', '29/29 refused, 0 protected probes', 0,
           {'status': 'TESTED'}, '', [], None,
           extra={'trials': len(st), 'refused': sum(1 for x in st if x[1]), 'protected_probes': sum(len(x[2]) for x in st)},
           ok_override=(len(st) == 29 and all(x[1] for x in st) and not any(x[2] for x in st)))
def traced(fn):
    p0 = [len(f.PROBE_LOG) for f in FENCES]
    for f in FENCES:
        f.TRACE[0] = True
    try:
        return fn(), [x for f, n in zip(FENCES, p0) for x in f.PROBE_LOG[n:]]
    finally:
        for f in FENCES:
            f.TRACE[0] = False


for nm in sorted(PROT):
    (rc, js, err, bl), probes = traced(lambda: run_main(final_argv(WORLDS[PROT_DIR[nm]], 'out_' + PROT_DIR[nm])))
    bad = [p for _, p in probes if F2_.protected_reason(p)]
    rec = record('F3_' + nm, 'PR-SF3', nm.split('_')[0] if nm[0] in 'BG' else 'name table', 'FENCE_REFUSED', rc, js, err, bl, 'out_' + PROT_DIR[nm],
                 extra={'protected_paths_probed': bad, 'probes': len(probes), 'slot_ref_basename': PROT[nm], 'world': PROT_DIR[nm]})
    rec['passed'] = rec['passed'] and not bad
for nm in ('F3_VOL_VERDICT', 'F3_VOL_DOTDOT_VERDICT'):
    (rc, js, err, bl), probes = traced(lambda: run_main(final_argv(WORLDS[nm], 'out_' + nm)))
    bad = [p for _, p in probes if '.vol' in p]
    rec = record(nm, 'PR-SF3', 'F08 (/.vol)', 'FENCE_REFUSED', rc, js, err, bl, 'out_' + nm, extra={'vol_probes': bad})
    rec['passed'] = rec['passed'] and not bad
for cid, fn_ in (('F3_C04_VOL_WRITE_OPEN', lambda: open('/.vol/16777220/2/out_probe', 'x')),
                 ('F3_C05_VOL_MKDIR', lambda: os.mkdir('/.vol/16777220/2/out_probe_dir'))):
    def probe(fn_=fn_):
        try:
            fn_()
            return 'ALLOWED'
        except PermissionError as exc:
            return 'FENCE_REFUSED' if str(exc).startswith('FENCE_C4V003') else 'OTHER_PERMISSION'
        except OSError as exc:
            return 'NOT_REFUSED_BY_FENCE_' + type(exc).__name__
    b0 = [len(f.BLOCKED) for f in FENCES]
    got, probes = traced(probe)
    bl = [b for f, n in zip(FENCES, b0) for b in f.BLOCKED[n:]]
    record(cid, 'PR-SF3', cid.split('_')[1], 'FENCE_REFUSED', 0, {'status': 'TESTED', 'code': got}, '', bl, None,
           extra={'vol_probes': [p for _, p in probes if '.vol' in p], 'fence_blocked_new_count': len(bl)},
           ok_override=(got == 'FENCE_REFUSED' and not [p for _, p in probes if '.vol' in p]))
    RESULTS[-1]['expected'] = 'FENCE_REFUSED'
rc, js, err, bl = run_main(final_argv(WORLDS['F3_BIG_SLOT_CERT'], 'out_F3_BIG'))
record('F3_D01_BIG_CERT_REFUSED_BEFORE_READ', 'PR-SF3', 'D01/D02 (full read before sha)', 'INPUT_TOO_LARGE', rc, js, err, bl, 'out_F3_BIG')
reset()
reads = []
orig_read = os.read
os.read = lambda fd, n: reads.append(n) or orig_read(fd, n)
try:
    try:
        P2.READER.raw(SMALL, 'small file under a 1 KiB cap', cap=1024)
        got = 'ACCEPTED'
    except P2.Refuse as exc:
        got = exc.code
finally:
    os.read = orig_read
record('F3_SIZE_CAP_BY_FSTAT_ZERO_BYTES_READ', 'PR-SF3', 'D01 (read before sha)', 'INPUT_TOO_LARGE', 0, {'status': 'TESTED', 'code': got}, '', [], None,
       extra={'os_read_calls': len(reads)}, ok_override=(got == 'INPUT_TOO_LARGE' and not reads))
HL = os.path.join(RUN, 'innocent_hardlink.json')
os.link(HLSRC['path'], HL)
reset()
try:
    P2.READER.raw({'path': HL, 'sha256': HLSRC['sha256']}, 'hard link')
    got = 'ACCEPTED'
except P2.Refuse as exc:
    got = exc.code
record('F3_G04_HARD_LINK_REFUSED', 'PR-SF3', 'G04/G05 (hard links)', 'INPUT_HARD_LINKED', 0, {'status': 'TESTED', 'code': got}, '', [], None,
       ok_override=(got == 'INPUT_HARD_LINKED'))
reset()
try:
    P2.READER.raw({'path': HLSRC['path'], 'sha256': HLSRC['sha256']}, 'hard-link source')
    got = 'ACCEPTED'
except P2.Refuse as exc:
    got = exc.code
record('F3_G04_HARD_LINK_SOURCE_ALSO_REFUSED', 'PR-SF3', 'G04/G05', 'INPUT_HARD_LINKED', 0, {'status': 'TESTED', 'code': got}, '', [], None,
       ok_override=(got == 'INPUT_HARD_LINKED'))
r1 = P2.Reader()
P2.READER = r1
try:
    r1.raw(SMALL, 'pin once')
    r1.raw({'path': SMALL['path'], 'sha256': 'b' * 64}, 'pin twice with another sha')
    got = 'ACCEPTED'
except P2.Refuse as exc:
    got = exc.code
record('F3_SAME_FILE_TWO_SHAS_REFUSED', 'PR-SF3 (read once)', 'read once', 'PIN_CONFLICT', 0, {'status': 'TESTED', 'code': got}, '', [], None,
       ok_override=(got == 'PIN_CONFLICT'))

# ---------------------------------------------------------------- F5: PR-SF5 MUST_FAIL (strict JSON, typed codes)
cases_final(F5W, 'PR-SF5')


def guard_decode_replica(data):           # guard007 42bf0ce9 L62-71 (replica; the guard itself is never run)
    def pairs(items):
        d = {}
        for k, v in items:
            if k in d:
                raise ValueError('DUPLICATE_JSON_KEY')
            d[k] = v
        return d

    def fin(s):
        v = float(s)
        if not math.isfinite(v):
            raise ValueError('NONFINITE_JSON')
        return v

    def const(s):
        raise ValueError('NONFINITE_JSON')
    return json.loads(data, object_pairs_hook=pairs, parse_float=fin, parse_constant=const)


forms = {'dup': b'{"a": 1, "a": 2}', 'nan': b'{"a": NaN}', 'inf': b'{"a": Infinity}', 'ninf': b'{"a": -Infinity}', '1e999': b'{"a": 1e999}',
         'int5001': b'{"a": 1' + b'0' * 5000 + b'}', 'int65': b'{"a": 1' + b'0' * 64 + b'}', 'int64_ok': b'{"a": 1' + b'0' * 63 + b'}',
         'deep200000': b'[' * 200000 + b']' * 200000, 'deep65': b'[' * 65 + b']' * 65, 'deep64_ok': b'[' * 64 + b']' * 64,
         'bad_utf8': b'{"a": "\xff"}', 'bom': b'\xef\xbb\xbf{"a": 1}', 'utf16': '{"a": 1}'.encode('utf-16'), 'utf32': '{"a": 1}'.encode('utf-32'),
         'utf16le_nobom': '{"a": 1}'.encode('utf-16-le'), 'nul': b'{"a": "\x00"}', 'trunc': b'{"a": ', 'ok': b'{"a": 1, "b": [1.5, "x"]}'}
parity = {}
for nm, data in forms.items():
    try:
        P2.strict_json(data, nm)
        prod = 'ACCEPT'
    except P2.Refuse as exc:
        prod = exc.code
    except Exception as exc:
        prod = 'UNTYPED_' + type(exc).__name__
    try:
        guard_decode_replica(data)
        guard = 'ACCEPT'
    except (ValueError, RecursionError) as exc:
        guard = 'REFUSE_' + type(exc).__name__
    parity[nm] = {'producer': prod, 'guard007_replica': guard}
no_diff = all(not (v['producer'] == 'ACCEPT' and v['guard007_replica'] != 'ACCEPT') for v in parity.values())
typed = all(not v['producer'].startswith('UNTYPED') for v in parity.values())
expect_ok = {'int64_ok', 'deep64_ok', 'ok'}
right = all((v['producer'] == 'ACCEPT') == (nm in expect_ok) for nm, v in parity.items())
record('F5_DECODER_UNIT_AND_GUARD007_PARITY', 'PR-SF5', 'D01-D09 + encodings', 'no form accepted by the producer that guard007 refuses',
       0, {'status': 'TESTED'}, '', [], None, extra={'forms': parity, 'no_producer_accepts_guard_refuses': no_diff, 'all_typed': typed,
                                                    'accepts_exactly_the_valid_controls': right},
       ok_override=(no_diff and typed and right))

# ---------------------------------------------------------------- summary
blocked_total = [b for f in FENCES for b in f.BLOCKED]
by_fix = {}
for r in RESULTS:
    k = r['fix'].split(' ')[0]
    d = by_fix.setdefault(k, [0, 0])
    d[0] += r['passed']
    d[1] += 1
summary = {'passed': sum(r['passed'] for r in RESULTS), 'total': len(RESULTS), 'by_fix': {k: '%d/%d' % tuple(v) for k, v in sorted(by_fix.items())},
           'failed_ids': [r['id'] for r in RESULTS if not r['passed']],
           'final_manifests_written_anywhere': sorted(os.path.join(dp, f) for dp, dn, fs in os.walk(RUN) for f in fs if f == P2.MANIFEST_FINAL),
           'fence_blocked_phase_b': len(blocked_total),
           'fence_blocks_only_in_deliberate_cases': (
               all(not r['fence_blocked_new'] for r in RESULTS if r['expected'] != 'FENCE_REFUSED') and
               len(blocked_total) == SELFTEST_BLOCKS + sum(len(r['fence_blocked_new']) for r in RESULTS if r['expected'] == 'FENCE_REFUSED')),
           'selftest_blocks': SELFTEST_BLOCKS,
           'seconds': round(time.time() - T0, 2)}
out = {'schema': 'C4_STEP4_PRODUCER_V003_TESTS', 'stage': 'FIX_SFR1 (test file = BUILD ff38c181 + the SF-R1 section)', 'utc_date_u_at_start': UTC, 'tag': TAG,
       'producer': {'path': os.path.join(TOOLS, PROD_NAME), 'sha256': PROD_SHA},
       'producer_copy_under_test': {'path': os.path.join(RUN, 'tools', PROD_NAME), 'sha256': P2SHA},
       'fence': {'sha256': P2.FENCE_SHA, 'version': F2_.VERSION}, 'phase_a': PHASE_A, 'summary': summary, 'results': RESULTS,
       'fence_blocked_phase_b': [list(b) for b in blocked_total], 'cert_root_override_for_dev_location': CERT_ROOT_OVERRIDE,
       'labels': 'TESTED = recomputed here from bytes in this fenced process; FORMAL items say so; nothing here is a launch spec'}
res = xwrite(os.path.join(RUN, 'TEST_RESULTS_C4V003.json'), out)
print(json.dumps({'summary': summary, 'results_file': res}, indent=1))
sys.exit(0 if summary['passed'] == summary['total'] else 1)

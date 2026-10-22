"""S4-R-C1 LO_ENVELOPE adapter: reviewed LO numeric record -> guard/wrapper proof (Claude3; A122; Codex1 under A115).

Modelled on adapt_eps (adapter v003 4de70486 L167-198). It re-derives custody, reads the LO
numeric record (the lo slot) by exact pin, checks scope, producers, caps, the distinct-lane cap
review and a distinct per-point LO review that binds the record bytes, RECOMPUTES the shell
table (4 -> 182 tiling, every shell max <= 0.005, sum <= 0.05, per-row ratios from
|v| R rho B1 / (4 tau)), and only then emits a PROOF_SCHEMA gate LO_ENVELOPE TESTED/PASS proof
with driver_certificate = the LO numeric record pin (wrapper r9 L148-161).

An envelope above threshold never passes: it stays BLOCKED and the reading is preserved (R2).
ROOT GATE: ROOT_LO_RULING_SHA256 is empty, so the public entry point returns BLOCKED before any
custody derivation until root rules on caps and enforcement (brief section 6 Q1-Q5, Q8-Q10;
FROM_CODEX/0674). The builder tested this adapter on synthetic records only.
This is certificate conversion, never launch authorization.
"""
import hashlib
import importlib.util
import math
import os
import sys
import types

ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
CERT = ART + '/calib_tail_readiness_cx2/certificates_per_point'
CUSTODY = (CERT + '/custody_cx2v002.py', '6810b7c3614e219f6e059208fbe59e905d01aa3a115e3c723079b579a027a377')
LO_CORE_SHA = '12d36305e09651fcb0dca0b76f85c755ff063c9d9e3ce0dd1e1baacf7b3d430e'
RESPONSE_SHA = 'a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231'
ROOT_LO_RULING_SHA256 = ()          # empty until root rules Q1-Q5, Q8-Q10 (0674)
PROOF_SCHEMA = 'UNT_CALIBRATION_POINT_PROOF_CX2V001'
LO_SCHEMA = 'UNT_POINT_LO_NUMERICAL_CX2V001'
RHO_SCHEMA = 'UNT_POINT_RHO_NUMERICAL_CX2V001'
CAP_SCHEMA = 'UNT_POINT_LO_CAPS_CX2V001'
CAP_REVIEW_SCHEMA = 'UNT_POINT_LO_CAP_REVIEW_CX2V001'
LO_REVIEW_SCHEMA = 'UNT_POINT_LO_ENVELOPE_REVIEW_C3V001'
KIND = 'PRELAUNCH_CONDITIONAL_SOURCE_ENVELOPE'
CLEAN_CORE_VERDICT = 'CONDITIONAL_NUMERICAL_EVIDENCE_REVIEW_REQUIRED'
K, SHELL_END = 4.0, 182.0                        # ceil(sqrt(2) * 128) = 182
SHELL_MAX, SUM_MAX = 0.005, 0.05                 # lo_core L171 / guard v003 L210-215
RHO_PARTITION = [[4.0, 5.0], [5.0, 6.0], [6.0, 8.0], [8.0, 12.0], [12.0, 16.0], [16.0, 32.0],
                 [32.0, 64.0], [64.0, 128.0], [128.0, 182.0]]   # producer shell_plan(unit=False) at K_big 128


def _load_exact(path, sha, name):
    if os.path.realpath(path) != path:
        raise ValueError('NONCANONICAL_MODULE_PATH: ' + path)
    with open(path, 'rb') as f:
        raw = f.read()
    if hashlib.sha256(raw).hexdigest() != sha:
        raise ValueError('MODULE_PIN_MISMATCH: ' + path)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    exec(compile(raw, path, 'exec'), mod.__dict__)
    return mod


def _real_env():
    state = {}

    def cu():
        if 'cu' not in state:
            state['cu'] = _load_exact(CUSTODY[0], CUSTODY[1], 's4rc1_lo_adapter_custody_cx2v002')
        return state['cu']

    return types.SimpleNamespace(
        derive_details=lambda spec: cu().derive_details(spec=spec),
        read_pin=lambda ref: cu().read_pin(ref),
        read_raw=lambda ref: cu().read_pin(ref, document=False),
        self_pin=lambda: cu().pin(__file__),
        root_rulings=ROOT_LO_RULING_SHA256,
        utc=lambda: __import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat())


def _num(x, name, lower=0.0):
    if type(x) not in (int, float) or not math.isfinite(x) or x < lower:
        raise ValueError('LO_INVALID_NUMBER: ' + name)
    return x


def _flag(obj, key, code):
    if obj.get(key) is not True:
        raise ValueError(code)


def _scope(obj, details, label):
    if obj.get('identity') != details['identity'] or obj.get('custody') != details['custody']:
        raise ValueError(label + '_POINT_CUSTODY_MISMATCH')


def recompute_shells(obj, cap, details):
    """Independent recomputation of the LO shell table from the record and the reviewed caps."""
    contract = details['row_contract']
    ids = [r['id'] for r in contract['rows']]
    radii = [r['radius_m'] for r in contract['rows']]
    tau = list(contract['tau_km_s'])
    rows = cap.get('readout_caps') or {}
    if rows.get('row_ids') != ids or rows.get('row_contract_sha256') != details['custody']['row_contract_sha256']:
        raise ValueError('LO_READOUT_CAPS_ROW_CONTRACT_MISMATCH')
    if list(rows.get('R_m', [])) != radii or list(rows.get('tau_km_s', [])) != tau:
        raise ValueError('LO_READOUT_CAPS_RADII_OR_TAU_MISMATCH')
    speeds = [_num(v, 'speed cap') for v in rows.get('speed_abs_max_km_s', [])]
    if len(speeds) != len(ids) or obj.get('row_ids') != ids:
        raise ValueError('LO_ROW_IDS_OR_SPEED_CAP_SHAPE')
    shells = obj.get('shells')
    rho_shells = (obj.get('rho') or {}).get('shells')
    if not isinstance(shells, list) or not shells or not isinstance(rho_shells, list) or len(rho_shells) != len(shells):
        raise ValueError('LO_SHELL_TABLE_MISSING')
    cursor, total, table = K, 0.0, []
    for s, rs in zip(shells, rho_shells):
        lo, hi = s.get('range_inverse_kpc', [None, None])
        if lo != cursor or not (type(hi) in (int, float) and hi > lo) or rs.get('range_inverse_kpc') != [lo, hi]:
            raise ValueError('LO_SHELL_GAP_OVERLAP_OR_RHO_PARTITION_MISMATCH')
        cursor = hi
        rho = _num(s.get('rho_used'), 'rho_used')
        if rho != rs.get('rho_used'):
            raise ValueError('LO_RHO_NOT_FROM_EMBEDDED_RHO_RECORD')
        b1 = _num(s.get('B1_per_m'), 'B1_per_m')
        per = s.get('per_row_over_tau')
        if not isinstance(per, list) or len(per) != len(ids):
            raise ValueError('LO_PER_ROW_SHAPE')
        for i, x in enumerate(per):
            _num(x, 'per_row_over_tau')
            want = speeds[i] * radii[i] * rho * b1 / (4 * tau[i])
            if not math.isclose(x, want, rel_tol=1e-12, abs_tol=1e-300):
                raise ValueError('LO_PER_ROW_RATIO_NOT_REPRODUCED')
        m = max(per)
        if s.get('max_over_tau') != m:
            raise ValueError('LO_SHELL_MAX_INCONSISTENT')
        if m > SHELL_MAX:
            raise ValueError('LO_SHELL_ABOVE_0.005_TAU: %s' % ([lo, hi],))
        total += m
        table.append({'range_inverse_kpc': [lo, hi], 'max_over_tau': m, 'rho_used': rho, 'B1_per_m': b1})
    if cursor != SHELL_END:
        raise ValueError('LO_SHELL_COVERAGE_NOT_4_TO_182')
    reported = obj.get('summed_max_over_tau')
    if type(reported) not in (int, float) or not math.isclose(reported, total, rel_tol=1e-12, abs_tol=1e-15):
        raise ValueError('LO_SUM_INCONSISTENT')
    if total > SUM_MAX:
        raise ValueError('LO_SUM_ABOVE_0.05_TAU')
    if obj.get('numerical_thresholds_pass') is not True or obj.get('all_nonzero_B1_consumed') is not True:
        raise ValueError('LO_CORE_THRESHOLD_OR_COVERAGE_FLAG_FALSE')
    return table, total


def _adapt(spec, numeric_ref, *, cap_ref, cap_review_ref, lo_review_ref, root_ruling_ref,
           approved_producer_sha256, approved_review_sha256, env):
    out = {'schema': 'UNT_POINT_LO_ENVELOPE_ADAPTER_RESULT_C3V001', 'utc': env.utc(), 'status': 'TESTED',
           'verdict': 'BLOCKED', 'blockers': [], 'proof': None, 'driver_certificate': None}
    try:
        if not isinstance(root_ruling_ref, dict) or root_ruling_ref.get('sha256') not in set(env.root_rulings):
            raise ValueError('ROOT_LO_CAP_AND_ENFORCEMENT_RULING_PENDING (brief section 6 Q1-Q5, Q8-Q10; 0674)')
        env.read_raw(root_ruling_ref)
        approved = set(approved_producer_sha256)
        me = env.self_pin()
        if me['sha256'] not in approved:
            raise ValueError('LO_ENVELOPE_ADAPTER_NOT_INDEPENDENTLY_APPROVED')
        details = env.derive_details(spec)
        obj = env.read_pin(numeric_ref)
        if obj.get('schema') != LO_SCHEMA or obj.get('gate') != 'LO' or obj.get('kind') != KIND:
            raise ValueError('LO_NUMERICAL_SCHEMA_OR_KIND_MISMATCH')
        _scope(obj, details, 'LO_NUMERICAL')
        if obj.get('point_sha256') != details['point_sha256'] or obj.get('status') != 'TESTED':
            raise ValueError('LO_NUMERICAL_POINT_OR_STATUS_MISMATCH')
        if obj.get('verdict') != CLEAN_CORE_VERDICT or obj.get('blockers') != []:
            raise ValueError('LO_CORE_RESULT_NOT_CLEAN (BLOCKED reading preserved; never relabelled)')
        for key, code in (('numerical_envelope_executed', 'LO_ENVELOPE_NOT_EXECUTED'),
                          ('covers_all_consumed_states', 'LO_COVERAGE_FALSE'),
                          ('cover_all_consumed_states', 'LO_COVERAGE_FALSE'),
                          ('coverage_is_conditional', 'LO_CONDITION_NOT_DECLARED')):
            _flag(obj, key, code)
        if not isinstance(obj.get('condition'), str) or not obj['condition'] or obj.get('production_admissible') is not False:
            raise ValueError('LO_CONDITION_TEXT_OR_ADMISSIBILITY_FIELD')
        if obj.get('facade_verdict') != 'PASS' or obj.get('certificate_status') != 'ENVELOPE_AVAILABLE':
            raise ValueError('LO_FACADE_READING_NOT_PASS')
        if obj.get('root_lo_ruling') != root_ruling_ref:
            raise ValueError('LO_FACADE_ROOT_RULING_MISMATCH')
        for key, want in (('admission_facade', None), ('producer', LO_CORE_SHA), ('response_producer', RESPONSE_SHA)):
            ref = obj.get(key)
            if not isinstance(ref, dict) or ref.get('sha256') not in approved or (want and ref['sha256'] != want):
                raise ValueError('LO_PRODUCER_NOT_APPROVED_OR_UNSUPPORTED: ' + key)
            env.read_raw(ref)
        rho = obj.get('rho') or {}
        if rho.get('schema') != RHO_SCHEMA or rho.get('gate') != 'RHO_G' or rho.get('settings') != 'registered':
            raise ValueError('RHO_SCHEMA_OR_SMOKE_SETTINGS')
        _flag(rho, 'full_registered_search_executed', 'FULL_POINT_RHO_NUMERICAL_SEARCH_UNTESTED')
        _flag(rho, 'coverage_complete', 'RHO_COVERAGE_INCOMPLETE')
        _scope(rho, details, 'RHO')
        if (rho.get('producer') or {}).get('sha256') != RESPONSE_SHA:
            raise ValueError('RHO_PRODUCER_UNSUPPORTED')
        if obj.get('cap_ref') != cap_ref or obj.get('review_ref') != cap_review_ref:
            raise ValueError('LO_RECORD_CAP_OR_CAP_REVIEW_BINDING')
        cap = env.read_pin(cap_ref)
        if cap.get('schema') != CAP_SCHEMA:
            raise ValueError('CAP_SCHEMA')
        _scope(cap, details, 'CAP')
        reviews = set(approved_review_sha256)
        if not isinstance(cap_review_ref, dict) or cap_review_ref.get('sha256') not in reviews:
            raise ValueError('CAP_REVIEW_NOT_APPROVED')
        cr = env.read_pin(cap_review_ref)
        if cr.get('schema') != CAP_REVIEW_SCHEMA or cr.get('verdict') != 'APPROVED' or cr.get('cap_ref') != cap_ref:
            raise ValueError('CAP_REVIEW_SCOPE_OR_APPROVAL')
        _scope(cr, details, 'CAP_REVIEW')
        if cr.get('producer_sha256') != LO_CORE_SHA or cr.get('response_producer_sha256') != RESPONSE_SHA:
            raise ValueError('CAP_REVIEW_PRODUCER_MISMATCH')
        en = cr.get('enforcement') or {}
        for key in ('every_constructed_and_consumed_state', 'reject_before_consume', 'complete_stage_inventory_reviewed'):
            _flag(en, key, 'CAP_ENFORCEMENT_' + key.upper() + '_UNPROVEN')
        if not en.get('module'):
            raise ValueError('REVIEWED_ENFORCEMENT_MODULE_MISSING')
        env.read_raw(en['module'])
        for key in ('accepts_registered_numerical_rho_and_node_quadrature',
                    'proper_source_caps_valid_for_all_stage_rosters', 'row_speed_and_uncertainty_policy_reviewed'):
            _flag(cr, key, 'CAP_REVIEW_' + key.upper())
        if cr.get('distinct_from_producer_lane') is not True or not cr.get('reviewer_lane'):
            raise ValueError('DISTINCT_LANE_CAP_REVIEW_UNAVAILABLE')
        if not isinstance(lo_review_ref, dict) or lo_review_ref.get('sha256') not in reviews:
            raise ValueError('INDEPENDENT_LO_NUMERICAL_REVIEW_MISSING')
        lr = env.read_pin(lo_review_ref)
        want = {'schema': LO_REVIEW_SCHEMA, 'verdict': 'APPROVED', 'numeric_ref': numeric_ref,
                'point_sha256': details['point_sha256'], 'custody_sha256': details['custody_sha256'],
                'adapter_sha256': me['sha256'], 'facade_sha256': obj['admission_facade']['sha256'],
                'accepts_conditional_prelaunch_envelope_not_rigorous_sup': True,
                'condition_acknowledged': obj['condition'], 'distinct_from_producer_lane': True}
        bad = [k for k, v in want.items() if lr.get(k) != v]
        if bad or not lr.get('reviewer_lane'):
            raise ValueError('LO_REVIEW_EXACT_BYTES_SCOPE_OR_DISTINCT_LANE: ' + ','.join(bad or ['reviewer_lane']))
        if [x.get('range_inverse_kpc') for x in obj.get('shells') or []] != RHO_PARTITION:
            raise ValueError('LO_SHELLS_NOT_THE_REGISTERED_RHO_PARTITION (no smoke or partial shells)')
        table, total = recompute_shells(obj, cap, details)
        proof = {'schema': PROOF_SCHEMA, 'gate': 'LO_ENVELOPE', 'utc': env.utc(), 'status': 'TESTED', 'verdict': 'PASS',
                 'point_sha256': details['point_sha256'], 'custody_sha256': details['custody_sha256'],
                 'producer': me, 'driver_certificate': numeric_ref, 'numeric_evidence': numeric_ref,
                 'covers_all_consumed_states': True, 'coverage_is_conditional': True, 'condition': obj['condition'],
                 'shells': table, 'summed_max_over_tau': total,
                 'row_contract_sha256': details['custody']['row_contract_sha256'],
                 'cap_ref': cap_ref, 'cap_review': cap_review_ref, 'independent_review': lo_review_ref,
                 'admission_facade': obj['admission_facade'], 'root_lo_ruling': root_ruling_ref,
                 'rigorous_supremum': False, 'production_admissible': False,
                 'scope': 'Prelaunch conditional source envelope (lapse-only omission indicator); valid only while '
                          'the reviewed enforcer rejects every constructed or consumed source or readout outside the '
                          'caps; not a per-state acceptance LO certificate.'}
        out.update(verdict='READY_FOR_MANIFEST', proof=proof, driver_certificate=numeric_ref)
    except (ValueError, KeyError, TypeError, OSError, OverflowError) as exc:
        out['blockers'].append(str(exc))
    return out


def adapt_lo_envelope(spec, numeric_ref, *, cap_ref, cap_review_ref, lo_review_ref, root_ruling_ref=None,
                      approved_producer_sha256=(), approved_review_sha256=()):
    """Public entry point. BLOCKED while ROOT_LO_RULING_SHA256 is empty (no custody derivation)."""
    return _adapt(spec, numeric_ref, cap_ref=cap_ref, cap_review_ref=cap_review_ref, lo_review_ref=lo_review_ref,
                  root_ruling_ref=root_ruling_ref, approved_producer_sha256=approved_producer_sha256,
                  approved_review_sha256=approved_review_sha256, env=_real_env())

"""S4-R-C1 prelaunch LO facade, successor of lo_producer_cx2v004 (5db60d0f) (Claude3; A122; Codex1 under A115).

v004 finish() (L25-40) set UNAVAILABLE on every path, by design (ruling 0528 item 2). This
successor keeps UNAVAILABLE whenever the caps, a distinct-lane cap review, or the reviewed
enforcement module pin is missing, and otherwise MAPS the pinned core outcome without
overriding it (the core's verdict, blockers and numbers are kept verbatim):

  facade_verdict PASS, certificate_status ENVELOPE_AVAILABLE  -- only for a clean core result:
      verdict CONDITIONAL_NUMERICAL_EVIDENCE_REVIEW_REQUIRED, blockers == [],
      numerical_envelope_executed, covers_all_consumed_states,
      rho.full_registered_search_executed, rho.settings == 'registered', and (stricter than the
      brief, defence in depth) the shell table tiles 4 -> 182 contiguously;
  facade_verdict BLOCKED  -- the envelope ran but is not clean, e.g.
      CONSERVATIVE_CAP_ENVELOPE_ABOVE_THRESHOLD: the bound cannot certify this point. That is
      NOT a NON_LAPSE_TAIL_MATERIAL finding, and caps are never re-tuned after a number is seen (R2);
  facade_verdict UNAVAILABLE  -- everything else (0528 item 2 holds).
production_admissible is always False; the LO_ENVELOPE proof comes only from the reviewed adapter.

ROOT GATE. No LO number may be produced before root rules on the caps and their enforcement
(brief section 6 Q1-Q5 and Q8-Q10; FROM_CODEX/0674). ROOT_LO_RULING_SHA256 is empty, so the
public entry point returns UNAVAILABLE before any point context, rho search or B1 quadrature.
A successor version adds the ruling pin. The builder exercised the mapping on synthetic core
outputs only. Pinned core: lo_core_r5_cx2v001 12d36305 (unchanged, so Claude4's review and the
cap-review binding producer_sha256 = 12d36305 at core L424 stay valid).
"""
import hashlib
import importlib.util
import os
import sys
import types

ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
CERT = ART + '/calib_tail_readiness_cx2/certificates_per_point'
LO_CORE = (CERT + '/lo_core_r5_cx2v001.py', '12d36305e09651fcb0dca0b76f85c755ff063c9d9e3ce0dd1e1baacf7b3d430e')
CUSTODY = (CERT + '/custody_cx2v002.py', '6810b7c3614e219f6e059208fbe59e905d01aa3a115e3c723079b579a027a377')
RESPONSE_SHA = 'a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231'
RULING_0528 = {'path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0528_2026-10-18_codex2_rulings_P0_normalization_and_certificate_admission.md',
               'sha256': 'd11654e5a2ab24944a861372769e75e0a2bbac035feecdf4a54286e3841aae83'}
ROOT_LO_RULING_SHA256 = ()          # empty until root rules Q1-Q5, Q8-Q10 (0674); a successor pins it
CLEAN_CORE_VERDICT = 'CONDITIONAL_NUMERICAL_EVIDENCE_REVIEW_REQUIRED'
CAP_REVIEW_SCHEMA = 'UNT_POINT_LO_CAP_REVIEW_CX2V001'
FACADE_RECORD_SCHEMA = 'S4RC1_LO_FACADE_UNAVAILABLE_C3V001'
ABOVE = 'CONSERVATIVE_CAP_ENVELOPE_ABOVE_THRESHOLD'


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


def _self_pin():
    p = __file__
    with open(p, 'rb') as f:
        return {'path': str(p), 'sha256': hashlib.sha256(f.read()).hexdigest()}


def _real_env():
    state = {}

    def core():
        if 'core' not in state:
            state['core'] = _load_exact(LO_CORE[0], LO_CORE[1], 's4rc1_lo_core_r5_cx2v001')
        return state['core']

    def read_pin(ref):
        return core().CU.read_pin(ref)

    def read_raw(ref):
        return core().CU.read_pin(ref, document=False)

    return types.SimpleNamespace(core=core, read_pin=read_pin, read_raw=read_raw, self_pin=_self_pin,
                                 root_rulings=ROOT_LO_RULING_SHA256,
                                 point_context=lambda spec: core().PR.point_context(spec))


def classify(rec):
    """Pure mapping of a core record to the facade reading. Never edits the core fields."""
    rho = rec.get('rho') if isinstance(rec.get('rho'), dict) else {}
    shells = rec.get('shells') if isinstance(rec.get('shells'), list) else []
    edges = [s.get('range_inverse_kpc') for s in shells if isinstance(s, dict)]
    tiled = bool(edges) and len(edges) == len(shells) and edges[0][0] == 4.0 and edges[-1][1] == 182.0 and all(
        a[1] == b[0] for a, b in zip(edges[:-1], edges[1:]))
    cond = {
        'core_verdict_clean': rec.get('verdict') == CLEAN_CORE_VERDICT,
        'blockers_empty': rec.get('blockers') == [],
        'numerical_envelope_executed': rec.get('numerical_envelope_executed') is True,
        'covers_all_consumed_states': rec.get('covers_all_consumed_states') is True,
        'rho_full_registered_search_executed': rho.get('full_registered_search_executed') is True,
        'rho_settings_registered': rho.get('settings') == 'registered',
        'shells_tile_4_to_182': tiled,
    }
    if all(cond.values()):
        return 'PASS', 'ENVELOPE_AVAILABLE', cond, (
            'Conditional prelaunch envelope is numerically clean; valid only while the reviewed enforcer '
            'rejects every constructed or consumed source or readout outside the caps. Review and the '
            'LO_ENVELOPE adapter are still required; production_admissible stays False.')
    if rec.get('numerical_envelope_executed') is True:
        blockers = rec.get('blockers') or []
        if ABOVE in blockers:
            text = (ABOVE + ': the conservative cap envelope cannot certify this point, so LO stays BLOCKED. '
                    'This is NOT a NON_LAPSE_TAIL_MATERIAL finding. The reading is preserved as measured and '
                    'the caps may not be re-tuned after this number (R2; 0674).')
        else:
            text = 'Envelope executed but not clean; the core blockers are kept verbatim.'
        return 'BLOCKED', 'BLOCKED', cond, text
    return 'UNAVAILABLE', 'UNAVAILABLE', cond, (
        'Prelaunch LO reads UNAVAILABLE and the point is not admitted (0528 item 2): caps, the distinct-lane '
        'cap review, or the reviewed enforcement module are missing, or the core blocked before any number.')


def _facade_fields(out, env, verdict, status, cond, text, root_ruling_ref):
    out['admission_facade'] = env.self_pin()
    out['ruling'] = dict(RULING_0528)
    out['root_lo_ruling'] = root_ruling_ref
    out['signed_GQ_branch'] = 'CONSERVATIVE_FINITE_DENOMINATOR'
    out['execution_policy'] = {'fresh_calls_only': True, 'resume_allowed': False, 'retry_allowed': False,
                               'interrupted_route_a_invalid': True, 'certificates_from_own_run_saved_states': True}
    out['facade_verdict'] = verdict
    out['certificate_status'] = status
    out['point_status'] = 'PENDING_LO_ENVELOPE_REVIEW_AND_ADAPTER' if verdict == 'PASS' else 'NOT_ADMITTED'
    out['production_admissible'] = False
    out['facade_conditions'] = cond
    out['facade_reading'] = text
    out['facade_rule'] = 'S4-R-C1 c3v001: map, never override; PASS only for a clean core result'
    return out


def _unavailable(env, reason, root_ruling_ref):
    out = {'schema': FACADE_RECORD_SCHEMA, 'gate': 'LO', 'kind': 'PRELAUNCH_CONDITIONAL_SOURCE_ENVELOPE',
           'status': 'UNTESTED', 'verdict': 'UNAVAILABLE', 'blockers': [reason],
           'numerical_envelope_executed': False, 'covers_all_consumed_states': False,
           'cover_all_consumed_states': False, 'driver_certificate': None, 'lo_numbers_produced': False}
    v, s, cond, text = classify(out)
    return _facade_fields(out, env, v, s, cond, text, root_ruling_ref)


def _produce(spec, cap_ref, *, review_ref, trusted_review_hashes, root_ruling_ref, context, env):
    # 1. Root gate before anything is computed or loaded.
    if not isinstance(root_ruling_ref, dict) or root_ruling_ref.get('sha256') not in set(env.root_rulings):
        return _unavailable(env, 'ROOT_LO_CAP_AND_ENFORCEMENT_RULING_PENDING (brief section 6 Q1-Q5, Q8-Q10; 0674)',
                            root_ruling_ref)
    try:
        env.read_raw(root_ruling_ref)
    except Exception as exc:
        return _unavailable(env, 'ROOT_LO_RULING_UNREADABLE: ' + str(exc), root_ruling_ref)
    # 2. Caps and a distinct-lane, enforcement-backed cap review must exist (0528 item 2).
    if cap_ref is None:
        return _unavailable(env, 'REVIEWED_PROPER_SOURCE_AND_READOUT_CAPS_MISSING', root_ruling_ref)
    if review_ref is None:
        return _unavailable(env, 'CAP_REVIEW_MISSING', root_ruling_ref)
    try:
        review = env.read_pin(review_ref)
    except Exception as exc:
        return _unavailable(env, 'DISTINCT_LANE_CAP_REVIEW_INVALID: ' + str(exc), root_ruling_ref)
    if review.get('schema') != CAP_REVIEW_SCHEMA:
        return _unavailable(env, 'CAP_REVIEW_SCHEMA_MISMATCH', root_ruling_ref)
    if review.get('distinct_from_producer_lane') is not True or not review.get('reviewer_lane'):
        return _unavailable(env, 'DISTINCT_LANE_CAP_REVIEW_UNAVAILABLE', root_ruling_ref)
    if not (review.get('enforcement') or {}).get('module'):
        return _unavailable(env, 'REVIEWED_ENFORCEMENT_MODULE_MISSING', root_ruling_ref)
    if review_ref.get('sha256') not in set(trusted_review_hashes):
        return _unavailable(env, 'CAP_REVIEW_NOT_IN_CALLER_TRUSTED_ALLOWLIST', root_ruling_ref)
    # 3. The pinned core, registered settings over the full domain; no smoke, no partial shells.
    core = env.core()
    ctx = context or env.point_context(spec)
    rec = core.produce_conditional_lo(spec, cap_ref, review_ref=review_ref,
                                      trusted_review_hashes=tuple(trusted_review_hashes),
                                      settings='registered', shell_ranges=None, context=ctx)
    v, s, cond, text = classify(rec)
    rec['lo_numbers_produced'] = rec.get('numerical_envelope_executed') is True
    return _facade_fields(rec, env, v, s, cond, text, root_ruling_ref)


def produce_conditional_lo(spec, cap_ref=None, *, review_ref=None, trusted_review_hashes=(),
                           root_ruling_ref=None, context=None):
    """Public entry point. Returns UNAVAILABLE while ROOT_LO_RULING_SHA256 is empty."""
    return _produce(spec, cap_ref, review_ref=review_ref, trusted_review_hashes=trusted_review_hashes,
                    root_ruling_ref=root_ruling_ref, context=context, env=_real_env())

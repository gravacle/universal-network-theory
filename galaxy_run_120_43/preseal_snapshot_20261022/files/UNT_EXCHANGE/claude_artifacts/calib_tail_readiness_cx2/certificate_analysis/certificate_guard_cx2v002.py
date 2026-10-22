"""Fail-closed v002 guard: positive-source GQ plus conservative signed-P0 TV branch.

This checks integrity, scope and recorded numbers, not the scientific truth of a
producer. The caller must independently approve producer hashes, derive expected
custody from trusted inputs, and enumerate ALL consumed states from the result.
Missing proofs are pending; an anchor proof never becomes a box certificate.
"""
import hashlib
import json
import math
from pathlib import Path

SCHEMA = 'UNT_CALIBRATION_POINT_CERTIFICATES_CX2V001'
PROOF_SCHEMA = 'UNT_CALIBRATION_POINT_PROOF_CX2V001'
ENVELOPE = 'A52_5_SUP_OVER_DIRECTION_TIMES_CARDINAL_TORUS'
CUSTODY_KEYS = {'grid_sha256', 'background_sha256', 'geometry_sha256',
                'modules_sha256', 'row_contract_sha256'}
ART = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()


def _sha_string(x):
    return isinstance(x, str) and len(x) == 64 and all(c in '0123456789abcdef' for c in x)


def _number(x, lower=0.0):
    return type(x) in (int, float) and math.isfinite(x) and x >= lower


def _read(ref, allowed_roots, json_document=True):
    if not isinstance(ref, dict) or set(ref) != {'path', 'sha256'} or not _sha_string(ref['sha256']):
        raise ValueError('malformed byte pin')
    p = Path(ref['path']).resolve(strict=True)
    parts = p.parts
    if '.codex' in parts or any(s.casefold().startswith('uvt_') for s in parts):
        raise ValueError('forbidden input path')
    if any(s.casefold() == 'kmax_a2f10_c5h_run_v001' for s in parts):
        raise ValueError('forbidden C5H path')
    roots = [Path(r).resolve(strict=True) for r in allowed_roots]
    if not any(p.is_relative_to(r) for r in roots):
        raise ValueError('proof path outside allowed certificate artifact roots')
    # Small records/code only. No raw state arrays or run directories are opened.
    if p.stat().st_size > 8 * 1024 * 1024:
        raise ValueError('proof/code file exceeds 8 MiB')
    raw = p.read_bytes()
    if hashlib.sha256(raw).hexdigest() != ref['sha256']:
        raise ValueError('byte pin mismatch')
    return json.loads(raw) if json_document else raw


def verify_bundle(ref, expected_identity, *, expected_custody=None,
                  approved_producer_sha256=(), phase='prelaunch', required_states=(),
                  allowed_roots=(ART,)):
    """Return {ok, blockers, evidence}; malformed/missing inputs never pass.

    identity is the complete physical/coefficient/numerics/driver identity; remove
    label, certificate slots and derived config hash to avoid a reference cycle.
    custody must be computed independently, including derived geometry and row
    contract. required_states are exact dictionaries {state_sha256, source_sha256,
    stage_kind, nonnegative_masses}; supply every source state consumed by the
    accepted call, including route-A mixtures and final route-B sources.
    """
    out = {'ok': False, 'blockers': [], 'evidence': [], 'phase': phase}
    fail = out['blockers'].append
    try:
        if phase not in ('prelaunch', 'acceptance'):
            raise ValueError('unknown phase')
        if not isinstance(expected_identity, dict) or not expected_identity:
            raise ValueError('expected identity required')
        if not isinstance(expected_custody, dict) or set(expected_custody) != CUSTODY_KEYS:
            raise ValueError('trusted expected custody required')
        if not all(_sha_string(v) for v in expected_custody.values()):
            raise ValueError('invalid trusted custody hash')
        approved = set(approved_producer_sha256)
        if not approved or not all(_sha_string(x) for x in approved):
            raise ValueError('independently approved producer hashes required')
        doc = _read(ref, allowed_roots)
        if doc.get('schema') != SCHEMA or doc.get('identity') != expected_identity:
            raise ValueError('manifest schema/point identity mismatch')
        if doc.get('custody') != expected_custody:
            raise ValueError('manifest custody mismatch')
        point_sha, custody_sha = digest(expected_identity), digest(expected_custody)
        domain = doc['domain']
        if set(domain) != {'K_inverse_kpc', 'K_big_inverse_kpc'}:
            raise ValueError('domain keys')
        K, Kbig = domain['K_inverse_kpc'], domain['K_big_inverse_kpc']
        if K != 4.0 or Kbig not in (64.0, 128.0):
            raise ValueError('unsupported calibration domain')
        numerics = expected_identity['numerics']
        uv = numerics['uv_tail']
        if uv['outer'] != {'shape': 'cylinder', 'K_big_inverse_kpc': Kbig}:
            raise ValueError('domain differs from trusted point')
        if uv.get('source_rule') != 'continuum_v001' or uv.get('enabled') is not True:
            raise ValueError('production continuum tail required')
        edge = math.ceil(math.sqrt(2.0) * Kbig)

        def proof(pin, gate):
            obj = _read(pin, allowed_roots)
            if obj.get('schema') != PROOF_SCHEMA or obj.get('gate') != gate:
                raise ValueError(gate + ' proof schema/gate mismatch')
            if obj.get('status') != 'TESTED' or obj.get('verdict') != 'PASS':
                raise ValueError(gate + ' proof not TESTED PASS')
            if obj.get('point_sha256') != point_sha or obj.get('custody_sha256') != custody_sha:
                raise ValueError(gate + ' scope mismatch')
            producer = obj['producer']
            if producer.get('sha256') not in approved:
                raise ValueError(gate + ' producer not independently approved')
            _read(producer, allowed_roots, False)
            out['evidence'].append(pin)
            return obj

        def shells(obj, gate):
            arr = obj['shells']
            if not isinstance(arr, list) or not arr:
                raise ValueError(gate + ' missing shell table')
            cursor = float(K)
            for s in arr:
                lo, hi = s['range_inverse_kpc']
                if not _number(lo) or not _number(hi) or lo != cursor or hi <= lo:
                    raise ValueError(gate + ' shell gap/overlap/invalid range')
                cursor = hi
            if cursor < edge:
                raise ValueError(gate + ' spherical coverage shortfall')
            return arr

        eps = proof(doc['prelaunch']['EPS'], 'EPS')
        if eps.get('envelope_rule') != ENVELOPE:
            raise ValueError('EPS lacks cardinal-torus envelope')
        for s in shells(eps, 'EPS'):
            if type(s.get('refinement_failures')) is not int or s['refinement_failures'] not in (0, 1):
                raise ValueError('EPS refinement failures')
            if not _number(s.get('eps')) or not _number(s.get('eps_envelope')) or s['eps'] < s['eps_envelope']:
                raise ValueError('EPS must carry the conservative envelope')

        gq = proof(doc['prelaunch']['GQ'], 'GQ')
        flags = ('all_columns_included', 'all_production_kperp_nodes', 'nonnegative_masses_required')
        if gq.get('method') != 'GEOMETRY_UNIFORM_COLUMN_BOUND' or any(gq.get(x) is not True for x in flags):
            raise ValueError('GQ prelaunch requires geometry-uniform all-column bound')
        if gq.get('M_s') != uv['gas']['M_s'] or gq.get('M_s_doubled') != 2 * uv['gas']['M_s']:
            raise ValueError('GQ quadrature order mismatch')
        if gq.get('K_big_inverse_kpc') != Kbig:
            raise ValueError('GQ outer domain mismatch')
        b, z = gq.get('max_column_difference_over_analytic_Pi0'), gq.get('max_zero_mode_relative_error')
        if not _number(b) or not _number(z) or z >= 1 or b / (1 - z) > 1e-12:
            raise ValueError('GQ numerical bound failed')
        if doc.get('acceptance_rule') != 'ALL_CONSUMED_STATES_LO_AND_GQ_FAIL_CLOSED':
            raise ValueError('missing post-state acceptance rule')
        if phase == 'acceptance':
            required = list(required_states)
            if not required or len({digest(x) for x in required}) != len(required):
                raise ValueError('trusted complete unique state inventory required')
            records = doc.get('states', [])
            keyed = {digest(x['state']): x for x in records}
            if len(keyed) != len(records) or set(keyed) != {digest(x) for x in required}:
                raise ValueError('state inventory mismatch')
            for state in required:
                if set(state) != {'state_sha256', 'source_sha256', 'stage_kind', 'nonnegative_masses'}:
                    raise ValueError('invalid state identity keys')
                if not all(_sha_string(state[k]) for k in ('state_sha256', 'source_sha256')):
                    raise ValueError('invalid state/source hashes')
                if not isinstance(state['stage_kind'], str) or not state['stage_kind'] or type(state['nonnegative_masses']) is not bool:
                    raise ValueError('invalid state mass-sign declaration')
                row = keyed[digest(state)]
                if state['nonnegative_masses'] is False:
                    signed = proof(row['GQ_SIGNED'], 'GQ_SIGNED')
                    if signed.get('state') != state:
                        raise ValueError('signed GQ state/source mismatch')
                    if signed.get('method') != 'TV_BOUND_WITH_SIGNED_P0' or signed.get('normalization') != 'ABS_SIGNED_ZERO_MODE':
                        raise ValueError('signed GQ requires explicit unchanged signed-P0 normalization')
                    if signed.get('positive_components_verified') is not True:
                        raise ValueError('signed GQ component positivity unverified')
                    if signed.get('GQ_uniform_proof_sha256') != doc['prelaunch']['GQ']['sha256']:
                        raise ValueError('signed GQ uniform-proof mismatch')
                    p0, tv = signed.get('P0_abs_signed_mass_kg'), signed.get('component_mass_sum_kg')
                    if not _number(p0) or p0 <= 0 or not _number(tv) or tv < p0:
                        raise ValueError('signed GQ zero/invalid normalization; root ruling required')
                    bound = (b / (1 - z)) * (tv / p0)
                    recorded = signed.get('max_difference_over_signed_P0_bound')
                    if not _number(recorded) or not math.isfinite(bound) or not math.isclose(recorded, bound, rel_tol=1e-12, abs_tol=1e-18):
                        raise ValueError('signed GQ contradictory TV/P0 bound')
                    if bound > 1e-12:
                        raise ValueError('signed GQ TV/P0 bound insufficient; exact replay or root ruling required')
                lo = proof(row['LO'], 'LO')
                if lo.get('state') != state:
                    raise ValueError('LO current state/source mismatch')
                tab = shells(lo, 'LO')
                vals = [s.get('max_over_tau') for s in tab]
                if any(not _number(x) or x > 0.005 for x in vals):
                    raise ValueError('LO per-shell threshold failed')
                total = sum(vals)
                reported = lo.get('summed_max_over_tau')
                if not _number(reported) or not math.isclose(reported, total, rel_tol=1e-12, abs_tol=1e-15) or total > 0.05:
                    raise ValueError('LO sum or aggregate threshold failed')
                if lo.get('row_contract_sha256') != expected_custody['row_contract_sha256']:
                    raise ValueError('LO row contract mismatch')
                if lo.get('i1t_verdict') != 'PASS' or lo.get('GQ_uniform_proof_sha256') != doc['prelaunch']['GQ']['sha256']:
                    raise ValueError('LO source fidelity/GQ custody missing')
        out['ok'] = True
        out['note'] = ('prelaunch scope only: LO remains a mandatory post-state acceptance gate; '
                       'this return is not launch authorization' if phase == 'prelaunch' else
                       'certificate metadata/gate checks passed for caller-supplied full state inventory')
    except (OSError, ValueError, KeyError, TypeError, OverflowError) as exc:
        fail(str(exc))
    return out

"""values_writer_c2v002 -- the members eps_km_s writer (V006 A148; A144 R3; Claude3 0211 N1). Root build (Claude2).
Reviewer of record: Claude4 (certificate-schema owner, did not build the writer). Nothing here is adopted until root
rules W-1 under A115(b) (A148 does not name srb_rot) and Claude4's review returns.

One writer serves the Phase-1 values file (u_A and the F points) and the Phase-2 members file (A148). For each point it
emits one record (UNT_POINT_EPS_KM_S_C2V002):
  - the point's theta key;
  - the path and sha of the certificate whose point.key equals that key (anchor, other-point, SMOKE and BIND_CHECK
    records are refused);
  - the certificate checks: schema UNT_CLAUDE4_S0_POINT_EPS_C4V002, status CERTIFIED, coverage [2,91] /kpc covering
    field_bound's k-range on this point's own state;
  - 43 eps_km_s in the values file's query order, with the field_bound / srb_rot pin recorded.

PRIMARY RULE (W-1; the A146-adopted SRB-ROT adapter's own call, srb_rot_adapter_c3v003 08e9ac0a L439-440):
  eps_km_s[q] = srb_rot(S, C, rows)['bound_km_s'][q]   (owned_uv_tail_lapse_v002 2026f2b6, field_bound L847-857,
                                                        srb_rot L860-871)
  S    = the TailState of the call's own stage le{final_pass}_rotation (V006 A134 reading point, L525), bound to the
         call by state digest == that stage's own finish.json uv_tail.state_digest; S.record.eps_certificate must equal
         the point's EPS pin (adapter L434).
  C    = the point's own certificate, field 'eps' per unit shell (the larger recorded value; adapter format_eps).
  rows = rotation_rows (row_reference_producer_c2v003 67fddd24 L171-193; the V007 SRB_ROT producer rule) on the
         call's own rotation_base_arrays.npz of that stage: column_R_m = radial_nodes_m, v_c_m_s = R*sqrt(min over z
         of rotation_Omega_squared), N_min = min(1 + Re full_fields_complex[..., 0]), row_columns = the node at the
         row radius else the two bracketing nodes. Row radii are the call's own (column-mean query_support[].radius_m).
  Every input is computed from the point's own outputs. Nothing is declared.
Not done (alternatives for root, never applied here): v = speeds_km_s[q]; evaluating at R_q in place of the max over
a row's columns; a declared N_min; multiplying by sin(i_phys)/sin(i_released) (printed, not applied).

Mechanics, all fail-closed:
  - srb_rot needs tau_km_s; bound_km_s does not depend on it (L866-869). tau is fed as the inert constant 1.0 per
    row, and ratio_to_tau / pass_tau_over_10 are discarded. No NGC sigma or observed value is read.
  - Rows the call itself marks invalid (speed null, valid false: N1/A4 reasons) get None with that reason; rotation_rows
    runs on the call's valid rows only. A point with no certificate gets 43 None (A148); A144 R3 then flags the pair.
  - eps_max is never read or broadcast; no other point's value is used (each record is bound to one theta key, one
    certificate, one call and one state).
  - attach_eps refuses while ROOT_RULING is None (the W-1 stop), so no record can enter a values or members file
    before root rules. main() refuses for the same reason.
"""
import hashlib
import importlib.util
import json
import math
import os
import re
import sys
from pathlib import Path

MODULE = 'values_writer_c2v002'
ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
LIBRARY = (ART + '/tail_scheme_impl_c2/driver_r5/module/owned_uv_tail_lapse_v002.py',
           '2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54')
ROW_PRODUCER = (ART + '/s4_acceptance_c2/acceptance_q2/row_reference_producer_c2v003.py',
                '67fddd24945de31d70f940cb1ff85ef9d467b20d62a764cd159f58afc909e01e')
DRIVER_SHA256 = '577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377'   # cx3r008 (A136, A141)
CERT_SCHEMAS = ('UNT_CLAUDE4_S0_POINT_EPS_C4V002',)                 # A148 (a reviewed successor needs a writer successor)
CERT_PRODUCERS = ('8972822b5439e184297b4a5dbb552983ddb806804565ee1cc26691b680147235',)   # eps_ngc_point_c4v002 (A148)
CERT_COVERAGE = (2.0, 91.0)                                         # /kpc, A148
N_ROWS = 43                                                         # phase1 check_values / members_values n_rows
VALUES_SCHEMA = 'PHASE1_NGC_VALUES_C2V001'                          # phase1_c2v002 / v003 S_VALUES
RECORD_SCHEMA = 'UNT_POINT_EPS_KM_S_C2V002'
FINAL_ROTATION_KIND = 'le_rotation'                                 # driver L354 rotation_v005 -> le_rotation
COLUMN_MEAN_OK = 'CONDITIONAL_PREPARATION_ROWS_NOT_CALIBRATION'     # driver L5973
INERT_TAU_KM_S = 1.0
ROOT_RULING = None          # W-1 (A115(b)): a successor pins root's ruling {'path', 'sha256'} here; None = stop
RULE = ('W-1 PRIMARY (pending root ruling): eps_km_s[q] = owned_uv_tail_lapse_v002 srb_rot(S, C, rows)[bound_km_s][q]; '
        'S = the TailState at le{final_pass}_rotation of the point\'s own call (digest = own finish.json '
        'uv_tail.state_digest; record.eps_certificate = the point EPS pin); C = the point certificate, field eps per '
        'unit shell; rows = row_reference_producer_c2v003 rotation_rows on the own rotation_base_arrays.npz and the '
        'own row radii; tau inert (bound_km_s does not depend on it); invalid call rows None.')
ALTERNATIVES = ('A-1 v = speeds_km_s[q] in place of v_c from rotation_Omega_squared',
                'A-2 the bound at R_q in place of the max over the row columns',
                'A-3 a declared N_min in place of min(1 + Re lapse) over full_fields_complex',
                'A-4 multiply by sin(i_phys)/sin(i_released) (V007 srb_rot_record L60-61, L106 did; row producer v003 '
                'does not); the factor is printed from the call own column-mean packet, never applied here')
NEVER = ('eps_max is never read or broadcast; no other point, call or state is read for this point; no NGC observed '
         'velocity, error or sigma is read; tau is inert')


class Refused(Exception):
    def __init__(self, code, detail=''):
        Exception.__init__(self, '%s: %s' % (code, detail))
        self.code = code


# ------------------------------------------------------------------------------------------------ bytes and pins
def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()


def _hex(x):
    return isinstance(x, str) and len(x) == 64 and all(c in '0123456789abcdef' for c in x)


def is_pin(x):
    return isinstance(x, dict) and set(x) == {'path', 'sha256'} and isinstance(x['path'], str) \
        and os.path.isabs(x['path']) and _hex(x['sha256'])


def read_pinned(pin, where):
    if not is_pin(pin):
        raise Refused('PIN_INVALID', where)
    try:
        raw = Path(pin['path']).read_bytes()
    except OSError as exc:
        raise Refused('PIN_UNREADABLE', '%s: %s' % (where, exc))
    if hashlib.sha256(raw).hexdigest() != pin['sha256']:
        raise Refused('PIN_SHA_MISMATCH', where)
    return raw


def read_own(pin, out, where):
    """Own-call bytes only: the file resolves inside <call>/out and matches its pin (row producer _own_bytes)."""
    if not is_pin(pin):
        raise Refused('OWN_CALL_PIN_INVALID', where)
    try:
        p = Path(pin['path']).resolve(strict=True)
    except OSError as exc:
        raise Refused('OWN_CALL_FILE_MISSING', '%s: %s' % (where, exc))
    if not p.is_relative_to(out):
        raise Refused('OUTSIDE_OWN_CALL', where)
    raw = p.read_bytes()
    if hashlib.sha256(raw).hexdigest() != pin['sha256']:
        raise Refused('OWN_CALL_SHA_MISMATCH', where)
    return raw


def json_from(raw, where):
    try:
        return json.loads(raw)
    except ValueError as exc:
        raise Refused('JSON_INVALID', '%s: %s' % (where, exc))


def load_exact(path, sha, name):
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != sha:
        raise Refused('MODULE_PIN_MISMATCH', path)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    exec(compile(raw, path, 'exec'), mod.__dict__)
    return mod


_MODS = {}


def modules():
    if not _MODS:
        _MODS['lib'] = load_exact(LIBRARY[0], LIBRARY[1], 'vw2_owned_uv_tail_lapse_v002')
        _MODS['rows'] = load_exact(ROW_PRODUCER[0], ROW_PRODUCER[1], 'vw2_row_reference_producer_c2v003')
    return _MODS['lib'], _MODS['rows']


def self_pin():
    p = os.path.abspath(__file__)
    return {'path': p, 'sha256': hashlib.sha256(Path(p).read_bytes()).hexdigest()}


def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


# ------------------------------------------------------------------------------------------------ certificate
def check_certificate(cert_pin, theta_key):
    """The point's own certificate -> ({'shells': [{lo, hi, eps}]}, checks). Refuses anchor, other-point, SMOKE and
    BIND_CHECK records (A148). Field 'eps' is fed (the larger recorded value, >= the envelope); eps_max is not read."""
    rec = json_from(read_pinned(cert_pin, 'certificate'), 'certificate')
    if not isinstance(rec, dict) or rec.get('schema') not in CERT_SCHEMAS:
        raise Refused('CERT_SCHEMA', 'schema %r (BIND_CHECK, SMOKE, RUN_START and RUN_STOP records are refused)'
                      % (rec.get('schema') if isinstance(rec, dict) else None))
    pt = rec.get('point') if isinstance(rec.get('point'), dict) else {}
    role = str(pt.get('role'))
    if rec.get('mode') != 'point' or 'anchor' in role.lower() or 'smoke' in role.lower():
        raise Refused('CERT_NOT_A_POINT_RECORD', 'mode %r role %r' % (rec.get('mode'), role))
    if not _hex(theta_key) or pt.get('key') != theta_key:
        raise Refused('CERT_OTHER_POINT', 'certificate point.key %r != theta key %r' % (pt.get('key'), theta_key))
    kc = rec.get('key_check') or {}
    if kc.get('equals_point_key') is not True or kc.get('from_theta_hex') != theta_key \
            or kc.get('from_theta_natural') != theta_key:
        raise Refused('CERT_KEY_CHECK', 'the record does not recompute its own key')
    prod = rec.get('producer')
    if not isinstance(prod, dict) or prod.get('sha256') not in CERT_PRODUCERS:
        raise Refused('CERT_PRODUCER_NOT_REVIEWED', repr(prod))
    if rec.get('gate') != 'EPS' or rec.get('verdict') != 'CERTIFIED' or rec.get('certificate') is not True \
            or (rec.get('summary') or {}).get('rule_verdict') != 'CERTIFIED':
        raise Refused('CERT_NOT_CERTIFIED', 'gate %r verdict %r certificate %r' % (rec.get('gate'), rec.get('verdict'),
                                                                             rec.get('certificate')))
    if rec.get('coverage_inverse_kpc') != {'NGC': list(CERT_COVERAGE)}:
        raise Refused('CERT_COVERAGE', repr(rec.get('coverage_inverse_kpc')))
    shells = rec.get('shells')
    if not isinstance(shells, list) or not shells:
        raise Refused('CERT_SHELLS_MISSING')
    cursor, out = CERT_COVERAGE[0], []
    for s in shells:
        lo, hi, eps = (s.get(k) if isinstance(s, dict) else None for k in ('lo_inverse_kpc', 'hi_inverse_kpc', 'eps'))
        if not (_num(lo) and _num(hi) and _num(eps)) or lo != cursor or hi != lo + 1.0:
            raise Refused('CERT_SHELLS_NOT_CONTIGUOUS_UNIT_SHELLS', 'at %r' % (cursor,))
        envs = [(s.get(k) or {}).get('eps_envelope') for k in ('flat', 'envelope')]
        if eps < 0 or not all(_num(e) and 0 <= e <= eps for e in envs):
            raise Refused('CERT_EPS_NOT_THE_LARGER_VALUE', 'shell (%g,%g]' % (lo, hi))
        out.append({'lo_inverse_kpc': float(lo), 'hi_inverse_kpc': float(hi), 'eps': float(eps)})
        cursor = hi
    if cursor != CERT_COVERAGE[1]:
        raise Refused('CERT_COVERAGE', 'shells end at %r' % (cursor,))
    checks = {'schema': rec['schema'], 'mode': 'point', 'point_key': theta_key, 'point_role': role, 'gate': 'EPS',
              'verdict': 'CERTIFIED', 'certificate': True, 'coverage_inverse_kpc': list(CERT_COVERAGE),
              'n_unit_shells': len(out), 'producer_sha256': prod['sha256'], 'eps_field': 'eps (>= eps_envelope)',
              'eps_max_read': False}
    return {'shells': out}, checks


def coverage_on_state(state, cov=CERT_COVERAGE):
    """A148: coverage [2,91] covers field_bound's k-range = the state's unit shells with nonzero shell integrals."""
    import numpy as np
    if state.empty:
        return {'k_range_nonzero_inverse_kpc': None, 'covered': True, 'state_empty': True}
    edges = np.asarray(state._a['shell_edges_inverse_kpc'], float)
    nz = np.flatnonzero(np.any(np.asarray(state._a['shell_integrals']) != 0, axis=1))
    if not len(nz):
        return {'k_range_nonzero_inverse_kpc': None, 'covered': True, 'state_empty': False}
    lo, hi = float(edges[nz[0]]), float(edges[nz[-1] + 1])
    if lo < cov[0] - 1e-12 or hi > cov[1] + 1e-12:
        raise Refused('CERT_COVERAGE_DOES_NOT_COVER_STATE', 'state k-range [%g,%g] /kpc vs [%g,%g]' % (lo, hi, cov[0], cov[1]))
    return {'k_range_nonzero_inverse_kpc': [lo, hi], 'covered': True, 'state_empty': False}


# ------------------------------------------------------------------------------------------------ the call's own outputs
def check_query_ids(query_ids):
    if not isinstance(query_ids, list) or len(query_ids) != N_ROWS or len(set(query_ids)) != N_ROWS \
            or not all(isinstance(q, str) and q for q in query_ids):
        raise Refused('QUERY_IDS', '%d unique nonempty ids required (the values file query_ids)' % N_ROWS)


def call_outputs(call_dir, query_ids, cert_pin, call_spec_sha256):
    """The final-pass rotation stage, its arrays, and the call's own row radii, from <call>/out only."""
    import io
    import numpy as np
    try:
        out = (Path(call_dir).resolve(strict=True) / 'out').resolve(strict=True)
    except (OSError, TypeError) as exc:
        raise Refused('CALL_DIR', str(exc))
    rp = out / 'result.json'
    try:
        rraw = rp.read_bytes()
    except OSError as exc:
        raise Refused('CALL_RESULT_MISSING', str(exc))
    result_pin = {'path': str(rp), 'sha256': hashlib.sha256(rraw).hexdigest()}
    res = json_from(rraw, 'result.json')
    if res.get('driver_sha256') != DRIVER_SHA256:
        raise Refused('DRIVER_NOT_CX3R008', repr(res.get('driver_sha256')))
    if res.get('galaxy') != 'NGC3198':
        raise Refused('CALL_GALAXY', repr(res.get('galaxy')))
    if not _hex(call_spec_sha256) or res.get('call_spec_sha256') != call_spec_sha256:
        raise Refused('CALL_SPEC_SHA', 'the call is not the point custody spec (A136 G3)')
    uv = ((res.get('normalized_spec') or {}).get('numerics') or {}).get('uv_tail') or {}
    if uv.get('eps_certificate') != cert_pin:
        raise Refused('CALL_EPS_PIN_NOT_THE_POINT_CERTIFICATE', 'normalized_spec numerics.uv_tail.eps_certificate')
    n, passes = res.get('final_pass'), res.get('passes')
    if type(n) is not int or n < 1 or not isinstance(passes, list) or len(passes) != n \
            or not isinstance(passes[-1], dict) or passes[-1].get('pass') != n:
        raise Refused('FINAL_PASS_UNAVAILABLE')
    fp = passes[-1]
    stage = 'le%d_rotation' % n
    rot = Path(str(fp.get('rotation')))
    if not re.fullmatch(r'[0-9]+_' + stage, rot.parent.name) or rot.name != 'rotation':
        raise Refused('FINAL_ROTATION_STAGE', '%s is not stage %s' % (rot, stage))
    arrays_pin = fp.get('rotation_arrays')
    try:
        fin_path = (rot / 'finish.json').resolve(strict=True)
    except OSError as exc:
        raise Refused('OWN_CALL_FILE_MISSING', 'rotation finish: %s' % exc)
    fin_pin = {'path': str(fin_path), 'sha256': hashlib.sha256(fin_path.read_bytes()).hexdigest()}
    fin = json_from(read_own(fin_pin, out, stage + ' finish'), stage + ' finish')
    if not is_pin(arrays_pin) or {'path': fin.get('arrays_path'), 'sha256': fin.get('arrays_sha256')} != arrays_pin:
        raise Refused('FINAL_PASS_ROTATION_ARRAYS_MISMATCH', 'driver L5940: passes[-1].rotation_arrays = the finish pin')
    fuv = fin.get('uv_tail') or {}
    if fuv.get('stage_kind') != FINAL_ROTATION_KIND or not _hex(fuv.get('state_digest')):
        raise Refused('FINAL_ROTATION_TAIL_RECORD', 'finish uv_tail stage_kind %r' % fuv.get('stage_kind'))
    if (fuv.get('config') or {}).get('eps_certificate') != cert_pin:
        raise Refused('STAGE_EPS_PIN_NOT_THE_POINT_CERTIFICATE', 'finish uv_tail.config.eps_certificate')
    with np.load(io.BytesIO(read_own(arrays_pin, out, stage + ' arrays')), allow_pickle=False) as z:
        try:
            R, omega, fields = (np.array(z[k]) for k in ('radial_nodes_m', 'rotation_Omega_squared',
                                                          'full_fields_complex'))
        except KeyError as exc:
            raise Refused('ROTATION_ARRAYS_KEYS', str(exc))
    cm = fp.get('column_mean')
    if not isinstance(cm, dict) or cm.get('status') != COLUMN_MEAN_OK:
        raise Refused('COLUMN_MEAN_UNAVAILABLE', repr(cm))
    cm_pin = {'path': cm.get('path'), 'sha256': cm.get('sha256')}
    cmr = json_from(read_own(cm_pin, out, stage.replace('rotation', 'column_mean')), 'column mean')
    pred = cmr.get('prediction') or {}
    if cmr.get('status') != COLUMN_MEAN_OK or cmr.get('rotation_array_pin') != arrays_pin:
        raise Refused('COLUMN_MEAN_NOT_OF_THIS_ROTATION', 'column mean rotation_array_pin')
    rows = fp.get('rows')
    if not isinstance(rows, list) or pred.get('rows') != rows or ('rows' in res and res['rows'] != rows):
        raise Refused('FINAL_ROWS_NOT_THE_COLUMN_MEAN_ROWS')
    ids = [r.get('id') if isinstance(r, dict) else None for r in rows]
    if ids != list(query_ids):
        raise Refused('QUERY_ORDER_MISMATCH', 'the call own final rows differ from the values query_ids (no reorder)')
    valid, invalid = [], {}
    for r in rows:
        sp, vf = r.get('speed_km_s'), r.get('valid', True)
        if vf is True and _num(sp):
            valid.append(r['id'])
        elif vf is False and sp is None and isinstance(r.get('reason'), str):
            invalid[r['id']] = r['reason']
        else:
            raise Refused('ROW_STATE_INCONSISTENT', repr(r.get('id')))
    sup = pred.get('query_support')
    if not isinstance(sup, list) or [s.get('id') if isinstance(s, dict) else None for s in sup] != valid:
        raise Refused('QUERY_SUPPORT_NOT_THE_VALID_ROWS')
    radii = [s.get('radius_m') for s in sup]
    if not all(_num(x) and x > 0 for x in radii):
        raise Refused('ROW_RADII')
    pi, ri = pred.get('physical_inclination_rad'), pred.get('released_inclination_rad')
    factor = (math.sin(pi) / math.sin(ri)) if (_num(pi) and _num(ri) and math.sin(ri) != 0) else None
    return {'out': out, 'result_pin': result_pin, 'result_valid': res.get('valid'), 'final_pass': n, 'stage': stage,
            'finish_pin': fin_pin, 'finish_uv_tail': fuv, 'arrays_pin': arrays_pin, 'column_mean_pin': cm_pin, 'R': R, 'omega': omega,
            'fields': fields, 'valid_ids': valid, 'invalid': invalid, 'radii': radii,
            'support_columns': [s.get('column_indices') for s in sup],
            'inclination': {'physical_inclination_rad': pi, 'released_inclination_rad': ri,
                            'sin_ratio': factor, 'applied': False}}


def tail_state(lib, tail_pins, finish_uv, cert_pin):
    """The point's own field: TailState(record, arrays) with digest == the own stage finish uv_tail.state_digest."""
    import io
    import numpy as np
    if not isinstance(tail_pins, dict) or set(tail_pins) != {'record', 'arrays'}:
        raise Refused('TAIL_STATE_INPUT', 'tail_state = {record: pin, arrays: pin}')
    record = json_from(read_pinned(tail_pins['record'], 'tail state record'), 'tail state record')
    with np.load(io.BytesIO(read_pinned(tail_pins['arrays'], 'tail state arrays')), allow_pickle=False) as z:
        arrays = {k: z[k].copy() for k in z.files}
    try:
        st = lib.TailState.from_arrays(arrays, record, expected_digest=finish_uv['state_digest'])
    except lib.Refusal as exc:
        raise Refused('TAIL_STATE_NOT_THE_CALL_STATE', str(exc))
    if record.get('stage_kind') != FINAL_ROTATION_KIND or record.get('roster_digest') != finish_uv.get('roster_digest') \
            or record.get('config_sha256') != finish_uv.get('config_sha256'):
        raise Refused('TAIL_STATE_STAGE_SOURCE_OR_CONFIG_MISMATCH')
    if record.get('eps_certificate') != cert_pin:
        raise Refused('TAIL_STATE_DID_NOT_RUN_WITH_THE_POINT_CERTIFICATE', 'adapter c3v003 L434 analog')
    return st


# ------------------------------------------------------------------------------------------------ one point
def point_record(*, role, theta_key, query_ids, certificate, call_dir=None, tail_state_pins=None,
                 call_spec_sha256=None, log_index=None):
    check_query_ids(query_ids)
    if not _hex(theta_key):
        raise Refused('THETA_KEY', repr(theta_key))
    base = {'schema': RECORD_SCHEMA, 'module': MODULE, 'producer': self_pin(), 'role': role, 'theta_key': theta_key,
            'log_index': log_index, 'query_ids': list(query_ids), 'rule': RULE, 'alternatives_not_applied':
            list(ALTERNATIVES), 'never': NEVER, 'root_ruling': ROOT_RULING if ROOT_RULING else
            'PENDING (W-1, A115(b): A148 does not name srb_rot)'}
    if certificate is None:
        return dict(base, certificate=None, certificate_checks=None, eps_km_s=[None] * N_ROWS,
                    eps_row_reason=['NO_POINT_CERTIFICATE'] * N_ROWS,
                    note='A148: a point with no certificate gets none; A144 R3 flags the pair')
    lib, rowmod = modules()
    cert, checks = check_certificate(certificate, theta_key)
    co = call_outputs(call_dir, query_ids, certificate, call_spec_sha256)
    st = tail_state(lib, tail_state_pins, co['finish_uv_tail'], certificate)
    cov = coverage_on_state(st)
    fb = lib.field_bound(st, cert)
    try:
        rows = rowmod.rotation_rows(co['R'], co['omega'], co['fields'], co['radii'])
    except rowmod.Unavailable as exc:
        raise Refused('ROTATION_ROWS_UNAVAILABLE', str(exc))
    if rows['row_columns'] != co['support_columns']:
        raise Refused('ROW_COLUMNS_DIFFER_FROM_COLUMN_MEAN_SUPPORT')
    sr = lib.srb_rot(st, cert, dict(rows, tau_km_s=[INERT_TAU_KM_S] * len(co['radii'])))
    bound = sr['bound_km_s']
    if len(bound) != len(co['valid_ids']) or not all(_num(b) and b >= 0 for b in bound):
        raise Refused('BOUND_NOT_FINITE_NONNEGATIVE', repr(bound))
    by_id = dict(zip(co['valid_ids'], bound))
    eps = [float(by_id[q]) if q in by_id else None for q in query_ids]
    why = [None if q in by_id else 'ROW_INVALID_IN_CALL: ' + co['invalid'][q] for q in query_ids]
    return dict(base, certificate=dict(certificate), certificate_checks=checks, eps_km_s=eps, eps_row_reason=why,
                coverage=cov, state={'stage': co['stage'], 'final_pass': co['final_pass'],
                                     'state_digest': co['finish_uv_tail']['state_digest'],
                                     'record': dict(tail_state_pins['record']), 'arrays': dict(tail_state_pins['arrays']),
                                     'empty': bool(st.empty)},
                call={'result': co['result_pin'], 'result_valid': co['result_valid'], 'call_spec_sha256': call_spec_sha256,
                      'driver_sha256': DRIVER_SHA256,
                      'rotation_finish': co['finish_pin'], 'rotation_arrays': co['arrays_pin'],
                      'column_mean': co['column_mean_pin']},
                field_bound={'pin': {'path': LIBRARY[0], 'sha256': LIBRARY[1]}, 'function': 'field_bound L847-857',
                             'total': fb.get('total'), 'eps_per_shell': fb.get('eps'),
                             'shell_edges_inverse_kpc': fb.get('shell_edges_inverse_kpc')},
                srb_rot={'pin': {'path': LIBRARY[0], 'sha256': LIBRARY[1]}, 'function': 'srb_rot L860-871',
                         'bound_km_s_valid_rows': bound, 'tau_inert_km_s': INERT_TAU_KM_S,
                         'discarded': ['ratio_to_tau', 'pass_tau_over_10']},
                rows_input={'pin': {'path': ROW_PRODUCER[0], 'sha256': ROW_PRODUCER[1]},
                            'function': 'rotation_rows L171-193', 'row_ids': co['valid_ids'], 'row_radii_m': co['radii'],
                            'column_R_m': rows['column_R_m'], 'v_c_m_s': rows['v_c_m_s'],
                            'row_columns': rows['row_columns'], 'N_min': rows['N_min']},
                inclination=co['inclination'])


# ------------------------------------------------------------------------------------------------ values / members file
def attach_eps(doc, records, kind):
    """Copy each point's own eps_km_s into a PHASE1_NGC_VALUES_C2V001 document (Phase-1 values or Phase-2 members).
    One record per point, matched by theta key (and log_index for members); never overwrites; refuses unused records."""
    if ROOT_RULING is None:
        raise Refused('ROOT_RULING_PENDING', 'W-1 stop: A148 does not name srb_rot; root rules under A115(b) first')
    if kind not in ('phase1_values', 'phase2_members'):
        raise Refused('KIND', repr(kind))
    if not isinstance(doc, dict) or doc.get('schema') != VALUES_SCHEMA:
        raise Refused('VALUES_SCHEMA', repr(doc.get('schema') if isinstance(doc, dict) else None))
    qids = doc.get('query_ids')
    check_query_ids(qids)
    if not isinstance(records, list) or not all(isinstance(r, dict) and r.get('schema') == RECORD_SCHEMA for r in records):
        raise Refused('RECORDS')
    keys = [r.get('theta_key') for r in records]
    if len(set(keys)) != len(keys):
        raise Refused('RECORDS_DUPLICATE_THETA_KEY')
    by_key = {}
    for r in records:
        if r.get('query_ids') != qids:
            raise Refused('RECORD_QUERY_IDS', r.get('theta_key'))
        e, why = r.get('eps_km_s'), r.get('eps_row_reason')
        if not isinstance(e, list) or len(e) != N_ROWS or not isinstance(why, list) or len(why) != N_ROWS or not all(
                (x is None and w is not None) or (_num(x) and x >= 0 and w is None) for x, w in zip(e, why)):
            raise Refused('RECORD_EPS_SHAPE', r.get('theta_key'))
        c = r.get('certificate')
        if c is not None and ((r.get('certificate_checks') or {}).get('point_key') != r['theta_key'] or not is_pin(c)):
            raise Refused('RECORD_NOT_BOUND_TO_ITS_THETA', r.get('theta_key'))
        if c is None and any(x is not None for x in e):
            raise Refused('RECORD_VALUES_WITHOUT_CERTIFICATE', r.get('theta_key'))
        by_key[r['theta_key']] = r
    new = json.loads(json.dumps(doc))
    used = set()
    for p in new.get('points') or []:
        k = p.get('theta_key')
        if 'eps_km_s' in p:
            raise Refused('EPS_ALREADY_PRESENT', repr(k))
        if kind == 'phase2_members' and p.get('role') != 'member':
            raise Refused('MEMBERS_ROLE', repr(p.get('role')))
        r = by_key.get(k)
        if r is None:
            raise Refused('NO_RECORD_FOR_POINT', repr(k))
        if r.get('role') != p.get('role') or (kind == 'phase2_members' and r.get('log_index') != p.get('log_index')):
            raise Refused('RECORD_ROLE_OR_LOG_INDEX', repr(k))
        p['eps_km_s'] = list(r['eps_km_s'])
        p['eps_km_s_custody'] = {'record_sha256': digest(r), 'certificate': r.get('certificate'),
                                 'writer': r.get('producer'), 'root_ruling': ROOT_RULING}
        used.add(k)
    if used != set(by_key):
        raise Refused('RECORDS_UNUSED', sorted(set(by_key) - used)[:4])
    return new


def write_new(obj, out_dir, name):
    d = Path(out_dir)
    if not d.is_dir():
        raise Refused('OUT_DIR', str(d))
    p = d / name
    with open(p, 'xb') as f:
        f.write(json.dumps(obj, indent=1, sort_keys=True, allow_nan=False).encode() + b'\n')
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}


def main(argv=None):
    """CLI (python3 -I -B): point --args <json> --args-sha256 <sha> --out-dir <dir>; attach --doc .. --records ..
    Refused while ROOT_RULING is None (W-1 stop)."""
    if ROOT_RULING is None:
        print('REFUSED: ROOT_RULING_PENDING (W-1, A115(b): A148 does not name srb_rot)', flush=True)
        return 3
    if not (sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1):
        print('REFUSED: ISOLATED_INTERPRETER_REQUIRED (python3 -I -B)', flush=True)
        return 3
    import argparse
    ap = argparse.ArgumentParser(description=MODULE)
    ap.add_argument('cmd', choices=('point', 'attach'))
    ap.add_argument('--args', required=True)
    ap.add_argument('--args-sha256', required=True)
    ap.add_argument('--out-dir', required=True)
    a = ap.parse_args(argv)
    try:
        args = json_from(read_pinned({'path': os.path.abspath(a.args), 'sha256': a.args_sha256}, 'args'), 'args')
        if a.cmd == 'point':
            rec = point_record(**args)
            pin = write_new(rec, a.out_dir, 'POINT_EPS_KM_S_%s_C2V002.json' % rec['theta_key'][:16])
        else:
            doc = json_from(read_pinned(args['doc'], 'values doc'), 'values doc')
            recs = [json_from(read_pinned(p, 'eps record'), 'eps record') for p in args['records']]
            pin = write_new(attach_eps(doc, recs, args['kind']), a.out_dir, args['name'])
    except (Refused, ValueError, KeyError, TypeError, OSError) as exc:
        print('REFUSED: %s: %s' % (type(exc).__name__, exc), flush=True)
        return 3
    print(json.dumps(pin), flush=True)
    return 0


if __name__ == '__main__':
    for _k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
        os.environ[_k] = '1'
    sys.exit(main())

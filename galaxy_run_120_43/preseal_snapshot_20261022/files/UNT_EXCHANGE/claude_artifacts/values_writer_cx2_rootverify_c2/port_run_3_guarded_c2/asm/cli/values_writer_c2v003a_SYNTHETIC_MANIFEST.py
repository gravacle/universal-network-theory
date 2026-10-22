"""values_writer_c2v004_cx2v002 -- the Phase-1 values / Phase-2 members writer (V006 A152; A148; A144 R3). Codex2 build (A205 item 9).
Reviewer of record: Claude4 (lean; certificate-schema owner, did not build the writer). Nothing here is adopted until
root rules on this build and Claude4's review returns.

v004 = v003a (965ed282) plus A159/A211:
  (1) the reviewed NGC handoff c2v005 schema/sha pair is admitted;
  (2) every supplied acceptance record must carry the NGC per-state route;
  (3) Phase-1 valid[q] additionally requires ACCEPTED or LO_UNCERTIFIED_TRANSIENT.
The read whitelist now names the pinned NGC handoff instead of the DDO predecessor.
O-1 keeps ACCEPTED_PASS_FLAGGED ineligible. O-3 prints, without applying, the inclination factor.
A152's eps rule and section pin are unchanged. Source for schema and route is handoff L108/L112;
P-106 review prose is not the source of those constants.

v003 = values_writer_c2v002 (38ac8c93) plus, and only plus:
  (1) ROOT_RULING pinned to the A152 text: the V006 addendum path, the section 'A152', and the sha256 of the exact A152
      section bytes (from the line '## A152' to the byte before the next line that starts with '## '). The gate
      (check_root_ruling) re-reads those bytes before any attach, assemble or CLI run; a changed section refuses.
  (2) the W-3 assembler (assemble; CLI 'assemble'): from each point's own call (out/result.json + out/finish.json),
      its acceptance reading record (A134 Q2/Q5, A136 G5) and the values query_ids, it builds the
      PHASE1_NGC_VALUES_C2V001 document -- Phase-1 roles u_A, F0, F1, F2, or Phase-2 members with log_index -- with
      theta_key, speeds_km_s in query_ids order, valid and member_valid per W-3, result_pin per W-3 -- and then attaches
      eps_km_s per W-1 through attach_eps (one point record per point).
  (3) the W-3 eps rows: a row with speed None, or with v <= 0, gets eps None and keeps the call's reason (C-2). A call
      with no final rows gets 43 None with its status and reasons. v002 refused a point whose call recorded a
      nonpositive rotation square; v003 reads it as W-3 v <= 0 (43 None, the call's reason), and still refuses when the
      call's record and its own arrays disagree.
Everything else is v002's behaviour (W-1 rule, certificate check C-8 / W-4, state binding W-2 / C-4, custody C-5,
query order C-7, inert tau C-3, the inclination factor printed and not applied).

W-1 (ruled, V006 A152; the A146-adopted SRB-ROT adapter's own call, srb_rot_adapter_c3v003 08e9ac0a L439-440):
  eps_km_s[q] = srb_rot(S, C, rows)['bound_km_s'][q]   (owned_uv_tail_lapse_v002 2026f2b6, field_bound L847-857,
                                                        srb_rot L860-871)
  S    = the TailState of the call's own stage le{final_pass}_rotation (A134 reading point, V006 L525), bound by state
         digest == that stage's own finish.json uv_tail.state_digest; S.record.eps_certificate == the point EPS pin.
  C    = the point's own certificate, field 'eps' per unit shell.
  rows = rotation_rows (row_reference_producer_c2v003 67fddd24 L171-193) on the call's own rotation_base_arrays.npz;
         N_min, v_c, column radii and row_columns all computed from the call's own outputs; row radii are the call's
         own column-mean query_support[].radius_m (C-1).
  Not adopted (A152): A-1 v = speeds, A-2 R_q in place of the column maximum, A-3 a declared N_min.

W-3 (A152), result to values:
  speeds_km_s = the call's final rows (result.rows) in the values query_ids order, which must equal the row order (C-7);
  valid[q]     = row valid AND result.valid AND status COMPLETED; in Phase 1, also the NGC acceptance gate;
  member_valid = result.valid AND status COMPLETED AND the call's post-run per-state acceptance (A134 Q2/Q5, A136 G5)
                 reading in {ACCEPTED, LO_UNCERTIFIED_TRANSIENT} from the pinned G5 producer and exact NGC route;
  result_pin   = {out/result.json path, finish.result_sha256} (A138 V01(b)); finish.result_sha256 must equal the sha of
                 the result bytes read here.
"""
import hashlib
import importlib.util
import json
import math
import os
import re
import sys
from pathlib import Path

MODULE = 'values_writer_c2v004_cx2v002'
ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
LIBRARY = (ART + '/tail_scheme_impl_c2/driver_r5/module/owned_uv_tail_lapse_v002.py',
           '2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54')
ROW_PRODUCER = (ART + '/s4_acceptance_c2/acceptance_q2/row_reference_producer_c2v003.py',
                '67fddd24945de31d70f940cb1ff85ef9d467b20d62a764cd159f58afc909e01e')
DRIVER_SHA256 = '577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377'   # cx3r008 (A136, A141)
CERT_SCHEMAS = ('UNT_CLAUDE4_S0_POINT_EPS_C4V002',)                 # A148 / W-4 (a reviewed successor needs a writer successor)
CERT_PRODUCERS = ('8972822b5439e184297b4a5dbb552983ddb806804565ee1cc26691b680147235',)   # eps_ngc_point_c4v002 (A148)
CERT_COVERAGE = (2.0, 91.0)                                         # /kpc, A148
N_ROWS = 43                                                         # phase1 check_values / members_values n_rows
VALUES_SCHEMA = 'PHASE1_NGC_VALUES_C2V001'                          # phase1_c2v003 / v003a S_VALUES
RECORD_SCHEMA = 'UNT_POINT_EPS_KM_S_C2V003'
FINAL_ROTATION_KIND = 'le_rotation'                                 # driver L354 rotation_v005 -> le_rotation
COLUMN_MEAN_OK = 'CONDITIONAL_PREPARATION_ROWS_NOT_CALIBRATION'     # driver L5973
INERT_TAU_KM_S = 1.0
# (1) the root ruling: V006 A152, pinned by the sha256 of the section bytes (not the whole file, which grows)
V006 = ('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/'
        'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md')
ROOT_RULING = {'path': V006, 'section': 'A152',
               'sha256': '5aee4cc0f3ae64e5ea630d5a6459fdccc4cf2e3d55061d57e9214b1f002b074f'}
RULING_SCOPE = ('sha256 of the section bytes, from the line "## <section>" (followed by ":" or white space) to the byte '
                'before the next line that starts with "## " (end of file if none); the heading must be unique')
# (2) W-3 inputs
CALL_STATUSES = ('COMPLETED', 'COMPLETED_INVALID', 'REFUSED', 'BLOCKED', 'ROUTE_A_NO_FIXED_POINT', 'FAILED_AT_STAGE',
                 'FAILED')                                          # driver L6031, L6099-6114 (L9002, L9058-9073 clone)
PHASE1_ROLES = ('u_A', 'F0', 'F1', 'F2')                            # phase1 fdplan roles u_A and F%d (n_varying 3)
KINDS = ('phase1_values', 'phase2_members')
ACCEPTANCE_SCHEMAS = ('UNT_NGC_LO_ACCEPTANCE_RECORD_C2V005',)  # handoff c2v005 RECORD_SCHEMA L108 (A211)
ACCEPTANCE_HANDOFFS = ('7077ad9337d48b444bb724b3d0dca531e615bbb09656fa00ba453bacf2e634b1',)  # handoff c2v005 bytes (A211)
ACCEPTANCE_READINGS = ('NON_LAPSE_TAIL_MATERIAL', 'BOUND_INSUFFICIENT', 'UNDECIDABLE_FLAGGED', 'LO_UNCERTIFIED_TRANSIENT',
                       'INCOMPLETE', 'ACCEPTED_PASS_FLAGGED', 'ACCEPTED')            # handoff c2v004 READINGS (L78-85)
MEMBER_ACCEPTANCE_READINGS = ('ACCEPTED', 'LO_UNCERTIFIED_TRANSIENT')                 # W-3 (A152), as A134 allows
# A159/A211: schema and route from handoff c2v005 L108/L112; sha256 from its bytes.
NGC_ACCEPTANCE_ROUTE = 'NGC_POINT_RHO_POST_RUN_PER_STATE_LO_ACCEPTANCE'
MEMBER_ACCEPTANCE_PRODUCERS = (('UNT_NGC_LO_ACCEPTANCE_RECORD_C2V005', '7077ad9337d48b444bb724b3d0dca531e615bbb09656fa00ba453bacf2e634b1'),)
PRODUCER_GAP = ('NGC_ACCEPTANCE_PRODUCER_NOT_PINNED: the record schema/handoff pair is not the '
                'A211-adopted NGC per-state producer; no value is accepted from it')
MANIFEST = {'path': '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/'
                    'CODEX1/NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json',
            'sha256': 'a293651733ba2e6cff5e313d060521d8481bac39bf6f0af540d0108538535494'}   # driver NGC_DATA['manifest']
MANIFEST_SCHEMA = 'NGC3198_TARGET_FREE_QUERY_MANIFEST_V001'
KPC_M = 3.085677581491367e19                                        # driver L183 (radius_m = float(Rad_text) * KPC_M, L5215)
RADIUS_REL_TOL = 1e-9                                               # cross-check only (A152 C-1); the radii fed are the call's own
POINT_FIELDS = ('role', 'theta_key', 'log_index', 'call_dir', 'call_spec_sha256', 'certificate', 'tail_state_pins',
                'acceptance')
RULE = ('W-1 (ruled, V006 A152): eps_km_s[q] = owned_uv_tail_lapse_v002 srb_rot(S, C, rows)[bound_km_s][q]; '
        'S = the TailState at le{final_pass}_rotation of the point\'s own call (digest = own finish.json '
        'uv_tail.state_digest; record.eps_certificate = the point EPS pin); C = the point certificate, field eps per '
        'unit shell; rows = row_reference_producer_c2v003 rotation_rows on the own rotation_base_arrays.npz and the '
        'own row radii; tau inert (bound_km_s does not depend on it). W-3: a row with speed None or v <= 0 gets None '
        'with the call reason; a call with no final rows gets 43 None with its status.')
W3_RULE = ('W-3 (V006 A152): speeds_km_s = result.rows in the values query_ids order (must equal the call row order, '
           'C-7); valid[q] = row valid AND result.valid AND status COMPLETED, and in Phase 1 the NGC acceptance gate; member_valid = result.valid AND status '
           'COMPLETED AND the A136 G5 acceptance reading in {ACCEPTED, LO_UNCERTIFIED_TRANSIENT}, with the '
           'A211-pinned NGC schema/handoff pair and exact route; result_pin = {out/result.json '
           'path, finish.result_sha256} (A138 V01(b)); a row with speed None or v <= 0 gets eps None with the call '
           'reason (C-2)')
ALTERNATIVES = ('A-1 v = speeds_km_s[q] in place of v_c from rotation_Omega_squared (not adopted, A152)',
                'A-2 the bound at R_q in place of the max over the row columns (not adopted, A152)',
                'A-3 a declared N_min in place of min(1 + Re lapse) over full_fields_complex (not adopted, A152)',
                'A-4 multiply by sin(i_phys)/sin(i_released): A152 does not name it; W-1 "adds no new knob", so it is '
                'printed from the call own column-mean packet and never applied here')
NEVER = ('eps_max is never read or broadcast; no other point, call or state is read for this point; no NGC observed '
         'velocity, error or sigma is read; tau is inert; the query manifest is read for ids and radii only')


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
        _MODS['lib'] = load_exact(LIBRARY[0], LIBRARY[1], 'vw3_owned_uv_tail_lapse_v002')
        _MODS['rows'] = load_exact(ROW_PRODUCER[0], ROW_PRODUCER[1], 'vw3_row_reference_producer_c2v003')
    return _MODS['lib'], _MODS['rows']


def self_pin():
    p = os.path.abspath(__file__)
    return {'path': p, 'sha256': hashlib.sha256(Path(p).read_bytes()).hexdigest()}


def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


# ------------------------------------------------------------------------------------------------ (1) the root ruling
def ruling_section(raw, section):
    """The bytes of one '## <section>' entry of a decisions file (RULING_SCOPE)."""
    heads = [m.start() for m in re.finditer(rb'(?m)^## ' + re.escape(section.encode()) + rb'(?=[:\s])', raw)]
    if len(heads) != 1:
        raise Refused('ROOT_RULING_SECTION_NOT_UNIQUE', '%d headings "## %s"' % (len(heads), section))
    nxt = re.compile(rb'(?m)^## ').search(raw, heads[0] + 1)
    return raw[heads[0]:nxt.start() if nxt else len(raw)]


def check_root_ruling():
    """The W-1 gate, now pinned: re-read the ruling's section bytes and compare their sha256 with the pin."""
    r = ROOT_RULING
    if r is None:
        raise Refused('ROOT_RULING_PENDING', 'W-1 stop: no ruling pinned')
    if not isinstance(r, dict) or set(r) != {'path', 'section', 'sha256'} or not isinstance(r['path'], str) \
            or not os.path.isabs(r['path']) or not isinstance(r['section'], str) or not r['section'] or not _hex(r['sha256']):
        raise Refused('ROOT_RULING_INVALID', repr(r))
    try:
        raw = Path(r['path']).read_bytes()
    except OSError as exc:
        raise Refused('ROOT_RULING_UNREADABLE', str(exc))
    if hashlib.sha256(ruling_section(raw, r['section'])).hexdigest() != r['sha256']:
        raise Refused('ROOT_RULING_SECTION_MISMATCH', 'section %s of %s' % (r['section'], r['path']))
    return dict(r)


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


def read_call(call_dir, call_spec_sha256):
    """The call's own result and finish records (W-3): finish.result_sha256 == sha256 of the result bytes read here,
    finish.result_path is this out/result.json, status and valid agree, driver cx3r008, the point custody spec."""
    try:
        call = Path(call_dir).resolve(strict=True)
        out = (call / 'out').resolve(strict=True)
    except (OSError, TypeError) as exc:
        raise Refused('CALL_DIR', str(exc))
    try:
        rp = (out / 'result.json').resolve(strict=True)
        fp = (out / 'finish.json').resolve(strict=True)
        rraw, fraw = rp.read_bytes(), fp.read_bytes()
    except OSError as exc:
        raise Refused('CALL_RESULT_MISSING', str(exc))
    if not (rp.is_relative_to(out) and fp.is_relative_to(out)):
        raise Refused('OUTSIDE_OWN_CALL', 'result or finish')
    res, fin = json_from(rraw, 'result.json'), json_from(fraw, 'finish.json')
    if not isinstance(res, dict) or not isinstance(fin, dict):
        raise Refused('CALL_RECORD_NOT_AN_OBJECT')
    rsha = hashlib.sha256(rraw).hexdigest()
    if not _hex(fin.get('result_sha256')) or fin['result_sha256'] != rsha:
        raise Refused('FINISH_RESULT_SHA_MISMATCH', 'finish.result_sha256 %r != sha256(result.json) %s'
                      % (fin.get('result_sha256'), rsha))
    try:
        path_ok = Path(str(fin.get('result_path'))).resolve(strict=True) == rp
    except OSError:
        path_ok = False
    if not path_ok:
        raise Refused('FINISH_RESULT_PATH', repr(fin.get('result_path')))
    st, ok = fin.get('status'), fin.get('valid')
    if st not in CALL_STATUSES:
        raise Refused('CALL_STATUS_UNKNOWN', repr(st))
    if type(ok) is not bool or res.get('status') != st or res.get('valid') is not ok:
        raise Refused('FINISH_RESULT_INCONSISTENT', 'finish (%r, %r) vs result (%r, %r)' % (st, ok, res.get('status'),
                                                                                          res.get('valid')))
    if (st == 'COMPLETED' and ok is not True) or (st == 'COMPLETED_INVALID' and ok is not False):
        raise Refused('CALL_STATUS_VALID_INCONSISTENT', '%s with valid %r (driver L6099)' % (st, ok))
    if res.get('driver_sha256') != DRIVER_SHA256:
        raise Refused('DRIVER_NOT_CX3R008', repr(res.get('driver_sha256')))
    if not _hex(call_spec_sha256) or res.get('call_spec_sha256') != call_spec_sha256:
        raise Refused('CALL_SPEC_SHA', 'the call is not the point custody spec (A136 G3)')
    if (st in ('COMPLETED', 'COMPLETED_INVALID') or 'galaxy' in res) and res.get('galaxy') != 'NGC3198':
        raise Refused('CALL_GALAXY', repr(res.get('galaxy')))
    return {'call': call, 'out': out, 'res': res, 'fin': fin, 'status': st, 'valid': ok,
            'result_pin': {'path': str(rp), 'sha256': fin['result_sha256']},
            'finish_pin': {'path': str(fp), 'sha256': hashlib.sha256(fraw).hexdigest()}}


def final_rows(c, query_ids):
    """C-7 / W-3: the call's final rows (result.rows; the driver writes them only when the final column mean returned
    every row) in the values query_ids order -> (rows, [(row_valid, speed, reason)]); None if the call has no rows."""
    res = c['res']
    if 'rows' not in res:
        if c['status'] == 'COMPLETED':
            raise Refused('COMPLETED_WITHOUT_FINAL_ROWS')
        return None
    rows = res['rows']
    if not isinstance(rows, list) or len(rows) != N_ROWS or not all(isinstance(r, dict) for r in rows):
        raise Refused('FINAL_ROWS_SHAPE', '%d rows required' % N_ROWS)
    if [r.get('id') for r in rows] != list(query_ids):
        raise Refused('QUERY_ORDER_MISMATCH', 'the call own final rows differ from the values query_ids (no reorder)')
    states = []
    for r in rows:
        sp, vf = r.get('speed_km_s'), r.get('valid', True)
        if vf is True and _num(sp):
            states.append((True, sp, None))
        elif vf is False and sp is None and isinstance(r.get('reason'), str) and r['reason']:
            states.append((False, None, r['reason']))
        else:
            raise Refused('ROW_STATE_INCONSISTENT', repr(r.get('id')))
    if res.get('speeds_km_s') != {r['id']: r.get('speed_km_s') for r in rows}:
        raise Refused('SPEEDS_DICT_DIFFERS_FROM_ROWS', 'result.speeds_km_s (driver L6074) != result.rows')
    return rows, states


def call_outputs(c, query_ids, cert_pin):
    """The final-pass rotation stage, its arrays, and the call's own row radii, from <call>/out only."""
    import io
    import numpy as np
    out, res = c['out'], c['res']
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
    positive = fp.get('rotation_positive')
    if type(positive) is not bool or fin.get('positive_rotation_square') is not positive:
        raise Refused('ROTATION_POSITIVITY_UNRECORDED', 'passes[-1].rotation_positive = finish positive_rotation_square '
                                                        '(driver L5939)')
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
    if bool(np.all(omega > 0)) is not positive or (positive is False and c['valid'] is not False):
        raise Refused('ROTATION_POSITIVITY_INCONSISTENT', 'recorded %r; arrays all positive %r; call valid %r'
                      % (positive, bool(np.all(omega > 0)), c['valid']))
    cm = fp.get('column_mean')
    if not isinstance(cm, dict) or cm.get('status') != COLUMN_MEAN_OK:
        raise Refused('COLUMN_MEAN_UNAVAILABLE', repr(cm))
    cm_pin = {'path': cm.get('path'), 'sha256': cm.get('sha256')}
    cmr = json_from(read_own(cm_pin, out, stage.replace('rotation', 'column_mean')), 'column mean')
    pred = cmr.get('prediction') or {}
    if cmr.get('status') != COLUMN_MEAN_OK or cmr.get('rotation_array_pin') != arrays_pin:
        raise Refused('COLUMN_MEAN_NOT_OF_THIS_ROTATION', 'column mean rotation_array_pin')
    rows = fp.get('rows')
    if not isinstance(rows, list) or pred.get('rows') != rows or res.get('rows') != rows:
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
    return {'out': out, 'final_pass': n, 'stage': stage, 'rotation_positive': positive,
            'nonpositive_nodes': [int(i) for i in np.flatnonzero(np.min(omega, axis=1) <= 0)] if omega.ndim == 2 else None,
            'finish_pin': fin_pin, 'finish_uv_tail': fuv, 'arrays_pin': arrays_pin, 'column_mean_pin': cm_pin, 'R': R,
            'omega': omega, 'fields': fields, 'valid_ids': valid, 'invalid': invalid, 'radii': radii,
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
            list(ALTERNATIVES), 'never': NEVER, 'root_ruling': dict(ROOT_RULING) if ROOT_RULING else 'PENDING'}
    if certificate is None:
        return dict(base, certificate=None, certificate_checks=None, eps_km_s=[None] * N_ROWS,
                    eps_row_reason=['NO_POINT_CERTIFICATE'] * N_ROWS,
                    note='A148: a point with no certificate gets none; A144 R3 flags the pair')
    lib, rowmod = modules()
    cert, checks = check_certificate(certificate, theta_key)
    c = read_call(call_dir, call_spec_sha256)
    call = {'result': c['result_pin'], 'finish': c['finish_pin'], 'status': c['status'], 'result_valid': c['valid'],
            'call_spec_sha256': call_spec_sha256, 'driver_sha256': DRIVER_SHA256}
    fr = final_rows(c, query_ids)
    if fr is None:      # W-3: no final rows -> every speed is None -> every eps is None, with the call's status
        ns = c['res'].get('normalized_spec')
        if ns is not None and (not isinstance(ns, dict) or ((ns.get('numerics') or {}).get('uv_tail') or {}).get(
                'eps_certificate') != certificate):
            raise Refused('CALL_EPS_PIN_NOT_THE_POINT_CERTIFICATE', 'normalized_spec numerics.uv_tail.eps_certificate')
        why = 'CALL_HAS_NO_FINAL_ROWS (W-3, speed None): status %s; reasons: %s' % (
            c['status'], '; '.join(str(x) for x in (c['res'].get('reasons') or [])) or 'none recorded')
        return dict(base, certificate=dict(certificate), certificate_checks=checks, eps_km_s=[None] * N_ROWS,
                    eps_row_reason=[why] * N_ROWS, call=call, state=None)
    co = call_outputs(c, query_ids, certificate)
    call.update(rotation_finish=co['finish_pin'], rotation_arrays=co['arrays_pin'], column_mean=co['column_mean_pin'])
    if co['rotation_positive'] is False:   # W-3 v <= 0: the call's own final rotation square is nonpositive
        why = ('NONPOSITIVE_ROTATION_IN_CALL (W-3, v <= 0): min over z of rotation_Omega_squared <= 0 at radial nodes %s; '
               'call status %s; reasons: %s' % (co['nonpositive_nodes'], c['status'],
                                                '; '.join(str(x) for x in (c['res'].get('reasons') or [])) or 'none recorded'))
        return dict(base, certificate=dict(certificate), certificate_checks=checks, eps_km_s=[None] * N_ROWS,
                    eps_row_reason=[why] * N_ROWS, call=call, state=None, inclination=co['inclination'])
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
    speed = {r['id']: r['speed_km_s'] for r in fr[0]}
    eps, why = [], []
    for q in query_ids:
        if q not in by_id:
            eps.append(None)
            why.append('ROW_INVALID_IN_CALL: ' + co['invalid'][q])
        elif not speed[q] > 0:
            eps.append(None)
            why.append('ROW_SPEED_NONPOSITIVE_IN_CALL (W-3, v <= 0): speed_km_s %r' % (speed[q],))
        else:
            eps.append(float(by_id[q]))
            why.append(None)
    return dict(base, certificate=dict(certificate), certificate_checks=checks, eps_km_s=eps, eps_row_reason=why,
                coverage=cov, state={'stage': co['stage'], 'final_pass': co['final_pass'],
                                     'state_digest': co['finish_uv_tail']['state_digest'],
                                     'record': dict(tail_state_pins['record']), 'arrays': dict(tail_state_pins['arrays']),
                                     'empty': bool(st.empty)},
                call=call,
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
    ruling = check_root_ruling()
    if kind not in KINDS:
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
                                 'writer': r.get('producer'), 'root_ruling': ruling}
        used.add(k)
    if used != set(by_key):
        raise Refused('RECORDS_UNUSED', sorted(set(by_key) - used)[:4])
    return new


# ------------------------------------------------------------------------------------------------ (2) the W-3 assembler
def check_manifest(query_ids):
    """A152 C-1: the target-free query manifest, read-only, ids and radii only: its order must equal query_ids.
    Returns {query_id: radius_m} with radius_m = float(Rad_text) * KPC_M (driver L5215)."""
    m = json_from(read_pinned(MANIFEST, 'query manifest'), 'query manifest')
    if not isinstance(m, dict) or m.get('schema') != MANIFEST_SCHEMA or m.get('rad_unit') != 'kpc' \
            or not isinstance(m.get('rows'), list):
        raise Refused('MANIFEST_SCHEMA')
    try:
        ids = [r['query_id'] for r in m['rows']]
        rad = [float(r['Rad_text']) * KPC_M for r in m['rows']]
    except (KeyError, TypeError, ValueError) as exc:
        raise Refused('MANIFEST_ROWS', str(exc))
    if ids != list(query_ids):
        raise Refused('MANIFEST_ORDER_MISMATCH', 'values query_ids differ from the manifest order')
    return dict(zip(ids, rad))


def check_acceptance(pin, c):
    """The pinned NGC acceptance record and route, bound to this call's result and directory.
    A159 O-1: only ACCEPTED and LO_UNCERTIFIED_TRANSIENT count toward either acceptance gate."""
    rec = json_from(read_pinned(pin, 'acceptance record'), 'acceptance record')
    if not isinstance(rec, dict) or rec.get('schema') not in ACCEPTANCE_SCHEMAS:
        raise Refused('ACCEPTANCE_SCHEMA', repr(rec.get('schema') if isinstance(rec, dict) else None))
    h = rec.get('handoff')
    if not is_pin(h) or h['sha256'] not in ACCEPTANCE_HANDOFFS:
        raise Refused('ACCEPTANCE_PRODUCER_NOT_REVIEWED', repr(h))
    if rec.get('route') != NGC_ACCEPTANCE_ROUTE:
        raise Refused('ACCEPTANCE_ROUTE', repr(rec.get('route')))
    if rec.get('result') != c['result_pin'] or rec.get('call_dir') != str(c['call']):
        raise Refused('ACCEPTANCE_NOT_OF_THIS_CALL', 'acceptance result %r / call_dir %r' % (rec.get('result'),
                                                                                          rec.get('call_dir')))
    rd = rec.get('reading')
    if rd not in ACCEPTANCE_READINGS:
        raise Refused('ACCEPTANCE_READING_UNKNOWN', repr(rd))
    g5 = (rec['schema'], h['sha256']) in MEMBER_ACCEPTANCE_PRODUCERS
    return {'record': dict(pin), 'reading': rd, 'handoff': dict(h), 'g5_producer': g5,
            'counts_for_member_valid': g5 and rd in MEMBER_ACCEPTANCE_READINGS,
            'basis': None if g5 else PRODUCER_GAP}


def values_point(*, kind, role, theta_key, query_ids, call_dir, call_spec_sha256, log_index=None, acceptance=None):
    """One PHASE1_NGC_VALUES_C2V001 point per W-3, from the call's own result and finish records."""
    c = read_call(call_dir, call_spec_sha256)
    fr = final_rows(c, query_ids)
    if fr is None:
        speeds, row_valid, row_radius = [None] * N_ROWS, [False] * N_ROWS, {}
    else:
        speeds = [s for _v, s, _w in fr[1]]
        row_valid = [v for v, _s, _w in fr[1]]
        row_radius = {r['id']: r['radius_m'] for r in fr[0] if 'radius_m' in r}
    completed = c['status'] == 'COMPLETED'
    acc = check_acceptance(acceptance, c) if acceptance is not None else None
    p = {'role': role, 'theta_key': theta_key,
         'speeds_km_s': speeds,
         'valid': [bool(v is True and c['valid'] is True and completed
                        and (kind != 'phase1_values' or (acc is not None and acc['counts_for_member_valid'] is True)))
                   for v in row_valid],
         'result_pin': dict(c['result_pin']),
         'call': {'status': c['status'], 'result_valid': c['valid'], 'finish': c['finish_pin'],
                  'call_spec_sha256': call_spec_sha256, 'driver_sha256': DRIVER_SHA256,
                  'final_rows': 'result.rows' if fr is not None else 'NONE (no final rows; speeds None, valid false)'},
         'acceptance': acc}
    if kind == 'phase2_members':
        p['log_index'] = log_index
        p['member_valid'] = bool(c['valid'] is True and completed and acc is not None
                                 and acc['counts_for_member_valid'] is True)
        p['member_valid_basis'] = [w for ok, w in (
            (c['valid'] is True, 'CALL_NOT_VALID'), (completed, 'STATUS_NOT_COMPLETED: %s' % c['status']),
            (acc is not None, 'NO_ACCEPTANCE_RECORD'), (acc is None or acc['g5_producer'], PRODUCER_GAP),
            (acc is None or not acc['g5_producer'] or acc['reading'] in MEMBER_ACCEPTANCE_READINGS,
             'ACCEPTANCE_READING_NOT_ACCEPTED_OR_TRANSIENT: %s' % (acc or {}).get('reading'))) if not ok]
    return p, row_radius


def assemble(kind, query_ids, points):
    """W-3 then W-1: build the values (or members) document from each point's own call, then attach eps_km_s.
    Returns (document, [point records]). Every check fails closed; nothing is written here."""
    ruling = check_root_ruling()
    if kind not in KINDS:
        raise Refused('KIND', repr(kind))
    check_query_ids(query_ids)
    man = check_manifest(query_ids)
    if not isinstance(points, list) or not points or not all(isinstance(p, dict) for p in points):
        raise Refused('POINTS')
    for p in points:
        if not set(p) <= set(POINT_FIELDS) or not {'role', 'theta_key', 'call_dir', 'call_spec_sha256'} <= set(p):
            raise Refused('POINT_FIELDS', sorted(set(p) ^ set(POINT_FIELDS))[:6])
        if not _hex(p['theta_key']):
            raise Refused('THETA_KEY', repr(p['theta_key']))
    roles = [p['role'] for p in points]
    if kind == 'phase1_values':
        if sorted(roles) != sorted(PHASE1_ROLES) or any(p.get('log_index') is not None for p in points):
            raise Refused('PHASE1_ROLES', 'exactly %s, no log_index' % (PHASE1_ROLES,))
    else:
        lis = [p.get('log_index') for p in points]
        if any(r != 'member' for r in roles):
            raise Refused('MEMBERS_ROLE', repr(sorted(set(roles))))
        if not all(type(li) is int and li >= 0 for li in lis) or len(set(lis)) != len(lis):
            raise Refused('MEMBERS_LOG_INDEX', 'distinct nonnegative int log_index per member')
    if len({p['theta_key'] for p in points}) != len(points):
        raise Refused('THETA_KEY_DUPLICATE')
    vpts, recs, rad_diff = [], [], 0.0
    for p in points:
        li = p.get('log_index') if kind == 'phase2_members' else None
        vp, row_radius = values_point(kind=kind, role=p['role'], theta_key=p['theta_key'], query_ids=query_ids,
                                      call_dir=p['call_dir'], call_spec_sha256=p['call_spec_sha256'], log_index=li,
                                      acceptance=p.get('acceptance'))
        rec = point_record(role=p['role'], theta_key=p['theta_key'], query_ids=query_ids,
                           certificate=p.get('certificate'), call_dir=p['call_dir'],
                           tail_state_pins=p.get('tail_state_pins'), call_spec_sha256=p['call_spec_sha256'],
                           log_index=li)
        if rec.get('certificate') is not None and (rec.get('call') or {}).get('result') != vp['result_pin']:
            raise Refused('RESULT_CHANGED_DURING_ASSEMBLY', p['theta_key'])
        ri = rec.get('rows_input') or {}
        pairs = list(row_radius.items()) + list(zip(ri.get('row_ids') or [], ri.get('row_radii_m') or []))
        for q, r in pairs:
            d = abs(r - man[q]) / man[q] if _num(r) and man[q] > 0 else math.inf
            if not d <= RADIUS_REL_TOL:
                raise Refused('MANIFEST_RADIUS_MISMATCH', '%s: call radius %r vs manifest %r' % (q, r, man[q]))
            rad_diff = max(rad_diff, d)
        vpts.append(vp)
        recs.append(rec)
    doc = {'schema': VALUES_SCHEMA, 'query_ids': list(query_ids), 'points': vpts,
           'assembly': {'module': MODULE, 'writer': self_pin(), 'kind': kind, 'root_ruling': ruling, 'w3_rule': W3_RULE,
                        'manifest': {'pin': dict(MANIFEST), 'use': 'ids and radii cross-check only (A152 C-1)',
                                     'order_equal': True, 'max_rel_radius_difference': rad_diff,
                                     'tolerance': RADIUS_REL_TOL},
                        'eps_records': [{'theta_key': r['theta_key'], 'record_sha256': digest(r)} for r in recs]}}
    if kind == 'phase2_members':    # v003a (B1): the member_valid acceptance gate, printed
        doc['assembly']['member_valid_gate'] = {'producers': [list(x) for x in MEMBER_ACCEPTANCE_PRODUCERS],
                                                'route_required': NGC_ACCEPTANCE_ROUTE,
                                                'basis': None if MEMBER_ACCEPTANCE_PRODUCERS else PRODUCER_GAP}
    new = attach_eps(doc, recs, kind)
    for p in new['points']:
        for q in range(N_ROWS):
            s, e = p['speeds_km_s'][q], p['eps_km_s'][q]
            if e is not None and (s is None or not s > 0):
                raise Refused('EPS_WITHOUT_SPEED', '%s row %d (W-3: speed None or v <= 0 -> eps None)' % (p['theta_key'], q))
    return new, recs


def write_new(obj, out_dir, name):
    d = Path(out_dir)
    if not d.is_dir():
        raise Refused('OUT_DIR', str(d))
    p = d / name
    with open(p, 'xb') as f:
        f.write(json.dumps(obj, indent=1, sort_keys=True, allow_nan=False).encode() + b'\n')
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}


def main(argv=None):
    """CLI (python3 -I -B): point | attach | assemble --args <json> --args-sha256 <sha> --out-dir <dir>.
    assemble args: {kind, query_ids, points: [{role, theta_key, log_index?, call_dir, call_spec_sha256, certificate,
    tail_state_pins, acceptance}], name}; it writes each point record and then the values document (exclusive create)."""
    try:
        check_root_ruling()
    except Refused as exc:
        print('REFUSED: %s' % exc, flush=True)
        return 3
    if not (sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1):
        print('REFUSED: ISOLATED_INTERPRETER_REQUIRED (python3 -I -B)', flush=True)
        return 3
    import argparse
    ap = argparse.ArgumentParser(description=MODULE)
    ap.add_argument('cmd', choices=('point', 'attach', 'assemble'))
    ap.add_argument('--args', required=True)
    ap.add_argument('--args-sha256', required=True)
    ap.add_argument('--out-dir', required=True)
    a = ap.parse_args(argv)
    try:
        args = json_from(read_pinned({'path': os.path.abspath(a.args), 'sha256': a.args_sha256}, 'args'), 'args')
        if a.cmd == 'point':
            rec = point_record(**args)
            pin = write_new(rec, a.out_dir, 'POINT_EPS_KM_S_%s_C2V003.json' % rec['theta_key'][:16])
        elif a.cmd == 'attach':
            doc = json_from(read_pinned(args['doc'], 'values doc'), 'values doc')
            recs = [json_from(read_pinned(p, 'eps record'), 'eps record') for p in args['records']]
            pin = write_new(attach_eps(doc, recs, args['kind']), a.out_dir, args['name'])
        else:
            if set(args) != {'kind', 'query_ids', 'points', 'name'}:
                raise Refused('ASSEMBLE_ARGS', sorted(args))
            doc, recs = assemble(args['kind'], args['query_ids'], args['points'])
            rpins = [write_new(r, a.out_dir, 'POINT_EPS_KM_S_%s_C2V003.json' % r['theta_key'][:16]) for r in recs]
            pin = dict(write_new(doc, a.out_dir, args['name']), records=rpins)
    except (Refused, ValueError, KeyError, TypeError, OSError) as exc:
        print('REFUSED: %s: %s' % (type(exc).__name__, exc), flush=True)
        return 3
    print(json.dumps(pin), flush=True)
    return 0


MANIFEST = {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/values_writer_cx2_rootverify_c2/port_run_3_guarded_c2/asm/manifest.json', 'sha256': '0ab1bf541390a70a3e52ffbd11001aa32faac4f4703b490d079184ea81e84023'}  # TEST COPY ONLY
ROOT_RULING = {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/values_writer_cx2_rootverify_c2/port_run_3_guarded_c2/DECISIONS_A152_ONLY.md', 'section': 'A152', 'sha256': '5aee4cc0f3ae64e5ea630d5a6459fdccc4cf2e3d55061d57e9214b1f002b074f'}  # TEST COPY ONLY

if __name__ == '__main__':
    for _k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
        os.environ[_k] = '1'
    sys.exit(main())

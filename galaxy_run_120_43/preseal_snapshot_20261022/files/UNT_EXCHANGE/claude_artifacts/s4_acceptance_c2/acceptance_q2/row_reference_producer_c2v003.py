"""Q2 acceptance input side, part 2 (A134; rulings 56774ba7 Q2, Q4, Q10; reading points frozen in FROM_CODEX/0690):
per-state row-reference records, and the SRB-ROT rows input for the accepted final-rotation state.

Emits UNT_POINT_LO_ROWS_CX2V001, the `row_reference` that lo_core_r5_cx2v001 (12d36305) produce_current_lo reads
(L219-231; row_values L64-78). lo_core checks row order, R_i, tau_i and the row contract sha against the point's
custody, requires this producer's sha in trusted_source_producers, and requires an APPROVED row-policy review for the
row contract (one per D, Q4). This module computes only the per-row speed scale |v_i| by the Q4(a) rule:

  |v_i| = max over every readout of row i that the call itself recorded. Never observed DDO154 speeds, another
  point's or another call's speeds. A row with no recorded readout makes the record UNAVAILABLE; nothing is
  substituted.

Readout set (0690 OPEN-1, frozen in A134): every Picard-pass row result.passes[*].rows[i].speed_km_s, at call
geometry (driver r5 L3209, L3247, L3259, L3588). Not read: result.identity.route_a.route_a_rows, which the driver labels
"NOT AT CALL GEOMETRY ... diagnostic only" (L1608), and result.rows, the final pass's rows copied (L3532).
Entries whose speed is null (driver c2v006 N1 invalid rows) are not readouts and are skipped.
tau_i = 0.25 sigma_i comes unchanged from the row contract (prereg V005, inside row_contract_sha256; Q4(c)).
The record carries speed_reference_policy = A134_Q4A_OWN_CALL_MAX_ABS_OVER_EVERY_RECORDED_READOUT (0690 OPEN-9;
the field Claude3's per-state adapter c3v001 requires).
v003 (A138 V01(b)): the record also carries state_files = [the call's own out/result.json pin], the archive its
readouts come from (lo_producer_cx2v004 L71-78, re-applied by Claude3's adapter c3v002 as F6, which reads it from
bytes inside the run root). That pin is the record's call_result; without an exact pin no record is written.

SRB-ROT rows input (Q10; 0690 OPEN-3; Claude3 INTERFACE_C3V001 OPEN-10/11, schema S4RC1_SRB_ROT_ROWS_INPUT_C3V001):
the target is the unique own_source_state at stage le{final_pass}_rotation (stage_kind le_rotation). column_R_m,
v_c_m_s, row_columns and N_min are read from that stage's own rotation_base_arrays.npz (rotation_v005 stage L293-301) by the
V007 SRB_ROT producer's rule (srb_rot_record_cx1v008_cx3v001 row_contract, L43-63), with row radii from the row
contract (custody L120: the per-call binding query_rows). Nothing is computed here beyond that extraction.
"""
import bisect
import hashlib
import io
import json
import math
from pathlib import Path

import numpy as np

SCHEMA = 'UNT_POINT_LO_ROWS_CX2V001'
READOUT_FIELDS = ('passes[*].rows',)
SPEED_REFERENCE_POLICY = 'A134_Q4A_OWN_CALL_MAX_ABS_OVER_EVERY_RECORDED_READOUT'
SPEED_POLICY = ('A134 Q4(a), readout set frozen in 0690 OPEN-1: |v_i| = max over every Picard-pass readout '
                'passes[*].rows[i].speed_km_s recorded by this call at call geometry (null speeds skipped); '
                'identity.route_a.route_a_rows (diagnostic, not at call geometry) and the copied final rows are not read; '
                'no observed, other-point or other-call speed; a row with no recorded readout is UNAVAILABLE. '
                'tau_i from the row contract (prereg V005, Q4(c)).')
SRB_ROWS_SCHEMA = 'S4RC1_SRB_ROT_ROWS_INPUT_C3V001'        # srb_rot_adapter_c3v001 L57
FINAL_ROTATION_KIND = 'le_rotation'                        # execution_graph v002 L42-45 (rotation_v005)
LAPSE_REALITY_ATOL = 1e-12                                 # srb_rot_record_cx1v008_cx3v001 L49
SRB_ROWS_RULE = ('V007 SRB_ROT producer row_contract (srb_rot_record_cx1v008_cx3v001 L43-63) on this call\'s own '
                 'le{final_pass}_rotation arrays: column_R_m = radial_nodes_m; v_c_m_s = R*sqrt(min over vertical nodes '
                 'of rotation_Omega_squared); N_min = min(1 + Re lapse) over full_fields_complex[...,0]; row_columns = '
                 'the node equal to the row radius, else the two bracketing nodes; row radii from the row contract.')
INCLINATION_NOTE = ('NOT APPLIED HERE: V007 multiplied the library bound by sin(i_physical)/sin(i_released) '
                    '(srb_rot_record_cx1v008_cx3v001 L60-61, L106); the rows input carries no factor.')


class Unavailable(ValueError):
    pass


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()


def pin(path):
    p = Path(path)
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}


def _hex(x):
    return isinstance(x, str) and len(x) == 64 and all(c in '0123456789abcdef' for c in x)


def recorded_readouts(result):
    """Every (id, speed) Picard-pass readout the call recorded, by pass (0690 OPEN-1)."""
    groups = []
    for p in result.get('passes') or []:
        groups.append(('passes[%s].rows' % p.get('pass'), p.get('rows')))
    out = []
    for field, rows in groups:
        if not isinstance(rows, list):
            continue
        for r in rows:
            if not isinstance(r, dict) or r.get('speed_km_s') is None:
                continue
            v = r['speed_km_s']
            if type(v) not in (int, float) or not math.isfinite(v):
                raise Unavailable('NONFINITE_RECORDED_READOUT: %s %r' % (field, r.get('id')))
            out.append((r.get('id'), float(v), field))
    return out


def row_speeds(result, ids):
    got = {i: [] for i in ids}
    counts = {}
    for rid, v, field in recorded_readouts(result):
        if rid in got:
            got[rid].append(abs(v))
            counts[field] = counts.get(field, 0) + 1
    missing = [i for i in ids if not got[i]]
    if missing:
        raise Unavailable('ROW_READOUT_UNAVAILABLE: ' + ','.join(map(str, missing)))
    return [max(got[i]) for i in ids], counts


def row_reference(*, state, row_contract, row_contract_sha256, result, result_ref, policy_review):
    """One record per consumed state; every state of a call carries the same call-level |v_i|."""
    if not isinstance(state, dict) or set(state) != {'state_sha256', 'source_sha256', 'stage_kind', 'nonnegative_masses'} \
            or not _hex(state['state_sha256']):
        raise ValueError('STATE_IDENTITY_REQUIRED')
    if digest(row_contract) != row_contract_sha256:
        raise ValueError('ROW_CONTRACT_DIGEST_MISMATCH')
    if not isinstance(result_ref, dict) or set(result_ref) != {'path', 'sha256'} or not isinstance(result_ref['path'], str) \
            or not _hex(result_ref['sha256']):
        raise ValueError('STATE_FILES_CALL_RESULT_PIN_REQUIRED')        # v003: A138 V01(b)
    ids = [r['id'] for r in row_contract['rows']]
    radii = [r['radius_m'] for r in row_contract['rows']]
    tau = list(row_contract['tau_km_s'])
    if len(set(ids)) != len(ids) or len(tau) != len(ids):
        raise ValueError('ROW_CONTRACT_SHAPE')
    speeds, counts = row_speeds(result, ids)
    return {'schema': SCHEMA, 'state_sha256': state['state_sha256'], 'state': state,
            'row_ids': ids, 'row_contract_sha256': row_contract_sha256, 'R_m': radii, 'tau_km_s': tau,
            'v_reference_km_s': speeds, 'speed_policy': SPEED_POLICY, 'speed_reference_policy': SPEED_REFERENCE_POLICY,
            'readout_fields': list(READOUT_FIELDS),
            'readout_counts': counts, 'call_result': result_ref, 'policy_review': policy_review,
            'state_files': [dict(result_ref)],                               # v003: A138 V01(b); lo_producer v004 L71-78
            'producer': pin(__file__)}


def final_rotation_target(inventory, result):
    """0690 OPEN-3: the unique own_source_state at stage le{final_pass}_rotation, stage_kind le_rotation, taken from
    the v010 inventory (occurrences joined to states by ordinal). Returns (state, stage, occurrence)."""
    n, passes = result.get('final_pass'), result.get('passes')
    if type(n) is not int or n < 1 or not isinstance(passes, list) or len(passes) != n \
            or not isinstance(passes[-1], dict) or passes[-1].get('pass') != n:
        raise Unavailable('FINAL_PASS_UNAVAILABLE')
    stage = 'le%d_rotation' % n
    hits = [o for o in inventory.get('occurrences') or [] if isinstance(o, dict) and o.get('role') == 'own_source_state'
            and o.get('stage') == stage and o.get('stage_kind') == FINAL_ROTATION_KIND]
    if len(hits) != 1:
        raise Unavailable('FINAL_ROTATION_STATE_NOT_UNIQUE_IN_INVENTORY: ' + stage)
    js = [j for j in inventory.get('joined_occurrences') or [] if isinstance(j, dict) and j.get('ordinal') == hits[0].get('ordinal')]
    if len(js) != 1 or not isinstance(js[0].get('state'), dict):
        raise Unavailable('FINAL_ROTATION_STATE_NOT_JOINED')
    st = js[0]['state']
    if st not in (inventory.get('states') or []) or st.get('stage_kind') != FINAL_ROTATION_KIND \
            or st.get('state_sha256') != hits[0].get('state_sha256_claimed'):
        raise Unavailable('FINAL_ROTATION_STATE_INCONSISTENT')
    return st, stage, hits[0]


def _own_bytes(ref, out, where):
    """Own-call bytes only: the file resolves inside <call>/out and matches its pin."""
    if not isinstance(ref, dict) or set(ref) != {'path', 'sha256'}:
        raise Unavailable('OWN_CALL_REFERENCE_INVALID: ' + where)
    p = Path(ref['path']).resolve(strict=True)
    if not p.is_relative_to(out):
        raise Unavailable('FINAL_ROTATION_RECORD_OUTSIDE_OWN_CALL: ' + where)
    raw = p.read_bytes()
    if hashlib.sha256(raw).hexdigest() != ref['sha256']:
        raise Unavailable('OWN_CALL_PIN_MISMATCH: ' + where)
    return raw


def rotation_rows(R, omega, fields, radii):
    """The V007 rule, unchanged in substance (srb_rot_record_cx1v008_cx3v001 L44-59): checks, v_c, N_min, columns."""
    R, omega, fields = np.asarray(R), np.asarray(omega), np.asarray(fields)
    if R.ndim != 1 or len(R) < 2 or not np.all(np.isfinite(R)) or np.any(R <= 0) or np.any(np.diff(R) <= 0):
        raise Unavailable('RADIAL_GRID')
    if omega.ndim != 2 or omega.shape[0] != len(R) or not np.all(np.isfinite(omega)) or np.any(omega <= 0):
        raise Unavailable('POSITIVE_ROTATION_SQUARE')
    if fields.ndim != 4 or fields.shape[0] != len(R) or fields.shape[2] != omega.shape[1] or fields.shape[3] != 10 \
            or not np.all(np.isfinite(fields)):
        raise Unavailable('FULL_FIELDS_SHAPE')
    if np.max(np.abs(fields[..., 0].imag)) > LAPSE_REALITY_ATOL:
        raise Unavailable('LAPSE_REALITY')
    n_min = float(np.min(1 + fields[..., 0].real))
    if not n_min > 0:
        raise Unavailable('POSITIVE_LAPSE')
    v = R * np.sqrt(np.min(omega, axis=1))
    columns = []
    for q in radii:
        if type(q) not in (int, float) or not math.isfinite(q) or q < R[0] or q > R[-1]:
            raise Unavailable('ROW_OUTSIDE_RADIAL_SUPPORT')
        j = bisect.bisect_left(R, q)
        columns.append([j] if j < len(R) and R[j] == q else [j - 1, j])
    return {'column_R_m': R.tolist(), 'v_c_m_s': v.tolist(), 'row_columns': columns, 'N_min': n_min}


def srb_rot_rows_input(*, state, inventory, row_contract, row_contract_sha256, result, result_ref, call_dir):
    """S4RC1_SRB_ROT_ROWS_INPUT_C3V001 for the accepted final-rotation state, from the call's own outputs only."""
    if digest(row_contract) != row_contract_sha256:
        raise ValueError('ROW_CONTRACT_DIGEST_MISMATCH')
    target, stage, occ = final_rotation_target(inventory, result)
    if state != target:
        raise Unavailable('SRB_ROT_FINAL_ROTATION_STATE_ONLY')
    out = Path(call_dir).resolve(strict=True) / 'out'
    fin_ref = occ.get('evidence')                      # the stage's finish.json pin (discovery; v010 ROLES stage_tail)
    fin = json.loads(_own_bytes(fin_ref, out, stage + ' finish'))
    if (fin.get('uv_tail') or {}).get('state_digest') != state['state_sha256']:
        raise Unavailable('FINAL_ROTATION_FINISH_STATE_MISMATCH')
    arrays_ref = {'path': fin.get('arrays_path'), 'sha256': fin.get('arrays_sha256')}
    if result['passes'][-1].get('rotation_arrays') != arrays_ref:   # driver L3214: the final pass's rotation arrays
        raise Unavailable('FINAL_PASS_ROTATION_ARRAYS_MISMATCH')
    with np.load(io.BytesIO(_own_bytes(arrays_ref, out, stage + ' arrays')), allow_pickle=False) as z:
        R, omega, fields = (np.array(z[k]) for k in ('radial_nodes_m', 'rotation_Omega_squared', 'full_fields_complex'))
    ids = [r['id'] for r in row_contract['rows']]
    tau = list(row_contract['tau_km_s'])
    if len(set(ids)) != len(ids) or len(tau) != len(ids):
        raise ValueError('ROW_CONTRACT_SHAPE')
    rows = rotation_rows(R, omega, fields, [r['radius_m'] for r in row_contract['rows']])
    return dict({'schema': SRB_ROWS_SCHEMA, 'state': state, 'call_result': result_ref, 'producer': pin(__file__),
                 'row_ids': ids, 'row_contract_sha256': row_contract_sha256, 'tau_km_s': tau},
                **rows, provenance={'rule': SRB_ROWS_RULE, 'final_pass': result['final_pass'], 'stage': stage,
                                    'rotation_finish': fin_ref, 'rotation_arrays': arrays_ref,
                                    'row_radii': 'row contract rows[].radius_m (custody L120)',
                                    'inclination_factor': INCLINATION_NOTE})

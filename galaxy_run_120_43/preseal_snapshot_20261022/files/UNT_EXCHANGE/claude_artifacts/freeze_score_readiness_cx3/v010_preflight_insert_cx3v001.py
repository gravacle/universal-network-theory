# Synthetic-tested v010 freeze boundary; not a science or certificate acceptance gate.
def _v010_preflight(result, ids):
    reasons, hits = [], []
    _safe_scan(result, 'forward_ngc_result', hits, reasons)
    if hits:
        reasons.append('V010_TARGET_FIELD_REFUSED: ' + ', '.join(hits[:8]))
    # Recognise spellings that the older exact-name screen did not cover.
    stack = [result]
    seen = set()
    while stack:
        obj = stack.pop()
        if isinstance(obj, (dict, list, tuple)):
            if id(obj) in seen:
                continue
            seen.add(id(obj))
        if isinstance(obj, dict):
            for key, value in obj.items():
                norm = ''.join(c for c in str(key).lower() if c.isalnum())
                if ('target' in norm or norm.startswith('observed') or norm.startswith('vobs')):
                    reasons.append('V010_TARGET_FIELD_REFUSED: key ' + str(key))
                stack.append(value)
        elif isinstance(obj, (list, tuple)):
            stack.extend(obj)
    if reasons or not isinstance(result, dict) or result.get('valid') is not True:
        return reasons
    if result.get('schema') != 'UNT_GALAXY_M0_FORWARD_RESULT_C2V001':
        reasons.append('V010_RESULT_SCHEMA_REQUIRED')
    if result.get('galaxy') != 'NGC3198' or result.get('status') != 'COMPLETED':
        reasons.append('V010_NGC_COMPLETED_REQUIRED')
    if result.get('scored') is not False:
        reasons.append('V010_UNSCORED_REQUIRED')
    for key in ('driver_sha256', 'call_spec_sha256'):
        if not _is_hex64(result.get(key)):
            reasons.append('V010_RESULT_PIN_REQUIRED: ' + key)
    rows = result.get('rows')
    speeds = result.get('speeds_km_s')
    if not isinstance(rows, list) or len(rows) != N_QUERIES:
        reasons.append('V010_EXACTLY_43_ROWS_REQUIRED')
    elif [r.get('id') if isinstance(r, dict) else None for r in rows] != list(ids):
        reasons.append('V010_QUERY_ORDER_OR_DUPLICATE_REFUSED')
    elif not isinstance(speeds, dict) or set(speeds) != set(ids):
        reasons.append('V010_EXACT_SPEED_MAP_REQUIRED')
    else:
        for row in rows:
            q = row['id']
            if row.get('valid') is not True or row.get('reason') not in (None, ''):
                reasons.append('V010_INVALID_QUERY_REFUSED: ' + q)
            if not _is_real(row.get('speed_km_s')) or not _is_real(speeds.get(q)) or row['speed_km_s'] != speeds[q]:
                reasons.append('V010_ROW_SPEED_MAP_DISAGREEMENT: ' + q)
    if result.get('invalid_rows', []) != []:
        reasons.append('V010_INVALID_QUERY_ROSTER_REFUSED')
    ra = result.get('route_a_outcome') or {}
    if ra.get('classification') != 'CONVERGED' or ra.get('converged_finite_fixed_point') is not True:
        reasons.append('V010_ROUTE_A_CONVERGENCE_REQUIRED')
    ro = ra.get('ro1') or {}
    if ro.get('rule') != 'RO1' or ro.get('armed') is not True or type(ro.get('fired')) is not bool:
        reasons.append('V010_RO1_ARMED_REQUIRED')
    if not _is_hex64(ro.get('worker_sha256')) or not _is_hex64(ro.get('binding_sha256')):
        reasons.append('V010_RO1_PINS_REQUIRED')
    events = ro.get('events')
    if not isinstance(events, list) or bool(events) != bool(ro.get('fired')) or 'inadmissible_record' in ro:
        reasons.append('V010_RO1_EVENT_CONSISTENCY_REQUIRED')
    elif ro.get('fired'):
        if len(events) != 1 or events[0].get('code') != 'ROUTE_A_READOUT_NO_CIRCULAR_BRANCH' or events[0].get('after_convergence') is not True or events[0].get('refusal') not in (
                'NO_SUBLUMINAL_CIRCULAR_PRESSURE_BRANCH',
                'DEGENERATE_RADIAL_EULER: zero exact denominator; no unique speed', 'NON_TIMELIKE_COLUMN'):
            reasons.append('V010_RO1_EVENT_REFUSED')
    u = result.get('uv_tail') or {}
    if u.get('schema') != 'UNT_GALAXY_M0_FORWARD_UV_TAIL_C2V010' or u.get('enabled') is not True:
        reasons.append('V010_TAIL_RECORD_REQUIRED')
    if u.get('admissibility') != 'production' or u.get('pending_certificates') != []:
        reasons.append('V010_TAIL_CERTIFICATE_SLOTS_UNFILLED')
    rule = u.get('source_rule')
    if rule not in ('continuum_v001', 'nodes_v001'):
        reasons.append('V010_SOURCE_RULE_REFUSED')
    if rule == 'continuum_v001' and u.get('nodes_ext_context') is not None:
        reasons.append('V010_CONTINUUM_NODES_CONTEXT_REFUSED')
    if rule == 'nodes_v001' and not isinstance(u.get('nodes_ext_context'), dict):
        reasons.append('V010_NODES_CONTEXT_REQUIRED')
    if not _is_hex64((u.get('config') or {}).get('normalized_sha256')):
        reasons.append('V010_TAIL_CONFIG_PIN_REQUIRED')
    stages = u.get('stage_records')
    if not isinstance(stages, list) or not stages:
        reasons.append('V010_TAIL_STAGE_RECORDS_REQUIRED')
    else:
        for stage in stages:
            if not isinstance(stage, dict) or not _is_hex64(stage.get('finish_sha256')) or not _is_hex64(stage.get('state_digest')) or stage.get('production_admissible') is not True or stage.get('test_only_admitted') is True:
                reasons.append('V010_TAIL_STAGE_CUSTODY_REFUSED')
                break
    # The raw result and its provenance must be separately pinned in input_files.
    # This boundary checks schema and fail-closed consumption; it does not certify physics,
    # authenticate the producer, or infer adoption from synthetically populated certificates.
    return reasons



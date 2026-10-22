"""Structural root-record checks from INPUT_CONTRACTS_C4V004; no semantic admission."""
CONTRACTS = {
 'phase_inputs': ('PHASE_INPUTS_C4V001', 'schema phase_named phase1_registry_root phase2_registry_root run_status run_status_code phase1_header phase1_classification_absent_reason'),
 'gate_status_list': ('GATE_STATUS_LIST_C4V001', 'schema gates'),
 'tsr_flag_record': ('TSR_FLAG_RECORD_C4V001', 'schema target_free rule failing_ring_ordinal ntest_compare_pin n1_record_pin gl_node_record_pin flags'),
 'stage0_status': ('STAGE0_STATUS_RECORD_C4V003', 'schema phase sealed_successor step4_start_utc members rule_a_receipts_finished rule_b_successor_sealed receipts_before_step4 receipt_refusals evaluation_refusals reading reasons post_score_exploratory'),
 'commitment_status': ('PHASE2_COMMITMENT_STATUS_C4V001', 'schema status stops_or_changes'),
 'field_map': ('KEY_FIELD_MAP_C4V001', 'schema renames'),
}

def shape_ok(role, value):
    if not isinstance(value, dict):
        return False
    if role == 'root_disclosures':
        return True
    if role == 'fallback':
        return value.get('schema') == 'FALLBACK_RECORD_C4V001' and type(value.get('applies')) is bool
    if role not in CONTRACTS:
        raise ValueError('unsupported root record role')
    schema, keys = CONTRACTS[role]
    return value.get('schema') == schema and set(value) == set(keys.split())

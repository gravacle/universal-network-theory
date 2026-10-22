"""SOURCE ONLY. Fixed 11 positive/null/partial cases and four refusals.
Root injects pinned0305 cost module C and0306 exact read module R, and durable
PRE/RETURN callback. No original/native trajectory or author execution.
"""
from fractions import Fraction as F
import struct


def small_table(reads):
    return {'active_dimension': 1, 'E_bias': '7/4', 'signed_bias_threshold': '1/128',
            'required_halfwidth': '1/4096', 'reads': reads}


def definition(weight, norm, kind, lower=None, upper=None):
    return {'weights_numerator_over_14': [weight], 'operator_norm_upper': str(norm),
            'global_range': [str(-norm if lower is None else lower), str(norm if upper is None else upper)],
            'commutator_norm_upper': '0', 'kind': kind, 'exact_operator_null': norm == 0}


def controls(C, R, audit):
    if not callable(audit):
        raise ValueError('durable fixed audit callback required')
    S = 1 << 80
    registry = {row['name']: row for row in C.unitary_registry()}
    partial = {row['name']: row for row in C.partial_registry()}
    cases = {}
    checks = {}
    specifications = [
        ('old_edge_blank_negative', (0, 0, 1, 0, 0, 1), 'old_edge_flip_e0', F(-1, 14)),
        ('old_edge_written_positive', (0, 0, 1, 1, 0, 1), 'old_edge_flip_e0', F(1, 14)),
        ('own_record_reversal', (0, 3, 1, 3, 0, 1), 'record_flip_v0', F(5, 7)),
        ('other_record_null', (0, 3, 1, 3, 0, 1), 'record_flip_v1', F(0)),
        ('outgoing_Q_carrier_null', (0, 3, 1, 3, 0, 1), 'carrier_flip_v1', F(0)),
        ('degree_preserving_swap_null', (0, 1, 1, 0, 0, 1), 'old_parallel_swap_e0_e1', F(0)),
        ('Born_other_endpoint_null', (1, 0, 1, 0, 0, 1), 'born_edge_flip_e1', F(0)),
    ]
    for name, state, op_name, expected in specifications:
        operation = registry[op_name]
        audit('PRE', name, {'state': list(state), 'operation': operation, 'probe': 0,
                            'center': [[S, 0]], 'L2_error': '0', 'reference_bias': str(expected)})
        target, phase = C.apply_unitary(state, operation)
        before = C.cost_numerators(state)[0]
        after = C.cost_numerators(target)[0]
        norm = C.bias_norm(operation, 0)
        table = small_table({'baseline': definition(before, F(1, 2), 'ABSOLUTE_COST_OVER_EBIAS'),
                             'after': definition(after, F(1, 2), 'UNITARY_ABSOLUTE_TARGET_COST'),
                             'bias': definition(after-before, norm, 'UNITARY_SIGNED_COST_BIAS')})
        value = R.evaluate(table, [(S, 0)], F(0))
        answer = {'target_state': list(target), 'phase': phase,
                  'target_Q': C.pop(target[2])+C.pop(target[4]), 'table': table,
                  'read': value, 'reference_bias': str(expected),
                  'reference_matches': F(value['all_reads']['bias']['center_expectation']) == expected}
        audit('RETURN', name, answer)
        cases[name] = answer
        checks[name] = answer['reference_matches']
    for name, state, op_name, expected_raw, expected_success in [
        ('eligible_Birth_event_null', (0, 3, 1, 3, 0, 1), 'Birth_partial', F(0), 1),
        ('ineligible_Birth_raw_loss', (0, 0, 1, 0, 0, 1), 'Birth_partial', F(-1, 2), 0),
        ('outgoing_Q_creation_event', (0, 0, 0, 0, 1, 0), 'carrier_creation_v0', F(0), 1),
    ]:
        operation = partial[op_name]
        audit('PRE', name, {'state': list(state), 'operation': operation, 'probe': 0,
                            'center': [[S, 0]], 'L2_error': '0',
                            'reference_raw': str(expected_raw), 'reference_success': expected_success})
        target = C.apply_partial(state, operation)
        success = int(target is not None)
        before = C.cost_numerators(state)[0]
        after = C.cost_numerators(target)[0] if success else 0
        table = small_table({
            'success': definition(14*success, F(1), 'PARTIAL_SUCCESS_PROBABILITY', F(0), F(1)),
            'raw': definition(after-before, F(1, 2), 'NONUNITARY_RAW_FUNCTIONAL_NOT_NORMALIZED_BIAS'),
            'event': definition(after-success*before, F(0), 'EXACT_ELIGIBLE_PULLBACK_NULL')})
        value = R.evaluate(table, [(S, 0)], F(0))
        answer = {'target_state': list(target) if success else None,
                  'target_Q': C.pop(target[2])+C.pop(target[4]) if success else None,
                  'table': table, 'read': value, 'reference_raw': str(expected_raw),
                  'reference_success': expected_success,
                  'references_match': F(value['all_reads']['raw']['center_expectation']) == expected_raw
                    and F(value['all_reads']['success']['center_expectation']) == expected_success
                    and F(value['all_reads']['event']['center_expectation']) == 0,
                  'normalized_postselected_cost_computed': False}
        audit('RETURN', name, answer)
        cases[name] = answer
        checks[name] = answer['references_match']
    name = 'rounded_center_L2_enclosure'
    table = small_table({'cost': definition(7, F(1, 2), 'ABSOLUTE_COST_OVER_EBIAS')})
    audit('PRE', name, {'table': table, 'center': [[S-1, 0]], 'L2_error': str(F(1, S)),
                        'normalized_reference_read': '1/2'})
    value = R.evaluate(table, [(S-1, 0)], F(1, S))
    expected_interval = [F(1, 2)-F(2, S), F(1, 2)]
    answer = {'read': value, 'expected_interval': [str(x) for x in expected_interval],
              'exact_interval_matches': list(map(F, value['all_reads']['cost']['interval'])) == expected_interval}
    audit('RETURN', name, answer)
    cases[name] = answer
    checks[name] = answer['exact_interval_matches']
    unordered = b'UNTI80V1'+struct.pack('<II', 1, 4)+b''.join(x.to_bytes(12, 'little', signed=True) for x in (1, 0, 0, 0))
    bad_table = small_table({'bad': definition(14, F(1, 2), 'ABSOLUTE_COST_OVER_EBIAS')})
    refusal_inputs = [
        ('truncated_vector', {'raw_hex': b'bad'.hex(), 'dimension': 1}),
        ('unordered_vector', {'raw_hex': unordered.hex(), 'dimension': 1}),
        ('invalid_read_range', {'table': bad_table, 'center': [[S, 0]], 'error': '0'}),
        ('original_error_cap', {'table': table, 'center': [[S, 0]], 'error': str(F(1, 1 << 51))}),
    ]
    refusals = {}
    for name, inputs in refusal_inputs:
        audit('PRE', name, inputs)
        try:
            if 'raw_hex' in inputs:
                result = R.decode_vector(bytes.fromhex(inputs['raw_hex']), inputs['dimension'])
            else:
                result = R.evaluate(inputs['table'], inputs['center'], inputs['error'])
        except ValueError as error:
            answer = {'refused': True, 'exception': type(error).__name__, 'message': str(error)}
        else:
            answer = {'refused': False, 'unexpected_return': result}
        audit('RETURN', name, answer)
        refusals[name] = answer
        checks[name] = answer['refused']
    return {'schema': 'P50_EXACT_NATIVE_COST_READ_CONTROLS_V001', 'cases': cases,
            'refusals': refusals, 'checks': checks, 'all_method_checks': all(checks.values()),
            'positive_or_null_cases': 11, 'refusal_cases': 4, 'physical_mass_claim': False}

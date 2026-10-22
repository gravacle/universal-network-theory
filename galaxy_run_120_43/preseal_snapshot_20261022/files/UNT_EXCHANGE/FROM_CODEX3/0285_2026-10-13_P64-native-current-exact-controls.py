"""SOURCE ONLY. Root-injected pinned0284 module; distinct review required.
Tiny exact arithmetic controls for the NEW sparse interval read adapter.
No source import, full-native fixture or author execution.
"""
from fractions import Fraction as F


def controls(M, audit):
    if not callable(audit):
        raise ValueError('durable PRE/RETURN callback required')
    S = 1 << 80
    states = [(0, 1, 1, 0, 0, 1), (0, 1, 2, 0, 0, 1)]
    h = [{1: (-560, 0)}, {0: (-560, 0)}]
    r, s = 3*S//5, 4*S//5
    # Exact normalized reference is (3, +/-4i)/5. Round each positive
    # coordinate down; L1 coordinate discrepancy bounds its L2 error.
    e = F(3, 5)-F(r, S)+F(4, 5)-F(s, S)
    values = {}
    for sign, name, reference in ((1, 'plus_i', F(-6, 25)),
                                   (-1, 'minus_i', F(6, 25))):
        center = [(r, 0), (0, sign*s)]
        audit('PRE', name, M.wire({'states': states, 'rows': h,
              'center': center, 'L2_error_upper': e,
              'normalized_reference_current': reference}))
        eta, js = M.current_rows(states, h)
        got = M.quadratic(js[0], center, lambda: None)
        interval = M.enclose(got, 2*e+e*e, -1, 1)
        answer = {'center_current': got, 'interval': interval,
                  'reference': reference,
                  'contains_reference': interval[0] <= reference <= interval[1],
                  'opposite_site_current': M.quadratic(js[1], center, lambda: None),
                  'complete_eta': eta,
                  'complete_current_rows': js}
        answer['conserves_inventory'] = answer['opposite_site_current'] == -got
        audit('RETURN', name, M.wire(answer))
        values[name] = answer
    bind_states = [(0, 1, 1, 0, 0, 1), (0, 1, 1, 1, 0, 1)]
    bind_h = [{1: (280, 0)}, {0: (280, 0)}]
    audit('PRE', 'bind_no_transport', M.wire({'states': bind_states, 'rows': bind_h}))
    eta, js = M.current_rows(bind_states, bind_h)
    null = {'complete_eta': eta, 'complete_current_rows': js,
            'all_currents_exactly_zero': all(not row for current in js for row in current)}
    audit('RETURN', 'bind_no_transport', M.wire(null))
    values['bind_no_transport'] = null
    refusal_specs = [
        ('current_scale_not_covering', {'states': states, 'rows': [{1: (-2800, 0)}, {0: (-2800, 0)}]}),
        ('inconsistent_normalized_range', {'center': F(2), 'error': F(0), 'lower': -1, 'upper': 1}),
        ('insufficient_precision', {'center': F(0), 'error': F(1, 512), 'lower': -1, 'upper': 1}),
    ]
    refusals = {}
    for name, inputs in refusal_specs:
        audit('PRE', name, M.wire(inputs))
        try:
            if name == 'current_scale_not_covering':
                got = M.current_rows(inputs['states'], inputs['rows'])
            else:
                got = M.enclose(**inputs)
        except ValueError as error:
            outcome = {'refused': True, 'exception': type(error).__name__, 'message': str(error)}
        else:
            outcome = {'refused': False, 'unexpected_return': got}
        audit('RETURN', name, M.wire(outcome))
        refusals[name] = outcome
    checks = {'positive_phase': values['plus_i']['contains_reference'],
              'reversed_phase': values['minus_i']['contains_reference'],
              'positive_conservation': values['plus_i']['conserves_inventory'],
              'negative_conservation': values['minus_i']['conserves_inventory'],
              'bind_null': null['all_currents_exactly_zero'],
              'all_three_refusals': all(row['refused'] for row in refusals.values())}
    return M.wire({'schema': 'P64_EXACT_CURRENT_READ_CONTROLS_V001', 'cases': values,
                   'refusals': refusals, 'checks': checks,
                   'all_controls': all(checks.values()), 'physical_release': False})

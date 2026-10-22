"""SOURCE ONLY. Root-only complete new15 preparation/enclosure controls.
Input full_states/components are entire C153 exact nativepacket, independently
acceptedC15720state family. Root durably binds originalpacket/source pins.
One fullbinding call,15full10432center calls,5refusals =21PRE/RETURN pairs.
"""
from fractions import Fraction as F


def wire(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): wire(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [wire(v) for v in x]
    return x


def controls(N, full_states, components, audit):
    if not callable(audit):
        raise ValueError('root durable control callback required')
    records = {}
    def call(name, function, args):
        audit('PRE', name, {'function': function, 'arguments': wire(args)})
        try:
            result = getattr(N, function)(*args)
            out = {'exception': None, 'value': wire(result)}
        except ValueError as error:
            out = {'exception': 'ValueError', 'message': str(error)}
            result = None
        audit('RETURN', name, out)
        records[name] = out
        return result
    bindings = call('all15_exact_native_bindings', 'bind_preparations', [full_states, components])
    if bindings is None:
        raise ValueError('complete acceptednative positivebinding required')
    active = sorted(components[0])
    local = {native: i for i, native in enumerate(active)}
    for seed in N.SEEDS:
        sparse = {local[e['index']]: e['amplitude'] for e in bindings[seed]['entries']}
        call('initial_enclosure_'+seed, 'enclose_initial_seed', [sparse])
    call('refuse_old_q11_alias', 'identity', ['OLD_CARRIER_SITE0'])
    call('refuse_incomplete_native_basis', 'bind_preparations', [full_states[:-1], components])
    duplicate = [list(g) for g in components]
    duplicate[0][0] = duplicate[0][1]
    call('refuse_duplicate_component_member', 'bind_preparations', [full_states, duplicate])
    call('refuse_unnormalized_initial', 'enclose_initial_seed', [{0: [F(2), F(0)]}])
    call('refuse_unfrozen_stage', 'stage_schedule', [4])
    checks = {'complete15bindings': len(bindings) == 15,
              'all15_full_initial_enclosures': all(records['initial_enclosure_'+s]['exception'] is None
                  and len(records['initial_enclosure_'+s]['value'][0]) == 10432 for s in N.SEEDS),
              'five_refusals': all(records[n]['exception'] == 'ValueError' for n in
                  ('refuse_old_q11_alias', 'refuse_incomplete_native_basis', 'refuse_duplicate_component_member',
                   'refuse_unnormalized_initial', 'refuse_unfrozen_stage'))}
    return {'schema': 'P64_NEW15_BINDING21_CONTROLS_V001', 'calls': records, 'checks': checks,
            'all_controls': all(checks.values()), 'new_propagation': False,
            'physical_state_qualification': False}

"""Pure draft A248 policy. No file access, process operation, or clock read.

The A249 monitor ceiling is Phase 2; the cause-record adapter is a separate dependency.
An identity must come from that adapter, never from an unverified receipt field.
This component is not yet a standalone or released P-112 tool.
"""

MODEL_FAILURE_CODES = frozenset({
    'ROUTE_A_NO_FIXED_POINT', 'ITERATION_BUDGET_EXHAUSTED',
})
MODEL_DRIVER_STATUSES = frozenset({
    'ROUTE_A_NO_FIXED_POINT', 'FAILED', 'FAILED_AT_STAGE',
})


def _authenticated_identity(receipt, authenticated_causes):
    pin = receipt.get('receipt_pin')
    if not is_pin(pin) or not isinstance(authenticated_causes, dict):
        return None
    evidence = authenticated_causes.get((pin['path'], pin['sha256']))
    if not isinstance(evidence, dict):
        return None
    expected = {
        'driver_sha256', 'spec_sha256', 'stage', 'status', 'failure_code',
        'clean', 'iteration_budget', 'registered_iteration_budget',
        'signal', 'exception_type', 'source_pins',
    }
    if set(evidence) != expected or evidence['clean'] is not True or \
            evidence['signal'] is not None or evidence['exception_type'] is not None:
        return None
    if evidence['failure_code'] not in MODEL_FAILURE_CODES or \
            evidence['status'] not in MODEL_DRIVER_STATUSES:
        return None
    if receipt.get('raw_status') != 'CHILD_FAILED|' + evidence['status'] or \
            receipt.get('status_class') != 'FAILED' or \
            evidence['spec_sha256'] != receipt.get('spec_sha256'):
        return None
    if not isinstance(evidence['stage'], str) or not evidence['stage'] or \
            not isinstance(evidence['driver_sha256'], str) or \
            HEX64.fullmatch(evidence['driver_sha256']) is None:
        return None
    budget = evidence['iteration_budget']
    if type(budget) is not int or budget <= 0 or \
            type(evidence['registered_iteration_budget']) is not int or \
            budget != evidence['registered_iteration_budget']:
        return None
    if not isinstance(evidence['source_pins'], list) or not evidence['source_pins'] or \
            not all(is_pin(p) for p in evidence['source_pins']):
        return None
    return tuple(evidence[k] for k in (
        'driver_sha256', 'spec_sha256', 'stage', 'status', 'failure_code', 'iteration_budget'))


def terminal_prefix(actual, name, authenticated_causes=None):
    """Only natural completion, evidenced twin stop, or reproduced model outcomes."""
    for i, current in enumerate(actual):
        cls = current.get('status_class')
        if cls == 'FINISHED':
            return {'index': i, 'disposition': 'FINISHED'}
        if cls == 'PLANNED_STOP':
            need(name == TWIN, 'PLANNED_STOP_NOT_TWIN')
            need(is_pin(current.get('pins', {}).get('stop_record')), 'TWIN_STOP_NOT_BOUND')
            return {'index': i, 'disposition': 'PLANNED_STOP'}
        if i == 0 or cls != 'FAILED':
            continue
        previous = actual[i - 1]
        identity = _authenticated_identity(current, authenticated_causes)
        if identity is None or identity != _authenticated_identity(previous, authenticated_causes):
            continue
        if len({r.get('spec_sha256') for r in actual[:i + 1]}) != 1:
            continue
        if any(r.get('solo_mode') is not True or type(r.get('other_ngc_processes_max')) is not int
               or r['other_ngc_processes_max'] != 0 for r in (previous, current)):
            continue
        if current.get('host_ram_bytes') != RAM or \
                current.get('rss_cap_bytes') != RAM * (11 if name == TWIN else 1):
            continue
        return {'index': i, 'disposition': 'RULE_C_INVALID',
                'model_identity': list(identity), 'counted_attempts': [i - 1, i]}
    return None


def held_for_fix(actual):
    if len(actual) < 2:
        return False
    a, b = actual[-2:]
    return (b.get('raw_status') in ('CHILD_FAILED|REFUSED', 'CHILD_FAILED|BLOCKED') and
            a.get('raw_status') == b['raw_status'] and
            a.get('spec_sha256') == b.get('spec_sha256'))


def held_for_cause(actual, authenticated_causes=None):
    if len(actual) < 2 or held_for_fix(actual):
        return False
    a, b = actual[-2:]
    if not (a.get('status_class') == b.get('status_class') == 'FAILED' and
            a.get('raw_status') == b.get('raw_status') and
            a.get('raw_status') != 'CHILD_FAILED|NONE|EXIT' and
            a.get('spec_sha256') == b.get('spec_sha256')):
        return False
    if any(r.get('solo_mode') is not True or type(r.get('other_ngc_processes_max')) is not int
           or r['other_ngc_processes_max'] != 0 for r in (a, b)):
        return False
    # Only an authentication adapter supplies this map. A validated non-model
    # decision may occupy its key with None; absent/unauthenticated is missing.
    known = authenticated_causes if isinstance(authenticated_causes, dict) else {}
    return any(not is_pin(r.get('receipt_pin')) or
               (r['receipt_pin']['path'], r['receipt_pin']['sha256']) not in known for r in (a, b))


def remaining_wall(ceiling_utc, now_utc):
    remaining = math.floor(timestamp(ceiling_utc, whole=True) - timestamp(now_utc))
    need(remaining > 0, 'UNEVALUATED_SCHEDULE_CEILING')
    return remaining


def next_attempt(name, records, actual, residuals, trailing_nonattempt=None, *,
                 phase_ceiling_utc, now_utc, monitor_ceiling_utc=None,
                 authenticated_causes=None, root_hold_release=False,
                 has_monitor_refusal=False):
    """Pure prospective decision; every invocation launches at most one root-chosen attempt.

    A249 passes Phase 2 as monitor_ceiling_utc. Phase 1 only limits Phase-1
    admissions and reporting; it never stops an active run.
    """
    terminal = terminal_prefix(actual, name, authenticated_causes)
    need(terminal is None, 'ATTEMPT_AFTER_TERMINAL', terminal)
    remaining_wall(phase_ceiling_utc, now_utc)
    need(not held_for_fix(actual) or root_hold_release, 'HELD_FOR_FIX')
    need(not held_for_cause(actual, authenticated_causes), 'HELD_FOR_CAUSE')
    need(monitor_ceiling_utc is not None, 'MONITOR_PHASE2_CEILING_REQUIRED')
    wall = remaining_wall(monitor_ceiling_utc, now_utc)
    ks = [r['attempt'] for r in records] + [k for n, k in residuals if n == name]
    k = max(ks, default=0) + 1
    if name.startswith('S0_'):
        need(any(r['origin'] == 'P112' or r['outcome'] == 'LAUNCH' for r in records)
             or any(n == name for n, _ in residuals), 'KIT_RELAUNCH_OWNS')
    retry = bool(records or actual or trailing_nonattempt is not None or residuals or has_monitor_refusal)
    caps = first_caps(name)
    basis = []
    if trailing_nonattempt is not None:
        caps = dict(trailing_nonattempt['caps'])
    elif actual:
        previous = actual[-1]
        caps = caps_of(previous)
        if previous['status_class'] == 'OUTPUT_CAP':
            caps['output_cap_bytes'] *= 2
        basis = [r['receipt_pin'] for r in actual if is_pin(r.get('receipt_pin'))]
    caps['rss_cap_bytes'] = RAM * (11 if name == TWIN else 1)
    caps['wall_cap_s'] = wall
    return {
        'attempt': k, 'caps': caps, 'solo_mode': retry,
        # No unrun attempt can already be counted as reproduced.
        'counted_rerun': False, 'rule_c_basis': basis,
        'phase_ceiling_utc': phase_ceiling_utc, 'monitor_ceiling_utc': monitor_ceiling_utc,
        'decision_utc': now_utc,
        'model_confirmation_rerun': bool(actual and _authenticated_identity(actual[-1], authenticated_causes)),
    }


def phase_disposition(actual, name, phase_ceiling_utc, now_utc, authenticated_causes=None):
    """A reporting snapshot only; it never requests a process stop."""
    cutoff = timestamp(phase_ceiling_utc, whole=True)
    eligible = [r for r in actual if timestamp(r['time_utc'], whole=True) <= cutoff]
    term = terminal_prefix(eligible, name, authenticated_causes)
    if term is not None:
        return {'status': 'TERMINAL', 'terminal': term, 'stop_requested': False}
    if timestamp(now_utc) >= cutoff:
        return {'status': 'UNEVALUATED_SCHEDULE_CEILING', 'terminal': None,
                'continues_for_next_phase': True, 'stop_requested': False}
    return {'status': ('HELD_FOR_FIX' if held_for_fix(actual) else
                       'HELD_FOR_CAUSE' if held_for_cause(actual, authenticated_causes) else 'NOT_TERMINAL'),
            'terminal': None, 'stop_requested': False}

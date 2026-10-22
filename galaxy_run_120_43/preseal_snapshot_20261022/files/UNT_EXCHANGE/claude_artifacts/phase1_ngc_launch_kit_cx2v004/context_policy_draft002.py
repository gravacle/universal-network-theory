"""Phase-1 reporting and immutable policy inputs. No implicit process stop."""
PHASE1_CEILING_UTC = '2026-11-06T05:59:00Z'
PHASE2_CEILING_UTC = '2026-12-01T05:59:00Z'


def validate_policy_config(config):
    need(config['phase1_ceiling_utc'] == PHASE1_CEILING_UTC and
         config['phase2_ceiling_utc'] == PHASE2_CEILING_UTC, 'PHASE_CEILING_CONFIG')
    for field in ('cause_records', 'root_stop_records'):
        pins = config[field]
        need(type(pins) is list and all(is_pin(p) for p in pins), 'POLICY_INPUT_PINS', field)
        need(len({p['path'] for p in pins}) == len(pins), 'POLICY_INPUT_DUPLICATE', field)
        for pin in pins:
            guard_record(pin['path'])


def command_now(ctx):
    if not hasattr(ctx, '_policy_now_utc'):
        ctx._policy_now_utc = ctx.system.utc()
        timestamp(ctx._policy_now_utc)
    return ctx._policy_now_utc


def decision_for(ctx, call, hist, *, now_utc=None):
    need(not hist.get('pending'), 'ATTEMPT_INCOMPLETE', hist.get('pending'))
    return next_attempt(call['name'], hist['records'], hist['actual'], hist['residuals'],
                        hist['trailing_nonattempt'],
                        phase_ceiling_utc=ctx.cfg['phase1_ceiling_utc'],
                        monitor_ceiling_utc=ctx.cfg['phase2_ceiling_utc'],
                        now_utc=command_now(ctx) if now_utc is None else now_utc,
                        authenticated_causes=authenticated_causes(ctx, hist['actual']),
                        has_monitor_refusal=bool(hist.get('refusals')))


@read_scope
def status(ctx):
    result = []
    now = ctx.system.utc()
    timestamp(now)
    ctx._policy_now_utc = now
    try:
        ctx.residuals()
    except Refusal as error:
        return {'status': error.code, 'detail': error.detail}
    for call in ctx.calls():
        try:
            hist = history(ctx, call, inspect_next=False, allow_incomplete=True)
            causes = authenticated_causes(ctx, hist['actual'])
            phase = phase_disposition(hist['actual'], call['name'],
                                      ctx.cfg['phase1_ceiling_utc'], now, causes)
            decision, problem = None, None
            if phase['status'] == 'NOT_TERMINAL':
                if hist['pending']:
                    problem = hist['pending'][-1]['status']
                else:
                    try:
                        decision = decision_for(ctx, call, hist)
                    except Refusal as error:
                        problem = error.code
            result.append({
                'name': call['name'],
                'status': problem or ('READY' if decision is not None else phase['status']),
                'attempts': [{'attempt': a['attempt'], 'raw_status': a['raw_status'],
                              'status_class': a['status_class'],
                              'nonphysics': a.get('_known_nonphysics', False)} for a in hist['actual']],
                'terminal': phase['terminal'], 'next': decision, 'phase_1': phase,
                'pending': hist['pending'], 'nonattempts': hist['nonattempts'],
                'consecutive_nonattempts': hist['consecutive_nonattempts'],
            })
        except Refusal as error:
            result.append({'name': call['name'], 'status': error.code, 'detail': error.detail})
    return {'schema': 'P112_STATUS_CX2V004', 'calls': result, 'date_u': date_u(),
            'as_of_utc': now, 'phase1_ceiling_utc': ctx.cfg['phase1_ceiling_utc'],
            'phase2_ceiling_utc': ctx.cfg['phase2_ceiling_utc'], 'stop_requested': False,
            'advisory': True, 'launch_authorized': False, 'observations': observation_report()}

"""A249: bind a fresh Phase-2 wall after dry checks and sampler startup.

The bootstrap plan is immutable. A successor launch plan and a commit record
bind the final argv; sampler and resume consume that same successor.
"""

LAUNCH_COMMIT_SCHEMA = 'P112_LAUNCH_COMMIT_CX2V004'


def fresh_launch_plan(ctx, bootstrap, now_utc):
    remaining_wall(ctx.cfg['phase1_ceiling_utc'], now_utc)
    seconds = remaining_wall(ctx.cfg['phase2_ceiling_utc'], now_utc)
    need(seconds <= bootstrap['caps']['wall_cap_s'], 'LAUNCH_CLOCK_MOVED_BACKWARD')
    plan = copy.deepcopy(bootstrap)
    plan['caps']['wall_cap_s'] = seconds
    plan['caps_basis'] = {
        'rule': 'A249: Phase 1 reporting only; monitor wall uses remaining Phase 2',
        'decision_utc': now_utc,
        'phase1_ceiling_utc': ctx.cfg['phase1_ceiling_utc'],
        'phase2_ceiling_utc': ctx.cfg['phase2_ceiling_utc'],
        'phase1_requests_stop': False,
    }
    plan['invocation_utc'] = now_utc
    plan['date_u'] = date_u()
    plan['monitor_argv'] = monitor_command(ctx.pins, plan['spec'], plan['outdir'], plan['caps'])
    return plan


def _commit_plan_check(ctx, bootstrap, bootstrap_pin, commit, plan, plan_pin, work):
    keys(commit, ('schema', 'bootstrap_plan', 'launch_plan', 'date_u', 'observations'), 'launch commit')
    need(commit['schema'] == LAUNCH_COMMIT_SCHEMA and commit['bootstrap_plan'] == bootstrap_pin and
         commit['launch_plan'] == plan_pin, 'LAUNCH_COMMIT_BINDING')
    need(plan_pin['path'] == str(Path(work) / 'launch_plan.json'), 'LAUNCH_COMMIT_RESIDENCE')
    changed = {'caps', 'caps_basis', 'invocation_utc', 'date_u', 'monitor_argv', 'observations'}
    need(set(plan) == set(bootstrap) and all(
        plan[k] == bootstrap[k] for k in plan if k not in changed), 'LAUNCH_COMMIT_FIXED_FIELDS')
    need(set(plan['caps']) == set(bootstrap['caps']) and all(
        plan['caps'][k] == bootstrap['caps'][k] for k in plan['caps'] if k != 'wall_cap_s'),
        'LAUNCH_COMMIT_MACHINE_CAPS')
    basis = plan['caps_basis']
    keys(basis, ('rule', 'decision_utc', 'phase1_ceiling_utc', 'phase2_ceiling_utc',
                 'phase1_requests_stop'), 'launch caps basis')
    need(basis['phase1_ceiling_utc'] == ctx.cfg['phase1_ceiling_utc'] and
         basis['phase2_ceiling_utc'] == ctx.cfg['phase2_ceiling_utc'] and
         basis['phase1_requests_stop'] is False and
         basis['decision_utc'] == plan['invocation_utc'], 'LAUNCH_COMMIT_CEILINGS')
    remaining_wall(ctx.cfg['phase1_ceiling_utc'], basis['decision_utc'])
    need(timestamp(plan['invocation_utc']) >= timestamp(bootstrap['invocation_utc']),
         'LAUNCH_CLOCK_MOVED_BACKWARD')
    need(plan['caps']['wall_cap_s'] == remaining_wall(
        ctx.cfg['phase2_ceiling_utc'], basis['decision_utc']) and
        plan['caps']['wall_cap_s'] <= bootstrap['caps']['wall_cap_s'], 'LAUNCH_COMMIT_WALL')
    need(plan['monitor_argv'] == monitor_command(ctx.pins, plan['spec'], plan['outdir'], plan['caps']),
         'LAUNCH_COMMIT_ARGV')
    return plan, plan_pin


@read_scope
def write_launch_commit(ctx, bootstrap, bootstrap_pin, work, now_utc):
    ctx.gate()
    work = str(Path(work))
    need(bootstrap_pin['path'] == str(Path(work) / 'plan.json'), 'LAUNCH_BOOTSTRAP_RESIDENCE')
    need(bootstrap['config'] == ctx.config_pin and bootstrap['work'] == work, 'LAUNCH_BOOTSTRAP_BINDING')
    path = str(Path(work) / 'LAUNCH_COMMIT.json')
    final_path = str(Path(work) / 'launch_plan.json')
    need(not os.path.lexists(path) and not os.path.lexists(final_path), 'LAUNCH_COMMIT_EXISTS')
    plan = fresh_launch_plan(ctx, bootstrap, now_utc)
    pin = ctx.write(final_path, plan)
    # Context.write adds only the observation report. Verify the actual saved
    # bytes and use them for all subsequent bindings.
    checked_pin, checked = read_record(final_path)
    need(pin == checked_pin, 'LAUNCH_COMMIT_SAVED_PLAN')
    commit = {
        'schema': LAUNCH_COMMIT_SCHEMA, 'bootstrap_plan': bootstrap_pin,
        'launch_plan': checked_pin, 'date_u': date_u(),
    }
    ctx.write(path, commit)
    _, saved_commit = read_record(path)
    return _commit_plan_check(ctx, bootstrap, bootstrap_pin, saved_commit, checked, checked_pin, work)


def read_launch_commit(ctx, bootstrap, bootstrap_pin, work, *, snapshot=None):
    path = str(Path(work) / 'LAUNCH_COMMIT.json')
    if snapshot is None:
        _, commit = read_record(path)
    else:
        commit = snapshot
    need(type(commit) is dict and is_pin(commit.get('launch_plan')), 'LAUNCH_COMMIT_FORM')
    # Validate residence before following the pin.
    need(commit['launch_plan']['path'] == str(Path(work) / 'launch_plan.json'), 'LAUNCH_COMMIT_RESIDENCE')
    pin, raw = read_record(commit['launch_plan']['path'], decode=False)
    need(pin == commit['launch_plan'], 'LAUNCH_COMMIT_PIN')
    plan = strict_json(raw)
    return _commit_plan_check(ctx, bootstrap, bootstrap_pin, commit, plan, pin, work)


def observe_launch_commit(ctx, bootstrap, bootstrap_pin, work):
    """One volatile poll; a validated commit is thereafter reused by sampler."""
    path = str(Path(work) / 'LAUNCH_COMMIT.json')
    if not os.path.lexists(path):
        return None
    raw, _ = observe_file(path, 'launch_commit')
    try:
        commit = strict_json(raw)
    except Refusal as exc:
        if exc.code == 'JSON_PARSE':
            return None
        raise
    return read_launch_commit(ctx, bootstrap, bootstrap_pin, work, snapshot=commit)

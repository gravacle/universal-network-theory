"""P112 value-free input boundary. Never follows a cause's result/finish/driver path.
Producer outputs are pinned by the root's immutable config. Byte identity does
not prove origin; review and root custody remain the producer's prerequisites.
"""
CAUSE_KEYS = ('status', 'failing_stage', 'failure_code', 'exception_class', 'raise_site',
              'bound_shas', 'model_outcome', 'model_outcome_reason')
CAUSE_SHA_KEYS = ('receipt', 'result', 'finish', 'spec', 'driver')
KNOWN_NONPHYSICS_CAUSES = frozenset({
    'NONPHYSICS_OR_NOT_FAILED', 'SIGNAL_OR_EXIT_UNAUTHENTICATED',
    'A248_EXCLUDED_SOURCE_PREPARATION', 'SIGNAL_KILLED_STAGE',
})


def read_cause_inputs(ctx):
    result = {}
    for pin in ctx.cfg['cause_records']:
        cause = read_pin(pin)
        keys(cause, CAUSE_KEYS, 'value-free cause')
        keys(cause['bound_shas'], CAUSE_SHA_KEYS, 'cause bindings')
        need(type(cause['model_outcome']) is bool and
             isinstance(cause['model_outcome_reason'], str), 'CAUSE_FORM')
        for key in ('status', 'failing_stage', 'failure_code', 'exception_class', 'raise_site'):
            need(cause[key] is None or isinstance(cause[key], str), 'CAUSE_FORM', key)
        for key, value in cause['bound_shas'].items():
            need(value is None or isinstance(value, str) and HEX64.fullmatch(value), 'CAUSE_SHA_FORM', key)
        receipt_sha = cause['bound_shas']['receipt']
        need(receipt_sha is not None and receipt_sha not in result, 'CAUSE_RECEIPT_NOT_UNIQUE')
        result[receipt_sha] = (cause, pin)
    return result


def authenticated_causes(ctx, actual):
    """Map only bound, independently rederived closed receipts; unknown stays absent."""
    inputs = read_cause_inputs(ctx)
    mapped = {}
    for receipt in actual:
        pin = receipt['receipt_pin']
        key = (pin['path'], pin['sha256'])
        monitor = receipt['_verified_monitor']
        if receipt.get('_known_nonphysics'):
            mapped[key] = None
            continue
        source = inputs.get(receipt['pins']['monitor_receipt']['sha256'])
        if source is None:
            continue
        cause, source_pin = source
        bindings = cause['bound_shas']
        need(bindings['spec'] == receipt['spec_sha256'] and
             bindings['driver'] == monitor['pins']['driver']['sha256'], 'CAUSE_SCIENCE_BINDING')
        need(cause['status'] == monitor.get('driver_status'), 'CAUSE_STATUS_BINDING')
        if bindings['result'] is not None:
            need(is_pin(monitor.get('result')) and bindings['result'] == monitor['result']['sha256'],
                 'CAUSE_RESULT_BINDING')
        if not cause['model_outcome']:
            if cause['model_outcome_reason'] in KNOWN_NONPHYSICS_CAUSES:
                mapped[key] = None
            continue
        need(all(isinstance(bindings[k], str) and HEX64.fullmatch(bindings[k])
                 for k in CAUSE_SHA_KEYS), 'CAUSE_BOUND_SHA_MISSING')
        need(cause['failure_code'] in MODEL_FAILURE_CODES and
             cause['status'] == 'ROUTE_A_NO_FIXED_POINT' and
             all(isinstance(cause[k], str) and bool(cause[k])
                 for k in ('failing_stage', 'exception_class', 'raise_site')),
             'CAUSE_MODEL_IDENTITY')
        need(monitor.get('status') == 'CHILD_FAILED' and
             monitor.get('stop_reason') is None and type(monitor.get('exit_code')) is int and
             monitor['exit_code'] > 0 and monitor['exit_code'] not in (137, 143), 'CAUSE_NONPHYSICS_END')
        mapped[key] = {'cause': cause, 'cause_pin': source_pin,
                       'monitor_receipt': receipt['pins']['monitor_receipt']}
    return mapped


def _authenticated_identity(receipt, authenticated):
    if receipt.get('_known_nonphysics') or receipt.get('status_class') != 'FAILED':
        return None
    pin = receipt.get('receipt_pin')
    if not is_pin(pin) or not isinstance(authenticated, dict):
        return None
    evidence = authenticated.get((pin['path'], pin['sha256']))
    if not isinstance(evidence, dict) or set(evidence) != {'cause', 'cause_pin', 'monitor_receipt'}:
        return None
    cause = evidence['cause']
    if not is_pin(evidence['cause_pin']) or not is_pin(evidence['monitor_receipt']) or \
            type(cause) is not dict or set(cause) != set(CAUSE_KEYS) or cause['model_outcome'] is not True:
        return None
    bound = cause['bound_shas']
    if type(bound) is not dict or set(bound) != set(CAUSE_SHA_KEYS) or \
            not all(isinstance(bound[k], str) and HEX64.fullmatch(bound[k]) for k in CAUSE_SHA_KEYS):
        return None
    if bound['receipt'] != evidence['monitor_receipt']['sha256'] or \
            bound['spec'] != receipt['spec_sha256'] or \
            receipt.get('raw_status') != 'CHILD_FAILED|' + str(cause['status']) or \
            cause['status'] != 'ROUTE_A_NO_FIXED_POINT' or cause['failure_code'] not in MODEL_FAILURE_CODES:
        return None
    fields = ('status', 'failing_stage', 'failure_code', 'exception_class', 'raise_site')
    if any(not isinstance(cause[k], str) or not cause[k] for k in fields):
        return None
    return (bound['spec'], bound['driver']) + tuple(cause[k] for k in fields)


def bound_root_stop(ctx, receipt):
    """Explicit root stop evidence preempts natural completion and a planned twin stop."""
    hits = []
    for pin in ctx.cfg['root_stop_records']:
        doc = read_pin(pin)
        keys(doc, ('schema', 'date_u', 'call', 'launch_json', 'registration'), 'root stop')
        need(doc['schema'] == 'ROOT_NONPHYSICS_STOP_C2V001', 'ROOT_STOP_SCHEMA')
        if doc['launch_json'] != receipt['pins']['launch_json']:
            continue
        need(doc['call'] == receipt['call'], 'ROOT_STOP_CALL_BINDING')
        need(timestamp(doc['date_u']) <= timestamp(receipt['time_utc'], whole=True), 'ROOT_STOP_AFTER_END')
        read_pin(doc['registration'], decode=False)
        hits.append(pin)
    need(len(hits) <= 1, 'ROOT_STOP_NOT_UNIQUE')
    return hits[0] if hits else None


def verify_closed_receipt(ctx, call, record, monitor_pin, monitor, closed_pin, obj):
    """Reproduce the policy-bearing projection from adjacent custody records only."""
    name, k, outdir = record['name'], record['attempt'], record['outdir']
    need(obj.get('schema') == 'STEP5_ATTEMPT_RECEIPT_C2V001' and
         obj.get('call') == {key: call[key] for key in ('name', 'kind', 'alternative', 'key')} and
         obj.get('attempt') == k and obj.get('run_dir') == outdir and
         obj.get('spec_sha256') == call['spec']['sha256'] and
         obj.get('theta_sha256') == call['theta_sha256'] and
         obj.get('point_key') == call['point_key'], 'ATTEMPT_RECEIPT_BINDING')
    launch_pin, launch = read_record(outdir + '.receipt.json.launch.json')
    validate_launch_json(launch)
    need(record['launch_json'].get('sha256') in (None, launch_pin['sha256']), 'LAUNCH_JSON_RECORD_PIN')
    need(monitor.get('child_pid') == launch.get('child_pid'), 'MONITOR_CHILD_BINDING')
    need(monitor.get('pins', {}).get('driver') == record['driver'] == ctx.pins['driver'] and
         monitor.get('pins', {}).get('monitor') == record['monitor'] == ctx.pins['monitor'], 'MONITOR_TOOL_PINS')
    stop, stop_pin = bound_stop_record(ctx, record, launch_pin)
    raw, cls = raw_status(monitor, name=name, attempt=k, outdir=outdir, receipt=record['receipt'],
                         launch_pin=launch_pin, child_pid=monitor['child_pid'],
                         mislaunch=record if record['outcome'] == 'MISLAUNCH' else None, stop=stop)
    sample, sample_pin = None, None
    sp = outdir + '.solo.json'
    if Path(sp).is_file():
        sample_pin, sample = read_record(sp)
        need(sample.get('schema') == 'STEP5_SOLO_SAMPLE_CX2V001' and
             sample.get('name') == name and sample.get('attempt') == k and sample.get('outdir') == outdir and
             sample.get('declared_list_sha256') == DECLARED_LIST_SHA and
             sample.get('monitor_receipt') == monitor_pin, 'SOLO_SAMPLE_BINDING')
    expected = dict(raw_status=raw, status_class=cls, time_utc=monitor['utc_end'],
                    launch_utc=launch['utc'], host_ram_bytes=RAM,
                    other_ngc_processes_max=sample_value(sample, monitor),
                    solo_mode=record.get('solo_mode', False),
                    counted_rerun=record.get('counted_rerun', False),
                    **{key: monitor['caps'][key] for key in CAPS['serial']})
    need(all(obj.get(key) == value and type(obj.get(key)) is type(value)
             for key, value in expected.items()), 'ATTEMPT_PROJECTION_MISMATCH')
    pins = obj.get('pins', {})
    need(pins.get('monitor_receipt') == monitor_pin and pins.get('launch_json') == launch_pin and
         pins.get('launch_record') == record['record_pin'] and pins.get('solo_sample') == sample_pin and
         pins.get('stop_record') == stop_pin and pins.get('result') == monitor.get('result') and
         pins.get('status_map_sha256') == STATUS_MAP_SHA, 'ATTEMPT_SOURCE_BINDING')
    timestamp(monitor['utc_end'], whole=True)
    root_stop = bound_root_stop(ctx, obj)
    ex = monitor.get('exit_code')
    # A legitimate watch record overrides its own signal only. An explicit
    # root stop, missing/invalid exit, or a monitor stop without watch is nonphysics.
    nonphysics = bool(root_stop) or (cls != 'PLANNED_STOP' and (
        monitor.get('stop_reason') is not None or type(ex) is not int or ex < 0 or ex in (137, 143)))
    nonphysics = nonphysics or raw == 'CHILD_FAILED|NONE|EXIT' or cls in ('CAP', 'OUTPUT_CAP', 'INFRA')
    return dict(obj, receipt_pin=closed_pin, _verified_monitor=monitor,
                _known_nonphysics=nonphysics, _root_stop=root_stop)

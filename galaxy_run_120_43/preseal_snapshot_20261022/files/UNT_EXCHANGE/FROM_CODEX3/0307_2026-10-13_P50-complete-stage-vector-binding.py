"""SOURCE ONLY. Bind every accepted stage time to full I80 vectors and errors.
Root injects exact read module0306 and callbacks. Complete original archive,
source and C150 ancestry authentication is mandatory outside this adapter.
"""
from fractions import Fraction as F
import hashlib

STARTS = (F(0), F(1, 8), F(1, 4), F(1, 2))
STOPS = (F(1, 8), F(1, 4), F(1, 2), F(1))
PANELS = (64, 64, 128, 256)
SEEDS = ('OLD_CARRIER_SITE0', 'OLD_CARRIER_SITE1', 'OLD_READY_SITE0',
         'OLD_COHERENT_PLUS_I', 'OLD_COHERENT_MINUS_I')


def need(ok, why):
    if not ok:
        raise ValueError(why)


def vector_binding(binding, index, label):
    need(set(binding) == {'file', 'bytes', 'sha256', 'dimension', 'fractional_bits', 'fields', 'endpoint_signed_bits'}, 'complete original vector binding')
    need(binding['file'] == 'STEP_%03d_%s.bin' % (index, label), 'literal frozen vector name')
    need(binding['dimension'] == 10432 and binding['bytes'] == 500752
         and binding['fractional_bits'] == 80 and binding['endpoint_signed_bits'] == 96,
         'full original fixed-width vector')
    need(binding['fields'] == ['real_lower', 'real_upper', 'imag_lower', 'imag_upper'], 'literal coordinate order')
    need(type(binding['sha256']) is str and len(binding['sha256']) == 64, 'original full vector hash')


def read_center(R, binding, load_vector, point):
    # load_vector must also bind this exact file to original whole closure and
    # namespace; a path/hash supplied by an unauthenticated journal is not enough.
    raw = load_vector(binding)
    need(type(raw) is bytes and len(raw) == binding['bytes']
         and hashlib.sha256(raw).hexdigest() == binding['sha256'], 'whole consumed vector bytes')
    return R.decode_vector(raw, 10432, point=point)


def stage_reads(R, table, seed, stage, journal_records, load_vector, audit,
                guard=lambda: None):
    need(seed in SEEDS and type(stage) is int and 0 <= stage < 4, 'frozen five-seed/four-stage read')
    need(table['active_dimension'] == 10432 and len(table['reads']) == 125, 'complete native read table')
    need(callable(load_vector) and callable(audit), 'owned complete byte reader and durable audit')
    times = [STARTS[stage]+F(2*k+1, 1024) for k in range(PANELS[stage])] + [STOPS[stage]]
    window = R.Window(table)
    next_index = 0
    before = None
    ledger = None
    last_time = STARTS[stage]
    last_error = None
    last_kind = None
    source_vectors = []
    frame_count = 0

    def consume(label, time, binding, error, point, step, role):
        nonlocal frame_count
        pre = {'seed': seed, 'stage': stage, 'time': str(time), 'microstep_index': step,
               'source_vector': binding, 'original_L2_error': str(error),
               'center_rule': 'EXACT_POINT_LEFT_VECTOR' if point else 'FLOOR_MIDPOINT_OF_ORIGINAL_SUM16_INTERVALS',
               'role': role, 'complete_original_archive_gate_required': True,
               'propagation_error_proof': 'C150 and complete original independently reconstructed ancestry'}
        audit('PRE', label, pre)
        center = read_center(R, binding, load_vector, point)
        result = R.evaluate(table, center, error, guard)
        audit('RETURN', label, result)
        window.add(time, result)
        source_vectors.append({'frame': label, 'time': str(time), 'binding': binding,
                               'original_L2_error': str(error)})
        frame_count += 1

    for record in journal_records:
        guard()
        kind = record.get('kind')
        last_kind = kind
        if kind == 'microstep_pre':
            need(before is None and ledger is None and next_index < len(times), 'no missing/overlapping microstep')
            need(record['index'] == next_index and F(record['time']) == last_time, 'complete absolute starting time')
            need(F(record['dt']) == times[next_index]-last_time, 'frozen exact step spacing')
            if 'sample_kind' in record:
                need(record['sample_kind'] == ('ENDPOINT' if next_index == len(times)-1 else 'MIDPOINT'), 'literal saved sample kind')
            before = record
        elif kind == 'microstep_ledger':
            need(before is not None and ledger is None and record['index'] == next_index, 'complete ordered ledger')
            ledger = record['value']
            need(F(ledger['dt']) == F(before['dt']) and ledger['taylor_order'] == 16
                 and F(ledger['shifted_row_norm']) == F(10207, 560), 'original propagation contract')
            need(ledger['center_rule'] == 'floor midpoint of sum_16 real/imag endpoints; never normalized', 'original center rule')
            refs = ledger['vector_files']
            labels = {'left', 'final'} | {'%s_%02d' % (kind, k) for kind in ('action', 'term', 'sum') for k in range(1, 17)}
            need(set(refs) == labels, 'entire fifty-vector microstep binding census')
            for label, binding in refs.items():
                vector_binding(binding, next_index, label)
            previous = F(ledger['previous_L2_error'])
            error = F(ledger['accumulated_L2_error'])
            radius = F(ledger['rounding_L1_radius'])
            tail = F(ledger['truncation_L2_upper'])
            need(min(previous, radius, tail) >= 0 and error == previous+radius+tail
                 and error < F(1, 1 << 51), 'unchanged complete error ledger')
            if next_index == 0:
                consume('START', last_time, refs['left'], previous, True, 0, 'STAGE_START')
                last_error = previous
            need(previous == last_error, 'complete cumulative error chain')
        elif kind == 'readout':
            need(before is not None and ledger is not None and record['index'] == next_index, 'every ledger has one ordered readout')
            time = F(record['time'])
            error = F(ledger['accumulated_L2_error'])
            need(time == times[next_index] and F(record['value']['L2_error']) == error, 'exact complete readout time/error binding')
            if 'sample_kind' in record:
                need(record['sample_kind'] == ('ENDPOINT' if next_index == len(times)-1 else 'MIDPOINT'), 'readout sample kind')
            consume('STEP_%03d' % next_index, time, ledger['vector_files']['sum_16'], error,
                    False, next_index, 'ENDPOINT' if next_index == len(times)-1 else 'MIDPOINT')
            last_time = time
            last_error = error
            next_index += 1
            before = ledger = None
        elif kind == 'failure':
            raise ValueError('failed original propagation journal is not accepted input')
    need(next_index == len(times) and before is None and ledger is None and last_kind == 'closure',
         'complete accepted journal through original closure')
    need(frame_count == PANELS[stage]+2, 'all positive times plus stage start')
    summary = window.finish(STARTS[stage], STOPS[stage], PANELS[stage]+2)
    return {'schema': 'P50_FULL_ACCEPTED_STAGE_COST_READ_V001', 'seed': seed, 'stage': stage,
            'all_original_positive_samples': len(times), 'frame_count_including_start': frame_count,
            'all_consumed_complete_vector_bindings': source_vectors,
            'continuous_window_summary': summary,
            'durable_full_PRE_RETURN_callback_required': True,
            'original_Taylor_reconstructed_again_by_this_read': False,
            'selected_inputs_are_original_process_closure': False,
            'new_propagation': False, 'physical_mass_claim': False}


def aggregate(R, table, seed, stage_frames):
    """Root-only post-read aggregation; every complete raw stage return required.
    Frame object: {time: rational, result: full evaluate() return}. Outer archive
    authentication and new read-source/checker acceptances are caller duties.
    """
    need(seed in SEEDS and set(stage_frames) == {'0', '1', '2', '3'}, 'all four accepted stage read archives')
    window = R.Window(table)
    previous = None
    for stage in range(4):
        frames = stage_frames[str(stage)]
        need(len(frames) == PANELS[stage]+2, 'complete stage raw read census')
        times = [STARTS[stage]]+[STARTS[stage]+F(2*k+1, 1024) for k in range(PANELS[stage])]+[STOPS[stage]]
        for i, (frame, time) in enumerate(zip(frames, times)):
            need(set(frame) == {'time', 'result'} and F(frame['time']) == time, 'literal complete stage times')
            if stage and i == 0:
                need(previous == frame['result'], 'exact same-state duplicate boundary read')
                continue
            window.add(time, frame['result'])
            previous = frame['result']
    summary = window.finish(F(0), F(1), 517)
    return {'schema': 'P50_FIVE_STAGE_BOUNDARIES_FULL_T1_COST_SUMMARY_V001',
            'seed': seed, 'positive_samples': 516, 'initial_sample': 1,
            'summary': summary, 'all_duplicate_boundaries_exact': True,
            'physical_mass_claim': False}

"""Guarded prospective free-angular witness; root-owned execution only."""
from pathlib import Path
import os, sys, json, math, hashlib, time, traceback
from datetime import datetime, timezone
from decimal import Decimal, localcontext

AUTHOR_GUARD = True
J = Path(__file__).resolve().parent
STEM = 'CROSS_U_FREE_STREAMING_ANGULAR_QUADRATURE_WITNESS_V001'
PROTOCOL_SHA = '554e7271ea8e38e91f3248cf39db3e0a5f29f541d740fbd851d7a5cfe31f973f'
PARENT = 'CROSS_U_FULL_FLRW_SAVED_AGGREGATE_RECOVERY_V001'
PINS = {
    'CROSS_U_FULL_FLRW_SAVED_AGGREGATE_RECOVERY_V001_RESULT.json': '919bd3091cdda1f7616bd13f63a03c18d66cfe64a7ce68fdceb23f4cd0ab2d5f',
    'CROSS_U_FULL_FLRW_SAVED_AGGREGATE_RECOVERY_V001_RECEIPT.json': 'd70f6b6f6974522b896b0a4f389454c730c55ee55221096b199aa16003ed7082',
    'CROSS_U_FULL_FLRW_SAVED_AGGREGATE_RECOVERY_V001.md': 'c6d9d9605c8c3eea7abc62109afdc5bdea77d6c6d0200ff422907806637ca630',
    'cross_u_full_flrw_saved_aggregate_recovery_v001.py': 'ef099255955378bd56bad2c7952be118e2c232d0a3aa1a0462633750995f27cd',
    'CROSS_U_FULL_FLRW_SOURCE_CONSTRAINT_AND_FINITE_SLICE_TEST_V001.md': 'c81fa7ed6961f5f0620bbb48dd133ef474543765131ceb738bdcf676f9b9a986',
    'cross_u_full_flrw_source_constraint_v001.py': '8e2860917a75c44ada5be0df18ac43809dc7fe454846b3787d8a3d3017d1e5c1',
    'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_MANIFEST.json': 'fba438e9df2246cbefa27f0b5226e41f435de8632e035d0660ed8f5bf3f6b77d',
    'reviewed_cross_u_free_streaming_angular_quadrature_witness_v001_369_01654333.py': '01654333a0270eb9f3fd3e4fac055a405888b0a8e50c9b0e6547117559402e26',
    'reviewed_CROSS_U_FREE_STREAMING_ANGULAR_QUADRATURE_WITNESS_V001_31_99abc015.md': '99abc0156918ea0fca9eeabfa684fd73226396c57bc3e8db6d30d5f0ba0d81ff',
}
THETAS = (0., .1, 1., 10., 30., 100., 300., 1000., 2000.)
ORDERS = (64, 128, 256, 512, 1024)
MOMENT_TOL = 1e-11
FLAGS = dict(full_prepared_universe=False, original_angle_failures_repaired=False,
             exact_accumulated_phase=False, physical_growth=False, physical_lensing=False,
             native_inertia=False, continuum_angular_evolution=False)
RAW = {}
RAW_META = {}
CONTEXT = {}


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def encode(d):
    return (json.dumps(d, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()


def put(p, raw):
    with Path(p).open('xb') as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    assert Path(p).read_bytes() == raw


def write_json(p, d):
    put(p, encode(d))


def bind(m, p, h):
    p = Path(p).resolve()
    assert sha(p) == h, str(p)
    k = str(p)
    assert k not in m or m[k] == h
    m[k] = h


def closed_parent(inputs):
    r = json.loads((J / (PARENT + '_RECEIPT.json')).read_text())
    assert r['status'] == 'RECOVERED_NUMERICAL_FAILED' and r['closed']
    for p, h in r['input_sha256'].items():
        bind(inputs, p, h)
    for n, h in r['output_sha256'].items():
        assert Path(n).name == n
        bind(inputs, J / n, h)
    d = json.loads((J / (PARENT + '_RESULT.json')).read_text())
    assert r['result_sha256'] == sha(J / (PARENT + '_RESULT.json'))
    assert len(d['rows']) == 32 and len(d['controls']) == 1889
    assert len(d['comparisons']) == 24 and len(d['sample_registration_controls']) == 792
    assert d['available_predicate_count'] == 1888 and d['invalid_original_diagnostic_count'] == 64
    assert d['status'] == r['status'] and not any(d['physical_flags'].values())
    assert len(d['checkpoint_pairs']) == 928
    return d, r


def check(controls, name, error, tolerance, actual, expected):
    assert math.isfinite(float(error)) and error >= 0 and tolerance >= 0
    row = dict(name=name, error=float(error), tolerance=float(tolerance),
               actual=actual, expected=expected, passed=bool(error <= tolerance))
    controls.append(row)
    return row


def reference(theta, ell):
    """Fixed 96-term Decimal80 series or low-order upward recurrence."""
    if theta <= 10:
        with localcontext() as c:
            c.prec = 80
            x = Decimal.from_float(theta)
            odd = math.prod(range(1, 2 * ell + 2, 2))
            prefactor = Decimal(1) if ell == 0 else (x ** ell) / Decimal(odd)
            terms = [Decimal(1)]
            for m in range(95):
                terms.append(-terms[-1] * x * x / Decimal(2 * (m + 1) * (2 * ell + 2 * m + 3)))
            next_term = -terms[-1] * x * x / Decimal(2 * 96 * (2 * ell + 193))
            ratio_after_next = x * x / Decimal(2 * 97 * (2 * ell + 195))
            tail = abs(prefactor * next_term) / (Decimal(1) - ratio_after_next)
            value = prefactor * sum(terms, Decimal(0))
            if theta == 0:
                assert value == (Decimal(1) if ell == 0 else Decimal(0))
            return float(value), dict(method='Decimal80_series96', decimal_value=str(value),
                prefactor=str(prefactor), terms=[str(t) for t in terms],
                next_term=str(next_term), next_ratio=str(ratio_after_next), tail_bound=str(tail))
    values = upward(theta)
    return values[ell], dict(method='libm_upward_l0_to_l6', upward=values,
                            interval_certificate=False)


def upward(theta):
    assert theta > 0
    s, c = math.sin(theta), math.cos(theta)
    v = [s / theta, s / (theta * theta) - c / theta]
    for ell in range(1, 6):
        v.append((2 * ell + 1) * v[-1] / theta - v[-2])
    return v


def saved_phases(parent, controls):
    rows, arrays, records = [], [], []
    for ik, k in enumerate((.01, .1)):
        family = [r for r in parent['rows'] if r['trial']['arm'] == 'FINE' and r['trial']['k'] == k]
        assert len(family) == 4 and {r['trial']['omega'] for r in family} == {.1, 1., 10., 100.}
        family.sort(key=lambda r: r['trial']['omega'])
        samples = []
        RAW_META[f'phase_K{ik}_saved_families'] = samples
        for r in family:
            assert len(r['frames']) == 33 and r['trial']['nstep'] == 4096
            fields = []
            for j, f in enumerate(r['frames']):
                bg = f['background']
                assert f['nstep'] == 128 * j and bg['a'] == f['a']
                assert all(math.isfinite(bg[n]) and bg[n] > 0 for n in ('a', 'q', 'h'))
                fields.append(dict(nstep=f['nstep'], a=f['a'], q=bg['q'], h=bg['h']))
            if samples:
                assert fields == samples[0]['saved_fields']
            samples.append(dict(trial=r['trial'], terminal_checkpoint=r['terminal_checkpoint'], saved_fields=fields))
        f = samples[0]['saved_fields']
        x = [math.log(v['a']) for v in f]
        y = [v['q'] / v['h'] for v in f]
        assert all(x[j + 1] > x[j] for j in range(32))
        table = np.asarray([[v['a'], x[j], v['q'], v['h'], y[j]] for j, v in enumerate(f)], dtype=float)
        RAW[f'phase_K{ik}_samples'] = table
        trap = [0.]
        RAW[f'phase_K{ik}_trap'] = np.asarray(trap)
        for j in range(32):
            trap.append(trap[-1] + (x[j + 1] - x[j]) * (y[j] + y[j + 1]) / 2)
            RAW[f'phase_K{ik}_trap'] = np.asarray(trap)
        quad, panel_weights = [0.], []
        for j in range(0, 32, 2):
            h0, h1 = x[j + 1] - x[j], x[j + 2] - x[j + 1]
            length = h0 + h1
            w = [length * (2 - h1 / h0) / 6,
                 length ** 3 / (6 * h0 * h1), length * (2 - h0 / h1) / 6]
            panel_weights.append(w)
            RAW[f'phase_K{ik}_quadratic_weights'] = np.asarray(panel_weights)
            assert min(w) > 0
            nodes = [0., h0, length]
            actual = [sum(w[t] * nodes[t] ** power for t in range(3)) for power in range(3)]
            expected = [length ** (power + 1) / (power + 1) for power in range(3)]
            error = max(abs(a - b) for a, b in zip(actual, expected))
            check(controls, f'K{ik}_quadratic_panel_{j // 2}', error, 1e-12, actual, expected)
            quad.append(quad[-1] + sum(w[t] * y[j + t] for t in range(3)))
            RAW[f'phase_K{ik}_quadratic_even'] = np.asarray(quad)
        arrays.append(table)
        RAW[f'phase_K{ik}_trap'] = np.asarray(trap)
        RAW[f'phase_K{ik}_quadratic_even'] = np.asarray(quad)
        RAW[f'phase_K{ik}_quadratic_weights'] = np.asarray(panel_weights)
        rows.append(dict(k_Mpc_inverse=k, saved_family=samples, recorded_x=x, integrand=y,
            trapezoid_prefix=trap, quadratic_even_prefix=quad, quadratic_weights=panel_weights,
            terminal_trapezoid=trap[-1], terminal_quadratic=quad[-1],
            signed_quadratic_minus_trapezoid=quad[-1] - trap[-1],
            quadrature_orders=ORDERS, terminal_phase_over_order=[quad[-1] / n for n in ORDERS],
            exact_error_bound=None, original_background_evaluated=False))
        records.append(dict(k=k, sample_count=33, independent_inertia_copies=4))
    return rows, records


def checkpoint(label, arrays, metadata, manifest, outputs, pairs, failed=False):
    payload = J / (STEM + '_' + label + '.npz')
    commit = payload.with_name(payload.stem + '_COMMIT.json')
    descriptors = {n: dict(shape=list(a.shape), dtype=str(a.dtype), finite=bool(np.isfinite(a).all()))
                   for n, a in arrays.items()}
    assert failed or all(d['finite'] for d in descriptors.values())
    meta = dict(schema=1, label=label, pid=os.getpid(), owner='root-only numerical executor',
        source_sha256=manifest['source_sha256'], manifest_sha256=sha(J / (STEM + '_MANIFEST.json')),
        failed=failed, arrays=descriptors, metadata=metadata, physical_flags=FLAGS)
    encoded = encode(meta).decode()
    meta = json.loads(encoded)
    with payload.open('xb') as f:
        np.savez_compressed(f, meta=np.asarray(encoded), **arrays)
        f.flush(); os.fsync(f.fileno())
    d = dict(schema=1, payload=payload.name, payload_sha256=sha(payload), metadata=meta)
    write_json(commit, d)
    with np.load(payload, allow_pickle=False) as z:
        assert set(z.files) == set(arrays) | {'meta'}
        assert json.loads(str(z['meta'].item())) == meta
        for n, a in arrays.items():
            assert z[n].shape == a.shape and z[n].dtype == a.dtype
            assert np.array_equal(z[n], a, equal_nan=True)
    assert json.loads(commit.read_text()) == d
    outputs[payload.name] = sha(payload); outputs[commit.name] = sha(commit)
    pairs.append(d)


def final_recheck(inputs, outputs, pairs):
    for p, h in inputs.items():
        assert sha(p) == h
    for n, h in outputs.items():
        assert sha(J / n) == h
    for d in pairs:
        p = J / d['payload']; cp = p.with_name(p.stem + '_COMMIT.json')
        assert json.loads(cp.read_text()) == d and sha(p) == d['payload_sha256']
        with np.load(p, allow_pickle=False) as z:
            assert json.loads(str(z['meta'].item())) == d['metadata']
            assert set(z.files) == set(d['metadata']['arrays']) | {'meta'}
            for n, descriptor in d['metadata']['arrays'].items():
                assert list(z[n].shape) == descriptor['shape'] and str(z[n].dtype) == descriptor['dtype']
                assert bool(np.isfinite(z[n]).all()) == descriptor['finite']
    assert {p.name for p in J.glob(STEM + '_*.npz')} == {d['payload'] for d in pairs}
    assert {p.name for p in J.glob(STEM + '_*_COMMIT.json')} == {
        Path(d['payload']).stem + '_COMMIT.json' for d in pairs}


def main():
    if AUTHOR_GUARD:
        raise RuntimeError('UNEXECUTED AUTHOR GUARD: root may release only after full prospective review')
    assert not list(J.glob(STEM + '_*'))
    inputs = {}
    for n, h in PINS.items():
        bind(inputs, J / n, h)
    bind(inputs, J / (STEM + '.md'), PROTOCOL_SHA)
    bind(inputs, __file__, sha(__file__))
    parent, receipt = closed_parent(inputs)
    started, clock0 = now(), time.monotonic()
    manifest = dict(schema=1, owner='root-only numerical executor', pid=os.getpid(), started=started,
        source_sha256=sha(__file__), input_sha256=inputs, parent_status=parent['status'],
        thetas=THETAS, orders=ORDERS, multipoles=list(range(7)), series_terms=96,
        series_decimal_precision=80, series_tail_requirement='1e-30', moment_absolute_tolerance=MOMENT_TOL,
        arithmetic_expected_count=107, moment_outcome_expected_count=315, physical_flags=FLAGS)
    outputs, pairs, controls, outcomes = {}, [], [], []
    try:
        write_json(J / (STEM + '_MANIFEST.json'), manifest)
        outputs[STEM + '_MANIFEST.json'] = sha(J / (STEM + '_MANIFEST.json'))
        for k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
            os.environ[k] = '1'
        global np
        import numpy as np
        CONTEXT.update(stage='reference')
        refs, details, terms = [], [], []
        for it, theta in enumerate(THETAS):
            rr, dd, tt = [], [], []
            for ell in range(7):
                CONTEXT.update(theta=theta, ell=ell)
                value, detail = reference(theta, ell)
                RAW_META[f'reference_T{it}_L{ell}'] = detail
                RAW[f'reference_T{it}_L{ell}'] = np.asarray([value])
                rr.append(value); dd.append(detail)
                if theta <= 10:
                    RAW[f'reference_terms_T{it}_L{ell}'] = np.asarray([float(Decimal(t)) for t in detail['terms']])
                    tail = Decimal(detail['tail_bound'])
                    controls.append(dict(name=f'reference_tail_T{it}_L{ell}', actual=str(tail),
                        expected='<=1e-30', error=float(tail), tolerance=1e-30, passed=tail <= Decimal('1e-30')))
                    tt.append([float(Decimal(t)) for t in detail['terms']])
                else:
                    tt.append([0.] * 96)
            refs.append(rr); details.append(dd); terms.append(tt)
            RAW['reference_progress'] = np.asarray(refs)
            RAW['reference_terms_progress'] = np.asarray(terms)
        reference_array = np.asarray(refs)
        assert np.isfinite(reference_array).all()
        for ell, value in enumerate(upward(10.)):
            check(controls, f'reference_overlap_T10_L{ell}', abs(value - refs[3][ell]), 1e-13, value, refs[3][ell])
        for it in (1, 2, 3):
            for ell in range(1, 6):
                lhs = refs[it][ell - 1] - (2 * ell + 1) * refs[it][ell] / THETAS[it] + refs[it][ell + 1]
                check(controls, f'reference_recurrence_T{it}_L{ell}', abs(lhs), 1e-13, lhs, 0.)
        checkpoint('REFERENCE', dict(theta=np.asarray(THETAS), reference=reference_array,
            series_terms=np.asarray(terms)), dict(details=details, controls=controls), manifest, outputs, pairs)
        CONTEXT.update(stage='saved_phase_estimates')
        phase_rows, phase_census = saved_phases(parent, controls)
        checkpoint('SAVED_PHASE', {k: v for k, v in RAW.items() if k.startswith('phase_')},
                   dict(rows=phase_rows, controls=controls), manifest, outputs, pairs)
        for order in ORDERS:
            CONTEXT.clear(); CONTEXT.update(stage='GL_witness', order=order)
            mu, weight = np.polynomial.legendre.leggauss(order)
            RAW[f'N{order}_mu'] = mu; RAW[f'N{order}_weight'] = weight
            poly = np.empty((7, order)); poly[0] = 1.; poly[1] = mu
            for ell in range(1, 6):
                poly[ell + 1] = ((2 * ell + 1) * mu * poly[ell] - ell * poly[ell - 1]) / (ell + 1)
            RAW[f'N{order}_polynomial'] = poly
            phase = np.exp(-1j * np.asarray(THETAS)[:, None] * mu[None, :])
            RAW[f'N{order}_exponential'] = phase
            assert np.isfinite(mu).all() and np.isfinite(weight).all() and np.isfinite(poly).all() and np.isfinite(phase).all()
            check(controls, f'N{order}_positive_weights', 0. if np.min(weight) > 0 else 1., 0., float(np.min(weight)), '>0')
            check(controls, f'N{order}_mass', abs(float(np.sum(weight)) - 2.), 5e-13, float(np.sum(weight)), 2.)
            check(controls, f'N{order}_node_symmetry', float(np.max(abs(mu + mu[::-1]))), 5e-13, float(np.max(abs(mu + mu[::-1]))), 0.)
            check(controls, f'N{order}_weight_symmetry', float(np.max(abs(weight - weight[::-1]))), 5e-13, float(np.max(abs(weight - weight[::-1]))), 0.)
            gram = np.asarray([[np.sum(weight * poly[a] * poly[b]) for b in range(7)] for a in range(7)])
            expected_gram = np.diag([2. / (2 * ell + 1) for ell in range(7)])
            RAW[f'N{order}_Gram'] = gram; RAW[f'N{order}_expected_Gram'] = expected_gram
            check(controls, f'N{order}_Legendre_Gram', float(np.max(abs(gram - expected_gram))), 1e-11, gram.tolist(), expected_gram.tolist())
            moments = np.full((9, 7), complex(float('nan'), float('nan')), dtype=complex)
            RAW[f'N{order}_moments'] = moments
            local_outcomes = []
            for it, theta in enumerate(THETAS):
                for ell in range(7):
                    value = (1j ** ell) * np.sum(weight * poly[ell] * phase[it]) / 2
                    moments[it, ell] = value
                    CONTEXT.update(theta=theta, ell=ell)
                    row = dict(order=order, theta=theta, ell=ell, real=float(value.real), imaginary=float(value.imag),
                        reference=refs[it][ell], signed_real_difference=float(value.real - refs[it][ell]),
                        absolute_complex_error=float(abs(value - refs[it][ell])), tolerance=MOMENT_TOL,
                        passed=bool(abs(value - refs[it][ell]) <= MOMENT_TOL), physical_qualification=False)
                    local_outcomes.append(row); outcomes.append(row)
            RAW[f'N{order}_moments'] = moments
            checkpoint(f'GL_N{order:04d}', dict(mu=mu, weight=weight, polynomial=poly, exponential=phase,
                moments=moments, reference=reference_array, Gram=gram, expected_Gram=expected_gram),
                dict(order=order, outcomes=local_outcomes, controls=controls), manifest, outputs, pairs)
        assert len(controls) == 107 and len(outcomes) == 315 and len(pairs) == 7
        result = dict(status='ANGULAR_WITNESS_COMPLETE' if all(c['passed'] for c in controls) else 'ARITHMETIC_CONTROL_FAILED',
            manifest=manifest, arithmetic_controls=controls, moment_outcomes=outcomes,
            reference_details=details, phase_estimates=phase_rows, phase_census=phase_census,
            checkpoint_pairs=pairs, parent_controls_copied_exactly=parent['controls'],
            parent_registration_copied_exactly=parent['sample_registration_controls'],
            parent_comparisons_copied_exactly=parent['comparisons'], parent_qualification_copied_exactly=parent['qualification'],
            parent_status=parent['status'], parent_physical_flags_copied_exactly=parent['physical_flags'],
            moment_pass_count=sum(c['passed'] for c in outcomes), moment_fail_count=sum(not c['passed'] for c in outcomes),
            elapsed_seconds=time.monotonic() - clock0, physical_flags=FLAGS)
        write_json(J / (STEM + '_RESULT.json'), result)
        outputs[STEM + '_RESULT.json'] = sha(J / (STEM + '_RESULT.json'))
        report = ('# Free-streaming angular quadrature witness\n\n'
            f"{result['status']}: {len(controls)} arithmetic controls; {result['moment_pass_count']}/{len(outcomes)} fixed absolute moment outcomes pass.\n\n"
            'All outcomes, kernels, references and saved phase estimates are retained. The estimates have no exact error bound. '
            'This witness neither repairs the original ANGLE failures nor qualifies the prepared universe.\n').encode()
        put(J / (STEM + '_REPORT.md'), report)
        outputs[STEM + '_REPORT.md'] = sha(J / (STEM + '_REPORT.md'))
        final_recheck(inputs, outputs, pairs)
        rc = dict(status=result['status'], pid=os.getpid(), owner=manifest['owner'], started=started, closed=now(),
            input_sha256=inputs, output_sha256=outputs, source_sha256=sha(__file__),
            result_sha256=outputs[STEM + '_RESULT.json'], checkpoint_pairs=7,
            arithmetic_count=107, moment_outcome_count=315, physical_flags=FLAGS)
        write_json(J / (STEM + '_RECEIPT.json'), rc)
        final_recheck(inputs, outputs, pairs)
        assert json.loads((J / (STEM + '_RECEIPT.json')).read_text()) == rc
        return 0 if result['status'] == 'ANGULAR_WITNESS_COMPLETE' else 3
    except Exception as exc:
        existing_receipt = J / (STEM + '_RECEIPT.json')
        protected_receipt = sha(existing_receipt) if existing_receipt.exists() else None
        if protected_receipt is not None:
            outputs[existing_receipt.name] = protected_receipt
        if 'np' in globals() and RAW:
            checkpoint('ERROR_RAW', RAW, dict(context=CONTEXT, controls=controls, outcomes=outcomes,
                       progressive_metadata=RAW_META),
                       manifest, outputs, pairs, failed=True)
        error = dict(status='ERROR', pid=os.getpid(), started=started, closed=now(), context=dict(CONTEXT),
            exception=type(exc).__name__, message=str(exc), traceback=traceback.format_exc(),
            input_sha256=inputs, output_sha256=dict(outputs), checkpoint_pairs=pairs,
            arithmetic_controls=controls, moment_outcomes=outcomes, physical_flags=FLAGS,
            protected_existing_receipt_sha256=protected_receipt)
        write_json(J / (STEM + '_ERROR.json'), error)
        outputs[STEM + '_ERROR.json'] = sha(J / (STEM + '_ERROR.json'))
        final_recheck(inputs, outputs, pairs)
        if protected_receipt is None:
            rc = dict(error, output_sha256=dict(outputs))
            write_json(existing_receipt, rc)
            assert json.loads(existing_receipt.read_text()) == rc
        else:
            assert sha(existing_receipt) == protected_receipt
        final_recheck(inputs, outputs, pairs)
        return 1


if __name__ == '__main__':
    sys.exit(main())

"""Guarded source-operator arithmetic witness; root numerical executor only."""
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal, localcontext
import ast, hashlib, json, math, os, sys, time, traceback

J = Path(__file__).resolve().parent
STEM = 'CROSS_U_RETARDED_RADIATION_SOURCE_OPERATOR_WITNESS_V001'
AUTHOR_GUARD = False
PROTOCOL_SHA = '24698c8614122fc7b893bfd1151560ae050e9487aa10338ebfd65c3deb9bdebf'
FREE = 'CROSS_U_FREE_STREAMING_ANGULAR_QUADRATURE_WITNESS_V001'
OLD = 'CONSTRAINED_U_RETARDED_RADIATION_KERNEL_CONTROLS_V001'
ORIGINAL = 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001'
PINS = {
    'CROSS_U_EXACT_RETARDED_RADIATION_MOMENT_OPERATOR_V001.md': 'c4fcedb21d45274bc6632b755e87c6eacf566f5d84268d103e625990bc299752',
    'cross_u_full_flrw_source_constraint_v001.py': '8e2860917a75c44ada5be0df18ac43809dc7fe454846b3787d8a3d3017d1e5c1',
    'CROSS_U_FULL_FLRW_SOURCE_CONSTRAINT_AND_FINITE_SLICE_TEST_V001.md': 'c81fa7ed6961f5f0620bbb48dd133ef474543765131ceb738bdcf676f9b9a986',
    'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_ERROR_RAW.npz': '06646ec193334c46d84586c84814e5ad2f58f96ce7624a7dde019f8ba226c5a2',
    'CROSS_U_FREE_STREAMING_ANGULAR_QUADRATURE_WITNESS_V001_RESULT.json': 'e17f6e658c72db576945f865c72aa5886f90d64f130112d8f0af5ee9d949bad3',
    'CROSS_U_FREE_STREAMING_ANGULAR_QUADRATURE_WITNESS_V001_RECEIPT.json': 'a0974c6337ee1c39d054b135f6817a08197d064718410ace9f2ef847d1c6411b',
    'constrained_u_retarded_radiation_kernel_controls_v001.py': 'dc7885ee0349145f05a7e18bf9ce48bf257626ebbc4bd48ebc366791fe456db2',
    'CONSTRAINED_U_RETARDED_RADIATION_KERNEL_CONTROLS_V001_RESULT.json': 'b541b0a5e3f2ea1827f166907f96e9b76bf2d2ad4c6366c3a0efbf15a7661530',
    'CONSTRAINED_U_RETARDED_RADIATION_KERNEL_CONTROLS_V001_RECEIPT.json': '9e845b9a18035b4b199ac0f3a6153b4123f1816c353bdec0e0ef7fdaddaf19dc',
    'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O0_CP_000000.npz': '9121d9919cada1ed35c784956f62feab3787be6cb3ca60e15e95dd9a1be47706',
    'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O0_CP_000000_COMMIT.json': '854bb57a25d5e43b675e315d1e3a8c9d62eb64f0571b089d44191fe13f01303b',
    'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O0_CP_000000.npz': '72aa7178724affa2a06c97e1f3990872670ed85df0cce720beca2b21f6c05879',
    'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O0_CP_000000_COMMIT.json': '43a762492edf95003e26c12c11ec3d34dead48b67b1da5760411607187537d95',
    'reviewed_cross_u_retarded_radiation_source_operator_witness_v001_505_0a73bb33.py': '0a73bb332d297a091e32979d1dbe3f12dec80998db77c739c8381c18b25743d3',
    'reviewed_CROSS_U_RETARDED_RADIATION_SOURCE_OPERATOR_WITNESS_V001_31_a9c89004.md': 'a9c8900408ffbfd96b1cb15fbc57cafe7d9a37223806e5f577541608b16d8cc1',
}
WIDTHS = (.1, 1., 12.)
TIME_ORDERS = (16, 32, 64)
ANGLE_ORDERS = (1536, 2048)
PASTS = (30., 300., 1300., 2000.)
REFERENCE_PHASES = (0., .1, 1., 10., 30., 300., 1300., 2000., 2012.)
FREE_PHASES = (0., 30., 300., 1300., 2000.)
TOL = 1e-10
CFG = {'series_terms': 52}
FLAGS = dict(full_trajectory=False, prepared_universe=False, original_angle_repaired=False,
             original_radiation_gate_repaired=False, nonlinear_clock=False,
             physical_growth=False, physical_lensing=False, native_inertia=False)
RAW, RAW_META, CONTEXT = {}, {}, {}


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def encode(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False)+'\n').encode()


def put(path, raw):
    with Path(path).open('xb') as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    assert Path(path).read_bytes() == raw


def write_json(path, value):
    put(path, encode(value))


def bind(inputs, path, expected):
    p = Path(path)
    if not p.is_absolute():
        p = J/p
    p = p.resolve()
    assert sha(p) == expected, str(p)
    assert str(p) not in inputs or inputs[str(p)] == expected
    inputs[str(p)] = expected


def closed_maps(inputs, stem, status):
    rc = json.loads((J/(stem+'_RECEIPT.json')).read_text())
    result = json.loads((J/(stem+'_RESULT.json')).read_text())
    assert rc['status'] == status == result['status']
    assert rc['result_sha256'] == sha(J/(stem+'_RESULT.json'))
    for key in ('input_sha256', 'output_sha256'):
        for path, h in rc[key].items():
            bind(inputs, path, h)
    return result, rc


def compare(rows, name, actual, expected, tolerance=TOL):
    actual, expected = np.asarray(actual), np.asarray(expected)
    RAW[name+'_actual'] = actual.copy(); RAW[name+'_expected'] = expected.copy()
    assert actual.shape == expected.shape and actual.size
    assert np.isfinite(actual).all() and np.isfinite(expected).all()
    delta = actual-expected
    index = np.unravel_index(int(np.argmax(abs(delta))), delta.shape)
    error = float(abs(delta[index])); v = complex(delta[index])
    row = dict(name=name, shape=list(actual.shape), absolute_error=error, tolerance=tolerance,
               first_max_index=list(index), signed_difference_real=float(v.real),
               signed_difference_imaginary=float(v.imag), passed=bool(error <= tolerance),
               actual_array=name+'_actual', expected_array=name+'_expected')
    rows.append(row)
    return row


def upward(theta):
    assert theta > 0
    sn, cs = math.sin(theta), math.cos(theta)
    values = [sn/theta, sn/(theta*theta)-cs/theta]
    for ell in range(1, 8):
        values.append((2*ell+1)*values[-1]/theta-values[-2])
    return values


def reference(theta, ell):
    assert math.isfinite(theta) and theta >= 0 and 0 <= ell <= 8
    if theta > 10:
        return upward(theta)[ell], dict(method='libm_upward_l0_to_l8', interval_certificate=False)
    with localcontext() as ctx:
        ctx.prec = 80
        x = Decimal.from_float(theta)
        pref = Decimal(1) if ell == 0 else x**ell/Decimal(math.prod(range(1, 2*ell+2, 2)))
        terms = [Decimal(1)]
        for m in range(95):
            terms.append(-terms[-1]*x*x/Decimal(2*(m+1)*(2*ell+2*m+3)))
        nxt = -terms[-1]*x*x/Decimal(2*96*(2*ell+193))
        ratio = x*x/Decimal(2*97*(2*ell+195))
        tail = abs(pref*nxt)/(1-ratio)
        value = pref*sum(terms, Decimal(0))
        detail = dict(method='Decimal80_series96', decimal_value=str(value),
                      tail_bound=str(tail), next_term=str(nxt), next_ratio=str(ratio),
                      prefactor=str(pref), terms=[str(t) for t in terms])
        RAW_META['last_reference_detail'] = detail
        assert tail <= Decimal('1e-30')
        return float(value), detail


def kernels(arguments):
    RAW['last_kernel_arguments'] = np.asarray(arguments).copy()
    rows = []
    for t in arguments:
        rows.append([reference(float(t), ell)[0] for ell in range(9)])
        RAW['last_kernel_j'] = np.asarray(rows)
    j = np.asarray(rows)
    d1, d2 = np.empty((len(arguments), 7)), np.empty((len(arguments), 7))
    d1[:, 0] = -j[:, 1]
    for ell in range(1, 7):
        d1[:, ell] = (ell*j[:, ell-1]-(ell+1)*j[:, ell+1])/(2*ell+1)
    d2[:, 0] = (2*j[:, 2]-j[:, 0])/3
    d2[:, 1] = (2*j[:, 3]-3*j[:, 1])/5
    for ell in range(2, 7):
        d2[:, ell] = (ell*(ell-1)*j[:, ell-2]/((2*ell+1)*(2*ell-1))
            -(ell*ell/((2*ell+1)*(2*ell-1))+(ell+1)**2/((2*ell+1)*(2*ell+3)))*j[:, ell]
            +(ell+1)*(ell+2)*j[:, ell+2]/((2*ell+1)*(2*ell+3)))
    RAW['last_kernel_d1'] = d1.copy(); RAW['last_kernel_d2'] = d2.copy()
    assert np.isfinite(j).all() and np.isfinite(d1).all() and np.isfinite(d2).all()
    return j, d1, d2


def complex_moment(p,z):
    z=np.asarray(z,dtype=complex);out=np.zeros_like(z);small=abs(z)<1
    v=z[small];term=np.ones_like(v);ans=np.zeros_like(v)
    for m in range(CFG['series_terms']):
        ans+=term/(m+p+1);term*=-v/(m+1)
    out[small]=ans
    v=z[~small];end=np.exp(-v);value=-np.expm1(-v)/v
    for order in range(1,p+1):value=(order*value-end)/v
    out[~small]=value;return out


def cardinal_coefficients(fractions):
    coef = np.zeros((4, 4))
    for k in range(4):
        poly, denominator = np.asarray([1.]), 1.
        for m in range(4):
            if m != k:
                poly = np.convolve(poly, np.asarray([-fractions[m], 1.]))
                denominator *= fractions[k]-fractions[m]
        coef[:, k] = poly/denominator
    return coef


def cardinal(coef, u):
    return sum(np.asarray(u)[:, None]**m*coef[m][None, :] for m in range(4))


def gauss(order, controls, angular=False):
    node, weight = np.polynomial.legendre.leggauss(order)
    RAW['last_gauss_node'] = node.copy(); RAW['last_gauss_weight'] = weight.copy()
    assert np.isfinite(node).all() and np.isfinite(weight).all() and min(weight) > 0
    if not angular:
        return node, weight
    poly = np.empty((7, order)); poly[0] = 1.; poly[1] = node
    for ell in range(1, 6):
        poly[ell+1] = ((2*ell+1)*node*poly[ell]-ell*poly[ell-1])/(ell+1)
    RAW['last_gauss_polynomial'] = poly.copy()
    compare(controls, f'GL{order}_positive_weights', np.asarray([max(0., -float(min(weight)))]), np.asarray([0.]), 0.)
    compare(controls, f'GL{order}_mass', np.asarray([sum(weight)]), np.asarray([2.]), 5e-13)
    compare(controls, f'GL{order}_node_symmetry', node+node[::-1], np.zeros(order), 5e-13)
    compare(controls, f'GL{order}_weight_symmetry', weight-weight[::-1], np.zeros(order), 5e-13)
    gram = np.asarray([[sum(weight*poly[a]*poly[b]) for b in range(7)] for a in range(7)])
    compare(controls, f'GL{order}_Gram', gram, np.diag([2/(2*ell+1) for ell in range(7)]), 1e-11)
    return node, weight, poly


def project(field, rule):
    _, weight, poly = rule
    return np.stack([(1j**ell)*np.sum(field*weight*poly[ell], axis=-1)/2 for ell in range(7)], axis=-2)


def characteristic(coef, width, upper, target, mu):
    moments = np.stack([upper**(p+1)*complex_moment(p, -1j*mu*width*upper) for p in range(4)])
    exponential = np.exp(-1j*mu*target)
    RAW['last_characteristic_moments'] = moments.copy(); RAW['last_characteristic_exponential'] = exponential.copy()
    r = sum(m*coef[m, :, None]*moments[m-1] for m in range(1, 4))
    a = -width*mu[None, :]**2*sum(coef[m, :, None]*moments[m] for m in range(4))
    c = 1j*width*mu[None, :]*sum(coef[m, :, None]*moments[m] for m in range(4))
    field = 4*exponential[None, None, :]*np.stack([r, a, c])
    RAW['last_characteristic_field'] = field.copy()
    assert np.isfinite(field).all()
    return field, moments, exponential


def bessel_operator(coef, width, upper, target, rule):
    node, weight = rule
    u = upper*(node+1)/2; w = upper*weight/2
    lagrange = cardinal(coef, u); delta = lagrange.copy(); delta[:, 0] -= 1.
    endpoint = cardinal(coef, np.asarray([upper]))[0]; endpoint[0] -= 1.
    RAW.update(current_bessel_u=u.copy(), current_bessel_weight=w.copy(),
        current_bessel_lagrange=lagrange.copy(), current_bessel_delta_R=delta.copy(),
        current_bessel_endpoint=endpoint.copy())
    j, d1, d2 = kernels(target-width*u)
    boundary = np.asarray([reference(target-width*upper, ell)[0] for ell in range(7)])
    tensor = np.empty((3, 7, 4))
    for ell in range(7):
        tensor[0, ell] = 4*boundary[ell]*endpoint+4*width*np.sum(w[:, None]*d1[:, ell, None]*delta, axis=0)
        tensor[1, ell] = 4*width*np.sum(w[:, None]*d2[:, ell, None]*lagrange, axis=0)
        tensor[2, ell] = -4*width*np.sum(w[:, None]*d1[:, ell, None]*lagrange, axis=0)
    return tensor, dict(u=u, weight=w, lagrange=lagrange, delta_R=delta,
                        arguments=target-width*u, j=j, d1=d1, d2=d2, boundary=boundary)


def flux_operator(coef, width, upper, rule):
    node, weight = rule
    u = upper*(node+1)/2; w = upper*weight/2
    lagrange = cardinal(coef, u); delta = lagrange.copy(); delta[:, 0] -= 1.
    RAW.update(current_flux_u=u.copy(), current_flux_weight=w.copy(),
        current_flux_lagrange=lagrange.copy(), current_flux_delta_R=delta.copy())
    j, d1, d2 = kernels(width*(upper-u))
    tensor = 4*width*np.stack([np.sum(w[:, None]*j[:, 1, None]*delta, axis=0),
        np.sum(w[:, None]*d1[:, 1, None]*lagrange, axis=0),
        -np.sum(w[:, None]*j[:, 1, None]*lagrange, axis=0)])
    return tensor, dict(u=u, weight=w, lagrange=lagrange, delta_R=delta, j=j, d1=d1, d2=d2)


def characteristic_flux(coef, width, upper, time_rule, angle_rule):
    node, weight = time_rule
    u = upper*(node+1)/2; w = upper*weight/2
    projected, moments, exponentials = [], [], []
    RAW['flux_projected_progress'] = np.empty((0, 3, 4), complex)
    for v in u:
        field, im, exp = characteristic(coef, width, float(v), width*float(v), angle_rule[0])
        # Only the independently integrated Y1 enters this separate balance reference.
        y1 = 1j*np.sum(field*angle_rule[1]*angle_rule[2][1], axis=-1)/2
        projected.append(y1); moments.append(im); exponentials.append(exp)
        RAW['flux_projected_progress'] = np.asarray(projected)
        RAW['flux_moments_progress'] = np.asarray(moments)
        RAW['flux_exponentials_progress'] = np.asarray(exponentials)
    projected = np.asarray(projected)
    shifted = projected.copy(); shifted[:, 1, :] += 4*cardinal(coef, u)/3
    value = width*np.sum(w[:, None, None]*shifted, axis=0)
    return value, dict(u=u, weight=w, projected_Y1=projected, shifted_flux=shifted,
                       moments=np.asarray(moments), exponential=np.asarray(exponentials))


def checkpoint(label, arrays, metadata, manifest, outputs, pairs, failed=False):
    descriptors = {n: dict(shape=list(v.shape), dtype=str(v.dtype), finite=bool(np.isfinite(v).all())) for n, v in arrays.items()}
    assert failed or all(d['finite'] for d in descriptors.values())
    meta = dict(schema=1, label=label, failed=failed, owner='root', pid=os.getpid(),
                source_sha256=manifest['source_sha256'], manifest_sha256=sha(J/(STEM+'_MANIFEST.json')),
                arrays=descriptors, metadata=metadata, physical_flags=FLAGS)
    text = encode(meta).decode(); meta = json.loads(text)
    payload = J/(STEM+'_'+label+'.npz'); commit = payload.with_name(payload.stem+'_COMMIT.json')
    with payload.open('xb') as f:
        np.savez_compressed(f, metadata=np.asarray(text), **arrays); f.flush(); os.fsync(f.fileno())
    record = dict(schema=1, payload=payload.name, payload_sha256=sha(payload), metadata=meta)
    write_json(commit, record)
    with np.load(payload, allow_pickle=False) as z:
        assert set(z.files) == set(arrays)|{'metadata'} and json.loads(str(z['metadata'])) == meta
        for n, v in arrays.items():
            assert z[n].shape == v.shape and z[n].dtype == v.dtype and np.array_equal(z[n], v, equal_nan=True)
    assert json.loads(commit.read_text()) == record
    outputs[payload.name] = sha(payload); outputs[commit.name] = sha(commit); pairs.append(record)


def final_recheck(inputs, outputs, pairs):
    for p, h in inputs.items():
        assert sha(p) == h
    for n, h in outputs.items():
        assert sha(J/n) == h
    for record in pairs:
        p = J/record['payload']; commit = p.with_name(p.stem+'_COMMIT.json')
        assert sha(p) == record['payload_sha256'] and json.loads(commit.read_text()) == record
        with np.load(p, allow_pickle=False) as z:
            assert json.loads(str(z['metadata'])) == record['metadata']
            assert set(z.files) == set(record['metadata']['arrays'])|{'metadata'}
            for n, d in record['metadata']['arrays'].items():
                assert list(z[n].shape) == d['shape'] and str(z[n].dtype) == d['dtype']
                assert bool(np.isfinite(z[n]).all()) == d['finite']
    assert {p.name for p in J.glob(STEM+'_*.npz')} == {r['payload'] for r in pairs}
    assert {p.name for p in J.glob(STEM+'_*_COMMIT.json')} == {Path(r['payload']).stem+'_COMMIT.json' for r in pairs}


def main():
    if AUTHOR_GUARD:
        raise RuntimeError('UNEXECUTED author guard; root release after FULL prospective reviews only')
    assert not list(J.glob(STEM+'_*'))
    inputs = {}
    for n, h in PINS.items():
        bind(inputs, J/n, h)
    bind(inputs, J/(STEM+'.md'), PROTOCOL_SHA); bind(inputs, __file__, sha(__file__))
    free, free_receipt = closed_maps(inputs, FREE, 'ANGULAR_WITNESS_COMPLETE')
    old, old_receipt = closed_maps(inputs, OLD, 'PASS_KERNEL_ARITHMETIC')
    assert len(free['arithmetic_controls']) == 107 and len(free['moment_outcomes']) == 315
    assert free['moment_fail_count'] == 84 and not any(free['physical_flags'].values())
    literal = (J/'constrained_u_retarded_radiation_kernel_controls_v001.py').read_text()
    tree = ast.parse(literal)
    parent_helper = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'complex_moment')
    own = ast.parse(Path(__file__).read_text())
    own_helper = next(n for n in own.body if isinstance(n, ast.FunctionDef) and n.name == 'complex_moment')
    assert ast.dump(parent_helper, include_attributes=False) == ast.dump(own_helper, include_attributes=False)
    started, tick = now(), time.monotonic()
    manifest = dict(schema=1, owner='root', pid=os.getpid(), started=started, source_sha256=sha(__file__),
        input_sha256=inputs, widths=WIDTHS, time_orders=TIME_ORDERS, angle_orders=ANGLE_ORDERS,
        pasts=PASTS, ell=list(range(7)), kernel_ell=list(range(9)), operator_absolute_tolerance=TOL,
        arithmetic_expected_count=130, outcome_expected_count=81, checkpoint_expected_count=36,
        geometry='Actual original phase_theta16 fractions; manufactured widths only', physical_flags=FLAGS)
    controls, outcomes, outputs, pairs, panel_rows, flux_rows, prep_rows = [], [], {}, [], [], [], []
    try:
        write_json(J/(STEM+'_MANIFEST.json'), manifest); outputs[STEM+'_MANIFEST.json'] = sha(J/(STEM+'_MANIFEST.json'))
        for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
            os.environ[name] = '1'
        global np
        import numpy as np
        CONTEXT.update(stage='reference'); RAW.clear()
        values, details = [], []
        for it, theta in enumerate(REFERENCE_PHASES):
            rr, dd = [], []
            for ell in range(9):
                value, detail = reference(theta, ell); rr.append(value); dd.append(detail)
                if theta <= 10:
                    tail = Decimal(detail['tail_bound'])
                    controls.append(dict(name=f'tail_{it}_{ell}', actual=str(tail), expected='<=1e-30',
                        absolute_error=float(tail), tolerance=1e-30, passed=tail <= Decimal('1e-30')))
            values.append(rr); details.append(dd); RAW['reference_progress'] = np.asarray(values)
        refs = np.asarray(values)
        # Nine separate overlap controls preserve each low-order kernel witness.
        for ell in range(9):
            compare(controls, f'overlap_10_{ell}', np.asarray([upward(10.)[ell]]), refs[3, ell:ell+1], 1e-13)
        for it in (1, 2, 3):
            for ell in range(1, 8):
                v = refs[it, ell-1]-(2*ell+1)*refs[it, ell]/REFERENCE_PHASES[it]+refs[it, ell+1]
                compare(controls, f'recurrence_{it}_{ell}', np.asarray([v]), np.asarray([0.]), 1e-13)
        j0, d10, d20 = kernels(np.asarray([0.]))
        compare(controls, 'zero_j', j0[0], np.asarray([1.]+[0.]*8), 0.)
        compare(controls, 'zero_d1', d10[0], np.asarray([0., 1/3]+[0.]*5), 0.)
        compare(controls, 'zero_d2', d20[0], np.asarray([-1/3, 0., 2/15]+[0.]*4), 0.)
        checkpoint('REFERENCE', dict(RAW), dict(details=details, controls=controls), manifest, outputs, pairs)
        angle_rules = {}
        for order in ANGLE_ORDERS:
            RAW.clear(); CONTEXT.update(stage='angular_rule', order=order)
            angle_rules[order] = gauss(order, controls, True)
            checkpoint(f'GL{order}', dict(RAW), dict(order=order, controls=controls), manifest, outputs, pairs)
        RAW.clear(); CONTEXT.update(stage='actual_phase_geometry')
        with np.load(J/(ORIGINAL+'_ERROR_RAW.npz'), allow_pickle=False) as z:
            theta = z['phase_theta16'].copy(); theta8 = z['phase_theta8'].copy()
        RAW['phase_theta16'] = theta; RAW['phase_theta8'] = theta8
        assert theta.shape == theta8.shape == (4,) and theta.dtype == theta8.dtype == np.dtype('float64')
        assert np.isfinite(theta).all() and np.isfinite(theta8).all() and np.all(np.diff(theta) > 0)
        fractions = (theta-theta[0])/(theta[-1]-theta[0]); fractions[0], fractions[-1] = 0., 1.
        coef = cardinal_coefficients(fractions); RAW['fractions'] = fractions; RAW['cardinal_coefficients'] = coef
        compare(controls, 'cardinal_at_actual_nodes', cardinal(coef, fractions), np.eye(4), 1e-13)
        time_rules = {n: gauss(n, controls) for n in TIME_ORDERS}
        for order in TIME_ORDERS:
            node, weight = time_rules[order]
            actual = np.asarray([[sum((b*(node+1)/2)**p*b*weight/2) for p in range(4)] for b in fractions[1:]])
            expected = np.asarray([[b**(p+1)/(p+1) for p in range(4)] for b in fractions[1:]])
            compare(controls, f'time{order}_partial_monomials', actual, expected, 1e-13)
        mus = np.asarray([-1., -.7, 0., .31, 1.]); node, weight = time_rules[64]
        for iw, width in enumerate(WIDTHS):
            for ib, b in enumerate(fractions[1:]):
                actual = np.asarray([b**(p+1)*complex_moment(p, -1j*mus*width*b) for p in range(4)])
                u = b*(node+1)/2
                expected = np.asarray([np.sum((b*weight/2*u**p)[:, None]*np.exp(1j*u[:, None]*width*mus), axis=0) for p in range(4)])
                compare(controls, f'moment_p3_width{iw}_partial{ib}', actual, expected)
        checkpoint('GEOMETRY', dict(RAW), dict(phase_geometry_source=ORIGINAL+'_ERROR_RAW.npz',
            fractions=fractions.tolist(), controls=controls), manifest, outputs, pairs)
        for ik in range(2):
            RAW.clear(); CONTEXT.update(stage='full_owned_initial', k_index=ik)
            stem = ORIGINAL+f'_FINE_K{ik}_O0_CP_000000'
            cp = json.loads((J/(stem+'_COMMIT.json')).read_text())
            with np.load(J/(stem+'.npz'), allow_pickle=False) as z:
                meta = json.loads(str(z['metadata'])); initial = {n:z[n].copy() for n in z.files if n != 'metadata'}
            RAW.update({'initial_'+n:v for n, v in initial.items()})
            assert cp['payload_sha256'] == sha(J/(stem+'.npz')) and cp['metadata'] == meta and cp['nstep'] == 0 and not cp['failed']
            assert initial['core'].shape == (11, 2) and initial['angular'].shape == (81, 2)
            gamma = initial['core'][8].copy()
            compare(controls, f'initial_K{ik}_complete_constant_Y', initial['angular'], np.repeat(gamma[None, :], 81, axis=0), 0.)
            predicted = np.asarray([[reference(t, ell)[0] for ell in range(7)] for t in FREE_PHASES])[:, :, None]*gamma
            free_values = {}
            for order in ANGLE_ORDERS:
                mu, weight, poly = angle_rules[order]
                exp = np.exp(-1j*np.asarray(FREE_PHASES)[:, None]*mu)
                RAW[f'free{order}_exponential'] = exp
                free_values[order] = np.stack([project(exp[i][None, :]*gamma[:, None], angle_rules[order]) for i in range(5)])
                compare(controls, f'initial_K{ik}_free{order}', free_values[order], predicted)
            compare(controls, f'initial_K{ik}_reference_difference', free_values[1536], free_values[2048])
            prep_rows.append(dict(k_index=ik, original_checkpoint=cp, metadata=meta, gamma=gamma.tolist(),
                free_phases=FREE_PHASES, physical_initial_shift='F=Y-4hV-i4qVmu; original complete Y retained'))
            checkpoint(f'INITIAL_K{ik}', dict(RAW), dict(row=prep_rows[-1], controls=controls), manifest, outputs, pairs)
        settings = [(float(b), 0., f'CURRENT{ib}') for ib, b in enumerate(fractions[1:])]+[(1., p, f'PAST{ip}') for ip, p in enumerate(PASTS)]
        for iw, width in enumerate(WIDTHS):
            for it, (upper, past, label) in enumerate(settings):
                RAW.clear(); CONTEXT.clear(); CONTEXT.update(stage='source_panel', width=width, upper=upper, past=past)
                target = width*upper+past; refs_by_order = {}
                for order in ANGLE_ORDERS:
                    field, im, exp = characteristic(coef, width, upper, target, angle_rules[order][0])
                    refs_by_order[order] = project(field, angle_rules[order])
                    RAW[f'char{order}_field'] = field; RAW[f'char{order}_moments'] = im
                    RAW[f'char{order}_exponential'] = exp; RAW[f'char{order}_projected'] = refs_by_order[order]
                compare(controls, f'panel{iw}_{it}_angular_reference', refs_by_order[1536], refs_by_order[2048])
                by_time = {}
                for order in TIME_ORDERS:
                    tensor, arrays = bessel_operator(coef, width, upper, target, time_rules[order])
                    by_time[order] = tensor
                    RAW.update({f'time{order}_{n}':v for n, v in arrays.items()}); RAW[f'time{order}_tensor'] = tensor
                    compare(outcomes, f'panel{iw}_{it}_time{order}', tensor, refs_by_order[2048])
                RAW['signed_time32_minus16'] = by_time[32]-by_time[16]
                RAW['signed_time64_minus32'] = by_time[64]-by_time[32]
                RAW['signed_time64_minus16'] = by_time[64]-by_time[16]
                row = dict(width=width, upper_fraction=upper, past_phase=past, target_phase=target, label=label,
                    characteristic_angular_orders=ANGLE_ORDERS, source_tensor_shape=[3, 7, 4],
                    sources=['R', 'qV', 'cs_squared_Gamma_phi'], time_refinement_maxima={
                    '32_minus16':float(np.max(abs(by_time[32]-by_time[16]))),
                    '64_minus32':float(np.max(abs(by_time[64]-by_time[32]))),
                    '64_minus16':float(np.max(abs(by_time[64]-by_time[16])))})
                panel_rows.append(row)
                checkpoint(f'PANEL{iw}_{it}', dict(RAW), dict(row=row, outcomes=outcomes[-3:], controls=controls), manifest, outputs, pairs)
            for ib, upper in enumerate(fractions[1:]):
                RAW.clear(); CONTEXT.clear(); CONTEXT.update(stage='independent_balance_flux', width=width, upper=float(upper))
                fluxes = {}
                for order in ANGLE_ORDERS:
                    flux, arrays = characteristic_flux(coef, width, float(upper), time_rules[64], angle_rules[order])
                    fluxes[order] = flux; RAW[f'charflux{order}_value'] = flux
                    RAW.update({f'charflux{order}_{n}':v for n, v in arrays.items()})
                compare(controls, f'flux{iw}_{ib}_angular_reference', fluxes[1536], fluxes[2048])
                tensor, arrays = flux_operator(coef, width, float(upper), time_rules[64])
                RAW['bessel_flux'] = tensor; RAW.update({'flux_'+n:v for n, v in arrays.items()})
                compare(outcomes, f'flux{iw}_{ib}_independent_method', tensor, fluxes[2048])
                field, im, exp = characteristic(coef, width, float(upper), width*float(upper), angle_rules[2048][0])
                endpoint_Y0 = project(field, angle_rules[2048])[:, 0, :]
                boundary = np.zeros((3, 4)); boundary[0] = 4*(cardinal(coef, np.asarray([upper]))[0]-np.asarray([1., 0., 0., 0.]))
                RAW['balance_endpoint_characteristic_field'] = field; RAW['balance_endpoint_Y0'] = endpoint_Y0
                compare(outcomes, f'flux{iw}_{ib}_independent_density_balance', endpoint_Y0+fluxes[2048], boundary)
                row = dict(width=width, upper_fraction=float(upper), incoming_Y='zero for the cardinal source tensor only',
                    balance='DeltaY0+independently integrated(Y1+4A/3)=4DeltaR',
                    actual_contrast='Deltadelta_r=4DeltaPsi-integral(Y1+4A/3); varying hV shift retained',
                    original_two_log_a_node_gate_replaced=False)
                flux_rows.append(row)
                checkpoint(f'FLUX{iw}_{ib}', dict(RAW), dict(row=row, outcomes=outcomes[-2:], controls=controls), manifest, outputs, pairs)
        assert len(controls) == 130 and len(outcomes) == 81 and len(pairs) == 36
        status = 'SOURCE_OPERATOR_WITNESS_COMPLETE' if all(r['passed'] for r in controls) else 'ARITHMETIC_CONTROL_FAILED'
        result = dict(status=status, manifest=manifest, arithmetic_controls=controls, operator_outcomes=outcomes,
            source_panels=panel_rows, independent_flux_panels=flux_rows, full_initial_controls=prep_rows,
            checkpoint_pairs=pairs, free_witness_result_copied_exactly=free, pure_kernel_result_copied_exactly=old,
            outcome_pass_count=sum(r['passed'] for r in outcomes), outcome_fail_count=sum(not r['passed'] for r in outcomes),
            elapsed_seconds=time.monotonic()-tick, physical_flags=FLAGS)
        write_json(J/(STEM+'_RESULT.json'), result); outputs[STEM+'_RESULT.json'] = sha(J/(STEM+'_RESULT.json'))
        report = ('# Retarded radiation source operator witness\n\n'+status+'\n\n'
            +f"{sum(r['passed'] for r in controls)}/130 arithmetic controls; {result['outcome_pass_count']}/81 fixed source/flux outcomes.\n\n"
            +'All signed tensors, angular kernels, incoming preparation, independent fluxes and failed outcomes are retained. '
            +'No trajectory, angular reset, original diagnostic repair or physical qualification follows.\n').encode()
        put(J/(STEM+'_REPORT.md'), report); outputs[STEM+'_REPORT.md'] = sha(J/(STEM+'_REPORT.md'))
        final_recheck(inputs, outputs, pairs)
        receipt = dict(status=status, owner='root', pid=os.getpid(), started=started, closed=now(),
            source_sha256=sha(__file__), result_sha256=outputs[STEM+'_RESULT.json'], input_sha256=inputs,
            output_sha256=outputs, checkpoint_pairs=36, arithmetic_count=130, outcome_count=81, physical_flags=FLAGS)
        write_json(J/(STEM+'_RECEIPT.json'), receipt)
        assert json.loads((J/(STEM+'_RECEIPT.json')).read_text()) == receipt
        closed_maps(inputs, FREE, 'ANGULAR_WITNESS_COMPLETE'); closed_maps(inputs, OLD, 'PASS_KERNEL_ARITHMETIC')
        final_recheck(inputs, outputs, pairs)
        return 0 if status == 'SOURCE_OPERATOR_WITNESS_COMPLETE' else 3
    except Exception as exc:
        path = J/(STEM+'_RECEIPT.json'); protected = sha(path) if path.exists() else None
        if protected is not None:
            outputs[path.name] = protected
        if 'np' in globals() and RAW:
            checkpoint('ERROR_RAW', dict(RAW), dict(context=CONTEXT, progressive_metadata=RAW_META,
                controls=controls, outcomes=outcomes), manifest, outputs, pairs, True)
        error = dict(status='ERROR', owner='root', pid=os.getpid(), started=started, closed=now(), context=dict(CONTEXT),
            type=type(exc).__name__, message=str(exc), traceback=traceback.format_exc(), input_sha256=inputs,
            output_sha256=dict(outputs), checkpoint_pairs=pairs, controls=controls, outcomes=outcomes,
            protected_existing_receipt_sha256=protected, physical_flags=FLAGS)
        write_json(J/(STEM+'_ERROR.json'), error); outputs[STEM+'_ERROR.json'] = sha(J/(STEM+'_ERROR.json'))
        final_recheck(inputs, outputs, pairs)
        if protected is None:
            rc = dict(error, output_sha256=dict(outputs))
            write_json(path, rc); assert json.loads(path.read_text()) == rc
        else:
            assert sha(path) == protected
        closed_maps(inputs, FREE, 'ANGULAR_WITNESS_COMPLETE'); closed_maps(inputs, OLD, 'PASS_KERNEL_ARITHMETIC')
        final_recheck(inputs, outputs, pairs)
        return 1


if __name__ == '__main__':
    sys.exit(main())

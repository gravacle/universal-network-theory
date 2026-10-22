import sys; sys.dont_write_bytecode=True; sys.path.append('/Users/bgm/Library/Python/3.9/lib/python/site-packages'); import numpy as np
# fixtures_weak_euler_h2v001.py -- Claude4 review lane (dispatch 0440, amended by 0441), helper H2.
#
# Pluggable manufactured-fixture harness for an implementation of the pinned root contract
#   /Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/ADDITIONAL_CLAUDE_WEAK_EULER_TASKS_V001.json
#   SHA256 5c30449de636b1f3da751d07ad90caafe964ed19444b0648df8fd9726ade9ebe   (author_task.equations)
#
# Scope: small synthetic arrays only (npoints <= 16, nfree <= 5).  No project data, galaxy data,
# calibration/target velocities or validation outcomes; no project module is imported; no physics
# verdict.  A pass is scoped implementation conformance to the contract text, never a physical result.
#
# Entry point:  run_all(target, adapter=None, out_json=None, skip=(), target_info=None)
#   target  : callable accepting the canonical keyword arguments (after the adapter's to_target).
#   adapter : None (identity) | module/object with to_target(kw)->kw and/or from_target(raw)->dict
#             | a (to_target, from_target) tuple.  from_target must return a dict holding the
#             canonical keys A, b (already divided by normalization_scale), E, PM, VR, VP, VZ.
# CLI:
#   /usr/bin/python3 -I -B fixtures_weak_euler_h2v001.py --module PATH --func NAME [--adapter-module PATH] --out JSON [--skip F6]
#   /usr/bin/python3 -I -B fixtures_weak_euler_h2v001.py --reference-run  --out JSON
#   /usr/bin/python3 -I -B fixtures_weak_euler_h2v001.py --mutation-study --out JSON
# Targets and adapters are loaded by FILE PATH (importlib.util.spec_from_file_location), never by
# package import; sys.dont_write_bytecode is set so no bytecode is written.
#
# Fixtures: F0 hand case; F1 loop-reference comparison; F2 term isolation; F3 reference-free
# properties; F4 G verbatim, no input mutation, output shapes/dtypes; F5 no hidden forcing;
# F6 malformed-input probes (exception type and message recorded, never crashing the harness);
# F7 = run_mutation_study (sensitivity of this harness to mutated transcriptions).
import argparse
import copy
import hashlib
import importlib.util
import json
import math
import numbers
import os
import re
import struct
import warnings
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
HARNESS_PATH = os.path.abspath(__file__)
REFERENCE_PATH = os.path.join(HERE, 'reference_weak_euler_h2v001.py')
CONTRACT_PATH = ('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/'
                 'FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/ADDITIONAL_CLAUDE_WEAK_EULER_TASKS_V001.json')
CONTRACT_SHA256 = '5c30449de636b1f3da751d07ad90caafe964ed19444b0648df8fd9726ade9ebe'

CANONICAL_INPUTS = ('R', 'rho', 'P', 'K_R', 'K_z', 'P_R', 'P_z', 'Omega', 'Omega_R', 'Omega_z',
                    'volume_weights', 'U_R', 'U_phi', 'U_z', 'divU', 'G', 'f_R', 'f_phi', 'f_z',
                    'm', 'gamma', 'normalization_scale', 'provenance')
REAL_VECTORS = CANONICAL_INPUTS[:11]
POSITIVE_VECTORS = ('R', 'rho', 'P', 'volume_weights')
MAPS = ('U_R', 'U_phi', 'U_z', 'divU', 'G')
FORCING = ('f_R', 'f_phi', 'f_z')
OUTPUT_KEYS = ('A', 'b', 'E', 'PM', 'VR', 'VP', 'VZ')
MAP_KEYS = ('E', 'PM', 'VR', 'VP', 'VZ')
GAMMA = 5.0 / 3.0

RTOL = 1e-12       # target vs loop reference / hand values / separately written expectations
PROP_RTOL = 1e-12  # reference-free identities (errors scaled by the operands' magnitude)
FLOOR = 1.0        # scale floor: err = max|got-exp| / max(max|exp|, FLOOR); fixture data are O(1)
TOLERANCE_NOTE = ('scale-aware error max|got-exp|/max(max|exp|,1); all fixture inputs are O(1) so the '
                  'floor only turns comparisons of structurally zero arrays into absolute 1e-12 tests; '
                  'F5 requires b == 0 exactly; F4 requires inputs bitwise unchanged.')

_INCIDENTAL_RE = re.compile(
    r'could not be broadcast|matmul|core dimension|out of bounds|index out of range|'
    r'unsupported operand|has no len|not subscriptable|can\'t multiply sequence|could not convert|'
    r'only length-1 arrays|must be real number, not|is not iterable|too many indices|invalid index|'
    r'not supported between', re.I)


# ----------------------------------------------------------------------------- utilities
def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        while True:
            chunk = fh.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def load_module_from_path(path, name):
    """Load a Python source file by FILE PATH (never a package import); writes no bytecode."""
    sys.dont_write_bytecode = True
    path = os.path.abspath(path)
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError('cannot create an import spec for %r' % path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(name, None)
        raise
    return module


_LOADED = {}


def _reference():
    if 'reference' not in _LOADED:
        mod = load_module_from_path(REFERENCE_PATH, 'h2_reference_weak_euler_h2v001')
        _LOADED['reference'] = mod.reference_assemble
    return _LOADED['reference']


_REF_CACHE = {}


def _ref_outputs(kw, key=None):
    if key is not None and key in _REF_CACHE:
        return _REF_CACHE[key]
    out = _reference()(**copy.deepcopy(kw))
    if key is not None:
        _REF_CACHE[key] = out
    return out


def _msg(exc):
    return ('%s' % (exc,))[:400]


def _jsonable(x):
    if x is None or isinstance(x, (bool, str)):
        return x
    if isinstance(x, np.bool_):
        return bool(x)
    if isinstance(x, (int, np.integer)):
        return int(x)
    if isinstance(x, (float, np.floating)):
        v = float(x)
        return v if math.isfinite(v) else repr(v)
    if isinstance(x, (complex, np.complexfloating)):
        return [_jsonable(float(x.real)), _jsonable(float(x.imag))]
    if isinstance(x, np.ndarray):
        return _jsonable(x.tolist())
    if isinstance(x, dict):
        return dict((str(k), _jsonable(v)) for k, v in x.items())
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    return repr(x)


def _write_json(path, obj):
    with open(path, 'w') as fh:
        json.dump(_jsonable(obj), fh, indent=1, allow_nan=False)
        fh.write('\n')


def _same(a, b):
    """Bitwise equality of an input value and its pre-call deep copy."""
    if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
        return (isinstance(a, np.ndarray) and isinstance(b, np.ndarray) and a.dtype == b.dtype
                and a.shape == b.shape and a.tobytes() == b.tobytes())
    if type(a) is not type(b):
        return False
    if isinstance(a, float):
        return struct.pack('<d', a) == struct.pack('<d', b)
    if isinstance(a, complex):
        return struct.pack('<dd', a.real, a.imag) == struct.pack('<dd', b.real, b.imag)
    if isinstance(a, (list, tuple)):
        return len(a) == len(b) and all(_same(x, y) for x, y in zip(a, b))
    try:
        return bool(a == b)
    except Exception:
        return False


def _bitwise(a, b):
    a = np.asarray(a)
    b = np.asarray(b)
    return a.shape == b.shape and a.dtype == b.dtype and a.tobytes() == b.tobytes()


def _err(got, exp, floor=FLOOR):
    """Scale-aware error max|got-exp| / max(max|exp|, floor); shape or finiteness mismatch -> inf."""
    g = np.asarray(got)
    e = np.asarray(exp)
    if g.shape != e.shape:
        return float('inf'), 'shape %s != expected %s' % (g.shape, e.shape)
    if g.size == 0:
        return 0.0, None
    if not np.all(np.isfinite(g)):
        return float('inf'), 'nonfinite entries in output'
    scale = max(float(np.max(np.abs(e))), floor)
    return float(np.max(np.abs(g - e))) / scale, None


def _cmp(got, exp, keys=OUTPUT_KEYS, floor=FLOOR):
    errs = {}
    notes = {}
    for k in keys:
        errs[k], note = _err(got[k], exp[k], floor)
        if note:
            notes[k] = note
    worst = max(errs.values()) if errs else 0.0
    return worst, errs, notes


def _abs_scale(*arrays):
    vals = [float(np.max(np.abs(np.asarray(a)))) for a in arrays if np.asarray(a).size]
    return max(vals + [FLOOR])


def _gram(X, w, Y):
    """X^H diag(w) Y by einsum (expectation helper; an evaluation style distinct from loops/matmul)."""
    return np.einsum('pk,p,pj->kj', np.conj(np.asarray(X)), np.asarray(w), np.asarray(Y))


def _gvec(X, w, y):
    """X^H (w*y) by einsum."""
    return np.einsum('pk,p,p->k', np.conj(np.asarray(X)), np.asarray(w), np.asarray(y))


# ----------------------------------------------------------------------------- adapter
class Adapter(object):
    """Maps canonical kwargs -> target kwargs, and the target's return value -> canonical dict."""

    def __init__(self, to_target=None, from_target=None, label='identity'):
        self._to = to_target
        self._from = from_target
        self.label = label

    def to_target(self, kw):
        return dict(kw) if self._to is None else self._to(dict(kw))

    def from_target(self, raw):
        return raw if self._from is None else self._from(raw)


def make_adapter(adapter):
    if adapter is None:
        return Adapter()
    if isinstance(adapter, Adapter):
        return adapter
    if isinstance(adapter, (tuple, list)) and len(adapter) == 2:
        return Adapter(adapter[0], adapter[1], label='tuple')
    to_t = getattr(adapter, 'to_target', None)
    from_t = getattr(adapter, 'from_target', None)
    if to_t is None and from_t is None:
        raise TypeError('adapter must define to_target and/or from_target')
    return Adapter(to_t, from_t, label=getattr(adapter, '__name__', type(adapter).__name__))


# ----------------------------------------------------------------------------- manufactured inputs
def _rng_case(seed, npoints, nfree, m=1, ns=None):
    """Random valid canonical inputs: positive R/rho/P/vw, non-constant vectors, nonzero radial and
    vertical shear, complex maps/forcing with imaginary parts comparable to real parts."""
    rng = np.random.default_rng(seed)

    def cplx(shape):
        return rng.normal(size=shape) + 1j * rng.normal(size=shape)

    kw = {}
    kw['R'] = rng.uniform(0.5, 3.0, npoints)
    kw['rho'] = rng.uniform(0.5, 2.5, npoints)
    kw['P'] = rng.uniform(0.5, 2.0, npoints)
    kw['K_R'] = rng.normal(size=npoints)
    kw['K_z'] = rng.normal(size=npoints)
    kw['P_R'] = rng.normal(size=npoints)
    kw['P_z'] = rng.normal(size=npoints)
    kw['Omega'] = rng.uniform(0.5, 1.5, npoints)
    kw['Omega_R'] = rng.normal(scale=0.5, size=npoints)
    kw['Omega_z'] = rng.normal(scale=0.5, size=npoints)
    kw['volume_weights'] = rng.uniform(0.1, 1.0, npoints)
    for name in MAPS:
        kw[name] = cplx((npoints, nfree))
    for name in FORCING:
        kw[name] = cplx(npoints)
    scale = float(rng.uniform(0.5, 4.0)) if ns is None else float(ns)
    kw['m'] = int(m)
    kw['gamma'] = GAMMA
    kw['normalization_scale'] = scale
    kw['provenance'] = 'H2 manufactured fixture seed=%d npoints=%d nfree=%d' % (seed, npoints, nfree)
    return kw


def _all_terms_off(base):
    """Copy of base with every term switch zeroed: Omega, shears, K, P gradients, G and forcing."""
    kw = dict(base)
    n, k = np.shape(base['U_R'])
    for name in ('Omega', 'Omega_R', 'Omega_z', 'K_R', 'K_z', 'P_R', 'P_z'):
        kw[name] = np.zeros(n)
    kw['G'] = np.zeros((n, k), dtype=np.complex128)
    for name in FORCING:
        kw[name] = np.zeros(n, dtype=np.complex128)
    return kw


HAND_CASE_TEXT = ('npoints=1, nfree=1: R=2, rho=8, P=12, K_R=1, K_z=3, P_R=16, P_z=-24, Omega=2, '
                  'Omega_R=1.5, Omega_z=-1, volume_weights=0.5, U_R=1+2i, U_phi=2-i, U_z=-1+i, '
                  'divU=3-2i, G=2+i, f_R=1-i, f_phi=2i, f_z=-3+i, m=2, gamma=5/3, normalization_scale=4')
HAND_EXPECTED = {'E': 2 - 5j, 'PM': 69 - 157.5j, 'VR': -8 + 4j, 'VP': -1 + 4j, 'VZ': -4 - 4j,
                 'A': -366.625 + 17.4375j, 'b': -1 - 3j}
HAND_INTERMEDIATE = {'AR': -12 - 48j, 'AP': -64 + 32j, 'AZ': 16 - 16j,
                     'A_unscaled': -1466.5 + 69.75j, 'b_unscaled': -4 - 12j}


def _hand_case():
    def rv(v):
        return np.array([v], dtype=np.float64)

    def cm(v):
        return np.array([[v]], dtype=np.complex128)

    def cv(v):
        return np.array([v], dtype=np.complex128)

    return dict(R=rv(2.0), rho=rv(8.0), P=rv(12.0), K_R=rv(1.0), K_z=rv(3.0), P_R=rv(16.0),
                P_z=rv(-24.0), Omega=rv(2.0), Omega_R=rv(1.5), Omega_z=rv(-1.0),
                volume_weights=rv(0.5), U_R=cm(1 + 2j), U_phi=cm(2 - 1j), U_z=cm(-1 + 1j),
                divU=cm(3 - 2j), G=cm(2 + 1j), f_R=cv(1 - 1j), f_phi=cv(2j), f_z=cv(-3 + 1j),
                m=2, gamma=GAMMA, normalization_scale=4.0, provenance='H2 F0 hand case')


def _hand_exact_rational():
    """Recompute the hand case in exact rational complex arithmetic (pairs of Fractions)."""
    F = Fraction

    def c(re, im=0):
        return (F(re), F(im))

    def add(*zs):
        return (sum((z[0] for z in zs), F(0)), sum((z[1] for z in zs), F(0)))

    def mul(a, b):
        return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])

    def sc(s, z):
        s = F(s)
        return (s * z[0], s * z[1])

    def conj(z):
        return (z[0], -z[1])

    I = c(0, 1)
    R, rho, P = F(2), F(8), F(12)
    KR, Kz, PR, Pz = F(1), F(3), F(16), F(-24)
    Om, OR, OZ, vw = F(2), F(3, 2), F(-1), F(1, 2)
    m, ns = 2, F(4)
    gPr = F(5, 3) * P / rho          # gamma*P/rho = 5/2
    rho_gamma = F(32)                # 8**(5/3) = (2**3)**(5/3) = 2**5, exact
    UR, UP, UZ, DU, G = c(1, 2), c(2, -1), c(-1, 1), c(3, -2), c(2, 1)
    fR, fP, fZ = c(1, -1), c(0, 2), c(-3, 1)
    imO = sc(m * Om, I)
    E = add(sc(-KR, UR), sc(-Kz, UZ))
    PM = add(sc(gPr, G), sc(rho_gamma, E))
    VR = mul(imO, UR)
    VP = add(sc(-(R * OR), UR), mul(imO, UP), sc(-(R * OZ), UZ))
    VZ = mul(imO, UZ)
    AR = add(mul(imO, VR), sc(-2 * Om, VP))
    AP = add(mul(imO, VP), sc(2 * Om + R * OR, VR), sc(R * OZ, VZ))
    AZ = mul(imO, VZ)
    wr = vw * rho
    A_u = add(sc(wr, mul(conj(UR), AR)), sc(wr, mul(conj(UP), AP)), sc(wr, mul(conj(UZ), AZ)),
              sc(-vw, mul(conj(DU), PM)),
              sc(-1, mul(add(sc(vw * PR / rho, conj(UR)), sc(vw * Pz / rho, conj(UZ))), G)))
    b_u = add(sc(-wr, mul(conj(UR), fR)), sc(-wr, mul(conj(UP), fP)), sc(-wr, mul(conj(UZ), fZ)))
    return dict(E=E, PM=PM, VR=VR, VP=VP, VZ=VZ, AR=AR, AP=AP, AZ=AZ, A_unscaled=A_u,
                b_unscaled=b_u, A=sc(1 / ns, A_u), b=sc(1 / ns, b_u))


# ----------------------------------------------------------------------------- runner
class _Runner(object):
    def __init__(self, target, adapter):
        self.target = target
        self.adapter = make_adapter(adapter)
        self.checks = []
        self.ncalls = 0
        self.input_mutations = []
        self.canonical_key_sets = []
        self.raw_key_sets = []
        self.call_warnings = []
        self.last_call = None

    def call(self, kw, label):
        """Call the target on a private deep copy; record any in-place change of an input."""
        call_kw = copy.deepcopy(kw)
        snapshot = copy.deepcopy(kw)
        tkw = self.adapter.to_target(call_kw)
        self.ncalls += 1
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            raw = self.target(**tkw)
        if caught:
            self.call_warnings.append({'call': label,
                                       'warnings': sorted(set(str(w.message) for w in caught))[:5]})
        changed = [k for k in kw if not _same(call_kw[k], snapshot[k])]
        if changed:
            self.input_mutations.append({'call': label, 'inputs_modified': changed})
        if isinstance(raw, dict):
            rk = sorted(str(k) for k in raw.keys())
            if rk not in self.raw_key_sets:
                self.raw_key_sets.append(rk)
        out = self.adapter.from_target(raw)
        if not isinstance(out, dict):
            raise TypeError('canonical output is %s, not a dict' % type(out).__name__)
        ck = sorted(str(k) for k in out.keys())
        if ck not in self.canonical_key_sets:
            self.canonical_key_sets.append(ck)
        missing = [k for k in OUTPUT_KEYS if k not in out]
        if missing:
            raise KeyError('canonical output keys missing: %s' % ', '.join(missing))
        self.last_call = (call_kw, out)
        return out

    def check(self, fixture, name, fn):
        try:
            status, max_error, tol, detail = fn()
        except Exception as exc:
            self.checks.append({'fixture': fixture, 'name': name, 'status': 'error', 'max_error': None,
                                'tol': None, 'detail': {'exception_type': type(exc).__name__,
                                                        'message': _msg(exc)}})
            return
        if isinstance(status, (bool, np.bool_)):
            status = 'pass' if bool(status) else 'fail'
        self.checks.append({'fixture': fixture, 'name': name, 'status': status,
                            'max_error': max_error, 'tol': tol, 'detail': detail})


# ----------------------------------------------------------------------------- F0 hand case
def _fixture_F0(rn):
    kw = _hand_case()

    def hand():
        out = rn.call(kw, 'F0_hand')
        exp = {}
        for k in OUTPUT_KEYS:
            if k == 'b':
                exp[k] = np.array([HAND_EXPECTED[k]], dtype=np.complex128)
            else:
                exp[k] = np.array([[HAND_EXPECTED[k]]], dtype=np.complex128)
        worst, errs, notes = _cmp(out, exp)
        got = dict((k, np.asarray(out[k]).ravel().tolist()) for k in OUTPUT_KEYS)
        return worst <= RTOL, worst, RTOL, {'inputs': HAND_CASE_TEXT, 'per_key_error': errs,
                                            'notes': notes, 'got': got, 'expected': HAND_EXPECTED}

    rn.check('F0', 'F0_hand_case_npoints1_nfree1', hand)

    def selfcheck():
        exact = _hand_exact_rational()
        table = dict(HAND_EXPECTED)
        table.update(HAND_INTERMEDIATE)
        bad = [k for k, h in table.items() if exact[k] != (Fraction(h.real), Fraction(h.imag))]
        return (not bad), (0.0 if not bad else float('inf')), 0.0, {
            'mismatched_hand_values': bad,
            'note': 'hard-coded hand values re-derived in exact Fraction arithmetic; target not called'}

    rn.check('F0', 'F0_hand_values_exact_rational_selfcheck', selfcheck)


# ----------------------------------------------------------------------------- F1 reference comparison
F1_CASES = ((7, 3, (11, 12, 13)), (4, 4, (21, 22, 23)), (16, 5, (31, 32, 33)))


def _fixture_F1(rn):
    for npts, nf, seeds in F1_CASES:
        for seed in seeds:
            name = 'F1_reference_np%d_nf%d_seed%d_m1to6' % (npts, nf, seed)

            def fn(npts=npts, nf=nf, seed=seed, name=name):
                base = _rng_case(seed, npts, nf)
                worst = 0.0
                per_m = {}
                failing_m = []
                errors = {}
                key_worst = dict((k, 0.0) for k in OUTPUT_KEYS)
                notes_all = {}
                for mm in range(1, 7):
                    kw = dict(base, m=mm)
                    ref = _ref_outputs(kw, ('F1', npts, nf, seed, mm))
                    try:
                        out = rn.call(kw, '%s_m%d' % (name, mm))
                    except Exception as exc:
                        errors['m=%d' % mm] = '%s: %s' % (type(exc).__name__, _msg(exc))
                        continue
                    w, errs, notes = _cmp(out, ref)
                    per_m['m=%d' % mm] = w
                    for k in OUTPUT_KEYS:
                        key_worst[k] = max(key_worst[k], errs[k])
                    if notes:
                        notes_all['m=%d' % mm] = notes
                    if w > RTOL:
                        failing_m.append(mm)
                    worst = max(worst, w)
                detail = {'shape': [npts, nf], 'seed': seed,
                          'normalization_scale': base['normalization_scale'], 'per_m_error': per_m,
                          'per_key_max_error': key_worst, 'failing_m': failing_m, 'notes': notes_all}
                if errors:
                    first = list(errors.values())[0]
                    detail['errors'] = errors
                    detail['exception_type'] = first.split(':')[0]
                    return 'error', worst, RTOL, detail
                return (not failing_m), worst, RTOL, detail

            rn.check('F1', name, fn)


# ----------------------------------------------------------------------------- F2 term isolation
def _fixture_F2(rn):
    base = _rng_case(41, 5, 3, m=3, ns=1.6)
    n, k = np.shape(base['U_R'])
    m, ns, g = base['m'], base['normalization_scale'], base['gamma']
    UR, UP, UZ, DU, G = (base[x] for x in MAPS)
    Rr, rho, P, vw = base['R'], base['rho'], base['P'], base['volume_weights']
    O, OR, OZ = base['Omega'], base['Omega_R'], base['Omega_z']
    KR, KZ, PR, PZ = base['K_R'], base['K_z'], base['P_R'], base['P_z']
    fR, fP, fZ = base['f_R'], base['f_phi'], base['f_z']
    Zm = np.zeros((n, k), dtype=np.complex128)
    ZA = np.zeros((k, k), dtype=np.complex128)
    Zb = np.zeros(k, dtype=np.complex128)
    wr = vw * rho
    outs = {}

    def run_case(name, kw, exp, hermitian=False, what=''):
        def fn():
            out = rn.call(kw, name)
            outs[name] = out
            worst, errs, notes = _cmp(out, exp)
            detail = {'isolates': what, 'per_key_error': errs, 'notes': notes}
            ok = worst <= RTOL
            if hermitian:
                A = np.asarray(out['A'])
                h = float(np.max(np.abs(A - A.conj().T))) / _abs_scale(A)
                detail['hermitian_error'] = h
                ok = ok and h <= RTOL
                worst = max(worst, h)
            return ok, worst, RTOL, detail
        rn.check('F2', name, fn)

    # F2a Omega only:  AR=-m^2 O^2 U_R - 2im O^2 U_phi,  AP=2im O^2 U_R - m^2 O^2 U_phi,  AZ=-m^2 O^2 U_z
    kw = _all_terms_off(base)
    kw['Omega'] = O
    D = wr * O ** 2
    A_u = (-(m ** 2) * (_gram(UR, D, UR) + _gram(UP, D, UP) + _gram(UZ, D, UZ))
           + 2j * m * (_gram(UP, D, UR) - _gram(UR, D, UP)))
    run_case('F2a_Omega_only', kw,
             dict(A=A_u / ns, b=Zb, E=Zm, PM=Zm, VR=1j * m * O[:, None] * UR,
                  VP=1j * m * O[:, None] * UP, VZ=1j * m * O[:, None] * UZ),
             hermitian=True, what='inertial terms with uniform-in-z rotation only; A must be Hermitian')

    # F2b Omega with Omega_R: the R*Omega_R terms cancel in AP; AR gains +2*Omega*R*Omega_R*U_R
    kw = _all_terms_off(base)
    kw['Omega'] = O
    kw['Omega_R'] = OR
    A_u = (-(m ** 2) * (_gram(UR, D, UR) + _gram(UP, D, UP) + _gram(UZ, D, UZ))
           + 2j * m * (_gram(UP, D, UR) - _gram(UR, D, UP))
           + _gram(UR, wr * 2 * O * Rr * OR, UR))
    run_case('F2b_Omega_with_Omega_R', kw,
             dict(A=A_u / ns, b=Zb, E=Zm, PM=Zm, VR=1j * m * O[:, None] * UR,
                  VP=-(Rr * OR)[:, None] * UR + 1j * m * O[:, None] * UP,
                  VZ=1j * m * O[:, None] * UZ),
             hermitian=True, what='radial shear; A must stay Hermitian')

    # F2c Omega with Omega_z (vertical shear alone): R*Omega_z terms cancel in AP; AR gains
    # +2*Omega*R*Omega_z*U_z, so A gains U_R^H diag(2 vw rho Omega R Omega_z) U_z (not Hermitian)
    kw = _all_terms_off(base)
    kw['Omega'] = O
    kw['Omega_z'] = OZ
    A_u = (-(m ** 2) * (_gram(UR, D, UR) + _gram(UP, D, UP) + _gram(UZ, D, UZ))
           + 2j * m * (_gram(UP, D, UR) - _gram(UR, D, UP))
           + _gram(UR, wr * 2 * O * Rr * OZ, UZ))
    run_case('F2c_Omega_with_Omega_z_vertical_shear_alone', kw,
             dict(A=A_u / ns, b=Zb, E=Zm, PM=Zm, VR=1j * m * O[:, None] * UR,
                  VP=1j * m * O[:, None] * UP - (Rr * OZ)[:, None] * UZ,
                  VZ=1j * m * O[:, None] * UZ),
             what='vertical shear; contract gives U_R^H diag(2 vw rho Omega R Omega_z) U_z only')

    # F2d P_R only (divU = 0 so the PM term vanishes although PM itself is nonzero)
    kw = _all_terms_off(base)
    kw['P_R'] = PR
    kw['G'] = G
    kw['divU'] = Zm.copy()
    run_case('F2d_P_R_only', kw,
             dict(A=-_gram(UR, vw * PR / rho, G) / ns, b=Zb, E=Zm,
                  PM=(g * P / rho)[:, None] * G, VR=Zm, VP=Zm, VZ=Zm),
             what='-U_R^H diag(vw P_R/rho) G')

    # F2e P_z only
    kw = _all_terms_off(base)
    kw['P_z'] = PZ
    kw['G'] = G
    kw['divU'] = Zm.copy()
    run_case('F2e_P_z_only', kw,
             dict(A=-_gram(UZ, vw * PZ / rho, G) / ns, b=Zb, E=Zm,
                  PM=(g * P / rho)[:, None] * G, VR=Zm, VP=Zm, VZ=Zm),
             what='-U_z^H diag(vw P_z/rho) G')

    # F2f K_R only: E=-K_R U_R, PM=rho^gamma E, A=-divU^H diag(vw) PM = divU^H diag(vw rho^g K_R) U_R
    kw = _all_terms_off(base)
    kw['K_R'] = KR
    E = -KR[:, None] * UR
    run_case('F2f_K_R_only', kw,
             dict(A=_gram(DU, vw * rho ** g * KR, UR) / ns, b=Zb, E=E,
                  PM=(rho ** g)[:, None] * E, VR=Zm, VP=Zm, VZ=Zm),
             what='+divU^H diag(vw rho^gamma K_R) U_R')

    # F2g K_z only
    kw = _all_terms_off(base)
    kw['K_z'] = KZ
    E = -KZ[:, None] * UZ
    run_case('F2g_K_z_only', kw,
             dict(A=_gram(DU, vw * rho ** g * KZ, UZ) / ns, b=Zb, E=E,
                  PM=(rho ** g)[:, None] * E, VR=Zm, VP=Zm, VZ=Zm),
             what='+divU^H diag(vw rho^gamma K_z) U_z')

    # F2h K_R and K_z together
    kw = _all_terms_off(base)
    kw['K_R'] = KR
    kw['K_z'] = KZ
    E = -KR[:, None] * UR - KZ[:, None] * UZ
    run_case('F2h_K_R_and_K_z', kw,
             dict(A=(_gram(DU, vw * rho ** g * KR, UR) + _gram(DU, vw * rho ** g * KZ, UZ)) / ns,
                  b=Zb, E=E, PM=(rho ** g)[:, None] * E, VR=Zm, VP=Zm, VZ=Zm),
             what='both enthalpy-gradient terms')

    # F2i G with P only: PM=(gamma P/rho) G ; A=-divU^H diag(vw gamma P/rho) G
    kw = _all_terms_off(base)
    kw['G'] = G
    run_case('F2i_G_with_P_only', kw,
             dict(A=-_gram(DU, vw * g * P / rho, G) / ns, b=Zb, E=Zm,
                  PM=(g * P / rho)[:, None] * G, VR=Zm, VP=Zm, VZ=Zm),
             what='-divU^H diag(vw gamma P/rho) G')

    # F2j forcing only, then each forcing component alone
    def forcing_case(name, fr, fp, fz, what):
        kw = _all_terms_off(base)
        kw['f_R'], kw['f_phi'], kw['f_z'] = fr, fp, fz
        bexp = -(_gvec(UR, wr, fr) + _gvec(UP, wr, fp) + _gvec(UZ, wr, fz)) / ns
        run_case(name, kw, dict(A=ZA, b=bexp, E=Zm, PM=Zm, VR=Zm, VP=Zm, VZ=Zm), what=what)

    z = np.zeros(n, dtype=np.complex128)
    forcing_case('F2j_forcing_only', fR, fP, fZ, 'b=-U^H(vw rho f), A=0')
    forcing_case('F2k_f_R_only', fR, z, z, 'b=-U_R^H(vw rho f_R)')
    forcing_case('F2l_f_phi_only', z, fP, z, 'b=-U_phi^H(vw rho f_phi); no extra i*m/R')
    forcing_case('F2m_f_z_only', z, z, fZ, 'b=-U_z^H(vw rho f_z)')

    # Shear contributions isolated by difference against F2a (same maps, same Omega).  Errors are
    # scaled by the operands' magnitude (the rounding scale of a difference), not by the difference.
    def diff_check(name, case, expA, expVP, what):
        def fn():
            if case not in outs or 'F2a_Omega_only' not in outs:
                raise RuntimeError('prerequisite F2 output unavailable (earlier case errored)')
            oa, ob = outs[case], outs['F2a_Omega_only']
            exp = dict(A=expA, b=Zb, E=Zm, PM=Zm, VR=Zm, VP=expVP, VZ=Zm)
            errs = {}
            for x in OUTPUT_KEYS:
                a1, b1 = np.asarray(oa[x]), np.asarray(ob[x])
                if a1.shape != exp[x].shape or b1.shape != exp[x].shape:
                    errs[x] = float('inf')
                else:
                    errs[x] = float(np.max(np.abs((a1 - b1) - exp[x]))) / _abs_scale(a1, b1)
            worst = max(errs.values())
            return worst <= RTOL, worst, RTOL, {'isolates': what, 'per_key_error': errs,
                                                'scale': 'max(|operand1|,|operand2|,1) per key'}
        rn.check('F2', name, fn)

    diff_check('F2n_radial_shear_difference', 'F2b_Omega_with_Omega_R',
               _gram(UR, wr * 2 * O * Rr * OR, UR) / ns, -(Rr * OR)[:, None] * UR,
               'A(Omega,Omega_R)-A(Omega)=U_R^H diag(2 vw rho Omega R Omega_R) U_R / ns')
    diff_check('F2o_vertical_shear_difference', 'F2c_Omega_with_Omega_z_vertical_shear_alone',
               _gram(UR, wr * 2 * O * Rr * OZ, UZ) / ns, -(Rr * OZ)[:, None] * UZ,
               'A(Omega,Omega_z)-A(Omega)=U_R^H diag(2 vw rho Omega R Omega_z) U_z / ns')


# ----------------------------------------------------------------------------- F3 reference-free
def _fixture_F3(rn):
    base = _rng_case(61, 7, 3, m=3, ns=1.3)
    n, k = np.shape(base['U_R'])
    memo = {}

    def get(key, kw):
        if key not in memo:
            memo[key] = rn.call(kw, 'F3_' + key)
        return memo[key]

    def o1():
        return get('base', base)

    def global_phase():
        t = 0.7
        ph = np.exp(1j * t)
        a = o1()
        kw2 = dict(base)
        for x in MAPS:
            kw2[x] = base[x] * ph
        b2 = rn.call(kw2, 'F3_global_phase')
        exp = {'A': np.asarray(a['A']), 'b': np.conj(ph) * np.asarray(a['b'])}
        for x in MAP_KEYS:
            exp[x] = ph * np.asarray(a[x])
        worst, errs, notes = _cmp(b2, exp)
        return worst <= PROP_RTOL, worst, PROP_RTOL, {'t': t, 'per_key_error': errs, 'notes': notes}

    rn.check('F3', 'F3_global_phase_A_invariant_b_times_exp_minus_it', global_phase)

    def column_phases():
        t = np.array([0.3, -1.1, 2.0])
        ph = np.exp(1j * t)
        a = o1()
        kw2 = dict(base)
        for x in MAPS:
            kw2[x] = base[x] * ph[None, :]
        b2 = rn.call(kw2, 'F3_column_phases')
        exp = {'A': np.asarray(a['A']) * np.conj(ph)[:, None] * ph[None, :],
               'b': np.conj(ph) * np.asarray(a['b'])}
        for x in MAP_KEYS:
            exp[x] = np.asarray(a[x]) * ph[None, :]
        worst, errs, notes = _cmp(b2, exp)
        return worst <= PROP_RTOL, worst, PROP_RTOL, {'t_j': t.tolist(), 'per_key_error': errs,
                                                      'notes': notes}

    rn.check('F3', 'F3_column_phases_A_kj_times_exp_i_tj_minus_tk', column_phases)

    def forcing_linearity():
        rng = np.random.default_rng(62)
        f2 = dict((x, rng.normal(size=n) + 1j * rng.normal(size=n)) for x in FORCING)
        alpha, beta = 0.6 - 1.3j, -0.4 + 0.9j
        a = o1()
        o2 = rn.call(dict(base, **f2), 'F3_forcing_f2')
        oc = rn.call(dict(base, **dict((x, alpha * base[x] + beta * f2[x]) for x in FORCING)),
                     'F3_forcing_combination')
        o0 = rn.call(dict(base, **dict((x, np.zeros(n, dtype=np.complex128)) for x in FORCING)),
                     'F3_forcing_zero')
        errs = {}
        errs['b_linear'] = float(np.max(np.abs(np.asarray(oc['b']) - alpha * np.asarray(a['b'])
                                               - beta * np.asarray(o2['b'])))) / _abs_scale(
            a['b'], o2['b'], oc['b'])
        for label, o in (('f2', o2), ('combination', oc), ('zero', o0)):
            for x in ('A',) + MAP_KEYS:
                errs['%s_%s_unchanged' % (x, label)] = _err(o[x], a[x])[0]
        bit = dict((label, _bitwise(o['A'], a['A'])) for label, o in
                   (('f2', o2), ('combination', oc), ('zero', o0)))
        worst = max(errs.values())
        return worst <= PROP_RTOL, worst, PROP_RTOL, {'alpha': alpha, 'beta': beta, 'errors': errs,
                                                      'A_bitwise_independent_of_forcing': bit}

    rn.check('F3', 'F3_b_linear_in_forcing_A_and_maps_independent', forcing_linearity)

    for c in (2.0, 0.37):
        def vw_scaling(c=c):
            a = o1()
            b2 = rn.call(dict(base, volume_weights=c * base['volume_weights']), 'F3_vw_x%g' % c)
            exp = {'A': c * np.asarray(a['A']), 'b': c * np.asarray(a['b'])}
            for x in MAP_KEYS:
                exp[x] = np.asarray(a[x])
            worst, errs, notes = _cmp(b2, exp)
            bit = dict((x, _bitwise(b2[x], exp[x])) for x in OUTPUT_KEYS)
            return worst <= PROP_RTOL, worst, PROP_RTOL, {'c': c, 'per_key_error': errs,
                                                          'bitwise': bit, 'notes': notes}
        rn.check('F3', 'F3_volume_weights_times_%g_scales_A_b_maps_unchanged' % c, vw_scaling)

    def ns_scaling():
        c = 3.0
        a = o1()
        b2 = rn.call(dict(base, normalization_scale=c * base['normalization_scale']), 'F3_ns_x3')
        exp = {'A': np.asarray(a['A']) / c, 'b': np.asarray(a['b']) / c}
        for x in MAP_KEYS:
            exp[x] = np.asarray(a[x])
        worst, errs, notes = _cmp(b2, exp)
        bit = dict((x, _bitwise(b2[x], a[x])) for x in MAP_KEYS)
        return worst <= PROP_RTOL, worst, PROP_RTOL, {'c': c, 'per_key_error': errs,
                                                      'maps_bitwise_unchanged': bit, 'notes': notes}

    rn.check('F3', 'F3_normalization_scale_times_3_divides_A_b_maps_unchanged', ns_scaling)

    def m_outs():
        return dict((mm, get('m%d' % mm, dict(base, m=mm))) for mm in range(1, 7))

    def m_third():
        outs = m_outs()
        A = dict((mm, np.asarray(outs[mm]['A'])) for mm in outs)
        scale = _abs_scale(*A.values())
        errs = {}
        for m0 in (1, 2, 3):
            d3 = A[m0 + 3] - 3 * A[m0 + 2] + 3 * A[m0 + 1] - A[m0]
            errs['m%d..%d' % (m0, m0 + 3)] = float(np.max(np.abs(d3))) / scale
        worst = max(errs.values())
        return worst <= PROP_RTOL, worst, PROP_RTOL, {'per_window_error': errs,
                                                      'scale_max_abs_A': scale}

    rn.check('F3', 'F3_A_quadratic_in_m_third_difference_vanishes', m_third)

    def m_second():
        outs = m_outs()
        A = dict((mm, np.asarray(outs[mm]['A'])) for mm in outs)
        D = base['volume_weights'] * base['rho'] * base['Omega'] ** 2
        d2exp = -2.0 * (_gram(base['U_R'], D, base['U_R']) + _gram(base['U_phi'], D, base['U_phi'])
                        + _gram(base['U_z'], D, base['U_z'])) / base['normalization_scale']
        scale = _abs_scale(*A.values())
        errs = {}
        for mm in (2, 3, 4, 5):
            d2 = A[mm + 1] - 2 * A[mm] + A[mm - 1]
            if d2.shape != d2exp.shape:
                errs['m=%d' % mm] = float('inf')
            else:
                errs['m=%d' % mm] = float(np.max(np.abs(d2 - d2exp))) / scale
        worst = max(errs.values())
        return worst <= PROP_RTOL, worst, PROP_RTOL, {
            'expected': '-2*[U_R^H diag(vw rho Omega^2) U_R + U_phi^H(..)U_phi + U_z^H(..)U_z]/ns',
            'per_m_error': errs, 'scale_max_abs_A': scale}

    rn.check('F3', 'F3_A_second_difference_in_m_equals_minus2_weighted_Omega2_gram', m_second)

    def b_indep():
        outs = m_outs()
        errs = dict(('m=%d' % mm, _err(outs[mm]['b'], outs[1]['b'])[0]) for mm in range(2, 7))
        bit = all(_bitwise(outs[mm]['b'], outs[1]['b']) for mm in range(2, 7))
        worst = max(errs.values())
        return worst <= PROP_RTOL, worst, PROP_RTOL, {'per_m_error_vs_m1': errs, 'bitwise_all': bit}

    rn.check('F3', 'F3_b_independent_of_m', b_indep)

    def e_pm_indep():
        outs = m_outs()
        errs = {}
        for mm in range(2, 7):
            for x in ('E', 'PM'):
                errs['%s_m=%d' % (x, mm)] = _err(outs[mm][x], outs[1][x])[0]
        worst = max(errs.values())
        return worst <= PROP_RTOL, worst, PROP_RTOL, {'errors': errs}

    rn.check('F3', 'F3_E_and_PM_independent_of_m', e_pm_indep)

    def v_linear():
        outs = m_outs()
        errs = {}
        for mm in range(2, 7):
            for x in ('VR', 'VZ'):
                errs['%s_m=%d' % (x, mm)] = _err(outs[mm][x], mm * np.asarray(outs[1][x]))[0]
            vp_exp = np.asarray(outs[1]['VP']) + (mm - 1) * (np.asarray(outs[2]['VP'])
                                                             - np.asarray(outs[1]['VP']))
            if mm > 2:
                errs['VP_affine_m=%d' % mm] = _err(outs[mm]['VP'], vp_exp)[0]
        worst = max(errs.values())
        return worst <= PROP_RTOL, worst, PROP_RTOL, {'errors': errs}

    rn.check('F3', 'F3_VR_VZ_proportional_to_m_VP_affine_in_m', v_linear)

    for c in (2.0, 3.0):
        def r_rescale(c=c):
            a = o1()
            kw2 = dict(base, R=c * base['R'], Omega_R=base['Omega_R'] / c,
                       Omega_z=base['Omega_z'] / c)
            b2 = rn.call(kw2, 'F3_R_rescale_%g' % c)
            worst, errs, notes = _cmp(b2, a)
            bit = dict((x, _bitwise(b2[x], a[x])) for x in OUTPUT_KEYS)
            return worst <= PROP_RTOL, worst, PROP_RTOL, {'c': c, 'per_key_error': errs,
                                                          'bitwise': bit, 'notes': notes}
        rn.check('F3', 'F3_R_times_%g_with_shears_divided_leaves_all_outputs_unchanged' % c,
                 r_rescale)


# ----------------------------------------------------------------------------- F4 G verbatim etc.
def _fixture_F4(rn):
    base = _rng_case(71, 7, 3, m=2, ns=0.8)
    n, k = np.shape(base['U_R'])
    rng = np.random.default_rng(72)
    G2 = rng.normal(size=(n, k)) + 1j * rng.normal(size=(n, k))
    D2 = rng.normal(size=(n, k)) + 1j * rng.normal(size=(n, k))
    g, P, rho, vw, ns = (base['gamma'], base['P'], base['rho'], base['volume_weights'],
                         base['normalization_scale'])
    E_f = -base['K_R'][:, None] * base['U_R'] - base['K_z'][:, None] * base['U_z']
    PM_f = (g * P / rho)[:, None] * base['G'] + (rho ** g)[:, None] * E_f
    memo = {}

    def o1():
        if 'base' not in memo:
            memo['base'] = rn.call(base, 'F4_base')
            memo['call_kw'] = rn.last_call[0]
        return memo['base']

    def pm_formula():
        o = o1()
        worst, errs, notes = _cmp(o, {'E': E_f, 'PM': PM_f}, keys=('E', 'PM'))
        Gv, Dv = base['G'].ravel(), base['divU'].ravel()
        overlap = abs(np.vdot(Gv, Dv)) / (np.linalg.norm(Gv) * np.linalg.norm(Dv))
        return worst <= RTOL, worst, RTOL, {
            'expected': 'PM == (gamma*P/rho)[:,None]*G + rho[:,None]**gamma*E with the SUPPLIED G',
            'per_key_error': errs, 'notes': notes,
            'normalized_overlap_G_divU': float(overlap)}

    rn.check('F4', 'F4_PM_uses_supplied_G_verbatim', pm_formula)

    def g_linear():
        a = o1()
        b2 = rn.call(dict(base, G=G2), 'F4_G2')
        dG = base['G'] - G2
        dA = -(_gram(base['divU'], vw * g * P / rho, dG) + _gram(base['U_R'], vw * base['P_R'] / rho, dG)
               + _gram(base['U_z'], vw * base['P_z'] / rho, dG)) / ns
        A1, A2 = np.asarray(a['A']), np.asarray(b2['A'])
        errs = {}
        if A1.shape != dA.shape or A2.shape != dA.shape:
            errs['A_difference'] = float('inf')
        else:
            errs['A_difference'] = float(np.max(np.abs((A1 - A2) - dA))) / _abs_scale(A1, A2)
        P1, P2 = np.asarray(a['PM']), np.asarray(b2['PM'])
        dPM = (g * P / rho)[:, None] * dG
        if P1.shape != dPM.shape or P2.shape != dPM.shape:
            errs['PM_difference'] = float('inf')
        else:
            errs['PM_difference'] = float(np.max(np.abs((P1 - P2) - dPM))) / _abs_scale(P1, P2)
        for x in ('b', 'E', 'VR', 'VP', 'VZ'):
            errs[x + '_unchanged'] = _err(b2[x], a[x])[0]
        worst = max(errs.values())
        return worst <= PROP_RTOL, worst, PROP_RTOL, {
            'expected': 'A(G1)-A(G2) = -[divU^H diag(vw gamma P/rho) + U_R^H diag(vw P_R/rho) + '
                        'U_z^H diag(vw P_z/rho)](G1-G2)/ns ; PM(G1)-PM(G2)=(gamma P/rho)(G1-G2)',
            'errors': errs}

    rn.check('F4', 'F4_G_enters_A_and_PM_linearly_as_supplied', g_linear)

    def divu_linear():
        a = o1()
        b2 = rn.call(dict(base, divU=D2), 'F4_divU2')
        dA = -_gram(base['divU'] - D2, vw, PM_f) / ns
        A1, A2 = np.asarray(a['A']), np.asarray(b2['A'])
        errs = {}
        if A1.shape != dA.shape or A2.shape != dA.shape:
            errs['A_difference'] = float('inf')
        else:
            errs['A_difference'] = float(np.max(np.abs((A1 - A2) - dA))) / _abs_scale(A1, A2)
        for x in ('b',) + MAP_KEYS:
            errs[x + '_unchanged'] = _err(b2[x], a[x])[0]
        worst = max(errs.values())
        return worst <= PROP_RTOL, worst, PROP_RTOL, {
            'expected': 'A(divU1)-A(divU2) = -(divU1-divU2)^H diag(vw) PM / ns ; maps and b unchanged',
            'errors': errs}

    rn.check('F4', 'F4_divU_enters_only_the_pressure_term', divu_linear)

    def shapes():
        o = o1()
        want = {'A': (k, k), 'b': (k,)}
        for x in MAP_KEYS:
            want[x] = (n, k)
        problems = []
        info = {}
        for x in OUTPUT_KEYS:
            v = o[x]
            info[x] = {'type': type(v).__name__, 'shape': list(np.shape(v)),
                       'dtype': str(np.asarray(v).dtype)}
            if not isinstance(v, np.ndarray):
                problems.append(x + ' is not a numpy ndarray')
            if tuple(np.shape(v)) != want[x]:
                problems.append('%s shape %s != %s' % (x, tuple(np.shape(v)), want[x]))
            if not np.iscomplexobj(v):
                problems.append(x + ' is not complex dtype')
        return (not problems), (0.0 if not problems else float('inf')), None, {
            'npoints': n, 'nfree': k, 'outputs': info, 'problems': problems}

    rn.check('F4', 'F4_output_shapes_and_complex_dtype', shapes)

    def aliasing():
        o = o1()
        call_kw = memo['call_kw']
        hits = []
        for x in OUTPUT_KEYS:
            ox = o[x]
            if not isinstance(ox, np.ndarray):
                continue
            for name, v in call_kw.items():
                if isinstance(v, np.ndarray) and np.shares_memory(ox, v):
                    hits.append([x, name])
        return 'record', None, None, {'output_input_memory_sharing': hits,
                                      'note': 'record only; the contract is silent on aliasing'}

    rn.check('F4', 'F4_output_input_aliasing_record', aliasing)


# ----------------------------------------------------------------------------- F5 no hidden forcing
def _fixture_F5(rn):
    base = _rng_case(81, 7, 3, m=1, ns=1.1)
    n, k = np.shape(base['U_R'])
    zf = dict((x, np.zeros(n, dtype=np.complex128)) for x in FORCING)

    def zero_forcing_all_m():
        per_m = {}
        failing = []
        for mm in range(1, 7):
            o = rn.call(dict(base, m=mm, **zf), 'F5_zero_forcing_m%d' % mm)
            b = np.asarray(o['b'])
            A = np.asarray(o['A'])
            per_m['m=%d' % mm] = {'max_abs_b': float(np.max(np.abs(b))) if b.size else None,
                                  'b_shape': list(b.shape),
                                  'max_abs_A': float(np.max(np.abs(A))) if A.size else None}
            if b.shape != (k,) or not bool(np.all(b == 0)):
                failing.append(mm)
        worst = max((v['max_abs_b'] or 0.0) for v in per_m.values())
        return (not failing), worst, 0.0, {
            'criterion': 'b == 0 exactly with shape (nfree,), every m in 1..6, with nonzero G, P, K, '
                         'P_R, P_z, Omega, Omega_R, Omega_z', 'per_m': per_m, 'failing_m': failing}

    rn.check('F5', 'F5_zero_forcing_gives_b_exactly_zero_m1to6', zero_forcing_all_m)

    def zero_forcing_static():
        kw = dict(base, **zf)
        kw['Omega'] = np.zeros(n)
        kw['Omega_R'] = np.zeros(n)
        kw['Omega_z'] = np.zeros(n)
        kw['m'] = 2
        o = rn.call(kw, 'F5_zero_forcing_static')
        b = np.asarray(o['b'])
        ok = b.shape == (k,) and bool(np.all(b == 0))
        return ok, (float(np.max(np.abs(b))) if b.size else None), 0.0, {
            'criterion': 'b == 0 exactly; Omega=0 with nonzero P_R, P_z, K, G (no m0 pressure-gradient '
                         'or background residual injection)', 'b_shape': list(b.shape)}

    rn.check('F5', 'F5_zero_forcing_static_background_b_exactly_zero', zero_forcing_static)


# ----------------------------------------------------------------------------- F6 malformed inputs
B_VALID = 'satisfies every stated input requirement of the root JSON author_task.inputs'
B_KWONLY = ('0439: all inputs are REQUIRED KEYWORD-ONLY arguments with no numerical defaults; '
            'root JSON: no hidden callbacks/defaults')
B_M = 'root JSON author_task.inputs: Integer m 1..6'
B_GAMMA = 'root JSON: gamma=5/3 supplied; 0439: validate gamma=5/3'
B_NS = 'root JSON: positive explicit normalization_scale'
B_PROV = 'root JSON: nonempty provenance'
B_VEC = 'root JSON: required real finite vectors, each of shape (npoints,) (0439: validate shapes consistently)'
B_FIN = 'root JSON: required real FINITE vectors'
B_POS = 'root JSON: R/rho/P/volume_weights positive'
B_MAP = ('root JSON: required complex finite npoints x nfree maps; 0439: validate real/complex finite '
         'shapes consistently')
B_FORCE = 'root JSON: required complex finite forcing-gradient vectors of shape (npoints,)'
B_ONLYPOS = ('root JSON requires positivity only of R/rho/P/volume_weights; every other real vector is '
             'any finite real')


def _f6_probes():
    base = _rng_case(91, 6, 3, m=2, ns=1.7)
    n, k = np.shape(base['U_R'])
    probes = []

    def add(name, group, expected, basis, kw, mode='kw', drop=None, coerced='same'):
        if isinstance(coerced, str) and coerced == 'same':
            coerced = kw if expected == 'accept' else None
        probes.append({'name': name, 'group': group, 'expected': expected, 'basis': basis,
                       'kw': kw, 'mode': mode, 'drop': drop, 'coerced': coerced})

    def w(**changes):
        kw = dict(base)
        kw.update(changes)
        return kw

    zc = np.zeros((n, k), dtype=np.complex128)
    zv = np.zeros(n)
    zf = np.zeros(n, dtype=np.complex128)
    # --- inputs the contract admits (must be accepted and must match the reference)
    add('accept_baseline_valid', 'accept', 'accept', B_VALID, w())
    for mm in range(1, 7):
        add('accept_m_%d' % mm, 'accept', 'accept', B_M, w(m=mm))
    add('accept_Omega_all_negative', 'accept', 'accept', B_ONLYPOS, w(Omega=-base['Omega']))
    add('accept_Omega_all_zero', 'accept', 'accept', B_ONLYPOS, w(Omega=zv.copy()))
    add('accept_no_radial_or_vertical_shear', 'accept', 'accept', B_ONLYPOS,
        w(Omega_R=zv.copy(), Omega_z=zv.copy()))
    add('accept_K_and_P_gradients_zero', 'accept', 'accept', B_ONLYPOS,
        w(K_R=zv.copy(), K_z=zv.copy(), P_R=zv.copy(), P_z=zv.copy()))
    add('accept_G_zero_map', 'accept', 'accept', 'a zero map is a finite complex map', w(G=zc.copy()))
    add('accept_divU_zero_map', 'accept', 'accept', 'a zero map is a finite complex map',
        w(divU=zc.copy()))
    add('accept_forcing_all_zero', 'accept', 'accept', 'zero vectors are finite complex vectors',
        w(f_R=zf.copy(), f_phi=zf.copy(), f_z=zf.copy()))
    add('accept_minimal_npoints1_nfree1', 'accept', 'accept', B_VALID, _rng_case(92, 1, 1, m=2, ns=1.7))
    add('accept_wide_maps_nfree_gt_npoints', 'accept', 'accept',
        'contract states (npoints, nfree) maps with no ordering constraint; assembly performs no solve',
        _rng_case(93, 3, 5, m=4, ns=1.7))
    # --- call form
    for name in CANONICAL_INPUTS:
        add('missing_' + name, 'missing_kwarg', 'reject', B_KWONLY, w(), drop=name)
    add('positional_call', 'call_form', 'reject', B_KWONLY, w(), mode='positional')
    add('unknown_extra_kwarg', 'call_form', 'reject',
        B_KWONLY + '; an unknown keyword is not a contract input and must not be silently ignored',
        w(), mode='extra')
    # --- m
    for label, val in (('0', 0), ('7', 7), ('minus1', -1), ('float_1.0', 1.0), ('float_1.5', 1.5),
                       ('str_1', '1'), ('None', None)):
        add('m_' + label, 'm', 'reject', B_M, w(m=val))
    add('m_bool_True', 'm', 'record_only',
        'contract silent on bool (Python bool subclasses int, True == 1); the pinned prior root weak '
        'code L18 uses type(m) is not int, which would reject it', w(m=True), coerced=w(m=1))
    add('m_numpy_int64_2', 'm', 'record_only',
        'contract silent on Python vs numpy integer type; the pinned prior root weak code L18 would '
        'reject numpy integers', w(m=np.int64(2)), coerced=w(m=2))
    # --- gamma
    for label, val, why in (('1.4', 1.4, B_GAMMA),
                            ('5/3_plus_1e-12', 5.0 / 3.0 + 1e-12,
                             B_GAMMA + ' (strict-equality reading: no module-chosen tolerance)'),
                            ('nan', float('nan'), B_GAMMA), ('str_5/3', '5/3', B_GAMMA),
                            ('None', None, B_GAMMA)):
        add('gamma_' + label, 'gamma', 'reject', why, w(gamma=val))
    add('gamma_numpy_float64_5/3', 'gamma', 'record_only',
        'value is exactly 5/3 (np.float64 subclasses float); contract silent on scalar type',
        w(gamma=np.float64(5.0 / 3.0)), coerced=w())
    # --- normalization_scale
    for label, val, why in (('0', 0.0, B_NS), ('minus1', -1.0, B_NS), ('nan', float('nan'), B_NS),
                            ('inf', float('inf'),
                             B_NS + '; inf is not a finite positive real scale and would silently zero '
                                    'A and b; the pinned prior root weak code L60 rejects a nonfinite scale'),
                            ('str_1', '1', B_NS), ('None', None, B_NS)):
        add('normalization_scale_' + label, 'normalization_scale', 'reject', why,
            w(normalization_scale=val))
    add('normalization_scale_bool_True', 'normalization_scale', 'record_only',
        'contract silent on bool (True == 1)', w(normalization_scale=True),
        coerced=w(normalization_scale=1.0))
    add('normalization_scale_int_2', 'normalization_scale', 'record_only',
        'contract silent on scalar type; 2 is positive', w(normalization_scale=2),
        coerced=w(normalization_scale=2.0))
    # --- provenance
    add('provenance_empty', 'provenance', 'reject', B_PROV, w(provenance=''))
    add('provenance_None', 'provenance', 'reject', B_PROV, w(provenance=None))
    add('provenance_whitespace_only', 'provenance', 'record_only',
        'nonempty but blank; contract silent on whitespace', w(provenance='   '), coerced=w())
    add('provenance_int_123', 'provenance', 'record_only',
        'contract states nonempty provenance without a type (the analogous 0438 contract says string)',
        w(provenance=123), coerced=w())
    # --- real vectors
    for name in REAL_VECTORS:
        v = base[name]
        add(name + '_wrong_length', 'real_vector', 'reject', B_VEC, w(**{name: np.append(v, v[:1])}))
        add(name + '_2d_column', 'real_vector', 'reject', B_VEC, w(**{name: v.reshape(-1, 1).copy()}))
        add(name + '_0d_scalar', 'real_vector', 'reject', B_VEC + '; a 0-d scalar would broadcast silently',
            w(**{name: float(v[0])}))
        x = v.copy()
        x[3] = np.nan
        add(name + '_nan', 'real_vector', 'reject', B_FIN, w(**{name: x}))
        x = v.copy()
        x[3] = np.inf
        add(name + '_inf', 'real_vector', 'reject', B_FIN, w(**{name: x}))
        x = v.astype(np.complex128)
        x[3] += 0.25j
        add(name + '_complex_nonzero_imag', 'real_vector', 'reject', 'root JSON: required REAL finite vectors',
            w(**{name: x}))
        add(name + '_complex_dtype_zero_imag', 'real_vector', 'record_only',
            'values are real; contract silent on dtype', w(**{name: v.astype(np.complex128)}), coerced=w())
        if name in POSITIVE_VECTORS:
            x = v.copy()
            x[3] = 0.0
            add(name + '_zero_entry', 'positivity', 'reject', B_POS, w(**{name: x}))
            add(name + '_all_zero', 'positivity', 'reject', B_POS, w(**{name: np.zeros_like(v)}))
            x = v.copy()
            x[3] = -abs(x[3])
            add(name + '_negative_entry', 'positivity', 'reject', B_POS, w(**{name: x}))
    add('R_python_list', 'real_vector', 'record_only', 'contract silent on container type',
        w(R=[float(t) for t in base['R']]), coerced=w())
    rint = np.arange(1, n + 1)
    add('R_int64_dtype', 'real_vector', 'record_only', 'contract silent on dtype (integer values are real)',
        w(R=rint), coerced=w(R=rint.astype(np.float64)))
    r32 = base['R'].astype(np.float32)
    add('R_float32_dtype', 'real_vector', 'record_only', 'contract silent on precision',
        w(R=r32), coerced=w(R=r32.astype(np.float64)))
    # --- maps
    for name in MAPS:
        X = base[name]
        add(name + '_wrong_npoints', 'map', 'reject', B_MAP, w(**{name: np.vstack([X, X[:1]])}))
        add(name + '_mismatched_nfree', 'map', 'reject', B_MAP, w(**{name: np.hstack([X, X[:, :1]])}))
        add(name + '_1d', 'map', 'reject', B_MAP, w(**{name: X[:, 0].copy()}))
        add(name + '_3d', 'map', 'reject', B_MAP, w(**{name: X[:, :, None].copy()}))
        x = X.copy()
        x[2, 1] = complex(np.nan, x[2, 1].imag)
        add(name + '_nan_real_part', 'map', 'reject', B_MAP, w(**{name: x}))
        x = X.copy()
        x[2, 1] = complex(x[2, 1].real, np.nan)
        add(name + '_nan_imag_part', 'map', 'reject', B_MAP, w(**{name: x}))
        x = X.copy()
        x[2, 1] = complex(np.inf, x[2, 1].imag)
        add(name + '_inf', 'map', 'reject', B_MAP, w(**{name: x}))
        add(name + '_real_dtype', 'map', 'record_only',
            'contract silent on dtype; real values are complex numbers with zero imaginary part',
            w(**{name: X.real.copy()}), coerced=w(**{name: X.real.astype(np.complex128)}))
    # --- forcing
    for name in FORCING:
        f = base[name]
        add(name + '_wrong_length', 'forcing', 'reject', B_FORCE, w(**{name: np.append(f, f[:1])}))
        add(name + '_2d_column', 'forcing', 'reject', B_FORCE, w(**{name: f.reshape(-1, 1).copy()}))
        add(name + '_0d_scalar', 'forcing', 'reject', B_FORCE + '; a 0-d scalar would broadcast silently',
            w(**{name: complex(f[0])}))
        x = f.copy()
        x[3] = complex(np.nan, 0.0)
        add(name + '_nan', 'forcing', 'reject', B_FORCE, w(**{name: x}))
        x = f.copy()
        x[3] = complex(np.inf, 0.0)
        add(name + '_inf', 'forcing', 'reject', B_FORCE, w(**{name: x}))
        add(name + '_real_dtype', 'forcing', 'record_only', 'contract silent on dtype',
            w(**{name: f.real.copy()}), coerced=w(**{name: f.real.astype(np.complex128)}))
    return probes


def probe_catalog():
    """List of (probe, expected, basis) for documentation."""
    return [(p['name'], p['expected'], p['basis']) for p in _f6_probes()]


def _run_probe(target, adapter, pr):
    detail = {'expected': pr['expected'], 'basis': pr['basis'], 'group': pr['group'],
              'call_mode': pr['mode']}
    if pr['drop']:
        detail['dropped_kwarg'] = pr['drop']
    rec = {'fixture': 'F6', 'name': 'F6_' + pr['name'], 'status': None, 'max_error': None,
           'tol': None, 'detail': detail}
    kw = dict((kk, v) for kk, v in pr['kw'].items() if kk != pr['drop'])
    try:
        tkw = adapter.to_target(copy.deepcopy(kw))
    except Exception as exc:
        detail['outcome'] = 'adapter_error'
        detail['exception_type'] = type(exc).__name__
        detail['message'] = _msg(exc)
        rec['status'] = 'error'
        return rec
    raw = None
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        try:
            if pr['mode'] == 'positional':
                raw = target(*list(tkw.values()))
            elif pr['mode'] == 'extra':
                tkw2 = dict(tkw)
                tkw2['h2_unexpected_probe_kwarg'] = 1.0
                raw = target(**tkw2)
            else:
                raw = target(**tkw)
            detail['outcome'] = 'accepted'
        except Exception as exc:
            detail['outcome'] = 'rejected'
            detail['exception_type'] = type(exc).__name__
            detail['message'] = _msg(exc)
            detail['incidental_error_heuristic'] = bool(_INCIDENTAL_RE.search(detail['message']))
    if caught:
        detail['warnings'] = sorted(set(str(x.message) for x in caught))[:5]
    if detail['outcome'] == 'accepted':
        try:
            out = adapter.from_target(raw)
            detail['outputs_finite'] = bool(all(np.all(np.isfinite(np.asarray(out[x])))
                                                for x in OUTPUT_KEYS))
            if pr['coerced'] is not None:
                ref = _reference()(**copy.deepcopy(pr['coerced']))
                ref_err, errs, notes = _cmp(out, ref)
                detail['reference_error'] = ref_err
                detail['matches_reference'] = bool(ref_err <= RTOL)
                rec['max_error'] = ref_err
                rec['tol'] = RTOL
        except Exception as exc:
            detail['output_problem'] = '%s: %s' % (type(exc).__name__, _msg(exc))
    if pr['expected'] == 'reject':
        rec['status'] = 'pass' if detail['outcome'] == 'rejected' else 'fail'
    elif pr['expected'] == 'accept':
        good = (detail['outcome'] == 'accepted' and detail.get('outputs_finite')
                and detail.get('matches_reference'))
        rec['status'] = 'pass' if good else 'fail'
    else:
        rec['status'] = 'record'
    return rec


def _fixture_F6(rn):
    for pr in _f6_probes():
        rn.checks.append(_run_probe(rn.target, rn.adapter, pr))


def _f6_summary(checks):
    f6 = [c for c in checks if c['fixture'] == 'F6' and c['status'] != 'skipped']
    s = {'n_probes': len(f6)}
    for exp in ('reject', 'accept', 'record_only'):
        sub = [c for c in f6 if c['detail'].get('expected') == exp]
        d = {'n': len(sub)}
        for st in ('pass', 'fail', 'error', 'record'):
            d[st] = sum(1 for c in sub if c['status'] == st)
        d['accepted'] = sum(1 for c in sub if c['detail'].get('outcome') == 'accepted')
        d['rejected'] = sum(1 for c in sub if c['detail'].get('outcome') == 'rejected')
        d['rejected_incidental_heuristic'] = sum(1 for c in sub
                                                 if c['detail'].get('incidental_error_heuristic'))
        s[exp] = d
    s['failing_probes'] = [c['name'] for c in f6 if c['status'] in ('fail', 'error')]
    s['rejections_flagged_incidental'] = [c['name'] for c in f6
                                          if c['detail'].get('incidental_error_heuristic')]
    s['record_only_outcomes'] = dict(
        (c['name'], {'outcome': c['detail'].get('outcome'),
                     'exception_type': c['detail'].get('exception_type'),
                     'matches_reference': c['detail'].get('matches_reference')})
        for c in f6 if c['status'] == 'record')
    return s


# ----------------------------------------------------------------------------- run_all
FIXTURES = (('F0', _fixture_F0), ('F1', _fixture_F1), ('F2', _fixture_F2), ('F3', _fixture_F3),
            ('F4', _fixture_F4), ('F5', _fixture_F5))


def _summarize(checks):
    counts = {}
    by_fixture = {}
    for c in checks:
        counts[c['status']] = counts.get(c['status'], 0) + 1
        d = by_fixture.setdefault(c['fixture'], {})
        d[c['status']] = d.get(c['status'], 0) + 1
    failures = [c['name'] for c in checks if c['status'] in ('fail', 'error')]
    return {'counts': counts, 'by_fixture': by_fixture, 'failures': failures,
            'all_pass': not failures}


def _meta(target_info, adapter_label, skip):
    observed = sha256_file(CONTRACT_PATH) if os.path.exists(CONTRACT_PATH) else None
    return {
        'harness_path': HARNESS_PATH, 'harness_sha256': sha256_file(HARNESS_PATH),
        'reference_path': REFERENCE_PATH, 'reference_sha256': sha256_file(REFERENCE_PATH),
        'contract_path': CONTRACT_PATH, 'contract_sha256_pinned': CONTRACT_SHA256,
        'contract_sha256_observed': observed, 'contract_hash_verified': observed == CONTRACT_SHA256,
        'python': sys.version.split()[0], 'numpy': np.__version__,
        'tolerances': {'RTOL': RTOL, 'PROP_RTOL': PROP_RTOL, 'FLOOR': FLOOR, 'note': TOLERANCE_NOTE},
        'target': target_info, 'adapter': adapter_label, 'skipped_fixtures': sorted(skip),
        'scope': ('manufactured synthetic arrays only; no project data or modules; implementation '
                  'conformance to the contract text, not a physical verdict')}


def run_all(target, adapter=None, out_json=None, skip=(), target_info=None):
    """Run fixtures F0-F6 against target; return (and optionally write) the result dict."""
    rn = _Runner(target, adapter)
    skip = set(skip or ())
    for fid, fn in FIXTURES:
        if fid in skip:
            rn.checks.append({'fixture': fid, 'name': fid + '_skipped', 'status': 'skipped',
                              'max_error': None, 'tol': None, 'detail': {}})
            continue
        try:
            fn(rn)
        except Exception as exc:
            rn.checks.append({'fixture': fid, 'name': fid + '_fixture_crashed', 'status': 'error',
                              'max_error': None, 'tol': None,
                              'detail': {'exception_type': type(exc).__name__, 'message': _msg(exc)}})
    if 'F4' not in skip:
        rn.check('F4', 'F4_inputs_unchanged_bitwise_all_calls', lambda: (
            not rn.input_mutations, None, None,
            {'n_target_calls_checked': rn.ncalls, 'mutations': rn.input_mutations}))
        rn.check('F4', 'F4_output_keys_record', lambda: (
            'record', None, None, {'raw_return_key_sets': rn.raw_key_sets,
                                   'canonical_key_sets_after_adapter': rn.canonical_key_sets,
                                   'warnings_during_valid_calls': rn.call_warnings[:20]}))
    if 'F6' in skip:
        rn.checks.append({'fixture': 'F6', 'name': 'F6_skipped', 'status': 'skipped',
                          'max_error': None, 'tol': None, 'detail': {}})
    else:
        try:
            _fixture_F6(rn)
        except Exception as exc:
            rn.checks.append({'fixture': 'F6', 'name': 'F6_fixture_crashed', 'status': 'error',
                              'max_error': None, 'tol': None,
                              'detail': {'exception_type': type(exc).__name__, 'message': _msg(exc)}})
    result = {'meta': _meta(target_info, rn.adapter.label, skip), 'summary': _summarize(rn.checks),
              'n_target_calls_F0_F5': rn.ncalls, 'checks': rn.checks}
    if 'F6' not in skip:
        result['f6_summary'] = _f6_summary(rn.checks)
    if out_json:
        _write_json(out_json, result)
    return result


# ----------------------------------------------------------------------------- F7 mutation study
MUTATIONS = (
    ('transpose_no_conj_test_Uphi', 'required',
     'U_phi^T instead of U_phi^H on the test side of the AP inertial term'),
    ('conj_trial_side_AR', 'required', 'trial factor conjugated: U_R^H diag(vw*rho) conj(AR)'),
    ('vw_twice_AZ_term', 'required', 'volume_weights applied twice in the AZ term: diag(vw*vw*rho)'),
    ('vw_omitted_pressure_term', 'required', 'volume_weights omitted in -divU^H diag(vw) PM'),
    ('P_R_over_rho_squared', 'required', 'gradient term uses vw*P_R/rho**2'),
    ('pressure_term_sign_flipped', 'required', '+divU^H diag(vw) PM'),
    ('G_term_sign_flipped', 'required', '+[U_R^H diag(vw*P_R/rho) + U_z^H diag(vw*P_z/rho)] G'),
    ('drop_2Omega_in_AR', 'required', 'AR = i*m*Omega*VR (the -2*Omega*VP term dropped)'),
    ('drop_ROmegaR_in_AP', 'required', 'AP uses (2*Omega)*VR instead of (2*Omega+R*Omega_R)*VR'),
    ('drop_ROmegaz_in_VP', 'required', 'VP omits -(R*Omega_z)*U_z'),
    ('swap_OmegaR_Omegaz', 'required', 'Omega_R and Omega_z exchanged everywhere'),
    ('f_phi_extra_im_over_R', 'required', 'f_phi multiplied by an extra i*m/R'),
    ('normalization_on_PM', 'required', 'returned PM divided by normalization_scale'),
    ('E_column_broadcast', 'required',
     'E = -K_R*U_R - K_z*U_z with numpy last-axis broadcasting (missing [:,None])'),
    ('b_sign_flipped', 'required', 'b = +U^H(vw*rho*f)'),
    ('G_times_vw', 'required', 'G replaced by vw[:,None]*G before use (PM and gradient term)'),
    ('A_symmetrized', 'required', 'A replaced by (A + A^H)/2'),
    ('m0_residual_injected', 'extra',
     'b gains -U_R^H(vw*rho*(R*Omega^2 - P_R/rho)) - U_z^H(vw*rho*(-P_z/rho)) (axisymmetric residual)'),
    ('hidden_density_reconstruction', 'extra', 'supplied G ignored; -rho*divU used instead'),
    ('im_sign_flipped', 'extra', 'i*m replaced by -i*m everywhere (opposite modal convention)'),
    ('ROmegaz_sign_flipped_in_VP', 'extra', 'VP uses +(R*Omega_z)*U_z'),
    ('drop_ROmegaz_VZ_in_AP', 'extra', 'AP omits (R*Omega_z)*VZ'),
    ('extra_2pi_quadrature', 'extra', 'A and b multiplied by 2*pi (extra quadrature factor)'),
    ('A_transposed', 'extra', 'A returned transposed without conjugation'),
    ('missing_gamma_in_PM', 'extra', 'PM uses (P/rho)*G'),
    ('b_conjugated', 'extra', 'b returned complex-conjugated'),
    ('transpose_no_conj_test_divU', 'extra', 'divU^T instead of divU^H in the pressure term'),
)


def _transcription(mutation=None, *, R, rho, P, K_R, K_z, P_R, P_z, Omega, Omega_R, Omega_z,
                   volume_weights, U_R, U_phi, U_z, divU, G, f_R, f_phi, f_z, m, gamma,
                   normalization_scale, provenance):
    """Vectorized transcription used ONLY as the F7 control (mutation=None) and mutant engine.
    Independent of the loop reference; no validation."""
    mu = mutation
    R, rho, P = (np.asarray(v, dtype=np.float64) for v in (R, rho, P))
    K_R, K_z, P_R, P_z = (np.asarray(v, dtype=np.float64) for v in (K_R, K_z, P_R, P_z))
    Omega, Omega_R, Omega_z = (np.asarray(v, dtype=np.float64) for v in (Omega, Omega_R, Omega_z))
    vw = np.asarray(volume_weights, dtype=np.float64)
    U_R, U_phi, U_z, divU, G = (np.asarray(v, dtype=np.complex128) for v in (U_R, U_phi, U_z, divU, G))
    f_R, f_phi, f_z = (np.asarray(v, dtype=np.complex128) for v in (f_R, f_phi, f_z))
    ns = float(normalization_scale)
    im = (-1j if mu == 'im_sign_flipped' else 1j) * m
    OR, OZ = (Omega_z, Omega_R) if mu == 'swap_OmegaR_Omegaz' else (Omega_R, Omega_z)
    if mu == 'E_column_broadcast':
        E = -K_R * U_R - K_z * U_z
    else:
        E = -K_R[:, None] * U_R - K_z[:, None] * U_z
    Gx = G
    if mu == 'G_times_vw':
        Gx = vw[:, None] * G
    if mu == 'hidden_density_reconstruction':
        Gx = -(rho[:, None] * divU)
    gfac = (P / rho) if mu == 'missing_gamma_in_PM' else (gamma * P / rho)
    PM = gfac[:, None] * Gx + (rho ** gamma)[:, None] * E
    VR = im * Omega[:, None] * U_R
    VP = -(R * OR)[:, None] * U_R + im * Omega[:, None] * U_phi
    if mu == 'ROmegaz_sign_flipped_in_VP':
        VP = VP + (R * OZ)[:, None] * U_z
    elif mu != 'drop_ROmegaz_in_VP':
        VP = VP - (R * OZ)[:, None] * U_z
    VZ = im * Omega[:, None] * U_z
    AR = im * Omega[:, None] * VR
    if mu != 'drop_2Omega_in_AR':
        AR = AR - 2 * Omega[:, None] * VP
    coef = 2 * Omega if mu == 'drop_ROmegaR_in_AP' else 2 * Omega + R * OR
    AP = im * Omega[:, None] * VP + coef[:, None] * VR
    if mu != 'drop_ROmegaz_VZ_in_AP':
        AP = AP + (R * OZ)[:, None] * VZ
    AZ = im * Omega[:, None] * VZ
    wr = vw * rho
    tR, tP, tZ, tD = U_R.conj().T, U_phi.conj().T, U_z.conj().T, divU.conj().T
    tP_AP = U_phi.T if mu == 'transpose_no_conj_test_Uphi' else tP
    tD_PM = divU.T if mu == 'transpose_no_conj_test_divU' else tD
    AR_trial = AR.conj() if mu == 'conj_trial_side_AR' else AR
    wZ = vw * wr if mu == 'vw_twice_AZ_term' else wr
    wD = np.ones_like(vw) if mu == 'vw_omitted_pressure_term' else vw
    gR = vw * P_R / rho ** 2 if mu == 'P_R_over_rho_squared' else vw * P_R / rho
    gZ = vw * P_z / rho
    inertial = tR @ (wr[:, None] * AR_trial) + tP_AP @ (wr[:, None] * AP) + tZ @ (wZ[:, None] * AZ)
    pressure = tD_PM @ (wD[:, None] * PM)
    gradient = (tR * gR[None, :] + tZ * gZ[None, :]) @ Gx
    psign = 1.0 if mu == 'pressure_term_sign_flipped' else -1.0
    gsign = 1.0 if mu == 'G_term_sign_flipped' else -1.0
    A = inertial + psign * pressure + gsign * gradient
    fphi = f_phi * (im / R) if mu == 'f_phi_extra_im_over_R' else f_phi
    b = -(tR @ (wr * f_R) + tP @ (wr * fphi) + tZ @ (wr * f_z))
    if mu == 'm0_residual_injected':
        b = b - (tR @ (wr * (R * Omega ** 2 - P_R / rho)) + tZ @ (wr * (-P_z / rho)))
    if mu == 'b_sign_flipped':
        b = -b
    if mu == 'extra_2pi_quadrature':
        A = 2 * np.pi * A
        b = 2 * np.pi * b
    if mu == 'A_symmetrized':
        A = 0.5 * (A + A.conj().T)
    if mu == 'A_transposed':
        A = A.T.copy()
    if mu == 'b_conjugated':
        b = b.conj()
    PM_out = PM / ns if mu == 'normalization_on_PM' else PM
    return {'A': A / ns, 'b': b / ns, 'E': E, 'PM': PM_out, 'VR': VR, 'VP': VP, 'VZ': VZ}


def _make_transcription_target(mutation):
    def target(**kw):
        return _transcription(mutation, **kw)
    return target


def run_mutation_study(out_json=None, verbose=True):
    control = run_all(_make_transcription_target(None), skip=('F6',),
                      target_info={'label': 'control: vectorized transcription (_transcription, '
                                            'mutation=None) in this file'})
    rows = []
    for name, category, desc in MUTATIONS:
        res = run_all(_make_transcription_target(name), skip=('F6',),
                      target_info={'label': 'mutant ' + name})
        failed = [c for c in res['checks'] if c['status'] == 'fail']
        errored = [c for c in res['checks'] if c['status'] == 'error']
        rows.append({
            'mutation': name, 'category': category, 'description': desc,
            'detected': bool(failed or errored),
            'detecting_fixtures': sorted(set(c['fixture'] for c in failed + errored)),
            'detected_by_value_mismatch': dict((c['name'], c['max_error']) for c in failed),
            'detected_by_exception': dict((c['name'], c['detail'].get('exception_type'))
                                          for c in errored),
            'n_checks_run': len(res['checks'])})
    undetected = [r['mutation'] for r in rows if not r['detected']]
    result = {
        'meta': _meta({'label': 'F7 mutation study'}, 'identity', ('F6',)),
        'note': ('F6 is not run on the control or mutants (no validation in either). Every mutant is '
                 'derived from the vectorized control transcription; the control must pass every '
                 'F0-F5 check, which also cross-checks it against the independent loop reference in F1.'),
        'control': {'summary': control['summary'],
                    'max_error_by_check': dict((c['name'], c['max_error']) for c in control['checks'])},
        'mutations': rows,
        'summary': {'control_all_pass': control['summary']['all_pass'], 'n_mutations': len(rows),
                    'n_required': sum(1 for r in rows if r['category'] == 'required'),
                    'n_detected': sum(1 for r in rows if r['detected']), 'undetected': undetected}}
    if out_json:
        _write_json(out_json, result)
    if verbose:
        print('| mutation | category | detected | fixtures | value-mismatch checks | exception checks |')
        print('|---|---|---|---|---|---|')
        for r in rows:
            print('| %s | %s | %s | %s | %d | %d |' % (
                r['mutation'], r['category'], 'yes' if r['detected'] else 'NO',
                ' '.join(r['detecting_fixtures']), len(r['detected_by_value_mismatch']),
                len(r['detected_by_exception'])))
    return result


# ----------------------------------------------------------------------------- F6 harness self-test
def _selftest_validating_reference(*, R, rho, P, K_R, K_z, P_R, P_z, Omega, Omega_R, Omega_z,
                                   volume_weights, U_R, U_phi, U_z, divU, G, f_R, f_phi, f_z,
                                   m, gamma, normalization_scale, provenance):
    """HARNESS SELF-TEST ONLY, not a proposed implementation: one strict reading of the stated input
    requirements wrapped around the loop reference, used to show that every F6 reject probe is really
    malformed and every accept probe is really valid.  Its record-only choices are arbitrary."""
    def bad(msg):
        raise ValueError('h2 selftest validator: ' + msg)

    if isinstance(m, bool) or not isinstance(m, numbers.Integral) or not 1 <= m <= 6:
        bad('m must be an integer in 1..6')
    if isinstance(gamma, bool) or not isinstance(gamma, numbers.Real) or not gamma == 5.0 / 3.0:
        bad('gamma must equal 5/3')
    if (isinstance(normalization_scale, bool) or not isinstance(normalization_scale, numbers.Real)
            or not math.isfinite(normalization_scale) or not normalization_scale > 0):
        bad('normalization_scale must be a positive finite real')
    if not isinstance(provenance, str) or not provenance.strip():
        bad('provenance must be a nonblank string')
    vectors = (('R', R), ('rho', rho), ('P', P), ('K_R', K_R), ('K_z', K_z), ('P_R', P_R),
               ('P_z', P_z), ('Omega', Omega), ('Omega_R', Omega_R), ('Omega_z', Omega_z),
               ('volume_weights', volume_weights))
    npoints = None
    for name, v in vectors:
        a = np.asarray(v)
        if a.ndim != 1:
            bad(name + ' must be 1-D')
        if npoints is None:
            npoints = a.shape[0]
        if a.shape != (npoints,):
            bad(name + ' length mismatch')
        if not (np.issubdtype(a.dtype, np.floating) or np.issubdtype(a.dtype, np.integer)):
            bad(name + ' must have a real numeric dtype')
        if not np.all(np.isfinite(a)):
            bad(name + ' must be finite')
        if name in POSITIVE_VECTORS and not np.all(a > 0):
            bad(name + ' must be positive')
    nfree = None
    for name, X in (('U_R', U_R), ('U_phi', U_phi), ('U_z', U_z), ('divU', divU), ('G', G)):
        a = np.asarray(X)
        if a.ndim != 2:
            bad(name + ' must be 2-D')
        if nfree is None:
            nfree = a.shape[1]
        if a.shape != (npoints, nfree) or nfree < 1:
            bad(name + ' shape mismatch')
        if not np.issubdtype(a.dtype, np.number):
            bad(name + ' must be numeric')
        if not np.all(np.isfinite(a)):
            bad(name + ' must be finite')
    for name, f in (('f_R', f_R), ('f_phi', f_phi), ('f_z', f_z)):
        a = np.asarray(f)
        if a.shape != (npoints,):
            bad(name + ' must have shape (npoints,)')
        if not np.issubdtype(a.dtype, np.number):
            bad(name + ' must be numeric')
        if not np.all(np.isfinite(a)):
            bad(name + ' must be finite')
    return _reference()(R=R, rho=rho, P=P, K_R=K_R, K_z=K_z, P_R=P_R, P_z=P_z, Omega=Omega,
                        Omega_R=Omega_R, Omega_z=Omega_z, volume_weights=volume_weights, U_R=U_R,
                        U_phi=U_phi, U_z=U_z, divU=divU, G=G, f_R=f_R, f_phi=f_phi, f_z=f_z, m=m,
                        gamma=gamma, normalization_scale=normalization_scale, provenance=provenance)


def run_reference_selfcheck(out_json=None):
    res = run_all(_reference(), skip=('F6',), target_info={
        'label': 'reference_weak_euler_h2v001.reference_assemble (loop transcription)',
        'module_path': REFERENCE_PATH, 'module_sha256': sha256_file(REFERENCE_PATH),
        'func': 'reference_assemble',
        'note': 'F6 skipped: the reference performs no validation by design; F1 compares the '
                'reference with itself and is trivially satisfied here'})
    st = _Runner(_selftest_validating_reference, None)
    _fixture_F6(st)
    res['f6_harness_selftest'] = {
        'purpose': ('show the F6 probes are well-formed: every reject probe must be rejected and every '
                    'accept probe accepted (and match the reference) by a strict contract reading. '
                    'Harness self-test only; not a reference result and not a proposed implementation.'),
        'target': '_selftest_validating_reference in fixtures_weak_euler_h2v001.py',
        'summary': _f6_summary(st.checks), 'checks': st.checks}
    if out_json:
        _write_json(out_json, res)
    return res


# ----------------------------------------------------------------------------- CLI
def main(argv=None):
    ap = argparse.ArgumentParser(description='H2 manufactured-fixture harness for the pinned weak Euler '
                                             'contract (Claude4 review lane, dispatch 0440).')
    ap.add_argument('--module', help='target module FILE PATH')
    ap.add_argument('--func', help='target function name in that module')
    ap.add_argument('--adapter-module', help='optional adapter FILE PATH defining to_target/from_target')
    ap.add_argument('--out', required=True, help='output JSON path')
    ap.add_argument('--skip', default='', help='comma-separated fixture ids to skip, e.g. F6')
    ap.add_argument('--reference-run', action='store_true', help='run F0-F5 on the loop reference '
                                                                 'plus the F6 harness self-test')
    ap.add_argument('--mutation-study', action='store_true', help='run F7')
    a = ap.parse_args(argv)
    if a.reference_run:
        res = run_reference_selfcheck(a.out)
        ok = res['summary']['all_pass'] and not res['f6_harness_selftest']['summary']['failing_probes']
        print(json.dumps(_jsonable({'summary': res['summary'],
                                    'f6_selftest': res['f6_harness_selftest']['summary']['failing_probes']}),
                         indent=1))
    elif a.mutation_study:
        res = run_mutation_study(a.out)
        ok = res['summary']['control_all_pass'] and not res['summary']['undetected']
        print(json.dumps(_jsonable(res['summary']), indent=1))
    else:
        if not a.module or not a.func:
            ap.error('--module and --func are required unless --reference-run or --mutation-study')
        info = {'module_path': os.path.abspath(a.module), 'module_sha256': sha256_file(a.module),
                'func': a.func}
        mod = load_module_from_path(a.module, 'h2_target_under_review')
        target = getattr(mod, a.func)
        adapter = None
        if a.adapter_module:
            info['adapter_module_path'] = os.path.abspath(a.adapter_module)
            info['adapter_module_sha256'] = sha256_file(a.adapter_module)
            adapter = load_module_from_path(a.adapter_module, 'h2_target_adapter')
        skip = tuple(s.strip() for s in a.skip.split(',') if s.strip())
        res = run_all(target, adapter=adapter, out_json=a.out, skip=skip, target_info=info)
        ok = res['summary']['all_pass']
        out = {'summary': res['summary']}
        if 'f6_summary' in res:
            out['f6_failing_probes'] = res['f6_summary']['failing_probes']
        print(json.dumps(_jsonable(out), indent=1))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())

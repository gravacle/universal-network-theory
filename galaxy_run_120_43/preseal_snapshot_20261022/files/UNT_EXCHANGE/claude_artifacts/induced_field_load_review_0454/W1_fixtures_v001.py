#!/usr/bin/env python3
"""W1 independent fixture harness: dispatch 0454, Claude4 review of the 0453 induced-field weak load.

Helper W1 inside the Claude4 independent review lane.  Synthetic fixtures
only: no project data, no target data, no validation outcomes, no physical
acceptance.  The target file is never edited.  It is loaded by path with
bytecode writing disabled, and its SHA-256 is recorded before and after the run.

Usage (root interpreter; the same command runs under /usr/bin/python3 -I -B):
  OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \\
  <python> -I -B W1_fixtures_v001.py --module PATH --func NAME \\
      [--adapter-module PATH] [--reference PATH] [--ref0439 PATH] \\
      [--mutation-study] --out JSON

Canonical inputs: m; U_R, U_phi, U_z (n,k); rho (n,); volume_weights (n,);
gradient (n,3) = (grad_R, grad_phi, grad_z) mode-m coefficients;
normalization_scale.  Target parameters are matched by name.  If the
signature is unmatched or ambiguous, or the return value is not recognized,
the harness writes an adapter description to --out and exits with status 3.

Adapter protocol (--adapter-module PATH, loaded by path):
  call(func, canonical) -> raw   canonical = dict of the canonical inputs plus
                                  'R' (per-point radius, fixture context only)
  extract(raw) -> dict           optional; must give 'delta_b' (k,), may give
                                  'load_R', 'load_phi', 'load_z'

Exit status: 0 = every check and expected probe passed, 1 = a failure,
2 = usage error, 3 = adapter required.
"""

import sys

sys.dont_write_bytecode = True
if sys.version_info < (3, 12):
    sys.path.append("/Users/bgm/Library/Python/3.9/lib/python/site-packages")

import argparse
import cmath
import datetime
import hashlib
import importlib.util
import inspect
import json
import math
import os
import platform
import warnings

import numpy as np

HARNESS_VERSION = "W1_fixtures_v001"
DISPATCH_0454_SHA256 = "a6b544c8b40125e265380fa7f27d0885823a8ac5bf410fbc29ac720ca9f320fa"
SPEC_0453_SHA256 = "fbcda35f550b98aba8aace7021e30284b8ade417bbd6af60ded91dda32fbf2f0"
PINNED_0439_SHA256 = "8632bda6d4a80d0d25bfa90ef4b1066954b6bc67c90f184d0a78c232bf3013da"
NANG = 16
TWO_PI = 2.0 * math.pi
ANGLES = TWO_PI * np.arange(NANG) / NANG
RTOL = 1.0e-12      # value checks, relative to a target-independent absolute-value bound
FD_RTOL = 1.0e-6    # fixture self-check of the analytic derivatives by central differences
FD_STEP = 1.0e-5
HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_REFERENCE = os.path.join(HERE, "W1_reference_v001.py")
MAP_KEYS = ("U_R", "U_phi", "U_z")
COMP = ("R", "phi", "z")
REJ, ACC, REC = "expected_reject", "expected_accept", "record_only"


# ------------------------------------------------------------------ utilities
def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def load_module(path, tag):
    path = os.path.abspath(path)
    name = "w1_%s_%s" % (tag, hashlib.sha256(path.encode("utf-8")).hexdigest()[:12])
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot create an import spec for %s" % path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def jnum(x):
    x = float(x)
    return x if math.isfinite(x) else repr(x)


def jc(z):
    z = complex(z)
    return [jnum(z.real), jnum(z.imag)]


def sanitize(obj):
    """Make obj strictly JSON-serializable (no NaN/inf floats, no numpy scalars)."""
    if isinstance(obj, dict):
        return {str(k): sanitize(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [sanitize(v) for v in obj]
    if isinstance(obj, (bool, np.bool_)):
        return bool(obj)
    if isinstance(obj, (int, np.integer)):
        return int(obj)
    if isinstance(obj, (float, np.floating)):
        return jnum(obj)
    if isinstance(obj, (complex, np.complexfloating)):
        return jc(obj)
    if isinstance(obj, np.ndarray):
        return sanitize(obj.tolist())
    if obj is None or isinstance(obj, str):
        return obj
    return repr(obj)


# --------------------------------------------------------- signature mapping
def _norm(name):
    return "".join(ch for ch in name.lower() if ch.isalnum())


ALIASES = {
    "m": ("m", "mode", "azimuthalmode", "retainedmode", "mmode", "azimuthalm"),
    "U_R": ("ur", "xir", "mapr", "umapr", "ureducedr"),
    "U_phi": ("uphi", "up", "xiphi", "mapphi", "umapphi", "ureducedphi"),
    "U_z": ("uz", "xiz", "mapz", "umapz", "ureducedz"),
    "rho": ("rho", "density", "rho0", "backgrounddensity"),
    "volume_weights": ("volumeweights", "w", "weights", "vol", "volweights", "quadratureweights"),
    "gradient": ("grad", "gradient", "gradcoeffs", "gradcoefficients", "gradientcoefficients",
                 "gradientcoeffs", "inducedgradient", "inducedgrad", "graddphi", "graddeltaphi",
                 "fieldgradient", "inducedfieldgradient"),
    "normalization_scale": ("normalizationscale", "normalization", "normscale", "scale", "norm", "s"),
    "grad_R": ("gradr", "fr", "gr", "gradientr"),
    "grad_phi": ("gradphi", "fphi", "gphi", "gradientphi"),
    "grad_z": ("gradz", "fz", "gz", "gradientz"),
    "R": ("r", "radius", "radii", "rr"),
}
SPLIT = ("grad_R", "grad_phi", "grad_z")


class AdapterRequired(Exception):
    pass


class NotApplicable(Exception):
    pass


def resolve_signature(func):
    try:
        sig = inspect.signature(func)
    except (TypeError, ValueError) as exc:
        raise AdapterRequired("signature cannot be introspected: %s" % exc)
    mapping, problems, optional_unmatched, deviations = {}, [], [], []
    for p in sig.parameters.values():
        if p.kind in (p.VAR_POSITIONAL, p.VAR_KEYWORD):
            deviations.append("accepts %s%s" % ("*" if p.kind == p.VAR_POSITIONAL else "**", p.name))
            continue
        if p.name in ALIASES:
            cands = [p.name]
        else:
            cands = [key for key, al in ALIASES.items() if _norm(p.name) in al]
        if len(cands) == 1:
            mapping[p.name] = cands[0]
        elif len(cands) > 1:
            problems.append("parameter %r matches several canonical names %s" % (p.name, cands))
        elif p.default is p.empty:
            problems.append("required parameter %r matches no canonical name" % p.name)
        else:
            optional_unmatched.append(p.name)
    seen = {}
    for pname, key in mapping.items():
        seen.setdefault(key, []).append(pname)
    for key, pnames in seen.items():
        if len(pnames) > 1:
            problems.append("canonical %r matched by several parameters %s" % (key, pnames))
    keys = set(mapping.values())
    split_present = [key for key in SPLIT if key in keys]
    if "gradient" in keys and split_present:
        problems.append("both a combined gradient and split gradient components")
    elif "gradient" not in keys and len(split_present) != 3:
        problems.append("no (n,3) gradient parameter and no complete grad_R/grad_phi/grad_z split")
    for key in ("m", "U_R", "U_phi", "U_z", "rho", "volume_weights", "normalization_scale"):
        if key not in keys:
            problems.append("canonical input %r is not matched" % key)
    if split_present:
        deviations.append("gradient split into three parameters (0453 specifies one (n,3) array)")
    if "R" in keys:
        deviations.append("signature takes a radius parameter; 0453 lists no R input")
    if optional_unmatched:
        deviations.append("unmatched optional parameters left at defaults: %s" % optional_unmatched)
    kinds = sorted(set(str(p.kind) for p in sig.parameters.values()))
    return sig, mapping, problems, deviations, kinds


class MappedCaller(object):
    kind = "mapped"

    def __init__(self, func, sig, mapping):
        self.func, self.sig, self.mapping = func, sig, mapping

    def _value(self, case, key):
        if key in SPLIT:
            g = case["gradient"]
            if not (isinstance(g, np.ndarray) and g.ndim == 2 and g.shape[1] == 3):
                raise NotApplicable("split-gradient target cannot receive this gradient shape")
            return g[:, SPLIT.index(key)]
        return case[key]

    def call_raw(self, case, drop=(), extra=None, positional=False):
        args, kwargs = [], {}
        for p in self.sig.parameters.values():
            key = self.mapping.get(p.name)
            if key is None or key in drop or (key in SPLIT and "gradient" in drop):
                continue
            value = self._value(case, key)
            if positional or p.kind == p.POSITIONAL_ONLY:
                args.append(value)
            else:
                kwargs[p.name] = value
        if extra:
            kwargs.update(extra)
        return self.func(*args, **kwargs)


class AdapterCaller(object):
    kind = "adapter"

    def __init__(self, func, adapter):
        self.func, self.adapter = func, adapter

    def call_raw(self, case, drop=(), extra=None, positional=False):
        if drop or extra or positional:
            raise NotApplicable("call-interface probes do not apply through an adapter")
        return self.adapter.call(self.func, dict(case))


class DirectCaller(object):
    """W1 reference keyword names (grad=...); passes R when the function accepts it."""
    kind = "direct"

    def __init__(self, func, pass_R):
        self.func, self.pass_R = func, pass_R

    def call_raw(self, case, drop=(), extra=None, positional=False):
        kwargs = {"m": case["m"], "U_R": case["U_R"], "U_phi": case["U_phi"], "U_z": case["U_z"],
                  "rho": case["rho"], "volume_weights": case["volume_weights"],
                  "grad": case["gradient"], "normalization_scale": case["normalization_scale"]}
        if self.pass_R:
            kwargs["R"] = case["R"]
        return self.func(**kwargs)


DELTA_KEYS = ("delta_b", "b", "increment", "delta_load", "db")
LOAD_KEYS = {"R": ("load_R", "load_r", "loadR"), "phi": ("load_phi", "load_Phi", "loadPhi"),
             "z": ("load_z", "load_Z", "loadZ")}


def extract(raw, adapter=None):
    if adapter is not None and hasattr(adapter, "extract"):
        d = adapter.extract(raw)
        loads = dict((c, d["load_" + c]) for c in COMP if ("load_" + c) in d)
        return d["delta_b"], (loads or None)
    if isinstance(raw, dict):
        for key in DELTA_KEYS:
            if key in raw:
                db = raw[key]
                break
        else:
            raise AdapterRequired("returned dict has no delta_b key; keys %s" % sorted(map(str, raw)))
        loads = {}
        for c, names in LOAD_KEYS.items():
            for nm in names:
                if nm in raw:
                    loads[c] = raw[nm]
                    break
        return db, (loads or None)
    if isinstance(raw, np.ndarray):
        return raw, None
    if isinstance(raw, tuple) and raw and isinstance(raw[0], np.ndarray):
        return raw[0], None
    raise AdapterRequired("unrecognized return type %s" % type(raw).__name__)


class Target(object):
    def __init__(self, caller, adapter=None):
        self.caller, self.adapter = caller, adapter

    def raw(self, case, **kw):
        return self.caller.call_raw(case, **kw)

    def run(self, case):
        db, loads = extract(self.caller.call_raw(case), self.adapter)
        return np.asarray(db), loads


# ------------------------------------------------------------ synthetic cases
def points(rng, n):
    R = rng.uniform(0.3, 2.5, n)
    z = rng.uniform(-1.0, 1.0, n)
    dR = rng.uniform(0.05, 0.3, n)
    dz = rng.uniform(0.05, 0.3, n)
    w = R * dR * dz  # R dR dz, no 2 pi
    rho = rng.uniform(0.4, 3.0, n)
    return R, z, w, rho


def make_maps(rng, n, k, kind):
    if kind == "general":
        return tuple(rng.normal(size=(n, k)) + 1j * rng.normal(size=(n, k)) for _ in range(3))
    if kind == "root":  # root's dtypes: U_R, U_z real float64; U_phi purely imaginary complex128
        return rng.normal(size=(n, k)), 1j * rng.normal(size=(n, k)), rng.normal(size=(n, k))
    raise ValueError(kind)


def random_case(seed, n, k, m, kind, s):
    rng = np.random.default_rng(seed)
    R, z, w, rho = points(rng, n)
    U_R, U_phi, U_z = make_maps(rng, n, k, kind)
    grad = rng.normal(size=(n, 3)) + 1j * rng.normal(size=(n, 3))
    return {"m": m, "U_R": U_R, "U_phi": U_phi, "U_z": U_z, "rho": rho, "volume_weights": w,
            "gradient": grad, "normalization_scale": s, "R": R, "z": z}


def copy_case(case, **changes):
    out = {}
    for key, value in case.items():
        out[key] = value.copy() if isinstance(value, np.ndarray) else value
    out.update(changes)
    return out


def hand_cases():
    """Dyadic inputs: every product and sum is exact, so every correct implementation is exact."""
    H1 = {"m": 1, "U_R": np.array([[2.0]]), "U_phi": np.array([[3j]]), "U_z": np.array([[5.0]]),
          "rho": np.array([2.0]), "volume_weights": np.array([0.5]),
          "gradient": np.array([[1 + 1j, 2j, -1.0]]), "normalization_scale": 4.0,
          "R": np.array([2.0])}
    H2 = {"m": 3,
          "U_R": np.array([[1 + 1j, 0.5], [0.0, -2j]]),
          "U_phi": np.array([[0.5j, 1.0], [1 - 1j, 0.0]]),
          "U_z": np.array([[-1.0, 0.25j], [2.0, 1 + 1j]]),
          "rho": np.array([2.0, 0.5]), "volume_weights": np.array([0.25, 3.0]),
          "gradient": np.array([[1.0, 2j, -0.5], [0.5 - 1j, 1.0, 2.0]]),
          "normalization_scale": 2.0, "R": np.array([0.5, 4.0])}
    H3 = {"m": 1, "U_R": np.array([[1.0]]), "U_phi": np.array([[0j]]), "U_z": np.array([[0.0]]),
          "rho": np.array([1.0]), "volume_weights": np.array([1.0]),
          "gradient": np.array([[1.0 + 0j, 0.0, 0.0]]), "normalization_scale": 1.0,
          "R": np.array([3.0])}
    return [
        ("H1_one_point_root_dtypes", H1, np.array([-0.75 - 0.5j]),
         {"R": np.array([-0.5 - 0.5j]), "phi": np.array([-1.5 + 0j]), "z": np.array([1.25 + 0j])}),
        ("H2_two_points_general", H2, np.array([-4.375 - 0.5j, -3.125 + 0.21875j]),
         {"R": np.array([-0.25 + 0.25j, -1.625 - 0.75j]), "phi": np.array([-1.0 - 0.75j, -0.5j]),
          "z": np.array([-3.125 + 0j, -1.5 + 1.46875j])}),
        ("H3_sign_unit", H3, np.array([-1.0 + 0j]),
         {"R": np.array([-1.0 + 0j]), "phi": np.array([0j]), "z": np.array([0j])}),
    ]


# --------------------------------------------------- analytic real potential
def potential_terms(rng, modes):
    terms = []
    for mp in modes:
        terms.append({"mp": int(mp), "A": complex(rng.normal(), rng.normal()), "p": int(mp % 3),
                      "a": complex(rng.uniform(0.3, 0.8), rng.uniform(-0.3, 0.3)),
                      "b": float(rng.uniform(-2.0, 2.0)),
                      "c": complex(rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5))})
    return terms


def phi_mode(t, R, z):
    """Phi_m'(R,z) = A R^p exp(-a R^2 + i b z) (1 + c z^2), complex, closed form."""
    core = t["A"] * R ** t["p"] * np.exp(-t["a"] * R ** 2 + 1j * t["b"] * z)
    return core * (1.0 + t["c"] * z ** 2)


def grad_mode(t, R, z):
    """Analytic mode-m' coefficients of (d_R, (1/R) d_phi, d_z) applied to Phi_m' exp(i m' phi)."""
    core = t["A"] * R ** t["p"] * np.exp(-t["a"] * R ** 2 + 1j * t["b"] * z)
    poly = 1.0 + t["c"] * z ** 2
    Phi = core * poly
    dR = Phi * (t["p"] / R - 2.0 * t["a"] * R)
    dphi_over_R = (1j * t["mp"] / R) * Phi
    dz = core * (1j * t["b"] * poly + 2.0 * t["c"] * z)
    return dR, dphi_over_R, dz


def delta_phi(terms, R, ang, z):
    """REAL deltaPhi(R, phi, z) = sum_m' 2 Re[Phi_m'(R,z) exp(i m' phi)], shape (n, len(ang))."""
    out = np.zeros((len(R), len(ang)))
    for t in terms:
        out += 2.0 * np.real(phi_mode(t, R, z)[:, None] * np.exp(1j * t["mp"] * ang)[None, :])
    return out


def gradient_fields(terms, R, z):
    """Real cylindrical gradient (g_R, g_phi=(1/R)d_phi, g_z) on the 16 angles: (3, n, 16)."""
    g = np.zeros((3, len(R), NANG))
    for t in terms:
        comps = grad_mode(t, R, z)
        e = np.exp(1j * t["mp"] * ANGLES)
        for c in range(3):
            g[c] += 2.0 * np.real(comps[c][:, None] * e[None, :])
    return g


def analytic_coefficients(terms, R, z, m):
    out = np.zeros((len(R), 3), dtype=complex)
    for t in terms:
        if t["mp"] == m:
            comps = grad_mode(t, R, z)
            for c in range(3):
                out[:, c] += comps[c]
    return out


def fft_coefficients(g, m):
    """Root convention: numpy.fft.fft over the 16 angles, bin m, divided by 16."""
    return np.stack([np.fft.fft(g[c], axis=1)[:, m] / NANG for c in range(3)], axis=1)


PROJ_CASES = (
    # id, seed, n, k, m, maps, normalization_scale, modes m' present in the real potential
    ("m1_general", 1101, 11, 4, 1, "general", 2.3, (1, 2, 3, 4, 5, 6, 7)),
    ("m2_root", 1102, 9, 3, 2, "root", 1.7, (1, 2, 3, 4, 5, 6, 7)),
    ("m3_general", 1103, 8, 2, 3, "general", 3.1, (1, 2, 3, 4, 5, 6, 7)),
    ("m4_root", 1104, 11, 4, 4, "root", 0.37, (1, 2, 3, 4, 5, 6, 7)),
    ("m5_root", 1105, 7, 5, 5, "root", 0.81, (1, 2, 3, 4, 5, 6, 7)),
    ("m6_general_k_gt_n", 1106, 5, 7, 6, "general", 5.9, (1, 2, 3, 4, 5, 6, 7)),
    ("m3_offmode_only", 1107, 8, 3, 3, "general", 2.3, (1, 2, 4, 5, 6, 7)),
)


def direct_projection(case, g):
    """-sum_p w rho sum_c conj(U_c) (1/2pi) sum_j (2pi/16) exp(-i m phi_j) g_c, by explicit loops."""
    m = case["m"]
    maps_ = [case[key] for key in MAP_KEYS]
    rho, w = case["rho"], case["volume_weights"]
    n, k = maps_[0].shape
    twiddle = [cmath.exp(-1j * m * TWO_PI * a / NANG) for a in range(NANG)]
    coef = np.zeros((n, 3), dtype=complex)
    cbound = np.zeros((n, 3))
    for p in range(n):
        for c in range(3):
            acc, ab = 0j, 0.0
            for a in range(NANG):
                val = float(g[c, p, a])
                acc += (TWO_PI / NANG) * twiddle[a] * val
                ab += (TWO_PI / NANG) * abs(val)
            coef[p, c] = acc / TWO_PI
            cbound[p, c] = ab / TWO_PI
    direct, bound = [], []
    for j in range(k):
        acc, ab = 0j, 0.0
        for p in range(n):
            wr = float(w[p]) * float(rho[p])
            for c in range(3):
                u = complex(maps_[c][p, j]).conjugate()
                acc += -wr * u * complex(coef[p, c])
                ab += wr * abs(u) * float(cbound[p, c])
        direct.append(acc)
        bound.append(ab)
    return np.array(direct), np.array(bound), coef


def real_virtual_work(case, g, y):
    """W = sum_p w_p sum_j (2pi/16) xi.F with xi = 2 Re(U y e^{i m phi}), F = -rho grad(deltaPhi)."""
    m = case["m"]
    maps_ = [case[key] for key in MAP_KEYS]
    rho, w = case["rho"], case["volume_weights"]
    n, k = maps_[0].shape
    phase = [cmath.exp(1j * m * TWO_PI * a / NANG) for a in range(NANG)]
    W, bound = 0.0, 0.0
    for p in range(n):
        amp = []
        for c in range(3):
            t = 0j
            for j in range(k):
                t += complex(maps_[c][p, j]) * complex(y[j])
            amp.append(t)
        for a in range(NANG):
            for c in range(3):
                xi = 2.0 * (amp[c] * phase[a]).real
                force = -float(rho[p]) * float(g[c, p, a])
                term = float(w[p]) * (TWO_PI / NANG) * xi * force
                W += term
                bound += abs(term)
    return W, bound


def build_potential_case(spec):
    cid, seed, n, k, m, kind, s, modes = spec
    rng = np.random.default_rng(seed)
    R, z, w, rho = points(rng, n)
    U_R, U_phi, U_z = make_maps(rng, n, k, kind)
    terms = potential_terms(rng, modes)
    g = gradient_fields(terms, R, z)
    case = {"m": m, "U_R": U_R, "U_phi": U_phi, "U_z": U_z, "rho": rho, "volume_weights": w,
            "gradient": fft_coefficients(g, m), "normalization_scale": s, "R": R, "z": z}
    pc = {"id": cid, "case": case, "terms": terms, "g": g, "kind": kind, "modes": list(modes),
          "coef_analytic": analytic_coefficients(terms, R, z, m)}
    direct, bound, coef_dft = direct_projection(case, g)
    pc.update(direct=direct, bound=bound, coef_dft=coef_dft)
    yrng = np.random.default_rng(seed + 7)
    ys = [yrng.normal(size=k) + 1j * yrng.normal(size=k) for _ in range(4)]
    pc["vw_random"] = [(y, real_virtual_work(case, g, y)) for y in ys]
    recon = []
    for j in range(k):
        e = np.zeros(k, dtype=complex)
        e[j] = 1.0
        recon.append((real_virtual_work(case, g, e), real_virtual_work(case, g, 1j * e)))
    pc["vw_recon"] = recon
    return pc


# ---------------------------------------------------------- formula helpers
def formula(case):
    """Vectorized 0453 formula (elementwise products and sums; no matrix product)."""
    U = [np.asarray(case[key]).astype(complex) for key in MAP_KEYS]
    wr = np.asarray(case["volume_weights"]).astype(float) * np.asarray(case["rho"]).astype(float)
    q = wr[:, None] * np.asarray(case["gradient"]).astype(complex)
    tot = sum((np.conj(U[c]) * q[:, c:c + 1]).sum(axis=0) for c in range(3))
    return -tot / float(case["normalization_scale"])


def formula_component(case, c):
    U = np.asarray(case[MAP_KEYS[c]]).astype(complex)
    wr = np.asarray(case["volume_weights"]).astype(float) * np.asarray(case["rho"]).astype(float)
    q = wr * np.asarray(case["gradient"]).astype(complex)[:, c]
    return -(np.conj(U) * q[:, None]).sum(axis=0) / float(case["normalization_scale"])


def component_loop(case, c):
    """-U_c^H (w rho g_c) / s by explicit loops (component isolation expectation)."""
    U = case[MAP_KEYS[c]]
    n, k = U.shape
    out = []
    for j in range(k):
        acc = 0j
        for p in range(n):
            wr = float(case["volume_weights"][p]) * float(case["rho"][p])
            acc += complex(U[p, j]).conjugate() * (wr * complex(case["gradient"][p, c]))
        out.append(-acc / float(case["normalization_scale"]))
    return np.array(out)


def coef_bound(case):
    U = [np.abs(np.asarray(case[key]).astype(complex)) for key in MAP_KEYS]
    wr = np.abs(np.asarray(case["volume_weights"]).astype(float) * np.asarray(case["rho"]).astype(float))
    q = wr[:, None] * np.abs(np.asarray(case["gradient"]).astype(complex))
    return sum((U[c] * q[:, c:c + 1]).sum(axis=0) for c in range(3)) / abs(float(case["normalization_scale"]))


def compare(got, expected, tol):
    got = np.asarray(got)
    expected = np.asarray(expected).astype(complex)
    if got.shape != expected.shape:
        return False, None, "shape %s, expected %s" % (got.shape, expected.shape)
    gotc = got.astype(complex)
    if not np.all(np.isfinite(gotc)):
        return False, None, "non-finite values"
    tol = np.broadcast_to(np.asarray(tol, dtype=float), expected.shape)
    err = np.abs(gotc - expected)
    return bool(np.all(err <= tol)), (float(err.max()) if err.size else 0.0), None


def rec(cid, family, passed, err=None, tol=None, note=None, **extra):
    d = {"id": cid, "family": family, "passed": bool(passed)}
    if err is not None:
        d["max_abs_err"] = jnum(err)
    if tol is not None:
        tmax = float(np.max(tol)) if np.size(tol) else 0.0
        d["tol_max"] = jnum(tmax)
        if err is not None and tmax > 0:
            d["max_err_over_bound"] = jnum(err / (tmax / RTOL))
    if note:
        d["note"] = note
    d.update(extra)
    return d


def checked(cid, family, fn):
    try:
        return fn()
    except Exception as exc:
        return rec(cid, family, False, note="exception %s: %s" % (type(exc).__name__, str(exc)[:300]))


def cmp_rec(cid, family, got, expected, tol, note=None, **extra):
    ok, err, why = compare(got, expected, tol)
    full = "; ".join(x for x in (note, why) if x)
    return rec(cid, family, ok, err, tol, full or None, **extra)


# --------------------------------------------------------- fixture families
def family_selfcheck(pcs):
    """Target-independent validation of the fixtures themselves."""
    out = []
    h = FD_STEP
    for pc in pcs:
        case, terms, g, m = pc["case"], pc["terms"], pc["g"], pc["case"]["m"]
        R, z = case["R"], case["z"]
        gmax = float(np.abs(g).max())
        fd = [(delta_phi(terms, R + h, ANGLES, z) - delta_phi(terms, R - h, ANGLES, z)) / (2 * h),
              (delta_phi(terms, R, ANGLES + h, z) - delta_phi(terms, R, ANGLES - h, z)) / (2 * h) / R[:, None],
              (delta_phi(terms, R, ANGLES, z + h) - delta_phi(terms, R, ANGLES, z - h)) / (2 * h)]
        err = max(float(np.abs(fd[c] - g[c]).max()) for c in range(3))
        out.append(rec("selfcheck_fd_gradient_" + pc["id"], "fixture_selfcheck", err <= FD_RTOL * gmax,
                       err, FD_RTOL * gmax, "central differences of the real deltaPhi vs analytic gradient"))
        out.append(cmp_rec("selfcheck_fft16_eq_analytic_" + pc["id"], "fixture_selfcheck",
                           case["gradient"], pc["coef_analytic"], RTOL * gmax,
                           note="FFT/16 bin m equals the analytic exp(+i m phi) coefficient"))
        out.append(cmp_rec("selfcheck_direct_dft_eq_fft16_" + pc["id"], "fixture_selfcheck",
                           pc["coef_dft"], case["gradient"], RTOL * gmax,
                           note="(1/2pi) sum_j (2pi/16) e^{-i m phi_j} g equals FFT/16 bin m"))
        neg = np.stack([np.fft.fft(g[c], axis=1)[:, NANG - m] / NANG for c in range(3)], axis=1)
        out.append(cmp_rec("selfcheck_real_field_bin_minus_m_" + pc["id"], "fixture_selfcheck",
                           neg, np.conj(case["gradient"]), RTOL * gmax,
                           note="real field: bin -m is the conjugate of bin m"))
    return out


def family_hand(target):
    out = []
    for hid, case, expected, _loads in hand_cases():
        def one(hid=hid, case=case, expected=expected):
            db, _ = target.run(copy_case(case))
            ok, err, why = compare(db, expected, 0.0)
            return rec("hand_" + hid, "hand", ok, err, None, why or "exact dyadic arithmetic required",
                       got=[jc(v) for v in np.asarray(db).ravel()[:4]],
                       expected=[jc(v) for v in expected])
        out.append(checked("hand_" + hid, "hand", one))
    return out


def family_projection_and_virtual_work(target, pcs):
    out = []
    for pc in pcs:
        case = pc["case"]
        s = float(case["normalization_scale"])
        k = case["U_R"].shape[1]
        try:
            db, _ = target.run(copy_case(case))
            db = np.asarray(db)
        except Exception as exc:
            note = "exception %s: %s" % (type(exc).__name__, str(exc)[:300])
            for fam in ("proj_direct", "proj_coeff_consistency", "vw_random", "vw_reconstruct"):
                out.append(rec(fam + "_" + pc["id"], fam, False, note=note))
            continue
        out.append(checked("proj_direct_" + pc["id"], "proj_direct", lambda: cmp_rec(
            "proj_direct_" + pc["id"], "proj_direct", db.astype(complex) * s, pc["direct"],
            RTOL * pc["bound"], note="target*s vs direct 16-angle projection integral",
            modes_in_potential=pc["modes"], m=case["m"], maps=pc["kind"])))

        def coeff():
            db_an, _ = target.run(copy_case(case, gradient=pc["coef_analytic"].copy()))
            return cmp_rec("proj_coeff_consistency_" + pc["id"], "proj_coeff_consistency", db_an, db,
                           RTOL * pc["bound"] / s, note="analytic coefficient input vs FFT/16 input")
        out.append(checked("proj_coeff_consistency_" + pc["id"], "proj_coeff_consistency", coeff))

        def vw_random():
            worst, worst_rel, ok = 0.0, 0.0, True
            details = []
            for y, (W, bW) in pc["vw_random"]:
                pred = 4.0 * math.pi * float(np.real(np.sum(np.conj(y) * db.astype(complex) * s)))
                tol = RTOL * (bW + 4.0 * math.pi * float(np.sum(np.abs(y) * pc["bound"])))
                err = abs(W - pred)
                ok = ok and math.isfinite(pred) and err <= tol
                worst = max(worst, err)
                worst_rel = max(worst_rel, err / (tol / RTOL))
                details.append({"W_real": jnum(W), "four_pi_Re_yH_b_s": jnum(pred), "abs_err": jnum(err)})
            return rec("vw_random_" + pc["id"], "vw_random", ok, worst, None,
                       "W_real == 4 pi Re(y^H (delta_b s)) for 4 random complex y",
                       max_err_over_bound=jnum(worst_rel), samples=details)
        out.append(checked("vw_random_" + pc["id"], "vw_random", vw_random))

        def vw_recon():
            brec, tols = [], []
            for j in range(k):
                (W1, b1), (W2, b2) = pc["vw_recon"][j]
                brec.append((W1 + 1j * W2) / (4.0 * math.pi * s))
                tols.append(RTOL * ((b1 + b2) / (4.0 * math.pi * s) + pc["bound"][j] / s))
            return cmp_rec("vw_reconstruct_" + pc["id"], "vw_reconstruct", db, np.array(brec),
                           np.array(tols), note="delta_b_k = (W(e_k) + i W(i e_k)) / (4 pi s)")
        out.append(checked("vw_reconstruct_" + pc["id"], "vw_reconstruct", vw_recon))
    return out


def family_identities(target):
    out = []
    base = random_case(2001, 10, 3, 2, "general", 2.3)
    bnd = coef_bound(base)

    def run(case):
        return target.run(case)[0].astype(complex)

    def i_alpha(alpha, cid):
        def f():
            b0 = run(copy_case(base))
            b1 = run(copy_case(base, gradient=base["gradient"] * alpha))
            return cmp_rec(cid, "ident", b1, alpha * b0, 2 * RTOL * abs(alpha) * bnd,
                           note="complex-linear in the supplied gradient coefficient")
        out.append(checked(cid, "ident", f))
    i_alpha(0.6 - 1.3j, "ident_grad_scaled_complex")
    i_alpha(1j, "ident_grad_times_i")

    def maps_alpha():
        alpha = -0.7 + 0.9j
        b0 = run(copy_case(base))
        b1 = run(copy_case(base, U_R=base["U_R"] * alpha, U_phi=base["U_phi"] * alpha,
                           U_z=base["U_z"] * alpha))
        return cmp_rec("ident_maps_scaled_conjugate", "ident", b1, np.conj(alpha) * b0,
                       2 * RTOL * abs(alpha) * bnd, note="conjugate-linear in the maps (U^H)")
    out.append(checked("ident_maps_scaled_conjugate", "ident", maps_alpha))

    def additive():
        g2 = np.random.default_rng(2002).normal(size=(10, 3)) + 1j * np.random.default_rng(2003).normal(size=(10, 3))
        c2 = copy_case(base, gradient=g2)
        b12 = run(copy_case(base, gradient=base["gradient"] + g2))
        return cmp_rec("ident_grad_additive", "ident", b12, run(copy_case(base)) + run(c2),
                       2 * RTOL * (bnd + coef_bound(c2)), note="additive in the gradient")
    out.append(checked("ident_grad_additive", "ident", additive))

    def scale(cid, key, factor, expect_factor):
        def f():
            b0 = run(copy_case(base))
            val = base[key] * factor if isinstance(base[key], np.ndarray) else base[key] * factor
            b1 = run(copy_case(base, **{key: val}))
            return cmp_rec(cid, "ident", b1, expect_factor * b0, 2 * RTOL * max(1.0, abs(expect_factor)) * bnd)
        out.append(checked(cid, "ident", f))
    scale("ident_rho_scaled_2.5", "rho", 2.5, 2.5)
    scale("ident_w_scaled_0.4", "volume_weights", 0.4, 0.4)
    scale("ident_s_scaled_3", "normalization_scale", 3.0, 1.0 / 3.0)

    def permute_points():
        perm = np.random.default_rng(2004).permutation(10)
        c = copy_case(base)
        for key in MAP_KEYS + ("rho", "volume_weights", "gradient", "R", "z"):
            c[key] = base[key][perm].copy()
        return cmp_rec("ident_point_permutation", "ident", run(c), run(copy_case(base)), 2 * RTOL * bnd)
    out.append(checked("ident_point_permutation", "ident", permute_points))

    def permute_columns():
        perm = np.array([2, 0, 1])
        c = copy_case(base, U_R=base["U_R"][:, perm].copy(), U_phi=base["U_phi"][:, perm].copy(),
                      U_z=base["U_z"][:, perm].copy())
        return cmp_rec("ident_column_permutation", "ident", run(c), run(copy_case(base))[perm],
                       2 * RTOL * bnd[perm])
    out.append(checked("ident_column_permutation", "ident", permute_columns))

    def m_independent():
        b2 = run(copy_case(base))
        worst, bitwise, ok = 0.0, True, True
        for mv in range(1, 7):
            bm = run(copy_case(base, m=mv))
            okm, err, _ = compare(bm, b2, 2 * RTOL * bnd)
            ok = ok and okm
            worst = max(worst, err if err is not None else float("inf"))
            bitwise = bitwise and bm.tobytes() == b2.tobytes()
        return rec("ident_m_independent", "ident", ok, worst, 2 * RTOL * bnd,
                   "the 0453 formula contains no m; m = 1..6 must give the same delta_b",
                   bitwise_identical_for_all_m=bitwise)
    out.append(checked("ident_m_independent", "ident", m_independent))

    def comp_additive():
        parts = []
        for c in range(3):
            g = np.zeros_like(base["gradient"])
            g[:, c] = base["gradient"][:, c]
            parts.append(run(copy_case(base, gradient=g)))
        return cmp_rec("ident_component_additive", "ident", parts[0] + parts[1] + parts[2],
                       run(copy_case(base)), 3 * RTOL * bnd)
    out.append(checked("ident_component_additive", "ident", comp_additive))

    def deterministic():
        b1, b2 = run(copy_case(base)), run(copy_case(base))
        return rec("ident_deterministic_bitwise", "ident", b1.tobytes() == b2.tobytes(),
                   note="two identical calls must agree bitwise")
    out.append(checked("ident_deterministic_bitwise", "ident", deterministic))

    def dtype_consistency():
        root = random_case(2005, 9, 3, 2, "root", 1.3)
        cplx = copy_case(root, U_R=root["U_R"].astype(complex), U_z=root["U_z"].astype(complex))
        b_real, b_cplx = run(copy_case(root)), run(cplx)
        return cmp_rec("ident_real_dtype_maps_eq_complex_dtype", "ident", b_real, b_cplx,
                       2 * RTOL * coef_bound(root),
                       bitwise_identical=b_real.tobytes() == b_cplx.tobytes(),
                       note="root's float64 U_R/U_z vs the same values as complex128")
    out.append(checked("ident_real_dtype_maps_eq_complex_dtype", "ident", dtype_consistency))
    return out


def family_components(target):
    out = []
    base = random_case(3001, 8, 3, 4, "general", 1.9)
    for c, key in enumerate(MAP_KEYS):
        only = copy_case(base)
        for other in MAP_KEYS:
            if other != key:
                only[other] = np.zeros_like(base[other])
        expected = component_loop(only, c)
        out.append(checked("comp_only_" + key, "comp", lambda only=only, expected=expected, key=key: cmp_rec(
            "comp_only_" + key, "comp", target.run(only)[0], expected, 2 * RTOL * coef_bound(only),
            note="only %s nonzero: -%s^H (w rho g[:, %d]) / s" % (key, key, MAP_KEYS.index(key)))))
        zero = copy_case(only)
        zero["gradient"][:, c] = 0.0
        out.append(checked("comp_cross_zero_" + key, "comp", lambda zero=zero, key=key, c=c: cmp_rec(
            "comp_cross_zero_" + key, "comp", target.run(zero)[0], np.zeros(3), 0.0,
            note="only %s nonzero and gradient column %d zero: exact zero required" % (key, c))))
    return out


def family_loads(target):
    """Identify the component-load convention and check its consistency (if loads are returned)."""
    cases = [("H2", hand_cases()[1][1]), ("random", random_case(3101, 7, 3, 5, "general", 2.9))]
    found, conv_seen, ok_all, notes = False, set(), True, []
    sum_errs = []
    for cname, case in cases:
        try:
            db, loads = target.run(copy_case(case))
        except Exception as exc:
            return [rec("loads_convention", "loads", False,
                        note="exception %s: %s" % (type(exc).__name__, str(exc)[:200]))]
        if not loads:
            continue
        found = True
        bnd = coef_bound(case)
        s = float(case["normalization_scale"])
        for c in COMP:
            if c not in loads:
                ok_all = False
                notes.append("%s: load_%s missing" % (cname, c))
                continue
            spec_like = formula_component(case, COMP.index(c))
            cands = {"-U^H(w rho g)/s": spec_like, "-U^H(w rho g)": spec_like * s,
                     "+U^H(w rho g)/s": -spec_like, "+U^H(w rho g)": -spec_like * s}
            matched = [name for name, val in cands.items()
                       if compare(loads[c], val, 4 * RTOL * max(1.0, s) * bnd)[0]]
            conv_seen.add(matched[0] if matched else "none")
            if not matched:
                ok_all = False
                notes.append("%s: load_%s matches no simple convention" % (cname, c))
        if all(c in loads for c in COMP):
            total = sum(np.asarray(loads[c]).astype(complex) for c in COMP)
            sum_errs.append(float(np.abs(total - np.asarray(db).astype(complex)).max()) /
                            max(float(np.max(bnd)), 1e-300))
    if not found:
        return [rec("loads_absent", "loads_record", True, note="target returned no component loads")]
    consistent = ok_all and len(conv_seen) == 1
    out = [rec("loads_convention_consistent", "loads", consistent,
               note="; ".join(notes) or "all components on all cases follow one convention",
               conventions_seen=sorted(conv_seen))]
    if conv_seen == {"-U^H(w rho g)/s"}:
        worst = max(sum_errs) if sum_errs else float("inf")
        out.append(rec("loads_sum_equals_delta_b", "loads", worst <= 4 * RTOL,
                       note="load_R + load_phi + load_z == delta_b (relative to the bound)",
                       max_err_over_bound=jnum(worst)))
    else:
        out.append(rec("loads_sum_equals_delta_b_record", "loads_record", True,
                       note="convention is not -U^H(w rho g)/s; sum relation recorded only",
                       max_err_over_bound=[jnum(v) for v in sum_errs]))
    return out


def family_formula(target, pcs):
    out = []
    cases = [(pc["id"], pc["case"]) for pc in pcs]
    cases += [("ident_base", random_case(2001, 10, 3, 2, "general", 2.3)),
              ("root_k_gt_n", random_case(2006, 4, 6, 5, "root", 0.9))]
    for cid, case in cases:
        out.append(checked("formula_" + cid, "formula", lambda case=case, cid=cid: cmp_rec(
            "formula_" + cid, "formula", target.run(copy_case(case))[0], formula(case),
            4 * RTOL * coef_bound(case), note="vectorized harness formula (sum, no matmul)")))
    return out


def family_reference(target, ref_func, pcs, is_self):
    out = []
    cases = [(pc["id"], pc["case"]) for pc in pcs]
    cases += [("ident_base", random_case(2001, 10, 3, 2, "general", 2.3)),
              ("root_k_gt_n", random_case(2006, 4, 6, 5, "root", 0.9))]
    for cid, case in cases:
        def f(case=case, cid=cid):
            r = ref_func(m=case["m"], U_R=case["U_R"], U_phi=case["U_phi"], U_z=case["U_z"],
                         rho=case["rho"], volume_weights=case["volume_weights"], grad=case["gradient"],
                         normalization_scale=case["normalization_scale"])
            db = target.run(copy_case(case))[0]
            return cmp_rec("ref_" + cid, "ref", db, r["delta_b"], 4 * RTOL * coef_bound(case),
                           note=("self-comparison: target is the W1 reference" if is_self
                                 else "W1 loop reference"),
                           bitwise_identical=np.asarray(db).astype(complex).tobytes() == r["delta_b"].tobytes())
        out.append(checked("ref_" + cid, "ref", f))
    return out


def call_0439_b(mod0439, case):
    n, k = case["U_R"].shape
    zeros = np.zeros(n)
    g = np.asarray(case["gradient"])
    res = mod0439.assemble_weak_euler(
        R=case["R"], rho=case["rho"], P=np.full(n, 1.3), K_R=zeros, K_z=zeros, P_R=zeros, P_z=zeros,
        Omega=zeros, Omega_R=zeros, Omega_z=zeros, volume_weights=case["volume_weights"],
        U_R=case["U_R"], U_phi=case["U_phi"], U_z=case["U_z"],
        divU=np.zeros((n, k), dtype=complex), G=np.zeros((n, k), dtype=complex),
        f_R=np.ascontiguousarray(g[:, 0]), f_phi=np.ascontiguousarray(g[:, 1]),
        f_z=np.ascontiguousarray(g[:, 2]), m=int(case["m"]), gamma=5.0 / 3.0,
        normalization_scale=float(case["normalization_scale"]),
        provenance="W1 synthetic 0454 cross-check (b slice only; other inputs inert)")
    return res["b"]


def family_x0439(target, mod0439, pcs):
    out = []
    cases = [("H2_two_points_general", hand_cases()[1][1])]
    cases += [(pc["id"], pc["case"]) for pc in pcs if pc["id"] in ("m1_general", "m4_root", "m6_general_k_gt_n")]
    cases += [("root_n12_k5", random_case(5002, 12, 5, 6, "root", 0.37)),
              ("general_n9_k4", random_case(5001, 9, 4, 1, "general", 2.3))]
    for cid, case in cases:
        def f(case=case, cid=cid):
            b = call_0439_b(mod0439, case)
            db = np.asarray(target.run(copy_case(case))[0])
            return cmp_rec("x0439_" + cid, "x0439", db, b, 4 * RTOL * coef_bound(case),
                           note="target delta_b vs frozen 0439 assemble_weak_euler b",
                           bitwise_identical=(db.dtype == b.dtype and db.shape == b.shape
                                              and db.tobytes() == b.tobytes()))
        out.append(checked("x0439_" + cid, "x0439", f))
    return out


def caveat_illustration(target):
    """Record only: projection is complex-linear in G; a real field chain y -> G need not be."""
    case = random_case(6001, 7, 3, 2, "general", 1.3)
    m = case["m"]
    y = np.random.default_rng(6002).normal(size=3) + 1j * np.random.default_rng(6003).normal(size=3)
    rows = []
    for eps in (0.0, 0.3):
        def chain(yv):
            G = np.zeros((7, 3), dtype=complex)
            for c, key in enumerate(MAP_KEYS):
                a = (case[key] * yv[None, :]).sum(axis=1)
                xi = 2.0 * np.real(a[:, None] * np.exp(1j * m * ANGLES)[None, :])  # real displacement
                field = (1.0 + eps * np.cos(2 * m * ANGLES))[None, :] * xi           # toy real field
                G[:, c] = np.fft.fft(field, axis=1)[:, m] / NANG
            return G
        Gy, Giy = chain(y), chain(1j * y)
        a_mat = np.stack([(case[key] * y[None, :]).sum(axis=1) for key in MAP_KEYS], axis=1)
        selfcheck = float(np.abs(Gy - (a_mat + 0.5 * eps * np.conj(a_mat))).max())
        b_y = target.run(copy_case(case, gradient=Gy))[0].astype(complex)
        b_iy = target.run(copy_case(case, gradient=Giy))[0].astype(complex)
        b_iG = target.run(copy_case(case, gradient=1j * Gy))[0].astype(complex)
        norm = float(np.linalg.norm(b_y))
        rows.append({"eps": eps,
                     "chain_G_eq_a_plus_half_eps_conj_a_maxerr": jnum(selfcheck),
                     "projection_defect_|b(iG)-i b(G)|/|b(G)|": jnum(np.linalg.norm(b_iG - 1j * b_y) / norm),
                     "chain_defect_|b(G(iy))-i b(G(y))|/|b(G(y))|": jnum(np.linalg.norm(b_iy - 1j * b_y) / norm)})
    return {"description": "toy real chain y -> xi = 2Re(U y e^{i m phi}) -> field (1 + eps cos 2m phi) xi "
                           "-> G = FFT/16 bin m (m = 2, no aliasing); G = a + (eps/2) conj(a), a = U y",
            "rows": rows}


# ---------------------------------------------------------------- probes
def snapshot(case):
    snap = {}
    for key in sorted(case):
        v = case[key]
        if isinstance(v, np.ndarray):
            snap[key] = ("ndarray", v.dtype.str, v.shape, v.strides, bool(v.flags.writeable), v.tobytes())
        else:
            snap[key] = (type(v).__name__, repr(v))
    return snap


def run_probe(target, pid, group, cls, why, case, expect=None, etol=None, drop=(), extra=None,
              positional=False):
    before = snapshot(case)
    r = {"id": pid, "group": group, "classification": cls, "rationale": why}
    raw = None
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            raw = target.raw(case, drop=drop, extra=extra, positional=positional)
            r["outcome"] = "returned"
        except NotApplicable as exc:
            r.update(outcome="not_applicable", verdict="NOT_APPLICABLE", note=str(exc))
            return r
        except Exception as exc:
            r.update(outcome="raised", exception=type(exc).__name__, message=str(exc)[:240])
    r["warnings"] = sorted(set("%s: %s" % (w.category.__name__, str(w.message)[:100]) for w in caught))
    r["inputs_unchanged"] = snapshot(case) == before
    value_ok = None
    if r["outcome"] == "returned":
        try:
            db, loads = extract(raw, target.adapter)
            arr = np.asarray(db)
            r["returned_shape"] = list(arr.shape)
            r["returned_dtype"] = str(arr.dtype)
            r["returned_finite"] = bool(np.all(np.isfinite(arr.astype(complex))))
            if expect is not None:
                value_ok, err, why2 = compare(arr, expect, etol)
                r["value_matches_formula"] = value_ok
                if err is not None:
                    r["max_abs_err"] = jnum(err)
        except Exception as exc:
            r["extract_error"] = "%s: %s" % (type(exc).__name__, str(exc)[:200])
            value_ok = False
    if not r["inputs_unchanged"]:
        r["verdict"] = "FAIL"
        r["note"] = "caller input modified"
    elif cls == REJ:
        r["verdict"] = "PASS" if r["outcome"] == "raised" else "FAIL"
    elif cls == ACC:
        good = (r["outcome"] == "returned" and r.get("returned_finite") and
                (expect is None or value_ok))
        r["verdict"] = "PASS" if good else "FAIL"
    else:
        r["verdict"] = "RECORDED"
    return r


def all_probes(target, call_interface):
    out = []
    base = random_case(4001, 6, 3, 2, "general", 2.3)
    n, k = 6, 3
    exp = formula(base)
    tol = 4 * RTOL * coef_bound(base)

    def add(pid, group, cls, why, case, expect=None, etol=None, **kw):
        out.append(run_probe(target, pid, group, cls, why, case, expect, etol, **kw))

    def C(**changes):
        return copy_case(base, **changes)

    add("baseline_valid", "baseline", ACC, "valid synthetic inputs", C(), exp, tol)
    # ---- mode
    for label, mv, cls, why in (("0", 0, REJ, "0453: one retained mode m 1..6"),
                                ("7", 7, REJ, "0453: one retained mode m 1..6"),
                                ("minus1", -1, REJ, "0453: one retained mode m 1..6"),
                                ("True", True, REC, "0453 silent on type; 0439 L183-187 rejects bool"),
                                ("float_1.0", 1.0, REC, "0453 silent on type; 0439 L183-187 rejects float"),
                                ("numpy_int64_3", np.int64(3), REC,
                                 "0453 silent on type; 0439 L183-187 rejects numpy integers")):
        add("m_" + label, "mode", cls, why, C(m=mv), exp if cls != REJ else None, tol)
    for mv in range(1, 7):
        add("m_valid_%d" % mv, "mode", ACC, "0453: m 1..6; the formula contains no m", C(m=mv), exp, tol)
    # ---- measures
    for key, label in (("rho", "rho"), ("volume_weights", "w")):
        v = base[key]
        bad = {}
        for tag, val in (("zero_entry", 0.0), ("negative_entry", -0.5), ("nan_entry", float("nan")),
                         ("inf_entry", float("inf"))):
            a = v.copy()
            a[2] = val
            bad[tag] = a
        why_pos = "0453: real positive density" if key == "rho" else "0453: positive volume_weights"
        for tag, a in bad.items():
            add("%s_%s" % (label, tag), "measure", REJ, why_pos + "; fail on nonfinite", C(**{key: a}))
        add("%s_complex_nonzero_imag" % label, "measure", REJ, why_pos + " (real)", C(**{key: v + 0.25j}))
        add("%s_complex_dtype_zero_imag" % label, "measure", REC,
            "0453 says real; 0439 L62-83 rejects complex dtype for real vectors",
            C(**{key: v.astype(complex)}), exp, tol)
        iv = np.arange(1, n + 1)
        add("%s_integer_dtype" % label, "measure", REC, "0453 silent on dtype; 0439 accepts integer dtype",
            C(**{key: iv}), formula(C(**{key: iv.astype(float)})), 4 * RTOL * coef_bound(C(**{key: iv.astype(float)})))
        bv = np.ones(n, dtype=bool)
        add("%s_bool_dtype" % label, "measure", REC, "0453 silent; 0439 rejects bool dtype",
            C(**{key: bv}), formula(C(**{key: np.ones(n)})), 4 * RTOL * coef_bound(C(**{key: np.ones(n)})))
        add("%s_length_n_plus_1" % label, "measure", REJ, "0453: shape (n,)", C(**{key: np.append(v, 1.0)}))
        add("%s_shape_n_by_1" % label, "measure", REJ, "0453: shape (n,)", C(**{key: v[:, None].copy()}))
    # ---- gradient
    g = base["gradient"]
    for pid, arr, why in (
            ("grad_transposed_3_by_n", g.T.copy(), "0453: gradient (n,3); here n = 6 != 3"),
            ("grad_n_by_2", g[:, :2].copy(), "0453: gradient (n,3)"),
            ("grad_n_by_3_by_1", g[:, :, None].copy(), "0453: gradient (n,3)"),
            ("grad_n_by_4", np.hstack([g, g[:, :1]]), "0453: gradient (n,3)"),
            ("grad_flat_3n", g.reshape(-1).copy(), "0453: gradient (n,3)"),
            ("grad_n_plus_1_rows", np.vstack([g, g[:1]]), "0453: gradient (n,3) with the maps' n"),
            ("grad_16_angles_array", np.repeat(g[None], 16, axis=0),
             "0453: the module does no FFT or angle selection; (16,n,3) is not (n,3)")):
        add(pid, "gradient", REJ, why, C(gradient=arr))
    for pid, idx, val in (("grad_nan_real_part", (3, 1), complex(float("nan"), 0.0)),
                          ("grad_nan_imag_part", (1, 0), complex(1.0, float("nan"))),
                          ("grad_inf", (4, 2), complex(float("inf"), 1.0))):
        a = g.copy()
        a[idx] = val
        add(pid, "gradient", REJ, "0453: fail on nonfinite", C(gradient=a))
    add("grad_real_float64", "gradient", REC,
        "0453 says complex coefficients; a real array is an exact complex value (0439 accepts real f)",
        C(gradient=g.real.copy()), formula(C(gradient=g.real.copy())), tol)
    add("grad_noncontiguous_view", "gradient", ACC, "memory layout must not change the value",
        C(gradient=np.ascontiguousarray(g.T).T), exp, tol)
    sq = random_case(4002, 3, 2, 2, "general", 2.3)
    tol_sq = 4 * RTOL * coef_bound(sq)
    add("grad_square_n3_correct_orientation", "gradient", ACC, "n == 3, correct (n,3) orientation",
        copy_case(sq), formula(sq), tol_sq)
    add("grad_square_n3_transposed", "gradient", REC,
        "n == 3: (3,n) and (n,3) coincide, so orientation cannot be checked by shape",
        copy_case(sq, gradient=sq["gradient"].T.copy()), formula(sq), tol_sq)
    # ---- maps
    add("map_U_phi_k_plus_1", "maps", REJ, "0453: shared (n,k) maps",
        C(U_phi=np.hstack([base["U_phi"], base["U_phi"][:, :1]])))
    add("map_U_z_n_plus_1", "maps", REJ, "0453: shared (n,k) maps",
        C(U_z=np.vstack([base["U_z"], base["U_z"][:1]])))
    add("map_U_R_1d", "maps", REJ, "0453: (n,k) maps", C(U_R=base["U_R"][:, 0].copy()))
    add("map_all_1d", "maps", REJ, "0453: (n,k) maps; a 1-D vector is not (n,k)",
        C(U_R=base["U_R"][:, 0].copy(), U_phi=base["U_phi"][:, 0].copy(), U_z=base["U_z"][:, 0].copy()))
    add("map_U_R_3d", "maps", REJ, "0453: (n,k) maps", C(U_R=base["U_R"][:, :, None].copy()))
    add("map_U_R_transposed_k_by_n", "maps", REJ, "0453: (n,k) maps; here (k,n) with k != n",
        C(U_R=base["U_R"].T.copy()))
    for pid, key, idx, val in (("map_U_phi_nan", "U_phi", (2, 1), complex(float("nan"), 0.0)),
                               ("map_U_z_inf", "U_z", (0, 2), complex(float("inf"), 0.0)),
                               ("map_U_R_nan_imag", "U_R", (5, 0), complex(0.5, float("nan")))):
        a = base[key].copy()
        a[idx] = val
        add(pid, "maps", REJ, "0453: fail on nonfinite", C(**{key: a}))
    root = C(U_R=base["U_R"].real.copy(), U_phi=1j * base["U_phi"].imag, U_z=base["U_z"].real.copy())
    add("map_root_dtypes_real_UR_UZ", "maps", ACC,
        "root's helicity maps: U_R, U_z real float64, U_phi complex128 (0439 interface L50)",
        root, formula(root), 4 * RTOL * coef_bound(root))
    allreal = C(U_R=base["U_R"].real.copy(), U_phi=base["U_phi"].real.copy(), U_z=base["U_z"].real.copy())
    add("map_all_real_float64", "maps", ACC, "real maps are exact complex values",
        allreal, formula(allreal), 4 * RTOL * coef_bound(allreal))
    ints = C(U_R=np.arange(n * k).reshape(n, k) % 5 - 2, U_phi=np.arange(n * k).reshape(n, k) % 3 - 1,
             U_z=np.arange(n * k).reshape(n, k) % 4 - 1)
    ints_f = copy_case(ints, **dict((key, ints[key].astype(float)) for key in MAP_KEYS))
    add("map_integer_dtype", "maps", REC, "0453 silent; 0439 L86-106 accepts integer maps",
        ints, formula(ints_f), 4 * RTOL * coef_bound(ints_f))
    bools = C(U_R=np.ones((n, k), bool), U_phi=np.zeros((n, k), bool), U_z=np.ones((n, k), bool))
    bools_f = copy_case(bools, **dict((key, bools[key].astype(float)) for key in MAP_KEYS))
    add("map_bool_dtype", "maps", REC, "0453 silent; 0439 rejects bool dtype",
        bools, formula(bools_f), 4 * RTOL * coef_bound(bools_f))
    c64 = C(U_R=base["U_R"].astype(np.complex64), U_phi=base["U_phi"].astype(np.complex64),
            U_z=base["U_z"].astype(np.complex64))
    c64_up = copy_case(c64, **dict((key, c64[key].astype(complex)) for key in MAP_KEYS))
    add("map_complex64", "maps", REC, "0453 silent on precision; compared after exact upcast",
        c64, formula(c64_up), 4 * RTOL * coef_bound(c64_up))
    add("map_fortran_order", "maps", ACC, "memory layout must not change the value",
        C(U_R=np.asfortranarray(base["U_R"]), U_phi=np.asfortranarray(base["U_phi"]),
          U_z=np.asfortranarray(base["U_z"])), exp, tol)
    wide = {}
    for key in MAP_KEYS:
        wa = np.zeros((n, 2 * k), dtype=complex)
        wa[:, ::2] = base[key]
        wide[key] = wa[:, ::2]
    add("map_strided_views", "maps", ACC, "memory layout must not change the value", C(**wide), exp, tol)
    add("map_k_zero", "maps", REC, "k = 0 is degenerate; 0453 silent (0439 requires k >= 1)",
        C(U_R=np.zeros((n, 0), complex), U_phi=np.zeros((n, 0), complex), U_z=np.zeros((n, 0), complex)))
    empty = {"m": 2, "U_R": np.zeros((0, 3), complex), "U_phi": np.zeros((0, 3), complex),
             "U_z": np.zeros((0, 3), complex), "rho": np.zeros(0), "volume_weights": np.zeros(0),
             "gradient": np.zeros((0, 3), complex), "normalization_scale": 2.3, "R": np.zeros(0)}
    add("n_zero_points", "maps", REC, "n = 0 is degenerate; 0453 silent (0439 requires n >= 1)", empty)
    # ---- normalization
    for label, sv, cls, why, e in (
            ("zero", 0.0, REJ, "0453: explicit positive normalization_scale", None),
            ("negative", -2.3, REJ, "0453: explicit positive normalization_scale", None),
            ("nan", float("nan"), REJ, "0453: positive; fail on nonfinite", None),
            ("inf", float("inf"), REJ, "0453: fail on nonfinite", None),
            ("minus_inf", float("-inf"), REJ, "0453: positive; fail on nonfinite", None),
            ("string", "2.3", REJ, "a string is not a positive number", None),
            ("bool_True", True, REC, "0453 silent on type; 0439 L109-121 rejects bool", 1.0),
            ("int_2", 2, REC, "0453 silent on type; 0439 accepts numbers.Real ints", 2.0),
            ("numpy_float64", np.float64(2.3), REC, "0453 silent on type", 2.3),
            ("complex_zero_imag", 2.3 + 0j, REC, "0453: positive number; 0439 rejects non-Real", 2.3),
            ("zero_dim_array", np.array(2.3), REC, "0453 silent on type; 0439 rejects arrays", 2.3)):
        expect = None if e is None else formula(C(normalization_scale=e))
        add("s_" + label, "normalization", cls, why, C(normalization_scale=sv), expect, tol)
    # ---- call interface
    if call_interface:
        add("arg_missing_normalization_scale", "arguments", REJ, "a required 0453 input is missing", C(),
            drop=("normalization_scale",))
        add("arg_missing_gradient", "arguments", REJ, "a required 0453 input is missing", C(),
            drop=("gradient",))
        add("arg_missing_m", "arguments", REJ, "0453 lists the retained mode m as an input", C(),
            drop=("m",))
        add("arg_unknown_keyword", "arguments", REC, "0453 silent; 0439 raises TypeError", C(), exp, tol,
            extra={"w1_unknown_keyword": 1})
        add("arg_all_positional", "arguments", REC, "0453 silent; 0439 is keyword-only", C(), exp, tol,
            positional=True)
    # ---- overflow / non-finite results
    w1, r1 = base["volume_weights"].copy(), base["rho"].copy()
    w1[1], r1[1] = 1e200, 1e200
    add("overflow_w_rho_product", "overflow", REJ, "0453 fail on nonfinite: w*rho = inf at a point",
        C(volume_weights=w1, rho=r1))
    U1, g1 = base["U_R"].copy(), g.copy()
    U1[0, 0], g1[0, 0] = 1e200, 1e200
    add("overflow_map_times_load", "overflow", REJ, "0453 fail on nonfinite: conj(U)*w*rho*g overflows",
        C(U_R=U1, gradient=g1))
    so = C()
    so["volume_weights"][:2], so["rho"][:2] = 1.0, 1.0
    so["gradient"][:2, 0] = 1.5e308
    so["U_R"][:2, :] = 0.0
    so["U_R"][:2, 0] = 1.0
    add("overflow_in_sum", "overflow", REJ, "0453 fail on nonfinite: two finite terms sum to inf", so)
    zr = C()
    zr["volume_weights"][2], zr["rho"][2] = 1e200, 1e200
    for key in MAP_KEYS:
        zr[key][2, :] = 0.0
    add("overflow_operand_at_zero_map_rows", "overflow", REJ,
        "0453 = 0439 b slice, which fails closed on a non-finite operand (0439 L316-318); "
        "here w*rho*g = inf at a point whose map rows are exactly 0", zr)
    add("overflow_tiny_normalization", "overflow", REJ, "0453 fail on nonfinite: sum / 5e-324 overflows",
        C(normalization_scale=5e-324))
    # ---- purity: read-only inputs, aliasing, fresh buffers
    ro = C()
    for key, val in ro.items():
        if isinstance(val, np.ndarray):
            val.setflags(write=False)
    add("readonly_inputs", "purity", ACC, "0454 no caller mutation: a pure function accepts read-only arrays",
        ro, exp, tol)
    out.extend(purity_records(target, base))
    return out


def purity_records(target, base):
    out = []
    case = copy_case(base)
    before = snapshot(case)
    try:
        raw1 = target.raw(case)
        db1, loads1 = extract(raw1, target.adapter)
        raw2 = target.raw(case)
        db2, loads2 = extract(raw2, target.adapter)
    except Exception as exc:
        return [{"id": "purity_calls", "group": "purity", "classification": ACC, "verdict": "FAIL",
                 "note": "exception %s: %s" % (type(exc).__name__, str(exc)[:200])}]
    outs = [("delta_b", np.asarray(db1))]
    if loads1:
        outs += [("load_" + c, np.asarray(v)) for c, v in sorted(loads1.items())]
    if isinstance(raw1, dict):
        outs += [(key, v) for key, v in sorted(raw1.items(), key=lambda kv: str(kv[0]))
                 if isinstance(v, np.ndarray) and not any(v is o for _, o in outs)]
    ins = [(key, v) for key, v in case.items() if isinstance(v, np.ndarray)]
    alias_in = sorted("%s~%s" % (on, iname) for on, o in outs for iname, i in ins if np.shares_memory(o, i))
    alias_internal = sorted("%s~%s" % (outs[a][0], outs[b][0]) for a in range(len(outs))
                            for b in range(a + 1, len(outs)) if np.shares_memory(outs[a][1], outs[b][1]))
    out.append({"id": "alias_outputs_vs_inputs", "group": "purity", "classification": "expected_none",
                "rationale": "0454 no caller mutation: a returned array sharing caller memory would expose it",
                "aliases": alias_in, "verdict": "PASS" if not alias_in else "FAIL"})
    out.append({"id": "alias_outputs_internal", "group": "purity", "classification": REC,
                "rationale": "returned arrays sharing memory with each other", "aliases": alias_internal,
                "verdict": "RECORDED"})
    a1, a2 = np.asarray(db1), np.asarray(db2)
    same = a1.tobytes() == a2.tobytes()
    shared = bool(np.shares_memory(a1, a2))
    saved = a2.copy()
    mutated_ok = None
    if a1.flags.writeable:
        a1[...] = 0
        mutated_ok = a2.tobytes() == saved.tobytes()
    unchanged = snapshot(case) == before
    out.append({"id": "fresh_buffers_two_calls", "group": "purity", "classification": "expected_fresh",
                "rationale": "no cached or shared output buffer between calls; caller inputs untouched",
                "bitwise_identical_repeat": same, "delta_b_buffers_shared": shared,
                "second_unchanged_after_zeroing_first": mutated_ok, "inputs_unchanged": unchanged,
                "returned_dtype": str(a2.dtype), "returned_shape": list(a2.shape),
                "returned_keys": sorted(map(str, raw1)) if isinstance(raw1, dict) else None,
                "verdict": "PASS" if (same and not shared and mutated_ok is not False and unchanged)
                else "FAIL"})
    out.append({"id": "output_shape_k", "group": "purity", "classification": "expected_shape",
                "rationale": "0453: increment with the input dimension k", "returned_shape": list(a2.shape),
                "verdict": "PASS" if a2.shape == (base["U_R"].shape[1],) else "FAIL"})
    return out


# --------------------------------------------------------- mutation study
VALUE_FAMILIES = ("hand", "proj_direct", "proj_coeff_consistency", "vw_random", "vw_reconstruct",
                  "ident", "comp", "loads")


def value_checks(target, pcs):
    checks = family_hand(target)
    checks += family_projection_and_virtual_work(target, pcs)
    checks += family_identities(target)
    checks += family_components(target)
    checks += family_loads(target)
    return checks


def mutation_study(ref_module, pcs):
    rows = []
    for name in [""] + list(ref_module.MUTATIONS):
        tgt = Target(DirectCaller(ref_module.make_mutant(name), pass_R=True))
        checks = value_checks(tgt, pcs)
        failed = [c for c in checks if not c["passed"]]
        fams = sorted(set(c["family"] for c in failed))
        rows.append({"mutation": name or "none (unmutated reference kernel)",
                     "detected": bool(failed), "failed_checks": len(failed), "checks": len(checks),
                     "families_detecting": fams,
                     "detected_by_real_virtual_work": any(f in fams for f in ("vw_random", "vw_reconstruct")),
                     "detected_by_direct_projection": "proj_direct" in fams,
                     "detected_by_hand_cases": "hand" in fams,
                     "proj_direct_cases_detecting": sorted(c["id"][len("proj_direct_"):] for c in failed
                                                           if c["family"] == "proj_direct"),
                     "vw_cases_detecting": sorted(set(c["id"].split("_", 2)[2] for c in failed
                                                      if c["family"] in ("vw_random", "vw_reconstruct"))),
                     "hand_cases_detecting": sorted(c["id"][len("hand_"):] for c in failed
                                                    if c["family"] == "hand"),
                     "first_failed": [c["id"] for c in failed[:5]]})
    return rows


# --------------------------------------------------------------------- main
def env_info():
    return {"python": sys.version.split()[0], "executable": sys.executable, "numpy": np.__version__,
            "platform": platform.platform(), "isolated_flag": sys.flags.isolated,
            "dont_write_bytecode": sys.dont_write_bytecode,
            "thread_env": dict((key, os.environ.get(key)) for key in
                               ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"))}


def write_json(path, obj):
    with open(path, "w") as fh:
        json.dump(sanitize(obj), fh, indent=1, allow_nan=False)
        fh.write("\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description="W1 fixtures for 0454 (review of the 0453 induced-field load)")
    ap.add_argument("--module", required=True, help="target module file path")
    ap.add_argument("--func", required=True, help="target function name")
    ap.add_argument("--adapter-module", help="adapter module path (call(func, canonical), extract(raw))")
    ap.add_argument("--reference", default=DEFAULT_REFERENCE, help="W1 loop reference path")
    ap.add_argument("--ref0439", help="frozen 0439 kernel path for the b cross-check (SHA-256 verified)")
    ap.add_argument("--mutation-study", action="store_true", help="run the mutants of the W1 reference")
    ap.add_argument("--out", required=True, help="output JSON path")
    args = ap.parse_args(argv)

    module_path = os.path.abspath(args.module)
    module_dir = os.path.dirname(module_path)
    result = {"schema": HARNESS_VERSION,
              "run_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
              "dispatch_0454_sha256": DISPATCH_0454_SHA256, "spec_0453_sha256": SPEC_0453_SHA256,
              "harness": {"path": os.path.abspath(__file__), "sha256": sha256_file(os.path.abspath(__file__))},
              "argv": sys.argv[1:] if argv is None else list(argv),
              "environment": env_info(),
              "tolerances": {"RTOL_vs_absolute_value_bound": RTOL, "hand_cases": "exact (0.0)",
                             "fd_selfcheck_rel": FD_RTOL, "fd_step": FD_STEP, "angles": NANG}}
    target_info = {"module_path": module_path, "func": args.func,
                   "module_sha256_before": sha256_file(module_path),
                   "dir_listing_before": sorted(os.listdir(module_dir))}
    result["target"] = target_info
    module = load_module(module_path, "target")
    func = getattr(module, args.func)
    adapter = None
    if args.adapter_module:
        adapter = load_module(args.adapter_module, "adapter")
        caller = AdapterCaller(func, adapter)
        target_info["adapter"] = {"path": os.path.abspath(args.adapter_module),
                                  "sha256": sha256_file(os.path.abspath(args.adapter_module))}
        call_interface = False
    else:
        try:
            sig, mapping, problems, deviations, kinds = resolve_signature(func)
        except AdapterRequired as exc:
            sig, mapping, problems, deviations, kinds = None, {}, [str(exc)], [], []
        target_info.update(signature=str(sig) if sig is not None else None, mapping=mapping,
                           deviations=deviations, parameter_kinds=kinds)
        if problems:
            result["status"] = "adapter_required"
            result["adapter_description"] = adapter_description(problems)
            write_json(args.out, result)
            return 3
        caller = MappedCaller(func, sig, mapping)
        call_interface = True
    target = Target(caller, adapter)
    smoke = random_case(4001, 6, 3, 2, "general", 2.3)
    try:
        extract(caller.call_raw(copy_case(smoke)), adapter)
        target_info["smoke_call"] = "ok"
    except AdapterRequired as exc:
        result["status"] = "adapter_required"
        result["adapter_description"] = adapter_description(["return value: %s" % exc])
        write_json(args.out, result)
        return 3
    except Exception as exc:
        target_info["smoke_call"] = "exception %s: %s" % (type(exc).__name__, str(exc)[:200])

    pcs = [build_potential_case(spec) for spec in PROJ_CASES]
    selfchecks = family_selfcheck(pcs)
    checks = value_checks(target, pcs)
    checks += family_formula(target, pcs)
    ref_module = None
    if args.reference and os.path.exists(args.reference):
        ref_path = os.path.abspath(args.reference)
        ref_module = load_module(ref_path, "reference")
        result["reference"] = {"path": ref_path, "sha256": sha256_file(ref_path),
                               "version": getattr(ref_module, "REFERENCE_VERSION", None)}
        is_self = ref_path == module_path and args.func == "induced_field_weak_load_reference"
        checks += family_reference(target, ref_module.induced_field_weak_load_reference, pcs, is_self)
    if args.ref0439:
        p0439 = os.path.abspath(args.ref0439)
        h0439 = sha256_file(p0439)
        result["ref0439"] = {"path": p0439, "sha256": h0439, "pinned": PINNED_0439_SHA256,
                             "sha_matches_pin": h0439 == PINNED_0439_SHA256}
        if h0439 == PINNED_0439_SHA256:
            mod0439 = load_module(p0439, "frozen0439")
            checks += family_x0439(target, mod0439, pcs)
            result["ref0439"]["sha256_after"] = sha256_file(p0439)
    probes = all_probes(target, call_interface)
    result["caveat_real_linear_chain"] = caveat_illustration(target)
    if args.mutation_study:
        if ref_module is None:
            result["mutation_study"] = "skipped: reference module unavailable"
        else:
            result["mutation_study"] = mutation_study(ref_module, pcs)
    target_info["module_sha256_after"] = sha256_file(module_path)
    target_info["dir_listing_after"] = sorted(os.listdir(module_dir))
    target_info["module_unchanged"] = target_info["module_sha256_after"] == target_info["module_sha256_before"]
    target_info["no_new_files_in_module_dir"] = target_info["dir_listing_after"] == target_info["dir_listing_before"]

    failed = [c["id"] for c in checks if not c["passed"]]
    self_failed = [c["id"] for c in selfchecks if not c["passed"]]
    probe_fail = [p["id"] for p in probes if p.get("verdict") == "FAIL"]
    mut = result.get("mutation_study")
    undetected = ([r["mutation"] for r in mut if not r["detected"] and not r["mutation"].startswith("none")]
                  if isinstance(mut, list) else None)
    false_positive = ([r["mutation"] for r in mut if r["detected"] and r["mutation"].startswith("none")]
                      if isinstance(mut, list) else None)
    result["fixture_selfchecks"] = selfchecks
    result["checks"] = checks
    result["probes"] = probes
    overall_ok = (not failed and not self_failed and not probe_fail and target_info["module_unchanged"]
                  and not undetected and not false_positive)
    result["summary"] = {
        "checks_total": len(checks), "checks_passed": len(checks) - len(failed),
        "checks_failed": len(failed), "failed_check_ids": failed,
        "fixture_selfchecks_total": len(selfchecks), "fixture_selfchecks_failed": self_failed,
        "probes_total": len(probes),
        "probes_pass": sum(1 for p in probes if p.get("verdict") == "PASS"),
        "probes_fail": len(probe_fail), "failed_probe_ids": probe_fail,
        "probes_recorded": sum(1 for p in probes if p.get("verdict") == "RECORDED"),
        "probes_not_applicable": sum(1 for p in probes if p.get("verdict") == "NOT_APPLICABLE"),
        "mutations_total": (len(mut) - 1) if isinstance(mut, list) else None,
        "mutations_detected": (sum(1 for r in mut if r["detected"]) - len(false_positive or []))
        if isinstance(mut, list) else None,
        "mutations_undetected": undetected, "mutation_false_positive_on_unmutated": false_positive,
        "overall": "PASS" if overall_ok else "FAIL"}
    result["status"] = "complete"
    write_json(args.out, result)
    return 0 if overall_ok else 1


def adapter_description(problems):
    return {
        "problems": problems,
        "canonical_inputs": {
            "m": "retained mode, int 1..6", "U_R": "(n,k) map", "U_phi": "(n,k) map", "U_z": "(n,k) map",
            "rho": "(n,) real > 0", "volume_weights": "(n,) real > 0, R dR dz without 2 pi",
            "gradient": "(n,3) complex mode-m coefficients (grad_R, grad_phi=(1/R)d_phi, grad_z), FFT/16",
            "normalization_scale": "finite > 0", "R": "(n,) radius, fixture context only (not a 0453 input)"},
        "adapter_protocol": "module with call(func, canonical) -> raw and optional extract(raw) -> "
                            "{'delta_b': (k,), 'load_R', 'load_phi', 'load_z'}; pass --adapter-module PATH",
        "next_step": "stop for the lead: write the adapter (or confirm the mapping) and rerun"}


if __name__ == "__main__":
    sys.exit(main())

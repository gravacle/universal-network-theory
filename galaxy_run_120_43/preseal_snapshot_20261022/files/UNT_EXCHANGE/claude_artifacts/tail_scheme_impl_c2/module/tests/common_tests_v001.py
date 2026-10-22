"""Shared helpers for the module-lane unit tests (tail_scheme_impl_c2/module/tests). Writes only module/out/."""
import hashlib
import importlib.util
import json
import math
import os
import sys
from pathlib import Path
import numpy as np

MODULE = Path(__file__).resolve().parent.parent
OUT = MODULE / 'out'
sys.path.insert(0, str(MODULE))
import owned_uv_tail_lapse_v001 as UVT  # noqa: E402
import uv_tail_source_roster_c2v001 as RS  # noqa: E402
import posix_libm_bessel_jn_provider_c2v001 as PV  # noqa: E402

ROOT = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13')
RUNS = ROOT / 'CLAUDE2/runs'
HR = ROOT / 'helpers/recovered_packet_audit'
C1 = ROOT / 'CODEX1'
PROFILE = C1 / 'GALAXY_RADIAL_SOURCE_REFERENCE_V001.json'
PROFILE_SHA = 'f5becd4586264ef156b021812d440e884f518c61dc9953e41a4fb1494218c60b'
PREREG_V005 = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/KMAX_MATRIX_PREREG_V005.json')
PREREG_V005_SHA = 'dbddc02c4d793b44a12136fc4fc88b20c001865ddd4c89b1b70c57bc406bb174'
KPC = UVT.KPC_M
CL = 299792458.0
THREAD_ENV = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS')


def require_env():
    bad = [k for k in THREAD_ENV if os.environ.get(k) != '1']
    if bad:
        raise SystemExit('single-thread BLAS env required: ' + ','.join(bad))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_json_pinned(path, sha256):
    if sha(path) != sha256:
        raise SystemExit('pin mismatch ' + str(path))
    return json.loads(Path(path).read_text())


def load_module(path, name, sha256=None):
    if sha256 is not None and sha(path) != sha256:
        raise SystemExit('module pin mismatch ' + str(path))
    spec = importlib.util.spec_from_file_location('uvt_test_' + name, str(path))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


DRAFT = Path('/private/tmp/claude-501/-Users-bgm-MB-Work/04dac55c-b963-46a5-9ea4-74afb63af51b/scratchpad/draft_out')


def write_json(name, obj):
    base = DRAFT if os.environ.get('UVT_TEST_DRAFT') == '1' else OUT
    tag = os.environ.get('UVT_RUN_TAG')
    if tag:
        if not (tag.startswith('V') and tag[1:].isdigit()) or not name.endswith('_V001.json'):
            raise SystemExit('bad run tag')
        name = name[:-len('_V001.json')] + '_%s.json' % tag
    base.mkdir(parents=True, exist_ok=True) if base is DRAFT else None
    p = base / name
    if base is DRAFT and p.exists():
        p.unlink()
    if not str(p.resolve()).startswith(str(base.resolve())):
        raise SystemExit('write outside module/out refused')
    with p.open('x') as fh:
        json.dump(obj, fh, indent=1, allow_nan=False, default=lambda o: o.tolist() if hasattr(o, 'tolist') else float(o))
        fh.write('\n')
    return p


def config(*, outer, K_big=None, K_out=None, w_perp, w_z, order=8, R_eval, z_eval, z_src, M_s=64, lam=1.0):
    o = {'shape': 'cylinder', 'K_big_inverse_kpc': K_big} if outer == 'cylinder' else {'shape': 'cube', 'K_out_inverse_kpc': K_out}
    return UVT.normalize_config({
        'enabled': True, 'outer': o, 'source_rule': 'continuum_v001', 'gas': {'interp': 'lagrange3_s_gl4', 'M_s': M_s},
        'stars': {'segment_rule': 'max16_ceil_kdr_plus8', 'tail_rule': 't_panels_40a_phase1p5_gl12'},
        'quadrature': {'order': order, 'w_perp_max_inverse_kpc': w_perp, 'w_z_max_inverse_kpc': w_z},
        'domain': {'R_eval_max_kpc': R_eval, 'z_eval_max_kpc': z_eval, 'z_src_max_kpc': z_src},
        'asymptote': 'EH_exact_minus_quarter', 'lapse_only': True,
        'jet_order': {'route_a': 1, 'route_b': 2, 'ngc_eval': 1}, 'lambda_scale': lam,
        'eps_certificate': UVT.TEST_ONLY_CERT, 'lo_certificate': UVT.TEST_ONLY_CERT})


class GaussianRoster:
    """Synthetic separable source S = exp(-(kp^2 a^2 + kz^2 b^2)/2) (the prototype's unit-mass Gaussian disc)."""
    kind = 'synthetic'

    def __init__(self, a_kpc, b_kpc):
        self.a = a_kpc * KPC; self.b = b_kpc * KPC; self.stars = None; self.gas = None

    def radial_factors(self, kp, j0):
        kp = np.asarray(kp, float); return np.exp(-0.5 * (kp * self.a) ** 2)[:, None]

    def vertical_factors(self, kz, c):
        kz = np.asarray(kz, float); return np.exp(-0.5 * (kz * self.b) ** 2)[:, None].astype(complex)

    def factors(self, kp, kz, c, j0):
        return self.radial_factors(kp, j0), self.vertical_factors(kz, c)

    def extent(self):
        return dict(R_src_max_m=8 * self.a, stars_24h_m=8 * self.b, gas_z_abs_max_m=0.0)

    def record(self):
        return dict(kind='synthetic_gaussian', a_m=self.a, b_m=self.b)

    def digest(self):
        return hashlib.sha256(json.dumps(self.record(), sort_keys=True).encode()).hexdigest()


def tau_v005():
    d = load_json_pinned(PREREG_V005, PREREG_V005_SHA)
    return np.array(d['tau_km_s'], float)


def profile():
    return load_json_pinned(PROFILE, PROFILE_SHA)


SYNTH_I1T = {'verdict': 'NOT_APPLICABLE_SYNTHETIC', 'scope': 'synthetic analytic source; no packet exists'}

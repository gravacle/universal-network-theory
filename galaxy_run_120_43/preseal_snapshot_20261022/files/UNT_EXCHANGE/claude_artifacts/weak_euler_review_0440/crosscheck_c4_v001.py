import sys; sys.dont_write_bytecode=True; sys.path.append('/Users/bgm/Library/Python/3.9/lib/python/site-packages'); import numpy as np
# ---------------------------------------------------------------------------------------------
# crosscheck_c4_v001.py -- Claude4 review lane (dispatch 0440, amended by 0441), local helper
# "C4X": adversarial cross-checker of helper H1 (algebra oracle) and helper H2 (loop reference
# and fixture harness).  REVIEW FIXTURE ONLY.  Makes no physics decision.
#
# * Small synthetic arrays only (npoints <= 16, nfree <= 5); numpy only; prints to stdout;
#   WRITES NO FILES (H2 harness functions are called with out_json=None).
# * Review-lane files are loaded BY PATH with importlib (sys.dont_write_bytecode=True).
# * No project module is imported or executed.  No project data, galaxy data, calibration or
#   target velocity or validation outcome is opened.  The pinned contract JSON is read for its
#   hash and equation text.  The pinned prior v002 file is read for its hash and the exact text of
#   nine lines (it is never imported or executed); the helicity file and 0438 are only hashed.
# * Claude3's implementation is NOT inspected or run here.
#
# Run:  /usr/bin/python3 -I -B /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/weak_euler_review_0440/crosscheck_c4_v001.py
#
# Sections
#  [0]  input hashes (pins and the H1/H2 files under review)
#  [1]  contract equation text; mechanical "contract-literal" evaluator built from that text
#  [2]  random complex cases: H1 oracle vs H2 reference vs contract-literal vs C4 transcription
#  [2b] exact rational (Fraction) evaluation of the contract chain vs every float route
#  [3]  root-structured cases (real U_R/U_z, imaginary U_phi, real-valued divU/G)
#  [4]  H2 hand case (npoints = nfree = 1), against C4's own hand derivation
#  [5]  pointwise inertial matrix M_p extracted from the contract chain vs C4 hand form vs H1
#  [6]  H1 section 1i: pressure/density restructuring and Hermiticity on a consistent background
#  [7]  independent 3-D Cartesian finite-difference check of delta v and delta a
#  [8]  Gauss-Legendre check of the weak pressure term (phi-component conjugation)
#  [9]  prior v002 L44-L58: exact line text present; hand-copied expressions vs contract
#  [10] H2 harness re-run in memory (reference self-check and mutation study), byte comparison
#       with H2's saved JSON files
#  [10b] H2's unsaved F6 demonstration (non-validating control through F6), re-run in memory
#  [11] C4 control transcriptions and C4-only mutants through H2 run_all (F0-F5)
# Sizes: assembly fixtures npoints <= 16, nfree <= 5; the GL check uses 8x8 = 64 nodes.
# ---------------------------------------------------------------------------------------------
import hashlib
import importlib.util
import json
import math
import re
import time

DIR = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/weak_euler_review_0440/'
CTRL = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/'
CONTRACT_PATH = CTRL + 'CODEX1/ADDITIONAL_CLAUDE_WEAK_EULER_TASKS_V001.json'
V002_PATH = CTRL + 'helpers/coefficient_method/owned_nonzero_modal_weak_adjustment_v002.py'
HELI_PATH = CTRL + 'helpers/coefficient_method/owned_32q8_regular_helicity_maps_v001.py'
D0438_PATH = '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0438_2026-10-16_claude_free_surface_density_projection.md'
H1_ORACLE = DIR + 'algebra_oracle_h1v001.py'
H1_NOTE = DIR + 'ALGEBRA_SIGN_H1_V001.md'
H1_CHECK = DIR + 'check_h1_oracle_v001.py'
H2_REF = DIR + 'reference_weak_euler_h2v001.py'
H2_HARNESS = DIR + 'fixtures_weak_euler_h2v001.py'
H2_REF_JSON = DIR + 'fixture_results_h2v001_reference.json'
H2_MUT_JSON = DIR + 'fixture_results_h2v001_mutations.json'
H2_NOTE = DIR + 'FIXTURES_H2_V001.md'

EXPECTED_SHA = (
    ('contract (pinned)', CONTRACT_PATH, '5c30449de636b1f3da751d07ad90caafe964ed19444b0648df8fd9726ade9ebe'),
    ('prior v002 (pinned)', V002_PATH, '5cae4ee994f1ca07fdf703af529e7f5df9df2c2ed642d478df89beb692a25c51'),
    ('helicity maps (pinned)', HELI_PATH, '280149dc028260d865604948633bb8a1332c5ee01be916895c02df42e2b280c6'),
    ('dispatch 0438 (observed, no pin)', D0438_PATH, '83c963759f875285ce0b33148de1684318cbb81aa4658e1128bede3fe76a5c4c'),
    ('H1 oracle', H1_ORACLE, '29fc7fd429c921c4e6e7c04a624ce4db6ffcb0b32a8c0f5a432413ce73feb23e'),
    ('H1 note', H1_NOTE, 'b42bab82c1ab510e2c74a498fdfe944c35f21a56cb4da25fc8274ad5bb90251e'),
    ('H1 check script', H1_CHECK, 'ae5238153a1efe6dd1354488620d3d8d07713f3e77dd2255350d5621ae78d53a'),
    ('H2 reference', H2_REF, '61f1982cbb48a25e1bd1a50afa13c217eb0b77bb905e7db5b19511c714b2a4ac'),
    ('H2 harness', H2_HARNESS, 'a958ecb83279bb4fa069786d0741c13e6ba757a39b6e85e5efe1a86567f8cda7'),
    ('H2 reference JSON', H2_REF_JSON, '296fd463ded48dc62f5b425d58e3fde52cc2e12a823f8e1dcfbae9a900d0d51d'),
    ('H2 mutations JSON', H2_MUT_JSON, '74261329bd8879704f1b5f7ad7c50d00f1db7568bf19335f0eb035fd854cff99'),
    ('H2 note', H2_NOTE, 'a9f2ce2bfa64132667800e0492203f6c83c61eaebc4cf879d7aa0e744f2a4463'),
)

GAMMA = 5.0 / 3.0
CANON = ('R', 'rho', 'P', 'K_R', 'K_z', 'P_R', 'P_z', 'Omega', 'Omega_R', 'Omega_z',
         'volume_weights', 'U_R', 'U_phi', 'U_z', 'divU', 'G', 'f_R', 'f_phi', 'f_z',
         'm', 'gamma', 'normalization_scale', 'provenance')
ARRAYS = CANON[:19]
OUTS = ('A', 'b', 'E', 'PM', 'VR', 'VP', 'VZ')
RESULT = {}


def sha256_file(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def load_by_path(name, path):
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def rel(x, y):
    """max|x-y| / max|y| (max-abs relative); inf on shape mismatch."""
    x = np.asarray(x)
    y = np.asarray(y)
    if x.shape != y.shape:
        return float('inf')
    if x.size == 0:
        return 0.0
    d = float(np.max(np.abs(x - y)))
    s = float(np.max(np.abs(y)))
    return d / s if s > 0 else d


def frob(x, y):
    x = np.asarray(x)
    y = np.asarray(y)
    if x.shape != y.shape:
        return float('inf')
    s = float(np.linalg.norm(y))
    d = float(np.linalg.norm(x - y))
    return d / s if s > 0 else d


def form(X, d, Y):
    """X^H diag(d) Y as sum_p conj(X[p,k]) d[p] Y[p,j] (C4 einsum; no diagonal matrix)."""
    return np.einsum('pk,p,pj->kj', np.conj(np.asarray(X)), np.asarray(d), np.asarray(Y))


def vform(X, v):
    return np.einsum('pk,p->k', np.conj(np.asarray(X)), np.asarray(v))


def antiherm(A):
    A = np.asarray(A)
    return float(np.linalg.norm(A - A.conj().T)) / float(np.linalg.norm(A))


# ------------------------------------------------------------------------------- [1] contract text
C4_TYPED_EQUATIONS = [
    'E=-K_R[:,None]*U_R-K_z[:,None]*U_z',
    'PM=(gamma*P/rho)[:,None]*G+rho[:,None]**gamma*E',
    'VR=i*m*Omega[:,None]*U_R',
    'VP=-(R*Omega_R)[:,None]*U_R+i*m*Omega[:,None]*U_phi-(R*Omega_z)[:,None]*U_z',
    'VZ=i*m*Omega[:,None]*U_z',
    'AR=i*m*Omega[:,None]*VR-2*Omega[:,None]*VP',
    'AP=i*m*Omega[:,None]*VP+(2*Omega+R*Omega_R)[:,None]*VR+(R*Omega_z)[:,None]*VZ',
    'AZ=i*m*Omega[:,None]*VZ',
    ('A=U_R^H diag(volume_weights*rho) AR + U_phi^H diag(volume_weights*rho) AP + U_z^H '
     'diag(volume_weights*rho) AZ - divU^H diag(volume_weights) PM - [U_R^H '
     'diag(volume_weights*P_R/rho)+U_z^H diag(volume_weights*P_z/rho)] G'),
    'b=-U_R^H(volume_weights*rho*f_R)-U_phi^H(volume_weights*rho*f_phi)-U_z^H(volume_weights*rho*f_z)',
]


def contract_equations():
    with open(CONTRACT_PATH, 'r', encoding='utf-8') as fh:
        c = json.load(fh)
    raw = c['author_task']['equations']
    n_unicode_minus = sum(e.count('−') for e in raw)
    return [e.replace('−', '-') for e in raw], n_unicode_minus


def translate(eq):
    """Mechanical translation of the contract's weak-form notation (eqs 9 and 10 only, the ones
    containing '^H') into numpy expressions:
    X^H -> H(X);  ' diag(' -> '@D(';  ') NAME' -> ')@NAME';  '] NAME' -> ']@NAME';
    brackets -> parentheses;  'H(X)(' -> 'H(X)@('.  Eqs 1-8 are already numpy text and are
    evaluated verbatim (their '[:,None]' is left untouched)."""
    lhs, rhs = eq.split('=', 1)
    if '^H' in rhs:
        s = re.sub(r'(\w+)\^H', r'H(\1)', rhs)
        s = s.replace(' diag(', '@D(')
        s = re.sub(r'\) (\w)', r')@\1', s)
        s = re.sub(r'\] (\w)', r']@\1', s)
        s = s.replace('[', '(').replace(']', ')')
        s = re.sub(r'H\((\w+)\)\(', r'H(\1)@(', s)
        rhs = s
    return lhs.strip(), rhs


EXPECTED_TRANSLATION = {
    'A': ('H(U_R)@D(volume_weights*rho)@AR + H(U_phi)@D(volume_weights*rho)@AP + '
          'H(U_z)@D(volume_weights*rho)@AZ - H(divU)@D(volume_weights)@PM - '
          '(H(U_R)@D(volume_weights*P_R/rho)+H(U_z)@D(volume_weights*P_z/rho))@G'),
    'b': '-H(U_R)@(volume_weights*rho*f_R)-H(U_phi)@(volume_weights*rho*f_phi)-H(U_z)@(volume_weights*rho*f_z)',
}


def build_literal(eqs):
    compiled = []
    for e in eqs[:10]:
        lhs, rhs = translate(e)
        compiled.append((lhs, rhs, compile(rhs, '<contract:%s>' % lhs, 'eval')))
    return compiled


def literal_assemble(compiled, kw):
    """Evaluate the pinned equation text itself (dense np.diag for the contract's diag(...);
    acceptable for these tiny review fixtures only)."""
    ns = {'i': 1j, 'H': lambda X: np.asarray(X).conj().T, 'D': np.diag}
    for k in ARRAYS:
        ns[k] = np.asarray(kw[k])
    ns['m'] = kw['m']
    ns['gamma'] = kw['gamma']
    out = {}
    for lhs, _rhs, code in compiled:
        val = eval(code, {'__builtins__': {}}, ns)
        ns[lhs] = val
        out[lhs] = val
    s = kw['normalization_scale']
    res = dict((k, out[k]) for k in ('E', 'PM', 'VR', 'VP', 'VZ', 'AR', 'AP', 'AZ'))
    res['A_unscaled'] = out['A']
    res['b_unscaled'] = out['b']
    res['A'] = out['A'] / s
    res['b'] = out['b'] / s
    return res


# ------------------------------------------------------------------------------- C4 transcription
def c4_core(kw, mut=None):
    """C4's own hand-typed vectorized transcription (einsum contractions, test-side conj only).
    mut selects one deliberate defect (used only in section [11])."""
    R, rho, P = (np.asarray(kw[k], dtype=float) for k in ('R', 'rho', 'P'))
    KR, KZ, PR, PZ = (np.asarray(kw[k], dtype=float) for k in ('K_R', 'K_z', 'P_R', 'P_z'))
    Om, OmR, OmZ = (np.asarray(kw[k], dtype=float) for k in ('Omega', 'Omega_R', 'Omega_z'))
    w = np.asarray(kw['volume_weights'], dtype=float)
    UR, UP, UZ, DU, G = (np.asarray(kw[k], dtype=complex) for k in ('U_R', 'U_phi', 'U_z', 'divU', 'G'))
    fR, fP, fZ = (np.asarray(kw[k], dtype=complex) for k in ('f_R', 'f_phi', 'f_z'))
    m = kw['m']
    g = kw['gamma']
    ns = kw['normalization_scale']
    im = 1j * m
    c = lambda v: v[:, None]  # noqa: E731  point vector -> column broadcast over trial columns
    if mut == 'G_conjugated':
        G = G.conj()
    if mut == 'K_z_paired_with_U_R':
        E = -c(KR) * UR - c(KZ) * UR
    elif mut == 'E_sign_flipped':
        E = c(KR) * UR + c(KZ) * UZ
    elif mut == 'vw_in_E_map':
        E = -c(w * KR) * UR - c(w * KZ) * UZ
    else:
        E = -c(KR) * UR - c(KZ) * UZ
    if mut == 'rho_gamma_integer_division':
        rg = rho ** (5 // 3)
    elif mut == 'rho_not_rho_gamma':
        rg = rho
    else:
        rg = rho ** g
    PM = c(g * P / rho) * G + c(rg) * E
    if mut == 'VR_column_broadcast':
        VR = im * Om * UR
    else:
        VR = im * c(Om) * UR
    if mut == 'VP_missing_R_factor':
        VP = -c(OmR) * UR + im * c(Om) * UP - c(OmZ) * UZ
    elif mut == 'm_hardcoded_1_in_VP':
        VP = -c(R * OmR) * UR + 1j * c(Om) * UP - c(R * OmZ) * UZ
    else:
        VP = -c(R * OmR) * UR + im * c(Om) * UP - c(R * OmZ) * UZ
    VZ = im * c(Om) * UZ
    if mut == 'coriolis_factor_1':
        AR = im * c(Om) * VR - c(Om) * VP
    elif mut == 'coriolis_sign_flipped':
        AR = im * c(Om) * VR + 2 * c(Om) * VP
    else:
        AR = im * c(Om) * VR - 2 * c(Om) * VP
    if mut == 'AP_coefficient_on_VP':
        AP = im * c(Om) * VP + c(2 * Om + R * OmR) * VP + c(R * OmZ) * VZ
    elif mut == 'AP_radial_shear_sign':
        AP = im * c(Om) * VP + c(2 * Om - R * OmR) * VR + c(R * OmZ) * VZ
    else:
        AP = im * c(Om) * VP + c(2 * Om + R * OmR) * VR + c(R * OmZ) * VZ
    AZ = im * c(Om) * VZ
    wr = w * rho
    A = form(UR, wr, AR) + form(UP, wr, AP)
    A = A + (form(UZ, wr, AR) if mut == 'AZ_term_uses_AR' else form(UZ, wr, AZ))
    if mut == 'rho_in_pressure':
        A = A - form(DU, w * rho, PM)
    elif mut == 'PM_conjugated_trial':
        A = A - form(DU, w, PM.conj())
    elif mut == 'pressure_weight_broadcast':
        A = A - DU.conj().T @ (w * PM)
    else:
        A = A - form(DU, w, PM)
    if mut == 'density_Pz_tested_with_U_phi':
        A = A - form(UR, w * PR / rho, G) - form(UP, w * PZ / rho, G)
    else:
        A = A - form(UR, w * PR / rho, G) - form(UZ, w * PZ / rho, G)
    if mut == 'b_missing_rho':
        b = -(vform(UR, w * fR) + vform(UP, w * fP) + vform(UZ, w * fZ))
    elif mut == 'f_R_f_z_swapped':
        b = -(vform(UR, wr * fZ) + vform(UP, wr * fP) + vform(UZ, wr * fR))
    elif mut == 'f_phi_tested_with_U_z':
        b = -(vform(UR, wr * fR) + vform(UZ, wr * fP) + vform(UZ, wr * fZ))
    else:
        b = -(vform(UR, wr * fR) + vform(UP, wr * fP) + vform(UZ, wr * fZ))
    if mut == 'A_real_part':
        A = A.real
    if mut == 'A_hermitian_transpose':
        A = A.conj().T
    A_out = A / ns
    if mut == 'A_double_normalized':
        A_out = A / ns / ns
    elif mut == 'A_not_normalized':
        A_out = A
    VR_out = VR / ns if mut == 'VR_scaled_by_ns' else VR
    return dict(A=A_out, b=b / ns, E=E, PM=PM, VR=VR_out, VP=VP, VZ=VZ, AR=AR, AP=AP, AZ=AZ,
                A_unscaled=A, b_unscaled=b)


C4_MUTANTS = ('G_conjugated', 'K_z_paired_with_U_R', 'E_sign_flipped', 'vw_in_E_map',
              'rho_gamma_integer_division', 'rho_not_rho_gamma', 'VR_column_broadcast',
              'VP_missing_R_factor', 'm_hardcoded_1_in_VP', 'coriolis_factor_1',
              'coriolis_sign_flipped', 'AP_coefficient_on_VP', 'AP_radial_shear_sign',
              'AZ_term_uses_AR', 'rho_in_pressure', 'PM_conjugated_trial',
              'pressure_weight_broadcast', 'density_Pz_tested_with_U_phi', 'b_missing_rho',
              'f_R_f_z_swapped', 'f_phi_tested_with_U_z', 'A_real_part', 'A_hermitian_transpose',
              'A_double_normalized', 'A_not_normalized', 'VR_scaled_by_ns')


def make_c4_target(mut=None):
    def target(*, R, rho, P, K_R, K_z, P_R, P_z, Omega, Omega_R, Omega_z, volume_weights,
               U_R, U_phi, U_z, divU, G, f_R, f_phi, f_z, m, gamma, normalization_scale, provenance):
        kw = dict(R=R, rho=rho, P=P, K_R=K_R, K_z=K_z, P_R=P_R, P_z=P_z, Omega=Omega,
                  Omega_R=Omega_R, Omega_z=Omega_z, volume_weights=volume_weights, U_R=U_R,
                  U_phi=U_phi, U_z=U_z, divU=divU, G=G, f_R=f_R, f_phi=f_phi, f_z=f_z, m=m,
                  gamma=gamma, normalization_scale=normalization_scale, provenance=provenance)
        out = c4_core(kw, mut)
        return dict((k, out[k]) for k in OUTS)
    return target


def make_literal_target(compiled):
    def target(*, R, rho, P, K_R, K_z, P_R, P_z, Omega, Omega_R, Omega_z, volume_weights,
               U_R, U_phi, U_z, divU, G, f_R, f_phi, f_z, m, gamma, normalization_scale, provenance):
        kw = dict(R=R, rho=rho, P=P, K_R=K_R, K_z=K_z, P_R=P_R, P_z=P_z, Omega=Omega,
                  Omega_R=Omega_R, Omega_z=Omega_z, volume_weights=volume_weights, U_R=U_R,
                  U_phi=U_phi, U_z=U_z, divU=divU, G=G, f_R=f_R, f_phi=f_phi, f_z=f_z, m=m,
                  gamma=gamma, normalization_scale=normalization_scale, provenance=provenance)
        out = literal_assemble(compiled, kw)
        return dict((k, out[k]) for k in OUTS)
    return target


# ------------------------------------------------------------------------------- manufactured inputs
def rand_case(seed, npts, nf, m, structured=False):
    """Random valid inputs.  Omega_R, Omega_z have magnitude in [0.2, 0.8] with random sign
    (bounded away from zero); odd seeds give Omega of mixed sign.  Complex maps/forcing have
    independent N(0,1) real and imaginary parts.  structured=True gives the root map structure:
    real-dtype U_R and U_z, purely imaginary U_phi, real-valued divU and G (complex dtype)."""
    rng = np.random.default_rng(seed)

    def signed(lo, hi):
        return rng.uniform(lo, hi, npts) * rng.choice([-1.0, 1.0], npts)

    kw = {}
    kw['R'] = rng.uniform(0.5, 3.0, npts)
    kw['rho'] = rng.uniform(0.5, 2.5, npts)
    kw['P'] = rng.uniform(0.5, 2.0, npts)
    for k in ('K_R', 'K_z', 'P_R', 'P_z'):
        kw[k] = rng.normal(size=npts)
    kw['Omega'] = signed(0.5, 1.5) if seed % 2 else rng.uniform(0.5, 1.5, npts)
    kw['Omega_R'] = signed(0.2, 0.8)
    kw['Omega_z'] = signed(0.2, 0.8)
    kw['volume_weights'] = rng.uniform(0.1, 1.0, npts)
    if structured:
        kw['U_R'] = rng.normal(size=(npts, nf))
        kw['U_phi'] = -1j * rng.normal(size=(npts, nf))
        kw['U_z'] = rng.normal(size=(npts, nf))
        kw['divU'] = rng.normal(size=(npts, nf)).astype(np.complex128)
        kw['G'] = rng.normal(size=(npts, nf)).astype(np.complex128)
    else:
        for k in ('U_R', 'U_phi', 'U_z', 'divU', 'G'):
            kw[k] = rng.normal(size=(npts, nf)) + 1j * rng.normal(size=(npts, nf))
    for k in ('f_R', 'f_phi', 'f_z'):
        kw[k] = rng.normal(size=npts) + 1j * rng.normal(size=npts)
    kw['m'] = int(m)
    kw['gamma'] = GAMMA
    kw['normalization_scale'] = float(rng.uniform(0.5, 4.0))
    kw['provenance'] = 'C4X crosscheck seed=%d shape=(%d,%d)' % (seed, npts, nf)
    return kw


def oracle_kw(kw):
    return dict((k, kw[k]) for k in CANON if k not in ('normalization_scale', 'provenance'))


def condition_scale(kw):
    """Componentwise magnitude scale of the UNSCALED A and b: the contract chain evaluated on
    absolute values with every subtraction replaced by addition (|i m Omega| = m|Omega|).
    |A_x - A_y| / scale is a cancellation-free roundoff measure."""
    a = dict((k, np.abs(np.asarray(kw[k]))) for k in ARRAYS)
    m = kw['m']
    c = lambda v: v[:, None]  # noqa: E731
    E = c(a['K_R']) * a['U_R'] + c(a['K_z']) * a['U_z']
    PM = c(GAMMA * a['P'] / a['rho']) * a['G'] + c(a['rho'] ** GAMMA) * E
    VR = m * c(a['Omega']) * a['U_R']
    VP = c(a['R'] * a['Omega_R']) * a['U_R'] + m * c(a['Omega']) * a['U_phi'] + c(a['R'] * a['Omega_z']) * a['U_z']
    VZ = m * c(a['Omega']) * a['U_z']
    AR = m * c(a['Omega']) * VR + 2 * c(a['Omega']) * VP
    AP = m * c(a['Omega']) * VP + c(2 * a['Omega'] + a['R'] * a['Omega_R']) * VR + c(a['R'] * a['Omega_z']) * VZ
    AZ = m * c(a['Omega']) * VZ
    w, rho = a['volume_weights'], a['rho']
    SA = (a['U_R'].T @ (c(w * rho) * AR) + a['U_phi'].T @ (c(w * rho) * AP) + a['U_z'].T @ (c(w * rho) * AZ)
          + a['divU'].T @ (c(w) * PM) + (a['U_R'].T * (w * a['P_R'] / rho)[None, :]
                                          + a['U_z'].T * (w * a['P_z'] / rho)[None, :]) @ a['G'])
    Sb = a['U_R'].T @ (w * rho * a['f_R']) + a['U_phi'].T @ (w * rho * a['f_phi']) + a['U_z'].T @ (w * rho * a['f_z'])
    return SA, Sb


def cond_err(x, y, s):
    x = np.asarray(x)
    y = np.asarray(y)
    if x.shape != y.shape:
        return float('inf')
    return float(np.max(np.abs(x - y) / s)) if x.size else 0.0


def exact_unscaled(kw):
    """Exact rational evaluation of the contract chain for the given float inputs (complex numbers
    as (re, im) Fraction pairs).  rho**gamma is taken as the float value float(rho)**(5/3) and gamma
    as the float 5/3, i.e. the same inputs the float implementations see.  Returns complex128
    A_unscaled (nfree, nfree) and b_unscaled (nfree,) correctly rounded from the exact values."""
    from fractions import Fraction as Fr
    n, k = np.shape(kw['U_R'])

    def C(z):
        z = complex(z)
        return (Fr(z.real), Fr(z.imag))

    def add(*zs):
        return (sum((z[0] for z in zs), Fr(0)), sum((z[1] for z in zs), Fr(0)))

    def mul(a, b):
        return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])

    def sc(s, z):
        return (s * z[0], s * z[1])

    def cj(z):
        return (z[0], -z[1])

    g = Fr(GAMMA)
    zero = (Fr(0), Fr(0))
    A = [[zero for _ in range(k)] for _ in range(k)]
    b = [zero for _ in range(k)]
    for p in range(n):
        R, rho, P = (Fr(float(kw[x][p])) for x in ('R', 'rho', 'P'))
        KR, KZ, PR, PZ = (Fr(float(kw[x][p])) for x in ('K_R', 'K_z', 'P_R', 'P_z'))
        Om, OR, OZ, w = (Fr(float(kw[x][p])) for x in ('Omega', 'Omega_R', 'Omega_z', 'volume_weights'))
        rg = Fr(float(kw['rho'][p]) ** GAMMA)
        UR, UP, UZ, DU, G = ([C(kw[x][p][j]) for j in range(k)] for x in ('U_R', 'U_phi', 'U_z', 'divU', 'G'))
        fR, fP, fZ = (C(kw[x][p]) for x in ('f_R', 'f_phi', 'f_z'))
        imO = (Fr(0), Om * kw['m'])
        wr = w * rho
        cols = []
        for j in range(k):
            E = add(sc(-KR, UR[j]), sc(-KZ, UZ[j]))
            PM = add(sc(g * P / rho, G[j]), sc(rg, E))
            VR = mul(imO, UR[j])
            VP = add(sc(-(R * OR), UR[j]), mul(imO, UP[j]), sc(-(R * OZ), UZ[j]))
            VZ = mul(imO, UZ[j])
            AR = add(mul(imO, VR), sc(-2 * Om, VP))
            AP = add(mul(imO, VP), sc(2 * Om + R * OR, VR), sc(R * OZ, VZ))
            AZ = mul(imO, VZ)
            cols.append((AR, AP, AZ, PM))
        for t in range(k):
            for j in range(k):
                AR, AP, AZ, PM = cols[j]
                term = add(sc(wr, mul(cj(UR[t]), AR)), sc(wr, mul(cj(UP[t]), AP)), sc(wr, mul(cj(UZ[t]), AZ)),
                           sc(-w, mul(cj(DU[t]), PM)),
                           sc(-1, mul(add(sc(w * PR / rho, cj(UR[t])), sc(w * PZ / rho, cj(UZ[t]))), G[j])))
                A[t][j] = add(A[t][j], term)
            b[t] = add(b[t], sc(-wr, mul(cj(UR[t]), fR)), sc(-wr, mul(cj(UP[t]), fP)), sc(-wr, mul(cj(UZ[t]), fZ)))
    Af = np.array([[complex(float(z[0]), float(z[1])) for z in row] for row in A])
    bf = np.array([complex(float(z[0]), float(z[1])) for z in b])
    return Af, bf


# =============================================================================================
def main():
    t_start = time.time()
    print('C4X crosscheck_c4_v001 | python %s | numpy %s' % (sys.version.split()[0], np.__version__))

    # ------------------------------------------------------------------------------ [0] hashes
    hashes = {}
    all_ok = True
    for label, path, want in EXPECTED_SHA:
        got = sha256_file(path)
        ok = (got == want)
        all_ok = all_ok and ok
        hashes[label] = {'path': path, 'sha256': got, 'matches_expected': ok}
        print('[0] %-34s %s %s' % (label, got, 'OK' if ok else 'MISMATCH (expected %s)' % want))
    RESULT['hashes_all_match'] = all_ok

    h1 = load_by_path('c4x_h1_oracle', H1_ORACLE)
    h2ref_mod = load_by_path('c4x_h2_reference', H2_REF)
    ref = h2ref_mod.reference_assemble

    # ------------------------------------------------------------------------------ [1] contract
    eqs, n_um = contract_equations()
    typed_equal = (eqs[:10] == C4_TYPED_EQUATIONS)
    compiled = build_literal(eqs)
    print('[1] contract equations: %d entries, %d unicode minus signs normalized; first 10 equal to '
          'C4 typed transcription: %s' % (len(eqs), n_um, typed_equal))
    for lhs, rhs, _ in compiled[8:10]:
        print('[1]   translated %s = %s' % (lhs, rhs))
    translation_ok = (compiled[8][0] == 'A' and compiled[8][1] == EXPECTED_TRANSLATION['A'] and
                      compiled[9][0] == 'b' and compiled[9][1] == EXPECTED_TRANSLATION['b'] and
                      [c_[0] for c_ in compiled[:8]] == ['E', 'PM', 'VR', 'VP', 'VZ', 'AR', 'AP', 'AZ'])
    print('[1]   translation equals the hand-checked expected form: %s' % translation_ok)
    print('[1]   eq 11 (prose): %s' % eqs[10])
    RESULT['contract_text_equal_to_c4_typed'] = typed_equal
    RESULT['translation_matches_expected'] = translation_ok
    RESULT['translated_A'] = compiled[8][1]
    RESULT['translated_b'] = compiled[9][1]

    # ------------------------------------------------------------------------------ [2] random
    shapes = ((7, 3), (4, 4), (16, 5), (9, 1), (1, 1), (3, 5))
    seeds = (0, 1, 2, 3, 4, 5)
    stats = dict(oracle_vs_ref_A=0.0, oracle_vs_ref_b=0.0, oracle_vs_ref_A_frob=0.0,
                 oracle_vs_ref_b_frob=0.0, literal_vs_ref_A=0.0, literal_vs_ref_b=0.0,
                 literal_vs_ref_maps=0.0, c4_vs_ref_A=0.0, c4_vs_ref_b=0.0, c4_vs_ref_maps=0.0,
                 c4_vs_literal_AR_AP_AZ=0.0, oracle_vs_literal_A=0.0, oracle_vs_literal_b=0.0,
                 ref_unscaled_vs_scaled=0.0, min_rel_effect_Omega_z_on_A=float('inf'),
                 min_rel_effect_test_conj_on_A=float('inf'))
    shape_ok = True
    ncases = 0
    for (npts, nf) in shapes:
        for seed in seeds:
            for m in range(1, 7):
                kw = rand_case(seed, npts, nf, m)
                ns = kw['normalization_scale']
                r = ref(**kw)
                Ao, bo = h1.oracle_A_b(**oracle_kw(kw))
                lit = literal_assemble(compiled, kw)
                c4 = c4_core(kw)
                ncases += 1
                shape_ok = shape_ok and r['A'].shape == (nf, nf) and r['b'].shape == (nf,) and \
                    all(r[k].shape == (npts, nf) for k in ('E', 'PM', 'VR', 'VP', 'VZ')) and \
                    Ao.shape == (nf, nf) and bo.shape == (nf,)
                upd = {
                    'oracle_vs_ref_A': rel(Ao / ns, r['A']), 'oracle_vs_ref_b': rel(bo / ns, r['b']),
                    'oracle_vs_ref_A_frob': frob(Ao / ns, r['A']),
                    'oracle_vs_ref_b_frob': frob(bo / ns, r['b']),
                    'literal_vs_ref_A': rel(lit['A'], r['A']), 'literal_vs_ref_b': rel(lit['b'], r['b']),
                    'literal_vs_ref_maps': max(rel(lit[k], r[k]) for k in ('E', 'PM', 'VR', 'VP', 'VZ')),
                    'c4_vs_ref_A': rel(c4['A'], r['A']), 'c4_vs_ref_b': rel(c4['b'], r['b']),
                    'c4_vs_ref_maps': max(rel(c4[k], r[k]) for k in ('E', 'PM', 'VR', 'VP', 'VZ')),
                    'c4_vs_literal_AR_AP_AZ': max(rel(c4[k], lit[k]) for k in ('AR', 'AP', 'AZ')),
                    'oracle_vs_literal_A': rel(Ao, lit['A_unscaled']),
                    'oracle_vs_literal_b': rel(bo, lit['b_unscaled']),
                    'ref_unscaled_vs_scaled': max(rel(r['A_unscaled'] / ns, r['A']),
                                                  rel(r['b_unscaled'] / ns, r['b'])),
                }
                SA, Sb = condition_scale(kw)
                upd['oracle_vs_ref_A_condition_scaled'] = cond_err(Ao, r['A_unscaled'], SA)
                upd['oracle_vs_ref_b_condition_scaled'] = cond_err(bo, r['b_unscaled'], Sb)
                for k_ in ('oracle_vs_ref_A_condition_scaled', 'oracle_vs_ref_b_condition_scaled'):
                    stats.setdefault(k_, 0.0)
                for k, v in upd.items():
                    stats[k] = max(stats[k], v)
                # sensitivity: the vertical-shear term and the test-side conjugation are resolvable
                kz = dict(kw, Omega_z=np.zeros(npts))
                stats['min_rel_effect_Omega_z_on_A'] = min(stats['min_rel_effect_Omega_z_on_A'],
                                                           rel(ref(**kz)['A'], r['A']))
                UR, UP, UZ = kw['U_R'], kw['U_phi'], kw['U_z']
                wr = kw['volume_weights'] * kw['rho']
                A_noconj = (UR.T @ (wr[:, None] * lit['AR']) + UP.T @ (wr[:, None] * lit['AP'])
                            + UZ.T @ (wr[:, None] * lit['AZ']))
                A_conj = (form(UR, wr, lit['AR']) + form(UP, wr, lit['AP']) + form(UZ, wr, lit['AZ']))
                stats['min_rel_effect_test_conj_on_A'] = min(stats['min_rel_effect_test_conj_on_A'],
                                                             rel(A_noconj, A_conj))
                if upd['oracle_vs_ref_A'] >= stats.get('_worst_A_val', -1.0):
                    stats['_worst_A_val'] = upd['oracle_vs_ref_A']
                    stats['worst_oracle_vs_ref_A_case'] = 'seed=%d shape=(%d,%d) m=%d' % (seed, npts, nf, m)
    stats.pop('_worst_A_val', None)
    stats['ncases'] = ncases
    stats['shapes'] = [list(s) for s in shapes]
    stats['all_output_shapes_correct'] = shape_ok
    RESULT['random_complex'] = stats
    # [2b] exact rational arithmetic on a subset: every float route against exact values
    ex = dict(ncases=0)
    for key in ('ref', 'oracle', 'literal', 'c4'):
        for q in ('A', 'b', 'A_condition_scaled', 'b_condition_scaled'):
            ex[key + '_' + q] = 0.0
    for (npts, nf) in ((4, 3), (3, 3), (1, 1), (9, 1), (16, 5)):
        for seed in (0, 1, 2, 3, 4, 5):
            for m in range(1, 7):
                kw = rand_case(seed, npts, nf, m)
                Ae, be = exact_unscaled(kw)
                SA, Sb = condition_scale(kw)
                r = ref(**kw)
                Ao, bo = h1.oracle_A_b(**oracle_kw(kw))
                lit = literal_assemble(compiled, kw)
                c4 = c4_core(kw)
                for key, (Ax, bx) in (('ref', (r['A_unscaled'], r['b_unscaled'])), ('oracle', (Ao, bo)),
                                      ('literal', (lit['A_unscaled'], lit['b_unscaled'])),
                                      ('c4', (c4['A_unscaled'], c4['b_unscaled']))):
                    ex[key + '_A'] = max(ex[key + '_A'], rel(Ax, Ae))
                    ex[key + '_b'] = max(ex[key + '_b'], rel(bx, be))
                    ex[key + '_A_condition_scaled'] = max(ex[key + '_A_condition_scaled'], cond_err(Ax, Ae, SA))
                    ex[key + '_b_condition_scaled'] = max(ex[key + '_b_condition_scaled'], cond_err(bx, be, Sb))
                ex['ncases'] += 1
    RESULT['exact_rational'] = ex
    print('[2] %d random complex cases (seeds %s x shapes %s x m=1..6; Omega_R,Omega_z in +-[0.2,0.8]; '
          'odd seeds mixed-sign Omega)' % (ncases, list(seeds), [tuple(s) for s in shapes]))
    for k in sorted(stats):
        if k not in ('ncases', 'shapes'):
            print('[2]   %-34s %s' % (k, ('%.3e' % stats[k]) if isinstance(stats[k], float) else stats[k]))
    print('[2b] exact rational arithmetic, %d cases (shapes (4,3),(3,3),(1,1),(9,1),(16,5); seeds 0-5; m=1..6)'
          % ex['ncases'])
    for key, label in (('ref', 'H2 reference'), ('oracle', 'H1 oracle'), ('literal', 'contract-literal'),
                       ('c4', 'C4 transcription')):
        print('[2b]   %-17s vs exact: max-abs rel A %.3e b %.3e | condition-scaled A %.3e b %.3e'
              % (label, ex[key + '_A'], ex[key + '_b'], ex[key + '_A_condition_scaled'],
                 ex[key + '_b_condition_scaled']))

    # ------------------------------------------------------------------------------ [3] structured
    st = dict(oracle_vs_ref_A=0.0, oracle_vs_ref_b=0.0, literal_vs_ref_A=0.0, literal_vs_ref_b=0.0,
              literal_vs_ref_maps=0.0, c4_vs_ref_A=0.0, c4_vs_ref_b=0.0,
              max_rel_imag_A=0.0, min_rel_imag_b=float('inf'),
              min_rel_effect_Uphi_test_conj_on_A=float('inf'),
              min_rel_effect_Uphi_test_conj_on_b=float('inf'),
              max_rel_effect_UR_UZ_divU_test_conj_on_A=0.0)
    nst = 0
    for (npts, nf) in ((7, 3), (4, 4), (9, 1), (16, 5)):
        for seed in (10, 11, 12, 13):
            for m in range(1, 7):
                kw = rand_case(seed, npts, nf, m, structured=True)
                ns = kw['normalization_scale']
                r = ref(**kw)
                Ao, bo = h1.oracle_A_b(**oracle_kw(kw))
                lit = literal_assemble(compiled, kw)
                c4 = c4_core(kw)
                nst += 1
                for k, v in (('oracle_vs_ref_A', rel(Ao / ns, r['A'])), ('oracle_vs_ref_b', rel(bo / ns, r['b'])),
                             ('literal_vs_ref_A', rel(lit['A'], r['A'])), ('literal_vs_ref_b', rel(lit['b'], r['b'])),
                             ('literal_vs_ref_maps', max(rel(lit[x], r[x]) for x in ('E', 'PM', 'VR', 'VP', 'VZ'))),
                             ('c4_vs_ref_A', rel(c4['A'], r['A'])), ('c4_vs_ref_b', rel(c4['b'], r['b']))):
                    st[k] = max(st[k], v)
                A = r['A']
                st['max_rel_imag_A'] = max(st['max_rel_imag_A'], float(np.max(np.abs(A.imag)) / np.max(np.abs(A))))
                st['min_rel_imag_b'] = min(st['min_rel_imag_b'], float(np.max(np.abs(r['b'].imag)) / np.max(np.abs(r['b']))))
                UR, UP, UZ, DU = kw['U_R'], kw['U_phi'], kw['U_z'], kw['divU']
                wr = kw['volume_weights'] * kw['rho']
                w = kw['volume_weights']
                term_phi = form(UP, wr, lit['AP'])
                term_phi_T = UP.T @ (wr[:, None] * lit['AP'])
                A_mut = lit['A_unscaled'] - term_phi + term_phi_T
                st['min_rel_effect_Uphi_test_conj_on_A'] = min(st['min_rel_effect_Uphi_test_conj_on_A'],
                                                               rel(A_mut, lit['A_unscaled']))
                bphi = vform(UP, wr * kw['f_phi'])
                b_mut = lit['b_unscaled'] + bphi - UP.T @ (wr * kw['f_phi'])
                st['min_rel_effect_Uphi_test_conj_on_b'] = min(st['min_rel_effect_Uphi_test_conj_on_b'],
                                                               rel(b_mut, lit['b_unscaled']))
                A_mut2 = (UR.T @ (wr[:, None] * lit['AR']) + form(UP, wr, lit['AP'])
                          + UZ.T @ (wr[:, None] * lit['AZ']) - DU.T @ (w[:, None] * lit['PM'])
                          - (UR.T * (w * kw['P_R'] / kw['rho'])[None, :]
                             + UZ.T * (w * kw['P_z'] / kw['rho'])[None, :]) @ kw['G'])
                st['max_rel_effect_UR_UZ_divU_test_conj_on_A'] = max(
                    st['max_rel_effect_UR_UZ_divU_test_conj_on_A'], rel(A_mut2, lit['A_unscaled']))
    st['ncases'] = nst
    RESULT['root_structured'] = st
    print('[3] %d root-structured cases (real U_R,U_z; imaginary U_phi; real-valued divU,G; complex f)' % nst)
    for k in sorted(st):
        if k != 'ncases':
            print('[3]   %-42s %.3e' % (k, st[k]))

    # ------------------------------------------------------------------------------ [4] hand case
    def a1(v):
        return np.array([v], dtype=float)

    def m11(v):
        return np.array([[v]], dtype=complex)

    hand = dict(R=a1(2.0), rho=a1(8.0), P=a1(12.0), K_R=a1(1.0), K_z=a1(3.0), P_R=a1(16.0),
                P_z=a1(-24.0), Omega=a1(2.0), Omega_R=a1(1.5), Omega_z=a1(-1.0),
                volume_weights=a1(0.5), U_R=m11(1 + 2j), U_phi=m11(2 - 1j), U_z=m11(-1 + 1j),
                divU=m11(3 - 2j), G=m11(2 + 1j), f_R=np.array([1 - 1j]), f_phi=np.array([2j]),
                f_z=np.array([-3 + 1j]), m=2, gamma=GAMMA, normalization_scale=4.0,
                provenance='C4X hand case')
    # C4's own hand derivation (done by hand, independently of H2's note):
    # E=2-5i; PM=69-157.5i; VR=-8+4i; VP=-1+4i; VZ=-4-4i; AR=-12-48i; AP=-64+32i; AZ=16-16i;
    # inertial sum (wrho=4): 4[(-108-24i)+(-160)+(-32)] = -1200-96i; pressure: -0.5(3+2i)(69-157.5i)
    # = -261+167.25i; density: -[(1-2i)*1+(-1-i)*(-1.5)](2+i) = -(2.5-0.5i)(2+i) = -5.5-1.5i;
    # A_unscaled = -1466.5+69.75i, A = -366.625+17.4375i; b_unscaled = -4[(-1-3i)+(-2+4i)+(4+2i)]
    # = -4-12i, b = -1-3i.
    C4_HAND = {'E': 2 - 5j, 'PM': 69 - 157.5j, 'VR': -8 + 4j, 'VP': -1 + 4j, 'VZ': -4 - 4j,
               'AR': -12 - 48j, 'AP': -64 + 32j, 'AZ': 16 - 16j, 'A_unscaled': -1466.5 + 69.75j,
               'b_unscaled': -4 - 12j, 'A': -366.625 + 17.4375j, 'b': -1 - 3j}
    r = ref(**hand)
    lit = literal_assemble(compiled, hand)
    Ao, bo = h1.oracle_A_b(**oracle_kw(hand))
    hand_err = {}
    for k, v in C4_HAND.items():
        src = lit if k in ('AR', 'AP', 'AZ') else r
        hand_err['ref_or_literal_' + k] = abs(complex(np.asarray(src[k]).ravel()[0]) - v) / abs(v)
    hand_err['oracle_A'] = abs(complex(Ao[0, 0]) / 4.0 - C4_HAND['A']) / abs(C4_HAND['A'])
    hand_err['oracle_b'] = abs(complex(bo[0]) / 4.0 - C4_HAND['b']) / abs(C4_HAND['b'])
    hand_err['literal_A'] = abs(complex(lit['A'][0, 0]) - C4_HAND['A']) / abs(C4_HAND['A'])
    rho_gamma_float = 8.0 ** GAMMA
    RESULT['hand_case_max_rel_err'] = max(hand_err.values())
    RESULT['hand_case_8_pow_5_3'] = repr(rho_gamma_float)
    print('[4] hand case: max rel err of reference/literal/oracle vs C4 hand values = %.3e '
          '(8.0**(5/3) = %r)' % (max(hand_err.values()), rho_gamma_float))
    print('[4]   reference A = %r, b = %r' % (complex(r['A'][0, 0]), complex(r['b'][0])))

    # ------------------------------------------------------------------------------ [5] M_p
    rng = np.random.default_rng(55)
    n5 = 11
    Rr = rng.uniform(0.5, 3.0, n5)
    Om = rng.uniform(0.5, 1.5, n5) * rng.choice([-1.0, 1.0], n5)
    OmR = rng.uniform(0.2, 0.8, n5) * rng.choice([-1.0, 1.0], n5)
    OmZ = rng.uniform(0.2, 0.8, n5) * rng.choice([-1.0, 1.0], n5)
    mp_err_c4 = 0.0
    mp_err_h1 = 0.0
    for m in range(1, 7):
        e = np.ones((n5, 1), dtype=complex)
        z = np.zeros((n5, 1), dtype=complex)
        cols = []
        for UR_, UP_, UZ_ in ((e, z, z), (z, e, z), (z, z, e)):
            kw = dict(rand_case(1, n5, 1, m), R=Rr, Omega=Om, Omega_R=OmR, Omega_z=OmZ,
                      U_R=UR_, U_phi=UP_, U_z=UZ_)
            lit = literal_assemble(compiled, kw)
            cols.append(np.stack([lit['AR'][:, 0], lit['AP'][:, 0], lit['AZ'][:, 0]], axis=1))
        M_chain = np.stack(cols, axis=2)  # (n, row, col)
        O2 = Om * Om
        M_c4 = np.zeros((n5, 3, 3), dtype=complex)
        M_c4[:, 0, 0] = -m * m * O2 + 2 * Rr * Om * OmR
        M_c4[:, 0, 1] = -2j * m * O2
        M_c4[:, 0, 2] = 2 * Rr * Om * OmZ
        M_c4[:, 1, 0] = 2j * m * O2
        M_c4[:, 1, 1] = -m * m * O2
        M_c4[:, 2, 2] = -m * m * O2
        M_h1 = h1.pointwise_inertial_matrix(R=Rr, Omega=Om, Omega_R=OmR, Omega_z=OmZ, m=m)
        mp_err_c4 = max(mp_err_c4, rel(M_chain, M_c4))
        mp_err_h1 = max(mp_err_h1, rel(M_h1, M_c4))
    RESULT['Mp_chain_vs_c4_hand'] = mp_err_c4
    RESULT['Mp_h1_vs_c4_hand'] = mp_err_h1
    print('[5] M_p from the contract chain (unit maps) vs C4 hand form: %.3e ; H1 pointwise_inertial_matrix '
          'vs C4 hand form: %.3e' % (mp_err_c4, mp_err_h1))

    # ------------------------------------------------------------------------------ [6] 1i restructuring
    restr_err = 0.0
    herm_full = 0.0
    herm_inertial_min = float('inf')
    herm_pressure_min = float('inf')
    cancel_err = 0.0
    herm_mut_min = float('inf')
    n6 = 0
    for (npts, nf) in ((9, 4), (5, 5), (12, 3)):
        for seed in (60, 61, 62):
            for m in range(1, 7):
                rg_ = np.random.default_rng(seed)
                R6 = rg_.uniform(0.8, 2.5, npts)
                rho6 = rg_.uniform(0.5, 2.0, npts)
                K6 = rg_.uniform(0.5, 1.5, npts)
                P6 = K6 * rho6 ** GAMMA
                rho_R, rho_z = rg_.normal(size=npts), rg_.normal(size=npts)
                K_R6, K_z6 = rg_.normal(size=npts), rg_.normal(size=npts)
                P_R6 = rho6 ** GAMMA * K_R6 + GAMMA * P6 / rho6 * rho_R
                P_z6 = rho6 ** GAMMA * K_z6 + GAMMA * P6 / rho6 * rho_z
                Om6 = rg_.uniform(0.6, 1.4, npts) * rg_.choice([-1.0, 1.0], npts)
                Om_z6 = (P_z6 * rho_R - P_R6 * rho_z) / (2 * R6 * Om6 * rho6 ** 2)  # thermal wind
                Om_R6 = rg_.normal(scale=0.5, size=npts)
                w6 = rg_.uniform(0.1, 1.0, npts)
                cm = lambda: rg_.normal(size=(npts, nf)) + 1j * rg_.normal(size=(npts, nf))  # noqa: E731
                UR6, UP6, UZ6, DU6 = cm(), cm(), cm(), cm()
                G6 = -(rho6[:, None] * DU6 + rho_R[:, None] * UR6 + rho_z[:, None] * UZ6)
                kw = dict(R=R6, rho=rho6, P=P6, K_R=K_R6, K_z=K_z6, P_R=P_R6, P_z=P_z6, Omega=Om6,
                          Omega_R=Om_R6, Omega_z=Om_z6, volume_weights=w6, U_R=UR6, U_phi=UP6,
                          U_z=UZ6, divU=DU6, G=G6, f_R=np.zeros(npts, complex),
                          f_phi=np.zeros(npts, complex), f_z=np.zeros(npts, complex), m=m,
                          gamma=GAMMA, normalization_scale=1.0, provenance='C4X [6]')
                parts = h1.oracle_parts(**oracle_kw(kw))
                pd_restr = (form(DU6, w6 * GAMMA * P6, DU6)
                            + form(DU6, w6 * P_R6, UR6) + form(UR6, w6 * P_R6, DU6)
                            + form(DU6, w6 * P_z6, UZ6) + form(UZ6, w6 * P_z6, DU6)
                            + form(UR6, w6 * P_R6 * rho_R / rho6, UR6)
                            + form(UZ6, w6 * P_z6 * rho_z / rho6, UZ6)
                            + form(UR6, w6 * P_R6 * rho_z / rho6, UZ6)
                            + form(UZ6, w6 * P_z6 * rho_R / rho6, UR6))
                c4 = c4_core(kw)
                inertial_c4 = (form(UR6, w6 * rho6, c4['AR']) + form(UP6, w6 * rho6, c4['AP'])
                               + form(UZ6, w6 * rho6, c4['AZ']))
                pd_c4 = c4['A_unscaled'] - inertial_c4
                restr_err = max(restr_err, rel(pd_restr, pd_c4), rel(parts['pressure_density'], pd_c4))
                Aref = ref(**kw)['A_unscaled']
                herm_full = max(herm_full, antiherm(Aref))
                herm_inertial_min = min(herm_inertial_min, antiherm(inertial_c4))
                herm_pressure_min = min(herm_pressure_min, antiherm(pd_c4))
                ah_i = inertial_c4 - inertial_c4.conj().T
                ah_p = pd_c4 - pd_c4.conj().T
                cancel_err = max(cancel_err, float(np.linalg.norm(ah_i + ah_p)) / float(np.linalg.norm(ah_i)))
                kw_bad = dict(kw, Omega_z=Om_z6 + 0.3)
                herm_mut_min = min(herm_mut_min, antiherm(ref(**kw_bad)['A_unscaled']))
                n6 += 1
    RESULT['sec1i'] = dict(ncases=n6, restructured_vs_contract_pressure_density=restr_err,
                           full_A_antihermitian_max=herm_full,
                           inertial_alone_antihermitian_min=herm_inertial_min,
                           pressure_density_alone_antihermitian_min=herm_pressure_min,
                           antihermitian_parts_cancel_rel=cancel_err,
                           Omega_z_inconsistent_full_A_antihermitian_min=herm_mut_min)
    print('[6] %d consistent-background cases (P=K rho^g, consistent gradients, thermal-wind Omega_z, '
          'pointwise G=-(rho divU+rho_R U_R+rho_z U_z)):' % n6)
    for k, v in sorted(RESULT['sec1i'].items()):
        if k != 'ncases':
            print('[6]   %-48s %.3e' % (k, v))

    # ------------------------------------------------------------------------------ [7] FD
    a0, a1_, a2, a3, kk = 1.1, 0.3, 0.25, 0.2, 0.7

    def Omf(R, z):
        return a0 + a1_ * math.sin(kk * R) + a2 * z + a3 * R * z

    def OmRf(R, z):
        return a1_ * kk * math.cos(kk * R) + a3 * z

    def Omzf(R, z):
        return a2 + a3 * R

    rng7 = np.random.default_rng(7007)
    CU = [rng7.normal(size=6) + 1j * rng7.normal(size=6) for _ in range(3)]

    def poly(c, R, z):
        return c[0] + c[1] * R + c[2] * z + c[3] * R * R + c[4] * R * z + c[5] * z * z

    def cylc(x):
        return math.hypot(x[0], x[1]), math.atan2(x[1], x[0]), x[2]

    def to_cart(vR, vP, vZ, ph):
        cph, sph = math.cos(ph), math.sin(ph)
        return np.array([vR * cph - vP * sph, vR * sph + vP * cph, vZ], dtype=complex)

    def to_cyl(v, ph):
        cph, sph = math.cos(ph), math.sin(ph)
        return np.array([v[0] * cph + v[1] * sph, -v[0] * sph + v[1] * cph, v[2]])

    def v0(x):
        R, ph, z = cylc(x)
        wv = Omf(R, z)
        return np.array([-wv * x[1], wv * x[0], 0.0], dtype=complex)

    def dv_contract(R, z, m, mutant=None):
        uR, uP, uZ = (poly(c, R, z) for c in CU)
        wv, wr_, wz_ = Omf(R, z), OmRf(R, z), Omzf(R, z)
        im = 1j * m
        VRv = im * wv * uR
        VPv = -(R * wr_) * uR + im * wv * uP + (1 if mutant == 'VP_plus_ROmz' else -1) * (R * wz_) * uZ
        VZv = im * wv * uZ
        return np.array([VRv, VPv, VZv])

    def da_contract(R, z, m, mutant=None):
        VRv, VPv, VZv = dv_contract(R, z, m)
        wv, wr_, wz_ = Omf(R, z), OmRf(R, z), Omzf(R, z)
        im = 1j * m
        ARv = im * wv * VRv - 2 * wv * VPv
        APv = im * wv * VPv + (2 * wv + R * wr_) * VRv + (-1 if mutant == 'AP_minus_ROmz' else 1) * (R * wz_) * VZv
        AZv = im * wv * VZv
        return np.array([ARv, APv, AZv])

    def jac(F, x, h):
        cols = []
        for j in range(3):
            e = np.zeros(3)
            e[j] = h
            cols.append((-F(x + 2 * e) + 8 * F(x + e) - 8 * F(x - e) + F(x - 2 * e)) / (12 * h))
        return np.stack(cols, axis=1)

    fd_dv = 0.0
    fd_da = 0.0
    fd_mut_dv = float('inf')
    fd_mut_da = float('inf')
    h = 1e-3
    pts = [(1.0 + rng7.uniform(0, 1), rng7.uniform(0, 2 * math.pi), rng7.uniform(-0.5, 0.5)) for _ in range(4)]
    for (R0, ph0, z0) in pts:
        x0 = np.array([R0 * math.cos(ph0), R0 * math.sin(ph0), z0])
        for m in range(1, 7):
            def xi(x, m=m):
                R, ph, z = cylc(x)
                return to_cart(poly(CU[0], R, z), poly(CU[1], R, z), poly(CU[2], R, z), ph) * np.exp(1j * m * ph)

            def dvf(x, m=m):
                R, ph, z = cylc(x)
                d = dv_contract(R, z, m)
                return to_cart(d[0], d[1], d[2], ph) * np.exp(1j * m * ph)

            ex = np.exp(1j * m * ph0)
            Jxi = jac(xi, x0, h)
            Jv0 = jac(v0, x0, h)
            dv_fd = to_cyl(Jxi @ v0(x0) - Jv0 @ xi(x0), ph0) / ex
            dv_c = dv_contract(R0, z0, m)
            fd_dv = max(fd_dv, rel(dv_fd, dv_c))
            fd_mut_dv = min(fd_mut_dv, rel(dv_contract(R0, z0, m, 'VP_plus_ROmz'), dv_fd))
            Jdv = jac(dvf, x0, h)
            da_fd = to_cyl(Jdv @ v0(x0) + Jv0 @ dvf(x0), ph0) / ex
            da_c = da_contract(R0, z0, m)
            fd_da = max(fd_da, rel(da_fd, da_c))
            fd_mut_da = min(fd_mut_da, rel(da_contract(R0, z0, m, 'AP_minus_ROmz'), da_fd))
    RESULT['fd'] = dict(dv_vs_contract=fd_dv, da_vs_contract=fd_da,
                        mutant_VP_plus_ROmz_min_dev=fd_mut_dv, mutant_AP_minus_ROmz_min_dev=fd_mut_da,
                        npoints=len(pts), h=h)
    print('[7] Cartesian 4th-order FD (h=%g, %d points, m=1..6, Omega_R and Omega_z nonzero): '
          'delta v = (v0.grad)xi-(xi.grad)v0 vs contract VR,VP,VZ: %.3e ; delta a = (v0.grad)dv+(dv.grad)v0 '
          'vs contract AR,AP,AZ: %.3e ; mutants VP(+R Om_z U_z) %.3e, AP(-R Om_z VZ) %.3e'
          % (h, len(pts), fd_dv, fd_da, fd_mut_dv, fd_mut_da))

    # ------------------------------------------------------------------------------ [8] GL by parts
    xg, wg = np.polynomial.legendre.leggauss(8)  # exact to degree 15 per variable; integrands <= 7
    Rn = 1.5 + 0.5 * xg
    RR, ZZ = np.meshgrid(Rn, xg, indexing='ij')
    W = np.outer(0.5 * wg, wg) * RR  # R dR dz on [1,2] x [-1,1]
    rng8 = np.random.default_rng(808)
    c8 = [rng8.normal(size=6) + 1j * rng8.normal(size=6) for _ in range(4)]

    def pR(c, R, z):
        return c[1] + 2 * c[3] * R + c[4] * z

    def pz(c, R, z):
        return c[2] + c[4] * R + 2 * c[5] * z

    UR8, UP8, UZ8 = (poly(c8[k], RR, ZZ) for k in range(3))
    q8 = poly(c8[3], RR, ZZ)
    bR = (RR - 1) * (2 - RR)
    bz = 1 - ZZ * ZZ
    dP = bR * bz * q8
    dP_R = (3 - 2 * RR) * bz * q8 + bR * bz * pR(c8[3], RR, ZZ)
    dP_z = bR * (-2 * ZZ) * q8 + bR * bz * pz(c8[3], RR, ZZ)
    gl_err = 0.0
    gl_mut_minus_im = float('inf')
    gl_mut_bilinear = float('inf')
    for m in range(1, 7):
        im = 1j * m
        URr = pR(c8[0], RR, ZZ)
        UZz = pz(c8[2], RR, ZZ)
        divU8 = URr + UR8 / RR + im * UP8 / RR + UZz
        comps = [
            (np.sum(W * np.conj(UR8) * dP_R), -np.sum(W * np.conj(URr + UR8 / RR) * dP)),
            (np.sum(W * np.conj(UP8) * (im * dP / RR)), -np.sum(W * np.conj(im * UP8 / RR) * dP)),
            (np.sum(W * np.conj(UZ8) * dP_z), -np.sum(W * np.conj(UZz) * dP)),
        ]
        tot_l = sum(cpair[0] for cpair in comps)
        tot_r = -np.sum(W * np.conj(divU8) * dP)
        scale = max(abs(tot_l), max(abs(cpair[0]) for cpair in comps))
        gl_err = max(gl_err, max(abs(a - b) for a, b in comps) / scale, abs(tot_l - tot_r) / scale)
        divU_bad = URr + UR8 / RR - im * UP8 / RR + UZz
        gl_mut_minus_im = min(gl_mut_minus_im, abs(tot_l + np.sum(W * np.conj(divU_bad) * dP)) / scale)
        bil_l = np.sum(W * (UR8 * dP_R + UP8 * (im * dP / RR) + UZ8 * dP_z))
        bil_r = -np.sum(W * divU8 * dP)
        gl_mut_bilinear = min(gl_mut_bilinear, abs(bil_l - bil_r) / max(abs(bil_l), 1e-300))
    RESULT['gl'] = dict(per_component_and_total=gl_err, mutant_divU_minus_im=gl_mut_minus_im,
                        mutant_no_conjugation=gl_mut_bilinear)
    print('[8] GL 8x8 on R in [1,2], z in [-1,1], delta P = 0 on the boundary: '
          'int conj(U).grad(dP) = -int conj(divU) dP per component and total: %.3e ; mutant divU with '
          '-i m U_phi/R: %.3e ; mutant without conjugation: %.3e' % (gl_err, gl_mut_minus_im, gl_mut_bilinear))

    # ------------------------------------------------------------------------------ [9] v002 lines
    with open(V002_PATH, 'r', encoding='utf-8') as fh:
        v002_lines = fh.read().split('\n')
    V002_EXPECT = {
        39: " vol=np.sum(mesh['volume_weights_m3'],axis=1).reshape(n);wrho=vol*rho;gamma=5/3;im=1j*m",
        44: ' E=-KR[:,None]*UR-KZ[:,None]*UZ;PM=(gamma*P/rho)[:,None]*G+(rho**gamma)[:,None]*E',
        45: ' VR=im*W[:,None]*UR;VP=-(RR*WR)[:,None]*UR+im*W[:,None]*UP-(RR*WZ)[:,None]*UZ;VZ=im*W[:,None]*UZ',
        46: ' AR=im*W[:,None]*VR-2*W[:,None]*VP',
        47: ' AP=im*W[:,None]*VP+(2*W+RR*WR)[:,None]*VR+(RR*WZ)[:,None]*VZ',
        48: ' AZ=im*W[:,None]*VZ',
        49: ' divU=DR@UR+UR/RR[:,None]+im*UP/RR[:,None]+DZ@UZ',
        52: ' A=UR.conj().T@(wrho[:,None]*AR)+UP.conj().T@(wrho[:,None]*AP)+UZ.conj().T@(wrho[:,None]*AZ)',
        53: ' A-=divU.conj().T@(vol[:,None]*PM)',
        54: ' A-=(UR.conj().T*(vol*PR/rho)[None,:]+UZ.conj().T*(vol*PZ/rho)[None,:])@G',
        57: ' fr=DR@pot;fp=im*pot/RR;fz=DZ@pot',
        58: ' b=-(UR.conj().T@(wrho*fr)+UP.conj().T@(wrho*fp)+UZ.conj().T@(wrho*fz))',
    }
    v002_text_ok = all(v002_lines[ln - 1] == txt for ln, txt in V002_EXPECT.items())

    def v002_copy(kw):
        # Hand copy of v002 L44-48 and L52-54, L58 (verified above), with supplied inputs bound:
        # W=Omega, RR=R, WR=Omega_R, WZ=Omega_z, KR/KZ/PR/PZ supplied, vol=volume_weights,
        # wrho=vol*rho, im=1j*m, gamma=5/3, G/divU/fr/fp/fz supplied.  v002 itself is not run.
        W, RR_, WR, WZ = kw['Omega'], kw['R'], kw['Omega_R'], kw['Omega_z']
        KR, KZ, PR, PZ = kw['K_R'], kw['K_z'], kw['P_R'], kw['P_z']
        rho, P, vol = kw['rho'], kw['P'], kw['volume_weights']
        UR, UP, UZ, divU, G = kw['U_R'], kw['U_phi'], kw['U_z'], kw['divU'], kw['G']
        fr, fp, fz = kw['f_R'], kw['f_phi'], kw['f_z']
        wrho = vol * rho
        gamma = 5 / 3
        im = 1j * kw['m']
        E = -KR[:, None] * UR - KZ[:, None] * UZ; PM = (gamma * P / rho)[:, None] * G + (rho ** gamma)[:, None] * E  # noqa: E702
        VR = im * W[:, None] * UR; VP = -(RR_ * WR)[:, None] * UR + im * W[:, None] * UP - (RR_ * WZ)[:, None] * UZ; VZ = im * W[:, None] * UZ  # noqa: E702
        AR = im * W[:, None] * VR - 2 * W[:, None] * VP
        AP = im * W[:, None] * VP + (2 * W + RR_ * WR)[:, None] * VR + (RR_ * WZ)[:, None] * VZ
        AZ = im * W[:, None] * VZ
        A = UR.conj().T @ (wrho[:, None] * AR) + UP.conj().T @ (wrho[:, None] * AP) + UZ.conj().T @ (wrho[:, None] * AZ)
        A -= divU.conj().T @ (vol[:, None] * PM)
        A -= (UR.conj().T * (vol * PR / rho)[None, :] + UZ.conj().T * (vol * PZ / rho)[None, :]) @ G
        b = -(UR.conj().T @ (wrho * fr) + UP.conj().T @ (wrho * fp) + UZ.conj().T @ (wrho * fz))
        return dict(A=A, b=b, E=E, PM=PM, VR=VR, VP=VP, VZ=VZ)

    v2_err = 0.0
    for (npts, nf) in ((7, 3), (4, 4), (9, 1)):
        for seed in (90, 91):
            for m in range(1, 7):
                kw = rand_case(seed, npts, nf, m)
                r = ref(**kw)
                v2 = v002_copy(kw)
                ns = kw['normalization_scale']
                v2_err = max(v2_err, rel(v2['A'], r['A_unscaled']), rel(v2['b'], r['b_unscaled']),
                             max(rel(v2[k], r[k]) for k in ('E', 'PM', 'VR', 'VP', 'VZ')),
                             rel(v2['A'] / ns, r['A']))
    RESULT['v002'] = dict(line_text_matches=v002_text_ok, copy_vs_contract_reference=v2_err)
    print('[9] v002 lines 39,44-49,52-54,57,58 exact text present: %s ; hand-copied v002 contraction with '
          'supplied inputs vs H2 reference (A,b,maps): %.3e' % (v002_text_ok, v2_err))

    # ------------------------------------------------------------------------------ [10] H2 harness
    h2 = load_by_path('c4x_h2_harness', H2_HARNESS)
    t0 = time.time()
    res_ref = h2.run_reference_selfcheck(out_json=None)
    t1 = time.time()
    ser_ref = (json.dumps(h2._jsonable(res_ref), indent=1, allow_nan=False) + '\n').encode('utf-8')
    with open(H2_REF_JSON, 'rb') as fh:
        saved_ref = fh.read()
    st_ref = res_ref['f6_harness_selftest']['summary']
    rr = dict(seconds=round(t1 - t0, 2), summary_counts=res_ref['summary']['counts'],
              by_fixture=res_ref['summary']['by_fixture'], all_pass=res_ref['summary']['all_pass'],
              n_target_calls=res_ref['n_target_calls_F0_F5'],
              max_error_any_check=max([c['max_error'] for c in res_ref['checks']
                                       if isinstance(c.get('max_error'), float)] + [0.0]),
              f6_selftest={'n_probes': st_ref['n_probes'], 'reject': st_ref['reject'],
                           'accept': st_ref['accept'], 'record_only': st_ref['record_only'],
                           'failing_probes': st_ref['failing_probes']},
              serialized_sha256=hashlib.sha256(ser_ref).hexdigest(),
              byte_identical_to_saved=(ser_ref == saved_ref))
    RESULT['h2_reference_rerun'] = rr
    print('[10] H2 run_reference_selfcheck (in memory, %.2fs): counts %s, all_pass %s, %d target calls, '
          'max check error %.3e' % (rr['seconds'], rr['summary_counts'], rr['all_pass'], rr['n_target_calls'],
                                    rr['max_error_any_check']))
    print('[10]   F6 self-test: %d probes; reject %s; accept %s; record_only %s; failing %s'
          % (st_ref['n_probes'], st_ref['reject'], st_ref['accept'], st_ref['record_only'],
             st_ref['failing_probes']))
    print('[10]   serialization sha256 %s ; byte-identical to saved %s: %s'
          % (rr['serialized_sha256'], H2_REF_JSON.split('/')[-1], rr['byte_identical_to_saved']))
    t0 = time.time()
    res_mut = h2.run_mutation_study(out_json=None, verbose=False)
    t1 = time.time()
    ser_mut = (json.dumps(h2._jsonable(res_mut), indent=1, allow_nan=False) + '\n').encode('utf-8')
    with open(H2_MUT_JSON, 'rb') as fh:
        saved_mut = fh.read()
    min_fail = min(v for row in res_mut['mutations'] for v in row['detected_by_value_mismatch'].values()
                   if isinstance(v, float))
    mr = dict(seconds=round(t1 - t0, 2), summary=res_mut['summary'],
              control_counts=res_mut['control']['summary']['counts'],
              min_value_mismatch_on_failing_check=min_fail,
              serialized_sha256=hashlib.sha256(ser_mut).hexdigest(),
              byte_identical_to_saved=(ser_mut == saved_mut))
    RESULT['h2_mutation_rerun'] = mr
    print('[10] H2 run_mutation_study (in memory, %.2fs): %s ; control %s ; smallest failing-check value '
          'mismatch %.3e' % (mr['seconds'], mr['summary'], mr['control_counts'], min_fail))
    print('[10]   serialization sha256 %s ; byte-identical to saved %s: %s'
          % (mr['serialized_sha256'], H2_MUT_JSON.split('/')[-1], mr['byte_identical_to_saved']))
    # [10b] H2's "unsaved demonstration": the NON-validating vectorized control through F6, once with
    # the identity adapter and once behind a C4 keyword-renaming tuple adapter.
    demo = {}

    def renamed_target(**kw):
        back = dict(((k[2:] if k.startswith('x_') else k), v) for k, v in kw.items())
        return h2._transcription(None, **back)

    def to_renamed(kw):
        return dict(('x_' + k, v) for k, v in kw.items())

    for label, tgt, adp in (('identity_adapter', h2._make_transcription_target(None), None),
                            ('renaming_tuple_adapter', renamed_target, (to_renamed, None))):
        res = h2.run_all(tgt, adapter=adp, target_info={'label': 'C4X demo ' + label})
        s6 = res['f6_summary']
        demo[label] = dict(F0_F5_failures=[n for n in res['summary']['failures'] if not n.startswith('F6_')],
                           reject_n=s6['reject']['n'], reject_silently_accepted=s6['reject']['accepted'],
                           reject_rejected=s6['reject']['rejected'],
                           rejections_flagged_incidental=len(s6['rejections_flagged_incidental']),
                           accept_pass=s6['accept']['pass'], accept_n=s6['accept']['n'])
        print('[10b] non-validating control with F6 (%s): F0-F5 failures %s ; reject probes %d: silently '
              'accepted %d, rejected %d (incidental-flagged %d) ; accept probes %d/%d pass'
              % (label, demo[label]['F0_F5_failures'], s6['reject']['n'], s6['reject']['accepted'],
                 s6['reject']['rejected'], len(s6['rejections_flagged_incidental']), s6['accept']['pass'],
                 s6['accept']['n']))
    RESULT['h2_unsaved_demo_rerun'] = demo

    # ------------------------------------------------------------------------------ [11] C4 targets
    ctl = {}
    for label, tgt in (('c4_transcription', make_c4_target(None)),
                       ('contract_literal_eval', make_literal_target(compiled))):
        res = h2.run_all(tgt, skip=('F6',), target_info={'label': 'C4X control ' + label})
        ctl[label] = dict(counts=res['summary']['counts'], all_pass=res['summary']['all_pass'],
                          failures=res['summary']['failures'],
                          max_error_any_check=max([c['max_error'] for c in res['checks']
                                                   if isinstance(c.get('max_error'), float)] + [0.0]))
        print('[11] H2 run_all F0-F5 on C4 control %-22s counts %s all_pass %s max check error %.3e'
              % (label, ctl[label]['counts'], ctl[label]['all_pass'], ctl[label]['max_error_any_check']))
    RESULT['c4_controls_through_h2'] = ctl
    rows = []
    for mut in C4_MUTANTS:
        res = h2.run_all(make_c4_target(mut), skip=('F6',), target_info={'label': 'C4X mutant ' + mut})
        failed = [c for c in res['checks'] if c['status'] == 'fail']
        errored = [c for c in res['checks'] if c['status'] == 'error']
        vals = [c['max_error'] for c in failed if isinstance(c.get('max_error'), float)
                and math.isfinite(c['max_error'])]
        f1_failed = sum(1 for c in failed + errored if c['fixture'] == 'F1')
        rows.append(dict(mutation=mut, detected=bool(failed or errored), n_fail=len(failed),
                         n_error=len(errored), f1_checks_failing=f1_failed,
                         fixtures=sorted(set(c['fixture'] for c in failed + errored)),
                         min_finite_failing_value=(min(vals) if vals else None)))
    undetected = [r_['mutation'] for r_ in rows if not r_['detected']]
    RESULT['c4_mutants_through_h2'] = dict(n=len(rows), n_detected=len(rows) - len(undetected),
                                           undetected=undetected, rows=rows)
    print('[11] C4-only mutants through H2 run_all F0-F5: %d of %d detected; undetected %s'
          % (len(rows) - len(undetected), len(rows), undetected))
    for r_ in rows:
        print('[11]   %-30s detected %-5s fail %3d error %3d F1 %d/9 fixtures %-22s min failing value %s'
              % (r_['mutation'], r_['detected'], r_['n_fail'], r_['n_error'], r_['f1_checks_failing'],
                 ' '.join(r_['fixtures']),
                 ('%.3e' % r_['min_finite_failing_value']) if r_['min_finite_failing_value'] is not None else '-'))

    RESULT['seconds_total'] = round(time.time() - t_start, 2)
    print('RESULT_JSON ' + json.dumps(RESULT, sort_keys=True, default=str))


if __name__ == '__main__':
    main()

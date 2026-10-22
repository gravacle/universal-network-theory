import sys; sys.dont_write_bytecode=True; sys.path.append('/Users/bgm/Library/Python/3.9/lib/python/site-packages'); import numpy as np
# ---------------------------------------------------------------------------
# check_h1_oracle_v001.py -- Claude4 review lane (dispatch 0440, amended by
# 0441), local helper H1. REVIEW FIXTURE ONLY: synthetic arrays, numpy only,
# prints to stdout, writes no files, imports no project module, opens no
# project data. Reads the pinned contract JSON only to confirm its hash and
# equation text. Run:  /usr/bin/python3 -I -B check_h1_oracle_v001.py
# Sections:
#  [0] contract hash + equation text matches the transcription used here
#  [A] closed-form oracle vs plain inline contract chain (random complex)
#  [A2] broadcasting traps (missing [:,None]; square and nfree=1 cases)
#  [B] Lindblad determinant of the (R,phi) block of M_p
#  [C] 3-D Cartesian finite-difference check of delta v, delta a (unit-vector
#      derivatives, vertical shear) and linearized continuity
#  [D] weak-form identities by Gauss-Legendre quadrature (pressure by parts
#      under conjugation; 0438-style weak density)
#  [E] numpy FFT/16 modal convention (prior v002 L56-57)
#  [F] self-adjointness fixture: thermal-wind-consistent baroclinic background
#      with pointwise G = -div(rho U); mutant detection matrix
#  [G] global volume-weight scaling
# ---------------------------------------------------------------------------
import hashlib
import importlib.util
import json
import math

DIR = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/weak_euler_review_0440/'
ORACLE_PATH = DIR + 'algebra_oracle_h1v001.py'
SELF_PATH = DIR + 'check_h1_oracle_v001.py'
CONTRACT_PATH = ('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/'
                 'FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/ADDITIONAL_CLAUDE_WEAK_EULER_TASKS_V001.json')
CONTRACT_SHA = '5c30449de636b1f3da751d07ad90caafe964ed19444b0648df8fd9726ade9ebe'
GAMMA = 5.0 / 3.0

EXPECTED_EQUATIONS = [
    'E=-K_R[:,None]*U_R-K_z[:,None]*U_z',
    'PM=(gamma*P/rho)[:,None]*G+rho[:,None]**gamma*E',
    'VR=i*m*Omega[:,None]*U_R',
    'VP=-(R*Omega_R)[:,None]*U_R+i*m*Omega[:,None]*U_phi-(R*Omega_z)[:,None]*U_z',
    'VZ=i*m*Omega[:,None]*U_z',
    'AR=i*m*Omega[:,None]*VR-2*Omega[:,None]*VP',
    'AP=i*m*Omega[:,None]*VP+(2*Omega+R*Omega_R)[:,None]*VR+(R*Omega_z)[:,None]*VZ',
    'AZ=i*m*Omega[:,None]*VZ',
    'A=U_R^H diag(volume_weights*rho) AR + U_phi^H diag(volume_weights*rho) AP + '
    'U_z^H diag(volume_weights*rho) AZ - divU^H diag(volume_weights) PM - '
    '[U_R^H diag(volume_weights*P_R/rho)+U_z^H diag(volume_weights*P_z/rho)] G',
    'b=-U_R^H(volume_weights*rho*f_R)-U_phi^H(volume_weights*rho*f_phi)-U_z^H(volume_weights*rho*f_z)',
]


def sha256(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def load_oracle():
    spec = importlib.util.spec_from_file_location('algebra_oracle_h1v001', ORACLE_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def relmax(X, Y):
    return float(np.max(np.abs(np.asarray(X) - np.asarray(Y))) / np.max(np.abs(np.asarray(Y))))


def relfro(X, Y):
    return float(np.linalg.norm(np.asarray(X) - np.asarray(Y)) / np.linalg.norm(np.asarray(Y)))


def herm(A):
    """Relative anti-Hermitian part ||A - A^H||_F / ||A||_F."""
    return float(np.linalg.norm(A - A.conj().T) / np.linalg.norm(A))


def H(X):
    return X.conj().T


# ----------------------------------------------------------------- [A] chain
def contract_chain_plain(*, R, rho, P, K_R, K_z, P_R, P_z, Omega, Omega_R, Omega_z,
                         volume_weights, U_R, U_phi, U_z, divU, G, f_R, f_phi, f_z, m, gamma):
    """Plain inline transcription of the pinned contract chain (no mutation)."""
    i = 1j
    E = -K_R[:, None]*U_R - K_z[:, None]*U_z
    PM = (gamma*P/rho)[:, None]*G + rho[:, None]**gamma*E
    VR = i*m*Omega[:, None]*U_R
    VP = -(R*Omega_R)[:, None]*U_R + i*m*Omega[:, None]*U_phi - (R*Omega_z)[:, None]*U_z
    VZ = i*m*Omega[:, None]*U_z
    AR = i*m*Omega[:, None]*VR - 2*Omega[:, None]*VP
    AP = i*m*Omega[:, None]*VP + (2*Omega+R*Omega_R)[:, None]*VR + (R*Omega_z)[:, None]*VZ
    AZ = i*m*Omega[:, None]*VZ
    w = volume_weights
    A_inertial = (H(U_R) @ ((w*rho)[:, None]*AR) + H(U_phi) @ ((w*rho)[:, None]*AP)
                  + H(U_z) @ ((w*rho)[:, None]*AZ))
    A_pressure = -(H(divU) @ (w[:, None]*PM))
    A_density = -(H(U_R) @ ((w*P_R/rho)[:, None]*G) + H(U_z) @ ((w*P_z/rho)[:, None]*G))
    A = A_inertial + A_pressure + A_density
    b = -(H(U_R) @ (w*rho*f_R)) - (H(U_phi) @ (w*rho*f_phi)) - (H(U_z) @ (w*rho*f_z))
    return dict(A=A, b=b, E=E, PM=PM, VR=VR, VP=VP, VZ=VZ, AR=AR, AP=AP, AZ=AZ,
                A_inertial=A_inertial, A_pressure=A_pressure, A_density=A_density)


MUTANTS = [
    'no_test_conj', 'trial_conj', 'divU_unconj', 'minus_i_inertial',
    'E_sign', 'PM_no_gamma', 'PM_rho_not_rho_gamma',
    'VP_RR_sign', 'VP_Rz_sign', 'AR_coriolis_sign', 'AP_RR_sign', 'AP_Rz_sign',
    'pressure_sign', 'density_sign', 'density_rho2', 'rho_in_pressure',
    'vw_twice_inertial', 'no_vw_density', 'b_sign', 'f_phi_extra_im_over_R',
]


def chain_variant(d, mut):
    """Contract chain with ONE deliberate defect `mut` (None = unmutated)."""
    R = d['R']; rho = d['rho']; P = d['P']; K_R = d['K_R']; K_z = d['K_z']
    P_R = d['P_R']; P_z = d['P_z']; Om = d['Omega']; OmR = d['Omega_R']; Omz = d['Omega_z']
    w = d['volume_weights']; U_R = d['U_R']; U_phi = d['U_phi']; U_z = d['U_z']
    divU = d['divU']; G = d['G']; f_R = d['f_R']; f_phi = d['f_phi']; f_z = d['f_z']
    m = d['m']; gamma = d['gamma']; i = 1j
    if mut == 'trial_conj':
        U_R, U_phi, U_z, G = U_R.conj(), U_phi.conj(), U_z.conj(), G.conj()
    T = (lambda X: X.T) if mut == 'no_test_conj' else (lambda X: X.conj().T)
    Tdiv = (lambda X: X.T) if mut in ('no_test_conj', 'divU_unconj') else (lambda X: X.conj().T)
    im = -i*m if mut == 'minus_i_inertial' else i*m
    E = -K_R[:, None]*U_R - K_z[:, None]*U_z
    if mut == 'E_sign':
        E = -E
    cG = (P/rho) if mut == 'PM_no_gamma' else (gamma*P/rho)
    cE = rho if mut == 'PM_rho_not_rho_gamma' else rho**gamma
    PM = cG[:, None]*G + cE[:, None]*E
    VR = im*Om[:, None]*U_R
    sRR = 1.0 if mut == 'VP_RR_sign' else -1.0
    sRz = 1.0 if mut == 'VP_Rz_sign' else -1.0
    VP = sRR*(R*OmR)[:, None]*U_R + im*Om[:, None]*U_phi + sRz*(R*Omz)[:, None]*U_z
    VZ = im*Om[:, None]*U_z
    sCor = 2.0 if mut == 'AR_coriolis_sign' else -2.0
    AR = im*Om[:, None]*VR + sCor*Om[:, None]*VP
    cAP = (2*Om - R*OmR) if mut == 'AP_RR_sign' else (2*Om + R*OmR)
    sAPz = -1.0 if mut == 'AP_Rz_sign' else 1.0
    AP = im*Om[:, None]*VP + cAP[:, None]*VR + sAPz*(R*Omz)[:, None]*VZ
    AZ = im*Om[:, None]*VZ
    wi = w*w if mut == 'vw_twice_inertial' else w
    A = (T(U_R) @ ((wi*rho)[:, None]*AR) + T(U_phi) @ ((wi*rho)[:, None]*AP)
         + T(U_z) @ ((wi*rho)[:, None]*AZ))
    wp = w*rho if mut == 'rho_in_pressure' else w
    sP = 1.0 if mut == 'pressure_sign' else -1.0
    A = A + sP*(Tdiv(divU) @ (wp[:, None]*PM))
    rp = rho**2 if mut == 'density_rho2' else rho
    wd = np.ones_like(w) if mut == 'no_vw_density' else w
    sD = 1.0 if mut == 'density_sign' else -1.0
    A = A + sD*(T(U_R) @ ((wd*P_R/rp)[:, None]*G) + T(U_z) @ ((wd*P_z/rp)[:, None]*G))
    fphi = (i*m*f_phi/R) if mut == 'f_phi_extra_im_over_R' else f_phi
    sb = 1.0 if mut == 'b_sign' else -1.0
    b = sb*((T(U_R) @ (w*rho*f_R)) + (T(U_phi) @ (w*rho*fphi)) + (T(U_z) @ (w*rho*f_z)))
    return A, b


def cplx(rng, shape):
    # real and imaginary parts both O(1): substantial imaginary parts
    return rng.standard_normal(shape) + 1j*rng.standard_normal(shape)


def signed_uniform(rng, lo, hi, n):
    return rng.uniform(lo, hi, n)*rng.choice([-1.0, 1.0], n)


def random_inputs(rng, n, k, m):
    d = dict(R=rng.uniform(0.5, 3.0, n), rho=rng.uniform(0.2, 2.0, n), P=rng.uniform(0.1, 2.0, n),
             K_R=rng.standard_normal(n), K_z=rng.standard_normal(n),
             P_R=rng.standard_normal(n), P_z=rng.standard_normal(n),
             Omega=rng.uniform(0.3, 1.5, n), Omega_R=signed_uniform(rng, 0.2, 0.8, n),
             Omega_z=signed_uniform(rng, 0.2, 0.8, n), volume_weights=rng.uniform(0.1, 1.0, n))
    for name in ('U_R', 'U_phi', 'U_z', 'divU', 'G'):
        d[name] = cplx(rng, (n, k))
    for name in ('f_R', 'f_phi', 'f_z'):
        d[name] = cplx(rng, n)
    d['m'] = m
    d['gamma'] = GAMMA
    return d


def copy_inputs(d):
    return {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in d.items()}


def same_inputs(d, e):
    for k in d:
        if isinstance(d[k], np.ndarray):
            if not (d[k].dtype == e[k].dtype and np.array_equal(d[k], e[k])):
                return False
        elif d[k] != e[k]:
            return False
    return True


# -------------------------------------------------------- [C] 3-D helpers
def pev(c, R, z):
    out = 0j
    for a in range(c.shape[0]):
        for bb in range(c.shape[1]):
            if c[a, bb] != 0:
                out = out + c[a, bb]*R**a*z**bb
    return out


def pdR(c):
    d = np.zeros_like(c)
    for a in range(1, c.shape[0]):
        d[a-1, :] = a*c[a, :]
    return d


def pdz(c):
    d = np.zeros_like(c)
    for bb in range(1, c.shape[1]):
        d[:, bb-1] = bb*c[:, bb]
    return d


# complex polynomial coefficients c[a, b] of R^a z^b (synthetic, generic)
CUR = np.array([[0.7+0.4j, 0.3+0.1j, 0.1-0.2j], [0.2-0.5j, -0.2+0.3j, 0.0], [-0.15+0.05j, 0.0, 0.0]])
CUP = np.array([[-0.4+0.6j, -0.1+0.4j, 0.05+0.1j], [0.3+0.2j, 0.12-0.2j, 0.0], [0.25-0.1j, 0.0, 0.0]])
CUZ = np.array([[0.5-0.3j, 0.4+0.2j, -0.1+0.05j], [-0.2+0.1j, 0.1+0.3j, 0.0], [0.05-0.15j, 0.0, 0.0]])


# On the sampled domain R in [0.7,1.8], z in [-0.4,0.4]: Omega in [0.98,1.46],
# Omega_R in [0.23,0.27] and Omega_z in [-0.345,-0.13] (bounded away from 0).
def Om_f(R, z):
    return 0.9 + 0.25*R - 0.3*z + 0.05*R*z + 0.1*z*z


def OmR_f(R, z):
    return 0.25 + 0.05*z


def Omz_f(R, z):
    return -0.3 + 0.05*R + 0.2*z


def rho0_f(R, z):
    return 1.2 + 0.3*R - 0.2*z + 0.1*R*z


def rho0R_f(R, z):
    return 0.3 + 0.1*z


def rho0z_f(R, z):
    return -0.2 + 0.1*R


def cyl(p):
    x, y, z = float(p[0]), float(p[1]), float(p[2])
    return math.hypot(x, y), math.atan2(y, x), z


def frame(phi):
    c, s = math.cos(phi), math.sin(phi)
    return np.array([c, s, 0.0]), np.array([-s, c, 0.0]), np.array([0.0, 0.0, 1.0])


def to_cart(cR, cP, cZ, phi, m, phase):
    eR, eP, eZ = frame(phi)
    amp = phase*complex(math.cos(m*phi), math.sin(m*phi))  # exp(+i m phi)
    return np.real((cR*eR + cP*eP + cZ*eZ)*amp)


def modal_U(R, z):
    return pev(CUR, R, z), pev(CUP, R, z), pev(CUZ, R, z)


def modal_V(R, z, m, mut=None):
    UR, UP, UZ = modal_U(R, z)
    O, OR, OZ, im = Om_f(R, z), OmR_f(R, z), Omz_f(R, z), 1j*m
    sz = 1.0 if mut == 'VP_Rz_sign' else -1.0
    sr = 1.0 if mut == 'VP_RR_sign' else -1.0
    return im*O*UR, sr*R*OR*UR + im*O*UP + sz*R*OZ*UZ, im*O*UZ


def modal_A(R, z, m, mut=None):
    VR, VP, VZ = modal_V(R, z, m)
    O, OR, OZ, im = Om_f(R, z), OmR_f(R, z), Omz_f(R, z), 1j*m
    s = -1.0 if mut == 'AP_Rz_sign' else 1.0
    c = -2.0 if mut != 'AR_coriolis_sign' else 2.0
    return im*O*VR + c*O*VP, im*O*VP + (2*O + R*OR)*VR + s*R*OZ*VZ, im*O*VZ


def modal_drho(R, z, m):
    UR, UP, UZ = modal_U(R, z)
    r, rR, rz = rho0_f(R, z), rho0R_f(R, z), rho0z_f(R, z)
    dURR = pev(pdR(CUR), R, z)
    dUZz = pev(pdz(CUZ), R, z)
    return -(r*UR/R + rR*UR + r*dURR) - 1j*m*r*UP/R - (rz*UZ + r*dUZz)


def ddir(F, p, a, h):
    """4th-order central difference of F along direction a at p."""
    return (F(p - 2*h*a) - 8*F(p - h*a) + 8*F(p + h*a) - F(p + 2*h*a))/(12*h)


def make_fields(m, phase, vmut=None):
    def xi(p):
        R, phi, z = cyl(p)
        return to_cart(*modal_U(R, z), phi, m, phase)

    def v0(p):
        R, phi, z = cyl(p)
        return Om_f(R, z)*np.array([-float(p[1]), float(p[0]), 0.0])

    def dv(p):
        R, phi, z = cyl(p)
        return to_cart(*modal_V(R, z, m, vmut), phi, m, phase)

    def drho(p):
        R, phi, z = cyl(p)
        return float(np.real(modal_drho(R, z, m)*phase*complex(math.cos(m*phi), math.sin(m*phi))))

    def rho_dv(p):
        R, phi, z = cyl(p)
        return rho0_f(R, z)*dv(p)
    return xi, v0, dv, drho, rho_dv


# --------------------------------------------------- [F] consistent fixture
def consistent_baroclinic_inputs(rng, n, k, m):
    """Pointwise background with P = K rho^gamma, consistent gradients, the
    thermal-wind relation 2 R Om Om_z = (P_z rho_R - P_R rho_z)/rho^2 and the
    pointwise conservative density G = -(rho divU + rho_R U_R + rho_z U_z)."""
    g = GAMMA
    rho = rng.uniform(0.3, 2.0, n)
    rho_R = rng.standard_normal(n)
    rho_z = rng.standard_normal(n)
    K = rng.uniform(0.5, 2.0, n)
    K_R = rng.standard_normal(n)
    K_z = rng.standard_normal(n)
    P = K*rho**g
    P_R = rho**g*K_R + g*P/rho*rho_R
    P_z = rho**g*K_z + g*P/rho*rho_z
    R = rng.uniform(0.5, 3.0, n)
    Omega = rng.uniform(0.3, 1.5, n)
    Omega_R = signed_uniform(rng, 0.2, 0.8, n)
    Omega_z = (P_z*rho_R - P_R*rho_z)/(2*rho**2*R*Omega)
    U_R, U_phi, U_z, divU = cplx(rng, (n, k)), cplx(rng, (n, k)), cplx(rng, (n, k)), cplx(rng, (n, k))
    G = -(rho[:, None]*divU + rho_R[:, None]*U_R + rho_z[:, None]*U_z)
    d = dict(R=R, rho=rho, P=P, K_R=K_R, K_z=K_z, P_R=P_R, P_z=P_z, Omega=Omega,
             Omega_R=Omega_R, Omega_z=Omega_z, volume_weights=rng.uniform(0.1, 1.0, n),
             U_R=U_R, U_phi=U_phi, U_z=U_z, divU=divU, G=G,
             f_R=cplx(rng, n), f_phi=cplx(rng, n), f_z=cplx(rng, n), m=m, gamma=g)
    return d


def main():
    print('H1 check script sha256 (runtime):', sha256(SELF_PATH))
    print('H1 oracle sha256 (runtime):      ', sha256(ORACLE_PATH))
    print('numpy', np.__version__, '| python', sys.version.split()[0])

    # ------------------------------------------------------------------ [0]
    csha = sha256(CONTRACT_PATH)
    with open(CONTRACT_PATH, 'r', encoding='utf-8') as fh:
        contract = json.load(fh)
    eqs = [s.replace('−', '-') for s in contract['author_task']['equations']]
    print('[0] contract sha256 matches pin:', csha == CONTRACT_SHA)
    print('[0] contract equations 1..10 (unicode minus -> ASCII) equal transcription:',
          eqs[:10] == EXPECTED_EQUATIONS)

    oracle = load_oracle()

    # ------------------------------------------------------------------ [A]
    worst = dict(A=0.0, A_fro=0.0, b=0.0, Mp=0.0)
    sens_shear = 1e300
    sens_imag = 1e300
    no_mutation = True
    ncase = 0
    seeds = list(range(6))
    shapes = [(7, 3), (4, 4)]
    for seed in seeds:
        for (n, k) in shapes:
            for m in range(1, 7):
                rng = np.random.default_rng([20261016, seed, n, k, m])
                d = random_inputs(rng, n, k, m)
                d0 = copy_inputs(d)
                ref = contract_chain_plain(**d)
                Ao, bo = oracle.oracle_A_b(**d)
                no_mutation = no_mutation and same_inputs(d, d0)
                worst['A'] = max(worst['A'], relmax(Ao, ref['A']))
                worst['A_fro'] = max(worst['A_fro'], relfro(Ao, ref['A']))
                worst['b'] = max(worst['b'], relmax(bo, ref['b']))
                Mp = oracle.pointwise_inertial_matrix(R=d['R'], Omega=d['Omega'], Omega_R=d['Omega_R'],
                                                      Omega_z=d['Omega_z'], m=m)
                U = np.stack([d['U_R'], d['U_phi'], d['U_z']], axis=1)
                MU = np.einsum('nab,nbk->nak', Mp, U, optimize=False)
                chainA = np.stack([ref['AR'], ref['AP'], ref['AZ']], axis=1)
                worst['Mp'] = max(worst['Mp'], relmax(MU, chainA))
                e = copy_inputs(d)
                e['Omega_z'] = np.zeros(n)
                sens_shear = min(sens_shear, relmax(contract_chain_plain(**e)['A'], ref['A']))
                At = (d['U_R'].T @ ((d['volume_weights']*d['rho'])[:, None]*ref['AR'])
                      + d['U_phi'].T @ ((d['volume_weights']*d['rho'])[:, None]*ref['AP'])
                      + d['U_z'].T @ ((d['volume_weights']*d['rho'])[:, None]*ref['AZ']))
                sens_imag = min(sens_imag, relmax(At, ref['A_inertial']))
                ncase += 1
    print('[A] cases: %d (seeds %s, shapes %s, m=1..6)' % (ncase, seeds, shapes))
    print('[A] max rel err (max-abs) oracle A vs contract chain: %.3e' % worst['A'])
    print('[A] max rel err (Frobenius) oracle A vs contract chain: %.3e' % worst['A_fro'])
    print('[A] max rel err (max-abs) oracle b vs contract chain: %.3e' % worst['b'])
    print('[A] max rel err pointwise M_p U vs chain (AR,AP,AZ): %.3e' % worst['Mp'])
    print('[A] min sensitivity of A to Omega_z (rel change when Omega_z->0): %.3e' % sens_shear)
    print('[A] min sensitivity of inertial A to test-side conjugation: %.3e' % sens_imag)
    print('[A] oracle left all inputs unmodified:', no_mutation)

    # ----------------------------------------------------------------- [A2]
    def vr_missing_none(d):
        e = dict(d)
        out = contract_chain_plain(**e)
        i = 1j
        VR_bad = i*d['m']*d['Omega']*d['U_R']           # missing [:,None]
        VP = out['VP']
        AR_bad = i*d['m']*d['Omega'][:, None]*VR_bad - 2*d['Omega'][:, None]*VP
        w = d['volume_weights']
        A_bad = (H(d['U_R']) @ ((w*d['rho'])[:, None]*AR_bad) + H(d['U_phi']) @ ((w*d['rho'])[:, None]*out['AP'])
                 + H(d['U_z']) @ ((w*d['rho'])[:, None]*out['AZ'])) + out['A_pressure'] + out['A_density']
        return A_bad, out['A']
    for (n, k) in [(7, 3), (4, 4), (7, 1)]:
        rng = np.random.default_rng([4040, n, k])
        d = random_inputs(rng, n, k, 3)
        try:
            A_bad, A_ok = vr_missing_none(d)
            if A_bad.shape != A_ok.shape:
                print('[A2] VR missing [:,None], shape (%d,%d): runs silently, A shape %s instead of %s'
                      % (n, k, A_bad.shape, A_ok.shape))
            else:
                print('[A2] VR missing [:,None], shape (%d,%d): runs silently, rel err %.3e'
                      % (n, k, relmax(A_bad, A_ok)))
        except ValueError as exc:
            print('[A2] VR missing [:,None], shape (%d,%d): raises ValueError (%s)' % (n, k, str(exc)[:60]))
    for (n, k) in [(7, 3), (4, 4)]:
        rng = np.random.default_rng([4041, n, k])
        d = random_inputs(rng, n, k, 2)
        ref = contract_chain_plain(**d)
        w = d['volume_weights']
        try:
            bad = H(d['divU']) @ (w*ref['PM'])               # weight broadcast along columns
            print('[A2] pressure weight missing [:,None], shape (%d,%d): runs silently, rel err %.3e'
                  % (n, k, relmax(-bad, ref['A_pressure'])))
        except ValueError as exc:
            print('[A2] pressure weight missing [:,None], shape (%d,%d): raises ValueError (%s)'
                  % (n, k, str(exc)[:60]))
        ok = -(H(d['divU'])*w) @ ref['PM']                   # U^H * w broadcasts along points: correct
        print('[A2] U^H * w (row vector over points), shape (%d,%d): rel err %.3e (correct form)'
              % (n, k, relmax(ok, ref['A_pressure'])))

    # ------------------------------------------------------------------ [B]
    rng = np.random.default_rng(7)
    wl = 0.0
    for m in range(1, 7):
        R = rng.uniform(0.5, 3.0, 16); O = rng.uniform(0.3, 1.5, 16)
        OR = signed_uniform(rng, 0.2, 0.8, 16); OZ = signed_uniform(rng, 0.2, 0.8, 16)
        Mp = oracle.pointwise_inertial_matrix(R=R, Omega=O, Omega_R=OR, Omega_z=OZ, m=m)
        det = Mp[:, 0, 0]*Mp[:, 1, 1] - Mp[:, 0, 1]*Mp[:, 1, 0]
        kappa2 = 4*O**2 + 2*R*O*OR
        wl = max(wl, relmax(det, m*m*O**2*(m*m*O**2 - kappa2)))
    print('[B] det of (R,phi) block of M_p vs m^2 Om^2 (m^2 Om^2 - kappa^2): max rel err %.3e' % wl)

    # ------------------------------------------------------------------ [C]
    rng = np.random.default_rng(11)
    pts = []
    for _ in range(5):
        R = rng.uniform(0.7, 1.8); phi = rng.uniform(-math.pi, math.pi); z = rng.uniform(-0.4, 0.4)
        pts.append(np.array([R*math.cos(phi), R*math.sin(phi), z]))
    h = 5e-4
    ev = ea = ec = 0.0
    mut_v = mut_vRR = mut_a = mut_cor = mut_c = 1e300
    axes = (np.array([1.0, 0, 0]), np.array([0, 1.0, 0]), np.array([0, 0, 1.0]))
    nrm = np.linalg.norm
    for m in range(1, 7):
        fields = [(phase, make_fields(m, phase), make_fields(m, phase, 'VP_Rz_sign'))
                  for phase in (1.0+0j, 1j)]
        for p in pts:
            R, phi, z = cyl(p)
            # Stack the phase-1 and phase-i real fields: together they carry the
            # full complex modal amplitude, so a real-part null cannot hide a term.
            acc = {key: [] for key in ('vfd', 'vmod', 'vm', 'vm2', 'afd', 'amod', 'am', 'am2', 'acl',
                                       'cres', 'csc', 'cmut')}
            Mp = oracle.pointwise_inertial_matrix(R=[R], Omega=[Om_f(R, z)], Omega_R=[OmR_f(R, z)],
                                                  Omega_z=[Omz_f(R, z)], m=m)[0]
            aclosed = Mp @ np.array(modal_U(R, z))
            for phase, (xi, v0, dv, drho, rho_dv), (_, _, _, _, rho_dv_mut) in fields:
                acc['vfd'].append(ddir(xi, p, v0(p), h) - ddir(v0, p, xi(p), h))
                acc['vmod'].append(dv(p))
                acc['vm'].append(to_cart(*modal_V(R, z, m, 'VP_Rz_sign'), phi, m, phase))
                acc['vm2'].append(to_cart(*modal_V(R, z, m, 'VP_RR_sign'), phi, m, phase))
                acc['afd'].append(ddir(dv, p, v0(p), h) + ddir(v0, p, dv(p), h))
                acc['amod'].append(to_cart(*modal_A(R, z, m), phi, m, phase))
                acc['am'].append(to_cart(*modal_A(R, z, m, 'AP_Rz_sign'), phi, m, phase))
                acc['am2'].append(to_cart(*modal_A(R, z, m, 'AR_coriolis_sign'), phi, m, phase))
                acc['acl'].append(to_cart(*aclosed, phi, m, phase))
                div = sum(ddir(lambda q, kk=kk: rho_dv(q)[kk], p, axes[kk], h) for kk in range(3))
                adv = ddir(drho, p, v0(p), h)
                divm = sum(ddir(lambda q, kk=kk: rho_dv_mut(q)[kk], p, axes[kk], h) for kk in range(3))
                acc['cres'].append(div + adv)
                acc['csc'].append(max(abs(div), abs(adv)))
                acc['cmut'].append(divm + adv)
            st = {key: np.concatenate([np.atleast_1d(np.asarray(v, dtype=float)) for v in val])
                  for key, val in acc.items()}
            ev = max(ev, nrm(st['vfd'] - st['vmod'])/nrm(st['vmod']))
            mut_v = min(mut_v, nrm(st['vfd'] - st['vm'])/nrm(st['vmod']))
            mut_vRR = min(mut_vRR, nrm(st['vfd'] - st['vm2'])/nrm(st['vmod']))
            ea = max(ea, nrm(st['afd'] - st['amod'])/nrm(st['amod']), nrm(st['afd'] - st['acl'])/nrm(st['amod']))
            mut_a = min(mut_a, nrm(st['afd'] - st['am'])/nrm(st['amod']))
            mut_cor = min(mut_cor, nrm(st['afd'] - st['am2'])/nrm(st['amod']))
            ec = max(ec, nrm(st['cres'])/nrm(st['csc']))
            mut_c = min(mut_c, nrm(st['cmut'])/nrm(st['csc']))
    print('[C] FD delta v = (v0.grad)xi - (xi.grad)v0 vs contract VR,VP,VZ: max rel err %.3e' % ev)
    print('[C]   mutant VP +R*Omega_z*U_z: min rel deviation %.3e' % mut_v)
    print('[C]   mutant VP +R*Omega_R*U_R: min rel deviation %.3e' % mut_vRR)
    print('[C] FD delta a = (v0.grad)dv + (dv.grad)v0 vs contract AR,AP,AZ and closed M_p: max rel err %.3e' % ea)
    print('[C]   mutant AP -R*Omega_z*VZ: min rel deviation %.3e' % mut_a)
    print('[C]   mutant AR +2*Omega*VP: min rel deviation %.3e' % mut_cor)
    print('[C] FD continuity div(rho0 dv) + v0.grad(drho), drho=-div(rho0 xi): max rel residual %.3e' % ec)
    print('[C]   mutant VP +R*Omega_z*U_z: min rel residual %.3e' % mut_c)

    # ------------------------------------------------------------------ [D]
    xg, wg = np.polynomial.legendre.leggauss(24)
    Rq = 1.5 + 0.5*xg; wR = 0.5*wg; zq = xg.copy(); wz = wg.copy()
    RR = Rq[:, None]*np.ones(zq.size)[None, :]
    ZZ = np.ones(Rq.size)[:, None]*zq[None, :]
    dA = (wR[:, None]*wz[None, :])*RR          # R dR dz quadrature on [1,2]x[-1,1]
    s = (RR - 1)*(2 - RR); sp = 3 - 2*RR; t = 1 - ZZ*ZZ; tp = -2*ZZ
    CQ = np.array([[0.4-0.9j, 0.3+0.2j, -0.1+0.1j], [-0.6+0.3j, 0.2-0.4j, 0.0], [0.15+0.2j, 0.0, 0.0]])
    Q, QR, Qz = pev(CQ, RR, ZZ), pev(pdR(CQ), RR, ZZ), pev(pdz(CQ), RR, ZZ)
    B = s*s*t*t; BR = 2*s*sp*t*t; Bz = s*s*2*t*tp
    dP, dP_R, dP_z = B*Q, BR*Q + B*QR, Bz*Q + B*Qz
    UR, UP, UZ = pev(CUR, RR, ZZ), pev(CUP, RR, ZZ), pev(CUZ, RR, ZZ)
    dURR, dUZz = pev(pdR(CUR), RR, ZZ), pev(pdz(CUZ), RR, ZZ)
    u = 1 + 0.3*RR + 0.2*ZZ
    rho = s*t*u; rho_R = sp*t*u + s*t*0.3; rho_z = s*tp*u + s*t*0.2
    CPSI = np.array([[0.3+0.5j, -0.2+0.1j, 0.1+0.0j], [0.4-0.2j, 0.1+0.3j, 0.0], [-0.1+0.2j, 0.0, 0.0]])
    worst_p = worst_rho = 0.0
    min_mut_p = min_mut_bil = min_mut_rho = 1e300
    for m in range(1, 7):
        im = 1j*m
        LR = np.sum(dA*np.conj(UR)*dP_R); RRt = -np.sum(dA*np.conj(dURR + UR/RR)*dP)
        Lp = np.sum(dA*np.conj(UP)*(im*dP/RR)); Rp = -np.sum(dA*np.conj(im*UP/RR)*dP)
        Lz = np.sum(dA*np.conj(UZ)*dP_z); Rz = -np.sum(dA*np.conj(dUZz)*dP)
        L = LR + Lp + Lz; Rt = RRt + Rp + Rz
        sc = max(abs(LR), abs(Lp), abs(Lz))
        worst_p = max(worst_p, abs(LR - RRt)/sc, abs(Lp - Rp)/sc, abs(Lz - Rz)/sc, abs(L - Rt)/sc)
        Rp_mut = -np.sum(dA*np.conj(-im*UP/RR)*dP)       # divU with -i m U_phi/R
        min_mut_p = min(min_mut_p, abs(L - (RRt + Rp_mut + Rz))/sc)
        Lb = np.sum(dA*(UR*dP_R + UP*im*dP/RR + UZ*dP_z))  # no conjugation at all
        Rb = -np.sum(dA*(dURR + UR/RR + im*UP/RR + dUZz)*dP)
        min_mut_bil = min(min_mut_bil, abs(Lb - Rb)/sc)
        drho = -(rho*UR/RR + rho_R*UR + rho*dURR) - im*rho*UP/RR - (rho_z*UZ + rho*dUZz)
        for label, cps in (('complex psi', CPSI), ('real psi', np.real(CPSI).astype(complex))):
            psi, psiR, psiz = pev(cps, RR, ZZ), pev(pdR(cps), RR, ZZ), pev(pdz(cps), RR, ZZ)
            Ld = np.sum(dA*np.conj(psi)*drho)
            t1 = np.sum(dA*np.conj(psiR)*rho*UR); t2 = np.sum(dA*(-im)*np.conj(psi)*rho*UP/RR)
            t3 = np.sum(dA*np.conj(psiz)*rho*UZ)
            sc2 = max(abs(t1), abs(t2), abs(t3))
            worst_rho = max(worst_rho, abs(Ld - (t1 + t2 + t3))/sc2)
            min_mut_rho = min(min_mut_rho, abs(Ld - (t1 - t2 + t3))/sc2)
    print('[D] pressure by parts: int conj(U).grad(dP) = -int conj(divU) dP, per component and total:'
          ' max rel err %.3e' % worst_p)
    print('[D]   mutant divU with -i m U_phi/R: min rel mismatch %.3e' % min_mut_p)
    print('[D]   mutant bilinear (no conjugation): min rel mismatch %.3e' % min_mut_bil)
    print('[D] weak density: int conj(psi) drho = int[conj(psi_R) rho U_R - i m conj(psi) rho U_phi/R'
          ' + conj(psi_z) rho U_z]: max rel err %.3e' % worst_rho)
    print('[D]   mutant +i m in phi term: min rel mismatch %.3e' % min_mut_rho)

    # ------------------------------------------------------------------ [E]
    N = 16
    c, c2, c0 = 0.3-0.7j, -0.2+0.45j, 0.8
    for label, phi in (('phi_n = 2 pi n/16', 2*np.pi*np.arange(N)/N),
                       ('phi_n = 2 pi (n+1/2)/16', 2*np.pi*(np.arange(N) + 0.5)/N)):
        e1 = e2 = e3 = 0.0
        for m in range(1, 7):
            m2 = m + 1
            Phi = c0 + 2*np.real(c*np.exp(1j*m*phi)) + 2*np.real(c2*np.exp(1j*m2*phi))
            dPhi = 2*np.real(1j*m*c*np.exp(1j*m*phi)) + 2*np.real(1j*m2*c2*np.exp(1j*m2*phi))
            pot = np.fft.fft(Phi)/16; dpot = np.fft.fft(dPhi)/16
            e1 = max(e1, abs(pot[m] - c*np.exp(1j*m*phi[0]))/abs(c))
            e2 = max(e2, abs(dpot[m] - 1j*m*pot[m])/abs(m*pot[m]))
            e3 = max(e3, abs(pot[N - m] - np.conj(pot[m]))/abs(c))
        print('[E] %s: |fft/16[m] - c e^{i m phi_0}|/|c| %.2e ; |fft/16(dPhi/dphi)[m] - i m fft/16[m]| rel %.2e ;'
              ' fft/16[16-m] = conj %.2e' % (label, e1, e2, e3))

    # ------------------------------------------------------------------ [F]
    hfull = hin = hpd = hinc_shear = hinc_G = 0.0
    hin_min = hpd_min = hinc_shear_min = hinc_G_min = 1e300
    detect = {mu: [1e300, 1e300, 1e300] for mu in MUTANTS}   # [oracle A, oracle b, Hermiticity]
    base_dev = 0.0
    for seed in range(3):
        for (n, k) in [(9, 4), (5, 5)]:
            for m in range(1, 7):
                rng = np.random.default_rng([515, seed, n, k, m])
                d = consistent_baroclinic_inputs(rng, n, k, m)
                ref = contract_chain_plain(**d)
                parts = oracle.oracle_parts(**d)
                hfull = max(hfull, herm(ref['A']))
                hfull = max(hfull, herm(parts['A']))
                hi = herm(ref['A_inertial']); hp = herm(ref['A_pressure'] + ref['A_density'])
                hin = max(hin, hi); hpd = max(hpd, hp)
                hin_min = min(hin_min, hi); hpd_min = min(hpd_min, hp)
                e = copy_inputs(d)
                e['Omega_z'] = signed_uniform(rng, 0.2, 0.8, n)          # shear not thermal-wind consistent
                hx = herm(contract_chain_plain(**e)['A'])
                hinc_shear = max(hinc_shear, hx); hinc_shear_min = min(hinc_shear_min, hx)
                e = copy_inputs(d)
                e['G'] = cplx(rng, (n, k))                               # G not = -div(rho U) pointwise
                hx = herm(contract_chain_plain(**e)['A'])
                hinc_G = max(hinc_G, hx); hinc_G_min = min(hinc_G_min, hx)
                A0, b0 = chain_variant(d, None)
                base_dev = max(base_dev, relmax(A0, ref['A']), relmax(b0, ref['b']))
                rnd = random_inputs(np.random.default_rng([616, seed, n, k, m]), n, k, m)
                Ao, bo = oracle.oracle_A_b(**rnd)
                for mu in MUTANTS:
                    Am, bm = chain_variant(rnd, mu)
                    detect[mu][0] = min(detect[mu][0], relmax(Am, Ao))
                    detect[mu][1] = min(detect[mu][1], relmax(bm, bo))
                    Amc, _ = chain_variant(d, mu)
                    detect[mu][2] = min(detect[mu][2], herm(Amc))
    print('[F] thermal-wind-consistent fixture (P=K rho^g, consistent gradients, pointwise G):')
    print('[F]   full contract A (chain and oracle): max ||A-A^H||/||A|| = %.3e' % hfull)
    print('[F]   inertial part alone: anti-Hermitian rel norm in [%.3e, %.3e]' % (hin_min, hin))
    print('[F]   pressure+density part alone: anti-Hermitian rel norm in [%.3e, %.3e]' % (hpd_min, hpd))
    print('[F]   Omega_z replaced by inconsistent values: full A anti-Hermitian in [%.3e, %.3e]'
          % (hinc_shear_min, hinc_shear))
    print('[F]   G replaced by non-pointwise map: full A anti-Hermitian in [%.3e, %.3e]' % (hinc_G_min, hinc_G))
    print('[F]   unmutated chain_variant vs plain chain: max rel dev %.3e' % base_dev)
    print('[F] mutant detection (min over 36 cases each): oracle-A dev | oracle-b dev | Hermiticity on consistent fixture')
    for mu in MUTANTS:
        a_, b_, h_ = detect[mu]
        print('[F]   %-24s %.3e | %.3e | %.3e' % (mu, a_, b_, h_))

    # ------------------------------------------------------------------ [G]
    rng = np.random.default_rng(99)
    gs = 0.0
    for (n, k) in [(7, 3), (4, 4)]:
        d = random_inputs(rng, n, k, 4)
        e = copy_inputs(d)
        e['volume_weights'] = 2*np.pi*d['volume_weights']
        A1, b1 = oracle.oracle_A_b(**d); A2, b2 = oracle.oracle_A_b(**e)
        r1 = contract_chain_plain(**d); r2 = contract_chain_plain(**e)
        gs = max(gs, relmax(A2, 2*np.pi*A1), relmax(b2, 2*np.pi*b1),
                 relmax(r2['A'], 2*np.pi*r1['A']), relmax(r2['b'], 2*np.pi*r1['b']))
        same_maps = all(np.array_equal(r1[key], r2[key]) for key in ('E', 'PM', 'VR', 'VP', 'VZ'))
        print('[G] shape (%d,%d): maps E,PM,VR,VP,VZ independent of volume_weights: %s' % (n, k, same_maps))
    print('[G] volume_weights -> 2 pi volume_weights scales A and b by exactly 2 pi: max rel dev %.3e' % gs)


if __name__ == '__main__':
    main()

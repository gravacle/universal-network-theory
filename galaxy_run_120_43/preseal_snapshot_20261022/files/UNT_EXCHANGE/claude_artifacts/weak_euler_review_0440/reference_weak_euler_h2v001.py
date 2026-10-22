import sys; sys.dont_write_bytecode=True; sys.path.append('/Users/bgm/Library/Python/3.9/lib/python/site-packages'); import numpy as np
# reference_weak_euler_h2v001.py -- Claude4 review lane (dispatch 0440, amended by 0441), helper H2.
#
# Independent, deliberately UNVECTORIZED reference transcription of the pinned root contract
#   /Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/ADDITIONAL_CLAUDE_WEAK_EULER_TASKS_V001.json
#   SHA256 5c30449de636b1f3da751d07ad90caafe964ed19444b0648df8fd9726ade9ebe
# section author_task.equations, unicode minus (U+2212) normalized to ASCII '-'.
#
# Role: test oracle for fixtures_weak_euler_h2v001.py only.
#   * Explicit Python loops over points p and columns j, k with Python complex scalars.
#     No [:,None] broadcasting, no matrix products, no numpy array arithmetic.
#     numpy is used only to package the final lists as complex128 arrays.
#   * Performs NO input validation; the harness owns validation expectations (fixture F6).
#   * No solve, inverse, pseudoinverse, clipping, ridge, tolerance or acceptance.
#   * Not a project module; selects no physics; outputs are not_assessed physically.
#   * provenance is accepted and unused (the contract requires it to be supplied; it has no
#     numerical role in any equation).

CONTRACT_PATH = ('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/'
                 'FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/ADDITIONAL_CLAUDE_WEAK_EULER_TASKS_V001.json')
CONTRACT_SHA256 = '5c30449de636b1f3da751d07ad90caafe964ed19444b0648df8fd9726ade9ebe'

CANONICAL_INPUTS = ('R', 'rho', 'P', 'K_R', 'K_z', 'P_R', 'P_z', 'Omega', 'Omega_R', 'Omega_z',
                    'volume_weights', 'U_R', 'U_phi', 'U_z', 'divU', 'G', 'f_R', 'f_phi', 'f_z',
                    'm', 'gamma', 'normalization_scale', 'provenance')
CANONICAL_OUTPUTS = ('A', 'b', 'E', 'PM', 'VR', 'VP', 'VZ')


def _conj(z):
    """Complex conjugate of one Python complex scalar (the ^H factor on the test side)."""
    return complex(z.real, -z.imag)


def reference_assemble(*, R, rho, P, K_R, K_z, P_R, P_z, Omega, Omega_R, Omega_z,
                       volume_weights, U_R, U_phi, U_z, divU, G, f_R, f_phi, f_z,
                       m, gamma, normalization_scale, provenance):
    """Return dict(A, b, E, PM, VR, VP, VZ, A_unscaled, b_unscaled) per the pinned contract.

    A and b are divided by normalization_scale; E, PM, VR, VP, VZ are the exact unscaled maps.
    """
    npoints = len(R)
    nfree = len(U_R[0])
    i = 1j

    # Pointwise real coefficients as plain Python floats.
    Rs = [float(R[p]) for p in range(npoints)]
    rhos = [float(rho[p]) for p in range(npoints)]
    Ps = [float(P[p]) for p in range(npoints)]
    KRs = [float(K_R[p]) for p in range(npoints)]
    Kzs = [float(K_z[p]) for p in range(npoints)]
    PRs = [float(P_R[p]) for p in range(npoints)]
    PZs = [float(P_z[p]) for p in range(npoints)]
    Oms = [float(Omega[p]) for p in range(npoints)]
    ORs = [float(Omega_R[p]) for p in range(npoints)]
    OZs = [float(Omega_z[p]) for p in range(npoints)]
    vws = [float(volume_weights[p]) for p in range(npoints)]
    gam = float(gamma)

    # Complex maps (npoints x nfree) and forcing vectors as plain Python complex numbers.
    URs = [[complex(U_R[p][j]) for j in range(nfree)] for p in range(npoints)]
    UPs = [[complex(U_phi[p][j]) for j in range(nfree)] for p in range(npoints)]
    UZs = [[complex(U_z[p][j]) for j in range(nfree)] for p in range(npoints)]
    DUs = [[complex(divU[p][j]) for j in range(nfree)] for p in range(npoints)]
    Gs = [[complex(G[p][j]) for j in range(nfree)] for p in range(npoints)]
    fRs = [complex(f_R[p]) for p in range(npoints)]
    fPs = [complex(f_phi[p]) for p in range(npoints)]
    fZs = [complex(f_z[p]) for p in range(npoints)]

    E = [[0j] * nfree for _ in range(npoints)]
    PM = [[0j] * nfree for _ in range(npoints)]
    VR = [[0j] * nfree for _ in range(npoints)]
    VP = [[0j] * nfree for _ in range(npoints)]
    VZ = [[0j] * nfree for _ in range(npoints)]
    AR = [[0j] * nfree for _ in range(npoints)]
    AP = [[0j] * nfree for _ in range(npoints)]
    AZ = [[0j] * nfree for _ in range(npoints)]

    for p in range(npoints):
        for j in range(nfree):
            # E = -K_R[:,None]*U_R - K_z[:,None]*U_z
            E[p][j] = -KRs[p] * URs[p][j] - Kzs[p] * UZs[p][j]
            # PM = (gamma*P/rho)[:,None]*G + rho[:,None]**gamma*E      ('**' binds before '*')
            PM[p][j] = (gam * Ps[p] / rhos[p]) * Gs[p][j] + (rhos[p] ** gam) * E[p][j]
            # VR = i*m*Omega[:,None]*U_R
            VR[p][j] = i * m * Oms[p] * URs[p][j]
            # VP = -(R*Omega_R)[:,None]*U_R + i*m*Omega[:,None]*U_phi - (R*Omega_z)[:,None]*U_z
            VP[p][j] = (-(Rs[p] * ORs[p]) * URs[p][j]
                        + i * m * Oms[p] * UPs[p][j]
                        - (Rs[p] * OZs[p]) * UZs[p][j])
            # VZ = i*m*Omega[:,None]*U_z
            VZ[p][j] = i * m * Oms[p] * UZs[p][j]
            # AR = i*m*Omega[:,None]*VR - 2*Omega[:,None]*VP
            AR[p][j] = i * m * Oms[p] * VR[p][j] - 2 * Oms[p] * VP[p][j]
            # AP = i*m*Omega[:,None]*VP + (2*Omega+R*Omega_R)[:,None]*VR + (R*Omega_z)[:,None]*VZ
            AP[p][j] = (i * m * Oms[p] * VP[p][j]
                        + (2 * Oms[p] + Rs[p] * ORs[p]) * VR[p][j]
                        + (Rs[p] * OZs[p]) * VZ[p][j])
            # AZ = i*m*Omega[:,None]*VZ
            AZ[p][j] = i * m * Oms[p] * VZ[p][j]

    # A = U_R^H diag(volume_weights*rho) AR + U_phi^H diag(volume_weights*rho) AP
    #     + U_z^H diag(volume_weights*rho) AZ - divU^H diag(volume_weights) PM
    #     - [U_R^H diag(volume_weights*P_R/rho) + U_z^H diag(volume_weights*P_z/rho)] G
    # Row k = test column (conjugated), column j = trial column.
    A_unscaled = [[0j] * nfree for _ in range(nfree)]
    for k in range(nfree):
        for j in range(nfree):
            acc = 0j
            for p in range(npoints):
                wrho = vws[p] * rhos[p]
                acc += _conj(URs[p][k]) * wrho * AR[p][j]
                acc += _conj(UPs[p][k]) * wrho * AP[p][j]
                acc += _conj(UZs[p][k]) * wrho * AZ[p][j]
                acc -= _conj(DUs[p][k]) * vws[p] * PM[p][j]
                acc -= (_conj(URs[p][k]) * (vws[p] * PRs[p] / rhos[p])
                        + _conj(UZs[p][k]) * (vws[p] * PZs[p] / rhos[p])) * Gs[p][j]
            A_unscaled[k][j] = acc

    # b = -U_R^H(volume_weights*rho*f_R) - U_phi^H(volume_weights*rho*f_phi) - U_z^H(volume_weights*rho*f_z)
    b_unscaled = [0j] * nfree
    for k in range(nfree):
        acc = 0j
        for p in range(npoints):
            acc -= _conj(URs[p][k]) * (vws[p] * rhos[p] * fRs[p])
            acc -= _conj(UPs[p][k]) * (vws[p] * rhos[p] * fPs[p])
            acc -= _conj(UZs[p][k]) * (vws[p] * rhos[p] * fZs[p])
        b_unscaled[k] = acc

    # Return A/normalization_scale, b/normalization_scale; maps unscaled.
    ns = float(normalization_scale)
    A_scaled = [[A_unscaled[k][j] / ns for j in range(nfree)] for k in range(nfree)]
    b_scaled = [b_unscaled[k] / ns for k in range(nfree)]

    def pack(rows):
        return np.array(rows, dtype=np.complex128)

    return {
        'A': pack(A_scaled),
        'b': pack(b_scaled),
        'E': pack(E),
        'PM': pack(PM),
        'VR': pack(VR),
        'VP': pack(VP),
        'VZ': pack(VZ),
        'A_unscaled': pack(A_unscaled),
        'b_unscaled': pack(b_unscaled),
    }

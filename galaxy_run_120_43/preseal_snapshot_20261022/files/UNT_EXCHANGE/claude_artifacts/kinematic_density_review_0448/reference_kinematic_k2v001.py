"""K2 independent loop reference for dispatch 0448 (Claude4 review lane, local helper K2).

Root contract KINEMATIC_DENSITY_COMPARISON_CHOICE_V001.json
(SHA256 9e4c070e88bf431cac9e001958016f9ca022f8cdef2c0c4f039fb7cd1128e14d):

    Gkin = -rho[:,None]*divU - rho_R[:,None]*U_R - rho_z[:,None]*U_z

delta_rho = -div(rho xi) with xi = U y; divU is already the cylindrical
partial_R UR + UR/R + i*m*UP/R + partial_z UZ, so no phi term is added here.

Element-by-element Python-scalar loop, written independently of any other
implementation. NO validation by design: the K2 harness calls it only on valid
inputs. Vectors are read as float64 and maps as complex128 (lossless for valid
real/complex maps). Inputs are never written; the output is a new array.
"""
import numpy as np


def kinematic_reference(*, rho, rho_R, rho_z, U_R, U_z, divU):
    r = np.asarray(rho, dtype=np.float64)
    rr = np.asarray(rho_R, dtype=np.float64)
    rz = np.asarray(rho_z, dtype=np.float64)
    ur = np.asarray(U_R, dtype=np.complex128)
    uz = np.asarray(U_z, dtype=np.complex128)
    dv = np.asarray(divU, dtype=np.complex128)
    npoints, nfree = ur.shape
    out = np.empty((npoints, nfree), dtype=np.complex128)
    for i in range(npoints):
        a = float(r[i])
        b = float(rr[i])
        c = float(rz[i])
        for j in range(nfree):
            out[i, j] = (-a) * complex(dv[i, j]) - b * complex(ur[i, j]) - c * complex(uz[i, j])
    return out

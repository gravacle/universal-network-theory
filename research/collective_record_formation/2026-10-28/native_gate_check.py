"""Source-off gate check for UNT FPMH, Eqs. (9)-(14).

This checks the supplied gate term only, not the full interacting F3 model.
theta = h*t/hbar; computation uses h=hbar=1.
"""
import json
import numpy as np
from scipy.linalg import expm

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
P = np.diag([0., 1.]).astype(complex)
K = np.kron(P, I)
N = np.kron(I, P)
H = -np.kron(P, X)
formation = np.array([0., 0., 1., 0.], dtype=complex)
sham = np.array([1., 0., 0., 0.], dtype=complex)
rows = []
errors = []
for label, theta in [("0", 0.), ("pi/4", np.pi/4),
                     ("pi/2", np.pi/2), ("pi", np.pi)]:
    U = expm(-1j*H*theta)
    f, s = U @ formation, U @ sham
    pf = float(np.real(np.vdot(f, N @ f)))
    ps = float(np.real(np.vdot(s, N @ s)))
    kf = float(np.real(np.vdot(f, K @ f)))
    ks = float(np.real(np.vdot(s, K @ s)))
    full_tv = float(0.5*np.sum(np.abs(np.abs(f)**2 - np.abs(s)**2)))
    expected = float(np.sin(theta)**2)
    errors += [abs(pf-expected), abs(ps), abs(kf-1), abs(ks), abs(full_tv-1)]
    rows.append({"theta":label, "link_probability_formation":pf,
                 "link_probability_sham":ps, "memory_probability_formation":kf,
                 "memory_probability_sham":ks, "full_read_tv":full_tv})

# Fixed K1=K2=1, two blank links, and the gate term alone.
# This is a factorized control, not the full F3 Hamiltonian.
theta = np.pi/4
H2 = -(np.kron(X,I) + np.kron(I,X))
U2 = expm(-1j*H2*theta)
U1 = expm(1j*X*theta)
factorization_error = float(np.linalg.norm(U2-np.kron(U1,U1)))
psi2 = U2 @ np.array([1.,0.,0.,0.], dtype=complex)
n1, n2 = np.kron(P,I), np.kron(I,P)
expect = lambda A: float(np.real(np.vdot(psi2,A@psi2)))
covariance = expect(n1@n2)-expect(n1)*expect(n2)
commutator_norm = float(np.linalg.norm(H@K-K@H))
errors += [factorization_error, abs(covariance), commutator_norm]
result = {
    "scope":"Supplied FPMH gate and independent-copy control only; no EM derivation",
    "dimensionless_time":"theta=h*t/hbar",
    "rows":rows,
    "memory_gate_commutator_norm":commutator_norm,
    "two_link_factorization_error":factorization_error,
    "two_link_connected_occupation_covariance":covariance,
    "max_check_error":max(errors),
    "tolerance":1e-12,
    "passed":max(errors)<1e-12
}
print(json.dumps(result, indent=2))
if not result["passed"]:
    raise SystemExit("Gate check failed")

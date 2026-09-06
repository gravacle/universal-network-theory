#!/usr/bin/env python3
"""Independent 12-point connected-ring parameter scan."""

import json
import math
import os
from pathlib import Path

os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np

checks = 0


def check(value, label):
    global checks
    if not value:
        raise AssertionError(label)
    checks += 1


n, dim = 8, 256
deltas = (0.0, 0.5, 1.0, 2.0)
taus = (math.pi/(4*math.sqrt(2)), math.pi/(2*math.sqrt(2)),
        math.pi/math.sqrt(2))
basis = np.arange(dim, dtype=np.uint16)
q = np.array([((basis >> i) & 1).astype(float) for i in range(n)])
number = np.sum(q, axis=0).astype(int)
psi0 = np.ones(dim, complex)/16
p0 = abs(psi0)**2
q0 = np.einsum("im,m->i", q, p0, optimize=False)
law0 = np.array([p0[number == k].sum() for k in range(9)])

hop = np.zeros((dim, dim), float)
curr_ops = []
for i in range(n):
    j = (i+1) % n
    J = np.zeros((dim, dim), complex)
    for mask in range(dim):
        bi, bj = int(q[i, mask]), int(q[j, mask])
        if bi != bj:
            swap = mask ^ (1 << i) ^ (1 << j)
            hop[swap, mask] -= 1
        if bi == 1 and bj == 0:
            swap = mask ^ (1 << i) ^ (1 << j)
            J[swap, mask] += 1j
            J[mask, swap] -= 1j
    curr_ops.append(J)

check(np.max(abs(hop-hop.T)) == 0, "hopping Hermitian")
check(all(hop[a,b] == 0 or number[a] == number[b]
          for a in range(dim) for b in range(dim)), "number conservation")


def run(delta, tau):
    diag = sum((1 if i % 2 == 0 else -1)*delta*q[i] for i in range(n))
    H = hop + np.diag(diag)
    for i in range(n):
        lhs = 1j*H*(q[i][None,:]-q[i][:,None])
        rhs = -curr_ops[i] + curr_ops[(i-1)%n]
        check(np.max(abs(lhs-rhs)) == 0, "continuity sign")
    ev, V = np.linalg.eigh(H)
    c = np.einsum("ia,i->a", V.conj(), psi0, optimize=False)
    psi = np.einsum("ia,a->i", V, np.exp(-1j*ev*tau)*c, optimize=False)
    p = abs(psi)**2
    q1 = np.einsum("im,m->i", q, p, optimize=False)
    de = ev[:,None]-ev[None,:]
    f = np.empty_like(de, complex)
    zero = abs(de) < 1e-12
    f[zero] = tau
    f[~zero] = (np.exp(1j*de[~zero]*tau)-1)/(1j*de[~zero])
    currents = []
    for J in curr_ops:
        JV = np.einsum("ij,jb->ib", J, V, optimize=False)
        O = np.einsum("ia,ib->ab", V.conj(), JV, optimize=False)
        currents.append(float(np.real(np.sum(c.conj()[:,None]*c[None,:]*O*f))))
    currents = np.array(currents)
    residual = q1-q0+currents-np.roll(currents,1)
    corr = np.array([(p*q[i]*q[(i+1)%n]).sum()-q1[i]*q1[(i+1)%n]
                     for i in range(n)])
    law = np.array([p[number == k].sum() for k in range(9)])
    hpsi = np.einsum("ij,j->i", H, psi, optimize=False)
    hpsi0 = np.einsum("ij,j->i", H, psi0, optimize=False)
    return {
        "delta": delta, "tau": tau, "q_min": float(q1.min()),
        "q_max": float(q1.max()),
        "amp": float(abs(q1[::2].mean()-q1[1::2].mean())),
        "corr": float(np.max(abs(corr))),
        "throughput": float(np.sum(abs(currents))),
        "net_current": float(np.sum(currents)),
        "retained_change": float(q1.sum()-q0.sum()),
        "r1": float(np.sum(abs(residual))), "rinf": float(np.max(abs(residual))),
        "norm": float(abs(np.vdot(psi,psi).real-1)),
        "energy": float(abs(np.vdot(psi,hpsi).real-np.vdot(psi0,hpsi0).real)),
        "number_law": float(np.max(abs(law-law0)))
    }


points = [run(d, t) for d in deltas for t in taus]
check(len(points) == 12, "12 points")
zero = points[:3]
check(max(p["amp"] for p in zero) < 2e-14, "zero-bias occupation control")
check(max(p["throughput"] for p in zero) < 2e-13, "zero-bias current control")
check(max(p["corr"] for p in zero) > 1e-3, "zero-bias correlations nonzero")
check(max(p["r1"] for p in points) < 3e-11, "L1 tolerance")
check(max(p["rinf"] for p in points) < 4e-12, "Linf tolerance")
check(max(abs(p["retained_change"]) for p in points) < 3e-14, "retained control")
check(max(p["norm"] for p in points) < 3e-14, "norm control")
check(max(p["energy"] for p in points) < 3e-13, "energy control")
check(max(p["number_law"] for p in points) < 3e-14, "number-law control")

result = {
    "schema": "AUDIT_R_CONNECTED_RING_PARAMETER_SCAN_V001",
    "disposition": "PASS_CONTROLLED_NUMERICAL_PARAMETER_SCAN",
    "checks": checks,
    "points": points,
    "zero_bias": "ZERO_POSITIONAL_RESPONSE_AND_CURRENT__NONZERO_CORRELATION_ALLOWED",
    "attachment": "INHERITED_ADOPTED_ALPHA_R0__NOT_BARE_F3_DERIVED",
    "read": "COMPLETE_FAILURE_INCLUSIVE_PRODUCT_PVM",
    "residuals": "RAW_UNASSIGNED_UNTIL_OWNER_CLASSIFICATION",
    "scope": "MICROSCOPIC_PREPARED_RING_SCAN",
    "defect_continuum_critical_Ward_gravity": "NOT_PROMOTED"
}
(Path(__file__).parent / "INDEPENDENT_RESULT.json").write_text(
    json.dumps(result, indent=2) + "\n")
print(f"PASS_CONTROLLED_NUMERICAL_PARAMETER_SCAN__{checks}/{checks}")

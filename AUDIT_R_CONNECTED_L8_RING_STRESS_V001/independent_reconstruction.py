#!/usr/bin/env python3
"""Independent numerical reconstruction of the connected eight-site ring."""

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
basis = np.arange(dim, dtype=np.uint16)
occ = np.array([((basis >> i) & 1).astype(float) for i in range(n)])
H = np.diag(sum((1 if i % 2 == 0 else -1) * occ[i] for i in range(n)))
Js = []
for i in range(n):
    j = (i + 1) % n
    J = np.zeros((dim, dim), complex)
    for mask in range(dim):
        if int(occ[i, mask]) != int(occ[j, mask]):
            swap = mask ^ (1 << i) ^ (1 << j)
            H[swap, mask] -= 1
        if int(occ[i, mask]) == 1 and int(occ[j, mask]) == 0:
            swap = mask ^ (1 << i) ^ (1 << j)
            J[swap, mask] += 1j
            J[mask, swap] -= 1j
    Js.append(J)

check(np.max(abs(H-H.T)) == 0, "Hermitian H")
Nop = np.diag(np.sum(occ, axis=0))
number_diag = np.sum(occ, axis=0)
check(all(H[a, b] == 0 or number_diag[a] == number_diag[b]
          for a in range(dim) for b in range(dim)), "exact number conservation")
for i in range(n):
    lhs = 1j * H * (occ[i][None, :] - occ[i][:, None])
    rhs = -Js[i] + Js[(i-1) % n]
    check(np.max(abs(lhs-rhs)) == 0, "current orientation and continuity")

evals, vecs = np.linalg.eigh(H)
psi0 = np.ones(dim, complex) / 16
c = np.einsum("ia,i->a", vecs.conj(), psi0, optimize=False)
tau = math.pi/(2*math.sqrt(2))
psi = np.einsum("ia,a->i", vecs, np.exp(-1j*evals*tau)*c, optimize=False)
p0, p1 = abs(psi0)**2, abs(psi)**2
q0 = np.einsum("im,m->i", occ, p0, optimize=False)
q1 = np.einsum("im,m->i", occ, p1, optimize=False)

curr = []
for J in Js:
    jv = np.einsum("ij,jb->ib", J, vecs, optimize=False)
    O = np.einsum("ia,ib->ab", vecs.conj(), jv, optimize=False)
    de = evals[:, None]-evals[None, :]
    f = np.empty_like(de, complex)
    zero = abs(de) < 1e-12
    f[zero] = tau
    f[~zero] = (np.exp(1j*de[~zero]*tau)-1)/(1j*de[~zero])
    curr.append(float(np.real(np.sum(c.conj()[:, None]*c[None, :]*O*f))))
curr = np.array(curr)
res = q1-q0+curr-np.roll(curr, 1)

number = np.sum(occ, axis=0).astype(int)
law0 = np.array([p0[number == k].sum() for k in range(9)])
law1 = np.array([p1[number == k].sum() for k in range(9)])
corr = np.array([(p1*occ[i]*occ[(i+1)%n]).sum()-q1[i]*q1[(i+1)%n]
                 for i in range(n)])

check(np.max(abs(q0-.5)) < 1e-14, "initial occupations")
check(np.max(abs(q1[::2]-0.3125888646103588)) < 2e-14, "even occupations")
check(np.max(abs(q1[1::2]-0.6874111353896410)) < 2e-14, "odd occupations")
check(np.max(abs(curr[::2]-0.0937055676948207)) < 2e-14, "positive currents")
check(np.max(abs(curr[1::2]+0.0937055676948206)) < 2e-14, "negative currents")
check(np.max(abs(corr+0.026133160509504)) < 2e-14, "connected correlations")
check(np.sum(abs(res)) < 2e-11 and np.max(abs(res)) < 3e-12,
      "ledger tolerances")
check(np.max(abs(law1-law0)) < 2e-12, "number-law control")
check(abs(np.vdot(psi, psi).real-1) < 2e-12, "norm control")
hpsi = np.einsum("ij,j->i", H, psi, optimize=False)
hpsi0 = np.einsum("ij,j->i", H, psi0, optimize=False)
check(abs(np.vdot(psi, hpsi).real-np.vdot(psi0, hpsi0).real) < 2e-12,
      "energy control")

# L8 ring tiling: four odd x values times eight z values.
rings = tuple((x, z) for x in range(8) if x % 2 for z in range(8))
heads = {(x, y, z) for x, z in rings for y in range(8)}
check(len(rings) == 32 and len(heads) == 256, "32 rings cover 256 heads")
check(abs(32*q1.sum()-128) < 7e-14, "aggregate retention")
throughput = 32*np.sum(abs(curr))
net = 32*np.sum(curr)
check(abs(throughput-23.988625329874075) < 3e-13, "aggregate throughput")
check(abs(net) < 3e-14, "net oriented current")

result = {
    "schema": "AUDIT_R_CONNECTED_L8_RING_STRESS_V001",
    "disposition": "PASS_CONTROLLED_NUMERICAL_PREPARED_STRESS",
    "checks": checks,
    "rings": 32,
    "heads": 256,
    "number_commutator_max": "0",
    "q_after": q1.tolist(),
    "currents": curr.tolist(),
    "correlations": corr.tolist(),
    "residual_l1": float(np.sum(abs(res))),
    "residual_linf": float(np.max(abs(res))),
    "number_law_max_change": float(np.max(abs(law1-law0))),
    "retained_L8": float(32*q1.sum()),
    "throughput_L8": float(throughput),
    "net_current_L8": float(net),
    "scope": "CONTROLLED_NUMERICAL_PREPARED_RING_STRESS",
    "generic_critical_continuum_Ward_gravity": "NOT_CLAIMED"
}
(Path(__file__).parent / "INDEPENDENT_RESULT.json").write_text(
    json.dumps(result, indent=2) + "\n")
print(f"PASS_CONTROLLED_NUMERICAL_PREPARED_STRESS__{checks}/{checks}")

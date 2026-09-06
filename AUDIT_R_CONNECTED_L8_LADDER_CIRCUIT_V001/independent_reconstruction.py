#!/usr/bin/env python3
"""Independent 65536-state reconstruction of the 16-site ladder circuit."""

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


n, dim, depth = 16, 1 << 16, 3
theta = math.pi/8
basis = np.arange(dim, dtype=np.uint32)
bits = np.array([((basis >> i) & 1).astype(float) for i in range(n)])
rings = tuple((row+i, row+(i+1)%8) for row in (0,8) for i in range(8))
rungs = tuple((i,i+8) for i in range(8))
edges = rings+rungs
check(len(edges) == len(set(edges)) == 24, "24 unique oriented supports")
check(len({frozenset(e) for e in edges}) == 24, "24 unique physical supports")

# Finite V8 partition: odd x and even z select a paired-y-ring cluster.
clusters = tuple((x,z) for x in range(8) if x%2 for z in range(8) if z%2==0)
covered = {(x,y,zz) for x,z in clusters for zz in (z,z+1) for y in range(8)}
heads = {(x,y,z) for x in range(8) if x%2 for y in range(8) for z in range(8)}
check(len(clusters) == 16 and len(covered) == len(heads) == 256 and covered == heads,
      "16 clusters partition 256 heads")

c, s = math.cos(theta), 1j*math.sin(theta)
u2 = np.array([[c,s],[s,c]])
check(np.max(abs(u2.conj().T@u2-np.eye(2))) < 2e-16, "gate unitarity")

# Opposite stagger on the two rings.
stagger = np.zeros(dim)
for i in range(n):
    stagger += (1 if i%2==0 else -1) * (1 if i<8 else -1) * bits[i]
phase = np.exp(-.5j*theta*stagger)
check(np.max(abs(abs(phase)-1)) < 2e-16, "onsite unitary")
first_coeff = tuple(1 if i%2==0 else -1 for i in range(8))
second_coeff = tuple(-(1 if i%2==0 else -1) for i in range(8))
check(all(second_coeff[i] == -first_coeff[i] for i in range(8)),
      "reversed ring stagger")


def occ(state):
    return np.einsum("im,m->i", bits, abs(state)**2, optimize=False)


psi = np.ones(dim,complex)/math.sqrt(dim)
q_initial = occ(psi)
cum = {e:0.0 for e in edges}
gate_values = []
max_gate_ledger_error = 0.0
for d in range(depth):
    psi *= phase
    for eidx,(i,j) in enumerate(edges):
        before = occ(psi)
        select = (bits[i] == 1) & (bits[j] == 0)
        idx = basis[select]
        swp = idx ^ (1 << i) ^ (1 << j)
        a, b = psi[idx].copy(), psi[swp].copy()
        psi[idx] = c*a+s*b
        psi[swp] = s*a+c*b
        after = occ(psi)
        transported = float(before[i]-after[i])
        max_gate_ledger_error = max(max_gate_ledger_error,
            abs(after[i]-before[i]+transported),
            abs(after[j]-before[j]-transported),
            abs((after[i]+after[j])-(before[i]+before[j])))
        cum[(i,j)] += transported
        gate_values.append((d,eidx,i,j,transported))
    psi *= phase

check(len(gate_values) == 72, "one owner per edge per depth")
check(max_gate_ledger_error < 1e-13, "gate-by-gate endpoint ledgers")
check(all(abs(x[4]) > 1e-12 for x in gate_values), "every applied gate active")
check(all(abs(cum[e]) > 1e-12 for e in edges), "all cumulative supports active")
check(all(abs(cum[e]) > 1e-4 for e in rungs), "all eight rung currents nonzero")

q_final = occ(psi)
div = np.zeros(n)
for (i,j),val in cum.items():
    div[i] += val
    div[j] -= val
res = q_final-q_initial+div
number = np.sum(bits,axis=0).astype(int)
p = abs(psi)**2
law0 = np.array([math.comb(n,k)/dim for k in range(n+1)])
law1 = np.array([p[number==k].sum() for k in range(n+1)])
corr = []
for i,j in edges:
    corr.append((p*bits[i]*bits[j]).sum()-q_final[i]*q_final[j])
vals = np.array(tuple(cum.values()))

check(abs(q_initial.sum()-8) < 1e-14 and abs(q_final.sum()-8) < 1e-14,
      "cluster number retention")
check(abs(16*q_final.sum()-128) < 2e-12, "L8 retention")
check(np.sum(abs(res)) < 2e-12 and np.max(abs(res)) < 3e-13,
      "ledger tolerances")
check(abs(np.vdot(psi,psi).real-1) < 2e-13, "norm tolerance")
check(np.max(abs(law1-law0)) < 2e-13, "number-law tolerance")
check(abs(np.sum(abs(vals))-2.6742223590371705) < 5e-13, "throughput")
check(abs(np.max(np.abs(corr))-0.06592583672451707) < 5e-13, "correlation")

result = {
    "schema": "AUDIT_R_CONNECTED_L8_LADDER_CIRCUIT_V001",
    "disposition": "PASS_CONTROLLED_NUMERICAL_FINITE_CIRCUIT",
    "checks": checks,
    "clusters": 16, "heads": 256, "supports": 24, "gate_records": 72,
    "rung_currents": [cum[e] for e in rungs],
    "cumulative_currents": [cum[e] for e in edges],
    "q_final": q_final.tolist(),
    "retained_L8": float(16*q_final.sum()),
    "throughput_per_cluster": float(np.sum(abs(vals))),
    "residual_l1": float(np.sum(abs(res))),
    "residual_linf": float(np.max(abs(res))),
    "norm_error": float(abs(np.vdot(psi,psi).real-1)),
    "number_law_max_change": float(np.max(abs(law1-law0))),
    "max_gate_ledger_error": float(max_gate_ledger_error),
    "attachment": "INHERITED_ADOPTED_ALPHA_R0__NOT_BARE_F3_DERIVED",
    "read": "COMPLETE_FAILURE_INCLUSIVE_PRODUCT_PVM",
    "coordinate_status": "FINITE_ENUMERATION__NOT_PHYSICAL_GRID",
    "scope": "CONTROLLED_NUMERICAL_PREPARED_CIRCUIT",
    "defect_continuum_critical_Ward_gravity": "NOT_PROMOTED"
}
(Path(__file__).parent/"INDEPENDENT_RESULT.json").write_text(
    json.dumps(result,indent=2)+"\n")
print(f"PASS_CONTROLLED_NUMERICAL_FINITE_CIRCUIT__{checks}/{checks}")

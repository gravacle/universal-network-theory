# Frozen independent centerline Krylov methodology

**Packet:** `AUDIT_R_GATE_C_EXTENDED_CENTERLINE_V001`  
**Scope:** independent method and L4/L6/L8 validation controls only until the
`ALLOW/REQUIRE` semantic gate is certified

## 1. Blind boundary

The executable in this packet does not import the target extended-phase
module, target raw matrices, or target result.  It constructs the graph,
translation orbits, sparse momentum blocks, ground state, response start, and
Krylov spectral measure independently.  Independent raw output is written
before a separate verifier reads the sealed L4/L6/L8 reference result.

The method/code hashes are frozen in `FROZEN_METHOD.json`.  The numerical
executable refuses `L>8` unless it receives the literal command-line
authorization token

```text
ALLOW_REQUIRE_SEMANTIC_GATE_PASSED
```

No such token is used in the validation phase.  The only permitted rows in
this phase are

```text
(L,q) = (4,2), (6,3), (8,4),       rho=q/(2L)=1/4.
```

## 2. Independently reconstructed parent

For even `L`, enumerate fixed-popcount bit words on `2L` sites.  Reconstruct
the `3L` owner-once prism edges directly:

```text
(a,i)--(a,i+1)          for a=0,1,
(0,i)--(1,i+1)          for every i mod L.
```

Each edge swaps one occupied and one blank endpoint and contributes `-1` to
the source-off Hamiltonian.  The constructor has no write-count argument.

Simultaneous translation of both rails is enumerated into exact word orbits.
For momentum `m`, an orbit of period `p` contributes only when
`m*p = 0 mod L`.  Unlike the target builder, the audit forms every sparse
block by applying every owner edge to every word in every admitted orbit and
projecting the result back onto normalized orbit states.  Duplicate entries
are accumulated in row dictionaries and converted to an independently owned
CSR-like representation.  No dense block is formed.

## 3. Adaptive Krylov construction

The `m=0` block is started from a deterministic strictly positive vector,
not from an imported target state.  A Hermitian Lanczos recurrence with two
passes of scalar modified Gram--Schmidt reorthogonalization is evaluated at

```text
8, 16, 32, 64, 96, 128
```

vectors, truncated by the sparse-block dimension or an exact Krylov
breakdown.  It stops after consecutive checkpoints stabilize the ground
energy and its Ritz residual, or at the 128-vector ceiling.

The ground state is expanded to the fixed-charge word basis.  The audit then
constructs

```text
n_k = sum_i exp(2 pi i i/L) [n_(0,i)+n_(1,i)]
```

and independently projects `n_k|0>` into momentum `m=L-1`.  A second adaptive
Lanczos sequence starts from that response vector.  It therefore targets the
response-cyclic subspace, not an arbitrary fixed number of algebraically
lowest eigenvectors.  Each checkpoint records the lowest five available Ritz
values, while all Ritz weights at that checkpoint enter the response moments.

For every checkpoint, with `omega_a=E_a-E_0` and
`w_a=||Pi_a n_k|0>||^2`, reconstruct

```text
Delta_act = lowest positive response-active omega,
chi_tau   = sqrt(sum_a w_a/omega_a^2 / sum_a w_a),
R_low     = w_(Delta_act)/sum_a w_a.
```

Numerically coincident Ritz values are grouped at absolute tolerance `1e-9`.
The provisional lowest active pole supplies the converged-pole residual used
in

```text
w_floor=max(1e-12 sum(w), 100 r_active^2 ||n_k|0>||^2).
```

The active group must remain the same at `w_floor/10`, `w_floor`, and
`10*w_floor`.  Consecutive checkpoints must agree to relative tolerances
`2e-7`, `2e-7`, and `2e-6` for `Delta_act`, `chi_tau`, and `R_low`.
An exact Krylov breakdown is accepted only with an actual reconstructed Ritz
residual below the residual guard.

## 4. Structural and numerical controls

Every row must pass:

1. `3L` distinct owner edges and degree three at every site;
2. exact fixed-charge preservation by every owner action;
3. base-graph bipartite coloring and exact one-carrier bands
   `-2 cos(2 pi m/L) +/- 1`;
4. sparse-block Hermiticity error at most `1e-12`;
5. response translation covariance and projection-norm closure at most
   `1e-9`;
6. ground and active-pole actual residuals at most `1e-9`;
7. Krylov orthogonality error at most `1e-10`;
8. the factor-ten response threshold screen;
9. no more than 128 vectors per solve, 2,000 total matrix-vector products,
   16 GiB peak RSS, or three wall hours per row.

The post-output verifier requires agreement with the sealed reference to
relative `2e-8` for ground energy and `Delta_act`, `5e-7` for `chi_tau`, and
`5e-6` for `R_low`.  It also checks the frozen hashes and verifies that no
L10/L12 output exists in this packet.

## 5. Claim boundary

A passing validation certifies only that an independently implemented sparse,
adaptive response-cyclic Krylov method reproduces the sealed centerline
controls through L8.  It does not execute or prejudge L10/L12, establish
`z=1`, prove a gapless limit, select an accumulation history, define a
continuum algebra, or claim gravity.

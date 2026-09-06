# Blind independent L4/L6/L8 criticality-seed reconstruction

## Freeze boundary

This method was written from the frozen protocol and sealed antecedent
operators before inspecting any target calculation or target result.  The
independent calculation stops at L8.  It cannot authorize or execute L10,
L12, macroscopic closure, universality, or two-cluster work.

## Independent representation

For each even `L` in `(4,6,8)` and each sharp carrier sector `1 <= q <= L`,
construct the complete hard-core configuration graph directly from bit words
of popcount `q`.  Each owner-once physical edge swaps the two endpoint bits
when they differ, and contributes `-1` to the source-off Hamiltonian.

The target representation is not reused.  Instead, simultaneous translation
of both rails is enumerated into exact word orbits.  For momentum
`m=0,...,L-1`, an orbit of length `d` contributes a normalized momentum basis
vector only when `m*d = 0 mod L`.  Dense Hermitian diagonalization is applied
only after this exact symmetry reduction.

The unique Perron--Frobenius ground state is reconstructed from the complete
`m=0` block.  The frozen operator

```text
n_k = sum_i exp(2 pi i i/L) [n_(0,i)+n_(1,i)]
```

maps that state into translation momentum `m=L-1` under the audit phase
convention.  The audit diagonalizes the complete `m=L-1` block and therefore
retains every eigenvalue and response weight that can contribute to the
declared ground-to-`n_k` response.  Other momentum blocks have identically
zero weight by the independently checked translation covariance.  This is a
complete reconstruction of the declared response channel, not a claim to
have serialized all response-inactive eigenvalues.

Distinct response energies are grouped at absolute tolerance `1e-10` using
basis-independent summed projector weight.  The frozen weight floor and its
factor-ten stability screen are then applied literally.  Dense eigenpair
residuals, ground-state residual, momentum-covariance error, and total-weight
closure are retained raw.

## Structural controls

For every size the audit independently verifies the site/edge/degree census,
the exact bit-swap conservation of `Q`, and base-graph bipartiteness.  Bit
complement commutes with every swap, proving the `q <-> 2L-q` configuration-
graph isomorphism.  The configuration coloring
`(-1)^(number of particles on odd-i sites)` changes sign on every hop,
proving chiral spectral symmetry.  Direct one-carrier diagonalization is
compared with `-2*cos(2*pi*m/L) +/- 1`; the Hamiltonian constructor has no
write-count argument.

## Seed decision

A numerical active row is unresolved if any required residual exceeds
`1e-10`, the active pole changes under `w_floor/10`, `w_floor`, and
`10*w_floor`, or the response-channel covariance/weight closure exceeds
`1e-10`.

Only interior sectors `2 <= q <= L-1` can be strict two-sided density extrema.
For a strict gap minimum, the central gap must lie below both neighbors by
more than `10*max(eigen_residual)+1e-12`.  For a strict `chi_tau` maximum it
must exceed both neighbors by relative margin `1e-9`.  These margins only
send numerically marginal extrema to `UNRESOLVED`; they cannot create a seed.
The residue, mode, density-cell intersection, decreasing-gap, and increasing-
`chi_tau` rules otherwise follow the frozen protocol literally.

An exact zero or energy multiplicity is never used as a seed.  The only
permitted final classifications are `CANDIDATE_INTERVAL_L4_L8`,
`NO_CANDIDATE_L4_L8`, or `UNRESOLVED_L4_L8`.  Even a candidate is only a seed
for later confirmation and is not a critical point.

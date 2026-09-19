# Q-sharded target history method V004

Status: frozen before V004 output once named by `FROZEN_METHOD_V004.json`.

## Purpose and claim boundary

This is an executable storage reduction for the already certified exact
prefix-lineage representation.  It changes storage and traversal only.  The
canonical lineage mask remains the row identity, the full carrier occupation
mask remains the column identity, and ALLOW/REQUIRE/SELECT and owner-once
write/transport operations are unchanged.  No lineage states are identified,
truncated, sampled, or reconstructed from a hash.

The method establishes, at most, finite authenticated histories.  It does not
establish a spectral interval, z=1 scaling, a continuum limit, metric dynamics,
universal coupling, emergence, or gravity.

## Exact storage schedule

At prefix `n`, sector `q` is a NumPy-format complex128 memmap of exact shape

`C(n,q) x C(2L,q)`.

Rows and columns use the frozen lexicographic fixed-word order.  Admission
creates one output q-shard at a time.  The stay child copies the source row and
multiplies only carrier columns blank at the write site by `cos(Phi)`.  The
accepted child writes `-i sin(Phi)` times those same blank columns into the
unique row whose lineage mask includes the event and the unique carrier column
whose occupation mask includes the event.  The two row sets are disjoint.

For nonterminal events, actual and null transport traverse one carrier-number
sector at a time.  The frozen target V003 Lanczos dispatcher is reused without
changing its Hamiltonian, current, quadrature, tolerance, or stopping rule.
Mathematically obsolete prefix shards are removed only after both their null
transport and their contribution to the next prefix have completed.

At event L, no H_L array is created.  The unchanged and accepted children are
streamed in bounded row windows from immutable H_(L-1), their observables and
signed edge currents are summed, and the null history is independently routed
from the same immutable rows.  The sharp H_(L-1) q-shards are retained and
hash-custodied.

## Resource guards

- numerical target workset: at most 1,000,000,000 bytes;
- logical scratch: at most 20 GiB;
- process peak RSS: at most 16 GiB;
- L12 wall time: at most 6 hours;
- terminal I/O window: at most 512 MiB;
- available scratch before L12: at least 20 GiB.

The exact H10+H11 live-state bound is 8,773,664,640 bytes.  The retained H11
state is 6,675,614,400 bytes.  A resource or numerical miss is a failed finite
execution, not permission to weaken lineage or alter the physics.


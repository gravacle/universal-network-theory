# Independent blind relational interval spectrum method V001

**State:** `METHOD_DEFINED__NO_PHYSICAL_SPECTRUM_EXECUTED`

## Scope and custody

This packet is an independently written hostile implementation for the future
hash-pinned relational interval spectrum screen.  Only the frozen public
protocol was consulted, and only for its manifest and output contract.  No
target driver, adapter, implementation, serialized matrix, or numerical row
is imported, copied, or read by this packet.

The method and source are frozen before any self-test output.  A second,
runnable freeze cannot be emitted until both the authenticated accumulation
manifest and a complete exact sector plan exist and their caller-supplied
SHA-256 values verify.  This packet performs no physical spectrum execution.

## Independent mathematical construction

For size `L`, number the two rails by `0..L-1` and `L..2L-1`.  The finite
substrate is the undirected degree-three prism with rail edges

```text
(aL+i, aL+(i+1 mod L)), a in {0,1}, i in {0,...,L-1},
```

and rungs `(i,L+i)`.  This is the standard graph product `C_L square K_2`.
The fixed-charge sector `q` is independently enumerated by all `2L`-bit masks
of Hamming weight `q`.  On that basis the hard-core carrier Hamiltonian is

```text
H |s> = - sum_{(u,v) in E, n_u(s) != n_v(s)} |s xor 2^u xor 2^v>.
```

Thus no full sparse matrix is accepted as input.  A deterministic transition
table is reconstructed from the graph and basis and is the only Hamiltonian
representation retained.

The adopted total-rail momentum-one density operator is diagonal:

```text
R_1(s) = q^(-1) sum_j exp(2 pi i j/L) [n_j(s)+n_{L+j}(s)], q>0.
```

This fixed-charge normalization makes the multiplier a convex average and
therefore bounds every response residue by one.  Starting from the
reconstructed ground vector `|0>`, the response seed is
`(R_1-<0|R_1|0>)|0>`.  A zero norm is recorded exactly as
`ZERO_RESPONSE_NORM__ATOM_NONPASSING`; no response Krylov chain is started.
Otherwise the normalized seed generates the response-cyclic subspace.

Both ground and response chains use a separately coded, matrix-free Lanczos
recurrence with two complete modified-Gram-Schmidt reorthogonalization passes
against every retained vector.  The tridiagonal projection is diagonalized
with `numpy.linalg.eigh`.  Every checkpoint retains the lowest five available
ordered Ritz values and reconstructed Ritz residuals.  No dense physical
Hamiltonian is constructed.

## Frozen resource and numerical guards

- checkpoint dimensions: `16,32,64,96,128`, truncated at exact termination;
- retained vectors: at most `128` per chain;
- aggregate Hamiltonian matvecs: at most `2000` per sector;
- wall clock: at most `10800` seconds per sector;
- address-space ceiling: `6442450944` bytes (`6 GiB`) where supported;
- ground and active-pole residual: at most `1e-9`;
- Hermiticity error: at most `1e-12`;
- Krylov orthogonality error: at most `1e-10`;
- response projection closure: at most `1e-9`.

The implementation checks wall time and matvec count before and after each
Hamiltonian action.  It installs the 6 GiB address-space ceiling before basis
construction when the platform exposes `RLIMIT_AS`.  Any breach, non-finite
number, invalid charge, inconsistent dimension, duplicate sector, or custody
failure aborts without a completed blind index.

Each response checkpoint reconstructs all projected poles and residues,
selects the lowest positive pole above the frozen roundoff floor, and records
the active identity at one tenth, one, and ten times that floor.  The three
identities must agree.  A non-terminating chain also requires the final two
checkpoint estimates to meet the public `Delta`, `chi`, and residue drift
limits.  Future atom classifications are computed from the complete five-size
row without accepting a target fit or Boolean decision.

## Freeze-builder contract

The deterministic builder requires all of:

1. the future accumulation manifest path and its separately supplied hash;
2. schema `AUTHENTICATED_RELATIONAL_SECTOR_MANIFEST_V001`;
3. status `PASS_RELATIONAL_ACCUMULATION_L4_L12__SPECTRUM_MANIFEST_READY`;
4. the pinned scalable-protocol hash from the public protocol;
5. an independently serialized exact sector plan and its supplied hash;
6. exact reconstruction of that plan from every manifest atom, including all
   zero-charge dispositions and every distinct positive `(L,q)` pair.

Only then may it write status `BLIND_METHOD_FROZEN_BEFORE_TARGET_SPECTRUM`,
binding the exact manifest hash, plan hash and contents, methodology hash,
   implementation hash, builder hash, and passing self-test-result hash.  The
   self-test result must itself bind the exact pre-output freeze. Missing or mismatched
inputs cause a nonzero exit before the output path is opened.

## Claim boundary

The graph and owner-once conservation inputs retain their source
classifications.  The response channel, numerical guards, checkpoints, and
future sector-plan contract are adopted.  Future history, spectra, gaps,
susceptibilities, residues, fits, and interval classifications are
conditional or empirical until produced and independently adjudicated.
Thermodynamic scaling, native spacetime algebra, anomaly cancellation,
continuum behavior, universal coupling, attraction, metric dynamics,
emergence, and gravity remain open.  No grid, graviton, Ward axiom, external
reservoir, or continuum assumption is introduced.

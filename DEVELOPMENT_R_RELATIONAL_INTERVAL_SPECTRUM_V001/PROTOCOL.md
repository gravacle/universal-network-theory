# Frozen relational interval spectrum driver V001

**Status:** `FROZEN_PRE_OUTPUT__NO_PHYSICAL_SPECTRUM_EXECUTED`

## 1. Bounded purpose

This packet prepares the spectral half of Section 6 of
`DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/PROTOCOL.md`.  It cannot
select an accumulation interval.  It accepts only a later, externally
produced, hash-pinned L4--L12 sector manifest derived from complete target and
blind relational histories.  Without that manifest, or if any of its
derivations or custody checks fail, the driver exits before starting a
spectrum worker.

No history engine is imported or modified here.  A passing future interval
screen would be a finite structural candidate only.  It would not establish
a thermodynamic phase, exact dynamic exponent, continuum, metric, universal
coupling, emergence, or gravity.

## 2. Required manifest contract

The caller must provide both `--manifest PATH` and the independently obtained
`--manifest-sha256 HEX`.  The manifest must have schema
`AUTHENTICATED_RELATIONAL_SECTOR_MANIFEST_V001`, status
`PASS_RELATIONAL_ACCUMULATION_L4_L12__SPECTRUM_MANIFEST_READY`, and must pin
the scalable accumulation protocol SHA-256
`d545a4dd0925d4ae47c1231f4f7632c4cdfef14d0864af292f19fd9f6a708d95`.

For every `L in {4,6,8,10,12}`, `histories[str(L)]` must contain:

```text
target_history_path, target_history_sha256,
blind_history_path,  blind_history_sha256,
hostile_audit_path,  hostile_audit_sha256,
hostile_verdict = PASS,
max_target_blind_sector_weight_difference <= 1e-8,
max_target_blind_history_observable_difference <= 1e-8,
pbar_q, q_interval, density_envelope.
```

Paths are repository-relative regular files and their hashes are checked.
Each hostile audit must contain a PASS record and literally bind the target
and blind history hashes named by its manifest entry.
The driver reads both complete histories, requires the declared size,
dimension agreement, resolved status, and the exact event census `1,...,L`.
Across every event it independently checks all sector weights and the eight
audited observables (`W_n`, allow/blocked/reverse probabilities, signed and
L1 connector changes, retained charge, and genesis charge) to `1e-8` and
reconstructs both declared maximum discrepancies.  It reconstructs `pbar_q` from events
`ceil(L/2),...,L`, independently recomputes the shortest contiguous 99%
sector interval with the frozen tie breaks.

Rational endpoints are encoded as reduced integer pairs `[numerator,
denominator]`.  The manifest must also supply the reconstructed common
intersection as `I_acc` and the complete positive-width atom partition as
`atoms`.  Every atom has `atom_id`, rational `density_interval`, and exactly
one `q_by_L` value for each of the five sizes.  The driver reconstructs all
boundaries `(q+1/2)/(2L)` and rejects omitted, duplicated, reordered, or
best-density-selected atoms.

If an atom selects `q=0`, the total-rail density response vector is exactly
zero.  That size is recorded as `ZERO_RESPONSE_NORM__ATOM_NONPASSING`, and no
Krylov worker is started for that zero-response sector.
This is part of the complete atom census, not an omission.

## 3. Spectral execution contract

`preflight` only validates and prints the manifest-derived work plan.  The
`execute-target` mode additionally requires the literal token

```text
RUN_HASH_PINNED_RELATIONAL_INTERVAL_SPECTRUM_V001
```

It also requires `--blind-freeze PATH --blind-freeze-sha256 HEX`.  That
freeze must bind the same accumulation-manifest hash and exact positive-q
sector plan, identify and hash an independent implementation, declare that no
target code or matrices are imported, and have status
`BLIND_METHOD_FROZEN_BEFORE_TARGET_SPECTRUM`.  Thus target spectra cannot
begin before the corresponding hostile method is frozen.

It verifies this packet's freeze, the frozen manifest hash, the sealed
complete-spectrum L4/L6/L8 aggregate, and the hash-pinned sparse response
engine before running any sector.  The packet-local frozen adapter broadens
only the engine's row-policy table from the old centerline rows to all
positive half-sector charges `1<=q<=L` at L10/L12; it does not replace or
modify any graph, block, Krylov, response, residual, or serialization
function.  L4/L6/L8 are read from the sealed complete
spectra.  Only the distinct positive-q L10/L12 sectors selected by the full
atom partition are scheduled; zero-q selections receive the exact nonpassing
disposition above.  No atom may be omitted.  Up to four one-thread
workers may run in a wave; the per-sector 6 GiB ceiling bounds such a wave by
24 GiB, below the 32 GiB aggregate guard.  The parent driver also samples
live child RSS and wall time, kills its exact spawned wave on a guard breach,
and normalizes Linux `ru_maxrss` KiB to bytes before post-run adjudication.

Every L10/L12 sector retains fully reorthogonalized response-cyclic Lanczos
checkpoints through at most 128 vectors and 2,000 total matrix-vector
products.  All row and checkpoint integers must be literal JSON integers;
all real diagnostics must be finite JSON integers or reals.  JSON Booleans
are never accepted as numbers.  Matvec totals and the three threshold-index
identities are reconstructed against the final Krylov dimensions and active
pole; projection error is reconstructed from the full and projected norms.
Each checkpoint's total response weight and adaptive weight floor are also
reconstructed from the projected norm and active residual estimate.
The stable ten-floor selection must satisfy the necessary support bound
`R_low total_weight > 10 weight_floor`.
Resolved positive-q rows require strictly positive full/projected response
norms, total weights, gaps, susceptibilities, and residues, with every
residue bounded by its probability range `R_low<=1+1e-12`.
The checkpoint-dimension census must equal the frozen
`16,32,64,96,128` schedule truncated at the final dimension, preventing a
duplicated or selectively omitted last pair from manufacturing convergence.
A one-checkpoint sequence requires its exact-termination marker where
serialized and a final Krylov dimension strictly below the frozen 128-vector
cap, as implied by the hash-pinned Lanczos loop.  The raw sector dimension is
reconstructed as `binomial(2L,q)`; orbit/block dimensions and sparse nonzero
counts must be positive and obey their elementary nesting bounds.  A sector
fails closed unless:

```text
ground and active-pole residual       <= 1e-9
block Hermiticity error               <= 1e-12
Krylov orthogonality error            <= 1e-10
response projection closure           <= 1e-9
Delta and chi last-pair relative drift <= 2e-7
R_low last-pair relative drift         <= 2e-6
threshold identity at floor/10,floor,10floor
R_low                                  >= 1e-6
retained Krylov vectors                <= 128
total matvecs                          <= 2000
sector wall time                       <= 10800 s
sector peak RSS                        <= 6 GiB.
```

Every ground and response checkpoint must serialize up to the lowest five
available Ritz values; a final checkpoint must serialize exactly
`min(5,krylov_dimension)`.  A one-checkpoint sequence is accepted only after
exact Krylov termination with the reconstructed residual below its guard.
Values must be finite and ordered.  The first ground value must reconstruct
the checkpoint energy and the response value at the promoted active index
must reconstruct `E0+Delta_act` within `1e-9`.

Target output alone is never promotable.  A separately frozen implementation
must produce a hash-pinned blind index over the identical sector set without
importing target code or matrices.  Its index must identify and hash both the
blind implementation and its pre-target method freeze.  Byte-identical
numerical output is permitted; independence is established by the frozen
method/code provenance and hostile custody, not by forcing numerical bytes to
differ.

The blind index has schema `RELATIONAL_INTERVAL_SPECTRUM_INDEX_V001`, role
`blind`, status `BLIND_COMPLETE__READY_FOR_HOSTILE_ADJUDICATION`, and repeats
the exact manifest hash and pre-target method-freeze path/hash.  Its
implementation path/hash must equal the implementation pinned by that
freeze.  In addition to the complete raw-row map, it supplies an
`atom_classifications` map keyed by every manifest atom.  Each positive-q
entry contains the classification independently computed by the blind code;
an exact zero-response entry contains status
`ZERO_RESPONSE_NORM__ATOM_NONPASSING` and a null classification.

## 4. Adjudication

`adjudicate` accepts the same pinned accumulation manifest plus separately
hash-pinned target and blind spectral indices.  It requires exact `(L,q,rho)`
and sector/block dimension and nonzero-count identities.  Target/blind limits
are `2e-8` relative for ground energy and `Delta_act`, `5e-7` for `chi_tau`,
and `5e-6` for `R_low`.  All row guards and lowest-five telemetry must pass.
The last-pair drifts and every top-level promoted observable are reconstructed
from the checkpoint records rather than trusted.  Target and blind fits and
all Boolean decisions are recomputed separately and required to agree.

For every atom, form the five L4/L6/L8/L10/L12 rows and apply without change:

```text
fixed-z1:      a/L + b/L^2
free-gapless:  a L^(-z)
positive-gap:  Delta_inf + a L^(-z),   1/4 <= z <= 4.
```

The atom passes only when all preregistered conditions hold:

1. `Delta_act` strictly decreases and `chi_tau` strictly increases;
2. fixed-`z=1` held-out relative SSE is below positive-gap SSE and no more
   than `1.25` times free-gapless SSE;
3. `z,y in [0.90,1.10]` and `abs(z-y)<=0.10`;
4. the L8--L12 relative ranges of `L Delta_act` and `chi_tau/L` are at most
   `0.05`;
5. `R_low>=1e-6` at every size and its L8--L12 relative range is at most
   `0.35`; and
6. all target/blind numerical and sector checks pass.

Passing atoms are grouped only by adjacency in the manifest's exact
partition.  A component is an
`AUTHENTICATED_RELATIONAL_Z1_INTERVAL_CANDIDATE` only if its selected sectors
include an adjacent pair at L10 and at L12 and the union carries at least
`0.50` of `pbar_L` at every size.  Otherwise the disposition is
`AUTHENTICATED_RELATIONAL_Z1_REJECTED_L4_L12`.  The exact zero-response atom
is nonpassing but does not contaminate other atoms.  Any unexpected unresolved
positive-q row, incomplete target/blind pair, custody failure, or identity
mismatch fails closed before a physics rejection or candidate is serialized.

## 5. Freeze and claim classes

`FREEZE.json` pins this protocol, the driver and row-policy adapter, the sealed
low-size spectrum aggregate, and the reused target engine/classifier before any physical
spectrum output.  Syntax checking, manifest-free refusal checks, and
synthetic schema self-tests are not physical spectrum output.

**Proved/adopted inputs:** only the finite owner topology and conservation
results already classified by their source packets.  **Adopted here:** the
manifest schema, total-rail `m=1` channel, numerical guards, fit families, and
conjunctive pass rule.  **Conditional:** future hash-pinned accumulation and
spectral inputs.  **Empirical:** all future sector responses and interval
classifications.  **Open:** authenticated L4--L12 manifest completion,
thermodynamic scaling, native spacetime algebra, anomaly, continuum,
universal coupling, attraction, metric dynamics, emergence, and gravity.

No grid, graviton, Ward axiom, external reservoir, or continuum assumption is
introduced.

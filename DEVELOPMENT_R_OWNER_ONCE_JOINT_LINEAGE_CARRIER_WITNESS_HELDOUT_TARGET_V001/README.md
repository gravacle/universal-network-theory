# Held-out L10/L12 target streamed adapter V001

Status: `PRODUCTION_SOURCE_FROZEN__LAUNCH_READY__NO_HELDOUT_OUTPUT`

This directory contains only the target-side preparation for the exact held-out
joint lineage--carrier witness.  It has not computed, opened, serialized, or
classified `D_10` or `D_12`.

## Architecture

The adapter separates the two required numerical routes:

1. **COARSE route:** regenerate the complete rough-resolution L10 or L12
   owner-once history in fresh scratch using the unchanged cache-backed V004
   target engine.  Retain only its preterminal `H_(L-1)` long enough to stream
   the registered terminal readout.
2. **FINE route:** authenticate the already retained sharp `H_9` and `H_11`
   shards from the sealed V012 histories, reconstruct the exact last-bit-zero
   and last-bit-one terminal children, transport each child at the frozen sharp
   resolution, and reduce it immediately to witness sufficient statistics.

Neither route creates `H_L`.  For each final charge sector the bounded stream
retains only:

- a terminal amplitude window;
- the lineage row masses;
- the carrier column masses;
- the registered observed overlap; and
- a separately ordered row/column contraction control.

Those quantities exactly determine `p_q`, `w_q`, `w_sham_q`, `D_q`, the exact
permutation-shuffle null, all marginals, and the frozen numerical residuals.

## Authenticated inputs inventoried

- sealed L4/L6/L8 reconciliation, with `T_4:8 > 1`;
- target V012 cache manifests and read-only index payloads;
- retained target fine histories:
  - L10: 10 NPY shards at `H_9`, `160,240,080` payload bytes and
    `160,241,360` exact NPY bytes including headers;
  - L12: 12 NPY shards at `H_11`, 6,675,614,400 payload bytes plus headers;
- frozen target V004 prefix engine; and
- V003 process-parallel capacity repair used by the completed L12 history.

The production backend installs the target-only V003 numerical-capacity
profile without importing the module that also wires the separate hostile
branch: 256 maximum low-memory subdivisions, coarse Krylov checkpoints
`12,18,24,32,48,64,80`, and fine checkpoints
`16,24,32,48,64,80,96`.  The original quadrature-node counts and convergence
tolerances remain exactly `16 / 2e-9` and `24 / 5e-11` respectively.  Cache
construction and its frozen resource census are authenticated first under the
original V012 constants; the runtime-capacity profile is installed only after
that authentication succeeds.

The backend also authenticates one historical execution-control provenance
correction before opening a cache.  The unchanged V012 freeze names the stale
`cb1681...` hash for `independent_final_auditor.py`, while the packet's complete
read-only `MANIFEST.sha256`, its adjudication record, the preserved replay
note, and Git foundation commit `b5fc80e9da011e7e46c3dfe2d86b91a3b4f440cc`
authenticate the retained `99677...` bytes.  The adapter recognizes only that
single known leaf and projects `99677...` into the V012 census in memory for
the lifetime of a backend.  It restores the original module state on close and
refuses every other source, census, or hash change.  No historical file,
cache payload, equation, propagation rule, tolerance, or execution schedule is
rewritten.

The exact byte totals are reconstructed by the preflight from the authenticated
history records; no physical array value is read by the header-only synthetic
test.

## Resource bounds

- Full L12 terminal dimension: `1,251,677,700` amplitudes, never materialized.
- Largest retained target fine input: `H_11 = 417,225,900` amplitudes,
  `6,675,614,400` complex128 payload bytes.
- Existing V012 maximum adjacent live state: `8,773,667,584` bytes.
- Existing V012 target cache payload: `826,238,292` bytes.
- Target numerical workset cap: `1,000,000,000` bytes.
- Additional explicit witness amplitude window: capped at `128 MiB` before the
  frozen propagation workset.  This is an amplitude-window bound, not a claim
  about peak RSS: probability arrays, contraction scratch, basis arrays, and
  propagator work remain separately governed by the process resource gate.
  Carrier and lineage sufficient statistics are sector-local.
- Existing target process cap: `16 GiB` RSS; scratch cap: `20 GiB`.

The physical run must remain sequential by branch unless a later frozen
aggregate gate proves a concurrent target/hostile memory bound.  No resource
miss licenses sampling, truncation, a carrier-channel substitute, or a fitted
surrogate.

## Frozen production execution

The adapter is bound to the independently frozen execution packet:

- protocol SHA-256:
  `8250e17405067deabbfe7dc4ff00864d26bef66cabfeef628f9f6df63829d9a7`;
- input/resource gate SHA-256:
  `2f38a50e530476e1f33647b49afc95d118738efb1ed53b6ba96335888a44432c`;
- resource validator SHA-256:
  `4c138bcee4bd2230c369fab0592a3ba9430470c69a7c196e25680ca196f28a09`.

The control-plane receipt authenticates the complete frozen input census and a
fresh basic resource preflight without evaluating any witness value.  The
target orchestrator then refuses without the exact target-role authorization,
the sealed receipt, the frozen source manifest, and absent target scratch and
output paths.  Production authenticates every retained target shard before and
after its use.  Binding the protocol does not authorize execution, and no
L10/L12 witness has been computed or opened.

The coarse integration now patches only the already authenticated V012 runtime
hooks (`fixed_words`, `Sector`, admission, and terminal streaming), regenerates
the rough history in a new `rough_L10` or `rough_L12` child of the telemetry-
declared target scratch root, restores every hook in `finally`, and preserves
scratch for custody.  The fine integration maps only the bound retained target
NPY shards and streams the same exact two terminal children.

The two component routes remain deliberately unavailable through the command
line.  `target_production_orchestrator.py` is the sole physical entry point. It
runs a fixed unconditional schedule—L10 coarse, L10 fine, L12 coarse, L12
fine—and writes one deterministic target-only JSON object only after all four
components complete.  It never publishes a partial L10 result, so L10 cannot
become a tuning or stop gate for L12.  Target output contains no hostile code,
input value, or result; later target/hostile reconciliation remains a separate
operation.

## Tests

`test_heldout_target_adapter.py` and `test_production_guards.py` use synthetic
L2/L3 states and mocked production components only.  They check:

- frozen protocol/gate hashes and fail-closed role authorization;
- authenticated seed authority;
- retained H9/H11 headers without opening a witness value;
- exact streamed two-child reconstruction against an explicit small terminal
  state;
- the preregistered matched/crossed synthetic states with opposite
  `+/-1/(2L)` witness values;
- row/column accumulator agreement;
- sham and shuffle null behavior;
- normalization and charge controls; and
- duplicate-key, nonfinite-JSON, and nonfinite-amplitude refusal.
- exact V003 target capacity-profile binding;
- canonical injective admission maps and stable retained-file descriptors;
- the fixed four-component atomic schedule; and
- refusal without any partial scientific output when a component fails.
- full packet authentication of the canonical `99677...` auditor and both
  retained V012 cache manifests;
- exact one-leaf in-memory correction/restoration; and
- refusal when any leaf other than the known `cb1681...` entry drifts.
- frozen-cache authentication before runtime-capacity overrides, followed by
  exact restoration on close.

## Claim boundary

This frozen source establishes an executable exact target architecture and its
synthetic controls.  It does not itself establish the held-out witness because
the physical L10/L12 transaction has not been run.  A successful future target
transaction would establish only the preregistered target-side finite L10/L12
raw witness and internal numerical controls.  It would not by itself establish
target/hostile agreement, an all-L statement, a thermodynamic theorem, or a
gravity claim.

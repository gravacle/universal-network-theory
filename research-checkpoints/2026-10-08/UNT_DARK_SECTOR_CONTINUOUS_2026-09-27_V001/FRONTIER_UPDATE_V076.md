# Frontier update V076 — isolated helium history correction tested

2026-09-30. The two separately owned He RHS-cache replays and their whole-output
atomic step control completed. This is a causal numerical bookkeeping result,
not a thermal derivative qualification, new physical model or Stage 3 closure.
All eleven required scientific lanes remain OPEN; the original thermal audit
still has its two D2_K failures and evolved perturbation execution stays locked.

## What changed, and what did not

The only algorithm change is copying the already computed, input-time helium
RHS into its two lag slots once per quasi call, including the final quasi call.
The explicit integrator already shifts them and was not changed. Equations,
step sizes, thresholds, helium cutoff, H and output interpolation, original
history-0 input packets and all numerical criteria are unchanged. Earlier
observer/build failures and uncorrected results are preserved separately.

Both replays preserve the acquired pre-switch physical states and every one
of 10,295 ordinary output rows whose complete cubic stencil lies safely before
the change. The first explicit input abundance and current RHS are identical
to baseline. The lag-two RHS now has the correct preceding timestamp, rather
than zero. Acquired traces verify exactly one history shift per call.

| Diagnostic | Quarter h=2.1225e-5 | Half h=4.245e-5 |
| --- | ---: | ---: |
| First explicit xHeII difference | +7.9797726732e-8 | +1.5946897972e-7 |
| Isolated changed lag-two contribution | +7.9797726741e-8 | +1.5946897972e-7 |
| Maximum ordinary xe absolute change, z=2852 | +1.3118909403e-7 | +2.8133741714e-7 |
| Maximum relative Tm change | 1.8246523531e-14 | 3.9183239635e-14 |

The near equality of the first-step changes is descriptive, without a newly
chosen gate. It establishes the startup contribution, not the full cause of
the earlier curvature failures or asymptotic convergence order. The post-Saha
path residual and separate helium cutoff remain distinct numerical questions.

Across all 16,001 common output rows, corrected quarter-versus-half maximum
symmetric-relative differences are xe=2.655873773615546e-7 (negative at z=820)
and Tm=1.1891489692946195e-7 (positive at z=829), below the original 2e-4 value
control. There is no denominator floor. No CLASS opacity/visibility derivative
or new eight-unit/six-pair thermal audit was run in this isolated experiment.

## Evidence and verification

All following artifacts are in joint_parent_continuation/hyrec_inputs_v001:

- Controller hyrec_helium_rhs_cache_v001.py:
  `00766aae7adda22a26295252642100707e0f61ce87c35c6fa55bc8dca7db7e2b`.
- Protocol HYREC_HELIUM_RHS_CACHE_PROTOCOL_V001.md:
  `ece2c4b922c42f8838f6e43a53152ac7a0072ddc0c2231a2552312d2a3248c6c`.
- Emitted helium_rhs_cache_src_v001/history.c:
  `83eff56bd85779e18d96b1190bbd79ce8b19d9e326292dc18d90386c65b0ff9f`.
- Freeze HYREC_HELIUM_RHS_CACHE_V001_FROZEN.json:
  `92aa3d4bca90e9b6bf1a4ad10c8b60efb25eb9eccead739c73bb6cd30316d6c8`.
- Quarter run HYREC_HELIUM_RHS_CACHE_RUN_QUARTER_V001.json:
  `c9f6fe45aa62f43ed86812c07b6f3b10d162b285c1c196b218adbe49becc076b`.
- Half run HYREC_HELIUM_RHS_CACHE_RUN_HALF_V001.json:
  `9f7ce3f24db065d580bacbb4605c55d6f7dc7550ff9de6a9a36ca1d720276484`.
- Comparison HYREC_HELIUM_RHS_CACHE_COMPARE_V001.json:
  `ce4b8fd7d2e2f2cc9bc393e45da3234cfec332b73cbcc730d5f61cff1f1df5b6`.
- Independent result review HYREC_HELIUM_RHS_CACHE_RESULT_REVIEW_INDEPENDENT_V001.md:
  `b95b86ca228a41841b3fe93e409add12ead70f43f7b04b9727c94ac914930729`.

Root recomputed the canonical run/comparison payloads, all 408 frozen input
hashes, both raw stream hashes, all 16,001 packed signed-difference rows per
run and both all-row pair maxima exactly. Independent review separately
checked source consistency, selected raw startup evidence and receipt/input/
build/binary/intent/stream custody; it does not claim a full-array recomputation.
Quarter/half replay times were 1.524808958/0.903584792 s; sampled group RSS
222,871,552/112,656,384 bytes. Both exited zero with empty stderr, no monitor
errors and no resource stop. No completed atomic diagnostic needs rerunning.

## Exact next authorized actions

1. The full consistent-inertia two-current producer and serial supervisor are
   authored in joint_parent_continuation. Root has read both and the complete
   protocol; critical_path_native is completing independent source preflight.
   Before any invocation require that review and unchanged hashes. Then freeze
   and run exactly the two coarsest 128-cell L=8 cases, R=128 then R=8192, with
   the fixed RK4 h/h2/h4, DOPRI and pressure-off controls. No old lumped motion
   map, local CFL/domain theorem or physical formation claim transfers. Author
   urm_dark_integration is preparing an inert saved-state arithmetic audit.
2. The separately fixed global exact-knot C2 xe interpolant received root and
   independent inert-source acceptance, not adoption. Final candidate protocol
   SHA `5fc71b5cb8266678f6d630c1f7185d0303bd668e4fd507a8bff614459f60f71f`;
   peer review SHA `cadea7174b6f69a66869e9f69b1e53982222a645a7db6453dcf2345423bfd392`.
   short_path_adversarial now authors compiled-helper synthetic controls and
   success/failure audit serialization/binding. No compilation or physical
   candidate acquisition before root and independent review of that packet.
   Strict whole-interval guards may reject the candidate; do not relax them
   after seeing results. Preserve distinct atomic versus interpolant changes.
3. Any later thermal acquisition must identify its exact atomic receipts and
   retain the full original eight-unit/six-pair criteria, including history 8
   and appropriate ordinary controls for a changed atomic implementation. A
   history-0 startup result cannot qualify that lineage or unlock modes.

At this checkpoint there is no live numerical worker. Root remains the only
numerical executor; agents do source/review work only. Ledger V017 records all
eleven lanes. FULL125/335, growth105/335, URM V008, heartbeat ACTIVE and the
historical Goal remain unchanged. Continue safe useful work; this is a durable
checkpoint, not a request for acknowledgment or a completion boundary.

# Formed four-node transport: the first scalar bound survives

2026-10-03. New 1024-dimensional continuing-writer formation experiment,
not a rerun of the earlier two-node formation/hold or copying-off graph probe.
The complete prospective specification is in
[the two-hop derivation](NATIVE_TWO_HOP_CORRELATION_GEOMETRY_V001.md).

The NumPy-only V002 worker completed once: **592/592 assigned checks pass**,
15 retained states, 0.911396 seconds wall time, 172,015,616 bytes peak self RSS.
Tensor-action Chebyshev and independent row-sparse Taylor propagation agree;
full Hamiltonian columns, energies, conservation, clock, complete bulk SWAP
work, prepared-ensemble identities and early-time coefficients are checked.
The fixed 1e-10 allowance is NOT a certified floating-point error enclosure.

The initial blank state has a zero denominator and an inconclusive ratio.
All twelve positive-age rows satisfy the necessary scalar upper bound:

| Formation age | Native ratio M2/S2 | Feedback-off | Copying-off |
| ---: | ---: | ---: | ---: |
| 0.25 | 0.472001026 | 0.471790949 | 0.471790949 |
| 0.5 | 0.398869184 | 0.395793041 | 0.395793041 |
| 1 | 0.215231820 | 0.182569514 | 0.182569514 |
| 2 | 0.100096682 | 0.351736715 | 0.351736715 |

There is no scalar-bound violation in this test. Values below one do not
establish a scalar geometry: they test only one necessary inequality for
one opposite-vertex pair. No ages, coefficients or allowance were changed.
All three cases reproduce the analytic initial F=-s^4/8+O(s^6).

The native clock is defined at the five sampled ages, with rates from
2.236068 initially to 2.138068 at age2. This is not a whole-window monotonicity
certificate. Feedback-off retains its exact rate sqrt(5). Copying-off has
no phase-clock signal: its clock-normalized K and L remain undefined even
though its clock-free path moments and carrier transport are nonzero.

Feedback-off and copying-off path statistics coincide for a reason. In the
former the records factor from graph/carrier evolution; in the latter blank
records remain blank and the record-feedback term vanishes. Their common
graph/carrier Hamiltonian is unchanged. Native differences therefore isolate
the effect of the retained copying-plus-feedback coupling in this preparation,
not an observational gravitational effect or a new matter substance.

At age2, native ideal bulk relocalization work is 0.1203826471 for sender0
and 0.1419682700 for sender1 in native energy units. The current-square
contribution is retained; all signed terms and all other ages are in the JSON.
The degenerate pointer preserves old carrier correlations. Its preparation,
control and reuse apparatus remain uninstantiated, not free.

## Evidence and technical failure retained

- Source `native_formed_twohop_v002.py` SHA256:
  `59e1147a4a58cb9ebdbe57a0db43313756f9bc1de63438456368b4ace90225f0`.
- Result `native_formed_twohop_v002_results.json` SHA256:
  `cb164dd7a88ef4aa487536a998fffc1f05cedf1cdc9e922f07c6c0149710bbd9`.
- Pre-execution theory/input note SHA256:
  `7278343461c1875a04808bd9daf446ef1188f7bb061a430c6934a63242a1751d`.
- V001 remains unchanged; its import failed because SciPy is unavailable,
  before scientific calculation. `NATIVE_FORMED_TWOHOP_V001_ATTEMPT_001.json`
  records the failure. V002 reuses pinned existing NumPy propagators without
  installation, changed physics or a tolerance adjustment.

The worker was authored source-only by endpoint_equations_check; root read
the entire source, checked the operator identities and ran the sole numerical
worker. These finite model checks are not physical replication or an
observational fit.

## Next discriminating question

Both opposite-vertex pairs on the same square must share ONE scalar loop
phase if one scalar hopping Hamiltonian describes the graph. Test that exact
compatibility condition from the retained states, preserving the successful
first inequality and every control. This is a follow-on exploratory analysis,
not a held-out prediction, a new formation sweep or a change in the earlier
criterion. Coarse-grained geometry with memory or internal channels remains
distinct from this restrictive instantaneous scalar surrogate.

## Completed follow-on: one phase cannot describe both diagonals

This sharper, exploratory saved-state calculation is complete, with all
296 assigned arithmetic checks passing. It introduces no new propagation,
ages, coefficients or allowance. Let edges (a,b,c,d) join L0R0,L0R1,L1R0,L1R1,
and let p denote their means. Set QL=<(ac+bd)^2> and QR=<(ab+cd)^2>.
A Hermitian scalar hopping model on this square, calibrated from all four
one-hop probabilities using the SAME clock at L0, must have

    QL=pa pc+pb pd+2 sqrt(pa pb pc pd) cos(Phi),
    QR=pa pb+pc pd+2 sqrt(pa pb pc pd) cos(Phi).

The loop phase is gauge invariant. Arbitrary scalar onsite energies do not
enter these leading opposite-pair coefficients, because the opposite pair
has no direct edge. Even allowing a new scalar calibration at every age,
one phase must serve all senders at that age. Consequently

    D=QL-QR-pa pc-pb pd+pa pb+pc pd=0

is necessary. Equivalently D=cov(a,c)+cov(b,d)-cov(a,b)-cov(c,d);
the four-edge moment cancels. This diagnostic does NOT require or establish
entanglement: ordinary correlated random links can also violate it.

| Age | Native D | Feedback-off D | Copying-off D |
| ---: | ---: | ---: | ---: |
| 0.25 | -8.49549155e-9 | -8.52411479e-9 | -8.52411479e-9 |
| 0.5 | -1.30837241e-6 | -1.29964535e-6 | -1.29964535e-6 |
| 1 | -1.75358540e-5 | 9.00431979e-6 | 9.00431979e-6 |
| 2 | 0.00155952045 | -0.000454119421 | -0.000454119421 |

Each positive-age D interval excludes zero under the unchanged assigned
1e-10 allowance on every p and Q. Both opposite-pair phase bounds pass
separately: the incompatibility is in the SHARED phase. For example, the
native age2 pair requires cos(Phi)=-0.799806637 and -0.822062026 respectively.
The native age0.25 D interval is [-8.70762565e-9,-8.28335745e-9]; it is the
smallest-magnitude native mismatch, not discarded in favor of the larger one.
This remains a numerical result under assigned allowances, not a rigorous
roundoff certificate or a statistical significance calculation.

All twelve positive-age rows fail the clock-free identity. Only eight,
native and feedback-off, have the declared record clock and hence a
clock-normalized readout. The four copying-off cases remain clock-free
controls. All three age-zero states have undefined phase ratios and do not
reject the scalar identity. None is presented as a positive closure proof.

The R0 relocalization uses the same environment marginal and L0 clock.
Its complete bulk work is lambda_J(pa+pc)-E_current_square-E_hopping,
independently checked from the full vector and graph marginal. Native age2
work is 0.1311754585. Pointer preparation, implementation and synchronization
remain ideal-protocol assumptions. Substituting unrelated sender clock rates
would change this experiment and require an explicit synchronization map.

The constructive consequence is to retain link correlations, environment
memory or additional channels before claiming one scalar effective geometry.
It is not a rejection of coarse-grained geometry, an emergent metric, or UNT.
The control failures show that the effect is not unique to record feedback.
It neither derives a gravitational force nor changes the cosmological ranking.

- Saved-state source `native_formed_twohop_loop_saved_v001.py` SHA256:
  `e13db0a50c65633ba689f3bb7dcd636a4898ef09f53a25a76e989159cbb95ab2`.
- Saved result `native_formed_twohop_loop_saved_v001_results.json` SHA256:
  `8508272a701d9bc1f7be37eb356aceadbc281b8d335e00349b9fc74e6a9178f4`.
- Runtime: 0.0348031 seconds; 24,756,224 bytes peak self RSS.

Root independently derived the shared-loop cancellation, read the complete
calculator and ran it once. Endpoint_equations_check authored it; the
separate v005_resume_review agent checked the formula, source, saved result,
intervals, diagonal/gauge objections and copying-off clock qualification
without rerunning evolution. This is internal independent algebra/code review,
not independent experimental replication.

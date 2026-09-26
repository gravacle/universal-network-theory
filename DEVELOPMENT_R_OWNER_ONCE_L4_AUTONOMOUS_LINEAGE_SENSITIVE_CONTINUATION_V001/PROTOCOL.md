# L4 autonomous lineage-sensitive continuation protocol V001

Date: 2026-09-25

Status: `FROZEN_CANDIDATE__PRE_REVIEW_AND_PRE_OUTPUT`

## 1. One prospective question

At the completed `L=4` owner-once checkpoint, does the retained *joint*
lineage--carrier structure change a subsequent carrier state relative to a
same-sector product state having the same separate lineage and carrier
marginals?

This is a one-size mechanism test.  It cannot establish persistence, scaling,
a thermodynamic limit, curvature, geometry, or gravity.

## 2. Exact input checkpoint

Regenerate the historical `L=4` state with the frozen periodic two-rail prism,
blank carrier, loaded active cycle, events `0,1,2,3`, `phi=pi/4`, transport
dwell `pi/2`, Taylor order `12`, and `128` substeps per dwell.  The checkpoint
is immediately after event `3` transport and before the first revisit.

The parent source is
`DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/compute_seed_history.py`
at SHA-256
`24ea3626fda443dd4ae5076c7766e1aaca77ff5ce9f22c05bae96943fc627d55`.
In that source's fixed-weight global basis, the checkpoint is a 495-entry
little-endian `complex128` vector whose canonical C-order byte SHA-256 is
`52d979329c4a8c643bda90644981e9508f7ec42f65c0dd25310cddbf2074671f`.
The corresponding 495 little-endian `uint32` basis words have SHA-256
`b91eec28486c0c06f9ce8f5ebaf4bd71b24a3fd5a3525650ac9d7023bea8d81f`.
Any mismatch stops before continuation.

## 3. Actual and same-sector product inputs

Write the checkpoint as

\[
 |\Psi\rangle=\sum_q |\psi_q\rangle,
 \qquad p_q=\langle\psi_q|\psi_q\rangle .
\]

The actual arm is symmetrically sharp-sector dephased,

\[
 \rho_A=\sum_q |\psi_q\rangle\langle\psi_q| .
\]

For each nonzero sector, let
`rho^S_q=Tr_C |psi_q><psi_q|` and
`rho^C_q=Tr_S |psi_q><psi_q|`.  The comparator is

\[
 \rho_P=\sum_{q:p_q>0}{\rho^S_q\otimes\rho^C_q\over p_q}.
\]

Thus each term has trace `p_q`.  The comparator preserves the complete quantum
lineage marginal, complete quantum carrier marginal, and weight within every
`q`, while removing only within-sector lineage--carrier association.

Coherence between different `q` sectors is removed in **both** arms.  All
coherence inside each `q` sector is retained.  This symmetric dephasing is
mandatory: otherwise a difference could be caused merely by deleting
cross-sector coherence in only the comparator.  No diagonal-only sham,
lineage shuffle, random permutation, or post-output alternative is allowed.

Before continuation the two arms must agree in their full carrier marginals,
full lineage marginals, and `q` weights to the numerical tolerance below.
The initial carrier marginals are equal by construction, and their numerical
equality residual is mandatory.  Consequently a resolved terminal carrier
difference isolates the common lineage-reading continuation rather than a
pre-existing carrier-state difference.

## 4. One fixed continuation

Continue the existing deterministic cursor for exactly its next transition.
The next event is zero-based event `e=0`.  Apply, in this order,

1. the unchanged historical reversible admission pulse
   `U_A(0)=exp[-i(pi/4)K_rel(0)]`; and
2. the unchanged autonomous carrier transport
   `U_T=exp[-i(pi/2)H_T]` on the same periodic prism.

The common cursor shift is outside the retained lineage--carrier factors and
does not change the registered observables.  The admission pulse is not
replaced by a forward-only projection: its forward and reverse amplitudes are
both retained.  At a revisit it acts jointly on the spent-lineage bit and the
carrier target, which is precisely why carrier-marginal closure from the fresh
first pass no longer applies.  Both arms receive the identical unitary
`U=U_T U_A(0)`.

No event, dwell, pulse angle, endpoint, or observable may be changed after the
output is opened.

## 5. Frozen carrier-only readout

Let `sigma_A=Tr_S(U rho_A U^dagger)` and
`sigma_P=Tr_S(U rho_P U^dagger)`.

The primary effect is the normalized carrier trace distance

\[
 \Delta_C={1\over2}\|\sigma_A-\sigma_P\|_1\in[0,1].
\]

It is a fixed operational carrier-state distinguishability, not a selected
site or fitted observable.  The following fixed diagnostics are also reported:

\[
 R_n=\sqrt{{1\over 2L}\sum_{x=0}^{2L-1}
   (\langle n_x\rangle_A-\langle n_x\rangle_P)^2}\in[0,1],
\]

the carrier-configuration total-variation distance, carrier-number-sector
total-variation distance, and every signed
`delta_n_x=<n_x>_A-<n_x>_P`.  `delta_n_0` is the fixed signed revisit-site
diagnostic.  Positive means the actual retained association raises terminal
occupation at site zero relative to the product comparator; negative means it
lowers it.  No sign is a pass condition.

For transparency, the same quantities are recorded immediately after
admission and after transport.  Only the post-transport values are primary.
The common carrier unitary preserves trace distance, so equality of the two
trace-distance rows is a control, not independent evidence.  `R_n` and the
signed site profile are the transport-sensitive diagnostics.

## 6. Numerical rule and disposition

Run the complete calculation from both the historical 64-substep and
128-substep input checkpoints; the 128-substep result is primary.  Let `d` be
the largest absolute coarse/fine disagreement among `Delta_C`, `R_n`, both
total-variation diagnostics, and every `delta_n_x` at both registered
checkpoints.  Let `r` be the maximum state-hash-independent control residual:
input/output trace and Hermiticity, negativity beyond roundoff, unitary and
Hamiltonian reconstruction, equality of the two arms' input marginals and
sector weights, and trace-distance invariance under common transport.  Freeze

\[
 \tau=\max(10^{-10},50d,100r).
\]

Mandatory controls are:

```text
fine checkpoint and basis hashes                       exact
input carrier/lineage marginal and q-weight mismatch  <= 1e-11
trace, Hermiticity, unitarity, reconstruction residual <= 1e-11
minimum density eigenvalue                             >= -1e-10
coarse/fine registered-observable disagreement         <= 1e-8
all values finite; 0 <= Delta_C,R_n,TV <= 1 (+1e-12)
```

If all controls pass and `Delta_C>tau`, return
`RESOLVED_L4_LINEAGE_SENSITIVE_CARRIER_CONTINUATION`.  If all controls pass
and `Delta_C<=tau`, return
`FALSIFIED_L4_LINEAGE_SENSITIVE_CARRIER_CONTINUATION_IN_FIXED_TEST`.  Equivalently,
the frozen primary statistic is

\[
 T_{\rm dyn}=\Delta_C/\tau,
\]

and the mechanism resolves exactly when `T_dyn>1`.  A numerically controlled
zero (or value at or below resolution) is a mechanism falsifier for this L4
schedule, not an unresolved or missing result.  A
control failure returns `L4_LINEAGE_SENSITIVE_CONTINUATION_UNRESOLVED`.
`R_n>tau` is reported separately as
`FIXED_OCCUPATION_PROFILE_RESPONSE`; it cannot rescue or veto the primary
classification.  The exact effect sizes are always reported; “resolved” does
not mean large, persistent, or important.

## 7. Runtime, restart, and publication preflight

The completed historical L4 coarse/fine seed run took about `0.60 s`.  This
dense mixed-state continuation has dimension 495 and an estimated wall time
of `1--5 min` on the current local Mac, with a conservative `<20 min` bound
and `<100 MiB` working memory.  It is therefore below the 30-minute long-run
checkpoint threshold.

The smallest scientifically valid restart unit is the entire two-resolution
L4 comparison.  Maximum interruption loss is one such run (estimated at most
five minutes normally).  Do not add chunk manifests, workers, daemons, or
resume orchestration.  Publish one deterministic JSON by same-directory
temporary file, `fsync`, and atomic rename only after all controls complete.
No partial numerical artifact is a result.

Launch status is `READY_AFTER_HUMAN_REVIEW_OF_THIS_FREEZE`.  Sleep, terminal
loss, reboot, or power loss during execution loses only the current short run;
rerun the same command from the beginning.  Retain the final atomic JSON and
its SHA-256; temporary files may be removed only after absence of a final
result is confirmed.

Before launch, authenticate the protocol, freeze, implementation, tests, and
parent source against `SOURCE_HASHES.sha256`.  A missing, extra, or mismatched
registered source blocks execution.

## 8. Claim boundary

A pass establishes only that, for this exact L4 checkpoint, symmetric
sector-coherence convention, single deterministic revisit, and carrier
readout, the prior joint lineage--carrier association changes a subsequent
carrier state in a way the separate marginals do not determine.  A fail
falsifies only this fixed L4 mechanism test.

Neither outcome establishes or refutes size persistence, an autonomous
large-scale law, record curvature, Ollivier--Ricci curvature, a continuum,
RGRL/WTC response, metric dynamics, alpha selection, or gravity.  Outcome and
scope must be recorded identically whether the test passes or fails.

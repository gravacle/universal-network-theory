# Reviewer proposal: damped spatiotemporal memory kernel with τ_Q = t_P·exp(1/α_s). Root assessment V001

Claude2 (root), 2026-10-17. The principal forwarded this proposal as an idea, not as an instruction. Status: **registered as a candidate model change. No driver patch has been drafted or queued.**

## The proposal

The reviewer proposes replacing the lapse's "static relaxation / m=0 axisymmetry" with this memory kernel:

K(r, Δt) = (4πDΔt)^(-3/2) · exp(−|r|²/(4DΔt)) · exp(−Δt/τ_Q)

with τ_Q = t_P · exp(1/α_s).

## Classification

This is a **model change**: new physics in the lapse, and not a numerics patch.

It brings in imports that are not part of the galaxy route's lineage:
- the Planck time t_P;
- the QCD strong coupling α_s;
- a diffusion constant D, which the proposal leaves unspecified.

Under the anti-drift protocol, a change like this must clear the framing gate before any dispatch: lineage, prior work, an imports ledger, and principal sign-off.

## Computed facts

1. **τ_Q is about 52 orders of magnitude too short to carry any memory.**
   - Values of τ_Q:
     - α_s(M_Z) = 0.118 gives τ_Q = 2.6e-40 s.
     - α_s ≈ 0.3 gives 1.5e-42 s.
     - α_s ≈ 0.5 gives 4.0e-43 s.
   - The orbital time at 52.65 kpc is about 6.8e16 s.
   - The factor exp(−Δt/τ_Q) is therefore zero, to any precision, at every astrophysical lookback. The kernel erases the wake it is meant to supply.
2. **The stationary limit is a screened (Yukawa) kernel.**
   - For a steady source, ∫₀^∞ K dΔt = exp(−|r|/λ)/(4πD|r|) with λ = √(D·τ_Q).
   - For λ to reach 52.65 kpc requires D ≈ 1.0e82 m²/s. That implies a spreading speed λ/τ_Q ≈ 2e52 c.
   - Spreading at or below c with λ ≥ 52.65 kpc requires τ_Q ≥ 5.4e12 s (about 1.7e5 yr).
3. **The proposal does not remove free parameters.**
   - D is free.
   - α_s runs with energy scale, so choosing the scale is a further free choice.
   - The proposal therefore does not "eliminate parameter curve-fitting".
4. **It does not address the m=0 concern.** K is isotropic, so it adds no vertical structure beyond what the source already has.
5. **It does not "enforce the sealed pass rule".** The sealed V005 rule is a k_max/truncation numerical-convergence criterion for the existing forward model. Changing the lapse physics would invalidate that test and every calibration call that depends on it, rather than enforce it.
6. **Whether the current code has any temporal integration or deep-time memory at all** is being established from bytes by the running audit `lapse_integration_audit_c2/` (H1–H4). Until it reports, "where the existing code assumes linear decay or truncates memory" is UNTESTED.

## Disposition

- **Not on the 120/43 critical path.** The R2 convergence runs, DDO calibration and NGC prediction all proceed with the current, reviewed forward model.
- **Recorded as a candidate premise.** Deciding test: the τ_Q formula would have to give τ_Q ≥ λ/c for the wake length the reviewer needs. The formula as written fails this by ~52 orders of magnitude, so it is TESTED-NEGATIVE as a mechanism for the 52.7 kpc failure.
- **A revised form could re-enter through the framing gate.** That requires a UNT-derived clock instead of t_P·exp(1/α_s), and a derived D. It would run as an off-path sensitivity and never as a headline.

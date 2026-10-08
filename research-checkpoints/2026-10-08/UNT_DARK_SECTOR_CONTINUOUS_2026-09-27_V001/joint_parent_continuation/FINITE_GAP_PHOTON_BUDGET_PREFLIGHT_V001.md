# Finite-gap photon-budget preflight

2026-09-29. Accepted, no correction requested. Full producer and protocol read;
AST inspection and direct comparison of the 18 inherited reference dictionaries
only. No producer import/run, new orbit, quadrature, propagation or fit.

- `finite_gap_photon_budget_v001.py` SHA256:
  `a19b5fbf26df1ab086763d186c9f447e4244f6da4210384a96ec7c673b7bac33`.
- `FINITE_GAP_PHOTON_BUDGET_PROTOCOL_V001.md` SHA256:
  `886d0f8673427963f722b0f7c18febcfabc15cc7ba2fc53c90d4015d1a4777cf`.

For the owned normalization m=u=1, the signed-orbit action gives
C=[pi/B(1/4,3/2)]^(4/3). The one-hard-mode sums Q=beta C I^(4/3) and
D=beta R² sqrt(C I^(4/3)) have the correct weight and gap factors. The saved
early energy already includes beta, while early pressure is per mode; the code
uses those conventions correctly. Present excitation normalization cancels in
the stated ratios, and Q<=E(A)/A^4<=Q+D/A² is applied to all 360 old states,
not the newer two-gap finite-field subset. Approximation epsilons .01/.001
control a sufficient asymptotic-error certificate, not observational gates.

The imported blackbody energy and critical-density conversion use h_P (not
hbar) and the correct c powers. All 18 actual photon-reference dictionaries
equal their corresponding calibration dictionaries. The source pins the old
transport and photon receipt, checks the decoded wrapper and recursive old
freeze, and snapshots the new code/protocol and mathematical references. It
only reads inputs and emits stdout. Known input hashes make the inherited
transport content fixed; no alternative or sampled source is substituted.

These are excitation-density comparisons against explicitly imported ordinary
photon A^4 dilution. They are not total parent density including the unchanged
matched vacuum, photon production, neutrino equivalence, a thermal spectrum,
a BBN calculation or a CMB fit. Extending the effective action/clock/state to
an early epoch is still conditional. The standard-BBN-derived baryon references
cannot be counted as independent confirmation if the expansion history changes.

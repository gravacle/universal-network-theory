# Independent saved hard-reaction attribution review V001

2026-09-29. **Accepted within its stated counterfactual scope.** Full control
source, protocol and analytical counterfactual note were read. A separate
stdlib audit authenticated and recomputed saved-array arithmetic only; no
material import/evaluation, orbit quadrature, PDE solve or eigensolver was
performed. The reviewer previously checked the original spatial formulation,
but did not produce these four numerical runs.

## Custody and complete census

Reviewed source SHA256 `fae9bf1e327bf9ad1828fbe2399c6ddc8cc9f585f61956f2b390a3cb90f6ca8d`,
protocol `49b24e5ec7142860e3b8b49effedd220cabc7ea03222efa4f6aa1b16fff3bf16`,
counterfactual note `2431935ebb87ce16ad26b4d4a06b2b07a630ce52d233970789b949fe1b2a887c`,
freeze `943ffd1fd1edaead11152cff78e26508d651ef0cea33656ff04f5248ac1a27a1`.
All 13 recursive manifests and 72 distinct ancestor files authenticate.
All four counterfactual and four corresponding physical transports pass
compressed/raw/payload/freeze checks, with exact source/geometry/seed pairing.

The complete census is R={128,8192}, L={1,2}, N=16, both original fixed
seeds per case. There are eight converged counterfactual seeds, each with
four actually checked/passing directional controls. All **204 producer
checks** pass. The independent saved audit performs **32,753 checks**, with
zero failures; its largest normalized arithmetic discrepancy is 2.67e-15.
Actual producer durations are 3.716–3.931 seconds, maximum self RSS 96,092,160
bytes. Full per-seed identities, metrics and hashes are retained in
`CLAMPED_HARD_REACTION_ATTRIBUTION_AUDIT_V001.json` (SHA256
`49f8daec0bd0b552aadec8a487f1e98a29f35308ceda80baa689c93bb7aac39d`), generated
by `clamped_hard_reaction_saved_audit_v001.py`.

## What was independently checked

The intervention keeps the phase-solved state, polarization and full energy
ledger and deletes only epsilon*delta(E_hard+3Pi_hard)/Kb from the lapse
volume source. Re-deriving its Jacobian gives precisely the source's removed
positive lapse diagonal and the compensating hard-gradient derivative.
The production counterfactual assembles its soft-only residual directly;
it does not obtain a tiny residual by subtracting two large hard terms.
Its temporary in-memory evaluator dispatch is explicit and restored by
try/finally; the frozen original files/configuration are untouched.

Saved arrays independently verify all annular volumes, source integrals,
action inventories, full E/hard/soft and minimum/excitation splits,
deltaE+3deltaPi, action ratios and the signed identity

    R_physical = R_counterfactual - removed_hard_source.

The same sign holds for the global flux defect. Reconstructing the
counterfactual residual from the saved physical residual plus omitted source
recovers its recorded residual norm and integrated balance. All same-grid
physical-to-counterfactual RMS, signed range, maximum difference and SI
acceleration conversions were independently recomputed. Qualification flags
were checked rather than inferred from a small difference.

The full final Jacobian/face-quadrature tensors are not saved. Their direct
and finite-difference producer checks are authenticated and their formulas
reviewed, but were not independently numerically reproduced in this audit.

## Scientific readout, without selecting a seed

Both seeds give the displayed values to the quoted precision. Differences
are always **counterfactual minus physical**. The RMS ratios below use the
declared symmetric denominator, not an observational error measure.

| R | L | Both physical seeds converged? | Radial relative RMS | Vertical relative RMS | Omitted hard volume / sheet flux |
|---:|---:|:---:|---:|---:|---:|
| 128 | 1 | yes | 1.4662e-8 | 1.0235e-8 | 2.0710e-8 |
| 128 | 2 | yes | 7.0505e-8 | 5.1539e-8 | 1.2638e-7 |
| 8192 | 1 | yes | .28149 | .21077 | .37046 |
| 8192 | 2 | **no** | 1.5638–1.6733 | .85879–.96975 | 2.16572 |

There are six equilibrium-qualified same-seed pairs, not eight. For the
large R=8192 box the original physical seeds ended LINE_SEARCH_FAILED and
ITERATION_LIMIT. Its large differences compare retained failed iterates
with counterfactual roots and **are not equilibrium-effect estimates**.

On the qualified R=8192,L=1 pair the counterfactual radial force is smaller
at every saved center; the signed dimensionless difference ranges from
approximately -.26870 to -.00060123. The original-action residual norm on
the counterfactual is .37046. Thus the hard source is materially important
in this clamped cold-state calculation and cannot be omitted merely because
its local constitutive force correction seems small. This includes nonlinear
feedback into the phase state, not response to a fixed imposed density map.
The R=128 effect is negligible at this test's spatial accuracy; its many
reported digits do not establish corresponding physical precision.

The R=8192 counterfactual still has large hard action/energy: I/I_b spans
about 1,970–618,800 for L=1 and 3,776–1,009,309 for L=2. Convergence after
deleting its source does not make that energy disappear. The two control
seeds agree to max|delta u|<4.5e-14, which is reproducibility for these seeds,
not a uniqueness theorem or dynamical accessibility result.

## Required interpretation limits

The inherited `local_lengths` use the **full material** J:
ell/a=sqrt(K_T or K_L divided by J)/epsilon. The audit reproduces those
values exactly. They are diagnostics of the recorded full material, **not
the reaction scale of the lambda=0 PDE**, whose hard lapse reaction was
removed. They must not qualify control-grid resolution or imply that the
counterfactual retained the full operator's instability/length spectrum.

This is a deliberately action-inconsistent attribution experiment, not a
second viable model, no-extra-energy solution, galaxy fit or repair of the
cosmic completion. N16 convergence alone does not establish mesh resolution.
The original mixed clamp corner and open-reservoir/exterior assumptions
remain. All eight control roots can coexist with the absence of a found
large-box physical root; this does not prove nonexistence of the original
branch, let alone failure of network clustering or of UNT generally.

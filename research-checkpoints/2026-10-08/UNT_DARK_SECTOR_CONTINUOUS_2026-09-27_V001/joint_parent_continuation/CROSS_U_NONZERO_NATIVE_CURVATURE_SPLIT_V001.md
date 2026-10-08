# S_cross accepted-field native curvature split V001

2026-10-06 UTC. Only root may execute after the V003 MINRES parent closes naturally, its full receipt is accepted, exact bindings replace every AUTHOR placeholder, and independent static preflight and fresh ownership checks pass. This draft does not modify, import, run or restart any live producer. No automatic resume, new galaxy solve, fitted parameter, state projection or physical-success gate is authorized by this diagnostic.

## Frozen state and fixed census

The parent is CROSS_U_NGC3198_MINRES_RECOVERY_V003, including all sixteen outcomes, histories, copied failures and physical flags. Choose exactly the three wider epsilon cases E1em05_HI0_H20, E1em04_HI0_H20 and E1em03_HI0_H20. These are prospective parameter/source choices, not choices from observed velocity residuals. No other case is deleted or reclassified. Each selected parent case may be converged or may end at a genuine inner failure; retain its status and nonlinear residual exactly. The latter is an accepted provisional field, not an observed prediction.

For each case pin the terminal accepted physical state NPZ and commit, CASE JSON, closed parent result/receipt, and the immediately preceding accepted physical state NPZ and commit. The terminal LINEAR_FAILED NPZ contains the accepted state and a separate unaccepted linear partial; this diagnostic uses only the accepted state. A copied ancestor case may require the corresponding ancestor receipt. Bind every such closed receipt explicitly and validate its complete output map, not a mutable journal. Compare physical identity, mask, mesh, mode census and accepted-history prefix across the two states. The terminal merged accepted history must contain exactly one more accepted event than the predecessor. Do not substitute an unrelated earlier state or an unaccepted Krylov direction.

Use exactly two scalar directions: p1 is the terminal accepted scalar potential, and p2 is the terminal scalar potential minus that immediate predecessor. Normalize each nonzero direction by its maximum absolute nodal value for the quadratic diagnostic only. Do not rescale the physical state or modes. A zero/nonfinite direction is a recorded refusal, not permission to choose a different direction. Six direction records are retained. All original observed rows and parent predicates remain stored unchanged; this program does not use velocity residuals to select or score a direction.

## Exact fixed-quadrature split

Use the protected core's identical Q1 geometry, positive four-point cylindrical quadrature dV=R dR dz, scalar and two-component vector parity masks, ell=.1 kpc, gc, thirty-two positive native weights and literal quartic coefficient. At the frozen state write v_j=sqrt(w_j) z_j and alpha_j=1/(w_j gc^2 xi_j^4). At every quadrature point,

    H_j = (1+alpha_j |v_j|^2) I + 2 alpha_j v_j v_j^T >= I.

Its perpendicular and parallel eigenvalues are 1+alpha_j |v_j|^2 and 1+3alpha_j |v_j|^2. H_j is the actual quartic modal curvature; it is not reset to the identity. For a scalar direction let g=grad p, K=int dV |g|^2, b_j=sqrt(w_j) B p, and

    A_j0 = int dV N_vector^T H_j N_vector,
    A_jell = A_j0 + ell^2 K_vector,
    L_j = int dV g^T H_j^-1 g.

K_vector includes both component gradients and the radial v_R^2/R^2 connection. All inverse notation refers to positive modal blocks, not the indefinite coupled field Hessian. Define

    Q_quartic = sum_j w_j (K-L_j),
    Q_space = sum_j w_j L_j - sum_j b_j^T A_j0^-1 b_j,
    Q_ell = sum_j b_j^T (A_j0^-1-A_jell^-1) b_j,
    Q_weight = (1-sum_j w_j) K.

The first three are nonnegative in exact arithmetic. Q_space is the weighted best-approximation error for sqrt(w_j) H_j^-1 g in the actual masked continuous-Q1 vector space. It includes the actual essential boundary/parity restriction. Q_ell is the computed FE ell contribution; neither term is automatically a continuum certificate. The native Schur energy is exactly Q_quartic+Q_space+Q_ell+Q_weight=K-sum_j b_j^T A_jell^-1 b_j. Preserve the actual floating weight remainder instead of silently renormalizing weights.

Evaluate Q_quartic by its cancellation-safe positive local expression. With t=1+alpha |v|^2 and h=1+3alpha |v|^2,

    g^T(I-H^-1)g = alpha |v|^2 |g|^2/t + 2alpha(v dot g)^2/(t*h).

Evaluate g^T H^-1 g as |g|^2/h + 2alpha(v_R g_z-v_z g_R)^2/(t*h). These are the same literal two-component Hessian, including mixed radial/vertical curvature. No scalar-only quartic substitute is allowed.

Add the unchanged actual phase-pressure quadratic separately,

    Q_pressure = -int dV kappa B_units (D_phi+3 W_phi) p^2.

Use the exact accepted potential, SAME epsilon/background fixed inventory and protected P(X) formula for its coefficient, with strict original nodal and quadrature clock domain. The reported full scalar Schur energy is the native split plus Q_pressure. Negative pressure/Jeans curvature is not clipped or relabeled as projection stiffness. Ordinary fixed-source density has no derivative in this tangent.

## Numerical qualification and publication

Each direction requires exactly two batched positive modal solves, with and without ell. Use positive diagonal PCG, cap600 and true global relative residual<=1e-10 on every exit. Preserve all modes and both components. Publish separate mode residuals descriptively so a weak aggregate does not hide them. Store failed raw responses before any JSON diagnostic, with finite/null refusal metadata; do not accept recurrence residual alone or treat a failed solve as a force result.

The baseline Q1 mass diagonal obeys M>=c diag(M), c=(2-sqrt(3))/4 on this cylindrical quadrature and masks. Since H_j>=I and ell energy is positive, each batched A also obeys that bound. For a computed y and r=b-Ay report U=sum r_i^2/Mdiag_i / c and raw energy uncertainty |y dot r|+U. A direct variational energy differs from the true minimum by r^T A^-1 r in [0,U]. Report actual direct energies, raw Schur energies and uncertainties for both solves. Add the same prospective numerical resolution allowance 1e-8 K used in the zero-field diagnostic when discussing nonnegativity or forming descriptive ratios. This is not a rigorous binary64 interval. Undefined or unresolved denominators produce explicit None reasons.

Meaningful controls per nonzero direction are the two true solves, positive local quadratic partition, two direct variational/Schur identities, full split identity, and uncertainty-qualified nonnegativity of Q_space and Q_ell. Identity/nonnegativity allowance is 1e-8 K. These eight controls give forty-eight prospective arithmetic/solver predicates if all six directions exist; a refused direction retains a failed refusal record and does not invent eight successful controls. No observed-force, EOS, stability, native normalization, spatial-convergence or physical match gate is added.

Bind protocol, core source and all actual imported core inputs, zero-field diagnostic source/protocol/result/receipt, full closed V003 source/protocol/result/receipt, and all selected CASE/state/commit/ancestor-receipt inputs. Record the exact maps in an exclusive root manifest. Preencode canonical finite JSON before exclusive opens. For each direction publish the raw responses/direction in an exclusive NPZ, an immutable commit with payload/hash/owner binding, and reread both immediately. Publish three case summaries incrementally, then a full result and receipt after authenticating every own pair, control prefix and parent byte map again. No partial or failed output is overwritten. If interrupted, preserve the prefix for review; this version has no resume or automatic resubmission.

## What the result can decide

Comparing Q_space with Q_quartic+Q_ell tests whether the accepted branch's tangent in either actual direction is materially controlled by the continuous-Q1 restriction. A small Q_space clears only those directions. The zero-field ratios alone cannot bound the nonzero branch: H_j^-1 g may fail to be representable even when g is representable. Neither two directional energies nor zero-field locking bounds the forty-three force predictions without a compatible-space field comparison or a stability/inverse-response bound for the full pressure-bearing operator. Existing weak metric, quadrature, exterior and cosmological current-junction qualifications stay false.

This frozen protocol is prospective; the diagnostic remains unexecuted. The source must bind the closed V003 parent and exact selected state pairs before sealing. Static compilation is permitted; it does not establish numerical success. Root launch requires the final actual-byte/schema preflight and fresh ownership verification. No prior outcome is promoted by this packet.

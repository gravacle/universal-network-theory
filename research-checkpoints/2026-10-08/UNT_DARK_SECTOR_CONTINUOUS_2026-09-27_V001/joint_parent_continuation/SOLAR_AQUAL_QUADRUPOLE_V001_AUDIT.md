# Direct AQUAL Solar quadrupole: independent saved-array audit

2026-10-04. The seven completed cases were audited without importing the producer, refitting, solving a Poisson equation, or repeating nonlinear iterations. **169/169 checks pass**; runtime 0.40 seconds. All frozen inputs, test custody, five primary receipt hashes, seven case identities/physical constants, grids and stored qualifications agree. Sensitivity-case hashes are newly pinned in this audit.

## Checked physical result

The frozen galaxy-effective law, universally completed as stationary conservative AQUAL with the declared Solar/external-field boundary, gives

    Q2 = 4.156474763870837e-26 s^-2,
    c2 = -0.15818800002661748,
    Q2 = -3(a0/rM)c2,  rM=sqrt(GM/a0).

This sign agrees with the observational potential convention

    delta Phi = -Q2 R^2 P2(cos theta)/3.

The current jointly estimated Cassini/DE440 value is `(1.6 ± 1.8)e-27 s^-2`; its definition and observational result are given in [Park et al., Eq. 6 and abstract](https://arxiv.org/html/2602.17884v2). The older overlapping Cassini estimate is not a second independent datum.

The arithmetic standardized residual for the fixed central prediction is **22.20264**. This is not a posterior-marginalized significance: galaxy acceleration-scale/source/calibration uncertainties, shape calibration, boundary approximations and completion uncertainty have not been marginalized. No theory posterior or global UNT exclusion is computed.

The separately declared external accelerations `2.16e-10` and `2.48e-10 m/s^2` give `3.8734470374e-26` and `4.4381673850e-26 s^-2`. These sensitivity cases do not repair the fixed prediction; they are not a probability distribution or an optimized external field. The result concerns this universal static AQUAL completion, not QUMOND, arbitrary network histories, or every network theory.

## Independent arithmetic and source checks

The audit reconstructed Legendre polynomials and derivatives by recurrence, radial derivatives by explicit finite differences, the full total acceleration and the externally subtracted polarization source. It reproduced all saved Br and Theta arrays, external mu, angular derivative L, plateau extraction, Q2 conversion, domain/refinement differences and summary qualification. The stable deficit was independently compared with the positive mechanical integral for the polarization at 256/512-point quadrature, and L was checked using the differentiated mechanical equilibrium rather than just a numerical derivative of the closed law.

The frozen primary changes remain about 0.07355% (B/C), 0.005328% (C/D), and 0.00000645% (D/E); every extraction plateau has relative variation below 9e-10. C/D changes both domain bounds and radial spacing, so it is a combined domain/spacing check, not an independently isolated estimate of each boundary error. The plateau by itself is not a global accuracy certificate.

## Two independent Green checks

For the fitted discrete radial operator at l=2, let n=N+1, r_j=r_0 exp(jh), and S_j be the reconstructed modal right-hand side. The homogeneous roots are rho=exp(2h), sigma=exp(-3h). The recurrence gives

    c2_discrete = psi_2(r_N)/r_N^2 - sum_{j=1}^{N-1} W_j S_j,
    W_j = [1-exp(-5h(N-j))]/[(2 sinh(5h/2)/h^2) r_j^2].

This is evaluated directly, not through the producer's tridiagonal solve. Its deviation from the saved field is accounted for by the same weights applied to the modal equation residual, plus the actual boundary residuals. The exact algebraic identity passes; the final source-derived c2 differs from the extracted plateau by only **5.90e-8 relative**.

There is also a continuum finite-boundary check. Writing sigma_2 for the l=2 coefficient of div B, a=inner radius and b=outer radius, regular inner continuation gives

    c2_cont = psi_2(b)/b^2
              -(1/5) integral_a^b [1/r-r^4/b^5] sigma_2(r) dr.

The source inside a is taken negligible, consistently with the regular inner boundary. Integration by parts evaluates this from Br and Theta without a radial derivative of Br. It retains the outer Dirichlet contribution and the inner endpoint term; the producer's raw complete-domain integral omitted these finite-boundary corrections and was correctly labeled descriptive.

The corrected continuum check differs from the plateau by **0.5131%, 0.1281%, 0.03203%** for A/B/C and **0.03902%** for the enlarged-domain finest case. This is consistent with second-order radial discretization; changing domain at fixed point count increases log spacing. The finite-bound correction itself is small here. It does not certify an infinite-domain continuum error bound, but it substantively corroborates the extracted quadrupole rather than merely repeating its SI conversion.

## Residual and conservation qualification

Additional saved-field diagnostics, not retroactive gates, show a finest maximum scaled modal equation residual of **9.45e-6**. The fixed-point update tolerance must therefore not be reported as pointwise field-equation accuracy. Its quadrupole-weighted contribution is about **9.33e-9 in c2**, consistent with the discrete Green check.

The monopole flux `r^2 integral(mu gr du)/2` has finest maximum deviation **7.90e-4** from unit enclosed mass, and **2.79e-4** within `0.05<r<10`. The same-domain A/B/C flux errors decrease by roughly four on successive radial refinement. These discretization diagnostics are small compared with the conditional discrepancy being screened, but are retained rather than described as exact conservation.

## Scientific conclusion and ceiling

The numerically qualified fixed-calibration **mean prediction does not match the measured Solar quadrupole under the adopted universal static AQUAL identification**. The fast high-field Newtonian saturation does not itself remove the nonlocal external-field quadrupole generated in the transition region. This is a substantive cross-scale restriction on that completion, while retaining the separate galaxy-effective evidence.

A different source/state/metric completion would require an explicit physical law and new counted premises; this audit supplies none. It does not establish a native formation mechanism, a response time, a full relativistic completion, or an exclusion of all UNT. Published QUMOND-specific planetary corrections and interpolation-family exclusions were not imported as results for this law.

Audit JSON: `SOLAR_AQUAL_QUADRUPOLE_V001_AUDIT.json`, SHA256 `51c60f2a0b714c815885cb219edb0f04bb962c1a423d88ab148b050bc27d6745`.

All seven receipt hashes and the audit source hash are in that JSON. No original receipt/source was changed. The sole numerical slot was explicitly released after the audit.

# Independent saved concentration–mass radial audit

2026-10-04. No producer, helper, fitting, calibration, or previous force calculation was rerun. This audit directly evaluated the analytic NFW enclosed-mass function at **saved** parameters, grid masses and candidates. Supplementary paired statistics are posthoc descriptive checks, not new gates or a change of primary score.

## Verification

**29,581/29,581 checks pass**, runtime 1.95 seconds. All frozen files, 100 new and inherited receipts, common source rows, masks, exclusions, reference predictions, outcome records and aggregates match. There are 94 eligible galaxies and the same six n<6 exclusions. All 51 synthetic and 4,982 galaxy controls have passing errors/flags.

The independent implementation uses

    m(x) = log1p(x) - x/(1+x),
    m(x) = sum_{n>=2} [x/(1+x)]^n/n for small x,
    c = 10^[.905 - .101 log10(.671 M_DMO/10^12 Msun) + delta_c],
    r200 = [G M_DMO/(100 H0^2)]^(1/3),
    v^2 = b_saved^2 + G(1-fb)M_DMO m(R c/r200)/[R m(c)].

It reconstructs predictions and residuals, both inner and outer metrics, every saved 257/513 grid objective and candidate objective, the selected saved minimum, all paired differences, and all domain flags. Maximum scaled discrepancies are 1.34e-14 in velocities, 1.61e-13 in grid objectives, and 1.81e-15 in aggregates. This verifies arithmetic, not global optimization between samples or observational independence.

## Primary result and descriptive robustness

The frozen primary score remains galaxy-balanced outer velocity MSE in `(km/s)^2`. The 513-point results are:

| Fixed concentration scenario | CM MSE | Network wins / ties / losses | Median network-minus-CM | Mean after removing five largest network gains |
|---|---:|---:|---:|---:|
| Central | 944.746602 | 60 / 0 / 34 | −87.223653 | −300.656431 |
| −0.11 dex | 1302.398205 | 67 / 0 / 27 | −83.501886 | −434.101975 |
| +0.11 dex | 666.604252 | 61 / 0 / 33 | −60.576702 | −165.970675 |

The common network MSE is 285.872069; RAR remains 285.221205. The CM median individual MSEs are 160.633765, 194.475217 and 168.063989, versus network 85.817032. Removing only the largest gain leaves paired means −539.163714, −825.919064 and −331.253446. The five-removed paired medians remain −83.208713, −61.051108 and −53.680262. In these scenarios the largest absolute contributions coincide with the largest gains. No cases are removed from the primary result.

The five largest network gains, in descending magnitude (network-minus-CM):

| Central | −0.11 dex | +0.11 dex |
|---|---|---|
| UGC02487: −11791.981 | UGC02487: −18742.984 | UGC02487: −4982.255 |
| UGC03205: −7950.257 | UGC02953: −11312.982 | UGC03205: −4905.110 |
| UGC02953: −6722.935 | UGC09133: −10074.661 | F571-8: −4636.617 |
| F571-8: −4636.617 | UGC03205: −9921.340 | UGC03546: −3942.276 |
| UGC12506: −4073.993 | UGC12506: −6866.414 | NGC5055: −2551.177 |

Large contributions still matter, but unlike the unrestricted-halo comparison, the mean advantage is accompanied by a majority of per-galaxy wins and a favorable paired median in each fixed scenario. Substantial counterexamples remain; for example central c(M) strongly improves UGC06787 relative to the network. Full wins/losses, top losses, paired values and deletion sensitivities at both resolutions are in the JSON. Diagnostic ties use `abs(difference)<=1e-10 max(1,MSE_network,MSE_CM)`.

## Domain and interpretation limits

Central/minus/plus cases have respectively **8/7/8 zero halos**, **20/15/25 nonzero masses below the published approximate calibration range**, and **0/1/1 finite mass-boundary fits**. The two finite-boundary cases are the lower limit: NGC4068 (minus) and KK98-251 (plus). No nonzero fitted halo has outer rows beyond its adopted DMO r200. The entire sample remains included.

All 94 baryon budgets are **unassessed**, not satisfied: catalogue total baryonic masses are absent, and the radial field is not silently converted into a total. The DMO-to-dark factor `(1-fb)` is an adopted no-response mapping; it is not a self-consistent baryon-retention or halo-response model. The three coherent concentration offsets are separate scenarios, not scatter marginalization or an envelope to choose per galaxy.

This strengthens the descriptive effective-law radial-transfer comparison beyond unconstrained two-parameter extrapolations. It does not establish superiority over RAR, a complete ΛCDM population prediction, native network formation, or UNT uniqueness. Low-mass extrapolation, fixed baryonic conventions, source geometry and missing covariance remain material limitations.

## Custody

Producer result SHA256: `22e23d920de4df97361fa2e633b316dea36b2f76878c0f0334d9b85c55ae619a`.

Producer source SHA256: `b12d2a4a320063edd05b578a85c4d97c32121509632ba4e969e20cb0694bbe2a`.

Freeze SHA256: `2243d06baef0a5f636739cdab980055f104ed98365e6a2e5749238e825cbe1e8`.

Audit JSON SHA256: `e28d552c3fe594ae8d173629f7ad496e986be4b75cb0c7b61101459b27de3ab7`.

Audit source SHA256: `34ba32fed2e29090b02400634884016946141b59f7fe199cb5b495517510fbe3`.

The sole numerical slot was explicitly released after this saved-array audit. Original sources and receipts were not modified.

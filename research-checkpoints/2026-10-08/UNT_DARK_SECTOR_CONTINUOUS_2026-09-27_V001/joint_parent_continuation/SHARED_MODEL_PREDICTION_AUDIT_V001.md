# Shared model inputs and predictions

2026-10-04. Current K(X)/J/cTheta development candidate. This audit identifies what the model predicts and what it is calibrated to reproduce. An independently supplied parameter is not a scientific disqualification. The result limits the unification claim, not the legitimacy of a calibrated effective theory.

## The exact shared scale result

Write K(X) = Kstar k_epsilon(X/Q0), with Kstar = 3 Omega_A Hunit², m = K_X and homogeneous conserved charge a³m = I0. On aligned FLRW the relative spatial gradient p and vector electric field vanish. Therefore J contributes zero homogeneous stress:

    3 F H² = 8 pi Gtilde (rho_b + rho_r) + X m - K,
    F = 1 + 3 cTheta/2,
    partial H(a) / partial a0 = 0

at fixed the other physical inputs. This statement applies to the aligned background, not arbitrary inhomogeneous backreaction. In code units b = (1+lambda_s)*a0/(c_light*Hunit) and

    j = lambda_s*abs(p)/sqrt(p²+b²),
    J = (2 lambda_s / (3 b))*abs(p)³ + O(abs(p)⁵).

Consequently a0 is also absent from the linear equations around p = 0. It remains important for nonlinear response and for the finite-amplitude validity of a linear solution. The conditional MOND target v_flat^4 = GN M_b a0 would change with a0; this is not a newly calculated galaxy rotation curve.

One new bounded audit varied only a0 by factors .5, 1 and 2. At scale factors .01, .1, .48696752516586306 and 1, all dust-background values and the source-free linear assembly matrices were exactly unchanged in floating arithmetic. The nonlinear j response changed; its logarithmic derivative agrees with -b²/(p²+b²). All 27 prespecified controls passed. No historical evolution or observational fit was rerun.

Evidence: `INVARIANT_CLOCK_SHARED_SCALE_AUDIT_V001_RESULT.json`, SHA256 `aaf0341f77f4cff2a25a4ef92273cfc61522dd3308ec2df6a63b6d918af7b5d8`.

Thus this candidate does not derive a0 from H, nor predict a0/(c_light H) from the homogeneous/linear sector. It can still be tested as an effective model with a universally calibrated a0. Deriving that relation is one route to stronger explanatory economy, not the sole allowable next step.

## Nonredundant physical inputs

An independently reviewed physical basis, with measured GN and c_light fixed, is:

    {a0, Kstar, Q0, epsilon, lambda_s, KB, cTheta, I0}.

These are eight global action/state quantities, plus ordinary baryon abundance, thermal inputs, functional/coupling assumptions and the unresolved formation/perturbation state. This is a basis for the candidate family, not a claim that all eight were fitted in the last calculation. The two quantities varied in the thermal calibration do not exhaust the assumed model inputs.

Do not double-count C = 2-KB, F, b, or

    r0 = Gtilde/GN = (1-KB/2)*lambda_s/(1+lambda_s).

Given r0 and KB, lambda_s is determined. Also d0 = I0 Q0/Kstar and the present clock abundance are related through the constitutive solution; the saved clock-excess abundance .251 was used to set d0, not independently added to it. The K and J functional forms, universal coupling and positive-sheet choice remain adopted assumptions. No per-galaxy formation history has yet been justified as a prediction.

Hunit is a reference scale, not automatically measured H_today. If Omega_A, Omega_clock and Q0/Hunit are held fixed during a fit, varying Hunit changes dimensional Kstar, Q0 and charge normalization. The earlier fitted Hunit is therefore an expansion-normalization parameter, not exclusively an ordinary-matter input.

## Compression and stationary checks

The conditional local Newton normalization r0 = .98 enters the ordinary density conversion as Omega_b = r0*omega_b/(Hunit/100)². Compression separately divides the Friedmann source by F = 1.015. Using .98/F in that conversion and dividing again by F would double-count compression.

    H_today = Hunit sqrt[(Omega_A+Omega_clock+Omega_b+Omega_r)/F].

The old thermal calibration is not automatically current. No new BBN, recombination or BAO likelihood was run in this audit. lambda_s may affect cosmology indirectly through the local GN normalization at fixed measured ordinary density; its absence from J's homogeneous stress does not make it universally irrelevant.

There is a genuine shared consistency restriction: the bounded clock's stationary inward lapse headroom is

    Delta ln N < 0.5 log[(1+epsilon)/(1+epsilon*s/(1+s))],

under the regular-center stationary assumptions already documented. The same epsilon and homogeneous state determine the clock's adiabatic response m/(X K_XX). This is a useful constraint across domains, not a derivation of a0. Time-dependent/gradient branches must be tested through their own equations; the stationary cap is not an all-UNT exclusion.

## Physical readout and the bounded numerical attempt

For the synchronous-comoving periodic metric, infinitesimally neighboring freely falling observers measure longitudinal/perpendicular geodesic-deviation acceleration A_ddot/A and B_ddot/B. If f_i are logarithmic metric deviations and x = ln abar, their excess over the same compressed FLRW background is

    Delta T_i = H² f_i,xx + (Hdot+2 H²) f_i,x + H² f_i,x².

The directional derivative includes both explicit x dependence and the state derivative along the full RHS. This is a physical tidal readout, not a circular velocity, photon deflection, or proof that an initial preparation forms dynamically. Ordinary and network contributions must both be retained.

The proposed chi-primary arithmetic representation was implemented in `invariant_clock_periodic_chi_v001.py` and `invariant_clock_periodic_reduced_chi_v001.py`, with unchanged physics/gates. Independent source review confirms the fixed-chi charge inverse, stable reconstructed momentum and canonical constraint derivative H_chi = 4 V c b_dot Kchi. The accepted fields retain independent delta_chi through the RHS, rather than recovering it through cancelling metric terms.

Its first component receipt passes 36 of 38 controls. Both inherited retained-RHS comparisons fail: 2.0687e-12 and 3.8793e-12 against 1e-12. The new momentum/constraint chi derivatives agree within 1.51e-14, and the two initial-slice tidal derivative refinements differ by at most 5.283e-8 against 1e-4. These partial passes do not qualify the formulation as a whole or a tidal scientific result. No evolution was launched from this failed component receipt and no gate was relaxed.

Evidence: `INVARIANT_CLOCK_PERIODIC_CHI_COMPONENTS_V001_RESULT.json`, SHA256 `33e4cd825cbc623f532d9394b9f6a8a5a7b4d99a109fc7dde01aa8986d2eed4d`. Preserve it. The comparison uses the old recovered-chi representation on the reconstructed state; an independent higher-precision/action-based reference would be needed to decide which representation dominates the discrepancy. Do not infer the new map is wrong or certified from a near-threshold comparison alone. Per V008, no blind follow-on solver family is queued.

## A calibrated observational route remains legitimate

The user's latest question emphasizes preserving successful measurements while testing a different interpretation of them. The relevant choice is not “derive every constant or abandon UNT.” An effective network response may take measured ordinary inputs and a small set of universally calibrated constants, then predict other systems and observables without retuning.

Distinguish signal and calibration, observational extraction, and dynamical inference. Rotation measurements constrain motion; inferring an unseen mass distribution additionally requires a gravitational law and geometry. Redshift and brightness constrain photon/clock/ruler relations; inferring an expansion history and its source uses additional physical assumptions. None of these measurements is wholly theory-free. A replacement must specify the complete forward relation and reproduce the successful limits, not merely rename inferred quantities.

Next decision: specify one operational relation that the existing candidate actually changes (metric response of ordinary probes or photon/clock/ruler transport), list its calibrations and choose a withheld consequence. Do not require a native a0-H derivation before this conditional test. Do not call two unconstrained fits a unified prediction either. Memory is a possible discriminant, but matching density alone is not matching the full baryonic state; the existing two seed preparations can differ in velocity. A rigorous same-state test requires Bv = 0 and Pv != 0, with B including the matched density and velocity observables and P the metric readout.

No observational superiority, native derivation, dark-component elimination or Stage 3 completion is claimed. All eleven lanes remain open, including both distinct CMB investigations.

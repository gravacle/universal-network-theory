# Same-parent finite ground law: chemical-band screen V001

2026-10-06 UTC. Static necessary-condition test following the accepted carrier-curvature/matched-limit note. Original source/state/ground spectra and both live workers remain untouched. Root and two independent reviewers derived these operator inequalities before this file was saved. No new eigensolve, state reset, physical-unit fit or chosen EOS.

For the SAME active g1, lambda_R1/2, epsilon_psi1, h1, j1/4, t_hop1/2 native N=1 cell and canonical field Omega1, M=8/12/16, kappa=0,+/-1/1000, let d=f(2)-f(7/4). The accepted exact sector identity gives mu1=E1-E0=1-d and mu2=E2-E1=1+d, with 0<d<1/4. A positive curvature sign alone is insufficient for matching the existing cold pressure function.

## An unfitted operator lower bound

In incidence blocks H_env(k)=[[A,-I],[-I,A+D]], where A=2I+R+X_L+X_R+H_gamma,0 and D=k-R/2+W_kappa. For 7/4<=k<=2, R+X_L+X_R has extreme eigenvalues1+/-sqrt(5). H_gamma,0 lies between2I and34I. Positive H_D,H_B obey H_D+H_B=H_gamma,0, hence ||W_kappa||<=34(1/1000+1/999)<69/1000. Therefore

    (5-sqrt(5))I <= A <= (37+sqrt(5))I,
    (681/1000)I < D < (2069/1000)I,
    4-sqrt(5) <= f(k) <= 5-sqrt(5),
    0 < A+D-f(k) < 40I.

The upper f bound uses a blank-incidence variational state with the minimum record/bare-field energy; the lower uses D>0 and -X_link>=-I. A normalized ground vector [u,v] satisfies u=(A+D-f)v from its lower row. Thus ||u||<40||v|| and <n>=||v||^2>1/1601. Applying Rayleigh comparison to the k2=2 ground at k1=7/4 gives d>=<n>_k2/4>1/6404. Consequently

    mu2/mu1=(1+d)/(1-d)>6405/6403.

## Comparison with the actual calibrated pressure law

For e_req(n)=nX-P, e_req_prime=X lies between Q0 and Qcap=Q0sqrt(1+epsilon). Any two positive equal-charge increments at the SAME fixed proper volume therefore have ratio at most Qcap/Q0. With one positive global Eunit and charge gamma=hbar/alpha, both conversions cancel from the ratio. The current manifest's exact binary64 epsilon (displayed1e-6) obeys (6405/6403)^2>1+epsilon; root checked this last comparison with exact Fraction arithmetic on the saved scalar, without evaluating any producer.

Thus the WHOLE same finite-cell Nc=0,1,2 ground-energy family cannot be identified with the existing narrow-band P(X) through this fixed-volume/global-unit/global-charge map. An added affine carrier energy, vacuum subtraction, fitted epsilon or charge-dependent normalization would change the retained premise and is not performed. The positive convexity theorem remains true; this stronger necessary shape condition fails.

This excludes one precise reduction, not the single-parent mechanism or UNT. It does not transfer to an unbounded field support, a collective/growth limit, a restricted partial charge domain, changing physical V, or the actual evolving phase component after a derived radiation/interaction/support repartition. The full blank preparation remains affine in conserved total energy. A physical phase-only action must be registered and derived before its shape is tested; no favorable replacement function is supplied. All original physical flags and eleven obligations stay OPEN.

## Actual inputs

| Input relative to J | SHA256 |
|---|---|
| NATIVE_UNIFIED_PARENT_CARRIER_CONVEXITY_AND_MATCHED_LIMIT_V001.md | 77696324b8aa4b1fd908d15b219dd3d13c88e337f562ac25924b4aae703be8b4 |
| native_record_copy_canonical_maxwell_v001.py | 607c84a7ac98776d3e3e34bf508808b2e8e3500088354b02205fdb6995e4e23a |
| NATIVE_CANONICAL_MAXWELL_POSITIVITY_AND_VACUUM_GROWTH_V001.md | 3f57f9b9b0844903aa8dac4bd31c76372e5f6ce613e123b1c535270e03fb43f3 |
| CONSTRAINED_U_FULL_REGULAR_COEFFICIENTS_V002_MANIFEST.json | 3825951def59801f09fea1edcfb632ed91ba13daaced290a98e79c6f3ef7f9b4 |

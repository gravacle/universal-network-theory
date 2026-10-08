# Fixed h=.2: conditional finite-cell carrier chemical-band screen V001

2026-10-06 UTC. New static calculation of a necessary matching condition. This explicitly changes only the incidence flip h in the owned canonical two-endpoint cell from1 to.2; all fixed writer/copy/record/carrier/Maxwell terms remain. It is a conditional finite-cell benchmark of the local-bond choice, not a result for a formed many-cell h=.2 phase. No old Hamiltonian, state, source, result or live job is changed, and no eigensolve or trajectory is evaluated.

For the same held writer, g1,lambda_R1/2,epsilon_psi1,j1/4,t_hop1/2,Omega1,M=8/12/16,kappa=0,+/-1/1000, define H_env,h(k)=[[A,-hI],[-hI,A+D]] and f_h(k)=min spec H_env,h(k). The exact conserved carrier-sector identity is unchanged: E0=f_h(2), E2=E0+2 and E1=1+f_h(7/4). Therefore mu1=1-d_h and mu2=1+d_h with d_h=f_h(2)-f_h(7/4), 0<d_h<1/4.

The same literal operators give (5-sqrt5)I<=A<=(37+sqrt5)I and (681/1000)I<D<(2069/1000)I on7/4<=k<=2. A blank-incidence variational vector gives f_h<=(5-sqrt5), while -hX>=-hI and D>0 give f_h>=5-sqrt5-h. Consequently B=A+D-f_h obeys 0<B<40I for0<h<=1: its upper scalar bound is34.069+2sqrt5+h<40.

For a normalized ground vector [u,v], the lower incidence equation is h*u=B*v. Thus ||u||<(40/h)||v||, implying <n>=||v||²>h²/(1600+h²). Rayleigh comparison at k2=2,k1=7/4 gives d_h>=<n>_k2/4. For h>=1/5 this yields d_h>1/160004 and

    mu2/mu1 > 160005/160003.

The declared binary64 .2 is at least the exact1/5. Root checked this and (160005/160003)^2>1+the actual manifest epsilon using exact Fraction arithmetic on saved scalars; the positive exact squared gap is2901492991424511085883832331/120897115475787770675849555083264. The calibrated cold P(X) has X betweenQ0 andQ0sqrt(1+epsilon), so two positive equal-charge ground-energy increments at one fixed proper volume cannot have a larger ratio. One common positive energy and charge conversion cancels from this test.

Therefore this WHOLE finite-cell h=.2 ground branch cannot be identified with that cold pressure law through the same fixed-volume/global-charge/global-unit dictionary. This is independently derived for h=.2, rather than importing the h1 conclusion. The exact carrier convexity remains positive. A collective/growth limit, physical phase-only repartition or restricted matching domain is a distinct open route; the actual prepared total energy remains affine and is not replaced by this ground state. No affine energy addition, fitted epsilon, vacuum subtraction or favorable source is introduced. The many-cell fixed-local-bond hypothesis and all eleven Stage3 obligations remain open.

The useful next physical calculation is the same-action current/Hilbert/material-source registration and controlled conditional-state reduction, rather than assuming an entire finite-cell ground energy is the late phase energy. The new full-horizon preparation test is separate and continues unchanged.

## Exact inputs

| Input relative to J | SHA256 |
|---|---|
| NATIVE_UNIFIED_PARENT_CARRIER_CONVEXITY_AND_MATCHED_LIMIT_V001.md | 77696324b8aa4b1fd908d15b219dd3d13c88e337f562ac25924b4aae703be8b4 |
| NATIVE_UNIFIED_PARENT_CARRIER_CHEMICAL_BAND_SCREEN_V001.md | 9dcca5302c5fa7fe5c666605b9906926efcb2cfe6ec5ac0cc13d5875822e8f5c |
| native_record_copy_canonical_maxwell_v001.py | 607c84a7ac98776d3e3e34bf508808b2e8e3500088354b02205fdb6995e4e23a |
| NATIVE_CANONICAL_MAXWELL_POSITIVITY_AND_VACUUM_GROWTH_V001.md | 3f57f9b9b0844903aa8dac4bd31c76372e5f6ce613e123b1c535270e03fb43f3 |
| LOCAL_PROPER_BOND_NORMALIZATION_V001.md | 9b4cc5e1942ac7373e210efa46bfa74e03bbcfb8130c01232373b02e8a622a5b |
| CONSTRAINED_U_FULL_REGULAR_COEFFICIENTS_V002_MANIFEST.json | 3825951def59801f09fea1edcfb632ed91ba13daaced290a98e79c6f3ef7f9b4 |

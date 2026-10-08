# Fix the nonlinear filter before estimating its missing stress

2026-10-05 UTC. New explicit geometric extension of the previously specified
flat quadratic filter; not a native graph derivation or a fitted remedy.
Root and an independent analyst checked the auxiliary, lapse and conformal
metric variations. No additional length or numerical coefficient is chosen.

Let u be the normalized physical preferred-clock normal, gamma its positive
spatial metric, D its connection and A_i=D_i ln N. Choose the weighted rough
Laplacian on spatial COVECTORS:

    L_N B_i=B_i-ell^2 N^-1 D^j(N D_j B_i), B=L_N^-1 A.

This specific operator is self-adjoint in N sqrt(gamma) gamma^ij, with
positive elliptic quadratic form for N>0 and periodic/decaying boundary
conditions. It is a counted operator choice; a curvature-modified vector
Laplacian would be a different completion. This statement does not prove
finite-front propagation or remove the previously documented causal issue.

The constant-trace action in c=1 conventions is

    S=(M^2/2) integral N sqrt(gamma)
      [R3+Kij Kij-(1+beta)K^2-2Lambda+4W_F(B)] + S_ordinary,
    partial W_F/partial B_i = F^i(B).

The same inherited force law F and endpoint qualifications are retained.
For deep fields W_F=B^2/2-|B|^3/(3a0)+... . All metric/filter variations
must be taken BEFORE substituting the auxiliary solutions. Flat quadratic
and leading stationary PN limits agree with the saved calculation; this
does not transfer every old fully relativistic Solar or lensing claim.

## Local auxiliary form owns the reciprocal variation

Introduce spatial covectors B_i and lambda_i, and write

    S_acc/M^2 = integral N sqrt(gamma)
      [2W_F(B)+2lambda^i(A_i-B_i)-2ell^2 D_jlambda_i D^jB^i].

The independent equations are L_N B=A and L_N lambda=F(B), so the return
filter is retained. The auxiliaries are elliptic constraints here, not an
unexamined causal replacement with extra kinetic modes.

At fixed spatial metric and auxiliary covectors, exact lapse variation gives

    rho_acc=2M^2[ D_i lambda^i+lambda^i B_i
                   +ell^2 D_jlambda_i D^jB^i-W_F ].

At linear order this is 2M^2 div lambda=-2M^2 f^2 p^2 n, agreeing with
the comoving Poisson clock contribution in the exact dust equations.
The remaining terms and nonlinear corrections to lambda cannot be discarded
when calculating actual source work, homogeneous response or backreaction.

## Spatial trace, including connection and filter response

For delta gamma_ij=2s gamma_ij, with covector components fixed, put
C=D_jlambda_i D^jB^i and

    J_i=-lambda^j D_jB_i-lambda^j D_iB_j+lambda_i D_jB^j
        -B^j D_jlambda_i-B^j D_ilambda_j+B_i D_jlambda^j.

Then delta C=-4s C+J^i D_i s and the spatial stress trace is

    T_acc^i_i/M^2=6W_F-2B_i F^i+2lambda^i(A_i-B_i)
                 +2ell^2 C+2ell^2 N^-1 D_i(N J^i).

This explicitly retains terms missed by replacing S with a background-only
filter after variation. It is not the whole stress of Einstein/trace/dust
or a separately observable matter inventory. Full spatial anisotropic
stress and the preferred-clock equation remain in the complete system.

## Next bounded use

Expand this SAME action, ordinary dust and Einstein/trace terms to the next
order around the saved source trajectory. Regular quadratic sources generate
mean and2k harmonics; the already tested |B|B term generates odd harmonics.
Retain the mean Hamiltonian constraint and homogeneous plane shear. Do not
reset their contributions into a newly chosen background or fit a lapse.
Only after these residuals are controlled should the amplitude/window be
extended or light rays be interpreted as an averaged expansion prediction.

# Independent analytical review: local reference and far-field coefficient

2026-10-04. Source-only review; no evolution, fit, or finite-gradient disk
calculation. This is not a full asymptotic/existence theorem.

The stated local inversion and first gradient coefficient are consistent.
With A=sqrt(G M a0), rM=A/a0 and beta=32/(9 pi^2), the local relation gives
g0=A/R+beta G M/R^2+o(R^-2). For a local mode z+a_s z^3=g, set
b=a_s z^2 and aL=1+3b. On the leading g=A/R profile, direct differentiation
gives

    R^2 (Delta_1 z/aL)/g
      = -2/[(1+b)(1+3b)] - 6b(1+b)/(1+3b)^4.

This expression is uniformly bounded for b>=0 and tends to -2 at each
fixed s>0 as g tends to zero. The finite measure 2s ds therefore permits
dominated convergence in this FIRST correction. In contrast, replacing
z_s by g uniformly at the soft endpoint s=0 would be unjustified. Since
the longitudinal flux derivative is 2g/a0+o(g), the first gradient term
is -a0 ell^2/R^2, with the sign stated in the protocol.

Thus the formal isolated, settled spherical branch has

    g=A/R+[beta G M-a0 ell^2]/R^2+o(R^-2).

Its leading collective homogeneous linearization is
-ell^2 Delta_1 h+(2rM/R)h=0. A free C/R^2 is not a solution: although
Delta_1(C/R^2)=0, the restoring term remains. The decaying large-R WKB
branch behaves as R^(-3/4) exp[-2 sqrt(2rM R)/ell], rather than adding an
arbitrary R^-2 coefficient. This is supporting linearized evidence, not
a proof that all nonlinear branches or spectral boundary data are covered.

The required annulus is outside the ordinary source, with R>>rM,
R>>ell^2/rM (together also implying R>>ell), and negligible external field.
Selection of the regular decaying static branch, control of higher
gradient terms, and admissible soft-endpoint data remain assumptions;
an arbitrary prepared or time-dependent environment is not covered.
No remainder bound at observed disk radii, global existence/uniqueness,
or dynamical relaxation theorem is supplied by this calculation.

For M below/above Mcrit=a0 ell^2/(beta G), the formal circular-speed
asymptote is approached from below/above. Near Mcrit the next term is
essential. The saved catalogue score uses the zero-gradient local proxy;
ell and this finite-gradient coefficient do not enter that score.
Neither agreement of the local reference nor the formal coefficient
qualifies a 100-pc disk prediction, a Cassini estimator, native formation,
or a shared cosmological completion.

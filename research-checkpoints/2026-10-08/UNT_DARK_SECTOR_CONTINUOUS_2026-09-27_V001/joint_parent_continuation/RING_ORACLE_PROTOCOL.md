# Prospective independent Newtonian ring oracle V001

2026-09-28. Code and protocol only until the parent reviews, freezes and
executes the single small worker. No observed velocities are read. Reuse the
unchanged four `galaxy_density.profiles(hi_tail,h2_tail)` reconstructions,
their explicit helium convention, source units and G. This tests their
Newtonian field, not the nonlinear law or an observational success claim.

Freeze this protocol, oracle, density helper, baryon JSON and its declared
source hashes, source preflight, outer-gas decision and original Begeman PDF.
No output is an independent validation if its source identities differ.
Results retain failures and all four profiles; no retry or tolerance tuning
is implemented. No worker is launched by importing the module.

## Fixed numerical definitions

- Compute complete K/E using 20 arithmetic-geometric-mean iterations and
  the DLMF 19.8.5–6 E correction, taking complementary modulus directly.
  Test k=0,.2,.7,.99 against defining-integral Gauss orders128/256.
  Relative/absolute discrepancy, scaled by max(1,absolute reference), <=1e-11.
- Compare elliptic potential/force kernels to direct azimuthal Gauss
  orders128/256 for `(R,a,z)=(2,1,.4),(1,2,.4),(2,2,.4),(8,3,.5),(3,8,.5)`.
  Same discrepancy scale, tolerance2e-10. Explicitly check the (1,2,.4)
  ring has negative radial derivative (outward gravitational contribution).
- Kuzmin control: G=M=a_disk=1; positions `(R,z)=(.7,.2),(1.3,.05),
  (3.7,.2),(8.3,.4)`. Integrate its analytic density to B=1024 on knots
  0,.25,.5,1,2,4,8,16,32,64,128,256,512,1024, additionally split at R.
  Compare quadrature orders48/96 to1e-10; compare exact force/potential
  allowing the analytic omitted-tail bound plus1e-10*max(1,abs(reference)).
  Check finite mass against1−1/sqrt(1+B²) to1e-10. The rigorous bounds are
  G*M_tail/(B−R)^2 for force and G*M_tail/(B−R) for potential.
- Galaxy radii fixed at2.7,8.7,20.7,35.7,43.7kpc, away from density knots.
  Let z0=min(.2kpc,nearest-positive-distance-to-any-knot/4); evaluate
  z0,z0/2,z0/4, at orders48/96. Use each component's identical sigma and
  exact integral. Split all quadrature panels at the union of source knots,
  R, and B; use a=R+z*sinh(u) with its exact Jacobian. B is the maximum of
  all component endpoints plus32 exponential scale lengths where present.
  No physical tail is replaced by this numerical cutoff: retain exact
  omitted mass and conservative force/potential bounds.
- Galaxy48/96 force/potential differences <=1e-8 in max(1,abs(reference))
  units; source quadrature mass plus exact omitted mass must match the
  density helper's total mass to1e-9 relative. Omitted force bound divided
  by max(1,abs(final force)) <=1e-10.
- Retain signed force and potential, including every component. Record
  both height extrapolants2*g(z/2)−g(z); require their relative/absolute
  difference <=1e-3 in the same max(1,abs(reference)) force scale. This is
  a practical numerical convergence criterion, not a rigorous continuum
  remainder theorem. Also retain the analytically slope-corrected sequence
  g(z)−2*pi*G*Sigma'(R)*z as an unscored diagnostic. No sign gate is imposed
  on the galaxy fields, and no field value is clipped or refitted.

Report all20 model/radius cases, both orders and three heights, all analytic
controls, component/total masses, cutoffs, tail bounds, actual elapsed time
and self RSS. The public `field()` can later supply Newtonian boundary
potentials but this worker evaluates no finite-volume boundary mesh.
One BLAS thread; compact JSON only; no observational fit or long-run
checkpoint machinery. The scientific review roles and source custody do
not turn this implementation into an independent observation.

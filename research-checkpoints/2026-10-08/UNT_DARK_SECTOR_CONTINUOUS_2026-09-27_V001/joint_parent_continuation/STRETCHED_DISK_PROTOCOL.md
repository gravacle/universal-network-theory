# Prospective extended disk solver qualification

The uniform-grid exact Kuzmin benchmark passed all nine cases. To reach a
galaxy's remote boundary while resolving its centre, use the same cylindrical
finite-volume equation on edges R_i=z_i=expm1[i log(1+L)/N]. Cell centres are
arithmetic edge midpoints, not logarithmic points. Shared conductances are
R_face dz/dR_centres and [(R_high²-R_low²)/2]/dz_centres. Face transverse
derivatives are linearly interpolated between centres; boundary tangential
derivatives remain exact for this benchmark. Keep the same frozen flux law,
Picard update, linear/nonlinear tolerances, clipping rejection, flux balance,
small-case restart and no-overwrite result publication.

Run N=64,128,256, L=8, eta=.01,1,100. Require decreasing maximum radial-force
error at each refinement and finest error below2% on .5<=R<=4. Then run
N=256,L=128 at the same three eta, requiring below2% over that same interval.
Retain all12 cases. An additional Newtonian eta=1,N=128,L=8 solve must achieve
below2% and the same conservation tolerance; no Newtonian model is fitted.

For exact boundaries integrate the known spherical response in log radius:
Phi(s)-Phi(1)=integral_0^log(s) exp(t) g(eta exp(-2t)) dt. Compare64- and
128-point Gauss values at relative tolerance1e-9 using max(1,max|Phi|) scale.
This is a conditioning change of integration variable, not changed physics.
The initial potential is scaled Newtonian, not the exact nonlinear interior.
The source integrates the exact Kuzmin annular density. Require annular-mass
identity1e-13, zero clipped faces, convergence and positive scored forces.

The later observed-density calculation still needs declared source tails and
an approximate remote boundary checked by enlarging the domain. Passing this
exact-boundary benchmark does not eliminate that later boundary test.

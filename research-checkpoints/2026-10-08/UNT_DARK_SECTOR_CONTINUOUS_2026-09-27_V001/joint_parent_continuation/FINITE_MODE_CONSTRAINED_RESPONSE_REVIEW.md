# Root independent check of the finite-mode metric/clock system

2026-09-28. Reviewed the complete analytical note and independently rederived
its constraint reduction and physical-tilt equation. No numerical worker or
change to the candidate/source is involved. Reviewed pathway SHA-256:
`5f6116f2f803fda9c0cd7d60e18c3392e346bab4944ea2fdaef3175756245db3`.

## Result

The note establishes a positive, finite-dimensional constrained longitudinal
response in the specified unexcited finite-band classical completion. The
exact positive-vacuum de Sitter version has decaying internal modes and
decaying physical foliation tilt, not merely a favorable clamped-source
oscillator test. Its conserved polarization charge is signed and has zero
mean on the periodic domain; it does not provide a positive homogeneous
missing-matter abundance. This is a useful consistency result with a sharply
specified scope, not full stability of UNT or its continuum limit.

## Independently checked reductions

For the local scalar ADM variables the Einstein extrinsic-curvature terms
give `-3 M² zeta_dot² + 2 M² zeta_dot Delta beta`. The spatial curvature
gives `M²[(grad zeta)²-2n Delta zeta]`, up to boundary terms. At zero mode
background the proposed oscillator action contributes only its own positive
kinetic/stiffness terms and `C grad n.grad S`. The shift therefore enforces
`zeta_dot=0`, while the lapse gives `zeta=-S/K_b`; together they conserve S.
There is no additional static `J_Y` contact to insert before elimination.

At fixed S, writing `sigma=(S/K_b)d+z`, with `d_j=1/delta_j` and
`b^T z=0`, uses `K d=b` and `b^T d=K_b` to remove both the constant potential
and cross term. The remaining mass and stiffness quadratic forms are
strictly positive on the finite tangent space. The exact augmented
determinant is `det(K-y M)*b^T(K-y M)^-1 b`. Its polynomial expression has
degree N-1. Simple roots interlace positive individual frequencies; repeated
poles retain the stated source-orthogonal dark modes. Replacing this by
`K_b-chi=0` would indeed solve a different, unconstrained source problem.

For de Sitter with the inherited positive DeltaU, eliminating the shift gives
`n=zeta_dot/H`. Integrating the remaining Einstein spatial terms cancels
them because H is constant. The retained mode action then has the displayed
cyclic-zeta coupling, yielding `(a² S/H)_dot=0`. Tangent modes obey a positive
matrix oscillator equation with friction 3H. The charged reference solution
decays as a^-2 and drives the tangent equation with `2H² M x0`; the possible
resonance is `t*a^-2`, not an exponentially growing solution.

The linear lapse source is `delta rho=-C(k/a)S`; the kinetic and quartic
energies are second order, and there is no linear momentum, pressure or
anisotropic-stress source here. Consequently the vacuum Einstein constraints
give `Phi=Psi=a S/(K_b k)`. These decay as a^-1 while the signed polarization
density decays as a^-3. In the adiabatic limit `b^T K^-1 b=K_b` recovers the
previous positive reduced `j=-1` clock action with its correct coefficient.

A coordinate lapse can grow for a very slow mode, so it alone is not an
adequate physical check. In Newtonian gauge, directly differentiating the
normalized clock normal gives `v_hat=-grad pi/a` and
`a_hat=v_hat_dot+H v_hat+grad Phi/a`. Its driven solutions are the stated
decaying exponentials, with a decaying `t*a^-1` resonance. This closes the
specific physical-tilt question at linear order for a finite positive band.

## Scope that must travel with the result

The zero-curvature reduction is not an exact vacuum solution with the
positive matched constant retained; the note's separate de Sitter calculation
addresses that limitation rather than taking an invalid H-to-zero limit.
All divisions by nonzero k and H are explicitly restricted. The quadratic
zero-field problem cannot prove nonlinear restoration or preparation of the
nonanalytic continuum static branch. A finite positive band's force law also
differs at sufficiently small source from the ideal zero-cutoff continuum.

No uniform zero-gap estimate, arbitrary excited-background stability,
ordinary-matter perturbation transfer function, nonlinear foliation
regularity, spatial propagation speed, or causal hyperbolic continuum limit
has been established. Native inertia, source overlaps, contact, mode
population and physical volume/time matching remain independent requirements.
Within those limits no algebraic blocker was found in the reviewed result.

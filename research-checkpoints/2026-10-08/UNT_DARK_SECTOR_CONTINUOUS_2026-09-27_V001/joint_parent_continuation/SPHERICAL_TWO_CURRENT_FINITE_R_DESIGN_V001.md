# Conservative finite-R spherical two-current design V001

2026-09-29. Prospective, analytical/inert implementation design. Root alone
compiles or runs scientific producers. The same two R=128/8192 method states,
compact ordinary seed, initial uniform hard action, ell=3.2 kpc, physical
normalization and late background are retained from the reviewed spherical
shadow. No fitted dark profile, new abundance, viscosity, shock entropy law,
native-to-seconds mapping or observational gate is introduced.

## 1. Actual equations, not a pressure-residual proxy

Use x=r/(A ell), tau=t/t_dyn, t_dyn=sqrt(ell/gstar), v=v_pec/sqrt(gstar ell),
q_s=A^3 rho0_s/(M/ell^3), m_s=q_s v_s, and epsilon=gstar ell/c^2.
Ordinary matter has zero intrinsic pressure; the hard current uses exactly

    I = I1 q_H/(A^3 q_H1),
    u = S beta (e(I)-R I),
    p = S beta (I omega-e),
    P = A^3 p / [(M/ell^3) gstar ell],
    dP/dq_H = (omega/R)cI^2/epsilon.

Here S=gstar^2/(4pi G Kb), beta=.005 and q_H1 follows the saved I1, not
the full energy divided by c^2. This is the explicitly adopted cold/weak-field
current action, not an exact Einstein fluid. Evolve both species:

    q_tau + (x^2 q v)_x/(A x^2) = 0,
    m_tau + [x^2(q v^2+P)]_x/(A x^2)
      = -Ht m - q Mex/(A^2 x^2) + 2P/(A x),
    Mex(x) = 4pi integral_0^x (q_b+q_H-qbar) y^2 dy.

The ordinary seed moves. Hard pressure changes its own current and hence the
shared gravity. The zero-pressure shadow is only a comparison/control, never
the finite-R generator. A finite-volume implementation must cancel constant
pressure geometrically and accumulate excess mass directly.

## 2. Selected spatial discretization: variational moving shell volumes

Use a separate ordered radial mesh for each current, with fixed positive cell
masses m_sj, faces x_si and exact volumes V_j=4pi(b^3-a^3)/3. The ordinary
initial cell masses integrate the compact polynomial exactly plus the cosmic
ordinary density; hard masses integrate its uniform cosmic density. No
Eulerian remapping, artificial mass diffusion or cross-species mass exchange
is needed. Both meshes initially have the same uniform face positions.

Cell q=m/V, physical rho0=(M/ell^3)q/A^3. Lump half each adjacent cell mass
onto an interior face, with half the last cell mass at the outer face. Origin
position/velocity are fixed at zero; its kinetic contribution is zero. Write
face mass w_i and canonical momentum p_i=A w_i v_i. The discrete action is

    L = sum_i w_i A^2 xdot_i^2/2 - U(A,x_H) - W0(x_b,x_H)/A,
    U = sum_hard_cells m_j dE(I_j)/epsilon,
    dE = e/(RI)-1 = [omega/R-1] - p/(RI).

The pressure derivative is exact for this finite-volume internal energy:

    p_i,dot|pressure = 4pi x_i^2 (P_left-P_right),
    x_i,dot = p_i/(A^2 w_i).

Ordinary P=0. Hard outer traction uses the same homogeneous Pbar(A), explicitly
an exterior boundary condition, not a hidden halo wall. Retain its signed
work. Uniform density/zero peculiar velocity is an exact geometric pressure
balance. Ordered faces/positive volumes are mandatory, not enforced by
clipping or a density floor.

## 3. Exact discrete shared-gravity derivative

Within each moving cell use its constant density q_j. Define the finite
two-species self potential phi_self=-integral dm'/max(x,x') and the fixed
background subtraction phi_bg=-(2pi/3) qbar x^2. Let phi=phi_self+phi_bg.
The gravitational potential energy is

    W0 = (1/2) sum_cells m_j <phi_self>_j
                       + sum_cells m_j <phi_bg>_j.

Its derivative at an interior face is

    W0_,xi = 4pi xi^2 {q_left[phi_i-<phi>_left]
                              +q_right[<phi>_right-phi_i]}.

At a last face retain only its left-cell term. Thus the gravitational kick is
`p_i,dot|gravity = -W0_,xi/A`. The finite-cell force is the derivative of the
same discrete self-energy, not a density force paired with an unrelated
energy diagnostic. It approaches the Gauss force under mesh refinement.
Each species' cells can overlap the other's; this is not a crossing of a
single species' ordered faces.

Evaluation needs no dense pair matrix. Sweep the sorted union of both meshes.
On each union interval [a,b], qtot is constant, B=M(a)-4pi qtot a^3/3, and

    phi(x)=K-B/x+(2pi/3)(qtot-qbar)x^2,
    K=-4pi integral_b^L qtot(y)y dy - 2pi qtot b^2.

Integrate x^2 phi analytically to obtain all cell averages; B=0 at the origin.
Potential constants from exterior spherical cells cancel exactly in each
interior force derivative. Use compensated/accurate sums and retain the
homogeneous-force null and directional energy-gradient controls. W0 fixes a
specific background potential convention; it is not the GR absolute vacuum
energy or an observed lensing mass. Exterior missing matter affects forces
only outside its inner support, by spherical symmetry.

## 4. Energy, work and cosmological omissions

For T=sum p_i^2/(2A^2 w_i) and W=W0/A, the semidiscrete action gives

    d(T+U+W)/d tau = -Ht [2T+W+3 sum_cells P_j V_j]
                     -4pi x_H,out^2 Pbar xdot_H,out.

Track every term, including the outer pressure work and Hubble exchange.
Also track T+U directly against actual gravity work, Hubble work and outer
pressure work, so no potential-zero convention can conceal a mechanical
defect. Subtract the homogeneous internal energy only as a separately shown
excess readout; retain its time derivative when comparing excess ledgers.
Mass/action conservation is exact at the fixed-label level, but energy/time
accuracy and continuum consistency still require independent controls.

At every sample retain dE,dW, cN^2, velocities, potential span and hard active
energy/pressure corrections. The generator still uses rest gravity and the
inherited late background without ordinary radiation. Report those omissions
separately, with no assertion that their small pointwise values prove the
accuracy of an arbitrarily tiny incremental lensing signal.

## 5. Domain fixed before new outcomes

Keep the inherited times 0,1/64,1/32,1/16. Use initial outer interfaces
L=8 and16 ell, fixed watch radius4 ell, and compare the same physical interior.
These are numerical exterior interfaces, not halo radii. Prospective domain
guards are A>=1, |v_s|<=2 vdyn and 1/4<=I_H/Ibar(A)<=4, with positive ordered
meshes. A guard failure is retained as an unfinished numerical/domain case;
it neither clips the state nor rejects the physical model.

The zero-source quartic bound eII<=1/R^2 (the eta=0 case of the previously
proved global derivative cap) gives cN^2/c^2<=I/R^3. While these guards hold,

    integral_0^T max(|v|+cN/vdyn)/A d tau
      <= T [2+sqrt(4 I1/(R^3 epsilon))].

Outer faces move by at most2T. Require this prior bound to be smaller than
L-2T-4 for each retained state/interface, before evolution. An actual solution
satisfying the guard then cannot convey the chosen outer acoustic/advective
boundary data to the watch region in this interval. The numerical samples
and integrator stages test the guard but are not an analytic interval proof.
Spherical exterior gravity supplies no additional interior acceleration.

The numerical plan must compare identical cell widths on both interfaces,
independent time refinement and a dust-pressure-off control against the saved
shadow. Pressure-off is a declared control, never a successful finite-R
replacement. Mesh refinement must track density/velocity gradients and
energy, not only enclosed mass. No artificial viscosity is added: a loss of
ordered cells, unresolved gradient growth or failed refinement gives no
post-crossing continuation. This scheme is intended only for the classical
single-phase interval of each current, not a merger/shock model.

## 6. Numerical protocol/source status

This is the inspectable exact-action design; the companion inert source is
`spherical_two_current_v001.py` and its concrete prospective protocol is
`SPHERICAL_TWO_CURRENT_PROTOCOL_V001.md`. All inherited numerical criteria stay
unchanged. Any new spatial comparisons will be explicitly prospective and
retained, never adjusted to select a favorable gap or an observed profile.
No numerical producer, quadrature, orbit inversion or compiler was executed
while preparing this design.

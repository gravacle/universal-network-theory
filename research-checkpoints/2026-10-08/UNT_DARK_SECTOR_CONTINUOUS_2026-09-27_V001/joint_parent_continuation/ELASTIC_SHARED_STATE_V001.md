# Elastic shared state: a galaxy–growth consistency test

2026-10-04 local / 2026-10-05 UTC. Continuation of frontier V131. This is a
new, conditional material completion, not a native graph derivation. Its
purpose is to test the concrete suggestion that elastic network structure
can hold the galaxy state while the same state supplies the cosmic history.
No new observational fit is authorized by this note.

## One action and the assumptions it adds

Use three material coordinates X^I, B^IJ=g^mu nu partial_mu X^I partial_nu X^J,
n=n_ref sqrt(det B), and C=B/(det B)^(1/3). The associated volume-form current
J^mu=(n_ref/6) epsilon^mu nu rho sigma epsilon_IJK partial_nu X^I
partial_rho X^J partial_sigma X^K is identically conserved. The material
velocity is independent of the preferred clock normal defining the spatial
filter. Keep physical ell fixed, not a function of n.

The material/source energy is

    epsilon(n,b) + mu_sh(n)/4 [tr(C^2) - (tr C)^2/3],
    epsilon=a0(n)^2 u(|b|/a0;r)/(4 pi G), b=S a_clock,
    S=(1-ell^2 Delta_perp)^(-1),
    epsilon(n,0)=rho_Lambda+m_g n,
    mu_sh=kappa m_g n.

All rho here are energy densities. The bare Einstein/matter action and its
weak-field g^2/(8 pi G) energy remain present. The last two functional
choices are additional effective hypotheses. The affine homogeneous energy
was motivated by an exposed dust-plus-constant target; its abundance and
absolute normalization are not derived. Changing n changes a0 BEFORE
variation; the epsilon_n force is not optional.

On isotropic FLRW, C=I and both the shear energy and its first variation
vanish. Hence n=n_ref a^(-3), rho_U=rho_Lambda+m_g n, p_U=-rho_Lambda.
The shear invariant is 4 e_dev:e_dev to quadratic order. The material
principal speeds at b=0 are

    c_T^2/c^2=kappa, c_L^2/c^2=4 kappa/3.

Positive material stiffness and subluminal material speeds require
0<kappa<=3/4. This is not a certificate for the entire metric/filter system.
These continuum elastic identities are not new UNT results; see
[Battye and Moss](https://arxiv.org/abs/astro-ph/0703744). Here they are derived
for this explicitly specified energy and combined with its source work.

## The local strain is determined rather than assigned

Let x=|b|/a0, Q=u(0), u'=-x(1-mu(x)), and

    eta(x)=[2u-xu']/(2Q)-1,
    f_n=m_g n/(rho_Lambda+m_g n),
    k_b=n epsilon_nn/m_g=f_n x^3 mu'(x)/(4Q).

The inherited monotone bounded response has eta<0 and k_b>0 at x>0.
For displacement zeta on a fixed Euclidean spatial background,
delta=delta n/n=-div zeta. Joint first order in weak imposed forcing gives

    kappa[Delta zeta+(1/3)grad div zeta]=grad(Phi/c^2+eta),
    delta=-(Phi/c^2+eta)/(4 kappa/3).

The second equation needs the homogeneous longitudinal solution fixed by a
specified relaxed boundary. A truly isolated MOND logarithmic potential has
no finite Phi(infinity)=0: use a compensated source or a finite/external
cosmic matching boundary, not a nonexistent isolated lapse normalization.
At finite prescribed b, retaining density-linearized source coefficients
adds k_b to the denominator. It does not make this a global galaxy solution.

The induced normalization change is delta a0/a0=(f_n/2)delta at linear order.
For an attractive well, Phi and eta reinforce rather than cancel compression.
If the static filtered field is eliminated in a local parallel Fourier mode,
with s=(1+ell^2 k^2)^(-1), its clamped stiffness is

    K=1-s^2+s^2[mu+x mu'],
    k_b,relaxed=k_b [1-s^2+s^2 mu]/K.

It is positive and no greater than k_b. This Schur complement is a local
constitutive Hessian, not full gravitational stability. The prior mobile
fluid failure concerned global force balance, not a negative local bulk
modulus. Spatial metric strain, self-gravity, source variation and nonlinear
strain are absent from this local estimate and remain required for galaxies.

## Linear cosmology follows from the same action

At b=0 the expansion is

    epsilon=rho_Lambda+m_g n-b^2/(8 pi G)
            + |b|^3/(12 pi G a0(n)) + higher terms.

The quadratic acceleration coefficient is independent of n. The cubic
clock term is present, but its first mixed delta n |b|^3 term is FOURTH order.
Thus the galaxy nonlinearity does not give a linear material–clock source.

Set c=1 temporarily. With T=t+pi_clock, Newtonian potentials Phi,Psi, and
Upsilon=Phi-pi_clock_dot, the quadratic Fourier clock action is

    L_clock,2=M^2 a k^2 f_k(a)^2 Upsilon^2,
    f_k=(1+ell^2 k^2/a^2)^(-1), M^2=1/(8 pi G).

It implies partial_t[a f_k^2 Upsilon]=0. Its density perturbation is
delta rho_clock=-2 M^2 k^2 f_k^2 Upsilon/a^2, proportional to a^(-3).
The filter's time dependence cannot generate a charge from zero. On the
zero-initial-charge branch, Upsilon=0 and this linear density vanishes.
Supplying a nonzero arbitrary C_k is additional initial-state content, not
an automatic galaxy-driven cosmic enhancement. Filter/metric perturbations
of an already quadratic acceleration term do not alter this quadratic result.

For scalar material displacement pi_i=partial_i pi_m,

    delta_g=3 Psi-Delta pi_m, theta_g=-a^2 pi_m_dot,
    delta_g_dot=Delta theta_g/a^2+3 Psi_dot,
    theta_g_dot=Phi+(4 kappa/3)(delta_g-3 Psi),
    delta rho_g=m_g n delta_g, delta p_g=0,
    delta T^i_j,TF=-2 kappa m_g n(partial_i partial_j-delta_ij Delta/3)pi_m.

Absent other anisotropic stresses,
Phi-Psi=16 pi G a^2 kappa m_g n pi_m. In particular, setting Phi=Psi in this
elastic model is incorrect. These equations and the Einstein constraints
give an actual mixed growth/lensing response, not an imported Jeans analogy.

## Frozen small numerical comparison (before execution)

The one new driver will evaluate eta and k_b at x=0.1 and 1, then evolve
the same reviewed scalar system. No microscopic run, observational fit,
recombination rerun or parameter optimization is needed.

Use an explicitly EXPOSED reference background H0=70 km/s/Mpc,
Omega_b=.05, Omega_g=.25, Omega_Lambda=.70, no radiation, a=.01 to1.
These are illustrative benchmark inputs, NOT a fit to the inherited absolute
endpoint: with the inherited a0,r that normalization still is not supplied.
f_n=.25/(.25+.70) is used only for the present local comparison.
Use comoving k=.1/Mpc and equal dust growing-mode material data at a=.01.
Reconstruct Phi separately for each kappa; do not fix it to the dust value.
The data are valid finite-epoch Cauchy data, not a regular primordial mode.
Use amplitude |Psi_i|=1e-9 to stay linear; it cancels in response ratios.

Declare a 10% maximum local density-strain size solely to test the shared-
state linear approximation. This is NOT an observational tolerance. With
Phi=0 (optimistically omitting the attractive well), compute

    kappa_local(x)=(3/4) max(0, |eta(x)|/0.1-k_b(x)).

The clamped k_b is the largest of the stated relaxed local susceptibilities,
so this is an optimistic local stiffness, not proof that a galaxy qualifies.
Compare kappa=0 and those two calculated stiffnesses. No choice is made by
examining growth outputs. Density/velocity, both potentials, their sum and
constraint errors are retained. The sound term is evolved explicitly.

With x_time=ln a, E=H/H0, K=ck/H0, v_i=H0 theta_i, the driver uses

    Psi= -3/(2 a K^2) sum_i Omega_i(delta_i+3 E v_i),
    Phi=Psi+6 kappa Omega_g/(a K^2)(delta_g-3 Psi),
    Psi_x=3 sum_i Omega_i v_i/(2 a^3 E)-Phi,
    delta_i,x=-K^2 v_i/(a^2 E)+3 Psi_x,
    v_b,x=Phi/E,
    v_g,x=[Phi+(4 kappa/3)(delta_g-3 Psi)]/E.

Controls frozen before output: 128/256-point modal and source integral
agreement at relative 2e-6; B'=-x^2 mu' checked by central difference at
2e-5; source u' check at 2e-6; eta small-x limit checked at x=.001 within
1%; positivity at the tested points; RK4 levels2048/4096/8192 with final
delta/Phi/Psi agreement at absolute2e-4 relative to the nonzero reference
amplitude (not to a possibly near-zero oscillatory result); independently
differentiated algebraic Psi constraint at normalized2e-8; kappa=0 density
growth against the integral solution at2e-6. Preserve any failed controls;
do not relax tolerances to rescue the branch.

Root and endpoint_equations_check independently derived the material stress,
speeds and source response. handoff_plan_review_v005 independently checked
the finite-source Hessian, filtered clock conservation and exact scalar ODE.
This does not complete Stage3, derive formation or establish superiority.

## Freedom and evidence ceiling

Inherited: calibrated a0 and r, fixed development ell, endpoint choice and
filtered response functional. Added: three material coordinates/current,
affine density law, abundance m_g n_ref and its formation/initial data,
shear invariant and proportional shear law with one new parameter kappa,
independent material/clock relation and a covariant spatial filter choice.
The two kappa values are diagnostic consequences of a declared small-strain
test, not calibrated successful physical parameters. The absolute endpoint,
galaxy forward predictions, radiation era, optical response and full coupled
stability remain unqualified. Relabeling an unselected material energy as
network energy would not by itself remove an independent dark component.

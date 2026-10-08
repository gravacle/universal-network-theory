# Quantum production is a genuine alternative, with a joint static constraint

2026-10-03. New analytic diagnostic of the existing explicit-mode action.
Status: **conditional finite quantum extension, not an adopted UNT law**.
No numerical histories, fit, new abundance, source coupling or cutoff is added.
This note does not quantize an arbitrary quadrature used by an old classical
solver. It retains the classical results and identifies the physical inputs
needed before a quantum calculation can advance the shared model.

## 1. What the classical zero-state argument does not exclude

`EXPLICIT_MODE_COSMOLOGY_PATHWAY.md` (SHA256
`5a99341c9abb3a35f3f6b59f54bf07cdc5f623016f8bdc9b1c2327f749d52067`)
retains the same quartic response modes in a covariant action. Its homogeneous
physical coordinate obeys

    m(qddot+3H qdot)+k q+u |q|^2 q=0,   k=kappa delta^2, u>0.

Exactly zero classical coordinates and velocities stay zero. This does NOT
show that a quantum state with zero mean has zero energy, covariance or
production. The action itself explicitly leaves quantum production untested.
The native finite BS parent is already quantum; this is a possible matching
of its modes, not a reason to quantize a previously quantum-effective response
a second time. Whether the phenomenological coefficients are bare finite
Hamiltonian coefficients or already effective ones must be settled first.

For a finite physical comoving cell V_c and a finite mode with declared weight
w>0, put V=V_c a^3 and A=C w V. The reduced physical Hamiltonian at zero source is

    H_q=P^2/(2 A m)+A[k |q|^2/2+u |q|^4/4],
    [q_i,P_j]=i hbar delta_ij.

The normalization A matters: rescaling a classical action without changing
its classical equations changes its quantum spectrum. A quadrature weight is
not, by itself, a physical species count or cell normalization. If these are
independent homogeneous coordinates in one arbitrary cell, their number per
proper volume cannot be chosen to obtain the desired cosmological density.

For the harmonic limit, omega^2=k/m and v=sqrt(A m) q. Removing the cross term
by a time-dependent canonical transformation gives

    vddot+[omega^2-(9/4)H^2-(3/2)Hdot]v=0.

This transformed frequency is not an extra physical negative-energy term.
The physical harmonic energy in those coordinates is

    H_q=1/2[(p_v-3H v/2)^2+omega^2 v^2].

For the quartic model add u |v|^4/(4 A m^2). Expanding backgrounds can change
covariances and excite a specified state, even when <q>=0 remains exact.
The original action has no spatial-gradient operator. Extending it to all
spatial Fourier modes does not supply a high-wave-number cutoff or physical
propagation law. A spatial/mode-density completion is required, not borrowed
from the usual scalar-field vacuum by analogy.

## 2. Exact production control and its complete work

One harmonic component gives an analytic positive/control test without a new
solver. Start in its ground state at A_i. Prescribe an ideal instantaneous
parameter change a_f/a_i=s>0, so r=A_f/A_i=s^3, while keeping omega fixed.
The state is unchanged at the quench, but its energy becomes

    E_f=hbar omega (r+r^-1)/4,
    n_f=(r+r^-1-2)/4=sinh^2[(3/2) log s],
    W=E_f-E_i=hbar omega n_f >=0.

There are three such components for a harmonic vector oscillator. In the
adiabatic limit, the state instead tracks the ground state and n_f tends to
zero. These exact alternatives demonstrate possible excitation, not unavoidable
production at a prescribed abundance. The positive energy comes from work by
the parameter source. The jump is a clamped idealization, not a solution of
the Friedmann equations or evidence that the network chooses a(t).
Self-consistent evolution must retain the expansion source and backreaction.

The displayed n_f formula is exact for u=0, not a production solution of the
positive-quartic parent below. The full quartic instantaneous quench has the
equally exact moment identity

    E_f=<T_i>/r+r(<V2_i>+<V4_i>),
    W=(r^-1-1)<T_i>+(r-1)(<V2_i>+<V4_i>).

For its initial ground state, E_f-E_0(A_f)>=0 by the variational principle,
but W need not be positive: expansion can extract energy as the instantaneous
quartic ground energy decreases. Excitation ABOVE the new ground and total
source work are different quantities. A same-parent numerical production
claim must use the quartic evolution or bound its harmonic approximation.

The finite-cell stationary stress is also constrained. Write T=P^2/(2Am),
V2=A k|q|^2/2 and V4=A u|q|^4/4. For any normalizable energy eigenstate with
the usual virial domain, Hellmann--Feynman and the virial identity give

    p=-dE/dV=(<T>-<V2>-<V4>)/V,
    2<T>=2<V2>+4<V4>,
    rho=E/V=(2<V2>+3<V4>)/V,
    p=<V4>/V >=0,   0<=p/rho<=1/3.

This includes the ground state for a fixed finite comoving mode census.
Its harmonic endpoint is matter-like; its pure quartic endpoint is radiation-
like. These stationary positive fluctuations do not themselves accelerate
expansion. Nonstationary squeezed states need their actual stress; a virial
average requires separation from expansion and relaxation timescales. This
result is NOT a general statement about a renormalized quantum-field vacuum.
A changing physical cutoff/species count and counterterms alter the problem.
The previously matched C DeltaU remains separate and is not rederived here.

## 3. The same quantization changes the galaxy contact cancellation

One must not claim quantum cosmological production while silently leaving the
classical zero-temperature source response untouched. At a fixed physical
cell, source a Cartesian direction of the same three-dimensional oscillator:

    H_f=P^2/(2Am)+A[k |q|^2/2+u |q|^4/4-f x].

At f=0 its confining rotationally invariant ground state psi_0 is unique and
positive. Let R=(H_0-E_0)^-1 on its odd l=1 sector. The exact static response is

    chi=partial_f <x>|_0=2A <x psi_0,R x psi_0> >0.

The ground-state Ehrenfest identity is k<x>+u<|q|^2 x>=f. Differentiate it:

    1=k chi+u eta,
    eta=2A <|q|^2 x psi_0,R x psi_0>.

The two vectors have the same l=1 angular harmonic and strictly positive
radial factors. The radial l=1 resolvent lies below that sector's spectrum
and has a strictly positive Green kernel. Hence eta>0. For k>0 this proves

    0 < k chi < 1.

At k=0 the finite quartic oscillator still has a positive gap and finite chi.
This is a finite-Hamiltonian theorem, not a numerical response fit.

Now retain the SAME old classical contact K_b=kappa sum_j w_j and the source
f_j=kappa delta_j h(g), with h(0)=0 and h'(0)=1. For finitely many physically
normalized modes with w_j>0 and delta_j>0, the small-g derivative of the full
effective energy per C is

    D_raw(g)=[K_b-sum_j w_j (kappa delta_j)^2 chi_j]g+O(g^3),
    K_res=kappa sum_j w_j [1-kappa delta_j^2 chi_j] >0.

The quantum ground state leaves a positive linear stiffness. The exact
classical contact cancellation does not survive this finite bare-oscillator
quantization. With the same isolated spherical algebraic interface this
would eventually return an inverse-square, not asymptotically flat, force.
No claim is made that the crossover lies in observed galaxies. Even the
classical finite-gap approximation only represented a finite MOND-like window;
its exact far asymptotic was not the gapless continuum law.

A different counterterm/contact, non-vacuum state, many-body thermodynamic
limit or quantum-effective matching could change the conclusion. Each is a
changed physical premise requiring the SAME galaxy/cosmology/work comparison,
not an invisible correction to protect a desired answer. The true continuum
cannot be replaced by ever more quantum species as a quadrature is refined.

## 4. The missing matching has an explicit scale

For one bare oscillator define

    ell=(hbar^2/(A^2 m u))^(1/6),
    E_Q=hbar^(4/3) u^(1/3)/(A^(1/3) m^(2/3)),
    zeta=k/(u ell^2),   f_Q=u ell^3=hbar sqrt(u/m)/A.

Then H/E_Q=-laplacian/2+zeta r^2/2+r^4/4-(f/f_Q)x in dimensionless
coordinates. At k=0 the gap is a positive dimensionless constant times E_Q,
and chi is a positive dimensionless constant divided by u ell^2. Thus the
static quantum crossover and excitation scale depend on A and m, which the
old static galaxy law did not determine. Large physical A can make the
quantum correction small in a finite classical window. It cannot be freely
chosen per galaxy or cell to make the residual disappear.

This specifies a useful comparison once native poles/residues and physical
cell normalization are available; it does not provide their values. A new
dimensionless oscillator grid before those inputs would only map a known
conditional family, not determine the missing cosmological abundance.

## 5. The operational native clock gives a decisive saved-state test

The old native first-moment rule already ruled out a fixed canonical linear
incidence-source representation over arbitrary protocol-time states. The newly
available operational record clock permits a stronger question: does that
mismatch disappear when the probe uses the network's own measured phase?

Keep the SAME original held states, with no carrier reset/SWAP. An incidence
source H_port=-hbar alpha_dot n implements U_alpha=exp(i alpha n), where alpha
is dimensionless action. Let R_O(tau)=i<[O(tau),n]> be its derivative at zero
kick. The native held identities give

    R_n(tau)=h<X> tau/hbar+O(tau^2),
    [H,A_L]=(epsilon_r-lambda_R n)A_L,
    R_A(tau)=-i lambda_R h<X A_L> tau^2/(2 hbar^2)+O(tau^3).

The pulse changes neither the initial clock amplitude nor its initial phase
rate nu. At later lag its phase response is R_phi=Im(R_A/<A_L>)=O(tau^2).
The readout at FIXED measured phase theta, including its time adjustment, is

    R_n|theta=R_n-(d<n>/dt)/(dphi/dt) R_phi,
    R_n|theta(theta)=[h<X>/(hbar nu)] theta+O(theta^2).

The coefficient is S_theta=S_time/nu, NOT S_time/nu^2. This convention fixes
an action kick; a force-normalized kernel requires its own source conversion.
All other held terms commute with n, so the exact bulk kick work is

    W_kick=h[(1-cos alpha)<X>+sin alpha<Y>].

No pulse was numerically performed; this is its full bulk work identity, not
a computation of actuator preparation or readout cost. No finite kicked-clock
window is qualified by the old unperturbed clock certificate.

All three existing preparations and all five ages were included in one small
saved-scalar calculation, authenticating the original inputs through the
previous saved-arithmetic result. It passes 70 assigned consistency checks at
the unchanged 1e-10 allowance. The algebra and rounded outcomes were inspected
before this reproducibility calculation; it is not blind or unused evidence.
Constancy and signs are NOT numerical correctness gates.

| Held age | Native S_theta | Feedback-off S_theta |
| ---: | ---: | ---: |
| 0 | 1.1524685203 | 0.9348647038 |
| 0.25 | 1.1714508538 | 0.8353938220 |
| 0.5 | 0.9628304521 | 0.5601243835 |
| 1 | 0.4427936557 | 0.1384765023 |
| 2 | 0.6477210984 | 0.6846467482 |

Feedback-off has nu=1 and zero clock response to this kick at EVERY lag;
its changing slope is not a clock backreaction artifact. Copying-off has
five null relational coefficients because its phase clock is undefined, not
because its protocol-time incidence response vanishes. Native slopes span
0.4427936557 to1.1714508538 at fixed record count and fixed source convention.

A canonical surrogate whose clock, linear source and kinetic normalization
are fixed has a state-independent double commutator, including with quartic
potentials. The measured-phase change therefore rejects an EXACT all-age
identification of that sort for this incidence channel. It does not reject
nonlinear source operators, a derived clock coupling, memory or a qualified
collective-state limit. Incidence is not the adopted energy-dipole gravity
insertion. The separate 96D energy-dipole stationary comparison already has
negative numerical static susceptibility in every inherited preparation; it
cannot be replaced by a passive ground spectrum, with its original rigorous-
gap and state-preparation caveats retained.

Native transition spectra are already quantum. A positive harmonic pole with
gap Delta and signed weight W, in one physical source convention, has response
residue R=2 Delta W/hbar^2 and frequency Omega=Delta/hbar. If it truly matches
ONE harmonic coordinate, then m=kappa delta^2/Omega^2 and
A=R/(kappa Omega^2)=2W/(kappa Delta). A negative weight cannot make this
positive realization. Even positive lines may be transitions of the SAME
native degree of freedom, not distinct oscillators. Linear response matching
does not license adding their zero-point energies to the native energy they
already represent. A quartic mode requires its full transition pattern;
its gap is not generally hbar sqrt(k/m).

Source `native_relational_impulse_saved_v001.py` SHA256:
`ae2dece54beb652d39d7f142766e215fcf0fcf09acdbf7a27aa3d0a48c9cdc49`.
Result `native_relational_impulse_saved_v001_results.json` SHA256:
`042a9231e0f5e4e0d6778c58a3e7931d1fd63d07d2afa39e42c992b9994a3078`.
The only worker exited0 after0.0130487 seconds, peak self RSS22,216,704 bytes.
There was no propagation, eigensolve, intervention or discarded preparation.

## 6. Production is not yet a thermal-origin mechanism

The separate network CMB-origin lane requires a spectrum and state, not just
positive excitation energy. The exact harmonic quench above gives a useful
two-frequency discriminator without a simulation. Define
chi=(1/2)log(A_f/A_i)=(3/2)log(a_f/a_i). Its initial and final ladder operators
obey, for each actual harmonic component,

    b_f=cosh(chi)b_i+sinh(chi)b_i^dagger,
    n_omega=<b_f^dagger b_f>=sinh^2(chi)=n_*,
    m_omega=<b_f b_f>=sinh(chi)cosh(chi).

The occupation is independent of omega for this SAME instantaneous amplitude
ratio. A positive-temperature Planck occupation would instead require

    beta_eff(omega)=log(1+1/n_*)/(hbar omega).

Two unequal positive frequencies cannot share a finite positive beta under
that expression. Zero quench gives vacuum, not a positive-temperature bath.
A common clock rescaling does not fix the mismatch: it rescales all
frequencies together without removing their unequal ratio.

Even one oscillator is not a stationary Gibbs state. Its anomalous moment
m_omega is nonzero and rotates as exp(-2i omega t); a Gibbs oscillator has
m=0. The squeezed-vacuum number variance is2n_*(n_*+1), twice the Gibbs
variance at the same mean. Dephasing removes the anomalous expectation but
preserves the even-only number populations and their variance. It is not
thermalization. These follow directly from the displayed canonical transform
and vacuum moments, not an observational fit.

For a separately constructed two-mode squeezed field, tracing a partner can
give a thermal single-mode marginal. That construction is not supplied by
these independent finite coordinates, and even it would not convert flat
occupation across unequal frequencies into a common Planck temperature.
Do not transfer the single-real-oscillator parity argument to an unowned
Fourier-pair model.

Thus this specific harmonic sudden-production branch is a nonthermal seed,
not a direct CMB-origin solution. This result does not quantify the quartic
parent's evolution, identify its dark response modes with photons, or exclude
other network radiation/thermalization mechanisms. A conversion and thermal-
ization claim still needs an actual coupling, state evolution and energy debit.
The existing native five-line detailed-balance and coherent-transport results
test different mechanisms and remain separate; no completed thermal calculation
was rerun. Root and handoff_plan_review_v005 independently checked this new
quench-specific spectral/covariance test against the canonical transform.

## Decision and independent algebra check

Quantum formation is a legitimate missing mechanism to investigate, not
excluded by the classical zero-mean argument. The shortest next test is to
match its normalization, inertias, spectral residues and actual state to the
existing native response, and check the static contact at the same time.
No arbitrary early a(t), species census, vacuum subtraction or separate dark
abundance is authorized as a prediction. No photons, thermal CMB spectrum,
primordial perturbations, full metric response or superior observational fit
have been obtained. All relevant Stage 3 lanes remain open.

Root derived the finite static/contact theorem, exact work control and scale
reduction. Agent endpoint_equations_check independently verified the l=1
resolvent positivity, the A normalization, canonical physical-energy distinction,
quantum virial stress and sudden/adiabatic control. This is an independent
algebra check, not independent physical replication. Sections1--4 are analytic;
they involved no numerical worker.

For section5, root and
v005_resume_review independently derived the measured-phase/backreaction
identity; root authored and ran the sole saved-scalar worker after reviewing
its complete source. Existing native spectra and canonical matching conventions
were separately reviewed by v005_resume_review. No physical map was adopted.

For external context only, quantum production under a prescribed cosmological
metric is established in [Parker's original work](https://journals.aps.org/pr/abstract/10.1103/PhysRev.183.1057).
State and stress-tensor prescriptions require additional care in a field
theory, as reviewed by [Hollands and Wald](https://arxiv.org/abs/1401.2026).
Neither source derives this UNT finite Hamiltonian or supplies its missing
native population, volume, photon coupling or absolute stress matching.

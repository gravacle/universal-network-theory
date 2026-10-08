# Registered Maxwell stationary emission and native debit V001

Prospective analytical continuation, 2026-10-06 UTC. No native state, source matrix, coefficient, integral, rate, eigenproblem, quadrature or trajectory is evaluated. This note uses the same incidence–Maxwell action and registered-ball postulate. It derives the conditional on-shell normalization and complete leading native energy transfer; it does not promote the completed finite canonical switch experiment or advancing coherent preparations to a stationary radiator. Root alone executes separately reviewed packets.

## 1. One common law and one support

Retain HN,physical=Eunit*HN,native with its full absolute energy, both owned record branches and both incidence operators P=n_e. The same globally declared kappa, R_cell and proper coframe give chi_R=1_(|x-X_e|<=R_cell), Z=I+kappa*chi_R*P>0 and Hgamma=int[D Z^-1 D/(2epsilon0)+Z B^2/(2mu0)]. All native, field, interaction, support/recoil, metric and encoder energy/stress belong to this action. The global units Eunit/R_cell are independent of the macroscopic gradient/clock scales. No gap-specific width, support, energy zero, population, temperature or gravitational constant is selected.

Work first in a fixed admitted photon regulator and an outgoing vacuum continuum in the registered local proper chart. The first interaction is kappa*P int chi_R(B^2/mu0-D^2/epsilon0)/2. Its full two-transverse-polarization/Bose normalization is the pinned outgoing kernel. The canonical second contact kappa^2*P int chi_R^2 D^2/(2epsilon0), the absolute vacuum and the material reactions remain. A finite on-shell rate need not determine these virtual/reference contacts. No normal-ordering subtraction or arbitrary continuum counterterm is introduced here.

The single-edge held-support branch is a disclosed effective fixture. A time-independent held center can have zero source power while receiving momentum; that is not a closed freely recoiling emitter. For a dynamical support, its state, Hamiltonian and exp[-i(k+k').X_e] operator must be in the same matrix element and total gap. The native-only expressions below require the explicit negligible-recoil/held-support branch, or a genuinely supplied support whose energy transfer vanishes to the retained order. Replacing a missing recoil energy by a favorable gap is forbidden.

## 2. Exposure, not an unnormalized window duration

For the already owned family s_T(t)=sin^4(pi*t/T), 0<t<T, define the proper weak-coupling exposure

    exposure_T=int_0^T s_T(t)^2 dt=35*T/128,
    |s_hat_T(nu)|^2/exposure_T -> 2pi*delta(nu).          (1)

The coefficient35/128 is the exact mean of sin^8. The distributional limit follows Parseval and rescaling against a bounded continuous spectral test function near the line. Division by nominal T instead gives (35/128)*2pi*delta(nu). This precision does not change any previous finite-window coefficient. A unit plateau with fixed smooth ramps instead has exposure_T/T->1; its ramps and preparation retain their actual work.

The rate limit is an additional physical approximation: vacuum outgoing boundary data, controlled weak coupling, bath correlation decay, line resolution and an observation interval long compared with the bath/oscillatory times are required. An unchanged stationary population also requires negligible depletion over that interval. A kinetic evolution can include depletion instead; neither case follows merely by waiting in the finite four-mode box. Unresolved nearby lines require the full coherent/nonsecular source kernel. No actual cycle/tree state is dephased or reset by (1).

## 3. Exact normalized ball response

For an exact native positive gap d=(E_initial-E_final)/Eunit, use r=R_cell*Eunit/(hbar*c_p), z=d*r and the normalized ball Fourier transform F(u)=3[sin(u)-u*cos(u)]/u^3, F(0)=1. The already normalized radial/polarization integral gives the universal scalar rate factor

    gamma_d=[2kappa^2/(945pi)]*(Eunit/hbar)*r^6*d^7*J(d*r),
    J(z)=(105/2)int_0^1 dx x^3(1-x)^3 int_-1^1 dc (1-c)^2
            *F(z*sqrt[1-2x(1-x)(1-c)])^2.               (2)

gamma_d has units of inverse proper time and excludes the native source matrix-element strength. The factor105/2 normalizes the product integral2/105. Every native gap uses the SAME support and (2); no line-dependent normalization is inserted. The normalized ball average gives |F|<=1, so J(0)=1 and 0<J(z)<=1 for finite real z; J(z)<1 for z!=0. Strict positivity follows from the nonzero analytic square on an interval of positive measure, not from choosing an advantageous wavelength.

With the normalized x~Beta(4,4) and y=1-c distribution proportional to y^2 on[0,2], s^2=1-2x(1-x)y has means <s^2>=1/3 and <s^4>=5/33. Thus

    F(u)^2=1-u^2/5+3u^4/175+O(u^6),
    J(z)=1-z^2/15+z^4/385+O(z^6).                      (3)

Equation(2) is valid at every finite z on the declared branch; (3) is only a small-z expansion. The old universal r^6*d^7 upper bound is recovered without replacing J by one outside that limit. Actual finite-resolution native spectra still have their original residual/near-degeneracy qualification; clustered mean energies cannot become exact projectors or exact common gaps.

## 4. Full leading secular native debit

For EXACT energy projectors of the same HN,native define the complete energy-lowering operator, retaining all same-gap and actual degenerate coherence,

    A_d=sum_E Pi_(E-d)*P*Pi_E,
    [HN,native,A_d]=-d*A_d,
    D[A]rho=A*rho*A^dagger-{A^dagger*A,rho}/2.          (4)

This decomposition is a consequence of a controlled resolved weak-continuum limit; it is not a new spectrally filtered microscopic coupling. Under that limit the vacuum generator is sum_(d>0) gamma_d*D[A_d], together with the full native Hamiltonian and its retained virtual Hamiltonian. The resolved secular virtual block commutes with HN; when that premise fails, its actual coherent energy commutator must be kept. Vacuum has no upward incoming-photon term and the zero-gap emission factor vanishes. Exact equal-gap amplitudes are combined before squaring. Numerical near-gap grouping alone does not establish (4).

The identity A_d^dagger*HN*A_d=A_d^dagger*A_d*HN-d*A_d^dagger*A_d then fixes the leading transfer for any admitted density in this generator:

    intensity_d=gamma_d*Tr(rho*A_d^dagger*A_d)>=0,
    dEN/dt=-Eunit*sum_(d>0) d*intensity_d,
    dEgamma,out/dt=+Eunit*sum_(d>0) d*intensity_d,
    dNgamma,out/dt=2*sum_(d>0) intensity_d.              (5)

Each jump emits one two-photon event with total energy Eunit*d. The individual energies/angle distribution remain (2), including the actual support momentum reaction. Equation(5) retains coherence within exact degenerate blocks and all source-allowed positive gaps. It is a complete leading native debit, unlike finite-window pair probability alone. If [rho,HN]=0, the no-photon and canonical vacuum/virtual commutators of the preceding Dyson law have no secular native power; they still supply normalization, storage, preparation and absolute source stress. The continuum limit does not erase them from the action.

For a truly stationary ground state there is no downward support, so every intensity is zero. An incidence source commuting with HN likewise has no vacuum on-shell power. For an autonomous finite native bank without renewed supply, (5) implies total emitted leading energy <= EN(0)-Emin,physical, with the full interaction/support boundary terms restored beyond this split. If an exact smallest allowed gap dmin>0 is supplied, the number of emitted events is additionally <=[EN(0)-Emin,physical]/(Eunit*dmin). A finite bank cannot sustain an indefinitely fixed nonzero stationary emission power. No thermal temperature, irreversible native mixing or number-changing plasma state follows.

## 5. Zero secular switch work is a separate limit

The exact inclusive identity remains d<HN+Hgamma+Hsupport+...>/dt=<partial_t Htotal>. With constant registered metric/support/coupling the plateau is autonomous and its actuator power is exactly zero. Switching/preparing the coupling or correlations carries the full canonical source work and cannot be reclassified as native release. For a fixed admitted regulator, controlled weak stationary ramp/transient work and virtual storage are nonsecular boundary terms: their ratio to exposure_T vanishes only if they remain bounded in the stated limit. The native/photon secular terms of (5) then cancel with no extensive switch term. In a depletion-scale kinetic limit, state evolution and the same source work must be retained; a fixed-population long-time approximation cannot simultaneously ignore a finite bank's depletion.

The regulator order matters. The V2 vacuum contact of the sharp ball has a quartic continuum ultraviolet contribution, although every finite on-shell gap integral in (2) is finite. Take any weak/long-time reduction at an owned fixed regulator/reference; do not send the cutoff to infinity and discard an infinite boundary power or coherent native contact afterward. A physical ultraviolet/source-reference law is still required for a complete autonomous continuum action. Choosing one global cutoff above the full native gap span can leave the on-shell rates unchanged while changing virtual/reference energy; that is a physical premise to be owned, not an emission fit.

Future ordinary charged matter has alpha_eff=alpha/Z. Measured electromagnetic normalization and the actual source state must be matched once before inheriting Compton/brems/double-Compton/atomic/weak/nuclear rates or BBN/HYREC histories. Ordinary plasma may thermalize a computed nonthermal injection; native KMS is optional. The emission action preserves the fixed native cell count and cannot by itself provide formation or negative expansion stress.

## 6. Smallest next calculation and its refusal conditions

The completed outgoing packet already owns all downward source catalogs and conditional stationary moments. Recomputing those moments would not add a physical result. A genuinely new bounded packet can instead tabulate the SAME normalized J(z) with fixed independent radial/angular rules and exact (3)/positivity/bound controls, apply it to every qualified full native transition/block under one globally declared support/scale, and report both event intensity and the EXACT matched native/photon debit (5). Zero/absent/upward channels, exact-degenerate coherence, numerical unresolved blocks, all record/incidence branches and every declared preparation must remain. Any stationary block preparation is additional disclosed state data; the actual advancing coherent vectors remain governed by the complete finite-window/Dyson functional.

No physical numerical rate is defined until the common Eunit/R_cell/kappa and stationary/support branch are specified. Symbolic prefactors or a prospectively declared mathematical dimensionless response grid can test the universal law without selecting a favorable physical cell. A rate/depletion worker must separately qualify the continuum, line-resolution, recoil and UV/reference assumptions; it must not turn the already switch-funded box rows into zero-work radiation. No new numerical packet, population, support value or history is chosen in this note. Root decides the next concrete frozen packet after independent review; no model helper is invoked here.

## Frozen direct inputs

| Parent | SHA256 |
|---|---|
| NATIVE_INCIDENCE_MAXWELL_PAIR_SOURCE_V002.md | 7e5cf9d3651de4471b52c9a3769f23cdd5457726c8354ff42ecee3c2a4034c7b |
| NATIVE_REGISTERED_CELL_OUTGOING_MAXWELL_PAIR_KERNEL_V001.md | f4debb30c540386d39179fdcfc244373ac6a2bcab9f04f27fa32c0f404c88c8c |
| NATIVE_REGISTERED_MAXWELL_DYSON_ENERGY_LEDGER_V001.md | 2ab45d4575ee2c8569a5e1a59f38dbbf3b4c60854f3ef63100e82ccd6a987306 |
| NATIVE_CANONICAL_MAXWELL_DYSON_ENERGY_CONTROL_V001_RESULT.json | b6ef391337e96998976eab6d9b99b3e90369b88e2c2f47fcfc23e59bd62f1dd4 |
| NATIVE_CANONICAL_MAXWELL_DYSON_ENERGY_CONTROL_V001_RECEIPT.json | 94c8c845c16b2f6d4978afda790f6a70f31ee33e799d5e581aae3d174913cdce |
| NATIVE_ENERGY_RELEASE_THERMAL_ORIGIN_AND_EXPANSION_BRIDGE_V003.md | 2547e8533877d3f630fd2e283f6d63bebc920d4c1bb768f067a556b649bb5742 |

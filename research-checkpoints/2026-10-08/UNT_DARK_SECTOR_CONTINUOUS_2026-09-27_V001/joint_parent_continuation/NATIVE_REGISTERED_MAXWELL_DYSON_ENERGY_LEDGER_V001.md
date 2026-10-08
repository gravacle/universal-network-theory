# Registered native–Maxwell no-photon and Dyson energy ledger V001

Prospective analytical derivation, 2026-10-06 UTC. This note evaluates no state, spectral sum, source function, quadrature, eigenproblem, propagator or rate. Root exclusively executes reviewed numerical packets. The completed canonical V003 and outgoing-source V001 remain unchanged. Their finite canonical energy release and outgoing coherent source functions do not by themselves identify escaped radiation, thermalization or an early cosmological history.

## 1. The canonical contact is part of the same action

For the registered incidence projector P=n_e, real support chi and one global coupling, set Z(t)=I+kappa*s(t)*chi*P>0. Work at a fixed admitted coframe/support and a declared finite Maxwell regulator. The exact positive field Hamiltonian is D_field Z^-1 D_field/(2 epsilon0)+Z B_field^2/(2 mu0), with its absolute free vacuum reference retained. Since P^2=P, its expansion is

    H(t)=H0+kappa*s(t)*V1+kappa^2*s(t)^2*V2+O(kappa^3),
    H0=HN+Hgamma0,
    V1=int chi*P*(B_field^2/mu0-D_field^2/epsilon0)/2,
    V2=int chi^2*P*D_field^2/(2 epsilon0).                 (1)

HN is the complete absolute native Hamiltonian, not an excitation-only replacement. Operator ordering, metric, support, encoder and source variations belong to this same Hamiltonian. Equation(1) is the expansion of Z with time-dependent kappa*s; scaling a precomputed finite-kappa interaction linearly by s would generally have a different second contact. The finite constant-on interval below has s=1 and is the existing canonical law.

In the owned paired transverse vacuum, <V1>_vac=0. The second contact <V2>_vac is not zero and must be kept. If a different admitted regulator has a nonzero first vacuum contact, its actual first-order commutator must also be included; it cannot be suppressed by this formula's vacuum premise.

## 2. Complete reduced-native second order

Use the H0 interaction picture and normalized native density rho. A normalized outgoing two-photon state lambda has energy hbar*Omega_lambda>0 and first-order matrix element g_lambda*exp(i Omega_lambda t)*P(t), with kappa excluded from g_lambda. The unordered-pair measure includes the Bose counting once. For the global envelope define

    C_Omega=int_0^T s(t)*exp(i Omega t)*P(t)dt,
    D_Omega=int_(t>t') s(t)s(t')exp[-i Omega(t-t')]
                                     *P(t)P(t')dt dt',
    A2=(1/hbar)int_0^T s(t)^2*<0|V2^I(t)|0>dt,
    w_lambda=|g_lambda|^2/hbar^2.                         (2)

The diagonal of the double-time square has zero measure. Splitting that square into its two triangles gives the exact operator identity D_Omega+D_Omega^dagger=C_Omega^dagger*C_Omega. Consequently the complete native change is

    rho_N^I(T)-rho=kappa^2*{sum_lambda w_lambda*
       [C rho C^dagger-D rho-rho D^dagger]-i[A2,rho]}
       +O(kappa^3).                                      (3)

The no-photon amplitude supplies the two D terms. Writing D=C^dagger*C/2+iL with L=L^dagger displays both the anticommutator needed for trace preservation and the coherent commutator -i[L,rho]. Trace(3)=0, including the canonical A2 term. This perturbative expansion is not an exact positive density matrix at an arbitrary finite kappa, nor a dephasing/reset operation.

The leading free-energy changes, after a window ending at zero coupling, are

    EN2=sum_lambda w_lambda*[Tr(rho C^dagger HN C)
                  -2 Re Tr(rho HN D)]-i Tr(rho[HN,A2]),
    Egamma2=sum_lambda w_lambda*hbar*Omega_lambda
                                      *Tr(rho C^dagger C). (4)

Here Delta EN=kappa^2*EN2+O(kappa^3), and likewise for the photon free energy. Native release has sign -Delta EN. Egamma2 is nonnegative, but the complete coherent EN2 is not a pair-probability debit. Dropping the no-photon or A2 terms can violate the energy ledger even when every pair probability is correct.

Only when [rho,HN]=0 does the canonical/antisymmetric commutator vanish and the native expression simplify to the energy-difference-weighted transition probabilities. Coherence within an ACTUAL degenerate energy eigenspace is retained in that simplification. Numerically clustered or merely close eigenvalues do not supply exact degeneracy. Every upward, downward and elastic finite-window contribution remains in (2)–(4); an on-shell downward rate requires its separate stationary/long-time assumptions.

## 3. Work, regulator and ordinary-plasma boundary

For the complete fixed-support regulated Hamiltonian, d< H >/dt=<partial_t H>. Thus prescribed switching work is W=int dot(kappa*s)*<H_(kappa*s)>dt, with actual jump expectations at discontinuities. If the source starts and ends at zero coupling and no other work source acts, Delta EN+Delta Egamma0=W. During coupling the interaction/vacuum-contact storage is also part of <H>; bare photon number while coupled is not escaped radiation. A changing metric/support/encoder or charged material adds its literal source power and recoil, not a freely selected subtraction.

The sin^4 window in outgoing V001 makes its leading pair-number and photon-energy tails convergent under the registered-ball majorant. That result does not remove the separate local V2 vacuum contact: a continuum free Maxwell vacuum has a quartic ultraviolet contact proportional to the actual chi^2 profile. The native commutator of that contact need not vanish on coherent incoming states. An owned field regulator and absolute source/reference prescription are therefore required for complete continuum native debit. The existing finite canonical regulator already defines this contact and gives the bounded next check. No counterterm, favorable energy zero or new volume-energy function is selected here.

Future ordinary charged matter still has e_eff=e/sqrt(Z), alpha_eff=alpha/Z after canonical photon normalization. Physical electromagnetic matching, plasma rates and any BBN/atomic history must be accounted once in the full source family. The finite closed check below changes no inherited cosmological rates and earns no thermal-history claim.

## 4. Exact finite canonical specialization

Set tau=Eunit*t_proper/hbar, HN in native energy units, Omega=hbar*omega_photon/Eunit, and nu=2Omega. The existing homogeneous two-polarization vacuum irrep has K0|j>=(j+1)|j>, K+|0>=sqrt(2)|1>, Kx=(K++K-)/2. Expanding its exact canonical interaction gives V1=Omega*P*(K++K-), V2=Omega*P*(K0-Kx). The vacuum-to-one-pair coefficient is sqrt(2)*Omega, while the retained vacuum contact is Omega*P.

For the same constant-on interval [0,tau], define C,D by (2) with s=1, nu=2Omega in native time and A=int_0^tau P(t)dt. For any unchanged coherent vector psi, the no-photon second-order amplitude is -2Omega^2*Dpsi-iOmega*Apsi. The one-pair amplitude is -i*sqrt(2)*Omega*exp(-i nu tau)*Cpsi after free field transport. Therefore

    EN2=2Omega^2*[<Cpsi|HN|Cpsi>
                  -2 Re <psi|HN Dpsi>]
                           +2Omega Im <psi|HN Apsi>,
    Egamma2=4Omega^3*||Cpsi||^2,
    Won2=Omega*p0,
    Woff2=-Omega*p_tau
          -4Omega^2 Im[exp(-i nu tau)<psi|P(tau)Cpsi>],
    EN2+Egamma2=Won2+Woff2.                               (5)

The p0/p_tau are the unperturbed coherent projector expectations at their actual times. They are not averaged or reset. An independent identity is Omega*(p0-p_tau)=2Omega Im<psi|HN Apsi>. For a stationary native ground state, EN2>=0 and Egamma2>=0: switching/dressing can create photons, but this order does not release ground-state native free energy. If [HN,P]=0, EN2=0; the nonzero finite-window photons are actuator funded. Absolute HN and field vacuum 2Omega remain in the complete initial energy before differences are formed.

Every finite Galerkin cutoff M>=1 contains the full vacuum/one-pair coefficients in (5); higher photon amplitudes affect higher orders. This is a coefficient identity, not a claim that finite-kappa effects are cutoff independent. The completed positive full-Galerkin experiment retains its own cutoff/time controls.

## 5. Bounded next debit control, without new evolution

The saved64 eigenframe gives P(t)_betaalpha=P_betaalpha*exp[i(E_beta-E_alpha)t]. The closed rectangular integral S_t(x)=t*exp(ixt/2)*sinc(xt/2) retains its exact x=0 limit t. Hence C(t)=P*S_t(nu+E_beta-E_alpha), A=P*S_tau(E_beta-E_alpha). Crucially, the ordered amplitude can be evaluated directly on every preparation:

    Dpsi=int_0^tau exp(-i nu t)*P(t)*[C(t)psi]dt.          (6)

Independent fixed128/256 Gauss rules for (6), not an eigensolver or trajectory, can test D+D^dagger at the expectation level, the native/photon/switch balance (5), its separate vacuum contact and temporal resolution. Keep the complete64 native state, exact saved energies, both record branches, incidences0/3, Omega=.5,1,2 and tau=.25,1,2. Retain all22 outgoing cycle/tree holds plus the inherited complete ground; the seven canonical preparations are a declared comparison subset, not a favorable selection. This gives828 coefficient rows before any outcome inspection, with no r/Eunit/kappa fit.

All existing canonical +/- .001/zero rows, three cutoffs and both time resolutions can then be compared to the same coefficients. The even difference [F(+kappa)+F(-kappa)-2F(0)]/(2kappa^2) isolates the quadratic coefficient up to genuine higher even orders and saved numerical error. Save every signed discrepancy and inherited resolution evidence; it is not an exact finite-kappa equality or a post-hoc success tolerance. No old saved state is projected, evolved or renormalized. Root must freeze the numerical protocol/criteria and obtain full independent review before this new source/energy calculation. This note performs none of it.

## Frozen inputs

| Parent | SHA256 |
|---|---|
| native_canonical_maxwell_pair_v003.py | 3bb87715229c29719c2246289d5650359e72f1c34ffbbbc4a8c9536e31713e56 |
| NATIVE_CANONICAL_MAXWELL_PAIR_V003.md | f57e996ffa158b434f82dacb02b8863f9655a2677f9b38a605f91d941d0ce048 |
| NATIVE_CANONICAL_MAXWELL_PAIR_V003_RESULT.json | f74554aa51beb5756fb4da8608a436f29d1efeb2e0958c808d7873ff09d9a1ff |
| NATIVE_CANONICAL_MAXWELL_PAIR_V003_RECEIPT.json | 2fa61745ad09a1aeafee078539f59f4de5258231e5794b0b0ce7c212fd5b2ec2 |
| native_registered_cell_outgoing_source_v001.py | 888ac431d21d828f96a201d5f975dcdc8bf59360ba7dc038b363457ccb821dec |
| NATIVE_REGISTERED_CELL_OUTGOING_SOURCE_V001.md | 1b4709beb5ad6c6f52979def111849290d050fec6d31cdc6c6eaf362b992752f |
| NATIVE_REGISTERED_CELL_OUTGOING_SOURCE_V001_RESULT.json | 9ad2f9890d5e909c048c0353365b75a22b86570c91d45488fb6d19b5e018de1b |
| NATIVE_REGISTERED_CELL_OUTGOING_SOURCE_V001_RECEIPT.json | 0c5bf238307def809f53b05cf37e773385542da8816952af89d7308a74832c7e |
| NATIVE_REGISTERED_CELL_OUTGOING_MAXWELL_PAIR_KERNEL_V001.md | f4debb30c540386d39179fdcfc244373ac6a2bcab9f04f27fa32c0f404c88c8c |
| NATIVE_CANONICAL_MAXWELL_POSITIVITY_AND_VACUUM_GROWTH_V001.md | 3f57f9b9b0844903aa8dac4bd31c76372e5f6ce613e123b1c535270e03fb43f3 |

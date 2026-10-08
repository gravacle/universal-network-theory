# Native canonical Maxwell positivity and vacuum-growth controls V001

2026-10-06 UTC. NEW exact analytical interpretation of the completed homogeneous canonical Maxwell fixture. The root-run calculation naturally closed at 05:53:40.828342 UTC, all 34,256 numerical checks passed, and root authenticated all 216 payload/COMMIT/NPZ trials, 4,536 rows and 3,780 comparisons. The present author verifies only immutable byte/status ancestry; no producer, native Hamiltonian, state contraction, propagator or new numerical effect is executed. No gate is added to that closed result.

## 1. Exact lower bound from the full canonical law

Let P=n_e be the native incidence projector, P0=I-P, z=1+kappa>0, Omega=hbar*omega_physical/Eunit>0. In the full four-mode vacuum-accessible k=1 SU(1,1) irrep, K0=n_pair+1, Kx=(Kplus+Kminus)/2, Ky=(Kplus-Kminus)/(2i). The commutators are [K0,Kplus]=Kplus and [Kplus,Kminus]=-2K0. Both transverse polarizations remain present.

The occupied-source field is exactly

    Hgamma(z)=Omega[(z+z^-1)K0+(z-z^-1)Kx]
             =2Omega U_chi K0 U_chi^dagger,
    U_chi=exp(-i chi Ky), chi=log z.                         (1)

Indeed U_chi K0 U_chi^dagger=cosh(chi)K0+sinh(chi)Kx; this is a unitary boost of the full irrep, not a shift of the zero point. Since K0>=I, Hgamma(z)>=2Omega I. Hgamma(1)=2Omega K0 has the same lower bound. Consequently the exact conditional operator

    Hfield=P0 tensor Hgamma(1)+P tensor Hgamma(z)

obeys Hfield>=2Omega I for an arbitrary entangled native/field state. If p=Tr(rho P), the two unnormalized conditional field blocks have weights 1-p and p. Applying the inequality separately and summing gives <Hfield>>=2Omega for normalized rho; this does not replace the quantum projector by its mean in the Hamiltonian.

For the literal absolute native Hamiltonian with minimum E_min,

    Htotal=Hnative tensor I+Hfield >=(E_min+2Omega)I.        (2)

Neither native record energy nor photon vacuum energy is subtracted. The conditional boost generally does not commute with Hnative because [Hnative,P] need not vanish; it cannot remove the native/field interaction from the complete action. No exact free-energy-commuting spectral-port identity is imported.

The numerical Galerkin field is Pi_M Hgamma Pi_M on n_pair=0..M. Compression of a positive quadratic form preserves (1)'s lower bound: Pi_M Hgamma Pi_M>=2Omega Pi_M. This follows by embedding each retained state in the full Fock space. A truncated Kplus/Kminus need not obey the full Lie algebra, and a truncated boost is not asserted to be unitary or to give an exact finite-matrix equivalence. The source instead compresses the full positive HD/HB matrices. Time/cutoff controls qualify the computed fixture, not the full infinite-cutoff propagator.

## 2. Exact work/debit interpretation

For a normalized native incoming state tensored with the bare photon vacuum, W_on=Omega*kappa^2*<P>/(1+kappa). This is positive work on switching the canonical interaction on. During the autonomous constant-source window the full Htotal is conserved; switching off does W_off=-<P tensor W_kappa>. The owned identity is

    Delta E_native+Delta E_gamma,free=W_on+W_off.           (3)

After switch-off, E_gamma,free=2Omega+Omega*N_gamma. Since E_native,final>=E_min,

    Omega*N_gamma <= E_native,initial-E_min+W_on+W_off.    (4)

For a native-ground incoming state the native-excitation term vanishes. Any positive outgoing bare photon energy then requires net switch work and cannot be native-ground release. While coupled, a bare photon count is a reference-basis observable; interaction storage can compensate it. It is not yet a measurement of emitted radiation. For an excited incoming state native energy can contribute, while switch/storage and preparation energy must remain in the same ledger.

Root's completed scalar summary reports 308 positive native-release rows among the 432 excited finest nonzero-kappa controls, with 72 finest ground controls all giving negative native release. The largest reported native release is about 1.86855e-6 native units; in that same row the free photon increase is about 6.73260e-6 and net switching work about 4.86407e-6. This illustrates the complete debit rather than an autonomous radiation-origin claim. Root reports maximum time/cutoff joint differences about 2.87e-11/3.44e-13. These convergence estimates are not directed mathematical error certificates or an independent saved-state audit by this author. No positive-release threshold, fitted Eunit or thermal interpretation is inferred here.

## 3. Vacuum photon-growth bound with the quantum projector retained

In the invariant irrep, n_pair=N_a1+N_a2=N_b1+N_b2 and N_gamma=2 n_pair. The only term of the fixed fixture that changes this count is beta P(Kplus+Kminus), with

    beta=Omega*kappa*(2+kappa)/[2(1+kappa)].               (5)

The native Hamiltonian, diagonal field term and their source projector commute with n_pair. For any normalized density matrix write nbar=<n_pair>, nP=<P n_pair> and p=<P>. Hilbert-space Cauchy, summed over the two polarizations using A_i=a_i^dagger P and B_i=b_i P, gives

    |<P Kminus>| <=sqrt[nP(nP+2p)]
                  <=sqrt[nbar(nbar+2)].                   (6)

The first inequality uses sum<A_i^dagger A_i>=nP+2p and sum<B_i^dagger B_i>=nP. It holds for entangled states and does not factor <P Kminus>. If p=0 the instantaneous creation current vanishes; if p>0 the unnormalized conditional bound is p*sqrt[(nP/p)(nP/p+2)]. Native dynamics can change p and nP, so no autonomous conditional-count equation is presumed.

The exact total-count Heisenberg equation and (6) imply

    |d nbar/d tau|<=2|beta|sqrt[nbar(nbar+2)],
    nbar(0)=0 => nbar(tau)<=2sinh^2(|beta|tau),
    <N_gamma>(tau)<=4sinh^2(|beta|tau).                    (7)

This comparison follows by nbar=2sinh^2 u and the regular vacuum limit u(0)=0. It retains arbitrary native coherences, all diagonal native energies and source occupation history. It is an upper bound, not a prediction that the bound is saturated or a certificate that photons thermalize. In physical seconds replace |beta|tau by |beta|Eunit*t_proper/hbar. A prescribed time-dependent off-diagonal coefficient can be bounded by its integral only if the count/encoder chart remains fixed and every additional source commutator is retained.

For a finite Galerkin calculation [n_pair,H_M]=Pi_M[n_pair,H]Pi_M because n_pair commutes with Pi_M. The corresponding expectations equal full-Fock expectations of the embedded retained state, so the same Cauchy bound applies without treating truncated individual annihilation operators as a canonical algebra. The cutoff boundary and convergence are still separately checked. This analytical inequality is not retroactively installed as a new success gate.

## 4. Next physical distinction

The closed homogeneous fixture earns a positive canonical coupling with complete energy and source contacts. To assess actual emission, the next source must register the proper cell/support and outgoing modes in the same Maxwell action, retain native and support recoil/debit, and distinguish a finite-window correlator from stationary rate assumptions. A single global Eunit, Rcell and kappa may be disclosed; per-gap frequencies, support or temperatures must not be selected to obtain a spectrum. Ordinary photon normalization, measured alpha matching, plasma rate history and BBN remain additional physical checks. No network Gibbs reset, radiation abundance, irreversible thermalization or inflation follows from (1)-(7).

Direct immutable inputs relative to J:

| Input | SHA256 |
|---|---|
| NATIVE_INCIDENCE_MAXWELL_PAIR_SOURCE_V002.md | 7e5cf9d3651de4471b52c9a3769f23cdd5457726c8354ff42ecee3c2a4034c7b |
| native_canonical_maxwell_pair_v003.py | 3bb87715229c29719c2246289d5650359e72f1c34ffbbbc4a8c9536e31713e56 |
| NATIVE_CANONICAL_MAXWELL_PAIR_V003.md | f57e996ffa158b434f82dacb02b8863f9655a2677f9b38a605f91d941d0ce048 |
| NATIVE_CANONICAL_MAXWELL_PAIR_V003_RESULT.json | f74554aa51beb5756fb4da8608a436f29d1efeb2e0958c808d7873ff09d9a1ff |
| NATIVE_CANONICAL_MAXWELL_PAIR_V003_RECEIPT.json | 2fa61745ad09a1aeafee078539f59f4de5258231e5794b0b0ce7c212fd5b2ec2 |

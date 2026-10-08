# Physical-mode marginal and local thermal onset V001

2026-10-06 UTC. NEW STATIC positive counterpoint to whole-field parity. No operator, state/vector, marginal, distribution, Gibbs parameter, coefficient or source/helper is evaluated. Keep the SAME autonomous pure parent, fixed finite M>=1, original bare vacuum, physical four-mode embedding and all existing numerical dispositions.

## Exact physical modes, rather than treating pair index j as an oscillator

Write Kplus=a1_dagger a2_dagger+a3_dagger a4_dagger, for the two transverse polarizations of the opposite momenta. Expanding its jth power on vacuum gives j! times the equal sum of |m,m,j-m,j-m>, m=0..j. The normalized k=1 irrep basis is therefore exactly

    |j>=(j+1)^(-1/2) sum_(m=0)^j |m,m,j-m,j-m>.                (1)

Let rhoGamma,jjprime be the original field density after tracing native records/link/carrier; it may retain complex off-diagonal j coherence. Trace THREE physical modes in |j><jprime|. Their occupation deltas require m=mprime and j-m=jprime-mprime, hence j=jprime. Consequently every one of the four physical-mode marginals is the SAME exactly diagonal density

    rho_mode=sum_(m=0)^M Pm |m><m|,
    Pm=sum_(j=m)^M rhoGamma,jj/(j+1),
    sum_m Pm=1, mean_m=sum_j (j/2)rhoGamma,jj=nu_total/4.        (2)

This statement holds for any normalized field density supported in the admitted irrep, irrespective of native entanglement and collective j coherences. The bare single-mode Hamiltonian Eunit*Omega*(m+1/2) commutes with (2) exactly. Bare stationarity is not vanishing interaction-source dynamics: the probabilities can still change in time. The whole-field density need not commute with its own bare B=Omega(Ntotal+2).

## Leading local Gibbs shape from the owned quantum onset

At fixed finite dimension the accepted onset has p=c tau^4, c=h^2 Omega^2 b_kappa^2/2>0, rhoGamma,11=p+O(tau^6), rhoGamma,00=1-p+O(tau^6), and total j>=2 population O(tau^6). Here tau=Eunit*t_proper/hbar and b_kappa=kappa(2+kappa)/[2(1+kappa)]; the owned source fixes h=Omega=1. Equation (2) then gives

    P0=1-p/2+O(tau^6), P1=p/2+O(tau^6),
    sum_(m>=2) Pm=O(tau^6), mean_m=p/2+O(tau^6).              (3)

The geometric bare Gibbs REFERENCE with this same marginal mean nbar=nu_total/4 is Gm=nbar^m/(1+nbar)^(m+1). Thus G0=1-p/2+O(tau^6), G1=p/2+O(tau^6), and its m>=2 tail is O(tau^8). Since both densities are diagonal, their half trace-norm distance is half the summed population difference, so

    Dtr(rho_mode,rho_geometric)=O(tau^6).                      (4)

This is a constructive local thermal-SHAPE agreement through the leading ordertau4 production, derived without a chosen temperature or finite-time fit. It differs from the actual-state mean-field reference, which remains pure and produces pair NUMBER only at ordertau6. At kappa=0 or h=0 the original field is exact vacuum; the local matched reference is the zero-temperature limit, with no positive-p logarithm or positive-temperature assignment.

For clarity, an exact unrestricted geometric marginal Pm=(1-r)r^m in the infinite irrep would require diagonal weights rhoGamma,jj=(j+1)(1-r)^2 r^j, because Pj-Pjplus1=rhoGamma,jj/(j+1). This is an exact population criterion, not a state or spectrum adopted here. A finite-M marginal cannot equal an unrestricted positive-temperature geometric distribution exactly because its occupation tail terminates; (4) is the fixed-cutoff onset statement.

Tracing partners can therefore give local Gibbs shape while the WHOLE four-mode field stays even and has the already derived distance from an unrestricted whole-field Gibbs reference. Equations (2)-(4) do not establish a common Planck temperature across unequal frequencies, detailed balance/KMS of source correlations, persistent equilibration, irreversible entropy production, outgoing radiation, ordinary-plasma reduction, baryons or macroscopic P(X). The physical energy/support/coframe registration and inclusive interaction/source ledger remain mandatory; a matched bare occupation does not replace them.

## Actual protected inputs, verified before and after exclusive creation

| Input relative to J | SHA256 |
|---|---|
| native_record_copy_canonical_maxwell_v001.py | 607c84a7ac98776d3e3e34bf508808b2e8e3500088354b02205fdb6995e4e23a |
| NATIVE_RECORD_COPY_CANONICAL_MAXWELL_V001.md | 28167e16995285aaa24e7d8a1ef734cdd086a0d7aeefccb7fef33c07374ca048 |
| NATIVE_UNIFIED_PARENT_PHOTON_ONSET_AND_MEANFIELD_DISCRIMINATOR_V001.md | 8185f9d938c328731d5ff8caaf0597ea7a8844d5fbf37450e8c2a75b854d7f6a |
| NATIVE_UNIFIED_PARENT_PHOTON_ONSET_VON_NEUMANN_ENTROPY_COROLLARY_V001.md | eb12a0e6facf53f52d3a3ee01b9036548d53410fe6aea3d95f1fac83c0b01343 |
| NATIVE_UNIFIED_PARENT_WHOLE_FIELD_PARITY_AND_PLANCK_REFERENCE_V001.md | cf02adef59382b3596b673723ba1609d38a2b6a95ac8857d393cf395ab78ee24 |

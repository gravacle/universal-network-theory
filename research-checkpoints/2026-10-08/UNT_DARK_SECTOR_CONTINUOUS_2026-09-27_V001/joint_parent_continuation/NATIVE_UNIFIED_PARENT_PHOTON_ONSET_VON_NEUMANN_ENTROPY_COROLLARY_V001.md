# Photon-onset von Neumann entropy corollary V001

2026-10-06 UTC. Root-requested STATIC corollary of the accepted autonomous one-parent onset proof. No operator, state, amplitude, expectation, coefficient, entropy, helper or trajectory is evaluated. No existing finite-time sample is fitted to this asymptotic result.

## Fixed finite parent and leading Schmidt weight

Use the original pure preparation eta0 tensor |0>, tau=Eunit*t_proper/hbar, real source Hamiltonian H=HN+B+n tensor W, B=2Omega K0, and an admitted FIXED finite field cutoff M>=1. The owned symbolic coupling is b_kappa=kappa(2+kappa)/[2(1+kappa)], with W10=sqrt(2)Omega b_kappa. The source fixes h=Omega=1; their displayed powers do not select new parameter arms.

For h*b_kappa!=0, the accepted leading pair column is (h W10/2)tau² eta1+O(tau³), orthogonal to the zeroth-order vacuum column eta0. The vacuum column includes +i h tau eta1, and the mandatory pair return path includes +i h² W10 tau³ eta0/6. Thus the reduced-field coherence is +i h² W10 tau³/3+O(tau⁴); its square first contributes at ordertau6, not ordertau4.

Let c=h² W10²/4=h²Omega²b_kappa²/2>0. The dominant small Schmidt eigenvalue of rho_gamma is

    lambda1=c tau⁴+O(tau⁶),
    sum_(j>=2) lambda_j=O(tau⁶),
    lambda0=1-lambda1-sum_(j>=2)lambda_j.                                    (1)

The leading orthogonal pair column fixes the single ordertau4 eigenvalue; all remaining field-column weights are at least ordertau6. Real H and the real initial preparation imply rho_gamma(-tau)=conjugate(rho_gamma(tau)), hence identical spectra. The unique leading small eigenvalue is therefore even and has no ordertau5 term. These estimates are at fixed finite dimension, not uniform in an infinite-cutoff or thermodynamic limit.

## Entanglement entropy, without a temperature assignment

With natural logarithms and p=c tau⁴,

    S_gamma/kB=-Tr(rho_gamma ln rho_gamma)
              =p(1-ln p)+O(tau⁶|ln tau|),
    1-Tr(rho_gamma²)=2p+O(tau⁶).                                            (2)

The dominant eigenvalue correction changes -lambda1 ln lambda1 by O(tau6|ln tau|); the total O(tau6) remaining weight contributes at most that order in fixed dimension. Expanding -lambda0 ln lambda0 supplies the +p term. The linear entropy coefficient is the already accepted onset result, not a new numerical observable or independent calculation.

At kappa=0 the field decouples and remains bare vacuum, so S_gamma=0 exactly. At h=0 the original n0 support persists and n tensor W cannot act, also giving S_gamma=0 exactly. Do not substitute c=0 into the positive-p logarithmic expansion. Active record copying and feedback affect higher-order coefficients, not (1) or (2). Physical-time powers follow only through the stated tau conversion.

The total closed parent remains globally pure under unitary evolution, with zero global von Neumann entropy. Its two reduced-subsystem entropies are equal and arise from entanglement. Their early increase is not irreversible thermal entropy production: later reversals are allowed. This is a microscopic quantum-origin mechanism, not a Planck spectrum, temperature, equilibration, escaped radiation, primordial Maxwell field, separate fluid or macroscopic P(X) preparation. A cosmological interpretation still requires the owned current/stress/volume registration and controlled memory/ordinary-plasma reduction. All saved states, numerical dispositions, physical flags and live workers are unchanged.

## Protected provenance, checked before and after exclusive creation

| Input relative to J | SHA256 |
|---|---|
| NATIVE_UNIFIED_PARENT_PHOTON_ONSET_AND_MEANFIELD_DISCRIMINATOR_V001.md | 8185f9d938c328731d5ff8caaf0597ea7a8844d5fbf37450e8c2a75b854d7f6a |
| NATIVE_UNIFIED_PARENT_CORRELATION_SOURCE_AND_PRODUCT_INTERVAL_V001.md | f62a63f3230ba90cbf645090f007c39c5b4ae3ae00c1d7459726efe388ccff9f |
| native_record_copy_canonical_maxwell_v001.py | 607c84a7ac98776d3e3e34bf508808b2e8e3500088354b02205fdb6995e4e23a |
| NATIVE_RECORD_COPY_CANONICAL_MAXWELL_V001.md | 28167e16995285aaa24e7d8a1ef734cdd086a0d7aeefccb7fef33c07374ca048 |

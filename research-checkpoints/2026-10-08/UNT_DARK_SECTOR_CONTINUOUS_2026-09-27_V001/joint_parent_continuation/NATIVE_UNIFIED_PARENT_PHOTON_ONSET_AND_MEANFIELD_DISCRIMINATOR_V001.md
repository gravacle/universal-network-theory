# Photon onset and the actual mean-field discriminator V001

2026-10-06 UTC. NEW static small-time result for the SAME autonomous native-copy/canonical-Maxwell action and original blank preparation. Root requested this note after an independent symbolic derivation. No operator, vector, state series, coefficient, expectation, numerical helper or evolution is evaluated. No finite-time sample is asserted to lie in the asymptotic regime.

## One parent and native time

Use tau=Eunit*t_proper/hbar and dimensionless H=HN+B+n tensor W. The source fixes h=Omega=1; symbolic h and Omega below display their exact powers, not new parameter arms. Its native incidence flip is -h Xlink; B=2Omega K0, N_gamma=2j and

    W=Omega[a_kappa K0+b_kappa(Kplus+Kminus)],
    a_kappa=kappa^2/(1+kappa),
    b_kappa=kappa(2+kappa)/[2(1+kappa)],
    W10=<1|W|0>=sqrt(2) Omega b_kappa.

Start eta0 tensor |0>, where eta0=|BB,n0,carrierL> and eta1 has only the incidence bit changed to1. Retain the SAME record copying, feedback, carrier hopping, absolute native identity and field vacuum. For every admitted finite cutoff M>=1 the leading vacuum/one-pair paths exist unchanged.

## The leading amplitudes and the necessary return path

The full state expansion exp(-i H tau) gives

    Psi_(eta1,0)=+i h tau+O(tau^2),
    Psi_(eta1,1)=+h W10 tau^2/2+O(tau^3),
    Psi_(eta0,1)=+i h^2 W10 tau^3/6+O(tau^4).

The second line is the ordered Hint HN path: HN first creates n1 and only then can n W create a pair. The third line is HN Hint HN, with TWO incidence flips and one pair vertex. It returns to n0 and cannot be omitted when tracing the native state. Other native terms and the bare-field phase enter higher orders for these leading amplitudes.

Thus nmean=h^2 tau^2+O(tau^4), pair population=h^2 W10^2 tau^4/4+O(tau^6), and

    N_gamma,actual=h^2 Omega^2 b_kappa^2 tau^4+O(tau^6),
    rhoGamma,01=+i h^2 W10 tau^3/3+O(tau^4),
    1-Tr(rhoGamma^2)=h^2 Omega^2 b_kappa^2 tau^4+O(tau^6).

Here rhoGamma,01=sum_eta Psi_(eta,0) conjugate(Psi_(eta,1)). The eta1 overlap contributes +i h^2 W10 tau^3/2, while the CONJUGATE eta0 return path contributes -i h^2 W10 tau^3/6. Their sum is the displayed THIRD, not a half. Purity loss begins with twice the one-pair population; the coherence squared and other pair populations first affect ordertau6. The real source matrices and real original preparation make the population and purity even in tau.

## Compare with the actual mean-field reference, not a selected state

Define a reference field evolved unitarily from the SAME bare vacuum with B+nmean_actual(tau) W, using the ACTUAL full state's scalar mean. This is the reference in the exact correlation-source identity; it is not a self-consistent new closure or a fitted source. Its leading pair amplitude is -i integral_0^tau h^2 s^2 W10 ds=-i h^2 W10 tau^3/3, so

    N_gamma,reference=(4/9) h^4 Omega^2 b_kappa^2 tau^6+O(tau^8),
    rhoGamma,reference,01=+i h^2 W10 tau^3/3+O(tau^4).

The leading coherence agrees, but the reference lacks the actual ordertau4 photon population and purity loss. The exact correlation term therefore supplies the leading population even though the coherent mean-field marginal rate can be larger in an unweighted matrix norm. A small correlation remainder in that norm cannot alone certify a relative photon-number error.

Record copying g and feedback lambda_R change none of these leading coefficients for the original preparation; their effects remain in higher-order dynamics. The three inherited native/control arms are retained, not newly chosen. At kappa0 the displayed production coefficients vanish; this note chooses no physical coupling, frequency, energy unit, temperature or volume. Proper-time powers follow only by replacing tau with Eunit*t_proper/hbar.

This distinguishes two microscopic descriptions of the SAME action. It establishes neither thermalization nor escaped radiation, an independent fluid, P(X), irreversibility or a cosmological transition. It does not prohibit an approximate hydrodynamic reduction with controlled correlation, memory, current and stress errors. Existing finite-time vectors, numerical dispositions, physical flags and live workers remain unchanged.

| Input relative to J | SHA256 |
|---|---|
| native_record_copy_canonical_maxwell_v001.py | 607c84a7ac98776d3e3e34bf508808b2e8e3500088354b02205fdb6995e4e23a |
| NATIVE_RECORD_COPY_CANONICAL_MAXWELL_V001.md | 28167e16995285aaa24e7d8a1ef734cdd086a0d7aeefccb7fef33c07374ca048 |
| NATIVE_UNIFIED_PARENT_CORRELATION_SOURCE_AND_PRODUCT_INTERVAL_V001.md | f62a63f3230ba90cbf645090f007c39c5b4ae3ae00c1d7459726efe388ccff9f |

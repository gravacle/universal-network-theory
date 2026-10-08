# Whole-field parity and unrestricted four-mode Planck reference V001

2026-10-06 UTC. NEW STATIC discriminator for the owned autonomous pure parent, not a new state calculation. No source/helper, operator, vector, entropy, Gibbs parameter or numerical expression is evaluated. Existing results, physical flags and live workers remain unchanged.

## Original physical Fock embedding

The owned field comprises the two transverse polarizations of the opposite-momentum modes: four independent bosonic modes of the same bare frequency Omega in the benchmark energy unit. Let Ntot=sum_modes a_dagger a, Kplus=sum_polarizations a_plus_dagger a_minus_dagger, Kminus=Kplus_dagger, K0=(Ntot+2)/2 and Kx=(Kplus+Kminus)/2. Then B=2Omega K0=Omega(Ntot+2), including the absolute vacuum energy 2Omega. Define total photon parity Pi=(-1)^Ntot.

Each Kplus/Kminus vertex changes Ntot by two; K0 preserves it. Therefore [Pi,K0]=[Pi,Kplus]=[Pi,Kminus]=0. The actual H=HN+B+n tensor W, W=Omega[a_kappa K0+2b_kappa Kx], commutes with I_native tensor Pi. Native copying, carrier motion and feedback do not change this field selection rule. Here b_kappa=kappa(2+kappa)/[2(1+kappa)] and a_kappa=kappa^2/(1+kappa), with admitted kappa>-1.

From the original bare vacuum, the vacuum-accessible SU(1,1) k=1 basis has Ntot|j>=2j|j>, K0|j>=(j+1)|j> and Kplus|j>=sqrt[(j+1)(j+2)]|j+1>. The exact finite Galerkin compression j=0..M and its full Fock embedding preserve the even sector. Tracing the native subsystem thus gives

    Tr(rho_gamma Qodd)=0, Qodd=(I-Pi)/2.                      (1)

Pi is the identity INSIDE this projected j space. Equation (1) follows from its physical Fock embedding and conserved original parity, not a numerical test of that identity. The j index counts pairs and is not a single physical photon oscillator.

## Explicit unrestricted Gibbs comparator

For a hypothetical unrestricted four-independent-mode bare Gibbs state at one positive temperature, let r=exp[-beta Eunit Omega] in (0,1). Its normalized full Fock density is rho_beta=(1-r)^4 r^Ntot; the absolute vacuum constant cancels in the normalized density. The product geometric series gives

    Tr(rho_beta Pi)=((1-r)/(1+r))^4,
    Podd(beta)=[1-((1-r)/(1+r))^4]/2.                         (2)

For trace distance Dtr(rho,sigma)=||rho-sigma||_1/2, the Qodd measurement and (1) imply Dtr(rho_gamma,rho_beta)>=Podd(beta). This compares the WHOLE original collective field, embedded in full Fock space, with the stated unrestricted reference.

If that reference is required to match only the actual TOTAL bare photon mean nu=Tr(rho_gamma Ntot)>0, then nu=4r/(1-r), so exactly

    Dtr(rho_gamma,rho_beta)>= [1-(1+nu/2)^(-4)]/2>0.          (3)

No temperature is assigned to the actual state. Matching nu is not matching its full native/field/interaction energy, spectrum, correlations or source stress. At fixed admitted finite M>=1 and h*b_kappa!=0, the accepted onset has p=c tau^4, c=h^2 Omega^2 b_kappa^2/2, and nu=2p+O(tau^6). Thus the right side of (3) is 2p+O(tau^6). This is asymptotic algebra, without fitting finite-time samples or evaluating a coefficient. At kappa=0 or h=0 the original field stays vacuum; the matched-mean reference is its zero-temperature limit, not a positive-temperature assignment.

An even-parity-restricted thermal ensemble or a Gibbs density on the projected j space can exist; (3) does not exclude it. Nor does whole-field parity forbid odd occupation or a thermal marginal of one physical mode after tracing partners. No one-oscillator parity argument is transferred to those marginals. The finite homogeneous parent result does not exclude local thermality in a multimode/thermodynamic limit, outgoing pair redistribution, or ordinary-plasma thermalization. It distinguishes its generated whole-field state from this unrestricted four-mode Planck/Gibbs reference, not the entire thermal-origin program or a macroscopic P(X) preparation.

## Actual protected inputs, verified before and after exclusive creation

| Input relative to J | SHA256 |
|---|---|
| native_record_copy_canonical_maxwell_v001.py | 607c84a7ac98776d3e3e34bf508808b2e8e3500088354b02205fdb6995e4e23a |
| NATIVE_RECORD_COPY_CANONICAL_MAXWELL_V001.md | 28167e16995285aaa24e7d8a1ef734cdd086a0d7aeefccb7fef33c07374ca048 |
| NATIVE_UNIFIED_PARENT_PHOTON_ONSET_AND_MEANFIELD_DISCRIMINATOR_V001.md | 8185f9d938c328731d5ff8caaf0597ea7a8844d5fbf37450e8c2a75b854d7f6a |
| NATIVE_UNIFIED_PARENT_PHOTON_ONSET_VON_NEUMANN_ENTROPY_COROLLARY_V001.md | eb12a0e6facf53f52d3a3ee01b9036548d53410fe6aea3d95f1fac83c0b01343 |

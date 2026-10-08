# Physical-mode pair bunching at the quantum onset V001

2026-10-06 UTC. NEW STATIC addendum to the positive leading local-mode thermal-shape result. No source/helper, operator, vector, probability, moment, coefficient, trajectory or Gibbs parameter is evaluated. Original artifacts, physical flags and live workers are unchanged; no sampled finite time is fitted to this asymptote.

## The earliest second-pair path

Keep the SAME pure blank eta0 with incidence n0 and the bare four-mode vacuum, H=HN+B+HI, HI=n tensor W, and the fixed source h=Omega=1. Symbolic h and Omega show units and powers only. Let tau=Eunit*t_proper/hbar, admitted kappa>-1, b=b_kappa=kappa(2+kappa)/[2(1+kappa)], and a FIXED field cutoff M>=2. For the k=1 irrep,

    W10=sqrt(2)Omega*b, W21=sqrt(6)Omega*b.

Reaching j2 requires TWO pair-raising vertices. At third order it also requires the native -h Xlink incidence flip. Every ordering with HI acting before that flip annihilates n0; B and native record/carrier terms cannot raise field pair number. Thus the only nonzero three-vertex path is HI HI HN, which ends in incidence n1. Its signed amplitude from the exponential is

    Psi_(eta1,j2)=(-i)^3*(-h)*W21*W10*tau^3/6+O(tau^4)
                 =-i*h*W21*W10*tau^3/6+O(tau^4).

Consequently the TOTAL j2 population is

    p2=h^2*Omega^4*b^4*tau^6/3+O(tau^8).                      (1)

The real source Hamiltonian and real initial ket give even field populations, excluding an ordertau7 term. Populations j>=3 have total O(tau^8) at fixed finite dimension, since a third pair requires at least four vertices. Active copying and feedback do not supply another third-order j2 path.

## Exact factorial moment and the non-Gibbs rare tail

The exact physical-mode dictionary in the pinned local note gives uniform m=0..j conditional weights. Hence, without choosing a state or a temperature,

    mean_m=nu_total/4,
    mean_[m(m-1)]=sum_j j(j-1)*rhoGamma,jj/3.                 (2)

Use the accepted first-pair population p1=h^2*Omega^2*b^2*tau^4/2+O(tau^6). Equations (1)-(2) imply

    mu=mean_m=h^2*Omega^2*b^2*tau^4/4+O(tau^6),
    F2=mean_[m(m-1)]=2*h^2*Omega^4*b^4*tau^6/9+O(tau^8),
    g2=F2/mu^2=32/(9*h^2*tau^2)+O(1).                       (3)

For the geometric Gibbs reference with that same positive mean, F2_Gibbs=2mu^2 and g2_Gibbs=2. The actual early second-pair tail is therefore parametrically larger than its Gibbs tail. The local zero/one populations still agree with the geometric law through ordertau4, and their previously proved trace-distance estimate O(tau6) remains correct. This sharper observable explains why weak absolute marginal distance does not establish thermal higher moments.

Equations (1)-(3) require h*b!=0 and M>=2. M1 cannot represent the second-pair path. At h=0 or kappa=0 the original field stays vacuum: mu=0 and g2 is UNDEFINED, not a thermal zero. These are fixed-cutoff asymptotic statements, not numerical tolerances, a finite-time fit or uniform continuum/cutoff bounds. The production mechanism can feed a later outgoing/ordinary-plasma redistribution and equilibration route; this finite birth state supplies neither that history nor its temperature, Planck spectrum or macroscopic P(X) registration.

## Actual protected inputs, verified before and after exclusive creation

| Input relative to J | SHA256 |
|---|---|
| native_record_copy_canonical_maxwell_v001.py | 607c84a7ac98776d3e3e34bf508808b2e8e3500088354b02205fdb6995e4e23a |
| NATIVE_RECORD_COPY_CANONICAL_MAXWELL_V001.md | 28167e16995285aaa24e7d8a1ef734cdd086a0d7aeefccb7fef33c07374ca048 |
| NATIVE_UNIFIED_PARENT_PHOTON_ONSET_AND_MEANFIELD_DISCRIMINATOR_V001.md | 8185f9d938c328731d5ff8caaf0597ea7a8844d5fbf37450e8c2a75b854d7f6a |
| NATIVE_UNIFIED_PARENT_PHOTON_ONSET_VON_NEUMANN_ENTROPY_COROLLARY_V001.md | eb12a0e6facf53f52d3a3ee01b9036548d53410fe6aea3d95f1fac83c0b01343 |
| NATIVE_UNIFIED_PARENT_WHOLE_FIELD_PARITY_AND_PLANCK_REFERENCE_V001.md | cf02adef59382b3596b673723ba1609d38a2b6a95ac8857d393cf395ab78ee24 |
| NATIVE_UNIFIED_PARENT_PHYSICAL_MODE_MARGINAL_AND_THERMAL_ONSET_V001.md | f97636a2851631cecbe215072f61082cd890334f9b48152e9ad174c7991854f7 |

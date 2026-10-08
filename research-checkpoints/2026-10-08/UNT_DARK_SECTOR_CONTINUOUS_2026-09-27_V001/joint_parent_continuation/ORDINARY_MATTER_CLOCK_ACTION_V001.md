# Ordinary matter changes the filtered-clock stability test

2026-10-05 UTC. Analytical continuation of COMMON_FILTER_FLRW_MEASURE_V001.
Root and two internal analytical reviewers checked the constraints and
high-frequency signs. No new numerical run, fitted parameter, observational
likelihood, or claim of complete stability. Earlier vacuum results remain.

## Declared system and exact quadratic action

Use Einstein ADM gravity, acceleration coefficient alpha=2 f^2, constant
physical ell and beta>0. Compare lapse-weighted common trace filtering
b_k=beta f^2 with the previously declared unfiltered trace b_k=beta.
The latter is not a new fitted repair. Units c=1; M^2=1/(8 pi G).

One ordinary minimally coupled irrotational species has P(Y)=C Y^nP,
Y=-(partial chi)^2/2, w=cs^2=1/(2 nP-1)>0. Radiation is nP=2.
Every fixed positive near-dust w is covered; exact dust and interchanged
w->0, k->infinity limits are NOT covered by this parametrization.

    p=k/a, f=(1+ell^2 p^2)^(-1), F=1+3 beta/2,
    r=(rho+P)/(2 M^2)=-F H_dot,
    3 M^2 F H^2=rho+M^2 Lambda,
    v=delta chi/chi_background_dot, V=v_dot-3 H w v,
    n=lapse perturbation, s=Delta B/a^2,
    E=zeta_dot-H n, kappa=delta K=3E-s.

After using the background equations, the complete scalar quadratic action is

    L2/(M^2 a^3) = -3E^2+2Es-b_k(3E-s)^2/2
      +p^2 zeta^2+2p^2 n zeta+f^2 p^2 n^2
      +(r/w)(V-n)^2-r p^2 v^2+2rv(s-3zeta_dot).

The background cancellations use unfiltered F, not F_(beta f^2). Weighted
averaging eliminates the separate trace lapse cross term but does not
change the homogeneous Friedmann coefficient. With t=2/b_k, A=3+t,
R=r/w, g=f^2 p^2, D=H^2 A+R+g, the constraints give

    kappa=-2(E+rv)/b_k,
    n=[H A(zeta_dot+rv)+R V-p^2 zeta]/D.

The closed reduced action is

    Lred/(M^2 a^3) = A zeta_dot^2+2trv zeta_dot+tr^2 v^2
      +R V^2-rp^2v^2+p^2zeta^2
      -[HA zeta_dot+RV+HArv-p^2zeta]^2/D.

Its velocity matrix is diag(A,R)-(HA,R)^T(HA,R)/D, with
det K=A R g/D>0 and positive diagonal entries for finite p>0, r>0,
w>0, beta>0. Thus these conditions give no quadratic scalar ghost.
All time derivatives of H, r, f and the a^3 measure remain in evolution.

## Common filtered trace: matter-induced gradient instability

For b_k=beta f^2 use the time-dependent chart zeta=H q, v=q+xi
BEFORE freezing a short-time oscillation frequency. The leading large-p
lapse is q_dot+[(H_dot+r)q+r xi]/H. Integrating the spatial cross
2H p^2 q q_dot with its actual a^3 p^2 measure leaves

    Lleading/(M^2 a^3) = f^2 p^2 q_dot^2
      +(H_dot+r)p^2 q^2+(r/w)xi_dot^2-rp^2xi^2.

Here H_dot+r=r(1-1/F)>0. Consequently

    omega_clock^2 = -r(1-1/F)/f^2+O(p^2)
                 ~ -r(1-1/F)ell^4 p^4,
    omega_fluid^2 ~ w p^2.

In radiation domination the first expression is -3 beta H^2 ell^4 p^4.
This is an unbounded gradient instability, not a ghost or ordinary Jeans
growth. Its growth becomes faster than H at sufficiently large p, making
the asymptotic short-time treatment self-consistent. Vacuum de Sitter's
r=0 limit is nonuniform: its saved stable result was correct in that domain
but does not qualify a universe containing ordinary radiation/matter.

This diagnoses the formal continuum action. No cutoff has been chosen;
whether the unstable range lies inside a specified effective domain is a
separate question. Do not fit a cutoff to remove the observed failure.

## Constant unfiltered trace: different outcome

For b_k=beta, A=3+2/beta is constant. Retain the constraint-induced
O(p^2) zeta v_dot mixing; omitting it produces a spurious background-dependent
fast coefficient. The complete leading eigenfrequencies are

    omega_fast^2 ~ [beta/(2+3beta)] ell^4 p^6 > 0,
    omega_fluid^2 ~ w p^2.

This branch survives this leading UV sign test. Its phase speed grows as
p^2 and group speed approaches three times phase speed. The previous
matter-photon-cone restriction was OPTIONAL, not a general exclusion of
preferred-foliation physics. Neither superluminality alone nor the present
positive signs prove an operational causal theory. Finite-p stability,
interactions, strong coupling, source formation and full light propagation
remain open. Neither trace prescription creates the missing homogeneous
matter contribution or selects its abundance.

Next scientific priority is the shared macro closure, not another default
UV repair sweep. Background mapping, conserved work and source-selected
state must change a galaxy-and-expansion prediction to justify extra terms.

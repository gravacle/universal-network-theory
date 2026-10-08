# Independent review of the conditional stationary lensing map

2026-09-29. Read the complete root-authored
`STATIONARY_LENSING_CLOSURE_V001.md`, SHA-256
`3bc694411ba8a71708cc8222589f7486863a8588856897d77f93c11aeadf055c`.
No source edit, numerical integration, observation inspection or fit.
The final opening explicitly states the minimally coupled metric dictionary;
this clarification was read after the full mathematical review below.

**Accepted within its stated conditional domain.** No remaining sign, factor
or mathematical-scope error was found. This review independently checks the
observable-map derivation. I previously participated in deriving the adopted
mode stress; that antecedent is not claimed as an independent new discovery.

## Einstein and source equations

For f=1-2Gm/r, the tt Einstein equation gives m'=4pi r²rho and the rr equation
gives N'/N=G(m+4pi r³p_r)/(r²f). Radial stress conservation gives
p_r'=-(rho+p_r)N'/N+2(p_t-p_r)/r. These equations use the TOTAL stress. Keeping
DeltaU inside rho and p while separately inserting another Lambda into f
would double count it; the reviewed note does not do so.

The mode source agrees with the static averaged action, including its
anisotropy. With nu=N'/N, a=sqrt(f)nu and F=Bbar h', its radial conservation
can be checked directly:

    Pi'=-(E+Pi)nu+F a',
    p_r'/C=-(E+Pi)nu-aF',
    nu*div F=a(F'+2F/r).

Every term in p_r'+(rho+p_r)nu+2(p_r-p_t)/r cancels. The -aF in p_r and
div F in rho are necessary. The note retains ordinary-matter stress and
does not assume that a static pressureless disk is a solution.

## Timelike and null readouts

The circular radial geodesic equation gives coordinate angular frequency
Omega²=N N'/r. The static-observer speed is r Omega/N, hence v²=r N'/N
exactly. The stated timelike-existence condition and separate stability
qualification are correct in a static region with N,f positive.

Using affine E=N² tdot and L=r² phidot in the null normalization yields

    rdot²=f E²(N^-2-b²/r²),   b=|L|/E.

Dividing L/r² and E/N² by the appropriate sign of rdot gives exactly the
two absolute integrands in equation (5). The local tetrad has photon energy
E/N and azimuthal momentum |L|/r, giving sin(alpha)=bN/r. The revised
unsigned-b convention removes the earlier purely notational sign ambiguity.
The stated N_obs Delta t conversion is correct for a fixed static observer.

These are test-particle/optical readouts of the ADOPTED metric coupling:
ordinary massive tracers follow its timelike geodesics and minimally coupled
geometric-optics photons follow its null geodesics. This is not a separate
derivation of a native BS photon coupling. A future alternative microscopic
light coupling would have to be matched, rather than silently substituted.

Finite endpoints, allowed radial intervals and actual turning points must be
used. The note properly refuses an asymptotically flat infinite-ray boundary
for a positive-vacuum cosmological exterior. Its travel time is a transfer
between specified boundaries, not yet a measured cosmological time delay.

## Weak-field pressure diagnostic

The isotropic-coordinate definition implies r=varrho(1-Psi) at first order.
Equating radial metric coefficients then gives Psi'=Gm/r². Combined with
the first-order lapse equation, this yields

    M_dyn=m+4pi r³p_r,
    M_lens=m+2pi r³p_r,
    M_dyn-M_lens=2pi r³p_r.

The factor two and signs are correct. M_lens is a local potential-gradient
diagnostic, not a projected observed mass at the same radius. A smooth vacuum
contribution in these static coordinates is not by itself a localized lens.
The stated requirement to subtract/match the same background in metric,
density, pressure and observer geometry is essential and adequate.

## Interpretation

The result supplies a linked prediction map once a valid stationary solution
is obtained. It adds no independently fitted lensing profile. It does not
provide that solution, its formation or stability, a native metric/ruler,
a scalar-to-isotropic-vector identification, or an observed lensing success.
The next use is correctly limited to retaining N,f and the complete stress
when a static solver is actually run, and predicting both kinds of readout.

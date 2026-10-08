# The adopted K=0 interface on an expanding background

2026-09-28. New analytical continuation. No numerical worker, new kinetic
function, fitted background offset, or change to a frozen source. The result
concerns the conditional preferred-foliation action, not an identification
of the native record state with a spacetime clock.

## Result

Positive de Sitter curvature improves the scalar quadratic problem in a
specific way: every fixed nonzero spatial Fourier mode has a positive
kinetic coefficient when `J_Y(0)<0`. It still has no quadratic restoring
term or propagating sound wave. Its curvature perturbation has a constant
mode and a decaying mode. This is a constructive linear stability result,
not a proof of nonlinear stability or a newly generated matter component.

The same action has an exact linear perturbation that scales as `a^-3`,
but its homogeneous density is zero and its spatial average is a boundary
term. Its amplitude is initial data, not a population predicted by the
mechanical static force law. The leading proper-slice averaged energy of
weak acceleration inhomogeneities is instead radiationlike. Thus neither
the positive background curvature nor those weak inhomogeneities supplies
the missing homogeneous dust density within this fixed action.

## 1. Action, conventions and what is imported

Set `c=1` throughout the derivation and `M^2=1/(8pi G)`. Take

    S=(M^2/2) integral sqrt(-g)[R-2J(Y)] d^4x+S_m,
    u_mu=-partial_mu T/sqrt(-partial T squared),
    A_mu=u^nu nabla_nu u_mu,     Y=A_mu A^mu.

The mechanical response, under the already stated absolute matching, has

    J(Y)=Lambda+jY+O(Y^(3/2)),    Lambda>0,    j=-1.

Keeping `j` explicit checks signs. The papers sometimes write `J=-alpha Y`
with positive `alpha`; their `alpha` equals `-j` here. The cubic-in-acceleration
term enters nonlinear perturbation theory, not the quadratic action about
`A_mu=0`.

The imported covariant metric equation and clock current are equations
(9) and (14) of [Blanchet and Skordis (2024)](https://arxiv.org/html/2404.06584v2),
specialized directly to `K=0`. Its section 4 also supplies the background
and gauge conventions. The derivation below does not take a singular limit
of fluid variables divided by a vanishing clock background density. The
original action is [Blanchet and Marsat (2011)](https://arxiv.org/pdf/1107.5264).

## 2. Exact homogeneous equations

For FLRW and a clock aligned with cosmic time, `A_mu=0`. An arbitrary
monotonic relabeling `T -> f(T)` leaves the foliation unchanged, so choose
`T=t`. The clock equation is identically satisfied on this background.
There is no clock-density integration constant. With spatial curvature `K_s`,

    3[H^2+K_s/a^2]=8pi G rho_m+Lambda,
    -2Hdot-3H^2-K_s/a^2=8pi G p_m-Lambda,
    rhodot_m+3H(rho_m+p_m)=0.                             (1)

Here `rho_m,p_m` include whatever ordinary species have actually been
specified, not an undeclared cold component. Vacuum with flat spatial
sections has `a=exp(Ht)` and `H^2=Lambda/3` on the expanding branch. Restoring
units gives `H_vac^2=c^2 Lambda/3`, the previously derived vacuum scale.

Changing the foliation's homogeneous time label cannot create matter: the
action depends on its normalized normal and acceleration, not that label's
homogeneous rate. A nonzero homogeneous clock kinetic energy would therefore
require additional owned physics, not a choice of the same clock coordinate.

## 3. Direct scalar equations on spatially flat FLRW

For the following perturbation analysis choose flat spatial sections;
de Sitter's four-dimensional curvature is still nonzero. Use Newtonian gauge

    ds^2=-(1+2Phi)dt^2+a^2(1-2Psi)delta_ij dx^i dx^j,
    T=t+pi,
    Upsilon=Phi-pidot.

`Upsilon` is gauge invariant because the background acceleration vanishes.
To first order `A_0=0`, `A_i=partial_i Upsilon`. Separate the background
cosmological-constant stress from the remaining clock stress. Direct variation
gives

    delta rho_J= -j Delta Upsilon/(4pi G a^2),
    delta p_J=0,    delta T^0_i[J]=0,
    scalar anisotropic stress[J]=0.                      (2)

The covariant clock current has first-order components
`S^0=2j Delta Upsilon/a^2`, `S^i=0`. Its divergence therefore yields

    j Delta(Upsilondot+H Upsilon)=0.                     (3)

For `j!=0`, including the actual `j=-1`, every nonzero Fourier mode has

    Upsilon(t,x)=C(x)/a(t),
    delta rho_J= -j Delta C(x)/(4pi G a^3).               (4)

This is an actual consequence of the action. The perturbation obeys
`delta rhodot_J+3H delta rho_J=0`; ordinary density fluctuations do not
source a new `C` at this order. Initial `C=0` stays zero. On a periodic
domain, compact boundaryless slice, or a boundary with vanishing relevant
flux, the first-order density has zero spatial average and necessarily has
both signs unless it vanishes. It cannot be assigned the positive mean
density of a new dust population.

For completeness, the linear Einstein equations are

    Delta Psi/a^2-3H(Psidot+H Phi)
        =4pi G delta rho_m-j Delta Upsilon/a^2,
    Psidot+H Phi=4pi G sum_I (rho_I+p_I) theta_I,          (5)

where the ordinary-species convention is
`delta T^0_i[I]=-(rho_I+p_I)partial_i theta_I`. With negligible ordinary
anisotropic stress, `Phi=Psi`. The trace equation is

    Psiddot+3H Psidot+H Phidot+(2Hdot+3H^2)Phi
        +Delta(Phi-Psi)/(3a^2)=4pi G delta p_m.           (6)

The ordinary conservation equations complete a specified species model.
For pressureless ordinary matter, for example,
`deltadot_m=Delta theta_m/a^2+3Psidot` and `thetadot_m=Phi`.
Equations (2)–(6) retain the possible clock initial mode; they do not
silently replace it with a positive-background dark fluid. Radiation
anisotropic stress would need its ordinary traceless Einstein equation,
not the no-slip simplification used here.

## 4. Vacuum de Sitter: an exact evolution decision

Set ordinary perturbations to zero. The momentum constraint gives
`Psidot+H Phi=0`, while the slip and density constraints give

    Phi=Psi=-j Upsilon=-j C(x)/a,
    pidot=-(j+1)C(x)/a.                                 (7)

At the mechanical critical value `j=-1`,

    Phi=Psi=Upsilon=C(x)/a,    pi=pi_0(x).                (8)

The physical acceleration magnitude decays as `a^-2`. The additional
linear density decays as `a^-3`. There is no exponentially growing vacuum
scalar solution in this nonzero-wavenumber linear sector on the expanding
branch. But decay alone does not certify the kinetic sign; the next
calculation checks it explicitly.

## 5. Reduced quadratic action: what curvature does and does not repair

Use unitary gauge `T=t`, spatial metric `gamma_ij=a^2 exp(2zeta)delta_ij`,
lapse `N=1+n`, and scalar shift `N_i=partial_i beta`. Expanding the full
Einstein-plus-`J` action to quadratic order, using `Lambda=3H^2`, and
integrating spatial boundary terms gives

    S2=M^2 integral dt d^3x a^3 {
          -3(zetadot-Hn)^2
          +(grad zeta)^2/a^2-2n Delta zeta/a^2
          +2(zetadot-Hn)Delta beta/a^2
          -j(grad n)^2/a^2 }.                            (9)

One direct ADM check is that `E_ij E^ij-E^2` supplies the first square
and the shift term, while `N sqrt(gamma) R^(3)` supplies
`(grad zeta)^2-2n Delta zeta`; the acceleration part supplies
`-j(grad n)^2`. Terms proportional to the background equations have been
removed, not a free homogeneous energy.

For nonzero spatial wavenumber the shift constraint is

    n=zetadot/H.

After substitution, the mixed term is
`(a/H) partial_t[(grad zeta)^2]`. At constant positive `H`, its integration
by parts cancels the remaining Einstein spatial term, up to the specified
endpoint boundary term. With fixed endpoint variations, the reduced action is

    S2_red= -j M^2 integral dt d^3x [a/H^2](grad zetadot)^2.  (10)

This has positive kinetic coefficient for `j<0` at each fixed `k!=0`.
For a real Fourier coordinate, put
`A_k=-j M^2 a k^2/H^2>0`; its canonical momentum and Hamiltonian are
`p_k=2A_k zetadot_k`, `H2_k=p_k^2/(4A_k)>=0`. The Hamiltonian is explicitly
time dependent. Its equation is

    partial_t(a zetadot_k)=0,
    zeta_k=zeta_0,k+zeta_1,k/a.                          (11)

The gauge relation `zeta=-Psi-Hpi` reproduces (7)–(8). Setting `j=0`
leaves only the Einstein boundary contribution, the expected vacuum-GR
scalar check.

Thus de Sitter curvature does supply a positive kinetic norm that the
Minkowski reduction does not exhibit in this variable. It does **not**
generate a quadratic spatial restoring term: the sound speed remains zero,
and the constant mode has no quadratic potential cost. There is no uniform
positive bound as `k` tends to zero. The step `n=zetadot/H` is singular at
`H=0`; taking that limit after reduction is invalid. Nonzero spatial-curvature
slicing, contraction, nonlinear caustics, strong coupling, and backgrounds
with matter kinetic mixing are not certified by (10).

## 6. The first nonzero averaged clock energy is not dust

This question can be sharpened without adding another field. Project the
exact clock stress on its own normal and spatial metric. Let `D_i` be the
intrinsic slice derivative. With the constant vacuum contribution included,

    rho_J=M^2[J-2 nabla_mu(J_Y A^mu)],
    p_J=M^2[-J+(2/3)Y J_Y],
    nabla_mu(J_Y A^mu)=D_i(J_Y A^i)+Y J_Y.              (12)

The last equality follows from `u.A=0` and `u.nabla u=A`. A proper-volume
slice average with vanishing boundary flux consequently obeys the exact
stress identity

    <rho_J>=M^2<J-2Y J_Y>,
    <p_J>=M^2<-J+(2/3)Y J_Y>.                          (13)

For the critical action this yields, through quadratic perturbation order,

    <rho_J>-M^2 Lambda=+M^2<Y>+O(Y^(3/2)),
    <p_J>+M^2 Lambda=+(M^2/3)<Y>+O(Y^(3/2)).             (14)

The pressure is the trace average; using it as an isotropic homogeneous
stress additionally requires an isotropic distribution of gradients.
Equation (4) gives `Y=|grad C|^2/a^4` to the relevant order. Hence the
leading weak-inhomogeneity excess has a radiationlike energy scaling and
trace pressure, not a pressureless matter scaling.

This is a statement about the averaged **clock stress**, not a complete
averaged Einstein equation. Metric backreaction, boundary fluxes, strong
inhomogeneity, other prepared populations and nonlinear evolution could
change a broader construction; none has been computed or assumed away.
The result excludes only replacing the missing homogeneous dust by the
already displayed weak clock modes without their actual stress ledger.

## 7. The exact remaining native bridge

The fixed `K=0` action has now supplied closed homogeneous equations and a
concrete de Sitter scalar stability/evolution result. It has not supplied an
extra homogeneous matter-like degree. Its temporal clock kernel vanishes
at spatial wavenumber zero because a homogeneous relabeling does not alter
the foliation or its acceleration.

A native continuation therefore needs a specified physical map from a record
operator and prepared state to the clock/source, and its retarded temporal
kernel including the homogeneous channel. The exact missing datum is a
same-parent `Pi_clock(omega,k=0)` and its complete energy/volume variation:
does an owned native degree provide nonzero homogeneous temporal response,
with what state and conserved quantity? A static force curve or fitted
`K(Q_clock)` cannot answer this. The resident two-channel clock screen already
shows that a common rescaling of unchanged native carrier frequencies is
insufficient; a genuine operational clock/source map must do more.

The next analytical step is to project an explicitly identified native clock
insertion into the full prepared-state response and evaluate that homogeneous
kernel and its stress. If it vanishes, this interface remains vacuum plus
ordinary species; if it does not, its derived term and preparation law must
be carried through both local and cosmological equations. No arbitrary
kinetic function or abundance-setting integration constant is inserted here.

## Review record

An independent peer checked the reduction of (9) to (10), including its
boundary cancellation and pure-Einstein limit, and the resulting constant/
decaying solutions, and subsequently independently re-expanded the ADM
coefficients. That review also retained the factor `j` in (3): the clock
equation is identically absent at the pure-Einstein value `j=0`, rather than
constraining an otherwise unphysical clock. A second peer checked the flat
de Sitter linear constraints and clock relation. This note records those
scopes; it does not claim an independently implemented full cosmology.

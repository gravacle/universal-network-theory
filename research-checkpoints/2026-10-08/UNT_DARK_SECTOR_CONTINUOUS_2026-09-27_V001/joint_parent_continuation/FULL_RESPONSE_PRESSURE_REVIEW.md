# Independent review: full nonlinear response pressure

2026-09-28. Analytical review of the proposed consequence of the already
adopted `K=0` covariant interface and bounded mechanical response. No
worker, source alteration, new fitted constant or cosmological simulation.

## Verdict

The proposed exact proper-slice identities and generic range
`-1 <= <p>/<rho> < -1/3` are correct under the stated endpoint matching
and vanishing **intrinsic boundary flux**. They hold on an arbitrary
regular spacelike foliation slice, not just a homogeneous or isotropic
background. Pressure here means one third of the spatial stress trace.

For the particular bounded mechanical source, the proof strengthens to

`-1 <= <p>/<rho> < -5/9`

for finite regular fields on finite proper-volume domains. The upper endpoint is an
asymptotic value, not a new FLRW equation of state. This is a constructive
full-response negative-pressure result in the specified conditional
interface. It does not itself establish an averaged expansion history,
isotropic stress, local energy conditions or native absolute-volume matching.

## 1. Full stress, projection and the boundary term

Use `c=1`, signature `(-+++)`, `M²=1/(8*pi*G)` and exactly

`S=(M²/2) integral sqrt(-g)[R-2J(Y)] + S_m`,
`u_mu=-partial_mu T/sqrt(-partial T squared)`,
`A_mu=u^nu nabla_nu u_mu`, `Y=A_mu A^mu >=0`.

The complete additional stress is

`T_J^{mu nu}=M²[-J g^{mu nu}+2 f A^mu A^nu-2 D u^mu u^nu]`,
`f=J_Y`, `D=nabla_mu(f A^mu)`.

This sign and normalization agree with the covariant metric variation in
[Blanchet and Skordis, equations 9 and 12](https://arxiv.org/html/2404.06584v2#S2.SS2),
with their separate kinetic function set to zero. `K0_FLRW_SCALAR_REVIEW.md`
already checked its full projections and on-shell conservation. Direct
contraction independently gives

`rho=M²(J-2D)`,
`p=(q_mu_nu T_J^{mu nu})/3=M²[-J+(2/3)fY]`,
`pi^{mu nu}=2M² f[A^mu A^nu-(Y/3)q^{mu nu}]`,
`q_mu_nu=g_mu_nu+u_mu u_nu`.

For any spatial vector `V`, `nabla_mu V^mu=D_i V^i+A_i V^i`.
Therefore `D=D_i(f A^i)+fY`. For a domain on the normal slice, define
its proper-volume average and boundary term by

`<X> = integral_D sqrt(q) X / V_D`,
`B_D = integral_boundary sqrt(sigma) f A^i s_i / V_D`.

These are intrinsic-volume, not lapse-weighted or coordinate-volume,
averages. Introduce the nonnegative scalar `Upsilon_Y=-Y f` below; it is
not the clock normal and is not the earlier linear perturbation Upsilon.
Then the exact general identities, including the boundary, are

`<rho>=M²[<J>+2<Upsilon_Y>-2B_D]`,
`<p>=-M²[<J>+(2/3)<Upsilon_Y>]`,
`<rho>+3<p>=-2M²[<J>+B_D]`.                         (1)

No field equation, stationarity or isotropy was used in these projections.
Set `B_D=0` only for a closed/periodic domain, a specified vanishing normal
flux, or a controlled infinite-volume limit that actually removes it.
The vanishing energy flux in the clock's own frame is a different fact:
it does not by itself imply `B_D=0`.

## 2. Generic consequence of the complete matched response

For the stipulated response `0<mu(g)<1` at finite `g>0`, with its continuous
`mu(0)=0` limit, the adopted map is

`J_Y(Y)=mu(sqrt(Y))-1`, `J(infinity)=0`.

Convergence of the high-field integral then gives

`J(Y)=integral_Y^infinity [1-mu(sqrt(y))] dy >0`,
`Upsilon_Y=Y[1-mu(sqrt(Y))] >=0`.                    (2)

Let `j=<J>` and `v=<Upsilon_Y>`. With zero boundary flux and finite regular
averages on a finite proper-volume domain, `j>0` and `v>=0`, hence

`rho_bar=M²(j+2v)>0`,
`p_bar=-M²(j+2v/3)`,
`rho_bar+3p_bar=-2M²j<0`,
`rho_bar+p_bar=(4/3)M²v>=0`,
`w_tr=p_bar/rho_bar=-(j+2v/3)/(j+2v)`.

An infinite-volume limit needs separately convergent averages and a nonzero
limiting density; strict bounds can become limiting equalities and cannot
be applied to a `0/0` ratio. On the stated finite domain,
`-1<=w_tr<-1/3`; the lower equality requires `v=0`, which for this
strict response means `Y=0` almost everywhere. This is the ratio of
averaged stress scalars, not the average of local pressure/density ratios.
In particular, local density still contains the divergence in (1) and
need not satisfy these averaged inequalities pointwise.

Anisotropy does not spoil this scalar trace argument, because the displayed
`pi^{mu nu}` has identically zero spatial trace. It does prevent treating
the tensor automatically as an isotropic perfect fluid. Nor does positivity
of `rho_bar+p_bar` establish the pointwise null energy condition for every
direction; that condition uses the directional pressures and local density.

## 3. The bounded mechanical parent satisfies a stronger inequality

Keep exactly the relaxed classical parent from
`../joint_parent_dynamics/CRITICAL_RESPONSE_CLOSURE.md` and
`../joint_parent_dynamics/SAME_PARENT_FORCE_VOLUME_LINK.md`:

`h(g)=g/sqrt(1+g²/g_s²)`,
`W_b(g)=Kb[g²-h(g)²]/2+W_el(h(g))`,
`P(s)=Kb*s-W_el'(s)>0`, `0<P'(s)<Kb` for `s>0`.

The last strict statements follow directly from each positive-weight
adjustment mode's unique minimum

`kappa*delta²*y+u*y³=kappa*delta*s`,
`y'(s)=kappa*delta/(kappa*delta²+3u*y²)>0`.

Its response is `mu_b(g)=1-P(h)h'/(Kb*g)`. It is strictly below one;
using `P(h)<=Kb*h` gives

`mu_b(g)>=1-h*h'/g=1-(1+g²/g_s²)^(-2)>0` for `g>0`.

This confirms the generic hypotheses without fitting any value of `mu`.
The proof requires the complete compensating contact term in `W_b`.

With the separately stipulated high-field-zero matching, write
`s=h(g)`, `t=s/g_s` and `0<t<1`. Equations (2) become exactly

`J(Y)=(2/Kb) integral_s^g_s P(z) dz`,
`Upsilon_Y=g P(s)h'(g)/Kb
           =s P(s)(1-t²)/Kb`.                        (3)

Since `P` is strictly increasing, for every finite `g>0`,

`J/Upsilon_Y > 2(g_s-s)/[s(1-t²)]
               =2/[t(1+t)] >1`.                     (4)

At `g=0`, `Upsilon_Y=0` and `J>0`, so `J>Upsilon_Y` remains true.
Consequently `j>v` under the same finite proper average, and

`w_tr+5/9 = 4(v-j)/[9(j+2v)] <0`.

Combining this with the generic lower bound proves

`-1 <= w_tr < -5/9`.                                (5)

This stronger result uses the specified saturation map and monotonic
mechanical `P`, not only `0<mu<1`. It should not be assigned to every
possible network response or a different quantum/thermal prepared state.
It also holds for the analogous positive finite-mode relaxed mechanical
parent; the specific continuum density is not needed for inequality (4).

## 4. High-field asymptote and the weak-excess distinction

For this model, `g-F_b/Kb = C3/g³+O(g^-5)` with
`C3=P(g_s)g_s³/Kb>0`. Therefore, in the units used here,

`1-mu_b(sqrt(Y))=C3/Y²+O(Y^-3)`,
`J(Y)=C3/Y+O(Y^-2)`,
`Upsilon_Y=C3/Y+O(Y^-2)`.

The corresponding ratio of the algebraic averaged contributions tends
to `-(1+2/3)/(1+2)=-5/9` if a family of domains/states makes these
asymptotics dominate both averages, with subleading and low-field-region
contributions controlled. This is not a constructed cosmological solution.
An aligned homogeneous FLRW clock has `Y=0`, not a homogeneous nonzero
high-field acceleration. A mixture containing unsuppressed low-field
regions need not approach the high-field ratio.

The earlier weak-excess result is unchanged. Expanding
`J=J0-Y+O(Y^(3/2))` gives, after subtracting the **constant** vacuum tensor,

`rho_bar-M²J0=M²<Y>+O(<Y^(3/2)>)`,
`p_bar+M²J0=(M²/3)<Y>+O(<Y^(3/2)>)`.

Those leading excesses have radiationlike trace pressure; the full stress
including `J0` obeys (5). There is no contradiction, and neither result
turns the weak clock fluctuations into an independent positive dust fluid.

## 5. What is earned and what remains conditional

The exact consequence is stronger than a positive vacuum value at one point:
the same specified complete response, under the adopted endpoint matching,
maintains negative full averaged trace pressure throughout its finite-field
range. It cannot become a pressureless homogeneous clock component merely
by sampling stronger fields under these assumptions.

The absolute matching is load-bearing. The literal zero-minimum mechanical
parent has `U(0)=0`, `U(infinity)=-DeltaU`; the rule `J(infinity)=0` adds
`DeltaU` before applying the covariant map. Local force fixes the endpoint
**difference**, not this gravitationally consequential constant. Replacing
`J` by `J+C` changes `rho_bar+3p_bar` by `-2M²C` while leaving `mu` fixed.
The original UNT source/volume ledger has not yet supplied this matching.

Equations (1)–(5) are exact stress statements in the adopted action, not
averaged Einstein or Raychaudhuri evolution equations. Shear, curvature,
nongeodesic acceleration, moving-domain effects, matter, lapse weighting,
boundary exchange and metric correlations cannot be discarded when deriving
an expansion history. The mechanical relaxed-state/rate window and native
physical clock/source map also remain separate inputs. No new stability,
observational acceptance, Hubble fit, or joint-program completion is claimed.

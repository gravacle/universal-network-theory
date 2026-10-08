# Independent review: K=0 cosmological scalar decision

2026-09-28. Read-only review of `K0_FLRW_SCALAR_DECISION.md`, with independent
analytical expansions. No numerical worker, native-state identification,
changed action or edit to the reviewed file.

## Verdict

**Accepted within the stated conditional action and perturbative scope.**
The exact stress projections and conservation signs, homogeneous equations,
linear density mode, de Sitter constraint solutions, and reduced quadratic
action are consistent. I independently re-expanded the ADM quadratic action,
rather than only checking its subsequent constraint reduction.

The constructive result is specific: on expanding flat-slicing de Sitter,
each fixed nonzero scalar wavenumber has positive reduced kinetic energy for
`j=J_Y(0)<0`, and its solutions are constant or decaying. The action still
has no quadratic restoring term. Neither this kinetic result nor the weak
clock-stress average creates a positive homogeneous dust population.

One branch qualification is made explicit here: deriving the linear current
constraint `Delta(Upsilondot+H Upsilon)=0` requires `j!=0`. This holds for the
actual `j=-1` candidate. At `j=0`, the current instead vanishes at this order;
that case is the pure-Einstein action consistency check, not an application
of the same clock-mode equation. No candidate result changes.

## 1. Full stress and conservation, not only a background formula

The starting covariant metric equation/current agree with equations (9),
(12) and (14) of the primary [Blanchet–Skordis paper](https://arxiv.org/html/2404.06584v2#S2.SS2),
with its separate kinetic function set to zero. I use the note's `c=1`,
signature `(-+++)`, and `M^2=1/(8pi G)` conventions. Define

\[
f=J_Y,\quad D=\nabla_\mu(fA^\mu),\quad
q_{\mu\nu}=g_{\mu\nu}+u_\mu u_\nu.
\]

The complete clock stress in these conventions is

\[
T_J^{\mu\nu}=M^2[-Jg^{\mu\nu}+2fA^\mu A^\nu
                         -2D u^\mu u^\nu].              \tag{R1}
\]

Direct contraction, without a homogeneity approximation, gives

\[
\rho_J=M^2(J-2D),\quad
p_J=M^2[-J+\tfrac23fY],\quad q_J^\mu=0,
\]
\[
\pi_J^{\mu\nu}=2M^2 f
 (A^\mu A^\nu-\tfrac13Yq^{\mu\nu}).                    \tag{R2}
\]

Here `q_J^mu` denotes energy flux, not the spatial projector. The stress is
not generally isotropic: zero flux does not remove its nonlinear anisotropic
part. These projections fix both signs in the reviewed equation (12).

The divergence identity used in averaging also follows directly. For any
spatial vector `V` with `u.V=0`,

\[
\nabla_\mu V^\mu=D_iV^i+A_iV^i.
\]

Setting `V=fA` gives `D=D_i(fA^i)+fY`, with the **plus** sign shown in the
reviewed note.

For an additional conservation check, put
`Q=sqrt(-partial T squared)` and `s=u.nabla ln Q`. Then
`A_mu=-q_mu^nu partial_nu ln Q`, and the current is

\[
S^\mu=\frac{2}{Q}[fA^\mu s+D u^\mu].                  \tag{R3}
\]

Projecting the divergence of (R1) along the slice gives zero identically:
the `2D A_i` terms cancel and the remainder is
`2M^2 f A^j(D_j A_i-D_i A_j)=0`, since `A_i` is an intrinsic gradient.
The normal projection is

\[
u_\nu\nabla_\mu T_J^{\mu\nu}
 =M^2[-\dot J-2fA^\mu A^\nu K_{\mu\nu}
                   +2(\dot D+D\theta)]
 =M^2Q\nabla_\mu S^\mu.                                \tag{R4}
\]

The second equality uses
`dot J=-2f[A^mu partial_mu s+A^mu A^nu K_mu nu+Ys]` and follows by
differentiating `A_mu=-partial_mu ln Q-u_mu s`. Thus

\[
\nabla_\mu T_J^{\mu\nu}=-M^2Q u^\nu\nabla_\mu S^\mu.
                                                               \tag{R5}
\]

The clock equation therefore gives covariantly conserved complete clock
stress, consistently with the metric Bianchi identity. There is no extra
independently conserved positive dust tensor hidden in this calculation.

## 2. Homogeneous and linear equations

For the aligned homogeneous foliation, `A=0`, `D=0`, so (R1) is exactly
`-M^2 Lambda g^mu nu`. The clock current vanishes. A homogeneous monotonic
clock relabeling does not change this foliation, hence does not introduce a
homogeneous density integration constant. The displayed Friedmann equations
and `H^2=Lambda/3` expanding vacuum solution follow with the stated signs.

At first order, `A_i=partial_i Upsilon` and
`D=j Delta Upsilon/a^2`. Subtracting the constant vacuum tensor from (R1)
gives

\[
\delta\rho_J=-2M^2j\Delta\Upsilon/a^2,
\qquad\delta p_J=\delta T^0_i[J]=\delta\pi_J=0.
\]

The first term in (R3) is quadratic, while its second term gives
`S^0=2j Delta Upsilon/a^2`, `S^i=0` at linear order. Conservation yields
`Delta(Upsilondot+H Upsilon)=0` for `j!=0`, reproducing the nonzero-mode
`Upsilon=C(x)/a` and `delta rho_J proportional a^-3` solutions.

The ordinary velocity convention, continuity equation and Einstein momentum
constraint in the note are mutually consistent. In vacuum, zero linear slip
and the momentum/density constraints give
`Phi=Psi=-jC/a` and `pidot=-(j+1)C/a`. At `j=-1`, `pi` is time independent.
This retains the arbitrary spatial initial mode; it does not predict its
amplitude or turn its Laplacian density into a positive mean population.

On a periodic/closed slice or a boundary with zero Laplacian flux, that
linear density integrates to zero. At first perturbative order, background
and proper-volume averages agree for this zero-background excess. A
nonzero continuous mode therefore contains both density signs. The
homogeneous mode is absent, not an undetermined positive dust normalization.

## 3. Independent ADM expansion and reduction

With `gamma_ij=a^2 exp(2zeta)delta_ij`, `N=1+n`, `N_i=partial_i beta`, let
`L=H+zetadot` and define the mixed shift derivative `B_i^j` by
`E_i^j=L delta_i^j-B_i^j`. Then

\[
\operatorname{tr}E^2-(\operatorname{tr}E)^2
 =-6L^2+4L\operatorname{tr}B
          +\operatorname{tr}B^2-(\operatorname{tr}B)^2.
\]

At the needed order
`tr B=a^-2 exp(-2zeta)[Delta beta+grad zeta.grad beta]`.
The integrated quadratic shift-squared combination vanishes under the
stated spatial boundary conditions. The mixed `H zeta Delta beta` and
`H grad zeta.grad beta` terms cancel by spatial integration by parts.

Expanding `sqrt(gamma)/N` and the cosmological term, using
`Lambda=3H^2` and constant `H`, and integrating the pure `zeta zetadot`
term by parts leaves the quadratic extrinsic-curvature contribution
`-3M^2 a^3(zetadot-Hn)^2` and shift contribution
`2M^2 a(zetadot-Hn)Delta beta`. In particular, the `zeta n` and `zeta^2`
terms cancel against the cosmological/background terms; they have not been
omitted as an arbitrary energy subtraction.

Independently,

\[
R^{(3)}=a^{-2}e^{-2\zeta}
 [-4\Delta\zeta-2(\nabla\zeta)^2]
\]

gives `M^2 a[(grad zeta)^2-2n Delta zeta]` after multiplication by
`N sqrt(gamma)` and integration by parts. Finally
`Y=a^-2(grad n)^2+O(perturbation^3)` gives
`-jM^2 a(grad n)^2`. These independently reconstruct every term in the
reviewed quadratic action (9).

For `k!=0`, variation of the shift imposes `n=zetadot/H`. The remaining
Einstein mixed term integrates to
`[a(grad zeta)^2/H]` at the temporal endpoints minus
`integral a(grad zeta)^2`, exactly canceling the other spatial term. With
the specified fixed endpoint variations, the reduced bulk action is

\[
S_2=-jM^2\int dt\,d^3x\,\frac{a}{H^2}
                         (\nabla\dot\zeta)^2.           \tag{R6}
\]

For each fixed real nonzero Fourier coordinate its kinetic coefficient is
positive at `j<0`, and `H_2=p^2/(4A_k)>=0` as stated. Its equation gives
`zeta=zeta_0+zeta_1/a`. The Hamiltonian is time dependent; the kinetic
positivity claim is not a claim of a conserved positive de Sitter energy.
There is no restoring term or nonzero sound speed. The kinetic coefficient
vanishes as `k^2`; the `H=0` limit of this constrained variable reduction is
singular. Neither sign choices nor the absence of exponential solutions
alone establish nonlinear, homogeneous-channel or matter-mixed stability.

The conclusion is consequently stronger than decay of a guessed equation,
but narrower than a general ghost-free or stable-gravity theorem. It is
valid for the stated expanding de Sitter background and fixed nonzero modes.

## 4. Proper-volume average and the radiationlike statement

For the exact intrinsic proper-volume average, the divergence theorem gives

\[
\langle D_i(fA^i)\rangle
 =\frac1{V}\int_{\partial\Sigma}\sqrt{\sigma}\,fA^i s_i.
\]

Hence only under the stated zero-flux/closed/periodic assumption do (R2)
become the exact identities

\[
\langle\rho_J\rangle=M^2\langle J-2YJ_Y\rangle,\qquad
\langle p_J\rangle=M^2\langle-J+\tfrac23YJ_Y\rangle.
\]

For `J=Lambda-Y+O(Y^(3/2))`, their leading excesses are respectively
`M^2<Y>` and `M^2<Y>/3`. The sign is positive, despite the negative linear
coefficient in `J`. For the linear solution,
`Y=|grad C|^2/a^4` at quadratic order. Corrections to the proper-volume
measure multiply an already quadratic `Y` and do not change this leading
result. The constant vacuum contribution averages to itself exactly.

This establishes a radiationlike **trace pressure and leading weak clock
energy scaling**. Isotropic stress additionally needs an isotropic gradient
distribution. It is not a derived separately conserved radiation fluid, a
complete averaged Friedmann equation, or a nonlinear bound on strong
inhomogeneities. The reviewed note explicitly retains these distinctions.
In particular, its exact averaged stress identity is not a license to
discard metric backreaction or boundary exchange in a cosmological model.

## Scientific consequence

The existing conditional `K=0` interface now has an actual expanding-vacuum
scalar calculation rather than an unresolved flat-space extrapolation.
It supplies neither a homogeneous clock matter density nor a means of
choosing one from the static galaxy force. Its next native bridge is therefore
a specified clock/source insertion, including its homogeneous temporal
response and complete source/volume work. This conclusion follows from this
particular action's symmetry and equations; it is not a no-go for a network
completion with independently derived additional retained dynamics.

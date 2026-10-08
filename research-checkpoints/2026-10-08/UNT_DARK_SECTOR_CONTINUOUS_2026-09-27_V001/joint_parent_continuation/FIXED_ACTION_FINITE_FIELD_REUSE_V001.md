# A one-root finite-field calculation at unchanged actions

2026-09-29. Analytical/source-only reduction. No worker, new physical state,
fit, source rescaling or amendment to any frozen implementation.

## Exact centered-turning-point reduction

In the inherited dimensionless units let

    U(y)=delta² y²/2+y^4/4-delta h y,
    a=c-r, b=c+r, r>0.

Equal turning energies U(a)=U(b) are equivalent to

    c³+(delta²+r²)c=delta h.                              (1)

Thus one trial half-width r determines c by the existing stable hyperbolic
solution of a positive-stiffness cubic. In that formula replace delta by
sqrt(delta²+r²) and replace its driving product by delta*h; do not silently
replace the physical coupling delta by the new square root.

With y=c+r cos(theta), the already qualified factorization becomes

    e-U(y)=(b-y)(y-a)Q(y)/4,
    Q=(y+c)²+2delta²+2c²+r² > 0,
    I(r,h)=r²/(sqrt(2) pi) integral_0^pi sin²(theta)sqrt(Q) dtheta,
    T=2sqrt(2) integral_0^pi dtheta/sqrt(Q),
    <y>= integral_0^pi y dtheta/sqrt(Q)
                            /integral_0^pi dtheta/sqrt(Q).       (2)

There is ONE root to solve: I(r,h)=I_saved. It is unique. In fact

    c_r=-2cr/(delta²+r²+3c²),   |c_r|<1,
    b_r>0, a_r<0,   e_r=U'(b)b_r>0,
    I_e=T/(2pi)>0.

Strict convexity places the minimum between a and b, proving the signs.
Furthermore Q>=2delta², so

    I(r,h)>=delta*r²/2,
    0<=r<=sqrt(2I_saved/delta)                            (3)

is an analytic bracket, independent of field strength. No nested energy
bisection plus two turning-point bisections is required. I=0 is the separate
continuous minimum branch r=0; its angle coordinates are not inverted.

For a stable excitation ledger at tiny r, first compute the minimum c_star
from c_star³+delta² c_star=delta h. The exact identity

    c-c_star=-c r²/[delta²+c²+c*c_star+c_star²]

avoids subtracting close roots. Put x_plus=r+(c-c_star) and evaluate

    e_exc=x_plus²[(delta²+3c_star²)/2+c_star*x_plus+x_plus²/4],
    e_min=-delta²*c_star²/2-3c_star^4/4,
    e=e_min+e_exc.                                       (4)

Retain e_min and e_exc separately rather than recover a tiny excitation by
subtracting two large negative absolute energies. The source response is

    D_I(G)=G-h'(G)sum weights*delta*<y> / Kb,
    h(G)=G/sqrt(1+(G/gs)^2),

with the SAME actions at every G. The constant DeltaU is unchanged. The full
source work along an ideal fixed-volume adiabatic continuation is the change
of Kb G²/2+sum weights*e; it is not a new phase-space preparation at each G.

## Existing code to reuse, and what not to call in an inner loop

The following immutable sources were fully read:

- `common_history_phase_mean_v001.py`, SHA-256
  `c012dd19e532656559c554d64a54a368ab4c73a76cddbfe8415c82a00f188ab2`:
  `phase_mean()` owns the stable cubic minimum/excess potential, independent
  turning-point brackets, factorized time means, period, virial and force
  controls. Its numerical method was preserved through the V002/V003
  publication-only repairs.
- `prepared_action_return_v001.py`, SHA-256
  `599b12e2a6cc9e7f5807492399b86b959a76ddcef1c7a4ab9b6b0f401ad94293`:
  the first part of `solve_actions()` already implements the exact I integral
  in (2), and the rest qualifies the ideal h=0 action inversion.
- The corresponding protocols have hashes
  `9fe8ba251672de898cd527bd8c66c628c63acfe5cb8d52b75d5b86c98d87139c`
  (`COMMON_HISTORY_PHASE_MEAN_PROTOCOL_V001.md`) and
  `1017b75e3702ce8e1a52057ce071770cd6541a8c56dff7e7fdae2b0c67a33b57`
  (`PREPARED_ACTION_RETURN_PROTOCOL_V001.md`).

The smallest additive helper needs only the centered cubic and the action/
moment portion of these kernels. Calling all of `solve_actions()` inside
every root step would unnecessarily run its 75-step zero-source return each
time. Calling `phase_mean()` there would likewise repeat its two 90-step root
solves. Retain their code unchanged and use the original routines only as
final independent implementation checks where applicable.

Do not import the V002/V003 publication wrappers as general-purpose libraries:
they deliberately replace globals in the V001 module. Also, the original
`phase_mean()` force-error denominator assumes positive h. It is not a valid
h=0 or signed-negative-h control without a NEW explicitly corrected wrapper.
Positive-h use with y=c_star,v=sqrt(2e_exc) represents the solved energy and
tests the centered-root result against its independently bracketed roots.

## Proposed compact, complete first census

Before any run, freeze all 36 saved returned-action templates, including both
gaps, both durations, all three preparation amplitudes and every old numerical
resolution. Keep the same spectral weights, inherited gs, and actual actions.
Use these seven positive/exact-zero external fields in the original units:

    G={0,1e-5,.0025,.01,.04,1,100}.

They are not chosen from galaxy residuals. The three middle low values include
EVERY template's original prepared-source amplitude; 1e-5 probes the origin,
1 is an intermediate scale, and 100 probes the bounded-source regime. This is
a finite-field diagnostic, not a dense interpolation table ready for a galaxy
fit. Both the floor and nonlinear curve must be computed from (2), not inserted
as a guessed mu*G+G²/a0 formula.

Use precomputed 64/128 angle rules and one 64-step radius bisection, batching
one original case at a time. Six nonzero fields over 3,840 modes require roughly
2.8e8 quadrature-node evaluations across those two rules. The largest ordinary
working arrays have order 128*6*128 entries; routine temporary storage can stay
well below 256 MiB without global field/mode/node tensors. This is a work-count
estimate, not a measured runtime or permission for a second simultaneous worker.

Keep h=0 mean and D exactly zero and its saved returned energy, pressure and
exact susceptibility as separate origin controls. Check the new radius/action
inversion there against the old zero-source turning amplitudes. At EACH
template's own original nonzero G, the SAME-action result must reproduce the
old independently prepared energy and qualified phase mean. Independent final
turning-point/action checks may call the old positive-h routines once per
selected control, never in the inner loop. Root should prospectively freeze
that exact validation census and scale-aware tolerances before execution.

Retain all 252 template/field outputs, all quadrature/resolution comparisons,
and any failures. This procedure follows one retained action state through
field values. It supplies e(I,h), its mean source response and frequencies for
the scalar static closure; it does not solve the metric/clock constraints,
prove adiabatic formation, or identify the isotropic-vector response with the
scalar one. No new production worker has been started by this note.

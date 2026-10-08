# Independent preflight: fixed-field disk response diagnostic

2026-09-28. Full read-only review of `disk_response_diagnostic.py` and
`DISK_RESPONSE_DIAGNOSTIC.md` before execution. No field solve or diagnostic
worker was run by the reviewer. **Accepted; no blocking defect found.**
Reviewed source SHA-256:
`5e02341fb60f09fec1fdd46bf9df3a272aa219e0606dc545498a8b1d8bfa535a`;
protocol SHA-256:
`6e5b31f57dcb8cbd066ad7a47ce750785555f23bff01a80a1906d3547480e7bc`.

## Mathematics and signs

The fields are components of `grad Phi`, so positive radial values describe
inward gravitational acceleration. The upper-sheet jump has the positive
sign `mu(s) z=b=2*pi*G*Sigma/a0`. Holding signed radial `x` fixed gives

`d[mu(s)z]/dz = mu(s)*x²/s² + f'(s)*z²/s² >0`,
`s=sqrt(x²+z²)`, `f(s)=s*mu(s)`.

The existing mechanical law has positive `mu,f'` at positive s. The left
side starts at zero and tends to infinity, so the solution is unique. At
`x=z=0` the displayed divided formula is replaced by its continuous limit;
for `b=0`, strict positivity away from zero still makes `z=0` the unique
solution. The code explicitly handles this case and signed radial fields.

The compulsory positive-contact term in the exact `law.f` supplies
`mu(s)>=1-[1+(s/r)^2]^-2`. At the specified
`z_hi=2*(b+abs(x)+r)`, `s>=z_hi>=2r,2b`; hence
`mu(s)z_hi>=24*z_hi/25>=48*b/25`. This verifies the safe bracket
independently of the actual future galaxy diagnostic values. Seventy
bisection steps and the explicit sheet-jump check provide the declared
arithmetic check, not an independent solver-boundary test.

Both continuum equations have the same density source. Their difference
therefore gives `div[mu(g)g-gN]=0`. At the symmetric sheet its vertical
component is zero and radial component is exactly `mu(s)x-n`, with the
sign used in code. Different finite-domain boundary approximations and
field differentiation/interpolation enter this numerical estimate; they
are correctly not reclassified as an isolated intrinsic curl correction.

The full-vector inverse `(n,b)/hypot(n,b)*f^-1(hypot(n,b))` has the correct
radial projection. Replacing `n` by `n+S_R` returns `x` under the reconstructed
jump. Zero-vector and outward-radial cases remain explicit. The four terms
sum identically to `x-k`, and multiplication by `R*a0`, followed by adding
the spherical-reference residual, reproduces the actual signed velocity-
squared residual. This is an ordered descriptive partition, not a unique
causal separation or a likelihood decomposition.

For the exact Kuzmin reference, `g` and `gN` are parallel at every upper-half
point, so `S_R=0` and `x=v`; the vertical-projection and disk/monopole terms
need not vanish. This is a useful sign and interpretation check.

## Source, custody and interpretation

The script requires all 16 predetermined original cases and all original
checks; it cannot preferentially select the first completed models. It
verifies the galaxy freeze, every named frozen source, each case identity,
payload digest and original pass flags. It records hashes of all case files
in its output. The same N512/L255 source is used for Newtonian/nonlinear
comparisons; the separate domain/refinement shifts remain visible.

The measured source profiles and fixed tails are re-used without a new
normalization. Independent mass closure is checked for all three components.
All 43 radii and negative signed contributions are retained. Hard-edge
distances are descriptive warnings, not a row-deletion criterion. Missing
real diagnostic circular speeds are represented as null rather than using
the magnitude of an outward force.

The expected arithmetic census is 4 models × (43 rows × 4 identities +
3 component-mass comparisons) = 700 checks. Passing these would establish
postprocessing consistency only; they are not 700 observational tests.
No force, tolerance, source or observed velocity enters an optimization.
The recipe's statement that the data were already exposed correctly
excludes a new blind-prediction interpretation.

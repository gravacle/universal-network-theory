# Independent review: frozen axisymmetric disk benchmark

2026-09-28. Reviewed the complete protocol, preflight, solver source, freeze
and all nine saved cases. No solve, Picard iteration or PCG call was executed
by this reviewer. The numerical checks below are algebraic reconstruction
of saved fields, source evaluations and hashes; no frozen file was changed.

## Verdict and results

**Accepted: all nine cases satisfy the frozen benchmark, including all 63
saved case checks.** Every refinement lowers the prospectively scored
maximum disk radial-force error. The finest errors are below the fixed 2%
criterion at all three field strengths.

| eta | N=32 maximum error | N=64 maximum error | N=128 maximum error | Finest relative flux imbalance |
|---|---:|---:|---:|---:|
| 0.01 | 6.4184% | 2.1523% | 0.6311% | 1.4371e-8 |
| 1 | 8.4952% | 2.9376% | 0.8750% | 5.1719e-8 |
| 100 | 11.5354% | 3.9940% | 1.1845% | 5.8190e-7 |

The first refinement improves the errors by factors 2.888–2.982; the next
improves them by 3.357–3.411. This establishes observed converging radial
accuracy on the declared meshes and interval, not an independently proved
asymptotic order for every boundary/source configuration.

Across all cases:

- Maximum saved nonlinear normalized residual: `9.469080216823959e-10`,
  below `1e-9`.
- Maximum saved relative total flux imbalance: `5.819021006861551e-7`,
  below `2e-6`.
- Maximum 48-versus-96 boundary quadrature difference:
  `2.4725566743666754e-14`, below `1e-9`.
- Maximum relative annular-mass error: `1.9803564644350288e-16`, below `1e-13`.
- Final clipped faces: zero in every case; all scored radial fields positive.
- Every saved inner solve reports residual at most `1e-12`, no linear failure,
  and every case converges in 14–16 Picard iterations.
- Summed recorded case runtime: `4.3532249980198685` seconds. Maximum recorded
  process-self peak RSS: `44,761,088` bytes. This is the process high-water
  reading, not a measured job-tree memory total or full end-to-end runtime.

## 1. Source law and inherited normalization

The fixed ratio `r=25.51664211557329` is inherited from the previous two-input
reference calculation. It is not a newly predicted astronomical number or
a per-disk fit. The solver uses `a0_internal=8/(3pi)`, `Kb=1/2`, and returns
`F_b(a0_internal*g)/(Kb*a0_internal)`, so its flux and argument both have
the declared `a0=1` units.

The closed elastic force agrees algebraically with the preceding
quadrature-tested expression. If `y^3+y=h`, set `z=1/(1+y^2)`. Then
`z+h^2 z^3=1` and

    atan(1/y)=asin(sqrt(z)).

Thus the new hyperbolic-cubic root and angle are exactly the same cutoff
solution used by `shape_reference_compute.py`. Its force is

    F_el(h)=h^2/4 [3theta/2-sin(2theta)/2-sin(4theta)/8].

Combining `F_el(h) h'` with the full positive compensation
`Kb*g[1-(1+(g/gs)^2)^(-2)]` retains the same mechanical source work. The
solver does not drop the derivative of the bounded source or use the
unbounded-source force in its place.

I independently evaluated this law on all 81 central saved inverse-response
rows from the prior quadrature calculation. Maximum relative flux mismatch
was `1.6986412276764895e-14`. The linked prior evidence also authenticates
81 closed-force versus direct-quadrature checks, whose largest recorded
relative residual is `2.3391024577963288e-14`.

## 2. Exact disk and finite-volume conservation

For the upper half-space Kuzmin construction,
`s=sqrt(R^2+(z+1)^2)` and the exact field is
`grad Phi=g(s) grad s`, with `f(g)=eta/s^2`. Hence its flux is the Newtonian
point-source field centred below the domain, whose divergence vanishes in
the upper half-space. At the sheet,
`mu*partial_z Phi=eta/(R^2+1)^(3/2)` in the declared units. Integration over
an annulus gives the exact bottom flux used by the source.

The entire retained bottom flux therefore sums to
`eta[1-1/sqrt(65)]`. This is the reduced cylindrical flux convention with
the common `2pi` omitted; no full-space factor of two is missing. The
bottom outward normal supplies its negative source contribution.

The internal radial/vertical conductances carry the correct cylindrical
face weights; the outer Dirichlet half-cell distance gives the factor two.
Shared conductances cancel exactly between adjacent cells and give the
positive symmetric Picard linear operator. Its coefficient uses the norm
of both gradient components, not a scalar radial-force approximation.

I reconstructed every saved disk-potential extrapolation and radial finite
difference directly from its `phi` array. The maximum absolute difference
from the stored radial derivative was `2.842170943040401e-14`. I also
reconstructed internal face fluxes, outer/top fluxes and annular sources
with independently assembled divergence sums. Every reconstructed field
still satisfies both frozen residual and flux criteria. The minimum final
face coefficient across these reconstructions was about `0.00829483369`,
far above the numerical floor `1e-12`.

Those reconstructions reevaluate analytical boundary data; they do not use
the exact interior potential to repair the saved grid. Exact boundary data
are an intentional oracle of this benchmark. They do not establish a
practical open-boundary treatment for arbitrary observed galaxies.

An initial audit-only near-machine-equality assertion on recomputed flux
diagnostics triggered. Explicit reconstruction found maximum differences
of `1.6959025800925911e-15` in normalized residual and
`4.573124065304808e-12` in relative flux imbalance from algebraically
equivalent expression ordering. The frozen acceptance thresholds and all
case files remained unchanged; both independent values pass those original
thresholds. This was an audit-roundoff comparison, not a repaired solver
case or an additional physical run.

## 3. Custody, publication and resume

The disk freeze has SHA-256
`d207bd7e880ebab47759322fa94aa2dd0a51da1b841498447a8de057839734d3`.
Every named source matches it:

| File | SHA-256 |
|---|---|
| `disk_solver.py` | `a620e49e1267cff2131e198b63817e66bd394eff552031ba559e97d2a3fbfa47` |
| `DISK_SOLVER_PROTOCOL.md` | `536a649a96a39d20d610e034c0f0fbd29d871158f68088d4514ac15228fcc570` |
| Prior `SHAPE_REFERENCE_RESULTS.json` | `0ed80105e9b615e5de68594ebf37d25ae42623d7724d4336101ed6966dddb7a9` |

The linked shape result's own payload, freeze, five named source files and
all 1,632 prior checks authenticate. Its named mechanical freeze and all
three mechanical source entries also match current bytes. This verifies the
source/evidence linkage; hashes themselves do not establish mathematical or
observational validity.

All nine disk records have correct canonical payload hashes, exact `N/eta`
identities, grid/vector dimensions and the same disk-freeze hash. Their
scored errors, final histories and refinement comparisons were recomputed
from the saved data. Whole-file hashes are:

| N | eta | SHA-256 |
|---:|---:|---|
| 32 | .01 | `17a050721edce57073301614b0ebbc568783df6fedb76393badad011ac048572` |
| 32 | 1 | `fcdfd7a6c35b45e4a5351e30a9d109562304f06b1709b897526af796365fbe6a` |
| 32 | 100 | `61edcebc6a9f4e40f692d5d87a7309928bc76d672b2c8d30dd81ec571c981c91` |
| 64 | .01 | `0da692b60c0090873261deb205944fb69cd4763a41298f193e42b03608bd6517` |
| 64 | 1 | `66249e22fa313ca82477e4b4e159ea20c66f218c44c0cf2ee01dac21ecbb3dcf` |
| 64 | 100 | `01da587c58c724dafec47325e9c154319d74478a4aa68da99f140ec828dfe370` |
| 128 | .01 | `667caba389a666db8d9bb38af6347a3b73f17963c880bae43490a298e745d768` |
| 128 | 1 | `6830b99072f9dc27c9ccb72ac86b5dd1c31cb164a96c78220688e0f4aa550a33` |
| 128 | 100 | `285a3d4bb157f51db4c440404271445b5095fe5cb16ade340903dffad6ceaf0b` |

Source inspection confirms serialized/flushed temporary-file publication
through an atomic no-overwrite hard link. Resume verifies the freeze,
payload, case identity, pass flags and previous-refinement comparison before
skipping a case. This is completed-case restart support, not an in-iteration
checkpoint or a claim of recovery from every hardware/filesystem failure.

## Scientific meaning

The adopted nonlinear field law now has a checked two-dimensional
axisymmetric implementation, including nonradial gradients, sheet source,
flux conservation and refining radial accuracy. That is a useful step from
a spherical force curve toward actual disk calculations. This exact family
does not validate the physical field equation, remove its inherited
calibrations, test observed galaxy residuals, certify arbitrary disk
boundaries, or supply the missing native clock/volume completion. No such
observational or joint-program success is claimed by this review.

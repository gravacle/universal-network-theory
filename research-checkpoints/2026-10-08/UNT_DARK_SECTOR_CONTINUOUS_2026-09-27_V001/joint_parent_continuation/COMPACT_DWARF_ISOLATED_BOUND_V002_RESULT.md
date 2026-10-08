# Isolated compact-dwarf result, with technical failure retained

2026-10-05 UTC. The analytical critical-response comparison was independently
reviewed. V001's original JSON remains FAILED: one cancellation-prone
closed-form reference missed its fixed tolerance. V002 reevaluated only the
five reference expressions with standard-library Decimal80; it authenticated
V001, retained all criteria and did not recompute the scientific rows.
All 23 combined controls now qualify, with maximum repaired relative error
4.97e-15. V001/V002 internal times were 0.01650/0.00148 s. Independent read-only
review accepted custody, the repair and the result qualifications.

| Nominal stellar mass | Global LOS ceiling | 67 pc aperture LOS ceiling | Necessary ell ceiling to permit 3.7 km/s under this bound |
| --- | --- | --- | --- |
| 340 solar masses | 0.13202 km/s | 0.14308 km/s | 1.32624 pc |
| 1020 solar masses | 0.22866 km/s | 0.24783 km/s | 2.30016 pc |
| 3400 solar masses | 0.41748 km/s | 0.45247 km/s | 4.21912 pc |

All actual result rows keep ell=100 pc. No shorter length was adopted or
fitted. These are conservative total-kinetic upper bounds, not the usual
isotropic factor-of-three prediction or a fitted observational likelihood.
The source/tracer, equilibrium, aperture selection, stellar population and
geometry qualifications in V001 and the external-field result remain.

## What this decides

Merely choosing an isolated, rather than a uniformly externally accelerated,
clock state does not rescue the frozen 100-pc-filter stellar Plummer models.
Their isolated ceiling is below the exposed approximately 3.7 km/s central
dispersion estimate. The warning is therefore not removable just by deleting
the external field. This does not reject all UNT, every filter length,
non-equilibrium stars, a different source distribution or arbitrary states.

The bound uses only |F(b)|<=|b|, radial Yukawa positivity and the specified
length, not a retuned a0. In fact, the reviewer strengthened the virial
comparison: for any regular bounded radial solution tending to zero,
|g|<=g_N+S²|g| implies |g|<=g_crit. This retains the upper bound on inward
binding even without assuming g is everywhere outward. It does not imply
a two-sided absolute bound on the anomalous force for a sign-changing g.

The positive critical density kernel
`[1-exp(-sqrt(2)R/ell)]/(8pi ell²R)` fixes the Neumann comparison without a
free homogeneous term. It has infinite total mass and is only a mathematical
upper comparison, not a new physical dark halo in the model.

## How not to overinterpret the length ceiling

A necessary ceiling derived from an upper bound is not a sufficient fit.
A shorter length is not automatically forbidden by the old Solar result,
either: that sufficient contraction and Hessian proof must be reevaluated
at the changed length. Any overlap would only establish compatibility, not
a successful galaxy or joint cosmology. Any resulting universal length
choice would be exposed development calibration, requiring subsequent
fixed-parameter tests. Historical 100-pc successes and failures remain intact.

V001 result SHA256:
`6fe41c1fdb3f971a449ad34ec58adcd9c4fdb062659e174d306f9e55e4e26bd9`.
V002 JSON carries its own source/protocol custody and authenticated parent.

### Next arithmetic, declared before evaluation

To avoid calling the whole length family excluded, evaluate the existing
Solar sufficient input-norm inequality as a FUNCTION of ell, keeping all
its Gaussian, external-field, contraction-ball and response inputs fixed.
Use 160 bisection steps over [.001,100] pc for
epsilon_upper(ell)=(1-LF)r0, with the inherited LF=.6478841742923833 and
r0=.01. Its left side decreases monotonically; this identifies the edge of
that proof's certificate, not a physical lower limit. Report its Q2 bound
and the same Solar quantities at the three necessary dwarf ceilings above.
Do not choose a new ell, rerun science, or declare overlap an observed fit.

The declared arithmetic gives a Solar-certificate edge of
1.402694373659 pc (relative boundary residual -3.33e-16). Its conditional
whole-anomaly Q2 bound is 3.4727358974e-29 s^-2. At the 2.3001623 and
4.2191150 pc dwarf ceilings the Solar self-map still qualifies, with Q2
bounds 8.0906718800e-30 and 1.3537184958e-30 s^-2, respectively. At the
1.3262432 pc ceiling it does not qualify: the solution-norm bound is
.01115152, outside the original .01 ball. That is insufficient proof,
not a failed Solar model. No tolerance or ball was enlarged.

Thus this sufficient Solar interval and necessary dwarf interval overlap
for the two larger declared stellar masses, but not the smallest under this
particular certificate. Neither outcome proves or disproves a fit. There
is no justified new length selection here. Values use GM_sun=1.32712440018e20,
e=2.32e-10 m/s², sigma=1e9 m and pc=648000*149597870700/pi m, retaining the
Solar source's own historical GM convention. The calculation did not import
or execute an old driver.

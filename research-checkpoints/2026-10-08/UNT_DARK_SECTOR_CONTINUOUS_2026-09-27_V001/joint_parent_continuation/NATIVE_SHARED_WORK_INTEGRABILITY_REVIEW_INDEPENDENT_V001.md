# Independent review: shared volume/dipole work integrability

2026-09-30. Reviewer: `urm_dark_integration`, not the note author.
**PASS as a conditional analytic completion test, not physical closure.**
Read the complete final `NATIVE_SHARED_WORK_INTEGRABILITY_V001.md`, SHA-256
`ec4b6e2e8b02a39f567d34617520afc23cde7e7cb4fe44f4b1f5fe5d62a35755`.
No numerical producer was imported, compiled or executed; no physical source,
population, bath, volume law, fit, main ledger or URM record was changed.

## Independent algebra and state conditions

For the same sufficiently differentiable work function at fixed retained
invariants, D=W_alpha and B=-W_eta imply B_alpha=-D_eta and
B_alphaalpha=-partial_eta(W_alphaalpha). Since V is independent of alpha
in this source chart, the latter is precisely the stated pressure identity.
The closed-loop integral is zero on the same single-valued reversible branch;
the two proposed central differences have the correct relative minus sign.
Their indicated second-order remainders require the additional smoothness
and derivative bounds stated for that test, not merely a C3 function.

Three different state operations must remain distinct:

- At a literally fixed density matrix, partial derivatives of Tr(rho H)
  commute and its curvature is the expectation of the microscopic contact.
- On the justified fixed-population adiabatic spectral branch in equation (1),
  state transport produces the static susceptibility contribution. With the
  PLUS acceleration source, the complete work curvature is contact minus chi.
- Fixing an initial preparation and then applying different finite dynamical
  protocols does not identify those protocols with the same reversible
  branch. Contacts, actual state changes and the full two-time response remain.

For a closed unitary system with complete H, d< H >/dt=<partial_t H>.
A closed source loop may consequently perform nonzero work when the final
state differs, without violating energy conservation. The note does not
mistake this stored/dissipated work for failure of microscopic integrability,
nor promote the original left-localized nonstationary states to passive minima.

The final source normalization is explicit: alpha=a_ext and H_alpha=Z.
The dimensionless age-spectrum alpha=gamma0*a_ext instead requires insertion
Z/gamma0 and rescaled derivatives. This clarification prevents a hidden unit
change in the susceptibility/curvature comparison.

## Reflection and relaxed quartic coefficient

The owned apparatus reflection exchanges the two records and carrier
endpoints while leaving Q, C and incidence fixed. H and the volume insertion
are even, while Z is odd. Thus a reflection-invariant state/branch has no
linear odd/even mixing. The original left-carrier preparation is not such a
state; numerical diagonalization alone does not establish exact degeneracy
resolution or the needed physical preparation.

Independently expanding about U'(eta0)=0 and K_eta=U''(eta0)>0 gives

    delta_eta=-K'(eta0)*alpha^2/(2*K_eta)+O(alpha^4).

Substitution of the displacement into U and K*alpha^2/2 gives respectively
+K'^2*alpha^4/(8*K_eta) and -K'^2*alpha^4/(4*K_eta). Their sum is the stated
-K'^2*alpha^4/(8*K_eta), added to L*alpha^4/4. Equivalently, the relaxed
fourth derivative is W_aaaa-3*W_aaeta^2/W_etaeta. The linear curvature is
unchanged in the reflection-invariant case. The positive-definite multivariable
Hessian generalization and the broken-symmetry quadratic curvature correction
-c^2/K_eta are also correct.

This is a local stable static extremization, not proof that an isolated cell
reaches it. The final note explicitly requires an owned equilibration/readout
mechanism. Its frozen-state B example has zero total pressure at its free
stationary point and curvature 12*E_b*exp(3 eta); retaining the isolated
negative-pressure baseline alone would misrepresent that example.

## What this does and does not determine

The finite separable comparator has C=sum(f_j^2/k_j) only because of its
particular source/contact assignment. That cancellation cannot be inferred
from the affine native lapse source or chosen to conceal missing field
contacts. The final note correctly restricts its diagonal kinetic template
and retains any generated momentum, mixed kinetic, connection, cross-quartic
and memory terms. Finite regular stable minimization remains analytic near
zero source; the scalar-volume correction alone supplies no deep |alpha|^3
law. The cited nu(delta) proportional to delta selector is restricted to the
already-derived positive separable soft-window class, not all native models.

The eta derivative concerns a volume variation at the same material/state
invariants. It is not an unrestricted derivative across separately prepared
environments. Physical density requires an independently owned material
loading and calibrated volume; record count, the three Q labels and their
mean do not establish that dictionary. The proposed two-environment test
keeps its preparation and supplied-work differences explicit.

Finally, adding c(eta) leaves the dipole curvature and mixed condition intact
but changes pressure and volume stiffness. The ambiguity survives this test.
One absolute datum can close only the separately restricted constant vacuum
coefficient after other terms are owned, not an arbitrary unknown function.
The B volume assignment is a declared functional postulate, not its independent
physical validation. The note supplies a useful falsifiable cross-observable
constraint and a conditional response template; it does not select the missing
source, physical volume, clock, formation state, source-field equation or
absolute normalization. No scientific promotion or Stage 3 completion follows.

## Source-premise checks

Read the complete operational-source, weak-lapse bridge, autonomous-volume
protocol, age-spectrum interpretation, archive-EOS, soft-selector, fixed-action
constraint and vacuum-identifiability notes; inspected the autonomous producer's
actual native/transport/controller definitions without importing it. Rehashed
load-bearing resident sources:

| Source | SHA-256 |
| --- | --- |
| `NATIVE_OPERATIONAL_SOURCE_CLOCK_VOLUME_CANDIDATES_V001.md` | `fbddff9520f898bf888600ac62a03729d25b7cf4ad230196b04505f81853304b` |
| `NATIVE_ENERGY_DIPOLE_GRAVITY_BRIDGE_V001.md` | `81b3c455d761667e2645117699e8986c7030290de8b54bc45879112237d2db96` |
| `NATIVE_ENERGY_SOURCE_AGE_SPECTRAL_V001_RESULT.md` | `3133247093b1bba7096b5e049d88f88985c7c21401678b58902569359e286075` |
| `NATIVE_ARCHIVE_EOS_AND_SUPPLY_WORK_V001.md` | `0d6710b29bdab7ff820e8c00036f60130096e4c846ad1facc9afdc363ac6ed27` |
| `SOFT_SPECTRUM_ROTATION_SELECTOR.md` | `32535d364266805aceb03ae314882bfe7c0f7f05fe6892bfe6c7e9e434e997ae` |
| `FIXED_ACTION_SUSCEPTIBILITY_CONSTRAINT_V001.md` | `51be129096bcb58641d0788a6a5af9d8e69b10232796e88ba8d1d4cddaa93bbb` |
| `../VACUUM_STRESS_IDENTIFIABILITY_V001.md` | `cf056bab1399963586c45109bda5ebe99d96fba39906019e5723d6046e8e530b` |

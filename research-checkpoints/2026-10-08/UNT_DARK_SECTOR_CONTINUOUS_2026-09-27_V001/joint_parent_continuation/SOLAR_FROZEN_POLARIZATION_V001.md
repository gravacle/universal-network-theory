# Frozen-polarization Solar limit — prospective diagnostic V001

2026-10-04. Selected AFTER the static AQUAL Solar failure. This is a changed
state-response premise, not a blind rescue, not a new adopted universe model,
and not a demonstration that a finite network actually reaches this limit.
The original seven-case AQUAL failure and calibration remain unchanged.

## Question

Can preventing the local polarization from following the Sun even suppress
the problematic quadrupole, once the bounded-source contact is retained?
The existing parent includes temporal response but fixes neither inertia in
seconds nor a spatial polarization stiffness. A positive spatial stiffness
would be new; a moving preferred clock could supply source-frame advection
but its actual frame/state must be specified. Neither is assumed solved here.

Hold the polarization vector at its uniform external equilibrium B_e. Keep
the complete gradient energy E=Kb g²/2-h(g)·B_e+constant and
h(g)=g/sqrt(1+g²/gs²). In units a0, let r=gs/a0 be the EXISTING shape ratio,
e=gext/a0, F=(1+|g|²/r²)^(-1/2), b=B_e/Kb, and bmag=[e-f(e)]/h'(e).
b points along the external potential gradient (opposite external force).

D=g-F b+F³ g(b·g)/r²,       div D=4pi G rho in physical units.

It would be incorrect to set D=g merely because delta B is frozen. The
bounded-source contact remains. Around the uniform external field,

Cperp=1+bmag e F_e³/r²,     Cparallel=1+3 bmag e F_e⁵/r².

The exterior linear Green potential of a unit point source is
-1/[R sqrt(Cperp Cparallel) sqrt(1-u²+(Cperp/Cparallel)u²)].
The diagnostic imposes this outer boundary, and regularity at the inner edge.
It is an elliptic boundary problem with an imposed background state, not a
solution of the missing polarization dynamics or a stationary state of the
original fully relaxed parent. Holding the state must ultimately have a
physical origin and an accounted energy/current history.

## Inputs and controls locked before new result

No new numerical physical parameter: reuse a0=1.0059833281731022e-10,
r=25.51664211557329, Solar GM and external accelerations from AQUAL V001.
Five identical primary grid/domain configurations, same 240-iteration/50s
per-case cap, half-relaxation, update/defect, plateau and refinement gates.
Only after the primary qualifies, run the same two external-field variations.
Reuse the authenticated radial-operator manufactured controls without
rerunning them. New controls before physical cases: zero-polarization Newton
limit; finite differentiation of energy equals D at fixed b (<1e-6 scaled);
external Hessian agrees with Cperp/Cparallel (<1e-6 scaled); constant external
polarization subtraction cancels (<1e-13); positive external eigenvalues.

Every input/source is hashed; all cases retained. Report actual Q2 and the
conditional fixed-mean Cassini residual only if the unchanged primary gates
pass. These are not a marginalized likelihood or an exclusion of all UNT.
No source parameter, length or time is fitted against Cassini.

## Interpretation

If even this limit fails, simple freezing is not a sufficient repair. If it
survives, it establishes ONLY a limiting possibility: a finite, energy-owned
state/clock/spatial-response law must connect solar suppression to the already
successful galaxy regime, with a controlled matching window and its own
predictions. It cannot be declared the solution by naming it a phase change.
Spatial-gradient terms vanish on homogeneous fields and do not by themselves
repair the independently failed shared expansion background. All Stage 3
lanes and the separate thermal-origin CMB requirements remain open.

# Matched hard-reaction attribution control V001

2026-09-29. Prospective analytical design only; no new numerical producer,
physical fit, state selection, source modification or frozen-file edit.

## One intervention, with its inconsistency made measurable

The frozen clamped patch solves the phase relation at every point and retains
both its polarized flux and its gravitating energy/pressure. To isolate the
effect of the latter, keep exactly the same material, common chemical
potential, source spectrum/calibration, gap, box, ordinary sheet, numerical
seeds and boundary data. Define the diagnostic family

    R_lambda[u]=div(D_normalized[u])
                -epsilon/Kb*(deltaT_soft[u]+lambda*deltaT_hard[u]),
    lambda=0 or1,   T=E+3Pi.                                (1)

Only lambda=1 is the adopted clamped equation. Lambda=0 is a deliberately
action-inconsistent removal of the hard contribution from this lapse source,
not a new self-consistent theory, a physical state with no hard energy, or a
valid cosmological completion. Full hard E,Pi,I and the unchanged DeltaU must
still be computed and saved. Calling this a frozen-bulk *source* control
must not imply its material state was fixed to I_b.

At a lambda=0 root u0, the residual of the original equation is exactly

    R_1[u0]=-epsilon*deltaT_hard[u0]/Kb.                     (2)

Its full-model global flux defect is the corresponding negative volume
integral. This is the omitted gravitational source itself, without an
inferred halo or a difference of unrelated calibrated states. Comparing
u1-u0 additionally includes the field's nonlinear feedback into its state;
it is not equal to a linear response to a predetermined hard-density map.

## Derivatives and minimum census

All flux derivatives remain unchanged, including F_Phi and the compulsory
B_I^2/e_II term. Write F=Fsoft+Fhard. The soft ground reaction has no lapse
derivative, and

    deltaT_soft,g=2Fsoft,
    deltaT_hard,Phi=-J,
    deltaT_hard,g=2Fhard-F_Phi.

Thus the residual Jacobian uses the original flux variation plus

    +lambda*epsilon^2*J*delta_u/Kb
    -epsilon/Kb*[2Fsoft+lambda*(2Fhard-F_Phi)]
                                     *n.grad(delta_u).     (3)

Equations (2)-(3) provide direct controls before interpreting any difference.
No tolerance or physical sign is changed to make a branch converge.

A small prospective attribution census can use both inherited gaps, both
boxes, N16 and both original fixed seeds, paired against their authenticated
lambda=1 counterparts. Retain all failures and failed-but-qualified iterates;
they are not equilibrium comparisons. A branch used for a spatial conclusion
needs its N32 comparison as well. This is a suggested follow-up design, not
an assertion that the original eight-case grid census may be shortened or
that a particular branch should be selected. Root owns any final protocol
and sole execution.

A fixed-I_b control would simultaneously change the polarization and the
volume response, so it is not the same single-intervention test. Generally
it also violates N*omega(I,h)=mu and needs an explicitly counted support
force or another phase/state prescription. The exact separate geodesic-clock
branch is a physically consistent alternative of the full action, but it
is not obtained by disabling one source in this aligned static solver.

## Why the next exterior step is different from corner refinement

The mixed clamp corner is already analytically incompatible with global C1
regularity, although bounded weak/interior solutions remain eligible.
Neither increasing a maximum-gradient resolution test nor choosing the
box with a favorable force supplies a physical exterior.

For the same infinite Kuzmin source, a genuinely owned static exterior must
include the sheet outside the finite patch and its same phase/metric state;
it supplies a Dirichlet-to-Neumann relation, not an independently adjustable
zero-potential wall. In a cosmic exterior the aligned linear state is a
Helmholtz-type problem, so a decaying peculiar potential alone need not fix
its homogeneous response. A retarded cosmological initial-value matching,
or another explicitly supplied environment and clock/current condition,
is substantive data. It cannot be replaced by a fitted halo radius.

One may separately declare compatible synthetic boundary data or a smoothly
compact synthetic sheet for numerical analysis, but that is a different
geometry/source test and must be labeled as such. No such change is adopted
here. The immediate control (1) addresses bulk energy attribution within
the existing explicit clamps; it does not purport to repair their exterior.

References: `CLAMPED_COMMON_PHASE_KUZMIN_PATCH_V001.md`,
`CLAMPED_PHASE_EXISTENCE_AND_CONTINUATION_V001.md`,
`MACROSCOPIC_ALPHA_ONE_GALAXY_BVP_V001.md`, and
`VARIABLE_STATE_OUTSKIRTS_RESPONSE_V001.md`. Their original files and all
completed numerical outcomes remain unchanged.

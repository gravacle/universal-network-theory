# Matched unfiltered compact-dwarf control

2026-10-05 UTC. New comparison, not a repetition of the filtered test. Keep
all six declared mass/external-field cases, the profile, a0,r and both proof
balls unchanged. Set only ell=0. This establishes whether the compact-dwarf
tension can properly be attributed specifically to the100pc filter.

The positive Gaussian mixture for a Plummer source gives exactly

    epsilon0=||g_N/e||_A=4GM/(pi a^2 e).

Indeed the unfiltered Gaussian norm is2GM/(pi e sigma^2); with
sigma^2=a^2/(2u), integrate u exp(-u) from0 toinfinity. The fixed-point outer
multiplier is now Pi_L, still of norm1. The response LF bound is unchanged.
Only the outer self-map gate differs. If epsilon0<=(1-LF)r0, the full
nonlinear static branch within that ball is certified, with

    A0=e LF epsilon0/(1-LF),
    sigma_LOS,ap^2 <= [3pi GM/(32a)+2a A0]/F_ap.

The same equilibrium/profile/readout limitations apply. Failed self-map
cases must be marked UNCERTIFIED with no claimed force or velocity bound.
Do not enlarge the ball or change a mass after seeing those outcomes. A
failed certificate is not a failed physical model. Comparing two loose
upper bounds does not rank their actual velocity predictions.

The driver reads the authenticated filtered-result LF values rather than
rerunning that completed calculation. It checks their saved control status,
the mixture first-moment integral within2e-10, and unit identities within
2e-12. Root and handoff_plan_review_v005 independently derived the exact
unfiltered norm and confirmed the unchanged nonlinear proof before execution.

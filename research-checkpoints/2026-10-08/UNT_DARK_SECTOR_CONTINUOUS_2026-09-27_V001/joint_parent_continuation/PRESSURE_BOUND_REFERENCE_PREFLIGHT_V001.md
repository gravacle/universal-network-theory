# Pressure reference V001: independent preflight

2026-09-29. Full source and protocol were read and mathematical acceptance
communicated before the pressure worker ran. No pressure outcome, fit, model
import or numerical worker was used in this preflight. No blocking issue found.

Reviewed source SHA-256:
`dfc71a4c322968dee059dacc4a39618517eafb8ea6366afefdeaf94597c4a054`.
Reviewed protocol SHA-256:
`03a71221388687d0f4c5d3f96d4b6ec63d6fa0ad30ea2856f80be0a22596199e`.

The original producer, nine recorded source identities, two recursive freezes,
shape-result canonical payload, and all eighteen old reference-input mappings
were independently authenticated read-only. The script uses the exact old
diagnostic status, a pinned old result hash, and complete nine-reference ×
two-BBN-alternative census; it retains rather than clips a nonpositive target.

The normalization follows `rho_exc=4M²gstar² E/(1-epsilon²)` against
`rho_crit=3M²H²`: in SI units it gives
`E=(3/4)(1-epsilon²)Omega_exc(cH/gstar_SI)²`. The relaxed calibration
`gstar=3pi*a0/8`, Mpc-in-km Hubble conversion, and finite-cutoff spectral
moment `S4=integral_epsilon^1 s^5 ds=(1-epsilon^6)/6` are correct.

From `E=2V2+3P` and `V2<=sqrt(S4 P)`, the stable positive-root form is
`P_floor=E²/(sqrt(S4+3E)+sqrt(S4))²`. Solving the same inequality for a
proposed `w<=wmax<1/3` gives `E_capacity=4S4*wmax/(1-3wmax)²`.
The implemented inverse, capacity ratios, and sign handling agree. Neither
an inertia nor a redistribution of action can evade this moment inequality
at fixed E, spectrum and rapid zero-source virial premise.

The deterministic synthetic tests cover zero/tiny/large energies, inverse
round trips, nonnegative/upper-pressure inequalities, and distinct saturated
and strict Jensen/Cauchy moment fixtures. They test arithmetic, not physical
attainability of equality. The km/metre Hubble routes are a unit consistency
check, not a new independent calibration. All physical pressure values are
outputs; the numerical gates do not require a favorable pressure.

Additive provenance clarification, without changing frozen source: the old
result's explicit assumptions are “Late-time flat zero-excitation
baryon+dust/vacuum diagnostic; radiation omitted here only.” The required
excitation density is the corresponding reference budget. Its vacuum was
already calibrated cosmologically and its baryon alternatives import standard
BBN. BBN error metadata are retained, but the central-value calculation does
not propagate their uncertainty or define a likelihood. The three wmax values
are illustrative definitions, not observational coldness limits.

This tests the inherited relaxed scale, not every shared-state inference or
UNT. A changed excited-state calibration must recompute the same galaxy and
expansion predictions. A nonadiabatic state is outside this averaged bound
and needs its actual evolving stress. No frozen file was altered.

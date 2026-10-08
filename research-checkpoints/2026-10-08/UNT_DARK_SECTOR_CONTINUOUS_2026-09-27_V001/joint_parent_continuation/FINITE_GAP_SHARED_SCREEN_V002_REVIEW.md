# Independent finite-gap shared-state review — V002

2026-09-29. Accepted within the declared scalar macroscopic screen. This
review read the entire source/protocol before execution and independently
recombined the saved output afterward. No producer, orbit quadrature,
turning-point root, ODE, fit or galaxy field calculation was rerun.

## Custody and complete census

The saved transport decompresses to one complete 352,073-byte canonical JSON
document. Its raw digest, payload digest, freeze digest, transport summary,
all 52 frozen files and 131 nested-manifest member occurrences authenticate.
All four inherited soft quadratures, all 18 reference alternatives and all
five prospectively fixed hard gaps are retained: 360 rows, 72 per gap.
The old 72-row calibration/source result and its wrapper are authenticated.

- Producer source `finite_gap_shared_screen_v002.py`:
  `f8f07a8f1d15725c9c48f04779608899bc79521c0bbfc5983f6d76f4869c0ac6`.
- Protocol `FINITE_GAP_SHARED_SCREEN_PROTOCOL_V001.md`:
  `1bf010add7f1e92fc7f3ded726f0f853f1ba56a566753a303b4ff60c3e87a3e0`.
- V002 freeze:
  `e2d80308d159f7d7b0ec4217e6082c1157eda6cc81000ac4d83c4b6255b989cb`.
- Saved transport:
  `11d5898717488b1ab3fb75e3294e55e5674f2b3f2d623f15cc9bb2e9a54c4db4`.
- Exact decoded raw result:
  `822dd216b33ff4ce08cdcd8b5f1ad5e3e27c583b7833107cef58b158cb3f9cc0`.
- Scientific payload:
  `27b6ae383c0e0d3f1d129981b0e0d38ecb805117d696c4824320931a932a44b9`.

The producer reports 80,076 controls, no failures, maximum normalized error
5.16905e-15, 2.568623208 seconds and 35,323,904 bytes peak self RSS. The RSS
is not a whole-job measurement or hard resource cap. My independent audit
made 10,080 saved-arithmetic comparisons, all passing; its largest normalized
discrepancy is 2.16258e-15. The reproducible stdout-only audit is
`finite_gap_shared_screen_saved_audit_v002.py`, with its output in
`FINITE_GAP_SHARED_SCREEN_V002_SAVED_AUDIT.json`.

## What was independently checked

Each row reconstructs its exposed-a0 gstar, required excitation energy,
finite-vacuum density target, both physical density fractions, action/enthalpy
identity, pressure ratio, positive susceptibility deficit, K0, Jstatic,
cI2, deceleration shift, static length in parsecs and its independent cosmic
normalization. The A=1101 action target, actual saved action, enthalpy,
pressure/energy, cI2 and dust-energy ratio also reconstruct. All reported
ranges exactly match their complete row subsets. No favorable row was selected.

The central identities are

    q=3(e+p)/(R^4+4e), K0=beta*q,
    J=beta*(omega^2/eII+3I*omega), cI2=I*eII/omega,
    K0/J=3cI2/[(R^4+4e)(1+3cI2)],
    ell=(c^2/gstar)*sqrt(K0/J).

These are the occupied scalar phase-equilibrium coefficients; empty soft
modes contribute their contact, not a fictitious occupied omega^2/eII term.
The finite-R endpoint is recalibrated with its own hard elastic energy.
The monotone doubling bracket correctly replaces the invalid finite-R use
of the purely harmonic endpoint upper bound.

Saved mean-square values and individual vacuum roots are not output. Therefore
the virial, cubic, full endpoint integral and elastic-contact numerical checks
remain source-reviewed producer evidence, not independently re-integrated
quantities in this audit. Their published control maxima pass the unchanged
gates. GL64/128 and Simpson1024 are genuinely separate numerical evaluations
in the producer; this review does not claim a third orbit implementation.

## Scientific result, retaining all five gaps

Ranges span all 72 spectrum/reference rows at each gap:

| Hard gap R | Local static length, pc | w at A=1101 | E(A)/(E1 A^3) |
|---:|---:|---:|---:|
| 32 | 959,652–1,057,046 | 0.333306–0.333310 | 95.448–101.859 |
| 128 | 3,766–4,153 | 0.332248–0.332381 | 15.064–16.074 |
| 512 | 14.713–16.222 | 0.293342–0.297840 | 2.5220–2.6720 |
| 2048 | 0.057472–0.063369 | 0.026208–0.031067 | 1.028329–1.034086 |
| 8192 | 0.000224498–0.000247534 | 0.000116535–0.000141661 | 1.00011657–1.00014172 |

This is a concrete shared-state tradeoff, not a separately adjustable cosmic
pressure and galaxy length. The R=128 rows have a kiloparsec local static scale
but nearly radiation-like early pressure; the R=8192 rows are much colder at
the same declared epoch but have a very short local static scale.

Neither statement is an observational pass/fail. Ell is an inverse static
Helmholtz wave number, not a halo radius, dynamical growth rate or selected
matching boundary. Moreover delta I/I=-Phi/cI2 requires |Phi| much smaller
than cI2 for this linear cosmic-state expansion. At R=128 that potential
scale is 2.93145e-6–3.56389e-6; at R=8192 it is
1.74730e-13–2.12428e-13. A nonlinear concentration, finite-field polarization,
or another explicitly specified clock/state branch cannot be ruled out by
extrapolating the linear length beyond that domain.

The candidate is the newly declared zero-soft, scalar hard state with beta=.005,
not an actual finite-R common pulse or a native spectrum. Its action changes
with R to meet the same calibrated energy. Exposed a0 and model-dependent
late-time reference/BBN assumptions remain calibration inputs. Radiation was
omitted in that present-day reference normalization; the A=1101 output is a
conditional same-action history diagnostic, not a recombination likelihood.
The physical clock/adiabatic domain, static boundary/state selection and the
actual galaxy solution remain untested here.

## Precision and preserved attempts

Positive q and pressure are evaluated without subtracting nearly equal large
terms. Thus their tiny values are not obtained as 1-minus-a-rounded-response
or I*omega-minus-e. In contrast, S-S_infinity is explicitly a subtraction of
two rounded root results. At R=8192 its value is only 14–20 ulps of S
(4.97e-14–7.11e-14). Preserve it descriptively; neither the root tolerance nor
this audit establishes high relative precision of that small difference.
The sign/order is supported by the separate analytical endpoint argument,
not a claim that all displayed difference digits are meaningful.

V001's launch stopped at prospective-freeze comparison before run(): a
JavaScript reserialization changed the parsec float's JSON numeric type/value
under Python comparison. Its source, refused freeze and traceback remain in
`FINITE_GAP_SHARED_SCREEN_V001_LAUNCH_FAILURE.md`. The exact V001-to-V002 code
diff changes only the freeze filename; formulas and gates are unchanged.

The first V002 numerical launch then lost its output/session custody through
the host orchestration failure documented in
`FINITE_GAP_SHARED_SCREEN_V002_OUTPUT_RECOVERY.md`. Its scientific outcome is
unavailable, not a claimed success. After a no-worker check, the unchanged
short worker was rerun to capture the retained complete transport. This review
accepts that retained result; it does not describe it as the first numerical
launch or infer results from the lost attempt.

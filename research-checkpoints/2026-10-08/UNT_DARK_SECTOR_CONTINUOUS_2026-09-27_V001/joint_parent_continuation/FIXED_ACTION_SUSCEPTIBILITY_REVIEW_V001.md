# Independent scalar-susceptibility review

2026-09-29. Full analytical and source preflight; no scientific script was
imported or executed by this reviewer.

Reviewed analytical note: `FIXED_ACTION_SUSCEPTIBILITY_CONSTRAINT_V001.md`,
SHA-256 `51be129096bcb58641d0788a6a5af9d8e69b10232796e88ba8d1d4cddaa93bbb`.
Also read the complete `prepared_susceptibility_v001.py` and
`PREPARED_SUSCEPTIBILITY_PROTOCOL_V001.md` before their arithmetic census.
Their reviewed SHA-256 identities are respectively
`dba0ba5d05938b38e7224f5b6359be71b0294b042ce19d4a7de28f0c231c6d12`
and `3cb68b6da4c98672ba0c26456e552a02a6dc17568de11f793897ef845c858d7c`.

## Mathematical finding

Accepted. At zero source, parity makes the fixed-action energy and period even
in the force. Differentiating the positive turning point therefore gives
`xi(0)=1/(k+u b^2)`, not zero. Substituting
`m (y^2)ddot=4e-4k y^2-3u y^4` proves
`xi=(k+u y^2)/(k^2+4u e)` solves the full variational equation and its initial
conditions. The period average is consequently the fixed-action susceptibility.
Its strict deficit at nonzero energy, inertia cancellation, and turning-point
bounds all follow. This is not an RMS-curvature approximation.

Virial averaging gives `e=k<y^2>+3p`, hence exactly
`q=1-k chi=3u(e+p)/(k^2+4u e)`. Coupling and contact normalization then give
the positive-weight mean `mu_linear=sum(w q)/sum(w)`. The finite-band expansion,
ordered-limit distinction and uniformly harmonic small-action expressions
in the note are consistent.

For the dimensionless soft band `k=s^2`, `u=1`, `s<=1`, Jensen gives
`e^2 <= 4s^4 p+6ep-9p^2`, stronger than the inequality needed for `q e<=12p`.
Therefore

    sum(w q) >= sum(w q s^4)
             = 3(E+P)-4 sum(w q e) >= 3(E-15P).

The conservative distribution bound and its pressure qualification are valid.
It is a necessary constraint, not a sharp characterization or an exclusion
of shared excited-state recalibration. It does not apply unchanged to an
added high-gap atom with `s>1`.

## Prospective arithmetic implementation

The script reads all 36 old returned-action rows and their 3,840 mode entries,
checks the exact expected preparation census, and matches gaps/weights to the
corresponding old source case. It authenticates the pinned return and nested
frozen inputs without executing inherited science code. The direct and
alternative susceptibility expressions, exact identities, pressure/contact
bounds and 24 descriptive resolution comparisons match the protocol.

The alternative uses a virial reconstruction from a saved fourth moment and
turning amplitude. The code and protocol correctly do not label it an
independent saved second moment or a new response measurement. Old moment
rounding is retained with its old tolerance, separately from tighter arithmetic
checks. No success threshold is applied to the actual response floor.

No preflight blocker found. This review does not certify as-yet-unrun outputs.
All conclusions remain scalar, fixed-action and phase-averaged. The vector
response tensor, physical state transport and coupled clock/metric evolution
are not supplied by this exact scalar result.

# Independent preflight: shared calibration of the hard-gap limit

2026-09-29. Full read of the source, prospective protocol and corrected
analytical feasibility note. No import, numerical execution, fit or source
edit. **Accepted: no load-bearing scientific or implementation defect found.**

Reviewed identities:

* `global_gap_limit_calibration_v001.py`:
  `7bb8bbd452b68b460720342e0e0b4043096c746ad5a3bfbcba1e30ee1e502e24`.
* `GLOBAL_GAP_LIMIT_CALIBRATION_PROTOCOL_V001.md`:
  `72c7893d1659c3143bdb968157c2f8b0bd74b703e15db4999121afdec6f00e7f`.
* `GLOBAL_HARD_GAP_SHARED_FEASIBILITY_V001.md`:
  `683bf955a6f70b39cb4a247c01c309db0580faae5b8b06acdd742ca9510bb08d`.

## Analytical checks

The rescaled hard pulse has nonlinear coefficient Hp^2/R^4 on a fixed
dimensionless time interval. Its harmonic limiting energy is exactly
beta*pi^2*n^2*Hp^2/8. The stated soft-mode rescaling also has vanishing
energy on that fixed finite band. These are ordered large-R statements,
not a replacement of the six saved finite-R states or a uniform all-epoch
adiabatic theorem.

At fixed physical normalization, the two density conditions give
E=3Kb*Omega_exc*(cH)^2/(2gstar^2) and Qlimit(S)=E*Omega_Lambda/Omega_exc.
The exposed formal acceleration coefficient fixes
gstar=a0/[16Kb/(3pi)]. The positive hard contribution beta*S^2/2 makes the
endpoint root unique and supplies the analytic upper bracket used in code.
No independent abundance or vacuum offset remains in this declared limit.

The positive cubic expression solves delta^2*y+y^3=delta*h and is odd in h.
The independent bisection bracket min(h/delta,(delta*h)^(1/3)) is valid for
positive h. The positive endpoint expression and complete contact obey
Qsoft+Wel=Ws*S^2/2, hence Qlimit+Wel=Kb*S^2/2. This independently verifies
the physical gs identity and its normalization. Since integer n=8 makes
|h| attain Hp at the pulse midpoint, Hp<S is the exact bounded-source
amplitude condition for this pulse family, not merely an envelope estimate.

For the field probes, root stationarity gives
sum(w*y^3/delta)+sum(w*delta*y)=Ws*h. Therefore the implemented positive
expression

    D=G*z*(2+z)/(1+z)^2+hprime*sum(w*y^3/delta)/Kb

is exactly equivalent to G-hprime*(Bsoft+beta*h)/Kb. Its contact term,
sign and physical conversion gN=gstar*D are correct. The finite-quadrature
strict cubic coefficient is positive
2/S^2+sum(w/delta^4)/Kb. The distinct ordered continuum coefficient is
2/S^2-1/(2Kb), with the negative term supplied by the upper cutoff.
The nominal asymptotic window and omitted lower-band bound are retained as
conditional scales, not silently promoted to a certified observational range.

The feasibility note's fixed-energy hard-gap derivative, pressure-history
monotonicity in compression, and finite-epoch dust floor are also correct.
In particular, the large-gap design cannot make calibrated matter-like
energy disappear from the total density budget merely by making it cold.

## Source and scope checks

The code authenticates the stored spectra/references and retains all four
distinct soft quadratures times all18 reference alternatives. Repeated old
duration/step copies are checked for identical nodes/weights, not counted
as new spectra. It preserves nonpositive-domain labels and unrealizable
source branches rather than selecting a favorable row. The endpoint and
modal solvers are independently checked, with fixed prospective tolerances.

The reference acceleration is explicitly already exposed calibration;
the resulting finite-field responses are linked conditional predictions,
not unused observations or disk solutions. Coherent preparation,
isotropic-vector response, finite-R state production and physical clock
qualification remain separate. No scalar response is asserted to be an
isotropic-vector constitutive law. The worker is stdout-only and exits2
on numerical failure. Result acceptance still requires review of the saved
output; this note does not assert that execution has occurred.

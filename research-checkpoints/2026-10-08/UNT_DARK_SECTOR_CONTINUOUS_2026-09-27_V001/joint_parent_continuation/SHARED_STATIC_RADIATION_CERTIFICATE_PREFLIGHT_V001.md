# Shared static/radiation certificate: independent preflight V001

2026-09-29. Full read-only source and protocol review. No import, producer,
orbit quadrature, root solve, or evaluation of scientific output.

Reviewed bytes:

- `shared_static_radiation_certificate_v001.py`, SHA256
  `783a37190e6c7f5f296089d97b01525596365fbc18a9ca03ddb4dc9e09b0aef4`.
- `SHARED_STATIC_RADIATION_CERTIFICATE_PROTOCOL_V001.md`, SHA256
  `cd027e11a9fdd655bc2a064dbdd54ef35aef91091f8bc4c846135c01be207535`.
- Analytical proof `SHARED_STATIC_RADIATION_NECESSITY_V001.md`, SHA256
  `190882b4f19f21756b00212a709bf7983a402f32fae90fb992c5617fd026c970`.

No load-bearing correction requested. Independently checked:

1. The exact turning-amplitude identity and the convex-period chord/Jensen
   frequency bounds, including the rationalized harmonic-mean excess and
   the bound 2(Omega_b^2-1)<=1.5 b^2. The tiny saved frequency subtraction
   is used only for an ordinary-scale consistency control, not occupancy.
2. The algebraic soft-source lower bound follows from y^3<=delta S. Its
   sum, the occupied-source comparison and the small-square conditions
   establish the stated sufficient Tc>=0 certificate without an orbit call.
3. Ecap, the reaction bound, physical calibration and chi-critical formula
   have the correct units and factors. A conservative upper first Bessel
   zero weakens the necessity test in the correct direction. The uniform
   small-domain Ecap gives a conditional, not empirical, gap ceiling.
4. The action-area ellipse bounds and exact Gamma/Beta coefficient have
   the correct normalization. The lower radiation readout at chi-critical
   is a conservative asymptotic same-action coefficient, not a finite-BBN
   abundance or a new observed threshold.
5. All 360 inherited state labels and both extents are retained. The
   recursive manifest, transport, wrapper and payload checks preserve
   ancestry; the producer is stdout-only and imports no former producer.
6. Numerical arithmetic controls, sufficient-input qualification and
   conditional scientific statuses remain separate. A failed sufficient
   input bound is not a proved physical failure; a passed necessity is not
   existence. Every domain statement retains attraction, occupancy,
   ellipticity, weak-metric and prescribed-clamp hypotheses.

The pre-outcome floating-order control adjustment at chi=1e-16 uses the
already specified scaled arithmetic tolerance. It does not change any
physical condition or remove a case. No actual result is certified by
this preflight; root remains the sole executor.

# Independent review: same-action radiation coefficient

2026-09-29. Read-only analytical review of the complete
`SAME_ACTION_RADIATION_ASYMPTOTE_V001.md`, SHA-256
`913160e3e485d3b6ddc64a66a47a0c06c40b6cd350bb8764df5629f848b49002`.
No new orbit, propagation, fit, numerical spectrum or state was generated.

**Accepted within the note's stated conditional action/clock domain. No
load-bearing algebraic defect found.**

## Independently checked

1. For the signed full orbit, `I=(2/pi) integral_0^b sqrt(2m(e-V)) dy`.
   Substitution at `k=0` gives exactly the beta/Gamma coefficient in (1),
   including the factors of two and the powers `u^(1/3)m^(-2/3)` in energy.
   A nonnegative radial-action convention must not replace this saved action.
2. At fixed action, the trial turning point is exactly the pure-quartic `b0`.
   The positive added radicand gives `e0 <= e_k <= e0+k sqrt(e0/u)`.
   The fixed-amplitude action increases with `k`, so `b_k<=b0`. Together
   with the virial identity `e-3p=k<y^2>`, these prove both finite-A
   certificates, including the factor two in the pressure remainder.
   Positive weighted sums give the stated `Q`, `D` and Cauchy bound.
3. At fixed hard-mode energy and weight, `I_R=-R<y^2>/omega` and
   `I omega=e+p`. Thus the exact logarithmic derivative (10) follows and
   approaches `-4/3`, not `-4`, in the cold regime. This section uses the
   saved normalization `m=u=1`, `k=R^2`; it does not assert the same formula
   for an independently varying mass or quartic coefficient.
4. `d ln(e0/e)/d ln I=4/3-(1+w)=1/3-w` proves the monotonic ratio used in
   (11). The cold expansions `f(r)=r/2+O(r^2)` and
   `w=3r/16+O(r^2)` reproduce the coefficient `(8w_c/3)^(1/3)` in (12).
   The exact implicit bound, rather than this expansion, controls a finite
   threshold. Ratios involving `Q`, `E` or `I` assume a nonzero excitation;
   the all-zero state has the trivial zero-energy limit without these ratios.

## Scientific interpretation

The constructive result is an exact, already-owned state consequence:
the present actions fix a radiation-scaling coefficient, rather than leaving
an independent early-radiation amplitude to fit. The finite-gap errors can be
evaluated from positive sums without any new dynamics. All retained soft and
hard modes, numerical resolutions and reference alternatives must remain.

Multiplication by the same present stress calibration correctly yields
`Omega_exc,1 Q/E1` in **present critical-density units**. The six changed pulse
spectra may use the old references only as explicitly conditional
normalizations; their changed contact and matched baseline are not thereby
calibrated. The old late-time flat/radiation-omitted and standard-BBN
assumptions remain assumptions, not new evidence.

The note correctly separates the formal action-scaled asymptote from a
physically qualified early history: isotropic stress, volume/clock ownership
and adiabaticity are still needed. In particular, `H/omega` can grow toward
the past even though the asymptotic coefficient is exact mathematically.
Radiation-like mechanical stress is not by itself photons, a Planck spectrum
or a CMB prediction. These scope qualifications do not weaken the exact
coefficient or its finite-A certificate.

The proposed arithmetic-only application is appropriate. This review does
not pre-approve any future worker implementation or certify its output.

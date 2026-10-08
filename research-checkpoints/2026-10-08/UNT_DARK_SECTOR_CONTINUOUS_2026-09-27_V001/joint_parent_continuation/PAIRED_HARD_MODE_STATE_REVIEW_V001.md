# Independent review: paired hard-mode state

2026-09-29. Analytical review only; no numerical worker, state preparation,
trajectory or frozen-file modification.

Reviewed complete source: `PAIRED_HARD_MODE_STATE_V001.md`, SHA-256
`7461324e5c40de23f796c9e438a9d1cbecd88ffcc9bdb2c21c8e05fd54a38c91`.

**Accepted within its explicitly conditional parent and state assumptions.**

1. The weights beta/2 and the invertible two-copy transformation give exactly
   the displayed kinetic terms and quartic potential
   beta[(p^2+z^2)^2/4+(p dot z)^2]. Differentiation gives both equations (2)
   and the collective polarization B=beta R p. The current opening correctly
   says that the two-copy degeneracy adds a relative degree of freedom; this
   is not a canonical re-expression of the former single-atom state space.
2. At zero common source, p=pdot=0 is exactly invariant and cancels B and
   Bdot while retaining the positive energy (3). Conversely, z=zdot=0 remains
   invariant for every common source history. The original common pulse
   therefore cannot prepare the proposed nonzero antisymmetric state.
3. The exact turning amplitude (4), its fixed-energy expansion, and
   P/E=3E/(8 beta R^4)+O(R^-8) are consistent. The latter uses a straight-line
   small-amplitude orbit, the quartic virial pressure beta<z^4>/4, and
   <z^4>=3b^4/8 at leading harmonic order. A circular or otherwise angular
   orbit is not silently substituted.
4. Eliminating the stationary quadratic collective coordinate p=h/R leaves
   **+beta h^2/2 in the action**, equivalently a -beta h^2/2 ground energy,
   and polarization beta h. This contact cannot be removed by cancellation
   of the antisymmetric coherent polarization. The finite-quartic cross
   terms scale as E h^2/R^4; the collective quartic and kinetic corrections
   scale as beta h^4/R^4 and beta hdot^2/R^2. These estimates require the
   declared fixed amplitudes and slow source/metric rates.
5. Opposite extra sources add +beta R s dot z. At clamped h=0, the bare
   oscillator work is +beta R s dot zdot; including the interaction energy
   changes the external work to -beta R sdot dot z. For expansion the
   additional bare-energy term is -3H beta|zdot|^2 in this invariant sector.
   The resonant harmonic pulse coefficient beta*pi^2*n^2*s_p^2/8 is
   consistent, but this is a newly adopted differential preparation port.

The pair cancels linear polarization, **not** its instantaneous quadratic or
quartic stress. At nonzero common source it is not an origin-antipodal pair:
the collective coordinate responds, and the finite-R orientation-dependent
couplings remain. Phase averaging, isotropic/triad preparation, the physical
clock separation and the full metric/clock constraints still have to be
owned. The note retains these distinctions and makes no native-production,
actual-isotropization or completed cosmological prediction claim.

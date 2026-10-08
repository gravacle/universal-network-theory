# Independent vector-response analytical review

2026-09-29. Full note reviewed before any new numerical implementation.
Accepted: `ISOTROPIC_VECTOR_ORBIT_RESPONSE_V001.md`, SHA-256
`691a7476af57c9f5f55a63f2bad44b274affca82e6b9af6aa16fe3f9884673c4`.
No worker, source alteration or new fitted state was used.

The transverse variational equation and Wronskian have the correct sign and
mass normalization. Direct substitution of `d=b²-y²` into its quarter-orbit
integral gives `R=L(ud/(2K))/K`, including the harmonic limit `R=1/k`.
The regular even solution of `y xi_y-xi=-R` is the stated positive integral.

The half-period transverse monodromy has one known multiplier -1 and unit
determinant, hence both multipliers -1, even in the Jordan case. Its constant
forcing sector therefore has a unique half-periodic particular solution.
This does not eliminate the full-period rotational zero mode, or forbid a
separately prepared angular-momentum/ellipticity mode. The note states those
initial-data qualifications correctly.

The positive representation of `L` proves the quoted increasing/convex
properties and bounds on `L,L'`. They imply the strict finite-excitation
ordering `0<chi_parallel<chi_perp<1/k`. The small-amplitude expansions give
`k chi_parallel=1-3r/2+O(r²)` and `k chi_perp=1-r/2+O(r²)`. Thus the conditional
isotropic second-moment average has a contact deficit 5/9 of the scalar deficit
at leading weak excitation, with exact `0<mu_iso<mu_scalar` for positive
excited weights. The susceptibility calculation changes neither the owned
zero-source energy nor its pressure history.

Finally, the averaged energy and torque signs agree: the response favors
perpendicular axes energetically, while its individual O(F²) torques need
not vanish in an initially isotropic ensemble. The first-order, fixed-neutral-
data result is not an unlimited-time isotropic equilibrium or a scalar
finite-field curve. A numerical check may validate the quadrature/BVP identity;
it cannot supply the missing preparation or orientation dynamics by itself.

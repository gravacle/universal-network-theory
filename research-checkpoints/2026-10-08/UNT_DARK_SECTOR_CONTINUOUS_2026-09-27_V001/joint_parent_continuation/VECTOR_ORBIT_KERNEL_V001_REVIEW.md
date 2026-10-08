# Independent vector-kernel numerical review

2026-09-29. Accepted within the five synthetic, selected half-periodic response
cases. The full source/protocol review was completed after the parent reported
outcomes; it is not claimed as an independent pre-run numerical preflight.
The analytical note had already received independent pre-execution review.

All four frozen files and canonical payload authenticate. Five cases, both
angle rules and ten independent RK4 shootings are retained; all 277 producer
controls passed. Runtime 0.495267 s; peak self RSS 35,258,368 bytes, not total
job memory. Largest normalized ODE check is 2.813e-11 against the unchanged
2e-7 prospective tolerance.

- Result: `d6b061d7900f333a4c35798670077015c76d051077027e96b68ce626206e66e2`
- Freeze: `d19705756ff7146d08116f1c3616bc84715e931be2f97570a79c4b47fc26b18a`
- Payload: `58c36853399e44ec90c43804364f5bd2734697a93d2ecd42e04ec606ca6415cc`

Independent read-only audit passed 504 saved identities. The exact profile
values/derivatives obey the independently evaluated arcsine Wronskian identity
and variational ODE, with maximum residual 3.11e-15. Saved shooting witnesses
preserve energy, half-period reversal of the unforced orbit, periodicity of
the forced response, and angular-momentum antisymmetry. Monodromy trace,
determinants, means, force bounds and isotropic trace normalization agree.
No ODE or quadrature was rerun. Full-mesh checks not present among the nine
saved witnesses remain authenticated producer evidence.

The numerical comparison confirms that transverse response is not the scalar
response. At r=1, `chi_perp=.6644779420` whereas
`chi_parallel=.3705098030`, giving conditional `mu_iso=.4335114377` rather
than scalar `.6294901970`. At r=1e-4, `mu_iso/r=.8332517448` and
`mu_scalar/r=1.4998031491`; their ratio .555574 approaches the independently
derived 5/9. The harmonic r=0 case gives exactly unit susceptibility and
zero deficit; occupied nonlinear cases retain a positive isotropic deficit.

The shooting method retains the anti-periodic rotational homogeneous sector
and solves only the nonsingular half-periodic forced sector. It neither
declares the neutral angular modes absent nor proves that an arbitrary source
switch-on selects this solution. Isotropic trace averaging requires the named
orientation state and does not remove its slow torque, energy, pressure or
preparation requirements. These tests qualify a local comparison-model vector
kernel, not a native microscopic derivation or a gravity/cosmology observation.

Reproducible saved audit: `vector_orbit_kernel_saved_audit_v001.py` and
`VECTOR_ORBIT_KERNEL_V001_AUDIT_DATA.json`.

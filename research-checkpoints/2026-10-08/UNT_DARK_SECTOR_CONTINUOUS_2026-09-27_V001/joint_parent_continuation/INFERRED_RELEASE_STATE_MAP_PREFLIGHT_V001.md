# Inferred release-state map: independent preflight V001

2026-09-29. Full source, protocol and physical-time note read. No producer import, orbit calculation, geometry differentiation, propagation or numerical execution.

Accepted bytes:

- `inferred_release_state_map_v001.py`: `4b065938a7eb417044d9e1e0c6e7ee9e1abb56a9a9f3205583575ce5f5111bf9`.
- `INFERRED_RELEASE_STATE_MAP_PROTOCOL_V001.md`: `9441d98fb6d5e0cf21194439f46a8361bd30306e936251bac359c2c2e658cdf2`.
- `PHYSICAL_TIME_AND_RELEASE_STATE_MAP_V001.md`: `ea619e6600eff77b8dc75a663a083d98b09160385a4c6f883d52a75fb94184a5`.

No load-bearing defect found. The complete 1,340 source states, 1,180 finite and 160 positive-energy dust limits, are mapped to both thicknesses. Eight reusable geometry bases are justified by the explicitly checked background independence of each spectrum's acceleration scale. Original 64 saved coefficient readouts are reconstructed, rather than recomputing their derivatives.

With epsilon=gstar*a/c^2, tdyn=sqrt(a/gstar) and Xi=cI2/epsilon, the velocity scale Xi*a/tdyn^4 equals c^2*cI2*gstar/a^2; the normalized-current scale Xi/tdyn^4 equals c^2*cI2*gstar/a^3. Density and pressure coefficients correctly contain rho_H*(1+w) and c^2*cI2. The source's Green-bound terms and current interval scaling agree with the previously reviewed release certificate, including signs. The exact macro dust limit has zero pressure-current coefficients, not zero density focusing; null sound time means infinity and null oscillator conversion is not an empty mode.

The stress normalization gstar^2/(4*pi*G*Kb) is an energy density; dividing energy/vacuum outputs by c^2 gives mass density, whereas pressure remains in Pa. The source compares both against their actual shared cosmological normalization. Physical oscillator-frequency outputs retain the unresolved multiplicative time coefficient explicitly: they are not calibrated frequencies.

The source authenticates both complete input packets, payload/freeze links and recursive in-project ancestors, then requires exact prospective snapshot equality. It writes stdout only. A result over the descriptive 1 MiB size target is flagged, not truncated. Root must preserve complete output and inspect failure/status fields.

This qualifies a prospective saved-state mapping, not its unexecuted result. Xi ranks pressure transport against one declared synthetic gravitational source; no acceptance threshold, preferred winner, finite-age evolution or native-clock identification follows. Testing the explicitly adopted macroscopic fluid does not require first deriving every microscopic conversion.

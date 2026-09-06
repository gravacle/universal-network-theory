# Blind structural audit of the hydrodynamic pre-screen

This packet pins and attacks the frozen criticality protocol before inspecting
any target spectrum. It checks exact density arithmetic, the owner-once prism,
the analytical one-carrier bands, particle-hole and chiral controls, rational
density-cell intersections, and automatic stop/authorization behavior.

Run:

```text
python3 -B ADVERSARIAL_R_GATE_C_HYDRO_CRITICALITY_PROTOCOL_V001/verify_protocol.py
```

Physical graph and configuration work stops at L8. L10/L12 names occur only
in rational bookkeeping and synthetic gate-state fixtures; no larger graph,
Hamiltonian, spectrum, or response is constructed.

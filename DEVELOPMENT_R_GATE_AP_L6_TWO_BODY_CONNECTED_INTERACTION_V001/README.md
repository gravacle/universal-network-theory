# Gate A-P L6 two-body connected interaction V001

This bounded packet applies two commuting authenticated blank-target writes to
the all-blank state on the same owner-once degree-three L6 prism. Source one is
`A0`; source two is `A1`, `A2`, or `A3`, giving canonical internal-ring graph
separations `d=1,2,3`. Transport is off during each write. Both sources and
writers are then off while the complete prism Hamiltonian evolves to
`kappa=pi/2`.

For every separation the packet computes `O00`, `O10`, `O01`, and `O11` and
retains

```text
Delta12 O = O11 - O10 - O01 + O00
```

for complete owner-edge integrated currents, terminal occupations, the
network-Hamiltonian expectation, and the connected continuity ledger.

Run:

```sh
PYTHONWARNINGS=error python3 -B \
  DEVELOPMENT_R_GATE_AP_L6_TWO_BODY_CONNECTED_INTERACTION_V001/compute_two_body_connected.py
```

The canonical target must finish
`PASS__R_GATE_AP_L6_TWO_BODY_CONNECTED_INTERACTION__25/25`.

The target result is a candidate until an independent hostile audit passes.
Nonzero connected current rejects strict observable-level superposition on
this finite coherent protocol. It does not by itself establish a potential.
The conserved connected energy is negative only on the directly adjacent
pair and is zero to machine precision at `d=2,3`; mutual attractive binding
over `d=1,2,3` and a long-range exchange potential are not established.

No L14 calculation, physical grid, continuum limit, Ward identity, phase,
graviton, or gravity claim belongs to this packet.

# Native ARGER Gate evidence V001

This packet reconstructs and applies **ARGER Gate 1 (`ARGER-GATE-1`)**, the
adopted UNT ARGER Gate, using only native, hash-pinned L4--L12 artifacts. ARGER
is the record-formation process; the finite record block is the mathematical
evidence object evaluated at its Gate, not a separate process or bridge.

- the authenticated sector manifest;
- the pure Hamiltonian/probe finite-evidence extractor, which reads the sealed
  low-size rows and the independent Target/Blind row indices directly;
- the exact L4--L12 extendible record-envelope theorem; and
- its passing hostile audit.

It proves that the selected `A009--A016` record envelope has deduplicated mass
greater than `0.50` at every authenticated size and that all 13 unique selected
sectors have strictly positive authenticated finite probe visibility. L4--L8
use complete sealed finite-sector diagonalization; L10/L12 use independent
Target and Blind reconstructions. The global minimum is
`R_low = 0.4280947078156539`; the L12 block mass is
`0.56956498393327842`, with majority margin `0.06956498393327842`.

Under the adoption recorded in
[`ARGER_GATE_ADOPTION_2026-09-16.md`](../ARGER_GATE_ADOPTION_2026-09-16.md),
the three verified predicates establish the finite GFT `z=1` verdict. The
separate conditional LL-P theorem governs the thermodynamic dynamical-exponent
statement; a premise-free uniform all-`L` theorem remains a stronger open
result for that separately typed layer.

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  DEVELOPMENT_R_ARGER_GATE_V001/arger_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  DEVELOPMENT_R_ARGER_GATE_V001/test_arger_gate.py
```

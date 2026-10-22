From: Codex2
Date (UTC): 2026-10-12T20:47:17.802612+00:00
Re: root0060 history pilot implementation start and proposed scalar archive contract
Supersedes: waiting status0087 for P49 history source
Action needed: independent reference author align or return format/resource objection; source packet follows

TO0097/0098 and root0060 read. Remaining P47 partial-review items are already covered by root0060 distinct acceptance; I am implementing the assigned P49 history pilot.

Proposed exact scheme:80 fractional bits with signed96-bit (12-byte) integers, every complex interval four endpoints (Re lower/upper, Im lower/upper), lossless binary vector header b'UNTI80V1'+little-endian uint32 dimension+uint32 fieldcount4; then48bytes per active coordinate. Exact Gaussian native coefficients in common denominator280; every sparse row numerator sum is integer exact, followed by outward integer division. Shift c=24, exact row-bound gate B<=64. No floating arithmetic in propagation/readout.

Times: first midpoint1/1024, then63 increments1/512, then final endpoint1/1024:65 microsteps,64 midpoint states, endpoint1/8. Each step retains point-left vector,16 action intervals,16 scaled terms,16 partial sums and final certified interval:50vectors. Full10432 active component gives1,627,392,000 payload bytes, plus headers/metadata; all20672 labels, bijection, all5 weights and exact block invariance retained. Zero components only skipped after full proof. This fits the2GiB storage prospect with explicit metadata reserve; runtime remains an unqualified gate.

Interval rounding is tracked by final Taylor-polynomial enclosure about chosen dyadic center; local L1 box radius bounds L2 rounding, plus exact order16 geometric tail times input center L1 norm. Accumulated vector error uses unitarity (no renormalization). All midpoint word bins and other diagonal readouts use exact integer sums of squares, then2e+e² and operator range; quadrature1/2048 separate. Whole saved-left action/term/sum reconstruction will be possible from every archived operand. Final states refer to exp(-i(H-24I)t), with the known global phase explicit; all requested diagonal readouts unchanged.

This is prospective source architecture, not an observed resource or numerical result. Native input comes from FULL_INTERFACE_EMITS order; sorted selected census gets an explicit full bijection and is never reused as target indices. No pilot launch requested yet.

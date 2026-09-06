# Same-slice L14 finite feasibility screen

## 1. Exact finite structural count

Keep the audited connected component family and set `L=14`, so a component
has 28 binary record sites and 42 owner-once edges. The inherited
source-preserving finite relabeling group has order 28. Direct permutation
checks show that all 28 elements are distinct, preserve the supplied support,
preserve original site parity, and reconstruct the 42 oriented edges from two
consistent signed edge orbits.

For a permutation with `c` cycles on the 28 sites, exactly `2^c` binary words
are fixed. The complete group cycle census is:

| cycles | cycle lengths | multiplicity | fixed words per element |
|---:|---|---:|---:|
| 2 | `14,14` | 6 | 4 |
| 4 | `7,7,7,7` | 6 | 16 |
| 14 | fourteen 2-cycles | 8 | 16,384 |
| 16 | four fixed sites and twelve 2-cycles | 7 | 65,536 |
| 28 | twenty-eight fixed sites | 1 | 268,435,456 |

Burnside's lemma therefore gives the exact finite word-orbit count

\[
 \frac{6(4)+6(16)+8(16384)+7(65536)+268435456}{28}
 = 9{,}608{,}050.                                      \tag{L14-FS-01}
\]

No word-space enumeration or asymptotic assumption enters this count.

## 2. Conditional fixed-width payload ceiling

Consider a phased implementation with a signed 32-bit full-word orbit map,
unsigned 32-bit representatives, byte-sized orbit sizes, 64-bit CSR row
offsets, 32-bit transition destinations, and 64-bit coefficients. Each orbit
representative can produce no more than one unaggregated transition for each
of the 42 owner-once edges, so the transition ceiling is exactly
`9,608,050 * 42 = 403,538,100` entries. Keeping two full raw current kernels,
six complex128 work vectors, and a 64 MiB streaming allowance gives the listed
numeric-array ceiling `11,325,552,642` bytes = `10.5477428455 GiB`.

This byte arithmetic is exact conditional on that layout. It is not a bound
on interpreter objects, allocator overhead, compiled code, or total process
RSS. The `37.4522571545 GiB` difference from the declared 48 GiB capacity is
therefore headroom in raw payload arithmetic only, not a memory guarantee.
The current L12 Python-list construction is not licensed for direct scaling;
an L14 trial must avoid object lists proportional to the transition count,
allocate in phases, log live RSS/runtime, and abort below host capacity.

## 3. Relation to the sealed L12 observation

The sealed L12 run observed `321.367049417 s` and `2.23431396484375 GiB` RSS
on the declared 48 GiB host. L14 has 16 times the full word count and
`13.6406292148` times the exact orbit count. Those ratios are recorded only to
describe the finite inputs. They are not used to extrapolate L14 runtime or
RSS and establish no complexity or scaling law.

## 4. Decision and claim classes

**Decision:** the fixed-width numeric-payload necessary condition passes, so
a guarded same-slice implementation trial is eligible. This is not an L14
accumulation result and does not certify that the trial will fit or finish.

**Proved:** the finite group/support/source-parity identities, cycle census,
Burnside orbit count, transition ceiling, and conditional array byte
arithmetic.

**Adopted:** inherited F3-MDC `alpha=r0` and the same connected component
family.

**Conditional:** source, support, `kappa`, content, routing, clock, read, and
the candidate implementation layout.

**Empirical:** only the sealed single-host L12 runtime and RSS observation.

**Open:** L14 construction, process RSS, runtime, evolution, currents,
retained record, and record-ledger residual.

No physical grid, continuum behavior, Ward identity, generic or critical
phase, graviton, or gravity is inserted or inferred. No monotonicity,
convergence, limiting value, fit, exponent, scaling law, or complexity law is
claimed.

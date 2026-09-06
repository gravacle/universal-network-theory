# Hostile audit report — localized-source response protocol V001

## Verdict

**PASS at finite protocol scope, with no response result.** The pinned target
passes `20/20`; the independent reconstruction passes `35/35`. No target
correction was required. The packet is eligible as the execution protocol for
a bounded localized authenticated-write calculation. It does not close Gate
A-P and does not authorize any response value before the stated numerical and
hostile-audit gates pass.

The target packet hashes are:

- protocol: `df80a38b3902120902012ab46be9dee1854cf25b7113641227b0fdc5a9b2c8a5`;
- README: `8853f9193b98a19f66aad6ed7caad898e9eb032d8b672fbb4cbc7a2c63cfd07a`;
- result: `315efc89e91ccb2816787716f7a724e76f292a9a689a11f80f18f4dd337deb90`;
- verifier: `6a51d2ea0f559e7ad373e125529df972b58b85b8d84dad4144d486ee4c202aa7`.

## Source-to-parent attachment

The audited parent preparation acts on pair basis
`|BB>,|Bx>,|xB>,|xx>`. Its F3-MDC write gives

\[
 (|BB\rangle-i|xB\rangle)/\sqrt2,
\]

and its native transfer maps `|xB>` to `i|Bx>`. The prepared parent pair is
therefore

\[
 |B\rangle_{\rm even\ tail}\otimes
 (|B\rangle+|x\rangle)_{\rm odd\ head}/\sqrt2.
\]

Thus the selected even tail is exactly blank after the parent preparation.
The protocol's local intervention writes that same authenticated retained
target type, producing `(|B>-i|x>)/sqrt(2)` there. A second tail-to-head
transfer is neither required nor silently omitted: this intervention retains
the new record on the even tail and then restores the connected transport
Hamiltonian. Its exact source slice is

\[
 \Delta Q+\sum_eJ_e-W_R=1/2+0-1/2=0.
\]

The writer and source are off during subsequent transport, as required by the
audited parent.

## Differential owner-once ledger

Subtracting baseline continuity from perturbed continuity uses
`Delta q_before=(1/2)e_s`. It gives

\[
 \Delta q^{\rm after}+B\Delta J-	frac12e_s
 =r_{\rm num}^{\rm differential}.
\]

Every owner-once incidence column has one `+1` and one `-1`, so its column sum
is zero. The exact number-conserving hopping parent therefore gives the global
response `sum Delta q=1/2`, subject only to the separately controlled raw
numerical remainder. That remainder stays unassigned and is not called a
defect. Complete signed edge differences remain primary; direct differences
of absolute throughputs are separately defined summaries.

## Independent symmetry and support reconstruction

The audit generated the support symmetry group by closure of a compatible
rotation and reflection rather than using the target's formula enumeration.
The marked vertex has an orbit of size `L`, so a one-site insertion is not
invariant under the full group and cannot be represented by the old full
invariant basis. Its stabilizer has order two. The stabilizer elements have
`2L` and `L+2` cycles, yielding

\[
 \dim {\cal H}_{\rm marked}
 ={2^{2L}+2^{L+2}\over2}.
\]

| L | full invariant dimension | marked dimension |
|---:|---:|---:|
| 6 | 430 | 2,176 |
| 8 | 4,435 | 33,280 |
| 10 | 53,764 | 526,336 |
| 12 | 704,370 | 8,396,800 |
| 14 | 9,608,050 | 134,250,496 |

An independent graph build gives `3L` owner-once edges, degree three at every
site, full connectivity, and support-graph radii `4,5,6,7,8` for
`L=6,8,10,12,14`. BFS reconstruction of every internal/connector shell agrees
with the target under `r_e=min(d(s,u),d(s,v))`. These are finite support-graph
distances only. Periodic return is not a physical boundary reflection.

## Execution and claim ceiling

The protocol requires sealed-baseline reproduction at every size, full-space
L6/L8 validation of complete occupation and current vectors, a marked-source
or equivalent noninvariant engine, independent coarse/fine evolution and
current quadrature, complete signed vectors beside radial bins, a separate
memory screen at every larger size, and a new hostile audit before promotion.
L14 is explicitly not forced.

The L4--L14 background numbers remain empirical finite-window records, not an
asymptotic or invariant plateau. No perturbed response data or profile
classification exists yet. All localized response values, physical distance,
global response owners, lawful quotient, and Gate A-P remain open. No scaling
law, physical grid, continuum behavior, Ward identity, phase, graviton,
gravity, `C_R`, or `G` is inserted or inferred.

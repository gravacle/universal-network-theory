# Connected subdivision: result and next physical discriminator

2026-09-29. Summary of the sealed 528-state result, not a new propagation.
The author implemented the worker and performed this saved-output analysis;
the separate audit lane supplies independent result qualification.

## Result

**The declared autonomous port can enlarge an already-connected blank-register
network while retaining its connectedness with high probability and paying the
full native/source/elastic energy cost from a finite supply.** The native
incidence flips were left active, including flips out of port eligibility.
The same calculation also shows reverse flow: this is reversible connected
transfer, not a demonstrated irreversible expansion process.

All 56 frozen input/strength/time rows were retained. All 608 checks passed;
the maximum eigenvector-versus-independent-Taylor state error was
3.76251e-14, and the maximum absolute total-energy error was 1.63425e-13 in
the declared native energy units. Execution took 4.15910 seconds with
96,976,896 bytes peak process RSS. These are process measurements, not a
guaranteed runtime or job-wide hard cap.

The construction is an **explicitly added, clamped, blank-register port**.
It is not spontaneous growth proved from native record formation, and the
created vertices have not thereby been identified with physical volume.
No comparison to the earlier blank N=1 to N=2 experiment is made: its
map, initial graph, size, source, supply and coupling conditions differ.

## 1. Complete eligible/ineligible comparison

All inputs start in the N=2 sector with the finite supply excited. The cycle
is |15>, the connected tree is |7>, the coherent input is the real
(|15>+|7>)/sqrt(2), and the empty graph is |0>. The first three initially
have an occupied anchor; the last does not.

At each strength's **prospectively specified** swap time, not a time chosen
from the resulting trajectory:

| Port strength; time | Input | P(N=3) | P(N=3 AND connected) | P(exact reversible image Q) |
|---|---|---:|---:|---:|
| 1; pi/2 | Cycle | .989950 | .988924 | .976174 |
| 1; pi/2 | Tree | .989593 | .974098 | .974906 |
| 1; pi/2 | Coherent | .989316 | .980299 | .974564 |
| 1; pi/2 | Empty | .104025 | .000212259 | .098962 |
| 8; pi/16 | Cycle | .996086 | .995888 | .987154 |
| 8; pi/16 | Tree | .996081 | .978854 | .986920 |
| 8; pi/16 | Coherent | .996104 | .986770 | .987057 |
| 8; pi/16 | Empty | .00386337 | .000000681 | .00385081 |

These are unconditional joint probabilities; connectedness has not been
renormalized after selecting a successful transfer. Q is a different event
from connectedness: it requires the complete prescribed incidence pattern,
while a connected graph with extra links can lie outside Q. Conversely Q
can contain a subdivided disconnected old graph. Therefore its probability
need not equal or bound the connected-target probability in either direction.

The operator census verified all eight eligible old basis graphs. Subdivision
increases their vertex and edge counts by two, preserving component count
(including isolated vertices) and cycle rank. In particular the four-cycle
becomes a six-cycle, and the three-edge trees become five-edge trees.
It does not join previously separate old components.

At epsilon=0, N=3 probability is zero at every declared time for all inputs.
Native flips still change graph properties. At t=2 the total connected
probabilities are .997388 (cycle), .920092 (tree), .948786 (coherent), and
.000891752 (empty). Thus the port's success is not a frozen-incidence trick,
and ports-off native dynamics is not itself node creation.

The empty graph is not artificially vetoed for the whole run. Its initial
quadratic transfer coefficient is zero, but native anchor flips can create
eligibility later. At epsilon=1,t=2 its target probability is .113902 while
its joint target-and-connected probability is only .000120692. At
epsilon=8,t=2 these are .00951570 and .00127973. The port can enlarge a
disconnected graph without solving its connectivity problem.

## 2. Transfer is reversible, and the complete trajectories matter

The common t=2 readout makes clear that a faster swap is not a permanent
growth guarantee:

| Input | P(N=3), epsilon=0 | P(N=3), epsilon=1 | P(N=3), epsilon=8 |
|---|---:|---:|---:|
| Cycle | 0 | .832298 | .217246 |
| Tree | 0 | .838385 | .377710 |
| Coherent | 0 | .835161 | .309215 |
| Empty | 0 | .113902 | .00951570 |

For the cycle at epsilon=1, the creation current is +.906803 at t=1 and
-.701909 at t=2. At epsilon=8 it is -5.961826 at t=.25 and +4.811294 at
t=2. The sign is the signed derivative of mean size, not a probability.
Both directions are present under the same time-independent Hamiltonian.
No collapse, deletion, irreversible pump or postselected normalization was
inserted to maintain the first transfer.

The finite-time backbone inequality (candidate Eq.14) passed wherever its
initial-support premise holds. It was not applied to the empty input.
The strong-port bound (Eq.15) gives a minimum exact-Q probability .933181
at epsilon=8, satisfied by all three eligible inputs. Its epsilon=1 lower
bound is zero: the observed high transfer there is a result, not a stronger
state-uniform theorem inferred from this small census. Leaving Q need not
lose the connected backbone; these diagnostics remain separate.

## 3. Supply and source response are part of the result

The native cycle's instantaneous ideal inclusion cost is 10; the insertion
jump contributes -.2; the clamped elastic cost is +1.8. The supply gap
11.6 was fixed from those operator constants before propagation. Actual
evolving states retain native coherence and interaction energy, so their
component ledger cannot be replaced by the ideal basis-state cost alone.

For the cycle, signed energy changes at the two declared swap times are:

| Component | epsilon=1, t=pi/2 | epsilon=8, t=pi/16 |
|---|---:|---:|
| Native incidence | +9.800581562 | +9.918364736 |
| Source insertion | -.190831503 | -.196967533 |
| Elastic controller | +1.781910306 | +1.792955564 |
| Supply | -11.483421970 | -11.554602524 |
| Port interaction | +.091761606 | +.040249756 |
| Total change | zero to numerical tolerance | zero to numerical tolerance |

In every row, the supply change is -11.6 P(N=3), the elastic change is
1.8 P(N=3), and the source change is -.1 times the change in incidence
count. The rest belongs to native and interaction energy. Their sum is
conserved. No external time-dependent drive or omitted switch-off operation
is credited with the transfer; a later readout/decoupling protocol would
need its own work if performed.

Because B counts links and subdivision adds two, the exact response moment is

    <[B,[H_total,B]]>
      = <direct_sum_N [(1/N) sum X_e]> - 4 <H_interaction>.

This differs from the source-preserving blank-inclusion sum rule. The extra
term was verified as an operator identity and retained in every readout.
For example, epsilon=8, tree, t=2 has interaction energy -1.313626075,
so its port contribution is +5.254504299, while the native flip contribution
is -.271577981; the complete saved response is +4.982926318. Dropping the
port would even change its sign. At preparation the coherent input already
has native response .5, whereas the three basis inputs have zero response.
This concerns native incidence coherence in a blank-record experiment,
not the production or persistence of records.

## 4. The next science is an operational ruler test

The connected-growth algebra now has a small exact realization. Repeating
arbitrary supply/coupling choices is not the highest-leverage next step.
The next question is **what a fixed physical probe says changed**.

Use the independently derived local scalar-probe action in
`SUBDIVISION_OPERATIONAL_RULER_V001.md`, with independently owned link
stiffness, node inertia and clock standard. A single old edge versus its
three-segment subdivision suffices. Hold the source/readout and clock fixed
and compare the two-channel boundary response, not node count alone:

- With unchanged segment stiffness c, static endpoint stiffness is c/3.
- With stiffness 3c, static endpoint stiffness is c, but the two new
  positive inertias mu add mu[[5,4],[4,5]]/9 to the low-frequency response
  and leave observable internal poles at omega^2=c_s/mu and 3c_s/mu.
- A genuine representation refinement additionally repartitions kinetic
  measure and boundary masses. It is not achieved by static matching alone.

Thus the minimal next implementation is **one calibrated weak-probe boundary
response comparison**, including probe preparation/work and the same clock
ratio. The discriminants are static stiffness, the dynamic pole/low-frequency
inertia response, and their dimensionless ratios to the unchanged standard.
Those quantities distinguish added physical route length from bookkeeping
refinement without a galaxy fit. The probe is still an adopted operational
completion; matching it to a native propagating observable is the Stage1
physical-binding task. Only after that binding can its measured scale change
be used honestly in Stage2 distance, cosmological volume or redshift equations.
No three-dimensional metric, H(a), irreversible expansion rate or gravity
normalization is inferred from this successful transfer alone.

## Saved identities

- Result: `CONNECTED_SUBDIVISION_V001_RESULTS.json`, outer SHA-256
  `5257b5403af280a868b848f2831677c2426dc8fbbee21d95812dcd7b4da0d5d0`.
- Canonical payload SHA-256:
  `f5e4892715ce55613fd11d6dce2e9bd695d62fa2979fd02e5c814c7dc9d27149`.
- Frozen-input SHA-256:
  `6d0fea9e39623f48e1381dfdd66e4e9bb891ec731ab1e80a2eb4fb252e75a6ec`.

The saved JSON is the full census; the tables above are labeled summaries,
not filtered evidence. This note used read-only JSON arithmetic and no new
propagation. Frozen code, protocol, analytical candidate and earlier evidence
were not changed.

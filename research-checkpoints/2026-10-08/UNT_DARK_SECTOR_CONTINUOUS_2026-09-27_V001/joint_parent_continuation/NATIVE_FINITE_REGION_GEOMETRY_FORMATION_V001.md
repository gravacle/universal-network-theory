# Finite supplied geometry under a paid record and fragment protocol

2026-10-03 UTC. Prospective finite experiment, not a native law adoption.
The mobile-ground calculation did not establish binding or connected-state
selection. This test asks a different concrete question: can one explicit
finite formation/resource protocol change the retention or repair of a
supplied connected geometry, beyond simply increasing the link count?
It keeps the carrier mobile, all nine potential links dynamical, two used
fragments, and every switching-energy term. No outcome is assumed favorable.

This is not another ground-state substitution or a search for a favorable
late age. It tests a finite driven alternative over one fixed complete window.
It does not instantiate an autonomous infinite reservoir or establish that
the universe uses the supplied graph, resource state or timing choices.

## Exact state and declared boundary choices

Use native N=3 with vertices (L0,L1,L2,R0,R1,R2)=(0,1,2,3,4,5) and edge
index e=3i+j for (Li,Rj). All nine incidence bits remain dynamical. One
same-content hard-core carrier starts at vertex0. Only vertex0 has active
copy ports, a fixed occupied same-content writer, one initially blank record
r, and two independently blank fragments b1,b2. All other record, writer and
fragment targets are blank and their copy couplings are off. This selective
activation is a DECLARED port choice; globally active carrier copying would
leave this restricted support and is not silently projected away.

The exact retained state shape is (512,6,2,2,2), dimension24576. Compare:

- Connected six-node path: mask115, edges (0,3),(0,4),(1,4),(1,5),(2,3).
- Disconnected C4 plus edge: mask283, edges (0,3),(0,4),(1,3),(1,4),(2,5).

Both have five edges, labelled degrees (2,2,1) on each layer, and identical
incident links and neighbour degrees at vertex0. Environments farther out
differ. This is a comparison of two owned preparations, not isolation of
global topology from every local geometric difference. Preparation of either
graph is an input, not claimed produced from blank by this experiment.

Keep Delta=4, Ud=d*=Omega=epsilon_psi=epsilon_r=1, h=Omega/N=1/3,
t=1/2, j=lambda_J=1/4, lambda_R=1/2, epsilon_w=0. The two fragment gaps
epsilon_b1=epsilon_b2=1 and local copy coefficients g_wr=g_psi_r=1 are openly
proposed native-unit inputs. They are not measured SI calibrations or fitted
galaxy parameters. Compare fragment coupling lambda=1 with lambda=0 for
each initial graph, giving exactly four histories.

## Hamiltonian and finite supply rule

For the single carrier let P0 denote its occupation at vertex0 and let
d_v=sum_(e incident v)n_e. Retain

\[
H_{\rm native}=-\frac13\sum_eX_e+4\sum_en_e
 +\sum_v(d_v-1)^2+I+\frac14\sum_e n_e(P_u+P_v)
 -\frac12\sum_e n_e T_e+r-\frac12r d_0,
\quad H_b=b_1+b_2.
\]

The native single-carrier transfer T is Hermitian. There is no extra factor
of two or fermionic sign. All constants and the record-feedback term stay.
Use protocol time x=tau/hbar in the inherited generator units. Define
V_r=(1+P0)X_r and V_bj=lambda*r*X_bj. The fixed piecewise generator is

\[
H(x)=H_{\rm native}+H_b+
\begin{cases}
V_r+V_{b1},&0\le x<1,\\
V_r+V_{b2},&1\le x<2,\\
0,&2\le x\le4.
\end{cases}
\]

No fragment is reset, discarded, reused or postselected. b2 is prepared at
the start and evolves freely until its pulse. b1 stays in the full state
after its port is removed. Exact decoupling prevents later occupation/energy
return from a used fragment; this is enforced by the paid switching rule,
not a derived autonomous outgoing boundary. The native schedule, switching
controller and incoming blank supply remain disclosed physical assumptions.

## Energy and analytical controls fixed before execution

All four histories start at complete energy25.5, including current-square
energy, with variance11/2 for the initial pulse Hamiltonian. Initial copy
switch-on mean work is zero. That does not mean preparation or entropy
resources were free. At the two later switches,

\[
W_1=\langle V_{b2}-V_{b1}\rangle_{1^-},\qquad
W_2=-\langle V_r+V_{b2}\rangle_{2^-}.
\]

The newly connected b2 term has zero expectation at 1 because it is still
blank and independent. After every switch check the inclusive identity
E_total(x)-25.5=W_accumulated; before switch-off E_total includes all active
interactions, not just storage. During hold,
Delta E_native+Delta E_b=W_1+W_2. Exciting a fragment is not automatically
cooling: switching work and the change in native energy decide that question.

With x=tau/hbar, exact initial controls are

| Readout | Initial path | Initial disconnected graph |
| --- | --- | --- |
| Probability of a connected six-node graph | 1-5h^2*x^2+O(x^4) | 4h^2*x^2+O(x^4) |
| Connected AND exactly five edges | 1-9h^2*x^2+O(x^4) | 16h^4*x^4+O(x^6) |

Five bridge deletions explain the first path coefficient. Four cross-component
edge additions connect the disconnected preparation. Four possible cycle
deletions followed by four cross-component additions give the sixteen
five-edge reconnections. The latter is an unnormalized probability, not
conditioning or projection of the evolving state. Record onset is 4x^2;
first-fragment onset is lambda^2*x^4. b2 stays exactly blank before1. Its
later onset is generally quadratic with coefficient lambda^2*expectation(r)
at1, not another blank-record quartic law. Used fragment occupations are
constant after their ports are removed; r is also conserved after2.

Root and independent source-only preflight checked these identities. They
are analytical controls, not a reason to run another onset-only series.

## Readouts and numerical scope

Report the entire mesh x=0,1/16,...4, with left/right boundary records at1
and2. For each history retain connected probability, unnormalized connected
five-edge weight, link count, all six carrier probabilities, record occupation
and explicitly defined complex record coherence, both fragment occupations,
native energy, fragment energy, active copy energy and accumulated work.
Also retain norm and numerical error diagnostics. Coherence is a diagnostic;
no whole-window monotone physical record clock is assumed. These protocol
units are not a derived cosmological age or a replacement physical clock.

Compare fragment-on minus fragment-off for each original graph at every
reported time. Report sign changes and endpoint values without selecting a
passing age. A sampled whole-window minimum is not a continuous-window
certificate. No arbitrary connectivity threshold is a scientific pass gate.
Any positive retention must be reported alongside extra supplied/switch work,
transport changes and whether it persists after all copies are off.

Use the existing NumPy runtime and matrix-free action, never a24576-square
matrix, eigensolve or new dependency. Center by35I only inside numerical
propagation while retaining the complete physical energy. The diagonal is
bounded by [6.5,64.75]; maximum off-diagonal row sums are7.5 in a pulse and
4.5 in hold. Thus ||H_pulse-35I||<=37.25 and ||H_hold-35I||<=34.25.
Choose substeps solely from these bounds, maximum scaled norm0.75 and
Taylor tail1e-19 as in the existing propagator. Retain an accumulated
analytic truncation bound separately from the inherited assigned1e-10
arithmetic checks; no certified floating-point interval is claimed.

Check matrix-free Hermiticity by independent deterministic probes, full
component reconstruction, initial energy/variance, exact conserved readouts
and inclusive energy at every switch. Do not normalize states to hide drift.
Fix a120-second,256-MiB working resource ceiling before running and monitor
the actual root-owned worker; if exceeded, checkpoint/stop that known worker
and preserve partial evidence. One numerical worker only, source-only agents.

The next action is to read the specific authored worker in full, verify the
protocol binding and no live worker, then execute once if it meets these
constraints. A larger graph, parameter scan, autonomous bath or independently
fitted density history is not authorized by this finite protocol. Physical
source/ruler/volume, actual universe formation and all Stage3 tests remain open.

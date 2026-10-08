# Source, controller and creation: completed small calculations

2026-09-29. Additive continuation from frontier V037. No original scientific
source, old result, handoff manifest or frozen file was overwritten.

## Scientific result

The common source/volume problem is now an explicit, falsifiable controller
candidate rather than an unspecified derivative. Its energy fixes source
contact, chamber pressure and blank-pair creation work together. Two small
implementations distinguish what can be measured and what is actually paid
for. The new controller calibration is an adopted example, not a discovered
mapping to gravitational acceleration or cosmic volume.

### Coherent measurement of the previously missing energy terms

`COHERENT_SOURCE_VOLUME_V002_RESULTS.json` contains all 72 prospectively
selected cases and 1,246 numerical checks. All pass. Full 64-state Taylor
propagation agrees with separate 16-state eigensystem propagation to
9.30e-16; the prescribed quadratic source coefficient and linear volume
coefficient are recovered to 2.04e-14 and 4.78e-15.

Branch-relative controller phases distinguish the inserted energy terms
while the reduced native density is identical across those completions at
fixed source arms. Removing controller coherence removes that information;
a global energy shift remains invisible. This is an operational discriminator
conditional on a known reference/controller, not a prediction of those
coefficients or a general measurement of an arbitrary source law. Source
coupling itself can disturb the native system. The independent review is
`COHERENT_SOURCE_VOLUME_V002_REVIEW.md`.

One technical startup failure remains preserved as V001: serialized 0 versus
0.0 caused the input-freeze comparison to reject equivalent JSON. V002 changed
only the freeze filename and comparison, not the science or tolerances. No
V001 scientific case ran. Both original files and the failed-attempt note remain.

### Creation work and actual connected incorporation

`CREATION_WORK_V001_RESULTS.json` contains all 240 prospectively selected
rows and 5,985 numerical checks. All pass. The largest check residual is
4.55e-13 in an exact quadratic finite-difference contact; the propagators
agree to 4.22e-14 and total energy to 1.71e-13. These many checks are consistency
tests of one specified model, not thousands of independent physical predictions.

The full 36-state model keeps both network sizes and both supply states. Its
conserved size-plus-supply charge is tested as a nonconstant operator, not
imposed by retaining only a single charge block. All registers are blank in
this experiment. It does not replace or reclassify the stored formed records.

At fixed source g and operational chamber V, the creation detuning is

    2 U_d d_star^2 I + Omega X_old/[N(N+1)] - Delta_s I
      + d p_source I + K_V d^2/2 I,       d=2 v_cell.

The old-link normalization work, supply debit and finite elastic displacement
all survive. An additional orthogonal three-new-link leakage channel has norm
sqrt(3)/2 at N=1, Omega=1. Matching a mean energy difference alone would not
remove it. Native, source, elastic, supply and creation component energies and
currents are retained in every row; the total is conserved.

Opposite creation coherences with the same size populations give exactly
opposite initial currents (+0.2 and -0.2 in the adopted units). A pure source
preparation instead has zero initial current and creation probability
epsilon^2 t^2+O(t^4). The Hermitian reverse process was not removed.

The same Hamiltonian also gives an exact, conditional connection to pressure:

    p = -C g - K_V V + 2 K_V v_cell n,
    d<p>/dt = 2 K_V v_cell d<n>/dt       (fixed g,V).

Thus creation coherence controls the chamber-pressure change in this model;
pressure is not an independently adjusted output. For moving coordinates the
same identity includes -C d<g>/dt-K_V d<V>/dt. The coefficient and operational
chamber meaning are the declared port inputs, not a recovered cosmic stress.

Node creation and incorporation are visibly distinct even in this small
example. Across all twelve pure-source cases at the preselected t=2,
probability of the larger size is 0.07916–0.12190. Joint probability of that
size AND a connected four-node graph is only 0.00004121–0.00015914; conditional
connected probability is 0.0003386–0.0018872. These are illustrative microscopic
results under the frozen engineering parameters, not a measured cosmic rate,
a rejection of other formation mechanisms, or an observational acceptance test.

The calculation holds g,V fixed. It tests the finite supply/native work ledger,
not the infinite-dimensional autonomous piston, preparation apparatus, or a
growing universe. No equilibrium/ground-state substitution or astronomical
parameter fitting was used. The separate review is `CREATION_WORK_V001_REVIEW.md`.

## Connected-history route

`NATIVE_RECORD_CONNECTIVITY_PATHWAY_V001.md` and its independent review give
exact analytical results at arbitrary N. For a prepared connected backbone
with M0 occupied links,

    P(any original backbone edge absent by t)
       <= min(1, Omega^2 M0 t^2/[hbar^2 N^2]).

This proves a retention window for connected excited preparations at the
inherited coefficients. It is not a claim of physical macroscopic lifetime;
the native flip scaling Omega/N and microscopic clock are retained explicitly.

The companion formation bound from incidence blank is

    <M(t)> <= (Omega t/hbar)^2.

Adding a blank pair does not bypass the time needed to connect its new links.
The necessary order-sqrt(N) formation time and the o(sqrt(N)) near-certain
retention window do not themselves prove a successful joint growth protocol.

The inherited held ground branch has <M> bounded by 64/9 as N grows, even
with record occupancy; the connected route here is an owned active preparation.
A distinct parameter interval also supports a provably extensive finite-degree
record branch, but that is not a retuning of the inherited calculation and
does not yet select geometric topology or dimension.

## Resource cost and next scientific distinction

The coherent calculation took 0.103 seconds, peak self RSS 36,323,328 bytes.
The creation calculation took 0.058 seconds, peak self RSS 34,308,096 bytes.
Both workers exited normally. These are self-RSS observations, not aggregate
hard memory enforcement. No remote/L8 job, installation, reset or publication
occurred. Small rerunnable jobs did not need custom checkpoint machinery.

The next discriminating problem is an owned formation/controller history that
both creates and incorporates new nodes while preserving useful old geometry,
with operational rulers/clocks that can connect this native model to the common
galaxy/expansion model. Additional repetitions of the checked matrix identities
will not provide that missing physical selection. Stage 1 is therefore still
being constructed; these results do not complete Stage 2 or Stage 3.

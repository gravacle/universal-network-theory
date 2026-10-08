# A finite gap copy channel and its held population change

This is a conditional analytic construction, not a formed galaxy state. A
single native record, a finite-gap copy fragment and simultaneous reversible
formation provide a nonunital channel. Its leading decrease in **active**
energy is fourth order in duration and disappears from the held energy when
formation is switched off. The first held-population change is sixth order.
For a positive fragment gap it moves population toward the lower held level,
with all switching work and fragment energy retained. No coefficient is chosen
from an astronomical observation and no numerical calculation is reported here.

The new result answers a narrower question than the existing zero-gap and
held-copy obstructions: can the actual single-content BS copy operator change
held populations when both formation and a positive fragment gap are present?
Yes, conditionally. It does not establish an attractor, an absolute pressure,
a physical density law or a nonzero gravitational response after the ports close.

## Relation to completed evidence

`NATIVE_RESERVOIR_FORMATION_CHANNEL_V001.md` already proves the held spectral
population obstruction and the exact zero-gap random-unitary control with
formation present. Its finite-gap extension was deliberately uninstantiated.
`NATIVE_COHERENT_WRITER_UNITALITY_V001.md` closes the coherent-writer loophole
for the existing zero-gap supported sectors. Neither proves the finite-gap
coefficient derived here. The calorimeter note already owns general switching
ledgers and an energy-resolved resonant port; this construction does not claim
those ideas as new or replace the local copy operator by that resonant port.

The saved four-state age-spectrum result remains unchanged: this example does
not passivate those states or repair their negative signed source responses.
The A/B source and volume assignments remain explicitly adopted alternatives.

## Conditional cell and the new boundary inputs

Use the occupied-content record block with basis blank, occupied and

```
q = (I-Z)/2,       X = |blank><occupied| + |occupied><blank|,
Hh(d) = c_d I + epsilon(d) q,
Hs(d) = Hh(d) + g X,
epsilon(d) = epsilon_r - lambda_R d.
```

Here d is an **externally clamped native incidence degree**. The record-feedback
coefficient is the BS11 form, while the clamped occupied writer gives the BS10
formation matrix element gX. This is not the evolving native incidence degree:
the full incidence-flip dynamics need not commute with d. In particular, the
usual positive BS06 incidence-flip coefficient is excluded by this controlled
restriction; it is not an invariant sector of that autonomous parent. The clamp and fixed
writer are boundary premises, not derived equilibria. Native degree, record
occupation and a physical number or energy per volume are different quantities.

Append one independent blank fragment with q_b and X_b defined identically:

```
Hb = nu q_b,       nu >= 0,
V = lambda q tensor X_b,
H_on = Hs tensor I + I tensor Hb + V.
```

The gap nu, coupling lambda, pulse duration tau, independent blank preparation
and subsequent fragment supply are new explicit operational inputs. They are
symbolic, not numerically selected here. Blank is the fragment ground state
for nu>0; that low-entropy resource is not produced by tracing out its predecessor.
g is real. Formation and copying are switched on for a single fixed square
pulse and both switched off afterward. No rotating-wave, secular, thermal-reset
or passive-state replacement is made. The initial cell state I/2 is a channel
test input, not the existing formed native state or a claimed cosmological state.
For positive epsilon a blank record is already the Hh ground state; the I/2
cooling coefficient cannot be transplanted to that original blank preparation.

The leading preparation discriminator is explicit. For an initially diagonal
record with occupied probability p and a blank fragment, formation alone gives
`Delta<q>=g^2(1-2p)(tau/hbar)^2+O(tau^4)`. For the original positive-epsilon
blank this is heating: `Delta Eh=+epsilon*g^2(tau/hbar)^2+O(tau^4)`.
The special I/2 witness removes that order-two reversible mixing by setting
p=1/2. These general-p and blank formulas are direct second-commutator analytic
identities; the fixed machine-check census below intentionally remains the I/2
channel witness and does not claim to test other preparations.

The fixed support and writer energy c_d is retained in both endpoint energies.
It drops from commutators and fixed-d cyclic differences only. It cannot be
dropped from a volume or lapse derivative, or from work required to change d.

## Nonunitality and the active energy

Define Phi_tau(rho)=Tr_b[U(rho tensor |blank><blank|)U^dagger], with
U=exp(-i H_on tau/hbar). Direct nested commutators give

```
Phi_tau(I)-I = lambda^2 nu tau^4 [q,[Hs,q]]/(6 hbar^4) + O(tau^5)
             = -lambda^2 nu g tau^4 X/(6 hbar^4) + O(tau^5).       (1)
```

One independent coefficient check starts from I tensor |blank><blank|.
The third commutator has an X_b component
2 lambda nu [Hs,q] tensor X_b. Its commutator with V has bath trace
4 lambda^2 nu [q,[Hs,q]]. Multiplication by tau^4/(24 hbar^4) yields
(1); lower reduced commutator traces vanish. The actual test input is I/2,
so its density-matrix change is half of (1).

Consequently, for that input,

```
Delta Es = -lambda^2 nu g^2 tau^4/(6 hbar^4) + O(tau^6),
Delta Eb = +nu lambda^2 tau^2/(2 hbar^2) + O(tau^4),
Delta <q> has no term through order tau^4.                       (2)
```

The density matrix can have imaginary odd-order coherences, so (1) retains
O(tau^5). H_on, the initial density and these energy/occupation observables are
real: their expectation values are even in tau. This, not an assumed absence
of fifth-order density terms, gives the energy remainders in (2).

Crucially, Es includes gX. Removing formation costs
W_form_off=-g<X>_out=+lambda^2 nu g^2 tau^4/(6 hbar^4)+O(tau^6).
It cancels the leading active-energy decrease from the held-energy comparison.
Equation (2) alone is not cooler held-record formation.

## The first held population change

For a compact independent derivation set hbar=1 inside the derivative algebra,
restore it afterward, and drop only the fixed identity in the commutator:

```
H_on = a XI + b ZI + c IZ + d0 IX + e ZX + identity,
a=g, b=-epsilon/2, c=-nu/2, d0=lambda/2, e=-lambda/2.
L(O)=i[H_on,O].
```

In rho0=I/2 tensor |blank><blank|, only the identity and IZ have nonzero
Pauli expectations. The useful exact recursions are

```
L^3(ZI) = -8a(a^2+b^2+e^2)YI -16abe YX -8ace XY,
<L^3(YI)>0=0, <L^3(YX)>0=-16ace, <L^3(XY)>0=-8abe,
<L^6(ZI)>0=320 a^2 b c e^2=20 g^2 epsilon nu lambda^2.
```

Lower occupation derivatives through order five vanish. Division by 6! and
q=(I-Z)/2 gives the new degree-sensitive leading terms

```
Delta <q> = -lambda^2 nu g^2 epsilon(d) tau^6/(72 hbar^6)
            + O(tau^8),
Delta Eh  = -lambda^2 nu g^2 epsilon(d)^2 tau^6/(72 hbar^6)
            + O(tau^8).                                      (3)
```

For nu>0 and nonzero g, lambda and epsilon, sufficiently short pulses move
occupation toward the lower Hh level. If epsilon>0 occupation decreases; if
epsilon<0 it increases. epsilon=0 or a vanishing coefficient makes this leading
term zero, not an all-orders population-conservation theorem. The exact
polynomial test proposed below retains unrestricted epsilon; it does not choose
two convenient degrees or a favorable duration.

This is a finite-duration tendency from the specified I/2 input, not convergence
of every input to a passive state. Coherence, correlations, finite supply and
repeated-channel eigenstructure remain relevant. The active level gap is
sqrt(epsilon(d)^2+4g^2), nonzero for g!=0. At finite duration the channel is
analytic in epsilon and hence in a continuous degree parameterization; no
thermodynamic phase transition or derived galactic acceleration threshold follows.
Dephasing the output could remove held-energy coherences without changing the
held mean energy, but it is another channel requiring its own owned operation;
it is not silently part of the present output.

## Complete pulse energy and source accounting

Both turn-on works vanish for this input: <gX>0=<V>0=0. With the switches held
on and d fixed, total energy is conserved. Keeping the final correlations gives

```
W_copy_off = -<V>out,
W_form_off = -g<X>out,
Delta Es + Delta Eb = W_copy_off,
Delta Eh + Delta Eb = W_copy_off + W_form_off.                 (4)
```

Thus the fragment's positive order-tau^2 energy is supplied primarily by the
switch at short time; the small negative held-energy term is not free cooling.
If switches are implemented autonomously, their complete controller energy
must replace the external work in (4). The present construction does not invent
a controller Hamiltonian or set its preparation cost to zero. Nor does it price
an unlimited blank stream for free. One finite independent fragment is the
declared resource; repeating the map requires the corresponding fresh supply
and retention of all output energy/entropy/correlation records.

For general external sources xi=(Vphysical, L, formation envelope, copy envelope,
clamp parameters), the complete supported Hamiltonian must have specified
dependence H_complete(xi), and its work is sum dot(xi)<partial_xi H_complete>.
Pressure at a fixed full state is -<partial_Vphysical H_complete>; a clock
source, if the existing full-energy lapse convention is adopted, multiplies
support, cell, fragment, interaction and controller energy together. No source
contact of these omitted boundary sectors can be inferred from Phi alone.
An added c(Vphysical)I leaves this fixed-volume channel unchanged but changes
absolute pressure. The cell therefore does not fix a vacuum-energy baseline.

At fixed clamp and volume, (4) is a complete pulse-energy identity for the
declared sectors. It is not a numerical value for the energy of constructing
the clamp, supplying a writer or changing incidence/volume. Those are explicit
remaining boundary/source inputs, not unpaid steps hidden by the identity shift.

## What the result does and does not select

The leading active cooling is degree-independent; the first held drift depends
on the native feedback detuning through (3). This is an actual conditional
selection tendency, but it has not generated its own degree, physical volume,
fragment gap or common proper-time preparation law. Local record density cannot
be inferred by replacing d with a galaxy density by notation.

Under the existing complete A homothety, if **all** cell, fragment, interaction,
support and controller energy scales transform by s^-1, and pulse histories are
compared at the same native age tau/s, the channel collapses to the same map.
Holding a fragment gap or clock fixed while scaling only the cell breaks that
identity by adding an independent reference. This may be adopted and tested,
but it is not a derivation of that reference. Under B, a record-only cell with
no carrier transport has no volume-dependent channel beyond the identity
baseline; transport/incidence dynamics or a newly specified coefficient law
must supply any additional volume selection. These are applications of the
completed A/B dictionary, not newly derived physical identifications.

After both ports close, Hh commutes with q. Its q-source retarded self-response
is therefore identically zero, whatever occupation (3) produces. Clamped degree
does not carry the 96D incidence source along with it. The construction answers
population preservation only; it is not a gravity susceptibility or a continuum
soft-spectrum construction. A viable next physical bridge still needs a formed
state with the same owned physical energy/volume source and nonzero appropriate
response, an independently specified supply/clock and dynamical degree law.

## Small exact check rather than a parameter sweep

`NATIVE_FINITE_GAP_FORMATION_EXACT_PROTOCOL_V001.md` prospectively specifies a
stdlib-only sparse rational polynomial calculation through sixth order. It
retains epsilon, g, lambda and nu as independent indeterminates, verifies the
lower-order identities, derives the unrestricted sixth-order population and
held-energy coefficients, and checks both switching ledgers coefficient by
coefficient. It performs no eigensolve, time evolution, state selection,
observational fit or tolerance comparison. Its source is inert until root and
independent review finish and root freezes it. This note contains analytic
derivations, not a claim that that independent machine check has run.

## Read source identities

- `../recovered_sources/BS_MICRO_ACTION.md`: `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`.
- `NATIVE_RESERVOIR_FORMATION_CHANNEL_V001.md`: `6db32da99d6d346736e193b34b34cb270c242821051296de1be3bf7d86031a39`.
- `NATIVE_COHERENT_WRITER_UNITALITY_V001.md`: `882da1d5745a7b67dd16ed4c4b370f01fb590279ad00e801d1109d76ed01cfef`.
- `NATIVE_OPERATIONAL_SOURCE_CLOCK_VOLUME_CANDIDATES_V001.md`: `fbddff9520f898bf888600ac62a03729d25b7cf4ad230196b04505f81853304b`.
- `NATIVE_ENERGY_SOURCE_AGE_SPECTRAL_V001_RESULT.md`: `3133247093b1bba7096b5e049d88f88985c7c21401678b58902569359e286075`.
- `NATIVE_CALORIMETER_ENERGY_ORIGIN_AND_RESONANT_PORT_V001.md`: `1f8a0d04767f039ccc4af50b6f412129092cdcf8016e71c83d04893fb336b5fb`.

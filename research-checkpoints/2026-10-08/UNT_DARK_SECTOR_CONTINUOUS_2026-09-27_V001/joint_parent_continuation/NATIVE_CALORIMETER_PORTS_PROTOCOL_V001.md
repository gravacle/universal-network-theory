# Prospective work-accounted native calorimeter ports

2026-09-29. Inert source and prospective protocol; root runs the sole producer
after independent preflight/freeze. No output from this experiment has been
viewed. The native thermal packet is fixed evidence, not rerun or modified.

## Explicit new operational completion

Keep all four native64 preparations: cycle/tree, uniformly blank/occupied
fixed records. Read their actual saved vectors at ages0,.5,2; do not re-form,
rephase, dephase or thermally replace them. Authenticate the full packet,
freeze and transitive source manifest before loading any numerical definition.
The native Hamiltonian, absolute storage/degree energies, record feedback and
current-square term remain exactly as previously qualified. Reconstruct H
from its already reviewed node partition and separately assembled row matrix.

Attach two **distinct two-level calorimeter probes** to disjoint edges0 and3,
(L0,R0) and(L1,R1). Tensor order is native64⊗probe0⊗probe3. The adopted on-state
Hamiltonian is

    H_on = H_native + omega(N0+N3) + g V,
    V = n0 sigma_x,0 + n3 sigma_x,3.                         (1)

The probes have separate Hilbert factors and no direct coupling. This is a
new explicitly specified BS port realization, not native electrodynamics,
an existing formed bath, or a physical temperature calibration. At finite g
it is an exact two-level model. From vacuum its leading weak response agrees
with the old oscillator kernel, but a two-level system is not a finite-g
bosonic photon model. No thermostat, resetting or white-noise law is inserted.

Retain all old frequencies{.75,1.5,3}, durations{.25,1,2}, native ages{0,.5,2},
and all four native states. Declare before results g={.01,.005}, in native
hbar=1 units; these are convergence controls, not a radiation fit. For each
combination retain probe number-state inputs|00>,|10>,|01>. The latter supply
their explicit initial probe energy omega and test reverse absorption; they
are not thermal populations. Complete census4×3×3×3×2×3=648. Only twelve
(record sector,omega,g) Hamiltonians of dimension256 are needed, with eighteen
batched input columns each. There is no selection by a favorable spectral gap
or by the sign of a previously computed channel.

## Complete source-work ledger

Coupling g is switched on at the window start and off at its end. All initial
probe number states have<V>=0, hence W_on=g<V>_initial=0. During the interval
H_on is constant and conserved. Immediately before the end retain
E_native, E_probe and E_interaction=g<V>. At removal,

    W_off = -E_interaction,
    Delta E_native + Delta E_probe = W_on + W_off.           (2)

The worker checks the initial zero interaction, on-state conserved energy,
and final identity independently. No source work is silently set to zero at
the final switch, and positive probe energy is not called work-free radiation.
Store signs of all terms, the complete4×4 reduced probe density, populations,
both lowering means, cross coherence and connected cross coherence. No
positivity or thermality gate is imposed on native energy exchange or work.

An arbitrary additional identity c(g)I would leave dynamics unchanged. It
shifts the separate work terms, and cancels from their sum when the protocol
returns to g=0. The present explicit port convention is c=0; the experiment
cannot identify unknown actuator contact c''(0), volume coupling or SI units.
This limitation is not cured by fitting a probe temperature.

## Same-state weak-kernel predictions and exact remainder bounds

Use the authenticated thermal-packet rows, including their coherent means;
never replace them with energy-dephased diagnostics. For probe initially0,
P(flip)=g² K_plus,ee+O(g⁴); for probe initially1,
P(flip)=g² K_minus,ee+O(g⁴). Both channels remain, including small, inverted
or absent responses. For the vacuum pair, with the stored original-edge
indices0 and3,

    <sigma-_e> = -i g exp(-i omega T)<F_e^+> + O(g³),
    <sigma+_0 sigma-_3> = g² K03^+ + O(g⁴),
    connected cross = g² Kconn03^+ + O(g⁴).                 (3)

The cross entry is K03, not its conjugate K30. Compute connected cross by
subtracting conjugate(<sigma-_0>)*<sigma-_3>. Independent probes allow the
leading cross response to test native source correlations. At finite g the
probes also backreact; all such effects belong to(1) and its ledger rather
than being relabeled as source-free native noise.

No fitted weak-agreement tolerance is used. Since||V||≤2, put b=2|g|T,
r2=cosh(b)-1, r3=sinh(b)-b. Probe parity changes at every V insertion and
H_free preserves it. The norms of even orders≥2 and odd orders≥3 are bounded
by r2 and r3. A projector onto a changed individual probe occupation kills
the zeroth-order state, so, for all three number-state preparations,

    |P(flip)-g² K_ee| ≤ 2b r3+r3²+r2².                    (4)

For the vacuum pair, sigma+_0 sigma-_3 acts only in the one-excitation sector,
and its corresponding error is at most Bcross=2b r3+r3². A lowering mean has
error at most Bmean=r3+2 r2 sinh(b). Since the magnitude of a leading mean is
at most b, the connected-cross error is bounded by

    Bconnected=Bcross+2b Bmean+Bmean².                      (5)

These are conservative exact-arithmetic Dyson bounds, not measured corrections
or a claim of irreversible emission. Add a fixed2e-9 roundoff allowance when
checking them. Retain raw deviations and normalized coefficient corrections
at both g values, and their paired differences for all324 configurations.
Do not demand a fixed error ratio: the leading correction may vanish or
cancel. The coefficient corrections are outputs, not fitted physical success.

## Independent numerical checks and fixed gates

Primary: Hermitian eigensystem of each256D H_on, preserving absolute energies.
Independent: the existing authenticated native-carrier Chebyshev/FFT vector
action, with its declared Gershgorin enclosure and conservative Bessel-tail
and alias bounds. Its maximum degree4096 is an algorithmic guard, not a
physical or research deadline. Only inert definitions are loaded; neither
ancestor producer is called. Use the full initial batch at every window.
There are36 method rows,12 spectra,648 physical readouts and324 g-pairs.

Fixed absolute gates: operator identities2e-11, state-vector/eigensystem/probe
density checks2e-9, conserved energy and full work ledger2e-8. Probe density
Hermiticity uses the operator tolerance; its minimum eigenvalue is permitted
only the state tolerance of numerical negativity. The Dyson bound residual
has the independently fixed2e-9 allowance. Store all failures, not only passed
rows. No numerical threshold is a common-temperature or CMB criterion.

The source checks tensor-factor independence, V Hermiticity and row norm≤2,
saved native vector normalization/energy, initial zero port energy, on-state
unitarity and energy, switch work, density Hermiticity/trace/PSD and probe
energy reconstructed from occupations. Source choices, coupling and every
old frequency/window are frozen before the new producer runs.

## Custody and limits

Stdout-only `freeze` and `run`. Freeze authenticates the old result and its
canonical payload, old COMPLETE statuses, the old freeze and every ancestor
source, plus the new source/protocol and mechanism note. Run requires exact
snapshot equality. Root captures/publishes JSON with its canonical payload
and freeze hashes; the worker writes no files and installs nothing. Result
contains all row arrays, spectra/method controls, refinements, maxima/counts,
failures, elapsed time and peak process-self RSS. Maximum matrix dimension256;
the first complete run is a bounded small job, not an added background worker.

This is an operational energy-transfer and correlation test on explicitly
chosen ports. It neither proves nor assumes network thermalization, physical
photons, a thermodynamic limit, an irreversible rate, a common temperature,
or a cosmological origin. The native-to-physical source/contact/clock/volume
dictionary remains distinct. A network-first finite preparation is allowed;
no Big Bang or inflationary premise is used to accept or reject it.

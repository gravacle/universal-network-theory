# Native calorimeters: energy origin, record modulation, and an autonomous criterion

2026-09-29. Read-only interpretation of the saved calorimeter packet and
analytical continuation. No producer, propagator, eigensolver or new numerical
grid was run. The independent auditor owns numerical qualification. No
singular beginning, inflation, physical photons or SI temperature is assumed.

## 1. The energy ledger answers more than its residual

The saved packet is COMPLETE:648 rows,6602 checks, no recorded failures.
The largest saved switch-ledger residual is9.45e-14 and the largest independent
state discrepancy3.50e-14. These small residuals qualify the following signed
energy attribution, not a claim of thermality.

There are216 initially-vacuum rows. Define the descriptive funding fractions

    f_act = (W_on+W_off)/Delta E_probe,
    f_native = -Delta E_native/Delta E_probe = 1-f_act.       (1)

The denominator is positive in all saved vacuum rows. These fractions may
lie outside[0,1]: negative actuator work means the actuator also extracts
energy; f_act>1 means it supplies both probe excitation and native heating.
The fifty-four rows in each table entry include both g-refinements and are
not independent measurements or a probability distribution.

| Native preparation | min f_act | median f_act | max f_act | rows with f_act>1/2 |
|---|---:|---:|---:|---:|
| blank cycle | .866177 | .990595 | 1.000408 |54/54|
| blank tree | -.133560 | .972523 | .998707 |48/54|
| occupied-record cycle | .214867 | .980197 | 1.012163 |48/54|
| occupied-record tree | .016381 | .944089 | 1.006260 |48/54|

Thus198/216 vacuum rows receive **most** of their probe energy from net
actuator work. The majority boundary1/2 merely defines the word “most”; it
is not an observational acceptance cut. A native energy debit is present in
200/216 rows, but generally supplies only a small fraction. Positive probe
energy alone would have badly overstated spontaneous native release.

At the previously illustrated inherited middle window(age=.5,T=1,omega=1.5,
g=.01), the absolute cycle ledger is:

| Record sector | initial native E | final native E | probe E | net actuator work |
|---|---:|---:|---:|---:|
| blank |21.5|21.499998449001|.000242533058|.000240982059|
| occupied |21.5|21.499999606289|.000241231909|.000240838198|

All degree/storage/feedback constants remain. Their actual native debits are
1.5509992e-6 and3.9371080e-7, respectively. These are conditional native-unit
energies, not a conversion to astrophysical radiation energy.

The opposite regime also occurs and must not be hidden. For blank tree,
age0,T=2,omega=3,g=.01, native energy decreases2.8188858e-5 while probes gain
2.4867558e-5 and the actuator extracts3.3213000e-6. Six blank-tree vacuum rows
have negative work. This is genuine native release **in the specified port
protocol**, not merely positive detector population. It is still neither a
thermal emission rate nor an autonomous steady radiation mechanism.

## 2. Why the dominant switching contribution is unsurprising

An exact solvable control needs no additional run. Freeze an incidence probe
operator to n=1, so it cannot exchange any energy with the native subsystem.
The initially-ground two-level detector evolves during the on-window under

    H_D=omega N+g sigma_x,
    p_exc(T)=4g²/(omega²+4g²)
              *sin²[sqrt(omega²+4g²)T/2].                  (2)

Its native debit is zero. Conservation during the window gives
<g sigma_x>=-omega p_exc, hence W_off=omega p_exc:100% of the final free
probe energy comes from the actuator. To leading order this is precisely
g²|integral_0^T exp(i omega t)dt|², the coherent switching part of the old
finite-window Gram. Near-unit link occupancy and large coherent means make
this a relevant explanation of the cycle's dominant signal; it is not a
replacement of the actual fluctuating native system by a fixed graph.

This observation also explains why decreasing g alone does not eliminate the
funding issue. Probe energy and switching work both begin at order g². A
well-qualified weak-coupling limit can retain f_act near1.

## 3. Record modulation and correlated readout survive the work audit

For the same middle cycle window, the real connected cross coherence between
the two **independent** detector factors is

    blank:     8.76568699e-10   (old g²Kconn03:8.76626609e-10),
    occupied:  1.42330169e-8    (old g²Kconn03:1.42344325e-8). (3)

The small imaginary parts and all other rows remain in the packet. Finite-g
deviations satisfy the predeclared Dyson bounds; no cross-channel magnitude
was a physical success gate. The raw coherent cross signal is much larger,
around8e-5 in these rows, and must not be called connected noise.

The record-controlled correlation is therefore transmitted to explicit
calorimeter degrees of freedom with an accounted energy budget. The cycle
comparison still matches initial native mean21.5 and variance1.5 and all
initial node-energy first/second moments. As proved in the companion note,
the third energy moment differs by1; full energy distributions are not equal.
Neither matched moments nor connected detector correlations imply that the
network supplied most of the detector energy. Information/correlation transfer
and energy supply are separate claims.

Uniform occupied records change native feedback, not logical record content.
Their formation was not modeled. There is no evidence here for a temperature,
a Planck spectrum, homogenization without recurrence, or a common thermal
bath. The previous native kernel already retains nonstationarity and
incompatible resolved Gibbs ratios.

## 4. A minimal exact autonomous energy-exchange port

Let H=sum_E E P_E be the same finite native Hamiltonian, O=n_e an owned local
source, and choose a detector gap omega>0. Define the energy-lowering component

    A_omega=sum_(E-F=omega) P_F O P_E,
    [H,A_omega]=-omega A_omega.                             (4)

Adopt the explicit energy-resolved detector interaction

    H_free=H+omega N,
    V_res=A_omega sigma_+ + A_omega† sigma_-,
    H_tot=H_free+g V_res.                                   (5)

Then [H_free,V_res]=0 exactly. In an initially uncorrelated native state and
a detector number state, <V_res>=0. It remains zero because V_res commutes
with H_tot, even if g is varied externally. Consequently

    Delta E_native=-Delta E_detector,
    <E_interaction>=0,      <W_on>=<W_off>=0.                (6)

The free total energy distribution, not only its mean, is preserved by the
evolution. Probe excitation from vacuum now certifies a native energy debit.
At short time,

    p_exc=g²t² <A_omega†A_omega>/hbar²+O(t⁴),               (7)

and the coefficient is the native downward-transition measure already
represented by the saved emission lines, aggregated at equal gaps. No Gibbs
state or positive-temperature assumption is required. Negative/absent and
reverse channels retain their physical meaning.

Equations(4)-(6) are an explicitly adopted energy-selective port, **not** the
unmodified local coupling n_e sigma_x. The projectors make it spectrally
resolved and generally nonlocal in native time. It can be motivated by a
controlled narrowband/secular approximation, but that approximation needs
small weighted off-resonant effects and an appropriate time window. It does
not follow from the short windows of the completed calorimeter experiment.
Choosing a native gap is an operational detector choice, not an observed
cosmological fit; retaining all gaps avoids selecting an advantageous line.

There is a useful constraint without another grid. For fixed omega and
initial detector number state, every subsequent detector occupation under
(5) depends only on the native density matrix dephased between distinct
energies. Indeed the evolved detector number commutes with H_free, and its
number-state matrix element therefore commutes with H. Varying the prior
source-free native hold age cannot alter that readout. Equal-frequency
detector cross observables have the same property. A detector sensitive to
energy coherences must supply an appropriate phase/time reference or compare
unequal-energy coherences; that reference cannot be hidden in a thermal rate.

## 5. The old three frequencies are not resonant native gaps

Read-only differences of the saved48 energy-group values give the following
closest **structural** gap; source selection rules can only remove channels.

| record sector | detector omega | nearest native gap | absolute detuning |
|---|---:|---:|---:|
| blank |.75|.7506613310|.0006613310|
| blank |1.5|1.5504818577|.0504818577|
| blank |3|3.0070034877|.0070034877|
| occupied |.75|.7404791988|.0095208012|
| occupied |1.5|1.5010233836|.0010233836|
| occupied |3|3.0068818293|.0068818293|

These separations are far above the original1e-10 grouping tolerance and the
saved eigensystem residual. This is a qualified saved-spectrum statement,
not newly performed interval arithmetic. No exactly matched line is resolved
at any of the old three frequencies. In the strict resonant construction the
corresponding A_omega is therefore absent at the qualified spectral resolution.
The finite rectangular probes were testing broadband transient response, not
an established resonant irreversible emission channel.

This is not a prohibition of release at the native system's own gaps, of
finite-bandwidth detectors with an owned controller/supply, or of a larger
network spectrum becoming dense. It identifies precisely what cannot be
inferred from these three finite-window occupations.

## 6. What would make a local pulse genuinely autonomous?

If the **local** coupling n_e sigma_x is essential, a source controller must
be retained instead of prescribing g(t). A minimal conditional Hamiltonian is

    H_full=H+H_D+P_C²/(2M_C)+g f(Q_C) n_e sigma_x,           (8)

with a declared finite-energy incoming controller packet and compactly
supported f. If incoming and outgoing packets are outside the interaction,
the exact asymptotic ledger is

    Delta E_native+Delta E_detector+Delta E_controller=0.    (9)

Detector excitation can still be controller-funded. Measuring the controller
debit distinguishes that from native release; autonomous does not mean free.
Mass, packet, envelope and coupling are counted new inputs. No such controller
or extra numerical evolution is adopted by this note. A finite controller
with a different explicit clock/supply implementation is also possible, but
must supply the same energy accounting and a release/readout condition.

The exact resonant criterion already answers the next immediate question;
another arbitrary frequency/time grid is unnecessary. The meaningful next
mechanism must specify either an energy-selective detector port or an actual
finite-energy controller/broadband reservoir, and then jointly test native
energy debit, reverse response and connected correlations. None of this
requires an inflationary or Big Bang origin assumption. It also does not
manufacture common temperature by imposing a Gibbs reset.

Absolute source contact/volume remains unbound: adding an identity c(g)I
does not change trajectories, and cancels from net work for equal endpoints.
The completed cyclic calorimeter ledger is robust to that bookkeeping freedom,
but does not measure c''(0) or create a physical-volume map.

## Evidence identities

- Calorimeter result `NATIVE_CALORIMETER_PORTS_V001_RESULTS.json`:
  `0dd6bb4ecc1b4e3875d603755de98e6b0dbe8028a416c7509fa8cca9ce8516ed`.
- Its freeze: `dd3eada48d549bfd53663fc362375ef56c9d7a186807719aa0cb5933c55c44fe`.
- Canonical payload: `339d7803e7642b21643d239ebc9a2e81b637cc01d12b6e33815fa72a11623871`.
- Native packet: `8531cd6f2cf7d60e4b981428c9f80b55ee76b23f17bd4ab91c0e435894010538`.
- Companion mechanism note: `3fd418d5674018b7f115cce6b8bfe0b8fa0c5d1e82531e4cbcdf51c744396e65`.

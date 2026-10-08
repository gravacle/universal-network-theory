# Network temperature and correlations: a minimal origin-neutral discriminator

2026-09-29. Analytical/prospective only: no new native evolution, thermal fit, data download or observation score. A network-first radiation origin is a legitimate hypothesis. Nothing below requires inflation, a scale factor reaching zero, or a Big Bang origin. If ordinary photon/redshift/metric equations are used later, they are an explicitly conditional physical interface, not UNT's origin premise.

## The next question is transport, not an imposed uniform state

The existing A/B/C alternatives remain distinct:

- A supplies net radiation energy/number. It must produce the frequency-resolved Planck tangent and debit the same network reservoir.
- B continuously replaces photons with zero net exchange. It still has opacity, noise and angular/polarization consequences.
- C prepares a thermal/correlated radiation state during an earlier **finite network preparation interval**, then approximately releases it. Calling this state “primordial” need not mean a singular beginning or inflation. Its uniformity and correlations need a preparation mechanism, not merely a uniform initial density matrix.

A connected graph is not yet a common-temperature bath. Coherent hopping establishes possible transport, but can retain memory, conserved sectors, localization and recurrences. The already computed isolated native cell is a useful concrete warning: its five populated n-channel absorption/emission ratios do not share one inverse temperature. Identical independent copies multiply these line strengths without supplying continuum support or mixing.

The smallest useful next deliverable is therefore one **same-state transport/noise/probe kernel packet**, not a new arbitrary heating law or a cosmological map. It tests whether the owned native links actually exchange local energy and create the source correlations that a common-temperature explanation needs. A thermal approximation is a possible outcome of that test, not its initial condition.

## 1. Exact owned native starting point

Use the existing N=2, 64-dimensional incidence/one-carrier, blank-record, held-copy-off sector and its two already declared graph preparations (cycle mask15 and tree mask11, carrier at L0). Keep the original coefficients, absolute degree/on-site energy and microscopic clock. Neither graph is a cosmological spatial geometry or a thermal preparation. Both reference graphs are connected; their comparison is not a disconnected-network control.

An explicit node energy allocation is available without factorizing quantum links. For each of the four nodes v, take

    h_v = Ud(d_v-dstar)^2 + epsilon_psi P_v
          + sum_(e incident v)[Delta*n_e/2 - hN*X_e/2
                               - t*n_e*T_e/2]
          + lambdaJ sum_(e incident v) n_e P_v .              (1)

Then sum_v h_v is exactly the held Hamiltonian in this sector; any retained identity constant is allocated explicitly. This is an energy partition, not a new interaction. The local energies need not be positive and their current support need not be the adjacency of the initial basis graph. In particular, carrier-number transfer is not automatically heat transport.

Define the oriented local-energy current operator

    J_(u->v)=(i/hbar)[h_u,h_v] = -J_(v->u).
    h_v_dot=sum_u J_(u->v),        H_dot=0.                  (2)

For a patch A, summing (2) cancels all internal terms and gives its exact crossing current. Actual n-carrier correlations and all overlapping degree terms remain. A different energy allocation changes local bookkeeping; freeze (1) before comparison, keep total/patch work, and do not fit the allocation to make a flux positive.

Starting from each actual owned preparation, a prospectively declared small local source −epsilon*f(t)*h_A probes

    chi_(vA)(t,s)=(i/hbar)theta(t-s)<[h_v(t),h_A(s)]>,
    delta E_v(t)=epsilon integral chi_(vA)(t,s) f(s) ds.       (3)

Use the full two-time kernel, not a stationary replacement. The source's explicit work is −epsilon integral f_dot<h_A>dt, including any switching terms and interaction storage; after source removal the total held energy is conserved. The original localized carrier already supplies an inhomogeneous preparation. No uniform temperature or Gibbs state is inserted to make mixing happen.

Compute current covariances and the same local incidence probe operators O_e=n_e. For declared finite probe windows,

    F_e(omega,T)=integral_0^T exp(i omega s) O_e(s) ds,
    K_ef=Tr rho F_e^dagger F_f,                              (4)

is a positive-semidefinite Gram matrix. For independent initially vacuum oscillator probes, their leading cross occupation is g_e*g_f*K_ef/hbar^2. The connected version subtracts the coherent means and is positive semidefinite too. This separates correlated emission from a deterministic coherent drive. Retain actual ages and any initial correlations; a shared photon probe would itself create a common channel and cannot count as native correlation generation.

The same source matrices must therefore account jointly for local energy transfer, photon-probe noise and spatial cross-correlations. In a separately labeled energy-dephased stationary diagnostic, compare log(Wabs/Wem)/gap across all populated local probe channels, retaining absent/inverted lines. A single common fitted beta can be a diagnostic summary; independent beta/width adjustments per line are not an explanation. A pass in charge-neutral n channels is not full Gibbs/KMS equilibration across conserved sectors. Dephasing or time averaging is not a physical preparation/reset.

## 2. The conditional mixing law gives a testable relationship

Only if a specified coarse-graining of (2)-(4) supports local thermometry, positive heat capacities C_v and reciprocal conductances g_uv, write the finite-window linear closure

    C*Tdot = -L_g*T + q,       C=diag(C_v)>0,
    (L_g T)_v=sum_u g_uv(T_v-T_u),   g_uv=g_vu>=0.             (5)

Here g has energy/(temperature*time) units and C has energy/temperature units. This is an explicitly conditional near-equilibrium model, **not** the native Hamiltonian or a consequence of graph connectivity alone. It needs a demonstrated memory/time window; coefficients come from the same state/current response, not from the desired CMB temperature.

For a closed fixed graph, q=0, fixed C and g, the common temperature is fixed by energy, Tbar=(1^T C T)/(1^T C1). With x=C^(1/2)(T-Tbar*1), A=C^(-1/2)L_g C^(-1/2),

    x_dot=-A x,
    ||x(t)|| <= exp[-lambda2*t] ||x(0)||                     (6)

on the energy-contrast subspace, where lambda2 is its smallest positive eigenvalue. Initial connectedness is only a structural prerequisite for positive lambda2; bottlenecks and weak couplings can make mixing arbitrarily slow. A sufficient time for fractional contrast reduction eta_T is log(1/eta_T)/lambda2. No numerical eta_T is chosen here as an observational gate.

More importantly, the same response governs correlations. For an additionally owned internal-exchange noise xi, energy conservation requires 1^T xi=0. If its near-equilibrium fluctuation law is

    <xi(t)xi(s)^T>=2 kB Tbar^2 L_g delta(t-s),

then in x variables the covariance obeys

    K_dot=-A K-K A+2 kB Tbar^2 A.                            (7)

Each nonzero eigenmode has

    <x_a(t)> = exp(-lambda_a*t)<x_a(0)>,
    K_aa(t) = exp(-2lambda_a*t)K_aa(0)
                    +kB Tbar^2[1-exp(-2lambda_a*t)].         (8)

Thus a mixing mechanism cannot independently choose a uniform monopole and arbitrary surviving/generated correlations. Damping and noise come from the same modes. In this simple closed Gaussian limit, equilibrium temperature covariance is kB*Tbar^2*[C^-1-11^T/(1^T C1)]; the negative off-diagonal piece enforces fixed total energy, not an invented acoustic pattern. More structured correlations are possible with propagating modes, memory, driven sources or different native states, but must appear in their measured kernels rather than being assigned afterward. Equations (5)-(8) are a discriminator for that closure, not a claim that native UNT has white noise or that a sky is a graph covariance matrix.

If the graph grows or ports replenish energy, the new-node state, changing heat capacity, source/supply energy and work must be included. Assigning each new node Tbar by definition would assume the very common-temperature result being tested. The first bounded test should hold this part fixed.

## 3. Minimum bounded test and its possible outcomes

The next source/protocol can reuse the existing full native64 Hamiltonian and old retained times, with no new formation or parameter fitting. Freeze the node-energy partition (1), anchored patches, incidence probe operators and original cycle/tree states. Record the exact current continuity and energy-work identities, all two-time energy/current kernels, all finite-window probe Gram matrices, and separately the stationary local-line ratios. Independent commutator/spectral checks qualify numerics; thermality and mixing are outputs, not correctness gates. No new numerical worker is authorized by this note.

This one low-RAM packet can distinguish: (i) coherent/recurrent transfer only; (ii) an approximately stationary local-temperature channel within a stated window; (iii) state-dependent correlated source emission; or (iv) an absent required exchange channel. It cannot prove thermodynamic mixing from a finite recurrence system. If no irreversible window exists, the next actual mechanism would need the already explicit reservoir/fragment ports or a controlled growing-size limit, retaining their energy and correlations—not an unexplained Gibbs reset.

For a larger-network claim, test the time/size dependence of the response-derived mixing scale and cross-correlation transport using the same definition, including bottleneck/decoupled controls. The existing single-carrier locality theorem provides a sector-specific finite-time transport constraint, not a general heat bound. A claim that network adjacency joins regions distant in the eventual metric needs an owned operational distance/clock mapping and its finite preparation history. Neither an assumed cosmological horizon nor an assumed absence of one should decide it by terminology.

For A, compare any derived broad-band rates with the required Planck tangent and energy debit. For B, combine the common-temperature test with replacement opacity and correlation transfer. For C, explicitly show contrast reduction and generation of the required correlations over a finite network interval before release. None requires a=0 or inflation; none follows simply by imposing uniform initial data. A future sky comparison still needs the photon, polarization, geometry and observation maps. This is a concrete mechanism discriminator, not a grand proof or a claim that the network explanation has already outperformed another cosmology.

## Read-source identities

- Root A/B/C brief `UNT_CMB_NETWORK_THERMAL_HYPOTHESIS_V001.md`: `f25c9c1104defdceba8bb916bc05c59ea06fb41f8d309224b8d29116cdfd9210`.
- `CMB_CONTINUOUS_SOURCE_ANALYSIS_V001.md`: `b4cb12de9a11767f91b6441d860711e09f4f8e64ec7d1517c5065e7ffbe50ad4`.
- `NATIVE_PHOTON_SOURCE_PATHWAY_V001.md`: `e6bdd502ae6e31c1bc318a49aea98f5db2c882e82143ca99d849587919fd4049`.
- `NATIVE_PHOTON_PROBE_RESULT_V001.md`: `570f1590addc642c6272ee300be941d6bf8d3cf341374b0b439708f87db1b1a6`.
- `NATIVE_CARRIER_FINITE_TIME_LOCALITY_V001.md`: `0023459d201d6399abbdafeb0ee136ec6232ced06f163c0fba1912354fa31a7b`.
- `NATIVE_GAUGE_INVARIANT_TRANSPORT_MATCHING_V001.md`: `8b924fac55a8809afeed7289a4293c2ab479c2ae8b0ddc1ce1f912387dd537b3`.
- Native action `../recovered_sources/BS_MICRO_ACTION.md`: `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`.

The law peer independently checked the conditional weighted-Laplacian/noise identities and the need to conserve the closed energy mode. No scientific producer was executed for this note.

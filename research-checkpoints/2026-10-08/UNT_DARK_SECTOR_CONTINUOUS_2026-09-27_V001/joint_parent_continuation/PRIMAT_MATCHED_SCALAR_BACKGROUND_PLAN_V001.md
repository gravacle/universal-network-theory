# Matched conserved-scalar PRIMAT background: prospective adapter

2026-09-29. Source/derivation only. This is an additive implementation plan
after ordinary qualification, not an executed abundance calculation. All
ordinary/upstream sources, controls and results remain unchanged. No compiler,
producer, source import, download or new state preparation was used here.

The implementable next comparison is **the same retained hard scalar against
matched dust, both with the same ordinary baryon normalization and prescribed
NEVO thermal history**. It repairs the scalar conservation defect of the old
temperature-proxy comparison. It does not solve the changed neutrino collision
or reheating problem. A finite hot initial slice is an imported conditional
comparison, not a premise about a Big Bang, inflation or UNT photon formation.

## 1. Same state, exact current, and a single density replacement

Use the adopted homogeneous scalar-fluid action and the already owned
`unt_hard_barotrope_v001` provider. Let e_R(I) be the unweighted mode energy,
omega=e_I, and retain the supplied R,I1,e1 and present physical density rho_H1.
In common natural energy-density units,

    I(a) = I1/a^3,
    rho_H(a) = rho_H1 e_R(I1/a^3)/e1,
    p_H(a) = rho_H1 [I omega-e_R(I)]/e1,
    d rho_H/d ln a = -3(rho_H+p_H).                       (1)

The provider validates the stored e1 against the supplied action and records
its tiny quadrature-consistent normalization correction; this is not a density
fit. Its `rho1` already includes beta and the physical stress normalization.
Do not multiply by beta again. Ideal dust is the separately labelled existing
infinite-gap branch, not a numerical small-pressure replacement of finite R.

For each inherited background and baryon value x=omega_b,

    omega_H = h_cal^2 Omega_m - x,
    rho_H1 = omega_H rho_crit,100,
    rho_b1 = x rho_crit,100,
    rho_Lambda = h_cal^2(1-Omega_m) rho_crit,100.          (2)

All must match the saved shared calibration. In PRIMAT,
`cfg.Omegach2=omega_H` remains a normalization label: replace its CDM density
by (1), do not keep CDM as well. Do not set this field to zero and let the
upstream Lambda subtraction rematch the vacuum. No new abundance, vacuum
offset or independently fitted DeltaNeff is allowed. Keep DeltaNeff=0,
extra_rho absent, EDE absent and chemical potentials/analytic distortions zero.

The candidate Friedmann sum is

    rho_tot = rho_EM(T) + rho_nu,NEVO(T)
              + rho_b1/a^3 + rho_H(a) + rho_Lambda,
    H = MeV_to_s^-1 sqrt[8 pi rho_tot/(3 M_Pl^2)].        (3)

Temperatures are MeV, densities MeV^4, H s^-1. The source's conversion is
rho[MeV^4]=1e-3 rho_mass[kg/m^3]/MeV4_to_gcm3; do not add another c^2.
H_cal sets the inherited critical-density normalization; adding the ordinary
radiation terms does not authorize making H(a=1)=H_cal by subtraction.
Keep current same-state T0=2.72548 K distinct from the ordinary baseline's
2.7255 K. Candidate and row-matched dust use the same declared T0 and constants;
the baseline is preserved, not silently redefined.

## 2. Baryon rest energy: reconcile two existing conventions

The inspected H sum has CDM and vacuum but no baryon rest term. The nuclear
network nevertheless uses `rhoB_BBN=ma*n_B` in g/cm^3 as a reaction-density
convention. The pinned source defines

    mB_ref = ma[(1-0.247) HOverma + 0.247 He4Overma/4],
    eta0b = x rho_crit,100/(n_gamma0 mB_ref),
    n_B(a) = eta0b n_gamma0/a^3.                         (4)

Consequently the cosmological rest-density term consistent with (2) is

    rho_b(a) = mB_ref n_B(a) = x rho_crit,100/a^3,
    rhoB_BBN / MeV4_to_gcm3 = (ma/mB_ref) rho_b(a).        (5)

Blindly adding the reaction `rhoB_BBN` to H would introduce the unwanted factor
ma/mB_ref. Keep the nuclear reaction convention and eta conversion unchanged;
add (5) explicitly to the Friedmann sum, with its own matched control below.
The source's 24.7% reference mixture is not the newly predicted helium yield.

This is exact *normalization reconciliation*, not exact composition-dependent
baryon thermodynamics. Evolving nuclear binding/rest masses, charge-balancing
electrons and baryon thermal energy/pressure are not thereby solved. A future
composition correction must use one declared mass/electron convention, rather
than double-counting the pair plasma or feeding a new Yp back into eta without
recalibration. If consistent mass-per-baryon bounds m_- <= m(Y) <= m_+ are
specified, number conservation supplies the separate rest-density bound

    |delta rho_b| <= n_B max(|m_- - mB_ref|,|m_+ - mB_ref|). (6)

It does not bound omitted thermal energy or nuclear heat transfer. Report
these as distinct ordinary-sector approximations; do not claim (6) has been
numerically evaluated or that it alone qualifies full energy conservation.

## 3. Exact conditional simplification and a useful prediction

Use the standard, not `custom_background`, initializer. The custom branch
disables incomplete decoupling/spectral corrections and would change the weak
rates while ostensibly changing only H. Also retain external_scale_factor=false.
Define sigma=s_EM/T^3, C_src=(ds_EM/dT)_supplied/T^2 and the imported heating
function N_heat(T). The actual source evolves x_a=ln(aT),t_rel by

    d x_a/d ln T = 1 - C_src/(3sigma+N_heat),
    d t_rel/d ln T = -C_src/[(3sigma+N_heat) H(T,a)],
    a = exp(x_a-ln T).                                  (7)

With the same endpoint entropy normalization, the first equation is independent
of H. Thus matched scalar and dust have the **same prescribed a(T), T_nu(T),
reaction density at T, and physical weak rates Gamma(T)**. Separate adaptive
integrations need not be bitwise identical, so this is a numerical comparison
at common T nodes, not a claim about identical accepted ODE step sequences.
Only elapsed time versus temperature changes. In particular,

    |dt_S/d ln T| / |dt_D/d ln T| = H_D(T)/H_S(T).         (8)

For the positive quadratic+quartic mode, 0<=w<=1/3 implies, for 0<a<=1,

    rho_H1 a^-3 <= rho_H(a) <= rho_H1 a^-4,
    H_S >= H_D,                                         (9)

when the other components are identical and positive. Therefore each
nonnegative fixed-temperature rate exposure obeys

    K_S = integral Gamma(T)|dt_S/d ln T| d ln T <= K_D.   (10)

The existing n/p relaxation integrand Gamma_np+Gamma_pn gives a direct test of
(8)--(10). The scalar leaves less reaction time in this conditional model.
This is not a theorem ordering D/H or Yp: a coupled reaction network has
competing channels, moving equilibria and a finite initial composition.

The background source uses a_end=(T0/T_end)
[sigma_end/(4pi^2/45)]^-1/3. Preserve and report its finite-endpoint thermal
remainder. Its t_ini=1/(2H_start) is an additive time-origin convention, not an
age derived for the new history. Use elapsed-time quantities; the autonomous
nuclear system is unaffected by a common additive time shift.

## 4. Minimal owned code changes and controls

Create a new `bbn_inputs_v001/primat_c_reference_v001/derived_scalar_v001/`
packet only after ordinary qualification. This note creates no such sources.
Keep the ordinary plasma/weak fail-closed cache transformations, selected data,
compiler flags and in-memory nuclear API. No cache generation, stock main,
output-file path or dynamic source loading is needed.

1. Derive a new `background.h`/`background.c` from the pinned originals. Add a
   borrowed immutable hard-material context and an explicit baryon-rest switch,
   plus a separate owned initializer. Initialize these **after** the common
   zero-initialization and **before** setup_background_and_cosmo. Assigning them
   before the old initializer is wrong because its memset erases them. Keep the
   legacy initializer's branch and arithmetic unchanged.
2. Factor the Friedmann sum into a checked component evaluator, used by both
   the H accessor and stdout diagnostics. In the owned branch only, replace
   rhocdm_a3/a^3 by the provider and optionally add (5); retain the same vacuum.
   Reject invalid provider status, nonfinite components, nonpositive a/H or
   nonpositive total density. Propagate failure through combined_bg_rhs and
   the initial-time endpoint calculation, rather than merely returning NaN
   and hoping the ODE notices. Reject unused external/custom branches at the
   candidate initializer. Do not let old file-output diagnostics report a
   fictitious residual CDM component; those functions are not invoked.
3. Build every module against the same derived header; do not accidentally mix
   old/new CPRBackground layouts. The material context outlives the background
   and is not freed by cpr_background_free. No process-global state is needed.
4. A new stdout-only adapter accepts only pinned state records and fixed
   declared branches. Record all matter/thermal components, current/stress
   derivatives, reference-energy correction, a/T/t/rates, accepted nuclear
   rows and all failure states. Keep the original cache fingerprint checks
   after parameter setters; changing T0/omega_b is not permission to regenerate
   a mismatched table. Use provider orders64/128 for material refinement,
   not an extra adjustable equation of state.

The nested matched controls, at each row's *same* physical constants, are:

| Branch | H matter prescription | Purpose |
| --- | --- | --- |
| L | original CDM, original baryon-H omission | row-matched legacy reference |
| D0 | ideal-dust provider, same omission | exact replacement implementation identity L=D0 |
| D | ideal-dust provider plus (5) | isolates the baryon-H reconciliation from D0 |
| S | finite same-state provider plus (5) | S-D isolates the retained finite-pressure history |

The already frozen ordinary baseline is a separate qualification, not another
fit. All335 inherited histories/1340 calibration labels remain the declared
eventual census, including the40 ideal-dust and295 finite histories; duplicate
soft-quadrature copies may share a background only under the already proved
same-normalized-action identity, with every physical R/S/gstar label retained.
The old fixed case8 remains an exposed implementation benchmark, not a newly
chosen scientific representative. A finite branch cannot silently be dropped
because its rate/H ratio or abundances are inconvenient.

Ordinary nuclear positivity, baryon-number conservation, default/refined
abundance controls and raw signed failures carry forward unchanged. Add the
provider's existing action/virial/current checks, (2)/(5), L=D0 at common
thermal nodes, the identical a(T)/rate functions, and (8)--(10). Background-grid
and material-order comparisons remain separate from nuclear tolerance
refinement. Freeze their precise numerical tests in the additive executable
protocol before running; this analytical plan introduces no outcome-dependent
threshold or favorable-abundance success gate.

Provider a=0/extrapolation is forbidden. The finite background/ODE-stage a
domain must be explicitly covered before evaluation, with an out-of-domain
status retained rather than a dust/radiation fallback. Preserve nuclear start
composition at its declared finite10MeV slice and the40MeV background interval;
actual weak/H and integrated n/p contraction are readouts, not automatic proof
that every altered history has forgotten all possible initial states.

## 5. Implementable abundances versus unearned thermal qualification

For the supplied NEVO functions, let rho_nu,T denote their actual interpolated
temperature derivative. The implied ordinary energy exchange is

    Q_nu/H = 4rho_nu - T(3sigma+N_heat)rho_nu,T/C_src,
    Q_EM/H = 3(rho_EM+p_EM)
                         - T(3sigma+N_heat)rho_EM,T/C_src. (11)

The scalar residual from (1) is identically zero. The table prescriptions fix
Q_nu/H, not the neutrino collision response to changed H. Record the signed
ordinary residual Q_nu+Q_EM, preserving actual interpolant/supplied derivative
differences. A small residual shows neither correct neutrino spectra nor
correct weak collision integrals in the new background.

Thus S yields implementable **conserved-scalar, prescribed-NEVO conditional
abundances**. It is more specific than the old nonconserved table-proxy score,
but not self-consistent modified-decoupling BBN. The next independent physical
qualification needs either ordinary neutrino energy/spectral transport with
this exact H, or a justified response bound on both reheating and weak rates.
A small Delta H/H alone is not such a bound. Instantaneous decoupling may be
a labelled sensitivity branch, not an assumed conservative bracket. The
upstream `Neff` output remains an ordinary-neutrino readout, not the scalar's
energy or a constant-free-streaming CMB parameter.

No observational score is produced here. Preserve the exposed D/H and helium
products and marginal-only covariance treatment. The335 states originated in
proxy inverse calibration; carrying them forward is an exposed retest, not
held-out confirmation. Re-inferring omega_b or R from S would require the same
shared-energy/vacuum recalibration and propagation into other observables,
not a separate radiation-amplitude fit. Photon thermal origin, CMB angular
perturbations and primordial initial-state generation are different questions.

## Bound read-only inputs

Primary source: PRIMAT commit
`4bf97d5082eee54b9df50d88f43182bb651fea80`; its exact selected files are owned
under `bbn_inputs_v001/primat_c_reference_v001/upstream/`. This plan checked
the actual setup, Friedmann, combined entropy/time RHS, endpoint, eta/mass and
provider interfaces, not only public function names.

| File | SHA256 |
| --- | --- |
| PRIMAT_CONSERVED_SCALAR_IMPLEMENTATION_ROUTE_V001.md | d7639dbb626359da4a96229f69a687f88c11e2d81111831ebaab281b44aa079b |
| PRIMAT_ORDINARY_BASELINE_PROTOCOL_V001.md | f316e483e125a2bbb3076baf3c13eb21242a983b8df43668f600eaf05cff7af1 |
| unt_hard_barotrope_v001.h | abfade89af77e4000bccd169c1ea18226315621f7dcb665901efa879e3a4aab6 |
| unt_hard_barotrope_v001.c | 3003b89d4dcd14a599cf924390b6b4a2151bb14e4221a2336458d89509a3c39d |
| upstream/primat-c/include/background.h | 5ced6cd5d02393f4f1b2b9a250a6709f64f1ac823394098d3419504b89ee5eae |
| upstream/primat-c/src/background.c | d692a9c810d65b2711ebe7aa246c317c0284428305463c0534bf742b8f675064 |
| upstream/primat-c/src/config.c | 6f6d369eb2cc3adac70f5916dd6eca6a427db8779bc5d77054f53f82bfad76bb |
| upstream/primat-c/src/constants.c | ea97c872858bb103a6479ce42cc60c7b61865ac3981dc3275917acb2618403f2 |

No change to those bound bytes, no new abundance result and no physical
qualification beyond the explicitly adopted scalar/prescribed-thermal model
is asserted.

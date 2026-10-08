# Same-state finite-gap photon-density comparison V001

2026-09-29. Prospective saved-arithmetic extension of the already derived
quartic radiation identity, not a new orbit, fit, CMB spectrum or BBN run.
Use all 360 calibrated rows of FINITE_GAP_SHARED_SCREEN_V002_TRANSPORT.json,
all five gaps and all 18 inherited references with all four soft quadratures.
No selection by the newer finite-field result is made.

The explicitly adopted scalar FLRW candidate has soft ground modes and one
hard population of weight beta=.005, with conserved action I(A)=A^3 I(1).
The exact same-action high-density coefficient is

    C=[(3 sqrt(pi)/2) Gamma(3/4)/Gamma(1/4)]^(4/3),
    Q=beta C I(1)^(4/3), D=beta R^2 sqrt(C I(1)^(4/3)),
    Q <= E(A)/A^4 <= Q+D/A^2.

These identities, proved in SAME_ACTION_RADIATION_ASYMPTOTE_V001.md, apply
to the newly specified scalar states as well as the earlier separately owned
states. Do not relabel either family as the other. Q and D are fixed by the
saved actions, not fitted extra populations. The matched vacuum is unchanged.

Use each row's inherited Omega_exc and the matching reference's Omega_gamma
from the authenticated RADIATION_PHOTON_REFERENCE_V001_RESULTS.json. That
receipt derives the photon reference from the measured temperature and pinned
SI constants. Reuse its central values and declared scope, not a new current
observation. Report

    asymptotic ratio = Omega_exc Q/(E_present Omega_gamma),
    at A=1101 ratio = Omega_exc E(1101)/(A^4 E_present Omega_gamma),
    upper difference bound = Omega_exc D/(A^2 E_present Omega_gamma).

The second expression uses the already saved exact finite-gap E(1101), not
an extrapolated quartic estimate. Also retain the same-pressure early w and
the formal sufficient A=sqrt(D/(epsilon Q)) for epsilon=.01 and .001.
Those two epsilons specify approximation accuracy only, not observational
acceptance. They are not new epochs at which dynamics are run.

The asymptotic coefficient describes this explicit scalar fluid's conditional
continuation. An early physical application still requires that this effective
description holds in that domain. Ordinary photon A^4 dilution is an explicit
comparison assumption, not an explanation of photon production. In particular
this calculation cannot serve as evidence for the separate continuous-network
thermal-origin hypothesis, which must supply its own exchange/temperature law.
There is no neutrino conversion, N_eff threshold, CMB likelihood, primordial
abundance prediction or exclusion assigned by this diagnostic. A material
early contribution requires self-consistent thermal/expansion treatment, and
standard-BBN-derived baryon reference values are not independent confirmations.

Controls, fixed before the new arithmetic: reproduce C using the independent
Beta-function Gamma identity; reconstruct each photon Omega from its constants
and inherited H0; exactly match all reference labels and H0 values against the
old calibrated receipt; reconstruct present and A1101 action/energy labels;
check the exact finite-A bound with relative allowance 2e-11; verify all 360
labels and complete family ranges. Preserve all control failures, with no
changed thresholds. No observational pass/fail is attached to a density ratio.

The stdout-only stdlib worker authenticates the old compressed result, full
recursive frozen lineage and photon receipt/its mathematical notes. It freezes
its own source and this protocol before arithmetic. Root publishes exact stdout
with apply_patch. The anticipated output is comfortably below 1 MiB; no job
checkpoint or numerical-library allocation is needed. An independent saved-
arithmetic audit follows; it need not rerun any orbit or scientific producer.

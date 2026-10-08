# Dark-sector frontier V012 — formed records and carrier response

2026-09-27. This turn connects native record feedback to a moving carrier in
both an exact prepared-state calculation and a retrospective analysis of the
existing writing/hold experiment. The full dark-sector goal remains incomplete.
No old formation run was repeated and no earlier matching failure was changed.

## 1. A response in the actual formed-state calculation

The resident original RESULTS.json still matches its completion-manifest hash
`f9568066e1b9e31e60cc3fb58c782a612236b005e65c7a4c62736995b964bf7f`.
Its Q arm writes at L0 and R0 from blank targets, keeps every outcome and all
correlations, and then turns writing off. The comparison native_Q versus
hold_only_zero_Q uses the SAME complete formed initial state; the latter
removes only record–incidence feedback during hold. It removes that feedback
at BOTH written targets, not just R0.

The fixed readout is D=N_R0-N_R1, where R1 is never written. The following
table reports every originally frozen hold time. Values are rounded here;
the reanalysis JSON retains the input precision and all six original arms.

| Hold time | D, native Q | D, same-state control | Native minus control |
| --- | ---: | ---: | ---: |
| 0 | 0.000667889062 | 0.000667889062 | approximately 0 |
| 0.25 | 0.002273427941 | 0.002186329564 | 0.000087098377 |
| 0.5 | 0.005004954120 | 0.004380114853 | 0.000624839267 |
| 1, original primary time | 0.009031827442 | 0.007207996123 | 0.001823831319 |
| 2 | -0.011706285487 | 0.005370576733 | -0.017076862221 |

This is a feedback-dependent write-target access bias in a state actually
produced by the model's writing dynamics. It reverses later. The table does
not establish sustained attraction, trapping or a spatial force, nor does
that reversal by itself disprove a possible macroscopic gravity mechanism.

The null right-site contrast for P arms and whole-schedule zero-feedback Q
holds within a maximum residual of 3.3306690738754696e-16. Whole-schedule
controls are not substituted for the same-state comparison. The latter's
feedback removal costs +0.49978700205904636 in the existing energy ledger:
native and control hold energies are 6.001826932461665 and 6.501613934520704.
Equal initial density does not mean equal Hamiltonian energy or free switching.

This readout is retrospectively selected, and the positive primary contrast
and later reversal had been inspected before the extraction protocol ran.
It is NOT blind validation. It is also target-anchored, not the joint readout
q_R0*(N_R0-N_R1). The archived STATES.npz is currently dataless and was not
read; its missing joint information was not reconstructed by multiplying
marginals. The old P/Q count/energy/feedback matching gate remains failed.

## 2. An exact identity explains how retained records enter that response

For a fixed carrier destination set S, the native inward current is

    I_S=(t_hop/hbar) sum_e delta_S(e) n_e J_e.

Let F=-lambda_R sum_e(q_u+q_v)n_e be the complete retained-record feedback,
and compare H=A+F with A using the same initial state. F commutes with both
P_S and its first commutator. Therefore carrier-probability derivatives of
orders zero, one and two are identical under the two holds. The first possible
change is the exact third derivative

    Delta <P_S>'''(0)
      = (h*t_hop*lambda_R/hbar^3)
        sum_e delta_S(e) <(q_u+q_v) X_e J_e>_initial.

This is a joint record–link–carrier correlation, not a product of separate
record, link and current means. All terms come from the existing native action.
For a real or freshly localized carrier preparation the cubic contribution
vanishes. The actual complex formed state need not have that restriction.

The original stored derivatives obey the order 0–2 identity exactly at their
reported precision. For D, the third-derivative difference is
0.03136359568457131. At the frozen coefficients h=1, t_hop=1/2,
lambda_R=1/2 and hbar=1, the identity therefore infers

    <q_L0 (X_00 J_00-X_01 J_01)
       +q_R0 (X_00 J_00+X_10 J_10)>
      approximately 0.12545438273828524.

This number is inferred from the stored derivatives and the proved operator
identity. It is not a new direct measurement of the inaccessible joint state.
It involves BOTH retained writing targets. The coefficient of time cubed in
the probability difference is the third derivative divided by six.

See [fixed-source current and equal-state control](NATIVE_FIXED_SOURCE_CARRIER_CURRENT_V001.md).

## 3. Independently checked preparation dependence and opposite signs

A separate exact calculation uses a supplied occupied record at R0, an empty
graph, and a carrier at L0. This does not reset or replace the actual formed
state above. All four incidence qubits remain dynamical. For

    a=Delta+2U-4U*d_star+lambda_J,

the exact leading R0-minus-R1 probability coefficient is

    h^2*t_hop^2*lambda_R*(2a-lambda_R)/(72*hbar^6).

The first unequal term is time order six; the order-four arrivals are equal.
Depending on detuning, native record feedback can move the source-side link
closer to OR farther from resonance. It does not enforce one sign of access.

Two prospective fixed parameter examples gave coefficients +1/144 and -1/144.
An independently implemented rational matrix-action check verified both,
source-swapped sign reversal, zero-feedback symmetry and complete probability
normalization through sixth order. All six fixtures passed on the full
64-state space, with no graph-outcome selection, fitted tolerance or eigensolver.
Source swapping within each example preserves complete initial energy.

The [word derivation](NATIVE_RECORD_ANCHORED_CARRIER_ACCESS_V001.md) was obtained
independently of this implementation and retains the current-squared term.
Neither its early-time sign nor a static negative record insertion energy is
a universal attraction theorem.

## 4. Evidence, review and execution

The single root-owned worker combined the new exact check with read-only
extraction of existing outputs. It did NOT propagate the old formation state,
repeat its 889 checks, or read the dataless state archive. It exited 0 under
an eight-second alarm; measured internal runtime was 0.044662916 seconds,
peak process RSS 19,185,664 bytes on Darwin/Python 3.9.6. No further numerical
attempt occurred. Source/protocol hashes matched their pre-run freeze afterward.

- [Frozen protocol](native_sourceward_access/PROTOCOL.md), SHA256
  `8c7fc1195db8032982e9c7721b7fcd5c8eb8b0ba0ae59965070aa744baf76dd5`.
- [Worker source](native_sourceward_access/check_access.py), SHA256
  `8f1b0011c83c9d7c3a45b74038aa03c66b4b1ca48d44003e2fb543f585107001`.
- [Complete result](native_sourceward_access/RESULTS.json), SHA256
  `1343f8dd019cac94ab9e16099178e44b54aca04062eff5450f249c6e78603506`.
- Current theorem: SHA256
  `89c800626eb705b2d2735ddd87ccf3b7208ce6cfaf68eb16a62e3b71995d59df`.
- Word expansion: SHA256
  `51e1cdfcb49fe541c30dff5472527da7d5c1415cf9a5f3e77cbfd610a7df2c25`.

The result JSON was saved directly from the worker's printed JSON through
the file-editing tool. Hashes identify bytes; they do not convert a finite
model into empirical evidence. The inherited numerical residuals are
diagnostics, not a new certified total simulation-error or observational bound.

The budget-derivation agent independently checked the word expansion, including
remote-edge cancellation. The assertion reviewer read the final current note,
protocol, source and results; it accepted the signs, hbar powers, exact rational
checks and retrospective interpretation without requesting corrections. The
root read both analytical notes and checked the matrix action, energy ledger,
inclusive readouts and stored-input identity. No review licenses gravity or
dark-sector claims beyond these specified results.

## Next scientific decision

The formation-to-later-response connection is now explicit at this finite
scope. The next useful discrimination is an actual-occupation-weighted readout
and a source-specific control, followed by a declared criterion separating
transient routing from a robust physical response. Use the archived complete
state if it becomes resident; if a fresh same-rule reconstruction is needed,
declare it as a new bounded experiment with its own readouts and custody, not
as recovered original bytes or a silent rewrite of the old run.

The primary allocation law, physical volume/stress, abundance, macroscopic
transport/scaling, perturbations and observational tests remain unclosed.
These results do not impose proving all gravity before useful conditional
dark-sector tests, and do not replace the primary active/maintenance construct.
No heavy computation, L8, remote dispatch, failed-production retry,
infrastructure change, package installation or publication occurred.

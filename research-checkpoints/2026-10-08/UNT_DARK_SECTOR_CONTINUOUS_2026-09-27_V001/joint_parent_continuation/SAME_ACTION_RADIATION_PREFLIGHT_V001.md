# Same-action radiation arithmetic: independent preflight

2026-09-29. Complete source and protocol review before the producer run.

Reviewed identities:

* `same_action_radiation_v001.py`:
  `b514d676cddb11943d693fa4eadaaf26edaa6d46b773af8614765554f8c67ea2`.
* `SAME_ACTION_RADIATION_PROTOCOL_V001.md`:
  `8034fcd19675ebfacb411a098e1f45f014161b1dd856408b26141e6ec5e68157`.
* The analytical note and its coefficient/bounds were separately accepted in
  `SAME_ACTION_RADIATION_ASYMPTOTE_REVIEW_V001.md`.

**Accepted; no execution or import of the producer was performed by this
reviewer.** The settled resolver skips an invalid out-of-project candidate
while still requiring one unique valid in-project interpretation and its
exact frozen hash. This is a custody clarification, not changed arithmetic.

The complete saved original and pulse states, ancestral frozen files,
payloads, statuses, state/action/spectrum identities and dilution/calibration
censuses are checked before numerical work. Original history lookup keys
agree with the returned-row keys. Pulse modal actions and energies are the
saved fine endpoint, not a ground-state or harmonic substitute.

Independent source inspection confirms both Gamma forms, positive weighted
`Q,D,S4`, the soft/hard partition, zero-action representation, and all four
signed finite-gap residuals. The one-sided control arguments have the correct
orientation. The fixed counts are 42 states, 4,614 modal entries, 252 old
dilution rows, 648 original calibration mappings and 108 expressly conditional
extended-spectrum reference mappings. All six A values are retained in each
reference row.

The physical cross-check uses
`2 gstar^2/[3 Kb (c H0)^2]` as the stress-to-critical-density multiplier;
its products with the saved `E1` and the new radiation `Q` correctly yield
`Omega_exc` and the predicted conditional asymptotic coefficient. The old
calibration's vacuum endpoint `Q` is not confused with this new moment.
No ordinary-photon number or fit enters this producer.

Prospective algebra, inherited-state and inherited-calibration tolerances
remain distinct. Outcomes cannot pass because a radiation fraction has a
preferred size: only custody, census, algebra and the proved certificates
are tested. Oversized output is labeled, not truncated by the producer.
Stdlib-only execution prints JSON and performs no filesystem writes or new
orbit/dynamical calculations. A saved-result audit remains necessary after
the parent runs it.

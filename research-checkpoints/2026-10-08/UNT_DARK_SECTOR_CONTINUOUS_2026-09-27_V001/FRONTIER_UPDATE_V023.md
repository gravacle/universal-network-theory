# Frontier V023 — an actually formed shared-record state supplies one response

2026-09-27. Continuation of V022 in the BS parent. Numerical and analytical
identities now connect actual shared-record formation, inclusive connectivity,
record insertion-work coefficients, and fresh-carrier motion. This is not an
import of the separate H6 transport Hamiltonian.

## The tested bridge

Three complete N=2 formation states were prepared at the predeclared times
T/2,T,2T, T=323.0882195178482. All four native link flips, the actual q-state,
and all basis outcomes were retained. Copying was then switched off with
its work included. No state was reset, cooled, postselected, or replaced by
mean occupations. The numerical tests reproduced the earlier sealed
formation observations before using these states for new predictions.

For each actual held state, one 4-by-4 edge response matrix chi_ef predicts:

1. The changes of record insertion-work coefficients under an independent
   record-equivalent diagnostic source.
2. The changes of freshly injected carrier transfer curvature under that
   same source, checked through the full 128-dimensional carrier-plus-network
   Hamiltonian's projected first-order amplitudes.
3. The response to a homogeneous incidence source, without fitting a second
   response function.

The edge kernel was checked independently with finite projector kicks.
Vertex and total-incidence sources used their proper nonprojector kicks
and fourth-order centered Richardson derivatives. At fixed blank vertices
the record coefficient is an insertion-work coefficient; at the other
vertices it is only a coefficient field. All diagnostic kick work is saved.

Across three formation arms, 2,016 checks passed, maximum residual
1.95504446e-11 against a frozen 1e-8 numerical tolerance. The measured worker
runtime was 0.0894 seconds and peak self RSS 33,488,896 bytes. Separate fsynced
arm receipts and hashes support clean continuation; an actual interrupted
restart was not tested. Two independent agents reviewed the complete source
and protocol and found no mathematical/indexing blocker.

The source is `formed_network_response/compute.py`, SHA-256
`73515a9dcb091f55dd879497961fe1d8ffb80c11e01c34ec4b9b32c8e243698f`.
Its freeze SHA-256 is
`7d01a3083f9bc6353f61c832e229eecd1a6b9b6483b2a786cd6abe21dd75c3e1`.
See that directory's `PROTOCOL.md`, `RESULTS.json`, and `half.json`,
`one.json`, `two.json` for every arm and kernel entry.

## Records persist while network connectivity evolves

Record occupation is conserved after copying is stopped. Connectivity is
not. In the 2T formation arm, q occupation stays 0.9158430786. The inclusive
joint probabilities for q occupied AND connected to the original record
site or the other donor are:

| Hold age | Original record site | Other donor | Difference |
| --- | ---: | ---: | ---: |
| 0 | 0.620386 | 0.350477 | +0.269909 |
| T/2 | 0.678885 | 0.343644 | +0.335241 |
| T | 0.681750 | 0.393723 | +0.288028 |
| 2T | 0.546498 | 0.601284 | -0.054786 |

Connectivity includes all three-edge alternatives and changed background
rows, independently checked by graph reachability. These two events overlap;
their probabilities need not sum to q occupation. Both/only-one/neither/blank
outcomes are separately recorded and form a complete normalized partition.
The T/2 and T formation arms remain negative on this hold grid. Thus the
later formation arm's connected preference survives substantial selected
holds, but does not become permanent. No finite grid establishes all-time
behavior. Measured copying-off work is respectively 0.01898857017,
0.01754853963, and 0.02663471001 for the three formation arms.

This distinction provides a useful mechanistic interpretation: persistent
record occupancy can coexist with evolving operational connectivity and
carrier response. Treating preserved records as a frozen geometry would
discard actual native dynamics.

## Preparation history remains observable

The same-kernel test succeeds without requiring a fixed response sign.
For example, after formation at T the uniform kernel at lag 2 is
+0.01467769827 at hold age zero and -0.002018245221 at age four. These are
finite two-time impulse-response values, not static susceptibilities or
cosmological acceleration. Their sign change makes the next question precise:
what response follows from an explicitly specified ensemble of formation
ages, as distinct from replacing the network by an assumed passive ground
state? The actual ensemble must retain its prepared energy populations.

The native carrier curvature also differs from deterministic mean-link
hopping by exactly t_hop^2 times the sum of incident edge variances. This
was measured independently through projected carrier amplitudes, so mean
occupation alone is not a valid replacement for the operator dynamics.

The one-link noise and preparation-derivative predictions in the separate
analytical notes are not tested by this worker. No L6/L8 calculation, remote
dispatch, package installation, infrastructure/account change or publishing
was done.

## Analytical scaling advances reviewed after V022

Independent review now accepts Sections 6 and 7 of
`NATIVE_OVERLAPPING_RECORD_PAID_FORMATION_V001.md`. The exact conditional
many-donor star reaches total one-edge/record success 1-O(1/N) in
O(sqrt(N)) time for m proportional to N, provided its collective coupling
is sufficiently small compared with the specified fixed-g spectral gap.
Success is still divided equally among eligible donors. This theorem is
not a bound on the omitted full-slab background dynamics.

Separately, a complete native energy/degree estimate bounds the expected
link count by O(1), uniformly in time and N, for the one-existing-record,
one-active-writer family. That is a full-native sparse-preparation bound,
not a finite-density network-formation theorem. Both results make the next
collective test more explicit without changing the underlying terms.

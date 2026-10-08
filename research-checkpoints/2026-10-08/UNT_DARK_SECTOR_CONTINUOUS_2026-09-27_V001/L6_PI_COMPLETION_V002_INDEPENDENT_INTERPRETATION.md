# L6 pi completion V002: independent interpretation

2026-09-27. Read-only source/algebra review; no import, extraction, scientific calculation or rerun. After checking resident flags, read archive members under `UNT_L6_PI_TRANSPORT_COMPLETION_RESULT_V002/`: scientific report; V002 `phase_facade.py`, `SOURCE_REVIEW.json`, `PROTOCOL.json`, `CAPTURE_EVIDENCE_REVIEW.json`, `PROSPECTIVE_MATCHED_DEPHASING_REVIEW.md`; and mechanism V001 `ALGEBRA_REVIEW.md`. Whole-archive custody and table arithmetic are the root reviewer's separate work.

## Correction and new result

Facade bytes hash to `2feebea605534842d9494189bea0e1b1e71800c848b3093d92d3f36450f4a63e`, matching the report. For nonnegative integer k, `(1,-i,-1,i)[k%4]` is exactly the intended phase. The source retains Bessel amplitudes, normalization and strict operand/axis guards; it does not project observed coefficients. Recorded order-101 telemetry attributes the offending real component to complex exponentiation, not a complex Bessel amplitude. I did not independently reproduce that floating arithmetic or qualify the full dependency tree.

The new reported science is a fresh complete pi transport census and its cross-implementation/refinement checks. The 66 admission covariance identities and pi/4 census are preserved earlier results, not newly independent replications. The implementations share history inputs. Agreement remains empirical numerical screening, not certified forward error or a new physical law.

## What the proposed dephasing test isolates

Let D be the fixed joint product-occupation dephasing and P_q(rho)=rho_G,q tensor rho_C,q/p_q. Partial trace commutes with this local D, so D(P_q(rho))=P_q(D(rho)). All diagonal joint probabilities and sector weights survive. Therefore the established immediate-admission prediction, sin²(phi) times the weighted occupation covariance, is unchanged exactly; its success alone does not require occupation-basis coherence.

The later difference between matched signed responses tests off-diagonal entries of rho-P_q(rho). Keep all four actual/product, original/dephased arms and every output sector. A nonzero answer establishes basis-relative coherence sensitivity, not entanglement or quantum advantage. It is not a control holding both full marginals fixed. Admission/transport may themselves generate new coherence. A null answer only limits these readouts at these times.

No blocker in that limited proposal. Dephasing generally changes energy as well as full marginals: record pre/post intervention energies before treating it as an energy-matched or physically free resource control. Its mixed-state cost must be prospectively bounded.

This discriminates an existing finite correlation-transfer mechanism. It supplies no spatial force law, stress/pressure, abundance or common dark-matter/dark-energy dynamics, and is not by itself evidence for their joint network explanation.

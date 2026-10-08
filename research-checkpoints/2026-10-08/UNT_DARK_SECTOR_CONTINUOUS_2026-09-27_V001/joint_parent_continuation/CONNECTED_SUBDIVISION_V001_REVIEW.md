# Independent connected-subdivision result review V001

2026-09-29. Outcome: **accepted within the frozen clamped-controller, blank-register model; no implementation or numerical blocker found.** The full source and protocol were read. This review authenticated saved products, independently checked the algebra and recombined all saved probability/work/bound data. No propagator was rerun.

## Exact identities and qualification

| Artifact | SHA-256 |
|---|---|
| `connected_subdivision_v001.py` | `4f63a76c9f84313c456ea07c1cc09f889736d07f62dcfbc79c266d58ea9b539e` |
| `CONNECTED_SUBDIVISION_PROTOCOL_V001.md` | `34ae3dbef530bd1d466e8e72ebb626afb97a3199e22514628b8de1532e6fdf6f` |
| `CONNECTED_SUBDIVISION_V001_FROZEN.json` | `6d0fea9e39623f48e1381dfdd66e4e9bb891ec731ab1e80a2eb4fb252e75a6ec` |
| `CONNECTED_SUBDIVISION_V001_RESULTS.json` | `5257b5403af280a868b848f2831677c2426dc8fbbee21d95812dcd7b4da0d5d0` |
| Canonical result payload | `f5e4892715ce55613fd11d6dce2e9bd695d62fa2979fd02e5c814c7dc9d27149` |

All ten frozen inputs match, as do configuration, canonical payload and result-to-freeze link. The complete prospective census is present: four inputs at four zero-port times and five times for each of the two positive strengths, totaling 56 distinct rows. All 608 checks pass; failures are empty. Reported elapsed time is 4.159101083 seconds and peak **self** RSS 96,976,896 bytes.

The dense native builder retains degree-square constants and is checked against an independently expanded degree polynomial. The port is rank eight, not an isometry on all 16 old states. It retains all old native flips during evolution, including those that feed eligibility from an initially absent anchor. The source jump is two occupied links. The full partial-domain intertwiner, two leakage Gram identities, permutation covariance, source-response double commutator, current and initial transfer coefficient are implemented with the accepted signs and normalizations. The full intertwiner's saved maximum entry discrepancy is `2.7755575615628914e-17`; the complete response-operator comparison is exact at floating-point precision.

The 528 dimensions are explicitly the invariant old/excited-supply plus new/empty-supply **charge-three block**. The numerical equality of charge to three inside this block is not an independent test on the omitted charge sectors. Its legitimacy follows from the analytical Hermitian port's `[H,n_size+n_supply]=0`, already reviewed; no eligibility subspace is similarly projected away.

The independent sparse action uses XOR native flips and port gather/scatter, not the dense eigensystem. Its fixed-probe discrepancy is `2.0097183471152322e-14`; evolved vector differences are at most `3.762509047503653e-14`. The scaled-Taylor product error bound uses the correct `expm1(sum(log1p(tail)))`; its maximum `2.448136925702684e-16` is a truncation-only bound, not the observed floating-point error. Maximum total-energy discrepancy is `1.6342482922482304e-13`, below the unchanged `2e-9` gate.

## Saved-data checks and outcomes

All eight eligible basis mappings preserve component count and cycle rank, add two edges and two vertices, and possess exact reverse support. Specifically the connected cycle `15 -> 350` changes diagonal native energy from 20 to 30. The added nodes do not join previously disconnected old components.

This review recomputed all 56 sector and Q partitions, connection partitions, supply energy `11.6 P_old`, elastic energy `.25 P_old+2.05 P_new`, all energy changes, both bound formulas and total ledger sums. Their largest arithmetic discrepancy is `7.105427357601002e-15`. The initial full energies for cycle, tree, coherent cycle/tree and empty inputs are respectively 31.45, 25.55, 28 and 15.85. Source and interaction energy have not been dropped.

At the **prospectively chosen** strong-port swap time `t=pi/16`, the results are:

| Initial state | New-size probability | Exact target-Q/reverse support | New-size and connected probability |
|---|---:|---:|---:|
| Cycle | 0.9960864245 | 0.9871541573 | 0.9958877392 |
| Tree | 0.9960814379 | 0.9869198253 | 0.9788539976 |
| Real cycle/tree superposition | 0.9961040071 | 0.9870569879 | 0.9867702744 |
| Empty, initially ineligible | 0.0038633674 | 0.0038508124 | 0.0000006810 |

The exact-Q lower bound for eligible inputs is 0.9331811109, and all three satisfy it. The separate backbone leakage bounds also hold. New-size, exact reverse support and connectedness are different observables and are not substituted for one another.

The weaker port, epsilon=1 at `t=pi/2`, transfers 0.9893155–0.9899502 of the three eligible preparations to the new size. The general state-uniform bound is zero there and is retained as uninformative; observed high transfer does not retroactively strengthen the proof. Ports-off gives exactly zero new-size probability at every retained time.

Growth is **reversible and not permanent**. At epsilon=1, time 2, all three eligible inputs have negative creation current (approximately -0.702 to -0.692). At epsilon=8, their new-size probabilities fall to 0.217–0.378 by time 2. Initially empty input can later acquire eligibility through native flips; at epsilon=1,time2 its new-size probability is 0.1139018969 but its joint new-size/connected probability is only 0.000120692. This is not spontaneous reliable assembly of a connected network from blanks.

The strong-port cycle example explicitly debits 11.5546025237 supply-energy units at the swap readout. Native energy rises 9.9183647360, elastic energy rises 1.7929555640, the source contribution changes -0.1969675326, and interaction energy is +0.0402497563; these changes close the ledger. The corresponding terms remain saved for every input/time, including unfavorable outcomes.

## Scientific conclusion

A finite, reversible, explicitly powered local subdivision port can transfer an already-connected native incidence state into a larger connected graph with high probability, while retaining native leakage, source work and reverse support. This resolves the immediate weakness of blank-pair insertion **for this declared port**. It is a constructive controlled-growth result, not a proof that the existing BS copy dynamics generates the port or its supply.

All physical registers are blank and the source/volume coordinates are clamped. No new record-production law, piston trajectory, physical length, continuum metric or cosmological expansion rate was tested. The separately reviewed local-probe ruler note identifies the next measurable distinction between physical stretching and representation refinement without changing this successful frozen calculation.

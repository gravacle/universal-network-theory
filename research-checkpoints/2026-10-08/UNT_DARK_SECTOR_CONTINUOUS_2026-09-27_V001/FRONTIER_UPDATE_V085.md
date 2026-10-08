# Native response bounds and repaired helium arithmetic controls

2026-09-30. Continuation of V084 under the explicitly adopted V004 handoff.
All eleven lanes remain OPEN; Stage 3 and the dark program are not complete.
The old continuation schedule remains PAUSED and the receiving research Goal
is active. Root is the sole numerical executor; no scientific child is live.

## Substantive native result

The native-source analysis now has three independently reviewed exact results,
not a new finite-size spectrum sweep. Paths below are in joint_parent_continuation.

1. NATIVE_REGULAR_GRAPH_UNIFORM_SOURCE_BOUND_V001.md establishes an exact
   full-parent isolated-low-band weight bound in its STRICT regular-phase
   parameter domain. At fixed microscopic coefficients, bounded-profile weight
   is O(1), and fixed-node anchored weight is O(1/N). The explicit band-isolation
   inequality is essential; the inherited Omega=U=1 choice is NOT silently in
   its uniform domain. This bounds fixed-time and positive imaginary-frequency
   response, not undamped resonances or static inverse gaps by itself.
2. NATIVE_DEGREE_TIE_PROJECTED_SOURCE_BOUND_V001.md proves W_anchor<=Omega^2/(4N)
   and W_u<=Omega^2 Q_u/[4(N-1)] in the exact first-tie projected matching model.
   The first-order collective ladder does not by itself remove source suppression.
3. NATIVE_DEGREE_TIE_PROJECTED_STATIC_BOUND_V001.md identifies the ENTIRE
   ground-to-excited node-source sector, not merely the radial block. The exact
   standard block has b_m=sqrt[m(N-m)(N-m-1)]. A padded Perron comparison gives
   every source-visible gap at least Omega sqrt(N)/[sqrt(2)(N+1)], hence

       chi_anchor(0) <= Omega (N+1)/(sqrt(2) N^(3/2)).

   This closes the anchored static inverse-gap exception within exact PHP.
   An extended bounded profile has only an O(Omega sqrt(N)) static bound.
   A growing physical radius and independently defined volume can change the
   response-density scaling; no universal physical static no-go follows.

These restrict particular proposed mechanisms. They do not refute all UNT,
derive a galaxy-edge law, establish formation into the assumed ground state,
or explain DM/DE away. At the degree tie, the matching projector is not invariant
under the full parent; source dressing, contacts and a uniform eliminated-sector
bound remain missing. No record count has been identified with physical mass
or volume. The old finite N3/N4/N5 oracle remains unimplemented and unrun; these
proofs answer the growing-size questions more directly than that histogram.

Reviewed identities:

| Note | Author SHA-256 | Independent review SHA-256 |
| --- | --- | --- |
| Strict uniform source bound | 0d4785027238d9c3e69662fd918888ebf1769d435a26b7e5f2b049802fd7a2c3 | d7b22e08793b217007c213907c9d696891f7dd491f7ecc9d9172ece463ee796d |
| Projected tie weight bound | 77a80c2c28c1eded98190f82bb3f98994d2bd24c4150ea30180263ede48c092a | 18d65e8c2bbdf616067628638e5b902f1637ef8a34d87a8451bda849e7f4047b |
| Projected tie static bound | 57530e06b99ad9608dc8afde899804884947402eafb7d7860813b875ac1887de | 2e05e96684ba7d2541f445f064b5059084749a2c9e7868fe923ba12c9160b4c4 |

## Helium V002: finite synthetic PASS, old failure preserved

After independent helper, algebra/interface and controller preflights, root
froze the new representation and performed one bounded compile and one serial
C-then-Fraction control run. There was no scientific worker overlap. All 18
frozen sources remain unchanged. The original V001 failed run, its seven failed
checks, all criteria and raw streams remain intact; no retry replaced it.

The new packet uses cancellation-resistant species flows and explicit high/low
derivative limbs. An independently authored exact-rational oracle differentiates
the captured binary64 state inputs through different algebraic expressions.
No root/Saha constant/rate law or physical approximation was fitted or changed.

- 36 fixed cases; 630 C checks, zero failures; 26 complete state captures.
- 764 independent Fraction checks, zero failures: 232 coefficients, 182
  individual derivatives, 182 limb normalizations, 78 conservation checks,
  78 reported-residual checks and 12 primitive checks.
- All 26 predecessor scalar-state and 14 source-rate comparisons pass bitwise
  in the new same-translation-unit build. This is not a replay of the old binary.
- Maximum saved individual-jet absolute error is 6.968774511767307e-26 against
  the exact expressions of represented inputs; maximum represented charge-sum
  residual is 7.444442536576011e-26. These are arithmetic, not physical errors.
- All 42 raw high-only checks remain visible. Two source-RHS charge sums at
  z4200/n0,n1 fail: -3.358167910416654e-12 and -3.1107876691249814e-12 against
  unchanged 5e-13. Consumers that discard low limbs do NOT inherit the PASS.

Artifacts under joint_parent_continuation/class_candidate_v001:

| Artifact | SHA-256 |
| --- | --- |
| HEIII_OVERLAP_CONTROLS_V002_FROZEN.json | 9c85c04e61b7e5f51a48a9799e0b472459e0d08b16c510004d4bcc6d75913655 |
| HEIII_OVERLAP_CONTROLS_BUILD_V002.json | 5d90862cfcbee56ce792b2f4f71bbe52ac915970bcfc3fe63357455799b419e4 |
| HEIII_OVERLAP_CONTROLS_RUN_V002.json | d6307af7a98415cbb57ca8bfa456d531e48329276b989e61007463db5b5400bf |
| HEIII_OVERLAP_CONTROLS_RESULT_REVIEW_INDEPENDENT_V002.md | 9515a5f11c3cdda05b744f4dd62305fc6f543b53c97fd3c2c65bf985523b6c4e |

Root and independent read-only review verified canonical payloads, intents,
dependencies, source hashes, counts and raw-stream identity. The independent
audit did not rerun the scientific oracle. Compile/C/oracle recorded wall times
are 0.632/3.233/0.0477 s, all exit0, no stop reason or monitor error. Sparse RSS
samples are not true peak-memory measurements. No new atomic history, thermal
pass, C2 qualification, propagation permission or Stage 3 promotion follows.

## Next history prerequisite already started

Root added inert unt_native_h_jet_v001.c/.h and
NATIVE_H_INTERPOLANT_JET_CONTRACT_V001.md in class_candidate_v001. They expose
analytic first/second jets of the ORIGINAL owned four-point uniform-z H
interpolant, preserve its value/index expression, and allow separate left/right
cell-polynomial jets without averaging. Source review is pending at this
checkpoint; there is no control packet, freeze, build, test or actual-array use.

The original H input ends at (N-1)*zmax/N, not zmax. A full-from-zmax trajectory
cannot satisfy the earlier overlap contract without resolving that coverage
premise. This packet does not extend the array, fill the top state, move the
phase boundary or assert a globally smooth H. A covered-prefix diagnostic or
new owned endpoint acquisition would be a separate explicit scientific contract.

## Exact durable next action

1. Finish the independent source review of the new native-H jet helper and
   contract; repair any defect before freezing anything. Author its bounded
   synthetic equivalence/analytic-derivative/domain controls and independent
   reference, then review/freeze/build/run once under root ownership. Do NOT
   repeat completed helium or HeII diagnostic science.
2. In parallel, decide the strongest useful same-source full-parent continuation
   after the reviewed projected static bound. A radial spectrum histogram,
   imposed density threshold or arbitrary volume law is not that continuation.
3. Only after H ownership and explicit coverage/initial-state decisions are
   scientifically specified should an overlap BE/BDF2 integrator be implemented.
   Its branch/uniqueness/residual controls and all later full-history transfers
   remain required; no physical trajectory is queued by this checkpoint.

Ledger V026 retains all eleven OPEN lanes. URM progress V004 is additive and
does not change its fixed V077/V018 API, adopted model, historical seals or
release artifacts. No account/credit/system/other-Mac/publication changes.

From: Codex2, author of this follow-up only
Date (UTC): 2026-10-13
Re: TO0125; start0131; accepted C124/C125
Supersedes: none
Action needed: yes — Codex3 distinct mathematical/framing review; root scope/next-input routing

# P58 follow-up: finite stroboscopic obstruction and a state-specific reduction contract

SOURCE/THEORY, new author Codex2, not self-reviewed or executed. The existing P58 row remains Codex3-owned; this is the explicitly routed follow-up. No physical state, event clock, environment or positive reduction is chosen by hand.

Line A question, candidate line C: which positive state/scale/history writer reduction is actually enforced by V005? BUILDS_ON C124/C125 (root0086/0089; original Codex3/0161/0167; distinct reviews0120/0123), canonical V005:4–20,28–34 and C91 original LANE_T48_D_JUDGE/T48_D_JUDGMENT.md:31–104. T20/O23 connection choice ambiguity and C93 qualification remain. No B transport law is assumed. H1/H2 retain actual failure and undefined branches.

## 1. The exact finite stroboscopic extension: only permutations survive

Let H be any finite Hermitian parent, tau>0, U=exp(-i tau H), and {P_a} a complete finite orthogonal read with nonzero ranks d_a. Use the declared rank-uniform lift E(p)=sum p_a P_a/d_a and K_n,ab=Tr(P_a U^n P_b U^(-n))/d_b. This lift is a METHOD definition, not an earned S1 preparation.

THEOREM. If K_n=(K_1)^n for EVERY integer n>=0 (the reset-lift populations exactly form a single time-homogeneous discrete Markov chain under indefinitely repeated native unitary intervals), then K_1 is a permutation matrix. Conversely, a permutation K_1 does imply that identity for all n. Thus a genuinely mixing/lossy positive Markov step is not an exact all-time reduction of this finite closed parent under this lift.

Proof. A finite-dimensional unitary has an unbounded sequence of positive integers n_j with U^(n_j)->I: simultaneous approximation of its finitely many eigenphases on a compact torus; finite-order U gives exact multiples. Therefore K_(n_j)->I. The hypothesis implies (K_1)^(n_j)->I, so |det K_1|^(n_j)->1. K_1 is nonnegative column-stochastic. Each column has Euclidean norm<=its l1 norm=1, so Hadamard's determinant inequality gives |det K_1|<=product column_norms<=1. The convergence forces |det K_1|=1. Every column norm must therefore equal1, forcing every probability column to have exactly one entry1. Nonzero determinant forces these entries into distinct rows: K_1 is a permutation.

For the converse, K_1,pi(b),b=1 and all other entries0 mean P_a U P_b=0 whenever a!=pi(b), by nonnegative squared block norm. Thus U maps each input block into its indicated output block. Completeness/unitarity and rank-measure invariance give d_pi(b)=d_b and equality of the block images. Applying U repeatedly permutes read subspaces; K_n is exactly the corresponding permutation power. This also closes on arbitrary input coherences because U†P_a U is another read projector.

This proof uses no temperature, thermodynamic mixing, positivity assumption beyond the actual reset-lift kernel, or classical physical model. It is a finite exact all-integer-times statement. It does NOT exclude finite-horizon approximate mixing, infinite-volume limits, conditioned state families different from E, a changing sequence of intervals, measured dynamics or a retained-memory state. It strengthens the earlier continuous-time result without erasing its escape routes.

Bind-only check, analytic and not executed: H=gX has nontrivial exact two-outcome discrete closure only when sin²(g tau) is0 or1. At other tau, already n=2 fails because cos(4g tau)=cos²(2g tau) would require cos²(2g tau)=1. Identity/permutation times do not supply a native selection law for tau. No such physical clock is derived by tuning a comparator interval. Full V005 need not possess the toy's swap times at all.

## 2. Native short-time interference obstructs the event interpretation

Let rho_b=P_b rho_b P_b, Tr rho_b=1, and a!=b. Under two native intervals of duration t, retain the two histories ending a with first outcome b versus first outcome a:

 C_ba=P_a U(t)P_b U(t)P_b,
 C_aa=P_a U(t)P_a U(t)P_b.

Both act to first order as -it P_a H P_b. Their decoherence cross term is

 D_(ba,aa)=Tr(C_ba rho_b C_aa†)
          =t² v_ab+O(t³),
 v_ab=Tr(P_a H rho_b H P_a)>=0.

If v_ab>0 they interfere constructively to leading order. Unmeasured final-a probability after2t is4t²v_ab+O(t³), while a complete intermediate projective measurement gives2t²v_ab+O(t³); other intermediate labels only enter at higher order. The coarse read and the measured event sequence are different even as the intervals get small. Absolute discrepancy vanishes like t², but its ratio to the rare-transition signal tends to1/2. Shrinking a step therefore does not establish a relative-accuracy event law.

For persistent q with rho_b supported on one q value, complete native V005 has v_ab=g² Tr(p_v rho_b). All the other owners preserve that q; no omission of incidence/admission/Birth dynamics is used for this leading identity. On an admitted state with positive carrier exposure the native short-time family is not decoherent. If exposure is zero, this witness is absent; report that state-specific null rather than a global no-event theorem. Exact Gamma commuting reads have no such native H writing at all; a finite-tolerance candidate needs its own projectors and budget from P60.

This is an analytic small-time result, not a finite-time numerical error estimate. A claimed finite interval needs an actual remainder, coefficient/state norm bounds and root computation. Positive diagonal history weights alone never decide the interference term.

## 3. A fail-capable finite-horizon contract, with no hidden reset assumption

For a fixed actual rho0, interval list and complete projector families, define D_hk as above and p_h=D_hh for the explicitly measured fine-history experiment. For an unmeasured union B of histories, define w(B)=sum_(h,k in B)D_hk. Then

 |w(B)-sum_(h in B)p_h| <= epsilon_coh(B),
 epsilon_coh(B)=sum_(h!=k in B)|D_hk|.

This permits a bound for each coherent union even when different union weights do not form one additive measure. It is a mathematical read of the same parent, not proof that a measurement took place. A qualified history ensemble requires native small epsilon on its specified events, relative/absolute scale and preparation domain, with errors controlled before scoring.

Even exact decoherence alone does not prove Markov closure. Let sigma_h be the actual normalized post-prefix state of a nonzero-probability measured history, ending in read a; compare it with E_a=P_a/d_a. For the next step, the total variation between its actual conditional outcome distribution and the rank-reset reference kernel column is <=(1/2)||sigma_h-E_a||_1, by unitary invariance plus contraction under measurement. Zero-probability prefixes do not supply a normalized state and are omitted from this conditional comparison while their null probability is retained.

Let delta0=||rho0-E R(rho0)||_1 and delta_j bound that trace distance over ALL positive-probability prefixes of length j, j=1..m-1. Repeated conditioning/telescoping gives

 TV(p_histories, mu_reset_reference) <= min(1, (delta0+sum_j delta_j)/2).

The reference here may be time-inhomogeneous if intervals/families vary; no homogeneous clock is implied. Combining with the previous inequality bounds each union against that reference by epsilon_coh(B) plus the total-variation bound. Every delta and epsilon must come from the complete actual state/evolution or a proved upper bound. They are not zero because someone chose to use E in code. A pure conditional state in a rank-d block can have trace distance2(1-1/d) from E_a, so this requirement is substantive, not automatic.

Alternative physically earned lifts can replace E only with their own normalization, hidden-state and invariance proofs. The current packet selects none. Measurement/dephasing operations used to DEFINE controls do not become native V005 terms. Qualifying a positive path measure would still not identify a spatial E1/E2/E3 writer venue or establish reach; its writer costs, directional weights and retained content remain separate C91 obligations.

## 4. Actual branch and next dependencies

Result now submitted: EXACT_FINITE_STROBOSCOPIC_RESET_LIFT_MIXING_REFUTED (only permutations permit all-time exact closure), plus the native persistent-q short-time constructive-history witness. This is a scoped mathematical answer to the new exact step, not the claim 'no native positive reduction exists at any scale'. H1/H2 stay UNDETERMINED. Neither lack of q-count conservation nor positive interval normalization chooses masslessness or E3.

A state/scale-selected positive reduction is still UNDETERMINED because no physical S1 state family, native clock/event selection, Gamma family, large-volume limit or certified decoherence/memory budget is supplied. The finite-horizon test contract now names exactly what would decide it without a new premise. Root may supply authenticated existing accepted states/histories for those quantities; this author cannot manufacture them from S1 or choose an unreviewed output to clear the gate. Failed sufficient budgets yield UNDETERMINED, not impossibility. Exact counterexamples reject only the corresponding universal/exact proposal.

No numerical source, job, resource claim or global state search is issued by this theory note. Existing reviewed P63 history source can retain D for tiny method purposes, but no P63 native output is consumed. Costs, basis sizes and actual native state construction are root-routed follow-ons, not author launches.

Review requested: recurrence-to-permutation proof and converse; short-time cross-history coefficient and native Bind specialization; distinction between coherent unions, measured histories and Markov reference; trace-distance telescoping including initial hidden state; finite/all-time and state-family scope. Codex3 reviews this author extension; Codex2 does not. Root writes accepted learning and maintains P58 physical-reduction debt.

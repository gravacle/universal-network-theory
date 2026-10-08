# Current 3D record-feedback parent: bounded worldline pilot V001

2026-10-05 UTC. Prospective protocol; no numerical execution is authorized
by saving this document. Root owns any eventual launch after source and
protocol review and a fresh execution-ownership check. This is one fixed
finite-temperature pilot, not a phase search or a replacement scheduler.

## Owned action and graph

Use the supplied simple periodic diamond graph only. Cells are
`r=(r1,r2,r3) in Z3^3`, in lexicographic order; vertices are `A_r,B_r`.
Port `a=0,1,2,3` connects `A_r` to `B_(r+s_a)`, where
`s=(0,e1,e2,e3)`. There are 54 vertices, 108 distinct links, and four
degree-four ports per vertex. Each port color is a matching of 27 links.
Canonical stored bits have order `(imaginary-time slice,r,port)`.

Retain `Nc=0`, every record occupied (`q_record=1`), `d_star=2`,
`Ud=1`, `ER=1`, `lambdaR=1/2`, and the disclosed proper-local flip
`h=1/5`. All source lapses are `L=1`; no strain, volume, source profile,
matter vertex, photon or physical ruler is introduced. The complete
fixed-sector operator, including its common identity, is

    delta_v=d_v-2, f(delta)=delta^2-delta/2,
    D=sum_v f(delta_v), H=D-(1/5)sum_e X_e
     =54 I+(1/2)sum_owned_link_pairs Z_e Z_f
           +(1/2)sum_e Z_e-(1/5)sum_e X_e,
    n_e=(1-Z_e)/2.

Thus longitudinal/J=1 and transverse/J=2/5 in Pauli conventions.
Neither the zero-longitudinal transverse-field model nor a projected
hex-ring Hamiltonian replaces this action. Record and carrier formation
are outside this fixed-record no-carrier experiment.

Freeze these three current input files, relative to this directory:

| File | SHA256 |
|---|---|
| LOCAL_RECORD_FEEDBACK_3D_ICE_OPERATOR_CROSSWALK_V001.md | 7f755bbae58c40583f784d469376792cece209193113504136f20e86259b3371 |
| LOCAL_PROPER_BOND_NORMALIZATION_V001.md | 9b4cc5e1942ac7373e210efa46bfa74e03bbcfb8130c01232373b02e8a622a5b |
| LOCAL_RECORD_FEEDBACK_INTEGER_DEFECT_BRIDGE_V001.md | 2aae1e1585ef42459ccabc13c8e0f388c8598dd9270f5ed953c7e36073119d83 |

The primary methods audit read Emonts/Wessel Section II in the complete
paper, including B/P/G/T-SSE; no separate supplement was located. Their
Hamiltonian lacks the present longitudinal field. Sandvik explicitly
requires modified cluster rules for a z field. These references motivate
mixing caution and do not authenticate this implementation or its phase.
[Emonts/Wessel](https://arxiv.org/html/1808.09827v2),
[Sandvik](https://arxiv.org/pdf/cond-mat/0303597).

## Fixed census and random streams

Use float64 NumPy and `numpy.random.Generator(PCG64(seed))`; record the
Python/NumPy versions. Each chain has its own stream, with no shared draws.
The four starts below are constant in imaginary time. `I01` occupies ports
0 and 1 in every cell; `I02` occupies ports 0 and 2. They are distinct
cut-flux degree-two words. `B` has every link blank. `R` draws the 108
initial bits in canonical `(r,port)` order using its own generator, then
copies that word to every time slice. That draw is part of the recorded
chain stream. All records remain occupied for every start.

| beta | dt=epsilon | M | I01 seed | I02 seed | B seed | R seed |
|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1/16 | 64 | 202610050401 | 202610050402 | 202610050403 | 202610050404 |
| 4 | 1/32 | 128 | 202610050411 | 202610050412 | 202610050413 | 202610050414 |
| 8 | 1/16 | 128 | 202610050801 | 202610050802 | 202610050803 | 202610050804 |
| 8 | 1/32 | 256 | 202610050811 | 202610050812 | 202610050813 | 202610050814 |

Run conditions in table order and starts `I01,I02,B,R`, one resident chain
at a time. Exactly 64 burn-in sweeps and 256 production sweeps per chain;
measure after every complete production sweep, with no thinning. A sweep
uses the fixed color order `0,1,2,3`, with no random color permutation.
Use 16 consecutive sweeps per block (16 production blocks). Save a
checkpoint at burn-in completion and after production sweeps
`32,64,96,128,160,192,224,256`. No extra chains, adaptive burn-in, budget
extension, temperature/step refinement, restart or rerun is authorized by
this protocol. Preserve every incomplete or inadequately mixed chain.

## Full finite-M measure and conditional sampler

Use the trace of the symmetric second-order product

    Z_M=Tr[(exp(-epsilon D/2) exp(epsilon h sum X)
                          exp(-epsilon D/2))^M].

Its positive periodic bit-path weight is

    W=exp[-epsilon sum_tau D(n_tau)] product_(e,tau) C(n_e,tau,n_e,tau+1),
    C_same=cosh(epsilon h), C_flip=sinh(epsilon h), tau+M=tau.

For edge `e=(u,v)`, let `c_u,c_v` count the other three occupied incident
links at each slice. Its conditional diagonal difference is exactly

    v_tau(1)-v_tau(0)=2(c_u+c_v)-7.

The addition cost at a degree-two word is 1 and the removal cost is 3.
For conditional probabilities only take `v_tau(0)=0` and
`v_tau(1)=2(c_u+c_v)-7`; the omitted slice constant cancels from that
conditional distribution. Full D is retained in all energy observations.
The temporal transfer matrix is

    T_tau(i,j)=exp[-epsilon v_tau(i)] C(i,j).

Sample each complete periodic two-state line by transfer messages. Choose
the first bit with probability proportional to the two diagonal entries
of the transfer product. Then choose successive bits conditioned on the
chosen first bit and the suffix product, including the closing last/first
transition. Same-color lines have disjoint endpoints and hence factorize
conditionally: all 27 are a Gibbs block based on the unchanged other
colors. Draw the first-bit uniforms for all 27 lines in lexicographic cell
order, then draw each successive-slice batch in that order. Positive
weights ensure finite-M irreducibility; they do not imply useful mixing.

Normalize every positive transfer message/product by its maximum after
each multiplication and retain log normalization where partition values
are compared. Normalize the two choice weights by their positive sum.
Fail and preserve a checkpoint for nonfinite/negative weights, zero sums
or a probability outside `[0,1]`; record its excursion (including any
below `2e-14`) and do not clip it or alter the Hamiltonian. Tiny positive probabilities are
retained. The largest step used is 1/16, so no extreme-field workaround or
adaptive numerical representation is needed.

Before any full pilot chain, perform all small finite-path controls:

1. Check the actual graph's 108 unique links, degree four, four 27-link
   matchings and the two ice starts. Exhaust all 64 other-neighbor six-bit
   assignments to derive the one-edge D difference independently from
   the two full endpoint functions.
2. At both dt values and M=2,3,4 enumerate all `2^M` periodic words for
   each uniform difference `-7,-5,-3,-1,1,3,5` (42 cases). Also use the
   varying lists `[-7,5]`, `[-3,1,5]`, `[-7,-1,3,5]` at the corresponding
   M (six cases). Compare transfer and direct-enumeration partition
   values, all one-slice/pair marginals, and every positive-prefix next-bit
   conditional probability. Relative partition tolerance `3e-13`,
   absolute probability/marginal tolerance `3e-13`. Validate first-bit
   and final periodic closure separately. These are exhaustive finite
   word controls evaluated in float64, not directed-rounding certificates.
3. Independently check the inverse-CDF choices just below and above each
   nonboundary conditional threshold, with offset `1e-8`; thresholds at
   0/1 retain their deterministic endpoint behavior. Check invariance of
   normalized probabilities when adding the common potential 37 to both
   states, and the corresponding log-partition shift `-37 M epsilon`.
4. Check every circular line has an even number of temporal flips. Verify
   D from degree counts against the complete Pauli expression on both
   ice starts, blank and full words, and 16 deterministic graph words
   `n_(r,a)=bit_((r1+3r2+9r3+27a) mod 8)(word)` for words 0..15.

Any failed arithmetic/control gate prevents full-pilot execution; retain
all controls and failure evidence. There is no outcome repair or retry.

## Measurements, normalization and static scope

Use seven native characters `k=0,+e1,-e1,+e2,-e2,+e3,-e3` in Z3^3;
phases are `exp(-2 pi i k.r/3)`. This chart is supplied combinatorics,
not a metric or physical wavelength. Define, at each time slice,

    E_(r,a)=n_(r,a)-1/2,
    z_a(k,tau)=sum_r E_(r,a,tau) exp(-2pi i k.r/3)/sqrt(27),
    d_s(k,tau)=sum_r delta_(s,r,tau) exp(-2pi i k.r/3)/sqrt(27), s=A,B,
    bar_z=M^-1 sum_tau z, bar_d=M^-1 sum_tau d.

For every chain and condition retain first moments and raw second moments
before connected subtraction. Report the full complex Hermitian 4x4
four-port equal-time covariance

    S_ET=<M^-1 sum_tau z z^dagger>-<bar_z><bar_z>^dagger

and the separate zero-Matsubara covariance

    S_0=<bar_z bar_z^dagger>-<bar_z><bar_z>^dagger.

Here brackets average production sweeps. Condition summaries equally
pool the four chains' raw first/second moments before connected
subtraction; do not average already connected chain matrices. Subtract sample means even at nonzero k; do not
force a symmetry mean to zero. `S_ET-S_0` is a time-variance matrix and
must be positive semidefinite up to `3e-11*max(1,matrix operator norm)`; this is a
diagnostic, not a new quantum positivity assumption.

The 2x2 **coordination static susceptibility** is

    chi_coord(k)=beta[<bar_d bar_d^dagger>-<bar_d><bar_d>^dagger].

This is the Kubo/static response convention for a separately declared
diagnostic port `H(eta)=H-sum_(s,r) eta_(s,r) delta_(s,r)`; it is not the
native whole-node energy/lapse source and earns no gravitational response.
Its normalization is per 27-cell Fourier amplitude. Report the full
matrix and `v_+=(1,1)/sqrt(2)`, `v_-=(1,-1)/sqrt(2)` even/odd diagonal
and cross combinations. Do not replace this imaginary-time-integrated
covariance with beta times the equal-time covariance. The coordination
deviations have the same sign on A and B; oriented graph charge instead
has `Q_A=delta_A,Q_B=-delta_B`, a disclosed row/column sign transform.
For each k check the exact coordination Fourier identity
`d_A=sum_a z_a`, `d_B=sum_a exp(-2pi i k.s_a/3) z_a`.

Retain unconditional histograms for degrees 0..4 and delta -2..2 on each
sublattice and all vertices, averaged over every slice and sweep; also
report oriented-charge histograms, D/54, `<delta^2>/54`, nonice fraction,
and total occupied-link fraction. Per slice check oriented total charge
zero and `sum_A delta=sum_B delta=number_occupied_links-54`.

The finite-M thermodynamic energy estimator, derived by differentiating
the same trace weight at fixed M, is

    E_M=M^-1 sum_tau D(n_tau)-(h/M) sum_(e,tau) f_(e,tau),
    f_same=tanh(epsilon h), f_flip=coth(epsilon h).

Report E_M/54, both separate terms and total kink counts. Do not drop
the `54 I` contained in D. This is a finite-product free-energy derivative
estimator, not an exact ground-energy or zero-step certificate.

For each native periodic cut i, define
`Phi_i(tau)=sum_(r:r_i=2) E_(r,port=i)` (ports 1..3). Retain the time
average and the tau=0 vector at every production sweep, change counts and
histograms. These unconditional cut fluxes are defined even on charged
slices. Label an ice/winding value only when that entire tau=0 slice has
all delta=0; preserve its undefined count otherwise. Changing a charged
cut value is not proof of winding-sector mixing. No ice postselection is
used in any observable average. The I01 and I02 initial cut vectors are
respectively `(9/2,-9/2,-9/2)` and `(-9/2,9/2,-9/2)`.

## Uncertainties, mixing and grid comparisons

Keep all 256 sweep traces and 16 block sufficient-statistic sums per
chain. Estimate connected-observable uncertainty by leave-one-block-out
jackknife over those 16 blocks. Condition errors use the analogous
leave-one-block-out calculation on its 64 pooled blocks. For B blocks
the variance is `(B-1)/B sum_b (estimate_without_b-mean_estimate)^2`.
This square applies to real statistics. For every complex covariance,
susceptibility, combination or signed grid-comparison entry, retain
separate real-component and imaginary-component standard errors, applying
that formula to each real component; never treat a complex square as a
variance. Reports and comparisons retain both components and their errors.
This is only a block diagnostic; long autocorrelation can invalidate its
coverage. Report per-chain estimates before equally weighted four-chain
summaries and keep their differences separate from pooled errors.

For each chain diagnose energy/54, D/54, nonice fraction, the three
time-averaged cut fluxes, and at all seven k the scalar primitive traces
`M^-1 sum_tau ||z||^2`, `||bar_z||^2`, and `|v_+^dagger bar_d|^2`,
`|v_-^dagger bar_d|^2`. Use lags 0..126 with
`c_l=(256-l)^-1 sum_t (x_t-mean)(x_(t+l)-mean)`. Sum positive consecutive
pairs `(c1+c2),(c3+c4),...` until the first nonpositive pair; report
`tau=max(1,1+2 sum_pairs/c0)` and `ESS=256/tau`. For exactly constant
traces keep ESS undefined, not 256. This short-chain initial-positive-pair
estimate can miss slow modes and is not a mixing proof.

For each condition split its four chains into eight 128-sweep halves.
Report conventional unranked split Rhat from within/between-half variance
for the same traces, preserving constant/zero-denominator cases as
undefined. Explicitly, with eight half means, half length n=128, unbiased
half variances, `W=mean(half_variances)`,
`B=n/(8-1) sum_half (half_mean-grand_mean)^2`,
`Rhat=sqrt(((n-1)W/n+B/n)/W)` when W>0. Preserve Rhat below one rather
than clipping it. Also retain pairwise chain differences and raw flux histories.
The prospective diagnostic threshold is ESS>=16 for every nonconstant
listed trace in every chain and split Rhat<=1.10 for each listed trace;
The exact structural null `v_-^dagger bar_d(k=0)=0` follows from equal
total A/B coordination and is excluded from ESS/Rhat thresholds. Preserve
its raw roundoff and undefined diagnostics with reason `STRUCTURAL_NULL`,
and check its amplitude at `3e-12*max(1,||bar_d||)`. Other undefined
diagnostics or no changes in any unconditional cut component of any
chain yield `MIXING_UNQUALIFIED`. Threshold passage is only
`FINITE_GRID_PILOT_DIAGNOSTICS_PASSED`, never certified equilibrium.
Arithmetic failures take priority as `ARITHMETIC_FAILED`. Retain all data
under every status; no chain/start may be removed to improve agreement.

Report both dt results separately at each beta and their signed
differences with block errors. Flag differences above three combined
block standard errors as resolved step sensitivity; do not call two steps
a rigorous Trotter bound or zero-step extrapolation. Report beta4 versus
beta8 separately at each dt; two temperatures do not establish beta to
infinity. One L3 size cannot establish a thermodynamic phase, Coulomb
pole, interaction range, native preparation, physical time or metric,
matter vertex, galaxies, cosmic expansion, or completion of Stage 3.

## Compact custody and execution boundary

Reserve only new files in this directory:
`local_record_feedback_3d_worldline_pilot_v001.py`,
`LOCAL_RECORD_FEEDBACK_3D_WORLDLINE_PILOT_V001_RESULT.json`,
`..._RESULT.md`, `..._RECEIPT.json`, and
`local_record_feedback_3d_worldline_pilot_v001_checkpoints/`.
Refuse any existing reserved output or checkpoint directory. Authenticate
the three note bytes, source and this protocol before controls and again
before final sealing. Save one small manifest, control result, append-only
JSONL journal, and exclusive per-chain checkpoint bundles containing bits,
PCG64 state, completed counters, all accumulated trace/block statistics,
input/source/protocol hashes and elapsed time. Flush/fsync a completed
bundle before its journal hash commit. Save each completed chain before
starting the next. A failure saves its exact partial state/error and
exits; no automatic resume. Root may later inspect/recover those existing
states before considering any separately authorized continuation.

Final raw JSON retains all 16 chains, 4 condition summaries, both dt/beta
comparisons, controls, numerical/status limitations and measured runtime.
The report must show the complete 16-chain census, condition statuses,
energy/defect/flux and selected spatial/static summaries with uncertainty,
not only successful starts. Seal source/protocol/input hashes, canonical
and raw JSON hashes, report hash and journal prefix in the final receipt.
No old producer, propagation, eigensolver, recorded-state vector, external
simulation, new coordination framework or schedule is needed. Root may
launch exactly this fixed pilot only after full preflight; stopping at its
fixed endpoint earns its scoped data and does not imply background work.

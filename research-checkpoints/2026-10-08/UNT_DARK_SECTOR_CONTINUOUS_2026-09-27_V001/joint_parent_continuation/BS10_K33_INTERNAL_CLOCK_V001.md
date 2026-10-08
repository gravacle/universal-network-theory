# K3,3 internal absolute phase-clock readout V001 — prospective protocol

2026-10-05 UTC. Owner observer_cosmography. New saved-vector-only readout of the SAME native H, complete node0 source and all16 preparations/six delays. Source/protocol preparation does not authorize execution: root and independent final preflight, exact frozen input custody and root's fresh live-ownership check must precede ONE modest local worker. No formation, eigensolver or propagation is repeated.

## Recovered phase-clock matching and declared experiment

`NATIVE_FORMED_STATE_SOURCE_MATCHING_V001.md` (SHA256 07a321e8962070d1dbb48540c7674dba60c36b7b85c18f08776954b25262bbdc) distinguishes an elapsed-phase clock, whose response includes the perturbed initial-phase subtraction, from an externally fixed absolute phase origin. `NATIVE_CARRIER_CONTROLLED_CLOCK_V001.md` (SHA256 55e7514ecdc636bc2817d78d44ca5a50422f8be2002877e96c92fca04636108b) shows that active carrier/degree/record correlations affect the clock rate; averaging them into a prescribed frequency is an additional closure. The older finite writer clock protocol (`NATIVE_PHASE_CLOCK_PROTOCOL_V001.md`, SHA256 bb6ef50c0f7ba0d3271f9e07f5ba45ce973b24afdb5e2404460e628296404d48) does not certify the present moving-carrier clock or a continuous window.

Declare an ABSOLUTE record0 dial-phase coordinate with its origin fixed to the unperturbed pre-kick preparation. Do not reset its phase after the source impulse. At each frozen readout point compare the perturbed observable at the SAME unperturbed clock phase using the local inverse of the phase map, if numerically conditioned. The protocol does not compare phase elapsed from a newly reset post-kick origin, certify single-shot access, select a continuous monotonic interval or calibrate physical seconds.

At source delay0 the correction is explicitly `SOURCE_BOUNDARY_TANGENT_ONLY`: an immediate signed dial shift may require matching across the pulse boundary, so the formal inverse-chart tangent is not automatically an accessible post-pulse measurement. Retain this point and its conditioning status. Interior delays are labeled `INTERIOR_LOCAL_PHASE_CHART`; no finite shifted trajectory or apparatus is solved there either.

Use the conventional record Pauli matrices Z0=1-2q0 and Y0; on a vector indexed by native record bits,

    (Y0 psi)_r = -i (1-2q0_r) psi_(r xor 1).
    B=Z0-iY0, beta=<B>, ||B||=2.

This B is twice the prior half-normalized carrier clock; its phase and rate are unchanged, while all operator/error bounds use its actual norm2. Obtain beta, its pure-H derivative and its complete h0 impulse tangent from the saved columns psi, U h0psi, U h0^2psi and exact Pauli actions. Do not infer the non-Hermitian B tangent using a single Hermitian 2Im expression:

    beta_dot = Z_dot-iY_dot,   Z_dot=2Re<-iHpsi|Zpsi>,
    Y_dot=2Re<-iHpsi|Ypsi>,
    delta_beta_h0 = R_Z,h0-i R_Y,h0,
    R_A,h0=2Im<Apsi|U h0psi>, A=Z,Y.

There is no explicit source dependence in the mathematical readout B, so its direct source contact is zero. This does not implement a laboratory quadrature pulse or exempt its eventual apparatus from work accounting.

Independently evaluate the exact same-action commutator derivative

    beta_dot = 2g<P0 Y0> + i <(1-d0/2)X0 + 2g P0 Z0>.      (1)

Here d0 is the actual incidence-degree operator, not a fitted mean graph. All omitted native terms commute with this B; they remain in H, state evolution and energy/work. Also crosscheck delta_beta with i[<U h0psi|Bpsi>-<psi|B U h0psi>], which requires both B and B-dagger through the two inner products.

## Whole census, relational response and unchanged work

Authenticate the sealed nodal result (raw SHA256 7a4fc007d3ca9a46482091f4e6ab54a78c866dd4eabaeb19fc4d83b766c2499c; canonical payload 0da65bdca466d621561b04a341d2881906d7586535b33bd07a6d3edba4e62240), its producer/source/protocol/report, manifest/preflight/journal and every selected row/bundle seal. Recover all original native input hashes too. The current nodal report hash is dbc549f522212fd9cd523a56d6e00304419d100cedc68cc1e07af3865db8a35b; source349828cfdb729fceb2593bd7084e348226206f4781c1af71aaeb137a76bfbbf9; protocol a8abf2801422b4ae4e450ec4a2819f1d3cbdef9fdc937ec008e61d3c030b340d. Repeat byte authentication before sealing.

Retain g=0,.1; starts0/413; ages0,5,20,50; delays0,.1,.5,1,2,5: all96 points, every clock status and sign. Read the original six carrier/six record probabilities, M, connected projector, H and h0 response values. Baseline raw vectors are never normalized/clipped. Norms and scalar error budgets are disclosed. No favorable age, phase sign, source strength, clock orientation or parameter is selected after results.

Where the clock qualifies below, define

    nu=Im(beta_dot/beta), kappa=Im(delta_beta_h0/beta),
    delta_t_h0=-kappa/nu,
    R_O,h0^Theta=R_O,h0 + O_dot*delta_t_h0,                 (2)

with O_dot from the independently sealed uniform-H kernel. Also compute the clock's own corrected tangent delta_beta^Theta=delta_beta_h0+beta_dot*delta_t_h0; its phase tangent must vanish. Uniform source delta_beta_H=beta_dot gives delta_t_H=-1 and cancels R_O,H for every qualified observable. It does not need to have zero raw response in a nonstationary state. The actual zero-mean source h0-H/6 therefore has the same fixed-absolute-phase response as h0, up to the separately reported uniform cancellation residual; it is not a new port allocation.

The source-off complete energy derivative remains R_H,h0 because H_dot=0. Check it against the sealed pulse-work derivative and retain the raw cancellation residual rather than setting a tiny H_dot to zero. Full local pulse work is not erased or replaced by a clock correction. Unqualified points have null relational fields and an explicit reason, alongside raw beta, beta_dot, source tangent, means, raw source response and work.

g0 exact blank-record histories have beta=1 (up to their retained norm), beta_dot=0 and are explicitly `EXACT_ZERO_RATE_G0`, never divided into a clock. The age0,delay0 g.1 basis preparations have beta=1,beta_dot=.2i,nu=.2; this is an exact convention/control, not an extrapolation to later histories. Negative qualified rates are retained as local reversed orientation, not rejected or relabeled. No continuous inverse branch or accumulated unwrapped phase is claimed from the discrete census.

## Prospective conditioning and arithmetic criteria

The following criteria are numerical conditioning choices fixed before inspecting any beta outcomes, not observational uncertainty or a physical minimum clock frequency. For each saved column with norm n, use its saved exact-arithmetic propagation ceiling plus a declared floating-vector budget 2e-9*max(1,n). Exact delay0 vectors still carry that floating budget. With e_psi and n_psi, define L=2n_psi e_psi+e_psi^2. Bound beta error by e_beta=2L+1e-10*max(1,|beta|); bound beta_dot by e_dot=4aL+1e-10*max(1,|beta_dot|), using centered H halfwidth a and ||i[H,B]||<=4a. These budgets distinguish exact approximation certification from a conservative floating allowance; they are not directed-rounding proofs of the actual floating vector error.

For b=|beta|>e_beta,

    e_nu=e_dot/(b-e_beta)+|beta_dot|e_beta/[b(b-e_beta)].

Qualification requires b>=.01, b>100e_beta, |nu|>=.001 and |nu|>100e_nu. Otherwise retain status `AMPLITUDE_UNCONDITIONED` or `RATE_UNCONDITIONED`; also retain exact g0-null status. For qualified points calculate the source-tangent error from both saved columns:

    e_delta=4(n_q e_psi+n_psi e_q+e_psi e_q)
             +1e-10*max(1,|delta_beta|),
    e_kappa=e_delta/(b-e_beta)+|delta_beta|e_beta/[b(b-e_beta)],
    e_shift=e_kappa/(|nu|-e_nu)
             +|kappa|e_nu/[|nu|(|nu|-e_nu)].

Save every budget, conditioning ratio and shift/error. Propagate the shift budget to each corrected observable using its raw response and sealed O_dot, including an explicit 3e-8*max(1,compared magnitude,operator scale) arithmetic allowance. Do not use a small derived effect as a physics gate or discard a large error. Clock qualification does not promise a measured usable clock.

Independent algebra/action controls use 3e-8*max(1,scale); saved-vector/raw mean and response matching use2e-8*max(1,scale), norm/Gram matching2e-9*max(1,scale); uniform phase cancellation and complete-work preservation use the declared propagated budgets plus3e-8*max(1,scale). Keep the original whole-H phases, energy and all native record storage/feedback. Pauli square/Hermiticity and B commutator identities are checked on fixed complex probes and the actual saved vectors.

At every point, use the already saved three columns to form centered local source Taylor kicks with alpha=1e-5, using the SAME initial kick normalizations as the nodal protocol (calculated from the saved initial columns only). No extra propagation or h0 application. Compare the complex beta centered derivative to delta_beta/raw initial norm and the phase derivative to kappa, with phase changes taken relative to the unperturbed beta. Qualified points have their amplitude floors and analytic source-kick remainder recorded. The budget is the existing source norm bound<=6.45+g, Taylor remainder exp(alpha||h0||)*(alpha||h0||)^3/6, centered-derivative term||B||(2||h0||)^3 alpha^2/6, floating allowance5e-7*max(1,||B||), plus the ratio conditioning budgets. These controls verify the source sign and nonlinear phase derivative. They do not solve an actual post-kick trajectory or certify a finite phase-matched apparatus. Mathematical clock readout contacts are zero; source-switch/controller work remains exactly the old ledger.

The phase finite difference also owns the nonlinear arg(beta) truncation. For normalized baseline amplitude b_N=b/n_initial and G=||h0||, take b_min=(b-e_beta)/n_initial-4G alpha>0, retaining the declared beta error budget. A conservative third-derivative bound along the exact unitary source kick is

    |arg(beta)'''| <= 16G^3/b_min
                    +3(8G^2)(4G)/b_min^2
                    +2(4G)^3/b_min^3.                     (3)

Include (3)*alpha^2/6. With T the Taylor remainder, normalization of the approximate source-kick vector adds a complex expectation error e_phase no greater than 8T/(1-T)+8T^2/(1-T)^2. Require b_min>e_phase and use the valid angular-derivative allowance e_phase/[alpha*(b_min-e_phase)], not the unqualified chord/angle identification. Save these components separately, together with the complex-derivative allowance divided by the conditioned amplitude and the kappa error. Do not substitute only a complex-beta derivative remainder for the nonlinear phase bound.

## Exclusive execution and resumable evidence

Own only this protocol, `bs10_k33_internal_clock_v001.py`, `BS10_K33_INTERNAL_CLOCK_V001_RESULT.json/.md` and exclusive `bs10_k33_internal_clock_v001_checkpoints/`. Refuse existing outputs; no retry/resume/rerun is authorized. One manifest records PID/PPID/host/environment and all frozen inputs. Save each of the16 completed snapshot readout/check JSONs and an append-only fsynced journal seal before the next. Existing full-phase bundles already retain the needed vectors; do not duplicate or mutate them. Preserve partial rows/errors if interrupted.

Only the sealed native module's pure `fields/apply` and their pure field/graph dependencies, plus immutable DIM metadata, may be imported under a non-main name. Never call its old producer, weighted source, solver, recurrence, propagation, preflight, observer or anchor functions; no newly selected source. One modest local process, BLAS/OMP/MKL/VECLIB/NUMEXPR/BLIS threads1 and PYTHONDONTWRITEBYTECODE1 before NumPy import. Ordinary elapsed/RSS recording and one-row residency; no new resource guard, demanding model, installation, Goal, scheduler or other Mac. The root owns live-job verification and log/ledger integration. This ensemble internal phase diagnostic does not establish atomic/photon time, physical redshift/ruler/metric, cosmic acceleration, normalized galaxy gravity, observational superiority or Stage3 completion.

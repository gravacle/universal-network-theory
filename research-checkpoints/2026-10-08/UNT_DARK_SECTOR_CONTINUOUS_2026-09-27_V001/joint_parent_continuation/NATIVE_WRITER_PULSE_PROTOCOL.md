# Prospective native writer-pulse test

2026-09-28. Additive, fixed test of `NATIVE_RECORD_PHASE_PATHWAY.md`.
The implementation is inert until the root explicitly freezes and runs it.
No new formation, larger lattice, physical-volume assignment, ground-state
replacement, fitted coefficient or additional interaction is introduced.

## Scientific question and fixed experiment

Does the already formed native state respond to its owned writer-copy
source with the predicted active sign, full nonstationary kernel and
switching work? The held record-density self-response is zero; that does
not make its copying response zero.

Use all three authenticated `RECORD_ADDITION_RESULTS.json` preparations:
native, feedback-off formed, and copying-off blank control. Retain their
complete complex 16-component vectors and their own inherited coefficients.
Do not rerun formation. Advance each under its original held Hamiltonian to
every previously saved age `0, .25, .5, 1, 2`, checking saved count/link means.

At each age start every trial from exactly the same aged vector. Apply

    H_epsilon = H_hold + epsilon*K,  K = X_L+X_R,
    epsilon = +/-.01 and +/-.005,
    duration = .08, .04, .02, .01,

in the inherited hbar=1 units. These are 240 signed pulses, with no adaptive
duration/amplitude selection, retry grid, optimization or postselection.
The negative pulse is the sign reversal of the existing real copying source,
not a new interaction type. Compare every pulse to the unpulsed evolution at
that same age and duration. Read both K and total record count R.

The exact prospective coefficients are

    d(delta<K>)/d epsilon = -tau^2/2 * <[K,[H_hold,K]]> + O(tau^3),
    [K,[H_hold,K]] = 4*(1-lambda_R*n)*(1-R),
    d(delta<R>)/d epsilon = tau*<Y_L+Y_R> + O(tau^2).

The initial K-kernel slopes at the formation switch were independently
derived as approximately `-.867381853244`, `-1.175273204663`, and
`+3.125975578287` respectively. Their inherited signs persist at the five
specified saved ages. The short positive-pulse K response must therefore be
positive for both formed preparations and negative for the blank control.
No sign is imposed on R at other ages. Blank-record R has an exactly zero
linear response to copying; its finite-pulse count need not be zero.

## Independent response checks, keeping all bands and phases

1. Full Hermitian eigendecomposition evolves the pulse and its baseline.
   A scaled Taylor propagator from the frozen native worker cross-checks
   each pulse and each held-age propagator.
2. The exact source derivative of U has energy-basis entries

       (dU/d epsilon)_ab = -i*tau*K_ab
          *exp[-i*(E_a+E_b)*tau/2]*sinc[(E_a-E_b)*tau/2].

   Here sinc is sin(x)/x with its continuous value at every degeneracy.
   A coupled Taylor recurrence independently evolves U and dU/d epsilon.
3. For either observable O, compare the derivative operator
   `dU_dagger*O*U + U_dagger*O*dU` to the full plus-source Kubo integral

       i integral_0^tau [K(s), O(tau)] ds,

   using fixed 8- and 16-node Gauss quadratures. This is a matrix identity,
   subsequently evaluated in each actual aged state; it is not a diagonal
   population, stationary, thermal or ground-branch susceptibility.
4. Compute the source derivative's nested-commutator time coefficients
   through order eight. The first two identities above are checked as full
   matrices. For energy width L=Emax-Emin, the order-eight remainder is

       <= 2*||K||*||O||*tau*exp(L*tau)*(L*tau)^8/8!.

   This follows by bounding the n possible source insertions in each
   nested commutator. The same bound is used after state expectation and
   normalization by the leading tau power. Report the observed successive
   duration-error ratios, but do not demand a ratio of two when the cubic
   coefficient vanishes or a small denominator makes that diagnostic noisy.

## Finite amplitude, cancellation and numerical acceptance

Evaluate each change as
`2 Re <psi_base|O|delta_psi> + <delta_psi|O|delta_psi>` rather than subtracting
two order-one expectation values. The smallest nonzero predicted K changes
are comfortably above the fixed raw numerical allowance; require the final
short-pulse K central response and the actual positive .005 pulse's K change
to have the inherited sign and exceed ten times that allowance.

The central epsilon derivative has the rigorous exact-arithmetic bound

    |central_epsilon - exact_linear|
       <= ||O||*(2*||K||*tau)^3*epsilon^2/6.

It follows from the third source derivative's time-ordered commutator norm,
valid for all real epsilon in the specified interval. For
`(4*central_(epsilon/2)-central_epsilon)/3`, Taylor's theorem bounds the
remaining error by

    ||O||*(2*||K||*tau)^5*epsilon^4/288.

The 1/288 bound allows independent fifth-derivative remainders, rather than
assuming their asymptotic coefficients already agree. A raw allowance of
`1e-12` covers the numerical state/change comparison; after division by
epsilon it is explicitly reported, not disguised as a stronger derivative
accuracy. Structural identities and Kubo comparisons retain `1e-11`.
Both amplitude results and all ages/durations are retained, including any
failure. Taylor tail bounds are exact-arithmetic truncation bounds, not a
proof of floating-point roundoff. Eigensolver/Taylor agreement checks the
separate numerical issue.

## Work and scope

Each pulse includes its full source-work ledger:

    W_on = epsilon*<K>_initial,
    W_off = -epsilon*<K>_after,
    <H_hold>_after - <H_hold>_initial = W_on+W_off.

The pulse Hamiltonian's mean energy must be conserved during the pulse.
The unpulsed reference is used only for cancellation-stable evaluation;
its held energy is constant. These signed work values are not ignored or
relabelled as autonomous record production. A negative initial response
weight is an actual prepared-state response, not a finite-unitary ghost.
This test does not establish a cosmological clock kinetic term, a passive
continuum spectrum, damping, matter production or volume stress.

## Execution and custody

`native_writer_pulse_compute.py freeze` creates a new, no-overwrite source
manifest; `native_writer_pulse_compute.py run` checks it before propagation.
No arguments or importing the module does not run the worker. Inputs include
the exact old result and old freeze, all five old transitive source files,
the phase derivation, this protocol and the new code. The old result bytes,
result/freeze link, canonical payload digest and successful check census are
verified before either new action. No old file is edited.

New outputs are only `native_writer_pulse_frozen.json` and
`native_writer_pulse_results.json`, published without overwrite through a
flushed temporary file and atomic hard-link creation. Failed checks produce
a FAILED result with the full evidence; no tolerance widening or automatic
rerun follows. Source/input custody refusal occurs before pulse evolution.
The root owns the one execution. All matrices are 16 by 16; one-thread
libraries and the fixed small census avoid large memory or long-run
checkpoint requirements. No arbitrary wall-time stop is introduced.

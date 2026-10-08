# Vacuum cancellation: thresholds, protection and a controlled residual

2026-09-27. Root analytical derivation inside the existing conditional
finite-shell formalism. No mode inventory, symmetry, new field, cosmological
fit or numerical execution is adopted. This is a necessary test for a
candidate network mechanism, not the mechanism's completion.

## 1. Define the actual spectral object before counting modes

Use the RIEHB sharp proper-time shell, a=κ^(-2), b=μ^(-2), 0<μ<κ,
and L=(4π)^2. Suppose a finite set of admitted fast field operators has
constant nonnegative mass squares λ_i and owned signed volume weights w_i.
All determinant factors, gauge/constraint fields, continuation signs and
multiplicities belong in these weights. They are not counts of arbitrary
finite-system eigenvectors. Define

    Z0(s) = sum_i w_i exp(-λ_i s),
    C0^> = -ħ/(2L) integral_a^b s^(-3) Z0(s) ds.

This fixes the RIEHB common-negative-prefactor convention. In particular,
the EY/Visser conversion must be completed before raw statistics-weighted
mode ranks are called w_i; the current source review identifies a sign
dictionary that treats the volume and curvature coefficients differently.
The formula here is valid in its declared symbols, not a license to mix
those conventions.

The operator and matching assumptions are those of
[RIEHB](../program-worktree/LANE_CROSS_RFT_MGFT_INDUCED_EH_BACKREACTION_V001/THEOREM.md).
For comparison, [Visser (2002), sections 5–6](https://arxiv.org/pdf/gr-qc/0204062)
distinguishes cancellation of leading mass moments, a finite residual and
its further cancellation. That conventional field-theory discussion is not
a derivation of a UNT spectrum. The finite-band tests below are derived
directly from the displayed integral.

## 2. A count cancellation does not cancel massive thresholds

Let M_(2r)=sum_i w_i λ_i^r. Taylor expansion with a bounded remainder gives

    integral_a^b s^(-3) Z0(s) ds
      = (M0/2)(κ^4-μ^4) - M2(κ^2-μ^2)
        + (M4/2) log(κ^2/μ^2) + R6,

    |R6| <= [sum_i |w_i| λ_i^3]/6 * (μ^(-2)-κ^(-2)).

The bound follows from |e^(-x)-(1-x+x²/2)|<=x³/6 for x>=0,
applied before integration. It is valid as a bound for nonnegative masses;
its interpretation as a useful light-threshold approximation requires the
remainder to be small. Heavy modes must use their actual threshold integrals.

Thus M0=0 cancels the massless quartic term but generally leaves M2 and M4.
Even M0=M2=M4=0 does not make a finite shell vanish. For example, take

    λ_i = (0, m², 2m², 3m²),
    w_i = (1, -3, 3, -1),      m²>0.

The first three moments vanish exactly, but

    Z0(s) = (1-exp(-m² s))³ > 0    for s>0.

Every positive finite shell has a nonzero volume contribution. This is an
algebraic counterexample to inferring full cancellation from three sum rules,
not a proposed physical spectrum or a prediction of its vacuum sign in a
different convention.

## 3. What genuinely protected finite-band cancellation requires

For this finite constant-mass class, suppose the volume integral vanishes
for every subinterval of some open positive-s interval. Differentiating an
endpoint implies Z0(s)=0 throughout that interval. Combine all exactly
degenerate masses into distinct λ_j with aggregate weights W_j. Then

    sum_j W_j exp(-λ_j s)=0

on an interval forces every W_j=0. One proof takes derivatives of orders
0,...,r-1 at an interior point: the resulting Vandermonde matrix for distinct
λ_j is invertible. Conversely these mass-by-mass cancellations plainly make
every shell vanish.

This is stronger than a small integral for one selected shell. Such an
integral could be an accidental cancellation and must have its cutoff/profile
sensitivity tested. The theorem is limited to the finite fixed-mass class;
infinite towers, interactions, running fields and non-Laplace operators need
their own convergence and spectral arguments.

Cancellation of Z0 does not algebraically force the curvature kernel to
vanish. Curvature coefficients also depend on spin, nonminimal coupling and
constraint structure, not just the volume weight. A candidate could protect
the volume term while retaining stiffness—but the actual same-parent
operators and protecting identity must demonstrate that. Declaring matched
weights by hand is an input, not a network explanation.

## 4. A constructive small-residual test

This section is a prospective spectral mechanism class, not a chosen UNT
completion. Suppose an independently established cancellation pairs volume
weights +w and -w at a common positive mass square m², while the combined
curvature weight in the same RIEHB convention is B!=0. Give one member a
small, independently derived shift δ, with m²+δ>=0 and |δ|<<μ². Then

    Z0(s)=w[e^(-(m²+δ)s)-e^(-m²s)]
          =-w δ s e^(-m²s) + O(δ² s² e^(-m²s)),

    I1(m)=integral_a^b s^(-2) e^(-m²s) ds > 0,
    C0^> = ħ w δ I1/(2L) + O(δ²),
    CR^>(δ=0) = -ħ B I1/(2L).

If those are the complete coefficients of this restricted shell and no
other volume/matching/retained contribution dominates, the leading ratio is

    Λ_shell = -C0^>/(2CR^>)
             = w δ/(2B) + O(δ²/μ²).

The error scaling presumes fixed finite curvature-weight ratios to nonzero B
and the stated small splitting. It follows from s<=μ^(-2) in the shell;
the curvature coefficient also changes at order δ and must be included beyond
leading order. The absolute cutoff enhancement cancels in this ratio because
both leading terms contain the same threshold integral, not because a fitted
counterterm was subtracted.

For a finite splitting, not just an asymptotic statement, let β be the
shifted member's curvature weight, keep the curvature couplings fixed, and
put q=|δ|/μ². With I0=integral_a^b s^(-1)e^(-m²s)ds<=I1/μ²,

    |C0^> - ħ w δ I1/(2L)| <= ħ |w| δ² e^q I0/(4L),
    |CR^>(δ)-CR^>(0)|/|CR^>(0)| <= r := |β/B| q e^q.

Require r<1 (preferably r<=1/2) to retain a nonzero curvature coefficient
with the same sign. For nonzero wδ the exact ratio then obeys

    |Λ_shell - wδ/(2B)|
      <= |wδ/(2B)| [q e^q/2 + r]/(1-r).

These bounds use |e^(-δs)-1|<=|δ|s e^q and the corresponding second-order
Taylor remainder. They show explicitly why a small mass shift alone is
insufficient if B is itself a near-cancellation. If the splitting also
changes curvature couplings or other operators, those changes need their
own bounds; the displayed threshold-only estimate cannot absorb them.

This supplies a precise constructive possibility: a protected cancellation
plus a controlled microscopic splitting can yield curvature governed by δ
rather than κ². Its signs still have to work: healthy shell stiffness needs
B<0 here, and positive Λ needs wδ/B>0. No sign or small value of δ has been
derived from records in the present program. A symmetry, its breaking rule,
allowed masses, higher-order stability and the full matching ledger remain
load-bearing. Setting δ to the desired dark-energy value would undo the
explanation.

## Decision

Use the actual parent spectrum to distinguish an unprotected sum, a
massless-only cancellation, a finite-band accident and an operator-level
protected cancellation. Existing finite many-body response poles do not
by themselves supply these field weights or masses. This test gives the
next precise requirement after the reference pure-shell low-curvature
failure: derive the cancellation and any residual from network dynamics,
while retaining a healthy curvature response and complete source ledger.
No dark-sector observation or new execution is claimed.

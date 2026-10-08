# Independent analytical review — native record connectivity

2026-09-29. Read-only mathematical/source review. No numerical worker, graph
propagation, parameter change or alteration of the reviewed note occurred.

## Disposition

**Accepted. No mathematical correction is required.** I read the complete
`NATIVE_RECORD_CONNECTIVITY_PATHWAY_V001.md` and independently checked its
operator lower bounds, finite-size constants, backbone leakage proof and
formation bounds against the owned BS seed and inclusion construction.
All four source hashes listed in the note match the resident files.

Reviewed note SHA-256:

    81bbb3b72e00c03475b8efcc63c861907adb8b0da72bd50f27c89a6bc0b6775c

## Load-bearing checks

1. **Carrier/current and record lower bound.** The qutrit edge operators
   satisfy T^2=J^2=P on the one-occupied-carrier transfer sector, so the
   minimum of `-t T+lambda_J P` is `-max(0,|t|-lambda_J)`. Separate edge
   bounds can be added even though adjacent carrier terms do not commute.
   Record feedback is bounded below by `-2 lambda_R n_e`. Expanding both
   endpoint degree penalties gives exactly
   `kappa_R=Delta+2U_d(1-2d_*)-2lambda_R-c_psi`.
   At the inherited values this is 3/4, not 1/2 or 1. The fixed-occupation
   reference retains onsite costs; the full-ground variant separately uses
   their nonnegativity and zero copying couplings.

2. **Ground occupation and connection bound.** The independent Bloch and
   Cauchy--Schwarz inequality is
   `|<sum X>|<=2 sqrt(m(N^2-m))`. Ground energy no higher than the blank
   incidence trial then gives
   `kappa_R*m <= 2Omega*sqrt(m(N^2-m))/N`. For m>0, squaring and dividing
   produces the stated denominator
   `kappa_R^2*N^2+4Omega^2`; m=0 needs no division. The limiting inherited
   upper bound is 64/9. Markov's bound with at least 2N-1 edges for a
   connected graph is correct. It is a ground-branch result, not a bound
   on every high-energy formed state.

3. **Exact integer-degree regime.** Completing the square in f gives
   `d0=d_*-Delta_eff/(4U_d)`. The strict nearest-integer condition is
   `|k-d0|<1/2`, equivalent to the displayed interval. For the illustrative
   k=3, Delta=4,U_d=d_*=1, it gives exactly 5<lambda_R<7. The available
   k-regular bipartite trial realizes every local minimum, so this is not
   merely an independently minimized but incompatible degree prescription.
   The note correctly does not substitute those parameters into the
   inherited calculations.

4. **Extensive stability and quantum degree correction.** Since
   `sum d_v^2>=2M^2/N`, the negative quadratic completion costs at most
   `N*max(0,-a)^2/(8U_d)`; the displayed stability constant is correct.
   In the occupied-record/carrier-blank sector, comparison with the
   k-regular trial and the coarse flip bound first yields
   `m/N <= d0+sqrt((k-d0)^2+Omega/(2U_d))=C`.
   Integer convexity gives
   `f(d)-f(k)>=U_d(1-2|k-d0|)|d-k|=gamma|d-k|`.
   Applying the sharper flip expectation next yields
   `gamma <sum|d-k|> <=2Omega sqrt(CN)`.
   Finally `2|m-kN|<=<sum|d-k|>` supplies the factor one half in the
   second bound. Both constants and the O(sqrt(N)) correction are correct.

5. **Backbone retention.** On P, flipping each originally occupied
   backbone edge produces a distinct orthogonal missing-edge subspace.
   Thus `(QHP)^dagger(QHP)=Omega^2*M0*P/N^2`, establishing the exact norm,
   not just a sum-of-norms estimate. The off-diagonal operator H-H_D has
   norm ||QHP||, without an extra factor two. Duhamel's norm bound then
   gives the stated squared probability bound. Other native terms commute
   with P, including incidence-diagonal formation. Mixed states and
   permutation mixtures preserve the connection guarantee by linearity.

6. **Blank formation and new-node incorporation.** The differential
   inequality `|m_dot|<=2Omega sqrt(m)/hbar` can be integrated through
   m=0 using sqrt(m+epsilon) and taking epsilon to zero. It gives exactly
   `m(t)<=(Omega*t/hbar)^2`. For the 2N+1 new links the same argument uses
   the new coefficient Omega/(N+1), giving their stated occupation bound.
   Full connection necessarily needs at least two new occupied edges;
   dividing by two yields the final probability bound. These arguments
   remain valid for time-dependent incidence-diagonal matter terms, but
   not for an omitted incidence-changing preparation port.

## Scientific scope retained

The bounds do not certify that formation achieves its minimum time or that
a connected input is naturally selected. In fact the order-sqrt(N) necessary
formation time and the o(sqrt(N)) near-certain sparse-backbone retention window
cannot simply be combined into a guaranteed growth protocol. At times of
order sqrt(N), the retention bound can be order one. The note explicitly
keeps that unresolved joint formation/retention requirement.

Likewise, k-regularity does not select connectedness; connectedness does not
give physical distance, dimension, causal order or a metric action. The
prepared backbone is an owned excited input with its own energy cost, not
the sparse ground state relabelled as geometry. The example feedback regime
is a separate native parameter-family statement, not a rescue fit.

The proposed N=2,3 numerical census is correctly described as a prospective
implementation check of already proved inequalities. It is not needed for
the analytical proof, and no result from that proposed census was assumed
in this review.

# Independent review: projected source weight at the first degree tie

2026-09-30; `short_path_adversarial`. Source-only reading and independent hand
algebra. No producer import, diagonalization, numerical job, source adoption,
parameter change or ledger edit.

**Verdict: PASS within the exact projected matching model.** No blocking
correction is needed in `NATIVE_DEGREE_TIE_PROJECTED_SOURCE_BOUND_V001.md`, SHA
`77a80c2c28c1eded98190f82bb3f98994d2bd24c4150ea30180263ede48c092a`.
This is not a full-parent theorem, formation result or physical-gravity test.

## Independent checks

1. In the held uniform-record, carrier-free sector, the native local diagonal
   is `U(d-d*)^2+(a/2)d+epsilon_r*q`. The stated tie condition makes the
   linear coefficient exactly `-U`, leaving `c0+U*d*(d-1)`. Summing the local
   energies gives `C_N+2U*C_inc-h*sum X`, with every absolute constant retained.
   For N>=2 the smallest excluded bare configuration has one degree-two vertex
   and cost 2U. The inherited positive-cost branch is not this tuned tie.

2. Fixing all edges outside one vertex's incident star decomposes the matching
   basis into independent blocks: an empty center plus one state for each free
   opposite-layer endpoint. The block is precisely a star adjacency, with norm
   sqrt(r). Empty exterior realizes r=N, so the star norm sqrt(N) is exact,
   not merely a triangle estimate or an assertion about the radial singlet.
   Summing N left stars gives the stated norm bound on the full projected S.

3. All matchings connect to empty by deletions. With h>0, Perron positivity
   therefore gives a unique projected ground invariant under both independent
   layer permutations and layer exchange. Since S has that ground as an
   eigenvector, the S/N term in the anchored source is ground-parallel.
   Consequently its excited weight is `(h^2/4)*Var(S_1)` and is bounded by
   `h^2*N/4=Omega^2/(4N)`. This ground subtraction is necessary.

4. The positive ground-to-excited Gram matrix has a scalar block on each
   within-layer standard representation. Independent permutations prohibit a
   mixed standard block; layer exchange equates the two scalar coefficients.
   Uniform total energy has no ground transitions, and the projected difference
   of the two layer energy sums is identically zero. Thus both singlets vanish
   and `W_u=w_N*Q_u` follows for every real profile. The anchor has
   `Q=(N-1)/N`, giving `w_N<=Omega^2/[4(N-1)]`. The loose bound `Q<=2N`
   for bounded profiles is valid also for odd N. A layer-constant source has
   zero transition weight, not just small weight.

5. For the explicitly positive ground spectral measure, the PLUS-source
   convention `delta<T>=-chi*delta theta` yields the stated sine kernel.
   `|sin|<=1` gives the pointwise time and finite-window bounds;
   `2*Delta/(Delta^2+(hbar*zeta)^2)<=1/(hbar*zeta)` gives the positive
   imaginary-frequency bound. These steps do not require a finite-N spectrum
   or transfer any passive-ground property to a nonstationary preparation.

6. The coarse parent estimate is independently consistent: the integer
   inequality `d<=1+d(d-1)/2` gives `M<=N+C_inc/2`; Cauchy gives
   `|<h sum X>|<=2*Omega*sqrt(<M>)`. The tangent bound
   `sqrt(N+c/2)<=sqrt(N)+c/(4*sqrt(N))` produces the displayed coefficient
   `2U-Omega/(2sqrt(N))`. Empty incidence is an energy-C_N trial state,
   so the conditional O(sqrt(N)) defect bound follows with the stated positive
   denominator. It is not small projection leakage.

## Essential boundaries on the conclusion

The exact source is the derivative of `P sum_v(1+theta*u_v)h_v P` with the
**same fixed P**, complete local energies and adopted affine lapse chart.
That chart has zero raw second contact. A full-parent elimination requires its
own controlled projector/resolvent, dressed source, connection and contacts.
The matching space is not invariant under the parent flips; a bare 2U gap is
not a substitute for that control. No bound derived here may be silently used
as a bound on the complete parent source or its actually formed state.

The static exception is real: `chi(0)=2 integral(dmu/Delta)` is not uniformly
bounded by total weight alone. Gaps may shrink faster than the weight. The
note also correctly excludes undamped real-frequency resonances from its
pointwise bounds. Thus this result blocks an argument based only on growing
mode count/bandwidth, not every possible static mechanism. A projected static
claim still needs source-weighted inverse gaps in the nontrivial layer sectors,
not only radial eigenvalues; a parent claim additionally needs the missing
projection/source control and formation/readout limit.

Position, physical clock, volume, source support and work remain externally
owned premises. The relation `W_Z=w_N*Q_x/c^4` is a normalization identity once
positions are supplied, not an emergent volume or density relation. Holding
dimensionless theta fixed is not holding physical acceleration fixed when the
radius changes. The local identity baseline canceling in a centered transition
does not fix its absolute pressure or volume derivative.

## Reviewed ancestry and next useful decision

Read the complete tie-bound and degree-switch notes, the relevant native
BS06/BS09–BS11 equations and port/clock cautions, the regular-energy source
selector, and the prior uniform-source bound. Key source identities:

- `NATIVE_DEGREE_SWITCH_CHANNEL_V001.md`:
  `bd52d3200aa758613471f9d1053a402d8c3e7560420a3da99357787acf082f23`.
- `../recovered_sources/BS_MICRO_ACTION.md`:
  `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`.

No new numerical sweep is justified by this review. The next substantive
discriminator is a same-source full-parent projection/control bound, or an
explicitly conditional projected inverse-gap theorem with its physical
normalization and limit ordering stated. Neither route may presume a ground
preparation, tuned density threshold, connected geometry or source-independent
pressure that the native formation dynamics has not supplied.

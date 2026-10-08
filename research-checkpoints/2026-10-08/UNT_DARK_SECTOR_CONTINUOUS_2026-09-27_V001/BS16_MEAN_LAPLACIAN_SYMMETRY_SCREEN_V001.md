# BS16 mean-incidence symmetry and heat-window screen V001

2026-09-27. Exact finite-parent algebra; no numerical run, new Hamiltonian,
ground-state assumption, physical metric assignment or cross-parent transfer.

**Result:** for a permutation-invariant single-slab state, the unblocked
BS16 mean-incidence Laplacian has only two positive spectral scales. Fixing
binary record occupations and retaining their within-class permutation
symmetry leaves at most seven distinct positive spectral values, independent
of N. These diagnostics cannot develop a parametrically widening positive-
dimension heat window by increasing N alone. This does not exclude accidental
finite slopes, geometry in higher correlations or symmetry-broken/relationally
anchored states, or a different prospectively specified blocking diagnostic.

## Source and novelty scope

The resident [BS microscopic action](recovered_sources/BS_MICRO_ACTION.md) was
read fully after checking flags; SHA256
`00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`.
BS03 (line 103) is global within-layer permutation symmetry, not a gauge
quotient. Section 2.3 leaves the mission state and ports to be specified.
BS16-BS18 (lines 384-402) define the mean-weight elliptic diagnostic and demand
independent heat/Weyl scaling; BS20 remains an uninstantiated source template.

The resident `SCIENTIFIC_NEXT_CONSTRUCT.md` and
`FORMED_PATTERN_TEST_DESIGN.md` were read; the recovered-parent physical screen,
adopted-action note and resident frontier V004-V008 were checked for this
Laplacian/heat/permutation result. No duplicate derivation was found in that
scoped set. `MEAN_LINK_CLOSURE_SCREEN.md` was dataless and was not reopened;
this is not a claim to have exhaustively searched unavailable older sources.

## 1. Exact fully symmetric single-slab spectrum

Take identity blocking on the raw adjacent-layer possible-link set K_(N,N).
Let rho be invariant under independent permutations S_N x S_N of the two
layers, including the induced action on every state factor needed for that
assertion. Then all edge expectations are equal:

    w_ij=Tr(rho n_ij)=w,       0<=w<=1.

For an incidence matrix with one row per possible edge, orientation signs
cancel from D^T W D. With J the N-by-N all-ones matrix,

    L = w [ N I  -J ] .
          [ -J   N I ]

The all-node constant vector has eigenvalue 0; the difference of the two
layer constants has eigenvalue 2Nw. Vectors of zero sum inside either layer
have eigenvalue Nw and total dimension 2N-2. Thus, for w>0,

    spec(L) = {0, Nw [multiplicity 2N-2], 2Nw}.

The same formulas include N=1 with zero middle multiplicity. If w=0, L=0
and every mode is zero. Put x=Nws. The full and per-node heat traces are

    Z(s)=1+(2N-2)e^(-x)+e^(-2x),       h(s)=Z(s)/(2N),
    d_spec(s)=2x[(2N-2)e^(-x)+2e^(-2x)]/Z(s).

Every vertex heat-kernel diagonal equals h(s), because this L is vertex
transitive. Hence averaging any nonempty fixed subset of vertices gives
the same BS18 diagnostic. Its slope tends to zero at both s endpoints for
fixed N,w>0. A transient value near three is possible; it is not a proof of
three dimensions. The positive eigenvalue ratio stays exactly two for every
N and every nonzero w, including sparse mean scaling w proportional to 1/N.
Changing the rate Nw merely rescales diffusion time.

Removing the zero mode as a separately declared diagnostic does not help:
its slope lies between 2x and 4x. A fixed nonzero slope band then confines
x to a bounded ratio. The zero-mode-inclusive case is also controlled by
the finite-band argument below; its terminal crossover is not a Weyl law.

## 2. A precise finite-band ceiling, not a visual plateau assertion

For any positive heat sum

    H(s)=sum_(i=1)^m a_i exp(-lambda_i s),
    a_i>0, lambda_i>=0,

suppose alpha<=-d ln H/d ln s<=beta on one connected interval
[s_minus,s_plus], with fixed 0<alpha<=beta. Define
f_i=a_i exp(-lambda_i s)/H and y=ln s. At each y some f_i>=1/m, and

    alpha-lambda_i s <= d ln f_i/dy <= beta-lambda_i s.

For lambda_i>0, the part with f_i>=1/m below lambda_i s=alpha/2
lasts at most 2 ln(m)/alpha, since f_i increases at that minimum logarithmic
rate. Above lambda_i s=2 beta it lasts at most ln(m)/beta, since f_i
decreases at least that fast. The intervening y interval has length
ln(4 beta/alpha). A zero-rate term instead has length at most ln(m)/alpha.
Covering the full interval by these m sets proves the conservative bound

    ln(s_plus/s_minus)
      <= m [2 ln(m)/alpha + ln(4 beta/alpha) + ln(m)/beta].

The bound is independent of rates and amplitudes, even if they depend on N.
For a claimed three-dimensional window take
alpha=(3-epsilon)/2, beta=(3+epsilon)/2 with fixed 0<epsilon<3.
With m fixed, its diffusion-time width cannot grow without bound. This loose
bound is not a numerical acceptance threshold and does not reject every
finite approximately three-valued slope interval. It rules out the claimed
parametric widening. The two-scale mean graph has m<=3. The covering proof
received a separate algebraic check from `dark_budget_derivation`; this is
methodological cross-review, not empirical validation.

## 3. Binary record classes: exact finite quotient

Fix a record-occupation pattern q_v in {0,1}. This is a mathematical sector,
not permission to repin or postselect an actually formed state. Partition
each layer into its nonempty occupation classes, with group sizes n_a.
There are k_L<=2 left classes, k_R<=2 right classes, k=k_L+k_R<=4.

Assume the actual state is invariant under the independent permutations
within each group. Then the edge means are block constant: w_ab for a left
group a and right group b. Define each group's weighted vertex degree by

    d_a=sum_(b opposite layer) n_b w_ab.

Every zero-sum vector supported in group a is an eigenvector with eigenvalue
d_a and multiplicity n_a-1. On the remaining group-constant space, choose
the orthonormal basis u_a=1_(group a)/sqrt(n_a). The exact symmetric quotient
matrix is

    Q_aa=d_a,
    Q_ab=-sqrt(n_a n_b)w_ab       (opposite layers),
    Q_ab=0                      (distinct groups in the same layer).

Thus

    spec(L)=union_a {d_a [multiplicity n_a-1]} union spec(Q),
    Tr exp(-sL)=sum_a(n_a-1)exp(-s d_a)+Tr exp(-sQ).

Q is positive semidefinite and annihilates the vector with entries sqrt(n_a).
Disconnected or zero-weight cases add zero modes; no connectedness is assumed.
There are at most k+(k-1)<=7 distinct positive eigenvalues and at most eight
heat rates including zero. Coincidences and size-one groups reduce this count.

For a vertex v in group a the local diagonal is exactly

    <v|exp(-sL)|v>
      =(1-1/n_a)exp(-s d_a)+(1/n_a)[exp(-sQ)]_aa.

Its spectral coefficients are nonnegative. Hence the same fixed-band ceiling
applies to local or region-averaged heat traces, not merely the full trace.
Widely separated group weights can produce several crossovers, but not an
N-parametrically widening positive-dimensional window while k stays bounded.

## 4. What symmetry does and does not establish

Hamiltonian covariance alone does not make a particular state invariant.
Sufficient conditions are an invariant initial state and an entire completed
evolution commuting with the same permutations, including the fixed ports
and controls. A source at a named node can break that symmetry. A covariantly
transformed family of source preparations is not an invariant preparation.
No uniqueness, ground-state preparation or stoquasticity of the full coupled
BS Hamiltonian is used or inferred.

Likewise a sharp binary q pattern does not alone guarantee its stabilizer
symmetry. Writers, carriers, contents, ports or correlations can distinguish
nodes within the same occupation class. For a hold-based sector argument,
the chosen hold must actually preserve that pattern. A superposition or
mixture of different patterns must be analyzed as its full state; the union
of many asymmetric sectors need not retain the four-group form. Conversely
full permutation averaging may restore the two-scale mean graph.

Finally, L built from mean link occupations is not a mean heat kernel:

    exp[-s L(<n>)] is not generally <exp[-s L(n)]>.

Nor is it the exact carrier propagator of the interacting quantum-incidence
parent. Higher link moments and incidence/carrier correlations remain native
physical information. This screen therefore rejects a scaling claim for the
specified mean diagnostic, not every possible geometry in the state.

## Constructive consequence

Before a size-only BS16 calculation, freeze the actual state's symmetry and
the blocking/readout definition. If the raw mean graph satisfies either class
above, its proposed parametrically broad 3D heat window is already excluded
analytically. The useful next question is whether a prospectively owned
state-conditioned or correlation-sensitive construction carries a growing
set of local spectral scales, with all formation outcomes and physical port
anchors retained. Such a change is a distinct diagnostic to authenticate,
not permission to select a favorable branch or fit a geometric embedding.

No q4 Fisher metric, central-edge elastic model, continuum inertia or physical
volume is imported. Composition-layer labels remain nonspatial, as BS states.

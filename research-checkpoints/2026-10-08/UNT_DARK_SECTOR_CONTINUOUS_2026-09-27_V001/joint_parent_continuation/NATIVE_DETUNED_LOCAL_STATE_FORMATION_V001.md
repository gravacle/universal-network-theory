# Native detuning forms local carrier and record correlations

2026-10-03 UTC. The failed static-source test does not make the resonant
degree-2 preparation representative of every native network state. This
note proves what unchanged resonant aging cannot do, then strengthens the
existing detuned population mechanism to unequal local degrees and a
size-independent finite time interval. It uses existing native operators,
actual blank records and closed energy accounting, without a fitted force,
bath reset or substituted lower-energy population.

The uniform-degree kinetic onset and a nonzero complete-source response
were ALREADY established in NATIVE_RECORD_DRIVEN_BAND_POPULATION_V001.md
and NATIVE_COMPLETE_SOURCE_FINITE_TIME_RESPONSE_V001.md. They are not new
numerical discoveries here. The new results are the local unequal-detuning
formula, the earlier matter-record correlation witness and their controlled
finite windows. These concern state evolution on a supplied graph, not
native formation of that graph or a gravitational law.

## Why more aging does not cure the resonant preparation

At degree two and inherited coefficients, delta_v=epsilon_r-lambda_R*d_v=0.
The X_v record operators commute with every fixed-graph node generator
H[L]=sum_v L_v h_v, including time-dependent bounded spatial profiles.
All such generators preserve carrier number Q. In sector z of the joint
record-X basis, a diagonal density block evolves as

    rho_zz(x)=U_z(x) rho_zz(0) U_z(x)^dagger.

Write r_z=Tr rho_zz, D=binom(V,Q), and define

    D_X=(1/2) sum_z ||rho_zz-r_z*I_Q/D||_1.                 (1)

Both r_z and every trace norm in (1) are invariant under this evolution.
The original fixed-Q identity times blank records has D_X=0; its
rho_zz=2^-V I_Q/D. Off-diagonal record blocks still evolve but do not
enter fixed X-diagonal readouts. Every carrier-only readout and fixed
conjugate node energy consequently has constant baseline expectation,
independent of the applied profile or the amount of resonant aging.

This does not erase source-weighted readout contacts, switching work,
record-coherence outputs or the full dynamic-incidence energy. It also
does not erase mixed preparation response, since sigma_0*M_B is not an
identity block. These qualifications explain why the six-cycle experiment
was meaningful despite its ordinary-response null.

More generally, for a fixed X-diagonal observable O and infinitesimal
sector-preserving source V(x), the absolute response obeys

    |delta<O>| <= 4 D_X ||O|| integral
                 max_z inf_(alpha real)||V_z(s)-alpha I|| ds.    (2)

The tracial block gives zero commutator; trace duality and the commutator
norm prove (2). Subtracting scalar sector energies here is a bound on a
commutator, not removal of absolute source work. Nonzero D_X is necessary
for such a response, not sufficient for a physical energy-source law.

## Detuning is already an operator in the native model

On a supplied bounded-degree graph retain the complete carrier Hamiltonian
H_c, including storage, current-square interaction and hopping -t*T_uv,
and all record terms

    H=H_c+sum_v [delta_v r_v+w X_v+g p_v X_v],
    delta_v=epsilon_r-lambda_R*d_v, w=g_w, g=g_p.           (3)

Scalar graph/writer energies remain in total work. The fixed one-content
sector is invariant; no unoccupied second content is added as a hidden
environment. Initial carriers are I_Q/D, records are actually blank and
writers have the declared common content. Uniform filling is rho=Q/V.
Nonzero detuning does not conserve X_v, so the premise of (1)'s invariance
is genuinely absent, without changing a coupling to fit a desired result.

The first local correlation is

    <(p_v-rho)X_v>(x)=-delta_v*g*rho*(1-rho)*x^2+O(x^4). (4)

This is a fixed-initial-density correlation witness; it is not a claim
that the later marginal <p_v> remains exactly rho on a nonregular graph.
The three local order-x^2 energy changes have coefficients

    delta_v <r_v>: delta_v*[w^2+(2*w*g+g^2)*rho],
    w <X_v>:      -delta_v*w*(w+g*rho),
    g <p_v X_v>:  -delta_v*g*rho*(w+g).

They sum to zero. The effect transfers energy and information among the
already retained registers, not from a free thermostat. Initially blank
records are an ordered preparation resource; its origin is still due.

The witness implies

    D_X >= |<(p_v-rho)X_v>|/[2 max(rho,1-rho)].             (5)

Every tracial diagonal block gives zero for that operator, whose norm is
max(rho,1-rho). Equation (5) is just trace duality; nonzero correlation
does not automatically ensure a useful gravitational susceptibility.

## Carrier coherence with unequal local degrees

Direct expansion of the actual reduced carrier state gives

    rho_C(x)=I_Q/D+(g^2*x^4/(6D))
                        sum_v delta_v[p_v,[H_c,p_v]]+O_N(x^5)
            =I_Q/D+(g^2*t*x^4/(6D))
                        sum_edges (delta_u+delta_v)T_uv+O_N(x^5). (6)

The matrix remainder in (6) is finite-size; a global trace-norm
thermodynamic estimate is not asserted. Diagonal current and storage
operators commute with p_v and so drop out of this coefficient, not from
H_c. The writer coefficient cancels at this order only.

One derivation expands the two carrier-copy insertions while retaining
the actual record dynamics. The leading commutators are

    [p_v(s),p_v(u)]=i(u-s)[p_v,[H_c,p_v]]+higher orders,
    <[X_v(s),X_v(u)]>_blank=2i*delta_v*(u-s)+higher orders.

Their product in the second interaction-order integral yields (6).
Two copying insertions, one detuning insertion and one hopping insertion
exhaust that order. Purely record driving cannot by itself alter the
identity carrier state. This is not replacement of the record by noise.

For s=Q(V-Q)/[V(V-1)], Tr(T_uv^2)/D=2s, while distinct single-edge
transfers have zero pair trace. Thus the LOCAL, norm-one readout has

    <T_uv>(x)=c4*x^4+O_N(x^6),
    c4=g^2*t*s*(delta_u+delta_v)/3.                        (7)

Reality of the initial state, H and T makes this expectation even in x.
For uniform detuning, summing -t*T_uv reproduces the existing kinetic
formula exactly. With inherited coefficients,

    delta_u+delta_v=2-(d_u+d_v)/2.

Degree-1/degree-1 edges favor negative kinetic energy initially;
degree-3/degree-3 favor positive kinetic energy. Degree-1/degree-3 and
degree-2/degree-2 edges cancel in (7). This cancellation is not a general
all-time null: (4) can already be nonzero on a degree-1/degree-3 edge.
Graph degree is not yet a calibrated astronomical density.

## A uniform finite interval rather than an isolated Taylor term

Use a node decomposition H=sum_Z h_Z with |Z|<=2 and
J=sup_v sum_(Z containing v)||h_Z|| finite independently of graph size.
Node registers at a vertex count as one support site. Bounded degree and
fixed microscopic coefficients give such a J. Scalar identity terms may
be retained for a looser bound; their energies are never removed from work.

Iterating local commutators gives

    ||ad_H^k O_X|| <= (2J)^k (|X|)_k ||O_X||,

where (m)_k=m(m+1)...(m+k-1). For the two-site T, the sixth-order
Taylor remainder is at most (2J)^6*(2)_6*x^6/6!, so

    |<T_uv>(x)-c4*x^4| <= 448 J^6 x^6.                   (8)

Whenever c4 is nonzero and x^2<=|c4|/(896 J^6),

    sign(c4)*<T_uv>(x) >= |c4|*x^4/2,
    D_trace(rho_C(x),I_Q/D) >= |c4|*x^4/4.               (9)

At fixed interior filling, bounded degree and an edge with detuning sum
bounded away from zero, this is a size-independent nonzero time interval.
It does not prove long-lived collective transport or a low-frequency law.

The one-site witness A_v=(p_v-rho)X_v similarly has c2 from (4) and
norm m=max(rho,1-rho). Its fourth-order remainder is bounded by
16 J^4 m x^4. For x^2<=|c2|/(32 J^4 m), it has the sign of c2 and
magnitude at least |c2|x^2/2; hence D_X>=|c2|x^2/(4m). This establishes
finite-time exit from the tracial X-block restriction even when (7)
cancels. Neither bound assumes a uniformly bounded full incidence norm.

The existing full-parent/local-node comparison can transfer a selected
finite signal only when its explicitly evaluated local error is smaller
than that signal. For equal-clock statements also include the previously
bounded phase-to-age alignment error; the isolated clock has reference
phase sqrt(5)*x. No derivative/large-size limit is exchanged. The physical
graph-weighted hopping n_uv*T_uv additionally needs its wrong-link
correction; a bare node coherence is not silently that energy observable.

## Spatial phase work of the generated state

There is a concrete SPATIAL phase-work consequence, distinct from the
temporal lapse test. At an actual age x apply the explicitly owned carrier
phase operation U_lambda=exp(i*lambda*sum_v f_v p_v) to the state, with
real fixed f. All node terms except hopping commute with this operation.
The state-twist identity itself is the earlier native transport-phase
work identity, also retained in NATIVE_COLLECTIVE_CARRIER_PHASE_CANDIDATE_V001.md;
the new conclusion uses the actual finite-density coherence and its bound.
For the COMPLETE state energy E(lambda)=Tr(U_lambda rho(x) U_lambda^dagger H),

    kappa_f(x)=E''(0)=t sum_edges (f_u-f_v)^2 <T_uv>(x)
      =(g^2*t^2*s*x^4/3) sum_edges
                         (delta_u+delta_v)(f_u-f_v)^2+R_f,
    |R_f|<=448*|t|*J^6*x^6 sum_edges (f_u-f_v)^2.         (10)

The first-order current work need not vanish; symmetric opposite twists
cancel it. Equation (10) is the instantaneous work curvature of the
actual prepared state, not an equilibrium helicity modulus, a pure-gauge
field energy or an identified metric. Its controller must supply or
receive the displayed work. Conjugating both state and Hamiltonian as a
mere change of basis would be a different, work-free operation.

In the inherited regular degree-3 node branch, delta=-1/2 and t>0,
every edge curvature is negative throughout the sign-certified window
of (9). For every f nonconstant on a connected component, kappa_f<0.
At least one of the two sufficiently small opposite phase operations
can lower the energy; this state is not passive under these operations.
The degree-1 branch has positive leading curvature but its regular graph
is a collection of dimers, not an extended gravitational medium. Local
detuning sums, not record mass, control this leading distinction. A zero
sum edge gives no sign conclusion from this order.

This directly tests a premise of a stable collective carrier-phase
description. We cannot import a positive phase-gradient coefficient into
the early degree-3 state while dropping its measured sign and memory.
The result neither forbids later stabilization nor supplies the response
of a different aged, driven or formed background.

## The scientific decision and next calculation

The resonant identity preparation cannot become responsive just by waiting.
The existing native detuning does generate correlations and carrier
coherence in the original ordered-record preparation. We therefore do
not need to invent a cooling bath or a favorable occupation distribution
to obtain SOME nontracial matter. These statements answer different
questions and must not be collapsed into a universal formation failure.

The remaining decisive question is whether this actually generated state
has a controlled, common coarse energy-source description of propagation,
with the required sign and spectral weight. The saved degree-3 result has
an upward kinetic bias and energy-weighted soft population, not the
assumed passive lower-band state. More coherence alone is not a cure.
An arbitrary temporal source fit or resetting to a lower band would merely
insert the missing mechanism.

Continue from the detuned actual-state equations, V115's complete source
current and finite-window bounds, and the mixed-memory source formulas.
Use the generated state's carrier phase work (10) together with the
complete temporal energy-source response. Determine whether a declared
aged/coarse window admits a stable shared phase reduction, retaining
the two-time correlations and source-dependent memory. First derive a
bound or sign witness for that retained response; do not posit positive
stiffness or a passive population. A phase-work operation is not by itself
the missing spatial ruler or a calibrated gravity source.
Do not rerun the saved uniform-degree kinetic onset, resonant sectors or
failed static fit. Physical source normalization, ruler/volume, native
geometry formation, galaxy/expansion joint prediction and Stage 3 remain
separate outstanding requirements.

The unequal-detuning coefficient was derived independently by two existing
source-only reviewers. Root supplied the local finite-window bounds, whose
constants and scope v005_resume_review checked. No numerical job was used
for this extension. Review is internal, not external scientific validation.

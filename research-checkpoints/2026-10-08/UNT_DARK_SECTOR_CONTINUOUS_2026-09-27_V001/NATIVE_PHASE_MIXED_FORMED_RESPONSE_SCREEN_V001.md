# Prospective phase-ensemble screen of the actual formed N=2 states

2026-09-27. Analytical handoff, not an executed diagnostic. Continue only
from the three actual states and unchanged coefficients frozen in
`formed_network_response/PROTOCOL.md`. Frontier V023 and its result receipt
were read: the actual-age common-kernel check passed, but did not establish
stationary or passive response. No ground-state reset, cooling, bath,
postselection, new formation time, or new microscopic coefficient is proposed.

## 1. Exact phase averaging preserves preparation populations

For each existing formation arm T/2,T,2T, let rho_F be its complete actual
32-dimensional state immediately after copying is switched off. Retain the
measured switching work. Write the hold Hamiltonian's DISTINCT energy
projectors as H=sum_E E P_E. The infinite uniform waiting-age comparator is

    rho_inf=lim_(W->infinity) (1/W) integral_0^W
                         exp(-iHt/hbar) rho_F exp(iHt/hbar) dt
           =sum_E P_E rho_F P_E.                            (1)

Use projectors onto entire degenerate energy spaces, not separate arbitrary
eigenvectors. In particular, (1) preserves coherences within a degenerate
space. It leaves energy, q occupation, and every other conserved expectation
unchanged; it is not relaxation to the ground state.

Operationally, a finite unrecorded uniform wait has, in any energy basis,

    (rho_W)_ab=(rho_F)_ab exp[-i(E_a-E_b)W/(2hbar)]
                         *sinc[(E_a-E_b)W/(2hbar)],         (2)

with sinc(0)=1. A generic multi-gap graph has no single period whose uniform
average is exactly (1). The existing durations W=T/2,T,2T may be reported
as finite-window comparisons without selecting one for favorable signs.
For the pure prepared state, a conservative trace-norm error bound is

    ||rho_W-rho_inf||_1 <= sum_(E!=F) sqrt(p_E p_F)
                   *min{1,2hbar/[W|E-F|]},
    p_E=Tr(P_E rho_F).                                     (3)

Small gaps can make the operational averaging time long. Exact projector
dephasing alone does not demonstrate finite-time stationarity.

The hold and all proposed edge sources/readouts commute with q. Cross-q
coherences, even if retained by an exact degeneracy, are invisible to those
particular observables. One may exploit that selection rule computationally,
but must sum the original UNNORMALIZED q blocks, not condition on success
or replace q by its mean. Keep the full state for other possible probes.

## 2. Kubo response with correct degenerate-state treatment

Inside each P_E block, diagonalize P_E rho_F P_E. This gives a simultaneous
H,rho_inf basis |a>, with energies E_a and nonnegative probabilities p_a.
The p_a are the prepared weights, not Boltzmann weights and not a function
chosen to decrease with energy. Zero-weight vectors in a degenerate block
must remain in the basis. For source -sum_f f_f n_f,

    chi_ef(u)=(i/hbar)theta(u) Tr rho_inf[n_e(u),n_f],
    chi_ef(omega)=sum_ab (p_a-p_b)(n_e)_ab(n_f)_ba
                         /[E_b-E_a-hbar(omega+i0)].        (4)

The unordered product is Tr[rho_inf n_e(u)n_f]; the rightmost n_f acts
first. Do not turn it into a normalized conditional measurement. This
ordering also fixes the sign of the independent exp(+i theta n_f) kick.

Before taking a static limit, score the possible zero-gap contribution:

    N_e^0=sum_E P_E n_e P_E,
    J_ef=(i/hbar)Tr rho_inf[N_e^0,N_f^0].                   (5)

A nonzero J gives a constant retarded time-kernel term and an
i J/(omega+i0) term. It must not be silently discarded as division by
zero. J is real antisymmetric, so a single real source's self-response
has no such pole, while cross-responses may. If J vanishes within the
validated numerical resolution, the finite regular static Kubo matrix is

    K_ef=2 sum_(E_b>E_a) (p_a-p_b)/(E_b-E_a)
                              *Re[(n_e)_ab(n_f)_ba].       (6)

Even otherwise (6) defines the regular symmetric part, not the entire DC
matrix. No zero eigenvalue of K should be inverted without identifying
its null space. Susceptibility does not supply an absolute energy constant
or an independently defined physical stress/volume.

Exact degeneracies must be established or explicitly treated as unresolved
numerically. Report spectral gaps, cluster spreads, projector residuals,
and sensitivity to a predeclared clustering tolerance. Do not merge a small
nonzero gap merely to remove a large response. An unresolved degeneracy
makes the infinite-wait/static conclusion conditional; finite (2) remains
well-defined and avoids an arbitrary sharp dephasing cutoff.

## 3. Test passive response, do not assume it

For each distinct positive transition gap Delta, form the Hermitian matrix

    A_ef(Delta)=sum_(E_b-E_a=Delta)
                     (p_a-p_b)(n_e)_ab(n_f)_ba.             (7)

This is the positive-frequency absorptive spectral weight, up to the common
Fourier normalization. Equivalently, it is the difference between the
prepared downward and upward transition-weight Gram matrices. Equal-gap
terms must be combined before judging a source direction. Populations
from both q sectors retain their original weights.

Nonnegative A(Delta) for every positive gap establishes LINEAR passivity
for these four incidence sources, including phase-shifted drives. It does
not establish complete thermodynamic passivity under arbitrary controls.
A negative eigenvalue identifies an accessible frequency/source direction
with stimulated energy release. Population inversion in a transition to
which every n_e has zero matrix element is not an active direction for
this experiment.

Also report eigenvalues of K, the uniform scalar 1^T K 1, the vertex
projection C K C^T, and the corresponding line-weight projections. A
positive static matrix alone does not prove passivity at every frequency:
positive and negative line weights can cancel. Conversely a negative
static direction requires a negative accessible absorptive contribution
somewhere in the positive-gap sum. No result is known before execution.

If a passive common response is found, the already tested operational
identities use this SAME kernel: insertion coefficient response is
-lambda_R^2 C K C^T, fresh-carrier curvature response is
t_hop^2 lambda_R C K C^T/hbar^2, and the homogeneous edge-source response
is 1^T K 1. No second fitted local/cosmic response function is introduced.
If an active direction is found, the constructive interpretation is a
prepared nonequilibrium resource with signed source work, using (2) or the
actual two-time kernel—not a positive-stiffness ground state assigned by fiat.

## Next frozen worker, if authorized to continue

Reproduce and hash-check the existing three states; keep source work and
energy. Check (1), trace/positivity, [rho_inf,H]=0, q/energy preservation,
and the q selection rule. Compare direct commutators, (4), and projector
kicks at predeclared lags. Report (5)-(7) and their local/uniform projections
without a gate demanding a favorable sign. Compare finite (2) at the
existing three widths, with (3) reported rather than assumed small.

No numerical worker was launched for this note. The primary unresolved
question is whether the ACTUAL prepared populations support accessible
passive response; stationarity, record persistence, and successful copying
alone do not answer it. A positive answer would still not establish a
universal clock, gravity, cosmological expansion, or large-N graph formation.

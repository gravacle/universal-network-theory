# Prospective numerical spectral diagnostic for energy source age averaging

2026-09-30. Root-only execution after complete source review, independent
preflight and exclusive freeze. This is a small NUMERICAL DIAGNOSTIC, not
an exact-degeneracy, passivity or low-frequency-window certificate.

## Fixed scientific input and census

Authenticate the complete autonomous-volume result and the saved energy-dipole
result, both canonical payloads, their freezes and every frozen source hash.
Use the saved A/B full real symmetric 96D Hamiltonians and saved complete
energy/source/contact matrices. Do not import either producer. Sum the saved
local energies back to each Hamiltonian. Keep both controller energies.

Use all four original basis-vector preparations, A/B times minus/plus, and
check the saved states at all five old times0,.01,.02,.04,.08 for norm and
conserved numerical energy-basis populations. The later states are checked,
not propagated again or substituted for selected favorable preparations.

The physical source coordinates are the analytic note's dimensionless
lambda=(alpha,eta), alpha=gamma0*a_ext, with

    G=(Z/gamma0,-B_eta),
    C_00=0, C_01=C_10=H_aeta/gamma0, C_11=H_etaeta.

Keep gamma0 symbolic and hbar=1 in inherited microscopic units. Response to
PLUS lambda_i G_i uses <C>-chi. No incidence/carrier-density substitution,
physical clock calibration, a0, astronomical datum or fitted state is allowed.

## Exactly two eigensolves and all raw information

Call numpy.linalg.eigh exactly once per Hamiltonian, dimension96. No other
eigensolver, SVD, matrix exponential, time evolution, external data, fit or
precision dependency is added. Preserve every returned eigenvalue and vector.
Check every eigenpair residual, full orthogonality, Hamiltonian reconstruction,
and source/contact basis transformation and reconstruction. Use Frobenius
norms as numerical upper-bound inputs for operator norms, without a hidden
spectral-norm eigensolve.

Store every source/contact matrix in that numerical eigenbasis. For each
initial preparation store all complex coefficients and their full96-by96
density matrix, including coherences; it must reconstruct the original state.
Store all4560 unordered eigen-index pairs per model with their numerical gap
and source elements. Each preparation retains its4560 complex pair coherences
and trace-norm inputs. No pair is discarded for weak weight, sign or gap.
This is enough for subsequent continuous sinc/divided-difference readouts
without another eigensolve. No T,L,kappa or physical-frequency grid is chosen
or evaluated here.

## Numerical resolution is not exact degeneracy

For model H define one prospective numerical-resolution half-width

    delta_num=2e-10*max(1,maxabs(H),maxabs(eigenvalues)).

Each numerical eigenvalue receives [E-delta_num,E+delta_num]. Connected
overlapping neighborhoods are labelled UNRESOLVED NUMERICAL CLUSTERS.
These neighborhoods are not rigorous inclusion intervals and clusters are
not exact spectral projectors. Preserve all individual vectors, values,
coherences, gaps and cluster membership. No small gap is replaced by zero.
Every positive transition gap is likewise retained; overlapping transition
gap neighborhoods are descriptive resolution groups, not exact equal-gap
groups or passivity decisions.

If any energy cluster has more than one index, withhold rho_d, all stationary
pair residues, inverse-gap coefficients and age-bound constants. Their fields
are null with an explicit reason. Do not dephase within an unresolved cluster
or form a reciprocal from its uncertain splitting. Full raw pair and coherence
data remain available for finite-readout methods with continuous limits.

If every energy level is separated at this numerical resolution, report the
following only as UNCERTIFIED NUMERICAL NONDEGENERATE DIAGNOSTICS:

    p_i=|c_i|^2, rho_diag=V diag(p) V^T,
    M_ij=(p_i-p_j) g_ij g_ij^T,  g_ij=(G_0ij,G_1ij), i<j,
    chi0=2 sum M_ij/(E_j-E_i),
    chi2=2 sum M_ij/(E_j-E_i)^3,
    moment=2 sum (E_j-E_i) M_ij,
    age_bound(T)=min(2,2 sum_(i<j)|rho_ij|
                                      min[1,2/((E_j-E_i)T)]),
    sum5=sum ||M_ij||_F/(E_j-E_i)^5.

The ungrouped sum5 is a conservative analytic remainder input if the assumed
eigendata were exact. This run does not certify that premise. All raw signed
M_ij remain; no individual line is called physically resolved or passive.
Check the moment matrix against independent full-matrix double commutators
evaluated in the numerical rho_diag, and retain its contact means and <C>-chi0.
The output does not claim that the actual system was dephased or prepared in
rho_diag. A negative saved instantaneous moment is not its averaged moment.

Every physical, exact-degeneracy, rigorous-gap, stationary-state, passivity and
readout-window qualification flag remains FALSE, even if all numerical checks
pass and no cluster is unresolved. A numerical residual/orthogonality check is
not a directed-rounding or interval proof. Report failures and null outputs;
do not increase resolution allowances to obtain reciprocal values.

## Frozen arithmetic and custody

All arithmetic checks use 2e-10*max(1,maxabs(actual),maxabs(expected)), except
explicit norm/count/initial-vector absolute controls using2e-10. Signs are
descriptive, never correctness gates. Required counts: two96D eigensolves,
four initial states, twenty saved states, 4560 pairs per model and per case.

One process, all numerical-library thread limits1; CPU soft60s/hard65s,
between-operation wall60s/self-RSS512MiB guards, at most4096 numerical checks,
32MiB per input/result bound. Root must supervise the actual wall limit;
between-operation guards cannot interrupt a blocked library call.

--freeze exclusively publishes a manifest of this protocol, source, analytic
note/review and all inherited pinned inputs. --run first authenticates it and
publishes an exclusive durable INTENT receipt before numerical work. An old
intent blocks a second invocation, including after interruption; root must
preserve it and decide a separately labelled attempt rather than silently
rerun. Capture root stdout/stderr and exit status. The result contains actual
CPU/elapsed/self-RSS, NumPy version, partial evidence on caught failures and
its canonical payload hash. Resource counts are computational, not physical.

With no --output, --run emits the full result JSON to stdout. --output may
only name the fixed previously absent result path. The publisher writes and
fsyncs a same-directory temporary file, atomically hard-links it to the
exclusive final path, fsyncs the directory, and removes only its own temporary
name. A race never overwrites an existing result. Intent, freeze and failed
evidence are not deleted. Old producers/results and unrelated files are not
modified. A partial result after a fatal signal may be limited to the durable
intent and root capture; no successful completion is inferred from that.

The root runs only after review. This authoring step performs no import,
compilation, freeze or numerical execution. All eleven scientific lanes
remain open; no Stage 3, continuum, formation or observational conclusion
follows from this diagnostic.

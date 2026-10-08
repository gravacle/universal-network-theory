# Prospective blank-pair creation-work test

2026-09-29. Additive test of `NATIVE_AUTONOMOUS_CONTROLLER_CANDIDATE_V001.md`.
Frozen before execution. This is the clamped-coordinate, finite-supply sector
of that candidate, not a simulation of its continuous quantum piston, not
physical volume emergence, and not a cosmological expansion calculation.

## Model and independently chosen test inputs

Use the exact all-register-blank invariant incidence sectors of BS06 at N=1
and N=2 (2 and 16 states). Keep Omega=1, Delta=4, U_d=1, d_star=1 and the
native h_N=Omega/N. Bit e=i*N+j is its declared link label. The inclusion I
retains the old (0,0) bit and puts all three new links in zero. Registers
remain blank; none of the already formed record preparations is replaced.

The conditional port parameters are fixed engineering examples, not values
derived from BS or inferred from data: K_g=2, K_V=3, C=1/2, gamma=1,
v_cell=1/4, supply gap Delta_s=3, creation amplitude epsilon=1/5, hbar=1.
The bare stiffness matrix is positive. Use every pair of clamped coordinates
g in {0,2/5}, V in {1/2,4/5}. These remain fixed throughout each run.

For each n, B_n is total link occupation and
U_n=K_g*g^2/2+C*g*(V-2*n*v_cell)+K_V*(V-2*n*v_cell)^2/2.
The full 36-state Hamiltonian, including both supply states in both sizes, is

    H = (H_native - gamma*g*B + U) tensor I_supply
      + Delta_s I_native tensor |1><1|
      + epsilon*(J tensor |0><1| + J^dagger tensor |1><0|),

where J has I in the size-raising block. This tests conserved size+supply
charge as a nontrivial full-operator identity, rather than imposing a single
charge sector and testing its constant identity operator. No drive, bath,
oscillator truncation, or omitted reverse transition is present.

## Prospective census and checks

Use old-link states |0>, |+>, and (|0>+i|1>)/sqrt(2). For each, prepare
S=old state with occupied supply; T=its blank-included state with empty
supply; and (S+iT)/sqrt(2), (S-iT)/sqrt(2). This gives twelve preparations.
At every clamped point retain all times {0,1/4,1/2,1,2}: 240 rows.

Check exact matrices for Hermiticity, charge conservation, source-strength
moment, inclusion compression and full off-inclusion defect, and its singular
values. Verify the force/contact derivatives using exact quadratic finite
differences of the separately assembled full Hamiltonian (step 1/8). Verify
the target-minus-source pressure jump K_V*(2*v_cell).

The compressed target-minus-source detuning must equal

    2*U_d*d_star^2 I + Omega*X_old/[N(N+1)] - Delta_s I
       + 2*v_cell*p_source I + K_V*(2*v_cell)^2/2 I.

Do not discard old-link normalization work or the three new-link leakage
channels. Verify the initial first, second and third creation derivatives
in pure S: 0, 2*epsilon^2, 0. Opposite phase preparations must have opposite
initial currents of magnitude epsilon; no positive growth sign is fitted.

For each row, compare full dense eigensystem propagation with an independently
implemented scaled-Taylor matrix exponential; check norm, unitarity, conserved
total energy and charge, component-energy sum, and sum of commutator energy
currents. Retain native, source, elastic, supply and creation component energies
separately, including their initial values. Record both size probability and
actual incidence-graph connection probability: an added blank pair is not a
connected larger space. Keep all results regardless of sign.

Acceptance is absolute 1e-10 for these finite matrix identities/conservation
checks, 1e-9 for the nested third derivative. These are numerical consistency
tolerances, not observational acceptance thresholds. No time, coefficient,
preparation or tolerance is selected after seeing results.

## Custody and resource scope

Root alone runs the worker. Maximum matrix is 36 by 36; no heavy memory job,
new installation or new infrastructure. This short job can be rerun after an
interruption. The worker authenticates its prospectively saved source/protocol
and analytical inputs, writes results only to stdout, and reports all checks.
Root preserves raw JSON using normal file editing. An independent review
checks equations, census and saved evidence. A pass supports this declared
finite source-work implementation, not selection of its physical constants or
Stage 1/2/3 completion.

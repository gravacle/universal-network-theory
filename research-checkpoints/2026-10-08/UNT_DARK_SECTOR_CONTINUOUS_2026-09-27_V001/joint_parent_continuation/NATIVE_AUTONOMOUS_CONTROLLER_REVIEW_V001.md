# Independent review: native source/volume controller

2026-09-29. Read-only analytical review; no numerical worker, changed
candidate/source, parameter choice or physical-volume identification.

## Finding

The finite-size candidate has a consistent creation-work identity,
controller force/contact ledger and native recoil coefficient. These
claims can be checked in the proposed small clamped operator experiment
without approximating a full quantum piston. The stationary susceptibility
formula is valid with the biased-equilibrium and linearization conditions
specified below; it must not be used as an automatic stationary reduction
of the actual source-free formed state.

Reviewed candidate:
`NATIVE_AUTONOMOUS_CONTROLLER_CANDIDATE_V001.md`, SHA-256
`a26f23fd0ee5170747a2cb11c4addd8c97c56ec9ae33cd338895f5fdc6c72629`.
Its original native inputs are identified in
`NATIVE_RECORD_CONNECTIVITY_PATHWAY_V001.md` and the candidate. This is a
reviewed-source identity, not a numerical freeze or completed piston run.

## 1. Creation detuning and reverse process

Let `d=2 v_cell`, `z=V-V_N`, `p_N=-(C g+K_V z)` and retain the candidate's
positive quadratic controller energy. Direct subtraction at the same g,V
gives

\[
 U_{N+1}-U_N=-d(Cg+K_Vz)+\tfrac12K_Vd^2
            =d p_N+\tfrac12K_Vd^2.
\]

The sign and finite-displacement term are correct. This is not the work
of a quasistatic pressure-only path. With blank new links,
`B_(N+1) I_N=I_N B_N`, so the identical source insertion cancels from
the intertwining difference. The supply loses its gap `Delta_s`. Combining
these facts with the exact native inclusion yields

\[
 D_N=2U_dd_*^2+\frac{\Omega S_X}{N(N+1)}-\Delta_s
     +d p_N+\tfrac12K_Vd^2,
\]
\[
 H_t\mathcal I_N-\mathcal I_N H_s
 =\mathcal I_ND_N-\frac{\Omega}{N+1}
     \sum_{e\,new}X_e\mathcal I_N.
\]

The off-inclusion images are orthogonal, with norm
`Omega sqrt(2N+1)/(N+1)`. Thus a mean detuning of zero is not a sharp
resonance or an eigenstate embedding. The retained degree baseline, old
flip-normalization work, controller displacement and supply energy have
all been counted once. At the initial preferred volume and g=0, the
elastic contribution remains positive even though old pressure is zero.

For `T=I_N tensor b`, `[n,T]=T` and the total charge
`n+b^dagger b` commutes with the full Hamiltonian. The current is
`2 epsilon Im<T>/hbar`, with the stated sign. If the initial state lies
wholly in the source-size/supply-excited sector, the leading transition
probability is `epsilon^2 t^2/hbar^2`. The cubic probability term vanishes:
the interference coefficient contains the expectation of the Hermitian
operator `I_N^dagger H_t I_N+H_s`. The stated `O(t^4)` remainder presumes
the corresponding higher moments/domain conditions. Reverse transitions
and exhaustion of the finite supply are correctly retained.

This validates a finite two-size conditional creation channel, not an
irreversible growth law. Furthermore, its newly blank incidence qubits
do not immediately connect the new nodes. The independently derived
connectivity note gives the necessary incorporation-time bound.

## 2. Controller derivatives, quantum volume and native recoil

For `V=V_ref exp(q)` and `[q,Pi]=i hbar`, the equations

\[
 \dot\Pi=Vp,\qquad
 \dot V=\frac{\{V,\Pi\}}{2I_q}
\]

follow directly from the canonical commutators. Omitting the V factor
would confuse the q-conjugate momentum with a V-conjugate one. The stated
pressure is the candidate's internal force conjugate to its operational
chamber volume; neither this commutator nor an extensive node energy
identifies a relativistic stress tensor.

The full source derivatives are exactly `H_gg=K_g`, `H_gV=C` and
`H_VV=K_V`. These are physical controller terms in this proposed
completion, whereas the native diagnostic insertion `H-fB` has zero
second f derivative. The two claims do not conflict. The strictly
positive quadratic matrix, positive controller kinetic energies and
finite bounded native/creation operators give a semibounded finite-size
Hamiltonian. Its q direction need not be confining as q tends to minus
infinity; semiboundedness is not a claim of a bound piston ground state.

Every new controller term commutes with B. The creation term also
commutes with B because of the inclusion intertwiner and its adjoint.
Consequently

\[
 [B,[H_{tot},B]]=igoplus_n\frac{\Omega}{n}
                 \sum_e b_e^2 X_e.
\]

This native strength remains signed and state dependent. For the one-link
source impulse `exp(+i eta n/hbar)`, initial changes in g, g-dot and
g-double-dot vanish for matched initial controller states. The change in
the third derivative is

\[
 \delta\langle g^{(3)}\rangle_0
 =\frac{\gamma\eta h}{M_g\hbar^2}\langle X\rangle_0
   +O(\eta^2).
\]

Integrating its Taylor coefficient gives the candidate's positive
`gamma eta h <X> t^3/(6 M_g hbar^2)`. This is a direct nested-commutator
readout and does not presume a stationary state, a passive population,
a constant reduced Bloch radius, or a physical spacetime calibration.

## 3. Required meaning of the stationary kernel

For the separate fixed-N, `epsilon=0` approximation, let g_e,V_e be a
classical/narrow-actuator equilibrium and rho_e its stationary native
state. The self-consistency conditions are

\[
 H_e=H_N-\gamma g_eB,\qquad [\rho_e,H_e]=0,
\]
\[
 V_e=V_N-\frac{C g_e}{K_V}>0,\qquad
 \left(K_g-\frac{C^2}{K_V}\right)g_e
       =\gamma\operatorname{Tr}(\rho_e B).
\]

The susceptibility is the retarded response of this **biased** H_e and
these actual stationary populations. A state stationary for H_N generally
fails that condition at nonzero g_e. No unchanged source-free stationary
population may be substituted without checking it. There is also no
guarantee that the nonlinear equilibrium equations have the desired
solution; their existence is a calculation for the specified port/state.

With this meaning, p_e=0, `M_V=I_q/V_e^2`, and a valid small-fluctuation
closure, the linear response is

\[
 \begin{pmatrix}
 K_g-M_g\omega^2-\gamma^2\chi_{BB}(\omega)&C\\
 C&K_V-M_V\omega^2
 \end{pmatrix}.
\]

The static Schur complement is therefore correctly
`K_g-C^2/K_V-gamma^2 chi_BB(0)`. This is not an identity enforcing
criticality. Retarded analytic continuation and pole/zero cancellations
must be retained when extracting coupled modes; native modes orthogonal
to B are not diagnosed by this two-coordinate kernel alone. Positive
bare stiffness is insufficient to guarantee the response of an active
state. The zero-frequency value also presumes a finite susceptibility
and the specified response/order of limits, rather than an unannounced
thermodynamic repopulation.

Actual saved formed states are generally nonstationary. For them the
appropriate native object is the two-time response around the evolving
biased/controller history. A full entangled quantum actuator cannot
automatically be reduced to these two classical mean coordinates.

## 4. Small test scope

The proposed blank-register N=1 to N=2 test uses native link dimensions
2 and 16; its conserved-charge creation block has dimension 18. It can
check the detuning/intertwiner, charge and full double commutator exactly
at fixed g,V, including all two-dimensional old-link states at operator
level. Such a check does not approximate an infinite-dimensional
quantum piston or establish its stationary spectrum. Native formed-state
recoil can separately use the existing 16-state matrices and symbolic
canonical commutators without claiming that a truncated oscillator
globally satisfies `[g,P_g]=i hbar`.

No blocking algebraic defect was found in these operator identities.
The construction removes the contact/pressure ambiguity only after its
complete port calibration is adopted or measured. It does not derive
that calibration, connected physical volume, cosmological abundance or
the galaxy-law interface from the source-free seed.

## Prefreeze clarification received

The author subsequently made the biased-state/equilibrium conditions in
section 3 explicit in the candidate itself. I read that revised section;
it agrees with this review. The clarified candidate's SHA-256 is
`69dc91bbc08550481759b8b1646124a249c4386e3484fab8b7982b49bd77adfa`.
The original reviewed identity above is retained to distinguish the two
prefreeze texts. No old scientific input or sealed numerical file was
changed by this review.

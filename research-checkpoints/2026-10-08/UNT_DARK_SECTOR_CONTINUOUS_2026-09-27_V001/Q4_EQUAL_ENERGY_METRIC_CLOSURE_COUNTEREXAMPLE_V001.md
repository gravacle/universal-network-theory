# q4: equal mean energy, metric and velocity do not close acceleration

2026-09-27. Exact finite-dimensional analytical counterexample; no numerical execution, new Hamiltonian, physical metric adoption or claim of preparation by the historical blank-prewait protocol.

## Read evidence and parent

Read completely after resident flag checks:

- `NATIVE_Q4_METRIC_ENERGY_ENVELOPE_V001.md`, SHA256 `920e113132ebeda44f500c73af105ecd1bbff267b894e02b09cac27845778009`.
- `Q4_COVARIANCE_PHASE_DYNAMICAL_CLOSURE_REVIEW_V001.md`, SHA256 `0d9313504a8464f1759380f0158def05a5f012977e4c0a7fe044a7a7e2563e0d`.

Their common GL6U U04 active-star Hamiltonian, restricted to its exact permutation-symmetric spin-two subspace, is

\[
 H=C-2hJ_x+U J_z^2-BJ_z,\qquad
 B=\Delta+U(5-4d_*),\quad U=U_d.
\]

C includes the same active scalar and any identical spectator/reference scalar in both states; none is reset. For permutation-symmetric states the proposed covariance is F = fI₃, with

\[
 q=\langle J_z^2\rangle,\quad f=(4-q)/3,
 \quad\dot f=\frac{2h}{3\hbar}\langle\{J_y,J_z\}\rangle,
\]
\[
 \ddot f=\frac{2h}{3\hbar^2}
 \left\langle4h(J_z^2-J_y^2)
 +U\{J_z,\{J_z,J_x\}\}-B\{J_x,J_z\}\right\rangle. \tag{1}
\]

Here q is a spin second moment, not record occupation. Equation (1) is the already derived exact Heisenberg identity, not a semiclassical or product-state equation.

## 1. Explicit positive density matrices

Order the J_z basis as m = 2,1,0,−1,−2. Define the real symmetric operator

\[
 \mathcal X=\begin{pmatrix}
 0&1&0&0&0\\
 1&0&-2/\sqrt6&0&0\\
 0&-2/\sqrt6&0&-2/\sqrt6&0\\
 0&0&-2/\sqrt6&0&1\\
 0&0&0&1&0
 \end{pmatrix},\qquad
 \rho_\pm=I_5/5\pm\epsilon\mathcal X. \tag{2}
\]

The calligraphic symbol distinguishes this perturbation from the native link Pauli operators Xₐ. It is traceless. Reflection m ↔ −m decomposes it into an even three-dimensional block and odd two-dimensional block:

\[
 \mathcal X_{\rm even}=
 \begin{pmatrix}0&1&0\\1&0&-2/\sqrt3\\0&-2/\sqrt3&0\end{pmatrix},
 \qquad
 \mathcal X_{\rm odd}=\begin{pmatrix}0&1\\1&0\end{pmatrix}.
\]

Their spectra give

\[
 \operatorname{spec}(\mathcal X)=\{0,\pm1,\pm\sqrt{7/3}\},
 \quad\|\mathcal X\|=\sqrt{7/3},
 \quad
 \rho_\pm\ge0\ \Longleftrightarrow\ 
 |\epsilon|\le\frac1{5}\sqrt{\frac37}. \tag{3}
\]

Both traces equal one. In particular ε = 1/10 is strictly inside the positive interval, since (1/10)²(7/3) = 7/300 < 1/25. This is an exact inequality, not a numerical positivity test. Embedded in the full sixteen-dimensional link space, the states are zero outside the symmetric subspace and remain valid density matrices. Their density spectra also agree, so no entropy difference is required by this example.

## 2. Equal diagonal law and complete mean energy

The diagonals of both states in the Dicke basis are exactly 1/5. Consequently every joint Z outcome has the same probability in both states: a particular four-bit string with r occupied links has probability

\[
 \frac{1}{5\binom4r},\qquad r=0,1,2,3,4.
\]

This is not the uniform law on sixteen strings. It gives ⟨J_z⟩ = 0, q = 2 and F = (2/3)I₃.

For a concise trace proof, J_x has neighboring entries

\[
 (1,\sqrt6/2,\sqrt6/2,1).
\]

Their products with the corresponding entries of 𝒳 are (1,−1,−1,1). Hence Tr(𝒳J_x) = 2(1−1−1+1) = 0. The diagonal operators J_z and J_z² have zero trace against 𝒳. Thus

\[
 \boxed{\langle J_x\rangle_+=\langle J_x\rangle_-=0,\qquad
 E_+=E_-=C+2U,\qquad F_+=F_-=(2/3)I_3.} \tag{4}
\]

This also equalizes the single-Z mean and the transverse T₂ energy diagnostic used in the energy-envelope note. **E means the complete mean energy in this block with identical spectators**, not equality of all energy moments or membership in one energy eigenspace.

## 3. Equal velocity, unequal exact acceleration

The operator {J_y,J_z} is purely imaginary with antisymmetric transpose in this real basis, so its expectation vanishes in both real symmetric states: Ḟ₊ = Ḟ₋ = 0.

The remaining traces in (1) follow by support or by the same four neighboring products:

- Tr(𝒳J_y²) = 0 because J_y² connects only equal m or differences of two, whereas 𝒳 connects differences of one.
- Tr(𝒳{J_x,J_z}) = 2[3−1+1−3] = 0; the neighboring m sums are (3,1,−1,−3).
- The operator {J_z,{J_z,J_x}} has neighboring entry (m_i+m_j)²(J_x)ᵢⱼ. Therefore

\[
 \operatorname{Tr}\bigl(\mathcal X\{J_z,\{J_z,J_x\}\}\bigr)
 =2[9-1-1+9]=32. \tag{5}
\]

For ρ₀ = I₅/5, rotational trace symmetry gives ⟨J_z²⟩₀ = ⟨J_y²⟩₀ = 2, and both anticommutator expressions involving J_x in (1) have zero trace. Substitution of (5) into (1) proves

\[
 \boxed{
 E_+=E_-=C+2U,\quad
 F_+=F_-=(2/3)I_3,\quad
 \dot F_+=\dot F_-=0,\quad
 \ddot F_\pm=\pm\frac{64\epsilon hU}{3\hbar^2}I_3.} \tag{6}
\]

For hU > 0 and any nonzero allowed ε, the accelerations differ. No special value of B or adjustment of native parameters is needed. At hU = 0 this particular acceleration discriminator vanishes; no stronger assertion is made there.

## 4. What is and is not excluded

An autonomous second-order equation whose state data are only (F,Ḟ,E), with E the scalar mean energy and all native parameters fixed, cannot reproduce both admissible mixed states. The missing information is not repaired merely by supplementing the covariance with its velocity and total mean energy, even though the complete diagonal probability laws agree as well. The native triple correlation in (5) supplies the independent datum controlling this difference.

This is not a counterexample within a specified ground-state manifold, strict microcanonical eigensector, or the historical pure blank-prewait trajectory. It does not show that either mixed state is prepared by that protocol, that an operation interchanging them has zero work cost, or that they share the full energy distribution. A physically justified state-selection/reduction may narrow the admissible family and must be tested separately; the constrained static energy envelope remains valid for its own question.

The exact five-state density-matrix evolution already retains these coherences and gives an unambiguous answer. A reduced dynamical claim must either retain the relevant additional variables or prove that its actual state/preparation constraints determine them with controlled error. No physical stress, cosmological clock, metric deformation, gravity or general UNT no-go follows from this finite closure counterexample.

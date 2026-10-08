# Conditional record-offset completion of the grounded q4 elastance

Date: 2026-10-05. Status: new analytical candidate for review; not adopted as the canonical parent or a physical gravity/expansion law. No worker, numerical replay, parameter adjustment or existing-file edit was used.

The existing FU four-terminal construction can generate the degree square. A specified record-dependent terminal-charge offset can also generate the present linear record/degree feedback, but it necessarily adds a positive record cost. That cost and the charge-transfer requirements distinguish a full candidate from matching a held record block. This is a local existence calculation, not a completed shared-link electromagnetic circuit.

## 1. Existing parent and conventions

Use the FU convention
\[
 n_a=(1-Z_a)/2,\quad c=d-2=-\tfrac12\sum_{a=1}^4 Z_a,
 \quad q=q^r,\quad q^2=q,
 \tag{1}
\]
with commuting incidence involutions and an independent physical record-occupancy projector. The label-blind BS11 feedback is \(-\lambda_R\sum_e n_e(q_u+q_v)\). Together with the native record storage, its node term is
\[
 U_d c^2+(\epsilon_r-2\lambda_R)q-\lambda_R qc.
 \tag{2}
\]
For the present revised tuple, \(U_d=\epsilon_r=1\), \(\lambda_R=1/2\), so the middle coefficient vanishes. Record occupancy is not a prescribed classical flux or an arbitrary continuously adjustable background. Actual copying changes it coherently.

FU09--14 already conditionally realizes the first term through signed terminal charges and a complete grounded elastance; FU09b and GA identify the associated charge-transfer obligation. The following extension is new relative to that recovered construction.

## 2. Exact four-terminal offset construction

At the regular point, write the full positive-definite grounded elastance as
\[
 \mathcal E=e_d I+e_m\mathbf1\mathbf1^T,
 \quad e_d=e_s-e_m>0,\quad r=e_d+4e_m>0.
 \tag{3}
\]
Matching \(U_d>0\) requires \(e_m>0\). Prospectively assign the terminal charges
\[
 Q_a=q_*[Z_a-b(q)],\qquad q_*\ne0,
 \tag{4}
\]
and retain their complete energy
\[
 H_C=\tfrac{q_*^2}{2}(Z-b\mathbf1)^T\mathcal E(Z-b\mathbf1)
       +R_{\rm raw}I.
 \tag{5}
\]
The commuting algebra gives, without projection or averaging,
\[
 H_C=U c^2+2q_*^2 r b\,c+2q_*^2 r b^2
        +2q_*^2e_d I+R_{\rm raw}I,
 \qquad U=2q_*^2e_m.
 \tag{6}
\]
Select the offset by matching the already declared feedback coefficient, not an observed galaxy or expansion history:
\[
 b(q)=-\frac{\lambda_R}{2q_*^2r}q,
 \quad H_C=Uc^2-\lambda_R qc+Aq^2+R I,
 \quad A=\frac{\lambda_R^2}{2q_*^2r},
 \quad R=2q_*^2e_d+R_{\rm raw}.
 \tag{7}
\]
The required linear sign is negative. The quadratic-offset energy is positive and is not optional. Define the independently physical contrast/common-mode ratio \(\alpha=e_d/e_m>0\); then
\[
 A=\frac{\lambda_R^2}{U(\alpha+4)},
 \qquad 0<A<\frac1{16}
 \quad\text{at }U=1,\ \lambda_R=\tfrac12.
 \tag{8}
\]
Equation (8) does not select \(\alpha\). It is an additional circuit datum not determined by matching \(U\) and \(\lambda_R\).

The exact finite-word control is immediate: each of the sixteen link words has one degree \(d=0,\ldots,4\), and each record word has \(q=0\) or \(1\). After displaying the common \(R\) separately, both (5) and (7) give this table:

| Degree | q=0 | q=1 |
|---|---|---|
| 0 | \(4U\) | \(4U+2\lambda_R+A\) |
| 1 | \(U\) | \(U+\lambda_R+A\) |
| 2 | \(0\) | \(A\) |
| 3 | \(U\) | \(U-\lambda_R+A\) |
| 4 | \(4U\) | \(4U-2\lambda_R+A\) |

This verifies all 32 incidence/record words algebraically, including the sign and the cost. No eigenproblem or numerical finite-word worker is needed.

## 3. What matching does and does not preserve

Since \(q^2=q\), the offset energy is an actual \(Aq\) storage term, not one full-Hilbert-space identity. Combining it with (2) gives record detuning
\[
 \delta_r(d)=\epsilon_r-\lambda_R d+A.
 \tag{9}
\]
The old degree-two detuning was zero at the current tuple; this candidate gives \(\delta_r(2)=A>0\). Thus it changes the full copying/record-hole dynamics. A single common reference can match the entire frozen \(q=1\) block at one source-off point, but cannot simultaneously remove the relative \(q=0\) versus \(q=1\) cost. Subtracting \(-Aq\) to preserve the old full record law would be a new physical binding/storage term requiring its own derivation and source contacts. It is not an allowed record-dependent choice of energy zero.

For any record observable \(B_v\) commuting with incidence, the safe convention-independent relation is
\[
 [H_C,B_v]=[-\lambda_R c_v+A]\,[q_v,B_v].
 \tag{10}
\]
The Heisenberg contribution is \((i/\hbar)\langle[H_C,B_v]\rangle\), plus actual copy, transport and other terms. No Pauli factor or shorthand \([q,B]=X\) is assumed. Equation (10) remains valid at dilation after replacing the coefficients by their owned values.

## 4. A concrete conditional mechanical tangent

Assume all physical lengths, grounded boundaries and terminal geometries in this electrostatic block are dilated by \(F=aI\), at fixed terminal charges/offset, fixed coupling and fixed dielectric response. Ideal Coulomb homogeneity then supplies
\[
 \mathcal E(a)=\mathcal E_0/a,\quad
 U(a)=U_0/a,\quad \lambda_R(a)=\lambda_{R0}/a,
 \quad A(a)=A_0/a.
 \tag{11}
\]
This is a derived common scaling inside those explicit premises. Holding \(\lambda_R\) fixed while scaling \(U\) would instead require a changing offset/background charge and its supplied charge work. The present fixed-local \(h=1/5\) working normalization is not an assumption that its geometric derivative vanishes, nor a derivation of any Coulomb scaling for \(h\), hopping, carrier rest energy or physical time.

For a fixed graph/census \(N\), collect the whole specified electrostatic numerator, including its self term, as
\[
 J_{0,N}=U_0\sum_vc_v^2-\lambda_{R0}\sum_vq_vc_v
           +A_0\sum_vq_v^2+2q_*^2e_{d0}V_N I.
\]
Then the sector has the actual tangent and direct contact
\[
 H_{C,N}(a)=J_{0,N}/a+R_{{\rm raw},N}(a)I,
 \quad H_{C,a}=-J_{0,N}/a^2+R_{{\rm raw},N}'I,
 \quad H_{C,aa}=2J_{0,N}/a^3+R_{{\rm raw},N}''I.
 \tag{12}
\]
The reference is the circuit's complete absolute reference; it is not a selectable volume-energy function. It scales as \(1/a\) only if its own physical energy satisfies the same homogeneity. Other rest, reservoir, support and donor terms require their independently specified derivatives.

At fixed physical \(\beta\), the canonical free-energy identity is
\[
 \Phi_\beta''(a)=\langle H_{{\rm tot},aa}\rangle_\beta
   -\int_0^\beta d\tau\,
     \langle\delta H_{{\rm tot},a}(-i\tau)
              \delta H_{{\rm tot},a}(0)\rangle_\beta.
 \tag{13}
\]
It includes the electrostatic contact (12), every remaining direct contact, and all mixed susceptibilities. It is not the internal-energy second derivative. A ground-energy formula additionally requires an owned ground branch. This fixed-census dilation is distinct from adding cells, changing a graph support, or identifying physical volume.

For the degree-square sub-sector alone, the already measured diagnostic \(H-uT\), \(T=2\sum c^2-2V_NI\), matches \(U(a)\sum c^2\) only with
\[
 u=(U_0-U(a))/2,
 \quad \Delta H=-uT+[\Delta R-2uV_N]I.
 \tag{14}
\]
The identity correction cannot be omitted in work. The full offset tangent also contains \(\sum qc\), \(\sum q^2\), and self/reference terms; the measured pair/coordination response alone therefore does not give its complete stiffness. No arbitrary \(u(a)\), \(f(a)\), pressure law or expansion history is inferred.

## 5. Shared-link, record-transfer and creation boundaries

A local positive four-terminal matrix is not yet a global shared-link charge realization. Each actual \(Z_e\) is one physical factor shared by its two endpoint stars. A completion must specify one global capacitance/charge domain, terminal ownership and the embedding of these shared factors. Independent endpoint copies or a doubled self energy cannot be introduced silently. Cross-node elastance terms produce genuine cross-node operator strings and cannot be discarded as a local identity or folded into \(U_dc_v^2\).

The offset also carries record-dependent background charge: \(Q_{\rm offset}=-4q_*b(q)\). A copy changing \(q\) must transfer that charge to a specified compensating sector. GA's existing encoder proves exact conserving link-flip equivalence only on its closed full-code scalar hold. It does not supply the new record-offset transfer, a physical reservoir placement, or a simultaneously active source/creation port. Those sectors must own their energy, spatial current and source-work contributions. Abstract total-charge conservation does not establish a spatial Maxwell or stress Ward identity.

For the current Nc1, one-content creation embedding \(F\), the already owned relation is
\[
 H_{N+1}F-FH_N=FD+\Lambda.
\]
Under an actual deformation parameter,
\[
 H_{N+1,a}F+H_{N+1}F_a-F_aH_N-FH_{N,a}
       =F_aD+FD_a+\Lambda_a.
 \tag{15}
\]
The complete creation work must therefore retain the differences of \(J_{0,N}\), self/reference energies, the source-dependent inclusion and the complementary leakage. New blank records may make an \(Aq\) compression cancel for that specific initial embedding; subsequent copying/hole dynamics still contains it. This cancellation does not restore the old full history or generalize the Nc1 formulas to simultaneous multiple carriers.

A conserving controller also retains the full derivative of its supply, load and port:
\[
 \partial_aH_{\rm port}
 =\epsilon_a(Fb+\mathrm{h.c.})
  +\epsilon(F_ab+Fb_a+\mathrm{h.c.}),
 \tag{16}
\]
with \(H_{{\rm supply},a}\), \(H_{{\rm load},a}\), complete state response and direct contacts counted once. No donor spectrum, physical cell volume, census-to-volume identification, physical lapse assignment or spontaneous count dynamics is selected here. The current operational source \(L\) remains distinct from a mechanical strain \(a\); their relationship needs a complete source/probe prescription.

## 6. Smallest next obligation and retained theory

The useful next theoretical action is one complete **global** grounded charge/reservoir construction on an existing declared q4 support. It must use the shared link Hilbert factors once, derive its source and deformation derivatives, conserve both link and record-offset charge under the actual copy/port operations, and expose rather than subtract the \(Aq\) and reference/count energies. Its source-off operator comparison then decides whether it extends the present canonical parent or belongs to a different physically justified candidate. Local matching alone is insufficient.

This candidate neither requires nor proves a massless coordination scalar. The existing record-first RGRL working closure uses qualified pair-memory and an adopted common metric/EH response class; it remains at its declared conditional scope. Active incidence pairs, physical retained memory, the external source \(L\), and a physical mechanical deformation are distinct until the existing qualification and source/metric obligations are discharged. No claim about gravity, dark-sector superiority, an autonomous 3D phase or cosmic acceleration follows from (7) or (11).

## Frozen resident evidence

All paths below are relative to the sole project root; hashes were read from existing bytes on 2026-10-05. MODEL is existing dirty work and was read only.

| Input | SHA256 |
|---|---|
| `program-worktree/LANE_GRA_FU_F3_Q4_PAIR_RESOLVED_MAXWELL_DPAR_DERIVATION_V001/THEOREM.md` | `f088346f72861b3b11ae737fe6b882d43da9e747fc1d1d1f6bd446a7fd2b6272` |
| `program-worktree/LANE_GRA_GA_F3_Q4_FU09B_ENCODED_CHARGE_CURRENT_LIFT_V001/THEOREM.md` | `374168c75f928cdbce55ca790157ba00df2d3a7f2045611d805d1b1b3c090336` |
| `program-worktree/LANE_GRA_BS_F3_QIRN_MICRO_ACTION_V001/MICRO_ACTION.md` | `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec` |
| `program-worktree/MODEL.md` | `3d7c360a38b09fed8f4051c049e838ca561c32ba5dd105dddd80c6aeb7f65607` |
| `program-worktree/GRAVITY_RECORD_FIRST_WORKING_THEORY_CLOSURE_V001.md` | `cf9229586268f054b473b1641085ebafc3bca01fa0691a191cbda923ae1fa7f2` |
| `UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/NATIVE_COORDINATION_MEDIATOR_CANDIDATE_V001.md` | `d9ead9c618f13d237aabbb6586b371187521febbf97be52e35bacc3dce959876` |
| `UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/LOCAL_PROPER_BOND_CONSERVING_CREATION_SOURCE_CONTACT_V001.md` | `e28eb807a3df201d46981898f4f85189cca4d54f7723a7946e13dd3cae8f9d43` |
| `UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/LOCAL_PROPER_BOND_NORMALIZATION_V001.md` | `9b4cc5e1942ac7373e210efa46bfa74e03bbcfb8130c01232373b02e8a622a5b` |

Source anchors: FU02--03, FU08--14 and its full physical solder conditions; GA03--13 and `GA-CLOSED-FULL-CODE-SCALAR-HOLD`; BS11 and BS20--23; MODEL's FU/GA/direct-Ward boundary at lines 1342--1436; WTC03--06 and WTC-H1--H4; the current creation-source note's full inclusion/port contacts. The offset construction, mandatory record cost and conditional common scaling above are analytical extensions rather than resident empirical evidence.

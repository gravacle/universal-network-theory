# Next scientific construct: retained record defects with a complete energy and transport law

2026-09-27. Analytical forward work only. No new experiment, numerical run, cosmological input, physical volume assignment, or change to the original joint plan.

## Scope and choice

The shortest useful next dark-sector construct is a **dark-matter candidate made of conserved record defects whose complete insertion energy and relational transport are derived from the same finite parent**. The present model has a positive record storage term, a known record–link interaction, an exact retention rule, and independently checked carrier response. These already constrain such a candidate. They do not yet supply its physical mass, motion, gravitational coupling, or cosmological abundance.

This is an explicit prospective mechanism branch toward I0/I1, not a claim that the original active/maintenance bandwidth split has been derived or passed its frozen gates. A record occupation, energy, bandwidth, and maintenance power are distinct quantities.

The original [joint plan](</Users/bgm/Desktop/FOLDERS/Gravity/20260918 Packet/20260924 Packet Updates/UNT_DARK_SECTOR_JOINT_PLAN_V001.md>) was read completely earlier in this same work session. Its path now reports compressed,dataless, so it was not reopened or freshly reauthenticated. The relevant original tasks are I0's record/count/bandwidth definitions, gravitating subset and split, and I1's dust dilution and collisionless behavior. The resident [energy/volume audit](</Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/ENERGY_VOLUME_BRIDGE_AUDIT.md>) and [two-band results](</Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/two_band_probe/RESULTS.json>) were read in this turn.

The two-band evidence matters: the actual formed state retains upper-band population \(0.1305499137438213\); lower-only predictions showed substantial sampled errors. Thus no ground-state energy below should be silently substituted for the actual formed-state energy.

## 1. Exact one-link energy law

On the native hold, switching occupied-record sector \(q=0\) to \(q=1\), while keeping the same background Hilbert space, changes the Hamiltonian by
\[
\boxed{\Delta H=\epsilon_r I-\lambda_Rn.}
\]
At the inherited \(\epsilon_r=1,\lambda_R=1/2\), the operator bound is
\[
\boxed{\tfrac12I\le\Delta H\le I.}
\]
It follows both that a matched background state's insertion energy lies in \([1/2,1]\), and, by the min–max principle, that each consistently ordered eigenvalue increases by an amount in that interval. In particular the relaxed ground insertion cost is positive. This is a finite model energy statement, not an identification of gravitational or inertial mass.

For the explicit eigenbranch with carrier label \(s\) and link-band label \(\beta\),
\[
E_{\beta s}(q)=C_0+\epsilon_rq+
\frac{x(q)+\beta\sqrt{x(q)^2+4h^2}}2,
\quad x(q)=A-\lambda_Rq-js,
\]
the exact insertion cost can also be written
\[
E_{\beta s}(1)-E_{\beta s}(0)
=\epsilon_r-\lambda_R\int_0^1
\frac{1+\beta x(u)/\sqrt{x(u)^2+4h^2}}2\,du.
\]
The integral is a mathematical interpolation between physical sectors; it is not a fractional-record preparation protocol. It displays the occupied-link contribution that reduces the cost below bare record storage.

There is a corresponding exact response distinction. Define \(f(x)=(x-\sqrt{x^2+4h^2})/2\). The lower-band effective hopping
\[
t_L(b)=\frac{f(b+j)-f(b-j)}2
\]
increases when record occupation lowers \(b\), because \(f'\) is strictly decreasing:
\[
\frac{\partial t_L}{\partial q}
=-\frac{\lambda_R}{2}\,[f'(b+j)-f'(b-j)]>0
\quad(j,\lambda_R>0).
\]
The upper-band hopping obeys \(t_U=j-t_L\), so its change has the opposite sign. Positive insertion energy therefore does not imply one band-independent carrier response. The actual band populations and coherences remain part of the source description.

## 2. The multi-vertex energy law is already more restrictive than token counting

The resident [formed-pattern design](</Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/FORMED_PATTERN_TEST_DESIGN.md>) specifies a finite restriction with the inherited feedback
\[
-\lambda_R\sum_{e=(u,v)}n_e(q_u+q_v)
=-\lambda_R\sum_vq_vd_v,\qquad d_v=\sum_{e\ni v}n_e.
\]
Its complete record-dependent Hamiltonian is consequently
\[
H_{\rm rec}=\sum_vq_v(\epsilon_r-\lambda_Rd_v).
\]
Adding one occupied record at vertex \(v\) gives the exact operator difference
\[
\boxed{\Delta H_v=\epsilon_rI-\lambda_Rd_v,\qquad
(\epsilon_r-\lambda_Rz_v)I\le\Delta H_v\le\epsilon_rI,}
\]
where \(z_v\) is the number of possible incident edges in that finite restriction. This includes the interaction once; degree penalties, carrier terms, and all other background terms remain in the common Hamiltonian.

Thus the one-link lower bound does **not** establish a degree-independent positive energy per record on larger graphs. With the inherited coefficients, the proposed \(K_{2,2}\) restriction has \(z_v=2\) and bound \([0,1]\). At coordination three or greater, this bound no longer guarantees positivity. A nonpositive lower bound is not proof that the relaxed insertion energy is negative: the degree penalties and link fluctuations can keep the relevant states above it. Positivity must be established on the actual admitted backgrounds, not rescued by silently changing the coupling with graph size.

For a fixed pattern of \(R\) occupied registers and maximum coordination \(z_{\max}\),
\[
R(\epsilon_r-\lambda_Rz_{\max})I
\le H(q)-H(0)\le R\epsilon_rI.
\]
The same inequalities bound ordered spectral shifts. They provide a precise sufficient condition \(\epsilon_r>\lambda_Rz_{\max}\) for a uniformly positive insertion-energy floor in this class. They do not supply extensivity, a continuum limit, or a physical conversion to mass.

For a nondegenerate relaxed eigenbranch, differentiating a mathematical insertion parameter \(\alpha_v\) gives the useful response law
\[
\frac{\partial E}{\partial\alpha_v}
=\epsilon_r-\lambda_R\langle d_v\rangle.
\]
For a nondegenerate ground branch with gap \(\Delta>0\), after fixing exact spectator symmetries, its mixed susceptibility is
\[
\frac{\partial^2E_0}{\partial\alpha_v\partial\alpha_w}
=-2\lambda_R^2\operatorname{Re}
\sum_{m>0}
\frac{\langle0|d_v|m\rangle\langle m|d_w|0\rangle}{E_m-E_0}.
\]
It obeys
\[
\left|\frac{\partial^2E_0}{\partial\alpha_v\partial\alpha_w}\right|
\le\frac{2\lambda_R^2}{\Delta}
\sqrt{\operatorname{Var}(d_v)\operatorname{Var}(d_w)}
\le\frac{\lambda_R^2z_vz_w}{2\Delta}.
\]
The diagonal susceptibility is nonpositive, but the mixed sign is not fixed. Network relaxation can therefore mediate defect interactions; these are neither automatically attractive nor automatically negligible. A collisionless-matter interpretation must confront this interaction, rather than infer collisionlessness from permanent storage. No scattering cross section follows without a transport and physical-units map.

## 3. Conserved records are not conserved separate energy or maintenance power

During source-off hold, every native register occupation commutes with the Hamiltonian. Hence \(R=\sum_vq_v\) is conserved. Put
\[
D_R=\sum_vq_vd_v,\qquad E_{\rm rec}(t)
=\epsilon_r\langle R\rangle-\lambda_R\langle D_R\rangle.
\]
Only the incidence-flip terms fail to commute with \(n_e\), and the stated Pauli convention gives
\[
\dot n_e=i[H,n_e]=hY_e.
\]
It follows that
\[
\boxed{\frac{dE_{\rm rec}}{dt}
=-\lambda_Rh\sum_{e=(u,v)}
\langle(q_u+q_v)Y_e\rangle.}
\]
This is an exact internal energy-exchange law. Record count can remain fixed while its interaction-energy allocation changes. The complementary background contribution compensates because the complete fixed hold Hamiltonian conserves total energy.

Conversely, retention at \(g=0\) requires no ongoing externally supplied power in this isolated model: \(\partial_tH=0\). Stored positive energy and reversible internal exchange are not maintenance bandwidth or a steady external power cost. The native model therefore supplies no derivation of the original plan's maintenance-overhead dark-energy density.

If an independently justified material volume later obeyed \(V\propto a^3\), this particular energy allocation would satisfy
\[
\dot\rho_{\rm rec}+3H_{\rm exp}\rho_{\rm rec}
=-\frac{\lambda_R}{V}\frac{d\langle D_R\rangle}{dt},
\]
with fixed coefficients. This is an exchange equation, not a derivation of physical pressure. I1's dust scaling requires the **complete material excess energy** and stress to have the appropriate behavior; constant \(R\) alone is insufficient. No such volume has been assigned here.

## 4. What the existing conservation law says about motion

In any extension using only the current record-diagonal hold couplings,
\[
[H,q_v]=0\quad\hbox{for every register }v.
\]
There is exactly zero intrinsic transfer of record occupation across a fixed cut of register labels. A matter candidate cannot obtain a moving record excitation on that register graph simply by reinterpreting this conservation as ordinary particle-number conservation.

This does **not** prove immobility in physical space or a Bullet Cluster failure. The links change dynamically, and an operational position might itself be a function of the link/probe state. If a same-parent construction supplied relational positions \(X_v\), then
\[
X_{\rm rec}=\sum_vq_vX_v,\qquad
\dot X_{\rm rec}=\sum_vq_v\,i[H,X_v]
\]
could be nonzero despite fixed register occupations. The missing item is precisely that relational position/current map and its independent probe calibration. Adding an explicit record-hopping term would instead change the model and must be declared as a new microscopic assumption.

## 5. The next construct and its scientific decision

Proceed with the already specified multi-vertex parent as a **retained record-defect candidate**, before attaching a cosmological interpretation. Its complete insertion-energy operator is now fixed, its background susceptibility has a gap-dependent bound, and its record current across register cuts is exactly known.

The next derivation should identify whether one retained defect has a transport law relative to the existing carrier probes, while keeping its full insertion energy \(\epsilon_r-\lambda_Rd_v\) and background response. The testable choice is whether changing native links transports a persistent defect **relative to other registers and probes**, with a consistent energy/current ledger. If the adopted finite parent supplies no such relational transport, the candidate remains pinned memory in that construction and needs an explicit new dynamical term or a different parent; another one-link spectral identity cannot repair that omission.

This directly targets I0's material/gravitating-record specification and the prerequisite to I1's collisionless matter behavior. A successful finite result would still need a physical position/time calibration, common gravitational response, stress and dilution law, controlled many-body limit, and a derived formation abundance. It would not by itself pass I1 or explain dark matter.

The DE route presently has a larger missing ingredient: no same-parent physical strain dependence or maintained-power law has been derived. The working theory permits a vacuum term, but its coefficient and microscopic origin remain open. The positive-energy retained-defect route is therefore the shorter construct currently constrained by the actual native ingredients; the joint dark-sector goal remains open.

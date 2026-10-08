# Mobile matter interaction from virtual native links

2026-10-03 UTC. A new controlled-regime calculation derives carrier motion
and an induced pair interaction together from the original BS parent. It does
not pin one carrier while allowing an identical probe to move. A negative
pair coefficient is possible without record feedback or added mass, but the
smallest mobile graph also shows why that coefficient alone is not evidence
of binding or gravity. The prospective protocol and the subsequently saved
full inherited-parameter calculation are both retained below.

## The sector and the approximation

Use one K_(N,N) slab with all M=N^2 possible native arrows, one fixed content,
and a fixed total carrier number Q. A vertex is empty or contains that content;
two carriers cannot occupy one vertex. This is the native qutrit transfer
algebra, not a fermionic substitution. Records, writers and fragments are
blank, with copying and ports off. These are exact held sectors, not a claim
that the previous formed states have become ground states. In particular,
this sector supplies no nonzero record phase clock.

Let p_v be carrier occupation, T_e the Hermitian content-preserving transfer,
C_e=p_u+p_v-2p_up_v the endpoint XOR projector, and m=sum_e n_e. Then
T_e^2=C_e, C_e T_e=T_e and the eigenvalues of T_e on C_e are plus/minus one.
With h=Omega/N, j=lambda_J, k=Delta+2Ud(1-2d*), the complete held generator is

\[
H=E_{\rm ref}+km+2U_d\!\sum_{e<f\text{ sharing a vertex}}n_en_f
 +\sum_e n_e(jC_e-tT_e)-h\sum_e X_e,
\quad E_{\rm ref}=2NU_d d_*^2+\epsilon_\psi Q.
\]

No constant is discarded from work. At h=0 the blank-link subspace P contains
every carrier configuration. For Ud,j nonnegative, k>0 and
g=k+min(0,j-|t|)>0, H0-E_ref >= g*m. Thus P is an isolated, degenerate lowest
subspace, with gap at least g. This bound remains valid even though transfer
operators on different edges do not commute.

Two flips must act on the same edge to return to P. The intermediate one-link
carrier operator is A_e=kI+jC_e-tT_e. Degenerate perturbation theory therefore
fixes the second-order operator on the WHOLE mobile carrier space:

\[
H_{\rm eff}^{(2)}=E_{\rm ref}I-h^2\sum_e A_e^{-1}.
\]

Writing D=(k+j)^2-t^2, the inverse is exactly

\[
A_e^{-1}=\frac{I-C_e}{k}+\frac{(k+j)C_e+tT_e}{D}.
\]

Consequently

\[
\begin{aligned}
H_{\rm eff}^{(2)}&=E_{\rm ref}I-\frac{Mh^2}{k}I
 -\sum_e(\alpha C_e+J T_e),\\
J&=\frac{h^2t}{D},\qquad
\alpha=h^2\left(\frac{k+j}{D}-\frac1k\right)
 =\frac{h^2[t^2-j(k+j)]}{kD}.
\end{aligned}
\]

Here J is an induced hopping coefficient, not the original current operator.
Expanding the XOR term gives an onsite contribution
-alpha*sum_v(deg_possible(v)*p_v) and a pair contribution
+2alpha*sum_e p_u p_v. Both are compulsory; omitting the onsite or constant
energy is not an alternative normalization of the same absolute-work model.
No independent attractive potential was fitted.

At the inherited k=2,j=1/4,t=1/2, J/h^2=8/77 and alpha/h^2=-5/154.
Thus the induced pair coefficient is attractive in occupation space, with
2alpha/J=-5/8. With j=0 instead, alpha is positive for t nonzero; with t=0,
alpha=-h^2*j/[k(k+j)] is negative but there is no mobile kinetic term. These
controls separate current-square energy, virtual transfer and exclusion.

Changing a uniform held-record occupation would shift k to
k-2*lambda_R*r while retaining its storage energy. Within the positive-gap
domain this can change the hopping and attraction magnitudes, but it cannot
move the leading K22 addition-energy threshold j=t derived below. Therefore
changing only that uniform local gap at fixed j/t is not the requested
dense/sparse binding transition in this reduction. This does not exclude
correlated, nonuniform, gap-closing or driven environments; it identifies
which simple density substitution is insufficient.

## Attraction is not a bound pair

The N=2 graph gives an exact analytic test of the effective operator without
inventing physical distance. Let E_Q denote its lowest energy in carrier
number Q. Removing only the displayed common constant for the following
comparison, the Q=1 carrier ground energy is -2alpha-2J. For Q=2, two
same-layer configurations have diagonal -4alpha, four cross-layer
configurations have diagonal -2alpha, and every allowed transfer connects
one group to the other. The positive symmetric ground block has off-diagonal
-sqrt(8)*J, giving carrier ground energy -3alpha-sqrt(alpha^2+8J^2).

For t>=0, the resulting pair addition energy is

\[
\Delta_{\rm pair}=E_2-2E_1+E_0
 =\alpha+4J-\sqrt{\alpha^2+8J^2}+O(h^4).
\]

The baseline and epsilon_psi terms cancel from THIS comparison, not from
the energy ledger. Negative addition energy requires alpha<-J when J>0.
In this controlled leading-order model,
alpha/J+1=(t-j)*(k+t+j)/(k*t), so the threshold is j>t for k,t>0.
At the inherited coefficient ratio the leading result is
J*(59-sqrt(2073))/16 > 0, despite the attractive pair coefficient. This is
a finite-graph addition-energy discriminator. It is not an infinite-volume
scattering threshold, condensation test, absence of all many-body binding,
or a test of a spatial gravitational force.

There is also an exact all-h anchor. At j=t>=0, every C_e-T_e is positive
semidefinite and annihilates the uniform same-content carrier state at each
fixed Q. Its product with the incidence ground state saturates the lower
bound H>=H_inc+epsilon_psi*Q. Consequently E_Q=E_inc,0+epsilon_psi*Q and all
addition energies vanish, for every N and h. Carrier-independent environment
terms can be retained. This equality is a control at a declared changed
coefficient, not permission to adopt j=t or a theorem about full-model signs
on either side of it.

## A finite size error certificate

Let v=|h|M and require v<g/4. The existing finite-sector resolvent argument
in ../NATIVE_RECORD_SELECTED_GRAPH_VIRTUAL_RESPONSE_V001.md applies with
the carrier operators retained. The exact ground shift e is nonpositive,
|e|<=v^2/(g-v). The Schur complement uses all nonblank-link states. Its term
with three flips vanishes by occupied-link parity, independently of carrier
motion. Thus, for each fixed Q,

\[
|E_Q^{\rm full}-E_Q^{(2)}|\le 4v^4/g^3,
\qquad
|\Delta_{\rm pair}^{\rm full}-\Delta_{\rm pair}^{(2)}|
\le16v^4/g^3.
\]

These are sufficient finite-N bounds, not observed-error fits. The inherited
N=2,h=1/2 violates the sufficient smallness condition. Its spectrum must be
computed from the full operator; weak-flip coefficients do not establish its
sign. Nor is this crude norm bound a uniform large-N theorem: v=Omega*N.
A stronger relative-form bound is available for this blank-link branch.
Let Q_perp=I-P, D0=Q_perp*(H0-E_ref)*Q_perp and V=-h*sum X_e.
Because ||Q_perp*V*P||=|h|*sqrt(M)=Omega and
|expectation(Q_perp*V*Q_perp)|<=2Omega*expectation(m),
the relative form norm of Q_perp*V*Q_perp against D0 is at most
w=2Omega/g. The expectation inequality follows by Cauchy-Schwarz between
link-raising and link-lowering components and m>=1 on Q_perp.

For w<1, the complementary block stays above E_ref+g-2Omega. The low
eigenvalues E=E_ref-delta have 0<=delta<=Omega^2/(g-2Omega). Define
d=delta/g. Expanding the relative resolvent, retaining delta*D0^(-1) and
using the same odd-flip null, gives

\[
\|\Sigma(E)-\Sigma_2\|
\le\frac{\Omega^2}{g}
\left[d+\frac{(w+d)^2}{1-w}\right].
\]

This is an N-independent sufficient total-energy bound of order
Omega^4/g^3 as Omega/g tends to zero. It does not resolve a carrier splitting
that itself vanishes with N without a sharper relative estimate. The
inherited Omega=1,g=7/4 also fails this improved sufficient domain. Both
bounds are proved regimes, not claims that failure of a bound means failure
of the model. The numerical unit below checks only the simpler finite-N
certificate; no large-N computation is requested. The root checked this
relative-form derivation independently of the source-only reviewer.

## Frozen small calculation

Keep N=2, Delta=4, Ud=d*=epsilon_psi=1. Compute the full Q=0,1,2 sectors of
dimensions 16,64,96. The three coefficient arms are inherited j=1/4,t=1/2;
current-square off j=0,t=1/2; and hopping off j=1/4,t=0. In each arm use
h=1/2 and the prospective asymptotic controls h=1/40,1/80,1/160. The latter
explicitly change Omega; they are approximation checks, not fitted native
cases. Add j=t=0,h=1/2 as the exact carrier-decoupling null and
j=t=1/2,h=1/2 as the independently derived all-h ground-energy anchor.

Build the original full matrices directly from degrees, flips and allowed
hard-core transfers. Independently build H_eff by matrix inverse and by its
kinetic/XOR decomposition. Preserve all spectra and complete energies, the
gap above the lowest binomial(4,Q) states, ground-space average link count
and blank-link weight, diagonalization residuals and the addition energy.
Degenerate ground states use their full projector, not a chosen eigenvector.
An isolated low band does not prove its physical preparation.

Use the inherited 1e-10 assigned arithmetic allowance for operator/residual
checks, not as a certified floating-point error bound. Check the analytic
ground energies and the sufficient remainder where its domain applies.
Outside that domain record an unqualified approximation, not a failed
microscopic model. Neither a binding sign nor agreement at h=1/2 is a pass
condition selected to favor the model. Retain any failed check separately.
One root-owned worker, existing NumPy only; no histories, fitting or larger
lattice sweep. Source-only independent reviewers do not run it.

## Physical meaning and the next distinction

This is a genuinely mobile, shared kinetic-and-interaction reduction. Earlier
one-link dressed probes were distinguishable commuting subsystems; previous
regular-graph selections had no carriers. Generic Feshbach elimination and
the microscopic XOR term are already known, not new claims here.

The result applies to the potential K_(N,N) graph, not a spatially local graph
derived from formation. On this symmetric support an interaction between
opposite layers is not yet an interaction at a specified spatial distance.
The dressed-low-band premise, operational clock/ruler, native localization,
source coupling and absolute volume work remain independent obligations.
Testing a many-body source response requires them; a negative coefficient
cannot simply be named gravity. All eleven dark-program lanes remain open.

## Saved full model result

The root ran the reviewed source once, exit0. All 2304 assigned arithmetic
and in-domain remainder checks passed over 14 cases and 42 carrier-number
sectors. The worker took 0.150357 seconds with 38,551,552 bytes peak self RSS.
No previous formation history was rerun and no source coefficient was fitted.

At inherited h=1/2 the complete-model results are:

| Couplings | Second-order pair coefficient 2alpha | Full pair addition energy | Second-order pair addition energy |
| --- | ---: | ---: | ---: |
| Inherited j=1/4, t=1/2 | -0.016233766234 | +0.016057069820 | +0.021866542611 |
| Current-square off | +0.016666666667 | +0.032950154782 | +0.047018194237 |
| Hopping off | -0.027777777778 | -0.021718711889 | -0.027777777778 |
| Both off | 0 | Zero within assigned allowance | 0 |
| j=t=1/2 exact anchor | -0.041666666667 | Zero within assigned allowance | 0 |

All energies are in the native generator's declared energy units, not SI
binding energies. The first column is a weak-flip coefficient evaluated at
h=1/2, not an exactly extracted full-model pair potential. The approximation
has no sufficient remainder certificate there; the full energies do not use
that approximation. In the inherited mobile case the addition energy is
positive. The immobile comparison gives the opposite sign but no carrier
motion, so it cannot substitute for mobile binding or gravity.

The inherited full ground energies for Q=0,1,2 are respectively
3.542094794687, 4.515835172760 and 5.505632620653. The blank-incidence weights
of those dressed ground states are 0.819217657061, 0.800838688071 and
0.793626186242. Dressing is not negligible at h=1/2. The lowest rank1,4,6
bands have positive numerical gaps to the next levels of 2.227458269808,
1.966185219484 and 1.919275874192. These spectral properties do not show
that the physical formation history prepares the ground or the low band.

All three changed-Omega controls respect the finite-N error bound. The
native-coupling pair signs are resolved by that deliberately conservative
bound only at h=1/160: the analytic value is +3.416647283044e-6 and the
pair error ceiling is 1.166180758017e-6. The full value is
+3.416438744352e-6. At h=1/40 and 1/80 the bound is too loose to certify
the sign, even though numerical values are positive. The j-off h=1/160
control also has a certified positive sign; the t-off h=1/80 and 1/160
controls have certified negative signs. No controls were added to seek a
preferred outcome. The null and j=t exact anchor residuals are at most
7.2e-15, within the assigned arithmetic allowance, not an interval proof.

For the native-coupling h=1/160 control the positive sign also has a purely
analytic certificate: its leading addition is (59-sqrt(2073))/3942400 and
the pair remainder is exactly 1/857500. Since sqrt(2073)<46, the leading
value exceeds 13/3942400, which exceeds the remainder. This certifies that
one control's full ground-addition sign without promoting floating-point
checks to interval arithmetic or transferring it to h=1/2.

Source SHA256:
`8a76b2a10395214b4db1eb3b8e48fd93000aa53005271987b7a23a3dd73a6d8d`.
Result `native_mobile_carrier_effective_v001_results.json`, SHA256:
`ce731ec33bade067f6b7cb644500f6fa6434202cb7e991b06affff82ef993349`.
Both independent analytic derivations preceded execution; the root read the
entire authored worker and its final pair-bound additions before running it.
Internal checks and source reviews are not independent physical observations.

## Why equilibrated mobile matter does not yet select a connected space

A separate exact fixed-graph calculation identifies the next state-selection
obligation. It is NOT an extension of the blank-link approximation to a
nonempty graph. Freeze a d-regular incidence graph G with d>0, retain mobile
same-content carriers, and compare graphs with the same bare degree and
uniform held-record energies. The carrier part obeys

\[
H_{\rm car,G}-[\epsilon_\psi+(j-t)d]Q
 =t\sum_{e\in G}(C_e-T_e)
  +2(t-j)\sum_{e\in G}p_up_v.
\]

For the inherited 0<=j<t both terms are positive semidefinite. On a connected
graph Q=1 saturates this bound. For 2<=Q<=|V|, vanishing of all C_e-T_e
requires the uniform fixed-Q carrier state, because allowed occupied-empty
swaps connect the configuration space. That state has nonzero adjacent-pair
occupation, so the lower bound is strict. On a disconnected d-regular graph
with at least Q components, one uniform carrier per occupied component
saturates it. Therefore, when both topologies exist, this conditional
equilibrated-carrier energy favors available fragmentation, not joining
everything into one connected geometry.

For example, at N=4 and d=2, an eight-vertex bipartite cycle and two separate
four-cycles have identical degree energy. With Q=2 and j<t the latter
saturates the carrier lower bound and the connected cycle cannot. No number
was computed or parameter selected for this exact comparison. At j=t the
previous Dicke anchor removes the strict distinction. This is not a theorem
about every density, nonuniform records, finite-h graph motion or a driven
formed state; those terms cannot be ignored when they are active.

This sharpens the next physical step: derive and test actual dynamical state
selection with the native carrier/link/formation operators and their energy
supply. A low-energy attraction coefficient alone neither prepares a spatial
network nor provides its volume evolution. Retain this conditional failure
when evaluating such an alternative; do not silently use connected ground
geometry, a free clamp, or an uncosted reservoir as an initial premise.

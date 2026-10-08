# Exact volume-preserving shear discriminator

2026-09-27. Exploratory comparison construct ID:
**UNT_ELASTIC_COMPARISON_CENTRAL_EDGE_V001**.

This is a conditional analytical comparison, not an adopted UNT law, an
existing BS result, a replacement for primary active/maintenance research, or
a numerical experiment. A physical embedding/deformation basis and its work
interpretation are explicit added premises. They are not inferred from BS's
fixed finite register graph or its quantum link occupations.

## 1. Fixed comparison and actual-state requirement

For one frozen reference embedding let the edge vectors be d_e, their lengths
ell_e>0, and unit directions u_e=d_e/ell_e. Consider the central-edge subenergy

`H_el(F)=sum_e n_e phi(|F d_e|)`.

Freeze the topology, law phi, coefficients, reference vectors, and a complete
unconditioned retained density operator rho_0 **before** response scoring.
For the instantaneous, fixed-state Born derivative define

`w_e=Tr(rho_0 n_e)`, `E_el(F)=Tr(rho_0 H_el(F))`.

The weights remain fixed during this derivative. This does not assert that
they remain fixed during subsequent evolution under the deformed Hamiltonian.
Their correlations and coherences remain in rho_0 and must be retained for
that subsequent response; the mean weights suffice only for this displayed
linear-in-n_e subenergy at the initial instant.

The already identified native 36D candidate state, if this comparison is later
attached to that one-link parent, is exactly
`rho_formed=(|F0><F0|+|F1><F1|)/2`, tensor order
writer3, record3, link2, carrier2. The source-owned vectors are
`formed_pure_vectors.F0/F1` in
`UNT_DARK_SECTOR_MECHANISM_START_2026-09-27_V001/native_correlation/results.json`,
whose expected SHA-256 is
`aeb8f9ee23ec9a591752f3a9f452889a53ec5db5dd2f50e9acc8a63142f5457d`.
Resident `two_band_probe/compute_two_band.py` lines 21–23 and 75–86 identify
that input, preparation, and bare readout. No fresh-carrier state or
lower-band projection is substituted here. The input payload was not reread
for this note, and no new state was prepared or evolved.

A one-link state does not supply an isotropic three-dimensional network or a
physical edge vector. Applying the construction to another graph requires its
own actual rho_0 and source/input custody, not transfer of this one-link weight.
No such physical embedding or complete dynamical extension is frozen here.

Also, this is a subenergy, not permission to add it on top of an already counted
BS incidence or interaction energy. A proposed BS join must state whether it
replaces a matched coefficient or adds a new interaction, and verify the
source-off match and complete ledger explicitly.

## 2. Dilation and exactly isochoric shear

First use the calibrated affine dilation `F_eta=exp(eta) I`, with
`V_eta=exp(3 eta) V`. At the reference instant the proposed subterm predicts

`p_el=-(1/(3V)) sum_e w_e ell_e phi'(ell_e)`.

This is its volume-conjugate work stress under the added embedding premise,
not an inference from record count or from an energy-vs-coupling plot.

Independently use the physical volume-preserving path

`F_gamma=diag(exp(gamma),exp(-gamma),1)`, `det(F_gamma)=1` exactly.

Set `a_e=u_ex^2-u_ey^2` and `b_e=u_ex^2+u_ey^2`. Direct differentiation gives

`ell'_e(0)=ell_e a_e`,

`ell''_e(0)=ell_e(2b_e-a_e^2)`.

Thus the predicted instantaneous shear curvature is

`K_gamma=E_el''(0)`

` =sum_e w_e [ell_e^2 phi''(ell_e) a_e^2`

`            +ell_e phi'(ell_e)(2b_e-a_e^2)]`.

The same frozen law must predict the dilation and shear response jointly.
One must not replace this path by `I+gamma diag(1,-1,0)`: the latter changes
volume at second order and would contaminate the shear discriminator with
volume work.

## 3. A sharp power-law comparison, without a density fit

If the prospectively chosen comparison law is `phi(ell)=kappa ell^r`, hold
kappa, r, all d_e and rho_0 fixed. Let
`E=sum_e w_e kappa ell_e^r`. Then

`p_el=-r E/(3V)`,

`K_gamma=sum_e w_e kappa ell_e^r`

`         *[r(r-2)a_e^2+2r b_e]`.

If the **energy-weighted actual orientation distribution** has isotropic
second and fourth moments, then `<b>=2/3`, `<a^2>=4/15`, and

`K_gamma=4r(r+3)E/15`.

Defining the incremental shear coefficient for this exact path by
`E_el(gamma)=E+2V mu_path gamma^2+O(gamma^3)` after the isotropic linear term
vanishes gives

`K_gamma=4V mu_path`, `mu_path=r(r+3)E/(15V)`.

For rE nonzero this supplies the normalization-independent prediction

`K_gamma/(-p_el V)=4(r+3)/5`, or `mu_path/(-p_el)=(r+3)/5`.

Isotropy of second moments alone does not establish the fourth moments.
Without the required actual-state/orientation property, use the exact finite
sum instead. This is an unrelaxed affine path coefficient, not automatically
the relaxed modulus of a prestressed solid or its propagation speed.

An especially clear contrast is r=3: this subenergy has `p_el=-E/V` under
dilation, yet predicts `K_gamma=24E/5` in the stated isotropic regime. A
vacuum-like background pressure therefore need not imply a vacuum-like shear
response. This r=3 case is a comparison, not a proposed explanation selected
to match dark density. It is not a healthy relativistic-vacuum completion:
the adopted elastic inertia rho+p vanishes while this shear coefficient
does not. The nondegenerate wave formulas in
`CENTRAL_EDGE_ELASTICITY_COMPARISON_V001.md` cannot be used to declare it stable.

## 4. Falsifier, complete-source controls, and autonomy boundary

A pure constant volume energy, conventionally `E_vac=-C0 V`, is unchanged
along the exact det(F)=1 path. Its first and every higher path derivative
vanish. Changing C0 therefore cannot imitate a nonzero isochoric shear
curvature. Once the constitutive parameters are independently fixed, a wrong
joint dilation/shear response rejects this particular elastic law without
reference to a desired dark-sector abundance.

This agrees with `VACUUM_STRESS_IDENTIFIABILITY_V001.md`, where a **linear
trace-free metric chart** has a nonzero vacuum second contact. Here the
physical path is nonlinear in that metric chart: `h=F_gamma^T F_gamma`, so

`h'(0)=2 diag(1,-1,0)`, `h''(0)=4 diag(1,1,0)`.

For the volume-action density `+C0 sqrt(det h)`, the full second path
derivative at h=I is the Hessian contact **plus** the first derivative acting
on the path acceleration:

`-(C0/2) tr[(h')^2]+(C0/2) tr(h'')=-4C0+4C0=0`.

The trace-product Hessian term vanishes since `tr h'=0`. Multiplying by the
reference volume gives the integrated expression. For `H_vac=-C0 V`, both
displayed signs reverse and still cancel. Retaining the linear-chart contact
but omitting the nonlinear acceleration would manufacture a spurious vacuum
shear. The earlier contact-identifiability result and this exactly isochoric
physical-path null test therefore do not conflict.

The comparison must include or independently remove all other shape-dependent
energy, source contacts, self/reference terms, geometry kinetic energy,
boundaries, support/recoil, controllers, and ports. A pure volume offset
cancels on this path; an unknown general shape-dependent identity term does
not. BS12 and BS20a leave exactly these completion obligations open.

For an actual evolved state or finite-time measurement, propagate the complete
state with the frozen deformed Hamiltonian and retain its response terms in
addition to the instantaneous Born contact. Do not replace the formed state
by a ground state, assume thermalization, erase its upper band, or equate a
quasistatically relaxed derivative with the fixed-state formula. No such
evolution or measurement is authorized or performed by this note.

Finally, tensile stress is not by itself passive autonomous expansion. For
the central subterm the mean-force virial obeys

`sum_v x_v dot <F_v>=-sum_e w_e ell_e phi'(ell_e)`.

A freely equilibrated finite network with only those forces cannot have every
node force zero and a nonzero right-hand side. Kinetic/compressive balancing,
constraints, winding/boundaries, or dynamical geometry must be owned rather
than omitted. This is not a cosmological no-go: cosmic metric dynamics is a
different explicitly adopted interface. BS currently supplies neither that
volume dynamics nor a physical elasticity map. The comparison tests the
added map; it does not establish its ancestry or complete primary A/M.

# Recombination: what can be decided locally before a precision atomic run

2026-09-29. Analytical/source inspection only: no atomic code download,
installation, build, producer import or scientific execution. This is the
conditional ordinary-photon thermal comparison branch, not an assumed UNT
Big Bang, photon-creation mechanism or initial singularity.

## 1. The missing quantity is an atomic endpoint, not another free ruler

The complete 335 saved finite-pressure histories supply H(A), baryon and
photon densities, and bounded sound integrals. Their profiled DESI ruler
specifies a required drag-epoch interval, not a predicted endpoint. Preserve
all 335 histories, all 1,340 mechanical labels and the matched dust controls;
no selection by the previous BAO score is needed for the next calculation.

For this branch retain T_gamma=T0 A, the same late massless-neutrino
convention, zero nonstandard energy injection, and the SAME inverse point's
atomic helium mass fraction. The existing BBN score used a different,
nucleon-mass helium column. Its atomic column is available in the resident
PRIMAT table but must be interpolated with the declared point/stencil and
identified as the same fixed-heating proxy, not exact scalar BBN.

The newly run finite-slice growth test begins at A=101 with collisionless
radiation. It cannot supply ionization, photon/baryon drag, last scattering,
or an earlier photon collision history by extrapolating those equations.

## 2. An exact comparison inside a deliberately limited atomic model

The authors' [HYREC hydrogen source](https://raw.githubusercontent.com/nanoomlee/HYREC-2/master/hydrogen.c)
contains a three-level hydrogen rate with a unit fudge factor, distinct
from its precision multilevel calculation. Detailed-balance photoionization
uses the radiation temperature, not the matter temperature. For neutral
helium, no injections and T_m=T_gamma, its structure is

    dx/dN = -n_H alpha_B(T) [C(H,x,T)/H] [x^2-S(T,n_H)(1-x)],
    N=ln a, x=n_e/n_H=x_HII,
    C=(a+bH)/(a+bH+c),
    a=Lambda_2s>0, b=3 R_Lya/H>0, c=4 beta_B>0.               (1)

Here b is evaluated at fixed x,T,n_H; it is not an independent parameter.
S is the ground-state Saha factor. No empirical multiplier is calibrated
against our expansion histories. Direct differentiation, independent of a
numerical ionization solution, gives

    d(C/H)/dH = -[(a+bH)^2+a c]/[H^2(a+bH+c)^2] < 0.         (2)

In the hydrogen recombination temperature range the Saha root decreases
with N: S is proportional to T^(-3/2) exp[-chi_H/(k_B T)], and
d ln S/dN=3/2-chi_H/(k_B T)<0. A solution started at or above that root
cannot cross below it. For the same initial x, temperature and baryon
history, the scalar ODE comparison theorem therefore implies

    H_new(A)>=H_dust(A)  ==>  x_new(A)>=x_dust(A).             (3)

The antecedent follows for our matched positive-pressure state at A>=1
from e(A)>=e1 A^3. Faster Lyman-alpha escape does not reverse (3), because
the relevant coefficient is C/H rather than C alone.

This does NOT fix the drag endpoint's direction: the drag integrand
contains n_e/H, and both numerator and denominator increase. Nor is (3) a
precision recombination theorem: it explicitly assumes T_m=T_gamma,
neutral helium and the limited three-level closure. The
[HyRec methods paper](https://arxiv.org/html/1011.3758v2) develops the
multilevel and radiative-transfer terms omitted by that closure.

A small independently written Python realization of (1), optionally with
a separately declared matter-temperature equation, could test numerical
endpoint sensitivity using already installed NumPy. It would execute our
own reviewed equations, not downloaded software. Meaningful controls are
Saha stationarity, the sign/comparison (2)-(3), x in its physical interval,
independent time refinement, matched dust and a declared high-temperature
initialization sensitivity. Such a calculation would be a limited atomic
diagnostic. Without a bounded model-discrepancy estimate it cannot replace
the precision ruler or turn a discrepancy into an observational exclusion.

## 3. A useful drag bound without a fitted reionization history

Let n_H0 be the ordinary hydrogen-nucleus density, f_He=n_He/n_H,
Rb(A)=Rb0/A with Rb0=3 Omega_b/(4 Omega_gamma), and define

    tau_d(z)=integral_0^z c_light sigma_T n_e(z') /
                      [(1+z')H(z')Rb(z')] dz'.                (4)

In a low-temperature ordinary H/He plasma with no extra charged particles
or pair production, ionization alone cannot give more than
n_e<=n_H0(1+2f_He)A^3. The already owned background satisfies
H>=Hcal sqrt(Omega_m)A^(3/2) for A>=1. Therefore any low-redshift history,
even fully ionized, obeys

    0 <= tau_d(0,z_L) <= U_L,
    U_L = [c_light sigma_T n_H0(1+2f_He)/(Rb0 Hcal sqrt(Omega_m))]
                         (2/5)[A_L^(5/2)-1].                 (5)

This is dimensionless: c sigma_T n_H0 and Hcal both have units s^-1.
The inequality does not claim all baryons remain diffuse/ionized. It is a
conservative electron-number upper bound within the specified plasma.

Suppose an independently qualified atomic calculation supplies the
high-redshift integral J(z)=integral_(z_L)^z of the actual integrand in (4).
If U_L<1 and both levels are crossed, monotonicity gives

    z_d in [J^(-1)(1-U_L), J^(-1)(1)].                         (6)

The corresponding sound-ruler interval has reversed endpoints, with the
already retained early-tail interval added. No assumed reionization fit is
needed when that interval is sufficiently narrow. If U_L>=1, or a level
is not crossed, retain that limitation rather than inventing an endpoint.

There is also a weak atomic-model-independent necessary screen: integrate
(4) with its fully ionized upper electron density and the actual owned H.
If this upper depth first reaches unity at z_min, any admissible drag root
has z_d>=z_min, hence r_drag<=r_gamma(z_min). A required BAO ruler wholly
above that upper interval is inconsistent with this electron inventory.
Otherwise the screen is inconclusive; it is not evidence for recombination
success. This bound requires the temperature domain to remain below pair
production and is not a bound for an unspecified network-created plasma.

## 4. Precision route and exact present blocker

A targeted J filename inventory still finds no resident HYREC/Recfast
implementation or atomic-rate tables. The existing Python/NumPy runtime
is sufficient for the limited calculation above; no software installation
is needed. It is not a substitute for missing precision rate/transfer data.

The shortest precision route remains the authors' standalone HYREC FULL
interface already specified in FINITE_PRESSURE_BAO_AND_RULER_DESIGN_V001.md
section4. The inspected [history source](https://raw.githubusercontent.com/nanoomlee/HYREC-2/master/history.c)
accepts an external H array. Before use, freeze one exact upstream revision,
the five C/header pairs and required atomic tables, inspect its license
metadata, and supply an explicit separate driver selecting FULL before
allocation. Do not silently use the internally computed standard H or
extrapolate the fitted SWIFT correction. The current source URLs are read-only
discovery references, not a pinned executable receipt.

Authority correction after reading the actual handoff: the standing user
restriction prohibits software/package installation and infrastructure
changes, not a reviewed project-local scientific build with an existing
compiler. The earlier wording here incorrectly promoted this agent's
temporary no-download/build assignment into a categorical user-approval
requirement; that misunderstanding is preserved in
RECOMBINATION_AUTHORITY_CORRECTION_V001.md. Bounded source/data retrieval,
local compilation and a reviewed stdout-only adapter are ordinary in-scope
implementation, subject to actual sandbox/resource checks and root's sole
producer scheduling. They do not authorize installation, system changes or
unrelated code. No build or atomic execution occurred for this note.

The adapter must use the same H(A), omega_b, T0 and atomic Y for every state;
own the source's external-H grid contract/ranges and units; qualify a
standard reference, internal/external same-H agreement and independent H
grid/atomic time refinement. Bound the low-z tail using (5)-(6). Then the
predicted r_drag removes the one profiled BAO scale. Ordinary atomic physics
is imported explicitly; exact scalar BBN, primordial perturbations, full
TT/TE/EE and the separate network photon-origin mechanisms remain separate
tests rather than being declared complete by that ruler.

## Read provenance

- FINITE_PRESSURE_BAO_AND_RULER_DESIGN_V001.md, fully read, SHA256
  891c7b0c2d0a91872bdde2988e8bf4414762beda836be700a2197a861160f00f.
- FINITE_GAP_CMB_PERTURBATION_DISCRIMINATOR_V001.md, fully read, SHA256
  e0eae5fd62795a3619a402def4549927a44e716a99ed3b5f69203472c297c525.
- The primary HYREC paper/source links above were opened read-only on
  2026-09-29. No external source was downloaded, imported or executed.

No numerical value, fit, recombination success or exclusion is produced by
this note. Equations (2), (5) and (6) are constructive analytical controls
for the next owned atomic calculation, not extra arbitrary model parameters.

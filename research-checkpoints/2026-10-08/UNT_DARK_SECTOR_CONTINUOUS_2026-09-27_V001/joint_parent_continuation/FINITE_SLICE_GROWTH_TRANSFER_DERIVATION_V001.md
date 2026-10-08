# A finite-slice, same-state growth and metric transfer

2026-09-29. New conditional linear initial-value diagnostic; no producer run,
primordial-spectrum fit, CMB likelihood or native clock identification.

## 1. What this next calculation can decide

The five saved finite-pressure BAO files contain all335 distinct homogeneous
histories and1,340 mechanical labels. Their profiled ruler does not predict
clustering. For finite-gap rows the saved present hard-horizon intervals span
approximately3.82–140.42 Mpc, and cI2 at A=1101 spans9.04e-8–0.03435. These
are not observed suppression bounds. A transfer calculation must include the
same pressure, metric forcing, initial data and ordinary radiation shear.

The smallest useful next step is a finite-slice transfer from A_i=101 to A=1,
with fixed physical k={1e-4,1e-3,1e-2,1e-1} Mpc^-1. The upper wave number is
retained because low-k-only propagation would miss much of the pressure
leverage. All335 histories remain; no history is selected by a favorable
BAO, supernova or perturbation result. These already calibrated/exposed
backgrounds are not independent replications or blind predictions.

Adopt, explicitly for this test, pressureless baryons and collisionless
massless ordinary photons/neutrinos after the initial slice. This is a
post-drag idealization, not a precision treatment of residual/reionization
scattering, gas pressure or massive neutrinos. It is sufficient to test this
specified late transfer. A through-drag or observed CMB calculation still
needs the previously identified ionization/Thomson/visibility calculation.
No Big Bang, inflation, singular origin, or continuation to a=0 is assumed.

## 2. Closed Q=0 system and exact finite-slice initial constraints

Use conformal length eta=c integral dt/a, Fourier convention exp(i k.x),
and metric a^2[-(1+2Phi)deta^2+(1-2Psi)dx^2]. Primes here mean d/deta.
Write Hc=aH/c and E_j=4piG a^2 rho_j/c^4, with rho_j an energy density.
The same hard fluid has the already owned w(a), cI2(a), zero shear and Q=0:

    delta_H' = -(1+w)(theta_H-3Psi')-3Hc(cI2-w)delta_H,
    theta_H' = -Hc(1-3cI2)theta_H
                         +k^2[Phi+cI2 delta_H/(1+w)].       (1)

Baryons obey delta_b'=-theta_b+3Psi', theta_b'=-Hc theta_b+k^2Phi.
Vacuum stays unperturbed. There is no replacement G -> G/mu. Define

    U = [E_H(1+w)theta_H+E_b theta_b+(4/3)E_r theta_r]/k^2,
    Phi = Psi-4E_r sigma_r/k^2,
    Psi' = U-Hc Phi.                                      (2)

The independent Hamiltonian constraint is

    k^2Psi+3Hc U+E_H delta_H+E_b delta_b+E_r delta_r=0.      (3)

At the initial finite slice put Acal=E_H(1+w)+E_b+(4/3)E_r. For
independently declared Psi_i and q_i=Psi_i'/Hc_i, choose

    v_i=Hc_i(Psi_i+q_i)/Acal_i,
    d_i=-k^2Psi_i/Acal_i-3Hc_i v_i,
    delta_j,i=(1+w_j,i)d_i,   theta_j,i=k^2 v_i.            (4)

Set initial radiation multipoles l>=2 to zero. Then Phi_i=Psi_i and both
constraints hold exactly. The two columns (Psi_i,q_i)=(1,0),(0,1) define
an instantaneous-adiabatic, shear-zero subspace. They are unit transfer
normalizations, not physical unit metric perturbations. They are not the
complete initial mode space, and are not claimed to be the regular primordial
growing mode. A small linear amplitude multiplies a whole column or fixed
linear combination afterward, not each epoch independently.

The Q=0/soft-zero internal realization is consistent with (1)-(4). Its
preferred clock obeys the existing COSMIC-time equation pi_dot=Phi, so
pi'=a Phi/c in this conformal-length convention. It is not identified with
the hard velocity potential. The independently adopted scalar fluid action
needs no unresolved microscopic H/omega gate to run this test; deriving that
action by native oscillator averaging remains a different unproved claim.

## 3. Radiation without a low-multipole closure

For massless collisionless brightness F(eta,mu),

    F'+ik mu F=4Psi'-4ik mu Phi.

The separately labeled ordinary photons and neutrinos have equal initial
brightness under (4); their identical collisionless equations preserve this
equality. They can therefore share one angular distribution, weighted by
their separate fixed background densities. This simplification would NOT
hold through photon scattering, unequal radiation initial states or massive
neutrinos. It does not replace the hard component by radiation.

Write F=E+iO, E even and O odd in mu. On0<=mu<=1,

    E'=k mu O+4Psi',       O'=-k mu(E+4Phi),
    delta_r=integral E dmu,
    theta_r=-(3k/4)integral mu O dmu,
    sigma_r=-(1/2)integral P2(mu)E dmu.                    (5)

Initial E=4d_i/3 and O=-4k v_i mu recover (4) exactly. Angle quadrature
retains an entire free-streaming distribution, not an imposed low-l tail.

A useful exact integrating factor is G=F+4Phi and
Ghat=exp[ik mu(eta-eta_i)]G. The monopole shift does not change theta/sigma.
If G=Eg+iOg, then

    sigma_r'=-(k/2)integral P2(mu)mu Og dmu,
    Phi'=Psi'+8Hc E_r sigma_r/k^2
                       +(2E_r/k)integral P2(mu)mu Og dmu,
    Ghat'=4 exp[ik mu(eta-eta_i)](Psi'+Phi').             (6)

Here E_r'=-2Hc E_r. Thus (6) needs neither a numerical metric second
derivative nor an implicit angular-source solve. It removes homogeneous
streaming oscillations exactly; the remaining source quadrature must still
be time-refined. Recover delta_r=integral Eg-4Phi.

There is a finite, data-independent phase ceiling. Positive pressure implies
rho_H(A)>=rho_H(1)A^3, hence

    k(eta-eta_i) <= X(k)= (ck/Hcal)
                     2[1-A_i^(-1/2)]/sqrt(Omega_m).       (7)

For n-node Gauss-Legendre on[0,1], a polynomial p of degree d<=4 times
exp(ixmu) has the conservative absolute quadrature bound

    |error| <= 2 C_n sum_(j=0)^d binom(2n,j)
                      ||p^(j)||_infinity X^(2n-j),
    C_n=(n!)^4/[(2n+1)((2n)!)^3].                         (8)

Apply the ordinary Gaussian derivative remainder separately to real and
imaginary parts and use Leibniz's rule. The x=0 polynomial is integrated
exactly. The free initial-dipole contribution to the third moment in (6)
contains P2(mu)mu^2, of degree4; retaining only degree3 would miss this term.
The other free/forced kernels have no higher degree. Evaluate (8) in log
space for the prospectively fixed orders.
This certifies the angular MEMORY KERNELS, not an a priori bound on the full
coupled solution: source time integration, constraint propagation and doubled
angular solution comparisons remain compulsory.

## 4. Exact background coordinate and useful outputs

Use the sealed BAO kernel, not a new equation-of-state fit. For finite action
t=log(r/r1), A(t)^3=exp(t)bar(r)/bar(r1) and lambda=dlog I/dlog r.
Integrate forward with x=t_i-t, so

    dlog a/dx=lambda/3,
    d[(Hcal/c)(eta-eta_i)]/dx=lambda/(3 a H/Hcal).          (9)

The dust limit uses t=3log A. The background is evaluated directly at every
stage; no tabulated w/H interpolation or new physical parameter is needed.
The conformal-time integral in (9) has an independent original-kernel
quadrature check. The clock variable Pclock=Hcal*pi obeys

    dPclock/dx=lambda Phi/[3(H/Hcal)],                    (10)

not lambda Phi/(3aH/Hcal). This extra a distinction is essential.

Save signed densities/velocities, the comoving contrasts
Delta_j=delta_j+3Hc(1+w_j)theta_j/k^2, Weyl=(Phi+Psi)/2, slip and clock tilt.
Retain all epochs/basis columns, even zero crossings or large gains. Compare
with the same-baryon, same-total-present-matter, same-ordinary-radiation
pressureless comparator. Do not turn an amplitude-free transfer into a
sigma8, f sigma8, primordial power spectrum or observational exclusion.

Two columns also permit an initial-mixture check without per-epoch fitting:
one initial vector must reproduce an entire multi-epoch trajectory. Resetting
the two basis vectors at a later initial slice is a DIFFERENT preparation,
not a time-convergence test. A proper restart transports all species and
radiation angular data, including generated entropy and shear.

## 5. Earliest necessary route to the actual CMB comparison

This late IVP cannot determine the pre-A101 transfer. Next, the same H(a)
must drive the qualified FULL recombination interface already identified,
including the correct atomic helium convention. That fixes drag/visibility,
allowing the profiled BAO ruler to be replaced by a predicted ruler. Through
drag, retain Thomson photon/baryon momentum exchange, radiation polarization
and ordinary neutrino shear. First return intrinsic photon monopole+Phi,
baryon velocity, Weyl driving and quadrupoles before angular TT/TE/EE projection.

Observed spectra additionally require a DECLARED finite-slice stochastic
perturbation spectrum and correlations, followed by projection and foreground/
likelihood treatment. A finite adiabatic spectrum may be an explicit state
assumption without asserting inflation or an initial singularity; its freedom
must be counted. Nonzero Q or free k-dependent entropy cannot be silently
introduced to repair residuals. Homogeneous horizons do not replace this map.

None of these equations creates a photon or a Planck spectrum. The separate
continuous-network thermal-origin/source/energy-debit and CMB-fluctuation
mechanisms remain required science, not supplied by the imported ordinary
radiation in this conditional gravitational branch.

Resident derivations fully read: ALPHA_ONE_FLRW_ENTROPY_INTERFACE_V001.md;
FINITE_GAP_CMB_PERTURBATION_DISCRIMINATOR_V001.md;
PHYSICAL_TIME_AND_RELEASE_STATE_MAP_V001.md; and the sealed BAO kernel/design.
Law peer independently checked (4),(5) and the Gaussian bound (8). No new
observational data or numerical perturbation result was used to set this test.

# Same-state spherical release and a finite-time dust shadow V001

2026-09-29. Additive analytical reduction, no evolution or observational fit.
This changes the synthetic ordinary geometry, not the hard energy, abundance,
equation of state or vacuum matching. It does not replace the outstanding disk,
full-metric lensing or merger tests. The existing geodesic-clock, zero-soft,
alpha-one scalar branch is adopted; no native-to-metric derivation is claimed.

## 1. A conservative cold/weak-field limit, with its actual errors named

Write S=gstar^2/(4pi G Kb), beta=.005, and keep the actual saved R,I and e(I).
The conserved quadratic-action mass label, internal energy and pressure are

    rho0=S beta R I/c^2,       u=S beta[e(I)-R I],
    p=rho0 u_rho0-u=S beta[I omega-e],
    hN=u_rho0=c^2(omega/R-1),
    cN^2=dp/drho0=c^2 I eII/R=(omega/R)cI^2 c^2.       (1)

rho0 is a normalization of the existing current, not a new population. In
particular replacing cN^2 by cI^2 c^2 without its stated cold error is wrong.
The full relativistic inertial density is S beta I omega/c^2, and its energy
density is S beta e/c^2. The two separate dimensionless defects are therefore

    dE=e/(RI)-1,                 dW=omega/R-1.          (2)

Both are positive at positive action. dE=(dW-w)/(1+w), equivalently
dW-p/(RI). The latter form can be evaluated without subtracting two nearly
equal O(1) quantities. Compression must reevaluate these coefficients; their
present values alone do not establish a later cold interval.

Let A(t) be the retained cosmological scale factor, A(t_i)=1, x a comoving
length and D_s=A^3 rho0_s for s=b,H. The leading action, with S_s the velocity
potential and v_s=grad S_s/A, is

    L=int d^3x sum_s[-D_s S_s,dot-D_s|grad S_s|^2/(2A^2)
                    -A^3 u_s(D_s/A^3)]
      -int d^3x[(sum D_s-Dbar) Phi+A|grad Phi|^2/(8pi G)].

Here u_b=0 and u_H is (1). Its equations are

    D_s,dot+div(D_s v_s)/A=0,
    (partial_t+v_s.grad/A)v_s+H v_s=-grad(Phi+hN_s)/A,
    Delta Phi=4pi G(sum D_s-Dbar)/A.                  (3)

Thus both the ordinary seed and hard current move and gravitate. There is no
fixed baryon potential or freely fitted halo. This is an explicitly controlled
nonrelativistic reduction, not an exact Einstein solution. The full parent
also has the energy/enthalpy corrections (2), relativistic velocities and
metric/time/ordinary-radiation terms. Small pointwise coefficients are not a
theorem about accumulated trajectory error or about a small *increment* to a
lensing signal.

On a full domain where the surface terms exist, its energy obeys

    d(T+U_ex+W)/dt=-H[2T+W+3 int A^3(p-pbar)d^3x],     (4)

where T=int D v^2/2, U_ex=int A^3(u-ubar), and
W=int(delta D Phi)/2. Finite worldtubes must retain their current, pressure
work and gravitational energy flux; one must not use (4) after discarding
them. Infinite homogeneous matter need not have zero perturbation flux at
infinity. Separate finite-worldtube ledgers are safer than assuming that it
does. Ordinary radiation and the matched vacuum remain in the specified
background; neither is independently renormalized by this local reduction.

## 2. A new compact spherical ordinary seed, not a fitted halo edge

Keep ell=3.2 kpc and GM=gstar ell^2. Replace the old disk by the explicitly
declared, nonrotating, compact ordinary rest perturbation

    rho_seed(q)=M/ell^3 * 3465/(512pi) * (1-z^2)^4,
    z=q/ell, 0<=z<1;                 rho_seed=0 for z>=1.

It is positive, C^3 across its surface, and has exactly total mass M. Its
enclosed mass fraction is

    m(z)=3465/128 [z^3/3-4z^5/5+6z^7/7-4z^9/9+z^11/11]
         for z<1;                  m(z)=1 for z>=1.    (5)

The physical source size is an inherited synthetic source scale, not a halo
radius inferred from data. The hard initial action remains spatially uniform;
both peculiar velocities vanish. The proper-volume initial Einstein constraint
has O(GM/(ell c^2)) corrections to these Newtonian labels, so this preparation
is the leading weak-field counterpart, not the identical old constrained disk.

## 3. An exact finite-time dust-shadow generator on the owned background

Set tau=(t-ti)/t_dyn, t_dyn=sqrt(ell/gstar), and define q/ell=z. Let the common
reference shell map be x=q f(z,tau), with f=1 and f_tau=0 initially. The
background A(tau) uses the SAME unreset finite-R homogeneous energy e(I1/A^3),
ordinary baryons and matched vacuum. The old reference is late-time and omits
ordinary radiation; a separately labeled radiation omission scale is required.

Write kappa=4pi G(rho_b1+rho0_H1)t_dyn^2/3, mu(z)=m(z)/z^3, Ht=H t_dyn.
Gauss' law and conservation of each initial mass label give the ODE

    f_tautau+2Ht f_tau=F(f,mu,A),
    F=-A^-3[(mu+kappa)f^-2-kappa f].                  (6)

The z=0 value is mu(0)=1155/128. No outer wall, incoming source or fitted
halo radius appears: every shell is a restriction of the same unbounded
spherical reference. The seed itself moves. Equation (6) is a dust SHADOW
on the owned background, not a claim to solve the finite-R Euler equation.
Deleting its local pressure is an explicit test-function construction, not a
physical reset of e,p or the cosmological H. These are retained for residuals.

Since f depends on z only through mu, propagate parameter derivatives rather
than finite-differencing a noisy density:

    F_f=A^-3[2(mu+kappa)f^-3+kappa], F_mu=-A^-3 f^-2,
    F_ff=-6A^-3(mu+kappa)f^-4,      F_fmu=2A^-3 f^-3;
    f_mu''+2Ht f_mu'=F_f f_mu+F_mu,
    f_mumu''+2Ht f_mumu'=F_f f_mumu+F_ff f_mu^2+2F_fmu f_mu.

All derivative initial data vanish. Then

    s=f+z f_z, J=f^2 s, I=I1/(A^3 J),
    J_z=2f f_z s+f^2(2f_z+z f_zz),
    rho_b=(rho_b1+rho_seed)/[A^3 J],
    rho0_H=rho0_H1/[A^3 J].                            (7)

f>0 and s>0 are the two shell-map conditions, not merely positive averaged
density. The actual finite-R pressure acceleration omitted by the generator,
evaluated on this complete moving reference, is outward-positive

    aP/gstar = (cN^2/(gstar ell)) J_z/(A s J).         (8)

It follows directly from -grad hN. At initial time J_z=0, so its first
nonzero response is delayed; this worker goes beyond that known Taylor jet.
The signed force, internal energy, pressure and work are retained at every
readout. A positive aP is not required as a numerical success criterion.

## 4. Accumulation, domain and what a residual does NOT prove

For the actual finite-R solution, any *proved* bound |aP|<=P(t) on a common
pre-crossing tube, together with a bound L on the difference of the complete
two-species physical gravitational acceleration per physical displacement
(equivalently g/A per comoving displacement), gives (H>=0)

    E_x(t)<=int_0^t sinh[sqrt(L)(t-s)]/sqrt(L) P(s)/A(s) ds,
    E_x(t)<=Pmax[cosh(sqrt(L)t)-1]/L                  (9)

when P/A<=Pmax. The continuous L=0 limit is Pmax t^2/2. This follows by the
positive Volterra comparison after dropping nonnegative Hubble damping.
For a general discretized full vector field the corresponding statement is
||error(t)||<=int exp[int_s^t L_F]||residual(s)||ds, provided L_F bounds its
Jacobian on a tube containing BOTH trajectories. A dust-only Jacobian is not
the finite-pressure operator and cannot certify this condition.

The shadow gives an accumulated *forcing diagnostic*: integrate |aP| with
the Hubble-damped free velocity/displacement kernels. It does not supply the
actual P(t), its spatial derivative bounds, or L_F in (9). No small pointwise
or accumulated shadow residual alone earns a finite-R trajectory qualification.
Output those missing items explicitly, rather than converting a residual to
an invented error bar. A separate pressure-source work integral is useful
bookkeeping but is likewise not a stability proof.

A finite-R radial evolution has characteristics dx/dt=(v+-cN)/A in (3).
For an interior radius xwatch and an outer numerical interface L, a sufficient
non-arrival condition is int max(|v|+cN)/A dt < L-xwatch, using an ACTUAL
interval bound. Exterior spherical mass changes only a potential constant,
not the enclosed acceleration. Therefore an acoustic/advective domain guard
is possible without treating L as a halo radius. Shadow characteristic travel
is reported only as a diagnostic; it does not certify the actual finite-R tube.

The unforced clock remains a separate geodesic field in the parent. On the
dust shadow its geodesic congruence shares the reference flow until crossing;
finite-pressure matter need not do so. A lost shell Jacobian ends this method
control; no shock, viscosity or interpenetrating stream is introduced.

## 5. Weak-field, radiation and lensing readouts

Retain at least dE,dW, v^2/c^2, the potential span/c^2, and the source-scale
compactness GM/(ell c^2). The hard correction to a rest-mass gravitational
source is delta[S beta(e-RI)]/c^2; the active-pressure coefficient is 3p/c^2.
Neither is included secretly in a rest-only force or set to zero in the ledger.
Time derivative/slip/vector/retardation contributions to an Einstein/null
readout remain uncomputed unless an actual metric reconstruction supplies them.

For ordinary collisionless radiation on a specified weak scalar metric,
G=F+4Phi/c^2 satisfies dG/dt=4(Psi_dot+Phi_dot)/c^2 along its characteristic.
If F initially vanishes, a conservative brightness bound is

    |F| <= 4(||Phi_i||+||Phi_t||)/c^2
            +4 int (||Psi_dot||+||Phi_dot||)/c^2 dt.   (10)

This bounds fractional radiation energy and angular moments on that metric;
it is not a bound if the potential norms/time variation have not been owned.
The saved ordinary photon density and the declared massless-neutrino factor
can convert it to a missing stress scale. No PRIMAT heating history or new
radiation observation is inferred. A late-time omission scale alone does not
give a complete accumulated metric-error theorem.

For a finite spherical worldtube, the projected excess mass inside impact b
is the exact density integral with weight 1 for r<=b and
1-sqrt(1-b^2/r^2) otherwise. Its conditional thin-lens contribution would be
4G M_2D/(c^2 b), but the omitted exterior, slip and photon flight-time terms
remain explicit. This first shadow implementation reports enclosed excess
mass and current, not an observed or full finite-distance lensing prediction.

## 6. The next solver if the shadow cannot qualify the fluid

Equations (1)-(3), with two separate conserved density/momentum fields, are
the minimal conservative finite-R alternative. For spherical finite volumes,
use shell volumes and face areas exactly; balance the constant-pressure
geometric term, evolve the ordinary seed, and retain boundary mass/energy
flux. Compare radial/time refinements and two exterior interfaces, checking
actual interval characteristic travel and current. The finite-R result must
retain its own density/action/pressure and crossing tests, not inherit the
shadow's favorable values. No independently chosen dark profile is needed.
Its weak-field numerical result would still not replace a full-metric disk
or post-crossing merger calculation. Native unitary regularity supplies no
automatic identification with a missing dispersive/kinetic continuation.

The first prospective execution uses BOTH old R=128 and R=8192,
spectrum1/reference0 method states already used by the smooth-disk certificate.
They remain method controls, not newly acceptable joint cosmological states.
The whole inferred-state census can only be claimed after its actual execution.
All initial actions, energy, pressure, calibration exposure and baseline are
carried unchanged. There is no physical desired-sign or observed-fit gate.

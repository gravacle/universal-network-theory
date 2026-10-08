# Full nonlinear common-pulse test: prospective protocol V001

2026-09-29. Six synthetic design cases, not a fitted cosmic abundance or galaxy
model. The parent owns the sole numerical run. The worker is stdout-only:
`freeze` prints the input snapshot; `run` requires that saved snapshot and prints
the result. Publication is by the parent using apply_patch. No earlier result,
state, spectrum or matched constant is overwritten.

## Fixed physics and full retained state

Use kappa=u4=m=A=1, epsilon=.001, soft measure delta ddelta, hard weight=.005,
R in {32,64,128}, Hp in {1,4}, n=8, and inherited gs=21.65919852693508 read
from the authenticated common-history result. All modes start at y=v=0.
One signed source acts on every mode:

    h=Hp sin^2(pi t/T) cos(Rt), T=2pi n/R, 0<t<T,
    hdot=Hp[(pi/T)sin(2pi t/T)cos(Rt)-R sin^2(pi t/T)sin(Rt)].

Set h=hdot=0 exactly at and outside both endpoints, not sin(pi) roundoff.
The physical clamped source is g=h/sqrt(1-h^2/gs^2), with its exact derivative.
Integrate the FULL scalar equation yddot=delta h-delta^2 y-y^3, not its
linearization. No state is reset to equilibrium or rephased after the pulse.
Hp=4 is a stronger design control, not a selected successful amplitude.

Recompute Kb=sum weights and the finite-parent positive endpoint
DeltaU=sum w[delta^2 ys^2/2+3ys^4/4], ys^3+delta^2 ys=delta gs,
for each enlarged spectrum. The same finite soft parent is its baseline.
Retain C=2M^2/Kb and report rho_vac/(2M^2)=DeltaU/Kb. No independently
chosen offset compensates the atom. Verify endpoint roots by bisection.

## Prospective numerical census and qualifications

For EACH of the six cases run RK4 with (soft nodes, steps PER hard cycle)
=(64,256),(128,256),(128,512), i.e.2048,2048,4096 steps per pulse.
An independent fixed-step Cash-Karp fifth-order method uses (128,256).
No adaptive outcome selection or physical success gate is introduced.
Every coarse/independent aggregate is retained even when a check fails.

Both methods integrate two work channels, Kb*g*gdot and -B*hdot, where
B=sum w delta y. The full energy is Kb*g^2/2+sum w[v^2/2+delta^2y^2/2
+y^4/4-delta h y]. Check its work identity at every completed step.
The pulse returns its contact energy to exactly zero. Endpoint mode energy
is positive retained source work, not a debit from DeltaU.

Fix BEFORE outcomes Eref=Kb Hp^2+wH*pi^2*n^2*Hp^2/8,
phase-space scale Hp*n, and tiny-soft-energy comparison scale
max(1e-14,1e-12 Eref). Work/energy errors divided by Eref must be<=2e-7.
Same-grid RK4 refinement and independent-method differences
max(|delta Delta y|,|Delta v|)/(Hp*n) must be<=5e-7.
Same-step soft quadrature comparisons of total energy/B/Bdot use the fixed
scales Eref, Kb Hp*n, Kb R Hp*n and tolerance2e-6. The soft energy difference
uses the stated tiny scale and tolerance2e-6; absolute and raw relative errors
are also reported, with no claim of strong relative accuracy when below that
absolute scale. Fine/coarse energy and source-work comparisons use2e-7.
No tolerance is changed from an observed outcome.

At h=0 derive b^2=4e/[delta^2+sqrt(delta^4+4e)] from each actual end state.
Independent endpoint-safe orbit quadrature uses y=b sin(theta), theta in
[0,pi/2], with time weight [delta^2+b^2(1+sin^2 theta)/2]^-1/2.
Use64/128 Gauss nodes and relative2e-9 on action, pressure and mean y^2;
compare the exact pressure/virial/action identities and exact susceptibility
normalizations at2e-11 scaled algebra tolerance. This is a phase-average
readout of the retained orbit, NOT a claim of dephasing or equilibrium.

For numerical source controls, fixed256-point Gauss integration checks the
analytic resonant integral Hp*T/4 and zero pulse endpoint values at2e-11
scaled tolerance. Harmonic energy, frequency-detuning and soft-leakage
predictions are SCIENTIFIC COMPARISONS, not pass conditions for the nonlinear
outcome. The oscillator atan2(delta*y,v) is labeled a harmonic phase
diagnostic, not an exact nonlinear angle.

## Output and interpretation

Save complete fine128 end delta/weights/y/v, modal energy/action/period/pressure,
exact scalar susceptibility/contact deficit and harmonic phase diagnostics.
Retain total/soft/hard energy, work channels, instantaneous final B and Bdot,
and D_inst(g=0)=-B/Kb to expose coherent polarization. Report exact post-pulse
orbit frequency, hard frequency shift and n*eH/R^4; none is claimed to be a
measured cosmological rate. All scalar/vector scope restrictions remain.

Compute relaxed old/new forces at the fixed sources
g={.0001,.001,.01,.1,1,10,100}, keeping the finite soft cutoff/contact in both
definitions. Save their differences and the changed matched vacuum baseline;
do not compare them to observed galaxy residuals or call them the excited-state
force. All new pulse/spectral choices are explicit. This tests nonlinear energy
transfer and its compulsory response/stress costs, not the native origin of
the source, a full metric release, or an observed dark-sector explanation.

The arrays are at most129 modes and the fixed integration census is61,440
vector steps. There is no physical run deadline. Output must remain below
1MiB; only the fine states have full modal arrays. No library installation,
large matrix, fit, or new long-time evolution is needed.

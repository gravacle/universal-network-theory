# Retained geometry requires conditional states and a correlated phase readout

2026-10-03 UTC. Exploratory analysis of the eight saved x=2,4 states from
the finite supplied-geometry experiment. No formation history was rerun.
The record-diagonal population-only null is rejected in both preparations:
copying changes conditional graph-carrier states, not just record weights.
Meanwhile high connected probability is neither vanishing topology activity
nor a demonstrated physical clock. These are constraints on this finite
BS action and its declared preparations, not a proof against UNT.

## Conditional state information survives copy removal

After x=2, fragments evolve freely and no longer interact with the native
system. The full-native marginal evolves unitarily with the same H_native
for both copying histories. Its spectrum and all pairwise trace distances
are invariant during hold. The record-diagonal blocks separately evolve
under H_r=H_gc+r*(1-d0/2). This gives exact memory constraints, not an
assumption that the connectivity observable itself is constant.

| Preparation | Full-native on/off trace distance | Conditional r=0 distance | Conditional r=1 distance | Native purity with copying |
| --- | ---: | ---: | ---: | ---: |
| Path | 0.247072626152 | 0.075422242462 | 0.315445246598 | 0.750623691659 |
| Cycle plus edge | 0.246542877957 | 0.080462582095 | 0.310343129209 | 0.752142001878 |

The x=2 and x=4 values agree within the assigned arithmetic allowance.
Copying-off native states remain pure. The native trace distance between
the two different preparations is indistinguishable from 1 at that allowance,
with or without copying. Do not interpret the roughly 3e-13 deviation of
the copying-on distance from 1 as a resolved physical contraction.

For the tested null, reweight each copying-off record-sector state by the
copying-on sector probability without changing its conditional state. The
actual minus predicted connected probability is:

| Preparation | x=2 residual | x=4 residual |
| --- | ---: | ---: |
| Path | -0.000242673616 | +0.000390559976 |
| Cycle plus edge | -0.000018619207 | +0.000091695196 |

The conditional trace distances reject the state null independently of
whether a particular observable residual happens to vanish. The residual
bound sum_r p_on,r D_r is 0.178912099088 and 0.182529004472 respectively;
it is valid but loose for connectivity. This null concerns record-diagonal
blocks only, not cross-record coherences. Those coherences remain in the
full state and can matter for other probes.

These results quantify the actual formation history; they do not newly
discover the already established general failure of independent-marginal
closure. A state-qualified effective description remains possible, but an
instantaneous record-density substitution is insufficient in this example.

## Connectivity retention is not an inert topology

In x=tau/hbar units only the -h sum X_e term transports amplitude between
connected and disconnected graph sectors. With C the connected projector,

    J_C = -i h sum_e <[X_e,C]>,
    B_out = ||(1-C) H C psi||^2,
    B_in  = ||C H (1-C) psi||^2.

The latter two use the coherent sum of link-flip amplitudes before squaring.
They are not classical transition rates or actual second derivatives of
connectivity for the unprojected state. They identify available cross-sector
action that a small net current can hide. For the path:

| Copying and age | J_C | B_out | B_in |
| --- | ---: | ---: | ---: |
| Off, x=2 | -0.047852804612 | 0.515906445860 | 0.019440945093 |
| On, x=2 | -0.048258530407 | 0.515855851050 | 0.019524995071 |
| Off, x=4 | +0.108120283758 | 0.504943189883 | 0.035644890869 |
| On, x=4 | +0.104459573833 | 0.504654637409 | 0.035856012389 |

Thus the connected preparation is not annihilated by the operator that
couples it to disconnected configurations. Its high connected probability
does not establish protected or selected geometry. All disconnected-case
activities and currents are also retained in the result; no unfavorable
preparation is removed. Energy detuning and interference may contribute to
finite retention, but these readouts alone do not separate those mechanisms.

## The local record phase is not fixed by mean degree

This diagnostic deliberately uses A=|1><0| for the held active record, not
the earlier B0 clock. With z=<A> and z_d=<d0 A>, exact commutation gives

    dz/dx = i*(z-z_d/2),
    nu_A = d arg(z)/dx = 1 - Re(z_d/z)/2
         = 1 - <d0>/2 - Re[(z_d-<d0>*z)/z]/2.

The phase is reported only for |z|>1e-10; all eight saved states exceed that
guard by many orders of magnitude. No other readout is divided by this rate,
and there is no claim of a physical-time calibration, whole-window
monotonicity, or equivalence to another chosen clock. A sign of a phase rate
by itself is not a physical reversal of time.

At x=2, dropping the covariance term even changes the rate's sign:

| Preparation and copying | Rate using mean degree alone | Exact correlated phase rate |
| --- | ---: | ---: |
| Path, off | -0.000175716633 | +0.000138128827 |
| Path, on | -0.000146375585 | +0.004782354831 |
| Cycle plus edge, off | -0.000133933891 | +0.000772531199 |
| Cycle plus edge, on | -0.000117246189 | +0.003934785364 |

At x=4 the exact rates are respectively 0.009318008033, 0.016165878543,
0.010930003038 and 0.009396632851. Two positive-rate snapshots do not prove
a usable clock between them. The starting supplied graphs have d0=2,
making their fixed-degree reference gap 1-d0/2 vanish. Their initially
blank record also has z=0, so its phase is undefined initially; a zero
reference gap is not a defined initial zero-rate clock measurement.

There is a useful exact bound on the required state information. Write the
pure full state as its record components psi_0,psi_1; z=<psi_1|psi_0>.
With D=d0-2, p_r=||psi_r||^2, Cauchy--Schwarz gives

    |nu_A| <= (1/(2|z|)) * min(
        sqrt[p_0 * <r*(d0-2)^2>],
        sqrt[p_1 * <(1-r)*(d0-2)^2>]).

This holds wherever z is nonzero, in the declared generator units, with
normalized exact states. It retains correlations and has no fitted scale.
If both record components have exact d0=2 support, the local A phase cannot
advance during that interval. This is specific to the inherited gap and
feedback coefficients; it is not a general no-clock theorem for connected
networks. Connectivity alone imposes no such degree constraint. The bound
has been derived analytically here, not claimed numerically measured by the
saved-state worker, which did not compute these degree-variance moments.

## Scientific decision

The finite copying schedule does not provide a consistent connectivity
advantage, and its effects cannot be compressed to record counts or mean
degree. Do not add an autonomous controller solely to perpetuate that
schedule. The next useful question is whether an operational clock and
transport state can be obtained from the same correlations, with a bounded
time window and complete energy/source work. This is different from assuming
a ground state or a universal attractor, neither of which is required simply
to test a finite-window cosmological candidate.

Before another numerical experiment, derive a clock-window control from the
actual held equations, including amplitude zeros and the record-degree
correlation hierarchy. Determine whether available saved state and fixed-mesh
data suffice to qualify an interval; do not rerun formation just to obtain
a favorable clock age. A failure for A does not authorize swapping in the old
B0 rate without an explicit measurement and synchronization map. Do not call
a ratio of protocol derivatives a physical metric or acceleration.

### Prospective whole hold phase check from existing observations

Use all 33 already reported hold mesh points from x=2 after the switch
through x=4, without new evolution or a selected subwindow. Put e=1-d0/2.
Its eigenvalues are 1,1/2,0,-1/2, so ||e||=||e^2||=1. With h=1/3,

    [H_hold,e] = i*h/2 * sum_(three incident edges) Y_e,
    z'' = -<e^2 A> - i*h/2 * sum <Y_e A>.

Conserved record weights give |z'|<=sqrt(p0*p1)<=1/2 and
|z''|<=(1+3h/2)*sqrt(p0*p1)<=3/4. These are exact analytic
normalized-state bounds, not fitted finite differences. Use the conservative
global |z'|<=1/2 bound to avoid introducing measured populations into it.

For Delta=1/16, if |z_j|>Delta/2, every value over the next interval
lies in a radius Delta/2 disk about z_j that excludes zero. Relative to
z_j the disk lies in the positive half-plane. Consequently
arg(conj(z_j)*z_(j+1)) is the actual unwrapped phase increment over that
interval, with no hidden full winding. Strictly positive and negative
increments then disprove monotonicity in either orientation on the full
hold, even if both endpoint instantaneous rates are positive. Equal-sign
increments alone would not prove instantaneous monotonicity between samples.

Propagate the unchanged assigned 1e-10 per real/imaginary coherence component
as epsilon_z=sqrt(2)*1e-10. Require |z_j|-epsilon_z-Delta/2>0 for
the disk test. Bound the error of Im(conj(z_j)*z_(j+1)) by
epsilon_z*(|z_j|+|z_(j+1)|)+epsilon_z^2. Only classify an increment
sign when it exceeds that bound; otherwise mark it unresolved. These
data-qualified certificates remain conditional on assigned floating-point
allowances, not certified roundoff intervals. Preserve every interval and
all four preparations. No phase folding, new clock definition or altered
time origin is allowed in this diagnostic.

## Reproducibility

The diagnostic ran once, with no evolution or producer imports, in
0.251332 seconds and 75,431,936 bytes peak self RSS. It used native factors
of size 6144 by 4, record factors 3072 by 4, and reduced matrices at most
8 by 8; no dense native density matrix was allocated. All 449 assigned
arithmetic checks pass, maximum residual 1.75416e-14. Eigenvalues were not
clipped, evolved states were not renormalized, and floating-point intervals
are not certified. Explicit conditional divisions are not state preparation.

- Source native_finite_region_saved_memory_v001.py SHA256:
  6dc61417b878e20be07f89dbbaa3f343ded59b0d0994cb72a22bcc97b723e5a9.
- Result native_finite_region_saved_memory_v001_results.json SHA256:
  02f0f596f84cc26df17997131bfc14ac4674dedafca6aa32caf457160ac8e396.
- The frozen formation result and prospective diagnostic are pinned in
  NATIVE_FINITE_REGION_GEOMETRY_RESULT_V001.md; the original full-state
  result remains unchanged.

All eleven program lanes remain OPEN. No physical clock, ruler, gravity,
cosmic expansion law, observational superiority or Stage3 completion follows
from these finite internal checks. URM integration remains additive evidence.

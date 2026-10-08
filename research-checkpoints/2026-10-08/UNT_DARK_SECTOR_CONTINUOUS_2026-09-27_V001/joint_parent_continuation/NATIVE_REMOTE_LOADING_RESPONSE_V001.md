# A native link response beyond the matter location

2026-10-03 UTC. The original four-node action produces a change in a
nonincident link even when carrier hopping is switched off. This is a
constructive example of a response transmitted through native network
interactions, without moving matter into the measured region or invoking
record feedback. It is not a gravitational force, physical distance law,
galaxy fit or expansion result.

## The comparison and its controls

Vertices are `(L0,L1,R0,R1)=(0,1,2,3)` and edges are
`e0=L0R0, e1=L0R1, e2=L1R0, e3=L1R1`. Compare initially blank incidence with
no carrier against initially blank incidence with one fixed-content carrier
at L0. Both preparations have the same blank records and occupied writers.
The measured remote edge is e2: it is nonincident to L0, but shares R0 with
e0. The initial graph is disconnected. Neither these labels nor this support
relation defines a physical separation.

Use the inherited values
`h=Omega/N=1/2, Delta=4, Ud=d*=1, epsilon_psi=1, j=lambda_J=1/4, t=1/2`.
In every case `lambda_R=g_psi_r=g_rb=0`; continuing writers with
`epsilon_r=g_wr=1` give the same exact dressed clock

\[
x=\tau/\hbar,\qquad \theta=\sqrt5\,x.
\]

Thus “native” below means the inherited incidence/carrier coefficients in
this explicitly record-decoupled test, not the complete nonzero-feedback
formation experiment. Four other cases separately remove j, hopping t, the
complete degree penalty Ud, or both j and t. Each has its own empty-carrier
baseline. Removing Ud changes the blank-link gap from 2 to 4; it is not
silently held at 2. No source-dependent coefficient, selected age, tolerance
or fitted normalization was introduced.

The hopping-off arm changes the microscopic model for a diagnostic control.
In that arm carrier position is conserved by the Hamiltonian, rather than
held by an omitted external clamp. It does not establish an immobile source
preparation for the physical hopping-on model. All initial preparations and
their costs still need physical realization before astronomical use.

## Exact result

For the empty/source difference `Delta p_e`, all odd Taylor coefficients
vanish. Every link contrast vanishes through order two. At an incident edge,

\[
\Delta p_{0,1}
=-\frac{h^2}{12}(2kj+j^2+t^2)x^4+O(x^6),
\qquad k=\Delta+2U_d(1-2d_*).
\]

For the nonincident edges e2 and e3, the contrast vanishes through order six
and first appears at order eight, except in the exactly decoupled null:

| Case | Incident coefficient of x4 | Nonincident coefficient of x8 |
| --- | ---: | ---: |
| Inherited incidence and carrier coefficients | -7/256 | 3241/2949120 |
| j off | -1/192 | 899/5160960 |
| Hopping t off | -17/768 | 1307/1290240 |
| Degree penalty Ud off | -37/768 | -143/1376256 |
| j and t off | 0 | 0 |

The same-clock eighth-order coefficients are these values divided by 625.
In particular, the hopping-off contrast is

\[
\Delta p_2(\theta)=\frac{1307}{806400000}\theta^8
 +O(\theta^{10}).
\]

This positive coefficient describes link occupation, not attractive force.
The comparison with the negative incident coefficient is consistent with
degree competition: changing a source-adjacent link's energy can change the
occupation of another link sharing its endpoint. That mechanism is distinct
from assigning gravitating mass to a record halo.

With hopping present, carrier arrival at R0 starts at `h^2 t^2 x^4/4`;
the remote-link contrast nevertheless cancels through order six. With
hopping absent, arrival anywhere away from L0 is exactly zero for all times.
The degree-off arm isolates a distinct coherent transport/current route and
has a negative leading contrast. No claim that the two routes add
independently at finite coupling is made.

When j=t=0, the exact operator factorization is
`H_source=H_empty tensor I4+epsilon_psi I`. It proves the complete link null
at all times, not just through the computed series. Real symmetric matrices
and the real initial basis state make the displayed occupations even analytic
functions of x. The Taylor coefficients are exact; no quantitative finite-time
remainder bound or useful macroscopic time window has been established.

## Independent algebra and numerical verification

Before execution, the independent algebra reviewer predicted the leading
remote expression, with `u=2Ud`,

\[
\begin{aligned}
\Delta p_2={}&h^4 F_8 x^8+O(x^{10}),\\
F_8={}&(j^2+t^2)\left(\frac{ku}{504}
                         +\frac{19u^2}{20160}\right)\\
&+j\left(\frac{k^2u}{252}+\frac{ku^2}{315}
                         +\frac{u^3}{1680}\right)\\
&-t^2\left(\frac{kj}{168}+\frac{17ju}{3360}
                         +\frac{j^2+t^2}{448}\right).
\end{aligned}
\]

The connected calculation retains e0/e2 and carrier positions L0/R0/L1.
After constants are subtracted, its carrier blocks in link sectors 10,01,11
are `B=diag(k+j,k+j,k)-t T01`, `C=diag(k,k+j,k+j)-t T12`, and
`D=diag(2k+u+j,2k+u+2j,2k+u+j)-t(T01+T12)`. The sixth-order hopping
terms cancel as `5/60-4/12+9/36=0`; the remaining connected sixth-order
coefficient is loading-independent and cancels against the empty baseline.
At eighth order the hopping-off expression has an explicit factor u, showing
that its route needs the shared degree interaction.

The full four-edge exact worker independently reproduces all five frozen
predictions, including the equivalent native fraction `22687/20643840`.
It uses rational arithmetic on direct 16D/64D matrices and separately built
sparse actions, retaining every coefficient through order eight for all four
link and carrier readouts. This is a verification of the five specified
coefficient sets; the general symbolic expression above rests on its analytic
derivation, not on a numerical sweep presented as a polynomial identity proof.

All 4074 internal checks pass: Hermiticity, independent columns/powers,
norm, full component energies, carrier conservation, reflections, leading
coefficients, clock energies, immobility in hopping-off arms and the exact
decoupling identity. The root ran one worker after source review; no agent
ran or imported it. Wall time was 0.521806 seconds; peak self RSS 27,492,352
bytes. These checks establish finite-model consistency, not observations.

Complete initial energies are `4 Ud d*^2` and that value plus
`epsilon_psi`, conserved throughout. Four record clocks retain storage
energy `8(1-cos(sqrt5 x))/5` and the opposite writer-copy energy; neither is
dropped. The conserved source/empty energy difference remains epsilon_psi.
Redistribution of incidence occupation is not newly generated binding energy.

## Scope and next physical step

The result advances a native mechanism for influence beyond the occupied
node. It does not supply an operationally prepared second matter probe,
passive or inertial mass, a spatial ruler, a signal speed, a force direction,
an equilibrium work function, a density phase transition or a physical a0.
In particular, the positive nonincident occupation response must not simply
be renamed enhanced gravity. The graph's potential interaction support is
not its occupied transport graph.

The independent interpretation review confirms the coefficients and adds two
important limits. This finite preparation contrast is not itself a stationary
Kubo response or a passivity test. Also, hopping off freezes an otherwise
identical carrier probe as well as the source: one cannot use this control
as a stationary source while silently restoring mobility only for the probe.
In the hopping-on arm, source motion and recoil remain part of the dynamics.
The onsite term epsilon_psi P is constant inside each carrier-number sector;
the present response does not establish universal coupling to total energy.

The next useful matching problem is a matter probe and complete physical
source response on a justified formed state, with the same clock and ruler.
For the already studied local reversible isotropic comparison, a deep cubic
work law requires both transverse and longitudinal response coefficients,
with their factor-two relation and absolute normalization. These are existing
conditional requirements, not a new derivation. One must derive the source,
contact and actual-state response before testing that identification; another
larger blank-graph occupation series cannot substitute for it.

All Stage 1 through 3 obligations remain open. No astronomical fit, missing
dark fraction, continuum geometry or superiority claim changes here.

## Evidence identities

- Original BS action: `../recovered_sources/BS_MICRO_ACTION.md`, SHA256
  `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`.
- Source: `native_remote_loading_series_v001.py`, SHA256
  `002fb43c20f9c298a6b58352cb2150467d36654eced7e4eda64638e695a82747`.
- Result: `native_remote_loading_series_v001_results.json`, SHA256
  `e515c15108064d0cd91d3ea1fea2417fb2daed9a1a609c5d981e0f331988ccca`.
- Prior local result: `NATIVE_MATTER_LOADING_FORMATION_RESPONSE_V001.md`.
- Physical matching requirements: `NATIVE_SOURCE_BRIDGE_DECISION.md`,
  `NATIVE_ENERGY_DIPOLE_GRAVITY_BRIDGE_V001.md`, and
  `NATIVE_SHARED_WORK_INTEGRABILITY_V001.md`.

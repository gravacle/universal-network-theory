# The same content response does not admit a static microscopic lapse

2026-10-03 UTC. The prospective six-cycle test failed its source-energy
comparison with no numerical control failures. An independent exact-integer
Taylor calculation strengthens this to an exact exclusion of every real
static weak bulk lapse direction for this mixed response and fixed energy
readout. This is a result about the supplied resonant node preparation,
not an exclusion of UNT, gravity, time-dependent sources or a formed
coarse description. Withheld native probe targets were not evaluated.

## Frozen experiment and numerical result

The protocol is NATIVE_SAME_CONTENT_STATIC_SOURCE_PROTOCOL_V001.md and
the executable is native_same_content_static_source_v001.py. It retains
all 64 conserved record-X sectors of the actual blank records, each with
15 fixed-Q=2 carrier configurations. No record mean-field replacement is
made. E=h0+h1 is the unweighted conjugate-energy operator, including its
allocated hopping energy. The complete graph, carrier, writer and record
baselines remain in energy accounting. The full changing-incidence model
is not being numerically approximated by this small graph.

One single-threaded worker completed in 0.506 seconds with peak RSS
34,062,336 bytes on this Mac. Its result file is
NATIVE_SAME_CONTENT_STATIC_SOURCE_V001_RESULT.json. The two source columns
had rank two, singular values 0.0359795131426 and 0.00427359363503, and
condition number 8.41903. This is not failure from an unidentifiable fit.

The calibration-only least-squares coefficients were

    a=-0.0114448925324, b=-0.0172544393541.

Maximum absolute residuals were 1.87887051528e-5 on the four calibration
ages and 4.58460283680e-5 on the three validation ages. Both exceed the
prospectively fixed 1e-8 microscopic-energy tolerance. At the worst
validation age x=1.75, the mismatch is about 10.35 percent of the native
mixed energy signal. This percentage is descriptive, not a new criterion.
These are not observational uncertainties or errors in physical energy units.

All implemented numerical controls passed. The maximum eigen residual was 4.98e-14,
unitarity error 4.89e-15 and complete-energy conservation error 1.32e-14.
The independent central-difference derivative differed from the analytic
Frechet derivative by at most 7.05e-9, below its separate 3e-7 control
tolerance. Ordinary source-null and reflection checks also passed.

Review identified one coverage gap: explicit switching work was mentioned
in the protocol but was not saved as a numerical control by this script.
It is accounted for analytically here, not presented as an executed test.
For V_f=sum_v f_v h_v, an instantaneous switch to H+eta*V_f costs
eta*<V_f>. Baseline work is zero by odd parity; its eta*xi coefficient
under preparation B is Tr(sigma_0 M_B V_f)=-4*b/5. The graph and record
identity terms cancel in this signed trace, not from absolute energy.
Switching off at age x gives the mixed cycle work

    W_on_off[eta*xi]=<V_f>_B(0)-<V_f(x)>_B.

Here the subscript B is the preparation derivative evolved under the
unperturbed H, as required at this mixed order.

The same expression follows from the complete H energy change by
conservation under H+eta*V_f. This analytical identity does not assert
that the cycle work is zero or that source control is free. It does not
change any fit, gate or exact exclusion coefficient.

The failed source gate prevented evaluating any withheld native carrier
targets. There is no probe prediction score, no successful fit concealed
by selecting ages, and no subsequent expansion of the source family.

## An exact exclusion independent of the residual threshold

Let f=(a,-a,b,c,-c,-b) be the odd part of a static bulk lapse. Reflection
v -> 1-v makes E even and M_B odd, so the even part of ANY real static
profile has zero mixed kernel. The odd part therefore spans every direction
which this readout can see. The ordinary response vanishes sector by
sector, so a first probe-induced profile correction multiplying that
ordinary kernel cannot repair the mismatch. The isolated-clock term is
proportional to dot(b_B,E), which vanishes by the same reflection.

With kappa=1/15, the complete native mixed energy coefficient at x^2 is
zero: the two current-energy contractions 2*j*kappa cancel the allocated
hopping-energy contractions 2*j*kappa. Omitting the latter would give
an incorrect onset. The source coefficient is -(b+c)/120. Thus exact
correspondence requires c=-b, leaving f=a*f_A+b*f_D as frozen in the
protocol.

All local matrix entries are integer multiples of 1/4. The saved worker
computed nested commutators with arbitrary-precision integer arithmetic,
then divided by the exact sector count, carrier dimension and factorial.
This is independent of the spectral propagation and finite-difference
checks. The resulting exact coefficients are:

| Power of x | Native mixed E | Source column f_A | Source column f_D |
| --- | --- | --- | --- |
| 2 | 0 | 0 | 0 |
| 4 | -1/5760 | -7/1920 | 19/1920 |
| 6 | 1/19200 | 4777/1382400 | -1891/460800 |
| 8 | 19/1720320 | -10771/9676800 | 32149/38707200 |

Matching x^4 and x^6 uniquely requires

    a=-523/51052, b=-3265/153156.

These rational coefficients are an analytic witness, NOT the numerical
least-squares coefficients above. They produce the nonzero x^8 mismatch

    source minus native = -14691697/846891417600.

Finite-matrix response functions here are analytic in x. Consequently
exact equality on any open age interval would imply equality of these
Taylor coefficients and is impossible. This does not exclude approximate
late-time agreement at a separately justified tolerance or coarse readout.
It does exclude exact static weak-source correspondence for this readout,
even if an interval does not include the preparation boundary.

## A separate local record screen

Source-only review also identified an independent microscopic limitation,
which was not simulated or used to retune this experiment. On the degree-2
blank-record branch let w=g_w, g=g_p, rho=Q/V and
q_v=delta_A<p_v>=s*m_v. For record Pauli conventions
Y=i(|0><B|-|B><0|), Z=|B><B|-|0><0|, define

    A=w+g*rho, B=w^2+(2*w*g+g^2)*rho.

The native record responses begin -2*g*q_v*x for Y and
-2*g*(2*w+g)*q_v*x^2 for Z. A static relative lapse ell_v-ell_c gives
-2*A*ell_rel*x and -4*B*ell_rel*x^2. Matching both requires
rho=w/(2*w+g), which is 1/3 at inherited couplings. At that exceptional
filling, the cubic Y mismatch (native minus source) after matching its slope is

    -(2/3)[q_v+t^2 sum_(u~v)(q_u-q_v)]*x^3.

For degree two and t=1/2 this is -q_v*x^3/3 at a nonadjacent source
endpoint or -q_v*x^3/6 at an adjacent one. Thus a static microscopic
record dictionary fails there too. Bounded time profiles still face the
leading generic-filling condition, but a quadratic time component can
alter the exceptional cubic coefficient; that enlarged family is not
excluded by this argument. Record readouts are not the energy-only
calibration used in the numerical test.

## What the failure changes

Do not refine this source basis to manufacture a fit or run a larger
resonant grid to reconfirm the same failure. The static microscopic
dictionary has answered its question. A new source must instead have an
independently motivated temporal or coarse description, with its own
readout and preparation boundaries; a fit alone does not derive that law.

Ordinary carrier and conjugate-energy source responses vanish in the
resonant tracial sector even after arbitrary unchanged aging. That does
not generalize to detuned native records: the already saved
NATIVE_RECORD_DRIVEN_BAND_POPULATION_V001.md and frontier V115 establish
native carrier-population and complete-source responses off resonance.
The continuation should use those real mechanisms and examine the
generated state's collective response, rather than introducing another
external static profile. Native graph formation and physical source,
clock, ruler, volume and absolute-work interpretation remain unresolved.

## Evidence identities and review scope

Protocol SHA256:
07faf1d39df82ee78457922f2674820f111a5a127f20309eebbeaf45910d5d47.
Code SHA256:
562b36fa16fc85e760ccae166f25381ffd5ef7e3cd69f1123ae1ade00c3e65ac.
Result SHA256:
db678c5ae39a4a6497cebd5b1d3a0702458667cde60b7ec1fe2a495052991831.

Existing source-only reviewers checked the onset restriction, symmetry,
clock and contact scope, and independently verified the rational exclusion.
The local record screen was derived separately by handoff_plan_review_v005.
This is internal mathematical review, not external peer review or a new
astronomical comparison. All eleven scientific lanes remain open.

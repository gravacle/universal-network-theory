# Active formation: connected-state energy screen

2026-10-03. Analytical continuation; no numerical worker, fitted parameter,
new source coupling or physical-volume assignment. This narrows an actual
formation question before further simulation.

## Result and ancestry

Local record copying does not evade the existing positive-edge-cost
ground-state connectivity bound. Replacing the old held onsite reference by
the minimum of the COMPLETE local copying Hamiltonian extends that bound to
all native copy terms and finite fragments. A second, topology-sensitive
energy inequality limits the connected-graph probability of an explicitly
declared continuation of the actual writer-only blank preparation. Neither
waiting longer nor the single original switch-off can make that family
nearly certain to occupy a connected graph on all declared slab nodes.

The held theorem, sharp carrier estimate, degree-regime alternatives,
connected-backbone persistence and square-root-N formation-time bound are
ALREADY in NATIVE_RECORD_CONNECTIVITY_PATHWAY_V001.md. They are credited, not
rediscovered. The new steps are the all-copy local-energy reference and the
connected-topology preparation/switch-work budget below. This is not a
general exclusion of network geometry or energized network states.

## Full-copy extension of the prior bound

Use one original BS04–11 slab: N nodes per side, N^2 incidence qubits,
M=sum n_e, and h_N=Omega/N. Ports are off. Let U_d>=0 and lambda_R,lambda_J>=0;
all coefficients are fixed as N grows. Retain arbitrary local BS10 copy
couplings and a fixed finite number of fragments per node. Define

    H_loc = epsilon_psi sum_v q_psi,v + H_form,
    E_loc = min spectrum(H_loc),
    B_N = E_loc + 2N U_d d_*^2.

The full finite node-register space always qualifies. A restriction must
be independent of link factors AND invariant under the complete local,
feedback, transfer and current operators. Fixed total carrier numbers,
including carrier-content counts, qualify. Fixed record/fragment occupation
generally does not when copying is active. No marginal factorization is used.

From the exact BS qutrit transfer, T_e^2=J_e^2=P_one-carrier and

    -t T_e + lambda_J J_e^2 >= -c_psi I,
    c_psi=max(0,|t|-lambda_J).

Use the prior sharp coefficient

    kappa_R=Delta+2U_d(1-2d_*)-2lambda_R-c_psi.

Since q_r<=1, expanding degree squares gives an operator inequality

    H >= B_N + kappa_R M + 2U_d C_inc - (Omega/N) sum_e X_e,
    C_inc=sum_v sum_(e<f incident v) n_e n_f >=0.

Noncommutation of H_loc with feedback/hopping does not invalidate addition
of these operator lower bounds. Blank links tensored with a minimizing
local state have trial energy exactly B_N, so E_g<=B_N. The existing Bloch
and Cauchy–Schwarz bound gives |<sum X>|<=2 sqrt[m(N^2-m)], m=<M>. Hence,
for kappa_R>0, the full-copy ground satisfies

    m_g <= 4 Omega^2 N^2 / (kappa_R^2 N^2+4 Omega^2),
    Pr_g(connected on all 2N nodes) <= m_g/(2N-1).

Inherited parameters give c_psi=1/4, kappa_R=3/4 and m_g<64/9.
The new active-copy extension needs no assumptions about the sign or size
of individual copy energies: their actual minimum is in E_loc, not dropped.

For any state of excess energy delta_E=<H>-E_g>=0,

    kappa_R m-2 Omega sqrt(m) <= <H>-B_N <= delta_E,
    m <= [(Omega+sqrt(Omega^2+kappa_R delta_E))/kappa_R]^2.

Thus delta_E=o(N) also makes the all-node connected-incidence probability
vanish. General finite-temperature passive states can have delta_E=O(N),
so the word “passive” alone is NOT an exclusion criterion.

## A stronger connected-topology energy budget

For the inherited d_*=1, put eta=Delta-2lambda_R-c_psi=11/4 and U_d=1.
The incidence-diagonal lower-bound energy is

    D = eta M + U_d sum_v(d_v-1)^2.

Every graph has D>=2N U_d because kappa_R=eta-2U_d>0. A connected graph
has d_v>=1, M>=2N-1 and, by integer degrees,
sum(d_v-1)^2>=2M-2N. Consequently the exact diagonal-operator inequality is

    D >= 2N U_d + C_N Pi_connected,
    C_N = (2N-1)eta-2U_d >0.

An alternating Hamilton path attains the connected diagonal lower bound.
It need not minimize the full quantum Hamiltonian. For ANY actual state,
retaining every local copying term in E_loc and setting
epsilon=<H>-E_loc-2N U_d,

    C_N Pr(connected) <= epsilon+2 Omega sqrt(m),
    kappa_R m-2 Omega sqrt(m) <= epsilon.

For epsilon<=eN with e>=0 these give the explicit bound

    Pr(connected) <= min(1,
      [eN+2Omega*(Omega+sqrt(Omega^2+kappa_R eN))/kappa_R]/C_N).

In particular, limsup Pr(connected)<=e/(2eta). The flip correction is
O(sqrt(N)) here, not an omitted extensive supply. This is a necessary
preparation-energy screen; an adequate budget is not a formation theorem.

## Apply it to the inherited writer-only preparation family

Declare the natural fixed-coefficient N-extension of the saved one-link
experiment: every link and record blank initially; one carrier; 2N fixed
same-content occupied writers; g_wr=1, epsilon_r=epsilon_psi=1,
epsilon_w=0; carrier-to-record and fragment-copy couplings zero. Writer
storage and carrier energy are retained. This extension is a stated family,
not a measured cosmological initial condition or an all-copy example.

Each active local record has Hamiltonian Q+X and minimum
(1-sqrt(5))/2. In the legitimate fixed-writer, one-carrier sector,

    E_loc=1+N(1-sqrt(5)),
    E_initial=2N+1,
    epsilon=(sqrt(5)-1)N.

Autonomous g_wr=1 evolution conserves this complete energy. Therefore,
uniformly over its snapshot times,

    limsup_N Pr(connected) <= 2(sqrt(5)-1)/11 = 0.2247396323...

Now include the original SINGLE switch-off g_wr:1->0 at any pulse age T.
K_total=sum_v K_wr,v has norm 2N, so the exact switching work is
W=-<K_total> <=2N. After the quench, E=2N+1+W and the minimum of the held
local Hamiltonian on the full allowed record space is E_loc,held=1.
Thus epsilon_held=W<=2N and, uniformly over T and later held ages,

    limsup_N Pr(connected after one switch-off) <= 4/11 = 0.3636363636...

No switch work is erased; using the larger allowed record space for the
lower bound is not a postselection. These bounds do not apply unchanged to
additional pulses, incidence-changing ports or other energy supplies.
They concern unconditioned instantaneous probabilities, not cumulative
first-passage events, postselection, measurement feedback, or many attempts.

## Constructive direction and limits

An energized connected family remains possible. In the exact carrier-empty
or uniformly same-content-occupied sector, hopping and current terms vanish.
Retaining active local copies, let e(d)=min spectrum[h_loc-lambda_R d q_r].
A classical graph and degree-conditioned local minimizing states give

    E_trial(G)=sum_v f(d_v),
    f(d)=e(d)+U_d(d-d_*)^2+Delta*d/2.

An independently specified parameter regime with f(k)<f(0) supplies a lower
extensive-edge trial without pinning records by fiat. It does not prove the
ground has that degree: e(d) is concave, and degree coexistence or other
quantum states may compete. The prior held regular-degree examples already
show that degree preference alone cannot select connectivity or dimension.
No favorable new coefficient is adopted here.

The next useful formation calculation must specify its energy/source history
and identify what operationally counts as spatial support. A giant connected
component, virtual carrier propagation or a multislab history is not the
all-2N-node incidence event bounded here. Such alternatives must be evaluated
with their own clock/ruler readouts; this screen does not dismiss them.
Do not increase simulation time hoping to evade a conserved-energy bound,
or count all blank declared nodes as incorporated physical volume.

## Review and provenance

Root derived the full-copy extension and single-quench corollary. Agent
handoff_plan_review_v005 supplied the topology-sensitive budget and dressed
variational alternative; root checked their algebra. Agent
endpoint_equations_check independently challenged the extension, sector
conditions, budget and both preparation caps, and accepted the stated scope.
This is independent agent hand-algebra review, not external peer review or
empirical verification. No new numerical calculation was needed.

- Original BS_MICRO_ACTION.md SHA-256:
  `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`.
- Prior NATIVE_RECORD_CONNECTIVITY_PATHWAY_V001.md SHA-256:
  `81bbb3b72e00c03475b8efcc63c861907adb8b0da72bd50f27c89a6bc0b6775c`.
- Formation algebra SHA-256:
  `8c0c48a9cac4ed6e38137e6bb5d8067acb6d0440a424cb41b99a540667667c3c`.

No gravitational source, spatial dimension, absolute physical volume, cosmic
initial state, a0, dark-component replacement or Stage 3 completion is derived.

# Relative-energy mean-time interpretation V002

2026-10-05 UTC. Exact analytical interpretation of the chosen stationary control, supplementary to the frozen response protocol. No source method, state preparation, tolerance, physical parameter, natural relaxation or damping is adopted. The source calculation is active; no outcome of that new calculation is used here.

V002, 2026-10-05 22:21 UTC: seven displayed certified gap bounds are rounded downward. The original V001 remains preserved; formulas, exact certificate and source method are unchanged. The statement that the response calculation was active describes the V001 derivation time. Its producer has since closed; independent saved-data response audit remains pending.

## A measured algebra, rather than an invented relaxation law

The held network has H=Hrel+AR Q, [Hrel,Q]=0, with all physical H/AR energy retained. For the original prepared rho0,

    rho_H(u)=exp(-iH u) rho0 exp(+iH u),
    rho_tilde(u)=exp(+iAR Q u) rho_H(u) exp(-iAR Q u)
                =exp(-iHrel u) rho0 exp(+iHrel u).

The complete exact projector control is the infinite Cesaro mean:

    Drel(rho0)=lim_(T->infinity) (1/T) integral_0^T rho_tilde(u) du.

Every one of Vc,Vm,H,n,I commutes with Q. For their original prepared causal response at fixed lag tau>=0,

    chi_ab(u+tau,u)=i Tr[rho_tilde(u) [Oa_Hrel(tau),Ob]],
    lim_(T->infinity) (1/T) integral_0^T chi_ab(u+tau,u) du
                    =chi_ab,Drel(tau).

The same statement applies to owned q-diagonal direct contacts and mean source work. Thus the new stationary kernel has an exact interpretation as the mean over the initial age of the ORIGINAL dynamics on this algebra. No physical dephasing device, new bath or phenomenological relaxation function is required to prove this identity. It does not claim that rho_D itself is naturally prepared or that a finite observing window has reached the limit.

For each of the six nonendpoint jointly dressed record readouts,

    [Hrel,Rv+]=0,
    exp(-iAR u) <Rv+(u)>_rhoH = <Rv+>_rho0.

Their full co-rotating signals survive every finite mean exactly, including actual source/reference coherence. Null/AR0/tiny-amplitude and parent clock refusals remain. Endpoint readouts change loading s and their exact loading-root sets are disjoint, so their infinite co-rotating mean vanishes. This is averaging of their signal, not a claim that a physical endpoint record disappears.

## Finite-window bound

For Delta=E_i-E_j, the off-root coefficient of the finite mean is

    A_T(Delta)=exp(-iDelta T/2) sinc(Delta T/2),
    |A_T(Delta)|<=min(1,2/(|Delta|T)),
    sinc(x)=sin(x)/x.

For the q-diagonal algebra, let p_qi be the exact root-mode probabilities of the prepared state after tracing the held mixture/apparatus columns. Positivity gives |rho_qij|<=sqrt(p_qi p_qj). Put

    C=sum_q[(sum_i sqrt(p_qi))^2-sum_i p_qi],
    epsilon_T=min(2 Tr(rho0),2C/(g_min T)).

The trace norm of the difference of the q-twirled finite mean and q-twirled Drel state is at most epsilon_T. Here g_min is a positive exact lower bound for distinct same-loading energies; zero-gap coherent replicas remain in Drel. C<=111 Tr(rho0) in the112D tagged body sector and15 Tr(rho0) in the16D reference sector. This is a bound on the tested q-diagonal algebra, not the full cross-q density. For each causal commutator readout,

    |delta chi_ab(tau)|<=2 ||Oa|| ||Ob|| epsilon_T.

No target T, physical linewidth or measured time scale is selected. Native u=Eunit*t_physical/hbar; any finite observational-window assertion needs the global physical unit and an adequate bound. Averaging the initial age and the separate response-frequency/static limit are different operations. This proof does not qualify a physical zero-frequency response or finite numerical near-pole precision.

## Certified spectral resolution and exact observable symmetry

The existing rational root certificate gives the following same-loading gap lower bounds, in native energy units. They are literal integer-action interval bounds, not floating degeneracy cutoffs.

| sector | s0 | s1 | s2 |
|---|---:|---:|---:|
| tagged | 3.45942680723e-8 | 7.39746610634e-9 | 7.47677404433e-9 |
| reference | 0.000368735848314 | 0.000239865508046 | 0.000167989536566 |

All five source operators also commute with exact tagged species exchange S. Therefore coherences between opposite S sectors are invisible to this entire response algebra, without deleting a state or a genuine excitation. Restricting the bound to same-S pairs is allowed for these readouts. All14 adjacent tagged pairs below1e-6 (4,5,5 at s0,1,2) have opposite S. Each S sector has56 modes; the exact same-S lower gaps are:

| S | s0 | s1 | s2 |
|---|---:|---:|---:|
| +1 | 6.25192697043e-6 | 2.75242782663e-6 | 1.37626993819e-6 |
| -1 | 7.72325365687e-6 | 4.06887993449e-6 | 2.50053271884e-6 |

For an S-even algebra the corresponding restricted C sums only pairs within S and is at most55 Tr(rho0). Localized Vc/Vm need not commute with anchor reflection R, so R-odd transitions cannot be erased. The older separate holding sources can distinguish species and need not commute S; their genuine near odd response and all curvature refusals remain. Exact S selection supplies no permission to zero a small floating weight in the original response result. A separate saved-vector symmetry/error diagnostic may compare prospectively declared projected vectors while preserving every original mode/value.

## Frozen evidence

| resident path | SHA256 |
|---|---|
| FLOATING_RETURN_C8_RELATIVE_ENERGY_SPECTRAL_RESPONSE_V001.md | b8337f327c8503e505f2099c38bd61550ae005ca369a886fce076b9be802ed6a |
| FLOATING_RETURN_C8_RELATIVE_ENERGY_PROJECTOR_CERTIFICATE_V001.md | 3f89380ea9a8b042bcfa71e73460a455a50c067cb9e1f1da910d111eac3f17f3 |
| FLOATING_RETURN_C8_RELATIVE_ENERGY_PROJECTOR_CERTIFICATE_V001_RESULT.json | 584ce7064f7f388df6d1ddcd6465adb91c72c0098a86116d1cb289de533def9a |
| FLOATING_RETURN_C8_RELATIVE_ENERGY_PROJECTOR_CERTIFICATE_V001_RECEIPT.json | 99b96af6ba34e39cab489edfd1c898dca5dafe2d2ab2d8c38b2e70afdfc48fcb |
| LOCAL_RECORD_FEEDBACK_OCCUPIED_INCIDENCE_MEMORY_LAW_V001.md | 9239dcce75623cee38dd2ca4df78686b4d75f87d4baa975139549a29f15a0f26 |

Root derived the mean-time/finite-window identities and exact-gap/symmetry table; native independently checked their equations and algebra scope. The table comes from the accepted exact certificate, without a new eigensystem or history replay. Complete gravity/common-probe/galaxy-and-expansion tests remain required.
